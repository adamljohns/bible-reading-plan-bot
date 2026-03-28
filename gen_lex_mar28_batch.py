#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek - March 28 cron batch"""
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

# ===== 24 HEBREW ENTRIES =====
hebrew_words = [
    (2363, "חוּשׁ", "Chuwsh", "Verb", "To Hasten, Make Haste",
     "To hasten, hurry, move quickly.",
     "The Hebrew <em>chuwsh</em> means to hasten or move with urgency. It appears in poetic contexts where the psalmist pleads with God to act quickly on his behalf. Psalm 71:12 cries: 'O God, do not be far from me; my God, <em>hasten</em> to help me.' The word captures the human cry for divine urgency — recognizing that delay can mean destruction.",
     "The use of <em>chuwsh</em> in prayer reflects a raw, honest theology: God is not slow to act by nature, but from the human perspective under pressure, his timing feels urgent. When David writes 'Hasten, O God, to save me' (Psalm 70:1), he is not accusing God of tardiness but expressing complete dependence. The counterweight is that God's haste is always perfect — when Scripture says 'He will not delay' (Habakkuk 2:3), the same urgency applies to divine promise as to human petition.",
     [("Psalm 71:12", "Do not be far from me, my God; come quickly, God, to <em>help</em> me."),
      ("Psalm 70:1", "Hasten, O God, to save me; come quickly, LORD, to <em>help</em> me."),
      ("Isaiah 28:16", "The one who relies on it will never be <em>stricken with panic</em> — never need to flee in haste."),
      ("Isaiah 5:19", "to those who say, 'Let God <em>hurry</em>; let him hasten his work so we may see it.'"),
      ("Habakkuk 2:3", "For the revelation awaits an appointed time; it speaks of the end and will not prove false. Though it linger, wait for it; it will certainly come and will not <em>delay</em>.")],
     [("H2363", "Chuwsh (Hasten)"), ("H4116", "Mahar (Hasten)"), ("H8668", "Teshuah (Salvation)")]),

    (2368, "חוֹתָם", "Chowtham", "Noun, masculine", "Seal, Signet Ring",
     "A seal or signet ring used to authenticate documents and decrees.",
     "The Hebrew <em>chowtham</em> refers to a seal or signet ring — the personal stamp of authority in the ancient world. Kings used seals to authenticate decrees (Esther 8:8), nobles used them to mark ownership, and God himself uses the image of the seal to describe covenantal intimacy. In Song of Solomon 8:6, the beloved cries: 'Set me as a <em>seal</em> upon your heart' — the most tender use of this word.",
     "The <em>chowtham</em> was the mark of identity and authority. To carry someone's seal was to carry their delegated power. When God says to Zerubbabel, 'I will make you like my signet ring (<em>chowtham</em>), for I have chosen you' (Haggai 2:23), he is reversing the curse on Jeconiah (Jeremiah 22:24) and restoring the line through which Messiah would come. The seal marks what belongs to the king. In the New Testament, believers are 'sealed' with the Holy Spirit (Ephesians 1:13) — marked as belonging to God.",
     [("Song of Solomon 8:6", "Place me like a <em>seal</em> over your heart, like a seal on your arm; for love is as strong as death."),
      ("Haggai 2:23", "'On that day,' declares the LORD Almighty, 'I will take you, my servant Zerubbabel son of Shealtiel,' declares the LORD, 'and I will make you like my <em>signet ring</em>, for I have chosen you.'"),
      ("Jeremiah 22:24", "'As surely as I live,' declares the LORD, 'even if you, Jehoiachin son of Jehoiakim king of Judah, were a <em>signet ring</em> on my right hand, I would still pull you off.'"),
      ("Job 38:14", "The earth takes shape like clay under a <em>seal</em>; its features stand out like those of a garment."),
      ("Esther 8:8", "Now write another decree in the king's name in behalf of the Jews as seems best to you, and <em>seal</em> it with the king's signet ring.")],
     [("H2856", "Chatham (To Seal)"), ("H2885", "Tabbaath (Ring)"), ("H4427", "Malak (To Reign)")]),

    (2373, "חָזֶה", "Chazeh", "Noun, masculine", "Breast, Chest",
     "The breast or chest of a sacrificial animal, waved before the LORD.",
     "The Hebrew <em>chazeh</em> specifically refers to the breast of a sacrificial animal — the portion of the peace offering that was waved before the LORD and then given to the priests. Leviticus 7:30-31 specifies: 'The breast (<em>chazeh</em>) that is waved and the thigh that is presented, you shall eat in a clean place, you and your sons and daughters with you.' The wave offering was a ritual of dedication before God.",
     "The <em>chazeh</em> — the wave-breast — was the priest's portion of the peace offering. In the sacrificial system, the worshiper brought the offering, the fat was burned for the LORD, the right thigh went to the officiating priest, and the breast was waved before God and shared with all Aaron's sons. This distribution embedded hospitality and community into the act of worship. The sacrificial meal was not merely private devotion but a covenantal feast involving God, the priest, and the worshiper's whole household.",
     [("Leviticus 7:31", "The priest shall burn the fat on the altar, but the <em>breast</em> belongs to Aaron and his sons."),
      ("Leviticus 10:14", "You and your sons and daughters may eat the <em>breast</em> that was waved and the thigh that was presented."),
      ("Numbers 6:20", "The priest shall then wave them before the LORD as a wave offering; they are holy and belong to the priest, together with the <em>breast</em> that was waved."),
      ("Exodus 29:27", "After you consecrate the <em>breast</em> of the wave offering and the thigh of the contribution offering that were presented from the ordination ram of Aaron and his sons."),
      ("Leviticus 9:21", "Aaron waved the <em>breasts</em> and the right thigh before the LORD as a wave offering, as Moses commanded.")],
     [("H4503", "Minchah (Grain Offering)"), ("H7810", "Shachad (Gift/Bribe)"), ("H2077", "Zebach (Sacrifice)")]),

    (2376, "חֶזֵו", "Chezev", "Noun, masculine", "Vision (Aramaic)",
     "A vision, dream-vision — Aramaic form used in Daniel.",
     "The Aramaic <em>chezev</em> is the equivalent of Hebrew <em>chazown</em> and appears exclusively in the Aramaic sections of Daniel (chapters 2-7). Daniel describes Nebuchadnezzar's dream and his own visions using this word: 'The visions (<em>chezev</em>) of my head troubled me' (Daniel 7:15). These are not ordinary dreams but divine revelations of world history and the coming kingdom.",
     "The <em>chezev</em> visions of Daniel 7 are among the most theologically dense in all Scripture. In these head-visions Daniel sees four beasts — empires rising and falling — and then the Ancient of Days enthroning the Son of Man. Jesus applies this imagery to himself (Mark 14:62). The Aramaic form of the word signals that these were given in the language of the empire (Aramaic was the diplomatic language of the ancient Near East), yet they reveal God's sovereignty over all empires. The nations rage in Daniel's visions — but the Ancient of Days is seated.",
     [("Daniel 7:1", "In the first year of Belshazzar king of Babylon, Daniel had a dream, and <em>visions</em> passed through his mind as he was lying in bed."),
      ("Daniel 7:13", "In my <em>vision</em> at night I looked, and there before me was one like a son of man, coming with the clouds of heaven."),
      ("Daniel 7:15", "I, Daniel, was troubled in spirit, and the <em>visions</em> that passed through my mind disturbed me."),
      ("Daniel 4:9", "I said, 'Belteshazzar, chief of the magicians, I know that the spirit of the holy gods is in you, and no mystery is too difficult for you. Here is my dream; interpret the <em>vision</em> for me.'"),
      ("Daniel 2:28", "But there is a God in heaven who reveals mysteries. He has shown King Nebuchadnezzar what will happen in days to come. Your dream and the <em>visions</em> that passed through your mind as you were lying in bed are these.")],
     [("H2377", "Chazown (Vision)"), ("H2472", "Chalowm (Dream)"), ("H7200", "Raah (To See)")]),

    (2390, "חָזֵק", "Chazeq", "Adjective", "Strong, Mighty, Hard",
     "Strong, mighty, hard — the adjectival form of the root meaning strength.",
     "The Hebrew adjective <em>chazeq</em> describes what is strong, mighty, or unyielding. It is used of the LORD's strong hand in delivering Israel from Egypt (Exodus 3:19 — 'only a mighty (<em>chazeq</em>) hand will compel him'), of a strong wind (Exodus 10:19), and of the people of God who must 'be strong' (<em>chazaq</em>) before the LORD. The word shares its root with <em>chazaq</em> (H2388) and the noun forms <em>chozeq</em> and <em>chezqah</em>.",
     "Strength in the Hebrew mindset is relational and purposive — it is always strength <em>for</em> something. The LORD's hand being <em>chazeq</em> against Pharaoh was redemptive strength. Joshua's charge to 'be strong and courageous' (Joshua 1:9) used the same root — strength not as personal capacity but as covenant confidence. When the arm or hand of God is described as <em>chazeq</em>, the emphasis is on his unwavering commitment to his promises. Human strength that does not flow from divine empowerment is described as fading or futile.",
     [("Exodus 3:19", "But I know that the king of Egypt will not let you go unless a <em>mighty</em> hand compels him."),
      ("Exodus 10:19", "And the LORD changed the wind to a very <em>strong</em> west wind, which caught up the locusts."),
      ("Joshua 1:9", "Have I not commanded you? Be <em>strong</em> and courageous. Do not be afraid; do not be discouraged."),
      ("Isaiah 35:4", "Say to those with fearful hearts, 'Be <em>strong</em>, do not fear; your God will come.'"),
      ("Nehemiah 2:18", "I also told them about the gracious hand of my God on me and what the king had said to me. They replied, 'Let us start rebuilding.' So they began this good work with <em>strong</em> hands.")],
     [("H2388", "Chazaq (To Strengthen)"), ("H2392", "Chozeq (Strength)"), ("H1369", "Geburah (Might)")]),

    (2391, "חֵזֶק", "Chezeq", "Noun, masculine", "Strength, Power",
     "Strength, power — the concrete noun from the chazaq root.",
     "The Hebrew <em>chezeq</em> is one of several nouns derived from the root <em>chazaq</em> (to be strong). It denotes the quality or exercise of strength. In Ezekiel 30:15 God says he will pour out his wrath on Sin (Pelusium), the 'stronghold (<em>chezeq</em>) of Egypt.' The word captures the idea of consolidated, concentrated power — whether divine or human.",
     "The <em>chezeq</em> family of words in Hebrew theology points to God as the ultimate source of all genuine strength. When Ezekiel describes Egypt's fortresses as <em>chezeq</em>, the point is that even human strongholds fall before God's judgment. The same root that describes God's invincible saving arm (Deuteronomy 4:34) is used to describe strongholds that will be shattered. Strength without covenant fidelity is temporary — the LORD's <em>chozeq</em> is eternal.",
     [("Ezekiel 30:15", "I will pour out my wrath on Pelusium, the stronghold of Egypt, and wipe out the hordes of Thebes."),
      ("Psalm 18:1", "I love you, LORD, my <em>strength</em>."),
      ("Psalm 46:1", "God is our refuge and <em>strength</em>, an ever-present help in trouble."),
      ("Isaiah 40:29", "He gives <em>strength</em> to the weary and increases the power of the weak."),
      ("Zechariah 8:9", "This is what the LORD Almighty says: 'Now hear these words, 'Let your hands be <em>strong</em>' so that the temple may be built.'")],
     [("H2388", "Chazaq (To Strengthen)"), ("H2392", "Chozeq (Strength)"), ("H5797", "Oz (Strength)")]),

    (2392, "חֹזֶק", "Chozeq", "Noun, masculine", "Strength, Might",
     "Strength, might — particularly the strong hand of God.",
     "The Hebrew <em>chozeq</em> appears most prominently in Exodus to describe God's mighty hand that brought Israel out of Egypt. Exodus 13:3 commands Israel to remember the day they came out of Egypt 'with a <em>mighty</em> hand (<em>chozeq</em> yad).' The Passover and Exodus memory was meant to be carried through all generations as testimony to this strength.",
     "The phrase <em>chozeq yad</em> (strength of hand / mighty hand) is central to Exodus theology. God's hand being strong meant his covenantal commitment was active and effective. When the Passover is celebrated and parents explain it to children (Exodus 13:14-16), the <em>chozeq</em> is the reason — 'by the strength of his hand the LORD brought us out of Egypt.' This word is the anchor of liberation theology in the OT: deliverance comes not by human force but by divine <em>chozeq</em>.",
     [("Exodus 13:3", "Moses said to the people, 'Commemorate this day, the day you came out of Egypt, out of the land of slavery, because the LORD brought you out of it with a <em>mighty</em> hand.'"),
      ("Exodus 13:14", "In days to come, when your son asks you, 'What does this mean?' say to him, 'With a <em>mighty</em> hand the LORD brought us out of Egypt, out of the land of slavery.'"),
      ("Exodus 13:16", "And it will be like a sign on your hand and a symbol on your forehead that the LORD brought us out of Egypt with his <em>mighty</em> hand."),
      ("Deuteronomy 4:34", "Has any god ever tried to take for himself one nation out of another nation, by testings, by signs and wonders, by war, by a <em>mighty</em> hand and an outstretched arm?"),
      ("Joshua 4:24", "He did this so that all the peoples of the earth might know that the hand of the LORD is <em>powerful</em> and so that you might always fear the LORD your God.")],
     [("H2388", "Chazaq (To Strengthen)"), ("H2220", "Zeroa (Arm)"), ("H6299", "Padah (To Redeem)")]),

    (2393, "חֶזְקָה", "Chezqah", "Noun, feminine", "Strength, Force",
     "Strength, force — the feminine abstract form of the chazaq root.",
     "The Hebrew <em>chezqah</em> is an abstract noun meaning strength or force. It appears in Ezekiel 3:14 where the prophet is taken by the Spirit with a strong (<em>chezqah</em>) hand upon him. The word captures overpowering compulsion — the irresistible divine force that impels a prophet to speak. It also appears in historical narrative to describe the strength of military sieges.",
     "The <em>chezqah</em> of the divine hand on the prophet is a recurring motif in Ezekiel (3:14; 8:1; 37:1; 40:1). The prophet does not go voluntarily or by his own initiative — the hand of God comes with force and relocates him, whether physically or in vision. This is the theology of prophetic compulsion: 'The Sovereign LORD has spoken — who can but prophesy?' (Amos 3:8). The prophet is not a volunteer speaker but a vessel under the <em>chezqah</em> of the divine hand.",
     [("Ezekiel 3:14", "The Spirit then lifted me up and took me away, and I went in bitterness and in the anger of my spirit, with the <em>strong</em> hand of the LORD on me."),
      ("2 Kings 12:12", "They used the money to pay the workers who repaired the house of the LORD. The workers labored faithfully under them to <em>strengthen</em> the house."),
      ("Ezekiel 8:1", "In the sixth year, in the sixth month on the fifth day, while I was sitting in my house and the elders of Judah were sitting before me, the hand of the Sovereign LORD came on me there with <em>great power</em>."),
      ("2 Chronicles 15:7", "But as for you, be <em>strong</em> and do not give up, for your work will be rewarded."),
      ("Daniel 11:2", "Now then, I tell you the truth: Three more kings will arise in Persia, and then a fourth, who will be far richer than all the others. When he has gained power by his wealth, he will stir up everyone against the kingdom of Greece.")],
     [("H2388", "Chazaq (To Strengthen)"), ("H2394", "Chozqah (Strength)"), ("H3027", "Yad (Hand)")]),

    (2394, "חָזְקָה", "Chozqah", "Noun, feminine", "Strength, Might, Force",
     "Strength, might — a variant form expressing active force or vehemence.",
     "The Hebrew <em>chozqah</em> is closely related to <em>chezqah</em> and appears to describe strength in its active, vehement expression. Isaiah 8:11 says: 'This is what the LORD spoke to me with his <em>strong</em> hand upon me, warning me not to follow the way of this people.' The word suggests not merely strength in reserve but strength breaking forth in action — the LORD's hand pressing down in urgent warning.",
     "The prophetic experience of divine <em>chozqah</em> was not always comfortable. Isaiah was warned not to follow the popular path (Isaiah 8:11-15) — the crowd's wisdom, the political calculation, the fear of nations. God's strong hand pressed the prophet in the opposite direction: 'The LORD Almighty is the one you are to regard as holy.' The strength of God's hand was also the pressure of his counter-cultural will. True prophetic ministry has always involved this <em>chozqah</em> — the divine hand redirecting the prophet against the grain of his culture.",
     [("Isaiah 8:11", "This is what the LORD says to me with his <em>strong hand</em> upon me, warning me not to follow the way of this people."),
      ("Ezekiel 1:3", "The word of the LORD came to Ezekiel the priest, the son of Buzi, in the land of the Babylonians by the Kebar River. There the hand of the LORD was on him with <em>great power</em>."),
      ("2 Samuel 3:6", "During the war between the house of Saul and the house of David, Abner had been <em>strengthening</em> his own position in the house of Saul."),
      ("Job 30:21", "You turn on me ruthlessly; with the <em>might</em> of your hand you attack me."),
      ("Psalm 89:13", "Your arm is endowed with power; your hand is <em>strong</em>, your right hand exalted.")],
     [("H2393", "Chezqah (Strength)"), ("H2388", "Chazaq (To Strengthen)"), ("H3225", "Yamin (Right Hand)")]),

    (2399, "חֵטְא", "Chet", "Noun, masculine", "Sin, Fault, Guilt",
     "Sin, fault, guilt — the guilty condition that results from missing the mark.",
     "The Hebrew <em>chet</em> is the noun form of <em>chata</em> (to sin, miss the mark) and denotes the condition of guilt or sin. Numbers 27:3 uses it when Zelophehad's daughters say their father 'did not die for his own sin' — he was not guilty of the sins of Korah's rebellion. The word captures sin as a forensic status: the state of being at fault before God or others.",
     "The <em>chet</em> and its companion words (<em>chataah</em>, <em>chattath</em>) form the most common sin-vocabulary cluster in the OT. Together they describe sin as missing a target — an archer's metaphor indicating that sin is not merely moral failure but a directional problem. The sinner is aimed at the wrong goal or has failed to hit the right one. The sacrificial system was designed to address <em>chet</em> through substitution: the animal bearing what the sinner deserved. This anticipates the final sacrifice — 'God made him who had no sin to be sin (<em>hamartia</em>) for us' (2 Corinthians 5:21).",
     [("Numbers 27:3", "Our father died in the wilderness. He was not among Korah's followers, who banded together against the LORD, but he died for his own <em>sin</em> and left no sons."),
      ("Genesis 4:7", "If you do what is right, will you not be accepted? But if you do not do what is right, <em>sin</em> is crouching at your door; it desires to have you, but you must rule over it."),
      ("Psalm 51:9", "Hide your face from my <em>sins</em> and blot out all my iniquity."),
      ("Isaiah 1:18", "'Come now, let us settle the matter,' says the LORD. 'Though your <em>sins</em> are like scarlet, they shall be as white as snow.'"),
      ("Proverbs 10:12", "Hatred stirs up conflict, but love covers over all <em>wrongs</em>.")],
     [("H2403", "Chattath (Sin Offering)"), ("H5771", "Avon (Iniquity)"), ("H6588", "Pesha (Transgression)")]),

    (2401, "חֲטָאָה", "Chataah", "Noun, feminine", "Sin, Sin Offering",
     "Sin, sinful act, or sin offering — the feminine noun from the chata root.",
     "The Hebrew <em>chataah</em> is a feminine variant form denoting sin or a sin offering. It appears in Genesis 20:9 where Abimelech confronts Abraham: 'What have you done to me? What sin (<em>chataah</em>) have you brought upon me and my kingdom?' The word is used interchangeably with <em>chattath</em> (H2403) and underscores that sin is always communal — it lands on households and kingdoms, not only individuals.",
     "Abimelech's cry to Abraham — 'What sin have you brought upon me?' — reveals the corporate dimension of sin in Hebrew thought. The <em>chataah</em> of one person pollutes the community. This is why the Levitical sin offerings addressed not only individual guilt but the defilement of sacred space. When the high priest entered the Holy of Holies on Yom Kippur, he was not only dealing with personal sins but cleansing the tabernacle/temple from the accumulated <em>chataah</em> of Israel (Leviticus 16:16). Sin contaminates what it touches — which is why atonement requires not just forgiveness but purification.",
     [("Genesis 20:9", "Then Abimelech called Abraham in and said, 'What have you done to me? What <em>sin</em> have I committed against you that you have brought such great guilt upon me and my kingdom?'"),
      ("Exodus 32:21", "He said to Aaron, 'What did these people do to you, that you led them into such great <em>sin</em>?'"),
      ("Deuteronomy 9:18", "Then once again I fell prostrate before the LORD for forty days and forty nights; I ate no bread and drank no water, because of all the <em>sin</em> you had committed."),
      ("2 Kings 17:21", "When he tore Israel away from the house of David, they made Jeroboam son of Nebat their king. Jeroboam enticed Israel away from following the LORD and caused them to commit a great <em>sin</em>."),
      ("Psalm 32:1", "Blessed is the one whose transgressions are forgiven, whose <em>sins</em> are covered.")],
     [("H2403", "Chattath (Sin Offering)"), ("H2399", "Chet (Sin)"), ("H3722", "Kaphar (Atonement)")]),

    (2402, "חַטָּאָה", "Chattaah", "Noun, feminine (Aramaic)", "Sin, Sin Offering",
     "Sin or sin offering — the Aramaic form used in Daniel.",
     "The Aramaic <em>chattaah</em> appears in Daniel 4:27 in Nebuchadnezzar's dream interpretation: Daniel urges the king to 'break off your sins by practicing righteousness, and your iniquities by showing mercy to the oppressed.' The Aramaic form signals we are in a diplomatic/international context — Nebuchadnezzar was addressed in his own world's language, yet the call to repentance from sin is unchanged.",
     "Daniel's counsel to Nebuchadnezzar is striking: <em>chattaah</em> (sin) can be broken off (<em>peraq</em>) by turning to righteousness and mercy. This is not salvation by works — Daniel is not promising that good deeds erase guilt before God — but a pragmatic prophetic appeal: 'Your kingdom may be extended if you govern justly.' The language echoes throughout the prophets: God relents from judgment when people turn from injustice (Jonah 3:10). Nebuchadnezzar's subsequent pride brought the very judgment Daniel warned against (Daniel 4:29-33). The king who could have broken off his <em>chattaah</em> was instead broken by God.",
     [("Daniel 4:27", "Therefore, Your Majesty, be pleased to accept my advice: Renounce your <em>sins</em> by doing what is right, and your wickedness by being kind to the oppressed."),
      ("Daniel 9:20", "While I was speaking and praying, confessing my <em>sin</em> and the sin of my people Israel and making my request to the LORD my God for his holy hill."),
      ("Ezra 6:17", "For the dedication of this house of God they offered a hundred bulls, two hundred rams, four hundred male lambs and, as a <em>sin offering</em> for all Israel, twelve male goats."),
      ("Proverbs 28:13", "Whoever conceals their <em>sins</em> does not prosper, but the one who confesses and renounces them finds mercy."),
      ("1 John 1:9", "If we confess our sins, he is faithful and just and will forgive us our sins and purify us from all unrighteousness.")],
     [("H2403", "Chattath (Sin Offering)"), ("H2401", "Chataah (Sin)"), ("H6588", "Pesha (Transgression)")]),

    (2404, "חָטַב", "Chatab", "Verb", "To Hew, Cut, Chop Wood",
     "To hew wood, cut timber — used of woodcutters as the lowest temple servants.",
     "The Hebrew <em>chatab</em> means to hew or cut wood. It appears most significantly in the curse Joshua pronounced on the Gibeonites who deceived Israel: 'You are now under a curse: You will never be released from service as woodcutters (<em>chatab</em>) and water carriers for the house of my God' (Joshua 9:23). This became a permanent role for the Gibeonites among the temple servants.",
     "The Gibeonites' cunning deception (Joshua 9) resulted not in extermination but in perpetual servitude — <em>chatab</em> (woodcutters) and water carriers for the house of God. Remarkably, this curse became a form of inclusion: the Gibeonites survived and served at the sanctuary. Centuries later, when Saul killed Gibeonites in violation of this covenant, it brought divine judgment on the land (2 Samuel 21:1). The <em>chatab</em> covenant outlived its shame and became a covenant obligation. Even the lowest temple service — wood-cutting — was bound by covenantal faithfulness.",
     [("Joshua 9:21", "They will be woodcutters and water carriers for the entire community."),
      ("Joshua 9:23", "'You are now under a curse: You will never be released from service as woodcutters and water carriers for the house of my God.'"),
      ("Joshua 9:27", "That day Joshua made the Gibeonites woodcutters and water carriers for the community and for the altar of the LORD at the place the LORD would choose."),
      ("Deuteronomy 29:11", "together with your children and your wives, and the foreigners living in your camps who chop your wood and carry your water."),
      ("Ezekiel 39:10", "They will not need to gather wood from the fields or cut it from the forests, because they will use the weapons for fuel.")],
     [("H2404", "Chatab (Hew)"), ("H7070", "Qaneh (Reed)"), ("H4196", "Mizbeach (Altar)")]),

    (2461, "חָלָב", "Chalab", "Noun, masculine", "Milk",
     "Milk — literal and symbolic of blessing, abundance, and the Promised Land.",
     "The Hebrew <em>chalab</em> (milk) is famous primarily as half of the iconic phrase 'a land flowing with milk and honey' — the Promised Land's signature description (Exodus 3:8). But <em>chalab</em> carries its own theological weight beyond geography. Joel 3:18 prophesies: 'In that day the mountains will drip new wine, and the hills will flow with milk' — a picture of the messianic age. Isaiah 55:1 invites the thirsty to 'come, buy milk and wine without money and without cost.'",
     "Milk in the ancient world represented nourishment that required no slaughter — it was the peaceable abundance of a blessing land. The contrast with Egypt was intentional: Israel had labored under Pharaoh for bread that came through oppression. God's land flowed with <em>chalab</em> — provision that came not through slavery but through covenant. When the New Testament speaks of 'pure spiritual milk' (1 Peter 2:2), it carries this resonance: the word of God as the nourishing abundance of the new Promised Land. The goal is to grow past milk to solid food (Hebrews 5:12-14) — but milk is where growth begins.",
     [("Exodus 3:8", "So I have come down to rescue them from the hand of the Egyptians and to bring them up out of that land into a good and spacious land, a land flowing with milk and honey."),
      ("Isaiah 55:1", "Come, all you who are thirsty, come to the waters; and you who have no money, come, buy and eat! Come, buy wine and <em>milk</em> without money and without cost."),
      ("Joel 3:18", "In that day the mountains will drip new wine, and the hills will flow with <em>milk</em>; all the ravines of Judah will run with water."),
      ("Judges 4:19", "He said to her, 'Please give me a little water; I'm thirsty.' So she opened a skin of <em>milk</em>, gave him a drink, and covered him up."),
      ("Song of Solomon 4:11", "Your lips drop sweetness as the honeycomb, my bride; <em>milk</em> and honey are under your tongue.")],
     [("H1706", "Debash (Honey)"), ("H776", "Erets (Land/Earth)"), ("H7704", "Sadeh (Field)")]),

    (2464, "חֶלְבְּנָה", "Chelbenah", "Noun, feminine", "Galbanum",
     "Galbanum — a pungent resin used in the sacred incense of the tabernacle.",
     "The Hebrew <em>chelbenah</em> is galbanum, a resinous gum from the plant <em>Ferula galbaniflua</em>. It appears in Scripture only in Exodus 30:34 as one of four ingredients in the sacred incense: 'Take fragrant spices — galbanum (<em>chelbenah</em>), onycha and galbanum — and pure frankincense, all in equal amounts.' This incense was holy to the LORD and could not be replicated for personal use (Exodus 30:37-38).",
     "Galbanum had a notably pungent, almost bitter odor on its own — yet when blended with the other sacred spices, it contributed depth and grounding to the incense. The rabbis saw theological meaning in this: even bitter or difficult elements, when offered to God within the community of worship, become part of something holy. The sacred incense was communal — no single note made the fragrance, but each ingredient was required. This points to the Body of Christ: members who may seem difficult or unrefined contribute essential notes to the corporate worship that rises as incense before the throne.",
     [("Exodus 30:34", "Then the LORD said to Moses, 'Take fragrant spices — gum resin, onycha and <em>galbanum</em> — and pure frankincense, all in equal amounts.'"),
      ("Revelation 8:3", "Another angel, who had a golden censer, came and stood at the altar. He was given much incense to offer, with the prayers of all God's people, on the golden altar in front of the throne."),
      ("Psalm 141:2", "May my prayer be set before you like incense; may the lifting up of my hands be like the evening sacrifice."),
      ("Exodus 30:37", "Do not make any incense with this formula for yourselves; consider it holy to the LORD."),
      ("Song of Solomon 4:14", "nard and saffron, calamus and cinnamon, with every kind of incense tree, with myrrh and aloes and all the finest spices.")],
     [("H3828", "Lebonah (Frankincense)"), ("H7004", "Qetoret (Incense)"), ("H4196", "Mizbeach (Altar)")]),

    (2465, "חֶלֶד", "Cheled", "Noun, masculine", "Lifetime, Duration, This World",
     "The span of a lifetime, the transient world — the brief duration of human existence.",
     "The Hebrew <em>cheled</em> refers to the duration of a human life or the transient world. Psalm 39:5 laments: 'You have made my days a mere handbreadth; the span of my years is as nothing before you. Everyone is but a breath, even those who seem secure.' The word carries the note of brevity and ephemerality — life as a <em>cheled</em> is measured and passing.",
     "The theology of <em>cheled</em> runs through the wisdom literature as a corrective to human pretension. Our days are a <em>cheled</em> — a brief span. Psalm 17:14 speaks of 'men of this world (<em>cheled</em>)' whose portion is in this life only. The contrast is always with eternity (Hebrew: <em>olam</em>). Knowing that life is <em>cheled</em> — brief and transient — is meant to produce not despair but wisdom: 'Teach us to number our days, that we may gain a heart of wisdom' (Psalm 90:12). The brevity of <em>cheled</em> makes the eternal weight of covenant all the more precious.",
     [("Psalm 39:5", "You have made my days a mere handbreadth; the <em>span</em> of my years is as nothing before you. Everyone is but a breath."),
      ("Psalm 17:14", "By your hand save me from such people, LORD, from those of this world (<em>cheled</em>) whose reward is in this life."),
      ("Psalm 49:1", "Hear this, all you peoples; listen, all who live in this world (<em>cheled</em>), both low and high, rich and poor alike."),
      ("James 4:14", "Why, you do not even know what will happen tomorrow. What is your life? You are a mist that appears for a little while and then vanishes."),
      ("Psalm 90:12", "Teach us to number our days, that we may gain a heart of wisdom.")],
     [("H5769", "Olam (Eternity/Forever)"), ("H1892", "Hebel (Vapor/Vanity)"), ("H3117", "Yom (Day)")]),

    (2467, "חֹלֶד", "Choled", "Noun, masculine", "Weasel",
     "The weasel — listed among the unclean creatures in Leviticus.",
     "The Hebrew <em>choled</em> refers to some small burrowing animal — traditionally translated 'weasel' — listed in Leviticus 11:29 among the unclean crawling animals. The Levitical purity laws governed not only moral behavior but extended to diet, bodily conditions, and contact with certain animals. The weasel was among those that 'swarm on the ground' and contaminate by touch.",
     "The inclusion of the <em>choled</em> in the Levitical unclean animals list may seem mundane, but it points to a holistic theology of purity. Holiness in Israel was to pervade every area of life — including what one ate and touched. The boundaries were not arbitrary: they visibly marked Israel as a distinct people with a distinct God. The New Testament declares all foods clean (Mark 7:19; Acts 10:15), signaling that the ritual boundary markers have been fulfilled in Christ. The dietary laws pointed to a deeper reality: the true uncleanness is not what goes into a person but what comes out of the heart (Mark 7:20-23).",
     [("Leviticus 11:29", "Of the animals that move along the ground, these are unclean for you: the <em>weasel</em>, the rat, any kind of great lizard."),
      ("Leviticus 11:31", "Of all those that move along the ground, these are unclean to you. Whoever touches them when they are dead will be unclean till evening."),
      ("Mark 7:19", "For it doesn't go into their heart but into their stomach, and then out of the body. In saying this, Jesus declared all foods clean."),
      ("Acts 10:15", "The voice spoke to him a second time, 'Do not call anything impure that God has made clean.'"),
      ("Isaiah 65:4", "who sit among the graves and spend their nights keeping secret vigil; who eat the flesh of pigs, and whose pots hold broth of impure meat.")],
     [("H2941", "Tame (Unclean)"), ("H2893", "Toharah (Purification)"), ("H3808", "Lo (Not)")]),

    (2470, "חָלָה", "Chalah", "Verb", "To Be Sick, Weak, Afflicted",
     "To be sick, weak, or afflicted — also used of seeking God's favor.",
     "The Hebrew <em>chalah</em> has two semantic streams. First, it means to be sick, weak, or diseased (Isaiah 53:3 — 'a man of suffering, and familiar with pain, as one from whom people hide their faces he was despised, and we held him in low esteem'). Second, in the piel stem it means to implore favor, seek grace — literally 'to make the face sick/soft.' This double meaning runs through prayer language: to 'entreat (<em>chalah</em>) the face of the LORD' is to come before him in weakness, seeking his kindness.",
     "Isaiah 53's portrait of the Suffering Servant is saturated with <em>chalah</em>: he was 'stricken' (<em>chalah</em>) — considered afflicted by God (Isaiah 53:4). Yet his affliction was not his own: 'Surely he took up our pain and bore our suffering' (Isaiah 53:4). The deepest theological use of <em>chalah</em> is in this reversal: the Servant's weakness and sickness was our healing. His <em>chalah</em> produced our wholeness. The New Testament quotes Isaiah 53 to explain Christ's healing ministry (Matthew 8:17) and his atoning death (1 Peter 2:24).",
     [("Isaiah 53:3", "He was despised and rejected by mankind, a man of suffering, and familiar with pain (<em>chalah</em>). Like one from whom people hide their faces he was despised, and we held him in low esteem."),
      ("Isaiah 53:10", "Yet it was the LORD's will to crush him and cause him to suffer (<em>chalah</em>), and though the LORD makes his life an offering for sin."),
      ("Psalm 77:10", "Then I thought, 'To this I will appeal: the years when the Most High stretched out his right hand. I will remember the deeds of the LORD.' — spoken in <em>affliction</em>"),
      ("2 Chronicles 16:12", "In the thirty-ninth year of his reign Asa was afflicted (<em>chalah</em>) with a disease in his feet. Though his disease was severe, even in his illness he did not seek help from the LORD, but only from the physicians."),
      ("1 Kings 17:17", "Some time later the son of the woman who owned the house became ill (<em>chalah</em>). He grew worse and worse, and finally stopped breathing.")],
     [("H7495", "Rapha (To Heal)"), ("H4341", "Makob (Pain)"), ("H3510", "Kaab (To Hurt)")]),

    (2483, "חֳלִי", "Choliy", "Noun, masculine", "Sickness, Disease, Affliction",
     "Sickness, disease — the noun form of chalah, used prophetically of the Servant.",
     "The Hebrew <em>choliy</em> is the noun form meaning sickness or disease. Its most theologically charged occurrence is in Isaiah 53:3-4: 'a man of sorrows, and acquainted with grief (<em>choliy</em>)... Surely he took up our pain and bore our suffering (<em>choliy</em>).' The Servant knows disease and carries it — this is the substitutionary heart of Isaiah's fourth Servant Song.",
     "Matthew 8:17 quotes Isaiah 53:4 in connection with Jesus' healing ministry: 'This was to fulfill what was spoken through the prophet Isaiah: He took up our infirmities and bore our diseases (<em>nosos</em> in Greek, translating <em>choliy</em>).' This is remarkable — the Gospel writer sees physical healing as a sign of the deeper bearing of human affliction in the Atonement. Christ's healings on earth were previews of the ultimate 'taking up' of human <em>choliy</em> at the cross. The resurrection is the final answer to <em>choliy</em>: in the age to come, 'no longer will there be any curse' (Revelation 22:3).",
     [("Isaiah 53:3", "He was despised and rejected by mankind, a man of suffering, and familiar with <em>sickness</em>."),
      ("Isaiah 53:4", "Surely he took up our pain and bore our <em>suffering</em>, yet we considered him punished by God, stricken by him, and afflicted."),
      ("Deuteronomy 28:61", "The LORD will also bring on you every kind of <em>sickness</em> and disaster not recorded in this Book of the Law, until you are destroyed."),
      ("Matthew 8:17", "This was to fulfill what was spoken through the prophet Isaiah: 'He took up our infirmities and bore our diseases.'"),
      ("Revelation 21:4", "He will wipe every tear from their eyes. There will be no more death or mourning or crying or pain, for the old order of things has passed away.")],
     [("H7495", "Rapha (To Heal)"), ("H2470", "Chalah (To Be Sick)"), ("H4341", "Makob (Pain)")]),

    (2485, "חָלִיל", "Chalil", "Noun, masculine", "Flute, Pipe",
     "A flute or pipe — a wind instrument used in worship and celebration.",
     "The Hebrew <em>chalil</em> is a wind instrument, likely a double-pipe or flute with a high, penetrating sound. It appears in 1 Samuel 10:5 among the prophetic band's instruments: 'You will meet a procession of prophets coming down from the high place with lyres, timbrels, pipes (<em>chalil</em>) and harps.' In 1 Kings 1:40 all the people played the <em>chalil</em> in rejoicing over Solomon's anointing. Isaiah 30:29 pairs it with the joy of the night of Passover.",
     "The <em>chalil</em> was both a liturgical and popular instrument — used in prophetic worship bands, royal processions, and communal celebrations. Jesus references pipe-playing in his critique of the religious leaders' inconsistency: 'We played the pipe (<em>aulein</em>) for you, and you did not dance' (Matthew 11:17). The pipe was meant to evoke joyful response — the joy of salvation, the dance of the redeemed. When the religious establishment refused to respond either to John's austerity or Jesus' celebration, they revealed a heart hardened to both judgment and grace.",
     [("1 Samuel 10:5", "After that you will go to Gibeah of God, where there is a Philistine outpost. As you approach the town, you will meet a procession of prophets coming down from the high place with lyres, timbrels, <em>pipes</em> and harps."),
      ("1 Kings 1:40", "And all the people went up after him, playing <em>pipes</em> and rejoicing greatly, so that the ground shook with the sound."),
      ("Isaiah 30:29", "And you will sing as on the night you celebrate a holy festival; your hearts will rejoice as when people playing <em>pipes</em> go up to the mountain of the LORD."),
      ("Isaiah 5:12", "They have harps and lyres at their banquets, pipes and timbrels and wine, but they have no regard for the deeds of the LORD, no respect for the work of his hands."),
      ("Matthew 11:17", "'We played the pipe for you, and you did not dance; we sang a dirge, and you did not mourn.'")],
     [("H3658", "Kinnor (Lyre)"), ("H8193", "Shophar (Ram's Horn)"), ("H4210", "Mizmor (Psalm/Song)")]),

    (2490, "חָלַל", "Chalal", "Verb", "To Profane, Defile, Begin",
     "To profane or desecrate the holy; also to pierce or begin.",
     "The Hebrew <em>chalal</em> carries two distinct but related meanings. In its primary sense it means to profane, pollute, or desecrate what is sacred. Leviticus 20:3: 'I will set my face against that man and cut him off from his people; for by giving his children to Molek, he has defiled (<em>chalal</em>) my sanctuary.' In its secondary sense it means to begin, or to pierce — suggesting a break in what was whole.",
     "The theology of <em>chalal</em> centers on the boundary between holy and common. God's name, Sabbath, sanctuary, priesthood, and covenant people are all candidates for profanation in the OT. Ezekiel is particularly focused on the <em>chalal</em> of God's holy name among the nations — Israel's exile was itself a profaning of God's reputation (Ezekiel 36:20-23). God's response is not to abandon his name but to re-sanctify it by restoring Israel. In Isaiah 53:5 the same root appears: 'he was pierced (<em>chalal</em>) for our transgressions' — the Servant profaned by our sin becomes the remedy for all profaning.",
     [("Isaiah 53:5", "But he was <em>pierced</em> for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his wounds we are healed."),
      ("Leviticus 20:3", "I myself will set my face against him and will cut him off from his people, because he gave his children to Molek, to <em>defile</em> my sanctuary and to profane my holy name."),
      ("Ezekiel 36:23", "I will show the holiness of my great name, which has been <em>profaned</em> among the nations, the name you have profaned among them."),
      ("Ezekiel 22:26", "Her priests do violence to my law and <em>profane</em> my holy things; they do not distinguish between the holy and the common."),
      ("Malachi 2:10", "Do we not all have one Father? Did not one God create us? Why do we <em>profane</em> the covenant of our ancestors by being unfaithful to one another?")],
     [("H6944", "Qodesh (Holiness)"), ("H2403", "Chattath (Sin Offering)"), ("H3722", "Kaphar (Atonement)")]),

    (2481, "חֲלִי", "Chaliy", "Noun, masculine", "Ornament, Jewel",
     "Ornament, jewel — adornment worn as beauty or betrothal gift.",
     "The Hebrew <em>chaliy</em> refers to ornaments or jewelry. In Job 28:17, wisdom's incomparable value is contrasted with gold and glass: 'Neither gold nor crystal can compare with it, nor can it be had for jewels (<em>chaliy</em>) of gold.' Proverbs 25:12 uses it in a wisdom saying: 'Like a gold earring or an ornament of fine gold is the rebuke of a wise judge to a listening ear.' The <em>chaliy</em> beautifies — and so does wise correction when received.",
     "The wisdom literature's use of <em>chaliy</em> (ornament) as a metaphor for wise words suggests that beauty and truth are aligned: a timely, true rebuke from a wise source is beautiful, not painful, to one with ears to hear. The same word appears in Isaiah 3:18-21 in the catalog of the Jerusalem women's finery that God would strip away in judgment. The contrast is sharp: the adornment that comes from wisdom lasts; the jewelry that comes from vanity is confiscated. True ornamentation is internal — the 'unfading beauty of a gentle and quiet spirit' (1 Peter 3:4).",
     [("Job 28:17", "Neither gold nor crystal can compare with it, nor can it be had for <em>jewels</em> of gold."),
      ("Proverbs 25:12", "Like a gold earring or an ornament of fine gold is the rebuke of a wise judge to a listening ear."),
      ("Isaiah 3:18", "In that day the Lord will snatch away their finery: the bangles and headbands and crescent necklaces, the earrings and bracelets and <em>veils</em>."),
      ("Song of Solomon 7:1", "How beautiful your sandaled feet, O prince's daughter! Your graceful legs are like jewels, the work of an artist's hands."),
      ("1 Peter 3:4", "Rather, it should be that of your inner self, the unfading beauty of a gentle and quiet spirit, which is of great worth in God's sight.")],
     [("H2091", "Zahab (Gold)"), ("H2885", "Tabbaath (Ring)"), ("H8597", "Tipharah (Beauty/Glory)")]),

    (2480, "חָלַט", "Chalat", "Verb", "To Snatch Away, Rescue",
     "To snatch, rescue — used of swift deliverance from danger.",
     "The Hebrew <em>chalat</em> means to snatch or pull away — either to rescue (positively) or to seize (forcefully). In Psalm 116:8, the psalmist praises God: 'For you, LORD, have delivered my soul from death, my eyes from tears, my feet from stumbling' — the word behind 'delivered' reflects the same root idea of snatching from danger. The imagery is of a hand pulling someone from the edge of a pit.",
     "The verb <em>chalat</em> captures divine rescue as dramatic intervention — not slow deliverance but a snatch from the jaws of death. This aligns with the broader OT theology of <em>yasha</em> (salvation) and <em>padah</em> (redemption): God saves with speed and decisiveness. In Isaiah 66:7, a related noun form describes the rapid birth of a child — suddenness of arrival. For the believer under threat, the comfort of <em>chalat</em>-theology is that God's rescue is not late: he moves quickly when his appointed moment comes.",
     [("Psalm 116:8", "For you, LORD, have delivered my soul from death, my eyes from tears, my feet from stumbling."),
      ("Isaiah 66:7", "Before she goes into labor, she gives birth; before the pains come upon her, she delivers a son."),
      ("Job 23:7", "There the upright can present their case before him, and I would be delivered (<em>chalat</em>) forever from my judge."),
      ("Psalm 18:19", "He brought me out into a spacious place; he rescued me because he delighted in me."),
      ("Zechariah 3:2", "The LORD said to Satan, 'The LORD rebuke you, Satan! The LORD, who has chosen Jerusalem, rebuke you! Is not this man a burning stick snatched from the fire?'")],
     [("H3467", "Yasha (To Save)"), ("H6299", "Padah (To Redeem)"), ("H5337", "Natsal (To Deliver)")]),

    (2484, "חֶלְיָה", "Chelyah", "Noun, feminine", "Ornament, Jewel",
     "A jewel or ornament — feminine form of chaliy.",
     "The Hebrew <em>chelyah</em> is the feminine form of <em>chaliy</em> and refers to ornaments or jewels. It appears in Hosea 2:13 as part of God's covenant lawsuit against Israel: 'She decked herself with rings and jewels (<em>chelyah</em>), and went after her lovers, but me she forgot.' The tragedy is stark: Israel adorned herself for Baal worship rather than for her true husband, the LORD.",
     "The prophetic use of <em>chelyah</em> in Hosea reverses the bridal imagery. In Jeremiah 2:32, God asks rhetorically: 'Does a young woman forget her jewelry, a bride her wedding ornaments? Yet my people have forgotten me, days without number.' The ornaments that were meant to signify the beauty of covenant devotion became tokens of spiritual adultery. Yet God's response is not permanent abandonment — Hosea 2:19 promises a new betrothal: 'I will betroth you to me forever.' The <em>chelyah</em> of idolatry would be stripped away (Hosea 2:13) and replaced by the far greater adornment of righteousness and steadfast love.",
     [("Hosea 2:13", "I will punish her for the days she burned incense to the Baals; she decked herself with rings and <em>jewelry</em>, and went after her lovers, but me she forgot."),
      ("Jeremiah 2:32", "Does a young woman forget her jewelry, a bride her wedding ornaments? Yet my people have forgotten me, days without number."),
      ("Ezekiel 16:11", "I adorned you with jewelry: I put bracelets on your arms and a necklace around your neck."),
      ("Isaiah 61:10", "I delight greatly in the LORD; my soul rejoices in my God. For he has clothed me with garments of salvation and arrayed me in a robe of his righteousness, as a bridegroom adorns his head like a priest, and as a bride adorns herself with her <em>jewels</em>."),
      ("Revelation 21:2", "I saw the Holy City, the new Jerusalem, coming down out of heaven from God, prepared as a bride beautifully dressed for her husband.")],
     [("H2481", "Chaliy (Ornament)"), ("H5716", "Adiy (Ornament)"), ("H3627", "Keliy (Vessel/Instrument)")]),
]

# ===== 23 GREEK ENTRIES =====
greek_words = [
    (1493, "εἰδωλεῖον", "Eidōleion", "Noun, neuter", "Idol Temple",
     "An idol temple or pagan shrine.",
     "The Greek <em>eidōleion</em> refers to an idol temple — the physical structure housing idol worship. Paul uses it in 1 Corinthians 8:10 in his discussion of food sacrificed to idols: 'For if someone with a weak conscience sees you, with all your knowledge, eating in an idol's temple (<em>eidōleion</em>), won't that person be emboldened to eat what is sacrificed to idols?' The location matters — eating in the <em>eidōleion</em> itself signals participation in idol worship beyond mere food.",
     "Paul's argument in 1 Corinthians 8-10 about <em>eidōleion</em> is nuanced. The strong know an idol is nothing (1 Corinthians 8:4) — but reclining at table in an idol temple could ensnare weaker brothers (8:10-11) or inadvertently constitute fellowship with demons (10:20-21). Knowledge without love causes harm. The freedom to know that idols are nothing does not grant freedom to participate in spaces devoted to their worship. The church's separation from the <em>eidōleion</em> was not because the idols were real but because of what such spaces signified socially and spiritually.",
     [("1 Corinthians 8:10", "For if someone with a weak conscience sees you, with all your knowledge, eating in an idol's <em>temple</em>, won't that person be emboldened to eat what is sacrificed to idols?"),
      ("Acts 17:23", "For as I walked around and looked carefully at your objects of worship, I even found an altar with this inscription: TO AN UNKNOWN GOD."),
      ("1 Corinthians 10:21", "You cannot drink the cup of the Lord and the cup of demons too; you cannot have a part in both the Lord's table and the table of demons."),
      ("2 Corinthians 6:16", "What agreement is there between the temple of God and idols? For we are the temple of the living God."),
      ("Revelation 2:14", "Nevertheless, I have a few things against you: There are some among you who hold to the teaching of Balaam, who taught Balak to entice the Israelites to sin so that they ate food sacrificed to idols.")],
     [("G1497", "Eidōlon (Idol)"), ("G2411", "Hieron (Temple)"), ("G3485", "Naos (Sanctuary)")]),

    (1506, "εἰλικρινής", "Eilikrinēs", "Adjective", "Sincere, Pure, Unmixed",
     "Sincere, pure, without hypocrisy — unmixed, tested in sunlight.",
     "The Greek <em>eilikrinēs</em> means sincere, pure, unmixed. The word's etymology is disputed but possibly relates to testing something in the sunlight (<em>eilē</em> + <em>krinō</em>) — holding a jar of honey or wax to the sun to check for impurities. Paul uses it in Philippians 1:10: 'so that you may be able to discern what is best and may be pure (<em>eilikrinēs</em>) and blameless for the day of Christ.' Peter uses it in 2 Peter 3:1 of sincere understanding.",
     "The <em>eilikrinēs</em> character is one that can be examined in full light — no hidden impurities, no mixture of motives, no wax filling the cracks of cracked pottery (as ancient vendors would do to hide defects). The NT call to sincerity is rooted in the character of God, who is utterly transparent and undeceiving. The gospel creates sincere people: 'I urge you, brothers and sisters, by our Lord Jesus Christ and by the love of the Spirit, to join me in my struggle by praying to God for me' (Romans 15:30) — earnest, unmixed intercession. Sincerity is not naivety but integrity of motive aligned with truth.",
     [("Philippians 1:10", "so that you may be able to discern what is best and may be pure (<em>eilikrinēs</em>) and blameless for the day of Christ."),
      ("2 Peter 3:1", "Dear friends, this is now my second letter to you. I have written both of them as reminders to stimulate you to wholesome (<em>eilikrinēs</em>) thinking."),
      ("1 Corinthians 5:8", "Therefore let us keep the Festival, not with the old bread leavened with malice and wickedness, but with the unleavened bread of sincerity and truth."),
      ("2 Corinthians 1:12", "Now this is our boast: Our conscience testifies that we have conducted ourselves in the world, and especially in our relations with you, with integrity and godly sincerity."),
      ("James 3:17", "But the wisdom that comes from heaven is first of all pure; then peace-loving, considerate, submissive, full of mercy and good fruit, impartial and sincere.")],
     [("G1505", "Eilikrineia (Sincerity)"), ("G228", "Alēthinos (True/Genuine)"), ("G4102", "Pistis (Faith)")]),

    (1521, "εἰσάγω", "Eisagō", "Verb", "To Lead In, Bring In",
     "To bring or lead into a place — used of bringing someone into the presence of authority.",
     "The Greek <em>eisagō</em> means to bring or lead into. It appears in Luke 2:27 when Simeon came into the temple as the parents 'brought in the child Jesus' (<em>eisagagon</em>) to fulfill the purification rites. It also appears in Acts 21:28-29 in the false accusation that Paul had 'brought Greeks into the temple.' In Hebrews 1:6, God the Father 'brings his firstborn into the world' — a declaration of the Son's royal entrance into creation.",
     "Hebrews 1:6 uses <em>eisagō</em> for the Father's act of introducing the Son into the world: the Incarnation seen from heaven's throne room — not a birth in obscurity but a royal presentation. The angels are commanded to worship. <em>Eisagō</em> frames the Nativity as an audience with the cosmos: the Son is led in, and all of heaven bows. The manger's humility did not diminish the throne-room reality.",
     [("Hebrews 1:6", "And again, when God <em>brings his firstborn</em> into the world, he says, 'Let all God's angels worship him.'"),
      ("Luke 2:27", "Moved by the Spirit, he went into the temple courts. When the parents <em>brought in</em> the child Jesus to do for him what the custom of the Law required."),
      ("Acts 7:45", "Having received the tabernacle, our ancestors under Joshua <em>brought it</em> with them when they took the land."),
      ("John 18:16", "but Peter had to wait outside at the door. The other disciple, who was known to the high priest, came back, spoke to the servant girl on duty there and <em>brought Peter in</em>."),
      ("Acts 21:28", "shouting, 'Fellow Israelites, help us! This is the man who teaches everyone everywhere against our people and our law and this place. And besides, he has <em>brought</em> Greeks into the temple.'")],
     [("G1525", "Eiserchomai (To Enter)"), ("G71", "Agō (To Lead)"), ("G4352", "Proskuneō (To Worship)")]),

    (1522, "εἰσακούω", "Eisakouō", "Verb", "To Hear, Listen To, Heed",
     "To hear attentively, to listen and respond — used of God hearing prayer.",
     "The Greek <em>eisakouō</em> means to hear attentively or to heed — it implies a response to what is heard, not merely passive reception. Paul uses it in 2 Corinthians 6:2, quoting Isaiah 49:8: 'In the time of my favor I heard (<em>eisēkousa</em>) you, and in the day of salvation I helped you.' God's hearing is always redemptive. The word also appears in Luke 1:13 when Gabriel tells Zechariah: 'Your prayer has been heard (<em>eisēkousthē</em>).'",
     "The <em>eisakouō</em> of God is the heart of prayer theology in both testaments. Gabriel's announcement to Zechariah — 'your prayer has been heard' — refers to decades of faithful intercession for a child, finally answered in the birth of John the Baptist. The word implies that God not only registered the prayer but acted upon it. The apostolic confidence in prayer (1 John 5:14-15) rests on the same conviction: God's hearing is never passive. He hears in order to respond. Paul's quotation of Isaiah 49:8 in 2 Corinthians 6:2 applies this to the gospel: 'now is the time of God's favor, now is the day of salvation' — the hearing has produced the great answer.",
     [("Luke 1:13", "But the angel said to him: 'Do not be afraid, Zechariah; your prayer has been <em>heard</em>. Your wife Elizabeth will bear you a son, and you are to call him John.'"),
      ("2 Corinthians 6:2", "For he says, 'In the time of my favor I <em>heard</em> you, and in the day of salvation I helped you.' I tell you, now is the time of God's favor, now is the day of salvation."),
      ("Matthew 6:7", "And when you pray, do not keep on babbling like pagans, for they think they will be <em>heard</em> because of their many words."),
      ("Hebrews 5:7", "During the days of Jesus' life on earth, he offered up prayers and petitions with fervent cries and tears to the one who could save him from death, and he was <em>heard</em> because of his reverent submission."),
      ("1 John 5:14", "This is the confidence we have in approaching God: that if we ask anything according to his will, he <em>hears</em> us.")],
     [("G191", "Akouō (To Hear)"), ("G4335", "Proseuche (Prayer)"), ("G611", "Apokrinomai (To Answer)")]),

    (1523, "εἰσδέχομαι", "Eisdechomai", "Verb", "To Receive In, Welcome",
     "To receive someone in, accept or welcome — used of God's welcoming acceptance.",
     "The Greek <em>eisdechomai</em> appears only once in the New Testament — 2 Corinthians 6:17: 'Therefore come out from them and be separate, says the Lord. Touch no unclean thing, and I will receive you (<em>eisdexomai</em>).' God's welcome — his <em>eisdechomai</em> — is conditioned on separation: the call to come out precedes the promise of reception. This is the covenantal logic of holiness.",
     "The single occurrence of <em>eisdechomai</em> in 2 Corinthians 6 carries enormous weight. Paul is weaving together several OT quotations (Isaiah 52:11; Ezekiel 20:34; 2 Samuel 7:14) to make the case that the new covenant community is the new temple in which God dwells. The promise 'I will receive you' (<em>eisdexomai</em>) echoes the Exodus promise of divine presence following purification. Separation from what defiles is not the cause of God's love — but it is the prerequisite of his welcoming intimacy. The same Father who runs to meet the prodigal (Luke 15:20) had already watched for his return.",
     [("2 Corinthians 6:17", "Therefore, 'Come out from them and be separate, says the Lord. Touch no unclean thing, and I will <em>receive</em> you.'"),
      ("Isaiah 52:11", "Depart, depart, go out from there! Touch no unclean thing! Come out from it and be pure, you who carry the articles of the LORD's house."),
      ("Revelation 21:27", "Nothing impure will ever enter it, nor will anyone who does what is shameful or deceitful, but only those whose names are written in the Lamb's book of life."),
      ("John 14:3", "And if I go and prepare a place for you, I will come back and <em>take you</em> to be with me that you also may be where I am."),
      ("Luke 15:20", "But while he was still a long way off, his father saw him and was filled with compassion for him; he ran to his son, threw his arms around him and kissed him.")],
     [("G1209", "Dechomai (To Receive)"), ("G40", "Hagios (Holy)"), ("G4335", "Proseuche (Prayer)")]),

    (1524, "εἴσειμι", "Eiseimi", "Verb", "To Go In, Enter",
     "To go into, enter — a formal verb for entering a place or presence.",
     "The Greek <em>eiseimi</em> means to go in or enter. It appears in Acts 3:3 when the lame man sees Peter and John 'about to enter (<em>eisienai</em>) the temple' and asks for alms. In Acts 21:18, Paul goes in (<em>eisēei</em>) to James with the elders. In Hebrews 9:6, 'the priests always entered (<em>eisiasin</em>) the outer room to carry on their ministry.'",
     "The <em>eiseimi</em> of the priests entering the sanctuary (Hebrews 9:6) is contrasted with the once-yearly entrance of the high priest into the Holy of Holies. This ritual geography — the separation of courts, the limited access, the daily service versus the annual approach — was a physical sermon: 'the Holy Spirit was showing by this that the way into the Most Holy Place had not yet been disclosed' (Hebrews 9:8). Christ's once-for-all entry (Hebrews 9:12) through his own blood opened what no Levitical priest could open. Believers now <em>eiseimi</em> freely into the presence of God (Hebrews 10:19-22).",
     [("Acts 3:3", "When he saw Peter and John about to <em>enter</em> the temple, he asked them for money."),
      ("Hebrews 9:6", "When everything had been arranged like this, the priests <em>entered</em> regularly into the outer room to carry on their ministry."),
      ("Acts 21:18", "The next day Paul and the rest of us went to see James, and all the elders were present."),
      ("Hebrews 10:19", "Therefore, brothers and sisters, since we have confidence to <em>enter</em> the Most Holy Place by the blood of Jesus."),
      ("Hebrews 9:12", "He did not enter by means of the blood of goats and calves; but he entered the Most Holy Place once for all by his own blood, thus obtaining eternal redemption.")],
     [("G1525", "Eiserchomai (To Enter)"), ("G3485", "Naos (Sanctuary/Temple)"), ("G749", "Archiereus (High Priest)")]),

    (1527, "εἷς καθ᾽ εἷς", "Heis kath heis", "Idiom/Adverbial phrase", "One by One",
     "One by one — each person individually, in sequence.",
     "The Greek idiom <em>heis kath' heis</em> means 'one by one' or 'one at a time.' It appears in Mark 14:19 at the Last Supper when Jesus announces that one of the Twelve will betray him. Each disciple's individual reckoning before Jesus is captured in this phrase — no one hid behind the group.",
     "The <em>heis kath' heis</em> scene at the Last Supper is one of the most psychologically penetrating in the Gospels. Eleven out of twelve asked 'Is it I?' (Mark 14:19) — a question that reflects not certainty of innocence but honest self-examination. Each man looked inward. Judas eventually asked too (Matthew 26:25) — but having already decided. The individual accountability captured by <em>heis kath' heis</em> anticipates the final judgment where 'each of us will give an account of ourselves to God' (Romans 14:12). There is no hiding in the crowd before the one who sees each heart.",
     [("Mark 14:19", "They were saddened, and <em>one by one</em> they said to him, 'Surely you don't mean me?'"),
      ("John 8:9", "At this, those who heard began to go away <em>one at a time</em>, the older ones first, until only Jesus was left, with the woman still standing there."),
      ("Romans 14:12", "So then, each of us will give an account of ourselves to God."),
      ("2 Corinthians 5:10", "For we must all appear before the judgment seat of Christ, so that each one of us may receive what is due us for the things done while in the body."),
      ("Matthew 26:22", "They were very sad and began to say to him <em>one after the other</em>, 'Surely you don't mean me, Lord?'")],
     [("G1520", "Heis (One)"), ("G2596", "Kata (According to)"), ("G3956", "Pas (All/Every)")]),

    (1528, "εἰσκαλέομαι", "Eiskaleomai", "Verb", "To Call In, Invite Inside",
     "To call in, invite into one's home — welcoming a guest.",
     "The Greek <em>eiskaleomai</em> means to call someone in or invite them inside. It appears only in Acts 10:23 when Peter, having received the vision about clean and unclean animals, 'invited the men in (<em>eiskalesamenos</em>) to be his guests.' The three men sent from Cornelius arrived, Peter received them, and the next day they departed together for a Gentile household — the pivotal turning point in early mission.",
     "The <em>eiskaleomai</em> in Acts 10:23 is a tiny word with massive theological weight. Peter calling these Gentile messengers into his host's house was a visible embodiment of the vision's meaning: 'Do not call anything impure that God has made clean' (Acts 10:15). Before his mind was fully convinced, his feet obeyed. He called them in. The next day he entered a Gentile home (Acts 10:27) — something previously forbidden. The gospel's expansion to the nations began with this act of hospitality: <em>eiskaleomai</em>, a simple invitation in.",
     [("Acts 10:23", "Then Peter <em>invited the men in</em> to be his guests. The next day Peter started out with them, and some of the believers from Joppa went along."),
      ("Acts 10:15", "The voice spoke to him a second time, 'Do not call anything impure that God has made clean.'"),
      ("Acts 11:3", "'You went into the house of uncircumcised men and ate with them.'"),
      ("Romans 15:7", "Accept one another, then, just as Christ accepted you, in order to bring praise to God."),
      ("Hebrews 13:2", "Do not forget to show hospitality to strangers, for by so doing some people have shown hospitality to angels without knowing it.")],
     [("G2564", "Kaleō (To Call)"), ("G5381", "Philoxenia (Hospitality)"), ("G2983", "Lambanō (To Receive)")]),

    (1529, "εἴσοδος", "Eisodos", "Noun, feminine", "Entrance, Coming, Access",
     "Entrance, arrival, access — used of Paul's ministry arrival and Christ's access to God.",
     "The Greek <em>eisodos</em> means entrance, coming, or access. Paul uses it in 1 Thessalonians 1:9 of his initial arrival among them: 'For they themselves report what kind of reception you gave us. They tell how you turned to God from idols.' In 1 Thessalonians 2:1 he refers to his <em>eisodos</em> as not having been in vain. In Hebrews 10:19, the 'new and living way' is the <em>eisodos</em> into the Most Holy Place opened by Christ's blood.",
     "The <em>eisodos</em> of Hebrews 10:19 is theologically decisive: believers have a bold entry-right into God's presence that the entire Levitical system could not provide. The high priest entered once a year, behind a veil, with blood not his own. Now, through Christ's torn flesh (the veil — Hebrews 10:20), the <em>eisodos</em> is permanent, confident, and open to all. Paul's pastoral <em>eisodos</em> into Thessalonica (1 Thessalonians 2:1) was meant to model the same gospel-boldness: coming in not with timidity but with Spirit-empowered proclamation. The messenger's entry mirrors the Lord's entry through the veil.",
     [("Hebrews 10:19", "Therefore, brothers and sisters, since we have confidence to enter (<em>eisodos</em>) the Most Holy Place by the blood of Jesus."),
      ("1 Thessalonians 1:9", "for they themselves report what kind of <em>reception</em> you gave us."),
      ("1 Thessalonians 2:1", "You know, brothers and sisters, that our visit to you was not without results."),
      ("2 Peter 1:11", "and you will receive a rich welcome (<em>eisodos</em>) into the eternal kingdom of our Lord and Savior Jesus Christ."),
      ("Acts 13:24", "Before the coming of Jesus, John preached repentance and baptism to all the people of Israel.")],
     [("G1525", "Eiserchomai (To Enter)"), ("G3952", "Parousia (Coming/Presence)"), ("G3485", "Naos (Sanctuary)")]),

    (1530, "εἰσπηδάω", "Eispēdaō", "Verb", "To Rush In, Spring In",
     "To rush into a place — violent or urgent entry.",
     "The Greek <em>eispēdaō</em> means to spring or rush in. It appears twice in Acts. In Acts 14:14, when the crowd at Lystra tries to sacrifice to Paul and Barnabas as gods, 'the apostles Barnabas and Paul heard of this and <em>tore their clothes</em> and rushed out (<em>exepēdēsan</em>).' The related <em>eispēdaō</em> appears in Acts 16:29 when the Philippian jailer, having heard the earthquake and thinking the prisoners had escaped, 'rushed in (<em>eispēdēsas</em>) and fell trembling before Paul and Silas.'",
     "The jailer's <em>eispēdaō</em> into the inner prison (Acts 16:29) is one of the great conversion moments in Acts. He came in trembling, ready for death (his own), and left a baptized man with joy. What drove him from a sword raised against himself to kneeling before prisoners? The earthquake, the open doors, the prisoners who had not fled — all of it pointed to a Power beyond Rome. 'What must I do to be saved?' (Acts 16:30) is the question that <em>eispēdaō</em> produced. Urgency in entering the presence of those who have the word leads to urgency in receiving the word.",
     [("Acts 16:29", "The jailer called for lights, <em>rushed in</em> and fell trembling before Paul and Silas."),
      ("Acts 16:30", "He then brought them out and asked, 'Sirs, what must I do to be saved?'"),
      ("Acts 14:14", "But when the apostles Barnabas and Paul heard of this, they tore their clothes and <em>rushed out</em> into the crowd, shouting."),
      ("John 20:4", "Both were running, but the other disciple outran Peter and reached the tomb first."),
      ("Mark 5:2", "When Jesus got out of the boat, a man with an impure spirit came from the tombs to meet him.")],
     [("G1525", "Eiserchomai (To Enter)"), ("G5400", "Phobos (Fear/Terror)"), ("G4991", "Sōtēria (Salvation)")]),

    (1531, "εἰσπορεύομαι", "Eisporeuomai", "Verb", "To Enter, Go In, Come In",
     "To go into, enter — used of entering places, the heart, and the kingdom.",
     "The Greek <em>eisporeuomai</em> is a common verb meaning to enter or go into. Jesus uses it in Mark 1:21 ('They went to Capernaum') and more significantly in the debate over clean and unclean: 'Nothing outside a person can defile them by going into (<em>eisporeuomenon</em>) them. Rather, it is what comes out of a person that defiles them' (Mark 7:15). It appears in Acts 28:30 of visitors coming to Paul during his house arrest.",
     "Jesus' use of <em>eisporeuomai</em> in Mark 7:15-18 is theologically revolutionary. What enters (<em>eisporeuomenon</em>) does not defile — this overturns the entire system of dietary law at the level of principle, though not yet in explicit declaration (Mark 7:19 adds the editorial note 'declaring all foods clean'). The true locus of defilement is the human heart: 'from within, out of the heart of man, come evil thoughts' (Mark 7:21). The <em>eisporeuomai</em> debate became the theological basis for the Gentile mission — if entering does not defile, neither does table fellowship with Gentiles.",
     [("Mark 7:15", "Nothing outside a person can defile them by going into (<em>eisporeuomenon</em>) them. Rather, it is what comes out of a person that defiles them."),
      ("Mark 1:21", "They went to Capernaum, and when the Sabbath came, Jesus went into the synagogue and began to teach."),
      ("Acts 28:30", "For two whole years Paul stayed there in his own rented house and welcomed all who came to see him."),
      ("Luke 22:10", "He replied, 'As you enter the city, a man carrying a jar of water will meet you. Follow him to the house that he enters.'"),
      ("Revelation 22:14", "Blessed are those who wash their robes, that they may have the right to the tree of life and may go through the gates into the city.")],
     [("G1525", "Eiserchomai (To Enter)"), ("G2588", "Kardia (Heart)"), ("G2840", "Koinoō (To Make Common/Defile)")]),

    (1533, "εἰσφέρω", "Eisphero", "Verb", "To Bring In, Carry In",
     "To bring or carry something into a place — used of bringing into temptation.",
     "The Greek <em>eisphero</em> means to bring or carry into. Its most theologically significant use is in the Lord's Prayer: 'And lead us not into temptation (<em>eisenegkēs</em>)' (Matthew 6:13; Luke 11:4). The word implies being carried or led into a dangerous situation. Paul also uses it in 1 Timothy 6:7: 'We brought nothing (<em>eisēnegkamen</em>) into the world, and we can take nothing out of it.'",
     "The Lord's Prayer petition against being <em>eisphero</em> into temptation has been much debated. Does God lead people into temptation? James 1:13 insists God tempts no one. The prayer's request is better understood as asking God not to bring us into the place of testing beyond our capacity — a prayer for divine navigation that steers us away from the severe trial. It acknowledges our weakness: we do not choose when to face the most dangerous tests. The companion phrase 'but deliver us from the evil one' adds specificity: the <em>eisphero</em> we fear is being handed over to the devil's domain.",
     [("Matthew 6:13", "And lead us not into temptation (<em>eisenegkēs</em>), but deliver us from the evil one."),
      ("Luke 11:4", "And lead us not into temptation."),
      ("1 Timothy 6:7", "For we brought (<em>eisēnegkamen</em>) nothing into the world, and we can take nothing out of it."),
      ("Hebrews 13:11", "The high priest carries (<em>eisphero</em>) the blood of animals into the Most Holy Place as a sin offering, but the bodies are burned outside the camp."),
      ("James 1:13", "When tempted, no one should say, 'God is tempting me.' For God cannot be tempted by evil, nor does he tempt anyone.")],
     [("G3986", "Peirasmos (Temptation/Trial)"), ("G4190", "Ponēros (Evil/Evil One)"), ("G4506", "Rhoumai (To Deliver)")]),

    (1534, "εἶτα", "Eita", "Adverb", "Then, Next, Afterward",
     "Then, next — indicating sequence or continuation.",
     "The Greek <em>eita</em> marks the next step in a sequence. In the resurrection passage of 1 Corinthians 15:5-8, Paul uses <em>eita</em> to trace the post-resurrection appearances: 'he appeared to Cephas, and then (<em>eita</em>) to the Twelve. After that, he appeared to more than five hundred of the brothers and sisters at the same time.' Mark uses <em>eita</em> in his sequence of parables (Mark 4:17, 28) and healing accounts. In 1 Timothy 2:13, <em>eita</em> anchors the creation order argument.",
     "Paul's use of <em>eita</em> in 1 Corinthians 15 is carefully ordered — a sequence of resurrection witnesses building to an irrefutable cumulative case. He then (<em>eita</em>) to the Twelve, then (<em>epeita</em>) to five hundred, then to James, then to all the apostles, last of all to Paul himself. The sequential logic answers skeptics: too many credible witnesses, too spread across time. The resurrection is not a single claim but a chain of <em>eita</em> — then, then, then, then, and finally. No single link can be dismissed without challenging the entire sequence.",
     [("1 Corinthians 15:5", "and that he appeared to Cephas, and <em>then</em> to the Twelve."),
      ("1 Corinthians 15:24", "<em>Then</em> the end will come, when he hands over the kingdom to God the Father after he has destroyed all dominion, authority and power."),
      ("Mark 4:28", "All by itself the soil produces grain — first the stalk, <em>then</em> the head, then the full kernel in the head."),
      ("1 Timothy 2:13", "For Adam was formed first, <em>then</em> Eve."),
      ("James 1:15", "<em>Then</em>, after desire has conceived, it gives birth to sin; and sin, when it is full-grown, gives birth to death.")],
     [("G1899", "Epeita (Then/After)"), ("G3739", "Hos (When/As)"), ("G386", "Anastasis (Resurrection)")]),

    (1535, "εἴτε", "Eite", "Conjunction", "Whether, If, Either...or",
     "Whether, if — used in conditional lists covering all possibilities.",
     "The Greek <em>eite</em> means 'whether' or 'if' and is used in correlative pairs to cover all alternatives: <em>eite...eite</em> = 'whether...or.' Paul deploys it extensively to express the universality of a principle. Romans 12:6-8 lists spiritual gifts with <em>eite</em>: 'if prophecy... if service... if teaching...' In 1 Corinthians 3:22, Paul insists all things belong to believers: 'whether (<em>eite</em>) Paul or Apollos or Cephas or the world or life or death.'",
     "Paul's use of <em>eite...eite</em> in 1 Corinthians 3:21-22 is one of the most sweeping declarations in the NT: all things belong to the believer in Christ — 'whether Paul or Apollos or Cephas or the world or life or death or the present or the future — all are yours, and you are of Christ, and Christ is of God.' The <em>eite</em> covers every category without exception. The Christian possesses everything because they belong to the one who owns everything. The divisions over human leaders (1 Corinthians 1-4) were absurd in light of this: why divide over instruments when you own the whole orchestra?",
     [("1 Corinthians 3:22", "whether (<em>eite</em>) Paul or Apollos or Cephas or the world or life or death or the present or the future — all are yours."),
      ("Romans 12:7", "<em>if</em> it is serving, then serve; if it is teaching, then teach."),
      ("2 Corinthians 5:9", "So we make it our goal to please him, whether (<em>eite</em>) we are at home in the body or away from it."),
      ("Philippians 1:27", "whatever happens, conduct yourselves in a manner worthy of the gospel of Christ. Then, whether (<em>eite</em>) I come and see you or only hear about you in my absence."),
      ("1 Peter 2:13", "Submit yourselves for the Lord's sake to every human authority: whether (<em>eite</em>) to the emperor, as the supreme authority.")],
     [("G1487", "Ei (If)"), ("G2532", "Kai (And)"), ("G3956", "Pas (All/Every)")]),

    (1538, "ἕκαστος", "Hekastos", "Adjective/Pronoun", "Each, Every One",
     "Each one, every individual — emphasizing individual accountability and distribution.",
     "The Greek <em>hekastos</em> means 'each one' or 'every individual.' Paul uses it in the judgment passages: 'For we must all appear before the judgment seat of Christ, so that <em>each one</em> may receive what is due him' (2 Corinthians 5:10). It also appears in spiritual gift distribution: 'to <em>each one</em> the manifestation of the Spirit is given for the common good' (1 Corinthians 12:7). <em>Hekastos</em> preserves individuality within community.",
     "The NT's use of <em>hekastos</em> holds two truths in tension. The Spirit gives to <em>each one</em> (1 Corinthians 12:7) — charisms are personal, varied, and individually assigned for communal benefit. No one is omitted and no one receives the same gift as everyone else. Yet <em>each one</em> will also give an individual account (2 Corinthians 5:10; Romans 14:12). The gift-giving and the accounting both run through the same word: the individuation of grace is matched by the individuation of responsibility. The giver must give a reckoning of their gift.",
     [("1 Corinthians 12:7", "Now to <em>each one</em> the manifestation of the Spirit is given for the common good."),
      ("2 Corinthians 5:10", "For we must all appear before the judgment seat of Christ, so that <em>each one</em> of us may receive what is due us."),
      ("Romans 14:12", "So then, <em>each of us</em> will give an account of ourselves to God."),
      ("Ephesians 4:7", "But to <em>each one of us</em> grace has been given as Christ apportioned it."),
      ("Galatians 6:4", "<em>Each one</em> should test their own actions. Then they can take pride in themselves alone, without comparing themselves to someone else.")],
     [("G3956", "Pas (All/Every)"), ("G1520", "Heis (One)"), ("G2962", "Kyrios (Lord)")]),

    (1539, "ἑκάστοτε", "Hekastote", "Adverb", "Always, Each Time, On Every Occasion",
     "Always, each time — marking consistent, repeated action.",
     "The Greek <em>hekastote</em> means 'always' or 'on each occasion.' It appears only in 2 Peter 1:15: 'And I will make every effort to see that after my departure you will always (<em>hekastote</em>) be able to remember these things.' Peter is speaking of leaving a permanent testimony — his letter itself — so that the truth remains accessible always, not just while he lives.",
     "Peter's use of <em>hekastote</em> in 2 Peter 1:15 reflects an apostle's pastoral burden for continuity. He knows his death is near (2 Peter 1:14 — 'the putting aside of my body will come soon'). His response is not resignation but resolve: he will write so that readers can <em>always</em> recall the truth. The word <em>hekastote</em> spans his death — the Scripture he leaves behind ensures that what he taught will be retrievable by every generation after him. The permanence of written apostolic testimony is the answer to the limitation of mortal teachers.",
     [("2 Peter 1:15", "And I will make every effort to see that after my departure you will <em>always</em> be able to remember these things."),
      ("2 Timothy 3:16", "All Scripture is God-breathed and is useful for teaching, rebuking, correcting and training in righteousness."),
      ("John 14:26", "But the Advocate, the Holy Spirit, whom the Father will send in my name, will teach you all things and will remind you of everything I have said to you."),
      ("Jude 1:3", "I felt compelled to write and urge you to contend for the faith that was once for all entrusted to God's holy people."),
      ("2 Peter 3:1", "Dear friends, this is now my second letter to you. I have written both of them as reminders to stimulate you to wholesome thinking.")],
     [("G104", "Aei (Always)"), ("G1538", "Hekastos (Each)"), ("G3417", "Mneia (Remembrance)")]),

    (1540, "ἑκατόν", "Hekaton", "Numeral", "One Hundred",
     "The number one hundred — used in parables of abundance and accounting.",
     "The Greek <em>hekaton</em> is the number one hundred. Jesus uses it in three parable contexts: the Lost Sheep (Luke 15:4 — 'Suppose one of you has a <em>hundred</em> sheep'), the hundredfold return of the sown word (Mark 4:8), and the parable of the unforgiving servant who owed a fellow servant a <em>hundred</em> denarii (Matthew 18:28). In Acts 1:15, the number of believers gathered after the Ascension was about <em>120</em> — drawn from the <em>hundred</em> and twenty.",
     "The parable of the Lost Sheep (Luke 15:4-7) hinges on <em>hekaton</em>. The shepherd leaves the ninety-nine to find the one. From a mathematical standpoint this is irrational — risk the <em>hundred</em> to recover the one? But that is precisely Jesus' theology of the Father: the value of the one is not diminished by the number of the ninety-nine. Every <em>hekaton</em> is made up of <em>hekastos</em> — every hundred is made up of individuals, each of infinite worth to the Shepherd. The hundredfold return (Mark 4:8) speaks to the inexhaustible generosity of the kingdom: what God receives, he returns at inconceivable multiplication.",
     [("Luke 15:4", "Suppose one of you has a <em>hundred</em> sheep and loses one of them. Doesn't he leave the ninety-nine in the open country and go after the lost sheep?"),
      ("Matthew 18:28", "But when that servant went out, he found one of his fellow servants who owed him a <em>hundred</em> silver coins."),
      ("Mark 4:8", "Still other seed fell on good soil. It came up, grew and produced a crop, some multiplying thirty, some sixty, some a <em>hundred</em> times."),
      ("John 19:39", "He was accompanied by Nicodemus, the man who earlier had visited Jesus at night. Nicodemus brought a mixture of myrrh and aloes, about seventy-five pounds."),
      ("Matthew 13:23", "But the seed falling on good soil refers to someone who hears the word and understands it. This is the one who produces a crop, yielding a <em>hundred</em>, sixty or thirty times what was sown.")],
     [("G1176", "Deka (Ten)"), ("G5507", "Chilioi (Thousand)"), ("G4130", "Plēthō (To Fill/Fulfill)")]),

    (1541, "ἑκατονταετής", "Hekatontaetēs", "Adjective", "One Hundred Years Old",
     "A hundred years old — used of Abraham's faith against biological impossibility.",
     "The Greek <em>hekatontaetēs</em> appears only in Romans 4:19 in Paul's exposition of Abraham's faith: 'Without weakening in his faith, he faced the fact that his body was as good as dead — since he was about a hundred years old (<em>hekatontaetēs</em>).' The word underscores the biological impossibility that Abraham and Sarah faced — and the theological point that faith counts on God's power, not human capacity.",
     "Romans 4 uses <em>hekatontaetēs</em> as the outer limit of human reproductive capacity — the point at which all natural hope is exhausted. Abraham's faith did not ignore this reality: he 'faced the fact' (Romans 4:19) of his <em>hekatontaetēs</em> status. Biblical faith is not denial of evidence but trust in God despite evidence. The miracle of Isaac is not less miraculous for being acknowledged as biologically impossible. Paul uses this as the paradigm of justifying faith: 'For us also, to whom righteousness will be credited — for us who believe in him who raised Jesus our Lord from the dead' (Romans 4:24). The same God who gave life to Abraham's <em>hekatontaetēs</em> body raised Jesus from the dead.",
     [("Romans 4:19", "Without weakening in his faith, he faced the fact that his body was as good as dead — since he was about a <em>hundred years old</em> — and that Sarah's womb was also dead."),
      ("Genesis 17:17", "Abraham fell facedown; he laughed and said to himself, 'Will a son be born to a man a <em>hundred years old</em>? Will Sarah bear a child at the age of ninety?'"),
      ("Hebrews 11:11", "And by faith even Sarah, who was past childbearing age, was enabled to bear children because she considered him faithful who had made the promise."),
      ("Romans 4:20", "Yet he did not waver through unbelief regarding the promise of God, but was strengthened in his faith and gave glory to God."),
      ("Luke 1:37", "For no word from God will ever fail.")],
     [("G1540", "Hekaton (Hundred)"), ("G4102", "Pistis (Faith)"), ("G1860", "Epangelia (Promise)")]),

    (1542, "ἑκατονταπλασίων", "Hekatontaplasiōn", "Adjective", "Hundredfold",
     "A hundredfold — the return promised to those who leave all for the kingdom.",
     "The Greek <em>hekatontaplasiōn</em> means hundredfold and appears in Jesus' promise to those who give up home, family, or land for the kingdom: 'I tell you the truth, no one who has left home or wife or brothers or sisters or parents or children for the sake of the kingdom of God will fail to receive many times as much in this age, and in the age to come eternal life' (Luke 18:29-30). Mark 10:30 specifies the hundredfold return 'in this age' — plus persecutions.",
     "The <em>hekatontaplasiōn</em> promise is both encouraging and surprising. Jesus does not say 'your sacrifice will be worth it in heaven.' He says it will be returned a hundred times in this present age — plus eternal life. The kingdom community becomes the new family for those who have lost family for Christ's sake. The church is the <em>hekatontaplasiōn</em> house: 'brothers, sisters, mothers, children.' Mark 10:30 adds the sobering 'and with them, persecutions' — the hundredfold comes with the cross attached. There is no abundance without suffering in the kingdom's present age.",
     [("Mark 10:30", "will fail to receive a <em>hundred times</em> as much in this present age: homes, brothers, sisters, mothers, children and fields — along with persecutions — and in the age to come eternal life."),
      ("Luke 18:29", "I tell you the truth, no one who has left home or wife or brothers or sisters or parents or children for the sake of the kingdom of God."),
      ("Matthew 19:29", "And everyone who has left houses or brothers or sisters or father or mother or wife or children or fields for my sake will receive a <em>hundred times</em> as much and will inherit eternal life."),
      ("2 Corinthians 9:6", "Remember this: Whoever sows sparingly will also reap sparingly, and whoever sows generously will also reap generously."),
      ("Mark 4:8", "Still other seed fell on good soil. It came up, grew and produced a crop, some multiplying thirty, some sixty, some a <em>hundred</em> times.")],
     [("G1540", "Hekaton (Hundred)"), ("G932", "Basileia (Kingdom)"), ("G2222", "Zōē (Life)")]),

    (1543, "ἑκατοντάρχης", "Hekatontarchēs", "Noun, masculine", "Centurion",
     "A centurion — commander of approximately one hundred soldiers in the Roman army.",
     "The Greek <em>hekatontarchēs</em> is the centurion — a Roman officer commanding roughly 100 soldiers. The Gospels and Acts present centurions consistently with positive characterization: the Capernaum centurion (Matthew 8:5-13) had greater faith than anyone in Israel; the centurion at the cross (Mark 15:39) confessed 'Surely this man was the Son of God!'; Cornelius (Acts 10) was the first Gentile convert; Julius (Acts 27:43) saved Paul's life by preventing the soldiers from killing the prisoners.",
     "The centurions of the NT are a striking pattern: Gentile military men who recognize Jesus when Israel's leaders do not. The Capernaum centurion understood authority ('I myself am a man under authority' — Matthew 8:9) and therefore understood Jesus' authority. His logic was military: authority works through delegation. Jesus' capacity to heal at a distance was not strange to someone who understood that real authority does not require physical presence. The cross-centurion's confession (Mark 15:39) came at the exact moment all others had abandoned Jesus. Rome's soldier saw what Israel's priests missed.",
     [("Matthew 8:8", "The centurion replied, 'Lord, I do not deserve to have you come under my roof. But just say the word, and my servant will be healed.'"),
      ("Mark 15:39", "And when the centurion, who stood there in front of Jesus, saw how he died, he said, 'Surely this man was the Son of God!'"),
      ("Acts 10:1", "At Caesarea there was a man named Cornelius, a centurion in what was known as the Italian Regiment."),
      ("Acts 27:43", "But the centurion wanted to spare Paul's life and kept them from carrying out their plan."),
      ("Luke 23:47", "The centurion, seeing what had happened, praised God and said, 'Surely this was a righteous man.'")],
     [("G4753", "Strateuma (Army)"), ("G1543", "Hekatontarches (Centurion — alt)"), ("G4102", "Pistis (Faith)")]),

    (1546, "ἐκβολή", "Ekbolē", "Noun, feminine", "Throwing Overboard, Jettisoning",
     "A throwing out or jettisoning — used of cargo thrown overboard in a storm.",
     "The Greek <em>ekbolē</em> appears only in Acts 27:18 during Paul's shipwreck voyage: 'We took such a violent battering from the storm that the next day they began to throw the cargo overboard (<em>ekbolēn epoiounto</em>).' The sailors cast off the freight to save the ship — a vivid picture of desperate sacrifice of the valuable to preserve the essential.",
     "Acts 27's <em>ekbolē</em> is not just navigation history but providential theology. The crew jettisoned the cargo; Paul received the word: 'last night an angel of the God to whom I belong and whom I serve stood beside me and said, Do not be afraid, Paul. You must stand trial before Caesar; and God has graciously given you the lives of all who sail with you' (Acts 27:23-24). The <em>ekbolē</em> is human response to crisis; the angel's word is divine guarantee beyond human calculation. What the sailors tried to accomplish by throwing cargo, God accomplished by keeping his promise. The ship was lost, but all 276 lives were saved — exactly as spoken.",
     [("Acts 27:18", "We took such a violent battering from the storm that the next day they began to throw the cargo overboard (<em>ekbolē</em>)."),
      ("Acts 27:24", "and said, 'Do not be afraid, Paul. You must stand trial before Caesar; and God has graciously given you the lives of all who sail with you.'"),
      ("Jonah 1:5", "All the sailors were afraid and each cried out to his own god. And they threw the cargo into the sea to lighten the ship."),
      ("Matthew 15:17", "Don't you see that whatever enters the mouth goes into the stomach and then out of the body?"),
      ("Philippians 3:8", "What is more, I consider everything a loss because of the surpassing worth of knowing Christ Jesus my Lord, for whose sake I have lost all things.")],
     [("G1544", "Ekballō (To Cast Out)"), ("G4143", "Ploion (Ship)"), ("G4151", "Pneuma (Spirit)")]),

    (1548, "ἐκγαμίζω", "Ekgamizō", "Verb", "To Give in Marriage",
     "To give a daughter in marriage — used in eschatological contexts.",
     "The Greek <em>ekgamizō</em> means to give in marriage (specifically of a father giving a daughter). Jesus uses it in Matthew 24:38 to describe the days before the flood — and therefore the days before his return: 'For in the days before the flood, people were eating and drinking, marrying and giving in marriage (<em>ekgamizontes</em>), up to the day Noah entered the ark.' Normal life continued until the moment of judgment.",
     "The <em>ekgamizō</em> saying of Matthew 24:38 is not a condemnation of marriage or eating and drinking — these are normal human activities. The warning is about the normalcy itself becoming a spiritual anesthetic. People were so absorbed in <em>ekgamizō</em> — the ordinary institution of family formation — that they missed the approaching flood. The same will be true before Christ's return. The antidote is not to stop marrying but to 'keep watch' (Matthew 24:42) — to live fully in the present while remaining watchful for the eternal. The Bridegroom's arrival will interrupt the wedding plans of those not waiting for him.",
     [("Matthew 24:38", "For in the days before the flood, people were eating and drinking, marrying and <em>giving in marriage</em>, up to the day Noah entered the ark."),
      ("Luke 17:27", "People were eating, drinking, marrying and being given in marriage up to the day Noah entered the ark."),
      ("Matthew 22:30", "At the resurrection people will neither marry nor be given in marriage; they will be like the angels in heaven."),
      ("1 Corinthians 7:38", "So then, he who marries the virgin does right, but he who does not marry her does even better."),
      ("Revelation 19:7", "Let us rejoice and be glad and give him glory! For the wedding of the Lamb has come, and his bride has made herself ready.")],
     [("G1062", "Gamos (Wedding/Marriage)"), ("G3952", "Parousia (Coming)"), ("G3067", "Loutron (Washing)")]),

    (1549, "ἔκγονος", "Ekgonos", "Adjective/Noun", "Grandchild, Descendant",
     "A grandchild or descendant — used in family responsibility passages.",
     "The Greek <em>ekgonos</em> (plural <em>ekgona</em>) means grandchildren or descendants. It appears only in 1 Timothy 5:4: 'But if a widow has children or grandchildren (<em>ekgona</em>), these should learn first of all to put their religion into practice by caring for their own family and so repaying their parents and grandparents, for this is pleasing to God.' The text establishes that godliness includes concrete, generational family responsibility.",
     "The theology of <em>ekgona</em> in 1 Timothy 5:4 grounds piety in the home. Paul is addressing the church's care for widows — a real economic and social burden on the early community. His principle: before the church bears the financial weight, the family must. Children and <em>ekgona</em> have the first obligation. 'Anyone who does not provide for their relatives, and especially for their own household, has denied the faith and is worse than an unbeliever' (1 Timothy 5:8). Discipleship that ignores family responsibility is not devotion — it is avoidance dressed as spirituality.",
     [("1 Timothy 5:4", "But if a widow has children or <em>grandchildren</em>, these should learn first of all to put their religion into practice by caring for their own family."),
      ("1 Timothy 5:8", "Anyone who does not provide for their relatives, and especially for their own household, has denied the faith and is worse than an unbeliever."),
      ("Mark 7:10", "For Moses said, 'Honor your father and mother,' and, 'Anyone who curses their father or mother is to be put to death.'"),
      ("Proverbs 17:6", "Children's children are a crown to the aged, and parents are the pride of their children."),
      ("Exodus 20:12", "Honor your father and your mother, so that you may live long in the land the LORD your God is giving you.")],
     [("G5043", "Teknon (Child)"), ("G3624", "Oikos (Household)"), ("G5087", "Tithēmi (To Place/Appoint)")]),

    (1550, "ἐκδαπανάω", "Ekdapanaō", "Verb", "To Spend Completely, Exhaust Oneself",
     "To spend entirely, to exhaust oneself — used of Paul's self-giving for the Corinthians.",
     "The Greek <em>ekdapanaō</em> means to spend completely or exhaust. Paul uses it only in 2 Corinthians 12:15: 'So I will very gladly spend for you everything I have and expend myself as well (<em>ekdapanēthēsomai</em>). If I love you more, will you love me less?' The word carries the image of total depletion — spending not just money but one's very life-energy for others.",
     "Paul's <em>ekdapanaō</em> in 2 Corinthians 12:15 is the language of radical pastoral self-gift. He is defending his apostleship against the 'super-apostles' (2 Corinthians 11:5) who took money from the Corinthians while Paul refused. His point: 'I ask for nothing; I give everything.' The verb <em>ekdapanaō</em> (to be completely spent) echoes Jesus' own self-giving — 'the Son of Man came not to be served but to serve, and to give his life as a ransom for many' (Mark 10:45). The pastor who exhausts himself for the flock is most like the Shepherd who gave his life for the sheep.",
     [("2 Corinthians 12:15", "So I will very gladly spend for you everything I have and <em>expend myself</em> as well. If I love you more, will you love me less?"),
      ("Philippians 2:17", "But even if I am being poured out like a drink offering on the sacrifice and service coming from your faith, I am glad and rejoice with all of you."),
      ("Mark 10:45", "For even the Son of Man did not come to be served, but to serve, and to give his life as a ransom for many."),
      ("John 15:13", "Greater love has no one than this: to lay down one's life for one's friends."),
      ("Romans 9:3", "For I could wish that I myself were cursed and cut off from Christ for the sake of my people, those of my own race.")],
     [("G1159", "Dapanaō (To Spend)"), ("G26", "Agapē (Love)"), ("G652", "Apostolos (Apostle)")]),
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
