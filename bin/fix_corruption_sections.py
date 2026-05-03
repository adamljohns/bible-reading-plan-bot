#!/usr/bin/env python3
"""Bulk-fix the 97 entries flagged BAD by audit_corruption_sections.py.

For each slug, replaces the entire <div class="corruption-inner">...</div>
block with new content. Two flavors:
  - bespoke: a real description of the postmodern corruption
  - caveat:  honest "no major postmodern corruption" note for words whose
             force has simply faded from common usage

After running, the corruption_summary line above the <details> remains the
same (it usually was already corruption-talk); only the expandable inner
paragraph changes.
"""
import os, re, sys

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'docs', 'dictionary')

# Generic caveat templates
CAVEAT_PERSON = ('<p><em>No major postmodern redefinition of this figure. '
                 'The risk is simply that they fade from common Christian vocabulary, '
                 'and the lessons their life teaches fade with them. Recover the figure to recover the lesson.</em></p>')

CAVEAT_PLACE = ('<p><em>No major postmodern redefinition of this place. '
                'The risk is that the geographic-symbolic resonance Scripture builds with it gets lost — '
                'modern readers skim past place-names that the biblical writers used as shorthand for whole histories.</em></p>')

CAVEAT_BOOK = ('<p><em>No major postmodern corruption of the book itself. '
               'The risk is simply that it gets read less, or read past. The corruption that hides in the gap '
               'is the corruption of forgetting — and forgetting Scripture is the slow corruption.</em></p>')

CAVEAT_LITURGY = ('<p><em>No major postmodern redefinition. The risk is its absence — '
                  'evangelical worship has often dropped this element, leaving a gap where formation used to happen. '
                  'Recover the practice; the empty hour fills with worse things.</em></p>')

CAVEAT_GENERIC = ('<p><em>No significant postmodern redefinition of this word — its force has simply faded '
                  'from common Christian vocabulary. Recover the word and you often recover the precision it brings.</em></p>')

# Bespoke replacements — real postmodern corruptions
BESPOKE = {
    'mocker': '<p>The age glamorizes the mocker. Comedy culture, takedown columns, ironic detachment, and cancel-mob dynamics all reward skilled mockery as wit. Scripture treats it as a moral category — the disposition of the heart that has hardened against truth. The corruption is not just trivializing the word; it is celebrating the disposition.</p>',

    'derision': '<p>Therapy-culture has banished derision as toxic, even when Scripture itself uses it (Psalm 2:4 — God holds rebellious kings in derision). The corruption swings two ways: secular culture mocks the holy with no shame, while Christians become afraid to name evil with the sharpness Scripture itself uses. Both extremes flatten the moral landscape.</p>',

    'blasphemer': '<p>Modern speech has emptied "blasphemy" of its weight — it now means "anything mildly offensive to a religious group" rather than "speech that injures the honor of God." The corruption is double: secular culture treats blasphemy as a quaint medieval concept; meanwhile, actual speech against God\'s character circulates freely without alarm.</p>',

    'ridicule': '<p>Ridicule has been recoded as legitimate political and cultural weapon — late-night television, viral takedowns, public shaming campaigns. The age defends it as "punching up." Scripture treats it as a weapon often deployed against godly work; Sanballat ridiculed before he attacked, and the cross-watchers ridiculed the Crucified.</p>',

    'absolute': '<p>Postmodernism\'s slogan "there are no absolutes" is itself an absolute claim — a self-defeating proposition. Relativism is marketed as humility ("who am I to say?") but functions as a refusal to be governed by anything outside the self. The corruption is making relativism feel like virtue while it is in fact the proud heart\'s refusal of authority.</p>',

    'advent-season': '<p>Advent gets compressed into commercial Christmas-prep — a three-week shopping countdown with sentimental music. The eschatological half (Christ\'s second coming in glory) is dropped almost entirely, leaving only the cozy first-coming half. The result is a sentimentalized season missing its hard edge of judgment-and-hope.</p>',

    'bible-translation': '<p>Bible translation has been politicized — partisan camps treat translations as tribal markers ("real Christians use the KJV / ESV / NIV"). Meanwhile, post-colonial critics treat all translation as cultural imposition. Both miss the Pentecostal vision: every people hearing in their own tongue. The corruption is partisanship displacing Pentecost.</p>',

    'chain': '<p>Modern self-help reframes spiritual chains as "limiting beliefs" or "trauma patterns" that the inner self can dissolve through mindset and practice. The biblical reality — that humans are bound by sin and Satan and death until Christ sets free — is replaced by a smaller story of self-actualization. Smaller chains, smaller Liberator.</p>',

    'child': '<p>Modern culture reframes children primarily as lifestyle choices to be optimized — when to have, how many, with what credentials, on what timeline. The biblical category of heritage / image-bearer / soul-to-be-formed gets obscured by economic and aspirational framings. Abortion makes the corruption literal: personhood denied at the convenient moment.</p>',

    'continence': '<p>Therapy-culture has reframed continence as repression and repression as harmful, with the result that any desire-restraint is suspect. Scripture distinguishes Spirit-given mastery from white-knuckle suppression — but the modern conversation has lost the distinction. The corruption is making the virtue feel like the pathology.</p>',

    'covenant-faithfulness': '<p>Contemporary culture treats faithfulness as obsolete idealism — relationships are "as long as it works," institutions are "earned trust" not given loyalty, vows are negotiable when circumstances change. The corruption is replacing the covenant frame entirely with the contract frame. Covenants bind through circumstance; contracts expire when convenient.</p>',

    'dove-harmless': '<p>Modern usage of "harmless" implies passivity or doormat-ism — the harmless person is the one without backbone. Christ\'s pairing — wise as serpents, harmless as doves — gets reduced to "be nice." The serpent half drops out; the dove half becomes naivete. The full pairing of shrewd-pure gets lost.</p>',

    'effectual-call': '<p>Modern evangelism often blurs the inward effectual call into the outward gospel call, treating decision-card-signing as itself the call. The corruption flattens what Scripture distinguishes: God\'s sovereign drawing of the elect (effectual) versus the universal proclamation. Lose the distinction and you lose both the urgency of the gospel call and the assurance of God\'s sovereign work.</p>',

    'eternal-state': '<p>Pop-Christian afterlife imagery — clouds, harps, floating souls, family reunions — corrupts the biblical eternal state which is bodily resurrection, new heavens and new earth, restored creation under Christ\'s reign. The corruption substitutes Greek dualism for Hebrew-Christian holism, leaving believers with a thinner, vaguer, and less hopeful vision than Scripture actually provides.</p>',

    'eternality': '<p>Modern theology reduces God\'s eternality to "lasting forever" — God as a creature with a longer battery. Scripture\'s richer claim is that God transcends time itself; He is the I AM, holding all moments at once. The corruption makes God smaller — older than the universe but still inside its river — and so makes His promises feel only as durable as time.</p>',

    'father': '<p>The cultural crisis of fatherhood — absent dads, mocked dads, "toxic masculinity" framings — has bled into how Christians hear "Father" in Scripture. Some flinch at the word; others demand alternatives. The corruption is not in Scripture but in the cultural noise around the word; the pastoral work is to recover Father-language as Christ Himself uses it (Abba) without apology.</p>',

    'flee': '<p>"Flee" sounds cowardly to modern ears — we\'re trained to confront, engage, and lean in. Scripture distinguishes contexts: flee youthful lusts, flee idolatry, flee the love of money. Some battles are won by retreat. The corruption is making fleeing feel weak when Paul commands it as wisdom.</p>',

    'forty-biblical': '<p>Numerology cranks have corrupted forty-symbolism — turning a biblical number into prediction code. Scripture\'s simpler use is rhythm: forty days of testing, forty years of formation, forty days of resurrection appearance. The corruption is the speculation, not the symbolism. Recover the rhythm without the codebreaking.</p>',

    'fruit-bearing': '<p>Performance-Christianity has weaponized fruit-bearing as quantifiable output — souls saved, programs run, growth metrics. The biblical fruit (love, joy, peace, longsuffering...) is character-fruit produced by the Spirit, not output-fruit produced by ministry strategy. The corruption is replacing patient cultivation with dashboard reporting.</p>',

    'gentleness-biblical': '<p>Modern usage equates gentleness with niceness or weakness — the "gentle" person is conflict-averse and inoffensive. Scripture\'s gentleness is meekness — controlled strength under God\'s direction, capable of rebuking false teachers and turning over moneychanger tables when needed. The corruption is making it the absence of force rather than its right ordering.</p>',

    'goel': '<p>The kinsman-redeemer concept gets reduced to romance-novel material because of Boaz-and-Ruth, missing the harder edge: a goel could also avenge blood, redeem property at cost, and refuse the role if it endangered his own inheritance. The corruption is sweetening what Scripture treats with full legal and economic seriousness.</p>',

    'government': '<p>Romans 13 ("the powers that be are ordained of God") gets weaponized in two opposite directions: by authoritarian regimes demanding unconditional obedience, and by libertarian Christians dismissing all government as illegitimate. The corruption is using one verse to override the rest of Scripture\'s teaching on lawful authority, prophetic resistance, and the limits of human rule.</p>',

    'hades-realm': '<p>Translations conflating Hades with Gehenna ("hell" for both) corrupt Scripture\'s careful eschatology. The intermediate state and the final state get mashed into one undifferentiated "hell," obscuring Scripture\'s actual ordering: Hades itself is cast into the lake of fire at the final judgment. The corruption blurs precision; recovering the distinction recovers the doctrine.</p>',

    'hallelujah-acclamation': '<p>"Hallelujah" has been secularized into general celebration ("hallelujah, the weekend is here") and commodified through pop songs that drain the word of its God-praise meaning. The corruption is severing the imperative ("praise YHWH") from its object until "hallelujah" means "I\'m happy" rather than "praise the LORD."</p>',

    'heart-bold': '<p>Modern self-help has rebranded boldness as self-confidence — believing in yourself, owning your power. Biblical boldness is grounded in Christ\'s finished work and the Spirit\'s presence; it is courage rooted outside the self. The corruption makes boldness another self-actualization tool rather than the gospel-rooted access to the throne of grace.</p>',

    'honesty': '<p>"Honesty" has been narrowed in modern usage to "not lying with words" — leaving room for false weights, misleading framing, evasive answers, and exploitative contracts that are technically true. Scripture\'s honesty is integrated: true word, true weight, true work, true witness. The corruption is the narrowing.</p>',

    'kindness-biblical': '<p>Modern kindness has been sentimentalized into "being nice" — affirming whatever people feel, affirming whatever choices people make. Scripture\'s hesed-kindness is covenantal loyalty that may include hard truth, costly commitment, and unwelcome correction. The corruption replaces covenant loyalty with mood management.</p>',

    'kyrie': '<p>Some Protestant subcultures dismiss the Kyrie as Catholic ritual, missing how thoroughly biblical the cry is — the publican, the blind men, the Canaanite woman all prayed it. The corruption is rejecting biblical vocabulary because of associations rather than receiving the cry of every needy soul that ever came to Christ.</p>',

    'last-enemy': '<p>Death has been medicalized, professionalized, and removed from the household — outsourced to hospitals and funeral homes — until it functions as event-management rather than the enemy Paul names. The corruption is treating death as natural rather than as the last enemy Christ has defeated and will finally destroy.</p>',

    'leaving-cleaving': '<p>Modern marriage culture preserves "cleaving" rhetorically while gutting "leaving" — adult children remain emotionally tethered to parents, parents continue managing married children\'s lives. The result is marriages that never form their own household identity. The corruption is the half-execution of the biblical pattern.</p>',

    'lent-season': '<p>Lent has been reduced to "give up chocolate" — a lifestyle tweak that empties the season of its repentance-and-fasting weight. Some traditions treat Lent as legalism; others perform it as Instagram-virtue. The corruption is either dismissing it or curating it, when Scripture\'s pattern is forty days of intensified gospel preparation.</p>',

    'lowliness-biblical': '<p>Modern self-esteem culture pathologizes lowliness as bad self-image, making humility feel toxic. Scripture\'s tapeinophrosynē is honest self-knowledge plus active esteem of others — Christ\'s pattern in Philippians 2. The corruption is reading humility as self-loathing rather than as right reckoning of the self in light of Christ.</p>',

    'money': '<p>Both prosperity gospel and certain ascetic strains corrupt money — the first sacralizing it as proof of God\'s favor, the second demonizing it as inherently evil. Scripture\'s actual teaching is that money is steward-test, not enemy: morally neutral as instrument, deeply tested in heart. The corruption swings between the two extremes.</p>',

    'naturalism-philosophical': '<p>Philosophical naturalism — the claim that nothing exists beyond the material — is marketed as "science" itself, conflating method with metaphysics. The corruption is pretending naturalism is the conclusion of evidence rather than the unprovable premise smuggled in before evidence is examined.</p>',

    'naturalism': '<p>Methodological naturalism (the practical assumption that scientific work explains via natural causes) gets quietly inflated into metaphysical naturalism (the claim that only natural causes exist). The corruption is the slide from method to metaphysics, often invisible to the speaker.</p>',

    'paedobaptism': '<p>Both sides of the baptism debate corrupt it: paedobaptism reduced to family tradition without covenant theology, or credobaptism turned into individualistic decisionism without covenantal context. The corruption is treating baptism\'s covenant frame as optional, leaving the practice without its theological skeleton.</p>',

    'pantheism': '<p>"God is in everything / everything is God" repackages pantheism as spirituality, marketed in wellness culture, yoga, and "we\'re all one" sloganism. The corruption is making it sound humble and inclusive while it actually denies the Creator-creature distinction Scripture builds everything on.</p>',

    'pentecost-season': '<p>Pentecost has been marginalized in much of Western Christianity — Christmas and Easter get the attention; Pentecost gets a sermon and disappears. The corruption is treating the Spirit\'s coming as liturgical decoration rather than as gospel-history coordinate with incarnation and resurrection.</p>',

    'phylactery': '<p>Modern Christians often dismiss phylacteries as Pharisaic legalism, missing that Jesus did not abolish the practice — He rebuked the showy enlargement. The corruption is reading Matthew 23:5 as condemnation of the phylactery itself rather than of the heart that wears it for show.</p>',

    'punctuality': '<p>"Time is fluid / be where your feet are" rhetoric makes habitual lateness sound holy or relaxed. Scripture treats time-keeping as love-of-neighbor (their time matters) and integrity (yes-means-yes). The corruption is reframing tongue-of-promise as personality preference.</p>',

    'qualifications-deacon': '<p>Modern church culture often treats deacon as a junior office requiring lower standards — entry-level church position. Paul\'s list is nearly as rigorous as the elder list. The corruption is treating the office as developmental rather than as its own dignity with its own bar.</p>',

    'reparation': '<p>Cheap-grace theology drops reparation entirely — God forgives, the matter is closed, no further action required. Scripture maintains that forgiven sin can still owe restitution to the wronged neighbor. The corruption is using vertical forgiveness to nullify horizontal obligation.</p>',

    'rod-of-correction': '<p>Both extremes corrupt the rod: harsh corporal punishment treated as Christian command, OR all parental discipline pathologized as abuse. Scripture\'s wisdom is calibrated correction in love, neither absent nor abusive. The corruption is reading proverbs without their wisdom-context.</p>',

    'sanctus': '<p>Some Protestant subcultures avoid the Sanctus as "too Catholic," dropping a hymn that is straight from Isaiah 6 and Revelation 4. The corruption is rejecting biblical worship-vocabulary because of associations rather than because of content.</p>',

    'semper-fidelis': '<p>The Marine motto has secularized "semper fi" into branch-loyalty and brand-marketing, draining the deeper Christian heritage of the phrase — always faithful to God\'s covenant and His people. The corruption is patriotic appropriation displacing the original devotional meaning.</p>',

    'shoes-of-gospel': '<p>The "shoes of the gospel of peace" gets sentimentalized as comfortable walking shoes for Christian life. Paul\'s image is Roman military footwear — hobnailed, traction-built, ready for battle. The corruption is replacing combat-readiness with comfort.</p>',

    'silver-biblical': '<p>Silver in modern usage is just precious metal; Scripture uses it as the measure of redemption (thirty pieces, the sanctuary shekel) and the test of refinement (silver tried in the furnace). The corruption is losing silver\'s symbolic load — which makes Judas\'s thirty pieces lose their narrative weight.</p>',

    'sincerity-biblical': '<p>Modern usage shrinks "sincere" to "meaning what you say" — earnest delivery. Scripture\'s eilikrineia is purity of motive — undisguised, unfilled, no wax in the cracks. The corruption is reducing the depth: a person can be sincere in delivery while having mixed motives, but not sincere in Scripture\'s sense.</p>',

    'socinianism': '<p>Socinianism\'s descendants — modernist liberalism, certain progressive Christianities, Unitarian Universalism — recur whenever rationalism overrides revelation. The corruption is rebranding the same anti-Trinitarian, anti-substitution moves under fresh names while claiming to be the cutting edge.</p>',

    'sow': '<p>Prosperity teachers have weaponized "you reap what you sow" into seed-faith money schemes — sow into my ministry to reap your harvest. The corruption inverts the moral seriousness of the principle (Galatians warns the corrupting flesh-sower) into transactional manipulation.</p>',

    'sweat-blood': '<p>Pop psychology medicalizes hematidrosis as rare-but-natural; the gospel writers present it as the weight of the cup Christ accepted. The corruption is making Gethsemane a medical curiosity rather than a window into the Lord\'s agony before substitutionary atonement.</p>',

    'sympathy': '<p>Modern usage often treats sympathy as condescension — "I\'m sorry that\'s happening to you" from a distance. Scripture\'s sympatheia is suffering-with: Christ as our High Priest does not look down on infirmities, He shares them. The corruption is reframing co-suffering as managed pity.</p>',

    'tetelestai': '<p>Common translations soften tetelestai to "it is finished" without conveying the receipt-stamp force ("paid in full"). The corruption is reading the cross as a conclusion ("Jesus died, the end") rather than as a verdict ("paid"). Whatever you add to a paid receipt diminishes it.</p>',

    'throne-of-grace': '<p>"Come boldly to the throne of grace" gets either casualized into flippancy (we walk in like buddies) or weighted back into fearful approach (still need a mediator, still tentative). The corruption is at either extreme; the boldness is real because the blood is sufficient — neither flippant nor timid.</p>',

    'unchangeable': '<p>Process theology and open theism both deny divine unchangeableness, marketing change-in-God as relational warmth. The corruption is selling reduction as enrichment — a god who learns and grows feels relatable but cannot keep promises whose fulfillment depends on knowing the future.</p>',

    'undershepherd': '<p>Pastor-as-CEO and pastor-as-celebrity replace pastor-as-undershepherd — the title is kept, the content is swapped. The corruption is invisibly inflating the office: the steward of the flock becomes the owner-operator, accountable to performance metrics rather than to the Chief Shepherd.</p>',

    'vexation': '<p>Modern usage reduces "vexation" to mild annoyance — "vexed" means "irritated." Scripture uses it for Lot\'s daily ache at Sodom\'s wickedness and Ecclesiastes\' cry of futility under the sun. The corruption flattens the vocabulary of moral and existential distress into a personality state.</p>',

    'vows': '<p>Contemporary culture treats vows as aspirational language — what you intend, contingent on circumstances. Scripture treats them as binding the moment they are spoken. The corruption is the soft escape clause that did not exist in Ecclesiastes 5 ("better not to vow than to vow and not pay").</p>',

    'weeks-feast': '<p>Christian calendars often reduce Pentecost / Weeks to Acts 2 alone, dropping the harvest-firstfruits dimension that Leviticus 23 builds. The corruption is reading Pentecost as an isolated miracle event rather than as the pre-figured firstfruits-of-Spirit harvest the feast calendar always pointed to.</p>',

    'work': '<p>Modern culture splits work between drudgery (something endured for the paycheck) and self-actualization (a vehicle for personal fulfillment). Scripture\'s work — Eden good, fall-cursed, redeemed in Christ — is neither. The corruption is treating work as transactional or as identity rather than as worship rendered to the Lord.</p>',
}

# Caveat-only slugs grouped by category
PERSONS = ['agabus', 'ahab', 'ahasuerus', 'andrew', 'hosea', 'jehu', 'joab', 'josiah',
           'malachi', 'mephibosheth', 'miriam', 'obadiah', 'othniel', 'prophetess',
           'the-twelve', 'luke-figure', 'judah', 'zechariah']
PLACES  = ['ashdod', 'bashan', 'caesarea', 'carmel', 'cyprus', 'edom', 'gaza', 'gilead',
           'haran', 'joppa', 'megiddo', 'midian-place', 'moab', 'jerusalem-city', 'laodicea']
BOOKS   = ['acts', 'hebrews-book', 'jonah-book', 'philemon-book', 'zechariah-book']

# Pattern to find and replace the corruption-inner block
INNER_BLOCK_PAT = re.compile(
    r'(<div class="corruption-inner">)(.*?)(</div>\s*</details>)',
    re.DOTALL
)


def fix_entry(slug):
    fp = os.path.join(DICT_DIR, slug + '.html')
    if not os.path.exists(fp):
        return False, 'file not found'
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()

    # Determine new content
    if slug in BESPOKE:
        new_inner = BESPOKE[slug]
    elif slug in PERSONS:
        new_inner = CAVEAT_PERSON
    elif slug in PLACES:
        new_inner = CAVEAT_PLACE
    elif slug in BOOKS:
        new_inner = CAVEAT_BOOK
    else:
        new_inner = CAVEAT_GENERIC

    # Replace
    def replacer(m):
        return m.group(1) + '\n                    ' + new_inner + '\n                ' + m.group(3)
    new_html, n = INNER_BLOCK_PAT.subn(replacer, html, count=1)
    if n == 0:
        return False, 'pattern not matched'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'


def main():
    bad_slugs = """
absolute acts advent-season agabus ahab ahasuerus andrew ashdod bashan
bible-translation blasphemer caesarea carmel chain child continence
covenant-faithfulness cyprus derision dove-harmless edom effectual-call
eternal-state eternality father flee forty-biblical fruit-bearing gaza
gentleness-biblical gilead goel government hades-realm hallelujah-acclamation
haran heart-bold hebrews-book honesty hosea jehu jerusalem-city joab
jonah-book joppa josiah judah kindness-biblical kyrie laodicea last-enemy
leaving-cleaving lent-season lowliness-biblical luke-figure malachi megiddo
mephibosheth midian-place miriam moab mocker money naturalism-philosophical
naturalism obadiah othniel paedobaptism pantheism pentecost-season
philemon-book phylactery prophetess punctuality qualifications-deacon
reparation ridicule rod-of-correction sanctus semper-fidelis shoes-of-gospel
silver-biblical sincerity-biblical socinianism sow sweat-blood sympathy
tetelestai the-twelve throne-of-grace unchangeable undershepherd vexation
vows weeks-feast work zechariah-book
""".split()

    ok, fail = 0, 0
    for slug in bad_slugs:
        success, reason = fix_entry(slug)
        if success:
            ok += 1
        else:
            fail += 1
            print(f"FAIL: {slug} — {reason}")
    print(f"\nFixed {ok} / {ok+fail} entries")


if __name__ == '__main__':
    main()
