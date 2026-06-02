"""MBT generator: Davidic + Solomonic monarchy landmarks.

Book IDs: 2 Samuel = 10, 1 Kings = 11.
NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- 2 Samuel 7 (29 verses) — the Davidic covenant: "your house and your
  kingdom shall be established forever"
- 1 Kings 3 (28 verses) — Solomon's dream at Gibeon and the judgment
  of the two mothers
- 1 Kings 8:22-53 (32 verses) — Solomon's temple dedication prayer

Total: 89 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# 2 Samuel 7 — the Davidic covenant
sam2_7 = {
    1: "Now it came to pass when the king was dwelling in his house, and the LORD had given him rest from all his enemies all around,",
    2: "that the king said to Nathan the prophet, \"See now, I dwell in a house of cedar, but the ark of God dwells inside tent curtains.\"",
    3: "Then Nathan said to the king, \"Go, do all that is in your heart, for the LORD is with you.\"",
    4: "But it happened that night that the word of the LORD came to Nathan, saying,",
    5: "\"Go and tell My servant David, 'Thus says the LORD: \"Would you build a house for Me to dwell in?",
    6: "For I have not dwelt in a house since the time that I brought the children of Israel up from Egypt, even to this day, but have moved about in a tent and in a tabernacle.",
    7: "Wherever I have moved about with all the children of Israel, have I ever spoken a word to anyone from the tribes of Israel, whom I commanded to shepherd My people Israel, saying, 'Why have you not built Me a house of cedar?'\"'",
    8: "Now therefore, thus shall you say to My servant David, 'Thus says the LORD of hosts: \"I took you from the sheepfold, from following the sheep, to be ruler over My people, over Israel.",
    9: "And I have been with you wherever you have gone, and have cut off all your enemies from before you, and have made you a great name, like the name of the great men who are on the earth.",
    10: "Moreover I will appoint a place for My people Israel, and will plant them, that they may dwell in a place of their own and move no more; nor shall the sons of wickedness oppress them anymore, as previously,",
    11: "since the time that I commanded judges to be over My people Israel, and have caused you to rest from all your enemies. Also the LORD tells you that He will make you a house.",
    12: "When your days are fulfilled and you rest with your fathers, I will set up your seed after you, who will come from your body, and I will establish his kingdom.",
    13: "He shall build a house for My name, and I will establish the throne of his kingdom forever.",
    14: "I will be his Father, and he shall be My son. If he commits iniquity, I will chasten him with the rod of men and with the blows of the sons of men.",
    15: "But My mercy shall not depart from him, as I took it from Saul, whom I removed from before you.",
    16: "And your house and your kingdom shall be established forever before you. Your throne shall be established forever.\"'\"",
    17: "According to all these words and according to all this vision, so Nathan spoke to David.",
    18: "Then King David went in and sat before the LORD; and he said: \"Who am I, O Lord GOD? And what is my house, that You have brought me this far?",
    19: "And yet this was a small thing in Your sight, O Lord GOD; and You have also spoken of Your servant's house for a great while to come. Is this the manner of man, O Lord GOD?",
    20: "Now what more can David say to You? For You, Lord GOD, know Your servant.",
    21: "For Your word's sake, and according to Your own heart, You have done all these great things, to make Your servant know them.",
    22: "Therefore You are great, O Lord GOD. For there is none like You, nor is there any God besides You, according to all that we have heard with our ears.",
    23: "And who is like Your people, like Israel, the one nation on the earth whom God went to redeem for Himself as a people, to make for Himself a name — and to do for Yourself great and awesome deeds for Your land — before Your people whom You redeemed for Yourself from Egypt, the nations, and their gods?",
    24: "For You have made Your people Israel Your very own people forever; and You, LORD, have become their God.",
    25: "Now, O LORD God, the word which You have spoken concerning Your servant and concerning his house, establish it forever and do as You have said.",
    26: "So let Your name be magnified forever, saying, 'The LORD of hosts is the God over Israel.' And let the house of Your servant David be established before You.",
    27: "For You, O LORD of hosts, God of Israel, have revealed this to Your servant, saying, 'I will build you a house.' Therefore Your servant has found it in his heart to pray this prayer to You.",
    28: "And now, O Lord GOD, You are God, and Your words are true, and You have promised this goodness to Your servant.",
    29: "Now therefore, let it please You to bless the house of Your servant, that it may continue forever before You; for You, O Lord GOD, have spoken it, and with Your blessing let the house of Your servant be blessed forever.\"",
}

# 1 Kings 3 — Solomon's wisdom and the judgment of the two mothers
kgs1_3 = {
    1: "Now Solomon made a treaty with Pharaoh king of Egypt, and married Pharaoh's daughter; then he brought her to the City of David until he had finished building his own house, and the house of the LORD, and the wall all around Jerusalem.",
    2: "Meanwhile the people sacrificed at the high places, because there was no house built for the name of the LORD until those days.",
    3: "And Solomon loved the LORD, walking in the statutes of his father David, except that he sacrificed and burned incense at the high places.",
    4: "Now the king went to Gibeon to sacrifice there, for that was the great high place: Solomon offered a thousand burnt offerings on that altar.",
    5: "At Gibeon the LORD appeared to Solomon in a dream by night; and God said, \"Ask! What shall I give you?\"",
    6: "And Solomon said: \"You have shown great mercy to Your servant David my father, because he walked before You in truth, in righteousness, and in uprightness of heart with You; You have continued this great kindness for him, and You have given him a son to sit on his throne, as it is this day.",
    7: "Now, O LORD my God, You have made Your servant king instead of my father David, but I am a little child; I do not know how to go out or come in.",
    8: "And Your servant is in the midst of Your people whom You have chosen, a great people, too numerous to be numbered or counted.",
    9: "Therefore give to Your servant an understanding heart to judge Your people, that I may discern between good and evil. For who is able to judge this great people of Yours?\"",
    10: "The speech pleased the Lord, that Solomon had asked this thing.",
    11: "Then God said to him: \"Because you have asked this thing, and have not asked long life for yourself, nor have asked riches for yourself, nor have asked the life of your enemies, but have asked for yourself understanding to discern justice,",
    12: "behold, I have done according to your words; see, I have given you a wise and understanding heart, so that there has not been anyone like you before you, nor shall any like you arise after you.",
    13: "And I have also given you what you have not asked: both riches and honor, so that there shall not be anyone like you among the kings all your days.",
    14: "So if you walk in My ways, to keep My statutes and My commandments, as your father David walked, then I will lengthen your days.\"",
    15: "Then Solomon awoke; and indeed it had been a dream. And he came to Jerusalem and stood before the ark of the covenant of the LORD, offered up burnt offerings, offered peace offerings, and made a feast for all his servants.",
    16: "Now two women who were harlots came to the king, and stood before him.",
    17: "And one woman said, \"O my lord, this woman and I dwell in the same house; and I gave birth while she was in the house.",
    18: "Then it happened, the third day after I had given birth, that this woman also gave birth. And we were together; no one was with us in the house, except the two of us in the house.",
    19: "And this woman's son died in the night, because she lay on him.",
    20: "So she arose in the middle of the night and took my son from my side, while your maidservant slept, and laid him in her bosom, and laid her dead child in my bosom.",
    21: "And when I rose in the morning to nurse my son, there he was, dead. But when I had examined him in the morning, indeed, he was not my son whom I had borne.\"",
    22: "Then the other woman said, \"No! But the living one is my son, and the dead one is your son.\" And the first woman said, \"No! But the dead one is your son, and the living one is my son.\" Thus they spoke before the king.",
    23: "And the king said, \"The one says, 'This is my son, who lives, and your son is the dead one'; and the other says, 'No! But your son is the dead one, and my son is the living one.'\"",
    24: "Then the king said, \"Bring me a sword.\" So they brought a sword before the king.",
    25: "And the king said, \"Divide the living child in two, and give half to one, and half to the other.\"",
    26: "Then the woman whose son was living spoke to the king, for she yearned with compassion for her son; and she said, \"O my lord, give her the living child, and by no means kill him!\" But the other said, \"Let him be neither mine nor yours, but divide him.\"",
    27: "So the king answered and said, \"Give the first woman the living child, and by no means kill him; she is his mother.\"",
    28: "And all Israel heard of the judgment which the king had rendered; and they feared the king, for they saw that the wisdom of God was in him to administer justice.",
}

# 1 Kings 8:22-53 — Solomon's temple dedication prayer
kgs1_8 = {
    22: "Then Solomon stood before the altar of the LORD in the presence of all the assembly of Israel, and spread out his hands toward heaven;",
    23: "and he said: \"LORD God of Israel, there is no God in heaven above or on earth below like You, who keep Your covenant and mercy with Your servants who walk before You with all their hearts.",
    24: "You have kept what You promised Your servant David my father; You have both spoken with Your mouth and fulfilled it with Your hand, as it is this day.",
    25: "Therefore, LORD God of Israel, now keep what You promised Your servant David my father, saying, 'You shall not fail to have a man sit before Me on the throne of Israel, if only your sons take heed to their way, that they walk before Me as you have walked before Me.'",
    26: "And now I pray, O God of Israel, let Your word come true, which You have spoken to Your servant David my father.",
    27: "But will God indeed dwell on the earth? Behold, heaven and the heaven of heavens cannot contain You. How much less this temple which I have built!",
    28: "Yet regard the prayer of Your servant and his supplication, O LORD my God, and listen to the cry and the prayer which Your servant is praying before You today:",
    29: "that Your eyes may be open toward this temple night and day, toward the place of which You said, 'My name shall be there,' that You may hear the prayer which Your servant makes toward this place.",
    30: "And may You hear the supplication of Your servant and of Your people Israel, when they pray toward this place. Hear in heaven Your dwelling place; and when You hear, forgive.",
    31: "When anyone sins against his neighbor, and is forced to take an oath, and comes and takes an oath before Your altar in this temple,",
    32: "then hear in heaven, and act, and judge Your servants, condemning the wicked, bringing his way on his head, and justifying the righteous by giving him according to his righteousness.",
    33: "When Your people Israel are defeated before an enemy because they have sinned against You, and when they turn back to You and confess Your name, and pray and make supplication to You in this temple,",
    34: "then hear in heaven, and forgive the sin of Your people Israel, and bring them back to the land which You gave to their fathers.",
    35: "When the heavens are shut up and there is no rain because they have sinned against You, when they pray toward this place and confess Your name, and turn from their sin because You afflict them,",
    36: "then hear in heaven, and forgive the sin of Your servants, Your people Israel, that You may teach them the good way in which they should walk; and send rain on Your land which You have given to Your people as an inheritance.",
    37: "When there is famine in the land, pestilence or blight or mildew, locusts or grasshoppers; when their enemy besieges them in the land of their cities; whatever plague or whatever sickness there is;",
    38: "whatever prayer, whatever supplication is made by anyone, or by all Your people Israel, when each one knows the plague of his own heart, and spreads out his hands toward this temple:",
    39: "then hear in heaven Your dwelling place, and forgive, and act, and give to everyone according to all his ways, whose heart You know (for You alone know the hearts of all the sons of men),",
    40: "that they may fear You all the days that they live in the land which You gave to our fathers.",
    41: "Moreover, concerning a foreigner, who is not of Your people Israel, but has come from a far country for Your name's sake",
    42: "(for they will hear of Your great name and Your strong hand and Your outstretched arm), when he comes and prays toward this temple,",
    43: "hear in heaven Your dwelling place, and do according to all for which the foreigner calls to You, that all peoples of the earth may know Your name and fear You, as do Your people Israel, and that they may know that this temple which I have built is called by Your name.",
    44: "When Your people go out to battle against their enemy, wherever You send them, and when they pray to the LORD toward the city which You have chosen and the temple which I have built for Your name,",
    45: "then hear in heaven their prayer and their supplication, and maintain their cause.",
    46: "When they sin against You (for there is no one who does not sin), and You become angry with them and deliver them to the enemy, and they take them captive to the land of the enemy, far or near;",
    47: "yet when they come to themselves in the land where they were carried captive, and repent, and make supplication to You in the land of those who took them captive, saying, 'We have sinned and done wrong, we have committed wickedness';",
    48: "and when they return to You with all their heart and with all their soul in the land of their enemies who led them away captive, and pray to You toward their land which You gave to their fathers, the city which You have chosen and the temple which I have built for Your name:",
    49: "then hear in heaven Your dwelling place their prayer and their supplication, and maintain their cause,",
    50: "and forgive Your people who have sinned against You, and all their transgressions which they have transgressed against You; and grant them compassion before those who took them captive, that they may have compassion on them",
    51: "(for they are Your people and Your inheritance, whom You brought out of Egypt, out of the iron furnace),",
    52: "that Your eyes may be open to the supplication of Your servant and the supplication of Your people Israel, to listen to them whenever they call to You.",
    53: "For You separated them from among all the peoples of the earth to be Your inheritance, as You spoke by Your servant Moses, when You brought our fathers out of Egypt, O Lord GOD.\"",
}

ENTRIES = {}
for v, t in sam2_7.items():
    ENTRIES[f"10_7_{v}"] = t
for v, t in kgs1_3.items():
    ENTRIES[f"11_3_{v}"] = t
for v, t in kgs1_8.items():
    ENTRIES[f"11_8_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Davidic-Solomonic landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
