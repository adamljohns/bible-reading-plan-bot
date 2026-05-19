#!/usr/bin/env python3
"""Batch 53 — expand 25 more entries from the 60-70 word bucket.

Targets: anatomy/imagery, hermeneutics, Reformed doctrines (TULIP),
theologians (J. C. Ryle), Lord's prayer & Christ's teaching,
NT figures, sacraments, and numerology.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'fingers': (
        '<p>The fingers are the articulate digits of the hand — and in Scripture they appear in some of the most striking moments of divine action. God wrote the Decalogue with His own finger: <em>"two tables of testimony, tables of stone, written with the finger of God"</em> (<em>Exodus 31:18; 32:16; Deuteronomy 9:10</em>). Christ cast out demons with the same finger: <em>"if I with the finger of God cast out devils"</em> (<em>Luke 11:20</em>). He wrote on the ground with His finger when the adulteress was brought before Him (<em>John 8:6, 8</em>). The mysterious hand wrote on Belshazzar’s wall: <em>"In the same hour came forth fingers of a man’s hand, and wrote"</em> (<em>Daniel 5:5</em>). Divine fingers write what divine words have said.</p>'
    ),
    'fulfillment': (
        '<p>Fulfillment is the bringing-to-completion of an Old Testament prophecy, type, promise, or shadow in the person and work of Jesus Christ. It is the New Testament writers’ favorite verb when describing why a particular event happened: <em>"that it might be fulfilled which was spoken by the prophet"</em> appears repeatedly through Matthew especially (<em>1:22; 2:15, 17, 23; 4:14; 8:17; 12:17; 13:14, 35; 21:4; 27:9</em>). Christ Himself summarized His mission: <em>"Think not that I am come to destroy the law, or the prophets: I am not come to destroy, but to fulfil"</em> (<em>Matthew 5:17</em>). The Old Testament expects; the New Testament fulfills. The whole Bible is one story, and its central character keeps every appointment.</p>'
    ),
    'hand-of-the-lord': (
        '<p>"The hand of the LORD" is the prophetic idiom for the LORD’s active power resting on a person — especially for prophetic vision, commission, or empowering. Ezekiel’s repeated formula: <em>"the hand of the LORD was there upon me"</em> introduces vision after vision (<em>Ezekiel 1:3; 3:14, 22; 8:1; 33:22; 37:1; 40:1</em>). Elijah ran before Ahab’s chariot <em>"and the hand of the LORD was on Elijah"</em> (<em>1 Kings 18:46</em>). Ezra fasted with confidence <em>"according to the good hand of his God upon him"</em> (<em>Ezra 7:9</em>). At Antioch <em>"the hand of the Lord was with them: and a great number believed"</em> (<em>Acts 11:21</em>). When the hand is upon a man, what he does has weight behind it.</p>'
    ),
    'last-enemy': (
        '<p>"The last enemy that shall be destroyed is death"</em> (<em>1 Corinthians 15:26</em>). Paul names death the final enemy of God’s redemptive purposes — the climax of the curse, the universal consequence of Adam’s fall, the unbeaten foe that mocks every human victory. Christ has already defeated death in principle at the resurrection: <em>"O death, where is thy sting? O grave, where is thy victory? The sting of death is sin; and the strength of sin is the law. But thanks be to God, which giveth us the victory through our Lord Jesus Christ"</em> (<em>vv. 55-57</em>). The final execution of the verdict awaits the resurrection of the dead. <em>"And there shall be no more death"</em> (<em>Revelation 21:4</em>). The last enemy is on death row.</p>'
    ),
    'let-your-light-shine': (
        '<p>"Let your light so shine" is Christ’s command in the Sermon on the Mount, immediately following the salt-of-the-earth and city-on-a-hill sayings: <em>"Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven"</em> (<em>Matthew 5:16</em>). Notice the careful telos. The light shines so that men see <em>good works</em>, not just the disciple. The end is the Father’s glory, not the disciple’s reputation. The verse is therefore the answer to both the secret-religion-only error (which hides the light under a bushel, <em>v. 15</em>) and the showmanship error (the next chapter’s warning against doing alms before men, <em>6:1</em>). Visible enough to point to the Father; never to the self.</p>'
    ),
    'marvel': (
        '<p>To <em>marvel</em> is to be struck with wonder — and in Scripture the verb describes a wide range of holy astonishment. Crowds marvel at Christ’s teaching: <em>"And the people were astonished at his doctrine"</em> (<em>Matthew 7:28</em>; <em>22:33</em>). They marvel at His miracles: <em>"the multitude wondered, when they saw the dumb to speak"</em> (<em>15:31</em>). Christ Himself marvels — only twice in the Gospels. At the centurion’s great faith: <em>"I have not found so great faith, no, not in Israel"</em> (<em>Matthew 8:10</em>). And, sobering, at the unbelief of Nazareth: <em>"And he marvelled because of their unbelief"</em> (<em>Mark 6:6</em>). The Lord can be astonished both ways. Be one He marvels over for the right reason.</p>'
    ),
    'naked-came-naked-return': (
        '<p>"Naked came I, and naked shall I return" is Job’s worship-confession after the catastrophe of <em>Job 1</em> — the day his oxen were carried off, his sheep burned, his camels stolen, his servants killed, and finally a whirlwind crushed the house where his ten children were feasting. He rent his mantle, shaved his head, fell on the ground, and worshipped: <em>"Naked came I out of my mother’s womb, and naked shall I return thither: the LORD gave, and the LORD hath taken away; blessed be the name of the LORD. In all this Job sinned not, nor charged God foolishly"</em> (<em>Job 1:21-22</em>). Paul echoes the verse in <em>1 Timothy 6:7</em>. Worship under loss is one of the highest forms of worship.</p>'
    ),
    'old-covenant': (
        '<p>The Old Covenant is the Mosaic-Sinaitic covenant — called <em>"old"</em> in <em>2 Corinthians 3:14</em> precisely in light of the New Covenant instituted by Christ’s blood at the Last Supper. The Old Covenant was <em>"holy, and just, and good"</em> (<em>Romans 7:12</em>) but unable to give life: <em>"If there had been a law given which could have given life, verily righteousness should have been by the law"</em> (<em>Galatians 3:21</em>). It functioned as a tutor leading to Christ (<em>Galatians 3:24-25</em>) — exposing sin, restraining wickedness, prefiguring the Savior. Christ fulfilled it, did not destroy it (<em>Matthew 5:17</em>). The New Covenant in His blood does what the Old could not: writes the law on hearts, gives the Spirit, secures eternal forgiveness.</p>'
    ),
    'passover-night': (
        '<p>Passover Night was the night of YHWH’s tenth and final plague upon Egypt — the death of every firstborn man and beast — while houses marked with the blood of an unblemished lamb on doorposts and lintel were <em>"passed over"</em> (<em>Exodus 12:1-30</em>). Inside each marked house the family ate the lamb roasted, with unleavened bread and bitter herbs, loins girded, sandals on, staff in hand — ready to march. <em>"And when I see the blood, I will pass over you, and the plague shall not be upon you to destroy you"</em> (<em>12:13</em>). The next morning Israel marched out of Egypt. The night is the defining act of Israel’s redemption — and the type of Christ the Lamb whose blood marks the believer’s doorpost.</p>'
    ),
    'pouring-baptism': (
        '<p>Pouring (affusion) is the mode of baptism in which water is poured over the candidate’s head — distinct from immersion (going completely under) and aspersion (sprinkling). Its biblical warrant is the outpouring imagery of the Spirit’s coming, which baptism signifies: <em>"And it shall come to pass afterward, that I will pour out my spirit upon all flesh"</em> (<em>Joel 2:28</em>); Peter at Pentecost: <em>"this Jesus hath God raised up, whereof we all are witnesses... he hath shed forth [<em>poured out</em>] this, which ye now see and hear"</em> (<em>Acts 2:32-33</em>). The Reformed and Presbyterian traditions have historically practiced pouring (or sprinkling) on this basis, especially for the baptism of infant covenant children. The mode varies; the meaning of union with Christ does not.</p>'
    ),
    'progressive-covenantalism': (
        '<p>Progressive Covenantalism is the modern theological position (Stephen Wellum and Peter Gentry, <em>Kingdom through Covenant</em>, 2012; <em>God’s Kingdom through God’s Covenants</em>, 2015) that traces the unfolding biblical covenants <em>progressively</em> to their climax in Christ’s New Covenant. The view sits as a middle path between classical covenant theology (one covenant of grace administered through successive epochs) and dispensationalism (sharply distinct programs for Israel and the church). Progressive Covenantalism emphasizes both continuity (one redemptive plan culminating in Christ) and discontinuity (the New Covenant is genuinely new, not just a renewed Mosaic covenant). It generally aligns with Baptist convictions about the church and covenant signs. Reformed paedobaptists critique it as understating Old-Covenant-New-Covenant continuity.</p>'
    ),
    'promise-fulfillment': (
        '<p>Promise-Fulfillment hermeneutics traces how Old Testament promises — covenant pledges, prophecies, types, longings, hopes — find their answer in Christ’s person and work. Paul’s great summary: <em>"For all the promises of God in him are yea, and in him Amen, unto the glory of God by us"</em> (<em>2 Corinthians 1:20</em>). Every covenant promise terminates on Christ as its fulfillment. Hebrews shows it at length: the priesthood, the sacrifices, the tabernacle, the Sabbath rest, the heavenly country promised to the patriarchs — all fulfilled, transformed, and consummated in Him. Promise-Fulfillment is the dominant Apostolic Hermeneutic; the apostles read the Old Testament as a vast tapestry of promises tied off in Christ. Christian preaching is largely a re-tracing of these threads.</p>'
    ),
    'promised-land': (
        '<p>The Promised Land is the land sworn by God to Abraham — <em>"Unto thy seed have I given this land, from the river of Egypt unto the great river, the river Euphrates"</em> (<em>Genesis 15:18-21; 12:7; 17:8</em>) — and inherited by Israel under Joshua through the Conquest. As biblical-theological motif, however, it expands beyond literal Canaan. Hebrews 11:13-16 names a heavenly country sought by the patriarchs: <em>"they desire a better country, that is, an heavenly"</em>. Christ in the Beatitudes promises that the meek shall inherit <em>"the earth"</em> (<em>Matthew 5:5; Psalm 37:11</em>) — restored, renewed, consummated. The final inheritance is the new heavens and new earth (<em>Revelation 21-22</em>). The Promised Land widens until it covers the redeemed cosmos.</p>'
    ),
    'robe': (
        '<p>A robe is a long, full-length outer garment of honor — and in Scripture it carries weight. The priest wore the blue robe with bells and pomegranates (<em>Exodus 28:31-35</em>). Joseph’s coat of many colors marked his father’s favoritism and provoked his brothers’ hatred (<em>Genesis 37:3-4</em>). The prodigal’s father called for <em>"the best robe"</em> to restore him to sonship (<em>Luke 15:22</em>). The high priest tore his robe at Christ’s confession — a forbidden act (<em>Matthew 26:65</em>). Christ was clothed in a scarlet (Matthew) or purple (Mark, John) robe in mockery before the crucifixion (<em>Matthew 27:28; Mark 15:17; John 19:2</em>). The redeemed in <em>Revelation 7:9</em> wear white robes <em>"washed in the blood of the Lamb"</em>.</p>'
    ),
    'ryle-jc': (
        '<p>J. C. Ryle (1816-1900) was the English evangelical Anglican who served as the first Bishop of Liverpool (1880-1900) and arguably the nineteenth century’s greatest plain-spoken Protestant preacher. Born to wealth, converted as a young man, ordained 1842, he wrote vigorously and simply for ordinary Christians. Major works: <em>Holiness</em> (1877, his most influential book), <em>Practical Religion</em>, <em>Knots Untied</em>, <em>Old Paths</em>, the seven-volume <em>Expository Thoughts on the Gospels</em>, and many pamphlets. His prose is direct, fearless, and pastoral. Famous lines: <em>"Holiness, holiness wanted, holiness needed, holiness preached, holiness insisted on, holiness daily aimed at, by very few"</em>; <em>"Sin rarely seems sin at its first beginnings."</em> J. I. Packer rediscovered Ryle for the twentieth century.</p>'
    ),
    'shema': (
        '<p>The Shema is the great Jewish confession from <em>Deuteronomy 6:4-9</em>, named from its opening Hebrew word <em>shema</em> ("hear"): <em>"Hear, O Israel: The LORD our God is one LORD: And thou shalt love the LORD thy God with all thine heart, and with all thy soul, and with all thy might. And these words, which I command thee this day, shall be in thine heart: And thou shalt teach them diligently unto thy children."</em> Recited twice daily by observant Jews (morning and evening), it is the most foundational Old Testament confession of monotheism and total love. Christ quoted it as <em>"the first commandment of all"</em> (<em>Mark 12:29-30</em>). Every Jewish-Christian convert grew up reciting it.</p>'
    ),
    'soldier': (
        '<p>A soldier is a man under military discipline and orders — and Scripture engages the office in multiple ways. The soldier is alternately the agent of governmental authority bearing the sword (<em>Romans 13:4</em>); the object of John the Baptist’s ethical instruction: <em>"Do violence to no man, neither accuse any falsely; and be content with your wages"</em> (<em>Luke 3:14</em>); the centurion of great faith Christ commended (<em>Matthew 8:5-13</em>); and the metaphor for the Christian life itself: <em>"Thou therefore endure hardness, as a good soldier of Jesus Christ. No man that warreth entangleth himself with the affairs of this life; that he may please him who hath chosen him to be a soldier"</em> (<em>2 Timothy 2:3-4</em>). The Christian is enlisted; he serves under colors; he obeys his Commander.</p>'
    ),
    'taking-every-thought': (
        '<p>"Bringing every thought into captivity" is Paul’s command in <em>2 Corinthians 10:3-5</em>, within his great metaphor of spiritual warfare: <em>"For though we walk in the flesh, we do not war after the flesh: (For the weapons of our warfare are not carnal, but mighty through God to the pulling down of strong holds;) Casting down imaginations, and every high thing that exalteth itself against the knowledge of God, and bringing into captivity every thought to the obedience of Christ."</em> The picture is a war of thoughts: the fortified positions of false philosophy and lying imagination are torn down, and every escaping thought is captured and led in chains to Christ’s obedience. The mind is the battlefield. Christian men do not just <em>have</em> thoughts; they <em>govern</em> them.</p>'
    ),
    'ten': (
        '<p>Ten, in Scripture, is the number of completeness in human or divine action — God’s number for finished sequence at the human scale. The LORD sent <em>ten plagues</em> on Egypt to break Pharaoh’s grip. He gave <em>Ten Commandments</em> at Sinai as the summary of His moral law. He called for the <em>tithe</em> (one-tenth) as the saint’s baseline giving. Christ spoke of <em>ten virgins</em> (<em>Matthew 25:1-13</em>), <em>ten lepers</em> (<em>Luke 17:11-19</em>), and <em>ten servants entrusted with pounds</em> (<em>Luke 19:12-27</em>). Genesis 5 lists <em>ten patriarchs</em> from Adam to Noah, and Genesis 11 lists <em>ten from Shem to Abraham</em>. Where you see ten in Scripture, the LORD is often signaling completed sequence — and inviting attention.</p>'
    ),
    'tertius': (
        '<p>Tertius was the amanuensis (professional secretary) who wrote down the epistle to the Romans at Paul’s dictation. The custom was common in antiquity: Paul dictated; Tertius wrote. The Latin name (literally "third") suggests a slave or freedman. Tertius inserts his own greeting near the close: <em>"I Tertius, who wrote this epistle, salute you in the Lord"</em> (<em>Romans 16:22</em>). The most theologically dense letter in the New Testament — Paul’s magnum opus expounding justification by faith, the doctrines of grace, and the future of Israel — was physically penned by a man whose entire biblical legacy is a single verse. Christian men should remember Tertius. The kingdom is built by countless co-laborers whose names appear once or never.</p>'
    ),
    'theft': (
        '<p>Theft is the taking of what is not one’s own — and the eighth commandment of the Decalogue forbids it absolutely: <em>"Thou shalt not steal"</em> (<em>Exodus 20:15; Deuteronomy 5:19</em>). In Scripture, theft includes stealing money, time, reputation, glory due to God, and goods. Paul names the cure: <em>"Let him that stole steal no more: but rather let him labour, working with his hands the thing which is good, that he may have to give to him that needeth"</em> (<em>Ephesians 4:28</em>). The repentance is not just stopping; it is reversing — the former thief becomes the giver, the laborer for others’ needs. Reformed and biblical economic ethics protect private property under the eighth commandment.</p>'
    ),
    'tulip': (
        '<p>TULIP is the seventeenth-century English acronym summarizing the Five Points of Calvinism — formalized at the Synod of Dort (1618-19) in response to the Arminian Remonstrance of 1610. The five points: <strong>T</strong>otal depravity (the whole man is morally corrupt by the fall), <strong>U</strong>nconditional election (God chooses the elect according to His own will, not foreseen merit), <strong>L</strong>imited atonement / particular redemption (Christ effectually died for the elect), <strong>I</strong>rresistible grace (the Spirit effectually draws the elect to Christ), and <strong>P</strong>erseverance of the saints (those truly saved are kept by God’s power and persevere to the end). The acronym is later than the Synod itself but accurately summarizes the Canons of Dort’s response.</p>'
    ),
    'two-ages': (
        '<p>The Two Ages are the biblical division of redemptive history into <em>"this age"</em> (Greek <em>aiōn houtos</em>) and <em>"the age to come"</em> (<em>aiōn ho mellōn</em>). <em>This age</em> is the present world under sin’s reign, ruled by <em>"the god of this world"</em> (<em>2 Corinthians 4:4</em>), <em>"the prince of the power of the air"</em> (<em>Ephesians 2:2</em>). <em>The age to come</em> is the consummated kingdom under Christ’s manifest reign, beginning at His return: <em>"the powers of the world to come"</em> (<em>Hebrews 6:5</em>); <em>"and these shall go away into everlasting punishment: but the righteous into life eternal"</em> (<em>Matthew 25:46</em>). The Christian lives in the overlap — the age to come has already broken in through Christ’s first advent, and is awaiting consummation at His second.</p>'
    ),
    'washing-feet': (
        '<p>The Washing of Feet is the act Christ performed at the Last Supper, washing the feet of His twelve disciples — including Judas — with a basin and towel (<em>John 13:1-17</em>). It was the work of the lowliest household servant; the Lord of the universe took it on Himself. Peter resisted: <em>"Thou shalt never wash my feet"</em>; Christ answered, <em>"If I wash thee not, thou hast no part with me"</em>; Peter relented: <em>"Lord, not my feet only, but also my hands and my head"</em>. After He had finished, Christ taught: <em>"If I then, your Lord and Master, have washed your feet; ye also ought to wash one another’s feet"</em>. Some traditions practice it as ordinance; all Christians are bound by its spirit. The greatest serves the least.</p>'
    ),
    'watch-and-pray': (
        '<p>"Watch and pray" is Christ’s command to the disciples in Gethsemane: <em>"Watch and pray, that ye enter not into temptation: the spirit indeed is willing, but the flesh is weak"</em> (<em>Matthew 26:41; Mark 14:38</em>). The pairing is essential. Watching alone (vigilance without prayer) becomes anxious self-reliance. Praying alone (devotion without watchfulness) becomes presumption. Together they form the Christian’s normal defense against temptation: alert to the enemy’s approach, dependent on the Father’s grace. The disciples failed to do either in Gethsemane — they fell asleep three times — and within hours every one of them forsook Him and fled. The pattern is a warning. Christian men should watch and pray as a paired daily discipline.</p>'
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
