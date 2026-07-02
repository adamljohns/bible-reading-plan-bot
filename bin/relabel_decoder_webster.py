#!/usr/bin/env python3
"""Retire the fabricated 'Webster 1828 Definition' section on generational-decoder
(slang) entries. Noah Webster (d. 1843) never defined 'rizz' or 'skibidi'; these
blocks actually hold slang etymology + era + a biblical application — real value
mis-filed under a false heading. So we RE-LABEL (keep the content, honest title)
rather than delete. Operates only on the slug list passed on argv (the entries
carded in the four generational -decoded sections).

Usage: python3 bin/relabel_decoder_webster.py <slugs-file>
"""
import os, sys, re

DICT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    'docs', 'dictionary')

SUBS = [
    # visible section heading: the false Webster reference -> honest heading
    ('<h3>&#128220; Webster 1828 Definition</h3>',
     '<h3>&#128220; Origin &amp; Era</h3>'),
    # section id (no anchors reference #webster; verified) -> honest id
    ('<div class="section" id="webster">',
     '<div class="section" id="origin">'),
    # SEO / share meta: drop the false 'Webster 1828,' claim (appears 2x: name + og)
    ('biblical definition, Webster 1828, Greek/Hebrew roots',
     'biblical definition, Greek/Hebrew roots'),
]

def main():
    slugs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    changed = skipped = 0
    still_ref = []
    for s in slugs:
        p = os.path.join(DICT, s + '.html')
        if not os.path.exists(p):
            skipped += 1; continue
        t = open(p, encoding='utf-8').read()
        orig = t
        for old, new in SUBS:
            t = t.replace(old, new)
        if t != orig:
            open(p, 'w', encoding='utf-8').write(t)
            changed += 1
        # audit: any visible 'Webster 1828' left (heading/summary/body, not css/id)?
        if re.search(r'Webster 1828', t):
            still_ref.append(s)
    print(f'relabeled: {changed} | skipped(missing): {skipped}')
    if still_ref:
        print(f'STILL reference "Webster 1828" ({len(still_ref)}): {", ".join(still_ref[:15])}')
    else:
        print('clean: no entry still shows "Webster 1828"')

if __name__ == '__main__':
    main()
