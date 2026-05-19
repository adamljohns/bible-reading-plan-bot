#!/usr/bin/env python3
"""Batch 23 — expand 25 more thin entries to 90-110 words each.

Targets: Reformed soteriology, Hebrew vocabulary, OT books, key verbs,
ecclesial qualifications, cultural reframe, and household imagery
from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'preserving-grace': (
        '<p>Preserving grace is the continuous, sovereign grace by which God preserves His true people in faith and holiness unto final salvation. It is the Reformed doctrine of the perseverance of the saints viewed from God’s side: the saints persevere precisely because God preserves. <em>"Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ"</em> (<em>Philippians 1:6</em>); <em>"My sheep hear my voice, and I know them, and they follow me: and I give unto them eternal life; and they shall never perish, neither shall any man pluck them out of my hand"</em> (<em>John 10:27-28</em>). The Father keeps, the Son intercedes (<em>Hebrews 7:25</em>), the Spirit seals (<em>Ephesians 1:13-14</em>). The whole Godhead guards the elect.</p>'
    ),
    'qualifications-deacon': (
        '<p>The qualifications of a deacon are Paul’s list in <em>1 Timothy 3:8-13</em>: <em>"Likewise must the deacons be grave, not doubletongued, not given to much wine, not greedy of filthy lucre; holding the mystery of the faith in a pure conscience. And let these also first be proved; then let them use the office of a deacon, being found blameless. Even so must their wives be grave, not slanderers, sober, faithful in all things. Let the deacons be the husbands of one wife, ruling their children and their own houses well."</em> Like elders, deacons must be tested before commissioning. The office is one of mercy, table-service, and hands-on ministry to the saints. Character precedes service.</p>'
    ),
    'ransom-verb': (
        '<p>To <em>ransom</em> is to purchase liberation — to deliver someone from bondage, captivity, or death by paying a price. The LORD ransomed Israel from Egyptian slavery: <em>"I will redeem you with a stretched out arm, and with great judgments"</em> (<em>Exodus 6:6</em>). Job confessed: <em>"I know that my redeemer liveth"</em> (<em>Job 19:25</em>). Christ Himself owns the role: <em>"the Son of man came not to be ministered unto, but to minister, and to give his life a ransom for many"</em> (<em>Mark 10:45</em>; cf. <em>1 Timothy 2:6</em>). The price was real — His blood — and the Ransomer paid it Himself. Ransom is the courtroom-economic side of salvation: not free in the sense of cheap, but free to us because dear to Him.</p>'
    ),
    'reconciliation-act': (
        '<p>Reconciliation is the decisive, finished work of God in Christ’s death by which He reconciled the world unto Himself. <em>"To wit, that God was in Christ, reconciling the world unto himself, not imputing their trespasses unto them; and hath committed unto us the word of reconciliation. Now then we are ambassadors for Christ, as though God did beseech you by us: we pray you in Christ’s stead, be ye reconciled to God"</em> (<em>2 Corinthians 5:19-20</em>). Reconciliation is <em>God’s</em> side of peace-making accomplished, not negotiated — He has acted; the saint receives the proclamation. The cross removed the enmity (<em>Ephesians 2:14-17</em>; <em>Colossians 1:20</em>) so that hostile sinners may now come home as sons. Reconciled to God, the saint is reconciled to all who are likewise reconciled.</p>'
    ),
    'repentance-godly': (
        '<p>Godly repentance is sorrow over sin <em>according to God</em> — sorrow that hates sin as offense against Him, turns from it to Christ, and bears the fruit of changed life. <em>"For godly sorrow worketh repentance to salvation not to be repented of: but the sorrow of the world worketh death"</em> (<em>2 Corinthians 7:10</em>). The diagnostic Paul lists in the next verse is striking: godly sorrow produces <em>carefulness, clearing of yourselves, indignation, fear, vehement desire, zeal, revenge</em> — a whole cluster of repenting energies (<em>v. 11</em>). Worldly sorrow regrets consequences; godly sorrow grieves the offense against God Himself, just as David did in <em>Psalm 51:4</em>: <em>"Against thee, thee only, have I sinned."</em> The first leads to despair, the second to life.</p>'
    ),
    'ruth-book': (
        '<p>Ruth is the short, luminous narrative of covenant loyalty (<em>chesed</em>) set in the days of the judges. In four chapters, the Moabitess Ruth clings to her widowed Israelite mother-in-law Naomi — <em>"whither thou goest, I will go... thy people shall be my people, and thy God my God"</em> (<em>Ruth 1:16</em>) — gleans in the field of Boaz, is granted the privilege of kinsman-redemption, and becomes the great-grandmother of King David (<em>Ruth 4:17-22</em>). The book displays the kinsman-redeemer (<em>goel</em>) who foreshadows Christ: a near-kinsman of means who acts willingly, at his own cost, to bring a Gentile widow into the covenant family. Matthew names Ruth in the genealogy of Christ (<em>Matthew 1:5</em>). The Gentile bride is grafted in.</p>'
    ),
    'side-hustle': (
        '<p>"Side hustle" is the current slang for secondary income work pursued alongside a primary job — freelance writing, app-driven driving, weekend consulting, online resale, etc. The vocabulary celebrates entrepreneurial energy and self-reliance, and Scripture honors the diligent hand: <em>"The hand of the diligent shall bear rule: but the slothful shall be under tribute"</em> (<em>Proverbs 12:24</em>; cf. <em>10:4; 21:5</em>). Paul himself worked as a tentmaker alongside his apostolic labors (<em>Acts 18:3</em>). Yet the side-hustle culture often quietly contradicts the contentment Scripture also commands: <em>"having food and raiment let us be therewith content"</em> (<em>1 Timothy 6:8</em>). Christian men work hard, save wisely, give generously — and rest weekly, refusing the slavery of perpetual hustle. Six days work; one day Sabbath.</p>'
    ),
    'strife': (
        '<p>Strife is bitter conflict — angry contention — the deliberate fanning of sparks between people. Scripture lists it among the works of the flesh: <em>"adultery, fornication, uncleanness, lasciviousness, idolatry, witchcraft, hatred, variance, emulations, wrath, strife..."</em> (<em>Galatians 5:19-21</em>). Proverbs names its source bluntly: <em>"Only by pride cometh contention"</em> (<em>Proverbs 13:10</em>); <em>"A wrathful man stirreth up strife: but he that is slow to anger appeaseth strife"</em> (<em>15:18</em>); <em>"As coals are to burning coals, and wood to fire; so is a contentious man to kindle strife"</em> (<em>26:21</em>). The peacemaker is blessed (<em>Matthew 5:9</em>); the strife-stirrer is named alongside the sexually immoral. Christian men must refuse to be the spark, even when the wood is dry.</p>'
    ),
    'suffer': (
        '<p>To <em>suffer</em>, biblically, is to undergo pain, hardship, or loss — but Scripture gives suffering a distinct Christian shape. Christ suffered <em>for us</em>, leaving an example that we should follow His steps (<em>1 Peter 2:21</em>). The saints suffer <em>with</em> Christ as participation in His sufferings (<em>Philippians 3:10</em>; <em>Romans 8:17</em>): not redemptive in the same way, but covenantally united. Paul writes: <em>"tribulation worketh patience; and patience, experience; and experience, hope"</em> (<em>Romans 5:3-4</em>). The KJV also uses <em>suffer</em> archaically for "permit" — <em>"Suffer the little children to come unto me, and forbid them not"</em> (<em>Mark 10:14</em>). Either sense, the Christian holds the cup with the Master and finds the bitter cup turned to wine.</p>'
    ),
    'tamid': (
        '<p>The <em>tamid</em> (תָּמִיד, "continual") was the continual daily burnt offering — one lamb sacrificed in the morning and one in the evening, perpetually, throughout Israel’s generations (<em>Exodus 29:38-42</em>; <em>Numbers 28:3-8</em>). It was the heartbeat of tabernacle and temple worship — smoke ascended without break from the altar of burnt offering. The continuity itself was the testimony: God’s worship never paused. Daniel’s prophecy of the abomination of desolation specifies the cessation of the <em>tamid</em> as a desolation-marker (<em>Daniel 8:11-13; 11:31; 12:11</em>). Christ Himself is the true continual offering: <em>"by one offering he hath perfected for ever them that are sanctified"</em> (<em>Hebrews 10:14</em>) — once for all, perpetually efficacious.</p>'
    ),
    'tsedaqah': (
        '<p><em>Tsedaqah</em> (צְדָקָה) is the Hebrew word for righteousness — but the concept is relational and covenantal rather than abstract moral perfection. <em>Tsedaqah</em> is <em>right-relating</em>: faithful to covenant obligations, just in dealings, generous to the poor (in later Jewish usage <em>tsedaqah</em> came to mean almsgiving itself). YHWH’s <em>tsedaqah</em> is His covenant faithfulness expressed in saving action: <em>"My righteousness is near; my salvation is gone forth"</em> (<em>Isaiah 51:5</em>); <em>"The LORD hath made known his salvation: his righteousness hath he openly shewed in the sight of the heathen"</em> (<em>Psalm 98:2</em>). Christ is the fulfillment: God’s <em>tsedaqah</em> revealed in Him, imputed to His people (<em>Romans 1:17; 3:21-26</em>). Righteousness is therefore not a private virtue but a covenant verdict.</p>'
    ),
    'wait-on-yhwh': (
        '<p>To "wait on the LORD" is the disciplined posture of expectant trust — not passive idleness but active, hope-laden patience. The Hebrew <em>qavah</em> ("wait") shares its root with <em>tikvah</em> ("hope") — waiting and hoping are one verb in Hebrew. Isaiah’s classic: <em>"But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint"</em> (<em>Isaiah 40:31</em>). David repeats it: <em>"Wait on the LORD: be of good courage, and he shall strengthen thine heart: wait, I say, on the LORD"</em> (<em>Psalm 27:14</em>; cf. <em>37:7; 130:5-6</em>). Christian waiting is not killing time; it is the soul leaning forward into God’s appointed answer.</p>'
    ),
    'watchful': (
        '<p>Watchful is the disposition of alertness — observant, on guard. The watchman of <em>Ezekiel 33:1-9</em> is the prophet’s self-portrait: God holds him accountable for warnings he failed to give. <em>"When I say unto the wicked, O wicked man, thou shalt surely die; if thou dost not speak to warn the wicked from his way, that wicked man shall die in his iniquity; but his blood will I require at thine hand."</em> Every father, pastor, magistrate, and citizen of God’s kingdom inherits this office in proportion to his sphere. The watchman cannot save anyone; he can only sound the trumpet. The blood of the warned is on his own head; the blood of the unwarned is on the watchman. Sound it loudly.</p>'
    ),
    'zenas': (
        '<p>Zenas was a believer in the early church whom Paul commended to Titus: <em>"Bring Zenas the lawyer and Apollos on their journey diligently, that nothing be wanting unto them"</em> (<em>Titus 3:13</em>). His pairing with the eloquent Apollos suggests a teaching itinerary through Crete or further. He is the only named lawyer (Greek <em>nomikos</em>) among the early disciples — the term could refer either to a Roman jurist or to a scribe expert in Mosaic law. Tradition makes him a bishop in Lydda or Diospolis, perhaps the author of an early apocryphal Acts of Pilate. Zenas appears once and never again in Scripture — but the apostle’s charge to provision his journey reminds the church that the gospel’s teachers travel on the saints’ hospitality.</p>'
    ),
    '1samuel': (
        '<p>1 Samuel traces Israel’s great transition from the era of the judges to the monarchy, centered on three figures: the prophet Samuel, the rejected king Saul, and the anointed shepherd David. The opening chapters give Hannah’s prayer-promise and Samuel’s call (chs. 1-3); the middle stretches recount the demand for a king like the nations (ch. 8), Saul’s anointing and tragic disobedience (chs. 9-15), and David’s anointing and rise (chs. 16-31). The book’s great verse is the LORD’s rebuke to Samuel when he favored Eliab’s appearance: <em>"the LORD seeth not as man seeth; for man looketh on the outward appearance, but the LORD looketh on the heart"</em> (<em>1 Samuel 16:7</em>). The kingdom belongs to the heart-chosen.</p>'
    ),
    'atonement-blood': (
        '<p>Atonement blood is the blood of sacrificial animals — and supremely of Christ — by which atonement is made for sin. <em>Leviticus 17:11</em> is the foundational principle: <em>"For the life of the flesh is in the blood: and I have given it to you upon the altar to make an atonement for your souls: for it is the blood that maketh an atonement for the soul."</em> Life is in blood; blood makes atonement; atonement is by life-given-for-life — substitution. Hebrews makes the doctrine final: <em>"without shedding of blood is no remission"</em> (<em>Hebrews 9:22</em>). Christ’s blood is therefore not symbolic; it is the very life of God-in-flesh poured out in death, sufficient to cover every sin of every saint who comes by faith.</p>'
    ),
    'believe': (
        '<p>To <em>believe</em>, in Scripture, is to rely upon, trust, commit oneself to — not mere mental assent. James cautions: <em>"Thou believest that there is one God; thou doest well: the devils also believe, and tremble"</em> (<em>James 2:19</em>). Devils are theologically correct and damned. Saving belief is the active leaning-into of the whole self upon God’s revelation of Himself in Christ. <em>"For with the heart man believeth unto righteousness; and with the mouth confession is made unto salvation"</em> (<em>Romans 10:10</em>). The Greek <em>pisteuō</em> means both "believe" and "entrust." Saving faith therefore receives Christ (<em>John 1:12</em>), rests in Christ (<em>Hebrews 4:3</em>), looks to Christ (<em>John 3:14-15</em>), and follows Christ (<em>Mark 8:34</em>). The whole man commits to the whole Christ.</p>'
    ),
    'brazier': (
        '<p>A brazier is a metal pan or open vessel for holding burning coals — the portable hearth of the ancient world. Scripture uses it both as the king’s winter heater and as a stand-in for any open fire of household or shame. The king Jehoiakim sat by such a brazier in the winter-house and contemptuously cut up Jeremiah’s scroll piece by piece, throwing each piece into the fire until the whole roll was consumed (<em>Jeremiah 36:21-23</em>) — the LORD’s word burned by the LORD’s king. Peter warmed himself at a brazier in the high priest’s courtyard the night Christ was tried, and there denied his Master three times (<em>John 18:18, 25</em>). Open coals are honest; they expose what the soul does when warmed.</p>'
    ),
    'gevurah': (
        '<p><em>Gevurah</em> (גְּבוּרָה) is the Hebrew word for might — the prevailing-power side of God’s character. It is distinguished from <em>oz</em> (protective strength) and <em>chayil</em> (force / valor): <em>gevurah</em> is the raw might that breaks armies and rolls back seas. <em>"Thine, O LORD, is the greatness, and the power [gevurah], and the glory, and the victory, and the majesty"</em> (<em>1 Chronicles 29:11</em>). The plural <em>gevurot</em> ("mighty deeds") names YHWH’s saving acts in history — the plagues, the Red Sea, the conquest, the return from exile. The Spirit of the LORD that rested on Messiah included <em>"the spirit of counsel and might (gevurah)"</em> (<em>Isaiah 11:2</em>). Where weakness reigns, <em>gevurah</em> is the LORD’s answer.</p>'
    ),
    'green-pastures': (
        '<p>"Green pastures" is <em>Psalm 23:2</em>’s image of YHWH as Shepherd making the saint lie down in tender, well-watered pasture: <em>"He maketh me to lie down in green pastures: he leadeth me beside the still waters."</em> The Hebrew is more specific than the English: <em>neʾot deshe</em> — "pastures of tender grass." This is not just grazing-ground but rest-ground. A sheep lies down only when full and at peace; if hungry, thirsty, frightened, or harassed, it cannot lie down. The Shepherd’s provision is total enough that lying down becomes possible. Modern Christians who cannot rest — sleeping poorly, anxious always — should ask whether they have stopped following the Shepherd, or have wandered beyond the pastures He prepared.</p>'
    ),
    'hide-in-heart': (
        '<p>"Hide in my heart" names the discipline of <em>Psalm 119:11</em>: <em>"Thy word have I hid in mine heart, that I might not sin against thee."</em> The verb is <em>tsaphan</em> ("treasure up, hide, lay up") — the same word used for hiding valuables for safekeeping. Memorization and meditation are the protective storage of Scripture in the inner core of the person. The hidden word is available in the moment of temptation, comfort, witness, or warfare — when the Bible is not at hand, the heart still is. Christ Himself drew on hidden Scripture in the wilderness (<em>Matthew 4:1-11</em>). Christian men should hide what they cannot live without: Psalms, key NT texts, the Sermon on the Mount, the Romans road, the great doctrinal proof-passages. Treasure the Word.</p>'
    ),
    'judges-book': (
        '<p>Judges is the seventh book of the Old Testament, covering roughly 300 years between Joshua and Samuel. It records the dark cyclical pattern that followed Joshua’s death: Israel sins, the LORD sends an oppressor, the people cry out, the LORD raises a deliverer (a <em>judge</em>), the land has rest — and then the cycle repeats. Twelve judges are named, including Othniel, Ehud, Deborah, Gideon, Jephthah, and Samson. The recurring summary diagnoses the era: <em>"In those days there was no king in Israel: every man did that which was right in his own eyes"</em> (<em>Judges 17:6; 21:25</em>). The book preaches its own thesis: without a king, the people perish. The true King comes through David’s line.</p>'
    ),
    'lintel': (
        '<p>The lintel is the horizontal beam above a doorway. In Scripture it is most famously the place where Israel was commanded to brush the blood of the Passover lamb on the night of the tenth plague (<em>Exodus 12:7, 22</em>): <em>"And they shall take of the blood, and strike it on the two side posts and on the upper door post of the houses... And when I see the blood, I will pass over you."</em> The threefold mark — two doorposts and the lintel — formed a sign of mercy over every household. The angel of death passed by every blood-marked door. Christ is the Passover Lamb (<em>1 Corinthians 5:7</em>); His blood marks the lintel of every believing heart, and judgment passes over.</p>'
    ),
    'melek': (
        '<p><em>Melek</em> (מֶלֶךְ) is the Hebrew word for king. Scripture establishes that Israel’s true King is YHWH Himself: <em>"The LORD is our judge, the LORD is our lawgiver, the LORD is our king; he will save us"</em> (<em>Isaiah 33:22</em>). The human king (David’s line) reigns as YHWH’s vassal under the Davidic covenant. Christ is therefore <em>Melek HaMelakim</em> — <em>"King of Kings, and Lord of Lords"</em> (<em>Revelation 19:16</em>). The kingdom-theme runs from Eden’s dominion mandate (<em>Genesis 1:28</em>), through the Davidic covenant (<em>2 Samuel 7</em>), through the prophetic anticipations of the Messianic king (<em>Isaiah 9:6-7</em>), to Christ’s eschatological reign (<em>Revelation 11:15</em>). Every earthly king holds his crown on loan from the true <em>Melek</em>.</p>'
    ),
    'oz': (
        '<p><em>Oz</em> (עֹז) is the Hebrew word for strength — especially YHWH’s saving strength on behalf of His people. It is distinguished from <em>gevurah</em> (raw might) and <em>chayil</em> (force, valor): <em>oz</em> is fierce, protective strength — the strength of a mother for her children, the strength YHWH shows for the saint. <em>"The LORD is my strength [oz] and song, and he is become my salvation"</em> (<em>Exodus 15:2</em>; <em>Psalm 118:14</em>); <em>"In the LORD have I righteousness and strength"</em> (<em>Isaiah 45:24</em>). David ascribes <em>oz</em> to the LORD repeatedly in the Psalter (<em>29:11; 28:7; 81:1</em>). When the Christian feels weakest, <em>oz</em> is the name to call: not the strength to perform, but the strength of the LORD wrapped around the weak.</p>'
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
