#!/usr/bin/env python3
"""Batch 24 — expand 25 more thin entries to 90-110 words each.

Targets: Hebrew vocabulary, OT events, Christology, women named in
the NT, virtues, offerings, and divine names from the 30-50 word
bucket. Brings the session total to 600.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'qadosh': (
        '<p><em>Qadosh</em> (קָדוֹשׁ) is the Hebrew word for <em>holy</em> — literally <em>"set apart, cut off, separated."</em> It is YHWH’s primary self-revelation. In the seraphic vision of <em>Isaiah 6:3</em> the angels cry without ceasing: <em>"Holy, holy, holy, is the LORD of hosts: the whole earth is full of his glory."</em> The triple repetition is the Hebrew superlative — most-holy, utterly holy — naming His total otherness from creation. Israel is to be <em>qadosh</em> because YHWH is <em>qadosh</em>: <em>"Ye shall be holy: for I the LORD your God am holy"</em> (<em>Leviticus 19:2</em>; cf. <em>1 Peter 1:15-16</em>). Holiness is therefore not generic moral excellence; it is set-apartness for God — a people, a place, a time, a use that God claims as His own.</p>'
    ),
    'teach': (
        '<p>To <em>teach</em> is to impart instruction — and Scripture treats teaching as a divine activity flowing down into ordained channels. The Spirit teaches the saints directly through the Word: <em>"the anointing which ye have received of him abideth in you, and ye need not that any man teach you... the same anointing teacheth you of all things"</em> (<em>1 John 2:27</em>). Christ taught with authority, <em>"not as the scribes"</em> (<em>Matthew 7:29</em>). The risen Christ gave to the church appointed teachers — pastor-teachers — as a gift to the body (<em>Ephesians 4:11-12</em>; <em>1 Corinthians 12:28</em>). Teaching is also a daily household reality: <em>"thou shalt teach them diligently unto thy children"</em> (<em>Deuteronomy 6:7</em>). Fathers teach; pastors teach; older women teach younger women.</p>'
    ),
    'tehillah': (
        '<p><em>Tehillah</em> (תְּהִלָּה) is the Hebrew word for praise — specifically <em>sung</em>, <em>declared</em>, public praise. It comes from the verb <em>halal</em>, the root of <em>hallelujah</em> ("praise YHWH"). The Book of Psalms is called in Hebrew <em>Tehillim</em> — "Praises" — though it contains many laments and petitions, because praise is the genre’s ultimate posture. <em>Tehillah</em> is what the saint owes God for who He is and what He has done. <em>"My mouth shall speak the praise [tehillah] of the LORD: and let all flesh bless his holy name"</em> (<em>Psalm 145:21</em>). The redeemed in Revelation sing it endlessly (<em>5:9-14; 19:1-7</em>). Where God’s people are silent, creation will cry out (<em>Luke 19:40</em>). Open your mouth.</p>'
    ),
    'ten-plagues': (
        '<p>The Ten Plagues were the escalating series of judgments God brought upon Egypt to deliver Israel and to display His supremacy over the gods of the land (<em>Exodus 7-12</em>): water to blood, frogs, lice, flies, livestock pestilence, boils, hail, locusts, darkness, and the death of the firstborn. Each plague targeted a specific Egyptian deity — Hapi the Nile-god, Heqet the frog-goddess, Geb the earth-god, Ra the sun-god, and finally Pharaoh himself, considered a son of the gods. The LORD said <em>"against all the gods of Egypt I will execute judgment: I am the LORD"</em> (<em>Exodus 12:12</em>). The tenth plague was answered by the Passover lamb’s blood on the lintel and doorposts — and Israel marched out free.</p>'
    ),
    'viper': (
        '<p>The viper is a venomous serpent of the desert, often striking from concealment — and in Scripture it becomes the unflattering metaphor John the Baptist and Jesus used for unrepentant religious leaders. <em>"O generation of vipers, who hath warned you to flee from the wrath to come?"</em> (<em>Matthew 3:7</em>; <em>Luke 3:7</em>); <em>"Ye serpents, ye generation of vipers, how can ye escape the damnation of hell?"</em> (<em>Matthew 23:33</em>). The image is sharp: religion that hides venom under a cloak of piety. The literal viper bit Paul on Malta after the shipwreck, and could not harm him (<em>Acts 28:3-6</em>) — fulfilling Christ’s promise of <em>Mark 16:18</em> and signaling that the gospel had reached the nations.</p>'
    ),
    'confess': (
        '<p>To <em>confess</em> is literally to <em>say the same thing</em> as another — the Greek <em>homologeō</em> (<em>homo</em>, "same"; <em>logos</em>, "word"). Scripture builds two parallel uses of the verb on this root meaning. Confession of <em>sin</em>: saying the same thing about it as God does — agreeing with His verdict, refusing to minimize or rename it. <em>"If we confess our sins, he is faithful and just to forgive us our sins"</em> (<em>1 John 1:9</em>). Confession of <em>Christ</em>: saying the same thing about Him as the Father does — that He is Lord, that He is the Son. <em>"Whosoever therefore shall confess me before men, him will I confess also before my Father"</em> (<em>Matthew 10:32</em>; cf. <em>Romans 10:9-10</em>). Both confessions run on the same verb.</p>'
    ),
    'ezra-book': (
        '<p>The book of Ezra recounts in two movements the great post-exilic return. Chapters 1-6 record the first return under Zerubbabel (538 BC) and the rebuilding of the temple — laying the foundation, encountering Samaritan opposition, halting under Persian decree, resuming under Haggai and Zechariah’s preaching, and completing the second temple in 516 BC. Chapters 7-10 narrate Ezra’s later return (458 BC) as priest-scribe-teacher, his commission from Artaxerxes, his journey, and his reform of the people — confronting the scandal of mixed marriages with pagan women (<em>Ezra 9-10</em>). The book opens with one of Scripture’s most striking lines: <em>"The LORD stirred up the spirit of Cyrus king of Persia"</em> (<em>Ezra 1:1</em>). Pagan kings serve covenant purposes.</p>'
    ),
    'impeccability-christ': (
        '<p>The impeccability of Christ is the orthodox doctrine that Jesus, though <em>"tempted in all points like as we are"</em>, was not only sinless but <em>incapable</em> of sin: <em>"yet without sin"</em> (<em>Hebrews 4:15</em>). The temptations in the wilderness, in Gethsemane, and at the cross were real — He suffered them — but the failure was metaphysically impossible. He is one Person with two natures, fully God and fully man, and the divine Person cannot deny Himself: <em>"if we believe not, yet he abideth faithful: he cannot deny himself"</em> (<em>2 Timothy 2:13</em>). Impeccability is the indispensable foundation of the gospel — the sinless Lamb is the only sufficient sacrifice (<em>1 Peter 1:19</em>), and the impeccable Advocate is the only trustworthy Mediator (<em>1 John 2:1</em>).</p>'
    ),
    'levitical-priesthood': (
        '<p>The Levitical priesthood is the priestly order descended from Aaron — set apart from the larger tribe of Levi — to mediate between God and Israel through sacrifice, intercession, and instruction in the law. The Levites who were not Aaron’s descendants served as the priests’ assistants (gatekeepers, singers, musicians, transporters, teachers), but only Aaron’s sons could approach the altar (<em>Numbers 18:1-7</em>). The order was hereditary, male, and bound by strict purity laws. The Levitical priesthood served until it was fulfilled and superseded by the priesthood of Christ after the order of Melchizedek (<em>Hebrews 7</em>). The shadow has yielded to substance: <em>"there is one God, and one mediator between God and men, the man Christ Jesus"</em> (<em>1 Timothy 2:5</em>).</p>'
    ),
    'mercy-biblical': (
        '<p>Biblical mercy is lovingkindness directed at the miserable — kindness that meets a creature where weakness, need, or guilt has put it. The Hebrew <em>chesed</em> covers covenant loyalty extended even when undeserved; the Greek <em>eleos</em> covers compassion stooping to the wounded. Christ’s ministry was a continual flow of such mercy: <em>"I will have mercy, and not sacrifice"</em> (<em>Matthew 9:13; 12:7</em>; quoting <em>Hosea 6:6</em>). Mercy is the recurring cry of those who would be saved: blind Bartimaeus (<em>Mark 10:47-48</em>), the ten lepers (<em>Luke 17:13</em>), the publican (<em>Luke 18:13</em>). Mercy is also a Christian duty: <em>"Blessed are the merciful: for they shall obtain mercy"</em> (<em>Matthew 5:7</em>). The merciful are children of the Father (<em>Luke 6:36</em>).</p>'
    ),
    'mount-gerizim': (
        '<p>Mount Gerizim was the mountain near Shechem from which the blessings of the covenant were pronounced when Israel first entered the promised land. Moses commanded that six tribes — Simeon, Levi, Judah, Issachar, Joseph, and Benjamin — stand on Gerizim to say <em>Amen</em> to the blessings, while six other tribes stood on Mount Ebal opposite to say <em>Amen</em> to the curses (<em>Deuteronomy 27:11-13</em>; <em>Joshua 8:33</em>). Gerizim later became the alternative worship-center of the Samaritans, who built a rival temple there in the fourth century BC. The Samaritan woman at the well asked Jesus about it: <em>"Our fathers worshipped in this mountain; and ye say, that in Jerusalem is the place where men ought to worship"</em> (<em>John 4:20</em>). Christ reframed the question entirely.</p>'
    ),
    'narcissism': (
        '<p>Narcissism is excessive self-focus and self-love — clinically, a personality disorder marked by grandiosity, lack of empathy, exploitation of others, and an insatiable need for admiration. The name comes from the Greek myth of Narcissus, who drowned staring at his own reflection. The term is now deployed widely as diagnosis-by-internet for difficult relationships, often misapplied. The deeper biblical category is older: Augustine called it <em>incurvatus in se</em> — <em>"curved in on the self"</em> — the universal fallen condition in which the soul collapses inward toward itself instead of outward toward God and neighbor. Only grace uncurves the soul, reorienting it toward worship and love. Self-focus is the disease; cross-shaped self-forgetfulness is the cure.</p>'
    ),
    'onesiphorus': (
        '<p>Onesiphorus appears in <em>2 Timothy 1:16-18</em> as a saint Paul especially commends: <em>"The Lord give mercy unto the house of Onesiphorus; for he oft refreshed me, and was not ashamed of my chain: but, when he was in Rome, he sought me out very diligently, and found me. The Lord grant unto him that he may find mercy of the Lord in that day: and in how many things he ministered unto me at Ephesus, thou knowest very well."</em> Onesiphorus is the model of the unspectacular saint whose ministry is to <em>refresh</em> the apostle — finding Paul in his Roman prison, owning the shame of the chain, repeatedly serving. Every faithful pastor remembers his Onesiphori with deep, tearful gratitude. Be one.</p>'
    ),
    'patience-biblical': (
        '<p>Biblical patience is the capacity to remain under pressure without breaking — whether the pressure is hostile (longsuffering toward people) or simply long (endurance under God’s timing). The Greek distinguishes the two: <em>makrothumia</em> ("long-tempered, slow-fuse") for forbearance with persons, and <em>hupomonē</em> ("remaining under") for steadfast endurance under circumstance. Both are fruit of the Spirit (<em>Galatians 5:22</em>) and both adorn Christ (<em>1 Timothy 1:16</em>). Paul writes: <em>"Be patient toward all men"</em> (<em>1 Thessalonians 5:14</em>); James, <em>"Be patient therefore, brethren, unto the coming of the Lord"</em> (<em>James 5:7</em>). The Christian husband is patient with his wife; the father with his children; the pastor with his flock. Patience is the love-form of time.</p>'
    ),
    'perpetual-fire': (
        '<p>The perpetual fire was the altar fire God commanded never to go out: <em>"The fire shall ever be burning upon the altar; it shall never go out"</em> (<em>Leviticus 6:13</em>). The priests trimmed it morning and evening, fed it with wood, and tended its ashes — a continuous flame from Sinai through Solomon to the second temple. The perpetual fire is the type of every fire God Himself lights and tells His people to tend: the household altar of family worship, the watchman’s post against false teaching, the inner devotion of the saint that refuses to grow cold. <em>"Quench not the Spirit"</em> (<em>1 Thessalonians 5:19</em>). The Christian man does not produce the fire; he tends what God has lit and never lets it die.</p>'
    ),
    'pit': (
        '<p>A pit, in Scripture, is a deep hole in the earth — and the literal image becomes a recurring figure for death, <em>Sheol</em>, and ultimate divine judgment. Literally: Joseph was thrown into a pit by his brothers (<em>Genesis 37:24</em>); Jeremiah was lowered into Malchiah’s muddy cistern (<em>Jeremiah 38:6</em>). Figuratively: <em>"I waited patiently for the LORD... He brought me up also out of an horrible pit"</em> (<em>Psalm 40:1-2</em>); the wicked <em>"made a pit, and digged it, and is fallen into the ditch which he made"</em> (<em>Psalm 7:15</em>). The "pit" or "abyss" of Revelation 9 and 20 is the prison of demonic powers, sealed and bottomless. Christ holds its keys (<em>Revelation 1:18</em>); no one comes out unauthorized.</p>'
    ),
    'recompense': (
        '<p>To recompense is to repay, render equivalent, balance the scales — a judicial verb. In Scripture it is used both of God’s just repayment of evil with judgment and of good with reward, and of restitution made by sinners to those they have wronged. <em>"Vengeance is mine; I will repay [recompense], saith the Lord"</em> (<em>Romans 12:19</em>; quoting <em>Deuteronomy 32:35</em>) takes vengeance out of the saint’s hand and places it in God’s. The Mosaic law required restitution: <em>"they shall confess their sin which they have done: and he shall recompense his trespass with the principal thereof, and add unto it the fifth part thereof"</em> (<em>Numbers 5:7</em>). Balance is the gospel’s shape: Christ recompensed our debt in full at the cross.</p>'
    ),
    'rose': (
        '<p>The rose, in Scripture, is a wild meadow-bloom of the plain of Sharon. In the Song of Solomon, the bride identifies herself: <em>"I am the rose of Sharon, and the lily of the valleys"</em> (<em>Song 2:1</em>) — applied by the Christian tradition to the bride of Christ and, through her, to her Bridegroom: <em>"the Rose of Sharon"</em> became one of the church’s favorite Christological titles. Isaiah foresees the desert blooming under the messianic age: <em>"The wilderness and the solitary place shall be glad for them; and the desert shall rejoice, and blossom as the rose"</em> (<em>Isaiah 35:1</em>). Where Christ comes, life returns to dry land; where He reigns, the desert rejoices. The Rose blooms in the wilderness.</p>'
    ),
    'still-waters': (
        '<p>"Still waters" is <em>Psalm 23:2</em>’s image of YHWH as Shepherd leading the saint beside calm, drinkable water: <em>"he leadeth me beside the still waters."</em> The Hebrew <em>mei menuchot</em> is literally <em>"waters of rest"</em> or <em>"resting-waters"</em> — quiet pools, side channels, gently flowing streams. Sheep cannot drink from rushing or muddy water; they refuse it. The Shepherd seeks out the still places where the flock can be refreshed without fear. Christian souls likewise must be led to still waters — the steady draught of Scripture and prayer, the unrushed sabbath, the quiet conversation with a trusted brother. The man who tries to drink from his own torrent of busyness will die of thirst beside the river. Slow down. Drink.</p>'
    ),
    'striking-thigh': (
        '<p>Striking the thigh is an Old Testament gesture of deep remorse, dismay, or prophetic instruction. Ephraim, in Jeremiah’s great repentance text, says: <em>"Surely after that I was turned, I repented; and after that I was instructed, I smote upon my thigh: I was ashamed, yea, even confounded, because I did bear the reproach of my youth"</em> (<em>Jeremiah 31:19</em>). Ezekiel is commanded to dramatize judgment: <em>"smite with thine hand, and stamp with thy foot, and say, Alas for all the evil abominations of the house of Israel!"</em> (<em>Ezekiel 6:11</em>; cf. <em>21:12</em>). The gesture is bodily — the soul’s grief brought outward to the limb. Christian repentance still needs the body. Tears, fasting, kneeling — and yes, the slap of a hand on the thigh.</p>'
    ),
    'syntyche': (
        '<p>Syntyche was a Christian sister at Philippi whom Paul names alongside Euodia in his closing exhortation: <em>"I beseech Euodias, and beseech Syntyche, that they be of the same mind in the Lord. And I intreat thee also, true yokefellow, help those women which laboured with me in the gospel... whose names are in the book of life"</em> (<em>Philippians 4:2-3</em>). Like Euodia, Syntyche had labored with Paul in the gospel — apparently in significant ministry — yet some disagreement had divided them. Paul does not take sides; he calls both to oneness in the Lord. The pastoral note teaches that even fruitful gospel workers can be at odds, and that the church’s call is always to reconciliation under the Lord whose names they bear.</p>'
    ),
    'table-fellowship': (
        '<p>Table fellowship is the act of eating with another as an expression of covenant, hospitality, and shared life. In ancient Near-Eastern culture, who you ate with named who you belonged to. Jesus broke every social wall by sitting down to table with the wrong people — tax collectors, sinners, women of ill repute, ritually unclean — and the Pharisees were scandalized: <em>"This man receiveth sinners, and eateth with them"</em> (<em>Luke 15:2</em>). The Lord’s Supper is the climactic table fellowship: the Bridegroom eats with His bride. The marriage supper of the Lamb awaits (<em>Revelation 19:9</em>). Christian hospitality at home — opening the table to neighbors, the lonely, the unconverted — is gospel ministry. The kingdom advances at table.</p>'
    ),
    'tikvah': (
        '<p><em>Tikvah</em> (תִּקְוָה) is the Hebrew word for <em>hope</em>. From the verb <em>qavah</em> ("to wait, to look expectantly for"), <em>tikvah</em> is sustained expectation rooted in God’s character — not wishful optimism. Jeremiah voices it from the ash heap: <em>"For I know the thoughts that I think toward you, saith the LORD, thoughts of peace, and not of evil, to give you an expected end [tikvah]"</em> (<em>Jeremiah 29:11</em>); <em>"Hope deferred maketh the heart sick: but when the desire cometh, it is a tree of life"</em> (<em>Proverbs 13:12</em>). Strikingly, <em>tikvah</em> also means "cord" — Rahab’s scarlet line in the window (<em>Joshua 2:18</em>). Hope is the cord stretched from present darkness to promised deliverance — anchored on the far side in God.</p>'
    ),
    'yhwh-tsidkenu': (
        '<p><em>YHWH-Tsidkenu</em> (יְהוָה צִדְקֵנוּ) — "the LORD Our Righteousness" — is the covenant name Jeremiah gives the coming Messianic Branch: <em>"In his days Judah shall be saved, and Israel shall dwell safely: and this is his name whereby he shall be called, THE LORD OUR RIGHTEOUSNESS"</em> (<em>Jeremiah 23:6</em>; cf. <em>33:16</em>). The name is foundational to Pauline gospel doctrine: the righteousness by which the believer is justified is not his own attainment, but Christ’s own righteousness, freely imputed (<em>Romans 1:17; 3:21-26; 5:17-19</em>; <em>2 Corinthians 5:21</em>: <em>"that we might be made the righteousness of God in him"</em>). The Christian wears not a robe of his own weaving but the very righteousness of the LORD. His name <em>is</em> our righteousness.</p>'
    ),
    'zebach-offering': (
        '<p>The <em>zebach</em> (זֶבַח) is the Mosaic peace offering, prescribed in <em>Leviticus 3</em> — also called the "fellowship offering." It was unique among Levitical sacrifices: the worshipper himself ate the meat as a fellowship-meal with God and others, after a portion was burned on the altar and another given to the priests (<em>Leviticus 7:11-21</em>). The <em>zebach</em> is therefore distinct from the burnt offering (<em>olah</em>, entirely consumed) and the sin offering (<em>chattat</em>, addressing guilt). It symbolized covenant fellowship — eating together as the picture of <em>shalom</em> with God. The Lord’s Supper is its New-Covenant fulfillment: the people of God eat with their God at His own table, in peace, by virtue of the once-for-all sacrifice of Christ.</p>'
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
