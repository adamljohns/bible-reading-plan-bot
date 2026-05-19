#!/usr/bin/env python3
"""Batch 28 — expand 25 more thin entries to 90-110 words each.

Targets: doctrines, slang/cultural reframes, biblical imagery,
Hebrew vocabulary, OT figures, and shepherd imagery from the
30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'ascension-doctrine': (
        '<p>The Ascension is the doctrinal fact that forty days after His resurrection, the Lord Jesus, in His glorified human body, was visibly taken up into heaven from the disciples’ sight at the Mount of Olives (<em>Acts 1:9-11</em>; <em>Luke 24:50-53</em>). He entered the Holy Place not made with hands to appear in the presence of God for us (<em>Hebrews 9:24</em>), there to reign and intercede until He shall so come in like manner. The Ascension is not a disappearance but an enthronement: Christ is now seated at the right hand of God, having all authority in heaven and on earth (<em>Matthew 28:18</em>; <em>Ephesians 1:20-22</em>). The Christian creed confesses it; the church awaits His return on the same terms.</p>'
    ),
    'cope': (
        '<p>"Cope" — to manage or endure — has been twisted in online slang into <em>copium</em>, a dismissive label deployed to name another person’s reasoning as drug-like denial of reality. The accusation is rarely friendly; it functions as a conversational kill-switch. Scripture has a richer and harder category: <em>hypomonē</em>, "remaining-under," the Christian endurance that is not denial but faith rooted in the resurrection. <em>"Tribulation worketh patience; and patience, experience; and experience, hope"</em> (<em>Romans 5:3-4</em>). "Cope" alone — gritted-teeth survival without God — is not a biblical category; biblical endurance always has Christ at its anchor and resurrection at its horizon. The Christian does not <em>cope</em>; he <em>endures unto the end</em>.</p>'
    ),
    'cup-overflows': (
        '<p>"My cup runneth over" is <em>Psalm 23:5</em>’s image of YHWH as Host whose pour for the saint exceeds the cup’s capacity. The Hebrew <em>revayah</em> means saturation, fullness, abundance — the cup is not merely topped up but spills over the rim onto the table. The Shepherd of <em>v. 1-4</em> is now seen as the Host: <em>"Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over."</em> The table is set in plain view of enemies who cannot interfere. The oil is the anointing of welcome. The cup overflows because the Host’s generosity exceeds the guest’s capacity. The Christian life under YHWH is not subsistence; it is abundance.</p>'
    ),
    'dancing-before-lord': (
        '<p>Dancing before the LORD is the embodied, public, sometimes uninhibited expression of joy at His salvation. David <em>"danced before the LORD with all his might"</em> when the ark returned to Jerusalem (<em>2 Samuel 6:14</em>) — and was rebuked by his wife Michal, who despised him in her heart and was struck barren for it. Miriam led the women in dance after the Red Sea: <em>"Sing ye to the LORD, for he hath triumphed gloriously"</em> (<em>Exodus 15:20-21</em>). The Psalms repeatedly call God’s people to <em>"Praise him with the timbrel and dance"</em> (<em>Psalm 149:3; 150:4</em>). Embodied praise is not optional — it is the natural overflow of redeemed joy. Cultured restraint is sometimes Michal-shaped.</p>'
    ),
    'fear-not': (
        '<p>"Fear not" is the most frequently spoken divine command in Scripture. It is spoken to Abraham: <em>"Fear not, Abram: I am thy shield, and thy exceeding great reward"</em> (<em>Genesis 15:1</em>); to Israel at the Red Sea: <em>"Fear ye not, stand still, and see the salvation of the LORD"</em> (<em>Exodus 14:13</em>); to Joshua: <em>"be not afraid, neither be thou dismayed: for the LORD thy God is with thee"</em> (<em>Joshua 1:9</em>); to Mary, the shepherds, the disciples in the storm, the women at the tomb. The grounding is always the same: not "you have nothing to fear" but "I am with thee." Christian courage is not the absence of danger but the presence of God in it.</p>'
    ),
    'former-rain-latter-rain': (
        '<p>The former and latter rains are the two distinct rainy seasons of the Mediterranean Levant. The <em>former rain</em> falls in autumn (October-November), softening the sun-baked ground for plowing and planting; the <em>latter rain</em> falls in spring (March-April), swelling the grain on the stalk just before harvest. Israel’s agricultural year hung on both. Moses promised them as covenant blessing for obedience: <em>"I will give you the rain of your land in his due season, the first rain and the latter rain"</em> (<em>Deuteronomy 11:14</em>). The prophets made them an emblem of Spirit-outpouring: <em>"he will cause to come down for you the rain, the former rain, and the latter rain"</em> (<em>Joel 2:23</em>; cf. <em>Hosea 6:3</em>; <em>James 5:7</em>). Spiritual harvest also requires two seasons of grace.</p>'
    ),
    'girlboss': (
        '<p>"Girlboss" was the self-branded ambitious-woman-entrepreneur archetype that peaked as feminist aspiration in the 2010s and crashed in critique-fodder when several prominent girlbosses’ empires collapsed amid documented harsh treatment of (often female) employees. The slang now functions sardonically. Scripture is not silent on capable, industrious women: the Proverbs 31 wife runs a household, plants vineyards, and provides for her servants; Lydia is a businesswoman and seller of purple (<em>Acts 16:14-15</em>); Priscilla teaches doctrine alongside her husband Aquila (<em>Acts 18:26</em>). But Scripture binds women’s work to godly character — submission to her husband, care for her household, fear of the LORD — not self-branding. The Christian alternative is the wife of valor, not the girlboss.</p>'
    ),
    'locust': (
        '<p>The locust is a migratory swarming insect that God deploys throughout Scripture as an instrument of national judgment. The eighth plague of Egypt was a locust swarm so dense it darkened the land (<em>Exodus 10:1-20</em>). Joel’s prophecy makes locust devastation the lens through which the great Day of the LORD is foreseen — and through which restoration is promised: <em>"I will restore to you the years that the locust hath eaten"</em> (<em>Joel 2:25</em>). John the Baptist ate locusts and wild honey in the wilderness (<em>Matthew 3:4</em>) — a permitted food under <em>Leviticus 11:22</em>. The fifth trumpet of Revelation releases demonic locusts upon the earth (<em>Revelation 9:1-11</em>). Where the LORD speaks, locusts come or go on His word.</p>'
    ),
    'multiply': (
        '<p>To <em>multiply</em> is to increase greatly — and Scripture loads the verb with covenant freight. It is the creation mandate: <em>"Be fruitful, and multiply, and replenish the earth, and subdue it"</em> (<em>Genesis 1:28</em>) — repeated to Noah (<em>9:1</em>) as the post-flood charter. It is the Abrahamic promise: <em>"in blessing I will bless thee, and in multiplying I will multiply thy seed as the stars of the heaven"</em> (<em>Genesis 22:17</em>). It is the early church’s growth: <em>"the word of God grew, and the number of the disciples multiplied in Jerusalem greatly"</em> (<em>Acts 6:7</em>); <em>"And the churches... were multiplied"</em> (<em>Acts 9:31</em>). God’s characteristic blessing is not addition but multiplication. He multiplies seed, sheep, souls, and saints.</p>'
    ),
    'nebuchadnezzar': (
        '<p>Nebuchadnezzar II was the great Babylonian king (605-562 BC) who conquered Jerusalem in three campaigns (605, 597, 586 BC), destroyed Solomon’s temple, and deported Judah to Babylon. He is the central figure of <em>Daniel 1-4</em>: his dream of the colossal statue (Daniel’s interpretation predicting the succession of four world empires, <em>ch. 2</em>); his erection of the ninety-foot golden image and the fiery furnace into which Shadrach, Meshach, and Abednego were thrown (<em>ch. 3</em>); his dream of the great tree, his seven years of bestial madness, and his restoration. His final confession is one of the most extraordinary in Scripture: <em>"those that walk in pride he is able to abase"</em> (<em>Daniel 4:37</em>). Even the king of kings of his age bows.</p>'
    ),
    'priesthood-christ': (
        '<p>The priesthood of Christ is His permanent priestly office — distinct from Aaron’s in five respects. (1) His person: He is the God-man, divine and human. (2) His sacrifice: He offered <em>Himself</em>, once for all, not bulls and goats yearly. (3) His tenure: He continues forever, where Aaron’s sons died and were succeeded. (4) His sanctuary: He entered the true holy place in heaven, not a man-made copy. (5) His order: He is priest after the order of Melchizedek — king-priest forever by divine oath — not after the temporary Levitical order. <em>"Wherefore he is able also to save them to the uttermost that come unto God by him, seeing he ever liveth to make intercession for them"</em> (<em>Hebrews 7:25</em>).</p>'
    ),
    'ram': (
        '<p>The ram (adult male sheep) recurs throughout Scripture in roles that all rehearse Christ. The ram caught in the thicket on Moriah was the substitute God provided for Isaac: <em>"And Abraham lifted up his eyes, and looked, and behold behind him a ram caught in a thicket by his horns: and Abraham went and took the ram, and offered him up for a burnt offering in the stead of his son"</em> (<em>Genesis 22:13</em>). The ram of consecration was offered when Aaron and his sons were ordained to the priesthood (<em>Exodus 29:15-28</em>). The ram’s horn (<em>shofar</em>) announced atonement, war, and the Year of Jubilee. Every ram in Scripture is a rehearsal of the Substitute — Christ, caught for us.</p>'
    ),
    'raven': (
        '<p>The raven is a large black bird of the corvid family — declared unclean under Levitical law (<em>Leviticus 11:15</em>; <em>Deuteronomy 14:14</em>), yet repeatedly used by God in surprising service. Noah sent a raven out from the ark first; it flew to and fro until the waters were abated (<em>Genesis 8:7</em>). YHWH commanded the ravens to feed Elijah by the brook Cherith — bread and flesh morning and evening (<em>1 Kings 17:4-6</em>). Christ used ravens to teach His disciples to trust the Father: <em>"Consider the ravens: for they neither sow nor reap; which neither have storehouse nor barn; and God feedeth them: how much more are ye better than the fowls?"</em> (<em>Luke 12:24</em>). God feeds His servants by clean and unclean alike.</p>'
    ),
    'reed': (
        '<p>The reed is a tall hollow grass of marshes and riverbanks — and in Scripture it becomes the figure both of the easily shaken and of the gently treated. Christ asked the crowds about John: <em>"What went ye out into the wilderness to see? A reed shaken with the wind?"</em> (<em>Matthew 11:7</em>) — implying that John was no such thing. James warns: <em>"He that wavereth is like a wave of the sea driven with the wind and tossed"</em> (<em>James 1:6</em>) — same image, same diagnosis. Yet Isaiah promises of the Servant: <em>"A bruised reed shall he not break, and the smoking flax shall he not quench"</em> (<em>Isaiah 42:3</em>; <em>Matthew 12:20</em>). The same Greek word names the measuring rod of the New Jerusalem (<em>Revelation 21:15</em>).</p>'
    ),
    'rent-free': (
        '<p>"Living rent-free" is the slang phrase dismissively used to name someone’s preoccupation with another person or idea as wasted mental real estate — <em>"that guy is living rent-free in your head."</em> The phrase is rhetorically deployed to belittle the obsession, not to address it. Scripture diagnoses what occupies the heart as worship-direction: whatever fills the mind is being granted authority. Christ says, <em>"out of the abundance of the heart the mouth speaketh"</em> (<em>Matthew 12:34</em>). The remedy is not lighter mental load (mere distraction) but reclaimed allegiance: <em>"bringing into captivity every thought to the obedience of Christ"</em> (<em>2 Corinthians 10:5</em>). What lives rent-free in your mind is what is actually ruling you. Evict it.</p>'
    ),
    'return-yhwh': (
        '<p>"Return to the LORD" is the prophetic call par excellence — turn back to YHWH from idols, sin, exile, or indifference. The Hebrew verb <em>shuv</em> ("turn") is used hundreds of times and is the standard word for repentance: <em>"Return unto me, and I will return unto you, saith the LORD of hosts"</em> (<em>Malachi 3:7</em>); <em>"Turn ye, turn ye from your evil ways; for why will ye die, O house of Israel?"</em> (<em>Ezekiel 33:11</em>); <em>"Take with you words, and turn to the LORD: say unto him, Take away all iniquity, and receive us graciously"</em> (<em>Hosea 14:2</em>). <em>Shuv</em> is the two-way verb of covenant restoration — God returning to us as we return to Him. Every reformation begins with this word.</p>'
    ),
    'river': (
        '<p>The river, in Scripture, is a recurring mark of God’s presence and provision. Eden had four rivers flowing out from the garden — Pishon, Gihon, Hiddekel (Tigris), and Euphrates (<em>Genesis 2:10-14</em>). The Chebar was the river by which Ezekiel saw the throne-chariot vision while in Babylonian exile (<em>Ezekiel 1:1, 3</em>). Ezekiel’s temple vision climaxed in a river flowing from under the threshold of the sanctuary, swelling to ankles, knees, waist, and finally a river too deep to cross (<em>Ezekiel 47:1-12</em>). Revelation gathers the imagery: <em>"a pure river of water of life, clear as crystal, proceeding out of the throne of God and of the Lamb"</em> (<em>Revelation 22:1</em>). Rivers are where God meets His people, beginning to end.</p>'
    ),
    'soft-answer': (
        '<p>The soft answer is the verse-encoded wisdom of <em>Proverbs 15:1</em>: <em>"A soft answer turneth away wrath: but grievous words stir up anger."</em> It is the discipline of choosing the gentle word in heated conversation — measured, low-toned, careful. Not weakness but tactical wisdom: soft answers de-escalate; sharp answers escalate. The verb <em>"turneth away"</em> shows the soft answer doing real work — bending the trajectory of anger before it lands. Solomon’s court taught his sons to govern by this. Modern public speech, talk radio, social media, and many family arguments are all losing wars on this front. Christian husbands and fathers learn it early or pay for it long. The soft answer is masculine restraint, not femininity.</p>'
    ),
    'soft-launch': (
        '<p>"Soft launch" is the modern social-media practice of revealing a romantic relationship through indirect cues — a hand in a photo, a back-of-head shot, an unidentified figure beside a meal — rather than explicit announcement. The practice trades the risk of public commitment for the safety of plausible deniability: if things end, no one needs to be told. Scripture knows none of this. Biblical covenant relationships are public commitments. Marriages have witnesses; vows are heard; the bride is brought out openly (<em>Genesis 24:65-67; 29:21-22</em>); the wedding is a feast. The "soft launch" represents a culture afraid to commit publicly. Christian men should propose plainly, marry openly, and walk visibly with their wives — no soft launches.</p>'
    ),
    'springs-living-water': (
        '<p>"Springs of living water" — or more precisely, "the fountain of living waters" — is YHWH’s self-description in Jeremiah’s great covenant indictment: <em>"For my people have committed two evils; they have forsaken me the fountain of living waters, and hewed them out cisterns, broken cisterns, that can hold no water"</em> (<em>Jeremiah 2:13</em>). The imagery contrasts the inexhaustible flowing spring (the LORD Himself) with the cracked, manmade cistern (every idol substitute). Christ takes up the imagery with the Samaritan woman: <em>"the water that I shall give him shall be in him a well of water springing up into everlasting life"</em> (<em>John 4:14</em>); and at the Feast of Tabernacles: <em>"out of his belly shall flow rivers of living water"</em> (<em>John 7:38</em>). Drink at the Spring.</p>'
    ),
    'stan': (
        '<p>"Stan" — slang derived from Eminem’s 2000 song — names intense, often public devotion to a celebrity, product, fictional character, athlete, or idea. The vocabulary treats this disposition as harmless enthusiasm (<em>"I stan that artist"</em>). Scripture treats it as something heavier: the architecture of the human heart is built to worship, and it will pour itself into <em>something</em> — God, or idol. <em>"Little children, keep yourselves from idols. Amen"</em> (<em>1 John 5:21</em>) is the closing word of the apostle of love. The only question is what we stan. Christ alone is worthy of the disposition the slang flippantly throws at musicians and ballplayers. Reorder it. Stan the King.</p>'
    ),
    'tefillin': (
        '<p><em>Tefillin</em> (Greek <em>phylacteries</em>) are the small leather boxes — one for the forehead, one for the arm — containing four key Torah passages on parchment: <em>Exodus 13:1-10; 13:11-16</em>; <em>Deuteronomy 6:4-9; 11:13-21</em>. They are bound on the head and the left arm during morning prayer in literal obedience to <em>Deuteronomy 6:8</em>: <em>"And thou shalt bind them for a sign upon thine hand, and they shall be as frontlets between thine eyes."</em> Jesus rebuked the Pharisees for enlarging their phylacteries to be seen of men (<em>Matthew 23:5</em>), not for wearing them. The deeper command is <em>internal</em>: the Word bound to hand (deed) and forehead (thought) is the believer’s vocation. <em>Tefillin</em> in the soul, not just the strap.</p>'
    ),
    'thanksgiving': (
        '<p>Thanksgiving is the deliberate offering of thanks to God for His mercies, gifts, and faithfulness — commanded explicitly: <em>"In every thing give thanks: for this is the will of God in Christ Jesus concerning you"</em> (<em>1 Thessalonians 5:18</em>) — and practiced continually as a hallmark of the Spirit-filled life: <em>"Giving thanks always for all things unto God and the Father in the name of our Lord Jesus Christ"</em> (<em>Ephesians 5:20</em>). The Greek root <em>eucharisteō</em> ("to give thanks") names the Lord’s Supper itself: <em>Eucharist</em>, the Great Thanksgiving. Christian thanksgiving is therefore not seasonal sentimentality but the ongoing posture of the redeemed soul — flowing back upward to God for every breath of life received from His open hand.</p>'
    ),
    'truthfulness': (
        '<p>Truthfulness is the saint’s disposition of speaking and dealing in accordance with what is. Paul’s command is direct: <em>"Wherefore putting away lying, speak every man truth with his neighbour: for we are members one of another"</em> (<em>Ephesians 4:25</em>). The ninth commandment forbids false witness (<em>Exodus 20:16</em>); Christ commands plain yes-and-no speech (<em>Matthew 5:37</em>); John writes that liars have no part in the New Jerusalem (<em>Revelation 21:8, 27; 22:15</em>). Christ called Himself <em>"the way, the truth, and the life"</em> (<em>John 14:6</em>); the saint’s tongue is to bear the same family resemblance. In an age of practiced spin and managed narratives, the Christian must be marked by an unfashionable, sometimes costly honesty. Truth is not negotiable.</p>'
    ),
    'tsur': (
        '<p><em>Tsur</em> (צוּר) is the Hebrew word for <em>rock</em> — specifically the great cliff-face, the strong-rock, the immovable foundation. It is distinct from <em>even</em> ("stone"), which can be small or carried. <em>Tsur</em> is used repeatedly as a divine title: <em>"He is the Rock, his work is perfect: for all his ways are judgment: a God of truth and without iniquity, just and right is he"</em> (<em>Deuteronomy 32:4</em>); <em>"The LORD is my rock, and my fortress, and my deliverer"</em> (<em>2 Samuel 22:2</em>); <em>"my rock, in whom I will trust"</em> (<em>Psalm 18:2</em>). Paul identifies the wilderness <em>tsur</em> with Christ: <em>"that spiritual Rock that followed them: and that Rock was Christ"</em> (<em>1 Corinthians 10:4</em>).</p>'
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
