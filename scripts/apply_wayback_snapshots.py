#!/usr/bin/env python3
"""
Phase 2 post-process: take the wayback_snapshots.json mapping produced by
wayback_archive_sources.py and rewrite enrichment_sources in churches.json
to use the archived URLs.

Adds `enrichment_sources_live` with the original URLs preserved for audit,
and `enrichment_sources_archived_at` with capture timestamp.

Usage:
    python3 scripts/apply_wayback_snapshots.py [--dry-run]
"""

import argparse
import json
import os
import sys

CHURCHES = 'docs/data/churches.json'
SNAPSHOTS = 'tmp/wayback_snapshots.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(SNAPSHOTS):
        sys.exit(f'No snapshots file at {SNAPSHOTS} — run wayback_archive_sources.py first')

    snaps = json.load(open(SNAPSHOTS))
    data = json.load(open(CHURCHES))
    churches = data.get('churches') if isinstance(data, dict) else data

    changed = 0
    urls_rewritten = 0
    churches_touched = 0

    for c in churches:
        rating = c.get('overall_rating')
        if rating not in ('green', 'red', 'black'):
            continue
        sources = c.get('enrichment_sources') or []
        if not sources:
            continue

        new_sources = []
        live_sources = []
        rewrites_here = 0
        for u in sources:
            if not isinstance(u, str) or not u.strip():
                continue
            if u in snaps and 'archived' in snaps[u]:
                archived = snaps[u]['archived']
                if archived and archived != u:
                    new_sources.append(archived)
                    live_sources.append(u)
                    rewrites_here += 1
                    continue
            new_sources.append(u)
            live_sources.append(u)

        if rewrites_here > 0:
            c['enrichment_sources'] = new_sources
            c['enrichment_sources_live'] = live_sources
            c['enrichment_sources_archived'] = True
            churches_touched += 1
            urls_rewritten += rewrites_here
            changed = 1

    print(f'Rewrote {urls_rewritten} URLs across {churches_touched} churches')

    if args.dry_run:
        print('Dry run — not writing churches.json')
        return

    if changed:
        if isinstance(data, dict):
            data['churches'] = churches
            json.dump(data, open(CHURCHES, 'w'), indent=2)
        else:
            json.dump(churches, open(CHURCHES, 'w'), indent=2)
        print('Wrote updated churches.json')
    else:
        print('No changes to write')


if __name__ == '__main__':
    main()
