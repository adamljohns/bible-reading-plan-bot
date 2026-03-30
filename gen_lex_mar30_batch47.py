#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch Mar 30 2026"""
import os

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")

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
        .section p { color:var(--white); line-height:1.8; margin-bottom:12px; }
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

JS = """<script>function bteToggleTheme(){var b=document.body;if(b.classList.contains("light-mode")){b.classList.remove("light-mode");localStorage.setItem("bte-theme","dark");}else{b.classList.add("light-mode");localStorage.setItem("bte-theme","light");}}(function(){if(localStorage.getItem("bte-theme")==="light"){document.body.classList.add("light-mode");}})();</script>"""

NAV = """    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div style="display:flex;justify-content:center;margin:10px 0 4px;">
      <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="display:flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 10px;cursor:pointer;font-size:0.75rem;gap:4px;">
        <span>🌙</span>
        <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
        <span>☀️</span>
      </div>
    </div>"""

def make_page(strongs_id, lang, script, translit, pos, gloss, short_def, definition, theology, verses, related):
    lang_label = "Hebrew · Old Testament" if lang == "H" else "Greek · New Testament"
    num = strongs_id[1:]
    ext_lang = "greek" if lang == "G" else "hebrew"
    blb_lang = "g" if lang == "G" else "h"
    extra_class = ' greek' if lang == 'G' else ''
    dir_attr = '' if lang == 'G' else ' direction:rtl;'

    verses_html = ""
    for ref, text in verses:
        ref_url = ref.replace(" ", "+")
        verses_html += f"""                <div class="verse-entry">
                    <a href="../bible.html?ref={ref_url}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>\n"""

    related_html = ""
    for rel_id, rel_label in related:
        related_html += f'                <a href="{rel_id}.html" class="related-word">{rel_id} — {rel_label}</a>\n'

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
    <meta property="og:description" content="{gloss} — {'Hebrew' if lang=='H' else 'Greek'} word study. Strong's {strongs_id}.">
    <meta name="description" content="{gloss} — {'Hebrew' if lang=='H' else 'Greek'} word study. Strong's {strongs_id}. USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{strongs_id} — {translit} ({gloss}) | USMC Ministries Lexicon</title>
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
            <div class="original-word{extra_class}" style="font-size:3rem;margin:15px 0 10px;color:var(--gold-light);{dir_attr}">{script}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{short_def}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{definition}</p>
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
                <a href="https://www.blueletterbible.org/lexicon/{blb_lang}{num}/kjv/wlc/0-1/" class="ext-link" target="_blank" rel="noopener">Blue Letter Bible</a>
                <a href="https://biblehub.com/{ext_lang}/{num}.htm" class="ext-link" target="_blank" rel="noopener">Bible Hub</a>
            </div>
        </div>
    </div>
    <footer>
        <p>USMC Ministries Greek &amp; Hebrew Lexicon · <a href="../lexicon.html">Browse All Words</a></p>
    </footer>
    {JS}
</body>
</html>"""

def write_page(strongs_id, script, translit, pos, gloss, short_def, full_def, theology, verses, related):
    lang = strongs_id[0]
    html = make_page(strongs_id, lang, script, translit, pos, gloss, short_def, full_def, theology, verses, related)
    path = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Created: {strongs_id}.html")

# ============================================================
# HEBREW WORDS (24)
# ============================================================
hebrew_words = [

    ("H844", "אַשְׂרִיאֵל", "Asriel", "Proper noun, masculine", "God Is My Joy; Vow of God",
     "A personal name meaning 'God is my happiness' or 'vow of God' — borne by a descendant of Manasseh and a son of Gilead.",
     "The name <em>Asriel</em> (H844) combines <em>asher</em> (H835, happy/blessed) with <em>El</em> (God), producing 'God is my joy' or 'God has filled with happiness.' It appears in Numbers 26:31 as a clan of Manasseh, in Joshua 17:2 as a son of Gilead receiving a territorial allotment, and in 1 Chronicles 7:14 as a descendant of Manasseh by an Aramean concubine. Though primarily a genealogical name, its meaning is theologically rich.",
     "Personal names in the OT were not mere labels but theological confessions — compressed statements of faith or hope. <em>Asriel</em> ('God is my joy') parallels the beatitude-spirit of Psalm 144:15: 'Blessed (<em>ashre</em>) is the people whose God is the LORD.' When a Manassite family named their son 'God-is-my-joy,' they were encoding a doctrine of divine happiness into their genealogy. God is not merely the source of blessing but is Himself the joy — a truth the NT amplifies in Philippians 4:4: 'Rejoice in the Lord always.'",
     [("Numbers 26:31", "of <em>Asriel</em>, the Asrielite clan; of Shechem, the Shechemite clan."),
      ("Joshua 17:2", "This was also for the rest of the descendants of Manasseh by their clans: for the sons of Abiezer, Helek, <em>Asriel</em>, Shechem, Hepher, and Shemida."),
      ("1 Chronicles 7:14", "The descendants of Manasseh: Asriel was his descendant through his Aramean concubine. She gave birth to Makir the father of Gilead."),
      ("Psalm 144:15", "Blessed (<em>ashre</em>) is the people whose God is the LORD."),
      ("Philippians 4:4", "Rejoice in the Lord always. I will say it again: Rejoice!")],
     [("H835", "Asher (Happy/Blessed)"), ("H410", "El (God/Mighty One)"), ("H4519", "Manasseh (Causing to Forget)")]),

    ("H1266", "בְּרוֹשׁ", "Berosh", "Noun, masculine", "Cypress Tree; Fir Tree",
     "A tall, fragrant evergreen tree — the cypress or fir — used extensively in temple construction and as a symbol of majesty and permanence.",
     "The Hebrew <em>berosh</em> refers to a tall, aromatic conifer, most likely the Cilician fir or Aleppo pine. It appears 20 times in the OT, most significantly in the construction of Solomon's Temple — Solomon requested <em>berosh</em> timber from Hiram of Tyre (1 Kings 5:8, 10) alongside the famous cedars of Lebanon. It was also used for David's palace (2 Samuel 5:11) and musical instruments (2 Samuel 6:5). Isaiah uses it in redemptive imagery: the wilderness will bloom with <em>berosh</em> trees (Isaiah 41:19; 55:13).",
     "<em>Berosh</em> in prophetic literature becomes a marker of transformation and glory. Where thorns and briers represent the curse of Genesis 3, the cypress and cedar represent the restored Eden. Isaiah 55:13 is particularly powerful: 'Instead of the thornbush will grow the <em>berosh</em> tree, and instead of briers the myrtle will grow. This will be for the LORD's renown, for an everlasting sign, that will endure forever.' The same wood that built the Temple will fill the wilderness — all creation reclaimed for worship.",
     [("1 Kings 5:10", "So Hiram kept Solomon supplied with all the cedar and <em>juniper</em> logs he wanted."),
      ("Isaiah 55:13", "Instead of the thornbush will grow the <em>pine tree</em>, and instead of briers the myrtle will grow."),
      ("Isaiah 41:19", "I will put in the desert the cedar and the acacia, the myrtle and the olive. I will set junipers in the wasteland, the fir and the <em>cypress</em> together."),
      ("2 Samuel 6:5", "David and all Israel were celebrating with all their might before the LORD, with castanets, harps, lyres, timbrels, sistrums and cymbals."),
      ("Hosea 14:8", "I am like a flourishing <em>juniper</em> tree; your fruitfulness comes from me.")],
     [("H730", "Erez (Cedar)"), ("H8558", "Tamar (Palm Tree)"), ("H4480", "Miqdash (Sanctuary)")]),

    ("H1466", "גֵּוָה", "Gevah", "Noun, feminine", "Pride; Haughtiness; Arrogance",
     "Exalted pride or arrogance — the lifted-up posture of a heart that forgets its dependence on God.",
     "The Hebrew <em>gevah</em> derives from <em>gavah</em> (to be high, lifted up) and denotes proud arrogance — the inward disposition that sets itself against God. It appears in Job 22:29 ('When men are humbled, you say, 'Lift them up!' and he saves the humble person'), in Proverbs 8:13 where wisdom declares hatred for <em>gevah</em>, and in Ezekiel 7:10 where <em>gevah</em> is connected to doom: 'The rod has budded, pride (<em>gevah</em>) has blossomed — violence has grown into a rod to punish the wicked.'",
     "Biblical anthropology consistently identifies pride (<em>gevah</em>, <em>gaavah</em>, <em>gaon</em>) as the root sin — the primordial turn from God-centeredness to self-centeredness. Proverbs 8:13 places <em>gevah</em> in the mouth of divine Wisdom herself as the primary object of her hatred: 'To fear the LORD is to hate evil; I hate pride (<em>gevah</em>) and arrogance.' This connects to Isaiah 14's portrait of Lucifer's fall — 'I will make myself like the Most High' — and to the NT principle of James 4:6: 'God opposes the proud but shows favor to the humble.'",
     [("Proverbs 8:13", "To fear the LORD is to hate evil; I hate <em>pride</em> and arrogance, evil behavior and perverse speech."),
      ("Ezekiel 7:10", "See, the day! See, it comes! Doom has burst forth, the rod has budded, <em>arrogance</em> has blossomed!"),
      ("Job 22:29", "When people are humbled, you say, 'Lift them up!' and he saves the downcast."),
      ("Proverbs 16:18", "Pride goes before destruction, a haughty spirit before a fall."),
      ("Isaiah 14:12", "How you have fallen from heaven, morning star, son of the dawn! You have been cast down to the earth, you who once laid low the nations!")],
     [("H1346", "Gaavah (Pride/Majesty)"), ("H8217", "Shaphal (Humble/Low)"), ("H3372", "Yare (Fear/Reverence)")]),

    ("H1482", "גּוּר", "Gur", "Noun, masculine", "Cub; Young Lion; Whelp",
     "A young lion, tiger, or other predatory animal — used as a metaphor for fierce tribal and royal strength.",
     "The Hebrew <em>gur</em> (distinct from H1481 <em>gur</em>, 'to sojourn') means a whelp or cub — specifically a young lion or other powerful beast. It appears most famously in Jacob's blessing on Judah: 'Judah is a lion's cub (<em>gur</em> aryeh), O my son' (Genesis 49:9). This prophetic blessing identifies Judah with the lion — fierce, kingly, ultimately Messianic. The same image recurs in Deuteronomy 33:22 (Dan is a lion's cub) and Nahum 2:11-12 (Nineveh as a den of lions).",
     "The <em>gur aryeh</em> of Genesis 49:9 launches one of the most consequential Messianic prophecies in the OT. Jacob sees Judah not merely as a tribe but as the line through which the kingly ruler will come: 'The scepter will not depart from Judah...until he to whom it belongs shall come and the obedience of the nations shall be his' (Genesis 49:10). This finds its fulfillment in Revelation 5:5 where the Lion of the tribe of Judah is identified as the Lamb who was slain — power and sacrifice united in one Person.",
     [("Genesis 49:9", "You are a lion's cub (<em>gur aryeh</em>), Judah; you return from the prey, my son. Like a lion he crouches and lies down, like a lioness — who dares to rouse him?"),
      ("Deuteronomy 33:22", "About Dan he said: 'Dan is a lion's cub, springing out of Bashan.'"),
      ("Nahum 2:11", "Where now is the lions' den, the place where they fed their young, where the lion and lioness went, and the cubs (<em>gur</em>), with nothing to fear?"),
      ("Revelation 5:5", "Then one of the elders said to me, 'Do not weep! See, the Lion of the tribe of Judah, the Root of David, has triumphed.'"),
      ("Micah 5:8", "The remnant of Jacob will be among the nations, in the midst of many peoples, like a lion among the beasts of the forest, like a young lion among flocks of sheep.")],
     [("H738", "Aryeh (Lion)"), ("H7626", "Shebet (Scepter/Tribe)"), ("H4899", "Mashiach (Messiah/Anointed)")]),

    ("H1645", "גֶּרֶשׁ", "Geresh", "Noun, masculine", "Produce; Yield; Monthly Fruit",
     "The fresh produce or yield of the land — specifically the monthly or seasonal fruit brought forth by the earth under God's blessing.",
     "The Hebrew <em>geresh</em> derives from <em>garash</em> (to drive out, expel) and in its agricultural sense means the produce that is 'brought forth' or yielded by the land. It appears most notably in Deuteronomy 33:14 in Moses' blessing on Joseph: 'the best gifts of the earth and its fullness, and the favor of him who dwelt in the burning bush. Let all these rest on the head of Joseph... with the <em>geresh</em> of the moon' — the monthly yield of fruit.",
     "The monthly produce (<em>geresh yerachim</em>, yield of the moons) in Moses' blessing on Joseph prefigures the eschatological vision of Revelation 22:2 — the tree of life bearing twelve crops, yielding its fruit every month. What Moses foresaw as covenant blessing on Joseph's land finds its ultimate fulfillment in the New Jerusalem where creation's productivity is fully restored. Every agricultural cycle of planting and harvest was a covenant sign — God keeping His promise to 'seed-time and harvest' (Genesis 8:22) until the city where every month yields its fruit.",
     [("Deuteronomy 33:14", "with the best gifts of the earth and its fullness and the favor of him who dwelt in the burning bush. Let all these rest on the head of Joseph, on the brow of the prince among his brothers."),
      ("Revelation 22:2", "On each side of the river stood the tree of life, bearing twelve crops of fruit, yielding its fruit every month."),
      ("Genesis 8:22", "As long as the earth endures, seedtime and harvest, cold and heat, summer and winter, day and night will never cease."),
      ("Psalm 67:6", "The land yields its harvest; God, our God, blesses us."),
      ("Ezekiel 47:12", "Their fruit will serve for food and their leaves for healing.")],
     [("H776", "Erets (Land/Earth)"), ("H1293", "Berakah (Blessing)"), ("H3126", "Yoneq (Tender Plant/Branch)")]),

    ("H2131", "זִיקָה", "Ziqah", "Noun, feminine", "Spark; Firebrand; Flying Bolt",
     "A flying spark or firebrand — the streak of fire hurled through the air, used as a vivid metaphor for divine judgment and the reckless man who spreads harm.",
     "The Hebrew <em>ziqah</em> (also rendered <em>ziqqim</em> in plural) refers to a spark or firebrand — the flying ember or burning projectile. It appears in Proverbs 26:18-19 in a piercing simile: 'Like a maniac shooting flaming arrows (<em>ziqqim</em>) of death is one who deceives their neighbor.' The image is visceral — a flaming bolt loosed into a crowd — applied to the person who lies and then says 'I was only joking.' Isaiah 50:11 uses it as a metaphor for those who trust in human wisdom rather than God: 'Walk in the light of your fires and of the <em>ziqqim</em> you have lit.'",
     "The <em>ziqah</em> in Isaiah 50:11 is one of the most sobering warnings in Scripture about self-made religion. Those who kindle their own light — who walk by human reasoning rather than divine revelation — are told: 'This is what you shall receive from my hand: you will lie down in torment.' The spark of self-sufficiency becomes a firebrand of judgment. This is the anti-type of the divine fire: God's fire purifies and illuminates (Exodus 3, Isaiah 6), while human fire blinds and destroys. Only the fire that God ignites is safe to walk in.",
     [("Proverbs 26:18", "Like a maniac shooting flaming arrows of death (<em>ziqqim</em>) is one who deceives their neighbor and says, 'I was only joking!'"),
      ("Isaiah 50:11", "But now, all you who light fires and provide yourselves with flaming torches (<em>ziqqim</em>), go, walk in the light of your fires and of the torches you have set ablaze."),
      ("Psalm 7:13", "He has prepared his deadly weapons; he makes ready his flaming arrows."),
      ("Ephesians 6:16", "In addition to all this, take up the shield of faith, with which you can extinguish all the flaming arrows of the evil one."),
      ("Exodus 3:2", "There the angel of the LORD appeared to him in flames of fire from within a bush. Moses saw that though the bush was on fire it did not burn up.")],
     [("H784", "Esh (Fire)"), ("H2595", "Chanit (Spear/Lance)"), ("H7423", "Remiyyah (Deceit/Slackness)")]),

    ("H2553", "חַמָּן", "Chamman", "Noun, masculine", "Incense Stand; Sun Pillar; Idol Altar",
     "A free-standing incense altar or sun pillar associated with Baal worship — a symbol of idolatry condemned throughout the Prophets.",
     "The Hebrew <em>chamman</em> refers to a cult object used in Canaanite worship — likely a standing incense burner, sun pillar, or altar for burning offerings to Baal or the sun god. The word may derive from <em>chamah</em> (sun/heat). It appears eight times in the OT (Leviticus 26:30; 2 Chronicles 14:5; 34:4,7; Isaiah 17:8; 27:9; Ezekiel 6:4,6) and is consistently connected with judgment — God promises to hack down these idolatrous structures when He cleanses the land.",
     "The <em>chammanim</em> were portable or standing incense stands set up at high places throughout Israel and Judah. Their destruction becomes a sign of covenant renewal: King Asa 'removed the foreign altars and the high places, smashed the sacred stones and cut down the Asherah poles, and commanded Judah to seek the LORD' (2 Chronicles 14:3-5, including <em>chammanim</em>). Josiah's reform (2 Chronicles 34:4-7) similarly demolished them. The prophets saw these objects as the physical embodiment of Israel's spiritual adultery — and their destruction as the prerequisite for restoration.",
     [("Leviticus 26:30", "I will destroy your high places, cut down your incense altars (<em>chammanim</em>) and pile your dead bodies on the lifeless forms of your idols."),
      ("2 Chronicles 14:5", "He removed the high places and incense altars (<em>chammanim</em>) in every town in Judah, and the kingdom was at peace under him."),
      ("Isaiah 17:8", "They will not look to the altars, the work of their hands, and they will have no regard for the Asherah poles and the incense altars (<em>chammanim</em>) their fingers have made."),
      ("Ezekiel 6:4", "Your altars will be demolished and your incense altars (<em>chammanim</em>) will be smashed; and I will slay your people in front of your idols."),
      ("2 Chronicles 34:7", "He burned the bones of the priests on their altars, and so he purged Judah and Jerusalem.")],
     [("H6456", "Pesilim (Carved Idols)"), ("H842", "Asherah (Fertility Goddess Pole)"), ("H1168", "Baal (Lord/Idol)")]),

    ("H3383", "יַרְדֵּן", "Yarden", "Proper noun", "The Jordan River; Flowing Down",
     "The Jordan River — the boundary river of the Promised Land, site of crossing, baptism, healing, and covenant entry.",
     "The Hebrew <em>Yarden</em> (Jordan) likely derives from <em>yarad</em> (to descend) — 'the descending one' — appropriate for a river that drops dramatically from Mount Hermon through the Sea of Galilee to the Dead Sea, below sea level. The Jordan marks the boundary between the wilderness and the Promised Land in Joshua 3-4, where Israel crossed on dry ground in a second Exodus miracle. It is also where Naaman was healed of leprosy (2 Kings 5) and where John baptized and Jesus was baptized (Matthew 3).",
     "The Jordan River is one of the most theologically layered geographical features in Scripture. Its crossing in Joshua 3 recapitulates the Red Sea crossing of Exodus 14 — same God, same miracle, new generation entering the inheritance. The Jordan became the ultimate threshold. Jesus' baptism in the Jordan (Matthew 3:13-17) transformed it once more: where Israel crossed to claim the land, Jesus descended to take up humanity's burden — and emerged to receive the Spirit and the Father's declaration. The Jordan is where divine history repeatedly pivots.",
     [("Joshua 3:17", "The priests who carried the ark of the covenant of the LORD stopped in the middle of the <em>Jordan</em> and stood on dry ground, while all Israel passed by."),
      ("2 Kings 5:14", "So Naaman went down and dipped himself in the <em>Jordan</em> seven times, as the man of God had told him, and his flesh was restored."),
      ("Matthew 3:13", "Then Jesus came from Galilee to the <em>Jordan</em> to be baptized by John."),
      ("Joshua 4:7", "Tell them that the flow of the <em>Jordan</em> was cut off before the ark of the covenant of the LORD. These stones are to be a memorial to the people of Israel forever."),
      ("Psalm 114:3", "The sea looked and fled, the <em>Jordan</em> turned back.")],
     [("H3220", "Yam (Sea)"), ("H7200", "Raah (See/Vision)"), ("H4057", "Midbar (Wilderness)")]),

    ("H3567", "כּוֹרֶשׁ", "Koresh", "Proper noun, masculine", "Cyrus; The Persian King",
     "Cyrus the Great, King of Persia — called by name in prophecy 150 years before his birth and designated as God's anointed instrument for Israel's restoration.",
     "The Hebrew <em>Koresh</em> (Persian: Kurush, Greek: Kyros) refers to Cyrus II the Great (c. 600-530 BC), founder of the Achaemenid Persian Empire. He conquered Babylon in 539 BC and immediately issued the Edict of Cyrus (Ezra 1:1-4; 2 Chronicles 36:22-23), freeing the Jewish exiles to return to Israel and rebuild the Temple. Most remarkably, Isaiah 44:28-45:1 names him 150 years in advance: 'who says of Cyrus, 'He is my shepherd and will accomplish all that I please'... This is what the LORD says to his anointed, to Cyrus.'",
     "The designation of <em>Koresh</em> as God's <em>mashiach</em> (anointed one) in Isaiah 45:1 is one of the most theologically provocative moments in the OT. A pagan king — one who did not know the God of Israel (Isaiah 45:4-5) — is called God's shepherd and anointed instrument. This teaches that divine sovereignty is not restricted to covenant insiders. God raises up and tears down kings according to His purposes (Daniel 2:21), and He can accomplish His redemptive plan through any means He chooses. Cyrus is a type of Christ — a liberator who sets captives free — but also a reminder that only Jesus is the ultimate Anointed One.",
     [("Isaiah 44:28", "who says of <em>Cyrus</em>, 'He is my shepherd and will accomplish all that I please; he will say of Jerusalem, Let it be rebuilt, and of the temple, Let its foundations be laid.'"),
      ("Isaiah 45:1", "This is what the LORD says to his anointed, to <em>Cyrus</em>, whose right hand I take hold of to subdue nations before him."),
      ("Ezra 1:2", "<em>Cyrus</em> king of Persia says: 'The LORD, the God of heaven, has given me all the kingdoms of the earth and he has appointed me to build a temple for him at Jerusalem in Judah.'"),
      ("2 Chronicles 36:23", "This is what <em>Cyrus</em> king of Persia says: 'The LORD, the God of heaven, has given me all the kingdoms of the earth and he has appointed me to build a temple for him at Jerusalem in Judah. Any of his people among you may go up.'"),
      ("Isaiah 45:4", "For the sake of Jacob my servant, of Israel my chosen, I summon you by name and bestow on you a title of honor, though you do not acknowledge me.")],
     [("H4899", "Mashiach (Anointed One)"), ("H1350", "Gaal (Redeemer)"), ("H7622", "Shevut (Restoration/Captivity)")]),

    ("H3979", "מַאֲכֶלֶת", "Maakheleth", "Noun, feminine", "Knife; Slaughtering Knife; Sacrificial Blade",
     "A large knife or sword used for slaughtering — appearing in the sacrifice of Isaac and in a sword-like destructive capacity.",
     "The Hebrew <em>maakheleth</em> (from <em>akal</em>, to eat/consume) is a large knife used for cutting meat — a butcher's blade or sacrificial knife. It appears in two striking OT contexts: Genesis 22:6 and 10, where Abraham carries the <em>maakheleth</em> to Mount Moriah to sacrifice Isaac; and Judges 19:29, where the Levite uses it to dismember his concubine. Proverbs 30:14 uses it figuratively for the devouring teeth of the wicked.",
     "The <em>maakheleth</em> in Genesis 22 is one of the most theologically charged objects in Scripture. Abraham lifts the knife over his bound son — and at that moment, the angel of the LORD stops him: 'Do not lay a hand on the boy.' A ram caught in a thicket becomes the substitute sacrifice. This scene is the typological center of atonement theology: the knife raised, the substitute provided, the son spared. Christians read Genesis 22 as the prototype of Calvary — where God the Father did not stay His hand, but gave His Son as the ram on the hill. The <em>maakheleth</em> Abraham carried is the shadow of the cross.",
     [("Genesis 22:6", "Abraham took the wood for the burnt offering and placed it on his son Isaac, and he himself carried the fire and the <em>knife</em> (<em>maakheleth</em>)."),
      ("Genesis 22:10", "Then he reached out his hand and took the <em>knife</em> to slay his son."),
      ("Genesis 22:13", "Abraham looked up and there in a thicket he saw a ram caught by its horns. He went over and took the ram and sacrificed it as a burnt offering instead of his son."),
      ("Proverbs 30:14", "Those whose teeth are swords and whose jaws are set with knives (<em>maakheleth</em>) to devour the poor from the earth."),
      ("Hebrews 11:17", "By faith Abraham, when God tested him, offered Isaac as a sacrifice. He who had embraced the promises was about to sacrifice his one and only son.")],
     [("H2076", "Zabach (Sacrifice)"), ("H352", "Ayil (Ram)"), ("H6453", "Pesach (Passover)")]),

    ("H4420", "מְלֵחָה", "Melecha", "Noun, feminine", "Salt Land; Barren Ground; Wasteland",
     "Salt-laden earth — unproductive, cursed land associated with divine judgment and the desolation of destroyed cities.",
     "The Hebrew <em>melecha</em> (from <em>melach</em>, salt) refers to ground so saturated with salt that nothing can grow — the wasteland left by divine judgment or the deliberate salting of conquered cities. It appears in Job 39:6 where God has given the wild donkey the salt flats (<em>melecha</em>) as its home, in Psalm 107:34 where God 'turns a fruitful land into a salt waste (<em>melecha</em>) because of the wickedness of those who live there,' and in Jeremiah 17:6 where the one who trusts in man 'will live in the parched places of the desert, in a salt land (<em>melecha</em>) where no one lives.'",
     "The <em>melecha</em> is the anti-Eden — the land of curse rather than blessing. Just as Eden was fruitful and life-sustaining, the salt land is barren and death-dealing. Judges 9:45 records that Abimelech 'destroyed the city and scattered salt over it' — a curse to ensure permanent desolation. Deuteronomy 29:23 prophesies that disobedient Israel will become like Sodom, 'the whole land a burning waste of salt and sulfur.' Yet Psalm 107 also shows the reverse: God can turn wilderness into pools of water and thirsty ground into springs. The same God who judges with salt can restore with water.",
     [("Psalm 107:34", "He turned their fruitful plains into salty (<em>melecha</em>) wastelands because of the wickedness of those who lived there."),
      ("Jeremiah 17:6", "That person will be like a bush in the wastelands; they will not see prosperity when it comes. They will dwell in the parched places of the desert, in a <em>salt land</em> where no one lives."),
      ("Job 39:6", "to whom I gave the wasteland as a home, the <em>salt flats</em> as a habitat?"),
      ("Deuteronomy 29:23", "The whole land will be a burning waste of salt and sulfur — nothing planted, nothing sprouting, no vegetation growing on it."),
      ("Ezekiel 47:11", "But the swamps and marshes will not become fresh; they will be left for salt.")],
     [("H4417", "Melach (Salt)"), ("H5215", "Nir (Freshly Tilled Land)"), ("H1293", "Berakah (Blessing)")]),

    ("H5218", "נָכֵא", "Nake", "Adjective", "Stricken; Smitten; Contrite; Broken",
     "Smitten, struck down, or broken — particularly in a spiritual sense of being humbled and contrite before God.",
     "The Hebrew <em>nake</em> (or <em>nakeh</em>) is an adjective from <em>nakah</em> (to strike/smite) meaning one who has been struck or smitten. In its spiritual dimension, it describes the broken, contrite heart — the person who has been struck by God's correction and brought low. Isaiah 66:2 is the key verse: 'These are the ones I look on with favor: those who are humble and contrite in spirit (<em>nake ruach</em>) and who tremble at my word.' This connects to Isaiah 53:4: the Servant was 'stricken (<em>nake</em>) by God, smitten by him.'",
     "The theology of <em>nake</em> is paradoxical: being struck is the pathway to being seen by God. Isaiah 66:2 announces that the God who fills heaven and earth looks specifically for the one who is <em>nake ruach</em> — stricken in spirit. Not the impressive, the accomplished, or the self-sufficient, but the broken one. This connects to the Beatitudes: 'Blessed are the poor in spirit' (Matthew 5:3). Isaiah 53 reveals that the Servant Himself became <em>nake</em> — stricken, smitten by God — so that we might be healed. The broken One bore our brokenness.",
     [("Isaiah 66:2", "Has not my hand made all these things, and so they came into being? declares the LORD. These are the ones I look on with favor: those who are humble and <em>contrite</em> in spirit and who tremble at my word."),
      ("Isaiah 53:4", "Surely he took up our pain and bore our suffering, yet we considered him punished by God, <em>stricken</em> by him, and afflicted."),
      ("Psalm 34:18", "The LORD is close to the brokenhearted and saves those who are crushed in spirit."),
      ("Psalm 51:17", "My sacrifice, O God, is a broken spirit; a broken and contrite heart you, God, will not despise."),
      ("Matthew 5:3", "Blessed are the poor in spirit, for theirs is the kingdom of heaven.")],
     [("H1792", "Dakah (Crush/Contrite)"), ("H3665", "Kana (Humble/Subdue)"), ("H5315", "Nephesh (Soul/Self)")]),

    ("H5443", "סַבְּכָא", "Sabbecha", "Noun, feminine", "Sackbut; Triangle; Stringed Instrument",
     "An ancient stringed or percussion instrument — one of the instruments in Nebuchadnezzar's royal orchestra, sounded at the dedication of the golden image.",
     "The Hebrew <em>sabbecha</em> (Aramaic form: <em>sabbekhah</em>) appears exclusively in Daniel 3 — the dramatic scene of Nebuchadnezzar's golden image. When 'the sound of the horn, flute, zither, lyre, harp, pipe and all kinds of music (<em>sabbecha</em> among them) is heard,' all people were commanded to fall and worship the image. Shadrach, Meshach, and Abednego refused. The <em>sabbecha</em> was likely a triangular harp or early form of lyre.",
     "The <em>sabbecha</em> in Daniel 3 is not merely an obscure instrument note — it is part of the machinery of totalitarian idolatry. The state-sponsored orchestra was designed to condition mass worship through sensory manipulation: hear the music, bow to the image. Nebuchadnezzar understood what modern propagandists rediscovered — music creates compliance. The three Hebrews' refusal to bow when the music played was not a small act of religious stubbornness. It was a declaration that there is a higher music, a higher King, and a higher fire than Nebuchadnezzar's furnace. They heard a different song.",
     [("Daniel 3:5", "As soon as you hear the sound of the horn, flute, zither, lyre, harp, pipe and all kinds of music (<em>sabbecha</em>), you must fall down and worship the image of gold."),
      ("Daniel 3:15", "Now when you hear the sound of the horn, flute, zither, lyre, harp, pipe and all kinds of music (<em>sabbecha</em>), if you are ready to fall down and worship the image I made, very good."),
      ("Daniel 3:17", "If we are thrown into the blazing furnace, the God we serve is able to deliver us from it."),
      ("Daniel 3:25", "He said, 'Look! I see four men walking around in the fire, unbound and unharmed.'"),
      ("Psalm 150:3", "Praise him with the sounding of the trumpet, praise him with the harp and lyre.")],
     [("H7030", "Qithros (Lyre/Harp)"), ("H7218", "Rosh (Head/Chief)"), ("H6754", "Tselem (Image/Statue)")]),

    ("H5837", "אֲרִיאֵל", "Ariel", "Proper noun / Noun, masculine", "Lion of God; Altar Hearth; Jerusalem",
     "A name meaning 'lion of God' applied to both Jerusalem and to the altar hearth — combining royal fierceness, sacred fire, and divine presence.",
     "The Hebrew <em>Ariel</em> combines <em>ari</em> (lion) and <em>El</em> (God) = 'lion of God.' In Isaiah 29:1-7 it is used as a poetic name for Jerusalem ('Woe to you, <em>Ariel</em>, <em>Ariel</em>, the city where David settled!'). In Ezekiel 43:15-16, <em>har'el</em> (variant spelling) refers to the altar hearth of the Temple — the place where the fire of God consumed the sacrifice. It also appears as a personal name (Ezra 8:16) and in 2 Samuel 23:20 where Benaiah kills 'two sons of <em>Ariel</em> of Moab.'",
     "The layered meaning of <em>Ariel</em> is theologically rich. Jerusalem as 'lion of God' invokes the lion of Judah's seat of power — but Isaiah 29 is a lament: the very city named for divine majesty becomes a place of distress and siege because of unfaithfulness. Yet even then, God promises to fight for Ariel (29:5-7). The altar hearth meaning (<em>ariel</em> in Ezekiel 43) points to the consuming fire of God's holiness meeting human sacrifice — the place of transformation. Both meanings converge in Christ: the Lion of Judah (Revelation 5:5) who is also the Lamb whose sacrifice kindles the fire of the Spirit.",
     [("Isaiah 29:1", "Woe to you, <em>Ariel</em>, <em>Ariel</em>, the city where David settled! Add year to year and let your cycle of festivals go on."),
      ("Isaiah 29:6", "the LORD Almighty will come with thunder and earthquake and great noise, with windstorm and tempest and flames of a devouring fire."),
      ("Ezekiel 43:15", "The altar hearth (<em>ariel</em>) is four cubits high, and four horns project upward from the hearth."),
      ("Ezra 8:16", "So I summoned Eliezer, Ariel, Shemaiah, Elnathan, Jarib, Elnathan, Nathan, Zechariah and Meshullam, who were leaders."),
      ("Revelation 5:5", "Then one of the elders said to me, 'Do not weep! See, the Lion of the tribe of Judah, the Root of David, has triumphed.'")],
     [("H738", "Aryeh (Lion)"), ("H410", "El (God)"), ("H4196", "Mizbeach (Altar)")]),

    ("H6184", "עָרִיץ", "Arits", "Adjective / Noun", "Ruthless; Tyrant; Terrible; Violent One",
     "The ruthless oppressor or tyrant — one who terrifies by violence and treats others with brutal contempt.",
     "The Hebrew <em>arits</em> (from <em>arats</em>, to be terrifying/dreadful) describes the violent, ruthless oppressor. It appears in Isaiah where 'the ruthless (<em>aritsim</em>) will vanish' (Isaiah 29:20), where the godly ask 'Where is the one who terrorized us?' (Isaiah 33:18), and where God promises that the <em>arits</em> will no longer be feared (Isaiah 49:25). Ezekiel uses it for the princes of Israel who have been 'like a roaring lion tearing its prey; they devour people, take treasures and precious things and make many widows.'",
     "The <em>arits</em> represents the domination system that crushes the vulnerable — the tyrant, the violent landlord, the ruthless creditor. Isaiah 29:20 promises eschatological reversal: 'The ruthless (<em>arits</em>) will vanish, the mockers will disappear, and all who have an eye for evil will be cut down.' This is the Magnificat's logic (Luke 1:51-53): the mighty are brought down, the humble lifted up. The oppressor's power is real but temporary. The God of Psalm 72 — who defends the poor, crushes the oppressor — will be the final Judge of every <em>arits</em>.",
     [("Isaiah 29:20", "The ruthless (<em>arits</em>) will vanish, the mockers will disappear, and all who have an eye for evil will be cut down."),
      ("Isaiah 33:18", "In your thoughts you will ponder the former terror: 'Where is that chief officer? Where is the one who took the revenue? Where is the officer in charge of the towers?'"),
      ("Isaiah 49:25", "But this is what the LORD says: 'Yes, captives will be taken from warriors, and plunder retrieved from the fierce (<em>arits</em>); I will contend with those who contend with you.'"),
      ("Psalm 72:4", "May he defend the afflicted among the people and save the children of the needy; may he crush the oppressor."),
      ("Luke 1:52", "He has brought down rulers from their thrones but has lifted up the humble.")],
     [("H6231", "Ashaq (Oppress)"), ("H1800", "Dal (Poor/Weak)"), ("H8199", "Shaphat (Judge/Govern)")]),

    ("H6558", "פֶּרֶץ", "Perets", "Proper noun / Noun", "Perez; Breach; Breaking Through",
     "The name Perez (son of Judah by Tamar), meaning 'breach' or 'breaking through' — carried in the Messianic genealogy from Genesis through Matthew.",
     "The Hebrew <em>Perets</em> (breach, breaking through) is born in one of the OT's most scandalous narratives: Judah and his daughter-in-law Tamar (Genesis 38). The name was given because Perez thrust past his twin brother at birth: 'What a breach you have made for yourself!' (Genesis 38:29). Despite this irregular origin, <em>Perets</em> appears in the Messianic genealogy: he is the ancestor of Boaz, who is the ancestor of Jesse, David, and ultimately Jesus (Ruth 4:18-22; Matthew 1:3).",
     "<em>Perets</em> is a theological emblem of grace overcoming shame. Born from an illicit union, conceived in a story of deception, his very name is an accusation — 'breach-maker.' Yet he stands in the line of the King of kings. Matthew 1:3 names him without apology in Jesus' genealogy, alongside Tamar (another irregular figure). The Messianic line runs through broken, complicated, even scandalous lives — because the point is not human worthiness but divine perseverance. God's purpose breaks through every obstacle, every moral failure, every 'what a breach you have made' — to bring forth the One who heals all breaches.",
     [("Genesis 38:29", "Then his brother came out, and the midwife said, 'So this is how you have broken out!' (<em>Perets</em>). And he was named <em>Perez</em>."),
      ("Ruth 4:18", "This, then, is the family line of <em>Perez</em>: Perez was the father of Hezron."),
      ("Ruth 4:12", "Through the offspring the LORD gives you by this young woman, may your family be like that of <em>Perez</em>, whom Tamar bore to Judah."),
      ("Matthew 1:3", "Judah the father of <em>Perez</em> and Zerah, whose mother was Tamar, Perez the father of Hezron, Hezron the father of Ram."),
      ("Micah 2:13", "The One who breaks open the way will go up before them; they will break through the gate and go out. Their King will pass through before them, the LORD at their head.")],
     [("H3063", "Yehudah (Judah)"), ("H8559", "Tamar (Tamar/Date Palm)"), ("H1732", "David (Beloved)")]),

    ("H6761", "צֶלַע", "Tsela", "Noun, feminine", "Stumbling; Adversity; Limping; Side",
     "A stumbling or fall — adversity, calamity, or the act of limping. Related to the word for 'rib' or 'side' in a separate usage.",
     "The Hebrew <em>tsela</em> in this entry (H6761) refers specifically to stumbling or adversity — a different usage from H6763 (<em>tsela</em>, rib/side). It appears in Psalm 35:15 ('when I stumbled, they gathered in glee; assailants gathered against me') and Jeremiah 20:10 ('I hear many whispering, 'Terror on every side! Denounce him!'). The sense is of vulnerable faltering — the moment when enemies see weakness and attack. The word captures the existential vulnerability of the righteous sufferer.",
     "The <em>tsela</em> (stumbling/adversity) in Psalm 35 is a lament pattern: the righteous person mourns, prays for enemies, and then discovers that enemies rejoice at the very stumbling they have helped cause. This is the theology of suffering under opposition — addressed supremely in the Servant Songs of Isaiah and in Jesus' own experience. Yet the Psalms consistently move from <em>tsela</em> (stumbling) to <em>simchah</em> (joy) and <em>tehillah</em> (praise). Psalm 37:24 promises: 'Though he may stumble (<em>naphal</em>), he will not fall, for the LORD upholds him with his hand.'",
     [("Psalm 35:15", "But when I stumbled, they gathered in glee; assailants gathered against me without my knowledge."),
      ("Jeremiah 20:10", "I hear many whispering, 'Terror on every side! Denounce him! Let's denounce him!' All my friends are waiting for me to slip, saying, 'Perhaps he will be deceived; then we will prevail over him.'"),
      ("Psalm 37:24", "Though he may stumble, he will not fall, for the LORD upholds him with his hand."),
      ("Proverbs 24:16", "For though the righteous fall seven times, they rise again, but the wicked stumble when calamity strikes."),
      ("Romans 8:28", "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.")],
     [("H5307", "Naphal (Fall/Overthrow)"), ("H6974", "Quts (Arise/Awake)"), ("H3444", "Yeshuah (Salvation)")]),

    ("H7969", "שָׁלוֹשׁ", "Shalosh", "Numeral", "Three; Third",
     "The number three — pervasive throughout Scripture in covenantal, resurrection, and Trinitarian patterns.",
     "The Hebrew <em>shalosh</em> (three) is one of the most theologically significant numbers in Scripture. It appears in the three-fold repetition of the divine name ('Holy, holy, holy' — Isaiah 6:3), the three patriarchs (Abraham, Isaac, Jacob), three days and three nights (Jonah 1:17; Matthew 12:40), the Temple's three-fold division (porch, holy place, holy of holies), Peter's three denials and three restorations, and the resurrection on the third day. Three is the number of divine completeness and testing.",
     "The pattern of <em>shalosh</em> in Scripture points toward the Triune nature of God (Father, Son, Spirit — Matthew 28:19; 2 Corinthians 13:14) and to the resurrection pattern established in the OT. Hosea 6:2 declares: 'After two days he will revive us; on the third day he will restore us.' Jonah's three days in the fish (Matthew 12:40) become the sign of the Son of Man. Jesus was raised on the third day 'according to the Scriptures' (1 Corinthians 15:4) — fulfilling the <em>shalosh</em> pattern embedded throughout OT narrative. Three is the number that opens into life.",
     [("Isaiah 6:3", "And they were calling to one another: 'Holy, holy, holy is the LORD Almighty; the whole earth is full of his glory.'"),
      ("Hosea 6:2", "After two days he will revive us; on the <em>third</em> day he will restore us, that we may live in his presence."),
      ("Jonah 1:17", "Now the LORD provided a huge fish to swallow Jonah, and Jonah was in the belly of the fish <em>three</em> days and <em>three</em> nights."),
      ("Genesis 40:12", "This is what it means: The <em>three</em> branches are <em>three</em> days."),
      ("1 Corinthians 15:4", "that he was buried, that he was raised on the <em>third</em> day according to the Scriptures.")],
     [("H705", "Arbaim (Forty)"), ("H8147", "Shenayim (Two)"), ("H702", "Arba (Four)")]),

    ("H8470", "תַּחַשׁ", "Tachash", "Noun, masculine", "Dugong Hide; Sea Cow Skin; Fine Leather",
     "The skin or hide of a sea creature (possibly dugong or manatee) used as a waterproof outer covering for the Tabernacle — a humble protection for sacred things.",
     "The Hebrew <em>tachash</em> refers to an animal skin used as the outermost covering of the Tabernacle (Exodus 26:14; 36:19; Numbers 4). The identity of the animal is debated: traditional translations say 'badger' or 'ram skins dyed red,' but modern scholars lean toward dugong (sea cow) or a North African animal with fine, waterproof hide. The <em>tachash</em> covering was the humble, weathered exterior of the Tabernacle — the last layer visible to outsiders, concealing the gold and sacred objects within.",
     "The theology of <em>tachash</em> skin is the theology of hiddenness and humility. The Tabernacle's exterior — rough, unadorned, unglamorous <em>tachash</em> hides — concealed glittering gold, the Ark of the Covenant, and the manifest presence of God. Isaiah 53:2 similarly describes the Suffering Servant: 'He had no beauty or majesty to attract us to him, nothing in his appearance that we should desire him.' God consistently chooses outer plainness to conceal inner glory. The manger, the carpenter's shop, the cross — all are <em>tachash</em> skins concealing the presence of the Divine.",
     [("Exodus 26:14", "Make for the tent a covering of ram skins dyed red, and over that a covering of the other durable leather (<em>tachash</em>)."),
      ("Numbers 4:6", "They are to cover this with <em>tachash</em> leather, spread a cloth of solid blue over that and put the poles in place."),
      ("Numbers 4:25", "They are to carry the curtains of the tabernacle and the tent of meeting, its covering and the outer covering of <em>tachash</em> leather."),
      ("Isaiah 53:2", "He grew up before him like a tender shoot, and like a root out of dry ground. He had no beauty or majesty to attract us to him."),
      ("2 Corinthians 4:7", "But we have this treasure in jars of clay to show that this all-surpassing power is from God and not from us.")],
     [("H168", "Ohel (Tent/Tabernacle)"), ("H727", "Aron (Ark)"), ("H3519", "Kabod (Glory)")]),

    ("H2160", "זִמְרִי", "Zimri", "Proper noun, masculine", "My Praise; My Music; Celebrated",
     "A Hebrew name meaning 'celebrated' or 'my music/praise' — borne by several OT figures including a king of Israel famous for violent usurpation and apostasy.",
     "The Hebrew name <em>Zimri</em> (from <em>zamar</em>, to sing/make music) means 'celebrated' or 'my praise.' It is borne by four OT figures: (1) Zimri son of Salu (Numbers 25:14), who openly sinned with a Moabite woman in Israel's camp during the Baal-Peor apostasy and was killed by Phinehas; (2) Zimri son of Zerah (1 Chronicles 2:6), a grandson of Judah; (3) Zimri the army commander who assassinated King Elah and seized Israel's throne (1 Kings 16:9-20), reigning only seven days before dying in his own burning palace; (4) a son of Jehoaddah in Benjamin's line.",
     "The irony of <em>Zimri</em> ('my praise/music') as the name of Israel's most notorious seven-day king is a poignant biblical irony. The name that should speak of worship and celebration is associated with violent usurpation, shameless apostasy, and swift judgment. Zimri king of Israel reigned exactly seven days — the shortest reign in Israel's history — then 'went into the inner room of the royal palace and set the palace on fire around him.' His story warns that a name connected to praise does not guarantee a life of worship. The truest music requires faithfulness, not just a fine name.",
     [("Numbers 25:14", "The name of the Israelite who was killed with the Midianite woman was <em>Zimri</em> son of Salu, the leader of a Simeonite family."),
      ("1 Kings 16:10", "<em>Zimri</em> went in, struck him down and killed him in the twenty-seventh year of Asa king of Judah. Then he succeeded him as king."),
      ("1 Kings 16:15", "In the twenty-seventh year of Asa king of Judah, <em>Zimri</em> reigned in Tirzah seven days."),
      ("1 Kings 16:18", "When <em>Zimri</em> saw that the city was taken, he went into the citadel of the royal palace and set the palace on fire around him. So he died."),
      ("Psalm 66:2", "Sing the glory of his name; make his praise glorious.")],
     [("H2167", "Zamar (Sing Praises)"), ("H4428", "Melek (King)"), ("H6663", "Tsadaq (Be Righteous)")]),

    ("H3221", "יַם", "Yam", "Noun, masculine (Aramaic)", "Sea (Aramaic); The Great Waters",
     "The Aramaic word for sea — used in Daniel's visions of the four great beasts emerging from the churning cosmic sea.",
     "The Aramaic <em>yam</em> (parallel to Hebrew H3220 <em>yam</em>) appears in Daniel 7:2-3 in one of the most consequential prophetic visions in Scripture: 'Daniel said: In my vision at night I looked, and there before me were the four winds of heaven churning up the great sea (<em>yamma rabbah</em>). Four great beasts, each different from the others, came up out of the sea.' The sea in Daniel's vision is the primordial chaos-sea — the cosmic deep — out of which empires rise and fall.",
     "The cosmic <em>yam</em> in Daniel 7 draws on ancient Near Eastern mythology (the sea as the domain of chaos, darkness, and the powers hostile to God) and transforms it into apocalyptic vision. Four empires emerge from the churning sea like beasts — Babylonian, Medo-Persian, Greek, Roman. But the Son of Man comes 'on the clouds of heaven' (Daniel 7:13) — from above, not from below; from God's domain, not the chaos sea. Revelation 21:1 announces the ultimate eschatological reversal: 'There was no longer any sea.' The chaos-sea is abolished, and the New Jerusalem descends from heaven.",
     [("Daniel 7:2", "Daniel said: 'In my vision at night I looked, and there before me were the four winds of heaven churning up the great <em>sea</em> (<em>yamma</em>).'"),
      ("Daniel 7:3", "Four great beasts, each different from the others, came up out of the <em>sea</em>."),
      ("Daniel 7:13", "In my vision at night I looked, and there before me was one like a son of man, coming with the clouds of heaven."),
      ("Revelation 13:1", "The dragon stood on the shore of the sea. And I saw a beast coming out of the sea."),
      ("Revelation 21:1", "Then I saw a new heaven and a new earth, for the first heaven and the first earth had passed away, and there was no longer any <em>sea</em>.")],
     [("H3220", "Yam (Sea — Hebrew)"), ("H7307", "Ruach (Spirit/Wind)"), ("H1121", "Ben (Son)")]),

    ("H4641", "מַעֲשֵׂיָה", "Maaseiah", "Proper noun, masculine", "Work of YHWH; Whom YHWH Made",
     "A Hebrew name meaning 'work of the LORD' — borne by numerous priests, Levites, and officials in the OT, particularly during the reforms of Josiah, Nehemiah, and Ezra.",
     "The name <em>Maaseiah</em> combines <em>ma'aseh</em> (work/deed) with <em>Yah</em> (the LORD) = 'work of the LORD' or 'whom the LORD made/does.' It is one of the most common priestly names in the OT — appearing over 20 times across Ezra, Nehemiah, Jeremiah, and Chronicles. Significant bearers include a Levite musician in David's service (1 Chronicles 15:18), an officer under King Joash (2 Chronicles 23:1), a governor of Jerusalem under Josiah (2 Chronicles 34:8), and a priest who stood beside Ezra as the Law was read (Nehemiah 8:4).",
     "The frequency of the name <em>Maaseiah</em> in priestly and reform contexts is striking. 'Work of the LORD' was a name that covenant families aspired to give their sons — an expectation that this child would be shaped by divine action and would himself become evidence of God's active work in Israel. Nehemiah 8:4 preserves one of the most evocative scenes in the OT: Ezra standing on a wooden platform, flanked by thirteen men including <em>Maaseiah</em>, reading the Law to all the people. These were men whose names proclaimed 'work of the LORD' — and they participated in one of Israel's greatest spiritual renewals.",
     [("Nehemiah 8:4", "Ezra the teacher of the Law stood on a high wooden platform built for the occasion. Beside him on his right stood Mattithiah, Shema, Anaiah, Uriah, Hilkiah and <em>Maaseiah</em>."),
      ("2 Chronicles 34:8", "In the eighteenth year of his reign, in order to purify the land and the temple, Josiah sent Shaphan son of Azaliah, <em>Maaseiah</em> the ruler of the city, and Joah son of Joahaz, the recorder, to repair the temple of the LORD his God."),
      ("1 Chronicles 15:18", "With them were their relatives next in rank: Zechariah, Jaaziel, Shemiramoth, Jehiel, Unni, Eliab, Benaiah, <em>Maaseiah</em>, Mattithiah, Eliphelehu, Mikneiah, Obed-Edom and Jeiel, the gatekeepers."),
      ("Ezra 10:18", "Among the descendants of the priests, the following had married foreign women: From the descendants of Jeshua son of Jozadak, and his brothers: <em>Maaseiah</em>, Eliezer, Jarib and Gedaliah."),
      ("Psalm 92:4", "For you make me glad by your deeds, LORD; I sing for joy at what your hands have done.")],
     [("H4639", "Maasah (Work/Deed)"), ("H3050", "Yah (LORD/YHWH)"), ("H3548", "Kohen (Priest)")]),

    ("H5968", "עָלַף", "Alaph", "Verb", "To Faint; To Cover Over; To Be Enveloped",
     "To faint, grow faint, or be covered over — used for physical collapse from exhaustion and for the spiritual languishing of the soul.",
     "The Hebrew <em>alaph</em> means to faint, swoon, or grow weak — to be enveloped by exhaustion or grief until one collapses. It appears in Amos 8:13 ('young women and strong young men will faint (<em>alapph</em>) from thirst'), in Song of Songs 2:5 ('I am faint with love' — rendered 'sick with love' in some translations), and in Isaiah 51:20 where Zion's sons have 'fainted... like antelope caught in a net.' The word captures the total depletion of strength — body and soul given out.",
     "The <em>alaph</em> of Song of Songs 2:5 ('I am faint with love') is one of the most theologically beautiful uses of this verb. The bride is not collapsed from despair or thirst but from the overwhelming weight of love — too much grace, too much nearness. Bernard of Clairvaux built much of his mystical theology on this verse. And Amos 8:13 warns that those who have despised God's word will one day faint — not from too much divine presence but from its total absence: 'a famine of hearing the words of the LORD' (Amos 8:11). Faint with love, or faint from thirst: these are the two directions of the human soul.",
     [("Song of Songs 2:5", "Strengthen me with raisins, refresh me with apples, for I am <em>faint</em> (<em>alaph</em>) with love."),
      ("Amos 8:13", "In that day the lovely young women and strong young men will <em>faint</em> because of thirst."),
      ("Isaiah 51:20", "Your children have fainted; they lie at every street corner, like antelope caught in a net."),
      ("Amos 8:11", "The days are coming, declares the Sovereign LORD, when I will send a famine through the land — not a famine of food or a thirst for water, but a famine of hearing the words of the LORD."),
      ("Psalm 63:1", "You, God, are my God, earnestly I seek you; I thirst for you, my whole being longs for you, in a dry and parched land where there is no water.")],
     [("H5315", "Nephesh (Soul/Life)"), ("H5771", "Avon (Iniquity — cause of faintness)"), ("H1129", "Banah (Build — restoration)")]),

    ("H5984", "עַמּוֹנִי", "Ammoni", "Adjective / Gentillic noun", "Ammonite; Descendant of Ammon",
     "An Ammonite — a descendant of Ben-Ammi, son of Lot, whose nation was perpetually in tension with Israel yet produced Ruth-like figures of conversion.",
     "The Hebrew <em>Ammoni</em> (Ammonite) refers to the people descended from Ben-Ammi, the son of Lot by his younger daughter (Genesis 19:38). The Ammonites were Israel's neighbors east of the Jordan, frequently hostile — Deuteronomy 23:3 excludes them from the assembly of the LORD 'even to the tenth generation.' They worshipped Molech (Milcom), the god associated with child sacrifice. Yet Naamah the Ammonite was the mother of Solomon's son Rehoboam (1 Kings 14:21), and Ruth — though not an Ammonite but a Moabite — represents the kind of gentile who crosses the boundary of exclusion through covenant loyalty.",
     "The Ammonites represent a recurring theological tension: the excluded people who are nonetheless drawn into God's story. Their exclusion from Israel's assembly (Deuteronomy 23:3) is permanent under the Law, yet their women became wives of Israelite kings, and their descendants appear in genealogies. Nehemiah 13 records Tobiah the Ammonite's opposition to Jerusalem's restoration — yet Nehemiah's reforms ultimately prevailed. The NT's expansion of the gospel to 'all nations' (Matthew 28:19) retroactively reframes these exclusions: in Christ, there is neither Jew nor Greek, Ammonite nor Israelite (Colossians 3:11).",
     [("Genesis 19:38", "The younger daughter also had a son, and she named him Ben-Ammi; he is the father of the Ammonites (<em>Ammoni</em>) of today."),
      ("Deuteronomy 23:3", "No Ammonite (<em>Ammoni</em>) or Moabite or any of their descendants may enter the assembly of the LORD, not even in the tenth generation."),
      ("1 Kings 14:21", "Rehoboam son of Solomon was king in Judah. His mother's name was Naamah; she was an Ammonite (<em>Ammoni</em>)."),
      ("Nehemiah 4:3", "Tobiah the <em>Ammonite</em>, who was at his side, said, 'What they are building — even a fox climbing up on it would break down their wall of stones!'"),
      ("Colossians 3:11", "Here there is no Gentile or Jew, circumcised or uncircumcised, barbarian, Scythian, slave or free, but Christ is all, and is in all.")],
     [("H4124", "Moab (Moabite)"), ("H3876", "Lot (Lot — ancestor)"), ("H3816", "Leom (Nation/People)")]),
]

# ============================================================
# GREEK WORDS (23)
# ============================================================
greek_words = [

    ("G1736", "ἐνδημέω", "Endēmeō", "Verb", "To Be at Home; To Be Present; To Dwell",
     "To be present, at home, or dwelling in a place — used by Paul for the contrast between being 'at home' in the body versus being 'at home' with the Lord.",
     "The Greek <em>endēmeō</em> (from <em>en</em> + <em>dēmos</em>, people/land) means to be present in one's homeland, to dwell at home. Paul uses it three times in 2 Corinthians 5:6-9 in a rich theological passage about embodied and unembodied existence: 'While we are at home (<em>endēmountes</em>) in the body we are away from the Lord... We are confident, I say, and would prefer to be away from the body and at home (<em>endēmēsai</em>) with the Lord.' The word is weighty: 'home' with God is the true homeland.",
     "Paul's use of <em>endēmeō</em> in 2 Corinthians 5 reveals his eschatological homesickness. The body is a dwelling, a tent (2 Corinthians 5:1), a temporary residence — but it is not home. True home is <em>pros ton Kyrion</em> — with the Lord. This is not an escapist dualism (Paul immediately affirms that whether present or absent, the goal is to please God) but a proper ordering of ultimate belonging. Every Christian is, in a sense, an exile in the body — longing for the homeland where God himself will be 'all in all' (1 Corinthians 15:28). The <em>endēmountes</em> with the Lord is the destination of all sanctification.",
     [("2 Corinthians 5:6", "Therefore we are always confident and know that as long as we are <em>at home</em> in the body we are away from the Lord."),
      ("2 Corinthians 5:8", "We are confident, I say, and would prefer to be away from the body and <em>at home</em> with the Lord."),
      ("2 Corinthians 5:9", "So we make it our goal to please him, whether we are <em>at home</em> in the body or away from it."),
      ("Philippians 1:23", "I am torn between the two: I desire to depart and be with Christ, which is better by far."),
      ("John 14:3", "And if I go and prepare a place for you, I will come back and take you to be with me that you also may be where I am.")],
     [("G1927", "Epidēmeō (To Sojourn/Reside Temporarily)"), ("G3611", "Oikeō (To Dwell/Inhabit)"), ("G3956", "Pas (All — 'all in all')")]),

    ("G1825", "ἐξεγείρω", "Exegeirō", "Verb", "To Raise Up; To Rouse; To Wake from Sleep or Death",
     "To fully rouse or raise up — used for God's raising of Pharaoh to display His power and for the future resurrection of the dead.",
     "The Greek <em>exegeirō</em> (from <em>ek</em>, out of + <em>egeirō</em>, to raise) means to raise up completely, to rouse from sleep or death. It appears in Romans 9:17 in a quotation from Exodus 9:16: 'For Scripture says to Pharaoh: I raised you up (<em>exēgeiran</em>) for this very purpose, that I might display my power in you and that my name might be proclaimed in all the earth.' In 1 Corinthians 6:14 it describes the resurrection of believers: 'By his power God raised (<em>exegerei</em>) the Lord from the dead, and he will raise us also.'",
     "The two uses of <em>exegeirō</em> in Paul create a stunning theological contrast. God raised up (<em>exegeirō</em>) Pharaoh — the most powerful man in the ancient world — as a vehicle for displaying divine sovereignty over hardened opposition. And God raised up (<em>exegeirō</em>) Jesus from the dead — and will raise all believers in the same power. The same verb covers both the raising up of an enemy for judgment and the raising up of a Savior for salvation. Resurrection and sovereignty share the same Greek word — reminding us that the same God who controls the hardening of Pharaoh's heart also commands the tombs to open.",
     [("Romans 9:17", "For Scripture says to Pharaoh: 'I raised you up (<em>exēgeiran</em>) for this very purpose, that I might display my power in you.'"),
      ("1 Corinthians 6:14", "By his power God raised (<em>exegerei</em>) the Lord from the dead, and he will raise us also."),
      ("Exodus 9:16", "But I have raised you up for this very purpose, that I might show you my power and that my name might be proclaimed in all the earth."),
      ("Romans 9:18", "Therefore God has mercy on whom he wants to have mercy, and he hardens whom he wants to harden."),
      ("1 Corinthians 15:52", "In a flash, in the twinkling of an eye, at the last trumpet. For the trumpet will sound, the dead will be raised imperishable.")],
     [("G1453", "Egeirō (To Raise/Awaken)"), ("G386", "Anastasis (Resurrection)"), ("G1411", "Dynamis (Power)")]),

    ("G1915", "ἐπίβλημα", "Epiblēma", "Noun, neuter", "Patch; Piece Sewn On; Covering Cloth",
     "A patch sewn onto clothing — used by Jesus in the parable of new cloth on old garments to teach the incompatibility of the gospel with the old covenant forms.",
     "The Greek <em>epiblēma</em> (from <em>epi</em>, upon + <em>ballō</em>, to throw/put) is a patch or covering — specifically a piece of cloth placed over a tear. It appears in all three Synoptics in Jesus' parable of the patched garment: 'No one sews a patch (<em>epiblēma</em>) of unshrunk cloth on an old garment, for the patch will pull away from the garment, making the tear worse' (Matthew 9:16; Mark 2:21; Luke 5:36). This parable is paired with the new wine in old wineskins — both illustrating the radical newness of the kingdom.",
     "The <em>epiblēma</em> parable is Jesus' own commentary on the relationship between the new covenant and the old. The issue is not that the old garment is bad — it is simply old, worn, established. The new cloth (the unshrunk, unbleached kingdom teaching) cannot simply be patched onto the old forms. The <em>epiblēma</em> would tear away and make things worse. This is not abolition but fulfillment — Jesus comes not to patch Judaism but to transfigure it from within. Hebrews unpacks this theologically: the old covenant was a 'shadow' (Hebrews 8:5; 10:1) and the new covenant replaces the obsolete with the eternal (Hebrews 8:13).",
     [("Matthew 9:16", "No one sews a patch (<em>epiblēma</em>) of unshrunk cloth on an old garment, for the patch will pull away from the garment, making the tear worse."),
      ("Mark 2:21", "No one sews a patch (<em>epiblēma</em>) of unshrunk cloth on an old garment. Otherwise, the new piece will pull away from the old, making the tear worse."),
      ("Luke 5:36", "He told them this parable: 'No one tears a piece out of a new garment to patch (<em>epiblēma</em>) an old one.'"),
      ("Hebrews 8:13", "By speaking of a new covenant he has made the first one obsolete; and what is obsolete and aging will soon disappear."),
      ("Matthew 5:17", "Do not think that I have come to abolish the Law or the Prophets; I have not come to abolish them but to fulfill them.")],
     [("G3501", "Neos (New)"), ("G3820", "Palaios (Old)"), ("G3631", "Oinos (Wine)")]),

    ("G1935", "ἐπιθανάτιος", "Epithanatios", "Adjective", "Condemned to Death; Appointed for Death",
     "Appointed for death — condemned to die, like a criminal awaiting execution. Paul uses it for his own apostolic experience.",
     "The Greek <em>epithanatios</em> (from <em>epi</em>, upon/at + <em>thanatos</em>, death) means one appointed to death, condemned as a criminal to be executed. It appears once in the NT: 1 Corinthians 4:9 — 'For it seems to me that God has put us apostles on display at the end of the procession, like those condemned to death (<em>epithanatious</em>). We have been made a spectacle to the whole universe, to angels as well as to human beings.' Paul draws on the image of Roman triumphal processions where captives condemned to die were displayed at the end.",
     "The <em>epithanatios</em> of 1 Corinthians 4:9 is Paul's savage rebuttal to the Corinthians' triumphalism. They were already reigning, already rich, already kings — while the apostles trailed at the end of God's procession as condemned men. The image of the Roman triumph's final display is precise: these were the prisoners who would be killed in the arena after the parade. Paul's theology of the cross produces this 'theology of the cross' for ministry: true apostolic power is displayed in weakness, suffering, and apparent failure. This was incomprehensible to Corinthian culture — and remains countercultural today.",
     [("1 Corinthians 4:9", "For it seems to me that God has put us apostles on display at the end of the procession, like those <em>condemned to death</em> (<em>epithanatious</em>)."),
      ("1 Corinthians 4:10", "We are fools for Christ, but you are so wise in Christ! We are weak, but you are strong! You are honored, we are dishonored!"),
      ("2 Corinthians 4:11", "For we who are alive are always being given over to death for Jesus' sake, so that his life may also be revealed in our mortal body."),
      ("Romans 8:36", "As it is written: 'For your sake we face death all day long; we are considered as sheep to be slaughtered.'"),
      ("Philippians 2:8", "And being found in appearance as a man, he humbled himself by becoming obedient to death — even death on a cross!")],
     [("G2288", "Thanatos (Death)"), ("G769", "Astheneia (Weakness)"), ("G5287", "Hupostasis (Substance/Confidence)")]),

    ("G2180", "Ἐφέσιος", "Ephesios", "Proper adjective / Noun", "Ephesian; Of Ephesus",
     "An Ephesian — a citizen or inhabitant of Ephesus, the great port city of Asia Minor and Paul's most strategic mission base.",
     "The Greek <em>Ephesios</em> refers to a person from Ephesus (modern-day Turkey), the capital of the Roman province of Asia. Ephesus was one of the largest cities in the Roman Empire, home to the Temple of Artemis (one of the Seven Wonders), a major port, and a commercial center. Paul spent three years there (Acts 20:31) — his longest stay in any city. The Ephesian church was the recipient of one of Paul's most theologically profound letters. Acts 19 records both the dramatic growth of the gospel in Ephesus and the riot of the silversmiths defending their Artemis trade.",
     "Ephesus represents the intersection of pagan religion, commercial power, and apostolic gospel. The <em>Ephesioi</em> who rioted in Acts 19 ('Great is Artemis of the Ephesians!' — Acts 19:28) demonstrate how economic interests defend false religion. Yet the same city produced the church to which Paul wrote his most elevated Christological letter — the epistle where Christ is presented as the head of all things, and the church as his body and fullness (Ephesians 1:22-23). Revelation 2:1-7 addresses Ephesus as the first of the seven churches — praised for perseverance, rebuked for abandoning its first love. The greatest churches can lose their greatest virtue.",
     [("Acts 19:28", "When they heard this, they were furious and began shouting: 'Great is Artemis of the <em>Ephesians</em>!'"),
      ("Acts 19:35", "The city clerk quieted the crowd and said: 'Fellow <em>Ephesians</em>, doesn't all the world know that the city of Ephesus is the guardian of the temple of the great Artemis?'"),
      ("Ephesians 1:22", "And God placed all things under his feet and appointed him to be head over everything for the church."),
      ("Revelation 2:4", "Yet I hold this against you: You have forsaken the love you had at first."),
      ("Acts 20:17", "From Miletus, Paul sent to Ephesus for the elders of the church.")],
     [("G116", "Athēnai (Athens)"), ("G4172", "Polis (City)"), ("G1577", "Ekklēsia (Church/Assembly)")]),

    ("G2276", "ἥττων", "Hēttōn", "Adjective (comparative)", "Worse; Less; Inferior",
     "Worse or inferior — the comparative form of 'bad/little' used in contexts of spiritual and moral deterioration.",
     "The Greek <em>hēttōn</em> (also <em>hēsson</em>) is the comparative adjective meaning 'worse' or 'less.' It appears in 1 Corinthians 11:17 where Paul says the Corinthian assembly has come together 'not for the better but for the worse (<em>hēsson</em>)' — referring to their divisive Lord's Supper practices. It also appears in 2 Peter 2:20: 'If they have escaped the corruption of the world by knowing our Lord and Savior Jesus Christ and are again entangled in it and are overcome, they are worse off (<em>ta eschata cheirona tōn prōtōn</em>) at the end than they were at the beginning.'",
     "Paul's use of <em>hēttōn</em> in 1 Corinthians 11:17 is a stinging indictment: the church's gatherings were making things <em>worse</em> rather than better. The Lord's Supper — the apex expression of Christ's self-giving community — had become a venue for class division, hunger for the poor, and drunkenness for the rich. When Christian practices reinforce worldly divisions rather than gospel equality, they become spiritually regressive. This is the anti-Gospel: a church that meets and deteriorates. The remedy Paul prescribes is <em>discernment</em> — recognizing the body of Christ in one another (1 Corinthians 11:29).",
     [("1 Corinthians 11:17", "In the following directives I have no praise for you, for your meetings do more harm than good — you come together not for the better but for the <em>worse</em>."),
      ("2 Peter 2:20", "If they have escaped the corruption of the world by knowing our Lord and Savior Jesus Christ and are again entangled in it and are overcome, they are <em>worse off</em> at the end than they were at the beginning."),
      ("Matthew 12:45", "Then it goes and takes with it seven other spirits more wicked than itself, and they go in and live there. And the final condition of that person is <em>worse</em> than the first."),
      ("2 Corinthians 12:15", "So I will very gladly spend for you everything I have and expend myself as well. If I love you more, will you love me <em>less</em>?"),
      ("Hebrews 10:29", "How much more severely do you think someone deserves to be punished who has trampled the Son of God underfoot?")],
     [("G2570", "Kalos (Good/Beautiful)"), ("G3123", "Mallon (Rather/More)"), ("G4983", "Sōma (Body)")]),

    ("G2421", "Ἰεσσαί", "Iessai", "Proper noun, masculine", "Jesse; Father of David",
     "Jesse of Bethlehem — father of King David and progenitor of the Messianic line, referenced in the 'root of Jesse' prophecies.",
     "The Greek <em>Iessai</em> transliterates the Hebrew <em>Yishai</em> (Jesse). Jesse was the grandson of Boaz and Ruth, father of eight sons including David, and grandfather (by extension) of the entire Davidic dynasty. He appears in Ruth 4:17-22, 1 Samuel 16-17, and in the Messianic prophecy of Isaiah 11:1: 'A shoot will come up from the stump of Jesse; from his roots a Branch will bear fruit.' In the NT, Jesse appears in Matthew 1:5-6, Luke 3:32, Acts 13:22, and Romans 15:12.",
     "Isaiah 11:1 chooses the name <em>Jesse</em> rather than <em>David</em> for the Messianic root — and this is theologically significant. By the time Isaiah prophesied, the Davidic dynasty had grown proud. Going back to Jesse — David's humble father, a Bethlehemite shepherd — strips away the regal accoutrements and returns to the root. The Messiah will not come from the palace but from the stump — the cut-down tree of Davidic promise. Paul quotes the 'root of Jesse' prophecy in Romans 15:12 ('the Root of Jesse will spring up, one who will arise to rule over the nations; in him the Gentiles will hope') as the scriptural basis for Gentile inclusion in the gospel.",
     [("Isaiah 11:1", "A shoot will come up from the stump of <em>Jesse</em>; from his roots a Branch will bear fruit."),
      ("Romans 15:12", "And again, Isaiah says, 'The Root of <em>Jesse</em> will spring up, one who will arise to rule over the nations; in him the Gentiles will hope.'"),
      ("Matthew 1:5", "Salmon the father of Boaz, whose mother was Rahab, Boaz the father of Obed, whose mother was Ruth, Obed the father of <em>Jesse</em>."),
      ("1 Samuel 16:1", "The LORD said to Samuel, 'How long will you mourn for Saul, since I have rejected him as king over Israel? Fill your horn with oil and be on your way; I am sending you to <em>Jesse</em> of Bethlehem.'"),
      ("Revelation 5:5", "See, the Lion of the tribe of Judah, the Root of David, has triumphed.")],
     [("G1138", "David (David/Beloved)"), ("G4491", "Rhiza (Root)"), ("G5547", "Christos (Christ/Anointed)")]),

    ("G2515", "καθέδρα", "Kathedra", "Noun, feminine", "Chair; Seat; Teacher's Chair",
     "A seat or chair — used for the seat of Moses (the authoritative teaching chair) and for the money-changers' seats in the Temple.",
     "The Greek <em>kathedra</em> (origin of the English 'cathedral') means a chair or seat, especially one of authority. It appears three times in the NT: Matthew 21:12 and Mark 11:15, where Jesus 'overturned the tables of the money changers and the <em>kathedras</em> of those selling doves'; and Matthew 23:2, where Jesus says 'The teachers of the law and the Pharisees sit in Moses' seat (<em>kathedra</em>).' A 'cathedral' is literally the church with the bishop's chair — the teaching seat.",
     "The <em>kathedra</em> of Moses in Matthew 23:2 is a physical seat in the synagogue from which the Torah was authoritatively read and interpreted. Jesus acknowledges its authority while condemning the hypocrisy of those who occupy it: 'do what they say, not what they do.' Then in Matthew 21, Jesus overturns the <em>kathedras</em> of the dove-sellers — the very seats of commercial religion within the Temple courts. The seat of teaching authority is holy when it serves God's people; it becomes a den of thieves when it exploits them. The cleansing of the Temple is Jesus asserting a higher teaching authority than any <em>kathedra</em>.",
     [("Matthew 23:2", "The teachers of the law and the Pharisees sit in Moses' seat (<em>kathedra</em>)."),
      ("Matthew 21:12", "Jesus entered the temple courts and drove out all who were buying and selling there. He overturned the tables of the money changers and the benches (<em>kathedras</em>) of those selling doves."),
      ("Mark 11:15", "On reaching Jerusalem, Jesus entered the temple courts and began driving out those who were buying and selling there. He overturned the tables of the money changers and the benches (<em>kathedras</em>) of the dove sellers."),
      ("John 8:2", "At dawn he appeared again in the temple courts, where all the people gathered around him, and he sat down to teach them."),
      ("Matthew 23:3", "So you must be careful to do everything they tell you. But do not do what they do, for they do not practice what they preach.")],
     [("G1320", "Didaskalos (Teacher)"), ("G4864", "Sunagōgē (Synagogue)"), ("G2417", "Hierosulos (Temple Robber)")]),

    ("G2656", "κατανεύω", "Kataneuō", "Verb", "To Signal; To Beckon; To Nod",
     "To give a signal by nodding or gesturing — used for Peter and John beckoning their fishing partners to come help with the miraculous catch.",
     "The Greek <em>kataneuō</em> (from <em>kata</em>, down/toward + <em>neuō</em>, to nod) means to signal by nodding the head or gesturing — a silent communication across a distance. It appears once in the NT: Luke 5:7, where after the miraculous catch of fish, Simon Peter and his partners 'beckoned (<em>kateneuson</em>) to their partners in the other boat to come and help them.' The boats were filling with fish and beginning to sink — a pantomimed cry for help across the water.",
     "The single use of <em>kataneuō</em> in Luke 5 is a vivid detail of eyewitness narrative. The miraculous catch was so overwhelming that the fishermen could not even shout — they gestured. James and John in the other boat saw the signal and came. This silent beckon across the water, in the immediate aftermath of the miraculous catch, captures the moment of transition: Simon Peter fell at Jesus' knees saying 'Go away from me, Lord; I am a sinful man.' Jesus answered: 'Don't be afraid; from now on you will fish for people.' The <em>kataneuō</em> — the signal that summoned partners for earthly fish — becomes the call to summon partners for the kingdom.",
     [("Luke 5:7", "So they signaled (<em>kateneuson</em>) their partners in the other boat to come and help them, and they came and filled both boats so full that they began to sink."),
      ("Luke 5:4", "When he had finished speaking, he said to Simon, 'Put out into deep water, and let down the nets for a catch.'"),
      ("Luke 5:8", "When Simon Peter saw this, he fell at Jesus' knees and said, 'Go away from me, Lord; I am a sinful man!'"),
      ("Luke 5:10", "Then Jesus said to Simon, 'Don't be afraid; from now on you will fish for people.'"),
      ("Matthew 4:19", "Come, follow me, Jesus said, and I will send you out to fish for people.")],
     [("G3漁", ""), ("G614", "Apokryphos (Hidden)"), ("G4137", "Plēroō (Fill/Fulfill)")]),

    ("G2731", "κατοίκησις", "Katoikēsis", "Noun, feminine", "Dwelling; Habitation; Abode",
     "A dwelling place or habitation — used for the tombs where Legion dwelt and for the dwelling of God's Spirit in believers.",
     "The Greek <em>katoikēsis</em> (from <em>katoikeō</em>, to dwell) means a place of permanent dwelling or habitation. It appears once in the NT in its noun form: Mark 5:3, where the demoniac Legion 'lived (<em>katoikēsin</em>) in the tombs' — his dwelling was among the dead. The related verb <em>katoikeō</em> is used extensively for God's presence: the fullness of deity 'dwells' (<em>katoikei</em>) in Christ (Colossians 2:9), and God's Spirit 'dwells' in believers (Romans 8:11).",
     "The single NT use of <em>katoikēsis</em> in Mark 5:3 is striking: the demon-possessed man's permanent dwelling was a graveyard — among the dead, unclean, bound, crying out and cutting himself. This is the demonic counterfeit of <em>katoikēsis</em>: a dwelling among death rather than life. When Jesus restored him, he was found 'sitting, dressed and in his right mind' (Mark 5:15) — a new habitation in sanity and dignity. The theology of dwelling runs throughout Scripture from the Garden (God walking with humanity) to Revelation 21:3 ('Now the dwelling (<em>skēnē</em>) of God is with humans'). Where we dwell reveals what or who we belong to.",
     [("Mark 5:3", "This man lived (<em>katoikēsin eichon</em>) in the tombs, and no one could bind him anymore, not even with a chain."),
      ("Colossians 2:9", "For in Christ all the fullness of the Deity lives (<em>katoikei</em>) in bodily form."),
      ("Romans 8:11", "And if the Spirit of him who raised Jesus from the dead is living in you, he who raised Christ from the dead will also give life to your mortal bodies."),
      ("Revelation 21:3", "And I heard a loud voice from the throne saying, 'Look! God's dwelling place is now among the people.'"),
      ("Ephesians 3:17", "so that Christ may dwell (<em>katoikēsai</em>) in your hearts through faith.")],
     [("G3611", "Oikeō (To Dwell)"), ("G4151", "Pneuma (Spirit)"), ("G1228", "Diabolos (Devil)")]),

    ("G3055", "λογομαχία", "Logomachia", "Noun, feminine", "Word-Battle; Quarreling About Words; Controversy",
     "Contentious arguing over words — Paul's term for the destructive theological hair-splitting that tears churches apart without producing godliness.",
     "The Greek <em>logomachia</em> (from <em>logos</em>, word + <em>machē</em>, battle/fight) means a battle of words — specifically the kind of petty, contentious disputing over terminology and verbal minutiae that produces no spiritual fruit. Paul uses the cognate verb <em>logomachein</em> in 2 Timothy 2:14 and the noun <em>logomachia</em> in 1 Timothy 6:4. In 1 Timothy 6:3-5, Paul describes false teachers as 'conceited and understanding nothing' who have 'an unhealthy interest in controversies and <em>logomachiai</em> that result in envy, strife, malicious talk, evil suspicions and constant friction.'",
     "The theology of <em>logomachia</em> is a study in how the good gift of language (logos) becomes weaponized. The Pastoral Epistles consistently warn against speculative, contentious theological debating that abandons the 'pattern of sound teaching' (2 Timothy 1:13) for unprofitable verbal warfare. This is not a warning against serious theological inquiry — Paul's letters are themselves works of deep theological reasoning. The target is arguing for the sake of argument, using words to establish social dominance rather than build up the body. James 3:9-10 captures the same pathology: the same tongue that blesses God curses people. <em>Logomachia</em> is the tongue turned against the community it should serve.",
     [("1 Timothy 6:4", "they are conceited and understand nothing. They have an unhealthy interest in controversies and <em>quarrels about words</em> (<em>logomachias</em>) that result in envy, strife, malicious talk, evil suspicions."),
      ("2 Timothy 2:14", "Keep reminding God's people of these things. Warn them before God against quarreling about words (<em>logomachein</em>); it is of no value, and only ruins those who listen."),
      ("Titus 3:9", "But avoid foolish controversies and genealogies and arguments and quarrels about the law, because these are unprofitable and useless."),
      ("James 3:10", "Out of the same mouth come praise and cursing. My brothers and sisters, this should not be."),
      ("2 Timothy 2:16", "Avoid godless chatter, because those who indulge in it will become more and more ungodly.")],
     [("G3056", "Logos (Word/Reason)"), ("G3163", "Machē (Battle/Quarrel)"), ("G2150", "Eusebeia (Godliness)")]),

    ("G3308", "μέριμνα", "Merimna", "Noun, feminine", "Anxiety; Worry; Care; Concern",
     "Anxious care or worry — the divided mind pulled in multiple directions, contrasted with the single-minded trust Paul commands in Philippians 4:6.",
     "The Greek <em>merimna</em> (from <em>merizō</em>, to divide + <em>nous</em>, mind) literally means a divided mind — the state of being pulled in multiple directions by worry. It appears in Matthew 13:22 (the thorns that choke the word are 'the worries (<em>merimna</em>) of this life'), Luke 21:34 (do not let <em>merimna</em> weigh down your hearts), 1 Peter 5:7 ('Cast all your <em>merimna</em> on him because he cares for you'), and 2 Corinthians 11:28 (Paul's daily burden: 'the care (<em>merimna</em>) for all the churches').",
     "Jesus identifies <em>merimna</em> as one of the three great soil-destroyers (Matthew 13:22) — thorns that choke the word of God. The anxious person is not evil; they are simply divided — pulled between trust in God and fear of circumstances. Paul's remedy in Philippians 4:6 is precise: 'Do not be anxious (<em>merimnate</em>) about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.' The antidote to divided-mind anxiety is concentrated prayer — bringing the divided concerns into the single focal point of God's presence. The peace that follows (<em>hē eirēnē tou Theou</em>) guards the mind that prayer has unified.",
     [("Matthew 13:22", "The seed falling among the thorns refers to someone who hears the word, but the worries (<em>merimna</em>) of this life and the deceitfulness of wealth choke the word, making it unfruitful."),
      ("1 Peter 5:7", "Cast all your anxiety (<em>merimnan</em>) on him because he cares for you."),
      ("Philippians 4:6", "Do not be anxious (<em>merimnate</em>) about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God."),
      ("Luke 21:34", "Be careful, or your hearts will be weighed down with carousing, drunkenness and the anxieties (<em>merimna</em>) of life."),
      ("2 Corinthians 11:28", "Besides everything else, I face daily the pressure of my concern (<em>merimna</em>) for all the churches.")],
     [("G1515", "Eirēnē (Peace)"), ("G4335", "Proseuche (Prayer)"), ("G4102", "Pistis (Faith/Trust)")]),

    ("G3484", "Ναΐν", "Nain", "Proper noun", "Nain; Village of the Widow's Son",
     "Nain — the village in Galilee where Jesus raised a widow's only son from the dead, his compassion overflowing before any request was made.",
     "The Greek <em>Nain</em> (Hebrew: <em>na'im</em>, pleasant) was a village in Galilee, identified with modern Nein at the base of the Hill of Moreh. It appears only in Luke 7:11-17 — the account of Jesus raising a widow's only son. As the funeral procession came out of the city gate, Jesus 'saw her, his heart went out to her and he said, 'Don't cry.'' Then he touched the bier and commanded: 'Young man, I say to you, get up!' The crowd glorified God saying 'A great prophet has appeared among us' and 'God has come to help his people.'",
     "The Nain miracle stands out in the Gospels because Jesus raised the dead without being asked. No one petitioned him — the widow was weeping, not requesting. Jesus acted from pure compassion (<em>esplagchnisthē</em> — 'his heart went out to her') before any faith was expressed. This is the grace of God unasked: the initiative of divine mercy that arrives before the prayer forms. The crowd's response — 'God has come to help (<em>epeskepsato</em>) his people' — uses the language of the Benedictus (Luke 1:68), the word of God 'visiting' His people. In Nain, that visitation took the form of a village funeral interrupted by resurrection.",
     [("Luke 7:11", "Soon afterward, Jesus went to a town called <em>Nain</em>, and his disciples and a large crowd went along with him."),
      ("Luke 7:13", "When the Lord saw her, his heart went out to her and he said, 'Don't cry.'"),
      ("Luke 7:14", "Then he went up and touched the bier they were carrying him on, and the bearers stood still. He said, 'Young man, I say to you, get up!'"),
      ("Luke 7:16", "They were all filled with awe and praised God. 'A great prophet has appeared among us,' they said. 'God has come to help his people.'"),
      ("1 Kings 17:22", "The LORD heard Elijah's cry, and the boy's life returned to him, and he lived.")],
     [("G386", "Anastasis (Resurrection)"), ("G4697", "Splagchnizomai (Have Compassion)"), ("G5503", "Chēra (Widow)")]),

    ("G3656", "ὁμιλέω", "Homileō", "Verb", "To Talk With; To Converse; To Associate With",
     "To speak together or converse — used for the Emmaus disciples talking with the risen Jesus and for Paul's extended teaching conversations.",
     "The Greek <em>homileō</em> (from <em>homou</em>, together + <em>hileō</em>, to speak) means to converse or talk with someone — the word from which 'homily' derives. It appears in Luke 24:14-15, where the two Emmaus disciples were 'talking together (<em>hōmiloun</em>)' about the crucifixion and resurrection when Jesus himself joined them and 'went with them.' Acts 20:11 records Paul 'talking (<em>homilēsas</em>) until daylight' after the raising of Eutychus. Acts 24:26 notes that Felix 'sent for Paul and talked (<em>hōmilei</em>) with him' frequently.",
     "The <em>homileō</em> of Luke 24:14-15 is one of the most theologically rich details of the resurrection narratives. Two disciples, walking and conversing about the devastating events in Jerusalem, are joined by the risen Jesus — whom they do not recognize. Their <em>homileō</em> (conversation) about Jesus leads to an encounter with Jesus. He draws out their grief, opens the Scriptures (Luke 24:27), and only at the breaking of bread are their eyes opened. The pattern: conversation about Christ → encounter with Christ → Scripture opened → recognition. Every Christian homily, at its best, recreates this Emmaus road: the word spoken leads to the Word recognized.",
     [("Luke 24:14", "They were talking (<em>hōmiloun</em>) with each other about everything that had happened."),
      ("Luke 24:15", "As they talked and discussed these things with each other, Jesus himself came up and walked along with them."),
      ("Acts 20:11", "Then he went upstairs again and broke bread and ate. After talking (<em>homilēsas</em>) until daylight, he left."),
      ("Acts 24:26", "He was hoping that Paul would offer him a bribe, so he sent for him frequently and talked (<em>hōmilei</em>) with him."),
      ("Luke 24:27", "And beginning with Moses and all the Prophets, he explained to them what was said in all the Scriptures concerning himself.")],
     [("G3056", "Logos (Word)"), ("G2980", "Laleō (Speak)"), ("G1921", "Epiginōskō (Recognize/Know Fully)")]),

    ("G3865", "παραθεωρέω", "Paratheōreō", "Verb", "To Overlook; To Neglect; To Pass Over",
     "To overlook or neglect — used for the dangerous pastoral failure in Acts 6 when Hellenistic widows were being passed over in the daily food distribution.",
     "The Greek <em>paratheōreō</em> (from <em>para</em>, beside/past + <em>theōreō</em>, to look/observe) means to look past, overlook, or fail to notice — with the implication of neglect. It appears once in the NT: Acts 6:1, in the crisis that gave birth to the diaconate: 'the Hellenistic Jews among them complained against the Hebraic Jews because their widows were being overlooked (<em>paretheorounto</em>) in the daily distribution of food.' This neglect — likely unintentional but structurally embedded — prompted the apostles to appoint seven deacons.",
     "The <em>paratheōreō</em> of Acts 6:1 is the origin story of diaconal ministry. A structural oversight — Greek-speaking widows being overlooked in food distribution — threatened to fracture the young church along ethnic lines. The apostles' response was not to ignore it or moralize it away but to reorganize: appoint Spirit-filled, wise servants to ensure equitable care. This is the theology of administration as ministry: proper structure prevents <em>paratheōreō</em> from becoming injustice. The seven deacons (including Stephen and Philip) became key figures in the book of Acts — proving that practical service and prophetic witness belong together.",
     [("Acts 6:1", "In those days when the number of disciples was increasing, the Hellenistic Jews among them complained against the Hebraic Jews because their widows were being overlooked (<em>paretheorounto</em>) in the daily distribution of food."),
      ("Acts 6:3", "Brothers and sisters, choose seven men from among you who are known to be full of the Spirit and wisdom. We will turn this responsibility over to them."),
      ("Acts 6:5", "This proposal pleased the whole group. They chose Stephen, a man full of faith and of the Holy Spirit; also Philip, Procorus, Nicanor, Timon, Parmenas, and Nicolas."),
      ("James 1:27", "Religion that God our Father accepts as pure and faultless is this: to look after orphans and widows in their distress."),
      ("Galatians 3:28", "There is neither Jew nor Gentile, neither slave nor free, nor is there male and female, for you are all one in Christ Jesus.")],
     [("G5503", "Chēra (Widow)"), ("G1248", "Diakonia (Service/Ministry)"), ("G1344", "Dikaioō (Justify/Make Right)")]),

    ("G3935", "παρίημι", "Pariēmi", "Verb", "To Let Pass; To Relax; To Allow; To Neglect",
     "To let something pass by or drop — used for the drooping hands that need strengthening and for God's patient 'passing over' of former sins.",
     "The Greek <em>pariēmi</em> (from <em>para</em>, beside + <em>hiēmi</em>, to send/let go) means to let pass, to relax, or to drop. In Hebrews 12:12 it is used for 'drooping hands' (<em>tas pareimenas cheiras</em>) that need strengthening — a call to spiritual renewal amid suffering. In Luke 11:42 it appears for 'neglecting' justice and the love of God. The related concept of God's <em>paresis</em> (passing over/overlooking) in Romans 3:25 describes how God 'left the sins committed beforehand unpunished' in his divine forbearance before Christ.",
     "The <em>pariēmi</em> of Hebrews 12:12 draws on Isaiah 35:3 ('Strengthen the feeble hands, steady the knees that give way') and applies it to Christian perseverance under discipline. The drooping hands and weak knees are not sinful — they are exhausted. Hebrews' response is not rebuke but encouragement: God's discipline is evidence of sonship (Hebrews 12:7-8), and the path through it leads to 'the peaceful fruit of righteousness' (12:11). Hands that <em>pariēmi</em> (droop and let go) need to be strengthened, not condemned — a pastoral theology of compassionate perseverance.",
     [("Hebrews 12:12", "Therefore, strengthen your feeble arms and weak knees (<em>pareimenas cheiras kai paralelymena gonata</em>)."),
      ("Luke 11:42", "Woe to you Pharisees, because you give God a tenth of your mint, rue and all other kinds of garden herbs, but you <em>neglect</em> justice and the love of God."),
      ("Isaiah 35:3", "Strengthen the feeble hands, steady the knees that give way."),
      ("Hebrews 12:7", "Endure hardship as discipline; God is treating you as his children. For what children are not disciplined by their father?"),
      ("Hebrews 12:11", "No discipline seems pleasant at the time, but painful. Later on, however, it produces a harvest of righteousness and peace for those who have been trained by it.")],
     [("G1411", "Dynamis (Power/Strength)"), ("G3809", "Paideia (Discipline/Training)"), ("G1515", "Eirēnē (Peace)")]),

    ("G4017", "περιβλέπω", "Periblepō", "Verb", "To Look Around; To Survey; To Gaze About",
     "To look all around — used specifically for Jesus' penetrating, searching gaze in the Synoptic Gospels at moments of challenge, healing, and holy anger.",
     "The Greek <em>periblepō</em> (from <em>peri</em>, around + <em>blepō</em>, to see) means to look around in all directions — a sweeping, comprehensive gaze. It is almost exclusively a Markan word in the NT, used seven times in Mark. Jesus <em>periblepō</em>s in the synagogue with anger and grief at the hardness of hearts (Mark 3:5), looks around at his disciples to identify his true family (Mark 3:34), surveys those seated around him after the healing of the woman with the hemorrhage (Mark 5:32), and gazes at the Temple before leaving (Mark 11:11). It conveys authority, comprehension, and moral intensity.",
     "Mark's frequent use of <em>periblepō</em> is part of his vivid, action-centered portrait of Jesus. The searching gaze — eyes sweeping the room — communicates sovereign awareness. No one is outside Jesus' field of vision; no heart is hidden from this gaze. In Mark 3:5, the <em>periblepō</em> is combined with emotion: 'He looked around at them in anger, deeply distressed at their stubborn hearts.' This is holy anger — not impulsive rage but grief-laden indignation at spiritual hardness. The One whose gaze encompasses all creation is moved to anger and sorrow by those who refuse mercy.",
     [("Mark 3:5", "He looked around (<em>periblepsamenos</em>) at them in anger and, deeply distressed at their stubborn hearts, said to the man, 'Stretch out your hand.'"),
      ("Mark 3:34", "Then he looked at (<em>periblepsamenos</em>) those seated in a circle around him and said, 'Here are my mother and my brothers!'"),
      ("Mark 5:32", "But Jesus kept looking around (<em>perieblepeto</em>) to see who had done it."),
      ("Mark 11:11", "Jesus entered Jerusalem and went into the temple courts. He looked around (<em>periblepsamenos</em>) at everything, but since it was already late, he went out to Bethany with the Twelve."),
      ("Hebrews 4:13", "Nothing in all creation is hidden from God's sight. Everything is uncovered and laid bare before the eyes of him to whom we must give account.")],
     [("G991", "Blepō (To See)"), ("G3708", "Horaō (To See/Perceive)"), ("G3709", "Orgē (Wrath/Anger)")]),

    ("G4135", "πληροφορέω", "Plērophoreō", "Verb", "To Fully Assure; To Fully Carry Out; To Fulfill Completely",
     "To bring to full measure — used for the full assurance of faith and for completely fulfilling the ministry of preaching the gospel.",
     "The Greek <em>plērophoreō</em> (from <em>plēros</em>, full + <em>phoreō</em>, to carry/bear) means to carry to completion, to fill fully, to bring full assurance. Paul uses it in Romans 4:21 for Abraham who 'was fully persuaded (<em>plērophorētheis</em>) that God had power to do what he had promised.' In Romans 14:5 it is 'fully convinced (<em>plērophoreistho</em>) in their own mind.' In 2 Timothy 4:5 Paul charges Timothy to 'fulfill your ministry (<em>plērophorēson</em>).' In Colossians 4:12 Epaphras prays for the Colossians to 'stand firm in all the will of God, fully assured (<em>peplērophorēmenoi</em>).'",
     "The theological richness of <em>plērophoreō</em> lies in its uniting of objective completeness and subjective assurance. Abraham's <em>plērophoreō</em> was not mere optimism but full persuasion grounded in God's character — 'he who had promised is faithful' (Hebrews 11:11). The same word for 'fully convinced' and 'fulfill the ministry' reveals Paul's theology of ministry: to preach the gospel to its full extent (<em>plērophoreō</em> the word) is itself an expression of the conviction that God will carry His promises to completion. The apostle who is <em>plērophorētheis</em> about God's faithfulness becomes the instrument through whom God's word is <em>plērophoreō</em>d in the world.",
     [("Romans 4:21", "being fully persuaded (<em>plērophorētheis</em>) that God had power to do what he had promised."),
      ("2 Timothy 4:5", "But you, keep your head in all situations, endure hardship, do the work of an evangelist, discharge all the duties of your ministry (<em>plērophorēson</em>)."),
      ("Colossians 4:12", "He is always wrestling in prayer for you, that you may stand firm in all the will of God, mature and fully assured (<em>peplērophorēmenoi</em>)."),
      ("Romans 14:5", "One person considers one day more sacred than another; another considers every day alike. Each of them should be fully convinced (<em>plērophoreistho</em>) in their own mind."),
      ("Hebrews 11:11", "And by faith even Sarah, who was past childbearing age, was enabled to bear children because she considered him faithful who had made the promise.")],
     [("G4137", "Plēroō (To Fill/Fulfill)"), ("G4102", "Pistis (Faith)"), ("G1680", "Elpis (Hope)")]),

    ("G4234", "πρᾶξις", "Praxis", "Noun, feminine", "Deed; Practice; Action; Function",
     "A deed, action, or regular practice — used for evil deeds of the body that must be put to death and for the 'Acts' of the apostles.",
     "The Greek <em>praxis</em> (from <em>prassō</em>, to do/practice) means an action, deed, or ongoing practice. It is a significant NT word: Romans 8:13 calls believers to 'put to death the <em>praxeis</em> of the body by the Spirit'; Colossians 3:9 commands putting off the 'old self with its <em>praxeis</em>'; Luke 23:51 describes Joseph of Arimathea as one 'who had not consented to their decision and action (<em>praxis</em>)'; and in Acts 19:18 new converts 'openly confessed what they had done (<em>praxeis</em>).' The word 'Acts' (Greek: <em>Praxeis</em>) in the title of Luke's second volume is the 'Deeds/Actions of the Apostles.'",
     "The theology of <em>praxis</em> in Romans 8:13 is the heart of sanctification: 'if by the Spirit you put to death the <em>praxeis</em> of the body, you will live.' The body's habitual practices — the patterns of flesh — must be actively mortified, not merely regretted. Yet this is not human self-improvement: it is specifically 'by the Spirit' that the old <em>praxeis</em> are put to death. Sanctification is cooperative — the human will and the divine Spirit working together to replace old patterns with new ones. The book of <em>Praxeis</em> (Acts) shows what this looks like at scale: Spirit-empowered people enacting the ongoing deed of God in history.",
     [("Romans 8:13", "For if you live according to the flesh, you will die; but if by the Spirit you put to death the misdeeds (<em>praxeis</em>) of the body, you will live."),
      ("Colossians 3:9", "Do not lie to each other, since you have taken off your old self with its practices (<em>praxesin</em>)."),
      ("Acts 19:18", "Many of those who believed now came and openly confessed what they had done (<em>praxeis</em>)."),
      ("Luke 23:51", "Joseph of Arimathea had not consented to their decision and deed (<em>praxis</em>). He came from the Judean town of Arimathea."),
      ("Hebrews 4:13", "Nothing in all creation is hidden from God's sight. Everything is uncovered and laid bare before the eyes of him to whom we must give account.")],
     [("G4151", "Pneuma (Spirit)"), ("G4561", "Sarx (Flesh)"), ("G2041", "Ergon (Work/Deed)")]),

    ("G4569", "Σαῦλος", "Saulos", "Proper noun, masculine", "Saul (Paul's Hebrew Name); Asked of God",
     "The Hebrew name of the Apostle Paul — Saul of Tarsus, persecutor turned apostle, whose encounter with the risen Christ on the Damascus road transformed world history.",
     "The Greek <em>Saulos</em> is the Greek form of the Hebrew <em>Shaul</em> (Saul), meaning 'asked for' or 'prayed for.' Paul bore two names: <em>Saulos</em> (his Jewish/Hebrew name, used in Acts 7:58-13:9) and <em>Paulos</em> (his Roman name, used from Acts 13:9 onward). The transition to <em>Paulos</em> in Acts 13:9 corresponds to his explicit Gentile mission. Saulos appears in Acts 7:58 (consenting to Stephen's stoning), Acts 9:1-19 (Damascus road encounter), Acts 22 and 26 (Paul's own retelling of his conversion), and Philippians 3:5 ('a Hebrew of Hebrews... a Pharisee').",
     "The name <em>Saulos</em> carries the weight of Israel's first king — Saul of Benjamin — and Paul was himself a Benjaminite (Romans 11:1; Philippians 3:5). Israel's Saul started as God's anointed and became a persecutor of David; Paul the Pharisee started as a persecutor of Christ and became his greatest apostle. The irony is not incidental: Paul himself draws on this in Philippians 3 and 1 Timothy 1:12-16 — 'I was a blasphemer and a persecutor... but I was shown mercy.' The transformation of <em>Saulos</em> into <em>Paulos</em> is the testimony of grace that could stop anyone: if God could turn the chief of persecutors into the apostle to the Gentiles, grace has no limits.",
     [("Acts 9:4", "He fell to the ground and heard a voice say to him, '<em>Saul</em>, <em>Saul</em>, why do you persecute me?'"),
      ("Acts 7:58", "and dragged him out of the city and began to stone him. Meanwhile, the witnesses laid their coats at the feet of a young man named <em>Saul</em>."),
      ("Acts 13:9", "Then <em>Saul</em>, who was also called Paul, filled with the Holy Spirit, looked straight at Elymas."),
      ("1 Timothy 1:15", "Here is a trustworthy saying that deserves full acceptance: Christ Jesus came into the world to save sinners — of whom I am the worst."),
      ("Philippians 3:5", "circumcised on the eighth day, of the people of Israel, of the tribe of Benjamin, a Hebrew of Hebrews; in regard to the law, a Pharisee.")],
     [("G3972", "Paulos (Paul)"), ("G1577", "Ekklēsia (Church)"), ("G5485", "Charis (Grace)")]),

    ("G4809", "συκομορέα", "Sykomorea", "Noun, feminine", "Sycamore-Fig Tree; Mulberry Fig",
     "The sycamore-fig tree that Zacchaeus climbed to see Jesus — a tree associated with humility, seeking, and unexpected encounter with grace.",
     "The Greek <em>sykomorea</em> (sycamore-fig, <em>Ficus sycomorus</em>) is a large, low-branching tree common in the Jordan Valley and Jericho plain. It appears once in the NT: Luke 19:4, where Zacchaeus 'ran ahead and climbed a sycamore-fig tree (<em>sykomorean</em>) to see him.' The tree's low, spreading branches made it ideal for climbing — and Zacchaeus, 'short in stature' (Luke 19:3) and a wealthy tax collector, used it to overcome both his physical limitation and his social exclusion from the crowd.",
     "The <em>sykomorea</em> of Luke 19 is the tree of seeking. Zacchaeus climbed it because he was a small man in a crowd that had no reason to let him through — he was doubly excluded (short and a sinner by reputation). Yet Jesus looked up, saw him, and called him by name: 'Zacchaeus, come down immediately. I must stay at your house today.' The crowd's grumbling ('He has gone to be the guest of a sinner') is the anti-gospel. Jesus' summary captures the theology of the entire episode: 'For the Son of Man came to seek and to save the lost' (Luke 19:10). The tree Zacchaeus used to seek Jesus became the location where Jesus found him.",
     [("Luke 19:4", "So he ran ahead and climbed a sycamore-fig tree (<em>sykomorean</em>) to see him, since Jesus was coming that way."),
      ("Luke 19:5", "When Jesus reached the spot, he looked up and said to him, 'Zacchaeus, come down immediately. I must stay at your house today.'"),
      ("Luke 19:8", "But Zacchaeus stood up and said to the Lord, 'Look, Lord! Here and now I give half of my possessions to the poor.'"),
      ("Luke 19:10", "For the Son of Man came to seek and to save the lost."),
      ("Luke 18:27", "Jesus replied, 'What is impossible with man is possible with God.'")],
     [("G5033", "Tachista (Most Quickly)"), ("G5485", "Charis (Grace)"), ("G684", "Apōleia (Loss/Destruction)")]),

    ("G5033", "τάχιστα", "Tachista", "Adverb (superlative)", "As Quickly as Possible; Most Swiftly",
     "As quickly as possible — the superlative of swiftness, used for urgent sailing decisions and the urgency of departure.",
     "The Greek <em>tachista</em> is the superlative adverb from <em>tachus</em> (quick/swift), meaning 'as quickly as possible' or 'most swiftly.' It appears in Acts 17:15, where Paul's companions escort him to Athens and 'received instructions for Silas and Timothy to join him as soon as possible (<em>tachista</em>).' The word captures urgency — the apostolic mission moves at pace because the window for proclamation is always closing. In Acts 17:14, Paul was sent away from Berea quickly because of the agitators from Thessalonica, and the <em>tachista</em> instructions were given immediately.",
     "The <em>tachista</em> of Acts 17:15 reflects the tempo of Pauline mission. Paul's movements — forced by persecution, guided by the Spirit, seized by opportunity — required swift response from his team. The gospel moved quickly because Paul's enemies moved quickly. Yet the urgency is not frantic; Paul arrives in Athens and, while waiting for his companions, begins reasoning daily in the agora. <em>Tachista</em> travel becomes <em>logos</em> time: every city is an opportunity for proclamation. The speed of the mission reflects the theology of redemption — time is short, the harvest is large, the workers are few (Luke 10:2).",
     [("Acts 17:15", "Those who escorted Paul brought him to Athens and then left with instructions for Silas and Timothy to join him as soon as possible (<em>tachista</em>)."),
      ("Acts 17:14", "The believers immediately sent Paul to the coast, but Silas and Timothy stayed at Berea."),
      ("Acts 17:16", "While Paul was waiting for them in Athens, he was greatly distressed to see that the city was full of idols."),
      ("Luke 10:2", "He told them, 'The harvest is plentiful, but the workers are few. Ask the Lord of the harvest, therefore, to send out workers into his harvest field.'"),
      ("Revelation 22:20", "He who testifies to these things says, 'Yes, I am coming soon.' Amen. Come, Lord Jesus.")],
     [("G5034", "Tachos (Speed)"), ("G652", "Apostolos (Apostle)"), ("G2782", "Kērygma (Proclamation)")]),

    ("G5110", "τόκος", "Tokos", "Noun, masculine", "Interest; Usury; Birth; Offspring",
     "Interest on money — used by Jesus in the Parable of the Talents for the returns that faithful stewardship of entrusted resources should produce.",
     "The Greek <em>tokos</em> (from <em>tiktō</em>, to give birth) means 'offspring' in the literal sense but is used commercially for 'interest' — the offspring of invested money. It appears in Matthew 25:27 and Luke 19:23 in the Parable of the Talents/Minas: 'You should have put my money on deposit with the bankers, so that when I returned I would have received it back with interest (<em>tokō</em>).' The master's rebuke to the unfaithful servant uses the minimal standard of a banker's interest as the baseline expectation for stewardship.",
     "The <em>tokos</em> in the Parable of the Talents is not a financial lesson but a stewardship theology. The master expected something — at minimum, the baseline return of a banker's interest — from every servant entrusted with his goods. The unfaithful servant buried his talent 'out of fear' and returned it unchanged. This is not humility — it is failed stewardship dressed as caution. The <em>tokos</em> standard is minimal: even a banker provides a return. God's expectation of those entrusted with the gospel, gifts, and opportunities of the kingdom is that they will be invested, risked, and multiplied — not preserved in safety.",
     [("Matthew 25:27", "Well then, you should have put my money on deposit with the bankers, so that when I returned I would have received it back with interest (<em>tokō</em>)."),
      ("Luke 19:23", "Why then didn't you put my money on deposit, so that when I came back, I could have collected it with interest (<em>tokō</em>)?"),
      ("Matthew 25:24", "Then the man who had received one bag of gold came. 'Master,' he said, 'I knew that you are a hard man, harvesting where you have not sown.'"),
      ("Matthew 25:29", "For whoever has will be given more, and they will have an abundance. Whoever does not have, even what they have will be taken from them."),
      ("1 Peter 4:10", "Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace in its various forms.")],
     [("G5007", "Talanton (Talent/Weight)"), ("G3623", "Oikonomos (Steward/Manager)"), ("G2041", "Ergon (Work/Deed)")]),
]

def write_page(strongs_id, script, translit, pos, gloss, short_def, full_def, theology, verses, related):
    lang = strongs_id[0]
    html = make_page(strongs_id, lang, script, translit, pos, gloss, short_def, full_def, theology, verses, related)
    path = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Created: {strongs_id}.html")

count = 0
print("=== Hebrew Words ===")
for entry in hebrew_words:
    num, script, translit, pos, gloss, short_def, full_def, theology, verses, related = entry
    strongs_id = f"H{num}"
    write_page(strongs_id, script, translit, pos, gloss, short_def, full_def, theology, verses, related)
    count += 1

print(f"\n=== Greek Words ===")
for entry in greek_words:
    num, script, translit, pos, gloss, short_def, full_def, theology, verses, related = entry
    strongs_id = f"G{num}"
    write_page(strongs_id, script, translit, pos, gloss, short_def, full_def, theology, verses, related)
    count += 1

print(f"\nTotal pages created: {count}")
