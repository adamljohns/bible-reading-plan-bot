#!/usr/bin/env python3
"""Generate 100 lexicon gap-fill pages for USMC Ministries."""
import os

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{sid} — {trans} | USMC Ministries Lexicon">
    <meta property="og:description" content="{og_desc}">
    <meta name="description" content="{og_desc} USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{sid} — {trans} ({gloss}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; --scarlet:#CC0000; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; font-weight:700; }}
        .container {{ max-width:800px; margin:0 auto; padding:20px; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a:link,nav a:visited,nav a:active {{ color:var(--gray) !important; text-decoration:none !important; }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .word-header {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .strongs-badge {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }}
        .original-word {{ font-size:3rem; margin:15px 0 10px; color:var(--gold-light); }}
        .transliteration {{ font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }}
        .pos {{ color:var(--gray); font-size:0.95rem; margin-bottom:10px; }}
        .gloss {{ color:var(--gold); font-size:1.1rem; font-weight:600; }}
        .section {{ background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }}
        .section h2 {{ color:var(--gold); font-size:1.3rem; margin-bottom:16px; }}
        .section p {{ color:var(--white); line-height:1.8; margin-bottom:12px; }}
        .section p em {{ color:var(--gold-light); font-style:italic; }}
        .section p strong {{ color:var(--white); }}
        .verse-entry {{ margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }}
        .verse-ref {{ color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }}
        .verse-ref:hover {{ color:var(--gold-light); border-bottom-style:solid; }}
        .verse-text {{ color:var(--gray); line-height:1.7; }}
        .verse-text em {{ color:var(--gold-light); font-style:italic; }}
        .verse-text strong {{ color:var(--white); }}
        .related-words {{ display:flex; flex-wrap:wrap; gap:10px; }}
        .related-word {{ display:inline-block; background:rgba(212,175,55,0.1); border:1px solid var(--border); color:var(--gold); text-decoration:none; padding:6px 14px; border-radius:20px; font-size:0.85rem; transition:all 0.2s; }}
        a.related-word:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.2); }}
        .ext-links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }}
        .ext-link {{ color:var(--gold); text-decoration:none; padding:8px 18px; border:1px solid var(--border); border-radius:8px; font-size:0.9rem; transition:all 0.2s; }}
        .ext-link:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.1); }}
        .back-link {{ display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }}
        .back-link:hover {{ color:var(--gold-light); }}
        footer {{ text-align:center; padding:40px 20px; color:var(--gray); font-size:0.85rem; border-top:1px solid var(--border); margin-top:40px; }}
        footer a {{ color:var(--gold); text-decoration:none; }}
        @media (max-width:640px) {{ .container {{ padding:15px; }} .original-word {{ font-size:2.2rem; }} }}
        body.light-mode{{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}}body.light-mode nav{{background:rgba(250,248,245,0.97);}}body.light-mode .section{{background:#fff;border-color:#d4d0c8;}}body.light-mode .ext-link{{border-color:#d4d0c8;}}body.light-mode .related-word{{background:rgba(212,175,55,0.08);border-color:#d4d0c8;}}body.light-mode footer{{border-top-color:#d4d0c8;}}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div class="container">
        <a href="../lexicon.html" class="back-link">← Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">{sid} · {lang_label}</span>
            <div class="original-word">{word}</div>
            <div class="transliteration">{trans}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{defn}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{usage}</p>
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
                <a href="{step_url}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="{blb_url}" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="{bh_url}" target="_blank" class="ext-link">📗 Bible Hub</a>
            </div>
        </div>
    </div>
    <div style="text-align:center;margin:24px auto 10px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="display:inline-flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
            <span style="width:18px;text-align:center;">🌙</span>
            <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
            <span style="width:18px;text-align:center;">☀️</span>
        </div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">© 2026 <a href="../index.html">U.S.M.C. Ministries</a> · <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
    <script>function bteToggleTheme(){{var b=document.body;if(b.classList.contains("light-mode")){{b.classList.remove("light-mode");localStorage.setItem("bte-theme","dark");}}else{{b.classList.add("light-mode");localStorage.setItem("bte-theme","light");}}}}(function(){{if(localStorage.getItem("bte-theme")==="light"){{document.body.classList.add("light-mode");}}}})();</script>
</body>
</html>'''


def verse_html(ref, text):
    return f'''                <div class="verse-entry">
                    <a href="../bible.html?ref={ref.replace(' ', '+')}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>'''

def related_html(sid, name):
    return f'                <a href="{sid}.html" class="related-word">{sid} — {name}</a>'

def build(sid, word, trans, pos, gloss, og_desc, defn, usage, verses, related):
    lang = "G" if sid.startswith("G") else "H"
    lang_label = "Greek · New Testament" if lang == "G" else "Hebrew · Old Testament"
    num = sid[1:]
    if lang == "G":
        step_url = f"https://www.stepbible.org/?q=strong={sid}"
        blb_url = f"https://www.blueletterbible.org/lexicon/g{num}/kjv/tr/0-1/"
        bh_url = f"https://biblehub.com/greek/{num}.htm"
    else:
        step_url = f"https://www.stepbible.org/?q=strong={sid}"
        blb_url = f"https://www.blueletterbible.org/lexicon/h{num}/kjv/wlc/0-1/"
        bh_url = f"https://biblehub.com/hebrew/{num}.htm"

    vh = "\n".join(verse_html(r, t) for r, t in verses)
    rh = "\n".join(related_html(s, n) for s, n in related)

    html = TEMPLATE.format(
        sid=sid, word=word, trans=trans, pos=pos, gloss=gloss,
        og_desc=og_desc, defn=defn, usage=usage,
        lang_label=lang_label, step_url=step_url, blb_url=blb_url, bh_url=bh_url,
        verses_html=vh, related_html=rh
    )
    path = os.path.join(LEXICON_DIR, f"{sid}.html")
    with open(path, 'w') as f:
        f.write(html)
    print(f"  ✓ {sid}")

# ═══════════════════════════════════════════════════════════
# GREEK ENTRIES (50)
# ═══════════════════════════════════════════════════════════

ENTRIES = [
# --- G5454 ---
("G5454", "φωλεός", "phōleós", "Noun, masculine", "Hole, Den, Lair",
 "Phōleós — the foxes have holes; Christ's voluntary homelessness. Strong's G5454.",
 "<em>Phōleós</em> (φωλεός) refers to a <strong>den, burrow, or lair</strong> — the hiding place of a wild animal such as a fox. It appears in the Gospels in one of Jesus' most poignant statements about the cost of discipleship.",
 "Jesus uses <em>phōleós</em> in Matthew 8:20 and Luke 9:58: 'Foxes have <em>dens</em> and birds have nests, but the Son of Man has no place to lay his head.' This voluntary poverty reveals the depth of the incarnation — the Creator of all had no earthly home. The statement simultaneously warns would-be disciples of the cost of following Jesus and reveals His identification with the displaced and homeless. It echoes Isaiah 53:3 and anticipates 2 Corinthians 8:9: 'though he was rich, yet for your sake he became poor.' <strong>The one who owns everything chose to own nothing</strong> so that we might inherit everything.",
 [("Matthew 8:20", "Jesus replied, 'Foxes have <em>dens</em> and birds have nests, but the Son of Man has no place to lay his head.'"),
  ("Luke 9:58", "Jesus replied, 'Foxes have <em>dens</em> and birds have nests, but the Son of Man has no place to lay his head.'"),
  ("2 Corinthians 8:9", "For you know the grace of our Lord Jesus Christ, that though he was rich, yet for your sake he became poor.")],
 [("G258", "Alōpēx (Fox)"), ("G4071", "Peteinon (Bird)"), ("G2646", "Katalyma (Lodging)")]),

# --- G2820 ---
("G2820", "κληρόω", "klēróō", "Verb", "To Obtain by Lot, To Choose",
 "Klēróō — to assign by lot or divine appointment; election by grace. Strong's G2820.",
 "<em>Klēróō</em> (κληρόω) means <strong>to assign by lot, to allot, to obtain as one's inheritance</strong>. In the passive, it conveys being chosen or predestined — receiving one's portion by divine appointment rather than human merit.",
 "Ephesians 1:11 uses the passive: believers '<em>have obtained an inheritance</em>, having been predestined according to the plan of him who works out everything in conformity with the purpose of his will.' The theological weight is immense: salvation is by <strong>divine lot and election</strong>, not human achievement. God's people are His <em>klēros</em> — His chosen possession. This echoes Deuteronomy 32:9: 'the LORD's portion is his people, Jacob his allotted inheritance,' and connects to 1 Peter 2:9: 'a chosen people, a royal priesthood, God's special possession.'",
 [("Ephesians 1:11", "In him we were also chosen (<em>eklērōthēmen</em>), having been predestined according to the plan of him who works out everything in conformity with the purpose of his will."),
  ("Deuteronomy 32:9", "For the LORD's portion is his people, Jacob his allotted inheritance."),
  ("1 Peter 2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession.")],
 [("G2819", "Klēros (Lot/Inheritance)"), ("G4309", "Proorizō (Predestine)"), ("G1589", "Eklogē (Election)")]),

# --- G2297 ---
("G2297", "θαυμάσιος", "thaumásios", "Adjective", "Wonderful, Marvelous",
 "Thaumásios — wonderful things that evoke awe. Strong's G2297.",
 "<em>Thaumásios</em> (θαυμάσιος) means <strong>wonderful, marvelous, astonishing</strong> — that which causes wonder and amazement. Derived from <em>thaumazō</em> (to marvel), it describes what transcends ordinary experience.",
 "In Matthew 21:15, the chief priests are indignant at the '<em>wonderful things</em>' Jesus did in the temple — healings and children's praise. The irony is sharp: those who should recognize the Messiah's wonders are offended by them. This contrasts with Psalm 118:23: 'The Lord has done this, and it is <em>marvelous</em> in our eyes.' <strong>God's works should leave us breathless with childlike wonder</strong>, not stiff with religious cynicism. All of God's redemptive acts — creation, exodus, incarnation, resurrection — are <em>thaumásia</em>.",
 [("Matthew 21:15", "But when the chief priests and the teachers of the law saw the <em>wonderful things</em> he did and the children shouting 'Hosanna,' they were indignant."),
  ("Psalm 118:23", "The LORD has done this, and it is marvelous in our eyes."),
  ("Psalm 139:14", "I praise you because I am fearfully and wonderfully made; your works are wonderful.")],
 [("G2296", "Thaumazō (To Marvel)"), ("G2298", "Thaumastos (Marvelous)"), ("G1411", "Dynamis (Power/Miracle)")]),

# --- G3698 ---
("G3698", "ὁπότε", "hopóte", "Conjunction", "When, At Which Time",
 "Hopóte — when; God's sovereign timing in redemptive history. Strong's G3698.",
 "<em>Hopóte</em> (ὁπότε) is a temporal conjunction meaning <strong>when, at which time, whenever</strong>. It combines the relative pronoun with <em>pote</em> (at some time). It appears in the Gospels to mark significant moments.",
 "In Luke 6:3, Jesus asks: 'Have you never read what David did <em>when</em> he and his companions were hungry?' Jesus uses this historical moment to establish that human need can take precedence over ceremonial law when rightly understood. The Sabbath was made for man, not man for the Sabbath. <em>Hopóte</em> marks a moment of necessity that revealed a principle of mercy. Throughout Scripture, <strong>God's timing is sovereign</strong>: 'when the set time had fully come, God sent his Son' (Galatians 4:4).",
 [("Luke 6:3", "Jesus answered them, 'Have you never read what David did <em>when</em> he and his companions were hungry?'"),
  ("Galatians 4:4", "But when the set time had fully come, God sent his Son, born of a woman, born under the law."),
  ("Ecclesiastes 3:1", "There is a time for everything, and a season for every activity under the heavens.")],
 [("G3753", "Hote (When)"), ("G3752", "Hotan (Whenever)"), ("G2540", "Kairos (Appointed Time)")]),

# --- G3542 ---
("G3542", "νομή", "nomḗ", "Noun, feminine", "Pasture, Spreading",
 "Nomē — pasture for sheep; also the spread of false teaching. Strong's G3542.",
 "<em>Nomē</em> (νομή) has two related meanings: (1) <strong>pasture, feeding ground</strong> — where flocks graze; and (2) <strong>spreading, increase</strong> — the advance of something like disease or error. Both senses appear in the NT.",
 "In John 10:9, Jesus promises those who enter through Him 'will come in and go out, and find <em>pasture</em>' — safe, abundant provision from the Good Shepherd. But in 2 Timothy 2:17, Paul warns that false teaching 'will spread like gangrene' — the same word now depicting something destructive. The contrast is instructive: <strong>truth nourishes and gives life; false doctrine spreads death</strong>. The shepherd image demands that elders protect the flock from teachings that eat away rather than feed.",
 [("John 10:9", "I am the gate; whoever enters through me will be saved. They will come in and go out, and find <em>pasture</em>."),
  ("2 Timothy 2:17", "Their teaching will spread like gangrene. Among them are Hymenaeus and Philetus."),
  ("Psalm 23:2", "He makes me lie down in green pastures, he leads me beside quiet waters.")],
 [("G4166", "Poimēn (Shepherd)"), ("G4168", "Poimnē (Flock)"), ("G1319", "Didaskalia (Teaching)")]),

# --- G3409 ---
("G3409", "μισθόω", "misthóō", "Verb", "To Hire for Wages",
 "Misthóō — to hire laborers; the parable of scandalous grace. Strong's G3409.",
 "<em>Misthóō</em> (μισθόω) means <strong>to hire, to employ for wages</strong>. In the middle voice it means to hire for one's own use. Related to <em>misthos</em> (wages, reward).",
 "The word appears in Matthew 20:1 in the Parable of the Laborers in the Vineyard. The landowner <em>hires</em> workers at different hours yet pays them all the same wage. The parable subverts all human calculations of merit: <strong>God's grace cannot be earned by length of service.</strong> Those hired at the eleventh hour — latecomers to faith — receive the same eternal life as those who labored longest. This is scandalous grace. The parable also challenges envy among God's people: 'Are you envious because I am generous?' (v.15).",
 [("Matthew 20:1", "For the kingdom of heaven is like a landowner who went out early in the morning to <em>hire</em> workers for his vineyard."),
  ("Matthew 20:7", "'Because no one has <em>hired</em> us.' He said to them, 'You also go and work in my vineyard.'"),
  ("Matthew 20:15", "'Don't I have the right to do what I want with my own money? Or are you envious because I am generous?'")],
 [("G3408", "Misthos (Wages/Reward)"), ("G3411", "Misthios (Hired Worker)"), ("G2040", "Ergatēs (Laborer)")]),

# --- G2968 ---
("G2968", "κώμη", "kṓmē", "Noun, feminine", "Village, Small Town",
 "Kōmē — village; Jesus' ministry reached every small community. Strong's G2968.",
 "<em>Kōmē</em> (κώμη) refers to a <strong>village or small town</strong> — a rural settlement smaller than a city (<em>polis</em>). It appears frequently in the Gospels and Acts.",
 "The Gospels emphasize that Jesus' ministry encompassed every <em>kōmē</em>. Matthew 9:35: 'Jesus went through all the towns and <em>villages</em>, teaching and healing every disease.' This is total, exhaustive ministry — <strong>no community too small, no person too insignificant</strong>. Jesus sent His disciples to villages (Mark 6:6; Luke 9:6). The Kingdom of God came to ordinary places through ordinary people. This challenges any gospel that only targets the powerful and urban.",
 [("Matthew 9:35", "Jesus went through all the towns and <em>villages</em>, teaching in their synagogues, proclaiming the good news of the kingdom."),
  ("Mark 6:56", "And wherever he went — into <em>villages</em>, towns or countryside — they placed the sick in the marketplaces."),
  ("Luke 9:6", "So they set out and went from <em>village</em> to <em>village</em>, proclaiming the good news and healing people everywhere.")],
 [("G4172", "Polis (City)"), ("G68", "Agros (Field)"), ("G2969", "Kōmopolis (Country Town)")]),

# --- G2769 ---
("G2769", "κεράτιον", "kerátion", "Noun, neuter", "Carob Pod, Husks",
 "Kerátion — the pods the prodigal son longed to eat; rock bottom. Strong's G2769.",
 "<em>Kerátion</em> (κεράτιον) literally means 'little horn' and refers to the <strong>carob pod</strong> — seed pods of the carob tree used as animal fodder. It appears once in the NT, in one of Jesus' most powerful parables.",
 "In Luke 15:16, the prodigal son longs to eat the <em>kerátion</em> — the pods the pigs were eating. A Jewish young man feeding unclean animals and desiring their food has reached the lowest imaginable point. But it is precisely here — at the carob pods — that he 'comes to his senses' (v.17). <strong>The <em>kerátion</em> is the turning point, the moment of repentance.</strong> Often, God uses the lowest circumstances to awaken the soul to its need for the Father. The Father didn't chase — He waited, watched, and ran to meet the returning son.",
 [("Luke 15:16", "He longed to fill his stomach with the <em>pods</em> that the pigs were eating, but no one gave him anything."),
  ("Luke 15:17", "When he came to his senses, he said, 'How many of my father's hired servants have food to spare!'"),
  ("Luke 15:20", "So he got up and went to his father. But while he was still a long way off, his father saw him and was filled with compassion.")],
 [("G5519", "Choiros (Pig)"), ("G3341", "Metanoia (Repentance)"), ("G4697", "Splanchnizomai (Compassion)")]),

# --- G5020 ---
("G5020", "ταρταρόω", "tartaróō", "Verb", "To Cast into Tartarus",
 "Tartaróō — to confine fallen angels to deepest darkness. Strong's G5020.",
 "<em>Tartaróō</em> (ταρταρόω) means <strong>to cast into Tartarus</strong> — the lowest abyss beneath Hades. In Greek mythology, Tartarus was the prison for the worst offenders. Peter borrows this term for divine judgment on fallen angels.",
 "Second Peter 2:4: 'God did not spare angels when they sinned, but cast them into hell (<em>tartarōsas</em>), putting them in chains of darkness to be held for judgment.' This is one of three examples of God's certain judgment (the others: Noah's flood and Sodom). <strong>If God did not spare even angels, how much more certain is judgment on unrepentant humans?</strong> Yet Peter also affirms 'the Lord knows how to rescue the godly from trials' (v.9). Divine wrath and divine rescue go together.",
 [("2 Peter 2:4", "For if God did not spare angels when they sinned, but sent them to <em>Tartarus</em>, putting them in chains of darkness to be held for judgment..."),
  ("Jude 1:6", "And the angels who did not keep their positions of authority — these he has kept in darkness, bound with everlasting chains for judgment."),
  ("Revelation 20:10", "And the devil, who deceived them, was thrown into the lake of burning sulfur.")],
 [("G86", "Hadēs (Underworld)"), ("G12", "Abyssos (The Abyss)"), ("G2920", "Krisis (Judgment)")]),

# --- G2683 ---
("G2683", "κατασκιάζω", "kataskiázō", "Verb", "To Overshadow, To Cast Shadow Over",
 "Kataskiázō — the cherubim overshadowing the mercy seat. Strong's G2683.",
 "<em>Kataskiázō</em> (κατασκιάζω) means <strong>to overshadow, to cast a shadow over, to cover with shade</strong>. From <em>kata</em> (down upon) + <em>skiazō</em> (to shade). It appears once in the NT in the description of the tabernacle.",
 "Hebrews 9:5 describes the cherubim of glory '<em>overshadowing</em> the mercy seat.' The mercy seat (<em>hilastērion</em>) was where atonement was made — where God's presence met the blood of sacrifice. The cherubim overshadowing it represented <strong>divine guardianship of the place of reconciliation</strong>. This imagery runs from Eden (cherubim guarding the way to the tree of life, Genesis 3:24) through the tabernacle to Christ Himself, who is our mercy seat (Romans 3:25). The shadow of the cherubim speaks of holy protection over the place where God and sinners meet.",
 [("Hebrews 9:5", "Above the ark were the cherubim of the Glory, <em>overshadowing</em> the atonement cover."),
  ("Exodus 25:20", "The cherubim are to have their wings spread upward, overshadowing the cover with them."),
  ("Romans 3:25", "God presented Christ as a sacrifice of atonement, through the shedding of his blood.")],
 [("G2435", "Hilastērion (Mercy Seat)"), ("G5502", "Cheroubim (Cherubim)"), ("G4639", "Skia (Shadow)")]),

# --- G5232 ---
("G5232", "ὑπεραυξάνω", "hyperauxánō", "Verb", "To Grow Exceedingly",
 "Hyperauxánō — faith growing beyond all measure. Strong's G5232.",
 "<em>Hyperauxánō</em> (ὑπεραυξάνω) is a compound verb: <em>hyper</em> (over, beyond) + <em>auxanō</em> (to grow). It means <strong>to grow exceedingly, to increase beyond measure</strong>. A superlative of spiritual growth. Appears once in the NT.",
 "Paul uses it in 2 Thessalonians 1:3: 'your faith is <em>growing exceedingly</em> and the love all of you have for one another is increasing.' This is remarkable encouragement — not gradual growth but growth <em>beyond all measure</em>. <strong>Spiritual growth through trials is not linear but exponential.</strong> Faith exercised through persecution grows dramatically. God's design is not maintenance-mode Christianity but faith that overflows its banks, faith that <em>hyperauxanō</em>.",
 [("2 Thessalonians 1:3", "We ought always to thank God for you, because your faith is <em>growing exceedingly</em> and the love all of you have for one another is increasing."),
  ("Colossians 1:10", "...growing in the knowledge of God, being strengthened with all power."),
  ("1 Peter 2:2", "Like newborn babies, crave pure spiritual milk, so that by it you may grow up in your salvation.")],
 [("G837", "Auxanō (To Grow)"), ("G4052", "Perisseuō (To Abound)"), ("G4102", "Pistis (Faith)")]),

# --- G4437 ---
("G4437", "πυκνός", "pyknós", "Adjective", "Frequent, Often, Dense",
 "Pyknós — frequent prayer and devotion without ceasing. Strong's G4437.",
 "<em>Pyknós</em> (πυκνός) means <strong>frequent, often, thick, dense</strong>. It describes regularity and intensity of practice. In the NT it appears in contexts of religious devotion and spiritual discipline.",
 "Luke 5:33 contrasts the disciples of John and the Pharisees who fast '<em>often</em>' (<em>pykna</em>) with Jesus' disciples who eat and drink. Jesus responds with the bridegroom metaphor — fasting will come when the bridegroom is taken away. In Acts 24:26, Felix '<em>frequently</em>' sent for Paul, hoping for a bribe. First Timothy 5:23 uses it of Timothy's '<em>frequent</em> ailments.' <strong>The word challenges us: what are we frequent about?</strong> Paul's command to 'pray without ceasing' (1 Thessalonians 5:17) calls for <em>pyknos</em> devotion — consistent, dense, unrelenting communion with God.",
 [("Luke 5:33", "John's disciples <em>often</em> fast and pray, and so do the disciples of the Pharisees, but yours go on eating and drinking."),
  ("Acts 24:26", "He <em>frequently</em> sent for Paul and talked with him, because he was hoping that Paul would offer him a bribe."),
  ("1 Thessalonians 5:17", "Pray without ceasing.")],
 [("G4336", "Proseuchomai (To Pray)"), ("G3522", "Nēsteuō (To Fast)"), ("G1619", "Ektenēs (Earnest/Fervent)")]),

# --- G2338 ---
("G2338", "θῆλυς", "thḗlys", "Adjective", "Female",
 "Thēlys — female; God's creation design and equal image-bearing. Strong's G2338.",
 "<em>Thēlys</em> (θῆλυς) means <strong>female</strong> — of the female sex. It appears in creation, marriage, and anthropological texts. Related to <em>thēlazō</em> (to nurse), reflecting nurture.",
 "Jesus quotes Genesis 1:27 in Matthew 19:4: 'at the beginning the Creator made them male and <em>female</em>' — <em>arsen kai thēly</em> — establishing sexual differentiation as <strong>God's design, not cultural accident</strong>. Galatians 3:28 declares 'neither male nor <em>female</em>... in Christ' — not erasing distinction but affirming that both equally bear God's image and receive salvation. The creation of humanity as male and female reflects the relational nature of God Himself.",
 [("Matthew 19:4", "Haven't you read that at the beginning the Creator 'made them male and <em>female</em>'?"),
  ("Galatians 3:28", "There is neither Jew nor Gentile, neither slave nor free, nor is there male and <em>female</em>, for you are all one in Christ Jesus."),
  ("Genesis 1:27", "So God created mankind in his own image... male and female he created them.")],
 [("G730", "Arsēn (Male)"), ("G1135", "Gynē (Woman/Wife)"), ("G444", "Anthrōpos (Human Being)")]),

# --- G2327 ---
("G2327", "θερισμός", "therismós", "Noun, masculine", "Harvest, Reaping",
 "Therismós — the harvest of souls; urgency of the gospel. Strong's G2327.",
 "<em>Therismós</em> (θερισμός) means <strong>harvest</strong> — the reaping of grain at the end of the growing season. Biblically, it becomes a rich metaphor for the gathering of souls in evangelism and final judgment.",
 "Jesus uses <em>therismós</em> in multiple ways. Matthew 9:37-38: 'the harvest is plentiful but the workers are few' — a call to urgent evangelism. Matthew 13:39: 'the harvest is the end of the age' — final judgment when angels separate righteous from wicked. John 4:35: 'open your eyes, the fields are ripe for harvest!' <strong>Harvest theology demands urgency</strong>: seasons pass, opportunity closes, and God calls His people to participate in His redemptive work before the final reaping.",
 [("Matthew 9:37-38", "The <em>harvest</em> is plentiful but the workers are few. Ask the Lord of the harvest to send out workers."),
  ("Matthew 13:39", "The <em>harvest</em> is the end of the age, and the harvesters are angels."),
  ("John 4:35", "Open your eyes and look at the fields! They are ripe for <em>harvest</em>.")],
 [("G2325", "Therizō (To Reap)"), ("G4687", "Speirō (To Sow)"), ("G2326", "Theristēs (Reaper)")]),

# --- G2713 ---
("G2713", "κατέναντι", "katénanti", "Preposition/Adverb", "Opposite, In the Presence Of",
 "Katénanti — in the sight of God; faith before His face. Strong's G2713.",
 "<em>Katénanti</em> (κατέναντι) means <strong>opposite, over against, in front of, in the presence of</strong>. A strengthened form of <em>enanti</em>. It appears in both geographical and theological contexts.",
 "The most theologically weighty use is Romans 4:17: Abraham had faith '<em>katénanti</em> God' — in His very presence, before His face. This intensifies Abraham's faith: it was not theoretical belief but <strong>faith exercised in direct relationship with the God who sees all</strong>. God's omniscience means faith is never private — always before His face. This appears also in 2 Corinthians 2:17: 'in Christ we speak before God with sincerity.'",
 [("Romans 4:17", "He is our father in the sight of God (<em>katénanti</em>), in whom he believed — the God who gives life to the dead."),
  ("2 Corinthians 2:17", "In Christ we speak before God with sincerity, as those sent from God."),
  ("Hebrews 4:13", "Nothing in all creation is hidden from God's sight. Everything is laid bare before him.")],
 [("G1799", "Enōpion (Before/In the Presence)"), ("G4383", "Prosōpon (Face)"), ("G3708", "Horaō (To See)")]),

# --- G3380 ---
("G3380", "μήπω", "mḗpō", "Adverb", "Not Yet",
 "Mēpō — not yet; God's sovereign election before merit. Strong's G3380.",
 "<em>Mḗpō</em> (μήπω) means <strong>not yet</strong> — indicating something anticipated but not yet occurred. Compound of <em>mē</em> (not) + <em>pō</em> (yet).",
 "Romans 9:11 uses <em>mēpō</em> to make a crucial point about election: 'before the twins were born or had done anything good or bad — <em>not yet</em> having done anything — God's purpose in election might stand: not by works but by him who calls.' <strong>This is one of the strongest statements of sovereign grace in all Scripture.</strong> God's choice preceded all human action. Similarly, Hebrews 12:4 ('you have <em>not yet</em> resisted to the point of shedding your blood') encourages perseverance.",
 [("Romans 9:11", "Before the twins were born or had done anything good or bad — in order that God's purpose in election might stand..."),
  ("Hebrews 12:4", "In your struggle against sin, you have <em>not yet</em> resisted to the point of shedding your blood."),
  ("John 7:39", "Up to that time the Spirit had <em>not yet</em> been given, since Jesus had not yet been glorified.")],
 [("G3768", "Oupō (Not Yet)"), ("G4309", "Proorizō (Predestine)"), ("G5485", "Charis (Grace)")]),

# --- G3468 ---
("G3468", "μώλωψ", "mṓlōps", "Noun, masculine", "Bruise, Stripe, Wound",
 "Mōlōps — the stripes of Christ by which we are healed. Strong's G3468.",
 "<em>Mṓlōps</em> (μώλωψ) means <strong>a bruise, weal, or stripe</strong> left by a blow or flogging — the mark on skin from a lash. It appears once in the NT, in a passage of enormous theological significance.",
 "First Peter 2:24 quotes Isaiah 53:5: 'He himself bore our sins in his body on the cross... by his <em>wounds</em> (<em>mōlōpi</em>) you have been healed.' The singular <em>mōlōpi</em> is a collective — the totality of Christ's wounds in His flogging and crucifixion. Isaiah 53 was written 700 years before the cross yet describes it with precision. <strong>Christ's wounds are our healing — His pain purchased our peace.</strong> The one who bore stripes without retaliation is the pattern for all who suffer unjustly.",
 [("1 Peter 2:24", "He himself bore our sins in his body on the cross... by his <em>wounds</em> you have been healed."),
  ("Isaiah 53:5", "He was pierced for our transgressions, crushed for our iniquities; the punishment that brought us peace was on him."),
  ("Isaiah 53:7", "He was led like a lamb to the slaughter, and as a sheep before its shearers is silent, so he did not open his mouth.")],
 [("G3817", "Paiō (To Strike)"), ("G2386", "Iama (Healing)"), ("G629", "Apolytrōsis (Redemption)")]),

# --- G4829 ---
("G4829", "συμμερίζομαι", "symmerízomai", "Verb", "To Share In Together",
 "Symmerízomai — sharing together in the blessings of ministry. Strong's G4829.",
 "<em>Symmerízomai</em> (συμμερίζομαι) means <strong>to share in something together, to partake jointly</strong>. From <em>syn</em> (together) + <em>merizō</em> (to divide/share).",
 "First Corinthians 9:13: those who serve at the altar '<em>share in</em>' what is offered on the altar. Paul argues that gospel ministers deserve material support, though he voluntarily waives this right. <strong>Ministry creates a community of mutual participation.</strong> Those who receive spiritual blessing have responsibility to share materially (Romans 15:27; Galatians 6:6). The early church's radical generosity was evidence of genuine koinōnia.",
 [("1 Corinthians 9:13", "Those who serve at the altar <em>share in</em> what is offered on the altar."),
  ("Galatians 6:6", "The one who receives instruction in the word should share all good things with their instructor."),
  ("Romans 15:27", "If the Gentiles have shared in the Jews' spiritual blessings, they owe it to share their material blessings.")],
 [("G2841", "Koinōneō (To Share)"), ("G2842", "Koinōnia (Fellowship)"), ("G3307", "Merizō (To Divide)")]),

# --- G5285 ---
("G5285", "ὑποπνέω", "hypopnéō", "Verb", "To Blow Gently",
 "Hypopnéō — a gentle wind that gave false confidence before the storm. Strong's G5285.",
 "<em>Hypopnéō</em> (ὑποπνέω) means <strong>to blow gently, to blow softly</strong>. From <em>hypo</em> (gently) + <em>pneō</em> (to blow). Appears once in Acts.",
 "Acts 27:13: 'when a <em>gentle south wind</em> began to blow, they thought they had obtained what they wanted; so they weighed anchor.' This gentle wind gave the sailors false confidence — they proceeded despite Paul's warning, then the northeaster struck. <strong>Favorable circumstances are not always God's green light.</strong> Smooth sailing can deceive us into ignoring wise counsel. Yet even this mistake was in God's providence — it led Paul to Rome as promised. Even our errors cannot thwart God's plan.",
 [("Acts 27:13", "When a <em>gentle south wind</em> began to blow, they thought they had obtained what they wanted."),
  ("Acts 27:14", "Before very long, a wind of hurricane force, called the Northeaster, swept down from the island."),
  ("Proverbs 3:5-6", "Trust in the LORD with all your heart and lean not on your own understanding.")],
 [("G417", "Anemos (Wind)"), ("G4157", "Pnoē (Breath/Wind)"), ("G3558", "Notos (South Wind)")]),

# --- G2303 ---
("G2303", "θεῖον", "theîon", "Noun, neuter", "Brimstone, Sulfur",
 "Theîon — brimstone; divine fire of judgment. Strong's G2303.",
 "<em>Theîon</em> (θεῖον) means <strong>brimstone or sulfur</strong> — the burning mineral of divine judgment. The word shares its root with <em>theos</em> (God), reflecting the ancient view that burning sulfur was 'divine fire.'",
 "Brimstone in Scripture consistently signals <strong>divine wrath</strong>. Sodom and Gomorrah established the archetype (Genesis 19:24). Revelation amplifies it: the lake of fire burns with <em>theion</em> — final destination for Satan, the beast, and all whose names are absent from the Book of Life (Revelation 19:20; 20:10; 21:8). A God who tolerates evil forever is not holy. The lake of fire expresses that God takes sin seriously. The good news: Christ drank the cup of wrath so believers need not.",
 [("Revelation 21:8", "Their place will be in the fiery lake of burning <em>sulfur</em>."),
  ("Revelation 19:20", "The two of them were thrown alive into the fiery lake of burning <em>sulfur</em>."),
  ("Genesis 19:24", "Then the LORD rained down burning sulfur on Sodom and Gomorrah.")],
 [("G4442", "Pyr (Fire)"), ("G3041", "Limnē (Lake)"), ("G2288", "Thanatos (Death)")]),

# --- G5095 ---
("G5095", "Τιμόθεος", "Timótheos", "Proper Noun", "Timothy — Honoring God",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G3275 ---
("G3275", "Ἰαείρος", "Iaeiros", "Proper Noun", "Jairus",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G5505 ---
("G5505", "χίλιοι", "chílioi", "Adjective/Numeral", "One Thousand",
 "Chílioi — a thousand; the millennial reign and God's eternal perspective. Strong's G5505.",
 "<em>Chílioi</em> (χίλιοι) means <strong>one thousand</strong>. Theologically significant as a symbol of completeness, fullness, and divine abundance, appearing repeatedly in Revelation.",
 "In Revelation 20:1-7, <em>chílioi</em> appears six times in the millennium — Satan bound 'for a thousand years,' saints reigning 'for a thousand years.' This is the foundation of <strong>millennial theology</strong>. Beyond eschatology, 2 Peter 3:8 (quoting Psalm 90:4): 'With the Lord a day is like a thousand years' — God's perspective on time is radically different from ours. Deuteronomy 7:9: God keeps faithfulness 'to a thousand generations.' The number speaks of God's inexhaustible patience and sovereignty over time.",
 [("Revelation 20:2-3", "He seized the dragon and bound him for a <em>thousand years</em>."),
  ("2 Peter 3:8", "With the Lord a day is like a <em>thousand years</em>, and a thousand years are like a day."),
  ("Deuteronomy 7:9", "The LORD your God... maintaining his love to a <em>thousand</em> generations.")],
 [("G5507", "Chiliás (A Thousand)"), ("G3461", "Myrias (Ten Thousand)"), ("G165", "Aiōn (Age/Eternity)")]),

# --- G5019 ---
("G5019", "Ταρσός", "Tarsós", "Proper Noun", "Tarsus",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G4426 ---
("G4426", "πτύρω", "ptýrō", "Verb", "To Terrify, To Frighten",
 "Ptýrō — do not be frightened by opponents; stand firm. Strong's G4426.",
 "<em>Ptýrō</em> (πτύρω) means <strong>to terrify, to frighten, to intimidate</strong>. In the passive, 'to be terrified or alarmed.' Originally used of startled horses. It appears once in the NT.",
 "Philippians 1:28: 'without being <em>frightened</em> in any way by those who oppose you.' Paul uses a word of panic — the kind that makes horses bolt — and tells the Philippians <strong>not to experience it</strong> when facing opposition. Courage in persecution is itself 'a sign to them that they will be destroyed, but that you will be saved — and that by God.' Fearlessness under pressure is theological testimony: it declares that God is sovereign, that death has been conquered, and that no opposition can separate us from Christ's love.",
 [("Philippians 1:28", "Without being <em>frightened</em> in any way by those who oppose you. This is a sign to them that they will be destroyed, but that you will be saved."),
  ("Isaiah 41:10", "Do not fear, for I am with you; do not be dismayed, for I am your God."),
  ("2 Timothy 1:7", "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline.")],
 [("G5399", "Phobéō (To Fear)"), ("G2292", "Tharréō (To Be Bold)"), ("G3954", "Parrhēsia (Boldness)")]),

# --- G3389 ---
("G3389", "μητραλῴας", "mētralṓias", "Noun, masculine", "One Who Strikes His Mother",
 "Mētralōias — violence against family; the law exposes the worst of sin. Strong's G3389.",
 "<em>Mētralṓias</em> (μητραλῴας) means <strong>one who strikes or kills his mother</strong>. From <em>mētēr</em> (mother) + <em>aloiaō</em> (to strike). It appears in Paul's vice list in 1 Timothy 1.",
 "First Timothy 1:9-10 lists those for whom the law exists: 'the lawless and rebellious... those who kill their fathers or <em>mothers</em>, murderers...' The list escalates from general to extreme violations. Striking a parent represented the ultimate violation of family honor and natural law. <strong>The law exposes sin in its most naked form</strong>, driving sinners to grace. Paul himself was once 'the worst of sinners' (1:15-16) and received mercy — no sin is beyond Christ's redemption.",
 [("1 Timothy 1:9-10", "The law is made for lawbreakers and rebels... for those who kill their fathers or <em>mothers</em>, for murderers..."),
  ("Ephesians 6:2", "'Honor your father and mother' — the first commandment with a promise."),
  ("Romans 5:20", "But where sin increased, grace increased all the more.")],
 [("G3964", "Patralōias (Father-Striker)"), ("G5406", "Phoneus (Murderer)"), ("G3551", "Nomos (Law)")]),

# --- G4558 ---
("G4558", "Σαρεπτά", "Sarepta", "Proper Noun", "Zarephath",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G5226 ---
("G5226", "ὑπείκω", "hypeíkō", "Verb", "To Submit, To Yield",
 "Hypeíkō — submit to leaders who watch over your soul. Strong's G5226.",
 "<em>Hypeíkō</em> (ὑπείκω) means <strong>to submit, to yield, to give way</strong>. It conveys deference to authority without resistance. Appears once in the NT.",
 "Hebrews 13:17: 'Have confidence in your leaders and <em>submit</em> to their authority, because they keep watch over you as those who must give an account.' The logic is pastoral accountability: leaders will answer to God for souls in their care. <strong>Christian submission is not servility but wisdom.</strong> It assumes leaders who are themselves submitted to God's Word. When leaders lead faithfully and congregants submit willingly, ministry becomes joy rather than burden.",
 [("Hebrews 13:17", "Have confidence in your leaders and <em>submit</em> to their authority, because they keep watch over you as those who must give an account."),
  ("1 Peter 5:5", "You who are younger, submit yourselves to your elders. Clothe yourselves with humility."),
  ("Ephesians 5:21", "Submit to one another out of reverence for Christ.")],
 [("G5293", "Hypotassō (To Submit)"), ("G3980", "Peitharcheō (To Obey)"), ("G4291", "Proistēmi (To Lead)")]),

# --- G3715 ---
("G3715", "ὄρεξις", "órexis", "Noun, feminine", "Desire, Appetite, Longing",
 "Orexis — desire and appetite; disordered when separated from God. Strong's G3715.",
 "<em>Orexis</em> (ὄρεξις) means <strong>desire, longing, appetite</strong> — the reaching out of the soul. Used in Greek philosophy for the appetitive faculty. Appears once in the NT, negatively.",
 "Romans 1:27 describes those 'inflamed with <em>lust</em>' — disordered <em>orexis</em>. Paul's point is not primarily about sexuality but about <strong>the corruption of all appetite when God is rejected</strong>. All desire was created good — for God, beauty, connection, nourishment. Separated from God, desires become consuming and destructive. The gospel restores <em>orexis</em> to proper order: 'Delight yourself in the LORD, and he will give you the desires of your heart' (Psalm 37:4).",
 [("Romans 1:27", "Men abandoned natural relations and were inflamed with <em>lust</em> for one another."),
  ("Psalm 37:4", "Take delight in the LORD, and he will give you the desires of your heart."),
  ("Galatians 5:24", "Those who belong to Christ have crucified the flesh with its passions and desires.")],
 [("G1939", "Epithymia (Desire/Lust)"), ("G3806", "Pathos (Passion)"), ("G4561", "Sarx (Flesh)")]),

# --- G2181 ---
("G2181", "Ἔφεσος", "Éphesos", "Proper Noun", "Ephesus",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G3080 ---
("G3080", "λύσις", "lýsis", "Noun, feminine", "Loosing, Release",
 "Lysis — release from bonds; Paul's counsel on marriage and freedom. Strong's G3080.",
 "<em>Lýsis</em> (λύσις) means <strong>loosing, releasing, dissolving</strong>. Derived from <em>lyō</em> (to loose). In the NT it refers to release from a commitment, specifically the marriage bond.",
 "First Corinthians 7:27: 'Are you pledged to a woman? Do not seek to be <em>released</em>. Are you free? Do not look for a wife.' Paul's counsel reflects eschatological urgency — singleness can allow undistracted devotion. He does not denigrate marriage (Hebrews 13:4 calls it honorable) but places it in eternal perspective. <strong>Both marriage and singleness are gifts when lived in consecration to God.</strong> What matters is full-hearted devotion to Christ in whatever state one finds oneself.",
 [("1 Corinthians 7:27", "Are you pledged to a woman? Do not seek to be <em>released</em>. Are you free? Do not look for a wife."),
  ("1 Corinthians 7:32", "An unmarried man is concerned about the Lord's affairs — how he can please the Lord."),
  ("Hebrews 13:4", "Marriage should be honored by all, and the marriage bed kept pure.")],
 [("G3089", "Lyō (To Loose)"), ("G1135", "Gynē (Woman/Wife)"), ("G1062", "Gamos (Marriage)")]),

# --- G4441 ---
("G4441", "πυνθάνομαι", "pynthánomai", "Verb", "To Inquire, To Ask",
 "Pynthánomai — to seek information diligently; the heart behind the question. Strong's G4441.",
 "<em>Pynthánomai</em> (πυνθάνομαι) means <strong>to inquire, to ask questions, to seek information</strong>. It implies deliberate inquiry — asking to find out something specific.",
 "The word appears at key moments. Matthew 2:4: Herod 'asked' where the Messiah was to be born — sinister inquiry with murderous intent. John 4:52: a royal official 'inquired' at what hour his son recovered — discovering healing simultaneous with Jesus' word. Acts 10:18: Cornelius' men ask for Peter. <strong>Inquiry is not inherently good or bad — the disposition of the heart matters.</strong> True seekers find (Matthew 7:7-8); those who inquire to destroy are judged.",
 [("Matthew 2:4", "He called together the chief priests and asked them where the Messiah was to be born."),
  ("John 4:52", "When he <em>inquired</em> as to the time when his son got better, they said, 'Yesterday at one in the afternoon.'"),
  ("Acts 10:18", "They called out, asking whether Simon who was known as Peter was staying there.")],
 [("G2065", "Erōtaō (To Ask)"), ("G154", "Aiteō (To Petition)"), ("G1934", "Epizēteō (To Seek After)")]),

# --- G4041 ---
("G4041", "περιούσιος", "perioúsios", "Adjective", "Special Possession, Treasured",
 "Perioúsios — God's special, treasured possession; the covenant people. Strong's G4041.",
 "<em>Perioúsios</em> (περιούσιος) means <strong>one's own special possession, peculiar, chosen as treasured property</strong>. In the LXX, it translates Hebrew <em>segullah</em> — a prized personal treasure.",
 "Titus 2:14: Christ 'gave himself for us to redeem us from all wickedness and to purify for himself a <em>people that are his very own</em>.' The background is Exodus 19:5: 'you will be my treasured possession out of all nations.' Through Christ, this identity extends to all believers. The church is not merely a religious organization but <strong>God's prized possession</strong> — people bought at infinite cost. This identity produces holiness: 'eager to do what is good.' We live as befits those treasured by God.",
 [("Titus 2:14", "Who gave himself to redeem us and to purify for himself a <em>people that are his very own</em>, eager to do what is good."),
  ("Exodus 19:5", "You will be my treasured possession out of all nations. The whole earth is mine."),
  ("1 Peter 2:9", "You are a chosen people, a royal priesthood, a holy nation, God's special possession.")],
 [("G1588", "Eklektos (Chosen)"), ("G2992", "Laos (People)"), ("G59", "Agorazō (To Purchase)")]),

# --- G3714 ---
("G3714", "ὀρεινός", "oreinós", "Adjective", "Mountainous, Hill Country",
 "Oreinós — the hill country; Mary's journey to Elizabeth. Strong's G3714.",
 "<em>Oreinós</em> (ὀρεινός) means <strong>mountainous, hilly, of the hill country</strong>. Related to <em>oros</em> (mountain). It appears in Luke's Gospel describing Judean geography.",
 "Luke 1:39: 'Mary got ready and hurried to a town in the <em>hill country</em> of Judea.' Newly pregnant with Jesus, Mary travels to visit Elizabeth — a journey of about 80 miles through mountainous terrain. This was not casual travel; it was <strong>urgent, faith-driven movement</strong>. Mary needed to see the sign Gabriel promised — Elizabeth's miraculous pregnancy. The meeting produces the Magnificat (Luke 1:46-55), one of Scripture's greatest songs. The hill country becomes the stage for the meeting of the old covenant (John the Baptist) and the new (Jesus) — both still in the womb.",
 [("Luke 1:39", "At that time Mary got ready and hurried to a town in the <em>hill country</em> of Judea."),
  ("Luke 1:41", "When Elizabeth heard Mary's greeting, the baby leaped in her womb, and Elizabeth was filled with the Holy Spirit."),
  ("Luke 1:46-47", "My soul glorifies the Lord and my spirit rejoices in God my Savior.")],
 [("G3735", "Oros (Mountain)"), ("G4172", "Polis (City)"), ("G4710", "Spoudē (Haste/Eagerness)")]),

# --- G3061 ---
("G3061", "λοιμός", "loimós", "Noun, masculine", "Plague, Pestilence",
 "Loimós — plague and pestilence; signs of the last days. Strong's G3061.",
 "<em>Loimós</em> (λοιμός) means <strong>plague, pestilence, deadly epidemic</strong>. Figuratively, a 'pest' — a dangerous troublemaker. Both senses appear in the NT.",
 "Jesus lists <em>loimós</em> among end-time signs in Luke 21:11: 'great earthquakes, famines and <em>pestilences</em>.' In Acts 24:5, Paul's accusers call him 'a <em>plague</em>' — using the word as insult. Revelation 6:8 includes pestilence among the four horsemen's instruments. <strong>The theological response to plague is not fatalism but trust in the sovereign God</strong> who promises in Psalm 91:3: 'Surely he will save you from the deadly pestilence,' combined with prayer for mercy as in Joel 1-2.",
 [("Luke 21:11", "There will be great earthquakes, famines and <em>pestilences</em> in various places."),
  ("Revelation 6:8", "They were given power to kill by sword, famine and <em>plague</em>."),
  ("Psalm 91:3", "Surely he will save you from the fowler's snare and from the deadly <em>pestilence</em>.")],
 [("G3042", "Limos (Famine)"), ("G4578", "Seismos (Earthquake)"), ("G2288", "Thanatos (Death)")]),

# --- G3359 ---
("G3359", "μέτωπον", "métōpon", "Noun, neuter", "Forehead",
 "Métōpon — the forehead; site of God's seal and the beast's mark. Strong's G3359.",
 "<em>Métōpon</em> (μέτωπον) means <strong>forehead</strong>. In Revelation, the forehead becomes a site of profound spiritual significance — where both the seal of God and the mark of the beast are placed, signifying allegiance.",
 "The 144,000 have the Father's name on their <em>foreheads</em> (Revelation 14:1). God's servants receive His seal there as protection (7:3). Those who worship the beast receive his mark on their foreheads (13:16). In the New Jerusalem, 'his name will be on their <em>foreheads</em>' (22:4). This draws on Exodus 28:36-38 (the high priest wore 'HOLY TO THE LORD' on his forehead) and Deuteronomy 6:8 (God's words as a sign on your forehead). <strong>The forehead represents conscious allegiance — who owns your mind and will.</strong>",
 [("Revelation 22:4", "They will see his face, and his name will be on their <em>foreheads</em>."),
  ("Revelation 13:16", "It forced all people to receive a mark on their right hands or on their <em>foreheads</em>."),
  ("Revelation 14:1", "The Lamb, and with him 144,000 who had his name and his Father's name written on their <em>foreheads</em>.")],
 [("G4973", "Sphragis (Seal)"), ("G5480", "Charagma (Mark)"), ("G3686", "Onoma (Name)")]),

# --- G4025 ---
("G4025", "περίθεσις", "períthesis", "Noun, feminine", "Wearing, Putting On",
 "Períthesis — outward adornment vs. inner beauty. Strong's G4025.",
 "<em>Períthesis</em> (περίθεσις) means <strong>the act of wearing or putting on adornment</strong>. From <em>peritithēmi</em> (to place around). Appears once in 1 Peter.",
 "First Peter 3:3-4: 'Your beauty should not come from outward adornment (<em>períthesis</em>)... but from your inner self, the unfading beauty of a gentle and quiet spirit, which is of great worth in God's sight.' Peter establishes a <strong>hierarchy of beauty</strong>: external adornment is temporary; inner character is 'of great worth' and 'unfading.' This applies beyond gender — all believers are called to prioritize character over appearance, integrity over impression management. God looks at the heart (1 Samuel 16:7).",
 [("1 Peter 3:3-4", "Your beauty should not come from outward <em>adornment</em>... but the unfading beauty of a gentle and quiet spirit."),
  ("1 Samuel 16:7", "The LORD does not look at the outward appearance, but the LORD looks at the heart."),
  ("Proverbs 31:30", "Charm is deceptive, and beauty is fleeting; but a woman who fears the LORD is to be praised.")],
 [("G2889", "Kosmos (Adornment/World)"), ("G4239", "Prays (Gentle)"), ("G1391", "Doxa (Glory)")]),

# --- G2767 ---
("G2767", "κεράννυμι", "keránnymi", "Verb", "To Mix, To Mingle Wine",
 "Keránnymi — God's cup of wrath poured full strength. Strong's G2767.",
 "<em>Keránnymi</em> (κεράννυμι) means <strong>to mix, to mingle</strong> — particularly mixing wine with water or spices. In Revelation, it describes divine judgment.",
 "Revelation 14:10: those who receive the mark 'will drink the wine of God's fury, <em>poured full strength</em> into the cup of his wrath.' The Greek is striking: wine 'mixed' yet 'unmixed' (<em>akratos</em>) — meaning undiluted, full strength. A deliberate paradox emphasizing <strong>unmitigated divine wrath</strong>. In 18:6, Babylon receives 'a double portion from her own cup.' This draws on Psalm 75:8. The cup of wrath is the counterpart to the cup of blessing (1 Corinthians 10:16) that Christ offered — He drank the cup of wrath so we might drink the cup of salvation.",
 [("Revelation 14:10", "They will drink the wine of God's fury, poured full strength into the cup of his wrath."),
  ("Revelation 18:6", "Pour her a double portion from her own cup."),
  ("Psalm 75:8", "In the LORD's hand is a cup full of foaming wine mixed with spices; he pours it out.")],
 [("G3631", "Oinos (Wine)"), ("G4221", "Potērion (Cup)"), ("G3709", "Orgē (Wrath)")]),

# --- G2709 ---
("G2709", "καταχθόνιος", "katachthónios", "Adjective", "Under the Earth",
 "Katachthónios — every knee under the earth bows to Jesus. Strong's G2709.",
 "<em>Katachthónios</em> (καταχθόνιος) means <strong>under the earth, subterranean</strong> — beings in the realm of the dead. Appears once in the NT in the great Christ-hymn.",
 "Philippians 2:10: 'at the name of Jesus every knee should bow, in heaven and on earth and <em>under the earth</em>.' The cosmic scope of Christ's lordship encompasses not just the living but even the dead — every power, principality, and being must bow. The one who descended lowest (the cross, death itself) has been exalted highest. <strong>No realm is outside Christ's sovereignty — not even death itself.</strong> Revelation 5:13 echoes: 'every creature in heaven and on earth and under the earth' praises the Lamb.",
 [("Philippians 2:10", "At the name of Jesus every knee should bow, in heaven and on earth and <em>under the earth</em>."),
  ("Revelation 5:13", "Every creature in heaven and on earth and <em>under the earth</em> and on the sea said: 'To him who sits on the throne and to the Lamb be praise.'"),
  ("Isaiah 45:23", "Before me every knee will bow; by me every tongue will swear.")],
 [("G3771", "Ouranios (Heavenly)"), ("G1919", "Epigeios (Earthly)"), ("G2962", "Kyrios (Lord)")]),

# --- G4237 ---
("G4237", "πρασιά", "prasiá", "Noun, feminine", "Garden Plot, Orderly Group",
 "Prasiá — groups seated like garden beds; the feeding of the 5,000. Strong's G4237.",
 "<em>Prasiá</em> (πρασιά) literally means a <strong>garden bed or plot</strong> — a rectangular section where plants grow in rows. In the NT, used for groups of people seated in organized rows.",
 "Mark 6:40: the crowd sat down in groups — <em>prasiái prasiái</em> ('garden-plot by garden-plot'). This eyewitness detail (likely from Peter) carries theological resonance. The orderly feeding of 5,000 echoes <strong>the Exodus feeding in the wilderness</strong> (Psalm 78:19: 'Can God spread a table in the wilderness?'). Jesus is the new Moses, the Good Shepherd of Psalm 23:2. The organized rows show God's provision is not chaotic — it is ordered, sufficient, and personal. No one in the <em>prasiá</em> was overlooked.",
 [("Mark 6:40", "So they sat down in groups of hundreds and fifties."),
  ("Mark 6:41-42", "Taking the five loaves... he gave thanks and broke the loaves. They all ate and were satisfied."),
  ("Psalm 23:2", "He makes me lie down in green pastures, he leads me beside quiet waters.")],
 [("G2828", "Klisia (Reclining Group)"), ("G740", "Artos (Bread)"), ("G5526", "Chortazō (To Satisfy)")]),

# --- G2734 ---
("G2734", "κατοπτρίζομαι", "katoptrízomai", "Verb", "To Behold as in a Mirror",
 "Katoptrízomai — beholding Christ's glory transforms us. Strong's G2734.",
 "<em>Katoptrízomai</em> (κατοπτρίζομαι) means <strong>to behold as in a mirror, to reflect like a mirror</strong>. Ancient mirrors were polished metal. Combines <em>kata</em> (fully) + <em>optron</em> (mirror). Appears once in the NT.",
 "Second Corinthians 3:18: 'we all, with unveiled faces contemplating the Lord's glory, are being <em>transformed into his image</em> with ever-increasing glory.' Moses' face radiated glory after being with God; now in Christ, the veil is removed and believers behold God's glory. As we behold, we become. <strong>This is the central mechanism of sanctification</strong>: prolonged, attentive beholding of Christ transforms us into His likeness. Bible reading, prayer, and worship are not optional — they are how God does His transformative work.",
 [("2 Corinthians 3:18", "We all, with unveiled faces contemplating the Lord's glory, are being <em>transformed into his image</em> with ever-increasing glory."),
  ("2 Corinthians 4:6", "God made his light shine in our hearts to give us the knowledge of God's glory in the face of Christ."),
  ("1 John 3:2", "When Christ appears, we shall be like him, for we shall see him as he is.")],
 [("G2072", "Esoptron (Mirror)"), ("G3339", "Metamorphoō (Transform)"), ("G1391", "Doxa (Glory)")]),

# --- G4131 ---
("G4131", "πλήκτης", "plḗktēs", "Noun, masculine", "Striker, Bully",
 "Plēktēs — a violent bully; disqualified from leadership. Strong's G4131.",
 "<em>Plḗktēs</em> (πλήκτης) means <strong>a striker, bully, pugnacious person</strong>. From <em>plēssō</em> (to strike). Appears in church leadership qualifications.",
 "First Timothy 3:3 and Titus 1:7: overseers must be 'not <em>violent</em>, but gentle.' The contrast is <em>epieikēs</em> (gracious, considerate). <strong>Christian leadership is incompatible with domination and violence.</strong> This was radical in a Greco-Roman world where authority was exercised by force. Jesus modeled the alternative: 'I am gentle and humble in heart' (Matthew 11:29). A leader who bullies or intimidates is disqualified because Christ-shaped leadership looks like a servant, not a tyrant.",
 [("1 Timothy 3:3", "Not given to drunkenness, <em>not violent</em> but gentle, not quarrelsome, not a lover of money."),
  ("Titus 1:7", "An overseer must be blameless... <em>not violent</em>, not pursuing dishonest gain."),
  ("Matthew 11:29", "I am gentle and humble in heart, and you will find rest for your souls.")],
 [("G1933", "Epieikēs (Gentle)"), ("G269", "Amachos (Peaceable)"), ("G1985", "Episkopos (Overseer)")]),

# --- G4063 ---
("G4063", "περιτρέχω", "peritréchō", "Verb", "To Run Through, To Run Around",
 "Peritréchō — people ran through villages to bring the sick to Jesus. Strong's G4063.",
 "<em>Peritréchō</em> (περιτρέχω) means <strong>to run through, to run around, to hasten about</strong> a region. Combines <em>peri</em> (around) + <em>trechō</em> (to run). Appears once in the NT.",
 "Mark 6:55: when Jesus arrived at Gennesaret, people 'ran throughout that whole region and carried the sick on mats to wherever they heard he was.' <em>Peritrechō</em> captures <strong>desperate faith</strong> — people didn't send polite invitations; they ran. They didn't wait for the sick to self-present; they carried them. The response to Jesus should be characterized by urgency, not complacency. Combined with Jesus healing all who came (v.56), it reveals infinite compassion — no case too hard, no person beyond reach.",
 [("Mark 6:55", "They <em>ran throughout that whole region</em> and carried the sick on mats to wherever they heard he was."),
  ("Mark 6:56", "Wherever he went, they placed the sick in the marketplaces. And all who touched him were healed."),
  ("Matthew 4:24", "News about him spread all over Syria, and people brought to him all who were ill.")],
 [("G5143", "Trechō (To Run)"), ("G2390", "Iaomai (To Heal)"), ("G4100", "Pisteuō (To Believe)")]),

# --- G5295 ---
("G5295", "ὑποτρέχω", "hypotréchō", "Verb", "To Run Under, To Sail Under the Lee",
 "Hypotréchō — sailing under the shelter of an island; divine protection. Strong's G5295.",
 "<em>Hypotréchō</em> (ὑποτρέχω) means <strong>to run under, to sail under the lee of</strong> — seeking shelter behind an island or landmass from wind and waves. Appears once in Acts.",
 "Acts 27:16: 'As we passed to the lee of a small island called Cauda, we were hardly able to make the lifeboat secure.' The sailors seek shelter from the northeaster by running under the island's protection. <strong>This nautical term illustrates a spiritual principle</strong>: in life's storms, we must seek shelter — not in our own skill but in God's provision. Psalm 91:1: 'Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty.' God provides Caudas — places of refuge in the storm.",
 [("Acts 27:16", "As we passed to the lee of a small island called Cauda, we were hardly able to make the lifeboat secure."),
  ("Psalm 91:1", "Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty."),
  ("Psalm 46:1", "God is our refuge and strength, an ever-present help in trouble.")],
 [("G417", "Anemos (Wind)"), ("G3491", "Naus (Ship)"), ("G4991", "Sōtēria (Salvation)")]),

# --- G3646 ---
("G3646", "ὁλοκαύτωμα", "holokautōma", "Noun, neuter", "Whole Burnt Offering",
 "Holokautōma — the whole burnt offering fulfilled in Christ. Strong's G3646.",
 "<em>Holokautōma</em> (ὁλοκαύτωμα) means <strong>whole burnt offering</strong> — a sacrifice entirely consumed by fire, nothing reserved. From <em>holos</em> (whole) + <em>kautos</em> (burned). The most complete OT sacrifice, representing total consecration.",
 "Hebrews 10:6,8 quotes Psalm 40: God 'did not desire' mere ritual sacrifices but a body prepared for Christ. Mark 12:33: loving God and neighbor 'is more important than all <em>burnt offerings</em>.' The OT sacrificial system always pointed beyond itself. <strong>Jesus is the ultimate whole burnt offering</strong>: completely given, nothing held back, totally consumed by divine judgment on our behalf. Romans 12:1 calls us to respond: 'offer your bodies as a living sacrifice.'",
 [("Hebrews 10:6", "With <em>burnt offerings</em> and sin offerings you were not pleased."),
  ("Mark 12:33", "To love him with all your heart is more important than all <em>burnt offerings</em> and sacrifices."),
  ("Romans 12:1", "Offer your bodies as a living sacrifice, holy and pleasing to God.")],
 [("G2378", "Thysia (Sacrifice)"), ("G749", "Archiereus (High Priest)"), ("G2434", "Hilasmos (Propitiation)")]),

# --- G2407 ---
("G2407", "ἱερατεύω", "hierateúō", "Verb", "To Serve as Priest",
 "Hierateúō — priestly service; all believers are now priests. Strong's G2407.",
 "<em>Hierateúō</em> (ἱερατεύω) means <strong>to serve as a priest, to perform priestly duties</strong>. Related to <em>hiereus</em> (priest) and <em>hieron</em> (temple). Appears in Luke's Gospel.",
 "Luke 1:8: Zechariah was '<em>serving as priest</em> before God' when Gabriel announced John the Baptist's birth. The priestly ministry was the highest religious duty in Israel. The NT then makes a stunning application: through Christ, <strong>all believers are priests</strong> (1 Peter 2:5,9; Revelation 1:6). The veil is torn; every believer has direct access to God. Our 'priestly service' is the sacrifice of praise (Hebrews 13:15) and holy living. Every Christian daily exercises a priestly calling.",
 [("Luke 1:8", "Once when Zechariah's division was on duty and he was <em>serving as priest</em> before God..."),
  ("1 Peter 2:9", "You are a chosen people, a royal <em>priesthood</em>, a holy nation."),
  ("Revelation 1:6", "He has made us to be a kingdom and <em>priests</em> to serve his God and Father.")],
 [("G2409", "Hiereus (Priest)"), ("G2405", "Hierateia (Priesthood)"), ("G2413", "Hieros (Sacred)")]),

# --- G4609 ---
("G4609", "Σίλας", "Sílas", "Proper Noun", "Silas",
 "SKIP", "", "", [], []),  # PROPER NAME — SKIP

# --- G4971 ---
("G4971", "σφόδρα", "sphódra", "Adverb", "Exceedingly, Very Much, Greatly",
 "Sphódra — exceedingly great emotion, sorrow, and joy. Strong's G4971.",
 "<em>Sphódra</em> (σφόδρα) means <strong>exceedingly, very much, greatly</strong>. It intensifies emotions, reactions, and states — both positive and negative throughout the NT.",
 "The word captures extreme human responses to divine encounters. Matthew 2:10: the Magi '<em>exceedingly</em> rejoiced' at the star. Matthew 17:6: at the Transfiguration, disciples were '<em>exceedingly</em> afraid.' Matthew 26:22: at the Last Supper, they were '<em>exceedingly</em> sorrowful.' Mark 16:4: the stone was '<em>exceedingly</em> great.' <strong>Encounters with God produce extreme reactions</strong> — not mild, measured religious feeling but overwhelming joy, trembling fear, and deep sorrow. Authentic faith is not lukewarm (Revelation 3:16).",
 [("Matthew 2:10", "When they saw the star, they rejoiced <em>exceedingly</em> with great joy."),
  ("Matthew 17:6", "The disciples fell on their faces and were <em>exceedingly</em> afraid."),
  ("Matthew 26:22", "They were <em>exceedingly</em> sorrowful, and each began to say, 'Surely not I, Lord?'")],
 [("G3029", "Lian (Very/Greatly)"), ("G4057", "Perissōs (Abundantly)"), ("G5479", "Chara (Joy)")]),

# --- G2893 ---
("G2893", "κουφίζω", "kouphízō", "Verb", "To Lighten, To Ease a Load",
 "Kouphízō — lightening the ship; God lifts our burdens. Strong's G2893.",
 "<em>Kouphízō</em> (κουφίζω) means <strong>to lighten, to make light, to ease a burden</strong>. From <em>kouphos</em> (light). Appears once in Acts.",
 "Acts 27:38: 'they <em>lightened</em> the ship by throwing the grain into the sea.' Survival required jettisoning valuable cargo. <strong>God specializes in lightening loads.</strong> Jesus invites, 'Come to me, all you who are weary and burdened, and I will give you rest' (Matthew 11:28). The Christian life involves both holding on (faith) and letting go (casting burdens on God). Sometimes survival requires throwing overboard what was once valuable — career, reputation, comfort — for the sake of what matters eternally.",
 [("Acts 27:38", "They <em>lightened</em> the ship by throwing the grain into the sea."),
  ("Matthew 11:28-30", "Come to me, all you who are weary and burdened, and I will give you rest."),
  ("1 Peter 5:7", "Cast all your anxiety on him because he cares for you.")],
 [("G5413", "Phortion (Burden)"), ("G922", "Baros (Weight)"), ("G373", "Anapauō (To Rest)")]),

# --- G4229 ---
("G4229", "πρᾶγμα", "prâgma", "Noun, neuter", "Thing, Matter, Deed",
 "Prâgma — a matter or deed; faith as evidence of unseen realities. Strong's G4229.",
 "<em>Prâgma</em> (πρᾶγμα) means <strong>a thing done, a matter, an affair</strong>. Related to <em>prassō</em> (to do). Broadly covers any matter of concern — legal, moral, or practical.",
 "The word appears in one of Scripture's greatest definitions. Hebrews 11:1: 'faith is the substance of things hoped for, the evidence of <em>things</em> (<em>pragmatōn</em>) not seen.' <strong>Faith is conviction about unseen realities</strong> — the greatest <em>pragmata</em> are invisible. In 1 Corinthians 6:1, Paul rebukes taking disputes (<em>pragmata</em>) before secular courts. In Hebrews 6:18, two unchangeable <em>pragmata</em> — God's promise and oath — anchor our hope.",
 [("Hebrews 11:1", "Faith is confidence in what we hope for and assurance about what we do not see."),
  ("1 Corinthians 6:1", "If any of you has a dispute, do you dare to take it before the ungodly for judgment?"),
  ("Hebrews 6:18", "By two unchangeable <em>things</em> in which it is impossible for God to lie, we may be greatly encouraged.")],
 [("G2041", "Ergon (Work/Deed)"), ("G4238", "Prassō (To Do)"), ("G4102", "Pistis (Faith)")]),

# ═══════════════════════════════════════════════════════════
# HEBREW ENTRIES (50)
# ═══════════════════════════════════════════════════════════

# --- H1991 ---
("H1991", "הֵם", "hēm", "Pronoun", "They, These",
 "SKIP", "", "", [], []),  # Basic pronoun — skip

# --- H7145 ---
("H7145", "קָרְחִי", "Qorchîy", "Adjective/Gentilic", "Korahite — of Korah",
 "SKIP", "", "", [], []),  # Proper name derivative — skip

# --- H4429 ---
("H4429", "מֶלֶךְ", "Melek", "Proper Noun", "King (as name)",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H7915 ---
("H7915", "שַׂכִּין", "sakkîyn", "Noun, masculine", "Knife",
 "Sakkîyn — the knife at the throat; radical self-control. Strong's H7915.",
 "<em>Sakkîyn</em> (שַׂכִּין) means <strong>knife, blade</strong> — a cutting instrument. A <em>hapax legomenon</em> (appearing once in the Hebrew Bible), possibly related to Aramaic cognates.",
 "Proverbs 23:2: 'Put a <em>knife</em> to your throat if you are given to gluttony.' The image is vivid — self-mastery so radical it is like restraining yourself at knifepoint. The broader context warns against being deceived by a ruler's delicacies. <strong>Self-control is a core spiritual discipline</strong>, especially regarding appetite. This connects to Galatians 5:24: 'those who belong to Christ have crucified the flesh with its passions and desires.' The knife symbolizes intentional, even violent resistance to ungodly impulses.",
 [("Proverbs 23:2", "Put a <em>knife</em> to your throat if you are given to gluttony."),
  ("Proverbs 23:1", "When you sit to dine with a ruler, note well what is before you."),
  ("Galatians 5:23-24", "...self-control. Those who belong to Christ have crucified the flesh with its passions and desires.")],
 [("H2719", "Chereb (Sword)"), ("H3979", "Ma'akelet (Knife)"), ("H4623", "Ma'tsar (Self-Restraint)")]),

# --- H7811 ---
("H7811", "שָׂחָה", "sāchāh", "Verb", "To Swim",
 "Sāchāh — to swim; flailing pride brought low by God. Strong's H7811.",
 "<em>Sāchāh</em> (שָׂחָה) means <strong>to swim</strong> — to move through water. Rare in the Hebrew Bible, used in a striking metaphor of helplessness.",
 "Isaiah 25:11: 'They will spread out their hands as a <em>swimmer</em> spreads hands to swim. God will bring down their pride.' The context is judgment on Moab — the proud nation flailing helplessly. <strong>Pride makes us think we can swim any depth; God reminds us He controls the waters.</strong> Ezekiel 47:5 uses a related image: the river from the temple deepens until it becomes 'deep enough to swim in' — representing the ever-increasing flow of God's life-giving grace.",
 [("Isaiah 25:11", "They will spread out their hands as a <em>swimmer</em> spreads hands to swim. God will bring down their pride."),
  ("Ezekiel 47:5", "The water had risen and was deep enough to <em>swim</em> in — a river no one could cross."),
  ("Psalm 69:1-2", "Save me, O God, for the waters have come up to my neck. I sink in the miry depths.")],
 [("H4325", "Mayim (Water)"), ("H7857", "Shataph (To Overflow)"), ("H1346", "Ga'avah (Pride)")]),

# --- H5138 ---
("H5138", "נָזִיד", "nāzîyd", "Noun, masculine", "Stew, Pottage",
 "Nāzîyd — the pottage Esau traded for his birthright. Strong's H5138.",
 "<em>Nāzîyd</em> (נָזִיד) means <strong>boiled pottage, stew</strong> — a thick dish of lentils or legumes. From <em>zîyd</em> (to boil). Appears in Genesis and 2 Kings.",
 "Genesis 25:29-34: Esau sells his birthright for red lentil <em>stew</em>. Hebrews 12:16-17 cites this as warning: 'godless like Esau, who for a single meal sold his inheritance rights.' <strong>The pottage represents immediate gratification traded for eternal inheritance.</strong> Esau's 'I am about to die' was hyperbole — he was hungry, not dying. Yet he treated eternal blessing as worthless. The warning is perpetually relevant: don't trade heavenly inheritance for earthly satisfaction. In 2 Kings 4:38-41, Elisha miraculously heals poisoned stew — death-dealing <em>nāzîyd</em> becomes nourishing.",
 [("Genesis 25:34", "Jacob gave Esau bread and lentil <em>stew</em>. He ate and drank and left. So Esau despised his birthright."),
  ("Hebrews 12:16", "See that no one is godless like Esau, who for a single meal sold his inheritance rights."),
  ("2 Kings 4:40", "'There is death in the pot!' But Elisha put flour in and said, 'Serve it.' And there was nothing harmful.")],
 [("H1310", "Bashal (To Boil/Cook)"), ("H1062", "Bekorah (Birthright)"), ("H5727", "Adan (Delight)")]),

# --- H7397 ---
("H7397", "רֶכֶב", "rekeb", "Noun, masculine", "Chariot, Riding",
 "SKIP", "", "", [], []),  # Variant form — skip

# --- H3365 ---
("H3365", "יָקַר", "yāqar", "Verb", "To Be Precious, To Be Prized",
 "Yāqar — precious in God's sight; the infinite value of faithful lives. Strong's H3365.",
 "<em>Yāqar</em> (יָקַר) means <strong>to be precious, to be prized, to be of great value, to be rare</strong>. Also means to be honored or esteemed. Related noun <em>yaqar</em> = preciousness.",
 "Psalm 116:15: '<em>Precious</em> in the sight of the LORD is the death of his faithful servants.' God places infinite value on His people's lives — every death of a saint matters to Him. Psalm 139:17: 'How <em>precious</em> to me are your thoughts, O God!' 1 Samuel 3:1: 'the word of the LORD was <em>rare</em> (<em>yaqar</em>) in those days' — God's Word was precious because it was scarce. <strong>What is precious to God should be precious to us</strong>: His Word, His people, His purposes. And we are precious to Him.",
 [("Psalm 116:15", "<em>Precious</em> in the sight of the LORD is the death of his faithful servants."),
  ("Psalm 139:17", "How <em>precious</em> to me are your thoughts, O God! How vast is the sum of them!"),
  ("1 Samuel 3:1", "The boy Samuel ministered before the LORD. The word of the LORD was <em>rare</em> in those days.")],
 [("H3366", "Yeqar (Honor/Preciousness)"), ("H2530", "Chamad (To Desire/Delight)"), ("H5689", "Agab (To Love)")]),

# --- H8668 ---
("H8668", "תְּשׁוּעָה", "teshû'āh", "Noun, feminine", "Salvation, Deliverance, Victory",
 "Teshû'āh — salvation and victory belong to the LORD. Strong's H8668.",
 "<em>Teshû'āh</em> (תְּשׁוּעָה) means <strong>salvation, deliverance, victory</strong>. Related to <em>yāsha'</em> (to save) and <em>Yeshûa</em> (Jesus). A comprehensive term for God's saving acts.",
 "Proverbs 21:31: 'The horse is made ready for the day of battle, but <em>victory</em> belongs to the LORD.' This is the tension of faith: prepare diligently, but know that <strong>ultimate victory is God's alone</strong>. Proverbs 11:14: 'For lack of guidance a nation falls, but <em>victory</em> is won through many advisers' — wisdom and counsel are the means God uses. Psalm 144:10: 'He gives <em>victory</em> to kings; he delivers his servant David from the deadly sword.'",
 [("Proverbs 21:31", "The horse is made ready for the day of battle, but <em>victory</em> belongs to the LORD."),
  ("Proverbs 11:14", "For lack of guidance a nation falls, but <em>victory</em> is won through many advisers."),
  ("Psalm 144:10", "He gives <em>victory</em> to kings; he delivers his servant David from the deadly sword.")],
 [("H3444", "Yeshû'āh (Salvation)"), ("H3467", "Yāsha' (To Save)"), ("H5337", "Natsal (To Deliver)")]),

# --- H1898 ---
("H1898", "הָגָה", "hāgāh", "Verb", "To Remove, To Take Away",
 "SKIP", "", "", [], []),  # Variant of H1897 — skip

# --- H1642 ---
("H1642", "גְּרָר", "Gerar", "Proper Noun", "Gerar",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H8234 ---
("H8234", "שֶׁפֶר", "Shepher", "Proper Noun", "Mount Shepher",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H3748 ---
("H3748", "כְּרִיתוּת", "kerîythûth", "Noun, feminine", "Divorce, Cutting Off",
 "Kerîythûth — the certificate of divorce; covenant-breaking and God's faithfulness. Strong's H3748.",
 "<em>Kerîythûth</em> (כְּרִיתוּת) means <strong>divorce, cutting off, severance</strong>. From <em>kārath</em> (to cut). It refers specifically to the certificate of divorce mentioned in Mosaic law.",
 "Deuteronomy 24:1,3: if a man finds 'something indecent' in his wife, he writes her a certificate of <em>divorce</em>. Isaiah 50:1 uses it theologically: 'Where is your mother's certificate of <em>divorce</em> with which I sent her away?' — God challenges Israel, declaring He never truly divorced His people. Jeremiah 3:8 says He gave faithless Israel a certificate of divorce, yet still calls her back. <strong>God's covenant faithfulness exceeds even the legal provisions for divorce.</strong> Jesus in Matthew 19:8 says Moses permitted divorce 'because your hearts were hard, but from the beginning it was not so.'",
 [("Deuteronomy 24:1", "If a man marries a woman and she becomes displeasing to him, he writes her a certificate of <em>divorce</em>."),
  ("Isaiah 50:1", "Where is your mother's certificate of <em>divorce</em> with which I sent her away?"),
  ("Jeremiah 3:8", "I gave faithless Israel her certificate of <em>divorce</em> and sent her away because of all her adulteries.")],
 [("H3772", "Karath (To Cut/Covenant)"), ("H7971", "Shalach (To Send Away)"), ("H1285", "Berîyth (Covenant)")]),

# --- H4388 ---
("H4388", "מַכְתֵּשׁ", "maktēsh", "Noun, masculine", "Mortar, Hollow Place",
 "Maktēsh — the mortar; grinding judgment and refining. Strong's H4388.",
 "<em>Maktēsh</em> (מַכְתֵּשׁ) means <strong>mortar, bowl, hollow place</strong> — a concave vessel in which grain or spices are ground with a pestle. Also refers to a geographical hollow or basin.",
 "Proverbs 27:22: 'Though you grind a fool in a <em>mortar</em>, grinding them like grain with a pestle, you will not remove their folly from them.' This is one of Proverbs' starkest assessments of deep-seated foolishness: <strong>some folly is so entrenched that even the most severe discipline cannot remove it</strong>. Only God's transformative grace can change a heart of stone to flesh (Ezekiel 36:26). In Judges 15:19, God splits open a <em>maktēsh</em> (hollow) and water flows for Samson — provision from an unexpected source.",
 [("Proverbs 27:22", "Though you grind a fool in a <em>mortar</em> with a pestle, you will not remove their folly."),
  ("Judges 15:19", "God opened up the hollow place (<em>maktēsh</em>) and water came out."),
  ("Ezekiel 36:26", "I will give you a new heart and put a new spirit in you; I will remove from you your heart of stone.")],
 [("H5940", "Eliy (Pestle)"), ("H191", "Eviyl (Fool)"), ("H3820", "Lēb (Heart)")]),

# --- H2024 ---
("H2024", "הָרָא", "Hārā'", "Proper Noun", "Hara",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H3796 ---
("H3796", "כֹּתֶל", "kōthel", "Noun, masculine", "Wall",
 "Kōthel — the wall; the beloved peering through the lattice. Strong's H3796.",
 "<em>Kōthel</em> (כֹּתֶל) means <strong>wall</strong> — specifically a house wall or partition. It appears in the Song of Solomon, where it is cherished in Jewish tradition as the word behind 'Western Wall' (<em>Kotel</em>).",
 "Song of Solomon 2:9: 'My beloved is like a gazelle... Look! There he stands behind our <em>wall</em>, gazing through the windows, peering through the lattice.' The beloved is near — separated only by a wall — looking through every opening to see the one he loves. <strong>This is a picture of God's nearness even when we feel a barrier.</strong> He is not distant; He is right behind the wall, seeking us. The Hebrew word <em>kōthel</em> lives on today in the Western Wall (Ha-Kotel) in Jerusalem — the closest point to where God's presence dwelt.",
 [("Song of Solomon 2:9", "My beloved stands behind our <em>wall</em>, gazing through the windows, peering through the lattice."),
  ("Song of Solomon 2:10", "My beloved spoke and said to me, 'Arise, my darling, my beautiful one, come with me.'"),
  ("Revelation 3:20", "Here I am! I stand at the door and knock. If anyone hears my voice and opens the door, I will come in.")],
 [("H2346", "Chōmāh (City Wall)"), ("H7023", "Qîyr (Wall)"), ("H2474", "Challôn (Window)")]),

# --- H2295 ---
("H2295", "חָגְלָה", "Choglāh", "Proper Noun", "Hoglah",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H5345 ---
("H5345", "נֶקֶב", "neqeb", "Noun, masculine", "Socket, Setting (for gemstones)",
 "Neqeb — the gem setting; each stone in its appointed place. Strong's H5345.",
 "<em>Neqeb</em> (נֶקֶב) means <strong>socket, setting, or bezel</strong> — the mounting or groove in which a gemstone is placed. From <em>nāqab</em> (to pierce, bore through).",
 "Ezekiel 28:13 describes the king of Tyre (echoing the covering cherub): 'every precious stone adorned you... The workmanship of your <em>settings</em> and mountings was prepared for you on the day you were created.' Each gemstone had its specific <em>neqeb</em> — its appointed place. <strong>God designs each person for a specific setting</strong>, a particular place in His purposes. When we try to occupy someone else's setting or refuse our own, the beauty God intended is marred. Ephesians 2:10: 'We are God's workmanship, created in Christ Jesus to do good works, which God prepared in advance for us to do.'",
 [("Ezekiel 28:13", "Every precious stone adorned you. The workmanship of your <em>settings</em> was prepared on the day you were created."),
  ("Exodus 28:17", "Mount four rows of precious stones on the breastpiece."),
  ("Ephesians 2:10", "We are God's handiwork, created in Christ Jesus to do good works, which God prepared in advance.")],
 [("H68", "'Eben (Stone)"), ("H2091", "Zāhāb (Gold)"), ("H4399", "Melā'kāh (Workmanship)")]),

# --- H4280 ---
("H4280", "מַחֲרָאָה", "machărā'āh", "Noun, feminine", "Latrine, Privy",
 "Machărā'āh — the latrine; the temple of Baal made a toilet. Strong's H4280.",
 "<em>Machărā'āh</em> (מַחֲרָאָה) means <strong>latrine, privy, toilet</strong>. From a root meaning to dig or hollow out. Appears once in the Hebrew Bible in a vivid act of theological desecration.",
 "Second Kings 10:27: 'They demolished the sacred stone of Baal and tore down the temple of Baal, and people have used it as a <em>latrine</em> to this day.' Jehu's destruction of Baal worship reached its climax by converting the pagan temple into a public toilet — the ultimate expression of contempt. <strong>False worship deserves not just rejection but utter desecration.</strong> What the culture honored, God's people made common. This radical iconoclasm reminds us that idols — ancient or modern — deserve no reverence. When we identify the Baals of our age, the response should be thorough destruction, not respectful coexistence.",
 [("2 Kings 10:27", "They demolished the temple of Baal, and people have used it as a <em>latrine</em> to this day."),
  ("2 Kings 10:28", "So Jehu destroyed Baal worship in Israel."),
  ("Deuteronomy 12:3", "Break down their altars, smash their sacred stones and burn their Asherah poles.")],
 [("H1168", "Ba'al (Baal)"), ("H4676", "Matstsēbāh (Sacred Stone)"), ("H8441", "Tô'ēbāh (Abomination)")]),

# --- H6138 ---
("H6138", "עֶקְרוֹן", "Eqrôn", "Proper Noun", "Ekron",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H7982 ---
("H7982", "שֶׁלֶט", "sheleṭ", "Noun, masculine", "Shield",
 "Sheleṭ — the shield; God's protection and the warrior's trust. Strong's H7982.",
 "<em>Sheleṭ</em> (שֶׁלֶט) means <strong>shield</strong> — a defensive weapon, often a small round shield or buckler. Related to <em>shālaṭ</em> (to have power, to dominate).",
 "Second Samuel 8:7: 'David took the gold <em>shields</em> that belonged to the officers of Hadadezer.' David's capture of enemy shields symbolized complete military dominance — the enemy's defense was now Israel's trophy. Song of Solomon 4:4 uses shields beautifully: 'Your neck is like the tower of David, built with courses of stone; on it hang a thousand <em>shields</em>, all of them shields of warriors.' <strong>The shields represent both beauty and defense</strong> — strength adorning the beloved. For the believer, Ephesians 6:16 commands us to take up 'the shield of faith, with which you can extinguish all the flaming arrows of the evil one.'",
 [("2 Samuel 8:7", "David took the gold <em>shields</em> that belonged to the officers of Hadadezer."),
  ("Song of Solomon 4:4", "On it hang a thousand <em>shields</em>, all of them shields of warriors."),
  ("Ephesians 6:16", "Take up the shield of faith, with which you can extinguish all the flaming arrows of the evil one.")],
 [("H4043", "Māgēn (Shield)"), ("H6793", "Tsinnāh (Large Shield)"), ("H3627", "Kelîy (Weapon)")]),

# --- H5176 ---
("H5176", "נָחָשׁ", "Nāchāsh", "Proper Noun", "Nahash",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H3060 ---
("H3060", "יְהוֹאָשׁ", "Yehô'āsh", "Proper Noun", "Jehoash",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H5233 ---
("H5233", "נֶכֶס", "nekes", "Noun, masculine", "Riches, Wealth, Treasure",
 "Nekes — riches and wealth; the stewardship of material possessions. Strong's H5233.",
 "<em>Nekes</em> (נֶכֶס) means <strong>riches, wealth, treasure, possessions</strong>. It appears in later OT books and is related to Aramaic usage for property and goods.",
 "Joshua 22:8: 'Return to your homes with your great <em>wealth</em> — with large herds of livestock, with silver, gold, bronze and iron, and a great quantity of clothing. Divide the plunder with your fellow Israelites.' After conquering the land, the eastern tribes are sent home with spoils. <strong>Wealth is presented as God's blessing to be shared</strong>, not hoarded. Ecclesiastes 5:19: 'when God gives someone wealth and possessions and enables them to enjoy them... this is a gift of God.' The Bible neither idolizes nor demonizes wealth — it demands faithful stewardship.",
 [("Joshua 22:8", "Return to your homes with your great <em>wealth</em> — with large herds, silver, gold, bronze, iron, and clothing."),
  ("Ecclesiastes 5:19", "When God gives someone <em>wealth</em> and possessions and enables them to enjoy them, this is a gift of God."),
  ("1 Timothy 6:17", "Command those who are rich not to be arrogant nor to put their hope in wealth, but to put their hope in God.")],
 [("H6239", "'Osher (Wealth)"), ("H2428", "Chayil (Wealth/Valor)"), ("H4301", "Matmôn (Treasure)")]),

# --- H5061 ---
("H5061", "נֶגַע", "nega'", "Noun, masculine", "Plague, Affliction, Stroke",
 "Nega' — the plague-mark; affliction as divine discipline and testing. Strong's H5061.",
 "<em>Nega'</em> (נֶגַע) means <strong>plague, affliction, blow, mark, wound</strong>. From <em>nāga'</em> (to touch, to strike). Used for skin diseases (Leviticus 13-14), divine judgments, and personal afflictions.",
 "Leviticus 13:3: 'The priest shall examine the <em>sore</em> on the skin.' The <em>nega'</em> required priestly examination — a reminder that <strong>spiritual leaders bear responsibility for diagnosing spiritual condition</strong>. In 1 Kings 8:37-38, Solomon prays at the temple dedication about 'whatever disaster or disease (<em>nega'</em>) may come' — asking God to hear from heaven. Psalm 91:10 promises: 'no <em>plague</em> will come near your tent.' The <em>nega'</em> system taught Israel that sin manifests in visible ways and requires examination, cleansing, and ultimately, atonement.",
 [("Leviticus 13:3", "The priest shall examine the <em>sore</em> on the skin of the body."),
  ("1 Kings 8:37-38", "Whatever disaster or disease may come... when a prayer is made, each knowing the <em>afflictions</em> of their own hearts."),
  ("Psalm 91:10", "No harm will overtake you, no <em>plague</em> will come near your tent.")],
 [("H5060", "Nāga' (To Touch/Strike)"), ("H4347", "Makkāh (Wound/Blow)"), ("H7495", "Rāphā' (To Heal)")]),

# --- H3551 ---
("H3551", "כַּו", "kav", "Noun, masculine", "Window, Opening (Aramaic)",
 "SKIP", "", "", [], []),  # Aramaic variant — skip

# --- H8320 ---
("H8320", "שָׂרֻק", "sāruq", "Adjective", "Red, Sorrel (of horses)",
 "Sāruq — the sorrel horses of Zechariah's vision; heaven's patrols. Strong's H8320.",
 "<em>Sāruq</em> (שָׂרֻק) means <strong>red, sorrel, reddish-brown</strong> — used to describe the color of horses. From <em>sāraq</em> (to be red). Appears in Zechariah's visions.",
 "Zechariah 1:8: 'I saw a man mounted on a red horse, standing among the myrtle trees... Behind him were red, brown and white horses.' These are the horses God sends to patrol the earth. Zechariah 6:2,6 also features colored horses pulling chariots — agents of God's sovereignty over the nations. <strong>The colored horses represent God's comprehensive surveillance and control over world affairs.</strong> Nothing escapes His notice; no nation acts beyond His reach. Revelation 6 echoes this with the four horsemen. The colors are not decorative — they signal different divine missions.",
 [("Zechariah 1:8", "I saw a man mounted on a red horse. Behind him were red, brown (<em>sāruq</em>) and white horses."),
  ("Zechariah 6:2-3", "The first chariot had red horses, the second black, the third white, and the fourth dappled."),
  ("Revelation 6:4", "Then another horse came out, a fiery red one. Its rider was given power to take peace from the earth.")],
 [("H122", "'Ādom (Red)"), ("H5483", "Sûs (Horse)"), ("H4818", "Merkābāh (Chariot)")]),

# --- H4162 ---
("H4162", "מוֹצָא", "môtsā'", "Noun, masculine", "Going Forth, Source, Spring",
 "Môtsā' — the going forth; from the sunrise to the source of living water. Strong's H4162.",
 "<em>Môtsā'</em> (מוֹצָא) means <strong>going forth, source, spring, exit, utterance</strong>. From <em>yātsā'</em> (to go out). A versatile word covering physical sources, geographical features, and divine origins.",
 "Micah 5:2: 'But you, Bethlehem Ephrathah... out of you will come for me one who will be ruler over Israel, whose origins (<em>môtsā'ōth</em>) are from of old, from ancient times.' This is one of the great Messianic prophecies — <strong>Christ's 'goings forth' are from eternity</strong>, predating His Bethlehem birth. Psalm 65:8: 'where morning dawns, where evening fades, you call forth songs of joy' — the <em>môtsā'</em> of morning. Proverbs 4:23: 'Guard your heart, for everything you do flows (<em>môtsā'</em>) from it.'",
 [("Micah 5:2", "Out of you will come one whose <em>origins</em> are from of old, from ancient times."),
  ("Psalm 65:8", "The whole earth is filled with awe at your wonders; where morning dawns, where evening fades."),
  ("Proverbs 4:23", "Guard your heart, for everything you do <em>flows</em> from it.")],
 [("H3318", "Yātsā' (To Go Out)"), ("H4161", "Môtsā' (Utterance)"), ("H4599", "Ma'yān (Spring)")]),

# --- H8642 ---
("H8642", "תְּרוּמִיָּה", "terûmiyyāh", "Noun, feminine", "Offering, Contribution",
 "Terûmiyyāh — the voluntary offering; generosity as worship. Strong's H8642.",
 "<em>Terûmiyyāh</em> (תְּרוּמִיָּה) means <strong>offering, contribution, gift</strong>. Related to <em>terûmāh</em> (heave offering). Appears in the context of temple offerings.",
 "Ezekiel 48:12: the consecrated portion will be 'a special gift (<em>terûmiyyāh</em>) to them out of the sacred portion of the land.' In Ezekiel's temple vision, this word describes land set apart for priestly service — a <strong>voluntary consecration of the best to God</strong>. The principle runs through Scripture: the firstfruits, the tithe, the freewill offering — all express the truth that everything belongs to God and we return a portion in grateful worship. 2 Corinthians 9:7: 'God loves a cheerful giver.'",
 [("Ezekiel 48:12", "It will be a special <em>gift</em> to them out of the sacred portion of the land."),
  ("Exodus 25:2", "Tell the Israelites to bring me an <em>offering</em>. You are to receive the offering from everyone whose heart prompts them."),
  ("2 Corinthians 9:7", "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver.")],
 [("H8641", "Terûmāh (Heave Offering)"), ("H5071", "Nedābāh (Freewill Offering)"), ("H7133", "Qorbān (Offering)")]),

# --- H8465 ---
("H8465", "תַּחַן", "Tachan", "Proper Noun", "Tahan",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H8110 ---
("H8110", "שִׁמְרוֹן", "Shimrôn", "Proper Noun", "Shimron",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H1914 ---
("H1914", "הִדַּי", "Hiddai", "Proper Noun", "Hiddai",
 "SKIP", "", "", [], []),  # Proper name — skip

# --- H7720 ---
("H7720", "שַׂהֲרֹן", "saharōn", "Noun, masculine", "Crescent Ornament",
 "Saharōn — crescent ornaments; pagan symbols stripped as war spoil. Strong's H7720.",
 "<em>Saharōn</em> (שַׂהֲרֹן) means <strong>crescent, moon-shaped ornament</strong>. From <em>sāhar</em> (moon). Small crescent pendants worn as jewelry or placed on camels as decorative amulets.",
 "Judges 8:21,26: Gideon took the <em>crescent ornaments</em> from the Midianite kings' camels. Isaiah 3:18: God will strip away the finery of the daughters of Zion, including their '<em>crescents</em>.' These ornaments were connected to moon worship — wearing them was a subtle form of pagan identification. <strong>God calls His people to separate from the symbols of false worship</strong>, even when they seem merely decorative. What we wear and display can signal spiritual allegiance.",
 [("Judges 8:21", "Gideon took the <em>crescent ornaments</em> that were on the camels' necks."),
  ("Judges 8:26", "The weight of the gold rings he asked for was 1,700 shekels, not counting the <em>crescents</em>, pendants and purple garments."),
  ("Isaiah 3:18", "In that day the Lord will snatch away their finery: bangles, headbands and <em>crescent</em> necklaces.")],
 [("H3394", "Yārēach (Moon)"), ("H5141", "Nezem (Ring/Earring)"), ("H6287", "Pe'ēr (Headdress)")]),

# --- H7975 ---
("H7975", "שִׁלֹחַ", "Shilōach", "Noun, masculine", "Shiloah, Siloam",
 "Shilōach — the waters of Shiloah that flow gently; trusting God's quiet provision. Strong's H7975.",
 "<em>Shilōach</em> (שִׁלֹחַ) means <strong>a sending forth (of water)</strong> — the name of the gentle aqueduct and pool in Jerusalem. From <em>shālach</em> (to send). Same as NT Siloam (John 9:7).",
 "Isaiah 8:6: 'Because this people has rejected the gently flowing waters of <em>Shiloah</em> and rejoices over Rezin and the son of Remaliah...' Judah preferred military alliances over God's quiet provision. The waters of Shiloah — gentle, modest, life-sustaining — represent <strong>God's unspectacular but faithful care</strong>. In contrast, God would bring the mighty Euphrates (Assyria) flooding over them. John 9:7: Jesus sends the blind man to wash in the Pool of <em>Siloam</em> ('Sent'), connecting healing to this ancient symbol of God's sending.",
 [("Isaiah 8:6", "Because this people has rejected the gently flowing waters of <em>Shiloah</em>..."),
  ("John 9:7", "Go, wash in the Pool of <em>Siloam</em> (this word means 'Sent'). So he went and washed, and came home seeing."),
  ("Isaiah 8:7", "The Lord is about to bring against them the mighty floodwaters of the Euphrates.")],
 [("H4325", "Mayim (Water)"), ("H7971", "Shālach (To Send)"), ("H1295", "Berēkāh (Pool)")]),

# --- H3148 ---
("H3148", "יוֹתֵר", "yôthēr", "Adverb/Adjective", "More, Excess, Advantage",
 "Yôthēr — the advantage of wisdom; what remains and what matters. Strong's H3148.",
 "<em>Yôthēr</em> (יוֹתֵר) means <strong>more, advantage, excess, remainder</strong>. From <em>yāthar</em> (to remain, to be left over). It appears in Ecclesiastes as a key philosophical term.",
 "Ecclesiastes 6:8: 'What <em>advantage</em> does a wise person have over a fool?' Ecclesiastes 6:11: 'The <em>more</em> the words, the less the meaning.' Ecclesiastes 7:11: 'Wisdom, like an inheritance, is a good thing and benefits those who see the sun; for wisdom is a shelter... the <em>advantage</em> of knowledge is this: wisdom preserves those who have it.' <strong>The Preacher wrestles with ultimate value</strong> — what truly matters 'under the sun.' His conclusion: fear God and keep His commandments (12:13). All other advantages are vapor (<em>hevel</em>) without this foundation.",
 [("Ecclesiastes 7:11-12", "Wisdom, like an inheritance, is a good thing. The <em>advantage</em> of knowledge is that wisdom preserves those who have it."),
  ("Ecclesiastes 6:8", "What <em>advantage</em> does a wise person have over a fool?"),
  ("Ecclesiastes 12:13", "Fear God and keep his commandments, for this is the duty of all mankind.")],
 [("H2451", "Chokmāh (Wisdom)"), ("H1892", "Hevel (Vanity/Vapor)"), ("H3504", "Yithrôn (Profit/Advantage)")]),

# --- H6947 ---
("H6947", "קָדֵשׁ בַּרְנֵעַ", "Qādēsh Barnēa'", "Proper Noun", "Kadesh Barnea",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H3917 ---
("H3917", "לִילִית", "lîylîyth", "Noun, feminine", "Night Creature, Screech Owl",
 "Lîylîyth — the night creature; desolation and the absence of God's blessing. Strong's H3917.",
 "<em>Lîylîyth</em> (לִילִית) means <strong>night creature, screech owl, night monster</strong>. From <em>layil</em> (night). Appears once in the Hebrew Bible. In later Jewish tradition, the name became associated with a demonic figure.",
 "Isaiah 34:14: 'Desert creatures will meet with hyenas, and wild goats will bleat to each other; there the <em>night creature</em> will also lie down and find for herself a place of rest.' This describes the utter desolation of Edom after God's judgment — a land so completely devastated that only the wildest, most fearsome creatures inhabit it. <strong>The absence of God's blessing reduces a nation to a haunt for desert creatures.</strong> The image serves as a warning: rebellion against God leads to desolation, while obedience leads to fruitfulness (Isaiah 35 immediately follows with restoration).",
 [("Isaiah 34:14", "Desert creatures will meet with hyenas; there the <em>night creature</em> will also lie down and find rest."),
  ("Isaiah 34:11", "The desert owl and screech owl will possess it; the great owl and the raven will nest there."),
  ("Isaiah 35:1", "The desert and the parched land will be glad; the wilderness will rejoice and blossom.")],
 [("H3915", "Layil (Night)"), ("H8577", "Tannîyn (Jackals/Monsters)"), ("H2723", "Chorbāh (Desolation)")]),

# --- H3073 ---
("H3073", "יְהוָה נִסִּי", "Yhvh Nissîy", "Proper Noun (Divine Name)", "The LORD Is My Banner",
 "Yhvh Nissîy — The LORD Is My Banner; God as our rallying point in battle. Strong's H3073.",
 "<em>Yhvh Nissîy</em> (יְהוָה נִסִּי) means <strong>The LORD Is My Banner</strong>. A compound divine name from <em>YHVH</em> + <em>nēs</em> (banner, standard, signal pole). Moses built an altar by this name after the battle with Amalek.",
 "Exodus 17:15: 'Moses built an altar and called it <em>The LORD is my Banner</em>.' The name commemorates Israel's victory over Amalek while Aaron and Hur held Moses' arms aloft. The raised hands with the staff of God functioned as a <strong>battle standard — a rallying point</strong>. When the banner was raised, Israel prevailed; when it dropped, Amalek gained ground. <strong>God Himself is our banner</strong> — the standard around which we rally, the signal that identifies whose army we belong to. Isaiah 11:10: 'the Root of Jesse will stand as a banner for the peoples.' Christ is the ultimate banner.",
 [("Exodus 17:15", "Moses built an altar and called it <em>The LORD is my Banner</em>."),
  ("Exodus 17:11", "As long as Moses held up his hands, the Israelites were winning."),
  ("Isaiah 11:10", "The Root of Jesse will stand as a banner for the peoples; the nations will rally to him.")],
 [("H5251", "Nēs (Banner/Standard)"), ("H4196", "Mizbēach (Altar)"), ("H3068", "YHVH (The LORD)")]),

# --- H6241 ---
("H6241", "עִשָּׂרוֹן", "'issārôn", "Noun, masculine", "Tenth Part, One-Tenth (Ephah)",
 "'Issārôn — the tenth part; the tithe principle woven into daily offerings. Strong's H6241.",
 "<em>'Issārôn</em> (עִשָּׂרוֹן) means <strong>a tenth part, one-tenth of an ephah</strong> — a standard dry measure used in grain offerings. From <em>'eser</em> (ten). Appears frequently in Levitical instructions for daily and festival offerings.",
 "Exodus 29:40: 'With the first lamb offer a <em>tenth</em> of an ephah of the finest flour mixed with a quarter of a hin of oil.' Numbers 28:5: 'a <em>tenth</em> of an ephah of the finest flour for a grain offering.' The <em>'issārôn</em> was the standard unit for grain offerings — <strong>the tithe principle built into the very fabric of daily worship</strong>. Every morning and evening sacrifice included this tenth-part offering, teaching Israel that a portion of their harvest belonged to God. Malachi 3:10: 'Bring the whole tithe into the storehouse.'",
 [("Exodus 29:40", "With the first lamb offer a <em>tenth</em> of an ephah of the finest flour mixed with oil."),
  ("Numbers 28:5", "Together with a grain offering of a <em>tenth</em> of an ephah of the finest flour."),
  ("Malachi 3:10", "Bring the whole tithe into the storehouse, that there may be food in my house.")],
 [("H6235", "'Eser (Ten)"), ("H4503", "Minchāh (Grain Offering)"), ("H374", "'Ēphāh (Ephah)")]),

# --- H5336 ---
("H5336", "נָצִיר", "nātsîyr", "Adjective", "Preserved, Guarded",
 "SKIP", "", "", [], []),  # Rare variant — skip

# --- H4198 ---
("H4198", "מָזֶה", "māzeh", "Adjective", "Exhausted, Lean, Wasted",
 "Māzeh — wasted and exhausted; the cost of untreated grief. Strong's H4198.",
 "<em>Māzeh</em> (מָזֶה) means <strong>exhausted, lean, sucked dry, wasted</strong>. From <em>māzāh</em> (to suck out, to drain). Describes physical depletion.",
 "Isaiah 17:4: 'In that day the glory of Jacob will fade; the fat of his body will <em>waste away</em>.' Israel's coming judgment is described in terms of physical wasting — the nation's prosperity and strength drained away. This is the consequence of persistent unfaithfulness. <strong>Sin is spiritually emaciated</strong> — it promises fullness but delivers depletion. Psalm 106:15: 'He gave them what they asked for, but sent a wasting disease upon them.' Getting what we want apart from God leads to <em>māzeh</em> — a soul sucked dry.",
 [("Isaiah 17:4", "In that day the glory of Jacob will fade; the fat of his body will <em>waste away</em>."),
  ("Psalm 106:15", "He gave them what they asked for, but sent a <em>wasting disease</em> upon them."),
  ("Isaiah 10:16", "The Lord will send a <em>wasting disease</em> upon his sturdy warriors.")],
 [("H7534", "Raq (Thin/Lean)"), ("H1803", "Dallāh (Poverty)"), ("H3615", "Kālāh (To Be Consumed)")]),

# --- H8025 ---
("H8025", "שָׁלַף", "shālaph", "Verb", "To Draw Out, To Pull Out (a sword)",
 "Shālaph — to draw the sword; decisive action in spiritual warfare. Strong's H8025.",
 "<em>Shālaph</em> (שָׁלַף) means <strong>to draw out, to pull out, to unsheathe</strong> — particularly drawing a sword from its scabbard. Also used for pulling off a sandal (Ruth 4:7-8).",
 "Judges 3:22: Ehud plunged his sword into Eglon's belly, and 'even the handle sank in... and Ehud did not <em>draw</em> the sword out.' Judges 8:20: Gideon told Jether to '<em>draw</em> your sword and kill them' — but the boy was afraid. Ruth 4:7-8: the kinsman-redeemer 'drew off his sandal' — transferring rights. <strong>Drawing the sword represents decisive action.</strong> Hebrews 4:12: 'The word of God is alive and active, sharper than any double-edged sword.' When God's Word is drawn, it accomplishes its purpose.",
 [("Judges 3:22", "Even the handle sank in after the blade, and Ehud did not <em>draw</em> the sword out."),
  ("Ruth 4:7-8", "The guardian-redeemer <em>drew off</em> his sandal, saying to Boaz, 'Buy it yourself.'"),
  ("Hebrews 4:12", "The word of God is alive and active. Sharper than any double-edged sword.")],
 [("H2719", "Chereb (Sword)"), ("H5275", "Na'al (Sandal)"), ("H1350", "Gā'al (To Redeem)")]),

# --- H8509 ---
("H8509", "תַּכְרִיךְ", "takrîyk", "Noun, masculine", "Robe, Garment",
 "SKIP", "", "", [], []),  # Rare variant — skip

# --- H7191 ---
("H7191", "קִשְׁיוֹן", "Qishyôn", "Proper Noun", "Kishion",
 "SKIP", "", "", [], []),  # Place name — skip

# --- H3658 ---
("H3658", "כִּנּוֹר", "kinnôr", "Noun, masculine", "Lyre, Harp",
 "Kinnôr — the lyre; music as weapon, worship, and healing. Strong's H3658.",
 "<em>Kinnôr</em> (כִּנּוֹר) means <strong>lyre, harp</strong> — the primary stringed instrument of ancient Israel. It was David's instrument and central to temple worship. First mentioned in Genesis 4:21 as Jubal's invention.",
 "First Samuel 16:23: 'Whenever the spirit from God came on Saul, David would take up his <em>lyre</em> and play. Then relief would come to Saul.' Music as spiritual warfare — David's <em>kinnôr</em> drove away tormenting spirits. Psalm 137:2: 'There on the willows we hung our <em>lyres</em>' — exile silenced Israel's worship. Psalm 150:3: 'Praise him with the harp and <em>lyre</em>.' <strong>The kinnôr represents the full range of human experience before God</strong>: joy in worship, healing in suffering, and silence in exile. Revelation 5:8 shows the elders with harps before the Lamb — worship restored forever.",
 [("1 Samuel 16:23", "David would take up his <em>lyre</em> and play. Then relief would come to Saul; the evil spirit would leave him."),
  ("Psalm 137:2", "There on the willows we hung our <em>lyres</em>."),
  ("Psalm 150:3", "Praise him with the sounding of the trumpet, praise him with the <em>harp</em> and lyre.")],
 [("H5035", "Nēbel (Harp/Lute)"), ("H8596", "Tōph (Tambourine)"), ("H2167", "Zāmar (To Sing Praise)")]),

# --- H8477 ---
("H8477", "תַּחַשׁ", "tachash", "Noun, masculine", "Fine Leather, Porpoise/Seal Skin",
 "Tachash — fine leather for the tabernacle; God's dwelling covered with costly material. Strong's H8477.",
 "<em>Tachash</em> (תַּחַשׁ) means <strong>fine leather, probably porpoise or seal skin</strong> — a durable, weather-resistant material. The exact animal is debated (dugong, dolphin, or fine-grained leather). Used for the tabernacle's outer covering.",
 "Exodus 26:14: 'Make for the tent a covering of ram skins dyed red, and over that a covering of <em>fine leather</em>.' Numbers 4:6: the ark of the covenant was covered with <em>tachash</em> during transport. Ezekiel 16:10: God says to Jerusalem, 'I put sandals of <em>fine leather</em> on you.' <strong>The finest materials were used for God's dwelling</strong> — nothing cheap or second-rate for the place where heaven met earth. This challenges us: do we give God our best, or our leftovers?",
 [("Exodus 26:14", "Make a covering of ram skins dyed red, and over that a covering of <em>fine leather</em>."),
  ("Numbers 4:6", "They are to cover the ark with hides of <em>fine leather</em>, spread a cloth of solid blue over that."),
  ("Ezekiel 16:10", "I clothed you with an embroidered dress and put sandals of <em>fine leather</em> on you.")],
 [("H5785", "'Ôr (Skin/Leather)"), ("H4908", "Mishkān (Tabernacle)"), ("H352", "Ayil (Ram)")]),

# --- H4726 ---
("H4726", "מָקוֹר", "māqôr", "Noun, masculine", "Fountain, Source, Spring",
 "Māqôr — the fountain of life; God as the source of all living water. Strong's H4726.",
 "<em>Māqôr</em> (מָקוֹר) means <strong>fountain, source, spring</strong> — the origin point from which water flows. It is used both literally and as one of Scripture's richest metaphors for life, wisdom, and God Himself.",
 "Jeremiah 2:13: 'My people have committed two sins: They have forsaken me, the <em>spring</em> of living water, and have dug their own cisterns, broken cisterns that cannot hold water.' This is the core indictment of all idolatry: abandoning the <strong>infinite fountain</strong> for cracked containers. Psalm 36:9: 'For with you is the <em>fountain</em> of life; in your light we see light.' Proverbs 14:27: 'The fear of the LORD is a <em>fountain</em> of life.' <strong>God is not a reservoir — He is a spring</strong>. His supply never runs dry; His grace is ever-flowing.",
 [("Jeremiah 2:13", "They have forsaken me, the <em>spring</em> of living water, and have dug broken cisterns that cannot hold water."),
  ("Psalm 36:9", "For with you is the <em>fountain</em> of life; in your light we see light."),
  ("Proverbs 14:27", "The fear of the LORD is a <em>fountain</em> of life, turning a person from the snares of death.")],
 [("H5869", "'Ayin (Spring/Eye)"), ("H4599", "Ma'yān (Spring)"), ("H2416", "Chay (Life)")]),

# --- H1750 ---
("H1750", "דּוּץ", "dûts", "Verb", "To Leap, To Spring",
 "Dûts — to leap for joy; exuberant worship and deliverance. Strong's H1750.",
 "<em>Dûts</em> (דּוּץ) means <strong>to leap, to spring, to jump</strong> — expressing joy, vitality, or sudden movement. It appears in vivid imagery of celebration and restoration.",
 "Malachi 4:2: 'But for you who revere my name, the sun of righteousness will rise with healing in its rays. And you will go out and <em>frolic</em> like well-fed calves.' The image is of calves released from the stall — <strong>exuberant, uncontainable joy</strong>. This is the promise for the faithful remnant: healing, freedom, and overwhelming gladness. The imagery connects to Luke 6:23: 'Rejoice in that day and leap for joy, because great is your reward in heaven.' Authentic worship sometimes looks like leaping — David danced before the ark with all his might (2 Samuel 6:14).",
 [("Malachi 4:2", "You will go out and <em>frolic</em> like well-fed calves."),
  ("2 Samuel 6:14", "David danced before the LORD with all his might."),
  ("Luke 6:23", "Rejoice in that day and leap for joy, because great is your reward in heaven.")],
 [("H7540", "Rāqad (To Dance/Skip)"), ("H1523", "Gîyl (To Rejoice)"), ("H8055", "Sāmach (To Rejoice)")]),

# --- H3759 ---
("H3759", "כַּרְמֶל", "karmel", "Noun, masculine", "Fruitful Field, Garden Land",
 "Karmel — the fruitful field; abundance as the sign of God's blessing. Strong's H3759.",
 "<em>Karmel</em> (כַּרְמֶל) means <strong>fruitful field, garden land, orchard</strong>. It can also mean 'fresh grain' or 'full ears of grain.' Mount Carmel takes its name from this word — the 'fruitful mountain.'",
 "Isaiah 32:15: 'till the Spirit is poured upon us from on high, and the desert becomes a <em>fertile field</em>, and the fertile field seems like a forest.' The transformation from desert to <em>karmel</em> is a prophetic image of <strong>the Holy Spirit's outpouring</strong> — turning barrenness into abundance. Isaiah 35:2: 'it will burst into bloom... the glory of Lebanon will be given to it, the splendor of <em>Carmel</em> and Sharon.' Leviticus 2:14 uses <em>karmel</em> for fresh grain offered as firstfruits — the best of the harvest given to God.",
 [("Isaiah 32:15", "Till the Spirit is poured upon us from on high, and the desert becomes a <em>fertile field</em>."),
  ("Isaiah 35:2", "The glory of Lebanon will be given to it, the splendor of <em>Carmel</em> and Sharon."),
  ("Leviticus 2:14", "If you bring a grain offering of firstfruits, offer crushed heads of new grain (<em>karmel</em>) roasted in the fire.")],
 [("H3754", "Kerem (Vineyard)"), ("H4057", "Midbār (Desert/Wilderness)"), ("H7307", "Rûach (Spirit)")]),

# --- H1484 ---
("H1484", "גּוֹרָל", "gôrāl", "Noun, masculine", "Lot, Portion, Destiny",
 "Gôrāl — the lot; divine determination of destiny and inheritance. Strong's H1484.",
 "<em>Gôrāl</em> (גּוֹרָל) means <strong>lot, portion, allotment, destiny</strong>. Casting lots was the primary method of determining God's will in the OT — not gambling but a sacred practice of seeking divine direction.",
 "Proverbs 16:33: 'The <em>lot</em> is cast into the lap, but its every decision is from the LORD.' This is the theology behind casting lots: <strong>what appears random to humans is directed by God</strong>. Joshua 14:2: the Promised Land was divided 'by <em>lot</em>, as the LORD had commanded.' Leviticus 16:8: on the Day of Atonement, Aaron cast <em>lots</em> for the two goats — one for the LORD, one as the scapegoat. The apostles cast lots to replace Judas (Acts 1:26). In every case, the lot was not chance but divine appointment.",
 [("Proverbs 16:33", "The <em>lot</em> is cast into the lap, but its every decision is from the LORD."),
  ("Joshua 14:2", "Their inheritances were assigned by <em>lot</em>, as the LORD had commanded through Moses."),
  ("Leviticus 16:8", "Aaron shall cast <em>lots</em> for the two goats — one lot for the LORD and the other for the scapegoat.")],
 [("H5307", "Nāphal (To Fall/Cast)"), ("H2506", "Chēleq (Portion/Share)"), ("H5159", "Nachalāh (Inheritance)")]),
]

# ═══════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════

count = 0
for entry in ENTRIES:
    sid, word, trans, pos, gloss, og_desc, defn, usage, verses, related = entry
    if og_desc == "SKIP":
        continue
    build(sid, word, trans, pos, gloss, og_desc, defn, usage, verses, related)
    count += 1

print(f"\n✅ Generated {count} lexicon pages")