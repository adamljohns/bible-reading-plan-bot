#!/usr/bin/env python3
"""Repair dictionary hyperlinks sitewide.

Three classes, all created or surfaced by the 2026-08-06/07 merge work:

1. REDIRECT HOPS — a link points at a slug that is now a merged stub, so the
   reader pays a redirect. The stub must stay (old URLs must not 404), but
   internal links should go straight to the canonical entry.
2. CHAINS — lords-supper-doctrine -> lord-supper -> lords-supper. Resolved
   transitively so no link and no stub points at another stub.
3. BROKEN — a link to a slug that has no page and no redirect entry.

Dry run unless --apply.
"""
import re, sys, glob, os, collections

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

red = {}
for line in open('data/dictionary-redirects.txt'):
    p = re.split(r'\s*->\s*', line.strip())
    if len(p) == 2:
        red[p[0].strip()] = p[1].strip()

def resolve(s, seen=None):
    """Follow the redirect chain to its end, guarding against cycles."""
    seen = seen or set()
    while s in red and s not in seen:
        seen.add(s); s = red[s]
    return s

slugs = {os.path.basename(f)[:-5] for f in glob.glob('docs/dictionary/*.html')}

# Broken links with no redirect entry — hand-mapped to the correct existing entry.
BROKEN = {
    'blood-of-the-new-covenant': 'blood-new-covenant',   # exact title match
    'blood-of-the-lamb':         'lamb-of-god',          # nearest real concept
}
for k, v in BROKEN.items():
    assert v in slugs, f'retarget {v} does not exist'

chains = {s: resolve(s) for s in red if resolve(s) != red[s]}
hop_fixed = broken_fixed = 0
touched = collections.Counter()

for f in glob.glob('docs/**/*.html', recursive=True):
    h = open(f, encoding='utf-8', errors='replace').read()
    orig = h
    def sub(m):
        global hop_fixed, broken_fixed
        pre, s = m.group(1), m.group(2)
        if s in BROKEN:
            broken_fixed += 1; return f'href="{pre}{BROKEN[s]}.html"'
        if s in red:
            # never rewrite a stub's OWN forwarding link
            if os.path.basename(f)[:-5] == s: return m.group(0)
            hop_fixed += 1; return f'href="{pre}{resolve(s)}.html"'
        return m.group(0)
    # Covers relative (../dictionary/x, ./x, x) AND absolute (/dictionary/x).
    # The absolute form was missed on the first pass and accounted for 92
    # surviving hops, 89 of them `communion` in the institutes/lbcf/catechism.
    h = re.sub(r'href="((?:/|(?:\.{1,2}/)*)(?:dictionary/)?)([a-z0-9][a-z0-9-]*)\.html"', sub, h)
    if h != orig:
        touched[f.split('/')[1] if '/' in f else 'root'] += 1
        if APPLY: open(f, 'w', encoding='utf-8').write(h)

print(f'redirect chains collapsed: {len(chains)}  {list(chains.items())[:3]}')
print(f'hop links rewritten : {hop_fixed}')
print(f'broken links fixed  : {broken_fixed}')
print(f'pages touched       : {sum(touched.values())}  by family: {dict(touched.most_common(8))}')
if not APPLY: print('\n--dry-run: nothing written.')
