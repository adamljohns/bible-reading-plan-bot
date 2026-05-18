#!/usr/bin/env python3
"""Expand 25 more Template-A under-30-word entries to 90-120 words each (batch 6)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'amos-book': (
        '<p>The third of the twelve Minor Prophets, written by Amos, a sheep-breeder and dresser of '
        'sycamore-figs from Tekoa (Amos 1:1; 7:14-15), called by God to prophesy against the prosperous '
        'northern kingdom of Israel about 760-750 BC, during the reign of Jeroboam II. The book opens with '
        'seven judgment-oracles against surrounding nations (chs. 1-2), each beginning <em>for three '
        'transgressions of [nation], and for four, I will not turn away the punishment thereof</em> &mdash; '
        'a rhetorical buildup that ends with the eighth and most extensive oracle against Israel itself. '
        'The middle chapters (3-6) deliver thunderous indictment of social injustice (the rich crushing '
        'the poor), religious hypocrisy (elaborate worship while practicing oppression), and complacent '
        'prosperity (<em>woe to them that are at ease in Zion</em>, 6:1). Five visions follow (chs. 7-9) '
        'culminating in the promise of restoration through the Davidic line (9:11-15), quoted by James at '
        'the Jerusalem Council (Acts 15:16-17) as the warrant for Gentile inclusion in the church.</p>'
    ),
    'ashdod': (
        '<p>One of the five great Philistine cities (the Pentapolis: Gaza, Ashkelon, Ashdod, Gath, Ekron), '
        'on the southern coastal plain of Canaan. Ashdod is famous as the city where the captured Ark of '
        'the Covenant was first taken after the Philistines defeated Israel at the battle of Ebenezer '
        '(1 Sam 4-5). The Philistines placed the ark in the temple of their god Dagon. The next morning, '
        'Dagon\'s statue was found prostrate before the ark; the morning after that, Dagon\'s head and hands '
        'lay broken on the threshold. The LORD then afflicted the city with tumors (1 Sam 5:6), forcing '
        'the Philistines to send the ark to Gath, then Ekron, before finally returning it to Israel. The '
        'prophets pronounce judgment-oracles against Ashdod (Amos 1:8; Isa 20:1; Jer 25:20; Zeph 2:4; '
        'Zech 9:6). Archaeology has identified Ashdod with Tel Ashdod, where extensive Philistine and later '
        'remains have been excavated.</p>'
    ),
    'ashkelon': (
        '<p>One of the five great Philistine cities (the Pentapolis: Gaza, Ashkelon, Ashdod, Gath, Ekron), '
        'an ancient seaport on the Mediterranean coast about ten miles north of Gaza. Ashkelon\'s biblical '
        'appearances span much of the OT: Samson killed thirty men of Ashkelon to pay his wager-debt to '
        'the Philistines (Judg 14:19); David\'s lament over Saul\'s death prays <em>Tell it not in Gath, '
        'publish it not in the streets of Askelon</em> (2 Sam 1:20). The prophets pronounce repeated '
        'judgment: Jeremiah 47, Zephaniah 2:4-7, Zechariah 9:5, Amos 1:8, Jer 25:20. Ashkelon\'s long '
        'history continued past the OT period into Roman times; Herod the Great built up the city in the '
        'first century BC. Archaeology has uncovered extensive Canaanite, Philistine, Persian, Hellenistic, '
        'and Roman remains, including the oldest known city wall in the Levant (c. 1850 BC) and a Roman-era '
        'street that ran through ancient public buildings.</p>'
    ),
    'beauty': (
        '<p>The created harmony, fittingness, and glory that reflects the character of God. Beauty is one '
        'of the three classical <em>transcendentals</em> &mdash; truth, goodness, beauty &mdash; that are '
        'properties of being itself, grounded in God\'s nature. Psalm 27:4 names the singular desire of '
        'David\'s life: <em>One thing have I desired of the LORD, that will I seek after; that I may dwell '
        'in the house of the LORD all the days of my life, to behold the beauty of the LORD, and to '
        'inquire in his temple.</em> Ecclesiastes 3:11: <em>He hath made every thing beautiful in his '
        'time.</em> Psalm 96:6: <em>strength and beauty are in his sanctuary.</em> Created beauty (the '
        'night sky, the mountain, the wife of one\'s youth, music, craftsmanship, justice rightly done) '
        'is real and theologically significant: it points beyond itself to the uncreated Beauty in whom '
        'every beautiful thing finds its source. Modern utilitarian aesthetics has impoverished the '
        'cultural imagination; the Christian recovery of beauty as a category is part of the recovery of '
        'whole-Christian living.</p>'
    ),
    'christ': (
        '<p>The Anointed One &mdash; Prophet, Priest, and King &mdash; promised throughout the Old Testament '
        'and revealed in the New as Jesus of Nazareth. Greek <em>Christos</em> translates Hebrew <em>Mashiach</em>, '
        'both meaning <em>the anointed</em>. Andrew\'s announcement to Peter: <em>We have found the Messias, '
        'which is, being interpreted, the Christ</em> (John 1:41). The Gospel of John\'s stated purpose: '
        '<em>but these are written, that ye might believe that Jesus is the Christ, the Son of God; and '
        'that believing ye might have life through his name</em> (John 20:31). Christ\'s threefold office '
        'fulfills three OT anointings: prophet (speaking God\'s word to men), priest (offering once-for-all '
        'sacrifice and now interceding at the Father\'s right hand), and king (reigning over the kingdom '
        'that will fill the earth). Every OT messianic prophecy &mdash; Isaiah 7:14, 9:6, 53; Psalm 2, 22, '
        '110; Daniel 7; Zechariah 9:9 &mdash; converges on the carpenter from Nazareth, who is the Word '
        'made flesh (John 1:14), the only mediator between God and men (1 Tim 2:5), and the name above '
        'every name (Phil 2:9-11).</p>'
    ),
    'doctrines-of-grace': (
        '<p>The Reformed cluster of five doctrines confessing the sovereignty of God in salvation, '
        'systematized at the Synod of Dort (1618-1619) in response to the Remonstrant (Arminian) party. '
        'Often arranged in the acronym TULIP: <em>Total depravity</em> (since the fall, every faculty of '
        'man is corrupted by sin; he is unable to seek God or choose Christ apart from grace), <em>Unconditional '
        'election</em> (God chose His people from eternity not because of foreseen faith or works but '
        'according to His sovereign good pleasure, Eph 1:4-5), <em>Limited atonement</em> (Christ\'s death '
        'effectually purchased salvation for the elect, not merely making it possible for all if they '
        'choose), <em>Irresistible grace</em> (the Spirit\'s effectual call infallibly draws the elect to '
        'Christ, John 6:37, 44), and <em>Perseverance of the saints</em> (those whom God has effectually '
        'called and justified He will also glorify, Rom 8:30). Together they confess that salvation from '
        'first to last is the work of God, with man\'s response (real and necessary) the fruit of God\'s '
        'prior gracious initiative. Often summarized as <em>sovereign-grace soteriology</em>.</p>'
    ),
    'dove-harmless': (
        '<p>The disposition of pure motive and gentle bearing Christ pairs with serpent-wisdom in His '
        'commissioning of the Twelve: <em>Behold, I send you forth as sheep in the midst of wolves: be ye '
        'therefore wise as serpents, and harmless as doves</em> (Matt 10:16). The Greek <em>akeraios</em> '
        '(harmless, pure, unmixed) suggests not naivety but uncompounded singleness of purpose &mdash; the '
        'disciple\'s motives unalloyed with deceit, manipulation, or self-promotion. Philippians 2:15 uses '
        'the same word: <em>that ye may be blameless and harmless, the sons of God, without rebuke, in the '
        'midst of a crooked and perverse nation, among whom ye shine as lights in the world.</em> Paired '
        'with serpent-wisdom, dove-harmlessness is not weakness; it is the inner cleanness that gives the '
        'outer shrewdness its moral force. The disciple is sent into hostile environments (sheep among '
        'wolves); he must read the threat accurately (serpent), but he must remain pure of motive (dove). '
        'Either virtue alone fails. Christ commands both.</p>'
    ),
    'farewell-discourse': (
        '<p>Jesus\' extended upper-room teaching the night before His crucifixion, covering John 13-17 &mdash; '
        'the longest single block of Christ\'s teaching preserved in the Gospels. The discourse unfolds in '
        'four sections. (1) John 13: the foot-washing &mdash; servant-leadership made tangible &mdash; '
        'and the new commandment to love one another as Christ has loved His disciples. (2) Chapters 14-16: '
        'preparation for Christ\'s departure &mdash; the promise of the Father\'s house, the way and the '
        'truth and the life, the True Vine and the abiding disciples, the promise of the Spirit as '
        'Comforter and Spirit of Truth, the warning that the world will hate the disciples as it hated '
        'Him. (3) Chapter 17: the high-priestly prayer &mdash; Christ praying first for Himself, then for '
        'His disciples, then for all who would believe through their word. Together the farewell discourse '
        'is Christ\'s last extended preparation of the eleven for ministry without His visible presence &mdash; '
        'the manual for the church-age the apostles would inaugurate at Pentecost.</p>'
    ),
    'genesis-1': (
        '<p>The opening chapter of Scripture, the foundational creation account. The chapter is structured '
        'around six days of creation followed by a seventh day of rest. Days 1-3 establish realms (light/'
        'darkness; sky/sea; land/vegetation); days 4-6 fill those realms with their inhabitants (sun/moon/'
        'stars; sea-creatures/birds; land-animals/man). The repeated refrain <em>and God saw that it was '
        'good</em> punctuates the chapter; the climactic creation of man in God\'s image (vv. 26-27) is '
        'declared <em>very good</em>. Key theological commitments anchored here: God creates ex nihilo by '
        'His word (Heb 11:3); creation is good (against ancient pagan and modern Gnostic dualisms that '
        'devalue matter); humanity is uniquely image-of-God, both male and female; the cultural mandate of '
        '<em>be fruitful and multiply, and replenish the earth, and subdue it</em> (v. 28) belongs to '
        'all humanity. The chapter\'s interpretation has divided Christian readers (six literal 24-hour '
        'days vs. day-age vs. framework theory vs. analogical days), but the doctrinal core &mdash; God '
        'creating by His sovereign word and declaring His work good &mdash; unites every orthodox position.</p>'
    ),
    'lent-season': (
        '<p>The forty-day Christian season of preparation before Easter, observed by liturgical Christian '
        'traditions (Roman Catholic, Eastern Orthodox, Anglican, Lutheran, some Presbyterian and Reformed) '
        'since at least the fourth century. The forty days commemorate Christ\'s forty days of fasting and '
        'temptation in the wilderness (Matt 4:1-11) and parallel Moses\' forty days on Sinai and Elijah\'s '
        'forty days at Horeb. Lent traditionally begins on Ash Wednesday (a service of penitence marked by '
        'the imposition of ashes on the forehead) and ends at Easter, comprising forty weekday-fasting-days '
        '(Sundays excluded as little-Easters). Observance has historically included fasting, abstaining '
        'from meat, increased prayer, almsgiving, and self-examination &mdash; the disciplines that prepare '
        'the soul to encounter the cross and resurrection afresh. Protestant traditions vary in their '
        'engagement: many Evangelical and Reformed bodies observe Lent in modified form; others reject the '
        'practice as unscriptural accretion. The MOOP Dictionary holds the observance as wise pastoral '
        'tradition, valuable when it leads to actual repentance and renewed devotion rather than to mere '
        'religious performance.</p>'
    ),
    'matthew-13': (
        '<p>Matthew\'s major collection of kingdom parables, seven (or eight, depending on counting) '
        'parables given in succession and clustered around the question of how the kingdom comes and grows. '
        'The chapter is the second of five major teaching discourses in Matthew. Parables included: '
        '(1) the sower (vv. 3-9, 18-23) &mdash; four soils receiving the same seed; (2) the wheat and '
        'tares (vv. 24-30, 36-43) &mdash; good and evil grow together until the harvest; (3) the mustard '
        'seed (vv. 31-32) &mdash; the kingdom\'s small beginning and large outcome; (4) the leaven '
        '(v. 33) &mdash; quiet penetration of the whole; (5) the hidden treasure (v. 44); (6) the pearl '
        'of great price (vv. 45-46) &mdash; both teach the kingdom\'s incomparable worth; (7) the dragnet '
        '(vv. 47-50) &mdash; the final separation. Christ\'s teaching method in this chapter is itself '
        'theologically significant: parables both reveal the kingdom to those granted understanding and '
        'conceal it from those whose hearts are hardened (vv. 10-17, citing Isaiah 6:9-10). The kingdom '
        'arrives in mystery before it arrives in glory.</p>'
    ),
    'midian-place': (
        '<p>The desert region east of the Gulf of Aqaba on the Arabian peninsula, named for Midian son of '
        'Abraham by Keturah (Gen 25:1-2). Midian becomes Moses\' refuge after he killed the Egyptian and '
        'fled Pharaoh\'s court (Ex 2:15). At a well in Midian he met Reuel/Jethro and married his daughter '
        'Zipporah, beginning the forty years of wilderness shepherding that prepared him for the burning '
        'bush and the exodus. Jethro himself became a wise counselor to Moses, suggesting the administrative '
        'structure of Israel\'s leadership (Ex 18). The Midianites later turn hostile: they seduce Israel '
        'into idolatry at Baal-Peor (Num 25) through the counsel of Balaam, leading to a war of judgment '
        '(Num 31). In the period of the judges, Midianite raiders oppressed Israel for seven years until '
        'Gideon delivered them with three hundred men by the LORD\'s hand (Judg 6-8). Midian therefore '
        'plays a dual biblical role: refuge in one generation, oppressor in another, redemption-instructor '
        '(Jethro) and idolatry-tempter (Balaam) sequentially.</p>'
    ),
    'nineveh-city': (
        '<p>The capital of the Neo-Assyrian Empire, on the eastern bank of the Tigris River opposite '
        'modern Mosul, Iraq. Nineveh was one of the largest cities of the ancient world &mdash; '
        '<em>an exceeding great city of three days\' journey</em> (Jonah 3:3) &mdash; and the seat of '
        'the most violent imperial power of its era, infamous for the cruelty of its military campaigns. '
        'Jonah was commissioned by God to preach against Nineveh\'s wickedness (Jonah 1:2), fled west by '
        'sea to Tarshish, was returned to Nineveh by the great fish, and saw the city repent from king '
        'down to commoner under his eight-word sermon (Jonah 3). The repentance staved off judgment for '
        'a generation. A century or so later, Nahum prophesied Nineveh\'s coming destruction, fulfilled '
        'when the Medes and Babylonians sacked the city in 612 BC, leaving it so thoroughly destroyed that '
        'within centuries its very location was disputed. Christ Himself cited the Ninevites who repented '
        'at Jonah\'s preaching as a witness against His own generation (Matt 12:41).</p>'
    ),
    'retreat': (
        '<p>The spiritual discipline of withdrawing from crowds, screens, and noise into deliberate '
        'solitude with God. Christ Himself practiced retreat as a regular pattern between seasons of '
        'ministry: <em>And in the morning, rising up a great while before day, he went out, and departed '
        'into a solitary place, and there prayed</em> (Mark 1:35); <em>he withdrew himself into the '
        'wilderness, and prayed</em> (Luke 5:16); <em>And it came to pass in those days, that he went out '
        'into a mountain to pray, and continued all night in prayer to God</em> (Luke 6:12). After the '
        'feeding of the five thousand, He sent the disciples away and went up into a mountain alone to '
        'pray (Matt 14:23). The pattern of withdrawal-for-prayer-then-return-to-ministry runs through the '
        'entire Gospel record. Retreat is not escapism; it is the necessary recharging of soul and mind '
        'that makes return-to-ministry sustainable. The man who never retreats inevitably hardens, dries '
        'up, or breaks. The man who learns the rhythm Christ kept lasts.</p>'
    ),
    'undershepherd': (
        '<p>The pastor or elder serving under Christ as Chief Shepherd, accountable to Him for the flock '
        'entrusted to his care. Peter\'s charge in 1 Peter 5:1-4 is the locus classicus: <em>The elders '
        'which are among you I exhort... Feed the flock of God which is among you, taking the oversight '
        'thereof... Neither as being lords over God\'s heritage, but being ensamples to the flock. And '
        'when the chief Shepherd shall appear, ye shall receive a crown of glory that fadeth not away.</em> '
        'The Greek <em>archipoimen</em> (Chief Shepherd) makes the human elder\'s role explicit by '
        'contrast: he is <em>under-shepherd</em>, not the Owner, not the Christ, not the Lord. The '
        'undershepherd\'s authority is real but derivative; he holds a stewardship that will be audited '
        'when the Chief Shepherd returns. Hebrews 13:17 reinforces: <em>Obey them that have the rule over '
        'you... for they watch for your souls, as they that must give account.</em> The doctrine grounds '
        'both the pastor\'s legitimate authority (he speaks for the Owner) and his accountability (he is '
        'not the Owner). Every faithful undershepherd serves the Chief Shepherd\'s flock and answers to '
        'the Chief Shepherd\'s standard.</p>'
    ),
    'vagabond': (
        '<p>A wanderer without settled home, in Scripture nearly always a negative category indicating '
        'either divine curse or unsettled spiritual disposition. God\'s curse on Cain after the murder of '
        'Abel: <em>When thou tillest the ground, it shall not henceforth yield unto thee her strength; a '
        'fugitive and a vagabond shalt thou be in the earth</em> (Gen 4:12). Cain\'s response named the '
        'punishment\'s severity: <em>my punishment is greater than I can bear... I shall be a fugitive and '
        'a vagabond in the earth; and it shall come to pass, that every one that findeth me shall slay '
        'me</em> (v. 14). The unsettled wandering is itself the curse-feature: rooted residence is part of '
        'God\'s blessing on humanity (the cultural mandate of Gen 1:28 requires sustained occupation of '
        'place). Acts 19:13 names another negative case: <em>certain of the vagabond Jews, exorcists</em> &mdash; '
        'unsettled itinerant exorcists who tried to use the name of Jesus and were overcome by the demon. '
        'The biblical disposition toward place is rootedness, stability, and household-built-over-generations. '
        'Vagabond is the loss of that good.</p>'
    ),
    'yoke-fellow': (
        '<p>A fellow-laborer joined under the same yoke of ministry. Paul\'s affectionate term in '
        'Philippians 4:3: <em>And I intreat thee also, true yokefellow, help those women which laboured '
        'with me in the gospel, with Clement also, and with other my fellowlabourers, whose names are in '
        'the book of life.</em> The Greek <em>syzygos</em> (yoked-together) draws on the agricultural '
        'image of two oxen sharing one yoke, pulling the same load in the same direction at the same '
        'pace. Some commentators take <em>syzygos</em> as a proper name (Syzygus) rather than a common '
        'noun; the consensus reading takes it as common noun. The image is rich: ministry yokemates are '
        'matched in pace, share the load, pull in the same direction, and cannot break apart without one '
        'or both falling. The Christian ministry is a yoked enterprise; the lone-wolf model is foreign to '
        'the apostolic pattern. The minister or missionary or pastor who tries to pull alone wears himself '
        'out faster than the work warrants; the yoked-fellowship of ministry sustains both partners through '
        'the long obedience.</p>'
    ),
    '1thessalonians': (
        '<p>Paul\'s first epistle to the church at Thessalonica, written from Corinth around AD 50-51 '
        'shortly after the Macedonian missionary journey (Acts 17:1-9). Among the earliest of Paul\'s '
        'letters. The Thessalonian church had been planted briefly (probably three Sabbaths of preaching '
        'plus subsequent informal work) before Paul was forced out by hostile mob. He wrote to a young '
        'church facing persecution, encouraging their faith, addressing concerns about deceased fellow-'
        'Christians, and unveiling the doctrine of Christ\'s return. The five chapters cover: (1) the '
        'apostolic testimony of the Thessalonians\' reception of the gospel; (2) Paul\'s pastoral heart '
        'and his missionary co-laborers; (3) Timothy\'s recent return with news from the church; (4) '
        'living-faithfully instructions including the famous passage on Christ\'s return and the dead in '
        'Christ rising first (4:13-18 &mdash; the canonical NT passage on the rapture / resurrection); '
        '(5) further exhortations including <em>pray without ceasing</em> (5:17), <em>in everything give '
        'thanks</em> (5:18), and <em>quench not the Spirit</em> (5:19).</p>'
    ),
    'active-obedience': (
        '<p>Christ\'s perfect, lifelong obedience to the entire law of God on behalf of His people &mdash; '
        'imputed to them as their righteousness. Distinguished theologically from Christ\'s <em>passive '
        'obedience</em> (His suffering and death paying the law\'s penalty). The classic Reformed '
        'formulation: Christ\'s active obedience earns the righteousness that is reckoned to the believer; '
        'His passive obedience pays the penalty due for the believer\'s sins. Both are essential; together '
        'they make the gospel possible. Romans 5:19 names both: <em>For as by one man\'s disobedience '
        'many were made sinners, so by the obedience of one shall many be made righteous.</em> Philippians '
        '2:8 captures the trajectory: <em>he humbled himself, and became obedient unto death, even the '
        'death of the cross</em> &mdash; the obedience extends from incarnation through cross. Christ\'s '
        'sinless life, His perfect fulfillment of the Sermon-on-the-Mount-level law, His positive love of '
        'God and neighbor, His mediatorial faithfulness &mdash; all are imputed to the believer. The '
        'Christian stands before God not just with sin removed (passive obedience) but with positive '
        'righteousness reckoned (active obedience).</p>'
    ),
    'children': (
        '<p>A heritage from the Lord, image-bearers entrusted to parents for nurture in the discipline '
        'and instruction of the Lord. Psalm 127:3-5 grounds the doctrine: <em>Lo, children are an heritage '
        'of the LORD: and the fruit of the womb is his reward. As arrows are in the hand of a mighty man; '
        'so are children of the youth. Happy is the man that hath his quiver full of them.</em> Ephesians '
        '6:4 names the parental responsibility: <em>And, ye fathers, provoke not your children to wrath: '
        'but bring them up in the nurture and admonition of the Lord.</em> Proverbs is full of fatherly '
        'instruction to a son. Christ\'s tenderness toward children (Mark 10:13-16: <em>suffer the little '
        'children to come unto me, and forbid them not: for of such is the kingdom of God</em>) sets the '
        'standard against which both ancient Roman child-exposure and modern Western child-as-lifestyle-'
        'choice are alike judged. The biblical doctrine of children is foundational to both the cultural '
        'mandate (be fruitful and multiply, Gen 1:28) and the gospel-discipleship pattern of generational '
        'covenant. Children are not a project, an interruption, or a category to be optimized; they are '
        'arrows for a quiver, image-bearers for the kingdom.</p>'
    ),
    'classical-theism': (
        '<p>The historic Christian doctrine of God, articulated across the fathers, medieval scholastics, '
        'and Reformation orthodox, holding that God is simple (without parts), eternal (not bound by time), '
        'immutable (does not change), impassible (not moved by external causes), omnipotent (all-powerful), '
        'omniscient (all-knowing), omnipresent (everywhere present), aseity (self-existent, self-sufficient), '
        'and perfect (lacking nothing). Distinguished from modern theological revisions that compromise '
        'one or more of these attributes: process theology (denying immutability and impassibility), '
        'open theism (denying exhaustive divine foreknowledge), pantheism (collapsing God into creation), '
        'panentheism (folding creation into God), and various neo-classical positions that retain some '
        'attributes while abandoning others. The classical attributes are not philosophical impositions '
        'on Scripture but are derived from Scripture\'s own portrayal of God: Mal 3:6 (<em>I am the LORD, '
        'I change not</em>); Ps 90:2 (<em>from everlasting to everlasting, thou art God</em>); Acts 17:28 '
        '(<em>in him we live, and move, and have our being</em>); 1 Tim 6:16 (<em>who only hath '
        'immortality, dwelling in the light which no man can approach unto</em>). The doctrine grounds the '
        'reliability of God\'s promises, the trustworthiness of His character, and the foundation of all '
        'creaturely worship.</p>'
    ),
    'heart-bold': (
        '<p>A bold heart speaks the gospel without shrinking. The Greek <em>parresia</em> (boldness, '
        'frankness, plain-speech) names both the disposition and the outward speech that flows from it. '
        'Acts 4:13 captures the apostolic example: <em>Now when they saw the boldness of Peter and John, '
        'and perceived that they were unlearned and ignorant men, they marvelled; and they took knowledge '
        'of them, that they had been with Jesus.</em> The Sanhedrin\'s reaction is the diagnostic: '
        'bold-hearted speech reveals time spent with Christ. The disciples\' prayer in Acts 4:29-31 asks '
        'for more: <em>grant unto thy servants, that with all boldness they may speak thy word</em>, and '
        'the Spirit answers by filling them and granting it. Paul\'s ministry is repeatedly framed as '
        'bold-hearted (Acts 9:27-28; 13:46; 14:3; 19:8; 28:31). Hebrews 4:16 extends the same boldness to '
        'every believer\'s access to the throne of grace. Ephesians 6:19-20 makes it the chief request '
        'Paul asks the Ephesians to pray for him. Bold heart is not personality; it is the Spirit\'s '
        'gift to the believer who has been with Jesus, asks for it, and steps out to speak.</p>'
    ),
    'indwelling': (
        '<p>The personal residence of the Holy Spirit in every believer at conversion. The doctrine '
        'distinguishes Christian experience from every prior dispensation: where the OT Spirit came upon '
        'specific persons for specific tasks (judges, prophets, kings), the NT Spirit indwells every '
        'believer permanently. Romans 8:9-11: <em>But ye are not in the flesh, but in the Spirit, if so '
        'be that the Spirit of God dwell in you. Now if any man have not the Spirit of Christ, he is none '
        'of his.</em> 1 Corinthians 6:19: <em>What? know ye not that your body is the temple of the Holy '
        'Ghost which is in you, which ye have of God, and ye are not your own?</em> Christ\'s promise '
        'in John 14:16-17 establishes the doctrine: the Spirit who has been with the disciples will be '
        '<em>in</em> them. The indwelling Spirit seals the believer for the day of redemption (Eph 1:13-14; '
        '4:30), produces fruit (Gal 5:22-23), gives gifts for the building up of the body (1 Cor 12), '
        'illuminates Scripture (1 Cor 2:12-14), convicts of sin and assures of sonship (Rom 8:15-16). '
        'There are no Spirit-less Christians and no second-class Christians who lack the Spirit.</p>'
    ),
    'lowliness-biblical': (
        '<p>The mind that takes a low place. Greek <em>tapeinophrosune</em> (lowly-mindedness, humility) '
        'is one of the marks of the Christ-conformed disciple. Philippians 2:3-8 names both the disposition '
        'and its ultimate exemplar: <em>Let nothing be done through strife or vainglory; but in lowliness '
        'of mind let each esteem other better than themselves... Let this mind be in you, which was also '
        'in Christ Jesus: Who, being in the form of God, thought it not robbery to be equal with God: But '
        'made himself of no reputation, and took upon him the form of a servant, and was made in the '
        'likeness of men: And being found in fashion as a man, he humbled himself, and became obedient '
        'unto death, even the death of the cross.</em> Christ\'s pattern is the standard: a willing '
        'descent from the highest possible position to the lowest, taking on servant-form for the sake of '
        'others. The biblical man\'s lowliness is not low self-esteem (modern therapy-category) but '
        'cultivated mind-position &mdash; the deliberate choice to esteem others above oneself, to refuse '
        'self-promotion, to take the form of a servant. Lowliness is the mark of Christian leadership; '
        'self-exaltation is the mark of its counterfeit.</p>'
    ),
    'maranatha': (
        '<p>The Aramaic plea <em>Our Lord, come</em> (or, parsed differently, <em>Our Lord has come</em>), '
        'preserved untranslated by Paul in 1 Corinthians 16:22 to retain the heartbeat of the early '
        'persecuted Aramaic-speaking church. <em>And if any man love not the Lord Jesus Christ, let him be '
        'Anathema. Maran-atha.</em> The word\'s preservation in Aramaic alongside Greek <em>anathema</em> '
        '(let him be cursed) is theologically loaded: the church\'s anticipatory cry of <em>Lord, come</em> '
        'stands directly against any merely-cultural Christian affiliation that does not love the Lord '
        'Jesus. The Didache (an early second-century church manual) ends its eucharistic prayer with the '
        'same word, suggesting it was used liturgically in the earliest Christian gatherings. Revelation '
        '22:20 closes the entire biblical canon with the Greek equivalent: <em>even so, come, Lord Jesus.</em> '
        'The Christian who has tasted enough of this age to know its insufficiency joins the church across '
        'twenty centuries in the same prayer the first generation prayed: <em>Maranatha &mdash; our Lord, '
        'come.</em></p>'
    ),
    'exorcism': (
        '<p>The casting-out of demons by the authority of Jesus Christ. The Greek <em>ekballo daimonia</em> '
        '(to cast out demons) appears throughout the Synoptic Gospels and Acts. Christ\'s ministry of '
        'exorcism is one of the signal evidences of the in-breaking kingdom: <em>But if I cast out devils '
        'by the Spirit of God, then the kingdom of God is come unto you</em> (Matt 12:28). Christ '
        'authorized the Twelve and the Seventy to cast out demons in His name (Matt 10:1, 8; Luke 10:17). '
        'The early church continued the ministry: Philip in Samaria (Acts 8:7), Paul at Philippi with the '
        'Pythian-spirited slave girl (Acts 16:16-18), Paul at Ephesus (Acts 19:11-12). The seven sons of '
        'Sceva attempting exorcism in Jesus\' name without Spirit-empowerment provide the canonical '
        'cautionary tale (Acts 19:13-17): <em>Jesus I know, and Paul I know; but who are ye?</em> Christian '
        'exorcism is real, biblical, and effective &mdash; though distinct from sensationalist treatments. '
        'It rests on the authority of Christ over every spiritual power and is exercised only by those '
        'who walk in His authority. The MOOP Dictionary affirms the historic Christian practice without '
        'either skeptical denial or sensational excess.</p>'
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
