#!/usr/bin/env python3
"""Batch 35 — expand 25 more entries from the 50-60 word bucket.

Targets: NT geography, NT figures, apologetics, doctrines, divine
names, OT figures, body gestures, and discipleship vocabulary.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'cana': (
        '<p>Cana was the Galilean village where Christ began His public ministry by turning water into wine at a wedding feast (<em>John 2:1-11</em>) — the first of seven signs in John’s Gospel: <em>"This beginning of miracles did Jesus in Cana of Galilee, and manifested forth his glory; and his disciples believed on him."</em> He returned to Cana to heal the nobleman’s son at a distance (<em>John 4:46-54</em>), the second sign. Nathanael (Bartholomew) was a native of Cana (<em>John 21:2</em>). The choice of a wedding for the inaugural miracle is theologically loaded: the Bridegroom has come, the wine of the kingdom is poured out, the wedding-supper is being prepared.</p>'
    ),
    'chastening': (
        '<p>Chastening is the Father’s loving discipline of His own children — not punitive wrath (Christ absorbed that on the cross) but corrective shaping aimed at producing holiness. <em>Hebrews 12:5-11</em> is the classic passage: <em>"My son, despise not thou the chastening of the Lord, nor faint when thou art rebuked of him: For whom the Lord loveth he chasteneth, and scourgeth every son whom he receiveth."</em> Chastening is the proof of sonship, not its negation: <em>"If ye endure chastening, God dealeth with you as with sons; for what son is he whom the father chasteneth not?"</em> (<em>v. 7</em>). It is painful for the present but afterward yields <em>"the peaceable fruit of righteousness unto them which are exercised thereby"</em>.</p>'
    ),
    'classical-apologetics': (
        '<p>Classical Apologetics defends the faith by a two-step argument. First, it establishes <em>theism</em> — that God exists — through the classical proofs: the cosmological argument (every effect has a cause), the teleological (design implies a designer), the moral (objective moral law requires a Lawgiver), and the ontological (a maximally great being exists). Second, it establishes <em>Christian</em> theism specifically — that this God has revealed Himself in Christ — through historical evidence for the deity and resurrection of Jesus. Major proponents include Norman Geisler, R. C. Sproul, William Lane Craig, J. P. Moreland, and substantially C. S. Lewis. Distinct from presuppositional apologetics (Van Til, Bahnsen), which begins with biblical authority as the only foundation for valid reasoning.</p>'
    ),
    'drunkenness': (
        '<p>Drunkenness is the sin of habitual or excessive intoxication — named explicitly in the works-of-the-flesh lists: <em>"drunkenness, revellings, and such like"</em> (<em>Galatians 5:21</em>); <em>"not in rioting and drunkenness"</em> (<em>Romans 13:13</em>); <em>"And be not drunk with wine, wherein is excess"</em> (<em>Ephesians 5:18</em>). It disqualifies a man from the eldership: <em>"not given to wine"</em> (<em>1 Timothy 3:3</em>; <em>Titus 1:7</em>). Scripture distinguishes drunkenness (sin) from wine itself — Christ’s first miracle produced 120 to 180 gallons of fine wine for a wedding (<em>John 2:6-10</em>), and the Lord’s cup is wine. The line is sobriety; the sin is loss of self-control. <em>"It is not for kings, O Lemuel... to drink wine; nor for princes strong drink"</em> (<em>Proverbs 31:4</em>).</p>'
    ),
    'economic-justice': (
        '<p>Biblical economic justice protects property while commanding generosity and care for the vulnerable. God forbids theft: <em>"Thou shalt not steal"</em> (<em>Exodus 20:15</em>). He forbids oppression of the poor: <em>"Rob not the poor, because he is poor: neither oppress the afflicted in the gate"</em> (<em>Proverbs 22:22-23</em>). He forbids dishonest weights: <em>"A false balance is abomination to the LORD: but a just weight is his delight"</em> (<em>Proverbs 11:1</em>). He forbids withholding wages: <em>"the hire of the labourers... is of you kept back by fraud, crieth"</em> (<em>James 5:4</em>). Mosaic Law included gleaning rights for the poor, the sabbatical debt-release, and the Jubilee land-restoration. The biblical model is neither socialism nor unrestrained capitalism — but covenant economics.</p>'
    ),
    'ecstatic-prophecy': (
        '<p>Ecstatic prophecy is prophecy delivered in a state of altered consciousness — the prophet temporarily transported beyond ordinary self-awareness, the Spirit so present that the natural faculties are overrun. Scripture records the phenomenon in several places. Saul stripped off his clothes and prophesied <em>"all that day and all that night"</em> among the company of prophets — twice (<em>1 Samuel 10:10-12; 19:23-24</em>). Balaam fell down with his eyes open, in a trance from the Almighty (<em>Numbers 24:4, 16</em>). Peter fell into a trance on Joppa’s rooftop and received the vision of the sheet (<em>Acts 10:10-16</em>). Paul fell into a trance in the temple (<em>Acts 22:17</em>) and was caught up to the third heaven (<em>2 Corinthians 12:2-4</em>). The state is real, biblical, and rare.</p>'
    ),
    'euodia': (
        '<p>Euodia was a Christian sister at Philippi whom Paul names alongside Syntyche in his closing exhortation: <em>"I beseech Euodias, and beseech Syntyche, that they be of the same mind in the Lord. And I intreat thee also, true yokefellow, help those women which laboured with me in the gospel, with Clement also, and with other my fellowlabourers, whose names are in the book of life"</em> (<em>Philippians 4:2-3</em>). Paul testifies that they had labored with him in the gospel — apparently in significant ministry — yet some disagreement had divided them. Paul does not take sides; he calls both to oneness in the Lord and exhorts a third party (<em>"true yokefellow"</em>) to help reconcile them. Even fruitful gospel workers can be at odds; the church’s call is reconciliation.</p>'
    ),
    'eutychus': (
        '<p>Eutychus was a young man at Troas who, sinking into deep sleep during Paul’s extended midnight discourse on the first day of the week, fell from a third-story window and was taken up dead (<em>Acts 20:7-12</em>). Paul went down, embraced him, and declared <em>"his life is in him"</em>; the boy was brought up alive — to no small comfort. The narrative preserves a wry humor (Paul preached so long the boy slept) and a clear miracle (the boy was dead). Luke specifies the meeting day (<em>"the first day of the week"</em>) and the purpose (<em>"to break bread"</em>) — one of the earliest explicit New Testament records of Christian Lord’s Day worship as the church’s settled pattern.</p>'
    ),
    'fiery-darts': (
        '<p>Fiery darts are the flaming arrows of <em>"the wicked"</em>, quenched on the shield of faith in Paul’s armor-of-God passage: <em>"Above all, taking the shield of faith, wherewith ye shall be able to quench all the fiery darts of the wicked"</em> (<em>Ephesians 6:16</em>). Roman warfare actually used such weapons: arrows wrapped in pitch-soaked cloth and lit before being shot — designed to burn through wood and demoralize the troops, not merely wound. The shield (Greek <em>thureos</em>, the long body-shield, often leather-covered and water-soaked to extinguish fire) absorbed them. The metaphor names the devil’s lies, accusations, temptations, and despair-injections as deliberate incendiary attacks. Faith in Christ — trust on His promises — extinguishes them.</p>'
    ),
    'fruit-bearing': (
        '<p>Fruit-bearing is the visible production of life-evidence in the saint’s walk — the Spirit’s fruit (<em>Galatians 5:22-23</em>), the abiding-in-Christ fruit (<em>John 15:5</em>: <em>"He that abideth in me, and I in him, the same bringeth forth much fruit"</em>), the good fruit of repentance (<em>Matthew 3:8</em>). Christ’s diagnostic is plain: <em>"By their fruits ye shall know them"</em> (<em>Matthew 7:16, 20</em>). Fruit is diagnostic and largely unfakable — what a man’s life produces over time reveals the root. Fruitlessness brings the Father’s pruning shears: <em>"Every branch in me that beareth not fruit he taketh away: and every branch that beareth fruit, he purgeth it, that it may bring forth more fruit"</em> (<em>John 15:2</em>). Bear fruit; expect pruning.</p>'
    ),
    'goodness': (
        '<p>Goodness is moral excellence active in benefit toward others — not merely the absence of evil, but the positive presence of generous, doing-good. It is listed in the fruit of the Spirit: <em>"But the fruit of the Spirit is love, joy, peace, longsuffering, gentleness, goodness, faith"</em> (<em>Galatians 5:22</em>) and in <em>"the fruit of the Spirit is in all goodness and righteousness and truth"</em> (<em>Ephesians 5:9</em>). Goodness is God’s own attribute reflected in His people: <em>"O give thanks unto the LORD; for he is good: because his mercy endureth for ever"</em> (<em>Psalm 107:1</em>). Paul commends Barnabas: <em>"For he was a good man, and full of the Holy Ghost and of faith"</em> (<em>Acts 11:24</em>). Christian goodness does what is right and is generous in doing it.</p>'
    ),
    'grief': (
        '<p>Grief is the heavy sorrow of loss — and Scripture neither minimizes nor mocks it. Christ Himself is named <em>"a man of sorrows, and acquainted with grief"</em> (<em>Isaiah 53:3</em>). He groaned in spirit at Lazarus’s tomb and wept (<em>John 11:33-35</em>); He sorrowed unto death in Gethsemane (<em>Matthew 26:38</em>); He sweat as it were great drops of blood in agony (<em>Luke 22:44</em>). Christianity therefore does not promise grief-free life; it promises the Comforter alongside the grieving (<em>John 14:16-18</em>). <em>"Blessed are they that mourn: for they shall be comforted"</em> (<em>Matthew 5:4</em>). Paul writes the Thessalonians: <em>"sorrow not, even as others which have no hope"</em> (<em>1 Thessalonians 4:13</em>) — Christians grieve, but with hope.</p>'
    ),
    'hebraic-calendar': (
        '<p>The Hebraic calendar is the lunisolar calendar of the Mosaic law — still used liturgically by Jews and indispensable to understanding biblical chronology. Twelve lunar months (each beginning at new moon, about 29.5 days) make up roughly 354 days; a thirteenth month (Adar II / Veadar) is intercalated in seven of every nineteen years to keep the calendar synchronized with the solar year. The religious year begins in Nisan (March-April, with Passover on the 14th), counting forward to Tishri (September-October); the civil year begins in Tishri (with Rosh Hashanah on the 1st). The major feasts cluster: Passover, Unleavened Bread, Firstfruits, Weeks (Pentecost), Trumpets, Atonement, Tabernacles. Christ fulfills the feast cycle in His own coming.</p>'
    ),
    'jehovah-tsidkenu': (
        '<p><em>Jehovah-Tsidkenu</em> (יְהוָה צִדְקֵנוּ) — "the LORD our Righteousness" — is the messianic covenant name Jeremiah twice gives the coming righteous Branch from David’s line: <em>"Behold, the days come, saith the LORD, that I will raise unto David a righteous Branch... and this is his name whereby he shall be called, THE LORD OUR RIGHTEOUSNESS"</em> (<em>Jeremiah 23:5-6; 33:15-16</em>). The New Testament identifies this Branch as Christ Himself — whose perfect righteousness is reckoned (imputed) to His people by faith: <em>"For he hath made him to be sin for us, who knew no sin; that we might be made the righteousness of God in him"</em> (<em>2 Corinthians 5:21</em>). Our righteousness is not ours; it is His given to us — and we wear His name.</p>'
    ),
    'kissing-feet': (
        '<p>Kissing the feet is the most extreme posture of homage, gratitude, or repentance in Scripture — reserved for kings, conquerors, prophets, and ultimately for the Lord Himself. <em>Psalm 2:12</em> commands the kings of the earth to <em>"Kiss the Son, lest he be angry, and ye perish from the way."</em> The sinful woman of <em>Luke 7:36-50</em> washed Jesus’ feet with her tears, wiped them with her hair, and <em>"kissed his feet"</em> — and Christ pronounced her sins forgiven. Mary of Bethany anointed His feet and wiped them with her hair (<em>John 12:3</em>). The kiss of the feet is the body’s most humbling gesture; the soul kneels lower than itself. The bride of Christ approaches the Bridegroom on her face.</p>'
    ),
    'korah': (
        '<p>Korah was a Levite of the Kohathite clan who led a rebellion of 250 Israelite leaders — princes of the assembly, men of renown — against Moses’ and Aaron’s authority in the wilderness (<em>Numbers 16</em>). The accusation was characteristically populist: <em>"Ye take too much upon you, seeing all the congregation are holy, every one of them"</em> (<em>v. 3</em>). The LORD judged Korah and his coalition decisively: the earth opened her mouth and swallowed Korah, his household, and all that pertained to him; fire from the LORD consumed the 250 with their censers (<em>vv. 31-35</em>). Jude names <em>"the gainsaying of Core"</em> (<em>Jude 11</em>) as a perpetual warning against rebellion against God-ordained authority. The pattern is permanent: every Korah eventually meets the same earth.</p>'
    ),
    'leper': (
        '<p>A leper, in biblical usage, is a person afflicted with a Levitically-defined skin disease (broader than modern Hansen’s disease — covering various scaling, discoloring, and weeping skin afflictions). The Mosaic law required exclusion from the camp: <em>"All the days wherein the plague shall be in him he shall be defiled; he is unclean: he shall dwell alone; without the camp shall his habitation be"</em> (<em>Leviticus 13:46</em>). He was to cry <em>"Unclean! Unclean!"</em> when others approached. The leper appears throughout the Gospels as the object of Christ’s most tender and risky compassion: <em>"And Jesus put forth his hand, and touched him, saying, I will; be thou clean. And immediately his leprosy was cleansed"</em> (<em>Matthew 8:3</em>). He touched the unclean, and the disease fled.</p>'
    ),
    'man-of-god': (
        '<p>"Man of God" is an Old Testament title applied to those uniquely commissioned by the LORD — Moses (<em>Deuteronomy 33:1</em>), Samuel (<em>1 Samuel 9:6</em>), David (<em>Nehemiah 12:24</em>), Elijah (<em>1 Kings 17:18</em>), Elisha (<em>2 Kings 4:7</em>), Shemaiah (<em>1 Kings 12:22</em>), and many anonymous prophets identified only by the phrase. The title marks distinguished commission and consistent walk with God. Paul applies it to Timothy: <em>"But thou, O man of God, flee these things; and follow after righteousness, godliness, faith, love, patience, meekness"</em> (<em>1 Timothy 6:11</em>); and again: <em>"That the man of God may be perfect, throughly furnished unto all good works"</em> (<em>2 Timothy 3:17</em>). The title is gendered, vocational, and qualitative — and earned, not self-claimed.</p>'
    ),
    'meekness-strength': (
        '<p>Biblical meekness is reined power — not weakness, not timidity, not absence of conviction. The Greek <em>praotēs</em> in classical use named a war-horse trained to obey the rider’s lightest touch: full strength under perfect control. The same Greek root names the colt Christ rode in the Triumphal Entry (<em>Matthew 21:5</em>). Christ Himself: <em>"I am meek and lowly in heart"</em> (<em>Matthew 11:29</em>). And Moses, the man with two million souls under his hand, is named the meekest man on earth: <em>"Now the man Moses was very meek, above all the men which were upon the face of the earth"</em> (<em>Numbers 12:3</em>). Meek men inherit the earth (<em>Matthew 5:5</em>) because they have not had to seize it.</p>'
    ),
    'moriah': (
        '<p>Mount Moriah is the mountain where Abraham offered Isaac (<em>Genesis 22:1-19</em>) — and where Solomon later built the first temple: <em>"Then Solomon began to build the house of the LORD at Jerusalem in mount Moriah, where the LORD appeared unto David his father"</em> (<em>2 Chronicles 3:1</em>). The geographical convergence is theologically loaded. The place of Abraham’s ram-substitution became the place of Israel’s entire sacrificial system — and ultimately, the place near which Christ the true Lamb of God was crucified. <em>"And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen"</em> (<em>Genesis 22:14</em>). The mountain of provision is the mountain of redemption.</p>'
    ),
    'pearl-price': (
        '<p>The Pearl of Great Price is Christ’s short parable of the kingdom in <em>Matthew 13:45-46</em>: <em>"Again, the kingdom of heaven is like unto a merchant man, seeking goodly pearls: who, when he had found one pearl of great price, went and sold all that he had, and bought it."</em> The merchant is not stumbling on the pearl accidentally — he is searching for fine pearls; he is qualified to recognize one when he sees it. The kingdom of heaven is worth more than all that a man owns; the only adequate response is total liquidation in pursuit of it. <em>"He that hath ears to hear, let him hear"</em> (<em>v. 9</em>). Christian men who have not yet sold all do not yet understand the worth.</p>'
    ),
    'rank-biblical': (
        '<p>Rank, in Scripture, is the ordered position one holds in a formation — the place from which one serves and to which one is accountable. Israel’s twelve tribes camped and marched in rank around the tabernacle: three tribes to each compass-point, the Levites in the middle, Judah leading (<em>Numbers 2</em>). Paul commends the Colossians: <em>"For though I be absent in the flesh, yet am I with you in the spirit, joying and beholding your order, and the stedfastness of your faith in Christ"</em> (<em>Colossians 2:5</em>) — the word is <em>taxis</em>, literally <em>tactical formation</em>. The kingdom of God honors order over disorder, rank over chaos. Christian men should learn to stand at their rank, take orders, give orders, and keep formation under Christ.</p>'
    ),
    'unequally-yoked': (
        '<p>To be unequally yoked is to be harnessed to a partner whose nature, pace, and direction differ so much that the joint pull is destructive to both. The Mosaic law forbade plowing with an ox and an ass together (<em>Deuteronomy 22:10</em>) — different sizes, different paces, different temperaments, both injured. Paul applies the figure: <em>"Be ye not unequally yoked together with unbelievers: for what fellowship hath righteousness with unrighteousness? and what communion hath light with darkness?"</em> (<em>2 Corinthians 6:14</em>). The principle forbids the binding of a believer to an unbeliever in any covenant relationship requiring shared traction — chiefly marriage and ministry partnership. Friendly evangelism remains; covenant union with the unconverted does not.</p>'
    ),
    'womb': (
        '<p>The womb is the maternal organ where God personally forms human life. In Scripture, the womb is far from anonymous tissue or impersonal biology — it is sacred ground. <em>"For thou hast possessed my reins: thou hast covered me in my mother’s womb. I will praise thee; for I am fearfully and wonderfully made"</em> (<em>Psalm 139:13-14</em>); <em>"Before I formed thee in the belly I knew thee; and before thou camest forth out of the womb I sanctified thee"</em> (<em>Jeremiah 1:5</em>). John the Baptist leapt in his mother Elisabeth’s womb at the voice of Mary (<em>Luke 1:41</em>) — recognizing the unborn Christ. Every abortion ends a sacred work-in-progress; every pregnancy is a divine craftsmanship in flesh. Honor the womb.</p>'
    ),
    'yhwh-jireh': (
        '<p><em>YHWH-Jireh</em> (יְהוָה יִרְאֶה) — "the LORD will provide" — is the covenant name Abraham gave to the mountain after God provided the ram caught in the thicket in Isaac’s place: <em>"And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen"</em> (<em>Genesis 22:14</em>). The Hebrew root <em>ra’ah</em> (<em>"to see"</em>) carries both <em>"see"</em> and <em>"see to it"</em> — God provides because God sees ahead. The same mountain (Moriah) became the site of Solomon’s temple and the very ground near which Christ was sacrificed — the ultimate provision of the Lamb in our place. What God showed Abraham in shadow, He fulfilled at Calvary in substance.</p>'
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
