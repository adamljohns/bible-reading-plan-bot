#!/usr/bin/env python3
"""Batch 51 — expand 25 more entries from the 60-70 word bucket.

Targets: Lord's Prayer petitions, Hebrew terms, doctrines,
theologians, Christology, prudence, and Passion-Week vocabulary.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'hallowed-be-thy-name': (
        '<p>"Hallowed be thy name" is the first petition of the Lord’s Prayer: <em>"Our Father which art in heaven, Hallowed be thy name"</em> (<em>Matthew 6:9</em>). The Greek verb is passive imperative third-person — <em>"let your name be made holy"</em> — and it places the prayer’s first concern on God’s glory rather than the petitioner’s needs. The petition asks that God’s character (which His Name carries) be recognized, honored, and feared by all — in the petitioner’s own heart first, then in his household, his church, his city, and the nations. The third commandment forbids taking the Name in vain (<em>Exodus 20:7</em>); the Lord’s Prayer asks that the same Name be made holy everywhere it is invoked.</p>'
    ),
    'haughtiness': (
        '<p>Haughtiness is the lifted-up posture of the proud heart — in Scripture, the inward elevation that always precedes a literal fall. <em>"Pride goeth before destruction, and an haughty spirit before a fall"</em> (<em>Proverbs 16:18</em>). The LORD declares Himself the enemy of it: <em>"For though the LORD be high, yet hath he respect unto the lowly: but the proud he knoweth afar off"</em> (<em>Psalm 138:6</em>); <em>"God resisteth the proud, but giveth grace unto the humble"</em> (<em>James 4:6; 1 Peter 5:5</em>). Isaiah’s Day of the LORD reduces all human loftiness: <em>"The lofty looks of man shall be humbled, and the haughtiness of men shall be bowed down, and the LORD alone shall be exalted in that day"</em> (<em>Isaiah 2:11, 17</em>). Christian men crucify haughtiness daily.</p>'
    ),
    'help-meet': (
        '<p>"Help meet" is the KJV translation of the Hebrew <em>ezer kenegdo</em> — the term God Himself uses for Eve in <em>Genesis 2:18</em>: <em>"And the LORD God said, It is not good that the man should be alone; I will make him an help meet for him."</em> <em>Ezer</em> means a <em>help-of-strength</em> (used elsewhere of God Himself, <em>Psalm 33:20; 70:5; 121:1-2</em>) — never connoting subordination of essence. <em>Kenegdo</em> means <em>"corresponding to him"</em> or <em>"opposite to him"</em> — a counterpart who fits. The wife is therefore a powerful and corresponding help to her husband within the patriarchal order God established before the fall. Not a slave; not a peer; a help — strong, dignified, and indispensable. Modern translations <em>"helper"</em> or <em>"partner"</em> can flatten the weight.</p>'
    ),
    'horse': (
        '<p>The horse is the large hooved animal used in war and royal travel — and in Scripture it is loaded both ways. As an emblem of <em>human military self-trust</em>, the horse is consistently rebuked: <em>"Some trust in chariots, and some in horses: but we will remember the name of the LORD our God"</em> (<em>Psalm 20:7</em>); <em>"An horse is a vain thing for safety: neither shall he deliver any by his great strength"</em> (<em>33:17</em>); Israel’s kings were forbidden to multiply horses (<em>Deuteronomy 17:16</em>). As a symbol of <em>divine power</em>, the horses and chariots of fire surround Elisha at Dothan (<em>2 Kings 6:17</em>); Christ returns on a white horse with the armies of heaven behind Him (<em>Revelation 19:11-16</em>). Vain in human hand; mighty in God’s.</p>'
    ),
    'immanuel': (
        '<p>Immanuel (or Emmanuel, Hebrew <em>Immanu El</em>) is the prophetic name promised in <em>Isaiah 7:14</em> to the wavering house of David through King Ahaz: <em>"Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel."</em> Matthew explicitly identifies the fulfillment as the Lord Jesus Christ: <em>"Now all this was done, that it might be fulfilled which was spoken of the Lord by the prophet, saying, Behold, a virgin shall be with child, and shall bring forth a son, and they shall call his name Emmanuel, which being interpreted is, God with us"</em> (<em>Matthew 1:22-23</em>). Immanuel combines deity (<em>El</em>) with covenantal presence (<em>Immanu</em>). Christ is God Himself, dwelling among His people.</p>'
    ),
    'inheritance-spiritual': (
        '<p>Spiritual inheritance is the portion of God’s grace, gifts, and final reward passed from the Father to His children in Christ. It is not earned but received — the legal entitlement of every adopted son. Peter names it most fully: <em>"To an inheritance incorruptible, and undefiled, and that fadeth not away, reserved in heaven for you, Who are kept by the power of God through faith unto salvation ready to be revealed in the last time"</em> (<em>1 Peter 1:4-5</em>). Paul names the present pledge: <em>"the holy Spirit of promise, Which is the earnest of our inheritance until the redemption of the purchased possession, unto the praise of his glory"</em> (<em>Ephesians 1:13-14</em>). Inheritance now in part; inheritance then in full.</p>'
    ),
    'kinship-house-of-faith': (
        '<p>"The household of faith" is Paul’s phrase in <em>Galatians 6:10</em>: <em>"As we have therefore opportunity, let us do good unto all men, especially unto them who are of the household of faith."</em> The believers are a family <em>before</em> they are anything else — bound by ties stronger than blood, geography, or ethnicity. Christ Himself: <em>"For whosoever shall do the will of God, the same is my brother, and my sister, and mother"</em> (<em>Mark 3:35</em>). The local church is the visible household; the universal church is the larger family across continents and centuries. Christian men should treat their fellow saints as actual brothers (with the duties of brotherhood) — opening homes, sharing resources, defending reputation, and showing up at every crisis.</p>'
    ),
    'mediator-biblical': (
        '<p>A mediator is one who stands between two estranged parties to reconcile them — and Scripture names two principal biblical mediators. Moses was the mediator of the Old Covenant: <em>"Wherefore then serveth the law? It was added because of transgressions... and it was ordained by angels in the hand of a mediator"</em> (<em>Galatians 3:19</em>; cf. <em>Hebrews 8:6</em>). Christ is the mediator of the New Covenant and the universal mediator between God and men: <em>"For there is one God, and one mediator between God and men, the man Christ Jesus; Who gave himself a ransom for all"</em> (<em>1 Timothy 2:5-6</em>; <em>Hebrews 8:6; 9:15; 12:24</em>). The article and number matter: <em>one</em> mediator. Rome’s saints, Mary as co-mediatrix, and every priestly substitute fall under this verse’s exclusive claim.</p>'
    ),
    'naturalism-philosophical': (
        '<p>Philosophical (or Metaphysical) Naturalism is the metaphysical position that only natural causes and entities exist — there is no God, no soul, no supernatural, no spirit. It is the dominant unspoken worldview of the modern Western academy, science establishment, and entertainment industry. It is distinct from <em>methodological naturalism</em> (which only <em>brackets</em> the supernatural for the limited purposes of natural-science investigation). Scripture refuses the metaphysical version: <em>"In the beginning God created the heaven and the earth"</em> (<em>Genesis 1:1</em>) requires a Creator before any natural cause exists. Romans 1:18-20 holds the naturalist responsible: God’s eternal power and Godhead are <em>"clearly seen, being understood by the things that are made; so that they are without excuse."</em> Suppression of the truth.</p>'
    ),
    'no-condemnation': (
        '<p>"There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the Spirit"</em> (<em>Romans 8:1</em>) — the great opening verdict of Romans 8 and the gospel’s most concentrated comfort. The <em>"therefore"</em> reaches back through Paul’s Romans 1-7 argument: God’s wrath against ungodliness; the impossibility of justification by law; justification by faith in Christ; the futility of the regenerate man’s struggle against indwelling sin in his own strength. The <em>"now"</em> is forensic — the verdict already pronounced, in the present tense, over every believer. The <em>"no condemnation"</em> is absolute: nothing, present or future, can re-summon the believer to the docket. Christ has been judged in our place; the case is closed.</p>'
    ),
    'offense': (
        '<p>An offense, biblically, is an injury, transgression, or stumbling-block. The Greek <em>skandalon</em> originally named the bait-stick of a trap — the small piece that, when touched, sprang the snare. So in Scripture: an offense is both an obstacle that <em>trips</em> and a trap that <em>snares</em>. Christ used it of Himself: the cross is an offense to the natural man — <em>"Christ crucified, unto the Jews a stumblingblock"</em> (<em>1 Corinthians 1:23</em>); <em>"the offence of the cross"</em> (<em>Galatians 5:11</em>). He also warned those who cause little ones to stumble: <em>"It were better for him that a millstone were hanged about his neck"</em> (<em>Luke 17:2</em>). Christian men must not <em>be</em> the offense; they must not <em>take</em> needless offense.</p>'
    ),
    'original-sin': (
        '<p>Original sin is the doctrine that Adam’s first sin in Eden corrupted the entire human race — both legally and morally. The entire human race is born <em>guilty</em> (federally, through Adam’s representative headship over humanity) and <em>corrupt</em> (naturally, through inherited fallen nature). <em>Romans 5:12-21</em> is the classic locus: <em>"Wherefore, as by one man sin entered into the world, and death by sin; and so death passed upon all men, for that all have sinned... by one man’s disobedience many were made sinners"</em>. <em>Psalm 51:5</em>: <em>"Behold, I was shapen in iniquity; and in sin did my mother conceive me."</em> The doctrine explains why babies die, why every child needs no instruction in selfishness, and why Christ’s substitutionary obedience as the Last Adam is the only remedy.</p>'
    ),
    'owen-figure': (
        '<p>John Owen (1616-1683) was the English Puritan theologian — vice-chancellor of Oxford under Cromwell, sometime chaplain to the Lord Protector, dean of Christ Church, and author of the most rigorous body of Puritan systematic theology in English. Major works: <em>The Death of Death in the Death of Christ</em> (definitive Reformed defense of particular redemption), <em>The Mortification of Sin in Believers</em> (<em>"Be killing sin or it will be killing you"</em>), the three-volume <em>Communion with God</em>, <em>Christological discourses</em> on the glory of Christ, and a vast multi-volume work on the Holy Spirit. After the Restoration he refused conformity and ministered as a non-conformist until his death. J. I. Packer reckoned Owen the greatest English theologian. Spurgeon called him the prince of the Puritans.</p>'
    ),
    'passion-week': (
        '<p>Passion Week is the final week of Christ’s earthly life — the most theologically dense seven days in human history. Sunday: the Triumphal Entry into Jerusalem (<em>Matthew 21:1-11</em>). Monday: the cleansing of the temple and cursing of the fig tree (<em>21:12-22</em>). Tuesday: the day of controversies in the temple, the Olivet Discourse (<em>Matthew 24-25</em>). Wednesday: probably retirement at Bethany; Judas’s bargain with the priests. Thursday evening: the Last Supper, Gethsemane, the arrest, the night-trials before Annas and Caiaphas. Friday: the morning trials before Pilate and Herod, the crucifixion, the burial before sundown. Saturday: the Sabbath in the tomb. Sunday: the Resurrection. Every gospel devotes a disproportionate share of its pages to this week.</p>'
    ),
    'paten': (
        '<p>A paten is the plate that holds the bread in the Lord’s Supper — the companion vessel to the chalice (which holds the cup). Christ on the night of His betrayal <em>"took bread, and blessed it, and brake it, and gave it to the disciples, and said, Take, eat; this is my body"</em> (<em>Matthew 26:26; Luke 22:19; 1 Corinthians 11:23-24</em>). The paten is what bears the broken bread to the communicants. Like the chalice, it varies in form across traditions — large platter, small individual plates, ornate gold-plated vessel, or simple wooden tray — but its function is constant: receiving the bread broken in remembrance of His broken body. Christian congregations should treat both vessels with the reverence due the elements they bear.</p>'
    ),
    'peace-biblical': (
        '<p>Biblical peace is not the absence of conflict; it is the presence of right order. The Hebrew <em>shalom</em> means wholeness, completeness, well-being — the integrated state of a life or community in which everything is in its proper place under God. The Greek <em>eirēnē</em> picks up the same range. Christ left this peace as His parting gift: <em>"Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid"</em> (<em>John 14:27</em>). Paul names the result: <em>"And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus"</em> (<em>Philippians 4:7</em>). Biblical peace endures because it is anchored above circumstances.</p>'
    ),
    'principalities-powers': (
        '<p>"Principalities and powers" is Paul’s term for the hierarchies of spiritual powers operative in the cosmos — both fallen (demonic) and unfallen (angelic). Most pointedly in the armor passage: <em>"For we wrestle not against flesh and blood, but against principalities, against powers, against the rulers of the darkness of this world, against spiritual wickedness in high places"</em> (<em>Ephesians 6:12</em>). Christ has triumphed over the fallen ranks at the cross: <em>"And having spoiled principalities and powers, he made a shew of them openly, triumphing over them in it"</em> (<em>Colossians 2:15</em>). He is exalted above all of them: <em>"Far above all principality, and power, and might, and dominion"</em> (<em>Ephesians 1:21</em>). The Christian fights in the wake of an already-decisive victory.</p>'
    ),
    'prudent': (
        '<p>"Prudent" describes the man possessing careful foresight, sound judgment, and shrewd application of wisdom. In Scripture it is frequently contrasted with simplicity, recklessness, and folly. <em>"The prudent man looketh well to his going"</em> (<em>Proverbs 14:15</em>); <em>"A prudent man foreseeth the evil, and hideth himself: but the simple pass on, and are punished"</em> (<em>Proverbs 22:3; 27:12</em>); <em>"The prudent are crowned with knowledge"</em> (<em>14:18</em>). Christ commands prudence in His sending of the disciples: <em>"be ye therefore wise as serpents, and harmless as doves"</em> (<em>Matthew 10:16</em>). Christian prudence is not worldly cunning or cowardly self-protection; it is faith-anchored shrewdness — looking ahead, counting cost, weighing outcomes, planning under God.</p>'
    ),
    'pulling-shoes': (
        '<p>Pulling off the shoes appears in two loaded biblical scenes. First, at the burning bush God commands Moses: <em>"Draw not nigh hither: put off thy shoes from off thy feet, for the place whereon thou standest is holy ground"</em> (<em>Exodus 3:5</em>; cf. <em>Joshua 5:15</em> to Joshua before Jericho). The unshod foot signals sacred space — the worshiper is at the LORD’s disposal. Second, in <em>Ruth 4:7-8</em>, Boaz’s nearer kinsman pulls off his shoe and hands it to Boaz, formally transferring the right of kinsman-redemption: <em>"Now this was the manner in former time in Israel concerning redeeming and concerning changing, for to confirm all things; a man plucked off his shoe, and gave it to his neighbour."</em> Holy ground; transferred inheritance — two reasons to pull off the shoe.</p>'
    ),
    'righteous-branch': (
        '<p>"The Righteous Branch" is Jeremiah’s specific Messianic title: <em>"Behold, the days come, saith the LORD, that I will raise unto David a righteous Branch, and a King shall reign and prosper, and shall execute judgment and justice in the earth. In his days Judah shall be saved, and Israel shall dwell safely: and this is his name whereby he shall be called, THE LORD OUR RIGHTEOUSNESS"</em> (<em>Jeremiah 23:5-6</em>; cf. <em>33:15</em>). The qualifier <em>"righteous"</em> distinguishes Him from Israel’s historical kings whose unrighteousness brought judgment. Isaiah, Zechariah, and others use the Branch-image (<em>Isaiah 11:1; Zechariah 3:8; 6:12</em>). Christ is therefore Branch from the stump of Jesse, Branch reigning in justice, Branch who is Himself <em>"the LORD our righteousness."</em></p>'
    ),
    'root-of-david': (
        '<p>"The Root of David" is Christ’s self-title in <em>Revelation 5:5</em>: <em>"Behold, the Lion of the tribe of Juda, the Root of David, hath prevailed to open the book, and to loose the seven seals thereof"</em>; and again in <em>Revelation 22:16</em>: <em>"I Jesus have sent mine angel to testify unto you these things in the churches. I am the root and the offspring of David, and the bright and the morning star."</em> The title carries a striking theological ambiguity: Christ is BOTH the root (the source from which David sprang — for as God, He preceded David) AND the offspring (the descendant who came after David — as Man). Both halves are true. This is precisely how He answers the riddle in <em>Matthew 22:41-46</em>: David’s Son and David’s Lord at once.</p>'
    ),
    'sign-of-jonah': (
        '<p>The Sign of Jonah is the only sign Christ promised to the unbelieving generation that demanded one. <em>"An evil and adulterous generation seeketh after a sign; and there shall no sign be given to it, but the sign of the prophet Jonas: For as Jonas was three days and three nights in the whale’s belly; so shall the Son of man be three days and three nights in the heart of the earth"</em> (<em>Matthew 12:39-40</em>; cf. <em>16:4; Luke 11:29-30</em>). The sign is His burial and resurrection. The reluctant prophet swallowed by the fish and disgorged alive on Nineveh’s coast typifies the willing Christ swallowed by death and risen on the third day. The unbelieving generation can have no sign greater than that — and no sign smaller than that.</p>'
    ),
    'signet': (
        '<p>A signet is a personal seal-stone — often set in a ring — used by kings and nobles to authenticate documents, decrees, and ownership. Pressed into wax or clay, it left an unforgeable mark that could not be replicated without the original. Pharaoh gave Joseph his signet to administer Egypt’s grain (<em>"And Pharaoh took off his ring from his hand, and put it upon Joseph’s hand"</em>, <em>Genesis 41:42</em>). Ahasuerus gave Haman his signet to seal the genocide decree, then transferred it to Mordecai after Haman’s fall (<em>Esther 3:10; 8:2</em>). Daniel’s lions’ den was sealed with the king’s signet (<em>Daniel 6:17</em>). And in <em>Haggai 2:23</em>, the LORD declares of Zerubbabel: <em>"I will make thee as a signet"</em> — fulfilled in Christ his descendant.</p>'
    ),
    'simple': (
        '<p>In Proverbs, "the simple" (Hebrew <em>peti</em>) is the person not yet wise and not yet committed to folly — teachable, persuadable, easily led for good or ill. The book of Proverbs explicitly addresses such people as its primary audience: <em>"To give subtilty to the simple, to the young man knowledge and discretion"</em> (<em>1:4</em>). The simple believes every word (<em>14:15</em>), passes on into trouble unwarned (<em>22:3</em>), and is found at Wisdom’s door and Folly’s door alike (<em>9:4, 16</em>). The four wisdom-tiers in Proverbs descend or ascend from this point: <em>simple → fool → scoffer</em> (incurable) on the downward path; <em>simple → wise → instructed-of-the-LORD</em> on the upward. The simple is salvageable; the scoffer is not.</p>'
    ),
    'song-solomon': (
        '<p>The Song of Solomon (also titled Canticles or Song of Songs) is the Old Testament love-poem of Solomon — explicitly named in the opening verse as <em>"The song of songs, which is Solomon’s"</em> (<em>1:1</em>). It is one of his 1,005 songs (<em>1 Kings 4:32</em>) and the greatest of them (the Hebrew superlative <em>"song of songs"</em> parallels <em>"holy of holies"</em> and <em>"vanity of vanities"</em>). Written as a dialogue between a bridegroom and his bride, with watchmen and a chorus of daughters of Jerusalem, the book has been read across church history both <em>literally</em> (as a celebration of marital love within covenant) and <em>allegorically</em> (as the relationship between Christ and His church). Both readings have warrant; the literal grounds the allegorical.</p>'
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
