#!/usr/bin/env python3
"""Build /dictionary/manifest.json — a fast lookup table the BTE viewer can
fetch once and use to wrap dictionary words in verse text with links.

For each entry it captures:
  slug:        the URL-safe slug (filename without .html)
  word:        the human-readable headword (extracted from <h1 class="word-title">
               or first non-stub h1)
  match_keys:  one or more lowercased space-collapsed strings the BTE
               highlighter should match against in verse text. Includes
               the headword, its singular/plural variants, and any
               obvious tokenizations of multi-word slugs.

Output is a flat JSON map of:
  {
    "tokens": { "<lowercased-token>": "<slug>", ... },   # single-word matches
    "phrases": [ ["<lowercased-phrase>", "<slug>"], ... ] # multi-word matches
  }

The split keeps the highlighter fast: it uses the tokens map for
single-word lookups (O(1) per word) and the phrases list for the
small set of multi-word matches (O(n)).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
OUTPUT = os.path.join(DICT_DIR, 'manifest.json')

# Stop-words and short words to skip — these would over-match verse text.
SKIP_WORDS = {
    'a', 'an', 'and', 'as', 'at', 'be', 'but', 'by', 'do', 'for', 'from',
    'go', 'has', 'have', 'he', 'her', 'him', 'his', 'i', 'if', 'in', 'is',
    'it', 'its', 'me', 'my', 'no', 'not', 'of', 'on', 'or', 'our', 's', 'so',
    'the', 'their', 'them', 'they', 'this', 'to', 'us', 'we', 'with',
    'who', 'whose', 'whom', 'will', 'would', 'were', 'was', 'what', 'when',
    'where', 'which', 'why', 'how', 'all', 'any', 'are', 'been', 'being',
    'before', 'between', 'both', 'each', 'her', 'here', 'into', 'one', 'only',
    'other', 'same', 'such', 'than', 'that', 'then', 'there', 'these',
    'those', 'too', 'up', 'very', 'you', 'your', 'about', 'after', 'again',
    'now', 'also',
}

# Headword extractor — works with the new template (.word-title)
WORD_TITLE_PAT = re.compile(
    r'<div class="word-title">([^<]+)</div>',
    re.DOTALL
)
# Older/alt: <h1 class="word-title">
H1_TITLE_PAT = re.compile(
    r'<h1[^>]*class="[^"]*word-title[^"]*"[^>]*>([^<]+)</h1>',
    re.DOTALL
)

def extract_word(html):
    m = WORD_TITLE_PAT.search(html)
    if m:
        return m.group(1).strip()
    m = H1_TITLE_PAT.search(html)
    if m:
        return m.group(1).strip()
    return None


# Biblical-def summary extractor — first paragraph of biblical_def.
BIBLICAL_DEF_PAT = re.compile(
    r'<div class="biblical-def">\s*<p>(.*?)</p>',
    re.DOTALL
)

TAG_STRIP = re.compile(r'<[^>]+>')
ENTITY_DECODE = {
    '&mdash;': '—', '&ndash;': '–', '&amp;': '&',
    '&#39;': "'", '&apos;': "'", '&quot;': '"', '&nbsp;': ' ',
    '&lt;': '<', '&gt;': '>',
}

def extract_summary(html, max_chars=180):
    """Extract a short biblical-def summary (first ~180 chars, sentence-clean)."""
    m = BIBLICAL_DEF_PAT.search(html)
    if not m:
        return None
    text = m.group(1)
    # Strip HTML tags
    text = TAG_STRIP.sub('', text)
    # Decode common entities
    for ent, ch in ENTITY_DECODE.items():
        text = text.replace(ent, ch)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Trim to first sentence-end within max_chars window if possible
    if len(text) > max_chars:
        # Try to break on sentence boundary near max_chars
        cutoff = max_chars
        # Find last period/semicolon/em-dash before cutoff
        match = re.search(r'^.{1,' + str(max_chars) + r'}[.;—]', text)
        if match:
            text = match.group(0)
        else:
            text = text[:max_chars].rsplit(' ', 1)[0] + '…'
    return text.strip()


def normalize(s):
    """Lowercase, decode common entities, collapse whitespace."""
    s = s.replace('&mdash;', '—').replace('&ndash;', '–').replace('&amp;', '&')
    s = s.replace('&#39;', "'").replace('&apos;', "'").replace('&quot;', '"')
    s = re.sub(r'\s+', ' ', s).strip().lower()
    # Strip outer parenthetical qualifiers e.g. "Allegory (Biblical)" → "allegory"
    s = re.sub(r'\s*\([^)]*\)\s*', '', s)
    return s.strip()


def main():
    tokens = {}
    phrases = []
    summaries = {}
    skipped_no_word = 0
    total = 0
    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html') or fn in ('index.html', 'template.html'):
            continue
        slug = fn[:-5]
        fp = os.path.join(DICT_DIR, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            html = f.read()
        word = extract_word(html)
        if not word:
            skipped_no_word += 1
            continue
        norm = normalize(word)
        total += 1
        # Capture summary regardless of whether the word goes into tokens
        summary = extract_summary(html)
        if summary:
            summaries[slug] = summary
        if not norm or norm in SKIP_WORDS:
            continue
        # Single-token vs multi-token
        if ' ' in norm:
            phrases.append([norm, slug])
        else:
            # Skip very short words that would over-match
            if len(norm) < 4:
                continue
            # First-come wins; if duplicate (e.g. plural-form already mapped),
            # prefer the shorter slug as canonical
            if norm not in tokens or len(slug) < len(tokens[norm]):
                tokens[norm] = slug

    manifest = {
        'version': 2,
        'generated_at_count': total,
        'tokens': tokens,
        'phrases': sorted(phrases, key=lambda p: (-len(p[0]), p[0])),
        'summaries': summaries,
    }
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=0, separators=(',', ':'))

    print(f"Wrote manifest: {OUTPUT}")
    print(f"  Entries with extractable headword: {total}")
    print(f"  Single-word matches (tokens):     {len(tokens)}")
    print(f"  Multi-word matches (phrases):     {len(phrases)}")
    print(f"  Hover summaries captured:         {len(summaries)}")
    print(f"  Skipped (no headword found):      {skipped_no_word}")
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"  File size:                         {size_kb:.1f} KB")


if __name__ == '__main__':
    main()
