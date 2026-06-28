#!/usr/bin/env python3
"""Find duplicate / near-duplicate dictionary entries — candidates for merge_entries.py.

Groups live entry pages by NORMALIZED display title and tiers each multi-slug
cluster by how likely it is a true redundancy (one concept written several times,
like 'submission') versus an intentional same-name distinction (two biblical
figures named John; a place AND a doctrine of the same name).

Signals used (never auto-merges — this only REPORTS for review):
  - cluster size (3+ near-identical slugs is a strong redundancy signal)
  - qualifier suffix kind: REDUNDANT (-doctrine, -biblical, -the-doctrine, -2,
    trailing numerals) vs DISAMBIGUATING (-place, -figure, -prophet, -king,
    -book, -son-of-…, -apostle, -the-…) which usually mark DISTINCT entities
  - biblical-definition overlap (first ~200 chars cosine-ish word overlap)

Tier 1 = high-confidence redundancy (review then merge). Tier 2 = review-only.
"""
from __future__ import annotations

import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs', 'dictionary')

SPECIAL = {'index', 'template', 'names', 'baby-names', 'by-topic', 'changelog',
           'doctrinal-anchors', 'biblical-order', 'expressly-prohibited',
           'most-corrupted', 'gen-z-decoded', 'millennial-decoded',
           'gen-x-decoded', 'boomer-decoded', 'christianese-decoded', 'jesus-generation'}
REDIR = set()
_r = os.path.join(ROOT, 'data', 'dictionary-redirects.txt')
if os.path.exists(_r):
    REDIR = {l.split('->')[0].strip() for l in open(_r) if '->' in l}

# suffixes that mark a DISTINCT entity sharing a name — never auto-merge these
DISAMBIG = ('-place', '-figure', '-prophet', '-king', '-book', '-apostle',
            '-the-elder', '-the-younger', '-son', '-daughter', '-of-', '-judge',
            '-priest', '-seer', '-scribe', '-singer', '-disciple', '-mighty-man',
            '-the-', '-companion', '-governor', '-evangelist', '-bishop')
# suffixes that usually mark a REDUNDANT re-statement of the same concept
REDUNDANT = ('-doctrine', '-biblical', '-the-doctrine', '-defined', '-meaning', '-word')


def norm_title(t):
    t = re.sub(r'\([^)]*\)', '', t)          # drop "(Doctrine)", "(Wife)" ...
    t = re.sub(r'[^a-z0-9 ]', '', t.lower()).strip()
    t = re.sub(r'\s+', ' ', t)
    return t


def entry_info(slug):
    t = open(os.path.join(DICT, slug + '.html'), encoding='utf-8').read()
    wt = re.search(r'<div class="word-title">([^<]+)</div>', t)
    bd = re.search(r'<div class="biblical-def">\s*<p>(.*?)</p>', t, re.DOTALL)
    bd = re.sub(r'<[^>]+>', '', bd.group(1))[:240] if bd else ''
    inbound = 0
    return (wt.group(1).strip() if wt else slug), bd


def def_overlap(a, b):
    wa = set(re.findall(r'[a-z]{4,}', a.lower()))
    wb = set(re.findall(r'[a-z]{4,}', b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def main():
    groups = defaultdict(list)
    for fn in os.listdir(DICT):
        if not fn.endswith('.html'):
            continue
        slug = fn[:-5]
        if slug in SPECIAL or slug in REDIR:
            continue
        title, bd = entry_info(slug)
        groups[norm_title(title)].append((slug, title, bd))

    tier1, tier2 = [], []
    for key, members in groups.items():
        if len(members) < 2 or not key:
            continue
        slugs = [m[0] for m in members]
        # any disambiguation suffix in the cluster -> treat as DISTINCT (review only)
        disambig = any(any(d in s for d in DISAMBIG) for s in slugs)
        # redundant-suffix variants of a shared base?
        bases = {re.sub(r'(-doctrine|-biblical|-the-doctrine|-defined|-\d+)$', '', s) for s in slugs}
        redundant_variant = len(bases) < len(slugs) or any(
            any(s.endswith(r) for r in REDUNDANT) for s in slugs)
        # def overlap between the two longest defs
        defs = sorted((m[2] for m in members), key=len, reverse=True)
        ov = def_overlap(defs[0], defs[1]) if len(defs) >= 2 else 0.0
        rec = (key, members, ov, disambig, redundant_variant)
        if (len(members) >= 3 or redundant_variant or ov >= 0.5) and not disambig:
            tier1.append(rec)
        else:
            tier2.append(rec)

    print(f'duplicate-title clusters: {len(tier1)+len(tier2)} '
          f'(tier1 merge-candidates: {len(tier1)}, tier2 review: {len(tier2)})\n')
    print('=== TIER 1 — high-confidence redundancy (review then merge) ===')
    for key, members, ov, _, rv in sorted(tier1, key=lambda r: -len(r[1])):
        tag = f'overlap={ov:.2f}' + (' redundant-suffix' if rv else '')
        print(f'  [{len(members)}] "{key}"  ({tag})')
        for s, t, _ in members:
            print(f'        {s:42} "{t}"')
    print(f'\n=== TIER 2 — review only (likely distinct or intentional): {len(tier2)} clusters ===')
    for key, members, ov, da, rv in sorted(tier2, key=lambda r: -len(r[1]))[:25]:
        print(f'  [{len(members)}] "{key}"  ({"disambig" if da else "ov=%.2f"%ov}): '
              + ', '.join(m[0] for m in members))


if __name__ == '__main__':
    main()
