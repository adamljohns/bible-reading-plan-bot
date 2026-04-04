#!/usr/bin/env python3
"""Generate 47 lexicon pages: 24 Hebrew + 23 Greek."""
import os

LEXICON_DIR = os.path.expanduser("~/bible-reading-plan-bot/docs/lexicon")

# Word data: each is a dict with strongs, lang, testament, dir, original, translit, pos, short_def, full_def, theology, verses, related
WORDS = []

def add(s, lang, testament, d, orig, trans, pos, sdef, fdef, theo, verses, related):
    WORDS.append({"strongs":s,"lang":lang,"testament":testament,"dir":d,
        "original":orig,"translit":trans,"pos":pos,"short_def":sdef,
        "full_def":fdef,"theology":theo,"verses":verses,"related":related})

# === 24 HEBREW ===
add("H8415","Hebrew","Old Testament","rtl","תְּהוֹם","t'hom","Noun, Feminine/Masculine",
    "Deep, abyss, primeval ocean",
    "From an unused root meaning to be deep. Refers to the primordial deep, the vast chaotic waters before creation. It appears at the very beginning of Scripture in Genesis 1:2 — 'darkness was upon the face of the deep.' Also refers to underground springs, ocean depths, and overwhelming forces of chaos that only God can master.",
    "<em>T'hom</em> is one of the most evocative words in the Hebrew Bible. In Genesis 1:2, the Spirit of God hovers over the <em>t'hom</em>, bringing order from chaos. This imagery recurs throughout Scripture — God controls the deep (Psalm 104:6), the deep erupts in judgment (Genesis 7:11), and the deep obeys God's voice (Habakkuk 3:10). God alone has authority over the chaotic forces of creation.",
    [("Genesis 1:2","https://www.blueletterbible.org/kjv/gen/1/2/s_1002","And the earth was without form, and void; and darkness was upon the face of the <strong>deep</strong>. And the Spirit of God moved upon the face of the waters."),
     ("Genesis 7:11","https://www.blueletterbible.org/kjv/gen/7/11/s_7011","...the same day were all the fountains of the great <strong>deep</strong> broken up, and the windows of heaven were opened."),
     ("Psalm 33:7","https://www.blueletterbible.org/kjv/psa/33/7/s_511007","He gathereth the waters of the sea together as an heap: he layeth up the <strong>depth</strong> in storehouses."),
     ("Psalm 104:6","https://www.blueletterbible.org/kjv/psa/104/6/s_582006","Thou coveredst it with the <strong>deep</strong> as with a garment: the waters stood above the mountains."),
     ("Habakkuk 3:10","https://www.blueletterbible.org/kjv/hab/3/10/s_906010","The mountains saw thee, and they trembled... the <strong>deep</strong> uttered his voice, and lifted up his hands on high.")],
    [("H4325","mayim (water)"),("H3220","yam (sea)"),("H7585","sh'ol (Sheol)")])

add("H8454","Hebrew","Old Testament","rtl","תּוּשִׁיָּה","tushiyyah","Noun, Feminine",
    "Sound wisdom, effective counsel, abiding success",
    "From an unused root meaning to be firm. Denotes practical, effective wisdom — not merely theoretical knowledge but the kind of insight that produces lasting results.",
    "<em>Tushiyyah</em> appears almost exclusively in Job and Proverbs. It represents something deeper than cleverness: substantial, enduring wisdom that comes from God alone (Job 12:16). Proverbs 2:7 says God 'layeth up sound wisdom for the righteous.' This is wisdom as a treasure — stored, guarded, and dispensed by God to those who fear Him.",
    [("Job 5:12","https://www.blueletterbible.org/kjv/job/5/12/s_441012","He disappointeth the devices of the crafty, so that their hands cannot perform their <strong>enterprise</strong>."),
     ("Job 12:16","https://www.blueletterbible.org/kjv/job/12/16/s_448016","With him is strength and <strong>wisdom</strong>: the deceived and the deceiver are his."),
     ("Proverbs 2:7","https://www.blueletterbible.org/kjv/pro/2/7/s_630007","He layeth up <strong>sound wisdom</strong> for the righteous: he is a buckler to them that walk uprightly."),
     ("Proverbs 3:21","https://www.blueletterbible.org/kjv/pro/3/21/s_631021","My son, let not them depart from thine eyes: keep <strong>sound wisdom</strong> and discretion:"),
     ("Isaiah 28:29","https://www.blueletterbible.org/kjv/isa/28/29/s_707029","This also cometh forth from the LORD of hosts, which is wonderful in <strong>counsel</strong>, and excellent in working.")],
    [("H2451","chokmah (wisdom)"),("H998","biynah (understanding)"),("H6098","etsah (counsel)")])

add("H5637","Hebrew","Old Testament","rtl","סָרַר","sarar","Verb",
    "To be stubborn, rebellious, backsliding",
    "A primitive root meaning to turn away, be refractory or rebellious. Used to describe Israel's persistent pattern of turning from God. Often used of a stubborn ox or rebellious child.",
    "<em>Sarar</em> is the verb of willful apostasy. Hosea 4:16 compares Israel to a 'backsliding heifer.' Jeremiah uses it repeatedly. The word implies rebellion is not a single act but a settled posture. The antidote is <em>shub</em> (return/repent).",
    [("Deuteronomy 21:18","https://www.blueletterbible.org/kjv/deu/21/18/s_174018","If a man have a <strong>stubborn</strong> and rebellious son, which will not obey the voice of his father..."),
     ("Psalm 66:7","https://www.blueletterbible.org/kjv/psa/66/7/s_544007","He ruleth by his power for ever; his eyes behold the nations: let not the <strong>rebellious</strong> exalt themselves."),
     ("Psalm 78:8","https://www.blueletterbible.org/kjv/psa/78/8/s_556008","And might not be as their fathers, a <strong>stubborn</strong> and rebellious generation..."),
     ("Hosea 4:16","https://www.blueletterbible.org/kjv/hos/4/16/s_866016","For Israel slideth back as a <strong>backsliding</strong> heifer..."),
     ("Jeremiah 5:23","https://www.blueletterbible.org/kjv/jer/5/23/s_650023","But this people hath a revolting and a <strong>rebellious</strong> heart; they are revolted and gone.")],
    [("H4784","marah (to be rebellious)"),("H7725","shub (to return, repent)"),("H6586","pasha (to rebel)")])

add("H6486","Hebrew","Old Testament","rtl","פְּקֻדָּה","p'quddah","Noun, Feminine",
    "Visitation, oversight, charge, punishment",
    "From H6485 (paqad). Refers to the act of visitation — whether for blessing or judgment. Also used for an office of oversight or stewardship.",
    "<em>P'quddah</em> captures one of the OT's most dynamic concepts: God's visitation. When God visits, everything changes. In Isaiah 10:3, the 'day of visitation' is accountability. In Numbers 3:36, it describes a stewardship charge. God is never passive — He observes, intervenes, and holds accountable.",
    [("Numbers 3:36","https://www.blueletterbible.org/kjv/num/3/36/s_120036","And under the custody and <strong>charge</strong> of the sons of Merari..."),
     ("Isaiah 10:3","https://www.blueletterbible.org/kjv/isa/10/3/s_689003","And what will ye do in the day of <strong>visitation</strong>..."),
     ("Jeremiah 8:12","https://www.blueletterbible.org/kjv/jer/8/12/s_653012","...in the time of their <strong>visitation</strong> they shall be cast down, saith the LORD."),
     ("Ezekiel 9:1","https://www.blueletterbible.org/kjv/eze/9/1/s_811001","...Cause them that have <strong>charge</strong> over the city to draw near..."),
     ("Job 10:12","https://www.blueletterbible.org/kjv/job/10/12/s_446012","Thou hast granted me life and favour, and thy <strong>visitation</strong> hath preserved my spirit.")],
    [("H6485","paqad (to visit, attend to)"),("H4931","mishmereth (guard, charge)"),("H3117","yom (day)")])

add("H7603","Hebrew","Old Testament","rtl","שְׂאֹר","s'or","Noun, Masculine",
    "Leaven, yeast",
    "From H7604 (sha'ar, to remain). Leaven — fermented dough that causes bread to rise. Strictly prohibited during Passover and the Feast of Unleavened Bread.",
    "<em>S'or</em> carries enormous symbolic weight. The removal of leaven during Passover symbolized urgency and purity. Leaven represents corruption — the 'puffing up' of what should remain simple. Jesus picks up this imagery: 'Beware of the leaven of the Pharisees.' Paul: 'A little leaven leaveneth the whole lump.'",
    [("Exodus 12:15","https://www.blueletterbible.org/kjv/exo/12/15/s_62015","Seven days shall ye eat unleavened bread; even the first day ye shall put away <strong>leaven</strong> out of your houses..."),
     ("Exodus 13:7","https://www.blueletterbible.org/kjv/exo/13/7/s_63007","...there shall no leavened bread be seen with thee, neither shall there be <strong>leaven</strong> seen with thee..."),
     ("Leviticus 2:11","https://www.blueletterbible.org/kjv/lev/2/11/s_92011","No meat offering...shall be made with <strong>leaven</strong>..."),
     ("Deuteronomy 16:4","https://www.blueletterbible.org/kjv/deu/16/4/s_169004","And there shall be no <strong>leavened bread</strong> seen with thee in all thy coast seven days..."),
     ("Exodus 34:25","https://www.blueletterbible.org/kjv/exo/34/25/s_84025","Thou shalt not offer the blood of my sacrifice with <strong>leaven</strong>...")],
    [("H4682","matstsah (unleavened bread)"),("H2557","chamets (leavened)"),("H6174","arom (naked, exposed)")])

add("H2441","Hebrew","Old Testament","rtl","חֵךְ","chek","Noun, Masculine",
    "Palate, roof of the mouth, taste",
    "The palate or roof of the mouth, and by extension, the faculty of taste and discernment. Used literally and figuratively for spiritual discernment.",
    "<em>Chek</em> bridges the physical and spiritual senses. Job 12:11: 'Doth not the ear try words? and the mouth taste his meat?' The Psalmist exclaims, 'How sweet are thy words unto my taste!' (Psalm 119:103). Knowing God is experiential, sensory, intimate.",
    [("Job 6:30","https://www.blueletterbible.org/kjv/job/6/30/s_442030","Is there iniquity in my tongue? cannot my <strong>taste</strong> discern perverse things?"),
     ("Job 12:11","https://www.blueletterbible.org/kjv/job/12/11/s_448011","Doth not the ear try words? and the <strong>mouth taste</strong> his meat?"),
     ("Job 34:3","https://www.blueletterbible.org/kjv/job/34/3/s_470003","For the ear trieth words, as the <strong>mouth tasteth</strong> meat."),
     ("Psalm 119:103","https://www.blueletterbible.org/kjv/psa/119/103/s_597103","How sweet are thy words unto my <strong>taste</strong>! yea, sweeter than honey to my mouth!"),
     ("Proverbs 8:7","https://www.blueletterbible.org/kjv/pro/8/7/s_636007","For my <strong>mouth</strong> shall speak truth; and wickedness is an abomination to my lips.")],
    [("H2940","taam (taste, perception)"),("H3956","lashon (tongue)"),("H6310","peh (mouth)")])

add("H2789","Hebrew","Old Testament","rtl","חֶרֶשׂ","cheres","Noun, Masculine",
    "Earthenware, potsherd, pottery",
    "An earthen vessel, pottery, or potsherd — a broken piece of clay. Used literally and figuratively for human frailty.",
    "<em>Cheres</em> is the word of human fragility. Job scrapes sores with a potsherd. Isaiah 45:9: 'Let the potsherd strive with the potsherds of the earth.' Paul echoes: 'We have this treasure in earthen vessels.' The weakness of the vessel magnifies the power of the Maker.",
    [("Job 2:8","https://www.blueletterbible.org/kjv/job/2/8/s_438008","And he took him a <strong>potsherd</strong> to scrape himself withal..."),
     ("Psalm 22:15","https://www.blueletterbible.org/kjv/psa/22/15/s_500015","My strength is dried up like a <strong>potsherd</strong>..."),
     ("Isaiah 45:9","https://www.blueletterbible.org/kjv/isa/45/9/s_724009","Woe unto him that striveth with his Maker! Let the <strong>potsherd</strong> strive with the potsherds of the earth."),
     ("Proverbs 26:23","https://www.blueletterbible.org/kjv/pro/26/23/s_654023","Burning lips and a wicked heart are like a <strong>potsherd</strong> covered with silver dross."),
     ("Leviticus 6:28","https://www.blueletterbible.org/kjv/lev/6/28/s_96028","But the <strong>earthen vessel</strong> wherein it is sodden shall be broken...")],
    [("H3335","yatsar (to form, fashion)"),("H2563","chomer (clay)"),("H5035","nebel (flask)")])

add("H3335","Hebrew","Old Testament","rtl","יָצַר","yatsar","Verb",
    "To form, fashion, frame",
    "A primitive root meaning to form or shape — as a potter forms clay. The word used in Genesis 2:7 when God 'formed' man from the dust.",
    "<em>Yatsar</em> is the artist's word for creation. While <em>bara</em> emphasizes creating from nothing, <em>yatsar</em> emphasizes hands-on craftsmanship. In Genesis 2:7, God forms Adam like a potter with clay, then breathes life into his nostrils. Isaiah develops the potter/clay metaphor extensively. We are not accidents — we are artisan-crafted.",
    [("Genesis 2:7","https://www.blueletterbible.org/kjv/gen/2/7/s_2007","And the LORD God <strong>formed</strong> man of the dust of the ground, and breathed into his nostrils the breath of life."),
     ("Genesis 2:19","https://www.blueletterbible.org/kjv/gen/2/19/s_2019","And out of the ground the LORD God <strong>formed</strong> every beast of the field..."),
     ("Isaiah 43:1","https://www.blueletterbible.org/kjv/isa/43/1/s_722001","...he that <strong>formed</strong> thee, O Israel, Fear not: for I have redeemed thee."),
     ("Isaiah 64:8","https://www.blueletterbible.org/kjv/isa/64/8/s_743008","...we are the clay, and thou our <strong>potter</strong>; and we all are the work of thy hand."),
     ("Jeremiah 18:4","https://www.blueletterbible.org/kjv/jer/18/4/s_663004","And the vessel that he made of clay was marred in the hand of the <strong>potter</strong>...")],
    [("H1254","bara (to create)"),("H6213","asah (to make)"),("H2789","cheres (pottery)")])

add("H3332","Hebrew","Old Testament","rtl","יָצַק","yatsaq","Verb",
    "To pour, pour out, cast (metal)",
    "A primitive root meaning to pour or pour out. Used of pouring liquids, casting molten metal, and figuratively of divine outpouring.",
    "<em>Yatsaq</em> connects the physical and spiritual. Oil poured for anointing (1 Samuel 10:1). Blood poured at the altar. Water poured as a drink offering. Every act of pouring in the OT points to the lavish generosity of God.",
    [("1 Samuel 10:1","https://www.blueletterbible.org/kjv/1sa/10/1/s_246001","Then Samuel took a vial of oil, and <strong>poured</strong> it upon his head..."),
     ("1 Kings 7:46","https://www.blueletterbible.org/kjv/1ki/7/46/s_298046","In the plain of Jordan did the king <strong>cast</strong> them, in the clay ground..."),
     ("2 Kings 4:5","https://www.blueletterbible.org/kjv/2ki/4/5/s_317005","...she <strong>poured out</strong>."),
     ("Job 29:6","https://www.blueletterbible.org/kjv/job/29/6/s_465006","...the rock <strong>poured</strong> me out rivers of oil..."),
     ("Leviticus 8:12","https://www.blueletterbible.org/kjv/lev/8/12/s_98012","And he <strong>poured</strong> of the anointing oil upon Aaron's head...")],
    [("H8210","shaphak (to pour out)"),("H5258","nasak (to pour out, cast)"),("H4886","mashach (to anoint)")])

add("H4341","Hebrew","Old Testament","rtl","מַכְאוֹב","mak'ob","Noun, Masculine",
    "Pain, sorrow, suffering",
    "From H3510 (ka'ab). Physical pain, mental anguish, or deep sorrow. Used of human suffering and the Messiah's prophetic suffering.",
    "<em>Mak'ob</em> reaches its summit in Isaiah 53:3-4: the Suffering Servant is 'a man of sorrows, and acquainted with grief.' The Messiah intimately knows pain — not theoretical awareness but experiential identification. The Bible's honest engagement with suffering is captured in this word.",
    [("Isaiah 53:3","https://www.blueletterbible.org/kjv/isa/53/3/s_732003","He is despised and rejected of men; a man of <strong>sorrows</strong>, and acquainted with grief..."),
     ("Isaiah 53:4","https://www.blueletterbible.org/kjv/isa/53/4/s_732004","Surely he hath borne our <strong>griefs</strong>, and carried our sorrows..."),
     ("Ecclesiastes 1:18","https://www.blueletterbible.org/kjv/ecc/1/18/s_660018","For in much wisdom is much grief: and he that increaseth knowledge increaseth <strong>sorrow</strong>."),
     ("Psalm 32:10","https://www.blueletterbible.org/kjv/psa/32/10/s_510010","Many <strong>sorrows</strong> shall be to the wicked..."),
     ("Job 33:19","https://www.blueletterbible.org/kjv/job/33/19/s_469019","He is chastened also with <strong>pain</strong> upon his bed...")],
    [("H3510","ka'ab (to be in pain)"),("H3015","yagon (grief)"),("H6089","etseb (pain, toil)")])

add("H5526","Hebrew","Old Testament","rtl","סָכַךְ","sakak","Verb",
    "To cover, screen, hedge in, protect",
    "A primitive root meaning to cover over, hedge about, screen or protect. Used of God covering the mercy seat, shielding His people, and the cherubim covering the ark.",
    "<em>Sakak</em> is the verb of divine protection. The cherubim 'covered' the mercy seat (Exodus 25:20). Psalm 91:4: God 'shall cover thee with his feathers.' Exodus 33:22: God covers Moses with His hand. God screens His people from destruction and covers their sin with mercy.",
    [("Exodus 25:20","https://www.blueletterbible.org/kjv/exo/25/20/s_75020","And the cherubims shall stretch forth their wings on high, <strong>covering</strong> the mercy seat..."),
     ("Exodus 33:22","https://www.blueletterbible.org/kjv/exo/33/22/s_83022","...I will put thee in a clift of the rock, and will <strong>cover</strong> thee with my hand while I pass by."),
     ("Psalm 91:4","https://www.blueletterbible.org/kjv/psa/91/4/s_569004","He shall <strong>cover</strong> thee with his feathers, and under his wings shalt thou trust..."),
     ("Psalm 140:7","https://www.blueletterbible.org/kjv/psa/140/7/s_618007","...thou hast <strong>covered</strong> my head in the day of battle."),
     ("Job 3:23","https://www.blueletterbible.org/kjv/job/3/23/s_439023","Why is light given to a man whose way is <strong>hid</strong>, and whom God hath hedged in?")],
    [("H3680","kasah (to cover)"),("H5643","sether (shelter)"),("H6822","tsaphah (to watch)")])

add("H7401","Hebrew","Old Testament","rtl","רָכַךְ","rakak","Verb",
    "To be tender, soft, weak, gentle",
    "A primitive root meaning to be tender, soft, or delicate. When applied to the heart, it describes responsiveness to God — the opposite of hardness.",
    "<em>Rakak</em> holds one of the most beautiful OT moments. When Josiah hears the Law read aloud, God says: 'Because thine heart was tender...I also have heard thee' (2 Kings 22:19). A tender heart is God's prerequisite for hearing. God doesn't need strong people — He needs soft ones.",
    [("2 Kings 22:19","https://www.blueletterbible.org/kjv/2ki/22/19/s_335019","Because thine heart was <strong>tender</strong>, and thou hast humbled thyself before the LORD...I also have heard thee."),
     ("2 Chronicles 34:27","https://www.blueletterbible.org/kjv/2ch/34/27/s_401027","Because thine heart was <strong>tender</strong>..."),
     ("Deuteronomy 20:3","https://www.blueletterbible.org/kjv/deu/20/3/s_173003","...let not your hearts <strong>faint</strong>..."),
     ("Isaiah 7:4","https://www.blueletterbible.org/kjv/isa/7/4/s_686004","...fear not, neither be <strong>fainthearted</strong>..."),
     ("Genesis 33:13","https://www.blueletterbible.org/kjv/gen/33/13/s_33013","...the children are <strong>tender</strong>...")],
    [("H3824","lebab (heart)"),("H6031","anah (to humble)"),("H7390","rak (tender)")])

add("H2021","Hebrew","Old Testament","rtl","הֹצֶן","hotsen","Noun, Masculine",
    "Weapon, arms, military equipment",
    "From an unused root meaning to be sharp. Refers to weapons of war or instruments of battle. A rare but vivid word in prophetic contexts.",
    "Though rare, <em>hotsen</em> appears where Scripture addresses the futility of human military power. Ezekiel 39:9 describes weapons of Gog becoming fuel for fire. The theological message: human weapons fail; God's power alone is decisive. True security comes from the LORD of hosts.",
    [("Ezekiel 39:9","https://www.blueletterbible.org/kjv/eze/39/9/s_841009","...they shall set on fire and burn the <strong>weapons</strong>..."),
     ("Ezekiel 39:10","https://www.blueletterbible.org/kjv/eze/39/10/s_841010","...they shall burn the <strong>weapons</strong> with fire..."),
     ("Isaiah 2:4","https://www.blueletterbible.org/kjv/isa/2/4/s_681004","...they shall beat their swords into plowshares..."),
     ("Psalm 46:9","https://www.blueletterbible.org/kjv/psa/46/9/s_524009","He maketh wars to cease...he breaketh the bow, and cutteth the spear in sunder..."),
     ("Psalm 44:6","https://www.blueletterbible.org/kjv/psa/44/6/s_522006","For I will not trust in my bow, neither shall my sword save me.")],
    [("H2719","chereb (sword)"),("H7198","qesheth (bow)"),("H3627","k'liy (instrument)")])

add("H2724","Hebrew","Old Testament","rtl","חָרָבָה","charabah","Noun, Feminine",
    "Dry land, dry ground",
    "From H2717 (charab). Dry land as opposed to water — especially the miraculous dry ground when God parted the waters.",
    "<em>Charabah</em> is the word of miraculous deliverance. Israel crosses the Red Sea on dry ground (Exodus 14:21). They cross the Jordan on dry ground (Joshua 3:17). This connects creation (God separating waters from dry land) with redemption (God making a way through waters). Every time God makes dry ground appear, He is re-creating the world for His people.",
    [("Genesis 1:9","https://www.blueletterbible.org/kjv/gen/1/9/s_1009","...let the <strong>dry land</strong> appear."),
     ("Exodus 14:21","https://www.blueletterbible.org/kjv/exo/14/21/s_64021","...made the sea <strong>dry land</strong>, and the waters were divided."),
     ("Joshua 3:17","https://www.blueletterbible.org/kjv/jos/3/17/s_190017","...stood firm on <strong>dry ground</strong> in the midst of Jordan..."),
     ("2 Kings 2:8","https://www.blueletterbible.org/kjv/2ki/2/8/s_315008","...they two went over on <strong>dry ground</strong>."),
     ("Haggai 2:6","https://www.blueletterbible.org/kjv/hag/2/6/s_910006","...I will shake the heavens, and the earth, and the sea, and the <strong>dry land</strong>.")],
    [("H3004","yabbashah (dry land)"),("H4057","midbar (wilderness)"),("H4325","mayim (water)")])

add("H5710","Hebrew","Old Testament","rtl","עָדָה","adah","Verb",
    "To adorn, deck oneself, put on ornaments",
    "A primitive root meaning to adorn or put on ornaments. Used literally of wearing jewelry and figuratively of God adorning Jerusalem.",
    "<em>Adah</em> carries deeply relational theology. In Ezekiel 16:11-13, God adorned orphaned Jerusalem with bracelets, chains, and a crown — the language of covenant love. The tragedy: Israel used these adornments to attract other lovers (Hosea 2:13). Yet the promise remains: God will adorn His people again (Isaiah 61:10).",
    [("Ezekiel 16:11","https://www.blueletterbible.org/kjv/eze/16/11/s_818011","I <strong>decked</strong> thee also with ornaments..."),
     ("Ezekiel 16:13","https://www.blueletterbible.org/kjv/eze/16/13/s_818013","Thus wast thou <strong>decked</strong> with gold and silver..."),
     ("Hosea 2:13","https://www.blueletterbible.org/kjv/hos/2/13/s_864013","...she <strong>decked</strong> herself with her earrings and her jewels..."),
     ("Jeremiah 4:30","https://www.blueletterbible.org/kjv/jer/4/30/s_649030","...though thou <strong>clothest</strong> thyself with crimson, though thou deckest thee with ornaments..."),
     ("Isaiah 61:10","https://www.blueletterbible.org/kjv/isa/61/10/s_740010","...as a bridegroom <strong>decketh</strong> himself with ornaments...")],
    [("H5716","adiy (ornament)"),("H3847","labash (to wear)"),("H8597","tiph'arah (beauty)")])

add("H3344","Hebrew","Old Testament","rtl","יָקַד","yaqad","Verb",
    "To kindle, burn, be burning",
    "A primitive root meaning to burn, kindle, or be ablaze. Used of literal fire and figuratively of divine judgment and purification.",
    "<em>Yaqad</em> appears in contexts of both judgment and revelation. In Deuteronomy 32:22, God's anger kindles fire to the lowest Sheol. The theological spectrum of fire runs from wrath to worship: the same fire that destroys also purifies. 'For our God is a consuming fire.'",
    [("Deuteronomy 32:22","https://www.blueletterbible.org/kjv/deu/32/22/s_185022","For a fire is <strong>kindled</strong> in mine anger, and shall burn unto the lowest hell..."),
     ("Isaiah 10:16","https://www.blueletterbible.org/kjv/isa/10/16/s_689016","...under his glory he shall <strong>kindle</strong> a burning like the burning of a fire."),
     ("Isaiah 30:14","https://www.blueletterbible.org/kjv/isa/30/14/s_709014","...a sherd to take fire from the <strong>hearth</strong>."),
     ("Jeremiah 15:14","https://www.blueletterbible.org/kjv/jer/15/14/s_660014","...a fire is <strong>kindled</strong> in mine anger, which shall burn upon you."),
     ("Leviticus 6:12","https://www.blueletterbible.org/kjv/lev/6/12/s_96012","And the fire upon the altar shall be <strong>burning</strong> in it; it shall not be put out...")],
    [("H784","esh (fire)"),("H1197","ba'ar (to burn)"),("H3857","lahat (to blaze)")])

add("H5549","Hebrew","Old Testament","rtl","סָלַל","salal","Verb",
    "To lift up, cast up, exalt, build a highway",
    "A primitive root meaning to lift up or heap up. Particularly used for building a road — clearing and raising a path through difficult terrain.",
    "<em>Salal</em> is behind one of the prophets' most stirring images: the highway of God. Isaiah 57:14: 'Cast ye up, prepare the way.' Isaiah 62:10 repeats. God is the ultimate road-builder. John the Baptist's ministry is previewed: 'Prepare ye the way of the LORD.' Every act of divine preparation is an act of <em>salal</em>.",
    [("Isaiah 57:14","https://www.blueletterbible.org/kjv/isa/57/14/s_736014","And shall say, <strong>Cast ye up, cast ye up</strong>, prepare the way..."),
     ("Isaiah 62:10","https://www.blueletterbible.org/kjv/isa/62/10/s_741010","...<strong>cast up, cast up the highway</strong>; gather out the stones..."),
     ("Psalm 68:4","https://www.blueletterbible.org/kjv/psa/68/4/s_546004","Sing unto God, sing praises to his name: <strong>extol</strong> him that rideth upon the heavens..."),
     ("Proverbs 15:19","https://www.blueletterbible.org/kjv/pro/15/19/s_643019","...the way of the righteous is made <strong>plain</strong>."),
     ("Job 19:12","https://www.blueletterbible.org/kjv/job/19/12/s_455012","His troops come together, and <strong>raise up their way</strong> against me...")],
    [("H4546","m'sillah (highway)"),("H6437","panah (to turn, prepare)"),("H3474","yashar (to be straight)")])

add("H6225","Hebrew","Old Testament","rtl","עָשַׁן","ashan","Verb",
    "To smoke, to be angry, to fume",
    "A primitive root meaning to smoke or send up smoke. Used literally of mountains smoking in God's presence and figuratively of God's anger.",
    "<em>Ashan</em> connects God's fearsome presence and righteous anger. When God descends on Sinai, the mount smoked (Exodus 19:18). When God's anger burns, His nostrils 'smoke' (Psalm 74:1). Fire and smoke mark every theophany because God's presence exposes and consumes what is impure.",
    [("Exodus 19:18","https://www.blueletterbible.org/kjv/exo/19/18/s_69018","And mount Sinai was altogether on a <strong>smoke</strong>..."),
     ("Psalm 74:1","https://www.blueletterbible.org/kjv/psa/74/1/s_552001","...why doth thine anger <strong>smoke</strong> against the sheep of thy pasture?"),
     ("Psalm 104:32","https://www.blueletterbible.org/kjv/psa/104/32/s_582032","...he toucheth the hills, and they <strong>smoke</strong>."),
     ("Psalm 144:5","https://www.blueletterbible.org/kjv/psa/144/5/s_622005","...touch the mountains, and they shall <strong>smoke</strong>."),
     ("Deuteronomy 29:20","https://www.blueletterbible.org/kjv/deu/29/20/s_182020","...the anger of the LORD and his jealousy shall <strong>smoke</strong> against that man...")],
    [("H784","esh (fire)"),("H6227","ashan (smoke)"),("H639","aph (anger)")])

add("H7411","Hebrew","Old Testament","rtl","רָמָה","ramah","Verb",
    "To deceive, beguile, deal treacherously",
    "A primitive root meaning to hurl — and by extension, to deceive or beguile. Used of human deception, fraud, and treachery.",
    "<em>Ramah</em> carries the weight of betrayal. In Genesis 29:25, Jacob confronts Laban: 'Wherefore hast thou beguiled me?' — the deceiver being deceived. Exodus 15:1 uses the same root for God's triumph. Those who deceive others are ultimately overthrown by God.",
    [("Genesis 29:25","https://www.blueletterbible.org/kjv/gen/29/25/s_29025","...wherefore then hast thou <strong>beguiled</strong> me?"),
     ("Exodus 15:1","https://www.blueletterbible.org/kjv/exo/15/1/s_65001","...the horse and his rider hath he <strong>thrown</strong> into the sea."),
     ("1 Samuel 19:17","https://www.blueletterbible.org/kjv/1sa/19/17/s_255017","...Why hast thou <strong>deceived</strong> me so..."),
     ("1 Samuel 28:12","https://www.blueletterbible.org/kjv/1sa/28/12/s_264012","...Why hast thou <strong>deceived</strong> me? for thou art Saul."),
     ("1 Chronicles 12:17","https://www.blueletterbible.org/kjv/1ch/12/17/s_350017","...if ye be come to <strong>betray</strong> me to mine enemies...")],
    [("H5377","nasha (to deceive)"),("H898","bagad (to act treacherously)"),("H3584","kachash (to deny)")])

add("H4302","Hebrew","Old Testament","rtl","מַטָּע","matta","Noun, Masculine",
    "A planting, plantation, place of planting",
    "From H5193 (nata, to plant). The act of planting, the place of planting, or what has been planted. Used metaphorically of God planting His people.",
    "<em>Matta</em> carries God's agricultural vision. In Isaiah 60:21, redeemed Israel is 'the branch of my planting.' Ezekiel 34:29 promises 'a plant of renown.' God as master gardener: He selects the soil, plants with intention, and expects fruit. This metaphor threads from Eden through the prophets to Jesus' vine parable.",
    [("Isaiah 60:21","https://www.blueletterbible.org/kjv/isa/60/21/s_739021","...the branch of my <strong>planting</strong>, the work of my hands..."),
     ("Isaiah 61:3","https://www.blueletterbible.org/kjv/isa/61/3/s_740003","...the <strong>planting</strong> of the LORD, that he might be glorified."),
     ("Ezekiel 17:7","https://www.blueletterbible.org/kjv/eze/17/7/s_819007","...from the furrows of her <strong>plantation</strong>."),
     ("Ezekiel 34:29","https://www.blueletterbible.org/kjv/eze/34/29/s_836029","...I will raise up for them a <strong>plant</strong> of renown..."),
     ("Micah 1:6","https://www.blueletterbible.org/kjv/mic/1/6/s_895006","...as <strong>plantings</strong> of a vineyard...")],
    [("H5193","nata (to plant)"),("H3754","kerem (vineyard)"),("H6529","p'riy (fruit)")])

add("H6216","Hebrew","Old Testament","rtl","עָשׁוֹק","ashowq","Adjective",
    "Oppressor, extortioner",
    "From H6231 (ashaq). One who oppresses, defrauds, or extorts. Appears in prophetic denunciations of social injustice.",
    "<em>Ashowq</em> names God's grievance against Israel: exploitation of the vulnerable. The prophets thundered against oppressors. Biblical justice is concrete, economic, and personal. God identifies with the oppressed (Psalm 12:5) and will judge the oppressor. No worship is acceptable while oppression continues.",
    [("Isaiah 51:13","https://www.blueletterbible.org/kjv/isa/51/13/s_730013","...the fury of the <strong>oppressor</strong>..."),
     ("Jeremiah 21:12","https://www.blueletterbible.org/kjv/jer/21/12/s_666012","...deliver him that is spoiled out of the hand of the <strong>oppressor</strong>..."),
     ("Jeremiah 22:3","https://www.blueletterbible.org/kjv/jer/22/3/s_667003","...deliver the spoiled out of the hand of the <strong>oppressor</strong>..."),
     ("Psalm 72:4","https://www.blueletterbible.org/kjv/psa/72/4/s_550004","...shall break in pieces the <strong>oppressor</strong>."),
     ("Ecclesiastes 4:1","https://www.blueletterbible.org/kjv/ecc/4/1/s_663001","...on the side of their <strong>oppressors</strong> there was power...")],
    [("H6231","ashaq (to oppress)"),("H3238","yanah (to maltreat)"),("H6041","aniy (poor, afflicted)")])

add("H1093","Hebrew","Old Testament","rtl","בְּלוֹ","b'lo","Noun, Masculine",
    "Tribute, tax, revenue",
    "An Aramaic loanword found only in Ezra, referring to an excise tax or tribute payment. Part of the triad: mindah, b'lo, halak.",
    "Though technical, <em>b'lo</em>'s significance lies in exile/return context. Artaxerxes exempted priests from <em>b'lo</em> (Ezra 7:24), enabling temple worship. God's sovereignty extends over tax codes of empires — He uses human administrative machinery for redemptive purposes.",
    [("Ezra 4:13","https://www.blueletterbible.org/kjv/ezr/4/13/s_437013","...will they not pay <strong>toll</strong>, tribute, and custom..."),
     ("Ezra 4:20","https://www.blueletterbible.org/kjv/ezr/4/20/s_437020","...<strong>toll</strong>, tribute, and custom, was paid unto them."),
     ("Ezra 7:24","https://www.blueletterbible.org/kjv/ezr/7/24/s_440024","...it shall not be lawful to impose <strong>toll</strong>, tribute, or custom, upon them."),
     ("Nehemiah 5:4","https://www.blueletterbible.org/kjv/neh/5/4/s_418004","...We have borrowed money for the king's tribute..."),
     ("Matthew 22:17","https://www.blueletterbible.org/kjv/mat/22/17/s_951017","...Is it lawful to give <strong>tribute</strong> unto Caesar, or not?")],
    [("H4061","middah (tribute)"),("H1983","halak (tax)"),("H4522","mas (forced labor)")])

add("H1110","Hebrew","Old Testament","rtl","בָּלַק","balaq","Verb",
    "To devastate, lay waste, annihilate",
    "A primitive root meaning to devastate or destroy completely. Used of total destruction as divine judgment.",
    "<em>Balaq</em> captures the totality of divine judgment. Isaiah 24:1: God 'maketh the earth empty and maketh it waste.' Related to the name Balak, the Moabite king who sought to destroy Israel. The irony: the 'devastator' could not devastate what God had blessed.",
    [("Isaiah 24:1","https://www.blueletterbible.org/kjv/isa/24/1/s_703001","...the LORD maketh the earth empty, and maketh it <strong>waste</strong>..."),
     ("Isaiah 24:3","https://www.blueletterbible.org/kjv/isa/24/3/s_703003","The land shall be utterly emptied, and utterly <strong>spoiled</strong>..."),
     ("Nahum 2:10","https://www.blueletterbible.org/kjv/nah/2/10/s_901010","She is <strong>empty</strong>, and void, and waste..."),
     ("Nahum 2:2","https://www.blueletterbible.org/kjv/nah/2/2/s_901002","...the emptiers have <strong>emptied</strong> them out..."),
     ("Isaiah 19:3","https://www.blueletterbible.org/kjv/isa/19/3/s_698003","...I will <strong>destroy</strong> the counsel thereof...")],
    [("H2717","charab (to be desolate)"),("H8074","shamem (to be appalled)"),("H7843","shachath (to destroy)")])

add("H1115","Hebrew","Old Testament","rtl","בִּלְתִּי","biltiy","Adverb/Conjunction",
    "Not, except, without, unless",
    "A negative particle meaning 'not,' 'except,' 'unless,' or 'without.' Frequently used in conditional and exclusionary covenant statements.",
    "<em>Biltiy</em> appears in critical covenant moments. It creates theological boundaries — marking what is excluded, exceptional, and non-negotiable. In God's economy, the 'except' and 'unless' clauses reveal where His lines are drawn. Amos 3:3: 'Can two walk together, except they be agreed?'",
    [("Genesis 43:3","https://www.blueletterbible.org/kjv/gen/43/3/s_43003","...Ye shall not see my face, <strong>except</strong> your brother be with you."),
     ("Deuteronomy 4:12","https://www.blueletterbible.org/kjv/deu/4/12/s_157012","...ye saw no similitude; <strong>only</strong> ye heard a voice."),
     ("Judges 7:14","https://www.blueletterbible.org/kjv/jdg/7/14/s_218014","...This is nothing else <strong>save</strong> the sword of Gideon..."),
     ("Isaiah 14:6","https://www.blueletterbible.org/kjv/isa/14/6/s_693006","...is persecuted, and none <strong>hindereth</strong>."),
     ("Amos 3:3","https://www.blueletterbible.org/kjv/amo/3/3/s_882003","Can two walk together, <strong>except</strong> they be agreed?")],
    [("H3808","lo (not)"),("H369","ayin (none)"),("H518","im (if)")])

add("H1144","Hebrew","Old Testament","rtl","בִּנְיָמִין","Binyamin","Proper Noun",
    "Benjamin — 'son of the right hand'",
    "From H1121 (ben) and H3225 (yamin). Jacob's youngest son, born to Rachel. Originally named Ben-oni ('son of my sorrow') by dying Rachel, renamed Benjamin by Jacob.",
    "<em>Binyamin</em> carries powerful renaming theology. Rachel's dying name was overruled by Jacob's prophetic name: 'son of the right hand' — honor and power. The right hand is blessing (Genesis 48:14), authority (Psalm 110:1), salvation (Psalm 138:7). Benjamin's tribe produced King Saul and the apostle Paul. God transforms identity: what begins in sorrow is redeemed as strength.",
    [("Genesis 35:18","https://www.blueletterbible.org/kjv/gen/35/18/s_35018","...she called his name Ben-oni: but his father called him <strong>Benjamin</strong>."),
     ("Genesis 43:34","https://www.blueletterbible.org/kjv/gen/43/34/s_43034","...<strong>Benjamin's</strong> mess was five times so much as any of theirs."),
     ("Deuteronomy 33:12","https://www.blueletterbible.org/kjv/deu/33/12/s_186012","...of <strong>Benjamin</strong> he said, The beloved of the LORD shall dwell in safety by him..."),
     ("Judges 20:16","https://www.blueletterbible.org/kjv/jdg/20/16/s_231016","Among all this people there were seven hundred chosen men lefthanded..."),
     ("Philippians 3:5","https://www.blueletterbible.org/kjv/phl/3/5/s_1106005","...of the tribe of <strong>Benjamin</strong>, an Hebrew of the Hebrews...")],
    [("H1121","ben (son)"),("H3225","yamin (right hand)"),("H3478","Yisrael (Israel)")])

# === 23 GREEK ===
add("G2104","Greek","New Testament","ltr","εὐγενής","eugenēs","Adjective",
    "Well-born, noble, generous",
    "From G2095 (eu, well) and G1096 (ginomai, to become). Literally 'well-born.' Used both literally (of nobility) and figuratively (noble character, open-mindedness).",
    "<em>Eugenēs</em> achieves its most famous use in Acts 17:11, where the Bereans are called 'more noble' because they 'searched the scriptures daily.' Nobility is redefined: not bloodline but intellectual honesty. Paul subverts it in 1 Corinthians 1:26 — 'not many noble are called.' True nobility is willingness to hear and obey.",
    [("Acts 17:11","https://www.blueletterbible.org/kjv/act/17/11/s_1035011","These were more <strong>noble</strong> than those in Thessalonica...and searched the scriptures daily..."),
     ("1 Corinthians 1:26","https://www.blueletterbible.org/kjv/1co/1/26/s_1063026","...not many mighty, not many <strong>noble</strong>, are called."),
     ("Luke 19:12","https://www.blueletterbible.org/kjv/luk/19/12/s_992012","...A certain <strong>nobleman</strong> went into a far country..."),
     ("Acts 17:10","https://www.blueletterbible.org/kjv/act/17/10/s_1035010","And the brethren immediately sent away Paul and Silas by night unto Berea..."),
     ("Luke 19:15","https://www.blueletterbible.org/kjv/luk/19/15/s_992015","...when he was returned, having received the kingdom...")],
    [("G2903","kratistos (most excellent)"),("G1741","endoxos (honored)"),("G4586","semnos (dignified)")])

add("G2108","Greek","New Testament","ltr","εὐεργεσία","euergesia","Noun, Feminine",
    "Beneficence, good deed, act of kindness",
    "From G2110 (euergetēs, benefactor). A good work, act of kindness or benefit. Tangible, practical goodness.",
    "<em>Euergesia</em> appears in Acts 4:9 when Peter is questioned about healing: 'If we be examined of the good deed done to the impotent man...' The irony: religious authorities interrogating an act of mercy. The word teaches that genuine Christianity produces tangible benefit. Faith without works of kindness is dead.",
    [("Acts 4:9","https://www.blueletterbible.org/kjv/act/4/9/s_1022009","If we this day be examined of the <strong>good deed</strong> done to the impotent man..."),
     ("1 Timothy 6:2","https://www.blueletterbible.org/kjv/1ti/6/2/s_1125002","...partakers of the <strong>benefit</strong>."),
     ("Acts 10:38","https://www.blueletterbible.org/kjv/act/10/38/s_1028038","...who went about doing good..."),
     ("Luke 22:25","https://www.blueletterbible.org/kjv/luk/22/25/s_995025","...they that exercise authority upon them are called benefactors."),
     ("Galatians 6:10","https://www.blueletterbible.org/kjv/gal/6/10/s_1097010","...let us do good unto all men...")],
    [("G2110","euergetēs (benefactor)"),("G18","agathos (good)"),("G5485","charis (grace)")])

add("G2151","Greek","New Testament","ltr","εὐσεβέω","eusebeō","Verb",
    "To show piety, to worship, to revere",
    "From G2152 (eusebēs, devout). To act piously, show reverence and practical devotion. Used for worship of God and honoring family.",
    "<em>Eusebeō</em> bridges worship and ethics. In 1 Timothy 5:4, children are told to 'shew piety at home' — caring for parents is worship. This is radical: honoring your aging mother is as much <em>eusebeia</em> as singing hymns. The NT refuses to separate vertical devotion from horizontal duty.",
    [("Acts 17:23","https://www.blueletterbible.org/kjv/act/17/23/s_1035023","...Whom therefore ye ignorantly <strong>worship</strong>, him declare I unto you."),
     ("1 Timothy 5:4","https://www.blueletterbible.org/kjv/1ti/5/4/s_1124004","...let them learn first to <strong>shew piety at home</strong>..."),
     ("2 Peter 1:3","https://www.blueletterbible.org/kjv/2pe/1/3/s_1157003","...all things that pertain unto life and godliness..."),
     ("1 Timothy 4:7","https://www.blueletterbible.org/kjv/1ti/4/7/s_1123007","...exercise thyself rather unto godliness."),
     ("1 Timothy 6:6","https://www.blueletterbible.org/kjv/1ti/6/6/s_1125006","But godliness with contentment is great gain.")],
    [("G2152","eusebēs (devout)"),("G2150","eusebeia (godliness)"),("G4576","sebō (to worship)")])

add("G2188","Greek","New Testament","ltr","ἐφφαθά","ephphatha","Aramaic Interjection",
    "Be opened!",
    "An Aramaic word preserved in Greek, meaning 'be opened.' Spoken by Jesus healing a deaf man (Mark 7:34). One of Jesus' actual Aramaic words preserved in the Gospels.",
    "<em>Ephphatha</em> is among the <em>ipsissima verba</em> of Jesus. When Jesus says 'Be opened,' deaf ears hear and mute tongues speak. This single word captures the gospel: Jesus opens what sin has closed — ears, eyes, tombs, hearts. The command of Christ creates the capacity to obey it.",
    [("Mark 7:34","https://www.blueletterbible.org/kjv/mar/7/34/s_964034","...he sighed, and saith unto him, <strong>Ephphatha</strong>, that is, Be opened."),
     ("Mark 7:35","https://www.blueletterbible.org/kjv/mar/7/35/s_964035","And straightway his ears were opened, and the string of his tongue was loosed..."),
     ("Isaiah 35:5","https://www.blueletterbible.org/kjv/isa/35/5/s_714005","Then the eyes of the blind shall be opened, and the ears of the deaf shall be unstopped."),
     ("Matthew 11:5","https://www.blueletterbible.org/kjv/mat/11/5/s_940005","The blind receive their sight...the deaf hear..."),
     ("Luke 4:18","https://www.blueletterbible.org/kjv/luk/4/18/s_977018","The Spirit of the Lord is upon me...to set at liberty them that are bruised.")],
    [("G1272","dianoigō (to open completely)"),("G455","anoigō (to open)"),("G5456","phōnē (voice)")])

add("G2190","Greek","New Testament","ltr","ἐχθρός","echthros","Adjective/Noun",
    "Enemy, hostile, hateful",
    "From G2189 (echthra, enmity). One who is hostile, an adversary. Used of human enemies and of Satan. Active hostility, not mere indifference.",
    "<em>Echthros</em> frames Jesus' most radical teaching: 'Love your enemies' (Matthew 5:44). <em>Agapaō</em> toward the <em>echthros</em>. Paul extends: 'While we were enemies, we were reconciled to God' (Romans 5:10). The last enemy is death (1 Corinthians 15:26). God loved His enemies first — and commands His children to do the same.",
    [("Matthew 5:44","https://www.blueletterbible.org/kjv/mat/5/44/s_934044","But I say unto you, Love your <strong>enemies</strong>..."),
     ("Romans 5:10","https://www.blueletterbible.org/kjv/rom/5/10/s_1051010","...when we were <strong>enemies</strong>, we were reconciled to God by the death of his Son..."),
     ("1 Corinthians 15:26","https://www.blueletterbible.org/kjv/1co/15/26/s_1077026","The last <strong>enemy</strong> that shall be destroyed is death."),
     ("Matthew 13:25","https://www.blueletterbible.org/kjv/mat/13/25/s_942025","...his <strong>enemy</strong> came and sowed tares among the wheat..."),
     ("Luke 1:71","https://www.blueletterbible.org/kjv/luk/1/71/s_974071","...saved from our <strong>enemies</strong>...")],
    [("G2189","echthra (enmity)"),("G476","antidikos (adversary)"),("G4567","Satanas (Satan)")])

add("G2195","Greek","New Testament","ltr","Ζακχαῖος","Zakchaios","Proper Noun",
    "Zacchaeus — 'pure, innocent'",
    "Of Hebrew origin, from H2141 (zakay). Chief tax collector in Jericho who climbed a sycamore tree. His name ironically means 'pure.'",
    "<em>Zakchaios</em> is irony and grace. A man named 'Pure' was considered most impure — a chief tax collector. Yet Jesus singles him out: 'Today I must abide at thy house.' The encounter transforms him. Jesus declares, 'This day is salvation come to this house.' The name became true: the 'impure' man was made pure by the one who called him.",
    [("Luke 19:2","https://www.blueletterbible.org/kjv/luk/19/2/s_992002","...a man named <strong>Zacchaeus</strong>, which was the chief among the publicans, and he was rich."),
     ("Luke 19:5","https://www.blueletterbible.org/kjv/luk/19/5/s_992005","...<strong>Zacchaeus</strong>, make haste, and come down; for to day I must abide at thy house."),
     ("Luke 19:8","https://www.blueletterbible.org/kjv/luk/19/8/s_992008","And <strong>Zacchaeus</strong> stood, and said unto the Lord; Behold, Lord, the half of my goods I give to the poor..."),
     ("Luke 19:9","https://www.blueletterbible.org/kjv/luk/19/9/s_992009","...This day is salvation come to this house..."),
     ("Luke 19:10","https://www.blueletterbible.org/kjv/luk/19/10/s_992010","For the Son of man is come to seek and to save that which was lost.")],
    [("G5057","telōnēs (tax collector)"),("G268","hamartōlos (sinner)"),("G4991","sōtēria (salvation)")])

add("G2149","Greek","New Testament","ltr","εὐρύχωρος","eurychōros","Adjective",
    "Broad, spacious, wide",
    "From G2095 (eu) and G5561 (chōra). Literally 'having much room.' Used by Jesus describing the broad way to destruction.",
    "<em>Eurychōros</em> appears in Jesus' sobering warning: 'Broad is the way that leadeth to destruction' (Matthew 7:13). The spaciousness is the danger — comfortable, easy, asking nothing. The narrow way demands everything. Spiritual danger often feels like freedom, and true freedom often feels like constraint.",
    [("Matthew 7:13","https://www.blueletterbible.org/kjv/mat/7/13/s_936013","...wide is the gate, and <strong>broad</strong> is the way, that leadeth to destruction..."),
     ("Matthew 7:14","https://www.blueletterbible.org/kjv/mat/7/14/s_936014","Because strait is the gate, and narrow is the way, which leadeth unto life..."),
     ("Psalm 119:96","https://www.blueletterbible.org/kjv/psa/119/96/s_597096","...thy commandment is exceeding broad."),
     ("Luke 13:24","https://www.blueletterbible.org/kjv/luk/13/24/s_986024","Strive to enter in at the strait gate..."),
     ("Proverbs 14:12","https://www.blueletterbible.org/kjv/pro/14/12/s_642012","There is a way which seemeth right unto a man, but the end thereof are the ways of death.")],
    [("G4116","platus (broad)"),("G4728","stenos (narrow)"),("G3598","hodos (way, road)")])

add("G2159","Greek","New Testament","ltr","εὐτόνως","eutonōs","Adverb",
    "Vigorously, powerfully, vehemently",
    "From G2095 (eu) and G5114 (teinō, to stretch). Literally 'well-stretched' — with full force, intensely.",
    "<em>Eutonōs</em> describes both fury of opposition and power of proclamation. In Luke 23:10, scribes accused Jesus 'vehemently.' In Acts 18:28, Apollos 'mightily convinced the Jews.' Intensity is neutral — it can serve truth or falsehood. The gospel demands passionate proclamation, not tepid agreement.",
    [("Luke 23:10","https://www.blueletterbible.org/kjv/luk/23/10/s_996010","And the chief priests and scribes stood and <strong>vehemently</strong> accused him."),
     ("Acts 18:28","https://www.blueletterbible.org/kjv/act/18/28/s_1036028","For he <strong>mightily</strong> convinced the Jews...shewing by the scriptures that Jesus was Christ."),
     ("Acts 18:25","https://www.blueletterbible.org/kjv/act/18/25/s_1036025","...being fervent in the spirit, he spake and taught diligently..."),
     ("Romans 12:11","https://www.blueletterbible.org/kjv/rom/12/11/s_1058011","Not slothful in business; fervent in spirit; serving the Lord;"),
     ("Titus 1:13","https://www.blueletterbible.org/kjv/tit/1/13/s_1130013","...rebuke them sharply, that they may be sound in the faith.")],
    [("G1722","en (in)"),("G2205","zēlos (zeal)"),("G1411","dynamis (power)")])

add("G2200","Greek","New Testament","ltr","ζεστός","zestos","Adjective",
    "Hot, boiling, fervent",
    "From G2204 (zeō, to boil). Literally 'boiling hot.' Used exclusively in Revelation 3:15-16 for the Laodicean church.",
    "<em>Zestos</em> is what Jesus wants: 'I would thou wert cold or hot.' Lukewarm is nauseating. Hot water healed (Hierapolis springs); cold water refreshed. Lukewarm was useless. The word demands a decision: passionate commitment or honest rejection. Comfortable indifference — the temperature at which nothing happens — is the worst spiritual condition.",
    [("Revelation 3:15","https://www.blueletterbible.org/kjv/rev/3/15/s_1170015","...thou art neither cold nor <strong>hot</strong>: I would thou wert cold or <strong>hot</strong>."),
     ("Revelation 3:16","https://www.blueletterbible.org/kjv/rev/3/16/s_1170016","So then because thou art lukewarm, and neither cold nor <strong>hot</strong>, I will spue thee out of my mouth."),
     ("Romans 12:11","https://www.blueletterbible.org/kjv/rom/12/11/s_1058011","Not slothful in business; fervent in spirit; serving the Lord."),
     ("Acts 18:25","https://www.blueletterbible.org/kjv/act/18/25/s_1036025","...being fervent in the spirit..."),
     ("Revelation 3:19","https://www.blueletterbible.org/kjv/rev/3/19/s_1170019","As many as I love, I rebuke and chasten: be zealous therefore, and repent.")],
    [("G2204","zeō (to boil)"),("G5593","psychros (cold)"),("G5513","chliaros (lukewarm)")])

add("G2205","Greek","New Testament","ltr","ζῆλος","zēlos","Noun, Masculine",
    "Zeal, jealousy, fervor, envy",
    "From G2204 (zeō, to boil). Intense emotion — positive (zeal, devotion) or negative (jealousy, envy). Context determines which.",
    "<em>Zēlos</em> is morally ambivalent. Positive: Jesus cleansed the temple because 'the zeal of thine house hath eaten me up' (John 2:17). Negative: James warns 'where envying and strife is, there is confusion' (James 3:16). Passion directed at God's glory is holy fire; directed at self-interest, consuming flame. Passion must be governed by truth.",
    [("John 2:17","https://www.blueletterbible.org/kjv/jhn/2/17/s_999017","...The <strong>zeal</strong> of thine house hath eaten me up."),
     ("Romans 10:2","https://www.blueletterbible.org/kjv/rom/10/2/s_1056002","...they have a <strong>zeal</strong> of God, but not according to knowledge."),
     ("2 Corinthians 7:11","https://www.blueletterbible.org/kjv/2co/7/11/s_1085011","...what vehement desire, yea, what <strong>zeal</strong>..."),
     ("Galatians 1:14","https://www.blueletterbible.org/kjv/gal/1/14/s_1092014","...being more exceedingly <strong>zealous</strong> of the traditions of my fathers."),
     ("James 3:16","https://www.blueletterbible.org/kjv/jas/3/16/s_1149016","For where <strong>envying</strong> and strife is, there is confusion...")],
    [("G2206","zēloō (to be zealous)"),("G2207","zēlōtēs (zealot)"),("G5355","phthonos (envy)")])

add("G2210","Greek","New Testament","ltr","ζημιόω","zēmioō","Verb",
    "To suffer loss, to forfeit, to be damaged",
    "From G2209 (zēmia, damage). To cause or experience loss or forfeiture. Used by Jesus and Paul for ultimate profit-and-loss.",
    "<em>Zēmioō</em> frames the gospel's most devastating cost-benefit analysis. Jesus: 'What shall it profit a man, if he shall gain the whole world, and lose his own soul?' (Mark 8:36). Paul counts everything as loss compared to knowing Christ (Philippians 3:8). The person who loses everything for Christ has lost nothing.",
    [("Matthew 16:26","https://www.blueletterbible.org/kjv/mat/16/26/s_945026","...what is a man profited, if he shall gain the whole world, and <strong>lose</strong> his own soul?"),
     ("Mark 8:36","https://www.blueletterbible.org/kjv/mar/8/36/s_965036","For what shall it profit a man, if he shall gain the whole world, and <strong>lose</strong> his own soul?"),
     ("Luke 9:25","https://www.blueletterbible.org/kjv/luk/9/25/s_982025","...if he gain the whole world, and <strong>lose</strong> himself, or be cast away?"),
     ("Philippians 3:8","https://www.blueletterbible.org/kjv/phl/3/8/s_1106008","...I count all things but <strong>loss</strong> for the excellency of the knowledge of Christ Jesus..."),
     ("1 Corinthians 3:15","https://www.blueletterbible.org/kjv/1co/3/15/s_1065015","If any man's work shall be burned, he shall <strong>suffer loss</strong>...")],
    [("G2209","zēmia (loss)"),("G622","apollymi (to destroy)"),("G2770","kerdainō (to gain)")])

add("G2213","Greek","New Testament","ltr","ζήτημα","zētēma","Noun, Neuter",
    "Question, issue, matter of debate",
    "From G2212 (zēteō, to seek). A disputed point or controversial issue. Used in Acts for theological and legal questions about the early church.",
    "<em>Zētēma</em> appears during critical moments where the gospel collides with religion and law. In Acts 15:2, Gentile circumcision is the <em>zētēma</em>. In Acts 18:15, Gallio dismisses Paul's case as a Jewish <em>zētēma</em>. The church's greatest advances came through resolving hard questions. God works through inquiry.",
    [("Acts 15:2","https://www.blueletterbible.org/kjv/act/15/2/s_1033002","...they determined...should go up to Jerusalem about this <strong>question</strong>."),
     ("Acts 18:15","https://www.blueletterbible.org/kjv/act/18/15/s_1036015","...if it be a <strong>question</strong> of words and names..."),
     ("Acts 23:29","https://www.blueletterbible.org/kjv/act/23/29/s_1041029","...accused of <strong>questions</strong> of their law..."),
     ("Acts 25:19","https://www.blueletterbible.org/kjv/act/25/19/s_1043019","...certain <strong>questions</strong> against him of their own superstition..."),
     ("Acts 26:3","https://www.blueletterbible.org/kjv/act/26/3/s_1044003","...expert in all customs and <strong>questions</strong> which are among the Jews...")],
    [("G2212","zēteō (to seek)"),("G2214","zētēsis (debate)"),("G1905","eperōtēma (inquiry)")])

add("G2222","Greek","New Testament","ltr","ζωή","zōē","Noun, Feminine",
    "Life, vitality, eternal life",
    "From G2198 (zaō, to live). Life in the fullest sense — not merely biological existence (bios) but the quality of life from God. John uses it 36 times.",
    "<em>Zōē</em> is one of the NT's most theologically loaded words. 'In him was life' (John 1:4). 'I am the way, the truth, and the life' (John 14:6). 'I am come that they might have life, and have it more abundantly' (John 10:10). Not survival but flourishing — divine existence that death cannot extinguish. <em>Zōē</em> is what humanity lost in Eden and Christ restores at the cross.",
    [("John 1:4","https://www.blueletterbible.org/kjv/jhn/1/4/s_998004","In him was <strong>life</strong>; and the life was the light of men."),
     ("John 10:10","https://www.blueletterbible.org/kjv/jhn/10/10/s_1007010","...I am come that they might have <strong>life</strong>, and that they might have it more abundantly."),
     ("John 14:6","https://www.blueletterbible.org/kjv/jhn/14/6/s_1011006","...I am the way, the truth, and the <strong>life</strong>..."),
     ("Romans 6:23","https://www.blueletterbible.org/kjv/rom/6/23/s_1052023","...the gift of God is eternal <strong>life</strong> through Jesus Christ our Lord."),
     ("1 John 5:12","https://www.blueletterbible.org/kjv/1jo/5/12/s_1164012","He that hath the Son hath <strong>life</strong>...")],
    [("G2198","zaō (to live)"),("G979","bios (life, livelihood)"),("G166","aiōnios (eternal)")])

add("G2232","Greek","New Testament","ltr","ἡγεμών","hēgemōn","Noun, Masculine",
    "Governor, leader, prince",
    "From G2233 (hēgeomai, to lead). A leader, commander, or provincial governor. Used for Roman governors — Pilate, Felix, Festus.",
    "<em>Hēgemōn</em> places the gospel within structures of earthly power. Jesus stood before Pilate the governor (Matthew 27:2) — the King of kings judged by a provincial functionary. Jesus prophesied followers would be brought before governors (Matthew 10:18). Human governors exercise temporary authority but unknowingly serve eternal purposes.",
    [("Matthew 27:2","https://www.blueletterbible.org/kjv/mat/27/2/s_956002","...delivered him to Pontius Pilate the <strong>governor</strong>."),
     ("Matthew 10:18","https://www.blueletterbible.org/kjv/mat/10/18/s_939018","...ye shall be brought before <strong>governors</strong> and kings for my sake..."),
     ("Matthew 27:11","https://www.blueletterbible.org/kjv/mat/27/11/s_956011","And Jesus stood before the <strong>governor</strong>..."),
     ("Acts 23:24","https://www.blueletterbible.org/kjv/act/23/24/s_1041024","...bring him safe unto Felix the <strong>governor</strong>."),
     ("1 Peter 2:14","https://www.blueletterbible.org/kjv/1pe/2/14/s_1153014","Or unto <strong>governors</strong>...sent by him for the punishment of evildoers...")],
    [("G2233","hēgeomai (to lead)"),("G758","archōn (ruler)"),("G1849","exousia (authority)")])

add("G2246","Greek","New Testament","ltr","ἥλιος","hēlios","Noun, Masculine",
    "Sun",
    "The sun. Used literally and figuratively for God's impartial goodness, apocalyptic signs, and the glory of the risen Christ.",
    "<em>Hēlios</em> operates on multiple theological levels. In the Sermon on the Mount, God 'maketh his sun to rise on the evil and on the good' (Matthew 5:45) — common grace. In the Transfiguration, Jesus' face 'did shine as the sun' (Matthew 17:2) — divine glory. In Revelation, the sun darkens in judgment (6:12) and becomes unnecessary in the New Jerusalem (21:23). The sun that began creation will be surpassed by the Creator.",
    [("Matthew 5:45","https://www.blueletterbible.org/kjv/mat/5/45/s_934045","...he maketh his <strong>sun</strong> to rise on the evil and on the good..."),
     ("Matthew 17:2","https://www.blueletterbible.org/kjv/mat/17/2/s_946002","...his face did shine as the <strong>sun</strong>..."),
     ("Revelation 6:12","https://www.blueletterbible.org/kjv/rev/6/12/s_1173012","...the <strong>sun</strong> became black as sackcloth of hair..."),
     ("Revelation 21:23","https://www.blueletterbible.org/kjv/rev/21/23/s_1188023","...the city had no need of the <strong>sun</strong>...for the glory of God did lighten it..."),
     ("Malachi 4:2","https://www.blueletterbible.org/kjv/mal/4/2/s_929002","...the <strong>Sun</strong> of righteousness arise with healing in his wings...")],
    [("G4582","selēnē (moon)"),("G792","astēr (star)"),("G5457","phōs (light)")])

add("G2247","Greek","New Testament","ltr","ἧλος","hēlos","Noun, Masculine",
    "Nail",
    "The iron nails of Roman crucifixion. Appears only in John 20:25, in Thomas' demand for proof of the resurrection.",
    "<em>Hēlos</em> carries the weight of the atonement. Thomas: 'Except I shall see the print of the nails...' The risen Christ still bore the nail-marks — His glorified body retained evidence of suffering. Resurrection does not erase the cross; it transforms it. The wounds become credentials. Thomas utters the highest Christological confession: 'My Lord and my God.'",
    [("John 20:25","https://www.blueletterbible.org/kjv/jhn/20/25/s_1017025","...Except I shall see in his hands the print of the <strong>nails</strong>...I will not believe."),
     ("John 20:27","https://www.blueletterbible.org/kjv/jhn/20/27/s_1017027","...Reach hither thy finger, and behold my hands..."),
     ("John 20:28","https://www.blueletterbible.org/kjv/jhn/20/28/s_1017028","...Thomas answered and said unto him, My Lord and my God."),
     ("Colossians 2:14","https://www.blueletterbible.org/kjv/col/2/14/s_1109014","...took it out of the way, <strong>nailing</strong> it to his cross."),
     ("Isaiah 53:5","https://www.blueletterbible.org/kjv/isa/53/5/s_732005","But he was wounded for our transgressions...")],
    [("G4716","stauros (cross)"),("G4717","stauroō (to crucify)"),("G5134","trauma (wound)")])

add("G2253","Greek","New Testament","ltr","ἡμιθανής","hēmithanēs","Adjective",
    "Half-dead",
    "From G2255 (hēmisu, half) and G2348 (thnēskō, to die). Used only in Luke 10:30 in the Good Samaritan parable.",
    "<em>Hēmithanēs</em> appears only once but carries immense weight. The man on the Jericho road is humanity after the Fall: stripped, wounded, half dead. He cannot save himself. The priest and Levite — the Law — pass by. Only the Samaritan — the despised outsider — stops. The deeper question: 'Who can save the half-dead?' Only one who crosses every boundary to reach us.",
    [("Luke 10:30","https://www.blueletterbible.org/kjv/luk/10/30/s_983030","...leaving him <strong>half dead</strong>."),
     ("Luke 10:33","https://www.blueletterbible.org/kjv/luk/10/33/s_983033","But a certain Samaritan...when he saw him, he had compassion on him."),
     ("Luke 10:34","https://www.blueletterbible.org/kjv/luk/10/34/s_983034","And went to him, and bound up his wounds, pouring in oil and wine..."),
     ("Luke 10:36","https://www.blueletterbible.org/kjv/luk/10/36/s_983036","Which now of these three...was neighbour unto him that fell among the thieves?"),
     ("Romans 5:6","https://www.blueletterbible.org/kjv/rom/5/6/s_1051006","For when we were yet without strength, in due time Christ died for the ungodly.")],
    [("G2255","hēmisu (half)"),("G2348","thnēskō (to die)"),("G4697","splanchnizomai (to have compassion)")])

add("G2256","Greek","New Testament","ltr","ἡμιώριον","hēmiōrion","Noun, Neuter",
    "Half an hour",
    "From G2255 (hēmisu) and G5610 (hōra). Appears only in Revelation 8:1 — the silence in heaven after the seventh seal.",
    "<em>Hēmiōrion</em> describes perhaps the most dramatic silence in Scripture. After six seals of cosmic upheaval, the seventh produces silence — 'about the space of half an hour.' Heaven, filled with ceaseless worship, goes utterly quiet. The seven trumpets are about to sound. Even heaven holds its breath before God's final acts. The half-hour is the hush before the holy.",
    [("Revelation 8:1","https://www.blueletterbible.org/kjv/rev/8/1/s_1175001","...there was silence in heaven about the space of <strong>half an hour</strong>."),
     ("Habakkuk 2:20","https://www.blueletterbible.org/kjv/hab/2/20/s_905020","But the LORD is in his holy temple: let all the earth keep silence before him."),
     ("Zephaniah 1:7","https://www.blueletterbible.org/kjv/zep/1/7/s_907007","Hold thy peace at the presence of the Lord GOD..."),
     ("Zechariah 2:13","https://www.blueletterbible.org/kjv/zec/2/13/s_913013","Be silent, O all flesh, before the LORD..."),
     ("Psalm 46:10","https://www.blueletterbible.org/kjv/psa/46/10/s_524010","Be still, and know that I am God...")],
    [("G4602","sigē (silence)"),("G5610","hōra (hour)"),("G4973","sphragis (seal)")])

add("G2178","Greek","New Testament","ltr","ἐφάπαξ","ephapax","Adverb",
    "Once for all, at once, once and for all time",
    "From G1909 (epi) and G530 (hapax). An intensified form meaning 'once for all' — a single, unrepeatable, decisive act.",
    "<em>Ephapax</em> is theologically decisive. In Romans 6:10, 'He died unto sin once.' Hebrews 7:27: Christ offered Himself 'once for all.' Hebrews 9:12: He entered the holy place 'once for all' with His own blood. The word eliminates any notion that Christ's sacrifice needs supplementing or repeating. It is finished. <em>Ephapax</em> is the adverb of the atonement.",
    [("Romans 6:10","https://www.blueletterbible.org/kjv/rom/6/10/s_1052010","For in that he died, he died unto sin <strong>once</strong>..."),
     ("Hebrews 7:27","https://www.blueletterbible.org/kjv/heb/7/27/s_1140027","...this he did <strong>once</strong>, when he offered up himself."),
     ("Hebrews 9:12","https://www.blueletterbible.org/kjv/heb/9/12/s_1142012","...by his own blood he entered in <strong>once</strong> into the holy place..."),
     ("Hebrews 10:10","https://www.blueletterbible.org/kjv/heb/10/10/s_1143010","...the offering of the body of Jesus Christ <strong>once for all</strong>."),
     ("1 Corinthians 15:6","https://www.blueletterbible.org/kjv/1co/15/6/s_1077006","...seen of above five hundred brethren <strong>at once</strong>...")],
    [("G530","hapax (once)"),("G2409","hiereus (priest)"),("G4376","prosphora (offering)")])

add("G2156","Greek","New Testament","ltr","εὐσχημόνως","euschēmonōs","Adverb",
    "Decently, becomingly, with propriety",
    "From G2158 (euschēmōn, comely). In a becoming manner, with propriety and dignity.",
    "<em>Euschēmonōs</em> appears three times in practical ethics. Romans 13:13: 'Let us walk honestly.' 1 Corinthians 14:40: 'Let all things be done decently and in order.' 1 Thessalonians 4:12: 'Walk honestly toward them that are without.' The gospel produces not only inner transformation but outward dignity. Christian freedom is not chaos — it is ordered beauty.",
    [("Romans 13:13","https://www.blueletterbible.org/kjv/rom/13/13/s_1059013","Let us walk <strong>honestly</strong>, as in the day..."),
     ("1 Corinthians 14:40","https://www.blueletterbible.org/kjv/1co/14/40/s_1076040","Let all things be done <strong>decently</strong> and in order."),
     ("1 Thessalonians 4:12","https://www.blueletterbible.org/kjv/1th/4/12/s_1115012","That ye may walk <strong>honestly</strong> toward them that are without..."),
     ("Ephesians 5:3","https://www.blueletterbible.org/kjv/eph/5/3/s_1102003","But fornication, and all uncleanness...let it not be once named among you, as becometh saints."),
     ("Colossians 4:5","https://www.blueletterbible.org/kjv/col/4/5/s_1111005","Walk in wisdom toward them that are without, redeeming the time.")],
    [("G2158","euschēmōn (comely)"),("G5010","taxis (order)"),("G2887","kosmios (orderly, modest)")])

# ===================== TEMPLATE & GENERATION =====================

def make_html(w):
    verses_html = ""
    for ref, url, text in w["verses"]:
        verses_html += f'''            <div class="verse-entry">
                <a href="{url}" target="_blank" class="verse-ref">{ref}</a>
                <div class="verse-text">{text}</div>
            </div>\n'''

    related_html = ""
    for rid, rdesc in w["related"]:
        related_html += f'                <a href="{rid}.html" class="related-word">{rid} - {rdesc}</a>\n'

    num = w["strongs"][1:]
    prefix = w["strongs"][0].lower()
    badge_label = f"{w['strongs']} · {w['lang']} · {w['testament']}"
    orig_dir = f' direction:{w["dir"]};' if w["dir"] == "rtl" else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <link rel="manifest" href="/manifest.json">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="{w['strongs']} — {w['translit']} | USMC Ministries Lexicon">
    <meta property="og:description" content="{w['short_def']} — {w['lang']} word study. Strong's {w['strongs']}.">
    <meta name="description" content="{w['short_def']} — {w['lang']} word study. Strong's {w['strongs']}. USMC Ministries Greek &amp; Hebrew Lexicon.">
    <title>{w['strongs']} — {w['translit']} ({w['short_def'].split(",")[0]}) | USMC Ministries Lexicon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg-dark:#000; --bg-card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; --scarlet:#CC0000; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg-dark); color:var(--white); min-height:100vh; line-height:1.6; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; font-weight:700; }}
        .container {{ max-width:800px; margin:0 auto; padding:20px; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a:link,nav a:visited,nav a:active {{ color:var(--gray) !important; text-decoration:none !important; }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .word-header {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .strongs-badge {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.9rem; padding:4px 14px; border-radius:20px; margin-bottom:15px; }}
        .original-word {{ font-size:3rem; margin:15px 0 10px; color:var(--gold-light);{orig_dir} }}
        .transliteration {{ font-size:1.4rem; color:var(--white); font-style:italic; margin-bottom:8px; }}
        .pos {{ color:var(--gray); font-size:0.95rem; margin-bottom:10px; }}
        .gloss {{ color:var(--gold); font-size:1.1rem; font-weight:600; }}
        .section {{ background:var(--bg-card); border:1px solid var(--border); border-radius:12px; padding:28px; margin-bottom:24px; }}
        .section h2 {{ color:var(--gold); font-size:1.3rem; margin-bottom:16px; }}
        .section p {{ color:var(--white); line-height:1.8; margin-bottom:12px; }}
        .section p em {{ color:var(--gold-light); font-style:italic; }}
        .section p strong {{ color:var(--white); }}
        .verse-entry {{ margin-bottom:16px; padding-left:18px; border-left:2px solid var(--gold); }}
        .verse-ref {{ color:var(--gold); text-decoration:none; font-weight:600; font-size:0.9rem; display:inline-block; margin-bottom:4px; border-bottom:1px dotted var(--gold); }}
        .verse-ref:hover {{ color:var(--gold-light); border-bottom-style:solid; }}
        .verse-text {{ color:var(--white); line-height:1.7; }}
        .verse-text em {{ color:var(--gold-light); font-style:italic; }}
        .verse-text strong {{ color:var(--white); }}
        .related-words {{ display:flex; flex-wrap:wrap; gap:10px; }}
        .related-word {{ display:inline-block; background:rgba(212,175,55,0.1); border:1px solid var(--border); color:var(--gold); text-decoration:none; padding:6px 14px; border-radius:20px; font-size:0.85rem; transition:all 0.2s; }}
        a.related-word:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.2); }}
        .ext-links {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; }}
        .ext-link {{ color:var(--gold); text-decoration:none; padding:8px 18px; border:1px solid var(--border); border-radius:8px; font-size:0.9rem; transition:all 0.2s; }}
        .ext-link:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.1); }}
        .back-link {{ display:inline-block; color:var(--gold); text-decoration:none; margin-bottom:20px; font-size:0.9rem; }}
        .back-link:hover {{ color:var(--gold-light); }}
        footer {{ text-align:center; padding:40px 20px; color:var(--gray); font-size:0.85rem; border-top:1px solid var(--border); margin-top:40px; }}
        footer a {{ color:var(--gold); text-decoration:none; }}
        @media (max-width:640px) {{ .container {{ padding:15px; }} .original-word {{ font-size:2.2rem; }} }}
        .theme-toggle {{ background:none; border:1px solid var(--border); border-radius:50%; width:34px; height:34px; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:1.1rem; transition:all 0.3s; padding:0; margin-left:6px; }}
        .theme-toggle:hover {{ border-color:var(--gold); transform:scale(1.1); }}
        body.light-mode {{ --bg-dark:#FAF8F5; --bg-card:#FFFFFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#FAF8F5; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(250,248,245,0.97); }}
        body.light-mode .section {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode .ext-link {{ border-color:#d4d0c8; }}
        body.light-mode .related-word {{ background:rgba(212,175,55,0.08); border-color:#d4d0c8; }}
        body.light-mode footer {{ border-top-color:#d4d0c8; }}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">Bible Translation Engine</a>
        <a href="../lexicon.html" class="active">Lexicon</a>
        <a href="../blog.html">Blog</a>
        <a href="../links.html">Connect</a>
    </nav>
    <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode" style="position:fixed;top:12px;right:12px;z-index:9999;display:flex;align-items:center;background:rgba(30,30,30,0.85);border:1px solid #333;border-radius:20px;padding:3px 6px;cursor:pointer;font-size:0.7rem;">
        <span style="width:18px;text-align:center;">🌙</span>
        <div style="width:28px;height:14px;background:#444;border-radius:7px;position:relative;margin:0 4px;"><div style="width:10px;height:10px;background:#D4AF37;border-radius:50%;position:absolute;top:2px;left:2px;transition:left 0.3s;"></div></div>
        <span style="width:18px;text-align:center;">☀️</span>
    </div>
    <div class="container">
        <a href="../lexicon.html" class="back-link">← Back to Lexicon</a>
        <div class="word-header">
            <span class="strongs-badge">{badge_label}</span>
            <div class="original-word">{w['original']}</div>
            <div class="transliteration">{w['translit']}</div>
            <div class="pos">{w['pos']}</div>
            <div class="gloss">{w['short_def']}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>{w['full_def']}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>{w['theology']}</p>
        </div>
        <div class="section">
            <h2>Key Bible Verses</h2>
{verses_html}        </div>
        <div class="section">
            <h2>Related Words</h2>
            <div class="related-words">
{related_html}            </div>
        </div>
        <div class="section">
            <h2>External Resources</h2>
            <div class="ext-links">
                <a href="https://www.stepbible.org/?q=strong={w['strongs']}" target="_blank" class="ext-link">📖 STEP Bible</a>
                <a href="https://www.blueletterbible.org/lexicon/{prefix}{num}/kjv/wlc/0-1/" target="_blank" class="ext-link">📘 Blue Letter Bible</a>
                <a href="https://biblehub.com/{w['lang'].lower()}/{num}.htm" target="_blank" class="ext-link">📗 Bible Hub</a>
            </div>
        </div>
    </div>
    <footer>
        <p><strong>USMC Ministries Greek &amp; Hebrew Lexicon</strong></p>
        <p style="margin-top:8px;">© 2026 <a href="../index.html">U.S.M.C. Ministries</a> · <a href="../bible.html">Bible Translation Engine</a></p>
    </footer>
    <script>
    function bteToggleTheme(){{var b=document.body;if(b.classList.contains('light-mode')){{b.classList.remove('light-mode');localStorage.setItem('bte-theme','dark');}}
    else{{b.classList.add('light-mode');localStorage.setItem('bte-theme','light');}}}}
    (function(){{if(localStorage.getItem('bte-theme')==='light'){{document.body.classList.add('light-mode');}}}})();
    </script>
</body>
</html>'''

if __name__ == "__main__":
    created = 0
    for w in WORDS:
        path = os.path.join(LEXICON_DIR, f"{w['strongs']}.html")
        if os.path.exists(path):
            print(f"SKIP {w['strongs']} (exists)")
            continue
        html = make_html(w)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        created += 1
        print(f"CREATED {w['strongs']} — {w['translit']}")
    print(f"\nDone: {created} files created.")
