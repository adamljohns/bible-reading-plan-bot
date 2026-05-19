#!/usr/bin/env python3
"""Batch 52 — expand 25 more entries from the 60-70 word bucket.

Brings the sprint total to 1,300 entries.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'sowing': (
        '<p>Sowing is the casting of seed onto plowed ground in expectation of a future harvest — and in Scripture, the moral and spiritual counterpart of reaping. <em>"He that goeth forth and weepeth, bearing precious seed, shall doubtless come again with rejoicing, bringing his sheaves with him"</em> (<em>Psalm 126:6</em>). Paul: <em>"Be not deceived; God is not mocked: for whatsoever a man soweth, that shall he also reap. For he that soweth to his flesh shall of the flesh reap corruption; but he that soweth to the Spirit shall of the Spirit reap life everlasting"</em> (<em>Galatians 6:7-8</em>). Sowing is therefore a moral category. Every day’s choices are seeds. The Christian sows to the Spirit — Word, prayer, obedience, generosity — and reaps eternally.</p>'
    ),
    'swearing-oaths': (
        '<p>Swearing of oaths is the calling of God or a sacred thing as witness to one’s speech. Jesus commanded: <em>"But I say unto you, Swear not at all; neither by heaven; for it is God’s throne... But let your communication be, Yea, yea; Nay, nay: for whatsoever is more than these cometh of evil"</em> (<em>Matthew 5:34-37; James 5:12</em>). The teaching does not abolish all judicial oaths (Paul swears under God in his epistles, <em>Romans 1:9; 2 Corinthians 1:23; Galatians 1:20</em>; God Himself swore by Himself to Abraham, <em>Hebrews 6:13-18</em>); it forbids the casual, self-promoting, or evasive use of oaths in ordinary speech. The Christian man’s plain word should be reliable enough that no oath is needed for it.</p>'
    ),
    'tertullian': (
        '<p>Tertullian (c. 160-225) was the Carthaginian lawyer-turned-Christian-apologist whose Latin theological writing shaped the Western church’s vocabulary for centuries. He coined or popularized <em>Trinitas</em> ("Trinity"), <em>persona</em> ("person" of the Trinity), <em>substantia</em> ("substance"), <em>sacramentum</em> ("sacrament"), and many other foundational Latin terms. Major works: <em>Apology</em> (defense of Christianity to Roman authorities), <em>Against Marcion</em>, <em>Against Praxeas</em> (against modalism, articulating Trinity), <em>On the Flesh of Christ</em>, <em>On Baptism</em>. Famous lines: <em>"the blood of the martyrs is the seed of the church"</em>; <em>"What hath Athens to do with Jerusalem?"</em> He drifted into Montanism late in life, but his theological legacy persisted in the great church he had served.</p>'
    ),
    'the-man': (
        '<p>"The Man" — counterculture phrase popularized in the 1960s and surviving in slang ever since — names any authority figure or institution as inherently adversarial: government, corporation, police, employer, school administration. <em>"Stick it to the Man,"</em> <em>"don’t let the Man get you down."</em> The slang treats authority as inherently suspect, the enemy of authenticity and freedom. Scripture refuses the framing. Authority is ordained by God: <em>"For there is no power but of God: the powers that be are ordained of God"</em> (<em>Romans 13:1</em>); <em>"Submit yourselves to every ordinance of man for the Lord’s sake"</em> (<em>1 Peter 2:13</em>). The Christian honors rightful authority — not because every authority is good, but because the office is ordained.</p>'
    ),
    'thousand-year-reign': (
        '<p>The Thousand-Year Reign is the period described in <em>Revelation 20:2-7</em> in which Satan is bound in the abyss, the martyrs are raised in <em>"the first resurrection"</em>, and the saints reign with Christ a thousand years. The number is variously interpreted across the three major millennial views. <em>Premillennialism</em> holds Christ returns bodily before the millennium to inaugurate a literal future thousand-year reign on earth. <em>Postmillennialism</em> holds Christ returns bodily after a long age of gospel triumph. <em>Amillennialism</em> (the historic Reformed majority view) holds the thousand years symbolize the present church age between Christ’s first and second advents — Satan currently bound from deceiving the nations as he once did. All three confess Christ returns to judge and consummate.</p>'
    ),
    'token-of-covenant': (
        '<p>A token of covenant is the visible sign attached to a covenant as its public mark — appointed by God Himself to remind both parties of the bond. Each major Old Testament covenant has its token. The Noahic covenant: the rainbow (<em>"I do set my bow in the cloud, and it shall be for a token of a covenant between me and the earth"</em>, <em>Genesis 9:12-13</em>). The Abrahamic: circumcision (<em>"This is my covenant... ye shall circumcise the flesh of your foreskin; and it shall be a token of the covenant"</em>, <em>Genesis 17:10-11</em>). The Mosaic: the Sabbath (<em>"It is a sign between me and the children of Israel for ever"</em>, <em>Exodus 31:17</em>). And the New Covenant: baptism and the Lord’s Supper.</p>'
    ),
    'tongue-life-death': (
        '<p>"Death and life are in the power of the tongue" is <em>Proverbs 18:21</em>’s diagnostic: <em>"Death and life are in the power of the tongue: and they that love it shall eat the fruit thereof."</em> The most concentrated biblical statement of speech-power. Words can give life or take it. The encouraging father builds the child’s soul; the demeaning father wounds it for life. The pastor’s sermon either feeds the flock or starves them. The husband’s tone with his wife either kindles love or freezes it. The friend’s honest counsel either rescues the brother or accelerates his fall. <em>"A word fitly spoken is like apples of gold in pictures of silver"</em> (<em>Proverbs 25:11</em>). Speak life.</p>'
    ),
    'treasure-field': (
        '<p>The Treasure Hidden in the Field is Christ’s parable in <em>Matthew 13:44</em>: <em>"Again, the kingdom of heaven is like unto treasure hid in a field; the which when a man hath found, he hideth, and for joy thereof goeth and selleth all that he hath, and buyeth that field."</em> The man does not haggle over price; the treasure’s worth so exceeds the cost of the field that selling everything else is obvious, joyful, immediate. The kingdom of heaven is worth more than everything the man owns added together. The parallel parable of the Pearl of Great Price (<em>vv. 45-46</em>) makes the same point. The Christian who has not yet sold all does not yet understand the worth.</p>'
    ),
    'trophimus': (
        '<p>Trophimus was a Gentile believer from Ephesus who accompanied Paul on his return journey to Jerusalem at the close of the third missionary journey (<em>Acts 20:4</em>), carrying part of the Gentile relief offering. His presence in the temple courts (or rather, the Jerusalem Jews’ assumption that Paul had brought him there past the Court of the Gentiles) sparked the riot that led to Paul’s arrest: <em>"For they had seen before with him in the city Trophimus an Ephesian, whom they supposed that Paul had brought into the temple"</em> (<em>Acts 21:29</em>). Paul mentions him again in his last letter — left sick at Miletum (<em>2 Timothy 4:20</em>). Even Paul could not always heal every illness; even apostolic ministry left wounded behind.</p>'
    ),
    'turn-cheek': (
        '<p>"Turn the other cheek" is Christ’s teaching in the Sermon on the Mount (<em>Matthew 5:38-42</em>): <em>"Ye have heard that it hath been said, An eye for an eye, and a tooth for a tooth: But I say unto you, That ye resist not evil: but whosoever shall smite thee on thy right cheek, turn to him the other also."</em> The teaching overturns the Mosaic <em>lex talionis</em> as a principle of personal vengeance. It does not abolish judicial justice (the state still bears the sword, <em>Romans 13:4</em>) or self-defense in extremity; it forbids personal retaliation. The right-cheek slap was a backhanded insult; the offered left cheek refuses the cycle. Christian men do not return insult for insult.</p>'
    ),
    'vinegar': (
        '<p>Vinegar — soured wine — was the cheap drink of Roman soldiers and laborers. In Scripture it is offered to Christ twice on the cross. First, mingled with gall before the crucifixion to dull pain — He tasted it and refused: <em>"They gave him vinegar to drink mingled with gall: and when he had tasted thereof, he would not drink"</em> (<em>Matthew 27:34</em>). Second, after His cry <em>"I thirst"</em>, a sponge soaked in vinegar was lifted to His lips on a reed or hyssop branch — He received this one, in fulfillment of <em>Psalm 69:21</em>: <em>"They gave me also gall for my meat; and in my thirst they gave me vinegar to drink."</em> <em>"When Jesus therefore had received the vinegar, he said, It is finished"</em> (<em>John 19:30</em>). Then He bowed His head.</p>'
    ),
    'water-wine': (
        '<p>The turning of water into wine is Christ’s first sign in John’s Gospel (<em>John 2:1-11</em>) — performed at the wedding at Cana of Galilee. Six stone water-pots, each holding twenty to thirty gallons (a total of 120 to 180 gallons), were filled to the brim at His command and became fine wine. The master of the feast was astonished: <em>"Every man at the beginning doth set forth good wine; and when men have well drunk, then that which is worse: but thou hast kept the good wine until now"</em> (<em>v. 10</em>). John concludes: <em>"This beginning of miracles did Jesus in Cana of Galilee, and manifested forth his glory; and his disciples believed on him"</em> (<em>v. 11</em>). The Bridegroom inaugurates His ministry at a wedding by providing the wine.</p>'
    ),
    'zerubbabel': (
        '<p>Zerubbabel was the post-exilic governor of Judah who led the first return of Jewish exiles from Babylon in 538 BC under the Persian decree of Cyrus, and who laid the foundation of the Second Temple. Born in exile (his name means <em>"seed of Babylon"</em>), he was of David’s royal line — the grandson of King Jehoiachin — and stands as a critical hinge of redemptive history: <em>"In that day, saith the LORD of hosts, will I take thee, O Zerubbabel, my servant, the son of Shealtiel, saith the LORD, and will make thee as a signet: for I have chosen thee"</em> (<em>Haggai 2:23</em>). The Davidic line survived the exile. Zerubbabel’s name appears in Christ’s genealogy in <em>Matthew 1:12-13</em>. The Branch grew from this preserved stump.</p>'
    ),
    'agabus': (
        '<p>Agabus was a New Testament prophet active in the AD 40s and 50s. <em>Acts 11:28</em> records his first foretelling: <em>"And there stood up one of them named Agabus, and signified by the Spirit that there should be great dearth throughout all the world: which came to pass in the days of Claudius Caesar"</em> — prompting the Antioch church to send relief to the Judean brethren through Barnabas and Saul. His second appearance is dramatic. At Caesarea on Paul’s return journey to Jerusalem, Agabus took Paul’s belt, bound his own hands and feet with it, and prophesied: <em>"So shall the Jews at Jerusalem bind the man that owneth this girdle, and shall deliver him into the hands of the Gentiles"</em> (<em>Acts 21:11</em>). Paul went anyway, knowing the cost.</p>'
    ),
    'amidah': (
        '<p>The Amidah (Hebrew "standing") is the central prayer of Jewish daily liturgy — eighteen (originally) or nineteen blessings prayed standing, three times daily (morning, afternoon, evening), still practiced in synagogue Judaism. It includes praise of God (the first three blessings), petitions for daily needs and national restoration (the middle thirteen), and thanksgiving (the last three). Christ’s rebuke of the Pharisees who <em>"love to pray standing in the synagogues and in the corners of the streets, that they may be seen of men"</em> (<em>Matthew 6:5</em>) probably refers to ostentatious public Amidah-praying — not the prayer itself but its weaponized display. He gave His disciples a shorter, simpler model: the Lord’s Prayer (<em>Matthew 6:9-13</em>).</p>'
    ),
    'attributes-of-god': (
        '<p>The Attributes of God are the qualities or perfections of God’s very being — eternal, infinite, unchanging, omnipresent, omniscient, omnipotent, holy, just, merciful, loving, faithful, sovereign, simple. Classical Christian theology distinguishes <em>incommunicable</em> attributes (those true only of God: aseity, infinity, immutability, eternity, immensity) from <em>communicable</em> attributes (those analogically true of His image-bearers: holiness, justice, love, mercy, wisdom, goodness). Westminster Shorter Catechism Q4: <em>"God is a Spirit, infinite, eternal, and unchangeable, in his being, wisdom, power, holiness, justice, goodness, and truth."</em> The attributes are not parts of God; they are the one simple God known under different aspects. Every doctrine of Christianity downstream from these.</p>'
    ),
    'bathsheba': (
        '<p>Bathsheba was the wife of Uriah the Hittite — one of David’s mighty men (<em>2 Samuel 23:39</em>) — taken by David in adultery while Uriah was at war (<em>2 Samuel 11</em>). David then arranged Uriah’s death at the front line and married her. The first child died as part of the LORD’s judgment on the sin after Nathan’s confrontation (<em>2 Samuel 12</em>). Bathsheba later bore David four more sons including Solomon, the heir to the throne, and became a powerful queen-mother in Solomon’s accession (<em>1 Kings 1-2</em>). Christ’s genealogy in <em>Matthew 1:6</em> names her obliquely as <em>"her that had been the wife of Urias"</em> — a deliberate verbal memorial of the sin grace did not erase from the record.</p>'
    ),
    'blessing-children': (
        '<p>"Blessing the children" is the deliberate spoken benediction of children — modeled by the patriarchs (Jacob blessing Joseph’s sons Manasseh and Ephraim with crossed hands, <em>Genesis 48:14-20</em>), required of fathers (the Aaronic-style benedictions extended over the household), and demonstrated by Christ Himself: <em>"And they brought young children to him, that he should touch them... And he took them up in his arms, put his hands upon them, and blessed them"</em> (<em>Mark 10:13-16</em>). Christian fathers should consciously bless their children — at table, at bedtime, at every significant transition. The Aaronic benediction is the standard text: <em>"The LORD bless thee, and keep thee... and give thee peace"</em> (<em>Numbers 6:24-26</em>). Spoken blessing carries weight.</p>'
    ),
    'city-on-hill': (
        '<p>"A city set on a hill" is Christ’s image in <em>Matthew 5:14</em>: <em>"Ye are the light of the world. A city that is set on an hill cannot be hid."</em> Two truths in one sentence. The disciples ARE the world’s light — not <em>will</em> be, not <em>should</em> become, but are. And a city on a hill is unhideable — the light from its houses, walls, and torches travels miles across the dark countryside. The combination is consequential: visibility is not the disciple’s decision but his condition. <em>"Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven"</em> (<em>5:16</em>). The American Puritan vision of "city on a hill" (John Winthrop) springs from this verse.</p>'
    ),
    'deluge': (
        '<p>The deluge is the worldwide flood of <em>Genesis 6-9</em> by which God judged the violent and corrupt antediluvian world for its <em>"wickedness of man... great in the earth, and... every imagination of the thoughts of his heart was only evil continually"</em> (<em>6:5</em>). He spared only Noah, his three sons, their wives (eight souls in all), and the animals on the ark. The flood lasted forty days of rain plus the bursting up of <em>"the fountains of the great deep"</em>, with the ark afloat for over a year before Noah disembarked on the mountains of Ararat. The rainbow became the covenant sign that God would never again destroy the world with water (<em>9:13-15</em>). Peter calls the deluge a type of judgment to come — by fire (<em>2 Peter 3:5-7</em>).</p>'
    ),
    'demure': (
        '<p>"Demure" is originally an English adjective for modesty, reserve, and quietness — virtues Scripture commends in <em>1 Timothy 2:9</em> (<em>"that women adorn themselves in modest apparel, with shamefacedness and sobriety"</em>) and <em>1 Peter 3:3-4</em> (<em>"Whose adorning let it not be that outward adorning of plaiting the hair... but let it be the hidden man of the heart, in that which is not corruptible, even the ornament of a meek and quiet spirit, which is in the sight of God of great price"</em>). The 2024 Gen-Z viral usage (<em>"very demure, very mindful"</em>) is largely ironic — it performs demureness as aesthetic rather than embodying it as character. Christian women should aspire to the substance the slang only borrows.</p>'
    ),
    'despair': (
        '<p>Despair is the opposite of biblical hope — to declare, in word or in disposition, that God cannot or will not act. Scripture acknowledges its reality. Paul describes extreme pressure at Ephesus: <em>"For we would not, brethren, have you ignorant of our trouble which came to us in Asia, that we were pressed out of measure, above strength, insomuch that we despaired even of life"</em> (<em>2 Corinthians 1:8</em>). Yet he found the purpose: <em>"that we should not trust in ourselves, but in God which raiseth the dead"</em> (<em>v. 9</em>). Despair drives the saint deeper into dependence. The cure is not pep-talk but the resurrected Christ. <em>"Why art thou cast down, O my soul?... hope thou in God"</em> (<em>Psalm 42:5, 11; 43:5</em>).</p>'
    ),
    'el-olam': (
        '<p><em>El Olam</em> (אֵל עוֹלָם) — "the Everlasting God" — is the divine name invoked by Abraham at Beersheba after his covenant with Abimelech: <em>"And Abraham planted a grove in Beersheba, and called there on the name of the LORD, the everlasting God"</em> (<em>Genesis 21:33</em>). The Hebrew <em>olam</em> denotes long duration receding beyond view in both directions — the unbounded ages, before and after. Isaiah celebrates the same name: <em>"Hast thou not known? hast thou not heard, that the everlasting God, the LORD, the Creator of the ends of the earth, fainteth not, neither is weary?"</em> (<em>Isaiah 40:28</em>). Christian men praying to <em>El Olam</em> address the God who is beneath every age, before every beginning, beyond every end.</p>'
    ),
    'el-shaddai': (
        '<p><em>El Shaddai</em> (אֵל שַׁדַּי) — "God Almighty" — is the divine name by which God revealed Himself to the patriarchs in their pilgrim-promise years. Most famously to Abram at age ninety-nine when the Abrahamic covenant was reaffirmed: <em>"I am the Almighty God; walk before me, and be thou perfect"</em> (<em>Genesis 17:1</em>). Also to Isaac and Jacob (<em>28:3; 35:11; 48:3</em>). The name emphasizes God’s all-sufficient power to keep covenant promises that human strength cannot fulfill — Sarah’s barren womb, Isaac’s late-life travel, Jacob’s long wandering. Strikingly, <em>Exodus 6:3</em> records the LORD telling Moses: <em>"I appeared unto Abraham, unto Isaac, and unto Jacob, by the name of God Almighty, but by my name JEHOVAH was I not known to them."</em></p>'
    ),
    'environmentalism': (
        '<p>God gave humanity dominion over creation as <em>stewards</em>: <em>"Be fruitful, and multiply, and replenish the earth, and subdue it: and have dominion"</em> (<em>Genesis 1:28</em>); Adam was placed in the garden <em>"to dress it and to keep it"</em> (<em>Genesis 2:15</em>). The earth and its fullness belong to the LORD (<em>Psalm 24:1</em>; <em>50:10-12</em>). Christian stewardship is therefore a real biblical category — wise care for soil, water, animals, and beauty. However, <em>Romans 1:25</em> warns against those who <em>"worshipped and served the creature more than the Creator"</em>. Modern environmentalism often crosses that line — divinizing "Mother Earth," treating humanity as a parasite, and silencing the dominion mandate. Christians steward; we do not worship.</p>'
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
