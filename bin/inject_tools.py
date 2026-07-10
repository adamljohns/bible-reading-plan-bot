#!/usr/bin/env python3
"""Inject the site-wide interactive toolkit (moop-tools.js) into static pages.

Idempotent: adds ONE <script defer> line before </body> when absent. Skips
redirect stubs (MERGED-REDIRECT). Relative path computed from page depth.

Usage: python3 bin/inject_tools.py docs/dictionary/*.html docs/cross-references.html
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rel_prefix(p):
    rel = os.path.relpath(p, os.path.join(ROOT, 'docs'))
    depth = rel.count(os.sep)
    return '../' * depth

def main():
    changed = skipped = stubs = 0
    for p in sys.argv[1:]:
        t = open(p, encoding='utf-8', errors='ignore').read()
        if 'MERGED-REDIRECT' in t[:600]:
            stubs += 1; continue
        if 'moop-tools.js' in t:
            skipped += 1; continue
        tag = f'    <script defer src="{rel_prefix(p)}assets/js/moop-tools.js"></script>\n</body>'
        if '</body>' not in t:
            skipped += 1; continue
        t = t.replace('</body>', tag, 1)
        open(p, 'w', encoding='utf-8').write(t)
        changed += 1
    print(f'injected: {changed} | already-had/nobody: {skipped} | stubs skipped: {stubs}')

if __name__ == '__main__':
    main()
