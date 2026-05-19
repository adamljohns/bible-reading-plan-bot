#!/usr/bin/env python3
"""Batch 49 — expand 25 more entries from the 60-70 word bucket.

Targets: divine names, NT figures, doctrines, parables, OT figures,
hermeneutics, sacraments, body imagery, and slang reframes.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'jehovah-shalom': (
        '<p><em>Jehovah-Shalom</em> (יְהוָה שָׁלוֹם) — "the LORD is peace" — is the covenant name given by Gideon to the altar he built at Ophrah after the Angel of the LORD revealed Himself and reassured him: <em>"Peace be unto thee; fear not: thou shalt not die. Then Gideon built an altar there unto the LORD, and called it Jehovahshalom"</em> (<em>Judges 6:23-24</em>). <em>Shalom</em> is not the absence of conflict; it is wholeness, integrity, restoration to right order under God. Christ Himself is the incarnate <em>Jehovah-Shalom</em>: <em>"For he is our peace, who hath made both one, and hath broken down the middle wall of partition between us"</em> (<em>Ephesians 2:14</em>). In Him hostility ceases — between sinner and God, between Jew and Gentile, between brothers.</p>'
    ),
    'lily': (
        '<p>The lily is a wildflower of Galilee’s hillsides — and in Scripture, the figure of three things. First, God’s effortless provision: <em>"Consider the lilies of the field, how they grow; they toil not, neither do they spin"</em> (<em>Matthew 6:28</em>; <em>Luke 12:27</em>). Second, God’s glory in design: <em>"yet I say unto you, That even Solomon in all his glory was not arrayed like one of these"</em> (<em>Matthew 6:29</em>). Third, Christ Himself in the Song of Solomon: <em>"I am the rose of Sharon, and the lily of the valleys. As the lily among thorns, so is my love among the daughters"</em> (<em>Song 2:1-2</em>). The hillside lily preaches: dressed lavishly without effort, replaced quickly, every wildflower a small sermon.</p>'
    ),
    'liturgical-year': (
        '<p>The liturgical year is the annual cycle of seasons and feasts by which the historic Church orders her worship around the life of Christ: Advent (waiting for the King), Christmas (His incarnation), Epiphany (His manifestation to the nations), Lent (40 days of repentance and preparation), Holy Week (His passion), Easter (His resurrection), Pentecost (the Spirit poured out), Trinity Sunday (the triune God), and the long stretch of Ordinary Time / Trinity Season that catechizes the Christian life. Old Testament Israel had its own annual cycle (Passover, Weeks, Tabernacles, Day of Atonement). Reformed traditions vary in adoption — some keep the major festivals, some keep the entire calendar, some keep only the Lord’s Day.</p>'
    ),
    'manaen': (
        '<p>Manaen was an aristocrat by upbringing — raised at the Herodian court as the foster-brother (Greek <em>syntrophos</em>, literally "raised together") or close companion of Herod Antipas, the same Herod who beheaded John the Baptist. By the time of <em>Acts 13:1</em>, however, Manaen is found teaching in the church at Antioch alongside Barnabas, Simeon called Niger, Lucius of Cyrene, and Saul: <em>"Now there were in the church that was at Antioch certain prophets and teachers... and Manaen, which had been brought up with Herod the tetrarch."</em> The Spirit set apart Barnabas and Saul for the first missionary journey out of this very meeting. Manaen is a cameo reminder that the gospel reaches even royal households.</p>'
    ),
    'mighty-god': (
        '<p>"Mighty God" — Hebrew <em>El Gibbor</em> — is one of the great Messianic names of <em>Isaiah 9:6</em>: <em>"For unto us a child is born, unto us a son is given... and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace."</em> The same name is used of God Himself just two chapters later: <em>"the remnant shall return... unto the mighty God"</em> (<em>Isaiah 10:21</em>; cf. <em>Jeremiah 32:18</em>). Isaiah is unambiguous: the Messiah is not a powerful man or even a high angel — He is <em>El Gibbor</em>, God Himself in warrior strength, born to fight the dragon and rescue the bride. The deity of Christ is anchored in the Old Testament, not invented by the New.</p>'
    ),
    'motherhood-biblical': (
        '<p>Biblical motherhood is the state and office of being a mother — with its dignity, formative power, and recognized weight before God. Eve was named <em>"the mother of all living"</em> (<em>Genesis 3:20</em>). The matriarchs Sarah, Rebekah, Rachel, Leah, and Hannah are named with extended attention. Hannah’s prayer and song shape <em>1 Samuel 1-2</em>; Mary the mother of Christ is called <em>"blessed among women"</em> (<em>Luke 1:42</em>); Elizabeth, Lois, Eunice (Timothy’s mother and grandmother), and Mary the mother of Mark all appear by name. <em>"Train up a child in the way he should go"</em> (<em>Proverbs 22:6</em>) is largely maternal work. Modern feminism has degraded motherhood; Scripture has always exalted it as a high vocation.</p>'
    ),
    'only-begotten': (
        '<p>"Only begotten" is the KJV’s translation of the Greek <em>monogenēs</em>, used uniquely of Christ in John’s writings: <em>"And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth"</em> (<em>John 1:14; cf. 1:18; 3:16, 18; 1 John 4:9</em>). Some modern translations render <em>"one and only"</em> or <em>"unique"</em>; the older eternal-generation theology preserves <em>"only begotten"</em> to mark Christ’s distinct, eternal relationship to the Father. He is not <em>made</em> like creatures; He is <em>begotten</em> — eternally generated, of one substance with the Father, true God of true God (Nicene Creed). The doctrine guards His full deity and His personal distinction from the Father.</p>'
    ),
    'orchard': (
        '<p>An orchard is a planted area of fruit-bearing trees — the patient husbandman’s long-term project, requiring years of cultivation before serious yield. Scripture knows the orchard primarily as the picture of the saint’s long-form fruitfulness: <em>"And he shall be like a tree planted by the rivers of water, that bringeth forth his fruit in his season; his leaf also shall not wither; and whatsoever he doeth shall prosper"</em> (<em>Psalm 1:3</em>). <em>Jeremiah 17:7-8</em> repeats the image. The Song of Solomon’s spice-orchard names the bride’s beauty (<em>Song 4:13: "an orchard of pomegranates, with pleasant fruits"</em>). The Christian life is an orchard, not a sprint. Patience, water, and time produce the eventual harvest.</p>'
    ),
    'phoebe-deaconess': (
        '<p>Phoebe was a believer of the church at Cenchreae, the eastern port of Corinth — and the woman Paul almost certainly entrusted with carrying his letter to the Romans across the Mediterranean. Paul commends her: <em>"I commend unto you Phebe our sister, which is a servant [<em>diakonos</em>] of the church which is at Cenchrea: That ye receive her in the Lord, as becometh saints, and that ye assist her in whatsoever business she hath need of you: for she hath been a succourer [<em>prostatis</em>, patroness] of many, and of myself also"</em> (<em>Romans 16:1-2</em>). The Greek <em>prostatis</em> suggests significant social standing — wealthy patroness, likely the funder of Paul’s mission. The deepest theological letter in the New Testament was delivered by a Greek woman.</p>'
    ),
    'priesthood': (
        '<p>Priesthood is the office of those set apart to mediate between God and people — offering sacrifice, teaching the law, blessing the people, and interceding for them. The Aaronic priesthood (Levitical) was instituted at Sinai (<em>Exodus 28-29; Leviticus 8</em>), restricted to Aaron’s descendants, and ran from Moses to the destruction of the second temple in AD 70. Christ’s eternal high priesthood after the order of Melchizedek — sinless, eternal, sufficient — fulfills and ends the Aaronic order (<em>Hebrews 7</em>). And all believers in Christ now form a royal priesthood under Him: <em>"Ye also, as lively stones, are built up a spiritual house, an holy priesthood, to offer up spiritual sacrifices"</em> (<em>1 Peter 2:5, 9; Revelation 1:6; 5:10</em>). Every Christian is a priest.</p>'
    ),
    'prophetic-symbol': (
        '<p>A prophetic symbol is an enacted sign — the prophet’s body or property pressed into service to embody the message visibly. Hosea married Gomer the harlot to dramatize Israel’s adultery against YHWH (<em>Hosea 1-3</em>). Isaiah walked naked and barefoot for three years to dramatize Egypt’s coming exile (<em>Isaiah 20:2-4</em>). Jeremiah broke a potter’s vessel before the elders to dramatize Jerusalem’s breaking (<em>Jeremiah 19</em>) and wore a wooden yoke (<em>Jeremiah 27</em>). Ezekiel lay 390 days on his left side and 40 on his right (<em>Ezekiel 4:4-8</em>), shaved his head and divided the hair into thirds (<em>5:1-4</em>), and refused mourning at his wife’s death (<em>24:15-24</em>). The prophet’s body was the message.</p>'
    ),
    'put-on-christ': (
        '<p>"Put on Christ" is both a Pauline command and a Pauline indicative. The command: <em>"But put ye on the Lord Jesus Christ, and make not provision for the flesh, to fulfil the lusts thereof"</em> (<em>Romans 13:14</em>). The indicative: <em>"For as many of you as have been baptized into Christ have put on Christ"</em> (<em>Galatians 3:27</em>). The image is of <em>clothing</em> oneself with Christ — His righteousness covers the saint, His character is to be visibly worn, His name is the saint’s outerwear before the world. The saint puts on Christ at baptism (positionally) and continues to put Him on daily (practically) — like dressing in the morning. Christian men should be visibly clothed in Christ before they leave the house.</p>'
    ),
    'raise-the-roof': (
        '<p>"Raise the roof" is the Gen-X-era celebratory gesture and verbal phrase meaning to celebrate enthusiastically — common at sporting events, parties, and concerts of the late 1990s and early 2000s. The hand-gesture (palms up, pushing the roof upward) accompanied it. The Christian observation: celebration is good — Ecclesiastes 3:4 names <em>"a time to laugh... and a time to dance"</em>; David danced before the ark <em>"with all his might"</em> (<em>2 Samuel 6:14</em>); the prodigal’s father killed the fatted calf and made merry (<em>Luke 15:23-24</em>). The Christian household should know how to celebrate hard — at weddings, baptisms, restorations, harvests. Just sanctify the celebrations: raise the roof for the LORD.</p>'
    ),
    'sealing': (
        '<p>Sealing is the act of impressing a signet upon a document, deed, or person to authenticate and secure it. Ancient seals (engraved cylinders or rings) pressed into wax or clay legally bound and protected what they marked. In the New Testament, every believer is sealed with the Holy Spirit at conversion: <em>"In whom also after that ye believed, ye were sealed with that holy Spirit of promise, Which is the earnest of our inheritance until the redemption of the purchased possession"</em> (<em>Ephesians 1:13-14; cf. 4:30; 2 Corinthians 1:21-22</em>). God’s own signet is impressed upon the believer as proof of ownership and pledge of consummation. The seal is the Spirit; the Spirit is the seal. Indelible.</p>'
    ),
    'silent-years': (
        '<p>The Silent Years are the roughly four centuries between Malachi’s last words (c. 430 BC) and Gabriel’s announcement to Zechariah in the temple (c. 5 BC) — the so-called "intertestamental period" during which no canonical prophet of Israel spoke. God was not absent from history during this stretch (the books of Maccabees, Esther’s later setting, Daniel’s prophetic timing, the rise and fall of Persia, the conquest of Alexander, the Maccabean revolt, the rise of Rome all unfolded). But the prophetic voice ceased — until John the Baptist suddenly broke the silence in the wilderness preaching repentance and pointing to the Lamb of God. The longest silence of the canon was followed by the loudest voice.</p>'
    ),
    'solomon-fall': (
        '<p>Solomon’s fall is the tragedy of <em>1 Kings 11</em>. The wisest man in the world — who had built the temple, ruled in unparalleled splendor, and prayed at the temple’s dedication — failed at the very point his father David had warned him about: covenant faithfulness. <em>"But king Solomon loved many strange women, together with the daughter of Pharaoh, women of the Moabites, Ammonites, Edomites, Zidonians, and Hittites"</em> (<em>11:1</em>). Seven hundred wives and three hundred concubines drew his heart away. He built high places for Chemosh of Moab and Molech of Ammon. The LORD announced the kingdom would be torn in two — and Jeroboam’s revolt followed under Solomon’s son. Wisdom unkept does not save its keeper.</p>'
    ),
    'sower': (
        '<p>The Sower is the Lord’s opening parable in <em>Matthew 13:3-23; Mark 4:3-20; Luke 8:5-15</em>: a sower casts the same seed (the Word of God) on four soils — the wayside (the path), the stony ground, the thorny ground, and the good ground. Three out of four soils fail: the birds devour, the sun scorches, the thorns choke. Only the good ground brings forth fruit — some thirty, some sixty, some a hundredfold. Christ Himself interprets the parable to His disciples privately and says: <em>"Know ye not this parable? and how then will ye know all parables?"</em> (<em>Mark 4:13</em>). The parable of the Sower is the master key to all His other parables — the diagnostic for hearing.</p>'
    ),
    'store-of-grain': (
        '<p>A store of grain is the accumulated provision laid up against future need. Joseph’s seven-year grain-storage in Egypt (<em>Genesis 41:35-49</em>) saved many lives — including his own family — when the seven years of famine came. The ant of Proverbs stores in summer for winter: <em>"Go to the ant, thou sluggard; consider her ways, and be wise: Which having no guide, overseer, or ruler, Provideth her meat in the summer, and gathereth her food in the harvest"</em> (<em>Proverbs 6:6-8</em>). Christ’s parable of the rich fool warns against treating barns as the soul’s security (<em>Luke 12:16-21</em>). Both lessons stand: <em>store</em> wisely, but do not <em>trust</em> the store. The Owner of the harvest is the LORD.</p>'
    ),
    'thus-saith-lord': (
        '<p>"Thus saith the LORD" is the prophet’s standard formula introducing a direct word from God. It appears more than four hundred times in the Old Testament prophetic literature. It is the linguistic seal that distinguishes the prophet’s own counsel from God’s spoken word: the prophet may have opinions, but when he says <em>"Thus saith the LORD"</em>, he claims to be conveying not commentary but oracle. <em>"For the prophecy came not in old time by the will of man: but holy men of God spake as they were moved by the Holy Ghost"</em> (<em>2 Peter 1:21</em>). False prophets used the formula falsely (<em>Jeremiah 14:14; 23:25-32</em>); true prophets used it under the burden of divine commission. Modern preachers should be slower to deploy it than they often are.</p>'
    ),
    'tongue': (
        '<p>The tongue is the organ of speech — and in Scripture it is the most-warned-about body part in the New Testament. James devotes nearly a whole chapter to its disproportionate damage: <em>"Even so the tongue is a little member, and boasteth great things. Behold, how great a matter a little fire kindleth!"</em> (<em>James 3:5-6</em>). Proverbs warns of its lethal power: <em>"Death and life are in the power of the tongue: and they that love it shall eat the fruit thereof"</em> (<em>18:21</em>). Christ says we will give account for every idle word at the day of judgment (<em>Matthew 12:36-37</em>). The tongue can bless and curse (<em>James 3:9</em>) — but Christian men must train it to bless.</p>'
    ),
    'victory': (
        '<p>Victory in Scripture is conquest over enemies — especially over sin, death, and the devil — through Christ. <em>"This is the victory that overcometh the world, even our faith"</em> (<em>1 John 5:4</em>). Christ defeated the principalities at the cross: <em>"And having spoiled principalities and powers, he made a shew of them openly, triumphing over them in it"</em> (<em>Colossians 2:15</em>). He defeated death at the resurrection: <em>"O death, where is thy sting? O grave, where is thy victory? The sting of death is sin; and the strength of sin is the law. But thanks be to God, which giveth us the victory through our Lord Jesus Christ"</em> (<em>1 Corinthians 15:55-57</em>). The Christian fights from victory already won.</p>'
    ),
    'way-truth-life': (
        '<p>"The way, the truth, and the life" is Christ’s threefold predicate-claim in <em>John 14:6</em>: <em>"I am the way, the truth, and the life: no man cometh unto the Father, but by me."</em> The triple-claim captures three aspects of His mediation. He is the <em>way</em> of access — the path to the Father, the only road open. He is the <em>truth</em> — the reliable content corresponding to reality, the standard against which every claim is measured. He is the <em>life</em> — the very source of spiritual and eternal vitality, in whom the dead are made alive. And the exclusivity is plain: <em>"no man cometh unto the Father, but by me."</em> Religious pluralism stumbles on this verse.</p>'
    ),
    'absolute': (
        '<p>"Absolute" describes that which is unconditioned, complete in itself, and not dependent on anything else for its existence or definition. In Christian theology only God is absolute: only He is <em>necessary</em>; everything else is <em>contingent</em> — dependent on Him for being, sustenance, and meaning. <em>"In him we live, and move, and have our being"</em> (<em>Acts 17:28</em>); <em>"by him all things consist"</em> (<em>Colossians 1:17</em>). Moral absolutes exist because they are rooted in God’s unchanging character — not arbitrary preferences but His own nature expressed in law. The modern denial of absolutes is therefore not just a philosophical position; it is a denial of the God who is. The Christian holds absolutes precisely because he confesses an absolute God.</p>'
    ),
    'achan': (
        '<p>Achan was the Israelite of the tribe of Judah who took devoted spoil from Jericho — a Babylonian garment, two hundred shekels of silver, and a wedge of gold of fifty shekels — directly against the LORD’s <em>herem</em>-ban which had devoted Jericho’s wealth to YHWH (<em>Joshua 6:18-19; 7</em>). His secret sin caused Israel’s humiliating defeat at the smaller city of Ai. After Joshua sought the LORD and was directed to identify the offender by lot, Achan was singled out by tribe, family, household, and finally by name. He confessed: <em>"I saw... I coveted... I took... I hid"</em> (<em>7:21</em>). He and his household were stoned and burned in the Valley of Achor. Hidden sin in one corrupts the whole camp.</p>'
    ),
    'apostolic-hermeneutic': (
        '<p>The Apostolic Hermeneutic is the interpretive method modeled by the apostles in their use of the Old Testament throughout the New. It is <em>christocentric</em> (every Old Testament passage finds its center in Christ), <em>redemptive-historical</em> (the canon traces one unfolding storyline), <em>typological</em> (Old Testament persons, events, and institutions prefigure Christ and the church), and <em>confident</em> — Peter at Pentecost: <em>"this is that which was spoken by the prophet Joel"</em> (<em>Acts 2:16</em>). The apostles read the Old Testament as a Christ-saturated book and applied it to the New-Covenant church without hesitation. The Reformed tradition has labored to recover this method, refusing both flat literalism and uncontrolled allegory. The apostles read Scripture the way Scripture is to be read.</p>'
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
