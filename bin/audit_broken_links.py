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
import argparse
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

# Skip these paths entirely (output noise, very long)
SKIP_DIRS = {'_archive', '_backup', '_wip', '_drafts', 'churches', 'lexicon', 'chapters', 'verse'}
# Template/scaffold HTML files that aren't real served pages — they hold placeholder hrefs
SKIP_FILES = {'docs/assets/lexicon-template.html', 'docs/assets/blog-template.html'}

# Match the opening quote and require the SAME quote to close. The previous
# pattern excluded both quote characters from the body, so a double-quoted href
# containing an apostrophe -- worship/slides/Jesus, Lover of My Soul (It's all
# about You).pdf -- was truncated at "It" and reported broken forever.
HREF_RE = re.compile(r'href=(["\'])([^#]*?)\1', re.IGNORECASE)
EXTERNAL_RE = re.compile(r'^(https?:|mailto:|tel:|javascript:|data:|//)', re.IGNORECASE)
# Any other custom URI scheme (lmstudio://, obsidian://, zoommtg://). These are
# app handlers, not site paths; without this the auditor resolved "lmstudio://"
# to the nonsense path "lmstudio:/index.html" and reported it broken forever.
CUSTOM_SCHEME_RE = re.compile(r'^[a-z][a-z0-9+.-]*://', re.IGNORECASE)
# Large media is uploaded to R2 out of band (rclone copy) and is deliberately
# absent from the git checkout -- deploy-r2.yml excludes these same patterns
# from the sync so a grind deploy cannot delete them. On a developer machine
# they happen to exist locally, in CI they never do, so counting them made the
# broken-link total differ between local and CI. They are live on R2; they are
# not broken links.
OUT_OF_BAND_RE = re.compile(r'^/?assets/(media|video)/.*\.(mp4|m4a)$', re.IGNORECASE)
# JS template / placeholder patterns — these are runtime-rendered, not real hrefs
TEMPLATE_RE = re.compile(r'\$\{|\{\{|<%|\[[A-Z_]+\]')
# Bare bible.us / bible.com etc. without protocol — older posts use this form,
# browser auto-prefixes the current site's scheme, so they hit a 404 on this site.
# We treat them as external URLs needing protocol-fix elsewhere; skip in audit
# to keep this script focused on internal-site link health.
PROTOCOL_LESS_BIBLE = re.compile(r'^bible\.(us|com|cc|gateway\.com)/', re.IGNORECASE)


def resolve_link(source_file, href):
    """Given a source HTML file and an href, return the resolved absolute path
    on disk that the link points to. None if not a file-resolvable link."""
    if not href or EXTERNAL_RE.match(href) or CUSTOM_SCHEME_RE.match(href):
        return None
    if OUT_OF_BAND_RE.match(href.split('?')[0]):
        return None
    # Skip JS template literals / placeholder patterns — these are runtime hrefs
    if TEMPLATE_RE.search(href):
        return None
    # Skip protocol-less Bible-app URLs (older posts had bare bible.us/X form)
    if PROTOCOL_LESS_BIBLE.match(href):
        return None
    # Strip query string for the path lookup
    path_part = href.split('?')[0].split('#')[0]
    if not path_part:
        return None
    # URL-decode
    path_part = unquote(path_part)
    # Site-root-relative if leading slash
    if path_part.startswith('/'):
        # Bare "/" => root index
        if path_part == '/':
            return os.path.join(DOCS, 'index.html')
        abs_path = os.path.normpath(os.path.join(DOCS, path_part.lstrip('/')))
    else:
        # Otherwise resolve relative to source file's dir
        source_dir = os.path.dirname(source_file)
        abs_path = os.path.normpath(os.path.join(source_dir, path_part))
    # If the path ends with / OR resolves to a directory, treat as directory's index.html
    if path_part.endswith('/') or os.path.isdir(abs_path):
        abs_path = os.path.join(abs_path, 'index.html')
    return abs_path


def main(max_broken=None):
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
            rel_src = os.path.relpath(src, os.path.dirname(DOCS))
            if rel_src in SKIP_FILES:
                continue
            sources_scanned += 1
            try:
                with open(src, 'r', encoding='utf-8') as f:
                    html = f.read()
            except Exception:
                continue
            # Strip <pre>...</pre>, <code>...</code>, and <script>...</script> so href patterns
            # shown as code examples or inside JS strings don't get flagged.
            html_scan = re.sub(r'<(pre|code|script|textarea)\b[^>]*>.*?</\1>', '', html,
                               flags=re.IGNORECASE | re.DOTALL)
            for m in HREF_RE.finditer(html_scan):
                href = m.group(2).strip()
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

    total_broken = sum(broken_per_dir.values())
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

    # Governance rule 6: a gate that examines nothing has not passed. Until
    # 2026-09-03 this script always exited 0, so it could report broken links
    # forever without anything noticing -- which is what it did.
    if checked == 0:
        print('\nFAIL: 0 internal links checked. A gate that examines nothing has not passed.')
        return 2
    print(f'\nTotal broken internal links: {total_broken}')
    if max_broken is not None and total_broken > max_broken:
        print(f'FAIL: {total_broken} broken links exceeds the ceiling of {max_broken}.')
        print('Fix the link, or raise the ceiling deliberately in the deploy workflow.')
        return 1
    if max_broken is not None:
        print(f'PASS: at or below the ceiling of {max_broken}.')
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-broken', type=int, default=None,
                    help='exit non-zero if more than N broken internal links are found')
    _args = ap.parse_args()
    sys.exit(main(max_broken=_args.max_broken))
