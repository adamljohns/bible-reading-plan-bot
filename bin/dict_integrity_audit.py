#!/usr/bin/env python3
"""dict_integrity_audit.py — one-command structural health check for the
entire MOOP Dictionary corpus.

Consolidates the checks proven out in the 2026-06-09 Fable corpus crawl so any
future session can verify the dictionary with a single command. Run it after
every batch session and before declaring the corpus stable.

HARD checks (any failure -> exit 1):
  1. page/slug/file consistency  — every slug has a page; orphan pages listed
  2. canonical                   — every entry page carries <link rel="canonical">
  3. nested anchors              — no <a> inside <a> anywhere in entry pages
  4. dangling related-chips      — every chip in <div class="related"> resolves
                                   to a real file (special pages count as valid)
  5. dead lexicon links          — every ../lexicon/<ID>.html target exists
  6. HTML entities               — only standard named entities + macron set
  7. WOTD pools                  — dict-index + lexicon Word-of-the-Day targets exist
  8. manifest                    — parses, and every manifest slug resolves

SOFT checks (reported, never fail the run):
  9. duplicate display titles    — possible duplicate entries to review
 10. section completeness        — counts of entries missing webster /
                                   corruption / usage sections (era debt)

Usage:
  python3 bin/dict_integrity_audit.py            # full report
  python3 bin/dict_integrity_audit.py --quiet    # summary + failures only
"""
import argparse
import html.entities
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
LEX_DIR = os.path.join(ROOT, 'docs', 'lexicon')
SLUGS_FILE = os.path.join(ROOT, 'data', 'dictionary-slugs.txt')
MANIFEST = os.path.join(DICT_DIR, 'manifest.json')
LEX_INDEX = os.path.join(ROOT, 'docs', 'lexicon.html')

SPECIAL = {'index', 'template', 'names', 'baby-names', 'by-topic',
           'doctrinal-anchors', 'biblical-order', 'expressly-prohibited',
           'most-corrupted', 'gen-z-decoded', 'millennial-decoded',
           'gen-x-decoded', 'boomer-decoded', 'changelog'}

VALID_ENTS = set(html.entities.name2codepoint) | {
    'amacr', 'emacr', 'imacr', 'omacr', 'umacr', 'aelig', 'thorn'}

RELATED_PAT = re.compile(r'<div class="related">(.*?)</div>', re.DOTALL)
CHIP_PAT = re.compile(r'<a href="([a-z0-9-]+)\.html">')
LEXLINK_PAT = re.compile(r'href="\.\./lexicon/([HG]\d+)\.html"')
ENT_PAT = re.compile(r'&([a-zA-Z][a-zA-Z0-9]*);')
TITLE_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')


def fail_list(name, items, quiet, cap=15):
    n = len(items)
    status = 'OK' if n == 0 else f'FAIL ({n})'
    print(f'  [{status:>9}] {name}')
    if n and not quiet:
        for it in items[:cap]:
            print(f'      - {it}')
        if n > cap:
            print(f'      ... and {n - cap} more')
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    pages = {f[:-5] for f in os.listdir(DICT_DIR) if f.endswith('.html')}
    entry_pages = pages - SPECIAL
    slugs = {l.strip() for l in open(SLUGS_FILE) if l.strip()}
    lex_pages = {f[:-5] for f in os.listdir(LEX_DIR) if f.endswith('.html')}

    missing_pages = sorted(slugs - pages)
    orphan_pages = sorted(entry_pages - slugs)

    no_canonical, nested, dangling, dead_lex, bad_ents = [], [], [], [], []
    titles = Counter()
    miss_webster = miss_corr = miss_usage = 0

    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html'):
            continue
        slug = fn[:-5]
        with open(os.path.join(DICT_DIR, fn), encoding='utf-8',
                  errors='ignore') as f:
            h = f.read()

        if slug not in SPECIAL and 'rel="canonical"' not in h:
            no_canonical.append(slug)

        # nested anchors: token walk tracking <a> depth
        depth = 0
        for tok in re.split(r'(<[^>]+>)', h):
            if tok.startswith('<a ') or tok == '<a>':
                depth += 1
                if depth > 1:
                    nested.append(slug)
                    break
            elif tok.startswith('</a'):
                depth = max(0, depth - 1)

        m = RELATED_PAT.search(h)
        if m:
            for target in CHIP_PAT.findall(m.group(1)):
                if target not in pages:
                    dangling.append(f'{slug} -> {target}')

        for lid in LEXLINK_PAT.findall(h):
            if lid not in lex_pages:
                dead_lex.append(f'{slug} -> {lid}')

        bad = set(ENT_PAT.findall(h)) - VALID_ENTS
        if bad:
            bad_ents.append(f'{slug}: {sorted(bad)[:4]}')

        if slug not in SPECIAL:
            tm = TITLE_PAT.search(h)
            if tm:
                titles[TAG_STRIP.sub('', tm.group(1)).strip().lower()] += 1
            if 'webster' not in h.lower():
                miss_webster += 1
            if 'corruption' not in h.lower():
                miss_corr += 1
            if '>Usage<' not in h and 'usage' not in h.lower():
                miss_usage += 1

    # WOTD pools
    wotd_bad = []
    idx = open(os.path.join(DICT_DIR, 'index.html'), encoding='utf-8').read()
    wm = re.search(r'var WOTD = \[(.*?)\];', idx, re.DOTALL)
    if wm:
        for s in re.findall(r"slug:'([a-z0-9-]+)'", wm.group(1)):
            if s not in pages:
                wotd_bad.append(f'dict-index WOTD -> {s}')
    else:
        wotd_bad.append('dict-index WOTD pool not found')
    lexidx = open(LEX_INDEX, encoding='utf-8').read()
    for num in re.findall(r"num:'([HG]\d+)'", lexidx):
        if num not in lex_pages:
            wotd_bad.append(f'lexicon WOTD -> {num}')

    # manifest
    manifest_bad = []
    try:
        man = json.load(open(MANIFEST, encoding='utf-8'))
        man_slugs = set()
        if isinstance(man, dict):
            for v in man.values():
                if isinstance(v, str):
                    man_slugs.add(v)
                elif isinstance(v, dict) and 'slug' in v:
                    man_slugs.add(v['slug'])
        elif isinstance(man, list):
            for v in man:
                if isinstance(v, dict) and 'slug' in v:
                    man_slugs.add(v['slug'])
        manifest_bad = sorted(s for s in man_slugs if s not in pages)[:50]
    except Exception as e:
        manifest_bad = [f'manifest unreadable: {e}']

    dupes = sorted(t for t, c in titles.items() if c > 1)

    print('=' * 62)
    print('MOOP DICTIONARY INTEGRITY AUDIT')
    print(f'  entry pages: {len(entry_pages)}   slugs: {len(slugs)}   '
          f'special pages: {len(pages & SPECIAL)}   lexicon: {len(lex_pages)}')
    print('=' * 62)
    hard = 0
    hard += fail_list('slugs without a page', missing_pages, args.quiet)
    hard += fail_list('entry pages missing from slugs.txt', orphan_pages, args.quiet)
    hard += fail_list('pages missing canonical', no_canonical, args.quiet)
    hard += fail_list('nested anchors', nested, args.quiet)
    hard += fail_list('dangling related-chips', dangling, args.quiet)
    hard += fail_list('dead lexicon links', dead_lex, args.quiet)
    hard += fail_list('invalid HTML entities', bad_ents, args.quiet)
    hard += fail_list('broken Word-of-the-Day targets', wotd_bad, args.quiet)
    hard += fail_list('manifest slugs without pages', manifest_bad, args.quiet)
    print('-' * 62)
    print('  SOFT (era debt / review items, not failures):')
    print(f'    duplicate display titles: {len(dupes)}'
          + ('' if args.quiet or not dupes else
             '\n      ' + ', '.join(dupes[:12]) + ('...' if len(dupes) > 12 else '')))
    print(f'    entries lacking a Webster section:    {miss_webster}')
    print(f'    entries lacking a Corruption section: {miss_corr}')
    print(f'    entries lacking a Usage section:      {miss_usage}')
    print('=' * 62)
    if hard:
        print(f'RESULT: FAIL — {hard} hard finding(s). Fix before declaring stable.')
        sys.exit(1)
    print('RESULT: PASS — corpus structurally sound.')


if __name__ == '__main__':
    main()
