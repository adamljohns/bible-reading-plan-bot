#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch Mar 28 batch3"""
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

def make_page(strongs_id, lang, script, translit, pos, gloss, short_def, definition, theology, verses, related):
    lang_label = "Hebrew · Old Testament" if lang == "H" else "Greek · New Testament"
    num = strongs_id[1:]
    title = f"{strongs_id} — {translit} ({gloss})"
    blb_lang = "g" if lang == "G" else "h"
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
    <meta property="og:description" content="{gloss} — {'Hebrew' if lang=='H' else 'Greek'} word study. Strong's {strongs_id}.">
    <meta name="description" content="{gloss} — {'Hebrew' if lang=='H' else 'Greek'} word study. Strong's {strongs_id}. USMC Ministries Greek &amp; Hebrew Lexicon.">
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
                <a href="https://www.blueletterbible.org/lexicon/{strongs_id.lower()}/kjv/{'wlc' if lang=='H' else 'tr'}/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/{'hebrew' if lang=='H' else 'greek'}/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>
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

# ─────────────────────────────────────────────
# HEBREW ENTRIES (24)
# ─────────────────────────────────────────────
hebrew_entries = [

    (2086, "זֵד", "Zed", "Adjective / Noun", "Proud; Arrogant; Insolent",
     "One who acts with presumptuous arrogance; the insolent, proud rebel against God.",
     "The Hebrew <em>zed</em> (Strong's H2086) describes someone who acts with proud presumption — the arrogant person who overreaches their place before God. In Psalm 119:51, the psalmist declares: 'The <em>arrogant</em> (<em>zedim</em>) mock me without restraint.' In Malachi 3:15, the wicked call the <em>arrogant</em> (<em>zedim</em>) blessed. The term carries a strong moral and spiritual charge — it describes those who defy God's authority.",
     "The <em>zed</em> represents the antithesis of the humble seeker after God. In Proverbs and Psalms, the proud (<em>zedim</em>) are consistently contrasted with those who walk in God's ways. Malachi 4:1 warns that the day of the Lord will burn up the <em>zedim</em> like stubble in a furnace. This is the ultimate end of arrogance that refuses to submit to God. The believer is called to self-examination: is there any <em>zed</em> in my heart that must be mortified?",
     [("Psalm 119:51", "The <em>arrogant</em> mock me without restraint, but I do not turn from your law."),
      ("Malachi 3:15", "But now we call the <em>arrogant</em> blessed. Certainly evildoers prosper, and even when they put God to the test, they escape."),
      ("Malachi 4:1", "Surely the day is coming; it will burn like a furnace. All the <em>arrogant</em> and every evildoer will be stubble."),
      ("Proverbs 21:24", "The proud and <em>arrogant</em> person — 'Mocker' is his name — behaves with insolent fury."),
      ("Psalm 119:78", "May the <em>arrogant</em> be put to shame for wronging me without cause.")],
     [("H1347", "Gaon (Pride/Majesty)"), ("H6184", "Arits (Fierce/Tyrant)"), ("H8217", "Shaphal (Lowly)")]),

    (2096, "זֹהַר", "Zohar", "Noun, masculine", "Brightness; Splendor; Radiance",
     "Shining brightness, brilliance, or radiance — used of heavenly glory and the wise.",
     "The Hebrew <em>zohar</em> (H2096) means brilliant radiance or shining brightness. Its most theologically significant occurrence is in Daniel 12:3: 'Those who are wise will shine like the <em>brightness</em> (<em>zohar</em>) of the heavens, and those who lead many to righteousness, like the stars forever and ever.' This verse gives the word an eschatological dimension — the righteous, in the resurrection age, shine with divine brightness.",
     "<em>Zohar</em> in Daniel 12:3 is a resurrection promise — those who impart wisdom and lead others to righteousness will bear a glory analogous to the heavens themselves. This connects to NT language about believers shining as lights in the world (Philippians 2:15) and the transformation of the righteous at the resurrection (1 Corinthians 15:40-41). The concept resonates with the Transfiguration — Christ's face shining like the sun — as a foretaste of the glorified state. To be 'wise' in the biblical sense is not intellectual achievement but covenant faithfulness that radiates God's glory.",
     [("Daniel 12:3", "Those who are wise will shine like the <em>brightness</em> of the heavens, and those who lead many to righteousness, like the stars for ever and ever."),
      ("Matthew 13:43", "Then the righteous will shine like the sun in the kingdom of their Father."),
      ("Philippians 2:15", "So that you may become blameless and pure, children of God without fault in a warped and crooked generation. Then you will shine among them like stars in the sky."),
      ("1 Corinthians 15:41", "The sun has one kind of splendor, the moon another and the stars another; and star differs from star in splendor."),
      ("Ezekiel 1:27", "I saw that from what appeared to be his waist up he looked like glowing metal, as if full of fire, and that from there down he looked like fire; and brilliant light surrounded him.")],
     [("H3519", "Kavod (Glory)"), ("H2122", "Ziw (Brightness/Radiance)"), ("H8416", "Tehillah (Praise)")]),

    (2119, "זָחַל", "Zachal", "Verb", "To Crawl; To Shrink Back; To Withdraw in Fear",
     "To crawl or wriggle like a snake; to shrink away in dread or reverence.",
     "The Hebrew <em>zachal</em> (H2119) describes a crawling, creeping motion — like a serpent or worm — and by extension, the shrinking back of the spirit in terror or awe. In Deuteronomy 32:24, the text describes serpents crawling through the dust among the judgment of God. In Micah 7:17, the nations will 'crawl' from their strongholds in terror before the God of Israel. The word pictures humiliation and awe before overwhelming power.",
     "The imagery of <em>zachal</em> in Micah 7:17 is a vision of eschatological reversal: the nations who once oppressed Israel will come crawling out of their fortresses like terrified serpents, trembling before the LORD. This is connected to the prophetic vision of all nations acknowledging God's sovereignty (Zechariah 14:16-17). The same God before whom the nations must <em>zachal</em> is the God who is 'a pardoning God' to his people (Micah 7:18). Terrifying majesty and tender mercy dwell together in the same God.",
     [("Micah 7:17", "They will lick dust like a snake, like creatures that <em>crawl</em> on the ground. They will come trembling out of their dens; they will turn in fear to the LORD our God."),
      ("Deuteronomy 32:24", "I will send against them the fangs of wild beasts, the venom of vipers that glide in the dust (<em>zachal</em>)."),
      ("Isaiah 2:10", "Go into the rocks, hide in the ground from the fearful presence of the LORD and the splendor of his majesty!"),
      ("Psalm 72:9", "May the desert tribes bow before him and his enemies lick the dust."),
      ("Revelation 6:15", "Then the kings of the earth, the princes, the generals, the rich, the mighty, and everyone else, both slave and free, hid in caves and among the rocks of the mountains.")],
     [("H2119", "Zachal (Crawl)"), ("H3372", "Yare (Fear)"), ("H7812", "Shachah (Bow Down)")]),

    (2132, "זַיִת", "Zayit", "Noun, masculine", "Olive Tree; Olive",
     "The olive tree — deeply symbolic of peace, prosperity, anointing, and divine blessing.",
     "The Hebrew <em>zayit</em> (H2132) is the olive tree, one of the most important trees in the ancient Near East and a dominant biblical symbol. The olive branch brought back by Noah's dove (Genesis 8:11) signified the end of judgment and the return of peace. The olive tree produces oil used for anointing kings and priests, fueling the lampstand in the tabernacle, and providing food. In Zechariah 4, two olive trees flank the golden lampstand — representing the two anointed ones who supply oil to the lampstand of God.",
     "The olive tree in Scripture encompasses a rich symbolic world: peace (the dove's olive branch), anointing (oil for priests and kings), light (lamp oil), prosperity (olive as a sign of divine blessing — Deuteronomy 8:8), and covenant continuity. Paul uses the olive tree as his master metaphor for the covenant people of God in Romans 11 — Israel is the cultivated olive tree into which Gentile branches are grafted. The warning that God can graft branches back and cut others off is one of the most sobering passages in Romans, calling for humility before God's sovereign purposes.",
     [("Genesis 8:11", "When the dove returned to him in the evening, there in its beak was a freshly plucked <em>olive</em> leaf! Then Noah knew that the water had receded."),
      ("Zechariah 4:3", "Also there are two <em>olive trees</em> by it, one on the right of the bowl and the other on its left."),
      ("Romans 11:17", "If some of the branches have been broken off, and you, though a wild olive shoot, have been grafted in among the others and now share in the nourishing sap from the olive root."),
      ("Deuteronomy 8:8", "A land with wheat and barley, vines and fig trees, pomegranates, <em>olive oil</em> and honey."),
      ("Psalm 52:8", "But I am like a flourishing <em>olive tree</em> in the house of God; I trust in God's unfailing love for ever and ever.")],
     [("H8081", "Shemen (Oil)"), ("H4899", "Mashiach (Anointed One)"), ("H3974", "Maor (Light)")]),

    (2134, "זַךְ", "Zakh", "Adjective", "Pure; Clean; Innocent; Transparent",
     "Morally pure, clean, or innocent — used of transparent, unmixed purity.",
     "The Hebrew <em>zakh</em> (H2134) means pure, clean, or innocent — especially in a transparent, unmixed sense. Job uses it to declare his own innocence: 'My prayer is pure (<em>zakh</em>)' (Job 16:17). In Proverbs 20:11, 'Even small children are known by their actions, so is their conduct really pure (<em>zakh</em>) and upright?' The word carries the sense of something unmixed, like clear water or transparent light.",
     "<em>Zakh</em> appears in Job's extended legal argument before God, where he insists on his innocence despite his suffering. The word is related to <em>zakah</em> (to be clean/pure) and <em>zakok</em> (transparent). Theologically, true purity before God is not achieved by human effort but is the result of divine cleansing and imputed righteousness. The NT echo is 'Blessed are the pure in heart' (Matthew 5:8) — those whose inner life is single, unmixed, and transparent before God, they alone see Him.",
     [("Job 16:17", "Yet my hands have been free from violence and my prayer is <em>pure</em>."),
      ("Proverbs 20:11", "Even small children are known by their actions, so is their conduct really <em>pure</em> and upright?"),
      ("Job 8:6", "If you are <em>pure</em> and upright, even now he will rouse himself on your behalf."),
      ("Matthew 5:8", "Blessed are the pure in heart, for they will see God."),
      ("Psalm 24:4", "The one who has clean hands and a pure heart, who does not trust in an idol or swear by a false god.")],
     [("H2889", "Tahor (Pure/Clean)"), ("H5355", "Naqi (Innocent)"), ("H6662", "Tsaddiq (Righteous)")]),

    (2146, "זִכְרוֹן", "Zikkaron", "Noun, masculine", "Memorial; Remembrance; Record",
     "A memorial, record, or reminder — something kept to preserve memory before God or men.",
     "The Hebrew <em>zikkaron</em> (H2146) is the noun form of <em>zakar</em> (to remember) and means a memorial, written record, or act of remembrance. The Passover is commanded as a <em>zikkaron</em> (Exodus 12:14): 'This is a day you are to commemorate; for the generations to come you shall celebrate it.' The twelve stones at Gilgal (Joshua 4:7) served as a <em>zikkaron</em>. The book of Malachi speaks of a <em>zikkaron</em> scroll of those who fear the LORD (Malachi 3:16).",
     "The concept of <em>zikkaron</em> reveals that remembrance in the Bible is not merely mental recollection but active re-engagement with saving events. The Passover Seder, the stones at Gilgal, the Lord's Supper — all are <em>zikkaronim</em>: physical anchors that call the people back into covenant reality. Most stunning is the scroll of remembrance in Malachi 3:16 — God Himself keeps a memorial record of those who fear Him. To be remembered by God is the highest security; to forget God is the deepest danger.",
     [("Exodus 12:14", "This is a day you are to commemorate (<em>zikkaron</em>); for the generations to come you shall celebrate it as a festival to the LORD."),
      ("Malachi 3:16", "Then those who feared the LORD talked with each other, and the LORD listened and heard. A scroll of <em>remembrance</em> was written in his presence."),
      ("Joshua 4:7", "These stones are to be a <em>memorial</em> to the people of Israel forever."),
      ("Esther 6:1", "That night the king could not sleep; so he ordered the book of the chronicles, the record of his reign, to be brought in."),
      ("Luke 22:19", "And he took bread, gave thanks and broke it, and gave it to them, saying, 'This is my body given for you; do this in <em>remembrance</em> of me.'")],
     [("H2142", "Zakar (Remember)"), ("H5715", "Eduth (Testimony)"), ("H6862", "Tsur (Rock/Refuge)")]),

    (2156, "זְמוֹרָה", "Zemorah", "Noun, feminine", "Branch; Vine Shoot; Tendril",
     "A branch, shoot, or tendril of a vine — used literally and as imagery of Israel.",
     "The Hebrew <em>zemorah</em> (H2156) is a branch or shoot, particularly of a vine. In Numbers 13:23, the spies cut a branch (<em>zemorah</em>) with a cluster of grapes from Eshcol. Ezekiel uses the vine branch extensively as metaphor for Israel and its leaders. In Ezekiel 15:2-4, the wood of the vine branch (<em>zemorah</em>) is useless for anything except burning — a powerful indictment of Jerusalem's unfaithfulness. In John 15, Jesus takes this imagery to its fulfillment: He is the true vine.",
     "<em>Zemorah</em> imagery establishes the vine-and-branches motif foundational to John 15. Israel was called to be God's vineyard (Isaiah 5), but the branches repeatedly failed to bear fruit. Ezekiel's use of <em>zemorah</em> as a judgment image — the branch is good only for fire if it bears no fruit — finds its echo in Jesus' warning that unfruitful branches are gathered and burned (John 15:6). Yet for those who abide in the True Vine, the promise is abundance: 'much fruit' that glorifies the Father (John 15:8).",
     [("Numbers 13:23", "When they reached the Valley of Eshkol, they cut off a <em>branch</em> bearing a single cluster of grapes."),
      ("Ezekiel 15:2", "Son of man, how is the wood of a vine different from that of a <em>branch</em> from any of the trees in the forest?"),
      ("John 15:5", "I am the vine; you are the branches. If you remain in me and I in you, you will bear much fruit."),
      ("Isaiah 5:2", "He dug it up and cleared it of stones and planted it with the choicest vines."),
      ("Psalm 80:11", "Its <em>branches</em> reached as far as the Sea, its shoots as far as the River.")],
     [("H1612", "Gephen (Vine)"), ("H6529", "Peri (Fruit)"), ("H5342", "Netser (Branch/Shoot)")]),

    (2162, "זָמָם", "Zamam", "Verb", "To Plan; To Plot; To Purpose; To Devise",
     "To devise a plan or scheme — used of both evil plotting and God's sovereign purposes.",
     "The Hebrew <em>zamam</em> (H2162) means to plan, devise, or purpose — it is used of both wicked scheming and God's sovereign determination. In Zechariah 8:14-15, God uses <em>zamam</em> for both: 'Just as I had determined (<em>zamam</em>) to bring disaster upon you... so now I have determined (<em>zamam</em>) to do good again to Jerusalem.' The word captures intentional, premeditated action — what one has firmly decided to do.",
     "The theological contrast in Zechariah 8 is remarkable: the same verb (<em>zamam</em>) describes God's prior purpose to judge and His present purpose to bless. This emphasizes that both judgment and restoration are equally deliberate acts of God — neither accidental, neither arbitrary. In Proverbs 30:32, <em>zamam</em> warns against prideful planning. The psalm of reversal (Psalm 37:12) shows the wicked plotting (<em>zamam</em>) against the righteous — but God laughs, for He sees their doom. Divine <em>zamam</em> overrules human <em>zamam</em> every time.",
     [("Zechariah 8:15", "So now I have determined (<em>zamam</em>) to do good again to Jerusalem and Judah. Do not be afraid."),
      ("Psalm 37:12", "The wicked plot (<em>zamam</em>) against the righteous and gnash their teeth at them."),
      ("Zechariah 8:14", "This is what the LORD Almighty says: 'Just as I had determined to bring disaster upon you when your ancestors angered me... and I did not relent.'"),
      ("Proverbs 30:32", "If you play the fool and exalt yourself, or if you plan evil, clap your hand over your mouth!"),
      ("Jeremiah 51:12", "The LORD has both planned and done what he said regarding the inhabitants of Babylon.")],
     [("H6098", "Etsah (Counsel/Plan)"), ("H2803", "Chashab (Devise/Plan)"), ("H3289", "Yaats (Counsel)")]),

    (2166, "זְמַן", "Zeman", "Noun, masculine (Aramaic)", "Time; Appointed Time; Season",
     "An appointed time or season — Aramaic term used especially in Daniel.",
     "The Aramaic <em>zeman</em> (H2166) is related to the Hebrew <em>zaman</em> and means an appointed time, set season, or specific moment. It appears predominantly in Daniel, where it carries enormous theological weight. In Daniel 2:21, 'He changes times and seasons (<em>zemanim</em>)' — declaring God's absolute sovereignty over history. In Daniel 7:25, the Antichrist figure attempts to 'change the set times and the laws' (<em>zemanim</em>) — a direct assault on divine order.",
     "The <em>zeman</em> passages in Daniel establish a theological axiom: God is the sovereign Lord of time itself. He sets the times and removes kings (Daniel 2:21). History has a telos — an appointed end — that no human or demonic power can ultimately derail. The eschatological significance is profound: when Daniel sees the 'time, times and half a time' in Daniel 7:25 and 12:7, he understands that even the period of tribulation has a divinely appointed limit. God's <em>zeman</em> brackets all human history, from creation to new creation.",
     [("Daniel 2:21", "He changes times and seasons (<em>zemanim</em>); he deposes kings and raises up others."),
      ("Daniel 7:25", "He will speak against the Most High and oppress his holy people and try to change the set times (<em>zemanim</em>) and the laws."),
      ("Daniel 3:7", "Therefore, as soon as they heard the sound... all the nations and peoples of every language fell down and worshiped the image."),
      ("Acts 1:7", "He said to them: 'It is not for you to know the times or dates the Father has set by his own authority.'"),
      ("Ecclesiastes 3:1", "There is a time for everything, and a season for every activity under the heavens.")],
     [("H6256", "Et (Time/Season)"), ("H4150", "Moed (Appointed Time)"), ("H5769", "Olam (Eternity)")]),

    (2184, "זְנוּת", "Zenut", "Noun, feminine", "Fornication; Harlotry; Spiritual Adultery",
     "Sexual immorality; harlotry — especially Israel's spiritual unfaithfulness to God.",
     "The Hebrew <em>zenut</em> (H2184) is the abstract noun from <em>zanah</em> (to commit fornication/play the harlot). It describes sexual immorality but more often, in the prophets, Israel's spiritual adultery — abandoning covenant loyalty to God for the pursuit of idols. In Ezekiel 23, both Samaria and Jerusalem are condemned for their <em>zenut</em> — the spiritual prostitution of covenant-breaking. Hosea's entire prophetic ministry was built on this metaphor.",
     "The prophets, especially Hosea, Jeremiah, and Ezekiel, develop <em>zenut</em> as the primary metaphor for apostasy. The covenant between God and Israel was marriage-like in its exclusivity and intimacy (cf. Hosea 2). Any turning to other gods was therefore adultery — a <em>zenut</em> that broke the covenant bond. This prophetic tradition is why Revelation speaks of 'Babylon the Great, the mother of prostitutes' (<em>porneion</em> — Rev 17:5): it represents the anti-covenant world system that seduces the people of God away from their true Husband.",
     [("Ezekiel 23:8", "She did not give up the prostitution (<em>zenut</em>) she began in Egypt, when during her youth men slept with her."),
      ("Hosea 1:2", "Go, marry a promiscuous woman and have children with her, for like an adulterous wife this land is guilty of unfaithfulness to the LORD."),
      ("Numbers 14:33", "Your children will be shepherds here for forty years, suffering for your unfaithfulness (<em>zenut</em>), until the last of your bodies lies in the wilderness."),
      ("Jeremiah 3:2", "Look up to the barren heights and see. Is there any place where you have not been ravished? By the roadside you sat waiting for lovers, sat like a nomad in the desert."),
      ("Revelation 17:5", "The name written on her forehead was a mystery: BABYLON THE GREAT THE MOTHER OF PROSTITUTES AND OF THE ABOMINATIONS OF THE EARTH.")],
     [("H2181", "Zanah (Play the Harlot)"), ("H5003", "Naaf (Commit Adultery)"), ("H2617", "Chesed (Steadfast Love)")]),

    (2187, "זָנַק", "Zanaq", "Verb", "To Spring; To Leap; To Bound",
     "To spring or leap forward with energy and sudden force.",
     "The Hebrew <em>zanaq</em> (H2187) means to spring, leap, or bound — the swift, powerful forward motion of an animal or person launching themselves. It appears in Deuteronomy 33:22, in the blessing of Dan: 'Dan is a lion's cub, springing (<em>zanaq</em>) out of Bashan.' The image is of a young lion launching itself from its crouching position in swift, unexpected attack. The word captures explosive, sudden force.",
     "<em>Zanaq</em> in the blessing of Dan presents the tribe as fierce and swift in battle — a quality God can use for His purposes. The NT parallel is found in descriptions of the Spirit's sudden empowerment (Acts 2:2: 'suddenly a sound like the blowing of a violent wind'). The image of the leaping lion also anticipates the Lion of Judah (Revelation 5:5), who springs upon His enemies in ultimate victory. There is a divine ferocity in God's redemptive action — sudden, powerful, and irresistible.",
     [("Deuteronomy 33:22", "About Dan he said: 'Dan is a lion's cub, <em>springing</em> out of Bashan.'"),
      ("Proverbs 30:19", "The way of an eagle in the sky, the way of a snake on a rock, the way of a ship on the high seas, and the way of a man with a young woman."),
      ("Joel 3:16", "The LORD will roar from Zion and thunder from Jerusalem; the earth and the heavens will tremble."),
      ("Revelation 5:5", "See, the Lion of the tribe of Judah, the Root of David, has triumphed."),
      ("Nahum 2:12", "The lion killed enough for his cubs and strangled the prey for his mate.")],
     [("H738", "Ari (Lion)"), ("H1070", "Gur (Young Lion/Cub)"), ("H2388", "Chazaq (Be Strong)")]),

    (5008, "נְאָקָה", "Neaqah", "Noun, feminine", "Groaning; Sighing; Moaning",
     "A groan or sigh — especially the anguished cry of the oppressed that reaches God.",
     "The Hebrew <em>neaqah</em> (H5008) is a deep groan or sigh — the inarticulate cry of someone under unbearable affliction. In Exodus 2:24, God heard the <em>neaqah</em> (groaning) of the Israelites enslaved in Egypt: 'God heard their groaning and he remembered his covenant with Abraham, with Isaac and with Jacob.' The word captures the kind of suffering that cannot be put into words — the moan that rises from the depths of human misery.",
     "<em>Neaqah</em> is one of the most powerful words in the theology of prayer and lament. It teaches that God receives groaning — not just articulate petition — as genuine prayer. The enslaved Israelites did not compose a formal prayer; they simply groaned, and God heard. This is the basis for Paul's statement in Romans 8:26: 'The Spirit himself intercedes for us through wordless groans (<em>stenagmois alalētois</em>).' When the believer is too broken to pray in words, the Spirit carries their <em>neaqah</em> directly to the throne of God.",
     [("Exodus 2:24", "God heard their <em>groaning</em> and he remembered his covenant with Abraham, with Isaac and with Jacob."),
      ("Psalm 102:20", "To hear the <em>groans</em> of the prisoners and release those condemned to death."),
      ("Romans 8:26", "The Spirit himself intercedes for us through wordless <em>groans</em>."),
      ("Ezekiel 30:24", "I will strengthen the arms of the king of Babylon and put my sword in his hand, but I will break the arms of Pharaoh, and he will <em>groan</em> before him like a mortally wounded man."),
      ("Lamentations 1:22", "Let all their wickedness come before you; deal with them as you have dealt with me because of all my transgressions. My <em>sighs</em> are many and my heart is faint.")],
     [("H6818", "Tsaaqah (Cry/Outcry)"), ("H7775", "Shavah (Cry for Help)"), ("H7356", "Rachamim (Compassion)")]),

    (5016, "נְבוּאָה", "Nebuah", "Noun, feminine", "Prophecy; Prophetic Utterance",
     "A prophetic word or utterance — the spoken or written message from God's prophet.",
     "The Hebrew <em>nebuah</em> (H5016) is the noun form of <em>naba</em> (to prophesy) and means the prophetic word itself — the utterance, message, or writing of a prophet. In 2 Chronicles 15:8, Asa took courage when he heard the <em>nebuah</em> (prophecy) of Azariah. The term points to the divine word mediated through the human prophet — a message that carries God's authority because it originates with Him.",
     "The concept of <em>nebuah</em> is central to biblical epistemology: humanity knows God's will because God speaks through prophets. The prophetic office was God's primary instrument of revelation throughout the OT period (Hebrews 1:1: 'at many times and in various ways, God spoke to our ancestors through the prophets'). The NT fulfillment is Christ Himself — the final and definitive Word (Hebrews 1:2). Yet prophecy continues in the church (1 Corinthians 12:10, 14:1) as a gift of the Spirit for building up the body in truth.",
     [("2 Chronicles 15:8", "When Asa heard these words and the <em>prophecy</em> of Azariah son of Oded the prophet, he took courage."),
      ("Nehemiah 6:12", "I realized that God had not sent him, but that he had prophesied against me because Tobiah and Sanballat had hired him."),
      ("2 Peter 1:20", "Above all, you must understand that no prophecy of Scripture came about by the prophet's own interpretation of things."),
      ("1 Corinthians 14:3", "But the one who prophesies speaks to people for their strengthening, encouraging and comfort."),
      ("Revelation 22:19", "And if anyone takes words away from this scroll of <em>prophecy</em>, God will take away from that person any share in the tree of life.")],
     [("H5012", "Naba (Prophesy)"), ("H5030", "Navi (Prophet)"), ("H2377", "Chazon (Vision)")]),

    (5034, "נָבֵל", "Navel", "Verb", "To Wither; To Fade; To Dishonor; To Be Foolish",
     "To wither and fall away like a dying leaf; to disgrace or treat as worthless.",
     "The Hebrew <em>navel</em> (H5034) carries two intertwined meanings: to wither/fade (like a plant dying) and to dishonor/treat as vile (to nabal — treat with contempt). Isaiah 1:30 uses it of withering leaves: 'You will be like an oak with fading leaves, like a garden without water.' Isaiah 64:6 declares: 'All of us have become like one who is unclean... we all <em>shrivel up</em> like a leaf.' The connection between fading and foolishness is rooted in the same root as <em>nabal</em> (fool).",
     "The theological depth of <em>navel</em> lies in its double meaning. Physical withering and moral foolishness/disgrace are linguistically linked in Hebrew thought. The fool (<em>nabal</em>, like Nabal in 1 Samuel 25) is the one who has withered spiritually — who has lost the sap of covenant relationship with God. Isaiah 40:7-8 contrasts this: 'The grass withers and the flowers fall... but the word of our God endures forever.' Human glory is <em>navel</em> — it fades. God's word is the only thing that does not wither.",
     [("Isaiah 64:6", "All of us have become like one who is unclean, and all our righteous acts are like filthy rags; we all <em>shrivel up</em> like a leaf, and like the wind our sins sweep us away."),
      ("Isaiah 1:30", "You will be like an oak with <em>fading</em> leaves, like a garden without water."),
      ("Isaiah 40:7", "The grass <em>withers</em> and the flowers fall, because the breath of the LORD blows on them."),
      ("1 Peter 1:24", "All people are like grass, and all their glory is like the flowers of the field; the grass <em>withers</em> and the flowers fall."),
      ("Psalm 37:2", "For like the grass they will soon <em>wither</em>, like green plants they will soon die away.")],
     [("H5036", "Nabal (Fool)"), ("H3001", "Yavesh (Dry Up/Wither)"), ("H1697", "Davar (Word)")]),

    (5059, "נָגַן", "Nagan", "Verb", "To Play a Stringed Instrument; To Make Music",
     "To play on a stringed instrument — the making of music as worship and prophetic act.",
     "The Hebrew <em>nagan</em> (H5059) means to play a stringed instrument, particularly the harp or lyre. In 1 Samuel 16:16-23, David is called to play (<em>nagan</em>) before Saul, and his playing brought relief from the tormenting spirit. In 2 Kings 3:15, Elisha called for a harpist, and 'while the harpist was playing, the hand of the LORD came on Elisha.' Music is not merely entertainment in Scripture — it is a vehicle for the Spirit.",
     "The theology of <em>nagan</em> reveals that music is spiritually potent: it can provide relief from oppression (David before Saul) and create the conditions for prophetic activity (Elisha and the harpist). The Psalms, which were sung to instruments, were Israel's primary vehicle of corporate worship. The NT vision of heaven is saturated with music (Revelation 5:8 — 'golden harps'; Revelation 15:2 — those who had harps). Music is not decorative in worship but structural — it carries spiritual weight and opens the human spirit to divine encounter.",
     [("1 Samuel 16:23", "Whenever the spirit from God came on Saul, David would take up his lyre and <em>play</em>. Then relief would come to Saul."),
      ("2 Kings 3:15", "But now bring me a harpist. While the harpist was <em>playing</em>, the hand of the LORD came on Elisha."),
      ("Psalm 33:3", "Sing to him a new song; <em>play</em> skillfully, and shout for joy."),
      ("Psalm 68:25", "In front are the singers, after them the <em>musicians</em>; with them are the young women playing the timbrels."),
      ("Revelation 5:8", "And when he had taken it, the four living creatures and the twenty-four elders fell down before the Lamb. Each one had a harp.")],
     [("H5035", "Nebel (Harp/Lyre)"), ("H7892", "Shir (Song)"), ("H8416", "Tehillah (Praise)")]),

    (5065, "נָגַשׂ", "Nagas", "Verb", "To Drive; To Press; To Oppress; To Exact",
     "To press hard upon; to drive or exact labor from; to oppress or be a taskmaster.",
     "The Hebrew <em>nagas</em> (H5065) means to press, drive, or oppress — to bear down hard on another person, especially as a slave driver or oppressor. In Exodus 3:7, God sees how the Egyptians have 'oppressed' (<em>nagas</em>) His people. Isaiah 53:7 uses it of the Suffering Servant: 'He was oppressed (<em>nagas</em>) and afflicted, yet he did not open his mouth.' The word conveys relentless, grinding pressure applied to the powerless.",
     "Isaiah 53:7 is the theological apex of <em>nagas</em>: the One who had come to free the oppressed became Himself the oppressed. The Servant of Isaiah 53 takes on the role of the enslaved, beaten, and silenced — the very condition God had come to relieve in Exodus. This inversion — the Liberator becoming the slave — is the heart of substitutionary atonement. Because He bore the <em>nagas</em> of sin and judgment, those who were crushed under sin's weight can be set free (Isaiah 61:1: 'to proclaim freedom for the captives').",
     [("Isaiah 53:7", "He was <em>oppressed</em> and afflicted, yet he did not open his mouth; he was led like a lamb to the slaughter."),
      ("Exodus 3:7", "The LORD said, 'I have indeed seen the misery of my people in Egypt. I have heard them crying out because of their slave drivers (<em>nagas</em>).'"),
      ("Isaiah 58:3", "'Why have we fasted,' they say, 'and you have not seen it? Why have we humbled ourselves, and you have not noticed?' Yet on the day of your fasting, you do as you please and exploit all your workers (<em>nagas</em>)."),
      ("Zechariah 9:8", "But I will encamp at my temple to guard it against marauding forces. Never again will an <em>oppressor</em> overrun my people."),
      ("Isaiah 60:17", "I will make peace your governor and well-being your ruler. No longer will violence be heard in your land, nor ruin or destruction within your borders.")],
     [("H6231", "Ashaq (Oppress)"), ("H2541", "Chamuts (Oppressed)"), ("H6304", "Peduth (Redemption)")]),

    (5066, "נָגַשׁ", "Nagash", "Verb", "To Draw Near; To Approach; To Come Close",
     "To draw near or approach — especially coming close to God, an altar, or a person.",
     "The Hebrew <em>nagash</em> (H5066) means to draw near or approach — it is used of people approaching God (Exodus 24:2), priests approaching the altar (Ezekiel 44:13), and enemies drawing near in battle. The word is particularly significant in the context of covenant access: who may draw near to God, under what conditions, and with what preparation? In Isaiah 45:20, the exiles are commanded: 'Gather together and come (<em>nagash</em>).'",
     "The theology of <em>nagash</em> is fundamentally about access. In the tabernacle/temple system, who could <em>nagash</em> to God was strictly defined by priestly law — the wrong approach meant death (Leviticus 10:1-2). The Messiah would be called to <em>nagash</em> to God in a unique, unprecedented way (Jeremiah 30:21: 'Who is he who will devote himself to be close to me?'). The NT answer is Jesus, our Great High Priest (Hebrews 4:16: 'Let us therefore come boldly to the throne of grace') — He has opened the way for all believers to <em>nagash</em> freely.",
     [("Exodus 24:2", "But Moses alone is to approach (<em>nagash</em>) the LORD; the others must not come near."),
      ("Hebrews 4:16", "Let us therefore approach (<em>nagash</em>) the throne of grace with confidence."),
      ("Isaiah 45:20", "'Gather together and come (<em>nagash</em>); assemble, you fugitives from the nations.'"),
      ("Jeremiah 30:21", "Their leader will be one of their own; their ruler will arise from among them. I will bring him near and he will come close to me — for who is he who will devote himself to be close to me?"),
      ("James 4:8", "Come near to God and he will come near to you.")],
     [("H7126", "Qarav (Draw Near)"), ("H935", "Bo (Come/Enter)"), ("H6440", "Panim (Face/Presence)")]),

    (5079, "נִדָּה", "Niddah", "Noun, feminine", "Impurity; Separation; Menstrual Uncleanness",
     "Ritual impurity — especially menstrual uncleanness, and metaphorically, moral defilement.",
     "The Hebrew <em>niddah</em> (H5079) refers to the state of separation or impurity, particularly associated with menstrual blood (Leviticus 15:19-33) but extended to other forms of severe ritual uncleanness and, metaphorically, moral corruption. Ezekiel 36:17 uses <em>niddah</em> for Israel's moral defilement: 'their conduct was like a woman's <em>uncleanness</em> in my sight.' Numbers 19:9 uses 'water of <em>niddah</em>' for the purification water made from the red heifer — the ritual for removing the most severe uncleanness.",
     "The <em>niddah</em> regulations in Leviticus establish a ritual world where physical bodily states reflect spiritual realities. Uncleanness is not sin but a symbol of the human condition before God — we are 'by nature deserving of wrath' (Ephesians 2:3). The water of purification (Numbers 19) involving the ashes of a red heifer is perhaps the most elaborate purification ritual in the OT, and the author of Hebrews uses it as the platform for declaring Christ's blood 'how much more' effective: 'how much more will the blood of Christ... cleanse our consciences from acts that lead to death' (Hebrews 9:13-14).",
     [("Leviticus 15:19", "When a woman has her regular flow of blood, the <em>impurity</em> of her monthly period will last seven days."),
      ("Ezekiel 36:17", "Son of man, when the people of Israel were living in their own land, they defiled it by their conduct and their actions. Their conduct was like a woman's <em>uncleanness</em> in my sight."),
      ("Numbers 19:9", "A man who is clean shall gather up the ashes of the heifer and put them in a ceremonially clean place outside the camp. They are to be kept by the Israelite community for use in the water of cleansing (<em>niddah</em>)."),
      ("Hebrews 9:13", "The blood of goats and bulls and the ashes of a heifer sprinkled on those who are ceremonially unclean sanctify them so that they are outwardly clean."),
      ("Zechariah 13:1", "On that day a fountain will be opened to the house of David and the inhabitants of Jerusalem, to cleanse them from sin and <em>impurity</em>.")],
     [("H2931", "Tame (Unclean)"), ("H2891", "Taher (Be Clean)"), ("H3722", "Kaphar (Atone)")]),

    (5080, "נָדַח", "Nadach", "Verb", "To Drive Away; To Thrust Out; To Be Scattered",
     "To drive or thrust away — used of exile, scattering of the outcast, and God's gathering.",
     "The Hebrew <em>nadach</em> (H5080) means to drive away, thrust out, or scatter — it is frequently used in the context of Israel's exile and the scattering of the people among the nations. Deuteronomy 30:4 gives the foundational promise: 'Even if you have been banished (<em>nadach</em>) to the most distant land under the heavens, from there the LORD your God will gather you and bring you back.' The same word used for exile becomes the setting for the promise of divine restoration.",
     "<em>Nadach</em> passages establish one of the Bible's most powerful reversals: those who have been driven out by human and demonic forces will be gathered in by God. Isaiah 11:12 promises that God will 'gather the exiles of Israel; he will assemble the scattered people of Judah from the four quarters of the earth.' This theme reaches its NT apex in John 11:52, where John interprets Christ's death as 'to gather together in one the scattered children of God.' The cross is the ultimate act of gathering the <em>nadach</em> — the driven-out ones — back to the Father.",
     [("Deuteronomy 30:4", "Even if you have been banished (<em>nadach</em>) to the most distant land under the heavens, from there the LORD your God will gather you and bring you back."),
      ("John 11:52", "And not only for that nation but also for the scattered children of God, to bring them together and make them one."),
      ("Jeremiah 23:3", "'I myself will gather the remnant of my flock out of all the countries where I have <em>driven</em> them.'"),
      ("Ezekiel 34:16", "I will search for the lost and bring back the strays. I will bind up the injured and strengthen the weak."),
      ("Isaiah 11:12", "He will raise a banner for the nations and gather the exiles of Israel; he will assemble the scattered people of Judah.")],
     [("H6327", "Puts (Scatter)"), ("H6908", "Qavats (Gather)"), ("H7725", "Shuv (Return)")]),

    (5081, "נָדִיב", "Nadiv", "Noun/Adjective, masculine", "Noble; Generous; Willing Heart",
     "A noble or generous person — one whose spirit is free and willing to give.",
     "The Hebrew <em>nadiv</em> (H5081) describes a person of nobility, generosity, and free-spirited willingness. It comes from <em>nadav</em> (to volunteer, to give freely) and describes both social nobility (a prince or leader) and moral generosity. In Exodus 35:5, Moses calls for 'everyone who is willing' (<em>nediv lev</em> — a generous heart) to bring an offering for the tabernacle. Psalm 51:12 prays: 'Grant me a willing (<em>nedivah</em>) spirit, to sustain me.'",
     "The <em>nadiv</em> is the opposite of the niggardly, the calculating, and the self-preserving. In Proverbs 17:26, 'it is not good to punish an innocent man, or to flog officials (<em>nedivim</em>) for their integrity' — nobility of spirit is worth protecting. The tabernacle and temple were built by <em>nediv lev</em> — willing-hearted givers (Exodus 35, 1 Chronicles 29:9). This becomes the pattern for NT generosity: 'Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver' (2 Corinthians 9:7).",
     [("Psalm 51:12", "Restore to me the joy of your salvation and grant me a willing (<em>nedivah</em>) spirit, to sustain me."),
      ("Exodus 35:5", "From what you have, take an offering for the LORD. Everyone who is willing (<em>nediv lev</em>), let them bring an offering to the LORD."),
      ("Isaiah 32:8", "But the noble (<em>nadiv</em>) make noble plans, and by noble deeds they stand."),
      ("2 Corinthians 9:7", "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver."),
      ("1 Chronicles 29:9", "The people rejoiced at the willing response of their leaders, for they had given freely and wholeheartedly to the LORD.")],
     [("H5068", "Nadav (Volunteer/Give Freely)"), ("H2617", "Chesed (Lovingkindness)"), ("H3068", "YHWH (LORD)")]),

    (5087, "נָדַר", "Nadar", "Verb", "To Vow; To Make a Solemn Promise to God",
     "To make a vow or solemn pledge to God — binding oneself by sacred promise.",
     "The Hebrew <em>nadar</em> (H5087) means to make a vow — a solemn, sacred pledge to God, typically conditional ('if you do this, I will do that') or dedicatory. Jacob vowed at Bethel (Genesis 28:20-22); Hannah vowed if God gave her a son (1 Samuel 1:11); Jephthah made a rash vow (Judges 11:30-31). Numbers 30:2 establishes the principle: 'When a man makes a vow (<em>nadar</em>) to the LORD or takes an oath to obligate himself by a pledge, he must not break his word.'",
     "The theology of <em>nadar</em> is about the weight of words before God. Ecclesiastes 5:4-5 warns: 'When you make a vow to God, do not delay to fulfill it... It is better not to make a vow than to make one and not fulfill it.' The NT does not abolish vowing (Paul takes a vow in Acts 18:18) but elevates the standard: Jesus teaches that all speech should carry the gravity of a vow — All you need to say is simply Yes or No (Matthew 5:37). The highest vow in Scripture is God's own oath, which grounds the new covenant in absolute certainty (Hebrews 6:17-18).",
     [("Numbers 30:2", "When a man makes a vow (<em>nadar</em>) to the LORD or takes an oath to obligate himself by a pledge, he must not break his word."),
      ("Psalm 116:14", "I will fulfill my vows (<em>nedarim</em>) to the LORD in the presence of all his people."),
      ("Ecclesiastes 5:4", "When you make a vow to God, do not delay to fulfill it. He has no pleasure in fools; fulfill your vow."),
      ("Jonah 2:9", "But I, with shouts of grateful praise, will sacrifice to you. What I have vowed I will make good. I will say, 'Salvation comes from the LORD.'"),
      ("Hebrews 6:17", "Because God wanted to make the unchanging nature of his purpose very clear to the heirs of what was promised, he confirmed it with an oath.")],
     [("H5088", "Neder (Vow)"), ("H7621", "Shebuah (Oath)"), ("H1285", "Berit (Covenant)")]),

    (5088, "נֶדֶר", "Neder", "Noun, masculine", "Vow; Pledge; Sacred Promise",
     "A vow or sacred pledge made to God — the object or content of a solemn promise.",
     "The Hebrew <em>neder</em> (H5088) is the noun for a vow — the vow itself as a sacred obligation made to God. The Psalms frequently celebrate the fulfillment of vows in the congregation: 'I will fulfill my vows (<em>nedarim</em>) to the LORD in the presence of all his people' (Psalm 116:14, 18). Numbers 15 and 30 provide extensive legislation on <em>nedarim</em>, regulating when vows must be kept and when they may be released. Proverbs 20:25 warns against making rash vows.",
     "<em>Neder</em> in the Psalms is consistently fulfilled publicly, in the assembly (Psalms 22:25, 50:14, 61:8, 116:14). This communal dimension is significant: the vow is not just between the individual and God but is witnessed by the congregation, binding the community to God's faithfulness and the individual's response. The NT church's public confession — baptism, the Lord's Supper, ordination — carries something of the weight of <em>neder</em>: public pledges that bind the community to their Lord and to one another.",
     [("Psalm 116:14", "I will fulfill my vows (<em>nedarim</em>) to the LORD in the presence of all his people."),
      ("Psalm 22:25", "From you comes the theme of my praise in the great assembly; before those who fear you I will fulfill my <em>vows</em>."),
      ("Numbers 30:2", "When a man makes a vow to the LORD or takes an oath to obligate himself by a pledge, he must not break his word."),
      ("Proverbs 20:25", "It is a trap to dedicate something rashly and only later to consider one's <em>vows</em>."),
      ("Jonah 1:16", "At this the men greatly feared the LORD, and they offered a sacrifice to the LORD and made <em>vows</em> to him.")],
     [("H5087", "Nadar (To Vow)"), ("H7621", "Shebuah (Oath)"), ("H2077", "Zebach (Sacrifice)")]),

    (5095, "נָהַל", "Nahal", "Verb", "To Lead; To Guide to Rest; To Shepherd",
     "To lead carefully to a resting place — to shepherd or guide with tender provision.",
     "The Hebrew <em>nahal</em> (H5095) means to lead or guide to a place of rest and refreshment — it carries the sense of tender, careful shepherding. In Psalm 23:2, 'he leads me beside quiet waters' uses a related concept; the verb itself appears in Isaiah 40:11: 'He tends his flock like a shepherd: He gathers the lambs in his arms and carries them close to his heart; he gently <em>leads</em> (<em>nahal</em>) those that have young.' In Exodus 15:13, God 'guides' (<em>nahal</em>) His redeemed people to His holy dwelling.",
     "<em>Nahal</em> is the shepherd-guide word par excellence. It is not the driving of cattle but the gentle leading of lambs and nursing mothers — the kind of guidance that adjusts its pace to the weakest member of the flock. This is the God of the exodus: not a general commanding troops at forced march, but a shepherd carrying lambs and guiding the weak with care. The NT fulfillment is the Good Shepherd who 'calls his own sheep by name and leads (<em>agei</em>) them out' (John 10:3) and lays down his life for them.",
     [("Isaiah 40:11", "He tends his flock like a shepherd: He gathers the lambs in his arms and carries them close to his heart; he gently <em>leads</em> those that have young."),
      ("Exodus 15:13", "In your unfailing love you will <em>lead</em> the people you have redeemed. In your strength you will guide them to your holy dwelling."),
      ("Psalm 31:3", "Since you are my rock and my fortress, for the sake of your name lead and <em>guide</em> me."),
      ("John 10:3", "The gatekeeper opens the gate for him, and the sheep listen to his voice. He calls his own sheep by name and leads them out."),
      ("Revelation 7:17", "For the Lamb at the center of the throne will be their shepherd; he will lead them to springs of living water.")],
     [("H7462", "Raah (Shepherd)"), ("H5090", "Nahag (Drive/Lead)"), ("H5116", "Naveh (Pasture/Resting Place)")]),

    (6005, "עִמָּנוּאֵל", "Immanuel", "Proper Name", "God With Us",
     "Immanuel — the name meaning 'God with us,' given to the child of Isaiah's prophecy and fulfilled in Jesus Christ.",
     "The Hebrew <em>Immanuel</em> (H6005) is a compound name: <em>im</em> (with) + <em>anu</em> (us) + <em>El</em> (God) = 'God with us.' It appears first in Isaiah 7:14: 'Therefore the Lord himself will give you a sign: The virgin will conceive and give birth to a son, and will call him <em>Immanuel</em>.' The name reappears in Isaiah 8:8 and 8:10 as a title of divine assurance: the land is 'your land, O Immanuel' (v.8) and the plot of the nations will fail 'for God is with us' (<em>Immanuel</em>) (v.10).",
     "<em>Immanuel</em> is one of the most theologically loaded proper names in the OT. Its fulfillment in Matthew 1:23 is the hinge of all redemptive history: the eternal Son of God taking human flesh so that 'God with us' becomes not a promise but a physical reality. The entire arc of Scripture moves toward <em>Immanuel</em>: God walking with Adam in the garden, dwelling in the tabernacle and temple, incarnated in Jesus of Nazareth, indwelling the church by the Spirit (John 14:16-17), and finally dwelling with His people forever in the New Jerusalem (Revelation 21:3: 'God's dwelling place is now among the people, and he will dwell with them').",
     [("Isaiah 7:14", "Therefore the Lord himself will give you a sign: The virgin will conceive and give birth to a son, and will call him <em>Immanuel</em>."),
      ("Matthew 1:23", "The virgin will conceive and give birth to a son, and they will call him <em>Immanuel</em> (which means 'God with us')."),
      ("Isaiah 8:10", "Devise your strategy, but it will be thwarted; propose your plan, but it will not stand, for God is with us (<em>Immanuel</em>)."),
      ("John 1:14", "The Word became flesh and made his dwelling among us. We have seen his glory, the glory of the one and only Son."),
      ("Revelation 21:3", "And I heard a loud voice from the throne saying, 'Look! God's dwelling place is now among the people, and he will dwell with them.'")],
     [("H410", "El (God)"), ("H430", "Elohim (God)"), ("H3091", "Yehoshua (Joshua/Salvation)")]),
]

# ─────────────────────────────────────────────
# GREEK ENTRIES (23)
# ─────────────────────────────────────────────
greek_entries = [

    (2003, "ἐπιταγή", "Epitagē", "Noun, feminine", "Command; Authority; Directive",
     "A command or authoritative directive — used of God's commands and apostolic authority.",
     "The Greek <em>epitagē</em> (G2003) is a command or authoritative directive, from <em>epitassō</em> (to arrange or command). Paul uses it of God's eternal command in Romans 16:26: 'the mystery now disclosed... made known through the prophetic writings by the command (<em>epitagē</em>) of the eternal God.' In Titus 1:3, Paul writes that he was 'entrusted with this task by the command (<em>epitagē</em>) of God our Savior.' The word carries the force of non-negotiable divine authority.",
     "<em>Epitagē</em> establishes that Paul's apostleship and the proclamation of the gospel are not human projects but divine commissions carrying the full weight of God's authority. In 1 Corinthians 7:6, Paul carefully distinguishes his personal counsel ('I, not the Lord') from his apostolic commands (<em>epitagē</em> — 'the Lord, not I'). The <em>epitagē</em> of God operates through the apostolic word — which is why Paul can say in Titus 2:15: 'Teach these things. Encourage and rebuke with all authority (<em>epitagē</em>). Do not let anyone despise you.'",
     [("Romans 16:26", "But now revealed and made known through the prophetic writings by the command (<em>epitagē</em>) of the eternal God."),
      ("Titus 1:3", "And which now at his appointed season he has brought to light through the preaching entrusted to me by the command (<em>epitagē</em>) of God our Savior."),
      ("Titus 2:15", "These, then, are the things you should teach. Encourage and rebuke with all authority (<em>epitagē</em>)."),
      ("1 Corinthians 7:25", "Now about virgins: I have no command from the Lord, but I give a judgment as one who by the Lord's mercy is trustworthy."),
      ("1 Timothy 1:1", "Paul, an apostle of Christ Jesus by the command (<em>epitagē</em>) of God our Savior and of Christ Jesus our hope.")],
     [("G1785", "Entolē (Commandment)"), ("G2003", "Epitagē (Command)"), ("G1849", "Exousia (Authority)")]),

    (2005, "ἐπιτελέω", "Epiteleō", "Verb", "To Complete; To Bring to Completion; To Perform",
     "To carry through to completion; to bring to full accomplishment what has been begun.",
     "The Greek <em>epiteleō</em> (G2005) means to bring something to its intended completion — to carry through, finish, or accomplish fully. Paul uses it in Philippians 1:6: 'He who began a good work in you will carry it on to completion (<em>epiteleō</em>) until the day of Christ Jesus.' This is one of the NT's most comforting assurances: God finishes what He starts. In 2 Corinthians 8:6, Paul urges the Corinthians to bring their charitable collection to completion (<em>epiteleō</em>).",
     "<em>Epiteleō</em> in Philippians 1:6 is the basis for the doctrine of the perseverance of the saints — not that believers persist by their own power but that God 'carries through to completion' His redemptive work in them. The prefix <em>epi-</em> intensifies the completion: it is not merely 'to finish' but 'to bring to its appointed fullness.' The God who began the good work of new creation in believers will not abandon it halfway. The parable of the Tower Builder (Luke 14:28-30) warns against beginning without finishing; God never fails to complete what He designs.",
     [("Philippians 1:6", "Being confident of this, that he who began a good work in you will carry it on to completion (<em>epiteleō</em>) until the day of Christ Jesus."),
      ("2 Corinthians 8:6", "So we urged Titus, just as he had earlier made a beginning, to bring also to completion (<em>epiteleō</em>) this act of grace on your part."),
      ("Hebrews 8:5", "They serve at a sanctuary that is a copy and shadow of what is in heaven. This is why Moses was warned when he was about to build the tabernacle: 'See to it that you make everything according to the pattern shown you on the mountain.'"),
      ("Galatians 3:3", "Are you so foolish? After beginning by means of the Spirit, are you now trying to finish (<em>epiteleō</em>) by means of the flesh?"),
      ("Romans 15:28", "So after I have completed (<em>epiteleō</em>) this task and have made sure they have received this contribution, I will go to Spain.")],
     [("G5055", "Teleō (To Finish/Complete)"), ("G5046", "Teleios (Perfect/Complete)"), ("G746", "Archē (Beginning)")]),

    (2007, "ἐπιτίθημι", "Epitithēmi", "Verb", "To Lay Upon; To Impose; To Place On",
     "To place or lay something upon — used of the laying on of hands, burdens, and names.",
     "The Greek <em>epitithēmi</em> (G2007) means to lay, place, or impose something upon someone. It is the verb used for the laying on of hands for blessing, ordination, and healing throughout the NT. Jesus laid hands on children (Matthew 19:13-15) and on the sick (Mark 6:5). The apostles laid hands on deacons (Acts 6:6) and on those receiving the Spirit (Acts 8:17-19). In 1 Timothy 4:14, Timothy's gift was given 'through the laying on of hands' (<em>epitheseōs tōn cheirōn</em>).",
     "The laying on of hands (<em>epitithēmi tas cheiras</em>) is one of the foundational practices of Christian ministry — listed in Hebrews 6:2 as an elementary teaching of the faith. The act communicates identification, blessing, commissioning, and impartation: the one laying hands is identified with the one receiving them, and something is transferred — authority, blessing, or the Holy Spirit. This physical act materializes spiritual reality: the invisible grace of ordination or healing is sealed by a visible, bodily gesture. The body matters in Christian ministry.",
     [("Acts 6:6", "They presented these men to the apostles, who prayed and laid their hands on (<em>epitithēmi</em>) them."),
      ("Mark 6:5", "He could not do any miracles there, except lay his hands on (<em>epitithēmi</em>) a few sick people and heal them."),
      ("1 Timothy 4:14", "Do not neglect your gift, which was given you through prophecy when the body of elders laid their hands on you."),
      ("Acts 8:17", "Then Peter and John placed their hands on them, and they received the Holy Spirit."),
      ("Matthew 19:13", "Then people brought little children to Jesus for him to place his hands on them and pray for them.")],
     [("G5495", "Cheir (Hand)"), ("G5485", "Charis (Grace)"), ("G4295", "Prokeimai (Lie Before/Set Forth)")]),

    (2008, "ἐπιτιμάω", "Epitimaō", "Verb", "To Rebuke; To Warn Sharply; To Silence",
     "To rebuke with sharp authority — used of Jesus silencing demons, storms, and disciples.",
     "The Greek <em>epitimaō</em> (G2008) means to rebuke, warn sharply, or censure with authority. It is one of the characteristic verbs of Jesus' ministry: He rebukes demons (Mark 1:25, 'Be quiet!'), the storm (Mark 4:39), Peter (Mark 8:33, 'Get behind me, Satan!'), and fever (Luke 4:39). The word carries a sense of authoritative control — the rebuke has power to actually silence and stop. In 2 Timothy 4:2, Timothy is charged to 'preach the word... correct, rebuke (<em>epitimaō</em>) and encourage.'",
     "<em>Epitimaō</em> reveals the nature of Jesus' authority: His word is not merely instructive but immediately effective. When He rebukes a demon, it obeys; when He rebukes a storm, it stops. The Capernaum crowd's astonishment was precisely this: 'He gives orders to impure spirits and they obey him' (Mark 1:27). This authority is not merely an attribute of the divine nature but has been delegated to the church (Luke 10:19) and exercised in His name. The pastoral charge in 2 Timothy 4:2 calls for this same spirit of authoritative, caring correction in the ministry of the Word.",
     [("Mark 1:25", "Jesus <em>rebuked</em> him. 'Be quiet!' said Jesus sternly. 'Come out of him!'"),
      ("Mark 4:39", "He got up, <em>rebuked</em> the wind and said to the waves, 'Quiet! Be still!'"),
      ("Mark 8:33", "Jesus turned and looked at his disciples, he <em>rebuked</em> Peter. 'Get behind me, Satan!'"),
      ("2 Timothy 4:2", "Preach the word; be prepared in season and out of season; correct, <em>rebuke</em> and encourage—with great patience and careful instruction."),
      ("Luke 17:3", "So watch yourselves. If your brother or sister sins against you, <em>rebuke</em> them; and if they repent, forgive them.")],
     [("G1651", "Elenchō (Convict/Rebuke)"), ("G3560", "Noutheteō (Admonish)"), ("G1849", "Exousia (Authority)")]),

    (2014, "ἐπιφαίνω", "Epiphainō", "Verb", "To Appear; To Shine Upon; To Manifest",
     "To appear or shine upon — used of God's grace and salvation becoming visible.",
     "The Greek <em>epiphainō</em> (G2014) means to appear, become visible, or shine forth. Its most theologically significant uses are in Luke-Acts and Paul. In Luke 1:79, the 'rising sun' will 'shine on (<em>epiphainō</em>) those living in darkness.' Paul declares in Titus 2:11: 'For the grace of God has appeared (<em>epiphainō</em>) that offers salvation to all people.' And in Titus 3:4: 'But when the kindness and love of God our Savior appeared (<em>epiphainō</em>).' The incarnation is the supreme act of divine <em>epiphainō</em>.",
     "<em>Epiphainō</em> is the verb behind the noun <em>epiphaneia</em> (epiphany) — the appearing of God in history. The Titus passages are among the most compressed theological statements in the NT: the <em>epiphainō</em> of grace (Titus 2:11), the <em>epiphainō</em> of kindness and love (Titus 3:4), and the expected future <em>epiphainō</em> of glory (Titus 2:13). The Christian life is bracketed between two appearances of Christ — the first, in humility and grace, bringing salvation; the second, in glory, bringing consummation. Between these two epiphanies, the church lives and serves.",
     [("Titus 2:11", "For the grace of God has appeared (<em>epiphainō</em>) that offers salvation to all people."),
      ("Titus 3:4", "But when the kindness and love of God our Savior appeared (<em>epiphainō</em>), he saved us."),
      ("Luke 1:79", "To shine on (<em>epiphainō</em>) those living in darkness and in the shadow of death, to guide our feet into the path of peace."),
      ("Acts 27:20", "When neither sun nor stars appeared (<em>epiphainō</em>) for many days and the storm continued raging, we finally gave up all hope of being saved."),
      ("John 1:9", "The true light that gives light to everyone was coming into the world.")],
     [("G2015", "Epiphaneia (Appearing/Epiphany)"), ("G5457", "Phōs (Light)"), ("G5485", "Charis (Grace)")]),

    (2015, "ἐπιφάνεια", "Epiphaneia", "Noun, feminine", "Appearing; Manifestation; Epiphany",
     "The appearing or manifestation of God in glory — used especially of Christ's return.",
     "The Greek <em>epiphaneia</em> (G2015) means a shining forth, manifestation, or visible appearing. In the Pastoral Epistles, it is the dominant word for the second coming of Christ. Paul writes of 'the appearing (<em>epiphaneia</em>) of our Lord Jesus Christ' (1 Timothy 6:14); Timothy is charged to 'keep this command until the appearing of our Lord Jesus Christ.' In 2 Timothy 4:8, Paul looks forward to 'a crown of righteousness... to all who have longed for his appearing (<em>epiphaneia</em>).' In 2 Timothy 1:10, the first coming is also an <em>epiphaneia</em>.",
     "The <em>epiphaneia</em> of Christ is simultaneously past (the incarnation — 2 Timothy 1:10: 'the appearing of our Savior, Christ Jesus, who has destroyed death') and future (the return — Titus 2:13: 'while we wait for the blessed hope — the appearing of the glory of our great God and Savior, Jesus Christ'). The Christian life is oriented between these two poles. The <em>epiphaneia</em> to come is described in 2 Thessalonians 2:8 as the event that destroys the lawless one: 'the splendor of his coming' — the mere appearing of Christ brings judgment upon darkness.",
     [("2 Timothy 4:8", "Now there is in store for me the crown of righteousness, which the Lord, the righteous Judge, will award to me on that day — and not only to me, but also to all who have longed for his appearing (<em>epiphaneia</em>)."),
      ("Titus 2:13", "While we wait for the blessed hope — the appearing (<em>epiphaneia</em>) of the glory of our great God and Savior, Jesus Christ."),
      ("1 Timothy 6:14", "To keep this command without spot or blame until the appearing (<em>epiphaneia</em>) of our Lord Jesus Christ."),
      ("2 Timothy 1:10", "But it has now been revealed through the appearing (<em>epiphaneia</em>) of our Savior, Christ Jesus, who has destroyed death."),
      ("2 Thessalonians 2:8", "And then the lawless one will be revealed, whom the Lord Jesus will overthrow with the breath of his mouth and destroy by the splendor of his coming.")],
     [("G2014", "Epiphainō (Appear)"), ("G3952", "Parousia (Coming/Presence)"), ("G1391", "Doxa (Glory)")]),

    (2048, "ἔρημος", "Erēmos", "Adjective/Noun", "Desert; Wilderness; Solitary Place",
     "A desolate, uninhabited place — the wilderness as place of testing, revelation, and renewal.",
     "The Greek <em>erēmos</em> (G2048) means a desolate or uninhabited place — the wilderness or desert. In the NT, it is deeply theologically charged. John the Baptist is 'a voice of one calling in the desert (<em>erēmos</em>)' (Matthew 3:3, quoting Isaiah 40:3). Jesus is led into the <em>erēmos</em> by the Spirit to be tempted (Matthew 4:1). Jesus frequently retreats to the <em>erēmos</em> to pray (Mark 1:35, Luke 5:16). The wilderness is simultaneously the place of greatest testing and most intimate encounter with God.",
     "The <em>erēmos</em> in biblical theology is the place where human self-sufficiency is stripped away and dependence on God becomes total. Israel's forty years in the desert, Elijah's forty days at Horeb, and Jesus' forty days of temptation all follow this pattern. The desert is where pride dies and trust is forged. Yet the same desert where Israel grumbled is where God provided manna, water from the rock, and His own presence. Isaiah 35:1 promises: 'The desert and the parched land will be glad; the wilderness will rejoice and blossom.' The eschatological hope is the transformation of the <em>erēmos</em> into a garden.",
     [("Matthew 4:1", "Then Jesus was led by the Spirit into the wilderness (<em>erēmos</em>) to be tempted by the devil."),
      ("Mark 1:35", "Very early in the morning, while it was still dark, Jesus got up, left the house and went off to a solitary place (<em>erēmos</em>), where he prayed."),
      ("Isaiah 40:3", "A voice of one calling: 'In the wilderness (<em>erēmos</em>) prepare the way for the LORD; make straight in the desert a highway for our God.'"),
      ("Exodus 16:35", "The Israelites ate manna forty years, until they came to a land that was settled; they ate manna until they reached the border of Canaan."),
      ("Revelation 12:6", "The woman fled into the wilderness (<em>erēmos</em>) to a place prepared for her by God, where she might be taken care of for 1,260 days.")],
     [("G3986", "Peirasmos (Trial/Temptation)"), ("G4336", "Proseuchomai (Pray)"), ("G4151", "Pneuma (Spirit)")]),

    (2049, "ἐρημόω", "Erēmoō", "Verb", "To Make Desolate; To Lay Waste; To Depopulate",
     "To make desolate or lay waste — used of divine judgment and the destruction of Babylon.",
     "The Greek <em>erēmoō</em> (G2049) means to make desolate, destroy, or lay waste. Jesus uses it in His warning about the 'abomination that causes desolation' (Matthew 24:15, quoting Daniel): the temple made desolate. Its most dramatic uses are in Revelation 17:16 and 18:17-19, where Babylon the Great is <em>erēmoō</em> — made desolate by God's judgment. 'In one hour your judgment has come'; 'in one hour she has been brought to ruin' (<em>erēmoō</em>). Divine judgment can reduce what appears permanent to utter desolation in an instant.",
     "<em>Erēmoō</em> in Revelation 17-18 is the verb of apocalyptic justice. Babylon — the city-symbol of all human civilization organized against God — is brought to utter desolation. The merchants who traded in 'the bodies and souls of human beings' (Rev 18:13) mourn her. But heaven rejoices (Rev 19:1-3): 'He has condemned the great prostitute who corrupted the earth by her adulteries. He has avenged on her the blood of his servants.' The <em>erēmoō</em> of Babylon is not senseless destruction but the vindication of justice. What oppresses the image of God will be made desolate.",
     [("Revelation 18:17", "In one hour such great wealth has been brought to ruin (<em>erēmoō</em>)!"),
      ("Matthew 12:25", "Every kingdom divided against itself will be ruined (<em>erēmoō</em>), and every city or household divided against itself will not stand."),
      ("Revelation 17:16", "The beast and the ten horns you saw will hate the prostitute. They will bring her to ruin (<em>erēmoō</em>) and leave her naked."),
      ("Luke 11:17", "Jesus knew their thoughts and said to them: 'Any kingdom divided against itself will be ruined (<em>erēmoō</em>)."),
      ("Isaiah 1:7", "Your country is desolate, your cities burned with fire; your fields are being stripped by foreigners right before you, laid waste as when overthrown by strangers.")],
     [("G2048", "Erēmos (Wilderness/Desolation)"), ("G2920", "Krisis (Judgment)"), ("G2316", "Theos (God)")]),

    (2050, "ἐρήμωσις", "Erēmōsis", "Noun, feminine", "Desolation; Laying Waste; Abandonment",
     "The state of desolation — used especially in the 'abomination of desolation' prophecy.",
     "The Greek <em>erēmōsis</em> (G2050) is the noun form of <em>erēmoō</em> — the state or act of being made desolate. Its most critical occurrence is in the synoptic apocalypse: 'So when you see standing in the holy place the abomination that causes desolation (<em>erēmōsis</em>), spoken of through the prophet Daniel' (Matthew 24:15; Mark 13:14). This phrase, drawn from Daniel 9:27, 11:31, and 12:11, refers to the ultimate desecration of the holy place — whether the Antiochene desecration in 168 BC, the Roman destruction in AD 70, or the final eschatological abomination.",
     "The 'abomination of desolation' (<em>bdelygma tēs erēmōseōs</em>) is the focal point of Jesus' eschatological warning in Matthew 24. It represents the supreme act of sacrilege — the installation of what is utterly abominable in God's most holy place. Historically, Antiochus Epiphanes installed a statue of Zeus in the Jerusalem temple and sacrificed pigs on the altar (1 Maccabees 1:54-59). Jesus warns this pattern will repeat: 'Then let those who are in Judea flee to the mountains' (Matt 24:16). The theological point is that desolation precedes deliverance — the darkest moment triggers the call to flee, not fight, and trust God's rescue.",
     [("Matthew 24:15", "So when you see standing in the holy place the abomination that causes desolation (<em>erēmōsis</em>), spoken of through the prophet Daniel — let the reader understand."),
      ("Mark 13:14", "When you see the abomination that causes desolation (<em>erēmōsis</em>) standing where it does not belong — let the reader understand — then let those who are in Judea flee to the mountains."),
      ("Daniel 9:27", "And at the temple he will set up an abomination that causes desolation, until the end that is decreed is poured out on him."),
      ("Luke 21:20", "When you see Jerusalem being surrounded by armies, you will know that its desolation is near."),
      ("Daniel 11:31", "His armed forces will rise up to desecrate the temple fortress and will abolish the daily sacrifice. Then they will set up the abomination that causes desolation.")],
     [("G2049", "Erēmoō (Make Desolate)"), ("G946", "Bdelygma (Abomination)"), ("G3485", "Naos (Temple/Sanctuary)")]),

    (2052, "ἐριθεία", "Eritheia", "Noun, feminine", "Selfish Ambition; Rivalry; Faction",
     "Self-seeking, partisan striving — contentious ambition that divides community.",
     "The Greek <em>eritheia</em> (G2052) is difficult to translate precisely — it means selfish ambition, partisan self-promotion, or divisive factional striving. It appears in Paul's vice lists (Galatians 5:20: 'selfish ambition' is a work of the flesh; Romans 2:8: those who 'are self-seeking and reject the truth'). In Philippians 2:3, Paul warns: 'Do nothing out of selfish ambition (<em>eritheia</em>) or vain conceit.' James 3:14-16 warns that <em>eritheia</em> in the heart is earthly, unspiritual, and demonic wisdom.",
     "<em>Eritheia</em> in James 3:16 receives one of the NT's most devastating diagnoses: 'For where you have envy and selfish ambition (<em>eritheia</em>), there you find disorder and every evil practice.' The word was originally used of day laborers who worked only for pay, indifferent to the common good. In Paul's usage, it describes the church member who pursues their own agenda at the expense of the body — the partisan who creates factions around their preferences. Philippians 2:3-4 is the direct antidote: 'Do nothing out of <em>eritheia</em>... rather, in humility value others above yourselves.'",
     [("Philippians 2:3", "Do nothing out of selfish ambition (<em>eritheia</em>) or vain conceit. Rather, in humility value others above yourselves."),
      ("Galatians 5:20", "Idolatry and witchcraft; hatred, discord, jealousy, fits of rage, selfish ambition (<em>eritheia</em>), dissensions, factions."),
      ("James 3:16", "For where you have envy and selfish ambition (<em>eritheia</em>), there you find disorder and every evil practice."),
      ("Romans 2:8", "But for those who are self-seeking (<em>eritheia</em>) and who reject the truth and follow evil, there will be wrath and anger."),
      ("2 Corinthians 12:20", "For I am afraid that when I come I may not find you as I want you to be... I fear that there may be discord, jealousy, fits of rage, selfish ambition (<em>eritheia</em>).")],
     [("G5355", "Phthonos (Envy)"), ("G2205", "Zēlos (Zeal/Jealousy)"), ("G5012", "Tapeinophrosynē (Humility)")]),

    (2054, "ἔρις", "Eris", "Noun, feminine", "Strife; Quarreling; Discord; Contention",
     "Strife and quarreling — divisive contention that destroys unity in the church and community.",
     "The Greek <em>eris</em> (G2054) means strife, quarreling, or contentious discord — the spirit of fighting and division. It appears consistently in Paul's vice lists alongside sexual immorality and jealousy: Romans 1:29, 13:13; 1 Corinthians 1:11, 3:3; 2 Corinthians 12:20; Galatians 5:20; Philippians 1:15; Titus 3:9. The Corinthian church was riddled with <em>eris</em> — divisions over teachers, spiritual gifts, and social status. Paul calls this 'worldly' and 'merely human' (1 Corinthians 3:3).",
     "<em>Eris</em> is not the occasional disagreement but the entrenched spirit of contention — the person or community that is perpetually at war with itself. Paul identifies it as a sign of spiritual immaturity: 'You are still worldly. For since there is jealousy and quarreling (<em>eris</em>) among you, are you not worldly?' (1 Corinthians 3:3). Titus 3:9 warns Timothy to 'avoid foolish controversies and genealogies and arguments and quarrels (<em>eris</em>) about the law, because these are unprofitable and useless.' The gospel creates peace; <em>eris</em> is a sign that the gospel has not yet fully taken root.",
     [("Romans 13:13", "Let us behave properly as in the day, not in carousing and drunkenness, not in sexual promiscuity and sensuality, not in strife (<em>eris</em>) and jealousy."),
      ("1 Corinthians 3:3", "For since there is jealousy and quarreling (<em>eris</em>) among you, are you not worldly? Are you not acting like mere humans?"),
      ("Galatians 5:20", "Hatred, discord, jealousy, fits of rage, selfish ambition, dissensions, factions and envy."),
      ("Titus 3:9", "But avoid foolish controversies and genealogies and arguments and quarrels (<em>eris</em>) about the law, because these are unprofitable and useless."),
      ("Proverbs 17:14", "Starting a quarrel is like breaching a dam; so drop the matter before a dispute breaks out.")],
     [("G1370", "Dichostasia (Division)"), ("G5379", "Philoneikia (Love of Strife)"), ("G1515", "Eirēnē (Peace)")]),

    (2083, "ἑταῖρος", "Hetairos", "Noun, masculine", "Companion; Comrade; Friend",
     "A companion or comrade — used notably by Jesus in addressing Judas at his betrayal.",
     "The Greek <em>hetairos</em> (G2083) means companion, associate, or friend. It appears three times in Matthew, and in two of the three it is on the lips of Jesus. In Matthew 20:13, the vineyard owner addresses a grumbling worker as '<em>hetairos</em>.' In Matthew 22:12, the king addresses the man without a wedding garment. Most strikingly, in Matthew 26:50, Jesus says to Judas at the moment of betrayal: '<em>Hetaire</em>, do what you came for.' The word is friendly in register — yet used in the most painful moments.",
     "Jesus addressing Judas as <em>hetairos</em> — 'friend' — at the very moment of betrayal is one of the most theologically charged moments in the Gospels. Unlike <em>philos</em> (intimate friend), <em>hetairos</em> is more of a familiar companion or associate. Jesus does not withdraw the title of companionship even in the face of betrayal — He receives the treacherous kiss with a gentle address. This reflects the character of Christ: He does not meet betrayal with coldness but with the grace that still held open the possibility of repentance until the last moment. The contrast with Peter's denial (who was restored) and Judas's suicide is stark.",
     [("Matthew 26:50", "Jesus replied, 'Do what you came for, <em>friend</em> (<em>hetairos</em>).' Then the men stepped forward, seized Jesus and arrested him."),
      ("Matthew 20:13", "But he answered one of them, '<em>Friend</em> (<em>hetairos</em>), I am not being unfair to you. Didn't you agree to work for a denarius?'"),
      ("Matthew 22:12", "He asked, 'How did you get in here without wedding clothes, <em>friend</em> (<em>hetairos</em>)?'"),
      ("Proverbs 17:17", "A friend loves at all times, and a brother is born for a time of adversity."),
      ("John 13:27", "As soon as Judas took the bread, Satan entered into him. So Jesus told him, 'What you are about to do, do quickly.'")],
     [("G5384", "Philos (Friend)"), ("G80", "Adelphos (Brother)"), ("G26", "Agapē (Love)")]),

    (2090, "ἑτοιμάζω", "Hetoimazō", "Verb", "To Prepare; To Make Ready; To Arrange",
     "To make something or someone ready — used of preparing for Christ's coming and dwelling.",
     "The Greek <em>hetoimazō</em> (G2090) means to prepare, make ready, or arrange. It is a key verb in the NT's theology of divine preparation. Isaiah 40:3 (quoted by all four Gospels) calls for preparing the way of the Lord. In John 14:2-3, Jesus declares: 'I am going there to prepare (<em>hetoimazō</em>) a place for you... I will come back and take you to be with me.' Revelation 21:2 describes the new Jerusalem as 'prepared (<em>hetoimazō</em>) as a bride beautifully dressed for her husband.' God is the great Preparer.",
     "<em>Hetoimazō</em> reveals that Christian eschatology is not random but divinely prepared. The places Jesus goes to prepare are not improvised — they are ready when the time comes. The same verb describes the preparation of the Passover meal (Luke 22:8-13), the preparation of the eternal dwelling (John 14:2), and the preparation of the bride-city for the final wedding (Revelation 19:7, 21:2). God does not react to history; He prepares for it. The believer's task is to be part of God's prepared people — the church that makes herself ready (Revelation 19:7: 'His bride has made herself ready').",
     [("John 14:2", "My Father's house has many rooms; if that were not so, would I have told you that I am going there to prepare (<em>hetoimazō</em>) a place for you?"),
      ("Matthew 3:3", "A voice of one calling in the wilderness, 'Prepare (<em>hetoimazō</em>) the way for the Lord, make straight paths for him.'"),
      ("Revelation 21:2", "I saw the Holy City, the new Jerusalem, coming down out of heaven from God, prepared (<em>hetoimazō</em>) as a bride beautifully dressed for her husband."),
      ("Luke 22:8", "Jesus sent Peter and John, saying, 'Go and make preparations (<em>hetoimazō</em>) for us to eat the Passover.'"),
      ("1 Corinthians 2:9", "No eye has seen, no ear has heard, no mind has conceived what God has prepared (<em>hetoimazō</em>) for those who love him.")],
     [("G2093", "Hetoimōs (Ready)"), ("G3588", "Ho (The)"), ("G3952", "Parousia (Coming)")]),

    (2094, "ἔτος", "Etos", "Noun, neuter", "Year; Annual Period",
     "A year — used to mark divine promises, long waits, and the fullness of time.",
     "The Greek <em>etos</em> (G2094) is simply a year, but in the NT its uses carry significant theological weight. Simeon and Anna had waited years for the Messiah (Luke 2:36-37). Paul had his three years in Arabia after his conversion (Galatians 1:18). The woman bent double had suffered eighteen years (Luke 13:11). The man at Bethesda had been ill thirty-eight years (John 5:5). The repeated emphasis on years of waiting underlines the costliness of hope and the faithfulness of the God who finally acts.",
     "The <em>etos</em> passages collectively form a theology of patient waiting. The years of delay are not failures of faith but spaces for God's sovereign preparation. Anna's eighty-four years as a widow in the temple, waiting for the consolation of Israel, is the paradigm of faithful longing (Luke 2:37). Paul's fourteen years before his public ministry (Galatians 2:1) parallel Moses' forty years in the desert. The NT's longest waiting period is the 1,000 years of Revelation 20 — but even that is not an eternity. All <em>etē</em> (years) move toward the moment when 'time shall be no more' (Revelation 10:6).",
     [("Luke 2:37", "She was a widow until she was eighty-four. She never left the temple but worshiped night and day, fasting and praying."),
      ("John 5:5", "One who was there had been an invalid for thirty-eight years."),
      ("Luke 13:11", "A woman was there who had been crippled by a spirit for eighteen years."),
      ("Galatians 4:4", "But when the set time (<em>plērōma tou chronou</em>) had fully come, God sent his Son."),
      ("Hebrews 11:27", "By faith he left Egypt, not fearing the king's anger; he persevered because he saw him who is invisible.")],
     [("G2540", "Kairos (Season/Time)"), ("G5550", "Chronos (Time)"), ("G165", "Aiōn (Age/Eternity)")]),

    (2112, "εὐθέως", "Eutheos", "Adverb", "Immediately; Straightway; At Once",
     "Immediately, at once — characteristic of Mark's Gospel, emphasizing Jesus' decisive action.",
     "The Greek <em>eutheōs</em> (G2112) means immediately or at once — and it is arguably the most characteristic word of Mark's Gospel, where it appears over 40 times. After Jesus calls a disciple, they follow immediately. After He heals, the person is well immediately. After the baptism, the Spirit drives Him into the desert immediately. The word captures the urgency and authority of Jesus' ministry — nothing drags or delays in Mark; the Kingdom of God arrives with the force and speed of divine action.",
     "<em>Eutheōs</em> in Mark is not merely a narrative device — it is a theological statement. The Kingdom of God does not arrive gradually or tentatively; it breaks in with sudden, decisive power. When Jesus speaks, things happen. When He heals, the healing is complete and instant. This is the God of the exodus, who acted swiftly to deliver (Exodus 12:12: 'On that same night I will pass through Egypt'). For the believer, <em>eutheōs</em> is also the appropriate response to divine calling — as the disciples demonstrate by leaving their nets 'immediately' and following (Mark 1:18, 20). Obedience need not wait.",
     [("Mark 1:18", "At once (<em>eutheōs</em>) they left their nets and followed him."),
      ("Mark 1:12", "At once (<em>eutheōs</em>) the Spirit sent him out into the wilderness."),
      ("Mark 4:29", "As soon as the grain is ripe, he puts the sickle to it, because the harvest has come."),
      ("John 19:34", "Instead, one of the soldiers pierced Jesus' side with a spear, and immediately (<em>eutheōs</em>) blood and water came out."),
      ("Acts 9:18", "Immediately (<em>eutheōs</em>), something like scales fell from Saul's eyes, and he could see again.")],
     [("G5034", "Tachos (Speed)"), ("G3956", "Pas (All)"), ("G3056", "Logos (Word)")]),

    (2186, "ἐφίστημι", "Ephistēmi", "Verb", "To Stand Near; To Appear Suddenly; To Come Upon",
     "To stand near or come upon suddenly — used of angels appearing, the Lord coming, and urgent preaching.",
     "The Greek <em>ephistēmi</em> (G2186) means to stand near, arrive suddenly, or come upon someone. In Luke-Acts it is the characteristic verb for angelic appearances: the angel of the Lord 'appeared' (<em>ephistēmi</em>) to the shepherds (Luke 2:9), to the disciples at the tomb (Luke 24:4), to Peter in prison (Acts 12:7). Paul uses it for urgent apostolic ministry: 'Preach the word; be prepared in season and out of season' — 'be prepared' translates <em>epistethi</em> (2 Timothy 4:2), the imperative of <em>ephistēmi</em>: 'stand at your post!'",
     "<em>Ephistēmi</em> creates a theology of divine suddenness. God breaks into human situations without warning: angels appear, the Lord comes, the Spirit arrives. Paul's charge in 2 Timothy 4:2 uses the same verb to charge Timothy to 'stand at his post' in preaching — matching the readiness of the divine messenger with the readiness of the human one. The Christian minister is to be as consistently present and ready as an angel: not waiting for convenient moments but standing ready in all seasons. The Day of the Lord itself comes like a thief — suddenly, without warning (1 Thessalonians 5:3: 'sudden destruction comes upon them').",
     [("Luke 2:9", "An angel of the Lord appeared (<em>ephistēmi</em>) to them, and the glory of the Lord shone around them."),
      ("Acts 12:7", "Suddenly an angel of the Lord appeared (<em>ephistēmi</em>) and a light shone in the cell."),
      ("2 Timothy 4:2", "Preach the word; be prepared (<em>epistethi</em>) in season and out of season."),
      ("Luke 24:4", "While they were wondering about this, suddenly two men in clothes that gleamed like lightning stood beside (<em>ephistēmi</em>) them."),
      ("1 Thessalonians 5:3", "While people are saying, 'Peace and safety,' destruction will come on them suddenly, as labor pains on a pregnant woman.")],
     [("G32", "Angelos (Messenger/Angel)"), ("G2784", "Kēryssō (Proclaim/Preach)"), ("G3952", "Parousia (Coming)")]),

    (2281, "θάλασσα", "Thalassa", "Noun, feminine", "Sea; Lake; Body of Water",
     "The sea — in Scripture a place of chaos, divine power, and eschatological promise.",
     "The Greek <em>thalassa</em> (G2281) is the sea — in Scripture not merely a geographical feature but a theological symbol. The OT sea represents primordial chaos (Genesis 1:2: 'the deep'), divine power (Job 38:8-11: 'Who shut up the sea behind doors?'), and the realm of danger and death. Jesus walking on the sea (Matthew 14:25) and stilling the storm (Mark 4:39) demonstrate His dominion over chaos. The Sea of Galilee (<em>thalassa</em>) is the arena for many of Jesus' miracles and the calling of His disciples.",
     "<em>Thalassa</em> carries eschatological weight in Revelation, where the 'sea' gives up its dead (Revelation 20:13) and, in the new creation, 'there was no longer any sea' (Revelation 21:1). The disappearance of the sea in the new creation is not the elimination of water but the end of the chaos, danger, and separation it represents. The new Jerusalem needs no sea because there will be no more separation, no more threat, no more death. Meanwhile, in the present age, the sea of glass before the throne (Revelation 4:6, 15:2) represents the tamed chaos — the <em>thalassa</em> brought under God's sovereign peace.",
     [("Matthew 14:25", "Shortly before dawn Jesus went out to them, walking on the lake (<em>thalassa</em>)."),
      ("Mark 4:39", "He got up, rebuked the wind and said to the waves, 'Quiet! Be still!' Then the wind died down and it was completely calm."),
      ("Revelation 21:1", "Then I saw a new heaven and a new earth, for the first heaven and the first earth had passed away, and there was no longer any <em>sea</em> (<em>thalassa</em>)."),
      ("Revelation 20:13", "The sea gave up the dead that were in it, and death and Hades gave up the dead that were in them."),
      ("Psalm 107:23", "Some went out on the sea in ships; they were merchants on the mighty waters.")],
     [("G5204", "Hydōr (Water)"), ("G417", "Anemos (Wind)"), ("G2316", "Theos (God)")]),

    (2380, "θύω", "Thyō", "Verb", "To Sacrifice; To Slaughter; To Kill",
     "To sacrifice or slaughter — used of the Passover lamb and Christ as the ultimate sacrifice.",
     "The Greek <em>thyō</em> (G2380) means to sacrifice or slaughter — it is used for both sacrificial offerings to God and ordinary slaughter for food. Its most theologically loaded occurrence is 1 Corinthians 5:7: 'For Christ, our Passover lamb, has been sacrificed (<em>thyō</em>).' In Luke 15:23-30, the father in the parable of the prodigal son commands: 'Kill (<em>thyō</em>) the fattened calf and let's have a feast.' In Acts 14:13, the priest of Zeus wants to sacrifice bulls to Barnabas and Paul — the pagan reflex of <em>thyō</em>.",
     "<em>Thyō</em> in 1 Corinthians 5:7 is one of the most compact atonement statements in the NT. Paul draws the direct typological line: the Passover lamb that was slaughtered (<em>thyō</em>) to protect Israel from the angel of death points to Christ, who was slaughtered once-for-all to protect His people from eternal death. The Passover required both the sacrifice and the application of blood — both are fulfilled in Christ's cross (the sacrifice) and the believer's faith (the application). And because Christ 'our Passover has been <em>thyō</em>'d,' the church can celebrate the feast — with sincerity and truth (v.8).",
     [("1 Corinthians 5:7", "For Christ, our Passover lamb, has been sacrificed (<em>thyō</em>). Therefore let us keep the Festival."),
      ("Luke 15:23", "'Bring the fattened calf and kill (<em>thyō</em>) it. Let's have a feast and celebrate.'"),
      ("John 10:10", "The thief comes only to steal and kill (<em>thyō</em>) and destroy; I have come that they may have life, and have it to the full."),
      ("Exodus 12:6", "Take care of them until the fourteenth day of the month, when all the members of the community of Israel must slaughter them at twilight."),
      ("Hebrews 9:22", "In fact, the law requires that nearly everything be cleansed with blood, and without the shedding of blood there is no forgiveness.")],
     [("G2378", "Thusia (Sacrifice)"), ("G286", "Amnos (Lamb)"), ("G129", "Haima (Blood)")]),

    (2634, "κατακυριεύω", "Katakurieuō", "Verb", "To Lord Over; To Dominate; To Have Mastery Over",
     "To exercise lordship or dominance over — forbidden as a leadership style in the church.",
     "The Greek <em>katakurieuō</em> (G2634) means to lord it over, to exercise dominion, or to master completely. The prefix <em>kata</em> intensifies: it is domineering lordship. Jesus uses it in defining the contrast between worldly and servant leadership: 'You know that the rulers of the Gentiles lord it over (<em>katakurieuō</em>) them, and their high officials exercise authority over them. Not so with you' (Matthew 20:25-26). Peter uses the same word to warn elders: 'Not lording it over (<em>katakurieuō</em>) those entrusted to you' (1 Peter 5:3).",
     "<em>Katakurieuō</em> is the negative pole against which Christian leadership is defined. The world's leadership model is domination — using power to control others, to secure one's position, to extract service from subordinates. Jesus explicitly forbids this in the church: the greatest must be servant of all, following the pattern of the Son of Man who 'came not to be served, but to serve, and to give his life as a ransom for many' (Matthew 20:28). Peter's echo of this in 1 Peter 5:3 adds: the alternative to <em>katakurieuō</em> is being an <em>example</em> to the flock — servant leadership visible in incarnate life.",
     [("Matthew 20:25", "Jesus called them together and said, 'You know that the rulers of the Gentiles lord it over (<em>katakurieuō</em>) them.'"),
      ("1 Peter 5:3", "Not lording it over (<em>katakurieuō</em>) those entrusted to you, but being examples to the flock."),
      ("Mark 10:42", "Jesus called them together and said, 'You know that those who are regarded as rulers of the Gentiles lord it over them.'"),
      ("Matthew 20:28", "Just as the Son of Man did not come to be served, but to serve, and to give his life as a ransom for many."),
      ("Philippians 2:5", "In your relationships with one another, have the same mindset as Christ Jesus.")],
     [("G1249", "Diakonos (Servant/Deacon)"), ("G5013", "Tapeinoō (Humble)"), ("G2962", "Kyrios (Lord)")]),

    (2637, "κατάλαλος", "Katalalos", "Noun/Adjective", "Slanderer; Backbiter; Evil Speaker",
     "One who speaks evil against others — the slanderer condemned in Paul's vice lists.",
     "The Greek <em>katalalos</em> (G2637) means a slanderer or backbiter — one who speaks behind another's back to injure them. It appears in Romans 1:30, in the catalog of the morally degraded: 'gossips, slanderers (<em>katalaloi</em>), God-haters.' The related verb <em>katalaleo</em> appears in James 4:11: 'Brothers and sisters, do not slander (<em>katalaleo</em>) one another.' The prefix <em>kata</em> suggests speaking down against someone — the act of diminishing another through speech.",
     "<em>Katalalos</em> in Romans 1:30 appears in a list that begins with cosmic rebellion against God and ends with slanderers and parent-haters — the social symptoms of a society that has exchanged God's glory for idols. Slander is not merely impolite; it is spiritually diagnostic. It reveals a heart shaped by the accuser (<em>diabolos</em> — devil — means 'the accuser'). James 4:11-12 goes further: 'Anyone who speaks against a brother or sister or judges them speaks against the law and judges it... There is only one Lawgiver and Judge.' To slander a person made in God's image is to indict God's work.",
     [("Romans 1:30", "Slanderers (<em>katalaloi</em>), God-haters, insolent, arrogant and boastful; they invent ways of doing evil; they disobey their parents."),
      ("James 4:11", "Brothers and sisters, do not slander (<em>katalaleo</em>) one another. Anyone who speaks against a brother or sister or judges them speaks against the law."),
      ("1 Peter 2:1", "Therefore, rid yourselves of all malice and all deceit, hypocrisy, envy, and slander (<em>katalalia</em>) of every kind."),
      ("Proverbs 20:19", "A gossip betrays a confidence; so avoid anyone who talks too much."),
      ("Psalm 101:5", "Whoever slanders their neighbor in secret, I will put to silence.")],
     [("G1228", "Diabolos (Devil/Slanderer)"), ("G5571", "Pseudēs (Liar)"), ("G26", "Agapē (Love)")]),

    (2640, "κατάλειμμα", "Kataleimma", "Noun, neuter", "Remnant; Those Left Behind",
     "A remnant — the small remainder preserved by God's grace through judgment.",
     "The Greek <em>kataleimma</em> (G2640) is the remnant — the small portion that survives when the larger group is cut down. It appears in Romans 9:27, quoting Isaiah 10:22: 'Though the number of the Israelites be like the sand by the sea, only the remnant (<em>kataleimma</em>) will be saved.' This is Paul's answer to the question of whether God has failed His people (Romans 9:6): No — God has always worked through a remnant, preserving a faithful core through whom His purposes advance.",
     "The <em>kataleimma</em> theology in Romans 9 is the key to understanding how God's faithfulness operates in history. The remnant principle is present throughout Scripture: Noah's eight (Genesis 7-8), Elijah's seven thousand (1 Kings 19:18), the exilic community, the Galilean disciples, the 120 at Pentecost, the church in every persecuted generation. God does not need majorities. His purposes run through faithful minorities — the <em>kataleimma</em>. Paul's personal testimony is the same: he himself is part of the remnant 'chosen by grace' (Romans 11:5), proving that God has not rejected His people.",
     [("Romans 9:27", "Isaiah cries out concerning Israel: 'Though the number of the Israelites be like the sand by the sea, only the remnant (<em>kataleimma</em>) will be saved.'"),
      ("Romans 11:5", "So too, at the present time there is a remnant (<em>leimma</em>) chosen by grace."),
      ("Isaiah 10:22", "Though your people be like the sand by the sea, Israel, only a remnant will return."),
      ("1 Kings 19:18", "Yet I reserve seven thousand in Israel — all whose knees have not bowed down to Baal."),
      ("Ezra 9:8", "But now, for a brief moment, the LORD our God has been gracious in leaving us a remnant.")],
     [("G3062", "Loipoi (Rest/Remainder)"), ("H7611", "Sherith (Remnant)"), ("G5485", "Charis (Grace)")]),

    (2641, "καταλείπω", "Kataleipō", "Verb", "To Leave Behind; To Forsake; To Abandon",
     "To leave behind or forsake — used of God's faithfulness to never forsake His people.",
     "The Greek <em>kataleipō</em> (G2641) means to leave behind, forsake, or abandon. It appears in the most comforting promise of the NT: Hebrews 13:5 quotes Deuteronomy 31:6 — 'Never will I leave (<em>kataleipō</em>) you; never will I forsake you.' The double negative in Greek is emphatic: 'I will absolutely never, not ever, abandon you.' In Romans 11:4, Paul quotes God's word to Elijah: 'I have reserved for myself seven thousand who have not bowed the knee to Baal' — God had not <em>kataleipō</em>'d His people.",
     "The promise 'Never will I <em>kataleipō</em> you' (Hebrews 13:5) is the anchor of Christian contentment in all circumstances. Paul grounds his instruction on contentment (Hebrews 13:5: 'Keep your lives free from the love of money and be content with what you have') directly in this divine promise. Because God will never abandon us, we never need to grasp for security through material accumulation. The same promise was given to Israel entering the land (Deuteronomy 31:6), to Joshua (Joshua 1:5), and now to every NT believer. The God who will never leave us is enough.",
     [("Hebrews 13:5", "Keep your lives free from the love of money and be content with what you have, because God has said, 'Never will I leave (<em>kataleipō</em>) you; never will I forsake you.'"),
      ("Deuteronomy 31:6", "Be strong and courageous. Do not be afraid or terrified because of them, for the LORD your God goes with you; he will never leave you nor forsake you."),
      ("Romans 11:4", "And what was God's answer to him? 'I have reserved for myself seven thousand who have not bowed the knee to Baal.'"),
      ("Matthew 19:5", "'For this reason a man will leave (<em>kataleipō</em>) his father and mother and be united to his wife.'"),
      ("John 14:18", "I will not leave you as orphans; I will come to you.")],
     [("G2640", "Kataleimma (Remnant)"), ("G3306", "Menō (Remain/Abide)"), ("G3754", "Hoti (Because)")]),

    (2647, "καταλύω", "Katalyō", "Verb", "To Destroy; To Abolish; To Dissolve; To Lodge",
     "To loose down, demolish, or abolish — and also to unharness for lodging; used of the law and the temple.",
     "The Greek <em>katalyō</em> (G2647) has two related meanings: (1) to demolish, destroy, or abolish — to undo what has been built or established; (2) to unharness animals and lodge for the night. Jesus uses <em>katalyō</em> in two critical passages: Do not think that I have come to abolish the Law or the Prophets; I have not come to abolish them but to fulfill them (Matthew 5:17). And at His trial: This fellow said, I am able to destroy the temple of God and rebuild it in three days (Matthew 26:61).",
     "The two uses of <em>katalyō</em> in Matthew point to the same theological axis. Jesus does not come to demolish the OT scriptures but to bring them to their full intended meaning — <em>katalyō</em> is contrasted with <em>plēroō</em> (fulfill/fill up). Yet He will 'destroy' the temple in a deeper sense: His body is the true temple (John 2:19-21), and in His death and resurrection the old sacrificial system is superseded. The temple authorities feared a literal <em>katalyō</em>; Jesus was announcing a deeper one — the end of the Mosaic ceremonial order and the inauguration of the new covenant in His body.",
     [("Matthew 5:17", "Do not think that I have come to abolish (<em>katalyō</em>) the Law or the Prophets; I have not come to abolish them but to fulfill them."),
      ("Matthew 26:61", "This fellow said, 'I am able to destroy (<em>katalyō</em>) the temple of God and rebuild it in three days.'"),
      ("John 2:19", "Jesus answered them, 'Destroy this temple, and I will raise it again in three days.'"),
      ("Luke 19:7", "All the people saw this and began to mutter, 'He has gone to be the guest (<em>katalyō</em>) of a sinner.'"),
      ("Acts 6:14", "For we have heard him say that this Jesus of Nazareth will destroy (<em>katalyō</em>) this place and change the customs Moses handed down to us.")],
     [("G3485", "Naos (Temple)"), ("G4137", "Plēroō (Fulfill)"), ("G1242", "Diathēkē (Covenant)")]),
]

def write_page(strongs_id, lang, script, translit, pos, gloss, short_def, definition, theology, verses, related):
    html = make_page(strongs_id, lang, script, translit, pos, gloss, short_def, definition, theology, verses, related)
    path = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Wrote {path}")

print("Generating 47 lexicon pages...")
print("\n=== HEBREW (24) ===")
for entry in hebrew_entries:
    num, script, translit, pos, gloss, short_def, definition, theology, verses, related = entry
    strongs_id = f"H{num}"
    write_page(strongs_id, "H", script, translit, pos, gloss, short_def, definition, theology, verses, related)

print("\n=== GREEK (23) ===")
for entry in greek_entries:
    num, script, translit, pos, gloss, short_def, definition, theology, verses, related = entry
    strongs_id = f"G{num}"
    write_page(strongs_id, "G", script, translit, pos, gloss, short_def, definition, theology, verses, related)

print("\nDone! 47 pages written.")
