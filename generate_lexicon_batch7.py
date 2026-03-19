#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek"""
import os
import json

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")
MANIFEST_PATH = os.path.expanduser("~/bible-reading-plan-bot/docs/assets/lexicon-manifest.json")

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
        .verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }
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

def make_verse(ref, text):
    return f"""                <div class="verse-entry">
                    <a href="../bible.html?ref={ref.replace(' ', '+')}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>"""

def make_related(entries):
    links = []
    for strongs, label in entries:
        links.append(f'                <a href="{strongs}.html" class="related-word">{strongs} — {label}</a>')
    return "\n".join(links)

def make_ext(strongs_id):
    num = strongs_id[1:]
    lang = strongs_id[0].lower()
    if lang == 'h':
        return f"""                <a href="https://www.stepbible.org/?q=strong=H{num}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/h{num}/kjv/wlc/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/hebrew/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>"""
    else:
        return f"""                <a href="https://www.stepbible.org/?q=strong=G{num}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/g{num}/kjv/mgnt/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/greek/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>"""

def build_page(strongs_id, script_dir, original, translit, pos, gloss,
               definition, theology, verses, related):
    num = strongs_id[1:]
    lang_label = "Hebrew · Old Testament" if strongs_id[0] == "H" else "Greek · New Testament"
    verses_html = "\n".join([make_verse(r, t) for r, t in verses])
    related_html = make_related(related)
    ext_html = make_ext(strongs_id)
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
    <meta property="og:description" content="{gloss} — {'Hebrew' if strongs_id[0]=='H' else 'Greek'} word study from the {'Old' if strongs_id[0]=='H' else 'New'} Testament. Strong's {strongs_id}.">
    <meta name="description" content="{gloss} — {'Hebrew' if strongs_id[0]=='H' else 'Greek'} word study. Strong's {strongs_id}. USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{strongs_id} — {translit} ({gloss}) | USMC Ministries Lexicon</title>
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
            <span class="strongs-badge">{strongs_id} · {lang_label}</span>
            <div class="original-word">{original}</div>
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
{verses_html}
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
{ext_html}
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

# ============================================================
# WORD DATA — 24 Hebrew + 23 Greek
# ============================================================
WORDS = [
    # ---- HEBREW ----
    {
        "id": "H3389",
        "original": "יְרוּשָׁלַיִם",
        "translit": "Yerushalayim",
        "pos": "Proper noun, feminine",
        "gloss": "Jerusalem",
        "definition": "The name <em>Yerushalayim</em> (Jerusalem) appears over 660 times in the Hebrew Bible, more than any other city. Its etymology likely combines <em>yireh</em> (he will see/provide) and <em>shalem</em> (peace/wholeness), yielding the sense of \"city of peace\" or \"foundation of peace.\" The city first appears as Salem in Genesis 14:18, ruled by the priest-king Melchizedek.",
        "theology": "Jerusalem occupies the theological center of the Hebrew scriptures as the place God chose for His name to dwell (1 Kings 8:29). As the city of David, it became the seat of Israel's monarchy and the home of the Temple — the meeting point of heaven and earth. The prophets envision a New Jerusalem, a transformed city where God dwells with His people in ultimate peace and righteousness (Isaiah 65:17–19; Zechariah 8:3). This hope is consummated in Revelation 21.",
        "verses": [
            ("Psalm 122:6", "Pray for the peace of <em>Jerusalem</em>: \"May those who love you be secure.\""),
            ("Isaiah 52:1", "Awake, awake, O <em>Zion</em>, clothe yourself with strength! Put on your garments of splendor, O <em>Jerusalem</em>, the holy city."),
            ("Zechariah 8:3", "This is what the LORD says: 'I will return to Zion and dwell in <em>Jerusalem</em>. Then Jerusalem will be called the Faithful City.'"),
            ("Psalm 137:5–6", "If I forget you, O <em>Jerusalem</em>, may my right hand forget its skill. May my tongue cling to the roof of my mouth if I do not remember you."),
            ("Isaiah 62:6–7", "I have posted watchmen on your walls, O <em>Jerusalem</em>; they will never be silent day or night. You who call on the LORD, give yourselves no rest."),
        ],
        "related": [("H6726", "Tsiyyon (Zion)"), ("H1004", "Bayit (House/Temple)"), ("H7965", "Shalom (Peace)")],
    },
    {
        "id": "H5892",
        "original": "עִיר",
        "translit": "Ir",
        "pos": "Noun, feminine",
        "gloss": "City",
        "definition": "The Hebrew <em>ir</em> designates a walled or fortified settlement — a city or town. Appearing about 1,090 times in the Old Testament, it denotes both small towns and major urban centers. The word conveys the idea of a permanent, enclosed community in contrast to the open countryside (<em>sadeh</em>).",
        "theology": "Cities in the Old Testament represent both human achievement and human ambition gone wrong — from Cain's city (Genesis 4:17) to Babel (Genesis 11) to Nineveh. Yet God redeems the city concept: He establishes cities of refuge (Numbers 35), elects Jerusalem as His holy city, and promises a redeemed urban future. The New Jerusalem of Revelation is the ultimate <em>ir</em> — God's eternal dwelling among His people (Revelation 21:2).",
        "verses": [
            ("Genesis 4:17", "Cain built a <em>city</em>, and he named it after his son Enoch."),
            ("Numbers 35:6", "Six of the towns you give the Levites will be <em>cities</em> of refuge, to which a person who has killed someone may flee."),
            ("Proverbs 11:10", "When the righteous prosper, the <em>city</em> rejoices; when the wicked perish, there are shouts of joy."),
            ("Isaiah 1:21", "See how the faithful <em>city</em> has become a prostitute! She once was full of justice; righteousness used to dwell in her."),
            ("Proverbs 18:19", "A brother wronged is more unyielding than a fortified <em>city</em>; disputes are like the barred gates of a citadel."),
        ],
        "related": [("H3389", "Yerushalayim (Jerusalem)"), ("H5038", "Mibtsarim (Fortresses)"), ("H7704", "Sadeh (Field)")],
    },
    {
        "id": "H4467",
        "original": "מַמְלָכָה",
        "translit": "Mamlakah",
        "pos": "Noun, feminine",
        "gloss": "Kingdom / Reign",
        "definition": "The Hebrew <em>mamlakah</em> denotes the realm, dominion, or reign of a king — a kingdom as both territory and royal authority. Derived from the root <em>malak</em> (to reign), it appears about 117 times in the Old Testament. It is distinct from <em>malkuth</em> (which emphasizes the rule itself) though often used interchangeably.",
        "theology": "The concept of <em>mamlakah</em> runs through the entire biblical narrative. Israel's request for a king (1 Samuel 8) introduces human monarchy, but God always remains the true King. The prophets anticipate a messianic <em>mamlakah</em> — the kingdom of God established through David's son (2 Samuel 7:12–16). This hope finds fulfillment in Jesus, whose kingdom is both present and coming (Matthew 4:17). The <em>mamlakah</em> of priests (Exodus 19:6) foreshadows the royal priesthood of all believers (1 Peter 2:9).",
        "verses": [
            ("Exodus 19:6", "You will be for me a <em>kingdom</em> of priests and a holy nation."),
            ("2 Samuel 7:16", "Your house and your <em>kingdom</em> will endure forever before me; your throne will be established forever."),
            ("Daniel 2:44", "In the time of those kings, the God of heaven will set up a <em>kingdom</em> that will never be destroyed."),
            ("Obadiah 1:21", "And the <em>kingdom</em> will be the LORD's."),
            ("Psalm 145:13", "Your <em>kingdom</em> is an everlasting kingdom, and your dominion endures through all generations."),
        ],
        "related": [("H4428", "Melek (King)"), ("H4438", "Malkuth (Royalty/Reign)"), ("H7287", "Radah (Rule/Dominion)")],
    },
    {
        "id": "H5221",
        "original": "נָכָה",
        "translit": "Nakah",
        "pos": "Verb, Hiphil",
        "gloss": "Strike / Smite",
        "definition": "The Hebrew <em>nakah</em> is a common verb meaning to strike, smite, beat, or kill. It appears about 500 times in the Old Testament and covers a wide range of physical blows — from a light tap to a lethal strike. The Hiphil stem (causative) dominates, meaning \"to cause to be struck.\" It is used of both human and divine action.",
        "theology": "<em>Nakah</em> is a theologically charged verb in Scripture. God strikes down Egypt's firstborn (Exodus 12:29), smites Israel's enemies, and disciplines His own people in covenant faithfulness. The prophetic suffering-servant passage uses this root: \"He was <em>stricken</em> by God, smitten by him, and afflicted\" (Isaiah 53:4). This points directly to Christ's atonement — the righteous one struck for the unrighteous. The verb thus bridges divine judgment and substitutionary grace.",
        "verses": [
            ("Exodus 12:29", "At midnight the LORD <em>struck</em> down all the firstborn in Egypt."),
            ("Isaiah 53:4", "Yet we considered him punished by God, <em>stricken</em> by him, and afflicted."),
            ("Zechariah 13:7", "\"Strike the shepherd, and the sheep will be scattered.\""),
            ("2 Samuel 24:17", "When David saw the angel who was <em>striking</em> down the people, he said to the LORD, 'I have sinned.'"),
            ("Numbers 14:42", "Do not go up, because the LORD is not with you. You will be <em>struck</em> down by your enemies."),
        ],
        "related": [("H2026", "Harag (Kill/Murder)"), ("H4194", "Mavet (Death)"), ("H3467", "Yasha (Save/Deliver)")],
    },
    {
        "id": "H6943",
        "original": "קֶדֶשׁ",
        "translit": "Qedesh",
        "pos": "Noun, masculine",
        "gloss": "Sacred place / Holy",
        "definition": "<em>Qedesh</em> can refer to a holy or sacred place, or to a male shrine prostitute (in its negative usage). As a place-name, Qedesh was a significant city in Naphtali that served as a city of refuge (Joshua 20:7). The root <em>qadash</em> (to be holy, set apart) connects it to the entire biblical theme of holiness and separation unto God.",
        "theology": "The concept of a <em>qedesh</em> (sacred place) parallels the theology of the Tabernacle and Temple — spaces set apart for divine encounter. However, Israel was repeatedly warned against Canaanite <em>qedeshim</em> (cultic prostitutes), as mixing worship with sexuality profaned the holiness of God (Deuteronomy 23:17). True holiness is ethical and relational, not ritualistic or sensual. God's holy places in Scripture exist to facilitate covenant relationship, not transactional religion.",
        "verses": [
            ("Joshua 20:7", "So they set apart <em>Kedesh</em> in Galilee in the hill country of Naphtali... as cities of refuge."),
            ("Deuteronomy 23:17", "No Israelite man or woman is to become a shrine prostitute [<em>qadesh</em>]."),
            ("Judges 4:9", "Deborah said, 'I will go with you. But because of the way you are going about this, the honor will not be yours, for the LORD will deliver Sisera into the hands of a woman.' — [Deborah judged at Kadesh-Barnea region]"),
            ("1 Kings 14:24", "There were even <em>shrine prostitutes</em> in the land; the people engaged in all the detestable practices of the nations the LORD had driven out before the Israelites."),
            ("Isaiah 6:3", "And they were calling to one another: 'Holy, holy, holy is the LORD Almighty; the whole earth is full of his glory.' [same qadash root]"),
        ],
        "related": [("H6918", "Qadosh (Holy)"), ("H6944", "Qodesh (Holiness/Sanctuary)"), ("H4720", "Miqdash (Sanctuary)")],
    },
    {
        "id": "H2351",
        "original": "חוּץ",
        "translit": "Chuts",
        "pos": "Noun, masculine / Adverb",
        "gloss": "Outside / Street",
        "definition": "<em>Chuts</em> means the outside, the open space, or the street — the area beyond a building or city wall. It functions both as a noun (\"the street,\" \"the open field\") and an adverb (\"outside,\" \"without\"). Appearing about 164 times, it is often used in the phrase <em>ba-chuts</em> (\"in the street/outside\") to contrast interior sacred or domestic space with the public realm.",
        "theology": "In biblical theology, the outside (<em>chuts</em>) can be a place of exposure, shame, and danger (Proverbs 22:13), but also a place of bold proclamation. Wisdom cries out in the streets (Proverbs 1:20). Jesus suffered \"outside the gate\" (Hebrews 13:12–13), bearing the shame of the excluded. This inverts the inside/outside dynamic: the Holy One went to the <em>chuts</em> so the outcast could come in.",
        "verses": [
            ("Proverbs 1:20", "Out in the open wisdom calls aloud, she raises her voice in the public square [<em>chuts</em>]."),
            ("Proverbs 22:13", "The sluggard says, 'There's a lion <em>outside</em>! I'll be killed in the public square!'"),
            ("Lamentations 4:14", "Now they grope through the streets [<em>chuts</em>] as if they were blind."),
            ("Jeremiah 9:21", "Death has climbed in through our windows and has entered our fortresses; it has removed the children from the streets [<em>chuts</em>]."),
            ("Proverbs 7:12", "Now in the street, now in the squares, at every corner she lurks."),
        ],
        "related": [("H7784", "Shuq (Marketplace/Street)"), ("H8179", "Shaar (Gate)"), ("H1004", "Bayit (House)")],
    },
    {
        "id": "H8010",
        "original": "שְׁלֹמֹה",
        "translit": "Shelomoh",
        "pos": "Proper noun, masculine",
        "gloss": "Solomon",
        "definition": "<em>Shelomoh</em> is the name of Israel's third king, son of David and Bathsheba. The name derives from <em>shalom</em> (peace), meaning \"peaceable\" or \"his peace.\" God gave him the additional name Jedidiah (\"beloved of the LORD\") through the prophet Nathan (2 Samuel 12:25). Solomon reigned approximately 970–930 BC and was renowned for wisdom, wealth, and his building of the First Temple.",
        "theology": "Solomon represents the apogee and tragedy of the Davidic kingdom. Granted unparalleled wisdom (1 Kings 3), he built the Temple as God's earthly dwelling place — yet he ultimately multiplied wives, horses, and gold in direct violation of Deuteronomy 17:16–17, leading Israel into idolatry. He is a warning that wisdom without obedience fails. Jesus identified Himself as \"greater than Solomon\" (Matthew 12:42) — the true King who embodies both wisdom and righteousness without compromise.",
        "verses": [
            ("1 Kings 3:12", "I will do what you have asked. I will give you a wise and discerning heart, so that there will never have been anyone like you, nor will there ever be."),
            ("1 Kings 6:1", "Solomon began to build the temple of the LORD."),
            ("Ecclesiastes 12:13", "Fear God and keep his commandments, for this is the duty of all mankind. [Solomon's conclusion]"),
            ("Matthew 12:42", "The Queen of the South will rise at the judgment with this generation and condemn it; for she came from the ends of the earth to listen to <em>Solomon's</em> wisdom, and now something greater than Solomon is here."),
            ("Song of Songs 1:5", "Dark am I, yet lovely, daughters of Jerusalem, dark like the tents of Kedar, like the tent curtains of <em>Solomon</em>."),
        ],
        "related": [("H1732", "David (Beloved)"), ("H7965", "Shalom (Peace)"), ("H2454", "Chokmah (Wisdom)")],
    },
    {
        "id": "H7704",
        "original": "שָׂדֶה",
        "translit": "Sadeh",
        "pos": "Noun, masculine",
        "gloss": "Field / Open country",
        "definition": "The Hebrew <em>sadeh</em> refers to an open field, cultivated land, or the open countryside — as opposed to a city or enclosed area. It appears about 333 times and can designate agricultural land, a wilderness area, or any open expanse. The related term <em>sade</em> (often used interchangeably) emphasizes the flat, spread-out nature of the terrain.",
        "theology": "<em>Sadeh</em> is the stage for many pivotal biblical events: Isaac meditates in the field at evening (Genesis 24:63), Jacob encounters God, Ruth gleans in Boaz's field, and the blood field of Judas (Matthew 27:8 echoes Zechariah 11:13). The field as contested ground — between toil and rest, life and death — reflects humanity's post-Eden condition (Genesis 3:18). The lilies of the <em>field</em> (Matthew 6:28–30) become a teaching on divine provision and freedom from anxiety.",
        "verses": [
            ("Genesis 3:18", "It will produce thorns and thistles for you, and you will eat the plants of the <em>field</em>."),
            ("Ruth 2:3", "So she went out, entered a <em>field</em> and began to glean behind the harvesters."),
            ("Psalm 103:15", "The life of mortals is like grass, they flourish like a flower of the <em>field</em>."),
            ("Isaiah 40:8", "The grass withers and the flowers fall, but the word of our God endures forever."),
            ("Micah 4:10", "Writhe in agony, Daughter Zion, like a woman in labor, for now you must leave the city to camp in the open <em>field</em>."),
        ],
        "related": [("H1250", "Bar (Grain/Open)")  , ("H5892", "Ir (City)"), ("H3293", "Yaar (Forest/Thicket)")],
    },
    {
        "id": "H5799",
        "original": "עֲזָאזֵל",
        "translit": "Azazel",
        "pos": "Proper noun / Noun",
        "gloss": "Scapegoat / Azazel",
        "definition": "<em>Azazel</em> appears four times in Leviticus 16, exclusively in the context of the Day of Atonement (Yom Kippur) ritual. The precise meaning is debated: it may be a place name (a remote wilderness), the name of a demonic entity, or a compound meaning \"goat of departure\" (<em>ez azal</em> — goat that goes away). In the ritual, one goat was sacrificed and one was sent into the wilderness \"for Azazel.\"",
        "theology": "The scapegoat ritual powerfully dramatizes the removal of sin from the covenant community. While one goat's blood atoned for sin (making it possible to stand before a holy God), the <em>Azazel</em>-goat visually demonstrated the complete removal of guilt — carried far away, never to return. This two-goat ritual previews the double-blessing of Christ's atonement: His blood cleanses our guilt and His resurrection removes the power of sin (Romans 4:25). Sin is not merely covered but expelled.",
        "verses": [
            ("Leviticus 16:8", "He is to cast lots for the two goats — one lot for the LORD and the other for <em>Azazel</em>."),
            ("Leviticus 16:10", "But the goat chosen by lot as the scapegoat shall be presented alive before the LORD to be used for making atonement by sending it into the wilderness as a scapegoat [<em>Azazel</em>]."),
            ("Leviticus 16:21–22", "Aaron shall lay both hands on the head of the live goat and confess over it all the wickedness... and send the goat away into the wilderness."),
            ("Isaiah 53:6", "We all, like sheep, have gone astray, each of us has turned to our own way; and the LORD has laid on him the iniquity of us all."),
            ("Psalm 103:12", "As far as the east is from the west, so far has he removed our transgressions from us."),
        ],
        "related": [("H3725", "Kippur (Atonement)"), ("H8163", "Sair (Goat/He-goat)"), ("H2403", "Chata'ah (Sin Offering)")],
    },
    {
        "id": "H3063",
        "original": "יְהוּדָה",
        "translit": "Yehudah",
        "pos": "Proper noun, masculine",
        "gloss": "Judah",
        "definition": "<em>Yehudah</em> is the name of the fourth son of Jacob and Leah, derived from the verb <em>yadah</em> (to praise, to give thanks). Leah named him saying, \"This time I will praise the LORD\" (Genesis 29:35). Judah became the ancestor of the tribe from which David and ultimately Jesus descended. The southern kingdom after Solomon's division also bore this name.",
        "theology": "Judah's trajectory in Genesis is one of the Bible's most compelling character arcs: from cowardly complicity in selling Joseph (Genesis 37) to self-sacrificing intercession for Benjamin (Genesis 44:33–34). This transformation becomes the prototype of true repentance and leadership. The messianic blessing of Genesis 49:8–12 declares that the scepter will not depart from Judah — a promise fulfilled in Jesus, the \"Lion of the tribe of Judah\" (Revelation 5:5). Judah's name meaning (praise) foreshadows a kingdom marked by worship.",
        "verses": [
            ("Genesis 29:35", "She conceived again, and when she gave birth to a son she said, 'This time I will praise the LORD.' So she named him <em>Judah</em>."),
            ("Genesis 49:10", "The scepter will not depart from <em>Judah</em>, nor the ruler's staff from between his feet, until he to whom it belongs shall come."),
            ("Micah 5:2", "But you, Bethlehem <em>Ephrathah</em>, though you are small among the clans of Judah, out of you will come for me one who will be ruler over Israel."),
            ("Revelation 5:5", "The Lion of the tribe of <em>Judah</em>, the Root of David, has triumphed."),
            ("Hebrews 7:14", "For it is clear that our Lord descended from <em>Judah</em>."),
        ],
        "related": [("H3290", "Yaakov (Jacob)"), ("H1732", "David (David)"), ("H3084", "Yehudah alt. (Praise)")],
    },
    {
        "id": "H2481",
        "original": "חֲלִי",
        "translit": "Chali",
        "pos": "Noun, masculine",
        "gloss": "Ornament / Jewel",
        "definition": "<em>Chali</em> refers to an ornament, jewel, or piece of jewelry — something worn for beauty or adornment. Appearing about 8 times, it derives from the root <em>chalah</em> (to be weak, sick) in an ironic way, or more likely from an unused root meaning \"to shine.\" It describes personal adornments such as necklaces, pendants, or decorative pieces worn as displays of wealth or status.",
        "theology": "In Scripture, ornaments (<em>chali</em>) serve as symbols of covenant blessing (Proverbs 25:12 — wise rebuke as a gold earring), but also as markers of pride and idolatry. Isaiah 3 lists the ornaments of Jerusalem's daughters as emblems of complacency that will be stripped away in judgment (Isaiah 3:18–23). True adornment in the Bible is not outward jewelry but inward character — the \"unfading beauty of a gentle and quiet spirit\" (1 Peter 3:4). Wisdom is the most beautiful ornament.",
        "verses": [
            ("Proverbs 25:12", "Like an earring of gold or an <em>ornament</em> of fine gold is the rebuke of a wise judge to a listening ear."),
            ("Isaiah 3:18", "In that day the Lord will snatch away their finery: the bangles and headbands and crescent necklaces, the earrings and bracelets and <em>ornaments</em>."),
            ("Song of Songs 7:1", "How beautiful your sandaled feet, O prince's daughter! Your graceful legs are like <em>jewels</em>, the work of an artist's hands."),
            ("Hosea 2:13", "I will punish her for the days she burned incense to the Baals; she decked herself with rings and <em>jewelry</em>, and went after her lovers."),
            ("Proverbs 1:9", "For they are a garland to grace your head and a chain to adorn your neck. [chali-related wisdom imagery]"),
        ],
        "related": [("H5716", "Adi (Ornament/Jewel)"), ("H3800", "Kethem (Pure Gold)"), ("H2454", "Chokmah (Wisdom)")],
    },
    {
        "id": "H7665",
        "original": "שָׁבַר",
        "translit": "Shavar",
        "pos": "Verb, Qal",
        "gloss": "Break / Shatter",
        "definition": "<em>Shavar</em> means to break, shatter, or smash — often applied to physical objects (pots, bones, tablets) but also to abstract realities like pride, covenants, and the spirit. Appearing about 148 times, it encompasses both destructive breaking (in judgment) and redemptive breaking (as when hardened hearts are broken before God). The Niphal form means \"to be broken.\"",
        "theology": "<em>Shavar</em> expresses both God's judgment and His healing work. The breaking of tablets at Sinai (Exodus 32:19) dramatized covenant rupture. God \"breaks the bow\" of the mighty (1 Samuel 2:4) and \"breaks the gates of bronze\" to free captives (Isaiah 45:2). Crucially, God is near to those whose spirit is <em>broken</em> (Psalm 34:18 — <em>nishbar lev</em>). The Hebrew concept of brokenness before God is not weakness but the doorway to divine encounter — a crushed and broken heart God does not despise (Psalm 51:17).",
        "verses": [
            ("Psalm 34:18", "The LORD is close to the brokenhearted and saves those who are crushed [<em>broken</em>] in spirit."),
            ("Psalm 51:17", "My sacrifice, O God, is a broken spirit; a broken and contrite heart you, God, will not despise."),
            ("Exodus 32:19", "When Moses approached the camp and saw the calf and the dancing, his anger burned and he threw the tablets out of his hands, breaking [<em>shavar</em>] them to pieces."),
            ("Isaiah 42:3", "A bruised reed he will not break, and a smoldering wick he will not snuff out."),
            ("Jeremiah 23:29", "'Is not my word like fire,' declares the LORD, 'and like a hammer that <em>breaks</em> a rock in pieces?'"),
        ],
        "related": [("H7533", "Ratsats (Crush/Oppress)"), ("H2522", "Chalash (Weaken)"), ("H7495", "Rapha (Heal)")],
    },
    {
        "id": "H4603",
        "original": "מָעַל",
        "translit": "Maal",
        "pos": "Verb, Qal",
        "gloss": "Act unfaithfully / Trespass",
        "definition": "<em>Maal</em> means to act unfaithfully, to commit a trespass, or to violate sacred trust — particularly in the context of covenant relationship. It appears about 35 times as a verb (plus the noun <em>maal</em> for \"unfaithfulness\"). The concept encompasses embezzlement of sacred property, marital unfaithfulness, and most critically, Israel's unfaithfulness to God.",
        "theology": "<em>Maal</em> is the word used when Israel commits sacrilege against God — taking what belongs to Him, violating His holiness, or betraying covenant loyalty. Achan's sin (Joshua 7:1) is called <em>maal</em>. The unfaithful husband or wife is described as committing <em>maal</em> (Numbers 5:12). Chronicles repeatedly uses this word to explain Israel's exile: persistent <em>maal</em> led to the Babylonian captivity (2 Chronicles 36:14). The gravity of <em>maal</em> lies in its relational dimension — it is not merely sin but the betrayal of someone's trust.",
        "verses": [
            ("Joshua 7:1", "But the Israelites were unfaithful [<em>maal</em>] in regard to the devoted things; Achan... took some of them."),
            ("2 Chronicles 36:14", "Furthermore, all the leaders of the priests and the people became more and more unfaithful [<em>maal</em>], following all the detestable practices of the nations."),
            ("Ezekiel 14:13", "Son of man, if a country sins against me by being unfaithful [<em>maal</em>] and I stretch out my hand against it to cut off its food supply..."),
            ("Numbers 5:12", "If a man's wife goes astray and is unfaithful [<em>maal</em>] to him..."),
            ("1 Chronicles 10:13", "Saul died because he was unfaithful [<em>maal</em>] to the LORD; he did not keep the word of the LORD."),
        ],
        "related": [("H898", "Bagad (Treachery/Betray)"), ("H2398", "Chata (Sin)"), ("H530", "Emunah (Faithfulness)")],
    },
    {
        "id": "H3684",
        "original": "כְּסִיל",
        "translit": "Kesil",
        "pos": "Noun, masculine",
        "gloss": "Fool / Dullard",
        "definition": "<em>Kesil</em> is the most common Hebrew word for \"fool\" in Proverbs, appearing about 49 times. Unlike <em>nabal</em> (a morally corrupt fool) or <em>ewil</em> (a stubborn simpleton), <em>kesil</em> describes someone who is mentally thick, dull, or fatuous — one who has rejected wisdom through deliberate lifestyle choices. The term carries the connotation of sluggishness of mind combined with moral obtuseness.",
        "theology": "In Proverbs' wisdom framework, the <em>kesil</em> is not intellectually incapable but willfully resistant to correction. He despises rebuke (Proverbs 12:1), returns to his folly (Proverbs 26:11), trusts his own heart (Proverbs 28:26), and brings grief to his parents (Proverbs 10:1). The <em>kesil</em> is the antithesis of the wise (<em>chakam</em>). Biblical wisdom insists that true intelligence is not measured by IQ but by fear of the LORD and receptivity to correction. The greatest fool is the one who knows better and refuses to act on it.",
        "verses": [
            ("Proverbs 10:1", "A wise son brings joy to his father, but a foolish [<em>kesil</em>] son brings grief to his mother."),
            ("Proverbs 26:11", "As a dog returns to its vomit, so fools [<em>kesil</em>] repeat their folly."),
            ("Proverbs 17:10", "A rebuke impresses a discerning person more than a hundred lashes a fool [<em>kesil</em>]."),
            ("Proverbs 29:11", "Fools [<em>kesil</em>] give full vent to their rage, but the wise bring calm in the end."),
            ("Ecclesiastes 5:3", "A dream comes when there are many cares, and many words mark the speech of a fool [<em>kesil</em>]."),
        ],
        "related": [("H5036", "Nabal (Vile Fool)"), ("H191", "Ewil (Foolish/Stubborn)"), ("H2454", "Chokmah (Wisdom)")],
    },
    {
        "id": "H3701",
        "original": "כֶּסֶף",
        "translit": "Keseph",
        "pos": "Noun, masculine",
        "gloss": "Silver / Money",
        "definition": "<em>Keseph</em> is the standard Hebrew word for silver, appearing about 403 times in the Old Testament. Since coined money was not common in ancient Israel until later periods, <em>keseph</em> (silver by weight) served as currency. The word can mean both the metal itself and money in general. Its root may mean \"to be pale\" or \"to long for\" (desire for silver).",
        "theology": "Silver in Scripture occupies complex theological terrain. It is a measure of value (30 pieces of silver was the price of a slave, Exodus 21:32), a material for sacred vessels in the Tabernacle, and a metaphor for refined speech (Proverbs 10:20 — \"the tongue of the righteous is choice silver\"). The love of silver (<em>keseph</em>) is condemned as a root of greed (Ecclesiastes 5:10). Most significantly, Zechariah 11:12–13 prophesies 30 pieces of silver as the \"price\" for the good shepherd — fulfilled in Judas' betrayal of Jesus (Matthew 26:15).",
        "verses": [
            ("Proverbs 10:20", "The tongue of the righteous is choice <em>silver</em>, but the heart of the wicked is of little value."),
            ("Zechariah 11:12", "I told them, 'If you think it best, give me my pay; but if not, keep it.' So they paid me thirty pieces of <em>silver</em>."),
            ("Psalm 12:6", "And the words of the LORD are flawless, like <em>silver</em> purified in a crucible, like gold refined seven times."),
            ("Proverbs 17:3", "The crucible for <em>silver</em> and the furnace for gold, but the LORD tests the heart."),
            ("Ecclesiastes 5:10", "Whoever loves <em>money</em> never has enough; whoever loves wealth is never satisfied with their income."),
        ],
        "related": [("H2091", "Zahav (Gold)"), ("H5178", "Nechoshet (Bronze/Copper)"), ("H4242", "Mechir (Price/Value)")],
    },
    {
        "id": "H5766",
        "original": "עַוְלָה",
        "translit": "Avlah",
        "pos": "Noun, feminine",
        "gloss": "Wickedness / Injustice",
        "definition": "<em>Avlah</em> (also spelled <em>awlah</em>) refers to moral wickedness, injustice, or perversity — a deviation from what is right and straight. Appearing about 32 times, it is closely related to <em>avel</em> (unrighteous one) and contrasts sharply with <em>tsedaqah</em> (righteousness/justice). It describes both individual moral corruption and systemic injustice in society.",
        "theology": "<em>Avlah</em> is the opposite of God's character and of the covenant life He calls Israel to. God is declared to have no <em>avlah</em> in Him (Deuteronomy 32:4) — He is perfectly just and right. The prophets cry out against <em>avlah</em> in courts, commerce, and worship. One of the most devastating charges against Israel is that <em>avlah</em> was found in their midst (Ezekiel 28:15). Because God is righteous, He cannot overlook wickedness — it must be judged or atoned for. Christ bore our <em>avlah</em> so we could receive His righteousness.",
        "verses": [
            ("Deuteronomy 32:4", "He is the Rock, his works are perfect, and all his ways are just. A faithful God who does no wrong [<em>avlah</em>], upright and just is he."),
            ("Psalm 92:15", "Proclaiming, 'The LORD is upright; he is my Rock, and there is no wickedness [<em>avlah</em>] in him.'"),
            ("Ezekiel 18:30", "Therefore, I will judge each of you, O house of Israel, according to your own ways, declares the Sovereign LORD. Repent! Turn away from all your <em>offenses</em>."),
            ("Zephaniah 3:13", "The remnant of Israel will do no wrong [<em>avlah</em>]; they will speak no lies, nor will deceit be found in their mouths."),
            ("Hosea 10:13", "But you have planted wickedness [<em>avlah</em>], you have reaped evil, you have eaten the fruit of deception."),
        ],
        "related": [("H5765", "Avel (Unrighteous)"), ("H6664", "Tsedeq (Righteousness)"), ("H4941", "Mishpat (Justice/Judgment)")],
    },
    {
        "id": "H6153",
        "original": "עֶרֶב",
        "translit": "Erev",
        "pos": "Noun, masculine",
        "gloss": "Evening / Sunset",
        "definition": "<em>Erev</em> means evening or sunset — the period from late afternoon through darkness. It appears about 134 times and is central to the biblical reckoning of time: in the Hebrew calendar, each day begins at sunset (<em>erev</em>), so evening precedes morning. The phrase <em>erev v'voker</em> (\"evening and morning\") appears in the creation account and the Daniel prophecy. The cognate verb <em>arav</em> means to become dark or to pledge/mix.",
        "theology": "The biblical day beginning at evening (<em>erev</em>) shapes Israel's entire liturgical calendar — Sabbath begins Friday evening, Passover begins at sunset, Yom Kippur is observed \"from evening to evening\" (Leviticus 23:32). This rhythm of darkness-before-light is deeply theological: before every divine morning there is an evening of waiting. The \"two evenings\" (<em>bein ha-arbayim</em>) of Exodus 12:6 (twilight) was when Passover lambs were slaughtered — the very time Jesus died. Evening becomes the hour of sacrifice and redemption.",
        "verses": [
            ("Genesis 1:5", "God called the light 'day,' and the darkness he called 'night.' And there was <em>evening</em>, and there was morning — the first day."),
            ("Exodus 12:6", "Take care of them until the fourteenth day of the month, when all the members of the community of Israel must slaughter them at twilight [between the two <em>evenings</em>]."),
            ("Psalm 55:17", "<em>Evening</em>, morning and noon I cry out in distress, and he hears my voice."),
            ("Leviticus 23:32", "It is a day of sabbath rest for you, and you must deny yourselves. From the <em>evening</em> of the ninth day of the month until the following evening you are to observe your sabbath."),
            ("Psalm 65:8", "The whole earth is filled with awe at your wonders; where morning dawns, where <em>evening</em> fades, you call forth songs of joy."),
        ],
        "related": [("H1242", "Boqer (Morning)"), ("H3117", "Yom (Day)"), ("H3915", "Layil (Night)")],
    },
    {
        "id": "H4885",
        "original": "מָשׂוֹשׂ",
        "translit": "Masos",
        "pos": "Noun, masculine",
        "gloss": "Joy / Exultation",
        "definition": "<em>Masos</em> denotes intense, exuberant joy or exultation — a gladness that overflows into expression. Appearing about 17 times, it comes from the root <em>sus</em> (to rejoice, exult). It describes the kind of joy associated with a wedding (Isaiah 62:5), harvest celebration, or the arrival of salvation. It is stronger than ordinary contentment — it is rapturous delight.",
        "theology": "Biblical joy is not circumstantial happiness but a deep theological reality rooted in God's saving acts. <em>Masos</em> captures this at its most intense. Jerusalem's <em>masos</em> was destroyed in the exile (Lamentations 5:15), but God promises to restore it — indeed to become Israel's <em>masos</em> (Isaiah 65:18–19). The New Testament counterpart is <em>agalliasis</em> (exultant joy) — the joy of those who see God's salvation. This joy is not escapism but the appropriate response to knowing the God who saves.",
        "verses": [
            ("Isaiah 62:5", "As a young man marries a young woman, so will your Builder marry you; as a bridegroom rejoices over his bride, so will your God rejoice [<em>masos</em>] over you."),
            ("Lamentations 5:15", "Joy [<em>masos</em>] is gone from our hearts; our dancing has turned to mourning."),
            ("Isaiah 24:11", "In the streets they cry out for wine; all joy [<em>masos</em>] turns to gloom, all joyful sounds are banished from the earth."),
            ("Isaiah 65:18", "But be glad and rejoice forever in what I will create, for I will create Jerusalem to be a delight and its people a <em>joy</em>."),
            ("Jeremiah 7:34", "I will bring an end to the sounds of joy and gladness and to the voices of bride and bridegroom in the towns of Judah."),
        ],
        "related": [("H8057", "Simchah (Gladness/Joy)"), ("H1524", "Gil (Rejoicing)"), ("H7440", "Rinnah (Joyful Shout)")],
    },
    {
        "id": "H4487",
        "original": "מָנָה",
        "translit": "Manah",
        "pos": "Verb, Qal",
        "gloss": "Number / Appoint / Assign",
        "definition": "<em>Manah</em> means to count, number, reckon, or appoint. It appears about 28 times and is related to the noun <em>maneh</em> (a unit of weight/money) and the noun <em>mannah</em> (manna — measured portion). The verb carries the sense of deliberate enumeration or calculated assignment — God numbering days, people, stars, or appointing specific persons for specific roles.",
        "theology": "<em>Manah</em> reveals that nothing in God's economy is arbitrary or left to chance. He numbers the stars and calls them each by name (Psalm 147:4). He has numbered our days (Psalm 90:12 — <em>menot</em>). Daniel 5 uses <em>mene</em> (numbered) as a divine verdict: God has numbered Belshazzar's kingdom and brought it to an end. Every life is counted and accounted for. Jesus' declaration that God knows the number of hairs on our head (Matthew 10:30) echoes this Hebrew concept of divine, intimate accounting.",
        "verses": [
            ("Daniel 5:26", "Here is what these words mean: <em>Mene</em>: God has numbered the days of your reign and brought it to an end."),
            ("Psalm 90:12", "Teach us to <em>number</em> our days, that we may gain a heart of wisdom."),
            ("Numbers 23:10", "Who can count the dust of Jacob or number even a fourth of Israel?"),
            ("Isaiah 53:12", "Therefore I will give him a portion among the great, and he will divide the spoils with the strong, because he poured out his life unto death, and was <em>numbered</em> with the transgressors."),
            ("Psalm 147:4", "He determines the number of the stars and calls them each by name."),
        ],
        "related": [("H5608", "Saphar (Count/Recount)"), ("H4480", "Min (From/Portion)"), ("H5612", "Sepher (Book/Scroll)")],
    },
    {
        "id": "H6965",
        "original": "קוּם",
        "translit": "Qum",
        "pos": "Verb, Qal",
        "gloss": "Arise / Rise up / Stand",
        "definition": "<em>Qum</em> is a fundamental Hebrew verb meaning to arise, rise up, stand, or be established. One of the most frequent verbs in the Hebrew Bible (appearing over 600 times), it is used of physical rising (getting up), of enemies rising against one, of establishing covenants, and — most significantly — of resurrection. The Hiphil means \"to raise up\" or \"to establish.\"",
        "theology": "<em>Qum</em> carries extraordinary theological weight as the verb most closely associated with resurrection hope in the Hebrew Bible. Job's declaration \"I know that my Redeemer lives, and that in the end he will <em>arise</em> (<em>yaqum</em>) on the earth\" (Job 19:25) is a resurrection affirmation. Isaiah 26:19 uses <em>qum</em> for the resurrection of the dead. Daniel 12:2 speaks of those who \"<em>awake</em>\" (<em>yaqitsu</em>, but the arise concept is parallel). When Jesus said \"<em>Qumi</em>\" (Talitha kum — \"Little girl, <em>arise</em>\"), He enacted the Hebrew resurrection hope.",
        "verses": [
            ("Job 19:25", "I know that my Redeemer lives, and that in the end he will <em>stand</em> [<em>yaqum</em>] upon the earth."),
            ("Isaiah 26:19", "But your dead will live, LORD; their bodies will <em>rise</em> [<em>yaqumu</em>]. You who dwell in the dust, wake up and shout for joy."),
            ("Psalm 3:7", "<em>Arise</em>, LORD! Deliver me, my God! Strike all my enemies on the jaw; break the teeth of the wicked."),
            ("Numbers 10:35", "Whenever the ark set out, Moses said, <em>Rise up</em>, LORD! May your enemies be scattered."),
            ("Micah 7:8", "Do not gloat over me, my enemy! Though I have fallen, I will <em>rise</em>. Though I sit in darkness, the LORD will be my light."),
        ],
        "related": [("H6966", "Qum (Aramaic - arise)"), ("H5782", "Ur (Awake/Arouse)"), ("H3467", "Yasha (Save/Deliver)")],
    },
    {
        "id": "H3394",
        "original": "יָרֵחַ",
        "translit": "Yareach",
        "pos": "Noun, masculine",
        "gloss": "Moon",
        "definition": "<em>Yareach</em> is the standard Hebrew word for the moon, appearing about 26 times. It may derive from a root related to wandering or the month. The related word <em>chodesh</em> (new moon, month) is more common for the monthly cycle. <em>Yareach</em> is the poetic and descriptive term for the luminous moon itself, distinguished from the sun (<em>shemesh</em>). A second, less frequent term <em>levanah</em> (the white one) also designates the moon.",
        "theology": "The moon in Hebrew thought is God's appointed servant — created on Day 4 \"to govern the night\" (Genesis 1:16) and to mark appointed times (<em>moedim</em>), seasons, and the sacred calendar. Unlike neighboring cultures that worshiped moon deities (Sin in Babylon), Israel was forbidden to bow down to the moon (Deuteronomy 4:19; Job 31:26–28). The moon reflects light it does not generate — a profound image of the believer's calling to reflect God's glory. Eschatologically, the moon's light will be surpassed by God's direct glory (Isaiah 60:19–20; Revelation 21:23).",
        "verses": [
            ("Genesis 1:16", "God made two great lights — the greater light to govern the day and the lesser light [<em>moon</em>] to govern the night."),
            ("Psalm 104:19", "He made the <em>moon</em> to mark the seasons, and the sun knows when to go down."),
            ("Joel 2:31", "The sun will be turned to darkness and the <em>moon</em> to blood before the coming of the great and dreadful day of the LORD."),
            ("Psalm 72:7", "In his days may the righteous flourish and prosperity abound till the <em>moon</em> is no more."),
            ("Isaiah 60:19", "The sun will no more be your light by day, nor will the brightness of the <em>moon</em> shine on you, for the LORD will be your everlasting light."),
        ],
        "related": [("H8121", "Shemesh (Sun)"), ("H2320", "Chodesh (New Moon/Month)"), ("H3556", "Kokav (Star)")],
    },
    {
        "id": "H7458",
        "original": "רָעָב",
        "translit": "Raav",
        "pos": "Noun, masculine",
        "gloss": "Famine / Hunger",
        "definition": "<em>Raav</em> means famine or severe hunger — the absence of adequate food resulting from drought, war, or divine judgment. Appearing about 101 times, it is closely linked to the verb <em>raev</em> (to be hungry). The word encompasses both the physical condition of starvation and the social catastrophe of widespread food scarcity. Famine was the most feared of ancient disasters.",
        "theology": "In the prophetic tradition, famine (<em>raav</em>) is one of God's covenant curses for disobedience (Deuteronomy 28:48) alongside sword and pestilence (the triple threat used by Jeremiah and Ezekiel). Yet God also provides miraculously in famine: Elijah is fed by ravens, Joseph's foresight saves Egypt and Israel, Ruth finds grain in Boaz's field. Amos prophesied a famine not of bread but of the word of God (Amos 8:11) — the deepest <em>raav</em>. Jesus, the Bread of Life (John 6:35), came to end this ultimate hunger.",
        "verses": [
            ("Genesis 12:10", "Now there was a <em>famine</em> in the land, and Abram went down to Egypt to live there for a while."),
            ("Amos 8:11", "\"The days are coming,\" declares the Sovereign LORD, \"when I will send a <em>famine</em> through the land — not a famine of food or a thirst for water, but a famine of hearing the words of the LORD.\""),
            ("Ruth 1:1", "In the days when the judges ruled, there was a <em>famine</em> in the land."),
            ("Psalm 37:19", "In times of <em>disaster</em> they will not wither; in days of <em>famine</em> they will enjoy plenty."),
            ("Romans 8:35", "Who shall separate us from the love of Christ? Shall trouble or hardship or persecution or <em>famine</em>?"),
        ],
        "related": [("H6635", "Tsaba (Host/Army — sword companion)"), ("H1698", "Dever (Plague/Pestilence)"), ("H3899", "Lechem (Bread/Food)")],
    },
    {
        "id": "H7722",
        "original": "שׁוֹא",
        "translit": "Sho'",
        "pos": "Noun, masculine",
        "gloss": "Devastation / Ruin / Desolation",
        "definition": "<em>Sho'</em> (also <em>shaw</em>) denotes sudden devastation, ruin, or desolation — the kind of catastrophic destruction that comes without warning. Appearing about 13 times, it often describes the sudden onset of calamity. Related to this root is <em>shav</em> (vanity/emptiness), used in the third commandment (\"not take the name of the LORD in vain\") — pointing to the destructive emptiness of profaning what is holy.",
        "theology": "<em>Sho'</em> in the prophetic literature depicts the judgment that falls on those who trust in false securities — Babylon's sudden fall (Isaiah 47:11), the destruction of the wicked (Job 30:3), the collapse of those who reject God. Psalm 35:8 prays that disaster (<em>sho'</em>) would fall upon the enemy unawares — echoing the pattern where unjust destroyers are themselves destroyed. The theological message: apart from God, all human strength is vulnerable to sudden <em>sho'</em>. Only the LORD is an indestructible refuge.",
        "verses": [
            ("Isaiah 47:11", "Disaster [<em>sho'</em>] will come upon you, and you will not know how to conjure it away."),
            ("Psalm 35:8", "May ruin [<em>sho'</em>] overtake them by surprise — may the net they hid entangle them."),
            ("Job 30:3", "Haggard from want and hunger, they roamed the parched land in desolate [<em>sho'</em>] wastelands at night."),
            ("Proverbs 1:27", "When calamity overtakes you like a storm, when disaster sweeps over you like a whirlwind, when distress and trouble overwhelm you."),
            ("Zephaniah 1:15", "That day will be a day of wrath — a day of distress and anguish, a day of trouble and ruin [<em>sho'</em>], a day of darkness and gloom."),
        ],
        "related": [("H7723", "Shav (Vanity/Emptiness)"), ("H7843", "Shachat (Destroy/Corrupt)"), ("H3444", "Yeshuah (Salvation)")],
    },
    {
        "id": "H6828",
        "original": "צָפוֹן",
        "translit": "Tsaphon",
        "pos": "Noun, masculine",
        "gloss": "North / Hidden",
        "definition": "<em>Tsaphon</em> means the north — the direction corresponding to the left when facing east (the direction of sunrise). Appearing about 153 times, it derives from the verb <em>tsaphan</em> (to hide, treasure up), perhaps because the north was the hidden or dark direction (away from the sun). In Ugaritic mythology, Mount Tsaphon was the dwelling of Baal, which makes the use of this term in Psalm 48 politically charged.",
        "theology": "The north (<em>tsaphon</em>) carries a complex symbolic range in Hebrew Scripture. Judgment comes \"from the north\" in the prophets — Jeremiah repeatedly warns of the \"foe from the north\" (Babylon: Jeremiah 1:14; 4:6). God's throne or dwelling is associated with the north/heights (Isaiah 14:13 — Lucifer's boast; Job 26:7 — God stretches the north over the void). Psalm 48:2 describes Zion as \"the heights of <em>Tsaphon</em>\" — deliberately appropriating Baal's mountain for Yahweh, declaring that the true God of the north is not Baal but the LORD.",
        "verses": [
            ("Jeremiah 1:14", "The LORD said to me, 'From the <em>north</em> disaster will be poured out on all who live in the land.'"),
            ("Psalm 48:2", "Beautiful in its loftiness, the joy of the whole earth, like the heights of <em>Zaphon</em> is Mount Zion, the city of the Great King."),
            ("Isaiah 14:13", "You said in your heart, 'I will ascend to the heavens... I will sit enthroned on the mount of assembly, on the utmost heights of Mount <em>Zaphon</em>.'"),
            ("Job 26:7", "He spreads out the <em>northern</em> skies over empty space; he suspends the earth over nothing."),
            ("Proverbs 25:23", "Like a <em>north</em> wind that brings unexpected rain is a sly tongue — which provokes a horrified look."),
        ],
        "related": [("H5045", "Negev (South)"), ("H4217", "Mizrach (East)"), ("H3220", "Yam (Sea/West)")],
    },
    # ---- GREEK ----
    {
        "id": "G3588",
        "original": "ὁ, ἡ, τό",
        "translit": "Ho, Hē, To",
        "pos": "Definite article",
        "gloss": "The",
        "definition": "The Greek definite article <em>ho/hē/to</em> is the most common word in the New Testament, appearing over 19,800 times. Unlike English \"the,\" the Greek article is fully declined — it has gender (masculine, feminine, neuter), number (singular, plural), and case (nominative, genitive, dative, accusative, vocative). The article often functions to identify, specify, or particularize a noun. Notably, Greek can use the article with abstract nouns, personal names, and whole phrases.",
        "theology": "The definite article in Greek carries profound theological weight in several key passages. John 1:1's \"the Word was God\" (<em>theos ēn ho logos</em>) is carefully constructed: the article before <em>logos</em> identifies it definitively, while its absence before <em>theos</em> indicates the predicate's qualitative nature — the Word is fully God in nature. Similarly, Colossians 2:9 uses the article to declare \"the fullness of deity\" (<em>pan to plērōma tēs theotētos</em>) dwells bodily in Christ. Small grammatical markers point to massive theological realities.",
        "verses": [
            ("John 1:1", "In the beginning was <em>the</em> Word, and <em>the</em> Word was with God, and <em>the</em> Word was God."),
            ("Romans 1:17", "For in <em>the</em> gospel <em>the</em> righteousness of God is revealed."),
            ("Matthew 5:3", "Blessed are <em>the</em> poor in spirit, for theirs is <em>the</em> kingdom of heaven."),
            ("John 14:6", "I am <em>the</em> way and <em>the</em> truth and <em>the</em> life."),
            ("Hebrews 1:3", "<em>The</em> Son is <em>the</em> radiance of God's glory and <em>the</em> exact representation of his being."),
        ],
        "related": [("G3739", "Hos (Who/Which — relative pronoun)"), ("G5101", "Tis (Who/What — interrogative)"), ("G3956", "Pas (All/Every)")],
    },
    {
        "id": "G3739",
        "original": "ὅς, ἥ, ὅ",
        "translit": "Hos, Hē, Ho",
        "pos": "Relative pronoun",
        "gloss": "Who / Which / That",
        "definition": "The Greek relative pronoun <em>hos/hē/ho</em> introduces relative clauses and refers back to an antecedent noun. It is fully declined and agrees with its antecedent in gender and number, but takes its case from its function within the relative clause. Appearing about 1,405 times in the NT, it is fundamental to constructing complex theological statements. The neuter <em>ho</em> can introduce clauses summarizing entire realities.",
        "theology": "Relative clauses introduced by <em>hos</em> often carry some of the NT's most concentrated Christological affirmations — what scholars call \"Christ hymns.\" Colossians 1:15 begins a magnificent Christological passage: \"He is [<em>hos</em>] the image of the invisible God.\" Philippians 2:6 (<em>hos en morphē theou</em> — \"who, being in very nature God\") and 1 Timothy 3:16 (<em>hos ephanerōthē en sarki</em> — \"who was revealed in the flesh\") use <em>hos</em> to launch creedal summaries. A tiny pronoun becomes the gateway to deep theology.",
        "verses": [
            ("Colossians 1:15", "The Son is the image of the invisible God, the firstborn over all creation. For in him all things were created — [<em>hos</em> — he <em>who</em> is]"),
            ("Philippians 2:6", "<em>Who</em>, being in very nature God, did not consider equality with God something to be used to his own advantage."),
            ("1 Timothy 3:16", "He <em>who</em> was revealed in the flesh, was vindicated by the Spirit, was seen by angels, was proclaimed among the nations."),
            ("John 1:12", "Yet to all <em>who</em> did receive him, to those <em>who</em> believed in his name, he gave the right to become children of God."),
            ("Romans 8:34", "<em>Who</em> then is the one <em>who</em> condemns? No one. Christ Jesus <em>who</em> died — more than that, <em>who</em> was raised to life."),
        ],
        "related": [("G3588", "Ho (The — definite article)"), ("G3754", "Hoti (That/Because — conjunction)"), ("G3748", "Hostis (Whoever/Which)")],
    },
    {
        "id": "G3754",
        "original": "ὅτι",
        "translit": "Hoti",
        "pos": "Conjunction",
        "gloss": "That / Because / For",
        "definition": "<em>Hoti</em> is one of the most common Greek conjunctions, appearing about 1,296 times in the NT. It serves two primary functions: (1) as a subordinating conjunction introducing indirect speech or content clauses (\"that\"); and (2) as a causal conjunction giving reason or explanation (\"because,\" \"for,\" \"since\"). Context determines which meaning is intended. It often follows verbs of saying, knowing, believing, or seeing.",
        "theology": "<em>Hoti</em> bridges theological declaration and its basis — connecting what is true with why it is true. The most theologically dense <em>hoti</em> clauses carry the weight of divine promises: \"I am convinced <em>that</em> neither death nor life... will be able to separate us from the love of God\" (Romans 8:38). \"God so loved the world <em>that</em> he gave his one and only Son\" (John 3:16). <em>Hoti</em> is the hinge on which vast theological truths swing — making explicit the content of faith and the reason for hope.",
        "verses": [
            ("John 3:16", "For God so loved the world <em>that</em> he gave his one and only Son."),
            ("Romans 8:28", "And we know <em>that</em> in all things God works for the good of those who love him."),
            ("1 John 4:10", "This is love: not <em>that</em> we loved God, but <em>that</em> he loved us and sent his Son as an atoning sacrifice for our sins."),
            ("Romans 10:9", "If you declare with your mouth, 'Jesus is Lord,' and believe in your heart <em>that</em> God raised him from the dead, you will be saved."),
            ("1 Corinthians 15:3–4", "For what I received I passed on to you as of first importance: <em>that</em> Christ died for our sins... <em>that</em> he was buried, <em>that</em> he was raised on the third day."),
        ],
        "related": [("G1063", "Gar (For — causal)"), ("G2443", "Hina (So that/In order that)"), ("G1487", "Ei (If — conditional)")],
    },
    {
        "id": "G3361",
        "original": "μή",
        "translit": "Mē",
        "pos": "Negative particle",
        "gloss": "Not (subjective/conditional)",
        "definition": "<em>Mē</em> is the subjective or conditional negation particle in Greek, as opposed to <em>ou/ouk/ouch</em> which negates objective facts. <em>Mē</em> appears about 1,042 times and is used with subjunctive, optative, imperative, and infinitive moods — any context involving will, wish, command, purpose, or possibility. It negates what is not the case from the speaker's perspective or in hypothetical situations.",
        "theology": "The distinction between <em>ou</em> (objective negation) and <em>mē</em> (subjective/volitional negation) matters theologically. When Jesus says \"Do not (<em>mē</em>) be afraid\" (Matthew 14:27), it is a command to stop letting fear control the will — not an assertion about external circumstances. Paul's \"by no means!\" (<em>mē genoito</em>) in Romans 6:2 is the strongest possible volitional negation — \"may it never be!\" This precision in negation reveals Scripture's nuanced view of human will, divine command, and the nature of faith.",
        "verses": [
            ("Matthew 6:13", "And lead us not [<em>mē</em>] into temptation, but deliver us from the evil one."),
            ("Romans 6:2", "By no means [<em>mē genoito</em>]! We are those who have died to sin; how can we live in it any longer?"),
            ("John 20:17", "Jesus said, 'Do not [<em>mē</em>] hold on to me, for I have not yet ascended to the Father.'"),
            ("Philippians 4:6", "Do not [<em>mē</em>] be anxious about anything, but in every situation, by prayer and petition... present your requests to God."),
            ("1 John 2:15", "Do not [<em>mē</em>] love the world or anything in the world."),
        ],
        "related": [("G3756", "Ou (Not — objective)"), ("G3762", "Oudeis (No one/Nothing)"), ("G3366", "Mēde (And not/Nor)")],
    },
    {
        "id": "G3382",
        "original": "μηρός",
        "translit": "Mēros",
        "pos": "Noun, masculine",
        "gloss": "Thigh",
        "definition": "<em>Mēros</em> means thigh, appearing only once in the New Testament (Revelation 19:16) but representing an important OT concept. In Greek culture the thigh was associated with strength and generation. In the Hebrew background, swearing on the thigh (euphemistically the generative organs) was a solemn oath (Genesis 24:2). Jacob's hip/thigh was touched by the angel at Peniel (Genesis 32:25).",
        "theology": "In Revelation 19:16, the returning King Jesus has a name written \"on his robe and on his <em>thigh</em>\" — KING OF KINGS AND LORD OF LORDS. This striking imagery combines royal proclamation with the ancient covenant oath tradition: His name on His thigh suggests the unbreakable, oath-bound authority of the Sovereign King. Jacob's wounded thigh (Genesis 32:25) taught him that divine encounter produces both blessing and permanent vulnerability — a limping worship that acknowledges God's supremacy. The weakness becomes the mark of grace.",
        "verses": [
            ("Revelation 19:16", "On his robe and on his <em>thigh</em> he has this name written: KING OF KINGS AND LORD OF LORDS."),
            ("Genesis 32:25", "When the man saw that he could not overpower him, he touched the socket of Jacob's hip so that his hip was wrenched as he wrestled with the man. [OT background to thigh oath]"),
            ("Genesis 24:2", "He said to the senior servant in his household, 'Put your hand under my <em>thigh</em>.'"),
            ("Genesis 24:9", "So the servant put his hand under the <em>thigh</em> of his master Abraham and swore an oath to him concerning this matter."),
            ("Psalm 45:3", "Gird your sword on your side, you mighty one; clothe yourself with splendor and majesty. [Royal warrior imagery parallel]"),
        ],
        "related": [("G1023", "Brachiōn (Arm/Strength)"), ("G3694", "Opisō (Behind/After)"), ("G935", "Basileus (King)")],
    },
    {
        "id": "G303",
        "original": "ἀνά",
        "translit": "Ana",
        "pos": "Preposition",
        "gloss": "Up / Each / Through",
        "definition": "<em>Ana</em> is a Greek preposition meaning \"up,\" \"each,\" \"through,\" or \"by.\" As a prefix in compound verbs it conveys upward motion, repetition, or reversal. In the NT it appears mainly in compounds and distributive expressions (\"apiece,\" \"each\"). Key compound verbs include <em>anabainō</em> (go up, ascend), <em>analambanō</em> (take up), <em>anastasis</em> (resurrection — literally, \"standing up again\"), and <em>anaginōskō</em> (read — \"know again\").",
        "theology": "<em>Ana</em> as a prefix is theologically ubiquitous: <em>anastasis</em> (resurrection) contains it at the core — the \"standing up again\" of the dead. <em>Anabainō</em> describes Christ's ascension (John 20:17). <em>Analambanō</em> is used for the assumption of Christ into heaven (Acts 1:2). The upward, reversal-of-death motion encoded in this prefix undergirds the entire NT theology of resurrection and exaltation. What has gone down — humanity, death — is reversed and raised <em>ana</em>.",
        "verses": [
            ("John 20:17", "Jesus said... 'I am ascending [<em>anabaino</em>] to my Father and your Father, to my God and your God.'"),
            ("Acts 1:2", "After giving instructions through the Holy Spirit to the apostles he had chosen, he was taken up [<em>anelēmphthē</em>]."),
            ("John 2:6", "Nearby stood six stone water jars... each [<em>ana</em>] holding from twenty to thirty gallons."),
            ("Revelation 4:8", "Each [<em>ana</em>] of the four living creatures had six wings."),
            ("Matthew 20:9–10", "Those who were hired about five in the afternoon came and each received [<em>ana</em>] a denarius."),
        ],
        "related": [("G386", "Anastasis (Resurrection)"), ("G305", "Anabainō (Go up/Ascend)"), ("G303", "Ana (Up — prefix root)")],
    },
    {
        "id": "G143",
        "original": "αἰσθάνομαι",
        "translit": "Aisthanoma",
        "pos": "Verb, middle/deponent",
        "gloss": "Perceive / Understand",
        "definition": "<em>Aisthanoma</em> means to perceive, comprehend, or understand — particularly through the senses or intuitive awareness. Appearing only once in the NT (Luke 9:45), it refers to understanding that comes through more than intellectual cognition — a whole-person grasping of reality. The noun <em>aisthēsis</em> (perception, discernment) appears in Philippians 1:9. The related word <em>aisthētērion</em> (faculty of perception) is used in Hebrews 5:14.",
        "theology": "Biblical knowing is never merely cerebral — it involves <em>aisthēsis</em>, a trained, holistic perception. Hebrews 5:14 says \"solid food is for the mature, who by constant use have trained their faculties (<em>aisthētēria</em>) to distinguish good from evil.\" This suggests that spiritual discernment is a skill developed through practice, not just inherited or instantly given. Paul's prayer in Philippians 1:9 that love would \"abound more and more in knowledge and depth of insight\" (<em>aisthēsei</em>) connects love with trained perception — seeing reality as God sees it.",
        "verses": [
            ("Luke 9:45", "But they did not <em>understand</em> what this meant. It was hidden from them, so that they did not grasp it."),
            ("Philippians 1:9", "And this is my prayer: that your love may abound more and more in knowledge and depth of insight [<em>aisthēsei</em>]."),
            ("Hebrews 5:14", "But solid food is for the mature, who by constant use have trained themselves to distinguish good from evil [<em>aisthētēria</em>]."),
            ("Luke 1:44", "As soon as the sound of your greeting reached my ears, the baby in my womb leaped for joy."),
            ("John 12:9", "Meanwhile a large crowd of Jews found out that Jesus was there and came, not only because of him but also to see Lazarus, whom he had raised from the dead."),
        ],
        "related": [("G1097", "Ginōskō (Know/Understand)"), ("G4907", "Sunesis (Understanding/Insight)"), ("G5428", "Phronēsis (Practical Wisdom)")],
    },
    {
        "id": "G218",
        "original": "ἀλείφω",
        "translit": "Aleiphō",
        "pos": "Verb, active",
        "gloss": "Anoint / Rub with oil",
        "definition": "<em>Aleiphō</em> means to anoint, rub, or smear with oil — specifically the common, everyday use of oil (as distinguished from the sacred anointing verb <em>chriō</em>, from which \"Christ\" derives). Appearing about 9 times in the NT, it describes anointing the head as hospitality (Luke 7:46), anointing the body after burial (Mark 16:1), anointing the sick (James 5:14), and the woman's anointing of Jesus' feet (Luke 7:38).",
        "theology": "<em>Aleiphō</em> and <em>chriō</em> represent the two dimensions of anointing: the human and the divine. While <em>chriō</em> designates sacred, authoritative anointing by God (as in \"the Christ\" = the Anointed One), <em>aleiphō</em> represents tangible, embodied love and care. The woman who anointed Jesus' feet with perfume (<em>aleiphō</em>) performed a prophetic act of devotion and burial preparation — an act Jesus said would be told wherever the gospel is preached (Matthew 26:13). James 5:14's instruction for elders to anoint with oil for healing uses <em>aleiphō</em> — the physical act accompanying prayer.",
        "verses": [
            ("James 5:14", "Is anyone among you sick? Let them call the elders of the church to pray over them and <em>anoint</em> them with oil in the name of the Lord."),
            ("Mark 16:1", "When the Sabbath was over, Mary Magdalene, Mary the mother of James, and Salome bought spices so that they might go to <em>anoint</em> Jesus' body."),
            ("Luke 7:46", "You did not put oil on my head, but she has <em>anointed</em> my feet with perfume."),
            ("John 11:2", "This Mary, whose brother Lazarus now lay sick, was the same one who poured perfume on the Lord and wiped his feet with her hair [<em>aleipsasa</em>]."),
            ("Matthew 6:17", "But when you fast, put oil on your head [<em>aleiphai</em>] and wash your face."),
        ],
        "related": [("G5548", "Chriō (Anoint — sacred/messianic)"), ("G5547", "Christos (Christ/Anointed One)"), ("G1637", "Elaion (Olive Oil)")],
    },
    {
        "id": "G312",
        "original": "ἀναγγέλλω",
        "translit": "Anaggellō",
        "pos": "Verb, active",
        "gloss": "Announce / Declare / Report",
        "definition": "<em>Anaggellō</em> means to announce, declare, or bring back a report — to relay information from one party to another. Appearing about 14 times in the NT, it is a compound of <em>ana</em> (up/back) and <em>aggellō</em> (announce/messenger), suggesting the bringing back of news or the full declaration of something. It is used of reporting back to authorities, declaring divine truths, and the proclamation of the gospel.",
        "theology": "John 4:25 provides a fascinating use: the Samaritan woman says the Messiah will \"<em>announce</em> all things\" to us — a recognition that the Christ's role includes divine revelation and disclosure. Jesus in John 16:13–15 uses <em>anaggellō</em> for the Spirit's ministry: \"He will tell [<em>anaggellei</em>] you what is yet to come... he will receive from me what he will make known to you.\" The Spirit's work is to faithfully declare what belongs to Christ. Acts 20:20,27 use it for Paul's complete declaration of the gospel — holding nothing back.",
        "verses": [
            ("John 4:25", "The woman said, 'I know that Messiah is coming. When he comes, he will <em>explain</em> everything to us.'"),
            ("John 16:13", "He will not speak on his own; he will speak only what he hears, and he will <em>tell</em> you what is yet to come."),
            ("Acts 20:27", "For I have not hesitated to <em>proclaim</em> to you the whole will of God."),
            ("1 Peter 1:12", "It was revealed to them that they were not serving themselves but you, when they spoke of the things that have now been <em>told</em> to you by those who have preached the gospel."),
            ("Acts 14:27", "When they arrived, they gathered the church together and <em>reported</em> all that God had done through them."),
        ],
        "related": [("G2097", "Euangelizō (Proclaim the Gospel)"), ("G2784", "Kērussō (Proclaim/Preach)"), ("G32", "Aggelos (Messenger/Angel)")],
    },
    {
        "id": "G352",
        "original": "ἀνακύπτω",
        "translit": "Anakuptō",
        "pos": "Verb, active",
        "gloss": "Lift up (one's head) / Stand erect",
        "definition": "<em>Anakuptō</em> means to lift up one's head, to straighten up, or to raise oneself up after being bowed down. It is a compound of <em>ana</em> (up) and <em>kuptō</em> (to stoop/bend). Appearing only 4 times in the NT, it is used of physical straightening (the bent woman healed by Jesus; rising from shame) and the eschatological lifting of the head at the approach of redemption (Luke 21:28).",
        "theology": "The most powerful theological use is Luke 21:28: \"When these things begin to take place, stand up and lift up your heads [<em>anakupsate</em>], because your redemption is drawing near.\" In contrast to the world's despair and fear at end-time events, disciples are to lift their faces — the physical posture of hope and anticipation. This is the same movement as the woman \"straightened up\" after 18 years of bondage (Luke 13:11–13) — liberation reverses the bent-over posture of oppression. Christ lifts what sin has bowed down.",
        "verses": [
            ("Luke 21:28", "When these things begin to take place, stand up and lift up your heads [<em>anakupsate</em>], because your redemption is drawing near."),
            ("Luke 13:11", "A woman was there who had been crippled by a spirit for eighteen years. She was bent over and could not straighten up [<em>anakupsai</em>] at all."),
            ("Luke 13:13", "Then he put his hands on her, and immediately she straightened up [<em>anōrthōthē</em>] and praised God."),
            ("John 8:7", "When they kept on questioning him, he straightened up [<em>anekupsen</em>] and said to them, 'Let any one of you who is without sin be the first to throw a stone at her.'"),
            ("John 8:10", "Jesus straightened up [<em>anakupsas</em>] and asked her, 'Woman, where are they? Has no one condemned you?'"),
        ],
        "related": [("G386", "Anastasis (Resurrection — raising up)"), ("G1869", "Epairō (Lift up)"), ("G629", "Apolytrōsis (Redemption)")],
    },
    {
        "id": "G703",
        "original": "ἀρετή",
        "translit": "Aretē",
        "pos": "Noun, feminine",
        "gloss": "Virtue / Excellence / Moral goodness",
        "definition": "<em>Aretē</em> is the classical Greek word for excellence, virtue, or moral goodness — the quality that makes something or someone outstanding in its proper function. In classical Greek philosophy (Plato, Aristotle), <em>aretē</em> was the highest human ideal — excellence of character. In the NT it appears only 5 times, suggesting the early Christians were selective about adopting this philosophically loaded term.",
        "theology": "The NT's use of <em>aretē</em> is theologically reorienting. In Philippians 4:8, Paul lists <em>aretē</em> among things worthy of thought — but places it in a distinctly Christian framework. 2 Peter 1:3 says God's divine power has given us everything needed for \"life and godliness through our knowledge of him who called us by his own glory and <em>aretē</em>\" — here God's own <em>aretē</em> is the basis for the call. The Christian vision of virtue is not self-cultivated Greek <em>aretē</em> but divine-imparted excellence through participation in Christ's nature (2 Peter 1:4–5).",
        "verses": [
            ("Philippians 4:8", "Finally, brothers and sisters, whatever is true... whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable — if anything is excellent [<em>aretē</em>] or praiseworthy — think about such things."),
            ("2 Peter 1:3", "His divine power has given us everything we need for a godly life through our knowledge of him who called us by his own glory and goodness [<em>aretē</em>]."),
            ("2 Peter 1:5", "For this very reason, make every effort to add to your faith goodness [<em>aretē</em>]; and to goodness, knowledge."),
            ("1 Peter 2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession, that you may declare the praises [<em>aretas</em>] of him who called you out of darkness."),
            ("Isaiah 43:21 LXX", "The people I formed for myself that they may proclaim my praise [<em>aretas</em>]."),
        ],
        "related": [("G5544", "Chrēstotēs (Kindness/Goodness)"), ("G19", "Agathōsunē (Goodness)"), ("G1343", "Dikaiosunē (Righteousness)")],
    },
    {
        "id": "G730",
        "original": "ἄρρην",
        "translit": "Arrēn",
        "pos": "Adjective / Noun",
        "gloss": "Male / Man",
        "definition": "<em>Arrēn</em> (also <em>arsēn</em>) means male — the biological designation of maleness, as opposed to <em>thēlys</em> (female). Appearing about 9 times in the NT, it emphasizes sexual distinction as a created biological reality. It differs from <em>anēr</em> (a man as a husband or adult male) and <em>anthrōpos</em> (a human person). <em>Arrēn</em> focuses on the basic category of maleness.",
        "theology": "Paul's use of <em>arsēn</em> in Romans 1:26–27 and 1 Corinthians 6:9 grounds sexual ethics in created order. In Romans 1, the exchange of natural relations between <em>thēlys</em> (female) and <em>arsēn</em> (male) is presented as a symptom of theological inversion — the rejection of the Creator reflected in the confusion of His creation. Galatians 3:28 uses <em>arsēn</em> in its counterpoint: \"There is neither <em>male</em> nor <em>female</em>\" in Christ — not erasing biological distinction but declaring equal dignity and access to grace. The <em>arsēn</em> firstborn being dedicated to God (Luke 2:23, citing Exodus 13:2) connects Jesus to the Passover deliverance.",
        "verses": [
            ("Matthew 19:4", "\"Haven't you read,\" he replied, \"that at the beginning the Creator made them <em>male</em> and female?\""),
            ("Romans 1:27", "In the same way the men also abandoned natural relations with women and were inflamed with lust for one another. <em>Men</em> committed shameful acts with other men."),
            ("Galatians 3:28", "There is neither Jew nor Gentile, neither slave nor free, nor is there <em>male</em> and female, for you are all one in Christ Jesus."),
            ("Luke 2:23", "As it is written in the Law of the Lord, 'Every firstborn <em>male</em> is to be consecrated to the Lord.'"),
            ("Revelation 12:5", "She gave birth to a son, a <em>male</em> child, who will rule all the nations with an iron scepter."),
        ],
        "related": [("G2338", "Thēlys (Female)"), ("G435", "Anēr (Man/Husband)"), ("G444", "Anthrōpos (Human being)")],
    },
    {
        "id": "G756",
        "original": "ἄρχομαι",
        "translit": "Archomai",
        "pos": "Verb, middle",
        "gloss": "Begin / Start",
        "definition": "<em>Archomai</em> is the middle-voice form of <em>archō</em>, meaning \"to begin\" or \"to start doing something.\" Appearing about 86 times in the NT, it is commonly followed by an infinitive: \"he began to teach\" (<em>ērxato didaskein</em>), \"they began to speak\" (<em>ērxanto lalein</em>). It is distinct from the active <em>archō</em> meaning \"to rule/govern.\" The word carries the Greek concept of <em>archē</em> (beginning, origin, first principle) at its root.",
        "theology": "The concept of beginning (<em>archē</em>) is foundational to the NT's theological framework. John 1:1 echoes Genesis 1:1: \"In the beginning (<em>en archē</em>) was the Word.\" Jesus' ministry is repeatedly described with <em>archomai</em> — marking inaugurated fulfillment. Luke uses it to signal new divine action: the Spirit leads, then Jesus \"<em>begins</em>.\" Acts uses it structurally (Acts 1:1 — \"all that Jesus <em>began</em> to do and teach\"). The implication is that what Jesus began in His incarnation, He continues through the Spirit and the Church — the story is not over.",
        "verses": [
            ("Acts 1:1", "In my former book, Theophilus, I wrote about all that Jesus <em>began</em> to do and to teach."),
            ("Mark 1:45", "Instead he went out and <em>began</em> to talk freely, spreading the news."),
            ("Luke 4:21", "He <em>began</em> by saying to them, 'Today this scripture is fulfilled in your hearing.'"),
            ("John 8:9", "At this, those who heard <em>began</em> to go away one at a time."),
            ("Matthew 4:17", "From that time on Jesus <em>began</em> to preach, 'Repent, for the kingdom of heaven has come near.'"),
        ],
        "related": [("G746", "Archē (Beginning/Rule)"), ("G757", "Archō (Rule — active voice)"), ("G4413", "Prōtos (First)")],
    },
    {
        "id": "G757",
        "original": "ἄρχω",
        "translit": "Archō",
        "pos": "Verb, active",
        "gloss": "Rule / Have dominion",
        "definition": "<em>Archō</em> in its active form means \"to rule,\" \"to govern,\" or \"to be first.\" Appearing only 2 times in the NT in its active form (Mark 10:42; Romans 15:12), it is much more common as a prefix in compound words. The related noun <em>archōn</em> (ruler, prince) appears 37 times. The core idea is holding first position — beginning, priority, and authority.",
        "theology": "Jesus' response to the disciples' power-seeking (Mark 10:42–45) directly confronts <em>archō</em>: \"Those who are regarded as rulers (<em>archontes</em>) of the Gentiles lord it over them... Not so with you.\" The kingdom reverses the world's <em>archō</em> — greatness is found in servanthood. Yet Christ Himself holds ultimate <em>archō</em>: He is the \"ruler (<em>archōn</em>) of the kings of the earth\" (Revelation 1:5) and \"head (<em>archē</em>) of every power and authority\" (Colossians 2:10). The <em>archē</em> that rules with a servant heart — this is the revolutionary politics of the kingdom.",
        "verses": [
            ("Mark 10:42", "You know that those who are regarded as rulers [<em>archontes</em>] of the Gentiles lord it over them."),
            ("Romans 15:12", "And again, Isaiah says, 'The Root of Jesse will spring up, one who will arise to <em>rule</em> over the nations.'"),
            ("John 12:31", "Now is the time for judgment on this world; now the prince [<em>archōn</em>] of this world will be driven out."),
            ("Revelation 1:5", "And from Jesus Christ, who is the faithful witness, the firstborn from the dead, and the ruler [<em>archōn</em>] of the kings of the earth."),
            ("Ephesians 2:2", "The spirit who is now at work in those who are disobedient... the ruler [<em>archōn</em>] of the kingdom of the air."),
        ],
        "related": [("G756", "Archomai (Begin — middle voice)"), ("G746", "Archē (Beginning/Rule/Origin)"), ("G758", "Archōn (Ruler/Prince)")],
    },
    {
        "id": "G794",
        "original": "ἄστοργος",
        "translit": "Astorgos",
        "pos": "Adjective",
        "gloss": "Heartless / Without natural affection",
        "definition": "<em>Astorgos</em> means \"without natural affection\" or \"heartless\" — lacking <em>storgē</em>, the natural love that binds families together (parental love, filial love). The alpha-privative prefix removes this natural bond. Appearing only twice in the NT (Romans 1:31; 2 Timothy 3:3), it describes the moral degeneration of humanity apart from God. <em>Storgē</em> itself, while not appearing in the NT directly, is combined with <em>philos</em> to form <em>philostorgos</em> (devoted family love, Romans 12:10).",
        "theology": "Paul lists <em>astorgos</em> among the marks of depraved humanity (Romans 1:31) and the last-days character profile (2 Timothy 3:3). The loss of natural family affection is presented not as a neutral development but as moral and spiritual decay — a society that destroys the most basic bonds reveals a deep rejection of God's design for human community. The antidote is not law but gospel transformation: through the Spirit, believers become <em>philostorgoi</em> (Romans 12:10), characterized by the warm, devoted family love that mirrors God's own heart toward His children.",
        "verses": [
            ("Romans 1:31", "They are senseless, faithless, heartless [<em>astorgous</em>], ruthless."),
            ("2 Timothy 3:3", "Without natural affection [<em>astorgoi</em>], implacable, slanderers, without self-control, fierce, despisers of those that are good."),
            ("Romans 12:10", "Be devoted to one another in love [<em>philostorgoi</em>]. Honor one another above yourselves."),
            ("Matthew 10:21", "Brother will betray brother to death, and a father his child; children will rebel against their parents and have them put to death."),
            ("Luke 15:20", "But while he was still a long way off, his father saw him and was filled with compassion for him; he ran to his son, threw his arms around him and kissed him. [Storgē exemplified]"),
        ],
        "related": [("G26", "Agapē (Love)"), ("G5387", "Philostorgos (Devoted in family love)"), ("G4767", "Stugētos (Hateful/Detestable)")],
    },
    {
        "id": "G803",
        "original": "ἀσφάλεια",
        "translit": "Asphaleia",
        "pos": "Noun, feminine",
        "gloss": "Safety / Certainty / Security",
        "definition": "<em>Asphaleia</em> means safety, security, certainty, or firmness — the quality of being without risk of stumbling or falling. From the alpha-privative + <em>sphallō</em> (to cause to stumble, to overthrow). Appearing 3 times in the NT (Luke 1:4; Acts 5:23; 1 Thessalonians 5:3), it encompasses both physical security and intellectual certainty/reliability.",
        "theology": "Luke uses <em>asphaleia</em> in his prologue (Luke 1:4) as the epistemic goal of his Gospel: that Theophilus might know the <em>certainty</em> (<em>asphaleian</em>) of the things he had been taught. Scripture's aim is not mere information but sure foundation — unshakeable security for faith. Paul's eschatological use (1 Thessalonians 5:3) is darkly ironic: when people cry \"peace and <em>safety</em> [<em>asphaleia</em>]!\" — trusting in human security systems — sudden destruction comes. True <em>asphaleia</em> is found only in God, not in human power structures or false prophets promising stability.",
        "verses": [
            ("Luke 1:4", "So that you may know the <em>certainty</em> of the things you have been taught."),
            ("Acts 5:23", "We found the jail securely locked, with the guards standing at the doors; but when we opened them, we found no one inside."),
            ("1 Thessalonians 5:3", "While people are saying, 'Peace and <em>safety</em> [<em>asphaleian</em>],' destruction will come on them suddenly, as labor pains on a pregnant woman, and they will not escape."),
            ("Hebrews 6:19", "We have this hope as an anchor for the soul, firm and secure. [Parallel concept of security]"),
            ("Philippians 3:1", "Further, my brothers and sisters, rejoice in the Lord! It is no trouble for me to write the same things to you again, and it is a safeguard for you."),
        ],
        "related": [("G804", "Asphalēs (Certain/Safe — adj)"), ("G1515", "Eirēnē (Peace)"), ("G1680", "Elpis (Hope)")],
    },
    {
        "id": "G850",
        "original": "αὐχμηρός",
        "translit": "Auchmēros",
        "pos": "Adjective",
        "gloss": "Dark / Murky / Squalid",
        "definition": "<em>Auchmēros</em> means dark, murky, squalid, or gloomy — describing something characterized by filth, dryness, or gloom. Appearing only once in the NT (2 Peter 1:19), it contrasts the shadowy uncertainty of the pre-Christian era (\"a dark [<em>auchmēron</em>] place\") with the dawning light of prophetic fulfillment. The word in classical Greek could describe a neglected, unwashed, or dried-out condition.",
        "theology": "2 Peter 1:19 uses <em>auchmēron</em> to describe the place (<em>topos</em>) of prophetic Scripture before full understanding comes — not that Scripture itself is dark, but that our current age requires the prophetic lamp until the Day Star (<em>phōsphoros</em> — Christ at His return) rises in our hearts. This is a profound epistemological and eschatological image: we inhabit a real but murky present age, lit by the lamp of prophecy, awaiting the full dawn. The appropriate response is not despair but lamp-tending vigilance — like the wise virgins (Matthew 25).",
        "verses": [
            ("2 Peter 1:19", "We also have the prophetic message as something completely reliable, and you will do well to pay attention to it, as to a light shining in a <em>dark</em> [<em>auchmēron</em>] place, until the day dawns and the morning star rises in your hearts."),
            ("John 1:5", "The light shines in the darkness, and the darkness has not overcome it."),
            ("Romans 13:12", "The night is nearly over; the day is almost here. So let us put aside the deeds of darkness."),
            ("1 John 2:8", "The darkness is passing and the true light is already shining."),
            ("Matthew 25:8", "The foolish ones said to the wise, 'Give us some of your oil; our lamps are going out.'"),
        ],
        "related": [("G4655", "Skotos (Darkness)"), ("G5457", "Phōs (Light)"), ("G5459", "Phōsphoros (Morning Star)")],
    },
    {
        "id": "G908",
        "original": "βάπτισμα",
        "translit": "Baptisma",
        "pos": "Noun, neuter",
        "gloss": "Baptism",
        "definition": "<em>Baptisma</em> is the technical NT term for the rite of baptism — the immersion in or application of water as a sign of cleansing, initiation, and identification. Appearing about 19 times, it is distinguished from <em>baptismos</em> (a ritual washing) as the specifically Christian/Johannine sacramental act. Derived from <em>baptizō</em> (to immerse, to dip), it is the noun designating the event or institution of baptism.",
        "theology": "<em>Baptisma</em> is theologically rich in the NT. John's baptism (<em>baptisma metanoias</em> — baptism of repentance) pointed forward to Jesus. Jesus' own baptism inaugurated His public ministry and identity as the beloved Son. Christian baptism (Romans 6:3–4) is participation in Christ's death and resurrection — an enacted declaration that the old self has died and a new creation has risen. It is the initiatory rite of the new covenant community (Acts 2:38). Paul boldly says there is \"one baptism\" (Ephesians 4:5) — pointing to the unity of the body of Christ.",
        "verses": [
            ("Romans 6:4", "We were therefore buried with him through <em>baptism</em> into death in order that, just as Christ was raised from the dead through the glory of the Father, we too may live a new life."),
            ("Matthew 3:7", "But when he saw many of the Pharisees and Sadducees coming to where he was baptizing, he said to them: 'You brood of vipers! Who warned you to flee from the coming wrath?'"),
            ("Acts 2:38", "Peter replied, 'Repent and be <em>baptized</em>, every one of you, in the name of Jesus Christ for the forgiveness of your sins.'"),
            ("Mark 10:38", "Jesus said to them, 'Can you drink the cup I drink or be <em>baptized</em> with the baptism I am baptized with?'"),
            ("Ephesians 4:5", "One Lord, one faith, one <em>baptism</em>."),
        ],
        "related": [("G907", "Baptizō (To baptize — verb)"), ("G909", "Baptismos (Ritual washing)"), ("G3341", "Metanoia (Repentance)")],
    },
    {
        "id": "G928",
        "original": "βασανίζω",
        "translit": "Basanizō",
        "pos": "Verb, active",
        "gloss": "Torment / Torture / Distress",
        "definition": "<em>Basanizō</em> means to torment, torture, or cause severe distress. Appearing about 12 times in the NT, it derives from <em>basanos</em> (a touchstone for testing metals; torture). It is used of physical pain (Matthew 8:6 — the paralytic \"terribly suffering\"), demonic torment, the distress of the disciples in the storm (Matthew 14:24 — \"buffeted\"), and eschatological judgment (Revelation 14:10).",
        "theology": "The presence of <em>basanizō</em> in the Gospels reveals the nature of the evil Jesus confronts. When demons encounter Jesus, they immediately cry out: \"Have you come to torment [<em>basanisai</em>] us before the appointed time?\" (Matthew 8:29) — recognizing His authority to judge and end their power. Jesus' ministry is a pattern of reversing <em>basanismos</em>: the suffering one is healed, the demonized is liberated. In Revelation, the bowls of wrath involve <em>basanismos</em> — the God who forbore judgment now vindicates His creation. He who was tormented for us (Isaiah 53) becomes the one before whom tormentors flee.",
        "verses": [
            ("Matthew 8:29", "\"What do you want with us, Son of God?\" they shouted. \"Have you come here to <em>torture</em> us before the appointed time?\""),
            ("Matthew 8:6", "\"Lord,\" he said, \"my servant lies at home paralyzed, suffering terribly [<em>basanizomenos</em>].\""),
            ("Revelation 14:10", "They, too, will drink the wine of God's fury... They will be <em>tormented</em> with burning sulfur in the presence of the holy angels."),
            ("Mark 5:7", "He shouted at the top of his voice, 'What do you want with me, Jesus, Son of the Most High God? In God's name don't <em>torture</em> me!'"),
            ("2 Peter 2:8", "For that righteous man, living among them day after day, was <em>tormented</em> in his righteous soul by the lawless deeds he saw and heard."),
        ],
        "related": [("G929", "Basanismos (Torment — noun)"), ("G2347", "Thlipsis (Tribulation/Distress)"), ("G1349", "Dikē (Justice/Punishment)")],
    },
    {
        "id": "G936",
        "original": "βασιλεύω",
        "translit": "Basileuō",
        "pos": "Verb, active",
        "gloss": "Reign / Rule as king",
        "definition": "<em>Basileuō</em> means to reign, rule, or be king — the exercise of royal authority. Appearing about 21 times in the NT, it is the verbal form of <em>basileus</em> (king). It describes past human kingdoms (the reign of sin and death), the present reign of grace and Christ, and the future eternal kingdom. The verb captures the dynamic, active exercise of sovereignty.",
        "theology": "<em>Basileuō</em> structures Paul's entire argument in Romans 5:12–21 — a battle of reigns. Sin reigned in death (<em>ebasileosen ho thanatos</em>), but grace now reigns through righteousness (<em>basileuein hē charis</em>). The transfer of reign is the essence of the gospel: from Adam's death-reign to Christ's life-reign. 1 Corinthians 15:25 declares \"he must reign (<em>basileuein</em>) until he has put all his enemies under his feet\" — an active, progressive sovereignty. Revelation celebrates the moment when \"the Lord our God Almighty reigns [<em>ebasileuses</em>]\" (Revelation 19:6) — the completion of the kingdom.",
        "verses": [
            ("Romans 5:17", "For if, by the trespass of the one man, death reigned [<em>ebasileosen</em>] through that one man, how much more will those who receive God's abundant provision of grace... <em>reign</em> in life through the one man, Jesus Christ!"),
            ("Revelation 19:6", "Then I heard what sounded like a great multitude... shouting: 'Hallelujah! For our Lord God Almighty <em>reigns</em> [<em>ebasileuses</em>].'"),
            ("1 Corinthians 15:25", "For he must <em>reign</em> until he has put all his enemies under his feet."),
            ("Luke 1:33", "He will <em>reign</em> over Jacob's descendants forever; his kingdom will never end."),
            ("Romans 6:12", "Therefore do not let sin <em>reign</em> [<em>basileuetō</em>] in your mortal body so that you obey its evil desires."),
        ],
        "related": [("G935", "Basileus (King)"), ("G932", "Basileia (Kingdom)"), ("G2904", "Kratos (Dominion/Strength)")],
    },
    {
        "id": "G944",
        "original": "βάτραχος",
        "translit": "Batrachos",
        "pos": "Noun, masculine",
        "gloss": "Frog",
        "definition": "<em>Batrachos</em> means frog, appearing only once in the NT (Revelation 16:13) where John sees three unclean spirits \"like frogs\" (<em>hōs batrachoi</em>) coming from the mouths of the dragon, the beast, and the false prophet. In the Greek world, frogs were associated with the noisy, slimy, and polluted. The image has clear OT roots in the second plague of Egypt (Exodus 8).",
        "theology": "The frog-spirits of Revelation 16:13 are a deliberate echo of the Exodus plagues — positioning the Beast's empire as a new Egypt under divine judgment. The unclean spirits \"like frogs\" that proceed from lying mouths represent demonic propaganda: the unholy trinity's final deception gathering the nations for Armageddon (Revelation 16:14). Frogs emerge from the water (primordial chaos), come out in multitudes (overwhelming deception), and are associated with filth. The contrast could not be sharper: the Spirit of truth (John 16:13) vs. the frog-spirits of lies. The mouths that should speak truth become sources of demonic deception.",
        "verses": [
            ("Revelation 16:13", "Then I saw three impure spirits that looked like <em>frogs</em>; they came out of the mouths of the dragon, out of the mouth of the beast and out of the mouth of the false prophet."),
            ("Exodus 8:6", "So Aaron stretched out his hand over the waters of Egypt, and the <em>frogs</em> came up and covered the land."),
            ("Psalm 78:45", "He sent swarms of flies that devoured them, and <em>frogs</em> that devastated them."),
            ("Revelation 16:14", "They are demonic spirits that perform signs, and they go out to the kings of the whole world, to gather them for the battle on the great day of God Almighty."),
            ("Exodus 8:2", "If you refuse to let them go, I will send a plague of <em>frogs</em> on your whole country."),
        ],
        "related": [("G1404", "Drakōn (Dragon)"), ("G2342", "Thērion (Beast)"), ("G5578", "Pseudoprophētēs (False Prophet)")],
    },
    {
        "id": "G571",
        "original": "ἄπιστος",
        "translit": "Apistos",
        "pos": "Adjective",
        "gloss": "Unbelieving / Faithless",
        "definition": "<em>Apistos</em> means unbelieving, faithless, or incredulous — the one who lacks <em>pistis</em> (faith/trust). Appearing about 23 times in the NT, it describes both those outside the faith (unbelievers/pagans) and those within the community who doubt or prove faithless. The alpha-privative negates the positive virtue of <em>pistos</em> (faithful, trustworthy). It encompasses both intellectual unbelief and relational unfaithfulness.",
        "theology": "<em>Apistos</em> in the NT reveals that unbelief is not merely an intellectual position but a relational and moral failure — a refusal to trust God's revealed character and promises. Thomas's doubt earns the gentle rebuke \"do not be unbelieving (<em>apistos</em>) but believing\" (John 20:27). Paul's missionary letters use it to describe Gentiles outside the covenant (1 Corinthians 6:6; 2 Corinthians 6:14). Hebrews 3:12 warns believers against an <em>apistos</em> heart — the departure from the living God that begins in the heart before manifesting in behavior. Faith is not a one-time decision but an ongoing relational trust.",
        "verses": [
            ("John 20:27", "Then he said to Thomas, 'Put your finger here; see my hands. Reach out your hand and put it into my side. Stop doubting [<em>apistos</em>] and believe.'"),
            ("Hebrews 3:12", "See to it, brothers and sisters, that none of you has a sinful, unbelieving [<em>apistos</em>] heart that turns away from the living God."),
            ("1 Corinthians 7:14", "For the unbelieving [<em>apistos</em>] husband has been sanctified through his wife."),
            ("2 Corinthians 6:14", "Do not be yoked together with unbelievers [<em>apistois</em>]. For what do righteousness and wickedness have in common?"),
            ("Luke 12:46", "The master of that servant will come on a day when he does not expect him... and will assign him a place with the unbelievers [<em>apistōn</em>]."),
        ],
        "related": [("G4102", "Pistis (Faith/Trust)"), ("G4103", "Pistos (Faithful/Trustworthy)"), ("G570", "Apistia (Unbelief)")],
    },
    {
        "id": "G902",
        "original": "βαΐον",
        "translit": "Baion",
        "pos": "Noun, neuter",
        "gloss": "Palm branch",
        "definition": "<em>Baion</em> means a palm branch or frond — the leafy branch of a date palm. Appearing only once in the NT (John 12:13), it describes the branches the crowd took to greet Jesus at the Triumphal Entry. The word is of Egyptian origin (<em>bai</em> = palm tree). In Jewish practice, palm branches were associated with the Feast of Tabernacles (<em>Sukkot</em>) celebration — particularly waving the <em>lulav</em> (palm, myrtle, and willow bundle) in worship.",
        "theology": "The crowd's use of <em>baia</em> at Jesus' entry into Jerusalem (John 12:13) is a deliberate Tabernacles-Passover fusion. By waving palm branches and shouting \"Hosanna!\" (<em>Save now!</em> from Psalm 118:25–26), they enacted the eschatological expectation of the coming Davidic king who would \"save\" at the feast of final ingathering. Revelation 7:9 shows the redeemed multitude before the throne holding <em>phoinikes</em> (palm branches) — completing the Tabernacles imagery: the ultimate harvest feast of all nations gathered before God. Jesus is the fulfillment of everything the palms pointed to.",
        "verses": [
            ("John 12:13", "They took palm branches [<em>baia</em>] and went out to meet him, shouting, 'Hosanna! Blessed is he who comes in the name of the Lord!'"),
            ("Revelation 7:9", "After this I looked, and there before me was a great multitude that no one could count, from every nation, tribe, people and language, standing before the throne and before the Lamb. They were wearing white robes and were holding palm branches in their hands."),
            ("Leviticus 23:40", "On the first day you are to take branches from luxuriant trees — from palms, willows and other leafy trees — and rejoice before the LORD your God for seven days."),
            ("Nehemiah 8:15", "Go out into the hill country and bring back branches from olive and wild olive trees... to make temporary shelters."),
            ("Matthew 21:8", "A very large crowd spread their cloaks on the road, while others cut branches from the trees and spread them on the road."),
        ],
        "related": [("G5404", "Phoinix (Palm tree)"), ("G5614", "Hōsanna (Hosanna — Save now!)"), ("G2962", "Kyrios (Lord)")],
    },
    {
        "id": "G1525",
        "original": "εἰσέρχομαι",
        "translit": "Eiserchomai",
        "pos": "Verb, deponent",
        "gloss": "Enter / Come in / Go in",
        "definition": "<em>Eiserchomai</em> means to enter, go into, or come in — physical or metaphorical entry into a space, state, or relationship. Appearing about 194 times in the NT, it is a compound of <em>eis</em> (into) and <em>erchomai</em> (to come/go). It describes entering buildings, cities, the kingdom, rest, temptation, and glory. It is one of the most theologically loaded spatial verbs in the NT.",
        "theology": "Entry (<em>eiserchomai</em>) is a major metaphor in the NT for salvation and the kingdom. Jesus commands \"Enter [<em>eiselthate</em>] through the narrow gate\" (Matthew 7:13). The kingdom \"enters\" as Jesus heals and casts out demons. Hebrews 3–4 builds an extended argument about entering God's rest (<em>eiserchomai eis katapausin</em>) — connecting the Promised Land entry with Sabbath rest with the eschatological rest Christ provides. In John's Gospel, Jesus is the Door through which the sheep <em>eiserchomai</em> (John 10:9). Entry is both invitation and requirement — requiring the right mediator and the right posture.",
        "verses": [
            ("Matthew 7:13", "<em>Enter</em> through the narrow gate. For wide is the gate and broad is the road that leads to destruction, and many enter through it."),
            ("John 10:9", "I am the gate; whoever enters [<em>eiselthē</em>] through me will be saved."),
            ("Hebrews 4:3", "Now we who have believed <em>enter</em> that rest."),
            ("Luke 18:25", "Indeed, it is easier for a camel to go through the eye of a needle than for someone who is rich to <em>enter</em> the kingdom of God."),
            ("Revelation 21:27", "Nothing impure will ever <em>enter</em> it, nor will anyone who does what is shameful or deceitful, but only those whose names are written in the Lamb's book of life."),
        ],
        "related": [("G1831", "Exerchomai (Go out/Exit)"), ("G305", "Anabainō (Go up/Ascend)"), ("G4198", "Poreuomai (Go/Travel)")],
    },
]

# ============================================================
# BUILD PAGES
# ============================================================
def main():
    created = []
    for w in WORDS:
        sid = w["id"]
        filepath = os.path.join(LEXICON_DIR, f"{sid}.html")
        html = build_page(
            sid, LEXICON_DIR,
            w["original"], w["translit"], w["pos"], w["gloss"],
            w["definition"], w["theology"], w["verses"], w["related"]
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        created.append(sid)
        print(f"  Created: {sid}.html")

    # Update manifest
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    existing = set(manifest["entries"])
    for sid in created:
        if sid not in existing:
            manifest["entries"].append(sid)
    # Sort entries
    def sort_key(e):
        return (e[0], int(e[1:]))
    manifest["entries"].sort(key=sort_key)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nManifest updated. Total entries: {len(manifest['entries'])}")
    print(f"New pages created: {len(created)}")
    print("Entries:", created)

if __name__ == "__main__":
    main()
