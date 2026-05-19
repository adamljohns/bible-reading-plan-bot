#!/usr/bin/env python3
"""Batch 16 — expand 25 more thin entries to 90-110 words each.

Targets: Beatitude heart-states, divine names, disciplines,
soteriology, ecclesial seasons, and KJV vocabulary from the 30-50
word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'heart-meek': (
        '<p>A meek heart is the disposition Jesus blesses in the third Beatitude: <em>"Blessed are the meek: for they shall inherit the earth"</em> (<em>Matthew 5:5</em>). Meekness (Greek <em>praus</em>) is not weakness, timidity, or doormat passivity — it is strength tamed by God, force bridled, power yielded to His will. The same word describes the colt Christ rode (<em>Matthew 21:5</em>) and Christ Himself: <em>"I am meek and lowly in heart"</em> (<em>Matthew 11:29</em>). Moses was <em>"very meek, above all the men which were upon the face of the earth"</em> (<em>Numbers 12:3</em>) — and led a nation. The meek man inherits the earth because he has refused to seize it. Biblical masculinity wears it well.</p>'
    ),
    'kyrie-eleison': (
        '<p><em>Kyrie eleison</em> ("Lord, have mercy") is the Greek plea that runs through the Psalms (<em>"Have mercy upon me, O God"</em> — <em>Psalm 4:1; 6:2; 41:4; 51:1</em>) and the gospels — the cry of the blind men of Jericho (<em>Matthew 20:30-31</em>), the Canaanite woman (<em>Matthew 15:22</em>), the ten lepers (<em>Luke 17:13</em>), and the publican who beat his breast (<em>Luke 18:13</em>). Early Christian liturgies embedded it as the <em>Kyrie</em>, sung antiphonally near the start of worship. It is a prayer with no pretense — no merit cited, no excuse offered — only a soul appealing to mercy because mercy is what saves. Christian men learn it before they learn anything else.</p>'
    ),
    'lead': (
        '<p>To <em>lead</em> in Scripture is to guide, direct, and conduct another along a path. God leads His people: <em>"He maketh me to lie down... he leadeth me beside the still waters"</em> (<em>Psalm 23:2</em>); <em>"He shall feed his flock like a shepherd... and shall gently lead those that are with young"</em> (<em>Isaiah 40:11</em>). The Spirit leads the sons of God (<em>Romans 8:14</em>). Pastors lead the flock (<em>Hebrews 13:7, 17</em>); husbands lead their wives (<em>1 Corinthians 11:3</em>; <em>Ephesians 5:23</em>); fathers lead their households (<em>Genesis 18:19</em>). The Shepherd-image is foundational: a leader walks ahead, knows the way, calls his charges by name, and accepts responsibility for getting them home.</p>'
    ),
    'love-of-money': (
        '<p>The love of money is Paul’s precise diagnosis of the root from which all kinds of evil grow: <em>"For the love of money is the root of all evil: which while some coveted after, they have erred from the faith, and pierced themselves through with many sorrows"</em> (<em>1 Timothy 6:10</em>). Notice: it is not money itself but the <em>love</em> of it — the desire, the trust, the worship — that corrupts. Greed disguises itself as ambition, prudence, or providing for one’s family; it is none of those. It is idolatry (<em>Colossians 3:5</em>). The remedy is not poverty but contentment: <em>"having food and raiment let us be therewith content"</em> (<em>1 Timothy 6:8</em>). The Christian man earns much and loves little of it.</p>'
    ),
    'mentoring': (
        '<p>Mentoring is the personal, life-on-life shaping of one disciple by an older man — modeled in Scripture by Moses-Joshua, Elijah-Elisha, Paul-Timothy, Paul-Titus, Barnabas-Paul, and ultimately Christ-the-Twelve. It is not a program, curriculum, or six-week study; it is a sustained relationship of imitation and instruction. Paul writes: <em>"Be ye followers of me, even as I also am of Christ"</em> (<em>1 Corinthians 11:1</em>), and <em>"the things that thou hast heard of me... the same commit thou to faithful men"</em> (<em>2 Timothy 2:2</em>). The mentor brings the younger man into his actual life — his work, his table, his struggles, his prayers. Reformed and patriarchal churches recover mentoring by recovering the table.</p>'
    ),
    'parental-honor': (
        '<p>Parental honor is the lifelong weight a child gives to father and mother in word, deed, and provision — the fifth commandment and the first <em>"commandment with promise"</em> (<em>Ephesians 6:2-3</em>; <em>Exodus 20:12</em>): <em>"Honour thy father and thy mother: that thy days may be long upon the land which the LORD thy God giveth thee."</em> Honor is not mere obedience (which expires at adulthood); it is the abiding posture of respect, gratitude, and responsibility — culminating in caring for aged parents (<em>1 Timothy 5:4</em>; <em>Mark 7:9-13</em>). The fifth commandment is the hinge between God-ward and man-ward duty: a child who cannot honor parents will struggle to honor any authority — magistrate, pastor, husband, or God Himself.</p>'
    ),
    'revelation-book': (
        '<p>Revelation (Greek <em>Apokalypsis</em>, "unveiling") is the capstone of Scripture — John’s apocalyptic vision given on Patmos around AD 95. It is no riddle for the curious but a pastoral letter to seven persecuted churches (chs. 2-3) unveiling Jesus Christ enthroned (chs. 4-5), opening seven seals (ch. 6), blowing seven trumpets (chs. 8-11), pouring seven bowls (ch. 16), judging the harlot Babylon (chs. 17-18), defeating beast and dragon (ch. 19), reigning in resurrection life (ch. 20), and consummating all things in the new heavens and new earth, the wedding of the Lamb (chs. 21-22). The book teaches the saints to endure: <em>"He which testifieth these things saith, Surely I come quickly. Amen."</em></p>'
    ),
    'solitude-extended': (
        '<p>Extended solitude is the discipline of prolonged aloneness with God — hours, a day, a season — long enough for the daily noise to fade, the false self to surface, and the still small voice to be heard. Jesus practiced it: <em>"Jesus himself departed into a mountain himself alone"</em> (<em>John 6:15</em>; cf. <em>Luke 5:16; 6:12</em>). Moses had Sinai; Elijah had Horeb; Paul had Arabia (<em>Galatians 1:17</em>). The first hour usually surfaces nothing but anxieties; only after the noise dies does the soul begin to hear. Modern Christians fear it because it strips them of distraction. Recovering it — Sabbath days, half-days, prayer retreats — is one of the costliest and most rewarding disciplines a man can take up.</p>'
    ),
    'trinity-season': (
        '<p>Trinity Season is the long season of the historic church year beginning Trinity Sunday (the Sunday after Pentecost) and running through Christ the King Sunday at the close of November, just before Advent. Sometimes called <em>Ordinary Time</em>, it is the longest stretch of the liturgical calendar — roughly half the year — and is given to the Christian’s growth in discipleship under triune grace. After the great festival cycle (Advent → Christmas → Epiphany → Lent → Easter → Pentecost) rehearses what God has <em>done</em>, Trinity Season catechizes what the Christian is to <em>be</em>. The lectionary turns to wisdom literature, the sermon on the mount, and the epistles’ ethical instruction. Holy living is the season’s theme.</p>'
    ),
    'vehement': (
        '<p>Vehement, in the KJV, names what is strong, fervent, forceful, and intense. Jonah’s shade-stripping <em>"vehement east wind"</em> drove him to despair under the gourd-vine (<em>Jonah 4:8</em>); the <em>"rushing mighty wind"</em> at Pentecost (<em>Acts 2:2</em>) was vehement; godly sorrow produced in the Corinthians <em>"vehement desire"</em> to make things right (<em>2 Corinthians 7:11</em>). The Song of Solomon calls love <em>"a most vehement flame"</em> (<em>Song 8:6</em>). The word reminds us that Scripture honors strong feeling rightly directed — covenantal love, holy zeal, sober earnestness — and rejects the modern flattening of every emotion into measured neutrality. The Christian man is permitted, and often required, to feel vehemently.</p>'
    ),
    'vexation': (
        '<p>Vexation is severe distress of spirit, harassment, or agitation. It is the great refrain of Ecclesiastes: <em>"all is vanity and vexation of spirit"</em> (<em>Ecclesiastes 1:14, 17; 2:11; 4:4</em>) — Solomon’s verdict on every life lived <em>under the sun</em> apart from God. Peter notes that Lot was <em>"vexed with the filthy conversation of the wicked"</em> in Sodom — <em>"vexed his righteous soul from day to day with their unlawful deeds"</em> (<em>2 Peter 2:7-8</em>). Vexation in Scripture is therefore not always sinful: a righteous soul is rightly vexed by surrounding wickedness. The man who is at peace in a perverse age is not the godly man; the godly man grieves daily over what grieves the Spirit.</p>'
    ),
    'vulnerability': (
        '<p>Vulnerability, biblically understood, is honest exposure of weakness, sin, and need before God and trusted brothers. It is not a virtue in itself, not therapy-culture oversharing, not a public confessional — it is the appropriate, ordered openness in which confession, healing, and covenant union grow. <em>"Confess your faults one to another, and pray one for another, that ye may be healed"</em> (<em>James 5:16</em>). Paul gloried in his weakness because Christ’s strength was made perfect in it (<em>2 Corinthians 12:9</em>). Christian men need older men, pastors, and accountability partners with whom they can be undefended — but they do not need to bleed in public. Strength holds, weakness is confessed, and the strong hide the weak under wing.</p>'
    ),
    'wisdom-from-above': (
        '<p>Wisdom from above is James’s sevenfold portrait of true wisdom — the kind that comes down from <em>"the Father of lights"</em> (<em>James 1:17</em>) rather than rising from below: <em>"the wisdom that is from above is first pure, then peaceable, gentle, and easy to be intreated, full of mercy and good fruits, without partiality, and without hypocrisy"</em> (<em>James 3:17</em>). It is contrasted sharply with <em>"earthly, sensual, devilish"</em> wisdom (<em>James 3:15</em>) that produces envy, strife, and confusion. The seven marks read like a moral medical chart: where any are missing, the wisdom claiming the name is counterfeit. Christian leaders especially must test their wisdom by this list — purity first, peaceableness next, gentleness throughout.</p>'
    ),
    'adoption-as-sons': (
        '<p>Adoption (Greek <em>huiothesia</em>, "placement as son") is the legal-relational act by which God brings believers into His family as full sons and heirs — not slaves, not hired servants, but blood-bought sons of God Himself (<em>Romans 8:15-17</em>; <em>Galatians 4:4-7</em>; <em>Ephesians 1:5</em>). Adoption is distinguished from regeneration (the new birth) and justification (the verdict) — it is the relational positioning of the believer within God’s household, sealed by the Spirit who cries <em>"Abba, Father"</em> in our hearts. Adoption ensures inheritance (<em>Romans 8:17</em>), fatherly discipline (<em>Hebrews 12:5-11</em>), and access (<em>Ephesians 2:18</em>). Every benefit of son-hood — name, status, future estate — belongs to the regenerate. The Christian is not God’s acquaintance; he is God’s heir.</p>'
    ),
    'assurance-pardon': (
        '<p>The Assurance of Pardon is the Scripture-based pronouncement of God’s forgiveness following the corporate prayer of confession in Reformed worship. Standing in the place of a minister of Christ — not as a Catholic absolutionist conferring pardon but as a herald announcing it — the pastor declares on the basis of Christ’s atoning work that those who have confessed are pardoned: <em>"If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness"</em> (<em>1 John 1:9</em>); <em>"as far as the east is from the west, so far hath he removed our transgressions from us"</em> (<em>Psalm 103:12</em>; cf. <em>Micah 7:19</em>). The congregation hears the verdict and goes free.</p>'
    ),
    'body-stewardship': (
        '<p>Body stewardship is the Christian discipline of caring for the body as the Holy Spirit’s temple (<em>1 Corinthians 6:19-20</em>) — sleep, food, exercise, modesty, sexual purity — not as vanity, narcissism, or fitness-culture self-worship, but as worship of the One who bought it with His blood: <em>"ye are not your own... therefore glorify God in your body."</em> The body is not the prison of the soul (Gnosticism) nor the toy of the self (modernity); it is the redeemed temple destined for resurrection (<em>1 Corinthians 15:42-44</em>). Treating it well is therefore Christian duty, not Christian luxury. Sloth, gluttony, drunkenness, immodesty, and sexual impurity all desecrate it. The Christian man eats, sleeps, trains, and clothes himself for the glory of God.</p>'
    ),
    'dead-sea': (
        '<p>The Dead Sea is the salt lake at the lowest point on the earth’s surface (about 1,400 feet below sea level), lying in the Jordan Rift Valley between modern Israel, Jordan, and the West Bank. Scripture calls it the <em>Salt Sea</em> (<em>Genesis 14:3</em>; <em>Numbers 34:3, 12</em>; <em>Joshua 15:5</em>), the <em>Sea of the Plain</em>, and the <em>East Sea</em>. The cities of Sodom and Gomorrah lay along its southern shore before their destruction (<em>Genesis 19</em>). Its mineral concentration is so high that nothing lives in it — fitting symbol of judgment. Yet <em>Ezekiel 47:8-10</em> prophesies a stream from the temple sweetening its waters and filling them with fish — eschatological reversal: where death reigned, life will swarm.</p>'
    ),
    'early-rising': (
        '<p>Early rising is the discipline of rising before the world’s noise to seek God in the day’s first quiet — the rhythm of David, of Christ, and of the saints who knew dawn belongs to prayer. <em>"My voice shalt thou hear in the morning, O LORD; in the morning will I direct my prayer unto thee, and will look up"</em> (<em>Psalm 5:3</em>; cf. <em>57:8; 63:1; 119:147</em>). <em>"In the morning, rising up a great while before day, he went out, and departed into a solitary place, and there prayed"</em> (<em>Mark 1:35</em>) — of Jesus. The first hour of the day is the territory most contested; the man who gives it to God secures the rest. Phone last, Bible first.</p>'
    ),
    'el-deah': (
        '<p><em>El-Deah</em> (אֵל דֵּעוֹת) — "the God of knowledge" — is the divine title Hannah declares in <em>1 Samuel 2:3</em>: <em>"Talk no more so exceeding proudly; let not arrogancy come out of your mouth: for the LORD is a God of knowledge, and by him actions are weighed."</em> The name names the omniscient LORD who weighs not merely deeds but motives, not merely actions but the heart from which they spring. Nothing is hidden from Him — <em>"all things are naked and opened unto the eyes of him with whom we have to do"</em> (<em>Hebrews 4:13</em>). The pride that thinks itself unseen is the worst delusion of the fallen mind. El-Deah sees through it, weighs it, and judges it justly.</p>'
    ),
    'el-gibbor': (
        '<p><em>El-Gibbor</em> (אֵל גִּבּוֹר) — "Mighty God, God-Warrior" — is the prophetic title Isaiah gives the coming Messiah: <em>"For unto us a child is born, unto us a son is given... and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace"</em> (<em>Isaiah 9:6</em>). The same word names the LORD Himself in <em>Deuteronomy 10:17</em> — <em>"a great God, a mighty"</em> — and the Davidic mighty men in <em>2 Samuel 23</em>. The title insists that the incarnate Child is no demigod, no lesser deity, no angelic envoy: He is <em>El-Gibbor</em>, God Himself in warrior strength, born to fight the dragon and rescue the bride.</p>'
    ),
    'eternal-procession': (
        '<p>The Eternal Procession of the Spirit is the orthodox Trinitarian doctrine that the Holy Spirit eternally proceeds from the Father (<em>John 15:26</em>) — and, in Western theology following Augustine and confirmed by the <em>filioque</em> clause of the Nicene Creed, also from the Son. Procession is not creation, generation, or temporal sending; it names the third Person’s eternal mode of existence within the one undivided Godhead. The Son is eternally <em>begotten</em>; the Spirit is eternally <em>spirated</em> (or <em>proceeds</em>). The Eastern Church rejected the <em>filioque</em>; the Western retained it; the Reformed Confessions affirm it. The doctrine protects the deity of the Spirit (He is not made) and His distinct personhood (He is not absorbed). Procession is who He <em>is</em>, eternally.</p>'
    ),
    'fool-biblical': (
        '<p>The biblical fool is not the comic figure of folklore but the morally rebellious — the man whose folly is religious, not intellectual. The Psalter opens the doctrine: <em>"The fool hath said in his heart, There is no God"</em> (<em>Psalm 14:1; 53:1</em>). Proverbs adds layers: the fool hates knowledge (<em>1:22</em>), despises correction (<em>1:7; 15:5</em>), trusts his own heart (<em>28:26</em>), and rages when crossed (<em>14:16</em>). His folly is not low IQ but high rebellion; he can be brilliant and a fool at once. Wisdom begins with the fear of the LORD (<em>Proverbs 1:7; 9:10</em>) — exactly what the fool refuses. The remedy is repentance, not education; the cure is conversion, not cleverness.</p>'
    ),
    'gilgal': (
        '<p>Gilgal was Israel’s first encampment after crossing the Jordan into the promised land (<em>Joshua 4-5</em>). There Joshua set up twelve memorial stones taken from the riverbed, circumcised the wilderness generation, and kept the first Passover in Canaan. The LORD said, <em>"This day have I rolled away the reproach of Egypt from off you"</em> — the name <em>Gilgal</em> means "rolling." From Gilgal the conquest fanned out. Later it became a center of worship (<em>1 Samuel 7:16; 10:8; 11:14-15</em>) and prophetic activity (<em>2 Kings 2:1; 4:38</em>). But by Hosea’s day it had become a syncretistic shrine and was condemned (<em>Hosea 4:15; 9:15; Amos 4:4; 5:5</em>). Like every place, it was holy only as the LORD met His people there.</p>'
    ),
    'heal': (
        '<p>To <em>heal</em>, biblically, is to make whole — physically, spiritually, relationally — restoring what sin and the fall have broken. The covenant name <em>YHWH-Rapha</em>, "the LORD that healeth thee" (<em>Exodus 15:26</em>), grounds the whole theology. Christ’s healing miracles demonstrate kingdom-arrival: <em>"the blind receive their sight, and the lame walk, the lepers are cleansed, and the deaf hear, the dead are raised up"</em> (<em>Matthew 11:5</em>). The church is to pray for the sick — <em>"the prayer of faith shall save the sick, and the Lord shall raise him up"</em> (<em>James 5:14-15</em>) — without making physical healing the proof of God’s favor. Ultimate, comprehensive healing is bodily resurrection, when no eye shall weep and no body shall break (<em>Revelation 21:4</em>).</p>'
    ),
    'heart-courageous': (
        '<p>A courageous heart is the obedient heart anchored in God’s present help. The command comes to Joshua three times in a single chapter: <em>"Be strong and of a good courage... Only be thou strong and very courageous... Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the LORD thy God is with thee whithersoever thou goest"</em> (<em>Joshua 1:6, 7, 9</em>). Courage is not the absence of fear but the willingness to act under God in spite of it. David charged Solomon the same way (<em>1 Chronicles 22:13</em>); Paul charged Timothy (<em>2 Timothy 1:7</em>). Christian men cultivate it by rehearsing God’s presence — and then doing the next hard thing.</p>'
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
