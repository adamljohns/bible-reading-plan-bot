#!/usr/bin/env python3
"""fix_dangling_chips.py — repair dead related-chip links across the dictionary.

The 2026-06-09 corpus crawl found ~790 distinct chip targets (~1,034 chip
references) inside <div class="related"> blocks pointing at entry pages that
do not exist. Strategy, in priority order:

  1. KEEP      — target file actually exists (incl. special pages like
                 index.html, gen-z-decoded.html): the old auditor's slug-set
                 missed these; they are valid.
  2. RETARGET  — curated true-synonym map (verified at runtime), then safe
                 automatic rules ('-doctrine' strip, plural/singular,
                 'biblical-' prefix, '-place/-figure/-king/-prophet' swaps).
                 Duplicate chips created by a retarget are dropped.
  3. SKIP      — slugs scheduled for creation (batch authored from corpus
                 demand); their chips will resolve once the entry exists.
  4. REMOVE    — everything else: the dead anchor is deleted outright
                 (a chip promising a 404 is worse than no chip).

Every decision is logged. Run with --dry-run first.

Usage:
  python3 bin/fix_dangling_chips.py --dry-run
  python3 bin/fix_dangling_chips.py            # apply
"""
import argparse
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

RELATED_PAT = re.compile(r'(<div class="related">)(.*?)(</div>)', re.DOTALL)
CHIP_PAT = re.compile(r'<a href="([a-z0-9-]+)\.html">((?:(?!</a>).)*)</a>', re.DOTALL)

# Curated true-synonym retargets (target verified to exist at runtime).
CURATED = {
    'puritan': 'puritanism',
    'puritan-doctrine': 'puritanism',
    'puritans': 'puritanism',
    'kjv-vocabulary': 'king-james-version',
    'kjv': 'king-james-version',
    'substitutionary-atonement': 'penal-substitution',
    'divine-attributes': 'attributes-of-god',
    'martyrdom-doctrine': 'martyrdom',
    'reformation-doctrine': 'reformation',
    'sanhedrin-doctrine': 'sanhedrin',
    'godly-mother': 'motherhood',
    'fourth-commandment': 'sabbath',
    'cringe-slang': 'gen-z-decoded',
}

# Slugs being authored as new entries from corpus demand — leave their chips.
SKIP_CREATE = {
    'lbcf', 'westminster-shorter-catechism', 'kings-of-judah',
    'sermon-on-the-mount', 'protoevangelium', 'cappadocian-fathers',
    'gentile-inclusion', 'biblical-anthropology', 'vulgate',
    'second-commandment',
}


def existing_pages():
    return {fn[:-5] for fn in os.listdir(DICT_DIR) if fn.endswith('.html')}


def auto_retarget(slug, pages):
    """Safe mechanical alias rules; return existing target or None."""
    cands = []
    if slug.endswith('-doctrine'):
        cands.append(slug[:-9])
    if slug.startswith('biblical-'):
        cands.append(slug[9:])
    else:
        cands.append('biblical-' + slug)
    for suf in ('-place', '-figure', '-king', '-prophet', '-person'):
        if slug.endswith(suf):
            cands.append(slug[: -len(suf)])
        else:
            cands.append(slug + suf)
    if slug.endswith('es'):
        cands.append(slug[:-2])
    if slug.endswith('s'):
        cands.append(slug[:-1])
    else:
        cands.append(slug + 's')
    for c in cands:
        if c and c in pages:
            return c
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    pages = existing_pages()
    decisions = Counter()
    retarget_log = Counter()
    remove_log = Counter()
    files_changed = 0

    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html'):
            continue
        fp = os.path.join(DICT_DIR, fn)
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        m = RELATED_PAT.search(html)
        if not m:
            continue
        block = m.group(2)
        seen_targets = set()
        changed = False

        def fix_chip(cm):
            nonlocal changed
            slug, label = cm.group(1), cm.group(2)
            target = None
            if slug in pages:
                target = slug                       # KEEP (valid, incl. specials)
                decisions['keep'] += 1
            elif slug in SKIP_CREATE:
                decisions['skip-create'] += 1
                target = slug                       # leave dead chip; entry coming
            else:
                alias = CURATED.get(slug)
                if alias and alias in pages:
                    target = alias
                else:
                    alias = auto_retarget(slug, pages)
                    if alias:
                        target = alias
                if target:
                    decisions['retarget'] += 1
                    retarget_log[f'{slug} -> {target}'] += 1
                    changed = True
                else:
                    decisions['remove'] += 1
                    remove_log[slug] += 1
                    changed = True
                    return ''                       # REMOVE chip entirely
            if target in seen_targets:
                decisions['dedup-drop'] += 1
                changed = True
                return ''                           # duplicate chip after retarget
            seen_targets.add(target)
            if target == slug:
                return cm.group(0)
            return f'<a href="{target}.html">{label}</a>'

        new_block = CHIP_PAT.sub(fix_chip, block)
        if changed and new_block != block:
            new_html = html[:m.start(2)] + new_block + html[m.end(2):]
            if not args.dry_run:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_html)
            files_changed += 1

    print(f'{"DRY-RUN — " if args.dry_run else ""}dangling-chip repair complete.')
    print(f'  files changed:   {files_changed}')
    for k in ('keep', 'skip-create', 'retarget', 'remove', 'dedup-drop'):
        print(f'  {k:14s} {decisions[k]}')
    print('\nTop retargets:')
    for pair, n in retarget_log.most_common(20):
        print(f'  {n:4d}  {pair}')
    print(f'\nRemoved chip targets: {len(remove_log)} distinct '
          f'({sum(remove_log.values())} chips). Top 20:')
    for slug, n in remove_log.most_common(20):
        print(f'  {n:4d}  {slug}')


if __name__ == '__main__':
    main()
