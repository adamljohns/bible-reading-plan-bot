#!/usr/bin/env python3
"""kjv_wordlist.py — derive the complete KJV vocabulary and diff it against the
MOOP Dictionary, so expansion work is driven by the biblical text itself rather
than by brainstorming.

The dictionary's stated mission is that *every meaningful word in the Bible* is
covered for word study. Until now the runway to that goal has been assembled by
hand, block by block. This computes it: 30,706 cached KJV verses in, a ranked
list of words the Bible uses and the dictionary does not cover out.

Usage:
  python3 bin/kjv_wordlist.py                      # summary + top gaps
  python3 bin/kjv_wordlist.py --out data/kjv-gap.txt --limit 20000
  python3 bin/kjv_wordlist.py --min-freq 3 --commons-only
  python3 bin/kjv_wordlist.py --json data/kjv-gap.json
"""
import json, re, sys, html, argparse, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')
SLUGS = os.path.join(ROOT, 'data/dictionary-slugs.txt')
REDIRECTS = os.path.join(ROOT, 'data/dictionary-redirects.txt')

# Function words carry no word-study payload. Everything else in the KJV is
# fair game — including archaic verbs and inflections, which are exactly the
# words a modern reader stumbles on and looks up.
STOPWORDS = set("""
a an the and or but if of in on at to for with by from as is was are were be been
being am art be that this these those there here it its his her their our your my
me him them us you ye thou thee thy thine we they he she i o oh not no nor so then
than when where which who whom whose what how all any both each few more most other
some such only own same too very can will just should now shall unto up out down
into over under again further once about against between through during before
after above below off do does did doing have has had having would could may might
must let s t don
""".split())

def clean(s: str) -> str:
    """Mirror bin/kjv_lookup.py's normalization so both read the same text."""
    s = html.unescape(s)
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\d+', '', s)
    # Strip trailing KJV translator margin notes ("...the light from: Heb.
    # between the light and between the darkness"). Without this the note
    # markers themselves (Heb, Gr, Chald) rank as top-frequency "words".
    s = re.sub(r'\s+[A-Za-z][\w-]*:\s+(?:or|Heb|Gr|Gk|Chald|Chal|Called)\b.*$', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def slugify(word: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', word.lower()).strip('-')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', help='write plain candidate list here')
    ap.add_argument('--json', dest='json_out', help='write full structured report here')
    ap.add_argument('--limit', type=int, default=0, help='cap candidates written')
    ap.add_argument('--min-freq', type=int, default=1)
    ap.add_argument('--commons-only', action='store_true',
                    help='exclude probable proper nouns (always capitalized in KJV)')
    args = ap.parse_args()

    cache = json.load(open(CACHE))
    freq = collections.Counter()
    lower_seen = collections.Counter()   # times the word appears lowercase
    total_seen = collections.Counter()
    first_ref = {}
    verses = 0

    for key, val in cache.items():
        if not isinstance(val, dict) or 'KJV' not in val:
            continue
        verses += 1
        text = clean(val['KJV'])
        for m in re.finditer(r"[A-Za-z][A-Za-z'-]*", text):
            raw = m.group(0).strip("'-")
            if len(raw) < 2:
                continue
            low = raw.lower()
            total_seen[low] += 1
            if raw[0].islower():
                lower_seen[low] += 1
            if low not in first_ref:
                first_ref[low] = key
            if low in STOPWORDS:
                continue
            freq[low] += 1

    # A word that NEVER appears lowercase anywhere in the KJV is almost certainly
    # a proper noun (Abraham, Jerusalem). One that sometimes does is a common
    # word that merely started a sentence.
    def is_proper(w):
        return lower_seen[w] == 0

    have = set()
    if os.path.exists(SLUGS):
        have |= {l.strip().lower() for l in open(SLUGS) if l.strip()}
    if os.path.exists(REDIRECTS):
        for l in open(REDIRECTS):
            parts = re.split(r'[\s,|>]+', l.strip())
            if parts and parts[0]:
                have.add(parts[0].lower())

    covered, missing = [], []
    for w, n in freq.items():
        if n < args.min_freq:
            continue
        if args.commons_only and is_proper(w):
            continue
        (covered if slugify(w) in have else missing).append((w, n))

    missing.sort(key=lambda x: (-x[1], x[0]))
    covered.sort(key=lambda x: (-x[1], x[0]))

    prop = [w for w, _ in missing if is_proper(w)]
    comm = [w for w, _ in missing if not is_proper(w)]

    print(f'KJV verses read:            {verses}')
    print(f'Distinct KJV words:         {len(total_seen)}')
    print(f'  minus stopwords:          {len(freq)}')
    print(f'Dictionary slugs on file:   {len(have)}')
    print()
    print(f'ALREADY COVERED:            {len(covered)}')
    print(f'NOT YET COVERED:            {len(missing)}')
    print(f'   probable proper nouns:   {len(prop)}')
    print(f'   common vocabulary:       {len(comm)}')
    print()
    print('Top 40 uncovered by frequency:')
    for w, n in missing[:40]:
        tag = 'proper' if is_proper(w) else 'common'
        print(f'   {w:22} {n:6}  {tag}  (first: {first_ref[w]})')

    band = lambda lo, hi: sum(1 for _, n in missing if lo <= n <= hi)
    print()
    print('Uncovered by frequency band:')
    for lo, hi, label in [(100, 10**9, '100+'), (25, 99, '25-99'), (10, 24, '10-24'),
                          (3, 9, '3-9'), (2, 2, '2'), (1, 1, '1 (hapax)')]:
        print(f'   {label:10} {band(lo, hi):6}')

    out_list = [w for w, _ in missing]
    if args.limit:
        out_list = out_list[:args.limit]

    if args.out:
        with open(args.out, 'w') as f:
            f.write('\n'.join(out_list) + '\n')
        print(f'\nWrote {len(out_list)} candidates -> {args.out}')

    if args.json_out:
        report = {
            'generated_from': 'docs/assets/verse-cache.json',
            'kjv_verses_read': verses,
            'distinct_words': len(total_seen),
            'covered': len(covered),
            'missing': len(missing),
            'missing_proper': len(prop),
            'missing_common': len(comm),
            'candidates': [
                {'word': w, 'freq': n, 'slug': slugify(w),
                 'proper_noun': is_proper(w), 'first_ref': first_ref[w]}
                for w, n in (missing[:args.limit] if args.limit else missing)
            ],
        }
        with open(args.json_out, 'w') as f:
            json.dump(report, f, indent=1)
        print(f'Wrote structured report -> {args.json_out}')

if __name__ == '__main__':
    main()
