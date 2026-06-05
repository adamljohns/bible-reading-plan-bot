#!/usr/bin/env python3
"""
Smart duplicate finder for churches.json.

Identifies TRUE duplicates (same physical church, multiple records)
distinguished from legit multi-campus records (same network, different sites).

Criteria for TRUE duplicate:
- Same website domain
- AND (same street address OR very similar church name with same city)

Produces tmp/dedup_plan.json — a list of proposed merges with:
  canonical: ID to keep (most-enriched record)
  remove: [list of IDs to delete]
  conflict_fields: [differences that need reconciliation]
"""

import json
import os
import re
from collections import defaultdict

CHURCHES = 'docs/data/churches.json'
OUT = 'tmp/dedup_plan.json'
REPORT = 'tmp/dedup_report.md'


def normalize_domain(url):
    if not url: return ''
    m = re.search(r'https?://(?:www\.)?([^/?#]+)', url)
    return m.group(1).lower() if m else ''


def normalize_name(name):
    if not name: return ''
    n = name.lower().strip()
    # Strip generic church-type words so "Bent Tree Bible Fellowship" and "Bent Tree Bible
    # Church" collapse to the same key. (Domain + street fingerprint still guard the merge.)
    for w in ('church', 'chapel', 'baptist', 'sbc', 'pca', 'fellowship', 'community', 'ministries', 'ministry'):
        n = re.sub(r'\b' + w + r'\b', '', n)
    n = re.sub(r"[^a-z0-9]+", ' ', n).strip()
    return n


def extract_city_state(address):
    if not address: return '', ''
    parts = [p.strip() for p in address.split(',')]
    if len(parts) >= 2:
        city = parts[-2] if len(parts) >= 3 else parts[-1]
        # last part often has state+zip
        tail = parts[-1].strip()
        state_match = re.search(r'\b([A-Z]{2})\b', tail)
        state = state_match.group(1) if state_match else ''
        city = city.lower().strip()
        # Filter out placeholder phrases
        if any(ph in city for ph in ('see website', 'verify', 'unknown', 'multi-campus', '(see')):
            return '', ''
        return city, state
    return '', ''


def extract_street(address):
    if not address: return ''
    parts = [p.strip() for p in address.split(',')]
    return parts[0].lower().strip() if parts else ''


STREET_NUM_RE = re.compile(r'^\d{1,6}\s+[A-Za-z]')


def has_real_street(address):
    """True if address starts with a street number + letter (actual street, not a placeholder)."""
    if not address: return False
    return bool(STREET_NUM_RE.match(address.strip()))


def richness(church):
    """How 'filled out' is this record? Higher = better canonical pick."""
    score = 0
    if church.get('enrichment_sources'): score += len(church['enrichment_sources']) * 3
    if church.get('enrichment_notes'): score += 5
    if church.get('pastor_credentials'): score += 3
    if church.get('denomination_detail'): score += 2
    if church.get('founded'): score += 2
    if church.get('facebook'): score += 1
    if church.get('instagram'): score += 1
    # Length of score_notes
    sn = church.get('score_notes') or {}
    if isinstance(sn, dict):
        for v in sn.values():
            if isinstance(v, str): score += min(len(v), 200) / 20
    if church.get('engagement'):
        e = church['engagement']
        score += sum(1 for v in e.values() if v)
    # Recent review
    if church.get('overall_rating') in ('green', 'red', 'black'): score += 2
    return score


def main():
    data = json.load(open(CHURCHES))
    churches = data.get('churches') if isinstance(data, dict) else data

    # Index by domain
    by_domain = defaultdict(list)
    for c in churches:
        d = normalize_domain(c.get('website', ''))
        # Skip noisy directory-only domains (not real church sites)
        if d and d not in (
            'pca.org', 'efca.org', 'uua.org', 'mccchurch.org', 'wels.net',
            'lcms.org', 'arpchurch.org', 'opc.org', 'urcna.org',
            'acts29.com', 'faithstreet.com', 'churches.sbc.net', 'sbc.net',
            'bgav.org', 'floridacbf.org', 'eastcentralbaptist.net',
            'acna.org', 'goarch.org', 'oca.org', 'crechurches.org',
            'sovereigngracechurches.org', 'thepillarnetwork.com',
            'churchfinder.com', 'crec.org', 'facebook.com', 'instagram.com',
        ) and 'facebook.com' not in d and 'instagram.com' not in d:
            by_domain[d].append(c)

    # For each domain group, find true dupes
    merges = []
    for domain, group in by_domain.items():
        if len(group) < 2:
            continue

        # Bucket by (normalized_name, city, state) — same domain + same name + same city
        # Also requires a real street address to avoid placeholder-address merge traps
        by_key = defaultdict(list)
        for c in group:
            addr = c.get('address') or ''
            if not has_real_street(addr):
                continue  # skip records without a real street; too risky to dedup
            city, state = extract_city_state(addr)
            name_key = normalize_name(c.get('name', ''))
            # Drop the city name out of the church name so "<Name> <City>" buckets with "<Name>"
            # (this is exactly how Bent Tree's third record — "...Carrollton" — evaded the v1 pass).
            for tok in city.split():
                if len(tok) >= 4:
                    name_key = re.sub(r'\b' + re.escape(tok) + r'\b', '', name_key)
            name_key = re.sub(r'\s+', ' ', name_key).strip()
            if not city or not name_key:
                continue
            by_key[(name_key, city, state)].append(c)

        for key, cs in by_key.items():
            if len(cs) < 2:
                continue
            # Additionally require same street number to confirm same building
            street_buckets = defaultdict(list)
            for c in cs:
                street = extract_street(c.get('address', ''))
                # Use just the street number + first street word as the fingerprint
                m = re.match(r'^(\d+)\s+(\w+)', street)
                fp = f'{m.group(1)}-{m.group(2)}' if m else street[:20]
                street_buckets[fp].append(c)
            for fp, bucket in street_buckets.items():
                if len(bucket) < 2:
                    continue
                bucket.sort(key=richness, reverse=True)
                canonical = bucket[0]
                duplicates = bucket[1:]

                merges.append({
                    'domain': domain,
                    'city': key[1],
                    'state': key[2],
                    'street_fp': fp,
                    'canonical': {
                        'id': canonical['id'],
                        'name': canonical.get('name'),
                        'address': canonical.get('address'),
                        'rating': canonical.get('overall_rating'),
                        'richness': richness(canonical),
                    },
                    'duplicates': [{
                        'id': c['id'],
                        'name': c.get('name'),
                        'address': c.get('address'),
                        'rating': c.get('overall_rating'),
                        'richness': richness(c),
                    } for c in duplicates],
                    'total_dupes': len(duplicates),
                })

    # Sort merges by total impact
    merges.sort(key=lambda m: -m['total_dupes'])

    total_removals = sum(m['total_dupes'] for m in merges)

    print(f'Found {len(merges)} merge groups covering {total_removals} duplicate records')
    print(f'Directory would shrink from {len(churches)} → {len(churches) - total_removals}')

    json.dump(merges, open(OUT, 'w'), indent=2)
    print(f'Wrote {OUT}')

    # Human-readable report
    with open(REPORT, 'w') as f:
        f.write(f'# Dedup report — {len(merges)} merge groups, {total_removals} records to remove\n\n')
        f.write(f'Directory {len(churches)} → {len(churches) - total_removals} after merges.\n\n')
        f.write('## Rating conflicts within dup groups (need human attention)\n\n')
        for m in merges:
            ratings = {m['canonical']['rating']} | {d['rating'] for d in m['duplicates']}
            if len(ratings) > 1:
                f.write(f'- **{m["canonical"]["name"]}** ({m["city"]}, {m["state"]}): ratings = {sorted(ratings)}\n')
                f.write(f'  - canonical: {m["canonical"]["id"]} = {m["canonical"]["rating"]}\n')
                for d in m['duplicates']:
                    f.write(f'  - dupe: {d["id"]} = {d["rating"]}\n')

        f.write('\n## All merge groups\n\n')
        for m in merges:
            f.write(f'### {m["canonical"]["name"]} — {m["city"]}, {m["state"]} ({m["domain"]})\n')
            f.write(f'- **KEEP**: `{m["canonical"]["id"]}` ({m["canonical"]["rating"]}, richness={m["canonical"]["richness"]:.0f})\n')
            for d in m['duplicates']:
                f.write(f'- REMOVE: `{d["id"]}` ({d["rating"]}, richness={d["richness"]:.0f})\n')
            f.write('\n')
    print(f'Wrote {REPORT}')


if __name__ == '__main__':
    main()
