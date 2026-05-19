#!/usr/bin/env python3
"""Batch 31 — final 9 from 30-50 bucket + first 16 from 50-60.

Clears the 30-50 word bucket entirely and begins the next thinnest
tier of entries. Brings the session total to 775.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    # === FINAL 9 OF 30-50 BUCKET ===
    'phat': (
        '<p>"Phat" was a 1990s hip-hop variant spelling of "fat," repurposed as a positive descriptor for things judged excellent, attractive, or impressive — <em>"that beat is phat,"</em> <em>"phat sneakers."</em> The slang inverts the modern English negative valence of "fat," suggesting that abundance, fullness, and richness are good — an instinct Scripture actually shares, though anchored very differently. <em>"My cup runneth over"</em> (<em>Psalm 23:5</em>); <em>"The blessing of the LORD, it maketh rich, and he addeth no sorrow with it"</em> (<em>Proverbs 10:22</em>); <em>"Thou crownest the year with thy goodness; and thy paths drop fatness"</em> (<em>Psalm 65:11</em>). Biblical fullness is God’s blessing, not human appetite — fatness of grain, milk, oil, and the fat of His house, not gluttony of the flesh.</p>'
    ),
    'pigeon': (
        '<p>The pigeon, in Scripture, is the small domesticated dove and the appointed sacrifice permitted to the poor who could not afford a lamb. The Mosaic law made specific accommodation: <em>"And if she be not able to bring a lamb, then she shall bring two turtles, or two young pigeons; the one for the burnt offering, and the other for a sin offering"</em> (<em>Leviticus 12:8</em>). When Joseph and Mary brought the infant Christ to the temple for the purification, they offered <em>"a pair of turtledoves, or two young pigeons"</em> (<em>Luke 2:24</em>) — Luke’s quiet declaration that the King of Glory was born into poverty, into a household that could not afford the lamb, that He might Himself be the Lamb who saves the poor.</p>'
    ),
    'seek-his-face': (
        '<p>"Seek His face" names the pursuit of God’s manifest <em>presence</em> rather than merely His benefits. To seek His face (Hebrew <em>panim</em>) is to seek personal nearness with the <em>Person</em>, not transactional access to power or gifts. <em>"When thou saidst, Seek ye my face; my heart said unto thee, Thy face, LORD, will I seek"</em> (<em>Psalm 27:8</em>); <em>"Seek the LORD, and his strength: seek his face evermore"</em> (<em>1 Chronicles 16:11</em>; <em>Psalm 105:4</em>). The Aaronic blessing prays: <em>"The LORD make his face shine upon thee, and be gracious unto thee"</em> (<em>Numbers 6:25</em>); the saint reciprocates by seeking the face that shines. Christians who have learned to want only what God gives are still infants; the mature want <em>Him</em>.</p>'
    ),
    'sodom': (
        '<p>Sodom was the Canaanite city of the Jordan plain destroyed in <em>Genesis 19</em> by fire and brimstone rained from heaven, alongside Gomorrah. Its sin was a multifold collapse — pride, idleness, fulness of bread, neglect of the poor, and the specific homosexual assault on Lot’s angel-guests at the gate (<em>Ezekiel 16:49-50</em>; <em>Genesis 19:4-9</em>). In Scripture the name becomes the fixed reference point for sexual depravity, civic pride, and divine judgment. Christ Himself names Sodom multiple times as a comparative measure for cities of greater gospel privilege: <em>"It shall be more tolerable for the land of Sodom in the day of judgment, than for thee"</em> (<em>Matthew 11:24</em>). Peter and Jude both invoke Sodom as warning to apostate communities (<em>2 Peter 2:6</em>; <em>Jude 7</em>).</p>'
    ),
    'stranger-welcome': (
        '<p>"Stranger welcome" is the Christian household’s practiced obedience to the command, repeated through both Testaments, to receive the foreigner, the traveler, and the unknown guest as if receiving the Lord Himself. The Mosaic law was emphatic: <em>"The stranger that dwelleth with you shall be unto you as one born among you, and thou shalt love him as thyself; for ye were strangers in the land of Egypt"</em> (<em>Leviticus 19:34</em>). Christ extends it: <em>"I was a stranger, and ye took me in"</em> (<em>Matthew 25:35</em>). Hebrews warns and promises: <em>"Be not forgetful to entertain strangers: for thereby some have entertained angels unawares"</em> (<em>Hebrews 13:2</em>). It is hospitality with sharper edges — not just to friends, but to those with no claim on us.</p>'
    ),
    'tomb': (
        '<p>The tomb is a sepulcher hewn in rock or built of stone for the dead — and in Scripture it serves both as evidence of sin’s curse and as the stage of the Resurrection. Christ’s denunciation of the Pharisees turned on the metaphor: <em>"Ye are like unto whited sepulchres, which indeed appear beautiful outward, but are within full of dead men’s bones, and of all uncleanness"</em> (<em>Matthew 23:27</em>) — whitened tombs hid decay under their paint. Joseph of Arimathea’s new tomb hewn in rock (<em>Matthew 27:60</em>) held the Lord of Glory three days and could not keep Him: <em>"He is not here: for he is risen, as he said"</em> (<em>Matthew 28:6</em>). The tomb is the great mocked enemy — defeated, opened, emptied, awaiting the final resurrection of every believer.</p>'
    ),
    'valor-biblical': (
        '<p>Biblical valor is strength-of-worth proven in real combat — the inner mettle that holds up under the test, displayed by warriors, prophets, and saints. The Hebrew <em>chayil</em> covers both military force and moral strength: a <em>"man of valor"</em> in Scripture is courageous, capable, and trustworthy in the day of pressure. Gideon, hiding from the Midianites, was greeted by the angel: <em>"The LORD is with thee, thou mighty man of valour"</em> (<em>Judges 6:12</em>). David’s mighty men were each named men of valor (<em>2 Samuel 23</em>). The Proverbs 31 wife is, in Hebrew, <em>eshet chayil</em> — "a woman of valor." Valor is not bluster; it is competence under fire, anchored in faith. Pray for it; train for it; display it when called.</p>'
    ),
    'yeshuah': (
        '<p><em>Yeshuah</em> (יְשׁוּעָה) is the Hebrew word for <em>salvation</em> — concrete and active deliverance from real enemies, real disease, real captivity, and ultimately from sin. The name <em>Joshua</em> (Hebrew <em>Yehoshua</em>, "YHWH saves") and the name <em>Jesus</em> (Greek <em>Iēsous</em>, contracted from <em>Yeshua</em>) are both built on this root. The angel told Joseph: <em>"thou shalt call his name JESUS: for he shall save his people from their sins"</em> (<em>Matthew 1:21</em>). The Psalmist sings: <em>"The LORD is my light and my salvation [yeshuah]; whom shall I fear?"</em> (<em>Psalm 27:1</em>); <em>"He only is my rock and my salvation"</em> (<em>Psalm 62:2, 6</em>). Salvation in Scripture is not abstract; it is the LORD acting to save.</p>'
    ),
    'yhwh-shammah': (
        '<p><em>YHWH-Shammah</em> (יְהוָה שָׁמָּה) — "the LORD is there" — is the covenant name Ezekiel gives the eschatological city in the closing verse of his prophecy: <em>"It was round about eighteen thousand measures: and the name of the city from that day shall be, The LORD is there"</em> (<em>Ezekiel 48:35</em>). The name does <em>not</em> mean "the LORD will visit there," or "the LORD’s name is honored there" — it means <em>the LORD is there</em>, in perpetual indwelling presence. The promise anticipates the closing vision of Scripture: <em>"And I heard a great voice out of heaven saying, Behold, the tabernacle of God is with men, and he will dwell with them, and they shall be his people, and God himself shall be with them, and be their God"</em> (<em>Revelation 21:3</em>).</p>'
    ),

    # === FIRST 16 OF 50-60 BUCKET ===
    'agape-love': (
        '<p><em>Agapē</em> is the New Testament’s great word for love — the willed, self-giving, covenant-keeping love that originates in God Himself and is poured out in the saint by the Holy Spirit (<em>Romans 5:5</em>). It is distinct from the other Greek loves: <em>erōs</em> (desire, particularly sexual), <em>philia</em> (friendly affection), and <em>storgē</em> (familial bond). <em>Agapē</em> is the love commanded toward enemies (<em>Matthew 5:44</em>), neighbors (<em>Mark 12:31</em>), God Himself (<em>Mark 12:30</em>), and the brethren (<em>John 13:34-35</em>). <em>"God so loved [ēgapēsen] the world, that he gave his only begotten Son"</em> (<em>John 3:16</em>). <em>Agapē</em> is not primarily feeling but commitment — chosen, willed, and acted upon regardless of the worthiness of its object. <em>"For greater love hath no man than this"</em> (<em>John 15:13</em>).</p>'
    ),
    'argument-from-design': (
        '<p>The Argument from Design (also called the Teleological Argument) infers the existence of an intelligent Designer from the order, complexity, and apparent purpose observed in nature. From William Paley’s 1802 <em>"watch on a heath"</em> analogy (a watch implies a watchmaker; the eye, vastly more complex, implies a Designer), to modern intelligent-design arguments (irreducible complexity, specified information in DNA), to fine-tuning arguments (the physical constants of the universe calibrated for life), the form is consistent: design implies a designer; nature shows design; therefore, a Designer. Scripture independently affirms the premise: <em>"For the invisible things of him from the creation of the world are clearly seen, being understood by the things that are made, even his eternal power and Godhead; so that they are without excuse"</em> (<em>Romans 1:20</em>).</p>'
    ),
    'beatitude-3': (
        '<p>The third Beatitude of Christ’s Sermon on the Mount is <em>"Blessed are the meek: for they shall inherit the earth"</em> (<em>Matthew 5:5</em>) — drawing directly on <em>Psalm 37:11</em>. The Greek <em>praus</em> ("meek") denotes strength under control: gentleness rooted in confidence in God, force bridled and yielded. It is not the natural temperament of timidity or doormat passivity. The same word describes the colt Christ rode triumphantly into Jerusalem (<em>Matthew 21:5</em>) and Christ Himself: <em>"I am meek and lowly in heart"</em> (<em>Matthew 11:29</em>). Moses was <em>"very meek, above all the men which were upon the face of the earth"</em> (<em>Numbers 12:3</em>) — and led a nation through forty wilderness years. The meek inherit because they have refused to seize.</p>'
    ),
    'beatitude-7': (
        '<p>The seventh Beatitude is <em>"Blessed are the peacemakers: for they shall be called the children of God"</em> (<em>Matthew 5:9</em>). The Greek <em>eirēnopoios</em> appears only here in the New Testament and carries a precise meaning: <em>peace-makers</em>, not just peace-keepers. The distinction matters. The peacemaker <em>creates</em> peace where there was none — by truth-telling, by reconciliation, by costly initiative. The peacekeeper merely avoids conflict at any cost, often through silence or compromise. Christ Himself is the great peacemaker: <em>"having made peace through the blood of his cross"</em> (<em>Colossians 1:20</em>); <em>"For he is our peace, who hath made both one"</em> (<em>Ephesians 2:14</em>). Christian men called to imitate Him are agents of real reconciliation — between sinners and God first, and among saints thereafter.</p>'
    ),
    'bow-down-worship': (
        '<p>The Hebrew word usually translated <em>worship</em> is <em>shachah</em> (שָׁחָה) — literally <em>to bow down, to prostrate oneself, to sink down</em>. Biblical worship is bodily before it is musical or verbal: knees bent, face to the ground, body lower than head. Abraham bowed to the LORD at Mamre (<em>Genesis 18:2</em>); the Magi <em>"fell down, and worshipped him"</em> (<em>Matthew 2:11</em>); the disciples <em>"came and held him by the feet, and worshipped him"</em> (<em>Matthew 28:9</em>); the elders <em>"fall down before the throne, and worship him that liveth for ever and ever"</em> (<em>Revelation 4:10</em>). The first commandment forbids bowing to other gods (<em>Exodus 20:5</em>) precisely because bowing <em>is</em> what worship physically is. Recover the body in worship. Kneel.</p>'
    ),
    'communion-saints': (
        '<p>The Communion of Saints is the fellowship that all the redeemed have with Christ and with one another by virtue of their union with Him. It crosses time (Abraham, Augustine, the present church, the future saints), geography (every tribe, tongue, people, and nation), and even the boundary of death (the church militant on earth and the church triumphant in heaven). The Apostles’ Creed confesses it. It binds gifts to be shared (<em>"the body... by that which every joint supplieth"</em>, <em>Ephesians 4:16</em>) and burdens to be borne (<em>"Bear ye one another’s burdens"</em>, <em>Galatians 6:2</em>), and finds its visible local expression in the gathered church under Word and sacrament, climaxing at the Lord’s Table where the one bread declares the one body (<em>1 Corinthians 10:16-17</em>).</p>'
    ),
    'contempt': (
        '<p>Contempt is settled disdain — the disposition that treats another as beneath notice. Scripture names it as a serious sin both vertically and horizontally. Paul charges the sinner who ignores grace: <em>"Or despisest thou the riches of his goodness and forbearance and longsuffering; not knowing that the goodness of God leadeth thee to repentance?"</em> (<em>Romans 2:4</em>). He warns Timothy against the contempt younger men sometimes show older brothers and authorities: <em>"Let no man despise thy youth"</em> (<em>1 Timothy 4:12</em>; cf. <em>Titus 2:15</em>). In marriage contempt corrodes faster than anger — researchers and Scripture agree; in worship, it grieves the Spirit. Christian men cannot afford reserves of contempt in their hearts. Every image-bearer is to be honored, even when corrected.</p>'
    ),
    'destiny': (
        '<p>Scripture replaces vague cosmic "destiny" with the personal, purposeful plan of a sovereign God. There is no impersonal fate, no astrological pull, no spirit-of-the-age determinism — only God’s decree, executed by His providence, for His glory and His people’s good. <em>"Before I formed thee in the belly I knew thee; and before thou camest forth out of the womb I sanctified thee, and I ordained thee a prophet unto the nations"</em> (<em>Jeremiah 1:5</em>). <em>"Having predestinated us unto the adoption of children by Jesus Christ to himself, according to the good pleasure of his will"</em> (<em>Ephesians 1:5</em>). Biblical destiny is not impersonal fate but the personal plan of a Father — known before the world began, executed in Christ.</p>'
    ),
    'doorkeeper': (
        '<p>A doorkeeper is the appointed gatekeeper of a household, palace, or sanctuary — the one who decides who crosses the threshold and who does not. Scripture treats the office with surprising honor. The temple gatekeepers were Levites of standing, organized in courses, named in the Chronicler’s lists (<em>1 Chronicles 9:17-27; 26:1-19</em>). The Psalmist confesses: <em>"For a day in thy courts is better than a thousand. I had rather be a doorkeeper in the house of my God, than to dwell in the tents of wickedness"</em> (<em>Psalm 84:10</em>). To stand at the door of God’s house — even just to keep watch — is greater than to feast in any palace of sin. The Christian who guards the threshold of his own house, his own church, his own heart, serves at an honored post.</p>'
    ),
    'dualism-gnostic': (
        '<p>Gnostic dualism teaches that matter is evil and spirit is good — that the material world is the prison of the soul, fashioned by a lesser god (the <em>demiurge</em>), to be escaped by hidden knowledge (<em>gnōsis</em>). Scripture rejects the whole architecture. God declared the material creation <em>"very good"</em> (<em>Genesis 1:31</em>) — including bodies, food, marriage, work, animals, and land. The incarnation — <em>"the Word was made flesh, and dwelt among us"</em> (<em>John 1:14</em>) — is the ultimate refutation: God Himself takes on matter. Bodily resurrection promises physical redemption (<em>Romans 8:23; 1 Corinthians 15</em>). Evil is not a property of matter but a corruption of the will. The Christian eats, marries, works, and worships with the body, not against it.</p>'
    ),
    'emmaus': (
        '<p>Emmaus was a small village a Sabbath-day’s journey (about seven miles) from Jerusalem — and the road to Emmaus is where one of the most beautiful resurrection-day scenes unfolds (<em>Luke 24:13-35</em>). Two disciples, Cleopas and his companion, walked the road discouraged on the very day of the Resurrection, talking together of all that had happened. The risen Christ joined them — though their eyes were holden — and beginning at Moses and all the prophets, He <em>"expounded unto them in all the scriptures the things concerning himself"</em> (<em>v. 27</em>). They constrained Him to lodge with them at evening; in the breaking of bread their eyes were opened and they knew Him. <em>"Did not our heart burn within us, while he talked with us by the way?"</em></p>'
    ),
    'felix': (
        '<p>Antonius Felix was the Roman procurator of Judea (c. AD 52-59) before whom Paul was tried after his transfer from Jerusalem to Caesarea by Claudius Lysias’s armed escort (<em>Acts 23:23-35; 24</em>). Felix was a former slave elevated under Claudius — and married to Drusilla, the Jewish princess he had lured from her first husband. He had Paul brought before him repeatedly, hoping that money would be given him to release Paul (<em>Acts 24:26</em>). When Paul reasoned <em>"of righteousness, temperance, and judgment to come, Felix trembled, and answered, Go thy way for this time; when I have a convenient season, I will call for thee"</em> (<em>24:25</em>). The convenient season never came. He left Paul bound for two years to please the Jews.</p>'
    ),
    'fountain': (
        '<p>A fountain is a natural spring of water issuing from the earth — and in Scripture it becomes the figure of God Himself as the inexhaustible source of life, and of Christ’s shed blood as the fountain opened for cleansing. <em>"For with thee is the fountain of life: in thy light shall we see light"</em> (<em>Psalm 36:9</em>). Jeremiah’s great covenant indictment turns on the image: <em>"For my people have committed two evils; they have forsaken me the fountain of living waters, and hewed them out cisterns, broken cisterns, that can hold no water"</em> (<em>Jeremiah 2:13</em>). Zechariah prophesies the gospel fountain: <em>"In that day there shall be a fountain opened to the house of David... for sin and for uncleanness"</em> (<em>Zechariah 13:1</em>). William Cowper’s hymn captures it: <em>"There is a fountain filled with blood."</em></p>'
    ),
    'herodias': (
        '<p>Herodias was the granddaughter of Herod the Great — first married to Herod Philip, then taken as wife by his brother Herod Antipas in defiance of Mosaic law (<em>Leviticus 18:16; 20:21</em>). John the Baptist publicly declared the marriage unlawful: <em>"It is not lawful for thee to have thy brother’s wife"</em> (<em>Mark 6:18</em>). Herodias nursed her grudge until Antipas’s birthday banquet, when her daughter (Salome by tradition) danced before the assembled court and won the king’s rash oath to grant her whatever she asked. Prompted by her mother, she demanded John the Baptist’s head on a platter — and Antipas, ashamed before his guests, obliged (<em>Mark 6:21-29</em>). The Forerunner of the gospel died because a wife’s wounded pride wanted a prophet silenced.</p>'
    ),
    'joshua-book': (
        '<p>Joshua is the sixth book of the Bible — the first of the historical books — recounting Israel’s conquest of Canaan under Joshua, son of Nun, the successor of Moses. After the crossing of the Jordan and the fall of Jericho (chs. 1-6), the conquest unfolds in three main campaigns (central, southern, and northern, chs. 7-12), followed by the division of the land among the twelve tribes (chs. 13-22) and Joshua’s farewell covenant renewal at Shechem (chs. 23-24). The book demonstrates God’s faithfulness to His covenant promises: <em>"There failed not ought of any good thing which the LORD had spoken unto the house of Israel; all came to pass"</em> (<em>Joshua 21:45</em>). Joshua’s great charge stands forever: <em>"Choose you this day whom ye will serve... as for me and my house, we will serve the LORD"</em> (<em>Joshua 24:15</em>).</p>'
    ),
    'lifting-staff': (
        '<p>"Lifting the staff" is Moses’ gesture during Israel’s battle against Amalek at Rephidim (<em>Exodus 17:8-16</em>). While Joshua led the troops in the valley, Moses stood on the hilltop with the rod of God in his hand. <em>"When Moses held up his hand, that Israel prevailed: and when he let down his hand, Amalek prevailed."</em> As his hands grew heavy with fatigue, Aaron and Hur fetched a stone for him to sit upon and stayed up his hands on either side until the going down of the sun. The staff lifted, and the steady hands holding the lifter, together declare a doctrine: the LORD fights for Israel, but His people pray, and faithful brothers steady the praying man. After the victory Moses built an altar called <em>YHWH-Nissi</em> — "the LORD is my banner."</p>'
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
