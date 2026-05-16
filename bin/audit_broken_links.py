#!/usr/bin/env python3
"""Audit internal links across docs/.

Scans every .html for href="..." values that look like relative internal
links and reports any that don't resolve to an actual file. Excludes:
  - Anchor-only links (#section)
  - mailto:, tel:, javascript:
  - Absolute http(s):// links (external)
  - Build/data files (.json, .xml, .pdf, etc.)
  - bible.html?ref=... (query-only links to a real page)

Outputs:
  - Summary count per source-page directory
  - First 30 specific broken-link examples
"""
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

# Skip these paths entirely (output noise, very long)
SKIP_DIRS = {'_archive', '_backup', '_wip', '_drafts', 'churches', 'lexicon', 'chapters', 'verse'}

HREF_RE = re.compile(r'href=["\']([^"\'#]+?)["\']', re.IGNORECASE)
EXTERNAL_RE = re.compile(r'^(https?:|mailto:|tel:|javascript:|data:|//)', re.IGNORECASE)


def resolve_link(source_file, href):
    """Given a source HTML file and an href, return the resolved absolute path
    on disk that the link points to. None if not a file-resolvable link."""
    if not href or EXTERNAL_RE.match(href):
        return None
    # Strip query string for the path lookup
    path_part = href.split('?')[0].split('#')[0]
    if not path_part:
        return None
    # URL-decode
    path_part = unquote(path_part)
    # Site-root-relative if leading slash
    if path_part.startswith('/'):
        abs_path = os.path.normpath(os.path.join(DOCS, path_part.lstrip('/')))
    else:
        # Otherwise resolve relative to source file's dir
        source_dir = os.path.dirname(source_file)
        abs_path = os.path.normpath(os.path.join(source_dir, path_part))
    # If the path ends with /, treat as directory's index.html
    if abs_path.endswith(os.sep) or os.path.isdir(abs_path):
        abs_path = os.path.join(abs_path, 'index.html')
    return abs_path


def main():
    broken_per_dir = defaultdict(int)
    broken_examples = []
    checked = 0
    sources_scanned = 0

    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.html'):
                continue
            src = os.path.join(root, fn)
            sources_scanned += 1
            try:
                with open(src, 'r', encoding='utf-8') as f:
                    html = f.read()
            except Exception:
                continue
            for m in HREF_RE.finditer(html):
                href = m.group(1).strip()
                target = resolve_link(src, href)
                if target is None:
                    continue
                checked += 1
                if not os.path.exists(target):
                    rel_src = os.path.relpath(src, DOCS)
                    rel_dir = os.path.dirname(rel_src) or '(root)'
                    broken_per_dir[rel_dir] += 1
                    if len(broken_examples) < 30:
                        broken_examples.append((rel_src, href, target))

    print(f'Scanned {sources_scanned} HTML files, checked {checked} internal links')
    print()
    print('=== Broken links per source directory ===')
    for d, n in sorted(broken_per_dir.items(), key=lambda x: -x[1])[:30]:
        print(f'  {d:<40} {n}')
    print()
    print('=== First 30 broken links (source -> target href -> resolved-path) ===')
    for src, href, target in broken_examples:
        rel_target = os.path.relpath(target, DOCS) if target.startswith(DOCS) else target
        print(f'  {src}')
        print(f'    -> href="{href}"')
        print(f'    -> would resolve to: {rel_target}')


if __name__ == '__main__':
    main()
