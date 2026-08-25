#!/usr/bin/env python3
"""validate_batches.py — run the batch_pipeline pre-flight checks over MANY
batch files at once, treating them as one authoring set.

The pipeline's inline pre-flight validates a single batch against slugs.txt.
When a session authors dozens of batches before settling the corpus, slugs.txt
is stale for every batch after the first, so cross-batch collisions go unseen.
This validates the whole set together: schema, entities, slug collisions
(against live slugs, redirects, AND the other batches in the set), related
targets, roots_lines typing, and the inflection guard.

Usage: python3 bin/validate_batches.py data/dictionary-batches/batch-6*.json
"""
import json, re, sys, os, html.entities, importlib.util, collections

REQ = ['slug','word','pronunciation','pos','etymology','biblical_def',
       'webster_summary','webster_full','scriptures','corruption_summary',
       'corruption_paragraphs','roots_summary','roots_lines','usage','related']
VALID_ENT = set(html.entities.name2codepoint) | {'amacr','emacr','imacr','omacr',
                                                 'umacr','aelig','thorn'}
RESERVED = {'sevenfold'}

_sp = importlib.util.spec_from_file_location('kw', 'bin/kjv_wordlist.py')
KW = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(KW)

def main():
    paths = sys.argv[1:]
    live = {l.strip() for l in open('data/dictionary-slugs.txt') if l.strip()}
    try:
        live |= {l.split('->')[0].strip() for l in open('data/dictionary-redirects.txt') if '->' in l}
    except FileNotFoundError:
        pass
    pages = {f[:-5] for f in os.listdir('docs/dictionary') if f.endswith('.html')}
    lemma_of_live = {}
    for s in live:
        for lem in KW.lemma_slugs(s):
            lemma_of_live.setdefault(lem, []).append(s)

    errs = []
    seen = {}                      # slug -> batch that first claimed it
    allnew = set()
    for p in paths:
        for e in json.load(open(p)):
            allnew.add(e.get('slug'))

    for p in paths:
        raw = open(p, encoding='utf-8').read()
        try:
            data = json.loads(raw)
        except Exception as ex:
            errs.append(f'{p}: BAD JSON {ex}'); continue
        bad = sorted(set(re.findall(r'&([a-zA-Z][a-zA-Z0-9]*);', raw)) - VALID_ENT)
        if bad:
            errs.append(f'{p}: invalid HTML entities {bad}')
        # Foreign-script guard: pronunciation keys legitimately use Latin
        # diacritics, but Cyrillic/Greek/CJK characters in the prose mean a
        # word from another language slipped in mid-sentence. One did on
        # 2026-08-17 ('военная' for 'military'), and read perfectly fluently
        # in every other respect, so only a codepoint check catches it.
        stray = sorted(set(re.findall(r'[\u0400-\u04FF\u0370-\u03FF\u4E00-\u9FFF\u0600-\u06FF]', raw)))
        if stray:
            errs.append(f'{p}: non-Latin characters in text: {"".join(stray)[:40]}')
        b = os.path.basename(p)
        for e in data:
            s = e.get('slug', '(missing)')
            miss = [k for k in REQ if k not in e]
            if miss:
                errs.append(f'{b}/{s}: missing fields {miss}')
            if s in RESERVED:
                errs.append(f'{b}/{s}: RESERVED slug — must not be authored')
            if s in live:
                errs.append(f'{b}/{s}: SLUG COLLISION with live corpus/redirects')
            if s in seen:
                errs.append(f'{b}/{s}: DUPLICATE of {seen[s]} in this same set')
            else:
                seen[s] = b
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', s or ''):
                errs.append(f'{b}/{s}: malformed slug')
            for k in ('webster_full','roots_lines','usage','corruption_paragraphs'):
                v = e.get(k)
                if not isinstance(v, list) or any(not isinstance(x, str) for x in v):
                    errs.append(f'{b}/{s}: {k} must be a list of STRINGS')
            sc = e.get('scriptures')
            if not isinstance(sc, list) or not sc:
                errs.append(f'{b}/{s}: scriptures must be a non-empty list')
            else:
                for pair in sc:
                    if not (isinstance(pair, list) and len(pair) == 2):
                        errs.append(f'{b}/{s}: malformed scripture pair {pair}')
            rels = []
            for pair in e.get('related', []):
                if not (isinstance(pair, list) and len(pair) == 2):
                    errs.append(f'{b}/{s}: malformed related pair {pair}'); continue
                rels.append(pair[0])
                if pair[0] not in pages and pair[0] not in allnew:
                    errs.append(f'{b}/{s}: related target "{pair[0]}" does not exist')
            if len(rels) != len(set(rels)):
                errs.append(f'{b}/{s}: duplicate related targets')
            ack = set(e.get('distinct_from', []))
            hits = {c for c in KW.lemma_slugs(s) if c in live}
            hits |= set(lemma_of_live.get(s, []))
            hits = sorted(h for h in hits if h != s and h not in ack and h not in allnew)
            if hits:
                errs.append(f'{b}/{s}: INFLECTION clash with {hits} — skip, or '
                            f'add "distinct_from": {hits}')
    if errs:
        print(f'VALIDATE FAIL: {len(errs)} problem(s)')
        for x in errs[:60]:
            print('  -', x)
        sys.exit(1)
    print(f'validate OK: {len(paths)} batches, {len(seen)} entries, all clean')

if __name__ == '__main__':
    main()
