#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch Mar 25 2026"""
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
    blb_lang = "g" if lang == "G" else "h"
    bhub_lang = "greek" if lang == "G" else "hebrew"
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
    direction = 'direction:rtl; ' if lang == 'H' else ''
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
            <div class="original-word" style="{direction}font-size:2.8rem;">{script}</div>
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
                <a href="https://www.blueletterbible.org/lexicon/{blb_lang}{num}/kjv/{'wlc' if lang=='H' else 'tr'}/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/{bhub_lang}/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>
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

# ===== HEBREW ENTRIES (24 total) =====
hebrew_words = [
    # (num, script, translit, pos, gloss, definition, theology, verses, related)
    (711, "אַרְגְּוָן", "Argewan", "Noun, masculine", "Purple; Crimson Cloth",
     "Purple or crimson-colored fabric or thread — the royal and priestly color of the ancient world. <em>Argewan</em> (also spelled <em>argaman</em>) refers specifically to the deep reddish-purple dye extracted from Mediterranean shellfish, prized above nearly all other materials in the ancient Near East.",
     "Purple (<em>argewan</em>) in Scripture is the color of royalty, priesthood, and wealth. The Tabernacle curtains were woven of blue, purple, and crimson (Exodus 26:1). The High Priest's garments included purple thread. Proverbs 31:22 describes the virtuous woman clothing herself in purple. In the New Testament, the soldiers mockingly robed Jesus in purple (Mark 15:17) — unknowingly dressing the true King in His rightful color. The woman of Revelation 17 wears purple as a sign of corrupt power. Purple dye was so expensive that only kings and the wealthiest merchants could afford it — making Lydia, the seller of purple (Acts 16:14), a woman of significant means whom God used as the first European convert.",
     [("Exodus 26:1", "Make the tabernacle with ten curtains of finely twisted linen and blue, <em>purple</em> and scarlet yarn, with cherubim woven into them by a skilled worker."),
      ("Proverbs 31:22", "She makes coverings for her bed; she is clothed in fine linen and <em>purple</em>."),
      ("Mark 15:17", "They put a <em>purple</em> robe on him, then twisted together a crown of thorns and set it on him."),
      ("Acts 16:14", "One of those listening was a woman from the city of Thyatira named Lydia, a dealer in <em>purple</em> cloth. She was a worshiper of God."),
      ("Judges 8:26", "The weight of the gold rings he asked for came to seventeen hundred shekels, not counting the ornaments, the pendants and the <em>purple</em> garments worn by the kings of Midian.")],
     [("H8438", "Towla (Crimson/Scarlet)"), ("H8504", "Tekheleth (Blue)"), ("H4428", "Melek (King)")]),

    (750, "אָרֵךְ", "Arek", "Adjective", "Long; Patient; Slow to Anger",
     "Long, extended, or patient — particularly used in the phrase <em>erek apayim</em> (long of nostrils/face), meaning slow to anger, patient, or long-suffering. This adjective comes from the root <em>arak</em> (H748) meaning to be long or to lengthen.",
     "The phrase <em>erek apayim</em> — literally 'long of nostrils' (since the nose flares in anger) — is one of the most theologically rich character descriptions in the entire Old Testament. It is first used of God Himself in Exodus 34:6-7, the great divine self-disclosure at Sinai: 'The LORD, the LORD, compassionate and gracious God, <em>slow to anger</em>, abounding in love and faithfulness.' This self-description becomes the cornerstone of biblical theology of God's character — repeated or alluded to dozens of times (Numbers 14:18; Nehemiah 9:17; Psalm 86:15; 103:8; 145:8; Joel 2:13; Jonah 4:2; Nahum 1:3). That God is <em>erek apayim</em> is simultaneously a source of comfort (He does not punish immediately) and of warning (He does not ignore sin forever). Peter connects this patience directly to salvation: God's patience means more time for repentance (2 Peter 3:9).",
     [("Exodus 34:6", "And he passed in front of Moses, proclaiming, 'The LORD, the LORD, the compassionate and gracious God, <em>slow to anger</em>, abounding in love and faithfulness.'"),
      ("Psalm 103:8", "The LORD is compassionate and gracious, <em>slow to anger</em>, abounding in love."),
      ("Proverbs 14:29", "Whoever is <em>patient</em> has great understanding, but one who is quick-tempered displays folly."),
      ("Nahum 1:3", "The LORD is <em>slow to anger</em> but great in power; the LORD will not leave the guilty unpunished."),
      ("2 Peter 3:9", "The Lord is not slow in keeping his promise, as some understand slowness. Instead he is <em>patient</em> with you, not wanting anyone to perish.")],
     [("H748", "Arak (To Lengthen)"), ("H2534", "Chemah (Wrath)"), ("H2617", "Chesed (Lovingkindness)")]),

    (898, "בָּגַד", "Bagad", "Verb", "To Betray; To Act Treacherously; To Be Faithless",
     "To deal treacherously, act faithlessly, or betray — used of covenant violation, marital unfaithfulness, and betrayal of trust. <em>Bagad</em> describes the breach of a relationship that was built on loyalty and trust.",
     "<em>Bagad</em> appears over fifty times in the Old Testament, consistently describing the violation of covenant fidelity. It is used of Israel's unfaithfulness to God (Isaiah 1:2 — 'I reared children and brought them up, but they have rebelled against me'), of husbands who deal treacherously with the wives of their youth (Malachi 2:14-16 — the most concentrated use of <em>bagad</em> in the Bible), and of nations betraying one another. Malachi 2 uses <em>bagad</em> five times in three verses, underscoring how deeply God regards marital and covenantal faithfulness. The New Testament counterpart is found in the betrayal of Jesus by Judas — the ultimate <em>bagad</em> — which paradoxically became the means of covenant renewal for all humanity.",
     [("Malachi 2:14", "You ask, 'Why?' It is because the LORD is the witness between you and the wife of your youth. You have been <em>unfaithful</em> to her, though she is your partner, the wife of your marriage covenant."),
      ("Isaiah 1:2", "Hear me, you heavens! Listen, earth! For the LORD has spoken: 'I reared children and brought them up, but they have <em>rebelled</em> against me.'"),
      ("Psalm 73:15", "If I had spoken out like that, I would have <em>betrayed</em> your children."),
      ("Lamentations 1:2", "Bitterly she weeps at night, tears are on her cheeks. Among all her lovers there is no one to comfort her. All her friends have <em>betrayed</em> her."),
      ("Proverbs 11:3", "The integrity of the upright guides them, but the unfaithful are destroyed by their <em>duplicity</em>.")],
     [("H539", "Aman (Faithful/Trust)"), ("H1285", "Berith (Covenant)"), ("H2617", "Chesed (Lovingkindness)")]),

    (1347, "גָּאוֹן", "Gaon", "Noun, masculine", "Majesty; Excellence; Arrogance",
     "Pride, excellence, majesty, or arrogance depending on context. The Hebrew <em>gaon</em> derives from the root <em>ga'ah</em> (H1342), meaning to rise up or be exalted. It carries a dual meaning: the legitimate majesty and excellency of God, and the sinful pride of humans who exalt themselves against Him.",
     "In Scripture, <em>gaon</em> captures a tension at the heart of theology: majesty belongs to God alone (Psalm 68:34), yet humanity tends to seize that glory for itself. Isaiah warns repeatedly against the pride of nations and individuals (Isaiah 13:11; 16:6). When <em>gaon</em> describes God, it speaks of His incomparable exaltation and splendor. The same word used of human pride becomes a warning against the creature usurping the Creator's glory. Amos uses <em>gaon</em> in a striking oath: 'The LORD has sworn by the Pride of Jacob' (Amos 8:7) — a reference to God Himself, who is Israel's true glory.",
     [("Psalm 68:34", "Ascribe power to God, whose <em>majesty</em> is over Israel, whose power is in the heavens."),
      ("Isaiah 13:11", "I will put an end to the <em>arrogance</em> of the haughty and lay low the pride of the ruthless."),
      ("Amos 8:7", "The LORD has sworn by the <em>Pride</em> of Jacob: I will never forget anything they have done."),
      ("Ezekiel 24:21", "Say to the house of Israel, 'This is what the Sovereign LORD says: I am about to desecrate my sanctuary — the stronghold in which you take <em>pride</em>."),
      ("Proverbs 16:18", "<em>Pride</em> goes before destruction, a haughty spirit before a fall.")],
     [("H1342", "Ga'ah (To Rise Up)"), ("H1346", "Ga'avah (Pride)"), ("H3519", "Kavod (Glory)")]),

    (2860, "חָתָן", "Chathan", "Noun, masculine", "Bridegroom; Son-in-Law",
     "A bridegroom or son-in-law; one who has entered into the covenant of marriage. <em>Chathan</em> is related to the concept of becoming family through covenant union, and is used throughout the OT for the joyful figure of the newly wed husband.",
     "The image of the bridegroom permeates biblical theology from beginning to end. God describes His relationship to Israel in marital terms (Isaiah 62:5; Hosea 2:19-20). The Psalmist compares the sun to a <em>chathan</em> coming out of his chamber with joy (Psalm 19:5). This imagery reaches its climax in the New Testament where Christ is revealed as the ultimate Bridegroom (Matthew 25:1-13; Revelation 19:7-9) and the Church as His bride. Understanding <em>chathan</em> helps unlock the covenant love that unites the entire biblical narrative.",
     [("Isaiah 62:5", "As a young man marries a young woman, so will your Builder marry you; as a <em>bridegroom</em> rejoices over his bride, so will your God rejoice over you."),
      ("Psalm 19:5", "It is like a <em>bridegroom</em> coming out of his chamber, like a champion rejoicing to run his course."),
      ("Joel 2:16", "Gather the people, consecrate the assembly; bring together the elders, gather the children. Let the <em>bridegroom</em> leave his room and the bride her chamber."),
      ("Jeremiah 7:34", "I will bring an end to the sounds of joy and gladness and to the voices of <em>bride and bridegroom</em> in the towns of Judah."),
      ("Song of Songs 3:11", "Come out, you daughters of Zion, and look at King Solomon wearing the crown with which his mother crowned him on his wedding day, the day his heart rejoiced.")],
     [("H3618", "Kallah (Bride)"), ("H157", "Ahav (Love)"), ("H1285", "Berith (Covenant)")]),

    (3391, "יֶרַח", "Yerach", "Noun, masculine", "Month; Moon",
     "A month (the lunar period of roughly 29-30 days); also the moon itself. <em>Yerach</em> emphasizes the full lunar cycle and appears alongside <em>chodesh</em> (H2320, the new moon/month) as a near-synonym, though <em>yerach</em> more specifically emphasizes the completed lunar cycle.",
     "Israel's sacred calendar was divinely structured around the moon's cycles (Genesis 1:14 — lights for signs, seasons, days, years). New Moon celebrations were significant worship occasions (Numbers 10:10; 28:11-15). The Psalmist declares God made the moon for appointed seasons (Psalm 104:19). The Passover, Pentecost, and Feast of Tabernacles were all governed by lunar dating. In this way <em>yerach</em> connects astronomical order to the covenant community's rhythm of worship and life.",
     [("Genesis 7:11", "In the six hundredth year of Noah's life, on the seventeenth day of the second <em>month</em> — on that day all the springs of the great deep burst forth."),
      ("1 Kings 6:37", "The foundation of the temple of the LORD was laid in the fourth year, in the <em>month</em> of Ziv."),
      ("Psalm 104:19", "He made the <em>moon</em> to mark the seasons, and the sun knows when to go down."),
      ("Zechariah 11:8", "In one <em>month</em> I got rid of the three shepherds. The flock detested me, and I grew weary of them."),
      ("Revelation 22:2", "On each side of the river stood the tree of life, bearing twelve crops of fruit, yielding its fruit every <em>month</em>.")],
     [("H2320", "Chodesh (New Moon/Month)"), ("H8141", "Shanah (Year)"), ("H4150", "Moed (Appointed Time)")]),

    (4180, "מוֹרָשׁ", "Morash", "Noun, masculine", "Possession; Inheritance; Dispossession",
     "A possession, inheritance, or something seized by conquest — that which is held as one's own territory or heritage. <em>Morash</em> derives from the root <em>yarash</em> (H3423) meaning to possess, inherit, or dispossess.",
     "The concept of <em>morash</em> — inheritance and possession — runs through the entire Mosaic covenant structure. The Promised Land itself was God's gift to Israel as their <em>morash</em>, a possession tied to covenant faithfulness. Obadiah 17 uses <em>morash</em> eschatologically: 'The house of Jacob will possess its <em>inheritance</em>' — pointing to the ultimate restoration. In Micah 1:15, Moresheth-Gath (the prophet's hometown) plays on this word: 'I will bring a conqueror against you who live in Mareshah.' The theology of <em>morash</em> ultimately points to the new creation — the meek shall inherit the earth (Matthew 5:5).",
     [("Obadiah 17", "But on Mount Zion will be deliverance; it will be holy, and Jacob will <em>possess his inheritance</em>."),
      ("Isaiah 14:23", "I will turn her into a place for owls and into swampland; I will sweep her with the broom of destruction, declares the LORD Almighty."),
      ("Numbers 24:18", "Edom will be conquered; Seir, his enemy, will be conquered, but Israel will grow strong."),
      ("Micah 1:15", "I will bring a conqueror against you who live in Mareshah. The nobles of Israel will flee to Adullam."),
      ("Matthew 5:5", "Blessed are the meek, for they will <em>inherit</em> the earth.")],
     [("H3423", "Yarash (To Inherit/Possess)"), ("H5159", "Nachalah (Inheritance)"), ("H776", "Eretz (Land/Earth)")]),

    (4539, "מָסָךְ", "Masak", "Noun, masculine", "Covering; Screen; Curtain",
     "A covering, screen, or curtain — specifically used of the elaborate screens and veils of the Tabernacle and Temple that separated the holy zones. <em>Masak</em> derives from <em>sakak</em> (H5526) meaning to cover or shelter.",
     "The <em>masak</em> in the Tabernacle theology is deeply significant. Three main curtain-screens are mentioned: the screen at the Tabernacle entrance, the veil before the Holy Place, and the inner veil before the Most Holy Place. These were not mere architectural features — they were theological statements about the holiness of God and the separation between a holy God and sinful humanity. The tearing of the Temple veil (a <em>masak</em>) at the crucifixion of Christ (Matthew 27:51) was the most dramatic theological event in the history of the Tabernacle/Temple system: the barrier between God and humanity was removed by the atoning death of the Son.",
     [("Exodus 26:36", "For the entrance to the tent make a <em>screen</em> of blue, purple and scarlet yarn and finely twisted linen — the work of an embroiderer."),
      ("Exodus 40:5", "Place the gold altar of incense in front of the ark of the covenant law and put the <em>curtain</em> at the entrance to the tabernacle."),
      ("Numbers 3:31", "They were responsible for the care of the ark, the table, the lampstand, the altars, the articles of the sanctuary used in ministering, the <em>curtain</em>, and everything related to their use."),
      ("Matthew 27:51", "At that moment the curtain of the temple was torn in two from top to bottom. The earth shook, the rocks split."),
      ("Hebrews 10:20", "By a new and living way opened for us through the curtain, that is, his body.")],
     [("H6532", "Poreketh (Veil/Inner Curtain)"), ("H168", "Ohel (Tent)"), ("H6944", "Qodesh (Holiness)")]),

    (5110, "נוּד", "Nud", "Verb", "To Wander; To Nod; To Show Sympathy",
     "To wander, move back and forth, or shake the head — and by extension, to show grief or sympathy by the nodding motion of mourning. <em>Nud</em> carries both the physical movement of wandering or shaking and the emotional expression of communal sorrow.",
     "<em>Nud</em> appears in Jeremiah's lament over Jerusalem (Jeremiah 16:5; 22:10) and in Job's description of his comforters who came to sympathize (<em>nud</em>). Psalm 69:20 — understood messianically — captures the isolation of the Suffering Servant: 'I looked for sympathy (<em>nud</em>), but there was none.' Isaiah 51:19 speaks of destruction and famine: 'who can comfort you?' The word bridges physical wandering (Cain's curse: 'a restless wanderer') and social sympathy. When Jesus wept at Lazarus's tomb, He embodied the deepest <em>nud</em> — God Himself entering into human grief.",
     [("Job 2:11", "When Job's three friends heard about all the troubles that had come upon him, they set out from their homes and met together by agreement to go and <em>sympathize</em> with him and comfort him."),
      ("Psalm 69:20", "Scorn has broken my heart and has left me helpless; I looked for <em>sympathy</em>, but there was none, for comforters, but I found none."),
      ("Jeremiah 22:10", "Do not weep for the dead king or <em>mourn</em> his loss; rather, weep bitterly for him who is exiled."),
      ("Nahum 3:7", "All who see you will flee from you and say, 'Nineveh is in ruins — who will <em>mourn</em> for her?'"),
      ("John 11:35", "Jesus wept.")],
     [("H5095", "Nahal (To Guide/Lead)"), ("H5162", "Nacham (To Comfort)"), ("H56", "Abal (To Mourn)")]),

    (5164, "נֹחַם", "Nocham", "Noun, masculine", "Repentance; Consolation; Regret",
     "Repentance, relenting, or consolation — the noun form of <em>nacham</em> (H5162). <em>Nocham</em> describes the deep inner change that comes with genuine sorrow — whether God's relenting from judgment or human turning from sin.",
     "<em>Nocham</em> appears rarely but powerfully. In Hosea 13:14, God declares: 'Compassion is hidden from my eyes' — the absence of <em>nocham</em> signaling the finality of judgment against unrepentant Israel. The verb root <em>nacham</em> however drives the entire theology of divine relenting: God relents when people repent (Jeremiah 18:7-10; Jonah 3:10). The tension in Exodus 32 — where God says He 'relented' from destroying Israel after Moses' intercession — shows that God's <em>nocham</em> is not capricious but responds to genuine intercession and repentance. This becomes the basis for all prophetic intercession.",
     [("Hosea 13:14", "I will deliver this people from the power of the grave; I will redeem them from death. Where, O death, are your plagues? Where, O grave, is your destruction? I will have no <em>compassion</em>."),
      ("Job 6:10", "Then I would still have this <em>consolation</em> — my joy in unrelenting pain — that I had not denied the words of the Holy One."),
      ("Ezekiel 5:13", "Then my anger will cease and my wrath against them will subside, and I will be avenged. And when I have spent my wrath upon them, they will know that I the LORD have spoken in my zeal."),
      ("Jonah 3:10", "When God saw what they did and how they turned from their evil ways, he relented and did not bring on them the destruction he had threatened."),
      ("Jeremiah 18:8", "And if that nation I warned repents of its evil, then I will relent and not inflict on it the disaster I had planned.")],
     [("H5162", "Nacham (To Comfort/Repent)"), ("H8666", "Teshuvah (Return/Repentance)"), ("H2617", "Chesed (Lovingkindness)")]),

    (5391, "נָשַׁךְ", "Nashak", "Verb", "To Bite; To Lend at Interest",
     "To bite — as a serpent bites — and metaphorically, to charge or exact interest on loans. The connection between biting and usury reflects the ancient view that excessive interest 'bites' or devours the borrower.",
     "The dual meaning of <em>nashak</em> illuminates both the serpent's role in Eden and the prophetic condemnation of economic exploitation. The Torah explicitly prohibits charging interest (<em>nashak</em>) to fellow Israelites (Exodus 22:25; Deuteronomy 23:19-20) — to exploit a poor brother's desperation by 'biting' him with interest violates the covenant of brotherhood. Ezekiel lists usury among the sins that bring divine judgment (Ezekiel 18:13). Proverbs 23:32 uses <em>nashak</em> of wine: 'In the end it bites like a snake and poisons like a viper.' The serpent who bit humanity in Eden and the creditor who bites the poor share the same word — both are instruments of destruction.",
     [("Exodus 22:25", "If you lend money to one of my people among you who is needy, do not treat it like a business deal; charge no <em>interest</em>."),
      ("Proverbs 23:32", "In the end it <em>bites</em> like a snake and poisons like a viper."),
      ("Numbers 21:6", "Then the LORD sent venomous snakes among them; they <em>bit</em> the people and many Israelites died."),
      ("Habakkuk 2:7", "Will not your creditors suddenly arise? Will they not wake up and make you tremble? Then you will become their <em>prey</em>."),
      ("Ezekiel 18:13", "He lends at <em>interest</em> and takes a profit. Will such a man live? He will not! Because he has done all these detestable things, he is to be put to death.")],
     [("H5175", "Nachash (Serpent)"), ("H6213", "Asah (To Do/Make)"), ("H1800", "Dal (Poor/Weak)")]),

    (5534, "סָכַר", "Sakar", "Verb", "To Shut Up; To Deliver Over; To Hire",
     "To shut, close, or stop up — and also to deliver someone into another's hand or to hire out for wages. The range of meaning spans from physically closing something to handing someone over to an enemy.",
     "<em>Sakar</em> appears in Psalm 63:11 ('the mouths of liars will be silenced/<em>stopped</em>') and carries a covenantal dimension: God 'delivers over' enemies to Israel in holy war contexts. The idea of God shutting up the womb (Genesis context) and shutting up enemies follows a similar pattern — divine sovereignty over openings and closings, victories and defeats. In Proverbs 17:28, holding one's tongue ('even a fool is thought wise if he keeps silent') uses the concept of shutting the mouth as wisdom. The theology: there are times God opens and times He shuts — and His closings are as purposeful as His openings.",
     [("Psalm 63:11", "But the king will rejoice in God; all who swear by God will glory in him, while the mouths of liars will be <em>silenced</em>."),
      ("Judges 3:28", "Follow me, he ordered, for the LORD has given Moab your enemy into your hands. So they followed him down and took possession of the fords of the Jordan."),
      ("Proverbs 17:28", "Even fools are thought wise if they keep silent, and discerning if they hold their tongues."),
      ("Isaiah 19:4", "I will hand the Egyptians over to the power of a cruel master, and a fierce king will rule over them, declares the Lord, the LORD Almighty."),
      ("Revelation 3:7", "These are the words of him who is holy and true, who holds the key of David. What he opens no one can shut, and what he shuts no one can open.")],
     [("H5462", "Sagar (To Shut/Close)"), ("H5414", "Nathan (To Give)"), ("H6605", "Pathach (To Open)")]),

    (5688, "עֲבֹת", "Avot", "Noun, masculine/feminine", "Rope; Cord; Thick Branch; Interwoven Thing",
     "A thick twisted cord, rope, or interwoven branch — anything braided or woven together for strength. <em>Avot</em> can refer to physical ropes used to bind, to the thick branches of a tree, or to the cords of the Tabernacle.",
     "<em>Avot</em> connects the physical and spiritual in striking ways. Psalm 118:27 uses it for the festival procession: 'Bind the festal sacrifice with <em>cords</em> to the altar' — the bound sacrifice pointing forward to the Lamb of God. In Ezekiel 19, Israel's princes are compared to young lions entangled in <em>nets</em> and trapped by the nations — the cords becoming instruments of judgment. Song of Songs 3:6 uses related imagery for the beloved. Isaiah 5:18 warns against those who 'draw sin along with <em>cords</em> of deceit.' Ropes both bind and liberate in Scripture — Rahab's scarlet cord saved her life; the cords that bound Samson were broken by God's Spirit.",
     [("Psalm 118:27", "The LORD is God, and he has made his light shine on us. With boughs in hand, join in the festal procession up to the horns of the altar."),
      ("Judges 15:13", "They answered, 'We will only tie you up and hand you over to them. We will not kill you.' So they bound him with two new <em>ropes</em>."),
      ("Isaiah 5:18", "Woe to those who draw sin along with <em>cords</em> of deceit, and wickedness as with cart ropes."),
      ("Ezekiel 19:8", "Then the nations came against him, those from regions round about. They spread their net for him, and he was trapped in their pit."),
      ("Ecclesiastes 12:6", "Remember him — before the silver cord is severed, and the golden bowl is broken.")],
     [("H2256", "Chevel (Cord/Line)"), ("H4147", "Moser (Band/Bond)"), ("H6616", "Pathiyl (Thread/Cord)")]),

    (5742, "עָדָשׁ", "Adash", "Noun, masculine", "Lentil",
     "A lentil — the small red legume that became one of the most theologically loaded foods in the Bible. <em>Adash</em> appears in the famous story of Esau selling his birthright for a bowl of lentil stew.",
     "The lentil (<em>adash</em>) is remembered not for its culinary value but for the catastrophic transaction it represents. In Genesis 25:34, Esau trades his birthright — his covenant inheritance as firstborn — for a single meal of bread and lentil stew. Hebrews 12:16-17 uses this as the defining warning against spiritual immaturity: 'See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son.' The <em>adash</em> is thus a symbol of valuing immediate physical appetite over eternal covenant promises. The tragedy is not the lentils — it is that Esau 'despised his birthright' (Genesis 25:34).",
     [("Genesis 25:34", "Then Jacob gave Esau some bread and some <em>lentil</em> stew. He ate and drank, and then got up and left. So Esau despised his birthright."),
      ("2 Samuel 23:11", "Next to him was Shammah son of Agee the Hararite. When the Philistines banded together at a place where there was a field full of <em>lentils</em>, Israel's troops fled from them."),
      ("Ezekiel 4:9", "Take wheat and barley, beans and <em>lentils</em>, millet and spelt; put them in a storage jar and use them to make bread for yourself."),
      ("Hebrews 12:16", "See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son."),
      ("Matthew 6:33", "But seek first his kingdom and his righteousness, and all these things will be given to you as well.")],
     [("H1060", "Bekor (Firstborn)"), ("H5159", "Nachalah (Inheritance)"), ("H3899", "Lechem (Bread/Food)")]),

    (5937, "עָלַז", "Alaz", "Verb", "To Exult; To Rejoice Triumphantly; To Shout for Joy",
     "To exult, rejoice loudly, or shout for triumph — a celebratory, even boisterous form of joy typically connected with victory, deliverance, or worship. <em>Alaz</em> conveys vigorous, outward expression of joy rather than quiet contentment.",
     "<em>Alaz</em> is used of God's people rejoicing in His salvation (Psalm 28:7 — 'my heart <em>leaps for joy</em> and with my song I praise him') and of God Himself rejoicing over His people (Zephaniah 3:17 uses the related verb <em>sus</em> alongside the concept). It also appears in the unsettling context of enemies <em>exulting</em> over Israel's fall (Lamentations 2:17; Psalm 25:2). The word thus frames a theology of whose victory is being celebrated — and Scripture assures that ultimate <em>alaz</em> belongs to God and His redeemed. Psalm 149:5 pictures the saints <em>singing for joy</em> on their beds — joy that does not require circumstances to change because it is rooted in covenant identity.",
     [("Psalm 28:7", "The LORD is my strength and my shield; my heart trusts in him, and he helps me. My heart <em>leaps for joy</em>, and with my song I praise him."),
      ("Psalm 149:5", "Let his faithful people <em>rejoice</em> in this honor and sing for joy on their beds."),
      ("Proverbs 28:12", "When the righteous triumph, there is great <em>elation</em>; but when the wicked rise to power, people go into hiding."),
      ("Lamentations 2:17", "The LORD has done what he planned; he has fulfilled his word, which he decreed long ago. He has overthrown you without pity, he has let the enemy <em>gloat</em> over you."),
      ("Zephaniah 3:14", "Sing, Daughter Zion; shout aloud, Israel! Be glad and <em>rejoice</em> with all your heart, Daughter Jerusalem!")],
     [("H7442", "Ranan (To Shout for Joy)"), ("H8055", "Samach (To Rejoice)"), ("H1984", "Halal (To Praise)")]),

    (6175, "עָרוּם", "Arum", "Adjective", "Shrewd; Crafty; Prudent",
     "Shrewd, crafty, or prudent — depending on context. <em>Arum</em> is morally neutral as a word: it describes the cunning of the serpent in Genesis 3:1 ('Now the serpent was more <em>crafty</em> than any of the wild animals') and also the praiseworthy prudence of the wise in Proverbs.",
     "The same word that describes the serpent's deadly cunning (Genesis 3:1) also describes the wise man's admirable prudence throughout Proverbs (12:16; 13:16; 14:8, 15, 18; 22:3; 27:12). This linguistic double-edge is theologically intentional: wisdom and cunning share the same face. The difference is not the sharpness of mind but its direction — toward God and others' good (prudence) or toward self-interest at others' expense (craftiness). Jesus commands His disciples to be 'shrewd as snakes and innocent as doves' (Matthew 10:16) — invoking the very same serpent image as a model for Kingdom wisdom, redeemed by innocence.",
     [("Genesis 3:1", "Now the serpent was more <em>crafty</em> than any of the wild animals the LORD God had made."),
      ("Proverbs 12:16", "Fools show their annoyance at once, but the <em>prudent</em> overlook an insult."),
      ("Proverbs 22:3", "The <em>prudent</em> see danger and take refuge, but the simple keep going and pay the penalty."),
      ("Proverbs 14:8", "The wisdom of the <em>prudent</em> is to give thought to their ways, but the folly of fools is deception."),
      ("Matthew 10:16", "I am sending you out like sheep among wolves. Therefore be as <em>shrewd</em> as snakes and as innocent as doves.")],
     [("H2450", "Chakam (Wise)"), ("H6191", "Aram (To Be Crafty)"), ("H8394", "Tevunah (Understanding)")]),

    (6482, "פֶּצַע", "Petza", "Noun, masculine", "Wound; Bruise; Stripe",
     "A wound, bruise, or stripe — the mark left by a blow. <em>Petza</em> is used literally of physical wounds and metaphorically of the wounds that bring healing. It is the word at the heart of Isaiah's suffering servant theology.",
     "Isaiah 53:5 stands as the theological summit of <em>petza</em>: 'By his <em>wounds</em> we are healed.' The Hebrew word here is <em>chaburah</em> (H2250, stripe/bruise), but <em>petza</em> appears earlier in Isaiah 1:6 in the catalog of Israel's spiritual wounds and in Proverbs 20:30 ('Blows and wounds cleanse away evil; stripes purge the inmost being'). The theology of <em>petza</em> is paradoxical: wounds that hurt can heal; the mark of punishment becomes the mark of redemption. Psalm 38:5 laments 'My wounds (<em>petza</em>) fester and are loathsome because of my sinful folly.' Christ's wounds were not from His own folly — they were the wounds of the innocent bearing the guilt of the guilty.",
     [("Proverbs 20:30", "Blows and <em>wounds</em> scrub away evil, and beatings purge the inmost being."),
      ("Psalm 38:5", "My <em>wounds</em> fester and are loathsome because of my sinful folly."),
      ("Isaiah 1:6", "From the sole of your foot to the top of your head there is no soundness — only <em>wounds</em> and welts and open sores."),
      ("1 Kings 20:37", "The man struck and <em>wounded</em> him, and then the prophet went and waited for the king by the road."),
      ("Isaiah 53:5", "But he was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his <em>wounds</em> we are healed.")],
     [("H2250", "Chaburah (Stripe/Bruise)"), ("H4347", "Makkah (Blow/Plague)"), ("H7495", "Rapha (To Heal)")]),

    (6544, "פָּרַע", "Para", "Verb", "To Let Go; To Expose; To Neglect; To Lead Wildly",
     "To let loose, uncover, make bare, or lead into disorder. <em>Para</em> describes the unloosing of hair (as in disgrace or mourning), the neglecting of restraint, and the wild, leaderless state of a people without godly guidance.",
     "Moses descends from Sinai to find the Israelites in chaos — and Aaron had 'let them run wild (<em>para</em>)' (Exodus 32:25). The same word describes the uncovering of a woman's hair in a jealousy ritual (Numbers 5:18) and the wild disorder of people without prophetic leadership (Proverbs 29:18 — 'Where there is no revelation/vision, the people <em>cast off restraint</em>'). This is one of the most widely quoted Old Testament proverbs in church leadership contexts. <em>Para</em> captures the spiritual danger of a community without truth-speaking leadership: not just discomfort, but dangerous moral unraveling.",
     [("Exodus 32:25", "Moses saw that the people were running wild (<em>para</em>) and that Aaron had let them get out of control."),
      ("Proverbs 29:18", "Where there is no revelation, people <em>cast off restraint</em>; but blessed is the one who heeds wisdom's instruction."),
      ("Numbers 5:18", "Then he shall have the woman stand before the LORD and let her hair hang loose (<em>para</em>) and place in her hands the reminder-offering."),
      ("Leviticus 13:45", "Anyone with such a defiling disease must wear torn clothes, let their hair be unkempt (<em>para</em>), cover the lower part of their face and cry out, 'Unclean! Unclean!'"),
      ("Proverbs 1:25", "Since you disregard all my advice and do not accept my rebuke.")],
     [("H6285", "Pea (Corner/Side)"), ("H2377", "Chazon (Vision/Revelation)"), ("H4428", "Melek (King)")]),

    (7111, "קְצָבָה", "Qetsavah", "Noun, feminine", "Fragment; Clipping; Cut Piece",
     "A piece cut off, a fragment, or an end-cut. <em>Qetsavah</em> refers to the clippings or cuttings from metal or material — the leftover pieces, the scraps of something larger. It appears in the context of economic deception.",
     "In Amos 8:5, merchants are condemned for 'making the shekel larger and the ephah smaller' and 'skimping on the measure, boosting the price and cheating with dishonest scales, buying the poor with silver and the needy for a pair of sandals, selling even the <em>sweepings</em> with the wheat.' The <em>qetsavah</em> — the scraps, the fragments, the dregs swept up — was being mixed with quality wheat and sold as pure grain. This economic fraud against the poor violated the covenant vision of a just society. Amos's prophetic thundering against this practice establishes that God cares about the <em>qetsavah</em> — about whether the poor are cheated even in the smallest commercial transactions.",
     [("Amos 8:5", "Skimping on the measure, boosting the price and cheating with dishonest scales, buying the poor with silver and the needy for a pair of sandals, selling even the <em>sweepings</em> with the wheat."),
      ("Micah 6:11", "Shall I acquit someone with dishonest scales, with a bag of false weights?"),
      ("Proverbs 11:1", "Dishonest scales are an abomination to the LORD, but an accurate weight finds favor with him."),
      ("Leviticus 19:35", "Do not use dishonest standards when measuring length, weight or quantity."),
      ("Luke 16:10", "Whoever can be trusted with very little can also be trusted with much, and whoever is dishonest with very little will also be dishonest with much.")],
     [("H374", "Ephah (Measure)"), ("H8255", "Shekel (Weight/Coin)"), ("H6664", "Tsedeq (Righteousness)")]),

    (7305, "רֶוַח", "Revach", "Noun, masculine", "Space; Relief; Breathing Room; Deliverance",
     "Space, room, or relief — particularly the sense of breathing room after a time of pressure and distress. <em>Revach</em> describes the relief that comes when danger passes or oppression lifts.",
     "In Esther 4:14, Mordecai challenges Esther with one of Scripture's most famous statements of Providence: 'If you remain silent at this time, relief and deliverance (<em>revach</em>) for the Jews will arise from another place, but you and your father's family will perish. And who knows but that you have come to your royal position for such a time as this?' The <em>revach</em> — the relief, the breathing room — will come either through Esther or through another means, because God's purposes cannot be stopped. Genesis 32:16 uses <em>revach</em> of the space Jacob put between his flocks as a buffer. The theology: God always provides <em>revach</em> — a way through, a space to breathe — for those who trust Him.",
     [("Esther 4:14", "If you remain silent at this time, <em>relief and deliverance</em> for the Jews will arise from another place, but you and your father's family will perish."),
      ("Genesis 32:16", "He put them in the care of his servants, each herd by itself, and said to his servants, 'Go ahead of me, and keep some <em>space</em> between the herds.'"),
      ("Job 36:16", "He is wooing you from the jaws of distress to a <em>spacious</em> place free from restriction."),
      ("Psalm 4:1", "Answer me when I call to you, my righteous God. Give me <em>relief</em> from my distress; have mercy on me and hear my prayer."),
      ("Isaiah 58:6", "Is not this the kind of fasting I have chosen: to loose the chains of injustice and untie the cords of the yoke, to set the oppressed free and break every yoke?")],
     [("H7337", "Rachav (To Be Wide/Spacious)"), ("H3467", "Yasha (To Save/Deliver)"), ("H6862", "Tsar (Distress/Adversary)")]),

    (7399, "רְכוּשׁ", "Rekush", "Noun, masculine", "Wealth; Property; Possessions",
     "Wealth, property, or possessions — particularly goods and material wealth accumulated over time. <em>Rekush</em> appears frequently in narratives of patriarchal prosperity and the spoils of warfare.",
     "<em>Rekush</em> is the word used of Abram's great wealth when he left Egypt (Genesis 12:5; 13:6) and of the property promised to Israel's descendants when they would leave Egypt after 400 years (Genesis 15:14 — 'they will come out with great <em>possessions</em>'). This prophetic promise was fulfilled in the Exodus plunder. In Ezra and Nehemiah, <em>rekush</em> describes the property restored to returning exiles. The theology of <em>rekush</em> in the OT establishes that material wealth is neither evil nor ultimate — it is a stewardship. Abraham's <em>rekush</em> was great enough to fund military campaigns (Genesis 14) and hospitality — it was wealth directed toward covenant purposes.",
     [("Genesis 15:14", "But I will punish the nation they serve as slaves, and afterward they will come out with great <em>possessions</em>."),
      ("Genesis 13:6", "But the land could not support them while they stayed together, for their <em>possessions</em> were so great that they were not able to stay together."),
      ("Ezra 1:6", "All their neighbors assisted them with articles of silver and gold, with goods and livestock, and with valuable gifts, in addition to all the freewill offerings."),
      ("Daniel 11:13", "For the king of the North will muster another army, larger than the first; and after several years, he will advance with a huge army fully equipped."),
      ("Proverbs 13:22", "A good person leaves an inheritance for their children's children, but a sinner's <em>wealth</em> is stored up for the righteous.")],
     [("H2428", "Chayil (Wealth/Valor)"), ("H1952", "Hon (Wealth)"), ("H5159", "Nachalah (Inheritance)")]),

    (8041, "שָׂמַאל", "Samal", "Verb", "To Go Left; To Turn to the Left",
     "To go to the left, take the left direction, or use the left hand. <em>Samal</em> is the verbal form related to <em>semol</em> (H8040, the left side), and is used of spatial direction in both navigation and symbolic positioning.",
     "In biblical symbolism, the right hand (<em>yamin</em>) represents favor, strength, and honor, while the left (<em>semol</em>/<em>samal</em>) often represents the secondary or less-favored position. Yet the Song of Songs uses both: 'His left arm is under my head, and his right arm embraces me' (Song of Songs 2:6; 8:3) — both directions encompass the beloved. Ecclesiastes 10:2 states: 'The heart of the wise inclines to the right, but the heart of the fool to the left.' The eschatological judgment in Matthew 25:33-41 places the sheep at the right and the goats at the left — the ultimate directional theology. Yet in the Kingdom, the formerly secondary is elevated: the elder serves the younger, the last becomes first.",
     [("Genesis 13:9", "Is not the whole land before you? Let's part company. If you go to the left, I'll go to the right; if you go to the right, I'll go to the left."),
      ("Song of Songs 2:6", "His left arm is under my head, and his right arm embraces me."),
      ("Ecclesiastes 10:2", "The heart of the wise inclines to the right, but the heart of the fool to the <em>left</em>."),
      ("Matthew 25:33", "He will put the sheep on his right and the goats on his <em>left</em>."),
      ("Proverbs 4:27", "Do not turn to the right or the <em>left</em>; keep your foot from evil.")],
     [("H3225", "Yamin (Right Hand/Side)"), ("H3027", "Yad (Hand)"), ("H1870", "Derek (Way/Path)")]),

    (8437, "תּוֹלָל", "Tolal", "Noun, masculine", "Oppressor; One Who Makes Wretched",
     "An oppressor or one who causes wretchedness and misery. <em>Tolal</em> derives from the root <em>yalal</em> (H3213, to wail/howl) and describes one whose oppression drives others to wailing and lamentation.",
     "<em>Tolal</em> appears in Psalm 137:3 — the haunting lament of the Babylonian exile: 'For there our captors asked us for songs, our <em>tormentors</em> demanded songs of joy.' The exiles were forced by their oppressors to perform — to sing the songs of Zion in a foreign land, adding humiliation to captivity. The theology of Psalm 137 speaks to the impossibility of authentic worship under coercion and the depth of grief that displacement produces. 'How can we sing the songs of the LORD while in a foreign land?' is not a rhetorical refusal to worship — it is a theological protest that true worship requires freedom, and that those who demand it from the oppressed will face God's judgment.",
     [("Psalm 137:3", "For there our captors asked us for songs, our <em>tormentors</em> demanded songs of joy; they said, 'Sing us one of the songs of Zion!'"),
      ("Psalm 137:1", "By the rivers of Babylon we sat and wept when we remembered Zion."),
      ("Lamentations 1:5", "Her foes have become her masters; her enemies are at ease. The LORD has brought her grief because of her many sins."),
      ("Isaiah 14:4", "You will take up this taunt against the king of Babylon: How the <em>oppressor</em> has come to an end! How his fury has ended!"),
      ("Revelation 18:10", "Terrified at her torment, they will stand far off and cry: 'Woe! Woe to you, great city, you mighty city of Babylon!'")],
     [("H6693", "Tsuk (To Constrain/Oppress)"), ("H3905", "Lachats (To Press/Oppress)"), ("H1350", "Gaal (Redeemer)")]),

    (8551, "תָּמַךְ", "Tamak", "Verb", "To Hold; To Support; To Uphold; To Grasp",
     "To hold, grasp, support, or uphold — used of physical support (holding up a person or object) and of God's sustaining grip on His people. <em>Tamak</em> describes a firm, sustaining hold that does not let go.",
     "<em>Tamak</em> appears powerfully in Psalm 63:8: 'I cling to you; your right hand upholds (<em>tamak</em>) me.' The syntax is remarkable — the worshiper clings to God while God simultaneously upholds the worshiper. Proverbs 4:4 uses <em>tamak</em> of holding wisdom: 'Take hold of my words with all your heart; keep my commands, and you will live.' Isaiah 41:10 — the great 'Do not fear' passage — concludes with God's promise: 'I will uphold (<em>tamak</em>) you with my righteous right hand.' The theology of <em>tamak</em> is that God's grip is more reliable than our own — He holds us even when our grip on Him fails.",
     [("Psalm 63:8", "I cling to you; your right hand <em>upholds</em> me."),
      ("Isaiah 41:10", "Do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will <em>uphold</em> you with my righteous right hand."),
      ("Proverbs 4:4", "Then he taught me, and he said to me, 'Take <em>hold</em> of my words with all your heart; keep my commands, and you will live.'"),
      ("Proverbs 11:16", "A kindhearted woman gains honor, but ruthless men gain only wealth."),
      ("Amos 1:5", "I will break down the gate of Damascus; I will destroy the king who is in the Valley of Aven and the one who holds the scepter in Beth Eden.")],
     [("H2388", "Chazaq (To Strengthen/Hold)"), ("H5582", "Saad (To Support)"), ("H3027", "Yad (Hand)")]),
]

# ===== GREEK ENTRIES (23 total) =====
greek_words = [
    # (num, script, translit, pos, gloss, definition, theology, verses, related)
    (1149, "Δαλματία", "Dalmatia", "Proper Noun (place)", "Dalmatia (Region on the Adriatic Coast)",
     "Dalmatia was a Roman province on the eastern shore of the Adriatic Sea, corresponding roughly to modern-day Croatia and Bosnia. It appears once in the New Testament — 2 Timothy 4:10 — where Paul reports that Titus has gone there for ministry.",
     "The mention of Dalmatia in 2 Timothy 4:10 is a window into the early church's missionary reach. Paul, writing from his final imprisonment in Rome, notes that his coworkers have scattered to their mission fields: Crescens to Galatia, Titus to <em>Dalmatia</em>, and only Luke remains. Rather than lamenting the loneliness, this verse reveals a church actively spreading beyond its Middle Eastern origins into the Roman Empire's provinces. Titus's mission to Dalmatia shows that the gospel was being planted in what would become Central Europe — a reminder that God's redemptive purposes are global, and that Paul's imprisonment did not stop the advance of the Kingdom.",
     [("2 Timothy 4:10", "For Demas, because he loved this world, has deserted me and has gone to Thessalonica. Crescens has gone to Galatia, and Titus to <em>Dalmatia</em>."),
      ("Titus 1:5", "The reason I left you in Crete was that you might put in order what was left unfinished and appoint elders in every town, as I directed you."),
      ("Acts 20:2", "He traveled through that area, speaking many words of encouragement to the people, and finally arrived in Greece."),
      ("Romans 15:19", "From Jerusalem all the way around to Illyricum, I have fully proclaimed the gospel of Christ."),
      ("Matthew 28:19", "Therefore go and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit.")],
     [("G5103", "Titos (Titus)"), ("G652", "Apostolos (Apostle)"), ("G2097", "Euangelizō (To Preach the Gospel)")]),

    (1151, "δάμαλις", "Damalis", "Noun, feminine", "Heifer; Young Cow",
     "A young cow or heifer — specifically an animal that has not yet been yoked. In Scripture, the heifer is the central element of several important purification rituals.",
     "The Greek <em>damalis</em> appears in Hebrews 9:13 in the context of the Day of Atonement and purification rites: 'The blood of goats and bulls and the ashes of a <em>heifer</em> sprinkled on those who are ceremonially unclean sanctify them so that they are outwardly clean.' This refers to the Red Heifer ritual of Numbers 19 — one of the most mysterious of all Mosaic ordinances. A perfectly red, unblemished heifer was slaughtered outside the camp, burned, and its ashes mixed with water to create a purification solution for those contaminated by contact with death. The writer of Hebrews uses this as a stepping-stone: if the ashes of a heifer could cleanse the body, how much more does the blood of Christ cleanse the conscience?",
     [("Hebrews 9:13", "The blood of goats and bulls and the ashes of a <em>heifer</em> sprinkled on those who are ceremonially unclean sanctify them so that they are outwardly clean."),
      ("Numbers 19:2", "This is a requirement of the law that the LORD has commanded: Tell the Israelites to bring you a red <em>heifer</em> without defect or blemish."),
      ("Hebrews 9:14", "How much more, then, will the blood of Christ, who through the eternal Spirit offered himself unblemished to God, cleanse our consciences from acts that lead to death."),
      ("Numbers 19:9", "A man who is clean shall gather up the ashes of the <em>heifer</em> and put them in a ceremonially clean place outside the camp."),
      ("1 Peter 1:19", "But with the precious blood of Christ, a lamb without blemish or defect.")],
     [("G80", "Adelphos (Brother)"), ("G129", "Haima (Blood)"), ("G2513", "Katharos (Clean/Pure)")]),

    (1153, "Δαμασκηνός", "Damaskēnos", "Adjective (proper)", "Damascene; Of Damascus",
     "An inhabitant or citizen of Damascus — used in Acts 9 of the Jews who plotted against Paul, and in 2 Corinthians 11:32 of the governor under King Aretas who guarded the city to arrest Paul.",
     "Damascus is one of the world's oldest continuously inhabited cities and holds pivotal significance in Paul's biography. It was on the road to Damascus that Saul of Tarsus encountered the risen Christ (Acts 9:3-8), and it was in Damascus that he was baptized and began preaching (Acts 9:19-22). The <em>Damascene</em> governor's pursuit of Paul (2 Corinthians 11:32) — forcing his dramatic escape in a basket through the city wall — is one of the few events Paul mentions in his autobiographical section. Damascus represents both Paul's conversion (new beginning) and his first persecution (immediate cost). The city that witnessed the death of the old Saul also witnessed the first attempts to kill the new Paul.",
     [("2 Corinthians 11:32", "In <em>Damascus</em> the governor under King Aretas had the city of the Damascenes guarded in order to arrest me."),
      ("Acts 9:8", "Saul got up from the ground, but when he opened his eyes he could see nothing. So they led him by the hand into <em>Damascus</em>."),
      ("Acts 9:22", "Yet Saul grew more and more powerful and baffled the Jews living in <em>Damascus</em> by proving that Jesus is the Messiah."),
      ("Galatians 1:17", "I did not go up to Jerusalem to see those who were apostles before I was, but I went into Arabia. Later I returned to <em>Damascus</em>."),
      ("Acts 22:6", "About noon as I came near <em>Damascus</em>, suddenly a bright light from heaven flashed around me.")],
     [("G3972", "Paulos (Paul)"), ("G652", "Apostolos (Apostle)"), ("G5547", "Christos (Christ)")]),

    (1154, "Δαμασκός", "Damaskos", "Proper Noun (city)", "Damascus",
     "The ancient city of Damascus — capital of Syria and one of the most historically significant cities in biblical narrative. Damascus features in the lives of Abraham, David, Elijah, Isaiah, and Paul.",
     "Damascus appears throughout Scripture as a geopolitical and theological reference point. In Genesis 14:15, Abram pursues the kings as far as Hobah, north of Damascus. David garrisoned Damascus after defeating Hadadezer (2 Samuel 8:6). Elijah was commanded to anoint Hazael as king of Damascus (1 Kings 19:15). Isaiah pronounced judgment oracles against Damascus (Isaiah 17:1). But Damascus's most theologically transformative moment is Paul's conversion on the Damascus road — the city whose name is forever linked to the moment God arrested the greatest persecutor of the church and transformed him into its greatest apostle.",
     [("Acts 9:3", "As he neared <em>Damascus</em> on his journey, suddenly a light from heaven flashed around him."),
      ("2 Corinthians 11:32", "In <em>Damascus</em> the governor under King Aretas had the city of the Damascenes guarded in order to arrest me."),
      ("Galatians 1:17", "I did not go up to Jerusalem to see those who were apostles before I was, but I went into Arabia. Later I returned to <em>Damascus</em>."),
      ("Isaiah 17:1", "A prophecy against <em>Damascus</em>: See, <em>Damascus</em> will no longer be a city but will become a heap of ruins."),
      ("Acts 9:19", "And after taking some food, he regained his strength. Saul spent several days with the disciples in <em>Damascus</em>.")],
     [("G1153", "Damaskēnos (Damascene)"), ("G3972", "Paulos (Paul)"), ("G2424", "Iēsous (Jesus)")]),

    (1156, "δανείζω", "Daneizō", "Verb", "To Lend Money; To Borrow",
     "To lend or borrow money — particularly the practice of lending at interest. In the New Testament, <em>daneizō</em> appears in Jesus' teaching on radical generosity.",
     "Jesus uses <em>daneizō</em> in Luke 6:34-35 to push far beyond the cultural norm of lending to those who will repay: 'And if you lend to those from whom you expect repayment, what credit is that to you? Even sinners lend to sinners, expecting to be repaid in full. But love your enemies, do good to them, and <em>lend</em> to them without expecting to get anything back.' This transforms <em>daneizō</em> from an economic transaction into a spiritual practice. Lending without expectation of return is financially absurd by any human calculus — but it images the generosity of a God who gives grace, not loans. Paul echoes this in Romans 13:8: 'Let no debt remain outstanding, except the continuing debt to love one another.'",
     [("Luke 6:34", "And if you <em>lend</em> to those from whom you expect repayment, what credit is that to you? Even sinners <em>lend</em> to sinners, expecting to be repaid in full."),
      ("Luke 6:35", "But love your enemies, do good to them, and <em>lend</em> to them without expecting to get anything back."),
      ("Matthew 5:42", "Give to the one who asks you, and do not turn away from the one who wants to <em>borrow</em> from you."),
      ("Deuteronomy 15:8", "Rather, be openhanded and freely <em>lend</em> them whatever they need."),
      ("Psalm 37:26", "They are always generous and <em>lend</em> freely; their children will be a blessing.")],
     [("G1157", "Danistēs (Creditor/Money-Lender)"), ("G1155", "Daneion (Debt)"), ("G26", "Agapē (Love)")]),

    (1157, "δανειστής", "Danistēs", "Noun, masculine", "Creditor; Money-Lender",
     "A creditor or money-lender — one who makes a business of lending money, often at interest. In the New Testament, the creditor figure appears in Jesus' parables as both a theological illustration and a warning.",
     "In Luke 7:41-42, Jesus uses the <em>danistēs</em> in one of His most pointed parables: 'Two people owed money to a certain creditor (<em>danistēs</em>). One owed five hundred denarii, and the other fifty. Neither of them had the money to pay him back, so he forgave the debts of both. Now which of them will love him more?' This is spoken to Simon the Pharisee after a sinful woman anointed Jesus' feet. The parable reframes sin as debt and forgiveness as cancellation by the creditor. The greater the debt cancelled, the greater the love produced. Every believer is the debtor who could not pay — and Christ is the creditor who absorbed the loss.",
     [("Luke 7:41", "Two people owed money to a certain <em>creditor</em>. One owed five hundred denarii, and the other fifty."),
      ("Luke 7:42", "Neither of them had the money to pay him back, so he forgave the debts of both. Now which of them will love him more?"),
      ("Matthew 18:23", "Therefore, the kingdom of heaven is like a king who wanted to settle accounts with his servants."),
      ("Romans 4:4", "Now to the one who works, wages are not credited as a gift but as an obligation."),
      ("Colossians 2:14", "Having canceled the charge of our legal indebtedness, which stood against us and condemned us; he has taken it away, nailing it to the cross.")],
     [("G1156", "Daneizō (To Lend)"), ("G1155", "Daneion (Debt/Loan)"), ("G863", "Aphiēmi (To Forgive/Release)")]),

    (1158, "Δανιήλ", "Daniēl", "Proper Noun (person)", "Daniel",
     "Daniel — the Hebrew prophet of the Babylonian exile, whose name means 'God is my judge.' In the New Testament, Jesus refers to Daniel in His Olivet Discourse as the source of the 'abomination of desolation' prophecy.",
     "Jesus' reference to 'the abomination that causes desolation, spoken of through the prophet <em>Daniel</em>' (Matthew 24:15; Mark 13:14) establishes Daniel as a key prophetic voice for end-times theology. Daniel's visions of the four kingdoms, the Son of Man coming on clouds (Daniel 7:13-14), the seventy weeks (Daniel 9:24-27), and the abomination of desolation (Daniel 11:31; 12:11) form the backbone of Jesus' eschatological teaching. The New Testament canon treats Daniel as authoritative predictive prophecy. Daniel himself is commended in Ezekiel 14:14, 20 alongside Noah and Job as a man of exceptional righteousness — extraordinary since Ezekiel's prophecy overlapped with Daniel's lifetime.",
     [("Matthew 24:15", "So when you see standing in the holy place 'the abomination that causes desolation,' spoken of through the prophet <em>Daniel</em> — let the reader understand."),
      ("Daniel 7:13", "In my vision at night I looked, and there before me was one like a son of man, coming with the clouds of heaven."),
      ("Daniel 9:27", "He will confirm a covenant with many for one 'seven.' In the middle of the 'seven' he will put an end to sacrifice and offering."),
      ("Ezekiel 14:14", "Even if these three men — Noah, <em>Daniel</em> and Job — were in it, they could save only themselves by their righteousness."),
      ("Hebrews 11:33", "Who through faith conquered kingdoms, administered justice, and gained what was promised; who shut the mouths of lions.")],
     [("G4396", "Prophētēs (Prophet)"), ("G5207", "Huios (Son)"), ("G444", "Anthrōpos (Man)")]),

    (1160, "δαπάνη", "Dapanē", "Noun, feminine", "Cost; Expense",
     "The cost or expense of something — the actual outlay required to accomplish a task. Jesus uses <em>dapanē</em> in the Parable of the Tower Builder to illustrate the cost of discipleship.",
     "Jesus uses <em>dapanē</em> in Luke 14:28: 'Suppose one of you wants to build a tower. Won't you first sit down and estimate the <em>cost</em> (<em>dapanē</em>) to see if you have enough money to complete it?' The parable is embedded in a larger teaching (Luke 14:25-33) about the radical demands of discipleship: hating family, carrying a cross, giving up all possessions. The Tower Builder who cannot finish is mocked; the King who cannot win makes peace. The point is not that discipleship is optional if the cost is too high, but that Jesus demands honest, clear-eyed commitment — not impulsive enthusiasm. Grace is free but discipleship is costly.",
     [("Luke 14:28", "Suppose one of you wants to build a tower. Won't you first sit down and estimate the <em>cost</em> to see if you have enough money to complete it?"),
      ("Luke 9:23", "Then he said to them all: 'Whoever wants to be my disciple must deny themselves and take up their cross daily and follow me.'"),
      ("Philippians 3:8", "What is more, I consider everything a loss because of the surpassing worth of knowing Christ Jesus my Lord."),
      ("Luke 14:33", "In the same way, those of you who do not give up everything you have cannot be my disciples."),
      ("Matthew 16:24", "Then Jesus said to his disciples, 'Whoever wants to be my disciple must deny themselves and take up their cross and follow me.'")],
     [("G1159", "Dapanaō (To Spend)"), ("G4716", "Stauros (Cross)"), ("G3101", "Mathētēs (Disciple)")]),

    (1164, "δεῖγμα", "Deigma", "Noun, neuter", "Example; Specimen; Public Display",
     "An example made visible — a specimen or display put before others as a warning or proof. In Jude 7, Sodom and Gomorrah are described as a <em>deigma</em> undergoing the punishment of eternal fire.",
     "Sodom and Gomorrah as <em>deigma</em> is a solemn theological statement: God's judgments in history serve pedagogical purposes. The punishment of cities and nations is not merely retributive — it is revelatory. The Hebrew prophets frequently cite Sodom as the comparison point for moral catastrophe. Jesus Himself uses Sodom as the measuring stick for towns that reject the gospel (Matthew 10:15). As a <em>deigma</em> of eternal fire, Sodom warns every generation that divine patience has limits and divine judgment is real.",
     [("Jude 7", "In a similar way, Sodom and Gomorrah and the surrounding towns gave themselves up to sexual immorality and perversion. They serve as an <em>example</em> of those who suffer the punishment of eternal fire."),
      ("Genesis 19:24", "Then the LORD rained down burning sulfur on Sodom and Gomorrah — from the LORD out of the heavens."),
      ("Matthew 10:15", "Truly I tell you, it will be more bearable for Sodom and Gomorrah on the day of judgment than for that town."),
      ("2 Peter 2:6", "If he condemned the cities of Sodom and Gomorrah by burning them to ashes, and made them an example of what is going to happen to the ungodly."),
      ("Ezekiel 16:49", "Now this was the sin of your sister Sodom: She and her daughters were arrogant, overfed and unconcerned; they did not help the poor and needy.")],
     [("G5262", "Hypodeigma (Pattern/Example)"), ("G2920", "Krisis (Judgment)"), ("G4442", "Pyr (Fire)")]),

    (1168, "δειλιάω", "Deiliaō", "Verb", "To Be Afraid; To Cower; To Be Cowardly",
     "To be timidly afraid or cowardly — to shrink back in fear when faithfulness demands standing firm. Jesus uses this verb in John 14:27 alongside 'troubled,' giving the full picture of anxiety and cowardice that His peace addresses.",
     "The peace that Jesus gives is not the world's peace (absence of conflict) but the peace of absolute security in God's eternal purpose. Because Jesus is going to the Father (John 14:28), the disciples can stand firm — they are not abandoned. <em>Deiliaō</em> in the face of persecution or loss is addressed not by minimizing the danger but by anchoring the soul in the resurrection reality. Those who know the risen Lord need not <em>deiliaō</em> before human powers.",
     [("John 14:27", "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid (<em>deiliaō</em>)."),
      ("Deuteronomy 1:21", "See, the LORD your God has given you the land. Go up and take possession of it as the LORD, the God of your ancestors, told you. Do not be afraid; do not be discouraged."),
      ("Joshua 8:1", "Then the LORD said to Joshua, 'Do not be afraid; do not be discouraged. Take the whole army with you.'"),
      ("Isaiah 35:4", "Say to those with fearful hearts, 'Be strong, do not fear; your God will come, he will come with divine retribution; God will come to save you.'"),
      ("1 John 4:18", "There is no fear in love. But perfect love drives out fear, because fear has to do with punishment.")],
     [("G1167", "Deilia (Cowardice)"), ("G1169", "Deilos (Cowardly/Fearful)"), ("G1515", "Eirēnē (Peace)")]),

    (1171, "δεινῶς", "Deinōs", "Adverb", "Terribly; Grievously; Fiercely",
     "Terribly, dreadfully, or fiercely — an adverb of intensity used of extreme suffering or fierce opposition. Appears twice in the NT: of terrible suffering (Matthew 8:6) and fierce opposition by religious leaders (Luke 11:53).",
     "The centurion's use of <em>deinōs</em> in Matthew 8:6 gives insight into his character: he comes not with a casual request but with the urgent weight of a man who has watched someone he cares for suffer terribly. This intense plea, matched with profound humility (v. 8), produces one of Jesus' greatest commendations: 'I have not found anyone in Israel with such great faith.' Meanwhile in Luke 11:53, <em>deinōs</em> describes how fiercely the religious establishment opposed Jesus after His woes against them — a reminder that faithful proclamation of truth provokes fierce resistance.",
     [("Matthew 8:6", "He said, 'Lord, my servant lies at home paralyzed, suffering <em>terribly</em>.'"),
      ("Luke 11:53", "When Jesus went outside, the Pharisees and the teachers of the law began to oppose him <em>fiercely</em> and to besiege him with questions."),
      ("Matthew 8:10", "When Jesus heard this, he was amazed and said to those following him, 'Truly I tell you, I have not found anyone in Israel with such great faith.'"),
      ("John 15:20", "If they persecuted me, they will persecute you also. If they obeyed my teaching, they will obey yours also."),
      ("2 Timothy 3:12", "In fact, everyone who wants to live a godly life in Christ Jesus will be persecuted.")],
     [("G3173", "Megas (Great)"), ("G2560", "Kakōs (Badly/Grievously)"), ("G4102", "Pistis (Faith)")]),

    (1174, "δεισιδαιμονέστερος", "Deisidaimonesteros", "Adjective (comparative)", "More Religious; Very Religious",
     "More devoted to the divine — intentionally ambiguous in Paul's Areopagus address, allowing it to be heard as either a polite compliment (very devout) or a gentle critique (overly superstitious). Paul uses this to open a bridge to the gospel.",
     "Paul's Areopagus speech (Acts 17:22-31) is a masterclass in apologetics. He begins with the Athenians' own religiosity — their altar 'TO AN UNKNOWN GOD' — and uses it as a bridge to proclaim Christ. Rather than condemning their worship, he acknowledges their genuine religious impulse and redirects it: 'What you worship as something unknown I am going to proclaim to you.' This approach — finding the true knowledge hidden inside incomplete seeking — reflects the theology that God has placed eternity in the human heart (Ecclesiastes 3:11) and that all genuine seeking ultimately leads to Him.",
     [("Acts 17:22", "Paul then stood up in the meeting of the Areopagus and said: 'People of Athens! I see that in every way you are very religious (<em>deisidaimonesteros</em>).'"),
      ("Acts 17:23", "For as I walked around and looked carefully at your objects of worship, I even found an altar with this inscription: TO AN UNKNOWN GOD."),
      ("Acts 17:28", "'For in him we live and move and have our being.' As some of your own poets have said, 'We are his offspring.'"),
      ("Ecclesiastes 3:11", "He has made everything beautiful in its time. He has also set eternity in the human heart; yet no one can fathom what God has done."),
      ("Romans 1:20", "For since the creation of the world God's invisible qualities — his eternal power and divine nature — have been clearly seen.")],
     [("G1175", "Deisidaimonia (Religion/Superstition)"), ("G2316", "Theos (God)"), ("G4151", "Pneuma (Spirit)")]),

    (1175, "δεισιδαιμονία", "Deisidaimonia", "Noun, feminine", "Religion; Fear of the Divine; Superstition",
     "Religion or religious scrupulosity — fear and reverence toward divine beings. Used by Festus in Acts 25:19 to describe Paul's dispute with Jewish leaders as being about their own religion and about a dead man named Jesus.",
     "Festus's use of <em>deisidaimonia</em> is a window into how early Christianity appeared to outsiders — as an internal Jewish dispute about resurrection. From the Roman perspective, it was religious enthusiasm. From the NT perspective, the resurrection is the hinge of all history. Paul's defense before both Festus and Agrippa (Acts 25-26) shows him willing to be dismissed as religiously zealous as long as he can proclaim that Christ died for our sins and rose again — the core of his gospel.",
     [("Acts 25:19", "Instead, they had some points of dispute with him about their own <em>religion</em> and about a dead man named Jesus who Paul claimed was alive."),
      ("Acts 17:22", "Paul then stood up in the meeting of the Areopagus and said: 'People of Athens! I see that in every way you are very religious.'"),
      ("Acts 26:5", "They have known me for a long time and can testify, if they are willing, that I conformed to the strictest sect of our religion, living as a Pharisee."),
      ("Romans 10:2", "For I can testify about them that they are zealous for God, but their zeal is not based on knowledge."),
      ("1 Corinthians 15:3", "For what I received I passed on to you as of first importance: that Christ died for our sins according to the Scriptures.")],
     [("G1174", "Deisidaimonesteros (More Religious)"), ("G2356", "Thrēskeia (Religion)"), ("G386", "Anastasis (Resurrection)")]),

    (1176, "δέκα", "Deka", "Numeral", "Ten",
     "The number ten — foundational to biblical covenant structure. Ten Commandments, ten plagues, ten virgins, ten minas. Ten represents completeness in the decimal system and full accountability.",
     "When Jesus structures a parable around ten virgins (Matthew 25:1-13) or ten minas (Luke 19:13-27), He invokes a completeness — the full range of humanity represented. The ten virgins represent the whole of those awaiting the Bridegroom: half prepared, half not. The lesson is radical: spiritual preparedness cannot be borrowed or transferred at the last moment. The ten minas represent the totality of what the King has entrusted — full accountability for every steward.",
     [("Matthew 25:1", "At that time the kingdom of heaven will be like <em>ten</em> virgins who took their lamps and went out to meet the bridegroom."),
      ("Luke 15:8", "Or suppose a woman has <em>ten</em> silver coins and loses one."),
      ("Luke 19:13", "So he called <em>ten</em> of his servants and gave them <em>ten</em> minas."),
      ("Revelation 17:12", "The <em>ten</em> horns you saw are ten kings who have not yet received a kingdom."),
      ("Exodus 34:28", "Moses was there with the LORD forty days and forty nights without eating bread or drinking water. And he wrote on the tablets the words of the covenant — the <em>Ten</em> Commandments.")],
     [("G1181", "Dekatē (Tithe/Tenth)"), ("G1182", "Dekatos (Tenth)"), ("G1785", "Entolē (Commandment)")]),

    (1178, "δεκαπέντε", "Dekapente", "Numeral", "Fifteen",
     "The number fifteen — appearing in key biblical chronological and relational details: fifteen stadia from Bethany to Jerusalem, fifteen days Paul spent with Peter, and fifteen Psalms of Ascent (Psalms 120-134).",
     "The fifteen days Paul spent with Peter (Galatians 1:18) is historically significant. After his Damascus conversion and three years in Arabia, Paul's first extended apostolic contact was this fifteen-day visit. This careful historical note grounds the continuity of Paul's gospel — it was independently received (Galatians 1:12) but consistent with what Peter and James testified. John 11:18's note that Bethany was fifteen stadia from Jerusalem explains why mourners from the city were present — and why the Lazarus miracle was so publicly witnessed and so threatening to the religious establishment.",
     [("John 11:18", "Now Bethany was less than two miles (<em>fifteen stadia</em>) from Jerusalem, and many Jews had come to Martha and Mary to comfort them."),
      ("Galatians 1:18", "Then after three years, I went up to Jerusalem to get acquainted with Cephas and stayed with him <em>fifteen</em> days."),
      ("Acts 27:28", "They took soundings and found that the water was a hundred and twenty feet deep. A short time later they took soundings again and found it was ninety feet deep."),
      ("Psalm 122:1", "I rejoiced with those who said to me, 'Let us go to the house of the LORD.' — one of the fifteen Psalms of Ascent"),
      ("1 Corinthians 15:5", "And that he appeared to Cephas, and then to the Twelve.")],
     [("G1176", "Deka (Ten)"), ("G4002", "Pente (Five)"), ("G652", "Apostolos (Apostle)")]),

    (1179, "Δεκάπολις", "Dekapolis", "Proper Noun (region)", "Decapolis; The Ten Cities",
     "The Decapolis — a league of ten (later more) Hellenistic cities in the region of modern-day Jordan, Syria, and northern Israel. Jesus ministered extensively in the Decapolis territory, reaching Gentile populations.",
     "The Decapolis was a cluster of largely Gentile, Greek-speaking cities established following Alexander the Great's conquests. Jesus' ministry in this region is significant: the healing of the demon-possessed man (Mark 5:20 — 'the man went away and began to tell in the <em>Decapolis</em> how much Jesus had done for him'), the healing of a deaf man (Mark 7:31-37), and the great crowd that came 'from the Decapolis' to hear Jesus (Matthew 4:25). The Decapolis healings foreshadow the universal scope of the gospel — that Jesus came not only for the lost sheep of Israel but for all nations. The healed demoniac became the first missionary to a Gentile region, sent by Jesus to 'go home to your own people.'",
     [("Mark 5:20", "So the man went away and began to tell in the <em>Decapolis</em> how much Jesus had done for him. And all the people were amazed."),
      ("Matthew 4:25", "Large crowds from Galilee, the <em>Decapolis</em>, Jerusalem, Judea and the region across the Jordan followed him."),
      ("Mark 7:31", "Then Jesus left the vicinity of Tyre and went through Sidon, down to the Sea of Galilee and into the region of the <em>Decapolis</em>."),
      ("Mark 5:19", "Jesus did not let him, but said, 'Go home to your own people and tell them how much the Lord has done for you, and how he has had mercy on you.'"),
      ("Matthew 28:19", "Therefore go and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit.")],
     [("G1176", "Deka (Ten)"), ("G4172", "Polis (City)"), ("G2097", "Euangelizō (To Preach the Gospel)")]),

    (1180, "δεκατέσσαρες", "Dekatessares", "Numeral", "Fourteen",
     "The number fourteen — used by Matthew to structure the genealogy of Jesus in three sets of fourteen generations (Matthew 1:17), and by Paul to mark fourteen years between his conversion and his second Jerusalem visit (Galatians 2:1).",
     "Matthew's structuring of Jesus' genealogy into three groups of fourteen (Matthew 1:1-17) is a deliberate theological pattern. In Hebrew numerology, the name 'David' (דוד) has a numerical value of fourteen (4+6+4). Matthew's three-fourteen structure is a triple declaration that Jesus is the Son of David — the Messianic King. The genealogy spans from Abraham to David (14), from David to the Babylonian exile (14), and from the exile to Christ (14) — tracing the whole sweep of covenant history. Paul's fourteen-year gap (Galatians 2:1) underscores that his apostleship and gospel were received independently before being confirmed by the Jerusalem pillars.",
     [("Matthew 1:17", "Thus there were <em>fourteen</em> generations in all from Abraham to David, <em>fourteen</em> from David to the exile to Babylon, and <em>fourteen</em> from the exile to the Messiah."),
      ("Galatians 2:1", "Then after <em>fourteen</em> years, I went up again to Jerusalem, this time with Barnabas. I took Titus along also."),
      ("2 Corinthians 12:2", "I know a man in Christ who <em>fourteen</em> years ago was caught up to the third heaven."),
      ("Matthew 1:1", "This is the genealogy of Jesus the Messiah the son of David, the son of Abraham."),
      ("Romans 1:3", "Regarding his Son, who as to his earthly life was a descendant of David.")],
     [("G1176", "Deka (Ten)"), ("G5064", "Tessares (Four)"), ("G1138", "David (David)")]),

    (1182, "δέκατος", "Dekatos", "Adjective/Ordinal", "Tenth",
     "The ordinal 'tenth' — marking the tenth position in a series. In John 1:39, the disciples first stayed with Jesus beginning at the tenth hour (approximately 4 PM), marking the beginning of Christian formation.",
     "The disciples' question 'Where are you staying?' (John 1:38) and Jesus' answer 'Come and see,' followed by a stay beginning at the <em>tenth</em> hour, marks the beginning of discipleship as unhurried time in the presence of Jesus. This 'come and see' invitation is the pattern of all Christian formation: not a lecture but a dwelling. The disciples who asked 'where?' became the apostles who knew 'who.' In Revelation, the <em>tenth</em> stone of the New Jerusalem's foundation and the falling of a <em>tenth</em> of the city extend the number's significance into eschatology.",
     [("John 1:39", "Come and see, Jesus replied. So they went and saw where he was staying, and they spent that day with him. It was about four in the afternoon (the <em>tenth</em> hour)."),
      ("Revelation 11:13", "At that very hour there was a severe earthquake and a <em>tenth</em> of the city collapsed."),
      ("Revelation 21:20", "The fifth sardonyx, the sixth carnelian, the seventh chrysolite, the eighth beryl, the ninth topaz, the <em>tenth</em> turquoise."),
      ("Leviticus 16:29", "This is to be a lasting ordinance for you: On the <em>tenth</em> day of the seventh month you must deny yourselves."),
      ("John 1:38", "Turning around, Jesus saw them following and asked, 'What do you want?' They said, 'Rabbi, where are you staying?'")],
     [("G1176", "Deka (Ten)"), ("G1181", "Dekatē (Tithe)"), ("G3391", "Mia (One/First)")]),

    (1191, "Δέρβη", "Derbē", "Proper Noun (city)", "Derbe (City in Asia Minor)",
     "Derbe — an ancient city in the region of Lycaonia in Asia Minor (modern-day Turkey). Paul and Barnabas visited Derbe on the first missionary journey, and Paul returned on subsequent journeys. Timothy's companion Gaius was from Derbe.",
     "Derbe is the easternmost point of Paul's first missionary journey before turning back (Acts 14:6, 20). After being stoned and left for dead in Lystra, Paul traveled to Derbe where he and Barnabas 'preached the gospel in that city and won a large number of disciples.' The fact that Paul returned through Derbe on his way back (Acts 14:21) — revisiting the same cities that had persecuted him — illustrates the theology of Acts: suffering does not stop the missionary advance, it confirms it. Derbe produced at least one notable disciple, Gaius (Acts 20:4), who traveled with Paul to Jerusalem.",
     [("Acts 14:6", "They fled to the Lycaonian cities of Lystra and <em>Derbe</em> and to the surrounding country."),
      ("Acts 14:20", "After the disciples had gathered around him, he got up and went back into the city. The next day he and Barnabas left for <em>Derbe</em>."),
      ("Acts 14:21", "They preached the gospel in that city and won a large number of disciples. Then they returned to Lystra, Iconium and Antioch."),
      ("Acts 20:4", "He was accompanied by Sopater son of Pyrrhus from Berea, Aristarchus and Secundus from Thessalonica, Gaius from <em>Derbe</em>, Timothy also."),
      ("2 Timothy 3:11", "Persecutions, sufferings — what kinds of things happened to me in Antioch, Iconium and Lystra, the persecutions I endured.")],
     [("G3070", "Lystra (Lystra)"), ("G3972", "Paulos (Paul)"), ("G5095", "Timotheos (Timothy)")]),

    (1192, "δέρμα", "Derma", "Noun, neuter", "Skin; Hide; Leather",
     "Skin or hide — particularly animal skin used as clothing or covering. In Hebrews 11:37, the faithful of old wandered 'in sheepskins and goatskins' (<em>derma</em>), describing the destitution of those who refused to compromise their faith.",
     "The heroes of Hebrews 11 — the great 'faith hall of fame' — include those who wore animal skins while wandering in caves and deserts, 'of whom the world was not worthy.' The <em>derma</em> clothing of these faith-heroes echoes John the Baptist's garment of camel's hair and a leather belt (Matthew 3:4; Mark 1:6 uses the related word) — the uniform of the prophet who has given up worldly comfort for faithfulness. In Eden, God clothed Adam and Eve in <em>or</em> (animal skins, H5785) after their fall — the first sacrifice, the first covering of shame. From Eden to the wilderness wanderers to John the Baptist, skin-clothing marks those who dwell outside the city of human comfort, waiting for the city whose architect and builder is God (Hebrews 11:10).",
     [("Hebrews 11:37", "They were put to death by stoning; they were sawed in two; they were killed by the sword. They went about in sheepskins and goatskins (<em>derma</em>), destitute, persecuted and mistreated."),
      ("Matthew 3:4", "John's clothes were made of camel's hair, and he had a leather belt around his waist."),
      ("Genesis 3:21", "The LORD God made garments of skin for Adam and his wife and clothed them."),
      ("Hebrews 11:38", "The world was not worthy of them. They wandered in deserts and mountains, living in caves and in holes in the ground."),
      ("Hebrews 11:10", "For he was looking forward to the city with foundations, whose architect and builder is God.")],
     [("G1193", "Dermatinos (Made of Leather)"), ("G2439", "Himatizō (To Clothe)"), ("G4102", "Pistis (Faith)")]),

    (1195, "δεσμεύω", "Desmeouō", "Verb", "To Bind; To Tie Up; To Fetter",
     "To bind, tie, or fetter — used of physically binding someone with ropes or chains, and metaphorically of the Pharisees binding heavy religious burdens on people. Jesus uses this word in His condemnation of religious legalism.",
     "In Matthew 23:4, Jesus condemns the scribes and Pharisees who 'tie up heavy, cumbersome loads and put them on other people's shoulders, but they themselves are not willing to lift a finger to move them.' The <em>desmeouō</em> of legalism — binding burdens onto people — is one of Jesus' most searching critiques of religion divorced from grace. The contrast is explicit in Matthew 11:28-30: 'Come to me, all you who are weary and burdened, and I will give you rest. Take my yoke upon you and learn from me, for I am gentle and humble in heart, and you will find rest for your souls. For my yoke is easy and my burden is light.' Christ unties what religious systems bind.",
     [("Matthew 23:4", "They tie up heavy, cumbersome loads (<em>bind</em>) and put them on other people's shoulders, but they themselves are not willing to lift a finger to move them."),
      ("Acts 22:4", "I persecuted the followers of this Way to their death, arresting both men and women and throwing them into prison."),
      ("Matthew 11:28", "Come to me, all you who are weary and burdened, and I will give you rest."),
      ("Luke 13:16", "Then should not this woman, a daughter of Abraham, whom Satan has kept <em>bound</em> for eighteen long years, be set free on the Sabbath day from what bound her?"),
      ("Galatians 5:1", "It is for freedom that Christ has set us free. Stand firm, then, and do not let yourselves be burdened again by a yoke of slavery.")],
     [("G1199", "Desmon (Bond/Chain)"), ("G3089", "Lyō (To Loose/Set Free)"), ("G2198", "Zaō (To Live)")]),

    (1196, "δεσμέω", "Desmeō", "Verb", "To Bind; To Keep in Bonds",
     "To bind or keep in bonds — nearly synonymous with <em>desmeouō</em> but used of specific binding circumstances: the bound demoniac in Luke 8, those bound by religious law, and eschatological binding of the adversary.",
     "In Luke 8:29, the Gadarene demoniac was bound with chains and under guard but 'broke his bonds' in supernatural strength. When Jesus encountered him, the man was freed with a word — all the chains of the community could not hold what Jesus could release in an instant. This is the theology of <em>desmeō</em>: human chains cannot hold what demonic power sustains; but demonic power cannot hold what divine authority releases. Revelation 20:2 uses a related word for the binding of Satan — the ultimate eschatological <em>desmeō</em>, when the accuser is chained for a thousand years.",
     [("Luke 8:29", "For Jesus had commanded the impure spirit to come out of the man. Many times it had seized him, and though he was chained hand and foot and kept under guard, he had broken his chains."),
      ("Acts 9:14", "And he has come here with authority from the chief priests to arrest all who call on your name."),
      ("Acts 22:29", "Those who were about to interrogate him withdrew immediately. The commander himself was alarmed when he realized that he had put Paul, a Roman citizen, in chains (<em>desmeuō</em>)."),
      ("Revelation 20:2", "He seized the dragon, that ancient serpent, who is the devil, or Satan, and bound him for a thousand years."),
      ("Isaiah 49:24", "Can plunder be taken from warriors, or captives be rescued from the fierce?")],
     [("G1199", "Desmon (Bond/Chain)"), ("G1195", "Desmeouō (To Bind)"), ("G3089", "Lyō (To Loose)")]),

    (1197, "δέσμη", "Desmē", "Noun, feminine", "Bundle; Sheaf; Bunch",
     "A bundle or sheaf — something bound together. Jesus uses <em>d