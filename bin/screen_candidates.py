#!/usr/bin/env python3
"""The one-entity screen: is this candidate word ALREADY in the corpus?

bin/coverage_check.py answers four ways (own slug / redirect / inflection in
either direction / identical display title). Three further ways have each
shipped a real duplicate, and this tool adds them:

  SIBLING  two surface forms sharing one lemma, neither of which is the other's
           inflection -- belonged vs the live belongeth, seemed vs seemeth,
           coupled vs coupling, flying vs flies, manifested vs manifesting.
           This is the class the lemma guards are blind to.
  TOKEN    the word already appears as a hyphen-delimited token of a live slug
           -- cherub in cherubim, oracle in oracle-god, race in race-set-before,
           toil in toil-biblical.
  DERIVED  a chained suffix walk (-ness -ly -ful -ity -ation -ment -ance -ive
           ...) in both directions, so honest reaches honesty and imagine
           reaches imagination.

A word is reported TAKEN if any hard check fires (slug, redirect, inflection,
sibling); TOKEN and DERIVED are advisory and print beside an OPEN verdict,
because a compound or a derivative is often a legitimately distinct entry.

Usage:
  python3 bin/screen_candidates.py led lieth seeth
  python3 bin/screen_candidates.py --file candidates.txt
  python3 bin/screen_candidates.py --file in.txt --open-only > clean.txt
"""
import os, re, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Generated pages that are not dictionary entries (mirrors batch_pipeline.sh
# regen-slugs and the SPECIAL set in bin/dict_integrity_audit.py).
SPECIAL = set('index manifest names doctrinal-anchors biblical-order '
              'expressly-prohibited most-corrupted gen-z-decoded '
              'millennial-decoded gen-x-decoded boomer-decoded '
              'christianese-decoded jesus-generation changelog baby-names '
              'by-topic'.split())

SUFFIXES = ['ness', 'ly', 'ful', 'less', 'ity', 'ation', 'tion', 'sion',
            'ment', 'ance', 'ence', 'er', 'or', 'ous', 'al', 'ive', 'ish',
            'ism', 'ist', 'ship', 'hood', 'dom', 'en', 'y', 'ed', 'ing',
            's', 'es', 'ies', 'eth', 'est']


def load_wordlist():
    spec = importlib.util.spec_from_file_location(
        'kjv_wordlist', os.path.join(ROOT, 'bin/kjv_wordlist.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lemmas(kw, slug):
    out = set(kw.lemma_slugs(slug)) | {slug}
    if slug.endswith('ied'):
        out.add(slug[:-3] + 'y')
    if slug.endswith('ies'):
        out.add(slug[:-3] + 'y')
    return out


def stems(word):
    out = {word}
    for suf in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            st = word[:-len(suf)]
            out |= {st, st + 'e'}
            if st.endswith('i'):
                out.add(st[:-1] + 'y')
            if len(st) > 2 and st[-1] == st[-2]:
                out.add(st[:-1])
    return out


def derived(word):
    out = set()
    for st in stems(word):
        out.add(st)
        for suf in SUFFIXES:
            out.add(st + suf)
            if st.endswith('e'):
                out.add(st[:-1] + suf)
            if st.endswith('y'):
                out.add(st[:-1] + 'i' + suf)
    return out - {word}


def build_index(kw):
    redirects = {}
    path = os.path.join(ROOT, 'data/dictionary-redirects.txt')
    if os.path.exists(path):
        for line in open(path):
            parts = line.split()
            if len(parts) >= 2:
                redirects[parts[0]] = parts[1]
    pages = os.path.join(ROOT, 'docs/dictionary')
    live = {f[:-5] for f in os.listdir(pages) if f.endswith('.html')}
    live -= SPECIAL | set(redirects)
    lemma_of = {}
    tokens = {}
    for slug in live:
        for lem in lemmas(kw, slug):
            lemma_of.setdefault(lem, set()).add(slug)
        for tok in slug.split('-'):
            tokens.setdefault(tok, []).append(slug)
    return live, redirects, lemma_of, tokens


def check(word, kw, index):
    live, redirects, lemma_of, tokens = index
    slug = re.sub(r'[^a-z0-9-]', '', word.lower().strip().replace(' ', '-'))
    notes, hard = [], False
    if slug in live:
        notes.append('SLUG'); hard = True
    if slug in redirects:
        notes.append(f'REDIRECT->{redirects[slug]}'); hard = True
    for lem in lemmas(kw, slug) - {slug}:
        if lem in live:
            notes.append(f'INFL-OF:{lem}'); hard = True
    for other in lemma_of.get(slug, ()):
        if other != slug:
            notes.append(f'INFLECTED-BY:{other}'); hard = True
    siblings = set()
    for lem in lemmas(kw, slug) - {slug}:
        siblings |= lemma_of.get(lem, set())
    siblings -= {slug}
    if siblings:
        notes.append('SIBLING:' + ','.join(sorted(siblings)[:5])); hard = True
    dv = sorted(d for d in derived(slug) if d in live)
    if dv:
        notes.append('DERIVED:' + ','.join(dv[:6]))
    tk = sorted(t for t in tokens.get(slug, []) if t != slug)
    if tk:
        notes.append('TOKEN:' + ','.join(tk[:5]) + ('...' if len(tk) > 5 else ''))
    return slug, hard, notes


def main():
    argv = sys.argv[1:]
    open_only = '--open-only' in argv
    words = []
    if '--file' in argv:
        path = argv[argv.index('--file') + 1]
        words += [l.strip() for l in open(path) if l.strip()]
        argv = [a for a in argv if a != path]
    words += [a for a in argv if not a.startswith('--')]
    if not words:
        print(__doc__)
        return 1
    kw = load_wordlist()
    index = build_index(kw)
    n_open = 0
    for word in words:
        slug, hard, notes = check(word, kw, index)
        if not hard:
            n_open += 1
        if open_only:
            if not hard:
                print(slug)
        else:
            print(f'{slug:22s} {"TAKEN" if hard else "OPEN "} {" | ".join(notes)}')
    if not open_only:
        print(f'\n{n_open} open of {len(words)} checked', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
