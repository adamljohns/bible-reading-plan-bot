#!/usr/bin/env python3
"""Batch 40 — expand 25 more entries from the 50-60 word bucket.

Brings the session total to 1,000 entries substantively expanded.

Targets: Hebrew vocab, NT figures, divine names, doctrines,
biblical imagery, slang reframes, and historical correctives.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'terebinth': (
        '<p>The terebinth (<em>Pistacia terebinthus</em>) is a large, long-lived tree of the pistachio family, common in Israel — and in Scripture, a frequent location of sacred encounter. Abraham received the three visitors at <em>"the plains [terebinths] of Mamre"</em> (<em>Genesis 18:1</em>). Gideon was called to deliver Israel under a terebinth at Ophrah (<em>Judges 6:11</em>). Jacob buried the foreign gods of his household and his earrings under a terebinth near Shechem (<em>Genesis 35:4</em>). Saul’s remains were buried under the terebinth in Jabesh-gilead (<em>1 Samuel 31:13</em>). The KJV often translates <em>"oak"</em> because the trees resemble each other. Whatever the species, the LORD repeatedly chose great trees as the canopy under which He met His servants.</p>'
    ),
    'testimony-personal': (
        '<p>Personal testimony is the believer’s spoken account of what God in Christ has done for him and through him. The saints overcome the accuser of the brethren by two weapons together: <em>"And they overcame him by the blood of the Lamb, and by the word of their testimony; and they loved not their lives unto the death"</em> (<em>Revelation 12:11</em>). Paul models personal testimony three times in Acts (chs. 9, 22, 26) — climactically before Agrippa, recounting his Damascus-road encounter. Christian testimony is not autobiographical theater; it is gospel proclamation through the conduit of one’s own life. The Christian man should learn to tell, briefly and powerfully, what Christ has done in him. The blood of the Lamb and the word of your testimony are paired.</p>'
    ),
    'wack': (
        '<p>"Wack" is dismissive Gen-X-era hip-hop slang for something judged bad, weak, uncool, or unpleasant — <em>"that movie was wack."</em> The slang frames taste as moral category: what is wack is to be rejected. Scripture also commands the saint to reject what is bad and cling to what is good: <em>"Abhor that which is evil; cleave to that which is good"</em> (<em>Romans 12:9</em>). But the biblical <em>bad</em> and <em>good</em> are anchored in God’s character, not in the speaker’s coolness instincts or generational aesthetic. The slang reveals the universal moral impulse — even relativists draw lines — while supplying it with the wrong floor. The Christian rejects rightly; the world rejects randomly. Same gesture; different anchor.</p>'
    ),
    'watchman-roles': (
        '<p>The watchman’s roles are three. First, <em>perceive</em> — see what is coming, attend to the horizon, refuse to sleep at the post (<em>"Watchman, what of the night?"</em>, <em>Isaiah 21:11</em>). Second, <em>warn</em> — sound the trumpet so the people can prepare: <em>Ezekiel 33:6</em>: <em>"if the watchman see the sword come, and blow not the trumpet... his blood will I require at the watchman’s hand."</em> Third, <em>intercede</em> — cry to God on behalf of those he watches: <em>"I have set watchmen upon thy walls, O Jerusalem, which shall never hold their peace day nor night: ye that make mention of the LORD, keep not silence"</em> (<em>Isaiah 62:6-7</em>). Habakkuk 2:1 models the standing. Failure on any of the three leaves the watchman accountable.</p>'
    ),
    'wickedness': (
        '<p>Wickedness is active, willful, settled commitment to evil — the disposition (not just the act) of the unrepentant heart. <em>Psalm 1</em> establishes the diagnostic contrast: the way of the righteous and the way of the wicked. <em>"For the LORD knoweth the way of the righteous: but the way of the ungodly shall perish"</em> (<em>Psalm 1:6</em>). The LORD hates wickedness: <em>"Thou lovest righteousness, and hatest wickedness"</em> (<em>Psalm 45:7</em>; quoted of Christ in <em>Hebrews 1:9</em>). The wicked shall not stand in the judgment (<em>Psalm 1:5</em>). Christ commands the saint to pray for deliverance from <em>"the wicked one"</em> (<em>Matthew 6:13</em>, KJV). The category exists; God names it; men either repent or are judged by it.</p>'
    ),
    'zealot': (
        '<p>The Zealots were a Jewish revolutionary party of the first century AD that advocated armed resistance against Roman occupation and against the Herodian client-kings — a movement that ultimately ignited the Jewish War (AD 66-70) and the destruction of Jerusalem. Simon, one of the Twelve Apostles, is identified as <em>"Simon called Zelotes"</em> (<em>Luke 6:15</em>; <em>Acts 1:13</em>) — likely a former Zealot before his calling. Christ’s choice of disciples is theologically striking: He called both a Zealot (Simon) and a tax collector (Matthew/Levi, the Roman collaborator) into the same band of twelve. Two political enemies, discipled into one love. The gospel reconciles what the world could not.</p>'
    ),
    'zera': (
        '<p><em>Zera</em> (זֶרַע) is the Hebrew word for <em>seed</em> — and Scripture loads it with a vast biblical sweep. The first messianic promise is of <em>the seed of the woman</em> who would crush the serpent’s head: <em>"And I will put enmity between thee and the woman, and between thy seed and her seed; it shall bruise thy head, and thou shalt bruise his heel"</em> (<em>Genesis 3:15</em>). The Abrahamic promise extends it: <em>"in thy seed shall all the nations of the earth be blessed"</em> (<em>Genesis 22:18</em>). David’s seed will reign on his throne forever (<em>2 Samuel 7:12-13</em>). Paul reveals the singular: <em>"He saith not, And to seeds, as of many; but as of one, And to thy seed, which is Christ"</em> (<em>Galatians 3:16</em>).</p>'
    ),
    'adversary': (
        '<p>"Adversary" is one of the New Testament’s direct titles for Satan. Peter writes: <em>"Be sober, be vigilant; because your adversary the devil, as a roaring lion, walketh about, seeking whom he may devour"</em> (<em>1 Peter 5:8</em>). The Hebrew <em>satan</em> means literally <em>"adversary"</em> — the one who stands opposite, accuses in court (<em>Job 1:6-12; Zechariah 3:1-2</em>), opposes in field (<em>Numbers 22:22</em>), and ambushes on road. The same word names the angel of the LORD who blocked Balaam’s path. Satan is the personal proper-name adversary par excellence — the prosecutor of the saints before God. Christ has disarmed him at the cross: <em>"having spoiled principalities and powers, he made a shew of them openly, triumphing over them in it"</em> (<em>Colossians 2:15</em>).</p>'
    ),
    'andrew': (
        '<p>Andrew was the brother of Simon Peter and the first disciple of John the Baptist to follow Christ. When John pointed and said <em>"Behold the Lamb of God!"</em>, Andrew and another disciple went after Jesus, abode with Him that day, and Andrew immediately <em>"first findeth his own brother Simon, and saith unto him, We have found the Messias... And he brought him to Jesus"</em> (<em>John 1:35-42</em>). Andrew is the apostle most often <em>introducing others to Jesus</em> — he brings Peter (his brother), the boy with the loaves and fishes (<em>John 6:8-9</em>), and the inquiring Greeks (<em>John 12:20-22</em>). Andrew is Scripture’s patron of personal evangelism: he never preaches a famous sermon; he keeps bringing people to the Lord.</p>'
    ),
    'archangel': (
        '<p>Archangel (Greek <em>archangelos</em>, "chief angel") is the highest rank in the angelic hierarchy named in Scripture. The New Testament uses the word only twice, and only one archangel is explicitly named: <em>"Yet Michael the archangel, when contending with the devil he disputed about the body of Moses, durst not bring against him a railing accusation"</em> (<em>Jude 9</em>). The voice of the archangel will accompany the trumpet of God at Christ’s descent and the resurrection of believers: <em>"For the Lord himself shall descend from heaven with a shout, with the voice of the archangel, and with the trump of God"</em> (<em>1 Thessalonians 4:16</em>). Apocryphal tradition speculates Gabriel, Raphael, Uriel; Scripture is restrained. One archangel is named.</p>'
    ),
    'barn': (
        '<p>A barn is the storage building for harvested grain. Scripture knows two kinds. First, the <em>wise barn</em> — the patient farmer’s ordinary tool, holding the increase against future need. <em>"The slothful man saith, There is a lion in the way"</em>; the wise gather. Christ’s harvest parable promises: <em>"Gather the wheat into my barn"</em> (<em>Matthew 13:30</em>). Second, the <em>foolish barn</em> — the rich man’s idol: <em>"I will pull down my barns, and build greater; and there will I bestow all my fruits and my goods. And I will say to my soul, Soul, thou hast much goods laid up for many years; take thine ease, eat, drink, and be merry"</em> (<em>Luke 12:18-20</em>). The Lord called him fool. Same barn; different soul.</p>'
    ),
    'beatitude-4': (
        '<p>The fourth Beatitude of Christ’s Sermon on the Mount: <em>"Blessed are they which do hunger and thirst after righteousness: for they shall be filled"</em> (<em>Matthew 5:6</em>). The intensity of the appetite metaphor matters. Christ is not commending casual interest in righteousness, mild approval of moral standards, or general religious sentimentality. He is describing <em>desperate</em> appetite — the hunger of the starving man, the thirst of the dying traveler. The promise of being <em>"filled"</em> (Greek <em>chortazō</em>, the same word used of the four thousand and five thousand fed to satisfaction) is Christ’s personal commitment: He will not leave the hungry-after-righteousness empty. The Christian who is no longer hungry has stopped pursuing the right meal.</p>'
    ),
    'blind': (
        '<p>"Blind," in Scripture, is physical inability to see — and a recurring metaphor for spiritual incapacity. The two meanings interlock. Isaiah prophesied of the Messiah: <em>"Then the eyes of the blind shall be opened, and the ears of the deaf shall be unstopped"</em> (<em>Isaiah 35:5</em>); the Gospels record Christ doing it repeatedly — Bartimaeus (<em>Mark 10:46-52</em>), the man born blind (<em>John 9</em>), the blind men outside Jericho (<em>Matthew 20:30-34</em>). Paul was struck physically blind on the Damascus road and given new sight three days later (<em>Acts 9:8-18</em>). But the more deadly variety is spiritual: <em>"Let them alone: they be blind leaders of the blind. And if the blind lead the blind, both shall fall into the ditch"</em> (<em>Matthew 15:14</em>). Only the Light gives sight.</p>'
    ),
    'boaz-redeemer': (
        '<p>Boaz was a wealthy landowner of Bethlehem during the period of the judges, and a kinsman of Naomi’s deceased husband Elimelech. When Ruth the Moabitess gleaned in his field, he treated her with extraordinary kindness — instructing his reapers to leave handfuls of purpose, and inviting her to eat at his table (<em>Ruth 2</em>). At Naomi’s direction Ruth pressed the claim at the threshing-floor (ch. 3), and Boaz at the city gate redeemed Elimelech’s land and married Ruth as <em>goel</em> (kinsman-redeemer, ch. 4). Their son Obed became the grandfather of King David. Boaz stands in Christ’s royal genealogy (<em>Matthew 1:5</em>) — and is one of Scripture’s clearest typological pictures of the greater Kinsman-Redeemer who buys back the Gentile bride.</p>'
    ),
    'camel': (
        '<p>The camel is the large hump-backed desert ruminant — essential to commerce and patriarchal travel across the ancient Near East, the great cargo-bearer of the trade routes. In Scripture it appears as the wealth-marker of Abraham (<em>Genesis 12:16; 24</em>), Job (3,000 camels — <em>Job 1:3</em>), and Eastern kings; it traditionally bore the Magi’s caravan to Bethlehem (<em>Matthew 2</em>). Christ uses the camel in two of His sharpest hyperboles. <em>"Ye blind guides, which strain at a gnat, and swallow a camel"</em> (<em>Matthew 23:24</em>) — Pharisaical scruple over trivia while swallowing scandal. And: <em>"It is easier for a camel to go through the eye of a needle, than for a rich man to enter into the kingdom of God"</em> (<em>Matthew 19:24</em>).</p>'
    ),
    'canticle': (
        '<p>A canticle is a Scripture-text song other than the Psalms, used in liturgical worship. Old Testament canticles include the Song of Moses after the Red Sea (<em>Exodus 15</em>), the Song of Hannah after Samuel’s birth (<em>1 Samuel 2</em>), the Song of Habakkuk closing his prophecy (<em>Habakkuk 3</em>), and the Song of Deborah (<em>Judges 5</em>). New Testament canticles, all from Luke 1-2, are the church’s most singable: the <em>Magnificat</em> of Mary (<em>Luke 1:46-55</em>), the <em>Benedictus</em> of Zechariah (<em>Luke 1:67-79</em>), the <em>Nunc Dimittis</em> of Simeon (<em>Luke 2:29-32</em>), and the <em>Gloria in Excelsis</em> of the angels (<em>Luke 2:14</em>). Reformed worship traditions retain them in metrical settings.</p>'
    ),
    'da-bomb': (
        '<p>"Da bomb" — late-90s Gen-X-coded superlative — names something judged the very best in a category: <em>"this restaurant is da bomb."</em> Era-stamped slang. The Christian observation is the same as for any superlative: superlatives reveal the speaker’s hierarchy of value. What you call <em>da bomb</em> tells the world (and yourself) what you actually treasure. <em>"For where your treasure is, there will your heart be also"</em> (<em>Matthew 6:21</em>). The slang itself is harmless; the audit it invites is real. If a man’s superlatives stack consistently on food, sports, gear, and entertainment — and never on Christ, His church, or His Word — the man has revealed his actual hierarchy. Reorder it.</p>'
    ),
    'doctrine-discovery': (
        '<p>The "Doctrine of Discovery" was a series of fifteenth- and sixteenth-century papal bulls (and English Crown extensions) by which Christian European nations claimed legal-theological warrant to seize lands inhabited by non-Christian peoples in the New World and elsewhere. It has no biblical basis. Scripture teaches God <em>"hath made of one blood all nations of men for to dwell on all the face of the earth, and hath determined the times before appointed, and the bounds of their habitation"</em> (<em>Acts 17:26</em>). In Christ <em>"there is neither Jew nor Greek"</em> (<em>Galatians 3:28</em>). The Great Commission commands making disciples of all nations (<em>Matthew 28:19</em>) — not conquering or dispossessing them. The Doctrine of Discovery was a perversion of Christianity used to justify imperial ambition.</p>'
    ),
    'duty-biblical': (
        '<p>Duty in Scripture is what one owes by virtue of position and relation — and it is a heavier word than modern English usually allows. Solomon closes Ecclesiastes: <em>"Let us hear the conclusion of the whole matter: Fear God, and keep his commandments: for this is the whole duty of man"</em> (<em>Ecclesiastes 12:13</em>). Christ teaches the unprofitable-servant posture: <em>"So likewise ye, when ye shall have done all those things which are commanded you, say, We are unprofitable servants: we have done that which was our duty to do"</em> (<em>Luke 17:10</em>). Christian duty is debt acknowledged and paid — not earning grace, but living out the obligations grace assigns. <em>"Owe no man any thing, but to love one another"</em> (<em>Romans 13:8</em>).</p>'
    ),
    'el-elyon': (
        '<p><em>El Elyon</em> (אֵל עֶלְיוֹן) — "God Most High" — is the divine name emphasizing God’s supreme rank above all rulers, gods, and powers — the One whose throne is above every throne. Melchizedek the priest-king of Salem first uses the name to Abraham: <em>"Blessed be Abram of the most high God, possessor of heaven and earth"</em> (<em>Genesis 14:19</em>). Abraham himself adopts it: <em>"I have lift up mine hand unto the LORD, the most high God"</em> (<em>14:22</em>). David sings it (<em>Psalm 7:17; 9:2; 47:2; 78:35</em>). Daniel uses it before Nebuchadnezzar to declare the political theology of the whole book: <em>"the most High ruleth in the kingdom of men, and giveth it to whomsoever he will"</em> (<em>Daniel 4:25, 32</em>).</p>'
    ),
    'exemptionism': (
        '<p>"Exemptionism" names the implicit assumption that some persons — by office, race, wealth, or charisma — are exempt from God’s moral law. Scripture refuses the premise. <em>"For there is no respect of persons with God"</em> (<em>Romans 2:11</em>; cf. <em>Acts 10:34; Ephesians 6:9</em>). David was confronted and judged despite being God’s anointed king (<em>2 Samuel 12:7-13</em>). Priests who violated God’s law were judged more severely, not less (<em>Malachi 2:1-9</em>). <em>"All have sinned, and come short of the glory of God"</em> (<em>Romans 3:23</em>). No celebrity Christian, no famous pastor, no political ally is exempt. The same standard runs through every office. Christian men must be alert to exemptionist instincts in themselves — and refuse them.</p>'
    ),
    'formation-biblical': (
        '<p>Formation is the ordered shape of a body — military or ecclesial — and the deliberate discipline that produces it. Paul speaks of <em>"Christ being formed in you"</em> (<em>Galatians 4:19</em>) — the apostle in labor-pains for the church until the Lord’s shape is visible in the saints. He also names the goal: <em>"for whom he did foreknow, he also did predestinate to be conformed to the image of his Son"</em> (<em>Romans 8:29</em>). Christian spiritual formation is therefore not vague self-improvement; it is the long shaping by Word, Spirit, ordinary providence, and intentional discipline into the shape of Christ. It happens through Scripture, sacrament, prayer, fellowship, fasting, and trial. The saint does not produce the form; he submits to its making.</p>'
    ),
    'guest-room': (
        '<p>The guest room (Greek <em>kataluma</em>) is the household’s deliberately reserved space for the traveler, the visitor, the unexpected need. Scripture gives it heavy theological weight. The inn at Bethlehem had no <em>kataluma</em> available for Joseph and Mary on the night of Christ’s birth, so the Savior of the world was laid in a manger (<em>Luke 2:7</em>). Christ held the Last Supper in another household’s <em>kataluma</em>: <em>"The Master saith, Where is the guestchamber [kataluma], where I shall eat the passover with my disciples?"</em> (<em>Mark 14:14; Luke 22:11</em>). Whether the household’s guest room is open or closed has literally shaped redemptive history. Keep yours open.</p>'
    ),
    'heart-of-king': (
        '<p><em>Proverbs 21:1</em> is the Old Testament’s bedrock statement of YHWH’s sovereignty over rulers: <em>"The king’s heart is in the hand of the LORD, as the rivers of water: he turneth it whithersoever he will."</em> Even the highest human authority is directable by YHWH like water in irrigation channels — channeled where the Owner of the field decides. The verse is the Old Testament foundation for the New Testament command to pray for rulers: <em>"I exhort therefore, that, first of all, supplications, prayers, intercessions, and giving of thanks, be made for all men; for kings, and for all that are in authority"</em> (<em>1 Timothy 2:1-2</em>). The Christian does not flatter or fear kings; he prays for them.</p>'
    ),
    'ink': (
        '<p>Ink is the dark fluid used by ancient scribes to write on papyrus, parchment, leather, and pottery — usually compounded from soot, gum, and water. Scripture names it in the writing of inspired correspondence: Jeremiah’s scribe Baruch wrote with ink at the prophet’s dictation (<em>Jeremiah 36:18</em>). John writes: <em>"Having many things to write unto you, I would not write with paper and ink"</em> (<em>2 John 12</em>; cf. <em>3 John 13</em>). Paul’s most theological use of ink is in <em>2 Corinthians 3:3</em>: the Spirit’s preferred metaphor for the New Covenant — <em>"written not with ink, but with the Spirit of the living God; not in tables of stone, but in fleshy tables of the heart."</em> The ink fades; the Spirit-script does not.</p>'
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
