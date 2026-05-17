#!/usr/bin/env python3
"""Expand 25 more short dictionary entries to 90-120 words each (batch 3)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'submission-biblical': (
        '<p>The willing placement of oneself under God-appointed authority for the good of the whole. The Greek '
        '<em>hypotasso</em> (to arrange under) is a military term &mdash; ordered ranks, each soldier under the next, '
        'all under the commander. Scripture commands mutual submission among believers (Eph 5:21: <em>submitting '
        'yourselves one to another in the fear of God</em>), wives to husbands (Eph 5:22-24), children to parents '
        '(Eph 6:1), servants to masters (Eph 6:5), citizens to magistrates (Rom 13:1; 1 Pet 2:13), younger to elder '
        '(1 Pet 5:5), and all Christians to Christ as Head (Eph 5:23-24). The Father-Son submission within the '
        'Trinity (1 Cor 11:3; 15:28) is the eternal pattern. Biblical submission is not weakness; it is the active '
        'strength of placing one\'s will under God\'s ordered authority, knowing the authority is itself accountable '
        'to the One who established it. Christ\'s own submission to the Father in Gethsemane (<em>not my will, but '
        'thine, be done</em>) is the highest expression of the virtue.</p>'
    ),
    'unforgivable-sin': (
        '<p>The blasphemy against the Holy Spirit named by Christ as the one sin that has no forgiveness. Mark 3:28-30: '
        '<em>Verily I say unto you, All sins shall be forgiven unto the sons of men, and blasphemies wherewith soever '
        'they shall blaspheme: But he that shall blaspheme against the Holy Ghost hath never forgiveness, but is in '
        'danger of eternal damnation: because they said, He hath an unclean spirit.</em> The context is decisive: '
        'the Pharisees, seeing Christ\'s miraculous works performed by the Spirit, attributed them to Beelzebub. '
        'The sin is not a single word but a settled, willful, irrevocable attribution of the Spirit\'s saving work '
        'to the devil &mdash; the heart that has so fully and finally hardened against the Spirit\'s testimony of '
        'Christ that it cannot repent. The genuinely worried Christian is, by definition, not committing it; the '
        'concern itself is evidence of the Spirit\'s ongoing work. The unforgivable sin is the final state of '
        'apostasy that no longer wants forgiveness.</p>'
    ),
    'repent': (
        '<p>Biblical repentance is not mere remorse, regret, or sorrow over consequences; it is a complete '
        'reorientation of the heart and life. Hebrew <em>shub</em> (turn, return) and Greek <em>metanoeo</em> '
        '(change one\'s mind) together carry the full sense: a turning <em>from</em> sin and <em>to</em> God, '
        'with the mind reordered, the will reset, and the conduct reformed. John the Baptist preached repentance '
        '(Matt 3:2), Christ\'s first recorded sermon was <em>repent: for the kingdom of heaven is at hand</em> '
        '(Matt 4:17), and Paul summarized his ministry as testifying to <em>repentance toward God, and faith '
        'toward our Lord Jesus Christ</em> (Acts 20:21). Scripture distinguishes godly sorrow that works repentance '
        'from worldly sorrow that works death (2 Cor 7:10). True repentance produces visible fruit (Luke 3:8) &mdash; '
        'not just better feelings, but a changed life. It is gift (2 Tim 2:25) and command (Acts 17:30) at once.</p>'
    ),
    'rest-faith': (
        '<p>The believer\'s entering into the rest God promised, ceasing from self-justifying works and resting '
        'in Christ\'s finished work. Hebrews 4 develops the theme: the Sabbath of Genesis 2, the Promised-Land '
        'rest that Israel forfeited through unbelief, and the eschatological rest still remaining for the people '
        'of God (<em>there remaineth therefore a rest to the people of God</em>, Heb 4:9). The Greek '
        '<em>sabbatismos</em> (Sabbath-rest) appears only here in the NT &mdash; a unique term naming the unique '
        'reality. The rest of faith is entered now (Heb 4:3: <em>for we which have believed do enter into rest</em>) '
        'and consummated at the end. It is not idleness; the Christian still labors (Heb 4:11: <em>let us labour '
        'therefore to enter into that rest</em>) but labors from the rest, not for it. Christ\'s yoke is easy '
        'because His finished work is the foundation.</p>'
    ),
    'river-life': (
        '<p>The river of the water of life proceeding from the throne of God and the Lamb in the New Jerusalem. '
        'Revelation 22:1-2: <em>And he shewed me a pure river of water of life, clear as crystal, proceeding out '
        'of the throne of God and of the Lamb. In the midst of the street of it, and on either side of the river, '
        'was there the tree of life, which bare twelve manner of fruits, and yielded her fruit every month: and '
        'the leaves of the tree were for the healing of the nations.</em> The river is the culmination of biblical '
        'water-imagery: the four rivers of Eden (Gen 2:10-14), the river that makes glad the city of God (Ps 46:4), '
        'Ezekiel\'s temple-river that becomes a great current healing the Dead Sea (Ezek 47), Christ\'s promise '
        'that rivers of living water shall flow from the belly of him that believes (John 7:38). All converge '
        'at Revelation 22\'s eternal city &mdash; the river of life flowing endlessly from the throne, the tree '
        'of life restored.</p>'
    ),
    'sabbath-rest': (
        '<p>The seventh-day rest commanded at creation (Gen 2:2-3), codified in the fourth commandment (Ex 20:8-11), '
        'fulfilled and reframed in Christ (Heb 4:9-11). The Hebrew <em>shabbat</em> (cease, rest) names both the '
        'day and the disposition. The OT Sabbath was a holy convocation on the seventh day, marked by cessation '
        'from work, observance of holy assembly, and the memory of God\'s rest from creation and Israel\'s '
        'deliverance from Egypt (Deut 5:15). The NT shifts the locus to the Lord\'s Day (the first day of the '
        'week, Rev 1:10), the day of Christ\'s resurrection (Matt 28:1), and applies the deeper Sabbath as the '
        'rest of faith in Hebrews 4. The Christian Sabbath is not legalistic Pharisee-style restriction; it is '
        'the weekly enactment of the rest the gospel has accomplished &mdash; cessation from striving, gathering '
        'for worship, and the anticipation of the eternal Sabbath still to come.</p>'
    ),
    'shadow-almighty': (
        '<p>The image of God\'s protective covering, especially in Psalm 91. The opening verse: <em>He that '
        'dwelleth in the secret place of the most High shall abide under the shadow of the Almighty.</em> The '
        'Hebrew <em>tsel Shaddai</em> (shadow of the Almighty) draws on multiple registers: the shade that '
        'protects from desert sun, the eagle\'s wings that cover its young (Ps 91:4), the cloud that overshadowed '
        'Israel by day, the wings of the cherubim over the mercy seat. Throughout Scripture, the LORD\'s shadow '
        'is a covering that protects the believer from harm without confining him (Ps 17:8; 36:7; 57:1; 63:7; '
        'Isa 25:4). Christ Himself uses the image when He laments over Jerusalem: <em>how often would I have '
        'gathered thy children together, even as a hen gathereth her chickens under her wings, and ye would '
        'not!</em> (Matt 23:37). To dwell under the shadow of the Almighty is to take refuge in His care &mdash; '
        'not from circumstance but in the midst of it.</p>'
    ),
    'sinai-experience': (
        '<p>Israel\'s encounter with God at Mount Sinai (Ex 19-20) &mdash; the foundational event of the OT '
        'covenant. Three days after the people arrived, the mountain was wrapped in smoke <em>because the LORD '
        'descended upon it in fire</em> (Ex 19:18); the whole mountain quaked greatly; the voice of the trumpet '
        'grew louder; God spoke the Ten Commandments from the cloud. The people stood at a distance, trembling, '
        'asking Moses to mediate. Sinai established the Mosaic covenant, the law, the tabernacle pattern, and '
        'the priesthood. Hebrews 12:18-24 contrasts Sinai with Zion: the believer comes not to the terrifying '
        'mountain that could not be touched but to <em>mount Sion, and unto the city of the living God, the '
        'heavenly Jerusalem... and to Jesus the mediator of the new covenant, and to the blood of sprinkling, '
        'that speaketh better things than that of Abel</em>. Sinai is the necessary backdrop against which '
        'the new covenant\'s grace is measured.</p>'
    ),
    'stumbling-block': (
        '<p>Christ crucified, who scandalizes both Jewish religious expectations and Greek philosophical '
        'sensibilities. Paul: <em>We preach Christ crucified, unto the Jews a stumblingblock, and unto the '
        'Greeks foolishness; But unto them which are called, both Jews and Greeks, Christ the power of God, '
        'and the wisdom of God</em> (1 Cor 1:23-24). The Greek <em>skandalon</em> (stumblingblock, scandal, '
        'snare) is the trip-wire of the cross &mdash; the offense of a crucified Messiah for those expecting '
        'a victorious king (Jews) and of a saving God for those reasoning from philosophical-categories alone '
        '(Greeks). Christ Himself is named <em>a stone of stumbling and a rock of offence</em> (Rom 9:33; '
        '1 Pet 2:8) for those who refuse Him. The cross has not stopped scandalizing in 2026; it scandalizes '
        'modern moral-therapeutic religion, modern self-help spirituality, and modern political-utopian '
        'projects equally. To remove the scandal is to remove the gospel.</p>'
    ),
    'twelve-tribes': (
        '<p>The twelve sons of Jacob and their descendants, the foundational divisions of the covenant nation '
        'Israel. Reuben, Simeon, Levi, Judah, Dan, Naphtali, Gad, Asher, Issachar, Zebulun, Joseph (often '
        'replaced in inheritance lists by his sons Ephraim and Manasseh), and Benjamin (Gen 49). The twelve '
        'tribes structured Israel\'s territorial inheritance (Josh 13-19), military organization (Num 1), '
        'priestly service (Levi set apart, Num 3-4), and royal lineage (Judah, Gen 49:10). Christ chose '
        'twelve apostles, deliberately echoing the pattern (Matt 19:28). The book of Revelation places the '
        'twelve tribes at the foundation of the New Jerusalem alongside the twelve apostles of the Lamb '
        '(Rev 21:12-14), and twelve thousand from each tribe are sealed in Revelation 7. The number is '
        'covenantal, structural, and eschatological. The twelve tribes are not abolished in Christ; they are '
        'fulfilled in the people of God drawn from every tribe and nation.</p>'
    ),
    'unclean-spirit': (
        '<p>The biblical category for demonic spirits, especially as encountered in the Gospels and Acts. The '
        'Greek <em>akatharton pneuma</em> (unclean spirit) appears throughout the Synoptic Gospels: the '
        'demoniac of Mark 1:23-28, the Gerasene demoniac of Mark 5, the Syrophoenician woman\'s daughter '
        '(Mark 7:25-30), and many others. <em>Unclean</em> here is not merely <em>dirty</em>; it is the '
        'ritual-and-moral opposite of <em>holy</em>. Demons are <em>unclean</em> because they are spirits of '
        'rebellion against the Holy God. Christ\'s ministry of casting out unclean spirits demonstrated His '
        'authority over the entire spiritual realm (Mark 1:27: <em>even the unclean spirits, and they do '
        'obey him</em>) and signaled the in-breaking of the kingdom (Matt 12:28). Matthew 12:43-45 gives the '
        'warning: an unclean spirit cast out without the house being filled by the Spirit of God may return '
        'with seven worse than itself. Deliverance is real; the only durable replacement is the Holy Spirit\'s '
        'indwelling.</p>'
    ),
    'virgin-birth': (
        '<p>The doctrine that Jesus Christ was conceived in the womb of Mary by the Holy Spirit without any '
        'human father. Prophesied in Isaiah 7:14 (<em>Behold, a virgin shall conceive, and bear a son, and '
        'shall call his name Immanuel</em>); fulfilled and explicitly applied in Matthew 1:18-25 and Luke '
        '1:26-38 (Gabriel\'s annunciation: <em>The Holy Ghost shall come upon thee, and the power of the '
        'Highest shall overshadow thee</em>, Luke 1:35). The Hebrew <em>almah</em> in Isaiah 7:14 (translated '
        '<em>parthenos</em>, virgin, in the LXX) became one of the most contested words in OT-NT continuity. '
        'The doctrine is essential to orthodox Christology: the Virgin Birth secures Christ\'s sinlessness '
        '(He was not in Adam\'s line by ordinary generation), His divine origin (His Father is God), and His '
        'true humanity (He took flesh from Mary, the daughter of Adam). To deny the Virgin Birth is to lose '
        'the incarnation as Scripture presents it.</p>'
    ),
    'wine-new': (
        '<p>Fresh wine as a biblical symbol of the Spirit, the new covenant, and eschatological joy. Christ\'s '
        'parable: <em>neither do men put new wine into old bottles: else the bottles break, and the wine '
        'runneth out, and the bottles perish: but they put new wine into new bottles, and both are preserved</em> '
        '(Matt 9:17). The image: the new wine of the kingdom Christ is bringing cannot be contained within the '
        'old wineskins of legalistic Pharisaism; both need renewal. At Pentecost, the mockers accuse the '
        'disciples of being <em>full of new wine</em> (Acts 2:13) &mdash; an accusation Peter answers by '
        'explaining that what they see is the outpouring of the Spirit prophesied by Joel. New wine in '
        'Scripture also signals the eschatological feast (Isa 25:6; Joel 3:18; Amos 9:13; Christ\'s promise '
        'in Matt 26:29 to drink new wine with His disciples in the Father\'s kingdom). The Christian life is '
        'new wine in new wineskins &mdash; the Spirit-given joy of the kingdom.</p>'
    ),
    'soldier-christ': (
        '<p>Paul\'s charge to Timothy: <em>Thou therefore endure hardness, as a good soldier of Jesus Christ. '
        'No man that warreth entangleth himself with the affairs of this life; that he may please him who hath '
        'chosen him to be a soldier</em> (2 Tim 2:3-4). The Christian life is consistently framed in military '
        'metaphor: spiritual warfare (Eph 6:10-18), the weapons of warfare not carnal but mighty through God '
        '(2 Cor 10:4), the fight of faith (1 Tim 6:12; 2 Tim 4:7), and Christ Himself as Captain of the host '
        '(Josh 5:14-15) and Captain of our salvation (Heb 2:10). The Christian soldier is enlisted under Christ '
        'the Commander, fights against principalities and powers (not flesh and blood), endures the hardness '
        'of the long campaign, and refuses to be entangled with civilian affairs that would compromise his '
        'service. The metaphor is biblical, not optional; the Christian life is, properly understood, the life '
        'of a soldier on active deployment until the campaign\'s end.</p>'
    ),
    'standing-firm': (
        '<p>Paul\'s fivefold imperative in 1 Corinthians 16:13: <em>Watch ye, stand fast in the faith, quit you '
        'like men, be strong.</em> The Greek <em>stekete en te pistei</em> (stand fast in the faith) is one '
        'of Paul\'s favorite commands &mdash; appearing also in Eph 6:13-14 (<em>stand therefore, having your '
        'loins girt about with truth</em>), Phil 1:27 (<em>stand fast in one spirit</em>), Phil 4:1 (<em>so '
        'stand fast in the Lord</em>), 1 Thess 3:8, 2 Thess 2:15. The image is military: holding the line, '
        'refusing to retreat, maintaining the position the commander has assigned. Standing firm is not '
        'aggression or initiative but the disciplined refusal to give way under pressure. The pressures '
        'against which the Christian stands are doctrinal (false teaching), moral (temptation), social '
        '(persecution), and personal (despair). The means of standing is the armor of God (Eph 6:10-18), '
        'the truth of the gospel, the fellowship of the saints, and the Spirit\'s power. Christians stand '
        'because God stands them; the standing is the result of having been made to stand (Rom 14:4).</p>'
    ),
    'sword-spirit': (
        '<p>Paul\'s identification of the Christian\'s offensive weapon in Ephesians 6:17: <em>And take the '
        'helmet of salvation, and the sword of the Spirit, which is the word of God.</em> Of the six pieces '
        'of armor Paul names, all are defensive (belt, breastplate, shoes, shield, helmet) except this one '
        '&mdash; the sword. The Greek <em>machaira</em> (short sword) is the close-quarters weapon, used for '
        'the precise strike. The sword is the <em>word of God</em>: Greek <em>rhema</em> (the spoken/applied '
        'word) rather than <em>logos</em> (the written corpus), emphasizing the active deployment of Scripture '
        'against specific spiritual attacks. Christ\'s own use of the sword is the model: in the wilderness '
        'temptation, He answered each of Satan\'s lies with a specific Scripture verse (<em>It is written</em>, '
        'Matt 4:4, 7, 10). Hebrews 4:12 calls the word <em>quick, and powerful, and sharper than any twoedged '
        'sword, piercing even to the dividing asunder of soul and spirit</em>. The Christian who has memorized '
        'Scripture has the sword in hand; the Christian who has not is unarmed in close combat.</p>'
    ),
    'unfailing-love': (
        '<p>The Hebrew <em>hesed</em> &mdash; God\'s covenant-faithful, loyal-loving steadfast love. The word '
        'appears 245 times in the OT and is variously translated <em>lovingkindness</em>, <em>steadfast love</em>, '
        '<em>mercy</em>, or <em>unfailing love</em>. It is the defining attribute of God\'s covenant relationship '
        'with His people: <em>The LORD, The LORD God, merciful and gracious, longsuffering, and abundant in '
        'goodness and truth, Keeping mercy [hesed] for thousands, forgiving iniquity and transgression and sin</em> '
        '(Ex 34:6-7). Psalm 136 returns to it twenty-six times: <em>his mercy endureth for ever</em>. Hesed is '
        'not romantic affection; it is the loyal love that keeps covenant promises even when the covenant '
        'partner has failed. The NT corresponding word is <em>agape</em> &mdash; the self-giving love of God '
        'in Christ. Both names point at the same divine reality: a love that does not change with the beloved\'s '
        'changes, that does not lessen with the beloved\'s failures, that finally overcomes every obstacle to '
        'fellowship.</p>'
    ),
    'upper-room': (
        '<p>The large furnished upper-story room where Christ ate the Last Supper with His disciples (Mark '
        '14:13-16; Luke 22:10-13) and where the disciples gathered to wait for the promised Spirit (Acts 1:13-14) '
        'before Pentecost. The Greek <em>anagaion</em> (upper room) was a common architectural feature of '
        'first-century Palestinian houses &mdash; an upstairs room used for gatherings, meals, and prayer. Christ\'s '
        'instructions for finding it (a man carrying a pitcher of water would lead the disciples to it) carry '
        'their own signal: men did not typically carry water-pitchers (women did), so the instruction was a '
        'pre-arranged sign. In the upper room Christ instituted the Lord\'s Supper, washed the disciples\' feet '
        '(John 13), gave the upper-room discourse (John 14-17), and prayed His high-priestly prayer. After the '
        'resurrection and ascension, the same kind of upper room (Acts 1:13) became the gestational space of '
        'the early church. From upper room to Pentecost &mdash; the foundational arc of the apostolic mission.</p>'
    ),
    'warrior-prayer': (
        '<p>The biblical pattern of prayer as warfare against spiritual enemies. 2 Corinthians 10:4-5: <em>For '
        'the weapons of our warfare are not carnal, but mighty through God to the pulling down of strong holds; '
        'Casting down imaginations, and every high thing that exalteth itself against the knowledge of God, '
        'and bringing into captivity every thought to the obedience of Christ.</em> Ephesians 6:18 closes Paul\'s '
        'armor-of-God passage with prayer as the all-encompassing context: <em>Praying always with all prayer '
        'and supplication in the Spirit, and watching thereunto with all perseverance and supplication for '
        'all saints.</em> The Christian\'s combat is not against flesh and blood but against principalities, '
        'powers, the rulers of the darkness of this world, and spiritual wickedness in high places (Eph 6:12). '
        'Prayer is the warfare. Daniel\'s three-week prayer in Daniel 10 reveals the spiritual conflict behind '
        'the scenes &mdash; an angelic messenger delayed twenty-one days by the prince of Persia. Real '
        'spiritual battles are won (or lost) by men and women who pray, not by men and women who only do.</p>'
    ),
    'widow-mite': (
        '<p>The poor widow Christ observed in the temple treasury, contrasted with the wealthy donors. Mark '
        '12:41-44 and Luke 21:1-4: <em>And there came a certain poor widow, and she threw in two mites, which '
        'make a farthing... Of a truth I say unto you, that this poor widow hath cast in more than they all: '
        'For all these have of their abundance cast in unto the offerings of God: but she of her penury hath '
        'cast in all the living that she had.</em> Christ\'s evaluation of giving is by proportion to means, '
        'not by absolute amount. The wealthy gave out of their surplus; the widow gave out of her poverty &mdash; '
        'and Christ counted hers the greater gift. The two mites (Greek <em>lepta</em>, the smallest copper '
        'coins in circulation) together made about one-quarter of a Roman penny. The widow\'s gift is the '
        'biblical paradigm of sacrificial generosity: not how much was given but how much was kept. Her '
        'imitation is the Christian standard.</p>'
    ),
    'wilderness-testing': (
        '<p>The biblical pattern of God leading His people into wilderness conditions to humble, test, and form '
        'them. The canonical case is Israel\'s forty years between Egypt and Canaan, summarized in Deuteronomy '
        '8:2: <em>And thou shalt remember all the way which the LORD thy God led thee these forty years in the '
        'wilderness, to humble thee, and to prove thee, to know what was in thine heart, whether thou wouldest '
        'keep his commandments, or no.</em> The pattern recurs throughout Scripture: Elijah\'s forty days in '
        'the wilderness after Carmel (1 Kgs 19); John the Baptist\'s ministry in the wilderness (Matt 3:1); '
        'Christ\'s forty days of temptation in the wilderness (Matt 4:1-11), where He explicitly succeeds where '
        'Israel failed; Paul\'s three years in Arabia after his conversion (Gal 1:17). Wilderness in Scripture '
        'is the place of stripping, dependency, and formation &mdash; where the believer\'s self-sufficiency '
        'dies and his trust in God matures. The wilderness is not punishment; it is preparation. The promised '
        'land lies on the other side of it, and not many enter the promised land except through the wilderness.</p>'
    ),
    'selah-meaning': (
        '<p>A term appearing 71 times in the Psalms and 3 times in Habakkuk, traditionally understood as a '
        'liturgical or musical instruction directing the reader or singer to pause and reflect. The exact '
        'meaning of Hebrew <em>selah</em> is uncertain &mdash; proposals include <em>pause</em>, <em>lift up</em> '
        '(of voice or instrument), <em>forever</em>, or a musical interlude marker. The LXX renders it '
        '<em>diapsalma</em> (between psalm-parts), supporting the pause-interpretation. Whatever the precise '
        'musical function, the spiritual effect for the reader is clear: <em>selah</em> marks the point at '
        'which the psalmist invites the soul to stop and weigh what has been said before moving on. Psalm 3:2 '
        '(<em>many there be which say of my soul, There is no help for him in God. Selah.</em>) gives the '
        'pattern: the trouble is named, and then the reader is invited to sit with it before the psalmist '
        'speaks the answer. The Christian reader of the Psalms learns to honor <em>selah</em> &mdash; to read '
        'slower, to feel what the psalmist felt, to be shaped by the pause as well as by the words.</p>'
    ),
    'song-deliverance': (
        '<p>The song of praise the redeemed sing after God has rescued them from danger or distress. Psalm 32:7: '
        '<em>Thou art my hiding place; thou shalt preserve me from trouble; thou shalt compass me about with '
        'songs of deliverance.</em> The biblical pattern of crisis-to-rescue-to-song runs through Scripture: '
        'Moses\' Song at the Red Sea (Ex 15); Deborah\'s Song after Jabin\'s defeat (Judg 5); David\'s songs '
        'of deliverance (2 Sam 22, repeated as Ps 18); Mary\'s Magnificat after Gabriel\'s annunciation (Luke '
        '1:46-55); the song of Moses and of the Lamb in the eschaton (Rev 15:3). Deliverance produces song, '
        'and song carries deliverance forward into memory and instruction. The Christian who has been delivered '
        'is to sing &mdash; not because singing is religious decoration, but because the song is the proper '
        'biblical response to rescue and the means by which the rescued teaches the next generation what God '
        'has done.</p>'
    ),
    'soul-anchor': (
        '<p>Christian hope as the anchor of the soul. Hebrews 6:19-20: <em>Which hope we have as an anchor of '
        'the soul, both sure and stedfast, and which entereth into that within the veil; Whither the forerunner '
        'is for us entered, even Jesus, made an high priest for ever after the order of Melchisedec.</em> The '
        'image is rich. An anchor descends into water the sailor cannot see and grips ground he cannot see, '
        'holding the ship against winds and currents that would otherwise carry it away. The Christian\'s hope '
        'is anchored not in this life or its visible circumstances but <em>within the veil</em> &mdash; the '
        'place of the heavenly Most Holy where Christ has already entered as forerunner and as eternal High '
        'Priest. The anchor is sure (it will hold), steadfast (it will not slip), and entered (it is already '
        'fixed where Christ has gone). In every storm, the believer\'s hope is not adrift; the line runs into '
        'the unseen heavenlies where Christ Himself secures it.</p>'
    ),
    'valley-shadow': (
        '<p>The dark valley through which the believer walks under the LORD\'s shepherding. Psalm 23:4: '
        '<em>Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art '
        'with me; thy rod and thy staff they comfort me.</em> The Hebrew <em>gei tsalmavet</em> (valley of the '
        'shadow of death) names the deepest darkness the psalm-traveler can encounter &mdash; whether literal '
        'physical danger, terminal illness, the death of loved ones, or the spiritual darkness of despair. '
        'Two features mark the valley as biblical: the speaker walks <em>through</em> it (not into it permanently '
        '&mdash; it is traversed, not inhabited), and the LORD is <em>with</em> him (the pronouns shift in '
        'the psalm precisely here, from <em>he leadeth me</em> in v. 3 to <em>thou art with me</em> in v. 4 '
        '&mdash; the deepest moment becomes the closest moment). The shadow of death is real; the LORD\'s '
        'presence in it is more real. The valley is for passing, not staying.</p>'
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
        if success: ok += 1
        else:
            fail += 1
            print(f'  FAIL {slug}: {reason}')
    print(f'Expanded {ok}/{ok+fail} entries')


if __name__ == '__main__':
    main()
