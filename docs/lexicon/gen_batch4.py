#!/usr/bin/env python3
"""Lexicon Batch 4 — 50 new pages, self-contained."""
import os, html

OUT = "/Users/adamjohns/bible-reading-plan-bot/docs/lexicon"

WORDS = [
    # (strongs, lang, testament, original, translit, pos, gloss,
    #  definition, usage, verses[(ref,text)], word_study, related[(id,label)], blb_id)
    ("H6086","Hebrew","Old Testament","עֵץ","etz","Noun, masculine","tree, wood, timber",
     "The common word for any woody plant — from orchard trees to lumber for building. Used of the Tree of Life and the Tree of Knowledge in Genesis, and prophetically of the cross (Deut 21:23; Gal 3:13).",
     "Spans forest trees, fruit trees, and construction timber. The phrase 'hung on a tree' carried covenantal curse (Deut 21:23), which Paul applies to Christ's crucifixion as redemptive substitution.",
     [("Genesis 2:9","Out of the ground the LORD God made to spring up every <em>tree</em> [etz] pleasant to the sight and good for food."),
      ("Deuteronomy 21:23","A hanged man is cursed by God — he who is hung on a <em>tree</em> [etz]."),
      ("Psalm 1:3","He is like a <em>tree</em> planted by streams of water that yields its fruit in its season.")],
     "The symbolic weight of <em>etz</em> runs from Eden's trees of life and death through Calvary's wooden cross. Paul's citation in Galatians 3:13 makes the curse of the tree the pivot of substitutionary atonement.",
     [("G3586","G3586 — xylon (wood/tree)"),("H2416","H2416 — chay (life)")],
     "h6086"),

    ("H6105","Hebrew","Old Testament","עָצַם","atsam","Verb","to be strong, mighty, numerous",
     "Means both physical strength/power and numerical greatness. Israel's growth in Egypt is described with this word (Exod 1:20). God's thoughts are declared more numerous than sand (Ps 139:18).",
     "Used of mighty nations, powerful rulers, and God's overwhelming greatness. The noun <em>etsem</em> (bone) shares this root — bones representing inner strength.",
     [("Exodus 1:20","The people multiplied and grew very <em>strong</em> [atsam]."),
      ("Psalm 139:17-18","Your thoughts, O God — how <em>vast</em> [atsam] is the sum of them! More than sand they are."),
      ("Micah 4:3","He shall rebuke <em>strong</em> nations far away.")],
     "The dual meaning — strong AND many — reflects ancient thought that power and number were linked. A mighty God is also an infinite God.",
     [("H1368","H1368 — gibbor (mighty warrior)"),("H3581","H3581 — koach (strength)")],
     "h6105"),

    ("H6160","Hebrew","Old Testament","עֲרָבָה","arabah","Noun, feminine","desert plain, steppe, Arabah",
     "The desolate rift valley stretching from the Sea of Galilee to the Gulf of Aqaba, but also any dry, barren steppe. Isaiah's prophecy promises the <em>arabah</em> will rejoice and blossom (Isa 35:1).",
     "Used both geographically (the Jordan Valley/Arabah) and as a symbol of desolation awaiting redemption. Isaiah 40:3 — 'make straight in the <em>desert</em> a highway' — is fulfilled in John the Baptist.",
     [("Isaiah 35:1","The wilderness and the <em>dry land</em> [arabah] shall be glad; the desert shall rejoice and blossom."),
      ("Isaiah 40:3","Make straight in the <em>desert</em> [arabah] a highway for our God."),
      ("Deuteronomy 1:1","Moses spoke to Israel in the <em>Arabah</em> opposite Suph.")],
     "The Arabah was real geography — Israel's 40-year home — but became a theological symbol. What was barren becomes fruitful; what was empty becomes a highway for God.",
     [("H4057","H4057 — midbar (wilderness)"),("H3068","H3068 — YHWH")],
     "h6160"),

    ("H6258","Hebrew","Old Testament","עַתָּה","attah","Adverb","now, at this time, therefore",
     "The Hebrew word for the present moment, often marking a decisive turning point in narrative. Frequently introduces a divine command or human response: 'And <em>now</em> therefore...'",
     "Signals that something consequential is happening. In covenantal speeches, <em>attah</em> marks the move from recounting God's past acts to present obligation (Josh 24:14).",
     [("Joshua 24:14","<em>Now</em> therefore fear the LORD and serve him in sincerity and faithfulness."),
      ("Genesis 3:22","And <em>now</em>, lest he reach out his hand and take also of the tree of life..."),
      ("Exodus 19:5","<em>Now</em> therefore, if you will indeed obey my voice and keep my covenant...")],
     "Hebrew narrative uses <em>attah</em> to create urgency — this moment is the hinge between past revelation and present decision. Many covenant appeals pivot on this word.",
     [("H3117","H3117 — yom (day)"),("H6440","H6440 — panim (face/presence)")],
     "h6258"),

    ("H6437","Hebrew","Old Testament","פָּנָה","panah","Verb","to turn, face toward, look",
     "To physically or spiritually turn toward or away from something. Turning toward God is repentance and attention; turning away is apostasy. The same root gives <em>panim</em> (face).",
     "The call to 'turn' runs throughout prophetic literature as a plea for repentance. When Israel turned their faces from God, they pursued idols; turning back was restoration.",
     [("Isaiah 45:22","<em>Turn</em> to me and be saved, all the ends of the earth!"),
      ("Lamentations 1:8","She herself groaned and <em>turned</em> her face away."),
      ("Numbers 16:42","When the congregation <em>turned</em> toward the tent of meeting...")],
     "Closely related to <em>panim</em> (H6440, face), this verb captures the directional nature of relationship — you face what you value. Divine 'turning toward' Israel signals mercy; their turning away signals rebellion.",
     [("H6440","H6440 — panim (face)"),("H7725","H7725 — shuv (to return/repent)")],
     "h6437"),

    ("H6629","Hebrew","Old Testament","צֹאן","tson","Noun, collective","flock, sheep and goats",
     "The collective noun for small livestock — sheep and goats together. Israel was a pastoral culture; flocks represented wealth, sacrifice, and food. God himself is the Shepherd of his flock.",
     "The shepherd/flock metaphor is central to Scripture. Israel is God's flock (Ps 100:3), kings are shepherds of the people, and Messiah is the Good Shepherd. The flock needed both provision and protection.",
     [("Psalm 100:3","We are his people and the <em>sheep</em> [tson] of his pasture."),
      ("Ezekiel 34:31","You are my <em>sheep</em>, human sheep of my pasture, and I am your God."),
      ("Genesis 4:2","Abel was a keeper of <em>sheep</em> [tson], and Cain a worker of the ground.")],
     "The flock image unifies sacrifice (unblemished lambs), wealth (Abraham's flocks), and metaphor (Israel as God's sheep). Jesus as the Good Shepherd (John 10) draws on this deep well.",
     [("H7462","H7462 — raah (to shepherd)"),("G4168","G4168 — poimnē (flock)")],
     "h6629"),

    ("H6754","Hebrew","Old Testament","צֶלֶם","tselem","Noun, masculine","image, likeness, representation",
     "An image or representation of something. Most famously, humanity is created in God's <em>tselem</em> (Gen 1:26-27), making humans his image-bearers and vice-regents over creation.",
     "Used of idols (carved images) and of the divine image in humanity. The two uses create a sharp contrast: humanity is the legitimate image of God, while carved idols are counterfeits. Image-bearing means representing God's rule.",
     [("Genesis 1:26","Let us make man in our <em>image</em> [tselem], after our likeness."),
      ("Genesis 9:6","Whoever sheds the blood of man — for God made man in his <em>image</em> [tselem]."),
      ("Psalm 39:6","Surely a man goes about as a <em>shadow</em> [tselem].")],
     "The <em>imago Dei</em> (image of God) is the theological foundation of human dignity. NT connects this to Christ as the perfect image of God (Col 1:15), and believers being renewed in that image (Col 3:10).",
     [("H1823","H1823 — demuth (likeness)"),("G1504","G1504 — eikon (image)")],
     "h6754"),

    ("H6780","Hebrew","Old Testament","צֶמַח","tsemach","Noun, masculine","sprout, branch, growth",
     "A sprouting or growth from the ground. Prophetically, 'the Branch' (tsemach) is a key messianic title — the shoot from David's line who would reign in righteousness (Jer 23:5; Zech 3:8; 6:12).",
     "The messianic 'Branch' passages are among the OT's clearest prophecies. Zechariah 6:12-13 depicts 'the man whose name is Branch' who will build the temple and rule — fulfilled in Jesus.",
     [("Jeremiah 23:5","I will raise up for David a righteous <em>Branch</em> [tsemach], and he shall reign as king."),
      ("Zechariah 3:8","I will bring my servant the <em>Branch</em>."),
      ("Zechariah 6:12","Behold, the man whose name is the <em>Branch</em> — he shall branch out from his place and build the temple of the LORD.")],
     "Four 'Branch' prophecies (Isa 4:2; Jer 23:5; Zech 3:8; 6:12) each highlight a different aspect of Messiah — Branch of the LORD, righteous Branch, Servant Branch, Builder Branch.",
     [("H8057","H8057 — simchah (joy)"),("G4491","G4491 — rhiza (root)")],
     "h6780"),

    ("H6862","Hebrew","Old Testament","צַר","tsar","Noun/Adjective","adversary, distress, narrow",
     "Both a noun for an enemy/adversary and an adjective meaning 'narrow, tight, distressed.' Distress is literally being in a 'tight spot.' Psalms of lament frequently cry out from <em>tsar</em>.",
     "The Psalms use <em>tsar</em> constantly for enemies and personal distress. The call 'from the narrow place I cried to the LORD' (Ps 118:5) uses this root. God saves from the <em>tsar</em>.",
     [("Psalm 118:5","Out of my <em>distress</em> [tsar] I called on the LORD; the LORD answered me and set me free."),
      ("Numbers 10:9","When you go to war in your land against the <em>adversary</em> [tsar] who oppresses you..."),
      ("Psalm 31:9","Be gracious to me, O LORD, for I am in <em>distress</em> [tsar].")],
     "The tightness/narrowness of <em>tsar</em> creates a spatial metaphor for trouble — you're hemmed in with no room to move. God's salvation is spaciousness (Ps 18:19: 'he brought me out into a broad place').",
     [("H6869","H6869 — tsarah (trouble/distress)"),("H7965","H7965 — shalom (peace)")],
     "h6862"),

    ("H6908","Hebrew","Old Testament","קָבַץ","qabats","Verb","to gather, collect, assemble",
     "To gather together — people, grain, or nations. Used of Israel's exile-and-return theology: God scattered his people and will gather them again. Eschatological gathering is a major prophetic theme.",
     "The ingathering of Israel is one of prophecy's great themes. God who scattered (H6327 puts) will gather (<em>qabats</em>). This finds partial fulfillment in the return from Babylon and ultimate fulfillment in the messianic age.",
     [("Isaiah 43:5","I will bring your offspring from the east, and from the west I will <em>gather</em> [qabats] you."),
      ("Ezekiel 36:24","I will take you from the nations and <em>gather</em> [qabats] you from all the countries."),
      ("Psalm 106:47","<em>Gather</em> [qabats] us from among the nations, that we may give thanks to your holy name.")],
     "Paired with H6327 (puts — to scatter), the scatter/gather dynamic describes Israel's covenant history. NT applies the gathering motif to the church (John 11:52: 'gather into one the children of God').",
     [("H6327","H6327 — puts (to scatter)"),("H5712","H5712 — edah (congregation)")],
     "h6908"),

    ("H6950","Hebrew","Old Testament","קָהַל","qahal","Verb","to assemble, gather together",
     "To convoke or assemble a community for a specific purpose — war, worship, covenant-making, or judgment. The noun <em>qahal</em> (congregation/assembly) is the OT background for the NT word <em>ekklesia</em> (church).",
     "Israel's assembly before God at Sinai and in the temple courts was <em>qahal</em>. The Greek translators rendered it as <em>ekklesia</em>, which became the NT word for 'church' — the called-out assembly.",
     [("Exodus 35:1","Moses <em>assembled</em> [qahal] all the congregation of the people of Israel."),
      ("1 Kings 8:1","Solomon <em>assembled</em> [qahal] the elders of Israel at Jerusalem."),
      ("Psalm 22:22","In the midst of the <em>congregation</em> [qahal] I will praise you.")],
     "The OT qahal is the direct ancestor of the NT ekklesia (church). Both describe the people of God formally assembled before him — Israel at Sinai is the type; the church is the antitype.",
     [("H5712","H5712 — edah (assembly)"),("G1577","G1577 — ekklesia (church)")],
     "h6950"),

    ("H7043","Hebrew","Old Testament","קָלַל","qalal","Verb","to be light, swift, curse, treat with contempt",
     "A versatile verb meaning to be light in weight, swift in movement, or trivial in value — and by extension to curse or treat someone as worthless. Contrasts with <em>kabed</em> (heavy/honor).",
     "The honor/shame axis of Hebrew culture runs through <em>qalal</em>. To curse (qalal) is to declare someone light — without worth. God's prohibition of cursing parents (Exod 21:17) uses this word.",
     [("Genesis 8:11","The waters had <em>abated</em> [qalal] from the face of the ground."),
      ("Exodus 21:17","Whoever <em>curses</em> [qalal] his father or his mother shall be put to death."),
      ("2 Samuel 16:5","Shimei was cursing [qalal] and throwing stones at David.")],
     "The curse/honor dynamic is central to covenant theology. To 'curse' Abraham's enemies (Gen 12:3) uses a different root (arar), but qalal captures the social dimension — treating as contemptible.",
     [("H3513","H3513 — kabed (to honor/be heavy)"),("H779","H779 — arar (to curse)")],
     "h7043"),

    ("H7110","Hebrew","Old Testament","קֶצֶף","qetseph","Noun, masculine","wrath, anger, indignation",
     "Divine or human anger, especially the fierce wrath of God against covenant violation. Closely associated with the consequences of idolatry. Israel's sin repeatedly provoked God's <em>qetseph</em>.",
     "Used primarily of God's anger against Israel's idolatry and unfaithfulness. The word carries the sense of fury that bursts out — not simmering but explosive. Prophets warn of impending <em>qetseph</em>.",
     [("Deuteronomy 29:28","The LORD uprooted them from their land in <em>anger</em> [qetseph] and fury."),
      ("Zechariah 1:2","The LORD was very <em>angry</em> [qetseph] with your fathers."),
      ("Isaiah 54:8","In overflowing <em>wrath</em> [qetseph] for a moment I hid my face from you.")],
     "Divine wrath in the OT is always covenantal — it rises from love betrayed and holiness violated. Isaiah 54:8 pairs the moment of wrath with eternal lovingkindness, showing God's anger is subordinate to his mercy.",
     [("H639","H639 — aph (anger/nose)"),("H2534","H2534 — chemah (wrath/heat)")],
     "h7110"),

    ("H7114","Hebrew","Old Testament","קָצַר","qatsar","Verb","to harvest, reap, be short",
     "To cut short — whether crops at harvest or days of life. The harvest image permeates both agricultural law (leave gleanings for the poor) and eschatological judgment ('the harvest is ripe').",
     "Israel's agricultural calendar centered on harvest. The laws of gleaning (Lev 19:9-10) showed that <em>qatsar</em> was not purely economic but ethical. NT harvest imagery (Matt 13, Rev 14) builds on this.",
     [("Leviticus 19:9","When you <em>reap</em> [qatsar] the harvest of your land, you shall not reap to the very edges."),
      ("Ruth 2:3","She came and gleaned in the field after the <em>reapers</em> [qatsar]."),
      ("Hosea 8:7","They sow the wind, and they shall <em>reap</em> [qatsar] the whirlwind.")],
     "The harvest as divine judgment is developed through Hosea and Joel into a major eschatological image. Jesus' parables of the harvest (tares, dragnet) and Revelation 14's harvest angel all echo <em>qatsar</em>.",
     [("H1715","H1715 — dagan (grain)"),("G2326","G2326 — therismos (harvest)")],
     "h7114"),

    ("H7161","Hebrew","Old Testament","קֶרֶן","qeren","Noun, feminine","horn, ray of light, strength",
     "Literally an animal horn; symbolically, power and glory. God 'exalts the horn' of his anointed (1 Sam 2:10). Moses' face 'shone' (qaran from same root) after meeting God (Exod 34:29).",
     "Horns on the altar were sacred (sanctuary for those who grabbed them). Lifting or breaking someone's horn meant rising or falling power. Daniel's horns in apocalyptic represent successive empires.",
     [("1 Samuel 2:10","He will exalt the <em>horn</em> [qeren] of his anointed."),
      ("Psalm 75:4-5","Do not lift up your <em>horn</em> [qeren]; do not speak with haughty neck."),
      ("Luke 1:69","He has raised up a <em>horn</em> of salvation for us in the house of his servant David.")],
     "Luke 1:69 ('horn of salvation') directly echoes the OT horn idiom. The 'horn of David's house' is Messiah — the one whose power God has exalted. Horn symbolism in Revelation (the Lamb with seven horns) draws on this tradition.",
     [("H2416","H2416 — chay (life)"),("H4428","H4428 — melek (king)")],
     "h7161"),

    ("H7235","Hebrew","Old Testament","רָבָה","rabah","Verb","to be many, multiply, increase",
     "The verb of multiplication and abundance. God's first commands involve <em>rabah</em>: 'Be fruitful and multiply' (Gen 1:28). The fulfillment of covenant blessing is measured by increase.",
     "Used of population growth, animal reproduction, and the increase of wisdom or sin. The Abrahamic promise of descendants 'as numerous as stars' uses this root's imagery throughout Genesis.",
     [("Genesis 1:28","Be fruitful and <em>multiply</em> [rabah] and fill the earth."),
      ("Genesis 22:17","I will surely multiply [rabah] your offspring as the stars of heaven."),
      ("Proverbs 9:11","By wisdom your days will be <em>multiplied</em> [rabah].")],
     "The multiplication command (Gen 1:28) is a commission — humanity as image-bearers filling and governing creation. Covenant blessing is often quantified as increase: more children, more land, more years.",
     [("H6509","H6509 — parah (to be fruitful)"),("H1254","H1254 — bara (to create)")],
     "h7235"),

    ("H7272","Hebrew","Old Testament","רֶגֶל","regel","Noun, feminine","foot, step, journey",
     "The foot as the organ of travel and as a metaphor for life's path. Washing feet was hospitality; putting feet on enemies' necks was victory. God guides the <em>regel</em> of the righteous.",
     "Feet represent direction and allegiance — you go where you place your feet. The Psalms and Proverbs use <em>regel</em> to picture moral choices as paths and the godly life as sure-footed walking.",
     [("Psalm 119:105","Your word is a lamp to my feet [regel] and a light to my path."),
      ("Proverbs 4:26","<em>Ponder</em> the path of your feet [regel]; then all your ways will be sure."),
      ("Isaiah 52:7","How beautiful upon the mountains are the feet [regel] of him who brings good news.")],
     "Isaiah 52:7's beautiful feet of the messenger become Paul's foundation for gospel preaching (Rom 10:15). The foot, as the instrument of going, represents the urgency and beauty of carrying good news.",
     [("H734","H734 — orach (path/way)"),("H1870","H1870 — derek (way/road)")],
     "h7272"),

    ("H7311","Hebrew","Old Testament","רוּם","rum","Verb","to be high, exalted, lifted up",
     "To be high or to lift up — applied to God's exaltation, the lifting up of prayer and praise, and the pride of the wicked. God himself is <em>rum</em>: high and exalted above all.",
     "Pride and exaltation diverge: God's <em>rum</em> is true majesty; human self-exaltation is pride heading for a fall (Prov 16:18 uses related root). The proper response to God's exaltation is worship.",
     [("Isaiah 6:1","I saw the Lord sitting upon a throne, high and <em>lifted up</em> [rum]."),
      ("Psalm 34:3","Oh, <em>magnify</em> [rum] the LORD with me, and let us exalt his name together."),
      ("Psalm 75:6-7","Exaltation [rum] comes not from the east or west — but God is the judge who puts down one and <em>lifts up</em> another.")],
     "Isaiah 6:1 — the inaugural vision of Isaiah — opens with God's exaltation (rum). This becomes the standard against which human pretension collapses and the foundation for prophetic proclamation of God's sovereignty.",
     [("H1984","H1984 — halal (to praise)"),("H1431","H1431 — gadal (to be great)")],
     "h7311"),

    ("H7323","Hebrew","Old Testament","רוּץ","ruts","Verb","to run, rush, hurry",
     "To run with urgency and purpose. Used of messengers (those who 'run' with news), of eager service, and of the godly running toward God's commandments. Speed implies desire.",
     "Running in Scripture signals priority — you run toward what matters most. The Servant of the LORD will not grow weary (Isa 40:31); those who run to do evil are condemned (Prov 1:16).",
     [("Psalm 119:32","I will <em>run</em> [ruts] in the way of your commandments when you enlarge my heart."),
      ("Isaiah 40:31","They shall <em>run</em> [ruts] and not be weary; they shall walk and not faint."),
      ("Song of Solomon 1:4","Draw me after you; let us <em>run</em> [ruts]. The king has brought me into his chambers.")],
     "Running to keep God's commandments (Ps 119:32) contrasts with running to sin (Prov 1:16). The believer's run is energized by an enlarged heart — desire, not duty, drives the pace.",
     [("H1980","H1980 — halak (to walk/go)"),("H7592","H7592 — shaal (to ask)")],
     "h7323"),

    ("H7349","Hebrew","Old Testament","רַחוּם","rachum","Adjective","compassionate, merciful",
     "The adjective form of <em>rachamim</em> (compassion/womb). Appears in God's self-declaration in Exodus 34:6 — the foundational statement of God's character that echoes throughout the OT.",
     "Exodus 34:6 — 'The LORD, the LORD, a God merciful [rachum] and gracious' — is the most cited OT text within the OT itself. Psalms and prophets invoke this declaration when calling on God's character.",
     [("Exodus 34:6","The LORD, the LORD, a God <em>merciful</em> [rachum] and gracious, slow to anger."),
      ("Psalm 103:8","The LORD is <em>merciful</em> [rachum] and gracious, slow to anger and abounding in steadfast love."),
      ("Nehemiah 9:31","For you are a gracious and <em>merciful</em> [rachum] God.")],
     "The 13 attributes of God (Exod 34:6-7) are called the Thirteen Middot in Jewish tradition. <em>Rachum</em> heads the list after the name YHWH itself — compassion is God's leading attribute in self-revelation.",
     [("H2617","H2617 — chesed (lovingkindness)"),("H7356","H7356 — rachamim (compassion)")],
     "h7349"),

    ("H7378","Hebrew","Old Testament","רִיב","rib","Verb/Noun","to strive, contend, legal dispute",
     "A legal dispute or contention — used of human quarrels and of God's covenant lawsuit against Israel. The prophets bring God's <em>rib</em> (case) against a faithless people, like a courtroom scene.",
     "Isaiah, Micah, and Hosea each open with God's rib (lawsuit) against Israel (Mic 6:1-2: 'Hear what the LORD says: Rise, plead your case [rib]'). The prophets are prosecuting attorneys for the divine plaintiff.",
     [("Micah 6:2","Hear, you mountains, the <em>indictment</em> [rib] of the LORD, and you enduring foundations of the earth."),
      ("Isaiah 1:18","Come now, let us reason together [rib], says the LORD."),
      ("Hosea 4:1","The LORD has a <em>controversy</em> [rib] with the inhabitants of the land.")],
     "The covenant lawsuit (rib pattern) in the prophets follows ancient treaty structure: summons, historical prologue, accusation, verdict, sentence. God is both plaintiff and judge — a paradox resolved only in Christ (the mediator).",
     [("H4941","H4941 — mishpat (judgment/justice)"),("H6664","H6664 — tsedeq (righteousness)")],
     "h7378"),

    ("H7385","Hebrew","Old Testament","רִיק","riq","Adjective/Noun","empty, vain, worthless",
     "Emptiness or vanity — the opposite of substance and meaning. 'Empty hands' return from failed endeavors. The wicked are called <em>req</em> men — men of no substance, moral vacuity.",
     "The emptiness theme runs from Genesis (the earth was 'formless and empty') to Ecclesiastes (all is vanity). Idols are <em>riq</em> — they promise fullness but deliver nothing (Isa 30:7).",
     [("Genesis 37:24","The pit was empty [riq]; there was no water in it."),
      ("Isaiah 30:7","Egypt's help is <em>worthless</em> [riq] and empty."),
      ("Judges 9:4","Abimelech hired worthless [riq] and reckless fellows.")],
     "Hebrew wisdom saw moral emptiness and ontological emptiness as connected. A life without God is literally <em>riq</em> — void, without weight. The NT's 'vain' translations echo this Hebrew foundation.",
     [("H1892","H1892 — hebel (vapor/vanity)"),("H8267","H8267 — sheqer (falsehood)")],
     "h7385"),

    ("H7440","Hebrew","Old Testament","רִנָּה","rinnah","Noun, feminine","ringing cry, shout of joy, lament",
     "A loud vocal expression — either joyful shouting or desperate crying out. The same word covers the shout of joy at harvest and the cry of anguish in suffering. Context determines which.",
     "The range of <em>rinnah</em> from joy to lament reflects how deeply felt emotion is expressed the same way — loudly, whole-heartedly. God hears the <em>rinnah</em> of both suffering and celebration.",
     [("Psalm 30:5","Weeping may tarry for the night, but <em>joy</em> [rinnah] comes with the morning."),
      ("Isaiah 35:10","Everlasting <em>joy</em> [rinnah] shall be upon their heads; they shall obtain gladness and joy."),
      ("Psalm 17:1","Hear a just cause, O LORD; attend to my <em>cry</em> [rinnah]!")],
     "Psalm 30:5's famous contrast — weeping at night, joy (rinnah) in the morning — makes rinnah the emotional sunrise after grief. It frames the entire Psalter's movement from lament to praise.",
     [("H8057","H8057 — simchah (joy/gladness)"),("H7442","H7442 — ranan (to shout for joy)")],
     "h7440"),

    ("H7442","Hebrew","Old Testament","רָנַן","ranan","Verb","to shout for joy, to sing aloud",
     "Loud, exuberant vocal praise — the kind that cannot be contained. Frequently calls on creation itself to join: trees, mountains, heavens. This is praise as celebration, not ceremony.",
     "The Psalms use <em>ranan</em> for the spontaneous overflow of joy before God. Isaiah 44 and 55 call on creation to break forth in singing. Joy in God should exceed any earthly joy.",
     [("Psalm 5:11","Let all who take refuge in you <em>rejoice</em> [ranan]; let them ever sing for joy."),
      ("Isaiah 44:23","<em>Sing</em> for joy [ranan], O heavens, for the LORD has done it!"),
      ("Psalm 145:7","They shall pour forth the fame of your abundant goodness and shall <em>sing aloud</em> [ranan] of your righteousness.")],
     "Creation praise (trees, mountains, heavens rejoicing in ranan) prefigures the 'new creation' praise of Revelation where every creature joins the song. Joy in God is cosmological, not merely personal.",
     [("H7440","H7440 — rinnah (cry of joy)"),("H1984","H1984 — halal (to praise)")],
     "h7442"),

    ("H7521","Hebrew","Old Testament","רָצָה","ratsah","Verb","to be pleased with, accept, delight in",
     "God's acceptance of an offering or person — the ultimate positive verdict. When God <em>ratsah</em> a sacrifice, it is accepted; when a person, they are favored. Connects to grace and election.",
     "The question 'Will God accept/favor me?' is central to OT worship. The Day of Atonement and the entire sacrificial system worked toward <em>ratsah</em> — God's pleasure in his people.",
     [("Psalm 51:16-17","You will not <em>delight</em> [ratsah] in sacrifice... a broken and contrite heart, O God, you will not despise."),
      ("Isaiah 61:2","To proclaim the year of the LORD's <em>favor</em> [ratsah]."),
      ("Leviticus 1:3","He shall offer it...that he may be <em>accepted</em> [ratsah] before the LORD.")],
     "Jesus opens his ministry by citing Isaiah 61:2 — 'the year of the LORD's favor (ratsah)' — and declaring it fulfilled (Luke 4:21). He is the one in whom God is fully pleased (Matt 3:17).",
     [("H7522","H7522 — ratson (favor/delight)"),("H2580","H2580 — chen (grace/favor)")],
     "h7521"),

    ("H7522","Hebrew","Old Testament","רָצוֹן","ratson","Noun, masculine","delight, favor, will, goodwill",
     "God's will or the state of his favor — what pleases him. Can describe God's own delight in his people or the seeking of human approval. 'The king's favor [ratson] is like dew on the grass' (Prov 19:12).",
     "The concept of divine favor (<em>ratson</em>) underlies much of the Psalms — praying that one's words would be acceptable (Ps 19:14). In Proverbs, human wisdom seeks to align with God's ratson.",
     [("Proverbs 8:35","Whoever finds me [Wisdom] finds life and obtains <em>favor</em> [ratson] from the LORD."),
      ("Psalm 19:14","Let the words of my mouth...be acceptable [ratson] in your sight, O LORD."),
      ("Isaiah 49:8","In a time of <em>favor</em> [ratson] I have answered you.")],
     "Paul's citation of Isaiah 49:8 in 2 Cor 6:2 — 'Behold, now is the favorable time [ratson]; behold, now is the day of salvation' — makes the eschatological moment of God's ratson the present age of the gospel.",
     [("H7521","H7521 — ratsah (to be pleased)"),("H2580","H2580 — chen (grace)")],
     "h7522"),

    ("H7549","Hebrew","Old Testament","רָקִיעַ","raqia","Noun, masculine","expanse, firmament, sky",
     "The dome-like expanse of sky that God created on day two and stretched out like a tent (Ps 104:2). The heavens declare God's glory (Ps 19:1) — the <em>raqia</em> itself is a proclamation.",
     "Ancient cosmology pictured the raqia as a solid dome holding back upper waters. Theologically it represents God's ordering of chaos into creation — the sky as the boundary of habitable space.",
     [("Genesis 1:6","Let there be an <em>expanse</em> [raqia] in the midst of the waters."),
      ("Psalm 19:1","The <em>sky</em> [raqia] above proclaims his handiwork."),
      ("Daniel 12:3","Those who are wise shall shine like the brightness of the <em>expanse</em> [raqia].")],
     "Daniel 12:3 uses <em>raqia</em> to describe resurrection glory — the wise shining like the sky. NT resurrection glory (Matt 13:43: 'the righteous will shine like the sun') draws on this image.",
     [("H8064","H8064 — shamayim (heavens)"),("H776","H776 — erets (earth)")],
     "h7549"),

    ("H7585","Hebrew","Old Testament","שְׁאוֹל","sheol","Noun, feminine","the grave, underworld, realm of the dead",
     "The place of the dead in Hebrew thought — the dim realm beneath the earth where all go at death. Not primarily a place of punishment; rather, a state of absence from the living and from full communion with God.",
     "The OT's view of death and afterlife is complex. <em>Sheol</em> is real but shadowy. The hope of resurrection breaks through in passages like Daniel 12:2 and Job 19:25-27, anticipating what the NT makes explicit.",
     [("Psalm 16:10","For you will not abandon my soul to <em>Sheol</em>, or let your holy one see corruption."),
      ("Isaiah 14:9","<em>Sheol</em> below is stirred up to meet you when you come."),
      ("Hosea 13:14","Shall I ransom them from the power of <em>Sheol</em>?")],
     "Psalm 16:10 is cited twice in Acts (2:27; 13:35) as proof of Christ's resurrection — the Holy One did not remain in Sheol. The NT's Hades corresponds to Sheol; Gehenna is the NT's place of final judgment.",
     [("H4194","H4194 — mavet (death)"),("G86","G86 — hades (realm of the dead)")],
     "h7585"),

    ("H7623","Hebrew","Old Testament","שָׁבַח","shabach","Verb","to praise, laud, commend, still",
     "To praise with words of commendation — to declare someone's greatness publicly. Also can mean to calm or still (the waves, a people). Both meanings involve an authoritative declaration.",
     "Psalm 63 and 117 use <em>shabach</em> for the praise that flows from encounter with God. Ecclesiastes uses it to say the dead cannot praise God — making life itself a context for worship.",
     [("Psalm 63:3","Because your steadfast love is better than life, my lips will <em>glorify</em> [shabach] you."),
      ("Psalm 117:1","<em>Praise</em> [shabach] the LORD, all nations!"),
      ("Ecclesiastes 4:2","I thought the dead...more fortunate than the living who are still alive — but better...is he who has not yet been born.")],
     "The call to praise (<em>shabach</em>) assumes that God's character and acts warrant public declaration. It is not merely subjective feeling but proclamation — saying of God what is true.",
     [("H1984","H1984 — halal (to praise)"),("H3034","H3034 — yadah (to thank/praise)")],
     "h7623"),

    ("H7650","Hebrew","Old Testament","שָׁבַע","shaba","Verb","to swear, take an oath",
     "To bind oneself with a solemn oath — literally, to 'seven oneself' (from sheva, seven). In the ancient Near East, oaths sealed covenants, and seven was the number of completion/perfection.",
     "God himself swears oaths (Gen 22:16; Heb 6:13) — the highest form of divine commitment, binding himself by his own name since there is no greater authority. Human oaths called on God as witness.",
     [("Genesis 22:16","By myself I have <em>sworn</em> [shaba], declares the LORD."),
      ("Hebrews 6:13","Since God had no one greater by whom to swear, he <em>swore</em> by himself."),
      ("Psalm 110:4","The LORD has <em>sworn</em> [shaba] and will not change his mind: 'You are a priest forever.'")],
     "God's oath-swearing is unique: he binds himself by his own name because there is no higher authority. Hebrews 6:17-18 says God interposed with an oath so that 'we who have fled for refuge might have strong encouragement.'",
     [("H1285","H1285 — berit (covenant)"),("H571","H571 — emet (truth/faithfulness)")],
     "h7650"),

    ("H7706","Hebrew","Old Testament","שַׁדַּי","shaddai","Noun, proper","the Almighty (divine name)",
     "One of the oldest divine names in Scripture, used especially in patriarchal narratives and Job. The exact etymology is debated (possibly 'mountain' or 'breast/nourisher'), but its meaning is clear: overwhelming power and all-sufficiency.",
     "God reveals himself to Abraham as <em>El Shaddai</em> (God Almighty, Gen 17:1) before revealing the name YHWH to Moses (Exod 6:3). Job's speeches use Shaddai 31 times — more than any other book.",
     [("Genesis 17:1","I am God Almighty [El Shaddai]; walk before me, and be blameless."),
      ("Exodus 6:3","I appeared to Abraham...as God Almighty [El Shaddai], but by my name the LORD I did not make myself known."),
      ("Job 37:23","The Almighty [Shaddai] — we cannot find him; he is great in power.")],
     "The shift from Shaddai to YHWH (Exod 6:3) marks a deepening of divine self-revelation. Patriarchs knew God as the Mighty One; Israel would know him as the covenant-keeping, personally present LORD.",
     [("H410","H410 — el (God/mighty one)"),("H3068","H3068 — YHWH (LORD)")],
     "h7706"),

    ("H7782","Hebrew","Old Testament","שׁוֹפָר","shophar","Noun, masculine","ram's horn, trumpet",
     "The curved horn of a ram, used as a musical instrument for signaling. Blown at the giving of the Law, the Jubilee, the new year, battle, and in worship. The <em>shophar</em> announced divine events.",
     "The Shofar connects human time with divine action. Its blast at Sinai terrified Israel (Exod 19:16); in Joshua 6 it brought down Jericho's walls; at Rosh Hashanah it calls Israel to repentance.",
     [("Exodus 19:16","There were thunders and lightnings and a thick cloud on the mountain and a very loud <em>trumpet</em> [shophar] blast."),
      ("Joshua 6:5","When they make a long blast with the ram's horn [shophar], all the people shall shout."),
      ("1 Thessalonians 4:16","The Lord himself will descend from heaven with a cry of command, with the voice of an archangel, and with the sound of the trumpet of God.")],
     "Paul's 'last trumpet' (1 Cor 15:52) and the trumpets of Revelation stand in the shophar tradition — cosmic, divine announcements that reorganize reality. The Jubilee shophar (Lev 25) proclaimed liberty, which Jesus claimed to fulfill (Luke 4:18).",
     [("H2689","H2689 — chatsotsera (silver trumpet)"),("G4536","G4536 — salpinx (trumpet)")],
     "h7782"),

    ("H7832","Hebrew","Old Testament","שָׂחַק","sachaq","Verb","to laugh, play, rejoice, mock",
     "Laughter in its full range — from joy and play to mockery and derision. Sarah laughed (sachaq) at God's promise of a son; Isaac's name derives from this root. God laughs at the wicked (Ps 37:13).",
     "The ambiguity of laughter runs through Scripture. Sarah's laugh of disbelief becomes the joy of fulfillment — her son Isaac embodies the transformation. God's derisive laugh at nations expresses sovereign confidence.",
     [("Genesis 21:6","God has made <em>laughter</em> [sachaq] for me; everyone who hears will laugh over me."),
      ("Psalm 37:13","The LORD <em>laughs</em> [sachaq] at the wicked, for he sees that his day is coming."),
      ("Ecclesiastes 3:4","A time to weep, and a time to <em>laugh</em> [sachaq].")],
     "Isaac's name — Yitschaq — means 'he laughs.' The laughter that begins in Sarah's disbelief (Gen 18:12) becomes the laughter of fulfilled promise (Gen 21:6) — a model of faith vindicated.",
     [("H8057","H8057 — simchah (joy)"),("H8055","H8055 — samach (to rejoice)")],
     "h7832"),

    ("H7836","Hebrew","Old Testament","שָׁחַר","shachar","Verb","to seek earnestly, seek early, dawn",
     "To seek diligently — the image is of rising at dawn to seek someone before the day's business begins. The <em>shachar</em> (dawn) and the verb of seeking share the same root, implying dawn-seeking.",
     "Proverbs personifies Wisdom saying 'those who seek me diligently [shachar] will find me' (Prov 8:17). The connection between dawn and diligent seeking suggests the urgency and priority of seeking God.",
     [("Proverbs 8:17","I love those who love me, and those who seek me diligently [shachar] find me."),
      ("Psalm 63:1","O God, you are my God; earnestly I seek [shachar] you; my soul thirsts for you."),
      ("Hosea 5:15","In their distress they will earnestly seek [shachar] me.")],
     "Psalm 63:1 pairs <em>shachar</em> (earnest seeking) with thirst — both describe urgent desire. Seeking God at dawn becomes a spiritual metaphor: God is the first priority, sought before anything else.",
     [("H1875","H1875 — darash (to seek/inquire)"),("H7836","H7836 — shachar (dawn)")],
     "h7836"),

    ("H7843","Hebrew","Old Testament","שָׁחַת","shachath","Verb","to destroy, corrupt, ruin, spoil",
     "To destroy or corrupt — used of moral corruption before the Flood (Gen 6:11-12), of God's destroying judgment, and of human ruin. The 'destroyer' in Egypt at Passover is the same root.",
     "The Flood narrative uses <em>shachath</em> repeatedly: the earth was corrupt, all flesh had corrupted its way (Gen 6:11-12). God's response to corruption is the flood — destruction restoring creation order.",
     [("Genesis 6:12","God saw the earth, and behold, it was <em>corrupt</em> [shachath], for all flesh had <em>corrupted</em> their way."),
      ("Exodus 12:23","The LORD will not allow the <em>destroyer</em> [shachath] to enter your houses."),
      ("Isaiah 54:16","I have created the destroyer [shachath] to destroy.")],
     "The 'destroyer' (mashchit) of Passover (Exod 12:23) shares this root. God both uses and restrains destruction. The incarnation brings the Savior into a world under <em>shachath</em> — corruption — to reverse the ruin of sin.",
     [("H7489","H7489 — raa (to be evil/destroy)"),("H2398","H2398 — chata (to sin)")],
     "h7843"),

    ("H7854","Hebrew","Old Testament","שָׂטָן","satan","Noun/Verb","adversary, accuser, Satan",
     "An adversary or accuser — one who opposes. Used of human opponents, of the angel blocking Balaam's path, and of the cosmic Accuser in Job and Zechariah. The NT personalizes this as the Devil.",
     "In Job 1-2 and Zechariah 3, ha-satan (the Accuser) functions in a heavenly court. The definite article suggests a role, not yet a personal name. By the NT, Satan is clearly a personal, fallen being opposing God.",
     [("Job 1:6","The sons of God came to present themselves before the LORD, and <em>Satan</em> also came among them."),
      ("Zechariah 3:1","He showed me Joshua the high priest standing before the angel...and <em>Satan</em> standing at his right hand to accuse him."),
      ("1 Chronicles 21:1","<em>Satan</em> stood against Israel and incited David to number Israel.")],
     "Zechariah 3 gives the clearest OT picture: Satan accuses; God rebukes Satan and clothes Joshua in clean garments — a preview of the gospel. Jesus' declaration 'I saw Satan fall like lightning' (Luke 10:18) shows the decisive defeat of the Accuser.",
     [("H341","H341 — oyev (enemy)"),("G1228","G1228 — diabolos (devil)")],
     "h7854"),

    ("H7878","Hebrew","Old Testament","שִׂיחַ","siach","Verb","to meditate, muse, speak, complain",
     "To let thoughts run freely — meditating, musing, or speaking at length. Used of both deep meditation on God's word and of complaint poured out in prayer. Both are valid forms of speech to God.",
     "The range from meditation to complaint reflects honest prayer. Psalm 77 uses <em>siach</em> for troubled musing in the night; Psalm 119 uses it for delighting in God's statutes. Same word, different heart postures.",
     [("Psalm 77:6","I <em>meditate</em> [siach] in my heart; let my spirit make diligent search."),
      ("Psalm 119:15","I will <em>meditate</em> [siach] on your precepts and fix my eyes on your ways."),
      ("Psalm 55:17","Evening and morning and at noon I will utter my <em>complaint</em> [siach] and moan.")],
     "The word's breadth — meditation and complaint — validates the full Psalter's range. God welcomes both the praising meditator and the lamenting complainer. Both are forms of authentic engagement with the living God.",
     [("H1897","H1897 — hagah (to meditate/murmur)"),("H8605","H8605 — tephillah (prayer)")],
     "h7878"),

    ("H7901","Hebrew","Old Testament","שָׁכַב","shakab","Verb","to lie down, sleep, have sexual relations",
     "To lie down — for sleep, rest, death, or sexual intimacy. The euphemism 'to lie with' describes sexual relations. 'He lay down with his fathers' is the standard death formula for kings.",
     "The resting/sleeping/dying range of <em>shakab</em> connects mortal sleep and eternal sleep. The resurrection hope is implicit in texts like Daniel 12:2 where many who 'sleep in the dust' will awake.",
     [("Daniel 12:2","Many of those who sleep [shakab] in the dust of the earth shall awake."),
      ("Psalm 4:8","In peace I will both lie down [shakab] and sleep; for you alone, O LORD, make me dwell in safety."),
      ("Ruth 3:4","When he lies down [shakab], observe the place where he lies.")],
     "Daniel 12:2 is a pivotal resurrection text — <em>shakab</em> used of death, with awakening to follow. Paul's language 'those who have fallen asleep' (1 Thess 4:13-15) draws on this OT idiom of death as sleep.",
     [("H8142","H8142 — shenah (sleep)"),("H6965","H6965 — qum (to arise/stand)")],
     "h7901"),

    ("H7919","Hebrew","Old Testament","שָׂכַל","sakal","Verb","to be prudent, wise, give insight, prosper",
     "To act with wise understanding and consequent success. The Servant of the LORD 'will act wisely' (<em>sakal</em>, Isa 52:13); David 'acted wisely' wherever Saul sent him (1 Sam 18:5). Wisdom leads to success.",
     "Joshua is commanded to meditate on the Torah so that he will act wisely and succeed (Josh 1:8). The connection between wisdom and success in <em>sakal</em> is not material prosperity but aligned living.",
     [("Isaiah 52:13","Behold, my servant shall act wisely [sakal]; he shall be high and lifted up."),
      ("Joshua 1:8","You shall meditate on it day and night...for then you will make your way prosperous and have good success [sakal]."),
      ("Proverbs 10:19","Whoever restrains his lips is <em>prudent</em> [sakal].")],
     "Isaiah 52:13 opens the fourth Servant Song with <em>sakal</em> — the Servant will act wisely. The rest of the song shows the Servant's 'wisdom' was the path through suffering to glory — a redefinition of success.",
     [("H2451","H2451 — chokmah (wisdom)"),("H3820","H3820 — lev (heart/mind)")],
     "h7919"),

    ("H7931","Hebrew","Old Testament","שָׁכַן","shakan","Verb","to dwell, settle, tabernacle",
     "To dwell or settle in a place — used especially of God's dwelling among his people. The divine presence that 'tabernacled' (shakan) with Israel gives us the word <em>shekinah</em> (though this word itself is post-biblical).",
     "God's desire to dwell among his people is the golden thread of Scripture: Eden > Tabernacle > Temple > Incarnation > New Jerusalem. Each is a form of divine <em>shakan</em>.",
     [("Exodus 25:8","Let them make me a sanctuary, that I may <em>dwell</em> [shakan] in their midst."),
      ("Psalm 85:9","Salvation is near...that glory may <em>dwell</em> [shakan] in our land."),
      ("John 1:14","The Word became flesh and <em>dwelt</em> among us [eskēnōsen — tabernacled].")],
     "John 1:14 uses the Greek verb <em>skēnoō</em> (to tabernacle/pitch tent) — a deliberate echo of <em>shakan</em>. Jesus is the ultimate fulfillment of God's long desire to dwell with his people.",
     [("H4908","H4908 — mishkan (tabernacle)"),("G4637","G4637 — skenoō (to tabernacle)")],
     "h7931"),

    ("H8002","Hebrew","Old Testament","שֶׁלֶם","shelem","Noun, masculine","peace offering, fellowship offering",
     "The 'fellowship' or 'peace' offering — one of the main sacrifice types, associated with communal eating and celebration before God. Unlike burnt offerings (wholly consumed), the <em>shelem</em> was shared.",
     "The peace offering created <em>shalom</em> — wholeness and right relationship — between God and worshipper. The shared meal at the altar foreshadowed communion and the Messianic banquet.",
     [("Leviticus 3:1","If his offering is a sacrifice of <em>peace offering</em> [shelem], if he offers an animal from the herd..."),
      ("Amos 5:22","Even though you offer me...your <em>peace offerings</em> [shelem], I will not look upon them."),
      ("Ezekiel 46:2","The prince shall...worship at the threshold...and the priests shall offer his...peace offerings [shelem].")],
     "Amos 5:22 shows the danger of ritual without justice — God rejects <em>shelem</em> from those who oppress the poor. Ritual and ethics cannot be separated. Christ is the true peace offering who achieves real shalom.",
     [("H7965","H7965 — shalom (peace)"),("H2077","H2077 — zebach (sacrifice)")],
     "h8002"),

    ("H8130","Hebrew","Old Testament","שָׂנֵא","sane","Verb","to hate, be hostile to",
     "The opposite of love — active hatred or rejection. Used of human enmity and of God's 'hating' evil and evildoers (Ps 5:5; 11:5). The prophets condemn those who 'hate good and love evil' (Mic 3:2).",
     "Biblical hate is not just feeling but orientation — turning away from, rejecting, treating as an enemy. 'Jacob I loved, Esau I hated' (Mal 1:2-3; Rom 9:13) uses election language, not merely emotion.",
     [("Psalm 5:5","You hate [sane] all evildoers."),
      ("Malachi 1:3","I have <em>hated</em> [sane] Esau."),
      ("Proverbs 6:16","There are six things the LORD <em>hates</em> [sane]...")],
     "The 'seven abominations' of Proverbs 6 clarify what God hates: pride, lies, murder, evil schemes, eagerness to sin, false witness, strife. Hatred of evil is inseparable from love of good in biblical ethics.",
     [("H157","H157 — ahab (to love)"),("H8441","H8441 — toevah (abomination)")],
     "h8130"),

    ("H8193","Hebrew","Old Testament","שָׂפָה","saphah","Noun, feminine","lip, language, speech, edge, shore",
     "The lip as the organ of speech and also as edge/border (seashore, edge of a garment). Speech is the central meaning. 'Pure lips' signify righteous speech; the Tower of Babel divided the one <em>saphah</em> (language).",
     "The lips represent the whole communicative self. Isaiah's vision (Isa 6:5-7) is resolved by a coal touching his unclean lips — speech purified for prophetic mission. Proverbs repeatedly contrasts righteous and wicked lips.",
     [("Genesis 11:1","The whole earth had one language [saphah] and the same words."),
      ("Isaiah 6:5","Woe is me! For I am a man of unclean <em>lips</em> [saphah]."),
      ("Psalm 34:13","Keep your <em>tongue</em> from evil and your <em>lips</em> [saphah] from speaking deceit.")],
     "Genesis 11:1 (one language/saphah) and Acts 2 (Pentecost reversing Babel) form a bracket. The Spirit gives the church a new unity of speech — proclaiming God's mighty works in every tongue.",
     [("H3956","H3956 — lashon (tongue)"),("H6310","H6310 — peh (mouth)")],
     "h8193"),

    ("H8213","Hebrew","Old Testament","שָׁפֵל","shaphel","Verb","to be low, humble, brought low",
     "To be in a lowly position — geographically, socially, or spiritually. God exalts the humble and brings low the proud (1 Sam 2:7). The 'low valleys' filled and 'rough places' made level in Isaiah 40 use this root.",
     "The exalt/humble dynamic is central to biblical theology. Mary's Magnificat (Luke 1:52) echoes Hannah's song: God has brought down the mighty and exalted those of humble estate — <em>shaphel</em> reversed.",
     [("Isaiah 40:4","Every valley shall be <em>lifted up</em>, and every mountain and hill be made low [shaphel]."),
      ("Proverbs 29:23","One's pride will bring him low [shaphel], but he who is lowly in spirit will obtain honor."),
      ("Job 40:11","Look on everyone who is proud and <em>bring him low</em> [shaphel].")],
     "Isaiah 40:3-4's preparation for God's coming involves shaphel-ing the mountains and lifting the valleys — moral and cosmic leveling for the arrival of the King. John the Baptist is this voice in the wilderness (John 1:23).",
     [("H1361","H1361 — gabah (to be high/proud)"),("H6041","H6041 — ani (poor/humble)")],
     "h8213"),

    ("H8269","Hebrew","Old Testament","שַׂר","sar","Noun, masculine","prince, official, commander, chief",
     "A leader or official — military commander, court official, or royal prince. The Messianic title 'Prince of Peace' (Isaiah 9:6) uses this word as <em>sar-shalom</em>.",
     "Authority structures in Israel used <em>sar</em> at every level: commanders of thousands, princes of tribes, officials in the court. The divine Warrior-Prince of Joshua 5 is the pre-incarnate Christ.",
     [("Isaiah 9:6","His name shall be called Wonderful Counselor, Mighty God, Everlasting Father, <em>Prince of Peace</em> [sar-shalom]."),
      ("Joshua 5:14","I am the commander [sar] of the army of the LORD."),
      ("Daniel 12:1","Michael, the great <em>prince</em> [sar] who has charge of your people.")],
     "Isaiah 9:6's compound title — <em>sar-shalom</em> — makes peace the defining characteristic of Messiah's rule. He is not a war-prince who brings peace after conquest; he IS the Prince of Peace, whose kingdom IS shalom.",
     [("H4428","H4428 — melek (king)"),("H7965","H7965 — shalom (peace)")],
     "h8269"),

    ("H8334","Hebrew","Old Testament","שָׁרַת","sharath","Verb","to minister, serve, attend",
     "To serve in an official capacity — specifically the cultic service of priests and Levites, and the royal service of courtiers. A higher, more dignified word than ordinary labor; it implies honor in serving.",
     "Priests <em>sharath</em> God; angels <em>sharath</em> as divine messengers; ministers <em>sharath</em> kings. Service to God is the highest form of <em>sharath</em> — an honor, not a burden.",
     [("Numbers 3:6","Bring the tribe of Levi near...that they may <em>minister</em> [sharath] to him."),
      ("Psalm 103:21","Bless the LORD, all his hosts, his <em>ministers</em> [sharath], who do his will."),
      ("Hebrews 1:14","Are they not all ministering [leitourgika] spirits sent out to serve for the sake of those who are to inherit salvation?")],
     "Hebrews 1:14 echoes <em>sharath</em> with <em>leitourgika</em> (liturgical/ministerial spirits). Angels are divine ministers; believers are priests (1 Pet 2:9) — the whole redeemed community becomes a worshipping, serving body.",
     [("H5647","H5647 — avad (to serve/work)"),("H3548","H3548 — kohen (priest)")],
     "h8334"),

    ("H8426","Hebrew","Old Testament","תּוֹדָה","todah","Noun, feminine","thanksgiving, praise, thank offering",
     "Thanksgiving offered to God in word and sacrifice. The <em>todah</em> offering was made when God had delivered from distress — a public testimony set to music. Psalm 100 is a psalm of todah.",
     "The thanksgiving sacrifice involved recounting God's saving act before the assembly — a public testimony. Scholars see the todah as the root of the Last Supper: Jesus' Passover meal was a form of covenant thanksgiving.",
     [("Psalm 100:1-4","Enter his gates with <em>thanksgiving</em> [todah], and his courts with praise!"),
      ("Psalm 50:23","The one who offers <em>thanksgiving</em> [todah] as his sacrifice glorifies me."),
      ("Jeremiah 33:11","There shall be heard again the voice of <em>mirth</em>...the voices of those who sing as they bring <em>thank offerings</em> [todah] to the house of the LORD.")],
     "Jeremiah 33:11 links the restoration of Jerusalem with the return of todah — thanksgiving as the sound of the redeemed community. Eschatological joy is measured by whether the todah resumes.",
     [("H1984","H1984 — halal (to praise)"),("H8416","H8416 — tehillah (praise)")],
     "h8426"),

    ("H8435","Hebrew","Old Testament","תּוֹלְדוֹת","toledoth","Noun, feminine","generations, records, history, birth narrative",
     "The recurring structural phrase in Genesis: 'These are the <em>toledoth</em> of...' — introducing each major section. Literally 'begettings' or 'what was generated,' it organizes the book around origins and outcomes.",
     "The phrase 'these are the generations of' appears 11 times in Genesis, structuring the book. Each <em>toledoth</em> section recounts what flowed from a key person or event — a theology of origins and consequences.",
     [("Genesis 2:4","These are the <em>generations</em> [toledoth] of the heavens and the earth when they were created."),
      ("Genesis 5:1","This is the book of the <em>generations</em> [toledoth] of Adam."),
      ("Matthew 1:1","The book of the <em>genealogy</em> [genesis] of Jesus Christ, the son of David.")],
     "Matthew 1:1's 'book of the genealogy of Jesus Christ' deliberately echoes the Genesis toledoth formula. Jesus is the culminating 'generation' — what all the preceding begettings were pointing toward.",
     [("H1121","H1121 — ben (son)"),("H2233","H2233 — zera (seed/offspring)")],
     "h8435"),

    ("H8577","Hebrew","Old Testament","תַּנִּין","tannin","Noun, masculine","sea monster, dragon, serpent, leviathan",
     "A great sea creature or dragon — used of literal large water creatures and of mythological sea monsters representing chaos. Egypt is called a <em>tannin</em> (Ezek 29:3). God's power over the tannin shows cosmic sovereignty.",
     "Ancient Near Eastern mythology featured sea monsters as chaos-beings. Israel's God commands these creatures (Job 7:12; Ps 148:7) and will ultimately slay Leviathan (Isa 27:1). Creation tames the chaos.",
     [("Genesis 1:21","God created the great sea creatures [tannin] and every living creature that moves."),
      ("Isaiah 27:1","The LORD...will punish Leviathan...and he will slay the dragon [tannin] that is in the sea."),
      ("Ezekiel 29:3","Behold, I am against you, Pharaoh king of Egypt, the great dragon [tannin] that lies in the midst of his streams.")],
     "Revelation 12-13 uses dragon imagery drawn from this tradition — the dragon is Satan, the chaos-power opposing God. Genesis 1:21 declares God created the great sea creatures — he is not in contest with them; they serve him.",
     [("H3882","H3882 — livyatan (Leviathan)"),("H5175","H5175 — nachash (serpent)")],
     "h8577"),

    ("H8655","Hebrew","Old Testament","תְּרָפִים","teraphim","Noun, masculine plural","household idols, image",
     "Small household figurines used for divination and as protective household gods. Rachel stole Laban's teraphim (Gen 31); they appear alongside legitimate religion, showing how syncretism crept into Israel.",
     "The teraphim represent the compromise of exclusive YHWH worship with household religion. Even Micah's household had a teraphim-shrine (Judg 17-18). Their condemnation is consistent: Josiah's reform destroys them (2 Kgs 23:24).",
     [("Genesis 31:19","Rachel stole her father's <em>household gods</em> [teraphim]."),
      ("1 Samuel 15:23","For rebellion is as the sin of divination, and presumption is as iniquity and idolatry [teraphim]."),
      ("2 Kings 23:24","Moreover, Josiah put away the mediums and the <em>household gods</em> [teraphim].")],
     "Teraphim represent the perennial temptation to mix exclusive covenant loyalty with popular religion. Samuel equates consulting teraphim with rebellion (1 Sam 15:23). Josiah's purge was Reformation-like — removing what had accumulated.",
     [("H457","H457 — elil (worthless idol)"),("H6456","H6456 — pesel (carved image)")],
     "h8655"),

    # --- Greek words ---
    ("G3056","Greek","New Testament","λόγος","logos","Noun, masculine","word, reason, message, account",
     "The word or rational principle — used in Greek philosophy for the ordering principle of the universe and in John 1 for the eternal Son of God. John's prologue is a deliberate engagement with both Jewish and Greek thought.",
     "John's use of <em>logos</em> bridges Jewish wisdom literature (Prov 8) and Greek philosophy, declaring that the eternal rational principle has become flesh. Every use of 'word' in Scripture participates in this concept.",
     [("John 1:1","In the beginning was the <em>Word</em> [logos], and the Word was with God, and the Word was God."),
      ("John 1:14","And the <em>Word</em> [logos] became flesh and dwelt among us."),
      ("Hebrews 4:12","The <em>word</em> [logos] of God is living and active, sharper than any two-edged sword.")],
     "John's logos Christology is the NT's most philosophically sophisticated claim: the divine rational principle that structures reality is a person — Jesus of Nazareth. This became the foundation of Christian engagement with Greek philosophy.",
     [("G4487","G4487 — rhema (word/saying)"),("H1697","H1697 — dabar (word)")],
     "g3056"),

    ("G3107","Greek","New Testament","μακάριος","makarios","Adjective","blessed, happy, fortunate",
     "The Greek word for blessedness — not emotional happiness dependent on circumstances, but the deep well-being of those who are right with God. The Beatitudes (Matt 5) open with <em>makarios</em>.",
     "Makarios was used in Greek of the gods who lived free from human troubles, and of the dead who were beyond earthly care. Jesus redefines it entirely — the blessed are the poor in spirit, the mourning, the persecuted.",
     [("Matthew 5:3","<em>Blessed</em> [makarios] are the poor in spirit, for theirs is the kingdom of heaven."),
      ("Revelation 1:3","<em>Blessed</em> [makarios] is the one who reads aloud the words of this prophecy."),
      ("Romans 4:7-8","<em>Blessed</em> [makarios] are those whose lawless deeds are forgiven.")],
     "The Beatitudes reverse every worldly measure of blessing. Jesus declares the mourning, the meek, the persecuted to be makarios — blessed beyond those the world counts happy. Paul's citation of Ps 32 in Romans 4 applies makarios to justification.",
     [("G5479","G5479 — chara (joy)"),("H835","H835 — ashre (blessed/happy)")],
     "g3107"),

    ("G3115","Greek","New Testament","μακροθυμία","makrothumia","Noun, feminine","patience, longsuffering, steadfastness",
     "Long-tempered endurance — the opposite of short-tempered anger. The word is a compound: <em>makros</em> (long) + <em>thumos</em> (passion/wrath). God's makrothumia is his patience with sinners (2 Pet 3:9).",
     "Included in both the fruit of the Spirit (Gal 5:22) and God's own character (Rom 2:4). The NT explains history's length as a form of divine makrothumia — God giving time for repentance before judgment.",
     [("2 Peter 3:9","The Lord is not slow to fulfill his promise...but is <em>patient</em> [makrothumia] toward you, not wishing that any should perish."),
      ("Galatians 5:22","The fruit of the Spirit is love, joy, peace, <em>patience</em> [makrothumia]..."),
      ("Hebrews 6:12","Through faith and <em>patience</em> [makrothumia] inherit the promises.")],
     "God's makrothumia toward sinners is the reason the present age continues. 2 Peter 3:15 says to 'count the patience [makrothumia] of our Lord as salvation' — his delay is grace, not absence.",
     [("G5281","G5281 — hupomone (endurance)"),("G5485","G5485 — charis (grace)")],
     "g3115"),

    ("G3340","Greek","New Testament","μετανοέω","metanoeo","Verb","to repent, change one's mind",
     "To change the mind at the deepest level — a turn of orientation, not merely regret. The word is <em>meta</em> (after/change) + <em>nous</em> (mind). John the Baptist and Jesus both opened their ministries with 'Repent!'",
     "Repentance in the NT is not primarily about emotion but direction — a turning from idols to the living God (1 Thess 1:9). It's the gateway to the kingdom and the ongoing posture of discipleship.",
     [("Matthew 4:17","Jesus began to preach, saying, 'Repent [metanoeo], for the kingdom of heaven is at hand.'"),
      ("Acts 2:38","Peter said to them, '<em>Repent</em> [metanoeo] and be baptized every one of you.'"),
      ("Revelation 3:19","Those whom I love, I reprove and discipline, so be zealous and <em>repent</em> [metanoeo].")],
     "The pairing of repentance with belief (Mark 1:15) defines the gospel response. Metanoeo is comprehensive — it affects the mind (nous), which then reorients the will and actions. It is the cognitive core of conversion.",
     [("G3341","G3341 — metanoia (repentance)"),("H7725","H7725 — shuv (to return/repent)")],
     "g3340"),

    ("G3341","Greek","New Testament","μετάνοια","metanoia","Noun, feminine","repentance, change of mind",
     "The noun form of metanoeo — the state or act of repentance. One of the NT's most significant theological concepts, paired with faith as the two-fold response to the gospel.",
     "The NT uses metanoia to describe both initial conversion and ongoing renewal. John the Baptist demanded fruit worthy of metanoia (Matt 3:8). Paul summarizes his ministry as calling for 'repentance toward God and faith in our Lord Jesus' (Acts 20:21).",
     [("Acts 20:21","Testifying both to Jews and to Greeks of <em>repentance</em> [metanoia] toward God and of faith in our Lord Jesus Christ."),
      ("2 Corinthians 7:10","Godly grief produces a <em>repentance</em> [metanoia] that leads to salvation."),
      ("Acts 5:31","God exalted Jesus...to give <em>repentance</em> [metanoia] to Israel and forgiveness of sins.")],
     "Acts 5:31 makes repentance a gift — God grants metanoia (also 2 Tim 2:25). This prevents a works-based view of repentance: even the turning is enabled by grace. Metanoia and pistis (faith) are twin gifts.",
     [("G3340","G3340 — metanoeo (to repent)"),("G4102","G4102 — pistis (faith)")],
     "g3341"),

    ("G3466","Greek","New Testament","μυστήριον","musterion","Noun, neuter","mystery, secret, hidden truth now revealed",
     "Not an unknowable secret but a truth formerly hidden and now disclosed — specifically the plan of God revealed in the gospel. Paul uses musterion for the inclusion of Gentiles in the body of Christ (Eph 3:3-6).",
     "The NT transforms the Greek word for pagan mystery-cult secrets into a word for the open gospel. God's mystery is now published, not hoarded — proclaimed to all nations (Rom 16:25-26).",
     [("Ephesians 3:6","This <em>mystery</em> [musterion] is that the Gentiles are fellow heirs, members of the same body."),
      ("Colossians 1:27","God chose to make known...the riches of the glory of this <em>mystery</em> [musterion], which is Christ in you."),
      ("Romans 16:25-26","The <em>mystery</em> [musterion] kept secret for long ages but now disclosed.")],
     "Paul's mystery = Christ + Gentiles together = one body. This was hidden in the OT's shadow but is now proclaimed. The preaching of the mystery is itself eschatological — it heralds the age of fulfillment.",
     [("G602","G602 — apokalupsis (revelation)"),("G4678","G4678 — sophia (wisdom)")],
     "g3466"),

    ("G3551","Greek","New Testament","νόμος","nomos","Noun, masculine","law, Torah, principle",
     "Law in its broadest sense — from the specific Torah of Moses to general principles of operation. Paul's complex theology of nomos distinguishes its role in condemning sin (Rom 3:20) from its place in the new covenant (Rom 8:4).",
     "The Torah is God's gracious gift to Israel — not the means of salvation but the constitution of covenant life. Paul argues the law was never meant to justify but to expose sin and lead to Christ (Gal 3:24).",
     [("Romans 3:20","Through the <em>law</em> [nomos] comes knowledge of sin."),
      ("Galatians 3:24","The <em>law</em> [nomos] was our guardian until Christ came."),
      ("Romans 8:4","The righteous requirement of the <em>law</em> [nomos] might be fulfilled in us.")],
     "Paul's nuanced treatment of nomos distinguishes the law's many functions: accuser, guide, shadow, covenant-boundary. The law is holy (Rom 7:12) but cannot give life (Gal 3:21). Only the Spirit fulfills what the law demanded.",
     [("H8451","H8451 — torah (law/instruction)"),("G5485","G5485 — charis (grace)")],
     "g3551"),

    ("G3563","Greek","New Testament","νοῦς","nous","Noun, masculine","mind, understanding, reason",
     "The rational faculty — the mind as seat of understanding, discernment, and moral reasoning. Paul calls for the renewal of the nous (Rom 12:2) and speaks of having 'the mind [nous] of Christ' (1 Cor 2:16).",
     "The mind is the battlefield of sanctification. Idolatry is a problem of the nous — suppressing truth (Rom 1:18). Renewal of the nous is how transformation happens: thinking differently, seeing reality as God sees it.",
     [("Romans 12:2","Be transformed by the renewing of your <em>mind</em> [nous]."),
      ("1 Corinthians 2:16","We have the <em>mind</em> [nous] of Christ."),
      ("Ephesians 4:23","Be renewed in the spirit of your <em>minds</em> [nous].")],
     "The renewed nous is central to Paul's ethics — not rule-following but transformed perception. Having the 'mind of Christ' means seeing situations as Christ sees them, then acting accordingly. This is sanctification from the inside out.",
     [("G2588","G2588 — kardia (heart)"),("G4151","G4151 — pneuma (spirit)")],
     "g3563"),

    ("G3629","Greek","New Testament","οἰκτίρμων","oiktirmon","Adjective","merciful, compassionate",
     "Deeply compassionate — feeling and acting on the misery of others. Used of God's mercy (Luke 6:36: 'Be merciful, even as your Father is merciful') and in the NT exhortation to show mercy.",
     "Luke 6:36 uses oiktirmon in the Sermon on the Plain parallel to Matthew's 'perfect' (Matt 5:48). Mercy, not abstract perfection, is the defining family trait of God's children.",
     [("Luke 6:36","Be <em>merciful</em> [oiktirmon], even as your Father is merciful."),
      ("James 5:11","The Lord is compassionate [oiktirmon] and merciful."),
      ("Romans 12:1","By the mercies [oiktirmon] of God, present your bodies as a living sacrifice.")],
     "James 5:11 pairs oiktirmon with <em>polusplagchnos</em> (very compassionate) — double-strength mercy language for God. The appeal of Romans 12:1 is grounded entirely in God's mercies, not obligation.",
     [("G1656","G1656 — eleos (mercy)"),("H7349","H7349 — rachum (compassionate)")],
     "g3629"),

    ("G3670","Greek","New Testament","ὁμολογέω","homologeo","Verb","to confess, acknowledge, declare publicly",
     "To say the same thing — from <em>homos</em> (same) + <em>legō</em> (to say). Confession is agreeing with God's assessment: of sin (1 John 1:9), of Christ (Rom 10:9), and of truth before others.",
     "Confession has two directions: confessing sin (agreeing with God that it is sin) and confessing Christ (publicly declaring him as Lord). Both are forms of aligning one's words with reality.",
     [("Romans 10:9","If you confess [homologeo] with your mouth that Jesus is Lord...you will be saved."),
      ("1 John 1:9","If we confess [homologeo] our sins, he is faithful and just to forgive us."),
      ("Matthew 10:32","Everyone who <em>acknowledges</em> [homologeo] me before men, I also will acknowledge before my Father.")],
     "The two great confessions — of sin and of Christ — are the Christian life in miniature: owning our failure and owning our Savior. Matthew 10:32 raises the stakes: earthly confession of Christ determines heavenly acknowledgment.",
     [("G1843","G1843 — exomologeo (to confess/praise)"),("G4102","G4102 — pistis (faith)")],
     "g3670"),

    ("G3709","Greek","New Testament","ὀργή","orge","Noun, feminine","wrath, anger, indignation",
     "Wrath — divine or human anger that is settled and purposeful, not explosive passion. The NT's teaching on God's wrath (Rom 1:18) must be understood in light of his justice and righteousness, not human rage.",
     "Paul's theology in Romans 1-3 argues that God's wrath (orge) is revealed against all unrighteousness — it is the negative side of his holiness, the necessary response of a just God to sin.",
     [("Romans 1:18","For the wrath [orge] of God is revealed from heaven against all ungodliness."),
      ("Ephesians 2:3","We were by nature children of <em>wrath</em> [orge], like the rest of mankind."),
      ("Revelation 6:17","For the great day of their <em>wrath</em> [orge] has come.")],
     "The same God who is love (1 John 4:8) is the God whose orge is revealed. These are not contradictions but aspects of his perfect character. The cross is the place where God's wrath and God's love meet — satisfying both.",
     [("G2372","G2372 — thumos (wrath/passion)"),("H639","H639 — aph (anger)")],
     "g3709"),

    ("G3809","Greek","New Testament","παιδεία","paideia","Noun, feminine","discipline, training, instruction",
     "The whole process of raising and educating a child — instruction, correction, and discipline together. Hebrews 12 uses paideia to reframe suffering as God's fatherly training rather than punishment or abandonment.",
     "Greek culture saw paideia as the formation of character through education and discipline. The NT adopts this: God's discipline is purposeful formation, not random hardship. No discipline seems pleasant at the time (Heb 12:11).",
     [("Hebrews 12:11","For the moment all <em>discipline</em> [paideia] seems painful rather than pleasant, but later it yields the peaceful fruit of righteousness."),
      ("Ephesians 6:4","Bring your children up in the <em>discipline</em> [paideia] and instruction of the Lord."),
      ("2 Timothy 3:16","All Scripture is...profitable for teaching, for reproof, for correction, for training [paideia] in righteousness.")],
     "2 Timothy 3:16 identifies Scripture as the instrument of God's paideia — four overlapping functions all aimed at forming righteousness. The goal of all divine discipline is the character of Christ.",
     [("G3810","G3810 — paideutes (trainer/instructor)"),("H4148","H4148 — musar (discipline)")],
     "g3809"),

    ("G3870","Greek","New Testament","παρακαλέω","parakaleo","Verb","to exhort, comfort, urge, encourage",
     "To call alongside — from <em>para</em> (alongside) + <em>kaleo</em> (to call). Used of exhortation, comfort, and urgent appeal. The same root gives us <em>parakletos</em> (Helper/Advocate — the Holy Spirit).",
     "The breadth of parakaleo covers the full range of pastoral ministry: comforting the grieving, exhorting the lazy, urging the reluctant. Paul's letters are full of parakaleo sections (Romans 12 begins one).",
     [("Romans 12:1","I appeal [parakaleo] to you therefore, brothers, by the mercies of God."),
      ("2 Corinthians 1:4","He comforts [parakaleo] us in all our affliction, so that we may comfort [parakaleo] others."),
      ("Hebrews 3:13","<em>Exhort</em> [parakaleo] one another every day.")],
     "2 Corinthians 1:3-7 builds an entire theology from parakaleo: the God of all comfort comforts us so we can comfort others. Comfort received overflows into comfort given — the church as a parakaleo community.",
     [("G3875","G3875 — parakletos (comforter/advocate)"),("G3874","G3874 — paraklesis (encouragement)")],
     "g3870"),

    ("G4043","Greek","New Testament","περιπατέω","peripateo","Verb","to walk, live, conduct oneself",
     "Literally to walk around, but Paul uses it pervasively as a metaphor for how one lives and conducts oneself — 'walking in the Spirit,' 'walking in love,' 'walking in the light.' Life as a sustained direction of travel.",
     "The Pauline 'walk' ethic is dynamic, not static — life is movement, direction, pace. To walk 'worthy' of the gospel means moving in a way consistent with what God has done. Seven 'walks' in Ephesians structure its ethics.",
     [("Galatians 5:16","Walk [peripateo] by the Spirit, and you will not gratify the desires of the flesh."),
      ("Ephesians 2:10","Created in Christ Jesus for good works, which God prepared beforehand, that we should <em>walk</em> [peripateo] in them."),
      ("1 John 1:7","If we walk [peripateo] in the light, as he is in the light, we have fellowship with one another.")],
     "Ephesians alone has seven peripateo calls (2:2, 2:10, 4:1, 4:17, 5:2, 5:8, 5:15). Each describes a dimension of the new life: worthy, in love, in light, in wisdom. The Christian life is a sustained purposeful walk.",
     [("H1980","H1980 — halak (to walk/go)"),("G3598","G3598 — hodos (way/road)")],
     "g4043"),

    ("G4240","Greek","New Testament","πραΰτης","prautes","Noun, feminine","gentleness, meekness, humility",
     "Strength under control — not weakness but power disciplined by love. The meek man is not a pushover but someone who has brought his power under the authority of God. Moses (Num 12:3) and Jesus (Matt 11:29) exemplify this.",
     "Classical Greek used prautes of the tamed horse — full power, fully controlled. The NT applies it to the Christian who has brought their full capacity under Christ's lordship. 'Meek' in English often sounds weak; the Greek is strong.",
     [("Matthew 5:5","<em>Blessed are the meek</em> [prautes], for they shall inherit the earth."),
      ("Galatians 5:23","The fruit of the Spirit is...gentleness [prautes]."),
      ("1 Peter 3:15","In your hearts honor Christ the Lord as holy, always being prepared to give a defense...with gentleness [prautes].")],
     "1 Peter 3:15's apologetic instruction — give a defense with prautes — shows this is not passive silence but active, confident, gentle engagement. The meek can contend without being combative.",
     [("G5012","G5012 — tapeinophrosune (humility)"),("G1933","G1933 — epieikes (gentle/reasonable)")],
     "g4240"),

    ("G4335","Greek","New Testament","προσευχή","proseuche","Noun, feminine","prayer, place of prayer",
     "Prayer — the specific word for directed prayer to God, as distinguished from general petition or intercession. Also used for a place of prayer (Acts 16:13). The core discipline of communion with God.",
     "The NT treats proseuche as conversation with the Father — not merely petition but also praise, confession, and listening. Jesus' teaching on prayer (Matt 6, Luke 11) and Paul's exhortation to pray without ceasing (1 Thess 5:17) shape the whole NT ethic of prayer.",
     [("1 Thessalonians 5:17","Pray [proseuche] without ceasing."),
      ("Philippians 4:6","In everything by prayer [proseuche] and supplication with thanksgiving let your requests be made known to God."),
      ("Acts 16:13","We went outside the gate to the riverside, where we supposed there was a place of prayer [proseuche].")],
     "Philippians 4:6 offers anxiety's antidote: proseuche + deesis (supplication) + eucharistia (thanksgiving). The three together constitute full-orbed prayer — address to God, specific requests, and gratitude.",
     [("G1162","G1162 — deesis (supplication)"),("H8605","H8605 — tephillah (prayer)")],
     "g4335"),

    ("G4487","Greek","New Testament","ῥῆμα","rhema","Noun, neuter","word, saying, utterance",
     "A spoken word or specific utterance — more concrete than logos. 'Man shall not live by bread alone but by every <em>rhema</em> that comes from the mouth of God' (Matt 4:4). Faith comes by hearing, and hearing by the <em>rhema</em> of Christ (Rom 10:17).",
     "While logos can refer to reason and message broadly, rhema emphasizes the specific spoken word. The rhema of God is alive — breathed out (theopneustos) and active in ways that accomplish divine purpose.",
     [("Matthew 4:4","Man shall not live by bread alone, but by every <em>word</em> [rhema] that comes from the mouth of God."),
      ("Romans 10:17","Faith comes from hearing, and hearing through the <em>word</em> [rhema] of Christ."),
      ("Ephesians 6:17","The sword of the Spirit, which is the <em>word</em> [rhema] of God.")],
     "Ephesians 6:17's 'sword of the Spirit' is the rhema of God — the specific, spoken, situational word applied to the moment. Paul pairs it with prayer (6:18), suggesting the Spirit supplies the right word at the right time.",
     [("G3056","G3056 — logos (word/reason)"),("H1697","H1697 — dabar (word)")],
     "g4487"),

    ("G4592","Greek","New Testament","σημεῖον","semeion","Noun, neuter","sign, miracle, portent",
     "A sign that points beyond itself to a greater reality. John calls Jesus' miracles <em>semeia</em> (signs) — they are not ends in themselves but revelations of who Jesus is and what he has come to do.",
     "John's Gospel is structured around seven signs. Each one is both a miracle and a revelation — the feeding of the 5000 signs Jesus as the bread of life; the raising of Lazarus signs Jesus as the resurrection and the life.",
     [("John 20:30-31","Jesus did many other <em>signs</em> [semeion] in the presence of the disciples...but these are written so that you may believe."),
      ("John 2:11","This, the first of his <em>signs</em> [semeion], Jesus did at Cana in Galilee."),
      ("Acts 2:22","A man attested to you by God with mighty works and <em>wonders and signs</em> [semeion].")],
     "John's seven signs form a cumulative argument: signs reveal identity, and identity demands response. The eighth 'sign' is the resurrection — the ultimate sign that vindicates all Jesus claimed to be.",
     [("G5056","G5056 — telos (end/goal)"),("H226","H226 — ot (sign)")],
     "g4592"),

    ("G4716","Greek","New Testament","σταυρός","stauros","Noun, masculine","cross, stake",
     "The Roman cross — instrument of execution and, in Christian theology, the pivot of history. Paul boasts in nothing except the cross (Gal 6:14) and determines to know nothing but Christ crucified (1 Cor 2:2).",
     "The cross was a symbol of shame and defeat in Roman culture. Paul's theology radically inverts this: the cross is the power of God (1 Cor 1:18). The stumbling block to Jews and folly to Greeks is God's wisdom and power.",
     [("1 Corinthians 1:18","The word of the <em>cross</em> [stauros] is folly to those who are perishing, but to us who are being saved it is the power of God."),
      ("Galatians 6:14","Far be it from me to boast except in the <em>cross</em> [stauros] of our Lord Jesus Christ."),
      ("Colossians 1:20","Making peace by the blood of his <em>cross</em> [stauros].")],
     "Colossians 1:20 says God reconciles 'all things' through the blood of the cross — cosmic reconciliation through a Roman execution device. This is the central scandal and glory of the Christian message.",
     [("G2288","G2288 — thanatos (death)"),("G629","G629 — apolutrosis (redemption)")],
     "g4716"),

    ("G5046","Greek","New Testament","τέλειος","teleios","Adjective","perfect, mature, complete, whole",
     "Not sinless perfection but completeness and maturity — having reached the <em>telos</em> (goal/end). James calls perseverance that leads to being teleios 'lacking nothing.' Hebrews contrasts immature and mature faith.",
     "The call to be teleios (Matt 5:48) is not a call to achieve sinlessness but to be complete in love — loving as the Father loves, without partiality or limit. Maturity as the goal of all spiritual formation.",
     [("Matthew 5:48","You therefore must be <em>perfect</em> [teleios], as your heavenly Father is perfect."),
      ("James 1:4","Let steadfastness have its full effect, that you may be <em>perfect</em> [teleios] and complete, lacking in nothing."),
      ("Hebrews 5:14","Solid food is for the mature [teleios], for those who have their powers of discernment trained.")],
     "Paul's use of teleios in Colossians 1:28 — 'presenting everyone mature [teleios] in Christ' — reveals this as the goal of all ministry. The church is not meant to stay in infancy but to grow to the fullness of Christ.",
     [("G5056","G5056 — telos (end/goal)"),("G3516","G3516 — nepios (infant/immature)")],
     "g5046"),

    ("G5207","Greek","New Testament","\u03c5\u1f31\u03cc\u03c2","huios","Noun, masculine","son, descendant, heir",
     "Son in both biological and covenantal senses. Jesus is the Son of God \u2014 a relational title expressing unique divine relationship and messianic identity. Believers become sons through adoption (huiothesia).",
     "The title Son of God is primarily relational and covenantal. Hebrews 1 argues the Son's superiority to angels; John 1 identifies him as the eternal Son. Adoption makes believers full heirs.",
     [("Matthew 3:17","This is my beloved <em>Son</em> [huios], with whom I am well pleased."),
      ("Galatians 4:4-5","God sent forth his <em>Son</em> [huios]...so that we might receive adoption as <em>sons</em> [huios]."),
      ("Romans 8:14","For all who are led by the Spirit of God are <em>sons</em> [huios] of God.")],
     "Galatians 4:4-5 is the gospel in miniature: Son sent, born under law, to redeem, to adopt. We become sons because he became the Son incarnate.",
     [("G5043","G5043 \u2014 teknon (child)"),("G2316","G2316 \u2014 theos (God)")],
     "g5207"),

    ("G5293","Greek","New Testament","\u1f51\u03c0\u03bf\u03c4\u03ac\u03c3\u03c3\u03c9","hupotasso","Verb","to submit, be subject to, subordinate",
     "To arrange under \u2014 a military term for ordering troops under a commander. Used of wives/husbands, citizens/government, Jesus/Father. Submission is relational order, not ontological inferiority.",
     "The NT submission ethic is rooted in the Trinity: the Son submits to the Father not because he is less divine but as a relational pattern. Mutual submission (Eph 5:21) precedes all specific applications.",
     [("Ephesians 5:21","<em>Submitting</em> [hupotasso] to one another out of reverence for Christ."),
      ("Romans 13:1","Let every person be <em>subject</em> [hupotasso] to the governing authorities."),
      ("1 Corinthians 15:28","The Son himself will also be <em>subjected</em> [hupotasso] to him who put all things in subjection under him.")],
     "1 Corinthians 15:28 \u2014 the Son's eternal submission \u2014 is relational order in the eschatological kingdom. Submission in the NT is always voluntary, purposeful, and dignifying.",
     [("G5218","G5218 \u2014 hupakoe (obedience)"),("G1849","G1849 \u2014 exousia (authority)")],
     "g5293"),
]


def make_page(strongs, lang, testament, original, translit, pos, gloss,
              definition, usage, verses, word_study, related, blb_id):
    lang_label = "Hebrew" if lang == "Hebrew" else "Greek"
    ext_links = f'''<a href="https://www.stepbible.org/?q=strong={strongs}" target="_blank" class="ext-link">\U0001f4d6 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/{blb_id}/kjv/tr/0-1/" target="_blank" class="ext-link">\U0001f4d8 Blue Letter Bible</a>'''

    verse_html = ""
    for ref, text in verses:
        url_ref = ref.replace(" ", "+")
        verse_html += f"""
                <div class="verse-entry">
                    <a href="../bible.html?ref={url_ref}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>"""

    related_html = ""
    for rid, rlabel in related:
        related_html += f'<a href="{rid}.html" class="related-word">{rlabel}</a>\n                    '

    css = """* { margin:0; padding:0; box-sizing:border-box; }
        :root { --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }
        body { font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }
        h1,h2,h3 { font-family:'Playfair Display',serif; font-weight:700; }
        .container { max-width:800px; margin:0 auto; padding:20px; }
        nav { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }
        nav a { color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }
        nav a:hover { color:var(--gold); border-color:var(--border); }
        nav a:link,nav a:visited,nav a:active { color:var(--gray) !important; text-decoration:none !important; }
        nav a.active { color:var(--gold) !important; border-color:var(--gold); }
        .word-header { text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }
        .strongs-badge { display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }
        .original-word { font-size:3rem; margin:15px 0 10px; color:var(--gold-light); direction:ltr; }
        .transliteration { font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }
        .pos { color:var(--gray); font-size:0.95rem; margin-bottom:10px; }
        .gloss { color:var(--gold); font-size:1.1rem; font-weight:600; }
        .section { background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }
        .section h2 { color:var(--gold); font-size:1.3rem; margin-bottom:16px; }
        .section p { color:var(--gray); line-height:1.8; margin-bottom:12px; }
        .section p em { color:var(--gold-light); font-style:italic; }
        .section p strong { color:var(--white); }
        .verse-entry { margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }
        .verse-ref { color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:block; margin-bottom:4px; border-bottom:1px dotted var(--gold); display:inline-block; }
        .verse-ref:hover { color:var(--gold-light); border-bottom-style:solid; }
        .verse-text { color:var(--gray); line-height:1.7; }
        .verse-text em { color:var(--gold-light); font-style:italic; }
        .verse-text strong { color:var(--white); }
        .related-words { display:flex; flex-wrap:wrap; gap:10px; }
        .related-word { display:inline-block; background:rgba(212,175,55,0.1); border:1px solid var(--border); color:var(--gold); text-decoration:none; padding:6px 14px; border-radius:20px; font-size:0.85rem; transition:all 0.2s; }
        a.related-word:hover { border-color:var(--gold); background:rgba(212,175,55,0.2); }
        .ext-links { display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }
        .ext-link { color:var(--gold); text-decoration:none; padding:8px 18px; border:1px solid var(--border); border-radius:8px; font-size:0.9rem; transition:all 0.2s; }
        .ext-link:hover { border-color:var(--gold); background:rgba(212,175,55,0.1); }
        .back-link { display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }
        .back-link:hover { color:var(--gold-light); }
        footer { text-align:center; padding:40px 20px; color:var(--gray); font-size:0.85rem; border-top:1px solid var(--border); margin-top:40px; }
        footer a { color:var(--gold); text-decoration:none; }
        @media (max-width:640px) { .container { padding:15px; } .original-word { font-size:2.2rem; } }"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{strongs} \u2014 {translit} | USMC Ministries Lexicon">
    <meta property="og:description" content="{gloss} \u2014 {lang_label} word study. Strong's {strongs}.">
    <meta name="description" content="{gloss} \u2014 {lang_label} word study. Strong's {strongs}. USMC Ministries Lexicon.">
    <title>{strongs} \u2014 {translit} ({gloss}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div class="container">
        <a href="../lexicon.html" class="back-link">\u2190 Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">{strongs} \u00b7 {lang_label} \u00b7 {testament}</span>
            <div class="original-word">{original}</div>
            <div class="transliteration">{translit}</div>
            <div class="pos">{pos}</div>
            <div class="gloss">{gloss}</div>
        </div>
        <div class="section"><h2>Definition</h2><p>{definition}</p></div>
        <div class="section"><h2>Usage &amp; Theological Significance</h2><p>{usage}</p></div>
        <div class="section"><h2>Key Bible Verses</h2>{verse_html}</div>
        <div class="section"><h2>Word Study</h2><p>{word_study}</p></div>
        <div class="section"><h2>Related Words</h2><div class="related-words">{related_html}</div></div>
        <div class="section"><h2>External Resources</h2><div class="ext-links">{ext_links}</div></div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">\u00a9 2026 <a href="../index.html">U.S.M.C. Ministries</a> \u00b7 <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
</body>
</html>"""

OUT = "/Users/adamjohns/bible-reading-plan-bot/docs/lexicon"
count = 0
for w in WORDS:
    strongs = w[0]
    path = os.path.join(OUT, f"{strongs}.html")
    page = make_page(*w)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    count += 1

print(f"Generated {count} pages in {OUT}")
