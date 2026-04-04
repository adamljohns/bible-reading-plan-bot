#!/usr/bin/env python3
"""Generate 100 lexicon gap-fill pages for USMC Ministries Lexicon."""

import os

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")

def make_page(strongs_id, lang, word, transliteration, pos, gloss,
              definition, usage, verses, related, og_desc):
    lang_label = "Greek · New Testament" if lang == "G" else "Hebrew · Old Testament"
    ext_num = strongs_id[1:]
    if lang == "G":
        step_url = f"https://www.stepbible.org/?q=strong={strongs_id}"
        blb_url = f"https://www.blueletterbible.org/lexicon/g{ext_num}/kjv/tr/0-1/"
        bh_url = f"https://biblehub.com/greek/{ext_num}.htm"
    else:
        step_url = f"https://www.stepbible.org/?q=strong={strongs_id}"
        blb_url = f"https://www.blueletterbible.org/lexicon/h{ext_num}/kjv/wlc/0-1/"
        bh_url = f"https://biblehub.com/hebrew/{ext_num}.htm"

    verse_html = ""
    for ref, text in verses:
        verse_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={ref.replace(' ', '+')}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>"""

    related_html = ""
    for rid, rname in related:
        related_html += f'\n                    <a href="{rid}.html" class="related-word">{rid} — {rname}</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{strongs_id} — {transliteration} | USMC Ministries Lexicon">
    <meta property="og:description" content="{og_desc}">
    <meta name="description" content="{og_desc} USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{strongs_id} — {transliteration} ({gloss}) | USMC Ministries Lexicon</title>
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
        body.light-mode{{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}}body.light-mode nav{{background:rgba(250,248,245,0.97);}}body.light-mode .section{{background:#fff;border-color:#d4d0c8;}}
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
            <span class="strongs-badge">{strongs_id} · {lang_label}</span>
            <div class="original-word">{word}</div>
            <div class="transliteration">{transliteration}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{definition}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{usage}</p>
        </div>
        <div class="section">
            <h2>Key Bible Verses</h2>
            {verse_html}
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
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">© 2026 <a href="../index.html">U.S.M.C. Ministries</a> · <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
    <script>(function(){{if(localStorage.getItem('bte-theme')==='light'){{document.body.classList.add('light-mode');}}}})();</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# WORD DATA
# ─────────────────────────────────────────────
WORDS = [
    # ── GREEK ──
    dict(
        id="G5454", lang="G", word="φωλεός", trans="phōleós", pos="Noun, masculine",
        gloss="Hole, Den, Lair",
        og_desc="The foxes have holes — phōleós means a lair or burrow. Strong's G5454.",
        defn="<em>Phōleós</em> (φωλεός) refers to a <strong>den, burrow, or lair</strong> — the hiding place of a wild animal. It appears once in the New Testament, spoken by Jesus when He describes the homelessness of His earthly ministry.",
        usage="Jesus' use of <em>phōleós</em> in Matthew 8:20 and Luke 9:58 is one of the most arresting contrasts in Scripture. Foxes have dens; birds have nests — but the Son of God, Creator of all creation, had <strong>no permanent home</strong>. This voluntary poverty reflects the kenosis (self-emptying) of Christ: He who owns everything owned nothing. The statement simultaneously warns would-be disciples of the cost of following Jesus and reveals the depth of His identification with the homeless, the displaced, and the exiled. It echoes Isaiah 53:3 — 'He was despised and rejected by mankind, a man of suffering, and familiar with pain.'",
        verses=[
            ("Matthew 8:20", "Jesus replied, 'Foxes have <em>dens</em> and birds have nests, but the Son of Man has no place to lay his head.'"),
            ("Luke 9:58", "Jesus replied, 'Foxes have <em>dens</em> and birds have nests, but the Son of Man has no place to lay his head.'"),
            ("2 Corinthians 8:9", "For you know the grace of our Lord Jesus Christ, that though he was rich, yet for your sake he became poor, so that you through his poverty might become rich."),
        ],
        related=[("G258", "Alōpēx — Fox"), ("G4071", "Peteinon — Bird"), ("G2646", "Katalyma — Lodging/Inn")],
    ),
    dict(
        id="G2820", lang="G", word="κληρόω", trans="klēróō", pos="Verb",
        gloss="To Obtain by Lot, To Be Chosen",
        og_desc="Klēróō — to assign by lot or divine appointment. Strong's G2820.",
        defn="<em>Klēróō</em> (κληρόω) means <strong>to assign by lot, to allot, or to obtain as one's share</strong>. In the passive form, it conveys being chosen or predestined — receiving one's inheritance or portion by divine appointment. It is related to <em>klēros</em> (lot, allotment, inheritance).",
        usage="The single NT occurrence in Ephesians 1:11 uses the passive: believers <em>have been made an inheritance</em> (or <em>have obtained an inheritance</em>) — depending on whether the subject is God or the believer. Either way, the theological weight is profound: salvation is not by human achievement but by <strong>divine lot and election</strong>. God predestines and appoints; His people are His <em>klēros</em> — His chosen possession. This ties to the OT concept of Israel as God's portion (Deuteronomy 32:9: 'the LORD's portion is his people') and to the NT reality that believers are 'a chosen people, a royal priesthood, a holy nation, God's special possession' (1 Peter 2:9).",
        verses=[
            ("Ephesians 1:11", "In him we were also chosen, having been predestined according to the plan of him who works out everything in conformity with the purpose of his will."),
            ("Deuteronomy 32:9", "For the LORD's portion is his people, Jacob his allotted inheritance."),
            ("1 Peter 2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession."),
        ],
        related=[("G2819", "Klēros — Lot, Inheritance"), ("G4309", "Proorizō — Predestine"), ("G1589", "Eklogē — Election")],
    ),
    dict(
        id="G2297", lang="G", word="θαυμάσιος", trans="thaumásios", pos="Adjective",
        gloss="Wonderful, Marvelous",
        og_desc="Thaumásios — wonderful and astonishing works. Strong's G2297.",
        defn="<em>Thaumásios</em> (θαυμάσιος) means <strong>wonderful, marvelous, astonishing</strong> — that which causes wonder and amazement. It is derived from <em>thaumazō</em> (to wonder, marvel) and describes something that transcends ordinary experience and evokes awe.",
        usage="In Matthew 21:15, the chief priests are indignant at the <em>wonderful things</em> Jesus did in the temple — the healings and the children's praise. The irony is sharp: those who should have recognized the Messiah's wonders are instead offended by them. This contrasts with Psalm 118:23, which Jesus quotes: 'The Lord has done this, and it is <em>marvelous</em> in our eyes.' The word invites us to approach God's works with childlike wonder rather than religious cynicism. All of God's redemptive acts — creation, exodus, incarnation, resurrection — are <em>thaumásia</em>: works that should leave us breathless with wonder and praise.",
        verses=[
            ("Matthew 21:15", "But when the chief priests and the teachers of the law saw the <em>wonderful things</em> he did and the children shouting in the temple courts, 'Hosanna to the Son of David,' they were indignant."),
            ("Psalm 118:23", "The Lord has done this, and it is marvelous in our eyes."),
            ("Psalm 139:14", "I praise you because I am fearfully and wonderfully made; your works are wonderful, I know that full well."),
        ],
        related=[("G2296", "Thaumazō — To Marvel"), ("G2298", "Thaumastos — Marvelous"), ("G1411", "Dynamis — Power/Miracle")],
    ),
    dict(
        id="G3542", lang="G", word="νομή", trans="nomḗ", pos="Noun, feminine",
        gloss="Pasture, Feeding, Spreading",
        og_desc="Nomē — pasture and the spread of false teaching. Strong's G3542.",
        defn="<em>Nomē</em> (νομή) has two related meanings: (1) <strong>pasture, feeding ground</strong> — the place where flocks graze; and (2) <strong>spreading, increase</strong> — the advance of something, whether growth or the spread of disease/error. It appears twice in the NT with these contrasting nuances.",
        usage="In John 10:9, Jesus promises that those who enter through Him (the gate) 'will come in and go out, and <em>find pasture</em>' (<em>nomēn</em>). This is the image of abundant, safe provision — the Good Shepherd leads His flock to green pastures (Psalm 23:2). But in 2 Timothy 2:17, Paul warns that false teaching 'will spread like gangrene' (<em>nomēn hexei</em>) — the same word now depicting something cancerous and destructive. The contrast is instructive: truth nourishes and gives life; false doctrine spreads death. The shepherd image demands that elders protect the flock from teachings that 'eat away' rather than feed.",
        verses=[
            ("John 10:9", "I am the gate; whoever enters through me will be saved. They will come in and go out, and find <em>pasture</em>."),
            ("2 Timothy 2:17", "Their teaching will spread like gangrene. Among them are Hymenaeus and Philetus."),
            ("Psalm 23:2", "He makes me lie down in green pastures, he leads me beside quiet waters."),
        ],
        related=[("G4166", "Poimēn — Shepherd"), ("G4168", "Poimnē — Flock"), ("G2347", "Thlipsis — Affliction")],
    ),
    dict(
        id="G3409", lang="G", word="μισθόω", trans="misthóō", pos="Verb",
        gloss="To Hire, To Employ for Wages",
        og_desc="Misthóō — to hire workers; used in the Parable of the Laborers. Strong's G3409.",
        defn="<em>Misthóō</em> (μισθόω) means <strong>to hire, to employ for wages, to engage someone for pay</strong>. It appears in the middle voice in the NT, meaning to hire for one's own use. It is related to <em>misthos</em> (wages, reward) and <em>misthios</em> (hired worker).",
        usage="The word appears in Matthew 20:1 in the Parable of the Laborers in the Vineyard — one of Jesus' most theologically rich parables about grace, generosity, and the nature of God's kingdom. The landowner <em>hires</em> workers at different hours of the day, yet pays them all the same wage. The parable subverts all human calculations of merit and fairness: God's grace cannot be earned by length of service. Those hired at the eleventh hour — latecomers to faith — receive the same eternal life as those who labored longest. This is <strong>scandalous grace</strong>. The parable also challenges envy among God's people: do we resent those who receive mercy later in life?",
        verses=[
            ("Matthew 20:1", "For the kingdom of heaven is like a landowner who went out early in the morning to <em>hire</em> workers for his vineyard."),
            ("Matthew 20:7", "They said to him, 'Because no one has hired us.' He said to them, 'You also go and work in my vineyard.'"),
            ("Luke 15:17", "When he came to his senses, he said, 'How many of my father's hired servants have food to spare, and here I am starving to death!'"),
        ],
        related=[("G3408", "Misthos — Wages/Reward"), ("G3411", "Misthios — Hired Worker"), ("G2040", "Ergatēs — Laborer/Worker")],
    ),
    dict(
        id="G2968", lang="G", word="κώμη", trans="kṓmē", pos="Noun, feminine",
        gloss="Village, Small Town",
        og_desc="Kōmē — village; Jesus' ministry encompassed every village and town. Strong's G2968.",
        defn="<em>Kōmē</em> (κώμη) refers to a <strong>village or small town</strong> — a rural settlement smaller than a city (<em>polis</em>). In the ancient world, villages were agricultural communities without the civic structures of a city. The word appears frequently in the Gospels and Acts.",
        usage="The Gospels emphasize that Jesus' ministry was not confined to prestigious cities but encompassed every <em>kōmē</em> — every village and hamlet. Matthew 9:35 says 'Jesus went through all the towns and villages, teaching in their synagogues, proclaiming the good news of the kingdom and healing every disease and sickness.' This is a portrait of <strong>total, exhaustive ministry</strong> — no community too small, no person too insignificant. Jesus sent His disciples out to villages (Mark 6:6,56; Luke 8:1; 9:6). The Kingdom of God came to ordinary places through ordinary people. This challenges any gospel that only targets the powerful and urban — Christ is Lord of the village too.",
        verses=[
            ("Matthew 9:35", "Jesus went through all the towns and <em>villages</em>, teaching in their synagogues, proclaiming the good news of the kingdom."),
            ("Mark 6:56", "And wherever he went — into <em>villages</em>, towns or countryside — they placed the sick in the marketplaces."),
            ("Luke 9:6", "So they set out and went from <em>village</em> to <em>village</em>, proclaiming the good news and healing people everywhere."),
        ],
        related=[("G4172", "Polis — City"), ("G68", "Agros — Field/Countryside"), ("G2969", "Kōmopolis — Country Town")],
    ),
    dict(
        id="G2769", lang="G", word="κεράτιον", trans="kerátionv", pos="Noun, neuter",
        gloss="Carob Pod, Husks",
        og_desc="Keration — the husks the prodigal son longed to eat. Strong's G2769.",
        defn="<em>Keration</em> (κεράτιον) literally means '<strong>little horn</strong>' (diminutive of <em>keras</em>) and refers to the <strong>carob pod</strong> — the seed pod of the carob tree (Ceratonia siliqua). Carob pods were commonly used as animal fodder in the ancient Near East. The word appears only once in the NT.",
        usage="The single occurrence in Luke 15:16 is one of the most poignant details in all of Scripture. The prodigal son, having 'squandered his wealth in wild living,' is now feeding pigs and longing to eat the <em>keration</em> — the pods the pigs were eating. This image of utter degradation and spiritual rock-bottom is intentional: a Jewish young man, feeding unclean animals and desiring their food, has reached the lowest imaginable point. But it is precisely here — at the carob pods — that he 'comes to his senses' (v.17). The <em>keration</em> is thus the turning point, the moment of repentance. Often, God uses the lowest circumstances to awaken the soul to its need for the Father.",
        verses=[
            ("Luke 15:16", "He longed to fill his stomach with the <em>pods</em> that the pigs were eating, but no one gave him anything."),
            ("Luke 15:17", "When he came to his senses, he said, 'How many of my father's hired servants have food to spare, and here I am starving to death!'"),
            ("Luke 15:20", "So he got up and went to his father. But while he was still a long way off, his father saw him and was filled with compassion for him."),
        ],
        related=[("G5519", "Choiros — Pig"), ("G5590", "Psychē — Soul"), ("G3341", "Metanoia — Repentance")],
    ),
    dict(
        id="G5020", lang="G", word="ταρταρόω", trans="tartaróō", pos="Verb",
        gloss="To Cast into Tartarus/Hell",
        og_desc="Tartaróō — to confine fallen angels to deepest darkness. Strong's G5020.",
        defn="<em>Tartaróō</em> (ταρταρόω) is a verb meaning <strong>to cast into Tartarus</strong> — the lowest abyss of Hades. It appears only once in the NT (2 Peter 2:4). <em>Tartaros</em> was the Greek name for the deepest underworld, below Hades, where the worst offenders were imprisoned. Peter uses this term to describe where God has confined fallen angels.",
        usage="Second Peter 2:4 declares that God 'did not spare angels when they sinned, but cast them into hell (<em>tartarōsas</em>), putting them in chains of darkness to be held for judgment.' This is one of three examples Peter gives of God's certain judgment on the ungodly (the others being Noah's flood and Sodom and Gomorrah). The theological point is clear: <strong>if God did not spare even angels</strong>, how much more certain is judgment on unrepentant humans? Yet in the same passage, Peter affirms that 'the Lord knows how to rescue the godly from trials' (v.9). Divine wrath and divine rescue go together — God is simultaneously the righteous Judge and the faithful Deliverer.",
        verses=[
            ("2 Peter 2:4", "For if God did not spare angels when they sinned, but sent them to hell (<em>tartarus</em>), putting them in chains of darkness to be held for judgment..."),
            ("Jude 1:6", "And the angels who did not keep their positions of authority but abandoned their proper dwelling — these he has kept in darkness, bound with everlasting chains for judgment."),
            ("Revelation 20:10", "And the devil, who deceived them, was thrown into the lake of burning sulfur."),
        ],
        related=[("G86", "Hadēs — Hades/Underworld"), ("G12", "Abyssos — The Abyss"), ("G2923", "Kritēs — Judge")],
    ),
    dict(
        id="G5232", lang="G", word="ὑπεραυξάνω", trans="hyperauxánō", pos="Verb",
        gloss="To Grow Exceedingly, To Increase Abundantly",
        og_desc="Hyperauxánō — faith and love that grow beyond all measure. Strong's G5232.",
        defn="<em>Hyperauxánō</em> (ὑπεραυξάνω) is a compound verb: <em>hyper</em> (over, beyond) + <em>auxanō</em> (to grow, increase). It means <strong>to grow exceedingly, to increase beyond measure, to abound greatly</strong>. It is a superlative of growth. This is the only occurrence in the NT.",
        usage="Paul uses <em>hyperauxánō</em> in 2 Thessalonians 1:3 to describe the Thessalonians' faith: 'We ought always to thank God for you... because your faith is <em>growing exceedingly</em> and the love all of you have for one another is increasing.' This is remarkable encouragement — Paul doesn't just note that their faith is growing, but that it is growing <em>beyond all measure</em>. This reflects an important principle: <strong>spiritual growth is not merely linear but exponential</strong>. Faith that is exercised through trials (which the Thessalonians faced abundantly) grows not gradually but dramatically. God's design is not for maintenance-mode Christianity but for faith that <em>hyperauxanō</em> — overflows its banks.",
        verses=[
            ("2 Thessalonians 1:3", "We ought always to thank God for you, brothers and sisters, and rightly so, because your faith is <em>growing exceedingly</em>, and the love all of you have for one another is increasing."),
            ("Colossians 1:10", "...growing in the knowledge of God, being strengthened with all power according to his glorious might."),
            ("1 Peter 2:2", "Like newborn babies, crave pure spiritual milk, so that by it you may grow up in your salvation."),
        ],
        related=[("G837", "Auxanō — To Grow"), ("G4052", "Perisseuō — To Abound"), ("G4057", "Perissōs — Exceedingly")],
    ),
    dict(
        id="G2338", lang="G", word="θῆλυς", trans="thḗlys", pos="Adjective",
        gloss="Female",
        og_desc="Thēlys — female; used in creation and marriage texts. Strong's G2338.",
        defn="<em>Thēlys</em> (θῆλυς) means <strong>female</strong> — of the female sex, whether human or animal. It appears in contexts discussing creation, marriage, and human sexuality. The word is related to <em>thēlazō</em> (to nurse/suckle), reflecting the nurturing role.",
        usage="The word appears in the creation texts quoted by Jesus (Matthew 19:4; Mark 10:6) and Paul (Romans 1:26; Galatians 3:28). In the creation account, 'male and female he created them' (Genesis 1:27) — <em>arsen kai thēly</em> — establishes sexual differentiation as <strong>God's design</strong>, not cultural accident. Jesus appeals to this as the foundation for lifelong marriage. Paul's use in Romans 1:26 ('even their women exchanged natural sexual relations') references abandonment of this created order as evidence of suppressing the truth in unrighteousness. Galatians 3:28 ('neither male nor female... in Christ') does not erase this distinction but declares that both equally bear God's image and receive salvation.",
        verses=[
            ("Matthew 19:4", "Haven't you read that at the beginning the Creator 'made them male and <em>female</em>'?"),
            ("Galatians 3:28", "There is neither Jew nor Gentile, neither slave nor free, nor is there male and <em>female</em>, for you are all one in Christ Jesus."),
            ("Genesis 1:27", "So God created mankind in his own image... male and female he created them."),
        ],
        related=[("G730", "Arsēn — Male"), ("G1135", "Gynē — Woman/Wife"), ("G444", "Anthrōpos — Human Being")],
    ),
    dict(
        id="G2327", lang="G", word="θερισμός", trans="therismós", pos="Noun, masculine",
        gloss="Harvest, Reaping",
        og_desc="Therismós — the great harvest of souls at the end of the age. Strong's G2327.",
        defn="<em>Therismós</em> (θερισμός) means <strong>harvest</strong> — the reaping of grain or crops at the end of the growing season. In biblical usage, harvest becomes a rich metaphor for <strong>the gathering of souls</strong> — both in evangelism and in final eschatological judgment.",
        usage="Jesus uses <em>therismós</em> in multiple contexts. In Matthew 9:37-38, 'the harvest is plentiful but the workers are few' — a call to urgent evangelism. The fields are ready; souls are receptive; what is lacking are laborers willing to go. In Matthew 13:39, the harvest is 'the end of the age' — the final judgment when angels reap the earth, separating righteous from wicked. John 4:35 adds another dimension: 'open your eyes and look at the fields! They are ripe for harvest' — Jesus sees spiritual readiness where others see time barriers. <strong>The harvest theology of Scripture demands urgency</strong>: seasons pass, opportunity closes, and God calls His people to participate in His redemptive work before the final reaping.",
        verses=[
            ("Matthew 9:37-38", "Then he said to his disciples, 'The <em>harvest</em> is plentiful but the workers are few. Ask the Lord of the harvest, therefore, to send out workers into his harvest field.'"),
            ("Matthew 13:39", "The enemy who sows them is the devil. The <em>harvest</em> is the end of the age, and the harvesters are angels."),
            ("John 4:35", "Don't you have a saying, 'It's still four months until <em>harvest</em>'? I tell you, open your eyes and look at the fields! They are ripe for harvest."),
        ],
        related=[("G2325", "Therizō — To Reap/Harvest"), ("G4687", "Speirō — To Sow"), ("G2326", "Theristēs — Reaper")],
    ),
    dict(
        id="G2303", lang="G", word="θεῖον", trans="theîon", pos="Noun, neuter",
        gloss="Brimstone, Sulfur",
        og_desc="Theîon — brimstone; the divine fire of judgment in Revelation. Strong's G2303.",
        defn="<em>Theîon</em> (θεῖον) means <strong>brimstone or sulfur</strong> — the burning mineral associated with divine judgment. The word shares its root with <em>theos</em> (God), reflecting the ancient belief that burning sulfur was 'divine fire' or 'divine stone.' It appears primarily in Revelation.",
        usage="Brimstone in Scripture is consistently associated with <strong>divine judgment and wrath</strong>. The destruction of Sodom and Gomorrah (Genesis 19:24) established the archetype: 'the LORD rained down burning sulfur on Sodom and Gomorrah.' Revelation amplifies this: the lake of fire burns with <em>theion</em> (sulfur) — the final destination for Satan, the beast, the false prophet, and all whose names are not in the Book of Life (Revelation 19:20; 20:10; 21:8). The imagery is intentionally catastrophic — complete, irreversible destruction. Yet even this serves God's holiness: <strong>a God who tolerates evil forever is not holy</strong>. The lake of fire is the ultimate expression that God takes sin seriously. The good news is that Christ drank the cup of wrath so that believers need not.",
        verses=[
            ("Revelation 21:8", "But the cowardly, the unbelieving, the vile, the murderers... their place will be in the fiery lake of burning sulfur (<em>theion</em>)."),
            ("Revelation 19:20", "The two of them were thrown alive into the fiery lake of burning <em>sulfur</em>."),
            ("Genesis 19:24", "Then the LORD rained down burning sulfur on Sodom and Gomorrah — from the LORD out of the heavens."),
        ],
        related=[("G4442", "Pyr — Fire"), ("G3041", "Limnē — Lake"), ("G2288", "Thanatos — Death")],
    ),
    dict(
        id="G5505", lang="G", word="χίλιοι", trans="chílioi", pos="Adjective/Numeral",
        gloss="One Thousand",
        og_desc="Chílioi — a thousand; including the millennial reign of Christ. Strong's G5505.",
        defn="<em>Chílioi</em> (χίλιοι) means <strong>one thousand</strong>. The word is significant not only as a numeral but as a theological symbol of completeness, fullness, and divine abundance. It appears throughout Revelation in the context of the millennium.",
        usage="In Revelation 20:1-7, <em>chílioi</em> appears six times in the description of Satan being bound 'for a thousand years' and Christ's saints reigning 'for a thousand years.' This passage is the foundation for <strong>millennial theology</strong> — the debate between premillennialism, amillennialism, and postmillennialism centers on whether this thousand years is literal or symbolic. Beyond eschatology, <em>chílioi</em> echoes Psalm 90:4 (quoted in 2 Peter 3:8): 'With the Lord a day is like a thousand years, and a thousand years are like a day' — reminding us that God's perspective on time is radically different from ours. The number also appears in promises of blessing: Deuteronomy 7:9 says God keeps covenant faithfulness 'to a thousand generations.'",
        verses=[
            ("Revelation 20:2-3", "He seized the dragon... and bound him for a <em>thousand years</em>... to keep him from deceiving the nations anymore until the thousand years were ended."),
            ("2 Peter 3:8", "But do not forget this one thing, dear friends: With the Lord a day is like a <em>thousand years</em>, and a thousand years are like a day."),
            ("Deuteronomy 7:9", "Know therefore that the LORD your God is God... maintaining his love to a <em>thousand</em> generations."),
        ],
        related=[("G5507", "Chiliás — A Group of Thousand"), ("G3461", "Myrias — Ten Thousand"), ("G165", "Aiōn — Age/Eternity")],
    ),
    dict(
        id="G4426", lang="G", word="πτοέω", trans="ptoéō", pos="Verb",
        gloss="To Terrify, To Frighten",
        og_desc="Ptoéō — the command not to be terrified by wars and upheaval. Strong's G4426.",
        defn="<em>Ptoéō</em> (πτοέω) means <strong>to terrify, to frighten, to cause panic</strong>. In the passive, it means 'to be terrified or alarmed.' It appears in the NT in the context of eschatological reassurance — Jesus commanding His disciples not to be seized by panic at disturbing events.",
        usage="Luke 21:9 records Jesus saying, 'When you hear of wars and uprisings, do not be <em>frightened</em> (<em>ptoeisthe</em>). These things must happen first, but the end will not come right away.' The command is a pastoral one: Jesus anticipates that His people will face deeply alarming news — wars, natural disasters, persecution — and He preemptively commands <strong>non-panic</strong>. This is not denial of danger but faith-grounded calm. The same word appears in Luke 24:37 when the disciples see the risen Jesus and 'were startled and frightened' — the verb of human terror in the presence of the supernatural. The antidote to <em>ptoéō</em> is trust in the sovereignty of God who declares 'these things must happen.'",
        verses=[
            ("Luke 21:9", "When you hear of wars and uprisings, do not be <em>frightened</em>. These things must happen first, but the end will not come right away."),
            ("Luke 24:37", "They were startled and <em>frightened</em>, thinking they saw a ghost."),
            ("Isaiah 41:10", "So do not fear, for I am with you; do not be dismayed, for I am your God."),
        ],
        related=[("G5399", "Phobéō — To Fear"), ("G1169", "Deilos — Cowardly/Fearful"), ("G2292", "Tharreō — To Be Bold")],
    ),
    dict(
        id="G5226", lang="G", word="ὑπείκω", trans="hypeíkō", pos="Verb",
        gloss="To Submit, To Yield",
        og_desc="Hypeíkō — submit to spiritual leaders who watch over your soul. Strong's G5226.",
        defn="<em>Hypeíkō</em> (ὑπείκω) means <strong>to submit, to yield, to give way</strong>. It conveys the idea of stepping aside, deferring to another's authority, or yielding ground without resistance. It appears only once in the NT.",
        usage="Hebrews 13:17 commands, 'Have confidence in your leaders and <em>submit</em> to their authority, because they keep watch over you as those who must give an account. Do this so that their work will be a joy, not a burden, for that would be of no benefit to you.' The theological logic is pastoral accountability: church leaders will give account to God for the souls in their care, so submission to godly leadership is not servility but wisdom. <em>Hypeíkō</em> is not blind obedience — it assumes leaders who are themselves submitted to God's Word. Genuine Christian community requires <strong>mutual submission and trust</strong>. When leaders lead faithfully and congregants submit willingly, the work of ministry becomes a joy rather than a burden.",
        verses=[
            ("Hebrews 13:17", "Have confidence in your leaders and <em>submit</em> to their authority, because they keep watch over you as those who must give an account."),
            ("1 Peter 5:5", "In the same way, you who are younger, submit yourselves to your elders. All of you, clothe yourselves with humility toward one another."),
            ("Ephesians 5:21", "Submit to one another out of reverence for Christ."),
        ],
        related=[("G5293", "Hypotassō — To Submit"), ("G3980", "Peitharcheō — To Obey"), ("G4291", "Proistēmi — To Lead/Manage")],
    ),
    dict(
        id="G3715", lang="G", word="ὄρεξις", trans="órexis", pos="Noun, feminine",
        gloss="Desire, Longing, Appetite",
        og_desc="Orexis — sinful desire and disordered appetite. Strong's G3715.",
        defn="<em>Orexis</em> (ὄρεξις) means <strong>desire, longing, appetite</strong> — the reaching out of the soul toward something. It can be neutral (desire generally) but in the one NT occurrence, it is used negatively of disordered sexual appetite. The term was used in Greek philosophy for the appetitive faculty of the soul.",
        usage="Romans 1:27 uses <em>orexis</em> in describing those who 'were inflamed with <em>lust</em> (<em>orexei</em>) for one another.' The context is Paul's description of the downward spiral of idolatry: when humanity exchanges the Creator for the creature, God gives them over to disordered desires. The passage is not primarily about sexuality but about the <strong>corruption of appetite when God is rejected</strong>. All human desire was created good — for God, for beauty, for connection, for nourishment. But when separated from God, these desires become disordered, consuming, and destructive. The gospel restores <em>orexis</em> to its proper order: 'Delight yourself in the LORD, and he will give you the desires of your heart' (Psalm 37:4).",
        verses=[
            ("Romans 1:27", "In the same way the men also abandoned natural relations with women and were inflamed with <em>lust</em> for one another."),
            ("Psalm 37:4", "Take delight in the LORD, and he will give you the desires of your heart."),
            ("Galatians 5:24", "Those who belong to Christ Jesus have crucified the flesh with its passions and desires."),
        ],
        related=[("G1939", "Epithymia — Desire/Lust"), ("G3806", "Pathos — Passion"), ("G4561", "Sarx — Flesh")],
    ),
    dict(
        id="G3080", lang="G", word="λύσις", trans="lýsis", pos="Noun, feminine",
        gloss="Loosing, Release, Separation",
        og_desc="Lysis — release from the bond of marriage; Paul's counsel to the unmarried. Strong's G3080.",
        defn="<em>Lýsis</em> (λύσις) means <strong>loosing, releasing, dissolving, separation</strong>. It is derived from <em>lyō</em> (to loose, untie, dissolve). In the NT it appears once in the context of the marriage bond.",
        usage="In 1 Corinthians 7:27, Paul asks: 'Are you pledged to a woman? Do not seek to be <em>released</em> (<em>lysin</em>). Are you free from such a commitment? Do not look for a wife.' Paul's counsel reflects his eschatological urgency — the present crisis makes singleness advantageous for undistracted devotion to God. The word <em>lysis</em> here refers to <strong>release from a marital or betrothal commitment</strong>. Paul is not denigrating marriage (which he calls honorable in Hebrews 13:4) but placing it in eschatological perspective: in light of eternity, what matters is full-hearted devotion to Christ, whether married or unmarried. Both states are gifts when lived in consecration to God.",
        verses=[
            ("1 Corinthians 7:27", "Are you pledged to a woman? Do not seek to be <em>released</em>. Are you free from such a commitment? Do not look for a wife."),
            ("1 Corinthians 7:32-33", "An unmarried man is concerned about the Lord's affairs — how he can please the Lord. But a married man is concerned about the affairs of this world — how he can please his wife."),
            ("Hebrews 13:4", "Marriage should be honored by all, and the marriage bed kept pure."),
        ],
        related=[("G3089", "Lyō — To Loose/Dissolve"), ("G1135", "Gynē — Woman/Wife"), ("G1056", "Gamizō — To Give in Marriage")],
    ),
    dict(
        id="G4441", lang="G", word="πυνθάνομαι", trans="pynthánomai", pos="Verb",
        gloss="To Inquire, To Ask, To Seek Information",
        og_desc="Pynthánomai — to inquire diligently; the Magi asking where Christ was born. Strong's G4441.",
        defn="<em>Pynthánomai</em> (πυνθάνομαι) means <strong>to inquire, to ask questions, to seek information by asking</strong>. It implies deliberate inquiry — asking to find out something specific. It appears in the Gospels, Acts, and other NT passages.",
        usage="The word appears at key moments of inquiry in the NT. In Matthew 2:4, Herod 'asked' (<em>epythaneto</em>) where the Messiah was to be born — a sinister inquiry with murderous intent, contrasting with the Magi's sincere seeking. In John 4:52, a royal official 'inquired' at what hour his son had gotten better — discovering the healing was simultaneous with Jesus' word. In Acts 4:7, the Sanhedrin 'asked' Peter and John by what power they healed. <strong>Inquiry is not inherently good or bad</strong> — what matters is the disposition of the heart. True seekers find (Matthew 7:7-8); those who inquire to destroy are ultimately destroyed. The word also echoes Jeremiah 29:13: 'You will seek me and find me when you seek me with all your heart.'",
        verses=[
            ("Matthew 2:4", "When he had called together all the people's chief priests and teachers of the law, he asked them where the Messiah was to be born."),
            ("John 4:52", "When he <em>inquired</em> as to the time when his son got better, they said to him, 'Yesterday, at one in the afternoon, the fever left him.'"),
            ("Acts 10:18", "They called out, asking whether Simon who was known as Peter was staying there."),
        ],
        related=[("G2065", "Erōtaō — To Ask/Request"), ("G154", "Aiteō — To Ask/Petition"), ("G1934", "Epizēteō — To Seek After")],
    ),
    dict(
        id="G4041", lang="G", word="περιούσιος", trans="perioúsios", pos="Adjective",
        gloss="Special, Peculiar, God's Own Possession",
        og_desc="Perioúsios — God's special, treasured possession; the covenant people. Strong's G4041.",
        defn="<em>Perioúsios</em> (περιούσιος) means <strong>one's own special possession, peculiar, chosen as special property</strong>. It comes from <em>peri</em> (around, exceedingly) + <em>ousia</em> (being, property). In the Septuagint, it translates the Hebrew <em>segullah</em> — a personal treasure or prized possession.",
        usage="Titus 2:14 says Christ 'gave himself for us to redeem us from all wickedness and to purify for himself a <em>people that are his very own</em> (<em>laon periousion</em>), eager to do what is good.' This is one of the richest descriptions of the church in the NT. The background is the Sinai covenant: 'you will be my treasured possession (<em>segullah</em>) out of all nations' (Exodus 19:5). God chose Israel as His special people, and through Christ, this identity is extended to all who believe. The church is not merely a religious organization but <strong>God's own prized possession</strong> — people He bought at infinite cost. This identity should produce holiness ('eager to do what is good') — we live as befits those who are treasured by God.",
        verses=[
            ("Titus 2:14", "Who gave himself for us to redeem us from all wickedness and to purify for himself a <em>people that are his very own</em>, eager to do what is good."),
            ("Exodus 19:5", "Although the whole earth is mine, you will be for me a kingdom of priests and a holy nation."),
            ("1 Peter 2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession."),
        ],
        related=[("G1588", "Eklektos — Chosen/Elect"), ("G2992", "Laos — People"), ("G4327", "Prosdechomai — To Await Eagerly")],
    ),
    dict(
        id="G3061", lang="G", word="λοιμός", trans="loimós", pos="Noun, masculine",
        gloss="Plague, Pestilence",
        og_desc="Loimós — plague; one of the signs of the last days. Strong's G3061.",
        defn="<em>Loimós</em> (λοιμός) means <strong>plague, pestilence, deadly epidemic</strong>. In a figurative sense, it can also mean a 'pest' — a troublesome, dangerous person. Both senses appear in the NT.",
        usage="Jesus lists <em>loimós</em> among the signs of the end of the age in Luke 21:11: 'There will be great earthquakes, famines and <em>pestilences</em> in various places, and fearful events and great signs from heaven.' Plagues appear throughout biblical history as divine judgments (the Egyptian plagues, the Assyrian plague of 2 Kings 19:35) and eschatological warnings. In Revelation, pestilence is one of the four horsemen's instruments (6:8). In Acts 24:5, Paul's accusers call him 'a <em>plague</em>' (<em>loimon</em>) — using the word as an insult. The theological response to plague is not fatalism but <strong>trust in the sovereign God</strong> who 'will command his angels concerning you to guard you in all your ways' (Psalm 91:11), and prayer for mercy as in Joel 1-2.",
        verses=[
            ("Luke 21:11", "There will be great earthquakes, famines and <em>pestilences</em> in various places, and fearful events and great signs from heaven."),
            ("Revelation 6:8", "...and Hades was following close behind him. They were given power over a fourth of the earth to kill by sword, famine and <em>plague</em>."),
            ("Psalm 91:3", "Surely he will save you from the fowler's snare and from the deadly <em>pestilence</em>."),
        ],
        related=[("G3042", "Limos — Famine"), ("G4578", "Seismos — Earthquake"), ("G2288", "Thanatos — Death")],
    ),
    dict(
        id="G3359", lang="G", word="μέτωπον", trans="métōpon", pos="Noun, neuter",
        gloss="Forehead",
        og_desc="Métōpon — the forehead marked with God's seal or the beast's mark. Strong's G3359.",
        defn="<em>Métōpon</em> (μέτωπον) means <strong>forehead</strong> — the front of the face above the eyes. In Revelation, the forehead becomes a site of profound spiritual significance: it is where both the mark of the beast and the seal of God are placed, signifying allegiance and ownership.",
        usage="In Revelation, the <em>métōpon</em> (forehead) appears eight times as the location of identity marks. The 144,000 have the Father's name written on their foreheads (14:1). God's servants receive His seal on their foreheads as protection (7:3; 9:4). Conversely, those who worship the beast receive his mark on their foreheads (13:16; 14:9). In the New Jerusalem, God's servants 'will see his face, and his name will be on their <em>foreheads</em>' (22:4). This imagery draws on the OT: the high priest wore 'HOLY TO THE LORD' on his forehead (Exodus 28:36-38), and God commanded Israel to bind His words as a sign 'on your foreheads' (Deuteronomy 6:8). <strong>The forehead represents conscious allegiance</strong> — who owns your mind and will.",
        verses=[
            ("Revelation 22:4", "They will see his face, and his name will be on their <em>foreheads</em>."),
            ("Revelation 13:16", "It also forced all people... to receive a mark on their right hands or on their <em>foreheads</em>."),
            ("Revelation 14:1", "There before me was the Lamb... and with him 144,000 who had his name and his Father's name written on their <em>foreheads</em>."),
        ],
        related=[("G4973", "Sphragis — Seal"), ("G5480", "Charagma — Mark/Stamp"), ("G3686", "Onoma — Name")],
    ),
    dict(
        id="G2767", lang="G", word="κεράννυμι", trans="keránnymi", pos="Verb",
        gloss="To Mix, To Mingle (Wine)",
        og_desc="Keránnymi — to pour out mixed wine; God's cup of wrath unmixed. Strong's G2767.",
        defn="<em>Keránnymi</em> (κεράννυμι) means <strong>to mix, to mingle</strong> — particularly the mixing of wine with water (a common ancient practice to dilute wine) or the mixing of spices into wine. In Revelation, it appears in the context of divine judgment.",
        usage="In Revelation 14:10, those who receive the mark of the beast 'will drink the wine of God's fury, which has been <em>poured full strength</em> (<em>kekerasmenou akratou</em>) into the cup of his wrath.' The Greek is striking: the wine has been <em>mixed</em> — but <em>unmixed</em> (akratos), meaning full strength, undiluted. This is a deliberate paradox emphasizing the <strong>unmitigated severity of divine wrath</strong>. In Revelation 18:6, Babylon is told to be paid back double — 'mix her a double portion from her own cup.' The image draws on OT texts like Psalm 75:8 ('In the LORD's hand is a cup full of foaming wine mixed with spices; he pours it out'). The cup of wrath is the counterpart to the cup of blessing (1 Corinthians 10:16) that Christ offered His disciples.",
        verses=[
            ("Revelation 14:10", "...they, too, will drink the wine of God's fury, which has been poured full strength into the cup of his wrath."),
            ("Revelation 18:6", "Give back to her as she has given; pay her back double for what she has done. Pour her a double portion from her own cup."),
            ("Psalm 75:8", "In the LORD's hand is a cup full of foaming wine mixed with spices; he pours it out."),
        ],
        related=[("G3631", "Oinos — Wine"), ("G4221", "Potērion — Cup"), ("G3709", "Orgē — Wrath")],
    ),
    dict(
        id="G2709", lang="G", word="καταχθόνιος", trans="katachthónios", pos="Adjective",
        gloss="Under the Earth, Subterranean",
        og_desc="Katachthónios — beings under the earth bow at the name of Jesus. Strong's G2709.",
        defn="<em>Katachthónios</em> (καταχθόνιος) means <strong>under the earth, subterranean</strong> — beings or things existing beneath the surface of the earth. In Greek cosmology, this referred to the realm of the dead. It appears once in the NT.",
        usage="Philippians 2:10 declares that at the name of Jesus 'every knee should bow, in heaven and on earth and <em>under the earth</em> (<em>katachthoniōn</em>).' This is the cosmic scope of Christ's lordship: not just the living and the blessed, but even those in the realm of the dead — every power, principality, and being in all of creation — must ultimately bow before Jesus. The context is the great Christ-hymn of Philippians 2:6-11, describing the kenosis (self-emptying) and subsequent exaltation of Christ. The one who descended to the lowest point (the cross, even death) has been exalted to the highest point, with universal lordship. <strong>No realm is outside Christ's sovereignty</strong> — not even death itself.",
        verses=[
            ("Philippians 2:10", "...that at the name of Jesus every knee should bow, in heaven and on earth and <em>under the earth</em>."),
            ("Revelation 5:13", "Then I heard every creature in heaven and on earth and <em>under the earth</em> and on the sea, and all that is in them, saying: 'To him who sits on the throne and to the Lamb be praise and honor.'"),
            ("Isaiah 45:23", "Before me every knee will bow; by me every tongue will swear."),
        ],
        related=[("G3771", "Ouranios — Heavenly"), ("G1919", "Epigeios — Earthly"), ("G2962", "Kyrios — Lord")],
    ),
    dict(
        id="G2734", lang="G", word="κατοπτρίζομαι", trans="katoptrízomai", pos="Verb",
        gloss="To Behold as in a Mirror, To Reflect",
        og_desc="Katoptrízomai — beholding Christ's glory transforms us into His image. Strong's G2734.",
        defn="<em>Katoptrízomai</em> (κατοπτρίζομαι) means <strong>to behold as in a mirror</strong> or <strong>to reflect like a mirror</strong>. Ancient mirrors were polished metal, giving an imperfect but real reflection. The word combines <em>kata</em> (fully) + <em>optron</em> (mirror). It appears once in the NT in a theologically profound passage.",
        usage="Second Corinthians 3:18 contains one of Paul's most beautiful statements: 'And we all, who with unveiled faces contemplate the Lord's glory, are being <em>transformed into his image</em> with ever-increasing glory, which comes from the Lord, who is the Spirit.' The image is of Moses, whose face radiated glory after being with God (but who veiled it). Now, in Christ, the veil is removed — and believers <em>behold</em> (or <em>reflect</em>) God's glory in the face of Christ. As we behold, we become. <strong>This is the central mechanism of sanctification</strong>: prolonged, attentive beholding of Christ transforms us into His likeness. This is why Bible reading, prayer, worship, and meditation are not optional — they are the means by which God does His transformative work.",
        verses=[
            ("2 Corinthians 3:18", "And we all, who with unveiled faces contemplate the Lord's glory, are being transformed into his image with ever-increasing glory, which comes from the Lord, who is the Spirit."),
            ("2 Corinthians 4:6", "For God, who said, 'Let light shine out of darkness,' made his light shine in our hearts to give us the light of the knowledge of God's glory displayed in the face of Christ."),
            ("1 John 3:2", "Dear friends, now we are children of God, and what we will be has not yet been made known. But we know that when Christ appears, we shall be like him, for we shall see him as he is."),
        ],
        related=[("G2072", "Esoptron — Mirror"), ("G3339", "Metamorphoō — To Transform"), ("G1391", "Doxa — Glory")],
    ),
    dict(
        id="G4131", lang="G", word="πλήκτης", trans="plḗktēs", pos="Noun, masculine",
        gloss="A Striker, Bully, Violent Person",
        og_desc="Plēktēs — a violent bully; disqualified from church leadership. Strong's G4131.",
        defn="<em>Plḗktēs</em> (πλήκτης) means <strong>a striker, a pugnacious person, a bully</strong> — someone who uses physical violence or is prone to fighting. Derived from <em>plēssō</em> (to strike, to smite). It appears in the qualifications lists for church leaders.",
        usage="In 1 Timothy 3:3 and Titus 1:7, overseers (elders/bishops) must be 'not <em>violent</em> (<em>plēktēn</em>), but gentle.' The word appears specifically in the negative list for leadership qualifications. The contrast is 'gentle' (<em>epieikēs</em>) — a word describing gracious, considerate, non-coercive character. <strong>Christian leadership is incompatible with domination and violence</strong>. This was radical in a Greco-Roman world where authority was often exercised by force. Jesus modeled the alternative: 'I am gentle and humble in heart' (Matthew 11:29). A leader who bullies, intimidates, or physically dominates is disqualified — not because the church has low standards, but because Christ-shaped leadership looks like a servant, not a tyrant.",
        verses=[
            ("1 Timothy 3:3", "...not given to drunkenness, <em>not violent</em> but gentle, not quarrelsome, not a lover of money."),
            ("Titus 1:7", "Since an overseer manages God's household, he must be blameless... <em>not violent</em>, not pursuing dishonest gain."),
            ("Matthew 11:29", "Take my yoke upon you and learn from me, for I am gentle and humble in heart, and you will find rest for your souls."),
        ],
        related=[("G1933", "Epieikēs — Gentle/Considerate"), ("G269", "Amachos — Non-Combative"), ("G1985", "Episkopos — Overseer/Bishop")],
    ),
    dict(
        id="G3646", lang="G", word="ὁλοκαύτωμα", trans="holokautōma", pos="Noun, neuter",
        gloss="Whole Burnt Offering, Holocaust",
        og_desc="Holokautōma — the whole burnt offering fulfilled and surpassed in Christ. Strong's G3646.",
        defn="<em>Holokautōma</em> (ὁλοκαύτωμα) means <strong>whole burnt offering</strong> — a sacrifice in which the entire animal is consumed by fire, nothing being reserved. From <em>holos</em> (whole) + <em>kautos</em> (burned). This was the most complete form of OT sacrifice, representing total consecration.",
        usage="The word appears three times in the NT, all in Mark 12:33 and Hebrews 10:6,8 (quoting Psalm 40:6). In Mark 12:33, a scribe tells Jesus that loving God and neighbor 'is more important than all <em>burnt offerings</em> and sacrifices.' Jesus affirms he is 'not far from the kingdom of God' — showing that the OT sacrificial system always pointed beyond itself to heart-obedience. Hebrews 10:6,8 quotes Psalm 40 to show that God 'did not desire' mere ritual sacrifices but a body prepared for Christ to offer — the ultimate <em>holokautōma</em>. <strong>Jesus is the whole burnt offering</strong>: completely given, nothing held back, totally consumed in the fire of divine judgment on our behalf. Romans 12:1 calls us to respond with our own living sacrifice.",
        verses=[
            ("Hebrews 10:6", "You did not delight in burnt offerings and sacrifices for sin."),
            ("Mark 12:33", "To love him with all your heart... is more important than all <em>burnt offerings</em> and sacrifices."),
            ("Romans 12:1", "Therefore, I urge you, brothers and sisters, in view of God's mercy, to offer your bodies as a living sacrifice, holy and pleasing to God."),
        ],
        related=[("G2378", "Thysia — Sacrifice"), ("G749", "Archiereus — High Priest"), ("G2434", "Hilasmos — Propitiation")],
    ),
    dict(
        id="G2407", lang="G", word="ἱερατεύω", trans="hierateúō", pos="Verb",
        gloss="To Serve as Priest, To Exercise Priestly Office",
        og_desc="Hierateúō — the priestly service; all believers now serve as priests. Strong's G2407.",
        defn="<em>Hierateúō</em> (ἱερατεύω) means <strong>to serve as a priest, to perform priestly duties, to exercise the priestly office</strong>. It appears once in the NT in Luke's Gospel and is related to <em>hiereus</em> (priest) and <em>hieron</em> (temple).",
        usage="Luke 1:8 records that Zechariah was '<em>serving as priest</em> before God, his division being on duty.' This sets the scene for the angelic announcement of John the Baptist's birth. The priestly ministry — offering incense, maintaining the temple — was the highest religious duty in Israel, done in God's presence. The NT then makes a stunning application: through Christ, <strong>all believers are priests</strong> (1 Peter 2:5,9; Revelation 1:6; 5:10). The veil has been torn; every believer has direct access to God. The 'priestly service' of the church is no longer animal sacrifice but the 'sacrifice of praise' (Hebrews 13:15) and living as holy instruments of God's glory. Every Christian daily exercises a priestly calling.",
        verses=[
            ("Luke 1:8", "Once when Zechariah's division was on duty and he was <em>serving as priest</em> before God..."),
            ("1 Peter 2:9", "But you are a chosen people, a royal priesthood, a holy nation, God's special possession."),
            ("Revelation 1:6", "...and has made us to be a kingdom and priests to serve his God and Father — to him be glory and power for ever and ever!"),
        ],
        related=[("G2409", "Hiereus — Priest"), ("G2405", "Hierateia — Priesthood"), ("G2420", "Hierōsynē — Priestly Office")],
    ),
    dict(
        id="G4971", lang="G", word="σφόδρως", trans="sphodrōs", pos="Adverb",
        gloss="Exceedingly, Vehemently, With Great Force",
        og_desc="Sphodrōs — the violent wind on Paul's ship; intensity and extremity. Strong's G4971.",
        defn="<em>Sphodrōs</em> (σφόδρως) is an adverb meaning <strong>exceedingly, vehemently, with great force or intensity</strong>. Related to the adjective <em>sphodros</em> (vehement, extreme). It appears once in the NT to describe a violent storm.",
        usage="Acts 27:18 records: 'We took such a violent battering from the storm that the next day they began to throw the cargo overboard.' The storm is described as <em>sphodrōs</em> — extreme in its violence. Paul's voyage to Rome is a narrative of divine providence through chaos: storms, shipwreck, snakebite, yet God guarantees that all 276 persons aboard will survive (Acts 27:22-24). The <em>sphodrōs</em> storm is the context in which Paul's faith shines brightest — he stands and declares, 'I urge you to keep up your courage, because not one of you will be lost.' <strong>Extreme circumstances reveal who truly trusts God.</strong> The storm that terrifies others becomes the stage for the believer's testimony.",
        verses=[
            ("Acts 27:18", "We took such a violent battering from the storm that the next day they began to throw the cargo overboard."),
            ("Acts 27:22-24", "'But now I urge you to keep up your courage, because not one of you will be lost... Last night an angel of the God to whom I belong and whom I serve stood beside me.'"),
            ("Psalm 107:28-29", "Then they cried out to the LORD in their trouble, and he brought them out of their distress. He stilled the storm to a whisper."),
        ],
        related=[("G5492", "Cheimazō — To Be Storm-Tossed"), ("G417", "Anemos — Wind"), ("G2366", "Thyella — Whirlwind/Storm")],
    ),
    dict(
        id="G2893", lang="G", word="κουφίζω", trans="kouphízō", pos="Verb",
        gloss="To Lighten, To Ease a Load",
        og_desc="Kouphízō — lightening the ship's load in a storm; God lifts our burdens. Strong's G2893.",
        defn="<em>Kouphízō</em> (κουφίζω) means <strong>to lighten, to make light, to ease a burden or load</strong>. Derived from <em>kouphos</em> (light in weight). It appears once in Acts in a nautical context.",
        usage="Acts 27:38 records that after sharing bread, 'they lightened the ship by throwing the grain into the sea.' This is part of the dramatic shipwreck narrative in Acts 27. The practical action of <em>kouphizō</em> — lightening the load — allowed the ship to ride higher in the water and potentially reach shore. But the word also carries metaphorical resonance in Christian thought. <strong>God specializes in lightening loads.</strong> Jesus invites, 'Come to me, all you who are weary and burdened, and I will give you rest' (Matthew 11:28) — a divine <em>kouphizō</em>. The Christian life involves both holding on (faith) and letting go (casting burdens on God). Sometimes survival requires throwing overboard what was once valuable cargo.",
        verses=[
            ("Acts 27:38", "When they had eaten as much as they wanted, they <em>lightened</em> the ship by throwing the grain into the sea."),
            ("Matthew 11:28-30", "'Come to me, all you who are weary and burdened, and I will give you rest. Take my yoke upon you and learn from me.'"),
            ("1 Peter 5:7", "Cast all your anxiety on him because he cares for you."),
        ],
        related=[("G5413", "Phortion — Burden/Load"), ("G922", "Baros — Weight/Burden"), ("G373", "Anapauō — To Give Rest")],
    ),
    dict(
        id="G4229", lang="G", word="πρᾶγμα", trans="prâgma", pos="Noun, neuter",
        gloss="Thing, Matter, Affair, Deed",
        og_desc="Pragma — a matter or affair; the things of God vs. the things of men. Strong's G4229.",
        defn="<em>Prâgma</em> (πρᾶγμα) means <strong>a thing done, a matter, an affair, a deed</strong>. It is related to <em>prassō</em> (to do, to practice) and broadly refers to any matter of concern — legal, practical, or moral. It appears numerous times in the NT.",
        usage="<em>Pragma</em> covers a wide range of NT contexts. In Matthew 18:19, 'if two of you on earth agree about anything they ask for' — <em>peri pantos pragmatos</em> — any matter at all. In Romans 16:2, Phoebe has 'been a great help to many people, including me' — <em>pragmati</em>. In 1 Corinthians 6:1, Paul rebukes Christians for taking their disputes (<em>pragmata</em>) before secular courts. In Hebrews 6:18, 'two unchangeable things' (<em>pragmatōn</em>) — God's promise and oath — are the anchor of our hope. The word also appears in Hebrews 11:1: 'faith is the substance of things hoped for, the evidence of <em>pragmatōn</em> (things) not seen.' <strong>Faith is the conviction about unseen realities</strong> — the greatest 'matters' are often invisible.",
        verses=[
            ("Hebrews 11:1", "Now faith is confidence in what we hope for and assurance about what we do not see (<em>pragma</em>)."),
            ("1 Corinthians 6:1", "If any of you has a dispute with another, do you dare to take it before the ungodly for judgment instead of before the Lord's people?"),
            ("Hebrews 6:18", "...so that by two unchangeable things in which it is impossible for God to lie, we who have fled to take hold of the hope set before us may be greatly encouraged."),
        ],
        related=[("G2041", "Ergon — Work/Deed"), ("G4238", "Prassō — To Do/Practice"), ("G1319", "Didaskalia — Teaching/Doctrine")],
    ),
    dict(
        id="G3468", lang="G", word="μώλωψ", trans="mṓlōps", pos="Noun, masculine",
        gloss="Bruise, Stripe, Weal",
        og_desc="Mōlōps — the stripes of Christ by which we are healed. Strong's G3468.",
        defn="<em>Mṓlōps</em> (μώλωψ) means <strong>a bruise, weal, or stripe</strong> left by a blow or flogging. It refers to the mark left on skin after being struck — the raised, discolored injury from a lash or rod. The word appears once in the NT and is of enormous theological significance.",
        usage="First Peter 2:24 quotes Isaiah 53:5: 'He himself bore our sins in his body on the cross, so that we might die to sins and live for righteousness; by his <em>wounds</em> (<em>mōlōpi</em>) you have been healed.' The singular <em>mōlōpi</em> (by his bruise/stripe) is a collective — the totality of the wounds Christ bore in His flogging and crucifixion. Isaiah 53 was written 700 years before the crucifixion, yet describes it with astonishing precision: the suffering Servant crushed for our iniquities. Peter applies this directly to Christian suffering: the one who bore stripes without retaliation is the pattern for slaves and all believers who suffer unjustly. <strong>Christ's wounds are our healing</strong> — His pain purchased our peace.",
        verses=[
            ("1 Peter 2:24", "He himself bore our sins in his body on the cross... by his <em>wounds</em> you have been healed."),
            ("Isaiah 53:5", "But he was pierced for our transgressions, he was crushed for our iniquities; the punishment that brought us peace was on him, and by his wounds we are healed."),
            ("Isaiah 53:7", "He was oppressed and afflicted, yet he did not open his mouth; he was led like a lamb to the slaughter."),
        ],
        related=[("G3817", "Paiō — To Strike"), ("G2386", "Iama — Healing"), ("G629", "Apolytrōsis — Redemption")],
    ),
    dict(
        id="G5285", lang="G", word="ὑποπνέω", trans="hypopnéō", pos="Verb",
        gloss="To Blow Gently, To Blow Softly",
        og_desc="Hypopnéō — a soft south wind that gave false hope before the storm. Strong's G5285.",
        defn="<em>Hypopnéō</em> (ὑποπνέω) means <strong>to blow gently, to blow softly</strong> — a light, favorable wind. From <em>hypo</em> (under, gently) + <em>pneō</em> (to blow). It appears once in Acts in the shipwreck narrative.",
        usage="Acts 27:13 records that 'when a gentle south wind began to blow (<em>hypopneusantos notou</em>), they thought they had obtained what they wanted; so they weighed anchor and sailed along the shore of Crete.' This gentle, favorable wind gave the sailors false confidence — they proceeded despite Paul's warning (v.10). Then the northeaster struck. The <em>hypopnéō</em> is a cautionary symbol: <strong>favorable circumstances are not always God's green light.</strong> Smooth sailing can deceive us into ignoring wise counsel. The disciples' decision to trust the gentle wind over Paul's Spirit-guided warning led to catastrophe. Yet even that catastrophe was in God's providence — it led Paul to Rome as God had promised (v.24). Even our mistakes cannot thwart God's plan.",
        verses=[
            ("Acts 27:13", "When a <em>gentle south wind</em> began to blow, they thought they had obtained what they wanted; so they weighed anchor and sailed along the shore of Crete."),
            ("Acts 27:14", "Before very long, a wind of hurricane force, called the Northeaster, swept down from the island."),
            ("Proverbs 3:5-6", "Trust in the LORD with all your heart and lean not on your own understanding; in all your ways submit to him."),
        ],
        related=[("G417", "Anemos — Wind"), ("G4157", "Pnoē — Breath/Wind"), ("G3558", "Notos — South Wind")],
    ),
    dict(
        id="G4237", lang="G", word="πρασιά", trans="prasiá", pos="Noun, feminine",
        gloss="Garden Plot, Group Seated in Rows",
        og_desc="Prasiá — the groups seated in rows like garden beds; the feeding of the 5,000. Strong's G4237.",
        defn="<em>Prasiá</em> (πρασιά) literally means a <strong>garden bed or plot</strong> — a rectangular section of a garden where plants grow in rows. In the NT it is used metaphorically for groups of people seated in organized rows, like garden beds. It appears only in Mark's account of the feeding of the 5,000.",
        usage="Mark 6:40 records a memorable detail: the crowd sat down in groups of hundreds and fifties — <em>prasiái prasiái</em> (literally 'garden-plot by garden-plot'). This seemingly minor detail reveals Mark's eyewitness precision (likely from Peter) but also carries theological resonance. The orderly, organized feeding of 5,000 on a hillside echoes the <strong>Exodus feeding of Israel in the wilderness</strong> (Psalm 78:19: 'Can God spread a table in the wilderness?'). Jesus is the new Moses, the good Shepherd who 'makes me lie down in green pastures' (Psalm 23:2). The organized rows suggest God's abundant provision is not chaotic — it is ordered, sufficient, and personal. No one in the <em>prasia</em> was overlooked.",
        verses=[
            ("Mark 6:40", "So they sat down in groups of hundreds and fifties — like <em>garden plots</em>."),
            ("Mark 6:41-42", "Taking the five loaves and the two fish and looking up to heaven, he gave thanks and broke the loaves... They all ate and were satisfied."),
            ("Psalm 23:2", "He makes me lie down in green pastures, he leads me beside quiet waters."),
        ],
        related=[("G2828", "Klisia — A Group Reclining"), ("G740", "Artos — Bread"), ("G5046", "Teleios — Complete/Perfect")],
    ),
    dict(
        id="G4063", lang="G", word="περιτρέχω", trans="peritréchō", pos="Verb",
        gloss="To Run Through, To Run Around",
        og_desc="Peritréchō — people ran through villages to bring the sick to Jesus. Strong's G4063.",
        defn="<em>Peritréchō</em> (περιτρέχω) means <strong>to run through, to run around, to hasten about</strong> a region or area. It combines <em>peri</em> (around, through) + <em>trechō</em> (to run). It appears once in the NT, depicting urgent movement.",
        usage="Mark 6:55 records that when Jesus arrived at Gennesaret, the people 'ran throughout that whole region and carried the sick on mats to wherever they heard he was.' The verb <em>peritrechō</em> captures the urgency and widespread response to Jesus' presence — people <strong>ran</strong> to bring the sick to Him. This is a picture of the desperate faith of those who recognized their need. They didn't send a polite invitation; they ran. They didn't wait for the sick to self-present; they carried them. The response to Jesus should be characterized by urgency, not complacency. This passage, combined with Jesus' healings of all who came (v.56), reveals the infinite compassion and power of Christ — no case too hard, no person beyond reach.",
        verses=[
            ("Mark 6:55", "They <em>ran throughout that whole region</em> and carried the sick on mats to wherever they heard he was."),
            ("Mark 6:56", "And wherever he went — into villages, towns or countryside — they placed the sick in the marketplaces."),
            ("Matthew 4:24", "News about him spread all over Syria, and people brought to him all who were ill with various diseases."),
        ],
        related=[("G5143", "Trechō — To Run"), ("G2390", "Iaomai — To Heal"), ("G2569", "Kalopoeō — To Do Good")],
    ),
    dict(
        id="G5295", lang="G", word="ὑπολείπω", trans="hypoleípō", pos="Verb",
        gloss="To Leave Behind, To Leave Remaining",
        og_desc="Hypoleípō — the remnant left behind; God always preserves a faithful few. Strong's G5295.",
        defn="<em>Hypoleípō</em> (ὑπολείπω) means <strong>to leave behind, to leave remaining</strong>. It signifies what is left over after a reduction — a remnant. The word appears once in the NT in Paul's quotation from 1 Kings 19.",
        usage="Romans 11:3 quotes Elijah's despairing prayer: 'LORD, they have killed your prophets and torn down your altars; I am the only one left (<em>hypeleiphthēn monos egō</em>).' Elijah believed he was the last faithful Israelite. But God corrects him: 'I have reserved for myself seven thousand who have not bowed the knee to Baal' (v.4). Paul uses this to argue that Israel has not been entirely rejected — there is always a <strong>remnant</strong> according to God's grace. This is one of Scripture's great encouragements for those in spiritual isolation: you are never actually alone. Even when faithfulness seems extinct, God always preserves His people. The remnant doctrine runs from Noah through Elijah through the exile through Christ through the church — God always keeps a faithful seed.",
        verses=[
            ("Romans 11:3-4", "Lord, they have killed your prophets... I am the only one left. And what was God's answer? I have reserved for myself seven thousand who have not bowed the knee to Baal."),
            ("1 Kings 19:10", "I am the only one left, and now they are trying to kill me too."),
            ("Isaiah 10:22", "Though your people be like the sand by the sea, Israel, only a remnant will return."),
        ],
        related=[("G3005", "Leimma — Remnant"), ("G2645", "Kataloipos — The Rest/Remnant"), ("G1588", "Eklektos — Chosen")],
    ),
    dict(
        id="G4829", lang="G", word="συμμερίζομαι", trans="symmerízomai", pos="Verb",
        gloss="To Share In, To Partake Together",
        og_desc="Symmerízomai — sharing in the ministry of the gospel together. Strong's G4829.",
        defn="<em>Symmerízomai</em> (συμμερίζομαι) means <strong>to share in something together, to partake jointly, to have a common portion</strong>. From <em>syn</em> (together) + <em>merizō</em> (to divide, to share). It appears once in Paul's letter to the Corinthians.",
        usage="First Corinthians 9:13 uses the concept in Paul's discussion of financial support for ministry: those who serve at the altar <em>share in</em> what is offered on the altar. Paul's broader argument is that those who preach the gospel should receive their living from the gospel (v.14) — yet he voluntarily waives this right. The word <em>symmerizō</em> captures the principle of <strong>mutual participation</strong>: ministry creates community of sharing. Those who receive spiritual blessing have a responsibility to share material blessing with those who labored for them (Romans 15:27; Galatians 6:6). The early church took this seriously — financial generosity toward ministers and the poor was evidence of genuine community.",
        verses=[
            ("1 Corinthians 9:13", "Don't you know that those who serve in the temple get their food from the temple, and that those who serve at the altar <em>share in</em> what is offered on the altar?"),
            ("Galatians 6:6", "Nevertheless, the one who receives instruction in the word should share all good things with their instructor."),
            ("Romans 15:27", "They were pleased to do it, and indeed they owe it to them. For if the Gentiles have shared in the Jews' spiritual blessings, they owe it to the Jews to share with them their material blessings."),
        ],
        related=[("G2841", "Koinōneō — To Share/Participate"), ("G2842", "Koinōnia — Fellowship"), ("G3307", "Merizō — To Divide/Share")],
    ),
    dict(
        id="G3380", lang="G", word="μήπω", trans="mḗpō", pos="Adverb",
        gloss="Not Yet",
        og_desc="Mēpō — not yet; God's patience and perfect timing in redemptive history. Strong's G3380.",
        defn="<em>Mḗpō</em> (μήπω) means <strong>not yet</strong> — indicating something that has not yet occurred but is anticipated or expected. It is a compound of <em>mē</em> (not) + <em>pō</em> (yet). It appears several times in the NT, often in theologically significant contexts.",
        usage="Romans 9:11 uses <em>mēpō</em> to make a crucial point about divine election: 'Yet, before the twins were born or had done anything good or bad — in order that God's purpose in election might stand: not by works but by him who calls — she was told, "The older will serve the younger."' The key is <em>mēpō</em>: 'not yet having done anything.' God's choice of Jacob over Esau was made before either had done anything — demonstrating that election is <strong>entirely by grace, not merit</strong>. This 'not yet' is one of the strongest statements of sovereign grace in all Scripture. Similarly, Hebrews 12:4 ('You have not yet resisted to the point of shedding your blood') uses <em>mēpō</em> to encourage perseverance in suffering.",
        verses=[
            ("Romans 9:11", "Yet, before the twins were born or had done anything good or bad — in order that God's purpose in election might stand..."),
            ("Hebrews 12:4", "In your struggle against sin, you have <em>not yet</em> resisted to the point of shedding your blood."),
            ("John 7:39", "By this he meant the Spirit, whom those who believed in him were later to receive. Up to that time the Spirit had <em>not yet</em> been given."),
        ],
        related=[("G3768", "Oupō — Not Yet (indicative)"), ("G3761", "Oude — Not Even"), ("G4309", "Proorizō — To Predestine")],
    ),
    dict(
        id="G2713", lang="G", word="κατέναντι", trans="katenanti", pos="Preposition/Adverb",
        gloss="Opposite, Over Against, In the Presence of",
        og_desc="Katenanti — in the presence of God; Abraham's faith before the all-seeing God. Strong's G2713.",
        defn="<em>Katenanti</em> (κατέναντι) means <strong>opposite, over against, in front of, in the presence of</strong>. A strengthened form of <em>enanti</em> (before, opposite). It appears in several NT contexts, both geographical and theological.",
        usage="The most theologically weighty use of <em>katenanti</em> is Romans 4:17: 'He is our father in the sight of God, in whom he believed — the God who gives life to the dead and calls into being things that did not exist.' Abraham had faith '<em>katenanti</em> God' — in His very presence, before His face. This preposition intensifies Abraham's faith: it was not merely theoretical belief but <strong>faith exercised in direct relationship with God Himself</strong>, who sees all and knows all. God's omniscience means our faith is never private — it is always before His face. This also appears in Mark 11:2 (village over against you) and Luke 19:30 (village ahead of you), showing the word's range from spatial to relational usage.",
        verses=[
            ("Romans 4:17", "As it is written: 'I have made you a father of many nations.' He is our father in the sight of God (<em>katenanti</em>), in whom he believed."),
            ("2 Corinthians 2:17", "Unlike so many, we do not peddle the word of God for profit. On the contrary, in Christ we speak before God with sincerity, as those sent from God."),
            ("Hebrews 4:13", "Nothing in all creation is hidden from God's sight. Everything is uncovered and laid bare before the eyes of him to whom we must give account."),
        ],
        related=[("G1799", "Enōpion — Before/In the Presence of"), ("G561", "Apenanti — Over Against"), ("G4383", "Prosōpon — Face/Presence")],
    ),
    dict(
        id="G3698", lang="G", word="ὁπότε", trans="hopóte", pos="Conjunction",
        gloss="When, Whenever",
        og_desc="Hopóte — whenever; the appointed times in God's sovereign plan. Strong's G3698.",
        defn="<em>Hopóte</em> (ὁπότε) is a temporal conjunction meaning <strong>when, at which time, whenever</strong>. It combines the relative pronoun <em>ho</em> with <em>pote</em> (at some time, ever). It appears rarely in the NT but is common in classical Greek.",
        usage="The word appears in Luke 6:3 where Jesus asks, 'Have you never read what David did when (<em>hopóte</em>) he and his companions were hungry?' Jesus uses this historical moment to establish a principle: human need can take precedence over ceremonial law when rightly understood. The Sabbath was made for man, not man for the Sabbath. <em>Hopóte</em> marks a moment of necessity that revealed a principle of mercy. Throughout Scripture, <strong>God's timing is sovereign</strong>: 'But when the set time (<em>to plērōma tou chronou</em>) had fully come, God sent his Son' (Galatians 4:4). Every 'when' in redemptive history is appointed by God.",
        verses=[
            ("Luke 6:3", "Jesus answered them, 'Have you never read what David did <em>when</em> he and his companions were hungry?'"),
            ("Galatians 4:4", "But when the set time had fully come, God sent his Son, born of a woman, born under the law."),
            ("Ecclesiastes 3:1", "There is a time for everything, and a season for every activity under the heavens."),
        ],
        related=[("G3753", "Hote — When"), ("G3752", "Hotan — Whenever"), ("G2540", "Kairos — Appointed Time")],
    ),
    dict(
        id="G3389", lang="G", word="μητραλώας", trans="mētralṓias", pos="Noun, masculine",
        gloss="One Who Strikes His Mother, Matricide",
        og_desc="Mētralōias — striking one's mother; the lawless condemned by the gospel. Strong's G3389.",
        defn="<em>Mētralṓias</em> (μητραλώας) means <strong>one who strikes or kills his mother</strong> — a matricide or mother-abuser. From <em>mētēr</em> (mother) + <em>aloiáō</em> (to strike, beat). It appears in Paul's vice list in 1 Timothy 1, a catalog of the most extreme moral violations.",
        usage="First Timothy 1:9-10 lists those for whom the law was made: 'the lawless and rebellious, the ungodly and sinful, the unholy and irreligious, those who kill their fathers or mothers (<em>mētralōiais</em>), murderers...' The list escalates from general to specific, from spiritual to relational to violent. Striking or killing a mother represented the ultimate violation of family honor and natural law. <strong>The law exposes sin in its most naked form.</strong> Paul's point is not that believers commit these sins but that the law is designed to restrain and convict sinners — driving them to the gospel of grace. No sin is beyond the reach of Christ's redemption: 'where sin increased, grace increased all the more' (Romans 5:20). Paul himself was once 'the worst of sinners' (1 Timothy 1:15-16) and received mercy.",
        verses=[
            ("1 Timothy 1:9-10", "We also know that the law is made not for the righteous but for lawbreakers and rebels, the ungodly and sinful... for those who kill their fathers or <em>mothers</em>, for murderers..."),
            ("Ephesians 6:2", "Honor your father and mother — which is the first commandment with a promise."),
            ("Romans 5:20", "But where sin increased, grace increased all the more."),
        ],
        related=[("G3389b", "Patralōias — Father-Striker"), ("G5406", "Phoneus — Murderer"), ("G3551", "Nomos — Law")],
    ),
    dict(
        id="G4025", lang="G", word="περίθεσις", trans="períthesis", pos="Noun, feminine",
        gloss="Wearing, Putting On (Adornment)",
        og_desc="Períthesis — the wearing of outward adornment; true beauty is inward. Strong's G4025.",
        defn="<em>Períthesis</em> (περίθεσις) means <strong>the act of wearing or putting on</strong> — specifically of adornment, the placing of decorative items on oneself. From <em>peritithēmi</em> (to place around). It appears once in 1 Peter in a teaching on inner vs. outer beauty.",
        usage="First Peter 3:3-4 instructs wives: 'Your beauty should not come from outward adornment (<em>peritheseōs</em>), such as elaborate hairstyles and the wearing of gold jewelry or fine clothes. Rather, it should be that of your inner self, the unfading beauty of a gentle and quiet spirit, which is of great worth in God's sight.' Peter is not banning all jewelry or styling — he is establishing a <strong>hierarchy of beauty</strong>. External adornment is temporary and fading; inner character is of 'great worth in God's sight' and 'unfading.' This principle applies beyond gender: all believers are called to prioritize character over appearance, integrity over impression management. God looks at the heart (1 Samuel 16:7), and so should we.",
        verses=[
            ("1 Peter 3:3-4", "Your beauty should not come from outward adornment (<em>peritheseōs</em>), such as elaborate hairstyles... Rather, it should be that of your inner self, the unfading beauty of a gentle and quiet spirit."),
            ("1 Samuel 16:7", "The LORD does not look at the things people look at. People look at the outward appearance, but the LORD looks at the heart."),
            ("Proverbs 31:30", "Charm is deceptive, and beauty is fleeting; but a woman who fears the LORD is to be praised."),
        ],
        related=[("G4016", "Periballō — To Clothe"), ("G2889", "Kosmos — Adornment/World"), ("G4239", "Prays — Gentle/Humble")],
    ),
    # ── HEBREW ──
    dict(
        id="H7915", lang="H", word="שַׂכִּין", trans="sakkîyn", pos="Noun, masculine",
        gloss="Knife",
        og_desc="Sakkîyn — the knife; the instrument of sacrifice and the table. Strong's H7915.",
        defn="<em>Sakkîyn</em> (שַׂכִּין) means <strong>knife, blade</strong> — a cutting instrument. It appears only once in the Hebrew Bible, making it a <em>hapax legomenon</em>. The word may be related to Aramaic and Syriac cognates meaning knife.",
        usage="Proverbs 23:2 uses <em>sakkîyn</em> in a counsel about table manners and self-control: 'And put a knife to your throat if you are given to gluttony.' The image is vivid and extreme — self-mastery so radical it is like restraining yourself at knifepoint. The broader context (v.1-3) warns about dining with rulers and being deceived by delicacies. <strong>Self-control is a spiritual discipline</strong>, especially in the area of appetite. This connects to the NT's call to 'crucify the flesh with its passions and desires' (Galatians 5:24). The knife as symbol of restraint precedes Paul's armor metaphors — both call for intentional, even violent resistance to ungodly impulses.",
        verses=[
            ("Proverbs 23:2", "Put a <em>knife</em> to your throat if you are given to gluttony."),
            ("Proverbs 23:1", "When you sit to dine with a ruler, note well what is before you."),
            ("Galatians 5:24", "Those who belong to Christ Jesus have crucified the flesh with its passions and desires."),
        ],
        related=[("H2719", "Chereb — Sword"), ("H3979", "Ma'akelet — Slaughtering Knife"), ("H6310", "Peh — Mouth")],
    ),
    dict(
        id="H7811", lang="H", word="שָׂחָה", trans="sāchāh", pos="Verb",
        gloss="To Swim",
        og_desc="Sāchāh — to swim; overwhelmed by tears, swimming in grief. Strong's H7811.",
        defn="<em>Sāchāh</em> (שָׂחָה) means <strong>to swim</strong> — to move through water by swimming. The word is rare in the Hebrew Bible and may also carry the sense of being overwhelmed or inundated.",
        usage="Isaiah 25:11 uses a remarkable swimming metaphor: 'They will spread out their hands in it, as a swimmer spreads out his hands to swim. God will bring down their pride despite the cleverness of their hands.' The context is God's judgment on Moab — the proud nation will be brought low, helplessly flailing like a swimmer in deep water. The image is simultaneously powerful and humbling. <strong>Pride makes us think we can swim in any depth;</strong> God reminds us that He controls the waters. Psalm 6:6 uses a related concept: 'I drench my couch with tears' — overwhelmed like one drowning in sorrow. Both passages remind us that God sees those who are overwhelmed, whether by pride or by tears.",
        verses=[
            ("Isaiah 25:11", "They will spread out their hands in it, as a <em>swimmer</em> spreads out his hands to swim. God will bring down their pride."),
            ("Psalm 6:6", "I am worn out from my groaning. All night long I flood my bed with weeping and drench my couch with tears."),
            ("Ezekiel 47:5", "He measured off another thousand, but now it was a river that I could not cross, because the water had risen and was deep enough to swim in."),
        ],
        related=[("H4325", "Mayim — Water"), ("H7857", "Shataph — To Overflow/Flood"), ("H1344", "Ge'ah — Pride")],
    ),
    dict(
        id="H5138", lang="H", word="נָזִיד", trans="nāzîd", pos="Noun, masculine",
        gloss="Boiled Pottage, Stew",
        og_desc="Nāzîd — the pottage for which Esau sold his birthright. Strong's H5138.",
        defn="<em>Nāzîd</em> (נָזִיד) means <strong>boiled pottage, stew</strong> — a thick, cooked dish made from lentils or other legumes. The word comes from <em>zud</em> (to boil, to seethe). It appears primarily in Genesis and 2 Kings.",
        usage="The most famous use of <em>nāzîd</em> is Genesis 25:29-34: Esau comes in famished from the field and sells his birthright to Jacob for a bowl of red lentil stew (<em>nazid</em>). Hebrews 12:16-17 cites this as a warning: 'See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son.' <strong>The pottage represents immediate, physical gratification traded for eternal, spiritual inheritance.</strong> Esau's 'I am about to die' (v.32) was hyperbole — he was hungry, not dying. Yet he treated an eternal blessing as worthless for a momentary meal. The warning is perpetually relevant: don't trade your heavenly inheritance for earthly satisfactions. In 2 Kings 4:38-40, Elisha miraculously heals a pot of poisoned stew — the <em>nāzîd</em> that brought death becomes nourishing.",
        verses=[
            ("Genesis 25:34", "Then Jacob gave Esau some bread and some lentil <em>stew</em>. He ate and drank, and then got up and left. So Esau despised his birthright."),
            ("Hebrews 12:16", "See that no one is sexually immoral, or is godless like Esau, who for a single meal sold his inheritance rights as the oldest son."),
            ("2 Kings 4:40-41", "'There is death in the pot!' And they could not eat it. But he said, 'Get some flour.' He put it into the pot and said, 'Serve it to the people to eat.' And there was nothing harmful in the pot."),
        ],
        related=[("H6521", "Paru'ach — Lentil/Pot Herb"), ("H1060", "Bekorah — Birthright"), ("H5921", "Al — Upon, Concerning")],
    ),
    dict(
        id="H3365", lang="H", word="יָקַר", trans="yāqar", pos="Verb",
        gloss="To Be Precious, To Be Prized, To Be Rare",
        og_desc="Yāqar — to be precious; the preciousness of God's word and faithful love. Strong's H3365.",
        defn="<em>Yāqar</em> (יָקַר) means <strong>to be precious, to be prized, to be of great value, to be rare</strong>. It can also mean to be honored or esteemed. The related noun <em>yaqar</em> means preciousness, costliness, or honor.",
        usage="<em>Yāqar</em> appears in some of Scripture's most beautiful expressions of value and worth. Psalm 116:15: 'Precious (<em>yaqar</em>) in the sight of the LORD is the death of his faithful servants' — God places infinite value on the lives of His people. Psalm