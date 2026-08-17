#!/usr/bin/env python3
"""One-pass usmcmin.org polish: founder hero icons, blog nav, manhood heroes, sitemap stats."""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
BLOG = os.path.join(DOCS, "blog")

FOUNDER_PAGES = {
    "plan.html": ("shield-chain-sword-48.png", "The Plan"),
    "purpose.html": ("shield-target.png", "Purpose"),
    "vision.html": ("shield-compass.png", "Vision"),
    "elevation.html": ("shield-broadcast-48.png", "Elevation"),
    "about.html": ("shield-about-person-48.png", "About the Founder"),
}

FOUNDER_CHAIN = ["about.html", "plan.html", "purpose.html", "vision.html", "elevation.html"]

MANHOOD_HEROES = {
    "the-wrong-question-biblical-masculinity-part-1.html": "/assets/blog-7as-war-inside.jpg",
    "universal-christian-virtues-biblical-masculinity-part-2.html": "/assets/blog-7as-helping-hand.jpg",
    "male-specific-stewardships-biblical-masculinity-part-3.html": "/assets/blog-7as-warrior-soul.jpg",
    "character-desire-responsibility-biblical-masculinity-part-4.html": "/assets/blog-7as-tank-crew.jpg",
    "the-conversation-were-not-having-biblical-masculinity-part-5.html": "/assets/blog-7as-ch46.jpg",
    "what-michael-foster-gets-right-about-masculine-maturity.html": "/assets/blog-philosopher-nature.jpg",
}

POST_NAV_CSS = """
        /* post navigation (chronological) */
        .post-nav { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin: 40px 0 0; padding-top: 22px; border-top: 1px solid var(--border); }
        .post-nav a { color: var(--gold); text-decoration: none; font-size: 0.88rem; font-weight: 600; max-width: 48%; line-height: 1.35; }
        .post-nav a:hover { text-decoration: underline; }
        .post-nav .post-next { margin-left: auto; text-align: right; }
        .post-nav .post-label { display: block; font-size: 0.72rem; font-weight: 500; color: var(--gray); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
"""

FOUNDER_NAV_CSS = """
        /* founder pillar chain */
        .founder-chain { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin: 28px 0 0; padding-top: 18px; border-top: 1px solid var(--border); }
        .founder-chain a { color: var(--gold); text-decoration: none; font-size: 0.85rem; font-weight: 600; }
        .founder-chain a:hover { text-decoration: underline; }
        .founder-chain .chain-next { margin-left: auto; text-align: right; }
"""

HERO_ANCHOR_CSS = """
        .hero-anchor { display: inline-block; margin-bottom: 16px; }
        .hero-anchor img { filter: drop-shadow(0 0 12px rgba(212,175,55,0.4)); }
"""


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def inject_css(html: str, block: str) -> str:
    if block.strip() in html:
        return html
    return html.replace("    </style>", block + "\n    </style>", 1)


def fix_founder_hero_icons() -> int:
    n = 0
    for fn, (icon, alt) in FOUNDER_PAGES.items():
        path = os.path.join(DOCS, fn)
        if not os.path.exists(path):
            continue
        html = read(path)
        old_pat = re.compile(
            r'<div style="font-size:3rem; margin-bottom:16px; filter:drop-shadow\(0 0 8px rgba\(212,175,55,0\.4\)\);">'
            r'<img src="assets/icons/[^"]+" alt="" width="16" height="16"[^>]*></div>'
        )
        new = (
            f'<div class="hero-anchor"><img src="assets/icons/{icon}" class="site-icon" '
            f'alt="{escape(alt)}" width="96" height="96"></div>'
        )
        html, c = old_pat.subn(new, html, count=1)
        if c == 0:
            html = re.sub(
                r'(<div class="hero-anchor"><img src="assets/icons/[^"]+"[^>]*width=")(20|16)(" height=")(20|16)(")',
                r"\g<1>96\3>96\5",
                html,
                count=1,
            )
            if "class=\"hero-anchor\"" not in html:
                html = re.sub(
                    r'<div class="hero-anchor"><img src="assets/icons/([^"]+)" class="site-icon" alt="([^"]*)" width="\d+" height="\d+"',
                    r'<div class="hero-anchor"><img src="assets/icons/\1" class="site-icon" alt="\2" width="96" height="96"',
                    html,
                    count=1,
                )
        if ".hero-anchor" not in html:
            html = inject_css(html, HERO_ANCHOR_CSS)
        if html != read(path):
            write(path, html)
            n += 1
    return n


def add_founder_chain_nav() -> int:
    labels = {
        "about.html": "About",
        "plan.html": "The Plan",
        "purpose.html": "Purpose",
        "vision.html": "Vision",
        "elevation.html": "Elevation",
    }
    n = 0
    for i, fn in enumerate(FOUNDER_CHAIN):
        path = os.path.join(DOCS, fn)
        if not os.path.exists(path):
            continue
        html = read(path)
        html = re.sub(r'\n\s*<nav class="founder-chain"[^>]*>.*?</nav>\s*', "\n", html, flags=re.S)
        prev_l = next_l = ""
        if i > 0:
            prev_fn = FOUNDER_CHAIN[i - 1]
            prev_l = f'<a href="{prev_fn}">← {labels[prev_fn]}</a>'
        if i < len(FOUNDER_CHAIN) - 1:
            next_fn = FOUNDER_CHAIN[i + 1]
            next_l = f'<a class="chain-next" href="{next_fn}">{labels[next_fn]} →</a>'
        if not prev_l and not next_l:
            continue
        block = f'\n        <nav class="founder-chain" aria-label="Founder pages">{prev_l}{next_l}</nav>\n'
        if 'class="content"' in html and "founder-chain" not in html:
            html = inject_css(html, FOUNDER_NAV_CSS)
            html = html.replace("    </div>\n    <!-- ── Footer ── -->", block + "    </div>\n    <!-- ── Footer ── -->", 1)
            if "founder-chain" not in html:
                html = html.replace("    </div>\n\n    <script>", block + "    </div>\n\n    <script>", 1)
            write(path, html)
            n += 1
    return n


def parse_post_date(html: str, slug: str) -> datetime:
    for pat in (
        r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})',
        r'<meta name="article:modified_time" content="(\d{4}-\d{2}-\d{2})',
        r'Published ([A-Za-z]+ \d{1,2}, \d{4})',
        r'· ([A-Za-z]+ \d{1,2}, \d{4}) ·',
        r'· (\d{4}-\d{2}-\d{2}) ·',
    ):
        m = re.search(pat, html)
        if m:
            raw = m.group(1)
            for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
                try:
                    return datetime.strptime(raw, fmt)
                except ValueError:
                    pass
    mtime = os.path.getmtime(os.path.join(BLOG, slug))
    return datetime.fromtimestamp(mtime)


def build_blog_order() -> list[tuple[str, str, datetime]]:
    rows: list[tuple[str, str, datetime]] = []
    for fn in sorted(os.listdir(BLOG)):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(BLOG, fn)
        html = read(path)
        title_m = re.search(r"<title>([^<|]+)", html)
        title = title_m.group(1).strip() if title_m else fn[:-5].replace("-", " ").title()
        title = re.sub(r"\s*—.*$", "", title).strip()
        rows.append((fn, title, parse_post_date(html, fn)))
    rows.sort(key=lambda r: (r[2], r[0]))
    return rows


def render_post_nav(prev_row, next_row) -> str:
    parts = ['<nav class="post-nav" aria-label="Post navigation">']
    if prev_row:
        fn, title, _ = prev_row
        parts.append(
            f'<a href="/blog/{fn}"><span class="post-label">← Previous</span>{escape(title[:72])}</a>'
        )
    if next_row:
        fn, title, _ = next_row
        parts.append(
            f'<a class="post-next" href="/blog/{fn}"><span class="post-label">Next →</span>{escape(title[:72])}</a>'
        )
    parts.append("</nav>")
    return "".join(parts)


def inject_nav_html(html: str, nav: str) -> str | None:
    if re.search(r'<nav class="series-nav"', html):
        return re.sub(r"(<nav class=\"series-nav\"[^>]*>.*?</nav>)", r"\1\n        " + nav, html, count=1, flags=re.S)
    if "</article>" in html:
        return html.replace("</article>", "    " + nav + "\n</article>", 1)
    if 'class="back-link"' in html:
        return html.replace(
            '<a href="../blog.html" class="back-link">',
            nav + '\n        <a href="../blog.html" class="back-link">',
            1,
        )
    if "<footer>" in html:
        return html.replace("<footer>", nav + "\n\n    <footer>", 1)
    return None


def add_blog_post_nav(skip_series: bool = True) -> int:
    order = build_blog_order()
    n = 0
    for i, row in enumerate(order):
        fn = row[0]
        path = os.path.join(BLOG, fn)
        html = read(path)
        if skip_series and "series-nav" in html and "post-nav" not in html:
            # still add post-nav alongside series-nav below
            pass
        html = re.sub(r'\n\s*<nav class="post-nav"[^>]*>.*?</nav>\s*', "\n", html, flags=re.S)
        nav = render_post_nav(order[i - 1] if i else None, order[i + 1] if i < len(order) - 1 else None)
        if ".post-nav" not in html:
            html = inject_css(html, POST_NAV_CSS)
        updated = inject_nav_html(html, nav)
        if updated is None or updated == html:
            continue
        write(path, updated)
        n += 1
    return n


def swap_hero_image(html: str, new_src: str) -> str:
    html = re.sub(
        r'(<img class="hero-img"\s+src=")[^"]+(")',
        rf"\g<1>{new_src}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:image" content=")[^"]+(")',
        rf"\g<1>https://usmcmin.org{new_src}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="twitter:image" content=")[^"]+(")',
        rf"\g<1>https://usmcmin.org{new_src}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'("image":\s*")https://usmcmin\.org[^"]+(")',
        rf"\g<1>https://usmcmin.org{new_src}\2",
        html,
        count=1,
    )
    return html


def fix_manhood_heroes() -> int:
    n = 0
    for fn, hero in MANHOOD_HEROES.items():
        path = os.path.join(BLOG, fn)
        if not os.path.exists(path):
            continue
        html = read(path)
        html2 = swap_hero_image(html, hero)
        if html2 != html:
            write(path, html2)
            n += 1
    listing = os.path.join(DOCS, "blog-mens-ministry.html")
    if os.path.exists(listing):
        html = read(listing)
        html2 = html
        for fn, hero in MANHOOD_HEROES.items():
            slug = fn.replace(".html", "")
            html2 = re.sub(
                rf'(<a href="blog/{re.escape(slug)}\.html"[^>]*>.*?<img src=")[^"]+(")',
                rf"\g<1>{hero}\2",
                html2,
                count=1,
                flags=re.S,
            )
        if html2 != html:
            write(listing, html2)
            n += 1
    return n


def counts_for_sitemap_html() -> dict:
    blog_files = len([f for f in os.listdir(BLOG) if f.endswith(".html")])
    dict_manifest = os.path.join(DOCS, "assets/dictionary-manifest.json")
    dict_count = 0
    if os.path.exists(dict_manifest):
        m = json.load(open(dict_manifest))
        dict_count = m.get("generated_at_count") or m.get("count") or 0
    dict_html = len([f for f in os.listdir(os.path.join(DOCS, "dictionary")) if f.endswith(".html")])
    return {
        "blog": blog_files,
        "dictionary_manifest": dict_count,
        "dictionary_html": dict_html,
    }


def update_sitemap_html() -> None:
    path = os.path.join(DOCS, "sitemap.html")
    html = read(path)
    c = counts_for_sitemap_html()
    blog_n = c["blog"]
    dict_n = max(c["dictionary_manifest"], c["dictionary_html"])
    html = re.sub(
        r'(<li><a href="blog\.html"[^>]*>[^<]*</a><span class="page-desc">)— \d+ posts',
        rf"\g<1>— {blog_n} posts",
        html,
    )
    html = re.sub(r"(<li>Blog posts: <strong>)\d+(</strong></li>)", rf"\g<1>{blog_n}\g<2>", html)
    html = re.sub(
        r'(<span id="dictDescCount">)[\d,]+(</span>)',
        lambda m: f"{m.group(1)}{dict_n:,}{m.group(2)}",
        html,
    )
    html = re.sub(
        r'(<span id="dictCount">)[\d,]+(</span>)',
        lambda m: f"{m.group(1)}{dict_n:,}{m.group(2)}",
        html,
        count=1,
    )
    html = re.sub(
        r"(<li>Dictionary definitions: <strong><span id=\"dictCount\">)[^<]+(</span>\+?</strong></li>)",
        rf"\g<1>{dict_n:,}+\g<2>",
        html,
    )
    if 'id="blogCount"' not in html:
        html = html.replace(
            "<li>Blog posts: <strong>",
            '<li>Blog posts: <strong><span id="blogCount">',
            1,
        ).replace(
            f"<strong><span id=\"blogCount\">{blog_n}</strong></li>",
            f'<strong><span id="blogCount">{blog_n}</span></strong></li>',
            1,
        )
    write(path, html)


def main() -> None:
    os.chdir(ROOT)
    print("Founder hero icons fixed:", fix_founder_hero_icons())
    print("Founder chain nav added:", add_founder_chain_nav())
    print("Manhood hero images updated:", fix_manhood_heroes())
    print("Blog post nav injected:", add_blog_post_nav())
    print("Updating sitemap.html stats…")
    update_sitemap_html()
    c = counts_for_sitemap_html()
    print(f"Counts — blog: {c['blog']} | dictionary: {c['dictionary_html']} html / {c['dictionary_manifest']} manifest")


if __name__ == "__main__":
    main()
