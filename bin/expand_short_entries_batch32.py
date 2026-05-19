#!/usr/bin/env python3
"""Batch 32 — expand 25 more entries from the 50-60 word bucket.

Targets: Hebrew vocab, OT figures, NT historical, eschatology,
divine names, providence, and Scripture-gesture vocabulary.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'machseh': (
        '<p><em>Machseh</em> (מַחֲסֶה) is the Hebrew word for <em>refuge</em> — a place of shelter and retreat in danger, used repeatedly of YHWH Himself in the Psalter. The verb <em>chasah</em> ("to take refuge, flee for protection") describes the saint’s instinctive run to YHWH for cover. <em>Psalm 91</em> is the great refuge-psalm: <em>"He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty. I will say of the LORD, He is my refuge and my fortress: my God; in him will I trust"</em> (<em>vv. 1-2</em>); <em>"For thou hast been a shelter for me, and a strong tower from the enemy. I will abide in thy tabernacle for ever: I will trust in the covert of thy wings"</em> (<em>Psalm 61:3-4</em>). YHWH is not merely a refuge-provider; He is the refuge itself.</p>'
    ),
    'omer': (
        '<p><em>Omer</em> (עֹמֶר) carries two distinct senses in Scripture. First, it is a sheaf of grain — the <em>omer of firstfruits</em> waved before YHWH on the day after the Sabbath following Passover: <em>"Then ye shall bring a sheaf of the firstfruits of your harvest unto the priest: and he shall wave the sheaf before the LORD"</em> (<em>Leviticus 23:10-11</em>). Christ is the firstfruits of resurrection (<em>1 Corinthians 15:20</em>) on the very day the <em>omer</em> was waved. Second, the <em>omer</em> is a small dry-measure unit (one-tenth of an ephah) — the daily portion of manna gathered in the wilderness: <em>"Gather of it every man according to his eating, an omer for every man"</em> (<em>Exodus 16:16</em>). The forty-nine days from <em>omer</em>-of-firstfruits to Pentecost are called "counting the omer."</p>'
    ),
    'sackcloth-ashes': (
        '<p>Sackcloth and ashes is Scripture’s combined sign of profound grief or repentance. <em>Sackcloth</em> (Hebrew <em>saq</em>) was a coarse, dark, scratchy garment of goat-hair worn next to the skin — visibly uncomfortable, deliberately humiliating. <em>Ashes</em> were scattered on the head or sat in. The pair appears together repeatedly: Mordecai when Haman’s decree was published (<em>Esther 4:1-3</em>); Daniel seeking the LORD over the seventy years (<em>Daniel 9:3</em>); Job repenting at the end of his trial (<em>Job 42:6</em>); the king of Nineveh upon Jonah’s preaching (<em>Jonah 3:6-9</em>). The combination physicalizes what mourning words alone can hide. The body’s discomfort joins the soul’s grief. Western Christianity should recover the visible signs of repentance — at least within the church year, in Lent.</p>'
    ),
    'salt-covenant': (
        '<p>A salt covenant is an unbreakable agreement marked by the shared eating of salt — the symbol of preservation, purity, and indissoluble bond. Scripture names two salt covenants explicitly. The priesthood given to Aaron is one: <em>"All the heave offerings of the holy things, which the children of Israel offer unto the LORD... it is a covenant of salt for ever before the LORD"</em> (<em>Numbers 18:19</em>). The kingdom given to David is another: <em>"the LORD God of Israel gave the kingdom over Israel to David for ever, even to him and to his sons by a covenant of salt"</em> (<em>2 Chronicles 13:5</em>). Salt does not spoil; salt-covenants do not unravel. The pattern points to Christ — perfect Priest and eternal King — whose covenant is salted with His own blood.</p>'
    ),
    'sin-vs-iniquity': (
        '<p>Scripture uses three different Hebrew nouns for moral wrong, each with its own shade — and modern English flattens all three to "sin," losing the precision. <em>Chatta’at</em> (חַטָּאת) is <em>sin</em> in the sense of <em>missing the mark</em>, falling short of God’s standard — the everyday word for moral failure (<em>Genesis 4:7</em>; <em>Exodus 32:30</em>). <em>Avon</em> (עָוֹן) is <em>iniquity</em> — twistedness, perverse moral crookedness, the inward bent of the fallen nature (<em>Psalm 51:5</em>; <em>Isaiah 53:5</em>). <em>Pesha</em> (פֶּשַׁע) is <em>transgression</em> — rebellion, willful breach of covenant, conscious revolt against the King (<em>Psalm 51:1, 3</em>; <em>Isaiah 53:5, 8</em>). <em>Psalm 32:1-2</em> uses all three at once: <em>"Blessed is he whose transgression [pesha] is forgiven, whose sin [chatta’at] is covered."</em> The gospel covers all three.</p>'
    ),
    'smite': (
        '<p>To <em>smite</em> is to strike with force — and in Scripture it is the verb of the judicial blow. God smote Egypt with the ten plagues (<em>Exodus 12:12, 29</em>); smote the firstborn at Passover; smote Uzzah for touching the ark (<em>2 Samuel 6:7</em>); smote Saul of Tarsus blind on the Damascus road (<em>Acts 9:8</em>); smote Herod Agrippa I with worms for accepting divine acclaim (<em>Acts 12:23</em>). Yet the most decisive smiting in Scripture fell on Christ Himself at the cross: <em>"yet we did esteem him stricken, smitten of God, and afflicted... he was wounded for our transgressions, he was bruised for our iniquities"</em> (<em>Isaiah 53:4-5</em>). Christ was smitten <em>so that</em> the smiting need not fall on us. The judicial blow has already landed.</p>'
    ),
    'thorns': (
        '<p>Thorns are the sharp-pointed growths on plants — and in Scripture they are the first visible sign of the Genesis 3 curse. <em>"Thorns also and thistles shall it bring forth to thee; and thou shalt eat the herb of the field"</em> (<em>Genesis 3:18</em>). They reappear: as the weed that chokes the Word in the third soil of Christ’s parable (<em>Mark 4:7, 18-19</em>); as Paul’s thorn in the flesh (<em>2 Corinthians 12:7</em>); and most pointedly as the crown of thorns pressed mockingly upon the Savior’s head: <em>"And when they had platted a crown of thorns, they put it upon his head"</em> (<em>Matthew 27:29</em>). Christ wore the curse on His brow that He might remove its sting from the ground forever. In the new earth there are no thorns.</p>'
    ),
    'type': (
        '<p>A <em>type</em>, in biblical theology, is a divinely intended foreshadowing in Old Testament history of a New Testament reality — especially of Christ Himself. The corresponding fulfillment is the <em>antitype</em>. <em>"All these things happened unto them for ensamples [Greek <em>typoi</em>]: and they are written for our admonition, upon whom the ends of the world are come"</em> (<em>1 Corinthians 10:11</em>). Types include: Adam (the man, fallen) as the type of the Last Adam (<em>Romans 5:14</em>); Melchizedek priest-king of Salem as the type of Christ (<em>Hebrews 7</em>); Joseph the rejected-then-exalted brother; Moses the deliverer-mediator; the manna; the bronze serpent (<em>John 3:14</em>); the Passover lamb; the temple; David. Christ is the antitype each one points toward — the substance behind every shadow.</p>'
    ),
    'yearning': (
        '<p>Yearning is the deep, often physical, almost involuntary longing of one heart for another — a parent for a lost child, a lover for a beloved, a saint for the presence of God. Scripture treats yearning as a felt, embodied movement: bowels stirred, soul fainting, eyes failing for hope of salvation. Joseph’s <em>"bowels did yearn upon his brother"</em> when he first saw Benjamin in Egypt (<em>Genesis 43:30</em>). The Psalmist: <em>"My soul fainteth for thy salvation... mine eyes fail for thy word"</em> (<em>Psalm 119:81-82</em>); <em>"My soul thirsteth for God, for the living God: when shall I come and appear before God?"</em> (<em>Psalm 42:2</em>). Christ longed over Jerusalem (<em>Matthew 23:37</em>); Paul yearned for the Philippians <em>"in the bowels of Jesus Christ"</em> (<em>Philippians 1:8</em>). Holy yearning is permitted and good.</p>'
    ),
    'yhwh-nissi': (
        '<p><em>YHWH-Nissi</em> (יְהוָה נִסִּי) — "the LORD is my banner" — is the covenant name Moses gave the altar he built after Israel’s victory over Amalek at Rephidim (<em>Exodus 17:14-16</em>). A <em>nes</em> ("banner, standard, ensign") was a military rallying-point — a tall flag visible across the battlefield around which the troops gathered. Moses’ declaration is twofold: YHWH Himself is the rallying point of His people’s warfare, and YHWH is the cause of every victory His armies win. The banner declares whose army this is. Isaiah extends the imagery to the Messiah: <em>"there shall be a root of Jesse, which shall stand for an ensign [nes] of the people; to it shall the Gentiles seek"</em> (<em>Isaiah 11:10</em>). Christ is the banner; gather around Him.</p>'
    ),
    'bar-jesus': (
        '<p>Bar-Jesus — also called Elymas the sorcerer — was a Jewish false prophet attached to the household of the Roman proconsul Sergius Paulus on Cyprus (<em>Acts 13:6-12</em>). When Sergius Paulus, <em>"a prudent man"</em>, called for Barnabas and Saul to hear the word of God, Bar-Jesus resisted them, seeking to turn the proconsul away from the faith. Saul, <em>"filled with the Holy Ghost"</em>, set his eyes on him and pronounced judgment: <em>"O full of all subtilty and all mischief, thou child of the devil, thou enemy of all righteousness, wilt thou not cease to pervert the right ways of the Lord? And now, behold, the hand of the Lord is upon thee, and thou shalt be blind"</em>. Bar-Jesus was struck blind; the proconsul believed. From this scene forward, Luke calls the apostle by his Roman name: Paul.</p>'
    ),
    'casting-down-crowns': (
        '<p>"Casting down crowns" is the worship-act of the twenty-four elders around the throne in <em>Revelation 4:9-11</em>. At every fresh sight of the One enthroned, the elders <em>"fall down before him that sat on the throne, and worship him that liveth for ever and ever, and cast their crowns before the throne, saying, Thou art worthy, O Lord, to receive glory and honour and power: for thou hast created all things, and for thy pleasure they are and were created."</em> The crowns (<em>stephanoi</em>, victors’ crowns) represent every reward they have received from God. The gesture declares: <em>all reward, all victory, all rank ultimately belong to Him.</em> Heaven knows no permanent ranking among saints — every crown ends up at the feet of the Lamb. Earth should rehearse it now.</p>'
    ),
    'desert': (
        '<p>The desert (Hebrew <em>midbar</em>, Greek <em>erēmos</em>) is the uninhabited or barely-inhabited dry land — and Scripture loads it with theological freight. It is the place of testing: Israel forty years (<em>Deuteronomy 8:2</em>) and Christ forty days (<em>Matthew 4:1-11</em>). It is the place of meeting God: Moses at the burning bush (<em>Exodus 3</em>), Israel at Sinai, Elijah at Horeb. It is the place of Spirit-formation: John the Baptist before his public ministry (<em>Luke 1:80</em>), Paul’s Arabia retreat after his conversion (<em>Galatians 1:17</em>). And it is the place of eschatological reversal: <em>"The wilderness and the solitary place shall be glad for them; and the desert shall rejoice, and blossom as the rose"</em> (<em>Isaiah 35:1</em>). Christian men still need desert seasons.</p>'
    ),
    'ebionitism': (
        '<p>Ebionitism was an early Jewish-Christian sect (named from Hebrew <em>ebyonim</em>, "the poor ones") that denied the deity of Christ and the doctrine of justification by faith alone. They insisted that Jesus was a great human prophet but not God incarnate, and that Gentile converts must still keep the Mosaic law — circumcision, Sabbath, dietary laws — to be justified. Paul combated the same root error in Galatians: <em>"a man is not justified by the works of the law, but by the faith of Jesus Christ"</em> (<em>Galatians 2:16</em>). John, Paul, and Hebrews all affirmed against them what Ebionites denied: <em>"the Word was made flesh"</em> (<em>John 1:14</em>); <em>"in him dwelleth all the fulness of the Godhead bodily"</em> (<em>Colossians 2:9</em>). The Ebionite formula is grace <em>plus</em> works, faith <em>plus</em> merit — and Paul calls it another gospel.</p>'
    ),
    'gospels': (
        '<p>The Gospels are the four canonical accounts of the life, ministry, teaching, death, and resurrection of Jesus Christ — Matthew, Mark, Luke, and John. The first three (the Synoptics) share substantial material and an outline-from-the-same-viewpoint perspective; the fourth (John) supplements with theological depth and several discourses unique to it. The traditional symbolic representations come from the four living creatures of <em>Revelation 4:7</em>: Matthew the lion (kingly), Mark the ox (servant), Luke the man (humanity), John the eagle (divinity). Together they constitute the New Testament’s Christological foundation — the same Lord seen from four divinely inspired angles. They are not biographies in the modern sense but gospels in the original sense: announcements of the King’s saving accomplishment.</p>'
    ),
    'humility-biblical': (
        '<p>Biblical humility is the right estimate of one’s self before God — not falsely low (self-deprecation as virtue-signaling), not falsely high (pride), but accurate. <em>"Let nothing be done through strife or vainglory; but in lowliness of mind let each esteem other better than themselves"</em> (<em>Philippians 2:3</em>). The Christological exemplar follows immediately: <em>"Let this mind be in you, which was also in Christ Jesus: who, being in the form of God... made himself of no reputation, and took upon him the form of a servant, and was made in the likeness of men: and being found in fashion as a man, he humbled himself, and became obedient unto death, even the death of the cross"</em> (<em>Philippians 2:5-8</em>). The saint’s humility is the imprint of Christ’s — descending step by step, willingly, for love.</p>'
    ),
    'jehovah-rohi': (
        '<p><em>Jehovah-Rohi</em> (יְהוָה רֹעִי) — "the LORD is my shepherd" — is the covenant name revealed in <em>Psalm 23:1</em> and embodied in Christ as the good shepherd. David’s opening line is one of the most quoted in the world: <em>"The LORD is my shepherd; I shall not want."</em> The shepherding image runs across Scripture: leading (<em>v. 2</em>), feeding, restoring (<em>v. 3</em>), defending (<em>v. 4</em>), and accompanying through the valley of the shadow of death. <em>Jehovah-Rohi</em> means God Himself takes the role of shepherd to His covenant people. Christ takes the title up directly in <em>John 10:11, 14</em>: <em>"I am the good shepherd: the good shepherd giveth his life for the sheep... I am the good shepherd, and know my sheep, and am known of mine."</em> The Shepherd of Israel is Jesus of Nazareth.</p>'
    ),
    'jephthah': (
        '<p>Jephthah was the ninth judge of Israel — the son of a harlot, driven out by his half-brothers for his birth, and forced to live on the margins of Israelite society. When the Ammonites threatened, the elders of Gilead came begging him to lead them (<em>Judges 11:5-11</em>). He prevailed and delivered Israel — but made a rash vow that whatever came out of his door first to greet him on his victorious return would be offered to the LORD. His only daughter came out (<em>Judges 11:30-40</em>). Scholars dispute whether she was literally sacrificed or perpetually consecrated as a virgin; the text’s grief is plain either way. Yet Jephthah is named in <em>Hebrews 11:32</em>’s great roll of faith. Compromised men, called of God, are still used.</p>'
    ),
    'mephibosheth': (
        '<p>Mephibosheth was the son of Jonathan and grandson of King Saul — lamed in both feet at age five when his nurse fled with him at the news of Saul and Jonathan’s deaths at Mount Gilboa (<em>2 Samuel 4:4</em>). He grew up hidden in Lo-debar ("no pasture") under the patron Machir. Years later, David, having consolidated his kingdom, asked: <em>"Is there yet any that is left of the house of Saul, that I may shew him kindness for Jonathan’s sake?"</em> (<em>2 Samuel 9:1</em>). Mephibosheth was sought out and given a permanent seat at the king’s table — and the restored estate of Saul. The story preaches the gospel: a lame, hidden son of a fallen line is sought out by the King for the sake of His Son, and brought to the table forever.</p>'
    ),
    'palm': (
        '<p>The palm (specifically the date palm, <em>Phoenix dactylifera</em>) is the tall, single-trunked tree that flourishes in the oases and valleys of Israel — and in Scripture it carries four loaded images. First, the emblem of the righteous: <em>"The righteous shall flourish like the palm tree"</em> (<em>Psalm 92:12</em>). Second, the carved ornament of Solomon’s temple, on doors, walls, and pillars (<em>1 Kings 6:29, 32, 35</em>). Third, the branch waved before Christ at the Triumphal Entry: <em>"Took branches of palm trees, and went forth to meet him"</em> (<em>John 12:13</em>) — fulfilling the prophesied Hosanna of <em>Psalm 118:25-26</em>. Fourth, the symbol of victory held by the great multitude of the redeemed: <em>"clothed with white robes, and palms in their hands"</em> (<em>Revelation 7:9</em>). Palm marks every coronation of the King.</p>'
    ),
    'post-of-duty': (
        '<p>A post of duty is the placement at which one’s appointed obligation is performed. Scripture knows the concept by office. The priest had his daily course (<em>Luke 1:8-9</em>), the Levite his service, the watchman his wall, the gatekeeper his door, the soldier his rank, the elder his oversight, the deacon his table-service. <em>"Wherefore stand having your loins girt about with truth"</em> (<em>Ephesians 6:14</em>) — stand at your post. The faithful saint and the faithful Marine share an instinct: the post is the place you do not abandon, no matter how dull, dangerous, or thankless. Faithfulness is not romantic; it is showing up on the wall, in the watch, at the assigned hour — every morning, until relieved.</p>'
    ),
    'premillennial': (
        '<p>Premillennialism is the eschatological view that Christ returns bodily <em>before</em> the thousand-year reign described in <em>Revelation 20:1-6</em>. Christ’s return is therefore the <em>inaugurating</em> event of the millennium, not its capstone (postmillennialism) or its already-present spiritual reality (amillennialism). The view subdivides. Historic premillennialism (Justin Martyr, Irenaeus, George Eldon Ladd) holds that the church goes through the great tribulation before Christ’s return. Dispensational premillennialism (J. N. Darby, the Scofield Reference Bible) adds a secret pre-tribulation rapture of the church distinct from Israel’s program. Reformed and confessional Protestants typically hold amillennial or postmillennial views, but premillennialism has ancient roots and serious modern defenders. Whichever view: Christ returns; the millennium serves His glory.</p>'
    ),
    'providence': (
        '<p>Divine providence is the governance of God by which He, with wisdom and love, cares for and directs all things in the universe — visible and invisible, great and small, present and future. The Westminster Shorter Catechism defines it: <em>"God’s works of providence are, his most holy, wise, and powerful preserving and governing all his creatures, and all their actions"</em> (Q.11). It is the outworking of His sovereignty — He upholds (<em>Hebrews 1:3</em>), directs (<em>Proverbs 16:9</em>), and governs (<em>Ephesians 1:11</em>) all creatures and all events for His glory and the good of His people. <em>"And we know that all things work together for good to them that love God, to them who are the called according to his purpose"</em> (<em>Romans 8:28</em>).</p>'
    ),
    'shadow-wings': (
        '<p>The "shadow of His wings" is one of the most tender recurring images of YHWH’s protection in the Psalter — chicks gathered safely under the hen, the saint hidden under the wing of the Almighty. Boaz uses the image of Ruth the Moabitess: <em>"The LORD recompense thy work, and a full reward be given thee of the LORD God of Israel, under whose wings thou art come to trust"</em> (<em>Ruth 2:12</em>). David repeats it: <em>"keep me as the apple of the eye, hide me under the shadow of thy wings"</em> (<em>Psalm 17:8</em>; cf. <em>36:7; 57:1; 61:4; 63:7</em>). Christ Himself takes up the image lamenting Jerusalem: <em>"how often would I have gathered thy children together, even as a hen gathereth her chickens under her wings, and ye would not!"</em> (<em>Matthew 23:37</em>).</p>'
    ),
    'shaking-dust-feet': (
        '<p>Shaking the dust off the feet is the gesture Christ commanded His apostles to perform in towns that refused them: <em>"And whosoever shall not receive you, nor hear your words, when ye depart out of that house or city, shake off the dust of your feet. Verily I say unto you, It shall be more tolerable for the land of Sodom and Gomorrha in the day of judgment, than for that city"</em> (<em>Matthew 10:14-15</em>; <em>Mark 6:11</em>; <em>Luke 9:5; 10:11</em>). It was a public, unmistakable sign that the messengers had finished their errand and the responsibility now lay on the unbelieving city — a Jewish gesture against pagan territory now reversed against unrepentant Jews. Paul and Barnabas did it at Antioch of Pisidia (<em>Acts 13:51</em>). Evangelism has an end; rejection has a verdict.</p>'
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
