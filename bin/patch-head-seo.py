#!/usr/bin/env python3
"""Inject head-only SEO JSON-LD into existing .org pages (no body/display changes).

Targets:
  - docs/dictionary/*.html  → DefinedTerm (skip if already present)
  - docs/blog/*.html        → BlogPosting (skip if already present)

Usage:
  python3 bin/patch-head-seo.py [--dry-run] [--limit N]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
BASE = 'https://usmcmin.org'


def _meta(content: str, name: str, attr: str = 'name') -> str | None:
    m = re.search(
        rf'<meta\s+{attr}="{re.escape(name)}"\s+content="([^"]*)"',
        content,
        re.I,
    )
    return html.unescape(m.group(1)) if m else None


def _title(content: str) -> str | None:
    m = re.search(r'<title>([^<]+)</title>', content, re.I)
    return html.unescape(m.group(1).strip()) if m else None


def _canonical(content: str) -> str | None:
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content, re.I)
    return m.group(1) if m else None


def _inject_before_style(content: str, block: str) -> str:
    """Insert JSON-LD immediately before first <style> or </head>."""
    if block.strip() in content:
        return content
    anchor = re.search(r'\n\s*<style>', content, re.I)
    if anchor:
        pos = anchor.start()
        return content[:pos] + '\n    ' + block + content[pos:]
    return content.replace('</head>', '    ' + block + '\n</head>', 1)


def patch_dictionary(path: str, dry_run: bool) -> bool:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'application/ld+json' in content and 'DefinedTerm' in content:
        return False
    slug = os.path.basename(path)[:-5]
    url = _canonical(content) or f'{BASE}/dictionary/{slug}.html'
    title = _title(content) or slug.replace('-', ' ').title()
    word = title.split('—')[0].split('&mdash;')[0].strip()
    desc = _meta(content, 'description') or f'{word} — biblical definition from The MOOP Dictionary.'
    ld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'DefinedTerm',
        'name': word,
        'termCode': slug,
        'url': url,
        'description': desc[:280],
        'inDefinedTermSet': {
            '@type': 'DefinedTermSet',
            'name': 'The MOOP Dictionary',
            'url': f'{BASE}/dictionary/',
        },
    }, ensure_ascii=False)
    block = f'<script type="application/ld+json">{ld}</script>'
    new_content = _inject_before_style(content, block)
    if new_content == content:
        return False
    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return True


def patch_blog(path: str, dry_run: bool) -> bool:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'application/ld+json' in content and 'BlogPosting' in content:
        return False
    url = _canonical(content)
    if not url:
        slug = os.path.basename(path)[:-5]
        url = f'{BASE}/blog/{slug}.html'
    title = _meta(content, 'og:title', 'property') or _title(content) or ''
    # Strip whichever brand suffix the page carries — legacy initials or the
    # full name newly generated pages use (P2#2b, 2026-08-20).
    for _suffix in (' — U.S.M.C. Ministries', ' &mdash; U.S.M.C. Ministries',
                    ' — Uniting, Serving, Mentoring & Counseling Ministries', ' &mdash; Uniting, Serving, Mentoring & Counseling Ministries',
                    ' — Uniting, Serving, Mentoring and Counseling Ministries', ' &mdash; Uniting, Serving, Mentoring and Counseling Ministries'):
        title = title.replace(_suffix, '')
    title = title.strip()
    desc = _meta(content, 'description') or _meta(content, 'og:description', 'property') or ''
    modified = _meta(content, 'article:modified_time') or _meta(content, 'article:published_time')
    image = _meta(content, 'og:image', 'property') or f'{BASE}/assets/usmc-ministries-full-crest.png'
    ld = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': title,
        'description': desc,
        'url': url,
        'inLanguage': 'en-US',
        'author': {'@type': 'Person', 'name': 'Adam Johns', 'alternateName': "Adam 'MOOP' Johns"},
        'publisher': {
            '@type': 'Organization',
            'name': 'Uniting, Serving, Mentoring and Counseling Ministries',
            'url': BASE,
            'logo': {'@type': 'ImageObject', 'url': f'{BASE}/assets/icons/icon-512.png'},
        },
    }
    if modified:
        ld['dateModified'] = modified
        ld['datePublished'] = modified
    if image:
        ld['image'] = image
    block = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    new_content = _inject_before_style(content, block)
    if new_content == content:
        return False
    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=0, help='Max files per section (0=all)')
    args = ap.parse_args()

    stats = {'dictionary': 0, 'blog': 0}
    for section, fn in (('dictionary', patch_dictionary), ('blog', patch_blog)):
        dirpath = os.path.join(DOCS, section)
        if not os.path.isdir(dirpath):
            continue
        files = sorted(f for f in os.listdir(dirpath) if f.endswith('.html') and f != 'index.html')
        if args.limit:
            files = files[: args.limit]
        for fn_name in files:
            if fn(os.path.join(dirpath, fn_name), args.dry_run):
                stats[section] += 1
        print(f'{section}: patched {stats[section]} pages' + (' (dry-run)' if args.dry_run else ''))

    return 0


if __name__ == '__main__':
    sys.exit(main())
