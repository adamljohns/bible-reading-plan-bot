#!/usr/bin/env python3
"""Batch 20 — expand 25 more thin entries to 90-110 words each.

Targets: virtues, OT/NT books, offerings, geography, monarchy
events, foundational verbs, and ecclesial qualifications from the
30-50 word bucket. This batch brings the session total to 500.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'hope-living': (
        '<p>Living hope is the hope into which God begets His people through the resurrection of Jesus Christ. Peter opens his first epistle with the phrase: <em>"Blessed be the God and Father of our Lord Jesus Christ, which according to his abundant mercy hath begotten us again unto a lively hope by the resurrection of Jesus Christ from the dead"</em> (<em>1 Peter 1:3</em>). The hope is <em>living</em> because its object lives — Christ is risen and ascended, alive forevermore (<em>Revelation 1:18</em>). It is sure because its anchor is in heaven within the veil (<em>Hebrews 6:19</em>). It is undefiled because the inheritance is <em>"reserved in heaven for you, who are kept by the power of God"</em> (<em>1 Peter 1:4-5</em>). The Christian’s tomorrow is guarded.</p>'
    ),
    'humility-true': (
        '<p>True humility is the Spirit-wrought lowliness of mind that knows its own creatureliness and corruption, magnifies God’s grace, esteems others better than self, and gladly takes the lowest place. It is the very mind of Christ: <em>"Let this mind be in you, which was also in Christ Jesus: who, being in the form of God... made himself of no reputation, and took upon him the form of a servant... and became obedient unto death, even the death of the cross"</em> (<em>Philippians 2:5-8</em>). It is distinct from false humility (self-deprecation as virtue-signal) and from servility (cringing weakness). Christian men are not falsely small — they are rightly placed. <em>"God resisteth the proud, and giveth grace unto the humble"</em> (<em>James 4:6</em>).</p>'
    ),
    'lamplight': (
        '<p>Lamplight is the soft, oil-fed glow of the Israelite home after dark — the small, steady flame that filled a tent or a house and pushed back the night. Scripture uses lamplight to picture three things. First, the household’s witness: <em>"Neither do men light a candle, and put it under a bushel, but on a candlestick; and it giveth light unto all that are in the house"</em> (<em>Matthew 5:15</em>). Second, the Word that lights the path: <em>"Thy word is a lamp unto my feet, and a light unto my path"</em> (<em>Psalm 119:105</em>). Third, the bridegroom’s arrival in the night: the wise virgins kept oil in their lamps (<em>Matthew 25:1-13</em>). Trim your wick; keep oil; watch.</p>'
    ),
    'mockery': (
        '<p>Mockery is derisive imitation — ridicule designed to humiliate, not correct. Scripture knows it on both sides. Elijah’s mockery of the prophets of Baal at Carmel exposed Baal as nothing: <em>"Cry aloud: for he is a god; either he is talking, or he is pursuing, or he is in a journey, or peradventure he sleepeth, and must be awaked"</em> (<em>1 Kings 18:27</em>). But the mockery of Christ at Golgotha — the crown of thorns, the purple robe, the <em>"Hail, King of the Jews"</em> (<em>Matthew 27:29</em>) — exposed the mockers as condemned. The apostolic warning is plain: <em>"Be not deceived; God is not mocked: for whatsoever a man soweth, that shall he also reap"</em> (<em>Galatians 6:7</em>). Men frequently try.</p>'
    ),
    'petros-petra': (
        '<p><em>Petros</em> and <em>petra</em> are the Greek words at the heart of Christ’s wordplay in <em>Matthew 16:18</em>: <em>"That thou art Peter (Petros), and upon this rock (petra) I will build my church."</em> The two words are deliberately distinct: <em>petros</em> is masculine and means a stone or small rock; <em>petra</em> is feminine and means bedrock, a massive ledge. Reformed exegesis (against Rome’s papal-foundation reading) recognizes that Christ is distinguishing Peter the man from the <em>petra</em> on which the church is built — the bedrock of the confession just made: <em>"Thou art the Christ, the Son of the living God"</em> (<em>v. 16</em>). Christ Himself is the rock (<em>1 Corinthians 10:4</em>; <em>Ephesians 2:20</em>), and confessing faith in Him is the foundation.</p>'
    ),
    'qualifications-elder': (
        '<p>The qualifications of an elder are Paul’s twin lists in <em>1 Timothy 3:1-7</em> and <em>Titus 1:5-9</em> — character and competence requirements for the office of overseer. The elder must be <em>"blameless, the husband of one wife, vigilant, sober, of good behaviour, given to hospitality, apt to teach; not given to wine, no striker, not greedy of filthy lucre; but patient, not a brawler, not covetous; one that ruleth well his own house, having his children in subjection with all gravity."</em> He must not be a novice, lest he fall into the condemnation of the devil, and he must have a good report of them which are without. Two skills (teach, rule) are surrounded by a wall of character traits. The character wall stands first.</p>'
    ),
    'return-from-exile': (
        '<p>The Return from Exile was the return of Jewish exiles from Babylon under the decree of Cyrus the Persian in 538 BC, fulfilling Jeremiah’s prophecy of seventy years (<em>Jeremiah 25:11-12; 29:10</em>; <em>Ezra 1:1-4</em>; <em>2 Chronicles 36:22-23</em>). The return came in three identifiable waves: under Zerubbabel, who rebuilt the temple altar and laid the foundation (<em>Ezra 1-6</em>, completed 516 BC); under Ezra the priest-scribe, who restored the law and dealt with mixed marriages (<em>Ezra 7-10</em>, c. 458 BC); and under Nehemiah the Persian cupbearer, who rebuilt the walls of Jerusalem (<em>Nehemiah 1-13</em>, c. 445 BC). Temple, law, and walls were the three things rebuilt. The shape of biblical restoration always begins with worship.</p>'
    ),
    'salutation-pastoral': (
        '<p>The Pastoral Salutation is the minister’s pronouncement of grace and peace at the start of worship in the name of the triune God — a brief, scriptural greeting that declares to the gathered congregation God’s favor over the assembly. The form is modeled on Paul’s epistolary openings: <em>"Grace be unto you, and peace, from God our Father, and from the Lord Jesus Christ"</em> (<em>Romans 1:7</em>; nearly identical in every Pauline letter). The salutation is not a casual welcome; it is an authoritative word spoken by the minister as Christ’s servant, paralleling the opening Votum. It tells the congregation: God is here, God is for you, the service is His gift. Worship begins under that pronouncement of unmerited favor.</p>'
    ),
    'sisera': (
        '<p>Sisera was the Canaanite army-captain of Jabin king of Hazor — the great oppressor of Israel for twenty years (<em>Judges 4:2-3</em>). He commanded nine hundred chariots of iron and held the northern tribes in fear until Deborah summoned Barak from Kedesh-naphtali. The LORD <em>"discomfited Sisera, and all his chariots, and all his host"</em> by the brook Kishon (<em>Judges 4:15</em>); Sisera fled on foot to the tent of Jael the wife of Heber, who gave him milk, covered him with a mantle, and then, as he slept exhausted, drove a tent peg through his temple. Deborah’s song celebrates the deliverance and Jael’s deed: <em>"Blessed above women shall Jael... be"</em> (<em>Judges 5:24-27</em>). Tyrants fall by the hand the LORD appoints.</p>'
    ),
    'speak': (
        '<p>To <em>speak</em>, in Scripture, is to utter words — but the word is freighted with creative and authoritative weight. God speaks creation into being: <em>"And God said, Let there be light: and there was light"</em> (<em>Genesis 1:3</em>). The prophets speak forth His word: <em>"Thus saith the LORD"</em>. Christ is the Word made flesh, and <em>"never man spake like this man"</em> (<em>John 7:46</em>). The Spirit speaks through prophets and apostles (<em>2 Peter 1:21</em>). The verb carries word-as-deed: divine speech produces what it says. Christian speech, made in God’s image, also carries weight. <em>"Death and life are in the power of the tongue"</em> (<em>Proverbs 18:21</em>). Christians are commanded to speak the truth in love (<em>Ephesians 4:15</em>) and let no corrupt communication proceed.</p>'
    ),
    'asham-offering': (
        '<p>The <em>asham</em> (אָשָׁם) is the Mosaic trespass or guilt offering, prescribed in <em>Leviticus 5:14-19</em> and <em>6:1-7</em> for sins requiring restitution — usually involving sacred property (a man who unknowingly used a holy thing) or harm to a neighbor (deceit, theft, swearing falsely). The required sacrifice was a ram without blemish, accompanied by full restitution plus a fifth-part penalty paid to the wronged party. The offering taught what cheap forgiveness has forgotten: real sin requires real repair. The deepest application is Christological: <em>"when thou shalt make his soul an offering for sin (asham), he shall see his seed"</em> (<em>Isaiah 53:10</em>). The Suffering Servant Himself is the great <em>asham</em> — Christ’s soul presented as the guilt offering that pays restitution for sin.</p>'
    ),
    'caesarea': (
        '<p>Caesarea was the great coastal city of Roman Judea — built by Herod the Great around 22-10 BC on the Mediterranean shore and named for Caesar Augustus. It became the Roman administrative capital of the province, seat of the procurators (Pilate, Felix, Festus). Scripture places three pivotal events there. First, the conversion of Cornelius the Roman centurion and the opening of the gospel to the Gentiles (<em>Acts 10</em>) — Peter’s visit that broke the wall. Second, Paul’s two-year imprisonment under Felix and Festus, with the dramatic defenses before them and before Agrippa (<em>Acts 23-26</em>). Third, the place from which Paul finally sailed in chains to Rome (<em>Acts 27:1-2</em>). The gospel’s reach to the empire ran through this city.</p>'
    ),
    'chattat-offering': (
        '<p>The <em>chattat</em> (חַטָּאת) is the Mosaic sin offering, prescribed in <em>Leviticus 4</em> for unintentional sins committed by the priest, the congregation, the ruler, or the common person. The remarkable Hebrew detail is that the same word <em>chattat</em> names both <em>"sin"</em> and <em>"sin offering"</em> — the sin and the sacrifice that addressed it share the very same name. The blood was applied to the horns of the bronze altar (for the people) or to the horns of the golden altar within the veil (for the priest or congregation). Christ fulfills both meanings: <em>"For he hath made him to be sin (chattat / hamartia) for us, who knew no sin"</em> (<em>2 Corinthians 5:21</em>). He is both the sin-bearer and the sin-offering.</p>'
    ),
    'dan-tribe': (
        '<p>Dan was the fifth son of Jacob — born to Bilhah, Rachel’s maid — and the tribe descended from him (<em>Genesis 30:6</em>). Originally allotted territory in the southern coastal plain near Joppa (<em>Joshua 19:40-48</em>), the tribe failed to take possession against the Amorites (<em>Judges 1:34</em>) and later migrated north, conquered the city of Laish, and renamed it Dan (<em>Judges 18</em>). It thus became the northernmost limit of Israel — the proverbial expression <em>"from Dan to Beersheba"</em> (<em>Judges 20:1</em>; <em>1 Samuel 3:20</em>) names the whole land. Dan also became a center of idolatry under Jeroboam, who set one of his golden calves there (<em>1 Kings 12:29</em>). The tribe is conspicuously absent from <em>Revelation 7</em>.</p>'
    ),
    'divided-kingdom': (
        '<p>The Divided Kingdom is the split of Solomon’s kingdom under his son Rehoboam (c. 931 BC), when the ten northern tribes followed Jeroboam to form Israel and only Judah and Benjamin remained loyal to the house of David. The break was triggered by Rehoboam’s refusal to lighten Solomon’s tax burden (<em>1 Kings 12</em>); the LORD allowed it as judgment for Solomon’s late idolatry (<em>1 Kings 11:11-13</em>). The northern kingdom — Israel — devolved through nineteen kings of nine dynasties, all wicked, falling to Assyria in 722 BC (<em>2 Kings 17</em>). The southern kingdom — Judah — endured longer through twenty kings of one Davidic line, with periodic revivals, falling to Babylon in 586 BC. The division endured until both went into exile.</p>'
    ),
    'dust': (
        '<p>Dust is the fine earth from which man was formed and to which his body returns — Scripture’s emblem of human frailty, mortality, and absolute dependence on the Creator. <em>"And the LORD God formed man of the dust of the ground"</em> (<em>Genesis 2:7</em>); <em>"for dust thou art, and unto dust shalt thou return"</em> (<em>3:19</em>). The Psalmist remembers it: <em>"For he knoweth our frame; he remembereth that we are dust"</em> (<em>Psalm 103:14</em>). To sit in dust is the biblical posture of repentance and grief: Job repented <em>"in dust and ashes"</em> (<em>Job 42:6</em>); Abraham acknowledged he was <em>"but dust and ashes"</em> (<em>Genesis 18:27</em>). The Christian who remembers his dustiness will not strut. Resurrection is the only answer.</p>'
    ),
    'esther-book': (
        '<p>Esther is the only book in Scripture that does not name God once — yet His sovereign providence is visible on every page. Set in the Persian court of King Xerxes (Ahasuerus, c. 486-465 BC), it tells how a Jewish orphan named Hadassah (Esther) becomes queen of Persia and rises <em>"to the kingdom for such a time as this"</em> (<em>Esther 4:14</em>). Through her cousin Mordecai and Persian providence, she exposes the plot of Haman to exterminate the Jews. The villain is hanged on his own gallows; the Jews are delivered; and the annual feast of Purim is instituted (<em>Esther 9:20-32</em>). The book teaches that God’s hand is sometimes most unmistakable precisely when it is most hidden. Providence works in silence.</p>'
    ),
    'fall-jericho': (
        '<p>The Fall of Jericho was the first conquest of the promised land (<em>Joshua 6</em>) — and one of the strangest victories in Scripture. The walled Canaanite stronghold guarded the Jordan crossing; humanly, it should have required a long siege. Instead, the LORD commanded Joshua to march the armed men and seven priests blowing rams’ horns silently around the city once a day for six days. On the seventh day they were to march around seven times, sound a long blast, and the people were to shout. <em>"The wall fell down flat, so that the people went up into the city, every man straight before him"</em> (<em>Joshua 6:20</em>). <em>"By faith the walls of Jericho fell down, after they were compassed about seven days"</em> (<em>Hebrews 11:30</em>). Faith conquers, not siegecraft.</p>'
    ),
    'give': (
        '<p>To <em>give</em> is to bestow, grant, hand over — and Scripture identifies the supreme giver as God Himself. <em>"For God so loved the world, that he gave his only begotten Son"</em> (<em>John 3:16</em>). The Son in turn <em>"gave himself for me"</em> (<em>Galatians 2:20</em>); the Spirit gives spiritual gifts <em>"to every man severally as he will"</em> (<em>1 Corinthians 12:11</em>). Christian giving is therefore response, not initiative — the receiver passing on what he has been given. Christ commands: <em>"freely ye have received, freely give"</em> (<em>Matthew 10:8</em>); <em>"give, and it shall be given unto you"</em> (<em>Luke 6:38</em>). The grace of giving is one of the surest marks of a regenerate soul. Generous men reflect a generous God.</p>'
    ),
    'heart-flesh': (
        '<p>The "heart of flesh" is the new heart God promises in the new covenant — not a renovated heart of stone but a wholly new creation. <em>"A new heart also will I give you, and a new spirit will I put within you: and I will take away the stony heart out of your flesh, and I will give you an heart of flesh. And I will put my spirit within you, and cause you to walk in my statutes"</em> (<em>Ezekiel 36:26-27</em>). The heart of flesh is soft, living, sensitive to God’s voice, and Spirit-empowered to obey His statutes. It is the inward credential of every true believer — the regenerate heart, given freely by sovereign grace, with no contribution from the recipient. Every Christian carries one.</p>'
    ),
    'israel': (
        '<p>Israel is the covenant name given to Jacob after his all-night wrestling with the LORD at Peniel: <em>"Thy name shall be called no more Jacob, but Israel: for as a prince hast thou power with God and with men, and hast prevailed"</em> (<em>Genesis 32:28</em>). The name passed to the nation descended from his twelve sons — the people through whom God brought His law, His prophets, His worship, and ultimately His Messiah. In the New Testament, <em>"Israel"</em> is extended through faith in Christ to include believing Gentiles grafted into the olive tree (<em>Romans 11:17-24</em>) — <em>"the Israel of God"</em> (<em>Galatians 6:16</em>). National Israel still has a future (<em>Romans 11:25-29</em>), and the church does not replace her — she is included with her.</p>'
    ),
    'job-book': (
        '<p>Job is probably the oldest book in the Bible — set in the patriarchal age, possibly composed by Moses — and the Bible’s great wrestling-text with the suffering of the righteous and the sovereignty of God. A blameless, upright man <em>"that feared God, and eschewed evil"</em> (<em>Job 1:1</em>) loses his children, his wealth, and his health in a single day at Satan’s accusation and God’s permission. Three friends arrive to defend a flat retribution-theology that does not fit the case. After thirty-seven chapters of debate, the LORD answers Job not with explanations but with Himself, out of the whirlwind, asking unanswerable questions about creation (chs. 38-41). Job repents in dust and ashes, his integrity is vindicated, and his end is greater than his beginning.</p>'
    ),
    'obey': (
        '<p>To <em>obey</em> is to <em>listen under</em> — to submit to authority. The Greek <em>hupakouō</em> literally means "to hear-under," and the Hebrew <em>shamaʿ</em> ("hear") carries the same weight: real hearing produces real doing. Scripture establishes a hierarchy. The saint obeys God absolutely (<em>"We ought to obey God rather than men"</em>, <em>Acts 5:29</em>). He obeys authorities placed over him by God within their God-given sphere (<em>Romans 13:1-7</em>; <em>Ephesians 6:1, 5</em>; <em>1 Peter 2:13-14</em>). And he obeys the truth itself (<em>"Seeing ye have purified your souls in obeying the truth"</em>, <em>1 Peter 1:22</em>). Disobedience is rebellion against the rightful order of things. The Christian man learns to hear God first and obey straight from the ear.</p>'
    ),
    'pray': (
        '<p>To <em>pray</em> is to address God — in worship, petition, thanksgiving, confession, or intercession. Prayer is the standing posture of the saint: <em>"Pray without ceasing"</em> (<em>1 Thessalonians 5:17</em>); <em>"Continue in prayer, and watch in the same with thanksgiving"</em> (<em>Colossians 4:2</em>). It is more than asking — it is communion with the living God through Christ in the Spirit. The Trinitarian shape is striking: the Spirit Himself prays in us when we do not know how (<em>Romans 8:26-27</em>); Christ at the Father’s right hand ever lives to intercede for us (<em>Hebrews 7:25</em>; <em>Romans 8:34</em>); the Father hears us for the Son’s sake (<em>John 14:13-14</em>). Christian prayer is therefore never solitary; the whole Godhead is engaged.</p>'
    ),
    'samuel-prophet': (
        '<p>Samuel was the son of Hannah’s prayer-promise — born after long barrenness, given back to the LORD, and raised in the tabernacle at Shiloh under Eli the priest (<em>1 Samuel 1-3</em>). The LORD called him as a child, and he became the final judge of Israel and the first major writing prophet, anointing both Saul and David as king. <em>"And the LORD was with him, and did let none of his words fall to the ground. And all Israel from Dan even to Beersheba knew that Samuel was established to be a prophet of the LORD"</em> (<em>1 Samuel 3:19-20</em>). Samuel is the transition figure from the judges and theocracy to the monarchy — and his Mizpah revival (<em>1 Samuel 7</em>) is the model of national repentance.</p>'
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
