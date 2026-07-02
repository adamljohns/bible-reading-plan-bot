#!/usr/bin/env python3
"""Verify a batch JSON's scripture quotes verbatim against docs/assets/verse-cache.json (KJV).

Usage: python3 bin/verify_kjv_quotes.py data/dictionary-batches/batch-NN-*.json [...]

The cache embeds Strong's numbers inline (word<S>1234</S>) and folds psalm
titles into verse 1 (Hebrew numbering), so we strip tags AND digits on both
sides and do a substring match — a quote that is genuine KJV always passes;
a paraphrase or wrong-verse citation fails. Title refs ("Psa 46, title")
are skipped (titles live inside verse 1 here). Exit 1 on any mismatch.
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
    cache = json.load(open(CACHE))
    bad = checked = skipped = 0
    for path in sys.argv[1:]:
        for e in json.load(open(path)):
            for ref, text in e.get('scriptures', []):
                if 'title' in ref:
                    skipped += 1; continue
                m = re.match(r'(\d?[A-Za-z]+)\s+(\d+):(\d+)', ref)
                bn = BOOKNUM.get(m.group(1)) if m else None
                v = cache.get(f'{bn}_{m.group(2)}_{m.group(3)}') if bn else None
                if not v or 'KJV' not in v:
                    skipped += 1; continue
                checked += 1
                if norm(text)[:100] not in norm(v['KJV']):
                    bad += 1
                    print(f'MISMATCH {e["slug"]} {ref}')
                    print(f'  quoted: {norm(text)[:110]}')
                    print(f'  KJV   : {norm(v["KJV"])[:110]}')
    print(f'{checked} verified, {bad} mismatched, {skipped} skipped (titles/uncached)')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
