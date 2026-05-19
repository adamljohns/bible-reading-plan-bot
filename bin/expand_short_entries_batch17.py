#!/usr/bin/env python3
"""Batch 17 — expand 25 more thin entries to 90-110 words each.

Targets: heart-states, tabernacle theology, sacraments, atonement
theories, ecclesial qualifications, and KJV idioms from the 30-50
word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'heart-fearful': (
        '<p>A fearful heart, in the bad sense, is the spirit of cowardice and craven timidity that paralyzes obedience. Paul warns Timothy directly: <em>"God hath not given us the spirit of fear; but of power, and of love, and of a sound mind"</em> (<em>2 Timothy 1:7</em>). The fearful are listed first in <em>Revelation 21:8</em>: <em>"the fearful, and unbelieving, and the abominable... shall have their part in the lake which burneth with fire."</em> This is not the fear of God (which is the beginning of wisdom) nor the natural startle of danger; it is the settled cowardice that refuses to obey God because of what man might do. The remedy is the cross of Christ remembered, the presence of Christ rehearsed, and the call of Christ obeyed in spite of trembling knees.</p>'
    ),
    'heart-soft': (
        '<p>A soft heart is the great gift of the new covenant, promised in <em>Ezekiel 36:26</em>: <em>"A new heart also will I give you, and a new spirit will I put within you: and I will take away the stony heart out of your flesh, and I will give you an heart of flesh."</em> A soft heart feels conviction quickly, receives the Word gladly, turns toward God repeatedly, and weeps with those who weep. It is the opposite of the calloused, deaf, presuming heart of natural unbelief. Christ commends Josiah for it (<em>2 Chronicles 34:27</em>). Christian men must guard it carefully — every harbored sin, neglected prayer, and unrepented bitterness adds a layer of stone. Keep it soft by daily repentance.</p>'
    ),
    'horns-altar': (
        '<p>The horns of the altar were the four upraised projections at the corners of the bronze altar of burnt offering (<em>Exodus 27:2</em>) and the smaller golden altar of incense (<em>Exodus 30:2-3</em>). Sacrificial blood was smeared on them on the Day of Atonement (<em>Leviticus 16:18</em>) and on every sin offering (<em>Leviticus 4:7, 18, 25, 30, 34</em>), marking the altar as the meeting place between blood and God. Fugitives clung to them as last refuge: Adonijah (<em>1 Kings 1:50-51</em>) and Joab (<em>1 Kings 2:28</em>) both fled there in fear. The horns prefigure Christ: He is the altar, the sacrifice, and the sanctuary — the only refuge to which sinners may flee and find covenant safety.</p>'
    ),
    'husband-of-one-wife': (
        '<p>"Husband of one wife" (Greek <em>mias gunaikos andra</em>, literally "a one-woman man") is Paul’s first qualification for elder and deacon (<em>1 Timothy 3:2, 12</em>; <em>Titus 1:6</em>). It does not mean "married only once" (which would disqualify widowers and divorcees-for-adultery alike); it means devoted in heart, eyes, and conduct to his wife alone — sexually faithful, emotionally faithful, visually faithful. He is not a flirt, not a porn-user, not a man whose eye wanders, not a polygamist, not a serial divorcer. The qualification is character before the spotlight ever falls on him. A church run by men whose households are sound is a church protected against the most common pastoral catastrophes.</p>'
    ),
    'laodicea': (
        '<p>Laodicea was a wealthy, complacent Roman city in the Lycus valley of Asia Minor — famous for its banking (Cicero cashed checks there), its black wool industry, and its renowned eye-salve school of medicine. Yet the church there received the seventh and most severe of Christ’s seven letters: <em>"I know thy works, that thou art neither cold nor hot... So then because thou art lukewarm, and neither cold nor hot, I will spue thee out of my mouth"</em> (<em>Revelation 3:14-22</em>). The risen Christ counsels them to buy gold tried in the fire, white raiment, and eyesalve — the very things the city prided itself on producing. The letter ends with the most famous invitation in Revelation: <em>"Behold, I stand at the door, and knock."</em></p>'
    ),
    'lords-supper-doctrine': (
        '<p>The Lord’s Supper is the church’s ordained meal of bread and cup, instituted by Christ on the night He was betrayed (<em>Matthew 26:26-29</em>; <em>1 Corinthians 11:23-26</em>), proclaiming His death until He comes. The bread is His body broken; the cup is the new covenant in His blood. The Reformed confession holds it to be more than memorial and less than transubstantiation — a real spiritual feeding on the body and blood of Christ <em>through faith</em>, by the Holy Spirit, not by physical change in the elements. <em>"The cup of blessing which we bless, is it not the communion of the blood of Christ?"</em> (<em>1 Corinthians 10:16</em>). It is communion, covenant renewal, and proclamation in a single ordinance.</p>'
    ),
    'magdala': (
        '<p>Magdala was a small fishing town on the western shore of the Sea of Galilee, the hometown of Mary Magdalene — the woman out of whom Christ cast seven demons (<em>Luke 8:2</em>), the loyal disciple who stood at the cross (<em>John 19:25</em>), and the first witness of the resurrection (<em>John 20:11-18</em>). The name appears explicitly in <em>Matthew 15:39</em> KJV (<em>"the coasts of Magdala"</em>), in the parallel to the feeding of the four thousand, though some manuscripts read <em>Magadan</em> or <em>Dalmanutha</em>. Modern archaeology has uncovered a first-century synagogue at the site. Magdala teaches the gospel’s reach: a demoniac of an obscure fishing village becomes the first to say, <em>"I have seen the Lord."</em></p>'
    ),
    'mind-stewardship': (
        '<p>Mind stewardship is the discipline of <em>"casting down imaginations, and every high thing that exalteth itself against the knowledge of God, and bringing into captivity every thought to the obedience of Christ"</em> (<em>2 Corinthians 10:5</em>). It means choosing what to dwell on, refusing speculation, lies, despair, and lust the moment they appear, and filling the mind instead with what is true, honest, just, pure, lovely, of good report (<em>Philippians 4:8</em>). The world floods every Christian mind through screens daily; the Christian counter-floods with Scripture, hymns, theology, and good books. <em>"As he thinketh in his heart, so is he"</em> (<em>Proverbs 23:7</em>). The mind that is not stewarded is the mind that is owned by someone else.</p>'
    ),
    'moral-influence': (
        '<p>The Moral Influence theory (associated with Peter Abelard, 12th c., and many liberal theologians since) teaches that Christ’s death moves us morally — primarily as a demonstration of God’s love that softens our hearts to repent — without addressing divine wrath, broken law, or substitutionary penalty. The cross becomes a powerful example of self-giving love rather than a payment for sin. The Reformed reject it as fatally insufficient. It captures a true element (the cross <em>does</em> move us — <em>"the love of Christ constraineth us"</em>, <em>2 Corinthians 5:14</em>) but loses the indispensable center: penal substitution, propitiation, satisfaction of justice (<em>Romans 3:25-26</em>; <em>1 John 2:2</em>). A cross that only moves us cannot save us; a cross that satisfies justice does both.</p>'
    ),
    'scripture-memory': (
        '<p>Scripture memory is the discipline of internalizing the Word of God verse-by-verse — committing chapters, psalms, and key texts to memory so the Spirit may recall them in the hour of temptation, comfort, witness, or warfare. <em>"Thy word have I hid in mine heart, that I might not sin against thee"</em> (<em>Psalm 119:11</em>). Christ Himself wielded memorized Scripture in the wilderness against the devil (<em>Matthew 4:1-11</em>), quoting Deuteronomy three times. Modern Christians outsource everything to their phones — and lose the sword. A man with a Bible in his hand has the Word nearby; a man with the Word hidden in his heart has it <em>in</em> hand, in the dark, in the trench, where the phone has died. Memorize what you cannot live without.</p>'
    ),
    'tabernacle-furnishings': (
        '<p>The tabernacle contained seven main pieces of furniture, each rich in typological meaning. The bronze altar of burnt offering met every approaching Israelite with sacrificial blood (<em>Exodus 27:1-8</em>). The bronze laver provided priestly washing (<em>30:17-21</em>). Within the Holy Place stood the golden lampstand for light (<em>25:31-40</em>), the table of showbread for the bread of presence (<em>25:23-30</em>), and the altar of incense for prayer (<em>30:1-10</em>). Behind the veil, in the Holy of Holies, rested the ark of the covenant and its mercy seat overshadowed by cherubim (<em>25:10-22</em>) — God’s throne-room on earth. Each piece prefigured Christ: the sacrifice, the laver, the light of the world, the bread of life, the great Intercessor, and the very mercy seat.</p>'
    ),
    'unbeliever': (
        '<p>An unbeliever is one who has not believed the gospel and remains in unbelief — Paul’s technical category for the unconverted. The label is not personal insult but covenant diagnosis. Scripture uses it for clear distinctions: the unbelieving spouse and the believer’s witness within marriage (<em>1 Corinthians 7:12-16</em>); the prohibition of yoking with unbelievers in covenant partnerships (<em>2 Corinthians 6:14-18</em>); the operation of prophecy and tongues for the conviction of unbelievers in the assembly (<em>1 Corinthians 14:22-25</em>). Christians must love unbelievers, witness to them, and pray for their conversion — but must not partner with them in marriage, business covenants that compromise conscience, or worship. The line matters precisely because the gospel saves across it.</p>'
    ),
    'watching': (
        '<p>Watching is the discipline of spiritual alertness — staying awake to the Lord’s return, to the soul’s drift, and to the enemy’s schemes — like a sentry whose eyes do not close on duty. <em>"Watch ye therefore: for ye know not when the master of the house cometh"</em> (<em>Mark 13:35</em>); <em>"Watch and pray, that ye enter not into temptation"</em> (<em>Matthew 26:41</em>); <em>"Be sober, be vigilant; because your adversary the devil... walketh about, seeking whom he may devour"</em> (<em>1 Peter 5:8</em>). The Christian life is a long night-watch. Drowsiness is the enemy of perseverance; complacency is the enemy of growth. Christian men watch over their own souls, their wives, their children, the flock — and look up for the King.</p>'
    ),
    'antichrist-figure': (
        '<p>The Antichrist is the eschatological adversary who opposes Christ and exalts himself as Christ — the climactic embodiment of the spirit that has always opposed God’s anointed. John gives the doctrine its breadth: <em>"as ye have heard that antichrist shall come, even now are there many antichrists"</em> (<em>1 John 2:18; cf. 2:22; 4:3; 2 John 7</em>). There is therefore both a final figure and a present spirit at work in many. Paul calls him <em>"that man of sin... the son of perdition; who opposeth and exalteth himself above all that is called God"</em> (<em>2 Thessalonians 2:3-4</em>). Historic Protestants identified the system in the papacy; futurists expect a final escalation; preterists locate elements in the first-century empire. All agree: Christ destroys him by the brightness of His coming.</p>'
    ),
    'avi-ad': (
        '<p><em>Avi-Ad</em> (אֲבִי־עַד) — "Everlasting Father" — is the messianic title in <em>Isaiah 9:6</em>: <em>"For unto us a child is born... and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace."</em> The title does not confuse the Son with the first Person of the Trinity. Rather, it declares that the incarnate Son is the eternal Father of His people — the everlasting Head, Origin, and Provider of the redeemed family. He <em>fathers</em> His people across all generations without end. The same Lord who in <em>Isaiah 53:10</em> <em>"shall see his seed"</em> is here the <em>Avi-Ad</em>. Every Christian who calls God <em>"Abba"</em> is fathered through this Son.</p>'
    ),
    'baptism-believer': (
        '<p>Believer’s baptism is the public immersion of a repentant confessor in water in the name of the Father, Son, and Holy Spirit. It pictures union with Christ in His death, burial, and resurrection: <em>"buried with him by baptism into death: that like as Christ was raised up from the dead by the glory of the Father, even so we also should walk in newness of life"</em> (<em>Romans 6:3-4</em>). Baptists insist the ordinance is for professing believers only and by immersion. Reformed paedobaptists, while affirming believer-baptism in conversion contexts (e.g., <em>Acts 2:38-41; 8:36-38</em>), also administer covenant baptism to the children of believers as the New-Covenant successor to circumcision (<em>Genesis 17; Colossians 2:11-12; Acts 2:39</em>).</p>'
    ),
    'binah': (
        '<p><em>Binah</em> (בִּינָה) is the Hebrew word for <em>understanding</em> — specifically the insight that distinguishes, separates, and weighs. It is distinct from <em>chokmah</em> (skill, applied wisdom) and <em>daath</em> (knowledge); <em>binah</em> is the discriminating faculty that tells truth from lie, good from evil, wisdom from folly. Solomon prayed for it (<em>1 Kings 3:9, 11</em>); Proverbs commends it (<em>"with all thy getting get understanding"</em>, <em>4:7</em>); the Spirit of the LORD rests upon Messiah as <em>"the spirit of wisdom and understanding"</em> (<em>Isaiah 11:2</em>). In an age of moral confusion, <em>binah</em> is the indispensable Christian faculty: not memorizing facts (<em>daath</em>) or producing output (<em>chokmah</em>), but seeing categories rightly. Pray for it daily.</p>'
    ),
    'day-atonement': (
        '<p>The Day of Atonement (Hebrew <em>Yom Kippur</em>) was the annual high holy day on the tenth of the seventh month — the one day each year when the high priest entered the Holy of Holies with sacrificial blood for the sins of the nation (<em>Leviticus 16</em>). He offered a bull for himself and his house, then a goat for the people; a second goat — the scapegoat — was sent into the wilderness bearing the people’s sins. The book of Hebrews makes the typology explicit: Christ is the better high priest who has entered <em>once for all</em> into the true holy place <em>"by his own blood"</em>, securing eternal redemption (<em>Hebrews 9:7-14, 24-28; 10:1-14</em>). The yearly shadow has been fulfilled in the once-for-all substance.</p>'
    ),
    'eye-discipline': (
        '<p>Eye discipline is the discipline of guarding what the eye looks upon — making a covenant against lust, vanity, and worthlessness — because <em>"the light of the body is the eye"</em> (<em>Matthew 6:22</em>), and what enters there fills the whole man. Job said, <em>"I made a covenant with mine eyes; why then should I think upon a maid?"</em> (<em>Job 31:1</em>). David prayed, <em>"Turn away mine eyes from beholding vanity; and quicken thou me in thy way"</em> (<em>Psalm 119:37</em>). Christ said it is better to pluck out the offending eye than to be cast whole into hell (<em>Matthew 5:29</em>). In a pornographic age, eye discipline is no longer optional discipleship — it is the front line of every Christian man’s sanctification.</p>'
    ),
    'forensic-justification': (
        '<p>Forensic justification is the Reformation doctrine — recovered from <em>Romans 3-5</em> — that justification is a <em>legal verdict</em>, not a moral transformation. God declares the sinner <em>righteous</em> on the basis of Christ’s imputed righteousness, received through faith alone, apart from any inherent change in the sinner at that moment: <em>"to him that worketh not, but believeth on him that justifieth the ungodly, his faith is counted for righteousness"</em> (<em>Romans 4:5</em>; cf. <em>5:1; 8:33-34</em>). The doctrine is forensic ("courtroom"), not transformative — it sits next to sanctification, which <em>is</em> the inner change. Rome confused the two and lost the gospel; Trent anathematized this very doctrine. The Reformers died for the distinction. We must hold it still.</p>'
    ),
    'gehenna-fire': (
        '<p>Gehenna is Christ’s primary term for the place of final, eternal punishment — drawn from the Hebrew <em>Gei-Hinnom</em>, the Valley of Hinnom on the southwest of Jerusalem. The valley was infamous for the child sacrifices of Molech-worship under Ahaz and Manasseh (<em>2 Kings 23:10</em>; <em>Jeremiah 7:31; 19:6</em>) and later became a smouldering refuse dump — fire that did not go out. Jesus used the word twelve times: <em>"the fire that never shall be quenched: where their worm dieth not, and the fire is not quenched"</em> (<em>Mark 9:43-48</em>; cf. <em>Matthew 5:22, 29-30; 10:28; 23:33</em>). It is final, conscious, eternal punishment, fearfully real. Christ alone preached it more often than anyone in Scripture; we cannot soften what He left so plain.</p>'
    ),
    'godly-household': (
        '<p>A godly household is the household ordered under God’s lordship — a Christian father leading family worship, training his children, ruling in love, providing diligently, and loving his wife as Christ loved the church. Paul makes household-leadership the test before church-leadership: <em>"One that ruleth well his own house, having his children in subjection with all gravity; (For if a man know not how to rule his own house, how shall he take care of the church of God?)"</em> (<em>1 Timothy 3:4-5</em>; cf. <em>Titus 1:6</em>). A man whose household is in chaos cannot lead Christ’s household. The household is the original training ground, the smallest church, and the proving lab of every other office a man may hold.</p>'
    ),
    'gratitude-discipline': (
        '<p>Gratitude as discipline is the deliberate, commanded practice of giving thanks in every circumstance — not because all things feel good, but because all things are governed by a good God who works them for the good of His own. <em>"In every thing give thanks: for this is the will of God in Christ Jesus concerning you"</em> (<em>1 Thessalonians 5:18</em>); <em>"Giving thanks always for all things unto God"</em> (<em>Ephesians 5:20</em>); <em>"Be careful for nothing; but in every thing by prayer and supplication with thanksgiving"</em> (<em>Philippians 4:6</em>). Gratitude is not a feeling we wait on; it is an act of will rendered upward. A grumbling heart is a heart that has stopped believing in providence. A grateful man trusts God in the dark.</p>'
    ),
    'hiding-place': (
        '<p>YHWH Himself is the saint’s hiding place from trouble — not a cave, a strategy, or a powerful patron, but the LORD personally. <em>"Thou art my hiding place; thou shalt preserve me from trouble; thou shalt compass me about with songs of deliverance"</em> (<em>Psalm 32:7</em>; cf. <em>119:114; 143:9</em>). Earthly hiding places fail under sufficient pressure: armies fall, friends turn, walls crack, fortunes vanish. YHWH-as-hiding-place is sufficient and sure — the only refuge that holds in the final storm. Corrie ten Boom titled her memoir of God’s preservation amid Nazi terror after this very text. Christian men learn to flee not <em>from</em> trouble but <em>to</em> the LORD, who hides them under the shadow of His wing (<em>Psalm 91:1, 4</em>).</p>'
    ),
    'kicked-against': (
        '<p>"To kick against the pricks" — or, more clearly, against the <em>goad</em> — is Christ’s arresting word to Saul on the Damascus road: <em>"Saul, Saul, why persecutest thou me? it is hard for thee to kick against the pricks"</em> (<em>Acts 9:5</em>; <em>26:14</em>). The image is taken from farming: an ox driven by a pointed goad only injures itself by kicking back. Christ uses the proverb diagnostically — Saul’s persecution of the church is not striking the church; it is striking himself, futilely, against the directing goad of God. The application is universal. Every man who fights the LORD’s providence — His commands, His discipline, His Spirit’s conviction — is kicking against the pricks, doing himself harm. Submit, and be healed.</p>'
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
