#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch Mar 28 batch2"""
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

# ===== HEBREW WORDS (24 total) =====
hebrew_words = [
    ("H2860", "חָתָן", "Chathan", "Noun, masculine", "Bridegroom; Son-in-Law",
     "The Hebrew <em>chathan</em> refers primarily to a bridegroom — the man who has just entered the covenant of marriage. Related to the concept of becoming bound through marriage, the bridegroom stands as the one who initiates and honors the marriage covenant. The word also extends to son-in-law, capturing family bonds created through marriage.",
     "The image of the bridegroom permeates biblical theology from beginning to end. God describes His relationship to Israel in marital terms (Isaiah 62:5; Hosea 2:19-20). The Psalmist compares the sun to a <em>chathan</em> coming out of his chamber with joy (Psalm 19:5). This imagery reaches its climax in the New Testament where Christ is revealed as the ultimate Bridegroom (Matthew 25:1-13; Revelation 19:7-9) and the Church as His bride. Understanding <em>chathan</em> helps unlock the covenant love that unites the entire biblical narrative.",
     [("Isaiah 62:5", "As a young man marries a young woman, so will your Builder marry you; as a <em>bridegroom</em> rejoices over his bride, so will your God rejoice over you."),
      ("Psalm 19:5", "It is like a <em>bridegroom</em> coming out of his chamber, like a champion rejoicing to run his course."),
      ("Joel 2:16", "Gather the people, consecrate the assembly; bring together the elders, gather the children. Let the <em>bridegroom</em> leave his room and the bride her chamber."),
      ("Jeremiah 7:34", "I will bring an end to the sounds of joy and gladness and to the voices of <em>bride and bridegroom</em> in the towns of Judah and the streets of Jerusalem."),
      ("Song of Songs 3:11", "Come out, daughters of Zion, and look at King Solomon wearing the crown, the crown with which his mother crowned him on his wedding day, the day his heart rejoiced.")],
     [("H3618", "Kallah (Bride)"), ("H157", "Ahav (Love)"), ("H1285", "Berith (Covenant)")]),

    ("H3391", "יֶרַח", "Yerach", "Noun, masculine", "Month; Moon",
     "The Hebrew <em>yerach</em> refers to the lunar month, the basic unit of the Hebrew calendar. The Hebrew calendar is fundamentally lunar, with each month beginning at the new moon. <em>Yerach</em> appears alongside <em>chodesh</em> (H2320, the new moon/month) as a near-synonym, though <em>yerach</em> more specifically emphasizes the full lunar cycle of approximately 29-30 days.",
     "Israel's sacred calendar was divinely structured around the moon's cycles (Genesis 1:14 — lights for signs, seasons, days, years). New Moon celebrations were significant worship occasions (Numbers 10:10; 28:11-15). Psalm 104:19 declares God made the moon for appointed seasons. The Passover, Pentecost, and Feast of Tabernacles were all governed by lunar dating. In this way <em>yerach</em> connects astronomical order to the covenant community's rhythm of worship, rest, and feasting.",
     [("Genesis 1:14", "And God said, 'Let there be lights in the vault of the sky to separate the day from the night, and let them serve as signs to mark sacred times, and days and years.'"),
      ("Psalm 104:19", "He made the moon to mark the seasons, and the sun knows when to go down."),
      ("Numbers 28:14", "With each bull there is to be a drink offering of half a hin of wine; with a ram, a third of a hin; and with a lamb, a quarter of a hin. This is the monthly burnt offering to be made each <em>month</em> throughout the year."),
      ("1 Kings 6:37", "The foundation of the temple of the LORD was laid in the fourth year, in the <em>month</em> of Ziv."),
      ("Deuteronomy 33:14", "With the best gifts of the earth and its fullness and the favor of him who dwelt in the burning bush — let all these rest on the head of Joseph.")],
     [("H2320", "Chodesh (New Moon/Month)"), ("H3394", "Yareah (Moon)"), ("H4150", "Moed (Appointed Time)")]),

    ("H4180", "מוֹרָשׁ", "Morash", "Noun, masculine", "Possession; Inheritance",
     "The Hebrew <em>morash</em> (also <em>morashah</em>) comes from the root <em>yarash</em> (H3423), meaning to seize, dispossess, or inherit. It describes a possession held by right — something that belongs to you either through conquest, inheritance, or divine grant. Closely related to <em>nachalah</em> (inheritance), <em>morash</em> often emphasizes the covenantal right to hold and keep the land.",
     "The land of Canaan was described as <em>morash</em> — Israel's God-given possession (Deuteronomy 33:4; Ezekiel 11:15). Moses' Torah was called <em>morashah</em> — the inheritance of the congregation of Jacob (Deuteronomy 33:4). This rich concept ties together land theology, covenantal promise, and the principle that God is the ultimate landowner who grants to His people what is theirs by grace. The Church inherits a spiritual <em>morash</em> — the kingdom of God — which no earthly power can strip away.",
     [("Deuteronomy 33:4", "Moses gave us the law, an <em>inheritance</em> for the assembly of Jacob."),
      ("Ezekiel 11:15", "Son of man, the people of Jerusalem have said of your fellow exiles, 'They are far away from the LORD; this land was given to us as our <em>possession</em>.'"),
      ("Ezekiel 33:24", "Abraham was only one man, yet he <em>possessed</em> the land. But we are many; surely the land has been given to us as our <em>possession</em>."),
      ("Obadiah 17", "But on Mount Zion will be deliverance; it will be holy, and Jacob will <em>possess</em> his <em>inheritance</em>."),
      ("Numbers 24:18", "Edom will be conquered; Seir, his enemy, will be conquered, but Israel will grow strong.")],
     [("H3423", "Yarash (To Inherit/Dispossess)"), ("H5159", "Nachalah (Inheritance)"), ("H776", "Erets (Land/Earth)")]),

    ("H4539", "מָסָךְ", "Masak", "Noun, masculine", "Curtain; Screen; Covering",
     "The Hebrew <em>masak</em> refers specifically to the woven screen or curtain that covered the entrance to the Tabernacle's outer court, the Holy Place, and the Holy of Holies. It comes from the root <em>sakak</em> (H5526), meaning to cover or screen. These curtains were crafted of fine linen, embroidered with blue, purple, and scarlet yarn — visually magnificent yet serving a barrier function, separating the holy from the common.",
     "The <em>masak</em> curtains of the Tabernacle (Exodus 26:36; 27:16) speak profoundly of access and separation. The veil separating humanity from God's presence was not a permanent barrier but a divinely appointed boundary awaiting the right time and the right Mediator. The tearing of the Temple veil at the crucifixion (Matthew 27:51) was the fulfillment of everything the <em>masak</em> pointed toward — Christ's body opened to give us direct access to the Father (Hebrews 10:19-20).",
     [("Exodus 26:36", "For the entrance to the tent make a <em>curtain</em> of blue, purple and scarlet yarn and finely twisted linen — the work of an embroiderer."),
      ("Exodus 27:16", "For the entrance to the courtyard, provide a <em>curtain</em> twenty cubits long, of blue, purple and scarlet yarn and finely twisted linen."),
      ("Numbers 3:31", "Their care of the ark, the table, the lampstand, the altars, the articles of the sanctuary used in ministering, the <em>curtain</em>, and everything related to their use."),
      ("Hebrews 10:20", "By a new and living way opened for us through the curtain, that is, his body."),
      ("Numbers 4:25", "They are to carry the curtains of the tabernacle and the tent of meeting, its covering, the <em>curtains</em> for the entrance to the tent of meeting.")],
     [("H6532", "Poreketh (Inner Veil/Curtain)"), ("H168", "Ohel (Tent)"), ("H4908", "Mishkan (Tabernacle)")]),

    ("H5110", "נוּד", "Nuwd", "Verb", "To Lament; To Wander; To Show Grief",
     "The Hebrew <em>nuwd</em> encompasses the idea of movement in response to grief. It can mean to move one's head in sorrow or sympathy (a sign of condolence), to wander as a fugitive, or to console and express compassion. When friends visited Job, they came to '<em>nuwd</em>' him — to mourn with him and comfort him. The wandering sense also appears in Cain's curse of being a wanderer on the earth.",
     "The ministry of presence in grief is captured by <em>nuwd</em>. When Scripture says to 'mourn with those who mourn' (Romans 12:15), the Old Testament background is this word — the physical act of nodding, weeping, and sitting with the suffering. <em>Nuwd</em> also appears in prophetic laments over fallen cities. Conversely, when God's people suffered, the lack of <em>nuwd</em>-ers was itself a judgment (Psalm 69:20) — the complete isolation of having no one to grieve alongside you.",
     [("Job 2:11", "When Job's three friends heard about all the troubles that had come upon him, they met together by agreement to go and <em>sympathize</em> with him and comfort him."),
      ("Psalm 69:20", "Scorn has broken my heart and has left me helpless; I looked for sympathy, but there was none, for <em>comforters</em>, but I found none."),
      ("Jeremiah 18:16", "Their land will be laid waste, an object of lasting scorn; all who pass by will be appalled and will <em>shake their heads</em>."),
      ("Genesis 4:12", "When you work the ground, it will no longer yield its crops for you. You will be a restless <em>wanderer</em> on the earth."),
      ("Jeremiah 15:5", "Who will have pity on you, Jerusalem? Who will <em>mourn for you</em>? Who will stop to ask how you are?")],
     [("H5162", "Nacham (To Comfort/Repent)"), ("H56", "Abal (To Mourn)"), ("H1058", "Bakah (To Weep)")]),

    ("H5164", "נֹחַם", "Nocham", "Noun, masculine", "Repentance; Consolation; Regret",
     "The Hebrew <em>nocham</em> is the noun form of <em>nacham</em> (H5162), meaning to be comforted or to repent/relent. It carries the full theological weight of its verbal root — the concept of a deep inner change that moves from grief to comfort, or from one course of action to another. In Hosea 13:14, God declares He will have no <em>nocham</em> from bringing redemption — His resolve is fixed and sure.",
     "<em>Nocham</em> sits at the intersection of divine pathos and covenant faithfulness. When God 'repents' or 'relents' in Scripture, it reflects His responsive love — His covenant heart reacting to human repentance or stubbornness. This concept is foundational to understanding a God who is not static but dynamically engaged with His creation, grieving over sin while determined to bring comfort and redemption to those who turn to Him.",
     [("Hosea 13:14", "I will deliver this people from the power of the grave; I will redeem them from death. Where, O death, are your plagues? Where, O grave, is your destruction? I will have no <em>compassion</em>."),
      ("Isaiah 57:18", "I have seen their ways, but I will heal them; I will guide them and restore <em>comfort</em> to Israel's mourners."),
      ("Jeremiah 16:7", "No one will offer food to comfort those who mourn for the dead — not even for a father or a mother — nor will anyone give them a drink of <em>consolation</em>."),
      ("Zechariah 1:13", "So the LORD spoke kind and <em>comforting</em> words to the angel who talked with me."),
      ("Psalm 119:52", "I remember, LORD, your ancient laws, and I find <em>comfort</em> in them.")],
     [("H5162", "Nacham (To Comfort/Relent)"), ("H8575", "Tanchumim (Consolations)"), ("H3068", "YHWH (The LORD)")]),

    ("H5391", "נָשַׁךְ", "Nashak", "Verb", "To Bite; To Charge Interest",
     "The Hebrew <em>nashak</em> has two distinct applications unified by the idea of harmful extraction. Literally it means to bite — used of a serpent's fatal bite (Numbers 21:6-9). Figuratively, it describes the practice of charging interest on loans, particularly to fellow Israelites — a practice condemned throughout the Law because it 'bites' the borrower into deeper poverty. The imagery is vivid: usury is likened to a venomous serpent.",
     "The connection between <em>nashak</em> (to bite) and lending at interest reveals God's economic ethics. The Torah forbade charging interest to fellow Israelites (Exodus 22:25; Leviticus 25:36-37) — lending was to be an act of covenant solidarity, not profit extraction. The prophets condemned usury as oppression of the poor (Ezekiel 18:8, 13; 22:12). The serpent that bites economically is as dangerous as the one in the wilderness — and the bronze serpent lifted by Moses (a type of Christ) healed those bitten, pointing to redemption from every curse.",
     [("Numbers 21:6", "Then the LORD sent venomous snakes among them; they <em>bit</em> the people and many Israelites died."),
      ("Exodus 22:25", "If you lend money to one of my people among you who is needy, do not treat it like a business deal; charge no <em>interest</em>."),
      ("Habakkuk 2:7", "Will not your creditors suddenly arise? Will they not wake up and make you tremble? Then you will become their prey."),
      ("Ezekiel 18:8", "He does not lend to them at <em>interest</em> or take a profit from them. He withholds his hand from doing wrong and judges fairly between two parties."),
      ("Psalm 15:5", "Who lends money to the poor without <em>interest</em>; who does not accept a bribe against the innocent. Whoever does these things will never be shaken.")],
     [("H5383", "Nasha (To Lend)"), ("H1215", "Betsa (Unjust Gain)"), ("H4855", "Mashsha (Usury)")]),

    ("H5534", "סָכַר", "Sakar", "Verb", "To Shut Up; To Barricade; To Hand Over",
     "The Hebrew <em>sakar</em> means to shut or close — barricading a passage or stopping it up. In some instances it carries the sense of delivering someone up or surrendering them, as when the men of Keilah were going to '<em>sakar</em>' David into Saul's hands. The word captures the idea of sealing off any escape — complete enclosure or entrapment.",
     "The concept of being 'shut in' or 'handed over' carries deep theological resonance. God sometimes shuts up enemies, delivering them into the hands of His servants. The flip side is the fear of being handed over to one's enemies — a theme of lament and petition throughout the Psalms. Understanding <em>sakar</em> helps illuminate passages about divine protection (God closing the way of danger) versus divine judgment (God surrendering the rebellious to the consequences of their sin).",
     [("1 Samuel 23:11", "Will the citizens of Keilah <em>surrender</em> me to him? Will Saul come down, as your servant has heard? LORD, God of Israel, tell your servant. And the LORD said, 'He will come down.'"),
      ("1 Samuel 23:12", "Again David asked, 'Will the citizens of Keilah <em>surrender</em> me and my men to Saul?' And the LORD said, 'They will.'"),
      ("Deuteronomy 32:30", "How could one man chase a thousand, or two put ten thousand to flight, unless their Rock had <em>sold</em> them, unless the LORD had given them up?"),
      ("Psalm 44:12", "You sold your people for a pittance, gaining nothing from their sale."),
      ("Isaiah 19:4", "I will hand the Egyptians over to the power of a cruel master, and a fierce king will rule over them, declares the Lord, the LORD Almighty.")],
     [("H5462", "Sagar (To Shut/Close)"), ("H4042", "Magan (To Deliver Up)"), ("H3027", "Yad (Hand)")]),

    ("H5688", "עָבֹת", "Avoth", "Noun, masculine/plural", "Thick Cords; Ropes; Braided Branches",
     "The Hebrew <em>avoth</em> (plural of <em>avat</em>) refers to thick, braided, interwoven cords or ropes — the kind used for restraining animals, hanging the Temple lamp, or describing the intertwined branches of a thick tree. The image is of multiple strands twisted together for strength, each strand amplifying the other.",
     "The imagery of <em>avoth</em> speaks to covenantal binding and the strength of unity. Ecclesiastes 4:12 says 'a cord of three strands is not quickly broken' — the principle that unity and interweaving creates strength that single strands cannot provide. God's bonds upon His people are described with this language — not as oppressive imprisonment but as life-giving connection. The cords of love and human kinship (Hosea 11:4) mirror this concept of strength through interweaving.",
     [("Judges 15:13", "They answered him, 'We will only tie you up and hand you over to them. We will not kill you.' So they bound him with two new <em>ropes</em> and led him up from the rock."),
      ("Psalm 2:3", "Let us break their chains and throw off their <em>shackles</em>."),
      ("Ezekiel 19:11", "Its branches were strong, fit for a ruler's scepter. It towered high above the thick foliage, conspicuous for its height and for its many <em>branches</em>."),
      ("Ecclesiastes 4:12", "Though one may be overpowered, two can defend themselves. A <em>cord</em> of three strands is not quickly broken."),
      ("Job 39:10", "Can you hold a wild ox to the furrow with a harness? Will he till the valleys behind you? Can you bind a wild donkey with his <em>ropes</em>?")],
     [("H2256", "Chevel (Rope/Band/Territory)"), ("H4147", "Moser (Bond/Chain)"), ("H631", "Asar (To Bind)")]),

    ("H5742", "עָדָשׁ", "Adash", "Noun, masculine", "Lentils",
     "The Hebrew <em>adash</em> refers to lentils — a staple legume in the ancient Near East. Small red or green lentil seeds were made into a thick, brownish-red pottage. Lentils appear at one of the most dramatic moments in biblical narrative — Esau's fateful trade of his birthright to Jacob for a bowl of red lentil stew (Genesis 25:29-34). They also appear as provisions brought to David at Mahanaim (2 Samuel 17:28) and in Ezekiel's symbolic bread (Ezekiel 4:9).",
     "The bowl of lentil stew in Genesis 25 is far more than a culinary detail. Esau's willingness to exchange his <em>birthright</em> — the covenantal inheritance passing through Abraham and Isaac — for immediate physical gratification became a defining moment in redemptive history. Hebrews 12:16 warns against being like Esau — profane, trading eternal inheritance for momentary appetite. The lentils symbolize the perennial danger of valuing the temporal over the eternal, of satisfying the flesh at the cost of covenant faithfulness.",
     [("Genesis 25:34", "Then Jacob gave Esau some bread and some <em>lentil</em> stew. He ate and drank, and then got up and left. So Esau despised his birthright."),
      ("2 Samuel 23:11", "Next to him was Shammah son of Agee the Hararite. When the Philistines banded together at a place where there was a field full of <em>lentils</em>, Israel's troops fled from them."),
      ("Ezekiel 4:9", "Take wheat and barley, beans and <em>lentils</em>, millet and spelt; put them in a storage jar and use them to make bread for yourself."),
      ("Genesis 25:29", "Once when Jacob was cooking some stew, Esau came in from the open country, famished."),
      ("Hebrews 12:16", "See that no one is godless like Esau, who for a single meal sold his inheritance rights as the oldest son.")],
     [("H1062", "Bekorah (Birthright/Firstborn)"), ("H3290", "Yaaqov (Jacob)"), ("H6215", "Esav (Esau)")]),

    ("H5937", "עָלַז", "Alaz", "Verb", "To Exult; To Rejoice Triumphantly",
     "The Hebrew <em>alaz</em> describes a vigorous, exuberant, often vocal rejoicing — the kind of joy that spills out in triumph and celebration. It is more intense than mere happiness, carrying the connotation of exultation after victory. The word appears in contexts of military triumph, divine salvation, and eschatological celebration.",
     "<em>Alaz</em> captures the joy of salvation — not a quiet, subdued relief but a triumphant shout. The righteous are called to <em>alaz</em> in the Lord (Psalm 28:7; 68:3). This is the joy of those who know they have been saved by a greater power than their own. In the prophets, <em>alaz</em> anticipates the eschatological celebration when God finally vindicates His people and restores all things. The Christian finds this joy already inaugurated in the resurrection of Christ.",
     [("Psalm 28:7", "The LORD is my strength and my shield; my heart trusts in him, and he helps me. My heart <em>leaps for joy</em>, and with my song I praise him."),
      ("Psalm 68:3", "But may the righteous be glad and <em>rejoice</em> before God; may they be happy and joyful."),
      ("Proverbs 23:24", "The father of a righteous child has great joy; a man who fathers a wise son <em>rejoices</em> in him."),
      ("Zephaniah 3:14", "Sing, Daughter Zion; shout aloud, Israel! Be glad and <em>rejoice</em> with all your heart, Daughter Jerusalem!"),
      ("1 Samuel 2:1", "Then Hannah prayed: 'My heart <em>rejoices</em> in the LORD; in the LORD my horn is lifted high.'")],
     [("H8055", "Samach (To Rejoice/Be Glad)"), ("H1523", "Giyl (To Rejoice/Exult)"), ("H7442", "Ranan (To Shout for Joy)")]),

    ("H6175", "עָרוּם", "Arum", "Adjective", "Shrewd; Crafty; Prudent",
     "The Hebrew <em>arum</em> describes a quality of sharp intelligence or shrewdness that can manifest as either wisdom or cunning. The same word describes the serpent in Eden (Genesis 3:1 — 'more crafty than any of the wild animals') and also the wise person who thinks before acting (Proverbs 12:16, 23; 13:16; 14:8, 15). Context determines whether the connotation is positive (prudent, sensible) or negative (scheming, sly).",
     "The Eden narrative uses <em>arum</em> for the serpent's cunning, playing on its similarity to <em>arummim</em> (naked) used of Adam and Eve. The serpent's cleverness exploited their innocence. In Proverbs, the same quality — redirected toward wisdom — becomes a virtue. This duality reflects the biblical view that human capacities are not inherently good or evil; their moral character depends on their direction. Wisdom submitted to God becomes true <em>arum</em>; wisdom turned against God becomes diabolical cunning.",
     [("Genesis 3:1", "Now the serpent was more <em>crafty</em> than any of the wild animals the LORD God had made. He said to the woman, 'Did God really say, You must not eat from any tree in the garden?'"),
      ("Proverbs 12:16", "Fools show their annoyance at once, but the <em>prudent</em> overlook an insult."),
      ("Proverbs 13:16", "All who are <em>prudent</em> act with knowledge, but fools expose their folly."),
      ("Proverbs 14:15", "The simple believe anything, but the <em>prudent</em> give thought to their steps."),
      ("Job 5:12", "He thwarts the plans of the <em>crafty</em>, so that their hands achieve no success.")],
     [("H2449", "Chakam (To Be Wise)"), ("H995", "Bin (To Understand/Discern)"), ("H3820", "Lev (Heart/Mind)")]),

    ("H6482", "פֶּצַע", "Petsa", "Noun, masculine", "Wound; Bruise; Stripe",
     "The Hebrew <em>petsa</em> refers to a wound, bruise, or stripe caused by a blow — the physical mark left by beating, lashing, or cutting. It is a vivid, concrete word evoking the visible evidence of violence on a body. This word appears in legal contexts (injury requiring compensation), in wisdom literature (discipline), and most significantly in the great Servant Song of Isaiah 52-53.",
     "Isaiah 53:5 is the theological summit of <em>petsa</em>: 'He was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was upon him, and by his <em>wounds</em> [petsa] we are healed.' The specific word <em>petsa</em> — a visible, physical wound — emphasizes the bodily reality of the Servant's suffering. The wounds that heal are not metaphorical. Peter quotes this passage directly in 1 Peter 2:24, applying it to the crucifixion of Christ.",
     [("Isaiah 53:5", "But he was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his <em>wounds</em> we are healed."),
      ("Proverbs 20:30", "Blows and <em>wounds</em> cleanse away evil, and beatings purge the inmost being."),
      ("Proverbs 27:6", "<em>Wounds</em> from a friend can be trusted, but an enemy multiplies kisses."),
      ("Exodus 21:25", "burn for burn, <em>wound</em> for wound, bruise for bruise."),
      ("1 Peter 2:24", "He himself bore our sins in his body on the cross, so that we might die to sins and live for righteousness; by his <em>wounds</em> you have been healed.")],
     [("H2250", "Chabbuwrah (Bruise/Stripe)"), ("H4347", "Makkah (Blow/Wound/Plague)"), ("H7495", "Rapha (To Heal)")]),

    ("H7111", "קְצָפָה", "Qetsaphah", "Noun, feminine", "Wrath; Splinters; Breaking Off",
     "The Hebrew <em>qetsaphah</em> derives from <em>qatsaph</em> (H7107), meaning to be angry or burst out in rage. As a noun it describes God's wrath poured out, or — in one usage — the broken-off fragments that result when something is shattered. The word captures the explosive nature of wrath: like something violently broken, shattering into pieces.",
     "Divine wrath in the Old Testament is not mere irritation but <em>qetsaphah</em> — the explosive response of infinite holiness to human covenant-breaking. Zechariah 1:15 shows God angry with the nations who exceeded His chastisement of Israel, while earlier generations suffered under God's fierce anger in the wilderness. Understanding <em>qetsaphah</em> is essential for grasping the gravity of sin and the wonder of grace — that God's wrath against our sin was absorbed by the Suffering Servant (Isaiah 53) rather than poured out on us.",
     [("Zechariah 1:15", "And I am very angry with the nations that feel secure. I was only a little angry, but they went too far with the punishment."),
      ("Isaiah 34:2", "The LORD is angry with all nations; his wrath is on all their armies. He will totally destroy them."),
      ("2 Kings 3:27", "There came great <em>wrath</em> against Israel, and they withdrew and returned to their own land."),
      ("Ezra 7:23", "Whatever the God of heaven has prescribed, let it be done diligently for the temple of the God of heaven. Why should his <em>wrath</em> fall on the realm of the king and of his sons?"),
      ("Isaiah 54:8", "In a surge of <em>anger</em> I hid my face from you for a moment, but with everlasting kindness I will have compassion on you, says the LORD your Redeemer.")],
     [("H7107", "Qatsaph (To Be Angry/Furious)"), ("H639", "Aph (Nostril/Anger)"), ("H2534", "Chemah (Wrath/Burning Anger)")]),

    ("H7305", "רֶוַח", "Revach", "Noun, masculine", "Space; Relief; Breathing Room",
     "The Hebrew <em>revach</em> comes from <em>ravach</em> (H7304), meaning to be wide or spacious, to breathe freely. As a noun it describes the experience of having space — whether physical space between animals, or the experiential relief that comes when pressure is released. Esther 4:14 famously uses <em>revach</em>: if Esther stays silent, 'relief and deliverance will arise for the Jews from another place.'",
     "The spiritual resonance of <em>revach</em> is profound. Being 'hemmed in' by enemies, circumstances, or sin is a recurrent biblical image of distress. The Psalms often cry out from constricted places (<em>metzar</em> — narrow straits) and praise God for bringing into a 'wide place' (<em>merchab</em>). <em>Revach</em> captures salvation as spaciousness — God making room, lifting pressure, restoring freedom. Esther 4:14 implies that God's purposes never fail — if one instrument refuses, He will make <em>revach</em> through another.",
     [("Esther 4:14", "For if you remain silent at this time, <em>relief and deliverance</em> for the Jews will arise from another place, but you and your father's family will perish."),
      ("Genesis 32:16", "He put them in the care of his servants, each herd by itself, and said to his servants, 'Go ahead of me, and keep some <em>space</em> between the herds.'"),
      ("Psalm 118:5", "When hard pressed, I cried to the LORD; he brought me into a <em>spacious place</em>."),
      ("Psalm 31:8", "You have not given me into the hands of the enemy but have set my feet in a <em>spacious place</em>."),
      ("Job 36:16", "He is wooing you from the jaws of distress to a <em>spacious place</em> free from restriction.")],
     [("H7304", "Ravach (To Breathe/Be Spacious)"), ("H4800", "Merchab (Broad/Spacious Place)"), ("H3444", "Yeshuah (Salvation/Deliverance)")]),

    ("H7399", "רְכוּשׁ", "Rekush", "Noun, masculine", "Property; Goods; Substance",
     "The Hebrew <em>rekush</em> refers to movable property — goods, cattle, and wealth accumulated through labor or acquisition. It appears frequently in narratives of migration and conquest: Abraham left Egypt with great <em>rekush</em> (Genesis 12:5; 13:6), Lot and Abraham's combined <em>rekush</em> was so great the land couldn't support them both, and Israel left Egypt with Egypt's <em>rekush</em> (plunder).",
     "The <em>rekush</em> of the patriarchs represents God's covenant blessing made tangible in history. God promised Abraham He would bless him and make him great (Genesis 12:2), and <em>rekush</em> was one visible sign of that blessing. Yet the same <em>rekush</em> that blessed could also separate — Lot's separation from Abraham was caused by their combined <em>rekush</em> (Genesis 13:6). Wealth is a test of character and stewardship; the question Scripture always asks is what we do with the <em>rekush</em> God has entrusted to us.",
     [("Genesis 12:5", "He took his wife Sarai, his nephew Lot, all the possessions (<em>rekush</em>) they had accumulated and the people they had acquired in Harran, and they set out for the land of Canaan."),
      ("Genesis 13:6", "But the land could not support them while they stayed together, for their possessions (<em>rekush</em>) were so great that they were not able to stay together."),
      ("Genesis 15:14", "But I will punish the nation they serve as slaves, and afterward they will come out with great possessions (<em>rekush</em>)."),
      ("Ezra 8:21", "There, by the Ahava Canal, I proclaimed a fast, so that we might humble ourselves before our God and ask him for a safe journey for us and our children, with all our possessions (<em>rekush</em>)."),
      ("Proverbs 13:22", "A good person leaves an inheritance for their children's children, but a sinner's wealth is stored up for the righteous.")],
     [("H5233", "Nekeseh (Wealth/Property)"), ("H1952", "Hon (Wealth/Substance)"), ("H5159", "Nachalah (Inheritance)")]),

    ("H8041", "שָׂמַאל", "Samal", "Verb", "To Go to the Left; To Use the Left Hand",
     "The Hebrew <em>samal</em> means to go to the left, take the left direction, or use the left hand. Its counterpart is <em>yaman</em> (H3231), to go right. In Hebrew culture, the right hand was the hand of strength, blessing, and honor (Genesis 48:14-17). The left was not shameful but was secondary — associated with the north when facing east, and with the lesser position.",
     "The right-left contrast in Scripture carries theological weight. God's right hand saves and sustains (Psalm 18:35; 63:8; 118:16). To 'turn neither to the right nor to the left' from God's commands means strict covenant faithfulness (Deuteronomy 5:32; 28:14). God holds His people with His right hand (Isaiah 41:10). Ecclesiastes 10:2 states the wise man's heart is at his right and the fool's heart at his left. Understanding <em>samal</em> helps interpret blessing narratives, the divine warrior motif, and Christ seated at the Father's right hand.",
     [("Ecclesiastes 10:2", "The heart of the wise inclines to the right, but the heart of the fool to the left."),
      ("Genesis 13:9", "Is not the whole land before you? Let's part company. If you go to the <em>left</em>, I'll go to the right; if you go to the right, I'll go to the <em>left</em>."),
      ("2 Samuel 14:19", "As surely as you live, my lord the king, no one can turn to the right or to the <em>left</em> from anything my lord the king says."),
      ("Ezekiel 21:16", "Slash to the right, you sword, then to the <em>left</em>, wherever your blade is turned."),
      ("Isaiah 54:3", "For you will spread out to the right and to the <em>left</em>; your descendants will dispossess nations and settle in their desolate cities.")],
     [("H3231", "Yaman (To Go to the Right)"), ("H3225", "Yamin (Right Hand/Right Side)"), ("H3027", "Yad (Hand/Power)")]),

    ("H8437", "תּוֹלָל", "Towlal", "Noun, masculine", "Oppressor; Tormentor",
     "The Hebrew <em>towlal</em> appears only in Psalm 137:3, describing those who caused the exiles anguish — demanding songs of joy in a foreign land. Related to the root meaning to howl or wail, <em>towlal</em> describes one who makes others wail: an oppressor who inflicts deep emotional torment on the vulnerable.",
     "Psalm 137 is one of the most raw and honest laments in Scripture, arising from the Babylonian exile. The exiles sat by the rivers of Babylon and wept — they could not sing the LORD's songs in a foreign land. Their <em>towlal</em> — oppressors — mockingly demanded worship songs as entertainment. This psalm captures the theology of lament: God's people may cry out their anguish in the confidence that God hears and remembers. The memory of Zion and the faithfulness of God sustain the community even in crushing oppression.",
     [("Psalm 137:3", "For there our captors asked us for songs, our <em>tormentors</em> demanded songs of joy; they said, 'Sing us one of the songs of Zion!'"),
      ("Psalm 137:1", "By the rivers of Babylon we sat and wept when we remembered Zion."),
      ("Lamentations 1:5", "Her foes have become her masters; her enemies are at ease. The LORD has brought her grief because of her many sins. Her children have gone into exile, captive before the foe."),
      ("Psalm 74:10", "How long will the enemy mock you, God? Will the foe revile your name forever?"),
      ("Isaiah 49:26", "I will make your oppressors eat their own flesh; they will be drunk on their own blood, as with wine.")],
     [("H3238", "Yanah (To Oppress/Mistreat)"), ("H6031", "Anah (To Afflict/Humble)"), ("H1350", "Gaal (Kinsman-Redeemer)")]),

    ("H8551", "תָּמַךְ", "Tamak", "Verb", "To Uphold; To Support; To Take Hold Of",
     "The Hebrew <em>tamak</em> describes the action of holding something or someone up — sustaining, supporting, or maintaining. It is used of God upholding His servants (Psalm 41:12; 63:8), of wisdom being held fast (Proverbs 3:18; 4:6), and of hands that grip and sustain. The word implies not merely touching but actively holding — bearing the weight, preventing the fall.",
     "The image of God <em>tamak</em>-ing His people is one of the most intimate and reassuring in the Psalms. Psalm 63:8 — 'Your right hand <em>upholds</em> me' — uses <em>tamak</em> to describe the experiential reality of divine sustaining during suffering. Psalm 41:12 says God upholds the person of integrity. This is not a distant God who watches from afar but One whose grip is active, present, and powerful. Isaiah 42:1 opens the first Servant Song: 'Here is my servant, whom I <em>uphold</em>' — using <em>tamak</em> of God's relationship to the Messiah.",
     [("Psalm 41:12", "Because of my integrity you <em>uphold</em> me and set me in your presence forever."),
      ("Psalm 63:8", "I cling to you; your right hand <em>upholds</em> me."),
      ("Proverbs 3:18", "She is a tree of life to those who take hold of her; those who hold her fast will be blessed."),
      ("Isaiah 42:1", "Here is my servant, whom I <em>uphold</em>, my chosen one in whom I delight; I will put my Spirit on him, and he will bring justice to the nations."),
      ("Proverbs 4:6", "Do not forsake wisdom, and she will protect you; love her, and she will watch over you.")],
     [("H5564", "Samak (To Support/Lean/Lay on)"), ("H2388", "Chazaq (To Strengthen/Hold)"), ("H3027", "Yad (Hand/Power)")]),

    # 5 additional Hebrew
    ("H2832", "חַרְשַׁנִּים", "Charshannîm", "Noun, masculine plural", "Craftsmen; Artisans",
     "The Hebrew <em>charshannîm</em> refers to craftsmen or skilled artisans — workers in wood, stone, or metal. The word appears in Zechariah 1:20 where four craftsmen (charshannîm) are sent to terrify and throw down the four horns that scattered Judah. It also appears in Nehemiah's lists of those who returned from exile, including craftsmen among the resettled communities.",
     "The four <em>charshannîm</em> in Zechariah's vision represent divine agents sent to oppose every force that has scattered God's people. Where the four horns represent the hostile world powers that have driven Israel into exile, the four craftsmen represent God's counter-movement — His workers who will tear down what oppressed His people. The imagery of craftsmen as agents of divine restoration is fitting: they are builders who also demolish the old to make way for the new. God is always at work constructing His purposes in history.",
     [("Zechariah 1:20", "Then the LORD showed me four <em>craftsmen</em>."),
      ("Zechariah 1:21", "I asked, 'What are these coming to do?' He answered, 'These are the horns that scattered Judah so that no one could raise their head, but the <em>craftsmen</em> have come to terrify them.'"),
      ("Nehemiah 11:35", "Lod and Ono, the valley of the <em>craftsmen</em>."),
      ("1 Chronicles 4:14", "Meonothai was the father of Ophrah. Seraiah was the father of Joab, the father of Ge Harashim. It was called this because its people were <em>craftsmen</em>."),
      ("Isaiah 44:13", "The <em>carpenter</em> measures with a line and makes an outline with a marker; he roughs it out with chisels and marks it with compasses.")],
     [("H2796", "Charash (Craftsman/Artisan)"), ("H542", "Amon (Master Craftsman)"), ("H4399", "Melakah (Work/Craft)")]),

    ("H3357", "יַקִּיר", "Yaqqir", "Adjective", "Dear; Precious; Costly",
     "The Hebrew <em>yaqqir</em> describes something or someone who is precious, costly, or dear. The word appears in Jeremiah 31:20 where God calls Ephraim His 'dear son' — a treasured, precious child. Related to the root meaning to be heavy or costly, <em>yaqqir</em> captures the preciousness of something valued so highly that its loss would be grievous.",
     "God's declaration of Ephraim as His '<em>yaqqir</em> son' (Jeremiah 31:20) is one of the most tender expressions of divine pathos in the entire Old Testament. Despite Israel's rebellion and exile, God's heart still yearns for them: 'Is not Ephraim my dear son, the child in whom I delight? Though I often speak against him, I still remember him. Therefore my heart yearns for him; I have great compassion for him.' This love — costly, cherishing, parental — is the foundation of the New Covenant (Jeremiah 31:31-34). Believers in Christ are God's beloved, precious children.",
     [("Jeremiah 31:20", "Is not Ephraim my dear son, the child in whom I delight? Though I often speak against him, I still remember him. Therefore my heart yearns for him; I have great compassion for him."),
      ("Proverbs 17:8", "A bribe is seen as a charm by the one who gives it; they think success will come at every turn."),
      ("Lamentations 4:2", "How the precious children of Zion, once worth their weight in gold, are now considered as pots of clay, the work of a potter's hands!"),
      ("Isaiah 43:4", "Since you are precious and honored in my sight, and because I love you, I will give people in exchange for you, nations in exchange for your life."),
      ("Psalm 139:17", "How precious to me are your thoughts, God! How vast is the sum of them!")],
     [("H3368", "Yaqar (Precious/Costly/Rare)"), ("H157", "Ahav (To Love)"), ("H2617", "Hesed (Lovingkindness/Covenant Love)")]),

    ("H3400", "יְקָרָה", "Yeqarah", "Noun, feminine", "Preciousness; Honor; Splendor",
     "The Hebrew <em>yeqarah</em> is the noun form expressing preciousness, honor, costliness, or splendor. It comes from the root <em>yaqar</em> (H3368), meaning to be precious or rare. <em>Yeqarah</em> appears in poetic and wisdom contexts to describe the incomparable value of wisdom over silver and gold, and in prophetic contexts describing divine glory and honor.",
     "Proverbs and Job celebrate wisdom as a <em>yeqarah</em> beyond all material wealth (Job 28:10). In Zechariah's vision, precious stones and splendor attend the divine restoration of Jerusalem (Zechariah 14:6). The concept bridges earthly beauty and divine glory — what is truly precious in God's eyes transcends market value. Understanding <em>yeqarah</em> reorients our values: the wisdom, knowledge of God, and righteousness that Scripture calls precious are the true wealth, more <em>yeqarah</em> than rubies.",
     [("Proverbs 3:15", "She is more precious than rubies; nothing you desire can compare with her."),
      ("Job 28:10", "It cuts channels through the rocks; its eyes see all its treasures. It searches the sources of the rivers and brings hidden things to light."),
      ("Zechariah 14:6", "On that day there will be neither sunlight nor cold, frosty darkness."),
      ("Proverbs 20:15", "Gold there is, and rubies in abundance, but lips that speak knowledge are a rare jewel."),
      ("Isaiah 28:16", "See, I lay a stone in Zion, a tested stone, a precious cornerstone for a sure foundation.")],
     [("H3368", "Yaqar (Precious/Rare/Honored)"), ("H5459", "Segullah (Special Treasure)"), ("H2451", "Chokmah (Wisdom)")]),

    ("H6010", "עֵמֶק", "Emeq", "Noun, masculine", "Valley; Plain",
     "The Hebrew <em>emeq</em> refers to a valley or lowland plain — a broad, open depression between hills or mountains. Unlike the narrow <em>gai</em> (ravine/gorge), an <em>emeq</em> is typically wider and more open. Famous <em>emeqs</em> include the Valley of Jezreel (Megiddo), the Valley of Elah (where David fought Goliath), and the Valley of Hinnom. These geographical features were sites of major battles, significant encounters, and prophetic visions.",
     "The <em>emeq</em> in Scripture is often a place of decisive encounter — military, spiritual, or divine. The Valley of Dry Bones (Ezekiel 37) was an <em>emeq</em> transformed by the Spirit into a scene of resurrection. Joel's Valley of Jehoshaphat (Joel 3:2,12) — likely an <em>emeq</em> — is the site of God's final judgment of the nations. Psalm 23's 'valley of the shadow of death' (<em>gai tsalmaveth</em>) uses a related but narrower term, but the <em>emeq</em> tradition reminds us that the low places of life are often where God's most dramatic interventions occur.",
     [("Ezekiel 37:1", "The hand of the LORD was on me, and he brought me out by the Spirit of the LORD and set me in the middle of a <em>valley</em>; it was full of bones."),
      ("1 Samuel 17:2", "Saul and the Israelites assembled and camped in the <em>Valley</em> of Elah and drew up their battle line to meet the Philistines."),
      ("Joel 3:2", "I will gather all nations and bring them down to the <em>Valley</em> of Jehoshaphat. There I will put them on trial."),
      ("Judges 5:15", "In the <em>valleys</em> of Reuben there were great searchings of heart."),
      ("Isaiah 22:7", "Your choicest <em>valleys</em> are full of chariots, and horsemen are posted at the city gates.")],
     [("H1516", "Gai (Valley/Ravine)"), ("H2022", "Har (Mountain/Hill)"), ("H4324", "Mayim (Waters)")]),
]

# ===== GREEK WORDS (23 total) =====
greek_words = [
    ("G1553", "ἐκδημέω", "Ekdēmeō", "Verb", "To Be Absent from Home; To Emigrate",
     "The Greek <em>ekdēmeō</em> means to be away from home — to emigrate or be absent from one's native place. Paul uses it in 2 Corinthians 5:6-9 to contrast being 'at home in the body' (<em>endēmeō</em>) with being 'away from the Lord,' and 'away from the body' (<em>ekdēmeō</em>) with being 'at home with the Lord.' The word frames the entire Christian life as a journey between two homes.",
     "Paul's use of <em>ekdēmeō</em> in 2 Corinthians 5 is one of the most profound NT meditations on death, resurrection, and the believer's longing. To be 'at home' in the body is to be in exile from the Lord's immediate presence. To <em>ekdēmeō</em> from the body — to die — is to arrive home with the Lord. This does not mean Paul minimizes bodily life (he wants to be clothed, not naked — v.4), but that his deepest orientation is always toward the greater home. For the believer, death is not departure but arrival.",
     [("2 Corinthians 5:6", "Therefore we are always confident and know that as long as we are at home in the body we are <em>away from</em> the Lord."),
      ("2 Corinthians 5:8", "We are confident, I say, and would prefer to be <em>away from</em> the body and at home with the Lord."),
      ("2 Corinthians 5:9", "So we make it our goal to please him, whether we are at home in the body or <em>away from</em> it."),
      ("Philippians 1:23", "I am torn between the two: I desire to depart and be with Christ, which is better by far."),
      ("John 14:2", "My Father's house has many rooms; if that were not so, would I have told you that I am going there to prepare a place for you?")],
     [("G1736", "Endēmeō (To Be at Home)"), ("G3939", "Paroikeō (To Live as a Stranger)"), ("G4864", "Synagōgē (Assembly)")]),

    ("G1557", "ἐκδίκησις", "Ekdikēsis", "Noun, feminine", "Vengeance; Justice; Vindication",
     "The Greek <em>ekdikēsis</em> means the execution of justice — punishment of the guilty or vindication of the wronged. It is used of God's judicial vengeance (Romans 12:19; 2 Thessalonians 1:8), of the widow's plea for justice from the judge (Luke 18:7-8), and of the Thessalonians' suffering and God's just response. The word combines the ideas of punishing evil and defending the vulnerable.",
     "The theology of <em>ekdikēsis</em> is not about revenge but about the restoration of right order by the only Judge who has perfect knowledge and perfect justice. Paul's command 'do not take revenge' (Romans 12:19) is grounded in God's own <em>ekdikēsis</em> — 'It is mine to avenge; I will repay, says the Lord.' Leaving vengeance to God is not passivity but an act of profound faith: trusting that the One who sees all will execute perfect justice. The widow's persistent prayer for <em>ekdikēsis</em> (Luke 18:3) is a model of persistent intercession.",
     [("Romans 12:19", "Do not take revenge, my dear friends, but leave room for God's wrath, for it is written: 'It is mine to avenge; I will repay,' says the Lord."),
      ("Luke 18:7", "And will not God bring about justice (<em>ekdikēsis</em>) for his chosen ones, who cry out to him day and night?"),
      ("Luke 18:8", "I tell you, he will see that they get justice (<em>ekdikēsis</em>), and quickly. However, when the Son of Man comes, will he find faith on the earth?"),
      ("2 Thessalonians 1:8", "He will punish those who do not know God and do not obey the gospel of our Lord Jesus."),
      ("Hebrews 10:30", "For we know him who said, 'It is mine to avenge; I will repay,' and again, 'The Lord will judge his people.'")],
     [("G1558", "Ekdikos (Avenger/Punisher)"), ("G2920", "Krisis (Judgment)"), ("G1343", "Dikaiosynē (Righteousness/Justice)")]),

    ("G1559", "ἐκδιώκω", "Ekdiōkō", "Verb", "To Persecute; To Drive Out Completely",
     "The Greek <em>ekdiōkō</em> is an intensified form of <em>diōkō</em> (to pursue/persecute), with the prefix <em>ek</em> indicating thoroughness or completion. It means to drive out completely, to persecute with the intent of total expulsion. In Luke 11:49, Jesus prophesies that some of God's messengers will be killed and others <em>ekdiōkō</em> — persecuted and expelled. Paul uses it in 1 Thessalonians 2:15 describing those who killed Jesus and persecuted the apostles.",
     "The escalating intensity of <em>ekdiōkō</em> — total, driving-out persecution — reflects the reality that the gospel has always provoked violent opposition from those whose power it threatens. Paul describes this in his own experience (Galatians 1:13; 1 Corinthians 15:9) — he himself was once the one doing the <em>ekdiōkō</em> before the Damascus encounter transformed him. The church's suffering through persecution has historically been the very means by which the gospel spreads — the scattered become missionaries (Acts 8:1,4).",
     [("Luke 11:49", "Because of this, God in his wisdom said, 'I will send them prophets and apostles, some of whom they will kill and others they will <em>persecute</em>.'"),
      ("1 Thessalonians 2:15", "Who killed the Lord Jesus and the prophets and also drove us out. They displease God and are hostile to everyone."),
      ("Matthew 5:10", "Blessed are those who are persecuted because of righteousness, for theirs is the kingdom of heaven."),
      ("Acts 8:1", "On that day a great persecution broke out against the church in Jerusalem, and all except the apostles were scattered throughout Judea and Samaria."),
      ("Romans 8:35", "Who shall separate us from the love of Christ? Shall trouble or hardship or persecution or famine or nakedness or danger or sword?")],
     [("G1377", "Diōkō (To Pursue/Persecute)"), ("G3144", "Martys (Witness/Martyr)"), ("G3804", "Pathēma (Suffering)")]),

    ("G1562", "ἐκδύω", "Ekduō", "Verb", "To Strip Off; To Undress; To Remove",
     "The Greek <em>ekduō</em> means to strip off clothing — to undress someone or remove what covers them. The word appears in the crucifixion accounts where soldiers strip Jesus of His garments before the crucifixion (Matthew 27:28, 31; Mark 15:20). Paul uses the concept in 2 Corinthians 5:4 — the believer does not want to be 'unclothed' (<em>ekdusasthai</em>) at death but to put on the resurrection body over the mortal.",
     "The stripping of Jesus' garments at Golgotha fulfills Psalm 22:18 ('They divide my clothes among them and cast lots for my garment'). The soldiers who stripped Him intended humiliation; God intended the fulfillment of prophecy. The body that was stripped and exposed in death would be clothed in resurrection glory. Paul's meditation on <em>ekduō</em> in 2 Corinthians 5 shows the believer's hope: not naked death but resurrection-clothed transformation — the mortal swallowed up by life.",
     [("Matthew 27:28", "They stripped him and put a scarlet robe on him."),
      ("Matthew 27:31", "After they had mocked him, they took off the robe and put his own clothes on him."),
      ("2 Corinthians 5:4", "For while we are in this tent, we groan and are burdened, because we do not wish to be unclothed but to be clothed instead with our heavenly dwelling."),
      ("Psalm 22:18", "They divide my clothes among them and cast lots for my garment."),
      ("Luke 10:30", "In reply Jesus said: 'A man was going down from Jerusalem to Jericho, when he was attacked by robbers. They stripped him of his clothes, beat him and went away, leaving him half dead.'")],
     [("G1746", "Enduō (To Put On/Clothe)"), ("G2440", "Himation (Garment/Robe)"), ("G386", "Anastasis (Resurrection)")]),

    ("G1567", "ἐκζητέω", "Ekzēteō", "Verb", "To Seek Out Diligently; To Search Earnestly",
     "The Greek <em>ekzēteō</em> is an intensified form of <em>zēteō</em> (to seek), meaning to seek out with diligence, to inquire carefully, to search earnestly. It is used of the prophets who 'searched intently' concerning the salvation to come (1 Peter 1:10), of Abel's blood that 'cries out' for justice (Luke 11:50-51), and of the impossibility of pleasing God without faith — since one must believe He rewards those who <em>ekzēteō</em> Him (Hebrews 11:6).",
     "Hebrews 11:6 establishes <em>ekzēteō</em> as the hallmark of faith: 'Without faith it is impossible to please God, because anyone who comes to him must believe that he exists and that he rewards those who earnestly seek him.' This is not casual interest but persistent, wholehearted pursuit — the kind of seeking Jesus described as 'seek first the kingdom' (Matthew 6:33). The prophets who <em>ekzēteō</em>-ed concerning salvation (1 Peter 1:10) modeled this diligent searching, and they found more than they knew — for they served not themselves but us.",
     [("Hebrews 11:6", "And without faith it is impossible to please God, because anyone who comes to him must believe that he exists and that he rewards those who <em>earnestly seek</em> him."),
      ("1 Peter 1:10", "Concerning this salvation, the prophets, who spoke of the grace that was to come to you, <em>searched intently</em> and with the greatest care."),
      ("Luke 11:50", "Therefore this generation will be held responsible for the blood of all the prophets that has been shed since the beginning of the world."),
      ("Acts 15:17", "That the rest of mankind may <em>seek</em> the Lord, even all the Gentiles who bear my name, says the Lord."),
      ("Matthew 6:33", "But seek first his kingdom and his righteousness, and all these things will be given to you as well.")],
     [("G2212", "Zēteō (To Seek)"), ("G4102", "Pistis (Faith)"), ("G4151", "Pneuma (Spirit)")]),

    ("G1569", "ἔκθαμβος", "Ekthambos", "Adjective", "Greatly Amazed; Utterly Astonished",
     "The Greek <em>ekthambos</em> means greatly amazed or utterly astonished — a state of overwhelming wonder produced by a miraculous or unexpected event. It appears only in Acts 3:11, describing the crowd's reaction as they ran to Solomon's Colonnade after Peter healed the lame man: 'they were filled with wonder and amazement.'",
     "The crowd's <em>ekthambos</em> at the healed lame man sets the stage for Peter's sermon (Acts 3:12-26). Peter immediately redirects their amazement away from himself and Barnabas — 'Why does this surprise you? Why do you stare at us as if by our own power or godliness we had made this man walk?' The miracle was real, the astonishment appropriate, but the glory belonged to 'the God of Abraham, Isaac and Jacob, the God of our fathers' who glorified His servant Jesus. <em>Ekthambos</em> is the proper response to divine power — as long as it leads to correct attribution.",
     [("Acts 3:11", "While the man held on to Peter and John, all the people were <em>astonished</em> and came running to them in the place called Solomon's Colonnade."),
      ("Mark 16:5", "As they entered the tomb, they saw a young man dressed in a white robe sitting on the right side, and they were <em>alarmed</em>."),
      ("Mark 9:15", "As soon as all the people saw Jesus, they were <em>overwhelmed with wonder</em> and ran to greet him."),
      ("Acts 3:12", "When Peter saw this, he said to them: 'Fellow Israelites, why does this surprise you? Why do you stare at us as if by our own power or godliness we had made this man walk?'"),
      ("Luke 4:36", "All the people were amazed and said to each other, 'What words these are! With authority and power he gives orders to impure spirits and they come out!'")],
     [("G1568", "Ekthambeo (To Amaze Greatly)"), ("G2285", "Thambos (Wonder/Amazement)"), ("G1411", "Dynamis (Power/Miracle)")]),

    ("G1571", "ἐκκαθαρίζω", "Ekkatharizō", "Verb", "To Cleanse Thoroughly; To Purge Completely",
     "The Greek <em>ekkatharizō</em> means to cleanse thoroughly or purge completely — the <em>ek</em> prefix intensifying the basic verb <em>katharizō</em> (to cleanse). Paul uses it in 1 Corinthians 5:7 regarding the removal of leaven from the household at Passover: 'Get rid of (<em>ekkatharizō</em>) the old yeast, so that you may be a new unleavened batch.' The command reflects both Passover ritual and spiritual renewal.",
     "Paul's use of <em>ekkatharizō</em> in 1 Corinthians 5 grounds the call for church discipline in the Passover typology. Just as every trace of leaven was removed from Jewish homes before Passover (Exodus 12:15), the church must remove the 'leaven' of flagrant sin — 'malice and wickedness' — to be a community of 'sincerity and truth' (1 Corinthians 5:8). The standard is total, not partial, cleansing. Christ our Passover Lamb has been sacrificed; therefore we must be what we are — unleavened, pure, renewed.",
     [("1 Corinthians 5:7", "<em>Get rid of</em> the old yeast, so that you may be a new unleavened batch — as you really are. For Christ, our Passover lamb, has been sacrificed."),
      ("2 Timothy 2:21", "Those who cleanse themselves from the latter will be instruments for special purposes, made holy, useful to the Master."),
      ("Ezekiel 43:22", "On the second day you are to offer a male goat without defect for a sin offering, and the altar is to be purified as it was purified with the bull."),
      ("Hebrews 9:22", "In fact, the law requires that nearly everything be cleansed with blood, and without the shedding of blood there is no forgiveness."),
      ("1 John 1:9", "If we confess our sins, he is faithful and just and will forgive us our sins and purify us from all unrighteousness.")],
     [("G2511", "Katharizō (To Cleanse/Purify)"), ("G2513", "Katharos (Clean/Pure)"), ("G106", "Azymos (Unleavened)")]),

    ("G1573", "ἐκκακέω", "Ekkakeō", "Verb", "To Lose Heart; To Grow Weary; To Give Up",
     "The Greek <em>ekkakeō</em> (also spelled <em>enkakeō</em>) means to lose heart, grow weary, or give up — specifically in the face of difficulty or discouragement. Paul uses it repeatedly in his letters as a warning against spiritual fatigue: 'do not lose heart' in prayer (Luke 18:1), in ministry (2 Corinthians 4:1, 16; 4:16), in doing good (Galatians 6:9; 2 Thessalonians 3:13), and in intercessory prayer for the Ephesians (Ephesians 3:13).",
     "<em>Ekkakeō</em> is the enemy of faithful endurance. Paul's most repeated pastoral command may be 'do not <em>ekkakeō</em>' — addressed to himself and to every church he led. The temptation to give up in ministry, prayer, and perseverance is real and perennial. But God's mercies sustain (2 Corinthians 4:1 — 'since through God's mercy we have this ministry, we do not lose heart'). Galatians 6:9 ties the promise directly to the warning: 'Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up.'",
     [("2 Corinthians 4:1", "Therefore, since through God's mercy we have this ministry, we do not <em>lose heart</em>."),
      ("2 Corinthians 4:16", "Therefore we do not <em>lose heart</em>. Though outwardly we are wasting away, yet inwardly we are being renewed day by day."),
      ("Galatians 6:9", "Let us not become <em>weary</em> in doing good, for at the proper time we will reap a harvest if we do not give up."),
      ("Ephesians 3:13", "I ask you, therefore, not to be discouraged because of my sufferings for you, which are your glory."),
      ("Luke 18:1", "Then Jesus told his disciples a parable to show them that they should always pray and not give up.")],
     [("G5278", "Hypomonē (Endurance/Perseverance)"), ("G2577", "Kamnō (To Grow Weary)"), ("G2479", "Ischus (Strength)")]),

    ("G1574", "ἐκκεντέω", "Ekkenteō", "Verb", "To Pierce Through; To Stab",
     "The Greek <em>ekkenteō</em> means to pierce through or stab — the <em>ek</em> prefix suggesting a penetrating thrust that goes through completely. The word appears in John 19:37 quoting Zechariah 12:10: 'They will look on the one they have <em>pierced</em>.' In Revelation 1:7, the same Zechariah quotation is applied eschatologically — every eye will see the returning Christ, including those who pierced Him.",
     "The fulfillment of <em>ekkenteō</em> in John 19:37 is one of the most precise fulfillments of Old Testament prophecy in the crucifixion narrative. Zechariah 12:10 predicted that Israel would 'look on me, the one they have pierced, and they will mourn for him.' The soldier's spear thrust into Jesus' side (John 19:34) fulfilled this prophecy to the letter. Revelation 1:7 extends this piercing to the Second Coming — the Christ who was pierced will be seen by all, and all who rejected Him will mourn. The wound that was meant as mockery becomes the sign of the King.",
     [("John 19:37", "And, as another scripture says, 'They will look on the one they have <em>pierced</em>.'"),
      ("Revelation 1:7", "Look, he is coming with the clouds, and every eye will see him, even those who <em>pierced</em> him; and all peoples on earth will mourn because of him."),
      ("Zechariah 12:10", "They will look on me, the one they have <em>pierced</em>, and they will mourn for him as one mourns for an only child."),
      ("John 19:34", "Instead, one of the soldiers pierced Jesus' side with a spear, bringing a sudden flow of blood and water."),
      ("Isaiah 53:5", "But he was pierced for our transgressions, he was crushed for our iniquities.")],
     [("H6482", "Petsa (Wound/Stripe)"), ("G2441", "Himatismos (Clothing)"), ("G3952", "Parousia (Coming/Presence)")]),

    ("G1575", "ἐκκλάω", "Ekkladō", "Verb", "To Break Off; To Snap Off",
     "The Greek <em>ekkladō</em> means to break off or snap off — specifically of branches broken from a tree. Paul uses this word exclusively in Romans 11:17-20, his extended metaphor of the olive tree. Some branches (unbelieving Israel) were 'broken off' (<em>ekkladō</em>) so that wild branches (Gentiles) could be grafted in. The same word appears three times in this passage.",
     "Romans 11's olive tree imagery is a foundational NT text on election, Gentile inclusion, and Jewish hope. The natural branches (<em>ekkladō</em>) were broken off because of unbelief — not permanently, for Paul insists 'if they do not persist in unbelief, they will be grafted in again, for God is able to graft them in again' (v.23). The Gentile who stands proudly should fear: 'Do not be arrogant, but tremble. For if God did not spare the natural branches, he will not spare you either.' The entire passage calls for humility, awe, and hope in God's sovereign mercy.",
     [("Romans 11:17", "If some of the branches have been <em>broken off</em>, and you, though a wild olive shoot, have been grafted in among the others."),
      ("Romans 11:19", "You will say then, 'Branches were <em>broken off</em> so that I could be grafted in.'"),
      ("Romans 11:20", "Granted. But they were <em>broken off</em> because of unbelief, and you stand by faith. Do not be arrogant, but tremble."),
      ("John 15:2", "He cuts off every branch in me that bears no fruit, while every branch that does bear fruit he prunes so that it will be even more fruitful."),
      ("Romans 11:23", "And if they do not persist in unbelief, they will be grafted in, for God is able to graft them in again.")],
     [("G1572", "Ekkaiō (To Inflame/Burn)"), ("G1461", "Enkentrizō (To Graft In)"), ("G570", "Apistia (Unbelief)")]),

    ("G1581", "ἐκκόπτω", "Ekkoptō", "Verb", "To Cut Down; To Cut Off; To Remove",
     "The Greek <em>ekkoptō</em> means to cut off or cut down — as an ax to a tree, or pruning shears to a branch. John the Baptist uses it in his most urgent warning: 'The ax is already at the root of the trees, and every tree that does not produce good fruit will be cut down (<em>ekkoptō</em>) and thrown into the fire' (Matthew 3:10; Luke 3:9). Jesus repeats the same warning in Matthew 7:19.",
     "The image of <em>ekkoptō</em> — the ax at the root — is one of the most urgent metaphors in the Gospels. John the Baptist's preaching confronted religious complacency: mere genealogical connection to Abraham was insufficient. The demand was fruit. The judgment was imminent. Paul uses similar language in Romans 11:22 (branches that are cut off) and 2 Corinthians 11:12 (cutting off occasion from his opponents). The consistent teaching: fruitlessness leads to removal. But the same power that can cut down can also graft in (Romans 11:23).",
     [("Matthew 3:10", "The ax is already at the root of the trees, and every tree that does not produce good fruit will be <em>cut down</em> and thrown into the fire."),
      ("Luke 3:9", "The ax is already at the root of the trees, and every tree that does not produce good fruit will be <em>cut down</em> and thrown into the fire."),
      ("Matthew 7:19", "Every tree that does not bear good fruit is <em>cut down</em> and thrown into the fire."),
      ("John 15:2", "He cuts off every branch in me that bears no fruit, while every branch that does bear fruit he prunes so that it will be even more fruitful."),
      ("Luke 13:7", "So he said to the man who took care of the vineyard, 'For three years now I've been coming to look for fruit on this fig tree and haven't found any. <em>Cut it down</em>!'")],
     [("G2590", "Karpos (Fruit)"), ("G4442", "Pyr (Fire)"), ("G1461", "Enkentrizō (To Graft In)")]),

    ("G1584", "ἐκλάμπω", "Eklampō", "Verb", "To Shine Forth; To Blaze Out",
     "The Greek <em>eklampō</em> means to shine forth brilliantly — to blaze out with radiant light. It appears only once in the New Testament: Matthew 13:43, the conclusion of the Parable of the Weeds — 'Then the righteous will shine like the sun (<em>eklampō</em>) in the kingdom of their Father.' The prefix <em>ek</em> intensifies the shining — a blazing forth from within, as the sun's full radiance.",
     "Matthew 13:43's promise of <em>eklampō</em> is the eschatological destiny of every believer: to shine like the sun in the Father's kingdom. This echoes Daniel 12:3 — 'Those who are wise will shine like the brightness of the heavens, and those who lead many to righteousness, like the stars for ever and ever.' The present hiddenness of the kingdom (mustard seed, leaven) gives way at the harvest to revealed glory. Every believer who now seems insignificant will <em>eklampō</em> in the fullness of Christ's transforming work.",
     [("Matthew 13:43", "Then the righteous will <em>shine like the sun</em> in the kingdom of their Father. Whoever has ears, let them hear."),
      ("Daniel 12:3", "Those who are wise will shine like the brightness of the heavens, and those who lead many to righteousness, like the stars for ever and ever."),
      ("Matthew 17:2", "There he was transfigured before them. His face shone like the sun, and his clothes became as white as the light."),
      ("Revelation 21:23", "The city does not need the sun or the moon to shine on it, for the glory of God gives it light, and the Lamb is its lamp."),
      ("2 Corinthians 4:6", "For God, who said, 'Let light shine out of darkness,' made his light shine in our hearts to give us the light of the knowledge of God's glory displayed in the face of Christ.")],
     [("G5457", "Phōs (Light)"), ("G1391", "Doxa (Glory)"), ("G3445", "Morphoō (To Form/Transform)")]),

    ("G1587", "ἐκλείπω", "Ekleipō", "Verb", "To Fail; To Cease; To Be Eclipsed",
     "The Greek <em>ekleipō</em> means to fail, give out, or cease — used of failing resources, fading light, and the end of life. Jesus uses it in Luke 22:32 praying that Peter's 'faith may not fail (<em>ekleipō</em>).' Luke 23:45 uses it of the sun's light during the crucifixion — 'the sun was eclipsed' (<em>ekleipō</em>). The astronomical term 'eclipse' comes directly from this Greek root.",
     "Two uses of <em>ekleipō</em> bracket the crucifixion in Luke's Gospel. Before: Jesus prays that Peter's faith will not <em>ekleipō</em> — fail utterly — under the coming trial. During: the sun itself <em>ekleipō</em>-s, as if creation mourns. The prayer and the sign interpret each other: just as the darkness was not permanent (resurrection came), so Peter's failure would not be final. The intercessory prayer of Christ sustains the faith of His people through their darkest hours. What <em>ekleipō</em>-s in human experience, Christ's prayer prevents from failing ultimately.",
     [("Luke 22:32", "But I have prayed for you, Simon, that your faith may not <em>fail</em>. And when you have turned back, strengthen your brothers."),
      ("Luke 23:45", "for the sun stopped shining (<em>ekleipō</em>). And the curtain of the temple was torn in two."),
      ("Luke 16:9", "I tell you, use worldly wealth to gain friends for yourselves, so that when it is gone (<em>ekleipō</em>), you will be welcomed into eternal dwellings."),
      ("Hebrews 1:12", "They will perish, but you remain; they will all wear out like a garment. You will roll them up like a robe; like a garment they will be changed."),
      ("James 1:11", "For the sun rises with scorching heat and withers the plant; its blossom falls and its beauty is destroyed. In the same way, the rich will fade away.")],
     [("G4102", "Pistis (Faith)"), ("G5457", "Phōs (Light)"), ("G386", "Anastasis (Resurrection)")]),

    ("G1589", "ἐκλογή", "Eklogē", "Noun, feminine", "Election; Selection; Divine Choosing",
     "The Greek <em>eklogē</em> refers to election or divine selection — God's sovereign act of choosing people for salvation and service. It appears in Romans 9:11 (Jacob was chosen before birth), 11:5 (a remnant chosen by grace), 11:7 (the elect obtained what Israel sought), 11:28 (the patriarchs' <em>eklogē</em> is irrevocable), 1 Thessalonians 1:4 (Paul's confidence in the Thessalonians' election), and 2 Peter 1:10 (make your calling and election sure).",
     "<em>Eklogē</em> is one of the most contested and most glorious doctrines in the NT. Paul's treatment in Romans 9-11 insists that election is: (1) by grace not works (9:11; 11:6), (2) in Christ (Ephesians 1:4), (3) for the purpose of holiness and witness (1 Peter 2:9), and (4) grounds for assurance rather than pride (Romans 8:33). The mystery of election is not an excuse for passivity but a foundation for confident mission — God has chosen; His purpose will not fail. 'Those he predestined, he also called; those he called, he also justified; those he justified, he also glorified' (Romans 8:30).",
     [("Romans 9:11", "Yet, before the twins were born or had done anything good or bad — in order that God's purpose in <em>election</em> might stand."),
      ("Romans 11:5", "So too, at the present time there is a remnant chosen by grace. And if by grace, then it cannot be based on works."),
      ("1 Thessalonians 1:4", "For we know, brothers and sisters loved by God, that he has chosen you."),
      ("2 Peter 1:10", "Therefore, my brothers and sisters, make every effort to confirm your calling and <em>election</em>."),
      ("Ephesians 1:4", "For he chose us in him before the creation of the world to be holy and blameless in his sight.")],
     [("G2821", "Klēsis (Calling)"), ("G4309", "Proorizō (To Predestine)"), ("G5485", "Charis (Grace)")]),

    ("G1590", "ἐκλύω", "Eklyō", "Verb", "To Faint; To Grow Weary; To Give Out",
     "The Greek <em>eklyō</em> means to loosen completely — hence to faint, grow weary, or give out from exhaustion. It appears in Hebrews 12:3 and 12:5, Galatians 6:9, and Matthew 15:32 / Mark 8:3 where Jesus expresses concern for the crowd who have been with Him three days and might 'collapse' on the way home if not fed. The word captures the physical experience of strength running out.",
     "Hebrews 12:3-5 pairs <em>eklyō</em> with the example of Jesus: 'Consider him who endured such opposition from sinners, so that you will not grow weary and lose heart (<em>eklyō</em>).' The antidote to spiritual fainting is fixing our eyes on Christ's endurance of the cross. Hebrews 12:5 then quotes Proverbs 3:11: 'do not make light of the Lord's discipline, and do not lose heart when he rebukes you.' Discipline is evidence of sonship, not rejection. Knowing this prevents the <em>eklyō</em> that comes from misreading suffering as abandonment.",
     [("Hebrews 12:3", "Consider him who endured such opposition from sinners, so that you will not grow weary (<em>eklyō</em>) and lose heart."),
      ("Hebrews 12:5", "And have you completely forgotten this word of encouragement that addresses you as a father addresses his son? It says: 'My son, do not make light of the Lord's discipline, and do not lose heart (<em>eklyō</em>) when he rebukes you.'"),
      ("Galatians 6:9", "Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up."),
      ("Matthew 15:32", "Jesus called his disciples to him and said, 'I have compassion for these people; they have already been with me three days and have nothing to eat. I do not want to send them away hungry, or they may <em>collapse</em> on the way.'"),
      ("Isaiah 40:31", "But those who hope in the LORD will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.")],
     [("G5278", "Hypomonē (Endurance)"), ("G3874", "Paraklēsis (Encouragement/Comfort)"), ("G4716", "Stauros (Cross)")]),

    ("G1592", "ἐκμυκτηρίζω", "Ekmuktērizō", "Verb", "To Sneer At; To Mock Contemptuously",
     "The Greek <em>ekmuktērizō</em> means to sneer contemptuously — literally 'to turn up the nose at' someone. The verb comes from <em>muktēr</em> (nose) and <em>ek</em> (out/fully), painting a picture of visible, physical mockery. It is used twice in Luke: of the Pharisees who 'sneered at' Jesus after His teaching on money and God (Luke 16:14), and of the rulers who 'sneered at' Him during the crucifixion (Luke 23:35).",
     "The <em>ekmuktērizō</em> of the Pharisees in Luke 16:14 is one of the clearest biblical pictures of hardened religious pride. They 'loved money' (v.14) and responded to Jesus' teaching about the impossibility of serving both God and money with contemptuous mockery rather than repentance. The same contemptuous sneering appears at the cross (Luke 23:35) — the religious leaders mocking the one they had crucified. Both moments are moments of revelation: those who sneer at Christ reveal the true state of their hearts. The one they mock is the judge before whom they will stand.",
     [("Luke 16:14", "The Pharisees, who loved money, heard all this and were <em>sneering</em> at Jesus."),
      ("Luke 23:35", "The people stood watching, and the rulers even <em>sneered</em> at him. They said, 'He saved others; let him save himself if he is God's Messiah, the Chosen One.'"),
      ("Psalm 22:7", "All who see me mock me; they hurl insults, shaking their heads."),
      ("Psalm 2:4", "The One enthroned in heaven laughs; the Lord scoffs at them."),
      ("Matthew 27:41", "In the same way the chief priests, the teachers of the law and the elders mocked him.")],
     [("G1701", "Empaigmos (Mockery/Ridicule)"), ("G3679", "Oneidizō (To Reproach/Insult)"), ("G2917", "Krima (Judgment)")]),

    ("G1595", "ἑκούσιος", "Hekousios", "Adjective", "Voluntary; Willing; Free",
     "The Greek <em>hekousios</em> means voluntary, willing, or free — done of one's own accord rather than under compulsion. In Philemon 14, Paul uses it to emphasize that he wants Onesimus to help voluntarily, not under compulsion: 'so that any favor you do would not seem forced but would be voluntary (<em>hekousios</em>).' In 1 Peter 5:2, elders are to shepherd 'not because you must, but because you are willing (<em>hekousios</em>).'",
     "The theology of <em>hekousios</em> service and sacrifice stands at the heart of NT ethics. Hebrews 10:26 uses the adverb form for a chilling warning: 'If we deliberately (<em>hekousios</em>) keep on sinning after we have received the knowledge of the truth, no sacrifice for sins is left.' This is the flip side: what makes voluntary sin so serious is that it mirrors the voluntary sacrifice of Christ — but in the opposite direction. Christ voluntarily gave Himself; deliberate post-conversion sin voluntarily tramples that sacrifice. The power of <em>hekousios</em> cuts both ways: toward redemption and toward rebellion.",
     [("Philemon 14", "But I did not want to do anything without your consent, so that any favor you do would not seem forced but would be <em>voluntary</em>."),
      ("1 Peter 5:2", "Be shepherds of God's flock that is under your care, watching over them — not because you must, but because you are <em>willing</em>."),
      ("Hebrews 10:26", "If we deliberately (<em>hekousios</em>) keep on sinning after we have received the knowledge of the truth, no sacrifice for sins is left."),
      ("Psalm 54:6", "I will <em>sacrifice a freewill offering</em> to you; I will praise your name, LORD, for it is good."),
      ("2 Corinthians 9:7", "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver.")],
     [("G1635", "Hekōn (Willingly)"), ("G1342", "Dikaios (Just/Righteous)"), ("G26", "Agapē (Love)")]),

    ("G1598", "ἐκπειράζω", "Ekpeirazō", "Verb", "To Test; To Put to the Test; To Tempt God",
     "The Greek <em>ekpeirazō</em> is an intensified form of <em>peirazō</em> (to test/tempt), meaning to put severely to the test — particularly the act of testing or tempting God. Satan quotes Psalm 91 to Jesus and says 'throw yourself down, for the angels will catch you' — Jesus responds 'Do not put the Lord your God to the test (<em>ekpeirazō</em>)' (Matthew 4:7; Luke 4:12), quoting Deuteronomy 6:16. Paul uses it in 1 Corinthians 10:9 as a warning from Israel's wilderness failure.",
     "The specific sin of <em>ekpeirazō</em> — testing God — is the demand that God prove Himself by performing on command. Israel's wilderness complaint 'Is the LORD among us or not?' (Exodus 17:7) was the original context of the Deuteronomy 6:16 prohibition. Jesus refuses to test the Father by forcing a spectacular rescue. The cross was not a display-of-power moment but a moment of hiddenness — and the resurrection vindicated the One who trusted rather than tested. Paul's warning to Corinth: 'Do not test Christ as some of them did — and were killed by snakes' (1 Corinthians 10:9).",
     [("Matthew 4:7", "Jesus answered him, 'It is also written: Do not put the Lord your God to the test (<em>ekpeirazō</em>).'"),
      ("Luke 4:12", "Jesus answered, 'It is said: Do not put the Lord your God to the test (<em>ekpeirazō</em>).'"),
      ("1 Corinthians 10:9", "We should not test Christ, as some of them did — and were killed by snakes."),
      ("Exodus 17:7", "And he called the place Massah and Meribah because the Israelites quarreled and because they tested the LORD saying, 'Is the LORD among us or not?'"),
      ("Deuteronomy 6:16", "Do not put the LORD your God to the test as you did at Massah.")],
     [("G3985", "Peirazō (To Test/Tempt)"), ("G4102", "Pistis (Faith)"), ("G3985", "Peirasmos (Trial/Temptation)")]),

    ("G1601", "ἐκπίπτω", "Ekpiptō", "Verb", "To Fall From; To Fall Away; To Be Cast Off",
     "The Greek <em>ekpiptō</em> means to fall out of or fall away from — to be dislodged from one's position. It is used of stars falling from heaven (Mark 13:25; Revelation 6:13), of the angel Gabriel's visit when Zechariah's fear 'fell upon' him (Luke 1:12), and most significantly in Galatians 5:4 — 'You who are trying to be justified by the law have been alienated from Christ; you have <em>fallen away</em> from grace.' Also Acts 27:17, 26, 29 of ships running aground.",
     "Galatians 5:4's use of <em>ekpiptō</em> from grace is one of Paul's sharpest warnings. To seek justification by law-keeping is not merely inadequate — it is to fall out of the entire sphere of grace. Grace and self-justification cannot coexist. Paul's point is not that believers can lose their salvation through sin, but that the very orientation toward law-righteousness places one outside the domain of grace. 2 Peter 3:17 uses <em>ekpiptō</em> similarly — beware lest you 'fall from your secure position' by being carried away with error. Stability in grace requires active attentiveness.",
     [("Galatians 5:4", "You who are trying to be justified by the law have been alienated from Christ; you have <em>fallen away</em> from grace."),
      ("2 Peter 3:17", "Therefore, dear friends, since you have been forewarned, be on your guard so that you may not be carried away by the error of the lawless and <em>fall</em> from your secure position."),
      ("Romans 9:6", "It is not as though God's word had failed (<em>ekpiptō</em>). For not all who are descended from Israel are Israel."),
      ("Mark 13:25", "The stars will <em>fall</em> from the sky, and the heavenly bodies will be shaken."),
      ("1 Corinthians 13:8", "Love never fails (<em>ekpiptō</em>). But where there are prophecies, they will cease; where there are tongues, they will be stilled.")],
     [("G5485", "Charis (Grace)"), ("G4102", "Pistis (Faith)"), ("G5278", "Hypomonē (Endurance)")]),

    ("G1606", "ἐκπνέω", "Ekpneō", "Verb", "To Breathe Out; To Expire; To Die",
     "The Greek <em>ekpneō</em> means to breathe out completely — to expire. In the New Testament it is used exclusively and specifically of Jesus' death on the cross. Mark 15:37 and 15:39 and Luke 23:46 all use <em>ekpneō</em> to describe the moment of Jesus' death. The word is a medical-literary term for the final exhalation — the breath going out without return.",
     "The precision of <em>ekpneō</em> for Christ's death is significant. He did not simply lose consciousness or collapse — He 'breathed out' life itself. Luke 23:46 is the most moving context: 'Jesus called out with a loud voice, Father, into your hands I commit my spirit. When he had said this, he breathed his last (<em>ekpneō</em>).' The loud voice before death underscores the voluntary nature of the sacrifice — He laid down His life; it was not taken from Him (John 10:18). The breath that came out in creation (Genesis 2:7) returned through the One whose <em>ekpneō</em> purchased our life.",
     [("Mark 15:37", "With a loud cry, Jesus breathed his last (<em>ekpneō</em>)."),
      ("Mark 15:39", "And when the centurion, who stood there in front of Jesus, saw how he died (<em>ekpneō</em>), he said, 'Surely this man was the Son of God!'"),
      ("Luke 23:46", "Jesus called out with a loud voice, 'Father, into your hands I commit my spirit.' When he had said this, he breathed his last (<em>ekpneō</em>)."),
      ("John 10:18", "No one takes it from me, but I lay it down of my own accord. I have authority to lay it down and authority to take it up again."),
      ("Genesis 2:7", "Then the LORD God formed a man from the dust of the ground and breathed into his nostrils the breath of life, and the man became a living being.")],
     [("G4151", "Pneuma (Spirit/Breath)"), ("G2288", "Thanatos (Death)"), ("G386", "Anastasis (Resurrection)")]),

    ("G1607", "ἐκπορεύομαι", "Ekporeuomai", "Verb", "To Go Out; To Proceed; To Come From",
     "The Greek <em>ekporeuomai</em> means to go out, proceed, or come forth from a source. It is used of rivers flowing out (Revelation 22:1), the words proceeding from God's mouth (Matthew 4:4 quoting Deuteronomy 8:3), the Spirit who 'proceeds from the Father' (John 15:26 — one of the most theologically significant uses in church history), and of multitudes coming out to be baptized by John (Matthew 3:5).",
     "John 15:26 — 'the Spirit of truth who goes out (<em>ekporeuomai</em>) from the Father' — became the central term in the Filioque controversy between Eastern and Western Christianity (does the Spirit proceed from the Father alone, or from the Father 'and the Son'?). Regardless of that later debate, the verse establishes the Spirit's divine origin and mission: He comes from the Father and is sent by Jesus. <em>Ekporeuomai</em> in Revelation 22:1 — the river of the water of life proceeding from the throne of God and of the Lamb — shows the Spirit's life-giving work flowing through all of new creation.",
     [("John 15:26", "When the Advocate comes, whom I will send to you from the Father — the Spirit of truth who goes out (<em>ekporeuomai</em>) from the Father — he will testify about me."),
      ("Matthew 4:4", "Jesus answered, 'It is written: Man shall not live on bread alone, but on every word that <em>comes</em> from the mouth of God.'"),
      ("Revelation 22:1", "Then the angel showed me the river of the water of life, as clear as crystal, flowing from the throne of God and of the Lamb."),
      ("Matthew 3:5", "People went out (<em>ekporeuomai</em>) to him from Jerusalem and all Judea and the whole region of the Jordan."),
      ("Mark 7:15", "Nothing outside a person can defile them by going into them. Rather, it is what comes out of a person that defiles them.")],
     [("G4151", "Pneuma (Spirit)"), ("G3962", "Patēr (Father)"), ("G2222", "Zōē (Life)")]),

    ("G1608", "ἐκπορνεύω", "Ekporneuo", "Verb", "To Indulge in Sexual Immorality; To Practice Prostitution",
     "The Greek <em>ekporneuo</em> means to indulge in sexual immorality intensely or thoroughly — the <em>ek</em> prefix suggesting excess and completion. It appears only once in the NT, in Jude 7, describing Sodom and Gomorrah's sin: 'They gave themselves up to sexual immorality and pursued unnatural desire.' The word captures not just the act but the total surrender to sexual sin.",
     "Jude's use of <em>ekporneuo</em> for Sodom's sin specifies the nature of the judgment: they pursued sexual immorality to the extreme, surrendering themselves completely. The result was that they 'serve as an example of those who suffer the punishment of eternal fire' (Jude 7). Jude is warning the church against those who 'pervert the grace of God into a license for immorality' (v.4). Sexual sin is never a private matter in Scripture — it is covenant-breaking, dishonoring the image of God, and has eternal consequences. The <em>ekporneuo</em> of Sodom is a perpetual warning.",
     [("Jude 7", "In a similar way, Sodom and Gomorrah and the surrounding towns gave themselves up to sexual immorality (<em>ekporneuo</em>) and perversion. They serve as an example of those who suffer the punishment of eternal fire."),
      ("Genesis 19:5", "They called to Lot, 'Where are the men who came to you tonight? Bring them out to us so that we can have sex with them.'"),
      ("1 Corinthians 6:18", "Flee from sexual immorality. All other sins a person commits are outside the body, but whoever sins sexually, sins against their own body."),
      ("Revelation 17:2", "With her the kings of the earth committed adultery, and the inhabitants of the earth were intoxicated with the wine of her adulteries."),
      ("1 Thessalonians 4:3", "It is God's will that you should be sanctified: that you should avoid sexual immorality.")],
     [("G4202", "Porneia (Sexual Immorality)"), ("G2920", "Krisis (Judgment)"), ("H2764", "Cherem (Devoted to Destruction)")]),

    ("G1610", "ἐκριζόω", "Ekrizoo", "Verb", "To Uproot; To Root Out; To Pull Up by the Roots",
     "The Greek <em>ekrizoo</em> means to uproot — to pull something up by its roots completely, leaving no remnant. Jesus uses it in Matthew 13:29 (the servants must not uproot the wheat along with the weeds at harvest) and 15:13 ('Every plant that my heavenly Father has not planted will be pulled up (<em>ekrizoo</em>) by the roots'). Luke 17:6 uses it of a mulberry tree being uprooted and planted in the sea by faith.",
     "The <em>ekrizoo</em> imagery in Matthew 15:13 is one of Jesus' most penetrating critiques of human religious traditions. The Pharisees were offended by His teaching; Jesus responded that every plant not planted by the Father would be uprooted. Human-constructed religion — however impressive its tradition — has no root in God and will be pulled up. In contrast, the word of God is seed planted by God Himself (Matthew 13:3-8) — it has roots that endure. Luke 17:6's faith that can <em>ekrizoo</em> trees shows the power available to even mustard-seed faith directed toward God's purposes.",
     [("Matthew 13:29", "He said, 'No,' he answered, 'because while you are pulling the weeds, you may uproot (<em>ekrizoo</em>) the wheat with them.'"),
      ("Matthew 15:13", "He replied, 'Every plant that my heavenly Father has not planted will be pulled up (<em>ekrizoo</em>) by the roots.'"),
      ("Luke 17:6", "He replied, 'If you have faith as small as a mustard seed, you can say to this mulberry tree, Be uprooted (<em>ekrizoo</em>) and planted in the sea, and it will obey you.'"),
      ("Jude 12", "They are autumn trees, without fruit and uprooted (<em>ekrizoo</em>) — twice dead."),
      ("Colossians 2:7", "Rooted and built up in him, strengthened in the faith as you were taught, and overflowing with thankfulness.")],
     [("G4491", "Rhiza (Root)"), ("G2590", "Karpos (Fruit)"), ("G4687", "Speirō (To Sow/Scatter Seed)")]),
]

def write_page(strongs_id, script, translit, pos, gloss, definition, theology, verses, related):
    lang = strongs_id[0]
    html = make_page(strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related)
    path = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Created: {strongs_id}.html")

count = 0
print("=== Hebrew Words (24) ===")
for entry in hebrew_words:
    strongs_id = entry[0]
    write_page(*entry)
    count += 1

print(f"\n=== Greek Words (23) ===")
for entry in greek_words:
    strongs_id = entry[0]
    write_page(*entry)
    count += 1

print(f"\nTotal pages created: {count}")
