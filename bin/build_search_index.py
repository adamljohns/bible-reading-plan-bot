#!/usr/bin/env python3
"""build_search_index.py — keep docs/dictionary/search-index.json level with the corpus.

The file is served publicly (https://usmcmin.org/dictionary/search-index.json)
but nothing built it: it was hand-patched, and by 2026-10-03 it held 4,252 of
12,303 entries. This script maintains it on an ADDITIVE rule, because a full
regeneration from page <meta> would overwrite ~1,400 curated descriptions with
template boilerplate.

  - every slug in data/dictionary-slugs.txt gets a row {s, t, p, d}
  - an existing row is never rewritten; only a BLANK t / p / d is filled
  - new rows take: t = the page's word-title, p = its part-of-speech pill,
    d = the first 280 characters of its Biblical Definition
  - a row whose page no longer exists is dropped (it could only 404)
  - a row whose page is a redirect stub is dropped: the stub's canonical entry
    already has its own row, so keeping both gives two hits for one entry,
    one of them carrying superseded text (PJG review of 10-03: 391 such rows,
    e.g. belt-truth beside belt-of-truth)
  - rows are kept sorted by slug; "count" is the row count

Idempotent: run on a level corpus it rewrites nothing.

  python3 bin/build_search_index.py            # write
  python3 bin/build_search_index.py --check    # report only, exit 1 if stale
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
SLUGS = os.path.join(ROOT, 'data', 'dictionary-slugs.txt')
OUT = os.path.join(DICT_DIR, 'search-index.json')

TITLE = re.compile(r'<div class="word-title">(.*?)</div>', re.S)
POS = re.compile(r'class="pos"[^>]*>(.*?)<', re.S)
BDEF = re.compile(r'<div class="biblical-def"[^>]*>(.*?)</div>', re.S)
META = re.compile(r'<meta name="description" content="([^"]*)"')
TAGS = re.compile(r'<[^>]+>')
# Merge stubs carry <!-- MERGED-REDIRECT -->; older hand-made ones (chesed.html)
# only a meta refresh. Either way the head is tiny, so 1,200 bytes is plenty.
REDIRECT = re.compile(r'MERGED-REDIRECT|http-equiv="refresh"', re.I)


def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(TAGS.sub('', s or ''))).strip()


def is_redirect(slug):
    with open(os.path.join(DICT_DIR, slug + '.html'), encoding='utf-8', errors='ignore') as f:
        return bool(REDIRECT.search(f.read(1200)))


def from_page(slug):
    with open(os.path.join(DICT_DIR, slug + '.html'), encoding='utf-8', errors='ignore') as f:
        h = f.read()
    t = TITLE.search(h)
    p = POS.search(h)
    d = BDEF.search(h)
    desc = clean(d.group(1))[:280] if d else ''
    if not desc:
        m = META.search(h)
        desc = clean(m.group(1))[:280] if m else ''
    return {'t': clean(t.group(1)) if t else slug.replace('-', ' ').title(),
            'p': clean(p.group(1)) if p else '', 'd': desc}


def main():
    check = '--check' in sys.argv
    raw = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
    data = json.loads(raw) if raw else {'v': 1, 'count': 0, 'entries': []}
    rows = {r['s']: r for r in data['entries']}
    slugs = [l.strip() for l in open(SLUGS, encoding='utf-8') if l.strip()]

    added = filled = dropped = stubs = 0
    for s in list(rows):
        if not os.path.exists(os.path.join(DICT_DIR, s + '.html')):
            del rows[s]
            dropped += 1
        elif is_redirect(s):
            del rows[s]
            stubs += 1
    for s in slugs:
        if not os.path.exists(os.path.join(DICT_DIR, s + '.html')) or is_redirect(s):
            continue
        r = rows.get(s)
        if r is None:
            rows[s] = dict(s=s, **from_page(s))
            added += 1
            continue
        if not all((r.get(k) or '').strip() for k in ('t', 'p', 'd')):
            page = from_page(s)
            for k in ('t', 'p', 'd'):
                if not (r.get(k) or '').strip() and page[k]:
                    r[k] = page[k]
                    filled += 1

    data['entries'] = [rows[s] for s in sorted(rows)]
    data['count'] = len(data['entries'])
    out = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    if raw.endswith('\n'):
        out += '\n'
    stale = out != raw
    print(f'search-index: {data["count"]} rows | added {added} | blank fields filled {filled} '
          f'| dropped (no page) {dropped} | dropped (redirect stub) {stubs} | {"STALE" if stale else "level"}')
    if check:
        sys.exit(1 if stale else 0)
    if stale:
        with open(OUT, 'w', encoding='utf-8') as f:
            f.write(out)


if __name__ == '__main__':
    main()
