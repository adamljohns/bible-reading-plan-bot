#!/usr/bin/env python3
"""Build docs/dictionary/names.html — a names-only sub-page of the MOOP Dictionary.

Scans docs/dictionary/*.html (skipping index.html, template.html, names.html),
extracts each entry's <h1> and .pos field, filters to proper-noun entries
(plus "Bible book" entries), categorizes them into:

    People · Places · Books of the Bible · Tribes & Nations · Other

and writes a single names.html that mirrors the visual style of index.html.

Usage:
    python3 bin/build_names_index.py
"""

import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
NAMES_FILE = os.path.join(DICT_DIR, 'names.html')

SKIP = {'index.html', 'template.html', 'names.html'}

# Category id, label, emoji-prefixed label, intro line
CATEGORIES = [
    ('people',  'People',             '🧍 People',
        'Patriarchs, prophets, kings, apostles, women of faith, and named figures throughout Scripture.'),
    ('places',  'Places',             '🗺️ Places',
        'Cities, towns, mountains, regions, islands, and bodies of water named in the Bible.'),
    ('books',   'Books of the Bible', '📖 Books of the Bible',
        'The 66 canonical books plus named sections (Pentateuch, Gospels, etc.).'),
    ('tribes',  'Tribes & Nations',   '⚔️ Tribes & Nations',
        'Tribes of Israel, surrounding nations, and named people-groups.'),
    ('divine',  'Divine Names & Christ Titles', '✝️ Divine Names & Christ Titles',
        'Names of God revealed in Scripture — YHWH-compounds, El-titles, and Messianic / Christ-titles.'),
    ('other',   'Other Proper Nouns', '✨ Other',
        'Proper nouns that don’t fall into the categories above — feasts, armor, events, miscellaneous.'),
]

# Curated list of bare-"proper noun" entries that are actually places.
# These are biblical place-names that don't carry a -city / -region / -mount
# suffix in their slug, so they would default to "people" without this list.
KNOWN_PLACE_SLUGS = {
    # Cities
    'antioch', 'athens', 'babylon', 'beersheba', 'bethany', 'bethel',
    'bethlehem', 'capernaum', 'colosse', 'corinth', 'damascus', 'ephesus',
    'galilee', 'gilgal', 'gomorrah', 'hebron', 'jericho', 'jerusalem',
    'joppa', 'judea', 'mizpah', 'nazareth', 'nineveh', 'nob', 'philippi',
    'rome', 'samaria', 'shechem', 'shiloh', 'shunem', 'sodom', 'tarsus',
    'thessalonica', 'troas', 'tyre', 'sidon', 'thyatira', 'sardis',
    'pergamum', 'pergamos', 'smyrna', 'laodicea', 'colosse', 'iconium',
    'lystra', 'derbe', 'cana', 'caesarea', 'gath', 'gaza', 'kadesh',
    'jezreel', 'megiddo', 'penuel', 'peniel', 'ramah', 'ziklag', 'aijalon',
    # Mountains / hills (not -mount-prefixed)
    'carmel', 'gerizim', 'horeb', 'olivet', 'sinai', 'tabor', 'zion',
    'moriah', 'ebal', 'gilboa', 'pisgah', 'nebo',
    # Regions / lands
    'arabia', 'asia', 'assyria', 'babylonia', 'canaan', 'cilicia',
    'egypt', 'galatia', 'goshen', 'greece', 'idumea', 'iran', 'israel',
    'macedonia', 'mesopotamia', 'moabite', 'palestine', 'paphos',
    'persia', 'phoenicia', 'sheba', 'syria', 'transjordan',
    # Bodies of water / rivers
    'jordan', 'jordan-river', 'euphrates', 'nile', 'tigris',
    'galilee-sea', 'mediterranean', 'red-sea', 'salt-sea', 'dead-sea',
    # Islands / waystations
    'cyprus', 'crete', 'malta', 'melita', 'patmos', 'rhodes',
    # Wilderness / specific places
    'eden', 'gethsemane', 'golgotha', 'gehenna', 'sheol', 'hades',
    'paradise', 'arabah', 'jezreel-valley',
}

# Slug-based hints used when the POS field is bare "proper noun"
PLACE_SLUG_SUFFIXES = (
    '-city', '-place', '-region', '-land', '-mount', '-mountain',
    '-river', '-sea', '-valley', '-island', '-plain', '-wilderness',
    '-town', '-spring', '-well', '-pool', '-brook',
)
PEOPLE_SLUG_SUFFIXES = (
    '-figure', '-prophet', '-king', '-judge', '-priest', '-apostle',
    '-evangelist', '-deacon', '-elder', '-disciple', '-martyr',
    '-first', '-younger', '-elder',
)
OTHER_SLUG_SUFFIXES = (
    '-exile', '-period', '-age', '-era', '-captivity', '-cycle',
    '-incident', '-rebellion', '-event', '-discourse',
)

# Known divine-name slugs (matches if exact or prefix)
DIVINE_NAME_SLUGS = {
    'yhwh', 'yahweh', 'jehovah', 'adonai', 'elohim', 'eloah',
    'el', 'el-elyon', 'el-shaddai', 'el-olam', 'el-roi', 'el-bethel',
    'el-elohe-israel', 'el-berith', 'jehovah-jireh', 'jehovah-nissi',
    'jehovah-rapha', 'jehovah-rohi', 'jehovah-roi', 'jehovah-shalom',
    'jehovah-shammah', 'jehovah-tsidkenu', 'jehovah-mekaddishkem',
    'jehovah-tsabaoth', 'yhwh-jireh', 'yhwh-nissi', 'yhwh-rapha',
    'yhwh-roi', 'yhwh-shalom', 'yhwh-shammah', 'yhwh-tsidkenu',
    'yhwh-mekaddishkem', 'yhwh-tsabaoth', 'yhwh-tsabaoth',
    'i-am', 'immanuel', 'messiah', 'son-of-god', 'son-of-man',
    'lamb-of-god', 'word-of-god', 'word', 'logos', 'christ', 'jesus',
    'lord-of-lords', 'king-of-kings', 'alpha-omega', 'alpha-and-omega',
    'mighty-god', 'prince-peace', 'prince-of-peace', 'wonderful-counselor',
    'counselor-wonderful', 'everlasting-father', 'ancient-of-days',
    'good-shepherd', 'great-shepherd', 'chief-shepherd', 'great-i-am',
    'angel-of-the-lord', 'angel-of-lord',
    # Seven I-AMs
    'i-am-bread', 'i-am-light', 'i-am-door', 'i-am-shepherd',
    'i-am-resurrection', 'i-am-way', 'i-am-vine', 'seven-i-am',
    # Christ titles also rendered as I AM
    'bread-of-life', 'light-of-world', 'way-truth-life', 'true-vine',
    'lion-of-judah', 'root-of-david', 'branch', 'branch-of-david',
    'righteous-branch', 'rod-of-jesse',
    'faithful-true-witness', 'amen-faithful-witness',
    'lamb-slain', 'firstborn-from-dead', 'only-begotten',
}

# Slug suffixes / words that mark divine-name compounds
DIVINE_PREFIXES = ('el-', 'jehovah-', 'yhwh-', 'yah-')
DIVINE_CONTAINS = ('-of-god', '-of-the-lord')


def extract_word_info(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    word = h1_m.group(1).strip() if h1_m else ''
    word = re.sub(r'<[^>]+>', '', word).strip()
    if not word:
        word = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()
    pos_m = re.search(r'class=["\']pos["\'][^>]*>(.*?)</[^>]+>', content, re.DOTALL)
    pos = pos_m.group(1).strip() if pos_m else ''
    pos = re.sub(r'<[^>]+>', '', pos).strip()
    return word, pos


def classify(pos, slug=''):
    """Return one of: people, places, books, tribes, divine, other, or None.

    Uses both POS hints AND slug-based heuristics — many bare "proper noun"
    entries have categorical signals in their slug (e.g., -city, -figure,
    el-/jehovah- prefixes).
    """
    p = pos.lower()
    p_norm = p.replace('&mdash;', '/').replace('—', '/').replace('  ', ' ')

    is_proper = 'proper noun' in p_norm or p_norm == 'bible book'
    if not is_proper:
        return None

    # 1. BOOKS — most distinctive
    if 'bible book' in p_norm or '/ book' in p_norm or 'book of bible' in p_norm or 'bible section' in p_norm:
        return 'books'

    # 2. DIVINE NAMES & CHRIST TITLES — explicit POS hints
    if 'divine name' in p_norm or 'christ-title' in p_norm or 'christ title' in p_norm:
        return 'divine'
    # Slug-based divine-name detection
    if slug in DIVINE_NAME_SLUGS:
        return 'divine'
    if any(slug.startswith(prefix) for prefix in DIVINE_PREFIXES):
        return 'divine'

    # 3. TRIBES & NATIONS
    if 'tribe' in p_norm or 'nation' in p_norm or '(sect)' in p_norm or '(group)' in p_norm:
        return 'tribes'

    # 4. PLACES — POS hints
    place_markers = ('city', 'town', 'place', 'mountain', 'island',
                     'body of water', 'region', 'river', 'valley')
    if any(m in p_norm for m in place_markers):
        return 'places'

    # 5. PEOPLE — POS hints
    people_markers = ('figure', 'person', 'king', 'judge', 'priest',
                      'apostle', 'prophet', 'address')
    if any(m in p_norm for m in people_markers):
        return 'people'

    # 6. Bare "proper noun" — use slug suffix heuristics
    if slug in KNOWN_PLACE_SLUGS:
        return 'places'
    if slug.endswith(PLACE_SLUG_SUFFIXES):
        return 'places'
    if slug.endswith(PEOPLE_SLUG_SUFFIXES):
        return 'people'
    if slug.endswith(OTHER_SLUG_SUFFIXES):
        return 'other'

    # 7. Special compound names (slug-based divine)
    if any(suffix in slug for suffix in DIVINE_CONTAINS):
        return 'divine'

    # 8. Bare-proper-noun default: people (sample shows most bare entries
    # are biblical persons — Aaron, Abel, Abraham, etc.)
    return 'people'


def letter_of(word):
    if not word:
        return '#'
    c = word[0].upper()
    return c if c.isalpha() else '#'


def render_letter_block(letter, entries):
    cards = '\n'.join(
        f'                            <a href="{e["file"]}" class="word-card">'
        f'<div class="word">{e["word"]}</div>'
        f'<div class="pos">{e["pos"]}</div></a>'
        for e in entries
    )
    return (
        f'                    <div class="category">\n'
        f'                        <h3>{letter} <span class="count-badge">{len(entries)}</span></h3>\n'
        f'                        <div class="word-grid">\n'
        f'{cards}\n'
        f'                        </div>\n'
        f'                    </div>'
    )


def render_section(cat_id, label_plain, label_emoji, intro, entries):
    by_letter = defaultdict(list)
    for e in entries:
        by_letter[letter_of(e['word'])].append(e)
    letters = sorted(by_letter.keys())
    blocks = '\n'.join(render_letter_block(l, by_letter[l]) for l in letters)
    return f'''
            <section class="names-section" id="sec-{cat_id}">
                <h2>{label_emoji} <span class="count-badge-lg">{len(entries)}</span></h2>
                <p class="sec-intro">{intro}</p>
{blocks}
            </section>'''


def build_html(buckets, total):
    section_buttons = '\n'.join(
        f'                <button class="sec-btn" onclick="jumpTo(\'sec-{cid}\')">{lbl_emoji} '
        f'<span class="sec-btn-count">{len(buckets[cid])}</span></button>'
        for (cid, _lbl, lbl_emoji, _intro) in CATEGORIES
        if buckets.get(cid)
    )

    sections_html = '\n'.join(
        render_section(cid, lbl_plain, lbl_emoji, intro, buckets[cid])
        for (cid, lbl_plain, lbl_emoji, intro) in CATEGORIES
        if buckets.get(cid)
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MOOP Dictionary &mdash; Biblical Names</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; display:inline-flex; align-items:center; gap:4px; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a:link,nav a:visited,nav a:active {{ color:var(--gray) !important; text-decoration:none !important; }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .site-icon {{ vertical-align:middle; opacity:0.8; }}
        .bte-theme-toggle {{
            justify-content: center; margin: 8px auto 0; width: fit-content;
            display: flex; align-items: center; gap: 0;
            background: rgba(30,30,30,0.85); border: 1px solid #333;
            border-radius: 20px; padding: 3px 6px; cursor: pointer;
            font-size: 0.7rem; user-select: none; backdrop-filter: blur(6px);
            transition: all 0.3s;
        }}
        .bte-theme-toggle:hover {{ border-color: #D4AF37; }}
        .bte-theme-toggle .toggle-icon {{ width: 18px; text-align: center; line-height: 1; }}
        .bte-theme-toggle .toggle-track {{
            width: 28px; height: 14px; background: #444; border-radius: 7px;
            position: relative; margin: 0 4px; transition: background 0.3s;
        }}
        .bte-theme-toggle .toggle-knob {{
            width: 10px; height: 10px; background: #D4AF37; border-radius: 50%;
            position: absolute; top: 2px; left: 2px; transition: left 0.3s;
        }}
        body.light-mode .bte-theme-toggle {{ background: rgba(240,238,233,0.9); border-color: #ccc; }}
        body.light-mode .bte-theme-toggle .toggle-track {{ background: #bbb; }}
        body.light-mode .bte-theme-toggle .toggle-knob {{ left: 16px; }}
        .bte-theme-toggle .moon-icon {{ color: #888; }}
        .bte-theme-toggle .sun-icon {{ color: #888; }}
        body.light-mode .bte-theme-toggle .sun-icon {{ color: #D4AF37; }}
        body:not(.light-mode) .bte-theme-toggle .moon-icon {{ color: #D4AF37; }}
        .container {{ max-width:900px; margin:0 auto; padding:20px; }}
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .hero h1 {{ font-size:2.6rem; color:var(--gold-light); margin-bottom:10px; }}
        .hero p {{ color:var(--gray); max-width:640px; margin:10px auto; }}
        .subtitle {{ font-size:1.05rem; color:var(--gray); font-style:italic; }}
        .back-link {{ display:inline-block; margin-top:18px; padding:6px 16px; border:1px solid var(--border); border-radius:20px; font-size:0.85rem; }}
        .back-link:hover {{ border-color:var(--gold); }}

        .sec-bar {{ display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin:24px 0 28px; }}
        .sec-btn {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:8px 16px; color:var(--white); font-size:0.88rem; font-family:'Inter',sans-serif; cursor:pointer; transition:all 0.2s; display:inline-flex; align-items:center; gap:8px; }}
        .sec-btn:hover {{ border-color:var(--gold); color:var(--gold); }}
        .sec-btn-count {{ background:var(--gold); color:#000; font-size:0.7rem; font-weight:700; padding:1px 7px; border-radius:10px; }}

        .names-section {{ margin:40px 0; scroll-margin-top:80px; }}
        .names-section > h2 {{ color:var(--gold-light); font-size:1.6rem; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:6px; }}
        .sec-intro {{ color:var(--gray); font-size:0.9rem; margin-bottom:18px; }}
        .count-badge-lg {{ display:inline-block; background:var(--gold); color:#000; font-size:0.75rem; font-weight:700; padding:3px 10px; border-radius:10px; margin-left:8px; vertical-align:middle; }}

        .category {{ margin:24px 0; }}
        .category h3 {{ color:var(--gold); font-size:1.15rem; margin-bottom:12px; border-bottom:1px solid var(--border); padding-bottom:6px; }}
        .word-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(160px, 1fr)); gap:10px; }}
        .word-card {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:12px 16px; text-decoration:none; color:var(--white); transition:border-color 0.2s, color 0.2s; }}
        .word-card:hover {{ border-color:var(--gold); color:var(--gold-light); }}
        .word-card .word {{ font-family:'Playfair Display',serif; font-size:1rem; }}
        .word-card .pos {{ font-size:0.75rem; color:var(--gray); margin-top:2px; }}
        .count-badge {{ display:inline-block; background:var(--gold); color:#000; font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:10px; margin-left:8px; vertical-align:middle; }}

        footer {{ text-align:center; padding:28px 20px; border-top:1px solid var(--border); margin-top:40px; color:var(--gray); font-size:0.88rem; }}
        footer a {{ color:var(--gray); text-decoration:none; }}
        footer a:hover {{ color:var(--gold); }}
        .cross-divider {{ margin-bottom:10px; }}

        body.light-mode {{ --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(245,243,239,0.97); }}
        body.light-mode .word-card,
        body.light-mode .sec-btn {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode footer {{ border-top-color:#d4d0c8; }}
        a, a:link, a:visited {{ color: var(--gold, #D4AF37) !important; }}
        a:hover {{ color: var(--gold-light, #F4D470) !important; }}

        .search-wrap {{ max-width:500px; margin:0 auto 16px; position:relative; }}
        .search-wrap input {{ width:100%; padding:12px 18px 12px 42px; background:var(--card); border:1px solid var(--border); border-radius:50px; color:var(--white); font-size:0.95rem; outline:none; transition:border-color 0.2s; font-family:'Inter',sans-serif; }}
        .search-wrap input:focus {{ border-color:var(--gold); }}
        .search-wrap input::placeholder {{ color:#555; }}
        .search-icon {{ position:absolute; left:15px; top:50%; transform:translateY(-50%); color:var(--gray); pointer-events:none; }}
        #searchResults {{ display:none; }}
        #searchResults.visible {{ display:block; }}
        #searchResults .word-grid {{ margin-top:10px; }}

        @media (min-width: 1025px) {{ .container {{ max-width: 1100px; }} }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <nav>
        <a href="../index.html"><img src="../assets/icons/shield-home-48.png" class="site-icon" alt="" width="16" height="16"> Home</a>
        <a href="../watchman.html"><img src="../assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Watchman</a>
        <a href="../bible.html"><img src="../assets/icons/shield-compass.png" class="site-icon" alt="" width="16" height="16"> BTE</a>
        <a href="../lexicon.html"><img src="../assets/icons/shield-alpha-omega-48.png" class="site-icon" alt="" width="16" height="16"> Lexicon</a>
        <a href="../cross-references.html"><img src="../assets/icons/shield-infinity-rope-48.png" class="site-icon" alt="" width="16" height="16"> Cross-Refs</a>
        <a href="index.html" class="active"><img src="../assets/icons/shield-book-greek-48.png" class="site-icon" alt="" width="16" height="16"> Dictionary</a>
        <a href="../blog.html"><img src="../assets/icons/shield-blog-quill-48.png" class="site-icon" alt="" width="16" height="16"> Blog</a>
        <a href="../connect.html"><img src="../assets/icons/shield-handshake.png" class="site-icon" alt="" width="16" height="16"> Connect</a>
    </nav>
    <div style="text-align:center; margin-top:8px; margin-bottom:4px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">
            <span class="toggle-icon moon-icon">🌙</span>
            <div class="toggle-track"><div class="toggle-knob"></div></div>
            <span class="toggle-icon sun-icon">☀️</span>
        </div>
    </div>
    <div class="container">

        <section class="hero">
            <img src="../assets/icons/shield-book-greek-48.png" alt="Dictionary" width="80" height="80" style="margin-bottom:14px;opacity:0.9;">
            <h1>Biblical Names</h1>
            <p class="subtitle">A names-only word-study layer of the MOOP Dictionary</p>
            <p style="margin-top:18px;">Every named figure, place, book, and tribe in the dictionary, gathered here for focused study. Full definitions and cross-references still live in the main dictionary &mdash; this page is just for finding them faster.</p>
            <p style="margin-top:10px;font-size:0.85rem;color:var(--gold);">{total} names &middot; 5 categories &middot; alphabetized within each</p>
            <a href="index.html" class="back-link">&larr; Back to Main Dictionary</a>
        </section>

        <div class="search-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="namesSearch" placeholder="Search names&hellip;" autocomplete="off" oninput="filterNames(this.value)">
        </div>

        <div id="searchResults">
            <div class="word-grid" id="searchGrid"></div>
            <p id="searchEmpty" style="display:none;color:var(--gray);text-align:center;padding:20px;">No names found.</p>
        </div>

        <div class="sec-bar" id="secBar">
{section_buttons}
        </div>

        <div id="sectionsWrap">
{sections_html}
        </div>

    </div><!-- /.container -->

    <footer>
        <div class="cross-divider"><img src="../assets/icons/shield-cross-bible-48.png" alt="" width="48" height="48" style="opacity:0.8;margin-bottom:10px;"></div>
        <p>
            <a href="../index.html#uniting"><img src="../assets/icons/shield-hands-joining.png" class="site-icon" alt="" width="20" height="20"> Uniting</a>
            &nbsp;&nbsp;
            <a href="../serving.html"><img src="../assets/icons/shield-serving.png" class="site-icon" alt="" width="20" height="20"> Serving</a>
            &nbsp;&nbsp;
            <a href="../mentoring.html"><img src="../assets/icons/shield-mentoring.png" class="site-icon" alt="" width="20" height="20"> Mentoring</a>
            &nbsp;&nbsp;
            <a href="../counseling.html"><img src="../assets/icons/shield-family.png" class="site-icon" alt="" width="20" height="20"> Counseling</a>
            &nbsp;&nbsp;
            <a href="../about.html"><img src="../assets/icons/shield-about-person-24.png" class="site-icon" alt="" width="20" height="20"> About the Founder</a>
        </p>
        <p style="margin-top:10px; font-size:0.82rem; font-style:italic; color:#555;">&ldquo;Iron sharpens iron, and one man sharpens another.&rdquo; &mdash; Proverbs 27:17</p>
        <p style="margin-top:8px; font-size:0.8rem; color:#555;">For more info on our services or products to purchase in support of this ministry, check out our other website: <a href="https://usmcmin.com" style="color:var(--gold);">usmcmin.com</a></p>
        <p style="margin-top:6px; font-size:0.8rem; color:#555;"><a href="../sitemap.html" style="color:var(--gray);font-size:0.85rem;">🗺️ Site Map</a> &nbsp;&nbsp; Powered by MOOPbot Pro</p>
    </footer>
    <script>
    function jumpTo(id) {{
        var el = document.getElementById(id);
        if (el) el.scrollIntoView({{behavior:'smooth', block:'start'}});
    }}
    function filterNames(q) {{
        var sr = document.getElementById('searchResults');
        var sw = document.getElementById('sectionsWrap');
        var sb = document.getElementById('secBar');
        var sg = document.getElementById('searchGrid');
        var se = document.getElementById('searchEmpty');
        q = q.trim().toLowerCase();
        if (!q) {{
            sr.classList.remove('visible');
            sw.style.display = '';
            sb.style.display = '';
            return;
        }}
        sw.style.display = 'none';
        sb.style.display = 'none';
        sr.classList.add('visible');
        var cards = document.querySelectorAll('#sectionsWrap .word-card');
        var hits = [];
        cards.forEach(function(c) {{
            var w = c.querySelector('.word');
            if (w && w.textContent.toLowerCase().indexOf(q) !== -1) hits.push(c.cloneNode(true));
        }});
        sg.innerHTML = '';
        hits.forEach(function(c) {{ sg.appendChild(c); }});
        se.style.display = hits.length ? 'none' : 'block';
    }}
    function bteToggleTheme(){{document.body.classList.toggle('light-mode');localStorage.setItem('bte-theme',document.body.classList.contains('light-mode')?'light':'dark');}}
    (function(){{if(localStorage.getItem('bte-theme')==='light')document.body.classList.add('light-mode');}})();
    </script>
</body>
</html>'''


def main():
    files = sorted(
        f for f in os.listdir(DICT_DIR)
        if f.endswith('.html') and f not in SKIP
    )

    buckets = defaultdict(list)
    for fname in files:
        fpath = os.path.join(DICT_DIR, fname)
        try:
            word, pos = extract_word_info(fpath)
        except Exception as e:
            print(f'  SKIP {fname}: {e}')
            continue
        slug = fname[:-5]  # strip .html
        cat = classify(pos, slug)
        if cat is None:
            continue
        buckets[cat].append({'file': fname, 'word': word, 'pos': pos})

    for cat in buckets:
        buckets[cat].sort(key=lambda e: e['word'].lower())

    total = sum(len(v) for v in buckets.values())
    print(f'Total names: {total}')
    for cid, lbl, _e, _i in CATEGORIES:
        print(f'  {lbl}: {len(buckets.get(cid, []))}')

    html = build_html(buckets, total)
    with open(NAMES_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\nWrote {NAMES_FILE}')


if __name__ == '__main__':
    main()
