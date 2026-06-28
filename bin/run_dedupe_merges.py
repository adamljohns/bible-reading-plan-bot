#!/usr/bin/env python3
"""Batch-execute the safe dedupe merges from /tmp/merge-groups.json.

Each group is {canonical: <bare slug>, merge: [<base+redundant-suffix slugs>],
title: <identical display title>}. For every group:

  1. CONTENT PROMOTION — if the richest variant is materially larger than the
     bare canonical (the nightly run sometimes wrote a fuller '-doctrine'
     version), promote that variant's body into the canonical file so the clean
     URL keeps the BEST content (Adam: "beef one up with the other"). Because
     the safe groups share an identical title, promotion is just a slug rewrite
     of the canonical/og/self refs.
  2. MERGE — repoint every inbound link to the canonical and replace each
     variant with a no-index redirect stub (one combined pass over the tree),
     then register the redirects.

Run with --apply. Afterwards run rebuild + regen-slugs + manifest + integrity.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs', 'dictionary')
REGISTRY = os.path.join(ROOT, 'data', 'dictionary-redirects.txt')
SCAN = [os.path.join(ROOT, 'docs', d) for d in ('dictionary', 'chapters', 'blog')]
GROUPS = json.load(open('/tmp/merge-groups.json'))

STUB = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- MERGED-REDIRECT canonical={c} -->
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://usmcmin.org/dictionary/{c}.html">
    <meta http-equiv="refresh" content="0; url={c}.html">
    <title>{w} &mdash; merged into {w} | The MOOP Dictionary</title>
    <style>body{{font-family:'Inter',sans-serif;background:#000;color:#FFF;text-align:center;padding:80px 20px;}}a{{color:#D4AF37;}}</style>
</head>
<body><p>This entry was merged into <a href="{c}.html">{w}</a>. Redirecting&hellip;</p>
<script>location.replace("{c}.html");</script></body>
</html>
'''


def size(s):
    p = os.path.join(DICT, s + '.html')
    return os.path.getsize(p) if os.path.exists(p) else 0


def word_of(s):
    m = re.search(r'<div class="word-title">([^<]+)</div>',
                  open(os.path.join(DICT, s + '.html'), encoding='utf-8').read())
    return m.group(1).strip() if m else s


def main():
    apply = '--apply' in sys.argv
    varmap = {}            # variant -> canonical
    promotions = []        # (variant, canonical)
    for g in GROUPS:
        c = g['canonical']
        richest = max(g['merge'], key=size)
        if size(richest) > size(c) * 1.15:
            promotions.append((richest, c))
        for m in g['merge']:
            varmap[m] = c

    print(f'groups: {len(GROUPS)} | variants to merge: {len(varmap)} | '
          f'content promotions (variant richer than bare): {len(promotions)}')
    if not apply:
        print('\nsample promotions:')
        for v, c in promotions[:8]:
            print(f'  promote {v} ({size(v)}b) -> {c} ({size(c)}b)')
        print('\n(dry run — re-run with --apply)')
        return

    # 1) content promotion (rewrite the variant's own slug refs to the canonical)
    for v, c in promotions:
        html = open(os.path.join(DICT, v + '.html'), encoding='utf-8').read()
        html = html.replace(f'/dictionary/{v}.html', f'/dictionary/{c}.html')
        html = html.replace(f'"{v}.html"', f'"{c}.html"')
        open(os.path.join(DICT, c + '.html'), 'w', encoding='utf-8').write(html)
    print(f'promoted {len(promotions)} richer variants into their clean canonical URL')

    # 2) one combined link-repoint pass
    alt = '|'.join(re.escape(v) for v in sorted(varmap, key=len, reverse=True))
    pat = re.compile(r'href="((?:\.\./dictionary/|/dictionary/)?)(' + alt + r')\.html"')
    repl = lambda m: f'href="{m.group(1)}{varmap[m.group(2)]}.html"'
    files = hrefs = 0
    for d in SCAN:
        for fn in os.listdir(d):
            if not fn.endswith('.html') or fn[:-5] in varmap:
                continue
            fp = os.path.join(d, fn)
            t = open(fp, encoding='utf-8').read()
            t2, n = pat.subn(repl, t)
            if n:
                open(fp, 'w', encoding='utf-8').write(t2)
                files += 1; hrefs += n
    print(f'repointed {hrefs} hrefs across {files} files')

    # 3) stubs + registry
    for v, c in varmap.items():
        open(os.path.join(DICT, v + '.html'), 'w', encoding='utf-8').write(
            STUB.format(c=c, w=word_of(c)))
    existing = set()
    if os.path.exists(REGISTRY):
        existing = {l.split('->')[0].strip() for l in open(REGISTRY) if '->' in l}
    with open(REGISTRY, 'a', encoding='utf-8') as f:
        for v, c in varmap.items():
            if v not in existing:
                f.write(f'{v} -> {c}\n')
    print(f'wrote {len(varmap)} redirect stubs + registered them')
    print('\nNow run: rebuild + regen-slugs + manifest + integrity.')


if __name__ == '__main__':
    main()
