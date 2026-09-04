#!/usr/bin/env python3
"""Generate 89 more Greek lexicon HTML entries - batch 2."""

import os
import glob

LEXICON_DIR = "/Users/adamjohns/bible-reading-plan-bot/docs/lexicon"

# Find existing entries
existing = set()
for f in glob.glob(os.path.join(LEXICON_DIR, "G*.html")):
    basename = os.path.basename(f)
    numstr = basename.replace(".html", "").lstrip("G")
    try:
        num = int(numstr)
        existing.add(num)
    except ValueError:
        continue

print(f"Found {len(existing)} existing Greek entries")

def make_html(num, greek, translit, pos, gloss, definition, theological, verses, related):
    og_desc = definition[:120].replace('"', '&quot;').replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')
    meta_desc = f"{translit} — {gloss} — Greek word study. Strong's G{num}. USMC Ministries Greek &amp; Hebrew Lexicon."
    verses_html = ""
    for ref, text in verses:
        verses_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={ref}" class="verse-ref">{ref.replace('+', ' ')}</a>
                    <span class="verse-text">{text}</span>
                </div>"""
    related_html = ""
    for rnum, rlabel in related:
        related_html += f"""
                    <a href="G{rnum}.html" class="related-word">G{rnum} — {rlabel}</a>"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="G{num} — {translit} | USMC Ministries Lexicon">
    <meta property="og:description" content="{og_desc}">
    <meta name="description" content="{meta_desc}">
    <title>G{num} — {translit} ({gloss}) | USMC Ministries Lexicon</title>
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
    .theme-toggle{{background:none;border:1px solid var(--border);border-radius:50%;width:34px;height:34px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.1rem;transition:all 0.3s;padding:0;margin-left:6px;}}.theme-toggle:hover{{border-color:var(--gold);transform:scale(1.1);}}body.light-mode{{--bg-dark:#FAF8F5;--bg-card:#FFF;--white:#1a1a1a;--gray:#666;--border:#d4d0c8;background:#FAF8F5;color:#1a1a1a;}}body.light-mode nav{{background:rgba(250,248,245,0.97);}}body.light-mode .section{{background:#fff;border-color:#d4d0c8;}}body.light-mode .ext-link{{border-color:#d4d0c8;}}body.light-mode .related-word{{background:rgba(212,175,55,0.08);border-color:#d4d0c8;}}body.light-mode footer{{border-top-color:#d4d0c8;}}</style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
</div>
        <span style="width:18px;text-align:center;">&#9728;&#65039;</span>
    </div>
    <div class="container">
        <a href="../lexicon.html" class="back-link">&larr; Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">G{num} &middot; Greek &middot; New Testament</span>
            <div class="original-word">{greek}</div>
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
            <p>{theological}</p>
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
                <a href="https://www.stepbible.org/?q=strong=G{num}" target="_blank" class="ext-link">&#128214; STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/g{num}/kjv/tr/0-1/" target="_blank" class="ext-link">&#128216; Blue Letter Bible</a>
                <a href="https://biblehub.com/greek/{num}.htm" target="_blank" class="ext-link">&#128215; Bible Hub (Interlinear + HELPS)</a>
            </div>
        </div>
    </div>
    <div style="text-align:center;margin:24px auto 10px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="display:inline-flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
            <span style="width:18px;text-align:center;">&#127769;</span>
            <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
            <span style="width:18px;text-align:center;">&#9728;&#65039;</span>
        </div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">&copy; 2026 <a href="../index.html">U.S.M.C. Ministries</a> &middot; <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
<script>function bteToggleTheme(){{var b=document.body;if(b.classList.contains("light-mode")){{b.classList.remove("light-mode");localStorage.setItem("bte-theme","dark");}}else{{b.classList.add("light-mode");localStorage.setItem("bte-theme","light");}}}};(function(){{if(localStorage.getItem("bte-theme")==="light"){{document.body.classList.add("light-mode");}}}})();</script></body>
</html>'''

# 89 more entries focused on gaps in 4026-4099 and 4105-4200 ranges
entries = [
    (4026, "Περιισταμαι", "Periistami", "Verb (Middle)", "To Stand Around / To Avoid",
     "Middle voice of <em>periistēmi</em>. To stand around or to avoid. Paul advises avoiding foolish disputes.",
     "Wisdom includes knowing what battles to fight and what to <em>avoid</em>. Not every controversy is worth engaging. <strong>Discernment means choosing silence when speech would only produce strife.</strong>",
     [("Titus+3:9","But <em>avoid</em> foolish controversies and genealogies and arguments about the law."),("2+Timothy+2:16","<em>Avoid</em> godless chatter, because those who indulge in it will become more and more ungodly."),("2+Timothy+2:23","Don't have anything to do with foolish and stupid arguments, because you know they produce quarrels."),("Proverbs+17:14","Starting a quarrel is like breaching a dam; so drop the matter before a dispute breaks out."),("Romans+16:17","I urge you, brothers and sisters, to watch out for those who cause divisions.")],
     [(4025,"Periistēmi (To Avoid)"),(4678,"Sophia (Wisdom)"),(3474,"Mōros (Foolish)"),(1515,"Eirēnē (Peace)")]),
    (4028, "Περικαλυπτω", "Perikaluptō", "Verb", "To Cover Around / To Blindfold / To Overlay",
     "From <em>peri</em> (around) and <em>kaluptō</em> (to cover). To cover all around, to blindfold, to overlay completely. Used of blindfolding Jesus during His trial.",
     "The soldiers <em>blindfolded</em> Jesus and demanded He prophesy who struck Him (Luke 22:64). The irony is devastating: they blindfolded the One who sees all things, mocked the gift of prophecy before the greatest Prophet. <strong>Human attempts to hide from God's sight are futile.</strong>",
     [("Luke+22:64","They <em>blindfolded</em> him and demanded, 'Prophesy! Who hit you?'"),("Mark+14:65","Then some began to spit at him; they <em>blindfolded</em> him, struck him with their fists."),("Hebrews+9:4","Which had the golden altar of incense and the gold-covered ark of the covenant."),("2+Corinthians+4:3","And even if our gospel is veiled, it is veiled to those who are perishing."),("Isaiah+6:10","Make the heart of this people calloused; make their ears dull and close their eyes.")],
     [(2572,"Kaluptō (To Cover)"),(5185,"Tuphlos (Blind)"),(4396,"Prophētēs (Prophet)"),(3708,"Horaō (To See)")]),
    (4029, "Περικειμαι", "Perikeimai", "Verb", "To Lie Around / To Be Surrounded / To Wear",
     "From <em>peri</em> (around) and <em>keimai</em> (to lie). To be placed around, to be surrounded by, to wear. Used of the great cloud of witnesses surrounding believers.",
     "Hebrews 12:1 declares that believers are '<em>surrounded</em> by such a great cloud of witnesses.' This imagery of faithful saints from Hebrews 11 surrounding the present-day church is meant to <strong>inspire perseverance</strong>. We do not run the race alone.",
     [("Hebrews+12:1","Therefore, since we are <em>surrounded</em> by such a great cloud of witnesses, let us throw off everything that hinders."),("Acts+28:20","It is because of the hope of Israel that I am bound with this <em>chain</em>."),("Mark+9:42","If anyone causes one of these little ones to sin, it would be better for them if a large millstone were <em>hung around</em> their neck."),("Hebrews+5:2","He is able to deal gently with those who are ignorant and are going astray, since he himself is beset by weakness."),("Hebrews+11:39","These were all commended for their faith, yet none of them received what had been promised.")],
     [(2749,"Keimai (To Lie)"),(3144,"Martus (Witness)"),(5281,"Hupomonē (Endurance)"),(4102,"Pistis (Faith)")]),
    (4030, "Περικεφαλαια", "Perikephalaia", "Noun, Feminine", "Helmet",
     "From <em>peri</em> (around) and <em>kephalē</em> (head). A helmet — armor for the head. Paul identifies it as the 'helmet of salvation' in the spiritual armor.",
     "The <em>helmet</em> of salvation protects the mind — the primary battlefield of spiritual warfare. If the enemy can capture your thinking, he captures your life. The helmet reminds believers that their <strong>salvation is secure</strong>, guarding against doubt, despair, and deception that attack the mind.",
     [("Ephesians+6:17","Take the <em>helmet</em> of salvation and the sword of the Spirit, which is the word of God."),("1+Thessalonians+5:8","Since we belong to the day, let us be sober, putting on faith and love as a breastplate, and the hope of salvation as a <em>helmet</em>."),("Isaiah+59:17","He put on righteousness as his breastplate, and the <em>helmet</em> of salvation on his head."),("Romans+8:1","Therefore, there is now no condemnation for those who are in Christ Jesus."),("Philippians+4:7","And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.")],
     [(4991,"Sōtēria (Salvation)"),(2776,"Kephalē (Head)"),(3696,"Hoplon (Weapon)"),(2382,"Thōrax (Breastplate)")]),
    (4031, "Περικρατης", "Perikratēs", "Adjective", "Having Power Over / In Control",
     "From <em>peri</em> (over) and <em>kratos</em> (strength/power). Having mastery over, being in control of. Used in Acts 27:16 of barely being able to secure the lifeboat during a storm.",
     "During the shipwreck in Acts 27, the sailors could barely gain <em>control</em> of the lifeboat (Acts 27:16). This vivid detail illustrates that in life's storms, human control is fragile. <strong>Only God maintains sovereign control</strong> when human strength fails.",
     [("Acts+27:16","As we passed to the lee of a small island called Cauda, we were hardly able to make the lifeboat <em>secure</em>."),("Acts+27:20","When neither sun nor stars appeared for many days and the storm continued raging, we finally gave up all hope."),("Acts+27:25","So keep up your courage, men, for I have faith in God that it will happen just as he told me."),("Psalm+107:29","He stilled the storm to a whisper; the waves of the sea were hushed."),("Mark+4:39","He got up, rebuked the wind and said to the waves, 'Quiet! Be still!' Then the wind died down.")],
     [(2904,"Kratos (Power)"),(2316,"Theos (God)"),(4102,"Pistis (Faith)"),(4982,"Sōzō (To Save)")]),
    (4032, "Περικρυβω", "Perikrubō", "Verb", "To Conceal Completely / To Hide",
     "From <em>peri</em> (completely) and <em>krubō</em> (to hide). To hide completely, to conceal entirely. Elizabeth <em>hid</em> herself for five months after conceiving John the Baptist.",
     "Elizabeth '<em>hid</em> herself for five months' (Luke 1:24) after miraculously conceiving John the Baptist. This period of seclusion suggests quiet reflection on God's miraculous work before public disclosure. <strong>Some of God's greatest works begin in hiddenness</strong> — seeds grow underground before breaking the surface.",
     [("Luke+1:24","After this his wife Elizabeth became pregnant and for five months <em>remained in seclusion</em>."),("Luke+1:25","The Lord has done this for me. In these days he has shown his favor and taken away my disgrace."),("Colossians+3:3","For you died, and your life is now <em>hidden</em> with Christ in God."),("Psalm+91:1","Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty."),("Isaiah+49:2","He made my mouth like a sharpened sword, in the shadow of his hand he <em>hid</em> me.")],
     [(2928,"Kruptō (To Hide)"),(2927,"Kruptos (Hidden)"),(4102,"Pistis (Faith)"),(5485,"Charis (Grace)")]),
    (4033, "Περικυκλοω", "Perikukloō", "Verb", "To Surround / To Encircle",
     "From <em>peri</em> (around) and <em>kukloō</em> (to circle). To encircle completely, to surround on every side. Jesus prophesied that enemies would <em>surround</em> Jerusalem.",
     "Jesus wept over Jerusalem and prophesied: 'Your enemies will build an embankment against you and <em>encircle</em> you and hem you in on every side' (Luke 19:43). This was fulfilled in AD 70 when Roman armies <em>surrounded</em> Jerusalem. <strong>Rejected grace leads to judgment.</strong>",
     [("Luke+19:43","The days will come upon you when your enemies will build an embankment against you and <em>encircle</em> you."),("Luke+19:44","They will dash you to the ground, you and the children within your walls."),("Luke+21:20","When you see Jerusalem being <em>surrounded</em> by armies, you will know that its desolation is near."),("Matthew+23:37","Jerusalem, Jerusalem, you who kill the prophets and stone those sent to you."),("Daniel+9:26","The people of the ruler who will come will destroy the city and the sanctuary.")],
     [(2944,"Kukloō (To Surround)"),(2419,"Hierousalēm (Jerusalem)"),(2920,"Krisis (Judgment)"),(4395,"Prophēteuō (To Prophesy)")]),
    (4034, "Περιλαμπω", "Perilampō", "Verb", "To Shine Around / To Illumine",
     "From <em>peri</em> (around) and <em>lampō</em> (to shine). To shine around, to illuminate from all sides. Used of the heavenly light at Jesus' birth announcement and Paul's conversion.",
     "The glory of the Lord '<em>shone around</em>' the shepherds at the birth announcement (Luke 2:9), and a light from heaven '<em>shone around</em>' Paul on the Damascus road (Acts 26:13). In both cases, divine light invaded darkness to deliver a life-changing message. <strong>God breaks into human darkness with blinding revelation.</strong>",
     [("Luke+2:9","An angel of the Lord appeared to them, and the glory of the Lord <em>shone around</em> them, and they were terrified."),("Acts+26:13","I saw a light from heaven, brighter than the sun, <em>blazing around</em> me and my companions."),("John+1:5","The light shines in the darkness, and the darkness has not overcome it."),("2+Corinthians+4:6","For God, who said, 'Let light shine out of darkness,' made his light shine in our hearts."),("Isaiah+60:1","Arise, shine, for your light has come, and the glory of the Lord rises upon you.")],
     [(2989,"Lampō (To Shine)"),(5457,"Phōs (Light)"),(1391,"Doxa (Glory)"),(32,"Angelos (Angel)")]),
    (4035, "Περιλειπω", "Perileipō", "Verb", "To Leave Remaining / To Survive",
     "From <em>peri</em> (around) and <em>leipō</em> (to leave). To leave around, to remain, to survive. Paul uses it of believers who are still alive at Christ's return.",
     "Paul assures the Thessalonians that those who are <em>still alive</em> at Christ's coming will not precede those who have died (1 Thessalonians 4:15, 17). The word guarantees that <strong>no believer is disadvantaged by timing</strong> — whether dead or alive at Christ's return, all will share in the resurrection glory.",
     [("1+Thessalonians+4:15","We who are still alive, who are <em>left</em> until the coming of the Lord, will certainly not precede those who have fallen asleep."),("1+Thessalonians+4:17","After that, we who are still alive and are <em>left</em> will be caught up together with them in the clouds."),("1+Corinthians+15:51","Listen, I tell you a mystery: We will not all sleep, but we will all be changed."),("Philippians+3:20","But our citizenship is in heaven. And we eagerly await a Savior from there."),("1+John+3:2","We know that when Christ appears, we shall be like him, for we shall see him as he is.")],
     [(3062,"Loipoi (Remaining)"),(386,"Anastasis (Resurrection)"),(3952,"Parousia (Coming)"),(2222,"Zōē (Life)")]),
    (4036, "Περιλυπος", "Perilupos", "Adjective", "Deeply Grieved / Very Sorrowful",
     "From <em>peri</em> (exceedingly) and <em>lupē</em> (grief). Extremely sorrowful, deeply grieved. Used of Jesus in Gethsemane — 'My soul is <em>overwhelmed with sorrow</em> to the point of death.'",
     "In Gethsemane, Jesus told His disciples: 'My soul is <em>overwhelmed with sorrow</em> to the point of death' (Matthew 26:38). This word reveals the full humanity of Christ — He experienced grief at its most extreme. The Son of God was not stoic but deeply emotional. <strong>Jesus' sorrow sanctifies our own grief</strong> and assures us He understands.",
     [("Matthew+26:38","Then he said to them, 'My soul is <em>overwhelmed with sorrow</em> to the point of death. Stay here and keep watch with me.'"),("Mark+14:34","'My soul is <em>overwhelmed with sorrow</em> to the point of death,' he said to them."),("Mark+6:26","The king was greatly <em>distressed</em>, but because of his oaths and his dinner guests, he did not want to refuse her."),("Luke+18:23","When he heard this, he became very <em>sad</em>, because he was very wealthy."),("Isaiah+53:3","He was despised and rejected by mankind, a man of suffering, and familiar with pain.")],
     [(3076,"Lupeō (To Grieve)"),(3077,"Lupē (Grief)"),(2424,"Iēsous (Jesus)"),(4716,"Stauros (Cross)")]),
    (4037, "Περιμενω", "Perimenō", "Verb", "To Wait For / To Await",
     "From <em>peri</em> (around, indicating completeness) and <em>menō</em> (to remain). To wait for with expectation, to await patiently. Jesus commanded the disciples to <em>wait for</em> the promise of the Father.",
     "Jesus' final pre-ascension command was to <em>wait for</em> the gift the Father had promised (Acts 1:4). Before the disciples could be sent out, they had to wait. Before power, patience. Before service, surrender. <strong>God's timing requires waiting, and waiting is not wasted time</strong> — it is preparation time.",
     [("Acts+1:4","On one occasion, while he was eating with them, he gave them this command: 'Do not leave Jerusalem, but <em>wait for</em> the gift my Father promised.'"),("Acts+1:8","But you will receive power when the Holy Spirit comes on you; and you will be my witnesses."),("Isaiah+40:31","But those who <em>wait</em> on the Lord will renew their strength."),("Psalm+27:14","<em>Wait</em> for the Lord; be strong and take heart and wait for the Lord."),("Lamentations+3:25","The Lord is good to those whose hope is in him, to the one who seeks him.")],
     [(3306,"Menō (To Remain)"),(4151,"Pneuma (Spirit)"),(1860,"Epangelia (Promise)"),(5281,"Hupomonē (Endurance)")]),
    (4038, "Περιξ", "Perix", "Adverb", "All Around / Round About",
     "An adverb meaning all around, round about, in every direction. Describes the surrounding area or the completeness of encirclement.",
     "God's presence is not directional — He is <em>all around</em> His people. The psalmist declares: 'As the mountains <em>surround</em> Jerusalem, so the Lord <em>surrounds</em> his people' (Psalm 125:2). Believers are not protected from one side only but are <strong>completely encircled by divine care</strong>.",
     [("Acts+5:16","Crowds gathered also from the towns <em>around</em> Jerusalem, bringing their sick and those tormented by impure spirits."),("Psalm+125:2","As the mountains <em>surround</em> Jerusalem, so the Lord <em>surrounds</em> his people both now and forevermore."),("2+Kings+6:17","And Elisha prayed, 'Open his eyes, Lord, so that he may see.' Then the Lord opened the servant's eyes, and he looked and saw the hills full of horses and chariots of fire <em>all around</em> Elisha."),("Psalm+34:7","The angel of the Lord encamps <em>around</em> those who fear him, and he delivers them."),("Revelation+4:6","In the center, <em>around</em> the throne, were four living creatures.")],
     [(2945,"Kuklō (Around)"),(4012,"Peri (About)"),(4060,"Peritithēmi (To Place Around)"),(3588,"Ho (The)")]),
    (4039, "Περιοικεω", "Perioikeō", "Verb", "To Dwell Around / To Be a Neighbor",
     "From <em>peri</em> (around) and <em>oikeō</em> (to dwell). To live in the neighborhood, to be a neighbor. Used of those who lived near Elizabeth and Zechariah.",
     "When Elizabeth gave birth to John, her <em>neighbors</em> and relatives rejoiced with her (Luke 1:58). The community witnessed God's faithfulness. <strong>God's blessings overflow to touch entire neighborhoods.</strong> The Christian life is not lived in isolation but in visible community.",
     [("Luke+1:58","Her <em>neighbors</em> and relatives heard that the Lord had shown her great mercy, and they shared her joy."),("Luke+1:65","All the <em>neighbors</em> were filled with awe, and throughout the hill country of Judea people were talking about all these things."),("Proverbs+27:10","Do not forsake your friend or a friend of your family, and do not go to your relative's house when disaster strikes you — better a <em>neighbor</em> nearby than a relative far away."),("Luke+10:36","Which of these three do you think was a <em>neighbor</em> to the man who fell into the hands of robbers?"),("Romans+13:10","Love does no harm to a <em>neighbor</em>. Therefore love is the fulfillment of the law.")],
     [(3611,"Oikeō (To Dwell)"),(4139,"Plēsion (Neighbor)"),(26,"Agapē (Love)"),(2842,"Koinōnia (Fellowship)")]),
    (4040, "Περιοικος", "Perioikos", "Noun/Adjective", "Neighbor / Dwelling Around",
     "From <em>peri</em> (around) and <em>oikos</em> (house). One who dwells nearby, a neighbor. The noun form of the concept of neighboring.",
     "The <em>neighbors</em> of Zechariah and Elizabeth became witnesses to God's miraculous work. Their proximity made them firsthand observers of divine faithfulness. <strong>God places believers strategically among neighbors</strong> so His works can be witnessed up close.",
     [("Luke+1:58","Her <em>neighbors</em> and relatives heard that the Lord had shown her great mercy."),("Luke+1:65","All the <em>neighbors</em> were filled with awe."),("Matthew+22:39","And the second is like it: 'Love your <em>neighbor</em> as yourself.'"),("Galatians+5:14","For the entire law is fulfilled in keeping this one command: 'Love your <em>neighbor</em> as yourself.'"),("James+2:8","If you really keep the royal law found in Scripture, 'Love your <em>neighbor</em> as yourself,' you are doing right.")],
     [(4139,"Plēsion (Neighbor)"),(3624,"Oikos (House)"),(26,"Agapē (Love)"),(3611,"Oikeō (To Dwell)")]),
    (4042, "Περιοχη", "Periochē", "Noun, Feminine", "Passage / Section (of Scripture)",
     "From <em>periechō</em> (to contain). A section or passage of text, particularly of Scripture. Used in Acts 8:32 of the passage of Isaiah that the Ethiopian eunuch was reading.",
     "The Ethiopian eunuch was reading a specific <em>passage</em> of Isaiah — Isaiah 53, the Suffering Servant prophecy (Acts 8:32). Philip used that very <em>passage</em> to tell him the good news about Jesus. <strong>Every passage of Scripture points to Christ</strong>, and the Spirit guides seekers to the right text at the right time.",
     [("Acts+8:32","This is the <em>passage</em> of Scripture the eunuch was reading: 'He was led like a sheep to the slaughter.'"),("Acts+8:35","Then Philip began with that very <em>passage</em> of Scripture and told him the good news about Jesus."),("Luke+4:17","He found the place where it is written."),("Luke+24:27","And beginning with Moses and all the Prophets, he explained to them what was said in all the Scriptures concerning himself."),("2+Timothy+3:16","All Scripture is God-breathed and is useful for teaching.")],
     [(1124,"Graphē (Scripture)"),(4023,"Periechō (To Contain)"),(2098,"Euangelion (Gospel)"),(4151,"Pneuma (Spirit)")]),
    (4044, "Περιπειρω", "Peripeirō", "Verb", "To Pierce Through / To Impale",
     "From <em>peri</em> (through) and <em>peirō</em> (to pierce). To pierce all the way through, to impale. Paul uses it of those who <em>pierce</em> themselves with many griefs through the love of money.",
     "Paul warns that those who desire to be rich fall into temptation and are '<em>pierced through</em> with many griefs' (1 Timothy 6:10). The love of money is not merely a surface wound — it <em>pierces through</em> the soul completely. <strong>Greed is self-inflicted spiritual injury.</strong>",
     [("1+Timothy+6:10","For the love of money is a root of all kinds of evil. Some people, eager for money, have wandered from the faith and <em>pierced</em> themselves with many griefs."),("1+Timothy+6:9","Those who want to get rich fall into temptation and a trap and into many foolish and harmful desires."),("Matthew+6:24","No one can serve two masters. You cannot serve both God and money."),("Luke+12:15","Watch out! Be on your guard against all kinds of greed; life does not consist in an abundance of possessions."),("Hebrews+13:5","Keep your lives free from the love of money and be content with what you have.")],
     [(4124,"Pleonexia (Greed)"),(5365,"Philarguria (Love of Money)"),(3601,"Odunē (Pain)"),(841,"Autarkeia (Contentment)")]),
    (4047, "Περιποιησις", "Peripoiēsis", "Noun, Feminine", "Preservation / Obtaining / Possession",
     "From <em>peripoieō</em> (to acquire, to preserve). The act of obtaining, preserving, or gaining possession. Used of God's own possession — His chosen people — and of obtaining salvation.",
     "Believers are God's own <em>possession</em> (1 Peter 2:9, Ephesians 1:14). This word carries stunning implications: the God of the universe has <em>acquired</em> a people for Himself at infinite cost — the blood of His Son. Salvation is also described as the '<em>obtaining</em>' of glory (2 Thessalonians 2:14). <strong>We belong to God because He purchased us.</strong>",
     [("Ephesians+1:14","Who is a deposit guaranteeing our inheritance until the redemption of those who are God's <em>possession</em>."),("1+Peter+2:9","But you are a chosen people, a royal priesthood, a holy nation, God's special <em>possession</em>."),("2+Thessalonians+2:14","He called you to this through our gospel, that you might share in the glory of our Lord Jesus Christ."),("1+Thessalonians+5:9","For God did not appoint us to suffer wrath but to receive salvation through our Lord Jesus Christ."),("Acts+20:28","Keep watch over yourselves and all the flock of which the Holy Spirit has made you overseers. Be shepherds of the church of God, which he bought with his own blood.")],
     [(4046,"Peripoieō (To Acquire)"),(2820,"Klēros (Lot/Inheritance)"),(629,"Apolutrōsis (Redemption)"),(4991,"Sōtēria (Salvation)")]),
    (4049, "Περισπαω", "Perispaō", "Verb", "To Be Distracted / To Be Pulled Away",
     "From <em>peri</em> (around) and <em>spaō</em> (to draw). To be drawn around in different directions, to be distracted, to be pulled away from what matters. Used of Martha's distraction with preparations.",
     "Martha was '<em>distracted</em> by all the preparations' while Mary sat at Jesus' feet (Luke 10:40). This single word captures one of the greatest spiritual dangers: being so busy with good things that we miss the best thing. <strong>Activity for God can become a substitute for intimacy with God.</strong>",
     [("Luke+10:40","But Martha was <em>distracted</em> by all the preparations that had to be made."),("Luke+10:41","'Martha, Martha,' the Lord answered, 'you are worried and upset about many things.'"),("Luke+10:42","But few things are needed — or indeed only one. Mary has chosen what is better, and it will not be taken away from her."),("Psalm+46:10","Be still, and know that I am God."),("Matthew+6:33","But seek first his kingdom and his righteousness, and all these things will be given to you as well.")],
     [(4685,"Spaō (To Draw)"),(3204,"Merimnaō (To Worry)"),(3210,"Merimna (Anxiety)"),(4102,"Pistis (Faith)")]),
    (4050, "Περισσεια", "Perisseia", "Noun, Feminine", "Abundance / Surplus / Overflow",
     "From <em>perissos</em> (exceeding). Abundance, surplus, that which overflows beyond what is needed. Used of the abundance of grace and the overflow of the heart.",
     "Paul declares that where sin increased, grace <em>abounded all the more</em> (Romans 5:17). Jesus said that out of the <em>overflow</em> of the heart the mouth speaks (Matthew 12:34). The Christian life is characterized by <em>abundance</em>, not scarcity. <strong>God's grace always exceeds sin's damage.</strong>",
     [("Romans+5:17","How much more will those who receive God's <em>abundant</em> provision of grace and of the gift of righteousness reign in life through the one man, Jesus Christ!"),("2+Corinthians+8:2","In the midst of a very severe trial, their <em>overflowing</em> joy and their extreme poverty welled up in rich generosity."),("James+1:21","Therefore, get rid of all moral filth and the evil that is so prevalent and humbly accept the word planted in you."),("Matthew+12:34","For the mouth speaks what the heart is full of."),("John+10:10","I have come that they may have life, and have it to the full.")],
     [(4052,"Perisseuō (To Abound)"),(5485,"Charis (Grace)"),(2222,"Zōē (Life)"),(5479,"Chara (Joy)")]),
    (4051, "Περισσευμα", "Perisseuma", "Noun, Neuter", "Abundance / What Remains / Surplus",
     "From <em>perisseuō</em> (to abound). That which is left over, the surplus, the abundance. Used of the twelve baskets of leftovers after feeding the five thousand.",
     "After feeding five thousand, the disciples collected twelve baskets of <em>leftovers</em> (Mark 8:8). God's provision always exceeds the need. The <em>surplus</em> is not waste — it demonstrates that <strong>God gives more than enough</strong>. Jesus also taught that what comes out of the mouth flows from the <em>overflow</em> of the heart (Matthew 12:34).",
     [("Mark+8:8","The people ate and were satisfied. Afterward the disciples picked up seven basketfuls of broken pieces that were <em>left over</em>."),("Matthew+12:34","For the mouth speaks what the heart is full of."),("Luke+6:45","A good man brings good things out of the good stored up in his heart, and an evil man brings evil things out of the evil stored up in his heart."),("2+Corinthians+8:14","Your <em>plenty</em> will supply what they need, so that in turn their plenty will supply what you need."),("John+6:12","When they had all had enough to eat, he said to his disciples, 'Gather the pieces that are <em>left over</em>. Let nothing be wasted.'")],
     [(4052,"Perisseuō (To Abound)"),(4050,"Perisseia (Abundance)"),(740,"Artos (Bread)"),(5485,"Charis (Grace)")]),
    (4054, "Περισσοτερον", "Perissoteron", "Adverb (Comparative)", "More Abundantly / Exceedingly",
     "Comparative form of <em>perissos</em> (exceeding). More abundantly, to a greater degree, exceedingly. Paul used this word to describe his labor and his love for the Corinthians.",
     "Paul declared: 'I worked harder than all of them — yet not I, but the grace of God that was with me' (1 Corinthians 15:10). He loved the Corinthians '<em>more abundantly</em>' (2 Corinthians 12:15). The superlative in Paul's life was always grace-driven. <strong>Grace produces more abundant effort, not less.</strong>",
     [("1+Corinthians+15:10","By the grace of God I am what I am, and his grace to me was not without effect. No, I worked <em>harder</em> than all of them."),("2+Corinthians+12:15","So I will very gladly spend for you everything I have and expend myself as well. If I love you <em>more</em>, will you love me less?"),("2+Corinthians+7:15","And his affection for you is all the <em>greater</em> when he remembers that you were all obedient."),("Hebrews+2:1","We must pay the <em>most careful</em> attention to what we have heard."),("Mark+7:36","The <em>more</em> he did so, the more they kept talking about it.")],
     [(4053,"Perissos (Exceeding)"),(5485,"Charis (Grace)"),(26,"Agapē (Love)"),(2041,"Ergon (Work)")]),
    (4055, "Περισσοτερως", "Perissoterōs", "Adverb", "More Exceedingly / Far More",
     "Adverbial form meaning far more, much more, to an even greater degree. Paul uses it of his labors exceeding those of other apostles.",
     "Paul's repeated use of superlatives about his ministry reveals not boasting but <strong>testimony to grace</strong>. He suffered '<em>far more</em>' imprisonments, beatings, and dangers (2 Corinthians 11:23). Yet his joy was also '<em>far more</em>' abundant. Suffering and joy are not opposites in God's economy — they are companions.",
     [("2+Corinthians+11:23","Are they servants of Christ? I am <em>more</em>. I have worked much harder, been in prison more frequently, been flogged more severely."),("2+Corinthians+1:12","Now this is our boast: Our conscience testifies that we have conducted ourselves in the world with integrity and godly sincerity."),("Galatians+1:14","I was advancing in Judaism beyond many of my own age among my people and was <em>extremely</em> zealous for the traditions of my fathers."),("Philippians+1:14","Because of my chains, most of the brothers and sisters have become confident in the Lord and dare all the <em>more</em> to proclaim the gospel without fear."),("1+Thessalonians+2:17","We made every effort to see you. For we wanted to come to you — certainly I, Paul, did, again and again.")],
     [(4054,"Perissoteron (More Abundantly)"),(3804,"Pathēma (Suffering)"),(5479,"Chara (Joy)"),(5485,"Charis (Grace)")]),
    (4056, "Περισσοτερως_2", "Perissoterōs (variant)", "Adverb", "All the More / Especially",
     "Variant usage of the same adverb. Context determines whether it means 'all the more,' 'especially,' or 'beyond measure.'",
     "The writer of Hebrews urges: 'We must pay the <em>most careful</em> attention to what we have heard, so that we do not drift away' (Hebrews 2:1). The more revelation we receive, the <em>greater</em> our responsibility. <strong>Knowledge increases accountability.</strong>",
     [("Hebrews+2:1","We must pay the <em>most careful</em> attention to what we have heard, so that we do not drift away."),("Hebrews+13:19","I particularly urge you to pray so that I may be restored to you soon."),("2+Corinthians+2:4","For I wrote you out of great distress and anguish of heart and with many tears, not to grieve you but to let you know the depth of my love for you."),("Mark+15:14","'Why? What crime has he committed?' asked Pilate. But they shouted all the <em>louder</em>, 'Crucify him!'"),("2+Corinthians+7:13","By all this we are encouraged. In addition to our own encouragement, we were especially delighted to see how happy Titus was.")],
     [(4053,"Perissos (Exceeding)"),(191,"Akouō (To Hear)"),(4102,"Pistis (Faith)"),(3056,"Logos (Word)")]),
    (4057, "Περισσως", "Perissōs", "Adverb", "Exceedingly / Abundantly / Beyond Measure",
     "Adverbial form of <em>perissos</em> (exceeding). Exceedingly, beyond measure, abundantly. Describes the intensity of emotional and spiritual responses.",
     "The crowds were '<em>exceedingly</em>' astonished at Jesus' teaching (Mark 10:26). Peter insisted '<em>more vehemently</em>' that he would never deny Jesus (Mark 14:31). This word captures moments when human experience pushes past normal boundaries — <strong>encounters with Christ produce extraordinary responses</strong>, whether of wonder, devotion, or conviction.",
     [("Mark+10:26","The disciples were <em>even more</em> amazed, and said to each other, 'Who then can be saved?'"),("Mark+14:31","But Peter insisted <em>emphatically</em>, 'Even if I have to die with you, I will never disown you.'"),("Matthew+27:23","'Why? What crime has he committed?' asked Pilate. But they shouted all the <em>louder</em>, 'Crucify him!'"),("Acts+26:11","Many a time I went from one synagogue to another to have them punished, and I tried to force them to blaspheme. I was so <em>obsessed</em> with persecuting them."),("Mark+15:14","But they shouted all the <em>louder</em>, 'Crucify him!'")],
     [(4053,"Perissos (Exceeding)"),(2285,"Thambos (Amazement)"),(1411,"Dunamis (Power)"),(2316,"Theos (God)")]),
    (4058, "Περιστερα", "Peristera", "Noun, Feminine", "Dove / Pigeon",
     "The Greek word for dove or pigeon. One of the most symbolically rich creatures in Scripture — representing the Holy Spirit, peace, purity, and sacrifice.",
     "At Jesus' baptism, the Spirit descended 'like a <em>dove</em>' (Matthew 3:16) — gentle, pure, and peaceful. Jesus told His disciples to be 'as innocent as <em>doves</em>' (Matthew 10:16). Doves were also the sacrifice of the poor (Luke 2:24). The <em>dove</em> thus represents <strong>the Spirit's gentle nature, the call to innocence, and God's provision for the humble</strong>.",
     [("Matthew+3:16","As soon as Jesus was baptized, he went up out of the water. At that moment heaven was opened, and he saw the Spirit of God descending like a <em>dove</em>."),("Matthew+10:16","I am sending you out like sheep among wolves. Therefore be as shrewd as snakes and as innocent as <em>doves</em>."),("Luke+2:24","And to offer a sacrifice in keeping with what is said in the Law of the Lord: 'a pair of <em>doves</em> or two young pigeons.'"),("John+1:32","Then John gave this testimony: 'I saw the Spirit come down from heaven as a <em>dove</em> and remain on him.'"),("Mark+1:10","Just as Jesus was coming up out of the water, he saw heaven being torn open and the Spirit descending on him like a <em>dove</em>.")],
     [(4151,"Pneuma (Spirit)"),(907,"Baptizō (To Baptize)"),(2378,"Thusia (Sacrifice)"),(40,"Hagios (Holy)")]),
    (4060, "Περιτιθημι", "Peritithēmi", "Verb", "To Place Around / To Put On / To Bestow",
     "From <em>peri</em> (around) and <em>tithēmi</em> (to place). To place around, to put on, to bestow. Used of placing the crown of thorns on Jesus and of God bestowing greater honor on lesser members.",
     "The soldiers '<em>placed</em>' a crown of thorns on Jesus' head (Matthew 27:29) — meant as mockery, it became the greatest symbol of vicarious suffering. Paul teaches that God '<em>bestows</em> greater honor' on the parts of the body that seem to lack it (1 Corinthians 12:24). <strong>What the world uses to shame, God transforms into glory.</strong>",
     [("Matthew+27:29","They twisted together a crown of thorns and <em>set it on</em> his head."),("1+Corinthians+12:24","While our presentable parts need no special treatment. But God has put the body together, giving <em>greater honor</em> to the parts that lacked it."),("Mark+15:17","They <em>put</em> a purple robe on him, then twisted together a crown of thorns and set it on him."),("John+19:2","The soldiers twisted together a crown of thorns and <em>put it on</em> his head."),("Song+of+Solomon+8:6","Place me like a seal over your heart, like a seal on your arm; for love is as strong as death.")],
     [(5087,"Tithēmi (To Place)"),(4735,"Stephanos (Crown)"),(4716,"Stauros (Cross)"),(1391,"Doxa (Glory)")]),
    (4062, "Περιτρεπω", "Peritrepō", "Verb", "To Turn / To Drive Mad",
     "From <em>peri</em> (around) and <em>trepō</em> (to turn). To turn around completely, to drive to madness. Festus accused Paul of being <em>driven mad</em> by too much learning.",
     "Festus declared: 'You are out of your mind, Paul! Your great learning is <em>driving you insane</em>!' (Acts 26:24). Paul's response was dignified: 'I am not insane... What I am saying is true and reasonable.' The world often views passionate faith as madness. <strong>Devotion to Christ will always appear unreasonable to those who reject Him.</strong>",
     [("Acts+26:24","At this point Festus interrupted Paul's defense. 'You are out of your mind, Paul!' he shouted. 'Your great learning is <em>driving you insane</em>.'"),("Acts+26:25","'I am not insane, most excellent Festus,' Paul replied. 'What I am saying is true and reasonable.'"),("2+Corinthians+5:13","If we are 'out of our mind,' as some say, it is for God."),("1+Corinthians+1:18","For the message of the cross is foolishness to those who are perishing, but to us who are being saved it is the power of God."),("Acts+17:32","When they heard about the resurrection of the dead, some of them sneered.")],
     [(3972,"Paulos (Paul)"),(225,"Alētheia (Truth)"),(3474,"Mōros (Foolish)"),(4678,"Sophia (Wisdom)")]),
    (4064, "Περιφερω", "Peripherō", "Verb", "To Carry About / To Move Around",
     "From <em>peri</em> (around) and <em>pherō</em> (to carry). To carry about, to bear from place to place. Used of carrying the sick to Jesus and of being tossed about by false doctrine.",
     "People '<em>carried about</em>' the sick on mats to wherever Jesus was (Mark 6:55). Paul warns against being '<em>carried about</em>' by every wind of doctrine (Ephesians 4:14). The contrast is powerful: being carried to Jesus brings healing; being carried by false teaching brings destruction. <strong>The question is always: who or what is carrying you, and where?</strong>",
     [("Mark+6:55","They ran throughout that whole region and <em>carried</em> the sick on mats to wherever they heard he was."),("Ephesians+4:14","Then we will no longer be infants, tossed back and forth by the waves, and blown here and there by every wind of teaching and by the cunning and craftiness of people."),("2+Corinthians+4:10","We always <em>carry around</em> in our body the death of Jesus, so that the life of Jesus may also be revealed."),("Hebrews+13:9","Do not be <em>carried away</em> by all kinds of strange teachings."),("Jude+1:12","They are clouds without rain, <em>blown along</em> by the wind.")],
     [(5342,"Pherō (To Carry)"),(1319,"Didaskalia (Teaching)"),(2390,"Iaomai (To Heal)"),(4102,"Pistis (Faith)")]),
    (4065, "Περιφρονεω", "Periphroneo", "Verb", "To Despise / To Think Around (Disregard)",
     "From <em>peri</em> (beyond) and <em>phroneō</em> (to think). To think beyond or around something, hence to disregard, to despise, to look down upon. Paul warns Timothy not to let anyone <em>despise</em> his youth.",
     "Paul's command to Timothy — 'Don't let anyone <em>look down on</em> you because you are young' (1 Timothy 4:12) — is not about attitude alone but about lifestyle. Timothy was to set an example in speech, conduct, love, faith, and purity so compelling that age became irrelevant. <strong>Godly character silences contempt.</strong>",
     [("Titus+2:15","These, then, are the things you should teach. Encourage and rebuke with all authority. Do not let anyone <em>despise</em> you."),("1+Timothy+4:12","Don't let anyone <em>look down on</em> you because you are young, but set an example for the believers."),("Matthew+18:10","See that you do not <em>despise</em> one of these little ones."),("Romans+14:3","The one who eats everything must not treat with <em>contempt</em> the one who does not."),("1+Corinthians+1:28","God chose the lowly things of this world and the <em>despised</em> things — and the things that are not — to nullify the things that are.")],
     [(5426,"Phroneō (To Think)"),(1848,"Exoutheneō (To Despise)"),(5014,"Tapeinophrosunē (Humility)"),(5262,"Hupodeigma (Example)")]),
    (4066, "Περιχωρος", "Perichōros", "Adjective/Noun", "Surrounding Region / Country Around",
     "From <em>peri</em> (around) and <em>chōra</em> (region). The surrounding region, the area around a place. Used frequently of the territory around the Jordan and around Galilee.",
     "John the Baptist's ministry drew people from 'all the <em>surrounding country</em> of the Jordan' (Luke 3:3). Jesus' fame spread throughout 'the entire <em>surrounding region</em>' (Luke 4:14). <strong>The gospel radiates outward from its point of impact</strong>, like ripples in a pond, reaching the surrounding territory and beyond.",
     [("Luke+3:3","He went into all the <em>country around</em> the Jordan, preaching a baptism of repentance for the forgiveness of sins."),("Luke+4:14","Jesus returned to Galilee in the power of the Spirit, and news about him spread through the whole <em>countryside</em>."),("Matthew+3:5","People went out to him from Jerusalem and all Judea and the whole <em>region</em> of the Jordan."),("Mark+1:28","News about him spread quickly over the whole <em>region</em> of Galilee."),("Luke+4:37","And the news about him spread throughout the <em>surrounding area</em>.")],
     [(5561,"Chōra (Region)"),(2098,"Euangelion (Gospel)"),(2784,"Kērussō (To Proclaim)"),(3341,"Metanoia (Repentance)")]),
    (4067, "Περιψωμα", "Peripsōma", "Noun, Neuter", "Refuse / Scum / Offscouring",
     "From <em>peripsaō</em> (to scrape all around). That which is scraped off, refuse, scum. Paul uses it to describe how the apostles were regarded by the world.",
     "Paul writes: 'We have become the <em>scum</em> of the earth, the garbage of the world' (1 Corinthians 4:13). This is not self-pity but a sober assessment of how the world views faithful servants of Christ. <strong>The world's contempt for God's messengers is a badge of authenticity</strong>, not shame.",
     [("1+Corinthians+4:13","When we are slandered, we answer kindly. We have become the <em>scum</em> of the earth, the garbage of the world — right up to this moment."),("1+Corinthians+4:9","For it seems to me that God has put us apostles on display at the end of the procession, like those condemned to die in the arena."),("2+Corinthians+6:8","Through glory and dishonor, bad report and good report; genuine, yet regarded as impostors."),("Matthew+5:11","Blessed are you when people insult you, persecute you and falsely say all kinds of evil against you because of me."),("Hebrews+11:38","The world was not worthy of them.")],
     [(2889,"Kosmos (World)"),(1377,"Diōkō (To Persecute)"),(3804,"Pathēma (Suffering)"),(5281,"Hupomonē (Endurance)")]),
    (4068, "Περπερευομαι", "Perpereuomai", "Verb", "To Brag / To Boast / To Be Vainglorious",
     "Of uncertain origin. To brag, to be boastful, to be a windbag. Used only in 1 Corinthians 13:4 — 'love does not <em>boast</em>.'",
     "In Paul's great hymn to love, he declares that love 'does not <em>boast</em>' (1 Corinthians 13:4). Boasting is self-promotion — the opposite of love, which seeks the good of others. <strong>Love and pride cannot coexist.</strong> Where love increases, self-promotion decreases. The greatest demonstration of un-boastful love was Christ's kenosis — emptying Himself of glory to become a servant (Philippians 2:7).",
     [("1+Corinthians+13:4","Love is patient, love is kind. It does not envy, it does not <em>boast</em>, it is not proud."),("1+Corinthians+13:5","It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs."),("Philippians+2:3","Do nothing out of selfish ambition or vain conceit. Rather, in humility value others above yourselves."),("Philippians+2:7","Rather, he made himself nothing by taking the very nature of a servant, being made in human likeness."),("Proverbs+27:2","Let someone else praise you, and not your own mouth; an outsider, and not your own lips.")],
     [(26,"Agapē (Love)"),(2744,"Kauchaomai (To Boast)"),(5012,"Tapeinophrosunē (Humility)"),(5014,"Tapeinos (Humble)")]),
    (4069, "Περσις", "Persis", "Noun, Proper", "Persis (Woman's Name)",
     "A feminine proper name meaning 'Persian woman.' Persis was a Christian woman in Rome whom Paul greeted warmly in Romans 16.",
     "Paul commends Persis as 'the beloved <em>Persis</em>, who has worked hard in the Lord' (Romans 16:12). Romans 16 contains a remarkable number of women who served in the early church — Persis among them. <strong>Women were active laborers in the gospel</strong> from the very beginning, recognized and commended by the apostle Paul himself.",
     [("Romans+16:12","Greet Tryphena and Tryphosa, those women who work hard in the Lord. Greet my dear friend <em>Persis</em>, another woman who has worked very hard in the Lord."),("Romans+16:1","I commend to you our sister Phoebe, a deacon of the church in Cenchreae."),("Romans+16:3","Greet Priscilla and Aquila, my co-workers in Christ Jesus."),("Romans+16:7","Greet Andronicus and Junia, my fellow Jews who have been in prison with me. They are outstanding among the apostles."),("Philippians+4:3","Yes, and I ask you, my true companion, help these women since they have contended at my side in the cause of the gospel.")],
     [(3972,"Paulos (Paul)"),(1577,"Ekklēsia (Church)"),(1248,"Diakonia (Service)"),(26,"Agapē (Love)")]),
    (4070, "Περυσι", "Perusi", "Adverb", "Last Year / A Year Ago",
     "An adverb meaning last year, a year ago. Paul uses it to remind the Corinthians of their early enthusiasm for the collection for Jerusalem's saints.",
     "Paul reminds the Corinthians: 'Last year you were the first not only to give but also to have the desire to do so' (2 Corinthians 8:10). Initial enthusiasm can fade. <strong>Finishing what we start is as important as starting it.</strong> Desire without completion is incomplete obedience.",
     [("2+Corinthians+8:10","Here is my judgment about what is best for you in this matter. <em>Last year</em> you were the first not only to give but also to have the desire to do so."),("2+Corinthians+9:2","For I know your eagerness to help, and I have been boasting about it. I told them that since <em>last year</em> you in Achaia were ready to give."),("Galatians+6:9","Let us not become weary in doing good, for at the proper time we will reap a harvest if we do not give up."),("Philippians+1:6","Being confident of this, that he who began a good work in you will carry it on to completion."),("Hebrews+10:36","You need to persevere so that when you have done the will of God, you will receive what he has promised.")],
     [(5281,"Hupomonē (Endurance)"),(1325,"Didōmi (To Give)"),(5485,"Charis (Grace)"),(2041,"Ergon (Work)")]),
    (4071, "Πετεινον", "Peteinon", "Noun, Neuter", "Bird / Fowl",
     "From <em>petomai</em> (to fly). A bird, any winged creature that flies. Jesus used birds extensively in His teaching — as examples of God's provision and in the Parable of the Sower.",
     "Jesus pointed to <em>birds</em> as proof of God's care: 'Look at the <em>birds</em> of the air; they do not sow or reap or store away in barns, and yet your heavenly Father feeds them. Are you not much more valuable than they?' (Matthew 6:26). In the Parable of the Sower, <em>birds</em> ate the seed on the path — representing Satan snatching away the word. <strong>The same creatures that illustrate providence also illustrate spiritual attack.</strong>",
     [("Matthew+6:26","Look at the <em>birds</em> of the air; they do not sow or reap or store away in barns, and yet your heavenly Father feeds them."),("Matthew+13:4","As he was scattering the seed, some fell along the path, and the <em>birds</em> came and ate it up."),("Luke+12:24","Consider the ravens: They do not sow or reap, they have no storeroom or barn; yet God feeds them. And how much more valuable you are than <em>birds</em>!"),("Matthew+13:32","Though it is the smallest of all seeds, yet when it grows, it is the largest of garden plants and becomes a tree, so that the <em>birds</em> come and perch in its branches."),("Genesis+1:20","And let <em>birds</em> fly above the earth across the vault of the sky.")],
     [(4421,"Peteinos variant"),(4058,"Peristera (Dove)"),(2316,"Theos (God)"),(4307,"Pronoia (Providence)")]),
    (4072, "Πετομαι", "Petomai", "Verb", "To Fly",
     "To fly, to move through the air. Used in Revelation of an eagle (or angel) flying in midheaven, proclaiming God's messages.",
     "In Revelation, an eagle '<em>flying</em> in midair' cries out triple woe to the inhabitants of the earth (Revelation 8:13). Angels also '<em>fly</em>' in midheaven proclaiming the eternal gospel (Revelation 14:6). <strong>God's final messages are delivered with urgency and speed</strong> — flying, not walking — because time is short.",
     [("Revelation+8:13","As I watched, I heard an eagle that was <em>flying</em> in midair call out in a loud voice: 'Woe! Woe! Woe!'"),("Revelation+14:6","Then I saw another angel <em>flying</em> in midair, and he had the eternal gospel to proclaim."),("Revelation+19:17","And I saw an angel standing in the sun, who cried in a loud voice to all the birds <em>flying</em> in midair."),("Isaiah+40:31","They will soar on wings like eagles; they will run and not grow weary."),("Revelation+12:14","The woman was given the two wings of a great eagle, so that she might <em>fly</em> to the place prepared for her.")],
     [(4071,"Peteinon (Bird)"),(32,"Angelos (Angel)"),(105,"Aetos (Eagle)"),(2098,"Euangelion (Gospel)")]),
    (4073, "Πετρα", "Petra", "Noun, Feminine", "Rock / Bedrock / Large Stone",
     "A mass of rock, bedrock, a large immovable stone. Distinguished from <em>petros</em> (a single stone). Jesus said He would build His church on 'this <em>rock</em>' — one of the most discussed statements in the NT.",
     "Jesus declared: 'On this <em>rock</em> I will build my church' (Matthew 16:18). Whether the 'rock' is Peter's confession, Peter himself, or Christ, the point is clear: the church is built on an <strong>immovable, unshakeable foundation</strong>. Paul identifies Christ as 'the <em>rock</em>' that followed Israel in the wilderness (1 Corinthians 10:4). The wise man builds on <em>rock</em>, the fool on sand (Matthew 7:24-25).",
     [("Matthew+16:18","And I tell you that you are Peter, and on this <em>rock</em> I will build my church."),("1+Corinthians+10:4","And drank the same spiritual drink; for they drank from the spiritual <em>rock</em> that accompanied them, and that rock was Christ."),("Matthew+7:24","Therefore everyone who hears these words of mine and puts them into practice is like a wise man who built his house on the <em>rock</em>."),("Romans+9:33","See, I lay in Zion a stone that causes people to stumble and a <em>rock</em> that makes them fall."),("1+Peter+2:8","And, 'A stone that causes people to stumble and a <em>rock</em> that makes them fall.'")],
     [(4074,"Petros (Peter/Stone)"),(3037,"Lithos (Stone)"),(2310,"Themelios (Foundation)"),(1577,"Ekklēsia (Church)")]),
    (4075, "Πετρωδες", "Petrōdes", "Adjective", "Rocky / Stony Ground",
     "From <em>petra</em> (rock). Rocky, consisting of rock with thin soil over it. Used in the Parable of the Sower for seed that falls on <em>rocky</em> ground.",
     "In Jesus' parable, seed on <em>rocky</em> ground sprang up quickly but had no root and withered when the sun came up (Mark 4:5-6). This represents those who receive the word with joy but have no depth — when trouble comes, they fall away. <strong>Quick growth without deep roots produces impressive but temporary faith.</strong>",
     [("Mark+4:5","Some fell on <em>rocky</em> places, where it did not have much soil. It sprang up quickly, because the soil was shallow."),("Mark+4:16","Others, like seed sown on <em>rocky</em> places, hear the word and at once receive it with joy."),("Mark+4:17","But since they have no root, they last only a short time. When trouble or persecution comes because of the word, they quickly fall away."),("Matthew+13:5","Some fell on <em>rocky</em> places, where it did not have much soil."),("Luke+8:6","Some fell on <em>rocky</em> ground, and when it came up, the plants withered because they had no moisture.")],
     [(4073,"Petra (Rock)"),(4687,"Speirō (To Sow)"),(4491,"Rhiza (Root)"),(4102,"Pistis (Faith)")]),
    (4076, "Πηγανον", "Pēganon", "Noun, Neuter", "Rue (Herb Plant)",
     "A pungent herb (Ruta graveolens) used in cooking and medicine. Jesus mentioned it when rebuking the Pharisees for tithing herbs while neglecting justice and love.",
     "Jesus said: 'Woe to you Pharisees, because you give God a tenth of your mint, <em>rue</em> and all other kinds of garden herbs, but you neglect justice and the love of God' (Luke 11:42). <strong>Meticulous religious observance without justice and love is spiritual hypocrisy.</strong> God cares more about character than calculations.",
     [("Luke+11:42","Woe to you Pharisees, because you give God a tenth of your mint, <em>rue</em> and all other kinds of garden herbs, but you neglect justice and the love of God."),("Matthew+23:23","Woe to you, teachers of the law and Pharisees, you hypocrites! You give a tenth of your spices — mint, dill and cumin. But you have neglected the more important matters of the law — justice, mercy and faithfulness."),("Micah+6:8","He has shown you, O mortal, what is good. And what does the Lord require of you? To act justly and to love mercy and to walk humbly with your God."),("Isaiah+1:17","Learn to do right; seek justice. Defend the oppressed."),("Hosea+6:6","For I desire mercy, not sacrifice, and acknowledgment of God rather than burnt offerings.")],
     [(1343,"Dikaiosunē (Righteousness)"),(26,"Agapē (Love)"),(2920,"Krisis (Judgment)"),(1656,"Eleos (Mercy)")]),
    (4077, "Πηγη", "Pēgē", "Noun, Feminine", "Spring / Fountain / Source / Well",
     "A spring, fountain, or well — a natural source of flowing water. Jesus used this metaphor powerfully of the living water that springs up to eternal life.",
     "Jesus told the Samaritan woman: 'The water I give them will become in them a <em>spring</em> of water welling up to eternal life' (John 4:14). James notes that a <em>spring</em> cannot produce both fresh and salt water (James 3:11) — a person's speech should be consistent. In Revelation, the Lamb leads to '<em>springs</em> of living water' (Revelation 7:17). <strong>Christ is the ultimate spring — inexhaustible, life-giving, and pure.</strong>",
     [("John+4:14","Whoever drinks the water I give them will never thirst. Indeed, the water I give them will become in them a <em>spring</em> of water welling up to eternal life."),("Revelation+7:17","For the Lamb at the center of the throne will be their shepherd; he will lead them to <em>springs</em> of living water."),("James+3:11","Can both fresh water and salt water flow from the same <em>spring</em>?"),("Revelation+21:6","To the thirsty I will give water without cost from the <em>spring</em> of the water of life."),("Jeremiah+2:13","My people have committed two sins: They have forsaken me, the <em>spring</em> of living water.")],
     [(5204,"Hudōr (Water)"),(2222,"Zōē (Life)"),(4215,"Potamos (River)"),(4151,"Pneuma (Spirit)")]),
    (4078, "Πηγνυμι", "Pēgnumi", "Verb", "To Fix / To Pitch / To Set Up",
     "To make firm, to fix in place, to pitch (a tent). Used in Hebrews 8:2 of the tabernacle that the Lord <em>pitched</em>, not man.",
     "The 'true tabernacle <em>set up</em> by the Lord, not by a mere human being' (Hebrews 8:2) is the heavenly sanctuary where Christ ministers as high priest. The earthly tabernacle was a copy; the heavenly one is the reality. <strong>God's dwelling is not made with human hands</strong> — it is eternal, perfect, and firmly established by the Lord Himself.",
     [("Hebrews+8:2","Who serves in the sanctuary, the true tabernacle <em>set up</em> by the Lord, not by a mere human being."),("Hebrews+9:11","But when Christ came as high priest of the good things that are now already here, he went through the greater and more perfect tabernacle that is not made with human hands."),("Hebrews+9:24","For Christ did not enter a sanctuary made with human hands that was only a copy of the true one; he entered heaven itself."),("Acts+7:44","Our ancestors had the tabernacle of the covenant law with them in the wilderness."),("Revelation+21:3","And I heard a loud voice from the throne saying, 'Look! God's dwelling place is now among the people.'")],
     [(4633,"Skēnē (Tabernacle)"),(749,"Archiereus (High Priest)"),(2413,"Hieros (Sacred)"),(3772,"Ouranos (Heaven)")]),
    (4079, "Πηδαλιον", "Pēdalion", "Noun, Neuter", "Rudder / Helm",
     "A rudder — the steering mechanism of a ship. James uses it as an analogy for the tongue: small but directing the entire course of one's life.",
     "James writes: 'Ships are steered by a very small <em>rudder</em> wherever the pilot wants to go' (James 3:4). The tongue, like a <em>rudder</em>, is disproportionately powerful relative to its size. A ship's course is determined by this small instrument. <strong>Words steer lives.</strong> The direction of a person's existence is shaped by what they say.",
     [("James+3:4","Or take ships as an example. Although they are so large and are driven by strong winds, they are steered by a very small <em>rudder</em> wherever the pilot wants to go."),("Acts+27:40","Cutting loose the anchors, they left them in the sea and at the same time untied the ropes that held the <em>rudders</em>."),("James+3:5","Likewise, the tongue is a small part of the body, but it makes great boasts."),("Proverbs+18:21","The tongue has the power of life and death."),("Proverbs+15:1","A gentle answer turns away wrath, but a harsh word stirs up anger.")],
     [(1100,"Glōssa (Tongue)"),(3056,"Logos (Word)"),(4678,"Sophia (Wisdom)"),(3295,"Metagō (To Direct)")]),
    (4080, "Πηλικος", "Pēlikos", "Adjective (Interrogative)", "How Large / How Great",
     "An interrogative adjective asking 'how large?' or 'how great?' Paul uses it at the end of Galatians, possibly referring to the large size of his handwriting due to his eye condition.",
     "Paul writes: 'See what large letters I use as I write to you with my own hand!' (Galatians 6:11). This personal detail — possibly due to poor eyesight — demonstrates the apostle's love: he wrote personally despite physical difficulty. <strong>Love finds ways to serve even through weakness.</strong>",
     [("Galatians+6:11","See what <em>large</em> letters I use as I write to you with my own hand!"),("Hebrews+7:4","Just think <em>how great</em> he was: Even the patriarch Abraham gave him a tenth of the plunder!"),("2+Corinthians+12:9","But he said to me, 'My grace is sufficient for you, for my power is made perfect in weakness.'"),("Galatians+4:15","Where, then, is your blessing of me now? I can testify that, if you could have done so, you would have torn out your eyes and given them to me."),("2+Corinthians+11:30","If I must boast, I will boast of the things that show my weakness.")],
     [(3972,"Paulos (Paul)"),(5485,"Charis (Grace)"),(769,"Astheneia (Weakness)"),(26,"Agapē (Love)")]),
    (4081, "Πηλος", "Pēlos", "Noun, Masculine", "Clay / Mud",
     "Clay or mud. Used of the clay Jesus made to anoint the blind man's eyes and of Paul's potter-and-clay analogy for God's sovereignty.",
     "Jesus made <em>clay</em> with His saliva and anointed the blind man's eyes (John 9:6) — using the very substance from which Adam was formed to restore sight. Paul asks: 'Shall what is formed say to the potter, Why did you make me like this? Does not the potter have the right over the <em>clay</em>?' (Romans 9:20-21). <strong>We are clay in the hands of the sovereign Potter.</strong>",
     [("John+9:6","After saying this, he spit on the ground, made some <em>mud</em> with the saliva, and put it on the man's eyes."),("Romans+9:21","Does not the potter have the right to make out of the same lump of <em>clay</em> some pottery for special purposes and some for common use?"),("John+9:11","He replied, 'The man they call Jesus made some <em>mud</em> and put it on my eyes.'"),("Isaiah+64:8","Yet you, Lord, are our Father. We are the <em>clay</em>, you are the potter; we are all the work of your hand."),("Jeremiah+18:6","Like <em>clay</em> in the hand of the potter, so are you in my hand, Israel.")],
     [(2316,"Theos (God)"),(2763,"Kerameus (Potter)"),(4160,"Poieō (To Make)"),(2937,"Ktisis (Creation)")]),
    (4082, "Πηρα", "Pēra", "Noun, Feminine", "Bag / Wallet / Leather Pouch",
     "A leather bag or traveler's wallet used for carrying provisions. Jesus instructed His disciples to take no <em>bag</em> on their mission, teaching radical dependence on God's provision.",
     "Jesus sent out His disciples with the instruction: 'Take nothing for the journey — no staff, no <em>bag</em>, no bread, no money, no extra shirt' (Luke 9:3). This was not about poverty as a virtue but about <strong>demonstrating that God Himself is sufficient provision</strong>. When they returned, Jesus asked: 'Did you lack anything?' They answered: 'Nothing' (Luke 22:35).",
     [("Luke+9:3","He told them: 'Take nothing for the journey — no staff, no <em>bag</em>, no bread, no money, no extra shirt.'"),("Luke+10:4","Do not take a purse or <em>bag</em> or sandals; and do not greet anyone on the road."),("Matthew+10:10","Take no <em>bag</em> for the journey or extra shirt or sandals or a staff."),("Mark+6:8","These were his instructions: 'Take nothing for the journey except a staff — no bread, no <em>bag</em>, no money in your belts.'"),("Luke+22:35","Then Jesus asked them, 'When I sent you without purse, <em>bag</em> or sandals, did you lack anything?' 'Nothing,' they answered.")],
     [(4102,"Pistis (Faith)"),(1325,"Didōmi (To Give)"),(4307,"Pronoia (Providence)"),(649,"Apostellō (To Send)")]),
    (4083, "Πηχυς", "Pēchus", "Noun, Masculine", "Cubit / Forearm Length",
     "A cubit — a unit of measure based on the length of the forearm (approximately 18 inches). Jesus used it to illustrate the futility of worry: no one can add a single <em>cubit</em> to their life by worrying.",
     "Jesus asked: 'Can any one of you by worrying add a single <em>hour</em> to your life?' (Matthew 6:27). The literal Greek says 'a single <em>cubit</em> to your stature/lifespan.' Worry is not just spiritually harmful — it is <strong>utterly ineffective</strong>. It cannot change reality by even the smallest measurement. Only trust in God produces genuine change.",
     [("Matthew+6:27","Can any one of you by worrying add a single <em>hour</em> to your life?"),("Luke+12:25","Who of you by worrying can add a single <em>hour</em> to your life?"),("Revelation+21:17","The angel measured the wall using human measurement, and it was 144 <em>cubits</em> thick."),("John+21:8","The other disciples followed in the boat, towing the net full of fish, for they were not far from shore, about a hundred <em>yards</em>."),("Genesis+6:15","This is how you are to build it: The ark is to be three hundred <em>cubits</em> long, fifty cubits wide and thirty cubits high.")],
     [(3204,"Merimnaō (To Worry)"),(4102,"Pistis (Faith)"),(3358,"Metron (Measure)"),(2222,"Zōē (Life)")]),
    (4084, "Πιαζω", "Piazō", "Verb", "To Seize / To Arrest / To Catch",
     "To seize, to take hold of, to arrest, to catch. Used of attempts to arrest Jesus and of catching fish. A word of forceful, purposeful grasping.",
     "Multiple times the Jewish authorities tried to <em>arrest</em> Jesus but could not, 'because his hour had not yet come' (John 7:30). When His hour finally arrived, Jesus allowed Himself to be <em>seized</em> (John 18:12). This shows <strong>sovereign timing</strong>: no one took Jesus' life — He laid it down voluntarily at the appointed moment.",
     [("John+7:30","At this they tried to <em>seize</em> him, but no one laid a hand on him, because his hour had not yet come."),("John+7:32","Then the chief priests and the Pharisees sent temple guards to <em>arrest</em> him."),("John+10:39","Again they tried to <em>seize</em> him, but he escaped their grasp."),("John+21:3","'I'm going out to fish,' Simon Peter told them, and they said, 'We'll go with you.' So they went out and got into the boat, but that night they <em>caught</em> nothing."),("Acts+12:4","After <em>arresting</em> him, he put him in prison, handing him over to be guarded by four squads of four soldiers each.")],
     [(2902,"Krateō (To Seize)"),(4815,"Sullambanō (To Arrest)"),(2540,"Kairos (Appointed Time)"),(2424,"Iēsous (Jesus)")]),
    (4085, "Πιεζω", "Piezō", "Verb", "To Press / To Press Down",
     "To press, to squeeze, to press down. Used in Luke 6:38 of giving: 'a good measure, <em>pressed down</em>, shaken together and running over.'",
     "Jesus promised that generous givers would receive 'a good measure, <em>pressed down</em>, shaken together and running over' (Luke 6:38). The imagery is of grain being measured: the seller presses it down to pack in more, shakes the container, and still it overflows. <strong>God's generosity to the generous is extravagant and overflowing.</strong>",
     [("Luke+6:38","Give, and it will be given to you. A good measure, <em>pressed down</em>, shaken together and running over, will be poured into your lap."),("2+Corinthians+9:6","Whoever sows sparingly will also reap sparingly, and whoever sows generously will also reap generously."),("Proverbs+11:25","A generous person will prosper; whoever refreshes others will be refreshed."),("Malachi+3:10","Bring the whole tithe into the storehouse, that there may be food in my house. Test me in this, says the Lord Almighty, and see if I will not throw open the floodgates of heaven."),("Acts+20:35","It is more blessed to give than to receive.")],
     [(1325,"Didōmi (To Give)"),(4052,"Perisseuō (To Abound)"),(5485,"Charis (Grace)"),(3358,"Metron (Measure)")]),
    (4086, "Πιθανολογια", "Pithanologia", "Noun, Feminine", "Persuasive Speech / Plausible Arguments",
     "From <em>pithanos</em> (persuasive) and <em>logos</em> (word). Persuasive, plausible-sounding but deceptive argumentation. Paul warns the Colossians against being deceived by <em>fine-sounding arguments</em>.",
     "Paul warns: 'I tell you this so that no one may deceive you by <em>fine-sounding arguments</em>' (Colossians 2:4). False teaching rarely sounds obviously wrong — it sounds <em>plausible</em>. The danger is not absurd claims but reasonable-sounding alternatives to the gospel. <strong>Discernment requires knowing truth so well that counterfeits are immediately recognized.</strong>",
     [("Colossians+2:4","I tell you this so that no one may deceive you by <em>fine-sounding arguments</em>."),("Colossians+2:8","See to it that no one takes you captive through hollow and deceptive philosophy."),("2+Corinthians+11:3","But I am afraid that just as Eve was deceived by the serpent's cunning, your minds may somehow be led astray."),("Ephesians+5:6","Let no one deceive you with empty words, for because of such things God's wrath comes on those who are disobedient."),("1+Timothy+4:1","The Spirit clearly says that in later times some will abandon the faith and follow deceiving spirits and things taught by demons.")],
     [(3056,"Logos (Word)"),(539,"Apatē (Deception)"),(225,"Alētheia (Truth)"),(1319,"Didaskalia (Teaching)")]),
    (4087, "Πικραινω", "Pikrainō", "Verb", "To Make Bitter / To Embitter",
     "From <em>pikros</em> (bitter). To make bitter, to embitter, to produce bitterness. Paul warns husbands not to be <em>harsh</em> (embittered) with their wives.",
     "Paul commands: 'Husbands, love your wives and do not be <em>harsh</em> with them' (Colossians 3:19). The word implies a pattern of bitterness that poisons the relationship. In Revelation, the waters become <em>bitter</em> at the trumpet judgment (Revelation 8:11). <strong>Bitterness — whether in marriage or in the soul — is toxic and destructive.</strong>",
     [("Colossians+3:19","Husbands, love your wives and do not be <em>harsh</em> with them."),("Revelation+8:11","A third of the waters turned <em>bitter</em>, and many people died from the waters that had become bitter."),("Revelation+10:9","He said to me, 'Take it and eat it. It will turn your stomach <em>sour</em>, but in your mouth it will be as sweet as honey.'"),("Hebrews+12:15","See to it that no one falls short of the grace of God and that no <em>bitter</em> root grows up to cause trouble and defile many."),("Ephesians+4:31","Get rid of all <em>bitterness</em>, rage and anger, brawling and slander, along with every form of malice.")],
     [(4088,"Pikria (Bitterness)"),(26,"Agapē (Love)"),(5485,"Charis (Grace)"),(863,"Aphiēmi (To Forgive)")]),
    (4088, "Πικρια", "Pikria", "Noun, Feminine", "Bitterness / Gall",
     "From <em>pikros</em> (bitter). Bitterness — both literal and metaphorical. The spiritual poison that corrupts the soul and defiles others.",
     "Hebrews warns against a 'root of <em>bitterness</em>' growing up to defile many (Hebrews 12:15). Peter told Simon the sorcerer he was 'full of <em>bitterness</em>' (Acts 8:23). Paul commands believers to get rid of all <em>bitterness</em> (Ephesians 4:31). <strong>Bitterness is never private — it always spreads</strong>, poisoning relationships and communities.",
     [("Hebrews+12:15","See to it that no one falls short of the grace of God and that no <em>bitter</em> root grows up to cause trouble and defile many."),("Ephesians+4:31","Get rid of all <em>bitterness</em>, rage and anger, brawling and slander, along with every form of malice."),("Acts+8:23","For I see that you are full of <em>bitterness</em> and captive to sin."),("Romans+3:14","Their mouths are full of cursing and <em>bitterness</em>."),("James+3:14","But if you harbor <em>bitter</em> envy and selfish ambition in your hearts, do not boast about it or deny the truth.")],
     [(4087,"Pikrainō (To Embitter)"),(863,"Aphiēmi (To Forgive)"),(26,"Agapē (Love)"),(5485,"Charis (Grace)")]),
    (4089, "Πικρος", "Pikros", "Adjective", "Bitter / Sharp",
     "Bitter, sharp, harsh. Used both of taste and of character. James warns against <em>bitter</em> jealousy that comes from earthly, unspiritual wisdom.",
     "James contrasts two kinds of wisdom: the wisdom from above is 'pure, peaceable, gentle,' while earthly wisdom produces '<em>bitter</em> jealousy and selfish ambition' (James 3:14). <strong>The taste test of wisdom is its fruit</strong> — true wisdom produces sweetness; false wisdom leaves a bitter aftertaste of conflict and division.",
     [("James+3:14","But if you harbor <em>bitter</em> envy and selfish ambition in your hearts, do not boast about it or deny the truth."),("James+3:11","Can both fresh water and salt water flow from the same spring?"),("James+3:17","But the wisdom that comes from heaven is first of all pure; then peace-loving, considerate, submissive, full of mercy and good fruit, impartial and sincere."),("Proverbs+14:10","Each heart knows its own <em>bitterness</em>, and no one else can share its joy."),("Revelation+10:10","I took the little scroll from the angel's hand and ate it. It tasted as sweet as honey in my mouth, but when I had eaten it, my stomach turned <em>sour</em>.")],
     [(4088,"Pikria (Bitterness)"),(4678,"Sophia (Wisdom)"),(2205,"Zēlos (Jealousy)"),(1515,"Eirēnē (Peace)")]),
    (4090, "Πικρως", "Pikrōs", "Adverb", "Bitterly",
     "The adverb form of <em>pikros</em> (bitter). Bitterly — with intense grief and remorse. Used of Peter's weeping after denying Jesus.",
     "After denying Jesus three times, Peter went out and 'wept <em>bitterly</em>' (Matthew 26:75). This is one of the most poignant moments in the Gospels. Peter's <em>bitter</em> tears were not mere regret but the beginning of genuine repentance. Unlike Judas, whose remorse led to suicide, Peter's <em>bitter</em> weeping led to restoration. <strong>Bitter tears watered by grace produce sweet restoration.</strong>",
     [("Matthew+26:75","Then Peter remembered the word Jesus had spoken: 'Before the rooster crows, you will disown me three times.' And he went outside and wept <em>bitterly</em>."),("Luke+22:62","And he went outside and wept <em>bitterly</em>."),("John+21:17","The third time he said to him, 'Simon son of John, do you love me?' Peter was hurt because Jesus asked him the third time."),("2+Corinthians+7:10","Godly sorrow brings repentance that leads to salvation and leaves no regret."),("Psalm+51:17","My sacrifice, O God, is a broken spirit; a broken and contrite heart you, God, will not despise.")],
     [(4088,"Pikria (Bitterness)"),(3340,"Metanoeō (To Repent)"),(2799,"Klaiō (To Weep)"),(600,"Apokathistēmi (To Restore)")]),
    (4091, "Πιλατος", "Pilatos", "Noun, Proper", "Pilate (Pontius Pilate)",
     "Pontius <em>Pilate</em> — the Roman prefect of Judea (AD 26-36) who presided over the trial and crucifixion of Jesus Christ. One of the most historically documented figures in the New Testament.",
     "<em>Pilate</em> asked Jesus: 'What is truth?' (John 18:38) — one of history's most ironic questions, spoken in the presence of Him who IS truth. Pilate found no fault in Jesus yet condemned Him under political pressure. He represents the <strong>tragedy of moral cowardice</strong>: knowing what is right but lacking the courage to do it. The Apostles' Creed preserves his name: 'suffered under Pontius Pilate.'",
     [("John+18:38","'What is truth?' retorted <em>Pilate</em>. With this he went out again to the Jews gathered there and said, 'I find no basis for a charge against him.'"),("Matthew+27:24","When <em>Pilate</em> saw that he was getting nowhere, but that instead an uproar was starting, he took water and washed his hands."),("Luke+23:4","Then <em>Pilate</em> announced to the chief priests and the crowd, 'I find no basis for a charge against this man.'"),("John+19:19","<em>Pilate</em> had a notice prepared and fastened to the cross. It read: JESUS OF NAZARETH, THE KING OF THE JEWS."),("1+Timothy+6:13","Christ Jesus, who while testifying before Pontius <em>Pilate</em> made the good confession.")],
     [(2424,"Iēsous (Jesus)"),(4716,"Stauros (Cross)"),(225,"Alētheia (Truth)"),(2920,"Krisis (Judgment)")]),
    (4092, "Πιμπρημι", "Pimprēmi", "Verb", "To Swell Up / To Burn / To Be Inflated",
     "To swell up, to burn, to become inflated. Used in Acts 28:6 when the Maltese expected Paul to <em>swell up</em> after being bitten by a viper.",
     "After Paul was bitten by a viper on Malta, the islanders watched, expecting him to <em>swell up</em> and die (Acts 28:6). When nothing happened, they changed their minds about him. <strong>God's protection of His servants confounds human expectations.</strong> The viper could not harm the one God was determined to deliver to Rome.",
     [("Acts+28:6","The people expected him to <em>swell up</em> or suddenly fall dead; but after waiting a long time and seeing nothing unusual happen to him, they changed their minds and said he was a god."),("Acts+28:3","Paul gathered a pile of brushwood and, as he put it on the fire, a viper, driven out by the heat, fastened itself on his hand."),("Mark+16:18","They will pick up snakes with their hands; and when they drink deadly poison, it will not hurt them at all."),("Luke+10:19","I have given you authority to trample on snakes and scorpions and to overcome all the power of the enemy; nothing will harm you."),("Psalm+91:13","You will tread on the lion and the cobra; you will trample the great lion and the serpent.")],
     [(3789,"Ophis (Serpent)"),(3972,"Paulos (Paul)"),(4982,"Sōzō (To Save)"),(2316,"Theos (God)")]),
    (4093, "Πινακιδιον", "Pinakidion", "Noun, Neuter", "Writing Tablet / Small Board",
     "Diminutive of <em>pinax</em> (board, platter). A small writing tablet, typically coated with wax for inscription with a stylus. Zechariah wrote on one to name his son John.",
     "When asked what his son should be named, the mute Zechariah asked for a <em>writing tablet</em> and wrote: 'His name is John' (Luke 1:63). At that moment his mouth was opened and he began praising God. <strong>Obedience to God's word releases the tongue for praise.</strong> Zechariah's silence ended when he obeyed the angel's instruction.",
     [("Luke+1:63","He asked for a <em>writing tablet</em>, and to everyone's astonishment he wrote, 'His name is John.'"),("Luke+1:64","Immediately his mouth was opened and his tongue set free, and he began to speak, praising God."),("Luke+1:13","But the angel said to him: 'Do not be afraid, Zechariah; your prayer has been heard. Your wife Elizabeth will bear you a son, and you are to call him John.'"),("Luke+1:20","And now you will be silent and not able to speak until the day this happens, because you did not believe my words."),("Psalm+40:3","He put a new song in my mouth, a hymn of praise to our God.")],
     [(1125,"Graphō (To Write)"),(2491,"Iōannēs (John)"),(134,"Aineō (To Praise)"),(4102,"Pistis (Faith)")]),
    (4094, "Πιναξ", "Pinax", "Noun, Masculine", "Platter / Dish / Board",
     "A flat board, platter, or dish. Used of the platter on which John the Baptist's head was brought — one of the NT's most horrifying images.",
     "Herodias' daughter asked for John the Baptist's head 'on a <em>platter</em>' (Matthew 14:8). This gruesome request, fulfilled by a weak king's rash oath, illustrates the <strong>deadly consequences of moral compromise</strong>. Herod's foolish promise, Herodias' vindictiveness, and the girl's manipulation combined to murder God's prophet.",
     [("Matthew+14:8","Prompted by her mother, she said, 'Give me here on a <em>platter</em> the head of John the Baptist.'"),("Matthew+14:11","His head was brought in on a <em>platter</em> and given to the girl, who carried it to her mother."),("Mark+6:25","At once the girl hurried in to the king with the request: 'I want you to give me right now the head of John the Baptist on a <em>platter</em>.'"),("Mark+6:28","And brought back his head on a <em>platter</em>. He presented it to the girl, and she gave it to her mother."),("Luke+11:39","Then the Lord said to him, 'Now then, you Pharisees clean the outside of the cup and <em>dish</em>, but inside you are full of greed and wickedness.'")],
     [(2491,"Iōannēs (John)"),(907,"Baptizō (To Baptize)"),(4396,"Prophētēs (Prophet)"),(3144,"Martus (Witness)")]),
    (4095, "Πινω", "Pinō", "Verb", "To Drink",
     "The basic Greek verb for drinking. Jesus used drinking metaphorically of receiving the Spirit, sharing in His suffering, and eternal life. One of the most theologically loaded ordinary words in the NT.",
     "Jesus cried out: 'Let anyone who is thirsty come to me and <em>drink</em>' (John 7:37). He asked James and John: 'Can you <em>drink</em> the cup I am going to <em>drink</em>?' (Matthew 20:22) — referring to His suffering. At the Last Supper, He said: '<em>Drink</em> from it, all of you. This is my blood of the covenant' (Matthew 26:27-28). <strong>To drink is to receive, to participate, to take something into oneself.</strong>",
     [("John+7:37","Let anyone who is thirsty come to me and <em>drink</em>."),("Matthew+26:27","Then he took a cup, and when he had given thanks, he gave it to them, saying, '<em>Drink</em> from it, all of you.'"),("Matthew+20:22","'You don't know what you are asking,' Jesus said to them. 'Can you <em>drink</em> the cup I am going to drink?'"),("John+4:14","Whoever <em>drinks</em> the water I give them will never thirst."),("1+Corinthians+10:4","And <em>drank</em> the same spiritual drink; for they drank from the spiritual rock that accompanied them, and that rock was Christ.")],
     [(4221,"Potērion (Cup)"),(5204,"Hudōr (Water)"),(3631,"Oinos (Wine)"),(4151,"Pneuma (Spirit)")]),
    (4096, "Πιοτης", "Piotēs", "Noun, Feminine", "Fatness / Richness",
     "From <em>piōn</em> (fat, rich). Fatness, richness — used metaphorically of the spiritual richness of the olive tree (Israel) into which Gentile believers are grafted.",
     "Paul warns Gentile believers not to boast against the natural branches (Israel), for they share in the 'nourishing <em>richness</em>' of the olive tree (Romans 11:17). Gentile believers are <em>grafted in</em> and share Israel's spiritual heritage. <strong>The church does not replace Israel but is grafted into the same root of God's covenant faithfulness.</strong>",
     [("Romans+11:17","You, though a wild olive shoot, have been grafted in among the others and now share in the nourishing sap from the olive root."),("Romans+11:18","Do not consider yourself to be superior to those other branches."),("Romans+11:24","If you were cut out of an olive tree that is wild by nature, and contrary to nature were grafted into a cultivated olive tree, how much more readily will these natural branches be grafted into their own olive tree!"),("Ephesians+2:12","Remember that at that time you were separate from Christ, excluded from citizenship in Israel and foreigners to the covenants of the promise."),("Psalm+52:8","But I am like an olive tree flourishing in the house of God; I trust in God's unfailing love for ever and ever.")],
     [(1636,"Elaia (Olive Tree)"),(2464,"Israēl (Israel)"),(1577,"Ekklēsia (Church)"),(1242,"Diathēkē (Covenant)")]),
    (4097, "Πιπρασκω", "Pipraskō", "Verb", "To Sell",
     "To sell, to dispose of for a price. Used of selling possessions, selling oneself into slavery to sin, and Judas' betrayal of Jesus for thirty pieces of silver.",
     "Jesus said to the rich young ruler: 'Go, <em>sell</em> your possessions and give to the poor' (Matthew 19:21). Paul describes humanity as '<em>sold</em> under sin' (Romans 7:14) — enslaved like a commodity. The early church '<em>sold</em>' their possessions to share with those in need (Acts 2:45). <strong>What we sell and what we buy reveals our deepest values.</strong>",
     [("Matthew+19:21","If you want to be perfect, go, <em>sell</em> your possessions and give to the poor, and you will have treasure in heaven."),("Romans+7:14","We know that the law is spiritual; but I am unspiritual, <em>sold</em> as a slave to sin."),("Acts+2:45","They <em>sold</em> property and possessions to give to anyone who had need."),("Matthew+26:9","This perfume could have been <em>sold</em> at a high price and the money given to the poor."),("Acts+4:34","For from time to time those who owned land or houses <em>sold</em> them, brought the money from the sales.")],
     [(59,"Agorazō (To Buy)"),(266,"Hamartia (Sin)"),(1325,"Didōmi (To Give)"),(629,"Apolutrōsis (Redemption)")]),
    (4098, "Πιπτω", "Piptō", "Verb", "To Fall",
     "One of the most common Greek verbs, meaning to fall. Used of physical falling, spiritual falling, falling before God in worship, the fall of Jerusalem, and the fall of Babylon in Revelation.",
     "This word spans the entire range of human experience before God. People <em>fell</em> at Jesus' feet in worship (Matthew 2:11). Jesus warned that those who <em>fall</em> on the stone will be broken (Matthew 21:44). Stars <em>fall</em> from heaven in apocalyptic judgment (Revelation 6:13). Babylon the Great has '<em>fallen</em>!' (Revelation 18:2). Paul asks: 'If they <em>fall</em>, will they never get up?' (Romans 11:11). <strong>In God's economy, falling can lead to worship, judgment, or restoration — depending on how one falls.</strong>",
     [("Matthew+2:11","They bowed down and worshiped him. Then they opened their treasures and presented him with gifts."),("Revelation+18:2","<em>Fallen</em>! Fallen is Babylon the Great!"),("Romans+11:11","Did they stumble so as to <em>fall</em> beyond recovery? Not at all!"),("Matthew+7:27","The rain came down, the streams rose, and the winds blew and beat against that house, and it <em>fell</em> with a great crash."),("Luke+10:18","He replied, 'I saw Satan <em>fall</em> like lightning from heaven.'")],
     [(4352,"Proskuneō (To Worship)"),(2920,"Krisis (Judgment)"),(450,"Anistēmi (To Rise)"),(4982,"Sōzō (To Save)")]),
    (4099, "Πισιδια", "Pisidia", "Noun, Proper", "Pisidia (Region)",
     "A region in southern Asia Minor (modern Turkey). Paul visited Pisidian Antioch during his first missionary journey and delivered a pivotal sermon in the synagogue there.",
     "Paul's sermon at Pisidian Antioch (Acts 13:16-41) is one of the most important in Acts. He traced salvation history from the Exodus through David to Jesus, declaring that through Christ 'everyone who believes is set free from every sin' (Acts 13:39). When the Jews rejected the message, Paul turned to the Gentiles. <strong>Pisidian Antioch became a turning point: rejection by some opened the door for others.</strong>",
     [("Acts+13:14","From Perga they went on to Pisidian Antioch. On the Sabbath they entered the synagogue and sat down."),("Acts+13:39","Through him everyone who believes is set free from every sin, a justification you were not able to obtain under the law of Moses."),("Acts+13:46","Then Paul and Barnabas answered them boldly: 'We had to speak the word of God to you first. Since you reject it, we now turn to the Gentiles.'"),("Acts+13:48","When the Gentiles heard this, they were glad and honored the word of the Lord; and all who were appointed for eternal life believed."),("Acts+14:24","After going through <em>Pisidia</em>, they came into Pamphylia.")],
     [(3972,"Paulos (Paul)"),(490,"Antiocheia (Antioch)"),(2098,"Euangelion (Gospel)"),(1484,"Ethnos (Nation)")]),
    (4101, "Πιστικος", "Pistikos", "Adjective", "Genuine / Pure / Trustworthy",
     "From <em>pistis</em> (faith/trust). Genuine, pure, trustworthy — describing the quality of the expensive nard (spikenard) ointment poured on Jesus.",
     "Mary anointed Jesus with '<em>pure</em> nard, an expensive perfume' (Mark 14:3, John 12:3). The adjective emphasizes the ointment was <strong>genuine, not counterfeit</strong> — the real thing, not a cheap imitation. This mirrors the gospel call: genuine faith, genuine love, genuine worship. God is not honored by imitations.",
     [("Mark+14:3","A woman came with an alabaster jar of very expensive perfume, made of <em>pure</em> nard. She broke the jar and poured the perfume on his head."),("John+12:3","Then Mary took about a pint of <em>pure</em> nard, an expensive perfume; she poured it on Jesus' feet and wiped his feet with her hair."),("John+12:5","Why wasn't this perfume sold and the money given to the poor? It was worth a year's wages."),("Mark+14:6","'Leave her alone,' said Jesus. 'Why are you bothering her? She has done a beautiful thing to me.'"),("Matthew+26:13","Truly I tell you, wherever this gospel is preached throughout the world, what she has done will also be told, in memory of her.")],
     [(4102,"Pistis (Faith)"),(4103,"Pistos (Faithful)"),(3464,"Muron (Ointment)"),(26,"Agapē (Love)")]),
]

# Filter out already existing
entries = [(n, *rest) for n, *rest in entries if n not in existing]
entries = entries[:89]  # Take only what we need

print(f"Will create {len(entries)} new entries (batch 2)")

created = 0
for entry in entries:
    num = entry[0]
    greek = entry[1]
    translit = entry[2]
    pos = entry[3]
    gloss = entry[4]
    definition = entry[5]
    theological = entry[6]
    verses = entry[7]
    related = entry[8]
    filepath = os.path.join(LEXICON_DIR, f"G{num}.html")
    html = make_html(num, greek, translit, pos, gloss, definition, theological, verses, related)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    created += 1

print(f"Created {created} new entries in batch 2!")
print(f"Numbers: {sorted([e[0] for e in entries])}")
