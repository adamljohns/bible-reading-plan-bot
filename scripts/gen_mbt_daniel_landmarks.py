"""MBT generator: Daniel landmark chapters.

Book ID 27. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Daniel 1 (21 verses) — the Babylonian training, refusing the king's food
- Daniel 3 (30 verses) — the fiery furnace
- Daniel 6 (28 verses) — the lions' den
- Daniel 9 (27 verses) — Daniel's prayer and the seventy weeks

Total: 106 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Daniel 1 — the boys at Babylon
ch1 = {
    1: "In the third year of the reign of Jehoiakim king of Judah, Nebuchadnezzar king of Babylon came to Jerusalem and besieged it.",
    2: "And the Lord gave Jehoiakim king of Judah into his hand, with some of the articles of the house of God, which he carried into the land of Shinar to the house of his god; and he brought the articles into the treasure house of his god.",
    3: "Then the king instructed Ashpenaz, the master of his eunuchs, to bring some of the children of Israel and some of the king's descendants and some of the nobles,",
    4: "young men in whom there was no blemish, but good-looking, gifted in all wisdom, possessing knowledge and quick to understand, who had ability to serve in the king's palace, and whom they might teach the language and literature of the Chaldeans.",
    5: "And the king appointed for them a daily provision of the king's delicacies and of the wine which he drank, and three years of training for them, so that at the end of that time they might serve before the king.",
    6: "Now from among those of the sons of Judah were Daniel, Hananiah, Mishael, and Azariah.",
    7: "To them the chief of the eunuchs gave names: he gave Daniel the name Belteshazzar; to Hananiah, Shadrach; to Mishael, Meshach; and to Azariah, Abed-Nego.",
    8: "But Daniel purposed in his heart that he would not defile himself with the portion of the king's delicacies, nor with the wine which he drank; therefore he requested of the chief of the eunuchs that he might not defile himself.",
    9: "Now God had brought Daniel into the favor and goodwill of the chief of the eunuchs.",
    10: "And the chief of the eunuchs said to Daniel, \"I fear my lord the king, who has appointed your food and drink. For why should he see your faces looking worse than the young men who are your age? Then you would endanger my head before the king.\"",
    11: "So Daniel said to the steward whom the chief of the eunuchs had set over Daniel, Hananiah, Mishael, and Azariah,",
    12: "\"Please test your servants for ten days, and let them give us vegetables to eat and water to drink.",
    13: "Then let our appearance be examined before you, and the appearance of the young men who eat the portion of the king's delicacies; and as you see fit, so deal with your servants.\"",
    14: "So he consented with them in this matter, and tested them ten days.",
    15: "And at the end of ten days their features appeared better and fatter in flesh than all the young men who ate the portion of the king's delicacies.",
    16: "Thus the steward took away their portion of delicacies and the wine that they were to drink, and gave them vegetables.",
    17: "As for these four young men, God gave them knowledge and skill in all literature and wisdom; and Daniel had understanding in all visions and dreams.",
    18: "Now at the end of the days, when the king had said that they should be brought in, the chief of the eunuchs brought them in before Nebuchadnezzar.",
    19: "Then the king interviewed them, and among them all none was found like Daniel, Hananiah, Mishael, and Azariah; therefore they served before the king.",
    20: "And in all matters of wisdom and understanding about which the king examined them, he found them ten times better than all the magicians and astrologers who were in all his realm.",
    21: "Thus Daniel continued until the first year of King Cyrus.",
}

# Daniel 3 — the fiery furnace
ch3 = {
    1: "Nebuchadnezzar the king made an image of gold, whose height was sixty cubits and its width six cubits. He set it up in the plain of Dura, in the province of Babylon.",
    2: "And King Nebuchadnezzar sent word to gather together the satraps, the administrators, the governors, the counselors, the treasurers, the judges, the magistrates, and all the officials of the provinces, to come to the dedication of the image which King Nebuchadnezzar had set up.",
    3: "So the satraps, the administrators, the governors, the counselors, the treasurers, the judges, the magistrates, and all the officials of the provinces gathered together for the dedication of the image that King Nebuchadnezzar had set up; and they stood before the image that Nebuchadnezzar had set up.",
    4: "Then a herald cried aloud: \"To you it is commanded, O peoples, nations, and languages,",
    5: "that at the time you hear the sound of the horn, flute, harp, lyre, and psaltery, in symphony with all kinds of music, you shall fall down and worship the gold image that King Nebuchadnezzar has set up;",
    6: "and whoever does not fall down and worship shall be cast immediately into the midst of a burning fiery furnace.\"",
    7: "So at that time, when all the people heard the sound of the horn, flute, harp, and lyre, in symphony with all kinds of music, all the peoples, nations, and languages fell down and worshiped the gold image which King Nebuchadnezzar had set up.",
    8: "Therefore at that time certain Chaldeans came forward and accused the Jews.",
    9: "They spoke and said to King Nebuchadnezzar, \"O king, live forever!",
    10: "You, O king, have made a decree that everyone who hears the sound of the horn, flute, harp, lyre, and psaltery, in symphony with all kinds of music, shall fall down and worship the gold image;",
    11: "and whoever does not fall down and worship shall be cast into the midst of a burning fiery furnace.",
    12: "There are certain Jews whom you have set over the affairs of the province of Babylon: Shadrach, Meshach, and Abed-Nego; these men, O king, have not regarded you. They do not serve your gods or worship the gold image which you have set up.\"",
    13: "Then Nebuchadnezzar, in rage and fury, gave the command to bring Shadrach, Meshach, and Abed-Nego. So they brought these men before the king.",
    14: "Nebuchadnezzar spoke, saying to them, \"Is it true, Shadrach, Meshach, and Abed-Nego, that you do not serve my gods or worship the gold image which I have set up?",
    15: "Now if you are ready at the time you hear the sound of the horn, flute, harp, lyre, and psaltery, in symphony with all kinds of music, and you fall down and worship the image which I have made, good! But if you do not worship, you shall be cast immediately into the midst of a burning fiery furnace. And who is the god who will deliver you from my hands?\"",
    16: "Shadrach, Meshach, and Abed-Nego answered and said to the king, \"O Nebuchadnezzar, we have no need to answer you in this matter.",
    17: "If that is the case, our God whom we serve is able to deliver us from the burning fiery furnace, and He will deliver us from your hand, O king.",
    18: "But if not, let it be known to you, O king, that we do not serve your gods, nor will we worship the gold image which you have set up.\"",
    19: "Then Nebuchadnezzar was full of fury, and the expression on his face changed toward Shadrach, Meshach, and Abed-Nego. He spoke and commanded that they heat the furnace seven times more than it was usually heated.",
    20: "And he commanded certain mighty men of valor who were in his army to bind Shadrach, Meshach, and Abed-Nego, and cast them into the burning fiery furnace.",
    21: "Then these men were bound in their coats, their trousers, their turbans, and their other garments, and were cast into the midst of the burning fiery furnace.",
    22: "Therefore, because the king's command was urgent, and the furnace exceedingly hot, the flame of the fire killed those men who took up Shadrach, Meshach, and Abed-Nego.",
    23: "And these three men, Shadrach, Meshach, and Abed-Nego, fell down bound into the midst of the burning fiery furnace.",
    24: "Then King Nebuchadnezzar was astonished; and he rose in haste and spoke, saying to his counselors, \"Did we not cast three men bound into the midst of the fire?\" They answered and said to the king, \"True, O king.\"",
    25: "\"Look!\" he answered, \"I see four men loose, walking in the midst of the fire; and they are not hurt, and the form of the fourth is like the Son of God.\"",
    26: "Then Nebuchadnezzar went near the mouth of the burning fiery furnace and spoke, saying, \"Shadrach, Meshach, and Abed-Nego, servants of the Most High God, come out, and come here.\" Then Shadrach, Meshach, and Abed-Nego came from the midst of the fire.",
    27: "And the satraps, administrators, governors, and the king's counselors gathered together, and they saw these men on whose bodies the fire had no power; the hair of their head was not singed nor were their garments affected, and the smell of fire was not on them.",
    28: "Nebuchadnezzar spoke, saying, \"Blessed be the God of Shadrach, Meshach, and Abed-Nego, who sent His Angel and delivered His servants who trusted in Him, and they have frustrated the king's word, and yielded their bodies, that they should not serve nor worship any god except their own God!",
    29: "Therefore I make a decree that any people, nation, or language which speaks anything amiss against the God of Shadrach, Meshach, and Abed-Nego shall be cut in pieces, and their houses shall be made an ash heap; because there is no other God who can deliver like this.\"",
    30: "Then the king promoted Shadrach, Meshach, and Abed-Nego in the province of Babylon.",
}

# Daniel 6 — the lions' den
ch6 = {
    1: "It pleased Darius to set over the kingdom one hundred and twenty satraps, to be over the whole kingdom;",
    2: "and over these, three governors, of whom Daniel was one, that the satraps might give account to them, so that the king would suffer no loss.",
    3: "Then this Daniel distinguished himself above the governors and satraps, because an excellent spirit was in him; and the king gave thought to setting him over the whole realm.",
    4: "So the governors and satraps sought to find some charge against Daniel concerning the kingdom; but they could find no charge or fault, because he was faithful; nor was there any error or fault found in him.",
    5: "Then these men said, \"We shall not find any charge against this Daniel unless we find it against him concerning the law of his God.\"",
    6: "So these governors and satraps thronged before the king, and said thus to him: \"King Darius, live forever!",
    7: "All the governors of the kingdom, the administrators and satraps, the counselors and advisors, have consulted together to establish a royal statute and to make a firm decree, that whoever petitions any god or man for thirty days, except you, O king, shall be cast into the den of lions.",
    8: "Now, O king, establish the decree and sign the writing, so that it cannot be changed, according to the law of the Medes and Persians, which does not alter.\"",
    9: "Therefore King Darius signed the written decree.",
    10: "Now when Daniel knew that the writing was signed, he went home. And in his upper room, with his windows open toward Jerusalem, he knelt down on his knees three times that day, and prayed and gave thanks before his God, as was his custom since early days.",
    11: "Then these men assembled and found Daniel praying and making supplication before his God.",
    12: "And they went before the king, and spoke concerning the king's decree: \"Have you not signed a decree that every man who petitions any god or man within thirty days, except you, O king, shall be cast into the den of lions?\" The king answered and said, \"The thing is true, according to the law of the Medes and Persians, which does not alter.\"",
    13: "So they answered and said before the king, \"That Daniel, who is one of the captives from Judah, does not show due regard for you, O king, or for the decree that you have signed, but makes his petition three times a day.\"",
    14: "And the king, when he heard these words, was greatly displeased with himself, and set his heart on Daniel to deliver him; and he labored till the going down of the sun to deliver him.",
    15: "Then these men approached the king, and said to the king, \"Know, O king, that it is the law of the Medes and Persians that no decree or statute which the king establishes may be changed.\"",
    16: "So the king gave the command, and they brought Daniel and cast him into the den of lions. But the king spoke, saying to Daniel, \"Your God, whom you serve continually, He will deliver you.\"",
    17: "Then a stone was brought and laid on the mouth of the den, and the king sealed it with his own signet ring and with the signets of his lords, that the purpose concerning Daniel might not be changed.",
    18: "Now the king went to his palace and spent the night fasting; and no musicians were brought before him. Also his sleep went from him.",
    19: "Then the king arose very early in the morning and went in haste to the den of lions.",
    20: "And when he came to the den, he cried out with a lamenting voice to Daniel. The king spoke, saying to Daniel, \"Daniel, servant of the living God, has your God, whom you serve continually, been able to deliver you from the lions?\"",
    21: "Then Daniel said to the king, \"O king, live forever!",
    22: "My God sent His angel and shut the lions' mouths, so that they have not hurt me, because I was found innocent before Him; and also, O king, I have done no wrong before you.\"",
    23: "Now the king was exceedingly glad for him, and commanded that they should take Daniel up out of the den. So Daniel was taken up out of the den, and no injury whatever was found on him, because he believed in his God.",
    24: "And the king gave the command, and they brought those men who had accused Daniel, and they cast them into the den of lions — them, their children, and their wives; and the lions overpowered them, and broke all their bones in pieces before they ever came to the bottom of the den.",
    25: "Then King Darius wrote: \"To all peoples, nations, and languages that dwell in all the earth: Peace be multiplied to you.",
    26: "I make a decree that in every dominion of my kingdom men must tremble and fear before the God of Daniel. For He is the living God, and steadfast forever; His kingdom is the one which shall not be destroyed, and His dominion shall endure to the end.",
    27: "He delivers and rescues, and He works signs and wonders in heaven and on earth, who has delivered Daniel from the power of the lions.\"",
    28: "So this Daniel prospered in the reign of Darius and in the reign of Cyrus the Persian.",
}

# Daniel 9 — Daniel's prayer + the Seventy Weeks
ch9 = {
    1: "In the first year of Darius the son of Ahasuerus, of the lineage of the Medes, who was made king over the realm of the Chaldeans —",
    2: "in the first year of his reign I, Daniel, understood by the books the number of the years specified by the word of the LORD, given through Jeremiah the prophet, that He would accomplish seventy years in the desolations of Jerusalem.",
    3: "Then I set my face toward the Lord God to make request by prayer and supplications, with fasting, sackcloth, and ashes.",
    4: "And I prayed to the LORD my God, and made confession, and said, \"O Lord, great and awesome God, who keeps His covenant and mercy with those who love Him, and with those who keep His commandments,",
    5: "we have sinned and committed iniquity, we have done wickedly and rebelled, even by departing from Your precepts and Your judgments.",
    6: "Neither have we heeded Your servants the prophets, who spoke in Your name to our kings and our princes, to our fathers and all the people of the land.",
    7: "O Lord, righteousness belongs to You, but to us shame of face, as it is this day — to the men of Judah, to the inhabitants of Jerusalem and all Israel, those near and those far off in all the countries to which You have driven them, because of the unfaithfulness which they have committed against You.",
    8: "O Lord, to us belongs shame of face, to our kings, our princes, and our fathers, because we have sinned against You.",
    9: "To the Lord our God belong mercy and forgiveness, though we have rebelled against Him.",
    10: "We have not obeyed the voice of the LORD our God, to walk in His laws, which He set before us by His servants the prophets.",
    11: "Yes, all Israel has transgressed Your law, and has departed so as not to obey Your voice; therefore the curse and the oath written in the Law of Moses the servant of God have been poured out on us, because we have sinned against Him.",
    12: "And He has confirmed His words, which He spoke against us and against our judges who judged us, by bringing upon us a great disaster; for under the whole heaven such has never been done as what has been done to Jerusalem.",
    13: "As it is written in the Law of Moses, all this disaster has come upon us; yet we have not made our prayer before the LORD our God, that we might turn from our iniquities and understand Your truth.",
    14: "Therefore the LORD has kept the disaster in mind, and brought it upon us; for the LORD our God is righteous in all the works which He does, though we have not obeyed His voice.",
    15: "And now, O Lord our God, who brought Your people out of the land of Egypt with a mighty hand, and made Yourself a name, as it is this day — we have sinned, we have done wickedly!",
    16: "O Lord, according to all Your righteousness, I pray, let Your anger and Your fury be turned away from Your city Jerusalem, Your holy mountain; because for our sins, and for the iniquities of our fathers, Jerusalem and Your people are a reproach to all those around us.",
    17: "Now therefore, our God, hear the prayer of Your servant, and his supplications, and for the Lord's sake cause Your face to shine on Your sanctuary, which is desolate.",
    18: "O my God, incline Your ear and hear; open Your eyes and see our desolations, and the city which is called by Your name; for we do not present our supplications before You because of our righteous deeds, but because of Your great mercies.",
    19: "O Lord, hear! O Lord, forgive! O Lord, listen and act! Do not delay for Your own sake, my God, for Your city and Your people are called by Your name.\"",
    20: "Now while I was speaking, praying, and confessing my sin and the sin of my people Israel, and presenting my supplication before the LORD my God for the holy mountain of my God,",
    21: "yes, while I was speaking in prayer, the man Gabriel, whom I had seen in the vision at the beginning, being caused to fly swiftly, reached me about the time of the evening offering.",
    22: "And he informed me, and talked with me, and said, \"O Daniel, I have now come forth to give you skill to understand.",
    23: "At the beginning of your supplications the command went out, and I have come to tell you, for you are greatly beloved; therefore consider the matter, and understand the vision:",
    24: "Seventy weeks are determined for your people and for your holy city, to finish the transgression, to make an end of sins, to make reconciliation for iniquity, to bring in everlasting righteousness, to seal up vision and prophecy, and to anoint the Most Holy.",
    25: "Know therefore and understand, that from the going forth of the command to restore and build Jerusalem until Messiah the Prince, there shall be seven weeks and sixty-two weeks; the street shall be built again, and the wall, even in troublesome times.",
    26: "And after the sixty-two weeks Messiah shall be cut off, but not for Himself; and the people of the prince who is to come shall destroy the city and the sanctuary. The end of it shall be with a flood, and till the end of the war desolations are determined.",
    27: "Then he shall confirm a covenant with many for one week; but in the middle of the week he shall bring an end to sacrifice and offering. And on the wing of abominations shall be one who makes desolate, even until the consummation, which is determined, is poured out on the desolate.\"",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"27_1_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"27_3_{v}"] = t
for v, t in ch6.items():
    ENTRIES[f"27_6_{v}"] = t
for v, t in ch9.items():
    ENTRIES[f"27_9_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Daniel landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
