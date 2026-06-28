#!/usr/bin/env python3
"""Curate the topical Special-Directory sections toward ~100 cards each.

Unlike the generational/christianese DECODER sections (whose cards are authored
with verdicts), the TOPICAL sections (Doctrinal Anchors, Most Corrupted, ...)
are curated collections of EXISTING corpus entries. This tool refills their
card grids in rebuild-dictionary.py from VETTED slug sources — never a blind
auto-rank, because raw signals (e.g. corruption-section length) surface biblical
realia like Red Heifer / Mite that are not what a reader means by "corrupted."

Sources are intentionally editorial:
  - doctrinal-anchors  <- the doctrine categories curated in bin/build_by_topic.py
  - most-corrupted     <- the corruption-correctors category + a curated
                          culture-war word list + the section's existing picks

Usage:
  python3 bin/curate_sections.py            # dry run: print selections + counts
  python3 bin/curate_sections.py --apply    # rewrite the section grids in rebuild-dictionary.py
Then run rebuild + integrity to settle.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs', 'dictionary')
REBUILD = os.path.join(ROOT, 'rebuild-dictionary.py')
BYTOPIC = os.path.join(ROOT, 'bin', 'build_by_topic.py')

EXISTING = {f[:-5] for f in os.listdir(DICT) if f.endswith('.html')}
REDIR = set()
_r = os.path.join(ROOT, 'data', 'dictionary-redirects.txt')
if os.path.exists(_r):
    REDIR = {l.split('->')[0].strip() for l in open(_r) if '->' in l}

# A curated list of classic culture-war words the world has redefined.
CULTURE_WORDS = [
    'tolerance', 'justice', 'love', 'gender', 'marriage', 'freedom', 'liberty',
    'equality', 'pride', 'identity', 'truth', 'judgment', 'hate', 'bigotry',
    'phobia', 'diversity', 'inclusion', 'equity', 'rights', 'choice', 'consent',
    'progress', 'science', 'health', 'safety', 'harm', 'violence', 'justice-doctrine',
    'compassion', 'kindness', 'authenticity', 'empathy', 'spirituality', 'sin',
    'shame', 'guilt', 'conscience', 'virtue', 'tribe', 'family', 'woman', 'man',
]


def word_of(slug):
    p = os.path.join(DICT, slug + '.html')
    if os.path.exists(p):
        m = re.search(r'<div class="word-title">([^<]+)</div>', open(p, encoding='utf-8').read())
        if m:
            return m.group(1).strip()
    return slug.replace('-', ' ').title()


def pos_of(slug):
    p = os.path.join(DICT, slug + '.html')
    if os.path.exists(p):
        m = re.search(r'<span class="pos">([^<]+)</span>', open(p, encoding='utf-8').read())
        if m:
            return m.group(1).strip()
    return 'word'


def bytopic_categories():
    src = open(BYTOPIC, encoding='utf-8').read()
    cats = re.findall(r'\(\s*"([a-z-]+)",\s*"([^"]+)",\s*"[^"]*",\s*\[(.*?)\]\s*,?\s*\)', src, re.DOTALL)
    out = {}
    for anchor, title, body in cats:
        out[anchor] = (re.sub('&amp;', '&', title), re.findall(r'"([a-z0-9-]+)"', body))
    return out


def live(slug):
    return slug in EXISTING and slug not in REDIR


def doctrinal_anchors_cards():
    cats = bytopic_categories()
    order = ['theology-proper', 'christology', 'soteriology',
             'ecclesiology-sacraments', 'eschatology']
    seen, cards = set(), []
    for anchor in order:
        title, slugs = cats.get(anchor, ('', []))
        for s in slugs:
            if live(s) and s not in seen:
                seen.add(s)
                cards.append((s, word_of(s), title))
    return cards[:100]


def most_corrupted_cards():
    cats = bytopic_categories()
    seen, cards = set(), []
    # 1) keep the section's existing curated picks
    blk = section_block('most-corrupted')
    if blk:
        for s in re.findall(r'href="([a-z0-9-]+)\.html" class="corrupted-card"', blk):
            if live(s) and s not in seen:
                seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    # 2) the corruption-correctors frameworks
    for s in cats.get('corruption-correctors', ('', []))[1]:
        if live(s) and s not in seen:
            seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    # 3) curated culture-war words
    for s in CULTURE_WORDS:
        if live(s) and s not in seen:
            seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    return cards[:100]


def _seed_from_existing(slug, card_class):
    out = []
    blk = section_block(slug)
    if blk:
        for s in re.findall(rf'href="([a-z0-9-]+)\.html" class="{card_class}"', blk):
            if live(s):
                out.append(s)
    return out


# Vetted slug-substring cues — an entry qualifies if its slug contains a cue
# (kept tight to avoid false positives; review the dry-run before --apply).
ORDER_CUES = ('headship', 'submission', 'helpmeet', 'helpmate', 'patriarch',
              'complementar', 'manhood', 'womanhood', 'husband', 'wife', 'wives',
              'father', 'household', 'family-order', 'biblical-order', 'biblical-man',
              'biblical-woman', 'biblical-fraternity', 'authority', 'elder-qual',
              'deacon', 'masculin', 'feminin', 'marriage', 'betroth', 'dowry',
              'firstborn', 'birthright', 'inheritance-doctrine', 'levirate')
PROHIBITED_CUES = ('adultery', 'fornication', 'idolatry', 'idol', 'sorcery',
                   'witchcraft', 'divination', 'necromancy', 'sodom', 'bestiality',
                   'incest', 'drunkenness', 'gluttony', 'covetousness', 'blasphemy',
                   'abomination', 'whoredom', 'harlot', 'usury', 'child-sacrifice',
                   'molech', 'graven-image', 'false-witness', 'murder', 'occult',
                   'wizard', 'familiar-spirit', 'effeminate', 'unnatural',
                   'profane', 'sabbath-breaking', 'oppression-of', 'man-stealing')


def _cue_cards(slug, card_class, cues, anthro_cat=None):
    seen, cards = set(), []
    for s in _seed_from_existing(slug, card_class):           # keep current picks
        if s not in seen:
            seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    if anthro_cat:                                            # add a vetted by-topic category
        for s in bytopic_categories().get(anthro_cat, ('', []))[1]:
            if live(s) and s not in seen:
                seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    for fn in sorted(os.listdir(DICT)):                       # slug-cue matches
        if not fn.endswith('.html'):
            continue
        s = fn[:-5]
        if s in seen or not live(s):
            continue
        if any(c in s for c in cues):
            seen.add(s); cards.append((s, word_of(s), pos_of(s)))
    return cards[:100]


def biblical_order_cards():
    return _cue_cards('biblical-order', 'order-card', ORDER_CUES, 'anthropology-order')


def expressly_prohibited_cards():
    return _cue_cards('expressly-prohibited', 'forbidden-card', PROHIBITED_CUES)


SECTIONS = {
    'doctrinal-anchors': dict(card='featured-card', word='fword', tag='ftag',
                              builder=doctrinal_anchors_cards),
    'most-corrupted': dict(card='corrupted-card', word='cword', tag='ctag',
                           builder=most_corrupted_cards),
    'biblical-order': dict(card='order-card', word='oword', tag='otag',
                           builder=biblical_order_cards),
    'expressly-prohibited': dict(card='forbidden-card', word='pword', tag='ptag',
                                 builder=expressly_prohibited_cards),
}


def section_block(slug):
    """Return the current <div ...-section> block in rebuild-dictionary.py whose
    h3 links to <slug>.html, else ''."""
    src = open(REBUILD, encoding='utf-8').read()
    h = src.find(f'href="{slug}.html" class="section-title-link"')
    if h < 0:
        return ''
    start = src.rfind('<div class="', 0, h)
    m = re.search(r'\n\n        <div class="|\n\n        <!--|\n\n    </div><!-- /\.container -->',
                  src[h:])
    end = (h + m.start()) if m else len(src)
    return src[start:end]


def rebuild_block(slug, cfg, cards):
    old = section_block(slug)
    if not old:
        return None
    h3 = re.search(r'(<h3>.*?</h3>)', old, re.DOTALL).group(1)
    sub = re.search(r'(<p class="subtitle">.*?</p>)', old, re.DOTALL)
    sub = sub.group(1) if sub else ''
    wrapper = re.match(r'<div class="([a-z-]+-section)"[^>]*>', old).group(0)

    def card(slug_, word, tag):
        return (f'<a href="{slug_}.html" class="{cfg["card"]}">'
                f'<div class="{cfg["word"]}">{word}</div>'
                f'<div class="{cfg["tag"]}">{tag}</div></a>')

    vis = '\n'.join('                ' + card(*c) for c in cards[:12])
    more = '\n'.join('                    ' + card(*c) for c in cards[12:])
    grid = cfg['card'].replace('-card', '-grid')
    block = (f'{wrapper}\n            {h3}\n            {sub}\n'
             f'            <div class="{grid}">\n{vis}\n            </div>\n'
             f'            <details>\n                <summary><em>expand to see all {len(cards)}</em></summary>\n'
             f'                <div class="{grid} more-grid">\n{more}\n                </div>\n'
             f'            </details>\n        </div>')
    return old, block


def dedup_by_word(cards):
    """Drop cards whose display word already appeared (avoids twin titles like
    two 'Abomination of Desolation' — those are merge candidates, not two cards)."""
    seen, out = set(), []
    for c in cards:
        key = c[1].lower()
        if key not in seen:
            seen.add(key); out.append(c)
    return out


def main():
    apply = '--apply' in sys.argv
    src = open(REBUILD, encoding='utf-8').read()
    for slug, cfg in SECTIONS.items():
        cards = dedup_by_word(cfg['builder']())
        print(f'\n{slug}: {len(cards)} cards')
        print('  ', ', '.join(w for _, w, _ in cards[:12]), '...')
        if apply:
            res = rebuild_block(slug, cfg, cards)
            if res:
                old, new = res
                src = src.replace(old, new, 1)
    if apply:
        open(REBUILD, 'w', encoding='utf-8').write(src)
        print('\napplied — now run rebuild + integrity.')
    else:
        print('\n(dry run — re-run with --apply)')


if __name__ == '__main__':
    main()
