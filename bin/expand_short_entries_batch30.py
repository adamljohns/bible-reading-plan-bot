#!/usr/bin/env python3
"""Batch 30 — expand 25 more thin entries to 90-110 words each.

Targets: OT figures, NT historical, Hebrew vocab, slang reframes,
ecclesial concepts, KJV vocabulary, and biblical imagery from the
30-50 word bucket. Brings the session total to 750.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'solomons-temple': (
        '<p>Solomon’s Temple was the first permanent house of YHWH, built on Mount Moriah in Jerusalem (the very site of Abraham’s near-sacrifice of Isaac, <em>2 Chronicles 3:1</em>) — completed c. 957 BC after seven years of construction (<em>1 Kings 6:38</em>). It housed the ark of the covenant in the Most Holy Place, and was the place where God set His Name (<em>1 Kings 9:3</em>). Cedar from Lebanon, gold overlay, twin cherubim with outstretched wings, the two great bronze pillars Jachin and Boaz, the sea of cast bronze — the structure preached the holiness, wealth, and order of the LORD. It stood until Babylon’s destruction in 586 BC. The temple prefigured Christ Himself: <em>"Destroy this temple, and in three days I will raise it up"</em> (<em>John 2:19</em>).</p>'
    ),
    'still-small-voice': (
        '<p>The "still small voice" is the surprising mode of YHWH’s revelation to despondent Elijah on Mount Horeb in <em>1 Kings 19:11-13</em>. Elijah had collapsed under Jezebel’s death-threat, fled to Sinai, and complained that he alone was left. The LORD passed by — but not in the strong wind that broke the rocks, not in the earthquake, not in the fire. After these, came <em>"a still small voice"</em> — literally <em>qol demamah daqqah</em>, "the sound of a thin silence." Elijah wrapped his face in his mantle and went out. YHWH’s preferred mode of speaking to His exhausted prophet was not the spectacular but the quiet, attentive presence — and the renewed commission that followed.</p>'
    ),
    'tabernacle-meeting': (
        '<p>The Tabernacle of Meeting (Hebrew <em>ohel moed</em>, often translated "tent of meeting" or "tabernacle of the congregation" in the KJV) is the wilderness sanctuary considered specifically as the <em>appointed place of meeting</em> between YHWH and His people. The term emphasizes the encounter that happens there, in distinction from <em>mishkan</em> ("dwelling"), which emphasizes God’s residence in it. <em>"And there I will meet with thee, and I will commune with thee from above the mercy seat"</em> (<em>Exodus 25:22</em>); <em>"And the LORD spake unto Moses face to face, as a man speaketh unto his friend"</em> (<em>Exodus 33:11</em>). The whole biblical pattern of corporate worship descends from <em>ohel moed</em>: the LORD gives His people a place to meet Him.</p>'
    ),
    'vashti': (
        '<p>Vashti was the Persian queen and wife of King Ahasuerus (Xerxes I, reigned 486-465 BC) at the start of the book of Esther. At the close of a 180-day banquet of nobles, Ahasuerus — <em>"merry with wine"</em> (<em>Esther 1:10</em>) — summoned Vashti to display her beauty before his court. She refused. The deposition that followed (<em>Esther 1:11-22</em>) and the subsequent empire-wide search for a new queen led to Esther’s elevation, and through her to the deliverance of the Jews from Haman’s genocide. Vashti is debated in modern feminist readings as proto-resistance; the biblical text passes no overt judgment. The narrative simply records that her refusal was the providential opening for Esther’s reign.</p>'
    ),
    'vesture': (
        '<p>Vesture is clothing — especially the outer garment, the public-facing layer of a person. Scripture loads the word with three theological uses. First, the seamless robe at the cross: <em>"They parted my raiment among them, and for my vesture they did cast lots"</em> (<em>Psalm 22:18</em>; fulfilled <em>John 19:23-24</em>). Second, the vesture dipped in blood at Christ’s return: <em>"And he was clothed with a vesture dipped in blood: and his name is called The Word of God"</em> (<em>Revelation 19:13</em>). Third, the changed vesture of the saved soul: <em>"as a vesture shalt thou change them, and they shall be changed"</em> (<em>Hebrews 1:12</em>; <em>Psalm 102:26</em>). The Christian has put on Christ as his vesture (<em>Galatians 3:27</em>).</p>'
    ),
    'ahab': (
        '<p>Ahab was the seventh king of the northern kingdom of Israel (873-852 BC), son of Omri the dynasty-founder. His reign is the high-water mark of biblical wickedness. He married Jezebel of Sidon, daughter of Ethbaal the priest-king, and established Baal worship as state religion: building Baal temples in Samaria, supporting four hundred prophets of Asherah at his table, and persecuting the prophets of YHWH (<em>1 Kings 16:31-33; 18:4, 13</em>). Elijah confronted him repeatedly — drought, the Mount Carmel contest, the Naboth-vineyard judgment. The summary verdict is severe: <em>"But there was none like unto Ahab, which did sell himself to work wickedness in the sight of the LORD, whom Jezebel his wife stirred up"</em> (<em>1 Kings 21:25</em>).</p>'
    ),
    'artisan': (
        '<p>An artisan is a practitioner of a trained, skilled trade — the carpenter, mason, smith, weaver, embroiderer. Scripture honors them by name. Bezalel and Aholiab, filled with the Spirit of God in wisdom, understanding, knowledge, and all manner of workmanship, oversaw the tabernacle construction (<em>Exodus 31:1-11; 35:30-35</em>). Hiram of Tyre, a worker in bronze full of wisdom and understanding, cast the temple’s pillars (<em>1 Kings 7:13-14</em>). Christ Himself was a <em>tektōn</em> — a carpenter or builder — of Nazareth (<em>Mark 6:3</em>). Paul the apostle was a tentmaker (<em>Acts 18:3</em>). The kingdom of God uses artisans; the church should not be ashamed of them or treat their trades as second-tier vocations beneath knowledge-workers. Skilled hands are sanctified hands.</p>'
    ),
    'avodah': (
        '<p><em>Avodah</em> (עֲבוֹדָה) is the Hebrew word that fuses work, service, and worship into one concept. It is the verb of priests in the tabernacle (worship-as-service), of slaves in Egypt (forced labor), and of saints serving YHWH (worship-as-life). The same root names the Levitical service of the temple and the daily labor of the field. Hebrew refuses the modern Western distinction between sacred and secular labor: the carpenter at his bench and the priest at the altar are both engaged in <em>avodah</em> when done unto the LORD. <em>"Whatsoever ye do in word or deed, do all in the name of the Lord Jesus"</em> (<em>Colossians 3:17</em>). Christian labor is liturgy; the office and the field are altars when offered to God.</p>'
    ),
    'bow-the-knee': (
        '<p>To bow the knee is to publicly confess submission and worship — the body’s amen to lordship claimed. <em>"I have sworn by myself, the word is gone out of my mouth in righteousness, and shall not return, That unto me every knee shall bow, every tongue shall swear"</em> (<em>Isaiah 45:23</em>; quoted <em>Romans 14:11</em>). Paul applies it specifically to Christ: <em>"That at the name of Jesus every knee should bow, of things in heaven, and things in earth, and things under the earth"</em> (<em>Philippians 2:10</em>). The seven thousand in Israel who had not bowed the knee to Baal (<em>1 Kings 19:18</em>) are the model. Christian men bow the knee voluntarily to Christ now, that they may not be forced to bow at His judgment-seat then.</p>'
    ),
    'bummer': (
        '<p>"Bummer" is the boomer-era one-word verdict on any disappointing experience — originally drug-culture slang for a bad LSD trip, then broadened to any unpleasant turn of events. The slang dismisses the experience without engaging it: a single word as the whole response. Scripture treats disappointment differently — as fertile ground where the soul learns to lament, to hope, and to wait on the LORD. <em>"Cast thy burden upon the LORD, and he shall sustain thee"</em> (<em>Psalm 55:22</em>). David, Job, Hannah, Jeremiah, Habakkuk — each pressed their disappointment up into honest prayer rather than down into a dismissive shrug. "Bummer" is the verbal equivalent of stuffing the feeling. Christian men learn to feel honestly and name the disappointment to God.</p>'
    ),
    'canceled': (
        '<p>To be "canceled" in modern parlance is to have one’s social standing revoked en masse for past statements, actions, or beliefs deemed unacceptable by the current cultural consensus. The verdict is delivered by crowds — Twitter, employers, institutions — and the process is unstructured: no formal accusation, no witnesses, no opportunity to repent. Scripture distinguishes between just church discipline (<em>Matthew 18:15-17</em>) — private confrontation, witnessed warning, public exclusion, all aimed at restoration — and the crowd-driven excommunication of Pilate’s mob or the Sanhedrin’s rush verdict against Christ. Cancellation lacks both Matthew 18’s process and its restorative aim. Christians must repudiate cancel-culture’s shape while still practicing genuine biblical discipline.</p>'
    ),
    'cap': (
        '<p>"Cap" is modern slang for lying or exaggerating: <em>"That’s cap"</em> = "that’s false"; <em>"no cap"</em> = "no lie, I’m being honest." The vocabulary is often deployed playfully but always points at the same underlying problem Scripture has always named — deceit, false witness, lying speech. Whether the cap-accusation is comic or serious, it acknowledges a real moral category: truth and lying <em>are</em> real, opposite, and morally weighted. That instinct the broader culture has otherwise tried to erase — flattening truth into "your truth" and "my truth." The slang preserves the instinct even where philosophy has lost it. Christian men should affirm the instinct and tighten the definition: there is one truth, and lying speech is sin (<em>Ephesians 4:25</em>).</p>'
    ),
    'capernaum': (
        '<p>Capernaum was the Galilean town on the northwestern shore of the Sea of Galilee that Christ adopted as His ministry headquarters — <em>"his own city"</em> (<em>Matthew 9:1</em>). He taught in its synagogue with such authority that the people were astonished (<em>Mark 1:21-22</em>); He healed the centurion’s servant (<em>Matthew 8:5-13</em>), raised Jairus’s daughter (<em>Mark 5:21-43</em>), and fed the multitudes nearby. Despite witnessing more of Christ’s miracles than any other town, Capernaum did not repent. The Lord pronounced one of His sharpest woes upon it: <em>"And thou, Capernaum, which art exalted unto heaven, shalt be brought down to hell: for if the mighty works, which have been done in thee, had been done in Sodom, it would have remained until this day"</em> (<em>Matthew 11:23</em>).</p>'
    ),
    'cyrus-king': (
        '<p>Cyrus the Great was the founder of the Persian Empire (reigned 559-530 BC). He conquered Babylon in 539 BC, ending the seventy-year exile prophesied by Jeremiah (<em>Jeremiah 25:11-12; 29:10</em>). In his first regnal year he issued the decree (<em>Ezra 1:1-4</em>) permitting Jews to return to Jerusalem and rebuild the temple, with imperial funding. The most extraordinary detail is that Isaiah named him by name, calling him <em>"my shepherd"</em> and <em>"his anointed [messiah],"</em> some 150 years before his birth — when no Persian kingdom yet existed: <em>"That saith of Cyrus, He is my shepherd, and shall perform all my pleasure"</em> (<em>Isaiah 44:28-45:4</em>). It stands among Scripture’s most extraordinary specific prophecies. Pagan emperors are the LORD’s instruments.</p>'
    ),
    'drusilla': (
        '<p>Drusilla was the Jewish daughter of Herod Agrippa I (the king who killed James the brother of John, <em>Acts 12:1-2</em>), and the third wife of the Roman procurator Felix — whom she had married after he lured her from her first husband. She sat beside Felix at Caesarea as Paul, in chains, reasoned <em>"of righteousness, temperance, and judgment to come"</em> (<em>Acts 24:24-25</em>). Felix trembled and dismissed the apostle, saying, <em>"Go thy way for this time; when I have a convenient season, I will call for thee."</em> The convenient season never came. Drusilla and her son by Felix died in the eruption of Vesuvius in AD 79. The lesson is sober: gospel proximity does not save; only repentant faith does.</p>'
    ),
    'early-church': (
        '<p>The early church was born at Pentecost (<em>Acts 2:1-4</em>) and characterized from its first days by four marks: <em>"the apostles’ doctrine and fellowship, and in breaking of bread, and in prayers"</em> (<em>Acts 2:42</em>) — Word, fellowship, sacrament, and prayer. It had real conflicts (the Hellenist-Hebrew tension of <em>Acts 6</em>; the Jerusalem Council of <em>Acts 15</em>), real heresies to combat (Judaizers, Gnostics, Nicolaitans), and real discipline to exercise (Ananias and Sapphira, the man of <em>1 Corinthians 5</em>). But its commitment to apostolic truth, household-level community, and outward gospel mission shames most modern Western churches. The early church does not stand as nostalgic ideal but as <em>standard</em>. Recover those four marks and you recover the form.</p>'
    ),
    'epistles': (
        '<p>The Epistles are the twenty-one occasional letters of the New Testament — from Romans through Jude. Thirteen are Pauline (Romans, 1-2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1-2 Thessalonians, 1-2 Timothy, Titus, Philemon); one is anonymous but traditionally attributed to Paul or one of his circle (Hebrews); and seven are the General or Catholic Epistles (James, 1-2 Peter, 1-3 John, Jude). Each letter addresses specific churches and situations in the first-century Roman world — yet each dispenses universal apostolic teaching that remains binding for the church today. <em>"All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness"</em> (<em>2 Timothy 3:16</em>). Read them as letters to you.</p>'
    ),
    'evangelical-left': (
        '<p>"Evangelical Left" names a stream within American evangelicalism (Jim Wallis, Sojourners, Ron Sider, Tony Campolo, others) that emphasizes social-justice concerns — poverty, racial reconciliation, environmental stewardship, peace activism — sometimes at the expense of personal-righteousness doctrines historically central to evangelical conviction. Scripture refuses the binary the term implies. The prophets demanded <em>both</em> justice and holiness: <em>"let judgment run down as waters, and righteousness as a mighty stream"</em> (<em>Amos 5:24</em>) is paired with denunciation of idolatry. James teaches that <em>"pure religion and undefiled before God and the Father is this, To visit the fatherless and widows in their affliction, <strong>and</strong> to keep himself unspotted from the world"</em> (<em>James 1:27</em>). The biblical model refuses to separate gospel message from gospel ethics — but it never makes ethics the gospel.</p>'
    ),
    'forth-tell': (
        '<p>"Forth-tell" names the prophet’s primary work: declaring publicly what God has already revealed. It is distinct from <em>foretelling</em> (predicting future events) — the popular but reduced sense of "prophecy" in modern usage. Most Old Testament prophecy is in fact forth-telling: <em>"Repent ye, and turn yourselves from your idols"</em> (<em>Ezekiel 14:6</em>); <em>"Hear the word of the LORD"</em> (<em>Jeremiah 7:2</em>); <em>"Hath he not shewed thee, O man, what is good"</em> (<em>Micah 6:8</em>). The prophet stands in the public square and forth-tells what the people already know in the law but have stopped doing. Forth-telling is the sermon’s spine; foretelling is its occasional crown. Christian preaching is mostly the former — and ought to be unashamed of it.</p>'
    ),
    'gall': (
        '<p>Gall is a bitter and poisonous substance — and in Scripture it becomes the figure of three things. First, the bitter potion offered to Christ on the cross: <em>"They gave him vinegar to drink mingled with gall: and when he had tasted thereof, he would not drink"</em> (<em>Matthew 27:34</em>; fulfilling <em>Psalm 69:21</em>). Second, the bitter fruit of injustice: <em>"Ye have turned judgment into gall, and the fruit of righteousness into hemlock"</em> (<em>Amos 6:12</em>; cf. <em>Hosea 10:4</em>). Third, the description of a soul in bondage to sin: Peter said of Simon Magus, <em>"For I perceive that thou art in the gall of bitterness, and in the bond of iniquity"</em> (<em>Acts 8:23</em>). Christ tasted gall to remove its sting from us.</p>'
    ),
    'gravity': (
        '<p>Gravity (Greek <em>semnotēs</em>) is the settled, dignified weight of a Spirit-formed life — the bearing of a man or woman in whom the eternal has become substantial. It is required of elders: <em>"One that ruleth well his own house, having his children in subjection with all gravity"</em> (<em>1 Timothy 3:4</em>); of older men: <em>"That the aged men be sober, grave, temperate, sound in faith, in charity, in patience"</em> (<em>Titus 2:2</em>); and prayed for in every congregation: <em>"that we may lead a quiet and peaceable life in all godliness and honesty"</em> (<em>1 Timothy 2:2</em>). Gravity is not stiffness, severity, or pomposity — it is depth. The man whose words mean something has gravity; the chronic clown has not yet earned it.</p>'
    ),
    'hearthside': (
        '<p>Hearthside is the place beside the hearth — the chair drawn near the fire, the bench by the warming-pan, the family circle where flame and food and stories gather. Scripture does not use the modern English word, but the picture is everywhere. The disciples on the Emmaus road sat down with the risen Christ and recognized Him in the breaking of bread (<em>Luke 24:30-31</em>). Peter warmed himself at a brazier in the high priest’s courtyard (<em>John 18:18</em>). Christ Himself prepared a charcoal fire on the shore and broke bread with the disciples after the resurrection (<em>John 21:9-13</em>). The Christian home should keep its hearthside warm — its table set, its fire lit, its chairs filled with neighbors and travelers and family.</p>'
    ),
    'hippie': (
        '<p>"Hippie" names the 1960s American counterculture identity built around peace, love, communal living, drug use, sexual permissiveness, and rejection of "the establishment" — mainstream institutions, the Vietnam War, conventional authority. The movement borrowed deeply from Christian vocabulary — love, peace, brotherhood, community, simplicity — while detaching every term from Christ Himself. The resulting words have been doing damage in American culture ever since: <em>"love"</em> shorn of moral content, <em>"peace"</em> as drug-induced inertia, <em>"community"</em> as cohabitation. The Christian church must therefore not abandon the original biblical terms but reclaim them. True love is covenant-faithful; true peace is reconciliation with God; true community is the church of Jesus Christ. Take the words back from the haze.</p>'
    ),
    'horeb': (
        '<p>Horeb is the mountain of God in the Sinai wilderness — the same elevation Scripture also names <em>Sinai</em>. It is the geographical pivot of the Pentateuch and beyond. Moses saw the burning bush there and was commissioned (<em>Exodus 3:1-6</em>); Israel heard the Voice from the fire and received the Ten Commandments there (<em>Deuteronomy 4:10-15; 5:2-22</em>); Elijah, fleeing Jezebel, came there forty days and forty nights to hear <em>"the still small voice"</em> after the wind, earthquake, and fire (<em>1 Kings 19:8-12</em>). Horeb is therefore where God reveals Himself to men at the end of their strength — to the man chasing a flock, to the trembling nation, to the exhausted prophet. Each meeting changes the man who comes back down.</p>'
    ),
    'mourning': (
        '<p>Mourning, in Scripture, is public, sustained, often communal lamentation over death, sin, exile, or covenant betrayal — marked by tearing of clothes (<em>Genesis 37:34</em>), sackcloth (<em>Esther 4:1-3</em>), ashes on the head (<em>2 Samuel 13:19</em>), fasting (<em>Daniel 10:2-3</em>), and dirge-singing (<em>2 Samuel 1:17-27</em>, David’s lament for Saul and Jonathan). Modern Western culture has nearly lost the discipline; grief is privatized, hurried, professionalized into the funeral home. Christ blesses the mourners: <em>"Blessed are they that mourn: for they shall be comforted"</em> (<em>Matthew 5:4</em>). The Spirit teaches the church both how to mourn — over death, over sin, over the world — and how to be comforted. Christian men must recover both halves.</p>'
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
