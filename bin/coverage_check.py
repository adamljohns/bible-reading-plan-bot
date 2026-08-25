#!/usr/bin/env python3
"""coverage_check.py — is this word ALREADY in the MOOP Dictionary?

An exact slug match is not enough. The 2026-08-16 run shipped `tache` beside
`taches` and `wimple` beside `wimples` because it only checked slugs.txt for
the literal string. A word can already be present in four distinct ways:

  1. as its own slug                      (`grace`)
  2. as a redirect, either side           (`tache -> taches`)
  3. as an inflection of a live entry,
     or with a live entry that is an
     inflection of IT                     (`come` vs live `cometh`)
  4. under a different slug but the same
     DISPLAY TITLE                        (`Alpha and Omega` twice)

Usage:
  python3 bin/coverage_check.py word [word ...]      # report per word
  python3 bin/coverage_check.py --file candidates.txt
  python3 bin/coverage_check.py --file in.txt --open-only > clean.txt
"""
import json, os, re, sys, importlib.util, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, f'bin/{name}.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

KW = _load('kjv_wordlist')

def slugify(w):
    return re.sub(r'[^a-z0-9]+', '-', w.lower()).strip('-')

def build_index():
    slugs = {l.strip() for l in open(os.path.join(ROOT, 'data/dictionary-slugs.txt')) if l.strip()}
    redir_from, redir_to = set(), {}
    rp = os.path.join(ROOT, 'data/dictionary-redirects.txt')
    if os.path.exists(rp):
        for l in open(rp):
            if '->' in l:
                a, b = [x.strip() for x in l.split('->', 1)]
                redir_from.add(a); redir_to[a] = b
    # live entry -> its lemma forms, so we can catch BOTH directions
    lemma_of_live = {}
    for s in slugs:
        for lem in KW.lemma_slugs(s):
            lemma_of_live.setdefault(lem, []).append(s)
    # display titles, from the generated pages
    titles = {}
    dd = os.path.join(ROOT, 'docs/dictionary')
    for fn in os.listdir(dd):
        if not fn.endswith('.html'):
            continue
        slug = fn[:-5]
        if slug not in slugs:
            continue
        try:
            head = open(os.path.join(dd, fn), encoding='utf-8').read(4000)
        except Exception:
            continue
        m = re.search(r'<title>(.*?)(?:\s*&mdash;|\s*—|</title>)', head, re.S)
        if m:
            t = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip().lower()
            titles.setdefault(t, []).append(slug)
    return slugs, redir_from, redir_to, lemma_of_live, titles

def check(word, idx):
    slugs, redir_from, redir_to, lemma_of_live, titles = idx
    s = slugify(word)
    hits = []
    if s in slugs:
        hits.append(('SLUG', s))
    if s in redir_from:
        hits.append(('REDIRECT', f'{s} -> {redir_to[s]}'))
    for lem in KW.lemma_slugs(s):
        if lem in slugs:
            hits.append(('INFLECTION-OF', lem))
    for live in lemma_of_live.get(s, []):
        if live != s:
            hits.append(('INFLECTED-BY', live))
    t = word.strip().lower()
    for owner in titles.get(t, []):
        if owner != s:
            hits.append(('SAME-TITLE', owner))
    return hits

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    open_only = '--open-only' in sys.argv
    if '--file' in sys.argv:
        path = sys.argv[sys.argv.index('--file') + 1]
        args = [l.strip() for l in open(path) if l.strip() and not l.startswith('#')]
    idx = build_index()
    n_open = 0
    for w in args:
        hits = check(w, idx)
        if not hits:
            n_open += 1
            print(w if open_only else f'OPEN   {w}')
        elif not open_only:
            desc = '; '.join(f'{k}:{v}' for k, v in dict.fromkeys(hits))
            print(f'TAKEN  {w:24} {desc}')
    if not open_only:
        print(f'\n{n_open} open of {len(args)} checked', file=sys.stderr)

if __name__ == '__main__':
    main()
