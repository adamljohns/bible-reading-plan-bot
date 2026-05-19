#!/usr/bin/env python3
"""Batch 50 — fiftieth-batch milestone — 25 more entries.

Brings the sprint total to 1,250 entries substantively expanded.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'augustine-figure': (
        '<p>Augustine of Hippo (354-430) was the North African bishop, theologian, and former rhetorician whose <em>Confessions</em> and <em>City of God</em> shaped Western Christianity for fifteen centuries. Converted at Milan in 386 under Ambrose’s preaching and the famous garden-voice <em>"Tolle lege"</em> ("Take up and read"), ordained priest in 391 and bishop of Hippo Regius in 395, he served as pastor-theologian until his death during the Vandal siege. Major works: <em>Confessions</em> (autobiographical theology), <em>The City of God</em> (philosophy of history against pagan attack), <em>On the Trinity</em>, <em>On Christian Doctrine</em>. He fought Manichaean dualism, Donatist schism, and especially Pelagianism — establishing the doctrines of grace the Reformers later recovered. Catholic and Protestant alike claim him; Calvin called him <em>"my own."</em></p>'
    ),
    'book-of-covenant': (
        '<p>The Book of the Covenant is the written record of a covenant’s terms — kept and read aloud at moments of ratification or renewal. The original at Sinai: Moses <em>"took the book of the covenant, and read in the audience of the people: and they said, All that the LORD hath said will we do, and be obedient. And Moses took the blood, and sprinkled it on the people"</em> (<em>Exodus 24:7-8</em>). Josiah’s priests rediscovered it in the temple during repairs (<em>2 Kings 22:8</em>), and Josiah read it publicly and renewed the covenant (<em>2 Kings 23:2-3</em>). Ezra read the law at the Water Gate (<em>Nehemiah 8</em>). The pattern is recurring: covenant lives in a written book, read aloud, renewed by the people’s public assent.</p>'
    ),
    'brainrot': (
        '<p>"Brainrot" is Gen-Z’s own self-diagnosis of the cognitive damage produced by endless short-form video, algorithmic meme-feeds, and TikTok scrolling — manifested in shortened attention, vocabulary collapse into in-group memes (<em>"skibidi sigma rizz"</em>), weakened reasoning, and a felt sense that the brain has become mush. The slang’s honesty is notable: the generation most affected has named the phenomenon and admits its damage. Scripture provides the deeper diagnosis. Christ commands wholehearted love of God: <em>"with all thy mind"</em> (<em>Mark 12:30</em>). Paul commands mind-stewardship: <em>"bringing into captivity every thought to the obedience of Christ"</em> (<em>2 Corinthians 10:5</em>). The mind is not a passive feed-receptacle; it is a member to be governed.</p>'
    ),
    'canonical-reading': (
        '<p>Canonical Reading interprets any biblical text in light of its place in the whole canon — the 66-book Christian Bible read as a unified whole rather than as disconnected ancient documents. Brevard Childs (Yale, late twentieth century) developed the method as an alternative to atomistic historical-critical fragmentation. Canonical reading recognizes that the church received the Bible <em>as canon</em> — as the rule of faith and life with each part contributing to one coherent message. Closely aligned with Reformed and confessional readings, which have always insisted on Scripture interpreting Scripture (<em>analogia Scripturae</em>). The method respects each text’s historical particularity while never losing sight of the unity given by one divine Author writing through many human authors.</p>'
    ),
    'circumcision-of-heart': (
        '<p>Circumcision of the heart is the interior, spiritual counterpart to the physical sign of the Abrahamic covenant — the cutting away of the heart’s callused, rebellious "foreskin" so that the believer may love and obey God. The Old Testament prophets called for it: <em>"Circumcise therefore the foreskin of your heart, and be no more stiffnecked"</em> (<em>Deuteronomy 10:16</em>); <em>"And the LORD thy God will circumcise thine heart"</em> (<em>30:6</em>); <em>"Circumcise yourselves to the LORD, and take away the foreskins of your heart"</em> (<em>Jeremiah 4:4</em>). Paul makes it the substance the New Covenant fulfills: <em>"he is a Jew, which is one inwardly; and circumcision is that of the heart, in the spirit, and not in the letter"</em> (<em>Romans 2:29</em>; cf. <em>Colossians 2:11</em>). Inward sign of true covenant membership.</p>'
    ),
    'city-motif': (
        '<p>The City Motif traces human concentration through Scripture. Cain builds the first city after his fratricide (<em>"And he builded a city, and called the name of the city, after the name of his son, Enoch"</em>, <em>Genesis 4:17</em>). Babel attempts to make a name without God (<em>Genesis 11</em>). Jerusalem becomes God’s chosen city under David and Solomon. Babylon emerges as the great rival empire — fallen finally as the harlot in <em>Revelation 17-18</em>. And the New Jerusalem descends from heaven as the bride at the close (<em>Revelation 21-22</em>). Two cities run through the Bible: Augustine called them the City of Man and the City of God. Every Christian is dual-citizen, traveling between them, ultimately bound for one.</p>'
    ),
    'counterfeit-spirit': (
        '<p>A counterfeit spirit is an evil spiritual power impersonating the Holy Spirit — or claiming inspiration from God while actually opposing Him. <em>1 John 4:1-3</em> commands the church: <em>"Beloved, believe not every spirit, but try the spirits whether they are of God: because many false prophets are gone out into the world. Hereby know ye the Spirit of God: Every spirit that confesseth that Jesus Christ is come in the flesh is of God: And every spirit that confesseth not that Jesus Christ is come in the flesh is not of God: and this is that spirit of antichrist."</em> The test is Christological. Counterfeit spirits abound in every age — false revival, prosperity-gospel emotional manipulation, occult deception, demonic visitation. Test by Scripture and by Christology.</p>'
    ),
    'covenant-witness': (
        '<p>A covenant witness is the third party — person, stone, song, or natural feature — that bears testimony to the covenant’s ratification. The mode varies. Joshua set up a great stone under the oak in Shechem: <em>"And Joshua said unto all the people, Behold, this stone shall be a witness unto us; for it hath heard all the words of the LORD which he spake unto us"</em> (<em>Joshua 24:27</em>). Jacob and Laban erected the cairn of Mizpah (<em>Genesis 31:48-52</em>). Moses commanded a song to be a witness against rebellious Israel (<em>Deuteronomy 31:19-21</em>; <em>Deuteronomy 32</em>). Heaven and earth are summoned to witness in <em>Deuteronomy 30:19</em>. Covenant cannot be broken silently; witnesses remember.</p>'
    ),
    'cursing-speech': (
        '<p>Cursing speech is the calling-down of evil on persons made in God’s image — and the corrupt communication that proceeds from a heart not yet brought under the lordship of Christ. James marvels at the inconsistency: <em>"Therewith bless we God, even the Father; and therewith curse we men, which are made after the similitude of God. Out of the same mouth proceedeth blessing and cursing. My brethren, these things ought not so to be"</em> (<em>James 3:9-10</em>). Paul commands its replacement: <em>"Let no corrupt communication proceed out of your mouth, but that which is good to the use of edifying"</em> (<em>Ephesians 4:29</em>). Christ Himself warns that idle words will be judged (<em>Matthew 12:36</em>). Christian men must train their tongues to bless.</p>'
    ),
    'daddy-o': (
        '<p>"Daddy-o" is the mid-twentieth-century informal address for a man — <em>"hey, daddy-o"</em> — era-stamped Boomer / pre-Boomer slang originating in jazz and beat-culture vocabulary of the 1940s-50s. It is a form of <em>address</em> rather than a category-name. The Christian observation: address-vocabulary reveals cultural assumptions about whom one is speaking to and what posture one takes toward them. <em>"Daddy-o"</em> is jocular and equalizing — it flattens hierarchy. Scripture is more careful with address: pastors are <em>"esteem(ed) very highly in love for their work’s sake"</em> (<em>1 Thessalonians 5:13</em>); elders are honored; fathers are not called by first names by their sons. Recover address that respects.</p>'
    ),
    'dialectical-theology': (
        '<p>Dialectical theology (sometimes called Crisis Theology) arose in the 1920s against nineteenth-century liberal Protestantism, which had domesticated God into the highest human ideal and reduced theology to ethics. Karl Barth (<em>Epistle to the Romans</em>, 1922) reasserted God’s radical otherness and the impossibility of reaching Him through human reason or religious effort — the "infinite qualitative distinction" between God and man. Major figures: Barth, Emil Brunner, Friedrich Gogarten, Rudolf Bultmann (early). The movement recovered important truths — God’s transcendence, the inadequacy of natural theology, the necessity of revelation — but the Reformed tradition critiques its tendency to relativize Scripture’s propositional content and to make revelation a perpetual event rather than a written deposit. Useful as corrective; insufficient as foundation.</p>'
    ),
    'disagree': (
        '<p>To disagree is to hold a different judgment than another — and Scripture treats it as not in itself sinful. Many faithful disagreements are recorded: Paul withstood Peter to the face at Antioch over hypocrisy (<em>"I withstood him to the face, because he was to be blamed"</em>, <em>Galatians 2:11</em>). Paul and Barnabas parted ways over John Mark (<em>"the contention was so sharp between them, that they departed asunder one from the other"</em>, <em>Acts 15:39</em>) — both were faithful men. The Bereans examined the Scriptures daily to test even Paul’s teaching (<em>Acts 17:11</em>). What Scripture forbids is <em>contentiousness</em> (<em>Romans 16:17; 1 Timothy 6:4</em>) and <em>strife</em> (<em>Galatians 5:20</em>) — not honest, charitable disagreement. Christian men must learn to disagree well.</p>'
    ),
    'discernment-spirits': (
        '<p>"Do not believe every spirit, but test the spirits to see whether they are from God; for many false prophets have gone out into the world"</em> (<em>1 John 4:1</em>, modernized rendering). Paul lists <em>"the discerning of spirits"</em> as a spiritual gift: <em>"To another the working of miracles; to another prophecy; to another discerning of spirits"</em> (<em>1 Corinthians 12:10</em>). This gift is exercised through Scripture (does the spirit confess Christ come in the flesh?), through fruit-inspection (<em>Matthew 7:16</em>), through doctrinal soundness (<em>Galatians 1:8-9</em>), and through Spirit-given sensitivity to detect demonic counterfeit, fleshly self-deception, and false teaching dressed in pious language. In our seducing-spirits age (<em>1 Timothy 4:1</em>), the church desperately needs men exercising this gift.</p>'
    ),
    'divorce-biblical': (
        '<p>Jesus taught that God’s design was lifelong union: <em>"What therefore God hath joined together, let not man put asunder"</em> (<em>Matthew 19:6</em>). Moses permitted divorce <em>"because of the hardness of your hearts"</em> (<em>19:8</em>) — a concession, not a creation-norm. Jesus identified sexual immorality (<em>porneia</em>) as a ground for divorce: <em>"Whosoever shall put away his wife, except it be for fornication, and shall marry another, committeth adultery"</em> (<em>19:9</em>). Paul added abandonment by an unbelieving spouse as a second ground: <em>"if the unbelieving depart, let him depart. A brother or a sister is not under bondage in such cases"</em> (<em>1 Corinthians 7:15</em>). The Reformed and confessional tradition has historically held these two grounds as the only biblical grounds for divorce.</p>'
    ),
    'dorcas': (
        '<p>Dorcas (also called by her Aramaic name <em>Tabitha</em>) was a disciple of Joppa described in <em>Acts 9:36-42</em> as <em>"full of good works and almsdeeds which she did"</em> — particularly making coats and garments for the widows of the city. She fell sick and died; the widows of Joppa gathered around her body weeping, showing Peter the very coats and garments she had made for them. Peter sent them all out, knelt by the body, prayed, and said, <em>"Tabitha, arise."</em> She opened her eyes and sat up; Peter gave her his hand, lifted her up, and presented her alive to the saints and widows. <em>"And it was known throughout all Joppa; and many believed in the Lord"</em> (<em>9:42</em>). Quiet faithfulness produced loud witness.</p>'
    ),
    'earthen-vessels': (
        '<p>"We have this treasure in earthen vessels, that the excellency of the power may be of God, and not of us"</em> (<em>2 Corinthians 4:7</em>). The treasure is the gospel — <em>"the light of the knowledge of the glory of God in the face of Jesus Christ"</em> (<em>v. 6</em>); the earthen vessels are weak, fragile, breakable mortals — clay pots, cheap pottery, common dishes. Paul names God’s strategy: He deliberately puts His glory in ordinary containers so that the surpassing power is unmistakably from Him. The Christian who feels too weak, too ordinary, too easily broken to be of use should reread the verse. Weakness is not a disqualification; it is the design. Earthen vessels carry the King’s treasure. The cracks let the light out.</p>'
    ),
    'exodus-motif': (
        '<p>The Exodus Motif is the recurring biblical pattern of God’s deliverance of His people from bondage to inheritance — established in Israel’s departure from Egypt (<em>Exodus 1-15</em>) and recapitulated throughout Scripture. The return from Babylonian exile is the second great Exodus, prophesied in Isaiah 40-66. The Christian conversion is a personal Exodus — out of slavery to sin into liberty in Christ. <em>"And, behold, there talked with him two men, which were Moses and Elias: Who appeared in glory, and spake of his decease [Greek <em>exodos</em>] which he should accomplish at Jerusalem"</em> (<em>Luke 9:30-31</em>) — Christ’s death is the great Exodus. The ultimate Exodus awaits at His return, when the church marches out of the wilderness of this age into the promised consummation.</p>'
    ),
    'father': (
        '<p>A father is a man who begets, adopts, or raises children — bearing God-given authority and responsibility for their physical provision, spiritual formation, and moral instruction. Fatherhood is grounded in God’s own identity: Scripture reveals God supremely as <em>"our Father which art in heaven"</em> (<em>Matthew 6:9</em>). Every human father is therefore a derivative office, named from the Father: <em>"For this cause I bow my knees unto the Father of our Lord Jesus Christ, Of whom the whole family in heaven and earth is named"</em> (<em>Ephesians 3:14-15</em>). Paul charges fathers specifically: <em>"And, ye fathers, provoke not your children to wrath: but bring them up in the nurture and admonition of the Lord"</em> (<em>Ephesians 6:4</em>). Honor your father; be one.</p>'
    ),
    'festus': (
        '<p>Porcius Festus succeeded Felix as Roman procurator of Judea around AD 59 — and inherited Paul’s long-unresolved case at Caesarea. Unlike Felix, who had left Paul bound for two years hoping for a bribe (<em>Acts 24:27</em>), Festus moved promptly. He refused to deliver Paul to the Sanhedrin’s ambush (<em>Acts 25:1-12</em>) and accepted Paul’s appeal to Caesar: <em>"Hast thou appealed unto Caesar? unto Caesar shalt thou go"</em> (<em>25:12</em>). Before sending Paul to Rome, he convened a hearing with King Agrippa II and his sister Bernice, at which Paul preached the gospel and Festus interrupted with the famous outburst: <em>"Paul, thou art beside thyself; much learning doth make thee mad"</em> (<em>26:24</em>). Rome’s judicial procedure providentially delivered the apostle to Caesar’s household.</p>'
    ),
    'first-and-last': (
        '<p>"First and last" carries two main usages in Scripture. First, Christ’s reversal-saying about kingdom-economy: <em>"But many that are first shall be last; and the last shall be first"</em> (<em>Matthew 19:30; 20:16; Mark 10:31; Luke 13:30</em>) — the kingdom upends the world’s rankings. The rich young ruler walks away grieved; the poor widow receives commendation; the prodigal is welcomed home; the prostitutes and publicans enter the kingdom before the religious. Second, Christ’s self-naming title: <em>"I am Alpha and Omega, the beginning and the ending"</em> (<em>Revelation 1:8</em>); <em>"I am the first and the last: I am he that liveth, and was dead; and, behold, I am alive for evermore"</em> (<em>1:17-18; 2:8; 22:13</em>). He brackets all of history — He is the first and the last.</p>'
    ),
    'foot': (
        '<p>The foot is the body part Scripture associates with the lowliest service (the washing of feet — <em>John 13</em>), the beauty of the gospel-messenger (<em>"How beautiful upon the mountains are the feet of him that bringeth good tidings"</em>, <em>Isaiah 52:7; Romans 10:15</em>), the pilgrim’s sojourning (<em>"By faith Abraham, when he was called to go out into a place which he should after receive for an inheritance, obeyed; and he went out, not knowing whither he went"</em>, <em>Hebrews 11:8</em>), and the King’s final triumph (<em>"For he must reign, till he hath put all enemies under his feet"</em>, <em>1 Corinthians 15:25; Psalm 110:1</em>). The dust on the feet of the apostles was the witness against rejecting cities (<em>Matthew 10:14</em>). Feet matter in Scripture.</p>'
    ),
    'fountain-of-life': (
        '<p>The fountain of life is Proverbs’ recurring image for what gives life — and the book names several springs as <em>fountain-of-life</em>-equivalent. <em>"The fear of the LORD is a fountain of life, to depart from the snares of death"</em> (<em>Proverbs 14:27</em>). <em>"The law of the wise is a fountain of life"</em> (<em>13:14</em>). <em>"The mouth of a righteous man is a well of life"</em> (<em>10:11</em>). <em>"Understanding is a wellspring of life unto him that hath it"</em> (<em>16:22</em>). And supremely the LORD Himself: <em>"For with thee is the fountain of life: in thy light shall we see light"</em> (<em>Psalm 36:9</em>). Christ takes up the image: <em>"the water that I shall give him shall be in him a well of water springing up into everlasting life"</em> (<em>John 4:14</em>).</p>'
    ),
    'funky': (
        '<p>"Funky" is the positive Boomer-era adjective for music or style judged soulful, earthy, rhythmic, and distinctively unpolished — tied to the Funk music genre from James Brown onward. The slang carries an aesthetic conviction worth examining: that polish and over-refinement can flatten what is honest and embodied in art. Scripture commends skill in worship (<em>"Sing unto him a new song; play skilfully with a loud noise"</em>, <em>Psalm 33:3</em>) but also commends the loud, embodied, soul-engaged praise that Western Christianity has often sanitized: <em>"Praise him with the timbrel and dance: praise him with stringed instruments and organs. Praise him upon the loud cymbals"</em> (<em>Psalm 150:4-5</em>). Worship can be funky. Just keep it holy.</p>'
    ),
    'genesis': (
        '<p>Genesis is the first book of the Bible — attributed by Christ and the New Testament writers to Moses (<em>Matthew 19:4-8; Mark 12:26; Luke 24:44; John 5:46-47</em>). <em>Genesis 1-11</em> covers primeval history: creation in six days, the Sabbath rest, the fall, Cain and Abel, the line of Seth, the global flood, Noah’s covenant, and Babel. <em>Genesis 12-50</em> covers the patriarchs: Abraham (chs. 12-25), Isaac (chs. 21-35), Jacob (chs. 25-50), and Joseph (chs. 37-50). Genesis establishes every major biblical theme: God’s sovereign creation, sin and judgment, the seed of the woman, election, covenant, blessing through Abraham’s seed, Christ-typology in Isaac and Joseph, the longing for a promised land. The whole Bible flows from Genesis.</p>'
    ),
    'haggai-prophet': (
        '<p>Haggai was a post-exilic prophet active in 520 BC alongside Zechariah. His brief two-chapter book contains four dated oracles delivered between August (1 Elul) and December (24 Chislev) of 520 to rouse the returned exiles to finish rebuilding the temple they had begun in 538 BC and then neglected for sixteen years while building their own paneled houses. <em>"Is it time for you, O ye, to dwell in your cieled houses, and this house lie waste? ... Consider your ways"</em> (<em>Haggai 1:4-5</em>). The people responded; the work resumed; the second temple was completed in 516 BC. Haggai promised: <em>"The glory of this latter house shall be greater than of the former"</em> (<em>2:9</em>) — fulfilled when Christ Himself entered it.</p>'
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
