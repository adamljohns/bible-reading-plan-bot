#!/usr/bin/env python3
"""Batch 27 — expand 25 more thin entries to 90-110 words each.

Targets: covenant promises, divine attributes, Hebrew vocabulary,
OT figures, NT geography, prayer petitions, slang reframes, and
sin diagnoses from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'inherit-land': (
        '<p>The promise to "inherit the land" runs as a great cord through Scripture. It was given concretely to Abraham: <em>"Unto thy seed have I given this land"</em> (<em>Genesis 15:18</em>; cf. <em>12:7; 13:15</em>). It was fulfilled under Joshua’s conquest. It was withheld in exile and partially restored under Cyrus’s decree. And it was projected eschatologically by Christ in the third Beatitude — quoting <em>Psalm 37:11</em>: <em>"Blessed are the meek: for they shall inherit the earth"</em> (<em>Matthew 5:5</em>). The promise is concrete and physical, not just spiritual abstract: the renewed earth, the new heavens and new earth (<em>Revelation 21:1-5</em>; <em>Isaiah 65:17</em>), is the saint’s eternal portion. Christianity is not escape from earth; it is restoration of it under Christ.</p>'
    ),
    'inner-room': (
        '<p>The inner room is the household’s most withdrawn chamber — a closet, store-room, or innermost bedroom — where no one passes through and no observer can intrude. Christ commands it explicitly as the place of secret prayer: <em>"But thou, when thou prayest, enter into thy closet, and when thou hast shut thy door, pray to thy Father which is in secret; and thy Father which seeth in secret shall reward thee openly"</em> (<em>Matthew 6:6</em>). The inner room strips prayer of audience; the only Witness is God. Public prayer has its place (in worship, in family, at meals), but the spine of Christian prayer is hidden — known only to the saint and to the Father. Every Christian man needs an inner room. Build one if you must.</p>'
    ),
    'kindness-biblical': (
        '<p>Biblical kindness is the disposition that treats the other as one’s own kin — extending the affection, loyalty, and care that family enjoys to those outside the bloodline. The Hebrew <em>chesed</em> covers it; the Greek <em>chrēstotēs</em> names it as fruit of the Spirit (<em>Galatians 5:22</em>). The deepest theological use of the word is Paul’s in <em>Titus 3:4-5</em>: <em>"But after that the kindness and love of God our Saviour toward man appeared, not by works of righteousness which we have done, but according to his mercy he saved us."</em> The incarnation itself is divine <em>chrēstotēs</em>. The Christian therefore is kind to strangers, beggars, enemies, and irritating relatives alike — because God has been so kind to him first.</p>'
    ),
    'leb': (
        '<p><em>Leb</em> (לֵב) — or <em>levav</em> — is the Hebrew word for heart, but vastly broader than the modern English emotional sense. The <em>leb</em> is the integrated inner core of the person — the seat of thought, will, conscience, memory, decision, intention, and (yes) emotion. <em>"Out of the heart proceed evil thoughts, murders, adulteries, fornications, thefts, false witness, blasphemies"</em> (<em>Matthew 15:19</em>): the catalogue is moral and volitional, not merely affective. <em>"Keep thy heart with all diligence; for out of it are the issues of life"</em> (<em>Proverbs 4:23</em>). The great command of the <em>Shema</em> is to love the LORD <em>"with all thine heart, and with all thy soul, and with all thy might"</em> (<em>Deuteronomy 6:5</em>). The whole man, from the inside.</p>'
    ),
    'menorah': (
        '<p>The <em>menorah</em> (מְנוֹרָה) is the seven-branched gold lampstand commanded for the tabernacle (<em>Exodus 25:31-40; 37:17-24</em>) and continued in Solomon’s and the second temple. Wrought of a single talent of pure beaten gold, it stood in the Holy Place opposite the table of showbread, and was kept burning continually by the priests (<em>Exodus 27:20-21</em>; <em>Leviticus 24:1-4</em>). It was the living picture of God’s undying light among His people — and a type Christ Himself takes up: <em>"I am the light of the world"</em> (<em>John 8:12</em>). The seven churches of Revelation are seen as seven golden candlesticks (<em>Revelation 1:12, 20</em>); Christ walks among them as the great High Priest tending the lamps.</p>'
    ),
    'mount-ebal': (
        '<p>Mount Ebal stood in central Canaan opposite Mount Gerizim — Shechem nestled in the valley between — and was the curse-mountain of the covenant ceremony. Moses commanded that six tribes (Reuben, Gad, Asher, Zebulun, Dan, and Naphtali) stand on Ebal to pronounce the curses of the law: <em>"And these shall stand upon mount Ebal to curse; Reuben, Gad, and Asher, and Zebulun, Dan, and Naphtali"</em> (<em>Deuteronomy 27:13</em>; cf. <em>Joshua 8:33</em>). Joshua faithfully obeyed, building an altar of uncut stones on Ebal, offering burnt offerings, and inscribing a copy of the law on plastered stones for all the people to read (<em>Joshua 8:30-32</em>). The covenant carries two edges — blessing and curse — and a nation called by God’s name must answer to both.</p>'
    ),
    'murmuring': (
        '<p>Murmuring is the low, persistent complaint of the heart given voice — a grumbling discontent against God’s providence and His ordained servants. It killed the wilderness generation: <em>"Neither murmur ye, as some of them also murmured, and were destroyed of the destroyer"</em> (<em>1 Corinthians 10:10</em>; cf. <em>Numbers 14:27; 16:41; Exodus 16:7-12</em>). Paul commands the New-Covenant church: <em>"Do all things without murmurings and disputings: that ye may be blameless and harmless, the sons of God, without rebuke"</em> (<em>Philippians 2:14-15</em>). Murmuring is the audible form of unbelief. The Christian man who has begun to murmur is on the road the wilderness fathers walked into the grave. Repent of it quickly; speak praise instead.</p>'
    ),
    'nacham': (
        '<p><em>Nacham</em> (נָחַם) is a remarkable double-meaning Hebrew verb. On one side, it means <em>to comfort</em> — to give breathing-room to the distressed: <em>"Comfort ye, comfort ye my people, saith your God"</em> (<em>Isaiah 40:1</em>; cf. <em>Psalm 23:4; 71:21</em>). On the other side, it means <em>to relent</em> or <em>regret</em> — a change of mind from grief: <em>"And God repented [nacham] of the evil, that he had said that he would do unto them; and he did it not"</em> (<em>Jonah 3:10</em>; cf. <em>Genesis 6:6</em>). The same verb pictures the deep breath of relief and the deep breath of grief. God’s "repenting" never names mutability in His eternal nature — it names the bend in His decree that mercy may flow.</p>'
    ),
    'olives-mount': (
        '<p>The Mount of Olives is the ridge running roughly north-south on the eastern side of Jerusalem across the Kidron Valley, rising about 2,700 feet. Several pivotal events of Scripture occurred there. David fled over it weeping at the rebellion of Absalom (<em>2 Samuel 15:30</em>). Jesus taught the Olivet Discourse on its slopes (<em>Matthew 24-25</em>), agonized in Gethsemane at its foot (<em>Matthew 26:36-46</em>), and bodily ascended from it after the resurrection (<em>Acts 1:9-12</em>). The angels promised, <em>"This same Jesus, which is taken up from you into heaven, shall so come in like manner as ye have seen him go"</em> (<em>Acts 1:11</em>). Zechariah prophesies: <em>"his feet shall stand in that day upon the mount of Olives"</em> (<em>Zechariah 14:4</em>) at His return.</p>'
    ),
    'samson-figure': (
        '<p>Samson was the last and most tragic of Israel’s judges (c. 1075 BC) — a Nazirite from the womb (<em>Judges 13:5</em>) gifted with supernatural strength tied to his uncut hair, charged with beginning Israel’s deliverance from Philistine oppression. The narrative of <em>Judges 13-16</em> records his exploits: tearing a lion, killing thirty Philistines for a riddle’s wager, slaying a thousand with the jawbone of an ass, carrying off the gates of Gaza. But he repeatedly compromised his Nazirite vow through women — culminating in his betrayal by Delilah, his blinding, and his Philistine slavery. The Spirit returned at the end; Samson pulled down Dagon’s temple in his death, killing more Philistines in death than in life. Compromised men can still die well.</p>'
    ),
    'scapegoat-azazel': (
        '<p>The scapegoat was the second goat of the Day of Atonement ritual in <em>Leviticus 16</em>. After the first goat was slain as a sin-offering and its blood sprinkled on the mercy seat, the high priest laid both hands on the head of the live goat and confessed over it <em>"all the iniquities of the children of Israel, and all their transgressions in all their sins"</em>, transferring them symbolically (<em>16:21</em>). The goat — destined <em>"for Azazel"</em> (a contested name, perhaps a wilderness demon, or a removal-name) — was then led by the appointed man into the wilderness to a solitary land. Tyndale coined the English <em>"scape-goat"</em> to translate the term. Christ fulfills both goats: slain victim and sin-bearer driven outside the camp.</p>'
    ),
    'secret-place': (
        '<p>The "secret place" is the hidden, intimate refuge of YHWH’s presence — known by experience to the saint who dwells in it. <em>Psalm 91:1</em>’s opener is the great text: <em>"He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty."</em> David repeats it: <em>"For in the time of trouble he shall hide me in his pavilion: in the secret of his tabernacle shall he hide me"</em> (<em>Psalm 27:5</em>; cf. <em>31:20; 32:7</em>). The saint’s life is sustained by a private, hidden communion with God that observers do not see and the world cannot enter. Christian men whose public life is strong but whose secret place is empty will eventually fail in both. Tend the hidden.</p>'
    ),
    'sentinel': (
        '<p>A sentinel is a soldier on watch — the more formal cousin of the sentry. Scripture’s sentinel is the watchman of <em>Ezekiel 33:1-9</em> who must warn the city, the porter of <em>Mark 13:34</em> commanded to watch through the night, and the elder of <em>Hebrews 13:17</em> watching for souls <em>"as they that must give account."</em> The sentinel sees first, and what he sees shapes his warning. He cannot save anyone by sight alone — only by sounding the alarm. Pastors, fathers, magistrates, citizens — each holds a sentinel’s post in proportion to his sphere. The unsounded alarm is the sentinel’s sin. The unheeded alarm is the city’s. Sleep at the post is the gravest dereliction. Wake up.</p>'
    ),
    'session-christ': (
        '<p>The "session of Christ" is the technical doctrinal name for the seated reign of the risen, ascended Lord at the right hand of God. <em>"This man, after he had offered one sacrifice for sins for ever, sat down on the right hand of God"</em> (<em>Hebrews 10:12</em>; cf. <em>1:3; Mark 16:19; Acts 2:33; Ephesians 1:20-22</em>). The posture is unprecedented for a priest — Old-Covenant priests stood daily (<em>Hebrews 10:11</em>), because their work was never finished. Christ’s sitting declares three things at once: the sacrifice complete (the Priest sits), the King enthroned (the throne is His), and the Father’s pleasure secured (the right hand of glory). He reigns now. He is not waiting to begin reigning at His return; He reigns until every enemy is under His feet.</p>'
    ),
    'slander': (
        '<p>Slander is false or malicious speech that injures another’s reputation — the breaking of the ninth commandment (<em>Exodus 20:16</em>) in everyday clothes. Scripture forbids it absolutely. The slanderer is grouped with the murderer and idolater in the catalogue at the close of <em>Romans 1:29-30</em>: <em>"backbiters, haters of God, despiteful, proud, boasters."</em> The Greek <em>diabolos</em> ("slanderer") is the very title of the devil. A deacon’s wife is disqualified by the trait: <em>"Even so must their wives be grave, not slanderers, sober, faithful in all things"</em> (<em>1 Timothy 3:11</em>). Christian men must refuse it absolutely — not gossip, not innuendo, not cleverly worded half-truths. <em>"Speak evil of no man"</em> (<em>Titus 3:2</em>).</p>'
    ),
    'thy-kingdom-come': (
        '<p>"Thy kingdom come" is the second petition of the Lord’s Prayer: <em>"Our Father which art in heaven, Hallowed be thy name. Thy kingdom come. Thy will be done in earth, as it is in heaven"</em> (<em>Matthew 6:9-10</em>). It is an eschatological cry for the in-breaking of God’s reign — both the present-tense advance through the church’s witness and the future-tense consummation at Christ’s return. The petition aligns the saint with God’s kingdom-purpose against every rival kingdom (worldly empire, fleshly self-rule, demonic darkness). To pray it sincerely is to want His reign over <em>everything</em> — including the petitioner’s own life, household, vocation, and nation. The Christian who prays <em>"thy kingdom come"</em> renounces the throne of his own life.</p>'
    ),
    'todah': (
        '<p><em>Todah</em> (תּוֹדָה) is the Hebrew word for <em>thanksgiving</em> — specifically a <em>public</em>, often sacrificial, declaration of God’s deliverance: <em>"I was in trouble; God delivered me; here is my thanks-offering."</em> The <em>todah</em> sacrifice (<em>Leviticus 7:11-15</em>) was a category of peace offering offered with unleavened cakes, eaten the same day, and accompanied by a public testimony of what God had done. Psalms 30, 32, 116, and 138 are <em>todah</em>-psalms. <em>"O give thanks unto the LORD; for he is good: because his mercy endureth for ever. Let the redeemed of the LORD say so, whom he hath redeemed from the hand of the enemy"</em> (<em>Psalm 107:1-2</em>). Modern Hebrew uses <em>todah</em> as the everyday word for "thanks." Recover the public testimony.</p>'
    ),
    'triggered': (
        '<p>"Triggered" in modern usage names an involuntary distress response. Sometimes it is a real PTSD trigger — a sound, smell, or word that genuinely re-fires trauma neurology — and is to be treated with care. Often it is loosely deployed for any strong negative reaction, especially to ideas or speech that displease the speaker. Scripture distinguishes both categories: there is a real wound that needs Christ’s healing (<em>"He healeth the broken in heart, and bindeth up their wounds"</em>, <em>Psalm 147:3</em>), and a flesh that needs Christ’s mortification (<em>"Mortify therefore your members which are upon the earth"</em>, <em>Colossians 3:5</em>). Confusing the two is destructive in both directions. Christian pastoral care knows when to bandage and when to crucify.</p>'
    ),
    'unchangeable': (
        '<p>Unchangeable names the divine attribute by which God neither shifts in being, in will, nor in word. It is the doctrine of <em>divine immutability</em>: <em>"For I am the LORD, I change not"</em> (<em>Malachi 3:6</em>); <em>"Every good gift and every perfect gift is from above, and cometh down from the Father of lights, with whom is no variableness, neither shadow of turning"</em> (<em>James 1:17</em>); the LORD’s counsel <em>"shall stand"</em> (<em>Isaiah 46:10</em>). <em>Hebrews 7:24</em> applies it to Christ’s priesthood: <em>"this man, because he continueth ever, hath an unchangeable priesthood."</em> The Christian rests here: God’s promises do not rot, His mercies do not fluctuate, His Word does not get repealed in the next administration. He is who He has always been.</p>'
    ),
    'vigilance': (
        '<p>Vigilance is sustained, alert watchfulness against danger — the spiritual discipline of guarding the heart, the household, the church, and the doctrine entrusted to one’s care. Christ commands it of every disciple: <em>"Watch and pray, that ye enter not into temptation"</em> (<em>Matthew 26:41</em>); <em>"What I say unto you I say unto all, Watch"</em> (<em>Mark 13:37</em>). Peter applies it to the prowling enemy: <em>"Be sober, be vigilant; because your adversary the devil, as a roaring lion, walketh about, seeking whom he may devour"</em> (<em>1 Peter 5:8</em>). Paul charges the Ephesian elders: <em>"Therefore watch, and remember, that by the space of three years I ceased not to warn every one night and day with tears"</em> (<em>Acts 20:31</em>). Elders, fathers, pastors — live by vigilance.</p>'
    ),
    'water-from-rock': (
        '<p>The water-from-the-rock was the wilderness miracle of YHWH providing water from a stone when Israel was dying of thirst. The first occurrence was at Rephidim, where Moses struck the rock with his rod at YHWH’s command and water gushed forth (<em>Exodus 17:1-7</em>). The second was at Meribah-Kadesh, where Moses — in anger — struck the rock twice instead of speaking to it as commanded, and was excluded from the promised land for it (<em>Numbers 20:1-13</em>). Paul reads the rock typologically: <em>"and did all drink the same spiritual drink: for they drank of that spiritual Rock that followed them: and that Rock was Christ"</em> (<em>1 Corinthians 10:4</em>). The smitten Rock is Christ; from His side flowed living water.</p>'
    ),
    'yhwh-shalom': (
        '<p><em>YHWH-Shalom</em> (יְהוָה שָׁלוֹם) — "the LORD our peace" — is the covenant name Gideon gave the altar he built after the Angel of the LORD appeared to him at Ophrah and reassured him: <em>"Peace be unto thee; fear not: thou shalt not die. Then Gideon built an altar there unto the LORD, and called it Jehovah-shalom"</em> (<em>Judges 6:23-24</em>). The name declares not merely that the LORD <em>gives</em> peace but that He <em>is</em> peace — the substance, not only the source. Paul echoes it in <em>Ephesians 2:14</em>: <em>"For he is our peace, who hath made both one."</em> Christ is the incarnate <em>YHWH-Shalom</em>; in Him hostility ceases — between sinner and God, between Jew and Gentile, between brothers.</p>'
    ),
    'yirah': (
        '<p><em>Yirah</em> (יִרְאָה) is the Hebrew word for fear — especially "the fear of the LORD." It is not anxious dread or terrified flight; it is reverent awe that recognizes God for who He is and leads to obedience. <em>"The fear of the LORD is the beginning of wisdom"</em> (<em>Proverbs 9:10; Psalm 111:10</em>); <em>"By the fear of the LORD men depart from evil"</em> (<em>Proverbs 16:6</em>); <em>"The fear of the LORD prolongeth days"</em> (<em>Proverbs 10:27</em>). The <em>Shema</em>’s love of God (<em>Deuteronomy 6:5</em>) implies its <em>yirah</em>: covenant love and reverent fear are not opposites but two sides of the same heart-disposition. The man without <em>yirah</em> may be religious; he is not yet wise. Begin here.</p>'
    ),
    'arise': (
        '<p>To <em>arise</em> is to stand up, get up, rise — and Scripture loads the verb in four directions. First, the imperative of urgent obedience: <em>"Arise, get thee to Nineveh"</em> (<em>Jonah 1:2</em>); <em>"Arise, take up thy bed, and walk"</em> (<em>John 5:8</em>). Second, the cry for divine intervention: <em>"Arise, O LORD; save me, O my God"</em> (<em>Psalm 3:7; 7:6; 9:19</em>). Third, the resurrection-verb of Christ Himself: <em>"He is not here: for he is risen"</em> (<em>Matthew 28:6</em>). And fourth, the eschatological summons to the dead in Christ: <em>"Awake thou that sleepest, and arise from the dead, and Christ shall give thee light"</em> (<em>Ephesians 5:14</em>). The Christian life is one extended <em>arise</em>: get up, follow, fight, rise on the last day.</p>'
    ),
    'asaph': (
        '<p>Asaph was the chief of the Levitical worship leaders appointed by David for tabernacle and (later) temple service (<em>1 Chronicles 16:4-7, 37; 25:1-2</em>). He was a singer, a musician, and a Spirit-given composer in his own right. The Psalter attributes twelve psalms to Asaph or "the sons of Asaph" — Psalms 50 and 73-83 — including some of the deepest theological wrestling in Scripture. <em>Psalm 73</em> is the great honest grappling with the prosperity of the wicked, ending in the resolution of the sanctuary: <em>"Whom have I in heaven but thee? and there is none upon earth that I desire beside thee"</em> (<em>v. 25</em>). Asaph’s gift was leading the people of God to confess God in song through doubt.</p>'
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
