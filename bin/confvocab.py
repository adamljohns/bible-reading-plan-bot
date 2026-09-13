#!/usr/bin/env python3
"""Extract theological vocabulary from the repo's confessional library."""
import re, glob, html, collections, sys, os

FILES = (glob.glob('docs/lbcf/*.html') + glob.glob('docs/institutes/*.html')
         + ['docs/catechism.html', 'docs/lbcf-full.html'])

CHROME = set('''html head body div span class href src nav footer header main section
article aside script style link meta title button input form label select option
usmc ministries usmcmin org com www http https jsx css js png jpg svg font awesome
copyright rights reserved menu toggle search home about contact donate subscribe
browser audio download blog lexicon dictionary chapter chapters verse verses
previous next index page pages print share email facebook twitter youtube
les des une qui que pas nous vous ils elles pour dans avec sur est sont etre avoir
comme mais plus tout tous cette ces son ses leur leurs par aux sans sous
rom cor gal eph phil col thess tim tit heb pet jas jude rev matt mark luke john acts
gen exod lev num deut josh judg ruth sam kings chron ezra neh esth job psa prov eccl
song isa jer lam ezek dan hos joel amos obad jonah mic nah hab zeph hag zech mal
viz sec lib cap chap ibid loc cit
pemberton beveridge modernized linked generated
'''.split())

STOP = set('''the and that not they which this are but from with all their our was have
them who when him what were has those there more any than own been these same how
for was his her she was you your yours had him its it is be to of in on at by as an
or if so no nor yet do does did done will would shall should can could may might must
must been being am are was were we us he i a we one two three first second third
also such other some then here now thus therefore however unless because since while
whom whose where why though although upon into unto without within against between
among about above below after before under over again further once each every either
neither both few many most other own such only very same too just even still
say says said see seen let make made take taken give given come came go went know
known think thought thing things man men word words way ways part parts case cases
time times day days year years place places name names life live lives long great
good better best true truth false new old own great little large small whole
sense meaning example instance manner order kind sort form point view respect regard
himself herself itself themselves myself ourselves yourselves
'''.split())

def words_of(path):
    try:
        s = open(path, encoding='utf-8').read()
    except Exception:
        return []
    s = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.findall(r"[A-Za-z][a-z]{3,}", s)

def main():
    minfreq = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    counts = collections.Counter(); docs = collections.Counter()
    for f in FILES:
        seen = set()
        for w in words_of(f):
            lw = w.lower()
            if lw in STOP or lw in CHROME: continue
            counts[lw] += 1; seen.add(lw)
        for w in seen: docs[w] += 1
    out = [(w, c, docs[w]) for w, c in counts.items() if c >= minfreq and docs[w] >= 2]
    out.sort(key=lambda t: -t[1])
    for w, c, d in out: print(w)
    print(f'{len(out)} terms (freq>={minfreq}, in >=2 docs) from {len(FILES)} files', file=sys.stderr)

if __name__ == '__main__':
    main()
