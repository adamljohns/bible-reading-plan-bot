#!/usr/bin/env python3
"""enhance_entry_pages.py — presentation & navigation upgrades for every
dictionary entry page. Idempotent (marker-based); safe to re-run any time;
runs as a standard step of bin/batch_pipeline.sh so new entries get the
same treatment automatically.

Adds, per entry page:

  1. SECTION ANCHORS + JUMP ROW  — each major section (<div class="section">
     with a recognized <h3>) gets a stable id, and a small centered jump row
     is injected above the first section: Definition · Webster · Scriptures ·
     Corruption · Roots · Usage · In the Text · Related.

  2. "IN THE TEXT" CONCORDANCE   — the inverse of the chapter auto-linker:
     every Bible chapter page that links to this entry becomes a chip
     (canonical book order, capped, with overflow count), so the reader can
     jump from a word to the places it lives in the text.

  3. SAME-TITLE DISAMBIGUATION   — entries sharing a display title get a
     "See also" line under the header pointing at their namesakes
     (distinguished by part-of-speech), turning silent duplicates into
     navigation.

Usage:
  python3 bin/enhance_entry_pages.py            # apply
  python3 bin/enhance_entry_pages.py --dry-run
  python3 bin/enhance_entry_pages.py --quiet
"""
import argparse
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
CHAP_DIR = os.path.join(ROOT, 'docs', 'chapters')

SPECIAL = {'index', 'template', 'names', 'baby-names', 'by-topic',
           'doctrinal-anchors', 'biblical-order', 'expressly-prohibited',
           'most-corrupted', 'gen-z-decoded', 'millennial-decoded',
           'gen-x-decoded', 'boomer-decoded', 'changelog'}

# Canonical book order by chapter-file prefix.
BOOK_ORDER = ['gen', 'exo', 'lev', 'num', 'deu', 'jos', 'jdg', 'rut', '1sa',
              '2sa', '1ki', '2ki', '1ch', '2ch', 'ezr', 'neh', 'est', 'job',
              'psa', 'pro', 'ecc', 'sng', 'isa', 'jer', 'lam', 'eze', 'dan',
              'hos', 'joe', 'amo', 'oba', 'jon', 'mic', 'nah', 'hab', 'zep',
              'hag', 'zec', 'mal', 'mat', 'mar', 'luk', 'joh', 'act', 'rom',
              '1co', '2co', 'gal', 'eph', 'php', 'col', '1th', '2th', '1ti',
              '2ti', 'tit', 'phm', 'heb', 'jas', '1pe', '2pe', '1jn', '2jn',
              '3jn', 'jud', 'rev']
BOOK_RANK = {b: i for i, b in enumerate(BOOK_ORDER)}

JUMPS_MARK = '<!-- DICT-JUMPS -->'
DISAMBIG_MARK = '<!-- DICT-DISAMBIG -->'
ITT_START = '<!-- IN-THE-TEXT-START -->'
ITT_END = '<!-- IN-THE-TEXT-END -->'

SECTION_H3 = re.compile(r'(<div class="section[^"]*")(\s*>\s*<h3[^>]*>)(.*?)(</h3>)',
                        re.DOTALL)
TITLE_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
POS_PAT = re.compile(r'<div class="pos">(.*?)</div>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')

H3_TO_ANCHOR = [
    ('biblical definition', 'definition', 'Definition'),
    ('webster', 'webster', 'Webster 1828'),
    ('key scripture', 'scriptures', 'Scriptures'),
    ('modern corruption', 'corruption', 'Corruption'),
    ('greek', 'roots', 'Roots'),
    ('hebrew', 'roots', 'Roots'),
    ('roots', 'roots', 'Roots'),
    ('proto', 'roots', 'Roots'),
    ('usage', 'usage', 'Usage'),
    ('in the text', 'in-the-text', 'In the Text'),
    ('related', 'related', 'Related'),
]


def book_names():
    """Derive display name per chapter-file prefix from one chapter title."""
    names = {}
    for fn in sorted(os.listdir(CHAP_DIR)):
        m = re.match(r'([0-9a-z]{3})-(\d+)\.html$', fn)
        if not m or m.group(1) in names:
            continue
        try:
            h = open(os.path.join(CHAP_DIR, fn), encoding='utf-8',
                     errors='ignore').read(4000)
        except OSError:
            continue
        t = re.search(r'<title>(.*?)</title>', h, re.DOTALL)
        if t:
            tm = re.match(r'\s*(.+?)\s+\d+\b', TAG_STRIP.sub('', t.group(1)))
            if tm:
                names[m.group(1)] = tm.group(1).strip()
    return names


def chapter_backlinks():
    """slug -> sorted list of (rank, chapter_int, prefix, chap_file)."""
    inv = defaultdict(set)
    pat = re.compile(r'href="\.\./dictionary/([a-z0-9-]+)\.html"')
    for fn in os.listdir(CHAP_DIR):
        m = re.match(r'([0-9a-z]{3})-(\d+)\.html$', fn)
        if not m:
            continue
        h = open(os.path.join(CHAP_DIR, fn), encoding='utf-8',
                 errors='ignore').read()
        for slug in set(pat.findall(h)):
            inv[slug].add((BOOK_RANK.get(m.group(1), 99), int(m.group(2)),
                           m.group(1), fn))
    return {s: sorted(v) for s, v in inv.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--cap', type=int, default=14,
                    help='max In-the-Text chips per entry')
    args = ap.parse_args()

    names = book_names()
    inv = chapter_backlinks()

    # Pass 1: collect display titles for disambiguation.
    titles = defaultdict(list)   # title-lower -> [(slug, pos)]
    pages = []
    for fn in sorted(os.listdir(DICT_DIR)):
        if not fn.endswith('.html'):
            continue
        slug = fn[:-5]
        if slug in SPECIAL:
            continue
        pages.append(slug)
        h = open(os.path.join(DICT_DIR, fn), encoding='utf-8',
                 errors='ignore').read()
        tm = TITLE_PAT.search(h)
        pm = POS_PAT.search(h)
        if tm:
            t = TAG_STRIP.sub('', tm.group(1)).strip()
            pos = TAG_STRIP.sub('', pm.group(1)).strip() if pm else ''
            titles[t.lower()].append((slug, t, pos))

    dupes = {t: lst for t, lst in titles.items() if len(lst) > 1}

    stats = {'jumps': 0, 'ids': 0, 'itt': 0, 'disambig': 0, 'files': 0}
    for slug in pages:
        fp = os.path.join(DICT_DIR, slug + '.html')
        h = open(fp, encoding='utf-8', errors='ignore').read()
        orig = h

        # --- strip any previous injections (idempotency) ---
        h = re.sub(re.escape(ITT_START) + r'.*?' + re.escape(ITT_END), '',
                   h, flags=re.DOTALL)
        h = re.sub(JUMPS_MARK + r'.*?' + JUMPS_MARK, '', h, flags=re.DOTALL)
        h = re.sub(DISAMBIG_MARK + r'.*?' + DISAMBIG_MARK, '', h,
                   flags=re.DOTALL)

        # --- 1. section ids + collect available anchors ---
        present = []          # (order, anchor, label)
        seen_anchor = set()

        def add_id(m):
            head, gap, h3text, close = m.groups()
            plain = TAG_STRIP.sub('', h3text).lower()
            for key, anchor, label in H3_TO_ANCHOR:
                if key in plain:
                    if anchor not in seen_anchor:
                        seen_anchor.add(anchor)
                        present.append((anchor, label))
                    if 'id=' not in head:
                        head = head + f' id="{anchor}"'
                    break
            return head + gap + h3text + close

        h = SECTION_H3.sub(add_id, h)
        # related block: ensure its enclosing div is reachable
        if '<div class="related">' in h and 'related' not in seen_anchor:
            present.append(('related', 'Related'))

        # --- 2. In the Text section ---
        chaps = inv.get(slug, [])
        itt_html = ''
        if chaps:
            chips = []
            for rank, cnum, pref, cf in chaps[:args.cap]:
                book = names.get(pref, pref.upper())
                chips.append(f'<a href="../chapters/{cf}">{book} {cnum}</a>')
            more = ''
            if len(chaps) > args.cap:
                more = (f'<p class="section-summary" style="margin-top:8px;">'
                        f'&hellip;and {len(chaps) - args.cap} more chapters.</p>')
            itt_html = (
                f'\n        {ITT_START}\n'
                f'        <div class="section" id="in-the-text">\n'
                f'            <h3><img src="../assets/icons/shield-open-book-48.png" alt="" width="20" height="20" style="vertical-align:-4px;"> In the Text</h3>\n'
                f'            <p class="section-summary">Chapters of the reading Bible where this entry is linked.</p>\n'
                f'            <div class="related in-text-chips">{"".join(chips)}</div>\n'
                f'            {more}\n'
                f'        </div>\n'
                f'        {ITT_END}\n')
            if ('in-the-text', 'In the Text') not in present:
                present.append(('in-the-text', 'In the Text'))

        # insertion point: before the section that contains the related chips,
        # else before the footer.
        if itt_html:
            ridx = h.find('<div class="related">')
            ins = h.rfind('<div class="section"', 0, ridx) if ridx != -1 else -1
            if ins == -1:
                ins = h.find('<footer')
            if ins != -1:
                h = h[:ins] + itt_html + '        ' + h[ins:]
                stats['itt'] += 1

        # --- 3. jump row (only if 3+ sections to jump between) ---
        if len(present) >= 3:
            order = {'definition': 0, 'webster': 1, 'scriptures': 2,
                     'corruption': 3, 'roots': 4, 'usage': 5,
                     'in-the-text': 6, 'related': 7}
            present_sorted = sorted(set(present), key=lambda x: order.get(x[0], 9))
            links = ' &middot; '.join(
                f'<a href="#{a}" style="color:var(--gold);text-decoration:none;">{l}</a>'
                for a, l in present_sorted)
            jump = (f'\n        {JUMPS_MARK}<p class="section-summary" '
                    f'style="text-align:center;margin:2px 0 10px;">{links}</p>'
                    f'{JUMPS_MARK}\n')
            first_sec = h.find('<div class="section')
            if first_sec != -1:
                h = h[:first_sec] + jump + '        ' + h[first_sec:]
                stats['jumps'] += 1

        # --- 4. disambiguation ---
        tm = TITLE_PAT.search(h)
        if tm:
            t = TAG_STRIP.sub('', tm.group(1)).strip().lower()
            if t in dupes:
                others = [(s, disp, pos) for s, disp, pos in dupes[t]
                          if s != slug]
                if others:
                    parts = []
                    for s, disp, pos in others:
                        tag = f' <span style="color:var(--gray);">({pos})</span>' if pos else ''
                        parts.append(f'<a href="{s}.html" style="color:var(--gold);">{disp}</a>{tag}')
                    line = (f'\n        {DISAMBIG_MARK}<p class="section-summary" '
                            f'style="text-align:center;margin:0 0 8px;">See also: '
                            + ' &middot; '.join(parts) + f'</p>{DISAMBIG_MARK}\n')
                    first_sec = h.find(JUMPS_MARK)
                    if first_sec == -1:
                        first_sec = h.find('<div class="section')
                    if first_sec != -1:
                        h = h[:first_sec] + line + '        ' + h[first_sec:]
                        stats['disambig'] += 1

        if h != orig:
            stats['files'] += 1
            if not args.dry_run:
                open(fp, 'w', encoding='utf-8').write(h)

    print(f'{"DRY-RUN — " if args.dry_run else ""}entry enhancement complete.')
    print(f'  files changed:        {stats["files"]}/{len(pages)}')
    print(f'  jump rows injected:   {stats["jumps"]}')
    print(f'  In-the-Text sections: {stats["itt"]}')
    print(f'  disambiguation notes: {stats["disambig"]}')


if __name__ == '__main__':
    main()
