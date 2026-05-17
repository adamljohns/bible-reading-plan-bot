#!/usr/bin/env python3
"""Expand the biblical_def of 25 short dictionary entries to 60-100 words each.

Each expansion is hand-authored to be substantive theological prose grounded
in specific scripture references, matching the voice of the existing MOOP
Dictionary entries.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

# slug -> new biblical_def inner HTML (everything inside <div class="biblical-def">...</div>)
EXPANSIONS = {
    'cloud-glory': (
        '<p>The visible manifestation of God\'s presence &mdash; what Hebrew Scripture calls the '
        '<em>kavod</em> (weight, glory) and the rabbis later named the <em>Shekinah</em>. The cloud '
        'descends at Sinai (Ex 19:16-18), leads Israel through the wilderness as pillar of cloud by '
        'day and fire by night (Ex 13:21-22), fills the tabernacle at its completion (Ex 40:34-38), '
        'and overshadows Solomon\'s temple so that the priests cannot stand to minister (1 Kgs 8:10-11). '
        'Christ ascends in a cloud (Acts 1:9) and returns the same way (Rev 1:7; Matt 24:30). The cloud '
        'is not weather; it is the LORD condescending to be seen while keeping His infinity from being '
        'contained. Where the cloud is, there is the dwelling of God with His people.</p>'
    ),
    'gate-narrow': (
        '<p>Christ\'s image for the entrance to eternal life: <em>strait is the gate, and narrow is the '
        'way, which leadeth unto life, and few there be that find it</em> (Matt 7:13-14). The narrowness '
        'is double. First, the gate itself: entry is by Christ alone, who declares <em>I am the door</em> '
        '(John 10:9) and <em>I am the way, the truth, and the life: no man cometh unto the Father, but by '
        'me</em> (John 14:6). Second, the path that follows: the daily taking up of the cross (Luke 9:23) '
        'in disciplined obedience. Wide-gate Christianity that offers Christ without surrender is not '
        'Christ\'s gospel; it is its inversion. The narrow gate is the only door, and few find it &mdash; '
        'not because God hides it, but because the cost of entering is the death of the self.</p>'
    ),
    'restore': (
        '<p>To bring back to an original state of wholeness, soundness, or favor. The Hebrew root '
        '<em>shub</em> (turn, return, restore) runs through Scripture from the personal (<em>he restoreth '
        'my soul</em>, Ps 23:3) to the prophetic call for national repentance (Jer 15:19; Hos 6:1) to the '
        'sweeping promise of Joel 2:25: <em>I will restore to you the years that the locust hath eaten</em>. '
        'The Greek New Testament uses <em>apokathistemi</em> (Acts 3:21) of the eschatological restoration '
        'of all things. Christian salvation is restoration to a deeper wholeness than Eden\'s, because the '
        'restored bear Christ\'s resurrection-life rather than Adam\'s original innocence. What God restores, '
        'He restores upward &mdash; not back to before-the-fall but forward to better-than-Eden.</p>'
    ),
    'blood-new-covenant': (
        '<p>Christ\'s blood that ratifies the new covenant promised in Jeremiah 31:31-34. At the Last Supper, '
        'Christ takes the cup and names it: <em>this is my blood of the new testament, which is shed for many '
        'for the remission of sins</em> (Matt 26:28; Luke 22:20). The image echoes Moses sprinkling sacrificial '
        'blood on the people to seal Sinai\'s covenant (Ex 24:8) &mdash; the same pattern, now fulfilled and '
        'surpassed in the blood of the Mediator (Heb 9:14-15). Where the old covenant required repeated animal '
        'sacrifices that could never finally take away sin, Christ\'s once-for-all blood-shedding eternally '
        'seals the new (Heb 10:10-14). To drink the cup of communion is to participate in this very ratification '
        '&mdash; not symbolically only, but in living covenantal union with the One whose blood was spilled.</p>'
    ),
    'body-broken': (
        '<p>Christ\'s sacrificial body given for the church. At the Last Supper, Christ breaks the bread '
        'and names it: <em>this is my body, which is broken for you</em> (Matt 26:26; 1 Cor 11:24). The '
        'brokenness fulfills the Passover lamb pattern (Ex 12) where the lamb was killed and consumed by '
        'the household, yet without a bone being broken (John 19:36 explicitly applies Ex 12:46 to the '
        'cross). Christ\'s body is broken in death but kept in bone (Ps 34:20) &mdash; both fulfillments '
        'at once. In the Lord\'s Supper, the broken bread is the participation in this single sacrifice '
        'through which the church is constituted as His one body (1 Cor 10:17). The broken body of '
        'Christ creates the one body of the church.</p>'
    ),
    'bread-life': (
        '<p>Christ\'s self-designation in John 6: <em>I am the bread of life: he that cometh to me shall '
        'never hunger</em> (v. 35). The discourse builds on three threads. First, the manna in the '
        'wilderness (Ex 16) &mdash; bread given from heaven, daily, to a redeemed people who had no other '
        'means of life. Second, Christ\'s own multiplication of the loaves (John 6:1-14), the sign that '
        'occasions the discourse. Third, the Eucharistic foreshadow: <em>except ye eat the flesh of the '
        'Son of man, and drink his blood, ye have no life in you</em> (John 6:53). The bread of life is '
        'not metaphor for moral inspiration; it is Christ Himself, given for the world\'s eating, and '
        'apart from feeding on Him there is no life.</p>'
    ),
    'door-sheep': (
        '<p>Christ\'s self-designation in John 10:7-9: <em>I am the door of the sheep... by me if any man '
        'enter in, he shall be saved</em>. The image draws on the ancient shepherd\'s practice of lying '
        'across the entrance to the sheepfold at night, becoming with his own body the door that no thief '
        'or wolf could pass. Christ is both the shepherd (John 10:11) and the door (10:9) &mdash; two '
        'images, one Person, one work. The door image is exclusive (He alone is the entrance to salvation) '
        'and pastoral (He gives Himself as the body the sheep pass through and the wolves cannot). To '
        'enter the fold is to enter through Christ; there is no second door, no secondary entrance, no '
        'alternative passage to the Father.</p>'
    ),
    'shofar-trumpet': (
        '<p>The ram\'s horn blown in Israel\'s assembly for war, worship, alarm, and feast. Hebrew '
        '<em>shofar</em>; Greek NT <em>salpinx</em>. Scripture sounds the trumpet at Sinai (Ex 19:16, where '
        'God Himself sounds it), at the conquest of Jericho (Josh 6), at the feast of trumpets (Lev 23:24, '
        'now called Rosh Hashanah), at the watchman\'s warning (Ezek 33:6), and at the eschatological '
        'gathering of the elect (Matt 24:31; 1 Cor 15:52; 1 Thess 4:16). Joel 2:1\'s <em>blow the trumpet '
        'in Zion</em> joins the day-of-the-LORD warning to the call for repentance. The shofar is not '
        'mere music; it is the audible sign that God Himself has spoken, summoned, or is about to act. '
        'The next great trumpet sound will raise the dead.</p>'
    ),
    'word-fire': (
        '<p>God\'s word as a consuming, purifying force. The image is Jeremiah\'s: <em>is not my word like '
        'as a fire? saith the LORD; and like a hammer that breaketh the rock in pieces</em> (Jer 23:29). '
        'The same prophet, exhausted, says the word burns in his bones so that he cannot stay silent (Jer '
        '20:9). Hebrews 4:12 names the word <em>quick, and powerful, and sharper than any twoedged sword, '
        'piercing even to the dividing asunder of soul and spirit</em>. Fire in Scripture both judges (Lev '
        '10:2; 2 Thess 1:7-8) and refines (1 Cor 3:13; 1 Pet 1:7); the word does both. To receive Scripture '
        'rightly is to be willing to be burned by it &mdash; the consuming of every false structure the '
        'word touches in the heart that submits to it.</p>'
    ),
    'wrath-lamb': (
        '<p>The fierce judgment of Christ in Revelation. The phrase \"wrath of the Lamb\" (Rev 6:16) is '
        'one of Scripture\'s most striking conjunctions: the slaughtered Passover sacrifice (Rev 5:6) is '
        'also the One from whose face kings of the earth, the great men, the rich men, the chief captains, '
        'the mighty men, every bondman and every free man hide in the rocks. The juxtaposition is '
        'theological, not contradictory. The same Christ who absorbed the Father\'s wrath at the cross now '
        'pours it out on those who have refused His sacrifice. Wrath of the Lamb names the impossibility '
        'of escaping into a fictional sentimental Jesus when the actual Christ returns. The meekest face '
        'in history will be the most terrible face on the last day for those who have spurned Him.</p>'
    ),
    'zeal-house': (
        '<p>Consuming passion for God\'s dwelling and honor. Psalm 69:9: <em>for the zeal of thine house '
        'hath eaten me up</em>. The disciples remember this verse when Christ drives the moneychangers '
        'from the temple (John 2:17), recognizing in His action the messianic fulfillment of the psalmist\'s '
        'consumed zeal. Biblical zeal (Heb. <em>qinah</em>, Gk. <em>zelos</em>) is not generic enthusiasm; '
        'it is a specifically God-ward burning that cannot tolerate the desecration of what God has called '
        'holy. Paul names zeal that is not according to knowledge as a real danger (Rom 10:2). But '
        'knowledge-formed zeal &mdash; the Christ-pattern &mdash; turns over tables and clears the temple '
        'of every commerce that has replaced worship. Where God\'s house is dishonored, the consumed-zealous '
        'heart acts.</p>'
    ),
    'abide-vine': (
        '<p>Christ\'s command in John 15: <em>abide in me, and I in you. As the branch cannot bear fruit '
        'of itself, except it abide in the vine; no more can ye, except ye abide in me</em> (v. 4). The '
        'Greek <em>meno</em> means to remain, dwell, continue &mdash; a settled staying rather than a '
        'sporadic visiting. The image draws on the OT vineyard of Israel (Isa 5; Ps 80), now '
        'eschatologically fulfilled in Christ as the true vine. Abiding is not effort to attain union but '
        'the constant cultivation of one already given: through the word abiding in us (15:7), through '
        'obedience (15:10), through love (15:9). Apart from the vine, the branch withers; in the vine, '
        'the branch bears fruit it could never have produced alone.</p>'
    ),
    'bright-morning-star': (
        '<p>Christ\'s self-designation as the herald of eternal day. Revelation 22:16: <em>I Jesus have '
        'sent mine angel to testify unto you these things in the churches. I am the root and the offspring '
        'of David, and the bright and morning star</em>. The morning star is Venus, the brightest body in '
        'the predawn sky &mdash; the last light before the sun rises, the sign that the night is ending. '
        'The image had been promised in Numbers 24:17 (<em>there shall come a Star out of Jacob</em>) and '
        'echoed in 2 Peter 1:19 (<em>the day star arise in your hearts</em>). Christ as the bright morning '
        'star is the promise that whatever night the church endures, the eternal day is at hand. He has '
        'risen; the dawn is certain; the night is almost over.</p>'
    ),
    'cup-wrath': (
        '<p>The full measure of divine judgment poured out, imaged as a cup the wicked must drink to the '
        'dregs. The OT prophetic image: <em>thus saith the LORD God of Israel unto me; Take the wine cup '
        'of this fury at my hand, and cause all the nations, to whom I send thee, to drink it</em> (Jer '
        '25:15; cf. Isa 51:17, 22; Hab 2:16; Ps 75:8). At Gethsemane, Christ prays <em>O my Father, if '
        'it be possible, let this cup pass from me</em> (Matt 26:39) &mdash; not the cup of physical '
        'suffering alone but the cup of His Father\'s wrath against sin, which He alone could drain to '
        'the bottom and exhaust on behalf of His people. The cup the Christian receives at communion '
        '(1 Cor 10:16) is the cup of blessing precisely because Christ drank the cup of wrath in full.</p>'
    ),
    'great-physician': (
        '<p>Christ as the healer of body and soul. The title is implicit in Christ\'s own words: <em>they '
        'that be whole need not a physician, but they that are sick. But go ye and learn what that meaneth, '
        'I will have mercy, and not sacrifice: for I am not come to call the righteous, but sinners to '
        'repentance</em> (Matt 9:12-13). The Gospels record His healing of physical disease repeatedly '
        '(Matt 4:23-24; Mk 1:32-34; Lk 4:40), but the deeper healing is spiritual: the forgiveness of '
        'sins (Mk 2:5), the casting out of unclean spirits, the raising of the dead. The great physician '
        'addresses the whole patient &mdash; body, soul, spirit &mdash; and unlike all other physicians, '
        'His ultimate cure is the resurrection of the body itself (1 Cor 15:42-44).</p>'
    ),
    'reward-heaven': (
        '<p>The eschatological recompense laid up for the faithful. Christ commands: <em>rejoice, and be '
        'exceeding glad: for great is your reward in heaven: for so persecuted they the prophets which '
        'were before you</em> (Matt 5:12). The reward is not earned wages (salvation is gift, Eph 2:8-9), '
        'but it is real and proportionate to faithful service (Matt 6:1-6; 1 Cor 3:14; Rev 22:12: '
        '<em>behold, I come quickly; and my reward is with me, to give every man according as his work '
        'shall be</em>). Scripture distinguishes <em>treasure in heaven</em> (Matt 6:20) from earthly '
        'reward, frames the reward as Christ Himself (Gen 15:1: <em>I am thy exceeding great reward</em>), '
        'and refuses the modern flattening of Christianity into earthly utility. The reward of the '
        'faithful is laid up, kept, certain &mdash; and will not disappoint.</p>'
    ),
    'righteous-anger': (
        '<p>Holy indignation against sin and injustice. Paul commands: <em>be ye angry, and sin not: let '
        'not the sun go down upon your wrath</em> (Eph 4:26, quoting Ps 4:4). The verse establishes two '
        'truths in tension: anger as such is not sin (Christ Himself was angry in Mark 3:5, John 2:13-17), '
        'and anger easily becomes sin if held, fed, or directed at the wrong object. Biblical righteous '
        'anger has three marks: it is God-ward in cause (angry at what God is angry at), proportionate '
        'in expression (not the rage of fleshly retaliation), and bounded in duration (not allowed to '
        'fester past nightfall). James 1:20 names the failure-mode: <em>the wrath of man worketh not the '
        'righteousness of God</em>. The Christian man learns to be angry rightly &mdash; rare, true, '
        'God-aimed &mdash; and to let go of the rest.</p>'
    ),
    'shield-faith': (
        '<p>The spiritual armor that extinguishes the enemy\'s attacks. Paul writes: <em>above all, taking '
        'the shield of faith, wherewith ye shall be able to quench all the fiery darts of the wicked</em> '
        '(Eph 6:16). The Roman soldier\'s <em>thureos</em> (door-shaped large shield) was soaked in water '
        'before battle so that flaming arrows hitting it would be extinguished on impact rather than '
        'igniting the soldier. Paul\'s analogy is precise: faith is what the believer holds in front of '
        'himself in spiritual combat, and the enemy\'s lies, accusations, doubts, and temptations are the '
        '<em>fiery darts</em> that faith extinguishes by meeting them with the truth of God\'s word and '
        'character. Faith is not feeling; it is the active trust that holds Christ\'s promises between '
        'the soul and every attack.</p>'
    ),
    'winnowing-fork': (
        '<p>The instrument of separation between wheat and chaff. John the Baptist\'s image: '
        '<em>whose fan is in his hand, and he will throughly purge his floor, and gather his wheat into '
        'the garner; but he will burn up the chaff with unquenchable fire</em> (Matt 3:12; Lk 3:17). The '
        'winnowing fork (Greek <em>ptuon</em>) was the wooden tool used at the threshing floor to toss '
        'the threshed grain into the air, letting the wind blow away the lighter chaff while the heavier '
        'wheat fell back to the floor. John applies the image to the coming One: Christ\'s ministry will '
        'separate. There is no third category. The same Christ who gathers the wheat into the garner '
        'burns the chaff with unquenchable fire. The fork is in His hand; the floor is being purged; the '
        'separation is in process now and will be complete at the end.</p>'
    ),
    'witness-cloud': (
        '<p>The saints of Hebrews 11 who surround the Christian in his race. Hebrews 12:1: <em>wherefore '
        'seeing we also are compassed about with so great a cloud of witnesses, let us lay aside every '
        'weight, and the sin which doth so easily beset us, and let us run with patience the race that is '
        'set before us</em>. The Greek <em>marturon</em> (witnesses) plays on the double sense of <em>those '
        'who have testified by faithful endurance</em> (the figures of ch. 11) and <em>those who watch the '
        'race</em>. Whether they observe the church\'s ongoing struggle in any conscious sense is debated; '
        'what is not debated is that their endurance is the precedent for ours. Abraham, Moses, Rahab, '
        'David, the prophets, the unnamed martyrs &mdash; all bore witness that faith in the unseen God '
        'pays out. We run the same race they ran, with their record as evidence of its end.</p>'
    ),
    'firstborn-dead': (
        '<p>Christ\'s title as the first to rise from the dead with a glorified, never-to-die-again body. '
        'Colossians 1:18: <em>he is the head of the body, the church: who is the beginning, the firstborn '
        'from the dead; that in all things he might have the preeminence</em>. Echoed in Revelation 1:5 '
        '(<em>the first begotten of the dead</em>) and 1 Corinthians 15:20 (<em>now is Christ risen from '
        'the dead, and become the firstfruits of them that slept</em>). The image distinguishes Christ\'s '
        'resurrection from prior resuscitations (Lazarus, Jairus\'s daughter, the widow of Nain\'s son) '
        '&mdash; all of whom died again. Christ is firstborn from the dead because His resurrection-body '
        'is the prototype of the glorified body all His people will receive (1 Cor 15:23, 49). His rising '
        'is not just His own; it is the firstfruits guaranteeing the full harvest.</p>'
    ),
    'sacred-assembly': (
        '<p>The set-apart gathering of God\'s people called by divine command. Hebrew <em>miqra qodesh</em> '
        '(holy convocation) &mdash; named over the appointed feasts of Leviticus 23 (Sabbath, Passover, '
        'Pentecost, Day of Atonement, Tabernacles). Joel 1:14 and 2:15 use the same term in calls for '
        'national repentance: <em>sanctify a fast, call a solemn assembly</em>. A sacred assembly is not '
        'merely a meeting; it is the people of God responding to God\'s summons in His prescribed way, '
        'set apart from ordinary commerce and ordinary labor for the worship of the LORD. The New '
        'Testament continuation is the <em>ekklesia</em> &mdash; the called-out assembly of Christ. The '
        'Lord\'s Day gathering of the church is the modern sacred assembly, and treating it as optional '
        'social calendar item rather than as commanded covenant gathering inverts what Scripture is naming.</p>'
    ),
    'salt-earth': (
        '<p>Christ\'s designation for His disciples in the Sermon on the Mount: <em>ye are the salt of the '
        'earth: but if the salt have lost his savour, wherewith shall it be salted? it is thenceforth good '
        'for nothing, but to be cast out, and to be trodden under foot of men</em> (Matt 5:13). In the '
        'ancient world salt was a preservative, a flavor-enhancer, a covenant-sign (Lev 2:13: <em>the salt '
        'of the covenant</em>; Num 18:19; 2 Chr 13:5), and a soil-purifier. Christ\'s use combines the '
        'preservative and covenant senses: His disciples are the agent by which the surrounding culture '
        'is kept from decay and the agent through which God\'s covenant faithfulness reaches the world. '
        'Salt that has lost its savour is useless &mdash; the warning is sharp: a church or Christian '
        'that no longer preserves what God preserves has become functionally trampled.</p>'
    ),
    'scroll-sealed': (
        '<p>The seven-sealed scroll of Revelation 5 that only the Lamb is worthy to open. The scene: a '
        'throne, a scroll written within and on the backside, sealed with seven seals, and a strong angel '
        'asking <em>who is worthy to open the book?</em> &mdash; the question producing John\'s tears '
        'because no one in heaven or earth or under the earth could be found worthy. Then one of the '
        'elders speaks: <em>weep not: behold, the Lion of the tribe of Juda, the Root of David, hath '
        'prevailed to open the book, and to loose the seven seals thereof</em>. The Lamb takes the scroll, '
        'and the unfolding of redemptive history follows. The scroll contains the LORD\'s plan for the '
        'consummation of all things; the Lamb alone is worthy to execute it because He alone purchased '
        'the right by His blood (5:9). History is going somewhere, and only Christ is opening it.</p>'
    ),
    'sufficient-grace': (
        '<p>God\'s answer to Paul\'s thrice-prayed prayer for relief from the thorn in the flesh: <em>my '
        'grace is sufficient for thee: for my strength is made perfect in weakness</em> (2 Cor 12:9). The '
        'verse refuses the modern Christian instinct that God\'s grace must remove the trial. Sometimes '
        'it does; in Paul\'s case it did not, and the not-removal was itself the lesson. Sufficient grace '
        'means: enough for this hour, enough for this weakness, enough for this thorn, with the strength '
        'of Christ rested on the weak servant precisely in the place of his weakness. Paul\'s response '
        'is the disposition Scripture commends: <em>most gladly therefore will I rather glory in my '
        'infirmities, that the power of Christ may rest upon me</em>. The thorn that remains becomes the '
        'site of the strength that comes &mdash; the very theology of the cross written into a personal '
        'life.</p>'
    ),
}

# Match the biblical-def div and capture inner content
BD_RE = re.compile(
    r'(<div class="biblical-def">)(.*?)(</div>)',
    re.DOTALL
)


def patch(slug, new_inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return False, 'file missing'
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_html, n = BD_RE.subn(rf'\g<1>\n                {new_inner}\n            \g<3>', html, count=1)
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
