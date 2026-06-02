"""MBT generator: Exodus foundational chapters.

Book ID 2. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Exodus 3 (22 verses) — the burning bush; I AM WHO I AM
- Exodus 19 (25 verses) — Sinai theophany
- Exodus 20 (26 verses) — the Ten Commandments
- Exodus 33 (23 verses) — "show me Your glory"
- Exodus 34 (35 verses) — the proclamation of the Name

Total: 131 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Exodus 3 — the burning bush, I AM WHO I AM
ch3 = {
    1: "Now Moses was tending the flock of Jethro his father-in-law, the priest of Midian. And he led the flock to the back of the desert, and came to Horeb, the mountain of God.",
    2: "And the Angel of the LORD appeared to him in a flame of fire from the midst of a bush. So he looked, and behold, the bush was burning with fire, but the bush was not consumed.",
    3: "Then Moses said, \"I will now turn aside and see this great sight, why the bush does not burn.\"",
    4: "So when the LORD saw that he turned aside to look, God called to him from the midst of the bush and said, \"Moses, Moses!\" And he said, \"Here I am.\"",
    5: "Then He said, \"Do not draw near this place. Take your sandals off your feet, for the place where you stand is holy ground.\"",
    6: "Moreover He said, \"I am the God of your father — the God of Abraham, the God of Isaac, and the God of Jacob.\" And Moses hid his face, for he was afraid to look upon God.",
    7: "And the LORD said: \"I have surely seen the oppression of My people who are in Egypt, and have heard their cry because of their taskmasters, for I know their sorrows.",
    8: "So I have come down to deliver them out of the hand of the Egyptians, and to bring them up from that land to a good and large land, to a land flowing with milk and honey, to the place of the Canaanites and the Hittites and the Amorites and the Perizzites and the Hivites and the Jebusites.",
    9: "Now therefore, behold, the cry of the children of Israel has come to Me, and I have also seen the oppression with which the Egyptians oppress them.",
    10: "Come now, therefore, and I will send you to Pharaoh that you may bring My people, the children of Israel, out of Egypt.\"",
    11: "But Moses said to God, \"Who am I that I should go to Pharaoh, and that I should bring the children of Israel out of Egypt?\"",
    12: "So He said, \"I will certainly be with you. And this shall be a sign to you that I have sent you: when you have brought the people out of Egypt, you shall serve God on this mountain.\"",
    13: "Then Moses said to God, \"Indeed, when I come to the children of Israel and say to them, 'The God of your fathers has sent me to you,' and they say to me, 'What is His name?' what shall I say to them?\"",
    14: "And God said to Moses, \"I AM WHO I AM.\" And He said, \"Thus you shall say to the children of Israel, 'I AM has sent me to you.'\"",
    15: "Moreover God said to Moses, \"Thus you shall say to the children of Israel: 'The LORD God of your fathers, the God of Abraham, the God of Isaac, and the God of Jacob, has sent me to you. This is My name forever, and this is My memorial to all generations.'",
    16: "Go and gather the elders of Israel together, and say to them, 'The LORD God of your fathers, the God of Abraham, of Isaac, and of Jacob, appeared to me, saying, \"I have surely visited you and seen what is done to you in Egypt;",
    17: "and I have said I will bring you up out of the affliction of Egypt to the land of the Canaanites and the Hittites and the Amorites and the Perizzites and the Hivites and the Jebusites, to a land flowing with milk and honey.\"'",
    18: "Then they will heed your voice; and you shall come, you and the elders of Israel, to the king of Egypt; and you shall say to him, 'The LORD God of the Hebrews has met with us; and now, please, let us go three days' journey into the wilderness, that we may sacrifice to the LORD our God.'",
    19: "But I am sure that the king of Egypt will not let you go, no, not even by a mighty hand.",
    20: "So I will stretch out My hand and strike Egypt with all My wonders which I will do in its midst; and after that he will let you go.",
    21: "And I will give this people favor in the sight of the Egyptians; and it shall be, when you go, that you shall not go empty-handed.",
    22: "But every woman shall ask of her neighbor, namely, of her who dwells near her house, articles of silver, articles of gold, and clothing; and you shall put them on your sons and on your daughters. So you shall plunder the Egyptians.\"",
}

# Exodus 19 — Sinai theophany
ch19 = {
    1: "In the third month after the children of Israel had gone out of the land of Egypt, on the same day, they came to the Wilderness of Sinai.",
    2: "For they had departed from Rephidim, had come to the Wilderness of Sinai, and camped in the wilderness. So Israel camped there before the mountain.",
    3: "And Moses went up to God, and the LORD called to him from the mountain, saying, \"Thus you shall say to the house of Jacob, and tell the children of Israel:",
    4: "'You have seen what I did to the Egyptians, and how I bore you on eagles' wings and brought you to Myself.",
    5: "Now therefore, if you will indeed obey My voice and keep My covenant, then you shall be a special treasure to Me above all people; for all the earth is Mine.",
    6: "And you shall be to Me a kingdom of priests and a holy nation.' These are the words which you shall speak to the children of Israel.\"",
    7: "So Moses came and called for the elders of the people, and laid before them all these words which the LORD commanded him.",
    8: "Then all the people answered together and said, \"All that the LORD has spoken we will do.\" So Moses brought back the words of the people to the LORD.",
    9: "And the LORD said to Moses, \"Behold, I come to you in the thick cloud, that the people may hear when I speak with you, and believe you forever.\" So Moses told the words of the people to the LORD.",
    10: "Then the LORD said to Moses, \"Go to the people and consecrate them today and tomorrow, and let them wash their clothes.",
    11: "And let them be ready for the third day. For on the third day the LORD will come down upon Mount Sinai in the sight of all the people.",
    12: "You shall set bounds for the people all around, saying, 'Take heed to yourselves that you do not go up to the mountain or touch its base. Whoever touches the mountain shall surely be put to death.",
    13: "Not a hand shall touch him, but he shall surely be stoned or shot with an arrow; whether man or beast, he shall not live.' When the trumpet sounds long, they shall come near the mountain.\"",
    14: "So Moses went down from the mountain to the people and sanctified the people, and they washed their clothes.",
    15: "And he said to the people, \"Be ready for the third day; do not come near your wives.\"",
    16: "Then it came to pass on the third day, in the morning, that there were thunderings and lightnings, and a thick cloud on the mountain; and the sound of the trumpet was very loud, so that all the people who were in the camp trembled.",
    17: "And Moses brought the people out of the camp to meet with God, and they stood at the foot of the mountain.",
    18: "Now Mount Sinai was completely in smoke, because the LORD descended upon it in fire. Its smoke ascended like the smoke of a furnace, and the whole mountain quaked greatly.",
    19: "And when the blast of the trumpet sounded long and became louder and louder, Moses spoke, and God answered him by voice.",
    20: "Then the LORD came down upon Mount Sinai, on the top of the mountain. And the LORD called Moses to the top of the mountain, and Moses went up.",
    21: "And the LORD said to Moses, \"Go down and warn the people, lest they break through to gaze at the LORD, and many of them perish.",
    22: "Also let the priests who come near the LORD consecrate themselves, lest the LORD break out against them.\"",
    23: "But Moses said to the LORD, \"The people cannot come up to Mount Sinai; for You warned us, saying, 'Set bounds around the mountain and consecrate it.'\"",
    24: "Then the LORD said to him, \"Away! Get down and then come up, you and Aaron with you. But do not let the priests and the people break through to come up to the LORD, lest He break out against them.\"",
    25: "So Moses went down to the people and spoke to them.",
}

# Exodus 20 — the Ten Commandments
ch20 = {
    1: "And God spoke all these words, saying:",
    2: "\"I am the LORD your God, who brought you out of the land of Egypt, out of the house of bondage.",
    3: "You shall have no other gods before Me.",
    4: "You shall not make for yourself a carved image — any likeness of anything that is in heaven above, or that is in the earth beneath, or that is in the water under the earth;",
    5: "you shall not bow down to them nor serve them. For I, the LORD your God, am a jealous God, visiting the iniquity of the fathers upon the children to the third and fourth generations of those who hate Me,",
    6: "but showing mercy to thousands, to those who love Me and keep My commandments.",
    7: "You shall not take the name of the LORD your God in vain, for the LORD will not hold him guiltless who takes His name in vain.",
    8: "Remember the Sabbath day, to keep it holy.",
    9: "Six days you shall labor and do all your work,",
    10: "but the seventh day is the Sabbath of the LORD your God. In it you shall do no work: you, nor your son, nor your daughter, nor your male servant, nor your female servant, nor your cattle, nor your stranger who is within your gates.",
    11: "For in six days the LORD made the heavens and the earth, the sea, and all that is in them, and rested the seventh day. Therefore the LORD blessed the Sabbath day and hallowed it.",
    12: "Honor your father and your mother, that your days may be long upon the land which the LORD your God is giving you.",
    13: "You shall not murder.",
    14: "You shall not commit adultery.",
    15: "You shall not steal.",
    16: "You shall not bear false witness against your neighbor.",
    17: "You shall not covet your neighbor's house; you shall not covet your neighbor's wife, nor his male servant, nor his female servant, nor his ox, nor his donkey, nor anything that is your neighbor's.\"",
    18: "Now all the people witnessed the thunderings, the lightning flashes, the sound of the trumpet, and the mountain smoking; and when the people saw it, they trembled and stood afar off.",
    19: "Then they said to Moses, \"You speak with us, and we will hear; but let not God speak with us, lest we die.\"",
    20: "And Moses said to the people, \"Do not fear; for God has come to test you, and that His fear may be before you, so that you may not sin.\"",
    21: "So the people stood afar off, but Moses drew near the thick darkness where God was.",
    22: "Then the LORD said to Moses, \"Thus you shall say to the children of Israel: 'You have seen that I have talked with you from heaven.",
    23: "You shall not make anything to be with Me — gods of silver or gods of gold you shall not make for yourselves.",
    24: "An altar of earth you shall make for Me, and you shall sacrifice on it your burnt offerings and your peace offerings, your sheep and your oxen. In every place where I record My name I will come to you, and I will bless you.",
    25: "And if you make Me an altar of stone, you shall not build it of hewn stone; for if you use your tool on it, you have profaned it.",
    26: "Nor shall you go up by steps to My altar, that your nakedness may not be exposed on it.'",
}

# Exodus 33 — "Show me Your glory"
ch33 = {
    1: "Then the LORD said to Moses, \"Depart and go up from here, you and the people whom you have brought out of the land of Egypt, to the land of which I swore to Abraham, Isaac, and Jacob, saying, 'To your descendants I will give it.'",
    2: "And I will send My Angel before you, and I will drive out the Canaanite and the Amorite and the Hittite and the Perizzite and the Hivite and the Jebusite.",
    3: "Go up to a land flowing with milk and honey; for I will not go up in your midst, lest I consume you on the way, for you are a stiff-necked people.\"",
    4: "And when the people heard this bad news, they mourned, and no one put on his ornaments.",
    5: "For the LORD had said to Moses, \"Say to the children of Israel, 'You are a stiff-necked people. I could come up into your midst in one moment and consume you. Now therefore, take off your ornaments, that I may know what to do to you.'\"",
    6: "So the children of Israel stripped themselves of their ornaments by Mount Horeb.",
    7: "Moses took his tent and pitched it outside the camp, far from the camp, and called it the tabernacle of meeting. And it came to pass that everyone who sought the LORD went out to the tabernacle of meeting which was outside the camp.",
    8: "So it was, whenever Moses went out to the tabernacle, that all the people rose, and each man stood at his tent door and watched Moses until he had gone into the tabernacle.",
    9: "And it came to pass, when Moses entered the tabernacle, that the pillar of cloud descended and stood at the door of the tabernacle, and the LORD talked with Moses.",
    10: "All the people saw the pillar of cloud standing at the tabernacle door, and all the people rose and worshiped, each man in his tent door.",
    11: "So the LORD spoke to Moses face to face, as a man speaks to his friend. And he would return to the camp, but his servant Joshua the son of Nun, a young man, did not depart from the tabernacle.",
    12: "Then Moses said to the LORD, \"See, You say to me, 'Bring up this people.' But You have not let me know whom You will send with me. Yet You have said, 'I know you by name, and you have also found grace in My sight.'",
    13: "Now therefore, I pray, if I have found grace in Your sight, show me now Your way, that I may know You and that I may find grace in Your sight. And consider that this nation is Your people.\"",
    14: "And He said, \"My Presence will go with you, and I will give you rest.\"",
    15: "Then he said to Him, \"If Your Presence does not go with us, do not bring us up from here.",
    16: "For how then will it be known that Your people and I have found grace in Your sight, except You go with us? So we shall be separate, Your people and I, from all the people who are upon the face of the earth.\"",
    17: "So the LORD said to Moses, \"I will also do this thing that you have spoken; for you have found grace in My sight, and I know you by name.\"",
    18: "And he said, \"Please, show me Your glory.\"",
    19: "Then He said, \"I will make all My goodness pass before you, and I will proclaim the name of the LORD before you. I will be gracious to whom I will be gracious, and I will have compassion on whom I will have compassion.\"",
    20: "But He said, \"You cannot see My face; for no man shall see Me, and live.\"",
    21: "And the LORD said, \"Here is a place by Me, and you shall stand on the rock.",
    22: "So it shall be, while My glory passes by, that I will put you in the cleft of the rock, and will cover you with My hand while I pass by.",
    23: "Then I will take away My hand, and you shall see My back; but My face shall not be seen.\"",
}

# Exodus 34 — the proclamation of the Name
ch34 = {
    1: "And the LORD said to Moses, \"Cut two tablets of stone like the first ones, and I will write on these tablets the words that were on the first tablets which you broke.",
    2: "So be ready in the morning, and come up in the morning to Mount Sinai, and present yourself to Me there on the top of the mountain.",
    3: "And no man shall come up with you, and let no man be seen throughout all the mountain; let neither flocks nor herds feed before that mountain.\"",
    4: "So he cut two tablets of stone like the first ones. Then Moses rose early in the morning and went up Mount Sinai, as the LORD had commanded him; and he took in his hand the two tablets of stone.",
    5: "Now the LORD descended in the cloud and stood with him there, and proclaimed the name of the LORD.",
    6: "And the LORD passed before him and proclaimed, \"The LORD, the LORD God, merciful and gracious, longsuffering, and abounding in goodness and truth,",
    7: "keeping mercy for thousands, forgiving iniquity and transgression and sin, by no means clearing the guilty, visiting the iniquity of the fathers upon the children and the children's children to the third and the fourth generation.\"",
    8: "So Moses made haste and bowed his head toward the earth, and worshiped.",
    9: "Then he said, \"If now I have found grace in Your sight, O Lord, let my Lord, I pray, go among us, even though we are a stiff-necked people; and pardon our iniquity and our sin, and take us as Your inheritance.\"",
    10: "And He said: \"Behold, I make a covenant. Before all your people I will do marvels such as have not been done in all the earth, nor in any nation; and all the people among whom you are shall see the work of the LORD. For it is an awesome thing that I will do with you.",
    11: "Observe what I command you this day. Behold, I am driving out from before you the Amorite and the Canaanite and the Hittite and the Perizzite and the Hivite and the Jebusite.",
    12: "Take heed to yourself, lest you make a covenant with the inhabitants of the land where you are going, lest it be a snare in your midst.",
    13: "But you shall destroy their altars, break their sacred pillars, and cut down their wooden images",
    14: "(for you shall worship no other god, for the LORD, whose name is Jealous, is a jealous God),",
    15: "lest you make a covenant with the inhabitants of the land, and they play the harlot with their gods and make sacrifice to their gods, and one of them invites you and you eat of his sacrifice,",
    16: "and you take of his daughters for your sons, and his daughters play the harlot with their gods and make your sons play the harlot with their gods.",
    17: "You shall make no molded gods for yourselves.",
    18: "The Feast of Unleavened Bread you shall keep. Seven days you shall eat unleavened bread, as I commanded you, in the appointed time of the month of Abib; for in the month of Abib you came out from Egypt.",
    19: "All that open the womb are Mine, and every male firstborn among your livestock, whether ox or sheep.",
    20: "But the firstborn of a donkey you shall redeem with a lamb. And if you will not redeem him, then you shall break his neck. All the firstborn of your sons you shall redeem. And none shall appear before Me empty-handed.",
    21: "Six days you shall work, but on the seventh day you shall rest; in plowing time and in harvest you shall rest.",
    22: "And you shall observe the Feast of Weeks, of the firstfruits of wheat harvest, and the Feast of Ingathering at the year's end.",
    23: "Three times in the year all your men shall appear before the Lord, the LORD God of Israel.",
    24: "For I will cast out the nations before you and enlarge your borders; neither will any man covet your land when you go up to appear before the LORD your God three times in the year.",
    25: "You shall not offer the blood of My sacrifice with leaven, nor shall the sacrifice of the Feast of the Passover be left until morning.",
    26: "The first of the firstfruits of your land you shall bring to the house of the LORD your God. You shall not boil a young goat in its mother's milk.\"",
    27: "Then the LORD said to Moses, \"Write these words, for according to the tenor of these words I have made a covenant with you and with Israel.\"",
    28: "So he was there with the LORD forty days and forty nights; he neither ate bread nor drank water. And He wrote on the tablets the words of the covenant, the Ten Commandments.",
    29: "Now it was so, when Moses came down from Mount Sinai (and the two tablets of the Testimony were in Moses' hand when he came down from the mountain), that Moses did not know that the skin of his face shone while he talked with Him.",
    30: "So when Aaron and all the children of Israel saw Moses, behold, the skin of his face shone, and they were afraid to come near him.",
    31: "Then Moses called to them, and Aaron and all the rulers of the congregation returned to him; and Moses talked with them.",
    32: "Afterward all the children of Israel came near, and he gave them as commandments all that the LORD had spoken with him on Mount Sinai.",
    33: "And when Moses had finished speaking with them, he put a veil on his face.",
    34: "But whenever Moses went in before the LORD to speak with Him, he would take the veil off until he came out; and he would come out and speak to the children of Israel whatever he had been commanded.",
    35: "And whenever the children of Israel saw the face of Moses, that the skin of Moses' face shone, then Moses would put the veil on his face again, until he went in to speak with Him.",
}

ENTRIES = {}
for v, t in ch3.items():
    ENTRIES[f"2_3_{v}"] = t
for v, t in ch19.items():
    ENTRIES[f"2_19_{v}"] = t
for v, t in ch20.items():
    ENTRIES[f"2_20_{v}"] = t
for v, t in ch33.items():
    ENTRIES[f"2_33_{v}"] = t
for v, t in ch34.items():
    ENTRIES[f"2_34_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Exodus foundational verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
