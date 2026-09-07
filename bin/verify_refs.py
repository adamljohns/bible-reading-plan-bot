#!/usr/bin/env python3
"""Confirm every cited verse actually CONTAINS the entry's headword.

bin/verify_kjv_quotes.py proves a quote is verbatim. It cannot prove the verse
is the RIGHT verse: a misremembered reference filled by bin/fill_scriptures.py
produces a perfectly verbatim quote of a verse that has nothing to do with the
headword, and every existing gate passes it. This closes that hole.

For each entry, the headword (plus its stems and any words listed in the
optional "refcheck_words" key) is searched for in the KJV text of every
reference in scriptures[]. Only problems are printed.

Usage: python3 bin/verify_refs.py data/dictionary-batches/batch-NNN-*.json [...]

Known benign misses -- check by eye rather than "fixing" the ref:
  * a verse quoted for CONTEXT beside one that does contain the word. This is
    deliberate authoring practice, not an error -- entries routinely pair a
    headword verse with the verse after it (Isa 38:14 + 38:15) and with a
    thematic verse (Mat 6:26 under 'crane'). Expect a dozen such flags per
    batch and read them rather than chasing them.
  * y->i inflections (certify / certified) and prefixed forms
    (especially / specially, incorruptible / uncorruptible)
  * the AV rendering a Hebrew idiom with a different English word
"""
import json, re, sys, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')

BOOKS = ('Gen Exo Lev Num Deu Jos Jdg Rut 1Sa 2Sa 1Ki 2Ki 1Ch 2Ch Ezr Neh Est '
         'Job Psa Pro Ecc Sng Isa Jer Lam Eze Dan Hos Joe Amo Oba Jon Mic Nah '
         'Hab Zep Hag Zec Mal Mat Mar Luk John Act Rom 1Co 2Co Gal Eph Php Col '
         '1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jn 2Jn 3Jn Jud Rev').split()
ALIAS = {'Josh': 'Jos', 'Judg': 'Jdg', 'Ruth': 'Rut', 'Psalm': 'Psa',
         'Prov': 'Pro', 'Song': 'Sng', 'Ezek': 'Eze', 'Joel': 'Joe',
         'Amos': 'Amo', 'Obad': 'Oba', 'Matt': 'Mat', 'Mark': 'Mar',
         'Luke': 'Luk', 'Joh': 'John', 'Acts': 'Act', 'Phil': 'Php',
         'Philem': 'Phm', 'Titus': 'Tit', 'James': 'Jas', 'Jude': 'Jud'}
BOOKNUM = {b: i + 1 for i, b in enumerate(BOOKS)}

SUFFIXES = ('s', 'es', 'ies', 'ed', 'ing', 'eth', 'est', 'ly', 'er', 'ers', 'en', 'th')


def clean(s):
    s = html.unescape(s)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\d+', '', s)


def stems(word):
    w = word.lower()
    out = {w}
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            st = w[:-len(suf)]
            out |= {st, st + 'e', st + 'y'}
            if len(st) > 2 and st[-1] == st[-2]:
                out.add(st[:-1])
    if w.endswith('ied'):
        out.add(w[:-3] + 'y')
    return out


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        return 1
    cache = json.load(open(CACHE))
    issues = 0
    for path in paths:
        for entry in json.load(open(path)):
            slug = entry.get('slug', '?')
            heads = set()
            for h in [slug, entry.get('word', '')] + entry.get('refcheck_words', []):
                heads |= stems(re.split(r'[-\s]', h)[0])
            pats = [re.compile(r'\b' + re.escape(h) + r'\w{0,4}\b', re.I) for h in heads if h]
            # the AV often spells a compound as two words (nighthawk -> 'night hawk',
            # fellowlabourer -> 'fellow labourer'), so allow a split at any point
            base = slug.replace('-', '')
            if len(base) >= 6:
                for i in range(3, len(base) - 2):
                    pats.append(re.compile(r'\b' + re.escape(base[:i]) + r'\s+'
                                           + re.escape(base[i:]) + r'\w{0,3}\b', re.I))
            for pair in entry.get('scriptures', []):
                if not isinstance(pair, list) or not pair:
                    continue
                ref = re.sub(r'\s*\([A-Z]+\)\s*$', '', pair[0])
                m = re.match(r'(\d?\s?[A-Za-z]+)\.?\s+(\d+):(\d+)', ref)
                if not m:
                    print(f'{slug}: UNPARSED REF {ref!r}'); issues += 1; continue
                book = ALIAS.get(m.group(1).replace(' ', ''), m.group(1).replace(' ', ''))
                if book not in BOOKNUM:
                    print(f'{slug}: UNKNOWN BOOK {ref!r}'); issues += 1; continue
                key = f'{BOOKNUM[book]}_{m.group(2)}_{m.group(3)}'
                val = cache.get(key)
                text = val.get('KJV') if isinstance(val, dict) else val
                if not text:
                    print(f'{slug}: UNCACHED {ref}'); issues += 1; continue
                if not any(p.search(clean(text)) for p in pats):
                    print(f'{slug}: headword absent in {ref}: {clean(text)[:90]}')
                    issues += 1
    print(f'verify_refs: {issues} issue(s)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
