#!/usr/bin/env python3
"""Verify a batch JSON's scripture quotes verbatim against docs/assets/verse-cache.json (KJV).

Usage: python3 bin/verify_kjv_quotes.py data/dictionary-batches/batch-NN-*.json [...]

The cache embeds Strong's numbers inline (word<S>1234</S>) and folds psalm
titles into verse 1 (Hebrew numbering), so we strip tags AND digits on both
sides and do a substring match — a quote that is genuine KJV always passes;
a paraphrase or wrong-verse citation fails. Title refs ("Psa 46, title")
are skipped (titles live inside verse 1 here).

AN UNRESOLVABLE REFERENCE IS A FAILURE, NOT A SKIP (fixed 2026-08-05).
Until now a ref this script could not parse — `Psalm 22:1`, `John 1:14`,
`2 Tim. 3:16`, anything outside the 3-letter BOOKNUM table — fell into the
same `skipped` bucket as a genuine cache miss. A batch written entirely in
that style therefore reported "0 verified, 0 mismatched" and exited 0: a
PASS meaning *nothing was examined*. That is how batches 417, 423-426 and
430-436 cleared the pipeline carrying NASB/LSB/ESV text, and how 10,973 of
20,780 scripture slots (52.8%) came to be silently unchecked corpus-wide.

Exit 1 on: any mismatch, any unresolvable reference, any uncached verse, or
a run that verified nothing at all. Pass --allow-uncached to downgrade only
the cache-miss class to a warning (the cache holds 30,706 of 31,102 KJV
verses, so a legitimate hole is possible and is not the author's fault).

Usage: python3 bin/verify_kjv_quotes.py data/dictionary-batches/batch-NN-*.json [...]
       python3 bin/verify_kjv_quotes.py --allow-uncached data/.../batch-NN-*.json
"""
import json, re, sys, html

CACHE = 'docs/assets/verse-cache.json'
BOOKNUM = {'Gen':1,'Exo':2,'Lev':3,'Num':4,'Deu':5,'Josh':6,'Jos':6,'Jdg':7,'Rut':8,
           '1Sa':9,'2Sa':10,'1Ki':11,'2Ki':12,'1Ch':13,'2Ch':14,'Ezr':15,'Neh':16,
           'Est':17,'Job':18,'Psa':19,'Pro':20,'Ecc':21,'Son':22,'Isa':23,'Jer':24,
           'Lam':25,'Eze':26,'Dan':27,'Hos':28,'Joe':29,'Amo':30,'Oba':31,'Jon':32,
           'Mic':33,'Nah':34,'Hab':35,'Zep':36,'Hag':37,'Zec':38,'Mal':39,'Mat':40,
           'Mar':41,'Luk':42,'Joh':43,'Act':44,'Rom':45,'1Co':46,'2Co':47,'Gal':48,
           'Eph':49,'Php':50,'Col':51,'1Th':52,'2Th':53,'1Ti':54,'2Ti':55,'Tit':56,
           'Phm':57,'Heb':58,'Jas':59,'1Pe':60,'2Pe':61,'1Jn':62,'2Jn':63,'3Jn':64,
           'Jud':65,'Rev':66}

def norm(s):
    s = html.unescape(s).lower()
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)   # translator margin notes
    s = re.sub(r'<[^>]+>', '', s)                       # tag markup
    s = re.sub(r'\d+', '', s)                           # inline Strong's numbers
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r'[“”]', '"', s)
    return re.sub(r'\s+', ' ', s).strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    allow_uncached = '--allow-uncached' in sys.argv[1:]

    cache = json.load(open(CACHE))
    bad = checked = titles = 0
    unresolvable, uncached = [], []

    for path in args:
        for e in json.load(open(path)):
            for ref, text in e.get('scriptures', []):
                if 'title' in ref:
                    titles += 1; continue
                m = re.match(r'(\d?[A-Za-z]+)\s+(\d+):(\d+)', ref)
                bn = BOOKNUM.get(m.group(1)) if m else None
                if not bn:
                    # The author wrote a ref this verifier cannot resolve. That
                    # is an authoring defect, not a cache gap — it must fail.
                    unresolvable.append((e.get('slug', '?'), ref))
                    continue
                v = cache.get(f'{bn}_{m.group(2)}_{m.group(3)}')
                if not v or 'KJV' not in v:
                    uncached.append((e.get('slug', '?'), ref))
                    continue
                checked += 1
                if norm(text)[:100] not in norm(v['KJV']):
                    bad += 1
                    print(f'MISMATCH {e["slug"]} {ref}')
                    print(f'  quoted: {norm(text)[:110]}')
                    print(f'  KJV   : {norm(v["KJV"])[:110]}')

    if unresolvable:
        print(f'\nUNRESOLVABLE REFERENCES ({len(unresolvable)}) — these were never checked.')
        print('Rewrite each in the 3-letter form this verifier reads (Psa 22:1, Joh 1:14, Php 2:6):')
        for slug, ref in unresolvable[:40]:
            print(f'  {slug:32} {ref}')
        if len(unresolvable) > 40:
            print(f'  ... and {len(unresolvable) - 40} more')

    if uncached:
        label = 'WARNING' if allow_uncached else 'UNCACHED — NOT VERIFIED'
        print(f'\n{label} ({len(uncached)}): verse absent from the cache, quote unchecked.')
        for slug, ref in uncached[:20]:
            print(f'  {slug:32} {ref}')
        if len(uncached) > 20:
            print(f'  ... and {len(uncached) - 20} more')

    print(f'\n{checked} verified, {bad} mismatched, '
          f'{len(unresolvable)} unresolvable, {len(uncached)} uncached, {titles} titles')

    fail = bool(bad or unresolvable or (uncached and not allow_uncached))
    # "Nothing was examined" is the failure mode this guard exists to catch:
    # it is what a wholly wrong-ref-style batch used to report as success.
    if not checked and (titles or unresolvable or uncached):
        print('FAIL: nothing was verified — this is not a pass.')
        fail = True
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
