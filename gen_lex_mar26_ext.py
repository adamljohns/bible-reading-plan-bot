#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.expanduser("~/bible-reading-plan-bot"))

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")

# Reuse CSS/JS/NAV/make_page from main script by inlining needed parts
CSS = """        * { margin:0; padding:0; box-sizing:border-box; }
        :root { --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; --scarlet:#CC0000; }
        body { font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }
        h1,h2,h3 { font-family:'Playfair Display',serif; font-weight:700; }
        .container { max-width:800px; margin:0 auto; padding:20px; }
        nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }
        nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
        nav a:hover { color:var(--gold); border-color:var(--border); }
        nav a:link,nav a:visited,nav a:active { color:var(--gray) !important; text-decoration:none !important; }
        nav a.active { color:var(--gold) !important; border-color:var(--gold); }
        .word-header { text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }
        .strongs-badge { display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }
        .original-word { font-size:3rem; margin:15px 0 10px; color:var(--gold-light); }
        .transliteration { font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }
        .pos { color:var(--gray); font-size:0.95rem; margin-bottom:10px; }
        .gloss { color:var(--gold); font-size:1.1rem; font-weight:600; }
        .section { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }
        .section h2 { color:var(--gold); font-size:1.3rem; margin-bottom:16px; }
        .section p { color:var(--white); line-height:1.8; margin-bottom:12px; }
        .section p em { color:var(--gold-light); font-style:italic; }
        .section p strong { color:var(--white); }
        .verse-entry { margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }
        .verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }
        .verse-ref:hover { color:var(--gold-light); border-bottom-style:solid; }
        .verse-text { color:var(--white); line-height:1.7; }
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
        @media (max-width:640px) { .container { padding:15px; } .original-word { font-size:2.2rem; } }
        .theme-toggle{background:none;border:1px solid var(--border);border-radius:50%;width:34px;height:34px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:all 0.3s;padding:0;margin-left:6px;}.theme-toggle:hover{border-color:var(--gold);transform:scale(1.1);}body.light-mode{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}body.light-mode nav{background:rgba(250,248,245,0.97);}body.light-mode .section{background:#fff;border-color:#d4d0c8;}body.light-mode .ext-link{border-color:#d4d0c8;}body.light-mode .related-word{background:rgba(212,175,55,0.08);border-color:#d4d0c8;}body.light-mode footer{border-top-color:#d4d0c8;}"""
JS = """<script>function bteToggleTheme(){var b=document.body;if(b.classList.contains("light-mode")){b.classList.remove("light-mode");localStorage.setItem("bte-theme","dark");}else{b.classList.add("light-mode");localStorage.setItem("bte-theme","light");}}(function(){if(localStorage.getItem("bte-theme")==="light"){document.body.classList.add("light-mode");}})();</script>"""
NAV = """    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="position:fixed;top:12px;right:12px;z-index:9999;display:flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
        <span style="width:18px;text-align:center;">🌙</span>
        <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
        <span style="width:18px;text-align:center;">☀️</span>
    </div>"""

def make_page(strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related):
    lang_label = "Hebrew · Old Testament" if lang == "H" else "Greek · New Testament"
    num = strongs_id[1:]
    title = f"{strongs_id} — {translit} ({gloss})"
    direction = 'direction:rtl; ' if lang == 'H' else ''
    verses_html = ""
    for ref, text in verses:
        ref_url = ref.replace(" ", "+")
        verses_html += f"""                <div class="verse-entry">
                    <a href="../bible.html?ref={ref_url}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>\n"""
    related_html = ""
    for rel_id, rel_label in related:
        related_html += f'                    <a href="{rel_id}.html" class="related-word">{rel_id} — {rel_label}</a>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{strongs_id} — {translit} | USMC Ministries Lexicon">
    <meta property="og:description" content="{gloss} — {lang_label.split(' ·')[0]} word study. Strong's {strongs_id}.">
    <meta name="description" content="{gloss} — {lang_label.split(' ·')[0]} word study. Strong's {strongs_id}. USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{title} | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
{CSS}
    </style>
</head>
<body>
{NAV}
    <div class="container">
        <a href="../lexicon.html" class="back-link">← Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">{strongs_id} · {lang_label}</span>
            <div class="original-word" style="{direction}">{script}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{definition}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{theology}</p>
        </div>
        <div class="section">
            <h2>Key Bible Verses</h2>
{verses_html}        </div>
        <div class="section">
            <h2>Related Words</h2>
            <div class="related-words">
{related_html}            </div>
        </div>
        <div class="section">
            <h2>External Resources</h2>
            <div class="ext-links">
                <a href="https://www.stepbible.org/?q=strong={strongs_id}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/{strongs_id.lower()}/kjv/wlc/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/{'greek' if lang == 'G' else 'hebrew'}/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>
            </div>
        </div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">© 2026 <a href="../index.html">U.S.M.C. Ministries</a> · <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
{JS}
</body>
</html>"""

EXTRA = [
("H940", "H", "בֻּזִי", "Buzi", "Proper noun — Person", "Contemptible / Son of Buz",
 "<em>Buzi</em> is the name of the father of the prophet Ezekiel. The name likely derives from the root <em>buz</em> (H936), meaning contempt, though some read it as a tribal/regional name. Ezekiel identifies himself as 'Ezekiel son of Buzi, the priest' (Ezekiel 1:3).",
 "The name of a prophet's father may seem unremarkable, but it grounds Ezekiel's identity in both priestly lineage and historical location. Ezekiel is the only prophet to identify himself by his father's name alongside priestly status, emphasizing the legitimacy of his call. He received his visions 'in the land of the Babylonians by the Kebar River' — in exile, far from Jerusalem. That God would speak to <em>Buzi's</em> son in Babylon declares that exile does not terminate revelation. The word of the Lord comes in unexpected places to prepared hearts. Priestly lineage combined with prophetic call pictures the ultimate priest-prophet, Jesus Christ.",
 [("Ezekiel 1:3", "The word of the Lord came to Ezekiel the priest, son of <em>Buzi</em>, in the land of the Babylonians by the Kebar River."),
  ("Ezekiel 1:1", "In my thirtieth year, in the fourth month on the fifth day, while I was among the exiles by the Kebar River, the heavens were opened and I saw visions of God."),
  ("Jeremiah 1:5", "Before I formed you in the womb I knew you, before you were born I set you apart; I appointed you as a prophet to the nations."),
  ("Acts 2:17", "In the last days, God says, I will pour out my Spirit on all people. Your sons and daughters will prophesy."),
  ("Hebrews 1:1", "In the past God spoke to our ancestors through the prophets at many times and in various ways.")],
 [("H3168", "Yechezqel — Ezekiel"), ("H3548", "Kohen — Priest"), ("H5030", "Nabi — Prophet")]),

("H941", "H", "בּוּזִי", "Buzi (adj.)", "Adjective / Gentillic", "Of Buz / Buzite",
 "The Hebrew term <em>Buzi</em> as an adjective/gentillic refers to someone from the region or clan of Buz — a descendant of Buz, son of Nahor (Abraham's brother). In Job 32:2, Elihu is identified as a Buzite, connecting him to this Arabian tribal background.",
 "Elihu the Buzite is one of Job's most theologically interesting interlocutors. Unlike the three friends who are rebuked by God, Elihu's speeches are not explicitly condemned. His identification as a Buzite (from the line of Abraham's extended family) gives him a non-Israelite yet covenant-adjacent perspective. Elihu speaks of God's sovereignty in suffering with greater nuance than the three friends — approaching the divine perspective that God Himself will deliver. Theologically, <em>Buzi</em> reminds us that wisdom is not confined to one nation; God's truth can be found among those outside the central covenant line, a hint of the breadth of God's common grace.",
 [("Job 32:2", "But Elihu son of Barakel the Buzite, of the family of Ram, became very angry with Job."),
  ("Genesis 22:21", "Uz the firstborn, Buz his brother, Kemuel the father of Aram."),
  ("Job 32:6", "So Elihu son of Barakel the Buzite said: 'I am young in years, and you are old; that is why I was fearful, not daring to tell you what I know.'"),
  ("Proverbs 2:6", "For the Lord gives wisdom; from his mouth come knowledge and understanding."),
  ("Job 37:22", "Out of the north he comes in golden splendor; God comes in awesome majesty.")],
 [("H936", "Buz — Contempt"), ("H347", "Iyov — Job"), ("H1681", "Dibbah — Evil Report")]),
]

created = 0
for entry in EXTRA:
    strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related = entry
    fname = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    if os.path.exists(fname):
        print(f"  SKIP {strongs_id} (exists)")
        continue
    html = make_page(strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    created += 1
    print(f"  ✓ {strongs_id} — {gloss}")

print(f"\nExtra words created: {created}")
