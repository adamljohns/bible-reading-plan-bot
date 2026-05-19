#!/usr/bin/env python3
"""Expand 25 more thin entries to 90-110 words each (batch 8)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'bible-reading': (
        '<p>The discipline of regular, attentive intake of Scripture &mdash; God\'s breathed-out words for '
        'instruction, reproof, correction, and training in righteousness (2 Tim 3:16-17). The biblical '
        'pattern commends daily intake: Joshua 1:8 (<em>This book of the law shall not depart out of thy '
        'mouth; but thou shalt meditate therein day and night</em>); Psalm 1:2 (<em>his delight is in the '
        'law of the LORD; and in his law doth he meditate day and night</em>); Deut 6:6-9 (the words bound '
        'to hand, between the eyes, on doorposts). The Bereans were commended for daily searching the '
        'scriptures (Acts 17:11). Paul exhorts Timothy to <em>give attendance to reading</em> (1 Tim 4:13). '
        'Bible reading is the foundational Christian discipline; every other discipline (prayer, worship, '
        'witness, work) depends on the renewed mind Scripture produces. The MOOP Watchman plan structures '
        'this as five daily watches; the discipline is not method but its result &mdash; a man shaped by '
        'God\'s words.</p>'
    ),
    'collect': (
        '<p>A short, structured prayer used in liturgical worship to gather (Latin <em>collecta</em>, '
        'gathered) the congregational attention around a single theme. The classic collect has five parts: '
        '(1) <em>address</em> &mdash; calling upon God by a specific divine name; (2) <em>attribute</em> &mdash; '
        'a clause naming the divine character relevant to the petition; (3) <em>petition</em> &mdash; the '
        'specific request; (4) <em>purpose</em> &mdash; the desired outcome; (5) <em>mediation</em> &mdash; '
        'closing through Jesus Christ our Lord. The form has been used in the Western church since the '
        'patristic period; the Book of Common Prayer\'s collects (largely by Thomas Cranmer, 1549) are '
        'among the masterpieces of English liturgical prose. The compactness of the form trains the '
        'congregation to pray with theological precision, biblical density, and corporate unity. Many '
        'Reformed traditions retain collect-form prayers; even non-liturgical evangelical traditions can '
        'profit from the discipline of writing brief structured prayers.</p>'
    ),
    'confession-of-faith': (
        '<p>The public declaration of what one believes. Biblical confession at its simplest is the '
        'cry that <em>Jesus is Lord</em> (Rom 10:9-10): <em>That if thou shalt confess with thy mouth the '
        'Lord Jesus, and shalt believe in thine heart that God hath raised him from the dead, thou shalt '
        'be saved. For with the heart man believeth unto righteousness; and with the mouth confession is '
        'made unto salvation.</em> The early church developed brief baptismal confessions that became the '
        'Apostles\' Creed; conciliar definitions produced the Nicene and Athanasian Creeds; the Reformation '
        'produced longer doctrinal confessions: the Augsburg Confession (Lutheran, 1530), the Belgic '
        'Confession (Reformed, 1561), the Heidelberg Catechism (Reformed, 1563), the Thirty-Nine Articles '
        '(Anglican, 1571), the Westminster Confession (Presbyterian, 1646), the Savoy Declaration '
        '(Congregational, 1658), the Second London Baptist Confession (1689). These confessions are not '
        'co-equal with Scripture but are faithful summaries of Scripture, providing the church\'s '
        'cumulative confession of biblical doctrine against heresy.</p>'
    ),
    'ear-discipline': (
        '<p>The discipline of guarding what the ear receives. Proverbs returns repeatedly to the theme: '
        '<em>Bow down thine ear, and hear the words of the wise, and apply thine heart unto my knowledge</em> '
        '(22:17); <em>The hearing ear, and the seeing eye, the LORD hath made even both of them</em> '
        '(20:12); <em>He that turneth away his ear from hearing the law, even his prayer shall be '
        'abomination</em> (28:9). The biblical ear is morally engaged: it can be heavy of hearing (Isa '
        '6:10), uncircumcised (Jer 6:10), or quick to hear what edifies (James 1:19). Ear discipline '
        'involves both refusal (the ear that refuses to receive gossip, mockery, slander, corrupting '
        'voices) and active reception (the ear that trains itself to hear God, wisdom, godly rebuke '
        'without flinching). The Christian who has cultivated his ears can hear correction without '
        'collapsing; the Christian who has not cannot. Christ\'s repeated <em>he that hath ears to hear, '
        'let him hear</em> assumes that hearing is a moral capacity that some have cultivated and others '
        'have not.</p>'
    ),
    'edom': (
        '<p>The nation descended from Esau, twin brother of Jacob (Gen 25:30: <em>Therefore was his name '
        'called Edom</em>, from Hebrew <em>adom</em>, red, after the red lentil pottage for which he sold '
        'his birthright). Edom settled the rocky mountainous region south of the Dead Sea, around the '
        'great city Petra. The relationship between Israel and Edom was perpetually antagonistic. Edom '
        'refused Israel passage during the wilderness wandering (Num 20:14-21). Saul and David warred '
        'with Edom (1 Sam 14:47; 2 Sam 8:13-14). Solomon\'s mines were in Edomite territory. After Judah\'s '
        'fall in 586 BC, the Edomites celebrated and helped the Babylonians plunder &mdash; the offense '
        'that prompted Obadiah\'s entire prophecy against them. The Edomites later moved north and became '
        'the Idumeans of the intertestamental period; Herod the Great was an Idumean &mdash; an Edomite '
        'ruling Israel under Roman authority. By the second century AD Edom as a distinct people ceased '
        'to exist, fulfilling the prophetic judgments of Obadiah, Isaiah 34, Jeremiah 49, and Ezekiel 25.</p>'
    ),
    'examine-self': (
        '<p>The self-examination Paul commands as part of Christian discipleship. Two key passages: '
        '1 Corinthians 11:28 (before the Lord\'s Supper): <em>But let a man examine himself, and so let '
        'him eat of that bread, and drink of that cup.</em> 2 Corinthians 13:5 (as ongoing discipleship): '
        '<em>Examine yourselves, whether ye be in the faith; prove your own selves. Know ye not your own '
        'selves, how that Jesus Christ is in you, except ye be reprobates?</em> The Greek <em>dokimazo</em> '
        '(to test, prove by examination) carries the sense of metallurgical assay &mdash; testing for '
        'genuineness rather than mere casual review. David models the prayer-form in Psalm 139:23-24: '
        '<em>Search me, O God, and know my heart: try me, and know my thoughts: And see if there be any '
        'wicked way in me, and lead me in the way everlasting.</em> Christian self-examination is not '
        'morbid introspection or self-flagellation; it is the disciplined honest reckoning with one\'s '
        'actual state before God, producing repentance where needed and assurance where genuine.</p>'
    ),
    'faithfulness-biblical': (
        '<p>Reliable steadfastness over time. God\'s primary character toward His covenant (<em>great is '
        'thy faithfulness</em>, Lam 3:23) and the character He produces in His people. Hebrew '
        '<em>emunah</em> and Greek <em>pistis</em> both carry the dual sense of <em>faith</em> '
        '(active trust) and <em>faithfulness</em> (covenantal reliability). The same word that names '
        'the believer\'s faith in Christ names Christ\'s faithfulness to His promises. God\'s faithfulness '
        'is the bedrock: <em>He is faithful that promised</em> (Heb 10:23); <em>he abideth faithful: he '
        'cannot deny himself</em> (2 Tim 2:13). The Spirit produces faithfulness as fruit (Gal 5:22), '
        'and faithfulness is the chief required quality of stewards (1 Cor 4:2: <em>Moreover it is '
        'required in stewards, that a man be found faithful</em>). The biblical man\'s faithfulness '
        'shows in long-arc consistency &mdash; same direction over decades, kept marriage, kept word, '
        'kept post. Christ\'s commendation <em>well done, thou good and faithful servant</em> (Matt '
        '25:21, 23) is the destination toward which Christian faithfulness aims.</p>'
    ),
    'firstfruits-resurrection': (
        '<p>Christ\'s resurrection as the firstfruits of the great resurrection-harvest of believers. '
        '1 Corinthians 15:20-23: <em>But now is Christ risen from the dead, and become the firstfruits '
        'of them that slept... But every man in his own order: Christ the firstfruits; afterward they '
        'that are Christ\'s at his coming.</em> The image draws on the Mosaic firstfruits offering '
        '(Lev 23:9-14): the first portion of the harvest dedicated to the LORD as both thanksgiving for '
        'the harvest begun and pledge of the full harvest to come. Christ\'s resurrection is exactly '
        'this: the first portion of the resurrection harvest, dedicated to God, guaranteeing the rest. '
        'The believer\'s bodily resurrection at Christ\'s return is the same crop, harvested in its '
        'season. The firstfruits theology grounds Christian hope objectively: Christ has been raised &mdash; '
        'the harvest has begun; nothing now can prevent the rest. The resurrection of believers is not '
        'speculative possibility; it is the inevitable continuation of a harvest already started.</p>'
    ),
    'hebrews-book': (
        '<p>A magisterial NT homily (the author is unnamed; tradition has long debated Paul, Apollos, '
        'Barnabas, Priscilla, others) proving from the Old Testament that Jesus Christ is supreme &mdash; '
        'and therefore that going back to the old covenant is unthinkable. The structure unfolds through '
        'a series of comparative arguments: Christ is greater than the angels (chs. 1-2), greater than '
        'Moses (3:1-6), greater than Joshua (3:7-4:13, with the Sabbath-rest exposition), the great High '
        'Priest after the order of Melchizedek (4:14-7:28), mediator of a better covenant (chs. 8-9), '
        'whose once-for-all sacrifice replaces the daily Levitical sacrifices (ch. 10). The famous '
        'faith-chapter (ch. 11) catalogues OT exemplars; chapter 12 calls the reader to run with '
        'patience the race set before us, looking unto Jesus; chapter 13 closes with practical '
        'exhortations. Written for a Jewish-Christian audience tempted to return to Judaism under '
        'persecution, the letter\'s central message is invariant: <em>there is no going back &mdash; '
        'because what you would go back to was the shadow, and what you have in Christ is the substance.</em></p>'
    ),
    'hosanna-acclamation': (
        '<p>The prayer-shout that begs God to save and praises Him as the saving King. Hebrew '
        '<em>hoshia-na</em> (literally <em>save now</em>, <em>save, we pray</em>), from the same root as '
        '<em>yasha</em> (to save) that gives us <em>Yeshua / Jesus</em>. The phrase originates in '
        'Psalm 118:25 (<em>Save now, I beseech thee, O LORD: O LORD, I beseech thee, send now '
        'prosperity</em>), part of the Hallel (Psalms 113-118) sung at Jewish festivals especially '
        'Passover. The crowds hailed Christ with <em>hosanna</em> at the triumphal entry (Matt 21:9, '
        'Mark 11:9, John 12:13): <em>Hosanna to the Son of David: Blessed is he that cometh in the '
        'name of the Lord; Hosanna in the highest.</em> The shout was simultaneously prayer (save now) '
        'and acclamation (the King is here). The same crowd that cried hosanna on Sunday cried '
        '<em>crucify him</em> by Friday &mdash; one of the sobering biblical pictures of crowd '
        'fickleness. The Christian liturgy still uses hosanna, particularly in the Sanctus of the '
        'communion service, joining the church across centuries to the cry of the Passover crowd.</p>'
    ),
    'insolent': (
        '<p>Arrogantly disrespectful; the bearing of those who treat sacred things and sacred persons '
        'with brash contempt. Romans 1:30 (ESV) lists <em>insolent</em> among the manifestations of the '
        'depraved mind God gives over to its desires: <em>slanderers, haters of God, insolent, haughty, '
        'boastful, inventors of evil.</em> The Greek <em>hybristes</em> (from which English '
        '<em>hubris</em>) names the disposition of one who exceeds proper bounds in his treatment of '
        'others &mdash; arrogance translated into action, often expressed in mockery, contempt, or '
        'physical aggression. Paul applies the term to his own pre-conversion self: <em>Who was before '
        'a blasphemer, and a persecutor, and injurious [hybristes]</em> (1 Tim 1:13). The transformation '
        'from insolent persecutor to humble servant testifies to the gospel\'s power. 2 Timothy 3:1-5 '
        'lists insolence (in some translations) among the marks of last-days behavior. The Christian '
        'response to insolence is not insolence-in-return but the bearing of Christ, who when reviled '
        'reviled not again.</p>'
    ),
    'invocation-prayer': (
        '<p>The opening prayer of worship that calls upon God\'s name and presence. The biblical practice '
        'of calling upon the LORD is ancient: <em>Then began men to call upon the name of the LORD</em> '
        '(Gen 4:26, the first instance after the murder of Abel). Acts 2:21 (citing Joel 2:32) declares '
        'the gospel-age promise: <em>And it shall come to pass, that whosoever shall call on the name '
        'of the Lord shall be saved.</em> Romans 10:13 reinforces. The invocation prayer in Christian '
        'liturgy gathers the congregation\'s scattered attention and consciously places the assembly '
        'before the throne of grace at the beginning of worship. Typical elements include a recognition '
        'of God\'s presence, a confession of human unworthiness, a plea for the Spirit\'s presence and '
        'illumination, and a closing through Jesus Christ. Even non-liturgical traditions usually open '
        'worship with some form of invocation, though they may not name it as such. The form embodies '
        'the foundational biblical posture: worship begins not with us reaching for God but with our '
        'calling on the God who is already near to all who call upon Him in truth.</p>'
    ),
    'lifted-hands': (
        '<p>The biblical posture of open palms raised toward heaven &mdash; a posture of prayer, '
        'blessing, oath, and praise. Psalm 28:2: <em>Hear the voice of my supplications, when I cry '
        'unto thee, when I lift up my hands toward thy holy oracle.</em> Psalm 63:4: <em>Thus will I '
        'bless thee while I live: I will lift up my hands in thy name.</em> 1 Timothy 2:8: <em>I will '
        'therefore that men pray every where, lifting up holy hands, without wrath and doubting.</em> '
        'The image carries multiple registers: empty open palms of a soul receiving (the suppliant '
        'asking God to fill), raised hands of surrender (the soldier yielding), the priestly blessing '
        'gesture (Aaron lifting hands over Israel, Lev 9:22), the oath-posture (raising the hand to '
        'heaven in covenant, Gen 14:22). Christian liturgical posture has often reduced prayer to '
        'folded hands and bowed head &mdash; pieties that have their place, but that have largely '
        'displaced the biblical posture of lifted hands. The charismatic recovery of lifted hands in '
        'worship reflects a real biblical pattern, even where the surrounding theology has sometimes '
        'gone awry.</p>'
    ),
    'quiver': (
        '<p>The case for arrows used by warriors and hunters. Psalm 127:3-5 turns the warrior image into '
        'the famous metaphor for many children: <em>Lo, children are an heritage of the LORD: and the '
        'fruit of the womb is his reward. As arrows are in the hand of a mighty man; so are children of '
        'the youth. Happy is the man that hath his quiver full of them: they shall not be ashamed, but '
        'they shall speak with the enemies in the gate.</em> The image is rich. Arrows are weapons '
        'pointed outward, sent forward, with reach beyond the warrior\'s own physical position; the man '
        'who has many sons has many extensions of his influence into the future. The full quiver is the '
        'man\'s confidence at the gate (the place of legal-judgment and civic-leadership in the ancient '
        'Israelite city). The biblical reception of children is, in a culture of declining fertility, a '
        'concrete act of faith: the man who receives children as arrows is the man who has decided his '
        'name will extend forward, his witness will continue, his influence will outlive him.</p>'
    ),
    'reparation': (
        '<p>The practical making-amends for wrong done. Beyond confession and forgiveness, biblical '
        'repentance often requires the restoration of what was taken or damaged. The Mosaic trespass '
        'offering (Lev 6:1-7) is the OT pattern: if a man wrongs his neighbor by violence, theft, or '
        'deceit, he must restore in full PLUS one fifth (twenty percent over the principal) AND bring '
        'a guilt offering. Zacchaeus models the NT pattern in Luke 19:8: <em>And Zacchaeus stood, and '
        'said unto the Lord; Behold, Lord, the half of my goods I give to the poor; and if I have taken '
        'any thing from any man by false accusation, I restore him fourfold.</em> Christ\'s response &mdash; '
        '<em>This day is salvation come to this house</em> &mdash; ties the reparation to the genuineness '
        'of the conversion. The Christian who has injured another is not merely to apologize; he is to '
        'restore wherever restoration is possible. Modern Western Christianity has often softened '
        'repentance into private confession; the biblical pattern includes the costly public restitution '
        'that proves the repentance is real.</p>'
    ),
    'reviler': (
        '<p>One who speaks abusively, attacks character, and dishonors with the tongue. Greek '
        '<em>loidoros</em>, listed alongside the catalogues of those whose habitual sin disqualifies '
        'them from kingdom inheritance: 1 Corinthians 6:10 (<em>nor revilers... shall inherit the '
        'kingdom of God</em>); 1 Corinthians 5:11 (the church is not to keep company with such a '
        'professing brother, not even to eat with him). Christ Himself bore reviling without returning '
        'it: 1 Peter 2:23: <em>Who, when he was reviled, reviled not again; when he suffered, he '
        'threatened not; but committed himself to him that judgeth righteously.</em> The reviler\'s sin '
        'is not occasional sharp words (everyone says things in heat they later regret); it is the '
        'settled habit of tongue-violence against others. Biblical correction of the reviler proceeds '
        'through church discipline (Matt 18:15-17), then exclusion if no repentance follows. The '
        'category overlaps with railer; both share the same Greek word in some passages.</p>'
    ),
    'seals-of-revelation': (
        '<p>The seven seals of the scroll, opened by the Lamb in Revelation 5-8. The scroll is sealed '
        'with seven seals (Rev 5:1); the search for one worthy to open it fails (5:2-4); only the Lamb '
        'who was slain is found worthy (5:5-9). The Lamb then opens each seal in turn (chs. 6-8:1). '
        'The first four seals release the famous Four Horsemen: white (conquest), red (war), black '
        '(famine), pale (death &mdash; Greek <em>chloros</em>, sickly green-gray). The fifth seal reveals '
        'the souls of the martyrs under the altar crying <em>How long?</em>; the sixth brings cosmic '
        'upheaval (sun darkened, moon blood-red, stars falling, heaven departing as a scroll); the '
        'seventh produces the silence in heaven for half an hour before the seven trumpet-judgments '
        'begin. Interpretations vary: historicist (each seal a phase of church history), preterist '
        '(fulfilled in the first century, especially AD 70), futurist (still to come, often in a final '
        'tribulation), idealist (recurring patterns throughout the church age). The MOOP Dictionary '
        'holds the futurist-with-historic-applicability reading as the most exegetically defensible.</p>'
    ),
    'seth-son': (
        '<p>The third son of Adam and Eve, given as the replacement for Abel. Genesis 4:25-26: <em>And '
        'Adam knew his wife again; and she bare a son, and called his name Seth: For God, said she, hath '
        'appointed me another seed instead of Abel, whom Cain slew. And to Seth, to him also there was '
        'born a son; and he called his name Enos: then began men to call upon the name of the LORD.</em> '
        'Seth\'s line is the godly line through which the messianic seed advanced (Gen 5 traces Adam to '
        'Noah through Seth, not Cain). Luke\'s genealogy of Christ runs back through Seth to Adam (Luke '
        '3:38), making Seth a direct ancestor of Jesus. The naming after Abel suggests Eve\'s '
        'recognition that the murder of one son could not destroy God\'s purpose; the LORD appoints '
        'another seed. The pattern recurs throughout Scripture: the godly seed is preserved despite '
        'apparent extinction (Noah and his family, the seventy souls of Joseph in Egypt, the surviving '
        'remnant in exile, the apostles after the cross). Seth is the first instance of the preserved-'
        'seed theme.</p>'
    ),
    'spiritual-union': (
        '<p>The Holy Spirit\'s work joining the believer to Christ &mdash; one aspect of the believer\'s '
        'union with Christ, with the Spirit emphasized as the bond. 1 Corinthians 6:17: <em>But he that '
        'is joined unto the Lord is one spirit.</em> Romans 8:9-11: <em>But ye are not in the flesh, but '
        'in the Spirit, if so be that the Spirit of God dwell in you. Now if any man have not the Spirit '
        'of Christ, he is none of his.</em> Union with Christ is one biblical reality apprehended from '
        'multiple angles: vital union (the vine and the branches, John 15), legal union (federal '
        'representation, Rom 5:12-21), mystical union (Christ in you, Col 1:27), and spiritual union '
        '(the Spirit as binding agent, 1 Cor 6:17). The same Spirit who descended on Christ at His '
        'baptism and animated His earthly ministry now indwells every believer, making the believer '
        'organically connected to Christ even at physical separation. The doctrine grounds Christian '
        'identity: not who I am in myself but who I am in Christ by the Spirit.</p>'
    ),
    'time-stewardship': (
        '<p>The discipline of redeeming time as God\'s entrusted resource. Ephesians 5:15-16: <em>See '
        'then that ye walk circumspectly, not as fools, but as wise, Redeeming the time, because the '
        'days are evil.</em> Colossians 4:5: <em>Walk in wisdom toward them that are without, redeeming '
        'the time.</em> The Greek <em>exagorazomenoi ton kairon</em> (buying up the opportune time) '
        'pictures time as a commodity to be deliberately purchased &mdash; bought back from the '
        'distractions and frivolities that would otherwise consume it. Psalm 90:12: <em>So teach us to '
        'number our days, that we may apply our hearts unto wisdom.</em> The Christian who has learned '
        'to number his days is the Christian who has begun to take time stewardship seriously. The '
        'modern enemies are specific: the slow theft of screen-time, the busy-but-fruitless calendar '
        'of low-value commitments, the procrastination that postpones the important for the urgent. '
        'The disciplined Christian audits where his hours go and reorders them around what God has '
        'entrusted to his stewardship: family, work, prayer, Word, body, witness, rest.</p>'
    ),
    'trespass-offering': (
        '<p>The Mosaic offering for specific sins involving violation of property, sacred things, or '
        'guilt requiring restitution. Hebrew <em>asham</em> (guilt offering, trespass offering). '
        'Leviticus 5:14-19 and 6:1-7 specify the offering and its context: when a man trespassed '
        'through ignorance against the holy things of the LORD, or violated his neighbor through '
        'deceit, theft, oppression, or false oath, he had to (1) restore the principal AND add one '
        'fifth (twenty percent over) to the injured party, then (2) bring a ram without blemish to '
        'the priest as a guilt offering. The order matters: restitution to the injured party first, '
        'then the offering to God. The pattern shapes biblical ethics: sin against the neighbor cannot '
        'be cleansed by God-ward ritual alone &mdash; the neighbor must be made whole. Christ\'s '
        'sacrifice fulfills the typology: He is the once-for-all guilt-offering whose blood cleanses '
        'all our trespasses (Heb 10:1-18; 1 John 1:7). The horizontal restitution-discipline remains '
        'binding on the Christian (Matt 5:23-24).</p>'
    ),
    'tyre': (
        '<p>The wealthy Phoenician city-state on the Mediterranean coast about 25 miles south of Sidon '
        '(in modern Lebanon). Originally a mainland city, Tyre established a fortified island stronghold '
        'half a mile offshore that proved nearly impregnable. Tyre was ally to David and Solomon: King '
        'Hiram of Tyre supplied cedar wood, gold, and skilled craftsmen for both David\'s palace and '
        'Solomon\'s temple (2 Sam 5:11; 1 Kgs 5; 9:11-14). Solomon\'s alliance with Tyre involved a '
        'twenty-year trade relationship that brought immense wealth to Israel. Later, however, Tyre\'s '
        'pride and trade-in-souls drew severe prophetic judgment. Ezekiel 26-28 contains an extended '
        'oracle against Tyre, with chapter 28\'s lament <em>against the king of Tyrus</em> extending '
        'into typological description of the original prince of pride (commonly interpreted as Satan): '
        '<em>thou wast in Eden the garden of God... thou art the anointed cherub that covereth.</em> '
        'Tyre fell to Nebuchadnezzar (after a 13-year siege) and later Alexander the Great (332 BC). '
        'Christ Himself visited the region of Tyre (Mark 7:24-31).</p>'
    ),
    'verily': (
        '<p>The KJV\'s standard rendering of Greek <em>amen</em> introducing a solemn declaration. '
        'Christ characteristically opened weighty statements with <em>verily I say unto you</em> (Greek '
        '<em>amen lego hymin</em>); in John\'s Gospel uniquely the word is doubled &mdash; <em>verily, '
        'verily, I say unto you</em> (Greek <em>amen amen lego hymin</em>) &mdash; for the most '
        'emphatic teaching: John 3:3 (<em>except a man be born again</em>); 5:24 (<em>he that heareth '
        'my word, and believeth on him that sent me, hath everlasting life</em>); 6:53 (<em>except ye '
        'eat the flesh of the Son of man, and drink his blood, ye have no life in you</em>). The '
        'doubled <em>amen</em> serves as Christ\'s signal that what follows is foundational, not '
        'optional, not negotiable. Unlike contemporary religious teachers who said <em>thus says the '
        'LORD</em>, Christ said <em>verily I say unto you</em> &mdash; the divine self-authority '
        'embedded in the word. The doctrine of Christ\'s deity is implicit in the formula: He speaks '
        'on His own authority because He is the authority.</p>'
    ),
    'vow-personal': (
        '<p>The discipline of making solemn, voluntary, considered promises to God and keeping them. '
        'Ecclesiastes 5:4-5: <em>When thou vowest a vow unto God, defer not to pay it; for he hath no '
        'pleasure in fools: pay that which thou hast vowed. Better is it that thou shouldest not vow, '
        'than that thou shouldest vow and not pay.</em> Numbers 30 details the law of vows. Distinguished '
        'from compulsive bargaining-with-God (<em>if you do X for me, I\'ll do Y</em>) by the deliberate, '
        'considered, future-binding nature of the biblical vow. Hannah\'s vow to dedicate her son to '
        'the LORD if He gave her one (1 Sam 1:11) is the canonical example of vow-fulfilled. The '
        'Nazirite vow (Num 6) is the priestly extension. Christ\'s caution in Matthew 5:33-37 raises '
        'the standard further: rather than negotiating vow-categories, let your yes be yes and your no '
        'be no. The biblical man uses vows sparingly but takes them with full seriousness when made. '
        'The modern Christian use includes marriage vows, baptismal vows, ordination vows, and '
        'occasionally specific personal vows (lifetime abstinence, dedicated giving, formal '
        'commitments). Each is binding on the future self by the present act.</p>'
    ),
    'wages-justice': (
        '<p>God\'s requirement that workers be paid promptly and fairly. Leviticus 19:13: <em>Thou '
        'shalt not defraud thy neighbour, neither rob him: the wages of him that is hired shall not '
        'abide with thee all night until the morning.</em> Deuteronomy 24:14-15: <em>Thou shalt not '
        'oppress an hired servant that is poor and needy... At his day thou shalt give him his hire, '
        'neither shall the sun go down upon it; for he is poor, and setteth his heart upon it: lest he '
        'cry against thee unto the LORD, and it be sin unto thee.</em> James 5:4 brings the principle '
        'into the new covenant church with sharp force: <em>Behold, the hire of the labourers who have '
        'reaped down your fields, which is of you kept back by fraud, crieth: and the cries of them '
        'which have reaped are entered into the ears of the Lord of sabaoth.</em> The biblical employer '
        'pays fairly and pays on time. The defrauded worker has direct access to the Lord of hosts &mdash; '
        'his cry reaches God\'s ears. Modern employers, Christian or otherwise, ignore this principle '
        'at their soul\'s peril. Christian business ethics begin with wages justice.</p>'
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
