#!/usr/bin/env python3
"""Generate docs/dictionary/jesus-generation.html.

A curated Special Directory: "The Jesus Generation." Where the four
generational decoders (Gen-Z / Millennial / Gen-X / Boomer) divide by
dialect, this page does the opposite — it gathers the words of revival,
prayer, new life, legacy, and worship around the one generation that
unites every age: the generation that belongs to Jesus.

Inspired by Forrest Frank's "The Jesus Generation" tour. The vision is a
redemption of the generational divide — not a decade or a demographic,
but a people of every age made willing in the day of God's power.

The curation is hand-editorial under DICTIONARY-VOICE-LOCK.md. Missing
slugs print a warning and are skipped (the page still builds).

When entries are added or renamed, edit SECTIONS below and re-run:
    python3 bin/build_jesus_generation.py
Then commit docs/dictionary/jesus-generation.html with the change.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

DICT_DIR = Path(__file__).resolve().parent.parent / "docs" / "dictionary"

# Each tuple: (anchor, title, lead, [slugs]). Slugs verified at build time.
SECTIONS = [
    (
        "revival-awakening", "Revival &amp; Awakening",
        "When God pours out His Spirit and a generation is made willing in the day of His power.",
        ["revival", "awakening", "great-awakening", "renewal", "jesus-movement",
         "pentecost", "outpouring", "first-love"],
    ),
    (
        "prayer-consecration", "Passionate Prayer &amp; Consecration",
        "The fervent, wrestling prayer and whole-hearted devotion that go before every true awakening.",
        ["passionate-prayer", "prayer", "intercession", "consecration",
         "repentance", "zeal", "fasting", "conviction-of-sin"],
    ),
    (
        "first-love-new-life", "First Love &amp; New Life",
        "The new birth and the freshly-kindled first love of a heart set wholly on Christ.",
        ["born-again", "new-creation", "regeneration", "conversion",
         "holiness", "sanctification", "joy", "testimony"],
    ),
    (
        "legacy-generations", "Legacy &amp; the Generations",
        "The faith handed down, that the generation to come might know it and declare it to their children.",
        ["legacy", "generations", "covenant", "catechesis-doctrine",
         "covenant-family", "household-religion", "discipleship", "make-disciples"],
    ),
    (
        "unity-worship", "Unity &amp; Worship",
        "One body of many ages, united not by a decade or a demographic but by the Lamb who was slain.",
        ["unity", "worship", "one-another", "one-in-christ-doctrine",
         "household-of-faith", "fellowship", "psalm-119", "marriage-supper-of-the-lamb"],
    ),
]

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>MOOP Dictionary &mdash; The Jesus Generation</title>
    <meta name="description" content="The Jesus Generation — a curated MOOP Dictionary directory of revival, passionate prayer, new life, legacy, and worship. The generation that unites every age is the one that belongs to Jesus.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --black: #0a0a0a; --gray-darker: #161616; --gray-dark: #1f1f1f;
            --gray: #999; --gray-light: #ccc; --white: #f5f5f5;
            --gold: #d4af37; --gold-soft: rgba(212,175,55,0.12);
            --border: rgba(212,175,55,0.18);
        }
        * { box-sizing: border-box; }
        body { background:var(--black); color:var(--white); font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif; margin:0; padding:0; line-height:1.6; }
        .container { max-width:1200px; margin:0 auto; padding:24px 22px 80px; }
        .topbar { display:flex; align-items:center; gap:14px; font-size:0.85rem; color:var(--gray-light); margin-bottom:30px; flex-wrap:wrap; }
        .topbar a { color:var(--gold); text-decoration:none; }
        .topbar a:hover { text-decoration:underline; }
        h1 { font-family:'Playfair Display',serif; color:var(--gold); font-size:2.5rem; margin:0 0 8px; }
        .lead { color:var(--gray-light); font-size:1.05rem; margin-bottom:24px; }
        .vision { background:linear-gradient(135deg,rgba(212,175,55,0.10) 0%,rgba(212,175,55,0.02) 100%); border:1px solid var(--border); border-radius:14px; padding:22px 26px; margin:24px 0 36px; }
        .vision h2 { font-family:'Playfair Display',serif; color:var(--gold); font-size:1.3rem; margin:0 0 10px; }
        .vision p { color:var(--gray-light); font-size:0.98rem; margin:0 0 12px; }
        .vision p:last-child { margin-bottom:0; }
        .vision .credit { color:var(--gray); font-size:0.82rem; font-style:italic; }
        .toc { background:var(--gray-darker); border:1px solid var(--border); border-radius:12px; padding:18px 22px; margin:24px 0 40px; }
        .toc h2 { font-family:'Playfair Display',serif; color:var(--gold); font-size:1.15rem; margin:0 0 12px; }
        .toc-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:8px; }
        .toc-grid a { color:var(--white); text-decoration:none; padding:7px 10px; border-radius:6px; font-size:0.92rem; display:block; transition:all 0.15s; border:1px solid transparent; }
        .toc-grid a:hover { background:var(--gold-soft); border-color:var(--border); color:var(--gold); }
        .toc-grid .topic-count { color:var(--gold); font-size:0.78rem; opacity:0.8; }
        section.cat { background:var(--gray-darker); border:1px solid var(--border); border-radius:14px; padding:24px 26px 28px; margin:30px 0; }
        section.cat h2 { font-family:'Playfair Display',serif; color:var(--gold); font-size:1.7rem; margin:0 0 6px; display:flex; align-items:center; gap:10px; }
        section.cat h2 .count-pill { font-family:'Inter',sans-serif; font-size:0.85rem; background:var(--gold-soft); color:var(--gold); border:1px solid var(--border); padding:3px 10px; border-radius:999px; font-weight:500; }
        section.cat .cat-lead { color:var(--gray-light); font-style:italic; font-size:0.95rem; margin-bottom:18px; }
        .cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:10px; }
        .card { background:var(--gray-dark); border:1px solid rgba(212,175,55,0.08); border-radius:8px; padding:11px 14px; text-decoration:none; transition:all 0.18s; }
        .card:hover { border-color:var(--gold); background:var(--gold-soft); transform:translateY(-1px); }
        .card .word { color:var(--white); font-weight:600; font-size:0.95rem; }
        .card .slug { color:var(--gold); font-size:0.72rem; opacity:0.7; margin-top:2px; }
        .nav-back { margin-top:40px; text-align:center; }
        .nav-back a { color:var(--gold); text-decoration:none; font-weight:500; padding:10px 22px; border:1px solid var(--border); border-radius:999px; display:inline-block; transition:all 0.15s; }
        .nav-back a:hover { background:var(--gold-soft); }
        footer { margin-top:50px; text-align:center; color:var(--gray); font-size:0.82rem; padding-top:24px; border-top:1px solid var(--border); }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <a href="index.html">&larr; Back to Dictionary</a>
            <span>&middot;</span>
            <a href="by-topic.html">Browse by Topic</a>
            <span>&middot;</span>
            <a href="gen-z-decoded.html">Gen-Z Decoded</a>
            <span>&middot;</span>
            <a href="boomer-decoded.html">Boomer Decoded</a>
        </div>

        <h1>The Jesus Generation</h1>
        <p class="lead">The four generational decoders sort the world by dialect &mdash; Gen-Z, Millennial, Gen-X, Boomer. This directory does the opposite. It gathers the words of revival, prayer, new life, legacy, and worship around the one generation that gathers <em>every</em> age into itself: the generation that belongs to Jesus.</p>

        <div class="vision">
            <h2>The generation that unites</h2>
            <p>Every age has its slang, its idols, and its wounds, and the world is forever splitting us into camps that cannot understand one another. But there is a people not bounded by a decade or a demographic &mdash; a people of the gray-headed and the young together, &ldquo;willing in the day of thy power, in the beauties of holiness&rdquo; (Psalm 110:3). The dividing line is not the year you were born but the Lord you belong to.</p>
            <p>So this page is an attempted redemption of the generational divide: a reach across the gap to find the generation that unites. The old men dream dreams and the young men see visions by the same outpoured Spirit (Joel 2:28). Grandmother Lois, mother Eunice, and young Timothy hold one unfeigned faith (2 Timothy 1:5). The words below &mdash; revival and awakening, passionate prayer and consecration, first love and new life, legacy and the generations, unity and worship &mdash; are the marks of that one family.</p>
            <p class="credit">Inspired by Forrest Frank&#39;s &ldquo;The Jesus Generation&rdquo; tour &mdash; the songs, the story, and the hunger of a generation turning toward Christ. Curated under the <a href="../../DICTIONARY-VOICE-LOCK.md" style="color:var(--gold);">Doctrinal Voice Lock</a>.</p>
        </div>

        <div class="toc">
            <h2>In This Directory</h2>
            <div class="toc-grid">
{toc_links}
            </div>
        </div>

{sections}

        <div class="nav-back">
            <a href="index.html">&larr; Back to A-Z Dictionary</a>
        </div>

        <footer>
            The Jesus Generation &middot; MOOP Dictionary &middot; {total_entries} words across {section_count} themes &middot; <a href="../../DICTIONARY-VOICE-LOCK.md" style="color:var(--gold);">Doctrinal Voice Lock</a>
        </footer>
    </div>
</body>
</html>
"""


def get_headword(slug: str) -> str | None:
    p = DICT_DIR / f"{slug}.html"
    if not p.exists():
        return None
    try:
        text = p.read_text(encoding="utf-8")
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
        return m.group(1).strip() if m else slug
    except Exception:
        return slug


def render_card(slug: str) -> str:
    hw = get_headword(slug)
    if hw is None:
        return ""
    safe_hw = html.escape(hw)
    return (
        f'<a class="card" href="{slug}.html">'
        f'<div class="word">{safe_hw}</div>'
        f'<div class="slug">{slug}</div>'
        f'</a>'
    )


def main():
    print("Building docs/dictionary/jesus-generation.html...")
    sections_html = []
    toc_links_html = []
    total = 0
    sec_count = 0

    for anchor, title, lead, slugs in SECTIONS:
        cards = []
        rendered = 0
        for slug in slugs:
            c = render_card(slug)
            if c:
                cards.append(c)
                rendered += 1
            else:
                print(f"  WARN: missing slug for [{anchor}]: {slug}")
        if rendered == 0:
            continue
        sec_count += 1
        total += rendered
        cards_html = "\n            ".join(cards)
        section = (
            f'        <section class="cat" id="{anchor}">\n'
            f'            <h2>{title} <span class="count-pill">{rendered}</span></h2>\n'
            f'            <p class="cat-lead">{lead}</p>\n'
            f'            <div class="cards">\n'
            f'            {cards_html}\n'
            f'            </div>\n'
            f'        </section>\n'
        )
        sections_html.append(section)
        toc_links_html.append(
            f'                <a href="#{anchor}">{title} '
            f'<span class="topic-count">({rendered})</span></a>'
        )

    out = (PAGE_TEMPLATE
        .replace("{toc_links}", "\n".join(toc_links_html))
        .replace("{sections}", "\n".join(sections_html))
        .replace("{total_entries}", str(total))
        .replace("{section_count}", str(sec_count))
    )
    out_path = DICT_DIR / "jesus-generation.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"  Wrote {out_path}")
    print(f"  Themes: {sec_count}")
    print(f"  Total cards rendered: {total}")


if __name__ == "__main__":
    main()
