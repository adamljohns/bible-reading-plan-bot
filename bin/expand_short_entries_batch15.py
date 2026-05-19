#!/usr/bin/env python3
"""Batch 15 — expand 25 more thin entries to 90-110 words each.

Targets: ecclesial keys, soteriology, geography, atonement theory,
disciplines, and KJV warrior vocabulary from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'keys-kingdom': (
        '<p>The Keys of the Kingdom are the symbol of ecclesial authority Christ gave first to Peter and then to the whole apostolic band: <em>"whatsoever thou shalt bind on earth shall be bound in heaven"</em> (<em>Matthew 16:19</em>; cf. <em>18:18</em>; <em>John 20:23</em>). The keys are not magical; they are the church’s authority to declare what God’s Word binds and looses — to preach the gospel (opening the kingdom to the penitent), to administer the sacraments, and to exercise discipline (shutting the kingdom against the impenitent until repentance). Rome wrongly hoarded them in the papal office; Protestants rightly recognize they belong to every faithful local church under Christ. The keys are wielded in council, by Scripture, with fear.</p>'
    ),
    'listening': (
        '<p>Listening is the discipline of slow, attentive hearing — of God in His Word, and of others in their need — <em>before</em> forming a reply. <em>"Wherefore, my beloved brethren, let every man be swift to hear, slow to speak, slow to wrath"</em> (<em>James 1:19</em>). Proverbs lays down the verdict on its opposite: <em>"He that answereth a matter before he heareth it, it is folly and shame unto him"</em> (<em>Proverbs 18:13</em>). Christian listening is active and pastoral, not passive — it asks, repeats back, and waits for the Spirit to clarify. Husbands who do not listen to their wives, pastors who do not listen to their flock, and fathers who do not listen to their sons all fail the same duty.</p>'
    ),
    'malta': (
        '<p>Malta is the small Mediterranean island (south of Sicily) where Paul was shipwrecked en route to Rome (<em>Acts 28:1-10</em>). The islanders, called <em>"barbarians"</em> in the KJV because they spoke neither Greek nor Latin, <em>"shewed us no little kindness"</em>, kindling a fire against the cold and rain. When Paul shook off the viper without harm, they took him for a god. He stayed three months, healing Publius the chief man’s father and many others, and was sent on his way honored with many gifts. Malta marks the providence of God in storm: shipwreck became gospel-opportunity, and the apostle’s appointed witness in Rome was not aborted by weather, viper, or sea.</p>'
    ),
    'money': (
        '<p>Money is the medium of exchange — morally neutral as a tool, but deeply tested in the heart’s love, use, and worship of it. <em>"The love of money is the root of all evil"</em> (<em>1 Timothy 6:10</em>); not money itself, but love of it. Christ commands wise stewardship (<em>Luke 16:9-13</em>) and warns of rivalry: <em>"Ye cannot serve God and mammon"</em> (<em>Matthew 6:24</em>). Scripture upholds honest gain, hard work, prudent saving, generous giving, tithing, providing for one’s house (<em>1 Timothy 5:8</em>), and the right of property. It condemns covetousness, usury against brothers in need, and the prosperity gospel that makes money proof of God’s favor. A Christian man earns much, saves wisely, gives generously, and never bows.</p>'
    ),
    'mystical-union': (
        '<p>Mystical union is the real, vital, spiritual joining of every believer to Christ by the Spirit — <em>"He in us, we in Him"</em> — the ground of every salvation benefit we receive. Jesus prayed, <em>"I in them, and thou in me, that they may be made perfect in one"</em> (<em>John 17:23</em>); Paul calls marriage <em>"a great mystery... concerning Christ and the church"</em> (<em>Ephesians 5:32</em>); Christ in you is <em>"the hope of glory"</em> (<em>Colossians 1:27</em>). Justification, sanctification, adoption, and glorification all flow from this union — not as separate transactions, but as the gifts of the Bridegroom to His bride. The Christian does not earn benefits from Christ; he <em>has</em> Christ, and in Him every benefit.</p>'
    ),
    'older-women': (
        '<p>"Older women" is the category Paul honors and commissions in <em>Titus 2:3-4</em>: <em>"The aged women likewise, that they be in behaviour as becometh holiness, not false accusers, not given to much wine, teachers of good things; that they may teach the young women..."</em> They are also honored as <em>"mothers"</em> in the household of faith (<em>1 Timothy 5:2</em>). Age, godliness, and seasoning qualify them to teach — not from a pulpit, but woman-to-woman, marriage-to-marriage, mother-to-mother. The biblical church needs grandmothers who are theologically literate and unafraid to instruct their daughters and granddaughters in the unfashionable duties of biblical womanhood. Feminism robbed two generations of this office; recovering it is one of the church’s most urgent works.</p>'
    ),
    'presumptuous': (
        '<p>Presumptuous, in Scripture, names the high-handed sin — acting boldly without warrant, against known commandment, in defiance of God. The Mosaic law distinguishes presumptuous sin sharply from sins of weakness or ignorance: <em>"But the soul that doeth ought presumptuously... that soul shall be cut off"</em> (<em>Numbers 15:30-31</em>). David’s prayer makes the doctrine personal: <em>"Keep back thy servant also from presumptuous sins; let them not have dominion over me"</em> (<em>Psalm 19:13</em>). Presumption is dangerous because it has already overruled conscience — it takes God’s mercy for license. Christian men must learn the difference between weakness (stumbling) and presumption (charging forward against the LORD), and beg God daily for the latter restraint.</p>'
    ),
    'rod-and-staff': (
        '<p>The rod and staff are the shepherd’s two tools in <em>Psalm 23:4</em>: <em>"thy rod and thy staff they comfort me."</em> The rod (Hebrew <em>shevet</em>) is the short, heavy club used to defend the flock against predators and to discipline straying sheep — the same word used of the king’s scepter and the father’s rod of correction (<em>Proverbs 13:24</em>). The staff (<em>mishʿenet</em>) is the long crook used to support, lift fallen sheep from pits, and gently turn them. Together they comfort because both express the shepherd’s strength on the sheep’s behalf — defending and directing. Christ shepherds His people with both: discipline and tenderness, never one without the other. So must fathers, husbands, and pastors.</p>'
    ),
    'send': (
        '<p>To <em>send</em> is to dispatch with authority and purpose. The biblical theology of mission is built on it: the Father sends the Son into the world (<em>John 3:17; 17:18</em>); the Son sends the Spirit (<em>John 15:26; 16:7</em>); the Father and Son together send the apostles (<em>John 20:21</em>: <em>"as my Father hath sent me, even so send I you"</em>). Greek <em>apostellō</em> ("send out") is the root of <em>apostle</em>. Sending implies authority behind the messenger, mission ahead of him, and accountability on return. The local church is the New Testament’s sending body (<em>Acts 13:1-3</em>): hands laid on, Spirit-led, men commissioned. Every Christian is sent somewhere, even if it is his own household.</p>'
    ),
    'service': (
        '<p>Service is the discipline of voluntarily lowering oneself to meet the needs of others, modeled supremely on Christ: <em>"the Son of man came not to be ministered unto, but to minister, and to give his life a ransom for many"</em> (<em>Mark 10:45</em>). It is not servility, not codependence, not earning love — it is the strong stooping in love because the King has stooped first. Paul calls himself the <em>"servant"</em> (<em>doulos</em>) of Christ (<em>Romans 1:1</em>) — a title of honor, not shame. In the household this means the husband serving his wife by leading her, the wife serving her husband by submitting, the parents serving the children by discipling them. Service is masculine and feminine alike; the kingdom is built on it.</p>'
    ),
    'single-eye': (
        '<p>The single eye is Jesus’ image in <em>Matthew 6:22</em> for the heart whose loyalty is undivided: <em>"The light of the body is the eye: if therefore thine eye be single, thy whole body shall be full of light."</em> The Greek <em>haplous</em> means "simple, single, undivided" — focused on one thing. The single-eyed man sees clearly because he is not double-minded. The context is decisive: it sits between treasures-in-heaven (<em>6:19-21</em>) and the impossibility of serving God and mammon (<em>6:24</em>). The single eye is the practical opposite of the divided heart. Christian men recover it by repenting of secondary loyalties — career, comfort, reputation — and fixing the eye again on Christ.</p>'
    ),
    'trumpets-of-revelation': (
        '<p>The seven trumpets of Revelation 8-11 are the second great cycle of judgments unsealed by the Lamb. After the seventh seal opens, seven angels are given seven trumpets, and at each blast a judgment falls — hail and fire on a third of the earth (8:7), a mountain of fire on a third of the sea (8:8), the star Wormwood on a third of the rivers (8:10-11), darkening of a third of the luminaries (8:12). The last three trumpets are <em>"woes"</em>: demonic locusts from the abyss (ch. 9), demonic horsemen (9:13-21), and the final trumpet of consummation announcing <em>"the kingdoms of this world are become the kingdoms of our Lord, and of his Christ"</em> (<em>Revelation 11:15</em>). Judgments escalate; the Lamb reigns.</p>'
    ),
    'two-ways': (
        '<p>The Two Ways is the wisdom-tradition image of two paths laid before every life: the way of righteousness leading to life, and the way of wickedness leading to destruction. <em>Psalm 1</em> opens the Psalter with it; <em>Proverbs 4:18-19</em> contrasts the shining dawn of the just with the deep darkness of the wicked. Jesus seals it: <em>"Wide is the gate, and broad is the way, that leadeth to destruction, and many there be which go in thereat: because strait is the gate, and narrow is the way, which leadeth unto life, and few there be that find it"</em> (<em>Matthew 7:13-14</em>). The earliest church manual, the <em>Didache</em>, opens with the same words. There is no third way. Choose.</p>'
    ),
    'usury': (
        '<p>Usury, in biblical usage, is the lending of money at interest to a brother in need — explicitly forbidden in the Mosaic law (<em>Exodus 22:25</em>; <em>Leviticus 25:36-37</em>; <em>Deuteronomy 23:19-20</em>). The KJV translates <em>neshek</em> ("bite") as usury; the modern English word has narrowed to mean excessive interest, but Scripture’s concern is broader. Israel could lend at interest to a foreigner (commercial), but not exploit a brother’s poverty. The prophets fold usury into their list of national sins (<em>Ezekiel 18:8, 13; 22:12</em>); the righteous man <em>"putteth not out his money to usury"</em> (<em>Psalm 15:5</em>). The principle stands: covenant brotherhood forbids profiting from a brother’s hardship. Charity, not interest, answers his need.</p>'
    ),
    'valiant': (
        '<p>Valiant — KJV for "brave, courageous, mighty in battle" — is one of the great masculine words of Scripture. Saul gathered <em>"any strong man, or any valiant man"</em> (<em>1 Samuel 14:52</em>); David’s mighty men in <em>2 Samuel 23</em> performed valiant deeds, killing lions in pits and breaking through Philistine lines for a drink of water. <em>Hebrews 11:34</em> commends the saints who <em>"out of weakness were made strong, waxed valiant in fight, turned to flight the armies of the aliens."</em> Valiant is not bluster — it is courage wedded to skill, anchored in faith. The age that has lost the word has lost the virtue, and the church which cannot say it of her men is in trouble. <em>"Be of good courage, and let us play the men"</em> (<em>2 Samuel 10:12</em>).</p>'
    ),
    'conscience-clear': (
        '<p>A clear conscience is the state of integrity Paul names repeatedly: <em>"a conscience void of offence toward God, and toward men"</em> (<em>Acts 24:16</em>). It is not the false peace of the seared conscience (<em>1 Timothy 4:2</em>) nor the merit of self-righteousness — it is the settled inner witness that one is walking honestly under God, with nothing hidden, nothing owed, nothing unconfessed. Paul prizes it: <em>"the end of the commandment is charity out of a pure heart, and of a good conscience, and of faith unfeigned"</em> (<em>1 Timothy 1:5</em>; cf. <em>3:9</em>; <em>2 Timothy 1:3</em>; <em>1 Peter 3:16</em>). Christian men keep clear consciences by walking in the light — confession quick, restitution made, secret sins killed. Without it, no man can lead.</p>'
    ),
    'cyrene': (
        '<p>Cyrene was a major North African city (in modern Libya) with a substantial Jewish population — the home of Simon, who was compelled by the Romans to carry Jesus’ cross to Golgotha (<em>Mark 15:21</em>; <em>Matthew 27:32</em>; <em>Luke 23:26</em>). Simon’s sons, Alexander and Rufus, are named in Mark’s Gospel, suggesting they were known to the early church. Cyrenian Jews were also among the first to step across the gospel’s ethnic line, preaching to Greeks at Antioch in <em>Acts 11:20</em> — a critical hinge in the church’s mission. <em>"Lucius of Cyrene"</em> was a teacher at the Antiochene church (<em>Acts 13:1</em>). Cyrene thus appears in Scripture both at the cross and at the breakthrough of the gospel to the nations.</p>'
    ),
    'day-of-lord-nt': (
        '<p>The Day of the Lord in the New Testament is the eschatological day of Christ’s return in glory, bringing final judgment on the wicked and final salvation to the church. It draws on the OT prophets (<em>Joel 2; Amos 5; Zephaniah 1</em>) and is identified explicitly with the Second Coming of Jesus: <em>"the day of the Lord so cometh as a thief in the night"</em> (<em>1 Thessalonians 5:2</em>); <em>"the day of the Lord will come... in the which the heavens shall pass away with a great noise"</em> (<em>2 Peter 3:10</em>; cf. <em>1 Corinthians 1:8; 5:5</em>). It is sudden, certain, and unmistakable — every eye shall see Him. The Christian lives in light of that day: sober, hopeful, watching.</p>'
    ),
    'definitive-sanctification': (
        '<p>Definitive sanctification is the decisive, one-time break with sin’s dominion that takes place at conversion — the believer is set apart in Christ, transferred from death to life, no longer a slave of sin (<em>Romans 6:1-14</em>; <em>1 Corinthians 6:11</em>). It is distinguished from <em>progressive</em> sanctification (the lifelong growth in holiness) and is the foundation on which that growth rests. John Murray recovered the doctrine: in Christ the believer has <em>already</em> died to sin (<em>Romans 6:2, 11</em>) — not aspires to die, has died. Progressive sanctification is therefore not earning a status but working out what is already true. The Christian fights from victory, not for it. Recognizing definitive sanctification settles the war.</p>'
    ),
    'ephesus-city': (
        '<p>Ephesus was the leading commercial and religious city of Roman Asia, on the western coast of modern Turkey — home of the great temple of Artemis (Diana of the Ephesians), one of the Seven Wonders of the ancient world. Paul ministered there for three years (<em>Acts 19; 20:31</em>), preaching daily in the hall of Tyrannus, performing extraordinary miracles, and seeing the cult of Artemis so threatened that the silversmiths rioted (<em>Acts 19:23-41</em>). The city later received Paul’s great cosmic-Christology letter (the Epistle to the Ephesians), and is the first of the seven churches addressed in <em>Revelation 2:1-7</em>, commended for orthodoxy but rebuked for having <em>"left thy first love."</em> The lampstand of Ephesus has long since been removed.</p>'
    ),
    'euangelion': (
        '<p><em>Euangelion</em> (Greek εὐαγγέλιον) — translated <em>"gospel"</em> in our New Testaments — literally means <em>"good news."</em> In Greco-Roman imperial usage, the word announced tidings of military victory or the accession of a new emperor; an inscription at Priene calls the birth of Augustus <em>"good news"</em>. The New Testament seizes the political word and turns it on the empire: the true <em>euangelion</em> is the announcement of Christ’s saving accomplishment — His incarnation, death, resurrection, and reign as the true King of kings. <em>"I am not ashamed of the gospel of Christ: for it is the power of God unto salvation to every one that believeth"</em> (<em>Romans 1:16</em>). The word is itself a claim of rival sovereignty. Caesar is not Lord; Christ is.</p>'
    ),
    'governmental-theory': (
        '<p>The Governmental Theory of the atonement (associated with Hugo Grotius, 1583-1645) teaches that Christ’s death was a public demonstration of God’s hatred of sin and the seriousness of His moral government — but not a substitutionary penalty actually paid for individual sinners. God, the moral Governor, forgave sin while displaying its costliness through Christ’s suffering. The Reformed reject the theory as a half-truth: it preserves God’s justice in appearance but loses the heart of penal substitution — that Christ <em>bore</em> the actual wrath due our sin and <em>satisfied</em> the law on our behalf (<em>Isaiah 53:5-6, 10</em>; <em>2 Corinthians 5:21</em>; <em>Galatians 3:13</em>). Demonstration is not satisfaction; theatre is not transaction. The cross was both — but mostly the latter.</p>'
    ),
    'great-high-priest': (
        '<p>The Great High Priest is Jesus Christ, who <em>"is passed into the heavens"</em> and <em>"ever liveth to make intercession"</em> for His people (<em>Hebrews 4:14; 7:25</em>). He is the fulfillment and termination of the Aaronic order — sinless, eternal, holy, harmless, undefiled, separate from sinners (<em>Hebrews 7:26</em>) — and the priest forever after the order of Melchizedek by divine oath (<em>Hebrews 7:21</em>). Where Aaron offered repeated sacrifices for himself and the people, Christ offered Himself once for all (<em>Hebrews 9:12, 26-28</em>). Where Aaron’s priesthood ended at death, Christ’s continues forever in resurrection life. Every Christian who comes to the Father comes through this priest — and may come with boldness, because the throne is now a throne of grace.</p>'
    ),
    'guilt-true': (
        '<p>True guilt is the objective moral state of having broken God’s law — distinguished from <em>feelings</em> of guilt (which may be true or false). A man can feel guilty over what God has not forbidden, and he can feel innocent over what God has condemned; feelings are not the test. Paul lays the diagnosis in <em>Romans 3:19</em>: <em>"that every mouth may be stopped, and all the world may become guilty before God."</em> The gospel responds to <em>true</em> guilt with <em>real</em> forgiveness: <em>"If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness"</em> (<em>1 John 1:9</em>). False guilt requires education from Scripture; true guilt requires the blood of Christ.</p>'
    ),
    'heart-hard': (
        '<p>A hard heart is one calloused by repeated sin and unwilling to repent — deaf to God’s voice, blind to His warnings, settled in unbelief. The figure runs the whole Bible: Pharaoh’s heart hardened against Moses (<em>Exodus 7-14</em>); Israel’s heart hardened in the wilderness (<em>Psalm 95:8</em>); the Pharisees’ hearts hardened against Christ (<em>Mark 3:5</em>). <em>Hebrews 3-4</em> repeatedly warns the New-Covenant church: <em>"To day if ye will hear his voice, harden not your hearts."</em> Hardening is gradual — each refusal of conviction tightens the surface until the conscience no longer registers. The remedy is immediate response: hear, repent, soften, return. Christian men must examine themselves regularly for the first cracks of indifference; what is left unsoftened soon hardens to stone.</p>'
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
