#!/usr/bin/env python3
"""Expand 25 more short dictionary entries to 90-120 words each (batch 2)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'whole-armor': (
        '<p>The complete spiritual protection commanded in Ephesians 6:10-18. Paul names six pieces &mdash; '
        'belt of truth, breastplate of righteousness, shod feet with the preparation of the gospel of peace, '
        'shield of faith, helmet of salvation, sword of the Spirit (which is the word of God) &mdash; and '
        'commands the Christian to <em>put on the whole armor of God, that ye may be able to stand against '
        'the wiles of the devil</em>. The plural <em>wiles</em> matters: the enemy attacks variously, and '
        'partial armor fails the test. Each piece corresponds to a specific spiritual function; together '
        'they constitute the panoply (Greek <em>panoplia</em>) the Christian needs for the <em>evil day</em>. '
        'The armor is a gift to put on, not a virtue to manufacture &mdash; but the putting-on is the '
        'believer\'s responsibility, daily and deliberate.</p>'
    ),
    'woman-valor': (
        '<p>The Proverbs 31 portrait of feminine strength and godliness. The Hebrew phrase <em>eshet chayil</em> '
        '(woman of valor) uses the same strength-word (<em>chayil</em>) elsewhere applied to mighty warriors '
        'and the LORD\'s armies. The biblical ideal is the opposite of the cultural caricature: she is '
        'industrious (vv. 13-19), entrepreneurial (vv. 16, 24), strong in body and mind (v. 17, <em>she '
        'girdeth her loins with strength</em>), spiritually formed (v. 30, <em>a woman that feareth the LORD</em>), '
        'wise in speech (v. 26, <em>the law of kindness is in her tongue</em>), and the trust of her husband\'s '
        'heart (v. 11). She is not the passive doll of soft-complementarian fantasy or the rivalrous striver '
        'of feminist polemic. She is a strength deployed under covenant for the good of household, husband, '
        'and the LORD whose fear orders her life.</p>'
    ),
    'word-became-flesh': (
        '<p>The incarnation &mdash; the eternal <em>Logos</em> taking on human nature without ceasing to be God. '
        'John 1:14: <em>And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory '
        'as of the only begotten of the Father,) full of grace and truth</em>. The Greek <em>egeneto sarx</em> '
        '(became flesh) is direct and shocking: the One who was God (1:1) became the kind of weakness God '
        'created. The verb <em>eskēnōsen</em> (dwelt) literally means <em>tabernacled</em> &mdash; placing '
        'His tent among us &mdash; echoing the tabernacle where the cloud of glory had dwelt (Ex 40:34). '
        'The incarnation is not God appearing as a man; it is God becoming truly Man, two natures permanently '
        'united in one Person, without confusion, without change, without division, without separation '
        '(Chalcedon, AD 451).</p>'
    ),
    'worship-spirit-truth': (
        '<p>Christ\'s teaching to the Samaritan woman at the well: <em>God is a Spirit: and they that worship '
        'him must worship him in spirit and in truth</em> (John 4:24). The phrase corrects two opposite errors. '
        '<em>In spirit</em> rules out merely external, ritualistic, geographically-bound worship &mdash; the '
        'specific issue the woman raised about Gerizim vs. Jerusalem. <em>In truth</em> rules out merely '
        'emotional, subjective, doctrinally-loose worship &mdash; the modern temptation that opposite-corrects '
        'the first error and lands in a different ditch. True worship is heart-engaged AND doctrinally '
        'grounded: the Spirit-quickened soul responding to the truth of who God actually is, on the basis '
        'of what He has actually said. Either pole alone fails. Both together are what the Father seeks.</p>'
    ),
    'worthy-lamb': (
        '<p>The heavenly anthem of Revelation 5:12: <em>Worthy is the Lamb that was slain to receive power, '
        'and riches, and wisdom, and strength, and honour, and glory, and blessing</em>. The scene is the '
        'climax of the throne-room vision (Rev 4-5): the sealed scroll, the search for one worthy to open '
        'it, John\'s tears at finding none, and then the Lamb &mdash; standing as if slain &mdash; stepping '
        'forward and taking the scroll from the Father\'s right hand. The four living creatures and the '
        'twenty-four elders fall down before Him, the new song bursts forth, and ten thousand times ten '
        'thousand voices join the worship. The Lamb is worthy not despite being slain but because of it &mdash; '
        'the slain Lamb has purchased people from every tribe, tongue, people, and nation. Worship in '
        'heaven is centered on the cross.</p>'
    ),
    'yoke-easy': (
        '<p>Christ\'s invitation in Matthew 11:28-30: <em>Come unto me, all ye that labour and are heavy '
        'laden, and I will give you rest. Take my yoke upon you, and learn of me; for I am meek and lowly '
        'in heart: and ye shall find rest unto your souls. For my yoke is easy, and my burden is light</em>. '
        'The Greek <em>chrēstos</em> (easy) carries the sense of <em>well-fitting, suited, kindly</em>. '
        'The image is comparative: Christ\'s yoke is easier than the law\'s yoke (which Peter calls a yoke '
        '<em>neither our fathers nor we were able to bear</em>, Acts 15:10), easier than the world\'s yokes '
        'of vain striving, easier than the legalist\'s yoke of self-justification. Christian discipleship '
        'is not effortless &mdash; the narrow way is still narrow &mdash; but it is fitted to the redeemed '
        'soul as no other yoke can be, because the One who designed the soul also designed the yoke.</p>'
    ),
    'good-shepherd': (
        '<p>Christ\'s self-designation in John 10:11-18: <em>I am the good shepherd: the good shepherd '
        'giveth his life for the sheep</em>. The image draws on the OT shepherd-king tradition (Ezek 34, '
        'where God Himself promises to come shepherd His scattered flock when their human shepherds have '
        'failed; Ps 23, the most beloved psalm) and fulfills it. Christ contrasts Himself with the hireling '
        '(10:12-13) who flees when the wolf comes &mdash; the hireling does not own the sheep and so does '
        'not love them at cost. The good shepherd lays down His life voluntarily (10:18, <em>no man taketh '
        'it from me, but I lay it down of myself</em>) and takes it up again. The mark of the true Christ-shepherd, '
        'over against the false, is willingness to die for the sheep. The cross is the diagnostic.</p>'
    ),
    'renewal-mind': (
        '<p>The ongoing transformation of the Christian\'s thinking by the Holy Spirit. Romans 12:2: '
        '<em>And be not conformed to this world: but be ye transformed by the renewing of your mind, that '
        'ye may prove what is that good, and acceptable, and perfect, will of God</em>. The Greek '
        '<em>metamorphousthe</em> (be transformed) is the same verb used of Christ\'s transfiguration on '
        'the mount &mdash; the inner reality becoming visibly displayed. The renewal happens through the '
        'word (Eph 5:26, <em>cleansing by the washing of water by the word</em>), through the Spirit\'s '
        'continued application of that word to specific patterns of thought, and through the Christian\'s '
        'deliberate participation: taking every thought captive to the obedience of Christ (2 Cor 10:5). '
        'The mind is the battlefield; renewal is the long campaign that ends in conformity to Christ.</p>'
    ),
    'rock-ages': (
        '<p>Christ as the eternal, unshakable foundation. The image is sounded throughout Scripture: '
        '<em>the LORD is my rock, and my fortress, and my deliverer</em> (Ps 18:2; cf. 2 Sam 22:2, Deut '
        '32:4); the rock smitten by Moses that gave water in the wilderness (Ex 17:6) which Paul identifies '
        'as Christ (<em>and that Rock was Christ</em>, 1 Cor 10:4); the stone the builders rejected that '
        'became the chief cornerstone (Ps 118:22; Matt 21:42; 1 Pet 2:7); and Isaiah\'s <em>tried stone, a '
        'precious corner stone, a sure foundation</em> (Isa 28:16). Augustus Toplady\'s 1776 hymn <em>Rock '
        'of Ages</em> gathered the threads into one of the church\'s most enduring lyrics. The rock of '
        'ages is the One foundation that storms cannot shake and ages cannot wear down.</p>'
    ),
    'rod-staff': (
        '<p>The shepherd\'s twin instruments in Psalm 23:4: <em>thy rod and thy staff they comfort me</em>. '
        'In ancient Near Eastern shepherding, the rod (Hebrew <em>shebet</em>) was the short club worn at '
        'the belt &mdash; used to fight off predators and to count and inspect the sheep. The staff (Hebrew '
        '<em>mishenet</em>) was the longer crook &mdash; used to guide, to gently push or pull the sheep, '
        'to retrieve a lamb from a crevice. Together they comprise the shepherd\'s pastoral kit: the rod '
        'for protection from enemies and the staff for guidance of the flock. Both <em>comfort</em> the '
        'sheep because both communicate the shepherd\'s presence and care &mdash; the same instruments '
        'that discipline are the instruments that protect. The LORD\'s discipline and the LORD\'s '
        'guidance are not separate gifts; they are two functions of one shepherding love.</p>'
    ),
    'sanctification-progressive': (
        '<p>The lifelong process by which the justified believer is gradually conformed to the image of '
        'Christ. Distinguished from <em>positional</em> sanctification (the once-for-all setting-apart at '
        'conversion, 1 Cor 6:11) and from <em>final</em> sanctification (the perfection at glorification, '
        '1 John 3:2). Progressive sanctification works by the Spirit applying the word to specific sin '
        'patterns over time, with the believer\'s deliberate participation: <em>work out your own salvation '
        'with fear and trembling. For it is God which worketh in you both to will and to do of his good '
        'pleasure</em> (Phil 2:12-13). The paradox is real: God works, AND the believer works; the works '
        'are not in competition. Sanctification is not earned (it is grace) but it is also not passive '
        '(the believer is commanded to pursue it). Slow, real, often invisible from the inside, the '
        'mirror at the end of the process is Christ Himself.</p>'
    ),
    'second-death': (
        '<p>Eternal separation from God in the lake of fire. Revelation 20:14-15: <em>And death and hell '
        'were cast into the lake of fire. This is the second death. And whosoever was not found written '
        'in the book of life was cast into the lake of fire</em>. The first death is physical &mdash; '
        'the body\'s separation from the soul, the consequence of Adam\'s fall (Rom 5:12). The second '
        'death is final &mdash; the eternal conscious punishment of those whose names are not in the '
        'Lamb\'s book of life. Christ promises His own that they will not be hurt by the second death '
        '(Rev 2:11). The doctrine is among the hardest in Scripture and is among the clearest. The modern '
        'church\'s frequent flight from eternal punishment is a refusal of Christ\'s own teaching '
        '(Matt 25:46, <em>these shall go away into everlasting punishment: but the righteous into life '
        'eternal</em>). The same Christ who promised heaven warned of hell.</p>'
    ),
    'sow-reap': (
        '<p>The biblical law of cause-and-consequence in moral and spiritual life. Galatians 6:7-8: '
        '<em>Be not deceived; God is not mocked: for whatsoever a man soweth, that shall he also reap. '
        'For he that soweth to his flesh shall of the flesh reap corruption; but he that soweth to the '
        'Spirit shall of the Spirit reap life everlasting</em>. The principle is observable in nature '
        '(the agricultural reality) and pronounced as moral law in Scripture (Job 4:8; Prov 22:8; Hos 8:7; '
        '2 Cor 9:6). It is not karma &mdash; Christian sowing-and-reaping operates under grace and final '
        'judgment, not impersonal cosmic balance. But within God\'s ordering of moral reality, what is '
        'sown matters: <em>be not deceived</em> is Paul\'s warning to those who imagine they can plant '
        'flesh and harvest spirit, or sow sin and reap blessing. The harvest comes. It always comes.</p>'
    ),
    'stranger-pilgrim': (
        '<p>The biblical identity of believers as temporary residents on earth. Hebrews 11:13: <em>These '
        'all died in faith, not having received the promises, but having seen them afar off, and were '
        'persuaded of them, and embraced them, and confessed that they were strangers and pilgrims on the '
        'earth</em>. Peter applies the same vocabulary to ordinary Christians: <em>Dearly beloved, I '
        'beseech you as strangers and pilgrims, abstain from fleshly lusts, which war against the soul</em> '
        '(1 Pet 2:11). The Greek <em>parepidemos</em> (sojourner, resident alien) and <em>paroikos</em> '
        '(stranger) capture both halves: present in the place but not finally belonging to it, with a '
        'better country awaiting (Heb 11:16). The stranger-pilgrim identity orders the Christian\'s '
        'engagement with the world: invested but not enmeshed, working but not weighted down, present '
        'but on the way to somewhere truer.</p>'
    ),
    'strength-joy': (
        '<p>Nehemiah 8:10\'s declaration to the people weeping over the rediscovered law: <em>Go your way, '
        'eat the fat, and drink the sweet, and send portions unto them for whom nothing is prepared: for '
        'this day is holy unto our Lord: neither be ye sorry; for the joy of the LORD is your strength</em>. '
        'The verse establishes a counter-intuitive principle. Strength does not come from suppressing '
        'sorrow or manufacturing positivity; it comes from a particular joy &mdash; <em>the joy of the '
        'LORD</em>, which is to say the joy that has God Himself as its object. This is why Paul can say '
        '<em>rejoice in the Lord alway: and again I say, rejoice</em> from a prison cell (Phil 4:4). '
        'Christian strength is sustained by Christian joy, and Christian joy is sustained by Christian '
        'communion with the LORD whose unchanging character is the joy\'s ground.</p>'
    ),
    'vine-branches': (
        '<p>Christ\'s defining metaphor for the believer\'s living dependence on Him. John 15:5: <em>I am '
        'the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much '
        'fruit: for without me ye can do nothing</em>. The image fulfills the OT vineyard tradition (Isa '
        '5; Ps 80; Jer 2:21), in which Israel was God\'s vineyard but had become a wild vine that produced '
        'wild grapes. Christ is the true vine; the Father is the husbandman; believers are branches grafted '
        'into Christ by faith. Two warnings follow: branches that do not abide are pruned away and burned '
        '(15:6); branches that do abide are pruned for greater fruitfulness (15:2). The metaphor presses '
        'organic, not mechanical, union: the believer\'s life is Christ\'s life flowing through him, '
        'and apart from that flow nothing of true fruit is produced.</p>'
    ),
    'water-rock': (
        '<p>God\'s miraculous provision for Israel in the wilderness, and a typological picture of Christ. '
        'Exodus 17:1-7 and Numbers 20:7-13 record two occasions when the LORD brought water from a rock '
        'to sustain His thirsty people. Psalm 78:20: <em>he smote the rock, that the waters gushed out, '
        'and the streams overflowed</em>. Paul interprets the rock typologically in 1 Corinthians 10:4: '
        '<em>they drank of that spiritual Rock that followed them: and that Rock was Christ</em>. The '
        'pattern is rich: the rock smitten gives life-giving water; Christ smitten on the cross pours '
        'out the Spirit (John 7:37-39) and the blood-and-water of His side (John 19:34). Moses\' second '
        'failure (striking the rock when commanded to speak to it, Num 20) cost him entry into the land &mdash; '
        'the typological reason being that Christ is smitten once, not twice.</p>'
    ),
    'wisdom-above': (
        '<p>James 3:17\'s description of the wisdom that comes from God, contrasted with the earthly, '
        'sensual, devilish wisdom of the prior verses: <em>But the wisdom that is from above is first '
        'pure, then peaceable, gentle, and easy to be intreated, full of mercy and good fruits, without '
        'partiality, and without hypocrisy</em>. James lists seven marks. <em>First pure</em> &mdash; '
        'the priority is unmistakable; wisdom that compromises moral integrity for the sake of peace is '
        'not wisdom from above. <em>Then peaceable</em> &mdash; peace is real but second to purity. The '
        'remaining marks (gentleness, willingness to be entreated, mercy, good fruit, impartiality, '
        'no hypocrisy) all flow from the prior two. The contrast with earthly wisdom (vv. 14-16, marked '
        'by bitter envying and strife) is sharp: where one produces confusion and every evil work, the '
        'other produces a harvest of righteousness sown in peace.</p>'
    ),
    'reproach': (
        '<p>Shame or disgrace borne for God\'s sake. Hebrews 11:26: <em>Esteeming the reproach of Christ '
        'greater riches than the treasures in Egypt: for he had respect unto the recompence of the reward</em>. '
        'Moses\' choice prefigures the Christian\'s ordinary calling: to count association with Christ '
        '&mdash; including the social cost it carries &mdash; as greater wealth than worldly advantage. '
        'Christ Himself bore the ultimate reproach (Heb 13:13, <em>let us go forth therefore unto him '
        'without the camp, bearing his reproach</em>). The apostles rejoiced when counted worthy to '
        'suffer shame for His name (Acts 5:41). Reproach is not pursued for its own sake (some Christians '
        'mistake annoying obnoxiousness for cross-bearing) but neither is it avoided when it comes for '
        'real association with Christ. The biblical man wears the cost without complaint and counts it '
        'gain.</p>'
    ),
    'royal-priesthood': (
        '<p>The biblical identity of all believers as priests to God under Christ the great High Priest. '
        '1 Peter 2:9: <em>But ye are a chosen generation, a royal priesthood, an holy nation, a peculiar '
        'people; that ye should shew forth the praises of him who hath called you out of darkness into '
        'his marvellous light</em>. Peter applies to the church what was said of Israel at Sinai (Ex 19:6: '
        '<em>a kingdom of priests, and an holy nation</em>). Under the new covenant, every believer has '
        'direct access to God through Christ (Heb 10:19-22) and bears priestly functions: offering '
        'spiritual sacrifices (1 Pet 2:5), interceding for others, mediating God\'s blessing into the '
        'world. The doctrine of the priesthood of all believers does not abolish ordained office (elders '
        'and pastors remain, 1 Pet 5:1-4) but it does abolish a separate priestly caste mediating between '
        'God and lay believers. Christ is the only such mediator (1 Tim 2:5).</p>'
    ),
    'sermon-mount': (
        '<p>The most concentrated body of Christ\'s ethical teaching in all of Scripture, given on a '
        'hillside in Galilee and recorded in Matthew 5-7 (with the parallel Sermon on the Plain in Luke '
        '6:20-49). The sermon opens with the Beatitudes (5:3-12) and closes with the parable of the two '
        'builders (7:24-27). Between, Christ addresses anger, lust, divorce, oaths, retaliation, love '
        'of enemies, almsgiving, prayer (giving the Lord\'s Prayer, 6:9-13), fasting, treasure, anxiety, '
        'judging others, asking-seeking-knocking, the narrow gate, and false prophets. The sermon is '
        'sometimes mistakenly read as the ethic of natural-religion goodness; it is the opposite. The '
        'standard is so high (<em>be ye therefore perfect, even as your Father which is in heaven is '
        'perfect</em>, 5:48) that without Christ\'s atoning work and the Spirit\'s power, no one can '
        'keep it. The sermon drives the sinner to grace, then forms the redeemed into kingdom-people.</p>'
    ),
    'shepherd-psalm': (
        '<p>Psalm 23 &mdash; the most beloved psalm of divine care, six brief verses unfolding the LORD\'s '
        'pastoral oversight of His people from green pastures through the valley of the shadow of death '
        'to the dwelling in the house of the LORD forever. David, himself a shepherd before he was king, '
        'wrote it from the inside of the trade. The structure moves through the sheep\'s ordinary day '
        '(feeding, watering, lying down), through the dangerous valley (the comforting rod and staff), '
        'through the surprising banquet (a table prepared in the presence of enemies), to the eternal '
        'destination (<em>I will dwell in the house of the LORD for ever</em>). The psalm is loved because '
        'every clause is true and because the speaker stakes everything on the goodness of the Shepherd, '
        'including the parts of life that look least like good pastures. Christ\'s claim to be the good '
        'shepherd (John 10:11) is the explicit fulfillment.</p>'
    ),
    'sign-covenant': (
        '<p>A visible marker God has appointed as the public token of a specific covenant. Scripture '
        'names several. The rainbow (Gen 9:12-17) signs the Noahic covenant of God\'s pledge never again '
        'to destroy the earth by flood. Circumcision (Gen 17:11) signs the Abrahamic covenant of God\'s '
        'pledge to be God to Abraham and his seed, marked in the flesh. The Sabbath (Ex 31:13-17) signs '
        'the Mosaic covenant between God and Israel as the people set apart in time. Baptism and the '
        'Lord\'s Supper sign the New Covenant ratified in Christ\'s blood (Matt 26:28; 28:19; 1 Cor 11:25). '
        'Each sign is more than memorial &mdash; it is God\'s self-pledge made visible. To despise the '
        'sign is to despise the covenant; to receive the sign rightly is to bind oneself in faith to the '
        'God who has signed Himself first.</p>'
    ),
    'silence-god': (
        '<p>The experience of God\'s apparent absence in the midst of suffering, prayer, or longing. '
        'The deepest biblical instance is Christ\'s cry from the cross: <em>My God, my God, why hast '
        'thou forsaken me?</em> (Matt 27:46), quoting Psalm 22:1 directly. Job\'s lament traces the same '
        'shape (Job 23:3-9). Many psalms (13, 22, 42, 88) hold the absence and the trust together without '
        'resolving them prematurely. The silence is not, finally, abandonment &mdash; Psalm 22 itself '
        'moves from forsaken-cry to triumphant praise (vv. 22-31), and Christ\'s cross-cry is followed '
        'by His resurrection. But the experience is real, and Scripture refuses to deny it. The Christian '
        'in the silence is in the company of the saints, the prophets, the psalmist, and the Son of God '
        'Himself. The silence will not be the last word; in the meantime, the saints have learned to '
        'speak into it.</p>'
    ),
    'stone-rejected': (
        '<p>Psalm 118:22\'s prophetic image, applied to Christ by Christ Himself: <em>The stone which '
        'the builders refused is become the head stone of the corner</em>. The image draws on ancient '
        'construction: a stone deemed unfit by the foremen, set aside as waste, but later discovered to '
        'be precisely the stone needed for the foundational corner where two walls meet and bear the '
        'weight of the whole structure. Christ applies the verse to Himself after the parable of the '
        'wicked vinedressers (Matt 21:42; Mark 12:10-11; Luke 20:17). Peter expounds the image (Acts '
        '4:11; 1 Pet 2:6-7) and Paul cites Isaiah 28:16 in the same context. The religious leaders of '
        'Israel were the builders who rejected the cornerstone &mdash; an irony Scripture does not let '
        'pass: the very experts in building the house of God refused the only stone that could hold it. '
        'Rejection by the qualified evaluators is not always evidence of unworthiness; sometimes it is '
        'the diagnosis of the evaluators.</p>'
    ),
}

BD_RE = re.compile(r'(<div class="biblical-def">)(.*?)(</div>)', re.DOTALL)


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
