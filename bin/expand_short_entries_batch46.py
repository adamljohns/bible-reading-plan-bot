#!/usr/bin/env python3
"""Batch 46 — expand 25 more entries from the 60-70 word bucket.

Targets: theologians (Schaeffer, Bahnsen, Calvin, Benedict),
OT/NT figures, Hebrew vocab, liturgy, apologetics, virtues, and
numerology.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'gladness': (
        '<p>Gladness is the inner brightness of soul — covenant rejoicing, the disposition of a heart anchored in the LORD and overflowing into the face. Scripture commands it as the proper response to redemption: <em>"Be glad in the LORD, and rejoice, ye righteous: and shout for joy, all ye that are upright in heart"</em> (<em>Psalm 32:11</em>). It is the public posture of the great feasts: <em>"And thou shalt rejoice in thy feast, thou, and thy son, and thy daughter, and thy manservant... and the stranger, and the fatherless, and the widow"</em> (<em>Deuteronomy 16:14</em>). And it is the climactic atmosphere of the new heavens and new earth: <em>"the redeemed of the LORD shall return, and come with singing unto Zion; and everlasting joy shall be upon their head"</em> (<em>Isaiah 51:11</em>).</p>'
    ),
    'goat': (
        '<p>The goat is a horned ruminant — both a clean Levitical sacrificial animal and, in Christ’s eschatological parable, a sobering negative type. As sacrifice: goats were offered as sin offerings (<em>Leviticus 4:23-28; 5:6</em>), as peace offerings, and most notably as the two goats of Yom Kippur (<em>Leviticus 16</em>) — one slain for the people’s sins, one driven into the wilderness as the scapegoat bearing iniquity away. In Christ’s parable of the sheep and the goats (<em>Matthew 25:31-46</em>), the goats are separated from the sheep at the final judgment and sent into eternal punishment: <em>"Depart from me, ye cursed, into everlasting fire"</em>. Two destinies in one animal-type — the goat sacrificed for sin, and the goat judged for unbelief.</p>'
    ),
    'harmlessness': (
        '<p>Harmlessness is the saint’s disposition of doing no injury — the gentle restraint that does not lash out, mock, or wound. Christ’s instruction to the twelve: <em>"Behold, I send you forth as sheep in the midst of wolves: be ye therefore wise as serpents, and harmless as doves"</em> (<em>Matthew 10:16</em>). Paul applies it to the church corporately: <em>"That ye may be blameless and harmless, the sons of God, without rebuke, in the midst of a crooked and perverse nation, among whom ye shine as lights in the world"</em> (<em>Philippians 2:15</em>). The harmless saint is not weak or naive (he is also wise as a serpent); he simply does not return evil for evil. <em>"Recompense to no man evil for evil"</em> (<em>Romans 12:17</em>).</p>'
    ),
    'hart': (
        '<p>The hart is the male deer — and in Scripture, the figure of swift, surefooted longing. The most famous use is the Psalmist’s thirst: <em>"As the hart panteth after the water brooks, so panteth my soul after thee, O God. My soul thirsteth for God, for the living God: when shall I come and appear before God?"</em> (<em>Psalm 42:1-2</em>). The Psalter uses the same animal for the saint’s sure-footed running where the LORD strengthens him: <em>"He maketh my feet like hinds’ feet, and setteth me upon my high places"</em> (<em>Psalm 18:33; 2 Samuel 22:34; Habakkuk 3:19</em>). The Song of Solomon names the Beloved’s swiftness: <em>"my beloved is like a roe or a young hart"</em> (<em>Song 2:9</em>). Thirst, agility, and grace converge.</p>'
    ),
    'iron-sharpens-iron': (
        '<p>"Iron sharpens iron" is <em>Proverbs 27:17</em>’s wisdom of sharpening fellowship: <em>"Iron sharpeneth iron; so a man sharpeneth the countenance of his friend."</em> The image is the literal sharpening of metal blades by friction with each other — the friction is what produces the sharper edge. So with covenant friendship: real friends rub against each other in honest disagreement, mutual correction, and earnest debate, and both come away sharper. The man with no friends sharper than himself dulls. The man surrounded by yes-men dulls. Christian men need covenant brothers who will tell them the truth, push back on their bad ideas, and hold them to higher standards than their wives, children, and employees can. Iron requires iron.</p>'
    ),
    'jehovah-rapha': (
        '<p><em>Jehovah-Rapha</em> (יְהוָה רֹפְאֶךָ) — "the LORD that healeth thee" — is the covenant name God revealed at Marah after Moses cast the tree into the bitter waters and they were made sweet: <em>"If thou wilt diligently hearken to the voice of the LORD thy God, and wilt do that which is right in his sight, and wilt give ear to his commandments, and keep all his statutes, I will put none of these diseases upon thee, which I have brought upon the Egyptians: for I am the LORD that healeth thee"</em> (<em>Exodus 15:26</em>). The Hebrew <em>rapha</em> covers physical healing, spiritual healing, and the binding-up of the broken-hearted. The Healer of bodies in the Old Testament becomes the Healer of bodies and souls in the Gospels and the consummator of all healing in <em>Revelation 21:4</em>.</p>'
    ),
    'jezebel': (
        '<p>Jezebel was the Phoenician princess — daughter of Ethbaal the priest-king of Sidon — and queen-consort of King Ahab of Israel. She became the chief sponsor of state-imposed Baal worship in the northern kingdom (<em>1 Kings 16:31</em>): she killed the prophets of the LORD (<em>18:4</em>), supported 450 prophets of Baal and 400 of Asherah at her table (<em>18:19</em>), threatened Elijah’s life after Mount Carmel (<em>19:2</em>), and framed Naboth’s judicial murder to seize his vineyard for Ahab (<em>21:5-16</em>). She died exactly as Elijah prophesied — thrown from her window, trampled by horses, eaten by dogs (<em>2 Kings 9:30-37</em>). In <em>Revelation 2:20</em>, "Jezebel" names the false-prophetess teacher Christ rebukes at Thyatira. The archetype endures.</p>'
    ),
    'lamentation-genre': (
        '<p>Lament is the biblical genre of structured grief-prayer addressed to God. About a third of the Psalms are laments (e.g., <em>Psalms 3, 6, 13, 22, 42-43, 51, 73, 77, 88</em>); the entire book of Lamentations is a sustained funeral-dirge for fallen Jerusalem; Habakkuk and Job are extended laments. The standard pattern includes: (1) <em>address</em> to God by covenant name; (2) <em>complaint</em>, naming the grief honestly; (3) <em>request</em> for help; (4) <em>expression of trust</em> or renewed confession of faith; (5) sometimes <em>vow of praise</em>. The pivot is usually marked by <em>"yet"</em>: <em>"yet will I trust in him"</em>. Modern Christianity has nearly lost the genre and pays for it in shallow joy. Recover lament — and the pivot.</p>'
    ),
    'marital-fidelity': (
        '<p>Marital fidelity is the covenant loyalty of one spouse to the other through life — sexual exclusivity, emotional commitment, vow-keeping unto death. Hebrews summarizes the call and the warning: <em>"Marriage is honourable in all, and the bed undefiled: but whoremongers and adulterers God will judge"</em> (<em>Hebrews 13:4</em>). The seventh commandment forbids the breach: <em>"Thou shalt not commit adultery"</em> (<em>Exodus 20:14</em>). Christ extends it inward: <em>"whosoever looketh on a woman to lust after her hath committed adultery with her already in his heart"</em> (<em>Matthew 5:28</em>). Christian fidelity is therefore costly in mind, eyes, and body. The man who has guarded eyes, governed thoughts, and refused secondary attachments is the man who can be trusted with a wife.</p>'
    ),
    'rejoice': (
        '<p>To <em>rejoice</em> is to be glad, to celebrate with the soul actively engaged. In the New Testament it is given as explicit command: <em>"Rejoice in the Lord alway: and again I say, Rejoice. Let your moderation be known unto all men. The Lord is at hand"</em> (<em>Philippians 4:4-5</em>). Crucially, the rejoicing is tied not to circumstances but to <em>union with Christ</em> — <em>"in the Lord"</em>. Paul writes from a Roman prison and commands it. Christian rejoicing is therefore a discipline, not a feeling — willed gladness in a present Lord, independent of what the day brings. <em>"Rejoice with them that do rejoice, and weep with them that weep"</em> (<em>Romans 12:15</em>); <em>"Rejoice evermore"</em> (<em>1 Thessalonians 5:16</em>).</p>'
    ),
    'samaritan': (
        '<p>The Samaritans were the mixed-religion population of central Israel descended from intermarriage between the surviving Northern Israelites and the Assyrian colonists imported after Samaria’s fall in 722 BC (<em>2 Kings 17:24-41</em>). They worshipped a syncretized version of Yahwism centered at Mount Gerizim and were regarded as racial and religious half-breeds by Jews of the New Testament era — the depth of contempt visible in <em>John 4:9</em>: <em>"for the Jews have no dealings with the Samaritans."</em> Christ deliberately ministered to Samaritans: the woman at Jacob’s well (<em>John 4</em>), the ten lepers (only the Samaritan returned to give thanks, <em>Luke 17:11-19</em>), the parable of the Good Samaritan (<em>Luke 10:30-37</em>). Philip preached Samaria in <em>Acts 8</em>; revival broke out.</p>'
    ),
    'schaeffer': (
        '<p>Francis Schaeffer (1912-1984) was the American Presbyterian apologist, founder of L’Abri Fellowship in Switzerland (1955), and author whose books bridged philosophy, theology, and culture for late-twentieth-century evangelicals. Trained at Westminster Theological Seminary, ordained in the Bible Presbyterian Church, he moved to Switzerland in 1948 and from 1955 ran L’Abri as a study-and-hospitality community where seekers and skeptics lived in his home, asked their hardest questions, and worked the garden. Major books: <em>The God Who Is There</em>, <em>Escape from Reason</em>, <em>How Should We Then Live?</em>, <em>A Christian Manifesto</em>, <em>The Mark of the Christian</em>. He combined Reformed conviction, cultural-analytical depth, and pastoral warmth. His son Frank Schaeffer carried on parts of the work.</p>'
    ),
    'thankfulness': (
        '<p>Thankfulness is the saint’s disposition of recognized gift — the standing acknowledgment that what one has is given. Paul commands it explicitly and broadly: <em>"In every thing give thanks: for this is the will of God in Christ Jesus concerning you"</em> (<em>1 Thessalonians 5:18</em>); <em>"Giving thanks always for all things unto God and the Father in the name of our Lord Jesus Christ"</em> (<em>Ephesians 5:20</em>). Thanklessness is named in <em>2 Timothy 3:2</em> as one of the last-days marks of corrupted humanity: <em>"unthankful, unholy"</em>. Paul writes from prison and gives thanks ceaselessly (<em>Philippians 1:3; Colossians 1:3</em>). Christian men should learn to begin meals, days, prayers, and crises with thanks. The default tone is gratitude.</p>'
    ),
    'time-for-everything': (
        '<p>"A time for everything" comes from Ecclesiastes’ great poem of seasons: <em>"To every thing there is a season, and a time to every purpose under the heaven: A time to be born, and a time to die; a time to plant, and a time to pluck up that which is planted"</em> (<em>Ecclesiastes 3:1-2</em>). Twenty-eight times are paired in fourteen oppositions across <em>vv. 1-8</em> — birth/death, plant/pluck up, kill/heal, weep/laugh, mourn/dance, embrace/refrain, love/hate, war/peace. The wisdom is recognizing that life moves in seasons, not steady-states, and that the wise man reads the season he is in. <em>"He hath made every thing beautiful in his time"</em> (<em>v. 11</em>). The Christian discerns seasons and acts accordingly.</p>'
    ),
    'tithing': (
        '<p>Tithing is the setting apart of a tenth of one’s increase as belonging to God — practiced by Abraham (<em>"And he gave him tithes of all"</em>, <em>Genesis 14:20</em>) before Sinai, codified under Moses (<em>Leviticus 27:30-32; Numbers 18:21-32; Deuteronomy 14:22-29</em>), and criticized by Christ when scrupulous tithing replaced weightier matters: <em>"ye pay tithe of mint and anise and cummin, and have omitted the weightier matters of the law, judgment, mercy, and faith: these ought ye to have done, and not to leave the other undone"</em> (<em>Matthew 23:23</em>). Christ affirms the tithe; the New Testament generally presents it as a baseline, not a ceiling. Many Reformed traditions hold tithing as still binding; others see proportionate giving as the NT principle, with the tithe as the floor.</p>'
    ),
    'twelve': (
        '<p>Twelve, in Scripture, is the number of covenant government and ordered people — God’s structure-number, distinct from seven (His completion-number). Jacob has twelve sons (<em>Genesis 35:22</em>); Israel has twelve tribes; Aaron’s breastplate had twelve gemstones, one per tribe (<em>Exodus 28:21</em>). Christ deliberately chose twelve apostles (<em>Mark 3:13-19</em>) to govern the new Israel — and after Judas’s defection, the eleven gathered to restore the number to twelve before Pentecost (<em>Acts 1:15-26</em>). The New Jerusalem has twelve gates and twelve foundations (<em>Revelation 21:12-14</em>) — the names of the twelve tribes on the gates and the names of the twelve apostles on the foundations. Old and new covenant peoples join in one city.</p>'
    ),
    'upholding': (
        '<p>Upholding is the continual sustaining of a thing in being — the holding-up of what would otherwise fall. Hebrews names the eternal Son as the One who upholds all things by His active word: <em>"Who being the brightness of his glory, and the express image of his person, and upholding all things by the word of his power"</em> (<em>Hebrews 1:3</em>). The universe is not coasting; Christ upholds it moment by moment. The same verb pictures God’s arm under His servant: <em>"Fear thou not; for I am with thee... I will uphold thee with the right hand of my righteousness"</em> (<em>Isaiah 41:10</em>). His promises uphold His people; His Spirit upholds His prophets; His hand upholds His son. The Christian leans on Upholder.</p>'
    ),
    'waiter': (
        '<p>A waiter, in Scripture, is a servant who waits at table or attends a master — an honorable role, not a humble one in the modern dismissive sense. The word covers both the literal table-server (<em>"It is not reason that we should leave the word of God, and serve [Greek <em>diakonein</em>] tables"</em>, <em>Acts 6:2</em>) and the saint who waits on the LORD (<em>"Wait on the LORD: be of good courage, and he shall strengthen thine heart"</em>, <em>Psalm 27:14; 37:9, 34</em>). Both are the same posture: ready, attentive, prepared to act on instant command. The deacons of Acts 6 are <em>diakonoi</em> — table-servers — and their office gave us the word <em>deacon</em>. To wait is to serve standing.</p>'
    ),
    'ananias-of-damascus': (
        '<p>Ananias of Damascus was an ordinary disciple in the Jewish-Christian community of Damascus — named twice in Scripture, otherwise unknown — who was sent by the Lord in a vision to lay hands on the newly blinded Saul of Tarsus (<em>Acts 9:10-19; 22:12-16</em>). He hesitated, reasonably: <em>"Lord, I have heard by many of this man, how much evil he hath done to thy saints at Jerusalem"</em>. The Lord answered the hesitation: <em>"Go thy way: for he is a chosen vessel unto me, to bear my name before the Gentiles, and kings, and the children of Israel"</em>. Ananias obeyed. Saul received his sight, was filled with the Holy Ghost, was baptized, and arose. The most important Christian convert in the New Testament was discipled by an ordinary man no one would have predicted.</p>'
    ),
    'anaphora': (
        '<p>The anaphora is the central eucharistic prayer of historic Christian liturgy — the great thanksgiving in which the elements of bread and wine are offered up to the Father, the words of institution are recited (<em>"For I have received of the Lord that which also I delivered unto you, That the Lord Jesus the same night in which he was betrayed took bread..."</em>, <em>1 Corinthians 11:23-26</em>), and the Holy Spirit is invoked (the <em>epiclesis</em>). Most ancient liturgies include four main parts: the praise (Sanctus and beyond), the anamnesis (remembrance of Christ’s saving work), the epiclesis (calling down of the Spirit), and the intercessions. Reformed traditions retain the form simplified, refusing transubstantiation but preserving the substance: the great thanksgiving of the gathered church.</p>'
    ),
    'antithesis': (
        '<p>Antithesis, in Reformed apologetic usage (Van Til, Bahnsen, Frame), is the conviction that the Christian and non-Christian worldviews are irreducibly opposed at the foundation. The unregenerate man cannot, in his unregenerate condition, neutrally evaluate Christian claims; his fallen reason is bent against God by his own ethical commitment to autonomy (<em>"the carnal mind is enmity against God"</em>, <em>Romans 8:7</em>). There is therefore no neutral common ground from which both sides argue. The apologetic task is to expose the unbeliever’s suppression of the truth (<em>Romans 1:18-21</em>) and the internal incoherence of every system built on suppression — challenging the impossibility of the contrary. Antithesis stands behind Van Til’s transcendental method.</p>'
    ),
    'bahnsen': (
        '<p>Greg Bahnsen (1948-1995) was the American Reformed theologian who became the most effective popularizer of Cornelius Van Til’s presuppositional apologetics. Trained at Westminster Theological Seminary and the University of Southern California (PhD in philosophy), he wrote <em>Van Til’s Apologetic: Readings and Analysis</em>, <em>Always Ready</em>, and theonomist works on biblical law. His most famous debate — against atheist philosopher Gordon Stein at the University of California-Irvine in 1985 — became a teaching classic, illustrating Van Tilian method against an articulate opponent. He also debated Edward Tabash. Bahnsen died young (age 47) of complications from heart surgery. His audio lectures continue to disciple new generations of Reformed apologists.</p>'
    ),
    'benedict-of-nursia': (
        '<p>Benedict of Nursia (c. 480-547) was the Italian abbot whose <em>Rule</em> shaped Western monasticism for fifteen hundred years. Born in Umbria during the collapse of the Roman Empire, he withdrew first to a cave at Subiaco, then founded the great monastery at Monte Cassino around 529. His <em>Rule</em> (the <em>Regula Benedicti</em>) became the foundational guide for monastic life across medieval Europe — organized around prayer, work, study, and stable community under the motto <em>ora et labora</em> ("pray and work"). Protestants and Catholics alike honor his recovery of disciplined, communal Christianity in an age of cultural collapse. Rod Dreher’s 2017 book <em>The Benedict Option</em> proposes a contemporary application: a strategic retreat for renewal.</p>'
    ),
    'break-up-fallow': (
        '<p>"Break up your fallow ground" is Hosea’s agricultural metaphor for repentance — breaking up the hardened, untilled ground of the heart so that the seed of God’s word can take root and bear fruit. <em>Hosea 10:12</em> issues the call: <em>"Sow to yourselves in righteousness, reap in mercy; break up your fallow ground: for it is time to seek the LORD, till he come and rain righteousness upon you."</em> Jeremiah uses the same image: <em>"Break up your fallow ground, and sow not among thorns"</em> (<em>Jeremiah 4:3</em>). The verb is violent; the fallow heart is hard from neglect or sin; only the plow of repentance breaks it. Then the rain of righteousness can come. Christian men in spiritually dry seasons must take up the plow. Hardness must be broken before fruit can grow.</p>'
    ),
    'calvin-figure': (
        '<p>John Calvin (1509-1564) was the French theologian, exegete, and Reformer of Geneva whose <em>Institutes of the Christian Religion</em> remains the most comprehensive systematic theology of the Reformation. Trained as a humanist scholar and lawyer in Paris and Orléans, he fled France after his conversion around 1533 and settled in Geneva, where (after one expulsion and return) he led the city’s reformation from 1541 to his death. Major works: the <em>Institutes</em> (multiple editions, 1536-1559), commentaries on most of the Bible, and sermons preached daily for decades. His doctrines — sovereign election, the priesthood of all believers, the regulative principle of worship, the spirituality of the Lord’s Supper — define the Reformed tradition. <em>Soli Deo Gloria.</em></p>'
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
