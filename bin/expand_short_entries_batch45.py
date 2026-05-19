#!/usr/bin/env python3
"""Batch 45 — final 7 of 50-60 bucket + 18 from 60-70 bucket.

Clears the 50-60 word bucket entirely and begins working the
60-70 word bucket for further polish.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')

EXPANSIONS = {
    # === FINAL 7 OF 50-60 BUCKET ===
    'shekinah-glory': (
        '<p>The <em>Shekinah Glory</em> (from Hebrew <em>shakan</em>, "to dwell") names the visible manifestation of YHWH’s dwelling-presence with His covenant people. It appeared as the cloud-and-fire pillar that led Israel through the wilderness (<em>Exodus 13:21-22</em>), the cloud that filled the completed tabernacle so Moses could not enter (<em>Exodus 40:34-35</em>) and Solomon’s temple at its dedication (<em>1 Kings 8:10-11</em>), and the glory between the cherubim of the mercy seat. The glory departed in Ezekiel’s vision (<em>Ezekiel 10-11</em>) as judgment ripened. And it returned in the Word made flesh: <em>"And the Word was made flesh, and dwelt [Greek <em>eskēnōsen</em>, tabernacled] among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth"</em> (<em>John 1:14</em>).</p>'
    ),
    'sing': (
        '<p>To <em>sing</em> is to produce musical sound with the voice in worship of God — and Scripture commands it over fifty times. The Bible begins with the morning stars singing (<em>Job 38:7</em>) at creation; it books a whole song-collection in the middle (the Psalter — Hebrew <em>Tehillim</em>, "Praises"); it records Christ singing the Passover Hallel (<em>Psalms 113-118</em>) with His disciples before going to Gethsemane (<em>Matthew 26:30</em>); and it ends in heaven with the new song of the Lamb (<em>Revelation 5:9; 14:3; 15:3</em>). Paul commands the church: <em>"Speaking to yourselves in psalms and hymns and spiritual songs, singing and making melody in your heart to the Lord"</em> (<em>Ephesians 5:19</em>). Christian men must sing — gladly, lustily, and out loud.</p>'
    ),
    'treasure-store': (
        '<p>Treasure store is the accumulated wealth or stored value — material or moral — that one has laid up over time. Christ’s sharpest teaching on it is the Sermon on the Mount: <em>"Lay not up for yourselves treasures upon earth, where moth and rust doth corrupt, and where thieves break through and steal: But lay up for yourselves treasures in heaven, where neither moth nor rust doth corrupt, and where thieves do not break through nor steal: For where your treasure is, there will your heart be also"</em> (<em>Matthew 6:19-21</em>). The store is real; the question is <em>where</em> it is laid up. The heart, He says, follows the store. The Christian audits his treasure-store regularly: more in heaven than in this world.</p>'
    ),
    'uttermost-parts': (
        '<p>The "uttermost parts" are the farthest reaches of the earth, of the sea, of the morning. Scripture uses the phrase to insist that no place is too distant for God’s presence, the gospel’s reach, or even the sinner’s flight from God’s hand. <em>"If I take the wings of the morning, and dwell in the uttermost parts of the sea; Even there shall thy hand lead me, and thy right hand shall hold me"</em> (<em>Psalm 139:9-10</em>); <em>"Yet from thence will I gather them"</em> (<em>Nehemiah 1:9</em>). Christ’s ascension commission makes the missionary geography explicit: <em>"But ye shall receive power, after that the Holy Ghost is come upon you: and ye shall be witnesses unto me both in Jerusalem, and in all Judaea, and in Samaria, and unto the uttermost part of the earth"</em> (<em>Acts 1:8</em>).</p>'
    ),
    'validation': (
        '<p>Validation is the establishment that something is genuine — and Scripture’s sense differs sharply from the therapy-culture meaning now dominant. Modern usage often centers on <em>emotional approval</em> ("I need validation"); Scripture centers it on God’s <em>establishment of His word</em> and His people. <em>"For verily I say unto you, Till heaven and earth pass, one jot or one tittle shall in no wise pass from the law, till all be fulfilled"</em> (<em>Matthew 5:18</em>) — every word stands. <em>"Moreover whom he did predestinate, them he also called: and whom he called, them he also justified: and whom he justified, them he also glorified"</em> (<em>Romans 8:30</em>) — each link holds. The saint’s deepest validation is God’s verdict over him, not the world’s approval.</p>'
    ),
    'wonder': (
        '<p>Wonder is astonishment at what is greater than the observer — and in Scripture it is the disposition proper to creatures contemplating the works and Person of God. The LORD declares Himself <em>"wonderful"</em> in His name (<em>"His name shall be called Wonderful"</em>, <em>Isaiah 9:6</em>) and in His works (<em>"Marvellous things did he in the sight of their fathers"</em>, <em>Psalm 78:12</em>). Wonder is the right response: <em>"Stand still, and consider the wondrous works of God"</em> (<em>Job 37:14</em>); <em>"O the depth of the riches both of the wisdom and knowledge of God! how unsearchable are his judgments"</em> (<em>Romans 11:33</em>). Modern Western Christianity has often lost wonder to mere familiarity. Recover it. Stand outside on a clear night and look up.</p>'
    ),
    'work-cursed-blessed': (
        '<p>Work is both cursed and blessed in Scripture. It is <em>blessed</em> as the original calling of Adam in unfallen creation: <em>"And the LORD God took the man, and put him into the garden of Eden to dress it and to keep it"</em> (<em>Genesis 2:15</em>). Work pre-dates the fall — it is part of being human, not part of being broken. It is <em>cursed</em> in its soil and texture after the fall: <em>"cursed is the ground for thy sake; in sorrow shalt thou eat of it... Thorns also and thistles shall it bring forth to thee... In the sweat of thy face shalt thou eat bread"</em> (<em>Genesis 3:17-19</em>). The redemption in Christ does not yet remove the curse from the soil but begins to redeem the worker. The new creation will finish what grace has begun.</p>'
    ),

    # === FIRST 18 OF 60-70 BUCKET ===
    'anna': (
        '<p>Anna was a prophetess of the tribe of Asher, daughter of Phanuel — <em>"a widow of about fourscore and four years, which departed not from the temple, but served God with fastings and prayers night and day"</em> (<em>Luke 2:37</em>). She had been married seven years before her husband died, and now lived in the temple precincts, an aged Spirit-filled intercessor. At Christ’s presentation by Joseph and Mary on the fortieth day, she <em>"coming in that instant gave thanks likewise unto the Lord, and spake of him to all them that looked for redemption in Jerusalem"</em> (<em>2:38</em>). Anna is a luminous picture of late-life faithfulness: decades of fasting and prayer kept her ready for the one moment.</p>'
    ),
    'anointing-oil': (
        '<p>The holy anointing oil was prepared by the Mosaic recipe of <em>"pure myrrh five hundred shekels, and of sweet cinnamon half so much... and of sweet calamus two hundred and fifty shekels, And of cassia five hundred shekels... and of oil olive an hin"</em> (<em>Exodus 30:23-25</em>). It was used to consecrate priests, kings, and the tabernacle and temple furnishings — setting them apart for sacred service. The Hebrew <em>mashach</em> ("to anoint") gives us <em>mashiach</em> ("anointed one, Messiah"); the Greek <em>chriō</em> gives us <em>Christos</em>. Christ is therefore the Anointed One — anointed not with literal oil but with the Holy Spirit at His baptism (<em>Acts 10:38</em>). Every believer shares in His anointing (<em>1 John 2:20, 27</em>).</p>'
    ),
    'be-strong': (
        '<p>"Be strong" is the divine command to take courageous strength — given as preparation for the conquest of Canaan and repeated as the perpetual call to spiritual warfare. The LORD spoke it to Joshua three times in a single chapter: <em>"Be strong and of a good courage... Only be thou strong and very courageous... Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the LORD thy God is with thee whithersoever thou goest"</em> (<em>Joshua 1:6, 7, 9</em>). Strength in Scripture is rarely raw; it is courage rooted in God’s presence and command. Paul echoes the call: <em>"Watch ye, stand fast in the faith, quit you like men, be strong"</em> (<em>1 Corinthians 16:13</em>; cf. <em>Ephesians 6:10</em>).</p>'
    ),
    'belt-truth': (
        '<p>The belt of truth is the first piece of the whole armor of God in <em>Ephesians 6:14</em>: <em>"Stand therefore, having your loins girt about with truth."</em> The Roman soldier’s leather belt (<em>cingulum</em>) was the foundational garment of his combat dress — it gathered the long tunic at the waist, suspended the scabbard, kept the breastplate from shifting, and left the legs free for vigorous combat. Without the belt, every other piece was unstable. Truth functions exactly the same way for the believer: the foundational, gathering, stabilizing reality that makes every other piece of Christian armor work. Lies and self-deception leave the soldier’s armor flapping loose. Christian men gird truth on first every morning. The other pieces hang on this one.</p>'
    ),
    'biblical-theology-method': (
        '<p>Biblical Theology (as a method) is the discipline that traces the unfolding of biblical themes — covenant, kingdom, temple, priesthood, sacrifice, exodus, exile-and-return, Spirit, son-of-Man, bride — through the canon’s redemptive-historical storyline. It reads Scripture <em>diachronically</em> (across time), tracing how each theme develops from Genesis to Revelation and climaxes in Christ. It is distinct from Systematic Theology (which gathers all biblical teaching under doctrinal categories — God, man, sin, salvation, last things) but complements it. Modern foundational figures include Geerhardus Vos, Edmund Clowney, Graeme Goldsworthy, D. A. Carson, and Sidney Greidanus. <em>"And beginning at Moses and all the prophets, he expounded unto them in all the scriptures the things concerning himself"</em> (<em>Luke 24:27</em>) is the method’s charter.</p>'
    ),
    'bull': (
        '<p>The bull is an adult male bovine — and in Levitical sacrifice, the costliest clean animal. The bull was offered as a sin offering for the high priest (<em>Leviticus 4:3-12</em>), for the congregation when the whole assembly sinned (<em>4:13-21</em>), in the priestly dedication ceremony (<em>Exodus 29:1, 10-14</em>), and in major covenant rites (<em>Exodus 24:5</em>). David offered bulls when the ark came to Jerusalem (<em>2 Samuel 6:13</em>). Solomon offered <em>twenty-two thousand</em> bulls at the temple dedication (<em>1 Kings 8:63</em>). Yet Hebrews makes the limit plain: <em>"it is not possible that the blood of bulls and of goats should take away sins"</em> (<em>Hebrews 10:4</em>). Christ’s sacrifice does what the blood of bulls could only foreshadow.</p>'
    ),
    'chain-of-command': (
        '<p>The chain of command is the ordered structure through which authority is delegated downward and accountability flows upward. The Roman centurion in <em>Matthew 8:5-13</em> understood it perfectly: <em>"For I am a man under authority, having soldiers under me: and I say to this man, Go, and he goeth; and to another, Come, and he cometh; and to my servant, Do this, and he doeth it."</em> He grasped Christ’s authority because he understood his own — he was a man under authority and over it at the same time. Christ marveled and said He had not found such great faith in all Israel. Scripture honors the chain of command throughout: <em>"Let every soul be subject unto the higher powers... the powers that be are ordained of God"</em> (<em>Romans 13:1</em>). Authority flows from God down.</p>'
    ),
    'chant': (
        '<p>Chant is the simple, sustained, often unaccompanied singing of Scripture or liturgical text — older than Western music, and the historic vehicle of public Bible-reading. The Levites chanted the Psalms in the temple courts under appointed musical leadership (<em>1 Chronicles 16:4-7; 25:1-7</em>); the synagogue continues to chant the Torah lection; the early church inherited and developed Gregorian chant, Byzantine chant, and many other plainsong traditions. <em>"And the Levites... stood up and praised the LORD God of Israel with a loud voice on high"</em> (<em>2 Chronicles 20:19</em>). Chant slows the words enough that the congregation actually hears them — the text rides the melody into memory. Many Reformed traditions retain chanted Psalms and canticles to this day.</p>'
    ),
    'covenant-meal': (
        '<p>A covenant meal is the meal that ratifies, remembers, or renews a covenant — and Scripture is full of them. Abraham and Abimelech ate together at Beer-sheba after making covenant (<em>Genesis 21:27-32</em>). Isaac and Abimelech repeated the pattern (<em>Genesis 26:30</em>). Jacob and Laban ate on the cairn at Mizpah (<em>Genesis 31:54</em>). The elders of Israel ate with the LORD on Sinai after the covenant blood: <em>"Also they saw God, and did eat and drink"</em> (<em>Exodus 24:11</em>). The Last Supper of Christ with His disciples instituted the New Covenant meal: <em>"This cup is the new testament in my blood, which is shed for you"</em> (<em>Luke 22:20</em>). The Lord’s Supper renews it weekly. Every meal you take with another saint is a small covenant meal.</p>'
    ),
    'daniel-prophet': (
        '<p>Daniel was a young Hebrew of royal or noble blood taken captive to Babylon in the first deportation (c. 605 BC). He rose to high office under four successive empires — Nebuchadnezzar, Belshazzar, Darius the Mede, and Cyrus the Persian — without ever compromising his covenant faith. He refused to defile himself with the king’s food (<em>Daniel 1</em>); he prayed three times daily with windows open toward Jerusalem even under death-decree (<em>6:10</em>); he interpreted Nebuchadnezzar’s dream of the great image and the writing on Belshazzar’s wall; he saw apocalyptic visions of four beasts, the Ancient of Days, the Son of Man, and the seventy weeks. <em>"Daniel was preferred above the presidents... because an excellent spirit was in him"</em> (<em>6:3</em>). His character was his platform.</p>'
    ),
    'dominion-mandate': (
        '<p>The Dominion Mandate is God’s original commission to humanity in <em>Genesis 1:28</em>: <em>"Be fruitful, and multiply, and replenish the earth, and subdue it: and have dominion over the fish of the sea, and over the fowl of the air, and over every living thing that moveth upon the earth."</em> This is not a license for exploitation but a commission for stewardship under God. <em>Psalm 8:5-6</em> celebrates: <em>"For thou hast made him a little lower than the angels, and hast crowned him with glory and honour. Thou madest him to have dominion over the works of thy hands."</em> Dominion is exercised rightly when conformed to God’s character — fruitfully, multiplicatively, productively, with care for what is ruled. The mandate is renewed to Noah (<em>9:1-7</em>) and fulfilled finally in Christ.</p>'
    ),
    'easter': (
        '<p>Easter celebrates the central event of the Christian faith: Christ’s bodily resurrection on the third day after His crucifixion. <em>"For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures"</em> (<em>1 Corinthians 15:3-4</em>). Paul declares the stakes: <em>"And if Christ be not raised, your faith is vain; ye are yet in your sins"</em> (<em>15:17</em>). The resurrection is a historical event, not a metaphor — witnessed by over 500 people (<em>15:6</em>), preached publicly in the very city of the empty tomb seven weeks later, and confessed in the Apostles’ Creed. Every Lord’s Day rehearses it; Easter celebrates it annually.</p>'
    ),
    'eli-priest': (
        '<p>Eli was the high priest at Shiloh during Samuel’s childhood (c. 1100 BC) — honest with Hannah when she prayed silently for a son (<em>1 Samuel 1:17</em>), kind to young Samuel in the tabernacle, and personally faithful in his old age. But he catastrophically failed to discipline his wicked sons Hophni and Phinehas, who treated the priestly offerings with contempt and slept with the women who came to worship (<em>2:12-17, 22</em>). The LORD warned Eli through both an anonymous man of God (<em>2:27-36</em>) and the boy Samuel (<em>3:11-14</em>); Eli did not act. Both sons died at the Philistine battle of Aphek; the ark was captured; Eli fell backward from his judgment-seat and broke his neck (<em>4:18</em>). His failure was paternal more than priestly.</p>'
    ),
    'emmanuel': (
        '<p><em>Emmanuel</em> (or <em>Immanuel</em>, Hebrew <em>Immanu El</em>) is the Messianic name prophesied by Isaiah to wavering King Ahaz: <em>"Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel"</em> (<em>Isaiah 7:14</em>). Matthew explicitly applies it to the conception of Christ: <em>"Now all this was done, that it might be fulfilled which was spoken of the Lord by the prophet, saying, Behold, a virgin shall be with child, and shall bring forth a son, and they shall call his name Emmanuel, which being interpreted is, God with us"</em> (<em>Matthew 1:22-23</em>). The name combines deity (<em>El</em>, God) with covenantal presence (<em>Immanu</em>, with us). Christ is therefore God Himself in the flesh, dwelling among His people.</p>'
    ),
    'enthusiasm': (
        '<p>Enthusiasm — from Greek <em>en theos</em>, "in God" — originally meant "inspired by a god." Modern usage has flattened it to "eager interest." Scripture commends genuine zeal while warning against zeal without knowledge. Paul testifies of Israel: <em>"For I bear them record that they have a zeal of God, but not according to knowledge"</em> (<em>Romans 10:2</em>). True biblical enthusiasm is Spirit-empowered zeal directed by truth: <em>"Not slothful in business; fervent in spirit; serving the Lord"</em> (<em>Romans 12:11</em>). Christ Himself was consumed: <em>"The zeal of thine house hath eaten me up"</em> (<em>John 2:17</em>). The corruption is religious enthusiasm untethered from Scripture — heat without light, feeling without truth. The Christian wants both fire <em>and</em> light.</p>'
    ),
    'faithful-true-witness': (
        '<p>"The Faithful and True" is Christ’s recurring title across Revelation. <em>"And unto the angel of the church of the Laodiceans write; These things saith the Amen, the faithful and true witness, the beginning of the creation of God"</em> (<em>Revelation 3:14</em>) — opening the letter to lukewarm Laodicea. <em>"And I saw heaven opened, and behold a white horse; and he that sat upon him was called Faithful and True, and in righteousness he doth judge and make war"</em> (<em>Revelation 19:11</em>) — the rider returning in glory. The two titles bracket Christ’s character across the present church-age and into the consummation: His witness is faithful (the testimony does not change) and true (the testimony corresponds to reality). The Christian trusts His word absolutely.</p>'
    ),
    'forty': (
        '<p>Forty is the recurring biblical duration of testing, probation, and preparation. The flood-rains fell forty days and nights (<em>Genesis 7:12</em>). Moses fasted forty days on Sinai (<em>Exodus 24:18; 34:28</em>). The spies surveyed Canaan forty days (<em>Numbers 13:25</em>). Israel wandered the wilderness forty years (<em>Deuteronomy 8:2</em>). Goliath challenged Israel forty days morning and evening (<em>1 Samuel 17:16</em>). Elijah journeyed forty days to Horeb (<em>1 Kings 19:8</em>). Jonah preached forty days to Nineveh (<em>Jonah 3:4</em>). Christ fasted forty days in the wilderness (<em>Matthew 4:2</em>) and remained forty days on earth after the resurrection before ascending (<em>Acts 1:3</em>). Where you see forty in Scripture, expect testing — and on the far side, advance.</p>'
    ),
    'foxy': (
        '<p>"Foxy" is the Boomer-era adjective for an attractive woman — era-stamped 1960s and 70s mainstream vocabulary (<em>"that’s one foxy lady"</em>). The slang’s framing is largely physical: "foxy" names visible appearance with no comment on character. The Christian observation: physical attraction is real and good in its biblical place — <em>"Let her be as the loving hind and pleasant roe; let her breasts satisfy thee at all times; and be thou ravished always with her love"</em> (<em>Proverbs 5:19</em>); the Song of Solomon celebrates bodily beauty within covenant marriage. But Scripture refuses to make appearance the measure: <em>"Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised"</em> (<em>Proverbs 31:30</em>). Foxy describes; God’s metric goes deeper.</p>'
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
