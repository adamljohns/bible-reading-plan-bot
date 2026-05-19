#!/usr/bin/env python3
"""Batch 13 — expand 25 more thin entries to 90-110 words each.

Targets: OT books, NT books, priesthood/cult terms, divine names,
disciplines, and ecclesial offices from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    '1chronicles': (
        '<p>1 Chronicles retells the history of Israel from Adam through David, but from a priestly, post-exilic perspective shaped by life under Persian rule. Where Samuel records the man — flawed, repentant, beloved — Chronicles records the throne, the temple, and the Levitical orders that surround them. Long genealogies (chs. 1-9) anchor the returnees in covenant identity; the David narrative (chs. 10-29) emphasizes his preparations for temple worship, his organizing of the priestly and musical orders, and the Davidic covenant of <em>2 Samuel 7</em> retold in <em>1 Chronicles 17</em>. The book preaches that the throne of David endures forever, finally fulfilled in Christ the Son of David.</p>'
    ),
    'aaronic-priesthood': (
        '<p>The Aaronic priesthood is the Levitical priestly line descended from Aaron, set apart in <em>Exodus 28-29</em> to mediate the old covenant sacrifices, tend the lampstand, burn incense, and bless the people with the threefold benediction of <em>Numbers 6:24-26</em>. It was hereditary, male, and bound by strict purity laws — a typological priesthood pointing forward, not a permanent institution. <em>Hebrews 7</em> declares it fulfilled and surpassed by Christ in the eternal order of Melchizedek: a better priesthood, after a better order, securing a better covenant. The Aaronic ministry was the shadow; the High Priesthood of Jesus is the substance, and through Him every believer is now drawn near.</p>'
    ),
    'all-saints-day': (
        '<p>All Saints Day (November 1) is the historic Christian observance honoring the great cloud of witnesses — the faithful departed believers who have finished their race ahead of us — drawn from <em>Hebrews 11-12</em> and <em>Revelation 7:9-17</em>. It is not Catholic invocation of the dead, but Protestant remembrance of the church triumphant: martyrs, reformers, fathers, mothers, and ordinary saints whose faith fed our own. The Reformation kept the feast and stripped it of veneration. Biblical observance teaches our children that the church is older than they are, that the saints persevered through worse than we face, and that we belong to a covenant line of witnesses stretching back to Abel.</p>'
    ),
    'ancient-of-days': (
        '<p>The Ancient of Days is the title Daniel gives to God enthroned in cosmic judgment (<em>Daniel 7:9-14, 22</em>): white-haired in eternal majesty, robed in white as snow, His throne flaming fire, ten thousand times ten thousand standing before Him. The books are opened, the beasts are judged, and dominion is given to One like a Son of Man who comes on the clouds. This is the courtroom scene that frames all of Daniel and echoes through <em>Revelation 1</em>, where the risen Christ bears the same description — proving that the Son of Man <em>is</em> the Ancient of Days. Eternal Father and incarnate Son share the throne; the gavel is His.</p>'
    ),
    'apostolic-decree': (
        '<p>The Apostolic Decree is the binding decision issued by the Jerusalem Council in <em>Acts 15:19-29</em>, ruling that Gentile converts need not be circumcised or come under the Mosaic ceremonial law. They were charged to abstain from four things: food sacrificed to idols, blood, things strangled, and sexual immorality (<em>porneia</em>). The decree was no compromise but a doctrinal line — justification is by faith in Christ alone, not by works of the law — paired with practical fellowship requirements that protected table communion between Jewish and Gentile believers. Written, sealed, and circulated by Paul and Silas (<em>Acts 15:30; 16:4</em>), it remains the pattern for how the church settles doctrine: in council, by Scripture, under apostolic authority.</p>'
    ),
    'avenger-blood': (
        '<p>The avenger of blood (<em>goʼel ha-dam</em>) was the nearest male kinsman of a slain person, charged under Mosaic law with executing justice on the killer (<em>Numbers 35:19-27</em>; <em>Deuteronomy 19:6-13</em>). This was not vendetta but ordered patriarchal justice, bounded by the six cities of refuge, the requirement of two witnesses, and the distinction between murder and manslaughter. The office honored two truths feminism cannot hold together: human life is sacred, and men bear the burden of enforcing that sacredness with the sword. Christ, our true Goel, both fulfills the office and ends private vengeance — the avenger of blood is now the magistrate (<em>Romans 13:4</em>), and the kinsman-redeemer is our risen Lord.</p>'
    ),
    'bashan': (
        '<p>Bashan was the fertile, well-watered tableland east of the Sea of Galilee, famous in Scripture for its strong cattle (<em>Psalm 22:12</em>; <em>Amos 4:1</em>) and great oaks (<em>Isaiah 2:13</em>). It belonged originally to Og, the last of the Rephaim — a giant whose iron bedstead measured nine cubits (<em>Deuteronomy 3:11</em>) — and was conquered under Moses (<em>Numbers 21:33-35</em>) and given to half-Manasseh. In the prophets Bashan symbolizes worldly strength brought low under God’s judgment, and in <em>Psalm 68:15-22</em> it becomes the stage on which the LORD ascends in triumph, leading captivity captive — the very passage Paul applies to the ascended Christ in <em>Ephesians 4:8</em>.</p>'
    ),
    'beast-of-revelation': (
        '<p>The two beasts of <em>Revelation 13</em> together form the satanic counterfeit of Christ and His church. The first beast rises from the sea — political and imperial blasphemy, drawing on the four beasts of <em>Daniel 7</em>, with seven heads and ten horns. The second rises from the earth, with two horns like a lamb and a dragon’s voice — religious deception serving the political beast, performing signs, demanding the mark, enforcing worship. Together they wage war on the saints for an appointed season. Historic Protestant interpreters identified the system in Rome’s persecuting power and papacy; futurist readers see a final escalation. Either way, the Lamb wins (<em>Revelation 17:14</em>), and faithful endurance is the church’s charge.</p>'
    ),
    'benediction': (
        '<p>A benediction is the authoritative pronouncement of God’s favor and peace upon His covenant people. It is not a wish, a hope, or a polite farewell — it is a word spoken under God’s authority that actually conveys what it declares. The Aaronic blessing of <em>Numbers 6:24-26</em> (<em>"The LORD bless thee and keep thee..."</em>) and the apostolic benediction of <em>2 Corinthians 13:14</em> (grace, love, communion) are the canonical patterns. In a Reformed service the pastor lifts his hands and speaks the blessing over the congregation; in the home a Christian father may rightly bless his wife and children. Benediction is a masculine office: the priest, pastor, and father pronouncing peace upon those under their charge.</p>'
    ),
    'call-to-worship': (
        '<p>The Call to Worship is the opening element of formal Christian worship, in which the minister summons the gathered congregation into the presence of God on the basis of God’s own command and invitation. Typical Scriptures include <em>Psalm 95:6</em> (<em>"O come, let us worship and bow down"</em>), <em>Psalm 100:1-2</em>, and <em>Psalm 96:7-9</em>. The Call grounds worship in God’s initiative rather than ours: He summons, we respond. It establishes posture — reverent, glad, expectant — and tells the saints why we have come. In the Regulative-Principle tradition, the Call to Worship marks the formal beginning of the covenant assembly under the ministry of an ordained man.</p>'
    ),
    'continence': (
        '<p>Continence is the Spirit-wrought self-restraint of bodily desires, especially sexual ones. Paul speaks of it directly in <em>1 Corinthians 7:9</em>: <em>"if they cannot contain, let them marry: for it is better to marry than to burn."</em> In the KJV, the word translated <em>temperance</em> in the fruit of the Spirit (<em>Galatians 5:23</em>) is the same Greek <em>egkrateia</em> — mastery of self. Continence is not repression or sexlessness; it is the discipline that orders desire toward its covenant end (marriage) and refuses to be ruled by appetite. The man who cannot govern his own body cannot govern a household or a church (<em>1 Timothy 3:2-5</em>). Continence is foundational masculine virtue.</p>'
    ),
    'crucifying-flesh': (
        '<p>Crucifying the flesh is the active, daily discipline of putting indwelling sinful desires to death by the Spirit (<em>Romans 8:13</em>; <em>Galatians 5:24</em>; <em>Colossians 3:5</em>). It is not managing the flesh, not negotiating with it, not finding balance — it is execution. Paul’s verbs are violent: <em>mortify</em>, <em>put off</em>, <em>crucify</em>. The cross is not a metaphor here; it is the actual instrument by which Christ’s death is applied to indwelling sin in every member. John Owen warned: <em>"Be killing sin or it will be killing you."</em> The Christian man wages this war by Scripture, prayer, accountability, and fasting — and he wages it daily, because the flesh that survives until evening will rise again at dawn.</p>'
    ),
    'cyprus': (
        '<p>Cyprus is the large eastern Mediterranean island that served as the launching point of Gentile mission. It was the homeland of Barnabas the Levite (<em>Acts 4:36</em>), where Hellenistic Jews scattered by the Stephen persecution first preached to Greeks (<em>Acts 11:19-20</em>), and the first stop on Paul’s first missionary journey (<em>Acts 13:4-12</em>). It was on Cyprus that Saul became <em>Paul</em>, that the magician Bar-Jesus was struck blind, and that the proconsul Sergius Paulus believed — the first recorded conversion of a Roman official. The island thus marks the transition point where the gospel left Jewish soil and stepped onto Gentile imperial ground for the first sustained advance.</p>'
    ),
    'discerning-spirits': (
        '<p>Discerning of spirits (<em>diakriseis pneumatōn</em>) is the spiritual gift listed by Paul in <em>1 Corinthians 12:10</em> for distinguishing true from false spiritual influence in the assembly. It is the necessary counterpart to prophecy, tongues, and teaching — the church must test the spirits because not every spirit is from God (<em>1 John 4:1</em>). Discernment operates by Scripture as its sole rule (does the spirit confess Christ come in the flesh?), but it also includes a Spirit-given sensitivity to detect demonic counterfeit, fleshly self-deception, and false teaching dressed in pious language. In our age of seducing spirits and doctrines of devils (<em>1 Timothy 4:1</em>), the church desperately needs men gifted in this office and willing to use it.</p>'
    ),
    'discipling-pattern': (
        '<p>The discipling pattern is the four-generation multiplication framework Paul describes in <em>2 Timothy 2:2</em>: <em>"And the things that thou hast heard of me among many witnesses, the same commit thou to faithful men, who shall be able to teach others also."</em> Four generations are present in one verse: <strong>Paul → Timothy → faithful men → others.</strong> This is the engine of biblical discipleship — not programmatic, not feminized small groups, but ordained men reproducing themselves in younger men who will in turn reproduce. Every healthy church needs this chain visible somewhere. Where it breaks, the church ages out in one generation; where it holds, the gospel goes another thousand years.</p>'
    ),
    'doxology': (
        '<p>A doxology (Greek <em>doxa</em>, "glory," + <em>logia</em>, "word") is a brief utterance of praise that ascribes all glory, honor, and dominion to God forever. Scripture is full of them: <em>Romans 11:36</em>, <em>Ephesians 3:20-21</em>, <em>1 Timothy 1:17</em>, <em>Jude 24-25</em>, and the great heavenly doxologies of <em>Revelation 4-5</em>. The doxology seals prayers, sermons, and epistles with a verbal <em>Amen</em> of worship; in the Reformed liturgical tradition the Trinitarian doxology (<em>"Praise God from whom all blessings flow..."</em>) is sung at the close of worship. A doxology is not filler; it is the heart of redeemed speech, the right way to end any sentence about God.</p>'
    ),
    'el-emet': (
        '<p><em>El-Emet</em> (אֵל אֱמֶת) — "God of Truth" — is the divine name David invokes in <em>Psalm 31:5</em>: <em>"Into thine hand I commit my spirit: thou hast redeemed me, O LORD God of truth."</em> These are also the words Christ took on His own lips at Calvary (<em>Luke 23:46</em>). The name names God as the LORD who is Truth itself — whose every word is faithful, whose covenant cannot fail, whose promises do not return void. He is not merely truthful; He is Truth. In an age of doctored news, gaslit institutions, and pronouns, the saints find their footing here: the God of Truth keeps the spirits of those who commit themselves to Him.</p>'
    ),
    'el-tsaddik': (
        '<p><em>El-Tsaddik</em> (אֵל צַדִּיק) — "the Righteous God" — is the name Isaiah declares in <em>Isaiah 45:21</em>: <em>"there is no God else beside me; a just God and a Saviour; there is none beside me."</em> The name binds two truths the modern mind tries to separate: God is righteous in all His ways (<em>Psalm 145:17</em>), and that same righteous God is the only Savior. He does not save by overlooking sin; He saves by satisfying His own righteousness at the cross of Christ. Salvation that is not also justice is sentimentality; justice that is not also salvation is hell. <em>El-Tsaddik</em> is both — and there is no other.</p>'
    ),
    'endurance-saints': (
        '<p>The endurance of the saints (Greek <em>hupomonē tōn hagiōn</em>, <em>Revelation 13:10; 14:12</em>) is the Spirit-wrought capacity to remain under affliction, temptation, and tribulation without abandoning Christ. It is not stoic resignation, not gritted teeth, not white-knuckle religion — it is loving loyalty that bears up under load because hope has already anchored the soul (<em>Hebrews 6:19</em>). Endurance is the proof of regeneration: <em>"he that shall endure unto the end, the same shall be saved"</em> (<em>Matthew 24:13</em>). The Reformed doctrine of perseverance is the same coin from God’s side. He keeps us, and so we keep going — through martyrdom, exile, betrayal, sickness, slander, and the long ordinary years.</p>'
    ),
    'follow': (
        '<p>To <em>follow</em>, in the Gospels, is Christ’s defining call to discipleship. The Greek <em>akoloutheō</em> implies far more than going behind: it is sustained accompaniment, walking the master’s road, sharing his fate. Jesus calls fishermen, a tax collector, and a rich young ruler with the same two words: <em>"Follow me"</em> (<em>Matthew 4:19; 9:9; 19:21</em>). Some leave their nets; some go away grieved. Following is not admiration from a distance — it is forsaking, taking up the cross daily, and going where He goes (<em>Luke 9:23</em>). Every other identity (occupation, family, nation) is reordered under that call. A man who will not follow Christ has not yet met Him.</p>'
    ),
    'goel': (
        '<p>The <em>goʼel</em> is the Old Testament office of kinsman-redeemer — the near relative whose covenant duty was to recover what his family had lost. He bought back forfeited land (<em>Leviticus 25:25</em>), married a brother’s childless widow to raise up seed (<em>Deuteronomy 25:5-10</em>), and avenged a slain kinsman (<em>Numbers 35:19</em>). The book of Ruth turns on this office: Boaz acts as <em>goel</em> for Naomi’s line and brings Ruth the Moabitess into the Davidic genealogy. The whole institution is typological — Jesus Christ is the true Kinsman-Redeemer, taking on our flesh (<em>Hebrews 2:14</em>) precisely so He could buy back what we had lost, marry the bride, and avenge her blood.</p>'
    ),
    'hebrews': (
        '<p>The Epistle to the Hebrews is the anonymous New Testament letter — likely written before AD 70 — addressed to Hebrew-Christian readers wavering under persecution and tempted to retreat into the safety of the synagogue. The author’s sustained argument is the superiority of Christ: better than the angels (chs. 1-2), better than Moses (ch. 3), better than Joshua’s rest (ch. 4), better than the Aaronic priesthood (chs. 5-7), better than the old covenant (chs. 8-10), worthy of a better faith and a better endurance (chs. 11-13). The book climaxes in the great cloud of witnesses and the call to run the race looking unto Jesus. Read it whenever you are tempted to go back.</p>'
    ),
    'high-place': (
        '<p>A high place (Hebrew <em>bamah</em>) was an elevated cultic shrine — often on a hilltop, with altar, pillar, and Asherah pole — used by the Canaanites for fertility worship and tolerated, even adopted, by Israel after the conquest. Solomon worshipped at Gibeon’s high place before the temple was built (<em>1 Kings 3:4</em>), but after the temple every high place was forbidden. The faithful kings (Hezekiah in <em>2 Kings 18:4</em>, Josiah in <em>2 Kings 23:8-9</em>) tore them down; the wicked kings rebuilt them. The pattern is permanent: every generation of God’s people inherits high places — household idolatries, syncretistic compromises, "respectable" alternative altars — and is called to pull them down.</p>'
    ),
    'holy-one-israel': (
        '<p>The Holy One of Israel (Hebrew <em>Qadosh Yisraʾel</em>) is the covenant name Isaiah uses more than two dozen times, joining absolute holiness to particular relationship. He is utterly other — <em>"high and lifted up,"</em> <em>"Holy, holy, holy"</em> (<em>Isaiah 6:1-3</em>) — and yet bound by covenant to <em>this</em> people, this nation, this elect bride. The name refuses the modern false choice between a transcendent God who is distant and a relational God who is soft. Israel’s LORD is the consuming fire who has also pledged Himself by oath. The Holy One sanctifies what He claims — which is why <em>1 Peter 1:15-16</em> applies the same call to the New Covenant church: <em>"Be ye holy; for I am holy."</em></p>'
    ),
    'jerusalem-council': (
        '<p>The Jerusalem Council (<em>Acts 15</em>, c. AD 49) was the first apostolic council, gathered to settle whether Gentile converts must be circumcised and keep the Mosaic ceremonial law. After sharp debate, Peter testified to God’s work among the Gentiles (<em>Acts 15:7-11</em>), Paul and Barnabas reported the signs done through them, and James (the Lord’s brother) issued the binding judgment from <em>Amos 9:11-12</em>: Gentiles are not under the yoke of Moses, but must abstain from idol-food, blood, things strangled, and porneia. The decree was written, sealed, and circulated (<em>Acts 16:4</em>). It is the foundational pattern for ecclesial decision-making: in council, by Scripture, under recognized authority — the model every Reformed and confessional church still follows.</p>'
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
