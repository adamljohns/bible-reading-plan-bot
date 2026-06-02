"""MBT generator: Genesis primeval narrative chapters.

Book ID 1. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Genesis 4 (26 verses) — Cain and Abel; the first murder
- Genesis 6 (22 verses) — corruption of the earth; Noah commissioned
- Genesis 9 (29 verses) — the Noahic covenant; the rainbow sign
- Genesis 11 (32 verses) — Babel; the genealogy to Abram

Total: 109 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 4 — Cain and Abel
ch4 = {
    1: "Now Adam knew Eve his wife, and she conceived and bore Cain, and said, \"I have acquired a man from the LORD.\"",
    2: "Then she bore again, this time his brother Abel. Now Abel was a keeper of sheep, but Cain was a tiller of the ground.",
    3: "And in the process of time it came to pass that Cain brought an offering of the fruit of the ground to the LORD.",
    4: "Abel also brought of the firstborn of his flock and of their fat. And the LORD respected Abel and his offering,",
    5: "but He did not respect Cain and his offering. And Cain was very angry, and his countenance fell.",
    6: "So the LORD said to Cain, \"Why are you angry? And why has your countenance fallen?",
    7: "If you do well, will you not be accepted? And if you do not do well, sin lies at the door. And its desire is for you, but you should rule over it.\"",
    8: "Now Cain talked with Abel his brother; and it came to pass, when they were in the field, that Cain rose up against Abel his brother and killed him.",
    9: "Then the LORD said to Cain, \"Where is Abel your brother?\" He said, \"I do not know. Am I my brother's keeper?\"",
    10: "And He said, \"What have you done? The voice of your brother's blood cries out to Me from the ground.",
    11: "So now you are cursed from the earth, which has opened its mouth to receive your brother's blood from your hand.",
    12: "When you till the ground, it shall no longer yield its strength to you. A fugitive and a vagabond you shall be on the earth.\"",
    13: "And Cain said to the LORD, \"My punishment is greater than I can bear!",
    14: "Surely You have driven me out this day from the face of the ground; I shall be hidden from Your face; I shall be a fugitive and a vagabond on the earth, and it will happen that anyone who finds me will kill me.\"",
    15: "And the LORD said to him, \"Therefore, whoever kills Cain, vengeance shall be taken on him sevenfold.\" And the LORD set a mark on Cain, lest anyone finding him should kill him.",
    16: "Then Cain went out from the presence of the LORD and dwelt in the land of Nod on the east of Eden.",
    17: "And Cain knew his wife, and she conceived and bore Enoch. And he built a city, and called the name of the city after the name of his son — Enoch.",
    18: "To Enoch was born Irad; and Irad begot Mehujael, and Mehujael begot Methushael, and Methushael begot Lamech.",
    19: "Then Lamech took for himself two wives: the name of one was Adah, and the name of the second was Zillah.",
    20: "And Adah bore Jabal. He was the father of those who dwell in tents and have livestock.",
    21: "His brother's name was Jubal. He was the father of all those who play the harp and flute.",
    22: "And as for Zillah, she also bore Tubal-Cain, an instructor of every craftsman in bronze and iron. And the sister of Tubal-Cain was Naamah.",
    23: "Then Lamech said to his wives: \"Adah and Zillah, hear my voice; wives of Lamech, listen to my speech! For I have killed a man for wounding me, even a young man for hurting me.",
    24: "If Cain shall be avenged sevenfold, then Lamech seventy-sevenfold.\"",
    25: "And Adam knew his wife again, and she bore a son and named him Seth, \"for God has appointed another seed for me instead of Abel, whom Cain killed.\"",
    26: "And as for Seth, to him also a son was born; and he named him Enosh. Then men began to call on the name of the LORD.",
}

# Genesis 6 — corruption of the earth, ark commission
ch6 = {
    1: "Now it came to pass, when men began to multiply on the face of the earth, and daughters were born to them,",
    2: "that the sons of God saw the daughters of men, that they were beautiful; and they took wives for themselves of all whom they chose.",
    3: "And the LORD said, \"My Spirit shall not strive with man forever, for he is indeed flesh; yet his days shall be one hundred and twenty years.\"",
    4: "There were giants on the earth in those days, and also afterward, when the sons of God came in to the daughters of men and they bore children to them. Those were the mighty men who were of old, men of renown.",
    5: "Then the LORD saw that the wickedness of man was great in the earth, and that every intent of the thoughts of his heart was only evil continually.",
    6: "And the LORD was sorry that He had made man on the earth, and He was grieved in His heart.",
    7: "So the LORD said, \"I will destroy man whom I have created from the face of the earth, both man and beast, creeping thing and birds of the air, for I am sorry that I have made them.\"",
    8: "But Noah found grace in the eyes of the LORD.",
    9: "This is the genealogy of Noah. Noah was a just man, blameless in his generations. Noah walked with God.",
    10: "And Noah begot three sons: Shem, Ham, and Japheth.",
    11: "The earth also was corrupt before God, and the earth was filled with violence.",
    12: "So God looked upon the earth, and indeed it was corrupt; for all flesh had corrupted their way on the earth.",
    13: "And God said to Noah, \"The end of all flesh has come before Me, for the earth is filled with violence through them; and behold, I will destroy them with the earth.",
    14: "Make yourself an ark of gopherwood; make rooms in the ark, and cover it inside and outside with pitch.",
    15: "And this is how you shall make it: The length of the ark shall be three hundred cubits, its width fifty cubits, and its height thirty cubits.",
    16: "You shall make a window for the ark, and you shall finish it to a cubit from above; and set the door of the ark in its side. You shall make it with lower, second, and third decks.",
    17: "And behold, I Myself am bringing floodwaters on the earth, to destroy from under heaven all flesh in which is the breath of life; everything that is on the earth shall die.",
    18: "But I will establish My covenant with you; and you shall go into the ark — you, your sons, your wife, and your sons' wives with you.",
    19: "And of every living thing of all flesh you shall bring two of every sort into the ark, to keep them alive with you; they shall be male and female.",
    20: "Of the birds after their kind, of animals after their kind, and of every creeping thing of the earth after its kind, two of every kind will come to you to keep them alive.",
    21: "And you shall take for yourself of all food that is eaten, and you shall gather it to yourself; and it shall be food for you and for them.\"",
    22: "Thus Noah did; according to all that God commanded him, so he did.",
}

# Genesis 9 — the Noahic covenant
ch9 = {
    1: "So God blessed Noah and his sons, and said to them: \"Be fruitful and multiply, and fill the earth.",
    2: "And the fear of you and the dread of you shall be on every beast of the earth, on every bird of the air, on all that move on the earth, and on all the fish of the sea. They are given into your hand.",
    3: "Every moving thing that lives shall be food for you. I have given you all things, even as the green herbs.",
    4: "But you shall not eat flesh with its life, that is, its blood.",
    5: "Surely for your lifeblood I will demand a reckoning; from the hand of every beast I will require it, and from the hand of man. From the hand of every man's brother I will require the life of man.",
    6: "Whoever sheds man's blood, by man his blood shall be shed; for in the image of God He made man.",
    7: "And as for you, be fruitful and multiply; bring forth abundantly in the earth and multiply in it.\"",
    8: "Then God spoke to Noah and to his sons with him, saying:",
    9: "\"And as for Me, behold, I establish My covenant with you and with your descendants after you,",
    10: "and with every living creature that is with you: the birds, the cattle, and every beast of the earth with you, of all that go out of the ark, every beast of the earth.",
    11: "Thus I establish My covenant with you: never again shall all flesh be cut off by the waters of the flood; never again shall there be a flood to destroy the earth.\"",
    12: "And God said: \"This is the sign of the covenant which I make between Me and you, and every living creature that is with you, for perpetual generations:",
    13: "I set My rainbow in the cloud, and it shall be for the sign of the covenant between Me and the earth.",
    14: "It shall be, when I bring a cloud over the earth, that the rainbow shall be seen in the cloud;",
    15: "and I will remember My covenant which is between Me and you and every living creature of all flesh; the waters shall never again become a flood to destroy all flesh.",
    16: "The rainbow shall be in the cloud, and I will look on it to remember the everlasting covenant between God and every living creature of all flesh that is on the earth.\"",
    17: "And God said to Noah, \"This is the sign of the covenant which I have established between Me and all flesh that is on the earth.\"",
    18: "Now the sons of Noah who went out of the ark were Shem, Ham, and Japheth. And Ham was the father of Canaan.",
    19: "These three were the sons of Noah, and from these the whole earth was populated.",
    20: "And Noah began to be a farmer, and he planted a vineyard.",
    21: "Then he drank of the wine and was drunk, and became uncovered in his tent.",
    22: "And Ham, the father of Canaan, saw the nakedness of his father, and told his two brothers outside.",
    23: "But Shem and Japheth took a garment, laid it on both their shoulders, and went backward and covered the nakedness of their father. Their faces were turned away, and they did not see their father's nakedness.",
    24: "So Noah awoke from his wine, and knew what his younger son had done to him.",
    25: "Then he said: \"Cursed be Canaan; a servant of servants he shall be to his brethren.\"",
    26: "And he said: \"Blessed be the LORD, the God of Shem, and may Canaan be his servant.",
    27: "May God enlarge Japheth, and may he dwell in the tents of Shem; and may Canaan be his servant.\"",
    28: "And Noah lived after the flood three hundred and fifty years.",
    29: "So all the days of Noah were nine hundred and fifty years; and he died.",
}

# Genesis 11 — Babel and the line to Abram
ch11 = {
    1: "Now the whole earth had one language and one speech.",
    2: "And it came to pass, as they journeyed from the east, that they found a plain in the land of Shinar, and they dwelt there.",
    3: "Then they said to one another, \"Come, let us make bricks and bake them thoroughly.\" They had brick for stone, and they had asphalt for mortar.",
    4: "And they said, \"Come, let us build ourselves a city, and a tower whose top is in the heavens; let us make a name for ourselves, lest we be scattered abroad over the face of the whole earth.\"",
    5: "But the LORD came down to see the city and the tower which the sons of men had built.",
    6: "And the LORD said, \"Indeed the people are one and they all have one language, and this is what they begin to do; now nothing that they propose to do will be withheld from them.",
    7: "Come, let Us go down and there confuse their language, that they may not understand one another's speech.\"",
    8: "So the LORD scattered them abroad from there over the face of all the earth, and they ceased building the city.",
    9: "Therefore its name is called Babel, because there the LORD confused the language of all the earth; and from there the LORD scattered them abroad over the face of all the earth.",
    10: "This is the genealogy of Shem: Shem was one hundred years old, and begot Arphaxad two years after the flood.",
    11: "After he begot Arphaxad, Shem lived five hundred years, and begot sons and daughters.",
    12: "Arphaxad lived thirty-five years, and begot Salah.",
    13: "After he begot Salah, Arphaxad lived four hundred and three years, and begot sons and daughters.",
    14: "Salah lived thirty years, and begot Eber.",
    15: "After he begot Eber, Salah lived four hundred and three years, and begot sons and daughters.",
    16: "Eber lived thirty-four years, and begot Peleg.",
    17: "After he begot Peleg, Eber lived four hundred and thirty years, and begot sons and daughters.",
    18: "Peleg lived thirty years, and begot Reu.",
    19: "After he begot Reu, Peleg lived two hundred and nine years, and begot sons and daughters.",
    20: "Reu lived thirty-two years, and begot Serug.",
    21: "After he begot Serug, Reu lived two hundred and seven years, and begot sons and daughters.",
    22: "Serug lived thirty years, and begot Nahor.",
    23: "After he begot Nahor, Serug lived two hundred years, and begot sons and daughters.",
    24: "Nahor lived twenty-nine years, and begot Terah.",
    25: "After he begot Terah, Nahor lived one hundred and nineteen years, and begot sons and daughters.",
    26: "Now Terah lived seventy years, and begot Abram, Nahor, and Haran.",
    27: "This is the genealogy of Terah: Terah begot Abram, Nahor, and Haran. Haran begot Lot.",
    28: "And Haran died before his father Terah in his native land, in Ur of the Chaldeans.",
    29: "Then Abram and Nahor took wives: the name of Abram's wife was Sarai, and the name of Nahor's wife, Milcah, the daughter of Haran the father of Milcah and the father of Iscah.",
    30: "But Sarai was barren; she had no child.",
    31: "And Terah took his son Abram and his grandson Lot, the son of Haran, and his daughter-in-law Sarai, his son Abram's wife, and they went out with them from Ur of the Chaldeans to go to the land of Canaan; and they came to Haran and dwelt there.",
    32: "So the days of Terah were two hundred and five years, and Terah died in Haran.",
}

ENTRIES = {}
for v, t in ch4.items():
    ENTRIES[f"1_4_{v}"] = t
for v, t in ch6.items():
    ENTRIES[f"1_6_{v}"] = t
for v, t in ch9.items():
    ENTRIES[f"1_9_{v}"] = t
for v, t in ch11.items():
    ENTRIES[f"1_11_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Genesis primeval verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
