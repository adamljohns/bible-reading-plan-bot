#!/usr/bin/env python3
"""autolink_dict_to_lexicon.py — forward Strong's cross-linking.

Many dictionary entries mention a Strong's number as PLAIN TEXT in their
etymology / roots prose (e.g. "Hebrew חֶסֶד (chesed, H2617)") but never link it
to the matching lexicon page. The companion script
autolink_lexicon_from_dict.py wires the INVERSE direction (lexicon page ->
dict backlinks); this script wires the FORWARD direction so a reader on a
dictionary entry can jump straight to the Strong's lexicon entry.

For each dictionary page:
  * Walk the HTML token-by-token, tracking whether we are inside an <a>, a
    <script>, or a <style> so we never wrap a Strong's number that is already a
    link or that lives in code.
  * In plain text, replace the FIRST occurrence of each distinct Strong's
    number (H#### / G####) with
        <a href="../lexicon/<ID>.html" class="lexicon-link">H####</a>
    but ONLY when docs/lexicon/<ID>.html actually exists (leading zeros are
    stripped to match the lexicon filenames).
  * First-occurrence-per-number keeps the page clean (no link spam).

Idempotent: numbers already inside an <a> are skipped, so re-runs are safe.

Usage:
  python3 bin/autolink_dict_to_lexicon.py            # full run
  python3 bin/autolink_dict_to_lexicon.py --dry-run
  python3 bin/autolink_dict_to_lexicon.py --verbose
"""
import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
LEX_DIR = os.path.join(ROOT, 'docs', 'lexicon')

# Split into tags vs text while preserving the tags.
TAG_SPLIT = re.compile(r'(<[^>]+>)')
STRONGS_PAT = re.compile(r'\b([HG])(\d{1,5})\b')
# Strong's IDs already wired to a lexicon page (any form, leading zeros stripped).
ALREADY_LINKED_PAT = re.compile(r'lexicon/([HG])(\d{1,5})\.html')

SPECIAL = {'index', 'names', 'doctrinal-anchors', 'biblical-order',
           'expressly-prohibited', 'most-corrupted', 'gen-z-decoded',
           'millennial-decoded', 'gen-x-decoded', 'boomer-decoded',
           'changelog', 'template', 'by-topic'}


def existing_lex_ids():
    ids = set()
    for p in glob.glob(os.path.join(LEX_DIR, '*.html')):
        base = os.path.basename(p)[:-5]
        m = re.match(r'^([HG])(\d+)$', base)
        if m:
            ids.add(f'{m.group(1)}{int(m.group(2))}')
    return ids


def link_page(html, lex_ids, used):
    """Return (new_html, n_links_added). `used` tracks numbers already linked
    on this page so each distinct Strong's number is linked once."""
    # Seed `used` with any Strong's ID that ALREADY points at a lexicon page,
    # so a number linked in a roots-line (or a prior run) is never linked a
    # second time. This makes the pass idempotent and prevents link-spam.
    for prefix, num in ALREADY_LINKED_PAT.findall(html):
        used.add(f'{prefix}{int(num)}')
    tokens = TAG_SPLIT.split(html)
    depth_a = 0
    in_code = False
    added = 0
    out = []
    for tok in tokens:
        if tok.startswith('<') and tok.endswith('>'):
            low = tok[:512].lower()
            if low.startswith('<a ') or low == '<a>':
                depth_a += 1
            elif low.startswith('</a'):
                depth_a = max(0, depth_a - 1)
            elif low.startswith('<script') or low.startswith('<style'):
                in_code = True
            elif low.startswith('</script') or low.startswith('</style'):
                in_code = False
            out.append(tok)
            continue
        if depth_a > 0 or in_code or not tok:
            out.append(tok)
            continue

        # Plain text token — link first occurrence of each new Strong's number.
        def repl(m):
            nonlocal added
            prefix, num = m.group(1), m.group(2)
            sid = f'{prefix}{int(num)}'
            if sid in used or sid not in lex_ids:
                return m.group(0)
            used.add(sid)
            added += 1
            return (f'<a href="../lexicon/{sid}.html" class="lexicon-link">'
                    f'{m.group(0)}</a>')

        out.append(STRONGS_PAT.sub(repl, tok))
    return ''.join(out), added


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    lex_ids = existing_lex_ids()
    print(f'Lexicon entry pages available: {len(lex_ids)}')

    files = sorted(glob.glob(os.path.join(DICT_DIR, '*.html')))
    pages_changed = 0
    total_links = 0
    for fp in files:
        slug = os.path.basename(fp)[:-5]
        if slug in SPECIAL:
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        new_html, n = link_page(html, lex_ids, set())
        if n > 0 and new_html != html:
            pages_changed += 1
            total_links += n
            if args.verbose:
                print(f'  {slug}: +{n}')
            if not args.dry_run:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_html)

    print()
    print(f'{"DRY-RUN — " if args.dry_run else ""}forward dict->lexicon linking complete.')
    print(f'  dict pages linked:  {pages_changed}')
    print(f'  Strong\'s links added: {total_links}')
    if pages_changed:
        print(f'  avg links/page:     {total_links/pages_changed:.1f}')


if __name__ == '__main__':
    main()
