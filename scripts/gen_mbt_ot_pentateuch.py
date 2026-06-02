"""MBT OT landmark passages — Pentateuch.

Genesis 1-3 (Creation and Fall), Exodus 3:1-15 (Burning Bush),
Exodus 20:1-17 (Ten Commandments), Deuteronomy 6:1-9 (Shema).
121 verses total.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 1 — Creation
gen_1 = {
    1: "In the beginning, God created the heavens and the earth.",
    2: "And the earth was formless and empty — darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters.",
    3: "And God said, \"Let there be light\" — and there was light.",
    4: "And God saw that the light was good. And God separated the light from the darkness.",
    5: "And God called the light Day, and the darkness He called Night. And there was evening and there was morning — one day.",
    6: "And God said, \"Let there be an expanse in the midst of the waters, and let it separate the waters from the waters.\"",
    7: "And God made the expanse, and separated the waters which were below the expanse from the waters which were above the expanse — and it was so.",
    8: "And God called the expanse Sky. And there was evening and there was morning — a second day.",
    9: "And God said, \"Let the waters under the sky be gathered into one place, and let the dry land appear\" — and it was so.",
    10: "And God called the dry land Earth, and the gathering of the waters He called Seas. And God saw that it was good.",
    11: "And God said, \"Let the earth sprout vegetation — plants yielding seed, and fruit trees bearing fruit with seed in them, after their kind, upon the earth\" — and it was so.",
    12: "And the earth brought forth vegetation: plants yielding seed after their kind, and trees bearing fruit with seed in them after their kind. And God saw that it was good.",
    13: "And there was evening and there was morning — a third day.",
    14: "And God said, \"Let there be lights in the expanse of the sky to separate the day from the night — and let them be for signs, and for seasons, and for days, and for years.",
    15: "And let them be for lights in the expanse of the sky, to give light upon the earth\" — and it was so.",
    16: "And God made the two great lights — the greater light to govern the day, and the lesser light to govern the night. He made the stars also.",
    17: "And God placed them in the expanse of the sky to give light upon the earth,",
    18: "and to govern the day and the night, and to separate the light from the darkness. And God saw that it was good.",
    19: "And there was evening and there was morning — a fourth day.",
    20: "And God said, \"Let the waters teem with swarms of living creatures — and let birds fly above the earth across the expanse of the sky.\"",
    21: "And God created the great sea creatures, and every living creature that moves — with which the waters swarmed — after their kind, and every winged bird after its kind. And God saw that it was good.",
    22: "And God blessed them, saying, \"Be fruitful and multiply, and fill the waters in the seas — and let the birds multiply on the earth.\"",
    23: "And there was evening and there was morning — a fifth day.",
    24: "And God said, \"Let the earth bring forth living creatures after their kind — cattle, and creeping things, and beasts of the earth, after their kind\" — and it was so.",
    25: "And God made the beasts of the earth after their kind, and the cattle after their kind, and everything that creeps upon the ground after its kind. And God saw that it was good.",
    26: "And God said, \"Let Us make man in Our image, after Our likeness — and let them rule over the fish of the sea, and over the birds of the sky, and over the cattle, and over all the earth, and over every creeping thing that creeps upon the earth.\"",
    27: "And God created man in His own image — in the image of God He created him; male and female He created them.",
    28: "And God blessed them. And God said to them, \"Be fruitful and multiply, and fill the earth, and subdue it — and rule over the fish of the sea, and over the birds of the sky, and over every living thing that moves upon the earth.\"",
    29: "And God said, \"Behold, I have given you every plant yielding seed that is upon the surface of all the earth, and every tree which has fruit yielding seed — it shall be food for you.",
    30: "And to every beast of the earth, and to every bird of the sky, and to everything that moves on the earth which has life, I have given every green plant for food\" — and it was so.",
    31: "And God saw all that He had made — and behold, it was very good. And there was evening and there was morning — the sixth day.",
}

# Genesis 2 — Garden of Eden
gen_2 = {
    1: "Thus the heavens and the earth were completed, and all their hosts.",
    2: "And by the seventh day God completed His work which He had done. And He rested on the seventh day from all His work which He had done.",
    3: "Then God blessed the seventh day and sanctified it — because in it He rested from all His work which God had created and made.",
    4: "These are the generations of the heavens and the earth when they were created — in the day that the LORD God made earth and heaven.",
    5: "Now no shrub of the field was yet in the earth, and no plant of the field had yet sprouted — for the LORD God had not sent rain upon the earth, and there was no man to cultivate the ground.",
    6: "But a mist used to rise from the earth, and water the whole surface of the ground.",
    7: "Then the LORD God formed man of dust from the ground, and breathed into his nostrils the breath of life — and man became a living being.",
    8: "And the LORD God planted a garden eastward in Eden — and there He placed the man whom He had formed.",
    9: "And out of the ground the LORD God caused to grow every tree that is pleasing to the sight and good for food — the tree of life also in the midst of the garden, and the tree of the knowledge of good and evil.",
    10: "Now a river flowed out of Eden to water the garden — and from there it divided and became four rivers.",
    11: "The name of the first is Pishon — it flows around the whole land of Havilah, where there is gold.",
    12: "And the gold of that land is good — the bdellium and the onyx stone are there.",
    13: "And the name of the second river is Gihon — it flows around the whole land of Cush.",
    14: "And the name of the third river is Tigris — it flows east of Assyria. And the fourth river is the Euphrates.",
    15: "Then the LORD God took the man and put him into the garden of Eden to cultivate it and to keep it.",
    16: "And the LORD God commanded the man, saying, \"From any tree of the garden you may eat freely —",
    17: "but from the tree of the knowledge of good and evil you shall not eat. For in the day that you eat from it, you shall surely die.\"",
    18: "Then the LORD God said, \"It is not good for the man to be alone. I will make him a helper suitable for him.\"",
    19: "And out of the ground the LORD God formed every beast of the field and every bird of the sky, and brought them to the man to see what he would call them. And whatever the man called a living creature, that was its name.",
    20: "And the man gave names to all the cattle, and to the birds of the sky, and to every beast of the field — but for Adam there was not found a helper suitable for him.",
    21: "So the LORD God caused a deep sleep to fall upon the man, and he slept. Then He took one of his ribs, and closed up the flesh at that place.",
    22: "And the LORD God fashioned into a woman the rib which He had taken from the man, and brought her to the man.",
    23: "And the man said, \"This is now bone of my bones, and flesh of my flesh — she shall be called Woman, because she was taken out of Man.\"",
    24: "For this cause a man shall leave his father and his mother, and shall cleave to his wife — and they shall become one flesh.",
    25: "And the man and his wife were both naked and were not ashamed.",
}

# Genesis 3 — The Fall
gen_3 = {
    1: "Now the serpent was more crafty than any beast of the field which the LORD God had made. And he said to the woman, \"Indeed, has God said, 'You shall not eat from any tree of the garden'?\"",
    2: "And the woman said to the serpent, \"From the fruit of the trees of the garden we may eat —",
    3: "but from the fruit of the tree which is in the middle of the garden, God has said, 'You shall not eat from it, or touch it, lest you die.'\"",
    4: "And the serpent said to the woman, \"You surely shall not die!",
    5: "For God knows that in the day you eat from it your eyes will be opened, and you will be like God — knowing good and evil.\"",
    6: "When the woman saw that the tree was good for food, and that it was a delight to the eyes, and that the tree was desirable to make one wise, she took from its fruit and ate. And she gave also to her husband with her, and he ate.",
    7: "Then the eyes of both of them were opened, and they knew that they were naked — and they sewed fig leaves together, and made themselves loin coverings.",
    8: "And they heard the sound of the LORD God walking in the garden in the cool of the day. And the man and his wife hid themselves from the presence of the LORD God among the trees of the garden.",
    9: "Then the LORD God called to the man, and said to him, \"Where are you?\"",
    10: "And he said, \"I heard the sound of You in the garden, and I was afraid because I was naked — so I hid myself.\"",
    11: "And He said, \"Who told you that you were naked? Have you eaten from the tree of which I commanded you not to eat?\"",
    12: "And the man said, \"The woman whom You gave to be with me — she gave me from the tree, and I ate.\"",
    13: "Then the LORD God said to the woman, \"What is this you have done?\" And the woman said, \"The serpent deceived me — and I ate.\"",
    14: "And the LORD God said to the serpent, \"Because you have done this, cursed are you more than all cattle, and more than every beast of the field. On your belly shall you go, and dust shall you eat all the days of your life.",
    15: "And I will put enmity between you and the woman — and between your seed and her Seed. He shall bruise your head, and you shall bruise His heel.\"",
    16: "To the woman He said, \"I will greatly multiply your pain in childbirth — in pain you shall bring forth children. Yet your desire shall be for your husband, and he shall rule over you.\"",
    17: "Then to Adam He said, \"Because you have listened to the voice of your wife, and have eaten from the tree about which I commanded you, saying, 'You shall not eat from it' — cursed is the ground because of you. In toil you shall eat of it all the days of your life.",
    18: "Both thorns and thistles it shall grow for you — and you shall eat the plants of the field.",
    19: "By the sweat of your face you shall eat bread, till you return to the ground — because from it you were taken. For you are dust, and to dust you shall return.\"",
    20: "Now the man called his wife's name Eve, because she was the mother of all the living.",
    21: "And the LORD God made garments of skin for Adam and his wife, and clothed them.",
    22: "Then the LORD God said, \"Behold, the man has become like one of Us — knowing good and evil. And now, lest he stretch out his hand, and take also from the tree of life, and eat, and live forever\" —",
    23: "therefore the LORD God sent him out from the garden of Eden, to cultivate the ground from which he was taken.",
    24: "So He drove the man out — and at the east of the garden of Eden He stationed the cherubim, and the flaming sword which turned every direction, to guard the way to the tree of life.",
}

# Exodus 3:1-15 — Burning Bush + Divine Name
exod_3 = {
    1: "Now Moses was pasturing the flock of Jethro his father-in-law, the priest of Midian. And he led the flock to the west side of the wilderness, and came to Horeb, the mountain of God.",
    2: "And the angel of the LORD appeared to him in a blazing fire from the midst of a bush. And he looked, and behold, the bush was burning with fire, yet the bush was not consumed.",
    3: "So Moses said, \"I must turn aside now and see this marvelous sight — why the bush is not burned up.\"",
    4: "When the LORD saw that he turned aside to look, God called to him from the midst of the bush, and said, \"Moses, Moses!\" And he said, \"Here I am.\"",
    5: "Then He said, \"Do not come near here — remove your sandals from your feet, for the place on which you are standing is holy ground.\"",
    6: "He said also, \"I am the God of your father — the God of Abraham, the God of Isaac, and the God of Jacob.\" Then Moses hid his face, for he was afraid to look at God.",
    7: "And the LORD said, \"I have surely seen the affliction of My people who are in Egypt, and have given heed to their cry because of their taskmasters — for I am aware of their sufferings.",
    8: "So I have come down to deliver them from the power of the Egyptians, and to bring them up from that land to a good and spacious land — to a land flowing with milk and honey, to the place of the Canaanite and the Hittite and the Amorite and the Perizzite and the Hivite and the Jebusite.",
    9: "And now, behold, the cry of the sons of Israel has come to Me — furthermore, I have seen the oppression with which the Egyptians are oppressing them.",
    10: "Therefore, come now, and I will send you to Pharaoh, so that you may bring My people, the sons of Israel, out of Egypt.\"",
    11: "But Moses said to God, \"Who am I, that I should go to Pharaoh, and that I should bring the sons of Israel out of Egypt?\"",
    12: "And He said, \"Certainly I will be with you, and this shall be the sign to you that it is I who have sent you: when you have brought the people out of Egypt, you shall worship God at this mountain.\"",
    13: "Then Moses said to God, \"Behold, I am going to the sons of Israel, and I shall say to them, 'The God of your fathers has sent me to you.' Now they may say to me, 'What is His name?' What shall I say to them?\"",
    14: "And God said to Moses, \"I AM WHO I AM.\" And He said, \"Thus you shall say to the sons of Israel — 'I AM has sent me to you.'\"",
    15: "And God, furthermore, said to Moses, \"Thus you shall say to the sons of Israel — 'The LORD, the God of your fathers, the God of Abraham, the God of Isaac, and the God of Jacob, has sent me to you.' This is My name forever, and this is My memorial-name to all generations.",
}

# Exodus 20:1-17 — Decalogue
exod_20 = {
    1: "Then God spoke all these words, saying,",
    2: "\"I am the LORD your God, who brought you out of the land of Egypt, out of the house of slavery.",
    3: "You shall have no other gods before Me.",
    4: "You shall not make for yourself an idol — or any likeness of what is in heaven above, or on the earth beneath, or in the water under the earth.",
    5: "You shall not worship them, or serve them — for I, the LORD your God, am a jealous God, visiting the iniquity of the fathers on the children, on the third and the fourth generations of those who hate Me,",
    6: "but showing lovingkindness to thousands, to those who love Me and keep My commandments.",
    7: "You shall not take the name of the LORD your God in vain — for the LORD will not leave him unpunished who takes His name in vain.",
    8: "Remember the Sabbath day, to keep it holy.",
    9: "Six days you shall labor and do all your work,",
    10: "but the seventh day is a Sabbath of the LORD your God — in it you shall not do any work, you or your son or your daughter, your male or your female servant, or your cattle, or your sojourner who stays with you.",
    11: "For in six days the LORD made the heavens and the earth, the sea and all that is in them, and rested on the seventh day. Therefore the LORD blessed the Sabbath day and made it holy.",
    12: "Honor your father and your mother — that your days may be prolonged in the land which the LORD your God gives you.",
    13: "You shall not murder.",
    14: "You shall not commit adultery.",
    15: "You shall not steal.",
    16: "You shall not bear false witness against your neighbor.",
    17: "You shall not covet your neighbor's house. You shall not covet your neighbor's wife, or his male servant or his female servant, or his ox or his donkey, or anything that belongs to your neighbor.",
}

# Deuteronomy 6:1-9 — The Shema
deut_6 = {
    1: "Now this is the commandment — the statutes and the judgments — which the LORD your God has commanded me to teach you, that you might do them in the land where you are going over to possess it.",
    2: "So that you and your son and your grandson might fear the LORD your God — to keep all His statutes and His commandments which I command you, all the days of your life, and that your days may be prolonged.",
    3: "O Israel, you should listen and be careful to do it — that it may be well with you, and that you may multiply greatly, just as the LORD, the God of your fathers, has promised you, in a land flowing with milk and honey.",
    4: "Hear, O Israel — the LORD is our God, the LORD is one!",
    5: "And you shall love the LORD your God with all your heart, and with all your soul, and with all your might.",
    6: "And these words, which I am commanding you today, shall be on your heart.",
    7: "And you shall teach them diligently to your sons, and shall talk of them when you sit in your house, and when you walk by the way, and when you lie down, and when you rise up.",
    8: "And you shall bind them as a sign on your hand, and they shall be as frontals on your forehead.",
    9: "And you shall write them on the doorposts of your house, and on your gates.",
}

ENTRIES = {}
for v, t in gen_1.items():  ENTRIES[f"1_1_{v}"] = t
for v, t in gen_2.items():  ENTRIES[f"1_2_{v}"] = t
for v, t in gen_3.items():  ENTRIES[f"1_3_{v}"] = t
for v, t in exod_3.items(): ENTRIES[f"2_3_{v}"] = t
for v, t in exod_20.items(): ENTRIES[f"2_20_{v}"] = t
for v, t in deut_6.items():  ENTRIES[f"5_6_{v}"] = t

def main():
    print(f"MBT OT Pentateuch landmark verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json updated.")

if __name__ == "__main__":
    main()
