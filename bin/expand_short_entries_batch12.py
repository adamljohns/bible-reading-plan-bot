#!/usr/bin/env python3
"""Batch 12 — expand 25 more thin entries (clearing the 1-30 word bucket)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'unspotted': (
        '<p>Free from the world\'s stains; the second half of pure religion James names. James 1:27: '
        '<em>Pure religion and undefiled before God and the Father is this, To visit the fatherless and '
        'widows in their affliction, and to keep himself unspotted from the world.</em> The Greek '
        '<em>aspilos</em> (without stain, spot, or blemish) is also used of Christ Himself as the '
        'spotless Lamb (1 Pet 1:19) and as the standard for Christian conduct (1 Tim 6:14: <em>That '
        'thou keep this commandment without spot, unrebukeable, until the appearing of our Lord Jesus '
        'Christ</em>). The two halves of James 1:27 are inseparable: outward service (visiting orphans '
        'and widows) AND inward purity (unspotted from the world). Either half without the other '
        'becomes counterfeit religion. James insists on both.</p>'
    ),
    'vows': (
        '<p>Solemn voluntary promises made to God, often in the context of distress or thanksgiving, '
        'binding once made. Vows are not commanded (Deut 23:22: <em>if thou shalt forbear to vow, it '
        'shall be no sin in thee</em>) but obligatory once spoken. Numbers 30 details the law of vows '
        '(including father\'s and husband\'s authority to disallow a woman\'s vow). Ecclesiastes 5:4-5: '
        '<em>When thou vowest a vow unto God, defer not to pay it; for he hath no pleasure in fools: '
        'pay that which thou hast vowed. Better is it that thou shouldest not vow, than that thou '
        'shouldest vow and not pay.</em> Christ\'s caution in Matthew 5:33-37 raises the bar further: '
        'rather than negotiating oath categories, let your yes be yes and your no be no. The biblical '
        'man uses vows sparingly but treats them with full seriousness when made &mdash; marriage '
        'vows, baptismal vows, ordination vows, and any explicit promise made before God.</p>'
    ),
    'zephaniah': (
        '<p>The ninth of the twelve Minor Prophets, a three-chapter prophecy proclaiming the Day of '
        'the LORD as universal judgment that purifies a humble remnant. Zephaniah prophesied during '
        'the reign of King Josiah (640-609 BC), probably before Josiah\'s great reforms of 622 BC. '
        'The book\'s structure: (1) chapter 1 announces the coming Day of the LORD against Judah\'s '
        'idolatry and against the entire world; (2) chapter 2 calls the meek to seek the LORD and '
        'pronounces specific oracles against surrounding nations (Philistia, Moab, Ammon, Ethiopia, '
        'Assyria); (3) chapter 3 indicts Jerusalem and then turns to the great promise of restoration. '
        'The book\'s climactic verse (3:17) is one of Scripture\'s most extraordinary statements of '
        'God\'s joy: <em>The LORD thy God in the midst of thee is mighty; he will save, he will '
        'rejoice over thee with joy; he will rest in his love, he will joy over thee with singing.</em> '
        'God Himself singing over His redeemed.</p>'
    ),
    '144000': (
        '<p>The sealed multitude of Revelation 7:1-8 (twelve thousand from each of twelve tribes of '
        'Israel) and Revelation 14:1-5 (with the Lamb on Mount Zion, having the Father\'s name '
        'written in their foreheads). The number is twelve squared times one thousand &mdash; a '
        'classic biblical fullness-of-fullness symbol. Interpretation varies among orthodox '
        'Christians: (1) literal Jewish remnant during the eschatological tribulation '
        '(dispensational futurist); (2) symbolic full number of the redeemed church (preterist, '
        'amillennial, postmillennial); (3) symbolic faithful within ethnic Israel still to be '
        'gathered (historic premillennial); the sect-based interpretations (Jehovah\'s Witnesses\' '
        '144,000 limited heaven-dwellers) misread the text by collapsing the figure into a literal '
        'cap. Either reading affirms God\'s sovereign preservation of His own through judgment: '
        'whether the number is ethnic-Israel-specific or church-symbolic, the doctrine of the '
        'preserved-elect-through-tribulation is invariant.</p>'
    ),
    '2peter': (
        '<p>Peter\'s second and final epistle, written shortly before his AD 67 martyrdom under Nero. '
        '2 Peter 1:13-14: <em>Yea, I think it meet, as long as I am in this tabernacle, to stir you '
        'up by putting you in remembrance; Knowing that shortly I must put off this my tabernacle, '
        'even as our Lord Jesus Christ hath shewed me.</em> Three chapters: (1) calls believers to '
        'grow in grace and knowledge of Christ, listing the Christian virtues to be added to faith '
        '(1:5-7), reminding readers of the apostles\' eyewitness testimony to Christ\'s majesty '
        '(1:16-18); (2) exposes false teachers within the church, with extended description of their '
        'character and doom (much of this chapter parallels Jude); (3) reaffirms the day of the Lord '
        'against scoffers who deny Christ\'s return, gives the famous <em>one day is with the Lord '
        'as a thousand years, and a thousand years as one day</em> (3:8), and closes with practical '
        'exhortation to growth in grace. The letter\'s urgency comes from its proximity to Peter\'s '
        'death.</p>'
    ),
    'babylon-revelation': (
        '<p>The symbolic name in Revelation for the worldly economic-religious system arrayed against '
        'the Lamb. <em>Mystery, Babylon the Great, the Mother of Harlots and Abominations of the '
        'Earth</em> (Rev 17:5). The figure draws on the historical Babylon of OT prophecy (Isa 13-14, '
        'Jer 50-51) and on the Babylon of the exile, expanding the type into the final-form '
        'world-system opposed to God. Revelation 17 portrays her as a great whore drunk with the '
        'blood of the saints, riding on a scarlet beast with seven heads. Revelation 18 narrates her '
        'sudden fall in one hour. Interpretive options: (1) first-century Rome as the historical '
        'referent (preterist); (2) the apostate church (some Protestant readings of <em>mystery</em>); '
        '(3) a future literal Babylon (dispensational futurist); (4) the recurring world-system '
        'pattern that takes various historical forms (idealist). The MOOP Dictionary holds (4) with '
        'futurist consummation: Babylon names the worldly Babylon-pattern operating across history, '
        'with a final eschatological form preceding Christ\'s return.</p>'
    ),
    'bear': (
        '<p>To carry, support, or produce. Greek <em>phero</em> (to carry, bring) and <em>bastazo</em> '
        '(to take up, bear burden) cover the field. Several biblical uses are theologically loaded. '
        '(1) <em>Bear fruit</em> &mdash; John 15:5: <em>I am the vine, ye are the branches: He that '
        'abideth in me, and I in him, the same bringeth forth much fruit.</em> Continuous production '
        'flowing from union with Christ. (2) <em>Bear one another\'s burdens</em> &mdash; Gal 6:2: '
        '<em>Bear ye one another\'s burdens, and so fulfil the law of Christ.</em> Mutual support '
        'within the body. (3) <em>Bear the cross</em> &mdash; Luke 14:27: <em>whosoever doth not bear '
        'his cross, and come after me, cannot be my disciple.</em> Sustained costly discipleship. (4) '
        '<em>Bear witness</em> &mdash; testimony to truth. (5) <em>Bear one\'s name</em> &mdash; '
        'wearing Christ\'s name publicly. Each use is active and ongoing &mdash; not a one-time act '
        'but a sustained carrying.</p>'
    ),
    'benediction-formula': (
        '<p>The pronounced blessing closing a worship service. Two great biblical formulas anchor the '
        'practice: the Aaronic benediction of Numbers 6:24-26 (<em>The LORD bless thee, and keep thee: '
        'The LORD make his face shine upon thee, and be gracious unto thee: The LORD lift up his '
        'countenance upon thee, and give thee peace</em>) and the apostolic benediction of 2 '
        'Corinthians 13:14 (<em>The grace of the Lord Jesus Christ, and the love of God, and the '
        'communion of the Holy Ghost, be with you all. Amen.</em>). Both are Trinitarian in shape: '
        'the Aaronic with its triple use of <em>the LORD</em>, the apostolic with explicit naming of '
        'Christ, God (the Father), and the Holy Ghost. Other significant biblical benedictions: '
        'Romans 15:13, Hebrews 13:20-21, Jude 24-25. The benediction is not the minister\'s wish but '
        'God\'s declaration <em>through</em> the minister &mdash; spoken with raised hands as a real '
        'pronouncement of divine favor on the gathered congregation. The minister blesses the people '
        'in the LORD\'s name; the LORD does the blessing.</p>'
    ),
    'cities-refuge': (
        '<p>Six Levitical cities (three east of the Jordan, three west) appointed to shelter '
        'manslayers from the avenger of blood (<em>goel ha-dam</em>) until trial and (in the case of '
        'unintentional killing) until the death of the high priest. Numbers 35, Deuteronomy 19, and '
        'Joshua 20 establish and detail the institution. The three east-Jordan cities: Bezer in '
        'Reuben\'s territory, Ramoth in Gilead in Gad\'s territory, Golan in Manasseh\'s territory. '
        'The three west-Jordan cities: Kedesh in Naphtali\'s territory, Shechem in Ephraim\'s '
        'territory, Hebron in Judah\'s territory. The cities had to be accessible (roads kept open, '
        'signposts maintained, per rabbinic tradition) and were arranged so no point in the land was '
        'too far from one. The institution distinguishes manslaughter from murder: the unintentional '
        'killer could find lasting refuge, but the deliberate murderer would be handed over to the '
        'avenger even from the altar. Christ as the eternal refuge for the believer is the typological '
        'antitype (Heb 6:18: <em>who have fled for refuge to lay hold upon the hope set before us</em>).</p>'
    ),
    'corinth-city': (
        '<p>The cosmopolitan Greek port-city on the four-mile isthmus connecting the Peloponnese to '
        'mainland Greece, controlling traffic between the Aegean and Adriatic Seas. Corinth was '
        'wealthy, urban, multicultural, and legendary for sexual immorality &mdash; the Greek verb '
        '<em>korinthiazomai</em> (to behave like a Corinthian) was slang for prostitution. The temple '
        'of Aphrodite on Acrocorinth was said to house a thousand cult prostitutes. Paul founded the '
        'Corinthian church on his second missionary journey, staying eighteen months (Acts 18:1-18). '
        'He met Aquila and Priscilla there, working as tentmakers together. The church Paul left was '
        'subsequently riddled with the problems his two preserved Corinthian letters address: '
        'factionalism, sexual immorality, lawsuits between believers, abuses of the Lord\'s Supper, '
        'confused worship, doubts about resurrection. Yet Paul addresses them as <em>sanctified in '
        'Christ Jesus, called to be saints</em> (1 Cor 1:2). The Corinthian correspondence remains '
        'one of the NT\'s richest sources for practical pastoral theology.</p>'
    ),
    'el-bethel': (
        '<p>The name Jacob gave to the altar he built at Bethel after returning from Paddan-aram. '
        'Genesis 35:1-7: God commanded Jacob to go up to Bethel and make an altar there, recalling '
        'the night God had appeared to him as he fled from Esau (the original Bethel encounter, Gen '
        '28:10-22, where Jacob saw the ladder reaching to heaven). Jacob put away the foreign gods '
        'his household had been carrying, purified them, and went up to Bethel. <em>And he built '
        'there an altar, and called the place El-bethel: because there God appeared unto him, when '
        'he fled from the face of his brother</em> (35:7). The name <em>El-Bethel</em> means '
        '<em>God of the house of God</em> &mdash; identifying the deity by the place where He had '
        'manifested Himself. The pattern recurs throughout the patriarchal narratives: place-names '
        'become theological markers, recording where and how God revealed Himself. Jacob\'s '
        'return-to-Bethel completes the circle that began with his fleeing.</p>'
    ),
    'eutychianism': (
        '<p>The fifth-century Christological heresy that Christ\'s human nature was absorbed into '
        'His divine nature, so He effectively has one (mixed) nature rather than two distinct natures '
        'in one person. Named for Eutyches, an aged archimandrite of Constantinople who taught the '
        'position around 448 AD. Eutyches said that after the union, Christ had <em>one nature</em> &mdash; '
        'the divine having effectively swallowed up the human like a drop of vinegar in the ocean. '
        'The position is the opposite error to Nestorianism (which split Christ into two persons): '
        'where Nestorianism over-distinguishes, Eutychianism over-unifies. The Council of Chalcedon '
        '(451 AD) condemned both: Christ is one person in two natures, <em>without confusion, without '
        'change, without division, without separation</em>. The Chalcedonian definition has been the '
        'orthodox standard ever since. Eutychianism, in its modified form Monophysitism, survives in '
        'the Coptic, Ethiopian, Syrian, and Armenian Orthodox churches. The doctrinal point matters: '
        'if Christ\'s human nature was absorbed, He cannot fully represent humanity in His atoning '
        'work.</p>'
    ),
    'evening-examen': (
        '<p>The nightly discipline of reviewing the day with God &mdash; tracing His mercies, '
        'confessing the day\'s sins, and entrusting tomorrow to His keeping. The practice has roots '
        'in Psalm 4:4 (<em>commune with your own heart upon your bed, and be still</em>) and in '
        'Psalm 119:55, 62 (<em>I have remembered thy name, O LORD, in the night... At midnight I '
        'will rise to give thanks unto thee because of thy righteous judgments</em>). The medieval '
        'monastic practice developed the discipline; Ignatius of Loyola formalized it as the '
        '<em>Examen</em> in his Spiritual Exercises. The Protestant Puritan tradition independently '
        'cultivated similar practice. A typical examen has five movements: (1) gratitude for the '
        'day\'s mercies; (2) prayer for the Spirit\'s light; (3) review of the day from morning to '
        'evening; (4) confession of failures and reception of forgiveness; (5) anticipation and '
        'entrustment of tomorrow. The conscience cleared before sleep is the conscience available '
        'for tomorrow\'s discipleship.</p>'
    ),
    'financial-stewardship': (
        '<p>The discipline of managing money as a trustee accountable to God. The biblical pattern: '
        'all money belongs to the LORD (Ps 24:1; 50:10-12); the believer is steward, not owner '
        '(Luke 16:1-13); faithfulness in little leads to authority over much (Luke 16:10); generosity '
        'to the poor and to the kingdom expresses gospel-shaped values (2 Cor 9:6-7); the love of '
        'money is a root of all kinds of evil (1 Tim 6:10). Christ\'s teaching on money is more '
        'extensive than His teaching on prayer or heaven; biblical financial stewardship is not '
        'optional. Core practices: regular giving (the OT pattern of the tithe as a starting point, '
        'the NT pattern of cheerful proportionate generosity); freedom from debt as a working ideal '
        '(Rom 13:8); saving for foreseeable needs (Prov 21:20); investment for future generations '
        '(Prov 13:22); refusal of love-of-mammon (Matt 6:24); accountability within marriage and '
        'church. The biblical man\'s checkbook reveals his actual loves more accurately than his '
        'mouth does.</p>'
    ),
    'haggai': (
        '<p>The tenth of the twelve Minor Prophets, a short two-chapter post-exilic prophecy dated '
        'precisely to the second year of Darius (520 BC), some sixteen years after the first '
        'returnees from Babylon had begun rebuilding the temple but had then stopped under '
        'opposition. Haggai\'s message rebuked the people for misplaced priorities: they had built '
        'their own paneled houses while the LORD\'s house lay in ruins. <em>Is it time for you, O '
        'ye, to dwell in your cieled houses, and this house lie waste? Now therefore thus saith the '
        'LORD of hosts; Consider your ways</em> (1:4-5). The people responded; the rebuilding '
        'resumed within twenty-three days of Haggai\'s first oracle. The book has four short '
        'oracles, each precisely dated. The climactic promise (2:6-9) anticipates Messiah\'s arrival '
        'and a glory of the latter temple greater than the former &mdash; fulfilled when Christ '
        'Himself walked in the second-temple courts. Haggai\'s ministry, brief and pointed, '
        'demonstrates the impact a clear prophetic word can have on a wavering generation.</p>'
    ),
    'hallelujah-acclamation': (
        '<p>The Hebrew imperative summons to praise the LORD &mdash; <em>halal-yah</em> (praise '
        'YHWH). The most concentrated worship-word in Scripture, used throughout the Psalms (24 '
        'times, mostly in Pss 104-118 and 146-150). Psalm 150 alone has the word four times. The '
        'NT preserves the Hebrew transliterated (<em>hallelouia</em>) without translation, '
        'preserving the word\'s ancient power. Revelation 19:1, 3, 4, 6 thunders the word four '
        'times at the climactic wedding of the Lamb &mdash; the only place in the NT where '
        'Hallelujah appears, fittingly at the eschatological consummation. The Hallel (Psalms '
        '113-118, sung at Passover and other festivals) was almost certainly what Christ and the '
        'disciples sang after the Last Supper (Matt 26:30: <em>when they had sung an hymn, they '
        'went out into the mount of Olives</em>). The Christian inheritance includes the same '
        'word, the same praise, the same orientation: Hallelujah is the church\'s eternal '
        'vocabulary.</p>'
    ),
    'heart-anxious': (
        '<p>An anxious heart is one fragmented by worry &mdash; pulled in many directions at once, '
        'unable to settle, distracted from the kingdom. Christ devoted significant teaching to it '
        'in the Sermon on the Mount (Matt 6:25-34): <em>Take no thought for your life... which of '
        'you by taking thought can add one cubit unto his stature?... seek ye first the kingdom of '
        'God, and his righteousness; and all these things shall be added unto you.</em> Paul\'s '
        'prescription is fourfold and definitive: <em>Be careful for nothing; but in every thing '
        'by prayer and supplication with thanksgiving let your requests be made known unto God. '
        'And the peace of God, which passeth all understanding, shall keep your hearts and minds '
        'through Christ Jesus</em> (Phil 4:6-7). The remedy is not denial of the difficulty but '
        'specific replacement: anxious thoughts replaced by prayed-and-thanked specific requests; '
        'the result is God\'s peace garrisoning heart and mind. The anxious heart is not destined '
        'to remain anxious; the path out is named.</p>'
    ),
    'joel-book': (
        '<p>The second of the twelve Minor Prophets, a short three-chapter prophecy reading a '
        'devastating locust invasion of Judah as a sign of the coming Day of the LORD. Joel\'s date '
        'is debated &mdash; proposals range from the pre-exilic ninth century to the post-exilic '
        'fifth century. The book\'s structure: (1) chapter 1 describes the locust devastation; '
        '(2) chapter 2 amplifies the locusts into the eschatological day of judgment, calls Israel '
        'to repentance, and promises the Spirit\'s outpouring on all flesh; (3) chapter 3 (Hebrew '
        '4) narrates the final judgment of the nations and the restoration of Judah. Joel 2:28-32 '
        'is the canonical Pentecost prophecy: <em>And it shall come to pass afterward, that I will '
        'pour out my spirit upon all flesh; and your sons and your daughters shall prophesy, your '
        'old men shall dream dreams, your young men shall see visions.</em> Peter explicitly cited '
        'this passage at Pentecost (Acts 2:16-21) as the inaugurating fulfillment of Joel\'s '
        'promise. The locusts that ravaged ancient Judah became the typological signal of the '
        'Spirit-poured-out age.</p>'
    ),
    'laver-bronze': (
        '<p>The bronze washing basin in the tabernacle court, between the bronze altar and the holy '
        'place. Exodus 30:17-21 specifies the requirement: priests had to wash their hands and feet '
        'in the laver before entering the tabernacle or approaching the altar to serve, <em>that '
        'they die not</em> (Ex 30:20). The laver was made from the bronze mirrors donated by the '
        'women who served at the door of the tabernacle (Ex 38:8) &mdash; a beautiful sacrificial '
        'gift. Solomon\'s temple expanded this with the great <em>molten sea</em> (1 Kgs 7:23-26) '
        'plus ten smaller lavers on movable stands. The typology runs forward: Christ\'s washing of '
        'the disciples\' feet (John 13) reframes the priestly washing as ongoing cleansing within '
        'an already-clean relationship; baptismal washing (Acts 22:16; Eph 5:26: <em>that he might '
        'sanctify and cleanse it with the washing of water by the word</em>); the eschatological '
        'sea of glass before the throne (Rev 4:6) is the consummated reality. Approach to God '
        'requires cleansing.</p>'
    ),
    'laying-on-hands': (
        '<p>The apostolic act of imparting blessing, healing, commissioning, or the Holy Spirit '
        'through prayerful touch. The practice is listed among the elementary doctrines of Christ '
        'in Hebrews 6:1-2. Biblical instances span: blessing (Jacob blessing Joseph\'s sons, Gen '
        '48:14; Christ blessing children, Matt 19:13-15); commissioning to office (Moses laying '
        'hands on Joshua, Num 27:18-23; the apostles on the seven, Acts 6:6; Paul and Barnabas '
        'commissioned, Acts 13:3; Timothy ordained, 1 Tim 4:14; 2 Tim 1:6); healing (Jesus '
        'throughout the Gospels, especially Mark 6:5; Acts 28:8); the Spirit\'s outpouring on '
        'specific occasions (Acts 8:17; 19:6). The act is symbolic and yet sacramental in some '
        'sense &mdash; God uses the physical touch as means of conveying the spiritual reality. '
        'Paul\'s warning in 1 Timothy 5:22 (<em>Lay hands suddenly on no man</em>) cautions against '
        'casual or premature use, especially in ordination. The practice continues across most '
        'Christian traditions today.</p>'
    ),
    'megiddo': (
        '<p>The strategic fortress overlooking the Jezreel valley in northern Israel, controlling '
        'the trade route between Egypt and Mesopotamia. Megiddo guarded the pass through the '
        'Carmel range; whoever held Megiddo held northern Israel\'s commercial and military '
        'access. The city was a major site of OT battles: Deborah and Barak defeated Sisera <em>by '
        'the waters of Megiddo</em> (Judg 5:19); Pharaoh Necho killed Josiah at Megiddo '
        '(2 Kgs 23:29-30); Solomon fortified the city (1 Kgs 9:15). Excavations at Tel Megiddo '
        'have revealed at least twenty-six layers of occupation across nearly four millennia &mdash; '
        'one of the most extensively-excavated archaeological sites in Israel. The Hebrew <em>Har '
        'Megiddo</em> (Mount of Megiddo) gives Revelation 16:16 the term <em>Armageddon</em> for '
        'the final apocalyptic gathering: <em>And he gathered them together into a place called in '
        'the Hebrew tongue Armageddon.</em> Whether Armageddon names a literal future battle in '
        'the Megiddo plain or a symbolic global conflict, the geographic name evokes the long '
        'history of battles fought on Israel\'s most contested ground.</p>'
    ),
    'mock': (
        '<p>To make sport of, deride, or treat with derisive imitation. In Scripture the verb '
        'recurs as the consistent response of the wicked to God\'s prophets, to Christ at the '
        'cross, and to truth generally. Galatians 6:7 issues the warning: <em>Be not deceived; God '
        'is not mocked: for whatsoever a man soweth, that shall he also reap.</em> The mockers of '
        '2 Peter 3:3 are described as walking after their own lusts and questioning Christ\'s '
        'return. Christ Himself was repeatedly mocked: by Herod\'s soldiers who dressed Him in '
        'royal robes (Luke 23:11), by the Roman soldiers who crowned Him with thorns (Mark 15:17-20), '
        'by passers-by at the cross (Mark 15:29-31), by the religious leaders (Mark 15:31), by '
        'one of the crucified thieves (Luke 23:39). Elisha was mocked by the young men of Bethel '
        '(2 Kgs 2:23) &mdash; two she-bears killed forty-two of them. The biblical pattern: '
        'mocking God\'s servants is mocking God; vindication comes, sometimes immediately, often '
        'finally.</p>'
    ),
    'ordinary-time': (
        '<p>The non-festal weeks of the Christian liturgical year &mdash; the seasons between the '
        'major feast-cycles. The Western Christian year has two stretches of Ordinary Time: the '
        'weeks between Epiphany and Lent (a shorter stretch, usually January through February), '
        'and the longer stretch between Pentecost / Trinity Sunday and Advent (most of June through '
        'November). During Ordinary Time, lectionary readings cycle through extended passages of '
        'the Gospels and Epistles without the focused thematic emphasis of the festal seasons. The '
        'name <em>ordinary</em> is sometimes misunderstood as suggesting these weeks are unimportant; '
        'in fact, they are <em>ordinal</em>, simply numbered (the third week, the seventh week, '
        'etc.) and pastorally significant: most of Christian life is lived in ordinary time, in '
        'the long-arc faithfulness between the highlight moments. The Reformed and Evangelical '
        'traditions have not always adopted the term, but the practical reality is universal &mdash; '
        'the church spends most of its year in the long stretches between Christmas and Easter and '
        'between Pentecost and Advent.</p>'
    ),
    'orphan-widow-defense': (
        '<p>The church\'s biblical duty to visit, protect, and provide for the fatherless and '
        'bereaved. James 1:27 names it as the test of true religion: <em>Pure religion and '
        'undefiled before God and the Father is this, To visit the fatherless and widows in their '
        'affliction, and to keep himself unspotted from the world.</em> The OT framework is '
        'extensive: the LORD is repeatedly named as the Defender of orphan and widow (Deut 10:18; '
        'Ps 68:5; 146:9). The harvest-corner-gleaning provisions (Lev 19:9-10; Deut 24:19-21) '
        'provided for them in agrarian society. The tri-annual tithe was for them (Deut 14:28-29). '
        'The NT continues the theme: the church established orderly care for widows (1 Tim 5:3-16, '
        'Paul\'s extended pastoral instruction on widow-ministry, distinguishing those with family '
        'support from those genuinely in need). The believer\'s actual life of orphan-and-widow '
        'care is, per James, the visible test of his religion. Religion that fails this test, '
        'whatever else it does, is not the kind God accepts.</p>'
    ),
    'pastoral-character': (
        '<p>The qualifications and dispositions of one who shepherds Christ\'s flock. Three NT '
        'passages give the foundational lists: 1 Timothy 3:1-7 (overseer / bishop), Titus 1:5-9 '
        '(elder), and 1 Peter 5:1-4 (elder under the Chief Shepherd). Core requirements: above '
        'reproach; husband of one wife; sober, temperate, gentle, patient, not violent, not greedy '
        'of filthy lucre; hospitable; apt to teach; ruling well his own house and having his '
        'children in subjection; not a novice; well-reported of those who are without; lover of '
        'good men; just, holy, temperate; holding fast the faithful word. The lists are character-'
        'oriented, not skill-oriented &mdash; the church does not need clever men in its pulpits, '
        'it needs sanctified men whose lives match their teaching. The qualifications are '
        'cumulative; a man failing significantly in one disqualifies for office regardless of '
        'gifting in the others. The pastoral character matters more than the pastoral ability; '
        'character without ability can still serve the flock, ability without character harms it.</p>'
    ),
}

BD_RE = re.compile(r'(<div class="biblical-def">)(.*?)(</div>)', re.DOTALL)


def patch(slug, new_inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return False, 'file missing'
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_html, n = BD_RE.subn(rf'\g<1>\n                {new_inner}\n            \g<3>', html, count=1)
    if n == 0:
        return False, 'pattern not matched'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'


def main():
    ok, fail = 0, 0
    for slug, new in EXPANSIONS.items():
        success, reason = patch(slug, new)
        if success: ok += 1
        else:
            fail += 1
            print(f'  FAIL {slug}: {reason}')
    print(f'Expanded {ok}/{ok+fail} entries')


if __name__ == '__main__':
    main()
