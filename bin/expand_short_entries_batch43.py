#!/usr/bin/env python3
"""Batch 43 — expand 25 more entries from the 50-60 word bucket.

Targets: ethics, NT figures, OT history, doctrines, theologians,
hermeneutics, sacraments, and biblical imagery.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'orphan-care': (
        '<p>Orphan care is the biblical mandate to defend and provide for the fatherless — paired consistently in Scripture with widow-care and stranger-welcome. <em>"Pure religion and undefiled before God and the Father is this, To visit the fatherless and widows in their affliction, and to keep himself unspotted from the world"</em> (<em>James 1:27</em>). The LORD is named <em>"a father of the fatherless, and a judge of the widows"</em> (<em>Psalm 68:5</em>); His people imitate Him. The Mosaic law commanded specific protections: <em>"Ye shall not afflict any widow, or fatherless child"</em> (<em>Exodus 22:22-24</em>); the gleaning corners belonged to them (<em>Deuteronomy 24:19-21</em>); the third-year tithe fed them (<em>Deuteronomy 14:29; 26:12-13</em>). Adoption, foster-care, and gospel orphan-ministry are the modern church’s same obedience.</p>'
    ),
    'pilate': (
        '<p>Pontius Pilate was the Roman prefect of Judea (AD 26-36) who presided over the trial of Jesus. The Gospels record him finding no fault in Christ three times (<em>Luke 23:4, 14, 22</em>), declaring <em>"What is truth?"</em> in the face of the Truth (<em>John 18:38</em>), seeking a way out by offering Barabbas, washing his hands of the verdict — <em>"I am innocent of the blood of this just person: see ye to it"</em> (<em>Matthew 27:24</em>) — and finally yielding Christ to crucifixion under political pressure: <em>"If thou let this man go, thou art not Caesar’s friend"</em> (<em>John 19:12</em>). Pilate is the New Testament case study of a man who saw the truth, said the truth, and still refused to act on it. The Apostles’ Creed names him among the few historical figures of the cross.</p>'
    ),
    'right-hand-of-god': (
        '<p>The Right Hand of God is the position of supreme honor and active power. <em>Psalm 110:1</em> prophesies the Messiah’s session there: <em>"The LORD said unto my Lord, Sit thou at my right hand, until I make thine enemies thy footstool."</em> The New Testament fulfills the prophecy explicitly and repeatedly: <em>Mark 16:19; Acts 2:33-34; 5:31; 7:55-56; Romans 8:34; Ephesians 1:20; Hebrews 1:3; 1 Peter 3:22</em>. Christ’s session at the right hand declares three things at once. His <em>finished</em> work — He sat down. His <em>ongoing</em> intercession — He ever lives to make intercession (<em>Hebrews 7:25</em>). And His <em>present</em> reign — all authority in heaven and earth (<em>Matthew 28:18</em>). The Christian prays toward, hopes toward, and lives toward that throne.</p>'
    ),
    'saul-king': (
        '<p>Saul was Israel’s first king (c. 1050-1010 BC), of the tribe of Benjamin — anointed by Samuel at YHWH’s reluctant concession to Israel’s demand for a king <em>"like the nations"</em> (<em>1 Samuel 8:5</em>). Tall and handsome, initially humble (<em>9:21</em>; <em>10:22</em>), Saul reigned well at first against the Philistines and Ammonites. But he grew impatient with prophetic constraint, offered the burnt-offering unlawfully at Gilgal (<em>13:8-14</em>), spared Agag the Amalekite king and the best of the spoils against direct command (<em>15:9</em>), descended into paranoia and persecution of David (<em>chs. 18-26</em>), consulted the witch of Endor on the eve of battle (<em>28:7-25</em>), and died by his own sword on Mount Gilboa (<em>31:4</em>). The rejected king prefigures every man who chooses self-rule over submission.</p>'
    ),
    'scorpion': (
        '<p>The scorpion is a venomous arachnid of the wilderness — and in Scripture an emblem of fierce affliction. Rehoboam’s arrogant threat to Israel: <em>"my father hath chastised you with whips, but I will chastise you with scorpions"</em> (<em>1 Kings 12:11, 14</em>) precipitated the kingdom’s division. Ezekiel was sent to a rebellious people <em>"though briers and thorns be with thee, and thou dost dwell among scorpions"</em> (<em>Ezekiel 2:6</em>). The demonic torment of the fifth trumpet stings <em>"as the scorpions of the earth have power"</em> (<em>Revelation 9:3-10</em>). And Christ uses the scorpion in His fatherhood-comparison: what father, asked for an egg, would give a scorpion (<em>Luke 11:12</em>)? Christ also gives His servants authority over scorpions (<em>Luke 10:19</em>).</p>'
    ),
    'serpent-old': (
        '<p>The "old serpent" is <em>Revelation 12:9</em>’s explicit identification of Satan with the serpent of Eden: <em>"And the great dragon was cast out, that old serpent, called the Devil, and Satan, which deceiveth the whole world: he was cast out into the earth, and his angels were cast out with him"</em> (cf. <em>20:2</em>). The line from <em>Genesis 3</em> to <em>Revelation 12</em> is unbroken: the same enemy, the same lying voice, the same deceiver of nations. The first promise of the Bible was the crushing of his head by the seed of the woman (<em>Genesis 3:15</em>); the climactic vision of Scripture is its execution. Christ has bruised the serpent’s head at the cross (<em>Hebrews 2:14</em>); the final binding awaits His return.</p>'
    ),
    'seven': (
        '<p>Seven, in Scripture, is the number of completion and covenant — God’s number. He rested on the seventh day (<em>Genesis 2:2-3</em>). The priest sprinkled blood seven times before the Lord on Yom Kippur (<em>Leviticus 16:14, 19</em>). Joshua marched seven days around Jericho with seven priests blowing seven trumpets (<em>Joshua 6:4-15</em>). Naaman dipped seven times in the Jordan (<em>2 Kings 5:14</em>). Christ commanded Peter to forgive <em>"seventy times seven"</em> (<em>Matthew 18:22</em>). Revelation organizes its visions into sevens: seven churches, seven seals, seven trumpets, seven bowls, seven heads of the dragon, seven hills of Babylon. The number marks divinely-completed work. Where you see seven in Scripture, look for the LORD finishing something.</p>'
    ),
    'tent-of-meeting': (
        '<p>The Tent of Meeting (Hebrew <em>ohel moed</em>) is the tabernacle — the portable sanctuary at the center of Israel’s camp during the wilderness years — the appointed place where God came down and met with Moses, with the priests, and with His people. <em>"And there I will meet with thee, and I will commune with thee from above the mercy seat"</em> (<em>Exodus 25:22</em>); <em>"and the LORD spake unto Moses face to face, as a man speaketh unto his friend"</em> (<em>Exodus 33:11</em>). The whole biblical pattern of corporate worship descends from <em>ohel moed</em>: God gives His people a place to meet Him. The temple, the synagogue, the New-Covenant <em>ekklēsia</em>, and finally the New Jerusalem all extend the gracious institution.</p>'
    ),
    'theological-interpretation': (
        '<p>Theological Interpretation of Scripture (TIS) is the modern movement (Kevin Vanhoozer, Stephen Fowl, Daniel Treier, R. R. Reno, the Brazos commentary series) recovering pre-modern, theologically-engaged reading of the Bible. TIS reacts against historical-critical fragmentation by reading Scripture as <em>the church’s book</em> — with creedal awareness, doctrinal coherence, traditional reception, and Christ-centered focus. It is not anti-historical-critical; it locates that work within a theologically richer reading frame. <em>"All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness"</em> (<em>2 Timothy 3:16</em>). Reformed readers will appreciate the recovery while testing each application against the rule of <em>sola Scriptura</em>. Tradition is consulted; it does not govern.</p>'
    ),
    'threshing': (
        '<p>Threshing is the post-harvest beating or rolling that separates grain from stalk — sledges, oxen, threshing-flails, or the unshod hooves of cattle were used. Scripture loads it figuratively. <em>"Judah shall plow, and Jacob shall break his clods"</em> (<em>Hosea 10:11</em>) calls Israel to repentance under the figure. <em>"Arise and thresh, O daughter of Zion: for I will make thine horn iron, and I will make thy hoofs brass: and thou shalt beat in pieces many people"</em> (<em>Micah 4:13</em>). John the Baptist describes Christ’s judgment: <em>"his fan is in his hand, and he will throughly purge his floor"</em> (<em>Matthew 3:12</em>). The LORD also calls Babylon His threshing-floor (<em>Jeremiah 51:33</em>). The Day of the LORD threshes nations.</p>'
    ),
    'tilling': (
        '<p>Tilling is the patient labor of breaking up the ground before any seed is sown — the unglamorous first work that makes everything else possible. Adam was placed in Eden <em>"to dress it and to keep it"</em> (<em>Genesis 2:15</em>) — to till and to guard. Hosea calls Israel back to repentance under the figure: <em>"Break up your fallow ground: for it is time to seek the LORD, till he come and rain righteousness upon you"</em> (<em>Hosea 10:12</em>; cf. <em>Jeremiah 4:3</em>). Christ’s parable of the four soils (<em>Matthew 13</em>) assumes that the difference between fruit and barrenness lies first in what was done to the soil. The Christian who would bear fruit must first till the heart by repentance.</p>'
    ),
    'trespass': (
        '<p>A trespass is a specific act of sin construed as a <em>crossing of a boundary</em> or a falling-aside from the path of obedience. In Levitical law, it formed the basis for a specific category of sin offering — the <em>asham</em>, the trespass offering of <em>Leviticus 5-7</em>, required especially where the wrong involved sacred property or harm to a neighbor, and demanded restitution plus a fifth-part penalty. The Lord’s Prayer in Matthew’s version hangs the petition for forgiveness on our forgiveness of others’ trespasses: <em>"Forgive us our debts, as we forgive our debtors... For if ye forgive men their trespasses, your heavenly Father will also forgive you: But if ye forgive not men their trespasses, neither will your Father forgive your trespasses"</em> (<em>Matthew 6:12, 14-15</em>).</p>'
    ),
    'under-the-sun': (
        '<p>"Under the sun" is Ecclesiastes’ framing phrase for the human-eye view of life — what is observable in this fallen world considered apart from divine revelation. It appears 29 times in Ecclesiastes alone and almost nowhere else in Scripture. <em>"I have seen all the works that are done under the sun; and, behold, all is vanity and vexation of spirit"</em> (<em>1:14</em>). The Preacher diagnoses everything <em>"under the sun"</em> as <em>hevel</em> — vapor, breath, smoke. Meaning emerges only when the perspective shifts <em>above the sun</em>, where the eternal God dwells and acts. The phrase is therefore methodological: it brackets what reason-without-revelation can see and lets the limits of that vision teach humility.</p>'
    ),
    'vinedresser': (
        '<p>A vinedresser is the skilled tender of grapevines — specifically the one who prunes, props, and prepares the vines for fruit-bearing. The work is technical and seasonal. Scripture loads the title theologically. The Father is the great <em>"husbandman"</em> (or vinedresser): <em>"I am the true vine, and my Father is the husbandman. Every branch in me that beareth not fruit he taketh away: and every branch that beareth fruit, he purgeth it, that it may bring forth more fruit"</em> (<em>John 15:1-2</em>). Isaiah reserves the title for the Spirit-led shepherd: <em>"strangers shall stand and feed your flocks, and the sons of the alien shall be your plowmen and your vinedressers"</em> (<em>Isaiah 61:5</em>). The vinedresser’s pruning shears are mentioned more often than his picking baskets.</p>'
    ),
    'wiles-of-devil': (
        '<p>"The wiles of the devil" is Paul’s precise phrase in <em>Ephesians 6:11</em>: <em>"Put on the whole armour of God, that ye may be able to stand against the wiles of the devil."</em> The Greek <em>methodeia</em> means a structured, deceptive <em>method</em> — not random or impulsive temptation, but planned, recurring tactical patterns: lying, accusing, distorting Scripture, exploiting weakness, isolating the saint from the herd, attacking at the lowest point of strength. The devil’s wiles are well-rehearsed — they have worked for millennia and they will be tried on the Christian in his turn. The armor is given specifically because the methods are known. <em>"Lest Satan should get an advantage of us: for we are not ignorant of his devices"</em> (<em>2 Corinthians 2:11</em>).</p>'
    ),
    'zion-worship': (
        '<p>Zion worship is the worship that ascended from the appointed mountain — the place where God set His Name, where the temple stood, and from which the Psalms came. <em>"For the LORD hath chosen Zion; he hath desired it for his habitation. This is my rest for ever: here will I dwell; for I have desired it"</em> (<em>Psalm 132:13-14</em>); <em>"The LORD loveth the gates of Zion more than all the dwellings of Jacob"</em> (<em>Psalm 87:2</em>). In the New Covenant, Zion is opened wider: the church gathers, by faith, to the heavenly Mount Zion. <em>"But ye are come unto mount Sion, and unto the city of the living God, the heavenly Jerusalem, and to an innumerable company of angels"</em> (<em>Hebrews 12:22</em>). Zion worship is completed in Christ.</p>'
    ),
    'allegory-method': (
        '<p>Allegorical interpretation reads a text as though its surface details represent deeper spiritual realities — often without warrant in the original author’s intent. Paul does call Hagar and Sarah an allegory (<em>"which things are an allegory"</em>, <em>Galatians 4:24</em>), giving the method a limited inspired foothold. Christian use across history has ranged from disciplined typology (Augustine, Aquinas at their best) to fanciful spiritualizing that severed the text from its literal sense (medieval excesses, the four-fold sense run wild). The Reformers — Luther, Calvin, Tyndale — largely rejected uncontrolled allegorizing in favor of literal-grammatical-historical reading: <em>"the literal sense is the root and ground of all"</em> (Tyndale). Typology, controlled by the New Testament’s own examples, remains; allegory as method does not.</p>'
    ),
    'aquinas': (
        '<p>Thomas Aquinas (1225-1274) was the Italian-born Dominican friar whose <em>Summa Theologica</em> remains the dominant medieval synthesis of theology and philosophy in the Roman Catholic tradition. He fused Christian theology with Aristotelian philosophy, formulated the famous Five Ways (cosmological-style arguments for God’s existence), and developed the doctrines of analogy of being, natural law, and the relation of grace and nature (<em>"grace does not destroy nature, but perfects it"</em>). The Roman Catholic Church names him <em>Doctor Angelicus</em> ("Angelic Doctor"). Reformed Protestants engage him critically — appreciating the Christological orthodoxy, the natural-theology project, and the moral framework, while rejecting his eucharistic transubstantiation, treasury-of-merit, and the broader Roman synthesis built on his work.</p>'
    ),
    'baptism-modes': (
        '<p>Baptism modes are the three principal Christian forms in which water has been applied: <em>immersion</em> (going completely under, the favored Baptist mode), <em>pouring</em> (affusion, water poured over the head, the historic Presbyterian and Lutheran mode), and <em>sprinkling</em> (aspersion, drops applied, the long-standing Reformed practice especially for infants). Different traditions emphasize different modes with theological argument; all three have biblical and historical warrant. The Greek <em>baptizō</em> covers a range of water-applications — from full immersion to ritual washing (<em>Mark 7:4</em>’s baptisms of <em>"pots, and cups, and brasen vessels, and of tables"</em>). The New Testament focus is on the meaning — union with Christ in death, burial, and resurrection (<em>Romans 6:3-4</em>) — not exclusively on a single mode.</p>'
    ),
    'bernice': (
        '<p>Bernice was the eldest daughter of Herod Agrippa I (the king who killed James and was eaten of worms, <em>Acts 12</em>), and sister to Agrippa II and Drusilla — the Herodian family’s second generation in the New Testament era. She lived with her brother Agrippa II in a relationship widely rumored among Roman writers to be incestuous. Bernice sat beside Agrippa <em>"with great pomp"</em> at Paul’s hearing in Caesarea: <em>"And on the morrow, when Agrippa was come, and Bernice, with great pomp, and was entered into the place of hearing... Paul was brought forth"</em> (<em>Acts 25:13, 23; 26:30</em>). Her later affair with the future emperor Titus (who destroyed Jerusalem in AD 70) is recorded by the Roman historians Tacitus and Suetonius.</p>'
    ),
    'blessed-hope': (
        '<p>"The blessed hope" is Paul’s phrase in <em>Titus 2:13</em>: <em>"Looking for that blessed hope, and the glorious appearing of the great God and our Saviour Jesus Christ."</em> The phrase has become the church’s standard summary of Christian eschatological expectation: not a vague hope but a <em>blessed</em> one — anchored in Christ’s personal appearing, sustained by His promise, and tested by His resurrection. The context (<em>vv. 11-14</em>) places it within the grace that <em>"teacheth us that, denying ungodliness and worldly lusts, we should live soberly, righteously, and godly, in this present world."</em> The blessed hope shapes present holiness; the man who looks for that appearing lives differently. <em>"Every man that hath this hope in him purifieth himself, even as he is pure"</em> (<em>1 John 3:3</em>).</p>'
    ),
    'carpenter': (
        '<p>A carpenter is a craftsman who works in wood — and in the Greek New Testament the term <em>tektōn</em> covers a broader category including stoneworker, builder, and woodworker (something like our modern "tradesman"). Joseph was a <em>tektōn</em> (<em>Matthew 13:55</em>), and Christ Himself was known as the carpenter by His Nazareth neighbors: <em>"Is not this the carpenter, the son of Mary, the brother of James, and Joses, and of Juda, and Simon? and are not his sisters here with us?"</em> (<em>Mark 6:3</em>). The Lord of creation — through whom <em>"all things were made"</em> (<em>John 1:3</em>) — spent the bulk of His earthly years working with His hands at an ordinary, sweaty, calloused trade. Every Christian carpenter, mason, mechanic, and farmer follows the same shop.</p>'
    ),
    'christ-centered-reading': (
        '<p>Christ-Centered Reading interprets every passage of Scripture with reference to its place in revealing Christ — either by direct prophecy, typological prefigurement, thematic anticipation, contrast (the law’s demand exposing the need for Christ’s grace), or canonical pointer. Christ Himself authorized this reading: <em>"And beginning at Moses and all the prophets, he expounded unto them in all the scriptures the things concerning himself"</em> (<em>Luke 24:27</em>); <em>"These are the words which I spake unto you, while I was yet with you, that all things must be fulfilled, which were written in the law of Moses, and in the prophets, and in the psalms, concerning me"</em> (<em>Luke 24:44</em>). Modern proponents include Edmund Clowney, Sidney Greidanus, Sinclair Ferguson, and Tim Keller. Christ is the Bible’s central character.</p>'
    ),
    'conquest': (
        '<p>The Conquest is Israel’s entry into and military possession of the land of Canaan under Joshua — fulfilling the Abrahamic land-promise: <em>"In the same day the LORD made a covenant with Abram, saying, Unto thy seed have I given this land, from the river of Egypt unto the great river, the river Euphrates"</em> (<em>Genesis 15:18</em>). The conquest occupied roughly seven years and is recorded in the books of Joshua and Judges. It was both a divine judgment on the Canaanite nations for their accumulated wickedness — <em>"for the iniquity of the Amorites is not yet full"</em> (<em>Genesis 15:16</em>) — and a covenant gift to Israel. The conquest is selective (not every Canaanite city was destroyed); the spiritual application is the church’s warfare against indwelling sin in the heart-land.</p>'
    ),
    'craft': (
        '<p>Craft is the learned trade — the manual skill by which one shapes wood, metal, cloth, or stone into useful or beautiful things. Scripture honors the craftsman explicitly and by name. <em>"And I have filled him with the spirit of God, in wisdom, and in understanding, and in knowledge, and in all manner of workmanship, To devise cunning works, to work in gold, and in silver, and in brass, And in cutting of stones... and in carving of timber"</em> (<em>Exodus 31:3-5</em>) — Bezalel filled by the Spirit for craft work on the tabernacle. Christ Himself was a <em>tektōn</em>, the carpenter of Nazareth (<em>Mark 6:3</em>). Paul made tents to support his apostolic ministry (<em>Acts 18:3</em>). Skilled hands are sanctified hands.</p>'
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
