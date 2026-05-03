#!/usr/bin/env python3
"""Add KJV Continual Tense annotation sections to existing dictionary entries.

The annotation surfaces what Pastor Matt Stokes pointed out:
the KJV's -eth ending (3rd-person singular present indicative active) marks
ongoing/habitual action in the underlying Greek/Hebrew. Modern English
flattened this — "he loves" doesn't tell you punctiliar vs continuous;
"he loveth" specifically signals continuous.

This script:
1. Has a hand-curated mapping of slug → KJV continual annotation
2. For each, finds the existing HTML file and inserts a new
   .kjv-continual <div class="section"> between Biblical Definition and
   Webster 1828 Definition.
3. Idempotent: detects already-annotated entries and skips them.

Pilot scope: the verb-entries that appear most prominently in John
(love, abide, hear, judge, witness, sanctify, glorify, dwell, behold,
overcome, comfort, rest, worship, fear, weep, rejoice, bless, etc.)
"""
import os
import re

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'docs', 'dictionary')

# Insertion marker: insert a new .section right BEFORE the Webster section.
INSERT_PAT = re.compile(
    r'(\n        <div class="section">\n            <h3>[^<]*Webster[^<]*</h3>)',
    re.DOTALL
)

# Fallback for stub entries (no Webster section) — insert after Biblical
# Definition's closing </div></div> and before the next <div class="section">
STUB_INSERT_PAT = re.compile(
    r'(<div class="section"><h3>[^<]*Biblical Definition[^<]*</h3><div class="biblical-def"><p>[^<]+</p></div></div>)',
    re.DOTALL
)

# Detect already-annotated entries (skip)
ALREADY_DONE = re.compile(r'class="section kjv-continual"')


def make_section(kjv_form, tense_label, summary, paragraphs):
    """Build the HTML for one KJV continual section."""
    para_html = '\n                    '.join(f'<p>{p}</p>' for p in paragraphs)
    return (
'''
        <div class="section kjv-continual">
            <h3>&#128220; KJV Continual Tense</h3>
            <p class="section-summary">{summary}</p>
            <details>
                <summary><em style="color:var(--gray)">expand to see more</em></summary>
                <div class="kjv-continual-inner">
                    {para_html}
                </div>
            </details>
        </div>
'''.format(summary=summary, para_html=para_html))


# ═══════════════════════════════════════════════════════════════════════
# Annotations for ~20 high-yield John verbs
# ═══════════════════════════════════════════════════════════════════════
ANNOTATIONS = {
    'love': make_section(
        kjv_form='loveth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>loveth</strong> &mdash; not "loved once" but "keeps on loving."',
        paragraphs=[
            'When the KJV renders the verb as <strong>loveth</strong>, the -eth ending marks the Greek <em>present indicative active</em> &mdash; an aspectual form that signals ongoing, habitual action. "Loveth" doesn\'t mean "loved once"; it means "keeps on loving."',
            'The grammar carries the doctrine. In <a class="verse-ref" href="../bible.html?ref=John+14:21">John 14:21</a> &mdash; "He that hath my commandments, and keepeth them, he it is that <strong>loveth</strong> me" &mdash; Jesus is not describing a punctiliar act of affection but a continuing posture of life. "Greater love hath no man" (<a class="verse-ref" href="../bible.html?ref=John+15:13">John 15:13</a>) names the supreme expression; the -eth verbs name the steady walk.',
            'Modern English flattens this distinction. The KJV preserves what the Greek aspect carries: love that perseveres.'
        ]
    ),

    'abide': make_section(
        kjv_form='abideth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>abideth</strong> &mdash; not "remains for a moment" but "keeps on dwelling."',
        paragraphs=[
            'The KJV\'s <strong>abideth</strong> renders the Greek present indicative active &mdash; ongoing, habitual remaining. Not "stopped by once" but "keeps on dwelling." This is the language of <a class="verse-ref" href="../bible.html?ref=John+15:5">John 15:5</a>: "He that <strong>abideth</strong> in me, and I in him, the same bringeth forth much fruit."',
            'In <a class="verse-ref" href="../bible.html?ref=1+John+2:6">1 John 2:6</a> &mdash; "He that saith he <strong>abideth</strong> in him ought himself also so to walk, even as he walked" &mdash; the continuous tense exposes the false claimant. To "abide" is not a moment but a manner of life.',
            'The aspect is theological. Eternal life is not a deposit one collects; it is a dwelling one inhabits.'
        ]
    ),

    'hear': make_section(
        kjv_form='heareth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>heareth</strong> &mdash; not "heard once" but "keeps on hearing."',
        paragraphs=[
            'In <a class="verse-ref" href="../bible.html?ref=John+5:24">John 5:24</a> &mdash; "He that <strong>heareth</strong> my word, and believeth on him that sent me, hath everlasting life" &mdash; the present tense is essential. Salvation is given to ongoing hearers, not one-time listeners.',
            'The same pattern runs through <a class="verse-ref" href="../bible.html?ref=John+10:27">John 10:27</a>: "My sheep <strong>hear</strong> my voice, and I know them, and they follow me." Hearing here is the standing posture of a sheep tuned to its Shepherd, not the brief attention of a passer-by.',
            'KJV\'s -eth recovers what modern translations often lose: hearing as habit, not event.'
        ]
    ),

    'judge': make_section(
        kjv_form='judgeth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>judgeth</strong> &mdash; God\'s ongoing, faithful discrimination.',
        paragraphs=[
            'When the KJV says <strong>judgeth</strong>, it marks God\'s judgment as continuous activity, not a single future event alone. <a class="verse-ref" href="../bible.html?ref=John+5:22">John 5:22</a> &mdash; "the Father <strong>judgeth</strong> no man, but hath committed all judgment unto the Son" &mdash; describes an ongoing transfer of authority.',
            'Likewise <a class="verse-ref" href="../bible.html?ref=1+Peter+1:17">1 Peter 1:17</a>: "the Father, who without respect of persons <strong>judgeth</strong> according to every man\'s work." His judging is not deferred entirely to the last day; it is currently in operation, weighing every life.',
            'Take the continuous force seriously and "the Father judgeth" becomes more pastoral than threat: He is paying attention, all the time, in righteousness.'
        ]
    ),

    'witness': make_section(
        kjv_form='witnesseth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>witnesseth</strong> / <strong>beareth witness</strong> &mdash; ongoing testimony.',
        paragraphs=[
            'John\'s gospel is structured around continuous witness. <a class="verse-ref" href="../bible.html?ref=John+5:32">John 5:32</a>: "There is another that <strong>beareth witness</strong> of me." The verb is not "bore witness once" but "keeps on bearing witness."',
            'The Spirit\'s present-tense witness in <a class="verse-ref" href="../bible.html?ref=Romans+8:16">Romans 8:16</a> is the same shape: "The Spirit itself <strong>beareth witness</strong> with our spirit, that we are the children of God." Not a one-time Pentecost but a continuous internal testimony.',
            'KJV\'s -eth keeps the witness fresh in the verb where modern English would render it past or generic.'
        ]
    ),

    'sanctify': make_section(
        kjv_form='sanctifieth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>sanctifieth</strong> &mdash; the ongoing setting-apart, not one finished act.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=John+17:17">John 17:17</a> &mdash; "<strong>Sanctify</strong> them through thy truth: thy word is truth" &mdash; is the high-priestly prayer for continuous setting-apart. The KJV elsewhere uses <strong>sanctifieth</strong> precisely because the Spirit\'s sanctifying work is not done at conversion; it is the steady labor of a lifetime.',
            'In <a class="verse-ref" href="../bible.html?ref=Hebrews+10:14">Hebrews 10:14</a> the language interweaves: "by one offering he hath perfected for ever them that are <strong>sanctified</strong>" (definitive past) &mdash; even there, the underlying Greek participle is durative. Christ has finally sanctified those whom the Spirit is presently sanctifying.',
            'The Reformed distinction between definitive and progressive sanctification is grammatically pre-figured here.'
        ]
    ),

    'glorify': make_section(
        kjv_form='glorifieth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>glorifieth</strong> &mdash; ongoing, mutual giving of glory.',
        paragraphs=[
            'In <a class="verse-ref" href="../bible.html?ref=John+15:8">John 15:8</a> &mdash; "Herein is my Father <strong>glorified</strong>, that ye bear much fruit" &mdash; the continuous glorification is happening through ongoing fruit-bearing. Not a one-time glorification but a perpetual one.',
            'The high-priestly prayer of <a class="verse-ref" href="../bible.html?ref=John+17:1">John 17:1</a>: "Father, the hour is come; <strong>glorify</strong> thy Son, that thy Son also may <strong>glorify</strong> thee." The mutual giving of glory between Father and Son is rendered with verb forms whose aspect is ongoing.',
            'The continuous tense reminds us: God\'s glory is a present concern, not deferred to "someday."'
        ]
    ),

    'dwell': make_section(
        kjv_form='dwelleth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>dwelleth</strong> &mdash; ongoing residence, the indwelling Spirit.',
        paragraphs=[
            'When Paul says in <a class="verse-ref" href="../bible.html?ref=Romans+8:11">Romans 8:11</a> &mdash; "if the Spirit of him that raised up Jesus from the dead <strong>dwell</strong> in you" &mdash; the verb is continuous-aspect Greek. The Spirit\'s indwelling is not a momentary visitation but a steady, abiding residence.',
            'Same in <a class="verse-ref" href="../bible.html?ref=John+14:17">John 14:17</a>: "the Spirit of truth... <strong>dwelleth</strong> with you, and shall be in you." The KJV preserves the present-continuous force.',
            'Theologically critical: the indwelling is not in-and-out. The Spirit who dwells in you is dwelling there now and shall continue.'
        ]
    ),

    'behold': make_section(
        kjv_form='beholdeth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>beholdeth</strong> &mdash; sustained, attentive looking.',
        paragraphs=[
            '"Behold!" is more than a synonym for "look." When the KJV uses <strong>beholdeth</strong>, it marks sustained attentive seeing. <a class="verse-ref" href="../bible.html?ref=James+1:23">James 1:23-24</a> uses it sharply: a man "<strong>beholdeth</strong> his natural face in a glass" &mdash; he looks long enough to register but not long enough to be transformed.',
            'Contrast Paul\'s <a class="verse-ref" href="../bible.html?ref=2+Corinthians+3:18">2 Corinthians 3:18</a>: "we all, with open face <strong>beholding</strong> as in a glass the glory of the Lord, are changed into the same image." The continuous beholding is what transforms.',
            '<strong>Beholdeth</strong> demands the kind of looking that lingers.'
        ]
    ),

    'overcome': make_section(
        kjv_form='overcometh',
        tense_label='Greek present indicative active (often used as substantive participle)',
        summary='In KJV: <strong>overcometh</strong> &mdash; the perpetual conquest, not a single victory.',
        paragraphs=[
            'The seven letters of Revelation each close with a promise to "him that <strong>overcometh</strong>." The Greek <em>ho nikōn</em> &mdash; "the one continually conquering" &mdash; is not a one-time hero but the persevering saint who keeps overcoming through trial after trial.',
            '<a class="verse-ref" href="../bible.html?ref=1+John+5:4">1 John 5:4</a>: "whatsoever is born of God <strong>overcometh</strong> the world: and this is the victory that overcometh the world, even our faith." The continuous tense binds victory to ongoing faith.',
            'Christ already <em>has</em> overcome (<a class="verse-ref" href="../bible.html?ref=John+16:33">John 16:33</a> &mdash; perfect tense, completed); we <em>are overcoming</em> (present, ongoing) by union with Him.'
        ]
    ),

    'comfort': make_section(
        kjv_form='comforteth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>comforteth</strong> &mdash; the Spirit\'s ongoing parakletos-work.',
        paragraphs=[
            'The Holy Spirit is named <em>parakletos</em> &mdash; "the one called alongside" &mdash; and the work is continuous. <a class="verse-ref" href="../bible.html?ref=2+Corinthians+1:4">2 Corinthians 1:4</a>: "Who <strong>comforteth</strong> us in all our tribulation, that we may be able to comfort them which are in any trouble." Not "comforted us once" but "keeps on comforting."',
            'Christ promises in <a class="verse-ref" href="../bible.html?ref=John+14:16">John 14:16</a>: "And I will pray the Father, and he shall give you another <strong>Comforter</strong>, that he may abide with you for ever." The Comforter is here continuously; the comfort is not seasonal.',
            'Recover the continuous force: not "the Spirit comforted me that one time" but "the Spirit is the One who is comforting me now."'
        ]
    ),

    'rest': make_section(
        kjv_form='resteth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>resteth</strong> &mdash; God\'s sustained presence settling on His people.',
        paragraphs=[
            'In <a class="verse-ref" href="../bible.html?ref=1+Peter+4:14">1 Peter 4:14</a>: "the spirit of glory and of God <strong>resteth</strong> upon you." The verb is continuous. The Spirit\'s glory does not flutter on and off the suffering saint &mdash; it settles and abides.',
            'Same continuous force at the cross-bridging text <a class="verse-ref" href="../bible.html?ref=Isaiah+11:2">Isaiah 11:2</a>: "the spirit of the LORD shall <strong>rest</strong> upon him." Christ does not have intermittent anointing; the Spirit is settled upon Him eternally.',
            'When the KJV says God\'s glory <strong>resteth</strong> on you, hear it as: it is settled, and it is staying.'
        ]
    ),

    'worship': make_section(
        kjv_form='worshippeth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>worshippeth</strong> &mdash; not "worshipped once" but "is a worshipper."',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=John+4:23">John 4:23</a> &mdash; "the true <strong>worshippers</strong> shall worship the Father in spirit and in truth: for the Father seeketh such to worship him" &mdash; pivots on continuous-aspect Greek. The Father is seeking those who <em>continually</em> worship rightly, not those who managed it once.',
            'The continuous force exposes the false worshipper of <a class="verse-ref" href="../bible.html?ref=Acts+18:13">Acts 18:13</a> &mdash; "this fellow <strong>persuadeth</strong> men to worship God contrary to the law" &mdash; and dignifies the steady worship of the elder church.',
            'A worshipper is not someone who worshipped; a worshipper is someone who is worshipping.'
        ]
    ),

    'fear': make_section(
        kjv_form='feareth',
        tense_label='Greek/Hebrew present indicative active',
        summary='In KJV: <strong>feareth</strong> &mdash; the abiding posture of reverence.',
        paragraphs=[
            'The fear of the LORD in Scripture is rarely a moment of trembling. It is a sustained posture of reverence. <a class="verse-ref" href="../bible.html?ref=Acts+10:35">Acts 10:35</a>: "in every nation he that <strong>feareth</strong> him, and worketh righteousness, is accepted with him." Cornelius was a continuous fearer.',
            '<a class="verse-ref" href="../bible.html?ref=Psalm+34:9">Psalm 34:9</a> &mdash; rendered through KJV continuous force &mdash; "O fear the LORD, ye his saints: for there is no want to them that <strong>fear</strong> him." Not "feared him once at conversion" but "are fearing him as a way of life."',
            'The continuous tense protects against thinking the fear of the LORD is ever finished work.'
        ]
    ),

    'rejoice': make_section(
        kjv_form='rejoiceth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>rejoiceth</strong> &mdash; sustained, not seasonal joy.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=1+Corinthians+13:6">1 Corinthians 13:6</a>: "<strong>Rejoiceth</strong> not in iniquity, but <strong>rejoiceth</strong> in the truth." Love\'s rejoicing is not bursts but a settled disposition. Continuous tense.',
            '<a class="verse-ref" href="../bible.html?ref=Philippians+4:4">Philippians 4:4</a>: "<strong>Rejoice</strong> in the Lord alway: and again I say, <strong>Rejoice</strong>." The "alway" interprets the verb&apos;s aspect &mdash; continuous, sustained, not contingent on circumstance.',
            'KJV\'s -eth recovers the disposition: a Christian is not someone who has rejoiced; a Christian is someone who is rejoicing.'
        ]
    ),

    'bless': make_section(
        kjv_form='blesseth',
        tense_label='Greek/Hebrew present indicative active',
        summary='In KJV: <strong>blesseth</strong> &mdash; God\'s continuous bestowal of favor.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=Psalm+115:13">Psalm 115:13</a>: "He will <strong>bless</strong> them that fear the LORD, both small and great." The Hebrew imperfect carries the same force the KJV preserves &mdash; ongoing, repeated blessing across generations.',
            'Not "God blessed me at conversion" but "God is the One who keeps on blessing those who fear Him."',
            'Read the Beatitudes (<a class="verse-ref" href="../bible.html?ref=Matthew+5:3">Matthew 5:3</a> ff.) with this lens. "<strong>Blessed</strong> are..." is not a one-time pronouncement but a sustained state.'
        ]
    ),

    'meditate': make_section(
        kjv_form='meditateth',
        tense_label='Hebrew imperfect / Greek present indicative active',
        summary='In KJV: <strong>meditateth</strong> &mdash; the continuous chewing-over of God\'s word.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=Psalm+1:2">Psalm 1:2</a>: "in his law doth he <strong>meditate</strong> day and night." The Hebrew <em>hagah</em> means to mutter, growl, chew over &mdash; and the imperfect aspect makes it ongoing. Not "meditated last week" but "is meditating, all the time."',
            'The picture is of an animal chewing cud &mdash; bringing the word back up, working it over, swallowing it down again.',
            'KJV\'s rendering preserves what the Hebrew aspect carries: meditation is not an act but a manner of life.'
        ]
    ),

    'praise': make_section(
        kjv_form='praiseth',
        tense_label='Greek/Hebrew present indicative active',
        summary='In KJV: <strong>praiseth</strong> / <strong>shall praise</strong> &mdash; sustained, eternal-shaped.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=Psalm+150:6">Psalm 150:6</a>: "Let every thing that hath breath <strong>praise</strong> the LORD." The verb force is continuous &mdash; while breath lasts, praise. The end of breath is the only stopping point.',
            '<a class="verse-ref" href="../bible.html?ref=Psalm+34:1">Psalm 34:1</a>: "I will <strong>bless</strong> the LORD at all times: his praise shall continually be in my mouth." The KJV preserves what the Hebrew imperfect demands.',
            'Worship music in the New Jerusalem (<a class="verse-ref" href="../bible.html?ref=Revelation+5:13">Revelation 5:13</a>) is similarly continuous &mdash; "blessing, and honour, and glory, and power, be unto him..." with no comma where it ends.'
        ]
    ),

    'repent': make_section(
        kjv_form='repenteth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>repenteth</strong> &mdash; the ongoing turning, not one moment\'s decision.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=Luke+15:7">Luke 15:7</a>: "joy shall be in heaven over one sinner that <strong>repenteth</strong>, more than over ninety and nine just persons, which need no repentance." The continuous tense paints repentance not as a transaction but as a turning-and-keeping-turned.',
            'The Reformed tradition rightly distinguishes initial repentance (the first turn at conversion) from ongoing repentance (the daily turning of the believer). KJV\'s -eth carries the second sense throughout.',
            '"He that <strong>repenteth</strong>" is not "he who once repented" but "he who is repenting" &mdash; the lifestyle Luther named in his first thesis: "the entire life of believers should be one of repentance."'
        ]
    ),

    'trust': make_section(
        kjv_form='trusteth',
        tense_label='Hebrew imperfect / Greek present indicative active',
        summary='In KJV: <strong>trusteth</strong> &mdash; sustained leaning, not one-time decision.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=Psalm+34:8">Psalm 34:8</a>: "blessed is the man that <strong>trusteth</strong> in him." The Hebrew imperfect carries the continuous force &mdash; the blessed life is ongoing trust.',
            '<a class="verse-ref" href="../bible.html?ref=Jeremiah+17:7">Jeremiah 17:7</a>: "Blessed is the man that <strong>trusteth</strong> in the LORD, and whose hope the LORD is." Trust is not a deposit; it is a sustained posture of the soul.',
            'The continuous force of trust is what makes Hebrews 11 readable as a single chapter: every name is doing one thing &mdash; trusting, trusting, trusting.'
        ]
    ),

    'hope': make_section(
        kjv_form='hopeth',
        tense_label='Greek present indicative active',
        summary='In KJV: <strong>hopeth</strong> &mdash; the abiding hope, not bursts of optimism.',
        paragraphs=[
            '<a class="verse-ref" href="../bible.html?ref=1+Corinthians+13:7">1 Corinthians 13:7</a>: love "<strong>hopeth</strong> all things, endureth all things." Continuous-aspect Greek &mdash; love is constantly hoping, not occasionally optimistic.',
            'Hope in Scripture is not optimism. It is sustained expectation rooted in God\'s promises. The KJV\'s -eth preserves the steadiness modern translations sometimes lose.',
            'Tie this to <a class="verse-ref" href="../bible.html?ref=Romans+12:12">Romans 12:12</a>: "<strong>Rejoicing</strong> in hope; <strong>patient</strong> in tribulation; <strong>continuing</strong> instant in prayer" &mdash; three present participles, one disposition.'
        ]
    ),
}


def patch_file(slug):
    fp = os.path.join(DICT_DIR, slug + '.html')
    if not os.path.exists(fp):
        return False, 'file not found'
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    if ALREADY_DONE.search(html):
        return False, 'already annotated'
    if slug not in ANNOTATIONS:
        return False, 'no annotation defined'
    section_html = ANNOTATIONS[slug]
    new_html, n = INSERT_PAT.subn(section_html + r'\1', html, count=1)
    if n == 0:
        # Try stub fallback — insert after Biblical Definition
        new_html, n = STUB_INSERT_PAT.subn(r'\1' + section_html, html, count=1)
        if n == 0:
            return False, 'no insertion point found'
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True, 'ok'


def main():
    ok, fail = 0, 0
    for slug in sorted(ANNOTATIONS):
        success, reason = patch_file(slug)
        marker = '✓' if success else '✗'
        if success:
            ok += 1
        else:
            fail += 1
        print(f'  {marker} {slug:<14} ({reason})')
    print(f'\nAnnotated {ok} / {ok+fail} entries')


if __name__ == '__main__':
    main()
