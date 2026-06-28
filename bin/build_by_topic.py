#!/usr/bin/env python3
"""Generate docs/dictionary/by-topic.html.

The page groups dictionary entries by doctrinal category so readers can
browse by theology rather than alphabetically. The categorization is
hand-curated (editorial decisions about which entries are most useful
under each category), not auto-derived.

When entries are added or renamed, edit CATEGORIES below and re-run:
    python3 bin/build_by_topic.py

Then commit docs/dictionary/by-topic.html along with the change.
"""
from __future__ import annotations

import html
import os
from pathlib import Path

DICT_DIR = Path(__file__).resolve().parent.parent / "docs" / "dictionary"

# ---------------------------------------------------------------------------
# Categorized entries. Each tuple: (anchor, title, lead, [slugs]).
# The script verifies each slug exists; missing slugs print a warning and
# are skipped (the page still builds).
# ---------------------------------------------------------------------------

CATEGORIES = [
    (
        "theology-proper", "Theology Proper",
        "God's nature, attributes, eternal decree, and Trinitarian existence.",
        [
            "trinity", "sovereignty", "aseity", "immutability", "impassibility",
            "divine-simplicity", "omniscience", "omnipotence", "omnipresence",
            "holiness", "eternal-decree", "decree-of-god", "providence",
            "eternal-generation", "eternal-procession", "perichoresis",
            "i-am-that-i-am", "the-almighty", "most-high", "holy-one-of-israel",
        ],
    ),
    (
        "christology", "Christology",
        "The Person and Work of Christ &mdash; one Person, two natures, the eternal Son incarnate.",
        [
            "hypostatic-union", "communicatio-idiomatum", "extra-calvinisticum",
            "incarnation", "virgin-birth", "active-obedience", "passive-obedience",
            "imputed-righteousness", "atonement", "definite-atonement", "limited-atonement",
            "propitiation", "substitution", "mediator", "resurrection", "ascension",
            "session", "light-of-the-world", "resurrection-and-life", "branch-of-the-lord",
            "word-made-flesh", "logos-doctrine", "only-begotten-doctrine",
            "captain-of-our-salvation", "ancient-of-days-doctrine",
        ],
    ),
    (
        "soteriology", "Soteriology",
        "Salvation &mdash; the five solas, TULIP, and the <em>ordo salutis</em>.",
        [
            "sola-scriptura", "sola-fide", "sola-gratia", "solus-christus",
            "soli-deo-gloria", "five-solas",
            "total-depravity", "unconditional-election", "limited-atonement",
            "irresistible-grace", "perseverance-of-the-saints", "tulip",
            "ordo-salutis", "regeneration", "effectual-calling", "faith",
            "repentance", "justification", "adoption", "sanctification",
            "glorification", "imputation", "election", "predestination",
            "reprobation", "common-grace", "special-grace",
        ],
    ),
    (
        "ecclesiology-sacraments", "Ecclesiology &amp; Sacraments",
        "The church, her offices, ordinances, worship, and means of grace.",
        [
            "church", "local-church-doctrine", "elder", "deacon", "pastor",
            "regulative-principle", "means-of-grace", "lords-supper-doctrine",
            "baptism", "ordinance", "discipline", "membership",
            "westminster-confession-of-faith", "lbcf", "heidelberg-catechism",
            "westminster-shorter-catechism", "second-helvetic-confession",
            "book-of-common-prayer", "apostolic-fathers",
        ],
    ),
    (
        "eschatology", "Eschatology",
        "Last things &mdash; the bodily return of Christ, resurrection, final judgment, eternal heaven and hell.",
        [
            "second-coming", "resurrection", "final-judgment", "heaven", "hell",
            "millennium", "amillennialism", "postmillennialism", "premillennialism",
            "already-not-yet", "kingdom-of-god", "new-jerusalem", "new-heavens-and-new-earth",
        ],
    ),
    (
        "anthropology-order", "Anthropology &amp; Biblical Order",
        "Humanity, sin, the imago Dei, and the creational order of headship and submission.",
        [
            "imago-dei", "image-of-god", "original-sin", "fall",
            "biblical-order", "biblical-egalitarianism", "complementarianism",
            "marriage", "biblical-manhood", "biblical-masculinity", "biblical-fraternity",
            "biblical-sexuality", "homosexuality", "transgender",
            "feminism", "patriarch", "headship",
        ],
    ),
    (
        "biblical-figures", "Biblical Figures",
        "Persons in the canonical record &mdash; patriarchs, prophets, kings, apostles, and faithful witnesses.",
        [
            "abraham", "isaac", "jacob", "joseph", "moses", "joshua-figure",
            "samuel", "david", "solomon", "elijah", "elisha-prophet",
            "isaiah-prophet", "jeremiah-prophet", "daniel-prophet", "ezekiel-prophet",
            "hosea-prophet", "amos-prophet", "jonah-prophet", "micah-prophet",
            "jehoshaphat", "hezekiah", "josiah", "amaziah", "jotham", "ahaz", "amon",
            "athaliah", "omri", "ahab", "jehu", "jeroboam", "jeroboam-ii", "hoshea",
            "peter", "paul", "john", "matthew-apostle", "mark-book", "luke",
            "stephen", "philip-evangelist", "barnabas", "timothy", "titus-doctrine",
            "priscilla-and-aquila", "lydia", "tabitha",
            "ruth", "esther", "hadassah", "anna-the-prophetess", "mary",
        ],
    ),
    (
        "corruption-correctors", "Corruption-Correctors",
        "Postmodern, progressive, charismatic, historical-critical, and other contemporary frameworks named and rebutted on Reformed-confessional biblical grounds.",
        [
            "critical-race-theory", "affirming-theology", "queer-theology",
            "side-a", "side-b", "homosexuality", "transgender", "feminism",
            "biblical-egalitarianism",
            "moral-therapeutic-deism", "progressive-christianity", "deconstruction",
            "exvangelical", "emerging-church", "emergent-church",
            "higher-criticism", "documentary-hypothesis", "theological-liberalism",
            "open-theism", "process-theology", "new-perspective-on-paul",
            "federal-vision", "word-of-faith", "prosperity-gospel",
            "new-apostolic-reformation", "signs-and-wonders", "bethel",
            "seeker-sensitive", "purpose-driven", "church-growth-movement",
            "spiritual-but-not-religious", "mainline-protestantism", "social-gospel",
            "vatican-ii", "ecumenism", "dominionism", "woke-evangelicalism",
            "finneyism", "hyper-calvinism", "antinomianism",
            "pelagianism", "semi-pelagianism", "arianism", "modalism", "socinianism",
        ],
    ),
    (
        "reformed-tradition", "Reformed Tradition",
        "Reformers, Puritans, confessions, and the Reformed-confessional theological line.",
        [
            "luther", "calvin", "zwingli", "bullinger", "melanchthon", "knox",
            "cranmer", "latimer", "ridley", "tyndale", "jan-hus", "wycliffe", "savonarola",
            "owen", "baxter", "sibbes", "spurgeon", "edwards", "whitefield",
            "william-perkins", "thomas-watson", "thomas-goodwin", "bunyan",
            "wesley", "wesleyan",
            "westminster-confession-of-faith", "lbcf", "heidelberg-catechism",
            "second-helvetic-confession", "canons-of-dort", "thirty-nine-articles",
            "five-solas", "tulip",
        ],
    ),
    (
        "christian-tradition", "Christian Tradition (Pre-Reformation)",
        "Apostolic fathers, ancient martyrs, medieval saints &mdash; honored where honor is due, doctrinally engaged on confessional grounds.",
        [
            "ignatius", "polycarp", "irenaeus", "tertullian", "cyprian",
            "athanasius", "augustine", "ambrose", "jerome", "chrysostom",
            "basil-the-great", "gregory-the-great",
            "bernard-of-clairvaux", "anselm", "aquinas", "bonaventure",
            "catherine-of-siena", "teresa-of-avila",
            "cecilia", "perpetua", "lucy", "monica", "patrick",
            "felicity", "agnes",
        ],
    ),
    (
        "biblical-realia", "Biblical Realia",
        "Objects, weights, measures, plants, animals, and material culture of the canonical text.",
        [
            "shekel", "talent", "cubit", "mite", "stater", "denarius", "drachma",
            "laver", "shewbread", "spikenard", "onyx", "psaltery",
            "ark-of-the-covenant", "mercy-seat", "candlestick",
            "veil-of-the-temple", "mitre", "girdle", "urim-and-thummim",
            "breastplate-of-judgment", "ephod", "red-heifer",
            "sword-of-the-spirit", "helmet-of-salvation", "breastplate-of-righteousness",
            "buckler", "bow-and-arrow", "yoke-doctrine", "potter-and-clay",
            "vine", "shepherd-and-sheep", "lamb", "lion",
            "dove", "balm-of-gilead", "serpent", "raven",
            "almond-tree",
            "jasper", "sapphire", "chalcedony", "emerald", "sardonyx", "sardius",
            "chrysolite", "beryl", "topaz", "chrysoprasus", "jacinth", "amethyst",
            "carbuncle", "pearl", "cornerstone-doctrine", "gold-bible",
            "silver-bible", "brass-bible", "iron-bible",
        ],
    ),
]

PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>MOOP Dictionary &mdash; Browse by Topic</title>
    <meta name="description" content="MOOP Dictionary entries grouped by doctrinal category &mdash; theology proper, Christology, soteriology, eschatology, biblical figures, corruption-correctors, Reformed tradition, Christian tradition, biblical realia.">
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
        .topbar { display:flex; align-items:center; gap:14px; font-size:0.85rem; color:var(--gray-light); margin-bottom:30px; }
        .topbar a { color:var(--gold); text-decoration:none; }
        .topbar a:hover { text-decoration:underline; }
        h1 { font-family:'Playfair Display',serif; color:var(--gold); font-size:2.4rem; margin:0 0 8px; }
        .lead { color:var(--gray-light); font-size:1.05rem; margin-bottom:24px; }
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
            <a href="baby-names.html">Baby Names</a>
            <span>&middot;</span>
            <a href="names.html">Biblical Names</a>
            <span>&middot;</span>
            <a href="doctrinal-anchors.html">Doctrinal Anchors</a>
        </div>

        <h1>Browse by Topic</h1>
        <p class="lead">The MOOP Dictionary grouped by doctrinal category &mdash; theology proper, Christology, soteriology, eschatology, biblical figures, corruption-correctors, Reformed tradition, Christian tradition (pre-Reformation), and biblical realia. Editorial curation under the <a href="../../DICTIONARY-VOICE-LOCK.md" style="color:var(--gold);">Doctrinal Voice Lock</a>.</p>

        <div class="toc">
            <h2>Table of Contents</h2>
            <div class="toc-grid">
{toc_links}
            </div>
        </div>

{sections}

        <div class="nav-back">
            <a href="index.html">&larr; Back to A-Z Dictionary</a>
        </div>

        <footer>
            MOOP Dictionary &mdash; Browse by Topic &middot; {total_entries} entries across {category_count} categories &middot; <a href="../../DICTIONARY-VOICE-LOCK.md" style="color:var(--gold);">Doctrinal Voice Lock</a>
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
        import re
        text = p.read_text(encoding="utf-8")
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
        if m:
            return m.group(1).strip()
        return slug
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
    print("Building docs/dictionary/by-topic.html...")
    sections_html = []
    toc_links_html = []
    total = 0
    cat_count = 0

    for anchor, title, lead, slugs in CATEGORIES:
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
        cat_count += 1
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
        .replace("{category_count}", str(cat_count))
    )
    out_path = DICT_DIR / "by-topic.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"  Wrote {out_path}")
    print(f"  Categories: {cat_count}")
    print(f"  Total cards rendered: {total}")


if __name__ == "__main__":
    main()
