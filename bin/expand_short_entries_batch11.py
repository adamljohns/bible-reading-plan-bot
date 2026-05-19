#!/usr/bin/env python3
"""Batch 11 — expand 25 more thin entries."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'golden-lampstand': (
        '<p>The seven-branched golden candelabrum (Hebrew <em>menorah</em>) in the Holy Place of the '
        'tabernacle and later Solomon\'s temple, providing the only light in the holy space. Exodus '
        '25:31-40 details its construction: a single piece of pure gold beaten into a central shaft with '
        'six branches (three on each side), each shaft adorned with almond-blossom cups and ornaments. '
        'Aaron was to dress the lamps morning and evening with pure beaten olive oil so they burned '
        'continually before the LORD (Ex 27:20-21). Zechariah\'s vision (Zech 4) gives a golden lampstand '
        'fed directly from two olive trees, signifying the Spirit\'s provision: <em>Not by might, nor by '
        'power, but by my spirit, saith the LORD of hosts.</em> Revelation 1-2 sees Christ standing among '
        'seven golden lampstands which are the seven churches &mdash; the church is the light-bearer in '
        'the world, fed by the oil of the Spirit, and Christ Himself walks among the assemblies.</p>'
    ),
    'heir-with-christ': (
        '<p>The status of every believer through adoption: heir of God and joint-heir with Christ, '
        'sharing His inheritance of all things. Romans 8:16-17: <em>The Spirit itself beareth witness '
        'with our spirit, that we are the children of God: And if children, then heirs; heirs of God, '
        'and joint-heirs with Christ; if so be that we suffer with him, that we may be also glorified '
        'together.</em> Galatians 4:7: <em>Wherefore thou art no more a servant, but a son; and if a '
        'son, then an heir of God through Christ.</em> Hebrews 1:2 identifies the basis: <em>God... '
        'hath in these last days spoken unto us by his Son, whom he hath appointed heir of all things.</em> '
        'Christ\'s inheritance is universal (all things); the believer\'s share is in Christ. Ephesians '
        '3:6 makes the Gentile inclusion explicit. The doctrine grounds the breathtaking scope of '
        'Christian hope: not survival of judgment but inheritance of the cosmos under Christ\'s reign.</p>'
    ),
    'immigrant-stranger': (
        '<p>The sojourner among God\'s people, the resident alien who lives within the covenant '
        'community without belonging to it by blood. Hebrew <em>ger</em>. The command is direct and '
        'repeated: <em>Thou shalt neither vex a stranger, nor oppress him: for ye were strangers in the '
        'land of Egypt</em> (Ex 22:21); <em>And if a stranger sojourn with thee in your land, ye shall '
        'not vex him. But the stranger that dwelleth with you shall be as one born among you, and thou '
        'shalt love him as thyself; for ye were strangers in the land of Egypt: I am the LORD your '
        'God</em> (Lev 19:33-34); <em>For the LORD your God... loveth the stranger, in giving him food '
        'and raiment. Love ye therefore the stranger: for ye were strangers in the land of Egypt</em> '
        '(Deut 10:18-19). The principle binds the church across the centuries: love the stranger, '
        'remembering that you were once one. The biblical posture also acknowledges the magistrate\'s '
        'real prudential authority to order immigration policy (Rom 13:1-4); kindness to the sojourner '
        'present is one duty, prudence in policy is another, and both stand together.</p>'
    ),
    'jonah-book': (
        '<p>The fifth of the twelve Minor Prophets, a four-chapter narrative prophecy unique in the OT '
        'for being almost entirely a story rather than oracle. The prophet Jonah ben Amittai (mentioned '
        'historically in 2 Kgs 14:25) was called to preach against the great Assyrian city Nineveh; he '
        'fled west by sea to Tarshish, was thrown overboard during a storm, was swallowed by a great '
        'fish, prayed from the fish\'s belly, was vomited up on dry land, preached the eight-word sermon '
        '(<em>Yet forty days, and Nineveh shall be overthrown</em>, 3:4), saw the entire city repent '
        'from king to commoner, and then pouted bitterly that the LORD had relented from destroying His '
        'enemies. The book is theologically loaded: God\'s mercy reaches even violent Gentile empires, '
        'God uses unwilling prophets to accomplish His purposes, God rebukes the prophet who resents '
        'grace shown to outsiders. Christ Himself authenticates the historicity (Matt 12:39-41), tying '
        'Jonah\'s three days in the fish to His own three days in the tomb.</p>'
    ),
    'journaling': (
        '<p>The discipline of writing what God speaks, what the soul wrestles, and what providence '
        'reveals &mdash; recording the inner life so that the believer\'s formation is examined and '
        'preserved. The biblical pattern is rich: David\'s Psalms are journaled prayers; Lamentations '
        'is journaled grief; Paul\'s prison letters carry journaled reflection. Habakkuk records a '
        'direct command: <em>And the LORD answered me, and said, Write the vision, and make it plain '
        'upon tables, that he may run that readeth it</em> (Hab 2:2). The Christian who journals does '
        'three things at once: he slows long enough to actually feel and think (the act of writing '
        'forces the mind to settle); he creates a record of God\'s dealings he can return to in '
        'darker seasons; and he disciplines emotion by naming it precisely. Many of the great '
        'spiritual masters across the centuries (Augustine, John Bunyan, Susanna Wesley, Jim Elliot, '
        'Bonhoeffer) journaled and left the records as gifts to subsequent generations.</p>'
    ),
    'kindred': (
        '<p>Family, relatives, kin. Hebrew <em>moledet</em> (kindred, native country, relations) and '
        '<em>mishpachah</em> (clan, family). Abram was called by God from his <em>kindred</em> (Gen '
        '12:1): <em>Get thee out of thy country, and from thy kindred, and from thy father\'s house, '
        'unto a land that I will shew thee.</em> The departure from kindred was costly &mdash; in the '
        'ancient world, kindred-relations meant inheritance, security, social standing, and identity. '
        'Boaz is identified as kindred to Naomi\'s deceased husband (Ruth 2:1, 3), establishing his '
        'qualification as kinsman-redeemer. The eschatological climax of the kindred-theme is at Rev '
        '5:9 and 7:9 &mdash; <em>thou hast redeemed us to God by thy blood out of every kindred, and '
        'tongue, and people, and nation</em>. The gospel\'s reach extends to every kindred. The '
        'church-as-family supersedes blood-kindred when the two conflict (Matt 10:34-37), but in their '
        'right ordering both stand: family of origin and family of faith.</p>'
    ),
    'king-of-glory': (
        '<p>The royal title used in Psalm 24, announcing the LORD\'s entrance through the gates as '
        'warrior-King returning in triumph. The psalm asks the question and gives the answer in '
        'fivefold repetition: <em>Lift up your heads, O ye gates; and be ye lift up, ye everlasting '
        'doors; and the King of glory shall come in. Who is this King of glory? The LORD strong and '
        'mighty, the LORD mighty in battle</em> (vv. 7-8). The repetition climaxes with <em>The LORD '
        'of hosts, he is the King of glory</em> (v. 10). The psalm has been used liturgically across '
        'Christian history for Ascension Day and for processions of the ark, with later application '
        'to Christ\'s triumphal ascent to the Father\'s right hand. The King-of-Glory title combines '
        'covenant lordship (the LORD), military victory (mighty in battle, LORD of hosts), and royal '
        'authority (the gates of the city open before Him). Christ Himself fulfills the title at His '
        'enthronement; the gates of heaven open before the returning Conqueror.</p>'
    ),
    'kinsman-near': (
        '<p>The kinsman near enough in family relation to qualify as <em>goel</em> (kinsman-redeemer), '
        'with the legal right and obligation to redeem a relative\'s property, raise up seed for a '
        'deceased childless brother, or avenge the blood of a murdered kinsman. Levitical law '
        '(Lev 25:23-55) and the levirate provisions (Deut 25:5-10) establish the role. The canonical '
        'narrative is Ruth 3-4: Boaz is a kinsman-redeemer for Naomi\'s family, but there is a nearer '
        'kinsman who has the first right of refusal. Boaz brings the case to the gate before ten '
        'elders; the unnamed nearer kinsman initially accepts the property but declines when he '
        'learns the levirate obligation comes with Ruth the Moabitess. He removes his shoe, the '
        'transaction is sealed, and Boaz redeems both the property and Ruth, marrying her and '
        'producing Obed, grandfather of David and ancestor of Christ. The kinsman-near figure is the '
        'foil that highlights Boaz\'s willingness; the gospel pattern: where the law-bound near '
        'kinsman declined the cost, the willing kinsman-redeemer paid in full.</p>'
    ),
    'liturgical-calendar': (
        '<p>The Christian year structured around the major events of redemption. The standard Western '
        'cycle begins with Advent (four Sundays before Christmas), continues through Christmas (the '
        'twelve days from December 25 to January 5), Epiphany (January 6 onward), pre-Lent / Ordinary '
        'Time, Ash Wednesday and Lent (forty days before Easter), Holy Week (Palm Sunday through Holy '
        'Saturday), Easter (a fifty-day season ending at Pentecost), Pentecost, Trinity Sunday, and '
        '<em>Ordinary Time</em> running through the rest of the year. Christ\'s life and work shape '
        'the year: His coming (Advent), His birth (Christmas), His manifestation (Epiphany), His '
        'fasting and passion (Lent and Holy Week), His resurrection (Easter), His ascension and the '
        'Spirit (Pentecost). The calendar guides preaching rotations, Scripture readings, hymn '
        'selections, and household devotional practice across the year. Liturgical traditions observe '
        'it formally; Reformed and Evangelical traditions vary, but many have recovered the major '
        'feast-days at minimum. The calendar shapes Christian memory across generations.</p>'
    ),
    'modesty-clothing': (
        '<p>The holy restraint that clothes the body to honor God and neighbor. 1 Timothy 2:9: <em>In '
        'like manner also, that women adorn themselves in modest apparel, with shamefacedness and '
        'sobriety; not with broided hair, or gold, or pearls, or costly array.</em> Paul lists '
        'modesty first, before any specific instruction on hair or ornament. The Greek <em>kosmios</em> '
        '(orderly, well-arranged) and <em>aidos</em> (reverence, shame in the good sense) together name '
        'the disposition: dress that honors the body as God\'s creation without inviting either lust '
        '(from outside) or pride (from within). 1 Peter 3:3-4 sets the comparative standard: the '
        'outward adorning is secondary to the unfading inward ornament of a meek and quiet spirit. '
        'Modesty applies to both sexes (1 Tim 2:8 addresses men first); cultural specifics vary, but '
        'the principle (clothe the body to neither display nor provoke) is invariant. The modern '
        'Christian recovery of modesty is part of the broader recovery of Christian aesthetics over '
        'against the sexualization of nearly every public space.</p>'
    ),
    'nestorianism': (
        '<p>The fifth-century Christological heresy that Christ is two persons &mdash; one divine, one '
        'human &mdash; loosely joined in conjunction rather than personally united in one '
        'incarnate Son. Named for Nestorius, Patriarch of Constantinople (428-431 AD), whose objection '
        'to calling Mary <em>theotokos</em> (God-bearer) precipitated the controversy. Nestorius held '
        'that Mary bore only the human nature of Christ, not the divine Son &mdash; effectively '
        'severing the personal unity of Christ into two distinct subjects. Cyril of Alexandria led the '
        'orthodox response: Christ is one person, the eternal Son, who took on a complete human '
        'nature; the personal subject of all His acts (whether divine or human) is the one Son. The '
        'Council of Ephesus (431 AD) condemned Nestorius and deposed him; the Council of Chalcedon '
        '(451 AD) reinforced with its definition: Christ is one person in two natures (divine and '
        'human), without confusion, change, division, or separation. The Assyrian Church of the East '
        'still bears Nestorian heritage. The Nestorian error is alive whenever Christian teaching '
        'implies Christ\'s natures are two persons rather than one.</p>'
    ),
    'othniel': (
        '<p>The first of the judges of Israel, nephew (and son-in-law) of Caleb. Judges 1:12-13 and '
        '3:7-11 narrate his story. Othniel won Caleb\'s daughter Achsah by capturing Kiriath-sepher, '
        'and later, when Israel had served Cushan-rishathaim king of Mesopotamia for eight years, the '
        'Spirit of the LORD came upon Othniel, he went to war, and the LORD delivered the Mesopotamian '
        'king into his hand. <em>And the land had rest forty years. And Othniel the son of Kenaz '
        'died</em> (Judg 3:11). Othniel is the prototype of the Judges-cycle: Israel sins, oppression '
        'follows, Israel cries to the LORD, the LORD raises up a deliverer, the deliverer subdues the '
        'enemy, the land has rest until the deliverer dies and the cycle begins again. Othniel is '
        'notably the only judge presented without significant character-flaw &mdash; subsequent '
        'judges (Ehud, Gideon, Jephthah, Samson) all have substantial moral complications. Othniel '
        'stands at the head of the line as the simplest, cleanest model of Spirit-empowered '
        'deliverance.</p>'
    ),
    'passive-obedience': (
        '<p>Christ\'s submission to the curse of the law and the wrath of God in His suffering and '
        'death &mdash; bearing the penalty due to His people. Distinguished theologically from '
        '<em>active obedience</em> (Christ\'s perfect lifelong fulfillment of the law that earned '
        'positive righteousness). Both are essential and inseparable. Galatians 3:13: <em>Christ hath '
        'redeemed us from the curse of the law, being made a curse for us: for it is written, Cursed '
        'is every one that hangeth on a tree.</em> Isaiah 53:5: <em>he was wounded for our '
        'transgressions, he was bruised for our iniquities: the chastisement of our peace was upon '
        'him; and with his stripes we are healed.</em> 1 Peter 2:24: <em>Who his own self bare our '
        'sins in his own body on the tree.</em> The Christian\'s sins are not just forgiven but '
        'transferred &mdash; reckoned to Christ on the cross, the penalty paid in full there. Together '
        'with His active obedience, Christ\'s passive obedience constitutes the complete work of '
        'atonement: penalty paid (passive) and righteousness earned (active), both imputed to the '
        'believer through faith.</p>'
    ),
    'phylactery': (
        '<p>Small leather boxes containing miniature Scripture scrolls, bound by Jewish men on the '
        'forehead and arm in literal fulfillment of Deut 6:8 (<em>thou shalt bind them for a sign '
        'upon thine hand, and they shall be as frontlets between thine eyes</em>; cf. Ex 13:9, 16; '
        'Deut 11:18). Hebrew <em>tefillin</em>. The boxes contained passages from the Torah, '
        'especially the Shema (Deut 6:4-9), and were worn during morning prayer. The commandment itself '
        'is debated as to whether it intends literal frontlet-binding or metaphorical heart-binding of '
        'God\'s words; second-temple Judaism interpreted it literally and elaborated the practice. '
        'Christ\'s criticism in Matthew 23:5 was not of phylacteries as such but of Pharisees who '
        '<em>make broad their phylacteries, and enlarge the borders of their garments</em> &mdash; '
        'enlarging the visible markers for display rather than for genuine devotion. The internal '
        'principle remains binding: God\'s Word kept before the eyes, in the hand, on the heart; the '
        'external particular forms may vary.</p>'
    ),
    'pillar-of-fire': (
        '<p>The visible nighttime presence of YHWH leading Israel through the wilderness. Exodus '
        '13:21-22: <em>And the LORD went before them by day in a pillar of a cloud, to lead them the '
        'way; and by night in a pillar of fire, to give them light; to go by day and night: He took '
        'not away the pillar of the cloud by day, nor the pillar of fire by night, from before the '
        'people.</em> The pillar combined two functions: visible guidance (Israel followed its '
        'movement) and visible presence (the LORD Himself accompanying His people). At the Red Sea, '
        'the pillar moved behind Israel to separate them from the pursuing Egyptians (Ex 14:19-20). '
        'During the wilderness years, the pillar rested over the tabernacle by day and night; when '
        'it lifted, Israel moved; when it settled, Israel camped (Num 9:15-23). The pillar disappears '
        'from the narrative after the conquest, replaced by the manifest glory of the LORD filling the '
        'tabernacle and later Solomon\'s temple. Christ Himself as the light of the world (John 8:12) '
        'and the Spirit\'s indwelling presence (Rom 8:9) fulfill the pillar\'s typology.</p>'
    ),
    'reveal': (
        '<p>To unveil what was hidden. The Greek <em>apokalupto</em> (uncover, disclose) and its noun '
        '<em>apokalypsis</em> (unveiling, revelation) name the divine act. Scripture distinguishes '
        '<em>general revelation</em> (God making Himself known to all humanity through creation, '
        'conscience, and providence &mdash; Ps 19:1; Rom 1:18-20; 2:14-15) and <em>special revelation</em> '
        '(God making Himself known through specific divine speech to His covenant people, climaxing '
        'in Christ &mdash; Heb 1:1-2; John 1:18). The English title <em>Revelation</em> for the last '
        'book of the Bible reflects this: Greek <em>apokalypsis Iesou Christou</em> &mdash; the '
        'unveiling of Jesus Christ. The cultural usage of <em>apocalypse</em> as <em>catastrophe</em> '
        'is a secondary derivation; the primary biblical sense is the unveiling itself, not the '
        'disasters it depicts. Christian revelation is comprehensive: it covers God\'s nature, His '
        'redemptive purposes, the believer\'s identity, the church\'s mission, and the consummation '
        'of all things. Scripture is the church\'s authoritative record of God\'s special revelation, '
        'closed at the apostolic era.</p>'
    ),
    'rule-of-life': (
        '<p>An intentional, written rhythm of practices &mdash; prayer, Word, work, rest, fellowship, '
        'service &mdash; ordered to keep the disciple aligned with Christ over the long haul. The '
        'discipline has roots in monastic tradition (Benedict\'s Rule, c. 530 AD), Eastern Orthodox '
        'practice, and Anglican / Methodist devotional traditions; many evangelical Christians have '
        'recovered the practice without the monastic associations. The Rule of Life is not legalism &mdash; '
        'it does not earn anything from God &mdash; but is the trellis on which the vine of '
        'discipleship grows. Wendell Berry: <em>The vine grows; the trellis does not.</em> A typical '
        'Christian Rule might cover: daily Bible reading + prayer pattern; weekly Lord\'s Day '
        'observance + sabbath rest; monthly fasting + larger reflection; annual reading goals; '
        'committed local church + fellowship; sustained service / vocation; regular giving; physical '
        'health practices; family liturgies and household worship. The Rule is reviewed annually and '
        'adjusted. Christ\'s sanctifying work is the vine; the Rule provides the structure on which '
        'sustained growth happens.</p>'
    ),
    'sabbath-keeping': (
        '<p>The discipline of weekly ceasing from labor to rest in God\'s finished work &mdash; a '
        'rhythm woven into creation (Gen 2:2-3), codified at Sinai (Ex 20:8-11), debated through the '
        'NT (Mark 2:23-28; Col 2:16-17; Heb 4:9-11). The Christian Sabbath is observed on the Lord\'s '
        'Day (Sunday, the day of resurrection) in most Christian traditions, with patterns varying from '
        'rigorous (Puritan strict-Sabbatarianism: only worship and works of necessity / mercy) to '
        'looser (general Lord\'s Day attendance and family rest without specific labor restrictions). '
        'The principle remains invariant: weekly ceasing trains the soul to trust the Provider rather '
        'than to rely on one\'s own ceaseless labor. The Sabbath proclaims theologically that the '
        'world does not depend on me &mdash; I can stop, and creation continues; God\'s good purposes '
        'do not require my unceasing effort. Modern always-on culture (smartphones, weekend work, '
        'leisure-as-consumption) has eroded Sabbath practice in the West; recovery is a significant '
        'pastoral task.</p>'
    ),
    'scoffer': (
        '<p>A person whose habitual posture toward truth, authority, and divine warning is contemptuous '
        'mockery. Hebrew <em>lets</em> (scoffer, scorner). Proverbs returns repeatedly to the type: '
        '<em>Reprove not a scorner, lest he hate thee: rebuke a wise man, and he will love thee</em> '
        '(Prov 9:8); <em>A scorner loveth not one that reproveth him: neither will he go unto the '
        'wise</em> (Prov 15:12); <em>Proud and haughty scorner is his name, who dealeth in proud '
        'wrath</em> (Prov 21:24). 2 Peter 3:3-4 names the eschatological emergence of scoffers: '
        '<em>knowing this first, that there shall come in the last days scoffers, walking after their '
        'own lusts, And saying, Where is the promise of his coming?</em> The scoffer is distinguished '
        'from the honest doubter or the inquiring simple-minded by his settled disposition of '
        'contempt; correction meets mockery, instruction meets sneer, warning meets dismissal. The '
        'biblical counsel is not to keep investing in the scoffer\'s reform but to invest in those '
        'who can still receive correction (Prov 9:8).</p>'
    ),
    'self-discipline': (
        '<p>The ordering of one\'s own appetites, time, words, and habits under God\'s lordship. '
        'Greek <em>egkrateia</em> (self-mastery, temperance). Listed as fruit of the Spirit '
        '(Gal 5:23), required of elders (Titus 1:8), commanded of all believers (2 Pet 1:5-7). Paul\'s '
        'self-description in 1 Corinthians 9:24-27 is the apostolic model: <em>And every man that '
        'striveth for the mastery is temperate in all things... I therefore so run, not as uncertainly; '
        'so fight I, not as one that beateth the air: But I keep under my body, and bring it into '
        'subjection: lest that by any means, when I have preached to others, I myself should be a '
        'castaway.</em> 2 Timothy 1:7: <em>For God hath not given us the spirit of fear; but of '
        'power, and of love, and of a sound mind [self-discipline].</em> Self-discipline is '
        'Spirit-given but humanly practiced: the believer cooperates with the Spirit\'s sanctifying '
        'work through deliberate cultivation of disciplined habits. Without self-discipline, even '
        'genuine faith remains immature; with it, the Christian life takes its proper shape.</p>'
    ),
    'semi-arianism': (
        '<p>The fourth-century midstream Trinitarian party who rejected the full Arian position '
        '(Christ is a created being, not God) but also rejected the Nicene <em>homoousios</em> '
        '(Christ of the same substance as the Father), preferring <em>homoiousios</em> &mdash; a '
        'softer position holding Christ\'s likeness to the Father rather than His ontological '
        'identity-of-substance. The one-letter Greek difference (an iota) between <em>homoousios</em> '
        'and <em>homoiousios</em> gave rise to the proverb that the early church split over a single '
        'letter &mdash; the difference between truly God and merely God-like. The semi-Arians '
        'flourished mid-century between Nicaea (325) and Constantinople (381); some major bishops '
        'and several emperors supported the position. The defeat of the semi-Arian position at the '
        'Council of Constantinople (381 AD) settled Nicene Trinitarianism as the church\'s standing '
        'orthodoxy. The doctrinal lesson: precision in Christology is not pedantic; the difference '
        'between Christ as God and Christ as God-like is the difference between salvation and no '
        'salvation.</p>'
    ),
    'seven-signs': (
        '<p>The seven miraculous signs John\'s Gospel selects from Christ\'s ministry to unveil His '
        'identity. John 20:30-31 names the selective intent: <em>And many other signs truly did Jesus '
        'in the presence of his disciples, which are not written in this book: But these are written, '
        'that ye might believe that Jesus is the Christ, the Son of God; and that believing ye might '
        'have life through his name.</em> The seven: (1) water turned to wine at Cana (John 2:1-11); '
        '(2) the official\'s son healed at Capernaum from a distance (4:46-54); (3) the lame man at '
        'Bethesda healed on the Sabbath (5:1-15); (4) the feeding of the five thousand (6:1-14); '
        '(5) walking on the water (6:16-21); (6) the man born blind healed (9:1-41); (7) the raising '
        'of Lazarus from the dead (11:1-44). Each sign reveals an aspect of Christ\'s identity and is '
        'paired with extended discourse interpreting the sign. The seventh sign (Lazarus) prefigures '
        'Christ\'s own resurrection, the consummating sign that does not technically count as one of '
        'the seven within John\'s scheme but stands as their completion.</p>'
    ),
    'simplicity': (
        '<p>The discipline of single-eyed devotion to God that frees the heart from divided loyalties. '
        'Christ\'s extended teaching in Matthew 6:19-34 sets the pattern: <em>The light of the body is '
        'the eye: if therefore thine eye be single, thy whole body shall be full of light... Take '
        'therefore no thought for the morrow: for the morrow shall take thought for the things of '
        'itself. Sufficient unto the day is the evil thereof.</em> Greek <em>haplotes</em> '
        '(singleness, sincerity, generous undivided focus) appears in 2 Corinthians 11:3: <em>I fear, '
        'lest by any means... your minds should be corrupted from the simplicity that is in Christ.</em> '
        '2 Corinthians 8:2 uses the same word for generous-undivided giving. The disciplined Christian '
        'simplicity is not poverty as such but unencumbered devotion &mdash; the heart so focused on '
        'God\'s kingdom that food, clothing, tomorrow, and possessions lose their tyrannical grip. '
        'The biblical man owns things; things do not own him.</p>'
    ),
    'sincerity-biblical': (
        '<p>Purity of motive &mdash; unmixed, undisguised, free from the fillers of pretense. Greek '
        '<em>eilikrineia</em> (sincerity, purity) literally means <em>tested by sunlight</em> &mdash; '
        'the image is of fine pottery held up to bright light to reveal whether it has been patched '
        'with wax (which would melt under heat). The sincere is what survives the sunlight test. '
        'Required of preaching (2 Cor 2:17: <em>For we are not as many, which corrupt the word of God: '
        'but as of sincerity, but as of God</em>), of love (1 Pet 1:22: <em>see that ye love one '
        'another with a pure heart fervently</em>), of life (Phil 1:10: <em>that ye may be sincere '
        'and without offence till the day of Christ</em>). Christian sincerity is not naivety or '
        'guilelessness in the social sense; it is the absence of hidden manipulative motive. The '
        'sincere Christian wants from his neighbor what he says he wants, says what he means, and '
        'does what he intends. He has stopped using people for ends they don\'t know about.</p>'
    ),
    'tongue-discipline': (
        '<p>The discipline of bridling speech. James 3 is the canonical NT meditation: <em>If any man '
        'offend not in word, the same is a perfect man, and able also to bridle the whole body... the '
        'tongue is a fire, a world of iniquity: so is the tongue among our members, that it defileth '
        'the whole body, and setteth on fire the course of nature... but the tongue can no man tame; '
        'it is an unruly evil, full of deadly poison</em> (vv. 2, 6, 8). Proverbs returns constantly '
        'to the theme: <em>Death and life are in the power of the tongue</em> (18:21); <em>In the '
        'multitude of words there wanteth not sin: but he that refraineth his lips is wise</em> '
        '(10:19); <em>He that hath knowledge spareth his words</em> (17:27). The biblical man\'s '
        'speech is weighed before it leaves the mouth; he refuses gossip, slander, idle words, '
        'flattery, and the casual destruction speech can do. Christ\'s warning is the standard: '
        '<em>every idle word that men shall speak, they shall give account thereof in the day of '
        'judgment</em> (Matt 12:36).</p>'
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
