#!/usr/bin/env python3
"""Backfill docs/assets/verse-cache.json from the BTE chapter files.

The cache is an aggregation of docs/assets/chapters/<book>_<chapter>.json and
had fallen 323 verses behind it (Job 35-42, Titus 2-3, 2 Peter 2-3, 1 John 2-5
whole, plus 11 scattered single verses) — every one of which exists in the
chapter files. Those holes are why verify_kjv_quotes.py carried a permanent
"uncached" class. STRICTLY ADDITIVE: existing cache entries are never touched,
so the MBT and readings lanes that share this cache are unaffected.

Usage: python3 bin/backfill_verse_cache.py [--dry-run]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')
CHAPTERS = os.path.join(ROOT, 'docs/assets/chapters')

def main():
    dry = '--dry-run' in sys.argv
    cache = json.load(open(CACHE))
    added = chapters_touched = 0
    for fn in sorted(os.listdir(CHAPTERS)):
        m = re.match(r'^(\d+)_(\d+)\.json$', fn)
        if not m:
            continue
        book, chap = m.group(1), m.group(2)
        try:
            data = json.load(open(os.path.join(CHAPTERS, fn)))
        except Exception as ex:
            print(f'skip {fn}: {ex}', file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        # {VERSION: {"1": "text", ...}} — invert to per-verse dicts
        verses = {}
        for version, vv in data.items():
            if not isinstance(vv, dict):
                continue
            for vnum, text in vv.items():
                if not str(vnum).isdigit() or not isinstance(text, str) or not text.strip():
                    continue
                verses.setdefault(vnum, {})[version] = text
        touched = False
        for vnum, versions in verses.items():
            key = f'{book}_{chap}_{vnum}'
            if key in cache:
                continue          # additive only — never rewrite an existing entry
            cache[key] = versions
            added += 1
            touched = True
        if touched:
            chapters_touched += 1
    print(f'added {added} verse entries from {chapters_touched} chapters '
          f'(cache now {len(cache)} entries)')
    if not dry and added:
        json.dump(cache, open(CACHE, 'w'), ensure_ascii=False)
    elif dry:
        print('--dry-run: nothing written')

if __name__ == '__main__':
    main()
