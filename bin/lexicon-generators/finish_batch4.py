#!/usr/bin/env python3
"""Append last 2 entries + generation code to gen_batch4.py, then run it."""
import os

TAIL = '''    ("G5207","Greek","New Testament","\\u03c5\\u1f31\\u03cc\\u03c2","huios","Noun, masculine","son, descendant, heir",
     "Son in both biological and covenantal senses. Jesus is the Son of God \\u2014 a relational title expressing unique divine relationship and messianic identity. Believers become sons through adoption (huiothesia).",
     "The title Son of God is primarily relational and covenantal. Hebrews 1 argues the Son's superiority to angels; John 1 identifies him as the eternal Son. Adoption makes believers full heirs.",
     [("Matthew 3:17","This is my beloved <em>Son</em> [huios], with whom I am well pleased."),
      ("Galatians 4:4-5","God sent forth his <em>Son</em> [huios]...so that we might receive adoption as <em>sons</em> [huios]."),
      ("Romans 8:14","For all who are led by the Spirit of God are <em>sons</em> [huios] of God.")],
     "Galatians 4:4-5 is the gospel in miniature: Son sent, born under law, to redeem, to adopt. We become sons because he became the Son incarnate.",
     [("G5043","G5043 \\u2014 teknon (child)"),("G2316","G2316 \\u2014 theos (God)")],
     "g5207"),

    ("G5293","Greek","New Testament","\\u1f51\\u03c0\\u03bf\\u03c4\\u03ac\\u03c3\\u03c3\\u03c9","hupotasso","Verb","to submit, be subject to, subordinate",
     "To arrange under \\u2014 a military term for ordering troops under a commander. Used of wives/husbands, citizens/government, Jesus/Father. Submission is relational order, not ontological inferiority.",
     "The NT submission ethic is rooted in the Trinity: the Son submits to the Father not because he is less divine but as a relational pattern. Mutual submission (Eph 5:21) precedes all specific applications.",
     [("Ephesians 5:21","<em>Submitting</em> [hupotasso] to one another out of reverence for Christ."),
      ("Romans 13:1","Let every person be <em>subject</em> [hupotasso] to the governing authorities."),
      ("1 Corinthians 15:28","The Son himself will also be <em>subjected</em> [hupotasso] to him who put all things in subjection under him.")],
     "1 Corinthians 15:28 \\u2014 the Son's eternal submission \\u2014 is relational order in the eschatological kingdom. Submission in the NT is always voluntary, purposeful, and dignifying.",
     [("G5218","G5218 \\u2014 hupakoe (obedience)"),("G1849","G1849 \\u2014 exousia (authority)")],
     "g5293"),
]
'''

GENERATION = '''

def make_page(strongs, lang, testament, original, translit, pos, gloss,
              definition, usage, verses, word_study, related, blb_id):
    lang_label = "Hebrew" if lang == "Hebrew" else "Greek"
    ext_links = f\'\'\'<a href="https://www.stepbible.org/?q=strong={strongs}" target="_blank" class="ext-link">\\U0001f4d6 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/{blb_id}/kjv/tr/0-1/" target="_blank" class="ext-link">\\U0001f4d8 Blue Letter Bible</a>\'\'\'

    verse_html = ""
    for ref, text in verses:
        url_ref = ref.replace(" ", "+")
        verse_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={url_ref}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>"""

    related_html = ""
    for rid, rlabel in related:
        related_html += f\'<a href="{rid}.html" class="related-word">{rlabel}</a>\\n                    \'

    css = """* { margin:0; padding:0; box-sizing:border-box; }
        :root { --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }
        body { font-family:\'Inter\',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }
        h1,h2,h3 { font-family:\'Playfair Display\',serif; font-weight:700; }
        .container { max-width:800px; margin:0 auto; padding:20px; }
        nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }
        nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
        nav a:hover { color:var(--gold); border-color:var(--border); }
        nav a:link,nav a:visited,nav a:active { color:var(--gray) !important; text-decoration:none !important; }
        nav a.active { color:var(--gold) !important; border-color:var(--gold); }
        .word-header { text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }
        .strongs-badge { display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }
        .original-word { font-size:3rem; margin:15px 0 10px; color:var(--gold-light); direction:ltr; }
        .transliteration { font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }
        .pos { color:var(--gray); font-size:0.95rem; margin-bottom:10px; }
        .gloss { color:var(--gold); font-size:1.1rem; font-weight:600; }
        .section { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }
        .section h2 { color:var(--gold); font-size:1.3rem; margin-bottom:16px; }
        .section p { color:var(--gray); line-height:1.8; margin-bottom:12px; }
        .section p em { color:var(--gold-light); font-style:italic; }
        .section p strong { color:var(--white); }
        .verse-entry { margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }
        .verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:block; margin-bottom:4px; border-bottom:1px dotted var(--gold); display:inline-block; }
        .verse-ref:hover { color:var(--gold-light); border-bottom-style:solid; }
        .verse-text { color:var(--gray); line-height:1.7; }
        .verse-text em { color:var(--gold-light); font-style:italic; }
        .verse-text strong { color:var(--white); }
        .related-words { display:flex; flex-wrap:wrap; gap:10px; }
        .related-word { display:inline-block; background:rgba(212,175,55,0.1); border:1px solid var(--border); color:var(--gold); text-decoration:none; padding:6px 14px; border-radius:20px; font-size:0.85rem; transition:all 0.2s; }
        a.related-word:hover { border-color:var(--gold); background:rgba(212,175,55,0.2); }
        .ext-links { display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }
        .ext-link { color:var(--gold); text-decoration:none; padding:8px 18px; border:1px solid var(--border); border-radius:8px; font-size:0.9rem; transition:all 0.2s; }
        .ext-link:hover { border-color:var(--gold); background:rgba(212,175,55,0.1); }
        .back-link { display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }
        .back-link:hover { color:var(--gold-light); }
        footer { text-align:center; padding:40px 20px; color:var(--gray); font-size:0.85rem; border-top:1px solid var(--border); margin-top:40px; }
        footer a { color:var(--gold); text-decoration:none; }
        @media (max-width:640px) { .container { padding:15px; } .original-word { font-size:2.2rem; } }"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{strongs} \\u2014 {translit} | USMC Ministries Lexicon">
    <meta property="og:description" content="{gloss} \\u2014 {lang_label} word study. Strong\'s {strongs}.">
    <meta name="description" content="{gloss} \\u2014 {lang_label} word study. Strong\'s {strongs}. USMC Ministries Lexicon.">
    <title>{strongs} \\u2014 {translit} ({gloss}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div class="container">
        <a href="../lexicon.html" class="back-link">\\u2190 Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">{strongs} \\u00b7 {lang_label} \\u00b7 {testament}</span>
            <div class="original-word">{original}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section"><h2>Definition</h2><p>{definition}</p></div>
        <div class="section"><h2>Usage &amp; Theological Significance</h2><p>{usage}</p></div>
        <div class="section"><h2>Key Bible Verses</h2>{verse_html}</div>
        <div class="section"><h2>Word Study</h2><p>{word_study}</p></div>
        <div class="section"><h2>Related Words</h2><div class="related-words">{related_html}</div></div>
        <div class="section"><h2>External Resources</h2><div class="ext-links">{ext_links}</div></div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">\\u00a9 2026 <a href="../index.html">U.S.M.C. Ministries</a> \\u00b7 <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
</body>
</html>"""

OUT = "/Users/adamjohns/bible-reading-plan-bot/docs/lexicon"
count = 0
for w in WORDS:
    strongs = w[0]
    path = os.path.join(OUT, f"{strongs}.html")
    page = make_page(*w)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    count += 1

print(f"Generated {count} pages in {OUT}")
'''

# Read the truncated file
with open("/Users/adamjohns/bible-reading-plan-bot/docs/lexicon/gen_batch4.py", "r") as f:
    content = f.read()

# Find the incomplete G5207 entry and cut there
cut_at = content.rfind('    ("G5207')
trimmed = content[:cut_at]

# Write the complete file
with open("/Users/adamjohns/bible-reading-plan-bot/docs/lexicon/gen_batch4.py", "w") as f:
    f.write(trimmed + TAIL + GENERATION)

print("gen_batch4.py rebuilt successfully")
