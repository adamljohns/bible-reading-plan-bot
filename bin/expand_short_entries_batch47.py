#!/usr/bin/env python3
"""Batch 47 — expand 25 more entries from the 60-70 word bucket.

Targets: covenant theology, NT figures, doctrines, OT figures,
divine names, hermeneutics, eschatology, and ecclesial vocabulary.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'chalice': (
        '<p>A chalice is the cup used for the wine in the Lord’s Supper — the New Testament cup, the cup of blessing, the new covenant in Christ’s blood. Christ named it on the night of His betrayal: <em>"This cup is the new testament in my blood, which is shed for you"</em> (<em>Luke 22:20</em>; cf. <em>Matthew 26:27-28; Mark 14:23-24; 1 Corinthians 11:25</em>). Paul names it <em>"the cup of blessing which we bless"</em> (<em>1 Corinthians 10:16</em>). The chalice is the household instrument by which the New-Covenant church proclaims the Lord’s death until He comes. Whether shared common cup (the ancient practice) or individual cups (the modern accommodation), the meaning is the same: drink, remember, proclaim.</p>'
    ),
    'covenant-hermeneutic': (
        '<p>The Covenant Hermeneutic reads Scripture as a unified covenantal narrative. The whole Bible is the story of God making and keeping covenants — with Adam (the covenant of works in creation, broken at the fall), with Noah (creation-preservation, <em>Genesis 9</em>), with Abraham (election and promise, <em>Genesis 15, 17</em>), with Moses (law at Sinai, <em>Exodus 19-24</em>), with David (kingship, <em>2 Samuel 7</em>), and consummated in the New Covenant of Christ (<em>Jeremiah 31:31-34; Luke 22:20; Hebrews 8</em>). Each covenant builds on the prior; each is administered by sovereign grace. The Reformed tradition explicitly organizes its hermeneutic around this framework — covenants of works and of grace, one continuous covenant of grace administered through successive epochs.</p>'
    ),
    'covenant': (
        '<p>A covenant is a solemn, binding agreement between two or more parties — sworn, often sealed in blood, and usually accompanied by signs of remembrance. In the Bible, covenant is the <em>primary framework</em> through which God relates to humanity. Biblical covenants are sovereignly administered by God (He proposes the terms; man does not negotiate). Each typically includes <em>promises</em> (what God will do), <em>stipulations</em> (what is expected of the partner), and <em>signs</em> (rainbow, circumcision, Sabbath, the blood of the New Covenant cup). The biblical canon names six major divine covenants — Adamic, Noahic, Abrahamic, Mosaic, Davidic, and the New Covenant of Christ — and many lesser human covenants modeled on them. Marriage is covenant; friendship can be covenant; baptism is covenant sign.</p>'
    ),
    'darius-king': (
        '<p>Three Persian kings named Darius appear in Scripture, and they are easily confused. (1) <em>Darius the Mede</em> (<em>Daniel 5:31; 6</em>) — who took the kingdom after Belshazzar’s fall and signed the foolish decree that put Daniel in the lions’ den; identified by some scholars as Cyrus, by others as Cyaxares II, by others as Gubaru. (2) <em>Darius I the Great</em> (reigned 522-486 BC; <em>Ezra 4:5; 6:1-15; Haggai 1:1; Zechariah 1:1</em>) — under whose second-year decree the second temple was finally completed in 516 BC. (3) <em>Darius II</em> (reigned 423-405 BC; <em>Nehemiah 12:22</em>) — under whom Nehemiah’s era closed. Scripture treats each as the LORD’s providential instrument for Israel’s good.</p>'
    ),
    'deliver-from-evil': (
        '<p>"Deliver us from evil" is the seventh and final petition of the Lord’s Prayer in Matthew’s version: <em>"And lead us not into temptation, but deliver us from evil"</em> (<em>Matthew 6:13</em>). The Greek text has the article — <em>"deliver us from the evil one"</em> (<em>apo tou ponerou</em>) — and many modern translations render it so. The petition asks for rescue from Satan and from his works of evil in the world and in our own flesh. Christ Himself models the prayer for the disciples in His high-priestly prayer: <em>"I pray not that thou shouldest take them out of the world, but that thou shouldest keep them from the evil"</em> (<em>John 17:15</em>). Christian men pray it daily.</p>'
    ),
    'demonology': (
        '<p>Demonology is the biblical doctrine of evil spirits. Scripture teaches that demons are fallen angels who rebelled with Satan: <em>"And there was war in heaven: Michael and his angels fought against the dragon; and the dragon fought and his angels"</em> (<em>Revelation 12:7-9</em>). They are personal, intelligent, malicious spiritual beings who oppose God, deceive humanity (<em>1 Timothy 4:1</em>), and empower false religions (<em>1 Corinthians 10:20</em>). Jesus demonstrated absolute authority over demons throughout His ministry (<em>Mark 1:21-27; 5:1-20; 9:14-29</em>) — they recognized Him, feared Him, and obeyed Him instantly. He delegated the same authority to His disciples (<em>Luke 10:17-20</em>). Demons are real; they are powerful; and they have already been defeated at the cross (<em>Colossians 2:15</em>).</p>'
    ),
    'epaphras': (
        '<p>Epaphras was the founder and pastor of the Colossian church — almost certainly converted under Paul’s ministry in Ephesus and sent home to plant the church in Colossae and the surrounding Lycus valley (Laodicea and Hierapolis). Paul calls him <em>"our dear fellowservant, who is for you a faithful minister of Christ; Who also declared unto us your love in the Spirit"</em> (<em>Colossians 1:7-8</em>). Later Paul names him a fellow-prisoner with himself in Rome (<em>Philemon 23</em>). Most strikingly, Paul commends Epaphras’s prayer ministry: <em>"always labouring fervently for you in prayers, that ye may stand perfect and complete in all the will of God. For I bear him record, that he hath a great zeal for you"</em> (<em>Colossians 4:12-13</em>). The model pastor labors in prayer.</p>'
    ),
    'fig-tree-israel': (
        '<p>The fig tree appears across Scripture in two recurring roles. First, as symbol of <em>peace and prosperity</em>: the idyll of every man <em>"under his vine and under his fig tree"</em> (<em>1 Kings 4:25</em>; <em>Micah 4:4</em>; <em>Zechariah 3:10</em>) — the picture of secure household life under God’s blessing. Second, as symbol of <em>Israel itself</em>, often under judgment for fruitlessness: Christ’s cursing of the leafy-but-fruitless fig tree on the way to Jerusalem (<em>Mark 11:12-14, 20-21</em>) — performed dramatically the very day before the temple cleansing — was an enacted parable of Israel’s coming judgment. The parable of the fruitless fig tree in <em>Luke 13:6-9</em> teaches the same. Outward leaves without inward fruit invites the Owner’s axe.</p>'
    ),
    'foolishness-cross': (
        '<p>"The foolishness of the cross" is Paul’s argument in <em>1 Corinthians 1:18-25</em> that the message of a crucified Messiah is <em>mōria</em> ("folly") to those who perish but <em>dynamis theou</em> ("the power of God") to those who are saved. <em>"For the preaching of the cross is to them that perish foolishness; but unto us which are saved it is the power of God"</em> (<em>v. 18</em>). The Greeks sought wisdom (philosophical sophistication); the Jews sought signs (visible power); the apostles preached <em>"Christ crucified, unto the Jews a stumblingblock, and unto the Greeks foolishness; But unto them which are called, both Jews and Greeks, Christ the power of God, and the wisdom of God"</em> (<em>vv. 23-24</em>). What looks foolish to the world is the deepest wisdom of God.</p>'
    ),
    'hypocrisy': (
        '<p>Hypocrisy is the playing of a part not one’s own — pretending righteousness one does not actually possess. The Greek <em>hypokritēs</em> originally named a stage actor playing a role behind a mask. Christ’s sharpest words were aimed at it: the seven woes against the scribes and Pharisees in <em>Matthew 23</em>, each addressed to <em>"scribes and Pharisees, hypocrites!"</em> The diagnosis is sustained throughout: <em>"Woe unto you... ye are like unto whited sepulchres, which indeed appear beautiful outward, but are within full of dead men’s bones, and of all uncleanness. Even so ye also outwardly appear righteous unto men, but within ye are full of hypocrisy and iniquity"</em> (<em>vv. 27-28</em>). Hypocrisy is the religious sin par excellence — and it is repeatedly the sin Christ names hardest.</p>'
    ),
    'iconium': (
        '<p>Iconium was a major city of Asia Minor — modern Konya, Turkey — visited by Paul and Barnabas on the first missionary journey (<em>Acts 13:51-14:6</em>) and revisited on the second (<em>Acts 16:1-2</em>) and likely the third. The pattern there became the pattern of Paul’s mission everywhere: <em>"And it came to pass in Iconium, that they went both together into the synagogue of the Jews, and so spake, that a great multitude both of the Jews and also of the Greeks believed. But the unbelieving Jews stirred up the Gentiles, and made their minds evil affected against the brethren"</em> (<em>14:1-2</em>). When a plot to stone them was uncovered, they fled to Lystra and Derbe. Iconium was also Timothy’s home region. The gospel takes root in resistance.</p>'
    ),
    'ish-bosheth': (
        '<p>Ish-bosheth ("man of shame," likely an editorial substitution for his original name <em>Eshbaal</em>, "man of Baal") was Saul’s youngest son, set up as rival king of Israel by Saul’s general Abner after Saul’s death at Mount Gilboa (<em>2 Samuel 2-4</em>). He reigned from Mahanaim east of the Jordan for two years over eleven tribes, while David reigned over Judah from Hebron. He was a weak figurehead under Abner’s real control. After Abner’s defection to David and subsequent murder by Joab, Ish-bosheth was murdered in his own bed by two of his own captains during his midday rest (<em>2 Samuel 4:5-7</em>). The two murderers were executed by David. Saul’s house ended in shame; David’s in covenant.</p>'
    ),
    'jehovah-nissi': (
        '<p><em>Jehovah-Nissi</em> (יְהוָה נִסִּי) — "the LORD my banner" — is the covenant name Moses gave the altar he built at Rephidim after Israel defeated Amalek not by Joshua’s sword in the valley but by Moses’ lifted hands on the hilltop (<em>Exodus 17:8-16</em>). The banner (<em>nes</em>) of an army was its rallying point and its identity in battle — a tall standard visible across the field around which the troops gathered. Israel’s rallying point is therefore the LORD Himself, and the victory belongs to Him: <em>"Because the LORD hath sworn that the LORD will have war with Amalek from generation to generation"</em> (<em>17:16</em>). Christian men march under one banner: the cross of the LORD Jesus Christ.</p>'
    ),
    'joanna-disciple': (
        '<p>Joanna was the wife of Chuza, Herod Antipas’s household steward (<em>epitropos</em>) — an aristocratic woman of the Herodian royal court who, after being healed by Christ of some affliction, supported His ministry from her own means: <em>"Joanna the wife of Chuza Herod’s steward, and Susanna, and many others, which ministered unto him of their substance"</em> (<em>Luke 8:3</em>). She was among the women who came to the empty tomb on Easter morning: <em>"It was Mary Magdalene, and Joanna, and Mary the mother of James, and other women that were with them, which told these things unto the apostles"</em> (<em>Luke 24:10</em>). Her presence in Antipas’s court was almost certainly Luke’s window into the king’s deliberations about Jesus.</p>'
    ),
    'luke-figure': (
        '<p>Luke was a Gentile (Greek) physician (<em>"Luke, the beloved physician, and Demas, greet you"</em>, <em>Colossians 4:14</em>), Paul’s traveling companion through much of the second and third missionary journeys, and the only New Testament writer who was not a Jew. He wrote the Gospel that bears his name and the Acts of the Apostles together — about a quarter of the New Testament. His "we" passages in Acts (<em>16:10-17; 20:5-21:18; 27:1-28:16</em>) mark his personal eyewitness participation. He was Paul’s most faithful companion in the end: <em>"Only Luke is with me"</em> (<em>2 Timothy 4:11</em>), the apostle’s last letter from a Roman prison facing martyrdom. The doctor stayed when others fled.</p>'
    ),
    'mantle-of-elijah': (
        '<p>The mantle of Elijah was the prophet’s rough hairy cloak — thrown by him over Elisha’s shoulders at the calling (<em>"And he left the oxen, and ran after Elijah"</em>, <em>1 Kings 19:19-21</em>); taken up by Elisha at Elijah’s ascension in the whirlwind (<em>2 Kings 2:13-14</em>); used to strike the Jordan in confirmation of the prophetic inheritance (the water parted, just as it had for Elijah). The mantle became the recognized symbol of prophetic succession in Israel: <em>"The spirit of Elijah doth rest on Elisha"</em>, the sons of the prophets declared (<em>2 Kings 2:15</em>). Christ Himself is the greater Elijah whose mantle now rests on every Spirit-baptized believer in some measure — the church inherits the prophetic word.</p>'
    ),
    'motive': (
        '<p>Motive is the inward reason or intent behind an outward act — the heart-direction the LORD weighs alongside the deed itself. <em>"All the ways of a man are clean in his own eyes; but the LORD weigheth the spirits"</em> (<em>Proverbs 16:2</em>); <em>"The LORD looketh on the heart"</em> (<em>1 Samuel 16:7</em>); <em>"For the word of God... is a discerner of the thoughts and intents of the heart"</em> (<em>Hebrews 4:12</em>). God judges deeds <em>by</em> motives, not motives <em>by</em> deeds. The same outward act can be done for utterly different reasons before God — almsgiving for the Father’s reward or for men’s applause (<em>Matthew 6:1-4</em>); prayer in faith or in showmanship; fasting in humility or in display. Examine motives daily.</p>'
    ),
    'oath-keeper': (
        '<p>An oath-keeper is one who, having sworn an oath, performs it — even when it costs him. <em>Psalm 15</em> describes the man who shall abide in God’s tabernacle and dwell on His holy hill: <em>"He that sweareth to his own hurt, and changeth not"</em> (<em>v. 4</em>). The Marine’s oath of enlistment, the citizen’s oath of allegiance, the marriage oath at the altar, the membership oath of the local church, the ordination oath of the elder — all rise or fall on this character. <em>"Better is it that thou shouldest not vow, than that thou shouldest vow and not pay"</em> (<em>Ecclesiastes 5:5</em>). Christ commands plain yes-and-no speech (<em>Matthew 5:33-37</em>), but where oaths <em>are</em> sworn, they must be kept. A man’s word is his bond.</p>'
    ),
    'olivet': (
        '<p>Olivet — the Mount of Olives — is the ridge running north-south east of Jerusalem across the Kidron Valley, rising about 2,700 feet. It was the geographic stage of the most decisive moments of Christ’s passion week and resurrection. He wept over the city from its western slope: <em>"O Jerusalem, Jerusalem... how often would I have gathered thy children together!"</em> (<em>Luke 19:41; Matthew 23:37</em>). He delivered the Olivet Discourse on its crest (<em>Matthew 24-25</em>). He prayed in Gethsemane at its foot (<em>Matthew 26:36-46</em>). He was arrested there. And He ascended bodily into heaven from Olivet (<em>Acts 1:9-12</em>) — and Zechariah prophesies His feet shall stand on the same mount at His return (<em>Zechariah 14:4</em>).</p>'
    ),
    'opening-mouth': (
        '<p>"Opening the mouth" is Scripture’s simple, frequent way of marking speech as worth marking — the verb foregrounded to signal that what follows is weighty. God opens His mouth to teach: <em>"And he opened his mouth, and taught them, saying"</em> (<em>Matthew 5:2</em>) — the opening of the Sermon on the Mount. The Psalmist begs the LORD to open his lips: <em>"O Lord, open thou my lips; and my mouth shall shew forth thy praise"</em> (<em>Psalm 51:15</em>). The saint is to open his mouth wide for God to fill it: <em>"Open thy mouth wide, and I will fill it"</em> (<em>Psalm 81:10</em>). To open the mouth is the body’s preparation to speak deliberately. Christian men should open the mouth more often — for blessing, instruction, and witness.</p>'
    ),
    'postmillennial': (
        '<p>Postmillennialism is the eschatological view that Christ returns bodily <em>after</em> the millennium — which is understood not as a literal future thousand-year political reign of Christ on earth, but as a long period of gospel triumph and increasing Christian influence on the nations <em>before</em> the consummation. The Great Commission is read optimistically: the gospel <em>will</em> succeed; the nations will be discipled; Christ’s kingdom will gradually fill the earth as <em>"the waters cover the sea"</em> (<em>Habakkuk 2:14</em>; <em>Isaiah 11:9</em>). Historic Puritan and Reformed proponents include Jonathan Edwards, the Hodges, B. B. Warfield, R. L. Dabney, and many modern Reformed thinkers. The view fuels missionary ambition: the King <em>shall</em> reign over the earth before He returns.</p>'
    ),
    'profession': (
        '<p>Profession in Scripture is what one publicly declares — both the <em>trade</em> by which one earns and the <em>faith</em> by which one lives. The two senses overlap: a man’s profession is the public-facing identity, what he is known by. Hebrews calls believers to <em>"hold fast the profession of our faith without wavering; (for he is faithful that promised:)"</em> (<em>Hebrews 10:23</em>; cf. <em>3:1; 4:14</em>). Paul appeals to Timothy’s <em>"good profession before many witnesses"</em> at his baptism or ordination (<em>1 Timothy 6:12</em>). Christian men should mean what they profess — in vocation and in confession. The discrepancy between profession and practice is hypocrisy; the alignment is integrity. Christ Himself made <em>"a good confession before Pontius Pilate"</em> (<em>6:13</em>).</p>'
    ),
    'provision': (
        '<p>Provision in Scripture is God’s active supply of His people’s needs — not abstract sustaining but specific daily care. Christ teaches it directly: <em>"Give us this day our daily bread"</em> (<em>Matthew 6:11</em>); <em>"Take no thought for your life, what ye shall eat... your heavenly Father knoweth that ye have need of all these things"</em> (<em>6:25-32</em>). Scripture is dense with examples: the manna in the wilderness (<em>Exodus 16</em>), the ravens feeding Elijah by the brook Cherith (<em>1 Kings 17</em>), the widow’s endless oil and meal (<em>1 Kings 17:14-16</em>), the multiplied loaves and fishes (<em>Matthew 14, 15</em>). The Hebrew <em>Yahweh-Jireh</em> ("the LORD will provide", <em>Genesis 22:14</em>) names the doctrine. Trust the Father’s open hand.</p>'
    ),
    'reformed-theology': (
        '<p>Reformed Theology is the Protestant tradition descended primarily from the sixteenth-century Swiss-Genevan Reformation under Huldrych Zwingli (Zurich), John Calvin (Geneva), and Heinrich Bullinger (Zurich) — distinguished from the parallel Lutheran tradition. It was extended through the Dutch Reformed (Heidelberg Catechism, Belgic Confession, Canons of Dort), the French Huguenots, the Scottish Presbyterians (Westminster Confession, Larger and Shorter Catechisms), and the English Puritans (Westminster, the Savoy Declaration). Its core convictions: the absolute sovereignty of God, salvation by grace alone through faith alone in Christ alone, the priority of Scripture over tradition, covenant theology, the spirituality of the Lord’s Supper, the regulative principle of worship, and the doctrines of grace summarized in the TULIP acronym.</p>'
    ),
    'servant-songs': (
        '<p>The Servant Songs are the four great poems in the second half of Isaiah portraying the LORD’s suffering Servant: <em>Isaiah 42:1-9; 49:1-13; 50:4-11; 52:13-53:12</em>. The Servant teaches with a quiet voice (<em>42:2-3</em>), is called from the womb (<em>49:1, 5</em>), sets His face like flint under suffering (<em>50:7</em>), is despised and rejected of men (<em>53:3</em>), suffers vicariously for the sins of His people (<em>"the LORD hath laid on him the iniquity of us all"</em>, <em>53:6</em>), justifies many by His knowledge (<em>53:11</em>), and is exalted high after the agony (<em>52:13; 53:12</em>). The New Testament identifies the Servant as Christ explicitly (<em>Matthew 8:17; 12:17-21; Acts 8:32-35; 1 Peter 2:21-25</em>).</p>'
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
