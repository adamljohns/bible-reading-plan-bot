#!/usr/bin/env python3
"""Batch 14 — expand 25 more thin entries to 90-110 words each.

Targets: prophetic books, disciplines, women's-discipleship terms,
cult/idolatry vocabulary, geography, and Christology from the 30-50
word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'lament-discipline': (
        '<p>Lament is the discipline of bringing grief, anger, and confusion directly to God in prayer — a covenant form of worship that refuses both denial and despair. Roughly a third of the Psalms are lament psalms (e.g., <em>Psalm 13, 22, 42, 88</em>), modeling the move from "How long, O LORD?" to "Yet I will trust." Lament names the loss honestly, addresses God personally, often complains bitterly, and almost always pivots to renewed confession of faith. It is not unbelief; it is faith refusing to leave the room when God seems silent. Modern Christianity has lost the language of lament and pays for it in shallow joy and silent suffering — Christian men recovering it learn how to grieve like men, before God, without softening into self-pity.</p>'
    ),
    'micah': (
        '<p>Micah is the prophetic book named for the prophet from Moresheth in Judah (c. 750-686 BC), a contemporary of Isaiah. The book denounces greedy rulers and corrupt priests who "<em>build up Zion with blood</em>" (<em>Micah 3:10</em>), predicts the Messiah’s birth in Bethlehem Ephratah (<em>Micah 5:2</em>) — the prophecy Herod’s scribes quoted to the Magi — and summarizes the whole law in one famous verse: <em>"He hath shewed thee, O man, what is good; and what doth the LORD require of thee, but to do justly, and to love mercy, and to walk humbly with thy God?"</em> (<em>Micah 6:8</em>). Micah’s structure alternates judgment and hope across three cycles, closing with covenant mercy and the unfailing oath sworn to Abraham.</p>'
    ),
    'pilgrimage': (
        '<p>Pilgrimage is the lifelong Christian discipline of living as a stranger and sojourner on earth, with treasures and citizenship lodged in the city to come (<em>Hebrews 11:13-16</em>; <em>Philippians 3:20</em>; <em>1 Peter 2:11</em>). The patriarchs <em>"confessed that they were strangers and pilgrims on the earth"</em>; the present journey is marked by tents rather than mansions. Pilgrimage does not mean abandoning the cultural mandate — the pilgrim builds, plants, marries, fathers, and disciples — but he does so as a man passing through, refusing to over-invest in a country that is not his final home. This is the antidote to both worldliness (settling in) and gnostic escapism (refusing to build). Build well; travel light.</p>'
    ),
    'rebuke-biblical': (
        '<p>Biblical rebuke is pointed verbal correction of error or sin, commanded as a regular part of gospel ministry: <em>"reprove, rebuke, exhort with all longsuffering and doctrine"</em> (<em>2 Timothy 4:2</em>). Proverbs draws the line of receiving it: <em>"Rebuke a wise man, and he will love thee... reprove not a scorner, lest he hate thee"</em> (<em>Proverbs 9:8</em>). Rebuke is not insult, mockery, or venting — it is the loving, specific, scripture-grounded naming of sin or error for the sake of repentance. Pastors must rebuke (<em>Titus 1:13; 2:15</em>); fathers must rebuke their sons (<em>Proverbs 13:24</em>); friends must rebuke their friends (<em>Proverbs 27:5-6</em>). A church that cannot rebuke cannot disciple, and a man who cannot receive rebuke cannot grow.</p>'
    ),
    'reformation-sunday': (
        '<p>Reformation Sunday is the Protestant observance commemorating Martin Luther’s posting of the Ninety-Five Theses on the door of the Castle Church in Wittenberg on October 31, 1517 — traditionally observed the last Sunday of October. It celebrates the recovery of the gospel from medieval accretions and the rallying cries that crystallized over the following century: <em>sola Scriptura</em>, <em>sola fide</em>, <em>sola gratia</em>, <em>solus Christus</em>, <em>soli Deo gloria</em>. Where Halloween cosplays death, Reformation Sunday confesses resurrection. Reformed and confessional Protestants read Luther, sing <em>A Mighty Fortress</em>, and rehearse the doctrines that pulled the church back to Scripture. It is a family and ecclesial reminder that the church is always reforming — <em>ecclesia reformata, semper reformanda</em>.</p>'
    ),
    'shame-toxic': (
        '<p>Toxic shame is the condemning, identity-destroying false shame that says <em>"I am wrong"</em> rather than <em>"I did wrong"</em> — a counterfeit conviction that does not lead to repentance but to despair, hiding, and self-loathing. It is not sanctified by Scripture; it is the residue of Adam in the bushes (<em>Genesis 3:8-10</em>) and the accusing voice of <em>"the accuser of the brethren"</em> (<em>Revelation 12:10</em>). Healthy biblical guilt names a deed and calls for confession; toxic shame names the soul itself as worthless. Christ absorbed both at the cross — <em>"despising the shame"</em> (<em>Hebrews 12:2</em>) — so there is now no condemnation (<em>Romans 8:1</em>). Christian men under toxic shame must learn to preach the verdict of justification back to themselves.</p>'
    ),
    'stiff-necked': (
        '<p>Stiff-necked is the biblical figure for stubbornly refusing instruction or correction, drawn from oxen that will not bend the neck to the yoke. It is God’s repeated diagnosis of Israel under the old covenant: <em>"I have seen this people, and, behold, it is a stiffnecked people"</em> (<em>Exodus 32:9; 33:3; 34:9</em>; <em>Deuteronomy 9:6, 13</em>). Stephen leveled the same charge against the Sanhedrin: <em>"Ye stiffnecked and uncircumcised in heart and ears, ye do always resist the Holy Ghost"</em> (<em>Acts 7:51</em>). The opposite of stiff-necked is teachable, submitted, broken — the disposition Christ blesses in <em>Matthew 5:3-5</em>. Every Christian man must regularly ask the LORD to break his neck, gently, before discipline becomes necessary.</p>'
    ),
    'sympathy': (
        '<p>Sympathy (Greek <em>sumpathēs</em>, "fellow-suffering") is the fellow-feeling of another’s pain that moves the soul to compassionate response. Christ is the high priest <em>"touched with the feeling of our infirmities"</em> (<em>Hebrews 4:15</em>) — He does not pity us from a distance but enters our experience by His own incarnate sufferings. Peter therefore commands the church: <em>"having compassion one of another"</em> (<em>1 Peter 3:8</em>). Sympathy is more than awareness; it is the soul actually bending toward another’s grief to bear it. The cold detachment of the modern professional class — even in pulpits — fails this Christian virtue. Sympathy keeps the strong gentle with the weak, the husband patient with his wife, and the father careful with his children.</p>'
    ),
    'tarshish': (
        '<p>Tarshish was a distant port — most likely <em>Tartessos</em> in southern Spain — representing the farthest known west of the ancient Mediterranean world. It was famous for silver, iron, tin, and lead (<em>Ezekiel 27:12</em>), and "ships of Tarshish" were the great seagoing merchant vessels Solomon’s fleet was built on (<em>1 Kings 10:22</em>). Jonah famously fled toward Tarshish to escape the call to Nineveh — toward the western horizon, the opposite direction (<em>Jonah 1:3</em>) — only to be overtaken by storm. Tarshish in Scripture is the symbol of the far country to which the rebellious soul runs, and from which the LORD draws His people back. <em>Psalm 72:10</em> prophesies the kings of Tarshish bringing tribute to Messiah.</p>'
    ),
    'the-twelve': (
        '<p>"The Twelve" carries two distinct biblical meanings. First, the twelve apostles chosen by Christ (<em>Mark 3:13-19</em>) as foundational witnesses of the gospel — the New-Covenant counterpart to the twelve tribes of Israel, men whose names are written on the foundations of the New Jerusalem (<em>Revelation 21:14</em>). Second, the Book of the Twelve — the twelve Minor Prophets (Hosea through Malachi) gathered as one scroll in the Hebrew canon, addressing covenant infidelity, coming judgment, and ultimate restoration. Both groups are foundational and structural: twelve apostles for the church, twelve prophets for the prophetic witness. Twelve in Scripture marks covenant completeness, and both Twelves point to the same Christ — Lord of the church and substance of the prophets.</p>'
    ),
    'titus-women': (
        '<p>"Titus 2 women" refers to Paul’s commissioning of older women in <em>Titus 2:3-5</em> to teach the younger women how to be wives, mothers, and homemakers. Their commission is explicit: <em>"that they may teach the young women to be sober, to love their husbands, to love their children, to be discreet, chaste, keepers at home, good, obedient to their own husbands, that the word of God be not blasphemed."</em> Notice the commission runs woman-to-woman, not from the pulpit, and it is unapologetically domestic, marital, and obedience-shaped. This is the patriarchal alternative to feminist discipleship: older Christian wives, theologically literate and seasoned, training the next generation in the high vocation of biblical womanhood under the headship of their husbands.</p>'
    ),
    'true-widow': (
        '<p>"True widow" is Paul’s precise category in <em>1 Timothy 5:3-16</em>: <em>"Honour widows that are widows indeed."</em> A "true widow" is the older woman, sixty or above, without family to support her, of faithful character (one husband, brought up children, lodged strangers, washed the saints’ feet), who depends on the church’s ongoing care and gives herself to <em>"supplications and prayers night and day"</em> (<em>1 Timothy 5:5</em>). She is distinguished sharply from younger widows, whom Paul urges to remarry, bear children, and guide the house (<em>1 Timothy 5:14</em>). The category protects the church from idle dependence on the one hand and neglect of the truly needy on the other — diaconal sobriety, not sentimentality.</p>'
    ),
    'weeks-feast': (
        '<p>The Feast of Weeks (Hebrew <em>Shavuot</em>; Greek <em>Pentēkostē</em>, "fiftieth") was the annual feast falling seven weeks (fifty days) after Passover, celebrating the wheat harvest’s first fruits and, in later Jewish tradition, the giving of the law at Sinai (<em>Leviticus 23:15-22</em>; <em>Deuteronomy 16:9-12</em>). It was on this feast that the Holy Spirit was poured out on the gathered disciples in <em>Acts 2</em>, fulfilling the typology: the Sinai-fire of stone-tablet law gave way to the Pentecost-fire of Spirit-written hearts (<em>Jeremiah 31:33</em>; <em>2 Corinthians 3:3</em>). The wheat first-fruits of Sinai became the human first-fruits of three thousand souls. Pentecost is therefore the New-Covenant Feast of Weeks, fulfilled in the Spirit-born church.</p>'
    ),
    'young-women': (
        '<p>"Young women" is the category Paul commits to the older women’s care in <em>Titus 2:4-5</em>. The training agenda is explicit and beautifully unfashionable: <em>"that they may teach the young women to be sober, to love their husbands, to love their children, to be discreet, chaste, keepers at home, good, obedient to their own husbands, that the word of God be not blasphemed."</em> The teaching runs woman-to-woman, not from the pulpit, and centers on the domestic vocation God has actually assigned. Where the world disciples young women into career idolatry, sexual revolution, and contempt for the household, the church is to disciple them into glad submission, fruitful motherhood, and joyful covenant home-building under Christ.</p>'
    ),
    'ararat': (
        '<p>Ararat is the mountainous region — in modern eastern Turkey near the Armenian border — where Noah’s ark came to rest after the Flood (<em>Genesis 8:4</em>). Scripture says <em>"upon the mountains of Ararat,"</em> plural: a range, not a single peak, though traditional sites (e.g., modern Mount Ağrı, 16,854 ft) have drawn pilgrims for centuries. The name appears again as a kingdom in <em>2 Kings 19:37</em> / <em>Isaiah 37:38</em> (the refuge of Sennacherib’s assassins) and in <em>Jeremiah 51:27</em>. Theologically, Ararat marks the new beginning of post-Flood humanity — the second Adam in Noah stepping onto dry ground under the rainbow covenant. The ark resting there is the type of every saint finally brought to safety through judgment in Christ.</p>'
    ),
    'ascension-of-christ': (
        '<p>The Ascension of Christ is the bodily ascension of the risen Jesus from the Mount of Olives forty days after the resurrection (<em>Acts 1:9-11</em>; <em>Luke 24:50-53</em>), where He was taken up into the cloud of divine glory and seated at the right hand of the Father. The Ascension is not a disappearance but an enthronement: <em>"set him at his own right hand in the heavenly places, far above all principality, and power, and might, and dominion"</em> (<em>Ephesians 1:20-22</em>). From that throne He reigns, He intercedes (<em>Hebrews 7:25</em>), and He has poured out the Spirit (<em>Acts 2:33</em>). The Ascension is therefore the present coronation of King Jesus, and the assurance that He will return the same way.</p>'
    ),
    'asherah-pole': (
        '<p>The Asherah pole (Hebrew <em>asherah</em>, rendered <em>"grove"</em> in the KJV) was the carved wooden cult-symbol of the Canaanite mother-goddess Asherah, consort of El and rival to YHWH. Often planted beside a Baal altar, it represented fertility religion at its most syncretistic. Israel was commanded repeatedly to <em>"cut down their groves"</em> (<em>Exodus 34:13</em>; <em>Deuteronomy 7:5; 16:21</em>), yet the apostate kings reinstalled them again and again. Manasseh even set one in the temple (<em>2 Kings 21:7</em>); Josiah burned it (<em>2 Kings 23:6</em>). The Asherah pole is the perpetual symbol of the church’s temptation to import goddess-spirituality into the worship of the LORD — sentimental, feminizing, fertility-mystic — and must be cut down wherever it reappears.</p>'
    ),
    'baal': (
        '<p>Baal (Hebrew "lord, owner") was the chief Canaanite storm-fertility god, perpetual rival of YHWH for Israel’s allegiance throughout the period of the judges and kings. Many local manifestations existed — Baal-Peor, Baal-Zebub, Baal-Berith — but all were one religious system: rain, fertility, prosperity worship, with cultic prostitution and sometimes child-sacrifice attached. The decisive confrontation came on Mount Carmel, where Elijah challenged 450 prophets of Baal and the LORD answered by fire (<em>1 Kings 18</em>). Baal worship is the perennial template of every prosperity-and-fertility religion that promises material blessing in exchange for compromised worship. Wherever Christians today trade covenant fidelity for "blessing-now" — financial, sexual, therapeutic — the spirit of Baal is again at work.</p>'
    ),
    'call': (
        '<p>To <em>call</em>, in Scripture, is to name, summon, or invite — but theologically the word carries the weight of God’s effectual calling of His elect to salvation, vocation, and service. There is the outward call of the gospel, which goes to all who hear (<em>Matthew 22:14</em>), and the inward effectual call by which the Spirit irresistibly draws the elect to Christ (<em>Romans 8:30</em>; <em>1 Corinthians 1:9; 7:17-24</em>). The Reformed <em>ordo salutis</em> places calling between election and regeneration: God summons His own by name, and the dead come out of the tomb. Calling also names Christian vocation — the providential placement of every believer into the work, station, and household where he serves.</p>'
    ),
    'feed-flock': (
        '<p>"Feed the flock" is the threefold charge Christ laid on Peter after the resurrection: <em>"Feed my lambs... Feed my sheep... Feed my sheep"</em> (<em>John 21:15-17</em>). Paul lays the same charge on the Ephesian elders: <em>"Take heed therefore unto yourselves, and to all the flock... to feed the church of God"</em> (<em>Acts 20:28</em>). Peter passes it on to every elder: <em>"Feed the flock of God which is among you"</em> (<em>1 Peter 5:2</em>). The primary task of the pastoral office is therefore the steady provision of spiritual food — the Word of God preached, taught, applied, and pressed home. Pastors who entertain, manage, or therapize instead of feed have abandoned their post. Sheep starve quietly.</p>'
    ),
    'footwashing': (
        '<p>Footwashing is the disciple’s ordained act of stooping in love to serve another, modeled by Christ on the night of His betrayal (<em>John 13:1-17</em>). Removing His outer garment, girding Himself with a towel, the Lord of glory washed the feet of twelve men — including the one about to betray Him — and then said: <em>"If I then, your Lord and Master, have washed your feet; ye also ought to wash one another’s feet."</em> Footwashing dramatizes the inversion at the heart of the gospel: the greatest serves the least. Some traditions practice it as ordinance; all Christians are bound by its spirit. The Christian man who will not stoop to serve his wife, his children, or his weaker brother has not yet learned what kind of King he follows.</p>'
    ),
    'hades-realm': (
        '<p>Hades (Greek), corresponding to the Hebrew <em>Sheol</em>, is the intermediate realm of the dead in New Testament usage. It is not yet the final hell (<em>Gehenna</em>) but the temporary holding-place of disembodied souls awaiting resurrection and final judgment. In Christ’s account of the rich man and Lazarus (<em>Luke 16:19-31</em>), Hades holds the rich man in conscious torment while Abraham’s bosom holds Lazarus in comfort, separated by a fixed gulf. Christ holds <em>"the keys of hell and of death"</em> (<em>Revelation 1:18</em>). At the final judgment Hades itself is emptied and then cast, with death, into the lake of fire (<em>Revelation 20:14</em>). The intermediate state ends; resurrection and final judgment do not.</p>'
    ),
    'harlot-figure': (
        '<p>The harlot is one of Scripture’s most charged figures, used to expose covenant infidelity. In the prophets she is unfaithful Israel — Hosea’s Gomer, Ezekiel’s Oholah and Oholibah (<em>Ezekiel 23</em>), Jeremiah’s adulterous bride (<em>Jeremiah 3</em>). In Revelation she becomes the great whore: <em>"that great city... arrayed in purple and scarlet... drunken with the blood of the saints"</em> (<em>Revelation 17:1-6</em>; <em>18:2-3</em>), the persecuting world-system and apostate religion fused. The harlot is the dark mirror of the Bride: both ride a beast, both are dressed in finery, both claim the world — but one ends in fire, the other in wedding. The choice between Whore and Bride is the choice the church must make every generation.</p>'
    ),
    'holy-saturday': (
        '<p>Holy Saturday is the Sabbath between Christ’s crucifixion and resurrection — the day He rested in the tomb after declaring <em>"It is finished"</em> (<em>John 19:30</em>). The Apostles’ Creed includes that day in the clause traditionally rendered <em>"descended into hell"</em> or, more carefully, <em>"descended to the dead"</em> — affirming the reality of His death and burial without affirming any post-mortem suffering on our behalf. Holy Saturday is the Christian Sabbath of waiting: the women resting from anointing, the disciples scattered, the world thinking it had won. The Reformed church marks the day soberly, neither denying its silence nor filling it with speculation. It teaches us how to wait when God seems most still.</p>'
    ),
    'homoiousion': (
        '<p>Homoiousion (Greek <em>homoiousios</em>, "of like substance") was the fourth-century semi-Arian compromise term proposed in the years after Nicaea — affirming that the Son is of <em>like</em> substance with the Father rather than the <em>same</em> substance. The single Greek letter <em>iota</em> separated it from the Nicene <em>homoousion</em> ("of the same substance"). Athanasius and the orthodox party rightly rejected the compromise: <em>like</em> is not <em>same</em>, and a Christ who is only similar to God cannot save. The struggle is the perpetual lesson of doctrinal precision — small words carry whole gospels, and the church that yields a single iota of Christ’s deity has yielded everything. Nicene Christology stands or falls on that letter.</p>'
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
