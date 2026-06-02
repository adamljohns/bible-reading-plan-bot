"""MBT generator: Judges landmark chapters.

Book ID 7. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Judges 4 (24 verses) — Deborah, Barak, and Sisera; Jael's tent peg
- Judges 6 (40 verses) — Gideon's call; the altar at Ophrah; the fleece
- Judges 7 (25 verses) — Gideon's 300; the torches in pitchers
- Judges 16 (31 verses) — Samson, Delilah, the gates of Gaza, Dagon's temple

Total: 120 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Judges 4 — Deborah and Barak
ch4 = {
    1: "When Ehud was dead, the children of Israel again did evil in the sight of the LORD.",
    2: "So the LORD sold them into the hand of Jabin king of Canaan, who reigned in Hazor. The commander of his army was Sisera, who dwelt in Harosheth Hagoyim.",
    3: "And the children of Israel cried out to the LORD; for Jabin had nine hundred chariots of iron, and for twenty years he had harshly oppressed the children of Israel.",
    4: "Now Deborah, a prophetess, the wife of Lapidoth, was judging Israel at that time.",
    5: "And she would sit under the palm tree of Deborah between Ramah and Bethel in the mountains of Ephraim. And the children of Israel came up to her for judgment.",
    6: "Then she sent and called for Barak the son of Abinoam from Kedesh in Naphtali, and said to him, \"Has not the LORD God of Israel commanded, 'Go and deploy troops at Mount Tabor; take with you ten thousand men of the sons of Naphtali and of the sons of Zebulun;",
    7: "and against you I will deploy Sisera, the commander of Jabin's army, with his chariots and his multitude at the River Kishon; and I will deliver him into your hand'?\"",
    8: "And Barak said to her, \"If you will go with me, then I will go; but if you will not go with me, I will not go!\"",
    9: "So she said, \"I will surely go with you; nevertheless there will be no glory for you in the journey you are taking, for the LORD will sell Sisera into the hand of a woman.\" Then Deborah arose and went with Barak to Kedesh.",
    10: "And Barak called Zebulun and Naphtali to Kedesh; he went up with ten thousand men under his command, and Deborah went up with him.",
    11: "Now Heber the Kenite, of the children of Hobab the father-in-law of Moses, had separated himself from the Kenites and pitched his tent near the terebinth tree at Zaanaim, which is beside Kedesh.",
    12: "And they reported to Sisera that Barak the son of Abinoam had gone up to Mount Tabor.",
    13: "So Sisera gathered together all his chariots, nine hundred chariots of iron, and all the people who were with him, from Harosheth Hagoyim to the River Kishon.",
    14: "Then Deborah said to Barak, \"Up! For this is the day in which the LORD has delivered Sisera into your hand. Has not the LORD gone out before you?\" So Barak went down from Mount Tabor with ten thousand men following him.",
    15: "And the LORD routed Sisera and all his chariots and all his army with the edge of the sword before Barak; and Sisera alighted from his chariot and fled away on foot.",
    16: "But Barak pursued the chariots and the army as far as Harosheth Hagoyim, and all the army of Sisera fell by the edge of the sword; not a man was left.",
    17: "However, Sisera had fled away on foot to the tent of Jael, the wife of Heber the Kenite; for there was peace between Jabin king of Hazor and the house of Heber the Kenite.",
    18: "And Jael went out to meet Sisera, and said to him, \"Turn aside, my lord, turn aside to me; do not fear.\" And when he had turned aside with her into the tent, she covered him with a blanket.",
    19: "Then he said to her, \"Please give me a little water to drink, for I am thirsty.\" So she opened a jug of milk, gave him a drink, and covered him.",
    20: "And he said to her, \"Stand at the door of the tent, and if any man comes and inquires of you, and says, 'Is there any man here?' you shall say, 'No.'\"",
    21: "Then Jael, Heber's wife, took a tent peg and took a hammer in her hand, and went softly to him and drove the peg into his temple, and it went down into the ground; for he was fast asleep and weary. So he died.",
    22: "And then, as Barak pursued Sisera, Jael came out to meet him, and said to him, \"Come, I will show you the man whom you seek.\" And when he went into her tent, there lay Sisera, dead with the peg in his temple.",
    23: "So on that day God subdued Jabin king of Canaan in the presence of the children of Israel.",
    24: "And the hand of the children of Israel grew stronger and stronger against Jabin king of Canaan, until they had destroyed Jabin king of Canaan.",
}

# Judges 6 — Gideon's call, altar at Ophrah, fleece
ch6 = {
    1: "Then the children of Israel did evil in the sight of the LORD. So the LORD delivered them into the hand of Midian for seven years,",
    2: "and the hand of Midian prevailed against Israel. Because of the Midianites, the children of Israel made for themselves the dens, the caves, and the strongholds which are in the mountains.",
    3: "So it was, whenever Israel had sown, Midianites would come up; also Amalekites and the people of the East would come up against them.",
    4: "Then they would encamp against them and destroy the produce of the earth as far as Gaza, and leave no sustenance for Israel, neither sheep nor ox nor donkey.",
    5: "For they would come up with their livestock and their tents, coming in as numerous as locusts; both they and their camels were without number; and they would enter the land to destroy it.",
    6: "So Israel was greatly impoverished because of the Midianites, and the children of Israel cried out to the LORD.",
    7: "And it came to pass, when the children of Israel cried out to the LORD because of the Midianites,",
    8: "that the LORD sent a prophet to the children of Israel, who said to them, \"Thus says the LORD God of Israel: 'I brought you up from Egypt and brought you out of the house of bondage;",
    9: "and I delivered you out of the hand of the Egyptians and out of the hand of all who oppressed you, and drove them out before you and gave you their land.",
    10: "Also I said to you, \"I am the LORD your God; do not fear the gods of the Amorites, in whose land you dwell.\" But you have not obeyed My voice.'\"",
    11: "Now the Angel of the LORD came and sat under the terebinth tree which was in Ophrah, which belonged to Joash the Abiezrite, while his son Gideon threshed wheat in the winepress, in order to hide it from the Midianites.",
    12: "And the Angel of the LORD appeared to him, and said to him, \"The LORD is with you, you mighty man of valor!\"",
    13: "Gideon said to Him, \"O my lord, if the LORD is with us, why then has all this happened to us? And where are all His miracles which our fathers told us about, saying, 'Did not the LORD bring us up from Egypt?' But now the LORD has forsaken us and delivered us into the hands of the Midianites.\"",
    14: "Then the LORD turned to him and said, \"Go in this might of yours, and you shall save Israel from the hand of the Midianites. Have I not sent you?\"",
    15: "So he said to Him, \"O my Lord, how can I save Israel? Indeed my clan is the weakest in Manasseh, and I am the least in my father's house.\"",
    16: "And the LORD said to him, \"Surely I will be with you, and you shall defeat the Midianites as one man.\"",
    17: "Then he said to Him, \"If now I have found favor in Your sight, then show me a sign that it is You who talk with me.",
    18: "Do not depart from here, I pray, until I come to You and bring out my offering and set it before You.\" And He said, \"I will wait until you come back.\"",
    19: "So Gideon went in and prepared a young goat, and unleavened bread from an ephah of flour. The meat he put in a basket, and he put the broth in a pot; and he brought them out to Him under the terebinth tree and presented them.",
    20: "The Angel of God said to him, \"Take the meat and the unleavened bread and lay them on this rock, and pour out the broth.\" And he did so.",
    21: "Then the Angel of the LORD put out the end of the staff that was in His hand, and touched the meat and the unleavened bread; and fire rose out of the rock and consumed the meat and the unleavened bread. And the Angel of the LORD departed out of his sight.",
    22: "Now Gideon perceived that He was the Angel of the LORD. So Gideon said, \"Alas, O Lord GOD! For I have seen the Angel of the LORD face to face.\"",
    23: "Then the LORD said to him, \"Peace be with you; do not fear, you shall not die.\"",
    24: "So Gideon built an altar there to the LORD, and called it The-LORD-Is-Peace. To this day it is still in Ophrah of the Abiezrites.",
    25: "Now it came to pass the same night that the LORD said to him, \"Take your father's young bull, the second bull of seven years old, and tear down the altar of Baal that your father has, and cut down the wooden image that is beside it;",
    26: "and build an altar to the LORD your God on top of this rock in the proper arrangement, and take the second bull and offer a burnt sacrifice with the wood of the image which you shall cut down.\"",
    27: "So Gideon took ten men from among his servants and did as the LORD had said to him. But because he feared his father's household and the men of the city too much to do it by day, he did it by night.",
    28: "And when the men of the city arose early in the morning, there was the altar of Baal, torn down; and the wooden image that was beside it was cut down, and the second bull was being offered on the altar which had been built.",
    29: "So they said to one another, \"Who has done this thing?\" And when they had inquired and asked, they said, \"Gideon the son of Joash has done this thing.\"",
    30: "Then the men of the city said to Joash, \"Bring out your son, that he may die, because he has torn down the altar of Baal, and because he has cut down the wooden image that was beside it.\"",
    31: "But Joash said to all who stood against him, \"Would you plead for Baal? Would you save him? Let the one who would plead for him be put to death by morning! If he is a god, let him plead for himself, because his altar has been torn down!\"",
    32: "Therefore on that day he called him Jerubbaal, saying, \"Let Baal plead against him, because he has torn down his altar.\"",
    33: "Then all the Midianites and Amalekites and the people of the East gathered together; and they crossed over and encamped in the Valley of Jezreel.",
    34: "But the Spirit of the LORD came upon Gideon; then he blew the trumpet, and the Abiezrites gathered behind him.",
    35: "And he sent messengers throughout all Manasseh, who also gathered behind him. He also sent messengers to Asher, Zebulun, and Naphtali; and they came up to meet them.",
    36: "So Gideon said to God, \"If You will save Israel by my hand as You have said —",
    37: "look, I shall put a fleece of wool on the threshing floor; if there is dew on the fleece only, and it is dry on all the ground, then I shall know that You will save Israel by my hand, as You have said.\"",
    38: "And it was so. When he rose early the next morning and squeezed the fleece together, he wrung the dew out of the fleece, a bowlful of water.",
    39: "Then Gideon said to God, \"Do not be angry with me, but let me speak just once more: Let me test, I pray, just once more with the fleece; let it now be dry only on the fleece, but on all the ground let there be dew.\"",
    40: "And God did so that night. It was dry on the fleece only, but there was dew on all the ground.",
}

# Judges 7 — Gideon's 300
ch7 = {
    1: "Then Jerubbaal (that is, Gideon) and all the people who were with him rose early and encamped beside the well of Harod, so that the camp of the Midianites was on the north side of them by the hill of Moreh in the valley.",
    2: "And the LORD said to Gideon, \"The people who are with you are too many for Me to give the Midianites into their hands, lest Israel claim glory for itself against Me, saying, 'My own hand has saved me.'",
    3: "Now therefore, proclaim in the hearing of the people, saying, 'Whoever is fearful and afraid, let him turn and depart at once from Mount Gilead.'\" And twenty-two thousand of the people returned, and ten thousand remained.",
    4: "But the LORD said to Gideon, \"The people are still too many; bring them down to the water, and I will test them for you there. Then it will be, that of whom I say to you, 'This one shall go with you,' the same shall go with you; and of whomever I say to you, 'This one shall not go with you,' the same shall not go.\"",
    5: "So he brought the people down to the water. And the LORD said to Gideon, \"Everyone who laps from the water with his tongue, as a dog laps, you shall set apart by himself; likewise everyone who gets down on his knees to drink.\"",
    6: "And the number of those who lapped, putting their hand to their mouth, was three hundred men; but all the rest of the people got down on their knees to drink water.",
    7: "Then the LORD said to Gideon, \"By the three hundred men who lapped I will save you, and deliver the Midianites into your hand. Let all the other people go, every man to his place.\"",
    8: "So the people took provisions and their trumpets in their hands. And he sent away all the rest of Israel, every man to his tent, and retained those three hundred men. Now the camp of Midian was below him in the valley.",
    9: "It happened on the same night that the LORD said to him, \"Arise, go down against the camp, for I have delivered it into your hand.",
    10: "But if you are afraid to go down, go down to the camp with Purah your servant,",
    11: "and you shall hear what they say; and afterward your hands shall be strengthened to go down against the camp.\" Then he went down with Purah his servant to the outpost of the armed men who were in the camp.",
    12: "Now the Midianites and Amalekites, all the people of the East, were lying in the valley as numerous as locusts; and their camels were without number, as the sand by the seashore in multitude.",
    13: "And when Gideon had come, there was a man telling a dream to his companion. He said, \"I have just had a dream: To my surprise, a loaf of barley bread tumbled into the camp of Midian; it came to a tent and struck it so that it fell and overturned, and the tent collapsed.\"",
    14: "Then his companion answered and said, \"This is nothing else but the sword of Gideon the son of Joash, a man of Israel! Into his hand God has delivered Midian and the whole camp.\"",
    15: "And so it was, when Gideon heard the telling of the dream and its interpretation, that he worshiped. He returned to the camp of Israel, and said, \"Arise, for the LORD has delivered the camp of Midian into your hand.\"",
    16: "Then he divided the three hundred men into three companies, and he put a trumpet into every man's hand, with empty pitchers, and torches inside the pitchers.",
    17: "And he said to them, \"Look at me and do likewise; watch, and when I come to the edge of the camp you shall do as I do:",
    18: "When I blow the trumpet, I and all who are with me, then you also blow the trumpets on every side of the whole camp, and say, 'The sword of the LORD and of Gideon!'\"",
    19: "So Gideon and the hundred men who were with him came to the outpost of the camp at the beginning of the middle watch, just as they had posted the watch; and they blew the trumpets and broke the pitchers that were in their hands.",
    20: "Then the three companies blew the trumpets and broke the pitchers — they held the torches in their left hands and the trumpets in their right hands for blowing — and they cried, \"The sword of the LORD and of Gideon!\"",
    21: "And every man stood in his place all around the camp; and the whole army ran and cried out and fled.",
    22: "When the three hundred blew the trumpets, the LORD set every man's sword against his companion throughout the whole camp; and the army fled to Beth Acacia, toward Zererah, as far as the border of Abel Meholah, by Tabbath.",
    23: "And the men of Israel gathered together from Naphtali, Asher, and all Manasseh, and pursued the Midianites.",
    24: "Then Gideon sent messengers throughout all the mountains of Ephraim, saying, \"Come down against the Midianites, and seize from them the watering places as far as Beth Barah and the Jordan.\" Then all the men of Ephraim gathered together and seized the watering places as far as Beth Barah and the Jordan.",
    25: "And they captured two princes of the Midianites, Oreb and Zeeb. They killed Oreb at the rock of Oreb, and Zeeb they killed at the winepress of Zeeb. They pursued Midian and brought the heads of Oreb and Zeeb to Gideon on the other side of the Jordan.",
}

# Judges 16 — Samson, Delilah, gates of Gaza, Dagon's temple
ch16 = {
    1: "Now Samson went to Gaza and saw a harlot there, and went in to her.",
    2: "When the Gazites were told, \"Samson has come here!\" they surrounded the place and lay in wait for him all night at the gate of the city. They were quiet all night, saying, \"In the morning, when it is daylight, we will kill him.\"",
    3: "And Samson lay low till midnight; then he arose at midnight, took hold of the doors of the gate of the city and the two gateposts, pulled them up, bar and all, put them on his shoulders, and carried them to the top of the hill that faces Hebron.",
    4: "Afterward it happened that he loved a woman in the Valley of Sorek, whose name was Delilah.",
    5: "And the lords of the Philistines came up to her and said to her, \"Entice him, and find out where his great strength lies, and by what means we may overpower him, that we may bind him to afflict him; and every one of us will give you eleven hundred pieces of silver.\"",
    6: "So Delilah said to Samson, \"Please tell me where your great strength lies, and with what you may be bound to afflict you.\"",
    7: "And Samson said to her, \"If they bind me with seven fresh bowstrings, not yet dried, then I shall become weak, and be like any other man.\"",
    8: "So the lords of the Philistines brought up to her seven fresh bowstrings, not yet dried, and she bound him with them.",
    9: "Now men were lying in wait, staying with her in the room. And she said to him, \"The Philistines are upon you, Samson!\" But he broke the bowstrings as a strand of yarn breaks when it touches fire. So the secret of his strength was not known.",
    10: "Then Delilah said to Samson, \"Look, you have mocked me and told me lies. Now, please tell me what you may be bound with.\"",
    11: "So he said to her, \"If they bind me securely with new ropes that have never been used, then I shall become weak, and be like any other man.\"",
    12: "Therefore Delilah took new ropes and bound him with them, and said to him, \"The Philistines are upon you, Samson!\" And men were lying in wait, staying in the room. But he broke them off his arms like a thread.",
    13: "Delilah said to Samson, \"Until now you have mocked me and told me lies. Tell me what you may be bound with.\" And he said to her, \"If you weave the seven locks of my head into the web of the loom\" —",
    14: "so she wove it tightly with the batten of the loom, and said to him, \"The Philistines are upon you, Samson!\" But he awoke from his sleep, and pulled out the batten and the web from the loom.",
    15: "Then she said to him, \"How can you say, 'I love you,' when your heart is not with me? You have mocked me these three times, and have not told me where your great strength lies.\"",
    16: "And it came to pass, when she pestered him daily with her words and pressed him, so that his soul was vexed to death,",
    17: "that he told her all his heart, and said to her, \"No razor has ever come upon my head, for I have been a Nazirite to God from my mother's womb. If I am shaven, then my strength will leave me, and I shall become weak, and be like any other man.\"",
    18: "When Delilah saw that he had told her all his heart, she sent and called for the lords of the Philistines, saying, \"Come up once more, for he has told me all his heart.\" So the lords of the Philistines came up to her and brought the money in their hand.",
    19: "Then she lulled him to sleep on her knees, and called for a man and had him shave off the seven locks of his head. Then she began to torment him, and his strength left him.",
    20: "And she said, \"The Philistines are upon you, Samson!\" So he awoke from his sleep, and said, \"I will go out as before, at other times, and shake myself free!\" But he did not know that the LORD had departed from him.",
    21: "Then the Philistines took him and put out his eyes, and brought him down to Gaza. They bound him with bronze fetters, and he became a grinder in the prison.",
    22: "However, the hair of his head began to grow again after it had been shaven.",
    23: "Now the lords of the Philistines gathered together to offer a great sacrifice to Dagon their god, and to rejoice. And they said: \"Our god has delivered into our hands Samson our enemy!\"",
    24: "When the people saw him, they praised their god; for they said: \"Our god has delivered into our hands our enemy, the destroyer of our land, and the one who multiplied our dead.\"",
    25: "So it happened, when their hearts were merry, that they said, \"Call for Samson, that he may perform for us.\" So they called for Samson from the prison, and he performed for them. And they stationed him between the pillars.",
    26: "Then Samson said to the lad who held him by the hand, \"Let me feel the pillars which support the temple, so that I can lean on them.\"",
    27: "Now the temple was full of men and women. All the lords of the Philistines were there — about three thousand men and women on the roof watching while Samson performed.",
    28: "Then Samson called to the LORD, saying, \"O Lord GOD, remember me, I pray! Strengthen me, I pray, just this once, O God, that I may with one blow take vengeance on the Philistines for my two eyes!\"",
    29: "And Samson took hold of the two middle pillars which supported the temple, and he braced himself against them, one on his right and the other on his left.",
    30: "Then Samson said, \"Let me die with the Philistines!\" And he pushed with all his might, and the temple fell on the lords and all the people who were in it. So the dead that he killed at his death were more than he had killed in his life.",
    31: "And his brothers and all his father's household came down and took him, and brought him up and buried him between Zorah and Eshtaol in the tomb of his father Manoah. He had judged Israel twenty years.",
}

ENTRIES = {}
for v, t in ch4.items():
    ENTRIES[f"7_4_{v}"] = t
for v, t in ch6.items():
    ENTRIES[f"7_6_{v}"] = t
for v, t in ch7.items():
    ENTRIES[f"7_7_{v}"] = t
for v, t in ch16.items():
    ENTRIES[f"7_16_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Judges landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
