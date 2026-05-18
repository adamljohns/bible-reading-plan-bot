#!/usr/bin/env python3
"""Expand 25 more thin entries to 90-110 words each (batch 7)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'nahum': (
        '<p>The seventh of the twelve Minor Prophets, a sustained poetic prophecy of the destruction of '
        'Nineveh, capital of the Assyrian Empire, written about 660-630 BC. Nineveh had repented under '
        'Jonah\'s preaching a century earlier (Jonah 3), but by Nahum\'s time had returned to and exceeded '
        'her former cruelty. The book\'s three chapters unfold as a triptych: (1) the LORD\'s character &mdash; '
        'slow to anger but great in power, the avenger of His enemies and refuge of those who trust Him; '
        '(2) the siege of Nineveh, described in vivid detail; (3) the city\'s certain fall and the '
        'rejoicing of nations long oppressed. The prophecy was fulfilled in 612 BC when the Medes, '
        'Babylonians, and Scythians sacked Nineveh so thoroughly that within centuries its location was '
        'forgotten. Nahum demonstrates that God\'s patience is real but not infinite; the same grace that '
        'spared Jonah\'s Nineveh judged Nahum\'s.</p>'
    ),
    'new-jerusalem-city': (
        '<p>The eschatological holy city descending from heaven at the consummation of all things, the '
        'eternal dwelling of God with His redeemed people. Revelation 21:1-22:5 gives the most extensive '
        'description in Scripture. The city descends <em>out of heaven from God, prepared as a bride '
        'adorned for her husband</em> (21:2). Its dimensions are a perfect cube of fifteen hundred miles '
        '(corresponding to the Holy of Holies\' cube-shape), made of pure gold transparent as glass, with '
        'walls of jasper, twelve foundations named for the apostles, twelve gates named for the tribes, '
        'each gate a single pearl. There is no temple, for the LORD God Almighty and the Lamb are its '
        'temple. There is no sun or moon, for the glory of God lightens it. The river of the water of '
        'life flows from the throne; the tree of life bears twelve fruits. There is no more curse. The '
        'New Jerusalem is the Christian\'s eternal home and the bride of Christ in her consummated form.</p>'
    ),
    'obadiah': (
        '<p>The shortest book in the Old Testament, a single chapter (twenty-one verses) prophesying '
        'judgment against Edom. Edom (descendants of Esau, twin brother of Jacob) had a long history of '
        'enmity against Israel/Judah, culminating in their treachery during Jerusalem\'s 586 BC fall to '
        'Babylon, when the Edomites celebrated, plundered, and helped Babylon capture fleeing Judeans. '
        'Obadiah\'s prophecy splits into three movements: (1) verses 1-9, the LORD\'s announcement of '
        'Edom\'s coming destruction despite their seemingly-impregnable mountain stronghold (Petra); '
        '(2) verses 10-14, the indictment for their specific betrayal of brother-Israel; (3) verses 15-21, '
        'the broader Day of the LORD vision in which all nations are judged and the kingdom belongs to '
        'the LORD, culminating in Israel\'s restoration. Edom was eventually destroyed by Nabatean and '
        'later Roman invasions; their territory became the Roman province of Idumea (Herod the Great '
        'was Idumean &mdash; an Edomite ruling over Israel in the providence of God).</p>'
    ),
    'philippians-book': (
        '<p>Paul\'s prison epistle to the church at Philippi, written from Rome about AD 61-62. Philippi '
        '(modern northern Greece) was Paul\'s first European church plant (Acts 16), founded after the '
        'Macedonian-vision call and famous for the conversion of Lydia, the Philippian jailer, and the '
        'midnight earthquake-deliverance. The letter\'s tone is warm and personal; Philippi had supported '
        'Paul materially several times (4:15-16), and the letter\'s purpose includes thanksgiving for a '
        'recent gift carried by Epaphroditus. Four chapters unfold around the recurring theme of joy in '
        'Christ even amid chains: chapter 1 (Paul\'s circumstances and rejoicing); chapter 2 (the great '
        'Christ-hymn of 2:5-11 on Christ\'s self-emptying and exaltation); chapter 3 (Paul\'s pressing '
        'on, counting all things loss for the knowledge of Christ); chapter 4 (peace passing all '
        'understanding, contentment in every state, the I-can-do-all-things-through-Christ verse). One of '
        'the most-loved Pauline letters, often read for spiritual encouragement.</p>'
    ),
    'punctuality': (
        '<p>Keeping appointed times. The practical expression of love-of-neighbor (respect for the other\'s '
        'time) and of integrity in keeping one\'s word (the appointment is a small covenant). Christ\'s '
        '<em>let your communication be, Yea, yea; Nay, nay</em> (Matt 5:37) covers the bound nature of all '
        'commitments, including stated times. Ecclesiastes 3:1: <em>To every thing there is a season, and '
        'a time to every purpose under the heaven.</em> The biblical man\'s yes-at-3pm is yes-at-3pm, not '
        'yes-at-3:20-most-days. Habitual lateness reveals either disordered priorities (other matters '
        'always preempt the appointment), disrespect (the other person\'s time matters less than mine), '
        'or weakness of will (I cannot organize my own movements). Christ Himself moved with deliberate '
        'pace toward His appointed hour. The modern excuses (busy schedule, traffic, last-minute things) '
        'are usually self-deception. The punctual Christian honors his word and his neighbor with the same '
        'small act.</p>'
    ),
    'unteachable': (
        '<p>The heart that refuses instruction. Proverbs returns to this theme repeatedly as a marker of '
        'the fool, the scoffer, and the stiff-necked. Proverbs 12:1: <em>Whoso loveth instruction loveth '
        'knowledge: but he that hateth reproof is brutish.</em> Proverbs 15:5: <em>A fool despiseth his '
        'father\'s instruction: but he that regardeth reproof is prudent.</em> Hosea 4:6: <em>My people '
        'are destroyed for lack of knowledge: because thou hast rejected knowledge, I will also reject '
        'thee.</em> Unteachability is not stupidity; it is a moral posture &mdash; the refusal to receive '
        'correction precisely because correction would require change. The unteachable man can be brilliant; '
        'his problem is not intellect but will. The biblical cure is humility (Prov 11:2; 15:33: <em>before '
        'honour is humility</em>) and the fear of the LORD (which is the beginning of knowledge, Prov 1:7). '
        'The teachable man learns; the unteachable man does not, and his unteachability is itself the '
        'judgment that comes upon him.</p>'
    ),
    'yore': (
        '<p>An archaic English adverb meaning <em>long ago, in olden times</em>. Appears in older English '
        'translations (and once in the KJV preface) but not directly in the KJV text; cognate concept '
        'translated as <em>of old</em>, <em>in days of old</em>, <em>from of old</em>. Hebrew <em>olam</em> '
        '(antiquity, long ago) and <em>qedem</em> (former times, ancient days) carry the underlying sense. '
        'Psalm 77:5: <em>I have considered the days of old, the years of ancient times.</em> Isaiah 63:9: '
        '<em>he bare them, and carried them all the days of old.</em> Micah 5:2: the Messiah\'s goings '
        'forth are <em>from of old, from everlasting.</em> The biblical posture toward <em>yore</em> is not '
        'nostalgia (idealizing a past that did not exist) but memory &mdash; recalling what God has done '
        'as the foundation for trusting what He will do. The discipline of remembering shapes the '
        'discipline of hoping. The Psalmist\'s consideration of days of old is itself a faith-practice.</p>'
    ),
    'confession-personal': (
        '<p>The discipline of specific, honest naming of sin &mdash; to God for cleansing and (in some '
        'forms) to a trusted brother for healing &mdash; rather than vague apologies or self-managed '
        'shame. 1 John 1:9 gives the gospel promise: <em>If we confess our sins, he is faithful and just '
        'to forgive us our sins, and to cleanse us from all unrighteousness.</em> The Greek <em>homologeo</em> '
        '(to say the same thing) names the act: the believer says about his sin what God says about it &mdash; '
        'naming it as sin, not excusing it, not minimizing it, not redefining it. James 5:16 adds the '
        'horizontal dimension: <em>Confess your faults one to another, and pray one for another, that ye '
        'may be healed.</em> Specific personal confession produces specific personal cleansing; vague '
        'confession produces vague forgiveness experienced as guilt-residue. The Christian who has learned '
        'to name his sins specifically before God walks in clearer fellowship with God than the Christian '
        'who has not.</p>'
    ),
    'effectual-call': (
        '<p>The inward, sovereign, Spirit-wrought summons that draws the elect from death to life and '
        'renders the outward gospel call effective in them. Distinguished from the <em>general call</em> '
        '(the outward proclamation of the gospel, which goes to all hearers but can be resisted). Romans '
        '8:30 anchors the doctrine: <em>Moreover whom he did predestinate, them he also called: and whom '
        'he called, them he also justified: and whom he justified, them he also glorified.</em> John 6:44: '
        '<em>No man can come to me, except the Father which hath sent me draw him.</em> 1 Corinthians '
        '1:23-24: Christ crucified is foolishness to those who perish but to <em>them which are called, '
        'both Jews and Greeks, Christ the power of God, and the wisdom of God</em>. The effectual call is '
        'one of the doctrines of grace (the I in TULIP&mdash;irresistible grace). It is not coercion '
        'against the will but the Spirit\'s gracious enabling of the will to embrace what it would '
        'otherwise refuse. The elect always come, because the Spirit always draws them effectually.</p>'
    ),
    'el-yeshuati': (
        '<p>Hebrew <em>El Yeshuati</em>, <em>God of my salvation</em> or <em>The LORD my salvation</em> &mdash; '
        'one of the compound divine-name expressions in the Old Testament. The root <em>yasha</em> (to '
        'save, deliver) is the same root from which the name <em>Yeshua / Jesus</em> derives. Isaiah\'s '
        'song uses the title: <em>Behold, God is my salvation; I will trust, and not be afraid: for the '
        'LORD JEHOVAH is my strength and my song; he also is become my salvation</em> (Isa 12:2). The '
        'expression is personal &mdash; <em>my salvation</em>, not just <em>the savior in general</em>. '
        'Psalm 88:1, 25:5, 27:9, and others use parallel phrases. The deepest expression is when the '
        'Psalmist confesses not just that God provides salvation but that God Himself <em>is</em> his '
        'salvation. Christ as Yeshua (Matt 1:21: <em>thou shalt call his name JESUS: for he shall save '
        'his people from their sins</em>) is the personal embodiment of El-Yeshuati &mdash; the saving '
        'God who became the salvation He gives.</p>'
    ),
    'elijah-figure': (
        '<p>A prophetic forerunner who calls Israel back from idolatry. The pattern unfolds across three '
        'biblical figures. (1) Elijah himself, the ninth-century BC prophet who confronted Baal worship '
        'under King Ahab and Queen Jezebel, called fire from heaven on Mount Carmel (1 Kgs 18), and was '
        'taken up by a whirlwind in a chariot of fire (2 Kgs 2). (2) John the Baptist, prophesied in '
        'Malachi 4:5-6 (<em>Behold, I will send you Elijah the prophet before the coming of the great and '
        'dreadful day of the LORD</em>) and identified by Christ as the Elijah-who-was-to-come (Matt '
        '11:14; 17:11-13). Like Elijah, John dressed roughly, ate desert food, lived ascetic life, and '
        'preached repentance to a culture deep in compromise. (3) An eschatological Elijah-figure '
        'expected at the end (Mal 4:5; many take Rev 11:3-12\'s two witnesses as including this figure). '
        'The Elijah-pattern is therefore not a one-time figure but a recurring office: the prophet who '
        'arrives in dark times to call God\'s people back to the covenant.</p>'
    ),
    'gainsayer': (
        '<p>KJV term for one who contradicts, opposes, or speaks against &mdash; particularly a teacher '
        'who distorts sound doctrine and must be silenced. Titus 1:9 uses the word of elder-qualifications: '
        '<em>Holding fast the faithful word as he hath been taught, that he may be able by sound doctrine '
        'both to exhort and to convince the gainsayers.</em> Romans 10:21 applies it to Israel: <em>But '
        'to Israel he saith, All day long I have stretched forth my hands unto a disobedient and '
        'gainsaying people.</em> The Greek <em>antilego</em> (literally <em>speak against</em>) carries '
        'both the active sense (speaking up in opposition) and the deeper disposition (settled posture '
        'of contradicting God\'s word). The elder\'s task in Titus 1:9 is two-edged: positively to exhort '
        'with sound doctrine, negatively to refute the gainsayer. The biblical pastor cannot only build '
        'up; he must also tear down false teaching when it threatens the flock. Gainsayer-handling is part '
        'of the office.</p>'
    ),
    'gilead': (
        '<p>The mountainous region east of the Jordan River, north of Moab and south of Bashan. Fertile, '
        'wooded, and famous for its <em>balm of Gilead</em> (a healing resin, Jer 8:22). At the conquest, '
        'Gilead was allotted to Reuben, Gad, and the half-tribe of Manasseh (Num 32; Josh 13). Gilead '
        'features in major OT narratives: Jacob crossed the Jabbok in Gilead on his way back to Esau (Gen '
        '31-32); Elijah the Tishbite was from Gilead (1 Kgs 17:1); Jephthah, one of the judges, was a '
        'Gileadite (Judg 11); Jair, another judge, judged Israel from Gilead (Judg 10:3-5); David fled '
        'to Mahanaim in Gilead during Absalom\'s revolt (2 Sam 17:24). The region\'s topography (rugged, '
        'easily defended) and economy (sheep, herds, wool, balm) shaped its biblical role as both refuge '
        'and battlefield. Jeremiah 8:22\'s rhetorical question &mdash; <em>Is there no balm in Gilead? '
        'is there no physician there?</em> &mdash; becomes the spiritual call later spiritualized in the '
        'African-American spiritual: <em>There is a balm in Gilead, to make the wounded whole.</em></p>'
    ),
    'habakkuk': (
        '<p>The eighth of the twelve Minor Prophets, a three-chapter dialogue between the prophet\'s '
        'honest complaint and God\'s answer, dated roughly 605-600 BC, on the eve of Babylon\'s invasion '
        'of Judah. The book\'s structure is unusual among the prophets: Habakkuk begins by asking God why '
        'evil flourishes within Judah unpunished (1:2-4); God answers that He is sending the Babylonians '
        'as judgment (1:5-11); Habakkuk responds with a deeper question &mdash; how can a holy God use a '
        'more wicked nation (Babylon) to judge a less wicked one (Judah)? (1:12-2:1); God answers that '
        'Babylon\'s pride will itself be judged in turn (2:2-20), and that meanwhile <em>the just shall '
        'live by his faith</em> (2:4) &mdash; the verse Paul cites three times in the NT (Rom 1:17; Gal '
        '3:11; Heb 10:38) as the doctrinal foundation of justification by faith. Chapter 3 is Habakkuk\'s '
        'closing psalm-of-trust: <em>Although the fig tree shall not blossom... yet I will rejoice in the '
        'LORD, I will joy in the God of my salvation.</em> Honest questioning followed by Spirit-given '
        'trust.</p>'
    ),
    'haran': (
        '<p>The ancient city in upper Mesopotamia (modern southeastern Turkey) on a tributary of the '
        'Euphrates, important throughout the patriarchal narratives. Terah took Abram, Sarai, and Lot '
        'from Ur of the Chaldees toward Canaan, but stopped at Haran where Terah died (Gen 11:31-32). '
        'Abram\'s actual departure for the promised land was from Haran (Gen 12:4). The city remained '
        'connected to Abraham\'s family: when Abraham sent his servant to find a wife for Isaac, he sent '
        'him back to <em>my country, and to my kindred</em> (Gen 24:4) &mdash; meaning Haran, where '
        'Rebekah was found (Gen 24:10). Years later, Jacob fled from Esau to Haran, where he served Laban '
        'twenty years, married Leah and Rachel, and fathered eleven of the twelve patriarchs (Gen 29-31). '
        'Haran was thus a transitional city in patriarchal pilgrimage: Abraham\'s pause-point before the '
        'land of promise, Isaac\'s wife-source, Jacob\'s long exile and household-formation place. The '
        'city itself was a center of moon-god worship, which deepens the contrast with Abram\'s monotheism.</p>'
    ),
    'jeer': (
        '<p>To mock with raucous shouting &mdash; the noisy public mockery of crowds against an exposed '
        'or defeated target. The biblical instances are sobering. The crowds passing the cross jeered at '
        'Christ: <em>And they that passed by railed on him, wagging their heads, and saying, Ah, thou '
        'that destroyest the temple, and buildest it in three days, Save thyself, and come down from the '
        'cross... Likewise also the chief priests mocking said... He saved others; himself he cannot '
        'save</em> (Mark 15:29-31). Jeremiah recorded the jeering against his prophetic ministry: <em>I '
        'am in derision daily, every one mocketh me</em> (Jer 20:7). The young men of Bethel jeered at '
        'Elisha: <em>Go up, thou bald head; go up, thou bald head</em> (2 Kgs 2:23); two bears came out '
        'of the woods and tore forty-two of them. The biblical pattern: jeering at God\'s servants is '
        'jeering at God; the LORD\'s response is sometimes immediate, sometimes delayed, but always '
        'serious. The disciple who knows he is in good company with Christ and the prophets when jeered '
        'at can endure it.</p>'
    ),
    'jesus': (
        '<p>The proper name of the eternal Son of God incarnate. Greek <em>Iesous</em>, transliterating '
        'Hebrew/Aramaic <em>Yeshua / Yehoshua</em> (Joshua) &mdash; meaning <em>The LORD saves</em> or '
        '<em>Yahweh is salvation</em>. Given by the angel to Joseph: <em>thou shalt call his name JESUS: '
        'for he shall save his people from their sins</em> (Matt 1:21). The name itself encodes the '
        'mission. Christ\'s earthly life unfolds in the four Gospels: born of the Virgin Mary in '
        'Bethlehem; grown up in Nazareth; baptized by John in the Jordan and announced from heaven as the '
        'beloved Son; preached the kingdom of God for three years across Galilee, Samaria, and Judea; '
        'performed miracles authenticating His identity; chose and trained twelve apostles; was rejected '
        'by His own people\'s leaders; was crucified under Pontius Pilate at Passover, AD 30 or 33; rose '
        'bodily the third day; appeared to many witnesses over forty days; ascended to the Father; sent '
        'the Spirit at Pentecost. He is presently seated at the Father\'s right hand interceding for His '
        'people, and will return personally and visibly to consummate the kingdom. His name is the only '
        'name given among men whereby we must be saved (Acts 4:12).</p>'
    ),
    'keep': (
        '<p>To guard, watch over, preserve, observe. The biblical use is bidirectional: God keeps His '
        'people (continuous preservation), and the believer keeps God\'s commandments (continuous '
        'obedience). Hebrew <em>shamar</em> (to keep, guard) and Greek <em>tereo</em> (to keep watch, '
        'preserve) cover the field. Adam was placed in Eden to <em>dress it and to keep it</em> (Gen '
        '2:15) &mdash; the original creational vocation. The priestly blessing prays <em>The LORD bless '
        'thee, and keep thee</em> (Num 6:24). Christ prays in His high-priestly prayer <em>keep through '
        'thine own name those whom thou hast given me</em> (John 17:11). The believer keeps God\'s '
        'commandments (John 14:15: <em>If ye love me, keep my commandments</em>) and is kept by God\'s '
        'power (1 Pet 1:5: <em>kept by the power of God through faith unto salvation</em>). Both '
        'directions are continuous: the believer\'s keeping flows from being kept; being kept produces '
        'the capacity to keep. The Christian life is keeping at every level &mdash; vows, hearts, '
        'commandments, brothers and sisters, the truth once delivered.</p>'
    ),
    'leisure': (
        '<p>Time freed from labor for restoration, worship, and contemplation. The biblical pattern is '
        'rhythmic rest within work, climaxing in the Sabbath. Christ\'s explicit instruction to His '
        'disciples in the press of ministry: <em>Come ye yourselves apart into a desert place, and rest '
        'a while: for there were many coming and going, and they had no leisure so much as to eat</em> '
        '(Mark 6:31). Hebrews 4:9-10 extends the principle theologically: <em>There remaineth therefore '
        'a rest to the people of God. For he that is entered into his rest, he also hath ceased from his '
        'own works, as God did from his.</em> Modern Western culture has both worshipped leisure (the '
        'weekend, retirement, recreation industry) and destroyed it (always-on smartphones, the merger '
        'of work and home, hustle-culture). The biblical pattern reorders both: leisure is real, '
        'commanded, and necessary; but it is leisure <em>for</em> something (worship, family, '
        'restoration, contemplation) not leisure as ultimate goal. The Christian works hard and rests '
        'well, both as parts of one ordered life under God.</p>'
    ),
    'proclamation': (
        '<p>Public announcement &mdash; the gospel\'s primary mode of advance through the world. The '
        'Greek <em>kerusso</em> (to proclaim, herald) and <em>euaggelizo</em> (to announce good news) '
        'together name the apostolic method. Christ\'s ministry began with proclamation: <em>Now after '
        'that John was put in prison, Jesus came into Galilee, preaching the gospel of the kingdom of '
        'God</em> (Mark 1:14). His commission to the apostles is proclamatory: <em>Go ye into all the '
        'world, and preach the gospel to every creature</em> (Mark 16:15). Acts narrates the apostolic '
        'proclamation expanding from Jerusalem through Judea and Samaria to the ends of the earth (Acts '
        '1:8). Paul\'s self-description: <em>For Christ sent me not to baptize, but to preach the '
        'gospel</em> (1 Cor 1:17). The church\'s central task is not therapy, not social transformation, '
        'not religious-experience facilitation &mdash; it is the proclamation of what God has done in '
        'Christ, with the implicit summons to repentance and faith. Where proclamation fades, the church '
        'fades into something else.</p>'
    ),
    'railer': (
        '<p>One given to abusive, slanderous, mocking speech. Greek <em>loidoros</em>. Listed by Paul as '
        'a category of brother whose fellowship the church must refuse: <em>But now I have written unto '
        'you not to keep company, if any man that is called a brother be a fornicator, or covetous, or '
        'an idolater, or a railer, or a drunkard, or an extortioner; with such an one no not to eat</em> '
        '(1 Cor 5:11). The category appears alongside <em>reviler</em> (which translates the same Greek '
        'word in some passages) in 1 Cor 6:10 as one of the categories excluded from inheriting the '
        'kingdom. Railing is not just sharp disagreement, prophetic rebuke, or pointed correction (all '
        'of which are biblical in their place); it is the settled habit of abusive, contemptuous, '
        'character-attacking speech. Peter notes that Christ Himself, <em>when he was reviled, reviled '
        'not again</em> (1 Pet 2:23) &mdash; the model for Christian response to railing. The Christian '
        'does not become the railer he confronts.</p>'
    ),
    'remain': (
        '<p>To stay, continue, abide. The Greek <em>meno</em> (often translated <em>abide</em> in older '
        'English versions) is the verb at the heart of John 15\'s vine-and-branches discourse: <em>Abide '
        'in me, and I in you. As the branch cannot bear fruit of itself, except it abide in the vine; '
        'no more can ye, except ye abide in me</em> (John 15:4). The same word names the believer\'s '
        'remaining in Christ\'s love (John 15:9), in His word (John 8:31), and in the apostolic teaching '
        '(2 John 9). 1 John develops the concept extensively: God remains in the believer; the believer '
        'remains in God; love remains; the truth remains. Remaining is faith\'s persistence &mdash; not '
        'a one-time decision but the ongoing settled state of staying-in-Christ. The branch that does '
        'not remain in the vine cannot bear fruit; the disciple who does not remain in Christ is in the '
        'same position spiritually. Christian assurance is bound to ongoing remaining.</p>'
    ),
    'responsive-reading': (
        '<p>The congregational practice of alternating Scripture reading between leader and people. '
        'Rooted in the antiphonal structure of many Psalms: Psalm 24:7-10 (the gate-keeper / king-of-glory '
        'exchange), Psalm 118 (repeated <em>let Israel say... let the house of Aaron say... let those '
        'who fear the LORD say... that his mercy endureth for ever</em>), Psalm 136 (twenty-six refrains '
        'of <em>for his mercy endureth for ever</em>). The temple choirs were structured antiphonally, '
        'with sections of Levites responding to each other (1 Chr 25; 2 Chr 5:13). Synagogue practice '
        'inherited the pattern; the early church continued it (Eph 5:19: <em>speaking to yourselves in '
        'psalms and hymns and spiritual songs</em>); medieval monastic offices used responsive reading '
        'extensively. Modern liturgical churches preserve the practice; many evangelical and Reformed '
        'congregations have recovered it. The form has theological substance: the reading is shared '
        'rather than only-heard, the congregation actively confesses what is being read, and the call-'
        'and-response embodies the dialogical character of God\'s revealed word and the church\'s answer.</p>'
    ),
    'special-grace': (
        '<p>The saving, regenerating, sanctifying grace given by God only to His elect &mdash; distinguished '
        'from <em>common grace</em>, which is shown to all humanity (the sun rising on the just and the '
        'unjust, the rain falling on the righteous and the unrighteous, Matt 5:45). Special grace is the '
        'grace that actually saves: regenerating the dead heart (Eph 2:1-5), justifying the ungodly '
        '(Rom 4:5), sanctifying the believer over a lifetime, finally glorifying him at Christ\'s return. '
        'Ephesians 2:8-9 is the locus classicus: <em>For by grace are ye saved through faith; and that '
        'not of yourselves: it is the gift of God: Not of works, lest any man should boast.</em> 2 '
        'Timothy 1:9: <em>Who hath saved us, and called us with an holy calling, not according to our '
        'works, but according to his own purpose and grace, which was given us in Christ Jesus before '
        'the world began.</em> Special grace is given in eternity (election), applied in time (effectual '
        'calling, regeneration, faith, justification, sanctification), and consummated in glory '
        '(glorification). Together with common grace, it accounts for everything good in God\'s '
        'relations with humanity.</p>'
    ),
    'titus-book': (
        '<p>Paul\'s pastoral epistle to Titus, written about AD 63-64, charging Titus to establish church '
        'order on the island of Crete. Three short chapters cover: (1) elder qualifications and the need '
        'to silence false teachers, especially the <em>many unruly and vain talkers and deceivers, '
        'specially they of the circumcision</em> (1:10); (2) sound doctrine producing sound living &mdash; '
        'instructions for older men, older women, younger women, younger men, servants, with the great '
        'gospel-summary of 2:11-14 (<em>For the grace of God that bringeth salvation hath appeared to '
        'all men, Teaching us that, denying ungodliness and worldly lusts, we should live soberly, '
        'righteously, and godly, in this present world; Looking for that blessed hope, and the glorious '
        'appearing of the great God and our Saviour Jesus Christ</em>); (3) Christian conduct in the '
        'broader world, the regeneration-through-the-Holy-Ghost passage (3:5), and final greetings. Titus '
        'and 1-2 Timothy together form the Pastoral Epistles, the canonical handbook for church order, '
        'pastoral qualification, and doctrinal-discipline in the local church.</p>'
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
