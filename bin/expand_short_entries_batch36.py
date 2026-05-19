#!/usr/bin/env python3
"""Batch 36 — expand 25 more entries from the 50-60 word bucket.

Targets: Hebrew vocab, Beatitudes (paired slugs), military imagery,
covenant theology, NT figures, doctrines, and biblical botany.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'yokefellow': (
        '<p>A yokefellow is one who labors under the same yoke as another — the partner pulling the load alongside, sharing the discipline, the pace, and the weight. Paul uses the word in <em>Philippians 4:3</em>: <em>"And I intreat thee also, true yokefellow, help those women which laboured with me in the gospel."</em> The picture is taken from the working pair of oxen joined by a single wooden yoke — they must walk in step, or the plow goes crooked and both are hurt. The same picture fits husband and wife (<em>Genesis 2:24</em>), the elders’ council, the missionary team (<em>Acts 13:2-3</em>), and any covenant partnership for the kingdom. Find your yokefellow; keep step.</p>'
    ),
    'anger-slow': (
        '<p>"Slow to anger" is the Hebrew <em>erekh appayim</em>, literally <em>"long of nostrils"</em> — a vivid Semitic idiom for delayed flaring. The image is the nose taking a long time to redden. It is YHWH’s recurring self-description in <em>Exodus 34:6</em>: <em>"The LORD, The LORD God, merciful and gracious, longsuffering [erekh appayim], and abundant in goodness and truth"</em> — quoted across the Psalms (<em>86:15; 103:8; 145:8</em>), prophets (<em>Joel 2:13; Jonah 4:2</em>), and gospel writers. Wisdom commands the saint to imitate it: <em>"He that is slow to wrath is of great understanding: but he that is hasty of spirit exalteth folly"</em> (<em>Proverbs 14:29</em>); <em>"slow to wrath: For the wrath of man worketh not the righteousness of God"</em> (<em>James 1:19-20</em>).</p>'
    ),
    'beatitude-5': (
        '<p>The fifth Beatitude of Christ’s Sermon on the Mount: <em>"Blessed are the merciful: for they shall obtain mercy"</em> (<em>Matthew 5:7</em>). Mercy here is active — the merciful <em>do</em> mercy, <em>show</em> mercy, <em>give</em> mercy, especially to the undeserving. The Greek <em>eleēmones</em> describes a settled disposition, not occasional kindness. Christ’s promise is reciprocal: those who show mercy receive mercy from God, both now and at the judgment: <em>"For he shall have judgment without mercy, that hath shewed no mercy; and mercy rejoiceth against judgment"</em> (<em>James 2:13</em>). The parable of the unforgiving servant (<em>Matthew 18:23-35</em>) illustrates the inverse. Mercy received and mercy given are tightly bound; the disciple who keeps tally has not yet understood his own forgiveness.</p>'
    ),
    'beatitude-6': (
        '<p>The sixth Beatitude of Christ’s Sermon on the Mount: <em>"Blessed are the pure in heart: for they shall see God"</em> (<em>Matthew 5:8</em>). Purity here is internal — Greek <em>katharoi tē kardia</em>, "clean in the heart" — not ritual purity of hands or vessels. The promise is the beatific vision: those whose hearts are cleansed (by Christ’s blood and the Spirit’s sanctifying work) will see God face-to-face. <em>"Follow peace with all men, and holiness, without which no man shall see the Lord"</em> (<em>Hebrews 12:14</em>). The promise is partly present (we see God now by faith in His Word and works) and ultimately future (<em>"we shall see him as he is"</em>, <em>1 John 3:2</em>). Cultivate the heart; clean the eye; see Him.</p>'
    ),
    'berit-hebrew': (
        '<p><em>Berit</em> (בְּרִית) is the Hebrew word for <em>covenant</em> — a solemn, sworn, binding agreement, usually sealed in blood. Across Scripture, YHWH binds Himself to His people through a series of <em>beritot</em>: with Noah (creation-preservation, <em>Genesis 9</em>); with Abraham (election, <em>Genesis 15, 17</em>); with Moses (the law at Sinai, <em>Exodus 19-24</em>); with David (kingship, <em>2 Samuel 7</em>); and the New Covenant (heart-renewal in Christ, <em>Jeremiah 31:31-34</em>; <em>Luke 22:20</em>; <em>Hebrews 8</em>). The Hebrew idiom "to cut a covenant" (<em>karat berit</em>) recalls the bisected animals through which Abraham walked in <em>Genesis 15:9-17</em> — the sworn pledge sealed in blood, with the threat: <em>may I be as these if I break covenant</em>. Christ Himself walked through that pledge.</p>'
    ),
    'campaign-biblical': (
        '<p>A campaign is an extended ordered military effort — the season in the field, with its planned phases, named objectives, and known cost. Scripture has its campaigns. David’s Philistine wars unfolded in named engagements: <em>Baal-perazim, Gibeon, Rephaim, Gath</em>. Joshua’s southern and northern campaigns each conquered specific kings and regions (<em>Joshua 10-11</em>). Paul’s missionary journeys are mapped phase by phase: first journey (<em>Acts 13-14</em>), second (<em>15:36-18:22</em>), third (<em>18:23-21:17</em>). The Christian life itself is a campaign with named hills: <em>"Fight the good fight of faith"</em> (<em>1 Timothy 6:12</em>); <em>"I have fought a good fight, I have finished my course"</em> (<em>2 Timothy 4:7</em>). Plan the campaign; name the objectives.</p>'
    ),
    'colors-military': (
        '<p>The colors, in military usage, are the flag or standard of a unit — treated as the visible embodiment of its honor, never abandoned without disgrace. Scripture has the parallel. Israel encamped by tribes around the tabernacle, each tribe under its own standard: <em>"Every man of the children of Israel shall pitch by his own standard, with the ensign of their father’s house"</em> (<em>Numbers 2:2</em>). Christ is the ensign to whom the nations rally: <em>"there shall be a root of Jesse, which shall stand for an ensign of the people; to it shall the Gentiles seek"</em> (<em>Isaiah 11:10</em>). The cross is now the colors under which the saints muster — emblem of victory by suffering, banner of the Lamb.</p>'
    ),
    'covenant-curses': (
        '<p>Covenant curses are the specific judgments threatened upon Israel in case of covenant breach — the conditional <em>if-then</em> structure of the Mosaic covenant. <em>Deuteronomy 28</em> lists them in detail: drought (<em>vv. 23-24</em>), military defeat (<em>vv. 25-26</em>), disease (<em>vv. 27-28</em>), agricultural disaster (<em>vv. 38-42</em>), oppression by foreigners (<em>vv. 43-44</em>), siege-cannibalism (<em>vv. 53-57</em>), and ultimate scattering and exile (<em>vv. 63-68</em>). The covenant curses are not arbitrary divine wrath; they are the covenant’s own warnings, sworn to publicly by the people themselves at Mount Ebal and Gerizim (<em>Deuteronomy 27:11-26</em>). Israel’s exile fulfilled them. Christ bore them all on the cross for His people (<em>Galatians 3:13</em>).</p>'
    ),
    'covenant-loyalty': (
        '<p>Covenant loyalty is the active disposition of staying with one’s covenant party through good and ill — the willingness to hold the bond when it costs you. The Hebrew <em>chesed</em> covers it. Ruth’s <em>"Intreat me not to leave thee, or to return from following after thee: for whither thou goest, I will go; and where thou lodgest, I will lodge: thy people shall be my people, and thy God my God"</em> (<em>Ruth 1:16</em>) is the great Old Testament narrative of it. Christ brings it into the New: <em>"I will never leave thee, nor forsake thee"</em> (<em>Hebrews 13:5</em>, quoting <em>Deuteronomy 31:6</em>). Covenant loyalty is the masculine virtue at the heart of marriage, friendship, citizenship, and church membership. Stick.</p>'
    ),
    'crispus': (
        '<p>Crispus was the chief ruler (Greek <em>archisynagōgos</em>) of the synagogue at Corinth who believed on the Lord with all his house when Paul preached there: <em>"And Crispus, the chief ruler of the synagogue, believed on the Lord with all his house; and many of the Corinthians hearing believed, and were baptized"</em> (<em>Acts 18:8</em>). Paul personally baptized him: <em>"I thank God that I baptized none of you, but Crispus and Gaius"</em> (<em>1 Corinthians 1:14</em>). He is one of the few converts Paul mentions baptizing himself. His conversion was a public turning point in Corinth — the synagogue’s leader publicly crossing the line — and strengthened the apostle’s confidence to remain: <em>"I have much people in this city"</em> (<em>Acts 18:10</em>).</p>'
    ),
    'episcopacy': (
        '<p>"Episcopacy" names the ecclesial polity governed by bishops as a distinct office above presbyters. The New Testament, however, uses <em>episkopos</em> (overseer/bishop) and <em>presbyteros</em> (elder) interchangeably for the same office: <em>"And from Miletus he sent to Ephesus, and called the elders [presbyterous] of the church... Take heed therefore unto yourselves, and to all the flock, over the which the Holy Ghost hath made you overseers [episkopous]"</em> (<em>Acts 20:17, 28</em>); cf. <em>Titus 1:5-7</em>. Paul addresses <em>"bishops and deacons"</em> at Philippi with no third order (<em>Philippians 1:1</em>). The development of a three-tier hierarchy (bishop / priest / deacon) appears post-apostolically (Ignatius of Antioch, c. AD 110) but is not clearly mandated in Scripture. Reformed and Presbyterian churches accordingly reject episcopal polity.</p>'
    ),
    'family-altar-rebuild': (
        '<p>"Family altar rebuild" names the deliberate restoration of household worship in homes where it has lapsed or never been established. The historical pattern is clear: when reformers and revivalists have addressed the church, they have consistently called for the recovery of family worship as the congregation’s essential domestic complement. Calvin, the Westminster divines, the Puritans, Jonathan Edwards, the Welsh revivalists, J. C. Ryle — each one preached it. The Directory for Family Worship (1647) is the classic Reformed manual. Without family altars rebuilt, congregational reform is rootless — children raised in churches with unconverted parents who never opened the Bible at home cannot be expected to retain the faith. Light the altar in your house this week.</p>'
    ),
    'fear-yhwh-imperative': (
        '<p>"Fear the LORD" is the most frequent Old Testament exhortation. It is not anxious dread or terrified flight; it is reverent awe that recognizes God for who He is and leads to obedience. <em>"The fear of the LORD is the beginning of wisdom"</em> (<em>Proverbs 9:10; Psalm 111:10</em>); <em>"Fear God, and keep his commandments: for this is the whole duty of man"</em> (<em>Ecclesiastes 12:13</em>); <em>"By the fear of the LORD men depart from evil"</em> (<em>Proverbs 16:6</em>). The fear of the LORD does not exclude the love of the LORD; the two are inseparable in Scripture: the same verse can command both (<em>Deuteronomy 10:12</em>: <em>"to fear the LORD thy God... and to love him"</em>). The man without the fear of God may be religious; he is not yet wise.</p>'
    ),
    'garden-motif': (
        '<p>The Garden Motif is the recurring biblical setting of intimate fellowship between God and humanity. Five gardens punctuate the canon. <em>Eden</em> (creation, fellowship, and fall — <em>Genesis 2-3</em>). The <em>Song of Solomon</em>’s gardens (love and union — <em>Song 4:12-16; 5:1; 6:2; 8:13</em>). <em>Gethsemane</em> (Christ’s submission to the cup — <em>John 18:1</em>; <em>Matthew 26:36</em>). The <em>garden tomb</em> where Christ rose, and where Mary mistook Him for the gardener (<em>John 19:41; 20:15</em>). And the <em>garden-city</em> of <em>Revelation 21-22</em> with the tree of life along the river — Eden restored and exceeded. Gardens in Scripture are where God and His image-bearers walk together; the whole biblical story moves from garden through wilderness back to garden.</p>'
    ),
    'giving': (
        '<p>Giving is the deliberate transfer of resources, time, gifts, or oneself to another — and Scripture identifies it as the act most characteristic of God Himself in the gospel: <em>"For God so loved the world, that he gave his only begotten Son"</em> (<em>John 3:16</em>). It is therefore the act most stamping the believer who has received. Paul’s sustained teaching on Christian giving in <em>2 Corinthians 8-9</em> names the principles: <em>cheerful</em> (<em>"God loveth a cheerful giver"</em>, 9:7), <em>proportionate</em> (<em>"according as God hath prospered him"</em>, <em>1 Corinthians 16:2</em>), <em>planned</em>, <em>secret</em> (<em>Matthew 6:3-4</em>), <em>sacrificial</em>, and <em>joyful</em>. <em>"It is more blessed to give than to receive"</em> (<em>Acts 20:35</em>). The Christian man earns much, lives modestly, and gives generously.</p>'
    ),
    'intent': (
        '<p>Intent is the directional purpose of the heart — what the soul is reaching for behind a given act. Scripture distinguishes it from the outward deed and treats it as the deeper truth. <em>"For the word of God is quick, and powerful, and sharper than any twoedged sword, piercing even to the dividing asunder of soul and spirit, and of the joints and marrow, and is a discerner of the thoughts and intents of the heart"</em> (<em>Hebrews 4:12</em>). The next verse adds the witness: <em>"Neither is there any creature that is not manifest in his sight: but all things are naked and opened unto the eyes of him with whom we have to do"</em> (<em>v. 13</em>). Intent is one of the categories on which God will judge every man at the last day.</p>'
    ),
    'merciful-blessed': (
        '<p>"Blessed are the merciful: for they shall obtain mercy" (<em>Matthew 5:7</em>) is the fifth Beatitude, and the reciprocal structure is unmistakable: those who give mercy receive it. Christ later illustrates the inverse in the parable of the unforgiving servant (<em>Matthew 18:23-35</em>) — the man who received ten thousand talents of forgiveness from his lord and refused a hundred pence to his fellow-servant. Mercy here is more than feeling-bad-for; it is active, costly relief shown to those in need or under judgment. James seals the doctrine: <em>"For he shall have judgment without mercy, that hath shewed no mercy; and mercy rejoiceth against judgment"</em> (<em>James 2:13</em>). The Christian man who has tasted mercy at the cross must pour it out on those around him.</p>'
    ),
    'mustard': (
        '<p>Mustard is a common garden plant of Palestine, grown from a tiny round seed (about 1 mm) into a tall annual reaching ten or twelve feet. Christ uses it twice with theological weight. First, as the figure of the kingdom of God: <em>"The kingdom of heaven is like to a grain of mustard seed... which indeed is the least of all seeds: but when it is grown, it is the greatest among herbs, and becometh a tree, so that the birds of the air come and lodge in the branches"</em> (<em>Matthew 13:31-32</em>). Second, as the figure of saving faith: <em>"If ye have faith as a grain of mustard seed, ye shall say unto this mountain, Remove hence to yonder place; and it shall remove"</em> (<em>Matthew 17:20</em>). The kingdom hides itself in small starts.</p>'
    ),
    'purity-of-heart': (
        '<p>Purity of heart is the inner cleanness Christ commends in the sixth Beatitude: <em>"Blessed are the pure in heart: for they shall see God"</em> (<em>Matthew 5:8</em>). It is distinct from ritual purity (washing of hands, vessels, garments) — it is the state of an inner life undivided by competing loves and uncluttered by hidden sin. David’s prayer names the goal: <em>"Create in me a clean heart, O God; and renew a right spirit within me"</em> (<em>Psalm 51:10</em>). Paul names the path: <em>"the end of the commandment is charity out of a pure heart, and of a good conscience, and of faith unfeigned"</em> (<em>1 Timothy 1:5</em>). Christ Himself is the only sufficient cleaning agent. By His blood the heart is made pure.</p>'
    ),
    'raising-banner': (
        '<p>Raising the banner is the act of lifting a rallying standard so that troops, kindred, and onlookers gather under one name. Moses raised an altar called <em>Jehovah-Nissi</em> after the victory over Amalek — <em>"the LORD is my banner"</em> (<em>Exodus 17:15</em>). Isaiah saw the LORD lifting an ensign to the nations: <em>"And he will lift up an ensign to the nations from far, and will hiss unto them from the end of the earth"</em> (<em>Isaiah 5:26</em>); <em>"there shall be a root of Jesse, which shall stand for an ensign of the people"</em> (<em>11:10</em>). The Song of Songs sings: <em>"his banner over me was love"</em> (<em>Song 2:4</em>). Christian men gather under the raised banner of the cross.</p>'
    ),
    'reins': (
        '<p>"Reins" — the KJV translation of the Hebrew <em>kelayot</em>, literally <em>kidneys</em> — names what biblical psychology calls the seat of innermost will, conscience, and emotional truth. The reins are deeper than the heart’s surface sentiment; they are the inner core where motive lives. <em>"The righteous God trieth the hearts and reins"</em> (<em>Psalm 7:9</em>); <em>"I the LORD search the heart, I try the reins, even to give every man according to his ways"</em> (<em>Jeremiah 17:10</em>); <em>"Examine me, O LORD, and prove me; try my reins and my heart"</em> (<em>Psalm 26:2</em>). Modern English keeps a fossil of the meaning in the verb <em>"to rein in"</em> — to restrain from the inside. God’s eye reaches the reins. Submit them.</p>'
    ),
    'reverence-biblical': (
        '<p>Biblical reverence is the settled inner posture of awe before God, His Name, His house, His Word, His messengers, and His ordained authorities. Hebrews commands it explicitly as the New Covenant’s appropriate response to receiving an unshakable kingdom: <em>"Wherefore we receiving a kingdom which cannot be moved, let us have grace, whereby we may serve God acceptably with reverence and godly fear: for our God is a consuming fire"</em> (<em>Hebrews 12:28-29</em>). The same disposition fits worship (<em>"keep silence before him"</em>, <em>Habakkuk 2:20</em>), parents (<em>Hebrews 12:9</em>), magistrates (<em>Romans 13:7</em>), and elders (<em>1 Timothy 5:17</em>). Modern Christianity has often lost reverence in pursuit of casualness. Recover it. The God who saves us is also the God who is a consuming fire.</p>'
    ),
    'simple-one': (
        '<p>The "simple one" (Hebrew <em>pethi</em>) is the Proverbs category for the open-hearted but undiscerning person — not malicious, but easily led astray for lack of discernment. <em>"The simple believeth every word: but the prudent man looketh well to his going"</em> (<em>Proverbs 14:15</em>; cf. <em>1:4, 22; 7:7; 9:4, 16; 19:25</em>). The four wisdom-tiers of Proverbs are revealing. On the descent: <em>simple → fool → scoffer</em> (incurable, mocking, beyond pleading). On the ascent: <em>simple → wise → instructed-of-the-LORD</em>. The simple one is salvageable — he can still be taught; he just has not been. The scoffer cannot; his folly is fixed. Christian fathers must train the simple young man into wisdom before mockery captures him.</p>'
    ),
    'son-of-god': (
        '<p>"Son of God" is the supreme New Testament title for Christ’s eternal deity and unique relationship to the Father. He is not a son of God in the generic sense in which believers are sons of God by adoption (<em>Romans 8:14-15</em>; <em>Galatians 4:5-7</em>). He is <em>the</em> Son — in the unique, eternal, ontological sense — <em>"the only begotten Son of God"</em> (<em>John 3:16, 18</em>; <em>1 John 4:9</em>). He is <em>"of one substance with the Father"</em> (Nicene Creed) — eternally generated, fully God, distinct in Person but one in essence. <em>"Thou art my Son; this day have I begotten thee"</em> (<em>Psalm 2:7</em>; <em>Hebrews 1:5</em>). Every believing confession of Christ as Son of God hangs the gospel on this eternal sonship.</p>'
    ),
    'sycamore': (
        '<p>The sycamore (<em>Ficus sycomorus</em>, the fig-mulberry) is a tree common in lowland Israel and Egypt — large, spreading, with rough bark easy to climb, bearing small fig-like fruit eaten by the poor and yielding durable timber. Amos was a herdsman and a <em>"gatherer of sycomore fruit"</em> when the LORD called him to prophesy (<em>Amos 7:14</em>). Zacchaeus the chief tax-collector of Jericho — short of stature and unable to see over the crowd — <em>"climbed up into a sycomore tree to see him: for he was to pass that way"</em> (<em>Luke 19:4</em>). Christ called him down by name, went to his house, and salvation came to that house. The LORD uses common trees to host uncommon encounters.</p>'
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
