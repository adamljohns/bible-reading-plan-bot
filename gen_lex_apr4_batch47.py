#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - Cron batch Apr 4 2026"""
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
            <div class="strongs-badge">{strongs_id} · {lang_label}</div>
            <div class="original-word{extra_class}" style="{dir_attr}">{script}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>

        <div class="section">
            <h2>📖 Definition</h2>
            <p><strong>{short_def}</strong></p>
            <p>{definition}</p>
        </div>

        <div class="section">
            <h2>✝️ Theological Significance</h2>
            <p>{theology}</p>
        </div>

        <div class="section">
            <h2>📜 Key Verses</h2>
{verses_html}        </div>

        <div class="section">
            <h2>🔗 Related Words</h2>
            <div class="related-words">
{related_html}            </div>
        </div>

        <div class="section">
            <h2>🌐 External Resources</h2>
            <div class="ext-links">
                <a href="https://www.blueletterbible.org/lexicon/{blb_lang}{num}/kjv/wlc/0-1/" class="ext-link" target="_blank" rel="noopener">Blue Letter Bible</a>
                <a href="https://biblehub.com/{ext_lang}/{num}.htm" class="ext-link" target="_blank" rel="noopener">BibleHub</a>
                <a href="https://www.studylight.org/lexicons/eng/{'greek' if lang=='G' else 'hebrew'}/{num}.html" class="ext-link" target="_blank" rel="noopener">StudyLight</a>
            </div>
        </div>
    </div>

    <footer>
        <p>Strong's {strongs_id} · <a href="../lexicon.html">USMC Ministries Lexicon</a> · <a href="../index.html">Home</a></p>
    </footer>
    {JS}
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────
# WORD DATA: 24 Hebrew + 23 Greek
# ─────────────────────────────────────────────────────────────────

WORDS = [

# ════════════════════════════════════
# HEBREW WORDS (24)
# ════════════════════════════════════

("H1470", "H", "גָּאוֹן", "gaon", "Masculine Noun", "Pride, majesty, excellency",
 "Pride, arrogance; but also majesty, splendor, and the swelling of greatness.",
 "<em>Gaon</em> (גָּאוֹן) carries a dual weight in Scripture. When applied to God, it speaks of His incomparable <em>majesty</em> and <em>excellency</em>—the rising up of divine glory like a flood in full surge. When applied to humanity, it warns of the swelling self-exaltation that precedes destruction. Derived from the root <em>ga'ah</em> (to rise up), the word captures both the grandeur of God's sovereign elevation and the fatal pride that causes mankind to exalt himself above his Maker.",
 "In <em>Gaon</em>, we encounter one of Scripture's sharpest contrasts: God's majesty is the only legitimate 'rising up,' and it is the measure by which all human pride is exposed as hollow. The prophets used <em>gaon</em> to declare God's glory over nations that boasted in their own strength. Israel's sin of <em>gaon</em> — trusting in her own greatness — brought exile and judgment. Yet God's own <em>gaon</em> — His majestic splendor — is the basis for ultimate restoration. For the USMC warrior, this word calls for the fierce humility of recognizing that only God's elevation endures; human achievement is vapor unless it rests in His glory.",
 [
   ("Ps 47:4", "He shall choose our inheritance for us, the <em>excellency</em> [gaon] of Jacob whom He loves."),
   ("Is 13:11", "I will punish the world for its evil, and the wicked for their iniquity; I will halt the <em>arrogance</em> [gaon] of the proud."),
   ("Is 60:15", "Whereas you have been forsaken and hated, so that no one went through you, I will make you an eternal <em>excellence</em> [gaon], a joy of many generations."),
   ("Amos 8:7", "The LORD has sworn by the <em>pride</em> [gaon] of Jacob: 'Surely I will never forget any of their works.'"),
   ("Ps 68:34", "Ascribe power to God; His <em>excellence</em> [gaon] is over Israel, and His strength is in the clouds."),
 ],
 [("H1346","gaavah — pride/arrogance"), ("H1361","gabah — be exalted"), ("H1363","gobah — height/haughtiness"), ("H3519","kabod — glory/honor")]),

("H1293", "H", "בְּרָכָה", "berakah", "Feminine Noun", "Blessing, benediction, gift of prosperity",
 "A blessing; the gift or state of prosperity and favor flowing from God.",
 "<em>Berakah</em> (בְּרָכָה) is the noun form of <em>barak</em> (to bless, H1288). It captures both the <em>act of blessing</em>—the pronouncement of divine favor—and the <em>state of being blessed</em>—the resulting flourishing in life. In the ancient Near East, a blessing was not merely a kind word but a conferral of life-force and favor. When God blesses, reality changes. <em>Berakah</em> was the treasure of the patriarchs (Isaac's blessing to Jacob), the inheritance of covenant (Abraham's blessing to all nations), and the goal of priestly ministry (the Aaronic blessing).",
 "<em>Berakah</em> reveals the generosity at the heart of God's character. He is not a reluctant giver—He is the source and summit of all blessing. The Aaronic Benediction (Numbers 6:24–26) entrusts human priests to pronounce <em>berakah</em> over Israel, showing that God enlists His people as conduits of His favor. Malachi's challenge—'bring the whole tithe... and test Me in this'—promises a <em>berakah</em> so overwhelming there is no room to receive it. For believers, every spiritual gift, every moment of shalom, every answered prayer flows from this word. Christ became a curse so that the <em>berakah</em> of Abraham might come to the Gentiles through faith.",
 [
   ("Gen 12:2", "I will make you a great nation; I will bless you and make your name great; and you shall be a <em>blessing</em> [berakah]."),
   ("Num 6:23", "Speak to Aaron and his sons, saying: 'This is the way you shall <em>bless</em> [berakah] the children of Israel.'"),
   ("Deut 28:2", "All these <em>blessings</em> [berakah] shall come upon you and overtake you, because you obey the voice of the LORD your God."),
   ("Ps 129:8", "Neither do those who pass by say, 'The <em>blessing</em> [berakah] of the LORD be upon you.'"),
   ("Mal 3:10", "Bring all the tithes into the storehouse... and try Me now in this, says the LORD, if I will not open for you the windows of heaven and pour out for you such <em>blessing</em> [berakah] that there will not be room enough to receive it."),
 ],
 [("H1288","barak — bless"), ("H1285","berit — covenant"), ("H2896","tov — good"), ("H7965","shalom — peace/welfare")]),

("H1300", "H", "בָּרָק", "baraq", "Masculine Noun", "Lightning, glittering brightness",
 "Lightning; the bright flash of divine power, the gleam of a sword, the dart of fire.",
 "<em>Baraq</em> (בָּרָק) is the vivid Hebrew word for <em>lightning</em>—that sudden, terrifying brilliance that splits the night sky. In Scripture, lightning is almost always associated with the <em>theophany</em> of God: the storm of Sinai, the chariot-throne of Ezekiel, the Psalms' cosmic warfare imagery. <em>Baraq</em> also describes the gleam of weapons (Ezek 21:15), the flashing spear-point, the dart of divine judgment. The name Barak the judge carries this meaning—a warrior like lightning across the battlefield.",
 "The theology of <em>baraq</em> is the theology of divine irresistibility. Lightning cannot be stopped, bargained with, or delayed. When God moves in judgment or salvation, He comes with the speed and brilliance of lightning. Jesus used this imagery for both His own return ('as lightning comes from the east...') and for Satan's fall ('I saw Satan fall like lightning'). For the USMC warrior and the man of God, <em>baraq</em> is a reminder: God's timing is sudden, His power absolute, His brilliance beyond anything human eyes can endure. Be ready. The lightning does not announce itself.",
 [
   ("Ps 18:14", "He sent out His arrows and scattered the foe, lightnings [baraq] in abundance, and He vanquished them."),
   ("Job 37:3", "He sends it forth under the whole heaven, His <em>lightning</em> [baraq] to the ends of the earth."),
   ("Ps 77:18", "The voice of Your thunder was in the whirlwind; the lightnings [baraq] lit up the world; the earth trembled and shook."),
   ("Ezek 1:14", "And the living creatures ran back and forth, in appearance like a flash of <em>lightning</em> [baraq]."),
   ("Nahum 3:3", "Horsemen charge with bright sword and glittering spear [baraq]; there is a multitude of slain."),
 ],
 [("H7565","resheph — flame/pestilence"), ("H2385","chaziz — lightning/thunderbolt"), ("H7482","raham — thunder"), ("H3519","kabod — glory")]),

("H1360", "H", "גֶּבֶא", "gebe", "Masculine Noun", "Cistern, pool, reservoir",
 "A pit, cistern, or reservoir for collecting water; a dug-out place of gathering.",
 "<em>Gebe</em> (גֶּבֶא) refers to a <em>cistern</em> or <em>pool</em>—a carved-out hollow in the earth that collects and holds water. In the ancient Near East, cisterns were life-or-death infrastructure; without them, settlements perished. The imagery of pit and cistern runs throughout biblical poetry and prophecy, often serving as metaphor for the human soul thirsting for God, or for the danger of trusting in anything but the living water of God's provision.",
 "Jeremiah's great indictment of Israel used cistern imagery at its sharpest: 'My people have committed two evils: they have forsaken Me, the fountain of living waters, and hewn themselves cisterns—broken cisterns that can hold no water' (Jer 2:13). The contrast is everything: the infinite, self-replenishing spring of God's presence versus the cracked, finite, self-constructed reservoirs of human religion and self-sufficiency. <em>Gebe</em> reminds us that every human institution, every man-made system of meaning, is ultimately a <em>gebe</em>—useful only insofar as it directs the thirsty to the living God.",
 [
   ("Is 30:14", "It shall not be found in the breaking of it a shard to take fire from the hearth, or to take water out of the <em>cistern</em> [gebe]."),
   ("Jer 14:3", "Their nobles have sent their little ones to the water; they came to the <em>cisterns</em> [gebe] and found no water."),
   ("2 Kings 18:31", "Make peace with me... eat each one of his own vine and each one of his own fig tree, and drink each one the water of his own <em>cistern</em> [gebe]."),
   ("Prov 5:15", "Drink water from your own <em>cistern</em>, running water from your own well."),
   ("Eccl 12:6", "Before the silver cord is snapped, or the golden bowl is broken, or the <em>pitcher</em> is shattered at the fountain, or the wheel broken at the <em>cistern</em> [gebe]."),
 ],
 [("H953","bor — pit/cistern"), ("H4599","mayan — spring/fountain"), ("H5869","ayin — eye/spring"), ("H2416","chay — living")]),

("H1382", "H", "גָּלַל", "galal", "Verb", "To roll, roll away, commit to, trust",
 "To roll; to roll away; to trust or commit (rolling one's burden onto another).",
 "<em>Galal</em> (גָּלַל) is primarily the physical action of <em>rolling</em>—rolling away a stone, rolling in anguish. But its theological depth comes from the metaphorical use: to <em>commit</em> or <em>roll</em> one's way and burdens onto God. Psalm 22 and Psalm 37 use forms of this word to instruct the faithful: don't grip your burdens with white-knuckled anxiety—<em>roll them onto</em> the Lord. The noun <em>gilgal</em> (rolling/wheel) comes from this root.",
 "The act of <em>galal</em> is an act of deliberate, muscular faith. Just as a stone must be physically rolled away—it doesn't move itself—so the burden of anxiety, the weight of uncertainty, the stone of grief must be actively, consciously <em>rolled onto</em> God. This is not passive acceptance; it is vigorous trust. Peter echoes this theology in 1 Peter 5:7 (casting all your anxiety on Him, because He cares for you). The Gospel itself is a <em>galal</em> event: the stone was rolled away from the tomb. Death's grip was broken. Every morning, the follower of Christ practices <em>galal</em>—rolling the stone of that day's fears onto the One who already rolled away the greatest stone of all.",
 [
   ("Ps 22:8", "He <em>trusted</em> [galal] in the LORD; let Him rescue him; let Him deliver him, since He delights in him."),
   ("Ps 37:5", "<em>Commit</em> [galal] your way to the LORD, trust also in Him, and He shall bring it to pass."),
   ("Prov 16:3", "<em>Commit</em> [galal] your works to the LORD, and your thoughts will be established."),
   ("Josh 5:9", "The LORD said to Joshua, 'This day I have <em>rolled away</em> [galal] the reproach of Egypt from you.'"),
   ("Gen 29:3", "When all the flocks were gathered, they would <em>roll</em> [galal] the stone from the well's mouth."),
 ],
 [("H1556","galal verb — roll/roll away"), ("H1360","gilgal — wheel/rolling"), ("H982","batach — trust"), ("H2620","chasah — take refuge")]),

("H1404", "H", "גְּבֶרֶת", "geberet", "Feminine Noun", "Mistress, lady, queen mother",
 "A mistress or lady of high rank; a queen mother; one in a position of honored authority.",
 "<em>Geberet</em> (גְּבֶרֶת) is the feminine form of <em>geber</em> (man of strength) — a woman of power and position. She is the <em>mistress</em> of a household or the <em>queen mother</em> in a royal court. In Israel, the <em>gebirah</em> (a related form) was a position of recognized authority in the Davidic monarchy. The word carries dignity, strength, and the responsibility of governance.",
 "The concept of <em>geberet</em> challenges reductive readings of women's roles in the Hebrew Bible. These were not passive figures; the queen mother in Judah held real political influence (see 1 Kings 15:13). More theologically, Hagar uses this word when she looks back at Sarah, her mistress — even in a relationship of hardship, the term signals order and covenant obligation. For the Christian, the church as the bride of Christ carries something of <em>geberet</em> dignity: clothed with honor, positioned for authority, carrying the responsibility of a household entrusted to her care.",
 [
   ("Gen 16:4", "And when she saw that she had conceived, her mistress [geberet] was despised in her eyes."),
   ("Gen 16:9", "The Angel of the LORD said to her, 'Return to your mistress [geberet], and submit yourself under her hand.'"),
   ("Is 47:5", "Sit in silence, and go into darkness, O daughter of the Chaldeans; for you shall no longer be called the <em>Lady</em> [geberet] of Kingdoms."),
   ("Is 47:7", "And you said, 'I shall be a <em>lady</em> [geberet] forever,' so that you did not take these things to heart."),
   ("Ps 123:2", "As the eyes of a maid to the hand of her <em>mistress</em> [geberet], so our eyes look to the LORD our God."),
 ],
 [("H1396","gabar — be mighty/prevail"), ("H1369","geburah — might/power"), ("H4428","melek — king"), ("H8282","sarah — princess/female ruler")]),

("H1454", "H", "גֵּה", "geh", "Pronoun/Particle", "This, that (rare demonstrative)",
 "A rare demonstrative particle meaning 'this' or 'that'; an indicator of immediacy or presence.",
 "<em>Geh</em> (גֵּה) is a rare demonstrative particle — one of the sparingly used pointing words of biblical Hebrew. Like its more common cousins <em>zeh</em> and <em>zot</em>, it indicates the presence or immediacy of something. Its rarity makes its occurrences noteworthy, as Hebrew writers typically chose this particle when ordinary demonstratives might seem insufficient for the weight of the moment.",
 "Even the smallest grammatical particles in Scripture carry theological weight. The act of pointing — 'THIS is the Lord's doing' — is itself an act of faith. When Scripture uses a demonstrative pronoun, it calls the reader to <em>stop and see</em>. The finger points. The eye follows. The heart must respond. In liturgical worship, 'This is the day the LORD has made' (Psalm 118) is a demonstrative act: refusing to let the moment be abstract, insisting on the concrete, present reality of God's action in time and space.",
 [
   ("Ezra 5:4", "Then we spoke to them accordingly, 'What are the names of the men <em>who are constructing</em> this building?'"),
   ("Ps 118:23", "<em>This</em> was the LORD's doing; it is marvelous in our eyes."),
   ("Deut 4:6", "Keep therefore and do them; for <em>this</em> is your wisdom and your understanding in the sight of the nations."),
   ("Ps 48:14", "For <em>this</em> is God, our God forever and ever; He will be our guide even to death."),
   ("Is 25:9", "And it will be said in <em>that</em> day: 'Behold, this is our God; we have waited for Him, and He will save us.'"),
 ],
 [("H2088","zeh — this"), ("H2063","zot — this (fem)"), ("H1931","hu — he/it"), ("H3651","ken — so/thus")]),

("H1480", "H", "גּוּפָה", "gufah", "Feminine Noun", "Body, corpse",
 "The physical body; a corpse; the substance and frame of a person.",
 "<em>Gufah</em> (גּוּפָה) refers to the physical body — both the living frame of a person and the corpse after death. Related to the Aramaic <em>guf</em> and connected to the sense of substance or bulk, this word grounds Hebrew theology in the reality of embodied existence. The body in Scripture is not the prison of the soul; it is the divinely crafted dwelling of the imago Dei.",
 "Hebrew theology was never dualistic in the Greek sense — there is no flight from the body toward a 'purer' spiritual existence. God created the body, called it good, entered it in the incarnation, and promises its resurrection. The dead body (<em>gufah</em>) is not discarded; it awaits the day of restoration. For the man of God who serves in uniform, who disciplines the flesh, who faces the body's mortality in combat or discipline — <em>gufah</em> is a theological anchor: the body matters because God made it, redeems it, and will raise it.",
 [
   ("1 Chr 10:12", "All the valiant men arose and took the <em>body</em> [gufah] of Saul and the bodies of his sons; and they brought them to Jabesh."),
   ("Gen 2:7", "And the LORD God formed man of the dust of the ground and breathed into his nostrils the breath of life."),
   ("Job 19:26", "And after my skin is destroyed, this I know, that in my flesh I shall see God."),
   ("Ps 139:13", "For You formed my inward parts; You covered me in my mother's womb."),
   ("Is 26:19", "Your dead shall live; together with my dead body [gufah] they shall arise."),
 ],
 [("H1320","basar — flesh/body"), ("H6106","etsem — bone/body/self"), ("H5315","nephesh — soul/being"), ("H7307","ruach — spirit/breath")]),

("H1484", "H", "גּוֹר", "gor", "Verb/Noun", "Young of animals; to sojourn, dwell as a stranger",
 "A young animal (cub); also to sojourn or dwell as a foreigner or temporary resident.",
 "<em>Gor</em> (גּוֹר) carries two related meanings in biblical Hebrew. As a noun, it refers to the <em>whelp</em> or <em>cub</em> of a lion or other animal — the young, not-yet-fullgrown offspring. As a verb form of the related root, it speaks to dwelling as a <em>sojourner</em> or <em>stranger</em>. Both images speak to vulnerability: the young animal not yet at full strength, the stranger without the protection of full citizenship.",
 "Both senses of <em>gor/gur</em> illuminate the pilgrim theology of Scripture. Israel was commanded to remember they were sojourners in Egypt — strangers, vulnerable, dependent on God's covenant protection. That memory was to generate compassion for the foreigner among them. Jesus, the Lion of Judah, entered the world as a cub — vulnerable, hunted, dependent on the Father's protection. The church is a community of sojourners (1 Pet 2:11), living as temporary residents in a world that is not their final home. Strength comes not from established status but from covenant belonging.",
 [
   ("Gen 49:9", "Judah is a lion's whelp [gor]; from the prey, my son, you have gone up."),
   ("Nahum 2:11", "Where is the dwelling of the lions, and the feeding place of the young lions [gor], where the lion walked..."),
   ("Lam 4:3", "Even the jackals present their breasts to nurse their young [gor]; but the daughter of my people is cruel."),
   ("Gen 12:10", "Now there was a famine in the land, and Abram went down to Egypt to <em>dwell</em> [gur] there, for the famine was severe."),
   ("Ps 120:5", "Woe is me, that I <em>dwell</em> [gor/gur] in Meshech, that I dwell among the tents of Kedar!"),
 ],
 [("H738","ari — lion"), ("H3715","kephir — young lion"), ("H1616","ger — sojourner/stranger"), ("H8453","toshab — temporary resident")]),

("H1495", "H", "גֵּרְשׁוֹן", "Gershon", "Proper Name", "Expulsion, banishment; 'a stranger there'",
 "A proper name meaning 'expulsion' or 'a stranger there'; firstborn son of Levi.",
 "<em>Gershon</em> (גֵּרְשׁוֹן) is the proper name of Levi's firstborn son and the eponymous ancestor of the Gershonite Levitical clan. The name derives from the root <em>garash</em> (to drive out, expel) or alternatively from <em>ger</em> (stranger) + <em>sham</em> (there) — 'a stranger there.' Both etymologies speak to the condition of exile and foreignness.",
 "That a foundational priestly family should bear a name meaning 'expulsion' or 'stranger there' is theologically profound. The Gershonites were entrusted with carrying the most sacred coverings of the Tabernacle — the curtains, veils, and hangings. Exiles carrying holy things. Strangers tending the dwelling place of God. This is the pattern of biblical ministry: those who know what it is to be expelled, to be foreigners, are precisely those entrusted with the most sacred responsibilities. The church's ministers are most effective when they have not forgotten their own exile from God's presence before grace found them.",
 [
   ("Gen 46:11", "The sons of Levi were Gershon, Kohath, and Merari."),
   ("Num 3:25", "And the duty of the children of <em>Gershon</em> in the tabernacle of meeting included the tabernacle, the tent with its covering."),
   ("Num 4:27", "All the service of the sons of the <em>Gershonites</em>, all their carrying and all their service, shall be coordinated."),
   ("1 Chr 6:1", "The sons of Levi: <em>Gershon</em>, Kohath, and Merari."),
   ("Josh 21:27", "To the children of <em>Gershon</em>, of the families of the Levites, they gave from the half-tribe of Manasseh the city of refuge for the slayer."),
 ],
 [("H3878","Levi — joined"), ("H6944","qodesh — holiness/set-apart"), ("H4908","mishkan — tabernacle/dwelling"), ("H1616","ger — sojourner")]),

("H1520", "H", "גִּלֹּה", "Giloh", "Proper Name", "Exile, uncovering, circle",
 "A city in Judah; name meaning 'exile' or 'uncovering'; home of Ahithophel.",
 "<em>Giloh</em> (גִּלֹּה) is the name of a town in the hill country of Judah. Its significance is largely through its most famous resident: Ahithophel, the brilliant counselor of David who later betrayed him by siding with Absalom. The name likely derives from the root <em>galah</em> (to uncover, reveal, go into exile).",
 "Ahithophel of Giloh is one of Scripture's most poignant tragedies: a man of extraordinary wisdom whose counsel was 'as if one inquired at the oracle of God' (2 Sam 16:23), yet whose loyalty crumbled under the weight of personal grievance (many believe he was Bathsheba's grandfather, making David's sin against Uriah a family wound). <em>Giloh</em> — the city of uncovering — becomes the birthplace of a betrayal that would have destroyed David had God not turned Ahithophel's counsel to foolishness. Psalm 41 likely reflects this moment. The warning: proximity to power and gift of wisdom do not guarantee faithfulness; only covenant love (chesed) sustained by humility does.",
 [
   ("Josh 15:51", "<em>Goshen</em>, Holon, <em>Giloh</em>; eleven cities with their villages."),
   ("2 Sam 15:12", "Then Absalom sent for <em>Ahithophel</em> the Gilonite, David's counselor, from his city."),
   ("2 Sam 23:34", "Eliphelet the son of Ahasbai, the son of the Maachathite, Eliam the son of <em>Ahithophel the Gilonite</em>."),
   ("Ps 41:9", "Even my close friend in whom I trusted, who ate my bread, has lifted his heel against me."),
   ("Prov 11:14", "Where there is no counsel, the people fall; but in the multitude of counselors there is safety."),
 ],
 [("H1540","galah — uncover/exile"), ("H302","Achithophel — brother of foolishness"), ("H1732","David — beloved"), ("H2617","chesed — lovingkindness")]),

("H6739", "H", "צְלָא", "tsela", "Verb (Aramaic)", "To pray, to intercede",
 "To pray; to intercede before God; to bow in supplication (Aramaic form used in Daniel).",
 "<em>Tsela</em> (צְלָא) is the Aramaic equivalent of the Hebrew <em>palal</em>—the act of prayer and intercession. It appears prominently in the book of Daniel, where the prophet's refusal to stop praying this word becomes the crisis point that lands him in the lion's den. The root sense involves bowing, bending, leaning into God in supplication.",
 "Daniel's prayer discipline was so consistent, so public, so defiant of royal decree that it became a capital offense — and the charge stuck because it was simply true: <em>he prays three times a day</em>. No defense needed. <em>Tsela</em> is the word for that kind of prayer — not crisis prayer, not emergency prayer, but the scheduled, deliberate, daily bowing before God that forms the backbone of a faithful life. For the warrior, the minister, the father — <em>tsela</em> is the rhythm that everything else hangs on. When Daniel came out of the lion's den, it wasn't just a miracle of preservation; it was the vindication of a prayer life that kings could not stop.",
 [
   ("Dan 6:10", "Now when Daniel knew that the writing was signed, he went home. And in his upper room, with his windows open toward Jerusalem, he <em>knelt down on his knees three times that day, and prayed</em> [tsela] and gave thanks before his God."),
   ("Dan 6:11", "Then these men assembled and found Daniel <em>praying</em> [tsela] and making supplication before his God."),
   ("Dan 6:13", "That Daniel, who is one of the captives from Judah, does not show due regard for you, O king, or for the decree... but makes his petition [tsela] three times a day."),
   ("Dan 9:4", "And I <em>prayed</em> [tsela] to the LORD my God, and made confession."),
   ("Ezra 6:10", "That they may offer sacrifices of sweet aroma to the God of heaven, and <em>pray</em> [tsela] for the life of the king and his sons."),
 ],
 [("H6419","palal — pray/intercede"), ("H8605","tephillah — prayer"), ("H7812","shachah — bow/worship"), ("H2470","chalah — implore/beseech")]),

("H7834", "H", "שַׁחַק", "shachaq", "Masculine Noun", "Clouds, skies, fine dust, powder",
 "Thin clouds; the expanse of sky; fine dust or powder; the celestial heights where God dwells.",
 "<em>Shachaq</em> (שַׁחַק) refers to the thin upper clouds, the vast expanse of the heavens — the sky as a place of fine, misty substance. It derives from the root meaning 'to pulverize' or 'grind thin,' suggesting the clouds as fine powder scattered across the sky. In poetry, <em>shachaq</em> is where God rides, where He pitches His tent, where the rain is stored.",
 "The theology of <em>shachaq</em> is the theology of God's cosmic home. He dwells between, above, and within the clouds — not absent, but present in a register beyond ordinary sight. When the psalmist asks 'Who is like the LORD?' the answer comes: He sits above the heavens (<em>shachaq</em>), yet stoops down to see. This paradox — infinite height and intimate nearness — is the heartbeat of biblical theology. The warrior who has lain in a field watching the night sky, the preacher who has stared into thunderheads building on the horizon — they are standing at the edge of <em>shachaq</em>, the thin place between the seen and the One who dwells beyond.",
 [
   ("Deut 33:26", "There is no one like the God of Jeshurun, who rides the heavens to your help, and in His excellency on the <em>clouds</em> [shachaq]."),
   ("Ps 89:6", "For who in the <em>heavens</em> [shachaq] can be compared to the LORD? Who among the sons of the mighty can be likened to the LORD?"),
   ("Ps 68:34", "Ascribe strength to God; His excellence is over Israel, and His strength is in the <em>clouds</em> [shachaq]."),
   ("Job 35:5", "Look at the heavens and see; and behold the <em>clouds</em> [shachaq] — they are higher than you."),
   ("Ps 57:10", "For Your mercy reaches unto the heavens, and Your truth unto the <em>clouds</em> [shachaq]."),
 ],
 [("H8064","shamayim — heaven/sky"), ("H6051","anan — cloud"), ("H7834","shachaq — cloud/sky"), ("H7549","raqia — expanse/firmament")]),

("H2587", "H", "חַנּוּן", "channun", "Adjective", "Gracious, compassionate, merciful",
 "Gracious; full of grace and favor; used almost exclusively as an attribute of God.",
 "<em>Channun</em> (חַנּוּן) is one of the most concentrated and important divine attributes in the Hebrew Bible. It means <em>gracious</em> — inclined to show favor freely, to give undeserved goodness. Derived from the root <em>chanan</em> (to be gracious, to show favor), <em>channun</em> appears in the great 'creed' of Exodus 34:6 — the self-disclosure of God after the golden calf debacle — and is echoed in nearly every Old Testament text that describes God's character.",
 "When Moses asked to see God's glory, God revealed His name: <em>Channun</em> — <em>gracious</em>. This is stunning. After Israel had broken covenant with the golden calf, God's defining response was not wrath but an overflow of grace. <em>Channun</em> is not the grace that ignores sin; it is the grace that persists in covenant love despite sin. It always appears alongside <em>rachum</em> (compassionate), <em>erek apayim</em> (slow to anger), and <em>chesed</em> (lovingkindness). Together they form the DNA of God's character. The New Testament answer to 'what is God like?' is Jesus — and Jesus is <em>channun</em> enfleshed.",
 [
   ("Ex 34:6", "And the LORD passed before him and proclaimed, 'The LORD, the LORD God, <em>merciful</em> and <em>gracious</em> [channun], longsuffering, and abounding in goodness and truth.'"),
   ("Ps 103:8", "The LORD is <em>merciful</em> and <em>gracious</em> [channun], slow to anger, and abounding in mercy."),
   ("Ps 111:4", "He has made His wonderful works to be remembered; the LORD is <em>gracious</em> [channun] and full of compassion."),
   ("Ps 116:5", "<em>Gracious</em> [channun] is the LORD, and righteous; yes, our God is merciful."),
   ("Neh 9:17", "But You are God, ready to pardon, <em>gracious</em> [channun] and merciful, slow to anger, abundant in kindness, and did not forsake them."),
 ],
 [("H2580","chen — grace/favor"), ("H7349","rachum — compassionate"), ("H2617","chesed — lovingkindness"), ("H750","arek — slow/patient")]),

("H1935", "H", "הוֹד", "hod", "Masculine Noun", "Majesty, splendor, vigor, glory",
 "Majesty, splendor, honor, vigor; the outward radiance of greatness and excellence.",
 "<em>Hod</em> (הוֹד) describes the outward radiance of majesty — the visible, felt impression of greatness. It is the splendor of a king's presence, the vigor of a warrior's strength, the brilliance of divine glory. <em>Hod</em> is sometimes paired with <em>hadar</em> (honor/majesty) and with <em>kabod</em> (glory), creating an overlapping cluster of words for the overwhelming, beautiful greatness of God and those who reflect Him.",
 "<em>Hod</em> is what you see before you can fully explain it. It is the quality that made David's songs stop people mid-breath, that made Solomon's wisdom leave the Queen of Sheba speechless. When Moses' face shone after meeting God, when the temple filled with cloud and fire — that was <em>hod</em>. Most magnificently, <em>hod</em> is an attribute both given and derived: God's majesty is inherent; the honor He grants to His servants is derived, reflected from the source. Joshua received <em>hod</em> by Moses' hand (Num 27:20). The proper response to <em>hod</em> is worship — because any majesty other than God's is borrowed light.",
 [
   ("Ps 96:6", "Honor and majesty [hod] are before Him; strength and beauty are in His sanctuary."),
   ("Ps 104:1", "O LORD my God, You are very great; You are clothed with honor and <em>majesty</em> [hod]."),
   ("Num 27:20", "And you shall give some of your authority [hod] to him, that all the congregation of the children of Israel may be obedient."),
   ("Job 37:22", "From the north comes golden splendor; with God is awesome <em>majesty</em> [hod]."),
   ("Ps 111:3", "His work is honorable and glorious, and His righteousness endures forever."),
 ],
 [("H1926","hadar — honor/majesty/beauty"), ("H3519","kabod — glory/honor/weight"), ("H6286","paar — glorify/beautify"), ("H8597","tiphereth — beauty/glory")]),

("H6490", "H", "פִּקּוּד", "piqqud", "Masculine Noun", "Precept, mandate, charge",
 "A precept, mandate, or charge; God's appointed orders and specific directives.",
 "<em>Piqqud</em> (פִּקּוּד) refers to God's specific <em>precepts</em> — His detailed, individual mandates and charges. While <em>torah</em> is instruction in broad sweep and <em>mitsvah</em> is commandment, <em>piqqud</em> connotes particular orders, appointed directives, the specific charges given to God's people. Psalm 119 uses it extensively alongside other law-words, showing the psalmist's total delight in every nuance of God's revealed will.",
 "In a military context, <em>piqqud</em> resonates immediately: these are the <em>orders of the day</em>, the standing operating procedures, the commander's intent translated into specific directives. The man who loves God's <em>piqqudim</em> is like the warrior who doesn't just acknowledge the mission brief but commits it to heart, meditates on it, structures his life around it. Psalm 119 returns to <em>piqqud</em> again and again — not as burden but as treasure. 'I love Your precepts more than gold, yes, more than fine gold.' The precept is where love and obedience merge.",
 [
   ("Ps 119:4", "You have commanded us to keep Your <em>precepts</em> [piqqudim] diligently."),
   ("Ps 119:15", "I will meditate on Your <em>precepts</em> [piqqudim], and contemplate Your ways."),
   ("Ps 119:40", "Behold, I long for Your <em>precepts</em> [piqqudim]; revive me in Your righteousness."),
   ("Ps 119:93", "I will never forget Your <em>precepts</em> [piqqudim], for by them You have given me life."),
   ("Ps 19:8", "The statutes of the LORD are right, rejoicing the heart; the commandment of the LORD is pure, enlightening the eyes."),
 ],
 [("H8451","torah — law/instruction"), ("H4687","mitsvah — commandment"), ("H2706","choq — statute/decree"), ("H4941","mishpat — judgment/ordinance")]),

("H1848", "H", "דֹּפִי", "dophi", "Masculine Noun", "Blemish, slander, defect",
 "A blemish, defect, or slander; something that mars or stains reputation or character.",
 "<em>Dophi</em> (דֹּפִי) is a rare word denoting <em>blemish</em> or <em>defect</em> — the stain on what should be pure, the flaw in what should be complete. In its few appearances, it points to the standard of perfection against which blemish is measured. Levitical law required unblemished sacrifices; the absence of <em>dophi</em> was a prerequisite for approaching God's altar.",
 "The theology of <em>dophi</em> is the theology of imputation and atonement. Israel's sacrificial system required animals without <em>dophi</em> because they prefigured the Lamb of God — the One who, being without blemish, could bear the blemish of all. Peter declares Christ was 'a lamb without blemish and without spot' (1 Pet 1:19). The church, in turn, is being prepared as a bride without blemish (Eph 5:27). <em>Dophi</em> — the defect — is what grace removes. The man of God, marked by his own failures and sin, is being brought to the altar of God's own choosing: not for his own perfection, but clothed in the unblemished righteousness of Another.",
 [
   ("Ps 50:20", "You sit and speak against your brother; you slander [dophi] your own mother's son."),
   ("Lev 22:21", "And whoever offers a sacrifice of a peace offering to the LORD, to fulfill his vow... it must be perfect; there shall be no defect [dophi] in it."),
   ("2 Sam 14:25", "Now in all Israel there was no one who was praised as much as Absalom for his good looks... there was no <em>blemish</em> [dophi] in him."),
   ("Song 4:7", "You are all fair, my love, and there is no spot [dophi] in you."),
   ("Job 11:15", "Surely then you could lift up your face without spot [dophi]; yes, you could be steadfast, and not fear."),
 ],
 [("H8549","tamim — complete/blameless"), ("H3971","mum — blemish/defect"), ("H7843","shachat — corrupt/ruin"), ("H2889","tahor — pure/clean")]),

("H3293", "H", "יַעַר", "yaar", "Masculine Noun", "Forest, woodland, thicket",
 "A forest, woods, or dense thicket; the wilderness of trees; a place of wild growth.",
 "<em>Yaar</em> (יַעַר) is the Hebrew word for <em>forest</em> or <em>thicket</em> — the dense, wild growth of trees beyond human cultivation. It appears in military contexts (the forest swallowing more of David's men than the sword), in prophetic imagery (Lebanon's great forest), and in natural descriptions of Israel's varied terrain.",
 "The forest in Scripture is a place of both beauty and danger — untamed, beyond the city's control, a realm where wild animals dwell and armies get lost. The great cedar forests of Lebanon symbolized both prosperity and the pride of nations that would eventually fall (Isaiah 10:18-19). When the psalmist speaks of every animal of the forest belonging to God (Ps 50:10), it is a declaration of universal sovereignty — even the untamed belongs to the Lord. The forest's wildness does not place it beyond His care. For the Christian, <em>yaar</em> speaks to the parts of life that feel untamed, beyond control — and the confidence that even there, in the thicket, God reigns.",
 [
   ("2 Sam 18:8", "For the battle there was scattered over the face of the whole countryside, and the <em>forest</em> [yaar] devoured more people that day than the sword devoured."),
   ("Ps 50:10", "For every beast of the <em>forest</em> [yaar] is Mine, and the cattle on a thousand hills."),
   ("Is 10:18", "And He will consume the glory of his <em>forest</em> [yaar] and of his fruitful field, both soul and body."),
   ("Mic 3:12", "Therefore Zion shall be plowed like a field, Jerusalem shall become heaps of ruins, and the mountain of the temple like the bare hills of the <em>forest</em> [yaar]."),
   ("1 Kings 7:2", "He also built the House of the <em>Forest</em> [yaar] of Lebanon; its length was one hundred cubits."),
 ],
 [("H6086","ets — tree/wood"), ("H2793","choresh — thicket/forest"), ("H4057","midbar — wilderness/desert"), ("H3754","kerem — vineyard")]),

("H3026", "H", "יְגַר שָׂהֲדוּתָא", "Yegar Sahadutha", "Proper Name / Aramaic Phrase", "Heap of witness",
 "Aramaic name meaning 'heap of witness' or 'cairn of testimony'; given by Laban to the covenant cairn.",
 "<em>Yegar Sahadutha</em> is the Aramaic phrase Laban uses to name the stone cairn that marked the covenant between himself and Jacob (Genesis 31). It is the Aramaic equivalent of the Hebrew <em>Galeed</em> — both mean 'heap of witness.' The use of Aramaic here reflects Laban's Syrian (Aramean) background; Jacob uses the Hebrew name for the same pile of stones.",
 "The bilingual naming of the covenant cairn at Mizpah is one of Scripture's most poignant moments: two men who speak different languages, operate from different loyalties, worship different 'gods' — stacking stones as a monument to a covenant neither can fully enforce on his own. 'The LORD watch between you and me when we are absent one from another' (the Mizpah benediction) — often quoted as a blessing, it is actually a warning: since we cannot trust each other, God will be the witness and judge. <em>Yegar Sahadutha</em> is a monument to the limits of human covenant-making — and to God as the only reliable witness and guarantor.",
 [
   ("Gen 31:47", "Laban called it <em>Yegar Sahadutha</em>, but Jacob called it Galeed."),
   ("Gen 31:48", "And Laban said, 'This heap is a witness between you and me today.' Therefore its name was called Galeed."),
   ("Gen 31:49", "Also Mizpah, because he said, 'May the LORD watch between you and me when we are absent one from another.'"),
   ("Gen 31:52", "This heap is a witness, and this pillar is a witness, that I will not pass beyond this heap to you, and you will not pass beyond this heap and this pillar to me, for harm."),
   ("Josh 24:27", "And Joshua said to all the people, 'Behold, this stone shall be a witness to us, for it has heard all the words of the LORD which He spoke to us.'"),
 ],
 [("H1567","Galeed — heap of witness (Hebrew)"), ("H5707","ed — witness"), ("H1285","berit — covenant"), ("H4709","Mitspah — watchtower")]),

("H3029", "H", "יְדָא", "yeda", "Verb (Aramaic)", "To give thanks, praise, confess",
 "Aramaic form of the Hebrew yadah; to give thanks, offer praise, confess with the hand raised.",
 "<em>Yeda</em> (יְדָא) is the Aramaic counterpart to the Hebrew <em>yadah</em> (H3034) — both mean to give thanks, praise, or confess, with the physical sense of extending or raising the hand. This form appears in Daniel and Ezra, written partly in Aramaic, where the act of thanksgiving to God crosses language barriers.",
 "That the Aramaic form of thanksgiving appears in Daniel is no accident. Daniel, living in Babylon, worshipping under a foreign sky, surrounded by pagan power — still gives thanks three times daily. His <em>yeda</em> is not circumstantial; it is covenantal. He thanks God not because his circumstances are good (he is an exile) but because God is good. This is the New Testament theology of 1 Thessalonians 5:18 ('give thanks in all circumstances') worked out in Aramaic, centuries before Paul. The man who can <em>yeda</em> in Babylon has discovered the secret of contentment.",
 [
   ("Dan 2:23", "I thank [yeda] You and praise You, O God of my fathers; You have given me wisdom and might."),
   ("Dan 6:10", "He knelt down on his knees three times that day, and prayed and gave thanks [yeda] before his God."),
   ("Ezra 7:27", "Blessed be the LORD God of our fathers, who has put such a thing as this in the king's heart."),
   ("Ps 107:1", "Oh, give thanks [yadah] to the LORD, for He is good! For His mercy endures forever."),
   ("Col 3:17", "And whatever you do in word or deed, do all in the name of the Lord Jesus, giving thanks to God the Father through Him."),
 ],
 [("H3034","yadah — give thanks/praise"), ("H1984","halal — praise/boast"), ("H8416","tehillah — praise/psalm"), ("H8426","todah — thanksgiving")]),

("H3031", "H", "יִדְּבָשׁ", "Yidbash", "Proper Name", "He will be sweet like honey",
 "A proper name meaning 'he will be sweet' or 'honeyed'; from the root dvash (honey).",
 "<em>Yidbash</em> (יִדְּבָשׁ) is a rare proper name appearing in the genealogies of Judah, derived from the noun <em>devash</em> (honey). The name carries the sweetness of blessing — a father naming his son with the prayer that his life would be as sweet as honey, as rich as the land flowing with milk and honey.",
 "Even in genealogical lists that seem like mere census data, theology runs deep. Honey in Scripture is the taste of God's Word (Ps 119:103: 'How sweet are Your words to my taste, sweeter than honey to my mouth'), the flavor of the Promised Land, the nourishment of the great Jonathan who tasted honey and his eyes brightened. When a family names their son 'honeyed' or 'sweet like honey,' they are expressing a theology of blessing: life under God's covenant is not bitter servitude but the sweetness of a land He has prepared. For the man of God, every day in Scripture is a day of <em>Yidbash</em> — finding the sweetness that the world cannot offer.",
 [
   ("1 Chr 4:3", "These were the sons of Etam: Jezreel, Ishma, and Idbash [Yidbash]..."),
   ("Ps 119:103", "How sweet are Your words to my taste, sweeter than honey to my mouth!"),
   ("Prov 24:13", "My son, eat honey because it is good, and the honeycomb which is sweet to your taste."),
   ("Ex 3:8", "A good and large land, to a land flowing with milk and <em>honey</em> [devash]."),
   ("Ezek 3:3", "And He said to me, 'Son of man, feed your belly, and fill your stomach with this scroll that I give you.' So I ate, and it was in my mouth like <em>honey</em> in sweetness."),
 ],
 [("H1706","devash — honey"), ("H4966","matok — sweet"), ("H5207","nichoach — pleasant/soothing"), ("H2896","tov — good")]),

("H3035", "H", "יִדּוֹ", "Yiddo", "Proper Name", "His hand, his praise",
 "A proper name meaning 'his hand' or 'his praised one'; appearing in Solomon's administrative records.",
 "<em>Yiddo</em> (יִדּוֹ) is a proper name in the Solomonic administrative list (1 Kings 4:14), meaning 'his hand' — the hand of God's provision and appointment. Names connected to the Hebrew word <em>yad</em> (hand) spoke of power, direction, and agency. To be named 'his hand' was to be marked as an instrument of action.",
 "The <em>yad</em> (hand) of God is one of the most important theological metaphors in the Old Testament. It represents power in action — the outstretched hand of deliverance in the Exodus, the hand that formed Adam from the dust, the hand that wrote the law on stone. For a person to be named <em>Yiddo</em> (his hand) is to be named as one appointed for a purpose, an instrument in the hand of a sovereign God. Every believer bears something of this name: called, shaped, and deployed as instruments of God's ongoing action in the world.",
 [
   ("1 Kings 4:14", "<em>Ahinadab</em> the son of Iddo [Yiddo] — in Mahanaim."),
   ("Ezra 5:1", "Then the prophet Haggai and Zechariah the son of Iddo [Yiddo], prophets, prophesied to the Jews who were in Judah and Jerusalem."),
   ("Ps 17:7", "Show Your marvelous lovingkindness by Your right hand [yad], O You who save those who trust in You."),
   ("Is 41:10", "I will strengthen you, yes, I will help you, I will uphold you with My righteous right <em>hand</em> [yad]."),
   ("Ps 31:5", "Into Your <em>hand</em> [yad] I commit my spirit; You have redeemed me, O LORD God of truth."),
 ],
 [("H3027","yad — hand"), ("H3034","yadah — give thanks/praise"), ("H3045","yada — know"), ("H5828","ezer — help/helper")]),

("H3037", "H", "יַדּוּעַ", "Yaddua", "Proper Name", "Known, known of God",
 "A proper name meaning 'known' or 'known one'; from the root yada (to know).",
 "<em>Yaddua</em> (יַדּוּעַ) is a Hebrew proper name derived from <em>yada</em> (to know). It appears among the returnees from Babylonian exile who signed the covenant renewal under Nehemiah, and notably in the Josephus account as the high priest who met Alexander the Great. The name means 'known' — one who is recognized, acknowledged, personally identified.",
 "To be named 'known' in Scripture carries extraordinary theological weight. God says to Jeremiah: 'Before I formed you in the womb I knew you' (<em>yedaaticha</em> — same root). Jesus tells His disciples: 'I know My sheep and am known by My own.' In John 10, the mutual <em>knowing</em> between Shepherd and sheep is the basis of eternal security. To be <em>yaddua</em> — known by God — is not merely to be recognized on a roster; it is to be personally known, intimately chosen, held in the active awareness of the Eternal. The opposite — to hear 'I never knew you' — is the most terrifying sentence in the New Testament.",
 [
   ("Neh 10:21", "<em>Meshezabel</em>, Zadok, <em>Jaddua</em> [Yaddua]..."),
   ("Neh 12:11", "And Joiada begot Jonathan, and Jonathan begot <em>Jaddua</em> [Yaddua]."),
   ("Jer 1:5", "Before I formed you in the womb I <em>knew</em> [yada] you; before you were born I sanctified you."),
   ("John 10:14", "I am the good shepherd; and I <em>know</em> My sheep, and am known by My own."),
   ("Ps 1:6", "For the LORD <em>knows</em> the way of the righteous, but the way of the ungodly shall perish."),
 ],
 [("H3045","yada — know"), ("H1847","daath — knowledge"), ("H3046","yeda — know (Aramaic)"), ("H7200","raah — see/discern")]),

("H3040", "H", "יְדִידָה", "Yedidah", "Proper Name / Adjective", "Beloved, darling, dear one",
 "Beloved; dearly loved; darling; from yadid (beloved/lovely), feminine form.",
 "<em>Yedidah</em> (יְדִידָה) comes from the root <em>yadad</em> (to love, be beloved) and means 'beloved' or 'dear one.' As a proper name, it belongs to the mother of King Josiah — the woman whose name means 'beloved' who raised the most faithful king in the line of David after the golden age. Related to <em>Yedidiah</em> — the name God gave Solomon, meaning 'beloved of the LORD.'",
 "The theology of <em>Yedidah</em> is the theology of divine affection. God is not merely sovereign, not merely just — He is a God who <em>loves</em> and who names His people beloved. Nathan brought the name <em>Yedidiah</em> to the infant Solomon as a sign of God's personal delight in the child. The Song of Songs breathes this same air: <em>dodi</em> (my beloved), <em>yadid</em> (dear one). The New Testament's echo: 'This is My beloved Son, in whom I am well pleased.' The warrior who knows he is God's beloved — not because of performance but because of covenant love — fights from security rather than fear.",
 [
   ("2 Kings 22:1", "Josiah was eight years old when he became king... His mother's name was <em>Jedidah</em> [Yedidah] the daughter of Adaiah of Bozkath."),
   ("2 Sam 12:25", "And He sent word by the hand of Nathan the prophet: So he called his name <em>Jedidiah</em> [Yedidiah], because of the LORD."),
   ("Ps 45:1", "My heart overflows with a <em>good theme</em>; I address my verses to the King; my tongue is the pen of a ready writer."),
   ("Song 2:16", "My beloved [dodi] is mine, and I am his; he browses among the lilies."),
   ("Is 5:1", "Now let me sing to my Well-beloved [yadid] a song of my Beloved regarding His vineyard."),
 ],
 [("H1730","dod — beloved/uncle"), ("H157","ahab — love"), ("H3039","yadid — beloved/dear"), ("H2617","chesed — lovingkindness")]),

("H3041", "H", "יְדִידְיָה", "Yedidyah", "Proper Name", "Beloved of the LORD, God's dear one",
 "A proper name meaning 'beloved of the LORD' or 'dear to Yahweh'; the name God gave Solomon.",
 "<em>Yedidyah</em> (יְדִידְיָה) combines <em>yadid</em> (beloved) with the divine name <em>Yah</em> — 'beloved of the LORD.' It was the name given by God through Nathan the prophet to the infant Solomon, whose name means 'peace' or 'his peace.' The double naming — Solomon publicly, Yedidyah privately between God and the child — signals an intimate covenant of love.",
 "The name <em>Yedidyah</em> is one of the most tender moments in all of David's story. After the devastating sequence of sin, death, and grief that followed the Bathsheba episode, God gives this child a name of pure love. It is not earned or deserved — it is grace. God signals to Nathan: <em>this child is Mine, and I love him.</em> Solomon would carry this name into the construction of the Temple, the writing of Proverbs, Song of Songs, and Ecclesiastes. When he turned away in old age, the tragedy was sharpened: the beloved of the LORD had forgotten Whose beloved he was. For the believer, <em>Yedidyah</em> is the name we bear: beloved of God, called to live from that identity.",
 [
   ("2 Sam 12:25", "And He sent word by the hand of Nathan the prophet: So he called his name <em>Jedidiah</em> [Yedidyah], because of the LORD."),
   ("Ps 127:2", "For so He gives His beloved [yadid] sleep."),
   ("Song 1:13", "My beloved [dod] is to me a sachet of myrrh that lies between my breasts."),
   ("Rom 8:39", "Nor height, nor depth, nor any other created thing, shall be able to separate us from the love of God which is in Christ Jesus our Lord."),
   ("Eph 1:6", "To the praise of the glory of His grace, by which He made us accepted in the Beloved."),
 ],
 [("H3040","Yedidah — beloved (fem)"), ("H1730","dod — beloved"), ("H157","ahab — love"), ("H3068","YHWH — LORD")]),

("H3042", "H", "יְדָיָה", "Yedayah", "Proper Name", "God knows, hand of God",
 "A proper name meaning 'God knows' or 'the hand of God'; borne by multiple priests and Levites.",
 "<em>Yedayah</em> (יְדָיָה) is a Hebrew name borne by multiple priests and leaders in the post-exilic community, appearing prominently in Nehemiah and Chronicles. It combines <em>yada</em> (to know) with <em>Yah</em> — 'God knows' — or alternatively reads as 'hand of God' (<em>yad</em> + <em>Yah</em>).",
 "The priestly families who returned from Babylon bearing names like <em>Yedayah</em> were living testimonies to covenant continuity. Exile had not erased God's knowledge of His people; seventy years of Babylonian captivity had not caused Him to forget the sons of Levi. The name 'God knows' is the opposite of abandonment. When Hagar cried in the wilderness, she named the God who found her <em>El Roi</em> — the God who sees. <em>Yedayah</em> is the same confession: even in exile, even scattered, even forgotten by the world — <em>God knows.</em> He keeps the register of His own. Every name on Nehemiah's covenant-signing list was known to God before it was written on parchment.",
 [
   ("Neh 7:39", "The priests: the children of <em>Jedaiah</em> [Yedayah], of the house of Jeshua, nine hundred and seventy-three."),
   ("1 Chr 9:10", "Of the priests: <em>Jedaiah</em> [Yedayah], Jehoiarib, and Jachin."),
   ("Neh 10:18", "Hodijah, Hashum, Bezai, Hariph, Anathoth, Nebai, <em>Magpiash</em>..."),
   ("Ps 139:1", "O LORD, You have searched me and <em>known</em> [yada] me."),
   ("Nah 1:7", "The LORD is good, a stronghold in the day of trouble; and He <em>knows</em> those who trust in Him."),
 ],
 [("H3045","yada — know"), ("H3027","yad — hand"), ("H3068","YHWH — LORD"), ("H6440","panim — face/presence")]),

# ════════════════════════════════════
# GREEK WORDS (23)
# ════════════════════════════════════

("G3986", "G", "πειρασμός", "peirasmos", "Masculine Noun", "Temptation, trial, testing",
 "A trial, test, or temptation; the proving of faith through difficulty or enticement to sin.",
 "<em>Peirasmos</em> (πειρασμός) carries a dual weight in Greek Scripture: it refers both to external <em>trials</em> that test and refine faith (as in James 1:2 — 'count it all joy when you fall into various trials') and to internal <em>temptations</em> that entice toward sin (as in Matthew 6:13 — 'lead us not into temptation'). The word comes from <em>peirazo</em> (to test, try, tempt). God does not tempt to sin (James 1:13), but He does permit trials that prove faith genuine.",
 "<em>Peirasmos</em> is one of the most important words in the Christian's practical vocabulary. Jesus himself underwent <em>peirasmos</em> — the forty-day wilderness testing by Satan — and emerged victorious, qualifying Him to become the sympathetic High Priest who understands our weakness (Heb 4:15). The Lord's Prayer asks God to not bring us into the <em>peirasmos</em> we cannot bear — a recognition that we are outmatched without divine protection. Yet James promises that surviving <em>peirasmos</em> produces the crown of life. For the warrior, every hard day, every moral crossroads, every spiritual attack is <em>peirasmos</em> — not meaningless suffering, but the proving ground of genuine faith.",
 [
   ("Matt 6:13", "And do not lead us into <em>temptation</em> [peirasmos], but deliver us from the evil one."),
   ("Jas 1:2", "My brethren, count it all joy when you fall into various <em>trials</em> [peirasmos]."),
   ("Jas 1:12", "Blessed is the man who endures <em>temptation</em> [peirasmos]; for when he has been approved, he will receive the crown of life."),
   ("1 Cor 10:13", "No <em>temptation</em> [peirasmos] has overtaken you except such as is common to man; but God is faithful, who will not allow you to be tempted beyond what you are able."),
   ("Luke 22:28", "But you are those who have continued with Me in My <em>trials</em> [peirasmos]."),
 ],
 [("G3985","peirazo — test/tempt"), ("G1382","dokime — proven character"), ("G2347","thlipsis — tribulation"), ("G5281","hupomone — endurance")]),

("G4167", "G", "ποίμνη", "poimne", "Feminine Noun", "Flock, sheepfold",
 "A flock of sheep; the gathered company of the shepherd's care.",
 "<em>Poimne</em> (ποίμνη) is the Greek word for a <em>flock</em> of sheep — the community of animals under a single shepherd's care. In the New Testament it becomes the primary metaphor for the gathered people of God: the church as flock, Christ as Shepherd. Related to <em>poimen</em> (shepherd, H4167) and <em>poimaino</em> (to tend a flock).",
 "Jesus' use of <em>poimne</em> in John 10 is among the most comforting passages in Scripture: 'My sheep hear My voice, and I know them, and they follow Me. And I give them eternal life, and they shall never perish; neither shall anyone snatch them out of My hand.' The flock is defined by its relationship to the Shepherd — knowing His voice, following His lead, protected by His power. Peter takes up this image in his letter to the elders: 'Shepherd the flock of God which is among you.' Every pastor, elder, and spiritual father is an under-shepherd of the <em>poimne</em> that belongs ultimately to Christ.",
 [
   ("John 10:16", "And other sheep I have which are not of this fold; them also I must bring, and they will hear My voice; and there will be one flock [poimne] and one shepherd."),
   ("Luke 12:32", "Do not fear, little flock [poimne], for it is your Father's good pleasure to give you the kingdom."),
   ("Matt 26:31", "Jesus said: All of you will stumble tonight, for it is written: I will strike the Shepherd, and the sheep of the flock [poimne] will be scattered."),
   ("1 Pet 5:2", "Shepherd the flock [poimne] of God which is among you, serving as overseers, not by compulsion but willingly."),
   ("Acts 20:28", "Therefore take heed to yourselves and to all the flock [poimne], among which the Holy Spirit has made you overseers."),
 ],
 [("G4166","poimen — shepherd"), ("G4168","poimnion — little flock"), ("G4165","poimaino — tend/shepherd"), ("G2041","ergon — work/deed")]),

("G2074", "G", "Ἑρωμένη", "Eromene", "Proper Name / Noun", "Beloved, desired one",
 "One who is loved or desired; appears as a name meaning 'beloved.'",
 "<em>Eromene</em> comes from the Greek verb <em>erao</em> — to love with deep desire and longing, a love that seeks union. As a concept, it appears in contexts of deep personal love and longing. The name and concept speak to the theology of divine desire — that God not only loves benevolently (<em>agape</em>) but longs for, pursues, and desires His people.",
 "The full range of Greek love vocabulary — <em>agape</em>, <em>phileo</em>, <em>eros</em> — illuminates different facets of divine love. While <em>eros</em> as a word does not appear in the New Testament, the <em>concept</em> of God's passionate longing for His people runs through the prophets (Hosea, the Song of Songs) and into the New Testament image of the church as Christ's bride, awaiting the marriage supper of the Lamb. The Song of Songs is the canonical text of holy desire — teaching that longing itself, properly ordered toward the ultimate Beloved, is a gift. The warrior who understands <em>eros</em> in its sanctified form — passionate commitment and desire — becomes a better husband, father, and worshipper.",
 [
   ("Song 7:10", "I am my beloved's, and his desire is toward me."),
   ("Hos 2:19", "I will betroth you to Me forever; yes, I will betroth you to Me in righteousness and justice, in lovingkindness and mercy."),
   ("Rev 19:7", "Let us be glad and rejoice and give Him glory, for the marriage of the Lamb has come, and His wife has made herself ready."),
   ("John 3:29", "He who has the bride is the bridegroom; but the friend of the bridegroom, who stands and hears him, rejoices greatly because of the bridegroom's voice."),
   ("Eph 5:25", "Husbands, love your wives, just as Christ also loved the church and gave Himself for her."),
 ],
 [("G26","agape — love"), ("G5368","phileo — love/be fond of"), ("G3565","numphe — bride"), ("G3566","numphios — bridegroom")]),

("G2075", "G", "ἐστέ", "este", "Verb", "You are (plural present indicative of eimi)",
 "You are; the second-person plural present indicative of the verb 'to be.'",
 "<em>Este</em> (ἐστέ) is the plural form of <em>eimi</em> (to be) — simply 'you are.' Though grammatically ordinary, in the New Testament it carries immense theological freight. Jesus and the apostles use this form to declare identity-transforming truths over communities of believers: 'You are the light of the world. You are the salt of the earth. You are a royal priesthood.'",
 "The declarative <em>este</em> is one of Scripture's primary instruments of identity transformation. It does not say 'try to become' or 'work toward being' — it says <em>you are.</em> The indicative mood precedes the imperative: first God declares what you are in Christ, then He calls you to live from that reality. 'You are the light of the world' — therefore let your light shine. 'You are a royal priesthood' — therefore offer spiritual sacrifices. The Gospel order is grace before command, identity before behavior. <em>Este</em> is the grammar of the new creation.",
 [
   ("Matt 5:13", "You <em>are</em> [este] the salt of the earth; but if the salt loses its flavor, how shall it be seasoned?"),
   ("Matt 5:14", "You <em>are</em> [este] the light of the world. A city that is set on a hill cannot be hidden."),
   ("John 15:3", "You <em>are</em> [este] already clean because of the word which I have spoken to you."),
   ("1 Pet 2:9", "But you <em>are</em> [este] a chosen generation, a royal priesthood, a holy nation, His own special people."),
   ("1 Cor 3:16", "Do you not know that you <em>are</em> [este] the temple of God and that the Spirit of God dwells in you?"),
 ],
 [("G1510","eimi — I am/to be"), ("G1096","ginomai — become"), ("G2937","ktisis — creation"), ("G1577","ekklesia — church/assembly")]),

("G2076", "G", "ἐστί", "esti", "Verb", "He/she/it is (third-person singular of eimi)",
 "He is, she is, it is; the third-person singular present indicative of eimi (to be).",
 "<em>Esti</em> (ἐστί) is simply 'he is' or 'it is' — the basic being-verb in third-person singular. Yet in Scripture, this small word carries the weight of the universe when it appears in the 'I AM' declarations of Jesus, the ontological statements about God, and the identity declarations about Christ.",
 "When John writes 'God is love' (<em>ho theos agape estin</em>) or 'God is light' (<em>ho theos phos estin</em>), every word matters — and <em>estin</em> (the full form of <em>esti</em>) is the copula that links the Creator's identity to His essential attributes. These are not descriptions of what God does; they are declarations of what God <em>is.</em> Ontology precedes function. In the same vein, 'Jesus is Lord' (<em>Kurios Iesous estin</em>) — the core confession of the early church — rests on this verb. Three syllables. The whole Gospel.",
 [
   ("John 4:24", "God <em>is</em> [estin] Spirit, and those who worship Him must worship in spirit and truth."),
   ("1 John 1:5", "This is the message which we have heard from Him and declare to you: that God <em>is</em> [estin] light and in Him is no darkness at all."),
   ("1 John 4:8", "He who does not love does not know God, for God <em>is</em> [estin] love."),
   ("Phil 2:11", "And that every tongue should confess that Jesus Christ <em>is</em> [estin] Lord, to the glory of God the Father."),
   ("John 11:25", "Jesus said to her, 'I am the resurrection and the life. He who believes in Me, though he may die, he shall live.'"),
 ],
 [("G1510","eimi — I am/to be"), ("G2075","este — you are (pl)"), ("G2316","theos — God"), ("G2962","kurios — Lord")]),

("G2077", "G", "ἔστω", "esto", "Verb", "Let it be, let him/her be (imperative of eimi)",
 "Let it be; let there be; the imperative mood of eimi (to be), commanding existence or state.",
 "<em>Esto</em> (ἔστω) is the imperative form of <em>eimi</em> — 'let it be' or 'let him be.' It is the mood of command applied to existence and state. Jesus uses it in the Sermon on the Mount: 'Let your yes be yes and your no be no' — <em>esto</em> applied to integrity. James echoes it: 'Let every man be swift to hear' (James 1:19). It is the grammar of divine command over human character.",
 "The imperative of being — 'let it be so' — is the grammar of both creation and sanctification. God said '<em>Let there be light</em>' at creation. He says to His people: 'Let your light so shine.' The command is not to manufacture light from scratch; it is to let what is already true by grace become visible in action. <em>Esto</em> is the bridge between indicative and imperative — between what God has declared and what He calls us to embody. For the warrior: let your word be your bond. Let your 'yes' be yes. Let your yes be yes.",
 [
   ("Matt 5:37", "But let your 'Yes' <em>be</em> [esto] 'Yes,' and your 'No,' 'No.'"),
   ("Jas 1:19", "So then, my beloved brethren, let every man <em>be</em> [esto] swift to hear, slow to speak, slow to wrath."),
   ("1 Tim 3:2", "A bishop then must <em>be</em> [esto] blameless, the husband of one wife, temperate, sober-minded."),
   ("1 Cor 16:13", "Watch, stand fast in the faith, <em>be</em> brave, <em>be</em> strong."),
   ("Eph 4:32", "And <em>be</em> [este] kind to one another, tenderhearted, forgiving one another."),
 ],
 [("G1510","eimi — to be"), ("G2075","este — you are"), ("G2316","theos — God"), ("G2889","kosmos — world/order")]),

("G2084", "G", "ἑτερόγλωσσος", "heteroglossos", "Adjective", "Speaking another language, foreign-tongued",
 "Speaking in another tongue or foreign language; of a different language group.",
 "<em>Heteroglossos</em> (ἑτερόγλωσσος) combines <em>heteros</em> (other/different) + <em>glossa</em> (tongue/language). Paul uses it in 1 Corinthians 14 when quoting Isaiah 28 — 'by men of strange tongues and foreign lips I will speak to this people.' It stands at the center of one of the most complex discussions in the New Testament: the nature, purpose, and order of glossolalia (speaking in tongues).",
 "Paul's argument in 1 Corinthians 14 is subtle and pastoral. God's design for speaking in unknown tongues (<em>heteroglossos</em>) is not chaos or self-display but the ordered, interpreted, loving communication that builds up the body. The Pentecost event of Acts 2 is <em>heteroglossos</em> in its most evangelistic form: foreigners hearing the mighty works of God in their own dialects. The Corinthian abuse was <em>heteroglossos</em> without interpretation — unintelligible even to other believers. The principle Paul establishes is still the plumb line for every Christian gathering: does it build up? Does it communicate? Does love govern its expression?",
 [
   ("1 Cor 14:21", "In the law it is written: 'With men of other tongues [heteroglossos] and other lips I will speak to this people; and yet, for all that, they will not hear Me,' says the Lord."),
   ("Acts 2:4", "And they were all filled with the Holy Spirit and began to speak with other tongues, as the Spirit gave them utterance."),
   ("1 Cor 14:2", "For he who speaks in a tongue does not speak to men but to God, for no one understands him."),
   ("1 Cor 14:5", "I wish you all spoke with tongues, but even more that you prophesied."),
   ("Is 28:11", "For with stammering lips and another tongue He will speak to this people."),
 ],
 [("G1100","glossa — tongue/language"), ("G4395","propheteuo — prophesy"), ("G3177","methermeneuo — interpret/translate"), ("G3619","oikodome — building up/edification")]),

("G2103", "G", "Εὔβουλος", "Euboulos", "Proper Name", "Good counsel, well-advised",
 "A proper name meaning 'good counsel' or 'well-advised'; a believer greeting Timothy.",
 "<em>Euboulos</em> (Εὔβουλος) combines <em>eu</em> (well/good) + <em>boule</em> (counsel/will/purpose). As a proper name, it belongs to a believer in Rome who sends greetings to Timothy in Paul's final letter (2 Tim 4:21). The name means 'one of good counsel' — a wise advisor, a man of sound judgment.",
 "That <em>Euboulos</em> appears only once in Scripture — in Paul's last letter, sending greetings from Rome as winter approaches and Paul faces execution — gives the name a poignant weight. He is one of the faithful remnant who remained with Paul when others had abandoned him. His name, 'good counsel,' speaks to what the persevering church most needs: not inspiration alone, but wisdom. The Hebrew <em>Wise Man</em> tradition (Proverbs, Ecclesiastes) insists that true wisdom is not academic achievement but the fear of the LORD applied to daily life. <em>Euboulos</em> — the well-counseled man — is the fruit of that wisdom.",
 [
   ("2 Tim 4:21", "<em>Eubulus</em> greets you, as well as Pudens, Linus, Claudia, and all the brethren."),
   ("Prov 11:14", "Where there is no counsel, the people fall; but in the multitude of counselors there is safety."),
   ("Prov 15:22", "Without counsel, plans go awry, but in the multitude of counselors they are established."),
   ("Jas 1:5", "If any of you lacks wisdom, let him ask of God, who gives to all liberally and without reproach, and it will be given to him."),
   ("Col 1:9", "...asking that you may be filled with the knowledge of His will in all wisdom and spiritual understanding."),
 ],
 [("G1012","boule — counsel/will"), ("G4678","sophia — wisdom"), ("G5428","phronesis — prudence"), ("G3563","nous — mind")]),

("G2105", "G", "εὐδία", "eudia", "Feminine Noun", "Fair weather, clear sky, calm",
 "Fair weather, serene sky, calmness; the settled, clear condition of the atmosphere.",
 "<em>Eudia</em> (εὐδία) combines <em>eu</em> (well/good) + <em>dios</em> (of Zeus/sky/divine) — literally 'good sky' or 'fair weather.' Jesus uses this word in His rebuke of the Pharisees who could read the evening sky for fair weather but could not discern the signs of the times. It appears only in Matthew 16:2 in the New Testament.",
 "Jesus' use of <em>eudia</em> is a lesson in spiritual discernment. The Pharisees were skilled at reading atmospheric signs — red sky at night, sailor's delight. But they were willfully blind to the signs of the Messianic age unfolding before them. <em>Eudia</em> — fair weather — becomes an ironic contrast to the spiritual storm they were ignoring. The point: the same mental capacity used to predict tomorrow's weather must be applied with even greater diligence to the signs of God's kingdom movement. For the believer, discernment is not mysticism; it is careful, prayerful attention to what God is doing in the world.",
 [
   ("Matt 16:2", "He answered and said to them, 'When it is evening you say, "It will be <em>fair weather</em> [eudia], for the sky is red."'"),
   ("Matt 16:3", "'And in the morning, "It will be foul weather today, for the sky is red and threatening." Hypocrites! You know how to discern the face of the sky, but you cannot discern the signs of the times.'"),
   ("Luke 12:54", "He also said to the multitudes, 'When you see a cloud rising out of the west, immediately you say, "A shower is coming"; and so it is.'"),
   ("1 Chr 12:32", "...the sons of Issachar who had understanding of the times, to know what Israel ought to do."),
   ("Heb 5:14", "But solid food belongs to those who are of full age, that is, those who by reason of use have their senses exercised to discern both good and evil."),
 ],
 [("G2540","kairos — appointed time/season"), ("G3739","hos — who/which"), ("G4592","semeion — sign/miracle"), ("G1253","diakrisis — discernment")]),

("G2110", "G", "εὐεργέτης", "euergetes", "Masculine Noun", "Benefactor, one who does good",
 "A benefactor; one who does good to others; a title used by Gentile rulers and ironically by Jesus.",
 "<em>Euergetes</em> (εὐεργέτης) combines <em>eu</em> (well) + <em>ergon</em> (work/deed) — 'well-doer' or benefactor. In the Greco-Roman world, it was an honorific title given to powerful patrons, kings, and public figures who used their influence and wealth to benefit others. Jesus subverts this cultural dynamic in Luke 22:25, using <em>euergetes</em> ironically to describe the Gentile power model before calling His disciples to servant leadership.",
 "Jesus' redefinition of greatness in Luke 22:25-26 is one of the most counter-cultural moments in the Gospels. The Gentile kings call themselves <em>Euergetes</em> — Benefactors — using their giving to establish status and patron-client relationships that obligate the recipients. Jesus says: 'Not so among you.' The kingdom inverts the power pyramid. The greatest is the one who serves. The one who rules is the one who takes last place. True <em>euergesia</em> (benefaction) in the kingdom is not status-building gift-giving; it is cross-bearing, self-emptying service that expects nothing in return. Jesus is the ultimate <em>Euergetes</em> — and He washed feet to prove it.",
 [
   ("Luke 22:25", "And He said to them, 'The kings of the Gentiles exercise lordship over them, and those who exercise authority over them are called <em>benefactors</em> [euergetes].'"),
   ("Acts 10:38", "How God anointed Jesus of Nazareth with the Holy Spirit and with power, who went about doing good [euergeteo] and healing all who were oppressed by the devil."),
   ("Matt 20:26", "Yet it shall not be so among you; but whoever desires to become great among you, let him be your servant."),
   ("Phil 2:7", "But made Himself of no reputation, taking the form of a bondservant, and coming in the likeness of men."),
   ("Mark 10:45", "For even the Son of Man did not come to be served, but to serve, and to give His life a ransom for many."),
 ],
 [("G2041","ergon — work/deed"), ("G18","agathos — good"), ("G1248","diakonia — service/ministry"), ("G1249","diakonos — servant/deacon")]),

("G2111", "G", "εὔθετος", "euthetos", "Adjective", "Well-placed, fit, suitable, proper",
 "Well-placed, fit for use, suitable; properly set or arranged for a purpose.",
 "<em>Euthetos</em> (εὔθετος) combines <em>eu</em> (well) + <em>tithemi</em> (to place/set) — 'well-placed' or 'fit.' It appears in Jesus' sobering statement about the one who puts his hand to the plow and looks back: he is not 'fit' (<em>euthetos</em>) for the kingdom. It also describes land fit for cultivation and the salt that has not lost its savor.",
 "Jesus' use of <em>euthetos</em> is an urgent call to wholehearted commitment. The image of the plowman who looks backward is viscerally practical: a plow pulled by a distracted driver goes crooked. The field is ruined. The work is wasted. 'Fit for the kingdom' (<em>euthetos eis ten basileian</em>) describes the person whose orientation is entirely forward — not because the past is forgotten but because the future is more compelling. Lot's wife looked back. The disciples Jesus called left their nets and followed. <em>Euthetos</em> is the quality of the fully committed: placed well, set right, aimed toward the goal.",
 [
   ("Luke 9:62", "But Jesus said to him, 'No one, having put his hand to the plow, and looking back, is <em>fit</em> [euthetos] for the kingdom of God.'"),
   ("Luke 14:35", "It is neither <em>fit</em> [euthetos] for the land nor for the dunghill, but men throw it out."),
   ("Heb 6:7", "For the earth which drinks in the rain that often comes upon it, and bears herbs <em>useful</em> [euthetos] for those by whom it is cultivated, receives blessing from God."),
   ("Phil 3:13", "Forgetting those things which are behind and reaching forward to those things which are ahead."),
   ("2 Tim 2:21", "...he will be a vessel for honor, sanctified and useful [euchrestos] for the Master, prepared for every good work."),
 ],
 [("G2117","euthus — straight/immediately"), ("G5117","topos — place"), ("G2570","kalos — good/excellent"), ("G18","agathos — good")]),

("G2113", "G", "εὐθυδρομέω", "euthudromeo", "Verb", "To run a straight course, sail directly",
 "To sail in a straight course; to run or travel directly without deviation.",
 "<em>Euthudromeo</em> (εὐθυδρομέω) combines <em>euthus</em> (straight) + <em>dromos</em> (course/race/running). In Acts, it describes the direct, favorable sailing of Paul's missionary voyages — when the wind was right and the ship made a straight run. It is the nautical word for unimpeded, direct progress.",
 "The use of <em>euthudromeo</em> in Acts is almost casually practical — a sailing log entry — but it opens into profound spiritual metaphor. Paul's missionary journeys were guided by the Holy Spirit: 'the Spirit did not permit them' to go one way, 'Come over to Macedonia' sent them another. When the sailing was straight (<em>euthudromeo</em>), it was because God's wind was in the sails. The image of sailing directly to a destination — no detours, no storms, no delays — is the image of a life perfectly aligned with God's will. Most lives have more tacking and storm than straight sailing; the Apostle's confidence was that even the indirect routes were purposeful. But when <em>euthudromeo</em> comes, you recognize it: Spirit-wind in the sails, harbor in sight.",
 [
   ("Acts 16:11", "Therefore, sailing from Troas, we ran a straight course [euthudromeo] to Samothrace."),
   ("Acts 21:1", "Now it came to pass that when we had departed from them and set sail, running a straight course [euthudromeo] we came to Cos."),
   ("Ps 5:8", "Lead me, O LORD, in Your righteousness... make Your way straight before my face."),
   ("Prov 3:6", "In all your ways acknowledge Him, and He shall direct [yashar] your paths."),
   ("Heb 12:1", "Let us run with endurance the race that is set before us."),
 ],
 [("G2117","euthus — straight"), ("G1408","dromos — course/race"), ("G4144","poreia — journey"), ("G3598","hodos — way/road/path")]),

("G2115", "G", "εὔθυμος", "euthumos", "Adjective", "Cheerful, in good spirits, of good courage",
 "Cheerful, in good spirits, of good courage; heartened rather than despairing.",
 "<em>Euthumos</em> (εὔθυμος) combines <em>eu</em> (well) + <em>thumos</em> (spirit/passion/heart-fire) — 'well-spirited,' in good heart. In Acts 27, Paul uses this word in the midst of one of the most terrifying maritime crises in the New Testament — a two-week storm threatening to destroy the ship: 'Therefore take heart (<em>euthumein</em>), for I believe God.'",
 "Paul's command to <em>euthumos</em> in the storm is not denial, not toxic positivity, not forced cheerfulness. The ship is in real danger. Lives are at risk. Fourteen days without food. And yet — <em>take heart.</em> The basis is not the weather report; it is the angel's word: 'God has granted you all those who sail with you.' Courage and cheerfulness rooted in divine promise, held in defiance of circumstances — this is biblical <em>euthumos</em>. It is the quality of the warrior who has seen enough of God's faithfulness to face the storm without despair. Not immune to fear, but not governed by it.",
 [
   ("Acts 27:22", "And now I urge you to take heart [euthumein], for there will be no loss of life among you, but only of the ship."),
   ("Acts 27:25", "Therefore take heart [euthumein], men, for I believe God that it will be just as it was told me."),
   ("Acts 27:36", "Then they were all <em>encouraged</em> [euthumoi] and also took food themselves."),
   ("Phil 4:11", "Not that I speak in regard to need, for I have learned, in whatever state I am, to be content."),
   ("2 Cor 5:6", "So we are always <em>confident</em> [tharrhountes], knowing that while we are at home in the body we are absent from the Lord."),
 ],
 [("G2293","tharsheo — take courage"), ("G3115","makrothumia — patience/longsuffering"), ("G5479","chara — joy"), ("G1515","eirene — peace")]),

("G2118", "G", "εὐθύτης", "euthutes", "Feminine Noun", "Straightness, uprightness, equity",
 "Straightness, uprightness; the quality of being morally direct and equitable.",
 "<em>Euthutes</em> (εὐθύτης) is the noun form of <em>euthus</em> (straight) — <em>straightness</em> or <em>uprightness</em>. In Hebrews 1:8, quoting Psalm 45, it appears in the declaration about Christ's kingdom: 'A scepter of righteousness is the scepter of Your kingdom; You have loved righteousness and hated lawlessness — therefore God has anointed You.' The word describes the perfect moral rectitude of the Messiah-King's rule.",
 "Psalm 45 is a royal wedding psalm that the author of Hebrews reads as Messianic — the divine king whose reign is characterized by absolute moral <em>euthutes</em> (straightness). There is no deviation in Christ's rule, no shadow of favoritism, no crooked judgment. His scepter (<em>rhabdos</em>) is the scepter of righteousness. This is both comfort and challenge: comfort, because the King is incorruptible; challenge, because those who serve in His kingdom are called to the same uprightness. The warrior who bends the rules for personal advantage, the elder who favors the wealthy — both violate the <em>euthutes</em> that marks the kingdom of Christ.",
 [
   ("Heb 1:8", "But to the Son He says: 'Your throne, O God, is forever and ever; a scepter of righteousness is the scepter of Your kingdom... therefore God, Your God, has anointed You with the oil of gladness more than Your companions.'"),
   ("Ps 45:6", "Your throne, O God, is forever and ever; a scepter of <em>uprightness</em> is the scepter of Your kingdom."),
   ("Prov 11:3", "The integrity of the upright will guide them, but the perversity of the unfaithful will destroy them."),
   ("Ps 25:21", "Let integrity and uprightness preserve me, for I wait for You."),
   ("Amos 5:24", "But let justice run down like water, and righteousness like a mighty stream."),
 ],
 [("G2117","euthus — straight"), ("G1343","dikaiosune — righteousness"), ("G1342","dikaios — just/righteous"), ("G93","adikia — unrighteousness")]),

("G2136", "G", "Εὐοδία", "Euodia", "Proper Name", "Good journey, prosperity, success",
 "A proper name meaning 'good journey' or 'prosperous way'; a woman in the Philippian church.",
 "<em>Euodia</em> (Εὐοδία) combines <em>eu</em> (good/well) + <em>hodos</em> (way/road/journey) — 'good journey' or 'prosperous way.' She is one of two women in the Philippian church whom Paul urges to reconcile in Philippians 4:2 — two co-workers in the Gospel who had fallen into conflict. The irony: a woman named 'Good Journey' was stuck in a relational impasse.",
 "Paul's gentle but direct appeal to Euodia and Syntyche is one of Scripture's most pastoral moments on conflict resolution. These were not marginal troublemakers; they were women who 'labored with me in the gospel' — genuine co-workers, trusted partners in mission. Their conflict was real enough to merit mention in a canonical letter read publicly to the whole church. <em>Euodia</em> — good journey — is a reminder that the most gifted, the most faithful, the most fruitful servants of God can still get stuck. The path forward is the same for all: humility, reconciliation, the peace that passes understanding.",
 [
   ("Phil 4:2", "I implore <em>Euodia</em> and I implore Syntyche to be of the same mind in the Lord."),
   ("Phil 4:3", "And I urge you also, true companion, help these women who labored with me in the gospel."),
   ("Matt 5:23", "Therefore if you bring your gift to the altar, and there remember that your brother has something against you... first be reconciled to your brother."),
   ("Rom 12:18", "If it is possible, as much as depends on you, live peaceably with all men."),
   ("Eph 4:3", "Endeavoring to keep the unity of the Spirit in the bond of peace."),
 ],
 [("G3598","hodos — way/road"), ("G1515","eirene — peace"), ("G3675","homothumadon — of one accord"), ("G4795","suntugchano — meet together")]),

("G2138", "G", "εὐμετάδοτος", "eumetadotos", "Adjective", "Ready to share, generous, liberal in giving",
 "Readily sharing, generous; inclined to give freely and liberally.",
 "<em>Eumetadotos</em> (εὐμετάδοτος) combines <em>eu</em> (well) + <em>metadidomi</em> (to share, give a portion of) — 'readily sharing' or 'generous.' Paul uses it in 1 Timothy 6:18 as part of his instruction to the wealthy: they are to be generous (<em>eumetadotos</em>) and ready to share (<em>koinonikos</em>). It captures the disposition of the cheerful giver — not one who gives grudgingly but one who <em>leans toward</em> generosity as a natural instinct.",
 "The theology of <em>eumetadotos</em> is the theology of overflow. Paul grounds his instruction to the wealthy not in guilt but in reality: they are 'rich in this present age' — a fact that carries responsibility. Those who have received abundantly from God's generosity are called to embody that same generous disposition toward others. 2 Corinthians 9:7 grounds this in the character of God: 'God loves a cheerful giver.' <em>Eumetadotos</em> is not the heroism of forced sacrifice; it is the natural expression of a heart that has grasped how much it has received and holds nothing with a clenched fist.",
 [
   ("1 Tim 6:18", "Let them do good, that they be rich in good works, ready to give, willing to share [eumetadotos]."),
   ("2 Cor 9:7", "So let each one give as he purposes in his heart, not grudgingly or of necessity; for God loves a cheerful giver."),
   ("Luke 12:33", "Sell what you have and give alms; provide yourselves money bags which do not grow old."),
   ("Acts 4:34", "Nor was there anyone among them who lacked; for all who were possessors of lands or houses sold them."),
   ("Prov 11:24", "There is one who scatters, yet increases more; and there is one who withholds more than is right, but it leads to poverty."),
 ],
 [("G3330","metadidomi — share/give"), ("G1656","eleos — mercy"), ("G5485","charis — grace"), ("G18","agathos — good")]),

("G2141", "G", "εὐπορέω", "euporeo", "Verb", "To prosper, be well-off, have abundance",
 "To be prosperous, to have abundance; to be well-resourced and able to give.",
 "<em>Euporeo</em> (εὐπορέω) comes from <em>eu</em> (well) + <em>poros</em> (passage/resource/means) — to have a good passage, to be well-provided for. In Acts 11:29, it describes the disciples sending relief to their brethren in Judea: 'each according to his ability [euporeo].' It is the word of proportional generosity — not everyone gives the same amount, but everyone gives from what they have.",
 "The Antioch church's response to the Judean famine (Acts 11) is a model of the early church at its best: Gentile converts, newly grafted into the covenant people, immediately sending relief to the Jewish believers in Jerusalem. The word <em>euporeo</em> preserves the beautiful principle: 'each according to his ability.' Not equal giving but equal sacrifice of proportion. This is why Jesus praised the widow's mite above the rich men's large gifts — not the amount but the proportion and the heart behind it. The prosperous Christian is called to ask not 'how much must I give?' but 'how much can I give?' — because <em>euporeo</em> is a gift that carries responsibility.",
 [
   ("Acts 11:29", "Then the disciples, each according to his ability [euporeo], determined to send relief to the brethren dwelling in Judea."),
   ("2 Cor 8:12", "For if there is first a willing mind, it is accepted according to what one has, and not according to what he does not have."),
   ("Luke 21:4", "For all these out of their abundance have put in offerings for God, but she out of her poverty put in all the livelihood that she had."),
   ("Prov 3:9", "Honor the LORD with your possessions, and with the firstfruits of all your increase."),
   ("Mal 3:10", "Bring all the tithes into the storehouse... and try Me now in this, says the LORD."),
 ],
 [("G4050","perisseia — abundance"), ("G4052","perisseuo — abound/overflow"), ("G2162","euphemia — good report"), ("G5485","charis — grace")]),

("G2142", "G", "εὐπορία", "euporia", "Feminine Noun", "Prosperity, wealth, good means",
 "Prosperity, wealth, abundance; the condition of having good resources and means.",
 "<em>Euporia</em> (εὐπορία) is the noun form of <em>euporeo</em> — the state of prosperity, the condition of being well-resourced. It appears in Acts 19:25, where Demetrius the silversmith rallies his craftsmen with the warning that Paul's preaching threatens 'our prosperity' — the economic engine of the Artemis-idol trade.",
 "The single occurrence of <em>euporia</em> in the New Testament places it in the mouth of a man defending an idol-economy against the Gospel. Demetrius' prosperity depends on people believing that the goddess Artemis is real and worth worshipping in silver form. Paul's message that 'gods made with hands are no gods' (<em>Acts 19:26</em>) threatens not just theology but commerce. This is the eternal collision: the Gospel confronts every <em>euporia</em> built on false gods. Whether ancient Ephesus or modern consumer culture, the question remains — what is your prosperity built on? The idols of any age are exactly as durable as the wealth they generate: crumble when the Truth arrives.",
 [
   ("Acts 19:25", "He called them together with the workers of similar occupation, and said: 'Men, you know that we have our <em>prosperity</em> [euporia] by this trade.'"),
   ("1 Tim 6:6", "Now godliness with contentment is great gain."),
   ("Luke 12:15", "Take heed and beware of covetousness, for one's life does not consist in the abundance of the things he possesses."),
   ("Prov 23:4", "Do not overwork to be rich; because of your own understanding, cease!"),
   ("Matt 6:33", "But seek first the kingdom of God and His righteousness, and all these things shall be added to you."),
 ],
 [("G4149","ploutos — wealth/riches"), ("G4148","ploutizo — make rich"), ("G2041","ergon — work"), ("G2316","theos — God")]),

("G2143", "G", "εὐπρέπεια", "euprepeia", "Feminine Noun", "Comeliness, beauty, good appearance",
 "Comeliness, beauty of appearance, outward grace and elegance.",
 "<em>Euprepeia</em> (εὐπρέπεια) combines <em>eu</em> (well) + <em>prepo</em> (to be fitting/to look well) — 'good appearance' or 'comeliness.' It appears in James 1:11, describing the beauty of the flower that the scorching heat withers: 'its <em>euprepeia</em> (beautiful appearance) perishes.' James uses it to illustrate the transience of the rich man's glory.",
 "James' single use of <em>euprepeia</em> is a masterclass in transience theology. The flower is genuinely beautiful — James does not deny it. But the same sun that causes it to bloom also causes it to wither. Outward beauty, worldly glory, social status, financial prominence — these are real, and they carry their own kind of joy. But they are <em>euprepeia</em>: surface beauty that does not survive the heat of hardship, time, or eternity. The wisdom James is teaching: do not let <em>euprepeia</em> determine your investments. Root yourself in what cannot be scorched. 'The rich man also will fade away in his pursuits' — but the one who endures temptation receives the crown of life.",
 [
   ("Jas 1:11", "For no sooner has the sun risen with a burning heat than it withers the grass; its flower falls, and its beautiful appearance [euprepeia] perishes. So the rich man also will fade away in his pursuits."),
   ("1 Pet 1:24", "For all flesh is as grass, and all the glory of man as the flower of the grass. The grass withers, and its flower falls away."),
   ("Prov 31:30", "Charm is deceitful and beauty is passing, but a woman who fears the LORD, she shall be praised."),
   ("Is 40:8", "The grass withers, the flower fades, but the word of our God stands forever."),
   ("Matt 6:19", "Do not lay up for yourselves treasures on earth, where moth and rust destroy."),
 ],
 [("G2566","kallion — better/more beautiful"), ("G2889","kosmos — world/adornment"), ("G5613","hos — like/as"), ("G5351","phtheiro — corrupt/destroy")]),

("G2146", "G", "εὐπροσωπέω", "euprosopeo", "Verb", "To make a fair show, look good outwardly",
 "To make a fair showing, to look good in outward appearance; to present an impressive face.",
 "<em>Euprosopeo</em> (εὐπροσωπέω) combines <em>eu</em> + <em>prosopon</em> (face/person) — to make a fair face, to appear impressive. Paul uses this rare word in Galatians 6:12 as a critique of those who compel circumcision 'that they may make a good showing [euprosopeo] in the flesh' — performing religious conformity for social approval rather than genuine faith.",
 "Paul's use of <em>euprosopeo</em> cuts to the heart of religious performance. The Judaizers in Galatia were not motivated primarily by theology; they were motivated by social pressure — they wanted to <em>look good</em> before their Jewish peers. They were using the Galatian converts as trophies of compliance. This is the perennial temptation of religious culture: to pursue the appearance of faithfulness more than its substance. Jesus called this hypocrisy — doing righteousness 'before men to be seen by them' (Matt 6:1). The antidote is not less religion but more Gospel: acting from gratitude toward God rather than performing for human approval.",
 [
   ("Gal 6:12", "As many as desire to make a good showing [euprosopeo] in the flesh, these would compel you to be circumcised, only that they may not suffer persecution for the cross of Christ."),
   ("Matt 6:1", "Take heed that you do not do your charitable deeds before men, to be seen by them."),
   ("Matt 23:27", "Woe to you, scribes and Pharisees, hypocrites! For you are like whitewashed tombs which indeed appear beautiful outwardly."),
   ("John 12:43", "For they loved the praise of men more than the praise of God."),
   ("Col 3:23", "And whatever you do, do it heartily, as to the Lord and not to men."),
 ],
 [("G4383","prosopon — face/person"), ("G5272","hupokrisis — hypocrisy"), ("G5273","hupokrites — hypocrite"), ("G1391","doxa — glory/honor")]),

("G2148", "G", "Εὐρακύλων", "Eurakylon", "Proper Name / Noun", "Northeast wind, Euroclydon",
 "A violent northeast wind in the Mediterranean; the storm that wrecked Paul's ship.",
 "<em>Eurakylon</em> (Εὐρακύλων) — also rendered 'Euroclydon' — is the name of the violent northeastern Mediterranean storm that struck Paul's ship in Acts 27. It is a nautical term combining 'euros' (east wind) + Latin 'aquilo' (north wind) — a deadly nor'easter. This was not a squall but a sustained, multi-week hurricane-force storm.",
 "The storm of Acts 27 is one of Scripture's most detailed narratives — and it is saturated with theology. The <em>Eurakylon</em> was Paul's final great trial before Rome. The ship that carried him also carried 276 souls, none of whom were lost — because Paul had heard from God. The storm stripped away every human resource: cargo jettisoned, tackle thrown overboard, ship's gear abandoned, hope of survival given up. Then the angel came. <em>Eurakylon</em> teaches that when God has a purpose for His servant, no storm can frustrate it. The nor'easter was real. The danger was real. The sovereign protection was also real.",
 [
   ("Acts 27:14", "But not long after, a tempestuous head wind arose, called <em>Euroclydon</em> [Eurakylon]."),
   ("Acts 27:20", "Now when neither sun nor stars appeared for many days, and no small tempest beat on us, all hope that we would be saved was finally given up."),
   ("Acts 27:23", "For there stood by me this night an angel of the God to whom I belong and whom I serve."),
   ("Ps 107:25", "For He commands and raises the stormy wind, which lifts up the waves of the sea."),
   ("Matt 8:26", "But He said to them, 'Why are you fearful, O you of little faith?' Then He arose and rebuked the winds and the sea."),
 ],
 [("G2967","koluo — hinder/prevent"), ("G4143","ploion — ship/vessel"), ("G417","anemos — wind"), ("G2830","kludonizomai — toss/surge")]),

("G2153", "G", "εὐσεβῶς", "eusebos", "Adverb", "Godly, piously, in a godly manner",
 "In a godly manner; piously; living out reverence toward God in conduct and character.",
 "<em>Eusebos</em> (εὐσεβῶς) is the adverb form of <em>eusebes</em> (godly, devout) — living <em>godly</em>, conducting oneself with reverence and devotion toward God. Paul uses it in 2 Timothy 3:12 in one of the most sobering promises in the New Testament: 'All who desire to live godly [eusebos] in Christ Jesus will suffer persecution.'",
 "Paul's equation is counter-intuitive: <em>eusebos</em> (godly living) + Christ Jesus = <em>persecution</em>. The formula is not: godly living leads to prosperity, popularity, and ease. The formula is: faithful, visible, Christlike living in a hostile world draws fire. This is not pessimism; it is realism. Jesus promised the same (John 15:18-20). The man who lives <em>eusebos</em> — in transparent, costly, consistent devotion to Christ — will not blend in. He will be noticed, questioned, resisted, and eventually persecuted in some form. The call is not to shrink back but to endure, knowing that the same Lord who suffered first leads the way.",
 [
   ("2 Tim 3:12", "Yes, and all who desire to live <em>godly</em> [eusebos] in Christ Jesus will suffer persecution."),
   ("Titus 2:12", "Teaching us that, denying ungodliness and worldly lusts, we should live soberly, righteously, and <em>godly</em> [eusebos] in the present age."),
   ("1 Tim 2:2", "That we may lead a quiet and peaceable life in all <em>godliness</em> [eusebeia] and reverence."),
   ("John 15:20", "Remember the word that I said to you: 'A servant is not greater than his master.' If they persecuted Me, they will also persecute you."),
   ("Acts 10:2", "A devout [eusebes] man and one who feared God with all his household."),
 ],
 [("G2150","eusebeia — godliness/piety"), ("G2151","eusebeo — show piety"), ("G2152","eusebes — godly/devout"), ("G764","asebeo — act ungodly")]),

("G2154", "G", "εὔσημος", "eusemos", "Adjective", "Clearly significant, easy to understand",
 "Of clear meaning, easily understood; giving a distinct and intelligible signal.",
 "<em>Eusemos</em> (εὔσημος) combines <em>eu</em> + <em>sema</em> (sign/signal) — 'giving a clear sign,' easily understood. Paul uses this word in 1 Corinthians 14:9 in his extended discussion of tongues versus prophecy: 'Unless you utter by the tongue words easy to understand [eusemos], how will it be known what is spoken?'",
 "Paul's criterion for valid public speech in the church is <em>eusemos</em> — intelligibility, clarity, communicability. A message that cannot be understood by the hearer is not communication; it is noise. This principle cuts across the centuries to every preacher, teacher, and leader: the measure of effective communication is not the sophistication of the speaker but the comprehension of the listener. The Gospel is not an esoteric mystery reserved for initiates; it is the <em>eusemos</em> word — clear, direct, accessible — announced to all who will hear. Preach plainly. Teach clearly. Signal distinctly.",
 [
   ("1 Cor 14:9", "So likewise you, unless you utter by the tongue words easy to understand [eusemos], how will it be known what is spoken? For you will be speaking into the air."),
   ("1 Cor 14:19", "Yet in the church I would rather speak five words with my understanding, that I may teach others also, than ten thousand words in a tongue."),
   ("Acts 2:6", "And when this sound occurred, the multitude came together, and were confused, because everyone heard them speak in his own language."),
   ("Neh 8:8", "So they read distinctly from the book, in the Law of God; and they gave the sense, and helped them to understand the reading."),
   ("Col 4:4", "That I may make it manifest, as I ought to speak."),
 ],
 [("G4592","semeion — sign/miracle"), ("G3056","logos — word"), ("G4395","propheteuo — prophesy"), ("G2097","euangelizo — proclaim good news")]),

("G2157", "G", "εὐσχημοσύνη", "euschemoosyne", "Feminine Noun", "Presentableness, decorum, propriety",
 "Presentableness, comeliness, decorum; proper and honorable outward form.",
 "<em>Euschemoosyne</em> (εὐσχημοσύνη) comes from <em>eu</em> + <em>schema</em> (form/fashion/bearing) — 'good form' or 'presentable bearing.' Paul uses it in 1 Corinthians 12:23 when discussing the body metaphor for the church: 'those members of the body which we think to be less honorable, on these we bestow greater honor; and our unpresentable parts have greater modesty/decorum [euschemoosyne].'",
 "Paul's theology of the body — both the human body and the body of Christ — insists that every member matters and every member is covered with honor. The parts that society deems unrespectable receive <em>extra</em> honor. This is the Gospel's great inversion of the honor-shame culture of the ancient world. In the kingdom, status is not fixed by birth, wealth, or talent; it is conferred by grace. The quietest intercessor, the unseen servant, the undramatic faithful husband — these receive <em>euschemoosyne</em>, the honor of God's regard, which outweighs any human assessment.",
 [
   ("1 Cor 12:23", "And those members of the body which we think to be less honorable, on these we bestow greater honor; and our unpresentable parts have greater modesty [euschemoosyne]."),
   ("1 Cor 12:24", "But our presentable parts have no need. But God composed the body, having given greater honor to that part which lacks it."),
   ("Rom 12:10", "Be kindly affectionate to one another with brotherly love, in honor giving preference to one another."),
   ("Phil 4:8", "Whatever things are true, whatever things are noble, whatever things are just, whatever things are pure, whatever things are lovely, whatever things are of good report... meditate on these things."),
   ("1 Pet 2:17", "Honor all people. Love the brotherhood. Fear God. Honor the king."),
 ],
 [("G4976","schema — form/fashion"), ("G5092","time — honor/price"), ("G2570","kalos — good/beautiful"), ("G819","atimia — dishonor")]),

("G2161", "G", "Εὔτυχος", "Eutuchos", "Proper Name", "Fortunate, good fortune, lucky",
 "A proper name meaning 'fortunate' or 'good fortune'; the young man raised from the dead by Paul.",
 "<em>Eutuchos</em> (Εὔτυχος) combines <em>eu</em> + <em>tuche</em> (fortune/chance) — 'good fortune' or 'fortunate.' He is the young man of Troas who fell asleep during Paul's long late-night sermon, tumbled from the third-floor window, and was 'taken up dead' — then raised to life by Paul in one of Acts' most striking miracle narratives (Acts 20:9-12).",
 "The story of <em>Eutuchos</em> has layers. On the surface: a young man falls asleep in church and falls out a window — the most relatable disaster in Scripture. Below the surface: a resurrection sign at the breaking of bread, on the first day of the week, in the upper room. Paul's response mirrors Elijah and Elisha — throwing himself on the body, life returning. His name 'fortunate' becomes literally true: he was dead, and he is alive again. For the community gathered in that upper room, watching Eutychus carried back in alive, the Eucharist that followed was charged with resurrection electricity. Every Sunday gathering is a Eutychus moment: death conquered, life renewed, the Lord present at His table.",
 [
   ("Acts 20:9", "And in a window sat a certain young man named <em>Eutychus</em> [Eutuchos], who was sinking into a deep sleep."),
   ("Acts 20:10", "But Paul went down, fell on him, and embracing him said, 'Do not trouble yourselves, for his life is in him.'"),
   ("Acts 20:11", "Now when he had come up, had broken bread and eaten, and talked a long while, even till daybreak, he departed."),
   ("Acts 20:12", "And they brought the young man in alive, and they were not a little comforted."),
   ("1 Kings 17:21", "And he stretched himself out on the child three times, and cried out to the LORD..."),
 ],
 [("G386","anastasis — resurrection"), ("G2222","zoe — life"), ("G2288","thanatos — death"), ("G2799","klaio — weep/mourn")]),

]  # end WORDS list

# ─────────────────────────────────────────────────────────────────
# GENERATE ALL PAGES
# ─────────────────────────────────────────────────────────────────

def main():
    os.makedirs(LEXICON_DIR, exist_ok=True)
    created = 0
    skipped = 0
    for word in WORDS:
        strongs_id = word[0]
        lang = word[1]
        fname = os.path.join(LEXICON_DIR, f"{strongs_id}.html")
        if os.path.exists(fname):
            skipped += 1
            continue
        html = make_page(*word)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Created: {fname}")
        created += 1
    print(f"\nDone: {created} created, {skipped} skipped (already existed).")

if __name__ == "__main__":
    main()
