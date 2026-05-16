#!/usr/bin/env python3
"""Fix broken lexicon references in dictionary entries.

Three transformations applied in order:
  1. Missing '../' prefix:
     href="lexicon/H2617.html" -> href="../lexicon/H2617.html"
     (only when the ../lexicon/H2617.html target exists)

  2. Strip leading zeros from Strong's numbers:
     href="../lexicon/G0040.html" -> href="../lexicon/G40.html"
     (only when the stripped variant exists)

  3. Unwrap remaining broken lexicon <a> tags:
     <a href="../lexicon/G4997.html">temperance</a> -> temperance
     (leaves the visible word as plain text; no more 404 on click)
"""
import os
import re
import glob

DICT_DIR = 'docs/dictionary'
LEX_DIR = 'docs/lexicon'


def existing_lex_slugs():
    return {os.path.basename(p).replace('.html', '')
            for p in glob.glob(os.path.join(LEX_DIR, '*.html'))}


def strip_leading_zeros(slug):
    """G0040 -> G40, H0578 -> H578."""
    m = re.match(r'^([GH])0+(\d+)$', slug)
    if m:
        return m.group(1) + m.group(2)
    return slug


# Pattern matches href="lexicon/HxxxN.html" or href="../lexicon/HxxxN.html"
# (with optional anchor or query)
LEX_HREF_RE = re.compile(
    r'href="((?:\.\./)?lexicon/)([GH]\d+)(\.html)([^"]*)"',
    re.IGNORECASE
)


def main():
    lex_slugs = existing_lex_slugs()
    print(f'Existing lexicon entries: {len(lex_slugs)}')

    n_dotdot_added = 0
    n_zero_stripped = 0

    for fp in sorted(glob.glob(os.path.join(DICT_DIR, '*.html'))):
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        orig = html

        def fix_href(m):
            nonlocal n_dotdot_added, n_zero_stripped
            prefix = m.group(1)  # "lexicon/" or "../lexicon/"
            slug = m.group(2)    # G1234 etc.
            ext = m.group(3)     # .html
            tail = m.group(4)    # anchor/query if any

            # Step 1: add ../ if missing
            if prefix == 'lexicon/':
                prefix = '../lexicon/'
                n_dotdot_added += 1

            # Step 2: try slug as-is
            if slug in lex_slugs:
                return f'href="{prefix}{slug}{ext}{tail}"'

            # Step 3: try stripping leading zeros
            stripped = strip_leading_zeros(slug)
            if stripped != slug and stripped in lex_slugs:
                n_zero_stripped += 1
                return f'href="{prefix}{stripped}{ext}{tail}"'

            # Couldn't fix — leave the broken href for step 4 (unwrap pass)
            return f'href="{prefix}{slug}{ext}{tail}"'

        html = LEX_HREF_RE.sub(fix_href, html)

        if html != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html)

    print(f'Added ../ prefix to {n_dotdot_added} refs')
    print(f'Stripped leading zeros on {n_zero_stripped} refs')

    # Step 4: unwrap remaining broken refs (lexicon target still doesn't exist)
    BROKEN_LEX_A_RE = re.compile(
        r'<a\s+href="(\.\./)?lexicon/([GH]\d+)\.html(#[^"]*)?"([^>]*)>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )

    n_unwrapped = 0
    for fp in sorted(glob.glob(os.path.join(DICT_DIR, '*.html'))):
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()

        unwrapped_here = [0]

        def unwrap_if_missing(m):
            slug = m.group(2)
            inner = m.group(5)
            if slug in lex_slugs:
                return m.group(0)
            unwrapped_here[0] += 1
            return inner

        new_html = BROKEN_LEX_A_RE.sub(unwrap_if_missing, html)
        if unwrapped_here[0] > 0:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_html)
            n_unwrapped += unwrapped_here[0]

    print(f'Unwrapped {n_unwrapped} broken lexicon refs')


if __name__ == '__main__':
    main()
