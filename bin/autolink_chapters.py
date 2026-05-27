#!/usr/bin/env python3
"""autolink_chapters.py — apply dictionary auto-linking to KJV chapter HTML.

Walks every file in `docs/chapters/*.html`, finds the `<ol class="verses">`
block, and inside each `<li data-verse="N" id="vN">VERSE TEXT</li>` wraps
matched dictionary headwords in `<a class="dict-link" href="../dictionary/<slug>.html">...</a>`.

Linking rules (match the BTE v6.3 convention from `docs/bible.html`):
  1. First-occurrence-per-page: each canonical slug is linked at most once
     per chapter file, regardless of how often the word appears.
  2. Longest match wins: phrases (`son of man`, `kingdom of god`) try first;
     single tokens try after.
  3. Word-boundary safe: `\b` anchors prevent matching inside a longer word.
  4. Skip-if-already-linked: tokens already inside an `<a>...</a>` are left
     alone.
  5. Verse-text only: only the inner content of `<li>` inside `<ol class="verses">`
     is touched. Nav, footer, title, attrs are untouched.

Output: rewrites chapter files in place. Reports stats.

Usage:
  python3 bin/autolink_chapters.py                     # all chapters
  python3 bin/autolink_chapters.py --dry-run           # report only
  python3 bin/autolink_chapters.py --pattern joh-*     # subset (glob)
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'docs', 'dictionary', 'manifest.json')
CHAPTERS_DIR = os.path.join(ROOT, 'docs', 'chapters')

# Match a <li data-verse="N" ...>BODY</li> — capture attrs + body separately.
LI_VERSE_PAT = re.compile(
    r'(<li\s+data-verse="\d+"[^>]*>)(.*?)(</li>)',
    re.DOTALL
)
# Match an existing <a ...>...</a> so we can skip its interior.
ANCHOR_PAT = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL | re.IGNORECASE)


def load_manifest():
    """Returns precompiled match lists for both phrases and single tokens.

    Each list element is `(slug, compiled_regex)` so the per-file loop never
    pays the regex-compile cost. Cuts wall-time from ~1.2s/chapter to a small
    fraction.
    """
    with open(MANIFEST, 'r', encoding='utf-8') as f:
        m = json.load(f)
    tokens = m.get('tokens', {})            # {"word": "slug", ...}
    phrases = m.get('phrases', [])          # [["word phrase", "slug"], ...]
    # Compile phrase regexes (multi-word). Already longest-first.
    phrase_pats = []
    for phrase, slug in phrases:
        words = phrase.split()
        if len(words) < 2:
            continue
        pat = r'\b' + r'\s+'.join(re.escape(w) for w in words) + r'\b'
        phrase_pats.append((slug, re.compile(pat, re.IGNORECASE)))
    # Compile token regexes, longest-first by token length.
    sorted_tokens = sorted(tokens.items(), key=lambda kv: (-len(kv[0]), kv[0]))
    token_pats = []
    for token, slug in sorted_tokens:
        pat = r'\b' + re.escape(token) + r'\b'
        token_pats.append((slug, re.compile(pat, re.IGNORECASE)))
    return token_pats, phrase_pats


def linkify_verse_body(body, token_pats, phrase_pats, used_slugs):
    """Apply first-occurrence-per-page linking to a verse body.

    body: inner HTML of a single <li> (typically pure text + some entities)
    used_slugs: set of slugs already linked on this PAGE; mutated.
    Returns: new body string.

    Implementation: we maintain a `masks` list of opaque tokens. Both
    pre-existing <a>...</a> blocks and any link we inject during this
    pass go into `masks` and are replaced with `\\x00MASK<i>\\x00`
    placeholders. The placeholder bytes contain no characters that any
    natural language regex would match, so subsequent matchers (longer
    phrase then shorter tokens) cannot collide with already-linked
    content. At the end we expand the placeholders.
    """
    masks = []

    def _store(text):
        masks.append(text)
        return f'\x00MASK{len(masks)-1}\x00'

    # Mask any existing <a>...</a> so we don't link inside them.
    work = ANCHOR_PAT.sub(lambda m: _store(m.group(0)), body)

    # PHRASES first (multi-word), longest-first (manifest pre-sorts).
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

    # SINGLE-WORD tokens, longest-first.
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

    # Expand all masks. Iterate until none remain (in case any masked
    # content itself contains an earlier mask placeholder — shouldn't
    # happen with our placeholder bytes, but defensive).
    while '\x00MASK' in work:
        for i, original in enumerate(masks):
            work = work.replace(f'\x00MASK{i}\x00', original)

    return work


# CSS injection for chapter pages — added once per file if missing.
DICT_LINK_CSS = (
    '\n    /* injected by bin/autolink_chapters.py */\n'
    '    a.dict-link{color:#0a6b7d;text-decoration:none;border-bottom:1px dotted #0a6b7d}\n'
    '    a.dict-link:hover{color:#04424f;border-bottom-style:solid}\n'
)


def ensure_dict_link_css(html):
    """Inject dict-link CSS once per page (idempotent via marker comment)."""
    if 'a.dict-link' in html or 'autolink_chapters.py' in html:
        return html
    # Insert before the closing </style>
    return html.replace('</style>', DICT_LINK_CSS + '  </style>', 1)


def process_chapter(filepath, token_pats, phrase_pats, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    used_slugs = set()
    new_links = 0

    def _process_li(m):
        nonlocal new_links
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        before_count = len(used_slugs)
        new_body = linkify_verse_body(body, token_pats, phrase_pats, used_slugs)
        added = len(used_slugs) - before_count
        new_links += added
        return opener + new_body + closer

    new_html = LI_VERSE_PAT.sub(_process_li, html)

    if new_links == 0:
        return 0  # nothing to do
    new_html = ensure_dict_link_css(new_html)

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)

    return new_links


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true', help='Report counts without writing')
    ap.add_argument('--pattern', default='*.html', help='Glob inside docs/chapters/ (default *.html)')
    ap.add_argument('--limit', type=int, default=None, help='Process at most N files')
    ap.add_argument('--verbose', action='store_true', help='Print per-file link count')
    args = ap.parse_args()

    token_pats, phrase_pats = load_manifest()
    print(f'Loaded manifest: {len(token_pats)} tokens, {len(phrase_pats)} phrases (regexes precompiled)')

    files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, args.pattern)))
    if args.limit:
        files = files[:args.limit]
    print(f'Processing {len(files)} chapter files...')

    total_links = 0
    files_with_links = 0
    for i, fp in enumerate(files):
        n = process_chapter(fp, token_pats, phrase_pats, dry_run=args.dry_run)
        if n > 0:
            files_with_links += 1
            total_links += n
            if args.verbose:
                print(f'  {os.path.basename(fp)}: +{n}')
        if (i + 1) % 200 == 0:
            print(f'  ... {i+1}/{len(files)} processed')

    avg = total_links / max(1, files_with_links)
    print()
    print(f'Done. {"DRY-RUN — no writes" if args.dry_run else "Wrote in place"}.')
    print(f'  Total dictionary links added: {total_links}')
    print(f'  Files affected: {files_with_links}/{len(files)}')
    print(f'  Avg links per affected file:  {avg:.1f}')


if __name__ == '__main__':
    main()
