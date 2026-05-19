#!/usr/bin/env python3
"""Batch 33 — expand 25 more entries from the 50-60 word bucket.

Targets: Hebrew vocab, OT/NT figures, doctrines, hermeneutics,
slang reframes, virtues, and household disciplines.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'shaking-of-nations': (
        '<p>The "shaking of the nations" is Haggai’s great post-exilic prophecy: <em>"Yet once, it is a little while, and I will shake the heavens, and the earth, and the sea, and the dry land; And I will shake all nations, and the desire of all nations shall come: and I will fill this house with glory, saith the LORD of hosts"</em> (<em>Haggai 2:6-7</em>). The prophecy promised that the latter temple’s glory would exceed the former — fulfilled in the coming of Christ to the second temple. The author of Hebrews picks it up and points it forward to the final, cosmic shaking: <em>"this word, Yet once more, signifieth the removing of those things that are shaken... that those things which cannot be shaken may remain"</em> (<em>Hebrews 12:26-29</em>). The kingdom of Christ alone is unshakable.</p>'
    ),
    'silent-before-god': (
        '<p>Silence before God is the settled hush Habakkuk commands the whole earth to keep when the LORD is in His holy temple: <em>"But the LORD is in his holy temple: let all the earth keep silence before him"</em> (<em>Habakkuk 2:20</em>). Zephaniah and Zechariah echo the call (<em>Zephaniah 1:7</em>; <em>Zechariah 2:13</em>). It is also the saint’s deliberate cessation of self-talk — not the silence of sullenness or the absence of words, but the silence of attention. <em>"Be still, and know that I am God"</em> (<em>Psalm 46:10</em>); <em>"Truly my soul waiteth upon God"</em> (<em>Psalm 62:1</em>). Modern Christians lost in noise must recover the discipline: silence the phone, silence the inner chatter, and listen for the still small voice.</p>'
    ),
    'sparrow': (
        '<p>The sparrow is a small common bird sold cheaply in first-century markets — two sold for a farthing, five for two farthings (<em>Matthew 10:29</em>; <em>Luke 12:6</em>). In Scripture it becomes the icon of the saint’s value in the Father’s eyes: <em>"Are not two sparrows sold for a farthing? and one of them shall not fall on the ground without your Father. But the very hairs of your head are all numbered. Fear ye not therefore, ye are of more value than many sparrows"</em> (<em>Matthew 10:29-31</em>). The Psalmist also envies the sparrow that finds a nest near God’s altar: <em>"Yea, the sparrow hath found an house, and the swallow a nest for herself... even thine altars, O LORD of hosts"</em> (<em>Psalm 84:3</em>).</p>'
    ),
    'stranger': (
        '<p>A stranger (Hebrew <em>ger</em>, Greek <em>xenos</em>) is a foreigner, sojourner, or person outside the covenant community — and in Scripture the stranger is the object of explicit, repeated divine concern. Moses commands: <em>"Love ye therefore the stranger: for ye were strangers in the land of Egypt"</em> (<em>Deuteronomy 10:19</em>); the law forbids oppressing him (<em>Exodus 22:21; 23:9</em>) and commands leaving the corners of the field for him to glean (<em>Leviticus 19:9-10</em>). Christ identifies Himself with the stranger in the great judgment scene: <em>"I was a stranger, and ye took me in"</em> (<em>Matthew 25:35</em>). Hebrews calls believers themselves <em>"strangers and pilgrims on the earth"</em> (<em>Hebrews 11:13</em>) — every saint a sojourner welcomed by God.</p>'
    ),
    'tea': (
        '<p>"Tea" is modern slang for gossip — <em>"spill the tea,"</em> <em>"give me all the tea"</em> — the inside story, the dirt, what people are not supposed to know. The slang aestheticizes gossip as a social glue, a flavor to share with friends over a kitchen table. Scripture’s diagnosis is unsoftened: <em>"A talebearer revealeth secrets: but he that is of a faithful spirit concealeth the matter"</em> (<em>Proverbs 11:13</em>); <em>"The words of a talebearer are as wounds, and they go down into the innermost parts of the belly"</em> (<em>Proverbs 18:8; 26:22</em>); <em>"A whisperer separateth chief friends"</em> (<em>Proverbs 16:28</em>). Gossip is sin even when delicious. Christian men refuse to be either consumers or dispensers of <em>tea</em>.</p>'
    ),
    'training-biblical': (
        '<p>Training, in Scripture, is deliberate, repeated practice that shapes the saint’s body and soul for godliness. Paul commands it of Timothy: <em>"exercise thyself rather unto godliness. For bodily exercise profiteth little: but godliness is profitable unto all things, having promise of the life that now is, and of that which is to come"</em> (<em>1 Timothy 4:7-8</em>). The Greek verb <em>gymnazō</em> (from which our word <em>gymnasium</em>) names the discipline of the athlete. The saint trains for fitness in righteousness as the athlete trains for the games — through repeated, ordinary acts of obedience, Scripture intake, prayer, fasting, and accountability. Spiritual maturity is built, not granted; the unexercised soul atrophies just as surely as the unexercised body.</p>'
    ),
    'tubular': (
        '<p>"Tubular" is the 1980s Gen-X surfer-coded superlative for excellent or awesome — a wave so perfectly curling that one rides through its tube. The slang is era-stamped, immediately recognizable as Valley-Girl / early-Gen-X linguistic furniture (<em>"That’s totally tubular!"</em>). The vocabulary category is the same as <em>"da bomb," "the bomb," "lit," "fire," "sick"</em> — every generation reinvents the superlative for "excellent." Scripture’s observation cuts to the heart of why: <em>"For where your treasure is, there will your heart be also"</em> (<em>Matthew 6:21</em>). What you stamp with the superlative reveals your hierarchy of value. The slang itself is colorful and harmless. The instinct it reveals deserves attention.</p>'
    ),
    'unsearchable': (
        '<p>"Unsearchable" — KJV for what is past finding out — appears at the height of doxology in Scripture, not at the limit of frustration. Job confesses it: <em>"Which doeth great things and unsearchable; marvellous things without number"</em> (<em>Job 5:9; 9:10</em>). Paul exclaims: <em>"O the depth of the riches both of the wisdom and knowledge of God! how unsearchable are his judgments, and his ways past finding out!"</em> (<em>Romans 11:33</em>); and again <em>"the unsearchable riches of Christ"</em> (<em>Ephesians 3:8</em>). Solomon: <em>"It is the glory of God to conceal a thing: but the honour of kings is to search out a matter"</em> (<em>Proverbs 25:2</em>). Unsearchable is what we <em>praise</em>; it is not what we lament. God’s greatness exceeds the saint’s measure precisely because He is God.</p>'
    ),
    'yes-and-amen': (
        '<p>"Yes and amen" is Paul’s phrase for the absolute reliability of every promise of God in Jesus Christ: <em>"For all the promises of God in him are yea, and in him Amen, unto the glory of God by us"</em> (<em>2 Corinthians 1:20</em>). The promises do not flicker between yes and no; they do not depend on the saint’s strength to hold them; they do not expire with the cultural mood. In Christ they are spoken <em>"yes"</em> by God Himself, and the church seals them <em>"amen"</em> back to His glory. Every promise of God is therefore a settled fact for the believer — fulfilled, being fulfilled, or about to be fulfilled — and the saint’s daily faith is the corporate <em>"amen"</em> spoken back across two thousand years.</p>'
    ),
    'yhwh-tsabaoth': (
        '<p><em>YHWH-Tsabaoth</em> (יְהוָה צְבָאוֹת) — "the LORD of hosts," "LORD of armies" — is the most frequent compound divine name in Scripture, appearing nearly three hundred times, especially in the prophets. The <em>hosts</em> are the angelic armies of heaven, the celestial bodies (sun, moon, stars), and the assembled people of God. YHWH commands all three: nothing is outside His command. <em>"The LORD of hosts is with us; the God of Jacob is our refuge"</em> (<em>Psalm 46:7, 11</em>); <em>"Who is this King of glory? The LORD of hosts, he is the King of glory"</em> (<em>Psalm 24:10</em>). David explicitly invoked the name against Goliath: <em>"I come to thee in the name of the LORD of hosts, the God of the armies of Israel, whom thou hast defied"</em> (<em>1 Samuel 17:45</em>).</p>'
    ),
    'beating-breast': (
        '<p>Beating the breast is the gesture of striking one’s own chest as a public sign of grief, unworthiness, or repentance. Luke uses it twice with weight. First, in the parable of the Pharisee and the publican: the publican, <em>"standing afar off, would not lift up so much as his eyes unto heaven, but smote upon his breast, saying, God be merciful to me a sinner. I tell you, this man went down to his house justified rather than the other"</em> (<em>Luke 18:13-14</em>). Second, after the crucifixion: <em>"all the people that came together to that sight, beholding the things which were done, smote their breasts, and returned"</em> (<em>Luke 23:48</em>). The body’s blow on the chest is the soul’s public Amen to its own guilt.</p>'
    ),
    'brawler': (
        '<p>A brawler is a contentious, quarrelsome person — one whose default posture is fight, whose first instinct in disagreement is escalation. Paul disqualifies brawlers from the eldership: <em>"Not given to wine, no striker, not greedy of filthy lucre; but patient, not a brawler, not covetous"</em> (<em>1 Timothy 3:3</em>); <em>"To speak evil of no man, to be no brawlers, but gentle, shewing all meekness unto all men"</em> (<em>Titus 3:2</em>). The disqualification is not because elders never confront — they must — but because the man whose first instinct is to swing should not stand in the pulpit. The pastor must be ready to <em>contend</em> for the faith (<em>Jude 3</em>) without becoming <em>contentious</em>. The difference is everything.</p>'
    ),
    'breach-of-covenant': (
        '<p>A breach of covenant is a party’s violation of his sworn obligation under the covenant’s terms. Israel’s history is, in large part, the history of covenant breach: idolatry (the golden calf, the Baals, the high places), Sabbath-breaking (<em>Nehemiah 13:15-22</em>), oppression of the poor (<em>Amos 2:6-8</em>), alliance with foreign gods, neglect of tithes. Each was breach; each invited the threatened curses of <em>Deuteronomy 28</em>. The LORD’s covenant-lawsuits in the prophets (<em>rib</em>) bring the formal indictment. Yet God’s mercy is also written into covenant: <em>"the LORD will not cast off his people, neither will he forsake his inheritance"</em> (<em>Psalm 94:14</em>). In Christ, the breach itself is healed, the curses borne, and the New Covenant secured.</p>'
    ),
    'carmel': (
        '<p>Mount Carmel is the wooded coastal mountain rising near modern Haifa — a long, fertile ridge running northwest into the Mediterranean. In Scripture it is the stage of one of the great showdowns of Hebrew religion: Elijah’s contest with the four hundred and fifty prophets of Baal in <em>1 Kings 18</em>. <em>"How long halt ye between two opinions? if the LORD be God, follow him: but if Baal, then follow him"</em> (<em>v. 21</em>). The two bulls were laid on rival altars; no fire was lit; the prophets of Baal cried all day in vain; Elijah rebuilt the LORD’s altar, drenched the sacrifice, and prayed. Fire fell. All the people fell on their faces: <em>"The LORD, he is the God."</em> Carmel is the mountain where Israel was forced to choose its God.</p>'
    ),
    'compassion-biblical': (
        '<p>Biblical compassion is the disposition that suffers with another’s suffering — not pity from a distance but visceral, embodied joining. The Greek verb <em>splanchnizomai</em> ("to be moved in the bowels") describes Christ repeatedly: <em>"But when he saw the multitudes, he was moved with compassion on them, because they fainted, and were scattered abroad, as sheep having no shepherd"</em> (<em>Matthew 9:36</em>; cf. <em>14:14; 15:32; 20:34; Mark 1:41; Luke 7:13</em>). The Father is the source of <em>"the multitude of his tender mercies"</em> (<em>Psalm 51:1; 119:156</em>). Christian compassion in Scripture is always followed by action — feeding, healing, teaching, lifting. Feeling that does not move the hand has not yet learned the word.</p>'
    ),
    'dystopia': (
        '<p>"Dystopia" — the modern literary term for a deliberately bad social order — has long been forecast by Scripture. The ultimate dystopia is the kingdom of Antichrist described in <em>Revelation 13</em>: controlling commerce by the mark (<em>v. 17</em>) and persecuting the faithful unto death (<em>v. 7</em>). Its archetype is older: Babel, where humanity, united in rebellion, built a tower to heaven to make a name for themselves and were scattered in confusion (<em>Genesis 11:1-9</em>). Every utopian project apart from God ends as dystopia, because man without God cannot govern man. The pattern is consistent: when sinful man seeks paradise without the Lord, he builds hell on earth. The new heavens and new earth come only by Christ’s return.</p>'
    ),
    'erastus': (
        '<p>Erastus was a Corinthian believer who held the office of city treasurer (Greek <em>oikonomos tēs poleōs</em>, sometimes translated <em>"chamberlain"</em>) and sent his greetings to the Roman church through Paul: <em>"Erastus the chamberlain of the city saluteth you"</em> (<em>Romans 16:23</em>). He appears later as a co-laborer traveling with Paul (<em>Acts 19:22</em>) and as one whom Paul left at Corinth during a later journey: <em>"Erastus abode at Corinth"</em> (<em>2 Timothy 4:20</em>). His name has been recovered archaeologically on a first-century Corinthian inscription crediting an Erastus <em>"who paved this pavement at his own expense in return for his aedileship."</em> The civic-officer Christian is a model — kingdom citizenship lived out faithfully in a Roman public office.</p>'
    ),
    'everlasting-covenant': (
        '<p>An "everlasting covenant" (Hebrew <em>berit olam</em>) is one whose duration is unending. Scripture names several. The Noahic Covenant: <em>"I will remember my covenant... an everlasting covenant between God and every living creature"</em> (<em>Genesis 9:16</em>). The Abrahamic: <em>"And I will establish my covenant between me and thee... for an everlasting covenant"</em> (<em>Genesis 17:7</em>). The Davidic: <em>"he hath made with me an everlasting covenant, ordered in all things, and sure"</em> (<em>2 Samuel 23:5</em>). The New Covenant in Christ: <em>"the blood of the everlasting covenant"</em> (<em>Hebrews 13:20</em>). The Mosaic covenant, by contrast, was provisional — pointing forward to the everlasting one. In Christ, the everlasting covenant has come.</p>'
    ),
    'fine-tuning': (
        '<p>The Fine-Tuning Argument is a modern form of the teleological (design) argument that observes how the fundamental physical constants of the universe — the gravitational constant, the strong nuclear force, the cosmological constant, the ratio of electromagnetic force to gravity, and dozens more — are precisely calibrated to permit life. Tiny variations in any one would render life impossible. The improbability of such fine-tuning by chance argues for intentional design. Modern proponents include physicist-theologians Robin Collins, philosopher William Lane Craig, and mathematician John Lennox. Scripture confirms the premise without the calculations: <em>"For the invisible things of him from the creation of the world are clearly seen, being understood by the things that are made"</em> (<em>Romans 1:20</em>).</p>'
    ),
    'foreknowledge': (
        '<p>In Scripture, God’s foreknowledge is not merely His knowing of events before they happen — though He does foresee all things. It is a relational, intimate, choosing knowledge. When Paul writes <em>"For whom he did foreknow, he also did predestinate to be conformed to the image of his Son"</em> (<em>Romans 8:29</em>), he does not mean God passively saw who would believe; he means God set His covenant love upon them beforehand. <em>"You only have I known of all the families of the earth"</em> (<em>Amos 3:2</em>) — God knew Israel relationally, not just informationally. Foreknowledge in this biblical sense is therefore inseparable from election: God’s prior choosing love, set on persons before the foundation of the world.</p>'
    ),
    'foreshadowing': (
        '<p>Foreshadowing is the Bible’s method of revealing coming realities — especially the person and work of Christ — through earlier types, prophecies, sacrifices, persons, and patterns. The Old Testament foreshadows; the New Testament fulfills; both are inspired by one God writing one story. <em>"For the law having a shadow of good things to come, and not the very image of the things"</em> (<em>Hebrews 10:1</em>); <em>"Which are a shadow of things to come; but the body is of Christ"</em> (<em>Colossians 2:17</em>). The shadow is real; the body that casts it is more real. To read the Old Testament without seeing Christ foreshadowed is to miss the burning point of every page. The whole Bible is one story, and its central character has always been Jesus.</p>'
    ),
    'genre-recognition': (
        '<p>Genre recognition is the hermeneutical discipline of identifying a biblical passage’s literary type <em>before</em> interpreting it. Scripture contains many genres: narrative (Genesis, Acts), poetry (Psalms), prophecy (Isaiah), parable (Luke 15), apocalyptic (Daniel 7, Revelation), epistle (Romans), wisdom (Proverbs), law (Leviticus), genealogy (1 Chronicles), gospel (Mark). Each genre has its own conventions, devices, and reading rules. Reading a parable as historical narrative or an apocalyptic vision as flat prediction will distort the text — as will reading poetry as prose, or law as gospel. Right reading begins with right genre identification. The literal sense of Scripture <em>includes</em> the figurative when the figurative is what the author intended.</p>'
    ),
    'glean': (
        '<p>To <em>glean</em> is to gather grain or fruit left behind by reapers after the main harvest. Under Mosaic law, the corners of the field and the dropped sheaves were not to be harvested by the owner — they were to be left for the poor, the widow, the orphan, and the stranger to glean: <em>"And when ye reap the harvest of your land, thou shalt not wholly reap the corners of thy field, neither shalt thou gather the gleanings of thy harvest. And thou shalt not glean thy vineyard"</em> (<em>Leviticus 19:9-10</em>; cf. <em>Deuteronomy 24:19-22</em>). The law’s mercy-shape is built into the harvest itself. Ruth the Moabitess gleans in Boaz’s field (<em>Ruth 2</em>) — and a Gentile widow becomes the great-grandmother of King David.</p>'
    ),
    'holiness-pursued': (
        '<p>Holiness, in Scripture, is the state of being set apart unto God and rendered whole — and it is <em>both</em> granted in Christ <em>and</em> pursued by the saint. <em>"But of him are ye in Christ Jesus, who of God is made unto us wisdom, and righteousness, and sanctification, and redemption"</em> (<em>1 Corinthians 1:30</em>) names the granted side. <em>"Follow peace with all men, and holiness, without which no man shall see the Lord"</em> (<em>Hebrews 12:14</em>) names the pursued side. It is positional and practical at once: declared in justification, worked out in sanctification. Christian men must hold both: never trade the imputed righteousness of Christ for moralism, never trade the call to actual obedience for cheap grace.</p>'
    ),
    'household-altar': (
        '<p>A household altar is the family’s appointed station for daily worship — the place where prayer is offered, Scripture read, hymns sung, and God remembered as the one true Lord of this house. The patriarchs built literal stone altars at every place they pitched their tents: Abraham at Shechem (<em>Genesis 12:7</em>), at Bethel (<em>12:8</em>), at Hebron (<em>13:18</em>); Isaac at Beer-sheba (<em>26:25</em>); Jacob at Shechem (<em>33:20</em>) and Bethel (<em>35:7</em>). The New Covenant household keeps the same fire by daily corporate worship under one roof: family prayer, Scripture reading, catechism, song. <em>"As for me and my house, we will serve the LORD"</em> (<em>Joshua 24:15</em>). Every Christian father is the priest of his household altar.</p>'
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
