#!/usr/bin/env python3
"""Batch 54 — expand 25 more entries from the 60-70 word bucket.

Brings the sprint total to 1,350.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'white-throne': (
        '<p>The Great White Throne is the throne of final judgment in <em>Revelation 20:11-15</em>, before which the resurrected dead — small and great — stand to be judged out of the books that are opened. <em>"And I saw a great white throne, and him that sat on it, from whose face the earth and the heaven fled away; and there was found no place for them. And I saw the dead, small and great, stand before God; and the books were opened: and another book was opened, which is the book of life: and the dead were judged out of those things which were written in the books, according to their works."</em> Whoever is not found written in the book of life is cast into the lake of fire. Final, irreversible, universal.</p>'
    ),
    'ziklag': (
        '<p>Ziklag is the Philistine town King Achish of Gath gave the fugitive David as a base of operation during his sixteen-month exile in the wilderness (<em>1 Samuel 27:5-7</em>) — a strategic gift that allowed David to raid Israel’s enemies while pretending to serve Achish. Ziklag is the place where the Amalekites raided and burned the camp while David and his men were away with Achish’s army; their wives and children were carried captive (<em>1 Samuel 30:1-6</em>). David’s own men spoke of stoning him. The text says: <em>"But David encouraged himself in the LORD his God"</em> (<em>v. 6</em>). He inquired of the LORD, pursued the Amalekites, recovered all, and returned. Two days later he learned of Saul’s death.</p>'
    ),
    'beard': (
        '<p>The beard is the hair of the male chin and lower face — and in Scripture, the visible mark of manhood, age, and dignity. The Levitical law explicitly protected it: <em>"Thou shalt not... mar the corners of thy beard"</em> (<em>Leviticus 19:27; 21:5</em>). To shave half a beard was an act of humiliation: Hanun king of the Ammonites did it to David’s ambassadors, and David made them tarry at Jericho until their beards grew (<em>2 Samuel 10:4-5</em>). To pluck off the beard was the mark of mourning or scandal (<em>Ezra 9:3; Isaiah 50:6</em>). Christ’s beard was plucked by His abusers: <em>"I gave my back to the smiters, and my cheeks to them that plucked off the hair"</em> (<em>Isaiah 50:6</em>). Honor the beard; recover it.</p>'
    ),
    'boasting': (
        '<p>Boasting is the proud declaration of one’s own works, status, or strength — and Scripture treats it in two opposite ways. <em>Self-boasting</em> is condemned absolutely: <em>"Where is boasting then? It is excluded. By what law? of works? Nay: but by the law of faith"</em> (<em>Romans 3:27</em>); <em>"That no flesh should glory in his presence"</em> (<em>1 Corinthians 1:29</em>). The whole gospel uproots ground for self-boasting. <em>Lord-boasting</em>, however, is commanded: <em>"But he that glorieth, let him glory in the Lord"</em> (<em>1 Corinthians 1:31</em>; quoting <em>Jeremiah 9:23-24</em>: <em>"Let not the wise man glory in his wisdom... but let him that glorieth glory in this, that he understandeth and knoweth me"</em>). Christian men learn to boast loudly — but only of Christ.</p>'
    ),
    'bread-of-the-presence': (
        '<p>The Bread of the Presence (KJV: <em>shewbread</em>) was the twelve loaves of fine flour set every Sabbath on the gold-overlaid table in the Holy Place of the tabernacle and later the temple — one loaf for each tribe of Israel — and eaten by the priests at week’s end (<em>Exodus 25:30; Leviticus 24:5-9</em>). It was not magical food but symbolic of God’s covenant presence with His twelve-tribe people. David famously ate the bread of the Presence at Nob when fleeing Saul, an exception cited by Christ when defending His disciples for plucking grain on the Sabbath (<em>1 Samuel 21:1-6; Matthew 12:3-4</em>). Christ Himself is the true Bread of the Presence: <em>"I am the bread of life"</em> (<em>John 6:35, 48</em>).</p>'
    ),
    'cool-beans': (
        '<p>"Cool beans" is the era-stamped mild positive exclamation of approval or pleasure — Boomer / early-Gen-X vocabulary popular from roughly 1965-1990 and now mostly nostalgic. The slang is purely expressive and theologically neutral. The Christian observation falls in the broader category of speech-as-sanctified — Paul’s direction: <em>"Let your speech be alway with grace, seasoned with salt, that ye may know how ye ought to answer every man"</em> (<em>Colossians 4:6</em>). Era-stamped slang is often a small generational signature; older Christians using it may find their grandchildren puzzled. The gospel itself is timeless; the verbal furniture surrounding it varies by generation. Speak gracefully in whatever vocabulary your hearers actually use.</p>'
    ),
    'creed-apostles': (
        '<p>The Apostles’ Creed is the early Christian baptismal creed, summarizing the faith in twelve articles structured Trinitarianly — confessing the Father (creation), the Son (incarnation, crucifixion, burial, descent, resurrection, ascension, return, judgment), and the Holy Spirit (church, communion of saints, forgiveness, resurrection of the body, life everlasting). Its earliest form (the <em>Old Roman Symbol</em>) dates to the second century AD and was used as the basic confession of baptismal candidates; its present full form was largely fixed by the fifth or sixth century. Not literally composed by the twelve apostles, but ancient and apostolic in substance. The Reformed tradition retains it as one of the three ecumenical creeds. Reciting it weekly binds the church across centuries.</p>'
    ),
    'dawn': (
        '<p>Dawn is the breaking of the morning light — and in Scripture, the hour the women came to the tomb on Resurrection morning. All four Gospels record it: <em>"In the end of the sabbath, as it began to dawn toward the first day of the week, came Mary Magdalene and the other Mary to see the sepulchre"</em> (<em>Matthew 28:1</em>; cf. <em>Mark 16:2; Luke 24:1; John 20:1</em>). They are unanimous: first-day-of-the-week dawn. Lamentations names the LORD’s mercies new at the same hour: <em>"It is of the LORD’s mercies that we are not consumed, because his compassions fail not. They are new every morning: great is thy faithfulness"</em> (<em>Lamentations 3:22-23</em>). Christian men should learn to meet the LORD at dawn.</p>'
    ),
    'denial': (
        '<p>Denial in Scripture cuts two ways. Peter’s denial of Christ before the maid in the high priest’s courtyard is the paradigm of <em>sinful</em> denial — refusing to confess what one knows to be true, out of fear: <em>"I know not the man"</em> (<em>Matthew 26:69-75</em>; cf. <em>Mark 14:66-72</em>). Christ had foretold it; Peter wept bitterly; the risen Christ restored him at the charcoal fire (<em>John 21:15-19</em>). But Christ also commands <em>righteous</em> denial: <em>"If any man will come after me, let him deny himself, and take up his cross, and follow me"</em> (<em>Matthew 16:24; Mark 8:34; Luke 9:23</em>). Deny self; never deny Christ. The two denials cut in opposite directions.</p>'
    ),
    'ear': (
        '<p>The ear is the organ of hearing — and in Scripture, the body part most associated with the chief duty of the believer to <em>hear</em> the voice of God. The Hebrew bondservant who chose to remain in his master’s house had the ear pierced through with an awl at the doorpost as the sign of perpetual willing service: <em>"And his master shall bore his ear through with an aul; and he shall serve him for ever"</em> (<em>Exodus 21:6</em>) — applied messianically in <em>Psalm 40:6</em>: <em>"mine ears hast thou opened"</em>. Christ repeatedly closes parables: <em>"He that hath ears to hear, let him hear"</em> (<em>Matthew 11:15; 13:9, 43; Revelation 2:7</em>). The pierced ear of the slave became the pierced ear of the Servant who said, <em>"Lo, I come... to do thy will, O God"</em> (<em>Hebrews 10:7</em>).</p>'
    ),
    'elizabeth': (
        '<p>Elizabeth was the wife of Zacharias the priest, mother of John the Baptist, and cousin (or kinswoman) of Mary the mother of Jesus (<em>Luke 1</em>). Of Aaron’s priestly line through both parents and described as <em>"both righteous before God, walking in all the commandments and ordinances of the Lord blameless"</em> (<em>1:6</em>), she was barren until old age — Sarah’s pattern repeated. She conceived after Gabriel’s announcement to her husband in the temple. When Mary came to visit during the sixth month, Elizabeth’s unborn John leapt in her womb at the sound of Mary’s greeting, and Elizabeth, filled with the Holy Ghost, prophesied: <em>"Blessed art thou among women, and blessed is the fruit of thy womb"</em> (<em>1:42</em>). Three months of holy fellowship between mothers.</p>'
    ),
    'engagement': (
        '<p>In Scripture, engagement (betrothal) was a legally binding covenant — far more serious than modern engagement. Joseph and Mary were <em>"espoused"</em> when she was found with child: <em>"Joseph her husband, being a just man, and not willing to make her a publick example, was minded to put her away privily"</em> (<em>Matthew 1:18-19</em>) — the betrothal pledge required legal divorce to break, and the angel directly calls Joseph her <em>husband</em>. Paul uses betrothal as a sustained metaphor for Christ and the church: <em>"For I have espoused you to one husband, that I may present you as a chaste virgin to Christ"</em> (<em>2 Corinthians 11:2</em>). The church is now in the engagement period awaiting the wedding-supper of the Lamb (<em>Revelation 19:7-9</em>).</p>'
    ),
    'eternal-punishment': (
        '<p>"Eternal punishment" is Christ’s phrase in <em>Matthew 25:46</em>: <em>"And these shall go away into everlasting punishment: but the righteous into life eternal."</em> The Greek adjective <em>aiōnios</em> ("eternal") modifies <em>both</em> the punishment of the wicked <em>and</em> the life of the righteous in the same sentence — and the parallel grammatical structure refuses any softening of one side without softening the other. Christ repeatedly preaches eternal punishment: the worm that dies not and the fire not quenched (<em>Mark 9:43-48</em>); the outer darkness with weeping and gnashing of teeth (<em>Matthew 8:12; 22:13; 25:30</em>); the everlasting fire prepared for the devil (<em>25:41</em>). Annihilationism and universalism collapse under His direct words. Hell is eternal, conscious, and just.</p>'
    ),
    'exodus-typology': (
        '<p>Exodus typology is the recurring biblical pattern that the Exodus from Egypt is the foundational redemptive-historical event, and that later redemptive acts are deliberately patterned on it. Christ is the Passover Lamb: <em>"For even Christ our passover is sacrificed for us"</em> (<em>1 Corinthians 5:7</em>). Christian baptism corresponds to the Red Sea crossing: <em>"And were all baptized unto Moses in the cloud and in the sea"</em> (<em>1 Corinthians 10:1-2</em>). Jesus deliberately recapitulates Israel’s history — called out of Egypt (<em>Matthew 2:15</em>, quoting <em>Hosea 11:1</em>), passing through the waters at baptism, tested forty days in the wilderness (<em>Matthew 4:1-11</em>) where Israel had been tested forty years. The whole gospel is an Exodus restaged.</p>'
    ),
    'exploitation': (
        '<p>Scripture condemns exploitation absolutely. <em>"He that oppresseth the poor reproacheth his Maker: but he that honoureth him hath mercy on the poor"</em> (<em>Proverbs 14:31</em>). The prophets thundered against those who exploited workers and widows: <em>"Because they sold the righteous for silver, and the poor for a pair of shoes; That pant after the dust of the earth on the head of the poor"</em> (<em>Amos 2:6-7</em>); <em>"Behold, the hire of the labourers who have reaped down your fields, which is of you kept back by fraud, crieth: and the cries of them which have reaped are entered into the ears of the Lord of sabaoth"</em> (<em>James 5:4</em>). The Mosaic law built protections into the harvest itself (gleaning), the calendar (sabbaths, Jubilee), and the courts (no respect of persons).</p>'
    ),
    'fear-god-keep-commandments': (
        '<p>"Fear God, and keep his commandments" is Ecclesiastes’ closing summary: <em>"Let us hear the conclusion of the whole matter: Fear God, and keep his commandments: for this is the whole duty of man. For God shall bring every work into judgment, with every secret thing, whether it be good, or whether it be evil"</em> (<em>Ecclesiastes 12:13-14</em>). After twelve chapters of diagnosing every domain under the sun as <em>hevel</em> (vapor) — wisdom, pleasure, work, wealth, power, reputation — the Preacher’s verdict lands here. Two clauses define <em>"the whole duty of man"</em>: fear God; keep His commandments. Everything else is commentary. The verse is a useful summary catechism for an entire Christian life.</p>'
    ),
    'feast-trumpets': (
        '<p>The Feast of Trumpets (Hebrew <em>Yom Teruah</em>, "day of the blast") is the Old Testament autumn convocation on the first day of the seventh month (Tishri), inaugurated by the blowing of trumpets (<em>shofars</em>): <em>"In the seventh month, in the first day of the month, shall ye have a sabbath, a memorial of blowing of trumpets, an holy convocation"</em> (<em>Leviticus 23:23-25; Numbers 29:1-6</em>). It was a Sabbath rest, a holy assembly, and the gateway to the autumn cluster of feasts — Day of Atonement (10th of Tishri) and Tabernacles (15th-21st of Tishri). In modern Judaism it became <em>Rosh Hashanah</em> ("head of the year"), the civil new year. Christ’s return is heralded by trumpet (<em>1 Corinthians 15:52; 1 Thessalonians 4:16</em>).</p>'
    ),
    'gaius': (
        '<p>At least three or four men named Gaius appear in the New Testament — a common Roman <em>praenomen</em>. (1) <em>Gaius of Corinth</em>, Paul’s host whom he personally baptized: <em>"I thank God that I baptized none of you, but Crispus and Gaius"</em> (<em>1 Corinthians 1:14</em>; cf. <em>Romans 16:23</em> — <em>"Gaius mine host, and of the whole church, saluteth you"</em>). (2) <em>Gaius of Macedonia</em>, dragged into the Ephesian theatre by the silversmiths’ riot (<em>Acts 19:29</em>). (3) <em>Gaius of Derbe</em>, one of Paul’s travel companions delivering the Jerusalem offering (<em>Acts 20:4</em>). (4) The <em>Gaius</em> of <em>3 John</em>, commended for his hospitality to traveling preachers: <em>"the beloved Gaius, whom I love in the truth"</em>. The same name; many faithful saints.</p>'
    ),
    'garrison': (
        '<p>A garrison is a military unit stationed in a fortified place to hold it against attack. Scripture uses the same picture for the peace of God watching over the believer’s soul: <em>"And the peace of God, which passeth all understanding, shall keep [Greek <em>phrourēsei</em>, "shall garrison"] your hearts and minds through Christ Jesus"</em> (<em>Philippians 4:7</em>). The Greek verb is a military term — to stand guard, to garrison a city against attack. God’s peace is not a soft soothing feeling; it is an armed sentry posted at the gate of heart and mind, repelling the assaults of anxiety. Peter uses the same verb of the believer himself: <em>"who are kept [garrisoned] by the power of God through faith"</em> (<em>1 Peter 1:5</em>).</p>'
    ),
    'government': (
        '<p>Government in Scripture is ordained by God for justice and order. <em>"Let every soul be subject unto the higher powers. For there is no power but of God: the powers that be are ordained of God"</em> (<em>Romans 13:1</em>). Civil rulers bear the sword to punish evildoers and reward good behavior: <em>"For he is the minister of God to thee for good. But if thou do that which is evil, be afraid; for he beareth not the sword in vain"</em> (<em>13:4</em>). Rulers are <em>"God’s ministers"</em> (<em>13:6</em>). Christians render the proper response: <em>"Render therefore to all their dues: tribute to whom tribute is due; custom to whom custom; fear to whom fear; honour to whom honour"</em> (<em>13:7</em>). Pay taxes; obey laws; honor the office.</p>'
    ),
    'hallelujah': (
        '<p>Hallelujah (Hebrew <em>halelu Yah</em>) is an exclamatory imperative addressed to a group: <em>"praise YHWH!"</em> It is a pure, unadulterated expression of worship, joy, and adoration directed to the LORD for who He is and what He has done. It appears frequently in the Psalter, especially in the closing Hallel psalms (<em>113-118; 146-150</em>) sung at the great feasts, and it punctuates the Psalter’s final crescendo: <em>"Let every thing that hath breath praise the LORD. Praise ye the LORD"</em> (<em>Psalm 150:6</em>). In the New Testament the Greek transliteration <em>Allēlouia</em> appears only in <em>Revelation 19:1-6</em> — sung by the great multitude in heaven over Babylon’s fall and at the marriage supper of the Lamb. The first and last word of the redeemed.</p>'
    ),
    'i-am-bread': (
        '<p>"I am the bread of life" is Christ’s first great <em>I AM</em> predicate-statement in John’s Gospel: <em>"I am the bread of life: he that cometh to me shall never hunger; and he that believeth on me shall never thirst"</em> (<em>John 6:35; cf. 6:48, 51</em>). The saying follows immediately upon the feeding of the five thousand and Christ’s walking on water — the people came back the next day for more loaves. Christ confronts them: they sought Him not because of the sign but for the bread that perished. He directs them to the bread that endures unto eternal life. He then identifies Himself as that bread: <em>"I am that bread of life"</em>. The <em>I AM</em> (Greek <em>egō eimi</em>) deliberately echoes God’s self-naming to Moses at the bush.</p>'
    ),
    'jehovah-shammah': (
        '<p><em>Jehovah-Shammah</em> (יְהוָה שָׁמָּה) — "the LORD is there" — is the eschatological covenant name given by Ezekiel as the new name of the restored Jerusalem in the closing verse of his prophecy: <em>"It was round about eighteen thousand measures: and the name of the city from that day shall be, The LORD is there"</em> (<em>Ezekiel 48:35</em>). The name climaxes Ezekiel’s vision of the restored temple, the river flowing from beneath the threshold, and the renewed land. It points beyond physical Jerusalem to the New Jerusalem of <em>Revelation 21-22</em>, where God Himself is the temple (<em>21:22</em>) and dwells with His people forever: <em>"the tabernacle of God is with men, and he will dwell with them, and they shall be his people, and God himself shall be with them, and be their God"</em> (<em>21:3</em>).</p>'
    ),
    'kept-faith': (
        '<p>"I have kept the faith" is the third of Paul’s confessions in <em>2 Timothy 4:7</em> about his completed ministry, written from a Roman prison shortly before his martyrdom: <em>"I have fought a good fight, I have finished my course, I have kept the faith: Henceforth there is laid up for me a crown of righteousness, which the Lord, the righteous judge, shall give me at that day."</em> The Greek <em>tērein</em> ("to keep, guard, preserve") implies stewardship of a deposit — Paul did not lose, alter, or compromise the gospel committed to him. He also commands Timothy: <em>"O Timothy, keep that which is committed to thy trust"</em> (<em>1 Timothy 6:20</em>; cf. <em>2 Timothy 1:14</em>). Every Christian elder receives the same deposit. Guard it.</p>'
    ),
    'kyrie': (
        '<p>The <em>Kyrie</em> is the historic short pleading prayer of the Christian liturgy: <em>Kyrie eleison, Christe eleison, Kyrie eleison</em> — "Lord have mercy, Christ have mercy, Lord have mercy" — typically sung antiphonally near the start of worship. Its biblical origin is unmistakable. Blind Bartimaeus cried: <em>"Jesus, thou Son of David, have mercy on me"</em> (<em>Mark 10:47-48</em>). The Canaanite woman: <em>"Have mercy on me, O Lord, thou Son of David"</em> (<em>Matthew 15:22</em>). The ten lepers: <em>"Jesus, Master, have mercy on us"</em> (<em>Luke 17:13</em>). The publican: <em>"God be merciful to me a sinner"</em> (<em>Luke 18:13</em>). The early church embedded the cry as the gathered congregation’s first liturgical word. Christian men learn it before they learn anything else.</p>'
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
