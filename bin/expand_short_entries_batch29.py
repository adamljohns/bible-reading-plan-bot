#!/usr/bin/env python3
"""Batch 29 — expand 25 more thin entries to 90-110 words each.

Targets: NT companions, OT figures, biblical imagery, slang reframes,
divine names, and disciplines from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'turtledove': (
        '<p>The turtledove is a small migratory dove whose annual return to the land of Israel marks the renewal of the year. <em>"The flowers appear on the earth; the time of the singing of birds is come, and the voice of the turtle is heard in our land"</em> (<em>Song of Solomon 2:12</em>). It served three biblical functions: a permitted sacrifice for the poor under Mosaic law (<em>Leviticus 1:14; 5:7; 12:6, 8</em>) — Mary and Joseph offered <em>"a pair of turtledoves, or two young pigeons"</em> at Christ’s presentation (<em>Luke 2:24</em>); an emblem of faithful conjugal love (<em>Song of Solomon</em>); and a prophetic voice announcing the seasons of the LORD: <em>"the turtle and the crane and the swallow observe the time of their coming; but my people know not the judgment of the LORD"</em> (<em>Jeremiah 8:7</em>).</p>'
    ),
    'tychicus': (
        '<p>Tychicus was a beloved brother and faithful minister whom Paul sent on multiple critical errands across the Roman world. He carried the Ephesian letter and was charged to comfort the saints with news of the apostle: <em>"that ye also may know my affairs, and how I do, Tychicus, a beloved brother and faithful minister in the Lord, shall make known to you all things"</em> (<em>Ephesians 6:21-22</em>). He carried the Colossian letter under the same commission (<em>Colossians 4:7-9</em>). Paul considered sending him to relieve Titus on Crete (<em>Titus 3:12</em>), and dispatched him to Ephesus during his second imprisonment (<em>2 Timothy 4:12</em>). Tychicus is the model of the faithful courier whose ministry is unspectacular but indispensable.</p>'
    ),
    'wormwood': (
        '<p>Wormwood is a bitter aromatic shrub of the wilderness (<em>Artemisia absinthium</em>) — and in Scripture it becomes the figure of bitter consequences for sin, of poisoned justice, and of apostasy. <em>"For the lips of a strange woman drop as an honeycomb... but her end is bitter as wormwood"</em> (<em>Proverbs 5:3-4</em>); <em>"Ye who turn judgment to wormwood, and leave off righteousness in the earth"</em> (<em>Amos 5:7</em>; cf. <em>6:12</em>); <em>"Behold, I will feed them, even this people, with wormwood"</em> (<em>Jeremiah 9:15; 23:15</em>). In <em>Revelation 8:10-11</em>, the third trumpet drops a star called Wormwood that turns one-third of the rivers and springs bitter, and many die of the waters. Sin always tastes sweet first and bitter last.</p>'
    ),
    'yhwh-roi': (
        '<p><em>YHWH-Roi</em> (יְהוָה רֹעִי) — "the LORD my Shepherd" — is David’s covenant name for YHWH in the most beloved psalm in the world: <em>"The LORD is my shepherd; I shall not want"</em> (<em>Psalm 23:1</em>). The shepherding image is foundational across Scripture. YHWH leads (<em>v. 2</em>), restores (<em>v. 3</em>), accompanies through the valley of the shadow of death (<em>v. 4</em>), feeds in the presence of enemies (<em>v. 5</em>), and pursues with mercy all the days of life (<em>v. 6</em>). Christ takes up the title in <em>John 10:11, 14</em>: <em>"I am the good shepherd: the good shepherd giveth his life for the sheep... I am the good shepherd, and know my sheep, and am known of mine."</em></p>'
    ),
    'zealous-jealousy': (
        '<p>Zealous jealousy is the burning, possessive love God Himself confesses for His people — the fire that will not share the bride with another. <em>"Thou shalt not bow down thyself to them, nor serve them: for I the LORD thy God am a jealous God"</em> (<em>Exodus 20:5</em>); <em>"For the LORD thy God is a consuming fire, even a jealous God"</em> (<em>Deuteronomy 4:24</em>); <em>"the LORD, whose name is Jealous, is a jealous God"</em> (<em>Exodus 34:14</em>). Scripture insists that <em>jealous</em> is one of God’s <em>names</em>, not a defect. It is the Husband’s right reaction to the Bride’s wandering eye. The same fire Paul wishes to see in pastors over their flocks: <em>"I am jealous over you with godly jealousy"</em> (<em>2 Corinthians 11:2</em>).</p>'
    ),
    'agrippa': (
        '<p>Herod Agrippa II (c. AD 27-100) was the great-grandson of Herod the Great and the last reigning Herod — ruler of small territories in northern Palestine and overseer of the temple in Jerusalem under Roman delegation. He visited Festus the new procurator at Caesarea, and Festus invited him to hear Paul’s case (<em>Acts 25:13-26:32</em>). Paul, knowing Agrippa was expert in Jewish customs and prophecies, made his bold defense before him — recounting his Damascus-road encounter and pressing the gospel directly. Agrippa famously answered: <em>"Almost thou persuadest me to be a Christian"</em> (<em>Acts 26:28</em>). Paul’s reply pierces still: <em>"I would to God, that not only thou, but also all that hear me this day, were both almost, and altogether such as I am, except these bonds."</em></p>'
    ),
    'bowels': (
        '<p>"Bowels" — the KJV’s favored translation of the Hebrew <em>meʿim</em> and the Greek <em>splanchnon</em> — names the seat of compassion, mercy, and tender affection. It is the somatic theology of love: deep feeling is located in the gut, not the head. <em>"Put on therefore, as the elect of God, holy and beloved, bowels of mercies, kindness, humbleness of mind, meekness, longsuffering"</em> (<em>Colossians 3:12</em>). Christ was repeatedly <em>"moved with compassion"</em> — the Greek <em>esplagchnisthe</em>, literally <em>"moved in His bowels"</em> — whenever He saw a crowd, a leper, a widow, a need (<em>Matthew 9:36; 14:14; Mark 1:41; Luke 7:13</em>). Modern English has lost the word; modern hearts have often lost the thing. Recover both.</p>'
    ),
    'cast-burden': (
        '<p>"Cast your burden" names the deliberate, active transfer of weight from one’s own shoulders to YHWH’s. The command is sharp and assertive: <em>"Cast thy burden upon the LORD, and he shall sustain thee: he shall never suffer the righteous to be moved"</em> (<em>Psalm 55:22</em>). Peter picks up the same verb in <em>1 Peter 5:7</em>: <em>"Casting all your care upon him; for he careth for you."</em> The Greek participle <em>epirhipsantes</em> ("having cast") is an aorist of decisive action — not a slow surrender but a deliberate handoff. The Christian man does not pretend to be carrying nothing; he hands over what God has invited him to hand over and trusts the LORD with what he can no longer hold. Cast it. The arms beneath are everlasting.</p>'
    ),
    'day-of-yhwh': (
        '<p>The Day of YHWH (Old Testament <em>Yom YHWH</em>) is the eschatological day of God’s decisive intervention, bringing both judgment of the wicked and salvation of the faithful. It is a major prophetic theme across <em>Joel 1-2; Amos 5:18-20; Isaiah 13:6-13; Zephaniah 1:7-18; Malachi 4:1-5</em>. Often it is near-and-far structured: an immediate judgment-day (Assyrian invasion, Babylonian exile, locust devastation) prefigures the ultimate, cosmic Day of the LORD. Amos warns Israel not to long for it lightly: <em>"Woe unto you that desire the day of the LORD! to what end is it for you? the day of the LORD is darkness, and not light"</em> (<em>Amos 5:18</em>). The New Testament identifies it with the second coming of Christ (<em>1 Thessalonians 5:2</em>; <em>2 Peter 3:10</em>).</p>'
    ),
    'demas': (
        '<p>Demas is one of the saddest character arcs in the New Testament — appearing in just three Pauline texts. In <em>Colossians 4:14</em> he stands at Paul’s side: <em>"Luke, the beloved physician, and Demas, greet you."</em> In <em>Philemon 24</em> he is listed among <em>"my fellowlabourers"</em>. But in <em>2 Timothy 4:10</em>, written just before Paul’s martyrdom, the line falls: <em>"Demas hath forsaken me, having loved this present world, and is departed unto Thessalonica."</em> From fellow-laborer to deserter — and the diagnosis is the most ordinary failure imaginable: love of this present world. Many men who run well for years are lost the same way. Christian men must guard the heart against the love of <em>now</em>, late as well as early.</p>'
    ),
    'discipline-biblical': (
        '<p>Biblical discipline runs in two forms — divine and ecclesial — and both are acts of love, not cruelty. The Lord disciplines those He loves: <em>"For whom the Lord loveth he chasteneth, and scourgeth every son whom he receiveth"</em> (<em>Hebrews 12:6</em>). Divine discipline is painful for the present but produces <em>"the peaceable fruit of righteousness unto them which are exercised thereby"</em> (<em>Hebrews 12:11</em>). Church discipline is prescribed by Christ in <em>Matthew 18:15-17</em> and unfolded by Paul in <em>1 Corinthians 5</em> — private confrontation, witnessed warning, public exclusion if needed, all aimed at restoration to repentance. The church that cannot discipline cannot disciple; the father who cannot discipline cannot father. Discipline absent is not love present; it is love withheld.</p>'
    ),
    'doorpost': (
        '<p>The doorpost is the vertical beam on either side of a doorway — and Scripture loads it with three theologically charged uses. First, the Passover blood: <em>"And they shall take of the blood, and strike it on the two side posts and on the upper door post of the houses"</em> (<em>Exodus 12:7</em>) — the sign over which the destroying angel passed. Second, the bondservant’s ear: a Hebrew slave who refused freedom was brought <em>"unto the door, or unto the door post; and his master shall bore his ear through with an aul"</em> (<em>Exodus 21:6</em>) — willing perpetual service. Third, the inscribed Word: <em>"thou shalt write them upon the posts of thy house, and on thy gates"</em> (<em>Deuteronomy 6:9</em>) — the basis of the <em>mezuzah</em>. Sanctify the threshold.</p>'
    ),
    'flattery': (
        '<p>Flattery is smooth, insincere praise designed to manipulate the hearer for the speaker’s gain. Solomon warned: <em>"A flattering mouth worketh ruin"</em> (<em>Proverbs 26:28</em>); <em>"a man that flattereth his neighbour spreadeth a net for his feet"</em> (<em>Proverbs 29:5</em>). David lamented: <em>"They speak vanity every one with his neighbour: with flattering lips and with a double heart do they speak"</em> (<em>Psalm 12:2-3</em>). Paul disowns it: <em>"For neither at any time used we flattering words, as ye know, nor a cloke of covetousness; God is witness"</em> (<em>1 Thessalonians 2:5</em>). Flattery is the public face of private deceit — and the lubricant of every false church, false political alliance, and false friendship. Christian men must refuse to give it and refuse to receive it.</p>'
    ),
    'front-porch': (
        '<p>The front porch is the covered, semi-public space facing the street — not yet inside, no longer outside. Functionally, it is the modern American household’s vestige of the ancient courtyard: a place where neighbors are seen, greeted, and (sometimes) drawn in. Many neighborhoods have lost it — replaced by garage-door entry and backyard-deck retreat — and a vital social organ has atrophied with it. Where the front porch dies, neighbors become strangers. Christian families should consciously rebuild the threshold: sit on the porch in the evening, wave at every car, greet every walker, and let the table inside be no farther than one porch-conversation away. Hospitality begins with being <em>visible</em>. <em>"Use hospitality one to another without grudging"</em> (<em>1 Peter 4:9</em>).</p>'
    ),
    'gomorrah': (
        '<p>Gomorrah was the companion city of Sodom on the Jordan plain — destroyed alongside Sodom by fire and brimstone from the LORD out of heaven (<em>Genesis 19:24-28</em>). The cities had become so wicked that <em>"the cry of Sodom and Gomorrah is great, and because their sin is very grievous"</em> (<em>Genesis 18:20</em>); not ten righteous souls could be found in either. Their destruction was so total that the plain became a wasteland of salt and ashes. In Scripture the two names function thereafter as a single, permanent benchmark of cities under divine wrath: the prophets invoke them (<em>Isaiah 1:9-10; Jeremiah 49:18; Ezekiel 16:48-50</em>); Christ Himself does (<em>Matthew 10:15; 11:23-24</em>); Peter and Jude both apply them to apostate communities. God ends what He has long warned.</p>'
    ),
    'hashtag-life': (
        '<p>"Hashtag life" names the verbal habit of saying <em>"hashtag"</em> before a curated label — <em>"hashtag blessed,"</em> <em>"hashtag goals,"</em> <em>"hashtag squad"</em> — either earnestly to brand one’s life or, more often, ironically to satirize the curated-self instinct. The slang exposes the deeper social-media-age temptation: every life moment becomes content, every meal becomes a photo, every relationship becomes a performance for the absent audience. Christ’s diagnosis cuts under both the earnest and the ironic version: <em>"Take heed that ye do not your alms before men, to be seen of them: otherwise ye have no reward of your Father which is in heaven"</em> (<em>Matthew 6:1</em>). The hidden life lived before God is the only one with an audience that matters.</p>'
    ),
    'honesty': (
        '<p>Honesty (the noun for what the truthful man <em>does</em>) is the saint’s disposition of truthful dealing in word and act — words matching meanings, transactions matching their stated terms, walk matching profession. Paul commends what is <em>"honest in the sight of all men"</em> (<em>Romans 12:17</em>; <em>2 Corinthians 8:21</em>) and prays that the saints may <em>"lead a quiet and peaceable life in all godliness and honesty"</em> (<em>1 Timothy 2:2</em>). It is distinct from <em>cleverness about truth</em> — the lawyerly skill of producing technically true statements designed to deceive. Honest is plain; honest is direct; honest does not hide behind precision. The Christian man’s yes is yes and his no is no, without smaller print. <em>"Whatsoever things are honest... think on these things"</em> (<em>Philippians 4:8</em>).</p>'
    ),
    'jericho': (
        '<p>Jericho was the walled "city of palms" in the Jordan valley — the first Canaanite stronghold Israel encountered after crossing the Jordan into the promised land. By the LORD’s command, the armed men and seven priests with rams’ horns marched silently around the city once a day for six days, then seven times on the seventh day; on the long blast and the people’s shout the walls fell flat (<em>Joshua 6</em>). Rahab and her father’s house were spared (<em>Joshua 6:22-25</em>) and grafted into Israel. Centuries later, Jericho returned to Scripture under Christ’s ministry: He passed through it on the way to Jerusalem, healed blind Bartimaeus (<em>Mark 10:46-52</em>), and called Zacchaeus the tax collector down from the sycamore tree (<em>Luke 19:1-10</em>).</p>'
    ),
    'joab-figure': (
        '<p>Joab son of Zeruiah — David’s sister — was the captain of David’s army through nearly his entire reign. He was a brilliant general and fierce loyalist who saved David’s kingdom many times over: at Rabbah, at Helam, against Absalom’s rebellion. But he was also a serial transgressor whose blood-debt finally exceeded his record. He murdered Abner in revenge for his brother Asahel; he killed Absalom against David’s explicit order; he assassinated Amasa with treachery at Gibeon’s great stone; and at the end he supported Adonijah’s coup against Solomon. David’s deathbed instructions called for justice: <em>"let not his hoar head go down to the grave in peace"</em> (<em>1 Kings 2:6</em>). Solomon executed him at the horns of the altar.</p>'
    ),
    'joab': (
        '<p>Joab, son of David’s sister Zeruiah, was commander of David’s army — effective in war but ruthless and politically scheming. His name marks four notorious killings. He murdered Abner at Hebron, in revenge for Abner’s self-defense killing of his brother Asahel (<em>2 Samuel 3:27</em>). He killed Absalom against David’s order (<em>2 Samuel 18:14</em>). He arranged Uriah the Hittite’s death by abandoning him on the front line at David’s order (<em>2 Samuel 11:14-17</em>). He treacherously stabbed Amasa, his replacement, at Gibeon (<em>2 Samuel 20:9-10</em>). He backed Adonijah’s coup at the end. Solomon, on David’s deathbed instructions, executed him at the horns of the altar (<em>1 Kings 2:28-34</em>). The blood of his kingdom-building eventually reached his own house.</p>'
    ),
    'lift-up-eyes': (
        '<p>"Lift up the eyes" is the deliberate act of redirecting one’s gaze from the immediate to the eternal, from the trouble to the Helper, from the self to the LORD. <em>Psalm 121:1</em> opens with the pilgrim’s gesture: <em>"I will lift up mine eyes unto the hills, from whence cometh my help. My help cometh from the LORD, which made heaven and earth."</em> The verb is a discipline, not a feeling. Abraham lifted up his eyes and saw the ram caught in the thicket (<em>Genesis 22:13</em>). The Levite of Bethany’s eyes were lifted, and he saw <em>"the LORD standing upon the wall"</em> (<em>Amos 7:7</em>). Christian men learn to look up first. The horizon shapes the heart.</p>'
    ),
    'metsudah': (
        '<p><em>Metsudah</em> (מְצוּדָה) is the Hebrew word for <em>fortress</em> — specifically a mountain stronghold, the cliff-side citadel rather than a walled city. David hid in such strongholds (<em>metsudoth</em>) when fleeing Saul: <em>"And David said unto his father and to his mother... Let my father and my mother, I pray thee, come forth, and be with you, till I know what God will do for me. And he brought them before the king of Moab: and they dwelt with him all the while that David was in the hold"</em> (<em>1 Samuel 22:3-5; 23:14</em>). The word then becomes a divine title in the Psalms: <em>"The LORD is my rock, and my fortress [metsudah], and my deliverer"</em> (<em>Psalm 18:2</em>; cf. <em>31:3; 71:3; 91:2; 144:2</em>). YHWH Himself is the mountain stronghold of the saint.</p>'
    ),
    'npc': (
        '<p>"NPC" — a gaming term for "non-player character," the scripted background figures populating a video game — has been repurposed online to describe a person you regard as having no original thoughts, someone running on autopilot or merely echoing a script. The slang flatters the speaker (<em>"I am a real player; you are background"</em>) and dehumanizes the target. Scripture has only one category for human beings: image-bearer of God. <em>"So God created man in his own image, in the image of God created he him; male and female created he them"</em> (<em>Genesis 1:27</em>). There are no NPCs. Every man you despise has an immortal soul; every "background character" is bound for either heaven or hell. Never use the slang.</p>'
    ),
    'quail': (
        '<p>The quail was the migratory bird sent twice by God to feed Israel in the wilderness — and the two episodes preach opposite lessons. In <em>Exodus 16:13</em>, the quail came in the evening with the manna in the morning as pure provision: <em>"in the evening the quails came up, and covered the camp."</em> In <em>Numbers 11</em>, after the people’s lustful complaint that they had no meat, the LORD sent quail in such quantity that they piled three feet deep around the camp — <em>"and while the flesh was yet between their teeth, ere it was chewed, the wrath of the LORD was kindled against the people, and the LORD smote the people with a very great plague"</em> (<em>11:33</em>). The quail teaches the saint: God answers prayers two ways — with bread, or with <em>"leanness of soul"</em> (<em>Psalm 106:15</em>).</p>'
    ),
    'sanctus': (
        '<p>The <em>Sanctus</em> (Latin "holy") is the threefold <em>"Holy, Holy, Holy"</em> sung by the seraphim around the throne in Isaiah’s vision: <em>"And one cried unto another, and said, Holy, holy, holy, is the LORD of hosts: the whole earth is full of his glory"</em> (<em>Isaiah 6:3</em>). The same chant is heard from the four living creatures around the throne in <em>Revelation 4:8</em>: <em>"Holy, holy, holy, Lord God Almighty, which was, and is, and is to come."</em> The historic eucharistic liturgy incorporates it as the congregation’s response to the prefatory dialogue — joining the church on earth with the worship of heaven. To sing the <em>Sanctus</em> is to add our voice to the seraphim and elders who have not stopped for two thousand years.</p>'
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
