#!/usr/bin/env python3
"""scaffold_new_corpora.py — stand up the page skeletons for two new works
Adam asked for on 2026-08-06:

  * Augustine's *Confessions*  (requested for his nephew Sandon)
  * The Baptist Faith & Message, 1925 / 1963 / 2000 side by side, so the
    evolution 1689 -> 1925 -> 1963 -> 2000 is visible with the LBCF already
    on the site.

SCAFFOLD ONLY. Every page is created with its structure, navigation and
house shell in place and its body marked TODO. No source text is written and
no content is invented — the fill is a separate, sourced pass.

The house shell (head, nav, footer) is lifted at runtime from a reference
Institutes page, so these cannot drift from the corpus they join.

Usage:
  python3 bin/scaffold_new_corpora.py            # dry run
  python3 bin/scaffold_new_corpora.py --apply
"""
import os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
APPLY = '--apply' in sys.argv
REF = 'docs/institutes/b1-c01.html'

ref = open(REF, encoding='utf-8').read()
HEAD = ref[:ref.find('</head>')]
NAV = re.search(r'<nav.*?</nav>', ref, re.S).group(0)
FOOT = re.search(r'<footer.*?</footer>', ref, re.S).group(0)

# ── Confessions ────────────────────────────────────────────────────────────
# 13 books. The Pusey translation (Gutenberg #3296, public domain) is
# continuous prose per book with NO chapter divisions — verified, not assumed.
# Chapter-level subdivision would need the Pilkington/NPNF text instead, which
# is also public domain but a different edition. Scaffolded at BOOK level;
# that decision is Adam's to confirm before the fill.
CONF = [
 (1,  "Infancy and Boyhood",            "Birth to his fifteenth year; the invocation of God."),
 (2,  "Sixteenth Year — The Stolen Pears","Idleness, lust, and the theft he could not explain."),
 (3,  "Carthage and the Manichees",     "Seventeen to nineteen; rhetoric, spectacle, and error."),
 (4,  "Nine Years Astray",              "Nineteen to twenty-eight; astrology, grief, and a lost friend."),
 (5,  "Rome, Milan, Ambrose",           "His twenty-ninth year; Faustus disappoints, Ambrose arrests."),
 (6,  "Thirtieth Year — Doctrine Opens","Ambrose's preaching; Monica arrives; ambition weighs."),
 (7,  "The Platonists and the Word",    "Thirty-first year; evil, substance, and the Incarnation."),
 (8,  "Tolle Lege — The Conversion",    "Thirty-second year; the garden, the voice, the epistle."),
 (9,  "Baptism and Monica's Death",     "Leaving rhetoric; Ostia; the death of his mother."),
 (10, "Memory and Temptation",          "What he still is; the vast fields of memory."),
 (11, "Time and Creation",              "Genesis 1:1; what time is, and what it is not."),
 (12, "Heaven and Earth",               "Formless matter; the many true readings of Moses."),
 (13, "The Trinity in Creation",        "Allegory of the six days; rest that has no evening."),
]

# ── Baptist Faith & Message ────────────────────────────────────────────────
# 18 articles, confirmed against the official SBC comparison chart which
# carries 1925, 1963 and 2000 in parallel columns.
BFM = [
 "The Scriptures", "God", "Man", "Salvation", "God's Purpose of Grace",
 "The Church", "Baptism and the Lord's Supper", "The Lord's Day",
 "The Kingdom", "Last Things", "Evangelism and Missions", "Education",
 "Stewardship", "Cooperation", "The Christian and the Social Order",
 "Peace and War", "Religious Liberty", "The Family",
]

def page(title, eyebrow, h1, subtitle, body, prev, nxt, up, uptxt):
    nav = []
    if prev: nav.append(f'<a href="{prev[0]}">&larr; {html.escape(prev[1])}</a>')
    nav.append(f'<a href="{up}">{html.escape(uptxt)}</a>')
    if nxt: nav.append(f'<a href="{nxt[0]}">{html.escape(nxt[1])} &rarr;</a>')
    return (HEAD.replace('<title>' + re.search(r'<title>(.*?)</title>', HEAD, re.S).group(1) + '</title>',
                         f'<title>{html.escape(title)}</title>')
            + '</head>\n<body>\n' + NAV + '\n<div class="container">\n'
            + f'  <div class="inst-chap-eyebrow">{html.escape(eyebrow)}</div>\n'
            + f'  <h1>{html.escape(h1)}</h1>\n'
            + f'  <p class="inst-subtitle"><em>{html.escape(subtitle)}</em></p>\n'
            + '  <div class="inst-body">\n' + body + '\n  </div>\n'
            + '  <div class="inst-chap-nav">' + ' '.join(nav) + '</div>\n'
            + '</div>\n' + FOOT + '\n</body>\n</html>\n')

TODO = ('    <!-- SCAFFOLD: body intentionally empty. Fill from the sourced\n'
        '         public-domain text, then add the "A Word for 2026" application\n'
        '         block in the house pattern. Do not invent content. -->\n'
        '    <p class="inst-todo"><em>Text pending — this page is scaffolding.</em></p>')

made = []

# Confessions pages
for i, (n, t, sub) in enumerate(CONF):
    prev = (f'book-{CONF[i-1][0]:02d}.html', f'Book {CONF[i-1][0]}') if i else None
    nxt  = (f'book-{CONF[i+1][0]:02d}.html', f'Book {CONF[i+1][0]}') if i < len(CONF)-1 else None
    p = f'docs/confessions/book-{n:02d}.html'
    made.append((p, page(f'Confessions {n}: {t} — Augustine (Pusey)',
                         f'Book {n} of 13 · USMC modern English',
                         t, sub, TODO, prev, nxt, 'index.html', 'All 13 Books')))

conf_idx = '\n'.join(
    f'    <li><a href="book-{n:02d}.html"><strong>Book {n}</strong> — {html.escape(t)}</a>'
    f'<br><span class="inst-sub">{html.escape(s)}</span></li>' for n, t, s in CONF)
made.append(('docs/confessions/index.html',
             page('The Confessions of Augustine — U.S.M.C. Ministries',
                  'Augustine of Hippo · c. AD 397–400',
                  'The Confessions',
                  'Thirteen books of prayer, memory and argument — read as one man talking to God.',
                  f'    <ol class="inst-toc">\n{conf_idx}\n    </ol>', None, None,
                  '../index.html', 'Home')))

# BF&M pages
for i, art in enumerate(BFM, start=1):
    prev = (f'article-{i-1:02d}.html', f'Article {i-1}') if i > 1 else None
    nxt  = (f'article-{i+1:02d}.html', f'Article {i+1}') if i < len(BFM) else None
    body = ('    <!-- SCAFFOLD: three columns, one per revision. Fill each from the\n'
            '         official SBC comparison chart. Where an article did not exist in a\n'
            '         given year, say so plainly rather than leaving it blank. -->\n'
            '    <div class="bfm-cols">\n'
            + '\n'.join(f'      <section class="bfm-col" data-year="{y}"><h2>{y}</h2>'
                        f'<p><em>Text pending — scaffolding.</em></p></section>'
                        for y in (1925, 1963, 2000))
            + '\n    </div>')
    made.append((f'docs/bfm/article-{i:02d}.html',
                 page(f'BF&M Article {i}: {art} — 1925 / 1963 / 2000',
                      f'Article {i} of 18 · 1925 · 1963 · 2000',
                      art, 'How Southern Baptists stated it, and how the statement changed.',
                      body, prev, nxt, 'index.html', 'All 18 Articles')))

bfm_idx = '\n'.join(
    f'    <li><a href="article-{i:02d}.html"><strong>Article {i}</strong> — {html.escape(a)}</a></li>'
    for i, a in enumerate(BFM, start=1))
made.append(('docs/bfm/index.html',
             page('The Baptist Faith & Message — 1925 · 1963 · 2000',
                  'Southern Baptist Convention',
                  'The Baptist Faith & Message',
                  'Eighteen articles, three revisions, side by side — with the 1689 Confession already on this site, the whole arc from 1689 to 2000.',
                  f'    <ol class="inst-toc">\n{bfm_idx}\n    </ol>', None, None,
                  '../index.html', 'Home')))

for p, _ in made:
    os.makedirs(os.path.dirname(p), exist_ok=True)
print(f'{"writing" if APPLY else "would write"} {len(made)} pages:')
print(f'  docs/confessions/  {len(CONF)} books + index')
print(f'  docs/bfm/          {len(BFM)} articles + index')
if APPLY:
    for p, c in made:
        open(p, 'w', encoding='utf-8').write(c)
    print('done.')
else:
    print('\n--dry-run: nothing written.')
