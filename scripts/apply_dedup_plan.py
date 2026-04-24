#!/usr/bin/env python3
"""
Apply the dedup plan produced by find_true_duplicates.py:
1. For each merge group, keep the canonical record but fold in useful fields
   from all duplicates (union sources, concat notes, prefer best rating).
2. Remove the duplicate records from churches.json.

Merge rules:
- enrichment_sources: union (preserving unique URLs)
- enrichment_sources_live: union
- enrichment_notes: concatenate with "\n— Merged from <id>: ..." markers
- score_notes: for each key, keep the longer non-placeholder string
- overall_rating: prefer non-yellow over yellow (green/red/black win)
- scores: for each key, prefer non-yellow
- facebook/instagram/pastor: keep canonical's, fill empty from duplicates

Usage:
    python3 scripts/apply_dedup_plan.py [--dry-run]
"""

import argparse
import json
import os
import sys

CHURCHES = 'docs/data/churches.json'
PLAN = 'tmp/dedup_plan.json'


NON_YELLOW_PRIORITY = {'green': 3, 'red': 4, 'black': 5, 'yellow': 2, 'unknown': 1, None: 0}


def better_rating(a, b):
    """Pick the 'more decisive' rating between two. Priorities: black > red > green > yellow > unknown."""
    return a if NON_YELLOW_PRIORITY.get(a, 0) >= NON_YELLOW_PRIORITY.get(b, 0) else b


def merge_source_lists(canonical_list, dup_list):
    """Union two lists preserving order, deduping."""
    seen = set()
    out = []
    for item in (canonical_list or []) + (dup_list or []):
        if item and item not in seen:
            out.append(item)
            seen.add(item)
    return out


def better_note(a, b):
    """Pick longer non-placeholder note."""
    if not a: return b
    if not b: return a
    placeholders = ('verify', 'unknown', 'not stated', 'not verified', 'tbd')
    a_ph = any(p in a.lower() for p in placeholders)
    b_ph = any(p in b.lower() for p in placeholders)
    if a_ph and not b_ph: return b
    if b_ph and not a_ph: return a
    return a if len(a) >= len(b) else b


def merge_records(canonical, duplicates):
    """Merge duplicates INTO canonical, returning the merged record."""
    merged = dict(canonical)  # shallow copy

    for dup in duplicates:
        # Union enrichment_sources
        merged['enrichment_sources'] = merge_source_lists(
            merged.get('enrichment_sources'),
            dup.get('enrichment_sources'),
        )
        if dup.get('enrichment_sources_live') or merged.get('enrichment_sources_live'):
            merged['enrichment_sources_live'] = merge_source_lists(
                merged.get('enrichment_sources_live'),
                dup.get('enrichment_sources_live'),
            )

        # Concat enrichment_notes
        c_notes = merged.get('enrichment_notes') or ''
        d_notes = dup.get('enrichment_notes') or ''
        if d_notes and d_notes != c_notes:
            sep = '\n--- Merged from ' + dup.get('id', '?') + ': '
            merged['enrichment_notes'] = (c_notes + sep + d_notes).strip()

        # For each score_note key, keep the longer
        c_sn = merged.get('score_notes') or {}
        d_sn = dup.get('score_notes') or {}
        if isinstance(c_sn, dict) and isinstance(d_sn, dict):
            new_sn = dict(c_sn)
            for k, v in d_sn.items():
                new_sn[k] = better_note(c_sn.get(k), v)
            merged['score_notes'] = new_sn

        # For each individual score, prefer non-yellow
        c_scores = merged.get('scores') or {}
        d_scores = dup.get('scores') or {}
        if isinstance(c_scores, dict) and isinstance(d_scores, dict):
            new_scores = dict(c_scores)
            for k, v in d_scores.items():
                new_scores[k] = better_rating(c_scores.get(k), v)
            merged['scores'] = new_scores

        # Overall rating: prefer non-yellow
        merged['overall_rating'] = better_rating(merged.get('overall_rating'), dup.get('overall_rating'))
        if merged['overall_rating'] != canonical.get('overall_rating'):
            # Update overall_label to match
            label_map = {
                'green': 'Aligned with Historic Orthodoxy',
                'red': 'WARNING!',
                'black': 'WARNING! — Critical Divergence',
                'yellow': 'Mixed — Caution in Top Priority',
            }
            merged['overall_label'] = label_map.get(merged['overall_rating'], merged.get('overall_label', ''))

        # Fill empty social/pastor fields
        for field in ('facebook', 'instagram', 'youtube', 'pastor', 'pastor_credentials', 'founded', 'denomination_detail'):
            if not merged.get(field) and dup.get(field):
                merged[field] = dup[field]

        # Engagement: union of true flags
        c_eng = merged.get('engagement') or {}
        d_eng = dup.get('engagement') or {}
        if isinstance(c_eng, dict) and isinstance(d_eng, dict):
            new_eng = dict(c_eng)
            for k, v in d_eng.items():
                if v and not new_eng.get(k):
                    new_eng[k] = v
            merged['engagement'] = new_eng

        # Tags: union
        c_tags = set(merged.get('tags') or [])
        d_tags = set(dup.get('tags') or [])
        if c_tags or d_tags:
            merged['tags'] = sorted(c_tags | d_tags)

    # Record merge metadata
    merged_from = [d['id'] for d in duplicates]
    existing = merged.get('merged_from') or []
    merged['merged_from'] = existing + merged_from

    return merged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(PLAN):
        sys.exit(f'No plan at {PLAN} — run find_true_duplicates.py first')

    plan = json.load(open(PLAN))
    data = json.load(open(CHURCHES))
    churches = data.get('churches') if isinstance(data, dict) else data
    by_id = {c['id']: c for c in churches if c.get('id')}

    to_remove_ids = set()
    rating_changes = []
    merges_applied = 0

    for m in plan:
        canonical_id = m['canonical']['id']
        dup_ids = [d['id'] for d in m['duplicates']]

        canonical = by_id.get(canonical_id)
        if not canonical:
            print(f'WARN: canonical {canonical_id} missing from churches')
            continue

        # Find full dup records
        dup_records = [by_id[d] for d in dup_ids if d in by_id]
        if not dup_records:
            continue

        old_rating = canonical.get('overall_rating')
        merged = merge_records(canonical, dup_records)
        new_rating = merged.get('overall_rating')

        if new_rating != old_rating:
            rating_changes.append((canonical_id, old_rating, new_rating))

        # Replace canonical in churches list
        for i, c in enumerate(churches):
            if c.get('id') == canonical_id:
                churches[i] = merged
                break

        to_remove_ids.update(dup_ids)
        merges_applied += 1

    # Remove duplicates
    churches = [c for c in churches if c.get('id') not in to_remove_ids]

    print(f'Applied {merges_applied} merges')
    print(f'Removed {len(to_remove_ids)} duplicate records')
    print(f'Directory: {len(by_id)} → {len(churches)}')
    print(f'Rating upgrades from merge: {len(rating_changes)}')
    for cid, old, new in rating_changes[:20]:
        print(f'  {cid}: {old} → {new}')
    if len(rating_changes) > 20:
        print(f'  ...and {len(rating_changes)-20} more')

    if args.dry_run:
        print('DRY RUN — no changes written')
        return

    if isinstance(data, dict):
        data['churches'] = churches
        data['total_churches'] = len(churches)
        json.dump(data, open(CHURCHES, 'w'), indent=2)
    else:
        json.dump(churches, open(CHURCHES, 'w'), indent=2)
    print('Wrote updated churches.json')


if __name__ == '__main__':
    main()
