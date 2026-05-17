#!/usr/bin/env python3
"""Expand 25 more short dictionary entries to 90-120 words each (batch 5)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'zechariah': (
        '<p>Post-exilic prophet (active c. 520 BC), contemporary of Haggai, son of Berechiah, son of Iddo '
        '(Zech 1:1). His ministry began in the second year of Darius and was directed at the discouraged '
        'returnees rebuilding the second temple in Jerusalem. The book of Zechariah falls into two parts: '
        'chs. 1-8 contain eight night visions and oracles encouraging the temple project; chs. 9-14 contain '
        'remarkable Messianic prophecies that are quoted extensively in the NT &mdash; the King coming '
        'humble and riding on a donkey (9:9; Matt 21:5), the thirty pieces of silver (11:12-13; Matt 27:9), '
        'the pierced one mourned (12:10; John 19:37; Rev 1:7), the smitten Shepherd (13:7; Matt 26:31), and '
        'the return of the LORD to the Mount of Olives (14:4). Zechariah\'s vision of the Branch (3:8; 6:12) '
        'is one of Scripture\'s clearest pre-NT names for the coming Messiah. The prophet whose ministry '
        'began with temple-encouragement ended with the broadest sweep of messianic vision in the Minor '
        'Prophets.</p>'
    ),
    'haughty': (
        '<p>The disposition of exalting oneself above others &mdash; high-and-mighty pride that looks down '
        'rather than across or up. Hebrew <em>gabhah</em> (to be high, exalted, lifted up) carries the literal '
        'sense of physical height applied to inner disposition. Scripture pairs haughtiness with destruction '
        'in Proverbs 16:18: <em>Pride goeth before destruction, and an haughty spirit before a fall.</em> '
        'Isaiah declares the day of the LORD against <em>every one that is proud and lofty, and upon every '
        'one that is lifted up</em>, with the result that <em>the haughtiness of men shall be bowed down... '
        'and the LORD alone shall be exalted in that day</em> (Isa 2:11-12). Haughty eyes are among the seven '
        'things the LORD hates (Prov 6:16-17). The disposition is not personality; it is sin, and the '
        'biblical man learns to walk humbly (Mic 6:8) precisely as the protection against the haughty fall.</p>'
    ),
    'heave-offering': (
        '<p>An offering portion <em>lifted up</em> and set apart for God, often becoming the priests\' food '
        'allotment within the broader sacrificial system. Hebrew <em>terumah</em> (contribution, heave-offering), '
        'from <em>rum</em> (to be high, lifted). The heave-offering was distinguished from the <em>wave-offering</em> '
        '(<em>tenufah</em>) by gesture: heaved was lifted vertically; waved was moved horizontally. Both '
        'were ritual acts of dedicating a portion to the LORD. Numbers 18:8-32 establishes the heave-offerings '
        'as the priestly portion &mdash; the priests had no land inheritance, so the heaved portions of '
        'sacrifices, firstfruits, and tithes became their material support. Exodus 29:27 designates portions '
        'of the consecration sacrifices as heave-offerings. The NT picks up the theme as believers themselves '
        'become a kind of offering presented to God (Rom 12:1: <em>present your bodies a living sacrifice</em>) '
        '&mdash; the whole person heaved up to the Lord in consecrated service.</p>'
    ),
    'hosea': (
        '<p>The first of the twelve Minor Prophets, son of Beeri, who prophesied to the northern kingdom '
        'of Israel in the eighth century BC during the reigns of Jeroboam II and successive kings, leading '
        'up to Assyria\'s 722 BC conquest. The book\'s defining feature is the prophet\'s own marriage to '
        '<em>Gomer the daughter of Diblaim</em> (Hosea 1:2-3), a wife of harlotries, taken at God\'s command '
        'as a living symbol of God\'s covenant relationship to unfaithful Israel. Their children are given '
        'symbolic judgment-names (Jezreel, Lo-ruhamah <em>no mercy</em>, Lo-ammi <em>not my people</em>) that '
        'are later reversed in the gospel restoration (1:10-2:1). The book oscillates between the LORD\'s '
        'judgment-oracles against Israel\'s spiritual adultery (chs. 4-13) and breath-taking declarations '
        'of His covenant love: <em>I drew them with cords of a man, with bands of love</em> (11:4); '
        '<em>How shall I give thee up, Ephraim?</em> (11:8); and the closing call <em>O Israel, return unto '
        'the LORD thy God</em> (14:1). Hosea\'s broken marriage is the OT\'s most extended living parable '
        'of God\'s pursuing love.</p>'
    ),
    'oath-keeping': (
        '<p>The fulfillment of oaths sworn before God &mdash; an act of fundamental moral seriousness in '
        'Scripture. Ecclesiastes 5:4-5: <em>When thou vowest a vow unto God, defer not to pay it; for he '
        'hath no pleasure in fools: pay that which thou hast vowed. Better is it that thou shouldest not '
        'vow, than that thou shouldest vow and not pay.</em> Leviticus 19:12: <em>And ye shall not swear by '
        'my name falsely, neither shalt thou profane the name of thy God: I am the LORD.</em> Numbers 30:2: '
        '<em>If a man vow a vow unto the LORD, or swear an oath to bind his soul with a bond; he shall not '
        'break his word, he shall do according to all that proceedeth out of his mouth.</em> Christ in '
        'Matthew 5:33-37 raises the standard further: rather than negotiating oath-categories, let your yes '
        'be yes and your no be no. The principle stands: the Christian\'s word binds him, oaths or not. '
        'Promise-keeping is not religious extra; it is the foundation of trustworthy character.</p>'
    ),
    'socinianism': (
        '<p>The 16th-17th century rationalist heresy founded by Italian uncle-and-nephew theologians Lelio '
        'Sozzini (1525-1562) and Fausto Sozzini (1539-1604), the latter giving the movement its name. '
        'Socinianism developed in Poland in the late 16th century and spread through pamphlet literature '
        'across Europe. Its core doctrines all denied historic Christian orthodoxy: the Trinity (one God in '
        'three persons) was rejected as irrational; the deity of Christ was denied (Christ a uniquely '
        'gifted man, but not God); the substitutionary atonement was repudiated (Christ\'s death was '
        'exemplary moral teaching, not satisfaction of divine justice); original sin was denied; and the '
        'doctrine of justification by imputed righteousness was abandoned. Socinian thought was the direct '
        'ancestor of 18th-century Unitarianism and 19th-century theological liberalism. Wherever the '
        'Trinitarian-incarnational-atonement core of orthodox faith has been quietly retired in modern '
        'mainline Protestantism, the underlying movement is Socinianism by a different name. The early '
        'Reformers (Calvin, Beza) and Reformed orthodox writers (Owen) wrote extensively against it.</p>'
    ),
    'ur-chaldees': (
        '<p>The ancient city in southern Mesopotamia from which God called Abram out by faith. Archaeological '
        'identification with Tell el-Muqayyar in modern Iraq, excavated by Leonard Woolley in the 1920s, '
        'revealed a major Sumerian-then-Babylonian urban center with a great ziggurat dedicated to the moon '
        'god Nanna/Sin, sophisticated craftsmanship, and an organized commercial economy. Genesis 11:31 '
        'narrates Terah taking Abram, Sarai, and Lot from Ur to Haran; Genesis 12 records the LORD\'s call '
        'to Abram in Haran (or perhaps initially in Ur, per Stephen\'s account in Acts 7:2-4). Genesis 15:7 '
        'has the LORD\'s self-identification: <em>I am the LORD that brought thee out of Ur of the Chaldees, '
        'to give thee this land to inherit it.</em> Hebrews 11:8 frames Abram\'s departure as the canonical '
        'act of faith: <em>he went out, not knowing whither he went.</em> Ur is the city Abram left; the '
        'promised land is the country toward which the entire Bible moves. The call from Ur is the call '
        'every Christian receives in spiritual form: leave the place you have built and follow the LORD '
        'into the place He will show you.</p>'
    ),
    '2thessalonians': (
        '<p>Paul\'s second epistle to the church at Thessalonica, written shortly after 1 Thessalonians '
        '(c. AD 51-52) to correct an eschatological confusion that had reached the congregation. Some '
        'Thessalonians had become convinced that the day of the Lord had already come (2:2) &mdash; perhaps '
        'through a misunderstood prophecy or a forged letter purporting to be from Paul. The apostle\'s '
        'response unfolds across three chapters. Chapter 1 commends the church\'s growing faith and patience '
        'in persecution, promising vengeance on their oppressors when Christ is revealed. Chapter 2 is the '
        'eschatological correction: the day cannot come until the apostasy comes first and <em>that man of '
        'sin be revealed, the son of perdition... who opposeth and exalteth himself above all that is called '
        'God</em> (2:3-4) &mdash; the man-of-lawlessness whose coming is by the working of Satan but whom '
        'the Lord will destroy <em>with the brightness of his coming</em> (2:8). Chapter 3 commands continued '
        'work, refusing the disorderly idleness that had set in among some who had taken eschatological '
        'expectation as license to stop working. Steady work while waiting is the apostolic command.</p>'
    ),
    'arrogant': (
        '<p>Claiming more for oneself than is one\'s due; the heart-disposition that exalts the self beyond '
        'what reality warrants. Greek <em>alazon</em> (boaster, braggart). James 4:6, quoting Proverbs 3:34: '
        '<em>God resisteth the proud, but giveth grace unto the humble.</em> Paul\'s catalog of last-days '
        'behavior in 2 Timothy 3:1-5 lists arrogance among the marks of perilous-times disposition: '
        '<em>For men shall be lovers of their own selves, covetous, boasters, proud, blasphemers... </em>. '
        'The arrogant heart is the inversion of the biblical pattern of Christ Himself, who being in the '
        'form of God thought it not robbery to be equal with God but emptied Himself (Phil 2:5-8). The '
        'cure for arrogance is the deliberate cultivation of humility through honest reckoning with one\'s '
        'actual standing before God: a sinner saved by grace, who has nothing he did not receive (1 Cor '
        '4:7). Whoever truly knows what he was, what God has done, and what remains is no longer arrogant.</p>'
    ),
    'gath': (
        '<p>One of the five great Philistine cities (the Pentapolis: Gaza, Ashkelon, Ashdod, Gath, Ekron). '
        'Gath\'s most famous resident in Scripture is Goliath of Gath (1 Sam 17:4, 23), the champion David '
        'killed with a sling-stone in the Valley of Elah. Other giants are also associated with Gath '
        '(2 Sam 21:18-22 names four more Philistine giants killed by David\'s men). David himself fled to '
        'Gath when escaping Saul, twice taking refuge with Achish king of Gath (1 Sam 21:10-15, where he '
        'feigned madness; and 1 Sam 27:1-12, where he served under Achish as a vassal). David later '
        'conquered Gath (2 Sam 8:1; 1 Chr 18:1). Solomon\'s rebellious official Shimei broke his oath by '
        'going to Gath to recover slaves (1 Kgs 2:39-41). Archaeology identifies Gath with Tell es-Safi, '
        'where excavations have confirmed massive Philistine fortifications. The city that produced Goliath '
        'also harbored fugitive David &mdash; the deep biblical irony of the same place serving as enemy '
        'stronghold and provident refuge in different chapters of one life.</p>'
    ),
    'impudent': (
        '<p>Shameless; without proper shame in the face of holy reproof. Hebrew <em>qasheh panim</em> (hard '
        'of face) and Greek <em>anaides</em> (without shame) name the disposition. Ezekiel 2:4 records God\'s '
        'commissioning of the prophet to a people who were exactly this: <em>For they are impudent children '
        'and stiffhearted. I do send thee unto them; and thou shalt say unto them, Thus saith the Lord GOD.</em> '
        'Ezekiel 3:7 reinforces: <em>For all the house of Israel are impudent and hardhearted.</em> Proverbs '
        '7:13 describes the harlot taking the young man with <em>an impudent face</em>. The impudent heart '
        'is past blushing &mdash; it has trained itself out of the natural shame-response that would '
        'otherwise check it from sin. The cure is the recovery of biblical shame: <em>were they ashamed when '
        'they had committed abomination? nay, they were not at all ashamed, neither could they blush: '
        'therefore shall they fall</em> (Jer 6:15). The Christian recovers the capacity to be ashamed of '
        'sin and to refuse it for the sake of the One whose holiness defines the standard.</p>'
    ),
    'jest': (
        '<p>Joking, especially the kind that Scripture identifies as improper for saints &mdash; coarse, '
        'crude, off-color, or making sport of holy things. Ephesians 5:4: <em>Neither filthiness, nor '
        'foolish talking, nor jesting, which are not convenient: but rather giving of thanks.</em> The '
        'Greek <em>eutrapelia</em> (jesting) names the witty turn that has gone in the wrong direction '
        '&mdash; speech that gets laughs at the expense of holiness or virtue. Proverbs 26:18-19 captures '
        'a related pattern: <em>As a mad man who casteth firebrands, arrows, and death, So is the man that '
        'deceiveth his neighbour, and saith, Am not I in sport?</em> The cover of jest is often the smuggling '
        'of cruelty, of mockery of the holy, or of sexual coarseness past the natural protection of shame. '
        'The Christian is not joyless; Proverbs honors a merry heart that doeth good like a medicine (17:22). '
        'The line is between godly laughter that brightens and ungodly jesting that corrupts. The first is '
        'commanded; the second is forbidden.</p>'
    ),
    'judah': (
        '<p>Fourth son of Jacob and Leah (Gen 29:35), and the tribe, kingdom, and royal line that bore the '
        'messianic promise. Jacob\'s blessing in Genesis 49:8-12 places the scepter and the lawgiver in '
        'Judah\'s hand and prophesies <em>until Shiloh come</em> &mdash; an ancient messianic title. The '
        'tribe took the lead in the wilderness camping order (Num 2:9) and led Israel\'s conquest of Canaan. '
        'David and Solomon were of Judah; the divided kingdom after Solomon left the southern kingdom of '
        'Judah (vs. the ten northern tribes of Israel) as the surviving line through which the Davidic '
        'covenant continued. Babylon\'s exile of Judah in 586 BC left the people known as Jews '
        '(<em>yehudim</em>, men of Judah). Christ Himself is <em>the Lion of the tribe of Juda</em> (Rev '
        '5:5), born of Mary in Bethlehem of Judah. Every messianic prophecy traces through Judah\'s line. '
        'The kingdom that nearly perished in exile was preserved through it for the King\'s arrival.</p>'
    ),
    'matthew-18': (
        '<p>Matthew\'s chapter on the kingdom\'s internal life &mdash; greatness, lostness, discipline, and '
        'forgiveness. It opens with Christ\'s answer to the disciples\' question about who is greatest in '
        'the kingdom: a little child set in the midst, with the warning that <em>except ye be converted, '
        'and become as little children, ye shall not enter into the kingdom of heaven</em> (v. 3). The '
        'shepherd-and-lost-sheep parable (vv. 12-14) shows the Father\'s heart for every wandering one. The '
        'four-step process of church discipline (vv. 15-20) is one of the NT\'s clearest applied procedures: '
        'go privately, then with one or two witnesses, then before the church, then treat as a Gentile and '
        'tax collector if there is no repentance. Verses 19-20 contain the promise of Christ\'s presence '
        'where two or three are gathered in His name. The chapter closes with Peter\'s question about '
        'how often to forgive a brother (v. 21) and Christ\'s parable of the unforgiving servant (vv. 23-35) '
        'with its devastating warning: forgive from the heart or face the same wrath. Greatness, discipline, '
        'and forgiveness are bound together in the chapter\'s structure.</p>'
    ),
    'meal-offering': (
        '<p>The grain offering of the Mosaic sacrificial system, distinct from the animal sacrifices but '
        'integral to the whole. Leviticus 2 details its preparation: fine flour, oil, and frankincense, '
        'either uncooked (with a handful burned as a <em>memorial</em>) or baked in oven, pan, or frying-pan '
        '(also with a memorial portion). Always unleavened (no leaven or honey could be burned to the LORD, '
        'Lev 2:11), always salted (<em>the salt of the covenant</em>, Lev 2:13). Most of the offering went '
        'to Aaron and his sons as their food allotment. The meal offering accompanied burnt and peace '
        'offerings (Num 28-29) and signified the consecrated labor and dedication of the offerer &mdash; '
        'his work-product brought before God. Christ as the true grain offering is implied in the NT: '
        'He is the corn of wheat that fell into the ground and died, that He might bring forth much fruit '
        '(John 12:24). The Christian believer offers the work of his hands as continuing meal-offering '
        '(Heb 13:15-16).</p>'
    ),
    'mocker': (
        '<p>One who derides, ridicules, or makes sport of holy things. The biblical category is sharp and '
        'recurrent. Proverbs 20:1: <em>Wine is a mocker, strong drink is raging: and whosoever is deceived '
        'thereby is not wise.</em> Isaiah 28:22: <em>Now therefore be ye not mockers, lest your bands be '
        'made strong.</em> Jude 18 prophesies: <em>How that they told you there should be mockers in the '
        'last time, who should walk after their own ungodly lusts.</em> The mocker is the man who has '
        'cultivated a posture toward the holy that responds with sneer rather than wonder, with derision '
        'rather than awe, with comedy at the expense of God rather than worship in His presence. Lot\'s '
        'sons-in-law thought he was mocking when he warned of the coming destruction of Sodom (Gen 19:14) &mdash; '
        'a poignant inversion where the warning is treated as mockery by men whose entire life had become '
        'mockery of God. The Christian recovers the disposition of reverence and refuses to be one of the '
        'last-days mockers Jude warned about.</p>'
    ),
    'prostration': (
        '<p>The full-body collapse before the manifest holiness of God. Hebrew <em>shachah</em> (to bow down, '
        'prostrate) and Greek <em>proskuneo</em> (to fall before, worship). Scripture\'s great prostration '
        'moments are revelations: Abraham fell on his face when God appeared (Gen 17:3); Joshua fell on his '
        'face before the captain of the host of the LORD (Josh 5:14); Ezekiel fell on his face at every '
        'vision (Ezek 1:28; 3:23; 43:3; 44:4); Daniel fell on his face before the man-clothed-in-linen '
        '(Dan 10:9); Peter fell at Jesus\' knees after the miraculous catch (Luke 5:8); Saul fell to the '
        'earth on the Damascus road (Acts 9:4); John fell at the feet of the glorified Christ in Revelation '
        '1:17 <em>as dead</em>. The prostration is not religious decoration; it is the natural response of '
        'creature-flesh to genuine encounter with the holy. The modern church\'s reflexive informality before '
        'the LORD often signals not theological sophistication but unfamiliarity with what actual presence '
        'feels like. Where God is known, prostration is not commanded; it happens.</p>'
    ),
    'rebellion': (
        '<p>Active resistance to legitimate authority &mdash; especially God\'s. Hebrew <em>marad</em> '
        '(to rebel, revolt) and <em>marah</em> (to be contentious, rebellious). Scripture treats rebellion '
        'with extraordinary seriousness. 1 Samuel 15:23 equates it with witchcraft: <em>For rebellion is '
        'as the sin of witchcraft, and stubbornness is as iniquity and idolatry.</em> Rebellion against God '
        'is the root of the fall (Gen 3) and of Satan\'s prior rebellion (Isa 14:12-15; Ezek 28:12-17); the '
        'NT calls Christians out of children of disobedience (Eph 2:2) into the obedience of faith (Rom 1:5). '
        'Rebellion against legitimate human authority is also forbidden (Rom 13:1-5; 1 Pet 2:13-17; Heb '
        '13:17) &mdash; submission to magistrates, elders, husbands, parents, employers, each in their '
        'God-appointed sphere. The exception is when human authority commands what God forbids: <em>we ought '
        'to obey God rather than men</em> (Acts 5:29). Outside that exception, rebellion is sin and is '
        'gravely weighted in Scripture.</p>'
    ),
    'restraint': (
        '<p>The disposition of holding-back from evil &mdash; from speech, from action, from indulgence. '
        'Proverbs identifies it as a mark of wisdom: <em>In the multitude of words there wanteth not sin: '
        'but he that refraineth his lips is wise</em> (10:19); <em>He that hath knowledge spareth his words: '
        'and a man of understanding is of an excellent spirit</em> (17:27). The Hebrew <em>chasak</em> '
        '(restrain, keep back, refrain) and Greek <em>egkrateia</em> (self-control, temperance) name the '
        'disposition. Restraint differs from cowardice: cowardice fails to act when action is required; '
        'restraint refuses to act when refraining is required. It is named as fruit of the Spirit (Gal 5:23: '
        '<em>temperance</em>) and as a mark of mature character (2 Pet 1:6: <em>add to your faith... '
        'temperance</em>). The biblical man is not driven by every appetite or impulse; he has cultivated '
        'the strength to wait, to refuse, to hold-back, to keep his own counsel until the time is right. '
        'Restraint is strength under God\'s direction, not weakness or hesitation.</p>'
    ),
    'shrewd': (
        '<p>Sharp-witted, prudent, practically wise in the navigation of complex situations. Christ '
        'commends shrewdness in the parable of the unjust steward (Luke 16:1-9): <em>And the lord commended '
        'the unjust steward, because he had done wisely [shrewdly]: for the children of this world are in '
        'their generation wiser than the children of light.</em> The praise is for the steward\'s practical '
        'cleverness in securing his future, not for his dishonesty. Christ\'s point: His followers should '
        'apply equal practical intelligence to eternal-stakes situations. Matthew 10:16 issues the parallel '
        'command: <em>be ye therefore wise as serpents, and harmless as doves.</em> The Christian is to '
        'combine the serpent\'s shrewd assessment of a hostile environment with the dove\'s harmless purity '
        'of intent. Christ\'s own dealings with religious leaders show this combination &mdash; He answers '
        'their trap-questions with questions that expose their own positions, He uses parables that conceal '
        'and reveal simultaneously, He times His public movements with prudent awareness of when the hour '
        'has come. Shrewdness without dove-purity becomes cunning; dove-purity without shrewdness becomes '
        'naive. Christ commands both.</p>'
    ),
    'soberness': (
        '<p>Sound-mindedness; clear-headed seriousness; the disposition Paul commands in Titus 2:12 (<em>that, '
        'denying ungodliness and worldly lusts, we should live soberly, righteously, and godly, in this '
        'present world</em>) and Peter in 1 Peter 5:8 (<em>Be sober, be vigilant; because your adversary the '
        'devil, as a roaring lion, walketh about, seeking whom he may devour</em>). The Greek <em>nepho</em> '
        '(to be sober) and <em>sophron</em> (of sound mind) are paired throughout the pastoral epistles '
        '(1 Tim 3:2, 11; Titus 1:8; 2:2, 4, 5, 6, 12) as essential qualifications for Christian leaders '
        'and standards for the whole church. Biblical sobriety is broader than abstention from drunkenness '
        '(though that is included); it is the disciplined alertness of mind that refuses both intoxication '
        '(literal or metaphorical) and the opposite extreme of fanatical emotional indulgence. The sober '
        'Christian is awake, watchful, judgment-engaged, capable of clear thought under pressure &mdash; '
        'the very disposition required for serving in a hostile world and watching for the Lord\'s return '
        '(1 Thess 5:6-8).</p>'
    ),
    'taunt': (
        '<p>A song or speech of bitter mockery, especially the prophetic taunt-song against fallen kings and '
        'nations. Hebrew <em>mashal</em> in this specific genre: a proverb-song that derides a defeated '
        'enemy. The canonical example is Isaiah 14, the taunt against the king of Babylon: <em>How art thou '
        'fallen from heaven, O Lucifer, son of the morning! how art thou cut down to the ground, which '
        'didst weaken the nations!</em> (v. 12) &mdash; a song that begins as derision of Babylon\'s human '
        'king and lifts toward the dragon-fall behind every tyrant. Habakkuk 2:6 introduces a fivefold woe-'
        'taunt against the Chaldean: <em>Shall not all these take up a parable against him, and a taunting '
        'proverb against him?</em> Micah 2:4 promises that when judgment falls, the people will <em>take '
        'up a parable</em> against themselves. The taunt-song is a specific prophetic genre with theological '
        'function: the LORD\'s victory over His enemies is rehearsed in song, not gloated over personally '
        'but proclaimed publicly as testimony to His justice. The taunt belongs to the LORD\'s vindication, '
        'not the saints\' private contempt.</p>'
    ),
    'te-deum': (
        '<p>The early Christian hymn <em>Te Deum laudamus</em> (<em>We praise thee, O God</em>), traditionally '
        'attributed to Ambrose of Milan and Augustine of Hippo, dated to the late fourth or early fifth '
        'century. Modern scholarship more often attributes it to Nicetas of Remesiana (c. 335-414). The hymn '
        'is a Trinitarian doxology in three movements: praise to the Father (we praise thee, O God, we '
        'acknowledge thee to be the Lord), praise of the Son (when thou tookest upon thee to deliver man), '
        'and intercession (we therefore pray thee, help thy servants, whom thou hast redeemed with thy '
        'precious blood). The Te Deum has been used liturgically across the Western church for over fifteen '
        'centuries at major Christian celebrations &mdash; the consecration of bishops, royal coronations, '
        'military victories, ordinary Sunday morning Matins. Numerous composers (Handel, Bruckner, Berlioz, '
        'Verdi) have set it. The hymn\'s endurance is a testimony to its theological grandeur: it gathers '
        'the church across centuries and cultures into one Trinitarian song of praise.</p>'
    ),
    'yielded': (
        '<p>Surrendered, presented, handed-over &mdash; Paul\'s central language for the believer\'s self-'
        'offering to God. Romans 6:13: <em>Neither yield ye your members as instruments of unrighteousness '
        'unto sin: but yield yourselves unto God, as those that are alive from the dead, and your members '
        'as instruments of righteousness unto God.</em> Romans 12:1: <em>I beseech you therefore, brethren, '
        'by the mercies of God, that ye present your bodies a living sacrifice, holy, acceptable unto God, '
        'which is your reasonable service.</em> The Greek <em>paristemi</em> (to present, place beside, '
        'yield) has the active sense of setting oneself or one\'s members at God\'s disposal. The yielded '
        'Christian is the Christian who has stopped negotiating with God over which parts of his life are '
        'available for redirection. Eyes, hands, mind, sexuality, schedule, money, ambitions, fears &mdash; '
        'each is presented as instrument of righteousness rather than of sin. The yielding is not passive; '
        'it is the active opposite of withholding. Christian sanctification proceeds at the speed and depth '
        'of the Christian\'s yielding.</p>'
    ),
    '2john': (
        '<p>The apostle John\'s brief epistle to <em>the elect lady and her children</em> (v. 1) &mdash; '
        'thirteen verses, the shortest book in the NT after 3 John. The <em>elect lady</em> may be a specific '
        'Christian woman host of a house-church or, more likely, a particular local church personified as '
        'a lady (the church as Bride being a common NT image). The letter rejoices that John has found some '
        'of her children walking in truth (v. 4), commands the central Christian duties of mutual love and '
        'continuing in the apostolic doctrine, and issues a sharp warning against false teachers who deny '
        'the incarnation: <em>For many deceivers are entered into the world, who confess not that Jesus '
        'Christ is come in the flesh. This is a deceiver and an antichrist</em> (v. 7). Verse 10 instructs '
        'the church to refuse hospitality to such teachers: <em>If there come any unto you, and bring not '
        'this doctrine, receive him not into your house, neither bid him God speed.</em> The brief letter '
        'balances love and discernment: love within the truth, refusal of hospitality outside it. The two '
        'do not contradict.</p>'
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
