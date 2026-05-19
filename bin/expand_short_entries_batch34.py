#!/usr/bin/env python3
"""Batch 34 — expand 25 more entries from the 50-60 word bucket.

Targets: Hebrew vocab, OT figures, slang reframes, body gestures,
Beatitudes, sabbath theology, typology, and ecclesial categories.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'kneel': (
        '<p>To kneel is to bend the knee in worship, supplication, or submission — the body’s native confession of someone greater than oneself. Solomon kneeled at the temple dedication: <em>"he kneeled down upon his knees before all the congregation of Israel, and spread forth his hands toward heaven"</em> (<em>2 Chronicles 6:13</em>). Daniel kneeled three times daily, at his open window, in defiance of the king’s decree (<em>Daniel 6:10</em>). Christ kneeled in Gethsemane (<em>Luke 22:41</em>). Stephen kneeled at his stoning, crying for his murderers (<em>Acts 7:60</em>). Paul kneeled at the Ephesian elders’ farewell (<em>Acts 20:36</em>) and at Tyre on the beach (<em>21:5</em>). Every knee will one day bow at the name of Jesus (<em>Philippians 2:10</em>). The Christian gladly kneels now.</p>'
    ),
    'leah': (
        '<p>Leah was the elder daughter of Laban — and the unloved first wife of Jacob, married to him by Laban’s deceit on the wedding night when Jacob had served seven years for Rachel her younger sister (<em>Genesis 29:21-30</em>). She is described as <em>"tender eyed"</em> in contrast with Rachel’s beauty. Yet Scripture quietly honors the unwanted wife: <em>"And when the LORD saw that Leah was hated, he opened her womb: but Rachel was barren"</em> (<em>Genesis 29:31</em>). Leah bore Jacob six of the twelve tribal patriarchs — including Levi (the priesthood) and Judah (the line of David and Christ). The Messiah comes through Leah’s line, not Rachel’s. God exalts the unchosen of men.</p>'
    ),
    'magen': (
        '<p><em>Magen</em> (מָגֵן) is the Hebrew word for shield — specifically the small round shield carried in personal combat, distinct from the large rectangular body-shield (<em>tsinnah</em>). It is used repeatedly and metaphorically of YHWH as the defender of His people: <em>"But thou, O LORD, art a shield for me; my glory, and the lifter up of mine head"</em> (<em>Psalm 3:3</em>); <em>"The LORD is my strength and my shield"</em> (<em>Psalm 28:7</em>); <em>"Fear not, Abram: I am thy shield, and thy exceeding great reward"</em> (<em>Genesis 15:1</em>). The Star of David is called <em>Magen David</em> — the shield of David — because David’s psalms repeatedly name YHWH as his shield. The Christian fights covered, not exposed.</p>'
    ),
    'mashal': (
        '<p><em>Mashal</em> (מָשָׁל) is the Hebrew literary category encompassing proverbs, parables, riddles, taunt-songs, and didactic poetry. The book of Proverbs is in Hebrew <em>Mishlei</em> — the plural of <em>mashal</em>. The Greek <em>parabolē</em> ("parable") translates the same Hebrew term in the Septuagint. Christ’s parables therefore operate in the rabbinic-<em>mashal</em> tradition — short, vivid, often allusive narratives designed to teach truth and simultaneously test the hearer’s heart: <em>"that seeing they may see, and not perceive"</em> (<em>Mark 4:12</em>). Reading the Lord’s parables as <em>meshalim</em> (plural) helps recognize their didactic, layered, and sometimes deliberately puzzling character. The teacher reveals to disciples and conceals from scoffers in the same sentence.</p>'
    ),
    'modesty-biblical': (
        '<p>Biblical modesty is the discipline of measure in apparel, speech, and self-presentation — the refusal to display what is properly hidden or to seek attention by display. Paul commands it of women: <em>"In like manner also, that women adorn themselves in modest apparel, with shamefacedness and sobriety; not with broided hair, or gold, or pearls, or costly array; but (which becometh women professing godliness) with good works"</em> (<em>1 Timothy 2:9-10</em>). Peter reaches the same point: <em>"Whose adorning let it not be that outward adorning... but let it be the hidden man of the heart"</em> (<em>1 Peter 3:3-4</em>). Modesty is broader than dress — it includes speech, social-media curation, and self-promotion — but it is not less. Christian men should expect it of their wives and daughters, and model it themselves.</p>'
    ),
    'mourn-comforted': (
        '<p>"Blessed are they that mourn: for they shall be comforted" is the second Beatitude of Christ’s Sermon on the Mount (<em>Matthew 5:4</em>). The mourning is not generic sadness or melancholy temperament. The Greek <em>penthountes</em> describes the deep grief of bereavement — and in context, the godly grief that grace produces over sin (one’s own and the world’s). It is the grief of <em>2 Corinthians 7:10</em>: <em>"godly sorrow worketh repentance to salvation."</em> The promised comfort runs in two horizons. Present-tense: the <em>Paraclete</em>, the Holy Spirit, the Comforter (<em>John 14:16</em>). Future-tense: <em>"And God shall wipe away all tears from their eyes"</em> (<em>Revelation 21:4</em>). The Christian mourns truly and is comforted decisively.</p>'
    ),
    'nabi': (
        '<p><em>Nabi</em> (נָבִיא) is the Hebrew word for <em>prophet</em>. The <em>nabi</em> is YHWH’s spokesman — one who declares God’s word to the people, often calling them back from idolatry to covenant faithfulness, denouncing sin, comforting the wounded, and announcing the LORD’s deeds. Abraham is the first man called <em>nabi</em> in Scripture (<em>Genesis 20:7</em>); Moses is the prophet against whom all others are measured (<em>Deuteronomy 18:15-18</em>); the prophetic line runs through Samuel, Elijah, Isaiah, Jeremiah, and the rest. Christ is the prophet <em>"like unto Moses"</em> (<em>Acts 3:22-23</em>). At Pentecost, Joel’s prophecy is fulfilled: the Spirit pours out the prophetic gift on all flesh (<em>Acts 2:17-18</em>). Every Spirit-filled saint is now a witness-prophet to Christ.</p>'
    ),
    'periodt': (
        '<p>"Periodt" — with the silent <em>t</em> — is the emphatic conversational seal popularized in social-media speech, meaning <em>"end of discussion, no further argument allowed."</em> In its mildest use it just marks confidence; in its harder use it shuts down dialogue and frames the speaker’s opinion as final without engagement. Scripture warns against the posture in the proud: <em>"Seest thou a man wise in his own conceit? there is more hope of a fool than of him"</em> (<em>Proverbs 26:12</em>). Conversely, the wise are willing to weigh: <em>"He that answereth a matter before he heareth it, it is folly and shame unto him"</em> (<em>Proverbs 18:13</em>). The Christian holds convictions firmly <em>and</em> remains open to correction by Scripture, periodt.</p>'
    ),
    'prayerfulness': (
        '<p>Prayerfulness is the settled disposition of a soul habitually turned to God in prayer — not occasional petition under pressure but sustained communion across the rhythms of the day. Paul commands it explicitly: <em>"Continuing instant in prayer"</em> (<em>Romans 12:12</em>); <em>"Pray without ceasing"</em> (<em>1 Thessalonians 5:17</em>); <em>"Continue in prayer, and watch in the same with thanksgiving"</em> (<em>Colossians 4:2</em>). Daniel modeled it: three times a day, on his knees, by an open window facing Jerusalem, in defiance of the royal decree (<em>Daniel 6:10</em>). Christ rose a great while before day to pray (<em>Mark 1:35</em>). Prayerfulness is built habit, not random mood. Christian men recover it by fixed times, fixed places, and a fixed determination to refuse silence with God.</p>'
    ),
    'quick-and-dead': (
        '<p>"The quick and the dead" is the older English phrase for <em>"the living and the dead."</em> Scripture and the historic creeds use it to confess that Christ will judge every human being who has ever existed — those still alive at His return, and those whose bodies have died and shall be raised: <em>"who shall give account to him that is ready to judge the quick and the dead"</em> (<em>1 Peter 4:5</em>); <em>"who shall judge the quick and the dead at his appearing and his kingdom"</em> (<em>2 Timothy 4:1</em>); the Apostles’ Creed: <em>"from thence he shall come to judge the quick and the dead."</em> The judgment is universal — no soul escapes by dying first; no living soul escapes by hiding. Every man stands before Christ.</p>'
    ),
    'sabbath-work-rest': (
        '<p>The Sabbath is the seventh-day rest God established at creation (<em>Genesis 2:2-3</em>) — codified at Sinai as the fourth commandment (<em>Exodus 20:8-11</em>), transposed in the New Covenant to the Lord’s Day (the first day of the week, in resurrection commemoration, <em>Revelation 1:10; Acts 20:7; 1 Corinthians 16:2</em>), and pointing forward to the eternal rest that remains for the people of God: <em>"There remaineth therefore a rest to the people of God"</em> (<em>Hebrews 4:9</em>). It is rest from work but not idleness — rest that is itself worship. The pattern of six-days-and-one is woven into the human creature; ignore it, and the body, soul, family, and nation pay. The Christian Sabbath is gift and command together.</p>'
    ),
    'sentry': (
        '<p>A sentry is the soldier posted to perceive and report. Scripture has the same office under the more frequent name <em>watchman</em>: stationed on the city wall, awake while the city sleeps, accountable for warning. The sentry’s sin is silence. Ezekiel’s great commission passage: <em>"if the watchman see the sword come, and blow not the trumpet, and the people be not warned; if the sword come, and take any person from among them, he is taken away in his iniquity; but his blood will I require at the watchman’s hand"</em> (<em>Ezekiel 33:6</em>). Pastors, fathers, citizens — each holds a sentry’s post in proportion to his sphere. The unsounded alarm is the sentry’s gravest dereliction.</p>'
    ),
    'single-minded': (
        '<p>"Single-minded" names the saint whose attention, allegiance, and aim are undivided. Christ taught the figure with the single eye: <em>"The light of the body is the eye: if therefore thine eye be single, thy whole body shall be full of light"</em> (<em>Matthew 6:22</em>). The Greek <em>haplous</em> means "simple, single, undivided" — focused on one object. James contrasts the double-minded man: <em>"A double minded man is unstable in all his ways"</em> (<em>James 1:8</em>); <em>"Draw nigh to God, and he will draw nigh to you... purify your hearts, ye double minded"</em> (<em>4:8</em>). Single-mindedness is wholeness of orientation: the man whose work, marriage, money, and rest all aim at one Lord. The fragmented man cannot be at peace.</p>'
    ),
    'spreading-cloaks': (
        '<p>Spreading the cloaks is the gesture by which a people received a king: they took their outer garments off and laid them on the road for him to ride or walk over. The crowds did this for Jesus at the Triumphal Entry: <em>"And a very great multitude spread their garments in the way; others cut down branches from the trees, and strawed them in the way"</em> (<em>Matthew 21:8</em>; <em>Mark 11:8</em>; <em>Luke 19:36</em>) — fulfilling <em>Zechariah 9:9</em>’s prophecy of the king coming on the colt of an ass. Jehu received the same honor at his anointing: <em>"Then they hasted, and took every man his garment, and put it under him on the top of the stairs, and blew with trumpets, saying, Jehu is king"</em> (<em>2 Kings 9:13</em>). The garment under the foot says: my honor for yours.</p>'
    ),
    'sprinkled-blood': (
        '<p>Sprinkled blood is one of Scripture’s great priestly motions — blood scattered in measured drops upon altar, mercy seat, people, or sacred vessel, cleansing what it touches and ratifying covenant. Moses sprinkled the blood of the covenant on the people: <em>"Behold the blood of the covenant, which the LORD hath made with you"</em> (<em>Exodus 24:8</em>). On the Day of Atonement, the high priest sprinkled blood on the mercy seat seven times (<em>Leviticus 16:14-15</em>). Hebrews culminates the picture: <em>"And to Jesus the mediator of the new covenant, and to the blood of sprinkling, that speaketh better things than that of Abel"</em> (<em>Hebrews 12:24</em>). The Christian has come to that blood — a believer’s soul is sprinkled by it, cleansed at depth.</p>'
    ),
    'strongholds': (
        '<p>Strongholds, in Paul’s metaphor, are fortified positions of false thought that the saint is to tear down — and the weapons of demolition are not of the flesh. <em>"For the weapons of our warfare are not carnal, but mighty through God to the pulling down of strong holds; casting down imaginations, and every high thing that exalteth itself against the knowledge of God, and bringing into captivity every thought to the obedience of Christ"</em> (<em>2 Corinthians 10:4-5</em>). The fortress is in the mind — false philosophy, addictive narrative, deep-rooted lie, persistent fear. The demolition is by the gospel, the Spirit, the Word, and prayer. The Christian man takes every thought captive to Christ; the unconquered stronghold eventually conquers him.</p>'
    ),
    'swell': (
        '<p>"Swell" is mid-twentieth-century American slang for <em>"excellent"</em> or <em>"fine"</em> — carrying overtones of mid-century optimism, propriety, and middle-class respectability (<em>"He’s a swell guy"</em>). The slang reveals a cultural assumption Boomers inherited (and partly rejected): that the right adjective could cover over much that was actually wrong. The era’s decorum-vocabulary had a way of papering over private sin and societal injustice alike. Scripture is willing to call good <em>good</em> and evil <em>evil</em>, without softening words: <em>"Woe unto them that call evil good, and good evil; that put darkness for light, and light for darkness"</em> (<em>Isaiah 5:20</em>). Christian speech must be both kind and precise. Saying "swell" is fine; using "swell" to hide what should be exposed is not.</p>'
    ),
    'swipe-right': (
        '<p>"Swipe right" is dating-app shorthand for expressing interest in a person — reduced to a profile photo, a one-line bio, and an algorithmically-served swipe of the finger. The same gesture is used to dismiss an Instagram ad. The slang names a profound cultural shift: marriage-track relationships are now formed (or rejected) by the same mechanic used to scroll through products. Scripture’s covenant frame is at war with the gesture. Marriage in the Bible is preceded by serious paternal consultation (<em>Genesis 24</em>), bride-price (<em>Exodus 22:16-17</em>), public witnesses, vows, and feasting. Christian men should refuse to court via swipe. Marriage is the central earthly covenant; build it on something more than a thumb-flick.</p>'
    ),
    'trials': (
        '<p>Trials are God-permitted testings of the believer’s faith, intended to refine and prove what is genuine. They are not to be confused with sin’s own enticements — which Scripture sharply distinguishes: <em>"Let no man say when he is tempted, I am tempted of God: for God cannot be tempted with evil, neither tempteth he any man: but every man is tempted, when he is drawn away of his own lust, and enticed"</em> (<em>James 1:13-14</em>). Peter calls trials a fiery refining: <em>"that the trial of your faith, being much more precious than of gold that perisheth"</em> (<em>1 Peter 1:7</em>). James commands believers to count them all joy (<em>James 1:2</em>); Paul says they produce patience, character, and hope (<em>Romans 5:3-4</em>). Welcome the test.</p>'
    ),
    'waving-palms': (
        '<p>Waving palms is the gesture of greeting a king, a deliverer, or a triumphant warrior — and Scripture loads it with messianic significance. The crowds at Jesus’ entry into Jerusalem cut palm branches and waved them, crying <em>"Hosanna; Blessed is he that cometh in the name of the Lord: Blessed is the King of Israel that cometh in the name of the Lord"</em> (<em>John 12:13</em>) — the only Gospel to specify palm. The Feast of Tabernacles required the <em>lulav</em> (palm-bundle) to be waved (<em>Leviticus 23:40</em>). The eschatological vision in Revelation places palms in the hands of the redeemed multitude: <em>"a great multitude... clothed with white robes, and palms in their hands"</em> (<em>Revelation 7:9</em>). Every palm waved hails the same King.</p>'
    ),
    'angel-of-light': (
        '<p>"Angel of light" is Paul’s grave warning phrase in <em>2 Corinthians 11:14</em>: <em>"And no marvel; for Satan himself is transformed into an angel of light. Therefore it is no great thing if his ministers also be transformed as the ministers of righteousness; whose end shall be according to their works."</em> The disguise is theologically loaded. The most dangerous deceptions look brightest. False apostles, false teachers, false revivals, false spiritualities, and false spirits are most effective when they look most spiritual — luminous, gentle, persuasive, well-credentialed. Paul warns by name. The Christian must therefore not measure truth by appearance, by brightness, or by experience; the test is Scripture (<em>1 John 4:1; Galatians 1:8-9</em>). Bright is not the same as <em>true</em>.</p>'
    ),
    'antitype': (
        '<p>The antitype is the New Testament fulfillment of a divinely-intended Old Testament <em>type</em> — the substance to which the shadow pointed. Christ is the great antitype of the whole Old Testament: the true Adam (<em>Romans 5:14; 1 Corinthians 15:45</em>), the true Passover lamb (<em>1 Corinthians 5:7</em>), the true Melchizedek (<em>Hebrews 7</em>), the true Israel, the true temple (<em>John 2:21</em>), the true manna (<em>John 6:48-51</em>), the true bronze serpent (<em>John 3:14</em>), the true Davidic king. Peter explicitly calls baptism the antitype of Noah’s flood: <em>"The like figure whereunto even baptism doth also now save us"</em> (<em>1 Peter 3:21</em>; the Greek is <em>antitypon</em>). Reading the Old Testament Christologically means recognizing the antitypes everywhere.</p>'
    ),
    'bethel': (
        '<p>Bethel — Hebrew <em>"house of God"</em> — was the town between Ai and Luz where Jacob saw the ladder reaching to heaven, with the angels of God ascending and descending. He named the place forever: <em>"Surely the LORD is in this place; and I knew it not... How dreadful is this place! this is none other but the house of God, and this is the gate of heaven"</em> (<em>Genesis 28:16-19</em>). Centuries later, after the kingdom split, Bethel became one of Jeroboam’s two golden-calf shrines (<em>1 Kings 12:28-29</em>) — a holy place turned counterfeit. Hosea condemns it as <em>Beth-Aven</em>, "house of vanity" (<em>Hosea 4:15</em>). Bethel is the case study: sacred places turn counterfeit whenever men replace God’s revelation with their own design.</p>'
    ),
    'bivouac': (
        '<p>A bivouac is the temporary, light camp of a military unit on the move — pitched at evening, struck at dawn, never the permanent base. Scripture has the corresponding word in the wilderness tabernacle: the portable, pitched-and-struck dwelling of God among His marching people, the cloud lifting and settling as the signal to move (<em>Numbers 9:15-23</em>). Paul applies the image to the Christian body: <em>"For we know that if our earthly house of this tabernacle were dissolved, we have a building of God, an house not made with hands, eternal in the heavens"</em> (<em>2 Corinthians 5:1</em>). We are bivouacked here, not yet at base. The body is the tent; the resurrection-body is the house. Travel light; expect to strike camp.</p>'
    ),
    'calling-secondary': (
        '<p>Secondary calling is the believer’s call to a particular work in the world — the trade, craft, post, vocation, or station that the saint occupies under the Lord. The Reformers (notably Luther) distinguished it from the <em>primary calling</em>, the call to Christ Himself. Both are real; both come from God; both are to be honored. <em>"Let every man abide in the same calling wherein he was called"</em> (<em>1 Corinthians 7:20</em>); <em>"And whatsoever ye do in word or deed, do all in the name of the Lord Jesus, giving thanks to God and the Father by him"</em> (<em>Colossians 3:17</em>). The carpenter, farmer, soldier, mother, and pastor are each fulfilling secondary callings under the primary one — and the workshop is a holy place when consecrated to God.</p>'
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
