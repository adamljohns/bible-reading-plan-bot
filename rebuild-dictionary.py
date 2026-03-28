#!/usr/bin/env python3
"""Rebuild the MOOP Dictionary index page from all word HTML files.

Usage:
    python3 rebuild-dictionary.py

Scans docs/dictionary/*.html (excluding index.html and template.html),
extracts each word's <h1> and .pos element, groups by first letter,
then regenerates docs/dictionary/index.html from scratch.
"""

import os
import re
from collections import defaultdict

DICT_DIR = os.path.join(os.path.dirname(__file__), 'docs', 'dictionary')
INDEX_FILE = os.path.join(DICT_DIR, 'index.html')


def extract_word_info(filepath):
    """Extract word name and part of speech from a dictionary HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Word from <h1>
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    word = h1_m.group(1).strip() if h1_m else ''
    word = re.sub(r'<[^>]+>', '', word).strip()
    if not word:
        word = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()

    # Part of speech from class="pos"
    pos_m = re.search(r'class=["\']pos["\'][^>]*>(.*?)</[^>]+>', content, re.DOTALL)
    pos = pos_m.group(1).strip() if pos_m else ''
    pos = re.sub(r'<[^>]+>', '', pos).strip()

    return word, pos


def render_letter_section(letter, entries):
    """Render one <div class="category"> block for a letter."""
    cards = '\n'.join(
        f'                        <a href="{e["file"]}" class="word-card">'
        f'<div class="word">{e["word"]}</div>'
        f'<div class="pos">{e["pos"]}</div></a>'
        for e in entries
    )
    return (
        f'                <div class="category">\n'
        f'                    <h2>{letter} <span class="count-badge">{len(entries)}</span></h2>\n'
        f'                    <div class="word-grid">\n'
        f'{cards}\n'
        f'                    </div>\n'
        f'                </div>'
    )


def render_range(letters, by_letter):
    return '\n'.join(
        render_letter_section(l, by_letter[l])
        for l in letters
        if by_letter.get(l)
    )


def build_index(words, by_letter, total):
    """Generate the complete index.html string."""

    AD = render_range(['A', 'B', 'C', 'D'], by_letter)
    EI = render_range(['E', 'F', 'G', 'H', 'I'], by_letter)
    JN = render_range(['J', 'K', 'L', 'M', 'N'], by_letter)
    OS = render_range(['O', 'P', 'Q', 'R', 'S'], by_letter)
    TZ = render_range(['T', 'U', 'V', 'W', 'X', 'Y', 'Z'], by_letter)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The MOOP Dictionary of the English Language</title>
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
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:40px; }}
        .hero h1 {{ font-size:2.8rem; color:var(--gold-light); margin-bottom:10px; }}
        .hero p {{ color:var(--gray); max-width:600px; margin:10px auto; }}
        .subtitle {{ font-size:1.1rem; color:var(--gray); font-style:italic; }}
        .category {{ margin:35px 0; }}
        .category h2 {{ color:var(--gold); font-size:1.3rem; margin-bottom:15px; border-bottom:1px solid var(--border); padding-bottom:8px; }}
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
        body.light-mode .word-card {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode footer {{ border-top-color:#d4d0c8; }}
        a, a:link, a:visited {{ color: var(--gold, #D4AF37) !important; }}
        a:hover {{ color: var(--gold-light, #F4D470) !important; }}
        .search-wrap {{ max-width:500px; margin:0 auto 24px; position:relative; }}
        .search-wrap input {{ width:100%; padding:12px 18px 12px 42px; background:var(--card); border:1px solid var(--border); border-radius:50px; color:var(--white); font-size:0.95rem; outline:none; transition:border-color 0.2s; font-family:'Inter',sans-serif; }}
        .search-wrap input:focus {{ border-color:var(--gold); }}
        .search-wrap input::placeholder {{ color:#555; }}
        .search-icon {{ position:absolute; left:15px; top:50%; transform:translateY(-50%); color:var(--gray); pointer-events:none; }}
        .range-bar {{ display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:28px; }}
        .range-btn {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:8px 18px; color:var(--gray); font-size:0.88rem; font-family:'Inter',sans-serif; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:6px; }}
        .range-btn:hover {{ border-color:var(--gold); color:var(--gold); }}
        .range-btn.open {{ border-color:var(--gold); background:rgba(212,175,55,0.12); color:var(--gold); }}
        .range-btn .rarrow {{ display:inline-block; width:0; height:0; border-top:5px solid transparent; border-bottom:5px solid transparent; border-left:8px solid #D4AF37; transition:transform 0.25s; }}
        .range-btn.open .rarrow {{ transform:rotate(90deg); }}
        .range-panel {{ overflow:hidden; max-height:0; transition:max-height 0.35s ease; }}
        .range-panel.open {{ max-height:30000px; }}
        #searchResults {{ display:none; }}
        #searchResults.visible {{ display:block; }}
        /* Suggest a Word Form */
        .suggest-section {{
            max-width: 600px;
            margin: 50px auto 40px;
            padding: 32px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
        }}
        .suggest-section h2 {{ color: var(--gold-light); font-size: 1.5rem; margin-bottom: 8px; }}
        .suggest-section .suggest-sub {{ color: var(--gray); font-size: 0.9rem; margin-bottom: 24px; line-height: 1.6; }}
        .suggest-section label {{ display: block; color: var(--gray); font-size: 0.85rem; margin-bottom: 6px; font-weight: 500; }}
        .suggest-section input[type="text"],
        .suggest-section textarea {{
            width: 100%; background: #1a1a1a; border: 1px solid var(--border);
            border-radius: 8px; color: var(--white); font-family: 'Inter', sans-serif;
            font-size: 0.95rem; padding: 12px 16px; margin-bottom: 18px; outline: none;
            transition: border-color 0.2s; resize: vertical;
        }}
        .suggest-section input[type="text"]:focus,
        .suggest-section textarea:focus {{ border-color: var(--gold); }}
        .suggest-section input[type="text"]::placeholder,
        .suggest-section textarea::placeholder {{ color: #555; }}
        .suggest-section .btn-suggest {{
            background: var(--gold); color: #000; border: none; border-radius: 8px;
            padding: 12px 32px; font-size: 0.95rem; font-weight: 700;
            font-family: 'Inter', sans-serif; cursor: pointer; transition: background 0.2s;
        }}
        .suggest-section .btn-suggest:hover {{ background: var(--gold-light); }}
        body.light-mode .suggest-section {{ background: #fff; border-color: #d4d0c8; }}
        body.light-mode .suggest-section input[type="text"],
        body.light-mode .suggest-section textarea {{ background: #f5f3ef; border-color: #d4d0c8; color: #1a1a1a; }}
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
            <img src="../assets/icons/shield-book-greek-48.png" alt="Dictionary" width="96" height="96" style="margin-bottom:16px;opacity:0.9;">
            <h1>The MOOP Dictionary</h1>
            <p class="subtitle">of the English Language</p>
            <p style="margin-top:20px;">Words have been stolen, redefined, and weaponized. This dictionary reclaims them &mdash; returning to the etymological roots, the biblical meaning, and the Webster 1828 definitions that shaped Western civilization, against which modern corruptions are measured.</p>
            <p style="margin-top:10px;font-size:0.85rem;color:var(--gold);">{total} entries &middot; Proto-language roots &middot; Collapsible deep-dive sections</p>
        </section>

        <!-- Search -->
        <div class="search-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="dictSearch" placeholder="Search entries&hellip;" autocomplete="off" oninput="filterDict(this.value)">
        </div>

        <!-- Search results (shown when searching) -->
        <div id="searchResults">
            <div class="word-grid" id="searchGrid"></div>
            <p id="searchEmpty" style="display:none;color:var(--gray);text-align:center;padding:20px;">No entries found.</p>
        </div>

        <!-- Range buttons (hidden during search) -->
        <div id="rangeSection">
            <div class="range-bar">
                <button class="range-btn" id="btn-AD" onclick="toggleRange('range-AD','btn-AD')"><span class="rarrow"></span> A &ndash; D</button>
                <button class="range-btn" id="btn-EI" onclick="toggleRange('range-EI','btn-EI')"><span class="rarrow"></span> E &ndash; I</button>
                <button class="range-btn" id="btn-JN" onclick="toggleRange('range-JN','btn-JN')"><span class="rarrow"></span> J &ndash; N</button>
                <button class="range-btn" id="btn-OS" onclick="toggleRange('range-OS','btn-OS')"><span class="rarrow"></span> O &ndash; S</button>
                <button class="range-btn" id="btn-TZ" onclick="toggleRange('range-TZ','btn-TZ')"><span class="rarrow"></span> T &ndash; Z</button>
            </div>

            <!-- A-D -->
            <div class="range-panel" id="range-AD">
{AD}
            </div>

            <!-- E-I -->
            <div class="range-panel" id="range-EI">
{EI}
            </div>

            <!-- J-N -->
            <div class="range-panel" id="range-JN">
{JN}
            </div>

            <!-- O-S -->
            <div class="range-panel" id="range-OS">
{OS}
            </div>

            <!-- T-Z -->
            <div class="range-panel" id="range-TZ">
{TZ}
            </div>
        </div><!-- /#rangeSection -->

    </div><!-- /.container -->

    <!-- Suggest a Word -->
    <div class="suggest-section">
        <h2>📝 Suggest a Word</h2>
        <p class="suggest-sub">Know a word that should be in the MOOP Dictionary? We&rsquo;re always expanding. Submit your suggestion and we&rsquo;ll review it.</p>
        <form action="https://formsubmit.co/usmcministries2022@gmail.com" method="POST">
            <input type="hidden" name="_subject" value="MOOP Dictionary &mdash; Word Suggestion">
            <input type="hidden" name="_next" value="https://usmcmin.org/dictionary/index.html">
            <input type="hidden" name="_captcha" value="false">
            <label for="suggest-word">Suggested Word *</label>
            <input type="text" id="suggest-word" name="word" placeholder="e.g., Sanctity, Providence, Logos&hellip;" required>
            <label for="suggest-why">Why should it be defined? <span style="color:var(--gray);font-weight:400;">(optional)</span></label>
            <textarea id="suggest-why" name="reason" rows="4" placeholder="Share why this word matters, or how you&rsquo;d like to see it defined&hellip;"></textarea>
            <button type="submit" class="btn-suggest">Submit Suggestion &rarr;</button>
        </form>
    </div>

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
    function toggleRange(panelId, btnId) {{
        var panel = document.getElementById(panelId);
        var btn = document.getElementById(btnId);
        var isOpen = panel.classList.contains('open');
        document.querySelectorAll('.range-panel').forEach(function(p) {{ p.classList.remove('open'); }});
        document.querySelectorAll('.range-btn').forEach(function(b) {{ b.classList.remove('open'); }});
        if (!isOpen) {{
            panel.classList.add('open');
            btn.classList.add('open');
        }}
    }}
    function filterDict(q) {{
        var sr = document.getElementById('searchResults');
        var rs = document.getElementById('rangeSection');
        var sg = document.getElementById('searchGrid');
        var se = document.getElementById('searchEmpty');
        q = q.trim().toLowerCase();
        if (!q) {{
            sr.classList.remove('visible');
            rs.style.display = '';
            return;
        }}
        rs.style.display = 'none';
        sr.classList.add('visible');
        var cards = document.querySelectorAll('#rangeSection .word-card');
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
    # Scan all word files
    files = sorted(
        f for f in os.listdir(DICT_DIR)
        if f.endswith('.html') and f not in ('index.html', 'template.html')
    )

    words = []
    for fname in files:
        fpath = os.path.join(DICT_DIR, fname)
        try:
            word, pos = extract_word_info(fpath)
            words.append({'file': fname, 'word': word, 'pos': pos})
        except Exception as e:
            print(f'  SKIP {fname}: {e}')

    words.sort(key=lambda w: w['word'].lower())

    # Group by first letter
    by_letter = defaultdict(list)
    for w in words:
        first = w['word'][0].upper() if w['word'] else '#'
        if not first.isalpha():
            first = '#'
        by_letter[first].append(w)

    total = len(words)
    print(f'Total entries: {total}')
    for letter in sorted(by_letter.keys()):
        print(f'  {letter}: {len(by_letter[letter])}')

    html = build_index(words, by_letter, total)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\nWrote {INDEX_FILE}')


if __name__ == '__main__':
    main()
