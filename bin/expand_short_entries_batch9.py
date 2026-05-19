#!/usr/bin/env python3
"""Expand 25 more thin entries (batch 9) to 90-110 words each."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    '1peter': (
        '<p>Peter\'s first epistle, written about AD 62-64 to <em>the strangers scattered throughout '
        'Pontus, Galatia, Cappadocia, Asia, and Bithynia</em> (1:1) &mdash; Gentile and Jewish Christians '
        'in northern Asia Minor (modern Turkey) facing the early waves of Roman persecution. The letter\'s '
        'organizing image is pilgrimage: believers are <em>strangers and pilgrims</em> (2:11) journeying '
        'through trials toward an inheritance reserved in heaven (1:4). Five chapters frame trials as '
        'refining fire (1:6-7), the believer\'s response of holy living (1:13-2:3), the priestly identity '
        'of the church (2:4-10), submission patterns (citizens to government 2:13-17, servants to masters '
        '2:18-25, wives to husbands 3:1-7, husbands to wives 3:7), suffering for righteousness modeled on '
        'Christ (3:8-4:19), and the call to elders to shepherd the flock of God (5:1-4). The hope that '
        'sustains the persecuted is grounded in Christ\'s resurrection (1:3) and consummated at His '
        'revelation (1:7).</p>'
    ),
    'alertness': (
        '<p>Watchful attention. Christ repeatedly commands it: <em>Watch and pray, that ye enter not into '
        'temptation</em> (Matt 26:41); <em>Take ye heed, watch and pray: for ye know not when the time '
        'is</em> (Mark 13:33). Paul commands it as the first of his five military imperatives in 1 '
        'Corinthians 16:13: <em>Watch ye, stand fast in the faith, quit you like men, be strong.</em> '
        'Peter intensifies in 1 Peter 5:8: <em>Be sober, be vigilant; because your adversary the devil, '
        'as a roaring lion, walketh about, seeking whom he may devour.</em> The Greek <em>gregoreo</em> '
        '(to be awake, watchful) names both the disposition (alertness) and the practice (sustained '
        'wakefulness). The biblical man is not paranoid but not drowsy &mdash; engaged-with-reality, '
        'aware of threats, attentive to the times. The Christian who has cultivated alertness sees '
        'temptation forming before it strikes; the drowsy Christian wakes up only after the fall.</p>'
    ),
    'amusement': (
        '<p>Diversion or entertainment that draws the mind away from thoughtful engagement. Not '
        'condemned in itself &mdash; Scripture knows feasts, music, family laughter, and the joy of a '
        'merry heart &mdash; but dangerous when amusement becomes the dominant mode of life. '
        'Ecclesiastes 7:4: <em>The heart of the wise is in the house of mourning; but the heart of '
        'fools is in the house of mirth.</em> 1 Corinthians 10:7 (quoting Ex 32:6): <em>Neither be ye '
        'idolaters, as were some of them; as it is written, The people sat down to eat and drink, and '
        'rose up to play.</em> Modern Western culture has industrialized amusement at unprecedented '
        'scale &mdash; streaming services, social media, mobile games, sports entertainment, ambient '
        'background distraction. Neil Postman\'s phrase <em>amusing ourselves to death</em> names the '
        'civilizational pattern: a culture that has chosen distraction over weight, performance over '
        'truth, spectacle over substance. The Christian disciplines amusement under the priority of '
        'weighty things: the Word, prayer, family, work, worship.</p>'
    ),
    'ascension-day': (
        '<p>The Christian observance forty days after Easter commemorating Christ\'s bodily ascension '
        'from the Mount of Olives to the Father\'s right hand. Acts 1:9-11 narrates the event: <em>And '
        'when he had spoken these things, while they beheld, he was taken up; and a cloud received him '
        'out of their sight... this same Jesus, which is taken up from you into heaven, shall so come '
        'in like manner as ye have seen him go into heaven.</em> The ascension is theologically '
        'inseparable from the resurrection, completing the work begun on Easter: the risen Christ does '
        'not remain on earth indefinitely but ascends to His enthronement at the Father\'s right hand. '
        'Hebrews 1:3 anchors the doctrine: <em>when he had by himself purged our sins, sat down on the '
        'right hand of the Majesty on high.</em> Christ\'s priestly intercession (Heb 7:25; Rom 8:34), '
        'His present rule as exalted Mediator-King (Phil 2:9-11; Eph 1:20-22), and the sending of the '
        'Spirit at Pentecost (John 16:7) all depend on the ascension. The Christian who skips ascension '
        'in his calendar loses the doctrinal bridge between Easter and Pentecost.</p>'
    ),
    'bronze-altar': (
        '<p>The large square altar of acacia wood overlaid with bronze in the tabernacle\'s outer court, '
        'the principal sacrificial altar of the Mosaic worship system. Exodus 27:1-8 specifies '
        'dimensions: five cubits long, five cubits wide (about 7.5 feet square), three cubits high '
        '(about 4.5 feet), with horns at the four corners and a grating of bronze halfway up the '
        'interior. All burnt offerings, peace offerings, sin offerings, and trespass offerings were '
        'sacrificed here &mdash; the altar fire was never to go out (Lev 6:13). The horns of the altar '
        'were sprinkled with atonement blood (Lev 4:7), and fugitives could grasp them for asylum '
        '(1 Kgs 1:50; 2:28; though the asylum of the altar did not protect intentional murderers, Ex '
        '21:14). Worshippers entering the tabernacle encountered the bronze altar first: there is no '
        'approach to God except through sacrifice. Christ as the once-for-all sacrifice fulfills the '
        'typology (Heb 9:11-14; 10:11-14); the bronze altar\'s blood is replaced by the blood of the '
        'Lamb.</p>'
    ),
    'derision': (
        '<p>Mocking laughter &mdash; the contemptuous response of the wicked toward the godly, and '
        'conversely, the LORD\'s response toward those who plot against His Christ. Psalm 2:4: <em>He '
        'that sitteth in the heavens shall laugh: the Lord shall have them in derision.</em> The same '
        'word is applied to the suffering Messiah\'s experience at Psalm 22:7: <em>All they that see '
        'me laugh me to scorn: they shoot out the lip, they shake the head.</em> And again at Psalm '
        '44:13: <em>Thou makest us a reproach to our neighbours, a scorn and a derision to them that '
        'are round about us.</em> The Hebrew <em>lag</em> (to mock, deride) and <em>qalas</em> (to '
        'scoff) name the disposition. Derision\'s direction matters: God\'s derision of human rebellion '
        'is the sober pronouncement of holy contempt for evil; man\'s derision of God\'s people is the '
        'inverted echo, contemptuous of what the LORD has set apart. The Christian who has been derided '
        'for the gospel\'s sake stands in the line of David, the prophets, and Christ Himself &mdash; '
        'and shares in their vindication.</p>'
    ),
    'epiphany-season': (
        '<p>The Christian season after Christmas (January 6 onward, ending at Ash Wednesday) celebrating '
        'the manifestation of Christ to the nations. The word <em>epiphany</em> (Greek <em>epiphaneia</em>) '
        'means <em>showing forth, manifestation</em>. The season anchors on three biblical events of '
        'Christ\'s self-revelation to the world: (1) the visit of the Magi from the East (Matt 2:1-12) &mdash; '
        'Gentile representatives recognizing the King; (2) the baptism of Jesus by John in the Jordan '
        '(Matt 3:13-17) &mdash; the voice from heaven publicly declaring His Sonship; (3) the wedding '
        'at Cana (John 2:1-11) &mdash; the first sign manifesting His glory. Together these events frame '
        'Christ\'s entrance onto the world stage as Lord of nations, Son of God, and miracle-working '
        'Messiah. Epiphany is observed across most liturgical Christian traditions; many evangelical '
        'and Reformed bodies have not adopted it formally but mark the same events in preaching '
        'rotations. The season\'s emphasis on Gentile inclusion makes it particularly suited to '
        'missions-focused preaching.</p>'
    ),
    'flock-of-god': (
        '<p>Peter\'s designation for the local church under elder care. 1 Peter 5:2-3: <em>Feed the '
        'flock of God which is among you, taking the oversight thereof, not by constraint, but '
        'willingly; not for filthy lucre, but of a ready mind; Neither as being lords over God\'s '
        'heritage, but being ensamples to the flock.</em> The image is decisive in three ways: (1) '
        'the flock belongs to God, not to the elders &mdash; they are stewards, not owners; (2) the '
        'elder\'s job is to feed, not to fleece &mdash; pastoral provision rather than self-enrichment '
        'from the sheep; (3) leadership is by example, not by domination &mdash; the chief shepherd '
        'pattern of John 10 applies to every undershepherd. Acts 20:28-29 reinforces with Paul\'s '
        'farewell to the Ephesian elders: <em>Take heed therefore unto yourselves, and to all the flock, '
        'over the which the Holy Ghost hath made you overseers, to feed the church of God, which he '
        'hath purchased with his own blood.</em> The flock-of-God metaphor grounds biblical pastoral '
        'ministry against every form of professional-clergy entrepreneurialism.</p>'
    ),
    'heart-grateful': (
        '<p>The ruled heart, governed by the peace of Christ and overflowing in thanksgiving. Colossians '
        '3:15-17 places gratitude at the center of the disciplined Christian life: <em>And let the '
        'peace of God rule in your hearts... and be ye thankful. Let the word of Christ dwell in you '
        'richly... singing with grace in your hearts to the Lord. And whatsoever ye do in word or deed, '
        'do all in the name of the Lord Jesus, giving thanks to God and the Father by him.</em> '
        'Ephesians 5:20 commands the practice: <em>Giving thanks always for all things unto God and the '
        'Father in the name of our Lord Jesus Christ.</em> 1 Thessalonians 5:18: <em>In every thing give '
        'thanks: for this is the will of God in Christ Jesus concerning you.</em> Gratitude is not '
        'sentiment but discipline &mdash; the practiced posture of recognizing every good gift as from '
        'above (James 1:17). The ungrateful heart is the heart of Romans 1: those who knew God but '
        '<em>glorified him not as God, neither were thankful</em> (Rom 1:21) became darkened in their '
        'understanding. Gratitude is the gateway-virtue that opens the soul to all the others.</p>'
    ),
    'israel-people': (
        '<p>The covenant people descended from Jacob (renamed Israel after wrestling with God, Gen '
        '32:28), set apart through Abraham, redeemed through the exodus, given the law at Sinai, '
        'planted in Canaan, judged and exiled, restored, and finally gathered in the Messiah. The '
        'biblical narrative of Israel runs from Abraham (Gen 12) to Revelation (the 144,000 of '
        'Revelation 7 and 14, twelve thousand from each tribe). Israel\'s identity is covenantal, not '
        'merely ethnic: blessing flows through faith (Rom 4:11-13), the true children of Abraham are '
        'the children of faith (Gal 3:7, 29), and the Gentile church is grafted into the cultivated '
        'olive tree of Israel (Rom 11:17-24). Paul\'s sustained meditation in Romans 9-11 wrestles with '
        'God\'s ongoing purposes for ethnic Israel within the church-age: a hardening in part has '
        'happened until the fullness of the Gentiles is come, after which <em>all Israel shall be '
        'saved</em> (Rom 11:25-26). The Christian holds two truths together: the church is the true '
        'Israel of God (Gal 6:16); and God has not cast away His people whom He foreknew (Rom 11:2).</p>'
    ),
    'joppa': (
        '<p>The ancient Mediterranean port of Israel (modern Jaffa, now part of Tel Aviv-Jaffa). Joppa '
        'features in three significant biblical episodes. (1) Jonah fled the LORD\'s commission by '
        'descending to Joppa and sailing for Tarshish (Jonah 1:3). The downward motion of his rebellion '
        'is itself a moral marker. (2) Cedars from Lebanon for both Solomon\'s temple (2 Chr 2:16) and '
        'the second temple (Ezra 3:7) were floated by sea to Joppa for overland transport to Jerusalem. '
        '(3) Most importantly, in Acts 9-10, Joppa is where Peter raised Tabitha from the dead (Acts '
        '9:36-43) and where he received the threefold rooftop vision of the great sheet descending '
        '(Acts 10:9-16) that opened his understanding to the Gentile mission: <em>What God hath '
        'cleansed, that call not thou common.</em> From Joppa Peter went to Cornelius\' house at '
        'Caesarea, where the Spirit fell on the Gentiles, sealing the church\'s expansion beyond Israel. '
        'Joppa is therefore one of the geographic hinges of Christian salvation history.</p>'
    ),
    'jude': (
        '<p>A short, fierce general epistle written by Jude (brother of James, half-brother of Jesus &mdash; '
        '<em>brother of James</em> in v. 1; cf. Matt 13:55, Mark 6:3) probably in the mid 60s AD. '
        'Twenty-five verses in length. The letter\'s explicit purpose: Jude had intended to write a '
        'general treatise on common salvation but instead found it <em>needful for me to write unto '
        'you, and exhort you that ye should earnestly contend for the faith which was once delivered '
        'unto the saints</em> (v. 3) &mdash; the canonical mandate for doctrinal contention. The '
        'concern is specific: <em>certain men crept in unawares... ungodly men, turning the grace of '
        'our God into lasciviousness, and denying the only Lord God, and our Lord Jesus Christ</em> '
        '(v. 4). Jude warns by citing three OT examples of judgment (Israel in the wilderness, the '
        'fallen angels, Sodom and Gomorrah), uses material parallel to 2 Peter 2, and closes with one '
        'of the great Trinitarian benedictions of Scripture (vv. 24-25). The letter is the canonical '
        'warrant for doctrinal contending against false teachers and antinomian smuggling.</p>'
    ),
    'kneeling': (
        '<p>The posture of a creature acknowledging the Creator\'s rightful rule. Throughout Scripture '
        'kneeling marks moments of submission, worship, intercession, and supplication. Solomon knelt '
        'before the bronze altar at the temple dedication (1 Kgs 8:54; 2 Chr 6:13). Daniel knelt three '
        'times daily toward Jerusalem in prayer, even under the threat of the lions\' den (Dan 6:10). '
        'Christ knelt in Gethsemane (Luke 22:41). The early church knelt: Stephen at his martyrdom '
        '(Acts 7:60), Peter at Tabitha\'s deathbed (Acts 9:40), Paul with the Ephesian elders (Acts '
        '20:36), Paul with the Tyrian disciples on the beach (Acts 21:5). The climactic biblical use '
        'is eschatological: <em>That at the name of Jesus every knee should bow, of things in heaven, '
        'and things in earth, and things under the earth</em> (Phil 2:10; quoting Isa 45:23). Every '
        'knee will bow at Christ\'s name &mdash; willingly now or compelled then. The Christian who '
        'kneels now anticipates the eschatological reality and trains his body in the truth his soul '
        'confesses.</p>'
    ),
    'lamech': (
        '<p>Two Old Testament figures of the same name, in opposing genealogical lines. (1) <em>The '
        'Cainite Lamech</em> (Gen 4:19-24): seventh from Adam through Cain, the first man to introduce '
        'polygamy (he <em>took unto him two wives</em>, Adah and Zillah), and the boaster who escalated '
        'Cain\'s curse-of-sevenfold to seventy-and-sevenfold in his song of vengeance: <em>If Cain '
        'shall be avenged sevenfold, truly Lamech seventy and sevenfold.</em> His three sons by Adah '
        'and Zillah were innovators in herding (Jabal), music (Jubal), and metalwork (Tubal-cain) &mdash; '
        'civilization\'s technical advance paired with the moral descent of Lamech himself. (2) <em>The '
        'Sethite Lamech</em> (Gen 5:28-29): seventh from Adam through Seth, father of Noah, whose '
        'naming speech expresses faith that <em>This same shall comfort us concerning our work and '
        'toil of our hands, because of the ground which the LORD hath cursed.</em> The two Lamechs '
        'frame the antithesis Genesis 4-5 draws: the line of Cain trending toward violence and '
        'self-glorying; the line of Seth trending toward calling on the LORD and toward the preserving '
        'patriarch Noah.</p>'
    ),
    'lamentations-book': (
        '<p>Five poems of national grief over fallen Jerusalem, traditionally attributed to the prophet '
        'Jeremiah (the Septuagint, Vulgate, and modern Hebrew Bible chapter divisions all place it '
        'after Jeremiah). The book mourns the 586 BC Babylonian destruction of Jerusalem, the burning '
        'of the temple, the slaughter and exile of the people. The structure is striking: four of the '
        'five chapters are acrostics (each verse beginning with a successive letter of the Hebrew '
        'alphabet), with the central chapter (3) using a triple-acrostic (three verses per Hebrew '
        'letter). The book refuses cheap comfort &mdash; the grief is real, the destruction final, the '
        'judgment deserved &mdash; yet at the precise center (Lam 3:21-23) stands one of Scripture\'s '
        'most luminous statements of hope: <em>This I recall to my mind, therefore have I hope. It is '
        'of the LORD\'s mercies that we are not consumed, because his compassions fail not. They are '
        'new every morning: great is thy faithfulness.</em> The book of tears built around the '
        'unfailing mercy of the LORD.</p>'
    ),
    'messianic-prophecy': (
        '<p>The Old Testament prophecies foretelling the coming Messiah &mdash; His person, work, '
        'suffering, and reign &mdash; fulfilled in Jesus Christ. Scripture\'s messianic prophecy is '
        'developed progressively across the OT canon. From Genesis: the protoevangelium of 3:15, the '
        'Shiloh-from-Judah of 49:10. From Numbers and Deuteronomy: the Star out of Jacob (Num 24:17), '
        'the Prophet like Moses (Deut 18:15-19). From the Psalms: the messianic kingship of Ps 2, the '
        'suffering Messiah of Ps 22, the priestly Messiah after the order of Melchizedek of Ps 110. '
        'From Isaiah: Immanuel (7:14), the Mighty God and Prince of Peace (9:6-7), the Branch from '
        'Jesse (11), the Suffering Servant of 52:13-53:12. From Jeremiah: the new covenant (31:31-34). '
        'From Ezekiel: the one Shepherd-David (34:23-24). From Daniel: the Son of Man (7:13-14), the '
        'seventy weeks (9:24-27). From Micah: Bethlehem birth (5:2). From Zechariah: humble King on a '
        'donkey (9:9), pierced one mourned (12:10), thirty pieces of silver (11:12-13). Christ\'s '
        'self-presentation as fulfillment of all these (Luke 24:25-27, 44-47) is the unity of '
        'biblical revelation.</p>'
    ),
    'moab': (
        '<p>The nation east of the Dead Sea, descended from Lot through his elder daughter (Gen 19:36-37) &mdash; '
        'an origin Scripture records with stark honesty. Moab\'s history with Israel was chronically '
        'antagonistic: Balak king of Moab hired Balaam to curse Israel (Num 22-24); Moabite women '
        'seduced Israel into Baal-Peor idolatry (Num 25); the Moabites were excluded from the assembly '
        'of the LORD to the tenth generation (Deut 23:3); Judges 3 narrates Eglon king of Moab\'s '
        'eighteen-year oppression of Israel ended by Ehud\'s left-handed dagger. Yet from Moab came '
        'Ruth the Moabitess (Ruth 1-4), great-grandmother of David and therefore ancestress of Christ '
        '(Matt 1:5). The biblical pattern is theologically loaded: even the excluded-nation could '
        'produce the woman through whom Messiah came, when faith bound her to the people of the LORD '
        '(Ruth 1:16). Moab is the test case for the gospel\'s reach: nations that produced enmity '
        'could also, through individual faith, contribute to the messianic line. Grace ran further '
        'than the law\'s exclusions.</p>'
    ),
    'nazirite-vow': (
        '<p>The voluntary vow of separation to YHWH described in Numbers 6:1-21. The Hebrew '
        '<em>nazir</em> (separated, consecrated) names both the vow and its taker. Three external '
        'distinctives marked the Nazirite during the vow period: (1) abstention from wine, strong '
        'drink, and any grape product (even raisins and grape seeds); (2) leaving the hair uncut for '
        'the entire vow period; (3) avoiding contact with any dead body, even of close family. The '
        'vow could be temporary (with a closing ceremony at the tabernacle/temple) or lifelong. '
        'Biblical lifelong Nazirites include Samson (Judg 13:5), Samuel (1 Sam 1:11; though the word '
        '<em>Nazirite</em> is not explicit), and John the Baptist (Luke 1:15). Paul took a temporary '
        'vow concluding at Cenchreae (Acts 18:18) and again in Jerusalem (Acts 21:23-26). The '
        'Nazirite\'s public uncut hair was visible testimony of dedication: the vow took on the man\'s '
        'body the marks of separation that distinguished him from ordinary Israelites. Christ '
        'Himself, though sometimes confused with Nazirite-style figures, was distinguished as <em>a '
        'Nazarene</em> (from Nazareth), not <em>a Nazirite</em> (Matt 2:23).</p>'
    ),
    'prayer-of-confession': (
        '<p>The corporate confession of sin in worship &mdash; congregation acknowledging their sins '
        'to God in united voice. The biblical pattern is well-established: Daniel 9 (Daniel\'s '
        'confession for the sins of Israel that brought the seventy-year exile); Nehemiah 9 (the '
        'post-exilic congregation\'s extended confession that names the long history of Israel\'s '
        'covenant unfaithfulness); Ezra 9 (Ezra\'s confession over mixed marriages); Psalm 51 '
        '(David\'s personal confession after Bathsheba and Uriah, used liturgically by the church for '
        'twenty centuries). The 1 John 1:9 promise (<em>If we confess our sins, he is faithful and '
        'just to forgive us our sins, and to cleanse us from all unrighteousness</em>) anchors the '
        'practice in the new covenant. Liturgical traditions include a corporate confession prayer '
        'early in the worship service, often paired with a declaration of pardon from Scripture. The '
        'corporate form does not replace personal confession but supplements it: the congregation '
        'acknowledges its shared sins, repents corporately, and receives shared assurance of '
        'forgiveness through Christ. The practice cultivates the church\'s collective awareness of '
        'its need for grace.</p>'
    ),
    'promise-keeping': (
        '<p>The faithfulness to fulfill what one has spoken. Modeled foundationally by God: <em>God '
        'is not a man, that he should lie; neither the son of man, that he should repent: hath he '
        'said, and shall he not do it? or hath he spoken, and shall he not make it good?</em> (Num '
        '23:19). 2 Corinthians 1:20: <em>For all the promises of God in him are yea, and in him '
        'Amen.</em> God\'s promise-keeping is the bedrock of every other Christian doctrine; if God '
        'does not keep His word, nothing remains. The human application is Psalm 15, the psalm of '
        'the man who dwells in the LORD\'s tabernacle: <em>He that sweareth to his own hurt, and '
        'changeth not</em> (v. 4). The biblical man\'s promise binds him even when keeping it costs '
        'him personally &mdash; precisely the test that distinguishes promise-keeping from '
        'convenience-keeping. Christ\'s teaching in Matthew 5:33-37 raises the bar: rather than '
        'negotiating oath-categories, let your yes be yes and your no be no. The Christian who has '
        'learned promise-keeping is the Christian whose word stands without oath because his '
        'character is reliable.</p>'
    ),
    'quaternion': (
        '<p>A Roman military squad of four soldiers. Acts 12:4 records King Herod Agrippa I assigning '
        '<em>four quaternions of soldiers</em> (sixteen total) to guard the imprisoned Peter: <em>And '
        'when he had apprehended him, he put him in prison, and delivered him to four quaternions of '
        'soldiers to keep him; intending after Easter to bring him forth to the people.</em> The '
        'arrangement reflected standard Roman watch-protocol: each quaternion stood watch for one of '
        'four three-hour watches of the night (6 PM-9 PM, 9 PM-midnight, midnight-3 AM, 3 AM-6 AM), '
        'with the duty rotating across the night. Two soldiers were chained directly to Peter\'s '
        'wrists; two more stood at the doors. Despite this security, an angel came in the night, '
        'struck Peter on the side, woke him, caused the chains to fall off, led him past two ward '
        'stations and through the iron gate of the prison that opened of its own accord (Acts '
        '12:7-10). Sixteen Roman soldiers could not hold Peter when the LORD intended his release. '
        'The episode\'s pointed irony was not lost on Luke or his readers.</p>'
    ),
    'seder': (
        '<p>The ordered Passover meal commanded in Exodus 12 and retold annually by Jewish families '
        'across the Diaspora. Hebrew <em>seder</em> (order) names the prescribed sequence: the meal '
        'follows a fixed structure with specific elements eaten in specific order, each carrying '
        'symbolic significance. The Mosaic essentials &mdash; bitter herbs (recalling the bitterness '
        'of Egyptian slavery), unleavened bread (the haste of departure), roasted lamb (the '
        'substitutionary blood sprinkled on the doorposts) &mdash; were elaborated in post-biblical '
        'Jewish tradition into the fifteen-step modern Seder with its four cups of wine, the asking '
        'of the four questions by the youngest child, the recitation of the Haggadah (the story of '
        'the exodus), the closing prayer <em>Next year in Jerusalem</em>. Christ instituted the '
        'Lord\'s Supper at a Passover Seder (Matt 26; Mark 14; Luke 22; the precise chronology '
        'between Synoptics and John has been long discussed), specifically reframing two of its '
        'elements: the bread became His body broken, the cup became His blood of the new covenant. '
        'The continuity is theologically loaded: the meal that commemorated the original deliverance '
        'becomes the meal that commemorates the greater deliverance accomplished through the true '
        'Passover Lamb.</p>'
    ),
    'selah': (
        '<p>A Hebrew term appearing 71 times in the Psalms and 3 times in Habakkuk 3, traditionally '
        'understood as a liturgical or musical direction. The exact meaning is uncertain; proposed '
        'derivations include <em>pause</em> (from <em>salah</em>, to lift or weigh), <em>forever</em> '
        '(from <em>selah</em> with permanence-meaning), or a musical interlude marker. The Septuagint '
        'renders it <em>diapsalma</em> (between psalm-parts), supporting the pause interpretation. '
        'Whatever the precise musical function, the spiritual effect for the reader is consistent: '
        '<em>selah</em> marks the moment when the psalmist invites the reader to stop, weigh, and '
        'absorb what has been said before moving to the next thought. Psalm 3:2: <em>many there be '
        'which say of my soul, There is no help for him in God. Selah.</em> The trouble is named; the '
        'reader is invited to sit with it before the psalmist speaks the answer. The Christian reader '
        'of the Psalms learns to honor <em>selah</em> &mdash; to read slowly, to feel what the '
        'psalmist felt, to be shaped by the pause as well as by the words.</p>'
    ),
    'serpent-wise': (
        '<p>The shrewd practical wisdom Christ commands of His disciples in mission. Matthew 10:16: '
        '<em>Behold, I send you forth as sheep in the midst of wolves: be ye therefore wise as '
        'serpents, and harmless as doves.</em> The Greek <em>phronimos</em> (prudent, wise in '
        'practical action) is paired with dove-harmlessness as the two halves of mature Christian '
        'navigation in a hostile world. Serpent-wisdom is not deceitfulness (which would belong to '
        'the literal serpent of Gen 3) but situational shrewdness &mdash; reading the threat '
        'environment accurately, choosing one\'s words with care, recognizing when silence serves '
        'better than speech, navigating dangerous social and political contexts without naive '
        'self-exposure. Christ Himself models the disposition: His timing of public moves, His '
        'parabolic teaching that both reveals and conceals, His pointed questions that expose '
        'opponents\' positions without His having to assert. Paired with dove-purity of motive, '
        'serpent-wisdom is the Christian\'s safe operating mode in a wolves-among-sheep world. '
        'Either virtue alone fails: serpent without dove is cunning; dove without serpent is naive.</p>'
    ),
    'teraphim': (
        '<p>Household idols used for divination and as markers of inheritance-rights in patriarchal '
        'and early Israelite contexts. The Hebrew <em>teraphim</em> appears throughout the OT in '
        'consistently negative context. Rachel stole her father Laban\'s teraphim when Jacob fled '
        'Mesopotamia (Gen 31:19, 30-35) &mdash; possibly to claim inheritance rights or to bring '
        'household-god protection along with her, but Scripture treats the act as theologically '
        'problematic. Michal placed a teraphim in David\'s bed to deceive Saul\'s messengers (1 Sam '
        '19:13) &mdash; suggesting it was approximately human-sized. Josiah destroyed the teraphim in '
        'his reforming purge (2 Kings 23:24): <em>And the workers with familiar spirits, and the '
        'wizards, and the images, and the idols, and all the abominations that were spied in the land '
        'of Judah and in Jerusalem, did Josiah put away.</em> Zechariah 10:2 condemns those who '
        'consult the teraphim: <em>For the idols have spoken vanity, and the diviners have seen a '
        'lie.</em> The category belongs with the Deut 18:10-12 list of forbidden divinatory '
        'practices; teraphim are pre-modern household idolatry, with the same biblical verdict as '
        'modern occult tools.</p>'
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
