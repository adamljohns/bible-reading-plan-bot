#!/usr/bin/env python3
"""dict_layout_audit.py — find dictionary entries whose PAGE LAYOUT departs
from the house pattern.

Adam, 2026-08-05: "ensure that we don't have any stray duplicated words that
have the wrong layout... it looked like it was made by a different model than
my normal model that I used to make words."

The KJV verifier checks what entries *say*; the drift audit checks their
*voice*. Nothing checked their *shape*. An entry authored outside the batch
pipeline can be perfectly orthodox and still be missing Webster, Roots,
Modern Corruption or a pronunciation — reading as a different kind of page
from the 6,765 that came through the pipeline.

House layout is defined empirically as the most common structural
fingerprint, not hardcoded, so the audit stays honest as the corpus evolves.

Usage:
  python3 bin/dict_layout_audit.py                 # summary + worst groups
  python3 bin/dict_layout_audit.py --list          # every non-conforming slug
  python3 bin/dict_layout_audit.py --missing roots # slugs lacking one part
  python3 bin/dict_layout_audit.py --out data/layout-outliers.txt
"""
import re, os, glob, sys, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs/dictionary')

# Pages that are indexes or themed collections, not word entries.
SPECIAL = set("""index names doctrinal-anchors biblical-order expressly-prohibited
most-corrupted gen-z-decoded millennial-decoded gen-x-decoded boomer-decoded
christianese-decoded jesus-generation changelog baby-names by-topic""".split())

# The structural parts a full house entry carries.
PARTS = {
    'pronunciation': r'class="pronunciation"',
    'etymology':     r'class="etymology"',
    'webster':       r'class="webster-inner"',
    'roots':         r'class="roots-inner"',
    'corruption':    r'class="corruption-inner"',
    'related':       r'class="related',
}

def redirect_slugs():
    """Merged entries keep a tiny stub page ('Abel Figure — merged into Abel')
    so the old URL never 404s. They are registered in the redirect registry and
    excluded from the slug count, so they must be excluded here too — otherwise
    ~440 legitimate stubs read as the worst layout outliers in the corpus."""
    path = os.path.join(ROOT, 'data/dictionary-redirects.txt')
    out = set()
    if os.path.exists(path):
        for line in open(path):
            parts = re.split(r'[\s,|>]+', line.strip())
            if parts and parts[0]:
                out.add(parts[0].lower())
    return out

def fingerprint(html):
    return tuple(k for k, pat in PARTS.items() if re.search(pat, html))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true', help='print every non-conforming slug')
    ap.add_argument('--missing', help='list slugs missing this part (%s)' % ', '.join(PARTS))
    ap.add_argument('--out', help='write non-conforming slugs here')
    args = ap.parse_args()

    shapes = collections.Counter()
    by_shape = collections.defaultdict(list)
    missing = collections.defaultdict(list)
    sizes = {}

    redirects = redirect_slugs()
    skipped_redirects = 0

    for f in sorted(glob.glob(os.path.join(DICT, '*.html'))):
        slug = os.path.basename(f)[:-5]
        if slug in SPECIAL:
            continue
        if slug.lower() in redirects:
            skipped_redirects += 1
            continue
        html = open(f, encoding='utf-8', errors='replace').read()
        fp = fingerprint(html)
        shapes[fp] += 1
        by_shape[fp].append(slug)
        sizes[slug] = len(html)
        for part in PARTS:
            if part not in fp:
                missing[part].append(slug)

    total = sum(shapes.values())
    house, house_n = shapes.most_common(1)[0]
    nonconf = [s for fp, slugs in by_shape.items() if fp != house for s in slugs]

    print(f'entry pages scanned : {total}   (redirect stubs skipped: {skipped_redirects})')
    print(f'house layout        : {", ".join(house)}')
    print(f'conforming          : {house_n} ({100*house_n/total:.1f}%)')
    print(f'NON-CONFORMING      : {len(nonconf)} ({100*len(nonconf)/total:.1f}%)')
    print(f'distinct layouts    : {len(shapes)}\n')

    print('missing part counts (across all entries):')
    for part in PARTS:
        n = len(missing[part])
        if n:
            print(f'  {part:14} absent from {n:5} entries')

    print('\nlargest non-conforming groups:')
    for fp, n in shapes.most_common():
        if fp == house:
            continue
        lack = [p for p in PARTS if p not in fp]
        ex = ', '.join(by_shape[fp][:6])
        print(f'  {n:5} entries — missing: {", ".join(lack) or "(none)"}')
        print(f'         e.g. {ex}')
        if n < 5:
            break

    # A short page missing several parts is the strongest "different model"
    # signal — orthodox content can still be the wrong kind of page.
    suspects = sorted(
        (s for s in nonconf if sizes[s] < 12000),
        key=lambda s: sizes[s])[:20]
    if suspects:
        print('\nthinnest non-conforming entries (most likely authored off-pipeline):')
        for s in suspects:
            fp = fingerprint(open(os.path.join(DICT, s + '.html'), encoding='utf-8', errors='replace').read())
            print(f'  {s:34} {sizes[s]:>7} bytes  missing: {", ".join(p for p in PARTS if p not in fp)}')

    if args.missing:
        part = args.missing
        if part not in PARTS:
            sys.exit(f'unknown part {part!r}; choose from {", ".join(PARTS)}')
        print(f'\nentries missing {part} ({len(missing[part])}):')
        for s in missing[part]:
            print(' ', s)

    if args.list:
        print(f'\nall non-conforming slugs ({len(nonconf)}):')
        for s in sorted(nonconf):
            print(' ', s)

    if args.out:
        with open(args.out, 'w') as fh:
            fh.write('\n'.join(sorted(nonconf)) + '\n')
        print(f'\nWrote {len(nonconf)} slugs -> {args.out}')

if __name__ == '__main__':
    main()
