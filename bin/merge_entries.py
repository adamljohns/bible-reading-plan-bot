#!/usr/bin/env python3
"""Merge duplicate MOOP Dictionary entries into one canonical entry.

The corpus accumulated near-duplicate entries over many batch eras (e.g.
submission / submission-biblical / submission-wife / wifely-submission — four
pages for one idea). This tool consolidates them WITHOUT breaking links or SEO:

  1. Repoints every inbound href from each merged slug to the canonical slug,
     across docs/dictionary, docs/chapters, and docs/blog.
  2. Replaces each merged page with a no-index REDIRECT STUB (meta-refresh +
     <link rel=canonical> to the canonical, plus a visible "merged into" note),
     so old URLs and bookmarks still resolve and SEO consolidates.
  3. Records each merge in data/dictionary-redirects.txt (the registry the
     slug-regen, manifest builder, and integrity audit all honor, so a stub is
     never miscounted as a live entry).

Usage:
  python3 bin/merge_entries.py <canonical> <merge1> [<merge2> ...]          # DRY RUN
  python3 bin/merge_entries.py <canonical> <merge1> [<merge2> ...] --apply  # execute

After --apply, run the rest of the pipeline (rebuild / regen-slugs / manifest /
integrity) to settle counts. NEVER merge a slug into itself; the canonical must
already exist as a real entry page.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs', 'dictionary')
REGISTRY = os.path.join(ROOT, 'data', 'dictionary-redirects.txt')
SCAN_DIRS = [os.path.join(ROOT, 'docs', 'dictionary'),
             os.path.join(ROOT, 'docs', 'chapters'),
             os.path.join(ROOT, 'docs', 'blog')]

STUB = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- MERGED-REDIRECT canonical={canonical} -->
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="https://usmcmin.org/dictionary/{canonical}.html">
    <meta http-equiv="refresh" content="0; url={canonical}.html">
    <title>{word} &mdash; merged into {canon_word} | The MOOP Dictionary</title>
    <style>body{{font-family:'Inter',sans-serif;background:#000;color:#FFF;text-align:center;padding:80px 20px;line-height:1.7;}}a{{color:#D4AF37;}}</style>
</head>
<body>
    <p>This entry has been merged into <a href="{canonical}.html">{canon_word}</a>.</p>
    <p>Redirecting&hellip; if nothing happens, <a href="{canonical}.html">click here</a>.</p>
    <script>location.replace("{canonical}.html");</script>
</body>
</html>
'''


def display_word(slug):
    """Best-effort display title from the entry page, else title-case the slug."""
    p = os.path.join(DICT, slug + '.html')
    if os.path.exists(p):
        t = open(p, encoding='utf-8').read()
        m = re.search(r'<div class="word-title">([^<]+)</div>', t)
        if m:
            return m.group(1).strip()
    return slug.replace('-', ' ').title()


def repoint_links(merge_slugs, canonical):
    """Repoint href="<merge>.html" -> href="<canonical>.html" everywhere. Returns (files, hrefs)."""
    files_changed = 0
    hrefs_changed = 0
    pats = []
    for ms in merge_slugs:
        # relative (within dictionary) and absolute-ish references
        pats.append((re.compile(r'href="' + re.escape(ms) + r'\.html"'),
                     f'href="{canonical}.html"'))
        pats.append((re.compile(r'href="(\.\./dictionary/|/dictionary/)' + re.escape(ms) + r'\.html"'),
                     lambda m: f'href="{m.group(1)}{canonical}.html"'))
    for d in SCAN_DIRS:
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith('.html'):
                continue
            fp = os.path.join(d, fn)
            # never rewrite a stub we are about to (or did) create
            if os.path.splitext(fn)[0] in merge_slugs:
                continue
            t = open(fp, encoding='utf-8').read()
            o = t
            n = 0
            for pat, repl in pats:
                t, k = pat.subn(repl, t)
                n += k
            if t != o:
                open(fp, 'w', encoding='utf-8').write(t)
                files_changed += 1
                hrefs_changed += n
    return files_changed, hrefs_changed


def main():
    args = [a for a in sys.argv[1:] if a != '--apply']
    apply = '--apply' in sys.argv
    if len(args) < 2:
        print('Usage: merge_entries.py <canonical> <merge1> [<merge2> ...] [--apply]', file=sys.stderr)
        sys.exit(2)
    canonical, merges = args[0], args[1:]

    if not os.path.exists(os.path.join(DICT, canonical + '.html')):
        print(f'ERROR: canonical "{canonical}" has no page — refusing.', file=sys.stderr)
        sys.exit(1)
    if canonical in merges:
        print('ERROR: cannot merge a slug into itself.', file=sys.stderr)
        sys.exit(1)
    bad = [m for m in merges if not os.path.exists(os.path.join(DICT, m + '.html'))]
    if bad:
        print(f'ERROR: these merge slugs have no page: {bad}', file=sys.stderr)
        sys.exit(1)

    canon_word = display_word(canonical)
    print(f'{"APPLY" if apply else "DRY RUN"} — merging {merges} -> {canonical} ({canon_word})')
    # count inbound references for the report
    for m in merges:
        cnt = 0
        for d in SCAN_DIRS:
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if fn.endswith('.html') and os.path.splitext(fn)[0] not in merges:
                    if f'{m}.html"' in open(os.path.join(d, fn), encoding='utf-8').read():
                        cnt += 1
        print(f'  {m}: ~{cnt} files link to it')

    if not apply:
        print('\n(dry run — re-run with --apply to repoint links, write stubs, register redirects)')
        return

    files, hrefs = repoint_links(merges, canonical)
    print(f'repointed {hrefs} hrefs across {files} files')

    for m in merges:
        open(os.path.join(DICT, m + '.html'), 'w', encoding='utf-8').write(
            STUB.format(canonical=canonical, word=display_word(m), canon_word=canon_word))
    print(f'wrote {len(merges)} redirect stubs')

    existing = set()
    if os.path.exists(REGISTRY):
        existing = {l.split('->')[0].strip() for l in open(REGISTRY) if '->' in l}
    with open(REGISTRY, 'a', encoding='utf-8') as f:
        for m in merges:
            if m not in existing:
                f.write(f'{m} -> {canonical}\n')
    print(f'registered redirects in {os.path.relpath(REGISTRY, ROOT)}')
    print('\nNow run: rebuild + regen-slugs + manifest + integrity to settle counts.')


if __name__ == '__main__':
    main()
