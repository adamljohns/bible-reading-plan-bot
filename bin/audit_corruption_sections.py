#!/usr/bin/env python3
"""Audit every entry's Modern Corruption section for the 'restated teaching'
anti-pattern.

The Modern Corruption section is meant to describe HOW a word has been
postmodernly redefined / diluted / inverted / sentimentalized / weaponized /
forgotten — not to restate the orthodox teaching.

This script flags entries where the corruption_paragraphs (the expandable body)
appear to teach doctrine rather than describe corruption.

Heuristics:
  - HEALTHY signal words (corruption-talk):
      reduced, replaced, redefined, sentimentalized, stripped, weaponized,
      diluted, blunted, lost, forgotten, trivialized, inverted, erased,
      glamorized, marketed, commodified, therapeutic, therapy-culture,
      secularized, relativized, gnosticized, moralized, conflated, collapsed,
      severed, hollowed, romanticized, dismissed, eclipsed, banished,
      mocked-as, redirected, drained, flattened, reframed, weaponizes, age
      tells, modern, postmodern, contemporary, today, popular, marketing,
      pop-culture, instagram, social media, therapy, twitter, internet,
      consumer, branding
  - WARNING signal opener (orthodox-teaching-as-corruption):
      paragraph starts with "X is" / "Y is" / "The X is" / "Christ" / "God"
      and contains a positive teaching frame without corruption vocabulary.
"""
import os, re, sys
from collections import defaultdict

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'docs', 'dictionary')

CORRUPTION_VOCAB = re.compile(
    r'\b('
    r'reduced|replaced|redefined|sentimentaliz|stripped|weaponiz|diluted|'
    r'blunted|lost|forgotten|trivializ|inverted|erased|glamoriz|marketed|'
    r'commodified|therapy[- ]?culture|secular|relativiz|gnosticiz|conflated|'
    r'collapsed|severed|hollowed|romanticiz|dismissed|eclipsed|banished|'
    r'flattened|reframed|drained|the age|modern|postmodern|contemporary|'
    r'today|pop[- ]?culture|instagram|therapy|twitter|consumer|branding|'
    r'cancel[- ]?culture|self[- ]?help|positivity|wellness|ironic'
    r')\b',
    re.IGNORECASE
)

ORTHODOX_OPENER = re.compile(
    r'^\s*(?:The\s+)?[A-Z][a-z]+\s+(?:is|are)\b',
    re.MULTILINE
)

# Extract corruption-paragraph block from a rendered entry HTML.
INNER_PAT = re.compile(
    r'<div class="corruption-inner">(.*?)</div>\s*</details>',
    re.DOTALL
)

def extract_inner(html):
    m = INNER_PAT.search(html)
    if not m:
        return None
    block = m.group(1)
    # Strip HTML tags, keep text only.
    text = re.sub(r'<[^>]+>', ' ', block)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def score_entry(text):
    """Return a tuple (verdict, reason).
    verdict in {'OK', 'WEAK', 'BAD'}.
    """
    if not text:
        return 'EMPTY', 'no inner paragraph'
    n_corruption_hits = len(CORRUPTION_VOCAB.findall(text))
    has_orthodox_opener = bool(ORTHODOX_OPENER.match(text))

    if n_corruption_hits >= 2:
        return 'OK', f'{n_corruption_hits} corruption-vocab hits'
    if n_corruption_hits == 1:
        if has_orthodox_opener:
            return 'WEAK', 'opens orthodox; only 1 corruption-hit'
        return 'OK', '1 corruption-vocab hit (acceptable)'
    # zero corruption hits
    if has_orthodox_opener:
        return 'BAD', 'opens orthodox; zero corruption-vocab'
    return 'WEAK', 'zero corruption-vocab; non-orthodox opener'


def main():
    results = defaultdict(list)
    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html') or fn in ('index.html', 'template.html'):
            continue
        with open(os.path.join(DICT_DIR, fn), 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
        inner = extract_inner(html)
        if inner is None:
            results['NOT_FOUND'].append((fn, ''))
            continue
        verdict, reason = score_entry(inner)
        results[verdict].append((fn, reason, inner[:200]))

    total = sum(len(v) for v in results.values())
    print(f"Scanned {total} entries\n")
    for verdict in ('BAD', 'WEAK', 'OK', 'EMPTY', 'NOT_FOUND'):
        items = results[verdict]
        print(f"{verdict}: {len(items)}")
    print()

    if len(sys.argv) > 1 and sys.argv[1] == '--show-bad':
        print("=== BAD entries (orthodox opener, zero corruption-vocab) ===")
        for fn, reason, sample in results['BAD'][:50]:
            print(f"\n  {fn}  ({reason})")
            print(f"    \"{sample[:160]}...\"")
    if len(sys.argv) > 1 and sys.argv[1] == '--show-weak':
        print("=== WEAK entries (sample 30) ===")
        for fn, reason, sample in results['WEAK'][:30]:
            print(f"\n  {fn}  ({reason})")
            print(f"    \"{sample[:160]}...\"")
    if len(sys.argv) > 1 and sys.argv[1] == '--list-bad':
        for fn, _, _ in results['BAD']:
            print(fn[:-5])

if __name__ == '__main__':
    main()
