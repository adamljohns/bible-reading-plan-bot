#!/usr/bin/env python3
"""Expand 25 more short dictionary entries to 90-120 words each (batch 4)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'resurrection-body': (
        '<p>The glorified body the redeemed will receive at Christ\'s return &mdash; the same body raised, '
        'transformed, and made immortal. Paul\'s extended discussion in 1 Corinthians 15:35-58 contrasts the '
        'natural body (Greek <em>soma psychikon</em>) sown in the ground at death with the spiritual body '
        '(<em>soma pneumatikon</em>) that will be raised. The four contrasts: corruption / incorruption, '
        'dishonor / glory, weakness / power, natural / spiritual (vv. 42-44). The resurrection body is not '
        'an immaterial spirit (Christ\'s post-resurrection body had flesh and bone, ate fish, was touched, '
        'Luke 24:39-43) but a transformed physical body fitted for eternal life. Christ\'s resurrection body '
        'is the prototype: <em>we shall be like him; for we shall see him as he is</em> (1 John 3:2). The '
        'Christian hope is not the soul\'s escape from the body but the body\'s resurrection &mdash; the '
        'biblical doctrine that defies both Greek dualism and modern materialism.</p>'
    ),
    'vessel-honor': (
        '<p>Paul\'s image in 2 Timothy 2:20-21: <em>But in a great house there are not only vessels of gold '
        'and of silver, but also of wood and of earth; and some to honour, and some to dishonour. If a man '
        'therefore purge himself from these, he shall be a vessel unto honour, sanctified, and meet for the '
        'master\'s use, and prepared unto every good work.</em> The image is of a household with various '
        'utensils: some used for fine occasions and noble purposes, some for menial and base purposes. The '
        'application is to Christians within the church: by self-purifying from sin and false teaching '
        '(specifically the youthful lusts and idle disputes Paul names in the surrounding verses), the '
        'believer becomes fit for honorable kingdom service. The vessel imagery also recalls Romans 9:21-23, '
        'where the potter\'s authority over the clay applies first to election and second to sanctification. '
        'Vessel of honor is the destination of those who clean their own vessels in cooperation with the '
        'Master.</p>'
    ),
    'mark-5': (
        '<p>The fifth chapter of Mark\'s Gospel, a tight triptych of Christ\'s authority displayed across the '
        'three great enemies: demonic possession, chronic disease, and death itself. The chapter opens with '
        'the Gerasene demoniac (5:1-20), a man so possessed that no chains could hold him; Christ commands '
        'the legion of unclean spirits into the herd of swine and restores the man clothed, in his right '
        'mind, and sent home to testify. Mid-chapter the woman with the twelve-year hemorrhage touches '
        'Christ\'s garment in faith and is healed (5:25-34), an interruption within the larger narrative of '
        'Jairus\' twelve-year-old daughter, whom Christ raises from death with the Aramaic <em>Talitha cumi</em> &mdash; '
        '<em>damsel, arise</em> (5:35-43). The three episodes together display Christ\'s comprehensive '
        'authority: over the spiritual realm, the physical realm, and the realm of death. Mark\'s tightly '
        'compressed account leaves no doubt: this is no ordinary teacher; this is the Lord.</p>'
    ),
    'spirit-adoption': (
        '<p>The Holy Spirit\'s work in assuring believers of their adopted-son standing before God. Romans '
        '8:15-17: <em>For ye have not received the spirit of bondage again to fear; but ye have received the '
        'Spirit of adoption, whereby we cry, Abba, Father. The Spirit itself beareth witness with our spirit, '
        'that we are the children of God: And if children, then heirs; heirs of God, and joint-heirs with '
        'Christ.</em> Galatians 4:5-7 develops the parallel: God sent His Son <em>to redeem them that were '
        'under the law, that we might receive the adoption of sons. And because ye are sons, God hath sent '
        'forth the Spirit of his Son into your hearts, crying, Abba, Father.</em> The Spirit\'s adoption-witness '
        'is not external sentiment but inward testimony &mdash; a settled conviction the Spirit produces in '
        'the believer\'s heart that he is, in fact, God\'s adopted child. <em>Abba</em> is the Aramaic intimate '
        'address (Father, Papa) that Christ Himself used in Gethsemane (Mark 14:36), now placed in the '
        'believer\'s mouth by the same Spirit.</p>'
    ),
    'spirit-truth': (
        '<p>Christ\'s designation for the Holy Spirit in John 14-16, the title connecting the Spirit\'s '
        'specific work of guiding the apostolic church into all truth. John 14:17, 15:26, and 16:13 each use '
        'the title. The fullest statement is John 16:13: <em>Howbeit when he, the Spirit of truth, is come, '
        'he will guide you into all truth: for he shall not speak of himself; but whatsoever he shall hear, '
        'that shall he speak: and he will shew you things to come.</em> The Spirit\'s ministry is specifically '
        'truth-giving: He inspires Scripture (2 Pet 1:21), illuminates Scripture to believers (1 Cor 2:10-14), '
        'and convicts the world of sin, righteousness, and judgment (John 16:8-11). The promise to the '
        'apostles &mdash; that the Spirit would lead them into all truth &mdash; was fulfilled in their '
        'inspired teaching that became the NT. The Spirit of truth still illuminates that same NT for the '
        'church across the ages, and the Spirit\'s witness will never contradict the Scripture He inspired.</p>'
    ),
    'walk-spirit': (
        '<p>Paul\'s command for the entire Christian life. Galatians 5:16: <em>This I say then, Walk in the '
        'Spirit, and ye shall not fulfil the lust of the flesh.</em> The Greek <em>peripateite pneumati</em> '
        'is present-tense imperative &mdash; continuous, daily, settled walking. Romans 8:1-4 develops the '
        'same theme: those who walk after the Spirit have the righteousness of the law fulfilled in them. '
        'Walking is the biblical metaphor for the whole pattern of life &mdash; not occasional spiritual '
        'moments but the steady habituated direction of the daily course. The Spirit is not merely consulted '
        'in emergencies; He is walked-in. The result is two-fold: the works of the flesh are not fulfilled '
        '(Gal 5:16) and the fruit of the Spirit grows (Gal 5:22-23). The walk is enabled by the indwelling '
        'Spirit but is also the believer\'s active responsibility &mdash; the synergy of divine power and '
        'human walking that characterizes the entire Christian life.</p>'
    ),
    'isaiah-53': (
        '<p>The Suffering Servant prophecy &mdash; the clearest OT portrait of the substitutionary atonement '
        'of the Messiah, written some seven hundred years before Christ\'s passion. Isaiah 52:13-53:12 forms '
        'one literary unit (often called the fourth Servant Song). It describes the Servant despised and '
        'rejected, a man of sorrows, wounded for our transgressions, bruised for our iniquities, the LORD '
        'laying on Him the iniquity of us all (53:5-6). His silence before His accusers (53:7) matches '
        'Christ\'s before Pilate (Matt 27:14). His grave with the wicked but with the rich in His death '
        '(53:9) matches Joseph of Arimathea\'s rich man\'s tomb after death between two criminals. The chapter '
        'closes with His resurrection vindication (53:10-11) and intercession for transgressors (53:12). '
        'The Ethiopian eunuch was reading this chapter when Philip met him (Acts 8:32-35) and from this '
        'passage Philip preached unto him Jesus. Isaiah 53 is the cross prophesied with stunning specificity '
        'centuries before the cross occurred.</p>'
    ),
    'james-book': (
        '<p>The general epistle of James, brother of the Lord (Gal 1:19; Acts 15:13) and first leader of the '
        'Jerusalem church. Probably the earliest NT book (c. AD 45-48), James writes to <em>the twelve tribes '
        'scattered abroad</em> (1:1) with a proverbial, practical, sometimes blunt insistence that genuine '
        'faith inevitably produces visible works: <em>faith without works is dead</em> (2:26). The epistle '
        'addresses trials and temptations (ch. 1), partiality (ch. 2), the tongue (ch. 3), worldly friendship '
        '(ch. 4), the rich who exploit, prayer, and patience until the Lord\'s coming (ch. 5). James and '
        'Paul have sometimes been read as contradicting on faith-and-works, but the contradiction is verbal '
        'only: Paul opposes works as the basis of justification before God; James opposes professed-faith '
        'without works as the evidence of genuine justification. Both apostles agree that saving faith '
        'always produces good works; one defends the doctrine on its front edge, the other on its back.</p>'
    ),
    'return-christ': (
        '<p>The personal, bodily, visible return of Jesus Christ to judge the living and the dead and to '
        'consummate the kingdom. The promise is given at the ascension by two men in white apparel: '
        '<em>this same Jesus, which is taken up from you into heaven, shall so come in like manner as ye '
        'have seen him go into heaven</em> (Acts 1:11). Christ Himself promised it (Matt 24:30; John 14:3). '
        'Paul develops the doctrine (1 Thess 4:13-18; 2 Thess 2; 1 Cor 15:23-28; 2 Tim 4:1, 8). Peter (2 Pet '
        '3) and John (Rev 22:20: <em>even so, come, Lord Jesus</em>) end the canon with the same expectation. '
        'Eschatological details vary among orthodox Christian traditions (premillennial, amillennial, '
        'postmillennial; pretribulational, posttribulational), but the personal bodily visible return is '
        'universally affirmed across all orthodox positions. The doctrine has shaped the church\'s posture '
        'of watchful holiness (Titus 2:13: <em>looking for that blessed hope, and the glorious appearing of '
        'the great God and our Saviour Jesus Christ</em>) for twenty centuries.</p>'
    ),
    'revelation-20': (
        '<p>The twentieth chapter of the Revelation, one of the most-discussed and most-contested chapters '
        'in Scripture. It unfolds in four movements: (1) the binding of Satan for a thousand years '
        '(20:1-3); (2) the thousand-year reign of Christ with the martyrs and saints (20:4-6); (3) Satan\'s '
        'release for a final rebellion (20:7-10), ending with his being cast into the lake of fire; and (4) '
        'the great white throne judgment, where the dead are judged out of the books according to their '
        'works, and death and Hades themselves are cast into the lake of fire (20:11-15). The interpretation '
        'of the thousand years is the dividing line among the major eschatological positions: premillennial '
        '(a literal future thousand-year reign after Christ\'s return), amillennial (the present church age '
        'is the symbolic thousand years between the cross and the return), and postmillennial (a future '
        'gospel-golden-age before the return). What is not disputed: the final judgment is real, the lake of '
        'fire is real, and the only safety is to have one\'s name in the book of life.</p>'
    ),
    'tarsus': (
        '<p>The free Roman city in Cilicia (southeastern Asia Minor, modern Turkey) where Paul the apostle '
        'was born and held citizenship (Acts 9:11; 21:39; 22:3). Tarsus was a major commercial and '
        'intellectual center in the first century &mdash; renowned for its philosophical schools (where '
        'Stoicism flourished), its textile industry (Paul\'s trade of tentmaking was probably tied to '
        'Cilicia\'s goat-hair cloth, <em>cilicium</em>), and its strategic position on trade routes between '
        'Asia Minor and Syria. Paul calls it <em>no mean city</em> (Acts 21:39). His Roman citizenship by '
        'birth (Acts 22:28) reflects Tarsus\' status; Cilician cities had received citizenship grants from '
        'various Roman emperors. Paul returned to Tarsus after his conversion and persecution in Jerusalem '
        '(Acts 9:30), and Barnabas later fetched him from there to teach the church at Antioch (Acts 11:25). '
        'The boy from Tarsus became the apostle to the Gentiles, his hometown shaping his unique cross-cultural '
        'reach.</p>'
    ),
    'victory-christ': (
        '<p>The triumph believers share in by union with the risen Christ. 1 Corinthians 15:57: <em>thanks '
        'be to God, which giveth us the victory through our Lord Jesus Christ.</em> The context is the '
        'resurrection chapter\'s climax &mdash; death itself swallowed up in victory through Christ\'s '
        'resurrection-conquest. The Greek <em>nikos</em> (victory) is the same root as Christ\'s repeated '
        'exhortations in Revelation 2-3: <em>to him that overcometh</em> (Greek <em>nikonti</em>, conqueror, '
        'is repeated to every church). Believers are <em>more than conquerors</em> (Greek <em>hypernikomen</em>, '
        'hyper-conquerors) through Him that loved us (Rom 8:37). The victory is comprehensive: over sin '
        '(Rom 6:14), over the law\'s condemnation (Rom 8:1), over the world (1 John 5:4), over the flesh '
        '(Gal 5:24), over death (1 Cor 15:54-55), and finally over Satan himself (Rom 16:20; Rev 12:11). '
        'The victory is not earned by the Christian but received by faith in the One who conquered first.</p>'
    ),
    '1-corinthians-15': (
        '<p>Paul\'s full doctrinal exposition of bodily resurrection &mdash; the chapter that establishes '
        'Christian eschatology more directly than any other. Verses 1-11 rehearse the gospel: Christ died '
        'for our sins according to the scriptures, was buried, rose again the third day according to the '
        'scriptures, appeared to Cephas, the twelve, five hundred brethren at once, James, all the apostles, '
        'and last of all to Paul. Verses 12-34 argue from the fact of Christ\'s resurrection to the necessity '
        'and reality of the believer\'s. Verses 35-49 develop the nature of the resurrection body: sown in '
        'corruption, raised in incorruption; sown in dishonor, raised in glory. Verses 50-58 unfold the '
        'mystery of the rapture/transformation at the trumpet sound and the final triumph: <em>O death, '
        'where is thy sting? O grave, where is thy victory?</em> The chapter is foundational; everything '
        'Paul says in 16:13 about standing fast assumes the resurrection-confidence of chapter 15.</p>'
    ),
    'bitterness': (
        '<p>A settled resentment of soul that refuses forgiveness and poisons community. Hebrews 12:15 issues '
        'the warning: <em>Looking diligently lest any man fail of the grace of God; lest any root of bitterness '
        'springing up trouble you, and thereby many be defiled.</em> The image of <em>root of bitterness</em> '
        'draws on Deuteronomy 29:18, where the LORD warns against any in Israel whose <em>heart turneth away '
        'this day from the LORD our God</em>, becoming <em>a root that beareth gall and wormwood</em>. '
        'Bitterness is not the same as grief or hurt; those are universal human responses to genuine harm. '
        'Bitterness is the settled refusal to release the offense to God\'s justice, the nursing of grievance '
        'until it becomes identity. Paul commands its removal: <em>Let all bitterness, and wrath, and anger, '
        'and clamour, and evil speaking, be put away from you, with all malice: And be ye kind one to '
        'another, tenderhearted, forgiving one another, even as God for Christ\'s sake hath forgiven you</em> '
        '(Eph 4:31-32). The poison spreads from the bitter heart to defile many; the cure is the cross-grounded '
        'release.</p>'
    ),
    'sidon': (
        '<p>The ancient Phoenician city on the Mediterranean coast north of Tyre, in modern Lebanon. Founded '
        'by Sidon, firstborn son of Canaan (Gen 10:15), Sidon was one of the oldest continuously inhabited '
        'cities of the ancient Near East. Its inhabitants were renowned for seamanship, purple-dye production, '
        'glass-making, and woodcraft (Solomon contracted Sidonian craftsmen and cedar for the temple, '
        '1 Kgs 5:6). Sidon stood alongside Tyre as a center of Phoenician trade and Baal worship; both '
        'cities receive prophetic judgment oracles (Ezek 28:20-23; Isa 23). Christ visited the region of '
        'Tyre and Sidon, where the Syrophoenician woman\'s daughter was delivered (Mark 7:24-31), and He '
        'pronounces a striking statement: had the mighty works done in Chorazin and Bethsaida been done in '
        'Tyre and Sidon, they would have repented long ago (Matt 11:21-22). The judgment of those who saw '
        'the works and refused to repent is greater than the judgment of those who never saw them &mdash; '
        'a sobering pattern still in force.</p>'
    ),
    'voice-god': (
        '<p>The Scripture\'s image for God\'s authoritative self-revelation, both audible-historical (at Sinai, '
        'baptism, transfiguration) and ongoing (through Scripture and the Spirit\'s application). Psalm 29 '
        'is the canonical voice-of-God psalm: <em>The voice of the LORD is upon the waters: the God of glory '
        'thundereth... The voice of the LORD is powerful; the voice of the LORD is full of majesty</em> '
        '(vv. 3-4). The voice splits cedars, shakes the wilderness, makes hinds calve. Scripture\'s great '
        'audible-voice moments: God walking and calling in Eden (Gen 3:8-9); Mount Sinai (Ex 20); Elijah\'s '
        'still small voice after the storm (1 Kgs 19:12); the voice at Christ\'s baptism (Matt 3:17) and '
        'transfiguration (Matt 17:5: <em>This is my beloved Son, in whom I am well pleased; hear ye him</em>). '
        'God\'s primary ongoing voice today is His written Word: <em>God, who at sundry times and in divers '
        'manners spake in time past unto the fathers by the prophets, Hath in these last days spoken unto '
        'us by his Son</em> (Heb 1:1-2). The Son has spoken; Scripture preserves what He said.</p>'
    ),
    '3john': (
        '<p>The fourteen-verse epistle by the apostle John, the shortest book in the New Testament. Written '
        'to a beloved church-member named Gaius, the letter has three subjects. First, John praises Gaius '
        'for his faithfulness in extending hospitality to traveling preachers of the gospel (vv. 5-8) &mdash; '
        'a real and costly ministry in the first century, when church planters depended on local Christians '
        'for room, board, and material support. Second, John exposes the failure of one Diotrephes, who '
        '<em>loveth to have the preeminence among them</em> (v. 9), refuses to receive John\'s authority, '
        'speaks malicious words against the apostle, and casts out of the church those who would receive '
        'the traveling brethren. Third, John commends Demetrius for the testimony of <em>all men, and of the '
        'truth itself</em>. The little epistle captures a recurring church dynamic: faithful hospitality, '
        'authority-grasping clergy, and Christ-honoring witness. All three are still present in 2026.</p>'
    ),
    'john-15': (
        '<p>The chapter of the True Vine &mdash; Christ\'s extended metaphor of the believer\'s living '
        'dependence on Him. The chapter falls into three sections. Verses 1-11 are the vine-and-branches '
        'image: Christ the true vine, the Father the husbandman, the believer the branch; abiding produces '
        'fruit, withering produces pruning, the relationship is organic and life-or-death. Verses 12-17 '
        'develop the command of love between the disciples: <em>Greater love hath no man than this, that a '
        'man lay down his life for his friends</em> (v. 13), and Christ\'s declaration that He calls them '
        'no longer servants but friends, having made known to them all He has heard from the Father. Verses '
        '18-27 turn to the world\'s hatred: as the world hated Christ, it will hate His disciples; this is '
        'the cost of bearing His name. Together the chapter holds the deepest comfort (abiding in Christ\'s '
        'love) and the sharpest warning (the world\'s hostility) the believer needs for the long faithfulness.</p>'
    ),
    'tubal-cain': (
        '<p>The pre-flood descendant of Cain remembered in Scripture as the first artificer of bronze and '
        'iron tools. Genesis 4:22: <em>And Zillah, she also bare Tubal-cain, an instructer of every artificer '
        'in brass and iron.</em> Tubal-cain stands as civilization\'s first metallurgist &mdash; the inventor '
        'of edged tools, weapons, and metalwork that would shape every subsequent culture. His placement in '
        'the line of Cain (rather than Seth) is theologically significant: the Genesis 4 narrative shows '
        'the Cainite line as cultural innovators (Jabal the herder, Jubal the musician, Tubal-cain the '
        'metallurgist, v. 21-22) but also as the line of Lamech\'s violence (vv. 23-24). The text portrays '
        'civilization\'s technical advance and moral decline as not opposed but as common products of fallen '
        'human ingenuity apart from God. The flood judgment falls precisely on this advanced and violent '
        'civilization (Gen 6). Tubal-cain reminds the reader that technology, in itself, is not redemption &mdash; '
        'the same metallurgy that builds plowshares also forges swords.</p>'
    ),
    'ekron': (
        '<p>The northernmost of the five great Philistine cities (Gaza, Ashkelon, Ashdod, Gath, Ekron), '
        'located in the coastal plain about 25 miles west of Jerusalem. Ekron features prominently in OT '
        'narrative: the captured Ark of the Covenant was sent to Ekron after disasters at Ashdod and Gath '
        '(1 Sam 5:10); David\'s defeat of Goliath caused the Philistine army to flee toward Ekron (1 Sam '
        '17:52); King Ahaziah of Israel, after falling through a lattice, sent messengers to inquire of '
        '<em>Baal-zebub the god of Ekron</em> (2 Kings 1:2-4), prompting Elijah\'s prophecy of his death. '
        'The name Baal-zebub (<em>lord of flies</em>, possibly a deliberate Hebrew satire of the actual '
        'Philistine deity name) later appears in the NT as Beelzebub, a name applied to Satan as prince of '
        'demons (Matt 12:24-27). Prophetic oracles against Ekron appear in Amos 1:8, Jer 25:20, Zeph 2:4, '
        'and Zech 9:5. Archaeology has identified Ekron with Tel Miqne, where extensive Philistine remains '
        'have been excavated.</p>'
    ),
    'graven-image': (
        '<p>Any sculpted, carved, or molded representation made for worship &mdash; explicitly forbidden in '
        'the second commandment. Exodus 20:4-5: <em>Thou shalt not make unto thee any graven image, or any '
        'likeness of any thing that is in heaven above, or that is in the earth beneath, or that is in the '
        'water under the earth: Thou shalt not bow down thyself to them, nor serve them.</em> The Hebrew '
        '<em>pesel</em> (graven image) names the carved or sculpted object specifically; the commandment\'s '
        'scope extends to all visual representations made <em>for the purpose of worship</em>. Roman Catholic '
        'and Eastern Orthodox traditions distinguish veneration (<em>dulia</em>, given to images of saints '
        'and Christ) from worship (<em>latria</em>, given only to God) &mdash; a distinction Protestant '
        'traditions have generally rejected as drawing a line Scripture does not draw. The commandment cuts '
        'against any practice of bowing before, kissing, lighting candles to, or directing prayer through '
        'a physical image. Even the bronze serpent Moses made at God\'s command became an object of idolatrous '
        'worship in Israel and had to be destroyed by Hezekiah (2 Kgs 18:4). The principle is sweeping: '
        'God will not share His glory with images.</p>'
    ),
    'maundy-thursday': (
        '<p>The Thursday of Holy Week commemorating the events of the Last Supper &mdash; Christ\'s washing '
        'of the disciples\' feet, the institution of the Lord\'s Supper, the upper-room discourse (John '
        '13-17), and the new commandment to love one another as He has loved us (John 13:34). The name '
        '<em>Maundy</em> derives from the Latin <em>mandatum novum</em> (new commandment) of John 13:34, '
        'compressed through Old French into modern English <em>maundy</em>. The day is observed in many '
        'liturgical Christian traditions with foot-washing services (echoing John 13:1-17), the celebration '
        'of communion, and the stripping of the altar in preparation for Good Friday. The Eastern Orthodox '
        'parallel is Holy Thursday. Maundy Thursday begins the Triduum (the three holy days of the Passion), '
        'continuing through Good Friday and ending at Easter. The day frames the cross within Christ\'s own '
        'pre-passion teaching of servant-love &mdash; the kingdom is built not by mastery over others but '
        'by laying-down-of-life for them.</p>'
    ),
    'scorner': (
        '<p>Scripture\'s Proverbs-vocabulary for the man whose disposition toward correction is contempt '
        'rather than receptivity. Hebrew <em>lets</em> (scorner, mocker, scoffer). Proverbs 9:7-8 gives the '
        'diagnostic: <em>He that reproveth a scorner getteth to himself shame: and he that rebuketh a wicked '
        'man getteth himself a blot. Reprove not a scorner, lest he hate thee: rebuke a wise man, and he '
        'will love thee.</em> The scorner is distinguished from the simple (who can be taught) and from '
        'the fool (whose problem is moral, not just intellectual) by his settled disposition: correction '
        'meets contempt, instruction meets mockery, wisdom meets sneer. Proverbs 13:1 contrasts: <em>A wise '
        'son heareth his father\'s instruction: but a scorner heareth not rebuke.</em> Proverbs 21:24 names '
        'the heart-condition: <em>Proud and haughty scorner is his name, who dealeth in proud wrath.</em> '
        'The scorner is the man pride has hardened past learning. The biblical counsel is not to keep '
        'trying to reach him; it is to invest correction-energy in the teachable.</p>'
    ),
    'sneer': (
        '<p>The silent or near-silent facial expression of contempt &mdash; mockery without words, dismissal '
        'with a curled lip. The Greek <em>ekmukterizo</em> (literally <em>to turn the nose up at</em>) is '
        'used twice in Luke\'s Gospel to describe the response of Christ\'s opponents. In Luke 16:14, the '
        'Pharisees, who were <em>covetous</em>, hear Christ\'s teaching on money and <em>derided him</em>. '
        'In Luke 23:35 at the cross, the rulers <em>derided</em> Christ as He hung dying. The sneer is the '
        'response of those who consider themselves above the speaker. It is distinguished from articulate '
        'disagreement (which engages the substance) by its refusal to engage at all &mdash; the sneer says '
        '<em>this is beneath my consideration</em>, often by people whose own position cannot survive '
        'consideration. The Christian who has been sneered at for Christ\'s sake is in good company: '
        'Christ Himself was sneered at first. The proper response to the sneer is not the counter-sneer '
        'but the steady truth that the sneer cannot finally answer.</p>'
    ),
    'youthful-lust': (
        '<p>Paul\'s warning to Timothy: <em>Flee also youthful lusts: but follow righteousness, faith, '
        'charity, peace, with them that call on the Lord out of a pure heart</em> (2 Tim 2:22). The Greek '
        '<em>neoterikas epithumias</em> (youthful desires, cravings) extends well beyond the modern '
        'reduction of <em>lust</em> to sexual desire alone. The surrounding verses make clear that Paul has '
        'in view the cluster of immature, ungoverned desires that mark the young man before sanctification '
        'matures him: sexual sin, certainly; but also disputatiousness (vv. 23-24), attention-craving, '
        'status-seeking, the impulse to win-the-argument over building-the-brother, the appetite for the '
        'spectacular over the steady. The command is to <em>flee</em> &mdash; not negotiate with, not slowly '
        'discipline, but actively run away from. Joseph fleeing Potiphar\'s wife (Gen 39) is the canonical '
        'pattern: the godly man does not assess the situation; he leaves it. The positive replacement is '
        'specific &mdash; righteousness, faith, charity, peace &mdash; pursued in the company of those who '
        'call on the Lord out of a pure heart.</p>'
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
