#!/usr/bin/env python3
"""Add BTE dark/light theme support to every blog post page (docs/blog/*.html).

The 168 post pages share one dark template era (GitHub-dark palette in :root:
--bg #0d1117 / --card #161b22 / --border #30363d / --white #e6edf3 /
--gray #8b949e / --gold #d4af37; the two `article-hero` posts use the synonyms
--text / --text-dim / --bg-elev / --bg-card / --gold-soft / --link). For each
post this script:

  1. inserts <link rel="stylesheet" href="/assets/css/light-icons.css"> before
     </head> (engraved -lm icon swaps, scoped under body.light-mode);
  2. inserts a body.light-mode CSS override block before the LAST </style> in
     <head> — remaps the template variables to the site-wide light palette
     (#F5F3EF page / #fff surfaces / #d4d0c8 borders / #1a1a1a text /
     #B8960C gold) and pins the hardcoded colors that escape the variables;
     the canonical .bte-theme-toggle CSS from docs/index.html is prepended
     when the post has no toggle styles yet;
  3. inserts the canonical toggle markup right after <body> plus the
     bteToggleTheme() JS using localStorage key 'bte-theme' (same key as the
     rest of the site) with an on-load class apply.

Idempotent: each insertion is guarded by a marker already present in patched
files, so re-running changes nothing. Dark mode (the default) renders
byte-identical except the added toggle UI — every injected rule is scoped
under body.light-mode apart from the toggle's own styling.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO / "docs" / "blog"

# ── Step 1: light-icons stylesheet ──────────────────────────────────────────
LINK_GUARD = "light-icons.css"
LINK_TAG = '    <link rel="stylesheet" href="/assets/css/light-icons.css">\n'

# ── Step 2a: canonical toggle CSS (copied from docs/index.html) ─────────────
TOGGLE_CSS_GUARD = ".bte-theme-toggle"
TOGGLE_CSS = """
        /* ── BTE Dark/Light Mode Toggle ── */
        .bte-theme-toggle {
            justify-content: center; margin: 8px auto 0; width: fit-content;
            display: flex; align-items: center; gap: 0;
            background: rgba(30,30,30,0.85); border: 1px solid #333;
            border-radius: 20px; padding: 3px 6px; cursor: pointer;
            font-size: 0.7rem; user-select: none; backdrop-filter: blur(6px);
            transition: all 0.3s;
        }
        .bte-theme-toggle:hover { border-color: #D4AF37; }
        .bte-theme-toggle .toggle-icon { width: 18px; text-align: center; line-height: 1; }
        .bte-theme-toggle .toggle-track {
            width: 28px; height: 14px; background: #444; border-radius: 7px;
            position: relative; margin: 0 4px; transition: background 0.3s;
        }
        .bte-theme-toggle .toggle-knob {
            width: 10px; height: 10px; background: #D4AF37; border-radius: 50%;
            position: absolute; top: 2px; left: 2px; transition: left 0.3s;
        }
        body.light-mode .bte-theme-toggle { background: rgba(240,238,233,0.9); border-color: #ccc; }
        body.light-mode img[src*="/icons/shield-"]:not([src*="-bronze"]) { filter:brightness(.72) saturate(1.18) hue-rotate(-12deg); }
        body.light-mode .bte-theme-toggle .toggle-track { background: #bbb; }
        body.light-mode .bte-theme-toggle .toggle-knob { left: 16px; }
        body.light-mode .bte-theme-toggle .toggle-icon { filter: none; }
        .bte-theme-toggle .moon-icon { color: #888; }
        .bte-theme-toggle .sun-icon { color: #888; }
        body.light-mode .bte-theme-toggle .sun-icon { color: #D4AF37; }
        body:not(.light-mode) .bte-theme-toggle .moon-icon { color: #D4AF37; }
"""

# ── Step 2b: light-mode overrides for the post template ─────────────────────
LIGHT_CSS_GUARD = "BTE Light Mode (blog post)"
LIGHT_CSS = """
        /* ── BTE Light Mode (blog post) — injected by bin/add_blog_light_mode.py ── */
        /* Variable remap: lightens every var()-driven surface in one pass.   */
        body.light-mode {
            --bg: #F5F3EF; --card: #FFFFFF; --bg-card: #FFFFFF; --bg-elev: #FFFFFF;
            --border: #d4d0c8;
            --white: #1a1a1a; --text: #1a1a1a;
            --gray: #666666; --text-dim: #666666;
            --gold: #B8960C; --gold-light: #8a6d10; --gold-soft: #8a6d10; --link: #B8960C;
        }
        body.light-mode { background: #F5F3EF !important; color: #1a1a1a !important; }
        body.light-mode .top-nav { background: rgba(245,243,239,0.97) !important; border-color: #d4d0c8 !important; }
        body.light-mode .top-nav a, body.light-mode .top-nav a:link, body.light-mode .top-nav a:visited, body.light-mode .top-nav a:active { color: #555 !important; }
        body.light-mode .top-nav a:hover, body.light-mode .top-nav a.active { color: #B8960C !important; }
        /* Hardcoded body-copy grays (#c9d1d9 era) → dark ink */
        body.light-mode .article, body.light-mode .content { color: #1a1a1a; }
        body.light-mode .article p, body.light-mode .article ul, body.light-mode .article ol, body.light-mode .article li,
        body.light-mode .table-block .row, body.light-mode .table-block .row .label,
        body.light-mode .drift-list .item, body.light-mode .green-list .item, body.light-mode .contradiction-list .item,
        body.light-mode .matrix td, body.light-mode .fw-table td,
        body.light-mode .book-card .book-note, body.light-mode .endnote-refs { color: #333; }
        body.light-mode .article blockquote p { color: #8a6d10; }
        body.light-mode [style*="color:#c9d1d9"] { color: #333 !important; }
        /* White headings that sat on dark card surfaces */
        body.light-mode article.article strong, body.light-mode article.article li strong,
        body.light-mode .captain-card h3, body.light-mode .quad .cell h4,
        body.light-mode .saca .item h4, body.light-mode .saca .item .script,
        body.light-mode .quad .cell.featured .quote-line,
        body.light-mode .attribution h3, body.light-mode .deck-cta .copy h4,
        body.light-mode .dict-cta h3 { color: #1a1a1a !important; }
        /* Card / section surfaces */
        body.light-mode .cta-box { background: #fff !important; }
        body.light-mode .sc-candidate, body.light-mode .profile-cat, body.light-mode .howto-step { background: #fff !important; border-color: #d4d0c8; }
        body.light-mode .profile-progress { background: #ddd !important; }
        body.light-mode footer { background: #F5F3EF !important; border-color: #d4d0c8 !important; color: #666 !important; }
        body.light-mode input, body.light-mode textarea, body.light-mode select { background: #fff !important; color: #1a1a1a !important; border-color: #d4d0c8 !important; }
"""

# Fallback when a post has no <style> in <head> at all (none today).
STYLE_WRAPPER = "    <style>\n%s    </style>\n"

# ── Step 3: canonical toggle markup + theme JS (after <body>) ───────────────
MARKUP_GUARD = 'onclick="bteToggleTheme()"'
JS_GUARD = "function bteToggleTheme"
TOGGLE_MARKUP = """
    <div style="text-align:center; margin-top:8px; margin-bottom:4px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">
            <span class="toggle-icon moon-icon">\U0001f319</span>
            <div class="toggle-track"><div class="toggle-knob"></div></div>
            <span class="toggle-icon sun-icon">☀️</span>
        </div>
    </div>
"""
# In-nav variant (preferred): light-icons.css floats it top-right via
# .nav-theme-toggle, and the flex nav wraps to fit it — no overlap on mobile.
TOGGLE_MARKUP_NAV = (
    '<div class="bte-theme-toggle nav-theme-toggle" onclick="bteToggleTheme()" '
    'title="Toggle dark/light mode" role="button" tabindex="0" '
    'aria-label="Toggle dark/light mode"></div>'
)
TOGGLE_JS = """    <script>
    /* ── BTE Dark/Light Mode ── */
    function bteToggleTheme(){
        document.body.classList.toggle('light-mode');
        localStorage.setItem('bte-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
    }
    (function(){
        if(localStorage.getItem('bte-theme')==='light') document.body.classList.add('light-mode');
    })();
    </script>
"""

BODY_RE = re.compile(r"<body\b[^>]*>")


def patch(html: str, fname: str):
    """Return (new_html, list_of_steps_applied)."""
    steps = []

    head_end = html.find("</head>")
    if head_end < 0:
        return html, [f"SKIP: no </head> in {fname}"]

    # 2) light-mode CSS (and toggle CSS if absent) before the LAST </style> in <head>
    css_chunk = ""
    if TOGGLE_CSS_GUARD not in html:
        css_chunk += TOGGLE_CSS
        steps.append("toggle-css")
    if LIGHT_CSS_GUARD not in html:
        css_chunk += LIGHT_CSS
        steps.append("light-css")
    if css_chunk:
        style_end = html.rfind("</style>", 0, head_end)
        if style_end >= 0:
            html = html[:style_end] + css_chunk + "    " + html[style_end:]
        else:  # no <style> in head — create one just before </head>
            html = html[:head_end] + (STYLE_WRAPPER % css_chunk) + html[head_end:]
            steps.append("style-block-created")

    # 1) light-icons.css link before </head>
    if LINK_GUARD not in html:
        head_end = html.find("</head>")
        html = html[:head_end] + LINK_TAG + html[head_end:]
        steps.append("link")

    # 3) toggle markup INSIDE the nav (uniform top-right; the wrapping nav
    #    reserves space so it never overlaps links on mobile), then the theme JS
    #    right after the <body...> opening tag.
    if MARKUP_GUARD not in html:
        nav_close = html.find("</nav>")
        if nav_close >= 0:
            html = html[:nav_close] + TOGGLE_MARKUP_NAV + html[nav_close:]
            steps.append("toggle-markup")
        else:  # no <nav> — fall back to the standalone block after <body>
            m = BODY_RE.search(html)
            if not m:
                return html, [f"SKIP: no <body> in {fname}"]
            html = html[: m.end()] + TOGGLE_MARKUP + html[m.end():]
            steps.append("toggle-markup-no-nav")
    if JS_GUARD not in html:
        m = BODY_RE.search(html)
        if not m:
            return html, [f"SKIP: no <body> in {fname}"]
        html = html[: m.end()] + TOGGLE_JS + html[m.end():]
        steps.append("theme-js")

    return html, steps


def main() -> int:
    posts = sorted(BLOG_DIR.glob("*.html"))
    if not posts:
        print(f"No posts found under {BLOG_DIR}", file=sys.stderr)
        return 1

    patched, unchanged, skipped = 0, 0, 0
    for post in posts:
        html = post.read_text(encoding="utf-8")
        new_html, steps = patch(html, post.name)
        if any(s.startswith("SKIP") for s in steps):
            skipped += 1
            print(f"  !! {post.name}: {steps}")
            continue
        if new_html != html:
            post.write_text(new_html, encoding="utf-8")
            patched += 1
        else:
            unchanged += 1

    print(f"Scanned {len(posts)} posts in {BLOG_DIR.relative_to(REPO)}: "
          f"{patched} patched, {unchanged} already up to date, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
