#!/usr/bin/env python3
"""Batch 10 — expand 25 more thin entries to 85-100 words each."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'tetelestai': (
        '<p>Christ\'s final word from the cross: <em>It is finished</em> (John 19:30). Greek <em>tetelestai</em> '
        'is the perfect passive indicative of <em>teleo</em> (to bring to completion, finish, accomplish) &mdash; a '
        'tense that names completed action with abiding effect. The work is finished and remains finished. '
        'Commercial receipts of the period have been found stamped <em>tetelestai</em> for <em>paid in full</em>: '
        'the debt is settled, the transaction closed. Christ\'s cry from the cross announces the satisfaction '
        'of every claim the law had against the elect: the price paid, the sacrifice complete, the work the '
        'Father gave Him accomplished (John 17:4). Romans 4:25 reinforces: Christ <em>was delivered for our '
        'offences, and was raised again for our justification.</em> Nothing remains to be added to Christ\'s '
        'finished work. The Christian rests on what is already accomplished.</p>'
    ),
    'unstable': (
        '<p>Wavering, unsteady, double-minded. James 1:6-8 names the disposition that gets nothing in prayer: '
        '<em>For let not that man think that he shall receive any thing of the Lord. A double minded man is '
        'unstable in all his ways.</em> 2 Peter 3:16 applies the term to those who twist Scripture: <em>which '
        'they that are unlearned and unstable wrest, as they do also the other scriptures, unto their own '
        'destruction.</em> 2 Peter 2:14 names the type: <em>beguiling unstable souls.</em> The unstable man '
        'has no center of gravity; he is whatever the latest pressure makes him &mdash; theologically, morally, '
        'emotionally. The biblical cure is rootedness in Christ (Eph 3:17), the Word (Col 2:7), and the '
        'communion of the saints. Stability is not personality; it is sanctified character, cultivated over '
        'time.</p>'
    ),
    'urim-thummim': (
        '<p>The mysterious objects placed in the high priest\'s breastplate of judgment, by which God '
        'communicated specific decisions to Israel before the era of established prophets. Hebrew <em>urim</em> '
        '(lights) and <em>thummim</em> (perfections). Exodus 28:30: <em>And thou shalt put in the breastplate '
        'of judgment the Urim and the Thummim; and they shall be upon Aaron\'s heart, when he goeth in before '
        'the LORD: and Aaron shall bear the judgment of the children of Israel upon his heart before the LORD '
        'continually.</em> Their physical nature is not described in Scripture; tradition has suggested lots, '
        'precious stones, or other objects giving binary yes/no answers. Used to determine guilt (1 Sam 14:41), '
        'royal selection (1 Sam 10:20-22), and divine direction. Saul was refused an answer through them at '
        'the end (1 Sam 28:6). After the exile they ceased to function (Ezra 2:63; Neh 7:65), with restoration '
        'awaiting a future priestly age (some take this as the eschatological priesthood of the Messiah).</p>'
    ),
    'waiting': (
        '<p>The discipline of active, hopeful expectancy that defers self-rescue and trusts God\'s timing. '
        'Isaiah 40:31 names the canonical promise: <em>they that wait upon the LORD shall renew their strength; '
        'they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and '
        'not faint.</em> Psalm 27:14: <em>Wait on the LORD: be of good courage, and he shall strengthen thine '
        'heart: wait, I say, on the LORD.</em> Psalm 130:5-6: <em>I wait for the LORD, my soul doth wait, and '
        'in his word do I hope. My soul waiteth for the Lord more than they that watch for the morning.</em> '
        'Hebrew <em>qavah</em> (to wait, hope expectantly) is not passive resignation but tensed expectation &mdash; '
        'the soldier at his post, the watchman through the night. Christian waiting refuses both presumption '
        '(rushing ahead of God) and despair (concluding God will not act). Both errors fail the active-hopeful '
        'middle the biblical pattern commands.</p>'
    ),
    'work': (
        '<p>Purposeful labor &mdash; created good before the fall, cursed at the fall, redeemed in Christ. '
        'Genesis 2:15: <em>And the LORD God took the man, and put him into the garden of Eden to dress it and '
        'to keep it</em> &mdash; work belongs to the pre-fall creational vocation. Genesis 3:17-19 records the '
        'curse: thorns, sweat, toil. The NT does not abolish work but transforms its motive and meaning: '
        'Colossians 3:23-24 frames every act of work as service to Christ: <em>And whatsoever ye do, do it '
        'heartily, as to the Lord, and not unto men; Knowing that of the Lord ye shall receive the reward of '
        'the inheritance: for ye serve the Lord Christ.</em> 1 Thessalonians 4:11 and 2 Thess 3:10-12 set the '
        'biblical work ethic. Ephesians 4:28 commands the recovering thief to <em>labour, working with his '
        'hands the thing which is good, that he may have to give to him that needeth</em>. Christian work is '
        'worship, witness, and provision for one\'s own and for the kingdom.</p>'
    ),
    'zophar': (
        '<p>The third and harshest of Job\'s three friends, a Naamathite (Job 2:11; 11:1; 20:1). Where Eliphaz '
        'appeals to mystical experience and Bildad to ancient tradition, Zophar appeals to dogmatic rigidity: '
        'Job\'s suffering proves hidden sin, and Job\'s self-defense is itself evidence of that hidden sin. '
        'Zophar\'s two speeches (Job 11; 20) are the most unyielding of the three friends\' interventions. He '
        'has no speech in the third cycle (chs. 22-27) &mdash; the friends have run out of arguments. At the '
        'end, the LORD\'s verdict comes against all three: <em>My wrath is kindled against thee, and against '
        'thy two friends: for ye have not spoken of me the thing that is right, as my servant Job hath</em> '
        '(Job 42:7). Job is required to pray for them. Zophar is the cautionary example of the orthodox-sounding '
        'comforter whose words about God are technically right in places but fail the pastoral situation '
        'completely &mdash; theology weaponized against the suffering.</p>'
    ),
    '1john': (
        '<p>The first of three Johannine epistles, written by the apostle John near the end of the first '
        'century (probably from Ephesus). The letter\'s explicit purpose appears at 5:13: <em>These things '
        'have I written unto you that believe on the name of the Son of God; that ye may know that ye have '
        'eternal life.</em> The epistle gives believers three tests of authentic faith, recurring throughout '
        'the five chapters: (1) <em>doctrinal</em> &mdash; confessing Jesus Christ come in the flesh, against '
        'incipient Gnostic denial of the Incarnation (1:1-3; 2:22-23; 4:1-3); (2) <em>moral</em> &mdash; walking '
        'in obedience to God\'s commandments, not continuing in habitual sin (2:3-6; 3:6-10); (3) <em>relational</em> &mdash; '
        'love for the brothers, demonstrated in deeds not just words (2:9-11; 3:14-18; 4:7-21). The famous '
        '1 John 1:9 (<em>If we confess our sins, he is faithful and just to forgive us our sins</em>) anchors '
        'the assurance the epistle aims to provide.</p>'
    ),
    '1timothy': (
        '<p>The first of three Pastoral Epistles (with 2 Timothy and Titus), written by Paul to Timothy &mdash; '
        'his young apostolic delegate stationed at Ephesus &mdash; about AD 62-64. The letter instructs Timothy '
        'in church order against false teachers in the Ephesian context. Six chapters cover: (1) warning '
        'against false doctrine and Paul\'s gospel testimony; (2) instructions for public prayer and the '
        'limits on women\'s teaching authority; (3) qualifications for elders (3:1-7) and deacons (3:8-13), '
        'with the famous declaration of the great mystery of godliness (3:16); (4) warning against apostasy '
        'and instructions to Timothy on personal ministry; (5) instructions for handling widows, elders, and '
        'church discipline; (6) instructions on money (6:6-10 contains the famous <em>love of money is the '
        'root of all evil</em>), final charge to Timothy to <em>fight the good fight of faith</em> (6:12), '
        'and closing benediction.</p>'
    ),
    '2timothy': (
        '<p>Paul\'s final epistle, written in chains from Rome about AD 67, awaiting execution under Nero. '
        'Possibly the last words of Paul preserved in Scripture. The tone is intensely personal: Paul knows '
        'his death is near (<em>I am now ready to be offered, and the time of my departure is at hand</em>, '
        '4:6) and writes urgent final counsel to Timothy. Four chapters: (1) reminder of Timothy\'s genuine '
        'faith from his grandmother Lois and mother Eunice, and Paul\'s charge to <em>stir up the gift of '
        'God which is in thee</em>; (2) call to endure hardship as a good soldier of Christ Jesus, with the '
        'parable of vessels of honor and dishonor; (3) prediction of perilous times in the last days, and '
        'the affirmation that <em>all scripture is given by inspiration of God</em> (3:16-17); (4) the great '
        'final charge to preach the Word in season and out (4:1-5), Paul\'s testimony of having fought the '
        'good fight (4:7-8), and final greetings.</p>'
    ),
    'advent-season': (
        '<p>The four-week Christian season of preparation before Christmas, focusing on the dual coming of '
        'Christ: His first coming in humility at Bethlehem and His second coming in glory. The word '
        '<em>advent</em> (Latin <em>adventus</em>, coming, arrival) names both. Advent begins on the fourth '
        'Sunday before December 25 and concludes at Christmas Eve. The traditional readings rotate through '
        'four themes (often: hope, peace, joy, love) and four classes of forerunner figures: the OT '
        'prophets (especially Isaiah), John the Baptist, Mary, and the church-of-watchful-expectation. The '
        'Advent wreath with its four candles (and one central Christ candle) is a common observance. The '
        'season\'s theological depth is in its refusal to collapse Christmas into a one-day cultural '
        'observance; Christ\'s first coming is a four-week meditation, and His second coming hovers in the '
        'background as the consummation toward which the entire season points.</p>'
    ),
    'ahasuerus': (
        '<p>The Persian king of the book of Esther, almost certainly Xerxes I (reigned 486-465 BC). His '
        'kingdom <em>reigned, from India even unto Ethiopia, over an hundred and seven and twenty provinces</em> '
        '(Esther 1:1) &mdash; the largest empire of the ancient world to that point. The book of Esther '
        'narrates how Ahasuerus deposed his queen Vashti (ch. 1), held a kingdom-wide search that elevated '
        'the Jewish exile Esther to the throne (ch. 2), how Haman manipulated the king into a genocidal '
        'decree against the Jews (ch. 3), Esther\'s providential intervention through Mordecai\'s guidance '
        '(chs. 4-7), and the reversal whereby the Jews were saved and Haman hanged on his own gallows '
        '(chs. 8-10). The book is famous for never explicitly mentioning God, yet His providence is visible '
        'throughout. The Feast of Purim (still observed annually by Jews worldwide) commemorates the '
        'deliverance. Ahasuerus himself appears as a vain, capricious, easily-manipulated monarch &mdash; '
        'a pagan king through whom God\'s sovereign purpose worked nonetheless.</p>'
    ),
    'augustinianism': (
        '<p>The theological tradition flowing from Augustine of Hippo (354-430 AD), characterized by '
        'distinctive doctrines of grace, sin, and predestination. Core commitments: (1) original sin &mdash; '
        'Adam\'s guilt and corruption are inherited by all his descendants; (2) total inability &mdash; the '
        'fallen will cannot of itself turn to God; (3) sovereign grace &mdash; salvation is entirely God\'s '
        'gift, not a cooperation God rewards for human effort; (4) unconditional election &mdash; God chose '
        'His elect from before the world\'s foundation, not on the basis of foreseen faith or works; (5) '
        'perseverance &mdash; those whom God effectually calls He will keep to the end. Developed against '
        'Pelagius (who taught that humans could choose God without grace), Augustine\'s positions were '
        'affirmed by multiple councils. The Reformation recovered Augustinianism against the medieval '
        'synergism that had compromised it; Luther was an Augustinian monk; Calvin quoted Augustine more '
        'than any other theologian. The Reformation can fairly be described as an internal Augustinian '
        'dispute over which Augustine (his doctrine of grace or his doctrine of the Church) should govern.</p>'
    ),
    'blasphemer': (
        '<p>One who speaks contemptuously of God or holy things. Greek <em>blasphemos</em>. Scripture treats '
        'blasphemy with extreme seriousness: the OT prescribed death for blasphemy against the LORD (Lev '
        '24:10-16). The high priest charged Christ with blasphemy at His trial (Matt 26:65; Mark 14:64). Paul '
        'confessed his pre-conversion self as <em>a blasphemer, and a persecutor, and injurious</em> (1 Tim '
        '1:13), but received mercy because he did it ignorantly in unbelief. Revelation 13:5-6 names the '
        'eschatological beast as one who speaks <em>great things and blasphemies</em>. The category extends '
        'beyond cursing-with-God\'s-name to any speech that diminishes God\'s glory or character. The biblical '
        'response: refuse such speech yourself; refuse to tolerate it in your gatherings; pray for the '
        'blasphemer\'s repentance as Paul received his. The unforgivable sin (Mark 3:28-30) is the final, '
        'settled blasphemy against the Spirit; ordinary blasphemy is gravely serious but not unforgivable.</p>'
    ),
    'bowls-wrath': (
        '<p>The seven final judgments of Revelation 16, poured out from heavenly bowls (or vials in older '
        'translations) by seven angels onto the unrepentant earth. The bowl-judgments complete God\'s wrath '
        'against the final pre-Parousia rebellion. Their order: (1) loathsome boils on those bearing the mark '
        'of the beast (16:2); (2) the sea turned to blood (16:3); (3) rivers and springs turned to blood &mdash; '
        'the avenging of the prophets\' and saints\' shed blood (16:4-7); (4) scorching solar heat (16:8-9); '
        '(5) darkness on the beast\'s kingdom (16:10-11); (6) the Euphrates dried up, three unclean spirits '
        'like frogs gathering the kings of the earth to Armageddon (16:12-16); (7) <em>It is done</em> &mdash; '
        'thunders, lightnings, earthquake, hundred-pound hailstones (16:17-21). The bowl-judgments parallel '
        'the seal- and trumpet-judgments earlier in the book; eschatological interpreters vary on whether these '
        'are sequential, simultaneous-from-different-angles, or recapitulating. The MOOP Dictionary holds the '
        'futurist reading: actual final judgments still ahead.</p>'
    ),
    'broken-vow': (
        '<p>The unfulfilled vow before God. Scripture treats vow-breaking as a serious matter, not lightly. '
        'Leviticus 5:4-5 prescribes the trespass offering for one who has sworn rashly: <em>Or if a soul '
        'swear, pronouncing with his lips to do evil, or to do good, whatsoever it be that a man shall '
        'pronounce with an oath, and it be hid from him; when he knoweth of it, then he shall be guilty in '
        'one of these. And it shall be, when he shall be guilty in one of these things, that he shall '
        'confess that he hath sinned in that thing.</em> Numbers 30:13-15 covers conditions for the head of '
        'household to disallow a vow. Ecclesiastes 5:4-6: <em>When thou vowest a vow unto God, defer not to '
        'pay it... Suffer not thy mouth to cause thy flesh to sin; neither say thou before the angel, that '
        'it was an error.</em> The biblical remedy for a broken vow is confession, restitution where '
        'possible, and the trespass-offering posture (which Christ\'s sacrifice fulfills). The category '
        'extends to broken marriage vows, baptismal vows, ordination vows, and any explicit promise made '
        'before God.</p>'
    ),
    'colossians-book': (
        '<p>Paul\'s prison epistle to the church at Colossae (a small city in the Lycus Valley of modern '
        'Turkey), written about AD 60-62, probably from Rome. Paul had not personally founded this church &mdash; '
        'Epaphras planted it (1:7) &mdash; but writes to address an early proto-Gnostic mixture of philosophy, '
        'angel worship, asceticism, and Jewish ritual that threatened the church. Paul\'s answer is the '
        'extended declaration of Christ\'s absolute preeminence: <em>Who is the image of the invisible God, '
        'the firstborn of every creature: For by him were all things created, that are in heaven, and that '
        'are in earth, visible and invisible... and he is before all things, and by him all things consist</em> '
        '(1:15-17). Four chapters: (1) thanksgiving and the great Christ-hymn (1:15-20); (2) warning against '
        'the false teaching; (3) practical instructions for the new-creation life and the household codes; '
        '(4) final greetings. <em>Christ in you, the hope of glory</em> (1:27) captures the letter\'s heart.</p>'
    ),
    'comfort-verb': (
        '<p>To strengthen-by-coming-alongside. Greek <em>parakaleo</em> (from <em>para</em>, beside + '
        '<em>kaleo</em>, to call) and its noun <em>paraklesis</em> are the verbs behind the Holy Spirit\'s '
        'title <em>Paraclete / Comforter / Helper</em> (John 14:16, 26; 15:26; 16:7). The English word '
        '<em>comfort</em> has weakened over time toward sentimental consolation; the biblical word is '
        'stronger: real strengthening by means of presence and word. 2 Corinthians 1:3-4: <em>Blessed be '
        'God, even the Father of our Lord Jesus Christ, the Father of mercies, and the God of all comfort; '
        'Who comforteth us in all our tribulation, that we may be able to comfort them which are in any '
        'trouble, by the comfort wherewith we ourselves are comforted of God.</em> Christian comfort is '
        'tripartite: the Spirit comforts the individual believer; the Word comforts through the recorded '
        'consolations of God; the saints comfort one another. None of the three replaces the others.</p>'
    ),
    'contentment-biblical': (
        '<p>The settled satisfaction with what God has provided. Paul names it as <em>great gain</em>: '
        '<em>But godliness with contentment is great gain</em> (1 Tim 6:6). Hebrews 13:5: <em>Let your '
        'conversation be without covetousness; and be content with such things as ye have: for he hath said, '
        'I will never leave thee, nor forsake thee.</em> The Greek <em>autarkeia</em> (sufficiency) carried '
        'a Stoic flavor that Paul filled with new content: not Stoic self-sufficiency but Christ-sufficiency. '
        'Philippians 4:11-13 is autobiographical: <em>for I have learned, in whatsoever state I am, '
        'therewith to be content. I know both how to be abased, and I know how to abound... I can do all '
        'things through Christ which strengtheneth me.</em> Contentment is not native to the heart; it is '
        '<em>learned</em> &mdash; cultivated through repeated experience of God\'s sufficiency across '
        'changing circumstances. The contented Christian is uncommon and conspicuous; modern consumerist '
        'culture is designed to prevent the disposition from forming.</p>'
    ),
    'covenant-marriage': (
        '<p>Marriage understood as covenant &mdash; not mere contract or romantic-emotional partnership, '
        'but a solemn binding oath sworn before God between one man and one woman, lifelong, exclusive, and '
        'imaging Christ\'s relationship to His Church. Malachi 2:14 names the LORD as the witness of the '
        'covenant: <em>the LORD hath been witness between thee and the wife of thy youth, against whom thou '
        'hast dealt treacherously: yet she is thy companion, and the wife of thy covenant.</em> Ephesians '
        '5:31-32 reveals the marriage covenant\'s deeper meaning: <em>For this cause shall a man leave his '
        'father and mother, and shall be joined unto his wife, and they two shall be one flesh. This is a '
        'great mystery: but I speak concerning Christ and the church.</em> Christ Himself anchored marriage '
        'in the creation order: <em>Have ye not read, that he which made them at the beginning made them '
        'male and female... What therefore God hath joined together, let not man put asunder</em> (Matt '
        '19:4-6). Covenant marriage is theological reality before it is social institution.</p>'
    ),
    'ehud': (
        '<p>The second judge of Israel, a left-handed Benjamite (the tribal name <em>Ben-jamin</em> means '
        '<em>son of the right hand</em> &mdash; the irony is biblical), who delivered Israel from Eglon king '
        'of Moab\'s eighteen-year oppression. Judges 3:12-30 narrates the deliverance. Ehud crafted a foot-'
        'and-a-half-long dagger, strapped it to his right thigh (where right-handed soldiers carried weapons '
        'on the left, and Eglon\'s guards apparently did not search there), delivered a tribute payment to '
        'Eglon, requested a private audience for a <em>secret message</em>, and assassinated the corpulent '
        'king with a single thrust before escaping through the parlor and rallying Israel to defeat the '
        'leaderless Moabites. The narrative\'s grimly comic detail (Eglon\'s servants delaying the discovery '
        'of his body, assuming privacy) is part of the biblical canon\'s honest narrative texture. Ehud is '
        'one of the more action-packed judges; Israel had rest for eighty years after his deliverance.</p>'
    ),
    'eternality': (
        '<p>The divine attribute that God has neither beginning nor end nor succession of moments. He is '
        'the eternal <em>I AM</em> (Ex 3:14), the One who is and was and is to come (Rev 1:8). Psalm 90:2: '
        '<em>Before the mountains were brought forth, or ever thou hadst formed the earth and the world, '
        'even from everlasting to everlasting, thou art God.</em> The divine eternality is not merely '
        'long-lasting time but qualitatively distinct from time itself: God is not bound by past, present, '
        'and future as creatures are. Augustine\'s formulation: <em>tota simul</em> &mdash; all-at-once. '
        'The classical theistic doctrine holds God\'s eternality as an essential attribute, against process-'
        'theology and open-theism revisions that tie God to the temporal-future flow. The doctrine grounds '
        'the reliability of God\'s promises: the One who has never changed cannot fail what He has '
        'covenanted. <em>Jesus Christ the same yesterday, and to day, and for ever</em> (Heb 13:8).</p>'
    ),
    'faithful-saying': (
        '<p>Five sayings in the Pastoral Epistles introduced by the formula <em>this is a faithful saying</em> '
        '(Greek <em>pistos ho logos</em>), likely circulating apostolic-era confessional formulas that Paul '
        'adopted into his letters as established summaries of Christian truth. The five: (1) 1 Tim 1:15 &mdash; '
        '<em>This is a faithful saying, and worthy of all acceptation, that Christ Jesus came into the '
        'world to save sinners; of whom I am chief.</em> (2) 1 Tim 3:1 &mdash; <em>This is a true saying, '
        'If a man desire the office of a bishop, he desireth a good work.</em> (3) 1 Tim 4:9 &mdash; (in '
        'context with 4:8\'s godliness-vs-bodily-exercise contrast). (4) 2 Tim 2:11-13 &mdash; <em>It is a '
        'faithful saying: For if we be dead with him, we shall also live with him...</em> (5) Titus 3:8 &mdash; '
        '(with the immediately preceding regeneration-through-the-Holy-Ghost passage). The formula testifies '
        'that early Christian theology had crystallized into memorable summary-statements within a few '
        'decades of the resurrection.</p>'
    ),
    'froward': (
        '<p>KJV word for <em>perverse, turned-away from what is right</em>. The Hebrew <em>iqqesh</em> '
        '(crooked, perverse) names the moral category. Proverbs returns to it frequently: <em>Put away from '
        'thee a froward mouth, and perverse lips put far from thee</em> (4:24); <em>A naughty person, a '
        'wicked man, walketh with a froward mouth</em> (6:12); <em>They that are of a froward heart are '
        'abomination to the LORD</em> (11:20); <em>The way of a fool is right in his own eyes... He that '
        'speaketh truth sheweth forth righteousness: but a false witness deceit. There is that speaketh '
        'like the piercings of a sword: but the tongue of the wise is health</em> (12:15-18, with frowardness '
        'all through). The froward person\'s mouth, ways, thoughts, and dealings have all gone the wrong '
        'direction at the heart level. The corrective is the fear of the LORD (Prov 8:13: <em>The fear of '
        'the LORD is to hate evil: pride, and arrogancy, and the evil way, and the froward mouth, do I '
        'hate</em>).</p>'
    ),
    'gambling': (
        '<p>The wagering of value on chance for personal gain. Not addressed by name in Scripture, but '
        'failing biblical principles in several directions: (1) <em>stewardship</em> &mdash; God\'s resources '
        'entrusted to His people are not to be risked on chance; (2) <em>work</em> &mdash; the biblical '
        'pattern is honest labor that has surplus to give (Eph 4:28), not winning others\' money; (3) '
        '<em>contentment</em> &mdash; gambling appeals to the desire-for-more that 1 Tim 6:6-10 names as '
        'covetousness-and-the-love-of-money; (4) <em>love of neighbor</em> &mdash; the gambler\'s gain '
        'requires another\'s loss; the systems of casinos and lotteries extract most heavily from those '
        'who can least afford it. The Reformed and Puritan traditions have generally treated gambling as '
        'incompatible with Christian discipleship, though some Christians distinguish between social '
        'low-stakes recreation and serious wagering as a way of life. The MOOP Dictionary holds the '
        'stricter position: the disposition that gambling cultivates is uniformly unhelpful to '
        'Christian formation.</p>'
    ),
    'gaza': (
        '<p>The southernmost of the five great Philistine cities (the Pentapolis), on the Mediterranean '
        'coast about forty miles southwest of Jerusalem. Gaza features in major OT narratives, most famously '
        'as the city where Samson tore off the gates and carried them to the top of a hill outside Hebron '
        '(Judg 16:1-3), and where after his betrayal by Delilah he was bound, blinded, and brought down to '
        'grind grain like an animal (Judg 16:21). His final act &mdash; pushing the temple pillars apart '
        'and bringing the building down on himself and the assembled Philistine lords &mdash; killed more '
        'in his death than he had killed in his life (Judg 16:30). The prophets pronounce judgment against '
        'Gaza (Amos 1:6-8; Jer 25:20; 47:1-5; Zeph 2:4; Zech 9:5). The Ethiopian eunuch was traveling '
        '<em>the way that goeth down from Jerusalem unto Gaza, which is desert</em> (Acts 8:26) when Philip '
        'met him and explained the suffering-Servant passage from Isaiah 53. Gaza is still inhabited; the '
        'modern city of the same name occupies the same coastal strip.</p>'
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
