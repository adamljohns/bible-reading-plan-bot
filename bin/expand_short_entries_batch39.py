#!/usr/bin/env python3
"""Batch 39 — expand 25 more entries from the 50-60 word bucket.

Targets: OT figures, NT figures, Hebrew vocab, hermeneutics,
solas, slang reframes, prophets, and biblical imagery.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'gideon-figure': (
        '<p>Gideon was a judge of Israel called from threshing wheat in a winepress (hiding from the Midianites) by the angel of the LORD: <em>"The LORD is with thee, thou mighty man of valour"</em> (<em>Judges 6:12</em>). He tore down the altar of Baal and the grove of Asherah his father had built (<em>6:25-32</em>). The LORD reduced his army from 32,000 to 300 by deliberate winnowing — <em>"lest Israel vaunt themselves against me, saying, Mine own hand hath saved me"</em> (<em>7:2</em>) — and the 300 with trumpets, pitchers, and torches routed the Midianite host. Gideon famously sought confirmation by the wet-and-dry fleeces (<em>6:36-40</em>); later he compromised by making a gold ephod that became a snare. <em>Hebrews 11:32</em> still names him in the faith-roll.</p>'
    ),
    'gird': (
        '<p>To <em>gird</em> is to bind around the waist — and in Scripture, especially to <em>gird the loins</em>: tucking up the long flowing robe under a belt to prepare for vigorous action, work, or battle. The verb is idiomatic for "prepare yourself for what is coming." Israel ate the first Passover with their <em>"loins girded"</em> (<em>Exodus 12:11</em>), ready to march out. Paul lists girding first in the armor of God: <em>"Stand therefore, having your loins girt about with truth"</em> (<em>Ephesians 6:14</em>). Peter applies it to the mind: <em>"Wherefore gird up the loins of your mind, be sober, and hope to the end for the grace that is to be brought unto you at the revelation of Jesus Christ"</em> (<em>1 Peter 1:13</em>). Tuck the long thoughts in. Move.</p>'
    ),
    'glaze': (
        '<p>"Glaze" is current slang for excessive, sycophantic praise — usually directed at someone the speaker does not know personally but wants to appear devoted to (<em>"the glaze on this guy is unbelievable"</em>). The slang is mocking. Scripture has its own word: <em>flattering lips</em>. <em>"A flattering mouth worketh ruin"</em> (<em>Proverbs 26:28</em>); <em>"a man that flattereth his neighbour spreadeth a net for his feet"</em> (<em>Proverbs 29:5</em>). The slang is right that the practice is unattractive. What it misses is the deeper biblical concern: glaze is worship-misdirection — devotion that belongs to God redirected toward a celebrity, athlete, or influencer. Scripture treats it as a soul-trap, not merely a social mistake. Stop glazing. Worship the King alone.</p>'
    ),
    'godly-fear': (
        '<p>Godly fear is the reverent dread proper to a creature before the Holy God — not slavish terror, not casual familiarity, but the weight of recognized holiness. Hebrews names it as the manner of acceptable New-Covenant service: <em>"Wherefore we receiving a kingdom which cannot be moved, let us have grace, whereby we may serve God acceptably with reverence and godly fear: for our God is a consuming fire"</em> (<em>Hebrews 12:28-29</em>). Solomon names it as the beginning of wisdom: <em>"The fear of the LORD is the beginning of wisdom: and the knowledge of the holy is understanding"</em> (<em>Proverbs 9:10</em>). The man without godly fear may be religious; he is not yet wise — and he is not yet ready to serve.</p>'
    ),
    'goel-redeemer': (
        '<p><em>Goel ha-Dam</em> ("redeemer of blood") was the Mosaic-law office of the kinsman responsible for executing justice on the slayer of a blood-relative (<em>Numbers 35:19-27</em>). Strikingly, the same Hebrew word <em>goel</em> names the kinsman-redeemer who buys back forfeited family land (<em>Leviticus 25:25</em>) and who marries the brother’s widow under levirate law (<em>Deuteronomy 25:5-10; Ruth 4</em>). One word, three offices: avenger of blood, redeemer of land, marrier of widow. All three converge in Christ: He avenges His people’s blood at the final judgment (<em>Revelation 6:9-11</em>), He redeems the forfeited inheritance (<em>Ephesians 1:14</em>), and He marries the bride (<em>Ephesians 5:25-32</em>). The whole institution is christological.</p>'
    ),
    'mammon': (
        '<p>Mammon is the Aramaic word for wealth — used by Christ to name money treated as a rival deity. <em>"No man can serve two masters: for either he will hate the one, and love the other; or else he will hold to the one, and despise the other. Ye cannot serve God and mammon"</em> (<em>Matthew 6:24</em>; <em>Luke 16:13</em>). Mammon is not money simply; it is money <em>with claims of devotion</em> — money positioned to receive trust, obedience, and worship that belong to God alone. Christ names it as a personal master, not a neutral tool — a god in the soul’s pantheon. The household chooses daily which master it serves. The Christian uses money; he does not <em>serve</em> it.</p>'
    ),
    'mezuzah': (
        '<p><em>Mezuzah</em> is the Hebrew word for <em>doorpost</em> (<em>Exodus 12:7</em>; <em>Deuteronomy 6:9</em>). In rabbinic and modern Jewish practice it is also the small parchment-and-case fastened to the right side of every Jewish doorway, bearing the words of the <em>Shema</em> (<em>Deuteronomy 6:4-9; 11:13-21</em>) — literally obeying the command: <em>"And thou shalt write them upon the posts of thy house, and on thy gates"</em> (<em>Deuteronomy 6:9</em>). Christians have generally let the word fall away — but the underlying command, that the Word of God should be visibly attached to our houses, remains. Frame Scripture on the walls; mark the household visibly as a house under God. The threshold preaches.</p>'
    ),
    'micah-prophet': (
        '<p>Micah was the eighth-century BC prophet from Moresheth in southwestern Judah, contemporary with Isaiah, Hosea, and Amos. His book prophesied to both Israel (the northern kingdom) and Judah (the southern), condemning oppression of the poor, corrupt judges and priests, and false prophets <em>"that bite with their teeth"</em> for hire (<em>Micah 3:5</em>). Three of his oracles are especially famous. <em>Micah 5:2</em>: <em>"But thou, Bethlehem Ephratah... out of thee shall he come forth unto me that is to be ruler in Israel"</em> — the Bethlehem prophecy. <em>Micah 6:8</em>: <em>"to do justly, and to love mercy, and to walk humbly with thy God."</em> <em>Micah 4:1-3</em>: the mountain of the LORD’s house in the last days (paralleled in <em>Isaiah 2</em>). Judgment and hope alternate.</p>'
    ),
    'mood': (
        '<p>"Mood" is one-word slang for identification with a feeling state — usually a relatable, mild misery (tired, overwhelmed, lazy, sad-but-fine). <em>"That’s a mood"</em> = "I identify with that feeling." The slang treats whatever the speaker is feeling as final reality, the floor of the soul beneath which there is nothing else to consult. Scripture treats feelings as real and worth honoring — Christ wept, sorrowed, rejoiced, was indignant — but never as the bottom layer. Underneath the feeling sits the <em>heart</em>; underneath the heart sits the <em>Lord</em>. <em>"Why art thou cast down, O my soul? and why art thou disquieted in me? hope thou in God: for I shall yet praise him"</em> (<em>Psalm 42:5, 11; 43:5</em>). The Christian speaks to his mood; he is not ruled by it.</p>'
    ),
    'mordechai': (
        '<p>Mordecai was the Jewish cousin and adoptive father of Esther, a faithful Jew in the Persian court of Xerxes (Ahasuerus). He refused to bow to Haman the Agagite, prompting Haman’s genocidal plot against all the Jews of the empire (<em>Esther 3:1-6</em>). Mordecai counseled Esther’s intervention with the famous words: <em>"Who knoweth whether thou art come to the kingdom for such a time as this?"</em> (<em>Esther 4:14</em>). Through Esther’s courage and Mordecai’s vigilance, Haman was hanged on the gallows he had built for Mordecai, and the Jews were delivered. Mordecai was honored at the king’s table, dressed in royal robes, and rose to second-in-kingdom (<em>Esther 10:3</em>). Providence works through quiet faithfulness.</p>'
    ),
    'muster-biblical': (
        '<p>To <em>muster</em> is to call together, count, and inspect — the formal showing of troops by name and number. Israel was mustered repeatedly under God’s command. At Sinai shortly after the Exodus (<em>Numbers 1</em>): 603,550 fighting men. In the plains of Moab before entering the land (<em>Numbers 26</em>): 601,730. And in David’s ill-advised muster of Israel and Judah, conducted out of pride against the LORD’s wisdom — for which David was severely chastened (<em>2 Samuel 24; 1 Chronicles 21</em>). The kingdom of God musters its saints in every generation — and a day is coming when every name will be read from the Lamb’s book of life. Christian men should expect to be counted.</p>'
    ),
    'nahum-prophet': (
        '<p>Nahum was a seventh-century BC prophet (c. 650-630 BC) whose three-chapter book is a sustained oracle of divine judgment against Nineveh, the capital of Assyria. A century after Jonah’s reluctant preaching had brought a generation of Ninevite repentance, the city had returned to its native violence and pride — and Nahum announces its complete and irreversible destruction: <em>"The burden of Nineveh... The LORD is jealous, and the LORD revengeth"</em> (<em>Nahum 1:1-2</em>). The prophecy was fulfilled with terrible precision in 612 BC when the Babylonians and Medes under Nabopolassar destroyed Nineveh utterly — so completely that for centuries its very site was forgotten. <em>"Woe to the bloody city! it is all full of lies and robbery"</em> (<em>Nahum 3:1</em>). God remembers and ends.</p>'
    ),
    'oil-lamp': (
        '<p>The oil lamp was the small clay or metal vessel that held olive oil and a wick — the household’s primary light after sundown for most of biblical history. Scripture freights it with theological weight. The lamp of David that would not be quenched (<em>1 Kings 11:36; 15:4; 2 Kings 8:19</em>) — the covenantal promise of an unending Davidic line. The five wise virgins’ lamps with oil ready, contrasted with the foolish whose oil ran out (<em>Matthew 25:1-13</em>). <em>"The light of the body is the eye"</em> (<em>Matthew 6:22</em>), with the lamp of the body as the figure. And the new Jerusalem: <em>"the city had no need of the sun, neither of the moon, to shine in it: for the glory of God did lighten it, and the Lamb is the light thereof"</em> (<em>Revelation 21:23</em>).</p>'
    ),
    'philip': (
        '<p>Two New Testament men bear the name Philip. First, <em>Philip the apostle</em> from Bethsaida in Galilee — who brought his friend Nathanael to Christ saying, <em>"Come and see"</em> (<em>John 1:43-46</em>), pointed out the lad with five loaves and two fish (<em>John 6:5-7</em>), and inquired, <em>"Lord, shew us the Father, and it sufficeth us"</em> (<em>John 14:8</em>). Second, <em>Philip the evangelist</em> — one of the seven Spirit-filled deacons (<em>Acts 6:5</em>), the first to preach the gospel in Samaria where revival broke out (<em>Acts 8:5-13</em>), supernaturally transported to meet the Ethiopian eunuch in the desert (<em>8:26-40</em>), and host to Paul’s band at Caesarea where his four virgin daughters prophesied (<em>21:8-9</em>). Both Philips show the gospel’s reach.</p>'
    ),
    'phoebe': (
        '<p>Phoebe was a <em>diakonos</em> ("deaconess") of the church at Cenchrea — the harbor of Corinth — commended by Paul at the opening of Romans 16: <em>"I commend unto you Phebe our sister, which is a servant [diakonos] of the church which is at Cenchrea: That ye receive her in the Lord, as becometh saints, and that ye assist her in whatsoever business she hath need of you: for she hath been a succourer of many, and of myself also"</em> (<em>Romans 16:1-2</em>). The Greek <em>prostatis</em> (<em>"succourer"</em>) suggests significant standing — perhaps wealthy patroness. She was almost certainly the carrier of the letter to the Romans across the Mediterranean — the woman who delivered the most theologically dense letter in the New Testament to its destination.</p>'
    ),
    'plain-sense': (
        '<p>Plain sense is the natural, direct meaning of a biblical text — what an ordinary reader, attending to grammar, context, and genre, would understand. The Reformers championed plain-sense reading against medieval allegorizing that loaded texts with hidden moral and mystical meanings on top of the literal. <em>"The grammatical sense alone is the true and proper sense"</em> (Luther). Plain-sense reading includes figurative speech read figuratively, narrative read as narrative, poetry as poetry, parable as parable — not flat-footed literalism, but ordinary intelligent reading honoring what the author intended his words to mean. Tyndale: <em>"the literal sense is the root and ground of all, and the anchor that never faileth, whereunto if thou cleave thou canst never err."</em></p>'
    ),
    'prince-peace': (
        '<p>"Prince of Peace" is Isaiah’s Messianic title for the coming Christ: <em>"For unto us a child is born, unto us a son is given: and the government shall be upon his shoulder: and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace"</em> (<em>Isaiah 9:6</em>). The next verse continues: <em>"Of the increase of his government and peace there shall be no end"</em> (<em>v. 7</em>). The peace He brings is not as the world gives (<em>John 14:27</em>) — not negotiated cessation of hostilities, not stoic equanimity, but <em>shalom</em>: wholeness, rightness, covenant restoration. Christ is the only Prince whose peace expands rather than contracts. His war on sin produces His peace in the soul.</p>'
    ),
    'prophetess': (
        '<p>A prophetess is a woman who prophesies under divine appointment. Scripture names them across both Testaments. Miriam, sister of Moses, after the Red Sea (<em>Exodus 15:20</em>). Deborah, judge of Israel (<em>Judges 4:4</em>). Huldah, consulted by Josiah’s reformers about the rediscovered scroll (<em>2 Kings 22:14</em>). Isaiah’s wife (<em>Isaiah 8:3</em>). Anna at the temple, who greeted the infant Christ (<em>Luke 2:36-38</em>). Philip the evangelist’s four virgin daughters (<em>Acts 21:9</em>). Joel’s great Pentecost prophecy promised: <em>"your sons and your daughters shall prophesy"</em> (<em>Joel 2:28</em>) — cited as fulfilled by Peter at Pentecost (<em>Acts 2:17</em>). The Spirit gives prophetic gift across the male/female line; church order remains intact.</p>'
    ),
    'prostrate': (
        '<p>To be <em>prostrate</em> is to lie face-down on the ground in worship, repentance, or terror — the deepest physical posture of submission Scripture records. Abram fell on his face when God spoke (<em>Genesis 17:3, 17</em>). Moses and Aaron fell on their faces at Korah’s rebellion (<em>Numbers 16:4, 22, 45</em>). Joshua fell prostrate before the Captain of the Host outside Jericho (<em>Joshua 5:14</em>). Daniel fell on his face when Gabriel came (<em>Daniel 8:17; 10:9</em>). The twenty-four elders of <em>Revelation 4:10</em> fall down before the throne and cast their crowns. Christ Himself <em>"fell on his face, and prayed"</em> in Gethsemane (<em>Matthew 26:39</em>). Modern Christianity has nearly lost the posture; the recovery costs little and reorients much.</p>'
    ),
    'proverbs': (
        '<p>Proverbs is the Old Testament wisdom book of pithy aphorisms — mostly two-line couplets, sometimes longer poems — chiefly attributed to Solomon (chs. 1-29) with appendices from Agur (ch. 30) and King Lemuel’s mother (ch. 31). The collection is arranged to instruct the simple in the fear of the LORD, contrasting wisdom and folly across every domain of life: speech, money, sex, work, friendship, parenting, government, anger, planning, generosity, drinking, marriage. The book opens with its keynote and never abandons it: <em>"The fear of the LORD is the beginning of knowledge: but fools despise wisdom and instruction"</em> (<em>Proverbs 1:7</em>). Christian fathers should teach their sons this book line by line.</p>'
    ),
    'redemptive-historical': (
        '<p>Redemptive-Historical hermeneutics reads Scripture as a <em>unified narrative</em> of God’s redemptive acts unfolding in history — creation, fall, covenant with Abraham, exodus, Sinai, monarchy, exile, return, Christ, church, consummation — climaxing decisively in Christ. Each text is interpreted in its place in the storyline. Geerhardus Vos and the Westminster theologians developed the discipline; Edmund Clowney, Sidney Greidanus, and Tim Keller popularized it for preaching. Christ Himself is the storyline’s climax (<em>Luke 24:27</em>: <em>"beginning at Moses and all the prophets, he expounded unto them in all the scriptures the things concerning himself"</em>). Every text therefore contributes, in its way, to His revelation. The Bible is one book — and the central character has always been Jesus.</p>'
    ),
    'reveille': (
        '<p>Reveille is the morning call — bugle, drum, fife, or now whistle — that wakes a military unit at dawn for the day’s service. Scripture has its reveille verses. <em>"Awake thou that sleepest, and arise from the dead, and Christ shall give thee light"</em> (<em>Ephesians 5:14</em>) — the gospel summons to spiritual life. <em>"Awake up, my glory; awake, psaltery and harp: I myself will awake early"</em> (<em>Psalm 57:8; 108:2</em>) — the worshiper’s self-summons. <em>"Awake to righteousness, and sin not"</em> (<em>1 Corinthians 15:34</em>) — the apostolic alarm. The kingdom calls its saints to rise. Christian men learn early rising not as cultural pose but as bodily reveille — answering the King’s summons before the world begins to call.</p>'
    ),
    'solus-christus': (
        '<p><em>Solus Christus</em> ("Christ alone") is the Reformation doctrine that Jesus Christ is the sole mediator between God and man, and that salvation is accomplished only through His atoning life, death, and resurrection. <em>"For there is one God, and one mediator between God and men, the man Christ Jesus"</em> (<em>1 Timothy 2:5</em>); <em>"Neither is there salvation in any other: for there is none other name under heaven given among men, whereby we must be saved"</em> (<em>Acts 4:12</em>). The doctrine asserts that Christ’s sacrifice is fully <em>sufficient</em> and fully <em>exclusive</em> — no other person, institution, sacrament, or work can add to what He has accomplished. Rome’s priesthood, Mariolatry, indulgences, and treasury of merit all fall under <em>solus Christus</em>’s rebuke.</p>'
    ),
    'stretched-out-hand': (
        '<p>The "stretched-out hand" (or <em>"outstretched arm"</em>) is the great Old Testament emblem of the LORD’s active power — the arm extended in deliverance to His people and in judgment to His enemies. Israel was redeemed from Egypt <em>"with a mighty hand, and with a stretched out arm"</em> (<em>Deuteronomy 4:34; 5:15; 7:19; Psalm 136:12</em>). The phrase becomes covenantal shorthand for the Exodus and every subsequent act of YHWH’s redemption. The early church in Jerusalem prayed for that same hand to be stretched out for healing and signs: <em>"By stretching forth thine hand to heal; and that signs and wonders may be done by the name of thy holy child Jesus"</em> (<em>Acts 4:30</em>). The hand is still extended; the saint may still ask it to act.</p>'
    ),
    'tamar-judah': (
        '<p>Tamar was the Canaanite daughter-in-law of Judah, son of Jacob — widowed twice in quick succession (by Er and then by Onan) and then denied levirate marriage to the third son Shelah by Judah’s reluctance (<em>Genesis 38</em>). Recognizing the injustice and pressed by the years, Tamar disguised herself as a roadside prostitute and conceived twins by Judah himself, taking his signet, bracelets, and staff as pledges. When her pregnancy was reported, Judah ordered her burned — until she produced his pledge-objects. He confessed: <em>"She hath been more righteous than I; because that I gave her not to Shelah my son"</em> (<em>v. 26</em>). She bore Pharez and Zarah; Pharez stands in Christ’s royal genealogy (<em>Matthew 1:3</em>). Gentile women are grafted in.</p>'
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
