#!/usr/bin/env python3
"""Batch 25 — expand 25 more thin entries to 90-110 words each.

Targets: Hebrew vocabulary, OT figures, key verbs, eschatology,
heart-states, NT geography, Greek/cultural reframes, and pastoral
imagery from the 30-50 word bucket.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'ascend': (
        '<p>To <em>ascend</em> is to go up — and Scripture loads the verb with theological weight. It is the verb of pilgrimage: <em>"Who shall ascend into the hill of the LORD? or who shall stand in his holy place? He that hath clean hands, and a pure heart"</em> (<em>Psalm 24:3-4</em>; cf. the Psalms of Ascent, <em>120-134</em>, sung as pilgrims climbed to Jerusalem). It is the verb of incense and prayer: the prayers of the saints ascend before God (<em>Revelation 8:4</em>). And supremely it is the verb of Christ’s bodily ascension: <em>"He that descended is the same also that ascended up far above all heavens, that he might fill all things"</em> (<em>Ephesians 4:10</em>). The Hebrew <em>alah</em> also gives the modern term <em>aliyah</em> — "going up" to Israel. Christians ascend continually in worship.</p>'
    ),
    'ascribe': (
        '<p>To <em>ascribe</em> is to attribute, give credit to — and in Scripture it is the worship-verb par excellence. <em>"Give unto the LORD the glory due unto his name; worship the LORD in the beauty of holiness"</em> (<em>Psalm 29:2; 96:8</em>) is literally <em>"ascribe to YHWH glory."</em> Worship is fundamentally <em>ascription</em>: declaring out loud what is true of God. <em>"Ascribe ye greatness unto our God"</em> (<em>Deuteronomy 32:3</em>). The Christian does not <em>give</em> God anything He did not already possess; the worshiper merely names rightly what is. This is why the Psalms are so saturated with attributes — He is <em>strong</em>, <em>holy</em>, <em>just</em>, <em>merciful</em>, <em>everlasting</em>. Christian men should learn the discipline: speak God’s attributes back to Him, daily, out loud.</p>'
    ),
    'barak': (
        '<p>Barak son of Abinoam was the military commander summoned by Deborah the prophetess to lead Israel against Sisera and the army of Jabin king of Canaan (<em>Judges 4-5</em>). He refused to go without Deborah: <em>"If thou wilt go with me, then I will go: but if thou wilt not go with me, then I will not go"</em> (<em>4:8</em>). Deborah agreed but warned that the glory for the kill would go to a woman — fulfilled when Jael drove the tent peg through Sisera’s temple. The LORD gave Israel the victory at Mount Tabor and the brook Kishon. Yet despite the qualified reluctance, Barak is listed among the great in <em>Hebrews 11:32</em>’s faith-roll — proof that imperfect faith, joined to God’s call, still receives commendation.</p>'
    ),
    'batach': (
        '<p><em>Batach</em> (בָּטַח) is the Hebrew verb for <em>trust</em> — different from <em>aman</em> (to be firm, the root of <em>amen</em> and <em>emunah</em>). <em>Batach</em> emphasizes the <em>felt-security</em> of leaning the weight of one’s soul on something solid. To trust the LORD is to put your weight on Him with the confidence that He will hold. <em>"Trust [bitchu] in the LORD with all thine heart; and lean not unto thine own understanding"</em> (<em>Proverbs 3:5</em>); <em>"They that trust [bot’chim] in the LORD shall be as mount Zion, which cannot be removed, but abideth for ever"</em> (<em>Psalm 125:1</em>). The opposite is trusting in chariots, horses, riches, princes — every one of which collapses under enough weight. <em>Batach</em> in YHWH alone holds.</p>'
    ),
    'berakah': (
        '<p><em>Berakah</em> (בְּרָכָה) is the Hebrew word for <em>blessing</em>, and it runs in two directions. Blessing flows <em>from God to humans</em>: covenant favor, increase, fruitfulness, peace — <em>"The LORD bless thee, and keep thee... and give thee peace"</em> (<em>Numbers 6:24-26</em>, the great Aaronic <em>berakah</em>). And blessing flows <em>from humans to God</em>: acclaim and praise, the saints’ acknowledgment of God’s goodness — <em>"Bless the LORD, O my soul: and all that is within me, bless his holy name"</em> (<em>Psalm 103:1</em>). The patriarchal blessings in Genesis transfer covenant favor down generations (<em>Genesis 27, 48, 49</em>). Christian fathers should learn to bless their wives and children deliberately — at table, at bedside, at marriage, at death. <em>Berakah</em> is masculine work.</p>'
    ),
    'darius': (
        '<p>Several kings bear the name Darius in Scripture. Most prominent is <em>Darius the Mede</em> of <em>Daniel 6</em>, who took the kingdom after the fall of Belshazzar — a figure historians have variously identified with Cyrus, Cyaxares II, or Gubaru. He signed the foolish decree that put Daniel in the lions’ den, then was deeply troubled and could not sleep, and at dawn cried out: <em>"Daniel, servant of the living God, is thy God, whom thou servest continually, able to deliver thee from the lions?"</em> (<em>6:20</em>). Daniel’s deliverance moved Darius to issue a kingdom-wide decree: <em>"In every dominion of my kingdom men tremble and fear before the God of Daniel: for he is the living God, and stedfast for ever"</em> (<em>6:26</em>).</p>'
    ),
    'dispensational-premillennialism': (
        '<p>Dispensational premillennialism is the eschatological system that teaches two distinct divine programs (Israel and Church), a secret pre-tribulation rapture, a literal seven-year tribulation, and Christ’s subsequent 1000-year reign from Jerusalem. While premillennialism itself has ancient roots (Justin Martyr, Irenaeus), the <em>dispensational</em> form is a nineteenth-century systematization (J. N. Darby, the Scofield Reference Bible) widely held in modern American evangelicalism. Reformed and confessional Protestants generally reject the system in favor of amillennialism or postmillennialism — holding the church and elect Israel as one new-covenant people, and the millennium of <em>Revelation 20</em> as the present church age. Whatever the position, Christ’s call stands: <em>"Watch therefore: for ye know not what hour your Lord doth come"</em> (<em>Matthew 24:42-44</em>).</p>'
    ),
    'eden-garden': (
        '<p>The Garden of Eden was the garden God planted in the east, in which He placed the first man and woman (<em>Genesis 2:8-15</em>). Two trees were named at its center: the tree of life, and the tree of the knowledge of good and evil. The garden was watered by four rivers — Pishon, Gihon, Hiddekel (Tigris), and Euphrates — and Adam was placed there <em>"to dress it and to keep it"</em> (<em>2:15</em>), with dominion over every creature. Eden is the paradigm of unbroken communion between God and humanity, lost in the Fall when Adam ate of the forbidden tree and was cast out east of Eden, the way to the tree of life blocked by cherubim with a flaming sword (<em>3:24</em>). Christ opens the way back.</p>'
    ),
    'exalt-yhwh': (
        '<p>To "exalt the LORD" is the verb of declaring YHWH’s greatness publicly. The communal call of <em>Psalm 34:3</em> stands at the heart of it: <em>"O magnify the LORD with me, and let us exalt his name together."</em> Exaltation is not <em>adding to</em> God’s greatness — that would be impossible, for He is already infinitely high. It is <em>declaring</em> His greatness — out loud, to ourselves, to one another, before the nations: <em>"I will extol thee, my God, O king; and I will bless thy name for ever and ever. Every day will I bless thee"</em> (<em>Psalm 145:1-2</em>). Worship is therefore active, vocal, public, congregational. The Christian who lifts up the name of YHWH lifts up nothing he can diminish — and everything the world tries to suppress.</p>'
    ),
    'flax': (
        '<p>Flax is a slender annual plant (<em>Linum usitatissimum</em>) whose long fibers are spun into linen and whose short tow serves for wicks. Egypt and Israel both cultivated it for cloth and lamps. In Scripture flax becomes the image of gentle divine mercy: Isaiah’s prophecy of the Servant says, <em>"A bruised reed shall he not break, and the smoking flax shall he not quench: he shall bring forth judgment unto truth"</em> (<em>Isaiah 42:3</em>), quoted in <em>Matthew 12:20</em>. The Messiah fans the dimmest spark into flame rather than snuffing it. Pastors, fathers, and elders called to imitate Him must learn the same restraint: the weakest believer’s smoking faith is not to be quenched, but tended into fire. Strong men handle weak men gently.</p>'
    ),
    'heart-circumcision': (
        '<p>The circumcision of the heart is the inward, supernatural work in which God Himself cuts away <em>"the foreskin of the heart"</em> — its hardness, idolatry, and rebellion — that His people might love Him with all their heart and soul. Moses commanded it: <em>"Circumcise therefore the foreskin of your heart"</em> (<em>Deuteronomy 10:16</em>) — and then promised God Himself would perform it: <em>"And the LORD thy God will circumcise thine heart, and the heart of thy seed, to love the LORD thy God with all thine heart"</em> (<em>30:6</em>). Paul makes the inward act primary: <em>"he is a Jew, which is one inwardly; and circumcision is that of the heart, in the spirit, and not in the letter"</em> (<em>Romans 2:29</em>). The sign of true covenant membership is not flesh-cutting but heart-cutting.</p>'
    ),
    'jehu': (
        '<p>Jehu was the tenth king of the northern kingdom (841-814 BC), anointed by Elisha’s prophetic servant with explicit commission to extirpate the house of Ahab (<em>2 Kings 9:1-10</em>). Jehu drove furiously to Jezreel, killed king Joram of Israel and king Ahaziah of Judah, and ordered Jezebel thrown from her window — where the dogs ate her flesh, as Elijah had prophesied. He gathered the prophets of Baal under pretense of a great sacrifice and slaughtered them at Samaria, destroying Baal worship in Israel (<em>2 Kings 10</em>). Yet Jehu did not depart from Jeroboam’s sin — the golden calves at Bethel and Dan remained. The LORD rewarded him with four generations on the throne, but withheld revival. Faithfulness must be entire.</p>'
    ),
    'lit': (
        '<p>"Lit" is the generic Millennial / Gen-Z intensifier meaning excellent, exciting, or wild — often deployed about parties, music, festivals, or events that promise unrestrained pleasure: <em>"the show was lit"</em>, <em>"that party got lit"</em>, <em>"it’s gonna be lit tonight."</em> The deeper assumption embedded in the slang is that peak experience equals peak intoxication — that the highest moments of life are the ones in which inhibition disappears. Scripture has a different intensifier and a different model: <em>"And be not drunk with wine, wherein is excess; but be filled with the Spirit"</em> (<em>Ephesians 5:18</em>). The Christian alternative to the world’s "lit" is not boredom but Spirit-saturation — sober, joyful, mighty-in-praise, controlled-from-within. Be filled with the Spirit, not the bottle.</p>'
    ),
    'lysias': (
        '<p>Claudius Lysias was the Roman commander (<em>chiliarch</em>, "captain of the thousand") of the Antonia garrison overlooking the Jerusalem temple courts. When Paul was assaulted by the temple mob in <em>Acts 21-23</em>, Lysias intervened with his soldiers, arrested Paul to save him from being torn to pieces, and ordered him examined by scourging (which he canceled on learning of Paul’s Roman citizenship). He convened the Sanhedrin to inquire into the charges (<em>22:30</em>), uncovered an assassination plot against Paul through Paul’s sister’s son (<em>23:16</em>), and dispatched the apostle under heavy armed escort — 200 soldiers, 70 horsemen, 200 spearmen — to Felix at Caesarea, with an explanatory letter. The Roman judicial system, however imperfectly, served the providential preservation of the apostle.</p>'
    ),
    'malice': (
        '<p>Malice is settled ill-will — the deliberate, deep-seated desire to injure another. In the New Testament, malice (<em>kakia</em>) is consistently listed among the works of the flesh that must be put off: <em>"Put off all these; anger, wrath, malice, blasphemy, filthy communication out of your mouth"</em> (<em>Colossians 3:8</em>); <em>"Let all bitterness, and wrath, and anger, and clamour, and evil speaking, be put away from you, with all malice"</em> (<em>Ephesians 4:31</em>). Children of God are commanded paradoxically to be <em>"children in malice, but in understanding be men"</em> (<em>1 Corinthians 14:20</em>): infantile in capacity for ill-will, mature in capacity for thought. The Christian man cannot afford even small reserves of malice. They poison the family, the church, and finally the soul that hosts them.</p>'
    ),
    'nathan-prophet': (
        '<p>Nathan was the court prophet of David’s reign — a man positioned in proximity to royal power yet fearless before it. He brought David the Davidic Covenant promise of <em>2 Samuel 7</em>: an eternal throne for the line of David, fulfilled in Christ. After David’s sin with Bathsheba and murder of Uriah, Nathan came alone into the king’s presence and told the parable of the poor man’s ewe lamb (<em>2 Samuel 12:1-7</em>) — and when David’s anger blazed against the parable’s villain, Nathan said the eight words that broke the king: <em>"Thou art the man."</em> At the end of David’s reign Nathan supported Solomon’s succession against Adonijah (<em>1 Kings 1</em>). Nathan is the model of prophetic courage close to power — speaking truth without political calculation.</p>'
    ),
    'see': (
        '<p>To <em>see</em>, biblically, goes beyond physical sight. The deeper meaning is <em>perceptive recognition</em> — seeing-with-understanding. <em>"Their eyes were holden, that they should not know him"</em> (<em>Luke 24:16</em>) at Emmaus, until at the breaking of bread <em>"their eyes were opened, and they knew him"</em> (<em>24:31</em>). Christ’s parables draw the line between the disciples (who see and understand) and the crowds (who see and miss): <em>"Blessed are your eyes, for they see"</em> (<em>Matthew 13:16</em>). The Pharisees claimed sight but were blind (<em>John 9:39-41</em>). At the climactic level there is eschatological seeing: <em>"we shall see him as he is"</em> (<em>1 John 3:2</em>); <em>"Blessed are the pure in heart: for they shall see God"</em> (<em>Matthew 5:8</em>). True seeing is grace.</p>'
    ),
    'shekel-sanctuary': (
        '<p>The shekel of the sanctuary was the standardized weight-of-silver used for tabernacle and temple offerings — set apart from the variable common shekel of the marketplace. Half a sanctuary-shekel was the redemption-price required of every Israelite male twenty years and upward in the census: <em>"a half shekel after the shekel of the sanctuary... an offering to the LORD"</em> (<em>Exodus 30:13-16</em>). Rich and poor paid the same — <em>"The rich shall not give more, and the poor shall not give less"</em> (<em>30:15</em>) — and the silver went to the service of the tabernacle. The standardization itself was theological: YHWH’s worship is not subject to market fluctuation. He values souls equally; He requires payment evenly; He keeps His own measures.</p>'
    ),
    'shelter': (
        '<p>Shelter is covered protection from storm, sun, or enemy. Scripture treats God Himself as the deepest shelter of the saint: <em>"He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty"</em> (<em>Psalm 91:1</em>); <em>"For thou hast been a strength to the poor... a refuge from the storm, a shadow from the heat"</em> (<em>Isaiah 25:4</em>). The Christian household is to mirror this — a small shelter inside His larger one, a place of refuge for the weak, the orphan, the stranger, and the wounded. <em>"Pure religion and undefiled before God and the Father is this, To visit the fatherless and widows in their affliction"</em> (<em>James 1:27</em>). The roof we live under is a stewardship.</p>'
    ),
    'tzitzit': (
        '<p><em>Tzitzit</em> (צִיצִית) — "fringes, tassels" — were the cords the Israelites were commanded to wear on the corners of their garments, with a thread of blue running through, as a visible reminder to keep the commandments of the LORD: <em>"that ye may look upon it, and remember all the commandments of the LORD, and do them; and that ye seek not after your own heart and your own eyes"</em> (<em>Numbers 15:38-40</em>; cf. <em>Deuteronomy 22:12</em>). The woman with the issue of blood touched the <em>tzitzit</em> of Jesus’ garment in the press of the crowd and was healed (<em>Matthew 9:20</em>). Christ wore the <em>tzitzit</em>; He kept the commandments; and the very fringes of His obedience brought healing to those who touched them.</p>'
    ),
    'weariness-good': (
        '<p>"Weariness in well-doing" names the temptation, especially upon long-faithful saints, to grow tired of doing right when fruit seems slow and reward delayed. Paul commands directly against it: <em>"And let us not be weary in well doing: for in due season we shall reap, if we faint not"</em> (<em>Galatians 6:9</em>); <em>"But ye, brethren, be not weary in well doing"</em> (<em>2 Thessalonians 3:13</em>). Scripture does not deny that fatigue is real — it commands the refusal to <em>faint</em>. The promise is harvest in due season for those who do not give up. Pastors twenty years in, husbands thirty years in, parents discipling teenagers, missionaries on the long field — these are the saints most under this temptation. Keep going. Harvest is coming.</p>'
    ),
    'well': (
        '<p>A well is a hollow shaft sunk into the earth to reach water — a daily necessity in the ancient Near East, and in Scripture also a recurring setting of <em>covenant meetings</em>. Abraham’s servant found Rebekah at a well outside Nahor (<em>Genesis 24</em>); Jacob found Rachel at a well in Haran (<em>Genesis 29</em>); Moses met Zipporah at the well of Midian (<em>Exodus 2:15-21</em>); Christ found the Samaritan woman at Jacob’s well in Sychar (<em>John 4</em>). Each time, a bride is identified by a well. The pattern is providential: God brings His sons their wives at the place of water — and in the final case, the Bridegroom Himself finds His Gentile bride by the well, offering her <em>"living water springing up into everlasting life"</em>.</p>'
    ),
    'consider-his-ways': (
        '<p>"Consider your ways" is the twice-repeated post-exilic command of Haggai to the returned community: <em>"Now therefore thus saith the LORD of hosts; Consider your ways"</em> (<em>Haggai 1:5, 7</em>). The command is diagnostic, not abstract. Haggai forces honest inventory of how their life is actually going: <em>"Ye have sown much, and bring in little; ye eat, but ye have not enough; ye drink, but ye are not filled with drink; ye clothe you, but there is none warm; and he that earneth wages earneth wages to put it into a bag with holes"</em> (<em>1:6</em>). The reason: the LORD’s house lay neglected while they paneled their own. Self-examination as honest accounting — sober, specific, comparative — is the start of every reformation.</p>'
    ),
    'courtyard': (
        '<p>The courtyard is the open, walled inner space of an ancient house, temple, or palace — not the street, not the inner room, but the place where household and guests met under sky. The tabernacle had its outer court for sacrifice (<em>Exodus 27:9-19</em>); the temple had multiple courts (the court of the Gentiles, the court of the women, the court of Israel, the court of the priests); ordinary households had their <em>aulē</em>. Peter denied Christ in the high priest’s courtyard, warming himself at a brazier (<em>Luke 22:55-62</em>; <em>John 18:15-27</em>). The courtyard was where people actually gathered, where social life happened — the equivalent of the front porch, the family-room, and the back-yard combined. Recover the courtyard at home.</p>'
    ),
    'cyrus': (
        '<p>Cyrus was the founder of the Persian Empire — reigning 559-530 BC, conquering Babylon in 539 BC, and issuing in his first regnal year the decree returning exiled Jews to rebuild the temple at Jerusalem (<em>Ezra 1:1-4</em>; <em>2 Chronicles 36:22-23</em>). The most extraordinary thing about Cyrus is that Isaiah named him by name, calling him <em>"my shepherd"</em> and <em>"his anointed"</em> (<em>messiah</em>), some 150 years before his birth — when no kingdom of Persia yet existed (<em>Isaiah 44:28; 45:1-4</em>). The naming is one of Scripture’s most striking specific prophecies, and Cyrus’s decree fulfilled it. The LORD raises and lowers pagan kings to serve covenant purposes. The boundaries of empires are set by the God of Israel.</p>'
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
