#!/usr/bin/env python3
"""Batch 41 — expand 25 more entries from the 50-60 word bucket.

Targets: divine names, OT/NT figures, doctrines, solas, theologians,
slang reframes, Beatitudes, and biblical imagery.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'jehovah-jireh': (
        '<p><em>Jehovah-Jireh</em> (יְהוָה יִרְאֶה) — "the LORD will provide" — is the covenant name Abraham gave to the place where God provided the ram caught in the thicket as a substitute for Isaac on Mount Moriah: <em>"And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen"</em> (<em>Genesis 22:14</em>). The Hebrew root <em>raah</em> ("to see") carries both <em>"see"</em> and <em>"see to it"</em>. Provision in Scripture begins with God’s sight: He sees the need before the need lands, and His seeing is itself the provision. The same mountain became the temple-site, and not far from it Christ — the true Lamb — was sacrificed. Jehovah-Jireh stands forever.</p>'
    ),
    'jonah': (
        '<p>Jonah was the reluctant Hebrew prophet of the Northern Kingdom (8th century BC, under Jeroboam II) whose four-chapter book records his flight from God’s call to Nineveh, his repentance in the belly of the great fish, his eight-word sermon to the Assyrian capital (<em>"Yet forty days, and Nineveh shall be overthrown"</em>, <em>Jonah 3:4</em>), and his bitter sulk under the gourd vine when God showed mercy. Christ Himself named Jonah’s three-day burial as the only sign He would give His generation: <em>"For as Jonas was three days and three nights in the whale’s belly; so shall the Son of man be three days and three nights in the heart of the earth"</em> (<em>Matthew 12:40</em>). The reluctant prophet typifies the willing Christ.</p>'
    ),
    'joshua-figure': (
        '<p>Joshua, son of Nun of the tribe of Ephraim, was Moses’ aide and military commander throughout the wilderness years. He was one of the two faithful spies — with Caleb — who urged Israel to enter the land: <em>"Let us go up at once, and possess it; for we are well able to overcome it"</em> (<em>Numbers 13:30; 14:6-9</em>). After Moses’ death, the LORD commissioned him to lead Israel into Canaan: <em>"Be strong and of a good courage"</em> (<em>Joshua 1:6, 7, 9</em>). He led the crossing of the Jordan, the fall of Jericho, the three-campaign conquest, the allotment of tribal territories, and the great covenant renewal at Shechem (<em>"choose you this day whom ye will serve"</em>, <em>Joshua 24:15</em>). His Hebrew name <em>Yehoshua</em> is the same as <em>Jesus</em>.</p>'
    ),
    'lifting-eyes': (
        '<p>Lifting the eyes is the deliberate posture of turning the gaze from the ground or the trouble to the LORD — a discipline as much as a feeling. Scripture marks the act repeatedly. Abraham lifted his eyes and saw the ram caught in the thicket on Moriah (<em>Genesis 22:13</em>). Hagar, dying with her son in the wilderness, lifted her eyes when the angel called and saw a well of water (<em>Genesis 21:19</em>). The Psalmist commands his soul: <em>"I will lift up mine eyes unto the hills, from whence cometh my help. My help cometh from the LORD"</em> (<em>Psalm 121:1-2</em>); <em>"Unto thee lift I up mine eyes, O thou that dwellest in the heavens"</em> (<em>123:1</em>). Christian men learn to look up first.</p>'
    ),
    'lystra': (
        '<p>Lystra was a Roman colony in Lycaonia (south-central Asia Minor) and one of the cities Paul and Barnabas evangelized on the first missionary journey (<em>Acts 14:6-20</em>). They healed a man crippled from birth, and the pagan crowd, speaking in their native Lycaonian dialect, hailed them as the gods Hermes and Zeus and tried to offer sacrifice. The apostles tore their clothes and barely restrained the priests. Then Jews from Antioch and Iconium arrived, turned the crowd, and Paul was stoned and dragged outside the city for dead. He rose, returned to the city, and continued his work. Lystra later became the home of Timothy, Paul’s most beloved spiritual son (<em>Acts 16:1-3</em>).</p>'
    ),
    'meditation': (
        '<p>Meditation, biblically, is the disciplined pondering of God’s Word and works until they shape the heart — the mind walking around the same verse from many angles, like a cow chewing the cud, returning to the same text until it yields its full nourishment. <em>"Blessed is the man that walketh not in the counsel of the ungodly... But his delight is in the law of the LORD; and in his law doth he meditate day and night"</em> (<em>Psalm 1:1-2</em>); <em>"O how love I thy law! it is my meditation all the day"</em> (<em>Psalm 119:97</em>). Christian meditation is not <em>emptying</em> the mind (the Eastern variety) but <em>filling</em> it with God’s Word and turning it over until it produces understanding, prayer, and obedience.</p>'
    ),
    'millstone': (
        '<p>The millstone is the heavy paired stone of the household mill — the upper riding on the lower — used daily to grind grain into flour for the household’s bread. It was so central to life that the Torah forbade taking it in pledge: <em>"No man shall take the nether or the upper millstone to pledge: for he taketh a man’s life to pledge"</em> (<em>Deuteronomy 24:6</em>). To seize the millstone was to starve the family. The millstone also appears as a weight of judgment: Christ’s warning to those who cause little ones to stumble is severe — <em>"It were better for him that a millstone were hanged about his neck, and he cast into the sea"</em> (<em>Luke 17:2; Matthew 18:6</em>).</p>'
    ),
    'night-watch': (
        '<p>A night watch is the guard kept through the dark hours when the household sleeps. Scripture is full of night-watch language. The shepherds <em>"keeping watch over their flock by night"</em> on the Bethlehem hills when the angels announced the Savior (<em>Luke 2:8</em>). The disciples failing to <em>"watch one hour"</em> with Christ in Gethsemane (<em>Matthew 26:40</em>). The Psalmist: <em>"Mine eyes prevent the night watches, that I might meditate in thy word"</em> (<em>Psalm 119:148</em>); <em>"My soul waiteth for the Lord more than they that watch for the morning: I say, more than they that watch for the morning"</em> (<em>Psalm 130:6</em>). Christian men are night-watchmen by trade — watching their own souls, their families, the flock, the world.</p>'
    ),
    'olam': (
        '<p><em>Olam</em> (עוֹלָם) is the Hebrew word for <em>eternity</em> or <em>age</em> — the long duration that recedes beyond view. It is used both backwards (<em>me-olam</em>, "from of old, from ancient times") and forwards (<em>le-olam va‘ed</em>, "forever and ever"). Abraham planted a grove in Beer-sheba <em>"and called there on the name of the LORD, the everlasting God"</em> — <em>El Olam</em> (<em>Genesis 21:33</em>). Moses sings: <em>"Even from everlasting to everlasting, thou art God"</em> (<em>Psalm 90:2</em>). The Hebrew word does not separate "eternity" from "age" as sharply as Greek thought; long duration that exceeds the visible horizon is the concept. YHWH is the <em>El Olam</em> — the God of the unbounded ages, before and behind, beneath and beyond.</p>'
    ),
    'oracle-biblical': (
        '<p>An <em>oracle</em>, in Scripture, is a divine utterance — the very word of God spoken through prophet, priest, or written text. The KJV uses <em>"oracle"</em> with two distinct senses. First, it names the Holy of Holies of the temple, the inner sanctuary: <em>"And the floor of the house he overlaid with gold, within and without. And for the entering of the oracle..."</em> (<em>1 Kings 6:30-31</em>; cf. <em>vv. 5, 19-23</em>). Second, it names the Old Testament Scriptures themselves: <em>"What advantage then hath the Jew?... Much every way: chiefly, because that unto them were committed the oracles of God"</em> (<em>Romans 3:1-2</em>; cf. <em>Hebrews 5:12; 1 Peter 4:11</em>). Oracle is the <em>place</em> and the <em>word</em> together — divine utterance from the appointed source.</p>'
    ),
    'packer': (
        '<p>J. I. Packer (1926-2020) was the English-Canadian Anglican theologian whose <em>Knowing God</em> (1973) became one of the most-read modern Christian books — selling over a million copies. Born in Gloucestershire, educated at Oxford (Corpus Christi, Wycliffe Hall), ordained Church of England priest in 1952, he emigrated to Vancouver in 1979 to teach at Regent College, where he served to the end of his life. His writing combined Reformed conviction (he was a self-described "Latimer Trust Calvinist"), Puritan affection (he loved John Owen above all), and Anglican breadth. Other major works: <em>Evangelism and the Sovereignty of God</em>, <em>A Quest for Godliness</em>, <em>Fundamentalism and the Word of God</em>. He died in Vancouver at 93.</p>'
    ),
    'pleasant-words': (
        '<p>"Pleasant words" is <em>Proverbs 16:24</em>’s image of life-giving speech: <em>"Pleasant words are as an honeycomb, sweet to the soul, and health to the bones."</em> Solomon names the wisdom of speech that nourishes rather than abrades — the kind of words that build others up instead of tearing them down. The Hebrew <em>noʿam</em> ("pleasantness") is the same word David uses of YHWH’s own beauty: <em>"to behold the beauty [no‘am] of the LORD"</em> (<em>Psalm 27:4</em>). Pleasant words at their best therefore partake of divine pleasantness. Paul commands the same: <em>"Let no corrupt communication proceed out of your mouth, but that which is good to the use of edifying, that it may minister grace unto the hearers"</em> (<em>Ephesians 4:29</em>).</p>'
    ),
    'quiver-full': (
        '<p>"A quiver full" is the biblical image of children as the household’s arrows: weapons given by God for the long campaign of family, faith, witness, and dominion. <em>Psalm 127:3-5</em> spells it out: <em>"Lo, children are an heritage of the LORD: and the fruit of the womb is his reward. As arrows are in the hand of a mighty man; so are children of the youth. Happy is the man that hath his quiver full of them: he shall not be ashamed, but they shall speak with the enemies in the gate."</em> The image is masculine, militant, and forward-looking. Children are not consumer goods; they are arrows. The Christian household is an armory — and the man whose quiver is full has weapons for the long war.</p>'
    ),
    'rahab-faith': (
        '<p>Rahab was the Canaanite prostitute in Jericho who hid the two Israelite spies sent by Joshua, confessed faith in YHWH (<em>"the LORD your God, he is God in heaven above, and in earth beneath"</em>, <em>Joshua 2:11</em>), and tied the scarlet cord in her window as the sign of her household’s deliverance. When the walls fell, Rahab and her father’s house were spared (<em>Joshua 6:22-25</em>). She married into Israel — taking Salmon as husband — and became the great-great-grandmother of King David and an ancestress of Christ (<em>Matthew 1:5</em>). She is honored twice in the New Testament faith-rolls: <em>Hebrews 11:31</em> and <em>James 2:25</em>. The Gentile harlot becomes the great-grandmother of the King.</p>'
    ),
    'savior': (
        '<p>"Savior" is one who saves — and in Scripture it is applied first to God Himself as the deliverer of His people. <em>"I, even I, am the LORD; and beside me there is no saviour"</em> (<em>Isaiah 43:11</em>). It is then applied specifically to Christ, who is the LORD become flesh to save: the angel told Joseph, <em>"and thou shalt call his name JESUS: for he shall save his people from their sins"</em> (<em>Matthew 1:21</em>). The angels at Bethlehem announced, <em>"For unto you is born this day in the city of David a Saviour, which is Christ the Lord"</em> (<em>Luke 2:11</em>). Savior is not a job description He took on optionally; it is the very name given by the angel before His birth.</p>'
    ),
    'simon-magus': (
        '<p>Simon Magus was the Samaritan sorcerer who had astonished his city with his arts <em>"giving out that himself was some great one"</em> (<em>Acts 8:9</em>) — when Philip the evangelist arrived preaching the gospel. Simon professed faith, was baptized, and remained with Philip, marveling at the miracles. When Peter and John came down from Jerusalem and conferred the Holy Spirit by laying on of hands, Simon offered money for the same power: <em>"Give me also this power, that on whomsoever I lay hands, he may receive the Holy Ghost"</em> (<em>8:19</em>). Peter’s rebuke is severe: <em>"Thy money perish with thee... Thou hast neither part nor lot in this matter: for thy heart is not right in the sight of God"</em>. From him is named the sin of <em>simony</em> — buying or selling ecclesial office.</p>'
    ),
    'soli-deo-gloria': (
        '<p><em>Soli Deo Gloria</em> ("to God alone be glory") is the fifth and crowning Reformation <em>sola</em> — the confession that God alone is worthy of all glory in every sphere of life. Since salvation is a work of God from beginning to end — from election before the foundation of the world (<em>Ephesians 1:4</em>) through justification, sanctification, perseverance, to final glorification — all the credit belongs to Him. <em>"For of him, and through him, and to him, are all things: to whom be glory for ever. Amen"</em> (<em>Romans 11:36</em>). The principle extends beyond salvation to all of life. The Westminster Shorter Catechism Q1: <em>"Man’s chief end is to glorify God, and to enjoy him forever."</em> Bach signed his manuscripts SDG.</p>'
    ),
    'standard-bearer': (
        '<p>A standard-bearer is the soldier appointed to carry the unit’s ensign — a position of conspicuous danger (the enemy aims for the colors first) and conspicuous honor (the standard is the unit’s soul). Isaiah names the LORD Himself in the office: <em>"When the enemy shall come in like a flood, the Spirit of the LORD shall lift up a standard against him"</em> (<em>Isaiah 59:19</em>). The Spirit Himself is the kingdom’s standard-bearer. Earlier, the prophet had named the Messiah as the standard: <em>"there shall be a root of Jesse, which shall stand for an ensign of the people; to it shall the Gentiles seek"</em> (<em>Isaiah 11:10</em>). Christ is the standard; the Spirit lifts it; the saints rally to it.</p>'
    ),
    'vineyard-keeper': (
        '<p>The vineyard keeper is the patient husbandman of grapes — pruner, watcher, harvester. Scripture is densely vineyard-imaged. Israel is the LORD’s vineyard (<em>Isaiah 5:1-7</em>; <em>Psalm 80:8-19</em>). Christ is the true vine: <em>"I am the true vine, and my Father is the husbandman... Abide in me, and I in you"</em> (<em>John 15:1, 4</em>). The Father is the vinedresser; the saints are branches; the branch that bears no fruit is taken away, and the branch that bears is pruned that it may bear more. Pastoral ministry is vineyard-keeping: pruning false teaching, watching against wolves and weeds, defending the vine, gathering the harvest at the appointed time. The vineyard keeper’s art is patient discipline.</p>'
    ),
    'word-of-god': (
        '<p>The Word of God is God’s active speech — and Scripture uses the phrase across four interlocking senses. First, the <em>spoken</em> Word that creates and sustains: <em>"By the word of the LORD were the heavens made"</em> (<em>Psalm 33:6</em>); <em>"upholding all things by the word of his power"</em> (<em>Hebrews 1:3</em>). Second, the <em>written</em> Word that is Scripture: <em>"All scripture is given by inspiration of God"</em> (<em>2 Timothy 3:16</em>). Third, the <em>incarnate</em> Word that is Christ: <em>"And the Word was made flesh, and dwelt among us"</em> (<em>John 1:14</em>). Fourth, the <em>preached</em> Word that calls and saves: <em>"faith cometh by hearing, and hearing by the word of God"</em> (<em>Romans 10:17</em>). All four senses converge in one God who speaks.</p>'
    ),
    'word-up': (
        '<p>"Word up" is a late-1980s / 90s hip-hop affirmation — meaning <em>agreed, well said, you speak truth</em>. It is the verbal companion to the earlier-defined Gen-X "Word" entry, used to stamp a sentence as accurate. The slang is healthy in its instinct: words have weight, and a truth well-spoken deserves a verbal stamp of agreement. Scripture’s own word-and-amen pattern points at the same thing — affirmation that says, <em>"so it is, let it stand."</em> <em>"For all the promises of God in him are yea, and in him Amen, unto the glory of God by us"</em> (<em>2 Corinthians 1:20</em>). The Christian alternative is <em>"amen"</em> — older, weightier, ultimately the same gesture. Speak truth; say amen.</p>'
    ),
    'yapping': (
        '<p>"Yapping" is current slang for talking excessively — often deployed dismissively to label someone whose speech is unwelcome or whose point the listener does not want to engage. The slang is rhetorically a kill-switch. Scripture has its own category for excessive talk: the <em>"multitude of words"</em>: <em>"In the multitude of words there wanteth not sin: but he that refraineth his lips is wise"</em> (<em>Proverbs 10:19</em>); <em>"A fool also is full of words: a man cannot tell what shall be"</em> (<em>Ecclesiastes 10:14</em>). The slang is right that incessant talk is a real problem — but the Bible aims the diagnosis <em>inward</em> (<em>"am I yapping?"</em>) rather than outward (<em>"you are yapping"</em>). Examine your own speech first.</p>'
    ),
    'almsgiving': (
        '<p>Almsgiving is charitable giving to the poor — and in Scripture it is one of the three pillars of Jewish piety Christ assumed His followers would practice (alongside prayer and fasting; <em>Matthew 6</em>). Christ does not say <em>"if"</em> you give alms; He says <em>"when thou doest alms"</em> (<em>6:2</em>). The giving is to be done quietly — not before men, not announced, not publicized: <em>"But when thou doest alms, let not thy left hand know what thy right hand doeth: That thine alms may be in secret: and thy Father which seeth in secret himself shall reward thee openly"</em> (<em>6:3-4</em>). The Father who sees in secret rewards openly. Tabitha at Joppa was <em>"full of good works and almsdeeds which she did"</em> (<em>Acts 9:36</em>).</p>'
    ),
    'aloe': (
        '<p>Aloe is a fragrant resinous wood (probably eaglewood, <em>Aquilaria</em>, distinct from the modern medicinal aloe-vera plant) used to perfume garments, beds, and burial cloths in the ancient Near East. The Bridegroom of <em>Psalm 45:8</em> wears it: <em>"All thy garments smell of myrrh, and aloes, and cassia, out of the ivory palaces, whereby they have made thee glad."</em> Proverbs uses it of the seductress’s perfumed bed (<em>7:17</em>); the Song of Solomon names it in the spice-garden of the bride (<em>4:14</em>). And Nicodemus brought it, mingled with myrrh, in great quantity to anoint the body of Jesus for burial: <em>"about an hundred pound weight"</em> (<em>John 19:39</em>). The Bridegroom’s burial-aloe became the resurrection-fragrance.</p>'
    ),
    'beatitude-1': (
        '<p>The first Beatitude of Christ’s Sermon on the Mount: <em>"Blessed are the poor in spirit: for theirs is the kingdom of heaven"</em> (<em>Matthew 5:3</em>). The Greek <em>ptōchos</em> denotes the destitute, the bankrupt, the one who has nothing of his own to bring — a stronger word than mere financial poverty. Spiritual poverty is the soul’s recognition of <em>utter dependence</em> on God’s grace: <em>"I am wretched, and miserable, and poor, and blind, and naked"</em> (<em>Revelation 3:17</em>). It is the doorway to the kingdom — the opposite of the rich-young-ruler self-sufficiency that walked away from Christ grieved. Every other Beatitude grows from this root. The kingdom is for the spiritually bankrupt who come to Christ empty-handed.</p>'
    ),
}

BD_RE = re.compile(r'(<div class="biblical-def">)(.*?)(</div>)', re.DOTALL)

def patch(slug, new_inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return False, 'file missing'
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_html, n = BD_RE.subn(
        rf'\g<1>\n                {new_inner}\n            \g<3>',
        html, count=1)
    if n == 0:
        return False, 'pattern not matched'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'

def main():
    ok, fail = 0, 0
    for slug, new in EXPANSIONS.items():
        success, reason = patch(slug, new)
        if success:
            ok += 1
        else:
            fail += 1
            print(f'  FAIL {slug}: {reason}')
    print(f'Expanded {ok}/{ok+fail} entries')

if __name__ == '__main__':
    main()
