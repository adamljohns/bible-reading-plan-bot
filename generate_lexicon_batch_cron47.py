#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch"""
import os, json

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
    <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="position:fixed;top:12px;right:12px;z-index:9999;display:flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
        <span style="width:18px;text-align:center;">🌙</span>
        <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
        <span style="width:18px;text-align:center;">☀️</span>
    </div>"""

def make_page(strongs_id, lang, script, translit, pos, gloss, short_def, definition, theology, verses, related):
    """verses = list of (ref, text), related = list of (strongs_id, label)"""
    lang_label = "Hebrew · Old Testament" if lang == "H" else "Greek · New Testament"
    num = strongs_id[1:]
    title = f"{strongs_id} — {translit} ({gloss})"
    ext_base = num.lower() if lang == "G" else num
    ext_lang = "greek" if lang == "G" else "hebrew"
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

# ===== HEBREW ENTRIES =====
hebrew_words = [
    # (strongs_num, script, translit, pos, gloss, short_def, full_def, theology, verses, related)
    (1347, "גָּאוֹן", "Gaon", "Noun, masculine", "Majesty; Arrogance",
     "Pride, excellence, majesty, or arrogance depending on context.",
     "The Hebrew <em>gaon</em> derives from the root <em>ga'ah</em> (H1342), meaning to rise up or be exalted. It carries a dual meaning: the legitimate majesty and excellency of God, and the sinful pride of humans who exalt themselves against Him. Used of the <em>gaon</em> of Jordan (the thicket/pride of the Jordan River), and of God's own majestic excellency.",
     "In Scripture, <em>gaon</em> captures a tension at the heart of theology: majesty belongs to God alone (Psalm 68:34), yet humanity tends to seize that glory for itself. Isaiah warns repeatedly against the pride of nations and individuals (Isaiah 13:11; 16:6). When <em>gaon</em> describes God, it speaks of His incomparable exaltation and splendor. The same word used of human pride becomes a warning against the creature usurping the Creator's glory.",
     [("Psalm 68:34", "Ascribe power to God, whose <em>majesty</em> is over Israel, whose power is in the heavens."),
      ("Isaiah 13:11", "I will put an end to the <em>arrogance</em> of the haughty and lay low the pride of the ruthless."),
      ("Amos 8:7", "The LORD has sworn by the <em>Pride</em> of Jacob: I will never forget anything they have done."),
      ("Jeremiah 12:5", "How can you compete with horses? If you stumble in safe country, how will you manage in the <em>thickets</em> by the Jordan?"),
      ("Ezekiel 16:49", "Now this was the sin of your sister Sodom: She and her daughters were arrogant, overfed and unconcerned — this was their <em>pride</em>.")],
     [("H1342", "Ga'ah (To Rise Up)"), ("H1346", "Ga'avah (Pride)"), ("H1348", "Ge'uth (Majesty)")]),

    (2490, "חָלַל", "Chalal", "Verb", "To Pierce; To Profane",
     "To bore through, pierce, wound mortally; also to defile, pollute, or profane what is holy.",
     "The Hebrew <em>chalal</em> encompasses two related meanings. First, physically: to pierce or wound so severely as to cause death — used of slain soldiers and the gravely wounded. Second, spiritually: to profane or defile that which is consecrated — the Sabbath, the name of God, the holy sanctuary. Both meanings involve a violation of integrity, whether of body or of holiness.",
     "<em>Chalal</em> is pivotal in Isaiah 53:5 — 'He was <em>pierced</em> for our transgressions' — one of the most profound messianic prophecies in the entire Hebrew Bible. The Suffering Servant absorbs the chalal — the fatal wounding — that our sins deserve. Additionally, God warns throughout the Law and Prophets against <em>chalal</em>-ing His holy name (Leviticus 18:21; Ezekiel 36:20-23), treating as common what He has set apart.",
     [("Isaiah 53:5", "But he was <em>pierced</em> for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his wounds we are healed."),
      ("Psalm 109:22", "For I am poor and needy, and my heart is <em>wounded</em> within me."),
      ("Ezekiel 36:23", "I will show the holiness of my great name, which has been <em>profaned</em> among the nations, the name you have profaned among them."),
      ("Leviticus 21:12", "He must not leave the sanctuary of his God or <em>desecrate</em> it, because he has been dedicated by the anointing oil of his God."),
      ("Numbers 30:2", "When a man makes a vow to the LORD or takes an oath to obligate himself by a pledge, he must not break his word or <em>profane</em> it.")],
     [("H2491", "Chalal (Pierced/Slain)"), ("H2491", "Chalal (Slain)"), ("H6944", "Qodesh (Holiness)")]),

    (2764, "חֵרֶם", "Cherem", "Noun, masculine", "Devoted to Destruction; Sacred Ban",
     "Something irrevocably devoted to God — either for total destruction or for consecrated service.",
     "The Hebrew <em>cherem</em> describes the most extreme form of dedication — an object or person placed entirely under divine claim. In the context of holy war (<em>milchamah</em>), entire cities and populations were <em>cherem</em> — utterly devoted to destruction, none of the plunder to be taken for personal use (Joshua 6:17-18). To violate the <em>cherem</em> was catastrophic, as Achan discovered. In another sense, things devoted to God in the Temple could also be <em>cherem</em> — permanently sanctified and irredeemable.",
     "The theology of <em>cherem</em> reveals God's absolute sovereignty over life and property. When He declared something <em>cherem</em>, no human calculation of value could override that decree. Achan's sin in taking devoted things (Joshua 7) brought disaster on all Israel, illustrating how one person's violation of God's holiness affects the entire community. The concept also prefigures total consecration — offering everything to God without reservation, holding nothing back.",
     [("Joshua 6:17", "The city and all that is in it are to be <em>devoted</em> to the LORD. Only Rahab the prostitute and all who are with her in her house shall be spared."),
      ("Deuteronomy 7:26", "Do not bring a <em>detestable thing</em> into your house or you, like it, will be set apart for destruction. Regard it as vile and utterly detest it."),
      ("1 Samuel 15:21", "The soldiers took sheep and cattle from the plunder, the best of what was <em>devoted to God</em>, in order to sacrifice them."),
      ("Leviticus 27:28", "But nothing that a person owns and <em>devotes to the LORD</em> — whether a human being or an animal or family land — may be sold or redeemed."),
      ("Isaiah 34:5", "My sword has drunk its fill in the heavens; see, it descends in judgment on Edom, the people I have <em>totally destroyed</em>.")],
     [("H2763", "Charam (To Devote/Destroy)"), ("H6944", "Qodesh (Holy)"), ("H4421", "Milchamah (War)")]),

    (2860, "חָתָן", "Chathan", "Noun, masculine", "Bridegroom; Son-in-Law",
     "A bridegroom or son-in-law; one related by marriage.",
     "The Hebrew <em>chathan</em> refers primarily to a bridegroom — the man who has just entered the covenant of marriage. It is related to the verb <em>chathan</em> (to become a son-in-law by circumcision, in ancient cognates). The bridegroom imagery is rich throughout the Old Testament, often used as a metaphor for joy, youth, and the intimate covenant relationship between God and His people.",
     "The image of the bridegroom permeates biblical theology from beginning to end. God describes His relationship to Israel in marital terms (Isaiah 62:5; Hosea 2:19-20). The Psalmist compares the sun to a <em>chathan</em> coming out of his chamber with joy (Psalm 19:5). This imagery reaches its climax in the New Testament where Christ is revealed as the ultimate Bridegroom (Matthew 25:1-13; Revelation 19:7-9) and the Church as His bride. Understanding <em>chathan</em> helps unlock the covenant love that unites the entire biblical narrative.",
     [("Isaiah 62:5", "As a young man marries a young woman, so will your Builder marry you; as a <em>bridegroom</em> rejoices over his bride, so will your God rejoice over you."),
      ("Psalm 19:5", "It is like a <em>bridegroom</em> coming out of his chamber, like a champion rejoicing to run his course."),
      ("Joel 2:16", "Gather the people, consecrate the assembly; bring together the elders, gather the children, those nursing at the breast. Let the <em>bridegroom</em> leave his room."),
      ("Jeremiah 7:34", "I will bring an end to the sounds of joy and gladness and to the voices of <em>bride and bridegroom</em> in the towns of Judah."),
      ("Song of Songs 3:11", "Come out, you daughters of Zion, and look at King Solomon wearing his crown, the crown with which his mother crowned him on his wedding day, the day his heart rejoiced.")],
     [("H3618", "Kallah (Bride)"), ("H157", "Ahav (Love)"), ("H1285", "Berith (Covenant)")]),

    (3391, "יֶרַח", "Yerach", "Noun, masculine", "Month; Moon",
     "A month (lunar period); also the moon itself.",
     "The Hebrew <em>yerach</em> refers to the lunar month, the basic unit of the Hebrew calendar. The Hebrew calendar is fundamentally lunar, with each month beginning at the new moon. <em>Yerach</em> appears alongside <em>chodesh</em> (H2320, the new moon/month) as a near-synonym, though <em>yerach</em> more specifically emphasizes the full lunar cycle. The moon (<em>yareah</em>) and the month it measures were central to Israelite worship, governing feast days, Sabbaths, and the agricultural year.",
     "Israel's sacred calendar was divinely structured around the moon's cycles (Genesis 1:14 — lights for signs, seasons, days, years). New Moon celebrations were significant worship occasions (Numbers 10:10; 28:11-15). Psalms 104:19 declares God made the moon for appointed seasons. The Passover, Pentecost, and Feast of Tabernacles were all governed by lunar dating. In this way <em>yerach</em> connects astronomical order to the covenant community's rhythm of worship and life.",
     [("Genesis 1:14", "And God said, 'Let there be lights in the vault of the sky to separate the day from the night, and let them serve as signs to mark sacred times, and days and years.'"),
      ("Psalm 104:19", "He made the moon to mark the seasons, and the sun knows when to go down."),
      ("Numbers 28:14", "With each bull there is to be a drink offering of half a hin of wine; with a ram, a third of a hin; and with a lamb, a quarter of a hin. This is the monthly burnt offering for each <em>month</em> of the year."),
      ("Deuteronomy 33:14", "With the best gifts of the earth and its fullness and the favor of him who dwelt in the burning bush. Let all these rest on the head of Joseph, on the brow of the prince among his brothers."),
      ("1 Kings 6:37", "The foundation of the temple of the LORD was laid in the fourth year, in the <em>month</em> of Ziv.")],
     [("H2320", "Chodesh (New Moon/Month)"), ("H3394", "Yareah (Moon)"), ("H4150", "Moed (Appointed Time)")]),

    (4180, "מוֹרָשׁ", "Morash", "Noun, masculine", "Possession; Inheritance",
     "A possession; something seized and held; an inheritance or estate.",
     "The Hebrew <em>morash</em> (also <em>morashah</em>) comes from the root <em>yarash</em> (H3423), meaning to seize, dispossess, or inherit. It describes a possession held by right — something that belongs to you either through conquest, inheritance, or divine grant. Closely related to <em>nachalah</em> (H5159, inheritance), <em>morash</em> often emphasizes the legal and covenantal right to hold the land.",
     "The land of Canaan was described as <em>morash</em> — Israel's God-given possession (Deuteronomy 33:4; Ezekiel 11:15). Moses' Torah was called <em>morashah</em> — the inheritance of the congregation of Jacob (Deuteronomy 33:4). This rich concept ties together land theology, covenantal promise, and the principle that God is the ultimate landowner who grants to His people what is theirs by grace. The Church inherits a spiritual <em>morash</em> — the kingdom of God.",
     [("Deuteronomy 33:4", "Moses gave us the law, an <em>inheritance</em> for the assembly of Jacob."),
      ("Ezekiel 11:15", "Son of man, the people of Jerusalem have said of your fellow exiles and all the other Israelites, 'They are far away from the LORD; this land was given to us as our <em>possession</em>.'"),
      ("Ezekiel 33:24", "Abraham was only one man, yet he <em>possessed</em> the land. But we are many; surely the land has been given to us as our <em>possession</em>."),
      ("Obadiah 17", "But on Mount Zion will be deliverance; it will be holy, and Jacob will <em>possess</em> his <em>inheritance</em>."),
      ("Isaiah 14:23", "I will turn her into a place for owls and into swampland; I will sweep her with the broom of destruction, declares the LORD Almighty.")],
     [("H3423", "Yarash (To Inherit)"), ("H5159", "Nachalah (Inheritance)"), ("H776", "Erets (Land)")]),

    (4539, "מָסָךְ", "Masak", "Noun, masculine", "Curtain; Screen; Covering",
     "A covering, screen, or curtain — especially the hanging at the entrance of the Tabernacle.",
     "The Hebrew <em>masak</em> refers specifically to the woven screen or curtain that covered the entrance to the Tabernacle's outer court, the Holy Place, and the Holy of Holies. It comes from the root <em>sakak</em> (H5526), meaning to cover or screen. These curtains were crafted of fine linen and were embroidered with blue, purple, and scarlet yarn — visually magnificent yet serving a barrier function, separating the holy from the common.",
     "The <em>masak</em> curtains of the Tabernacle (Exodus 26:36; 27:16) speak profoundly of access and separation. The veil separating humanity from God's presence was not a permanent barrier but a divinely appointed boundary awaiting the right time and the right Mediator. The tearing of the Temple veil at the crucifixion (Matthew 27:51) was the fulfillment of everything the <em>masak</em> pointed toward — Christ's flesh torn open to give us direct access to the Father (Hebrews 10:20).",
     [("Exodus 26:36", "For the entrance to the tent make a <em>curtain</em> of blue, purple and scarlet yarn and finely twisted linen — the work of an embroiderer."),
      ("Exodus 27:16", "For the entrance to the courtyard, provide a <em>curtain</em> twenty cubits long, of blue, purple and scarlet yarn and finely twisted linen."),
      ("Numbers 3:31", "Their care of the ark, the table, the lampstand, the altars, the articles of the sanctuary used in ministering, the <em>curtain</em>, and everything related to their use."),
      ("Numbers 4:25", "They are to carry the curtains of the tabernacle and the tent of meeting, its covering and the outer covering of hides of sea cows, the <em>curtains</em> for the entrance to the tent of meeting."),
      ("Isaiah 22:8", "The <em>defenses</em> of Judah are stripped away. And you looked in that day to the weapons in the Palace of the Forest.")],
     [("H6532", "Poreketh (Veil/Inner Curtain)"), ("H168", "Ohel (Tent)"), ("H4908", "Mishkan (Tabernacle)")]),

    (5110, "נוּד", "Nuwd", "Verb", "To Lament; To Wander; To Show Grief",
     "To shake or move; to show grief or sympathy; to wander; to console or comfort another.",
     "The Hebrew <em>nuwd</em> has a fascinating range of meanings all connected by the idea of movement in response to grief. It can mean to move one's head in sorrow or sympathy (as a sign of condolence), to wander as a fugitive, or to console and express compassion. When friends visited Job, the text says they came to 'nuwd' him — to mourn with him and comfort him (Job 2:11). The wandering sense appears in Cain's curse of being a 'nod' (wanderer).",
     "The ministry of presence in grief is captured by <em>nuwd</em>. When Scripture says to 'mourn with those who mourn' (Romans 12:15), the OT background is this word — the physical act of nodding, weeping, and sitting with the suffering. <em>Nuwd</em> also appears in prophetic laments over fallen cities, where the ruins are mocked rather than mourned — a mark of the deepest contempt (Jeremiah 18:16). Conversely, when God's people suffered, the lack of <em>nuwd</em>-ers was itself a judgment (Psalm 69:20).",
     [("Job 2:11", "When Job's three friends heard about all the troubles that had come upon him, they set out from their homes and met together by agreement to go and <em>sympathize</em> with him and comfort him."),
      ("Psalm 69:20", "Scorn has broken my heart and has left me helpless; I looked for sympathy, but there was none, for <em>comforters</em>, but I found none."),
      ("Jeremiah 18:16", "Their land will be laid waste, an object of lasting scorn; all who pass by will be appalled and will <em>shake their heads</em>."),
      ("Jeremiah 15:5", "Who will have pity on you, Jerusalem? Who will <em>mourn for you</em>? Who will stop to ask how you are?"),
      ("Genesis 4:12", "When you work the ground, it will no longer yield its crops for you. You will be a restless <em>wanderer</em> on the earth.")],
     [("H5162", "Nacham (To Comfort)"), ("H56", "Abal (To Mourn)"), ("H1058", "Bakah (To Weep)")]),

    (5164, "נֹחַם", "Nocham", "Noun, masculine", "Repentance; Consolation; Comfort",
     "Repentance or consolation; a change of mind producing comfort or regret.",
     "The Hebrew <em>nocham</em> is the noun form of <em>nacham</em> (H5162), meaning to be comforted or to repent. It appears rarely in the Old Testament but carries the full theological weight of its verbal root — the concept of a deep inner change that moves from grief to comfort, or from one course of action to another. In Hosea 13:14, God declares He will have no <em>nocham</em> from bringing redemption — His resolve is fixed.",
     "<em>Nocham</em> sits at the intersection of divine pathos and covenant faithfulness. When God 'repents' (nacham/nocham) in Scripture, it is not a sign of divine error but of responsive love — His covenant heart responding to human repentance or stubbornness. This concept is foundational to understanding a God who is not static but dynamically engaged with His creation, grieving over sin while determined to bring comfort and redemption to those who turn to Him.",
     [("Hosea 13:14", "I will deliver this people from the power of the grave; I will redeem them from death. Where, O death, are your plagues? Where, O grave, is your destruction? I will have no <em>compassion</em>."),
      ("Isaiah 57:18", "I have seen their ways, but I will heal them; I will guide them and restore <em>comfort</em> to Israel's mourners."),
      ("Jeremiah 16:7", "No one will offer food to comfort those who mourn for the dead — not even for a father or a mother — nor will anyone give them a drink of <em>consolation</em>."),
      ("Zechariah 1:13", "So the LORD spoke kind and <em>comforting</em> words to the angel who talked with me."),
      ("Psalm 119:52", "I remember, LORD, your ancient laws, and I find <em>comfort</em> in them.")],
     [("H5162", "Nacham (To Comfort)"), ("H8575", "Tanchumim (Consolations)"), ("H3068", "YHWH (The LORD)")]),

    (5391, "נָשַׁךְ", "Nashak", "Verb", "To Bite; To Charge Interest",
     "To bite like a serpent; to lend on interest; to exact usury.",
     "The Hebrew <em>nashak</em> has two distinct applications unified by the idea of harmful extraction. Literally it means to bite — used of a serpent's fatal bite (Numbers 21:6-9) and of a whip's sting. Figuratively, it describes the practice of charging interest on loans, particularly to fellow Israelites — a practice condemned throughout the Law because it 'bites' the borrower into deeper poverty. The imagery is graphic: usury is likened to a venomous serpent.",
     "The connection between <em>nashak</em> (to bite) and lending at interest reveals God's economic ethics. The Torah forbade charging interest to fellow Israelites (Exodus 22:25; Leviticus 25:36-37) — lending was to be an act of covenant solidarity, not profit extraction. The prophets condemned usury as oppression of the poor (Ezekiel 18:8, 13; 22:12). The serpent that bites economically is as dangerous as the one in the wilderness. Conversely, the bronze serpent lifted by Moses (Numbers 21:9) — a type of Christ — healed those bitten, pointing to redemption from every curse.",
     [("Numbers 21:6", "Then the LORD sent venomous snakes among them; they <em>bit</em> the people and many Israelites died."),
      ("Exodus 22:25", "If you lend money to one of my people among you who is needy, do not treat it like a business deal; charge no <em>interest</em>."),
      ("Habakkuk 2:7", "Will not your creditors suddenly arise? Will they not wake up and make you tremble? Then you will become their prey. Because you have plundered many nations, the peoples who are left will plunder you."),
      ("Ezekiel 18:8", "He does not lend to them at <em>interest</em> or take a profit from them. He withholds his hand from doing wrong and judges fairly between two parties."),
      ("Psalm 15:5", "Who lends money to the poor without <em>interest</em>; who does not accept a bribe against the innocent. Whoever does these things will never be shaken.")],
     [("H5383", "Nasha (To Lend)"), ("H1215", "Betsa (Unjust Gain)"), ("H4855", "Mashsha (Usury)")]),

    (5534, "סָכַר", "Sakar", "Verb", "To Shut Up; To Close; To Hand Over",
     "To stop up, close, or barricade; to deliver up or surrender to an enemy.",
     "The Hebrew <em>sakar</em> appears rarely but significantly. It means to shut or close — barricading a passage or stopping it up. In some instances it carries the sense of delivering someone up or surrendering them, as when the men of Keilah were going to 'sakar' David into Saul's hands (1 Samuel 23:12). The word captures the idea of sealing off any escape — complete enclosure or entrapment.",
     "The concept of being 'shut in' or 'handed over' carries deep theological resonance. God sometimes shuts up enemies (1 Samuel 23:11), delivering them into the hands of His servants. The flip side is the fear of being handed over to one's enemies — a theme of lament and petition throughout the Psalms. Understanding <em>sakar</em> helps illuminate passages about divine protection (God closing the way of danger) versus divine judgment (God surrendering the rebellious to the consequences of their sin).",
     [("1 Samuel 23:11", "Will the citizens of Keilah <em>surrender</em> me to him? Will Saul come down, as your servant has heard? LORD, God of Israel, tell your servant. And the LORD said, 'He will come down.'"),
      ("1 Samuel 23:12", "Again David asked, 'Will the citizens of Keilah <em>surrender</em> me and my men to Saul?' And the LORD said, 'They will.'"),
      ("Deuteronomy 32:30", "How could one man chase a thousand, or two put ten thousand to flight, unless their Rock had <em>sold</em> them, unless the LORD had given them up?"),
      ("Judges 16:18", "When Delilah saw that he had told her everything, she sent word to the rulers of the Philistines, 'Come back once more; he has told me everything.' So the rulers of the Philistines returned with the silver in their hands."),
      ("Psalm 44:12", "You sold your people for a pittance, gaining nothing from their sale.")],
     [("H5462", "Sagar (To Shut)"), ("H4042", "Magan (To Deliver Up)"), ("H3027", "Yad (Hand)")]),

    (5688, "עָבֹת", "Avoth", "Noun, masculine/plural", "Thick Cords; Ropes; Braided Branches",
     "Intertwined cords, braided ropes, or dense woven branches.",
     "The Hebrew <em>avoth</em> (plural of <em>avat</em>) refers to thick, braided, interwoven cords or ropes — the kind used for restraining animals, hanging the Temple lamp, or describing the intertwined branches of a thick tree. The image is of multiple strands twisted together for strength. Samson was bound with such cords (Judges 15:13-14). The cherubim of the Temple had interwoven chain-work. The word captures the idea of strength through structure — multiple elements woven into one.",
     "The imagery of <em>avoth</em> speaks to covenantal binding. Ecclesiastes 4:12 says 'a cord of three strands is not quickly broken' — the principle that unity and interweaving creates strength that single strands cannot provide. God's bonds upon His people are described with this language — not as oppressive imprisonment but as life-giving connection. The cords of love and the cords of human kinship (Hosea 11:4) mirror this concept.",
     [("Judges 15:13", "They answered him, 'No, we only want to tie you up and hand you over to them.' They will not kill you.' So they bound him with two new <em>ropes</em> and led him up from the rock."),
      ("Psalm 2:3", "Let us break their chains and throw off their <em>shackles</em>."),
      ("Ezekiel 19:11", "Its branches were strong, fit for a ruler's scepter. It towered high above the thick foliage, conspicuous for its height and for its many <em>branches</em>."),
      ("Job 39:10", "Can you hold him to the furrow with a harness? Will he till the valleys behind you? Can you bind a wild donkey with his <em>ropes</em>?"),
      ("Ecclesiastes 4:12", "Though one may be overpowered, two can defend themselves. A <em>cord</em> of three strands is not quickly broken.")],
     [("H2256", "Chevel (Rope/Band)"), ("H4147", "Moser (Bond)"), ("H631", "Asar (To Bind)")]),

    (5742, "עָדָשׁ", "Adash", "Noun, masculine", "Lentils",
     "Lentils — the edible legume seeds of the lentil plant.",
     "The Hebrew <em>adash</em> refers to lentils, a staple legume in the ancient Near East. Small red or green lentil seeds were made into a thick, red-brown pottage. Lentils appear at one of the most dramatic moments in biblical narrative — Esau's fateful trade of his birthright to Jacob for a bowl of red lentil stew (Genesis 25:29-34). They also appear as part of the provisions brought to David at Mahanaim (2 Samuel 17:28) and in Ezekiel's symbolic bread (Ezekiel 4:9).",
     "The bowl of lentil stew in Genesis 25 is far more than a culinary detail. Esau's willingness to exchange his <em>birthright</em> (the covenantal inheritance passing through Abraham and Isaac) for immediate physical gratification became a defining moment in redemptive history. Hebrews 12:16 warns against being like Esau — profane, trading eternal inheritance for momentary appetite. The lentils symbolize the danger of valuing the temporal over the eternal, the satisfying of flesh over covenant faithfulness.",
     [("Genesis 25:34", "Then Jacob gave Esau some bread and some <em>lentil</em> stew. He ate and drank, and then got up and left. So Esau despised his birthright."),
      ("2 Samuel 23:11", "Next to him was Shammah son of Agee the Hararite. When the Philistines banded together at a place where there was a field full of <em>lentils</em>, Israel's troops fled from them."),
      ("Ezekiel 4:9", "Take wheat and barley, beans and <em>lentils</em>, millet and spelt; put them in a storage jar and use them to make bread for yourself."),
      ("Genesis 25:29", "Once when Jacob was cooking some stew, Esau came in from the open country, famished."),
      ("Hebrews 12:16", "See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son.")],
     [("H1062", "Bekorah (Birthright)"), ("H3290", "Yaaqov (Jacob)"), ("H6215", "Esav (Esau)")]),

    (5937, "עָלַז", "Alaz", "Verb", "To Exult; To Rejoice Triumphantly",
     "To exult, cry out in triumph, or rejoice with great joy.",
     "The Hebrew <em>alaz</em> describes a vigorous, exuberant, often vocal rejoicing — the kind of joy that spills out in triumph and celebration. It is more intense than mere happiness, carrying the connotation of exultation after victory. The word appears in contexts of military triumph, divine salvation, and eschatological celebration. It often describes the rejoicing of God's people after experiencing His deliverance.",
     "<em>Alaz</em> captures the joy of salvation — not a quiet, subdued relief but a triumphant shout. The righteous are called to <em>alaz</em> in the Lord (Psalm 28:7; 68:3). This is the joy of those who know they have been saved by a greater power than their own. In the prophets, <em>alaz</em> anticipates the eschatological celebration when God finally vindicates His people and restores all things. The Christian finds this joy already inaugurated in the resurrection of Christ.",
     [("Psalm 28:7", "The LORD is my strength and my shield; my heart trusts in him, and he helps me. My heart leaps for joy, and with my song I praise him."),
      ("Psalm 68:3", "But may the righteous be glad and <em>rejoice</em> before God; may they be happy and joyful."),
      ("Proverbs 23:24", "The father of a righteous child has great joy; a man who fathers a wise son <em>rejoices</em> in him."),
      ("Isaiah 23:12", "He says, 'No more of your <em>reveling</em>, Virgin Daughter Sidon, now crushed! Up, cross over to Cyprus; even there you will find no rest.'"),
      ("Zephaniah 3:14", "Sing, Daughter Zion; shout aloud, Israel! Be glad and <em>rejoice</em> with all your heart, Daughter Jerusalem!")],
     [("H8055", "Samach (To Rejoice)"), ("H1523", "Giyl (To Rejoice)"), ("H7442", "Ranan (To Shout for Joy)")]),

    (6175, "עָרוּם", "Arum", "Adjective", "Shrewd; Crafty; Prudent",
     "Clever, cunning, crafty; wisely prudent or slyly scheming depending on context.",
     "The Hebrew <em>arum</em> describes a quality of sharp intelligence or shrewdness that can manifest as either wisdom or cunning. The same word describes the serpent in Eden (Genesis 3:1 — 'more crafty than any of the wild animals') and also the wise person who thinks before acting (Proverbs 12:16, 23; 13:16; 14:8, 15). Context determines whether the connotation is positive (prudent, sensible) or negative (scheming, sly). The dual usage is theologically rich.",
     "The Eden narrative uses <em>arum</em> for the serpent's cunning, playing on its similarity to <em>arummim</em> (naked) used of Adam and Eve. The serpent's cleverness exploited their innocence. In Proverbs, the same quality — redirected toward wisdom — becomes a virtue. This duality reflects the biblical view that human capacities are not inherently good or evil; their moral character depends on their direction. Wisdom submitted to God becomes true <em>arum</em>; wisdom turned against God becomes diabolical cunning.",
     [("Genesis 3:1", "Now the serpent was more <em>crafty</em> than any of the wild animals the LORD God had made. He said to the woman, 'Did God really say, You must not eat from any tree in the garden?'"),
      ("Proverbs 12:16", "Fools show their annoyance at once, but the <em>prudent</em> overlook an insult."),
      ("Proverbs 13:16", "All who are <em>prudent</em> act with knowledge, but fools expose their folly."),
      ("Proverbs 14:15", "The simple believe anything, but the <em>prudent</em> give thought to their steps."),
      ("Job 5:12", "He thwarts the plans of the <em>crafty</em>, so that their hands achieve no success.")],
     [("H2449", "Chakam (To Be Wise)"), ("H995", "Bin (To Understand)"), ("H3820", "Lev (Heart/Mind)")]),

    (6482, "פֶּצַע", "Petsa", "Noun, masculine", "Wound; Bruise; Stripe",
     "A wound or bruise inflicted by striking or cutting.",
     "The Hebrew <em>petsa</em> refers to a wound, bruise, or stripe caused by a blow — the physical mark left by beating, lashing, or cutting. It is a vivid, concrete word evoking the visible evidence of violence on a body. This word appears in legal contexts (injury requiring compensation), in wisdom literature (discipline), and most significantly in the great Servant Song of Isaiah 52-53.",
     "Isaiah 53:5 is the theological summit of <em>petsa</em>: 'He was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was upon him, and by his <em>wounds</em> [petsa] we are healed.' The specific word <em>petsa</em> — a visible, physical wound — emphasizes the bodily reality of the Servant's suffering. The wounds that heal are not metaphorical. Peter quotes this passage directly in 1 Peter 2:24, applying it to the crucifixion of Christ. Every stripe on the Servant's body carried the weight of human sin and purchased human healing.",
     [("Isaiah 53:5", "But he was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his <em>wounds</em> we are healed."),
      ("Proverbs 20:30", "Blows and <em>wounds</em> cleanse away evil, and beatings purge the inmost being."),
      ("Proverbs 27:6", "Wounds from a friend can be trusted, but an enemy multiplies kisses."),
      ("Exodus 21:25", "burn for burn, <em>wound</em> for wound, bruise for bruise."),
      ("1 Kings 22:35", "All day long the battle raged, and the king was propped up in his chariot facing the Arameans. The blood from his <em>wound</em> ran onto the floor of the chariot, and that evening he died.")],
     [("H2250", "Chabbuwrah (Bruise/Stripe)"), ("H4347", "Makkah (Blow/Wound)"), ("H7495", "Rapha (To Heal)")]),

    (6544, "פָּרַע", "Para", "Verb", "To Let Loose; To Lead; To Neglect",
     "To loosen, let go, or strip; to act as a leader; to neglect or let go unpunished.",
     "The Hebrew <em>para</em> carries several related meanings around the concept of loosening or letting go. It can mean to uncover or loosen one's hair (as a sign of mourning or defilement), to lead or act as a chief, or to let something go unpunished — to allow disorder by failing to restrain. Moses reproved Aaron for letting the people run <em>para</em> (loose/wild) during the golden calf incident (Exodus 32:25).",
     "The golden calf narrative uses <em>para</em> twice in a single verse — Aaron had 'let them loose' (<em>ki para</em>) among their enemies. This word captures the theological danger of unrestrained freedom — when the covenant community throws off divine order, they don't find liberation but chaos and exposure to their enemies. True freedom in Scripture is not absence of law but freedom within God's ordering. The leader who fails to restrain sin among the people bears responsibility for the resulting disorder.",
     [("Exodus 32:25", "Moses saw that the people were running wild and that Aaron had let them get out of control and so become a laughingstock to their enemies."),
      ("Proverbs 1:25", "Since you <em>disregarded</em> all my advice and did not accept my rebuke."),
      ("Proverbs 4:15", "Avoid it, do not travel on it; turn from it and go on your way."),
      ("Proverbs 8:33", "Listen to my instruction and be wise; do not <em>disregard</em> it."),
      ("Numbers 5:18", "After the priest has had the woman stand before the LORD, he shall loosen (<em>para</em>) her hair and place in her hands the reminder-offering.")],
     [("H7218", "Rosh (Head/Leader)"), ("H5800", "Azab (To Forsake)"), ("H6586", "Pasha (To Transgress)")]),

    (7111, "קְצָפָה", "Qetsaphah", "Noun, feminine", "Wrath; Breaking Off; Chips",
     "Wrath or rage; also broken-off pieces, splinters, or fragments.",
     "The Hebrew <em>qetsaphah</em> derives from <em>qatsaph</em> (H7107), meaning to be angry or burst out in rage. As a noun it can describe God's wrath poured out, or — in one occurrence — the broken-off fragments or chips that result when something is shattered. The word captures the explosive nature of wrath: like something violently broken, shattering into pieces.",
     "Divine wrath in the Old Testament is not mere irritation but <em>qetsaphah</em> — the explosive response of infinite holiness to human covenant breaking. Zechariah 1:15 shows God angry with the nations who exceeded His chastisement of Israel, and earlier generations suffered under God's fierce anger (<em>qetsaphah</em>) in the wilderness. Understanding <em>qetsaphah</em> is essential for grasping the gravity of sin and the wonder of grace — that God's wrath against our sin was absorbed by the Servant (Isaiah 53) rather than poured out on us.",
     [("Zechariah 1:15", "I am very angry with the nations that feel secure. I was only a little angry, but they went too far with the punishment."),
      ("Isaiah 34:2", "The LORD is angry (<em>qetseph</em>) with all nations; his wrath is on all their armies. He will totally destroy them."),
      ("2 Kings 3:27", "There came great <em>wrath</em> against Israel, and they withdrew and returned to their own land."),
      ("Ezra 7:23", "Whatever the God of heaven has prescribed, let it be done with diligence for the temple of the God of heaven. Why should his <em>wrath</em> fall on the realm of the king and of his sons?"),
      ("Isaiah 54:8", "In a surge of anger I hid my face from you for a moment, but with everlasting kindness I will have compassion on you, says the LORD your Redeemer.")],
     [("H7107", "Qatsaph (To Be Angry)"), ("H639", "Aph (Nostril/Anger)"), ("H2534", "Chemah (Wrath/Heat)")]),

    (7305, "רֶוַח", "Revach", "Noun, masculine", "Space; Relief; Breathing Room",
     "Room, space, relief; a broadening or enlarging — freedom to breathe.",
     "The Hebrew <em>revach</em> comes from <em>ravach</em> (H7304), meaning to be wide or spacious, to breathe freely. As a noun it describes the experience of having space — whether physical space between animals to prevent trampling, or the experiential relief that comes when pressure is released. Esther 4:14 famously uses <em>revach</em> — if Esther stays silent, 'relief and deliverance will arise for the Jews from another place,' but she will perish.",
     "The spiritual resonance of <em>revach</em> is profound. Being 'hemmed in' by enemies, circumstances, or sin is a recurrent biblical image of distress. The Psalms often cry out from constricted places (<em>metzar</em> — narrow straits) and praise God for bringing into a 'wide place' (<em>merchab</em>). <em>Revach</em> captures the theological reality of salvation as spaciousness — God making room, lifting pressure, restoring freedom. Esther 4:14 implies that God's purposes never fail — if one instrument refuses, He will make <em>revach</em> through another.",
     [("Esther 4:14", "For if you remain silent at this time, <em>relief and deliverance</em> for the Jews will arise from another place, but you and your father's family will perish."),
      ("Genesis 32:16", "He put them in the care of his servants, each herd by itself, and said to his servants, 'Go ahead of me, and keep some space (<em>revach</em>) between the herds.'"),
      ("Psalm 118:5", "When hard pressed, I cried to the LORD; he brought me into a spacious place."),
      ("Psalm 31:8", "You have not given me into the hands of the enemy but have set my feet in a spacious place."),
      ("Job 36:16", "He is wooing you from the jaws of distress to a spacious place free from restriction.")],
     [("H7304", "Ravach (To Breathe)"), ("H4800", "Merchab (Broad Place)"), ("H3444", "Yeshuah (Salvation)")]),

    (7399, "רְכוּשׁ", "Rekush", "Noun, masculine", "Property; Goods; Substance",
     "Accumulated goods, property, wealth, or substance — movable possessions.",
     "The Hebrew <em>rekush</em> refers to movable property — goods, cattle, and wealth accumulated through labor or acquisition. It appears frequently in narratives of migration and conquest: Abraham left Egypt with great <em>rekush</em> (Genesis 12:5; 13:6), Lot and Abraham's combined <em>rekush</em> was so great the land couldn't support them both, and Israel left Egypt with Egypt's <em>rekush</em> (plunder). The word emphasizes accumulated, portable wealth.",
     "The <em>rekush</em> of the patriarchs represents God's covenant blessing made tangible in history. God promised Abraham He would bless him and make him great (Genesis 12:2), and <em>rekush</em> was one visible sign of that blessing. Yet the same <em>rekush</em> that blessed could also separate — Lot's separation from Abraham was caused by their combined <em>rekush</em> (Genesis 13:6). Wealth is a test of character and stewardship; the question Scripture always asks is what we do with the <em>rekush</em> God has entrusted to us.",
     [("Genesis 12:5", "He took his wife Sarai, his nephew Lot, all the possessions (<em>rekush</em>) they had accumulated and the people they had acquired in Harran."),
      ("Genesis 13:6", "But the land could not support them while they stayed together, for their possessions (<em>rekush</em>) were so great that they were not able to stay together."),
      ("Genesis 15:14", "But I will punish the nation they serve as slaves, and afterward they will come out with great possessions (<em>rekush</em>)."),
      ("2 Chronicles 21:14", "The LORD is about to strike your people, your sons, your wives and everything that is yours, with a heavy blow."),
      ("Ezra 8:21", "There, by the Ahava Canal, I proclaimed a fast, so that we might humble ourselves before our God and ask him for a safe journey for us and our children, with all our possessions (<em>rekush</em>).")],
     [("H5233", "Nekeseh (Wealth)"), ("H1952", "Hon (Wealth/Substance)"), ("H7049", "Qela (Sling/Carving)")]),

    (8041, "שָׂמַאל", "Samal", "Verb", "To Go to the Left; To Use the Left Hand",
     "To go or turn to the left side; to use the left hand.",
     "The Hebrew <em>samal</em> means to go to the left, take the left direction, or use the left hand. Its counterpart is <em>yamin</em> (H3231), to go right. In Hebrew culture, the right hand was the hand of strength, blessing, and honor (Genesis 48:14-17). The left was not shameful but was secondary — associated with the north when facing east, and with the lesser blessing. Ecclesiastes 10:2 states the wise man's heart is at his right and the fool's heart at his left.",
     "The right-left contrast in Scripture carries theological weight. God's right hand saves and sustains (Psalm 18:35; 63:8; 118:16). To 'turn neither to the right nor to the left' from God's commands means strict covenant faithfulness (Deuteronomy 5:32; 28:14). God holds His people with His right hand (Isaiah 41:10). Understanding <em>samal</em> helps interpret blessing narratives (Genesis 48), the divine warrior motif, and the New Testament image of Christ seated at the Father's right hand.",
     [("Ecclesiastes 10:2", "The heart of the wise inclines to the right, but the heart of the fool to the left."),
      ("Genesis 13:9", "Is not the whole land before you? Let's part company. If you go to the left, I'll go to the right; if you go to the right, I'll go to the left."),
      ("2 Samuel 14:19", "As surely as you live, my lord the king, no one can turn to the right or to the left from anything my lord the king says."),
      ("Ezekiel 21:16", "Slash to the right, you sword, then to the left, wherever your blade is turned."),
      ("Isaiah 54:3", "For you will spread out to the right and to the left; your descendants will dispossess nations and settle in their desolate cities.")],
     [("H3231", "Yaman (Right Hand/Right Side)"), ("H3225", "Yamin (Right Hand)"), ("H3027", "Yad (Hand)")]),

    (8437, "תּוֹלָל", "Towlal", "Noun, masculine", "Oppressor; One Who Causes Anguish",
     "An oppressor or tormentor; one who causes writhing grief.",
     "The Hebrew <em>towlal</em> appears only in Psalm 137:3, where it describes those who caused Judah anguish — those who 'tormented' or 'oppressed' the exiles, demanding songs of joy in a foreign land. The word is related to <em>yalal</em> (H3213), meaning to howl or wail, and captures the sense of one who makes others wail — an oppressor who inflicts deep emotional torment.",
     "Psalm 137 is one of the most raw and honest laments in Scripture, arising from the Babylonian exile. The exiles sat by the rivers of Babylon and wept — they could not sing the LORD's songs in a foreign land. Their <em>towlal</em> — oppressors — mockingly demanded worship songs as entertainment. This psalm captures the theology of lament: God's people may cry out their anguish, even their rage (vv. 8-9), in the confidence that God hears and remembers. The memory of Zion and the faithfulness of God sustain the community even in crushing oppression.",
     [("Psalm 137:3", "For there our captors asked us for songs, our <em>tormentors</em> demanded songs of joy; they said, 'Sing us one of the songs of Zion!'"),
      ("Psalm 137:1", "By the rivers of Babylon we sat and wept when we remembered Zion."),
      ("Lamentations 1:5", "Her foes have become her masters; her enemies are at ease. The LORD has brought her grief because of her many sins. Her children have gone into exile, captive before the foe."),
      ("Psalm 74:10", "How long will the enemy mock you, God? Will the foe revile your name forever?"),
      ("Isaiah 49:26", "I will make your oppressors eat their own flesh; they will be drunk on their own blood, as with wine. Then all mankind will know that I, the LORD, am your Savior.")],
     [("H3238", "Yanah (To Oppress)"), ("H6031", "Anah (To Afflict)"), ("H1350", "Gaal (Kinsman-Redeemer)")]),

    (8551, "תָּמַךְ", "Tamak", "Verb", "To Uphold; To Take Hold Of; To Support",
     "To hold up, support, or maintain; to take hold of with sustaining grip.",
     "The Hebrew <em>tamak</em> describes the action of holding something or someone up — sustaining, supporting, or maintaining. It is used of God upholding His servants (Psalm 41:12; 63:8), of wisdom being held fast (Proverbs 3:18; 4:6), and of hands that grip and sustain. The word implies not merely touching but actively holding — bearing the weight, preventing the fall.",
     "The image of God <em>tamak</em>-ing His people is one of the most intimate and reassuring in the Psalms. Psalm 63:8 — 'Your right hand <em>upholds</em> me' — uses <em>tamak</em> to describe the experiential reality of divine sustaining during suffering. Psalm 41:12 says God upholds the person of integrity 'in my integrity you uphold me.' This is not a distant God who watches from afar but One whose grip is active, present, and powerful. Proverbs 3:18 describes Wisdom as a 'tree of life to those who take hold of her,' using <em>tamak</em> for the human side of the embrace.",
     [("Psalm 41:12", "Because of my integrity you <em>uphold</em> me and set me in your presence forever."),
      ("Psalm 63:8", "I cling to you; your right hand <em>upholds</em> me."),
      ("Proverbs 3:18", "She is a tree of life to those who take hold of her; those who hold her fast (<em>tamak</em>) will be blessed."),
      ("Proverbs 4:6", "Do not forsake wisdom, and she will protect you; love her, and she will watch over you."),
      ("Isaiah 42:1", "Here is my servant, whom I <em>uphold</em>, my chosen one in whom I delight; I will put my Spirit on him, and he will bring justice to the nations.")],
     [("H5564", "Samak (To Support/Lean)"), ("H2388", "Chazaq (To Strengthen)"), ("H3027", "Yad (Hand)")]),
]

# ===== GREEK ENTRIES =====
greek_words = [
    (1150, "δαμάζω", "Damazō", "Verb", "To Tame; To Subdue",
     "To tame, subdue, or bring under control — especially wild animals or the tongue.",
     "The Greek <em>damazō</em> refers to the taming of wild creatures — a process that brings what is wild and dangerous under control and harness. James 3:7-8 uses this word powerfully: every kind of animal has been tamed by humans, but no one can tame the tongue. The word appears in Mark 5:4 describing the Gadarene demoniac — no one could subdue him with chains, yet Jesus needed only a word.",
     "James's reflection on the tongue uses <em>damazō</em> to expose the deepest human inability: we can train animals, but we cannot control our own speech. The tongue is a 'restless evil, full of deadly poison' (James 3:8). This is not pessimism but honest theological anthropology — only the Spirit of God can truly subdue the tongue. The Gadarene demoniac who could not be subdued by any human power was instantly pacified by Christ's authority, showing that what human effort cannot <em>damazō</em>, divine power can.",
     [("James 3:7", "All kinds of animals, birds, reptiles and sea creatures are being <em>tamed</em> and have been tamed by mankind."),
      ("James 3:8", "But no human being can <em>tame</em> the tongue. It is a restless evil, full of deadly poison."),
      ("Mark 5:4", "For he had often been chained hand and foot, but he tore the chains apart and broke the irons on his feet. No one was strong enough to <em>subdue</em> him."),
      ("Proverbs 18:21", "The tongue has the power of life and death, and those who love it will eat its fruit."),
      ("Psalm 141:3", "Set a guard over my mouth, LORD; keep watch over the door of my lips.")],
     [("G1100", "Glōssa (Tongue)"), ("G2904", "Kratos (Strength/Power)"), ("G3956", "Pas (All/Every)")]),

    (1151, "δάμαλις", "Damalis", "Noun, feminine", "Heifer; Young Cow",
     "A young cow or heifer — specifically used of the red heifer of purification.",
     "The Greek <em>damalis</em> translates the Hebrew <em>parah</em> (red heifer) in Numbers 19 — the ashes of the red heifer were used to purify those who had become unclean through contact with a corpse. Hebrews 9:13 references the 'ashes of a heifer' (<em>damalis</em>) as a type of the greater purification accomplished by Christ's blood. The heifer was unblemished, had never borne a yoke — a picture of perfect, willing sacrifice.",
     "The red heifer (<em>damalis</em>) is one of the most theologically mysterious rituals in the Old Testament — it purified the unclean but made the clean unclean. Hebrews 9:13-14 contrasts it with Christ's blood: if the ashes of a heifer sanctify for bodily cleanliness, 'how much more will the blood of Christ, who through the eternal Spirit offered himself unblemished to God, cleanse our consciences from acts that lead to death?' The <em>damalis</em> typology shows God was always preparing His people to understand what the perfect Sacrifice would accomplish.",
     [("Hebrews 9:13", "The blood of goats and bulls and the ashes of a <em>heifer</em> sprinkled on those who are ceremonially unclean sanctify them so that they are outwardly clean."),
      ("Numbers 19:2", "This is a requirement of the law that the LORD has commanded: Tell the Israelites to bring you a red <em>heifer</em> without defect or blemish."),
      ("Numbers 19:9", "A man who is clean shall gather up the ashes of the <em>heifer</em> and put them in a ceremonially clean place outside the camp."),
      ("Hebrews 9:14", "How much more, then, will the blood of Christ, who through the eternal Spirit offered himself unblemished to God, cleanse our consciences from acts that lead to death!"),
      ("1 Peter 1:19", "But with the precious blood of Christ, a lamb without blemish or defect.")],
     [("G129", "Haima (Blood)"), ("G2511", "Katharizō (To Cleanse)"), ("G3045", "Hilasmós (Propitiation)")]),

    (1154, "Δαμασκός", "Damaskos", "Noun, proper", "Damascus",
     "Damascus — the ancient Syrian city; site of Paul's conversion encounter.",
     "Damascus (<em>Damaskos</em>) is one of the oldest continuously inhabited cities in the world, the capital of ancient Aram (Syria). In the New Testament, it is immortalized as the city toward which Saul of Tarsus was traveling when the risen Christ appeared to him on the road (Acts 9:1-9). He was blinded, led into Damascus, and there received his sight through Ananias — and with it, his apostolic calling. Damascus also appears in Paul's autobiographical accounts (2 Corinthians 11:32; Galatians 1:17).",
     "The road to Damascus is perhaps the most famous conversion account in history. The persecutor became the apostle; the hunter became the hunted; the man breathing threats became the man breathing grace. Damascus marks the geographical intersection of Paul's old life and new mission. But it also appears in OT prophecy (Isaiah 17; Amos 1) as a symbol of world power brought low before God's sovereignty. From Abraham passing through (Genesis 15:2 — Eliezer of Damascus) to Paul's blinding encounter, Damascus is a recurring stage in redemptive history.",
     [("Acts 9:3", "As he neared <em>Damascus</em> on his journey, suddenly a light from heaven flashed around him."),
      ("Acts 9:8", "Saul got up from the ground, but when he opened his eyes he could see nothing. So they led him by the hand into <em>Damascus</em>."),
      ("2 Corinthians 11:32", "In <em>Damascus</em> the governor under King Aretas had the city of the Damascenes guarded in order to arrest me."),
      ("Galatians 1:17", "Nor did I go up to Jerusalem to see those who were apostles before I was, but I went into Arabia. Later I returned to <em>Damascus</em>."),
      ("Isaiah 17:1", "A prophecy against <em>Damascus</em>: See, Damascus will no longer be a city but will become a heap of ruins.")],
     [("G652", "Apostolos (Apostle)"), ("G3972", "Paulos (Paul)"), ("G5547", "Christos (Christ)")]),

    (1155, "δανείζω", "Daneizō", "Verb", "To Lend Money",
     "To lend money, especially at interest; to borrow.",
     "The Greek <em>daneizō</em> means to lend money, and in the active voice specifically to lend on terms of repayment (sometimes with interest). Jesus uses this word in Luke 6:34-35 in a radically counter-cultural teaching: even sinners lend to those who can repay — but His disciples are to lend without expecting anything back. The word appears also in Matthew 5:42 in the broader context of generosity toward those who ask.",
     "Jesus redefines the economics of <em>daneizō</em>. The world's lending system is transactional: you lend to those who can repay, thereby increasing your social capital or wealth. Kingdom lending abandons the expectation of return and operates on pure generosity — 'lend to them without expecting to get anything back' (Luke 6:35). This ethic flows from God's own character, who gives rain to the righteous and unrighteous alike. The Christian who <em>daneizō</em>s without calculation reflects the generous heart of a Father who gives to all freely.",
     [("Luke 6:34", "And if you lend to those from whom you expect repayment, what credit is that to you? Even sinners <em>lend</em> to sinners, expecting to be repaid in full."),
      ("Luke 6:35", "But love your enemies, do good to them, and <em>lend</em> to them without expecting to get anything back."),
      ("Matthew 5:42", "Give to the one who asks you, and do not turn away from the one who wants to borrow from you."),
      ("Deuteronomy 15:8", "Rather, be openhanded and freely lend them whatever they need."),
      ("Psalm 37:26", "They are always generous and lend freely; their children will be a blessing.")],
     [("G1156", "Daneion (Debt/Loan)"), ("G1157", "Daneistēs (Creditor)"), ("G26", "Agapē (Love)")]),

    (1156, "δάνειον", "Daneion", "Noun, neuter", "Debt; Loan",
     "A loan of money; a debt owed.",
     "The Greek <em>daneion</em> refers to a financial loan or debt. Jesus uses it in the Parable of the Unforgiving Servant (Matthew 18:27) — the master cancels the servant's enormous <em>daneion</em> (the enormous debt he could never repay). This forgiven debt becomes the standard against which the servant's failure to forgive a small debt is measured, making his harshness incomprehensible.",
     "The parable of the unforgiving servant uses <em>daneion</em> to illuminate the nature of divine forgiveness. Our debt to God is staggering — beyond any human capacity to repay. Yet God, 'filled with compassion,' cancels it entirely. The forgiven servant's harshness toward his fellow servant (who owed a fraction of what was forgiven) is spiritually insane by comparison. The lesson: those who have experienced God's forgiveness of their infinite moral debt must extend forgiveness to others. The Lord's Prayer ('forgive us our debts') reflects this same concept.",
     [("Matthew 18:27", "The servant's master took pity on him, canceled the debt (<em>daneion</em>) and let him go."),
      ("Matthew 6:12", "And forgive us our debts, as we also have forgiven our debtors."),
      ("Luke 7:41", "Two people owed money to a certain moneylender. One owed him five hundred denarii, and the other fifty."),
      ("Romans 13:8", "Let no debt remain outstanding, except the continuing debt to love one another."),
      ("Colossians 2:14", "Having canceled the charge of our legal indebtedness, which stood against us and condemned us; he has taken it away, nailing it to the cross.")],
     [("G1155", "Daneizō (To Lend)"), ("G1157", "Daneistēs (Creditor)"), ("G859", "Aphesis (Forgiveness)")]),

    (1157, "δανειστής", "Daneistēs", "Noun, masculine", "Creditor; Moneylender",
     "A creditor; one who lends money and to whom a debt is owed.",
     "The Greek <em>daneistēs</em> (also spelled <em>danistēs</em>) is the creditor — the one who holds the debt. Jesus uses the term in Luke 7:41, the parable of the two debtors told to Simon the Pharisee: 'Two men owed money to a certain <em>moneylender</em>.' One owed 500 denarii, the other 50. Both debts were canceled. The question: which will love the creditor more? Simon correctly identifies the one who was forgiven more.",
     "The <em>daneistēs</em> in Jesus' parable is clearly a figure for God — the one who has the right to demand payment, yet chooses to forgive. The parable was prompted by a sinful woman's extravagant act of love toward Jesus (Luke 7:36-50). Her great love was evidence of great forgiveness received; Simon's small love revealed small appreciation for his own forgiveness. The creditor's cancellation of debt — completely without merit on the debtor's part — is the pattern of all divine grace.",
     [("Luke 7:41", "Two people owed money to a certain <em>moneylender</em>. One owed him five hundred denarii, and the other fifty."),
      ("Luke 7:42", "Neither of them had the money to pay him back, so he forgave the debts of both. Now which of them will love him more?"),
      ("Matthew 18:23", "Therefore, the kingdom of heaven is like a king who wanted to settle accounts with his servants."),
      ("Romans 4:4", "Now to the one who works, wages are not credited as a gift but as an obligation."),
      ("Isaiah 50:1", "This is what the LORD says: 'Where is your mother's certificate of divorce with which I sent her away? Or to which of my <em>creditors</em> did I sell you?'")],
     [("G1155", "Daneizō (To Lend)"), ("G1156", "Daneion (Debt)"), ("G5485", "Charis (Grace)")]),

    (1159, "δαπανάω", "Dapanaō", "Verb", "To Spend; To Consume Resources",
     "To spend, consume, or exhaust resources — money, strength, or supplies.",
     "The Greek <em>dapanaō</em> means to spend or consume resources. Jesus uses it in the Parable of the Prodigal Son — the younger son 'squandered his wealth in wild living' (<em>dapanaō</em>, Luke 15:14). Paul uses it in 2 Corinthians 12:15: 'I will very gladly spend and be spent for you.' The word captures the idea of resources flowing out — either wastefully or sacrificially.",
     "The contrast between <em>dapanaō</em> in Luke 15 and 2 Corinthians 12 is the difference between foolish waste and love-driven sacrifice. The prodigal squanders his inheritance on momentary pleasures; Paul gladly spends himself on the Corinthians' souls even when they love him less for it. This is the apostolic — and ultimately Christological — pattern: the Shepherd who spends Himself fully for the sheep. The Father's extravagant feast for the returning prodigal (Luke 15:22-24) mirrors God's own willing expenditure of grace.",
     [("Luke 15:14", "After he had spent everything (<em>dapanaō</em>), there was a severe famine in that whole country, and he began to be in need."),
      ("2 Corinthians 12:15", "So I will very gladly spend and be spent in service for your souls."),
      ("Mark 5:26", "She had suffered a great deal under the care of many doctors and had spent all she had, yet instead of getting better she grew worse."),
      ("Acts 21:24", "Take these men, join in their purification rites and pay their expenses."),
      ("James 4:3", "When you ask, you do not receive, because you ask with wrong motives, that you may spend what you get on your pleasures.")],
     [("G1160", "Dapanē (Expense/Cost)"), ("G4137", "Plēroō (To Fill)"), ("G26", "Agapē (Love)")]),

    (1160, "δαπάνη", "Dapanē", "Noun, feminine", "Cost; Expense",
     "The cost or expense of something; the price of undertaking a project.",
     "The Greek <em>dapanē</em> is the noun form of <em>dapanaō</em> — the actual cost or expense involved. Jesus uses it in the Parable of the Tower Builder (Luke 14:28): 'Suppose one of you wants to build a tower. Won't you first sit down and estimate the <em>cost</em> to see if you have enough money to complete it?' This parable about counting the cost of discipleship uses <em>dapanē</em> as the central image.",
     "The <em>dapanē</em> of discipleship is not incidental to following Jesus — it is central. Jesus explicitly demands that would-be followers calculate whether they can sustain the cost: cross-bearing, family-surrender, and total loyalty. The Tower Builder who cannot finish is mocked; the King who cannot win sits down to negotiate. The point is not that discipleship is optional if the cost is too high, but that Jesus demands honest, clear-eyed commitment — not impulsive enthusiasm that fades. Grace costs nothing to receive but everything to follow.",
     [("Luke 14:28", "Suppose one of you wants to build a tower. Won't you first sit down and estimate the <em>cost</em> to see if you have enough money to complete it?"),
      ("Luke 9:23", "Whoever wants to be my disciple must deny themselves and take up their cross daily and follow me."),
      ("Matthew 16:24", "Then Jesus said to his disciples, 'Whoever wants to be my disciple must deny themselves and take up their cross and follow me.'"),
      ("Philippians 3:8", "What is more, I consider everything a loss because of the surpassing worth of knowing Christ Jesus my Lord."),
      ("Luke 14:33", "In the same way, those of you who do not give up everything you have cannot be my disciples.")],
     [("G1159", "Dapanaō (To Spend)"), ("G4716", "Stauros (Cross)"), ("G3101", "Mathētēs (Disciple)")]),

    (1163, "δεῖ", "Dei", "Verb (impersonal)", "It Is Necessary; One Must",
     "It is necessary, inevitable, or divinely required — often expressing divine necessity.",
     "The Greek <em>dei</em> is an impersonal verb meaning 'it is necessary' or 'one must.' In the Gospels and Acts, it frequently carries the weight of divine necessity — particularly regarding the suffering, death, and resurrection of Christ. 'The Son of Man <em>must</em> suffer' (Mark 8:31); 'The Son of Man <em>must</em> be lifted up' (John 3:14); 'I <em>must</em> be in my Father's house' (Luke 2:49). This is not external compulsion but the inner necessity of God's redemptive plan.",
     "<em>Dei</em> is one of the most theologically significant words in Luke-Acts. It appears over 40 times, consistently marking events as divinely ordained rather than accidental. The crucifixion was not a tragedy interrupted by resurrection — it was a divine <em>dei</em>, a necessary fulfillment of God's eternal purpose. When Jesus says 'the Son of Man must suffer,' He is declaring that the cross was not plan B but the very plan of redemption determined before creation (1 Peter 1:20). Every <em>dei</em> in the Gospel points to the sovereignty and love of the Father.",
     [("Mark 8:31", "He then began to teach them that the Son of Man <em>must</em> suffer many things and be rejected."),
      ("John 3:14", "Just as Moses lifted up the snake in the wilderness, so the Son of Man <em>must</em> be lifted up."),
      ("Luke 2:49", "Why were you searching for me? Didn't you know I <em>had to</em> be in my Father's house?"),
      ("Acts 4:12", "Salvation is found in no one else, for there is no other name under heaven given to mankind by which we <em>must</em> be saved."),
      ("Revelation 4:1", "Come up here, and I will show you what <em>must</em> take place after this.")],
     [("G1012", "Boulē (Purpose/Plan)"), ("G4137", "Plēroō (To Fulfill)"), ("G3056", "Logos (Word)")]),

    (1164, "δεῖγμα", "Deigma", "Noun, neuter", "Example; Specimen; Public Display",
     "An example made visible; a specimen put on display as a warning or proof.",
     "The Greek <em>deigma</em> means an example, specimen, or public display — something held up so others can see what it is or what happens because of it. In Jude 7, Sodom and Gomorrah are described as a <em>deigma</em> (example) undergoing the punishment of eternal fire. They were not just destroyed but made into a visible, permanent example of divine judgment — their ruins a perpetual warning to the surrounding nations.",
     "Sodom and Gomorrah as <em>deigma</em> is a solemn theological statement: God's judgments in history serve pedagogical purposes. The punishment of cities and nations is not merely retributive — it is revelatory. The Hebrew prophets frequently cite Sodom as the comparison point for moral catastrophe. Jesus Himself uses Sodom as the measuring stick for towns that reject the gospel (Matthew 10:15). As a <em>deigma</em> of eternal fire, Sodom warns every generation that divine patience has limits and divine judgment is real.",
     [("Jude 7", "In a similar way, Sodom and Gomorrah and the surrounding towns gave themselves up to sexual immorality and perversion. They serve as an <em>example</em> of those who suffer the punishment of eternal fire."),
      ("Genesis 19:24", "Then the LORD rained down burning sulfur on Sodom and Gomorrah — from the LORD out of the heavens."),
      ("Matthew 10:15", "Truly I tell you, it will be more bearable for Sodom and Gomorrah on the day of judgment than for that town."),
      ("2 Peter 2:6", "If he condemned the cities of Sodom and Gomorrah by burning them to ashes, and made them an <em>example</em> of what is going to happen to the ungodly."),
      ("Ezekiel 16:49", "Now this was the sin of your sister Sodom: She and her daughters were arrogant, overfed and unconcerned; they did not help the poor and needy.")],
     [("G5262", "Hypodeigma (Pattern/Example)"), ("G2920", "Krisis (Judgment)"), ("G4442", "Pyr (Fire)")]),

    (1165, "δειγματίζω", "Deigmatizō", "Verb", "To Make a Public Example; To Expose",
     "To make a public spectacle of; to expose openly to shame or disgrace.",
     "The Greek <em>deigmatizō</em> means to put on public display — to expose someone to shame and reproach. In Matthew 1:19, Joseph, not wanting to 'expose' (<em>deigmatizō</em>) Mary publicly, decided to divorce her quietly — he did not want to make her a public example of apparent unfaithfulness. In Colossians 2:15, Christ 'made a public spectacle' of the rulers and authorities by triumphing over them through the cross.",
     "The two uses of <em>deigmatizō</em> create a remarkable contrast. Joseph chose not to publicly shame Mary — a profound act of mercy toward someone who appeared guilty. Meanwhile, Christ on the cross — where He appeared to be shamed — was actually making a public spectacle of demonic powers, stripping them of their authority. What looked like public shame for Christ was actually public triumph. God consistently inverts human expectations: the One who could have been shamed became the one who triumphed, and chose to protect those who might have been shamed.",
     [("Matthew 1:19", "Because Joseph her husband was faithful to the law, and yet did not want to <em>expose</em> her to public disgrace, he had in mind to divorce her quietly."),
      ("Colossians 2:15", "And having disarmed the powers and authorities, he made a public spectacle of them, triumphing over them by the cross."),
      ("Hebrews 6:6", "It is impossible for those who have once been enlightened... if they fall away, to be brought back to repentance. To their loss they are crucifying the Son of God all over again and subjecting him to public disgrace."),
      ("Numbers 25:4", "The LORD said to Moses, 'Take all the leaders of these people, kill them and expose them in broad daylight before the LORD.'"),
      ("Proverbs 11:2", "When pride comes, then comes disgrace, but with humility comes wisdom.")],
     [("G1164", "Deigma (Example)"), ("G819", "Atimia (Dishonor)"), ("G2358", "Thriambeuō (To Triumph)")]),

    (1167, "δειλία", "Deilia", "Noun, feminine", "Cowardice; Timidity",
     "Cowardice, timidity, or fearfulness — especially spiritual or moral cowardice.",
     "The Greek <em>deilia</em> means cowardice — not ordinary caution but the specific failure of nerve that causes a person to abandon duty, deny truth, or flee danger when faithfulness demands standing firm. In 2 Timothy 1:7, Paul declares: 'For God did not give us a spirit of <em>deilia</em> (timidity/cowardice), but a spirit of power, of love and of self-discipline.' This is one of only three NT occurrences of this word group, and it is definitionally opposed to the Spirit of God.",
     "The divine antidote to <em>deilia</em> is threefold: power, love, and self-discipline. Cowardice is not merely a personality trait but a failure of the Spirit — specifically, an operation in the opposite spirit to God's own. Paul writes to Timothy, who was apparently struggling with timidity in proclaiming the gospel. The context (2 Tim 1:6-14) emphasizes that faithfulness to the gospel requires enduring hardship, not shrinking from it. Cowardice in the face of persecution is incompatible with possessing the Holy Spirit.",
     [("2 Timothy 1:7", "For the Spirit God gave us does not make us timid (<em>deilia</em>), but gives us power, love and self-discipline."),
      ("John 14:27", "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid."),
      ("Joshua 1:9", "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the LORD your God will be with you wherever you go."),
      ("Revelation 21:8", "But the cowardly, the unbelieving, the vile, the murderers, the sexually immoral, those who practice magic arts, the idolaters and all liars — they will be consigned to the fiery lake."),
      ("Isaiah 41:10", "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you.")],
     [("G1168", "Deiliaō (To Be Afraid)"), ("G1169", "Deilos (Cowardly)"), ("G1411", "Dynamis (Power)")]),

    (1168, "δειλιάω", "Deiliaō", "Verb", "To Be Afraid; To Cower; To Be Cowardly",
     "To be timid, afraid, or cowardly — to shrink back in fear.",
     "The Greek <em>deiliaō</em> (verb form of <em>deilia</em>) describes the act of being fearfully timid or cowardly. Jesus uses it in John 14:27 in combination with <em>tarassomai</em> (to be troubled): 'Do not let your hearts be troubled and do not be afraid (<em>deiliaō</em>).' This is spoken in the Upper Room on the night of the crucifixion — the eve of the greatest trial the disciples would face. Jesus' peace is the antidote to <em>deiliaō</em>.",
     "The peace that Jesus gives is not the world's peace (absence of conflict) but the peace of absolute security in God's eternal purpose. Because Jesus is going to the Father (John 14:28), the disciples can stand firm — they are not abandoned. <em>Deiliaō</em> in the face of persecution or loss is addressed not by minimizing the danger but by anchoring the soul in the resurrection reality. Those who know the risen Lord need not <em>deiliaō</em> before human powers.",
     [("John 14:27", "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid (<em>deiliaō</em>)."),
      ("Deuteronomy 1:21", "See, the LORD your God has given you the land. Go up and take possession of it as the LORD, the God of your ancestors, told you. Do not be afraid; do not be discouraged."),
      ("Joshua 8:1", "Then the LORD said to Joshua, 'Do not be afraid; do not be discouraged. Take the whole army with you.'"),
      ("Isaiah 35:4", "Say to those with fearful hearts, 'Be strong, do not fear; your God will come, he will come with divine retribution; God will come to save you.'"),
      ("1 John 4:18", "There is no fear in love. But perfect love drives out fear, because fear has to do with punishment.")],
     [("G1167", "Deilia (Cowardice)"), ("G1169", "Deilos (Cowardly/Fearful)"), ("G1515", "Eirēnē (Peace)")]),

    (1169, "δειλός", "Deilos", "Adjective", "Cowardly; Fearful; Timid",
     "Cowardly, fearful, or timid — lacking the courage to stand firm.",
     "The Greek <em>deilos</em> is the adjective describing the cowardly or fearful person. Jesus uses it in the storm-stilling narrative: 'He said to them, "Why are you so afraid (<em>deilos</em>)?"' (Mark 4:40). Remarkably, Revelation 21:8 lists <em>deiloi</em> (cowards) first in the catalog of those excluded from the New Jerusalem — before the unbelieving, the vile, and the murderers. Cowardice in the context of persecution and apostasy is a serious spiritual failure.",
     "The placement of <em>deiloi</em> first in Revelation 21:8's list is theologically arresting. In the context of the book of Revelation — written to churches facing Roman persecution — cowardice means caving under pressure and denying Christ. This is not fear of spiders but the soul-level failure to 'hold fast to your faith' (Revelation 2:13). The antidote is the same throughout: 'Be faithful, even to the point of death, and I will give you life as your victor's crown' (Rev 2:10). Perfect love casts out <em>deilos</em> fear (1 John 4:18).",
     [("Mark 4:40", "He said to his disciples, 'Why are you so afraid (<em>deilos</em>)? Do you still have no faith?'"),
      ("Matthew 8:26", "He replied, 'You of little faith, why are you so afraid?' Then he got up and rebuked the winds and the waves."),
      ("Revelation 21:8", "But the <em>cowardly</em>, the unbelieving, the vile, the murderers, the sexually immoral, those who practice magic arts, the idolaters and all liars."),
      ("2 Timothy 1:7", "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline."),
      ("1 John 4:18", "There is no fear in love. But perfect love drives out fear, because fear has to do with punishment.")],
     [("G1167", "Deilia (Cowardice)"), ("G1168", "Deiliaō (To Be Afraid)"), ("G4102", "Pistis (Faith)")]),

    (1171, "δεινῶς", "Deinōs", "Adverb", "Terribly; Grievously; Mightily",
     "Terribly, dreadfully, or grievously — used of intense suffering or extreme action.",
     "The Greek <em>deinōs</em> is an adverb meaning terribly, grievously, or fiercely. It appears twice in the New Testament: in Matthew 8:6, the centurion describes his servant as 'lying at home paralyzed and in terrible (<em>deinōs</em>) agony'; and in Luke 11:53, the scribes and Pharisees 'began to oppose him fiercely (<em>deinōs</em>) and to besiege him with questions.' The word intensifies — things that are merely bad become terrible; opposition becomes fierce persecution.",
     "The centurion's use of <em>deinōs</em> gives insight into his character. He comes to Jesus not with a casual request but with the urgent weight of a man who has watched someone he cares for suffer terribly. His military rank means he had power over people's lives, yet before Jesus he speaks with profound humility (vv. 8-9). The intensity of <em>deinōs</em> suffering matched by the <em>deinōs</em> urgency of his faith produces one of the greatest commendations Jesus ever gave: 'I have not found anyone in Israel with such great faith.'",
     [("Matthew 8:6", "He said, 'Lord, my servant lies at home paralyzed, suffering <em>terribly</em>.'"),
      ("Luke 11:53", "When Jesus went outside, the Pharisees and the teachers of the law began to oppose him <em>fiercely</em> and to besiege him with questions."),
      ("Matthew 8:13", "Then Jesus said to the centurion, 'Go! Let it be done just as you believed it would.' And his servant was healed at that moment."),
      ("Psalm 22:14", "I am poured out like water, and all my bones are out of joint. My heart has turned to wax; it has melted within me."),
      ("Isaiah 53:3", "He was despised and rejected by mankind, a man of suffering, and familiar with pain.")],
     [("G3173", "Megas (Great)"), ("G2560", "Kakōs (Badly/Grievously)"), ("G4102", "Pistis (Faith)")]),

    (1172, "δειπνέω", "Deipneō", "Verb", "To Eat Supper; To Dine",
     "To eat the evening meal; to dine; to take supper.",
     "The Greek <em>deipneō</em> means to eat the main evening meal (<em>deipnon</em>). Jesus' use in Revelation 3:20 is deeply intimate and striking: 'I stand at the door and knock. If anyone hears my voice and opens the door, I will come in and eat with them (<em>deipneō</em>), and they with me.' Table fellowship in the ancient world was the deepest form of relational intimacy. To <em>deipneō</em> with someone was to be at home with them.",
     "Revelation 3:20 is addressed to the Laodicean church — a church that was lukewarm, self-sufficient, and apparently unaware that Christ had been pushed outside. The image of Jesus knocking at the door, offering to <em>deipneō</em> with those who open, is an offer of restored intimacy and fellowship. The Eucharist itself is a form of <em>deipneō</em> — the church gathered at the Lord's table participates in covenantal fellowship with Him. Every time we eat the Lord's Supper, we <em>deipneō</em> with the living Christ.",
     [("Revelation 3:20", "Here I am! I stand at the door and knock. If anyone hears my voice and opens the door, I will come in and <em>eat</em> with that person, and they with me."),
      ("Luke 17:8", "Wouldn't he rather say, 'Prepare my supper, get yourself ready and wait on me while I eat and drink; after that you may eat and drink'?"),
      ("Luke 22:20", "In the same way, after the supper he took the cup, saying, 'This cup is the new covenant in my blood, which is poured out for you.'"),
      ("1 Corinthians 11:25", "In the same way, after supper he took the cup, saying, 'This cup is the new covenant in my blood.'"),
      ("John 13:2", "The evening meal was in progress, and the devil had already prompted Judas, the son of Simon Iscariot, to betray Jesus.")],
     [("G1173", "Deipnon (Supper/Dinner)"), ("G2169", "Eucharistia (Thanksgiving)"), ("G2842", "Koinōnia (Fellowship)")]),

    (1173, "δεῖπνον", "Deipnon", "Noun, neuter", "Supper; Dinner; Feast",
     "The main evening meal; a dinner or banquet — including the Lord's Supper.",
     "The Greek <em>deipnon</em> is the primary word for the evening meal or dinner in the NT. It appears in the institution of the Lord's Supper ('after the <em>deipnon</em>' — Luke 22:20; 1 Corinthians 11:25), in the Parable of the Great Banquet (Luke 14:16-24), in the Marriage Supper of the Lamb (Revelation 19:9, 17), and in the washing of disciples' feet (John 13:2-4). This word bridges the physical and the eschatological.",
     "The <em>deipnon</em> in biblical theology is the gathering point of the covenant community around the provision of the host. The Great Banquet parable shows God's kingdom as a feast to which all are invited — and the tragedy of those who decline. The Lord's Supper is a <em>deipnon</em> where the Host himself is the food — 'This is my body, this is my blood.' The Marriage Supper of the Lamb in Revelation 19:9 is the eschatological fulfillment: 'Blessed are those who are invited to the wedding supper of the Lamb.' Every <em>deipnon</em> with Jesus is a foretaste of that final feast.",
     [("Luke 22:20", "In the same way, after the <em>supper</em> he took the cup, saying, 'This cup is the new covenant in my blood, which is poured out for you.'"),
      ("Revelation 19:9", "Then the angel said to me, 'Write this: Blessed are those who are invited to the wedding <em>supper</em> of the Lamb!'"),
      ("Luke 14:16", "Jesus replied: 'A certain man was preparing a great <em>banquet</em> and invited many guests.'"),
      ("John 13:2", "The evening meal (<em>deipnon</em>) was in progress, and the devil had already prompted Judas, the son of Simon Iscariot, to betray Jesus."),
      ("1 Corinthians 11:20", "So then, when you come together, it is not the Lord's <em>Supper</em> you eat.")],
     [("G1172", "Deipneō (To Dine)"), ("G1062", "Gamos (Wedding)"), ("G2222", "Zōē (Life)")]),

    (1174, "δεισιδαιμονέστερος", "Deisidaimonesteros", "Adjective (comparative)", "More Religious; Very Religious",
     "More devoted to the divine; more scrupulous in religious observance.",
     "The Greek <em>deisidaimonesteros</em> is a comparative adjective that Paul uses in Acts 17:22, addressing the Athenians on the Areopagus: 'Men of Athens! I see that in every way you are very religious (<em>deisidaimonesteros</em>).' The word literally means 'more fearing of the divine' — and it was intentionally ambiguous. Paul could be offering a polite compliment (you are very devout) or a subtle critique (you are overly superstitious). The Athenians would have heard it positively; the content that follows redirects their religious impulse toward the true God.",
     "Paul's Areopagus speech is a masterclass in apologetics. He begins with the Athenians' own <em>deisidaimonia</em> (religiosity) — their altar 'TO AN UNKNOWN GOD' — and uses it as a bridge to the gospel. Rather than condemning their worship as demonic, he acknowledges their genuine religious impulse and redirects it: 'What you worship as something unknown I am going to proclaim to you.' This approach — finding the true knowledge inside incomplete seeking — reflects the theology that God has placed eternity in the human heart (Ecclesiastes 3:11) and that all true seeking ultimately leads to Him.",
     [("Acts 17:22", "Paul then stood up in the meeting of the Areopagus and said: 'People of Athens! I see that in every way you are very religious (<em>deisidaimonesteros</em>).'"),
      ("Acts 17:23", "For as I walked around and looked carefully at your objects of worship, I even found an altar with this inscription: TO AN UNKNOWN GOD."),
      ("Acts 17:28", "'For in him we live and move and have our being.' As some of your own poets have said, 'We are his offspring.'"),
      ("Ecclesiastes 3:11", "He has made everything beautiful in its time. He has also set eternity in the human heart; yet no one can fathom what God has done."),
      ("Romans 1:20", "For since the creation of the world God's invisible qualities — his eternal power and divine nature — have been clearly seen.")],
     [("G1175", "Deisidaimonia (Religion/Superstition)"), ("G2316", "Theos (God)"), ("G4151", "Pneuma (Spirit)")]),

    (1175, "δεισιδαιμονία", "Deisidaimonia", "Noun, feminine", "Religion; Fear of the Divine; Superstition",
     "Religion, religious scrupulosity, or superstition — fear and reverence toward divine beings.",
     "The Greek <em>deisidaimonia</em> (noun from <em>deisidaimōn</em>) refers to the quality of being religiously observant — with the same ambiguity as the adjective form. In Acts 25:19, Festus describes Paul's dispute with the Jewish authorities as being about their own religion (<em>deisidaimonia</em>) and about 'a dead man named Jesus who Paul claimed was alive.' Festus uses the term from the outside, as a Roman administrator observing what seems to him a religious dispute.",
     "Festus's use of <em>deisidaimonia</em> is a small window into how early Christianity appeared to outsiders — as an internal Jewish dispute about resurrection. From the Roman perspective, it was religious enthusiasm (possibly superstition). From the NT perspective, the resurrection is the hinge of all history. Paul's defense before both Festus and Agrippa (Acts 25-26) shows him willing to be dismissed as religiously zealous as long as he can proclaim that 'Christ died for our sins according to the Scriptures, and that he was raised' (1 Corinthians 15:3-4).",
     [("Acts 25:19", "Instead, they had some points of dispute with him about their own <em>religion</em> and about a dead man named Jesus who Paul claimed was alive."),
      ("Acts 17:22", "Paul then stood up in the meeting of the Areopagus and said: 'People of Athens! I see that in every way you are very religious.'"),
      ("Acts 26:5", "They have known me for a long time and can testify, if they are willing, that I conformed to the strictest sect of our religion, living as a Pharisee."),
      ("Romans 10:2", "For I can testify about them that they are zealous for God, but their zeal is not based on knowledge."),
      ("Colossians 2:23", "Such regulations indeed have an appearance of wisdom, with their self-imposed worship, their false humility and their harsh treatment of the body.")],
     [("G1174", "Deisidaimonesteros (More Religious)"), ("G2356", "Thrēskeia (Religion)"), ("G386", "Anastasis (Resurrection)")]),

    (1176, "δέκα", "Deka", "Numeral", "Ten",
     "The number ten — foundational to Hebrew covenantal and decimal systems.",
     "The Greek <em>deka</em> (ten) is significant beyond its numeric value because the number ten pervades biblical covenant structure. The Ten Commandments (<em>aseret haddevarim</em> — the ten words) form the foundation of Mosaic covenant ethics. Ten plagues fell on Egypt. The Parable of the Ten Virgins and the Parable of the Ten Minas (Luke 19:13-27) both use ten as a structural number. In Revelation, the beast has ten horns representing ten kings. Ten is the number of completeness in a system — the full accounting.",
     "When Jesus structures a parable around ten virgins or ten minas, He is invoking a completeness — the full range of humanity represented in the story. The ten virgins (Matthew 25:1-13) represent the whole of those awaiting the Bridegroom: half prepared, half not. The lesson is radical: spiritual preparedness cannot be borrowed or transferred at the last moment. The ten minas of Luke 19 represent the totality of what the King has entrusted — <em>deka</em> as the symbol of full accountability.",
     [("Matthew 25:1", "At that time the kingdom of heaven will be like <em>ten</em> virgins who took their lamps and went out to meet the bridegroom."),
      ("Luke 15:8", "Or suppose a woman has <em>ten</em> silver coins and loses one."),
      ("Luke 19:13", "So he called <em>ten</em> of his servants and gave them <em>ten</em> minas."),
      ("Revelation 17:12", "The <em>ten</em> horns you saw are ten kings who have not yet received a kingdom, but who for one hour will receive authority as kings along with the beast."),
      ("Exodus 34:28", "Moses was there with the LORD forty days and forty nights without eating bread or drinking water. And he wrote on the tablets the words of the covenant — the <em>Ten</em> Commandments.")],
     [("G1181", "Dekatē (Tithe/Tenth)"), ("G1182", "Dekatos (Tenth)"), ("G1785", "Entolē (Commandment)")]),

    (1178, "δεκαπέντε", "Dekapente", "Numeral", "Fifteen",
     "The number fifteen — appearing in key biblical chronological and geographical details.",
     "The Greek <em>dekapente</em> (fifteen) appears in John 11:18 (Bethany was about fifteen stadia from Jerusalem), Galatians 1:18 (Paul stayed with Peter for fifteen days), Acts 27:28 (water depth of fifteen fathoms), and John 19:39 (Nicodemus brought seventy-five — not fifteen — pounds of spices). Fifteen also appears in the OT structure of fifteen Psalms of Ascent (Psalms 120-134), sung by pilgrims ascending to Jerusalem.",
     "The fifteen days Paul spent with Peter (Galatians 1:18) is historically significant. After his Damascus conversion and three years in Arabia, Paul's first extended contact with the Jerusalem apostles was this fifteen-day visit with Peter (<em>Cephas</em>), plus seeing James the Lord's brother. This careful historical note grounds the continuity of Paul's gospel — it was independently received (Galatians 1:12) but consistent with what Peter and James testified. Bethany being fifteen stadia from Jerusalem (John 11:18) explains why news of Lazarus reached Jerusalem so quickly, and why Martha and Mary could have mourners from the city present.",
     [("John 11:18", "Now Bethany was less than two miles from Jerusalem, and many Jews had come to Martha and Mary to comfort them."),
      ("Galatians 1:18", "Then after three years, I went up to Jerusalem to get acquainted with Cephas and stayed with him <em>fifteen</em> days."),
      ("Acts 27:28", "They took soundings and found that the water was a hundred and twenty feet deep. A short time later they took soundings again and found it was ninety feet deep."),
      ("Psalm 122:1", "I rejoiced with those who said to me, 'Let us go to the house of the LORD.' — one of the fifteen Psalms of Ascent"),
      ("Nehemiah 5:14", "Moreover, from the twentieth year of King Artaxerxes, when I was appointed to be their governor in the land of Judah, until his thirty-second year — <em>twelve</em> years.")],
     [("G1176", "Deka (Ten)"), ("G4002", "Pente (Five)"), ("G652", "Apostolos (Apostle)")]),

    (1181, "δεκάτη", "Dekatē", "Noun, feminine", "Tithe; Tenth Part",
     "A tithe — the tenth part given to God or to the priest.",
     "The Greek <em>dekatē</em> translates the Hebrew <em>maaser</em> (H4643) — the tithe, the tenth part set aside for God. Hebrews 7 uses <em>dekatē</em> six times in its theological argument that Melchizedek is greater than Abraham (because Abraham gave him a tenth — <em>dekatē</em>) and therefore that Christ's Melchizedekian priesthood surpasses the Levitical. The tithe predates the Mosaic Law (Genesis 14:20) and finds its NT fulfillment in Christ as the ultimate High Priest.",
     "The theology of <em>dekatē</em> is not primarily about finances but about sovereignty and gratitude. To tithe was to acknowledge that everything belongs to God and that the worshiper is a steward, not an owner. Abraham's tithe to Melchizedek (Hebrews 7:2) became the theological argument for Christ's superior priesthood — a priesthood not based on genealogy but on indestructible life (Hebrews 7:16). The Pharisees tithed meticulously but 'neglected the weightier matters of the law' (Matthew 23:23). Jesus affirmed tithing while insisting it flows from the heart, not mere duty.",
     [("Hebrews 7:2", "And Abraham gave him a <em>tenth</em> of everything. First, the name 'king of righteousness'; then also, 'king of Salem' meaning 'king of peace.'"),
      ("Hebrews 7:8", "In the one case, the <em>tenth</em> is collected by people who die; but in the other case, by him who is declared to be living."),
      ("Genesis 14:20", "And praise be to God Most High, who delivered your enemies into your hand. Then Abram gave him a <em>tenth</em> of everything."),
      ("Matthew 23:23", "Woe to you, teachers of the law and Pharisees, you hypocrites! You give a <em>tenth</em> of your spices — mint, dill and cumin."),
      ("Malachi 3:10", "Bring the whole <em>tithe</em> into the storehouse, that there may be food in my house. Test me in this, says the LORD Almighty.")],
     [("G1182", "Dekatos (Tenth)"), ("G749", "Archiereus (High Priest)"), ("G3198", "Melchisedek (Melchizedek)")]),

    (1182, "δέκατος", "Dekatos", "Adjective/Ordinal", "Tenth",
     "The ordinal number tenth — marking the tenth in a series.",
     "The Greek <em>dekatos</em> is the ordinal 'tenth.' It appears in John 1:39 — the disciples came to see where Jesus was staying and 'stayed with him that day, for it was about the <em>tenth</em> hour.' In Revelation, <em>dekatos</em> appears in descriptions of the city (Revelation 11:13 — a tenth of the city fell), the priestly garments sequence, and the foundational stones of the New Jerusalem (Revelation 21:20). The tenth hour of John 1 is approximately 4 PM — the disciples spent the evening with Jesus, a first extended encounter.",
     "The disciples' question 'Where are you staying?' (John 1:38) and Jesus' answer 'Come and see' followed by a stay until the <em>tenth</em> hour marks the beginning of discipleship — unhurried time in the presence of Jesus. This 'come and see' invitation is the pattern of all Christian formation: not a lecture but a dwelling. The disciples who asked 'where?' became the apostles who knew 'who.' The <em>tenth</em> hour marks the beginning of that transformation.",
     [("John 1:39", "Come and see, Jesus replied. So they went and saw where he was staying, and they spent that day with him. It was about four in the afternoon (<em>the tenth hour</em>)."),
      ("Revelation 11:13", "At that very hour there was a severe earthquake and a <em>tenth</em> of the city collapsed."),
      ("Revelation 21:20", "the fifth sardonyx, the sixth carnelian, the seventh chrysolite, the eighth beryl, the ninth topaz, the <em>tenth</em> turquoise."),
      ("Numbers 7:66", "On the <em>tenth</em> day, Ahiezer son of Ammishaddai, the leader of the people of Dan, brought his offering."),
      ("Leviticus 16:29", "This is to be a lasting ordinance for you: On the <em>tenth</em> day of the seventh month you must deny yourselves.")],
     [("G1176", "Deka (Ten)"), ("G1181", "Dekatē (Tithe)"), ("G3391", "Mia (One/First)")]),
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
