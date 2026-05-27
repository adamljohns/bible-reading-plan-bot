#!/usr/bin/env python3
"""build_baby_names.py — generate docs/dictionary/baby-names.html

A curated, browseable baby-name directory split off from the broader
biblical-names index. Categorizes by male / female / unisex (place-names
that work for both, biblical figures whose names cross gender lines).

Each name shows:
  * Headword (linked to the full dictionary entry)
  * One-line meaning / origin
  * Source category

The curated mapping below is hand-maintained — biblical baby-naming is
high-touch and benefits from editorial curation more than automated
inference. To add a name: append to the appropriate list with
(slug, short_meaning).
"""
import os
import re
import html as html_mod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
OUT = os.path.join(DICT_DIR, 'baby-names.html')

WORD_TITLE_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
H1_TITLE_PAT = re.compile(r'<h1[^>]*class="[^"]*word-title[^"]*"[^>]*>(.*?)</h1>', re.DOTALL)
BARE_H1_PAT = re.compile(r'<body[^>]*>.*?<h1[^>]*>(.*?)</h1>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')


def get_headword(slug):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return None
    with open(fp, 'r', encoding='utf-8') as f:
        h = f.read()
    for pat in (WORD_TITLE_PAT, H1_TITLE_PAT, BARE_H1_PAT):
        m = pat.search(h)
        if m:
            t = TAG_STRIP.sub('', m.group(1))
            t = t.replace('&mdash;', '—').replace('&amp;', '&').replace('&#39;', "'")
            t = re.sub(r'\s+', ' ', t).strip()
            # Strip "(Doctrinal)" / "(Figure)" / "(Mother of John)" parenthetical
            t = re.sub(r'\s*\([^)]*\)\s*$', '', t)
            return t
    return None


# Hand-curated mapping: (slug, short_meaning)
MALE = [
    ('aaron',           'mountain of strength; the first high priest'),
    ('abel',            'breath, vapor; the first martyr (Gen 4)'),
    ('abraham',         'father of many nations; the friend of God'),
    ('adam',            'man, earth; the first human'),
    ('andrew',          'manly, courageous; brought Peter to Jesus'),
    ('barnabas-doctrine', 'son of encouragement; companion of Paul'),
    ('boaz-doctrine',   'swift, strong; kinsman-redeemer of Ruth'),
    ('caleb-doctrine',  'whole-hearted; one of two faithful spies'),
    ('daniel',          'God is my judge; the prophet in exile'),
    ('david',           'beloved; king after God\'s own heart'),
    ('elijah',          'my God is Yahweh; great prophet of Mount Carmel'),
    ('elisha',          'God is salvation; successor of Elijah'),
    ('enoch',           'dedicated; walked with God, was not (Gen 5:24)'),
    ('ezekiel',         'God will strengthen; the prophet of the exile'),
    ('ezra',            'help; the priest-scribe of the return'),
    ('gabriel',         'man of God; the announcing angel'),
    ('gideon',          'mighty warrior; judge of three hundred'),
    ('hosea',           'salvation; prophet of God\'s covenant love'),
    ('isaac',           'laughter; son of promise to Abraham'),
    ('isaiah',          'the LORD is salvation; the messianic prophet'),
    ('jacob',           'supplanter; renamed Israel; the patriarch'),
    ('james-apostle',   'supplanter (Greek for Jacob); apostle and brother of John'),
    ('jeremiah',        'the LORD exalts; the weeping prophet'),
    ('john-the-baptist', 'Yahweh is gracious; the forerunner of Christ'),
    ('jonah',           'dove; the reluctant prophet'),
    ('jonathan',        'gift of Yahweh; David\'s covenant friend'),
    ('joseph',          'he will add; the dreamer-savior of Egypt'),
    ('joshua-figure',   'Yahweh is salvation; led Israel into the land'),
    ('josiah',          'the LORD heals; the boy-king of reform'),
    ('judah',           'praised; the tribe through which Messiah came'),
    ('luke',            'light; physician and evangelist'),
    ('malachi',         'my messenger; last prophet of the OT'),
    ('mark-book',       'warrior (Latin); the second evangelist'),
    ('matthew-apostle', 'gift of God; tax collector turned apostle'),
    ('micah',           'who is like God; the prophet of Bethlehem'),
    ('moses',           'drawn out; the lawgiver and deliverer'),
    ('nathan-prophet',  'he gave; David\'s prophet'),
    ('nathanael',       'gift of God; \'in whom is no guile\' (John 1:47)'),
    ('nehemiah',        'the LORD comforts; wall-builder of Jerusalem'),
    ('noah',            'rest; the ark-builder'),
    ('paul',            'small; apostle to the Gentiles'),
    ('peter',           'rock; chief apostle, fisherman'),
    ('philip',          'lover of horses; apostle and evangelist'),
    ('samuel',          'heard by God; the last judge, the first prophet of kings'),
    ('saul',            'asked of God; the first king of Israel'),
    ('seth-son',        'appointed; son of Adam after Abel'),
    ('silas',           'woods, forest; Paul\'s missionary companion'),
    ('solomon',         'peace; David\'s wise son; temple-builder'),
    ('stephen',         'crown; the first Christian martyr'),
    ('thomas',          'twin; the doubting-then-believing apostle'),
    ('timothy',         'honored by God; Paul\'s son in the faith'),
    ('titus-doctrine',  'honored; Paul\'s Gentile companion'),
    ('zacharias-prophet', 'Yahweh remembers; father of John the Baptist'),
    # Editor's family
    ('malachi-andrew',  'memorial — Adam & Maria\'s first child (2017)'),
]

FEMALE = [
    ('abigail',         'father is joy; David\'s wife of wisdom'),
    ('anna-the-prophetess', 'grace; the temple-prophetess at Christ\'s presentation'),
    ('bathsheba',       'daughter of the oath; mother of Solomon'),
    ('bethany',         'house of figs; the village of Lazarus, Mary, Martha'),
    ('deborah',         'bee; prophetess and judge'),
    ('elisabeth-mother-of-john', 'God is my oath; mother of John the Baptist'),
    ('esther',          'star; queen who saved her people'),
    ('hannah',          'grace; the long-barren mother of Samuel'),
    ('joanna',          'Yahweh is gracious; faithful woman at the resurrection'),
    ('leah',            'weary; Jacob\'s first wife; mother of Judah'),
    ('lydia',           'woman from Lydia; first European convert (Acts 16)'),
    ('martha',          'lady, mistress; sister of Mary and Lazarus'),
    ('mary',            'bitter, beloved; mother of Christ'),
    ('miriam',          'bitter; prophetess, sister of Moses and Aaron'),
    ('naomi',           'pleasant; Ruth\'s mother-in-law'),
    ('phoebe',          'radiant; deacon of Cenchrea (Rom 16:1)'),
    ('priscilla-and-aquila', 'ancient; co-worker with Paul (with husband Aquila)'),
    ('rachel',          'ewe; Jacob\'s beloved wife; mother of Joseph and Benjamin'),
    ('rebekah',         'to bind; Isaac\'s wife; mother of Jacob and Esau'),
    ('ruth',            'companion, friend; the Moabite great-grandmother of David'),
    ('salome',          'peace; mother of James and John; at the resurrection'),
    ('sarah',           'princess; Abraham\'s wife; mother of nations'),
    ('tabitha',         'gazelle (also Dorcas in Greek); raised by Peter (Acts 9)'),
    ('tamar',           'palm tree; mother in the line of Christ (Matt 1:3)'),
    # Editor's family
    ('maria',           'the Latin form of Mary; the editor\'s wife — bitter made sweet'),
    ('hope-twin',       'memorial — Adam & Maria\'s twin daughter (2018)'),
    ('mercy-twin',      'memorial — Adam & Maria\'s twin daughter (2018)'),
]

UNISEX = [
    ('shiloh-doctrine', 'he whose right it is (Gen 49:10); Messianic title + place-name; modern unisex use'),
    ('jordan-river',    'descend, flow down; the river of baptism; modern unisex'),
    ('eden',            'delight, pleasure; the garden of original creation; modern unisex'),
    ('carmel',          'vineyard, garden; the mountain where Elijah called down fire; rare modern use'),
    ('zion',            'fortification, parched place; God\'s holy hill; modern unisex use'),
]


def render_card(slug, meaning, headword):
    safe_h = html_mod.escape(headword or slug)
    safe_m = html_mod.escape(meaning)
    return (
        f'<a class="name-card" href="{slug}.html">'
        f'<div class="name-word">{safe_h}</div>'
        f'<div class="name-meaning">{safe_m}</div>'
        f'</a>'
    )


def render_section(title, anchor, intro, names):
    cards = []
    skipped = 0
    for slug, meaning in names:
        hw = get_headword(slug)
        if hw is None:
            print(f'  WARN: no headword for {slug} (skipping)')
            skipped += 1
            continue
        cards.append(render_card(slug, meaning, hw))
    if not cards:
        return ''
    cards_html = '\n        '.join(cards)
    return f'''
    <section class="names-section" id="{anchor}">
        <h2>{title} <span class="count-badge-lg">{len(cards)}</span></h2>
        <p class="sec-intro">{intro}</p>
        <div class="names-grid">
        {cards_html}
        </div>
    </section>
    '''


def main():
    print('Building baby-names.html…')
    male_html = render_section(
        'Boy Names', 'boys',
        'Biblical names suited for boys — drawn from the patriarchs, prophets, judges, kings, and apostles. Click any name for the full dictionary entry.',
        MALE,
    )
    female_html = render_section(
        'Girl Names', 'girls',
        'Biblical names suited for girls — drawn from matriarchs, prophetesses, queens, and disciples. Click any name for the full dictionary entry.',
        FEMALE,
    )
    unisex_html = render_section(
        'Unisex Names', 'unisex',
        'Biblical place-names and concept-names that have crossed into modern use for both boys and girls — like Shiloh, Eden, Jordan, and Zion.',
        UNISEX,
    )

    total = len(MALE) + len(FEMALE) + len(UNISEX)

    html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/dictionary/baby-names.html">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baby Names from the Bible &mdash; The MOOP Dictionary</title>
    <meta name="description" content="Biblical baby names with Hebrew and Greek meaning — boys, girls, and unisex names from Scripture. Curated from The MOOP Dictionary.">
    <meta property="og:title" content="Biblical Baby Names &mdash; The MOOP Dictionary">
    <meta property="og:description" content="Boy, girl, and unisex names from the Bible with original-language meaning — for expecting parents and curious readers.">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1, h2, h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px; border-bottom:1px solid var(--border); position:sticky; top:0; background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.8rem; padding:3px 6px; border-radius:6px; }}
        nav a:hover, nav a.active {{ color:var(--gold); }}
        .container {{ max-width:1100px; margin:0 auto; padding:30px 20px 60px; }}
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .hero h1 {{ font-size:2.6rem; color:var(--gold-light); margin-bottom:12px; }}
        .hero .lead {{ color:var(--gray); max-width:640px; margin:10px auto; font-size:1rem; }}
        .hero .total {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; padding:4px 14px; border-radius:14px; font-size:0.85rem; margin-top:14px; }}
        .quick-nav {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:28px 0 10px; }}
        .quick-nav a {{ background:var(--card); border:1px solid var(--border); color:var(--white) !important; text-decoration:none; padding:8px 18px; border-radius:20px; font-size:0.9rem; }}
        .quick-nav a:hover {{ border-color:var(--gold); color:var(--gold) !important; }}
        .editor-note {{ background:rgba(212,175,55,0.05); border:1px solid var(--border); border-radius:10px; padding:18px 22px; margin:24px 0 0; font-size:0.92rem; }}
        .editor-note h3 {{ color:var(--gold); font-size:1rem; margin-bottom:6px; font-family:'Inter',sans-serif; font-weight:600; }}
        .names-section {{ margin:48px 0; scroll-margin-top:80px; }}
        .names-section h2 {{ color:var(--gold-light); font-size:1.7rem; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:8px; }}
        .sec-intro {{ color:var(--gray); font-size:0.92rem; margin-bottom:20px; max-width:720px; }}
        .count-badge-lg {{ display:inline-block; background:var(--gold); color:#000; font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:10px; margin-left:8px; vertical-align:middle; }}
        .names-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(240px, 1fr)); gap:12px; }}
        .name-card {{ display:block; background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 18px; text-decoration:none; color:var(--white) !important; transition:border-color 0.2s, transform 0.15s; }}
        .name-card:hover {{ border-color:var(--gold); transform:translateY(-1px); }}
        .name-word {{ font-family:'Playfair Display',serif; font-size:1.18rem; color:var(--gold-light); margin-bottom:5px; }}
        .name-meaning {{ font-size:0.83rem; color:var(--gray); line-height:1.5; }}
        footer {{ text-align:center; padding:32px 20px; border-top:1px solid var(--border); margin-top:50px; color:var(--gray); font-size:0.88rem; }}
        footer a {{ color:var(--gray); text-decoration:none; }}
        footer a:hover {{ color:var(--gold); }}
        body.light-mode {{ --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(245,243,239,0.97); }}
        body.light-mode .name-card,
        body.light-mode .quick-nav a,
        body.light-mode .editor-note {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode .editor-note {{ background:rgba(212,175,55,0.04); }}
        a, a:link, a:visited {{ color:var(--gold) !important; }}
        @media (max-width:560px) {{ .hero h1 {{ font-size:2rem; }} .names-grid {{ grid-template-columns:1fr; }} }}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">BTE</a>
        <a href="index.html" class="active">Dictionary</a>
        <a href="names.html">Biblical Names</a>
        <a href="baby-names.html" class="active">Baby Names</a>
        <a href="../blog.html">Blog</a>
    </nav>
    <div class="container">
        <div class="hero">
            <h1>Biblical Baby Names</h1>
            <p class="lead">Boy, girl, and unisex names drawn from Scripture &mdash; with Hebrew, Greek, and original-language meaning. Each name links to the full dictionary entry.</p>
            <span class="total">{total} curated names</span>
            <div class="quick-nav">
                <a href="#boys">Boys &#9662;</a>
                <a href="#girls">Girls &#9662;</a>
                <a href="#unisex">Unisex &#9662;</a>
                <a href="names.html">Full Names Index &rarr;</a>
            </div>
            <div class="editor-note">
                <h3>&#128153; A Note from the Editor</h3>
                <p>This baby-name directory is split off from the larger biblical-names index to serve expecting parents and curious readers. The page is curated by Adam Johns, editor of the MOOP Dictionary, and includes a small number of personal-family entries (Maria, Malachi Andrew, Hope, Mercy) representing his wife and three children lost too soon. Each name links to its full entry with original-language etymology.</p>
            </div>
        </div>

        {male_html}
        {female_html}
        {unisex_html}

        <section class="names-section">
            <h2>Looking for More?</h2>
            <p class="sec-intro">The full <a href="names.html">Biblical Names index</a> covers every name in the dictionary (not just those traditionally given as baby names). The full <a href="index.html">dictionary index</a> covers all 5,000+ entries across doctrine, persons, places, and Hebrew/Greek word studies.</p>
        </section>
    </div>
    <footer>
        <p>Baby Names from the Bible &middot; Part of <a href="index.html">The MOOP Dictionary</a> &middot; <a href="../bible.html">Bible Translation Engine</a></p>
        <p style="margin-top:8px;font-size:0.78rem;">&copy; 2026 U.S.M.C. Ministries</p>
    </footer>
</body>
</html>'''

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f'Wrote {OUT}')
    print(f'  Boys: {len(MALE)}')
    print(f'  Girls: {len(FEMALE)}')
    print(f'  Unisex: {len(UNISEX)}')
    print(f'  Total: {total}')


if __name__ == '__main__':
    main()
