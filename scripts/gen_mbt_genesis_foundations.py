"""MBT generator: Genesis foundational chapters.

Book ID 1. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Genesis 1 (31 verses) — the creation week
- Genesis 2 (25 verses) — the Garden, the man, and the woman
- Genesis 3 (24 verses) — the Fall and the first promise (3:15)
- Genesis 12 (20 verses) — the call of Abram
- Genesis 15 (21 verses) — the covenant cut between the pieces

Total: 121 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 1 — the creation week
ch1 = {
    1: "In the beginning, God created the heavens and the earth.",
    2: "The earth was formless and empty, and darkness was over the face of the deep; and the Spirit of God was hovering over the face of the waters.",
    3: "And God said, \"Let there be light\" — and there was light.",
    4: "God saw the light, that it was good; and God divided the light from the darkness.",
    5: "God called the light Day, and the darkness He called Night. So the evening and the morning were the first day.",
    6: "Then God said, \"Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.\"",
    7: "Thus God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament; and it was so.",
    8: "And God called the firmament Heaven. So the evening and the morning were the second day.",
    9: "Then God said, \"Let the waters under the heavens be gathered together into one place, and let the dry land appear\"; and it was so.",
    10: "And God called the dry land Earth, and the gathering together of the waters He called Seas. And God saw that it was good.",
    11: "Then God said, \"Let the earth bring forth grass, the herb that yields seed, and the fruit tree that yields fruit according to its kind, whose seed is in itself, on the earth\"; and it was so.",
    12: "And the earth brought forth grass, the herb that yields seed according to its kind, and the tree that yields fruit, whose seed is in itself according to its kind. And God saw that it was good.",
    13: "So the evening and the morning were the third day.",
    14: "Then God said, \"Let there be lights in the firmament of the heavens to divide the day from the night; and let them be for signs and seasons, and for days and years;",
    15: "and let them be for lights in the firmament of the heavens to give light on the earth\"; and it was so.",
    16: "Then God made two great lights: the greater light to rule the day, and the lesser light to rule the night. He made the stars also.",
    17: "God set them in the firmament of the heavens to give light on the earth,",
    18: "and to rule over the day and over the night, and to divide the light from the darkness. And God saw that it was good.",
    19: "So the evening and the morning were the fourth day.",
    20: "Then God said, \"Let the waters abound with an abundance of living creatures, and let birds fly above the earth across the face of the firmament of the heavens.\"",
    21: "So God created great sea creatures and every living thing that moves, with which the waters abounded, according to their kind, and every winged bird according to its kind. And God saw that it was good.",
    22: "And God blessed them, saying, \"Be fruitful and multiply, and fill the waters in the seas, and let birds multiply on the earth.\"",
    23: "So the evening and the morning were the fifth day.",
    24: "Then God said, \"Let the earth bring forth the living creature according to its kind: cattle and creeping thing and beast of the earth, each according to its kind\"; and it was so.",
    25: "And God made the beast of the earth according to its kind, cattle according to its kind, and everything that creeps on the earth according to its kind. And God saw that it was good.",
    26: "Then God said, \"Let Us make man in Our image, according to Our likeness; let them have dominion over the fish of the sea, over the birds of the air, and over the cattle, over all the earth, and over every creeping thing that creeps on the earth.\"",
    27: "So God created man in His own image; in the image of God He created him; male and female He created them.",
    28: "Then God blessed them, and God said to them, \"Be fruitful and multiply; fill the earth and subdue it; have dominion over the fish of the sea, over the birds of the air, and over every living thing that moves on the earth.\"",
    29: "And God said, \"See, I have given you every herb that yields seed which is on the face of all the earth, and every tree whose fruit yields seed; to you it shall be for food.",
    30: "Also, to every beast of the earth, to every bird of the air, and to everything that creeps on the earth, in which there is life, I have given every green herb for food\"; and it was so.",
    31: "Then God saw everything that He had made, and indeed it was very good. So the evening and the morning were the sixth day.",
}

# Genesis 2 — the Garden, the man, the woman
ch2 = {
    1: "Thus the heavens and the earth, and all the host of them, were finished.",
    2: "And on the seventh day God ended His work which He had done, and He rested on the seventh day from all His work which He had done.",
    3: "Then God blessed the seventh day and sanctified it, because in it He rested from all His work which God had created and made.",
    4: "This is the history of the heavens and the earth when they were created, in the day that the LORD God made the earth and the heavens,",
    5: "before any plant of the field was in the earth and before any herb of the field had grown. For the LORD God had not caused it to rain on the earth, and there was no man to till the ground;",
    6: "but a mist went up from the earth and watered the whole face of the ground.",
    7: "And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living being.",
    8: "The LORD God planted a garden eastward in Eden, and there He put the man whom He had formed.",
    9: "And out of the ground the LORD God made every tree grow that is pleasant to the sight and good for food. The tree of life was also in the midst of the garden, and the tree of the knowledge of good and evil.",
    10: "Now a river went out of Eden to water the garden, and from there it parted and became four riverheads.",
    11: "The name of the first is Pishon; it skirts the whole land of Havilah, where there is gold.",
    12: "And the gold of that land is good. Bdellium and the onyx stone are there.",
    13: "The name of the second river is Gihon; it goes around the whole land of Cush.",
    14: "The name of the third river is Hiddekel; it goes toward the east of Assyria. The fourth river is the Euphrates.",
    15: "Then the LORD God took the man and put him in the garden of Eden to tend and keep it.",
    16: "And the LORD God commanded the man, saying, \"Of every tree of the garden you may freely eat;",
    17: "but of the tree of the knowledge of good and evil you shall not eat, for in the day that you eat of it you shall surely die.\"",
    18: "And the LORD God said, \"It is not good that man should be alone; I will make him a helper comparable to him.\"",
    19: "Out of the ground the LORD God formed every beast of the field and every bird of the air, and brought them to Adam to see what he would call them. And whatever Adam called each living creature, that was its name.",
    20: "So Adam gave names to all cattle, to the birds of the air, and to every beast of the field. But for Adam there was not found a helper comparable to him.",
    21: "And the LORD God caused a deep sleep to fall on Adam, and he slept; and He took one of his ribs, and closed up the flesh in its place.",
    22: "Then the rib which the LORD God had taken from man He made into a woman, and He brought her to the man.",
    23: "And Adam said: \"This is now bone of my bones and flesh of my flesh; she shall be called Woman, because she was taken out of Man.\"",
    24: "Therefore a man shall leave his father and mother and be joined to his wife, and they shall become one flesh.",
    25: "And they were both naked, the man and his wife, and were not ashamed.",
}

# Genesis 3 — the Fall
ch3 = {
    1: "Now the serpent was more cunning than any beast of the field which the LORD God had made. And he said to the woman, \"Has God indeed said, 'You shall not eat of every tree of the garden'?\"",
    2: "And the woman said to the serpent, \"We may eat the fruit of the trees of the garden;",
    3: "but of the fruit of the tree which is in the midst of the garden, God has said, 'You shall not eat it, nor shall you touch it, lest you die.'\"",
    4: "Then the serpent said to the woman, \"You will not surely die.",
    5: "For God knows that in the day you eat of it your eyes will be opened, and you will be like God, knowing good and evil.\"",
    6: "So when the woman saw that the tree was good for food, that it was pleasant to the eyes, and a tree desirable to make one wise, she took of its fruit and ate. She also gave to her husband with her, and he ate.",
    7: "Then the eyes of both of them were opened, and they knew that they were naked; and they sewed fig leaves together and made themselves coverings.",
    8: "And they heard the sound of the LORD God walking in the garden in the cool of the day, and Adam and his wife hid themselves from the presence of the LORD God among the trees of the garden.",
    9: "Then the LORD God called to Adam and said to him, \"Where are you?\"",
    10: "So he said, \"I heard Your voice in the garden, and I was afraid because I was naked; and I hid myself.\"",
    11: "And He said, \"Who told you that you were naked? Have you eaten from the tree of which I commanded you that you should not eat?\"",
    12: "Then the man said, \"The woman whom You gave to be with me, she gave me of the tree, and I ate.\"",
    13: "And the LORD God said to the woman, \"What is this you have done?\" The woman said, \"The serpent deceived me, and I ate.\"",
    14: "So the LORD God said to the serpent: \"Because you have done this, you are cursed more than all cattle, and more than every beast of the field; on your belly you shall go, and you shall eat dust all the days of your life.",
    15: "And I will put enmity between you and the woman, and between your seed and her Seed; He shall bruise your head, and you shall bruise His heel.\"",
    16: "To the woman He said: \"I will greatly multiply your sorrow and your conception; in pain you shall bring forth children; your desire shall be for your husband, and he shall rule over you.\"",
    17: "Then to Adam He said, \"Because you have heeded the voice of your wife, and have eaten from the tree of which I commanded you, saying, 'You shall not eat of it': cursed is the ground for your sake; in toil you shall eat of it all the days of your life.",
    18: "Both thorns and thistles it shall bring forth for you, and you shall eat the herb of the field.",
    19: "In the sweat of your face you shall eat bread till you return to the ground, for out of it you were taken; for dust you are, and to dust you shall return.\"",
    20: "And Adam called his wife's name Eve, because she was the mother of all living.",
    21: "Also for Adam and his wife the LORD God made tunics of skin, and clothed them.",
    22: "Then the LORD God said, \"Behold, the man has become like one of Us, to know good and evil. And now, lest he put out his hand and take also of the tree of life, and eat, and live forever\" —",
    23: "therefore the LORD God sent him out of the garden of Eden to till the ground from which he was taken.",
    24: "So He drove out the man; and He placed cherubim at the east of the garden of Eden, and a flaming sword which turned every way, to guard the way to the tree of life.",
}

# Genesis 12 — the call of Abram
ch12 = {
    1: "Now the LORD had said to Abram: \"Get out of your country, from your family and from your father's house, to a land that I will show you.",
    2: "I will make you a great nation; I will bless you and make your name great; and you shall be a blessing.",
    3: "I will bless those who bless you, and I will curse him who curses you; and in you all the families of the earth shall be blessed.\"",
    4: "So Abram departed as the LORD had spoken to him, and Lot went with him. And Abram was seventy-five years old when he departed from Haran.",
    5: "Then Abram took Sarai his wife and Lot his brother's son, and all their possessions that they had gathered, and the people whom they had acquired in Haran, and they departed to go to the land of Canaan. So they came to the land of Canaan.",
    6: "Abram passed through the land to the place of Shechem, as far as the terebinth tree of Moreh. And the Canaanites were then in the land.",
    7: "Then the LORD appeared to Abram and said, \"To your descendants I will give this land.\" And there he built an altar to the LORD, who had appeared to him.",
    8: "And he moved from there to the mountain east of Bethel, and he pitched his tent with Bethel on the west and Ai on the east; there he built an altar to the LORD and called on the name of the LORD.",
    9: "So Abram journeyed, going on still toward the South.",
    10: "Now there was a famine in the land, and Abram went down to Egypt to dwell there, for the famine was severe in the land.",
    11: "And it came to pass, when he was close to entering Egypt, that he said to Sarai his wife, \"Indeed I know that you are a woman of beautiful countenance.",
    12: "Therefore it will happen, when the Egyptians see you, that they will say, 'This is his wife'; and they will kill me, but they will let you live.",
    13: "Please say you are my sister, that it may be well with me for your sake, and that I may live because of you.\"",
    14: "So it was, when Abram came into Egypt, that the Egyptians saw the woman, that she was very beautiful.",
    15: "The princes of Pharaoh also saw her and commended her to Pharaoh. And the woman was taken to Pharaoh's house.",
    16: "He treated Abram well for her sake. He had sheep, oxen, male donkeys, male and female servants, female donkeys, and camels.",
    17: "But the LORD plagued Pharaoh and his house with great plagues because of Sarai, Abram's wife.",
    18: "And Pharaoh called Abram and said, \"What is this you have done to me? Why did you not tell me that she was your wife?",
    19: "Why did you say, 'She is my sister'? I might have taken her as my wife. Now therefore, here is your wife; take her and go your way.\"",
    20: "So Pharaoh commanded his men concerning him; and they sent him away, with his wife and all that he had.",
}

# Genesis 15 — the covenant cut between the pieces
ch15 = {
    1: "After these things the word of the LORD came to Abram in a vision, saying, \"Do not be afraid, Abram. I am your shield, your exceedingly great reward.\"",
    2: "But Abram said, \"Lord GOD, what will You give me, seeing I go childless, and the heir of my house is Eliezer of Damascus?\"",
    3: "Then Abram said, \"Look, You have given me no offspring; indeed one born in my house is my heir!\"",
    4: "And behold, the word of the LORD came to him, saying, \"This one shall not be your heir, but one who will come from your own body shall be your heir.\"",
    5: "Then He brought him outside and said, \"Look now toward heaven, and count the stars if you are able to number them.\" And He said to him, \"So shall your descendants be.\"",
    6: "And he believed in the LORD, and He accounted it to him for righteousness.",
    7: "Then He said to him, \"I am the LORD, who brought you out of Ur of the Chaldeans, to give you this land to inherit it.\"",
    8: "And he said, \"Lord GOD, how shall I know that I will inherit it?\"",
    9: "So He said to him, \"Bring Me a three-year-old heifer, a three-year-old female goat, a three-year-old ram, a turtledove, and a young pigeon.\"",
    10: "Then he brought all these to Him and cut them in two, down the middle, and placed each piece opposite the other; but he did not cut the birds in two.",
    11: "And when the vultures came down on the carcasses, Abram drove them away.",
    12: "Now when the sun was going down, a deep sleep fell upon Abram; and behold, horror and great darkness fell upon him.",
    13: "Then He said to Abram: \"Know certainly that your descendants will be strangers in a land that is not theirs, and will serve them, and they will afflict them four hundred years.",
    14: "And also the nation whom they serve I will judge; afterward they shall come out with great possessions.",
    15: "Now as for you, you shall go to your fathers in peace; you shall be buried at a good old age.",
    16: "But in the fourth generation they shall return here, for the iniquity of the Amorites is not yet complete.\"",
    17: "And it came to pass, when the sun went down and it was dark, that behold, there appeared a smoking oven and a burning torch that passed between those pieces.",
    18: "On the same day the LORD made a covenant with Abram, saying: \"To your descendants I have given this land, from the river of Egypt to the great river, the River Euphrates —",
    19: "the Kenites, the Kenezzites, the Kadmonites,",
    20: "the Hittites, the Perizzites, the Rephaim,",
    21: "the Amorites, the Canaanites, the Girgashites, and the Jebusites.\"",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"1_1_{v}"] = t
for v, t in ch2.items():
    ENTRIES[f"1_2_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"1_3_{v}"] = t
for v, t in ch12.items():
    ENTRIES[f"1_12_{v}"] = t
for v, t in ch15.items():
    ENTRIES[f"1_15_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Genesis foundational verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
