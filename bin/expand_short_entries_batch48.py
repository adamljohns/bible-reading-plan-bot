#!/usr/bin/env python3
"""Batch 48 — expand 25 more entries from the 60-70 word bucket.

Brings the session total to 1,200 entries.

Targets: theologians (Van Til), OT figures, apostles, hermeneutics,
sacraments, doctrines, NT geography, and prophetic imagery.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'sluggard': (
        '<p>The sluggard is Proverbs’ recurring antagonist — the chronically lazy man whose laziness has hardened into character. Proverbs catalogues his habits with biting wit. He loves sleep: <em>"How long wilt thou sleep, O sluggard? when wilt thou arise out of thy sleep?"</em> (<em>6:9</em>). He turns on his bed as a door on its hinges: <em>"As the door turneth upon his hinges, so doth the slothful upon his bed"</em> (<em>26:14</em>). His vineyard is overgrown with thorns and nettles (<em>24:30-31</em>). His hand is too heavy to bring back to his mouth (<em>26:15</em>). He invents excuses about lions in the streets (<em>26:13</em>). The remedy is the ant (<em>6:6-11</em>) — small, diligent, and unsupervised. Christian men should fear the slow drift toward sluggard.</p>'
    ),
    'solomon-wisdom': (
        '<p>Solomon’s wisdom is the God-given <em>chokmah</em> granted to Solomon at his accession when, given a blank check by the LORD, he asked for an understanding heart to judge the people rather than long life, wealth, or victory (<em>1 Kings 3:5-14</em>). The LORD gave him both his request and everything he had not asked. The wisdom manifested in his judicial discernment (the two mothers and the baby, <em>3:16-28</em>), encyclopedic knowledge of plants and animals (<em>4:33</em>), 3,000 proverbs and 1,005 songs (<em>4:32</em>), and the Queen of Sheba’s testimony: <em>"the half was not told me: thy wisdom and prosperity exceedeth the fame which I heard"</em> (<em>10:7</em>). His tragedy was the failure to keep his own wisdom — his foreign wives turned his heart.</p>'
    ),
    'tearing-clothes': (
        '<p>Tearing the clothes is the unmistakable Old Testament sign of mourning, repentance, or holy alarm — a deliberate, public, irreversible gesture (the garment was actually ripped). Reuben tore his clothes when he found Joseph gone from the pit (<em>Genesis 37:29</em>); Jacob tore his at the report of Joseph’s death (<em>37:34</em>); Job tore his at the word of his children’s deaths (<em>Job 1:20</em>); David tore his at the news of Saul and Jonathan (<em>2 Samuel 1:11</em>); Ezra tore his at the report of mixed marriages (<em>Ezra 9:3</em>); Mordecai tore his at Haman’s decree (<em>Esther 4:1</em>); the high priest tore his at Christ’s claim — a Levitical violation by then (<em>Matthew 26:65</em>). The body announces grief.</p>'
    ),
    'titus-figure': (
        '<p>Titus was Paul’s Greek (uncircumcised) co-worker — a test case in the Gentile-mission controversy, since Paul refused to compel his circumcision even at the Jerusalem Council (<em>Galatians 2:1-3</em>). Titus served repeatedly as the apostle’s delegate to the difficult Corinthian church, carrying letters and reports back and forth across the Aegean (<em>2 Corinthians 7:6, 13-15; 8:6, 16-24</em>). Paul finally left him in Crete <em>"to set in order the things that are wanting, and ordain elders in every city, as I had appointed thee"</em> (<em>Titus 1:5</em>). The pastoral letter that bears his name was sent to instruct him in this work. Titus is the model of the field-tested deputy whom the apostle could trust with the hardest cases.</p>'
    ),
    'van-til': (
        '<p>Cornelius Van Til (1895-1987) was the Dutch-American Reformed theologian who taught apologetics at Westminster Theological Seminary in Philadelphia for forty-three years (1929-1972). He developed <em>presuppositional</em> apologetics, arguing that no neutral common ground exists between believer and unbeliever — both interpret all data from prior philosophical commitments — and that the Christian apologist must therefore expose the impossibility of the contrary by showing how non-Christian worldviews cannot account for logic, science, ethics, or meaning on their own terms. Major works: <em>The Defense of the Faith</em>, <em>A Christian Theory of Knowledge</em>, <em>Christian Apologetics</em>. His method was popularized after his death by Greg Bahnsen and John Frame, and continues to shape Reformed engagement with secularism.</p>'
    ),
    'vexation-biblical': (
        '<p>Vexation, in Scripture, is the shaking, grinding, or tormenting of the soul by trouble. Solomon uses it as a refrain in Ecclesiastes — <em>"vanity and vexation of spirit"</em> (<em>1:14, 17; 2:11, 17, 26; 4:4, 6, 16; 6:9</em>) — to name the grinding emptiness of life lived under the sun without God. It is also the inward distress Lot felt in Sodom: <em>"vexed his righteous soul from day to day with their unlawful deeds"</em> (<em>2 Peter 2:7-8</em>). The Lord allowed Paul a thorn in the flesh <em>"to vex me"</em> in some sense — though He answered the prayer with grace, not removal (<em>2 Corinthians 12:7-9</em>). Vexation in Scripture is not always sinful: a righteous soul is rightly vexed by surrounding wickedness.</p>'
    ),
    'vine-of-israel': (
        '<p>The Vine of Israel is the recurring prophetic image of Israel as the vine YHWH planted, tended, and grew — with judgment-oracles when the vine produced wild grapes, and comfort-oracles when the vine was restored. <em>Isaiah 5:1-7</em> is the classic judgment text: <em>"For the vineyard of the LORD of hosts is the house of Israel... and he looked for judgment, but behold oppression; for righteousness, but behold a cry."</em> <em>Hosea 14:7</em> and <em>Psalm 80:8-19</em> give the restoration. Christ takes up the imagery directly and dramatically: <em>"I am the true vine, and my Father is the husbandman"</em> (<em>John 15:1</em>). The vine has at last produced the fruit it was planted to produce — but now the true vine is Christ, and Israel is His.</p>'
    ),
    'winepress': (
        '<p>The winepress is the hewn pit where grapes were trodden underfoot to release juice for wine — a normal feature of every vineyard (<em>"And he fenced it, and gathered out the stones thereof, and planted it with the choicest vine, and built a tower in the midst of it, and also made a winepress therein"</em>, <em>Isaiah 5:2</em>). And it is Scripture’s most graphic figure for divine wrath. <em>Isaiah 63:1-6</em> portrays the LORD with garments stained red from treading the winepress alone. <em>Revelation 14:19-20</em> and <em>19:15</em> describe the great winepress of the wrath of God where Christ Himself treads the nations: <em>"He treadeth the winepress of the fierceness and wrath of Almighty God."</em> Grapes; or nations under judgment. Same press.</p>'
    ),
    'analogia-scripturae': (
        '<p><em>Analogia Scripturae</em> ("analogy of Scripture") is the Reformation principle that Scripture is its own best interpreter — clearer passages illuminate obscure ones; the whole Bible interprets each part. Closely related to <em>analogia fidei</em> ("analogy of faith") — the rule that no interpretation of any passage may contradict the settled, clear doctrine of Scripture as a whole. Both principles flow from the doctrine of Scripture’s unity (one Author, one mind, one consistent message) and Scripture’s perspicuity (the central things are clear). The Westminster Confession 1.9: <em>"the infallible rule of interpretation of Scripture is the Scripture itself: and therefore, when there is a question about the true and full sense of any Scripture... it must be searched and known by other places that speak more clearly."</em></p>'
    ),
    'apostles': (
        '<p>Apostles, in the strict New Testament sense, are those Christ Himself chose, commissioned, and sent with foundational church-authority — eyewitnesses of the risen Lord empowered to write Scripture and lay the church’s foundation. The original Twelve (<em>Matthew 10:2-4</em>); Matthias chosen by lot to replace Judas before Pentecost (<em>Acts 1:26</em>); Paul as one <em>"born out of due time"</em> (<em>1 Corinthians 15:8</em>) who saw the risen Christ on the Damascus road and was commissioned as <em>"the apostle of the Gentiles"</em> (<em>Romans 11:13</em>). The office is unrepeatable: <em>"built upon the foundation of the apostles and prophets, Jesus Christ himself being the chief corner stone"</em> (<em>Ephesians 2:20</em>). Foundations are laid once. The word also names broader "sent ones" (e.g., Barnabas, <em>Acts 14:14</em>).</p>'
    ),
    'archippus': (
        '<p>Archippus was a minister of the gospel in the Lycus valley — almost certainly the son of Philemon and Apphia. Paul greets the household in the opening of his letter to Philemon: <em>"And to our beloved Apphia, and Archippus our fellowsoldier, and to the church in thy house"</em> (<em>Philemon 1-2</em>). Paul closes Colossians with a direct personal charge to him: <em>"And say to Archippus, Take heed to the ministry which thou hast received in the Lord, that thou fulfil it"</em> (<em>Colossians 4:17</em>). The exhortation suggests Archippus was at risk of failing in his pastoral duty. The verse has therefore been quoted to countless wavering ministers ever since: take heed to the ministry; fulfill it.</p>'
    ),
    'babylonian-exile': (
        '<p>The Babylonian Exile was the seventy-year deportation of the southern kingdom of Judah to Babylon following the destruction of Solomon’s temple in 586 BC (with earlier deportations in 605 and 597). It was predicted in detail by Jeremiah: <em>"this whole land shall be a desolation, and an astonishment; and these nations shall serve the king of Babylon seventy years"</em> (<em>Jeremiah 25:11; cf. 29:10</em>). Daniel and Ezekiel were prophets of the exile — Daniel in the royal court, Ezekiel by the river Chebar. The exile ended in 538 BC by the decree of Cyrus the Persian, prophesied a century and a half earlier by name in <em>Isaiah 44:28-45:1</em>. The exile is the great pattern of judgment, repentance, and restoration in biblical theology.</p>'
    ),
    'blood-of-christ': (
        '<p>The Blood of Christ is the actual physical blood Christ shed at His crucifixion — and theologically it is the basis of every saving benefit the church possesses. It is the basis of <em>redemption</em>: <em>"not redeemed with corruptible things, as silver and gold... But with the precious blood of Christ, as of a lamb without blemish and without spot"</em> (<em>1 Peter 1:18-19</em>). Of <em>atonement</em>: <em>"a propitiation through faith in his blood"</em> (<em>Romans 3:25</em>). Of the <em>new covenant</em>: <em>"the blood of the everlasting covenant"</em> (<em>Hebrews 9:15; 13:20</em>). Of the <em>cleansing of conscience</em>: <em>"shall not the blood of Christ... purge your conscience from dead works to serve the living God?"</em> (<em>Hebrews 9:14</em>). Of <em>access</em> to the holiest (<em>10:19</em>). All saving good flows from this blood.</p>'
    ),
    'breaking-bread': (
        '<p>The breaking of bread is the early Christian practice of meeting in homes for a shared meal that included the Lord’s Supper — the bread broken and cup poured in remembrance of Christ’s death until He comes. <em>Acts 2:42</em> lists it as one of the four pillars of the Jerusalem church: <em>"And they continued stedfastly in the apostles’ doctrine and fellowship, and in breaking of bread, and in prayers."</em> Acts 2:46 records its daily rhythm: <em>"And they, continuing daily with one accord in the temple, and breaking bread from house to house, did eat their meat with gladness and singleness of heart."</em> The practice is also explicitly the Lord’s-Supper-meal in <em>Acts 20:7, 11</em>, <em>Luke 24:30, 35</em>, and <em>1 Corinthians 10:16</em>. Christ’s death proclaimed at every table.</p>'
    ),
    'broad-way': (
        '<p>The Broad Way is Christ’s phrase for the wide, easy, well-traveled road that leads to destruction: <em>"Enter ye in at the strait gate: for wide is the gate, and broad is the way, that leadeth to destruction, and many there be which go in thereat: Because strait is the gate, and narrow is the way, which leadeth unto life, and few there be that find it"</em> (<em>Matthew 7:13-14</em>). The broad way is found <em>by many</em>; the narrow way is found <em>by few</em>. The teaching is unambiguous and uncomfortable: the majority is not the measure. Popular religion, cultural Christianity, and consensus piety lead to destruction by default. The Christian must deliberately find and enter the narrow way — and that finding requires the Holy Spirit to draw the heart.</p>'
    ),
    'covenant-children': (
        '<p>"Covenant children" are the children of believers — treated by Scripture as heirs of the covenant promises and members of the covenant household. The Abrahamic covenant explicitly included <em>"thee, and thy seed after thee in their generations"</em> (<em>Genesis 17:7</em>); the sign of circumcision was applied to infant sons. Peter on Pentecost: <em>"For the promise is unto you, and to your children, and to all that are afar off, even as many as the Lord our God shall call"</em> (<em>Acts 2:39</em>). Paul addresses children directly within his epistles to the churches (<em>Ephesians 6:1; Colossians 3:20</em>) — treating them as part of the gathered congregation, not outside it. Reformed paedobaptists ground infant baptism on this covenant-children theology.</p>'
    ),
    'crete': (
        '<p>Crete is the large Mediterranean island south of the Aegean Sea — a Roman province in the New Testament era and the largest of the Greek islands. Paul’s ship passed Crete on the voyage to Rome and met disaster off its coast in the storm and shipwreck recorded in <em>Acts 27</em>. The opening of the Epistle to Titus implies a prior evangelistic visit: <em>"For this cause left I thee in Crete, that thou shouldest set in order the things that are wanting, and ordain elders in every city, as I had appointed thee"</em> (<em>Titus 1:5</em>). Paul also cites a Cretan poet (Epimenides): <em>"The Cretians are alway liars, evil beasts, slow bellies. This witness is true"</em> (<em>1:12-13</em>). The gospel takes hold in unflattering places.</p>'
    ),
    'destruction-temple': (
        '<p>The two historical destructions of the Jerusalem temple bracket the entire Old Testament era and announce the close of the Mosaic-covenant era. The first: <em>Solomon’s temple</em> destroyed by Nebuchadnezzar II of Babylon in 586 BC after a two-year siege (<em>2 Kings 25:8-9; 2 Chronicles 36:18-19</em>) — prophesied for centuries by Jeremiah, ending the Davidic monarchy on its earthly throne. The second: <em>Herod’s temple</em> (the second temple as renovated by Herod the Great) destroyed by Titus of Rome and the Roman tenth legion in AD 70 — prophesied by Christ in <em>Matthew 24:1-2</em> and the Olivet Discourse: <em>"There shall not be left here one stone upon another, that shall not be thrown down."</em> Christ is the true Temple (<em>John 2:19-21</em>).</p>'
    ),
    'discipleship-cost': (
        '<p>Jesus was explicit about the cost of discipleship — and unflinching. <em>"And whosoever doth not bear his cross, and come after me, cannot be my disciple"</em> (<em>Luke 14:27</em>); <em>"If any man will come after me, let him deny himself, and take up his cross daily, and follow me"</em> (<em>Luke 9:23</em>). He told potential followers to <em>count the cost</em> like a builder estimating a tower or a king reckoning his army (<em>Luke 14:28-32</em>), and warned: <em>"whosoever he be of you that forsaketh not all that he hath, he cannot be my disciple"</em> (<em>14:33</em>). Discipleship is not light commitment to optional improvement; it is total surrender to Christ. Modern Christianity often suppresses the price; Christ never did.</p>'
    ),
    'ezra-priest': (
        '<p>Ezra was a priest and scribe of the Mosaic law — descended from Aaron through Zadok and Hilkiah (<em>Ezra 7:1-5</em>) — who led the second wave of Jewish return from Babylon to Jerusalem under Persian Artaxerxes around 458 BC. The book that bears his name says of him: <em>"For Ezra had prepared his heart to seek the law of the LORD, and to do it, and to teach in Israel statutes and judgments"</em> (<em>Ezra 7:10</em>). Three movements: prepare, do, teach. He led religious reformation in the restored community, confronted the scandal of mixed marriages with pagan women (<em>Ezra 9-10</em>), and (with Nehemiah) presided at the great public reading of the law at the Water Gate (<em>Nehemiah 8</em>). Scribe of the recovered Word.</p>'
    ),
    'font': (
        '<p>A font is the basin for baptismal water in a church — the Christian descendant of the Jewish <em>mikveh</em> (ritual immersion pool) and the apostolic-era riverbank or household basin. Its placement in church architecture is significant. Traditionally placed near the church entrance, the font signifies that baptism is the entry-rite into the visible church — the threshold sacrament. Other traditions place it forward near the altar to emphasize its connection to the Word and Table. Reformed and confessional Protestants vary in font-design (small basin, larger pool, or even immersion-tank) but agree that baptism is one of the two New Covenant sacraments, instituted by Christ (<em>Matthew 28:19</em>), administered with water in the Triune name.</p>'
    ),
    'foretell': (
        '<p>To <em>foretell</em> is to declare beforehand what God will do — the predictive dimension of prophecy. It is distinct from <em>forth-telling</em> (declaring already-revealed truth, the prophet’s primary work); foretelling reveals what is yet hidden in the divine future. Scripture is rich in fulfilled foretellings: Christ’s death and resurrection (foretold in <em>Psalm 22; Isaiah 53; Daniel 9</em>), the virgin birth (<em>Isaiah 7:14</em>), Bethlehem as His birthplace (<em>Micah 5:2</em>), Cyrus by name (<em>Isaiah 44:28-45:1</em>), the destruction of Jerusalem (Christ in <em>Matthew 24:2</em>, fulfilled AD 70), the conversion of the Gentiles (<em>Isaiah 49:6</em>), and the consummation. Foretelling is the sermon’s occasional crown, not its spine. Fulfilled prophecy is one of Scripture’s strongest evidences of divine authorship.</p>'
    ),
    'head': (
        '<p>The head is the chief body part — and in Scripture, the figure of authority, source, and leadership. <em>"Christ is the head of the church"</em> (<em>Ephesians 5:23</em>); <em>"the husband is the head of the wife, even as Christ is the head of the church"</em> (<em>Ephesians 5:23</em>; cf. <em>1 Corinthians 11:3</em>); <em>"the head of Christ is God"</em> (<em>1 Corinthians 11:3</em>). The headship order is therefore traceable from God through Christ through husband to wife — not a flat egalitarian arrangement but an ordered hierarchy of love and submission. Christ’s own head bore the crown of thorns at the cross (<em>Matthew 27:29</em>), reigns now in glory (<em>"on his head were many crowns"</em>, <em>Revelation 19:12</em>), and is the source of life to every Christian (<em>Colossians 2:19</em>).</p>'
    ),
    'historical-grammatical': (
        '<p>Historical-Grammatical interpretation reads Scripture by attending closely to two indispensable contexts: (1) the <em>historical</em> situation of the human author and original audience — what was happening, what the words then meant, who was being addressed; and (2) the <em>grammatical</em> structures of the original biblical languages — Hebrew, Aramaic, Greek — including syntax, idiom, and word usage. The method is closely related to (and sometimes treated as synonymous with) <em>plain sense</em> reading. The Reformers championed it against medieval allegorizing that had loaded texts with detached spiritual meanings. Modern conservative evangelical and Reformed exegesis remains rooted in historical-grammatical method. It does not exclude theological reflection; it grounds it.</p>'
    ),
    'i-am-shepherd': (
        '<p>"I am the good shepherd" is Christ’s fourth great I-AM predicate-statement in John’s Gospel: <em>"I am the good shepherd: the good shepherd giveth his life for the sheep"</em> (<em>John 10:11</em>; cf. <em>10:14</em>). The defining mark of the <em>good</em> shepherd (as opposed to the hireling who flees when the wolf comes) is laying down His life for the sheep. The statement echoes Ezekiel’s great prophecy: <em>"And I will set up one shepherd over them, and he shall feed them, even my servant David"</em> (<em>Ezekiel 34:23</em>). Christ identifies Himself as the prophesied Davidic Shepherd-King — and adds what the prophets had not yet revealed: this Shepherd dies for the flock, and rises again to gather it.</p>'
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
