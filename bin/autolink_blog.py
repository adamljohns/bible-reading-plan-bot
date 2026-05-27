#!/usr/bin/env python3
"""autolink_blog.py — apply dictionary auto-linking to blog HTML.

Walks `docs/blog/*.html` and inside the `<div class="content">…</div>`
region wraps matched dictionary headwords in `<a class="dict-link">`
elements pointing to `../dictionary/<slug>.html`.

Same first-occurrence-per-page rule as the chapter linker (one link per
canonical slug per page). Phrases tried before single tokens; longer
strings preferred to avoid sub-match collisions. Existing anchors are
masked so we never link inside them, and freshly-inserted links are
masked too (the bug I caught on chapter linker).

Container is identified by scanning for paragraphs and headings inside
the article body (`<p>`, `<h2>`, `<h3>`, `<h4>`, `<blockquote>`, `<li>`).
Anything inside `<nav>`, `<footer>`, `<style>`, `<script>` is skipped.

Idempotent: existing dict-link anchors are detected and skipped.

Usage:
  python3 bin/autolink_blog.py                    # all blog posts
  python3 bin/autolink_blog.py --dry-run
  python3 bin/autolink_blog.py --limit 10 --verbose
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'docs', 'dictionary', 'manifest.json')
BLOG_DIR = os.path.join(ROOT, 'docs', 'blog')

# Match content-bearing block elements. We only link inside these.
# Keep the regex non-greedy and bounded by the closing tag to avoid swallowing
# the rest of the document.
LINKABLE_BLOCK_PAT = re.compile(
    r'(<(?:p|h2|h3|h4|h5|h6|blockquote|li)\b[^>]*>)(.*?)(</(?:p|h2|h3|h4|h5|h6|blockquote|li)>)',
    re.DOTALL | re.IGNORECASE
)
ANCHOR_PAT = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)
# Void / self-closing / standalone tag (img, input, br, hr, source, etc.)
# OR any opening/closing tag we should treat as opaque markup, not text.
ANY_TAG_PAT = re.compile(r'<[^>]+>')
# Identify nav/footer/header zones we should NOT touch.
NAV_FOOTER_PAT = re.compile(
    r'(<(?:nav|footer|header|style|script)\b[^>]*>.*?</(?:nav|footer|header|style|script)>)',
    re.DOTALL | re.IGNORECASE
)

DICT_LINK_CSS = (
    '\n    /* injected by bin/autolink_blog.py */\n'
    '    a.dict-link{color:#0a6b7d;text-decoration:none;border-bottom:1px dotted #0a6b7d}\n'
    '    a.dict-link:hover{color:#04424f;border-bottom-style:solid}\n'
)


def load_manifest():
    with open(MANIFEST, 'r', encoding='utf-8') as f:
        m = json.load(f)
    tokens = m.get('tokens', {})
    phrases = m.get('phrases', [])
    phrase_pats = []
    for phrase, slug in phrases:
        words = phrase.split()
        if len(words) < 2:
            continue
        pat = r'\b' + r'\s+'.join(re.escape(w) for w in words) + r'\b'
        phrase_pats.append((slug, re.compile(pat, re.IGNORECASE)))
    sorted_tokens = sorted(tokens.items(), key=lambda kv: (-len(kv[0]), kv[0]))
    token_pats = []
    for token, slug in sorted_tokens:
        pat = r'\b' + re.escape(token) + r'\b'
        token_pats.append((slug, re.compile(pat, re.IGNORECASE)))
    return token_pats, phrase_pats


def linkify_text(body, token_pats, phrase_pats, used_slugs):
    masks = []

    def _store(text):
        masks.append(text)
        return f'\x00MASK{len(masks)-1}\x00'

    # Mask existing anchors FIRST (they're <a>...</a> blocks; we don't want
    # to link inside them, and they may contain inner text we'd otherwise
    # try to match).
    work = ANCHOR_PAT.sub(lambda m: _store(m.group(0)), body)
    # Then mask every remaining HTML tag (e.g., <img src="...">, <p>, </p>,
    # <em>, <strong>, etc.) so token matching never enters tag attributes
    # or markup. After all masks restore, the original structure is intact.
    work = ANY_TAG_PAT.sub(lambda m: _store(m.group(0)), work)

    # Phrases first
    for slug, rgx in phrase_pats:
        if slug in used_slugs:
            continue
        m = rgx.search(work)
        if m:
            matched = m.group(0)
            link = f'<a class="dict-link" href="../dictionary/{slug}.html">{matched}</a>'
            placeholder = _store(link)
            work = work[:m.start()] + placeholder + work[m.end():]
            used_slugs.add(slug)

    # Single tokens
    for slug, rgx in token_pats:
        if slug in used_slugs:
            continue
        m = rgx.search(work)
        if m:
            matched = m.group(0)
            link = f'<a class="dict-link" href="../dictionary/{slug}.html">{matched}</a>'
            placeholder = _store(link)
            work = work[:m.start()] + placeholder + work[m.end():]
            used_slugs.add(slug)

    while '\x00MASK' in work:
        for i, original in enumerate(masks):
            work = work.replace(f'\x00MASK{i}\x00', original)
    return work


def ensure_dict_link_css(html):
    if 'a.dict-link' in html or 'autolink_blog.py' in html:
        return html
    if '</style>' in html:
        return html.replace('</style>', DICT_LINK_CSS + '  </style>', 1)
    return html


def process_blog_post(filepath, token_pats, phrase_pats, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Mask nav/footer/header/style/script regions so linkify never enters them.
    masks = []
    def _store_region(m):
        masks.append(m.group(0))
        return f'\x01ZONE{len(masks)-1}\x01'
    work = NAV_FOOTER_PAT.sub(_store_region, html)

    used_slugs = set()
    new_links = 0

    def _process_block(m):
        nonlocal new_links
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        before = len(used_slugs)
        new_body = linkify_text(body, token_pats, phrase_pats, used_slugs)
        new_links += len(used_slugs) - before
        return opener + new_body + closer

    work = LINKABLE_BLOCK_PAT.sub(_process_block, work)

    # Restore masked zones
    while '\x01ZONE' in work:
        for i, original in enumerate(masks):
            work = work.replace(f'\x01ZONE{i}\x01', original)

    if new_links == 0:
        return 0
    work = ensure_dict_link_css(work)

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(work)
    return new_links


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--pattern', default='*.html')
    args = ap.parse_args()

    token_pats, phrase_pats = load_manifest()
    print(f'Loaded manifest: {len(token_pats)} tokens, {len(phrase_pats)} phrases')

    files = sorted(glob.glob(os.path.join(BLOG_DIR, args.pattern)))
    if args.limit:
        files = files[:args.limit]
    print(f'Processing {len(files)} blog files…')

    total_links = 0
    files_with_links = 0
    for i, fp in enumerate(files):
        n = process_blog_post(fp, token_pats, phrase_pats, dry_run=args.dry_run)
        if n > 0:
            files_with_links += 1
            total_links += n
            if args.verbose:
                print(f'  {os.path.basename(fp)}: +{n}')
        if (i + 1) % 50 == 0:
            print(f'  ... {i+1}/{len(files)} processed')

    print()
    print(f'Done. {"DRY-RUN" if args.dry_run else "Wrote in place"}.')
    print(f'  Total dict links added: {total_links}')
    print(f'  Files affected:         {files_with_links}/{len(files)}')
    if files_with_links:
        print(f'  Avg links per file:     {total_links/files_with_links:.1f}')


if __name__ == '__main__':
    main()
