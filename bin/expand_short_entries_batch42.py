#!/usr/bin/env python3
"""Batch 42 — expand 25 more entries from the 50-60 word bucket.

Targets: body gestures, parables, doctrines, Hebrew vocab, OT figures,
covenant theology, ethics, ecclesial categories, and slang reframes.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    'bowing-head': (
        '<p>Bowing the head is the body’s short confession of submission — before God, before authority, before grief. It is the simplest and most universal worship-posture in Scripture. Abraham’s servant bowed his head at the well when the LORD prospered his mission to find Isaac’s bride: <em>"And the man bowed down his head, and worshipped the LORD"</em> (<em>Genesis 24:26</em>). Israel bowed the head and worshipped when Moses delivered the Passover instructions (<em>Exodus 12:27</em>). The four-and-twenty elders bow before the throne (<em>Revelation 4:10</em>). Most pointedly, Christ Himself at the cross: <em>"he bowed his head, and gave up the ghost"</em> (<em>John 19:30</em>). The bowed head precedes every great surrender.</p>'
    ),
    'build-on-sand': (
        '<p>"Build on sand" comes from the closing parable of the Sermon on the Mount (<em>Matthew 7:24-27</em>; <em>Luke 6:46-49</em>). The wise man hears Christ’s words <em>and</em> does them, building his house on the rock; the foolish man hears Christ’s words but does not do them, building on sand. When the rain, floods, and winds come — and they always come — the rock-house stands; the sand-house falls, <em>"and great was the fall of it"</em>. The contrast is not hearing versus not-hearing; it is hearing-and-doing versus hearing-without-doing. James echoes the warning: <em>"Be ye doers of the word, and not hearers only, deceiving your own selves"</em> (<em>James 1:22</em>). Hear; obey; survive the storm.</p>'
    ),
    'conquering-king': (
        '<p>"Conquering King" is one of the central New Testament titles for the risen and returning Christ. In <em>Revelation 6:2</em> He goes forth <em>"conquering, and to conquer"</em> on the white horse — the first seal opened. In <em>Revelation 19:11-16</em> He returns: <em>"And his eyes were as a flame of fire, and on his head were many crowns... And out of his mouth goeth a sharp sword, that with it he should smite the nations... and he shall rule them with a rod of iron... And he hath on his vesture and on his thigh a name written, KING OF KINGS, AND LORD OF LORDS."</em> The saint marches under that King, in His train of triumph: <em>"thanks be unto God, which always causeth us to triumph in Christ"</em> (<em>2 Corinthians 2:14</em>).</p>'
    ),
    'covenant-blessings': (
        '<p>Covenant blessings are the favors promised to Israel for covenant faithfulness, listed in <em>Deuteronomy 28:1-14</em>: <em>"Blessed shalt thou be in the city, and blessed shalt thou be in the field. Blessed shall be the fruit of thy body, and the fruit of thy ground... Blessed shalt thou be when thou comest in, and blessed shalt thou be when thou goest out."</em> The blessings parallel the covenant curses of the rest of the chapter but are far shorter — only 14 verses to the curses’ 54, an asymmetry that records the law’s tragic realism about Israel’s coming history. Christ in the New Covenant inherits the blessings on behalf of His people: <em>"Blessed be the God and Father of our Lord Jesus Christ, who hath blessed us with all spiritual blessings in heavenly places in Christ"</em> (<em>Ephesians 1:3</em>).</p>'
    ),
    'covenant-keeper': (
        '<p>A covenant keeper is one who holds the terms of a sworn covenant — and the LORD is praised throughout Scripture as the great Covenant Keeper. <em>"Know therefore that the LORD thy God, he is God, the faithful God, which keepeth covenant and mercy with them that love him and keep his commandments to a thousand generations"</em> (<em>Deuteronomy 7:9</em>); cf. <em>1 Kings 8:23; Nehemiah 1:5; 9:32; Daniel 9:4</em>. The saint is called to mirror Him: <em>"He that sweareth to his own hurt, and changeth not"</em> (<em>Psalm 15:4</em>). Christian marriages, friendships, business dealings, and church memberships are tested by this character. The kingdom of God is built of covenant keepers — men whose word does not return void.</p>'
    ),
    'cymbal': (
        '<p>A cymbal is a pair of bronze percussion plates struck together — in Scripture, used in tabernacle and temple worship by Asaph and his sons under David’s appointment: <em>"Asaph the chief, and next to him Zechariah... with psalteries and with harps; but Asaph made a sound with cymbals"</em> (<em>1 Chronicles 16:5; 25:1, 6</em>). The climactic <em>Psalm 150</em>’s call to praise lists them last: <em>"Praise him upon the loud cymbals: praise him upon the high sounding cymbals"</em> (<em>v. 5</em>). Yet Paul deploys the same instrument as warning: spiritual gifts exercised without love sound empty. <em>"Though I speak with the tongues of men and of angels, and have not charity, I am become as sounding brass, or a tinkling cymbal"</em> (<em>1 Corinthians 13:1</em>).</p>'
    ),
    'double-portion': (
        '<p>The double portion is, in Old Testament inheritance law, the firstborn son’s share — twice that of any other son: <em>"But he shall acknowledge the son of the hated for the firstborn, by giving him a double portion of all that he hath"</em> (<em>Deuteronomy 21:17</em>). Elisha famously asks Elijah for it spiritually as the master prepares to be taken up: <em>"I pray thee, let a double portion of thy spirit be upon me"</em> (<em>2 Kings 2:9</em>). The request is not for twice as much Spirit but for the firstborn-son’s heritage of his master’s ministry. Elisha then performed exactly twice the recorded miracles of Elijah. The double portion belongs to Christ, the Firstborn (<em>Hebrews 1:6; Romans 8:29</em>) — and shared with His brethren.</p>'
    ),
    'dust-returns': (
        '<p>"Dust returns to dust" is the biblical statement of human mortality — the body’s return to its created material. <em>Genesis 3:19</em> announces it as part of the curse of the fall: <em>"In the sweat of thy face shalt thou eat bread, till thou return unto the ground; for out of it wast thou taken: for dust thou art, and unto dust shalt thou return."</em> <em>Ecclesiastes 12:7</em> echoes it with a critical addition: <em>"Then shall the dust return to the earth as it was: and the spirit shall return unto God who gave it."</em> Body and spirit separate at death; both return to their source. The resurrection of the body is the eschatological reversal: <em>"so also is the resurrection of the dead. It is sown in corruption; it is raised in incorruption"</em> (<em>1 Corinthians 15:42</em>).</p>'
    ),
    'euthanasia': (
        '<p>"Euthanasia" (Greek: "good death") names the intentional ending of a sufferer’s life — assisted suicide, mercy killing, doctor-administered death — increasingly legalized across the West. Scripture rejects it categorically. God alone has authority over life and death: <em>"The LORD killeth, and maketh alive: he bringeth down to the grave, and bringeth up"</em> (<em>1 Samuel 2:6</em>). The sixth commandment prohibits taking innocent human life (<em>Exodus 20:13</em>). Scripture acknowledges suffering and commends compassion — but never authorizes intentional killing as remedy. Job endured extraordinary suffering without requesting death and was vindicated (<em>Job 42</em>). Christ’s own dying was prolonged, not shortened. Life belongs to God; it is not ours to end. Compassion is medicine and palliative care, not the lethal dose.</p>'
    ),
    'fear-of-the-lord': (
        '<p>The Fear of the LORD is the reverent awe of God that Scripture names by many superlatives. It is <em>"the beginning of wisdom"</em> (<em>Proverbs 9:10; Psalm 111:10</em>) and <em>"the beginning of knowledge"</em> (<em>Proverbs 1:7</em>). It is <em>"clean, enduring for ever"</em> (<em>Psalm 19:9</em>). It is the saint’s strong confidence: <em>"In the fear of the LORD is strong confidence: and his children shall have a place of refuge"</em> (<em>Proverbs 14:26</em>). It is the whole duty of man (<em>Ecclesiastes 12:13</em>). It is not slavish terror that drives one from God; it is reverent submission that draws one to Him — the right disposition of a creature before the Holy God. The man without it may be religious; he is not yet wise.</p>'
    ),
    'forsake': (
        '<p>To <em>forsake</em> is to abandon, leave behind, or give up. In Scripture, the verb cuts both ways. God’s great promise to His people is that He will <em>never</em> forsake them: <em>"I will never leave thee, nor forsake thee"</em> (<em>Hebrews 13:5</em>, quoting <em>Deuteronomy 31:6, 8</em>; <em>Joshua 1:5</em>). The saints’ corresponding obligation is to <em>forsake</em> idols, evil ways, and the world: <em>"Let the wicked forsake his way, and the unrighteous man his thoughts"</em> (<em>Isaiah 55:7</em>). The cross-cry is the verb at its deepest pitch: <em>"My God, my God, why hast thou forsaken me?"</em> (<em>Matthew 27:46</em>; <em>Psalm 22:1</em>). Christ was forsaken in our place that we might never be forsaken.</p>'
    ),
    'generational-blessing': (
        '<p>Generational blessing is the covenantal favor that flows from the patriarch to his children and grandchildren — often spoken at named transitions: deathbed, departure, ordination, wedding. Isaac blessed Jacob (and unwittingly transferred Esau’s blessing along the line of God’s election, <em>Genesis 27</em>). Jacob blessed his twelve sons on his deathbed (<em>Genesis 49</em>) — and crossed his hands to bless Joseph’s sons Ephraim before Manasseh (<em>Genesis 48</em>). Moses blessed the twelve tribes (<em>Deuteronomy 33</em>). The spoken word in Scripture has shaping power across generations. Christian fathers should consciously speak blessings over their wives and children — not as superstition, but as the patriarchal exercise of an office God still honors. Bless the next generation; do not curse it with silence.</p>'
    ),
    'guilelessness': (
        '<p>Guilelessness is the moral disposition of one who does not deceive — transparent, undouble-tongued, free of hidden malice. Christ commended Nathanael with one of His highest commendations: <em>"Behold an Israelite indeed, in whom is no guile!"</em> (<em>John 1:47</em>). Peter applies the same word to Christ Himself: <em>"Who did no sin, neither was guile found in his mouth"</em> (<em>1 Peter 2:22</em>; quoting <em>Isaiah 53:9</em>). David: <em>"Blessed is the man... in whose spirit there is no guile"</em> (<em>Psalm 32:2</em>). Guilelessness is not naive simplicity (the disciple is also to be wise as serpents, <em>Matthew 10:16</em>); it is moral transparency — what is inside is what comes out. The Christian man’s yes is yes; his no is no.</p>'
    ),
    'hevel': (
        '<p><em>Hevel</em> (הֶבֶל) is the Hebrew noun translated <em>"vanity"</em> in the KJV Ecclesiastes — literally <em>breath, vapor, smoke</em>. The image is something visible-but-uncatchable: you can see it, but you cannot grasp it. The word appears 38 times in Ecclesiastes alone — more than half its uses in all of Scripture. <em>"Vanity of vanities, saith the Preacher; vanity of vanities; all is vanity [havel havalim]"</em> (<em>1:2; 12:8</em>). Strikingly, <em>hevel</em> is also the Hebrew name of <em>Abel</em>, the second son of Adam (<em>Genesis 4</em>) — possibly the first <em>hevel</em>: the brief-lived righteous man whose breath was cut short. The Preacher’s whole book riffs on what is vapor and what endures. Fear God endures.</p>'
    ),
    'homie': (
        '<p>"Homie" is Gen-X / hip-hop slang for a close friend — especially one from the same neighborhood, school, or shared background. The slang celebrates loyalty to one’s own circle. Scripture honors deep friendship — Jonathan and David are the great model — but it expands the circle wider than blood, neighborhood, or culture. In Christ, the homie pool is the whole household of faith, drawn from every tribe and tongue. <em>"For ye are all the children of God by faith in Christ Jesus... There is neither Jew nor Greek, there is neither bond nor free, there is neither male nor female: for ye are all one in Christ Jesus"</em> (<em>Galatians 3:26-28</em>). The Christian’s deepest homies are baptized brothers worldwide.</p>'
    ),
    'husbandry': (
        '<p>Husbandry is the patient cultivation of land and livestock — the discipline by which the householder turns soil and herd into food and provision for his people. Scripture is densely husbandry-imaged. God Himself is named the <em>husbandman</em> of His people’s vineyard: <em>"I am the true vine, and my Father is the husbandman"</em> (<em>John 15:1</em>). Paul calls the church <em>"God’s husbandry"</em>: <em>"For we are labourers together with God: ye are God’s husbandry, ye are God’s building"</em> (<em>1 Corinthians 3:9</em>). The noble work of farming is treated throughout Scripture as priestly stewardship of creation — Adam was placed in Eden <em>"to dress it and to keep it"</em> (<em>Genesis 2:15</em>). Cultivate the ground; cultivate the soul.</p>'
    ),
    'jonathan': (
        '<p>Jonathan was the eldest son of King Saul — covenant friend of David and crown prince of Israel by birth — who chose costly loyalty to David (God’s anointed) over his own dynastic claim to his father’s throne. <em>"The soul of Jonathan was knit with the soul of David, and Jonathan loved him as his own soul"</em> (<em>1 Samuel 18:1</em>). He made covenant with David, gave him his royal robe and sword (<em>18:3-4</em>), warned him by arrows in the field (<em>1 Samuel 20</em>), and renewed covenant when David hid at Horesh (<em>23:18</em>). He died fighting beside his apostate father on Mount Gilboa (<em>1 Samuel 31</em>). David’s lament: <em>"thy love to me was wonderful, passing the love of women"</em> (<em>2 Samuel 1:26</em>). Covenant friendship at its highest.</p>'
    ),
    'judas': (
        '<p>Judas Iscariot was one of the twelve apostles whom Christ deliberately chose, who kept the common purse, who was a thief (<em>"and bare what was put therein"</em>, <em>John 12:6</em>), who betrayed Christ to the chief priests for thirty pieces of silver — the price of a slave (<em>Matthew 26:14-16</em>) — and who hanged himself in remorse without repentance (<em>Matthew 27:3-5</em>; <em>Acts 1:18-19</em>). Christ called him <em>"the son of perdition"</em> (<em>John 17:12</em>). He is the most sobering case in the New Testament: outward apostleship — three years of intimate access, casting out demons in Christ’s name, preaching the kingdom — without inward life. Judas warns every minister and elder: nearness to Christ does not save where the heart is not regenerate.</p>'
    ),
    'kohen': (
        '<p><em>Kohen</em> (כֹּהֵן) is the Hebrew word for <em>priest</em> — one who mediates between God and people, offering sacrifices, pronouncing the priestly blessing (<em>Numbers 6:24-26</em>), and instructing in the law. Aaron’s descendants were set apart as the <em>kohanim</em> under the old covenant; the broader tribe of Levi served as their assistants. Christ is the great High <em>Kohen</em> of the new covenant — not after the Aaronic order but after the order of Melchizedek (<em>Hebrews 7</em>), eternal, sinless, sufficient. And all believers in Christ are now <em>kohanim</em> together in the priesthood of all believers: <em>"ye are a chosen generation, a royal priesthood, an holy nation, a peculiar people"</em> (<em>1 Peter 2:9</em>; cf. <em>Revelation 1:6; 5:10</em>). The Christian man is therefore a priest.</p>'
    ),
    'mildness': (
        '<p>Mildness is the saintly disposition that does not aggravate — soft of word, slow of temper, deliberate in handling those whose nerves are already raw. Paul commands it specifically of pastors: <em>"Not given to wine, no striker, not greedy of filthy lucre; but patient, not a brawler, not covetous"</em> (<em>1 Timothy 3:3</em>; cf. <em>Titus 1:7; 3:2</em>). Mildness is one of the characteristic temperaments of those entrusted with souls — for a sharp man at the head of a congregation, however gifted, wounds where he should heal. <em>"And the servant of the Lord must not strive; but be gentle unto all men, apt to teach, patient"</em> (<em>2 Timothy 2:24</em>). The Christian elder is strong <em>and</em> mild — the order is the strength of grace under control.</p>'
    ),
    'mission-biblical': (
        '<p>Mission, biblically, is the errand on which one is <em>sent</em>. The New Testament word for "sent ones" is <em>apostoloi</em> — apostles. The church’s greatest mission is the Great Commission of <em>Matthew 28:18-20</em>: <em>"Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost: Teaching them to observe all things whatsoever I have commanded you."</em> The pattern is Trinitarian and cascading: the Father sent the Son (<em>John 20:21</em>: <em>"as my Father hath sent me, even so send I you"</em>); the Son sent the Spirit (<em>John 15:26</em>); the Father and Son together send the church; the church sends the missionary. Mission is always derivative; the Originator is God.</p>'
    ),
    'neighbor': (
        '<p>A neighbor is the fellow human placed within reach of one’s life and care — and in the Levitical and Christian ethic, the proper object of love after God Himself. <em>"Thou shalt love thy neighbour as thyself"</em> (<em>Leviticus 19:18</em>) is summarized by Christ as the second great commandment: <em>"And the second is like unto it, Thou shalt love thy neighbour as thyself. On these two commandments hang all the law and the prophets"</em> (<em>Matthew 22:39-40</em>). Christ’s parable of the Good Samaritan (<em>Luke 10:25-37</em>) re-defines the term against the lawyer’s narrowing question: a neighbor is whoever is in front of you needing mercy — not the one with whom you happen to share ethnicity, theology, or politics. Love crosses lines.</p>'
    ),
    'new-heavens': (
        '<p>The "new heavens" is the renewed celestial realm of the consummated kingdom — prophesied by Isaiah, restated by Peter, and seen by John in vision. <em>"For, behold, I create new heavens and a new earth: and the former shall not be remembered, nor come into mind"</em> (<em>Isaiah 65:17; cf. 66:22</em>); <em>"Nevertheless we, according to his promise, look for new heavens and a new earth, wherein dwelleth righteousness"</em> (<em>2 Peter 3:13</em>); <em>"And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away"</em> (<em>Revelation 21:1</em>). Paired with the new earth, the new heavens are not <em>different</em> heavens but <em>renewed</em> ones — the cosmos liberated from the curse and restored to glory under the Lamb’s rule.</p>'
    ),
    'nicolaitans': (
        '<p>The Nicolaitans were a first-century sect within or adjacent to the church — mentioned in Christ’s letters to two of the seven churches in <em>Revelation</em>. To Ephesus: <em>"But this thou hast, that thou hatest the deeds of the Nicolaitans, which I also hate"</em> (<em>2:6</em>). To Pergamos: <em>"So hast thou also them that hold the doctrine of the Nicolaitans, which thing I hate"</em> (<em>2:15</em>). The Lord twice declares He <em>hates</em> their works and doctrine — a rare directness. The exact teaching is debated. Ancient writers (Irenaeus, Hippolytus) associated them with eating meat sacrificed to idols and sexual immorality. The etymology (<em>nikao</em> "conquer" + <em>laos</em> "people") may hint at clergy domination of laity. Whatever the specifics, Christ’s verdict is plain.</p>'
    ),
    'nifty': (
        '<p>"Nifty" is mid-twentieth-century American slang — a mild positive adjective for something cleverly designed or attractively practical: <em>"that’s a nifty trick,"</em> <em>"a nifty little gadget."</em> The slang is era-stamped (1940s-60s) and gently disappearing from contemporary speech. Its underlying instinct, however, is healthy: appreciation for craftsmanship, clever design, and practical excellence — an instinct the biblical man shares. <em>"And he hath filled him with the spirit of God, in wisdom, in understanding, and in knowledge, and in all manner of workmanship"</em> (<em>Exodus 35:31</em>) — of Bezalel’s God-given craftsmanship in the tabernacle. Craft well-done is a small reflection of the Creator who built well. Honor the craftsman. Use the word again.</p>'
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
