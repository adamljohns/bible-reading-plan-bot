#!/usr/bin/env python3
"""Fetch verbatim KJV text for references. Usage: python3 bin/kjv_lookup.py "Php 1:27" "1Ti 6:20" ...
Prints each ref with its exact KJV text (or MISS/UNCACHED). Use these strings verbatim in scriptures[]."""
import json,re,sys,html
CACHE='docs/assets/verse-cache.json'
BOOKNUM={'Gen':1,'Exo':2,'Lev':3,'Num':4,'Deu':5,'Josh':6,'Jos':6,'Jdg':7,'Rut':8,
 '1Sa':9,'2Sa':10,'1Ki':11,'2Ki':12,'1Ch':13,'2Ch':14,'Ezr':15,'Neh':16,'Est':17,
 'Job':18,'Psa':19,'Pro':20,'Ecc':21,'Son':22,'Isa':23,'Jer':24,'Lam':25,'Eze':26,
 'Dan':27,'Hos':28,'Joe':29,'Amo':30,'Oba':31,'Jon':32,'Mic':33,'Nah':34,'Hab':35,
 'Zep':36,'Hag':37,'Zec':38,'Mal':39,'Mat':40,'Mar':41,'Luk':42,'Joh':43,'Act':44,
 'Rom':45,'1Co':46,'2Co':47,'Gal':48,'Eph':49,'Php':50,'Col':51,'1Th':52,'2Th':53,
 '1Ti':54,'2Ti':55,'Tit':56,'Phm':57,'Heb':58,'Jas':59,'1Pe':60,'2Pe':61,'1Jn':62,
 '2Jn':63,'3Jn':64,'Jud':65,'Rev':66}
def clean(s):
    s=html.unescape(s)
    s=re.sub(r'<sup>.*?</sup>','',s,flags=re.S)
    s=re.sub(r'<[^>]+>','',s)
    s=re.sub(r'\d+','',s)  # strip Strong's numbers (verifier is digit-insensitive)
    s=re.sub(r'\s+[A-Za-z][\w-]*:\s+(?:or|Heb|Gr|Gk|Chald|Chal|Called)\b.*$','',s)  # strip trailing KJV margin notes
    s=re.sub(r'(?<=[a-zA-Z]) (?=[,.;:])','',s)  # note space-before-punct artifact
    s=re.sub(r'\s+\d+\s*$','',s)
    return re.sub(r'\s+',' ',s).strip()
cache=json.load(open(CACHE))
for ref in sys.argv[1:]:
    m=re.match(r'(\d?[A-Za-z]+)\s+(\d+):(\d+)',ref)
    if not m: print(f'{ref}\tBADREF'); continue
    bn=BOOKNUM.get(m.group(1))
    if not bn: print(f'{ref}\tBADBOOK (use 3-letter abbr: Php Joe Jud etc.)'); continue
    v=cache.get(f'{bn}_{m.group(2)}_{m.group(3)}')
    if not v or 'KJV' not in v: print(f'{ref}\tUNCACHED'); continue
    raw=v['KJV']
    txt=clean(raw)
    artifact=' ,' in raw or ' .' in raw or bool(re.search(r'[a-z] [,.;:]',raw))
    print(f'{ref}\t{txt}'+('\t[CACHE-ARTIFACT: verify no stray space-before-punct; pick another verse if it will not round-trip]' if artifact else ''))
