#!/usr/bin/env python3
"""Repoint every link to a redirected dictionary slug onto its canonical, site-wide.

merge_entries.py / run_dedupe_merges.py repoint docs/{dictionary,chapters,blog}
for speed, but other surfaces (the 7.8k lexicon pages' Strong's links, top-level
pages, LBCF, institutes, worship) and the generator card-lists in
rebuild-dictionary.py can still point at a merged slug — those links work (the
stub redirects) but cost an extra hop. This sweeps them all from
data/dictionary-redirects.txt so links land on the canonical directly.

Run after any merge: python3 bin/repoint_redirects.py [--apply]
Then rebuild + integrity.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
REG = os.path.join(ROOT, 'data', 'dictionary-redirects.txt')
# generator sources whose hard-coded card lists may name a merged slug
TEMPLATES = ['rebuild-dictionary.py', 'bin/build_by_topic.py', 'bin/build_jesus_generation.py']

varmap = {}
for l in open(REG):
    if '->' in l:
        a, b = l.split('->'); varmap[a.strip()] = b.strip()


def repoint_html(apply):
    alt = '|'.join(re.escape(v) for v in sorted(varmap, key=len, reverse=True))
    # absolute / relative dictionary hrefs
    pat = re.compile(r'href="((?:\.\./)?dictionary/|/dictionary/)(' + alt + r')\.html"')
    pat_bare = re.compile(r'href="(' + alt + r')\.html"')   # only applied inside docs/dictionary
    files = hrefs = 0
    for root, dirs, fns in os.walk(DOCS):
        if '_archive' in root:
            continue
        indict = root.replace('\\', '/').endswith('docs/dictionary')
        for fn in fns:
            if not fn.endswith('.html'):
                continue
            if indict and fn[:-5] in varmap:      # don't touch the stubs themselves
                continue
            fp = os.path.join(root, fn)
            t = open(fp, encoding='utf-8', errors='replace').read()
            n = 0
            t, k = pat.subn(lambda m: f'href="{m.group(1)}{varmap[m.group(2)]}.html"', t); n += k
            if indict:
                t, k = pat_bare.subn(lambda m: f'href="{varmap[m.group(1)]}.html"', t); n += k
            if n and apply:
                open(fp, 'w', encoding='utf-8').write(t)
            if n:
                files += 1; hrefs += n
    return files, hrefs


def repoint_templates(apply):
    fixed = 0
    for rel in TEMPLATES:
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp):
            continue
        t = open(fp, encoding='utf-8').read()
        o = t
        for v, c in varmap.items():
            t = t.replace(f'"{v}.html"', f'"{c}.html"').replace(f'"{v}"', f'"{c}"')
        if t != o:
            if apply:
                open(fp, 'w', encoding='utf-8').write(t)
            fixed += 1
    return fixed


def main():
    apply = '--apply' in sys.argv
    files, hrefs = repoint_html(apply)
    tpl = repoint_templates(apply)
    verb = 'repointed' if apply else 'would repoint'
    print(f'{verb} {hrefs} hrefs across {files} files + {tpl} generator templates '
          f'({len(varmap)} redirected slugs)')
    if not apply:
        print('(dry run — re-run with --apply, then rebuild + integrity)')


if __name__ == '__main__':
    main()
