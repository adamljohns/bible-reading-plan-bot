#!/usr/bin/env python3
"""
MOOP Dictionary — full rebuild generator.
Generates all 31 word pages + index.html with:
  - Collapsible Webster / Corruption / Proto-Roots / Greek-Hebrew / Usage sections
  - Always-visible Biblical Definition, Key Scripture, Related Words
  - Full site nav + footer, dark/light toggle
"""
import os, textwrap

DICT_DIR = "/Users/adamjohns/bible-reading-plan-bot/docs/dictionary"

# ── shared pieces ──────────────────────────────────────────────────────────────

NAV = """\
    <nav>
        <a href="../index.html"><img src="../assets/icons/shield-home-48.png" class="site-icon" alt="" width="16" height="16"> Home</a>
        <a href="../watchman.html"><img src="../assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Watchman</a>
        <a href="../bible.html"><img src="../assets/icons/shield-compass.png" class="site-icon" alt="" width="16" height="16"> BTE</a>
        <a href="../lexicon.html"><img src="../assets/icons/shield-alpha-omega-48.png" class="site-icon" alt="" width="16" height="16"> Lexicon</a>
        <a href="../cross-references.html"><img src="../assets/icons/shield-infinity-rope-48.png" class="site-icon" alt="" width="16" height="16"> Cross-Refs</a>
        <a href="index.html" class="active"><img src="../assets/icons/shield-book-greek-48.png" class="site-icon" alt="" width="16" height="16"> Dictionary</a>
        <a href="../blog.html"><img src="../assets/icons/shield-blog-quill-48.png" class="site-icon" alt="" width="16" height="16"> Blog</a>
        <a href="../connect.html"><img src="../assets/icons/shield-handshake.png" class="site-icon" alt="" width="16" height="16"> Connect</a>
        <button class="theme-toggle" onclick="toggleTheme()" id="themeToggle" title="Toggle dark/light">🌙</button>
    </nav>"""

FOOTER = """\
    <footer>
        <div class="cross-divider"><img src="../assets/icons/shield-cross-bible-48.png" alt="" width="36" height="36" style="opacity:0.6;margin-bottom:10px;"></div>
        <p>
            <a href="../index.html#uniting"><img src="../assets/icons/shield-hands-joining.png" class="site-icon" alt="" width="20" height="20"> Uniting</a> &middot;
            <a href="../serving.html"><img src="../assets/icons/shield-serving.png" class="site-icon" alt="" width="20" height="20"> Serving</a> &middot;
            <a href="../mentoring.html"><img src="../assets/icons/shield-mentoring.png" class="site-icon" alt="" width="20" height="20"> Mentoring</a> &middot;
            <a href="../counseling.html"><img src="../assets/icons/shield-family.png" class="site-icon" alt="" width="20" height="20"> Counseling</a> &middot;
            <a href="../about.html"><img src="../assets/icons/shield-about-person-24.png" class="site-icon" alt="" width="20" height="20"> About</a>
        </p>
        <p style="margin-top:8px;font-size:0.78rem;color:#555;">Powered by MOOPbot Pro &mdash; &ldquo;Iron sharpens iron.&rdquo; &mdash; Proverbs 27:17</p>
    </footer>"""

CSS = """\
        * { margin:0; padding:0; box-sizing:border-box; }
        :root { --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }
        body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }
        h1,h2,h3,h4 { font-family:'Playfair Display',serif; }

        /* nav */
        nav { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px;
              border-bottom:1px solid var(--border); position:sticky; top:0;
              background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }
        nav a { color:var(--gray); text-decoration:none; font-size:0.8rem; display:inline-flex; align-items:center;
                gap:3px; padding:3px 6px; border-radius:6px; transition:color 0.2s; }
        nav a:hover, nav a.active { color:var(--gold); }
        .site-icon { vertical-align:middle; opacity:0.8; }
        .theme-toggle { background:none; border:1px solid var(--border); border-radius:50%; width:28px; height:28px;
                        cursor:pointer; font-size:0.85rem; transition:all 0.3s; padding:0; color:var(--white);
                        display:inline-flex; align-items:center; justify-content:center; }
        .theme-toggle:hover { border-color:var(--gold); }

        /* layout */
        .container { max-width:820px; margin:0 auto; padding:28px 20px 60px; }
        .word-header { text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }
        .word-title { font-size:2.8rem; color:var(--gold-light); margin-bottom:6px; }
        .pronunciation { color:var(--gray); font-size:1.1rem; font-style:italic; }
        .pos { display:inline-block; background:var(--gold); color:#000; font-weight:700;
               font-size:0.78rem; padding:3px 14px; border-radius:15px; margin:10px 0; }
        .etymology { color:var(--gray); font-size:0.88rem; margin:12px auto; max-width:650px; }

        /* section cards */
        .section { margin:18px 0; padding:18px 22px; background:var(--card); border:1px solid var(--border); border-radius:10px; }
        .section > h3 { color:var(--gold); margin-bottom:12px; font-size:1.05rem; }
        .section p { margin:7px 0; }
        .biblical-def { border-left:3px solid var(--gold); padding-left:15px; }

        /* collapsibles */
        .dict-toggle { cursor:pointer; color:var(--gold); font-size:0.92rem; user-select:none;
                       display:inline-flex; align-items:center; gap:0; background:none; border:none;
                       padding:0; font-family:inherit; font-weight:600; }
        .dict-toggle:hover { color:var(--gold-light); }
        .dict-toggle .arrow { display:inline-block; transition:transform 0.2s; margin-right:8px; font-size:0.75rem; }
        .dict-toggle .arrow.open { transform:rotate(90deg); }
        .dict-section { display:none; margin:10px 0 4px 0; padding:12px 16px;
                        background:rgba(212,175,55,0.06); border-left:2px solid var(--gold);
                        border-radius:0 6px 6px 0; }
        .dict-section.open { display:block; }
        .dict-section p { margin:6px 0; font-size:0.95rem; }
        .dict-section pre { font-family:'Courier New',monospace; font-size:0.82rem; color:var(--gold-light);
                             line-height:1.7; white-space:pre-wrap; }
        .corruption-box { border-left:3px solid #CC0000; padding-left:14px; }

        /* verses / links */
        .verse-ref { color:var(--gold); text-decoration:none; font-weight:600; }
        .verse-ref:hover { color:var(--gold-light); text-decoration:underline; }
        .lexicon-link { color:var(--gold); font-family:monospace; text-decoration:none; }
        .lexicon-link:hover { color:var(--gold-light); text-decoration:underline; }

        /* related */
        .related { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
        .related a { background:var(--card); border:1px solid var(--border); padding:6px 14px;
                     border-radius:20px; color:var(--white); text-decoration:none; font-size:0.85rem;
                     transition:border-color 0.2s, color 0.2s; }
        .related a:hover { border-color:var(--gold); color:var(--gold); }

        /* footer */
        footer { text-align:center; padding:28px 20px; border-top:1px solid var(--border);
                 margin-top:40px; color:var(--gray); font-size:0.88rem; }
        footer a { color:var(--gray); text-decoration:none; }
        footer a:hover { color:var(--gold); }
        .cross-divider { margin-bottom:10px; }

        /* light mode */
        body.light-mode { --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }
        body.light-mode nav { background:rgba(245,243,239,0.97); }
        body.light-mode .section { background:#fff; border-color:#d4d0c8; }
        body.light-mode .dict-section { background:rgba(212,175,55,0.04); }
        body.light-mode footer { border-top-color:#d4d0c8; }
        body.light-mode .related a { background:#f0ede7; border-color:#d4d0c8; color:#1a1a1a; }"""

JS = """\
    <script>
    function toggleDict(id){
        var s=document.getElementById(id);
        var b=document.querySelector('[data-toggle="'+id+'"]');
        var a=b?b.querySelector('.arrow'):null;
        s.classList.toggle('open');
        if(a)a.classList.toggle('open');
    }
    function toggleTheme(){
        var b=document.body,t=document.getElementById('themeToggle');
        if(b.classList.contains('light-mode')){b.classList.remove('light-mode');t.textContent='🌙';localStorage.setItem('bte-theme','dark');}
        else{b.classList.add('light-mode');t.textContent='☀️';localStorage.setItem('bte-theme','light');}
    }
    (function(){
        if(localStorage.getItem('bte-theme')==='light'){
            document.body.classList.add('light-mode');
            var t=document.getElementById('themeToggle');if(t)t.textContent='☀️';
        }
    })();
    </script>"""

# ── template ───────────────────────────────────────────────────────────────────

def collapsible(toggle_id, label, content_html):
    return f"""\
        <button class="dict-toggle" data-toggle="{toggle_id}" onclick="toggleDict('{toggle_id}')">
            <span class="arrow">&#9658;</span>{label}
        </button>
        <div class="dict-section" id="{toggle_id}">
            {content_html}
        </div>"""

def word_page(word, pronunciation, pos, etymology,
              biblical_def,
              webster, corruption, proto,
              scriptures,   # [(ref_display, url_fragment, snippet), ...]
              roots,        # [(strongs, translit, unicode, desc), ...]
              usage,        # [str, ...]
              related):     # [(label, filename), ...]
    
    scrip_html = "\n".join(
        f'            <p>&#x2022; <a href="../bible.html?ref={u}" class="verse-ref">{r}</a> &mdash; {s}</p>'
        for r, u, s in scriptures
    )
    roots_html = "\n            ".join(
        f'<p><a href="../lexicon/{s}.html" class="lexicon-link">{s}</a> &mdash; <strong>{t}</strong> ({u}): {d}</p>'
        for s, t, u, d in roots
    )
    usage_html = "\n            ".join(f'<p>&#x2022; {ex}</p>' for ex in usage)
    related_html = "\n                ".join(
        f'<a href="{fn}.html">{lbl}</a>' for lbl, fn in related
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{word} &mdash; The MOOP Dictionary</title>
    <style>
{CSS}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
{NAV}
    <div class="container">

        <div class="word-header">
            <div class="word-title">{word}</div>
            <div class="pronunciation">{pronunciation}</div>
            <span class="pos">{pos}</span>
            <div class="etymology">{etymology}</div>
        </div>

        <!-- 1. Biblical Definition — always visible -->
        <div class="section">
            <h3>&#128214; Biblical Definition</h3>
            <div class="biblical-def">
                <p>{biblical_def}</p>
            </div>
        </div>

        <!-- 2. Webster 1828 — collapsible -->
        <div class="section">
            {collapsible("webster", "&#128220; Webster 1828 Definition",
                         f"<p>{webster}</p>")}
        </div>

        <!-- 3. Modern Corruption — collapsible -->
        <div class="section">
            {collapsible("corruption", "&#9888;&#65039; Modern Corruption",
                         f'<div class="corruption-box"><p>{corruption}</p></div>')}
        </div>

        <!-- 4. Proto-Language Roots — collapsible -->
        <div class="section">
            {collapsible("proto", "&#127760; Proto-Language Roots",
                         f"<pre>{proto}</pre>")}
        </div>

        <!-- 5. Key Scripture — always visible -->
        <div class="section">
            <h3>&#128214; Key Scripture</h3>
{scrip_html}
        </div>

        <!-- 6. Greek & Hebrew Roots — collapsible -->
        <div class="section">
            {collapsible("roots", "&#128279; Greek &amp; Hebrew Roots", roots_html)}
        </div>

        <!-- 7. Usage Examples — collapsible -->
        <div class="section">
            {collapsible("usage", "&#9997;&#65039; Usage Examples", usage_html)}
        </div>

        <!-- 8. Related Words — always visible -->
        <div class="section">
            <h3>Related Words</h3>
            <div class="related">
                {related_html}
            </div>
        </div>

    </div>

{FOOTER}
{JS}
</body>
</html>"""

# ── word data ──────────────────────────────────────────────────────────────────

PAGES = {}

# ── ATONEMENT ──────────────────────────────────────────────────────────────────
PAGES["atonement"] = word_page(
  "Atonement", "/&#601;&#712;to&#650;n.m&#601;nt/", "noun",
  'Coined ~1513 from English <em>at one</em> + <em>-ment</em> &mdash; &ldquo;at-one-ment,&rdquo; the state of being reconciled. Translates Hebrew <em>kaphar</em> (&#1499;&#1464;&#1508;&#1463;&#1512;, to cover/propitiate) and Greek <em>hilasmos</em> (&#7985;&#955;&#945;&#963;&#956;&#972;&#962;).',
  'Atonement is the <strong>satisfaction of divine justice through substitutionary sacrifice</strong>, making possible the reconciliation of sinful humanity to a holy God. The Hebrew <em>kaphar</em> (to cover, to make propitiation) is the key OT term &mdash; the Day of Atonement (<em>Yom Kippur</em>) was the annual ritual where the high priest entered the Holy of Holies with blood to cover Israel\'s sins. In the NT, Christ is the final and perfect atonement: &ldquo;He is the propitiation for our sins&rdquo; (1 John 2:2). The atonement satisfies both God\'s justice (sin must be punished) and his love (he provides the sacrifice himself).',
  '<strong>ATONEMENT</strong>, <em>n.</em> 1. Agreement; concord; reconciliation after enmity or controversy. 2. In theology, the expiation of sin made by the obedience and personal suffering of Christ; the reconciliation of God and sinners through the mediatorial and sacrificial work of Christ, by which the demands of the law are satisfied and God is rendered propitious to sinners.',
  'Modern theology often softens atonement into <strong>moral example theory</strong> (Christ merely shows us how to love) or <strong>governmental theory</strong> (God relaxes his law), evacuating the substitutionary core. &ldquo;Penal substitution is cosmic child abuse&rdquo; &mdash; a popular progressive critique &mdash; fundamentally misunderstands the Trinity\'s unity: the Father does not punish an unwilling Son; the Son willingly offers himself (John 10:18). Without penal substitution, there is no actual removal of guilt &mdash; only sentiment.',
  """Unique English coinage (~1513 CE):
  at + one + -ment
    "at one" = in harmony, reconciled (13th-c. Middle English phrase)
    -ment = Latin suffix indicating result or state

This is one of the rare major theological terms coined in English,
not borrowed from Latin or Greek.

Hebrew theological root:
Proto-Semitic *kpr → Hebrew כָּפַר (kaphar, H3722) — to cover, propitiate, atone
  → כַּפֹּרֶת (kapporeth, H3727) — the mercy seat (covering) on the Ark
  → כִּפֻּרִים (kippurim) → יוֹם כִּפֻּרִים (Yom Kippur) — Day of Atonement

Greek:
ἱλάσκομαι (hilaskomai, G2433) — to propitiate, make atonement
ἱλασμός (hilasmos, G2434) — propitiation, atoning sacrifice (1 John 2:2; 4:10)
ἱλαστήριον (hilastērion, G2435) — mercy seat / place of atonement (Rom 3:25)
καταλλαγή (katallagē, G2643) — reconciliation (Rom 5:11)""",
  [("Leviticus 16:30","Leviticus+16:30","The Day of Atonement — annual covering of Israel's sins before God."),
   ("Romans 3:25","Romans+3:25","\"God put forward [Christ] as a propitiation by his blood, to be received by faith.\""),
   ("1 John 2:2","1+John+2:2","\"He is the propitiation for our sins, and not for ours only but also for the sins of the whole world.\""),
   ("Isaiah 53:5","Isaiah+53:5","\"He was pierced for our transgressions... the punishment that brought us peace was on him.\""),
   ("Hebrews 9:22","Hebrews+9:22","\"Without the shedding of blood there is no forgiveness of sins.\"")],
  [("G2434","hilasmos","&#7985;&#955;&#945;&#963;&#956;&#972;&#962;","propitiation, atoning sacrifice; satisfaction of divine justice"),
   ("G2435","hilastērion","&#7985;&#955;&#945;&#963;&#964;&#942;&#961;&#953;&#959;&#957;","mercy seat / place of atonement; used in Rom 3:25 of Christ"),
   ("G2643","katallagē","&#954;&#945;&#964;&#945;&#955;&#955;&#945;&#947;&#942;","reconciliation; restoration of the God-humanity relationship"),
   ("H3722","kaphar","&#1499;&#1464;&#1508;&#1463;&#1512;","to cover, to make atonement, to propitiate; root of Yom Kippur")],
  ['"The tabernacle was a drama of atonement in architectural form: the veil, the altar, the blood — all pointing to Christ."',
   '"Without substitution, atonement is merely a metaphor. Someone must pay. Either we do, or Christ does."',
   '"Yom Kippur is the shadow; the cross is the substance. The high priest entered once a year; Christ entered once for all (Heb 9:12)."'],
  [("Redemption","redemption"),("Salvation","salvation"),("Grace","grace"),("Justification","justification"),("Covenant","covenant")])

# ── BLESSING ──────────────────────────────────────────────────────────────────
PAGES["blessing"] = word_page(
  "Blessing", "/&#712;bl&#603;s.&#618;&#331;/", "noun",
  'Old English <em>bl&#275;tsian</em> (to consecrate with blood); Proto-Germanic <em>*bl&#333;&#240;isojan</em>. Hebrew: <em>berakah</em> (&#1489;&#1468;&#1456;&#1512;&#1464;&#1499;&#1464;&#1492;). Greek: <em>eulogia</em> (&#949;&#8016;&#955;&#959;&#947;&#943;&#945;), <em>makarios</em> (&#956;&#945;&#954;&#940;&#961;&#953;&#959;&#962;).',
  'A blessing is the <strong>authoritative declaration or bestowal of divine favor, fruitfulness, and shalom</strong>. Biblical blessings are not merely pleasant feelings but powerful pronouncements that carry God\'s covenantal favor. To &ldquo;bless&rdquo; in Hebrew (<em>barak</em>) often involves kneeling &mdash; an act of reverence and giving. God blesses humanity with fruitfulness (Gen 1:28), Abraham with a covenant (Gen 12:2), and believers with &ldquo;every spiritual blessing in Christ&rdquo; (Eph 1:3). The Beatitudes redefine blessing as spiritual poverty, mourning, and meekness &mdash; inverting the prosperity paradigm.',
  '<strong>BLESSING</strong>, <em>n.</em> 1. Benediction; a solemn wish for the happiness of another, or prayer for that happiness. 2. Any means of happiness; that which promotes temporal prosperity or secures immortal felicity. 3. Divine favor or the bestowment of God\'s grace. 4. Praise; gratitude; adoration.',
  'Modern usage trivializes blessing into <strong>&ldquo;lucky things happening&rdquo;</strong> &mdash; &ldquo;I\'m so blessed&rdquo; for new cars, promotions, or sunny weather. This reduces the covenantal weight to prosperity-gospel sentimentality. Blessing becomes synonymous with comfort, stripping the Beatitudes of their scandal. Jesus pronounces blessing on the poor, the persecuted, and the mourning &mdash; not the prosperous. The prosperity gospel directly inverts this, treating material wealth as the primary sign of divine favor.',
  """Proto-Germanic *blōðisojan ("to mark or hallow with blood")
  → Old English blētsian / blēdsian ("to consecrate with blood, make sacred")
    → Old English blētsunge (noun)
      → Middle English blessinge
        → Modern English "blessing"

Note: the connection to blood (blōð) reflects ancient consecration ritual —
to "bless" was to set apart with sacrificial blood.
Meaning shifted via Christian influence: blessing = God's grace poured out.

Greek:
εὐλογία (eulogia, G2129) — "well-speaking"
  → eu- (good, well) + logos (word) → to speak good upon someone
μακάριος (makarios, G3107) — "blessed, happy, divinely favored"
  → The Beatitude word; not circumstantial happiness but God's bestowed favor

Biblical parallel:
Proto-Semitic *brk → Hebrew בָּרַךְ (barak, H1288) — to kneel, to bless
  → בְּרָכָה (berakah, H1293) — blessing, benediction, gift
  → בְּרֵכָה (berekhah) — pool, reservoir (blessings overflow like water)""",
  [("Genesis 12:2–3","Genesis+12:2-3","\"I will bless you... and in you all the families of the earth shall be blessed.\""),
   ("Numbers 6:24–26","Numbers+6:24-26","The Aaronic blessing: \"The LORD bless you and keep you...\""),
   ("Matthew 5:3–10","Matthew+5:3-10","The Beatitudes — the counterintuitive blessings of Christ's kingdom."),
   ("Ephesians 1:3","Ephesians+1:3","\"Blessed be... God... who has blessed us in Christ with every spiritual blessing.\""),
   ("Proverbs 10:22","Proverbs+10:22","\"The blessing of the LORD makes rich, and he adds no sorrow with it.\"")],
  [("G2129","eulogia","&#949;&#8016;&#955;&#959;&#947;&#943;&#945;","blessing; speaking good — divine declaration of favor over someone"),
   ("G3107","makarios","&#956;&#945;&#954;&#940;&#961;&#953;&#959;&#962;","blessed; the Beatitude word — divinely favored, spiritually flourishing"),
   ("H1288","barak","&#1489;&#1464;&#1512;&#1463;&#1498;","to kneel, to bless; to bestow divine favor upon"),
   ("H1293","berakah","&#1489;&#1468;&#1456;&#1512;&#1464;&#1499;&#1464;&#1492;","blessing, gift, benediction — the noun form of barak")],
  ['"The Aaronic blessing (Num 6:24–26) was the daily verbal covering of Israel — a priestly act of invoking God\'s face, grace, and peace."',
   '"To bless an enemy (Rom 12:14) is not to approve of their actions but to invoke God\'s favor on them — the ultimate act of spiritual warfare."',
   '"When Abraham was called to bless all nations (Gen 12:3), it was not a promise of cultural niceness but of cosmic redemption through his Seed (Gal 3:16)."'],
  [("Grace","grace"),("Covenant","covenant"),("Joy","joy"),("Peace","peace"),("Gospel","gospel")])

# ── COVENANT ──────────────────────────────────────────────────────────────────
PAGES["covenant"] = word_page(
  "Covenant", "/&#712;k&#652;v.&#601;.n&#601;nt/", "noun / verb",
  'Old French <em>covenant</em> (agreement), from Latin <em>convenire</em> (to come together); PIE <em>*gʷem-</em> ("to step, come"). Hebrew: <em>berit</em> (&#1489;&#1468;&#1456;&#1512;&#1460;&#1497;&#1514;). Greek: <em>diath&#275;k&#275;</em> (&#948;&#953;&#945;&#952;&#942;&#954;&#951;).',
  'A covenant is a <strong>solemn, binding agreement &mdash; often sealed with blood &mdash; that creates a relationship with obligations and promises</strong>. Biblical covenants are not mere contracts between equals; they are initiated by God, who condescends to bind himself by oath to his people. Major covenants: Noahic (Gen 9), Abrahamic (Gen 15, 17), Mosaic (Ex 19–24), Davidic (2 Sam 7), and the New Covenant (Jer 31:31–34; Luke 22:20). The Greek <em>diath&#275;k&#275;</em> is a &ldquo;testament&rdquo; or &ldquo;will&rdquo; &mdash; emphasizing that the New Covenant is enacted through Christ\'s death and is unilaterally guaranteed by God.',
  '<strong>COVENANT</strong>, <em>n.</em> 1. A mutual consent or agreement of two or more persons, to do or forbear some act or thing; a contract. 2. In theology, the covenant of works was made with Adam. The covenant of grace is an agreement between God and man, wherein God promises salvation through faith in Christ, and man trusts in Christ alone for justification.',
  'The word &ldquo;covenant&rdquo; has been largely evacuated from modern discourse, replaced by &ldquo;contract.&rdquo; The difference is profound: a contract binds parties to <em>performance</em>; a covenant binds them to <em>persons</em>. When covenant is reduced to contract, marriage becomes a legal arrangement terminable at will. Modern &ldquo;covenant theology&rdquo; in some circles has also been misused to collapse Israel and the Church in ways that erase the particularity of God\'s promises.',
  """Latin convenire ("to come together, agree, be fitting")
  → con- (together) + venire (to come)
    → PIE *gʷem- ("to step, come, go")

Latin: conventio (agreement), conventus (assembly)
  → Old French covenant / convenant
    → Middle English covenant
      → Modern English "covenant"

English cognates: convention, convenient, convene, venue, advent

Greek:
διαθήκη (diathēkē, G1242) — "testament, will, covenant"
  → dia- (through) + tithēmi (to place, set)
  → Emphasizes unilateral arrangement: one party sets the terms
  → Used in LXX to translate berit — highlighting God's sovereign initiative

Biblical parallel:
Proto-Semitic *bryt → Hebrew בְּרִית (berit, H1285) — covenant, treaty, pact
  → Root *brr possibly means "to cut, select"
  → כָּרַת בְּרִית (karat berit) — "to cut a covenant" (Gen 15:18)
  → Covenants were "cut" through sacrifice — blood sealed the bond""",
  [("Genesis 15:18","Genesis+15:18","\"On that day the LORD made a covenant with Abram...\""),
   ("Jeremiah 31:31–33","Jeremiah+31:31-33","\"I will make a new covenant... I will put my law within them.\""),
   ("Luke 22:20","Luke+22:20","\"This cup that is poured out for you is the new covenant in my blood.\""),
   ("Hebrews 9:15","Hebrews+9:15","\"He is the mediator of a new covenant...\""),
   ("Genesis 9:9–11","Genesis+9:9-11","The Noahic covenant — God's promise never to destroy the earth by flood.")],
  [("G1242","diathēkē","&#948;&#953;&#945;&#952;&#942;&#954;&#951;","covenant, testament, will; a unilateral disposition of terms by the superior party"),
   ("H1285","berit","&#1489;&#1468;&#1456;&#1512;&#1460;&#1497;&#1514;","covenant, treaty, agreement; 'cut' by sacrifice — karat berit")],
  ['"A contract says \'I will if you will.\' A covenant says \'I will, period.\' God\'s covenant with Abraham was sealed while Abraham slept — entirely God\'s initiative (Gen 15)."',
   '"Marriage is a covenant, not a contract — it binds persons, not performances, which is why \'irreconcilable differences\' is not biblical grounds for divorce."',
   '"The entire Bible is structured around covenants: each one advances God\'s redemptive plan, reaching its climax in the New Covenant sealed by Christ\'s blood."'],
  [("Atonement","atonement"),("Redemption","redemption"),("Grace","grace"),("Faith","faith"),("Marriage","marriage")])

# ── FAITH ──────────────────────────────────────────────────────────────────────
PAGES["faith"] = word_page(
  "Faith", "/fe&#618;&#952;/", "noun",
  'Old French <em>feid</em>, Latin <em>fides</em> (trust, confidence); PIE <em>*bheidh-</em> (&ldquo;to trust, confide, persuade&rdquo;). Greek: <em>pistis</em> (&#960;&#943;&#963;&#964;&#953;&#962;). Hebrew: <em>emunah</em> (&#1488;&#1457;&#1502;&#1493;&#1468;&#1504;&#1464;&#1492;).',
  'Faith in Scripture is not blind belief contrary to evidence but <strong>confident trust grounded in the character and promises of God</strong>. Hebrews 11:1 defines it as &ldquo;the substance of things hoped for, the evidence of things not seen&rdquo; &mdash; faith operates as a present reality (<em>hypostasis</em>, substance/assurance) toward future promises. Biblical faith is always <em>relational</em>: trust directed toward a personal God who has acted in history. It is inseparable from faithfulness &mdash; <em>emunah</em> in Hebrew encompasses both belief and the loyal obedience that flows from it. James makes clear that saving faith is never inert: &ldquo;faith without works is dead&rdquo; (Jas 2:26).',
  '<strong>FAITH</strong>, <em>n.</em> 1. Belief; the assent of the mind to the truth of what is declared by another, resting on his authority and veracity. 2. Evangelical, justifying, or saving faith, is the assent of the mind to the truth of divine revelation, on the authority of God\'s testimony, accompanied with a cordial assent of the will and entire confidence in God\'s character and declarations. 3. Faithfulness; fidelity; a strict adherence to duty and fulfillment of promises.',
  'Modern usage often treats faith as <strong>subjective feeling divorced from truth</strong> &mdash; a personal belief system that demands no evidence and admits no critique. &ldquo;That\'s just your faith&rdquo; dismisses biblical claims as private opinion. The prosperity gospel corrupts faith into a transaction: believe hard enough and God must deliver. Secular thought defines faith as &ldquo;belief without evidence&rdquo; &mdash; when in fact Scripture presents faith as <em>trust</em> grounded in what God has historically demonstrated (1 Cor 15:1–8).',
  """PIE *bheidh- ("to trust, confide, persuade")
  → Latin fīdō ("to trust") → fides ("faith, trust, reliability")
    → Old French feid / feit
      → Middle English feith
        → Modern English "faith"

Latin derivatives: fidelity, confide, federal, affidavit, bona fide

Greek (separate root):
PIE *bheydh- → Greek πείθω (peithō, "to persuade")
  → πίστις (pistis, G4102) — trust, faithfulness, the body of belief ("the faith")

Biblical parallel:
Proto-Semitic *ʾmn → Hebrew אָמַן (aman, "to be firm, reliable, sure")
  → אֱמוּנָה (emunah, H530) — steadfastness, faithfulness, fidelity
  → אָמֵן (amen) — "truly, firmly, so be it" — the world's most universal word""",
  [("Hebrews 11:1","Hebrews+11:1","\"Now faith is the substance of things hoped for, the evidence of things not seen.\""),
   ("Romans 10:17","Romans+10:17","\"Faith comes from hearing, and hearing through the word of Christ.\""),
   ("Ephesians 2:8–9","Ephesians+2:8-9","\"For by grace you have been saved through faith... it is the gift of God.\""),
   ("James 2:26","James+2:26","\"As the body apart from the spirit is dead, so also faith apart from works is dead.\""),
   ("Habakkuk 2:4","Habakkuk+2:4","\"The righteous shall live by his faith.\" (Quoted in Rom 1:17, Gal 3:11, Heb 10:38)")],
  [("G4102","pistis","&#960;&#943;&#963;&#964;&#953;&#962;","faith, trust, belief; also the body of Christian doctrine ('the faith')"),
   ("G4100","pisteuō","&#960;&#953;&#963;&#964;&#949;&#973;&#969;","to believe, to trust, to commit oneself to"),
   ("H530","emunah","&#1488;&#1457;&#1502;&#1493;&#1468;&#1504;&#1464;&#1492;","steadiness, faithfulness, fidelity; from aman (to be firm, reliable, trustworthy)")],
  ['"Faith is not the absence of doubt but the choice to trust God through it — every hero of Hebrews 11 acted before they received."',
   '"Abraham\'s faith was credited as righteousness not because he felt confident, but because he obeyed — faith and faithfulness are two sides of the same coin."',
   '"To say \'have faith\' in modern usage often means \'stop thinking\'; the biblical call is to think rightly about what God has promised and act accordingly."'],
  [("Grace","grace"),("Hope","hope"),("Righteousness","righteousness"),("Justification","justification"),("Truth","truth")])

# ── FAMILY ──────────────────────────────────────────────────────────────────────
PAGES["family"] = word_page(
  "Family", "/&#712;f&#230;m.&#618;.li/", "noun",
  'Latin <em>familia</em> (household, including servants); from <em>famulus</em> (servant). Greek: <em>oikos</em> (&#959;&#7990;&#954;&#959;&#962;, household). Hebrew: <em>mishpachah</em> (&#1502;&#1460;&#1513;&#1456;&#1468;&#1508;&#1464;&#1495;&#1464;&#1492;, clan/kindred).',
  'The family is <strong>God\'s first institution</strong> &mdash; established before the fall, before government, before the church. From one man and one woman (Gen 2:24), God designed the family as the irreducible unit of human society: the school of virtue, the nursery of faith, and the image of Trinitarian relationship. The household (<em>oikos</em>) in the NT extends to the &ldquo;household of God&rdquo; (1 Tim 3:15) &mdash; the church as extended family. Children are to be raised &ldquo;in the discipline and instruction of the Lord&rdquo; (Eph 6:4); fathers are to lead, not provoke.',
  '<strong>FAMILY</strong>, <em>n.</em> 1. The collective body of persons who live in one house and under one head; a household. 2. Those who descend from one common progenitor; a tribe or race. 3. Honorable descent; noble or respectable stock. 4. In its fullest sense, the father, mother, and children together under God\'s order.',
  'The redefinition of family is perhaps the most aggressive linguistic revolution of our time. &ldquo;Family&rdquo; now means <strong>any self-defined relational unit</strong>, detached from biology, marriage, or covenant commitment. The state increasingly positions itself as the ultimate family, contesting education, values, and religious formation. The resulting &ldquo;family&rdquo; is whatever individuals consent to, with no reference to God\'s design or children\'s developmental needs.',
  """Latin familia ("household, family, servants")
  → famulus ("servant, household slave")
    → PIE root possibly related to *dhē- ("to set, place")

The original Latin familia included ALL household members:
husband, wife, children, slaves, freedmen — a social unit under one authority.

Old French famille → borrowed into English ~15th century
  → Modern English "family"

Greek:
οἶκος (oikos, G3624) — house, household, family
  → οἰκονομία (oikonomia) — household management → "economy"
  → οἰκουμένη (oikoumenē) — the inhabited world
  → ἐκκλησία (ekklēsia) built on oikos metaphor — church as God's household

Biblical parallel:
Proto-Semitic *šph → Hebrew מִשְׁפָּחָה (mishpachah, H4940) — clan, kindred, family
  → בֵּית אָב (beit av) — "father's house" — the primary OT family unit
  → אָב (av, H1) — father → the foundational authority""",
  [("Genesis 2:24","Genesis+2:24","\"Therefore a man shall leave his father and mother and hold fast to his wife, and they shall become one flesh.\""),
   ("Deuteronomy 6:6–7","Deuteronomy+6:6-7","\"You shall teach [these words] diligently to your children...\""),
   ("Ephesians 6:1–4","Ephesians+6:1-4","Children obey, fathers do not provoke — the family order in Christ."),
   ("Psalm 128:3","Psalm+128:3","\"Your wife will be like a fruitful vine... your children like olive shoots around your table.\""),
   ("1 Timothy 3:4–5","1+Timothy+3:4-5","An elder must manage his own household well — family health is a leadership qualification.")],
  [("G3624","oikos","&#959;&#7990;&#954;&#959;&#962;","house, household, family; extended to the church as God's household"),
   ("H4940","mishpachah","&#1502;&#1460;&#1513;&#1456;&#1468;&#1508;&#1464;&#1495;&#1464;&#1492;","clan, family, kindred — the extended family unit in Israel's social structure"),
   ("H1","av","&#1488;&#1464;&#1489;","father; the foundational authority in the OT household")],
  ['"The family is the first government, the first church, and the first school — when it fails, every other institution strains to compensate."',
   '"God himself is defined in familial terms: Father, Son — the Trinity is the original family, and human families image it."',
   '"\'Honor your father and mother\' is the first commandment with a promise — family fidelity is the seedbed of societal flourishing (Eph 6:2–3)."'],
  [("Marriage","marriage"),("Covenant","covenant"),("Honor","honor"),("Blessing","blessing"),("Wisdom","wisdom")])

# ── FREEDOM ──────────────────────────────────────────────────────────────────────
PAGES["freedom"] = word_page(
  "Freedom", "/&#712;fri&#720;.d&#601;m/", "noun",
  'Old English <em>fr&#275;od&#333;m</em>; from <em>fr&#275;o</em> (free, beloved) + <em>-d&#333;m</em> (state); Proto-Germanic <em>*frijaz</em>; PIE <em>*preyH-</em> (&ldquo;to love, hold dear&rdquo;). Greek: <em>eleutheria</em> (&#949;&#955;&#949;&#965;&#952;&#949;&#961;&#943;&#945;). Hebrew: <em>dror</em> (&#1491;&#1456;&#1512;&#1493;&#1465;&#1512;).',
  'Biblical freedom is not the modern ideal of <strong>freedom from all constraint</strong> but freedom <em>for flourishing</em> within God\'s design. The Exodus is the paradigmatic freedom story: Israel is liberated from Egypt not to do whatever they please, but to serve God and receive his law (Ex 3:12; 19:4–6). Paul articulates the paradox: &ldquo;For freedom Christ has set us free&rdquo; (Gal 5:1), yet this freedom is not license &mdash; &ldquo;do not use your freedom as an opportunity for the flesh&rdquo; (Gal 5:13). True freedom is freedom <em>from</em> sin to serve God and neighbor.',
  '<strong>FREEDOM</strong>, <em>n.</em> 1. A state of exemption from the power or control of another; liberty; exemption from slavery, servitude, or confinement. 2. Power of self-determination; exemption from constraining influence. 3. Frankness; openness; unreservedness. 4. Separation from the power of sin — the highest freedom Scripture describes.',
  'Modern freedom has been radically individualized into <strong>the absolute right to self-definition and self-determination</strong> &mdash; freedom from God, from nature, from community, from tradition. &ldquo;My body, my choice&rdquo; applies this logic to the extreme. This is freedom as rebellion &mdash; precisely what Scripture calls bondage. The irony: the person &ldquo;free&rdquo; from God\'s design is enslaved to appetite, desire, and death (John 8:34). True freedom requires a master &mdash; the question is only which one.',
  """PIE *preyH- ("to love, hold dear, be precious")
  → Proto-Germanic *frijaz ("free, beloved, not enslaved")
    → Old English frēo ("free, noble, glad") — originally "beloved one"
      → Old English frēodōm ("state of being free")
        → Middle English freedom
          → Modern English "freedom"

Key insight: "Free" originally meant "beloved" — free persons were those
loved and belonging to family, as opposed to slaves.
FREEDOM = belonging to one who loves you.

Cognates: free, friend (frēond — "loving one"), Friday (Frīgedæg)

Greek:
ἐλευθερία (eleutheria, G1657) — freedom, liberty
ἐλεύθερος (eleutheros, G1658) — free person, not a slave

Biblical parallel:
Hebrew דְּרוֹר (dror, H1865) — freedom, release, liberty
  → Used in Year of Jubilee proclamations (Lev 25:10)
  → Inscribed on the Liberty Bell: "Proclaim liberty throughout all the land"
Hebrew חָפְשִׁי (chofshi, H2670) — free, released from bondage""",
  [("Galatians 5:1","Galatians+5:1","\"For freedom Christ has set us free; stand firm therefore, and do not submit again to a yoke of slavery.\""),
   ("John 8:36","John+8:36","\"If the Son sets you free, you will be free indeed.\""),
   ("Romans 6:18","Romans+6:18","\"You have been set free from sin and have become slaves of righteousness.\""),
   ("Leviticus 25:10","Leviticus+25:10","The Year of Jubilee — proclaiming liberty throughout the land."),
   ("2 Corinthians 3:17","2+Corinthians+3:17","\"Where the Spirit of the Lord is, there is freedom.\"")],
  [("G1657","eleutheria","&#949;&#955;&#949;&#965;&#952;&#949;&#961;&#943;&#945;","freedom, liberty; the state of the free person in Christ"),
   ("G1658","eleutheros","&#949;&#955;&#949;&#973;&#952;&#949;&#961;&#959;&#962;","free, not a slave; one who belongs to no earthly master"),
   ("H1865","dror","&#1491;&#1456;&#1512;&#1493;&#1465;&#1512;","freedom, release, Jubilee liberty — proclaimed throughout the land")],
  ['"The free person in Rome was not one without obligations, but one who served by choice. Biblical freedom is the same: we are free to serve God."',
   '"\'Free indeed\' (John 8:36) stands against both religious rule-keeping (slavery to law) AND moral anarchy (slavery to sin) — Christ\'s freedom is a third way."',
   '"The Liberty Bell quotation (Lev 25:10) was chosen by the Founders — freedom is theologically grounded in Jubilee, not Enlightenment individualism."'],
  [("Salvation","salvation"),("Redemption","redemption"),("Truth","truth"),("Sin","sin"),("Righteousness","righteousness")])

# ── GLORY ──────────────────────────────────────────────────────────────────────
PAGES["glory"] = word_page(
  "Glory", "/&#712;&#609;l&#596;&#720;r.i/", "noun / verb",
  'Latin <em>gloria</em> (fame, honor, renown); PIE root uncertain, possibly <em>*gʷelH-</em>. Hebrew: <em>kavod</em> (&#1499;&#1468;&#1464;&#1489;&#1493;&#1465;&#1491;, weight/honor). Greek: <em>doxa</em> (&#948;&#972;&#958;&#945;, opinion/splendor).',
  'Glory in Scripture refers to the <strong>manifest weight and splendor of God\'s presence and character</strong>. The Hebrew <em>kavod</em> literally means &ldquo;weight&rdquo; &mdash; glory is the substance of God\'s being made visible. When the glory of God fills the tabernacle (Ex 40:34), the priests cannot stand. The NT declares that Christ is &ldquo;the radiance of God\'s glory&rdquo; (Heb 1:3). The purpose of creation and redemption is God\'s glory: &ldquo;Whether you eat or drink... do all to the glory of God&rdquo; (1 Cor 10:31). Human glory is derivative; God\'s is intrinsic.',
  '<strong>GLORY</strong>, <em>n.</em> 1. Brightness; luster; as the glory of the sun. 2. Splendor; magnificence. 3. The divine perfections, or the exhibition of them. 4. Honor; praise; renown derived from good deeds, talents, or accomplishments. 5. The felicity of heaven prepared for the saints. <em>v.i.</em> To exult with joy; to boast.',
  'Modern usage has flatted glory into <strong>celebrity and self-promotion</strong> &mdash; &ldquo;glory&rdquo; is what athletes achieve, what brands project. Social media is an engine of vainglory: broadcasting self for human applause. Paul\'s warning against &ldquo;vainglory&rdquo; (&#954;&#949;&#957;&#959;&#948;&#959;&#958;&#943;&#945;, kenodoxia &mdash; empty glory) describes our current moment precisely. The prosperity gospel redirects the glory of God toward the comfort and success of believers &mdash; God becomes the means to our glory, reversing the biblical order entirely.',
  """Latin gloria ("fame, renown, praise, glory")
  → Possibly PIE *gʷelH- ("to call out, cry aloud")
  → Old French gloire
    → Middle English glorie
      → Modern English "glory"

Latin cognates: glorify, glorious, inglorious, vainglory

Greek:
δόξα (doxa, G1391) — originally "opinion, expectation" in classical Greek
  → Radically transformed by the LXX: doxa now = "glory, splendor, honor"
  → The translators chose doxa to render Hebrew kavod
  → δοξάζω (doxazō) — to glorify, to honor
  → doxology (doxa + logos = "word of glory/praise")

Biblical parallel:
Proto-Semitic *kbd → Hebrew כָּבֵד (kaved, "to be heavy, weighty")
  → כָּבוֹד (kavod, H3519) — glory, honor, weight
  → כָּבֵד (kaved) — liver (literally "the heavy organ")
  The glory of God = his "weight" — his substantial, undeniable presence""",
  [("Exodus 33:18–23","Exodus+33:18-23","Moses asks to see God's glory — God reveals his goodness and name."),
   ("Isaiah 6:3","Isaiah+6:3","\"Holy, holy, holy is the LORD of hosts; the whole earth is full of his glory.\""),
   ("John 17:22","John+17:22","\"The glory that you have given me I have given to them, that they may be one...\""),
   ("Habakkuk 2:14","Habakkuk+2:14","\"The earth will be filled with the knowledge of the glory of the LORD as the waters cover the sea.\""),
   ("1 Corinthians 10:31","1+Corinthians+10:31","\"Whether you eat or drink, or whatever you do, do all to the glory of God.\"")],
  [("G1391","doxa","&#948;&#972;&#958;&#945;","glory, honor, splendor; radically redefined by the LXX to convey God's weighty presence"),
   ("G1392","doxazō","&#948;&#959;&#958;&#940;&#950;&#969;","to glorify, to honor, to magnify"),
   ("H3519","kavod","&#1499;&#1468;&#1464;&#1489;&#1493;&#1465;&#1491;","glory, honor; literally 'weight' — the substantial, heavy presence of God")],
  ['"The Westminster Shorter Catechism opens: \'What is the chief end of man? To glorify God and enjoy him forever.\' Everything else is commentary."',
   '"Vainglory (kenodoxia) is glory-seeking — performing for human approval instead of living for God\'s. Social media is the cathedral of vainglory."',
   '"The Transfiguration (Matt 17) was a momentary uncovering of the glory Christ always possessed — the disciples saw what he veiled in the incarnation."'],
  [("Holy","holy"),("Worship","worship"),("Honor","honor"),("Truth","truth"),("Gospel","gospel")])

# ── GOSPEL ──────────────────────────────────────────────────────────────────────
PAGES["gospel"] = word_page(
  "Gospel", "/&#712;&#609;&#594;s.p&#601;l/", "noun",
  'Old English <em>g&#333;dspel</em> (&ldquo;good news&rdquo;; <em>g&#333;d</em> = good + <em>spel</em> = narrative). Calque of Latin <em>evangelium</em>, from Greek <em>euangelion</em> (&#949;&#8016;&#945;&#947;&#947;&#941;&#955;&#953;&#959;&#957;): <em>eu-</em> (good) + <em>angelos</em> (messenger).',
  'The gospel is the <strong>announcement of the good news that Jesus Christ &mdash; Son of God &mdash; died for sins, was buried, and was raised on the third day</strong> (1 Cor 15:3–4), accomplishing salvation for all who believe. It is not advice on how to live better or a moral philosophy; it is an announcement of what God has done. The Greek <em>euangelion</em> was used in Roman culture for imperial proclamations of victory &mdash; Paul provocatively applies it to Christ\'s superior victory over sin and death. The gospel is &ldquo;the power of God for salvation&rdquo; (Rom 1:16) &mdash; sufficient and complete. &ldquo;Another gospel&rdquo; is no gospel at all (Gal 1:6–9).',
  '<strong>GOSPEL</strong>, <em>n.</em> 1. The history of the birth, life, actions, death, resurrection, and ascension of Jesus Christ; the glad tidings of salvation through Jesus Christ. 2. The proclamation of the grace of God manifested and pledged in Christ. Gospel is appropriately called good news, being the most joyful tidings ever communicated to man.',
  'The social gospel movement and its contemporary heirs have redefined gospel as <strong>social transformation, economic equality, and political liberation</strong> &mdash; divorcing it from personal sin, substitutionary atonement, and resurrection. &ldquo;The gospel means justice&rdquo; is true in implication but catastrophically incomplete as definition. What Paul calls &ldquo;another gospel&rdquo; (Gal 1:6–9) can look very moral while removing the cross. Moralism, works-righteousness, and therapeutic self-improvement are all false gospels.',
  """Old English gōdspel ("good news, good narrative")
  → gōd ("good") + spel ("saying, tale, message")
    → calque (word-for-word translation) of Latin evangelium

Latin evangelium → Greek εὐαγγέλιον (euangelion)
  → eu- (good, well) + angelos (messenger, angel)
  → euangelion in classical Greek = "reward for good news" or "the good news itself"
  → Used by Roman emperors for victory proclamations (the imperial "gospel")
  → Paul deliberately uses this imperial term for Christ's superior victory

Proto-Germanic *spellam ("story, narrative") → English "spell"

Greek:
εὐαγγέλιον (euangelion, G2098) — the good news, gospel
εὐαγγελίζω (euangelizō, G2097) — to proclaim good news, evangelize
εὐαγγελιστής (euangelistēs, G2099) — evangelist

Biblical parallel:
Hebrew בְּשׂוֹרָה (besorah, H1309) — good news, tidings
  → Isaiah 52:7: "How beautiful... are the feet of him who brings good news (besorah)"
  → The feet of the herald, running ahead of the victorious army""",
  [("1 Corinthians 15:3–4","1+Corinthians+15:3-4","\"Christ died for our sins... was buried... was raised on the third day.\" The gospel in full."),
   ("Romans 1:16","Romans+1:16","\"I am not ashamed of the gospel, for it is the power of God for salvation to everyone who believes.\""),
   ("Isaiah 52:7","Isaiah+52:7","\"How beautiful... are the feet of him who brings good news, who publishes salvation...\""),
   ("Galatians 1:6–9","Galatians+1:6-9","Paul's warning: any other gospel is anathema — accursed."),
   ("Mark 1:14–15","Mark+1:14-15","\"Jesus came... proclaiming the gospel of God... Repent and believe in the gospel.\"")],
  [("G2098","euangelion","&#949;&#8016;&#945;&#947;&#947;&#941;&#955;&#953;&#959;&#957;","gospel, good news; the announcement of Christ's saving work"),
   ("G2097","euangelizō","&#949;&#8016;&#945;&#947;&#947;&#949;&#955;&#943;&#950;&#969;","to proclaim good news, to evangelize"),
   ("H1309","besorah","&#1489;&#1468;&#1456;&#1513;&#1474;&#1493;&#1465;&#1512;&#1464;&#1492;","good news, glad tidings — the OT herald-word Isaiah uses for the coming gospel")],
  ['"The gospel is not good advice — it is good news. Advice says \'do this.\' News says \'this has been done.\' Christ did it."',
   '"In the Roman world, when Caesar won a battle, a herald ran ahead with the euangelion. Paul\'s gospel says: Christ has won the ultimate battle."',
   '"Every false gospel adds something to grace: works, ethnicity, ritual, political alignment. Add anything, and you have no gospel at all (Gal 1:7–9)."'],
  [("Salvation","salvation"),("Redemption","redemption"),("Atonement","atonement"),("Grace","grace"),("Faith","faith")])

# ── GRACE ──────────────────────────────────────────────────────────────────────
PAGES["grace"] = word_page(
  "Grace", "/&#609;re&#618;s/", "noun",
  'Latin <em>gratia</em> (favor, goodwill, thanks); PIE <em>*gwer-</em> (&ldquo;to praise, celebrate&rdquo;). Greek: <em>charis</em> (&#967;&#940;&#961;&#953;&#962;). Hebrew: <em>chen</em> (&#1495;&#1461;&#1503;), <em>chesed</em> (&#1495;&#1462;&#1505;&#1462;&#1491;).',
  'Grace is the <strong>unmerited, freely given favor of God</strong> toward those who deserve wrath. It is not a reward for virtue but the very ground of salvation: &ldquo;For by grace you have been saved through faith &mdash; and this is not your own doing; it is the gift of God&rdquo; (Eph 2:8). The Greek <em>charis</em> carries the idea of a gift that flows from the giver\'s goodness, not the recipient\'s worth. In the OT, <em>chen</em> (favor) appears when God looks upon someone with acceptance. <em>Chesed</em> adds covenant loyalty &mdash; grace is not arbitrary sentimentality but faithful love anchored in covenant relationship.',
  '<strong>GRACE</strong>, <em>n.</em> 1. Favor; good will; kindness; disposition to oblige another. 2. Favorable influence of God; divine favor. 3. The free unmerited love and favor of God, the spring and source of all the benefits men receive from him. 4. A state of acceptance with God; justification. 5. Virtuous or religious affection arising from the divine influence.',
  'Contemporary usage has thinned grace into mere politeness or given it a therapeutic meaning: grace now often means <strong>excusing all behavior without judgment</strong>. &ldquo;Give yourself grace&rdquo; has become cultural shorthand for avoiding accountability. Cheap grace &mdash; Dietrich Bonhoeffer\'s term &mdash; divorces forgiveness from repentance and discipleship. True grace is costly: it required the cross. And it produces obedience, not license (Tit 2:11–12).',
  """PIE *gwer- ("to praise, be grateful, celebrate")
  → Latin gratus ("pleasing, favorable, thankful")
    → Latin gratia ("favor, goodwill, grace, thanks")
      → Old French grace
        → Middle English grace
          → Modern English "grace"

Latin derivatives: gratitude, gratify, gratis, congratulate, ingrate

Greek:
χάρις (charis, G5485) — grace, favor, gift
  → χαρίζομαι (charizomai) — to give freely, to forgive
  → χάρισμα (charisma) — gift of grace
  → χαίρω (chairō) — to rejoice (shares root with charis)
  → The standard Greek greeting "Greetings!" = "Grace to you!"

Biblical parallel:
Proto-Semitic *ḥnn → Hebrew חָנַן (chanan, "to be gracious, show favor")
  → חֵן (chen, H2580) — grace, favor, charm
  → חֶסֶד (chesed, H2617) — steadfast covenant love/grace
  → חַנּוּן (channun) — gracious (divine attribute: Ex 34:6)""",
  [("Ephesians 2:8–9","Ephesians+2:8-9","\"By grace you have been saved through faith — it is the gift of God, not a result of works.\""),
   ("Romans 5:20","Romans+5:20","\"Where sin increased, grace abounded all the more.\""),
   ("Titus 2:11–12","Titus+2:11-12","\"The grace of God has appeared... training us to renounce ungodliness.\""),
   ("2 Corinthians 12:9","2+Corinthians+12:9","\"My grace is sufficient for you, for my power is made perfect in weakness.\""),
   ("John 1:14","John+1:14","\"The Word became flesh... full of grace and truth.\"")],
  [("G5485","charis","&#967;&#940;&#961;&#953;&#962;","grace, favor, gift freely given; the generosity of God toward the undeserving"),
   ("H2580","chen","&#1495;&#1461;&#1503;","grace, favor, charm; finding acceptance in someone's eyes"),
   ("H2617","chesed","&#1495;&#1462;&#1505;&#1462;&#1491;","steadfast lovingkindness; covenant loyalty paired with grace")],
  ['"Grace is not the absence of law but the power to fulfill it — the same Spirit who forgives also transforms."',
   '"You cannot earn grace by definition; the moment you earn it, it becomes wages (Rom 4:4)."',
   '"Bonhoeffer distinguished cheap grace (forgiveness without discipleship) from costly grace (the cross that calls us to die to self)."'],
  [("Mercy","mercy"),("Love","love"),("Salvation","salvation"),("Justification","justification"),("Atonement","atonement")])

# ── HOLY ──────────────────────────────────────────────────────────────────────
PAGES["holy"] = word_page(
  "Holy", "/&#712;ho&#650;.li/", "adjective",
  'Old English <em>h&#257;lig</em>; Proto-Germanic <em>*hailagaz</em> (&ldquo;sacred, of good augury&rdquo;); PIE <em>*kailo-</em> (&ldquo;whole, uninjured&rdquo;). Hebrew: <em>qadosh</em> (&#1511;&#1464;&#1491;&#1493;&#1465;&#1513;&#1473;). Greek: <em>hagios</em> (&#7537;&#947;&#953;&#959;&#962;).',
  'Holiness is the <strong>essential otherness and moral perfection of God</strong> &mdash; the quality by which he is utterly distinct from all creation and absolutely pure from all evil. &ldquo;Holy, holy, holy&rdquo; (Isa 6:3; Rev 4:8) &mdash; the only divine attribute repeated three times &mdash; signals infinite, unmeasured holiness. God\'s holiness is not merely moral perfection but ontological uniqueness: he is in a category entirely his own. For creatures, holiness means being set apart for God\'s purposes and progressively conformed to his character (1 Pet 1:15–16). The call is: &ldquo;Be holy, for I am holy.&rdquo;',
  '<strong>HOLY</strong>, <em>adj.</em> 1. Properly, whole, entire, or perfect, in a moral sense. Hence, pure in heart, temper, or dispositions; free from sin and sinful affections; applied to the Supreme Being. 2. Hallowed; consecrated or set apart to a sacred use. 3. Proceeding from pious principles or directed to pious purposes. 4. Perfectly just and good; as a holy law.',
  'Holiness has been reduced in evangelical culture to <strong>moral rule-keeping</strong> (&ldquo;holy&rdquo; = doesn\'t drink, smoke, or swear) and in progressive culture to an essentially empty concept used casually (&ldquo;holy cow!&rdquo;) or dismissed as judgmental moralism. The deeper corruption is treating holiness as achievable by human effort rather than as God\'s gift &mdash; both legalism (earn it by behavior) and antinomianism (grace means God doesn\'t care about it) distort the biblical picture.',
  """PIE *kailo- ("whole, uninjured, of good omen")
  → Proto-Germanic *hailagaz ("sacred, holy, of good augury")
    → Old English hālig ("holy, consecrated, sacred")
      → Middle English holi / holy
        → Modern English "holy"

Cognates: hale (healthy), whole, heal, health — all from *kailo-
Key insight: "Holy" and "whole" share a root — holiness is wholeness/completeness.
To be holy = to be what God made you to be, without fragmentation or moral corruption.

German cognate: heilig ("holy") → Heil ("salvation, health") — same cluster

Greek:
ἅγιος (hagios, G40) — holy, set apart, sacred; the word for "saint"
  → ἁγιάζω (hagiazō) — to sanctify, make holy
  → ἁγιωσύνη (hagiōsynē) — holiness as a quality/character

Biblical parallel:
Proto-Semitic *qdš → Hebrew קָדַשׁ (qadash, H6942) — to be holy, set apart
  → קָדוֹשׁ (qadosh, H6918) — holy, sacred (adjective)
  → קֹדֶשׁ (qodesh, H6944) — holiness, sanctuary
  → "Set apart" = positively (for God) and negatively (from sin/defilement)""",
  [("Isaiah 6:3","Isaiah+6:3","\"Holy, holy, holy is the LORD of hosts; the whole earth is full of his glory.\""),
   ("Leviticus 11:44","Leviticus+11:44","\"Be holy, for I am holy\" — the foundational call of God to his people."),
   ("1 Peter 1:15–16","1+Peter+1:15-16","\"As he who called you is holy, you also be holy in all your conduct.\""),
   ("Revelation 4:8","Revelation+4:8","The seraphim cry 'Holy, holy, holy' before the throne — eternal worship."),
   ("Hebrews 12:14","Hebrews+12:14","\"Strive for... holiness without which no one will see the Lord.\"")],
  [("G40","hagios","&#7537;&#947;&#953;&#959;&#962;","holy, set apart, sacred; used for God, people, places, and the Spirit"),
   ("G37","hagiazō","&#7537;&#947;&#953;&#940;&#950;&#969;","to sanctify, to make holy, to set apart"),
   ("H6918","qadosh","&#1511;&#1464;&#1491;&#1493;&#1465;&#1513;&#1473;","holy, sacred, set apart — God's defining attribute"),
   ("H6944","qodesh","&#1511;&#1465;&#1491;&#1462;&#1513;&#1473;","holiness, sacredness, the sanctuary itself")],
  ['"The seraphim\'s triple \'Holy\' (Isa 6:3) is not a stutter — in Hebrew, tripling intensifies to the superlative: God is maximally, infinitely, incomparably holy."',
   '"Holiness and wholeness share a root: to be holy is to be what God made you to be, without fragmentation or moral corruption."',
   '"The Holy Spirit does not just help us behave — he is the agent of holiness, the one who unites us to Christ\'s own holiness (Rom 8:9–11)."'],
  [("Sacred","sacred"),("Sanctification","sanctification"),("Worship","worship"),("Glory","glory"),("Righteousness","righteousness")])

# ── HONOR ──────────────────────────────────────────────────────────────────────
PAGES["honor"] = word_page(
  "Honor", "/&#712;&#596;n.&#601;r/", "noun / verb",
  'Latin <em>honor / honos</em> (esteem, reputation, dignity); PIE root uncertain. Hebrew: <em>kavod</em> (&#1499;&#1468;&#1464;&#1489;&#1493;&#1465;&#1491;, weight/glory). Greek: <em>tim&#275;</em> (&#964;&#953;&#956;&#942;, worth/price/honor).',
  'Honor is the <strong>recognition and active attribution of worth to those who bear it by virtue of God\'s design</strong> &mdash; God, parents, rulers, elders, all people as image-bearers. The fifth commandment establishes parental honor as the first social obligation with a promise (Ex 20:12; Eph 6:2). The NT extends honor universally: &ldquo;Honor everyone. Love the brotherhood. Fear God. Honor the emperor&rdquo; (1 Pet 2:17). God is the ultimate source and object of all honor: &ldquo;To the King of ages... be honor and glory&rdquo; (1 Tim 1:17). To honor is to assign the correct weight to the correct person.',
  '<strong>HONOR</strong>, <em>n.</em> 1. The esteem due or paid to worth; high estimation. 2. A testimony of esteem; any expression of respect or high estimation by words or actions. 3. Dignity; exalted rank or place; distinction. 4. Reverence; veneration; as the honor due to the Creator. 5. Reputation; good name. <em>v.t.</em> To revere; to respect; to treat with deference and submission.',
  'Honor culture has been systematically dismantled &mdash; &ldquo;question authority&rdquo; became the supreme virtue of modernity. Honor is now often contingent on personal agreement: we honor those we approve of and cancel those we don\'t. <strong>Performative honor</strong> (awards shows, social media praise) has replaced genuine honor based on virtue and character. The commandment to honor parents regardless of how &ldquo;validating&rdquo; they are strikes the modern ear as oppressive.',
  """Latin honor / honos ("esteem, dignity, office, reputation")
  → PIE root uncertain; possibly *ono- or related to *en- (to honor)
  → Old French onor / honor
    → Middle English honor
      → Modern English "honor"

Latin derivatives: honorable, honorary, dishonor, honorarium

Greek:
τιμή (timē, G5092) — honor, price, value, worth
  → From τίω (tiō, "to honor, esteem, pay")
  → τιμάω (timaō, G5091) — to honor, to value, to set a price on
  → Related: timocracy (rule by honor), Timothy (τιμή + θεός = "honoring God")
  → ἄτιμος (atimos) — without honor, dishonored (Mark 6:4 — prophet in hometown)

Biblical parallel:
Proto-Semitic *kbd → Hebrew כָּבֵד (kaved, "to be heavy")
  → כָּבוֹד (kavod, H3519) — glory, honor, weight
  → כַּבֵּד (kabbēd) — to honor, to give weight to
  The same root as "glory" — to honor someone is to give them their proper weight""",
  [("Exodus 20:12","Exodus+20:12","\"Honor your father and your mother, that your days may be long in the land...\""),
   ("1 Peter 2:17","1+Peter+2:17","\"Honor everyone. Love the brotherhood. Fear God. Honor the emperor.\""),
   ("Romans 12:10","Romans+12:10","\"Love one another with brotherly affection. Outdo one another in showing honor.\""),
   ("Proverbs 3:9","Proverbs+3:9","\"Honor the LORD with your wealth and with the firstfruits of all your produce.\""),
   ("John 5:23","John+5:23","\"Whoever does not honor the Son does not honor the Father who sent him.\"")],
  [("G5092","timē","&#964;&#953;&#956;&#942;","honor, price, value; the worth attributed to a person or thing"),
   ("G5091","timaō","&#964;&#953;&#956;&#940;&#969;","to honor, to value, to esteem; used for honoring parents, God, rulers"),
   ("H3519","kavod","&#1499;&#1468;&#1464;&#1489;&#1493;&#1465;&#1491;","glory, honor, weight — honoring someone is assigning them their proper weight")],
  ['"To honor is not to agree or approve — it is to assign the correct worth. We can honor a flawed parent while not endorsing their failures."',
   '"Honor structures are load-bearing walls of society: remove them and everything collapses. Judges and Romans 1 both end in the same place."',
   '"The command \'outdo one another in showing honor\' (Rom 12:10) is a competitive pursuit of humility — the exact inversion of our culture\'s competition for status."'],
  [("Glory","glory"),("Humility","humility"),("Family","family"),("Worship","worship"),("Virtue","virtue")])

# ── HOPE ──────────────────────────────────────────────────────────────────────
PAGES["hope"] = word_page(
  "Hope", "/ho&#650;p/", "noun / verb",
  'Old English <em>hopian</em> (to hope); Proto-Germanic <em>*hup&#333;&#331;</em> (to leap up, spring). Greek: <em>elpis</em> (&#949;&#955;&#960;&#943;&#962;, expectation). Hebrew: <em>tikvah</em> (&#1514;&#1460;&#1511;&#1456;&#1493;&#1464;&#1492;, cord/expectation), <em>qavah</em> (to wait for).',
  'Biblical hope is not optimistic wishing but <strong>confident expectation grounded in God\'s promises and character</strong>. The Greek <em>elpis</em> in secular usage could mean uncertain expectation; the NT fills it with certainty: hope is an &ldquo;anchor of the soul, sure and steadfast&rdquo; (Heb 6:19). The Hebrew <em>tikvah</em> literally means &ldquo;cord&rdquo; &mdash; hope is what you hang by, your lifeline. Hope is directed toward the resurrection, the return of Christ, and the new creation: &ldquo;We are saved in this hope&rdquo; (Rom 8:24). Paul\'s triad &mdash; faith, hope, love &mdash; places hope as the forward-looking dimension of the Christian life.',
  '<strong>HOPE</strong>, <em>n.</em> 1. A desire of some good, accompanied with at least a slight expectation of obtaining it. 2. Confidence in a future event; the highest degree of well-founded expectation of good. 3. Trust; reliance on Christ\'s merits for salvation. <em>v.i.</em> To cherish a desire of good with some expectation of obtaining it.',
  'Modern hope is <strong>thin optimism</strong> &mdash; &ldquo;I hope it works out&rdquo; &mdash; entirely contingent on circumstances. Without transcendent grounding, hope collapses into wishful thinking at best and nihilism when circumstances fail. &ldquo;Hope and change&rdquo; as political slogan revealed the bankruptcy: hope projected onto a politician. The prosperity gospel corrupts hope into expectation of earthly blessings &mdash; when suffering comes, hope shatters because it was misplaced. Biblical hope is strongest in suffering (Rom 5:3–5) because it is grounded in the resurrection, not present comfort.',
  """Proto-Germanic *hupōną ("to leap up, spring forward")
  → Old English hopian ("to hope, trust, expect")
    → Middle English hope
      → Modern English "hope"

Root image: leaping forward in anticipation — kinetic, forward-straining hope.
Dutch: hopen, German: hoffen (same root family)

Greek:
ἐλπίς (elpis, G1680) — hope, expectation
  → In classical Greek: could be good or bad expectation
  → In NT: consistently positive — confident expectation of God's promises
  → ἐλπίζω (elpizō, G1679) — to hope, to expect, to trust

Biblical parallel:
Proto-Semitic *qwy → Hebrew קָוָה (qavah, H6960) — to wait for, to hope
  → The root image: straining of a rope or cord under tension
  → תִּקְוָה (tikvah, H8615) — hope, cord, expectation
  → Israel's national anthem is "Hatikvah" (The Hope) — a nation built on hope
Also: יָחַל (yachal, H3176) — to wait, hope with patience
      בָּטַח (batach, H982) — to trust, feel secure (confident hope)""",
  [("Romans 5:3–5","Romans+5:3-5","Suffering → endurance → character → hope — and hope does not disappoint."),
   ("Hebrews 6:19","Hebrews+6:19","\"We have this as a sure and steadfast anchor of the soul, a hope that enters into the inner place behind the curtain.\""),
   ("Romans 8:24–25","Romans+8:24-25","\"In this hope we were saved. Now hope that is seen is not hope... we wait for it with patience.\""),
   ("Lamentations 3:21–23","Lamentations+3:21-23","\"This I call to mind, and therefore I have hope: The steadfast love of the LORD never ceases.\""),
   ("1 Peter 1:3","1+Peter+1:3","\"He has caused us to be born again to a living hope through the resurrection of Jesus Christ from the dead.\"")],
  [("G1680","elpis","&#949;&#955;&#960;&#943;&#962;","hope, confident expectation; the forward dimension of faith"),
   ("H8615","tikvah","&#1514;&#1460;&#1511;&#1456;&#1493;&#1464;&#1492;","hope, expectation; also means 'cord' — hope as lifeline"),
   ("H6960","qavah","&#1511;&#1464;&#1493;&#1464;&#1492;","to wait for, to hope; implies straining toward something with earnest expectation")],
  ['"Biblical hope is not \'I hope so\' but \'I know it will be so, because God said so.\' The resurrection is the down payment on every promise."',
   '"Israel\'s national anthem is \'Hatikvah\' — The Hope. That a persecuted people built a nation on hope is a living parable of Romans 5."',
   '"\'We rejoice in our sufferings\' (Rom 5:3) is only possible if hope is anchored outside circumstance — in the character and promises of God."'],
  [("Faith","faith"),("Joy","joy"),("Salvation","salvation"),("Redemption","redemption"),("Love","love")])

# ── HUMILITY ──────────────────────────────────────────────────────────────────
PAGES["humility"] = word_page(
  "Humility", "/hju&#720;&#712;m&#618;l.&#618;.ti/", "noun",
  'Latin <em>humilitas</em> (lowness, abasement); from <em>humilis</em> (on the ground, low); from <em>humus</em> (earth); PIE <em>*dhghem-</em> (earth). Greek: <em>tapeinophrosy&#772;n&#275;</em> (&#964;&#945;&#960;&#949;&#953;&#957;&#959;&#966;&#961;&#959;&#963;&#973;&#957;&#951;). Hebrew: <em>anavah</em> (&#1506;&#1458;&#1504;&#1464;&#1493;&#1464;&#1492;).',
  'Humility is <strong>the accurate assessment of oneself in relation to God and others</strong> &mdash; neither self-deprecation nor false modesty, but honest recognition of one\'s creaturely dependence and God\'s infinite greatness. Christ is the supreme model: &ldquo;Though he was in the form of God... he humbled himself&rdquo; (Phil 2:6–8). Proverbs declares that &ldquo;pride goes before destruction&rdquo; and &ldquo;with the humble is wisdom&rdquo; (11:2). James and Peter both cite Proverbs 3:34: &ldquo;God opposes the proud but gives grace to the humble.&rdquo; Humility is the prerequisite for every other virtue &mdash; the soil in which they grow.',
  '<strong>HUMILITY</strong>, <em>n.</em> 1. In ethics, freedom from pride and arrogance; humbleness of mind; a modest estimate of one\'s own worth. 2. Lowliness of mind; a sense of one\'s own unworthiness, and submission to God. Christian humility consists in a deep sense of our own unworthiness in the sight of God, a conviction that our merits are nothing.',
  'Modernity prizes <strong>self-confidence, assertiveness, and self-esteem</strong> as cardinal virtues &mdash; humility is reframed as weakness, doormat behavior, or imposter syndrome. Therapeutic culture pathologizes low self-esteem while actually reinforcing narcissism: the cure for shame is not humility but pride. True humility, as C.S. Lewis noted, is not thinking less of yourself; it is thinking of yourself less.',
  """PIE *dhghem- ("earth, ground")
  → Latin humus ("earth, soil, ground")
    → Latin humilis ("on the ground, low, base, humble")
      → Latin humilitas ("lowness, smallness, humility")
        → Old French humilité
          → Middle English humilite
            → Modern English "humility"

Cognates: humus, exhume, human (homo from humus — "earthling")
Theological insight: to be humble = to remember you are dust (Gen 3:19)

Greek:
ταπεινός (tapeinos, G5011) — lowly, humble, of low position
  → ταπεινόω (tapeinoō, G5013) — to humble, to bring low
  → ταπεινοφροσύνη (tapeinophrosynē, G5012) — humility of mind
    → tapeinos + phronein (to think) = "lowly-minded"

Biblical parallel:
Proto-Semitic *ʿny → Hebrew עָנָו (anav, H6035) — humble, poor, afflicted
  → עֲנָוָה (anavah, H6038) — humility, meekness, gentleness
  → שָׁפַל (shaphal, H8213) — to be low, to humble oneself
  Moses described as the most humble man on earth (Num 12:3)""",
  [("Philippians 2:3–8","Philippians+2:3-8","Christ's self-emptying is the model of humility — from the form of God to the cross."),
   ("Proverbs 11:2","Proverbs+11:2","\"When pride comes, then comes disgrace, but with the humble is wisdom.\""),
   ("James 4:6","James+4:6","\"God opposes the proud but gives grace to the humble.\""),
   ("Matthew 5:5","Matthew+5:5","\"Blessed are the meek, for they shall inherit the earth.\""),
   ("Matthew 18:4","Matthew+18:4","\"Whoever humbles himself like this child is the greatest in the kingdom of heaven.\"")],
  [("G5012","tapeinophrosynē","&#964;&#945;&#960;&#949;&#953;&#957;&#959;&#966;&#961;&#959;&#963;&#973;&#957;&#951;","humility of mind; lowly thinking about oneself in relation to God and others"),
   ("G5013","tapeinoō","&#964;&#945;&#960;&#949;&#953;&#957;&#972;&#969;","to humble, to bring low; used of Christ's condescension and our call to self-abasement"),
   ("H6038","anavah","&#1506;&#1458;&#1504;&#1464;&#1493;&#1464;&#1492;","humility, meekness, gentleness — the virtue of the anav (humble/poor)")],
  ['"C.S. Lewis: \'Humility is not thinking less of yourself; it is thinking of yourself less.\' Self-forgetfulness, not self-deprecation."',
   '"The incarnation is the supreme act of humility: the infinite became finite, the eternal became temporal, the Lord became servant."',
   '"\'God opposes the proud\' (Jas 4:6) — not just ignores or overlooks but actively resists. Pride makes God your opponent. Humility makes him your ally."'],
  [("Honor","honor"),("Virtue","virtue"),("Wisdom","wisdom"),("Peace","peace"),("Grace","grace")])

# ── JOY ──────────────────────────────────────────────────────────────────────
PAGES["joy"] = word_page(
  "Joy", "/d&#658;&#596;&#618;/", "noun",
  'Old French <em>joie</em>; Latin <em>gaudium</em> (delight, joy); PIE <em>*g&#257;u-</em> (&ldquo;to rejoice&rdquo;). Greek: <em>chara</em> (&#967;&#945;&#961;&#940;). Hebrew: <em>simchah</em> (&#1513;&#1460;&#1502;&#1456;&#1495;&#1464;&#1492;), <em>sason</em> (&#1513;&#1464;&#1474;&#1513;&#1464;&#1474;&#1493;&#1503;).',
  'Joy in Scripture is <strong>deep, stable gladness rooted in the reality of God\'s presence and promises</strong> &mdash; distinct from happiness, which is circumstantially dependent. The Greek <em>chara</em> shares a root with <em>charis</em> (grace) &mdash; joy is the response to grace. Paul commands joy in the imperative (&ldquo;Rejoice in the Lord always&rdquo; &mdash; Phil 4:4), which means it is a choice, not merely a feeling. The &ldquo;joy of the LORD is your strength&rdquo; (Neh 8:10). Paradoxically, joy is found in suffering (Jas 1:2–3), in prison (Acts 16:25), and at the cross (Heb 12:2) &mdash; because it is grounded in resurrection reality, not present circumstance.',
  '<strong>JOY</strong>, <em>n.</em> 1. The passion or emotion excited by the acquisition or expectation of good; that excitement of pleasurable feelings which is caused by success, good fortune, or the gratification of desire; gladness; exultation. 2. The cause of joy or happiness. 3. That which causes gladness. <em>v.i.</em> To rejoice; to exult.',
  'Popular culture conflates joy with <strong>happiness, positivity, and good vibes</strong> &mdash; and &ldquo;toxic positivity&rdquo; is the ironic result: you must perform joy at all times or you\'re being negative. Therapeutic culture treats sadness as pathology to be managed. The prosperity gospel promises joy as a sign of God\'s blessing, which means suffering Christians are implicitly failures. The biblical picture is far richer: lament is holy (the Psalms are 40% lament), grief is appropriate (Eccl 3:4), and joy coexists with mourning in the already/not-yet tension of Christian life.',
  """PIE *gāu- ("to rejoice, to be glad")
  → Latin gaudēre ("to rejoice") → gaudium ("joy, delight")
    → Old French joie
      → Middle English joie
        → Modern English "joy"

Latin derivatives: gaudy (originally "jubilant, joyful" — now means garish), enjoy, rejoice
Note: "gaudy" once meant joyfully bright — a testimony to how words corrupt over time.

Greek:
χαρά (chara, G5479) — joy, delight, gladness
  → Shares root with χάρις (charis, grace) — joy as response to grace
  → χαίρω (chairō, G5463) — to rejoice, to be glad
  → The greeting "Rejoice!" (chairō) is the standard Greek salutation (Matt 28:9)

Biblical parallel:
Proto-Semitic *śmḥ → Hebrew שָׂמַח (samach, H8055) — to rejoice, be glad
  → שִׂמְחָה (simchah, H8057) — joy, gladness, mirth
  → שָׂשׂוֹן (sason, H8342) — exultation, great joy (more intense)
  → גִּיל (gil, H1523) — to exult, rejoice — often associated with the messianic era""",
  [("Philippians 4:4","Philippians+4:4","\"Rejoice in the Lord always; again I will say, rejoice.\" (Written from prison.)"),
   ("Nehemiah 8:10","Nehemiah+8:10","\"The joy of the LORD is your strength.\""),
   ("James 1:2–3","James+1:2-3","\"Count it all joy, my brothers, when you meet trials of various kinds...\""),
   ("Hebrews 12:2","Hebrews+12:2","Jesus endured the cross for the joy set before him."),
   ("John 15:11","John+15:11","\"These things I have spoken to you, that my joy may be in you, and that your joy may be full.\"")],
  [("G5479","chara","&#967;&#945;&#961;&#940;","joy, gladness; shares a root with charis (grace) — joy as gift and response"),
   ("G5463","chairō","&#967;&#945;&#943;&#961;&#969;","to rejoice, to be glad; also the standard Greek greeting"),
   ("H8057","simchah","&#1513;&#1460;&#1502;&#1456;&#1495;&#1464;&#1492;","joy, gladness, mirth; the most common OT joy word"),
   ("H8342","sason","&#1513;&#1464;&#1474;&#1513;&#1464;&#1474;&#1493;&#1503;","exultation, great joy — intense, often eschatological rejoicing")],
  ['"\'Rejoice always\' (1 Thess 5:16) is the shortest verse in the Greek NT — three words, an absolute command. Joy is not optional for the Christian."',
   '"Joy coexists with sorrow: \'sorrowful, yet always rejoicing\' (2 Cor 6:10) — the paradox of already/not-yet Christian life."',
   '"The angels\' announcement at the nativity: \'Fear not... I bring you good news of great joy\' (Luke 2:10) — joy is the proper response to the gospel."'],
  [("Peace","peace"),("Hope","hope"),("Love","love"),("Blessing","blessing"),("Grace","grace")])

# ── JUSTIFICATION ─────────────────────────────────────────────────────────────
PAGES["justification"] = word_page(
  "Justification", "/&#716;d&#658;&#652;s.t&#618;.f&#618;&#712;ke&#618;.&#643;&#601;n/", "noun",
  'Latin <em>iustificatio</em> (act of rendering just); from <em>iustus</em> (just) + <em>facere</em> (to make). Greek: <em>dikaiōsis</em> (&#948;&#953;&#954;&#945;&#943;&#969;&#963;&#953;&#962;). Hebrew concept: <em>tsaddiq</em> (&#1510;&#1463;&#1491;&#1468;&#1460;&#1497;&#1511;), <em>tsedaqah</em> (&#1510;&#1456;&#1491;&#1464;&#1511;&#1464;&#1492;).',
  'Justification is God\'s forensic declaration that a sinner is <strong>righteous in his sight, on the basis of Christ\'s righteousness credited to the believer through faith</strong>. It is not making righteous (that is sanctification) but declaring righteous &mdash; a legal verdict of &ldquo;not guilty.&rdquo; Paul\'s argument in Romans 3–5: all have sinned (3:23), but God justifies the ungodly (4:5) through the redemption in Christ (3:24), received by faith alone (3:28). God is simultaneously &ldquo;just and the justifier&rdquo; (3:26) &mdash; the cross satisfies divine justice while extending divine mercy. This is the article on which the church stands or falls (Luther).',
  '<strong>JUSTIFICATION</strong>, <em>n.</em> 1. The act of justifying; a showing to be just or conformable to law and rectitude. 2. In theology, the act of God\'s free grace by which he pardons all our sins and accepts us as righteous in his sight, only for the righteousness of Christ imputed to us, and received by faith alone. Not by works of the law, but by faith in Christ.',
  'Two modern corruptions: (1) <strong>Justification by works</strong> &mdash; still the default human religion, believing God accepts us based on our moral improvement or religious effort. (2) <strong>Universalism / therapeutic justification</strong> &mdash; everyone is already justified because God is love, repentance is unnecessary, and hell is empty. Both errors miss the forensic reality: sin is real, justice requires satisfaction, and Christ is the only ground on which God can declare the guilty &ldquo;not guilty&rdquo; without compromising his own righteousness.',
  """Latin iustus ("just, righteous, lawful") + facere ("to make, do")
  → iustificare ("to justify, make just, show to be just")
    → Late Latin iustificatio ("the act of justifying")
      → Old French justification
        → Middle English justificacion
          → Modern English "justification"

Latin root: ius / iuris ("law, right, justice") → justice, judicial, jury, juridical

Greek:
δικαιόω (dikaioō, G1344) — to justify, declare righteous
  → δικαίωσις (dikaiōsis, G1347) — justification (the act/result)
  → δίκαιος (dikaios, G1342) — righteous, just
  → δικαιοσύνη (dikaiosynē, G1343) — righteousness
  The entire δικ- (dik-) word family from *dike (justice, custom, right)

Biblical parallel:
Proto-Semitic *ṣdq → Hebrew צָדַק (tsadak, H6663) — to be righteous, to justify
  → צַדִּיק (tsaddiq, H6662) — righteous one, just person
  → צְדָקָה (tsedaqah, H6666) — righteousness, justice, justification""",
  [("Romans 3:21–26","Romans+3:21-26","The masterwork: God justifies the ungodly through Christ's blood — just and justifier."),
   ("Romans 5:1","Romans+5:1","\"Therefore, since we have been justified by faith, we have peace with God through our Lord Jesus Christ.\""),
   ("Galatians 2:16","Galatians+2:16","\"A person is not justified by works of the law but through faith in Jesus Christ.\""),
   ("Romans 4:5","Romans+4:5","\"To the one who... believes in him who justifies the ungodly, his faith is counted as righteousness.\""),
   ("Romans 8:30","Romans+8:30","The golden chain: foreknew → predestined → called → justified → glorified.")],
  [("G1344","dikaioō","&#948;&#953;&#954;&#945;&#953;&#972;&#969;","to justify, declare righteous; a forensic/legal declaration, not moral transformation"),
   ("G1347","dikaiōsis","&#948;&#953;&#954;&#945;&#943;&#969;&#963;&#953;&#962;","justification — the act by which God declares sinners righteous"),
   ("G1343","dikaiosynē","&#948;&#953;&#954;&#945;&#953;&#959;&#963;&#973;&#957;&#951;","righteousness — the quality imputed to the believer in justification"),
   ("H6663","tsadak","&#1510;&#1464;&#1491;&#1463;&#1511;","to be righteous, to justify, to declare just — the OT forensic concept")],
  ['"Justification is an instant, complete, forensic declaration — sanctification is the lifelong process that follows it. Confusing them is the root of both legalism and antinomianism."',
   '"\'God justifies the ungodly\' (Rom 4:5) — not the nearly-good-enough, not those who tried hard. The ungodly. That\'s who Christ died for."',
   '"Luther: \'This is the article upon which the church stands or falls.\' When justification is lost, the gospel is lost."'],
  [("Righteousness","righteousness"),("Salvation","salvation"),("Grace","grace"),("Atonement","atonement"),("Faith","faith")])

# ── LOVE ──────────────────────────────────────────────────────────────────────
PAGES["love"] = word_page(
  "Love", "/l&#652;v/", "noun / verb",
  'Old English <em>lufu</em>; Proto-Germanic <em>*lub&#333;</em>; PIE <em>*leubh-</em> (&ldquo;to care, desire, love&rdquo;). Greek: <em>agap&#275;</em> (&#7936;&#947;&#940;&#960;&#951;). Hebrew: <em>ahavah</em> (&#1488;&#1463;&#1492;&#1458;&#1489;&#1464;&#1492;), <em>chesed</em> (&#1495;&#1462;&#1505;&#1462;&#1491;).',
  'In Scripture, love is not primarily an emotion but a <strong>covenant commitment of the will</strong> expressed through sacrificial action. The Greek <em>agap&#275;</em> &mdash; the highest biblical love &mdash; is defined by God\'s own nature: &ldquo;God is love&rdquo; (1 John 4:8). It is selfless, unconditional, and active. Jesus demonstrates that love is measured not by feeling but by laying down one\'s life (John 15:13). The command to love (Matt 22:37–39) assumes love is a choice, not merely an experience. <em>Chesed</em> (lovingkindness) speaks of covenant loyalty &mdash; a faithful, steadfast devotion that does not abandon its object regardless of circumstance.',
  '<strong>LOVE</strong>, <em>n.</em> 1. An affection of the mind excited by beauty and worth of any kind. 2. The love of God is the first duty of man, springing from just views of his attributes. 3. <em>v.t.</em> To have benevolence or good will toward. The Christian is commanded to love his neighbor as himself and to love his enemies. Applied to God, it is the most exalted affection and supreme devotion of the soul.',
  'Modern culture has collapsed love into <strong>romantic feeling and sexual attraction</strong>, reducing <em>agap&#275;</em> to <em>eros</em>. &ldquo;Love is love&rdquo; has become a slogan to legitimize any desire as moral and beyond critique. The biblical definition &mdash; covenantal, self-sacrificial, truth-bound &mdash; is dismissed as &ldquo;conditional&rdquo; or unloving when it involves correction or calls to repentance. True love &ldquo;rejoices with the truth&rdquo; (1 Cor 13:6) and sometimes looks like loving rebuke rather than affirmation.',
  """PIE *leubh- ("to care, desire, love")
  → Proto-Germanic *lubō (love, affection)
    → Old English lufu (noun), lufian (verb)
      → Middle English love
        → Modern English "love"

Cognates: lief (Old English for "dear, beloved"), leave (originally "permission" from love)
Latin cognate: libēre / lubēre ("to please") → libido (desire)

Greek (separate root):
ἀγάπη (agapē, G26) — divine, covenantal, self-giving love
φιλία (philia, G5373) — friendship, brotherly love
ἔρως (eros) — romantic/sexual love (not used in NT)
στοργή (storgē) — family affection

Biblical parallel:
Proto-Semitic *ʾhb → Hebrew אָהַב (ahav, H157) — to love, desire
  → אַהֲבָה (ahavah) — love as covenant bond
  → חֶסֶד (chesed, H2617) — steadfast lovingkindness, covenant loyalty""",
  [("John 3:16","John+3:16","\"For God so loved the world that he gave his only Son...\""),
   ("1 Corinthians 13:4–7","1+Corinthians+13:4-7","The anatomy of love: patient, kind, not self-seeking."),
   ("1 John 4:8","1+John+4:8","\"Anyone who does not love does not know God, because God is love.\""),
   ("Matthew 22:37–39","Matthew+22:37-39","Love God and neighbor: the two great commandments."),
   ("Romans 5:8","Romans+5:8","\"God demonstrates his own love for us in this: While we were still sinners, Christ died for us.\"")],
  [("G26","agapē","&#7936;&#947;&#940;&#960;&#951;","unconditional, covenantal love; the love of God and commanded love of neighbor"),
   ("G5368","phileō","&#966;&#953;&#955;&#941;&#969;","brotherly affection, warm friendship"),
   ("H157","ahav","&#1488;&#1464;&#1492;&#1463;&#1489;","to love; used of God's love for Israel and of human covenant love"),
   ("H2617","chesed","&#1495;&#1462;&#1505;&#1462;&#1491;","steadfast lovingkindness; covenant loyalty and mercy")],
  ['"A father disciplines his son because he loves him — love is not the absence of correction but its motivation." (cf. Prov 3:12)',
   '"Love without truth is sentimentality; truth without love is cruelty — the biblical call is to speak truth in love." (Eph 4:15)',
   '"The measure of love is not how it feels but what it costs: Christ\'s cross is the definitive definition."'],
  [("Grace","grace"),("Mercy","mercy"),("Covenant","covenant"),("Faith","faith"),("Joy","joy")])

# ── MARRIAGE ──────────────────────────────────────────────────────────────────
PAGES["marriage"] = word_page(
  "Marriage", "/&#712;m&#230;r.&#618;d&#658;/", "noun",
  'Old French <em>mariage</em>; Latin <em>maritare</em> (to wed); from <em>maritus</em> (husband). Hebrew: <em>ishshah</em> (&#1488;&#1460;&#1513;&#1468;&#1464;&#1492;, wife), <em>berit</em> (covenant). Greek: <em>gamos</em> (&#947;&#940;&#956;&#959;&#962;).',
  'Marriage is the <strong>lifelong, covenantal union of one man and one woman</strong>, instituted by God before the fall as the fundamental human social institution. God himself presides over the first marriage (Gen 2:22–24): he creates woman from man\'s side, brings her to him, and pronounces the covenant. Marriage images the relationship between Christ and the church (Eph 5:22–33) &mdash; it is not merely a social contract but a theological symbol embedded in creation. The &ldquo;one flesh&rdquo; union (Gen 2:24) involves every dimension: spiritual, emotional, social, physical. History itself ends with a wedding (Rev 19:7–9).',
  '<strong>MARRIAGE</strong>, <em>n.</em> 1. The act of uniting a man and woman for life; wedlock; the legal union of a man and woman for life. Marriage was instituted by God himself for the purpose of preventing the promiscuous intercourse of the sexes, for promoting domestic felicity, and for securing the maintenance and education of children.',
  'Marriage has undergone total redefinition: from covenant to contract (easily dissolved), from male-female complementarity to same-sex union, from permanent to serial (no-fault divorce), from procreative to therapeutic (primarily about personal fulfillment). Each redefinition removes one more layer of the theological and biological structure God embedded in creation. When marriage loses its nature as covenant imaging Christ and the church, it becomes simply a romantic arrangement with legal benefits &mdash; which explains why the institution is collapsing.',
  """Latin maritus ("husband, married man")
  → maritare ("to wed, to give in marriage")
    → Old French mariage
      → Middle English mariage
        → Modern English "marriage"

Possible Latin root: mas/maris ("male") → maritus
Alternative etymology: PIE *mari- ("young woman") — the union of male and female

Greek:
γάμος (gamos, G1062) — marriage, wedding feast
  → γαμέω (gameō, G1060) — to marry
  → γαμίζω (gamizō, G1061) — to give in marriage (Matt 22:30)
  → Modern: monogamy (one marriage), bigamy (two), polygamy (many)

Biblical parallel:
Hebrew אִשָּׁה (ishshah, H802) — woman, wife
  → אִישׁ (ish, H376) — man, husband
  → Eve was taken from ish — they share the same root (Gen 2:23)
  → "She shall be called Woman (ishshah) because she was taken from Man (ish)"
  → בְּרִית (berit, H1285) — covenant; marriage described as covenant in Prov 2:17, Mal 2:14""",
  [("Genesis 2:24","Genesis+2:24","\"Therefore a man shall leave his father and his mother and hold fast to his wife, and they shall become one flesh.\""),
   ("Ephesians 5:25–32","Ephesians+5:25-32","Husbands love as Christ loved the church — marriage as theological symbol."),
   ("Malachi 2:14–16","Malachi+2:14-16","\"The LORD... is witness between you and the wife of your youth... she is your companion and your wife by covenant.\""),
   ("Matthew 19:4–6","Matthew+19:4-6","\"Have you not read that he who created them... made them male and female... what God has joined together, let not man separate?\""),
   ("Revelation 19:7–9","Revelation+19:7-9","The Marriage Supper of the Lamb — history ends with a wedding.")],
  [("G1062","gamos","&#947;&#940;&#956;&#959;&#962;","marriage, wedding, wedding feast — the institution and its celebration"),
   ("H376","ish","&#1488;&#1460;&#1497;&#1513;&#1473;","man, husband; shares a root with ishshah (woman) — etymologically united"),
   ("H802","ishshah","&#1488;&#1460;&#1513;&#1468;&#1464;&#1492;","woman, wife — she who came from ish (Gen 2:23)"),
   ("H1285","berit","&#1489;&#1468;&#1456;&#1512;&#1460;&#1497;&#1514;","covenant — marriage described as berit in Prov 2:17 and Mal 2:14")],
  ['"Marriage exists because the Trinity exists — eternal self-giving love eternally overflows. The Father gives himself to the Son, the Son to the Father, in the Spirit. Marriage images this."',
   '"\'One flesh\' is not metaphor — it is the most comprehensive human unity: two people becoming a new entity, which is why divorce is like tearing a body apart."',
   '"History ends with a wedding (Rev 19:7–9). Everything in between is the courtship — God pursuing his bride through covenant, redemption, and grace."'],
  [("Covenant","covenant"),("Family","family"),("Love","love"),("Sacred","sacred"),("Blessing","blessing")])

# ── MERCY ──────────────────────────────────────────────────────────────────────
PAGES["mercy"] = word_page(
  "Mercy", "/&#712;m&#604;&#720;r.si/", "noun",
  'Old French <em>merci</em>, Latin <em>merces</em> (wages) &#8594; Ecclesiastical Latin (pity, heavenly reward). Hebrew: <em>racham</em> (&#1512;&#1463;&#1495;&#1463;&#1501;), <em>chesed</em> (&#1495;&#1462;&#1505;&#1462;&#1491;). Greek: <em>eleos</em> (&#7952;&#955;&#949;&#959;&#962;).',
  'Mercy is <strong>compassionate forbearance toward the guilty</strong> &mdash; not getting the punishment one deserves. In Hebrew, <em>racham</em> derives from the word for womb (<em>rechem</em>), suggesting visceral, maternal tenderness. <em>Chesed</em> adds covenant loyalty &mdash; God\'s mercy is not arbitrary but flows from his faithful commitment. The Psalms cry out for mercy from a God who &ldquo;does not deal with us according to our sins&rdquo; (Ps 103:10). Jesus defines mercy practically in the parable of the Good Samaritan: mercy moves toward need at personal cost.',
  '<strong>MERCY</strong>, <em>n.</em> 1. That benevolence, mildness or tenderness of heart which disposes a person to overlook injuries, or to treat an offender better than he deserves; forbearance toward offenders and enemies. 2. The disposition that tempers justice and inclines one to pity and spare. 3. An act of kindness; a favor shown to the guilty. 4. The divine compassion exercised toward sinners.',
  'Mercy has been weaponized as <strong>opposition to all consequences</strong> &mdash; &ldquo;mercy&rdquo; now often means eliminating accountability entirely, regardless of repentance. This severs mercy from justice: biblical mercy never pretends the wrong didn\'t happen (that would be injustice); it absorbs the cost. The cross is the supreme demonstration &mdash; God is both just and the justifier (Rom 3:26). Mercy that requires no repentance is indulgence, not grace.',
  """Latin merces ("wages, pay, reward")
  → Ecclesiastical Latin sense: heavenly reward → then pity toward the poor
    → Old French merci ("pity, favor, thanks")
      → Middle English mercy
        → Modern English "mercy"

Semantic shift: from "wages" to "pity" reflects the idea of giving
unearned reward — pity as a gift beyond what is owed.

Greek:
ἔλεος (eleos, G1656) — mercy, compassion, pity
  → ἐλεέω (eleeō, G1653) — to have mercy, to show compassion
  → Kyrie eleison — "Lord, have mercy" (the oldest Christian liturgical cry)

Biblical parallel:
Proto-Semitic *rḥm → Hebrew רַחַם (racham, H7355) — to have compassion
  → רֶחֶם (rechem) — womb (mercy as womb-love, visceral, protective tenderness)
  → רַחֲמִים (rachamim) — mercies, compassions (Lam 3:22)
Proto-Semitic *ḥsd → Hebrew חֶסֶד (chesed, H2617) — covenant mercy/loyalty
  → The most theologically rich OT mercy term — steadfast covenantal kindness""",
  [("Lamentations 3:22–23","Lamentations+3:22-23","\"The steadfast love of the LORD never ceases; his mercies never come to an end.\""),
   ("Matthew 5:7","Matthew+5:7","\"Blessed are the merciful, for they shall receive mercy.\""),
   ("Micah 6:8","Micah+6:8","\"What does the LORD require of you but to do justice, and to love kindness (mercy), and to walk humbly with your God?\""),
   ("Psalm 103:10–12","Psalm+103:10-12","\"He does not deal with us according to our sins... as far as the east is from the west, so far does he remove our transgressions.\""),
   ("Luke 10:37","Luke+10:37","\"Go and do likewise\" — mercy defined as costly action toward the suffering.")],
  [("G1656","eleos","&#7952;&#955;&#949;&#959;&#962;","mercy, compassion, pity; active help toward the suffering"),
   ("H2617","chesed","&#1495;&#1462;&#1505;&#1462;&#1491;","steadfast lovingkindness, covenant mercy — the most frequent OT mercy term"),
   ("H7355","racham","&#1512;&#1463;&#1495;&#1463;&#1501;","to have compassion, show mercy; root connected to rechem (womb)")],
  ['"Mercy is not the absence of justice — it is justice satisfied at someone else\'s expense. Christ absorbed the penalty so mercy could flow freely."',
   '"\'Lord, have mercy\' (Kyrie eleison) is the oldest Christian prayer — the recognition that we stand before God only because he chooses not to deal with us as we deserve."',
   '"Earthly mercy trains us for the Final Mercy: \'Blessed are the merciful, for they shall receive mercy.\'"'],
  [("Grace","grace"),("Love","love"),("Atonement","atonement"),("Repentance","repentance"),("Righteousness","righteousness")])

# ── PEACE ──────────────────────────────────────────────────────────────────────
PAGES["peace"] = word_page(
  "Peace", "/pi&#720;s/", "noun",
  'Old French <em>pais</em>; Latin <em>pax</em> (peace, treaty); PIE <em>*peh&#8322;&#7611;-</em> (&ldquo;to fasten, make firm&rdquo;). Hebrew: <em>shalom</em> (&#1513;&#1464;&#1500;&#1493;&#1465;&#1501;, wholeness). Greek: <em>eir&#275;n&#275;</em> (&#949;&#7984;&#961;&#942;&#957;&#951;, harmony).',
  'Biblical peace is not the mere <strong>absence of conflict</strong> but the positive flourishing of wholeness, right relationship, and completeness. The Hebrew <em>shalom</em> encompasses well-being, health, prosperity, harmony, and completeness &mdash; the state in which all things are as they should be. Christ is the &ldquo;Prince of Peace&rdquo; (Isa 9:6) who makes peace &ldquo;by the blood of his cross&rdquo; (Col 1:20), reconciling humanity to God. The peace of God &ldquo;surpasses all understanding&rdquo; (Phil 4:7) &mdash; not rational calmness but supernatural stability in God\'s presence. True peace is not achieved by politics or therapy but given by Christ: &ldquo;My peace I give to you&rdquo; (John 14:27).',
  '<strong>PEACE</strong>, <em>n.</em> 1. A state of quiet or tranquility; freedom from disturbance or agitation. 2. Freedom from war with a foreign nation; public quiet. 3. Reconciliation; agreement after variance. 4. In a Scriptural sense, the tranquility, harmony, and blessedness of the heavenly state; reconciliation with God through Jesus Christ.',
  'Modern peace is primarily <strong>political and psychological</strong>: absence of conflict between nations (Pax Romana) or inner emotional stability (mindfulness culture). &ldquo;Peace and safety&rdquo; (1 Thess 5:3) is the false security Paul warns against. The therapeutic gospel promises inner peace through self-acceptance, bypassing repentance. The political gospel promises peace through justice activism, bypassing the cross. Both miss the root: all disharmony traces to the disruption of humanity\'s relationship with God, which only the cross can repair.',
  """PIE *peh₂ǵ- ("to fasten, to fix firmly, to bind")
  → Latin pangere ("to fasten") → pax/pacis ("peace, treaty")
    → The image: peace as a fixed, firm agreement — a binding compact

Latin derivatives: pacify, pacifist, appease, pact, compact, impact
Note: "pax" and "pact" share a root — peace is a fastened agreement.

Old French pais → Middle English pees → Modern English "peace"

Greek:
εἰρήνη (eirēnē, G1515) — peace, harmony, tranquility
  → Also the personal name Irene ("peaceful")
  → εἰρηνεύω (eirēneuō) — to be at peace, to live in peace
  → From εἴρω (eirō, "to join, link together") — peace as things rightly linked

Biblical parallel:
Proto-Semitic *šlm → Hebrew שָׁלֵם (shalem, "to be complete, whole, at peace")
  → שָׁלוֹם (shalom, H7965) — peace, wholeness, completeness, welfare
  → שָׁלַם (shalam) — to make restitution, to restore to wholeness
  → Jerusalem (Yeru-shalom) — "city of peace/wholeness"
  → Shalom is the OT greeting — "May you be whole"
  → שְׁלֵמוּת (shlemut) — completeness, integrity (from same root)""",
  [("Isaiah 9:6","