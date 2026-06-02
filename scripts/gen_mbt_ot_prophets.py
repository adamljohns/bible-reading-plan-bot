"""MBT OT landmark passages — Prophets.

Isaiah 6 (13v), Isaiah 9:6-7 (2v), Isaiah 40 (31v),
Isaiah 53 (12v), Isaiah 55 (13v), Jeremiah 29:11-14 (4v),
Daniel 3 (30v), Daniel 6 (28v). 133 verses total.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Isaiah 6 — Isaiah's vision in the temple
isa_6 = {
    1: "In the year of King Uzziah's death I saw the Lord sitting on a throne, lofty and exalted — with the train of His robe filling the temple.",
    2: "Seraphim stood above Him — each having six wings. With two he covered his face, and with two he covered his feet, and with two he flew.",
    3: "And one called out to another and said, \"Holy, holy, holy is the LORD of hosts — the whole earth is full of His glory.\"",
    4: "And the foundations of the thresholds trembled at the voice of him who called out — while the temple was filling with smoke.",
    5: "Then I said, \"Woe is me, for I am ruined! Because I am a man of unclean lips, and I live among a people of unclean lips. For my eyes have seen the King, the LORD of hosts!\"",
    6: "Then one of the seraphim flew to me with a burning coal in his hand, which he had taken from the altar with tongs.",
    7: "And he touched my mouth with it, and said, \"Behold, this has touched your lips — and your iniquity is taken away, and your sin is forgiven.\"",
    8: "Then I heard the voice of the Lord, saying, \"Whom shall I send, and who will go for Us?\" Then I said, \"Here am I — send me!\"",
    9: "And He said, \"Go, and tell this people: 'Keep on listening, but do not perceive — keep on looking, but do not understand.'",
    10: "Render the hearts of this people insensitive — their ears dull, and their eyes dim. Lest they see with their eyes, hear with their ears, understand with their hearts, and return and be healed.\"",
    11: "Then I said, \"Lord, how long?\" And He answered, \"Until cities are devastated and without inhabitant, and houses are without people, and the land is utterly desolate.",
    12: "And the LORD has removed men far away — and the forsaken places are many in the midst of the land.",
    13: "Yet there will be a tenth portion in it — and it will again be subject to burning, like a terebinth or an oak whose stump remains when it is felled. The holy seed is its stump.\"",
}

# Isaiah 9:6-7 — For unto us a Child is born
isa_9 = {
    6: "For a Child will be born to us, a Son will be given to us — and the government will rest on His shoulders. And His name will be called Wonderful Counselor, Mighty God, Eternal Father, Prince of Peace.",
    7: "There will be no end to the increase of His government or of peace — on the throne of David and over his kingdom, to establish it and to uphold it with justice and righteousness from then on and forevermore. The zeal of the LORD of hosts will accomplish this.",
}

# Isaiah 40 — Comfort, comfort My people
isa_40 = {
    1: "\"Comfort, O comfort My people,\" says your God.",
    2: "\"Speak kindly to Jerusalem — and call out to her, that her warfare has ended, that her iniquity has been removed, that she has received of the LORD's hand double for all her sins.\"",
    3: "A voice is calling: \"Clear the way for the LORD in the wilderness — make smooth in the desert a highway for our God.",
    4: "Let every valley be lifted up, and every mountain and hill be made low — and let the rough ground become a plain, and the rugged terrain a broad valley.",
    5: "Then the glory of the LORD will be revealed, and all flesh will see it together — for the mouth of the LORD has spoken.\"",
    6: "A voice says, \"Call out!\" Then he answered, \"What shall I call out?\" \"All flesh is grass, and all its loveliness is like the flower of the field.",
    7: "The grass withers, the flower fades, when the breath of the LORD blows upon it — surely the people are grass.",
    8: "The grass withers, the flower fades — but the word of our God stands forever.\"",
    9: "Get yourself up on a high mountain, O Zion, bearer of good news. Lift up your voice mightily, O Jerusalem, bearer of good news — lift it up, do not fear. Say to the cities of Judah, \"Behold your God!\"",
    10: "Behold, the Lord GOD will come with might, with His arm ruling for Him. Behold, His reward is with Him, and His recompense before Him.",
    11: "Like a shepherd He will tend His flock — in His arm He will gather the lambs, and carry them in His bosom. He will gently lead the nursing ewes.",
    12: "Who has measured the waters in the hollow of His hand, and marked off the heavens by the span — and calculated the dust of the earth by the measure, and weighed the mountains in a balance, and the hills in a pair of scales?",
    13: "Who has directed the Spirit of the LORD — or as His counselor has informed Him?",
    14: "With whom did He consult and who gave Him understanding? And who taught Him in the path of justice and taught Him knowledge, and informed Him of the way of understanding?",
    15: "Behold, the nations are like a drop from a bucket, and are regarded as a speck of dust on the scales — behold, He lifts up the islands like fine dust.",
    16: "Even Lebanon is not enough to burn — nor its beasts enough for a burnt offering.",
    17: "All the nations are as nothing before Him — they are regarded by Him as less than nothing and meaningless.",
    18: "To whom then will you liken God? Or what likeness will you compare with Him?",
    19: "As for the idol, a craftsman casts it — a goldsmith plates it with gold, and a silversmith fashions chains of silver.",
    20: "He who is too impoverished for such an offering selects a tree that does not rot — he seeks out for himself a skillful craftsman to prepare an idol that will not totter.",
    21: "Do you not know? Have you not heard? Has it not been declared to you from the beginning? Have you not understood from the foundations of the earth?",
    22: "It is He who sits above the circle of the earth — and its inhabitants are like grasshoppers. Who stretches out the heavens like a curtain, and spreads them out like a tent to dwell in.",
    23: "He it is who reduces rulers to nothing — who makes the judges of the earth meaningless.",
    24: "Scarcely have they been planted, scarcely have they been sown, scarcely has their stock taken root in the earth — but He merely blows on them, and they wither, and the storm carries them away like stubble.",
    25: "\"To whom then will you liken Me, that I should be his equal?\" says the Holy One.",
    26: "Lift up your eyes on high and see who has created these stars — the One who leads forth their host by number. He calls them all by name — because of the greatness of His might and the strength of His power, not one of them is missing.",
    27: "Why do you say, O Jacob, and assert, O Israel, \"My way is hidden from the LORD, and the justice due me escapes the notice of my God\"?",
    28: "Do you not know? Have you not heard? The Everlasting God, the LORD, the Creator of the ends of the earth, does not become weary or tired. His understanding is inscrutable.",
    29: "He gives strength to the weary, and to him who lacks might He increases power.",
    30: "Though youths grow weary and tired, and vigorous young men stumble badly —",
    31: "yet those who wait for the LORD will gain new strength. They will mount up with wings like eagles — they will run, and not get tired. They will walk, and not become weary.",
}

# Isaiah 53 — The Suffering Servant
isa_53 = {
    1: "Who has believed our message? And to whom has the arm of the LORD been revealed?",
    2: "For He grew up before Him like a tender shoot — and like a root out of parched ground. He has no stately form or majesty that we should look upon Him — nor appearance that we should be attracted to Him.",
    3: "He was despised and forsaken of men — a man of sorrows and acquainted with grief. And like one from whom men hide their face, He was despised — and we did not esteem Him.",
    4: "Surely our griefs He Himself bore, and our sorrows He carried — yet we ourselves esteemed Him stricken, smitten of God, and afflicted.",
    5: "But He was pierced through for our transgressions — He was crushed for our iniquities. The chastening for our well-being fell upon Him — and by His scourging we are healed.",
    6: "All of us like sheep have gone astray — each of us has turned to his own way. But the LORD has caused the iniquity of us all to fall on Him.",
    7: "He was oppressed and He was afflicted — yet He did not open His mouth. Like a lamb that is led to slaughter, and like a sheep that is silent before its shearers, so He did not open His mouth.",
    8: "By oppression and judgment He was taken away — and as for His generation, who considered that He was cut off out of the land of the living for the transgression of my people, to whom the stroke was due?",
    9: "His grave was assigned with wicked men — yet He was with a rich man in His death, because He had done no violence, nor was there any deceit in His mouth.",
    10: "But the LORD was pleased to crush Him, putting Him to grief — if He would render Himself as a guilt offering, He will see His offspring. He will prolong His days, and the good pleasure of the LORD will prosper in His hand.",
    11: "As a result of the anguish of His soul, He will see it and be satisfied. By His knowledge the Righteous One, My Servant, will justify the many — as He will bear their iniquities.",
    12: "Therefore I will allot Him a portion with the great — and He will divide the booty with the strong. Because He poured out Himself to death, and was numbered with the transgressors — yet He Himself bore the sin of many, and interceded for the transgressors.",
}

# Isaiah 55 — Come, every one who thirsts
isa_55 = {
    1: "\"Ho! Every one who thirsts, come to the waters — and you who have no money come, buy and eat. Come, buy wine and milk without money and without cost.",
    2: "Why do you spend money for what is not bread, and your wages for what does not satisfy? Listen carefully to Me, and eat what is good — and delight yourself in abundance.",
    3: "Incline your ear and come to Me. Listen, that you may live — and I will make an everlasting covenant with you, according to the faithful mercies shown to David.",
    4: "Behold, I have made him a witness to the peoples, a leader and commander for the peoples.",
    5: "Behold, you will call a nation you do not know, and a nation which knows you not will run to you — because of the LORD your God, even the Holy One of Israel, for He has glorified you.\"",
    6: "Seek the LORD while He may be found — call upon Him while He is near.",
    7: "Let the wicked forsake his way, and the unrighteous man his thoughts — and let him return to the LORD, and He will have compassion on him, and to our God, for He will abundantly pardon.",
    8: "\"For My thoughts are not your thoughts, nor are your ways My ways,\" declares the LORD.",
    9: "\"For as the heavens are higher than the earth, so are My ways higher than your ways, and My thoughts than your thoughts.",
    10: "For as the rain and the snow come down from heaven, and do not return there without watering the earth, and making it bear and sprout — and furnishing seed to the sower and bread to the eater,",
    11: "so will My word be which goes forth from My mouth. It will not return to Me empty — without accomplishing what I desire, and without succeeding in the matter for which I sent it.",
    12: "For you will go out with joy, and be led forth with peace. The mountains and the hills will break forth into shouts of joy before you — and all the trees of the field will clap their hands.",
    13: "Instead of the thorn bush the cypress will come up — and instead of the nettle the myrtle will come up. And it will be a memorial to the LORD, for an everlasting sign which will not be cut off.\"",
}

# Jeremiah 29:11-14 — For I know the plans I have for you
jer_29 = {
    11: "\"For I know the plans that I have for you,\" declares the LORD — \"plans for welfare and not for calamity, to give you a future and a hope.",
    12: "Then you will call upon Me and come and pray to Me — and I will listen to you.",
    13: "And you will seek Me and find Me, when you search for Me with all your heart.",
    14: "And I will be found by you,\" declares the LORD, \"and I will restore your fortunes, and will gather you from all the nations, and from all the places where I have driven you,\" declares the LORD, \"and I will bring you back to the place from where I sent you into exile.\"",
}

# Daniel 3 — The fiery furnace
dan_3 = {
    1: "Nebuchadnezzar the king made an image of gold, the height of which was sixty cubits and its width six cubits. He set it up on the plain of Dura in the province of Babylon.",
    2: "Then Nebuchadnezzar the king sent word to assemble the satraps, the prefects and the governors, the counselors, the treasurers, the judges, the magistrates and all the rulers of the provinces to come to the dedication of the image that Nebuchadnezzar the king had set up.",
    3: "Then the satraps, the prefects and the governors, the counselors, the treasurers, the judges, the magistrates and all the rulers of the provinces were assembled for the dedication of the image — and they stood before the image that Nebuchadnezzar had set up.",
    4: "Then the herald loudly proclaimed, \"To you the command is given, O peoples, nations and men of every language —",
    5: "that at the moment you hear the sound of the horn, flute, lyre, trigon, psaltery, bagpipe and all kinds of music, you are to fall down and worship the golden image that Nebuchadnezzar the king has set up.",
    6: "But whoever does not fall down and worship shall immediately be cast into the midst of a furnace of blazing fire.\"",
    7: "Therefore at that time, when all the peoples heard the sound of the horn, flute, lyre, trigon, psaltery, bagpipe, and all kinds of music, all the peoples, nations and men of every language fell down and worshiped the golden image that Nebuchadnezzar the king had set up.",
    8: "For this reason at that time certain Chaldeans came forward and brought charges against the Jews.",
    9: "They answered and said to Nebuchadnezzar the king, \"O king, live forever!",
    10: "You yourself, O king, have made a decree that every man who hears the sound of the horn, flute, lyre, trigon, psaltery, and bagpipe, and all kinds of music, is to fall down and worship the golden image —",
    11: "but whoever does not fall down and worship shall be cast into the midst of a furnace of blazing fire.",
    12: "There are certain Jews whom you have appointed over the administration of the province of Babylon, namely Shadrach, Meshach and Abed-nego. These men, O king, have disregarded you — they do not serve your gods or worship the golden image which you have set up.\"",
    13: "Then Nebuchadnezzar in rage and anger gave orders to bring Shadrach, Meshach and Abed-nego. Then these men were brought before the king.",
    14: "Nebuchadnezzar responded and said to them, \"Is it true, Shadrach, Meshach and Abed-nego, that you do not serve my gods or worship the golden image that I have set up?",
    15: "Now if you are ready, at the moment you hear the sound of the horn, flute, lyre, trigon, psaltery and bagpipe and all kinds of music, to fall down and worship the image that I have made, very well. But if you do not worship, you will immediately be cast into the midst of a furnace of blazing fire — and what god is there who can deliver you out of my hands?\"",
    16: "Shadrach, Meshach and Abed-nego answered and said to the king, \"O Nebuchadnezzar, we do not need to give you an answer concerning this matter.",
    17: "If it be so, our God whom we serve is able to deliver us from the furnace of blazing fire — and He will deliver us out of your hand, O king.",
    18: "But even if He does not, let it be known to you, O king, that we are not going to serve your gods or worship the golden image that you have set up.\"",
    19: "Then Nebuchadnezzar was filled with wrath, and his facial expression was altered toward Shadrach, Meshach and Abed-nego. He answered by giving orders to heat the furnace seven times more than it was usually heated.",
    20: "And he commanded certain valiant warriors who were in his army to tie up Shadrach, Meshach and Abed-nego in order to cast them into the furnace of blazing fire.",
    21: "Then these men were tied up in their trousers, their coats, their caps and their other clothes, and were cast into the midst of the furnace of blazing fire.",
    22: "For this reason, because the king's command was urgent and the furnace had been made extremely hot, the flame of the fire slew those men who carried up Shadrach, Meshach and Abed-nego.",
    23: "But these three men, Shadrach, Meshach and Abed-nego, fell into the midst of the furnace of blazing fire still tied up.",
    24: "Then Nebuchadnezzar the king was astounded and stood up in haste. He responded and said to his high officials, \"Was it not three men we cast bound into the midst of the fire?\" They answered and said to the king, \"Certainly, O king.\"",
    25: "He answered and said, \"Look — I see four men loosed and walking about in the midst of the fire without harm, and the appearance of the fourth is like a son of the gods!\"",
    26: "Then Nebuchadnezzar came near to the door of the furnace of blazing fire — he responded and said, \"Shadrach, Meshach and Abed-nego, come out, you servants of the Most High God, and come here!\" Then Shadrach, Meshach and Abed-nego came out of the midst of the fire.",
    27: "And the satraps, the prefects, the governors and the king's high officials gathered around and saw in regard to these men that the fire had no effect on the bodies of these men, nor was the hair of their head singed — nor were their trousers damaged, nor had the smell of fire even come upon them.",
    28: "Nebuchadnezzar responded and said, \"Blessed be the God of Shadrach, Meshach and Abed-nego, who has sent His angel and delivered His servants who put their trust in Him, violating the king's command — and yielded up their bodies so as not to serve or worship any god except their own God.",
    29: "Therefore I make a decree that any people, nation or tongue that speaks anything offensive against the God of Shadrach, Meshach and Abed-nego shall be torn limb from limb and their houses reduced to a rubbish heap — inasmuch as there is no other god who is able to deliver in this way.\"",
    30: "Then the king caused Shadrach, Meshach and Abed-nego to prosper in the province of Babylon.",
}

# Daniel 6 — The lions' den
dan_6 = {
    1: "It seemed good to Darius to appoint 120 satraps over the kingdom, that they should be in charge of the whole kingdom,",
    2: "and over them three commissioners (of whom Daniel was one), that these satraps might be accountable to them, and that the king might not suffer loss.",
    3: "Then this Daniel began distinguishing himself among the commissioners and satraps because he possessed an extraordinary spirit, and the king planned to appoint him over the entire kingdom.",
    4: "Then the commissioners and satraps began trying to find a ground of accusation against Daniel in regard to government affairs — but they could find no ground of accusation or evidence of corruption, inasmuch as he was faithful, and no negligence or corruption was to be found in him.",
    5: "Then these men said, \"We will not find any ground of accusation against this Daniel unless we find it against him with regard to the law of his God.\"",
    6: "Then these commissioners and satraps came by agreement to the king and spoke to him as follows: \"King Darius, live forever!",
    7: "All the commissioners of the kingdom, the prefects and the satraps, the high officials and the governors have consulted together that the king should establish a statute and enforce an injunction that anyone who makes a petition to any god or man besides you, O king, for thirty days, shall be cast into the lions' den.",
    8: "Now, O king, establish the injunction and sign the document so that it may not be changed, according to the law of the Medes and Persians, which may not be revoked.\"",
    9: "Therefore King Darius signed the document, that is, the injunction.",
    10: "Now when Daniel knew that the document was signed, he entered his house (now in his roof chamber he had windows open toward Jerusalem). And he continued kneeling on his knees three times a day, praying and giving thanks before his God, as he had been doing previously.",
    11: "Then these men came by agreement and found Daniel making petition and supplication before his God.",
    12: "Then they approached and spoke before the king about the king's injunction, \"Did you not sign an injunction that any man who makes a petition to any god or man besides you, O king, for thirty days, is to be cast into the lions' den?\" The king replied, \"The statement is true, according to the law of the Medes and Persians, which may not be revoked.\"",
    13: "Then they answered and spoke before the king, \"Daniel, who is one of the exiles from Judah, pays no attention to you, O king, or to the injunction which you signed — but keeps making his petition three times a day.\"",
    14: "Then, as soon as the king heard this statement, he was deeply distressed and set his mind on delivering Daniel. And even until sunset he kept exerting himself to rescue him.",
    15: "Then these men came by agreement to the king and said to the king, \"Recognize, O king, that it is a law of the Medes and Persians that no injunction or statute which the king establishes may be changed.\"",
    16: "Then the king gave orders, and Daniel was brought in and cast into the lions' den. The king spoke and said to Daniel, \"Your God whom you constantly serve will Himself deliver you.\"",
    17: "And a stone was brought and laid over the mouth of the den — and the king sealed it with his own signet ring and with the signet rings of his nobles, so that nothing would be changed in regard to Daniel.",
    18: "Then the king went off to his palace and spent the night fasting, and no entertainment was brought before him — and his sleep fled from him.",
    19: "Then the king arose at dawn, at the break of day, and went in haste to the lions' den.",
    20: "And when he had come near the den to Daniel, he cried out with a troubled voice. The king spoke and said to Daniel, \"Daniel, servant of the living God, has your God whom you constantly serve been able to deliver you from the lions?\"",
    21: "Then Daniel spoke to the king, \"O king, live forever!",
    22: "My God sent His angel and shut the lions' mouths, and they have not harmed me — inasmuch as I was found innocent before Him; and also toward you, O king, I have committed no crime.\"",
    23: "Then the king was very pleased and gave orders for Daniel to be taken up out of the den. So Daniel was taken up out of the den, and no injury whatever was found on him, because he had trusted in his God.",
    24: "The king then gave orders, and they brought those men who had maliciously accused Daniel, and they cast them, their children, and their wives into the lions' den — and they had not reached the bottom of the den before the lions overpowered them and crushed all their bones.",
    25: "Then Darius the king wrote to all the peoples, nations, and men of every language who were living in all the land: \"May your peace abound!",
    26: "I make a decree that in all the dominion of my kingdom men are to fear and tremble before the God of Daniel — for He is the living God and enduring forever, and His kingdom is one which will not be destroyed, and His dominion will be forever.",
    27: "He delivers and rescues, and He performs signs and wonders in heaven and on earth — He who has also delivered Daniel from the power of the lions.\"",
    28: "So this Daniel enjoyed success in the reign of Darius and in the reign of Cyrus the Persian.",
}

ENTRIES = {}
for v, t in isa_6.items():   ENTRIES[f"23_6_{v}"] = t
for v, t in isa_9.items():   ENTRIES[f"23_9_{v}"] = t
for v, t in isa_40.items():  ENTRIES[f"23_40_{v}"] = t
for v, t in isa_53.items():  ENTRIES[f"23_53_{v}"] = t
for v, t in isa_55.items():  ENTRIES[f"23_55_{v}"] = t
for v, t in jer_29.items():  ENTRIES[f"24_29_{v}"] = t
for v, t in dan_3.items():   ENTRIES[f"27_3_{v}"] = t
for v, t in dan_6.items():   ENTRIES[f"27_6_{v}"] = t

def main():
    print(f"MBT OT Prophets landmark verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json updated.")

if __name__ == "__main__":
    main()
