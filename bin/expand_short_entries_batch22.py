#!/usr/bin/env python3
"""Batch 22 — expand 25 more thin entries to 90-110 words each.

Targets: heart-state pairs, Reformed soteriology, OT figures and books,
covenant names, offerings, virtues, and prayer disciplines from the
30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'binding-isaac': (
        '<p>The Binding of Isaac (Hebrew <em>Aqedah</em>, "binding") was God’s ultimate test of Abraham, commanding him to take his beloved son Isaac — <em>"thine only son Isaac, whom thou lovest"</em> — and offer him as a burnt offering on Mount Moriah (<em>Genesis 22:1-19</em>). Abraham obeyed without delay, splitting the wood, saddling the ass, and walking three days to the mountain. As Isaac asked, <em>"where is the lamb for a burnt offering?"</em>, Abraham answered: <em>"My son, God will provide himself a lamb."</em> The LORD halted the blade and provided a ram caught in the thicket. Moriah was the very mount on which the temple would later stand — and on which Christ would be crucified. The Father who tested Abraham did not spare His own Son.</p>'
    ),
    'covenant-lawsuit': (
        '<p>The Covenant Lawsuit (Hebrew <em>rib</em>, "legal contention") is the prophetic genre in which YHWH brings formal courtroom charges against His covenant-breaking people. The form is borrowed from ancient Near-Eastern suzerain-vassal treaty proceedings, and includes summons-to-witnesses (often heaven and earth — <em>Deuteronomy 32:1</em>; <em>Isaiah 1:2</em>; <em>Micah 6:1-2</em>), recitation of past covenant kindness, the indictment of specific violations, the call of evidence, and the verdict. Major examples include <em>Hosea 4:1-3</em>, <em>Isaiah 1:18-20</em>, <em>Micah 6:1-8</em>, and large sections of <em>Jeremiah</em>. The genre teaches that God is not arbitrary — He <em>argues</em> His judgments from covenant. Christian preaching that lacks the <em>rib</em> tone has lost half of biblical prophetic ministry.</p>'
    ),
    'divided-heart': (
        '<p>A divided heart is a heart that tries to serve God and another — mammon, idols, self, lust, reputation — at the same time. Scripture diagnoses it as <em>"faulty"</em>: <em>"Their heart is divided; now shall they be found faulty: he shall break down their altars, he shall spoil their images"</em> (<em>Hosea 10:2</em>). James calls the divided man <em>"double minded... unstable in all his ways"</em> (<em>James 1:8</em>) and commands the cure: <em>"Cleanse your hands, ye sinners; and purify your hearts, ye double minded"</em> (<em>4:8</em>). The remedy is the prayer of <em>Psalm 86:11</em>: <em>"unite my heart to fear thy name."</em> God Himself must unite what sin has divided. The Christian man cannot integrate himself; he must be re-knit by grace.</p>'
    ),
    'election-doctrine': (
        '<p>Election is the free, gracious, unconditional act by which God, before the foundation of the world, chose a definite people in Christ unto holiness, adoption, and glory — not because of foreseen worth, faith, or works, but according to the good pleasure of His own will. <em>"According as he hath chosen us in him before the foundation of the world... according to the good pleasure of his will, to the praise of the glory of his grace"</em> (<em>Ephesians 1:4-6</em>; cf. <em>Romans 9:11-16</em>; <em>2 Thessalonians 2:13</em>). The doctrine humbles the saved (no boasting), comforts them (no losing what God secured), and frees them to evangelize (the elect <em>will</em> come). Sovereign grace is not bad news; it is the only news that finally saves.</p>'
    ),
    'ember': (
        '<p>An ember is a single live coal still glowing under the ashes — small, easily missed, sufficient to rekindle a whole fire. Scripture honors the ember. Christ refuses to quench <em>"smoking flax"</em> — the faintly burning wick: <em>"A bruised reed shall he not break, and smoking flax shall he not quench, till he send forth judgment unto victory"</em> (<em>Matthew 12:20</em>; <em>Isaiah 42:3</em>). The Spirit fans the faint faith into flame; the LORD does not despise small beginnings (<em>Zechariah 4:10</em>). Christians who fear their faith is too weak should consider the ember: the LORD’s ministry is not to extinguish but to rekindle. The smallest live coal, set to fresh fuel and given breath, becomes a hearth, a forge, or a beacon.</p>'
    ),
    'ephah': (
        '<p>The <em>ephah</em> was a standard Mosaic-law dry-measure unit — roughly 22 liters, about 20 dry quarts. It was the basket-sized container used for grain, flour, and bulk produce. The just <em>ephah</em> is required by the law: <em>"Just balances, just weights, a just ephah, and a just hin, shall ye have: I am the LORD your God"</em> (<em>Leviticus 19:36</em>; cf. <em>Deuteronomy 25:14-15</em>; <em>Ezekiel 45:10</em>). The prophets repeatedly condemn the merchant who <em>"maketh the ephah small, and the shekel great"</em> (<em>Amos 8:5</em>). Zechariah’s vision shows wickedness personified as a woman sealed inside an <em>ephah</em> and carried to Shinar (<em>Zechariah 5:5-11</em>). The unit is now only retained in biblical translation, but the principle of honest measure abides.</p>'
    ),
    'heart-stone': (
        '<p>A heart of stone is the natural state of fallen man’s heart: stony, dead to the things of God, impenetrable to threat and promise alike. <em>Ezekiel 36:26</em> names it sharply: <em>"I... will take away the stony heart out of your flesh, and I will give you an heart of flesh."</em> The heart of stone cannot be softened by external means — not by reasoning, not by tragedy, not by sermons, not by music, not by guilt. It must be sovereignly removed by God and replaced by the new heart of flesh, the Spirit indwelling the believer. This is monergistic regeneration: God acts alone in the resurrection of the dead soul. The Christian was not a finer block of stone before his conversion; he was rock and now is flesh.</p>'
    ),
    'manna-doctrine': (
        '<p>Manna was the bread from heaven by which God fed Israel forty years in the wilderness (<em>Exodus 16</em>). It appeared each morning as a small round substance like coriander seed, was gathered before the sun grew hot, and did not keep overnight except on the sixth day — when a double portion fell, and the kept portion did not spoil (the Sabbath miracle). The manna ceased the very day Israel ate the produce of Canaan (<em>Joshua 5:12</em>). Christ identifies Himself as the true and greater manna: <em>"I am the bread of life... Your fathers did eat manna in the wilderness, and are dead. This is the bread which cometh down from heaven... he that eateth of this bread shall live for ever"</em> (<em>John 6:48-51</em>).</p>'
    ),
    'multitude-counsellors': (
        '<p>The <em>"multitude of counsellors"</em> is the wisdom-principle of decision-making by submitted counsel from multiple wise voices — repeated throughout Proverbs: <em>"Where no counsel is, the people fall: but in the multitude of counsellers there is safety"</em> (<em>Proverbs 11:14</em>; cf. <em>15:22; 24:6</em>). It is not democracy (counting votes) but discernment-by-many — pooling the wisdom God has distributed across His servants. Scripture treats the lone-decider — <em>"I trust my gut"</em>, <em>"I don’t need anyone’s input"</em> — as a fool. The surrounded-decider, who consults wise counselors before deciding, is treated as wise. The pattern applies to husbands, pastors, magistrates, and businessmen. The man who cannot be advised cannot be helped.</p>'
    ),
    'naboth': (
        '<p>Naboth the Jezreelite owned an ancestral vineyard adjacent to King Ahab’s palace. Ahab coveted it; Naboth refused to sell, citing Mosaic law: <em>"The LORD forbid it me, that I should give the inheritance of my fathers unto thee"</em> (<em>1 Kings 21:3</em>). Ahab sulked. Jezebel his wife arranged a sham trial with two false witnesses, had Naboth charged with blaspheming God and the king, and stoned to death along with his sons (<em>2 Kings 9:26</em>). Ahab seized the vineyard. The LORD sent Elijah to meet him there: <em>"In the place where dogs licked the blood of Naboth shall dogs lick thy blood"</em> (<em>1 Kings 21:19</em>) — which came to pass at Jezreel for both Ahab and Jezebel. The blood of the murdered righteous always speaks.</p>'
    ),
    'nehemiah-book': (
        '<p>The book of Nehemiah recounts how Nehemiah, cupbearer to Artaxerxes I of Persia, returned to Jerusalem (445 BC) and led the rebuilding of the city walls in just fifty-two days against fierce regional opposition from Sanballat, Tobiah, and Geshem (<em>Nehemiah 1-6</em>). Half the workers built; half stood guard with weapons. The latter chapters narrate Ezra’s public reading of the law before the assembled people at the Water Gate (<em>Nehemiah 8</em>), a great covenant renewal (<em>chs. 9-10</em>), and Nehemiah’s closing reforms against intermarriage, Sabbath-breaking, and temple corruption (<em>ch. 13</em>). The book is a masterclass in faithful, prayerful, courageous lay leadership. <em>"Should such a man as I flee?"</em> (<em>Nehemiah 6:11</em>) is its summary verse.</p>'
    ),
    'spiritual-warfare-armor': (
        '<p>Spiritual warfare is the believer’s daily combat — <em>"for we wrestle not against flesh and blood, but against principalities, against powers, against the rulers of the darkness of this world, against spiritual wickedness in high places"</em> (<em>Ephesians 6:12</em>). Paul names the full armor of God: the belt of truth, the breastplate of righteousness, feet shod with the preparation of the gospel of peace, the shield of faith, the helmet of salvation, the sword of the Spirit which is the Word of God, and prayer in the Spirit at every season (<em>Ephesians 6:13-18</em>). Five pieces of armor and two weapons (Word, prayer). The Christian man does not put it on once; he puts it on daily, deliberately, by prayer and the Word.</p>'
    ),
    'steadfastness': (
        '<p>Steadfastness is the Spirit-wrought firmness of soul that does not waver under pressure, drift in seasons of ease, or quit under prolonged trial. Paul closes 1 Corinthians with it: <em>"Therefore, my beloved brethren, be ye stedfast, unmoveable, always abounding in the work of the Lord, forasmuch as ye know that your labour is not in vain in the Lord"</em> (<em>1 Corinthians 15:58</em>). It is the fruit of being <em>"rooted and grounded"</em> in Christ (<em>Ephesians 3:17</em>; <em>Colossians 2:7</em>) and of feeding daily on His Word. Steadfastness is not natural temperament; some men are constitutionally restless, and they too can be made steadfast by grace. The faithful Christian is not the most gifted or eloquent — he is the one still there in twenty years.</p>'
    ),
    'trust-radical': (
        '<p>Radical trust is the faith that does not lean on its own understanding but commits its way wholly to the LORD. <em>"Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths"</em> (<em>Proverbs 3:5-6</em>). It is trusting Him with what cannot be controlled — health, finances, children, reputation, outcomes — surrendering what cannot be kept, and resting in the steadfast love that does not fail. <em>"Some trust in chariots, and some in horses: but we will remember the name of the LORD our God"</em> (<em>Psalm 20:7</em>). Radical trust is not the absence of planning, but the right ordering of it: a Christian plans like a steward and trusts like a son.</p>'
    ),
    'yhwh-mekaddishkem': (
        '<p><em>YHWH-Mekaddishkem</em> (יְהוָה מְקַדִּשְׁכֶם) — "the LORD that doth sanctify you" — is the covenant name God speaks of Himself in the Mosaic law: <em>"And ye shall keep my statutes, and do them: I am the LORD which sanctify you"</em> (<em>Leviticus 20:8</em>; cf. <em>22:32; Exodus 31:13</em>). The setting-apart of Israel as God’s holy nation is His own active work — not their achievement. He chose them; He covenanted with them; He sanctifies them. The doctrine carries into the New Covenant: <em>"By the which will we are sanctified through the offering of the body of Jesus Christ once for all... For by one offering he hath perfected for ever them that are sanctified"</em> (<em>Hebrews 10:10, 14</em>). Sanctification is YHWH’s name and YHWH’s work.</p>'
    ),
    'zeal-godly': (
        '<p>Godly zeal is the Spirit-wrought ardor that consumes the saint with passion for God’s glory, His house, His name, and His people. Christ Himself displayed it cleansing the temple: <em>"The zeal of thine house hath eaten me up"</em> (<em>John 2:17</em>; quoting <em>Psalm 69:9</em>). Paul writes: <em>"Not slothful in business; fervent in spirit; serving the Lord"</em> (<em>Romans 12:11</em>); Titus is to expect from a redeemed people <em>"a peculiar people, zealous of good works"</em> (<em>Titus 2:14</em>). Yet Paul warns of zeal <em>"not according to knowledge"</em> (<em>Romans 10:2</em>): unredeemed religious zeal becomes fanaticism, persecution, terror. Christian zeal is purified by Christ, governed by Scripture, and bears the fruit of good works — never bitterness, never violence.</p>'
    ),
    '2kings': (
        '<p>2 Kings traces the slow collapse of both Israelite kingdoms across roughly 300 years. The first half (chs. 1-17) covers the prophetic ministry of Elisha — successor to Elijah — and the parallel declines of the northern kingdom, ending in Samaria’s fall to Assyria in 722 BC and the deportation of the ten tribes (<em>2 Kings 17</em>). The second half (chs. 18-25) follows Judah alone through the great revival of Hezekiah and the Assyrian siege (chs. 18-20), the deep apostasy of Manasseh, the reforming reign of Josiah (chs. 22-23), and finally the Babylonian destruction of Jerusalem and burning of the temple in 586 BC. The book ends with the temple in ashes and the people in exile — the covenant prosecution complete.</p>'
    ),
    'chag': (
        '<p><em>Chag</em> (חַג) is the Hebrew word for the three great pilgrimage feasts at which every Israelite male was required to appear before the LORD at the central sanctuary: <em>"Three times in the year shall all thy males appear before the LORD God"</em> (<em>Exodus 23:14-17</em>; <em>Deuteronomy 16:16</em>). The three are Passover (Pesach, with Unleavened Bread), the Feast of Weeks (Shavuot / Pentecost), and the Feast of Tabernacles (Sukkot). <em>Chag</em> is distinguished from other holy days (Sabbath, Day of Atonement, new moons) — it specifically denotes a pilgrimage festival, a covenant gathering of the whole people in the place the LORD chose to put His name. All three find their substance and fulfillment in Christ.</p>'
    ),
    'clean-heart': (
        '<p>The clean heart is the heart God Himself creates — washed by sacrificial blood, indwelt by His Spirit, single in devotion. David prays it after his great sin: <em>"Create in me a clean heart, O God; and renew a right spirit within me"</em> (<em>Psalm 51:10</em>). The Hebrew verb <em>baraʾ</em> ("create") is the same verb used of Genesis 1 creation — only God can do this. It is both gift and goal: the regenerate condition that marks every true saint (<em>Acts 15:9</em>) and the daily prayer that sanctifies him until he sees God (<em>Matthew 5:8</em>: <em>"Blessed are the pure in heart: for they shall see God"</em>). Christian men pray for clean hearts daily, knowing only the Creator can produce them.</p>'
    ),
    'el-elohe-israel': (
        '<p><em>El Elohe Israel</em> (אֵל אֱלֹהֵי יִשְׂרָאֵל) — "God, the God of Israel" — is the covenant name Jacob pronounced at the altar he built at Shechem after returning to the Promised Land from Padan-aram: <em>"And he erected there an altar, and called it El-elohe-Israel"</em> (<em>Genesis 33:20</em>). Jacob — newly renamed <em>Israel</em> at Peniel — declares that the God of his fathers Abraham and Isaac is now <em>his own</em> God. The name is a personal covenantal claim: the El of the patriarchs is not abstract deity but his particular LORD, in covenant with him by name. Every Christian father who builds an altar in his own home — family worship, family prayer — names the same God his.</p>'
    ),
    'heart-new': (
        '<p>The new heart is the promised covenant gift of <em>Ezekiel 36:26-27</em>: <em>"A new heart also will I give you, and a new spirit will I put within you... and cause you to walk in my statutes, and ye shall keep my judgments, and do them."</em> It is the inward credential of true conversion — the engine of all evangelical obedience and the absolute prerequisite for any righteous walk. The new heart is not the old heart cleaned, refurbished, or restored; it is a wholly new creation given by sovereign grace. Christian assurance rests here: where the new heart is, the law-keeping must follow, by Spirit-given energy — and where the law-keeping is absent, the new heart has not been given. Test yourselves.</p>'
    ),
    'kindling': (
        '<p>Kindling is the small, dry, deliberately gathered fuel that gets a fire going — the twigs and shavings the woodsman lays before the log. Spiritually, it names the small daily acts by which the Spirit sets a heart and a household ablaze: an opened Bible at the table, a knee bent at the bedside, a song hummed over a sleeping child, a verse memorized while waiting in line. None of these feels like fire on the day it is done. None looks like much in isolation. But the LORD lays kindling, breathes upon it, and what was nothing becomes a hearth. Christian men should pile dry kindling daily and stop waiting for the lightning strike. Fire follows fuel.</p>'
    ),
    'lovingkindness': (
        '<p>"Lovingkindness" is the English compound coined to capture the untranslatable Hebrew <em>chesed</em> — covenant loyalty matched with steadfast affection. It is not soft sentiment but iron-hearted devotion that keeps covenant even when the other party has failed. The defining characteristic of YHWH toward His people: <em>"The LORD’s lovingkindnesses... fail not. They are new every morning: great is thy faithfulness"</em> (<em>Lamentations 3:22-23</em>); <em>"Thy lovingkindness is better than life"</em> (<em>Psalm 63:3</em>); <em>"He delighteth in mercy [chesed]"</em> (<em>Micah 7:18</em>). The word echoes in <em>chesed</em>’s plural <em>chasidim</em> ("the loyal ones"). Christian husbands are to love their wives with <em>chesed</em> — sticking when feeling has flagged. <em>Chesed</em> outlasts emotion.</p>'
    ),
    'minchah-offering': (
        '<p>The <em>minchah</em> (מִנְחָה, "gift, tribute") is the Mosaic grain offering, prescribed in <em>Leviticus 2</em> — fine flour with oil and frankincense, sometimes baked into cakes, sometimes raw, sometimes mingled, but never with leaven or honey. It usually accompanied an animal sacrifice (the <em>olah</em> or the peace offering), and was sometimes offered alone. A portion was burned on the altar as a <em>"memorial"</em>, and the rest belonged to the priests. The <em>minchah</em> represented the consecration of the worshipper’s labor — bread, the work of human hands, presented to God. Christ Himself is the true <em>minchah</em>: <em>"the bread of God... which cometh down from heaven, and giveth life unto the world"</em> (<em>John 6:33</em>). Every Lord’s Table proclaims it.</p>'
    ),
    'perseverance-prayer': (
        '<p>Perseverance in prayer is the Spirit-wrought continuance that does not faint when answers tarry. Christ commanded importunity in the parable of the unjust judge: <em>"Men ought always to pray, and not to faint"</em> (<em>Luke 18:1</em>); Paul commanded ceaselessness: <em>"pray without ceasing"</em> (<em>1 Thessalonians 5:17</em>; cf. <em>Colossians 4:2</em>; <em>Ephesians 6:18</em>). The saints in Scripture wrestled, knocked, watched, and prevailed — Jacob at Peniel (<em>Genesis 32:24-30</em>), Hannah at the tabernacle (<em>1 Samuel 1</em>), Daniel at the window (<em>Daniel 6:10</em>), Paul concerning the thorn (<em>2 Corinthians 12:8</em>) — not because their persistence forced God’s hand, but because faith outlasts unbelief. The man who keeps praying has the answer already: he believes God hears.</p>'
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
