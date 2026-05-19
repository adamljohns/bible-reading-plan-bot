#!/usr/bin/env python3
"""Batch 44 — expand 25 more entries from the 50-60 word bucket.

Targets: ethics, hermeneutics, OT figures (Mary, Miriam),
slang/cultural reframes, eschatology, doctrines, divine names,
covenant theology, Marine motto, biblical creatures, and feasts.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'desacralization': (
        '<p>"Desacralization" names the modern Western project of removing God from every public sphere — government, economics, education, family, art, science — and insisting that religion be a strictly <em>"private matter."</em> Scripture refuses the premise. All of creation is sacred — declared <em>"very good"</em> by God (<em>Genesis 1:31</em>) and sustained moment-by-moment by Christ’s active word: <em>"and by him all things consist"</em> (<em>Colossians 1:17</em>). The biblical worldview has no neutral secular/sacred divide. Desacralization is not religious neutrality; it is rebellion against God’s comprehensive claim over all reality (<em>"the earth is the LORD’s, and the fulness thereof"</em>, <em>Psalm 24:1</em>). Christ’s lordship is total. The Christian must resist desacralization in his vocation, his polity, his marriage, and his speech.</p>'
    ),
    'dignity-of-work': (
        '<p>The dignity of work is the recognized worth of honest labor as service to God. <em>Genesis 2:15</em> establishes work <em>pre-Fall</em> as the dignified vocation of the man God placed in the garden: <em>"And the LORD God took the man, and put him into the garden of Eden to dress it and to keep it."</em> Work is not the curse; the curse made work harder (<em>3:17-19</em>). Paul commands those <em>"that with quietness they work, and eat their own bread"</em> (<em>2 Thessalonians 3:12</em>) and condemns idleness as serious sin: <em>"if any would not work, neither should he eat"</em> (<em>3:10</em>). Honest work, however humble — carpenter, farmer, mother, plumber, tradesman, programmer — is honorable in the kingdom. Six days work, one day rest, for life.</p>'
    ),
    'dissent': (
        '<p>Scripture recognizes both righteous and wicked dissent. The Hebrew midwives Shiphrah and Puah dissented from Pharaoh’s genocidal decree and were blessed: <em>"But the midwives feared God, and did not as the king of Egypt commanded them"</em> (<em>Exodus 1:17</em>). The apostles before the Sanhedrin: <em>"We ought to obey God rather than men"</em> (<em>Acts 5:29</em>). But Korah’s dissent against Moses brought immediate divine judgment, the earth swallowing him and his company (<em>Numbers 16:1-35</em>; cf. <em>Jude 11</em>). The legitimacy of dissent depends entirely on whether it is grounded in God’s Word or in human pride. Christian dissent from ungodly authority is duty; dissent from godly authority is rebellion. Discern the difference carefully.</p>'
    ),
    'dream-biblical': (
        '<p>God frequently used dreams as a channel of revelation in Scripture. He appeared to Jacob at Bethel with the ladder reaching to heaven (<em>Genesis 28:12</em>). He gave Joseph the patriarch prophetic dreams of his brothers’ and parents’ obeisance (<em>Genesis 37:5-9</em>), and gave him the interpretation of Pharaoh’s dreams (<em>chs. 40-41</em>). He warned the Magi not to return to Herod (<em>Matthew 2:12</em>) and directed Joseph the carpenter to take Mary as wife (<em>Matthew 1:20</em>) and to flee to Egypt (<em>2:13</em>). Yet Scripture also warns sharply against false dreamers who claim divine authority for their own imaginations: <em>"Behold, I am against them that prophesy false dreams, saith the LORD"</em> (<em>Jeremiah 23:25-32</em>). Test every dream by Scripture.</p>'
    ),
    'eat-my-shorts': (
        '<p>"Eat my shorts" is the Gen-X-era dismissive contempt phrase, popularized as Bart Simpson’s catchphrase on <em>The Simpsons</em> from 1989 onward. Schoolyard-coded, era-stamped, and now slightly nostalgic. The biblical category running underneath is the same as for any contempt-phrase: like <em>diss</em>, <em>Raca</em> (<em>Matthew 5:22</em>), or calling another <em>"fool"</em>, the willed verbal dismissal of another with contempt language is exactly what Christ forbids: <em>"But I say unto you, That whosoever is angry with his brother without a cause shall be in danger of the judgment: and whosoever shall say to his brother, Raca, shall be in danger of the council: but whosoever shall say, Thou fool, shall be in danger of hell fire."</em> The vehicle differs by era; the category does not.</p>'
    ),
    'flower-power': (
        '<p>"Flower Power" was the late-1960s American counterculture slogan for nonviolent, love-based resistance — symbolized by handing flowers to soldiers and police during anti-Vietnam protests. The instinct — returning good for evil — is genuinely biblical in form: <em>"Recompense to no man evil for evil"</em> (<em>Romans 12:17</em>); <em>"Bless them that curse you, do good to them that hate you"</em> (<em>Matthew 5:44</em>). The corruption was in its grounding. Flower Power was a felt sentiment, not a settled doctrine of God’s justice, Christ’s atonement, and the Christian’s appointed place in spiritual warfare. When the cultural feeling faded, the ethic faded with it — into drug-haze, libertinism, and eventual cynicism. Christ’s love-of-enemies is rooted in the cross. Sentiment alone cannot sustain it.</p>'
    ),
    'foundationalism': (
        '<p>Foundationalism is the epistemological view that knowledge has <em>foundational</em> beliefs — basic, self-evident, or otherwise warrant-conferring — from which all other beliefs are derived. <em>Strong</em> or <em>classical</em> foundationalism (Descartes) requires foundational beliefs to be incorrigibly certain (<em>"I think, therefore I am"</em>). <em>Modest</em> foundationalism allows foundational beliefs to be <em>"properly basic"</em> without absolute certainty — basic to the noetic structure but not infallible. Reformed epistemology (Alvin Plantinga, Nicholas Wolterstorff) argues that belief in God can itself be properly basic — a foundational belief produced by the <em>sensus divinitatis</em> God has placed in the human mind. The Christian therefore needs no Cartesian foundation; God’s witness in conscience and Scripture is foundation enough.</p>'
    ),
    'four-senses': (
        '<p>The Four Senses of Scripture is the medieval interpretive scheme summarized in the Latin couplet: <em>"Litera gesta docet, quid credas allegoria, moralis quid agas, quo tendas anagogia"</em> — "the letter teaches what happened; allegory teaches what to believe; the moral sense teaches how to act; anagogy teaches where to go." Literal (what happened), allegorical (what it points to about Christ and the church), moral or tropological (how to live), and anagogical (eschatological, where it points). The method shaped medieval exegesis for a millennium. The Reformers — Luther, Calvin, Tyndale — retained the legitimate insights (especially typology) while reasserting the priority and controlling role of the literal sense: <em>"the literal sense is the root and ground of all"</em>.</p>'
    ),
    'fox': (
        '<p>The fox is the wild canine of Israelite hill country — and in Scripture, a recurring figure of cunning destruction. Solomon warns of <em>"the little foxes, that spoil the vines: for our vines have tender grapes"</em> (<em>Song 2:15</em>) — small predators doing disproportionate damage. Christ called Herod Antipas <em>"that fox"</em> when warned of his designs against Him: <em>"Go ye, and tell that fox, Behold, I cast out devils, and I do cures to day and to morrow"</em> (<em>Luke 13:32</em>). Samson harnessed three hundred foxes tail-to-tail with firebrands and set the Philistine standing grain ablaze (<em>Judges 15:4-5</em>). Foxes in Scripture are slippery, opportunistic, and corrosive — they prefer small destruction at scale. Watch for them in the vineyard of marriage, church, and soul.</p>'
    ),
    'gabriel': (
        '<p>Gabriel is the angelic messenger entrusted with the most consequential birth-announcements in human history. He interprets Daniel’s vision of the ram and goat (<em>Daniel 8:16</em>) and then the seventy-weeks prophecy (<em>9:21-27</em>). He stands in the presence of God: <em>"I am Gabriel, that stand in the presence of God; and am sent to speak unto thee, and to shew thee these glad tidings"</em> (<em>Luke 1:19</em>). He announces the conception of John the Baptist to Zacharias at the altar of incense in the temple (<em>Luke 1:11-20</em>). He announces the incarnation to Mary at Nazareth (<em>Luke 1:26-38</em>): <em>"Hail, thou that art highly favoured, the Lord is with thee"</em>. Gabriel is the announcing angel of the messianic plan.</p>'
    ),
    'hanukkah': (
        '<p>Hanukkah — the Feast of Dedication — is the eight-day winter feast commemorating the cleansing and rededication of the Jerusalem temple by the Maccabees in 165 BC after Antiochus Epiphanes IV had desecrated it with the abomination of desolation (a swine sacrificed to Zeus on the altar). The traditional miracle of the oil — one day’s supply lasting eight — is post-biblical legend; the historical reality of the rededication is sober history (recorded in <em>1 and 2 Maccabees</em>). The feast is intertestamental in origin but biblical in mention: John 10:22 names it as the setting for Christ’s declaration <em>"I and my Father are one"</em> (<em>v. 30</em>). The Light of the World walked through the rededicated temple at the feast of lights.</p>'
    ),
    'harden-heart': (
        '<p>"Hardening the heart" is the recurring biblical theme applied both to humans and (judicially) to God’s acting upon them. Pharaoh hardens his own heart, and YHWH also hardens Pharaoh’s heart, throughout <em>Exodus 4-14</em> — the divine and human actions are not in conflict but converge in the same judicial outcome. The wilderness generation hardened their hearts at Meribah: <em>"Harden not your heart, as in the provocation, and as in the day of temptation in the wilderness"</em> (<em>Psalm 95:8</em>). <em>Hebrews 3-4</em> takes up the warning and applies it to the New-Covenant church repeatedly: <em>"To day if ye will hear his voice, harden not your hearts"</em> (<em>Hebrews 3:7-8, 15; 4:7</em>). Heart-hardening is gradual; each refusal of conviction tightens the surface.</p>'
    ),
    'hunger-thirst-righteousness': (
        '<p>"Hunger and thirst for righteousness" is the fourth Beatitude: <em>"Blessed are they which do hunger and thirst after righteousness: for they shall be filled"</em> (<em>Matthew 5:6</em>). The verbs are present tense — continuously hungering, continuously thirsting — not seekers who have arrived but seekers who keep seeking. <em>"Righteousness"</em> here includes both the righteousness Christ <em>provides</em> (imputed in justification, <em>2 Corinthians 5:21</em>) and the righteousness Christ <em>produces</em> (worked out in sanctification, <em>Romans 6:13</em>). Both kinds will be filled. The Christian who has lost his appetite has stopped pursuing the right meal. <em>"As the hart panteth after the water brooks, so panteth my soul after thee, O God"</em> (<em>Psalm 42:1</em>). Keep hungering.</p>'
    ),
    'jive': (
        '<p>"Jive" is Boomer / jazz-era slang for fast, glib talk — sometimes elaborate hipster slang for its own sake, more often deceptive or empty speech: <em>"don’t give me that jive."</em> The vocabulary accurately names something Scripture also names: smooth speech that hides emptiness or deception underneath. Where the slang offers a shrug, Scripture offers a warning. Smooth lips and a wicked heart are a familiar Proverbs pair: <em>"Burning lips and a wicked heart are like a potsherd covered with silver dross. He that hateth dissembleth with his lips, and layeth up deceit within him"</em> (<em>Proverbs 26:23-24</em>); <em>"A flattering mouth worketh ruin"</em> (<em>26:28</em>). The Christian man rejects jive — refuses to give it or receive it.</p>'
    ),
    'lying': (
        '<p>Lying is the deliberate utterance of falsehood — an offense the LORD hates. It stands in the sevenfold list of <em>Proverbs 6:16-19</em>: <em>"These six things doth the LORD hate: yea, seven are an abomination unto him... A lying tongue... A false witness that speaketh lies."</em> It breaks the ninth commandment (<em>Exodus 20:16</em>). Christ traces it to its source: <em>"He was a murderer from the beginning, and abode not in the truth, because there is no truth in him. When he speaketh a lie, he speaketh of his own: for he is a liar, and the father of it"</em> (<em>John 8:44</em>). Lying is condemned absolutely; liars are excluded from the New Jerusalem: <em>"and all liars, shall have their part in the lake"</em> (<em>Revelation 21:8, 27</em>).</p>'
    ),
    'mary': (
        '<p>Mary was the Galilean virgin of Nazareth chosen by God to be the mother of the incarnate Christ. Scripture portrays her in three principal poses. First, the <em>Magnificat</em> — a young woman magnifying the Lord in song after the angel’s annunciation: <em>"My soul doth magnify the Lord, And my spirit hath rejoiced in God my Saviour"</em> (<em>Luke 1:46-55</em>). Second, at the cross — suffering with her Son, where Christ commits her to John’s care (<em>John 19:25-27</em>). Third, in the upper room — praying with the disciples after the ascension (<em>Acts 1:14</em>). She is rightly called <em>"blessed... among women"</em> (<em>Luke 1:42</em>) and the church honors her, but she is <em>not</em> to be worshipped. She is mother, not mediatrix.</p>'
    ),
    'miriam': (
        '<p>Miriam was the older sister of Moses and Aaron — the alert child who watched the basket of bulrushes from the Nile reeds and arranged for Moses’ own mother to nurse him (<em>Exodus 2:4-8</em>). She became the prophetess who led Israel’s women in the song at the Red Sea: <em>"Sing ye to the LORD, for he hath triumphed gloriously"</em> (<em>Exodus 15:20-21</em>). She is named with Moses and Aaron as one of three sent to lead Israel out of Egypt (<em>Micah 6:4</em>). But she later sinned in challenging Moses’ unique prophetic authority (<em>"Hath the LORD indeed spoken only by Moses?"</em>) and was struck with leprosy white as snow — restored only after Moses’ intercession on her behalf (<em>Numbers 12:1-15</em>). She died at Kadesh and was buried there (<em>20:1</em>).</p>'
    ),
    'miserable-comforters': (
        '<p>"Miserable comforters" is Job’s exasperated diagnosis of his three friends in <em>Job 16:2</em>: <em>"I have heard many such things: miserable comforters are ye all."</em> The three — Eliphaz, Bildad, and Zophar — had come intending to comfort him in his suffering, and at first they sat with him in silence seven days (<em>Job 2:13</em>). But once they began to speak, they insisted his suffering proved hidden sin — pressing the flat retribution theology of <em>"the wicked suffer, so you suffered, therefore you are wicked"</em>. Their well-meaning theology was too small for the case. The phrase has become Christian shorthand for counselors whose theology of suffering cannot hold the actual life in front of them. Better silence than miserable comfort.</p>'
    ),
    'mouth': (
        '<p>The mouth is the bodily aperture for speech, eating, and breath — and in Scripture, the chief outlet of the heart’s contents. Christ says it directly: <em>"For out of the abundance of the heart the mouth speaketh"</em> (<em>Matthew 12:34</em>); <em>"those things which proceed out of the mouth come forth from the heart; and they defile the man"</em> (<em>Matthew 15:18</em>). Paul says: <em>"For with the heart man believeth unto righteousness; and with the mouth confession is made unto salvation"</em> (<em>Romans 10:10</em>). The mouth is therefore the diagnostic instrument for the heart and the public organ of profession. <em>"Set a watch, O LORD, before my mouth; keep the door of my lips"</em> (<em>Psalm 141:3</em>). Christians guard the mouth as a sentry at the gate.</p>'
    ),
    'myrtle': (
        '<p>The myrtle is a fragrant evergreen shrub native to Israel — and in Scripture, prescribed traditionally for the booths of the Feast of Tabernacles (<em>Leviticus 23:40</em>; <em>Nehemiah 8:15</em>). It is the symbol of the restored remnant in Isaiah’s great salvation oracles: <em>"I will plant in the wilderness the cedar, the shittah tree, and the myrtle, and the oil tree"</em> (<em>Isaiah 41:19</em>); <em>"instead of the thorn shall come up the fir tree, and instead of the brier shall come up the myrtle tree"</em> (<em>Isaiah 55:13</em>). And it is the tree among which the Angel of the LORD appeared in Zechariah’s first night-vision (<em>Zechariah 1:8</em>) — standing among Israel’s downtrodden in the bottom of the valley. The LORD shelters in the lowly tree.</p>'
    ),
    'name-of-yhwh': (
        '<p>The Name of YHWH is, in biblical thought, far more than a label. It carries His revealed character, His present-active presence, and His authority. To <em>call upon the Name</em> is to invoke YHWH Himself: <em>"And it shall come to pass, that whosoever shall call on the name of the LORD shall be saved"</em> (<em>Joel 2:32</em>; <em>Acts 2:21</em>; <em>Romans 10:13</em>). To <em>honor the Name</em> is to honor Him (<em>Malachi 1:11</em>); to <em>profane the Name</em> is to profane Him (<em>Ezekiel 36:20-23</em>). The third commandment guards it: <em>"Thou shalt not take the name of the LORD thy God in vain"</em> (<em>Exodus 20:7</em>). Christ comes <em>"in the name of the LORD"</em> (<em>Psalm 118:26; Matthew 21:9</em>) — He <em>is</em> the Name revealed.</p>'
    ),
    'nurture-admonition': (
        '<p>"Nurture and admonition" is the KJV pairing in <em>Ephesians 6:4</em>: <em>"And, ye fathers, provoke not your children to wrath: but bring them up in the nurture and admonition of the Lord."</em> <em>Nurture</em> (Greek <em>paideia</em>) is the broad child-training and formation, including discipline, instruction, correction, and example — the whole shaping work of raising a child. <em>Admonition</em> (Greek <em>nouthesia</em>) is the verbal placing-in-mind — the spoken instruction, the warning, the rehearsed lesson. Together they cover the formative task: discipline shaped by speech, speech reinforced by discipline. The two should not separate. A father who admonishes without nurturing produces resentment; one who nurtures without admonishing produces softness. Both belong to Christian fatherhood.</p>'
    ),
    'outer-darkness': (
        '<p>"Outer darkness" is the eschatological place Christ names three times in Matthew’s Gospel for those finally cast out of the kingdom feast. <em>"The children of the kingdom shall be cast out into outer darkness: there shall be weeping and gnashing of teeth"</em> (<em>Matthew 8:12</em>); the guest without the wedding garment is <em>"bound hand and foot... cast... into outer darkness"</em> (<em>Matthew 22:13</em>); the unprofitable servant: <em>"cast ye the unprofitable servant into outer darkness"</em> (<em>Matthew 25:30</em>). Three characteristics: <em>outer</em> (excluded from the lighted hall of the kingdom feast), <em>darkness</em> (the absence of God’s light, the place where He is not), and the place of <em>weeping and gnashing of teeth</em> (conscious, eternal sorrow). Christ’s sternest warnings about final exclusion.</p>'
    ),
    'remnant-faithful': (
        '<p>The "remnant" is the biblical-theological concept of the faithful core God preserves through judgment. Across the prophets, when judgment falls on Israel, a remnant survives; that remnant carries the covenant promise forward to the next generation. <em>"Except the LORD of hosts had left unto us a very small remnant, we should have been as Sodom"</em> (<em>Isaiah 1:9</em>); <em>"For though thy people Israel be as the sand of the sea, yet a remnant of them shall return"</em> (<em>Isaiah 10:21-22</em>; cf. <em>Jeremiah 23:3</em>; <em>Micah 4:7</em>; <em>Zephaniah 3:13</em>). Paul takes up the doctrine in Romans: <em>"Even so then at this present time also there is a remnant according to the election of grace"</em> (<em>Romans 11:5</em>). God always preserves His own.</p>'
    ),
    'semper-fidelis': (
        '<p><em>Semper Fidelis</em> — Latin for "always faithful" — has been the motto of the United States Marine Corps since 1883, shortened in service usage to <em>"Semper Fi"</em>. Scripture commends the same disposition continually. <em>"Be thou faithful unto death, and I will give thee a crown of life"</em> (<em>Revelation 2:10</em>); <em>"His lord said unto him, Well done, thou good and faithful servant: thou hast been faithful over a few things, I will make thee ruler over many things: enter thou into the joy of thy lord"</em> (<em>Matthew 25:21</em>); <em>"Moreover it is required in stewards, that a man be found faithful"</em> (<em>1 Corinthians 4:2</em>). The Marine’s <em>semper fi</em> and the saint’s perseverance share a vocabulary; for the Christian Marine, they share an object.</p>'
    ),
}

BD_RE = re.compile(r'(<div class="biblical-def">)(.*?)(</div>)', re.DOTALL)

def patch(slug, new_inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return False, 'file missing'
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_html, n = BD_RE.subn(
        rf'\g<1>\n                {new_inner}\n            \g<3>',
        html, count=1)
    if n == 0:
        return False, 'pattern not matched'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'

def main():
    ok, fail = 0, 0
    for slug, new in EXPANSIONS.items():
        success, reason = patch(slug, new)
        if success:
            ok += 1
        else:
            fail += 1
            print(f'  FAIL {slug}: {reason}')
    print(f'Expanded {ok}/{ok+fail} entries')

if __name__ == '__main__':
    main()
