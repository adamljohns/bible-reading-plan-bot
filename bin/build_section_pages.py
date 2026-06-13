#!/usr/bin/env python3
"""Build dedicated full-page browsers for each featured section of the dictionary.

Each section on the dictionary home page (Doctrinal Anchors, Biblical Order,
Expressly Prohibited, Most Corrupted Words, Gen-Z / Millennial / Gen X / Boomer
Decoded) gets its own dedicated page with all entries listed and section-accent
color theming. Matches the look-and-feel of docs/dictionary/names.html.

The generator parses docs/dictionary/index.html, extracts each section's anchor
list (visible + hidden combined), and produces:

    docs/dictionary/doctrinal-anchors.html
    docs/dictionary/biblical-order.html
    docs/dictionary/expressly-prohibited.html
    docs/dictionary/most-corrupted.html
    docs/dictionary/gen-z-decoded.html
    docs/dictionary/millennial-decoded.html
    docs/dictionary/gen-x-decoded.html
    docs/dictionary/boomer-decoded.html
"""
import os, re, html as html_lib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
INDEX = os.path.join(DICT_DIR, 'index.html')

# Section metadata: (css_class, page_slug, page_title, accent_hex, icon_filename, intro_paragraph)
SECTIONS = [
    {
        'css_class': 'featured-section',
        'card_class': 'featured-card',
        'word_class': 'fword',
        'tag_class': 'ftag',
        'slug': 'doctrinal-anchors',
        'title': 'Doctrinal Anchors',
        'accent': '#D4AF37',
        'accent_dim': 'rgba(212,175,55,0.10)',
        'icon': 'shield-chain-salvation-48.png',
        'intro': 'Words that hold the line. Foundational entries every man should know cold &mdash; the doctrines that anchor the Christian faith against every wind that blows.',
    },
    {
        'css_class': 'order-section',
        'card_class': 'order-card',
        'word_class': 'oword',
        'tag_class': 'otag',
        'slug': 'biblical-order',
        'title': 'Biblical Order',
        'accent': '#b85042',
        'accent_dim': 'rgba(184,80,66,0.10)',
        'icon': 'shield-crown.png',
        'intro': 'Patriarchy, headship, helpmeet, and the recovered vocabulary the modern church has tried to retire &mdash; including the New Christian Right / Kings Hall diagnosis of the Long House, the reviling wife, and the white-knight pattern.',
    },
    {
        'css_class': 'forbidden-section',
        'card_class': 'forbidden-card',
        'word_class': 'pword',
        'tag_class': 'ptag',
        'slug': 'expressly-prohibited',
        'title': 'Expressly Prohibited',
        'accent': '#8b1515',
        'accent_dim': 'rgba(139,21,21,0.10)',
        'icon': 'shield-chain-fire-48.png',
        'intro': 'Practices Scripture names directly &mdash; in Leviticus, Deuteronomy, the Gospels, the Epistles, or the Revelation &mdash; as forbidden, abomination, or grounds for exclusion from the kingdom. The modern church has retired many of these; the MOOP Dictionary holds them.',
    },
    {
        'css_class': 'corrupted-section',
        'card_class': 'corrupted-card',
        'word_class': 'cword',
        'tag_class': 'ctag',
        'slug': 'most-corrupted',
        'title': 'Most Corrupted Words',
        'accent': '#f44336',
        'accent_dim': 'rgba(244,67,54,0.10)',
        'icon': 'shield-chain-fire-48.png',
        'intro': 'Words that modern culture has stolen, redefined, or weaponized beyond recognition. Click any word to see what it actually means &mdash; before the linguistic laundering.',
    },
    {
        'css_class': 'genz-section',
        'card_class': 'genz-card',
        'word_class': 'gzword',
        'tag_class': 'gzverdict',
        'slug': 'gen-z-decoded',
        'title': 'Gen-Z Decoded',
        'accent': '#EC4899',
        'accent_dim': 'rgba(236,72,153,0.10)',
        'icon': 'shield-blog-quill-48.png',
        'intro': 'Every generation speaks a new dialect. Every dialect reveals a heart. Here is what the Gen-Z (and Gen Alpha) words mean and what Scripture says about them &mdash; with each entry verdict-tagged Redeemable, Neutral, Examine, or Reject.',
    },
    {
        'css_class': 'mill-section',
        'card_class': 'mill-card',
        'word_class': 'mword',
        'tag_class': 'mverdict',
        'slug': 'millennial-decoded',
        'title': 'Millennial Decoded',
        'accent': '#14B8A6',
        'accent_dim': 'rgba(20,184,166,0.10)',
        'icon': 'shield-blog-quill-48.png',
        'intro': 'Generation 1981&ndash;1996. They delayed adulthood, invented #squadgoals friendship, and turned YOLO into a life-philosophy. Here is what the words mean and what Scripture says.',
    },
    {
        'css_class': 'genx-section',
        'card_class': 'genx-card',
        'word_class': 'xword',
        'tag_class': 'xverdict',
        'slug': 'gen-x-decoded',
        'title': 'Gen X Decoded',
        'accent': '#84CC16',
        'accent_dim': 'rgba(132,204,22,0.10)',
        'icon': 'shield-blog-quill-48.png',
        'intro': 'Generation 1965&ndash;1980. Ironic, skeptical, and allergic to earnestness. They taught America the dismissive shrug. Here is what the vocabulary reveals and what Scripture corrects.',
    },
    {
        'css_class': 'boomer-section',
        'card_class': 'boomer-card',
        'word_class': 'bword',
        'tag_class': 'bverdict',
        'slug': 'boomer-decoded',
        'title': 'Boomer Decoded',
        'accent': '#D97706',
        'accent_dim': 'rgba(217,119,6,0.10)',
        'icon': 'shield-blog-quill-48.png',
        'intro': 'Generation 1946&ndash;1964. The counterculture vocabulary that built modern America&rsquo;s permissive moral imagination, plus some harmless retro-flavor. Here is what held up and what did not.',
    },
]


def extract_cards(index_html, css_class, card_class, word_class, tag_class):
    """Find all <a class="<card_class>"> ... </a> inside the section identified by css_class."""
    # Bound the section
    start_pat = re.compile(rf'<div class="{re.escape(css_class)}"', re.IGNORECASE)
    m = start_pat.search(index_html)
    if not m:
        return []
    after = index_html[m.start():]
    end_m = re.search(r'</div>\s*\n\s*<!--', after)
    block = after[:end_m.start()] if end_m else after[:8000]
    # Now extract each <a class="<card_class>"> ... </a>
    card_pat = re.compile(
        rf'<a\b[^>]*href="([^"]+)"[^>]*class="{re.escape(card_class)}"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    # Some pages have class first then href — match either ordering
    cards = []
    # First pattern: href before class
    pat1 = re.compile(
        rf'<a\s+href="([^"]+)"\s+class="{re.escape(card_class)}"[^>]*>\s*'
        rf'<div class="{re.escape(word_class)}">([^<]+)</div>\s*'
        rf'<div class="(?:{re.escape(tag_class)}|{re.escape(tag_class)}[^"]*)">([^<]+)</div>\s*'
        rf'</a>',
        re.DOTALL,
    )
    # Second pattern: class before href
    pat2 = re.compile(
        rf'<a\s+class="{re.escape(card_class)}"\s+href="([^"]+)"[^>]*>\s*'
        rf'<div class="{re.escape(word_class)}">([^<]+)</div>\s*'
        rf'<div class="(?:{re.escape(tag_class)}|{re.escape(tag_class)}[^"]*)">([^<]+)</div>\s*'
        rf'</a>',
        re.DOTALL,
    )
    found = list(pat1.finditer(block)) + list(pat2.finditer(block))
    return [(m.group(1), m.group(2), m.group(3)) for m in found]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} &mdash; MOOP Dictionary</title>
    <meta name="description" content="{title}: full page browse for the {title} featured section of the MOOP Dictionary.">
    <meta property="og:title" content="{title} &mdash; MOOP Dictionary">
    <meta property="og:description" content="Full-page browse of every entry in the {title} featured section.">
    <link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{
            --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470;
            --white:#FFF; --gray:#888; --border:#333;
            --accent:{accent}; --accent-dim:{accent_dim};
        }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; display:inline-flex; align-items:center; gap:4px; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .site-icon {{ vertical-align:middle; opacity:0.8; }}

        .container {{ max-width:1200px; margin:0 auto; padding:24px 20px 60px; }}

        section.hero {{
            text-align:center; padding:50px 20px 30px;
            background:linear-gradient(160deg,var(--accent-dim),transparent 60%);
            border-bottom:1px solid var(--border);
        }}
        section.hero img.hero-icon {{ width:80px; height:80px; margin-bottom:14px; opacity:0.95; }}
        section.hero h1 {{
            color:var(--accent); font-size:clamp(2rem,5vw,3rem);
            margin-bottom:10px; letter-spacing:0.5px;
        }}
        section.hero .subtitle {{ color:var(--gray); font-size:1rem; max-width:740px; margin:0 auto 16px; line-height:1.6; }}
        section.hero .count-line {{ font-size:0.85rem; color:var(--accent); letter-spacing:0.8px; }}
        section.hero .back-link {{
            display:inline-block; margin-top:18px; padding:8px 18px;
            color:var(--gray); border:1px solid var(--border); border-radius:20px;
            font-size:0.85rem; text-decoration:none; transition:all 0.2s;
        }}
        section.hero .back-link:hover {{ color:var(--accent); border-color:var(--accent); }}

        .search-wrap {{ position:relative; max-width:520px; margin:24px auto 18px; }}
        .search-wrap input {{
            width:100%; padding:10px 16px 10px 38px; background:var(--card);
            border:1px solid var(--border); border-radius:24px; color:var(--white);
            font-size:0.92rem; font-family:'Inter',sans-serif; outline:none;
            transition:border-color 0.2s;
        }}
        .search-wrap input::placeholder {{ color:var(--gray); }}
        .search-wrap input:focus {{ border-color:var(--accent); }}
        .search-wrap .search-icon {{
            position:absolute; left:14px; top:50%; transform:translateY(-50%);
            color:var(--gray); font-size:0.9rem; pointer-events:none;
        }}

        .full-grid {{
            display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
            gap:10px; margin-top:14px;
        }}
        .full-card {{
            background:var(--accent-dim); border:1px solid var(--accent);
            border-radius:8px; padding:12px 14px; text-decoration:none;
            transition:all 0.2s; text-align:center; opacity:0.94;
        }}
        .full-card:hover {{ background:var(--accent); opacity:1; transform:translateY(-1px); }}
        .full-card .word {{ color:var(--white); font-weight:600; font-size:0.95rem; line-height:1.25; }}
        .full-card:hover .word {{ color:#000; }}
        .full-card .tag {{ color:var(--accent); font-size:0.7rem; text-transform:uppercase; letter-spacing:0.6px; margin-top:4px; }}
        .full-card:hover .tag {{ color:#000; opacity:0.8; }}

        .empty-state {{ color:var(--gray); text-align:center; padding:24px; font-style:italic; }}

        body.light-mode {{ background:#f0eee9; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(240,238,233,0.95); border-bottom-color:#ccc; }}
        body.light-mode img[src*="/icons/shield-"]:not([src*="-bronze"]) {{ filter:brightness(.72) saturate(1.18) hue-rotate(-12deg); }}
        body.light-mode nav a {{ color:#666; }}
        body.light-mode nav a:hover {{ color:var(--accent); }}
        body.light-mode .full-card {{ background:#fff; border-color:var(--accent); }}
        body.light-mode .full-card .word {{ color:#1a1a1a; }}
        body.light-mode .full-card:hover {{ background:var(--accent); }}
        body.light-mode .full-card:hover .word {{ color:#fff; }}
        body.light-mode .search-wrap input {{ background:#fff; border-color:#ccc; color:#1a1a1a; }}

        footer {{ text-align:center; padding:32px 20px; border-top:1px solid var(--border); color:var(--gray); font-size:0.85rem; margin-top:60px; }}
        footer a {{ color:var(--accent); text-decoration:none; }}
    </style>
    <link rel="stylesheet" href="/assets/css/light-icons.css">
    <link rel="stylesheet" href="/assets/css/print.css" media="print">
</head>
<body>
    <nav aria-label="Site navigation">
        <a href="../index.html"><img src="../assets/icons/shield-home-property-48.png" class="site-icon" alt="" width="16" height="16"> Home</a>
        <a href="../bible.html"><img src="../assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Bible</a>
        <a href="../lexicon.html"><img src="../assets/icons/shield-book-greek-48.png" class="site-icon" alt="" width="16" height="16"> Lexicon</a>
        <a href="index.html" class="active"><img src="../assets/icons/shield-book.png" class="site-icon" alt="" width="16" height="16"> Dictionary</a>
        <a href="../blog.html"><img src="../assets/icons/shield-scroll-quill-48.png" class="site-icon" alt="" width="16" height="16"> Blog</a>
    </nav>

    <div class="container">

        <section class="hero">
            <img src="../assets/icons/{icon}" alt="" class="hero-icon">
            <h1>{title}</h1>
            <p class="subtitle">{intro}</p>
            <p class="count-line">{count} entries &middot; alphabetized</p>
            <a href="index.html" class="back-link">&larr; Back to Main Dictionary</a>
        </section>

        <div class="search-wrap">
            <span class="search-icon">&#128269;</span>
            <input type="text" id="sectionSearch" placeholder="Search this section&hellip;" autocomplete="off" oninput="filterCards(this.value)">
        </div>

        <div class="full-grid" id="cardGrid">
{cards_html}
        </div>
        <p class="empty-state" id="emptyState" style="display:none;">No entries match your search.</p>

    </div>

    <footer>
        <p>MOOP Dictionary &mdash; <strong style="color:var(--accent);">V5.25</strong> &middot; <a href="index.html">Full Dictionary Index</a> &middot; <a href="../index.html">Home</a></p>
    </footer>

    <script>
    function filterCards(query) {{
        query = query.trim().toLowerCase();
        var cards = document.querySelectorAll('#cardGrid .full-card');
        var shown = 0;
        cards.forEach(function(c) {{
            var word = (c.querySelector('.word')||{{}}).textContent || '';
            var tag = (c.querySelector('.tag')||{{}}).textContent || '';
            var hit = (word + ' ' + tag).toLowerCase().indexOf(query) !== -1;
            c.style.display = hit ? '' : 'none';
            if (hit) shown++;
        }});
        document.getElementById('emptyState').style.display = shown ? 'none' : 'block';
    }}

    // Theme persistence
    (function() {{
        if (localStorage.getItem('bte-theme') === 'light') {{
            document.body.classList.add('light-mode');
        }}
    }})();
    </script>
</body>
</html>
"""


def card_html(href, word, tag):
    return (
        f'            <a href="{html_lib.escape(href, quote=True)}" class="full-card">'
        f'<div class="word">{word.strip()}</div>'
        f'<div class="tag">{tag.strip()}</div>'
        f'</a>'
    )


def main():
    with open(INDEX, encoding='utf-8') as f:
        index_html = f.read()
    for sec in SECTIONS:
        cards = extract_cards(
            index_html,
            sec['css_class'],
            sec['card_class'],
            sec['word_class'],
            sec['tag_class'],
        )
        # Sort alphabetically by word
        cards.sort(key=lambda c: c[1].lower())
        cards_html = '\n'.join(card_html(*c) for c in cards)
        page = PAGE_TEMPLATE.format(
            title=sec['title'],
            accent=sec['accent'],
            accent_dim=sec['accent_dim'],
            icon=sec['icon'],
            intro=sec['intro'],
            count=len(cards),
            cards_html=cards_html,
        )
        out_path = os.path.join(DICT_DIR, f"{sec['slug']}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page)
        print(f'  wrote {sec["slug"]}.html ({len(cards)} entries)')


if __name__ == '__main__':
    main()
