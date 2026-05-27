#!/usr/bin/env python3
"""autolink_lexicon_from_dict.py — bidirectional Strong's-number cross-linking.

Inverse index: scan every dictionary entry for Strong's references in
roots_lines / body text (`(H123)`, `(G456)`). For each Strong's number
collected, find the matching `docs/lexicon/<H|G><n>.html` page and inject a
"Related Dictionary Entries" block with backlinks.

Linking rules:
  * One backlink per dictionary entry per lexicon page (no duplicates).
  * Idempotent — uses <!-- DICT-BACKLINKS-START --> / END markers so re-runs
    replace the existing block rather than stacking.
  * If a Strong's number has no dict references, the page is left alone.
  * The block is injected into the existing `<div class="related-words">` so
    it inherits the page's pill styling.

Usage:
  python3 bin/autolink_lexicon_from_dict.py            # full run
  python3 bin/autolink_lexicon_from_dict.py --dry-run
  python3 bin/autolink_lexicon_from_dict.py --limit 50
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
LEX_DIR = os.path.join(ROOT, 'docs', 'lexicon')

STRONGS_PAT = re.compile(r'\b([HG])(\d{1,5})\b')
# extract headword from dict entry — match build_dict_manifest.py logic
WORD_DIV_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
H1_WORD_PAT = re.compile(r'<h1[^>]*class="[^"]*word-title[^"]*"[^>]*>(.*?)</h1>', re.DOTALL)
BARE_H1_PAT = re.compile(r'<body[^>]*>.*?<h1[^>]*>(.*?)</h1>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')

# Markers — let us re-inject without stacking
START_MARK = '<!-- DICT-BACKLINKS-START -->'
END_MARK = '<!-- DICT-BACKLINKS-END -->'
# Existing related-words block in lex pages
RELATED_BLOCK_PAT = re.compile(
    r'(<div class="related-words">)(.*?)(</div>\s*</div>\s*<div class="section">\s*<h2>External Resources)',
    re.DOTALL
)
# Existing dict-backlinks block (idempotency)
EXISTING_BACKLINKS_PAT = re.compile(
    re.escape(START_MARK) + r'.*?' + re.escape(END_MARK),
    re.DOTALL
)


def clean_headword(text):
    text = TAG_STRIP.sub('', text)
    text = text.replace('&amp;', '&').replace('&mdash;', '—')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_headword(html):
    for pat in (WORD_DIV_PAT, H1_WORD_PAT, BARE_H1_PAT):
        m = pat.search(html)
        if m:
            w = clean_headword(m.group(1))
            if w:
                return w
    return None


def build_inverse_index():
    """Walk dictionary, build {strong_id: [(slug, headword), ...]} map."""
    inverse = {}
    SPECIAL = {'index', 'names', 'doctrinal-anchors', 'biblical-order',
               'expressly-prohibited', 'most-corrupted', 'gen-z-decoded',
               'millennial-decoded', 'gen-x-decoded', 'boomer-decoded',
               'changelog', 'template'}
    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html'):
            continue
        slug = fn[:-5]
        if slug in SPECIAL:
            continue
        fp = os.path.join(DICT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        word = extract_headword(html)
        if not word:
            continue
        # Find all H### / G### refs in the entry
        refs = set()
        for prefix, num in STRONGS_PAT.findall(html):
            try:
                # Strip leading zeros — lexicon files use bare numerics
                refs.add(f'{prefix}{int(num)}')
            except ValueError:
                pass
        for ref in refs:
            inverse.setdefault(ref, []).append((slug, word))
    # Sort each entry's backlinks alphabetically by headword for stable output
    for ref in inverse:
        inverse[ref].sort(key=lambda sw: sw[1].lower())
    return inverse


def render_backlinks_html(entries):
    """Render dict backlinks as styled pills in a single HTML block.

    When multiple entries share the same headword (e.g., 'Gehenna' from
    both `gehenna` and `gehenna-fire` slugs), append a slug suffix to
    disambiguate.
    """
    # Count headword frequencies for disambiguation
    from collections import Counter
    word_counts = Counter(w for _, w in entries)
    pills = []
    for slug, word in entries:
        if word_counts[word] > 1:
            # Show slug suffix to disambiguate, but only the differentiating part
            label = f'{word} <span style="opacity:0.7;font-size:0.85em;">({slug})</span>'
            title = f'MOOP Dictionary: {word} ({slug})'
        else:
            label = word
            title = f'MOOP Dictionary: {word}'
        pills.append(
            f'<a class="related-word" href="../dictionary/{slug}.html" '
            f'title="{title}">📖 {label}</a>'
        )
    inner = ' '.join(pills)
    return (
        f'{START_MARK}\n'
        f'                <div style="margin-top:18px;padding-top:14px;'
        f'border-top:1px dashed var(--border);">\n'
        f'                  <p style="color:var(--gold);font-size:0.95rem;'
        f'margin-bottom:10px;font-weight:600;">📖 MOOP Dictionary Entries '
        f'rooted in this Strong\'s number:</p>\n'
        f'                  <div class="related-words">{inner}</div>\n'
        f'                </div>\n'
        f'                {END_MARK}'
    )


def lexicon_strong_id(filename):
    """Extract H123 / G456 from a lexicon filename like 'G26.html'."""
    base = os.path.splitext(filename)[0]
    m = re.match(r'^([HG])(\d+)$', base)
    if not m:
        return None
    return f'{m.group(1)}{int(m.group(2))}'


def process_lexicon_page(filepath, inverse, dry_run=False):
    strong_id = lexicon_strong_id(os.path.basename(filepath))
    if not strong_id:
        return 0
    entries = inverse.get(strong_id, [])
    if not entries:
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    new_block = render_backlinks_html(entries)

    # If an existing block exists, replace it. Else inject inside the
    # related-words section (after its opening div).
    if START_MARK in html:
        new_html = EXISTING_BACKLINKS_PAT.sub(new_block, html)
    else:
        # Find the related-words div and inject AFTER its content but
        # BEFORE the section's </div></div><div class="section">External
        m = RELATED_BLOCK_PAT.search(html)
        if not m:
            # Page structure differs from expected — skip silently
            return 0
        # Insert backlinks after the existing related-words div (before
        # the closing </div></div> of the Related Words section).
        full = m.group(0)
        # Place the new block right after the existing related-words div
        existing_related_div = m.group(1) + m.group(2) + '</div>'
        injection = existing_related_div + '\n                ' + new_block + '\n            '
        # Replace: open + body + first close → injection (then keep the
        # outer </div><div class="section"><h2>External part)
        rest = '</div>\n        <div class="section">\n            <h2>External Resources'
        replacement = injection + rest
        new_html = html.replace(full, replacement, 1)

    if new_html == html:
        return 0
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
    return len(entries)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--pattern', default='*.html')
    args = ap.parse_args()

    print('Building inverse index from dictionary…')
    inverse = build_inverse_index()
    print(f'  Strong\'s numbers referenced: {len(inverse)}')
    total_backlinks_available = sum(len(v) for v in inverse.values())
    print(f'  Total dict-entry backlinks available: {total_backlinks_available}')

    files = sorted(glob.glob(os.path.join(LEX_DIR, args.pattern)))
    if args.limit:
        files = files[:args.limit]
    print(f'Processing {len(files)} lexicon files…')

    total_injected = 0
    files_with_links = 0
    for i, fp in enumerate(files):
        n = process_lexicon_page(fp, inverse, dry_run=args.dry_run)
        if n > 0:
            files_with_links += 1
            total_injected += n
            if args.verbose:
                print(f'  {os.path.basename(fp)}: +{n} backlinks')
        if (i + 1) % 2000 == 0:
            print(f'  ... {i+1}/{len(files)} processed')

    print()
    print(f'Done. {"DRY-RUN" if args.dry_run else "Wrote in place"}.')
    print(f'  Backlinks injected:     {total_injected}')
    print(f'  Lexicon pages updated:  {files_with_links}/{len(files)}')
    if files_with_links:
        print(f'  Avg backlinks/lex page: {total_injected/files_with_links:.1f}')


if __name__ == '__main__':
    main()
