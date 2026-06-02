#!/usr/bin/env python3
"""backfill_canonical.py — add a <link rel="canonical"> to dictionary pages
that lack one.

The generator (generate_dict_entries.py) historically emitted og:url but no
canonical link, so every page it produced (recent batches especially) is
missing the canonical tag that the rest of the corpus has. This one-time
backfill derives the canonical URL from the filename and inserts the tag
immediately after <meta charset="UTF-8">, matching where existing pages have
it.

Idempotent: pages that already contain a canonical link are skipped.

Usage:
  python3 bin/backfill_canonical.py            # full run
  python3 bin/backfill_canonical.py --dry-run
"""
import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
BASE = 'https://usmcmin.org/dictionary/'

CHARSET_PAT = re.compile(r'(<meta charset="UTF-8">)', re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(DICT_DIR, '*.html')))
    added = 0
    skipped = 0
    no_anchor = 0
    for fp in files:
        slug = os.path.basename(fp)[:-5]
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        if 'rel="canonical"' in html:
            skipped += 1
            continue
        canon = f'    <link rel="canonical" href="{BASE}{slug}.html">'
        m = CHARSET_PAT.search(html)
        if not m:
            no_anchor += 1
            continue
        new_html = html[:m.end()] + '\n' + canon + html[m.end():]
        if not args.dry_run:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_html)
        added += 1

    print(f'{"DRY-RUN — " if args.dry_run else ""}canonical backfill complete.')
    print(f'  pages updated (canonical added): {added}')
    print(f'  pages already had canonical:     {skipped}')
    if no_anchor:
        print(f'  pages with no charset anchor:    {no_anchor}  (skipped)')


if __name__ == '__main__':
    main()
