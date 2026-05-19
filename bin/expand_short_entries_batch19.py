#!/usr/bin/env python3
"""Batch 19 — expand 25 more thin entries to 90-110 words each.

Targets: classical doctrines, OT books/events, Reformed liturgy,
Hebrew vocabulary, disciplines, pastoral and KJV verbs from the
30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'quintessence': (
        '<p>Quintessence is not a biblical word but a useful concept — the purest, most distilled essence of something, free from any alloy or admixture. The medieval Latin <em>quinta essentia</em> (fifth element) named the heavenly substance beyond the four earthly elements. Christianly applied, Christ is the quintessence of God’s glory: <em>"Who being the brightness of his glory, and the express image of his person, and upholding all things by the word of his power"</em> (<em>Hebrews 1:3</em>). Whatever God is in essence, Christ is in incarnate form: <em>"in him dwelleth all the fulness of the Godhead bodily"</em> (<em>Colossians 2:9</em>). To see Christ is therefore not to see a piece of God or a representation of God — it is to see God Himself, purely, fully, undiluted.</p>'
    ),
    'red-sea-crossing': (
        '<p>The Red Sea Crossing is the great Exodus miracle in which the LORD divided the sea before Israel and drowned Pharaoh’s pursuing army behind them (<em>Exodus 14</em>). Moses stretched out his rod; the LORD drove back the waters by a strong east wind all night; Israel walked through on dry ground with walls of water on either hand; the Egyptian chariots followed and were swallowed at dawn. Miriam led the women in the song of the sea: <em>"The horse and his rider hath he thrown into the sea"</em> (<em>Exodus 15</em>). Paul makes the typology explicit: <em>"all our fathers... were all baptized unto Moses in the cloud and in the sea"</em> (<em>1 Corinthians 10:1-2</em>). The crossing is the Old Testament’s great picture of redemption.</p>'
    ),
    'shout-for-joy': (
        '<p>"Shout for joy" is the audible, loud, jubilant cry commanded as worship-response throughout the Psalms — not silent inner happiness but outward voiced jubilation. <em>"Make a joyful noise unto the LORD, all the earth: make a loud noise, and rejoice, and sing praise"</em> (<em>Psalm 98:4</em>; cf. <em>32:11; 35:27; 47:1; 66:1; 81:1; 95:1; 100:1</em>). Worship in Scripture has volume; the saints lift up the voice together. The same word covers victory shouts of armies (<em>1 Samuel 17:20</em>), the trumpet blast of the Day of Atonement, and the joyful return from exile. Modern reverence too often confuses solemnity with silence; the Psalter teaches us that holy joy is also <em>loud</em>. Sing out, shout, lift the voice.</p>'
    ),
    'votum': (
        '<p>The <em>Votum</em> (Latin "vow") is the opening declaration of dependence in classical Reformed worship: <em>"Our help is in the name of the LORD, who made heaven and earth"</em> (<em>Psalm 124:8</em>). Spoken by the minister at the very beginning of the service, before the Call to Worship, it is a brief vow placing the worship and the congregation under God’s name and protection. The whole service is hereby acknowledged as God-dependent — without His help no true worship can ascend. Calvin’s Geneva liturgy used it; the Dutch Reformed tradition still does. The <em>Votum</em> trains the soul: every Sunday begins not with welcome, music, or announcements, but with the explicit, scriptural confession that the LORD alone is our help.</p>'
    ),
    'work-ethic': (
        '<p>A biblical work ethic is the disciple’s steady, honest labor done <em>"as to the Lord, and not unto men"</em> (<em>Colossians 3:23-24</em>) — refusing idleness, earning his own bread, providing for his household. Paul’s rule stands: <em>"if any would not work, neither should he eat"</em> (<em>2 Thessalonians 3:10</em>). The Christian works hard, not because his identity is in his work, but because the LORD made man <em>"to dress and to keep"</em> the garden (<em>Genesis 2:15</em>). Sloth is sin; entitlement is sin; idleness is sin. So is workaholism that idolizes the labor itself. The Christian man works diligently six days, rests on the seventh, provides generously, and gives the glory to God. Wealth is to be earned, not extorted, not begged, not envied.</p>'
    ),
    'chokmah': (
        '<p><em>Chokmah</em> (חָכְמָה) is the Hebrew word for wisdom — not abstract knowledge but practical-spiritual skill at living. The same root names Bezalel’s craftsman-skill in fashioning the tabernacle (<em>Exodus 31:3</em>) and the moral-spiritual wisdom that fills the book of Proverbs. <em>Chokmah</em> is craftsmanship of the soul: knowing how to live well, speak rightly, govern a household, and walk before God. <em>"The fear of the LORD is the beginning of wisdom"</em> (<em>Proverbs 9:10</em>); without that fear, no skill is sanctified. Christ is the very <em>chokmah</em> of God (<em>1 Corinthians 1:24, 30</em>), in whom <em>"are hid all the treasures of wisdom and knowledge"</em> (<em>Colossians 2:3</em>). Wisdom is therefore not just data — it is union with the Wise One.</p>'
    ),
    'christ-king-sunday': (
        '<p>Christ the King Sunday is the final Sunday of the liturgical year — the last Sunday before Advent — confessing Christ’s sovereign kingship over all earthly powers, governments, and rulers. The feast was instituted by Pope Pius XI in 1925 as a direct theological answer to the secular nationalisms of the early twentieth century (Mussolini’s fascism, Lenin’s communism), and was adopted in Protestant lectionaries thereafter. Its texts gather around <em>Daniel 7:13-14</em>, <em>Revelation 1:5-8</em>, and the cross-side proclamation <em>"This is the King of the Jews"</em> (<em>Luke 23:38</em>). The Sunday rounds the Christian year before Advent begins anew — closing one cycle with the kingship proclaimed, and opening the next with the King’s coming awaited.</p>'
    ),
    'colossae': (
        '<p>Colossae was a small city in the Lycus valley of Phrygia (modern southwestern Turkey), about ten miles east of Laodicea. The church there was founded during Paul’s third missionary journey, almost certainly by Epaphras, a Colossian convert (<em>Colossians 1:7; 4:12-13</em>) — Paul himself had not personally visited the city when he wrote to it (<em>Colossians 2:1</em>). The epistle confronts an early syncretistic heresy that combined Jewish ritual, ascetic mysticism, and angel-veneration — collectively demoting Christ. Paul’s response is one of Scripture’s great Christological texts: <em>"in him dwelleth all the fulness of the Godhead bodily"</em> (<em>Colossians 2:9</em>); <em>"in him were all things created... and by him all things consist"</em> (<em>1:16-17</em>). The cosmic Christ has no rival.</p>'
    ),
    'day-of-atonement-doctrine': (
        '<p>The doctrine of the Day of Atonement is the theological substance behind the annual Mosaic ritual (<em>Leviticus 16</em>): on the tenth of the seventh month the high priest entered the Most Holy Place with sacrificial blood — first a bull for his own sins, then a goat for the people — to make atonement before the mercy seat. A second goat, the scapegoat, was sent into the wilderness bearing the iniquities of the nation. The whole liturgy preached one doctrine: <em>without shedding of blood is no remission</em> (<em>Hebrews 9:22</em>). Christ fulfills both goats — the slain victim whose blood is sprinkled and the bearer who carries sin away — entering once for all into the heavenly sanctuary with His own blood (<em>Hebrews 9:11-14, 24-28</em>).</p>'
    ),
    'disregard': (
        '<p>To disregard is to refuse to attend to, value, or weigh another — a withholding of the dignity Scripture commands toward every image-bearer (<em>Genesis 1:27</em>; <em>James 2:1-9</em>). It must be distinguished sharply from disagreement: disagreement differs in judgment but still grants the dignity of consideration; disregard withholds dignity altogether. The proud disregard the poor (<em>James 2:6</em>); the impatient disregard the slow; the strong disregard the weak; the cultured disregard the unsophisticated. Christ never disregarded anyone — He answered Pilate, the Samaritan woman, the leper, the demoniac, the rich young ruler, the blind beggar. Christian men must learn to engage what they disagree with rather than dismiss it; to value the dignity of even the wrong-headed image-bearer in front of them.</p>'
    ),
    'divine-impassibility': (
        '<p>Divine impassibility is the classical Christian doctrine that God in His divine nature is not subject to passions imposed from outside Himself. He is not pulled around by emotion as creatures are — anxious, frightened, lust-tossed, manipulated by mood. <em>"For I am the LORD, I change not"</em> (<em>Malachi 3:6</em>); <em>"every good gift... cometh down from the Father of lights, with whom is no variableness, neither shadow of turning"</em> (<em>James 1:17</em>). The doctrine does <em>not</em> mean God is unfeeling, stoic, or distant — Scripture freely speaks of His love, wrath, jealousy, and compassion. It means God’s affections are perfectly His own, expressing His unchanging character. The Reformed confessions teach impassibility precisely to protect God’s freedom and faithfulness. He is moved within Himself, not by us.</p>'
    ),
    'heart-pure': (
        '<p>A pure heart is a heart cleansed by the blood of Christ, unmixed in its devotion, single in its love — the place where God dwells and from which true charity flows. Jesus’ sixth Beatitude promises the beatific vision: <em>"Blessed are the pure in heart: for they shall see God"</em> (<em>Matthew 5:8</em>). The pure heart is contrasted with the divided heart (<em>James 4:8</em>: <em>"purify your hearts, ye double minded"</em>) and the defiled heart (<em>Mark 7:21-23</em>). It is the goal of Paul’s teaching: <em>"the end of the commandment is charity out of a pure heart"</em> (<em>1 Timothy 1:5</em>). Christ purifies it by His blood; we keep it by quick repentance, watchfulness, and singleness of aim. Only the pure-hearted will see God face to face.</p>'
    ),
    'honesty-biblical': (
        '<p>Biblical honesty is truthfulness in word and integrity in deed — refusing the false weight, the false report, the false witness, the false impression. The law commanded just balances: <em>"Ye shall do no unrighteousness in judgment, in meteyard, in weight, or in measure. Just balances, just weights, a just ephah, and a just hin, shall ye have"</em> (<em>Leviticus 19:35-36</em>). The ninth commandment forbids false witness (<em>Exodus 20:16</em>); Christ reaffirms it (<em>Matthew 5:33-37</em>); Paul presses it into the church: <em>"Recompense to no man evil for evil. Provide things honest in the sight of all men"</em> (<em>Romans 12:17</em>; <em>2 Corinthians 8:21</em>). The Christian man’s yes is yes and his no is no. A handshake is enough.</p>'
    ),
    'parables-of-kingdom': (
        '<p>The Parables of the Kingdom are the body of stories Christ told to unveil — and simultaneously to veil — the kingdom of heaven (<em>Matthew 13:10-17</em>). The Sower (<em>13:1-23</em>) shows how the word lands; the Wheat and Tares (<em>13:24-30</em>) explains why evil and good grow together until the harvest; the Mustard Seed and Leaven (<em>13:31-33</em>) describe the kingdom’s small beginnings and pervasive spread; the Hidden Treasure and Pearl (<em>13:44-46</em>) measure its worth; the Dragnet (<em>13:47-50</em>) anticipates final judgment. Add the Unforgiving Servant, Vineyard Laborers, Ten Virgins, Talents, and Sheep-and-Goats (chs. 18-25), and the kingdom is revealed in mystery form — open to those with ears to hear, closed to those without.</p>'
    ),
    'proverbs-31': (
        '<p>Proverbs 31 closes the book of Proverbs in two movements. First, the instruction of King Lemuel’s mother (<em>vv. 1-9</em>): warnings against women, drunkenness, and the perversion of justice; the king’s charge to <em>"open thy mouth for the dumb in the cause of all such as are appointed to destruction... open thy mouth, judge righteously"</em>. Second, the famous acrostic poem of the virtuous wife (<em>vv. 10-31</em>) — twenty-two verses, one per Hebrew letter, depicting the godly wife’s industry, fear of the LORD, household management, business acumen, charity to the poor, and the praise of her husband and children. <em>"Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised."</em> The chapter is the church’s portrait of the wife to be sought, raised, and honored.</p>'
    ),
    'uphold': (
        '<p>To uphold is to hold up, sustain, support — to keep from falling. The verb runs as a great cord through Scripture in God’s covenantal promises to His people. <em>"Fear thou not; for I am with thee... yea, I will help thee; yea, I will uphold thee with the right hand of my righteousness"</em> (<em>Isaiah 41:10</em>). The Servant of the LORD is upheld by the Father’s Spirit (<em>Isaiah 42:1</em>). Christ Himself upholds <em>"all things by the word of his power"</em> (<em>Hebrews 1:3</em>): the universe is not coasting — it is sustained moment by moment by the active will of God. The Christian who knows he is upheld walks differently. He cannot finally fall, because the right hand of the LORD holds him up.</p>'
    ),
    'vindicate': (
        '<p>To vindicate is to clear from blame, declare righteous, defend against accusation — the courtroom side of justification. The psalmist appeals: <em>"Judge me, O LORD; for I have walked in mine integrity... Examine me, O LORD, and prove me; try my reins and my heart"</em> (<em>Psalm 26:1-2</em>; cf. <em>43:1</em>). The LORD vindicates the oppressed against false accusation and ultimately vindicates His own Son: <em>"God was manifest in the flesh, justified in the Spirit"</em> (<em>1 Timothy 3:16</em>) — the resurrection is the Father’s public vindication of the crucified Christ. The believer who suffers slander unjustly entrusts his vindication to the Judge of all the earth, who shall do right (<em>Genesis 18:25</em>; <em>1 Peter 2:23</em>). The verdict is not yours to extract.</p>'
    ),
    'yearn': (
        '<p>To yearn is to long deeply, ache, be moved with strong desire — most often in Scripture of one heart toward another. Joseph’s <em>"bowels did yearn upon his brother"</em> when he first saw Benjamin in Egypt (<em>Genesis 43:30</em>). Paul writes the Philippians: <em>"For God is my record, how greatly I long after you all in the bowels of Jesus Christ"</em> (<em>Philippians 1:8</em>). The Psalmist’s soul yearns for God like a deer panting after the water brooks (<em>Psalm 42:1</em>). Christ Himself longs over Jerusalem: <em>"how often would I have gathered thy children together, even as a hen gathereth her chickens under her wings"</em> (<em>Matthew 23:37</em>). Holy yearning is the soul’s legitimate ache — for God, for souls, for the consummation.</p>'
    ),
    '2samuel': (
        '<p>2 Samuel chronicles David’s reign as king — first over Judah at Hebron, then over the united twelve tribes from Jerusalem (chs. 1-10). The book’s theological summit is the Davidic Covenant in chapter 7: the LORD promises to build David a house (dynasty) and to establish his throne forever — the prophetic seed-bed for every later messianic hope. Chapters 11-20 turn dark with David’s adultery with Bathsheba, his murder of Uriah, Nathan’s confrontation, and the long, costly chastening within his own house: Amnon’s incest, Absalom’s rebellion, Sheba’s revolt. The closing chapters (21-24) gather mighty-men lists, songs, and the threshing-floor of Araunah (future temple site). The throne stands; the throne suffers; the throne endures to Christ.</p>'
    ),
    'babel-tower': (
        '<p>The Tower of Babel was the post-flood monument built on the plain of Shinar (<em>Genesis 11:1-9</em>) by humanity united in language and rebellion: <em>"let us build us a city and a tower, whose top may reach unto heaven; and let us make us a name, lest we be scattered abroad upon the face of the whole earth."</em> The aim was self-glorification and resistance to God’s creational command to fill the earth. The LORD descended, confused their language, and scattered them — the very thing they had built the tower to prevent. Babel is therefore the origin of the nations and tongues, the founding act of human political pluralism, and the perpetual symbol of every imperial project to unify mankind apart from God. Pentecost reverses it.</p>'
    ),
    'emotion-stewardship': (
        '<p>Emotion stewardship is the discipline of governing feeling under the Spirit — neither suppressing emotion (stoicism, which is unbiblical) nor enthroning it (sentimentalism, which is destructive), but ruling one’s spirit as a city with walls (<em>Proverbs 25:28</em>). <em>"He that is slow to anger is better than the mighty; and he that ruleth his spirit than he that taketh a city."</em> The Christian acknowledges anger, fear, sorrow, and desire honestly, but does not let them rule him. They serve the King; they do not enthrone themselves. Christ wept, was grieved, was angry, was sorrowful unto death — and never once sinned. The biblical man feels strongly and is mastered only by God. Feelings are passengers in his soul, not pilots.</p>'
    ),
    'endure': (
        '<p>To endure is to remain under, persevere through — the saint’s steady continuance through trials, slander, suffering, and time. The Greek <em>hypomonē</em> is the noun — cheerful, patient endurance — and it is the eschatological qualifier of salvation in Christ’s own words: <em>"He that shall endure unto the end, the same shall be saved"</em> (<em>Matthew 24:13</em>; cf. <em>10:22</em>). It is the great theme of <em>Hebrews 12</em>: the cloud of witnesses, the race set before us, the Author and Finisher of our faith. Endurance is not natural toughness; it is supernatural staying-power produced by the Spirit, anchored in hope (<em>Romans 5:3-5</em>), proved by long obedience. The Christian does not need to win every battle today — he needs to be in the field tomorrow.</p>'
    ),
    'feed': (
        '<p>To feed is to provide nourishment — in Scripture especially of pastoral feeding. Christ fed the five thousand and the four thousand by miracle (<em>Matthew 14:13-21; 15:32-39</em>), He commanded Peter three times after the resurrection, <em>"Feed my lambs... Feed my sheep... Feed my sheep"</em> (<em>John 21:15-17</em>), and He charged the Ephesian elders through Paul to <em>"feed the church of God, which he hath purchased with his own blood"</em> (<em>Acts 20:28</em>; cf. <em>1 Peter 5:2</em>). Pastoral office is feeding-office. The minister’s primary task is not management, vision-casting, or entertainment; it is bringing the Word to the flock week after week. Where the Word is preached, sheep grow strong; where it is withheld, they starve and scatter.</p>'
    ),
    'flood-noah': (
        '<p>The Flood is the global judgment by water that destroyed all flesh in the days of Noah — every living thing on the face of the ground — except Noah, his wife, his three sons and their wives, and the animals preserved in the ark (<em>Genesis 6-9</em>). The waters of the deep burst, the windows of heaven opened, the rain fell forty days, and the earth was covered. After 150 days the waters abated, the ark rested on the mountains of Ararat, and Noah offered burnt offerings on dry ground. God gave the rainbow as covenant sign. The Flood is both historical event and pattern: universal judgment with a particular ark of salvation. Christ Himself is the ark; outside Him there is no shelter from the coming fire (<em>2 Peter 3</em>).</p>'
    ),
    'hin': (
        '<p>The <em>hin</em> was the standard Mosaic-law liquid-measure unit — roughly 3.7 liters (about one US gallon). It was used for oil, wine, and water in tabernacle offerings (<em>Exodus 29:40</em>; <em>30:24</em>; <em>Leviticus 23:13</em>; <em>Numbers 15:4-10; 28:7</em>). The just <em>hin</em> is required by the law alongside the just <em>ephah</em>: <em>"Just balances, just weights, a just ephah, and a just hin, shall ye have: I am the LORD your God, which brought you out of the land of Egypt"</em> (<em>Leviticus 19:36</em>). The verse is striking: the LORD’s authority over redemption is paired with His authority over honest measures. Worship and trade are governed by the same God. False measures defile both the marketplace and the altar.</p>'
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
