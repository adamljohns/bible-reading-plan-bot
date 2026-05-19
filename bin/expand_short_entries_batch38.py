#!/usr/bin/env python3
"""Batch 38 — expand 25 more entries from the 50-60 word bucket.

Targets: body gestures, NT geography, prophetic imagery, doctrines,
OT events, covenant language, slang reframes, and armor of God.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'lift-hands': (
        '<p>The lifting of the hands is the ancient gesture of prayer, blessing, supplication, or oath — the open palm raised toward God in physical confession that the help, the gift, or the verdict comes from Him. Aaron lifted his hands to bless Israel (<em>Leviticus 9:22</em>); Moses lifted his hands at Rephidim while Joshua fought Amalek (<em>Exodus 17:11</em>); David lifted his hands as the evening sacrifice ascended: <em>"Let my prayer be set forth before thee as incense; and the lifting up of my hands as the evening sacrifice"</em> (<em>Psalm 141:2</em>); Paul commanded men in particular to pray <em>"lifting up holy hands, without wrath and doubting"</em> (<em>1 Timothy 2:8</em>). The body announces what the soul means. Christians who never lift their hands in worship have suppressed half the language of prayer.</p>'
    ),
    'lips': (
        '<p>The lips are the boundary between heart and world — the channel through which the inner soul speaks itself into history. In Scripture they are the instruments of confession (<em>"with the mouth confession is made unto salvation"</em>, <em>Romans 10:10</em>), blessing, prayer, and praise — and, when undisciplined, the conduit for slander, lying, gossip, and folly. Isaiah cried <em>"Woe is me! for I am undone; because I am a man of unclean lips"</em> when he saw the LORD (<em>Isaiah 6:5</em>); the seraph touched his lips with a live coal from the altar, and his iniquity was purged. <em>"The lip of truth shall be established for ever: but a lying tongue is but for a moment"</em> (<em>Proverbs 12:19</em>). Guard the lips.</p>'
    ),
    'looking-toward-jerusalem': (
        '<p>"Looking toward Jerusalem" was Daniel’s exile posture of prayer: <em>"his windows being open in his chamber toward Jerusalem, he kneeled upon his knees three times a day, and prayed, and gave thanks before his God, as he did aforetime"</em> (<em>Daniel 6:10</em>) — even after the king’s decree forbade it on penalty of death. Solomon had instructed the people at the temple dedication: if exiled, <em>"if they pray toward their land... and toward the city which thou hast chosen, and toward the house which I have built for thy name: Then hear thou their prayer"</em> (<em>1 Kings 8:48-49</em>). Daniel did so even at risk of the lions’ den — and the LORD shut the lions’ mouths. The Christian’s prayer is now oriented toward the heavenly Jerusalem (<em>Hebrews 12:22</em>).</p>'
    ),
    'master': (
        '<p>In the KJV, <em>Master</em> translates several Greek words used of Christ, and the convergence is theologically rich. <em>Didaskalos</em> ("teacher") — the most frequent — used over forty times of Jesus: <em>"Master, we know that thou art a teacher come from God"</em> (<em>John 3:2</em>). <em>Kurios</em> ("Lord") — confessed by every saint: <em>"Jesus is Lord"</em> (<em>1 Corinthians 12:3</em>). <em>Epistatēs</em> ("overseer") — used by Luke seven times. <em>Despotēs</em> ("sovereign owner"). <em>Kathēgētēs</em> ("guide-leader"). <em>"But be not ye called Rabbi: for one is your Master, even Christ; and all ye are brethren... Neither be ye called masters: for one is your Master, even Christ"</em> (<em>Matthew 23:8, 10</em>). He is one Teacher and one Lord at once.</p>'
    ),
    'patmos': (
        '<p>Patmos is the small, rocky Aegean island — about 35 miles southwest of Ephesus — that the Roman empire used as a penal colony in the late first century. The apostle John was exiled there <em>"for the word of God, and for the testimony of Jesus Christ"</em> (<em>Revelation 1:9</em>), probably under Domitian (c. AD 95). It was from Patmos that the Lord Jesus Christ delivered the final book of the Bible — the Apocalypse — to His servant: <em>"What thou seest, write in a book, and send it unto the seven churches which are in Asia"</em> (<em>1:11</em>). Patmos is Scripture’s case study that imperial exile cannot silence the apostolic voice. God writes Revelation in the place Caesar chose for forgetting.</p>'
    ),
    'pour-out': (
        '<p>To <em>pour out</em> is to empty by pouring — and figuratively, to give without holding back, to spend the whole vessel. In Scripture it is the verb of total bestowing. God pours out His Spirit: <em>"I will pour out my spirit upon all flesh"</em> (<em>Joel 2:28</em>; <em>Acts 2:17</em>). God pours out His wrath in the seven bowls of <em>Revelation 16</em>. God pours out His love: <em>"the love of God is shed abroad in our hearts by the Holy Ghost which is given unto us"</em> (<em>Romans 5:5</em>). Saints in turn pour out their souls before Him (<em>1 Samuel 1:15; Psalm 62:8</em>) and their lives as drink offerings: <em>"For I am now ready to be offered"</em> (<em>2 Timothy 4:6</em>). The Christian life is a pouring out.</p>'
    ),
    'quench-the-spirit': (
        '<p>To "quench the Spirit" is to suppress, dampen, or refuse the prompting and presence of the Holy Spirit in the believer or the assembly. Paul commands the Thessalonians directly: <em>"Quench not the Spirit. Despise not prophesyings"</em> (<em>1 Thessalonians 5:19-20</em>). The injunction assumes the Spirit’s fire is real, present, and capable of being either tended or smothered by His own people. The Spirit is quenched by harbored sin, by neglect of the Word, by refusal to obey conviction, by formalism that crowds out spontaneous response, by leadership that suppresses gifts. Paired with Paul’s parallel command — <em>"And grieve not the holy Spirit of God"</em> (<em>Ephesians 4:30</em>) — the doctrine is plain: the Spirit can be both grieved and quenched. Tend the fire.</p>'
    ),
    'reaping': (
        '<p>Reaping is the harvest counterpart of sowing — the literal cutting and gathering of grain, and the figurative receiving of what one has planted. Scripture binds the literal to the moral with great seriousness: <em>"Be not deceived; God is not mocked: for whatsoever a man soweth, that shall he also reap. For he that soweth to his flesh shall of the flesh reap corruption; but he that soweth to the Spirit shall of the Spirit reap life everlasting"</em> (<em>Galatians 6:7-8</em>). Christ also names the disciples laborers in the harvest: <em>"The harvest truly is plenteous, but the labourers are few; pray ye therefore the Lord of the harvest, that he will send forth labourers into his harvest"</em> (<em>Matthew 9:37-38</em>). The Christian reaps every day what he has sown.</p>'
    ),
    'shepherd-king': (
        '<p>The Shepherd-King is the biblical ideal of the king as shepherd of his people — not boss, not tyrant, not figurehead. The figure is rooted in David, the literal shepherd-boy made king after God’s own heart, and is developed by the prophets when later kings fail their flocks. Ezekiel’s great rebuke and promise: <em>"I will set up one shepherd over them, and he shall feed them, even my servant David; he shall feed them, and he shall be their shepherd. And I the LORD will be their God, and my servant David a prince among them"</em> (<em>Ezekiel 34:23-24</em>; cf. <em>vv. 1-31</em>). It is fulfilled in Christ — both Good Shepherd (<em>John 10</em>) and King of Kings (<em>Revelation 19:16</em>). One Lord, one office.</p>'
    ),
    'silence': (
        '<p>Silence, in Scripture, is the disposition of restraint in speech and inward stillness before God. It is commanded as the proper posture before His throne: <em>"Hold thy peace at the presence of the Lord GOD"</em> (<em>Zephaniah 1:7</em>); <em>"But the LORD is in his holy temple: let all the earth keep silence before him"</em> (<em>Habakkuk 2:20</em>); <em>"Be silent, O all flesh, before the LORD"</em> (<em>Zechariah 2:13</em>). It is prized in His servants: <em>"And that ye study to be quiet, and to do your own business"</em> (<em>1 Thessalonians 4:11</em>). Yet Scripture distinguishes <em>godly</em> silence (waiting on the LORD) from <em>cowardly</em> silence (the watchman who will not blow the trumpet, <em>Ezekiel 33:6</em>). Know which yours is.</p>'
    ),
    'unbridled': (
        '<p>"Unbridled" describes a tongue, a passion, or a life with no governing strap — like a horse with no bit, going wherever instinct or appetite takes it. James warns the church: <em>"If any man among you seem to be religious, and bridleth not his tongue, but deceiveth his own heart, this man’s religion is vain"</em> (<em>James 1:26</em>). He returns to the figure in chapter 3: <em>"Behold, we put bits in the horses’ mouths, that they may obey us; and we turn about their whole body... Even so the tongue is a little member, and boasteth great things"</em> (<em>James 3:3, 5</em>). The New Testament treats unbridled speech, lust, and ambition as the defining marks of a soul not yet under Christ’s rein. The Christian wears the bridle gladly.</p>'
    ),
    'viper-brood': (
        '<p>"Brood of vipers" — KJV <em>"generation of vipers"</em> — is the unsparing rebuke John the Baptist and Jesus repeatedly addressed to the religious establishment of their day. John used it at his river-baptism: <em>"O generation of vipers, who hath warned you to flee from the wrath to come?"</em> (<em>Matthew 3:7; Luke 3:7</em>). Christ used it of the Pharisees and scribes more than once: <em>"O generation of vipers, how can ye, being evil, speak good things?"</em> (<em>Matthew 12:34</em>); <em>"Ye serpents, ye generation of vipers, how can ye escape the damnation of hell?"</em> (<em>23:33</em>). The phrase is the New Testament’s sharpest word, and it is reserved for religious leaders whose teaching keeps reproducing the same poisonous offspring — never for sinners coming for healing.</p>'
    ),
    'watchstand': (
        '<p>A watchstand is the fixed post at which a sentry is posted — the spot from which he is responsible to perceive and report. Habakkuk pictures it directly: <em>"I will stand upon my watch, and set me upon the tower, and will watch to see what he will say unto me, and what I shall answer when I am reproved"</em> (<em>Habakkuk 2:1</em>). The prophet’s watchstand is his appointed place of waiting and watching for the LORD’s answer — the discipline of staying at one’s post until heaven speaks. Christian pastors, fathers, and elders each have a watchstand. The post is not optional; it is appointed. <em>"Watch ye therefore, and pray always"</em> (<em>Luke 21:36</em>). Stand at your post.</p>'
    ),
    'weeping': (
        '<p>Weeping is the shedding of tears, often audibly — and in Scripture it is used for grief, repentance, intercession, and even joy. Hannah wept and prayed at Shiloh until Eli thought her drunken (<em>1 Samuel 1:10</em>). David wept until exhausted at Ziklag when the Amalekites had burned the city (<em>1 Samuel 30:4</em>). Hezekiah wept in his sickness toward the wall (<em>2 Kings 20:2-3</em>; <em>Isaiah 38:3</em>). Mary Magdalene wept at the empty tomb until the Lord spoke her name (<em>John 20:11-16</em>). Christ Himself wept at Lazarus’s tomb (<em>John 11:35</em>) and over Jerusalem (<em>Luke 19:41</em>). Paul wept warning the Ephesian elders night and day for three years (<em>Acts 20:31</em>). Tears in Scripture are weighed, not wasted: <em>"Put thou my tears into thy bottle"</em> (<em>Psalm 56:8</em>).</p>'
    ),
    'winnowing': (
        '<p>Winnowing is the post-threshing agricultural process of tossing the mixed grain-and-chaff into the air with a winnowing fork, so that the lighter chaff is blown away by the wind and the heavier kernel falls back to the threshing floor. In Scripture it becomes the figure of God’s decisive separation of the righteous from the wicked. John the Baptist describes the coming Christ with the fan (winnowing-fork) in His hand: <em>"Whose fan is in his hand, and he will throughly purge his floor, and gather his wheat into the garner; but he will burn up the chaff with unquenchable fire"</em> (<em>Matthew 3:12; Luke 3:17</em>). The wind on the floor reveals what was wheat all along.</p>'
    ),
    'bread-from-heaven': (
        '<p>"Bread from heaven" is the manna with which YHWH fed Israel forty years in the wilderness (<em>Exodus 16</em>) — given by miracle each morning, gathered before the sun grew hot, ceased only on Sabbath, and called <em>"bread from heaven"</em> by the Psalmist: <em>"And had rained down manna upon them to eat, and had given them of the corn of heaven"</em> (<em>Psalm 78:24</em>; cf. <em>105:40</em>). Christ takes up the imagery directly in <em>John 6:31-58</em>, contrasting the manna (which fed the body and let the eaters die) with Himself as the <em>true</em> bread from heaven: <em>"I am the living bread which came down from heaven: if any man eat of this bread, he shall live for ever"</em> (<em>v. 51</em>). The wilderness manna pointed forward to Him.</p>'
    ),
    'breastplate-righteousness': (
        '<p>The breastplate of righteousness is the second piece of the armor of God in Paul’s spiritual-warfare passage: <em>"Stand therefore, having your loins girt about with truth, and having on the breastplate of righteousness"</em> (<em>Ephesians 6:14</em>). It covers the soldier’s vital organs — heart and lungs — and protects specifically against the accusations of the enemy. Two senses run together. First, <em>imputed</em> righteousness: Christ’s perfect righteousness reckoned to the saint by faith (<em>Romans 4:5; 2 Corinthians 5:21</em>) — the legal defense against every charge brought at the courtroom of conscience or before the throne of God. Second, <em>practical</em> righteousness: the saint’s holy walk that gives the enemy no real foothold. Both protect; both are required.</p>'
    ),
    'cleave': (
        '<p>To <em>cleave</em> is to adhere strongly, to be glued to, to stick fast. It is the covenantal verb of marriage — <em>"Therefore shall a man leave his father and his mother, and shall cleave unto his wife: and they shall be one flesh"</em> (<em>Genesis 2:24</em>) — and the verb of the soul’s posture toward God: <em>"Thou shalt fear the LORD thy God; him shalt thou serve, and to him shalt thou cleave"</em> (<em>Deuteronomy 10:20; 11:22; 30:20</em>). The English word ironically has two opposite meanings — <em>"to split"</em> and <em>"to adhere"</em> — but biblical cleaving is always the <em>adhering</em> kind. The covenant verb commands the soul: do not let go. <em>"My soul followeth hard after thee: thy right hand upholdeth me"</em> (<em>Psalm 63:8</em>).</p>'
    ),
    'couch-potato': (
        '<p>"Couch potato" is Gen-X slang (originating in the 1970s, peaking with cable TV) for a person whose dominant activity is sedentary screen-watching — originally television, now also streaming, gaming, scrolling, and YouTube binging. The slang treats the disposition as comic; Scripture treats it as a moral category. The sluggard of Proverbs and the couch potato of late-twentieth-century America are the same man, separated only by 2,500 years of upholstery. <em>"How long wilt thou sleep, O sluggard? when wilt thou arise out of thy sleep?"</em> (<em>Proverbs 6:9</em>); <em>"The slothful man hideth his hand in his bosom; it grieveth him to bring it again to his mouth"</em> (<em>26:15</em>). Get off the couch. The kingdom is built on action.</p>'
    ),
    'covenant-faithfulness': (
        '<p>Covenant faithfulness is the unwavering steadfastness of one party to a covenant — the disposition that keeps the bond when the other party has not earned it. The Hebrew <em>chesed</em> covers it: the LORD’s loyal love that does not fail His people through their unfaithfulness; the saint’s loyalty that mirrors His. Jeremiah’s great confession from the ash heap of Lamentations: <em>"It is of the LORD’s mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness"</em> (<em>Lamentations 3:22-23</em>). <em>"If we believe not, yet he abideth faithful: he cannot deny himself"</em> (<em>2 Timothy 2:13</em>). God’s covenant faithfulness is the only reason the human race has a future. The saint mirrors it in marriage, friendship, and church.</p>'
    ),
    'crossing-red-sea': (
        '<p>The Crossing of the Red Sea is the climactic deliverance of Israel from Egypt, when YHWH parted the sea before His people, brought them through on dry ground, and drowned Pharaoh’s pursuing army (<em>Exodus 14</em>). It is the defining act of YHWH’s salvation in Old Testament memory — sung in Moses’ song the morning after: <em>"I will sing unto the LORD, for he hath triumphed gloriously: the horse and his rider hath he thrown into the sea"</em> (<em>Exodus 15:1</em>) — and referenced repeatedly through Scripture as the great paradigm of redemption (<em>Psalm 78:13; 106:9; 136:13-15; Isaiah 51:10</em>). Paul typologically connects it to Christian baptism: <em>"all our fathers... were all baptized unto Moses in the cloud and in the sea"</em> (<em>1 Corinthians 10:1-2</em>).</p>'
    ),
    'deep-state': (
        '<p>"Deep state" is the modern political term for hidden bureaucratic, intelligence, and institutional power that operates behind the visible elected government — sometimes used neutrally, often pejoratively. Scripture has long known that earthly powers are not what they appear. Behind every human ruler and institution stand spiritual principalities: <em>"For we wrestle not against flesh and blood, but against principalities, against powers, against the rulers of the darkness of this world, against spiritual wickedness in high places"</em> (<em>Ephesians 6:12</em>). Daniel sees behind the throne of Persia <em>"the prince of the kingdom of Persia"</em> resisting Gabriel (<em>Daniel 10:13</em>). The biblical worldview recognizes hidden powers behind visible authority structures. Christian discernment must look up and behind.</p>'
    ),
    'derbe': (
        '<p>Derbe was a city in Lycaonia — the eastern frontier of Paul’s first missionary journey, in southern Asia Minor. After being dragged outside Lystra and stoned and left for dead, Paul rose and the next day departed with Barnabas to Derbe: <em>"And when they had preached the gospel to that city, and had taught many, they returned again to Lystra"</em> (<em>Acts 14:20-21</em>). Gaius of Derbe later traveled with Paul, joining the collection-delegation to Jerusalem (<em>Acts 20:4</em>). Of all the cities Paul evangelized on the first journey, Derbe is the only one where Acts records no opposition, no riot, no expulsion. Sometimes the gospel field is hostile; sometimes it is, briefly, ready. Preach in both.</p>'
    ),
    'divided-monarchy': (
        '<p>The Divided Monarchy is the historical period after Solomon’s death when the kingdom of Israel split in two. The ten northern tribes followed Jeroboam to form the kingdom of <em>Israel</em> (931 BC), which lasted 209 years through nineteen kings of nine dynasties — all wicked — until the Assyrian conquest of Samaria in 722 BC ended it (<em>2 Kings 17</em>). The two southern tribes remained under the house of David as the kingdom of <em>Judah</em> (931 BC), which lasted 345 years through twenty kings of one Davidic line — with periodic revivals — until the Babylonian conquest of Jerusalem in 586 BC ended it (<em>2 Kings 25</em>). <em>1 Kings 12</em> through <em>2 Kings 17</em> covers the divided period; <em>2 Kings 18-25</em> covers Judah alone.</p>'
    ),
    'fall-of-jerusalem-586': (
        '<p>The Fall of Jerusalem in 586 BC was the Babylonian conquest of the city under Nebuchadnezzar after a two-and-a-half-year siege. The city walls were breached; Solomon’s temple was burned (<em>2 Kings 25:8-9</em>); the royal palace was destroyed; Zedekiah was captured fleeing toward Jericho, his sons were slaughtered before his eyes, and his eyes were then put out (<em>25:7</em>); and the third and final deportation to Babylon was carried out. It was the defining catastrophe of the Old Testament — prophesied for centuries by Isaiah, Jeremiah, Ezekiel, and others, and fulfilling the covenant curses of <em>Deuteronomy 28</em>. The book of Lamentations is the funeral-dirge for the fallen city: <em>"How doth the city sit solitary, that was full of people!"</em> (<em>Lamentations 1:1</em>).</p>'
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
