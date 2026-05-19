#!/usr/bin/env python3
"""Batch 18 — expand 25 more thin entries to 90-110 words each.

Targets: OT/NT books, kings, geography, biblical leadership terms,
soteriology, and contested doctrines (Reformed-corrective) from the
30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'knit-soul': (
        '<p>"Knit soul" describes the deep covenantal bond between two saints — the model of biblical friendship. <em>"And it came to pass... that the soul of Jonathan was knit with the soul of David, and Jonathan loved him as his own soul"</em> (<em>1 Samuel 18:1</em>). The same Hebrew root (<em>qashar</em>) describes a binding-together — a soul-cord, a covenant tie. Jonathan made a formal covenant with David (<em>1 Samuel 18:3-4; 20:16-17; 23:18</em>), giving him his royal robe and sword. This is masculine friendship as Scripture honors it: covenantal, loyal, sacrificial, going to the wall for one another, without a hint of the eroticism modern interpreters keep trying to inject. Every Christian man needs a Jonathan; few have one.</p>'
    ),
    'mizpah': (
        '<p>Mizpah (Hebrew "watchtower") was the name of multiple elevated sites in the Old Testament — at least four — each marking a place of covenant witness or assembly. Most famously, Jacob and Laban erected the heap of stones called Mizpah as a covenant boundary witness between them: <em>"The LORD watch between me and thee, when we are absent one from another"</em> (<em>Genesis 31:49</em>). Another Mizpah in Benjamin became the gathering place where Samuel led Israel to repentance and the LORD thundered against the Philistines (<em>1 Samuel 7:5-13</em>). It was also the seat of Gedaliah’s short-lived governorship after the fall of Jerusalem (<em>Jeremiah 40-41</em>). Watchtowers were where covenant memory was kept and renewed.</p>'
    ),
    'preach': (
        '<p>To <em>preach</em>, biblically, is to herald publicly — specifically, to proclaim the gospel of Jesus Christ. The Greek <em>kērussō</em> evokes the imperial herald who announces the king’s decree on the king’s authority, not his own opinion. Christian preaching is heralding the King’s good news: <em>"Preach the word; be instant in season, out of season; reprove, rebuke, exhort with all longsuffering and doctrine"</em> (<em>2 Timothy 4:2</em>). Paul rebukes any other approach: <em>"For Christ sent me... to preach the gospel: not with wisdom of words, lest the cross of Christ should be made of none effect"</em> (<em>1 Corinthians 1:17</em>). The preacher is not therapist, comedian, or coach; he is a herald. The age that has forgotten the difference is starving its souls.</p>'
    ),
    'shepherd-leadership': (
        '<p>Shepherd leadership is Christ’s pattern: feeding the flock, knowing the sheep by name, going before them, laying down His life for them. <em>"I am the good shepherd: the good shepherd giveth his life for the sheep"</em> (<em>John 10:11</em>). Peter applies the pattern directly to elders: <em>"Feed the flock of God which is among you, taking the oversight thereof, not by constraint, but willingly; not for filthy lucre, but of a ready mind; neither as being lords over God’s heritage, but being ensamples to the flock"</em> (<em>1 Peter 5:2-3</em>). Christ contrasts it sharply with the hireling, who flees when wolves come (<em>John 10:12-14</em>). Pastors are not CEOs, life-coaches, or brand-managers — they are shepherds. The difference is everything.</p>'
    ),
    'undefiled': (
        '<p>Undefiled is the biblical word for what is pure, unstained, free from ceremonial or moral pollution. Christ Himself is undefiled: <em>"holy, harmless, undefiled, separate from sinners"</em> (<em>Hebrews 7:26</em>). The believer’s inheritance is undefiled: <em>"reserved in heaven for you"</em> (<em>1 Peter 1:4</em>). True religion is undefiled: <em>"to visit the fatherless and widows in their affliction, and to keep himself unspotted from the world"</em> (<em>James 1:27</em>). The marriage bed is to be kept undefiled: <em>"Marriage is honourable in all, and the bed undefiled: but whoremongers and adulterers God will judge"</em> (<em>Hebrews 13:4</em>). What God calls undefiled the world calls prudish; the church must learn again to call it holy.</p>'
    ),
    'weakness': (
        '<p>Weakness is the state Paul learned to glory in — not endorsed sin or moral failure, but the human limitation that drives a man to depend on Christ. Faced with the thorn in the flesh and prayed for its removal three times, Paul heard: <em>"My grace is sufficient for thee: for my strength is made perfect in weakness"</em> (<em>2 Corinthians 12:9-10</em>). Paul concluded: <em>"Most gladly therefore will I rather glory in my infirmities, that the power of Christ may rest upon me... for when I am weak, then am I strong."</em> This is not the world’s weakness-cult, not therapy-culture victimhood, not learned helplessness — it is honest acknowledgment of finitude that opens the door to divine strength. The strong man who admits weakness is the strong man God uses.</p>'
    ),
    'youthful': (
        '<p>Youthful, in Scripture, names what pertains to youth — used both joyfully and warningly. Joyfully: <em>"Rejoice, O young man, in thy youth; and let thy heart cheer thee in the days of thy youth"</em> (<em>Ecclesiastes 11:9</em>); <em>"Remember now thy Creator in the days of thy youth"</em> (<em>Ecclesiastes 12:1</em>). Warningly: <em>"Flee also youthful lusts: but follow righteousness, faith, charity, peace"</em> (<em>2 Timothy 2:22</em>). Youth is the season of strength to be devoted, not wasted; of fire to be kindled toward God, not toward fleshly appetite. The Christian young man takes the long view: he runs his strongest years toward the kingdom, marries early, serves hard, learns Scripture, and refuses the cultural script that postpones manhood until it has been spoiled.</p>'
    ),
    'zedekiah': (
        '<p>Zedekiah was the last king of Judah (c. 597-586 BC), placed on the throne by Nebuchadnezzar as a vassal after Jehoiachin was deported. Originally named Mattaniah, he was Josiah’s third son and Jehoiachin’s uncle. Weak-willed, he listened to false prophets, ignored Jeremiah’s warnings, and broke his oath of allegiance to Babylon (<em>2 Chronicles 36:13</em>; <em>Ezekiel 17:11-21</em>). Nebuchadnezzar besieged Jerusalem for two years, breached the walls, captured Zedekiah fleeing toward Jericho, slaughtered his sons before his eyes — and then put out those eyes (<em>2 Kings 25:1-7</em>; <em>Jeremiah 39:1-7; 52</em>). He was led blind to Babylon to die in prison. His reign is the cautionary close of the Davidic kingdom until the true Son of David comes.</p>'
    ),
    '1kings': (
        '<p>1 Kings opens with the death of David and the glorious accession of Solomon — his prayer for wisdom, his construction of the temple in seven years (chs. 1-11), and the visit of the Queen of Sheba — before chronicling Solomon’s late apostasy and the tragic division of the kingdom under his son Rehoboam (ch. 12). Israel (the northern ten tribes) and Judah (the southern two) begin their separate downward trajectories. The second half of the book (chs. 17-22) introduces the great prophetic ministries of Elijah — confronting the apostate house of Ahab and Jezebel, calling down fire on Mount Carmel (<em>1 Kings 18</em>), hearing the still small voice at Horeb (<em>1 Kings 19</em>). Kings rise and fall; the prophets of the LORD continue to speak.</p>'
    ),
    '2chronicles': (
        '<p>2 Chronicles narrates the temple-building of Solomon (chs. 1-9) and the subsequent reigns of the kings of Judah only — silent on the northern kingdom except where it touches the south — through to the Babylonian destruction and the closing decree of Cyrus authorizing the return (<em>2 Chronicles 36:22-23</em>). Where Kings reads as covenant-prosecution, Chronicles reads as temple-history: the priestly perspective, the Davidic line preserved, the worship pattern emphasized, the great revivals of Hezekiah (chs. 29-32) and Josiah (chs. 34-35) given full attention. The book is aimed at the returned remnant under Persian rule: <em>"Who is there among you of all his people? The LORD his God be with him, and let him go up."</em> The exile is not the end.</p>'
    ),
    'altar-incense': (
        '<p>The altar of incense was the smaller golden altar in the Holy Place — set just before the veil of the Holy of Holies — where pure compounded incense was burned morning and evening (<em>Exodus 30:1-10; 37:25-28</em>). Unlike the bronze altar of burnt offering, this altar received no animal sacrifice; its smoke was perpetual prayer. Revelation makes the typology explicit: <em>"And another angel came and stood at the altar, having a golden censer; and there was given unto him much incense, that he should offer it with the prayers of all saints upon the golden altar"</em> (<em>Revelation 8:3-4</em>). The prayers of the saints rise as the sweet smoke once did — and Christ, our High Priest, mingles them with His perfect intercession.</p>'
    ),
    'caesarea-philippi': (
        '<p>Caesarea Philippi was a northern city at the foot of Mount Hermon, near the great cave-spring of Pan — a grotto dedicated to pagan fertility worship, sometimes called <em>"the gates of hell"</em>. It was at this place of overt paganism that Jesus drew His disciples aside and asked them, <em>"Whom say ye that I am?"</em> Peter answered, <em>"Thou art the Christ, the Son of the living God"</em> — and Christ replied, <em>"upon this rock I will build my church; and the gates of hell shall not prevail against it"</em> (<em>Matthew 16:13-19</em>). The geography preaches: at the very mouth of the pagan underworld, the church is founded on the confession of Christ. The gates of hell hold no terror for a church grounded there.</p>'
    ),
    'captain-of-host': (
        '<p>The Captain of the Host of the LORD is the divine Commander who appeared to Joshua before Jericho, sword drawn (<em>Joshua 5:13-15</em>). Joshua asked, <em>"Art thou for us, or for our adversaries?"</em> The reply: <em>"Nay; but as captain of the host of the LORD am I now come."</em> Joshua fell on his face and worshipped; the Captain accepted worship (<em>"Loose thy shoe from off thy foot; for the place whereon thou standest is holy"</em>) — a theophany of the pre-incarnate Christ, the same divine Person who met Moses at the burning bush. The church does not enlist Christ in its battles; Christ enlists the church in His. He does not take sides — He takes command.</p>'
    ),
    'chorazin': (
        '<p>Chorazin was a Galilean town near Capernaum and Bethsaida — part of the gospel triangle where Jesus performed the bulk of His Galilean ministry. Many of His mighty works were done there, yet the town did not repent. Christ pronounced one of His sharpest woes upon it: <em>"Woe unto thee, Chorazin! woe unto thee, Bethsaida! for if the mighty works, which were done in you, had been done in Tyre and Sidon, they would have repented long ago in sackcloth and ashes"</em> (<em>Matthew 11:21; Luke 10:13</em>). Greater revelation means greater responsibility — and where revelation does not produce repentance, judgment is heavier than at Sodom and Tyre. The same logic still falls on every Bible-saturated culture that turns away.</p>'
    ),
    'ebal': (
        '<p>Mount Ebal stood in central Canaan opposite Mount Gerizim, with the city of Shechem nestled in the valley between. Moses commanded that, upon entering the land, six tribes stand on Ebal to pronounce the curses for breaking covenant, and six on Gerizim to pronounce the blessings (<em>Deuteronomy 11:29; 27:11-26</em>). Joshua faithfully obeyed: he built an altar of uncut stones on Ebal, offered burnt offerings, and inscribed the law of Moses on stones for all the people to read (<em>Joshua 8:30-32</em>). Ebal teaches that the covenant comes with two edges — blessing and curse — and that any nation that takes God’s name must answer to both. Christ bore the Ebal-curse for His people (<em>Galatians 3:13</em>).</p>'
    ),
    'good-news-gospel': (
        '<p>"Good news" is the plain-English equivalent of <em>euangelion</em> — the announcement that Jesus Christ, God’s eternal Son, became man, lived sinlessly, <em>"died for our sins according to the scriptures... was buried, and... rose again the third day according to the scriptures"</em>, was seen by witnesses, and now reigns at the right hand of the Father (<em>1 Corinthians 15:1-4</em>; <em>Romans 1:1-4</em>). It is news, not advice; an announcement, not a program. The news demands a response: <em>"He that believeth on the Son hath everlasting life: and he that believeth not the Son shall not see life; but the wrath of God abideth on him"</em> (<em>John 3:36</em>). Christian preaching is the public broadcast of this news to every soul that will hear.</p>'
    ),
    'heart-deceitful': (
        '<p>The deceitful heart is the native condition of every fallen man since Adam, diagnosed sharply by Jeremiah: <em>"The heart is deceitful above all things, and desperately wicked: who can know it? I the LORD search the heart, I try the reins"</em> (<em>Jeremiah 17:9-10</em>). The heart deceives both its owner and its observers — telling itself flattering stories about its own motives while hiding what really drives it. Only God searches it, and only God can cure it. The remedy is not introspection (which the heart will simply manipulate) but the regenerating work of the Holy Spirit (<em>Ezekiel 36:26-27</em>) and the searching light of Scripture (<em>Hebrews 4:12-13</em>). Christian men trust the Word over their own gut.</p>'
    ),
    'josiah': (
        '<p>Josiah was king of Judah (c. 640-609 BC), a great-grandson of Hezekiah, who became king at age eight after his wicked father Amon was assassinated. At sixteen he began to seek the LORD; at twenty he began to purge Judah of idolatry (<em>2 Chronicles 34:3</em>). The crowning moment of his reign was the rediscovery of the book of the law during temple repairs (<em>2 Kings 22:8-13</em>), which sparked national reformation: covenant renewed, high places destroyed, Passover restored (<em>2 Kings 23</em>). Of him it was said: <em>"Like unto him was there no king before him, that turned to the LORD with all his heart"</em> (<em>2 Kings 23:25</em>). He was killed in battle at Megiddo by Pharaoh Necho — and Judah’s last hope died with him.</p>'
    ),
    'judgment-day': (
        '<p>Judgment Day is the eschatological day when Christ judges the living and the dead — every man recompensed according to his deeds, every secret thing brought to light. Scripture names several aspects: the Great White Throne for the wicked (<em>Revelation 20:11-15</em>), the <em>bema</em>-seat appearance of every Christian for reward or loss (<em>2 Corinthians 5:10</em>; <em>1 Corinthians 3:11-15</em>), and the universal <em>"day of wrath and revelation of the righteous judgment of God"</em> (<em>Romans 2:5-6</em>). It is the day every conscience already anticipates. The wicked have no advocate; the believer has Christ Himself, <em>"who shall also confirm you unto the end, that ye may be blameless in the day of our Lord Jesus Christ"</em> (<em>1 Corinthians 1:8</em>). The verdict has already been signed in His blood.</p>'
    ),
    'kinsman-redeemer-doctrine': (
        '<p>The kinsman-redeemer (Hebrew <em>goʼel</em>) is the relative who, under Mosaic law, had both the right and the obligation to redeem persons or property from bondage, poverty, or alienation. He bought back lost land (<em>Leviticus 25:25</em>), married a brother’s childless widow to raise up seed (<em>Deuteronomy 25:5-10</em>), and avenged a slain kinsman (<em>Numbers 35:19-27</em>). Boaz is the great Old Testament case study: at the city gate he takes off his shoe, claims Ruth the Moabitess as his bride, and is named ancestor of David and of Christ. The whole institution is typological. <em>"Forasmuch as the children are partakers of flesh and blood, he also himself likewise took part of the same"</em> (<em>Hebrews 2:14</em>): Christ became kinsman to be Redeemer.</p>'
    ),
    'levirate': (
        '<p>Levirate marriage (from Latin <em>levir</em>, "husband’s brother") is the Mosaic provision in <em>Deuteronomy 25:5-10</em> requiring a man to marry his brother’s childless widow to raise up offspring in the dead brother’s name. The arrangement protected the widow, preserved the brother’s line, and kept inheritance within the family. Refusal carried public shame: the widow loosed his shoe and spat in his face, and his house was called <em>"the house of him that hath his shoe loosed"</em>. The institution underlies the Ruth-Boaz narrative (where Boaz acts as <em>goel</em> after a nearer kinsman declines), and the Sadducees’ trick question to Jesus about the seven brothers (<em>Matthew 22:23-33</em>). It is one of many old-covenant laws Christ fulfilled in His own redemption of the widowed bride.</p>'
    ),
    'limited-omniscience': (
        '<p>"Limited omniscience" is the open-theist proposal that God knows everything that <em>can be known</em> — but that the future free actions of creatures cannot be known by anyone, even God, because they do not yet exist. The view is associated with Clark Pinnock, Greg Boyd, and the broader open theist movement. The Reformed church rejects it as a serious departure from classical theism and biblical revelation. Scripture insists that God <em>"declar(es) the end from the beginning, and from ancient times the things that are not yet done"</em> (<em>Isaiah 46:10</em>; cf. <em>Psalm 139:4, 16</em>; <em>Acts 2:23; 4:27-28</em>). A God who does not know the future cannot promise it; a God who cannot promise the future cannot save. Classical orthodoxy stands.</p>'
    ),
    'malachi': (
        '<p>Malachi is the last book of the Old Testament — likely written around 430 BC, well after the return from exile and the rebuilding of the temple. The prophet confronts the post-exilic community’s halfhearted worship (offering blind, lame, and sick animals — <em>Malachi 1:6-14</em>), faithless priests (<em>2:1-9</em>), the scandal of broken marriages and intermarriage with pagan women (<em>2:10-16</em>), and the robbing of God in tithes and offerings (<em>3:8-12</em>). Yet the book closes in promise: <em>"the Sun of righteousness shall arise with healing in his wings"</em> (<em>4:2</em>), and Elijah will come <em>"before the coming of the great and dreadful day of the LORD"</em> (<em>4:5-6</em>). Four hundred silent years follow — then John the Baptist.</p>'
    ),
    'prevenient': (
        '<p>"Prevenient" (Latin <em>praevenire</em>, "to come before") is the Wesleyan-Arminian theological term for the grace of God that goes before conversion and enables a free human response to the gospel. Universal in scope, resistible by design, it is offered to every sinner and may be received or rejected. The Reformed reject the construct as insufficient to the biblical data. Scripture teaches an <em>effectual</em> call — the inward, sovereign, irresistible drawing of the elect to Christ: <em>"All that the Father giveth me shall come to me"</em> (<em>John 6:37</em>); <em>"whom he called, them he also justified"</em> (<em>Romans 8:30</em>). Prevenient grace makes salvation possible; effectual grace makes salvation actual. The difference is who gets the final glory — and Scripture gives it to God alone.</p>'
    ),
    'psalm-1': (
        '<p>Psalm 1 is the opening psalm and the doorway into the whole Psalter — contrasting the blessed man with the ungodly in six tight verses. The blessed man does not walk in the counsel of the ungodly, does not stand in the way of sinners, does not sit in the seat of the scornful (<em>v. 1</em>) — but <em>"his delight is in the law of the LORD; and in his law doth he meditate day and night"</em> (<em>v. 2</em>). He is like a tree planted by the rivers of water (<em>v. 3</em>). The ungodly are not so, but are like the chaff which the wind drives away (<em>v. 4</em>). Two ways, two ends, one verdict. Psalm 1 is the lens through which to read every psalm.</p>'
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
