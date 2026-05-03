#!/usr/bin/env python3
"""Audit dangling related-chip links across all dictionary entries.

Each entry's footer has chips like <a href="some-slug.html">Label</a>.
This script scans all entries, gathers every chip-target slug, and reports
which slugs are referenced but have no corresponding HTML file.
"""
import os, re, sys
from collections import Counter

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'docs', 'dictionary')

# Find all .html files (the slug set that exists).
existing_slugs = set()
for fn in os.listdir(DICT_DIR):
    if fn.endswith('.html') and fn not in ('index.html', 'template.html'):
        existing_slugs.add(fn[:-5])

# Scan related-chip links across all entry files.
chip_pat = re.compile(r'<div class="related">(.*?)</div>', re.DOTALL)
href_pat = re.compile(r'<a href="([^"]+)\.html">([^<]+)</a>')

dangling = Counter()
for fn in os.listdir(DICT_DIR):
    if not fn.endswith('.html') or fn in ('index.html', 'template.html'):
        continue
    with open(os.path.join(DICT_DIR, fn), 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    m = chip_pat.search(content)
    if not m:
        continue
    block = m.group(1)
    for href_match in href_pat.finditer(block):
        slug = href_match.group(1)
        # Skip cross-section relative paths (e.g., ../bible.html)
        if '/' in slug or slug.startswith('http'):
            continue
        if slug not in existing_slugs:
            dangling[slug] += 1

# Print summary.
print(f"Dictionary entries scanned: {sum(1 for fn in os.listdir(DICT_DIR) if fn.endswith('.html') and fn not in ('index.html','template.html'))}")
print(f"Existing slugs: {len(existing_slugs)}")
print(f"Distinct dangling chip-targets: {len(dangling)}")
print(f"Total dangling chip-references: {sum(dangling.values())}")
print()
print("Top 30 most-referenced dangling slugs:")
for slug, count in dangling.most_common(30):
    print(f"  {count:4d}  {slug}")

if len(sys.argv) > 1 and sys.argv[1] == '--list-all':
    print()
    print("All dangling slugs (sorted by count):")
    for slug, count in dangling.most_common():
        print(f"  {count:4d}  {slug}")
