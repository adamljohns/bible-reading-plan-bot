#!/usr/bin/env python3
"""find_concept_duplicates.py — find entries that DEFINE THE SAME CONCEPT under
different names.

bin/find_duplicates.py groups by normalized display title, so it catches
'Wrath of the Lamb' written twice (wrath-lamb / wrath-of-the-lamb). It cannot
catch `wrath` against `wrath-of-god`, whose titles differ while their biblical
definitions open with almost the same sentence. Adam, 2026-08-05: "wrath has
two entries... that's the kind of thing I want to avoid — two definitions that
are basically the same. Expand one definition to encapsulate both concepts
instead."

So this compares the DEFINITION TEXT, not the title.

Method: tokenize each entry's biblical definition, drop stopwords and tokens so
common they carry no signal, build an inverted index over the remaining rare
tokens, and only score pairs that share several of them. That keeps it near
O(n) instead of the 31 million comparisons a full pairwise scan would need.
Pairs are ranked by Jaccard overlap.

NEVER auto-merges. The roadmap is explicit that human review decides every
merge, and that intentional theological disambiguations (grace-prevenient vs
grace-common, dualism-cartesian vs dualism-gnostic) must be KEPT. This only
reports, and flags which pairs look intentional.

Usage:
  python3 bin/find_concept_duplicates.py                  # top candidates
  python3 bin/find_concept_duplicates.py --min 0.45       # loosen threshold
  python3 bin/find_concept_duplicates.py --out data/concept-dupes.txt
"""
from __future__ import annotations
import os, re, sys, html, glob, argparse
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs/dictionary')

SPECIAL = set("""index names doctrinal-anchors biblical-order expressly-prohibited
most-corrupted gen-z-decoded millennial-decoded gen-x-decoded boomer-decoded
christianese-decoded jesus-generation changelog baby-names by-topic""".split())

STOP = set("""a an the and or but if of in on at to for with by from as is was were be
been being are am it its his her their our your my me him them us you we they he she
this that these those there here not no nor so than then when where which who whom
whose what how all any both each few more most other some such only own same too very
can will just should now shall unto up out down into over under again further once
about against between through during before after above below off do does did doing
have has had having would could may might must let s t not god lord jesus christ
scripture bible biblical word words man men one two also because through""".split())

# Suffixes that usually mark a DELIBERATE distinction rather than a redundancy.
DISAMBIG = re.compile(
    r'-(figure|book|town|city|place|prophet|king|priest|son|daughter|apostle|tribe|'
    r'mount|river|valley|brook|sin|detailed|modern|name|people|the-\w+)$')

def extract_def(path):
    """Definition text only, anchored on the page's own section id.

    Matching on the words 'Biblical Definition' and falling back to the whole
    document was wrong: pages without that section (the Gen-Z Decoded set)
    fell through to the full HTML, so slay/vibe/rizz/gyat scored 0.95 against
    each other on shared page chrome and JSON-LD. Returning nothing is the
    honest answer for a page that has no definition section.
    """
    h = open(path, encoding='utf-8', errors='replace').read()
    m = re.search(r'class="biblical-def"[^>]*>(.*?)(?=<div class="section"|<h3)', h, re.S)
    if not m:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html.unescape(m.group(1)))
    return re.sub(r'\s+', ' ', text).strip()

def tokens(text):
    ws = re.findall(r"[a-z][a-z'-]{2,}", text.lower())
    return {w for w in ws if w not in STOP}

def name_tokens(slug):
    parts = [p for p in slug.split('-') if p not in ('the', 'of', 'a', 'an')]
    return set(parts)

def name_related(a, b):
    """True duplicates almost always carry related names -- wrath/wrath-of-god,
    emmanuel/immanuel, ebal/mount-ebal, wheat-tares/wheat-and-tares. Entries
    that merely share an authoring template (two obscure Judahite towns, four
    Gen-Z slang entries) do not. This is the signal that separates them."""
    na, nb = name_tokens(a), name_tokens(b)
    if na & nb:
        return True
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.80

def opening(text, n=260):
    """The concept statement lives in the first sentence or two; later
    paragraphs drift into application and dilute an otherwise exact match."""
    return text[:n]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min', type=float, default=0.50, help='Jaccard threshold')
    ap.add_argument('--top', type=int, default=60)
    ap.add_argument('--out')
    args = ap.parse_args()

    docs, opens = {}, {}
    for f in sorted(glob.glob(os.path.join(DICT, '*.html'))):
        slug = os.path.basename(f)[:-5]
        if slug in SPECIAL:
            continue
        d = extract_def(f)
        if len(d) < 120:          # stubs and redirects carry no definition
            continue
        t = tokens(d[:1200])
        if len(t) >= 12:
            docs[slug] = t
            opens[slug] = tokens(opening(d))

    print(f'entries with a usable definition: {len(docs)}')

    # Inverted index over tokens that are rare enough to be discriminating.
    df = defaultdict(int)
    for t in docs.values():
        for w in t:
            df[w] += 1
    ceiling = max(3, int(len(docs) * 0.02))
    index = defaultdict(list)
    for slug, t in docs.items():
        for w in t:
            if df[w] <= ceiling:
                index[w].append(slug)

    # Candidate pairs = those sharing several rare tokens.
    shared = defaultdict(int)
    for w, slugs in index.items():
        if len(slugs) < 2 or len(slugs) > 40:
            continue
        for i in range(len(slugs)):
            for j in range(i + 1, len(slugs)):
                a, b = sorted((slugs[i], slugs[j]))
                shared[(a, b)] += 1

    pairs = []
    for (a, b), n in shared.items():
        if n < 4:
            continue
        ta, tb = docs[a], docs[b]
        union = len(ta | tb)
        if not union:
            continue
        jac = len(ta & tb) / union
        # Score on whichever is stronger: the whole definition, or just the
        # opening. wrath vs wrath-of-god share an almost verbatim first
        # sentence but diverge after it, scoring only 0.27 whole-text.
        oa, ob = opens[a], opens[b]
        ojac = len(oa & ob) / len(oa | ob) if (oa and ob) else 0.0
        score = max(jac, ojac)
        if score >= args.min:
            pairs.append((score, jac, ojac, a, b))

    pairs.sort(reverse=True)

    strong = [p for p in pairs if name_related(p[3], p[4])]
    weak = [p for p in pairs if not name_related(p[3], p[4])]
    print(f'candidate pairs above {args.min:.2f}: {len(pairs)}')
    print(f'  with related names (real merge candidates): {len(strong)}')
    print(f'  unrelated names (likely shared template):   {len(weak)}\n')

    lines = []
    print('=== MERGE CANDIDATES (same concept, related names) ===')
    for score, jac, ojac, a, b in strong[:args.top]:
        intentional = bool(DISAMBIG.search(a) or DISAMBIG.search(b))
        tag = 'review — suffix suggests intentional' if intentional else 'MERGE'
        line = f'{score:.2f} (full {jac:.2f} / open {ojac:.2f})  {a:30} {b:30} {tag}'
        lines.append(line)
        print('  ' + line)

    if weak:
        print('\n=== shared-template pairs (probably NOT duplicates) ===')
        for score, jac, ojac, a, b in weak[:12]:
            print(f'  {score:.2f}  {a:30} {b:30}')

    if args.out:
        with open(args.out, 'w') as fh:
            fh.write('\n'.join(f'{j:.4f}\t{a}\t{b}' for j, a, b in pairs) + '\n')
        print(f'\nWrote {len(pairs)} pairs -> {args.out}')

if __name__ == '__main__':
    main()
