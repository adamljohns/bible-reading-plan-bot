#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Mar 26 cron batch"""
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

    blb_lang = "g" if lang == "G" else "h"

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

# ─── WORD DATA ──────────────────────────────────────────────────────────────
WORDS = [

# ══════════════════════════════
#  HEBREW (24 words)
# ══════════════════════════════

("H747", "H", "אַרְנֶבֶת", "arnebeth", "Noun, feminine", "Hare / Rabbit",
 "The Hebrew word <em>arnebeth</em> refers to the hare or rabbit, a creature mentioned in the Mosaic dietary law. It appears in Leviticus and Deuteronomy as one of the animals declared unclean for Israel's consumption, identified as one that chews the cud but does not have a split hoof.",
 "Though a minor zoological term, <em>arnebeth</em> carries theological significance within Israel's purity laws. The dietary restrictions in the Torah served as boundary markers between Israel and the nations, reinforcing the call to holiness. The distinction between clean and unclean creatures taught Israel to discern and choose what is set apart for God. The New Testament fulfillment of these laws (Acts 10; Mark 7) reveals that the deeper principle was always spiritual purity of heart.",
 [("Leviticus 11:6", "The <em>hare</em>, because it chews its cud but does not have divided hooves — it is unclean for you."),
  ("Deuteronomy 14:7", "Of those that chew the cud or have divided hooves, you may not eat the camel, the rabbit, or the <em>hare</em>."),
  ("Leviticus 11:4", "There are some that only chew the cud or only have divided hooves, and you must not eat them."),
  ("Acts 10:15", "Do not call anything impure that God has made clean."),
  ("Mark 7:19", "In saying this, Jesus declared all foods clean.")],
 [("H2889", "Tahor — Clean"), ("H2931", "Tame — Unclean"), ("H6942", "Qadash — Be Holy")]),

("H749", "H", "אֲרַק", "araq", "Verb (Aramaic)", "Suitable / Be fitting",
 "An Aramaic verb meaning to be suitable, fitting, or appropriate. It appears in the Aramaic sections of the Old Testament (Daniel and Ezra) and conveys the idea of something being proper, right, or apposite for a given situation or purpose.",
 "Though rare, <em>araq</em> touches on a key biblical theme: divine ordering and fitness. In the context of Daniel, the term relates to the appropriateness of communication before kings — echoing wisdom literature's emphasis that the right word at the right time is a gift of God (Proverbs 15:23). God Himself acts with perfect fitness, and His servants are called to speak and act with wisdom and discernment.",
 [("Daniel 3:19", "Then Nebuchadnezzar was furious and his attitude toward Shadrach, Meshach, and Abednego changed — he ordered the furnace heated seven times hotter than usual."),
  ("Ezra 5:5", "But the eye of their God was watching over the elders of the Jews."),
  ("Proverbs 15:23", "A person finds joy in giving an apt reply — and how good is a timely word!"),
  ("Colossians 4:6", "Let your conversation be always full of grace, seasoned with salt, so that you may know how to answer everyone."),
  ("Proverbs 25:11", "Like apples of gold in settings of silver is a ruling rightly given.")],
 [("H3559", "Kun — Establish/Be Firm"), ("H8505", "Takan — Measure/Order"), ("H1697", "Dabar — Word/Matter")]),

("H763", "H", "אֲרַם נַהֲרַיִם", "Aram Naharaim", "Proper noun — Place", "Mesopotamia / Aram of the Two Rivers",
 "<em>Aram Naharaim</em> means 'Aram of the Two Rivers' — the ancient region between the Tigris and Euphrates, corresponding to upper Mesopotamia (modern northern Syria/Turkey). It is the homeland of the patriarchs and the source of Rebekah, Rachel, and Leah.",
 "This geographic term is laden with redemptive history. It marks the origin of God's covenant family — Abraham left Aram Naharaim at God's call (Acts 7:2–3). The region represents the world the patriarchs were called <em>out of</em>, yet God sent servants back into it to find covenant brides for the line of promise. Theologically, it pictures how God works through human geography and relationships to accomplish eternal purposes.",
 [("Genesis 24:10", "Then the servant left, taking with him ten of his master's camels loaded with all kinds of good things from his master. He set out for <em>Aram Naharaim</em> and made his way to the town of Nahor."),
  ("Deuteronomy 23:4", "They hired Balaam son of Beor from Pethor in <em>Aram Naharaim</em> to pronounce a curse on you."),
  ("Judges 3:8", "The anger of the Lord burned against Israel so that he sold them into the hands of Cushan-Rishathaim king of <em>Aram Naharaim</em>."),
  ("Acts 7:2", "The God of glory appeared to our father Abraham while he was still in Mesopotamia, before he lived in Harran."),
  ("Genesis 25:20", "Isaac was forty years old when he married Rebekah daughter of Bethuel the Aramean from Paddan Aram.")],
 [("H758", "Aram — Syria/Aram"), ("H5104", "Nahar — River"), ("H85", "Abraham — Father of a Multitude")]),

("H786", "H", "אִישׁ", "iysh (variant)", "Particle / Existential marker", "There is / It exists",
 "A poetic or archaic form related to the existential particle, used in contexts emphasizing the presence or existence of something. In several passages it functions to affirm that something truly exists or 'is there,' contrasting with its negative counterpart <em>ayin</em> (there is not).",
 "Existence and presence are deeply theological realities in Scripture. The affirmation that God <em>is</em> — present, real, and acting — underlies all biblical faith. When biblical poetry uses existential language, it often grounds human confidence in divine presence (Psalm 46; Isaiah 43). The contrast between <em>yesh</em> (there is) and <em>ayin</em> (there is not) frames some of Scripture's most profound meditations on divine sovereignty versus human futility.",
 [("Proverbs 13:7", "One person pretends to be rich, yet has nothing; another pretends to be poor, yet has great wealth."),
  ("Isaiah 43:10", "Before me no god was formed, nor will there be one after me."),
  ("Genesis 28:16", "Surely the Lord is in this place, and I was not aware of it."),
  ("Psalm 14:2", "The Lord looks down from heaven on all mankind to see if there are any who understand, any who seek God."),
  ("Proverbs 14:12", "There is a way that appears to be right, but in the end it leads to death.")],
 [("H369", "Ayin — There Is Not"), ("H3426", "Yesh — There Is"), ("H430", "Elohim — God")]),

("H794", "H", "אֲשֵׁדָה", "ashedah", "Noun, feminine", "Ravine / Slope / Watercourse",
 "The Hebrew word <em>ashedah</em> refers to mountain slopes, ravines, or the descending sides of a hill — the terrain that falls away from high ground. It describes the physical geography of the Promised Land, particularly the descent from the highlands of Canaan toward lower valleys.",
 "The topography of Canaan is not incidental in Scripture — it is theological landscape. God gave Israel a land of mountains and valleys that depend on rain from heaven (Deuteronomy 11:11), unlike Egypt's irrigation from the Nile. The slopes and ravines of the land picture both danger and provision. Jesus used similar imagery in describing the sheep that strays and must be sought, the narrow path descending into the valley of decision. The <em>ashedah</em> reminds believers that terrain itself is a gift from God to be stewarded.",
 [("Joshua 10:40", "So Joshua subdued the whole region, including the hill country, the Negev, the western foothills and the mountain <em>slopes</em>."),
  ("Joshua 12:8", "The hill country, the western foothills, the Arabah, the mountain <em>slopes</em>, the wilderness and the Negev."),
  ("Deuteronomy 11:11", "But the land you are crossing the Jordan to take possession of is a land of mountains and valleys that drinks rain from heaven."),
  ("Psalm 65:12", "The grasslands of the wilderness overflow; the hills are clothed with gladness."),
  ("Isaiah 54:10", "Though the mountains be shaken and the hills be removed, yet my unfailing love for you will not be shaken.")],
 [("H2022", "Har — Mountain"), ("H1516", "Gay — Valley"), ("H776", "Erets — Land/Earth")]),

("H804", "H", "אַשּׁוּר", "Ashshur", "Proper noun — People/Land", "Assyria / Asshur",
 "<em>Ashshur</em> is the name of both a son of Shem (Genesis 10:22) and the great empire of Assyria that dominated the ancient Near East. The Assyrian Empire became God's instrument of judgment against the northern kingdom of Israel (722 BC) and threatened Judah under Hezekiah.",
 "Assyria occupies a major place in biblical prophecy and history. It was the instrument God used to judge Israel's idolatry, yet God also judged Assyria itself for its pride and cruelty (Isaiah 10:5–19). The famous oracle 'Woe to Assyria, the rod of my anger!' demonstrates that God uses even wicked nations as tools of discipline while holding them accountable. Assyria's fall was prophesied and fulfilled, teaching that no earthly empire stands apart from God's sovereign governance.",
 [("Isaiah 10:5", "Woe to <em>Assyria</em>, the rod of my anger, in whose hand is the club of my wrath!"),
  ("2 Kings 17:6", "In the ninth year of Hoshea, the king of <em>Assyria</em> captured Samaria and deported the Israelites to Assyria."),
  ("Isaiah 37:36", "Then the angel of the Lord went out and put to death a hundred and eighty-five thousand in the <em>Assyrian</em> camp."),
  ("Nahum 3:1", "Woe to the city of blood, full of lies, full of plunder, never without victims!"),
  ("Micah 5:6", "They will rule the land of <em>Assyria</em> with the sword.")],
 [("H894", "Babel — Babylon"), ("H4714", "Mitsraim — Egypt"), ("H3478", "Yisrael — Israel")]),

("H822", "H", "אֶשְׁנָב", "eshnab", "Noun, masculine", "Lattice / Window-frame",
 "The Hebrew word <em>eshnab</em> refers to a latticed window or window-frame — a structure of interwoven bars through which one could see while being partially concealed. It appears in the account of Sisera's mother anxiously watching through a lattice for her son's return from battle.",
 "Windows and lattices in Scripture often frame moments of watching, waiting, and longing. Sisera's mother watches through the <em>eshnab</em> for a victory that will never come — a poignant picture of hope placed in human military strength. Solomon's beloved speaks of a beloved who looks through the lattice (Song 2:9), suggesting intimacy and desire. Theologically, the image of watching and being watched speaks to God's own gaze — He sees through every barrier, His eyes 'running to and fro throughout the earth' (2 Chronicles 16:9).",
 [("Judges 5:28", "Through the <em>window</em> peered Sisera's mother; behind the lattice she cried out."),
  ("Song of Songs 2:9", "My beloved is like a gazelle or a young stag. Look! There he stands behind our wall, gazing through the windows, peering through the <em>lattice</em>."),
  ("Proverbs 7:6", "At the window of my house I looked down through the <em>lattice</em>."),
  ("2 Chronicles 16:9", "For the eyes of the Lord range throughout the earth to strengthen those whose hearts are fully committed to him."),
  ("Psalm 139:3", "You discern my going out and my lying down; you are familiar with all my ways.")],
 [("H2474", "Challon — Window"), ("H1817", "Deleth — Door"), ("H5869", "Ayin — Eye")]),

("H827", "H", "אַשְׁפָּה", "ashpah", "Noun, feminine", "Quiver (for arrows)",
 "The Hebrew word <em>ashpah</em> denotes a quiver — the container used to carry arrows, typically worn on the back or shoulder of a warrior or archer. It appears in both literal military contexts and extended metaphorical uses.",
 "In the Psalms, the quiver becomes a powerful metaphor for family and heritage. Psalm 127:3–5 declares children to be like arrows in the hand of a warrior, and the man with many children has his quiver full — a vivid image of providential blessing and strength. Isaiah uses the quiver to describe Israel as a hidden instrument in God's hand (Isaiah 49:2). The theological depth of <em>ashpah</em> spans from the battlefield to the household, showing God as both military protector and covenant father who equips His people.",
 [("Psalm 127:5", "Blessed is the man whose <em>quiver</em> is full of them. They will not be put to shame when they contend with their opponents in court."),
  ("Isaiah 49:2", "He made me into a polished arrow and concealed me in his <em>quiver</em>."),
  ("Job 39:23", "The <em>quiver</em> rattles against its side, along with the flashing spear and lance."),
  ("Psalm 127:3", "Children are a heritage from the Lord, offspring a reward from him."),
  ("Lamentations 3:13", "He pierced my heart with arrows from his <em>quiver</em>.")],
 [("H2671", "Chets — Arrow"), ("H7198", "Qesheth — Bow"), ("H1121", "Ben — Son")]),

("H839", "H", "אָשֶׁל", "ashel", "Noun, masculine", "Tamarisk tree",
 "The Hebrew word <em>ashel</em> refers to the tamarisk tree — a hardy, salt-tolerant tree that thrives in arid and semi-arid environments. The tamarisk grows in the Negev and Sinai regions and was associated with the patriarchs, particularly Abraham.",
 "Abraham planted a tamarisk tree at Beersheba and called on the name of the Lord there (Genesis 21:33). The tamarisk's remarkable ability to survive in harsh, dry conditions makes it a fitting symbol of enduring faith. Planting a tree was an act of long-term hope — one does not plant for shade today but for generations to come. The tamarisk site at Beersheba became a place of covenant and worship, reminding Israel that their father Abraham worshiped the Eternal God (<em>El Olam</em>) even in desert places.",
 [("Genesis 21:33", "Abraham planted a <em>tamarisk</em> tree in Beersheba, and there he called on the name of the Lord, the Eternal God."),
  ("1 Samuel 22:6", "Now Saul heard that David and his men had been discovered. And Saul was seated, spear in hand, under the <em>tamarisk</em> tree on the hill at Gibeah."),
  ("1 Samuel 31:13", "Then they took their bones and buried them under a <em>tamarisk</em> tree at Jabesh."),
  ("Isaiah 41:19", "I will put in the desert the cedar and the acacia, the myrtle and the olive."),
  ("Psalm 84:6", "As they pass through the Valley of Baka, they make it a place of springs.")],
 [("H410", "El Olam — Eternal God"), ("H875", "Beer — Well"), ("H1285", "Berit — Covenant")]),

("H843", "H", "אָשֵׁר", "Asher", "Proper noun — Person/Tribe", "Happy / Blessed",
 "<em>Asher</em> means 'happy' or 'blessed' and was the eighth son of Jacob, born to Leah's maidservant Zilpah (Genesis 30:13). The tribe of Asher was allotted territory in the fertile coastal plain of northern Canaan, known for its abundance of oil.",
 "The name <em>Asher</em> derives from the root <em>ashar</em> (H833), meaning to go straight, advance, be happy. Jacob's blessing over Asher declares 'his food shall be rich, and he shall yield royal delicacies' (Genesis 49:20). Moses' blessing adds: 'Most blessed of sons is Asher; let him be favored by his brothers' (Deuteronomy 33:24). The prophetess Anna was from the tribe of Asher (Luke 2:36), one of the few New Testament references to the northern tribes. Theologically, <em>Asher</em> represents the blessedness that flows from covenant relationship — abundance that is to be shared.",
 [("Genesis 30:13", "Then Leah said, 'How happy I am! The women will call me happy.' So she named him <em>Asher</em>."),
  ("Genesis 49:20", "<em>Asher's</em> food will be rich; he will provide delicacies fit for a king."),
  ("Deuteronomy 33:24", "Most blessed of sons is <em>Asher</em>; let him be favored by his brothers and let him bathe his feet in oil."),
  ("Luke 2:36", "There was also a prophet, Anna, the daughter of Penuel, of the tribe of <em>Asher</em>."),
  ("Psalm 1:1", "Blessed is the one who does not walk in step with the wicked.")],
 [("H833", "Ashar — Be Happy/Blessed"), ("H1293", "Berakah — Blessing"), ("H8057", "Simchah — Joy")]),

("H855", "H", "אֵת", "et", "Noun, masculine", "Plowshare / Mattock",
 "The Hebrew word <em>et</em> (distinct from the common direct-object marker) refers to a plowing tool — a plowshare, mattock, or similar iron implement used in agriculture. It appears in a famous passage in 1 Samuel describing Philistine domination of Israel's metal-working.",
 "The absence of plowshares in 1 Samuel 13 represents Philistine oppression — Israel was disarmed, forbidden from sharpening their own agricultural tools, let alone weapons. The same imagery is reversed in the great eschatological vision of Isaiah and Micah, where nations 'beat their swords into plowshares' (<em>ittim</em>). The plowshare thus symbolizes both the weight of oppression and the promise of peace. In the kingdom of God, instruments of war become instruments of cultivation — creation restored, violence ended, productivity flourishing.",
 [("1 Samuel 13:20", "So all Israel went down to the Philistines to have their <em>plowshares</em>, mattocks, axes, and sickles sharpened."),
  ("Isaiah 2:4", "They will beat their swords into <em>plowshares</em> and their spears into pruning hooks."),
  ("Micah 4:3", "They will beat their swords into <em>plowshares</em> and their spears into pruning hooks."),
  ("Joel 3:10", "Beat your <em>plowshares</em> into swords and your pruning hooks into spears."),
  ("1 Samuel 13:22", "So on the day of the battle not a soldier with Saul and Jonathan had a sword or spear in his hand.")],
 [("H2719", "Chereb — Sword"), ("H2595", "Chanith — Spear"), ("H7965", "Shalom — Peace")]),

("H861", "H", "אַתּוּן", "attun", "Noun, feminine (Aramaic)", "Furnace / Fiery furnace",
 "An Aramaic word for a large furnace or kiln — appearing most notably in Daniel 3, where King Nebuchadnezzar commands the 'fiery furnace' (<em>attun nura</em>) to be used to execute those who refuse to worship his golden image.",
 "The furnace in Daniel 3 is one of Scripture's most powerful images of divine protection in the midst of persecution. Shadrach, Meshach, and Abednego enter the furnace at the cost of their lives rather than bow to an idol, and emerge untouched — with a mysterious fourth figure walking among them. The <em>attun</em> becomes a symbol of God's presence in the fire of trial (Isaiah 43:2). Early Christians saw this as a type of Christ's presence with His people in suffering, and the furnace story has provided courage to believers facing martyrdom across two millennia.",
 [("Daniel 3:6", "Whoever does not fall down and worship will immediately be thrown into a blazing <em>furnace</em>."),
  ("Daniel 3:17", "If we are thrown into the blazing <em>furnace</em>, the God we serve is able to deliver us from it."),
  ("Daniel 3:25", "He said, 'Look! I see four men walking around in the <em>fire</em>, unbound and unharmed.'"),
  ("Isaiah 43:2", "When you walk through the fire, you will not be burned; the flames will not set you ablaze."),
  ("1 Peter 4:12", "Do not be surprised at the fiery ordeal that has come on you to test you.")],
 [("H784", "Esh — Fire"), ("H5337", "Natsal — Deliver/Rescue"), ("H430", "Elohim — God")]),

("H867", "H", "אֶתְנִי", "Ethni", "Proper noun — Person", "Gift / Munificent",
 "<em>Ethni</em> is a Levite whose name means 'gift' or 'munificent' — generous in giving. He appears in the genealogical records of the gatekeepers appointed under David for temple service.",
 "Even in a minor genealogical reference, the name <em>Ethni</em> (gift) reflects the biblical theology of Levitical service as a gift given back to God. Numbers 8:19 describes the Levites themselves as a gift given to Aaron. Every act of temple service — whether by a celebrated figure or an obscure gatekeeper — was understood as a consecrated offering. The theology of gift-giving runs throughout Scripture: God gives good gifts to His children (James 1:17), and His greatest gift is eternal life in Christ (Romans 6:23). Even a name in a genealogy can preach this.",
 [("1 Chronicles 6:41", "The son of <em>Ethni</em>, the son of Zerah, the son of Adaiah."),
  ("Numbers 8:19", "Of all the Israelites, I have given the Levites as gifts to Aaron and his sons."),
  ("James 1:17", "Every good and perfect gift is from above, coming down from the Father of the heavenly lights."),
  ("Romans 6:23", "For the wages of sin is death, but the gift of God is eternal life in Christ Jesus our Lord."),
  ("1 Chronicles 26:1", "The divisions of the gatekeepers: From the Korahites.")],
 [("H4976", "Mattan — Gift"), ("H5414", "Nathan — Give"), ("H3878", "Levi — Joined/Levite")]),

("H876", "H", "בְּאֵרָה", "Beerah", "Proper noun — Person", "Well / Spring (personal name)",
 "<em>Beerah</em> means 'a well' or 'spring of water' and is the name of a Reubenite leader who was carried into exile by Tiglath-Pileser, king of Assyria. The name speaks of life-giving water — a powerful symbol throughout Scripture.",
 "Water and wells in Scripture consistently point to covenant relationship, provision, and the gift of life. Jacob met Rachel at a well; Moses met his wife at a well; Jesus revealed Himself as the Messiah at a well (John 4). The name <em>Beerah</em> (well/spring) in an exile context is poignant — the one named 'wellspring' was carried away from the land of wells and rivers. Yet God promises to be a spring of living water to the exiles (Isaiah 35:6–7). In Christ, the thirst of exile ends: 'Whoever drinks the water I give them will never thirst again' (John 4:14).",
 [("1 Chronicles 5:6", "<em>Beerah</em> his son, whom Tiglath-Pileser king of Assyria took into exile. He was a leader of the Reubenites."),
  ("John 4:14", "Whoever drinks the water I give them will never thirst. Indeed, the water I give them will become in them a spring of water welling up to eternal life."),
  ("Isaiah 35:6", "Water will gush forth in the wilderness and streams in the desert."),
  ("Psalm 87:7", "As they make music they will sing, 'All my fountains are in you.'"),
  ("Jeremiah 2:13", "They have forsaken me, the spring of living water, and have dug their own cisterns.")],
 [("H875", "Beer — Well"), ("H4325", "Mayim — Water"), ("H2416", "Chay — Life/Living")]),

("H889", "H", "בְּאֹשׁ", "beosh", "Noun, masculine", "Stench / Foul smell",
 "The Hebrew word <em>beosh</em> means stench or foul odor — the putrid smell of decaying matter. It derives from the root <em>baash</em> (H887), meaning to stink or emit a foul odor, used literally for spoiled food and metaphorically for moral corruption.",
 "The imagery of stench in the Old Testament is regularly used to describe the state of those who have abandoned covenant faithfulness. When the Egyptians' water turned to blood, there was a stench (Exodus 7:18). When Israel was oppressed, their situation stank in the nostrils of their oppressors. The prophets used olfactory language to describe moral rottenness (Amos 4:10). Paul, conversely, describes believers as a 'pleasing aroma of Christ' to God (2 Corinthians 2:15–16). Holiness has a fragrance; sin has a stench — a visceral reminder that God's moral categories are as real as physical senses.",
 [("Exodus 16:20", "However, some of them paid no attention to Moses; they kept part of it until morning, but it was full of maggots and began to <em>smell</em>."),
  ("Ecclesiastes 10:1", "As dead flies give perfume a bad smell, so a little folly outweighs wisdom and honor."),
  ("Amos 4:10", "I sent plagues among you as I did to Egypt. I killed your young men with the sword, along with your captured horses. I filled your nostrils with the <em>stench</em> of your camps."),
  ("2 Corinthians 2:15", "For we are to God the pleasing aroma of Christ among those who are being saved."),
  ("Isaiah 3:24", "Instead of fragrance there will be a <em>stench</em>.")],
 [("H887", "Baash — To Stink"), ("H7381", "Reyach — Scent/Smell"), ("H5207", "Nichoach — Soothing/Pleasant")]),

("H901", "H", "בָּגוֹד", "bagod", "Adjective", "Treacherous / Faithless",
 "The Hebrew adjective <em>bagod</em> describes one who is treacherous or faithless — a person who breaks covenant, betrays trust, or acts deceitfully. It derives from the root <em>bagad</em> (H898), meaning to deal treacherously, cover, or act covertly against another.",
 "Treachery is one of the great covenant violations in Scripture. The prophets repeatedly accuse Israel of being <em>bagod</em> — treacherously unfaithful to God, their covenant husband. Jeremiah calls Judah 'faithless Judah' (Jeremiah 3:7–11), and Isaiah describes how 'the treacherous betray' (Isaiah 33:1). The concept is relational at its core: treachery is only possible where trust existed first. God Himself is never <em>bagod</em> — He is the covenant keeper who remains faithful even when His people are faithless (2 Timothy 2:13). His steadfast love (<em>hesed</em>) is the antidote to human treachery.",
 [("Isaiah 33:1", "Woe to you, destroyer, you who have not been destroyed! Woe to you, <em>betrayer</em>, you who have not been betrayed!"),
  ("Jeremiah 3:11", "The Lord said to me, 'Faithless Israel is more righteous than unfaithful Judah.'"),
  ("Hosea 6:7", "As at Adam, they have broken the covenant; they were <em>unfaithful</em> to me there."),
  ("Malachi 2:14", "You have been unfaithful to her, though she is your partner, the wife of your marriage covenant."),
  ("2 Timothy 2:13", "If we are faithless, he remains faithful, for he cannot disown himself.")],
 [("H898", "Bagad — Deal Treacherously"), ("H2617", "Hesed — Steadfast Love"), ("H571", "Emeth — Truth/Faithfulness")]),

("H906", "H", "בַּד", "bad", "Noun, masculine", "Linen / Fine linen thread",
 "The Hebrew word <em>bad</em> refers to linen cloth or linen thread — specifically the fine white linen used in sacred garments. It is the material of the high priest's undergarments, the linen ephod, and the angelic figures described in Daniel and Ezekiel.",
 "Linen in the Old Testament is consistently associated with purity, priestly service, and divine holiness. The high priest wore <em>bad</em> garments on the Day of Atonement — a deliberate stripping down to simple white linen rather than golden vestments, symbolizing humble approach before God. The angelic figure in Daniel 10:5 is clothed in linen, representing heavenly purity. Revelation 19:8 declares that the fine linen of the bride of Christ represents 'the righteous acts of God's holy people.' The material itself becomes a theological symbol: those who draw near to God must be clothed in purity.",
 [("Exodus 28:42", "Make linen undergarments as a covering for the body, reaching from the waist to the thigh."),
  ("Leviticus 16:4", "He is to put on the sacred <em>linen</em> tunic, with <em>linen</em> undergarments next to his body; he is to tie the <em>linen</em> sash around him and put on the <em>linen</em> turban."),
  ("Daniel 10:5", "I looked up and there before me was a man dressed in <em>linen</em>, with a belt of fine gold from Uphaz around his waist."),
  ("Revelation 19:8", "Fine linen, bright and clean, was given her to wear. Fine linen stands for the righteous acts of God's holy people."),
  ("Ezekiel 9:2", "Among them was a man clothed in <em>linen</em> who had a writing kit at his side.")],
 [("H8336", "Shesh — Fine Linen"), ("H3548", "Kohen — Priest"), ("H6944", "Qodesh — Holiness")]),

("H908", "H", "בָּדָא", "bada", "Verb", "Devise / Fabricate / Invent",
 "The Hebrew verb <em>bada</em> means to fabricate, invent, or devise — especially to make up false stories or create unauthorized religious innovations. It carries a negative connotation of manufacturing something that lacks divine authorization.",
 "The term appears most notably in 1 Kings 12:33 to describe Jeroboam's invented festival — he 'devised in his own heart' a month for sacrifice, setting up a counterfeit religious calendar. This becomes the paradigm of unauthorized worship in Israel, repeated as a warning throughout Kings: the sin of Jeroboam who 'made Israel sin.' The theological principle is clear: worship must be according to God's revealed pattern, not human invention. The New Testament carries this forward — Jesus rebukes worship that follows 'rules taught by men' (Matthew 15:9). True faith receives; it does not fabricate.",
 [("1 Kings 12:33", "On the fifteenth day of the eighth month, a month of his own choosing, he offered sacrifices on the altar he had built at Bethel. So he instituted the festival for the Israelites and went up to the altar to make offerings — a month he had <em>devised</em> in his own heart."),
  ("Nehemiah 6:8", "Nothing like what you are saying is happening; you are just making it up out of your head."),
  ("Matthew 15:9", "They worship me in vain; their teachings are merely human rules."),
  ("Deuteronomy 12:32", "See that you do all I command you; do not add to it or take away from it."),
  ("Proverbs 14:12", "There is a way that appears to be right, but in the end it leads to death.")],
 [("H3577", "Kazab — Lie/Falsehood"), ("H8451", "Torah — Law/Instruction"), ("H5927", "Alah — Go Up/Offer")]),

("H912", "H", "בֵּדְיָה", "Bedeyah", "Proper noun — Person", "Servant of Yahweh",
 "<em>Bedeyah</em> (also spelled Bedeiah) is a name meaning 'servant of Yahweh' or 'branch of Yahweh.' He appears in Ezra 10:35 as one of the Israelites who had taken foreign wives and pledged to put them away during Ezra's reform.",
 "The name <em>Bedeyah</em> stands as a theological irony — 'servant of Yahweh' is found among those who had violated the covenant by foreign marriages. Yet this very context demonstrates grace: repentance was still possible. Ezra's reform was not punitive condemnation but covenant renewal. The man named 'servant of Yahweh' answers the call to return. This pictures sanctification: the name we bear in Christ defines who we are becoming, even when our actions fall short. God disciplines and restores those who bear His name.",
 [("Ezra 10:35", "Benaiah, <em>Bedeiah</em>, Keluhi."),
  ("Ezra 10:2", "We have been unfaithful to our God by marrying foreign women from the peoples around us."),
  ("Ezra 10:11", "Now honor the Lord, the God of your ancestors, and do his will. Separate yourselves from the peoples around you."),
  ("Romans 6:22", "But now that you have been set free from sin and have become slaves of God, the benefit you reap leads to holiness."),
  ("Nehemiah 9:2", "Those of Israelite descent had separated themselves from all foreigners. They stood in their places and confessed their sins.")],
 [("H5650", "Ebed — Servant"), ("H3068", "YHWH — The LORD"), ("H7725", "Shuv — Return/Repent")]),

("H927", "H", "בְּהַל", "behal", "Verb (Aramaic)", "Terrify / Disturb / Hasten",
 "The Aramaic verb <em>behal</em> means to terrify, disturb greatly, or hasten. In the Aramaic sections of Daniel, it describes the terror that strikes pagan kings when confronted with divine mysteries — the trembling and confusion that accompanies an encounter with the supernatural.",
 "The trembling that <em>behal</em> describes is the involuntary response of human pride before divine revelation. Nebuchadnezzar is terrified by his dreams; Belshazzar's face goes pale and his knees knock when he sees the handwriting on the wall (Daniel 5:6). This holy terror is not merely fear but the shattering of self-sufficiency. The biblical pattern is consistent: when mortals encounter the divine, they fall on their faces (Revelation 1:17). Yet grace follows terror — 'Do not be afraid' is one of Scripture's most repeated commands. God disturbs human pride to open space for His peace.",
 [("Daniel 4:5", "I had a dream that made me afraid. As I was lying in bed, the images and visions that passed through my mind <em>terrified</em> me."),
  ("Daniel 5:6", "His face turned pale and he was so frightened that his legs became weak and his knees were knocking."),
  ("Daniel 7:15", "I, Daniel, was <em>troubled</em> in spirit, and the visions that passed through my mind disturbed me."),
  ("Revelation 1:17", "When I saw him, I fell at his feet as though dead. Then he placed his right hand on me and said: 'Do not be afraid.'"),
  ("Isaiah 41:10", "So do not fear, for I am with you; do not be dismayed, for I am your God.")],
 [("H6342", "Pachad — Fear/Dread"), ("H1763", "Dechal — Fear [Aramaic]"), ("H7965", "Shalom — Peace")]),

("H929", "H", "בְּהֵמָה", "behemah", "Noun, feminine", "Animal / Beast / Cattle",
 "The Hebrew word <em>behemah</em> is the common term for domestic animals, livestock, or beasts — used broadly for any large quadruped. It appears over 180 times in the Old Testament, spanning creation accounts, dietary laws, property regulations, and poetry. Job 40:15 uses it for the mysterious creature Behemoth.",
 "Animals in biblical thought are not incidental — they are part of God's creation entrusted to human stewardship (Genesis 1:24–28; 2:19–20). The law's concern for animals (Deuteronomy 25:4; Proverbs 12:10) reflects a creation ethic where all living things bear the mark of their Maker. In Job, Behemoth and Leviathan are presented as evidence of God's incomprehensible power — 'Look at Behemoth, which I made along with you' (Job 40:15). The <em>behemah</em> praises God in the Psalms (148:10) and will be restored in the new creation (Isaiah 11:6–8).",
 [("Genesis 1:24", "And God said, 'Let the land produce living creatures according to their kinds: the livestock, the creatures that move along the ground, and the wild animals.'"),
  ("Job 40:15", "Look at <em>Behemoth</em>, which I made along with you and which feeds on grass like an ox."),
  ("Psalm 148:10", "Wild animals and all cattle, small creatures and flying birds."),
  ("Proverbs 12:10", "A righteous man cares for the needs of his animal."),
  ("Deuteronomy 25:4", "Do not muzzle an ox while it is treading out the grain.")],
 [("H2416", "Chay — Living/Animal"), ("H929", "Behemoth — Great Beast"), ("H120", "Adam — Humanity")]),

("H936", "H", "בּוּז", "buz", "Verb / Noun", "Despise / Contempt",
 "The Hebrew word <em>buz</em> means to despise, hold in contempt, or treat as worthless. As a noun it means contempt or scorn. It describes the attitude of treating something or someone as negligible, unworthy of respect, or beneath consideration.",
 "Contempt is one of the most spiritually dangerous sins in the Old Testament. Wisdom literature repeatedly warns against despising: the poor (Proverbs 14:21), parents (Proverbs 15:20), God's correction (Proverbs 3:11), and God's word (Numbers 15:31). The Psalms open with a contrast between those who take delight in God's law and the scornful (<em>luts</em>), but <em>buz</em> captures active dismissal. Esau 'despised his birthright' (Genesis 25:34) — the paradigm of trading the eternal for the temporary. Jesus warned that no one can serve two masters; to choose one is functionally to despise the other (Matthew 6:24).",
 [("Genesis 25:34", "So Esau <em>despised</em> his birthright."),
  ("Proverbs 14:21", "It is a sin to despise one's neighbor, but blessed is the one who is kind to the needy."),
  ("Proverbs 3:11", "Do not despise the Lord's discipline, and do not resent his rebuke."),
  ("Numbers 15:31", "Because they have <em>despised</em> the Lord's word and broken his commands, they must surely be cut off."),
  ("Matthew 6:24", "No one can serve two masters. Either you will hate the one and love the other, or you will be devoted to the one and <em>despise</em> the other.")],
 [("H959", "Bazah — Despise"), ("H7043", "Qalal — Be Slight/Curse"), ("H3519", "Kavod — Glory/Honor")]),

# ══════════════════════════════
#  GREEK (23 words)
# ══════════════════════════════

("G1277", "G", "διαπλέω", "diapleo", "Verb", "Sail across / Sail through",
 "The Greek verb <em>diapleo</em> means to sail across or sail through a body of water. It appears in Acts 27:5 to describe Paul's voyage across the open sea from Myra to Puteoli during his journey to Rome — a voyage that would end in shipwreck.",
 "Paul's sea voyages are theologically significant in Acts. They represent the unstoppable advance of the gospel — even storms, shipwrecks, and imperial prisons could not prevent the word of God from reaching Rome. The act of <em>diapleo</em> (sailing through) becomes a metaphor for persevering mission. Paul's confidence in Acts 27 ('Not one of you will lose a single hair from his head,' v. 34) is grounded not in favorable conditions but in divine promise. The Christian life often requires crossing dangerous open water, trusting the God who commands the seas.",
 [("Acts 27:5", "When we had sailed across the open sea off the coast of Cilicia and Pamphylia, we landed at Myra in Lycia."),
  ("Acts 27:24", "God has graciously given you the lives of all who sail with you."),
  ("Mark 4:39", "He got up, rebuked the wind and said to the waves, 'Quiet! Be still!' Then the wind died down and it was completely calm."),
  ("Psalm 107:23", "Some went out on the sea in ships; they were merchants on the mighty waters."),
  ("Acts 28:14", "And so we came to Rome.")],
 [("G4126", "Pleo — Sail"), ("G3598", "Hodos — Way/Road"), ("G2041", "Ergon — Work/Deed")]),

("G1314", "G", "διαφυλάσσω", "diaphylasso", "Verb", "Guard carefully / Keep safe",
 "The Greek verb <em>diaphylasso</em> means to guard thoroughly, keep carefully, or preserve from harm. The prefix <em>dia-</em> intensifies the verb <em>phylasso</em> (to guard), suggesting complete or thorough protection. It appears in the temptation of Jesus (Luke 4:10), quoted from Psalm 91:11.",
 "When Satan quotes Psalm 91:11 to Jesus — 'He will command his angels to <em>guard</em> you carefully' — he is using a genuine promise to tempt Jesus into testing God. Jesus' response reveals the proper posture: divine protection is not something to be forced or tested but received in trust. The promise of angelic <em>diaphylasso</em> is real, but it operates within surrender to God's will, not as a trump card for reckless presumption. The same God who guards us also leads us — into the wilderness before the victory, into the cross before the resurrection.",
 [("Luke 4:10", "For it is written: 'He will command his angels concerning you to <em>guard</em> you carefully.'"),
  ("Psalm 91:11", "For he will command his angels concerning you to guard you in all your ways."),
  ("John 17:12", "While I was with them, I protected them and kept them safe by that name you gave me."),
  ("1 Peter 1:5", "Who through faith are shielded by God's power until the coming of the salvation that is ready to be revealed."),
  ("Jude 1:1", "To those who are called, who are loved in God the Father and kept for Jesus Christ.")],
 [("G5442", "Phylasso — Guard/Keep"), ("G4929", "Syntasso — Command/Direct"), ("G32", "Angelos — Angel")]),

("G1340", "G", "διϊσχυρίζομαι", "diischyrizomai", "Verb", "Affirm strongly / Insist confidently",
 "The Greek verb <em>diischyrizomai</em> means to insist strongly, affirm confidently, or maintain something with certainty. The compound of <em>dia</em> (thoroughly) and <em>ischyros</em> (strong) suggests an emphatic, firm assertion — standing by one's testimony under pressure.",
 "In Acts 12, the servant girl Rhoda <em>diischyrizomai</em> — she insists with full confidence that Peter is at the door, even when the believers she tells refuse to believe her. The word also appears in Luke 22:59 when bystanders insist that Peter was with Jesus. Ironically, <em>diischyrizomai</em> is used for true testimony that is doubted (Rhoda) and for false identification that is true (Peter's association with Jesus). The word underscores the importance of bold, confident testimony — and the human tendency to doubt the very answers to our own prayers.",
 [("Acts 12:15", "You're out of your mind, they told her. When she kept <em>insisting</em> that it was so, they said, 'It must be his angel.'"),
  ("Luke 22:59", "About an hour later another asserted, 'Certainly this fellow was with him, for he is a Galilean.'"),
  ("Acts 12:14", "When she recognized Peter's voice, she was so overjoyed she ran back without opening it and exclaimed, 'Peter is at the door!'"),
  ("Romans 10:9", "If you declare with your mouth, 'Jesus is Lord,' and believe in your heart that God raised him from the dead, you will be saved."),
  ("1 John 1:3", "We proclaim to you what we have seen and heard.")],
 [("G2478", "Ischyros — Strong"), ("G3140", "Martyreo — Bear Witness"), ("G4102", "Pistis — Faith")]),

("G1345", "G", "δικαίωμα", "dikaioma", "Noun, neuter", "Righteous decree / Righteous act / Ordinance",
 "The Greek noun <em>dikaioma</em> refers to a righteous ordinance, legal decree, or a righteous act — what is declared just or required by righteousness. It can mean a legal statute (Romans 1:32), a righteous deed (Romans 5:18), or the requirements of the law (Romans 2:26).",
 "<em>Dikaioma</em> appears at pivotal moments in Paul's theology of justification. In Romans 5:18, the 'one righteous act' (<em>henos dikaiomatos</em>) of Christ — His obedient death — brings justification and life for all. This contrasts with Adam's one trespass that brought condemnation. The word carries the full legal weight of the law court: Christ's righteous act satisfies the righteous decree of God against sin. Romans 8:4 states that God sent His Son 'so that the righteous requirement (<em>dikaioma</em>) of the law might be fully met in us who live not according to the flesh but according to the Spirit.'",
 [("Romans 5:18", "Just as one trespass resulted in condemnation for all people, so also one <em>righteous act</em> resulted in justification and life for all people."),
  ("Romans 8:4", "In order that the righteous requirement of the law might be fully met in us, who do not live according to the flesh but according to the Spirit."),
  ("Romans 1:32", "Although they know God's righteous decree that those who do such things deserve death, they not only continue to do these very things but also approve of those who practice them."),
  ("Revelation 19:8", "Fine linen stands for the righteous acts of God's holy people."),
  ("Romans 2:26", "So if those who are not circumcised keep the law's requirements, will they not be regarded as though they were circumcised?")],
 [("G1343", "Dikaiosyne — Righteousness"), ("G1342", "Dikaios — Righteous"), ("G2631", "Katakrima — Condemnation")]),

("G1348", "G", "δικαστής", "dikastes", "Noun, masculine", "Judge",
 "The Greek noun <em>dikastes</em> refers to a judge — one who decides cases, pronounces verdicts, or arbitrates disputes. It appears in Stephen's speech in Acts 7 describing Moses as a judge or ruler among his people, and in Luke 12:14 where Jesus refuses to be a civil arbiter.",
 "Jesus' refusal to be a <em>dikastes</em> over an inheritance dispute (Luke 12:14) is revelatory: He came not as a civil judge but as a Savior. Yet the New Testament is clear that Jesus will be the ultimate judge of the living and the dead (Acts 10:42; 2 Timothy 4:1). The irony is striking — the One who refused to divide an earthly inheritance will one day divide humanity as sheep from goats (Matthew 25:32). Moses as <em>dikastes</em> among the Israelites in Egypt is a type of Christ, misunderstood and rejected by his own people before becoming their deliverer.",
 [("Luke 12:14", "Jesus replied, 'Man, who appointed me a <em>judge</em> or an arbiter between you?'"),
  ("Acts 7:27", "But the man who was mistreating the other pushed Moses aside and said, 'Who made you ruler and <em>judge</em> over us?'"),
  ("Acts 10:42", "He commanded us to preach to the people and to testify that he is the one whom God appointed as judge of the living and the dead."),
  ("2 Timothy 4:1", "In the presence of God and of Christ Jesus, who will judge the living and the dead."),
  ("James 4:12", "There is only one Lawgiver and Judge, the one who is able to save and destroy.")],
 [("G2923", "Krites — Judge"), ("G1343", "Dikaiosyne — Righteousness"), ("G2920", "Krisis — Judgment")]),

("G1350", "G", "δίκτυον", "diktyon", "Noun, neuter", "Net (fishing)",
 "The Greek noun <em>diktyon</em> refers to a fishing net — the large drag net used to gather fish in large quantities from the Sea of Galilee. It is distinct from the smaller cast net and appears in the calling of the disciples and in the post-resurrection appearance by the sea.",
 "The fishing net is one of Jesus' central images for the kingdom of God and discipleship. The parable of the net (Matthew 13:47–50) describes the kingdom as a net that gathers fish of every kind, with the final sorting reserved for the end of the age. At the calling of Peter and Andrew, Jesus transforms their occupation: 'I will make you fishers of men' — the net becomes a symbol of evangelism. In John 21, the miraculous catch after the resurrection (153 large fish, net unbroken) is a sign of the church's mission: the net of God will not break under the weight of those being saved.",
 [("Matthew 13:47", "Once again, the kingdom of heaven is like a <em>net</em> that was let down into the lake and caught all kinds of fish."),
  ("John 21:6", "He said, 'Throw your <em>net</em> on the right side of the boat and you will find some.' When they did, they were unable to haul the net in because of the large number of fish."),
  ("Matthew 4:20", "At once they left their <em>nets</em> and followed him."),
  ("John 21:11", "Simon Peter climbed aboard and dragged the <em>net</em> ashore. It was full of large fish, 153, but even with so many the net was not torn."),
  ("Luke 5:6", "When they had done so, they caught such a large number of fish that their <em>nets</em> began to break.")],
 [("G293", "Amphiblestron — Cast Net"), ("G232", "Halieus — Fisherman"), ("G932", "Basileia — Kingdom")]),

("G1353", "G", "διοδεύω", "diodeuo", "Verb", "Travel through / Pass through",
 "The Greek verb <em>diodeuo</em> means to travel through, pass through, or journey across a region. It describes the movement of going from one place to another, traversing territory. It appears in Luke and Acts in the context of Jesus' and Paul's missionary travels.",
 "The missionary journeys in the New Testament are deliberately described with movement verbs like <em>diodeuo</em>, communicating that the gospel does not stay in one place — it travels, passes through, penetrates regions. Jesus is described passing through towns and villages, teaching (Luke 8:1). Paul and Silas traveled through region after region strengthening the churches (Acts 15:3). The movement of the gospel is Spirit-driven (Acts 16:6–7, where the Spirit prevents entry into certain areas). The Great Commission itself is movement-language: 'Go and make disciples of all nations.' Faithful discipleship has legs.",
 [("Luke 8:1", "After this, Jesus traveled about from one town and village to another, proclaiming the good news of the kingdom of God."),
  ("Acts 17:1", "When Paul and his companions had passed through Amphipolis and Apollonia, they came to Thessalonica."),
  ("Luke 13:22", "Then Jesus went through the towns and villages, teaching as he made his way to Jerusalem."),
  ("Acts 15:3", "The church sent them on their way, and as they traveled through Phoenicia and Samaria, they told how the Gentiles had been converted."),
  ("Matthew 28:19", "Therefore go and make disciples of all nations.")],
 [("G3593", "Hodeuo — Travel"), ("G2064", "Erchomai — Come/Go"), ("G2784", "Kerusso — Preach/Proclaim")]),

("G1366", "G", "δίστομος", "distomos", "Adjective", "Two-edged / Double-mouthed",
 "The Greek adjective <em>distomos</em> literally means 'having two mouths' — from <em>dis</em> (twice) and <em>stoma</em> (mouth). It is used to describe a sword that is sharp on both edges, cutting in both directions. The term appears in Hebrews 4:12 and Revelation 1:16; 2:12 to describe the word of God and the sword of Christ.",
 "The image of the two-edged sword is one of the New Testament's most powerful metaphors for Scripture's penetrating power. Hebrews 4:12 declares that the word of God is 'sharper than any double-edged sword, it penetrates even to dividing soul and spirit, joints and marrow.' No part of the inner person is hidden from it. In Revelation, the risen Christ has a sharp two-edged sword coming from His mouth — the word of judgment and salvation that proceeds from Him. The <em>distomos</em> sword cuts both ways: it wounds with conviction and heals with grace; it judges sin and declares righteousness.",
 [("Hebrews 4:12", "For the word of God is alive and active. Sharper than any <em>double-edged sword</em>, it penetrates even to dividing soul and spirit."),
  ("Revelation 1:16", "In his right hand he held seven stars, and coming out of his mouth was a sharp, <em>double-edged sword</em>."),
  ("Revelation 2:12", "These are the words of him who has the sharp, <em>double-edged sword</em>."),
  ("Ephesians 6:17", "Take the helmet of salvation and the sword of the Spirit, which is the word of God."),
  ("Isaiah 49:2", "He made my mouth like a sharpened sword.")],
 [("G4501", "Rhomphaia — Large Sword"), ("G3056", "Logos — Word"), ("G3056", "Logos — Word of God")]),

("G1378", "G", "δόγμα", "dogma", "Noun, neuter", "Decree / Ordinance / Doctrine",
 "The Greek noun <em>dogma</em> refers to an official decree, ordinance, or established teaching — an authoritative pronouncement that demands compliance. In the New Testament it is used for imperial decrees (Luke 2:1; Acts 17:7), for the rulings of the Jerusalem council (Acts 16:4), and for the legal ordinances abolished in Christ (Colossians 2:14; Ephesians 2:15).",
 "The word <em>dogma</em> carries the weight of official authority. Caesar's <em>dogma</em> triggered the census that brought Joseph and Mary to Bethlehem — God used an imperial decree to fulfill prophecy (Micah 5:2). Paul declares that Christ 'canceled the written code, with its regulations (<em>dogmasin</em>), that was against us' (Colossians 2:14). The law's condemning decrees are nailed to the cross. Yet the Jerusalem council also issues <em>dogmata</em> — apostolic guidelines for Gentile believers. Not all dogma is abolished; authoritative apostolic teaching is to be delivered and obeyed (Acts 16:4).",
 [("Luke 2:1", "In those days Caesar Augustus issued a <em>decree</em> that a census should be taken of the entire Roman world."),
  ("Acts 16:4", "As they traveled from town to town, they delivered the decisions reached by the apostles and elders in Jerusalem for the people to obey."),
  ("Colossians 2:14", "Having canceled the charge of our legal indebtedness, which stood against us and condemned us; he has taken it away, nailing it to the cross."),
  ("Ephesians 2:15", "By setting aside in his flesh the law with its commands and regulations."),
  ("Acts 17:7", "They are all defying Caesar's decrees, saying that there is another king, one called Jesus.")],
 [("G3551", "Nomos — Law"), ("G1785", "Entole — Commandment"), ("G575", "Apo — From/Away")]),

("G1382", "G", "δοκιμή", "dokime", "Noun, feminine", "Proven character / Tested quality / Approval",
 "The Greek noun <em>dokime</em> refers to the quality of being tested and proved — the character that emerges from successfully enduring trials. It is related to <em>dokimazo</em> (to test/approve) and describes not merely the testing process but the proven result: character refined and validated.",
 "<em>Dokime</em> is central to Paul's theology of suffering and sanctification. In Romans 5:3–4, he traces the chain: suffering produces <em>hupomone</em> (endurance), endurance produces <em>dokime</em> (proven character), and proven character produces hope. This is not a path Paul observes from a distance — he knows it from the inside. In 2 Corinthians 2:9, he writes that he tested the Corinthians to know their <em>dokime</em> — whether they would obey in everything. Faith untested is faith unproven; faith that has passed through the fire has <em>dokime</em> that cannot be manufactured any other way.",
 [("Romans 5:4", "Perseverance must finish its work so that you may be mature and complete, not lacking anything. And perseverance produces proven character (<em>dokimen</em>), and proven character, hope."),
  ("2 Corinthians 2:9", "Another reason I wrote you was to see if you would stand the test and be obedient in everything."),
  ("2 Corinthians 9:13", "Because of the service by which you have proved yourselves, others will praise God."),
  ("Philippians 2:22", "But you know that Timothy has proved himself, because as a son with his father he has served with me in the work of the gospel."),
  ("1 Peter 1:7", "These have come so that the proven genuineness of your faith — of greater worth than gold, which perishes even though refined by fire — may result in praise, glory, and honor.")],
 [("G1381", "Dokimazo — Test/Approve"), ("G5281", "Hupomone — Endurance"), ("G1680", "Elpis — Hope")]),

("G1385", "G", "δοκός", "dokos", "Noun, feminine", "Wooden beam / Log",
 "The Greek noun <em>dokos</em> refers to a large wooden beam or log — the kind used in construction to support a roof or structure. Jesus uses it in one of His most memorable and convicting illustrations about judgment and hypocrisy.",
 "The parable of the speck and the log (Matthew 7:3–5; Luke 6:41–42) uses <em>dokos</em> for devastating rhetorical effect. How can you see the speck in your brother's eye while a whole beam is in your own? The absurdity of the image drives the point home: self-righteous judgment of others is inversely proportional to self-awareness. The <em>dokos</em> represents the blindness that comes with spiritual pride. Jesus is not forbidding discernment — He says 'first take the log out of your own eye, then you will see clearly to remove the speck from your brother's eye.' Genuine correction comes from humility, not superiority.",
 [("Matthew 7:3", "Why do you look at the speck of sawdust in your brother's eye and pay no attention to the <em>plank</em> in your own eye?"),
  ("Luke 6:42", "How can you say to your brother, 'Brother, let me take the speck out of your eye,' when you yourself fail to see the <em>plank</em> in your own eye?"),
  ("Matthew 7:5", "You hypocrite, first take the <em>plank</em> out of your own eye, and then you will see clearly to remove the speck from your brother's eye."),
  ("Romans 2:1", "You, therefore, have no excuse, you who pass judgment on someone else, for at whatever point you judge another, you are condemning yourself."),
  ("Galatians 6:1", "Brothers and sisters, if someone is caught in a sin, you who live by the Spirit should restore that person gently.")],
 [("G2595", "Karphos — Speck/Splinter"), ("G5273", "Hupokrites — Hypocrite"), ("G2920", "Krisis — Judgment")]),

("G1393", "G", "Δορκάς", "Dorkas", "Proper noun — Person", "Gazelle (also Tabitha)",
 "<em>Dorkas</em> is the Greek equivalent of the Aramaic name Tabitha, both meaning 'gazelle.' She was a disciple in Joppa, 'always doing good and helping the poor' (Acts 9:36), who died and was raised from the dead by Peter — one of the two resurrection miracles performed by an apostle in Acts.",
 "Dorcas/Tabitha represents the practical theology of mercy ministry. Her testimony is not a list of doctrinal positions but garments she made for widows — the living evidence of grace working through willing hands. When she dies, the weeping widows show Peter the coats and garments she had made. Her resurrection becomes an evangelistic event: 'This became known all over Joppa, and many people believed in the Lord' (Acts 9:42). Dorcas teaches that faithful service to the poor is not separate from the gospel — it is the gospel made visible. Her name, Gazelle, is beautifully fitting: graceful, quick, gentle in movement.",
 [("Acts 9:36", "<em>Tabitha</em> (in Greek her name is <em>Dorcas</em>); she was always doing good and helping the poor."),
  ("Acts 9:39", "All the widows stood around him, crying and showing him the robes and other clothing that <em>Dorcas</em> had made while she was still with them."),
  ("Acts 9:40", "Peter sent them all out of the room; then he got down on his knees and prayed. Turning toward the dead woman, he said, 'Tabitha, get up.'"),
  ("James 2:17", "In the same way, faith by itself, if it is not accompanied by action, is dead."),
  ("Matthew 25:40", "Whatever you did for one of the least of these brothers and sisters of mine, you did for me.")],
 [("G5503", "Chera — Widow"), ("G2041", "Ergon — Work/Deed"), ("G1654", "Eleemosyne — Almsgiving")]),

("G1402", "G", "δουλόω", "douloo", "Verb", "Enslave / Make a slave / Bond",
 "The Greek verb <em>douloo</em> means to enslave, reduce to slavery, or bring into bondage. It appears in Paul's letters describing both the bondage of sin and, paradoxically, the voluntary enslavement to righteousness and to God that characterizes the redeemed life.",
 "Paul's use of <em>douloo</em> in Romans 6 is rhetorically brilliant. He argues that all people are enslaved to something — either to sin or to God. 'You have been set free from sin and have become slaves to righteousness' (Romans 6:18). The freedom Christ brings is not autonomy but a transfer of masters: from a cruel master (sin, which pays death) to a gracious one (God, who gives eternal life). In 1 Corinthians 9:19, Paul says he makes himself a slave (<em>edoulosa</em>) to everyone for the sake of the gospel — voluntary, love-driven servitude that images Christ's own kenosis (Philippians 2:7).",
 [("Romans 6:18", "You have been set free from sin and have become <em>slaves to righteousness</em>."),
  ("Romans 6:22", "But now that you have been set free from sin and have become slaves of God, the benefit you reap leads to holiness."),
  ("1 Corinthians 9:19", "Though I am free and belong to no one, I have made myself a slave to everyone, to win as many as possible."),
  ("Galatians 4:3", "So also, when we were underage, we were in slavery under the elemental spiritual forces of the world."),
  ("John 8:34", "Very truly I tell you, everyone who sins is a slave to sin.")],
 [("G1401", "Doulos — Slave/Servant"), ("G1659", "Eleutheroo — Set Free"), ("G266", "Hamartia — Sin")]),

("G1412", "G", "δυναμόω", "dynamoo", "Verb", "Strengthen / Empower / Enable",
 "The Greek verb <em>dynamoo</em> means to strengthen, empower, or give ability to someone — derived from <em>dynamis</em> (power, might). It describes the impartation of divine strength to those who are weak, especially in the context of spiritual endurance and faithful living.",
 "The concept of divine empowerment is central to Paul's theology of weakness and grace. In Colossians 1:11, Paul prays that believers be 'strengthened with all power according to his glorious might so that you may have great endurance and patience.' This is not self-generated fortitude but divinely imparted capacity. The same <em>dunamis</em> that raised Jesus from the dead is at work in believers (Ephesians 1:19–20). When the disciples were told to wait in Jerusalem for the promise, they received the Spirit and became fearless proclaimers — <em>dynamoo</em> is what happened at Pentecost. God does not call the equipped; He equips the called.",
 [("Colossians 1:11", "Being <em>strengthened</em> with all power according to his glorious might so that you may have great endurance and patience."),
  ("Ephesians 6:10", "Finally, be strong in the Lord and in his mighty power."),
  ("Acts 9:22", "Yet Saul grew more and more powerful and baffled the Jews living in Damascus by proving that Jesus is the Messiah."),
  ("2 Timothy 2:1", "You then, my son, be strong in the grace that is in Christ Jesus."),
  ("Philippians 4:13", "I can do all this through him who gives me strength.")],
 [("G1411", "Dynamis — Power"), ("G2480", "Ischyo — Be Strong"), ("G4147", "Plouteo — Be Rich")]),

("G1416", "G", "δύνω", "duno", "Verb", "Set (of the sun) / Sink down",
 "The Greek verb <em>duno</em> means to sink, set, or go down — used specifically of the sun setting. It appears in Mark 1:32 and Luke 4:40, describing the moment when the sabbath ended (at sunset) and crowds brought the sick to Jesus for healing.",
 "The setting sun in these parallel accounts is not merely a time marker — it is a literary frame for Jesus' compassion. As the day ends and the light fades, the crowds gather: 'When the sun was setting (<em>dunontos</em>), the people brought to Jesus all who had various kinds of sickness, and laying his hands on each one, he healed them.' The close of the sabbath freed those restricted from travel; but what brings them is not freedom from law — it is the presence of the Healer. The sun sets on human time, but Christ's healing power operates beyond the clock. He is the 'sun of righteousness' (Malachi 4:2) who never ultimately sets.",
 [("Mark 1:32", "That evening after sunset, the people brought to Jesus all the sick and demon-possessed."),
  ("Luke 4:40", "At sunset, the people brought to Jesus all who had various kinds of sickness, and laying his hands on each one, he healed them."),
  ("Psalm 113:3", "From the rising of the sun to the place where it sets, the name of the Lord is to be praised."),
  ("Malachi 4:2", "But for you who revere my name, the sun of righteousness will rise with healing in its rays."),
  ("Ephesians 4:26", "Do not let the sun go down while you are still angry.")],
 [("G395", "Anatole — Rising/East"), ("G2243", "Helias — Elijah"), ("G2390", "Iaomai — Heal")]),

("G1433", "G", "δωρέομαι", "doreomai", "Verb", "Give / Bestow / Grant as a gift",
 "The Greek verb <em>doreomai</em> means to give freely, bestow as a gift, or grant graciously — emphasizing the voluntary, generous character of the giving. It is used of both human generosity and divine grace, particularly the gifts that flow from Christ.",
 "<em>Doreomai</em> appears at a crucial moment in Mark 15:45: Pilate 'granted' (<em>edoreesato</em>) the body of Jesus to Joseph of Arimathea. Even the burial of the Lord came through an act of human generosity enabled by official permission. Peter uses the verb in 2 Peter 1:3–4 to describe how God's 'divine power has given (<em>dedoreemenees</em>) us everything we need for a godly life.' The gifts of divine nature, precious promises — everything required for life and godliness — are bestowed, not earned. <em>Doreomai</em> is grace made concrete: God opens His hand and gives what no merit could obtain.",
 [("Mark 15:45", "When he learned from the centurion that it was so, he <em>gave</em> the body to Joseph."),
  ("2 Peter 1:3", "His divine power has given us everything we need for a godly life through our knowledge of him who called us by his own glory and goodness."),
  ("2 Peter 1:4", "Through these he has given us his very great and precious promises."),
  ("John 3:16", "For God so loved the world that he gave his one and only Son."),
  ("Romans 8:32", "He who did not spare his own Son, but gave him up for us all — how will he not also, along with him, graciously give us all things?")],
 [("G1435", "Doron — Gift"), ("G5485", "Charis — Grace"), ("G1325", "Didomi — Give")]),

("G1436", "G", "ἔα", "ea", "Interjection", "Ah! / Ha! / Leave alone!",
 "The Greek interjection <em>ea</em> is an exclamation of surprise, alarm, or command — roughly equivalent to 'ah!', 'ha!', or 'leave us alone!' It appears in Luke 4:34 in the words of the demonic spirit that cries out when confronted by Jesus in the synagogue at Capernaum.",
 "The demon's cry <em>ea!</em> is the involuntary recognition of a superior power. Confronted with the Holy One of God, the unclean spirit shouts: 'Ha! What do you want with us, Jesus of Nazareth? Have you come to destroy us?' The exclamation reveals the terror of the demonic realm before Christ's authority. This moment is significant: in the synagogue — a place of worship and teaching — an unclean spirit had been present, apparently undetected. Jesus' arrival immediately exposed and expelled it. The gospel regularly disrupts comfortable, religious settings, forcing a confrontation with the real and powerful Christ who tolerates no rivals.",
 [("Luke 4:34", "<em>'Ha!</em> What do you want with us, Jesus of Nazareth? Have you come to destroy us? I know who you are — the Holy One of God!'"),
  ("Mark 1:24", "'What do you want with us, Jesus of Nazareth? Have you come to destroy us? I know who you are — the Holy One of God!'"),
  ("James 2:19", "You believe that there is one God. Good! Even the demons believe that — and shudder."),
  ("Luke 4:36", "All the people were amazed and said to each other, 'What words these are! With authority and power he gives orders to impure spirits and they come out!'"),
  ("Philippians 2:10", "That at the name of Jesus every knee should bow, in heaven and on earth and under the earth.")],
 [("G169", "Akathartos — Unclean"), ("G1849", "Exousia — Authority"), ("G40", "Hagios — Holy")]),

("G1439", "G", "ἐάω", "eao", "Verb", "Let / Allow / Permit / Leave alone",
 "The Greek verb <em>eao</em> means to allow, permit, let something occur, or leave something alone. It is used in contexts where someone either grants permission or refrains from preventing an action. It appears in Acts when Paul prevents a would-be suicide, and in Luke when Jesus permits a group to bring children to Him.",
 "<em>Eao</em> is the verb of permission and restraint — sometimes God's 'allowing' carries deep theological weight. In Acts 14:16, Paul says God 'permitted' all nations to go their own ways in past generations — a form of divine patience, not approval. In Acts 27:32, soldiers cut the ropes of the lifeboat and 'let' it fall away. In Luke's parallel to 'Let the children come to me' (<em>aphete</em>), the disciples prevented and Jesus permitted. The theological principle: there are things God allows and things He restrains; wisdom and faith involve discerning which is which, and trusting His governance in both.",
 [("Acts 14:16", "In the past, he let all nations go their own way."),
  ("Acts 27:32", "So the soldiers cut the ropes that held the lifeboat and let it drift away."),
  ("Acts 16:7", "They tried to enter Bithynia, but the Spirit of Jesus would not allow them to."),
  ("Mark 10:14", "Let the little children come to me, and do not hinder them, for the kingdom of God belongs to such as these."),
  ("1 Corinthians 10:13", "God is faithful; he will not let you be tempted beyond what you can bear.")],
 [("G863", "Aphiemi — Let Go/Forgive"), ("G2010", "Epitrepo — Permit"), ("G2967", "Kolyo — Hinder")]),

("G1449", "G", "ἐγγράφω", "eggrapho", "Verb", "Write in / Inscribe / Record",
 "The Greek verb <em>eggrapho</em> means to write in, inscribe, or record in a document or medium. The prefix <em>en-</em> (in) combines with <em>grapho</em> (to write) to emphasize the writing of something <em>into</em> a surface — tablets, scrolls, or hearts.",
 "The theology of being 'written in' carries immense weight in Scripture. Moses asks God to blot his name from God's book rather than see Israel destroyed — and God says He will only blot out the names of the sinners (Exodus 32:32–33). Jesus tells the seventy-two disciples to rejoice not that spirits submit to them but that their names are 'written in heaven' (Luke 10:20). Paul uses <em>eggrapho</em> in 2 Corinthians 3:3 to describe believers as 'a letter from Christ... written not with ink but with the Spirit of the living God, not on tablets of stone but on tablets of human hearts.' The greatest inscription is the law written not on stone but within the renewed heart.",
 [("Luke 10:20", "However, do not rejoice that the spirits submit to you, but rejoice that your names are <em>written</em> in heaven."),
  ("2 Corinthians 3:3", "You show that you are a letter from Christ, the result of our ministry, written not with ink but with the Spirit of the living God, not on tablets of stone but on tablets of human hearts."),
  ("Exodus 32:32", "But now, please forgive their sin — but if not, then blot me out of the book you have written."),
  ("Revelation 20:15", "Anyone whose name was not found written in the book of life was thrown into the lake of fire."),
  ("Jeremiah 31:33", "I will put my law in their minds and write it on their hearts.")],
 [("G1125", "Grapho — Write"), ("G975", "Biblion — Scroll/Book"), ("G2588", "Kardia — Heart")]),

("G1454", "G", "ἔγερσις", "egersis", "Noun, feminine", "Resurrection / Rising up / Awakening",
 "The Greek noun <em>egersis</em> means a raising up, resurrection, or awakening — derived from the verb <em>egeiro</em> (to raise, arouse, wake). It appears in Matthew 27:53, describing the resurrection of the saints that occurred after Jesus' own resurrection.",
 "The <em>egersis</em> of Matthew 27:52–53 — where 'many holy people who had died were raised to life' after Christ's resurrection — is one of the most mysterious and theologically rich events in the Gospels. It demonstrates that Jesus' resurrection is not an isolated event but the firstfruits of a general resurrection (1 Corinthians 15:20). His rising triggered a preliminary resurrection of the saints as a sign. <em>Egersis</em> is also used in early Christian literature for the daily 'awakening' of the believer — the spiritual resurrection that baptism enacts (Romans 6:4; Ephesians 5:14). The resurrection of the body at the last day is the final <em>egersis</em>, the ultimate awakening.",
 [("Matthew 27:53", "They came out of the tombs after Jesus' resurrection (<em>egersin</em>) and went into the holy city and appeared to many people."),
  ("1 Corinthians 15:20", "But Christ has indeed been raised from the dead, the firstfruits of those who have fallen asleep."),
  ("Romans 6:4", "We were therefore buried with him through baptism into death in order that, just as Christ was raised from the dead through the glory of the Father, we too may live a new life."),
  ("Ephesians 5:14", "'Wake up, sleeper, rise from the dead, and Christ will shine on you.'"),
  ("John 11:25", "Jesus said to her, 'I am the resurrection and the life.'")],
 [("G386", "Anastasis — Resurrection"), ("G1453", "Egeiro — Rise/Raise"), ("G2222", "Zoe — Life")]),

("G1464", "G", "ἐγκοπή", "egkope", "Noun, feminine", "Hindrance / Obstacle / Interruption",
 "The Greek noun <em>egkope</em> means a hindrance, obstacle, or interruption — from <em>en</em> (in) and <em>kopto</em> (to cut). It conveys the image of something cut into one's path, blocking forward progress. Paul uses it in 1 Corinthians 9:12 to describe the kind of obstacle that would impede the gospel.",
 "Paul is unusually sensitive to anything that might create a <em>egkope</em> — a stumbling block to the gospel's advance. In 1 Corinthians 9:12, he says he endures everything 'rather than hinder the gospel of Christ.' His willingness to waive his apostolic rights (support, food, marriage) is driven by a single concern: no hindrance to the message. This is the architecture of missional sacrifice — not earning salvation, but removing obstacles between the lost and the gospel. Believers are called to examine their lives for <em>egkopai</em>: habits, attitudes, relationships that cut into others' path toward Christ.",
 [("1 Corinthians 9:12", "But we did not use this right. On the contrary, we put up with anything rather than <em>hinder</em> the gospel of Christ."),
  ("Romans 14:13", "Therefore let us stop passing judgment on one another. Instead, make up your mind not to put any stumbling block or obstacle in the way of a brother or sister."),
  ("1 Thessalonians 2:18", "For we wanted to come to you — certainly I, Paul, did, again and again — but Satan blocked our way."),
  ("Galatians 5:7", "You were running a good race. Who cut in on you to keep you from obeying the truth?"),
  ("1 Corinthians 8:9", "Be careful, however, that the exercise of your rights does not become a stumbling block to the weak.")],
 [("G4348", "Proskomma — Stumbling Block"), ("G4625", "Skandalon — Snare/Offense"), ("G2784", "Kerusso — Preach")]),

("G1469", "G", "ἐγκρίνω", "egkrino", "Verb", "Classify / Consider among / Count equal to",
 "The Greek verb <em>egkrino</em> means to reckon among, classify alongside, or consider oneself equal to a group. It appears in 2 Corinthians 10:12 in Paul's ironic contrast between himself and self-commending teachers who measure themselves by themselves.",
 "Paul's use of <em>egkrino</em> is devastatingly ironic: 'We do not dare to classify or compare ourselves with some who commend themselves. When they measure themselves by themselves and compare themselves with themselves, they are not wise.' Self-referential comparison — using your own group as the standard for excellence — produces spiritual blindness and pride. True apostolic authority is not self-certified but demonstrated by changed lives and divine approval. Paul boasts not in his own credentials but in his weakness (2 Corinthians 11–12), because that is where Christ's power is made perfect. The antidote to self-classification is cruciformity: being found in Christ, not in one's own righteousness (Philippians 3:9).",
 [("2 Corinthians 10:12", "We do not dare to <em>classify</em> or compare ourselves with some who commend themselves."),
  ("Philippians 3:9", "And be found in him, not having a righteousness of my own that comes from the law, but that which is through faith in Christ."),
  ("2 Corinthians 12:9", "But he said to me, 'My grace is sufficient for you, for my power is made perfect in weakness.'"),
  ("Luke 18:11", "The Pharisee stood by himself and prayed: 'God, I thank you that I am not like other people.'"),
  ("1 Corinthians 4:3", "I care very little if I am judged by you or by any human court; indeed, I do not even judge myself.")],
 [("G4793", "Synkrino — Compare"), ("G2744", "Kauchaomai — Boast"), ("G5012", "Tapeinophrosyne — Humility")]),

("G1474", "G", "ἐδαφίζω", "edaphizo", "Verb", "Dash to the ground / Level / Raze to the ground",
 "The Greek verb <em>edaphizo</em> means to dash to the ground, smash to the earth, or raze level with the ground. Derived from <em>edaphos</em> (ground, foundation), it conveys total destruction and leveling. It appears in Jesus' weeping lament over Jerusalem (Luke 19:44).",
 "When Jesus weeps over Jerusalem (Luke 19:41–44), His lament includes a devastating prophecy: enemies will 'dash you to the ground (<em>edaphiousin</em>), you and the children within your walls.' This was fulfilled with horrifying precision in 70 AD when the Romans under Titus destroyed Jerusalem, leveling the temple and slaughtering or enslaving the population. Jesus' grief is not vindictive but deeply compassionate — He wept before He predicted. The destruction came not because God abandoned Jerusalem but because Jerusalem did not recognize 'the time of God's coming.' <em>Edaphizo</em> warns that rejecting the visitation of peace leads to ruin; receiving it leads to life.",
 [("Luke 19:44", "They will dash you to the ground, you and the children within your walls. They will not leave one stone on another, because you did not recognize the time of God's coming to you."),
  ("Luke 19:41", "As he approached Jerusalem and saw the city, he wept over it."),
  ("Matthew 24:2", "Do you see all these things? Truly I tell you, not one stone here will be left on another; every one will be thrown down."),
  ("Psalm 137:9", "Happy is the one who seizes your infants and dashes them against the rocks."),
  ("Isaiah 3:8", "Jerusalem staggers, Judah is falling; their words and deeds are against the Lord.")],
 [("G1487", "Ei — If"), ("G2799", "Klaio — Weep"), ("G1515", "Eirene — Peace")]),

]

# ─── WRITE FILES ─────────────────────────────────────────────────────────────
created = 0
skipped = 0
for entry in WORDS:
    strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related = entry
    fname = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    if os.path.exists(fname):
        skipped += 1
        continue
    html = make_page(strongs_id, lang, script, translit, pos, gloss, definition, theology, verses, related)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    created += 1
    print(f"  ✓ {strongs_id} — {gloss}")

print(f"\nDone: {created} created, {skipped} skipped")
