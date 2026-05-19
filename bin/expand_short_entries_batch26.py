#!/usr/bin/env python3
"""Batch 26 — expand 25 more thin entries to 90-110 words each.

Targets: marriage/economy, OT/NT figures, theologians, virtues,
biblical imagery, and modern slang reframes from the 30-50 word
bucket. Brings the session total to 650.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'dowry': (
        '<p>The dowry — properly, the <em>bride-price</em> in biblical custom — was the payment a man made to the bride’s father in order to marry her. Scripture reflects the practice without condemning it: in <em>Exodus 22:16-17</em>, a man who seduces an unbetrothed virgin must pay the bride-price as he would have for a wife — and the father may still refuse. Jacob labored fourteen years (and then six more) for his wives Leah and Rachel (<em>Genesis 29:20-27</em>). The bride-price was not the purchase of a slave but a covenantal demonstration that marriage was costly, serious, and binding — the man invested his labor before the woman invested her life. Modern Christian men do well to recover the principle: marriage should cost the groom before it costs the bride.</p>'
    ),
    'enlist': (
        '<p>To enlist is to be entered upon the list of a military unit — to bind oneself, by oath, to serve under its colors. Paul applies the metaphor to discipleship in <em>2 Timothy 2:3-4</em>: <em>"Thou therefore endure hardness, as a good soldier of Jesus Christ. No man that warreth entangleth himself with the affairs of this life; that he may please him who hath chosen him to be a soldier."</em> The Christian life is enlisted service — not a casual association, not a fan-club membership, not a Sunday subscription. It is service under a Commander, bound by oath, under arms, on duty until discharge. The enlistment was made at baptism; the colors are the cross; the campaign continues until the King returns. Christian men should think like soldiers.</p>'
    ),
    'everlasting-arms': (
        '<p>The "everlasting arms" are Moses’ final-blessing image of YHWH’s eternal sustaining strength: <em>"The eternal God is thy refuge, and underneath are the everlasting arms: and he shall thrust out the enemy from before thee; and shall say, Destroy them"</em> (<em>Deuteronomy 33:27</em>). The arms hold from <em>below</em> — you cannot fall lower than they reach. They are <em>everlasting</em> — they do not weary, do not tire, do not give out. They are <em>the LORD’s</em> — neither the saint’s strength nor any creature’s, but God’s own arm bearing His own people. The doctrine is the basis of the great hymn <em>"Leaning on the Everlasting Arms"</em> (Hoffman/Showalter, 1887). Lean. The arms will not fail under your weight.</p>'
    ),
    'hearken-unto': (
        '<p>"Hearken unto" is the KJV’s standard rendering of the Hebrew <em>shamaʿ</em> — <em>to hear-and-obey</em>. The Hebrew verb does not split listening from obeying as English often does; biblical hearing already implies the obedient response. The great <em>Shema</em> of Israel — <em>"Hear, O Israel: The LORD our God is one LORD"</em> (<em>Deuteronomy 6:4</em>) — opens with the imperative of this verb. The prophets repeatedly cry: <em>"Hearken to the voice of the LORD your God"</em> (<em>Jeremiah 26:13</em>). To hearken is the saint’s first and continuing posture before the LORD’s word — not curating, not negotiating, not selectively engaging, but receiving with the readiness to obey. <em>"To obey is better than sacrifice"</em> (<em>1 Samuel 15:22</em>).</p>'
    ),
    'know': (
        '<p>To <em>know</em>, in Scripture, is rarely abstract data-acquisition. It is relational, experiential, and covenantal — a Hebrew way of seeing built into every layer of the Bible. The verb covers marital intimacy (<em>"Adam knew Eve his wife; and she conceived"</em>, <em>Genesis 4:1</em>), divine recognition (<em>"the LORD knoweth them that are his"</em>, <em>2 Timothy 2:19</em>; <em>John 10:14</em>), and the disciple’s growing acquaintance with Christ (<em>"this is life eternal, that they might know thee the only true God, and Jesus Christ, whom thou hast sent"</em>, <em>John 17:3</em>). Christian knowing is therefore never merely informational. The devil knows facts about God; the saint <em>knows</em> God. The difference is everything — the difference between hell and heaven.</p>'
    ),
    'linen': (
        '<p>Linen is a fine cloth woven from flax — the Scriptural fabric of priesthood, burial, and glory. Aaron and his sons ministered in linen garments specifically prescribed by God (<em>Exodus 28:39-43</em>; <em>Leviticus 16:4</em>). Christ’s body was wrapped in fine linen and laid in the tomb (<em>Matthew 27:59</em>; <em>John 19:40</em>); the same linen was found in the empty tomb folded neatly on resurrection morning (<em>John 20:6-7</em>). The Bride of Revelation 19 is clothed in <em>"fine linen, clean and white,"</em> and the text interprets the symbol: <em>"the fine linen is the righteousness of saints"</em> (<em>Revelation 19:8</em>). From priestly service to grave-cloth to wedding-garment, linen runs the whole biblical line.</p>'
    ),
    'mint': (
        '<p>Mint is an aromatic garden herb tithed by the Pharisees with painstaking accuracy — counting individual leaves into the tithe basket. Christ’s rebuke is sharp: <em>"Woe unto you, scribes and Pharisees, hypocrites! for ye pay tithe of mint and anise and cummin, and have omitted the weightier matters of the law, judgment, mercy, and faith: these ought ye to have done, and not to leave the other undone"</em> (<em>Matthew 23:23</em>; cf. <em>Luke 11:42</em>). Mint is therefore the perpetual type of religious precision that majors on the trivial while ignoring justice, mercy, and faith. The mint is not the problem; tithing it is right. The heart that tithes mint and devours widows is. Get both: tithe the mint, weep over the widows.</p>'
    ),
    'opening-hands': (
        '<p>"Opening the hands" is Scripture’s emblem for two paired truths. First, that God’s open hand sustains every living creature: <em>"Thou openest thine hand, they are filled with good"</em> (<em>Psalm 104:28</em>); <em>"The eyes of all wait upon thee; and thou givest them their meat in due season. Thou openest thine hand, and satisfiest the desire of every living thing"</em> (<em>Psalm 145:15-16</em>). Second, that the saint’s open hand is the only kind that can give: <em>"Thou shalt open thine hand wide unto thy brother, to thy poor, and to thy needy"</em> (<em>Deuteronomy 15:11</em>). The closed fist will neither receive provision nor pass it on. Christian generosity is just keeping the hand that the LORD opens to us open toward our neighbor.</p>'
    ),
    'plead-cause': (
        '<p>To "plead the cause" is to bring legal contention on behalf of another — to act as the spoken advocate in the courtroom. In Scripture, the LORD pleads the cause of the oppressed: <em>"Plead my cause, O LORD, with them that strive with me"</em> (<em>Psalm 35:1</em>); <em>"The LORD will plead their cause, and spoil the soul of those that spoiled them"</em> (<em>Proverbs 22:23</em>). And the saints are called to plead the cause of those who cannot plead their own: <em>"Open thy mouth for the dumb in the cause of all such as are appointed to destruction. Open thy mouth, judge righteously, and plead the cause of the poor and needy"</em> (<em>Proverbs 31:8-9</em>; cf. <em>Isaiah 1:17</em>). Christian advocacy is courtroom-shaped.</p>'
    ),
    'quietude': (
        '<p>Quietude is the settled, composed stillness of a soul that trusts God — not the absence of trouble but the absence of inner agitation in the midst of trouble. Isaiah locates it as the secret strength of God’s people: <em>"In returning and rest shall ye be saved; in quietness and in confidence shall be your strength"</em> (<em>Isaiah 30:15</em>); <em>"And the work of righteousness shall be peace; and the effect of righteousness quietness and assurance for ever"</em> (<em>Isaiah 32:17</em>). Peter applies it specifically to Christian women: <em>"the ornament of a meek and quiet spirit, which is in the sight of God of great price"</em> (<em>1 Peter 3:4</em>). The world prizes noise, performance, and reactive heat. The Christian recovers quietude — and finds strength.</p>'
    ),
    'scorn': (
        '<p>Scorn is the disposition of contemptuous derision — the heart that mocks what God has spoken. Scripture treats the <em>scorner</em> as a fixed type, not merely an unbeliever but a militant despiser: <em>"Blessed is the man... that sitteth not in the seat of the scornful"</em> (<em>Psalm 1:1</em>); <em>"Smite a scorner, and the simple will beware: and reprove one that hath understanding, and he will understand knowledge"</em> (<em>Proverbs 19:25</em>); <em>"Reprove not a scorner, lest he hate thee"</em> (<em>Proverbs 9:8</em>). The scorner cannot be argued out of his position because the scoff itself is his argument. The remedy is not more debate — it is the LORD’s own response: <em>"Surely he scorneth the scorners: but he giveth grace unto the lowly"</em> (<em>Proverbs 3:34</em>).</p>'
    ),
    'shemittah-year': (
        '<p>The <em>shemittah</em> (שְׁמִטָּה, "release") was the seventh-year Sabbath commanded for the land and for debt. The land was to lie fallow for one full year in every seven (<em>Leviticus 25:1-7</em>): no sowing, no pruning, no reaping — what grew of itself was for the poor and the wild. The same year, debts between Israelites were released: <em>"At the end of every seven years thou shalt make a release"</em> (<em>Deuteronomy 15:1-11</em>). Together with the Year of Jubilee (every fiftieth year), the <em>shemittah</em> encoded mercy into Israel’s economic and agricultural life. Failure to keep the <em>shemittah</em> is given as a reason for the seventy-year Babylonian exile (<em>2 Chronicles 36:21</em>). The land would have its sabbaths, one way or another.</p>'
    ),
    'sincerity': (
        '<p>Sincerity is freedom from pretense, deceit, and double-mindedness — the quality of being <em>sun-tested</em>, what holds up when the light falls full upon it. The Latin root <em>sine cera</em> ("without wax") originally described pottery sold without filler-wax patching the cracks. Paul names sincerity as the bread of the Lord’s table: <em>"Therefore let us keep the feast, not with old leaven, neither with the leaven of malice and wickedness; but with the unleavened bread of sincerity and truth"</em> (<em>1 Corinthians 5:8</em>). He commends his own apostolic conduct in the same terms: <em>"in simplicity and godly sincerity"</em> (<em>2 Corinthians 1:12</em>). The Christian man is sincere through and through — the same in private as in public, the same in trial as in ease.</p>'
    ),
    'thomas': (
        '<p>Thomas was one of the twelve apostles, called <em>Didymus</em> ("the twin"), and best remembered for two extraordinary statements. The first is his courageous loyalty on the way to Lazarus’s tomb: <em>"Let us also go, that we may die with him"</em> (<em>John 11:16</em>). The second is his absent-skepticism after the resurrection — <em>"Except I shall see in his hands the print of the nails... I will not believe"</em> (<em>John 20:25</em>) — followed by his climactic confession when the risen Christ appeared: <em>"My Lord and my God"</em> (<em>20:28</em>) — the highest Christological statement in any of the Gospels. Tradition sends him to evangelize as far as India, where he was reportedly martyred by spear-thrust around AD 72. Doubt that yields to worship is the disciple’s arc.</p>'
    ),
    'three-fold-cord': (
        '<p>The three-fold cord is Ecclesiastes’ image of strength-in-fellowship: <em>"Two are better than one; because they have a good reward for their labour. For if they fall, the one will lift up his fellow... and if one prevail against him, two shall withstand him; and a threefold cord is not quickly broken"</em> (<em>Ecclesiastes 4:9-12</em>). The standard application is friendship and partnership — two are stronger than one; three are stronger still. The Christian application often (rightly) adds: the third strand is God Himself in the relationship — every covenant friendship, every marriage, every ministry partnership held together at the center by the LORD. Christian men should not try to walk alone. Find your second strand; let God be the third.</p>'
    ),
    'unfeigned': (
        '<p>"Unfeigned" — KJV for <em>without pretense, without play-acting, without a mask</em> — names the inward reality matching the outward show. The Greek <em>anupokritos</em> means literally "un-hypocritical." Paul prizes <em>"unfeigned faith"</em> in Lois, Eunice, and Timothy (<em>2 Timothy 1:5</em>); <em>"love unfeigned"</em> as a mark of true apostolic ministry (<em>2 Corinthians 6:6</em>); and <em>"unfeigned love of the brethren"</em> as the Spirit’s purifying fruit (<em>1 Peter 1:22</em>). The wisdom from above is <em>"without partiality, and without hypocrisy"</em> (<em>James 3:17</em>). The world masters the practiced sincerity — the polished performance of feeling. The Christian must be marked by the un-performed real thing. Whatever the world will fake, the saint must actually be.</p>'
    ),
    'vanity-of-vanities': (
        '<p>"Vanity of vanities" is Ecclesiastes’ opening and closing refrain: <em>"Vanity of vanities, saith the Preacher, vanity of vanities; all is vanity"</em> (<em>Ecclesiastes 1:2; 12:8</em>). The Hebrew <em>havel havalim</em> ("breath of breaths") uses the superlative-of-superlatives construction — the same form as <em>holy of holies</em> and <em>song of songs</em>. <em>Hevel</em> originally means "vapor, breath, mist": something insubstantial that disappears the moment you try to grasp it. The Preacher’s diagnostic is that life lived <em>"under the sun"</em> — considered apart from God — is fleeting, vaporous, futile. The remedy is in the closing verse: <em>"Fear God, and keep his commandments: for this is the whole duty of man"</em> (<em>12:13</em>). Vapor terminates in fearing God.</p>'
    ),
    'abner': (
        '<p>Abner son of Ner was the cousin of King Saul and the commander of his armies — the chief military strategist of the house of Saul. After Saul’s death at Mount Gilboa, Abner set up Saul’s surviving son Ish-bosheth as a rival king to David, ruling the northern tribes from Mahanaim (<em>2 Samuel 2:8-10</em>). A two-year civil war followed. Eventually Abner defected to David, bringing the northern tribes with him (<em>2 Samuel 3:6-21</em>) — only to be murdered at Hebron by Joab in private revenge for Joab’s brother Asahel, whom Abner had killed in self-defense at the pool of Gibeon. David lamented Abner publicly: <em>"Died Abner as a fool dieth?"</em> (<em>2 Samuel 3:33</em>). Joab’s blood-feud cost the kingdom a uniter.</p>'
    ),
    'anselm': (
        '<p>Anselm of Canterbury (1033-1109) was an Italian-born Benedictine monk who became Archbishop of Canterbury under William II. His <em>Cur Deus Homo</em> (<em>Why God Became Man</em>) gave the medieval and Reformation churches their classic <em>satisfaction theory</em> of the atonement: human sin offends God’s infinite honor, and only a sacrifice of infinite worth — therefore the God-man — can satisfy what is owed. The argument is the seedbed of Reformed penal substitution. His <em>Proslogion</em> contained the first formulation of the ontological argument for God’s existence (<em>"that than which nothing greater can be conceived"</em>). His motto, <em>"fides quaerens intellectum"</em> ("faith seeking understanding"), still names the right posture of Christian theology — never faith fleeing reason, never reason without faith.</p>'
    ),
    'bestie': (
        '<p>"Bestie" is the casual diminutive of <em>best friend</em>, often performative — used freely on social media for relationships of widely varying depth. The category Scripture knows is far heavier: covenant friendship, like Jonathan and David, who <em>"made a covenant, because he loved him as his own soul"</em> (<em>1 Samuel 18:3</em>); iron-sharpens-iron — <em>"Iron sharpeneth iron; so a man sharpeneth the countenance of his friend"</em> (<em>Proverbs 27:17</em>); <em>"a friend that sticketh closer than a brother"</em> (<em>Proverbs 18:24</em>). Most of what the world calls <em>besties</em> are not biblical friends; some biblical friends would never call themselves <em>besties</em>. Recover the older category: covenant loyalty, sharpening words, lifelong commitment. Friendship is heavier than the slang allows.</p>'
    ),
    'brook': (
        '<p>A brook is a small stream or seasonal watercourse — and in Scripture it serves as both the channel of private provision and a setting of high drama. Elijah hid by the brook Cherith, where the ravens fed him morning and evening, and where he drank as long as the brook ran (<em>1 Kings 17:3-7</em>). David hid from Saul at En Gedi and Adullam, by such brooks. Most famously, Christ crossed the brook Kidron on the night of His arrest, going into the garden of Gethsemane: <em>"When Jesus had spoken these words, he went forth with his disciples over the brook Cedron"</em> (<em>John 18:1</em>). The brook is the scale at which God often sustains His saints — quiet, narrow, enough.</p>'
    ),
    'covenant-breaker': (
        '<p>A covenant breaker is one who violates the terms of a sworn covenant — one whose word does not bind himself. Paul names them in the catalogue of moral collapse at the end of <em>Romans 1</em>: <em>"without understanding, covenantbreakers, without natural affection, implacable, unmerciful"</em> (<em>Romans 1:31</em>). The category is structurally severe in Scripture, because covenant is the form of every serious bond — marriage covenant, business covenant, friendship covenant, citizenship covenant, baptismal covenant. The covenant-breaker is therefore a man whose civilization-fabric is already dissolving inside him; his word means nothing because his soul means nothing. The Christian man, by contrast, swears to his own hurt and changes not (<em>Psalm 15:4</em>). Keep covenant. Even when it costs you.</p>'
    ),
    'good-name': (
        '<p>A good name is the integrated reputation a man builds by character over time — more valuable than great wealth, better than precious ointment. Proverbs is emphatic: <em>"A good name is rather to be chosen than great riches, and loving favour rather than silver and gold"</em> (<em>Proverbs 22:1</em>). Ecclesiastes adds: <em>"A good name is better than precious ointment"</em> (<em>Ecclesiastes 7:1</em>). A good name is not crafted brand or curated image; it is the actual moral standing a man earns by years of integrity — the way his word is taken in the city gates, the way his handshake is trusted, the way his absence is noted. It is built slowly; it is ruined quickly; it is central to biblical character.</p>'
    ),
    'incense-altar': (
        '<p>The incense altar was the small gold-overlaid altar (one cubit square, two cubits high) that stood in the Holy Place of the tabernacle, just before the veil of the Most Holy (<em>Exodus 30:1-10; 37:25-28</em>). Twice daily — morning and evening — the priest burned a specially compounded incense of stacte, onycha, galbanum, and pure frankincense (<em>Exodus 30:34-38</em>) on its surface. The smoke was a continual, fragrant symbol of the people’s prayers ascending to God (<em>Psalm 141:2</em>; <em>Revelation 5:8; 8:3-4</em>). Strange fire on this altar killed Nadab and Abihu (<em>Leviticus 10:1-2</em>). Christ Himself is now our incense altar — His prayers continually ascend on behalf of the saints (<em>Hebrews 7:25</em>).</p>'
    ),
    'incline-ear': (
        '<p>"Incline the ear" names the deliberate act of bending the ear toward the speaker — the active, bodily discipline of attentive listening. Scripture uses the phrase in both directions. God inclines His ear to hear the saint’s prayer: <em>"Bow down thine ear, O LORD, hear me: for I am poor and needy"</em> (<em>Psalm 86:1; cf. 17:6; 31:2; 71:2</em>) — and the saint declares with confidence, <em>"because he hath inclined his ear unto me, therefore will I call upon him as long as I live"</em> (<em>Psalm 116:2</em>). And the saint inclines the ear to hear God’s word: <em>"Bow down thine ear, and hear the words of the wise"</em> (<em>Proverbs 22:17</em>). The verb names listening as bodily posture: not casual reception but leaning-in.</p>'
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
