#!/usr/bin/env python3
"""Generate Lexicon Batch 4 — 24 Hebrew + 23 Greek word pages."""

import json, os, re
from datetime import datetime, timezone

OUT = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")
MANIFEST = os.path.expanduser("~/bible-reading-plan-bot/docs/assets/lexicon-manifest.json")

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
        .original-word { font-size:3rem; margin:15px 0 10px; color:var(--gold-light); direction:rtl; }
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

        @media (max-width:640px) { .container { padding:15px; } .original-word { font-size:2.2rem; } }
    .theme-toggle{background:none;border:1px solid var(--border);border-radius:50%;width:34px;height:34px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:all 0.3s;padding:0;margin-left:6px;}.theme-toggle:hover{border-color:var(--gold);transform:scale(1.1);}body.light-mode{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}body.light-mode nav{background:rgba(250,248,245,0.97);}body.light-mode .section{background:#fff;border-color:#d4d0c8;}body.light-mode .ext-link{border-color:#d4d0c8;}body.light-mode .related-word{background:rgba(212,175,55,0.08);border-color:#d4d0c8;}body.light-mode footer{border-top-color:#d4d0c8;}"""

JS = """<script>function toggleTheme(){var b=document.body,t=document.getElementById("themeToggle");if(b.classList.contains("light-mode")){b.classList.remove("light-mode");t.textContent="🌙";localStorage.setItem("bte-theme","dark");}else{b.classList.add("light-mode");t.textContent="☀️";localStorage.setItem("bte-theme","light");}}(function(){if(localStorage.getItem("bte-theme")==="light"){document.body.classList.add("light-mode");var t=document.getElementById("themeToggle");if(t)t.textContent="☀️";}})();</script>"""

def make_html(entry):
    sid = entry["strongs"]
    lang = "Hebrew" if sid.startswith("H") else "Greek"
    testament = "Old Testament" if lang == "Hebrew" else "New Testament"
    num = sid[1:]
    dir_attr = ' direction:rtl;' if lang == "Hebrew" else ''

    verses_html = ""
    for v in entry["verses"]:
        verses_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={v['ref'].replace(' ','+')}" class="verse-ref">{v['ref']}</a>
                    <span class="verse-text">{v['text']}</span>
                </div>"""

    related_html = ""
    for r in entry["related"]:
        rcode = r.split(" ")[0]
        rfile = f"{rcode}.html"
        import os as _os
        rpath = _os.path.join(OUT, rfile)
        if _os.path.exists(rpath):
            related_html += f'\n                    <a href="{rfile}" class="related-word">{r}</a>'
        else:
            related_html += f'\n                    <span class="related-word">{r}</span>'

    step_url = f"https://www.stepbible.org/?q=strong={sid}"
    blb_url = f"https://www.blueletterbible.org/lexicon/{sid.lower()}/kjv/wlc/0-1/"
    bh_url = f"https://biblehub.com/{'hebrew' if lang=='Hebrew' else 'greek'}/{num}.htm"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{sid} — {entry['transliteration']} ({entry['gloss']}) | USMC Ministries Lexicon">
    <meta property="og:description" content="{entry['short_def']} — {lang} word study from the {testament}. Strong's {sid}.">
    <meta name="description" content="{entry['short_def']} — {lang} word study. Strong's {sid}. USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{sid} — {entry['transliteration']} ({entry['gloss']}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
{CSS}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
        <button class="theme-toggle" onclick="toggleTheme()" title="Toggle dark/light mode" id="themeToggle">🌙</button>
    </nav>

    <div class="container">
        <a href="../lexicon.html" class="back-link">← Back to Lexicon</a>

        <div class="word-header">
            <span class="strongs-badge">{sid} · {lang} · {testament}</span>
            <div class="original-word" style="{dir_attr}">{entry['original']}</div>
            <div class="transliteration">{entry['transliteration']}</div>
            <div class="pos">{entry['pos']}</div>
            <div class="gloss">{entry['gloss']}</div>
        </div>

        <div class="section">
            <h2>Definition</h2>
            <p>{entry['full_def']}</p>
        </div>

        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{entry['theology']}</p>
        </div>

        <div class="section">
            <h2>Key Bible Verses</h2>
            {verses_html}
        </div>

        <div class="section">
            <h2>Word Study</h2>
            <p>{entry['word_study']}</p>
        </div>

        <div class="section">
            <h2>Related Words</h2>
            <div class="related-words">
                    {related_html}
                    
            </div>
        </div>

        <div class="section">
            <h2>External Resources</h2>
            <div class="ext-links">
                <a href="{step_url}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="{blb_url}" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="{bh_url}" target="_blank" class="ext-link">📗 Bible Hub (Interlinear + HELPS)</a>
            </div>
        </div>
    </div>

    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">© 2026 <a href="../index.html">U.S.M.C. Ministries</a> · <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
{JS}</body>
</html>"""

# ============================================================
# DATA
# ============================================================

ENTRIES = [

# ==================== HEBREW ====================

{
  "strongs": "H117",
  "original": "אַדִּיר",
  "transliteration": "addir",
  "pos": "Adjective",
  "gloss": "mighty, majestic, noble",
  "short_def": "Powerful, magnificent, of exalted rank or force",
  "full_def": "<em>Addir</em> (אַדִּיר) means <strong>mighty, majestic, noble, or glorious</strong>. It derives from the root <em>adar</em> (H142), meaning to be great or wide. It is applied to people of high rank, to powerful waters, and—most significantly—to God Himself in His transcendent majesty. It describes both the awe-inspiring greatness of nature and the surpassing majesty of the Lord.",
  "theology": "<em>Addir</em> is used to glorify God's incomparable greatness. In Psalm 8, the psalmist declares that God's name is <em>addir</em> throughout all the earth. The word captures what theologians call the <strong>numinous</strong>—God's awesome, overwhelming majesty that surpasses all created power. It appears alongside words for glory and honor, indicating it is a term of the highest praise. It also describes the future Messianic ruler in Micah 5:2's context as the one whose goings are from everlasting.",
  "verses": [
    {"ref": "Psalm 8:1", "text": "LORD, our Lord, how <em>majestic</em> [addir] is your name in all the earth!"},
    {"ref": "Psalm 93:4", "text": "More <em>mighty</em> [addir] than the thunders of many waters, more mighty than the waves of the sea, the LORD on high is mighty!"},
    {"ref": "Isaiah 33:21", "text": "There the <em>majestic</em> [addir] LORD will be for us a place of broad rivers and streams."},
    {"ref": "Psalm 76:4", "text": "You are <em>glorious</em> [addir], more majestic than the mountains full of prey."},
    {"ref": "Exodus 15:10", "text": "You blew with your wind; the sea covered them; they sank like lead in the <em>mighty</em> [addir] waters."},
  ],
  "word_study": "The root <em>adar</em> suggests spreading out in greatness, like a wide river or a great cloak. <em>Addir</em> is used 27 times in the OT, applied to lions (Zechariah 11:3), cedar trees (Ezekiel 17:23), mighty men (Judges 5:13), and above all to God. The LXX (Greek Septuagint) typically translates it as <em>krateros</em> (mighty) or <em>megaloprepes</em> (magnificent). In Christian theology, it prefigures Christ, who is praised as the King of glory — majestic above all rulers.",
  "related": ["H430 — Elohim (God)", "H1419 — gadol (great)", "H3519 — kabod (glory)", "H6944 — qodesh (holiness)"]
},

{
  "strongs": "H369",
  "original": "אַיִן",
  "transliteration": "ayin",
  "pos": "Particle of negation / noun",
  "gloss": "nothing, there is not, nothingness",
  "short_def": "Non-existence, the absence of something, nothing",
  "full_def": "<em>Ayin</em> (אַיִן) is a particle expressing <strong>non-existence or absence</strong>. It functions as a negative existential — 'there is no…' or 'without.' It occurs over 700 times in the Old Testament. It may be related to a root meaning 'where?' suggesting the absence of that which is sought. It is the direct antithesis of <em>yesh</em> (there is), and is foundational for understanding Hebrew concepts of nothingness, non-being, and the vanity of idols.",
  "theology": "Theologically, <em>ayin</em> is central to understanding the <strong>incomparability of God</strong>. Isaiah repeatedly uses it to declare that before God there is no other god — 'before me there was no God formed, nor shall there be after me' (Isaiah 43:10). Idols are called <em>ayin</em> — nothingness. This profoundly shapes monotheism: other 'gods' do not merely lack power; they lack <em>being</em>. Creation <em>ex nihilo</em> (from nothing) is also implied: before God's creative word, there was only <em>ayin</em>.",
  "verses": [
    {"ref": "Isaiah 40:17", "text": "All the nations are as <em>nothing</em> [ayin] before him; they are accounted by him as less than nothing and emptiness."},
    {"ref": "Psalm 39:5", "text": "Surely all mankind stands as <em>nothing</em> [ayin] before you! Surely a man goes about as a shadow."},
    {"ref": "Isaiah 44:6", "text": "I am the first and I am the last; besides me there is <em>no</em> [ayin] God."},
    {"ref": "Proverbs 13:7", "text": "One pretends to be rich, yet has <em>nothing</em> [ayin]; another pretends to be poor, yet has great wealth."},
    {"ref": "Genesis 2:5", "text": "There was <em>no</em> [ayin] bush of the field yet in the land... and there was no man to work the ground."},
  ],
  "word_study": "<em>Ayin</em> is closely related to the Akkadian <em>ayanu</em> and Ugaritic <em>in</em>, both meaning 'there is not.' Its opposite, <em>yesh</em> (H3426), means 'there is.' Together they form the basic existential vocabulary of Hebrew thought. The word appears in poetry, prophecy, and narrative with powerful rhetorical force: reducing mighty empires, proud idols, and human strength to utter nothingness before the eternal God. This aligns with NT teaching that all things are 'from him and through him and to him' (Romans 11:36).",
  "related": ["H3426 — yesh (there is)", "H5769 — olam (eternity)", "H7385 — riq (emptiness, vanity)", "H430 — Elohim"]
},

{
  "strongs": "H428",
  "original": "אֵלֶּה",
  "transliteration": "elleh",
  "pos": "Demonstrative pronoun",
  "gloss": "these",
  "short_def": "Plural demonstrative pronoun — these things, these people",
  "full_def": "<em>Elleh</em> (אֵלֶּה) is the plural demonstrative pronoun meaning <strong>'these'</strong>. It points to things or persons near at hand (in contrast to remote ones). It appears over 700 times in the Old Testament and is used in narrative, poetry, law, and prophecy. It is distinct from the singular <em>zeh</em> (this) and <em>zo't</em> (this, feminine). In many pivotal biblical passages, <em>elleh</em> introduces solemn lists, covenant stipulations, genealogies, and acts of God.",
  "theology": "While grammatically a simple pronoun, <em>elleh</em> carries theological weight in context. The phrase <em>'elleh toldot'</em> ('these are the generations/records of') is the structural backbone of Genesis, introducing the sacred history of creation and covenant. The word also appears in theophanic moments: 'These are the statutes and ordinances which the LORD commanded' — pointing to the divine law as concrete, proximate, and binding. It frames Israel's history as specific, particular acts of God in real time.",
  "verses": [
    {"ref": "Genesis 2:4", "text": "<em>These</em> [elleh] are the generations of the heavens and the earth when they were created."},
    {"ref": "Deuteronomy 4:45", "text": "<em>These</em> [elleh] are the testimonies, the statutes, and the rules that Moses spoke to the people of Israel."},
    {"ref": "Isaiah 40:26", "text": "Lift up your eyes on high and see: who created <em>these</em> [elleh]? He who brings out their host by number."},
    {"ref": "Psalm 73:12", "text": "Behold, <em>these</em> [elleh] are the wicked; always at ease, they increase in riches."},
    {"ref": "Numbers 3:1", "text": "<em>These</em> [elleh] are the generations of Aaron and Moses at the time when the LORD spoke with Moses on Mount Sinai."},
  ],
  "word_study": "<em>Elleh</em> derives from the demonstrative particle <em>el</em> (toward, that direction) with a plural suffix. The related Aramaic form is <em>illen</em>. The phrase <em>elleh divrei</em> ('these are the words') opens Deuteronomy, marking Moses' final addresses as authoritative and complete. In Revelation language, John parallels this formula: 'These are the words of him who holds the seven stars' — pointing to the continuing authority of God's word across both testaments.",
  "related": ["H2088 — zeh (this)", "H834 — asher (which, that)", "H3605 — kol (all, every)", "H1697 — dabar (word)"]
},

{
  "strongs": "H505",
  "original": "אֶלֶף",
  "transliteration": "eleph",
  "pos": "Noun masculine / numeral",
  "gloss": "thousand, clan",
  "short_def": "One thousand; also a military or tribal unit (clan, squad)",
  "full_def": "<em>Eleph</em> (אֶלֶף) means <strong>one thousand</strong>, but it has a second, related meaning: a <strong>tribal subdivision or clan</strong> — a unit of people organized for military or administrative purposes. The number 1,000 in Hebrew thought represents completeness, fullness, and divine abundance. The word appears over 480 times in the OT in both its numerical and social senses. Some scholars argue that many of the large census numbers in the OT should be read as 'clans' rather than literal thousands.",
  "theology": "<em>Eleph</em> is theologically significant in God's promises of abundance and covenant faithfulness. God shows steadfast love to '<em>thousands</em> [eleph] of those who love me' (Exodus 20:6) — contrasting His mercy with His wrath on only three or four generations. The military use is prominent in the conquest narratives, where Israel marshals thousands for holy war. In doxology, the heavenly host numbers 'ten thousand times ten thousand' — eleph stacked upon eleph — to express infinite divine majesty.",
  "verses": [
    {"ref": "Exodus 20:6", "text": "But showing steadfast love to <em>thousands</em> [eleph] of those who love me and keep my commandments."},
    {"ref": "Deuteronomy 7:9", "text": "He is the faithful God who keeps covenant and steadfast love with those who love him, to a <em>thousand</em> [eleph] generations."},
    {"ref": "Psalm 84:10", "text": "For a day in your courts is better than a <em>thousand</em> [eleph] elsewhere."},
    {"ref": "Psalm 91:7", "text": "A <em>thousand</em> [eleph] may fall at your side, ten thousand at your right hand, but it will not come near you."},
    {"ref": "Micah 5:2", "text": "But you, O Bethlehem Ephrathah, who are too little to be among the <em>clans</em> [eleph] of Judah, from you shall come forth one who is to be ruler in Israel."},
  ],
  "word_study": "The same word <em>eleph</em> denotes both '1,000' and 'clan/military unit,' leading to rich interpretive discussions. In census passages (Numbers 1–4), some scholars re-read numbers like '46,500' as '46 clans, 500 men' — giving more historically plausible figures. Regardless, the theological point stands: God's covenant blessings extend to overwhelming, almost uncountable numbers, while His judgment is relatively restrained. <em>Eleph</em> also connects to the concept of God's army — the LORD of hosts commands thousands upon thousands.",
  "related": ["H7233 — rebabah (ten thousand, myriad)", "H3967 — meah (hundred)", "H4264 — machaneh (camp, army)"]
},

{
  "strongs": "H615",
  "original": "אָסִיר",
  "transliteration": "asir",
  "pos": "Noun masculine",
  "gloss": "prisoner, captive",
  "short_def": "One who is bound or imprisoned; a captive",
  "full_def": "<em>Asir</em> (אָסִיר) means <strong>prisoner or captive</strong>, derived from <em>asar</em> (H631, to bind, imprison). It refers to those held in physical captivity — in chains, in prison pits, or as war captives — and by extension to any state of spiritual or social bondage. The word carries deep pathos in the Psalms, where it describes the afflicted who cry out to God for deliverance.",
  "theology": "<em>Asir</em> is theologically rich because it sets up one of Scripture's great redemptive patterns: God as the liberator of prisoners. Psalm 68:6 declares that 'God sets the lonely in families and leads out the <em>prisoners</em> [asir] to prosperity.' This foreshadows the Messianic mission declared in Isaiah 61:1 — 'to proclaim liberty to the captives' — which Jesus directly claimed in Luke 4:18. The captive's cry becomes the prayer of all who are spiritually bound, and God's answer is the gospel of release.",
  "verses": [
    {"ref": "Psalm 68:6", "text": "God sets the lonely in families; he leads out the <em>prisoners</em> [asir] with singing, but the rebellious dwell in a parched land."},
    {"ref": "Psalm 102:20", "text": "To hear the groaning of the <em>prisoner</em> [asir], to set free those who were doomed to die."},
    {"ref": "Isaiah 42:7", "text": "To open the eyes that are blind, to bring out the <em>prisoners</em> [asir] from the dungeon, from the prison those who sit in darkness."},
    {"ref": "Zechariah 9:11", "text": "As for you also, because of the blood of my covenant with you, I will set your <em>prisoners</em> [asir] free from the waterless pit."},
    {"ref": "Genesis 39:20", "text": "And Joseph's master took him and put him into the prison, the place where the king's <em>prisoners</em> [asir] were confined."},
  ],
  "word_study": "<em>Asir</em> appears 12 times in the OT, always evoking vulnerability and dependence on a deliverer. The connection to <em>asar</em> (to bind) creates a semantic field of bondage: physical chains, spiritual slavery, and covenantal exile. The Psalms of the exilic period use <em>asir</em> to describe the whole nation under foreign domination. The NT fulfillment is dramatic: Christ 'led captivity captive' (Ephesians 4:8, citing Psalm 68:18), reversing the captive's condition through the cross and resurrection.",
  "related": ["H631 — asar (to bind)", "H1540 — galah (to go into exile)", "H5337 — natsal (to rescue, deliver)", "H3467 — yasha (to save)"]
},

{
  "strongs": "H693",
  "original": "אָרַב",
  "transliteration": "arab",
  "pos": "Verb",
  "gloss": "to lie in wait, ambush",
  "short_def": "To lurk in hiding, set an ambush, lie in wait to attack",
  "full_def": "<em>Arab</em> (אָרַב) means <strong>to lie in wait, to set an ambush, to lurk</strong>. The related noun <em>ereb</em> (ambush) and <em>oreb</em> (one who lies in wait) come from the same root. The verb describes a military or predatory strategy of concealment with intent to attack. It appears 40+ times in its various forms. In wisdom literature, it is characteristically the strategy of the wicked against the innocent.",
  "theology": "Theologically, <em>arab</em> is a vivid image of sin's deceptive nature. Proverbs repeatedly warns that the adulteress, the wicked, and evildoers 'lie in wait' like predators for the unsuspecting. This connects to the Satan figure — the adversary who prowls like a roaring lion (1 Peter 5:8). The NT Greek equivalent <em>enedreuo</em> (to lie in wait) picks up the same imagery. Yet God's people are not without recourse: the LORD Himself ambushes the enemies of His people (Joshua 8; Judges 20), turning the tactic against the wicked.",
  "verses": [
    {"ref": "Proverbs 1:11", "text": "Come with us, let us <em>lie in wait</em> [arab] for blood; let us ambush the innocent without reason."},
    {"ref": "Proverbs 1:18", "text": "These men <em>lie in wait</em> [arab] for their own blood; they set an ambush for their own lives."},
    {"ref": "Psalm 10:9", "text": "He <em>lurks</em> [arab] in ambush in the villages; in hiding places he murders the innocent."},
    {"ref": "Joshua 8:4", "text": "He commanded them: 'See, you shall <em>lie in ambush</em> [arab] against the city, behind it.'"},
    {"ref": "Lamentations 3:10", "text": "He is a bear <em>lying in wait</em> [arab] for me, a lion in hiding."},
  ],
  "word_study": "The root <em>arab</em> is connected to the noun <em>aravah</em> (desert/steppe), suggesting the ambusher hides in desolate, unguarded places. The imagery pervades Proverbs' warnings to the young: the paths of the simple lead through zones of spiritual ambush where sin and seduction lurk. The military usage in Joshua and Judges describes legitimate war strategy, sanctioned by God. The prophets use it metaphorically for false prophets and corrupt leaders who hide their true intent while preying on the vulnerable.",
  "related": ["H6660 — tsediyah (ambush)", "H7770 — sorer (lurker, adversary)", "H7854 — satan (adversary, accuser)", "H5341 — natsar (to watch, guard)"]
},

{
  "strongs": "H835",
  "original": "אֶשֶׁר",
  "transliteration": "esher",
  "pos": "Noun masculine (construct plural: ashrey)",
  "gloss": "blessedness, happiness, how blessed!",
  "short_def": "A state of happiness and blessedness; the joy of the one whom God favors",
  "full_def": "<em>Esher</em> (אֶשֶׁר) and its construct plural <em>ashrey</em> form the classic Hebrew formula for blessedness: <strong>'Blessed is/are...' or 'How happy is...'</strong> It opens the book of Psalms ('Blessed is the man who walks not in the counsel of the wicked') and appears in 26 psalms. Unlike <em>barak</em> (blessed by someone), <em>ashrey</em> is a declaration of a person's enviable state — the quality of life that flows from right relationship with God and wise living.",
  "theology": "<em>Ashrey</em> is the OT foundation for what Jesus develops in the Beatitudes (Matthew 5:3–12). The Greek <em>makarios</em> ('blessed, happy') directly translates <em>ashrey</em>. Both describe not a momentary feeling but an objective condition of divine favor and flourishing — what the tradition calls <em>beatitude</em>. Theologically, <em>ashrey</em> defines the good life: not as wealth, power, or pleasure, but as walking with God, fearing Him, trusting His Word, and caring for the poor. It is eschatological joy breaking into present experience.",
  "verses": [
    {"ref": "Psalm 1:1", "text": "<em>Blessed</em> [ashrey] is the man who walks not in the counsel of the wicked, nor stands in the way of sinners."},
    {"ref": "Psalm 32:1", "text": "<em>Blessed</em> [ashrey] is the one whose transgression is forgiven, whose sin is covered."},
    {"ref": "Psalm 84:5", "text": "<em>Blessed</em> [ashrey] is the man whose strength is in you, in whose heart are the highways to Zion."},
    {"ref": "Proverbs 8:34", "text": "<em>Blessed</em> [ashrey] is the one who listens to me, watching daily at my gates, waiting beside my doors."},
    {"ref": "Psalm 119:1", "text": "<em>Blessed</em> [ashrey] are those whose way is blameless, who walk in the law of the LORD!"},
  ],
  "word_study": "<em>Ashrey</em> is derived from the root <em>ashar</em> (to go straight, to advance, to be set right). The noun <em>esher</em> appears 44 times, always in the plural of intensity ('blessednesses'). It is never used of God (God does not need to be blessed in this sense) — it describes the human flourishing that comes from alignment with God's way. The LXX renders it <em>makarios</em>, which Jesus uses in the Beatitudes, creating a direct theological bridge between the two testaments' understanding of true human happiness.",
  "related": ["H1293 — berakah (blessing)", "H2617 — hesed (steadfast love)", "H8057 — simchah (joy)", "H7965 — shalom (peace, wholeness)"]
},

{
  "strongs": "H2296",
  "original": "חָגַר",
  "transliteration": "chagar",
  "pos": "Verb",
  "gloss": "to gird, gird on, put on a belt",
  "short_def": "To bind on a weapon or garment by means of a belt or girdle; to prepare for action",
  "full_def": "<em>Chagar</em> (חָגַר) means <strong>to gird on, to buckle on, to bind around</strong>. It describes the act of putting on a belt, sash, or sword — the universal ancient gesture of readiness for battle or service. A soldier would 'gird on' his sword before combat; a worker would gird his robe before labor. The word appears about 44 times in the OT in literal and metaphorical senses. Mourning was expressed by 'girding with sackcloth.'",
  "theology": "Girding in Scripture is an image of <strong>preparation, readiness, and strength</strong>. God is described as girding Himself with might (Psalm 65:6). He calls warriors to gird themselves. But most powerfully, in an inversion of expected hierarchy, Jesus girds Himself with a towel to wash His disciples' feet (John 13:4–5) — transforming the imagery from military dominance to servant leadership. Paul's 'armor of God' (Ephesians 6:14) builds on this: 'Stand therefore, having fastened on the belt of truth.'",
  "verses": [
    {"ref": "Psalm 65:6", "text": "The one who by his strength established the mountains, being <em>girded</em> [chagar] with might."},
    {"ref": "1 Samuel 17:39", "text": "David <em>strapped</em> [chagar] his sword over his armor. And he tried in vain to go, for he had not tested them."},
    {"ref": "Isaiah 45:5", "text": "I am the LORD, and there is no other; besides me there is no God; I <em>equip</em> [chagar] you, though you do not know me."},
    {"ref": "Psalm 18:32", "text": "It is God who <em>arms</em> [chagar] me with strength and makes my way blameless."},
    {"ref": "2 Kings 4:29", "text": "He said to Gehazi, '<em>Gird</em> [chagar] up your loins and take my staff in your hand and go.'"},
  ],
  "word_study": "<em>Chagar</em> is connected to the noun <em>chagor</em> (belt, girdle). In the ancient world, a man's belt was both functional and symbolic — it held his weapons and identified his rank. 'Girding the loins' (tucking the robe into the belt) meant readiness for strenuous action, a metaphor Jesus used in Luke 12:35: 'Stay dressed for action and keep your lamps burning.' The act of girding oneself or another was also a mark of honor or servitude, adding layers of meaning to every biblical instance.",
  "related": ["H232 — ezor (girdle, belt)", "H2428 — chayil (strength, might, valor)", "H5402 — nesheq (weapons, armor)"]
},

{
  "strongs": "H2346",
  "original": "חוֹמָה",
  "transliteration": "chomah",
  "pos": "Noun feminine",
  "gloss": "wall, city wall, rampart",
  "short_def": "The protective outer wall of a city; any fortifying wall",
  "full_def": "<em>Chomah</em> (חוֹמָה) means <strong>wall</strong>, specifically the thick defensive wall surrounding an ancient city. It appears over 130 times in the OT. City walls in the ancient Near East were not mere boundaries — they were the difference between life and death, freedom and captivity. Walls could be 20–30 feet thick and towered above the surrounding landscape. A broken wall meant vulnerability; an intact wall meant security. Nehemiah's restoration of Jerusalem's wall was therefore a deeply theological act of national and spiritual renewal.",
  "theology": "Metaphorically, <em>chomah</em> becomes a powerful image for divine protection and salvation. Isaiah declares: 'You shall call your walls Salvation and your gates Praise' (Isaiah 60:18). God Himself is described as a wall of fire around Jerusalem (Zechariah 2:5). The destruction of walls in judgment (Lamentations, Nehemiah) reflects covenant unfaithfulness; their rebuilding reflects restoration and grace. In the New Jerusalem (Revelation 21), the great wall signifies perfect divine security — no enemy can breach it.",
  "verses": [
    {"ref": "Nehemiah 2:17", "text": "You see the trouble we are in, how Jerusalem lies in ruins with its <em>walls</em> [chomah] broken down. Come, let us build the wall of Jerusalem."},
    {"ref": "Isaiah 60:18", "text": "You shall call your <em>walls</em> [chomah] Salvation, and your gates Praise."},
    {"ref": "Zechariah 2:5", "text": "I will be to her a <em>wall</em> [chomah] of fire all around, declares the LORD, and I will be the glory in her midst."},
    {"ref": "Proverbs 25:28", "text": "A man without self-control is like a city broken into and left without <em>walls</em> [chomah]."},
    {"ref": "Song of Solomon 8:10", "text": "I was a <em>wall</em> [chomah], and my breasts were like towers; then I was in his eyes as one who finds peace."},
  ],
  "word_study": "<em>Chomah</em> is distinguished from <em>gader</em> (a garden or field wall, H1447) and <em>kir</em> (a wall of a house, H7023). It refers specifically to the massive defensive perimeter of a fortified city. Archaeological excavations of Jericho, Megiddo, and Jerusalem confirm the importance of city walls in the biblical world. The NT parallel is found in Revelation 21:12–17, where the New Jerusalem has a great high wall with twelve gates — combining the imagery of access (gates) and security (walls) in God's eternal city.",
  "related": ["H5892 — ir (city)", "H8179 — sha'ar (gate)", "H4013 — mivtsar (fortress)", "H3389 — Yerushalayim (Jerusalem)"]
},

{
  "strongs": "H3196",
  "original": "יַיִן",
  "transliteration": "yayin",
  "pos": "Noun masculine",
  "gloss": "wine",
  "short_def": "Fermented wine, the most common alcoholic beverage of the ancient world",
  "full_def": "<em>Yayin</em> (יַיִן) is the most common Hebrew word for <strong>wine</strong>, appearing over 140 times in the OT. It refers to fermented grape juice — the standard drink of the ancient Near East. Wine was a staple of diet, hospitality, worship, and covenant. It appears in contexts ranging from Noah's vineyard to the wedding at Cana. The word encompasses both the gift (wine that 'gladdens the heart of man,' Psalm 104:15) and the danger (wine as a mocker, Proverbs 20:1).",
  "theology": "<em>Yayin</em> holds profound theological ambivalence. On one hand, wine is a sign of divine blessing: it accompanies offerings, feasts, and covenant meals. The promised land flows with grain and wine. On the other hand, wine symbolizes excess, loss of control, and moral ruin — Noah's drunkenness, Lot's seduction, and the prophets' condemnation of drunkards. The Nazirite vow excluded wine (Numbers 6:3). Most profoundly, Jesus takes the Passover cup of wine and redefines it as the cup of the new covenant in His blood (Luke 22:20), transforming <em>yayin</em> into the central symbol of redemption.",
  "verses": [
    {"ref": "Psalm 104:15", "text": "And <em>wine</em> [yayin] to gladden the heart of man, oil to make his face shine and bread to strengthen man's heart."},
    {"ref": "Proverbs 20:1", "text": "<em>Wine</em> [yayin] is a mocker, strong drink a brawler, and whoever is led astray by it is not wise."},
    {"ref": "Isaiah 55:1", "text": "Come, everyone who thirsts, come to the waters; and he who has no money, come, buy and eat! Come, buy <em>wine</em> [yayin] and milk without money."},
    {"ref": "Genesis 14:18", "text": "And Melchizedek king of Salem brought out bread and <em>wine</em> [yayin]. He was priest of God Most High."},
    {"ref": "Amos 9:14", "text": "They shall plant vineyards and drink their <em>wine</em> [yayin], and they shall make gardens and eat their fruit."},
  ],
  "word_study": "<em>Yayin</em> is distinct from <em>tirosh</em> (H8492, new wine/grape juice) and <em>shekar</em> (H7941, strong drink/beer). The grape vine (<em>gephen</em>) and its wine are among Scripture's most layered symbols: the true vine (John 15:1), the blood of the covenant, the eschatological feast of new wine on the mountain (Isaiah 25:6), and the wrath of God 'pressed' from the grapes of wickedness (Revelation 14:19). Wine runs through the full arc of redemption from Noah to the Marriage Supper of the Lamb.",
  "related": ["H8492 — tirosh (new wine)", "H1612 — gephen (vine)", "H3196 — yayin", "H3563 — kos (cup)"]
},

{
  "strongs": "H3499",
  "original": "יֶתֶר",
  "transliteration": "yether",
  "pos": "Noun masculine",
  "gloss": "remainder, rest, abundance, excess",
  "short_def": "What is left over; the remainder; also a cord, bowstring, or string",
  "full_def": "<em>Yether</em> (יֶתֶר) has two distinct but related meanings: (1) <strong>the remainder, the rest, the excess</strong> — what is left after something is taken; and (2) <strong>a cord, string, or bowstring</strong> — what hangs loose or extends beyond. The first meaning appears in historical and legal contexts ('the rest of the people,' 'what remains'); the second in descriptions of weapons and musical instruments. Both derive from the root idea of something extending or hanging beyond.",
  "theology": "In its sense of 'remainder' or 'remnant,' <em>yether</em> connects to one of the Bible's central redemptive themes: the <strong>remnant</strong>. Though not the primary term for this (that is <em>she'erit</em>), <em>yether</em> similarly expresses the idea that God's purposes are never exhausted. Even after judgment, something always remains — a remnant of grace. In its other sense (bowstring), it describes the warrior's readiness and the poet's instrument. The psalmist's stringed instruments and the warrior's bow both depend on a tensioned cord — a beautiful image of creative and martial power.",
  "verses": [
    {"ref": "Exodus 10:5", "text": "They shall cover the face of the land so that no one can see the land, and they shall eat what is left [yether] to you after the hail."},
    {"ref": "Psalm 17:14", "text": "From men of the world whose portion is in this life. You fill their womb with treasure; they are satisfied with children, and they leave their abundance [yether] to their infants."},
    {"ref": "Job 30:11", "text": "Because God has loosed my cord [yether] and humbled me, they have cast off restraint in my presence."},
    {"ref": "Judges 16:7", "text": "Samson said, 'If they bind me with seven fresh bowstrings [yether] that have not been dried, then I shall become weak.'"},
    {"ref": "2 Samuel 8:4", "text": "David took from him 1,700 horsemen, and 20,000 foot soldiers. And David hamstrung all the chariot horses but left enough [yether] for 100 chariots."},
  ],
  "word_study": "<em>Yether</em> appears approximately 97 times and also serves as a proper name (Jether, Jethro). The connection between 'remainder' and 'cord' may be the image of a hanging rope — that which is extra, extended beyond what is used. The theological resonance of the 'remainder' sense is profound: God always preserves a remnant. From Noah's family to Elijah's 7,000 to the Messianic remnant of Isaiah, divine preservation ensures continuity of the covenant community despite judgment.",
  "related": ["H7611 — she'erit (remnant, remainder)", "H7605 — she'ar (what is left)", "H3499 — yether", "H1471 — goy (nation)"]
},

{
  "strongs": "H4438",
  "original": "מַלְכוּת",
  "transliteration": "malkuth",
  "pos": "Noun feminine",
  "gloss": "kingdom, royalty, reign, royal dominion",
  "short_def": "The domain of a king; royal sovereignty; the reign and rule of a monarch",
  "full_def": "<em>Malkuth</em> (מַלְכוּת) means <strong>kingdom, kingship, reign, or royal power</strong>. It is the abstract noun from the root <em>malak</em> (to be king, to reign). It encompasses both the territorial domain of a king and the quality of royal authority itself. The word appears especially frequently in Esther, Daniel, Chronicles, and the Psalms. It is a key term for understanding the theology of divine kingship — God's sovereign rule over all creation.",
  "theology": "<em>Malkuth</em> is theologically central: it describes <strong>God's kingdom</strong>. 'Your kingdom is an everlasting kingdom, and your dominion endures throughout all generations' (Psalm 145:13). Daniel's apocalyptic visions climax in the declaration that 'the kingdom [malkuth] and the dominion and the greatness of all kingdoms under heaven shall be given to the people of the saints of the Most High' (Daniel 7:27). The Aramaic equivalent <em>malkutha</em> appears in Daniel 2–7, forming the conceptual background for Jesus' proclamation of the 'Kingdom of God' — the dawning of God's ultimate royal rule.",
  "verses": [
    {"ref": "Psalm 145:13", "text": "Your <em>kingdom</em> [malkuth] is an everlasting kingdom, and your dominion endures throughout all generations."},
    {"ref": "Daniel 7:27", "text": "And the <em>kingdom</em> [malkuth] and the dominion and the greatness of the kingdoms under the whole heaven shall be given to the people of the saints of the Most High."},
    {"ref": "1 Chronicles 29:11", "text": "Yours, O LORD, is the greatness and the power and the glory and the victory and the majesty, for all that is in the heavens and in the earth is yours. Yours is the <em>kingdom</em> [malkuth], O LORD."},
    {"ref": "Esther 1:2", "text": "In those days when King Ahasuerus sat on his royal throne in Susa, the citadel, in the third year of his <em>reign</em> [malkuth]."},
    {"ref": "Psalm 103:19", "text": "The LORD has established his throne in the heavens, and his <em>kingdom</em> [malkuth] rules over all."},
  ],
  "word_study": "<em>Malkuth</em> appears 91 times, predominantly in Daniel, Esther, Psalms, and Chronicles. Its Aramaic cognate <em>malkutha</em> appears 57 times in Daniel's Aramaic sections. The word bridges the Davidic covenant (God promises David an enduring kingdom) with the eschatological hope of God's universal reign. In the Lord's Prayer, 'Your kingdom come' echoes this OT longing: the full manifestation of <em>malkuth Yahweh</em> — God's royal rule breaking into history and finally consummated at Christ's return.",
  "related": ["H4428 — melek (king)", "H4427 — malak (to reign)", "H4467 — mamlakah (kingdom, realm)", "H3678 — kisse (throne)"]
},

{
  "strongs": "H4592",
  "original": "מְעַט",
  "transliteration": "me'at",
  "pos": "Noun / adjective / adverb",
  "gloss": "a little, few, small amount, shortly",
  "short_def": "A small quantity; a brief time; a few people; opposite of 'many'",
  "full_def": "<em>Me'at</em> (מְעַט) means <strong>a little, a small amount, few, or a short while</strong>. It functions as a noun ('a little bit'), an adjective ('few people'), or an adverb ('in a little while'). It appears about 100 times in the OT. The word is theologically significant in contexts where God works through small things — a small army, a small remnant, a little faith — to accomplish great purposes, consistently reversing human assessments of what is significant.",
  "theology": "The theology of <em>me'at</em> is the theology of divine inversion: <strong>God works through the small to shame the great</strong>. 'You were the fewest [me'at] of all peoples' (Deuteronomy 7:7), yet God chose Israel. Gideon's 300 overcome thousands. The little boy's lunch feeds 5,000. This pattern teaches that God's power is not dependent on human resources or numbers. Conversely, <em>me'at</em> describes the paucity of repentance, the smallness of faith, and the brevity of earthly life — framing the call to wholehearted devotion before the 'little while' passes.",
  "verses": [
    {"ref": "Deuteronomy 7:7", "text": "The LORD did not set his love on you and choose you because you were more in number than any other people, for you were the fewest [me'at] of all peoples."},
    {"ref": "Psalm 8:5", "text": "Yet you have made him a <em>little</em> [me'at] lower than the heavenly beings and crowned him with glory and honor."},
    {"ref": "Proverbs 6:10", "text": "A <em>little</em> [me'at] sleep, a little slumber, a little folding of the hands to rest."},
    {"ref": "Isaiah 10:25", "text": "For in a very <em>little while</em> [me'at] my fury will come to an end, and my anger will be directed to their destruction."},
    {"ref": "Psalm 37:10", "text": "In just a <em>little while</em> [me'at], the wicked will be no more; though you look carefully at his place, he will not be there."},
  ],
  "word_study": "<em>Me'at</em> appears in its most famous theological context in Psalm 8:5, quoted in Hebrews 2:7 — 'You made him for a little while lower than the angels.' The Hebrews author reads this as referring to Jesus, who in His incarnation took on human frailty (the 'little while') before being exalted to glory. This passage shows how the theme of smallness/lowering is not merely negative but is the pathway through which God accomplishes His greatest work — through the humiliation and exaltation of the Son.",
  "related": ["H7227 — rab (many, much)", "H4591 — ma'at (to be few, diminish)", "H1697 — dabar (matter, word)"]
},

{
  "strongs": "H4878",
  "original": "מְשׁוּבָה",
  "transliteration": "meshubah",
  "pos": "Noun feminine",
  "gloss": "backsliding, faithlessness, apostasy",
  "short_def": "A turning away from God; habitual unfaithfulness; spiritual regression",
  "full_def": "<em>Meshubah</em> (מְשׁוּבָה) means <strong>backsliding, apostasy, faithlessness</strong>. It is a nominal form of the verb <em>shub</em> (to turn, return), but in this form it denotes a negative turning — turning <em>away</em> from God rather than toward Him. It is a prophetic term, appearing almost exclusively in Jeremiah and Hosea, where it describes Israel's chronic unfaithfulness to the covenant. The word suggests not a single act of sin but a settled pattern of spiritual defection.",
  "theology": "<em>Meshubah</em> is one of Scripture's most searching diagnoses of the human spiritual condition: the tendency to drift from God not in one dramatic apostasy but through gradual, habitual turning away. Jeremiah 3 is the great locus: 'Return, O faithless Israel [meshubah]... I will not look on you in anger, for I am merciful.' The astounding theology is that God calls even the backslider to return — the very word for their sin (<em>shub</em>) becomes His invitation to repentance. Their spiritual failure is not the last word; His call to 'return' is.",
  "verses": [
    {"ref": "Jeremiah 3:12", "text": "Return, faithless [meshubah] Israel, declares the LORD. I will not look on you in anger, for I am merciful, declares the LORD."},
    {"ref": "Jeremiah 3:22", "text": "'Return, O faithless [meshubah] sons; I will heal your faithlessness [meshubah].' 'Behold, we come to you, for you are the LORD our God.'"},
    {"ref": "Hosea 14:4", "text": "I will heal their <em>backsliding</em> [meshubah]; I will love them freely, for my anger has turned from them."},
    {"ref": "Jeremiah 5:6", "text": "A wolf from the desert shall devastate them, a leopard is watching their cities; everyone who goes out of them shall be torn in pieces, because their transgressions are many, their <em>backslidings</em> [meshubah] are great."},
    {"ref": "Proverbs 1:32", "text": "For the simple are killed by their turning away [meshubah], and the complacency of fools destroys them."},
  ],
  "word_study": "<em>Meshubah</em> appears 12 times, concentrated in Jeremiah (7x) and Hosea (3x). It forms a wordplay with <em>teshubah</em> (return, repentance) — the same root <em>shub</em> produces both the disease and the cure. This is theologically profound: God's call to repent uses the same verbal root as Israel's rebellion. The prophets effectively say: 'You have been turning away — now turn back!' The NT equivalent is found in the imagery of the prodigal son, who 'came to himself' and returned, mirroring the prophetic call to return from <em>meshubah</em>.",
  "related": ["H7725 — shub (to return, repent)", "H5771 — avon (iniquity)", "H898 — bagad (to act treacherously)", "H2617 — hesed (steadfast love)"]
},

{
  "strongs": "H4916",
  "original": "מִשְׁלוֹחַ",
  "transliteration": "mishlowach",
  "pos": "Noun masculine",
  "gloss": "a sending, gift sent, mission",
  "short_def": "That which is sent; a gift dispatched; a sending forth; the reach of one's hand",
  "full_def": "<em>Mishlowach</em> (מִשְׁלוֹחַ) is a noun from <em>shalach</em> (H7971, to send), meaning <strong>a sending, that which is sent, or a mission</strong>. It can refer to (1) portions of food sent as gifts (Esther 9:19, 22), (2) the 'reach' or 'stroke' of God's hand in action or judgment, or (3) the sending out of someone on a mission. The word appears 9 times in the OT and connects to the broader biblical theme of divine sending — the missio Dei.",
  "theology": "The concept behind <em>mishlowach</em> — the sending — is foundational to biblical mission theology. The word <em>shalach</em> underlies all prophetic, priestly, and apostolic calling: Moses is sent to Pharaoh, the prophets are sent to Israel, and ultimately the Son is sent into the world. <em>Mishlowach</em> in Esther captures the communal joy of God's salvation: portions sent to neighbors, gifts to the poor, celebrating together what God has done. The NT word <em>apostolos</em> (apostle, 'one sent') is the Greek equivalent of this Hebrew sending concept.",
  "verses": [
    {"ref": "Esther 9:22", "text": "As the days on which the Jews got relief from their enemies... by sending gifts of food [mishlowach] to one another and gifts to the poor."},
    {"ref": "Deuteronomy 12:7", "text": "There you shall eat before the LORD your God, and you shall rejoice, you and your households, in all that you undertake, in which the LORD your God has blessed you."},
    {"ref": "Isaiah 11:14", "text": "But they shall swoop down on the shoulder of the Philistines in the west, and together they shall plunder the people of the east."},
    {"ref": "Psalm 78:49", "text": "He let loose on them his burning anger, wrath, indignation, and distress, a company of destroying angels."},
    {"ref": "Esther 9:19", "text": "The Jews of the villages... hold the fourteenth day of the month of Adar as a day for gladness and feasting, as a holiday, and as a day on which they send gifts of food [mishlowach] to one another."},
  ],
  "word_study": "<em>Mishlowach</em> is closely tied to the Purim tradition — the sending of food portions (<em>mishloach manot</em> in modern Hebrew) remains a central practice of the Jewish feast of Purim. This 'sending' transforms individual salvation into communal celebration and generosity. Theologically, the missionary impulse of the gospel — 'as the Father has sent me, even so I am sending you' (John 20:21) — is rooted in this OT pattern of divine sending that always aims at communal flourishing and joy.",
  "related": ["H7971 — shalach (to send)", "H4397 — malak (messenger, angel)", "H652 — apostle / sent one"]
},

{
  "strongs": "H5104",
  "original": "נָהָר",
  "transliteration": "nahar",
  "pos": "Noun masculine",
  "gloss": "river, stream, waterway",
  "short_def": "A river or large stream; used for the Euphrates, Nile, and rivers of paradise",
  "full_def": "<em>Nahar</em> (נָהָר) means <strong>river or stream</strong>. It is the primary word for large rivers — the Euphrates (often simply called 'the River'), the rivers of Eden, and the rivers of paradise. The word appears over 110 times in the OT. Rivers were the lifeblood of ancient civilization, enabling agriculture, trade, and travel. They were also objects of reverence and fear — sources of both blessing and destruction.",
  "theology": "Rivers in Scripture carry profound theological symbolism. The river of Eden (Genesis 2:10–14) watered the garden of God, establishing the archetype of divine abundance. Isaiah promises that God will 'extend peace like a river' (Isaiah 66:12). Ezekiel's vision of the river flowing from the temple (Ezekiel 47) — which deepens into a life-giving torrent — is fulfilled in John's vision of 'the river of the water of life' flowing from the throne of God (Revelation 22:1). The <em>nahar</em> thus becomes an eschatological symbol: God's life flows outward from His presence to give life to all.",
  "verses": [
    {"ref": "Genesis 2:10", "text": "A <em>river</em> [nahar] flowed out of Eden to water the garden, and there it divided and became four rivers."},
    {"ref": "Psalm 46:4", "text": "There is a <em>river</em> [nahar] whose streams make glad the city of God, the holy habitation of the Most High."},
    {"ref": "Ezekiel 47:5", "text": "Again he measured a thousand, and it was a <em>river</em> [nahar] that I could not pass through, for the water had risen. It was deep enough to swim in, a river that could not be passed through."},
    {"ref": "Isaiah 66:12", "text": "For thus says the LORD: Behold, I will extend peace to her like a <em>river</em> [nahar], and the glory of the nations like an overflowing stream."},
    {"ref": "Psalm 72:8", "text": "May he have dominion from sea to sea, and from the <em>River</em> [nahar] to the ends of the earth!"},
  ],
  "word_study": "<em>Nahar</em> connects to the verb <em>nahar</em> (H5102, to flow, to stream, also to be radiant/joyful) — a suggestive double meaning: rivers flow AND bring light/joy. 'All the nations stream to it' (Isaiah 2:2) uses this verb, showing that the Messianic pilgrimage to Zion is like rivers flowing. The 'river' of God's glory, peace, and life runs throughout the whole biblical narrative, from Eden's four rivers to the crystal river of Revelation 22.",
  "related": ["H5158 — nachal (stream, wadi, torrent)", "H4325 — mayim (water)", "H3220 — yam (sea)", "H6388 — peleg (canal, stream)"]
},

{
  "strongs": "H5236",
  "original": "נֵכָר",
  "transliteration": "nekar",
  "pos": "Noun masculine",
  "gloss": "foreignness, what is alien, foreign land",
  "short_def": "Foreign-ness; the alien or strange; a foreign land or foreign thing",
  "full_def": "<em>Nekar</em> (נֵכָר) means <strong>foreignness, alienness, or a foreign land</strong>. It is related to <em>nakar</em> (to be foreign, to recognize as different) and <em>nokri</em> (foreigner, H5237). The word appears 36 times. It describes what is foreign — foreign gods, foreign lands, foreign women — things that stand outside the covenant and can draw Israel away from YHWH. It is fundamentally a word of distinction: what belongs to the covenant versus what lies outside it.",
  "theology": "<em>Nekar</em> encapsulates a central tension in the OT: Israel is called to be distinct from surrounding nations (Leviticus 20:26) while also welcoming the sojourner and stranger. The 'foreign god' (<em>el nekar</em>) is the greatest danger — a false deity claiming allegiance that belongs only to YHWH. Yet Ruth, a 'foreign woman,' becomes an ancestor of David and Jesus — demonstrating that foreignness can be overcome by covenant loyalty. The eschatological vision includes foreigners joining the Lord's community (Isaiah 56:6–7), expanding the covenant beyond ethnic Israel.",
  "verses": [
    {"ref": "Genesis 35:2", "text": "So Jacob said to his household... 'Put away the foreign gods [elohei nekar] that are among you and purify yourselves.'"},
    {"ref": "Psalm 137:4", "text": "How shall we sing the LORD's song in a <em>foreign</em> [nekar] land?"},
    {"ref": "Isaiah 56:6", "text": "And the foreigners who join themselves to the LORD... to love the name of the LORD, and to be his servants."},
    {"ref": "Deuteronomy 31:16", "text": "And this people will rise and whore after the foreign gods [elohei nekar] among them in the land."},
    {"ref": "Joshua 24:20", "text": "If you forsake the LORD and serve foreign gods [elohei nekar], then he will turn and do you harm."},
  ],
  "word_study": "<em>Nekar</em> is in a semantic field with <em>ger</em> (sojourner/resident alien, H1616) and <em>zar</em> (strange/unauthorized, H2114). The distinctions matter: the <em>ger</em> is a foreigner who lives under covenant protection; the <em>nokri</em>/<em>nekar</em> is a foreigner who remains outside. The biblical vision progressively widens: Solomon's temple is built with prayer that even the foreigner may come and pray (1 Kings 8:41–43). In Christ, the dividing wall between Jew and Gentile is broken down (Ephesians 2:14), abolishing the ultimate <em>nekar</em> distinction.",
  "related": ["H1616 — ger (sojourner, resident alien)", "H2114 — zar (stranger, unauthorized)", "H5237 — nokri (foreigner)", "H1471 — goy (nation, Gentile)"]
},

{
  "strongs": "H5352",
  "original": "נָקָה",
  "transliteration": "naqah",
  "pos": "Verb",
  "gloss": "to be innocent, to be free from guilt, to go unpunished, to cleanse",
  "short_def": "To be declared clean or innocent; to go free from punishment; to acquit",
  "full_def": "<em>Naqah</em> (נָקָה) means <strong>to be empty, clean, free from guilt or punishment, innocent, or acquitted</strong>. In the Piel stem, it means to declare innocent or to cleanse. The adjective <em>naqi</em> means innocent or free from obligation. The word appears 44 times and is deeply connected to legal and moral purity — both the state of being innocent and the act of being acquitted by a judge. Most profoundly, it appears in God's own self-disclosure as one who will 'by no means clear the guilty' (Exodus 34:7).",
  "theology": "The theology of <em>naqah</em> sets up one of Scripture's great tensions: God is 'slow to anger, abounding in steadfast love, forgiving iniquity and transgression, yet he will by no means clear the guilty' (Numbers 14:18). How can God be both merciful and just? This tension is resolved at the cross: the innocent One (<em>naqi</em>) bears the guilt of the not-innocent, so that the guilty might be declared innocent. The NT doctrine of justification (<em>dikaioo</em>) — being declared righteous before God — is the NT resolution to the OT question: how can God <em>naqah</em> the guilty?",
  "verses": [
    {"ref": "Exodus 34:7", "text": "Who will by no means clear [naqah] the guilty, visiting the iniquity of the fathers on the children and the children's children."},
    {"ref": "Jeremiah 30:11", "text": "For I am with you to save you, declares the LORD; I will make a full end of all the nations among whom I scattered you, but of you I will not make a full end. I will discipline you in just measure, and I will by no means leave you <em>unpunished</em> [naqah]."},
    {"ref": "Psalm 19:13", "text": "Keep back your servant also from presumptuous sins; let them not have dominion over me! Then I shall be <em>blameless</em> [naqi], and innocent of great transgression."},
    {"ref": "Numbers 5:31", "text": "The man shall be free [naqah] from iniquity, but the woman shall bear her iniquity."},
    {"ref": "Joel 3:21", "text": "I will avenge their blood, blood I have not avenged, for the LORD dwells in Zion."},
  ],
  "word_study": "<em>Naqah</em> in the Qal (simple) stem means 'to be free/innocent'; in Piel it means 'to cleanse, acquit, leave unpunished.' The double negation 'by no means clear' (naqah lo' yenaqeh) emphasizes God's absolute refusal to treat sin lightly. This is not cruelty but the foundation of moral order. The resolution comes only through substitutionary atonement — the innocent (<em>naqi</em>) taking the place of the guilty — which is the logic of all OT sacrifice and the ultimate meaning of Christ's death.",
  "related": ["H2889 — tahor (pure, clean)", "H6663 — tsadaq (to be righteous, justify)", "H3722 — kaphar (to atone, cover)", "H5771 — avon (iniquity, guilt)"]
},

{
  "strongs": "H5504",
  "original": "סַחַר",
  "transliteration": "sachar",
  "pos": "Noun masculine",
  "gloss": "gain from trade, profit, merchandise",
  "short_def": "The profit or gain from trade; merchandise; commercial exchange",
  "full_def": "<em>Sachar</em> (סַחַר) means <strong>profit, merchandise, or the gain derived from trade</strong>. It is related to <em>sachar</em> (the verb, to go around as a merchant, to travel about trading). It appears 4 times in the OT. Ancient Israelite society was not primarily commercial, but trade with Phoenicia, Egypt, and neighboring nations created wealth and posed spiritual dangers — the seduction of wealth above covenant faithfulness.",
  "theology": "<em>Sachar</em> connects to the prophetic critique of unjust commerce and the exploitation of the poor. Ezekiel's lament over Tyre (Ezekiel 26–28) describes the merchant city's <em>sachar</em> as the root of its pride and ultimate destruction. 'By the abundance of your trade you were filled with violence in your midst, and you sinned' (Ezekiel 28:16). Yet Proverbs presents an alternative: the excellent wife is like merchant ships, her trade bringing benefit to her household and community. The question is not commerce itself but whether it serves God's purposes of justice and care.",
  "verses": [
    {"ref": "Proverbs 3:14", "text": "For the <em>gain</em> [sachar] from her is better than gain from silver and her profit better than gold."},
    {"ref": "Isaiah 23:3", "text": "Her revenue was the grain of Shihor, the harvest of the Nile; she was the <em>mart</em> [sachar] of nations."},
    {"ref": "Isaiah 23:18", "text": "Her <em>merchandise</em> [sachar] and her wages will be holy to the LORD. It will not be stored or hoarded, but her merchandise will supply abundant food and fine clothing for those who dwell before the LORD."},
    {"ref": "Ezekiel 28:5", "text": "By your great wisdom in your trade [sachar] you have increased your wealth, and your heart has become proud in your wealth."},
    {"ref": "Job 41:6", "text": "Shall traders [sachar] bargain over him? Shall they divide him up among the merchants?"},
  ],
  "word_study": "<em>Sachar</em> connects to the broader root <em>SChR</em> — to go around, to travel in a circuit — the merchant's activity of moving goods between markets. The word is etymologically related to <em>socher</em> (merchant). Isaiah 23:18 is remarkable: Tyre's commercial wealth, though gained in pagan trade, will ultimately be consecrated to the LORD — a hint of the eschatological ingathering of the nations' wealth into God's kingdom (see also Revelation 21:24–26: 'The kings of the earth will bring their glory into it').",
  "related": ["H4766 — marbo (increase, profit)", "H7666 — shabar (to buy grain)", "H3701 — keseph (silver, money)", "H6231 — ashaq (to oppress in trade)"]
},

{
  "strongs": "H5601",
  "original": "סַפִּיר",
  "transliteration": "sappir",
  "pos": "Noun masculine",
  "gloss": "sapphire, lapis lazuli",
  "short_def": "A brilliant blue precious stone, likely lapis lazuli or sapphire; a stone of divine glory",
  "full_def": "<em>Sappir</em> (סַפִּיר) refers to a <strong>brilliant blue precious stone</strong> — most likely lapis lazuli (in the ancient world) or what we call sapphire today. It appears 11 times in the OT. It is consistently associated with divine glory and the heavenly throne. The vivid blue of <em>sappir</em> — the color of clear sky — made it a natural symbol for heaven, divine purity, and transcendent beauty. It was one of the gems on the high priest's breastplate (Exodus 28:18) and appears in visions of God's throne.",
  "theology": "<em>Sappir</em> is remarkable for its consistent association with theophany — divine appearances. When Moses and the elders see God (Exodus 24:10), the pavement beneath His feet is like <em>sappir</em>. Ezekiel's throne vision (Ezekiel 1:26; 10:1) features a sapphire-blue expanse above the cherubim, and the throne itself is like sapphire stone. This is not mere decoration — the gleaming blue is the color of heaven itself, of the presence of God. In the New Jerusalem, the second foundation stone is sapphire (Revelation 21:19), carrying this divine-glory symbolism into the eternal city.",
  "verses": [
    {"ref": "Exodus 24:10", "text": "And they saw the God of Israel. There was under his feet as it were a pavement of <em>sapphire</em> [sappir] stone, like the very heaven for clearness."},
    {"ref": "Ezekiel 1:26", "text": "And above the expanse over their heads there was the likeness of a throne, in appearance like <em>sapphire</em> [sappir]; and seated above the likeness of a throne was a likeness with a human appearance."},
    {"ref": "Song of Solomon 5:14", "text": "His arms are rods of gold, set with jewels. His body is polished ivory, bedecked with <em>sapphires</em> [sappir]."},
    {"ref": "Lamentations 4:7", "text": "Her princes were purer than snow, whiter than milk; their bodies were more ruddy than coral, the beauty of their form like <em>sapphire</em> [sappir]."},
    {"ref": "Isaiah 54:11", "text": "I will set your stones in antimony, and lay your foundations with <em>sapphires</em> [sappir]."},
  ],
  "word_study": "<em>Sappir</em> is likely a loanword from Sanskrit <em>sanipria</em> (precious to Saturn) through Akkadian <em>sappar</em>. Modern sapphire (corundum) was almost certainly not mined in the ancient Near East; the biblical stone was almost certainly lapis lazuli — a deep blue stone with gold flecks, mined in Afghanistan. The consistent use of <em>sappir</em> in throne visions and covenant theophanies makes it a 'divine color' — the blue of heaven, glory, and the presence of God. It anticipates the crystal-clear New Jerusalem and the Lamb upon the sapphire-blue throne.",
  "related": ["H2859 — yahalom (diamond, jasper)", "H3068 — YHWH (in throne visions)", "H3519 — kabod (glory)", "H6944 — qodesh (holiness)"]
},

{
  "strongs": "H7227",
  "original": "רַב",
  "transliteration": "rab",
  "pos": "Adjective / noun masculine",
  "gloss": "much, many, great, abundant; chief, captain",
  "short_def": "Large in quantity, number, or degree; also a title of authority (chief, master)",
  "full_def": "<em>Rab</em> (רַב) means <strong>much, many, great, or abundant</strong> as an adjective, and <strong>chief, captain, or master</strong> as a noun. It is one of the most common Hebrew words, appearing over 400 times. As an adjective, it modifies people, things, and attributes. As a noun/title, it identifies leaders — the Rab-shakeh (chief cup-bearer/official), Rab-saris (chief eunuch), Rabboni (My Master). It becomes the basis for the Hebrew/Aramaic title <em>Rabbi</em> (my teacher/master).",
  "theology": "The greatness of God is expressed extensively with <em>rab</em> and related forms: His <strong>steadfast love</strong> (hesed) is <em>rab</em> — 'great is your steadfast love toward me' (Psalm 86:13). His mercy is 'according to his abundant [rab] steadfast love' (Psalm 51:1). His judgments are <em>rab</em>. When God declares Himself in Exodus 34:6–7, <em>rab</em> characterizes His core attributes. In titles, <em>Rabbi</em>/<em>Rabboni</em> is what disciples call Jesus — acknowledging His supreme teaching authority and divine wisdom.",
  "verses": [
    {"ref": "Psalm 51:1", "text": "Have mercy on me, O God, according to your steadfast love; according to your <em>abundant</em> [rab] mercy blot out my transgressions."},
    {"ref": "Psalm 86:13", "text": "For <em>great</em> [rab] is your steadfast love toward me; you have delivered my soul from the depths of Sheol."},
    {"ref": "Proverbs 14:20", "text": "The poor is disliked even by his neighbor, but the rich has <em>many</em> [rab] friends."},
    {"ref": "Isaiah 63:7", "text": "According to the <em>great</em> [rab] goodness to the house of Israel that he has granted them according to his compassion and according to the abundance of his steadfast love."},
    {"ref": "Daniel 2:48", "text": "Then the king gave Daniel high honors and many <em>great</em> [rab] gifts, and made him ruler over the whole province of Babylon."},
  ],
  "word_study": "<em>Rab</em> is the root for many significant Hebrew terms: <em>rabbim</em> (many), <em>robab</em> (multitude), and especially the Aramaic/Hebrew title <em>Rabbi</em> ('my great one' or 'my master'). When Mary Magdalene calls the risen Jesus 'Rabboni!' (John 20:16), she uses the most intimate form of this title. The theological weight: the One who is <em>rab</em> in all things — mighty in mercy, great in steadfast love, abundant in compassion — is also the intimate teacher and master of His disciples.",
  "related": ["H7230 — rob (greatness, abundance)", "H7231 — rabab (to be many)", "H2617 — hesed (steadfast love)", "H7349 — rachum (merciful, compassionate)"]
},

{
  "strongs": "H7392",
  "original": "רָכַב",
  "transliteration": "rakab",
  "pos": "Verb",
  "gloss": "to ride, to mount and ride, to drive",
  "short_def": "To ride upon an animal or chariot; to mount; to cause to ride",
  "full_def": "<em>Rakab</em> (רָכַב) means <strong>to ride, to mount (an animal or chariot), or to drive</strong>. The related noun <em>rekev</em> refers to a chariot or riding animal. In the ancient world, riding was associated with military power (cavalry, chariots) and royal dignity. The verb appears about 78 times. It is applied to human warriors, kings, and — most gloriously — to God Himself, who 'rides' upon the heavens and the clouds as His chariot.",
  "theology": "God riding upon the heavens (Deuteronomy 33:26; Psalm 68:4, 33) is one of Scripture's most majestic images of divine sovereignty. He 'rides on the clouds' — a title once applied to the Canaanite storm god Baal, but claimed exclusively for YHWH. This is theological polemic: the One who truly rides the storm clouds is Israel's God alone. The theme culminates in Revelation 19:11 — the rider on the white horse, whose name is 'Faithful and True,' goes out to judge and make war. This is YHWH-as-warrior, the Divine Rider who vindicates His people.",
  "verses": [
    {"ref": "Deuteronomy 33:26", "text": "There is none like God, O Jeshurun, who <em>rides</em> [rakab] through the heavens to your help, through the skies in his majesty."},
    {"ref": "Psalm 68:4", "text": "Sing to God, sing praises to his name; lift up a song to him who <em>rides</em> [rakab] through the deserts; his name is the LORD."},
    {"ref": "Psalm 45:4", "text": "In your majesty <em>ride</em> [rakab] out victoriously for the cause of truth and meekness and righteousness."},
    {"ref": "Zechariah 9:9", "text": "Rejoice greatly, O daughter of Zion! Shout aloud, O daughter of Jerusalem! Behold, your king is coming to you; righteous and having salvation is he, humble and <em>mounted</em> [rakab] on a donkey."},
    {"ref": "Habakkuk 3:8", "text": "Was your wrath against the rivers, O LORD? Was your anger against the rivers, or your indignation against the sea, when you <em>rode</em> [rakab] on your horses, on your chariot of salvation?"},
  ],
  "word_study": "<em>Rakab</em> in Zechariah 9:9 is crucial — the Messianic king comes riding on a donkey, not a war horse. This deliberate choice signals humility and peace rather than conquest by force. Matthew 21:5 and John 12:15 quote this passage at the Triumphal Entry, showing Jesus as the humble king who 'rides' into Jerusalem on a donkey — fulfilling the Messiah's pattern of lowly entry before glorious return. The contrast is deliberate: first coming on a donkey (peace), second coming as the Divine Rider (judgment).",
  "related": ["H4818 — merkavah (chariot)", "H5483 — sus (horse)", "H2428 — chayil (might, army)", "H4421 — milchamah (battle, war)"]
},

{
  "strongs": "H7624",
  "original": "שְׁבַח",
  "transliteration": "shebach",
  "pos": "Verb (Aramaic)",
  "gloss": "to praise, to laud, to commend",
  "short_def": "To praise or commend — used in Daniel's Aramaic sections for praising God or glorifying kings",
  "full_def": "<em>Shebach</em> (שְׁבַח) is the Aramaic equivalent of Hebrew <em>shabach</em> (H7623), meaning <strong>to praise, laud, or commend</strong>. It appears 5 times, exclusively in Daniel's Aramaic sections. In Daniel 2–7, the pagan kings Nebuchadnezzar and Darius make remarkable declarations praising the God of Israel — using this word to acknowledge His incomparable greatness after miraculous interventions. It is also used ironically of Belshazzar praising his gods of silver (Daniel 5:4).",
  "theology": "The use of <em>shebach</em> by Nebuchadnezzar (Daniel 4:34) is one of Scripture's most remarkable scenes: a pagan world emperor, after a period of divine humiliation, lifts his eyes to heaven and praises the Most High — 'I praised [shebach] and honored the King of heaven.' This is a foretaste of the eschatological universal praise: every tongue will confess that Jesus is Lord (Philippians 2:11). The contrast with Belshazzar (Daniel 5:4), who praises idols on the night of his death, frames the theological choice: praise the living God or face judgment.",
  "verses": [
    {"ref": "Daniel 4:34", "text": "My reason returned to me, and I blessed the Most High, and <em>praised</em> [shebach] and honored him who lives forever."},
    {"ref": "Daniel 4:37", "text": "Now I, Nebuchadnezzar, <em>praise</em> [shebach] and extol and honor the King of heaven, for all his works are right and his ways are just."},
    {"ref": "Daniel 5:4", "text": "They drank wine and <em>praised</em> [shebach] the gods of gold and silver, bronze, iron, wood, and stone."},
    {"ref": "Daniel 2:23", "text": "To you, O God of my fathers, I give thanks and <em>praise</em> [shebach], for you have given me wisdom and might."},
    {"ref": "Daniel 5:23", "text": "But you have lifted up yourself against the Lord of heaven... and you have <em>praised</em> [shebach] the gods of silver and gold."},
  ],
  "word_study": "<em>Shebach</em> belongs to the international Aramaic of the Persian period (538–333 BC). The Hebrew equivalent <em>shabach</em> (Psalm 63:3, 117:1) is used in the Psalter for enthusiastic public praise. Both words describe not quiet, private adoration but public, vocal, exuberant commendation. Nebuchadnezzar's praise in Daniel 4 is the literary climax of his arc — from arrogant self-deification to humble acknowledgment. It is one of the most theologically loaded scenes in the OT, modeling what universal worship of the King of heaven will look like.",
  "related": ["H7623 — shabach (to praise, laud — Hebrew)", "H1984 — halal (to praise, boast)", "H3034 — yadah (to give thanks, praise)", "H5046 — nagad (to declare, proclaim)"]
},

{
  "strongs": "H8135",
  "original": "שִׂנְאָה",
  "transliteration": "sinah",
  "pos": "Noun feminine",
  "gloss": "hatred, enmity",
  "short_def": "Strong hostile feeling directed against a person or thing; enmity, animosity",
  "full_def": "<em>Sinah</em> (שִׂנְאָה) means <strong>hatred, enmity, or animosity</strong>. It is the noun form of <em>sane'</em> (H8130, to hate). It appears 17 times in the OT. Biblical hatred is not merely dislike but intense, active hostility that produces harmful actions. Scripture speaks of human hatred toward others (brother against brother, enemies against the righteous) but also of God's hatred of evil — not a moral flaw but a holy response to wickedness and injustice.",
  "theology": "<em>Sinah</em> is theologically important because it reveals the opposite of love. The command 'love your neighbor as yourself' (Leviticus 19:18) is set against the implicit prohibition of <em>sinah</em>. Proverbs declares: 'Hatred [sinah] stirs up strife, but love covers all offenses' (10:12). Jesus intensifies this in the Sermon on the Mount: not just hatred of enemies, but hatred of brothers, makes one liable to judgment (Matthew 5:22). Yet God's own holy hatred of sin (Psalm 5:5; 45:7) is not sinful — it is the inevitable response of perfect goodness to evil. The cross resolves this: God's wrath against sin is poured out on Christ, so that His love for sinners is fully expressed.",
  "verses": [
    {"ref": "Proverbs 10:12", "text": "<em>Hatred</em> [sinah] stirs up strife, but love covers all offenses."},
    {"ref": "Proverbs 26:26", "text": "Though his <em>hatred</em> [sinah] be covered with deception, his wickedness will be exposed in the assembly."},
    {"ref": "Ecclesiastes 9:1", "text": "But all this I laid to heart, examining it all, how the righteous and the wise and their deeds are in the hand of God. Whether it is love or <em>hate</em> [sinah], man does not know."},
    {"ref": "Psalm 109:3", "text": "They encircle me with words of <em>hatred</em> [sinah], and attack me without cause."},
    {"ref": "2 Samuel 13:15", "text": "Then Amnon hated her with very great <em>hatred</em> [sinah], so that the hatred with which he hated her was greater than the love with which he had loved her."},
  ],
  "word_study": "<em>Sinah</em> in 2 Samuel 13:15 is one of Scripture's most psychologically acute observations: post-sin, Amnon's love inverts to violent hatred — greater than the original desire. This illustrates that disordered love (lust) inevitably produces its inverse (hatred/contempt). The Psalms of lament describe enemies whose <em>sinah</em> is gratuitous and unjust — mirroring the hatred the world bears toward Christ (John 15:25: 'They hated me without cause,' quoting Psalm 35:19). The NT resolution: love of enemies overcomes sinah; the cross absorbs enmity and creates peace.",
  "related": ["H8130 — sane' (to hate)", "H342 — eivah (enmity, hostility)", "H157 — ahav (to love)", "H7379 — riv (contention, strife)"]
},


# ==================== GREEK ====================

{
  "strongs": "G94",
  "original": "ἄδικος",
  "transliteration": "adikos",
  "pos": "Adjective",
  "gloss": "unjust, unrighteous, wicked",
  "short_def": "One who does not act rightly; violating what is right; unjust",
  "full_def": "<em>Adikos</em> (ἄδικος) means <strong>unjust, unrighteous, or wicked</strong>. It is the negative of <em>dikaios</em> (righteous, just) — prefixed with alpha-privative (<em>a-</em>) meaning 'not.' It describes persons or acts that deviate from what is right in God's moral order. It appears 12 times in the NT. It encompasses both legal injustice (unfair treatment of others) and moral unrighteousness (living contrary to God's standards).",
  "theology": "<em>Adikos</em> is theologically significant for defining what falls outside the kingdom of God. '...the unrighteous [adikos] will not inherit the kingdom of God' (1 Corinthians 6:9). But the gospel's power is that God 'justifies the ungodly' (Romans 4:5) — He declares as righteous those who are, by nature, <em>adikoi</em>. Peter (1 Peter 3:18) strikes the deepest note: 'Christ suffered once for sins, the righteous [<em>dikaios</em>] for the unrighteous [<em>adikos</em>].' The innocent One substituted for the guilty — this is the heart of atonement.",
  "verses": [
    {"ref": "1 Corinthians 6:9", "text": "Or do you not know that the <em>unrighteous</em> [adikos] will not inherit the kingdom of God? Do not be deceived."},
    {"ref": "1 Peter 3:18", "text": "For Christ also suffered once for sins, the righteous for the <em>unrighteous</em> [adikos], that he might bring us to God."},
    {"ref": "Luke 16:10", "text": "One who is faithful in a very little is also faithful in much, and one who is dishonest [adikos] in a very little is also dishonest in much."},
    {"ref": "Matthew 5:45", "text": "For he makes his sun rise on the evil and on the good, and sends rain on the just and on the <em>unjust</em> [adikos]."},
    {"ref": "Romans 3:5", "text": "But if our unrighteousness serves to show the righteousness of God, what shall we say? That God is <em>unrighteous</em> [adikos] to inflict wrath on us?"},
  ],
  "word_study": "<em>Adikos</em> is the adjectival form of <em>adikia</em> (G93, unrighteousness). In Greek philosophy, <em>dike</em> was the foundational concept of justice — what is rightly due. <em>Adikos</em> violates this cosmic order. In biblical usage, righteousness is not merely philosophical but covenantal: what God requires and what God provides. The magnificent paradox of the gospel (1 Peter 3:18) — the righteous dying for the unrighteous — is the solution to humanity's most fundamental problem: we are adikoi before a perfectly dikaios God.",
  "related": ["G93 — adikia (unrighteousness)", "G1342 — dikaios (righteous, just)", "G1343 — dikaiosyne (righteousness)", "G264 — hamartano (to sin)"]
},

{
  "strongs": "G138",
  "original": "αἱρέομαι",
  "transliteration": "haireomai",
  "pos": "Verb (middle voice)",
  "gloss": "to choose, to prefer, to take for oneself",
  "short_def": "To choose deliberately; to select one thing over another; to prefer",
  "full_def": "<em>Haireomai</em> (αἱρέομαι) means <strong>to choose, to prefer, or to take for oneself</strong>. It appears 3 times in the NT, always in the middle voice (indicating the subject acts for their own benefit or interest). It emphasizes deliberate, personal selection — choosing one thing over another based on preference and will. The related noun <em>hairesis</em> (heresy/sect) comes from this root — a group that 'chooses' its own way apart from the whole.",
  "theology": "Despite its rare NT occurrence, <em>haireomai</em> carries significant theological weight in its three uses. In Philippians 1:22, Paul says he does not know which to 'choose' — life or death. In 2 Thessalonians 2:13, God 'chose' believers from the beginning for salvation. This last use is profoundly important for understanding <strong>divine election</strong>: God's saving choice is not based on foreseen merit but on His sovereign will and grace. The word emphasizes that salvation originates in God's free, deliberate act of choosing — not in human desert.",
  "verses": [
    {"ref": "2 Thessalonians 2:13", "text": "But we ought always to give thanks to God for you, brothers beloved by the Lord, because God <em>chose</em> [haireomai] you as the firstfruits to be saved, through sanctification by the Spirit."},
    {"ref": "Philippians 1:22", "text": "If I am to live in the flesh, that means fruitful labor for me. Yet which I shall <em>choose</em> [haireomai] I cannot tell."},
    {"ref": "Hebrews 11:25", "text": "Choosing [haireomai] rather to be mistreated with the people of God than to enjoy the fleeting pleasures of sin."},
    {"ref": "John 15:16", "text": "You did not choose me, but I chose you and appointed you that you should go and bear fruit."},
    {"ref": "1 Corinthians 1:27", "text": "But God chose what is foolish in the world to shame the wise; God chose what is weak in the world to shame the strong."},
  ],
  "word_study": "<em>Haireomai</em> relates to the Greek philosophical concept of <em>prohairesis</em> (rational choice, free will) — a word important in Stoic ethics. In the biblical context, it is enlisted for the doctrine of divine election: God's choosing is not arbitrary but flows from His nature of love and sovereign grace. Hebrews 11:25's use is equally powerful: Moses 'chose' suffering over pleasure — showing that genuine faith expresses itself through deliberate preference for God's kingdom over earthly comfort.",
  "related": ["G1586 — eklego (to choose, elect)", "G1589 — ekloge (election, choice)", "G139 — hairesis (sect, heresy — from same root)", "G2309 — thelo (to will, desire)"]
},

{
  "strongs": "G155",
  "original": "αἴτημα",
  "transliteration": "aitema",
  "pos": "Noun neuter",
  "gloss": "request, petition, what is asked for",
  "short_def": "That which is asked or requested; a petition made to God or a person",
  "full_def": "<em>Aitema</em> (αἴτημα) means <strong>a request, petition, or demand</strong> — the thing asked for, not the act of asking. It appears 3 times in the NT. It derives from <em>aiteo</em> (G154, to ask, request, demand). The distinction is subtle: <em>aitesis</em> is the act of asking; <em>aitema</em> is the content of what is asked. In prayer contexts, it emphasizes the specific petitions brought before God — the particular burdens, needs, and desires laid at His feet.",
  "theology": "Philippians 4:6 uses <em>aitema</em> in one of Scripture's most complete teachings on prayer: 'Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your <em>requests</em> [aitema] be made known to God.' This is prayer as the antidote to anxiety — not stoic suppression of needs, but their honest presentation to the Father. 1 John 5:15 builds on this: 'Whatever we ask [aitema], we know that we have the requests that we have asked of him.' Bold, trusting petition is an expression of covenant confidence in a hearing God.",
  "verses": [
    {"ref": "Philippians 4:6", "text": "Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your <em>requests</em> [aitema] be made known to God."},
    {"ref": "1 John 5:15", "text": "And if we know that he hears us in whatever we ask, we know that we have the <em>requests</em> [aitema] that we have asked of him."},
    {"ref": "Luke 23:24", "text": "So Pilate decided that their <em>demand</em> [aitema] should be granted."},
    {"ref": "Matthew 7:7", "text": "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you."},
    {"ref": "1 John 5:14", "text": "And this is the confidence that we have toward him, that if we ask anything according to his will he hears us."},
  ],
  "word_study": "<em>Aitema</em> is distinguished from <em>deesis</em> (G1162, earnest entreaty) and <em>proseuche</em> (G4335, general prayer). Together in Philippians 4:6, these three words describe the full richness of prayer: general communion with God (<em>proseuche</em>), earnest pleading (<em>deesis</em>), and specific requests (<em>aitema</em>). This richness of vocabulary reveals that NT prayer is not a vague spiritual practice but a structured, relational, and specific bringing of oneself before the living God.",
  "related": ["G154 — aiteo (to ask, request)", "G1162 — deesis (entreaty, petition)", "G4335 — proseuche (prayer)", "G2065 — erotao (to ask, inquire)"]
},

{
  "strongs": "G226",
  "original": "ἀληθεύω",
  "transliteration": "aletheuo",
  "pos": "Verb",
  "gloss": "to speak truth, to deal truly, to be truthful",
  "short_def": "To tell the truth; to act according to truth; to be truthful in word and deed",
  "full_def": "<em>Aletheuo</em> (ἀληθεύω) means <strong>to speak truth, to tell the truth, or to act in truth</strong>. It appears only twice in the NT (Galatians 4:16 and Ephesians 4:15). It is the verbal form of <em>alethes</em> (true) and <em>aletheia</em> (truth). The word encompasses not just verbal accuracy but authentic, integral truthfulness — living and speaking in accordance with reality as God defines it.",
  "theology": "Both NT uses of <em>aletheuo</em> are theologically rich. Paul asks the Galatians (4:16) whether he has become their enemy 'by telling you the truth' — revealing that gospel truth often creates conflict. Ephesians 4:15 gives the great call to 'speak the truth in love' (<em>aletheuo</em> in the context of <em>agape</em>) as the means of maturing into Christ. This is a foundational Christian ethic: truth and love are not opposites but must always go together. Truth without love becomes brutality; love without truth becomes flattery. Only their union builds up the body of Christ.",
  "verses": [
    {"ref": "Ephesians 4:15", "text": "Rather, <em>speaking the truth</em> [aletheuo] in love, we are to grow up in every way into him who is the head, into Christ."},
    {"ref": "Galatians 4:16", "text": "Have I then become your enemy by <em>telling you the truth</em> [aletheuo]?"},
    {"ref": "John 8:32