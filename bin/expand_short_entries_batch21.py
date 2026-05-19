#!/usr/bin/env python3
"""Batch 21 — expand 25 more thin entries to 90-110 words each.

Targets: NT companions, covenant names, slang reframes, heart-states,
key verbs, offerings, and OT books from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'sosthenes': (
        '<p>Sosthenes was the ruler of the synagogue in Corinth who was beaten before the judgment seat of Gallio after Paul’s Jewish accusers failed to make their case (<em>Acts 18:17</em>). The Greeks dragged him forward and beat him publicly — and <em>"Gallio cared for none of those things."</em> He very likely succeeded Crispus, the previous synagogue ruler who had himself believed (<em>Acts 18:8</em>). Strikingly, a man named Sosthenes appears later as <em>"our brother"</em> co-greeting the Corinthians at the opening of Paul’s first epistle: <em>"Paul... and Sosthenes our brother, unto the church of God which is at Corinth"</em> (<em>1 Corinthians 1:1</em>). If the same man — and tradition holds he is — his beating was the providence that broke him toward Christ.</p>'
    ),
    'unhinged': (
        '<p>"Unhinged" originated as a clinical description of mental instability — a door come loose from its frame. In current slang it has been re-coded as a <em>positive</em> aesthetic: <em>"unhinged behavior,"</em> <em>"unhinged tweet,"</em> <em>"unhinged energy."</em> The fashion celebrates chaos as authenticity and treats restraint as fakeness, performance, or oppression. Scripture rebukes the inversion. The biblical category is <em>sōphrosynē</em> — sound-mindedness, soberness, self-mastery — and it is a virtue commanded of every Christian (<em>Titus 2:2-6</em>; <em>1 Timothy 3:2</em>; <em>2 Timothy 1:7</em>). The man freed from a demon at Gerasene was found <em>"sitting, and clothed, and in his right mind"</em> (<em>Mark 5:15</em>). Sanity is the fruit of the Spirit, not the residue of repression. Be hinged.</p>'
    ),
    'walk': (
        '<p>To <em>walk</em>, in Scripture, is the dominant metaphor for the conduct of life — the continuous pattern of behavior, choices, and direction. <em>"To walk"</em> is to live one’s daily way. <em>"Enoch walked with God: and he was not; for God took him"</em> (<em>Genesis 5:24</em>); Israel is to <em>"walk in his ways"</em> (<em>Deuteronomy 8:6</em>). The New Testament builds the metaphor into ethics: <em>"walk in the Spirit, and ye shall not fulfil the lust of the flesh"</em> (<em>Galatians 5:16</em>); <em>"walk worthy of the vocation wherewith ye are called"</em> (<em>Ephesians 4:1</em>); <em>"walk in love"</em> (<em>Ephesians 5:2</em>); <em>"walk in the light, as he is in the light"</em> (<em>1 John 1:7</em>). The Christian life is not a stand or a sit — it is a walk, step by step.</p>'
    ),
    'wolf': (
        '<p>The wolf, in Scripture, is the predatory beast and the recurring image of false prophets, heretical teachers, and abusive shepherds who scatter and devour the flock of God. Christ warns: <em>"Beware of false prophets, which come to you in sheep’s clothing, but inwardly they are ravening wolves"</em> (<em>Matthew 7:15</em>). Paul tells the Ephesian elders: <em>"after my departing shall grievous wolves enter in among you, not sparing the flock"</em> (<em>Acts 20:29</em>). The hireling flees when the wolf comes (<em>John 10:12</em>); the good shepherd lays down His life for the sheep. Wolves are not always outside the church — Paul says they come <em>in among</em> the flock. Faithful elders are therefore wolf-hunters first, and feeders second. A church that cannot bite cannot protect.</p>'
    ),
    'yhwh-rapha': (
        '<p><em>YHWH-Rapha</em> (יְהוָה רֹפְאֶךָ) — "the LORD that healeth thee" — is the covenant self-revelation God gave Israel at Marah, after sweetening the bitter waters with a tree cast in: <em>"If thou wilt diligently hearken to the voice of the LORD thy God... I will put none of these diseases upon thee, which I have brought upon the Egyptians: for I am the LORD that healeth thee"</em> (<em>Exodus 15:26</em>). The Hebrew <em>rapha</em> covers physical healing, spiritual healing, and the binding-up of the broken-hearted. God is the comprehensive Healer: of Naaman’s leprosy (<em>2 Kings 5</em>), of David’s soul (<em>Psalm 41:4; 147:3</em>), of the nations’ wounds (<em>Isaiah 53:5</em>). All medicine, all comfort, all resurrection terminate in this name.</p>'
    ),
    'abraham-call': (
        '<p>The Call of Abraham is God’s summons of Abram, around 2000 BC, out of Ur of the Chaldees to a land He would show him (<em>Genesis 12:1-3</em>): <em>"Get thee out of thy country, and from thy kindred, and from thy father’s house, unto a land that I will shew thee."</em> The promise is threefold: a great <em>nation</em> (seed), a <em>land</em> to inherit, and worldwide <em>blessing</em> — <em>"in thee shall all families of the earth be blessed."</em> The call inaugurates the Abrahamic covenant, formalized in <em>Genesis 15</em> and <em>17</em>, and traces the line through which Messiah would come. Paul makes the application universal: <em>"They which are of faith, the same are the children of Abraham"</em> (<em>Galatians 3:7</em>). Every Christian is called out, just as Abraham was.</p>'
    ),
    'ashes': (
        '<p>Ashes are the residue of what has burned — Scripture’s emblem of repentance, mourning, and consumed flesh yielded to God. To sit in sackcloth and ashes is to confess guilt and beg mercy: Job repented <em>"in dust and ashes"</em> (<em>Job 42:6</em>); Daniel sought the LORD <em>"with fasting, and sackcloth, and ashes"</em> (<em>Daniel 9:3</em>); Nineveh’s king sat <em>"in ashes"</em> at Jonah’s preaching (<em>Jonah 3:6</em>). Abraham acknowledged he was <em>"but dust and ashes"</em> (<em>Genesis 18:27</em>). Yet ashes are not the final word: <em>"to appoint unto them that mourn in Zion, to give unto them beauty for ashes, the oil of joy for mourning, the garment of praise for the spirit of heaviness"</em> (<em>Isaiah 61:3</em>). The gospel exchanges ashes for beauty.</p>'
    ),
    'broken-heart': (
        '<p>A broken heart is the contrite, shattered heart that grieves over its own sin, casts off self-righteousness, and clings only to mercy. God Himself names it as the sacrifice He requires: <em>"The sacrifices of God are a broken spirit: a broken and a contrite heart, O God, thou wilt not despise"</em> (<em>Psalm 51:17</em>; cf. <em>34:18</em>: <em>"The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit"</em>). The LORD scorns the bull and the goat of the proud worshiper, but draws near to the broken-hearted as His chosen sacrifice. Christian men must learn to come to God broken — not pretending strength, not bargaining merit, not negotiating terms — and find Him close exactly there.</p>'
    ),
    'delight-in-yhwh': (
        '<p>Delight in the LORD is the disposition of soul-satisfaction in God Himself. <em>"Delight thyself also in the LORD; and he shall give thee the desires of thine heart"</em> (<em>Psalm 37:4</em>). The order matters and is often misread: <em>delight first</em>, then desires fulfilled. The promise is not that God hands over whatever the natural heart wants — but that the delighting heart’s desires conform to His own, and those He delights to grant. Job said, <em>"Thou shalt have thy delight in the Almighty, and shalt lift up thy face unto God"</em> (<em>Job 22:26</em>). Isaiah said, <em>"Delight thyself in the LORD; and I will cause thee to ride upon the high places of the earth"</em> (<em>Isaiah 58:14</em>). Christian joy terminates on God, not on His gifts.</p>'
    ),
    'deny': (
        '<p>To <em>deny</em> is to refuse, repudiate, or disown. Scripture sets two opposite movements side by side. The saint denies <em>self</em> (a virtue): <em>"If any man will come after me, let him deny himself, and take up his cross, and follow me"</em> (<em>Mark 8:34</em>). And he refuses to deny <em>Christ</em> (the line of fidelity): <em>"Whosoever therefore shall confess me before men, him will I confess also before my Father which is in heaven. But whosoever shall deny me before men, him will I also deny before my Father"</em> (<em>Matthew 10:32-33</em>; <em>2 Timothy 2:12</em>). Peter denied Christ once with cursing — and wept bitterly. Denial cuts both ways; the question is always which side. Deny self; never deny the Master.</p>'
    ),
    'empathy-biblical': (
        '<p>Biblical empathy is the capacity to enter into another’s experience — modeled supremely by Christ, who <em>"himself took our infirmities, and bare our sicknesses"</em> (<em>Matthew 8:17</em>; <em>Isaiah 53:4</em>) and who <em>"was in all points tempted like as we are, yet without sin"</em> (<em>Hebrews 4:15</em>). Paul urges <em>"weep with them that weep"</em> (<em>Romans 12:15</em>); Peter commends <em>"having compassion one of another"</em> (<em>1 Peter 3:8</em>). Yet empathy is not the master virtue. Recent theological work (Joe Rigney, others) rightly warns against <em>untethered empathy</em> — empathy that bows to the feelings of another at the expense of truth. The biblical version is a servant of love and truth, not their replacement. Feel <em>with</em>; never lie <em>to</em>.</p>'
    ),
    'faith-victory': (
        '<p>"Victory faith" is the apostle John’s phrase for the faith that overcomes the world. <em>"For whatsoever is born of God overcometh the world: and this is the victory that overcometh the world, even our faith"</em> (<em>1 John 5:4</em>). The victory does not belong to faith as a virtue in itself — as if mere believing produced its own conquest. It belongs to faith because faith lays hold on Christ, who has already overcome (<em>John 16:33</em>: <em>"be of good cheer; I have overcome the world"</em>). Faith does not win the war; faith joins the winner. The Christian therefore fights from victory, not for it — refusing both presumption and despair, casting himself again on the Christ in whom every battle has already been decided.</p>'
    ),
    'fervency': (
        '<p>Fervency is the Spirit-kindled heat of the soul in love, prayer, and service — not occasional excitement but sustained warmth. Apollos came to Ephesus <em>"fervent in the spirit"</em> (<em>Acts 18:25</em>); James writes, <em>"The effectual fervent prayer of a righteous man availeth much"</em> and offers Elijah as proof (<em>James 5:16-18</em>); Peter commands, <em>"have fervent charity among yourselves"</em> (<em>1 Peter 4:8</em>); Paul, <em>"fervent in spirit; serving the Lord"</em> (<em>Romans 12:11</em>). The opposite is the lukewarmness of Laodicea (<em>Revelation 3:15-16</em>) that Christ vomits out. Christian men fight against coldness by drawing near to the fire — Scripture, prayer, fellowship — and refusing every comfortable distance that creeps in over time. The flame requires fuel.</p>'
    ),
    'gathering-place': (
        '<p>A gathering place is the appointed location where God’s people convene for worship — tabernacle, temple, synagogue, house-church, sanctuary. Scripture holds an unbroken line: the LORD does not save isolated individuals only — He gathers a people, and He gives them places. The tabernacle is the wilderness gathering place; Solomon’s temple is its settled fulfillment; the synagogue carries worship through exile; the New Testament <em>ekklēsia</em> is the called-out assembly of the new covenant. <em>"Not forsaking the assembling of ourselves together, as the manner of some is"</em> (<em>Hebrews 10:25</em>) — the imperative still stands. Christianity is not a private spirituality but a covenant people convened weekly under Word and sacrament. Stream the service if you must; never substitute the screen for the gathering.</p>'
    ),
    'heart-undivided': (
        '<p>The undivided heart is the heart God Himself unites — that fears His name without rival, walks in His truth without compromise, and is wholly His. It is David’s prayer in <em>Psalm 86:11</em>: <em>"Teach me thy way, O LORD; I will walk in thy truth: unite my heart to fear thy name."</em> The opposite is the divided heart of Hosea: <em>"Their heart is divided; now shall they be found faulty"</em> (<em>Hosea 10:2</em>) — half toward the LORD and half toward Baal. <em>James 1:8</em> calls the double-minded man <em>"unstable in all his ways."</em> The undivided heart is therefore not natural — it is a gift to be asked, a unity God grants the willing soul. Christian men must pray daily for it.</p>'
    ),
    'mnason': (
        '<p>Mnason was an early disciple from Cyprus with whom Paul lodged on his final journey to Jerusalem (<em>Acts 21:16</em>). The Greek phrase <em>"an old disciple"</em> (<em>archaiō mathētē</em>) does not mean elderly in years but <em>"a disciple from the beginning"</em> — likely a convert from Pentecost or the early Cyrenian-Cypriot mission. He was a member of the Caesarean church community and opened his home to Paul and his company as they made their way to Jerusalem with the Gentile collection. Mnason is a small but luminous Scripture cameo: the early-days disciple who never made it into the apostle lists, never wrote a letter, but whose hospitality served the apostle of the Gentiles on the road to his arrest. The kingdom is built on such men.</p>'
    ),
    'olah-offering': (
        '<p>The <em>olah</em> (עוֹלָה, "that which ascends") is the Mosaic burnt offering, prescribed in <em>Leviticus 1</em> — the sacrifice entirely consumed by fire on the bronze altar, ascending as smoke to YHWH. It was the most fundamental Levitical sacrifice and the only one that was <em>wholly</em> the LORD’s portion: nothing was eaten, nothing retained, all consumed. It symbolized total dedication. The continual <em>tamid</em> burnt-offering (a lamb morning and evening, <em>Numbers 28:3-4</em>) ran perpetually in Israel’s tabernacle and temple, so that smoke ascended from the altar without break. Christ is the supreme <em>olah</em>: <em>"who through the eternal Spirit offered himself without spot to God"</em> (<em>Hebrews 9:14</em>) — wholly consumed, wholly ascending, wholly accepted. The smoke of His offering rises still.</p>'
    ),
    'paths-righteousness': (
        '<p>The "paths of righteousness" are the well-worn moral and spiritual tracks along which the Shepherd leads His sheep in <em>Psalm 23:3</em>: <em>"He restoreth my soul: he leadeth me in the paths of righteousness for his name’s sake."</em> The image is not of pioneering new ways but of following righteousness-paths long established by the LORD — the trails the saints have walked from Abel to the present moment. The clause <em>"for his name’s sake"</em> is the key: the leading is more about <em>His</em> reputation than the sheep’s deserving. He will not bring His name to dishonor by losing one of His own. The Christian who feels lost on these paths is not as lost as he feels; the Shepherd is still ahead, still leading.</p>'
    ),
    'save': (
        '<p>To <em>save</em>, biblically, is to rescue, deliver, preserve — used both of physical deliverance (Israel from Pharaoh, Peter from drowning, Paul from shipwreck) and of the climactic salvation of the soul through Christ. The Hebrew root <em>yashaʿ</em> ("to save") is the very root of the names <em>Joshua</em> and <em>Jesus</em> — both mean <em>"YHWH saves."</em> The angel told Joseph: <em>"thou shalt call his name JESUS: for he shall save his people from their sins"</em> (<em>Matthew 1:21</em>). Salvation is wholly God’s work: <em>"by grace are ye saved through faith; and that not of yourselves: it is the gift of God"</em> (<em>Ephesians 2:8</em>). The Christian does not save himself; he is saved. The verb is passive on our side, active on God’s.</p>'
    ),
    'song-of-solomon': (
        '<p>The Song of Solomon (also called the Song of Songs or Canticles) is a poetic celebration of covenant love between a bridegroom and his bride — eight short chapters of dialogue, dream, and longing. Traditionally read by the Jewish synagogue as an allegory of YHWH and Israel, and by the Christian church as an allegory of Christ and His church (a reading already implicit in <em>Ephesians 5:32</em>), the Song is also the Bible’s great sanctification of bodily love within the covenant of marriage. It refuses both the gnostic shame of the body and the pagan worship of the body — it places desire under covenant, and covenant under God. <em>"Many waters cannot quench love, neither can the floods drown it"</em> (<em>Song 8:7</em>).</p>'
    ),
    'threshold': (
        '<p>The threshold is the stone or beam at the bottom of a doorway — the boundary between outside and inside, sacred and profane, household and street. Scripture treats it as a place to be guarded, honored, and crossed deliberately. The priests of Dagon would not step on the threshold of their temple after the idol fell broken across it (<em>1 Samuel 5:5</em>); the LORD’s glory paused at the threshold of the temple before departing in Ezekiel’s vision (<em>Ezekiel 10:18</em>); the Hebrew slave who refused freedom was brought to the doorpost for the ear-piercing ceremony (<em>Exodus 21:6</em>). Thresholds matter. The Christian household has thresholds: what comes in, who comes in, by what permission. Guard them. <em>"As for me and my house, we will serve the LORD"</em> (<em>Joshua 24:15</em>).</p>'
    ),
    'year-of-jubilee': (
        '<p>The Year of Jubilee was the fiftieth year of Israel’s calendar — every seventh sabbath-year, the year after the seven-times-seventh — in which slaves were freed, debts were forgiven, and ancestral lands were returned to their original families (<em>Leviticus 25:8-55</em>). The trumpet of jubilee was sounded on the Day of Atonement, and liberty was proclaimed throughout the land. The Jubilee enshrined two truths the modern economic order has forgotten: God owns the land — <em>"The land shall not be sold for ever: for the land is mine"</em> (<em>v. 23</em>) — and God owns the people. Christ opened His public ministry by reading <em>Isaiah 61</em> in Nazareth — the great Jubilee text — declaring: <em>"This day is this scripture fulfilled in your ears"</em> (<em>Luke 4:18-21</em>).</p>'
    ),
    'yielding-spirit': (
        '<p>A yielding spirit is the settled inner posture of giving way to God — not breaking, but bending; not surrendering ground to evil, but surrendering self-will to the LORD. Ecclesiastes commends it: <em>"yielding pacifieth great offences"</em> (<em>Ecclesiastes 10:4</em>). Romans names it the daily logic of the Christian life: <em>"I beseech you therefore, brethren, by the mercies of God, that ye present your bodies a living sacrifice, holy, acceptable unto God, which is your reasonable service"</em> (<em>Romans 12:1</em>; cf. <em>6:13, 19</em>). The Christian man is not weak — he is yielded. He has surrendered the throne of his own life to Christ, and he refuses to retake it. That difference is the difference between a Christian and an ungoverned soul.</p>'
    ),
    'aristarchus': (
        '<p>Aristarchus was a Thessalonian Macedonian believer who shared so much of Paul’s ministry that he appears at three major junctures. He was seized in the Ephesian theatre during the silversmiths’ riot over Artemis (<em>Acts 19:29</em>); he accompanied Paul on the long, perilous voyage to Rome (<em>Acts 27:2</em>); and from Rome Paul calls him <em>"my fellowprisoner"</em> in the close of Colossians (<em>Colossians 4:10</em>; cf. <em>Philemon 24</em>). Tradition holds he was martyred under Nero. Aristarchus is the model of long-suffering companionship in gospel ministry — the man who did not get a book named after him but stood beside Paul in riot, ship, and prison. Every faithful pastor has, or longs for, an Aristarchus. Every Christian man should aspire to be one.</p>'
    ),
    'berea': (
        '<p>Berea was a Macedonian city about fifty miles southwest of Thessalonica where Paul and Silas preached after fleeing the riot at Thessalonica (<em>Acts 17:10-15</em>). The local Jews are commended in one of Luke’s most-quoted notes: <em>"These were more noble than those in Thessalonica, in that they received the word with all readiness of mind, and searched the scriptures daily, whether those things were so. Therefore many of them believed; also of honourable women which were Greeks, and of men, not a few."</em> The Bereans modeled gospel reception at its best — eager, scripturally tested, leading to faith. <em>"Berean"</em> has since become shorthand for sound, Scripture-checking biblical engagement. Christian men should be Bereans. Trust nothing — not even a beloved teacher — without searching the Word.</p>'
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
