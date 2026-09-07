#!/usr/bin/env python3
"""KJV concordance over docs/assets/verse-cache.json.

Authoring a headword safely means seeing every place the Authorized Version
actually uses it -- memory is not reliable below about 20 occurrences, and a
misremembered reference produces a verbatim quote of the WRONG verse, which
bin/verify_kjv_quotes.py cannot catch (see bin/verify_refs.py).

Usage:
  python3 bin/kjv_concordance.py fishers            # first 10 verses
  python3 bin/kjv_concordance.py lieth --n 25       # first 25
  python3 bin/kjv_concordance.py sift --all         # every occurrence
  python3 bin/kjv_concordance.py led lieth seeth    # several words at once

Matching is whole-word and case-insensitive; verses come back in canonical
order with resolver-parseable references (see bin/verify_kjv_quotes.py).
"""
import json, re, sys, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')

# The abbreviations bin/verify_kjv_quotes.py parse_ref() accepts. NOTE 'John',
# not 'Jhn' -- Jhn is not resolvable and makes fill_scriptures.py refuse a file.
BOOKS = ('Gen Exo Lev Num Deu Jos Jdg Rut 1Sa 2Sa 1Ki 2Ki 1Ch 2Ch Ezr Neh Est '
         'Job Psa Pro Ecc Sng Isa Jer Lam Eze Dan Hos Joe Amo Oba Jon Mic Nah '
         'Hab Zep Hag Zec Mal Mat Mar Luk John Act Rom 1Co 2Co Gal Eph Php Col '
         '1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Rev').split()


def clean(s):
    """Strip markup and Strong's numbers the way the generators do."""
    s = html.unescape(s)
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\d+', '', s)
    s = re.sub(r'(?<=[a-zA-Z]) (?=[,.;:])', '', s)   # cache space-before-punct artifact
    return re.sub(r'\s+', ' ', s).strip()


def load_verses():
    cache = json.load(open(CACHE))
    rows = []
    for key, val in cache.items():
        m = re.match(r'(\d+)_(\d+)_(\d+)$', key)
        if not m:
            continue
        text = val.get('KJV') if isinstance(val, dict) else val
        if not text:
            continue
        b, c, v = map(int, m.groups())
        if 1 <= b <= 66:
            rows.append((b, c, v, clean(text)))
    rows.sort()
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show_all = '--all' in sys.argv
    n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 10
    if not args:
        print(__doc__)
        return 1
    rows = load_verses()
    for word in args:
        pat = re.compile(r'\b' + re.escape(word) + r'\b', re.I)
        hits = [r for r in rows if pat.search(r[3])]
        print(f'### {word}: {len(hits)} verses')
        for b, c, v, text in (hits if show_all else hits[:n]):
            print(f'  {BOOKS[b-1]} {c}:{v}  {text}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
