#!/usr/bin/env python3
"""Batch 56 — clears Names 50-70 bucket + starts generational polish.

Last 20 of the Names section's 50-70w bucket + first 5 generational
slang entries. Clears the Names section's thin tail entirely.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    # === REMAINING 20 NAMES ===
    'jason-thessalonica': (
        '<p>Jason was the Thessalonian believer who hosted Paul and Silas in his home during their brief Thessalonian mission (<em>Acts 17:1-9</em>). When the city erupted at Paul’s preaching, the mob — incited by certain unbelieving Jews — could not find the missionaries and dragged Jason and other brethren before the city rulers, charging: <em>"These that have turned the world upside down are come hither also; Whom Jason hath received: and these all do contrary to the decrees of Caesar, saying that there is another king, one Jesus"</em> (<em>17:6-7</em>). The accusation of political subversion was deadly serious under Roman law. Jason and the others posted security and were released, and Paul and Silas were sent away by night to Berea. Jason paid the cost of hospitality; Paul mentions a Jason in <em>Romans 16:21</em> who may be the same man.</p>'
    ),
    'sandals-peace': (
        '<p>The Sandals of Peace are the fifth piece of the whole armor of God: <em>"And your feet shod with the preparation of the gospel of peace"</em> (<em>Ephesians 6:15</em>). Roman soldiers wore studded sandals (<em>caligae</em>) — hobnailed footwear that gave them traction in melee and let them stand firm on uneven ground. Paul’s metaphor is precise. The believer stands firm in battle on <em>preparation</em> (Greek <em>hetoimasia</em>, "readiness") that comes from <em>the gospel of peace</em>. The reconciled-to-God soul has solid footing under it; the unsaved soldier slips. Footwear also bears the messenger out: <em>"How beautiful upon the mountains are the feet of him that bringeth good tidings, that publisheth peace"</em> (<em>Isaiah 52:7; Romans 10:15</em>). Stand firm; carry the news.</p>'
    ),
    'james-of-alphaeus': (
        '<p>James the son of Alphaeus was one of the Twelve and is distinguished in the apostle lists from James the son of Zebedee (the brother of John, beheaded by Herod Agrippa I in <em>Acts 12:2</em>) and from James the Lord’s brother (the leader of the Jerusalem church and author of the epistle of James). He is named in all four apostle lists (<em>Matthew 10:3; Mark 3:18; Luke 6:15; Acts 1:13</em>) but never given a separate biographical scene. He is often called <em>James the Less</em> (<em>Mark 15:40</em>) — distinguishing him from his more famous namesake. His mother Mary stood at the cross with the other women (<em>Mark 15:40; 16:1</em>). Tradition variously places his death by stoning in Egypt or by crucifixion in Persia. A faithful apostle hidden in plain sight.</p>'
    ),
    'spurgeon-figure': (
        '<p>Charles Haddon Spurgeon (1834-1892) was the English Particular Baptist preacher whose thirty-eight-year ministry at the Metropolitan Tabernacle in London made him <em>"the Prince of Preachers."</em> Converted at fifteen in a snowed-in Primitive Methodist chapel under a layman’s impromptu sermon on <em>Isaiah 45:22</em>, he pastored Waterbeach Baptist Chapel at sixteen and the New Park Street Chapel in London at nineteen. His sermons were transcribed and printed weekly, distributed worldwide, and translated into dozens of languages; the collected <em>Metropolitan Tabernacle Pulpit</em> runs to 63 volumes — the largest body of sermons in church history. Major works also: <em>The Treasury of David</em> (Psalms commentary), <em>Lectures to My Students</em>, <em>Morning and Evening</em>. He suffered chronic gout and depression; fought the Downgrade Controversy against liberalism. He was 57 when he died.</p>'
    ),
    'beelzebub': (
        '<p>Beelzebub (or <em>Beelzebul</em>, the Greek form) was originally the Philistine god of Ekron consulted by King Ahaziah of Israel after his fall through the lattice — <em>"Beelzebub the god of Ekron"</em> (<em>2 Kings 1:2-6, 16</em>). The Hebrew form (<em>Baal-zebub</em>) means "Lord of the flies"; the Greek (<em>Baal-zebul</em>) may mean "Lord of the dwelling" — perhaps a deliberate Jewish corruption of the Philistine title. In the Gospels the name is used by Christ’s opponents and by Christ Himself as a name for the prince of demons. The Pharisees attributed His exorcisms to <em>"Beelzebub the prince of the devils"</em>; Christ exposed the absurdity (<em>Matthew 12:24-27; Mark 3:22; Luke 11:15-19</em>). <em>"It is enough for the disciple that he be as his master... if they have called the master of the house Beelzebub, how much more shall they call them of his household?"</em> (<em>Matthew 10:25</em>).</p>'
    ),
    'beersheba': (
        '<p>Beersheba was the southernmost major city of biblical Israel, in the Negev desert — the southern boundary of the inhabited land in the recurring phrase <em>"from Dan even to Beersheba"</em> (<em>Judges 20:1; 1 Samuel 3:20; 2 Samuel 17:11</em>). Abraham planted a tamarisk tree there and called on the name of the Everlasting God (<em>El Olam</em>) after making a covenant of seven ewe lambs with Abimelech king of Gerar (<em>Genesis 21:31-33</em>; the name <em>Beer-Sheba</em> means "well of the oath" or "well of seven"). Isaac also dug wells there (<em>26:23-25</em>). Jacob offered sacrifices at Beersheba as he set out for Egypt to be reunited with Joseph (<em>46:1-5</em>). Centuries later, Elijah fled to Beersheba escaping Jezebel (<em>1 Kings 19:3</em>). A place of wells, covenants, and divine encounter.</p>'
    ),
    'ark-noah': (
        '<p>The Ark of Noah was the three-decked wooden vessel God commanded Noah to build for the salvation of his household and the animals during the deluge (<em>Genesis 6:14-22</em>) — 300 cubits long, 50 wide, 30 high (roughly 450 × 75 × 45 feet), with one door which God Himself shut behind Noah and his family (<em>7:16</em>). Built of <em>"gopher wood"</em> and sealed with pitch within and without, it housed Noah, his wife, his three sons and their wives (eight souls in all), and pairs of every kind of land animal and bird (with seven pairs of clean animals). It rested on the mountains of Ararat after 150 days. <em>1 Peter 3:20-21</em> draws baptism’s typological parallel: salvation by water through the appointed ark. Christ is the true Ark; outside Him there is no shelter from coming judgment.</p>'
    ),
    'salome-dancer': (
        '<p>Salome was the daughter of Herodias by her first husband Philip (Herod Antipas’s brother). At Antipas’s birthday banquet she danced before the king and his guests, pleased him, and at her mother’s prompting requested the head of John the Baptist on a charger (<em>Mark 6:21-29; Matthew 14:6-12</em>). Antipas, ashamed before his guests by the rash oath he had sworn, sent the executioner. John was beheaded in prison; the head was brought to Salome on a platter; she brought it to her mother. The gospels do not name her — only <em>"the daughter of the said Herodias"</em> — but Josephus names her Salome. She later married first Philip the tetrarch (Antipas’s half-brother) and then her cousin Aristobulus. The forerunner of Christ was murdered for a dance.</p>'
    ),
    'pilate-figure': (
        '<p>Pontius Pilate was the Roman prefect of Judea from AD 26 to 36 — the fifth Roman governor of the province, appointed under Tiberius. He is named four times in the New Testament epistles (<em>Acts 3:13; 4:27; 13:28; 1 Timothy 6:13</em>) and the Apostles’ Creed memorializes him by name: <em>"suffered under Pontius Pilate."</em> Under pressure from the Jewish leaders, he ordered the crucifixion of Jesus despite three explicit declarations of His innocence (<em>Luke 23:4, 14, 22</em>), washing his hands of the verdict (<em>Matthew 27:24</em>) and yielding to the cry <em>"Crucify him."</em> He is the New Testament case study of a man who saw the truth, said the truth, and refused to act on it. Removed from office in AD 36 after a massacre at Mount Gerizim; banished, by tradition died by suicide.</p>'
    ),
    'yahweh': (
        '<p><em>Yahweh</em> (יהוה, sometimes rendered <em>Jehovah</em> or <em>YHWH</em>) is the covenant, personal, self-existent name of the God of Israel — revealed at the burning bush to Moses as <em>"I AM THAT I AM"</em> (<em>Exodus 3:14</em>): <em>"Thus shalt thou say unto the children of Israel, I AM hath sent me unto you... this is my name for ever, and this is my memorial unto all generations"</em> (<em>3:14-15</em>). The name is bound permanently to the redemption of His people from Egypt: <em>"I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage"</em> (<em>20:2</em>). It appears nearly 7,000 times in the Old Testament. Out of reverence Jews stopped pronouncing it aloud, substituting <em>Adonai</em>; the KJV renders it <em>LORD</em> in small capitals. The Name is the LORD.</p>'
    ),
    'ecclesiastes': (
        '<p>Ecclesiastes is the Old Testament wisdom book commonly ascribed to Solomon in his old age — written from the perspective of <em>Qoheleth</em> ("the Preacher" or "Assembly-leader"). The book is structured around the keyword <em>hevel</em> (Hebrew "breath, vapor, smoke") — translated <em>"vanity"</em> in the KJV — appearing 38 times. The Preacher tests one domain of human life after another (wisdom, pleasure, work, wealth, power, religion) and pronounces each <em>"vanity and vexation of spirit"</em> when considered <em>"under the sun"</em> apart from God. The book closes with its only sufficient verdict: <em>"Let us hear the conclusion of the whole matter: Fear God, and keep his commandments: for this is the whole duty of man. For God shall bring every work into judgment"</em> (<em>12:13-14</em>). Vapor terminates in fearing God.</p>'
    ),
    'matthias': (
        '<p>Matthias was the disciple chosen by the eleven apostles in the days between the Ascension and Pentecost to fill the apostolic office vacated by Judas Iscariot (<em>Acts 1:15-26</em>). Peter cited <em>Psalm 109:8</em> as warrant: <em>"his bishoprick let another take."</em> Two candidates met the criterion — that he had accompanied them <em>"all the time that the Lord Jesus went in and out among us, beginning from the baptism of John, unto that same day that he was taken up from us"</em>. The two were Joseph called Barsabas (surnamed Justus) and Matthias. They prayed and cast lots; <em>"the lot fell upon Matthias; and he was numbered with the eleven apostles"</em> (<em>1:26</em>). Matthias appears no further in Scripture by name. Tradition variously places his ministry in Ethiopia or Cappadocia. The Twelve was complete by Pentecost.</p>'
    ),
    'simon-the-leper': (
        '<p>Simon the Leper was a resident of Bethany at whose house Christ was anointed by Mary of Bethany shortly before the Passion (<em>Matthew 26:6-13; Mark 14:3-9</em>). The text does not say whether he was a former leper Christ had healed (no leper would have lived in society or hosted a banquet under Levitical law) or whether the name had been retained from a prior identification. The likely answer: Christ had healed him, but the nickname stuck — a permanent memorial of grace. At the meal Mary broke an alabaster box of very precious spikenard and poured it on Christ’s head; some objected at the waste; Christ defended her: <em>"She is come aforehand to anoint my body to the burying. Verily I say unto you, Wheresoever this gospel shall be preached... this also that she hath done shall be spoken of for a memorial of her"</em>.</p>'
    ),
    'zelophehad-daughters': (
        '<p>Zelophehad’s daughters — Mahlah, Noah, Hoglah, Milcah, and Tirzah — were five sisters whose father died in the wilderness without sons (<em>Numbers 27:1-11</em>). They came to Moses and the assembly at the door of the tabernacle requesting a place in Israel’s tribal inheritance: <em>"Why should the name of our father be done away from among his family, because he hath no son? Give unto us therefore a possession among the brethren of our father."</em> Moses took the case before the LORD; the LORD ruled in their favor and established the principle as law for all Israel: where a man dies leaving daughters but no sons, his inheritance passes to his daughters. A later ruling (<em>Numbers 36</em>) added that they must marry within their father’s tribe to keep the inheritance in the tribe — which they did. Female inheritance under patriarchal order.</p>'
    ),
    'wesley-john': (
        '<p>John Wesley (1703-1791) was the Anglican priest, evangelist, and founder of Methodism. Converted at Aldersgate Street in London on May 24, 1738, when his heart was <em>"strangely warmed"</em> while listening to a reading of Luther’s preface to Romans, he began the open-air field-preaching that would mark his ministry. Over fifty years he rode an estimated 250,000 miles on horseback and preached more than 40,000 sermons. He organized converts into societies and class-meetings, sent itinerant lay preachers across England and to America, and remained an ordained Anglican to his death (though Methodism eventually separated). His theology was Arminian — Reformed Christians critique his denial of unconditional election and irresistible grace — but his emphasis on holiness, the witness of the Spirit, and small-group discipleship has shaped global Protestantism. His brother Charles wrote the hymns.</p>'
    ),
    'yahweh-yireh': (
        '<p><em>Yahweh-Yireh</em> (יְהוָה יִרְאֶה) — KJV <em>Jehovah-jireh</em>, "the LORD will provide" or "the LORD will see (and see to it)" — is the name Abraham gave Mount Moriah after God provided a ram in place of Isaac: <em>"And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen"</em> (<em>Genesis 22:14</em>). The Hebrew root <em>raah</em> ("to see") carries both <em>"see"</em> and <em>"see to it"</em> — God provides because God sees ahead. The name declares the LORD as the One who sees the need, sees the substitute, and supplies what no man could supply. The same mountain became the temple-site and the ground near which Christ — the true Lamb provided by God in our place — was sacrificed. Provision begins with God’s sight.</p>'
    ),
    'francis-of-assisi': (
        '<p>Francis of Assisi (c. 1181-1226) was the Italian merchant’s son who renounced his family wealth, embraced absolute poverty, and founded the Franciscan Order (the Order of Friars Minor) in 1209 with papal approval. After a youth of festivity, military service, and a serious illness, he heard the gospel call of <em>Matthew 10:7-10</em> — go, preach, take nothing — and obeyed it literally. He preached repentance and the kingdom across central Italy with bare feet and a rope-belted tunic, ministered to lepers (whom he had previously feared), composed the <em>Canticle of Brother Sun</em>, and reportedly received the stigmata on Mount La Verna two years before his death. Roman tradition makes him patron saint of animals and ecology; many sentimentalized modern renderings flatten his vigorous evangelistic preaching of repentance and judgment.</p>'
    ),
    'tamar': (
        '<p>Three biblical women bear the name Tamar. (1) <em>Tamar, daughter-in-law of Judah</em> — who, denied her levirate right after the deaths of Er and Onan, secured the Messianic line by disguising herself as a roadside prostitute and conceiving twins by Judah himself. Judah acknowledged: <em>"She hath been more righteous than I"</em> (<em>Genesis 38</em>). She is named in Christ’s genealogy (<em>Matthew 1:3</em>). (2) <em>Tamar, daughter of David and Maacah</em>, full sister of Absalom — raped by her half-brother Amnon in a pre-meditated act of feigned illness (<em>2 Samuel 13</em>); Absalom’s subsequent murder of Amnon set the rebellion in motion. (3) <em>Tamar, the daughter of Absalom</em> (<em>2 Samuel 14:27</em>) — named for her violated aunt. The name "palm tree" appears repeatedly in David’s house, in honor and in tragedy.</p>'
    ),
    'simon-of-cyrene': (
        '<p>Simon of Cyrene was a passerby — <em>"coming out of the country"</em> — almost certainly a North African Jew up to Jerusalem for the Passover, who was conscripted by the Roman soldiers to carry the cross of Jesus on the way to Golgotha. <em>"And as they came out, they found a man of Cyrene, Simon by name: him they compelled to bear his cross"</em> (<em>Matthew 27:32; Mark 15:21; Luke 23:26</em>). Mark adds the striking detail that he was <em>"the father of Alexander and Rufus"</em> — names evidently known to Mark’s Roman readers, suggesting Simon and his sons became believers (<em>Romans 16:13</em> greets <em>"Rufus chosen in the Lord, and his mother and mine"</em>). A man pressed into service to bear a stranger’s cross became, by grace, a father of believers.</p>'
    ),
    'amnon': (
        '<p>Amnon was David’s eldest son by Ahinoam of Jezreel, born in Hebron during David’s seven-and-a-half-year reign there (<em>2 Samuel 3:2</em>). He raped his half-sister Tamar, daughter of David and Maacah, in a pre-meditated act of feigned illness — sending all his attendants away and forcing her in his chamber (<em>2 Samuel 13:1-22</em>). The narrative is among the most disturbing in Scripture, deliberately echoing the language of <em>Genesis 39</em> (Joseph and Potiphar’s wife) with Amnon as the inverse anti-Joseph. David was furious but did nothing — a paternal failure that haunted the rest of his reign. Two years later, Absalom (Tamar’s full brother) had Amnon assassinated at a sheep-shearing feast in vengeance, and fled into exile. David’s sons reap what David sowed by silence.</p>'
    ),

    # === FIRST 5 GENERATIONAL ===
    'the-feels': (
        '<p>"The feels" is the catch-all noun-phrase for emotional response — especially response that the speaker cannot or does not bother to name precisely (<em>"that song hit me right in the feels"</em>). Common in pop-music captions, Millennial conversational style, and social-media reaction speech. The slang reveals a real category: feelings are real and worth honoring. Scripture acknowledges and engages emotion at depth (Christ wept; Paul yearned in the bowels of Christ; David’s Psalms feel out loud). The slang’s limitation is its <em>vagueness</em>. "The feels" treats feeling as an undifferentiated mood-blur rather than the precise affections Scripture names — sorrow, joy, gratitude, awe, anger, longing, grief. Christian men should learn the precise vocabulary Scripture uses. Don’t just feel <em>the feels</em>; name what you feel before God.</p>'
    ),
    'doomscrolling': (
        '<p>Doomscrolling is the habit of compulsively scrolling through negative content — news, social media, comment threads, world events — despite the scrolling itself producing distress, anxiety, and exhaustion. A modern pattern of the always-on smartphone era. The slang accurately diagnoses what it names: the soul is being fed something it cannot digest, and yet the thumb keeps swiping. Scripture has a different command for the mind: <em>"Finally, brethren, whatsoever things are true, whatsoever things are honest, whatsoever things are just, whatsoever things are pure, whatsoever things are lovely, whatsoever things are of good report... think on these things"</em> (<em>Philippians 4:8</em>). The remedy for doomscrolling is not <em>less</em> content but <em>better</em> content. Feed the mind on Scripture, theology, prayer, and the good works of the saints. Set the phone down.</p>'
    ),
    'five-finger-discount': (
        '<p>"Five-finger discount" is the Gen-X-era slang euphemism for shoplifting. The phrase’s mechanism is moral category-laundering: by calling theft a <em>discount</em>, the speaker softens the moral weight of what is biblically the eighth-commandment violation. <em>"Thou shalt not steal"</em> (<em>Exodus 20:15</em>; <em>Deuteronomy 5:19</em>) admits no euphemism. Paul names the cure: <em>"Let him that stole steal no more: but rather let him labour, working with his hands the thing which is good, that he may have to give to him that needeth"</em> (<em>Ephesians 4:28</em>). The repentance is not just stopping; it is reversing — the former thief becomes the giver, the laborer for others’ needs. Christian men refuse the euphemism. Theft is theft, whether by stealth in a store, by fraud at a desk, or by withholding wages at payroll.</p>'
    ),
    'mewing': (
        '<p>"Mewing" is a facial-posture exercise (tongue pressed against the roof of the mouth) believed by its advocates to reshape the jawline over time. Mainstream orthodontics is skeptical of the claimed effects. Gen-Z and male-aesthetics culture have embraced it as part of a broader "looksmaxxing" project — disciplined optimization of personal appearance. The Christian observation: bodily discipline is not forbidden but is sharply limited in eternal weight. <em>"For bodily exercise profiteth little: but godliness is profitable unto all things, having promise of the life that now is, and of that which is to come"</em> (<em>1 Timothy 4:8</em>). Effort spent reshaping the jaw is effort not spent reshaping the soul. <em>"Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised"</em> (<em>Proverbs 31:30</em>). Same for men.</p>'
    ),
    'foshizzle': (
        '<p>"Foshizzle" is the late-Gen-X / millennial affirmation phrase meaning <em>"for sure," "for certain," "yes absolutely."</em> Coined or popularized by hip-hop’s <em>-izzle</em> infix vocabulary (Snoop Dogg, early 2000s), now era-stamped and somewhat nostalgic. A small slang case of an honesty-marker: a verbal stamp on a claim or commitment, intensifying the speaker’s yes. Scripture commends plain yes-and-no speech (<em>Matthew 5:37</em>: <em>"Let your communication be, Yea, yea; Nay, nay: for whatsoever is more than these cometh of evil"</em>) — and the slang is a friendly violation of the principle, not a serious one. Christian men should aim for words their hearers trust without amplification. <em>"foshizzle"</em> is harmless; <em>"yes"</em> alone, from a man known for keeping his word, is heavier.</p>'
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
