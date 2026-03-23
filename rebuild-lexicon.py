#!/usr/bin/env python3
"""
rebuild-lexicon.py — Template-based Lexicon Grid Rebuilder
----------------------------------------------------------
Reads the template at docs/assets/lexicon-template.html
Scans all docs/lexicon/H*.html and G*.html for word data
Generates card HTML and inserts between the markers
Writes final docs/lexicon.html
Preserves ALL template content (JS, CSS, structure)

Usage: python3 ~/bible-reading-plan-bot/rebuild-lexicon.py
"""

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATE = SCRIPT_DIR / 'docs' / 'assets' / 'lexicon-template.html'
LEXICON_DIR = SCRIPT_DIR / 'docs' / 'lexicon'
OUTPUT = SCRIPT_DIR / 'docs' / 'lexicon.html'

HEBREW_START = '<!-- HEBREW_CARDS_START -->'
HEBREW_END   = '<!-- HEBREW_CARDS_END -->'
GREEK_START  = '<!-- GREEK_CARDS_START -->'
GREEK_END    = '<!-- GREEK_CARDS_END -->'


def extract_word_data(filepath: Path) -> dict | None:
    """Extract word card data from an individual lexicon word file."""
    try:
        text = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  WARN: Could not read {filepath}: {e}", file=sys.stderr)
        return None

    # Strong's number from filename (H1, G2, etc.)
    stem = filepath.stem  # e.g. "H1" or "G2"

    # Extract original word (Hebrew/Greek script)
    original = ''
    m = re.search(r'class="original-word(?:\s+greek)?"[^>]*>(.*?)</div>', text, re.DOTALL)
    if m:
        original = m.group(1).strip()

    # Transliteration
    translit = ''
    m = re.search(r'class="transliteration"[^>]*>(.*?)</div>', text, re.DOTALL)
    if m:
        translit = m.group(1).strip()

    # Gloss (definition)
    gloss = ''
    m = re.search(r'class="gloss"[^>]*>(.*?)</div>', text, re.DOTALL)
    if m:
        gloss = m.group(1).strip()

    if not gloss and not translit:
        return None  # Skip files with no useful data

    return {
        'id': stem,
        'original': original,
        'translit': translit,
        'gloss': gloss,
    }


def make_card(data: dict) -> str:
    """Generate a word card anchor tag from word data."""
    strongs_id = data['id']
    original = data['original']
    translit = data['translit']
    gloss = data['gloss']

    # Build data-search attribute
    search_parts = [
        strongs_id.lower(),
        translit.lower() if translit else '',
        gloss.lower() if gloss else '',
    ]
    data_search = ' '.join(p for p in search_parts if p)

    # Truncate gloss for display (match original style, max ~40 chars)
    gloss_display = gloss
    if len(gloss) > 40:
        gloss_display = gloss[:37] + '...'

    # Build the card HTML
    parts = [f'<span class="wc-strongs">{strongs_id}</span>']
    if original:
        parts.append(f'<span class="wc-original">{original}</span>')
    if translit:
        parts.append(f'<span class="wc-translit">{translit}</span>')
    parts.append(f'<span class="wc-def">{gloss_display}</span>')

    inner = ''.join(parts)
    href = f'lexicon/{strongs_id}.html'
    return f'<a href="{href}" class="word-card" data-search="{data_search}">{inner}</a>'


def sort_key(stem: str):
    """Sort H1 < H2 < H10 < H100, G1 < G2 < G10..."""
    prefix = stem[0]
    try:
        num = int(stem[1:])
    except ValueError:
        num = 0
    return (prefix, num)


def main():
    print(f"Lexicon Rebuilder — reading template...")

    if not TEMPLATE.exists():
        print(f"ERROR: Template not found at {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE.read_text(encoding='utf-8')

    # Verify markers
    for marker in [HEBREW_START, HEBREW_END, GREEK_START, GREEK_END]:
        if marker not in template:
            print(f"ERROR: Marker '{marker}' not found in template", file=sys.stderr)
            sys.exit(1)

    # Scan lexicon directory
    print(f"Scanning {LEXICON_DIR}...")
    hebrew_words = {}
    greek_words = {}

    for f in LEXICON_DIR.glob('*.html'):
        stem = f.stem
        if stem.startswith('H') and stem[1:].isdigit():
            data = extract_word_data(f)
            if data:
                hebrew_words[stem] = data
        elif stem.startswith('G') and stem[1:].isdigit():
            data = extract_word_data(f)
            if data:
                greek_words[stem] = data

    print(f"  Found {len(hebrew_words)} Hebrew words, {len(greek_words)} Greek words")

    # Sort by number
    sorted_hebrew = sorted(hebrew_words.values(), key=lambda d: sort_key(d['id']))
    sorted_greek  = sorted(greek_words.values(),  key=lambda d: sort_key(d['id']))

    # Generate card HTML blocks
    hebrew_cards = '\n'.join(make_card(d) for d in sorted_hebrew)
    greek_cards  = '\n'.join(make_card(d) for d in sorted_greek)

    # Update subtitle counts in template
    h_count = len(sorted_hebrew)
    g_count = len(sorted_greek)
    result = template
    result = re.sub(
        r'(<p class="section-sub" id="hebrew-sub"[^>]*>)[^<]*',
        rf'\g<1>{h_count} words from the Hebrew Scriptures',
        result
    )
    result = re.sub(
        r'(<p class="section-sub" id="greek-sub"[^>]*>)[^<]*',
        rf'\g<1>{g_count} words from the Greek New Testament',
        result
    )

    # Insert cards between markers
    result = result.replace(
        HEBREW_START + '\n' + HEBREW_END,
        HEBREW_START + '\n' + hebrew_cards + '\n' + HEBREW_END
    )
    result = result.replace(
        GREEK_START + '\n' + GREEK_END,
        GREEK_START + '\n' + greek_cards + '\n' + GREEK_END
    )

    # Write output
    OUTPUT.write_text(result, encoding='utf-8')
    total = h_count + g_count
    print(f"Written: {OUTPUT}")
    print(f"  Total: {total} words ({h_count} Hebrew, {g_count} Greek)")


if __name__ == '__main__':
    main()
