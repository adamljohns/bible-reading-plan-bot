#!/usr/bin/env python3
"""Batch 55 — Names section polish (25 entries from the 50-70w bucket).

High-leverage target: the Names page is one of the most-trafficked
browsing surfaces. Pushing its thinnest entries to the 90+ "deep" tier.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'miletus': (
        '<p>Miletus was an Ionian seaport on the western coast of Asia Minor, about thirty miles south of Ephesus. On Paul’s final voyage to Jerusalem, he bypassed Ephesus to save time but summoned the elders of the Ephesian church to meet him at Miletus — and there delivered his most personal farewell charge in the New Testament: <em>"Ye know, from the first day that I came into Asia, after what manner I have been with you at all seasons... I have shewed you all things, how that so labouring ye ought to support the weak"</em> (<em>Acts 20:17-38</em>). He warned of grievous wolves who would enter in among them after his departure. They knelt down on the shore and prayed; they wept and embraced him, sorrowing that they should see his face no more. Later, Paul left Trophimus sick at Miletum (<em>2 Timothy 4:20</em>).</p>'
    ),
    'melchizedek-figure': (
        '<p>Melchizedek was the mysterious king-priest of Salem (early Jerusalem) who appeared to Abraham after his rescue of Lot from the kings of the East. <em>"And Melchizedek king of Salem brought forth bread and wine: and he was the priest of the most high God. And he blessed him... And he gave him tithes of all"</em> (<em>Genesis 14:18-20</em>). The text gives him no genealogy, no death-date, no successor. <em>Psalm 110:4</em> prophesies a coming king-priest <em>"after the order of Melchizedek"</em> — quoted seven times in Hebrews 5-7 as fulfilled in Christ. Hebrews makes much of his lack of recorded ancestry: <em>"Without father, without mother, without descent, having neither beginning of days, nor end of life; but made like unto the Son of God; abideth a priest continually"</em> (<em>Hebrews 7:3</em>). Type of Christ’s eternal priesthood.</p>'
    ),
    'zephaniah-prophet': (
        '<p>Zephaniah was a late seventh-century BC prophet during the reign of King Josiah in Judah (c. 640-609 BC) — and probably a great-great-grandson of King Hezekiah, which would make him a royal kinsman of the reforming king. His three-chapter book of judgment-and-restoration develops Day-of-the-LORD theology more intensely than any other minor prophet: <em>"The great day of the LORD is near, it is near, and hasteth greatly... That day is a day of wrath, a day of trouble and distress... a day of darkness and gloominess"</em> (<em>Zephaniah 1:14-15</em>). After cataloging the judgments on Judah and the surrounding nations, the book closes with one of the most beautiful restoration promises in the prophets: <em>"The LORD thy God in the midst of thee is mighty; he will save, he will rejoice over thee with joy; he will rest in his love, he will joy over thee with singing"</em> (<em>3:17</em>).</p>'
    ),
    'junia': (
        '<p>Junia is named in <em>Romans 16:7</em> alongside Andronicus as Paul’s kinsmen, fellow prisoners, <em>"of note among the apostles"</em>, and in Christ before Paul himself: <em>"Salute Andronicus and Junia, my kinsmen, and my fellow-prisoners, who are of note among the apostles, who also were in Christ before me."</em> Most modern scholarship reads Junia as feminine (<em>Iounia</em>, a common Latin feminine name; the contracted masculine <em>Iounias</em> is not attested in Greco-Roman sources), and the early church fathers (Chrysostom included) overwhelmingly read her as a woman. The phrase <em>"of note among the apostles"</em> probably means well-known <em>to</em> the apostles rather than <em>numbered among</em> them in the strict twelve-plus-Paul sense — a likely reading consistent with Paul’s otherwise strict use of the title.</p>'
    ),
    'joseph-of-arimathea': (
        '<p>Joseph of Arimathea was a wealthy and respected member of the Sanhedrin who had not consented to the council’s plot against Jesus (<em>Luke 23:51</em>). All four Gospels record his role at the burial. <em>"He went in boldly unto Pilate, and craved the body of Jesus"</em> (<em>Mark 15:43</em>) — a costly request that publicly identified him with the executed Lord. He wrapped the body in fine linen, laid it in his own new tomb hewn out of rock, and rolled a great stone to the door (<em>Matthew 27:57-60</em>). John reveals that he had been a secret disciple <em>"for fear of the Jews"</em> (<em>John 19:38</em>) — but the cross undid the secrecy. The wealthy councilman provided the tomb that Christ borrowed for three days. Tradition makes him the apostle of Britain.</p>'
    ),
    'huldah': (
        '<p>Huldah was a prophetess in Jerusalem during the reign of King Josiah (c. 622 BC), wife of Shallum the keeper of the wardrobe. When Hilkiah the high priest discovered the Book of the Law during temple repairs, the king’s deputies — including Hilkiah himself, Shaphan the scribe, and Ahikam — were sent specifically to Huldah for prophetic authentication (<em>2 Kings 22:14-20; 2 Chronicles 34:22-28</em>). She confirmed the book as genuine, prophesied coming judgment on Judah for covenant-breaking, but assured Josiah that because his heart was tender and he had humbled himself before the LORD, the judgment would be delayed until after his death: <em>"thine eyes shall not see all the evil which I will bring upon this place."</em> The greatest king of Judah’s late period sought confirmation from a woman prophet.</p>'
    ),
    'antioch-pisidia': (
        '<p>Antioch of Pisidia was a Roman colony in central Asia Minor where Paul preached his first recorded sermon (<em>Acts 13:14-52</em>), tracing salvation history from Israel’s exodus through David to the resurrection of Jesus. The reception split predictably: <em>"And when the Jews were gone out of the synagogue, the Gentiles besought that these words might be preached to them the next sabbath. And the next sabbath day came almost the whole city together to hear the word of God. But when the Jews saw the multitudes, they were filled with envy"</em> (<em>13:42-45</em>). The Jews stirred up the leading women and chief men of the city to expel Paul and Barnabas, who shook off the dust of their feet and departed for Iconium. Paul revisited the city on his return journey to strengthen the disciples (<em>14:21-22</em>).</p>'
    ),
    'timothy-figure': (
        '<p>Timothy was Paul’s second-generation disciple — son of a Jewish believer Eunice and a Greek father, raised in the Scriptures by his mother and grandmother Lois (<em>2 Timothy 1:5; 3:15; Acts 16:1</em>) at Lystra. Paul calls him repeatedly <em>"my son"</em>, <em>"my dearly beloved son"</em>, and <em>"my own son in the faith"</em> (<em>1 Timothy 1:2, 18; 2 Timothy 1:2; 2:1</em>). Timothy joined Paul on the second missionary journey, became Paul’s most trusted delegate (sent to Thessalonica, Corinth, Philippi, Ephesus), and was finally left as overseer in Ephesus to combat false teaching. Paul’s two letters to him are among the New Testament’s most personal pastoral writings. Hebrews 13:23 records his imprisonment and release. Tradition says he was martyred in Ephesus during the reign of Domitian or Nerva.</p>'
    ),
    'bartholomew': (
        '<p>Bartholomew was one of the Twelve, named in all four apostle lists (<em>Matthew 10:3; Mark 3:18; Luke 6:14; Acts 1:13</em>) but never given a separate biographical scene in the Synoptics or Acts. The patronymic form of his name (<em>Bar-Tolmai</em>, "son of Tolmai") suggests "Bartholomew" was not his given name — and tradition (going back to the ninth century) identifies him with Nathanael of Cana, whom Philip brought to Christ in <em>John 1:45-51</em>. If so, he is the disciple Christ commended as <em>"an Israelite indeed, in whom is no guile"</em>. Eusebius records a tradition that Bartholomew preached the gospel in India, leaving behind a copy of Matthew’s Gospel in Hebrew. Other traditions place his martyrdom in Armenia, where he was flayed alive — a fate often depicted in Christian art.</p>'
    ),
    'joanna': (
        '<p>Joanna was the wife of Chuza, steward of Herod Antipas — that is, the chief financial administrator of the royal household at the very court that beheaded John the Baptist. She was healed by Jesus of <em>"evil spirits and infirmities"</em> (<em>Luke 8:2</em>) and became one of the women who supported Christ’s itinerant ministry <em>"of their substance"</em> (<em>Luke 8:3</em>). Joanna was among the women who came to the tomb on Easter morning with the spices and were told by the angels of the resurrection: <em>"It was Mary Magdalene, and Joanna, and Mary the mother of James, and other women that were with them, which told these things unto the apostles"</em> (<em>Luke 24:10</em>). An aristocratic woman of Herod’s court funded the ministry of the King her king had hated.</p>'
    ),
    'gregory-nazianzen': (
        '<p>Gregory of Nazianzus (c. 329-389) was the third of the Cappadocian Fathers (with Basil the Great and Gregory of Nyssa) — and the architect of orthodox Trinitarian formulation. His <em>Theological Orations</em> (380), preached in Constantinople, gave the church its definitive defense of the full deity of the Son and the Spirit against late Arian and Pneumatomachian opposition. He served briefly as Patriarch of Constantinople and presided at the opening of the First Council of Constantinople (381), where the Nicene Creed was finalized. He resigned in weariness over ecclesial politics and retired to write poetry and pastoral letters. Famous lines: <em>"That which is not assumed is not healed"</em> (against Apollinarianism); <em>"The Son is the same as the Father, except in being the Son."</em> The orthodox Trinitarian vocabulary the church still uses owes more to him than to any other single figure.</p>'
    ),
    'judah-tribe': (
        '<p>Judah is the tribe descended from the fourth son of Jacob and Leah, named in Jacob’s deathbed blessing as the royal tribe: <em>"The sceptre shall not depart from Judah, nor a lawgiver from between his feet, until Shiloh come; and unto him shall the gathering of the people be"</em> (<em>Genesis 49:10</em>) — the great Messianic prophecy. Its tribal territory included Jerusalem and Bethlehem. The Davidic line came through it, and the southern kingdom after the divided monarchy bore its name (the kingdom of Judah, 931-586 BC, eventually giving us the term <em>Jew</em>). Christ Himself is named the Lion of the tribe of Judah: <em>"Behold, the Lion of the tribe of Juda, the Root of David, hath prevailed to open the book"</em> (<em>Revelation 5:5</em>). The scepter has come; the sceptered King reigns.</p>'
    ),
    'centurion-cross': (
        '<p>The Centurion at the Cross was the Roman officer commanding the execution detail at Christ’s crucifixion. Watching Him die and witnessing the accompanying signs — three hours of darkness from the sixth to the ninth hour, the earthquake that split rocks and tore open graves — he was undone. <em>"Now when the centurion, and they that were with him, watching Jesus, saw the earthquake, and those things that were done, they feared greatly, saying, Truly this was the Son of God"</em> (<em>Matthew 27:54</em>; cf. <em>Mark 15:39</em>). Luke records the confession slightly differently: <em>"Certainly this was a righteous man"</em> (<em>Luke 23:47</em>). The first post-cross confession of the gospel came not from a disciple but from a Gentile centurion — a foretaste of the wide opening of the kingdom to the nations.</p>'
    ),
    'bunyan': (
        '<p>John Bunyan (1628-1688) was the English Baptist tinker, lay preacher, and allegorist whose <em>Pilgrim’s Progress</em> is the most-read Christian book outside the Bible — translated into more than two hundred languages. Imprisoned in Bedford county jail for twelve years (1660-1672) under Charles II’s persecution of nonconformists, he wrote much of his work behind bars. The first part of <em>Pilgrim’s Progress</em> appeared in 1678. Other major works: <em>Grace Abounding to the Chief of Sinners</em> (spiritual autobiography), <em>The Holy War</em>, <em>The Life and Death of Mr. Badman</em>. Famous opening: <em>"As I walked through the wilderness of this world, I lighted on a certain place where was a Den; and I laid me down in that place to sleep: and as I slept I dreamed a dream."</em> A Puritan classic in pilgrim form.</p>'
    ),
    'hymenaeus': (
        '<p>Hymenaeus was a first-century false teacher named twice by Paul. In <em>1 Timothy 1:19-20</em>, Paul says that he and Alexander <em>"have made shipwreck"</em> of the faith — and that he had delivered them to Satan, <em>"that they may learn not to blaspheme"</em>. In <em>2 Timothy 2:17-18</em>, Paul identifies the specific heresy: <em>"Their word will eat as doth a canker: of whom is Hymenaeus and Philetus; Who concerning the truth have erred, saying that the resurrection is past already; and overthrow the faith of some."</em> A spiritualized, already-realized resurrection doctrine — the bodily resurrection denied or relocated to a present-tense allegorical event — was already spreading in the apostolic generation. Paul’s response was excommunication. The pattern endures: gnostic and over-realized eschatology persistently re-emerge in church history.</p>'
    ),
    'amos-prophet': (
        '<p>Amos was an eighth-century BC prophet from Tekoa in Judah — a small village about ten miles south of Jerusalem — who described himself as <em>"no prophet, neither... a prophet’s son; but I was an herdman, and a gatherer of sycomore fruit"</em> (<em>Amos 7:14</em>). The LORD took him from following the flock and sent him to prophesy in the northern kingdom of Israel during the prosperous reign of Jeroboam II (c. 760-750 BC). His message was hard-edged: judgment on social injustice, false worship, and complacent prosperity. He thundered against luxurious women (<em>"kine of Bashan"</em>, <em>4:1</em>), against those who <em>"sold the righteous for silver, and the poor for a pair of shoes"</em> (<em>2:6</em>), and famously: <em>"But let judgment run down as waters, and righteousness as a mighty stream"</em> (<em>5:24</em>). The book closes with Davidic restoration.</p>'
    ),
    'gerizim': (
        '<p>Mount Gerizim is the southern of the two mountains flanking Shechem in central Canaan (Mount Ebal is the northern). Moses commanded that, on entering the promised land, Joshua would set six tribes on Gerizim to bless the people and six on Ebal to curse them — with the priests and the ark in the valley between, reading the blessings and curses of the covenant aloud (<em>Deuteronomy 11:29; 27:11-13; Joshua 8:33-34</em>). The blessing-mountain. Later, after the kingdom split, the Samaritans built a rival temple on Gerizim in the fourth century BC and worshipped there in defiance of Jerusalem. The Samaritan woman at the well asked Christ about it: <em>"Our fathers worshipped in this mountain; and ye say, that in Jerusalem is the place where men ought to worship"</em> (<em>John 4:20</em>). He reframed the question entirely.</p>'
    ),
    'alexander-coppersmith': (
        '<p>Alexander the coppersmith did Paul much harm and strongly opposed his words. Paul warned Timothy to beware of him, committing his judgment to the Lord: <em>"Alexander the coppersmith did me much evil: the Lord reward him according to his works: Of whom be thou ware also; for he hath greatly withstood our words"</em> (<em>2 Timothy 4:14-15</em>). Whether this Alexander is the same as the Alexander whom Paul had earlier <em>"delivered unto Satan"</em> along with Hymenaeus (<em>1 Timothy 1:20</em>), or the Alexander pushed forward by the Jews at Ephesus during the Demetrius riot (<em>Acts 19:33</em>), is debated. Either way, Paul’s pastoral instinct is clear: name false teachers explicitly so younger ministers can avoid them, and entrust their final judgment to the Lord rather than seeking personal revenge.</p>'
    ),
    'intelligent-design-mvmt': (
        '<p>The Intelligent Design Movement is the late twentieth-century academic and apologetic movement that argues scientific evidence — especially in biology and cosmology — points to intelligent design rather than blind material processes. Major figures: Phillip Johnson (<em>Darwin on Trial</em>, 1991), Michael Behe (<em>Darwin’s Black Box</em>, 1996, irreducible complexity), William Dembski (specified complexity), Stephen Meyer (<em>Signature in the Cell</em>, <em>Darwin’s Doubt</em>), Jonathan Wells. The Discovery Institute in Seattle is the movement’s primary academic center. Critics (Eugenie Scott, the National Center for Science Education) charge that it is creationism in disguise; proponents respond that they argue from the evidence to a designer without specifying the designer’s identity theologically. Reformed Christians broadly support the movement’s critique of materialism while pressing on to confess the Designer by name.</p>'
    ),
    'herod-antipas-figure': (
        '<p>Herod Antipas was the tetrarch of Galilee and Perea (4 BC-AD 39) — son of Herod the Great by his Samaritan wife Malthace, brother of Archelaus, half-brother to Philip. He is the Herod who beheaded John the Baptist for naming his unlawful marriage to Herodias, his brother Philip’s wife (<em>Matthew 14:1-12; Mark 6:14-29; Luke 9:7-9</em>). When Jesus came to trial, Pilate sent Him to Antipas (then visiting Jerusalem for Passover); Antipas questioned Him eagerly hoping to see a miracle, but Christ answered nothing, and Antipas mocked Him and sent Him back to Pilate (<em>Luke 23:6-12</em>). Christ called him <em>"that fox"</em> (<em>Luke 13:32</em>). Eventually he was exiled to Gaul by Caligula in AD 39 after Herodias’s envy of her brother Agrippa I’s rise — and disappeared from history there.</p>'
    ),
    'dorcas-tabitha': (
        '<p>Dorcas (Aramaic <em>Tabitha</em>, meaning "gazelle" in both languages) was a disciple in Joppa <em>"full of good works and almsdeeds which she did"</em> (<em>Acts 9:36</em>). She clothed the widows of her city with the coats and garments she had sewn with her own hands — small acts of ordinary mercy that defined her ministry. When she fell sick and died, the disciples sent two men to Lydda calling Peter to come quickly. He came, found the upper room full of weeping widows showing him the very garments Dorcas had made for them, sent them all out, knelt down by the body, prayed, and said simply: <em>"Tabitha, arise."</em> She opened her eyes, sat up, and was given back to the saints: <em>"And it was known throughout all Joppa; and many believed in the Lord"</em> (<em>9:42</em>). Quiet faithfulness; loud witness.</p>'
    ),
    'basil-the-great': (
        '<p>Basil the Great (c. 330-379) was Bishop of Caesarea in Cappadocia (modern central Turkey) and one of the three Cappadocian Fathers — with Gregory of Nazianzus and Basil’s younger brother Gregory of Nyssa — whose theology completed the Nicene defense of full Trinitarian orthodoxy against Arianism. Trained in rhetoric at Athens, converted under his sister Macrina the Younger’s influence, ordained 365 and consecrated bishop 370. Major works: <em>On the Holy Spirit</em> (defending the deity of the Spirit), <em>Hexaemeron</em> (homilies on the six days of creation), the <em>Liturgy of St. Basil</em> still used in Eastern Orthodox worship, and the monastic rule that shaped Eastern monasticism as Benedict’s did the West. He also organized one of the earliest hospitals for the poor (the <em>Basileias</em>) outside Caesarea. Tough, brilliant, and pastoral.</p>'
    ),
    'simeon-niger': (
        '<p>Simeon called Niger was one of the prophets and teachers in the church at Antioch (<em>Acts 13:1</em>) — the first multi-ethnic congregation in Christian history and the launching point of Paul’s missionary journeys. The five named teachers are remarkably diverse: Barnabas (Cypriot Jew), Simeon Niger (Hebrew name with Latin nickname), Lucius of Cyrene (North African), Manaen (foster-brother of Herod the tetrarch), and Saul of Tarsus. Simeon’s double name (Hebrew given-name plus Latin <em>Niger</em>, meaning "black") suggests he may have been a dark-skinned African Jew, and some scholars have proposed identifying him with Simon of Cyrene who carried Christ’s cross. The Antioch leadership cohort models the church Christ is building from every tribe, tongue, people, and nation.</p>'
    ),
    'demetrius': (
        '<p>Demetrius was an Ephesian silversmith who made silver shrines of the goddess Diana (Artemis) and saw his entire industry threatened by Paul’s preaching. He gathered the craftsmen, made an economic case (<em>"by this craft we have our wealth"</em>) and a religious one (<em>"the temple of the great goddess Diana should be despised"</em>), and incited the famous Ephesian riot that filled the theater with two hours of chanting: <em>"Great is Diana of the Ephesians!"</em> (<em>Acts 19:24-41</em>). The town clerk eventually quieted the crowd by appealing to the courts and the proconsul. The riot illustrates a perennial pattern: when the gospel threatens an entrenched economic-religious order, expect both economic alarm and religious appeal weaponized together. A different Demetrius is commended in <em>3 John 12</em> for his good report.</p>'
    ),
    'helmet-salvation': (
        '<p>The Helmet of Salvation is the sixth piece of the whole armor of God in <em>Ephesians 6:17</em>: <em>"And take the helmet of salvation, and the sword of the Spirit, which is the word of God."</em> The helmet protects the head — and therefore the mind, the seat of faith and assurance. Paul re-uses the image in <em>1 Thessalonians 5:8</em>: <em>"the hope of salvation" as a helmet</em>. The image is borrowed directly from Isaiah, where the Lord Himself first wore it: <em>"For he put on righteousness as a breastplate, and an helmet of salvation upon his head"</em> (<em>Isaiah 59:17</em>). The believer wears the helmet his Savior wore first. The helmet defends the mind against despair, doubt, and the accuser’s suggestion that salvation could be lost. Settled assurance protects everything else.</p>'
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
