"""MBT generator: Genesis Abraham expansion (batch 2).

Book ID 1. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Genesis 13 (18 verses) — Abram and Lot separate; lift up your eyes
- Genesis 17 (27 verses) — covenant of circumcision; new names
- Genesis 18 (33 verses) — three visitors; Sarah's laughter; Sodom intercession

Total: 78 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 13 — Abram and Lot separate
ch13 = {
    1: "Then Abram went up from Egypt, he and his wife and all that he had, and Lot with him, to the South.",
    2: "Abram was very rich in livestock, in silver, and in gold.",
    3: "And he went on his journey from the South as far as Bethel, to the place where his tent had been at the beginning, between Bethel and Ai,",
    4: "to the place of the altar which he had made there at first. And there Abram called on the name of the LORD.",
    5: "Lot also, who went with Abram, had flocks and herds and tents.",
    6: "Now the land was not able to support them, that they might dwell together, for their possessions were so great that they could not dwell together.",
    7: "And there was strife between the herdsmen of Abram's livestock and the herdsmen of Lot's livestock. The Canaanites and the Perizzites then dwelt in the land.",
    8: "So Abram said to Lot, \"Please let there be no strife between you and me, and between my herdsmen and your herdsmen; for we are brethren.",
    9: "Is not the whole land before you? Please separate from me. If you take the left, then I will go to the right; or, if you go to the right, then I will go to the left.\"",
    10: "And Lot lifted his eyes and saw all the plain of Jordan, that it was well watered everywhere (before the LORD destroyed Sodom and Gomorrah) like the garden of the LORD, like the land of Egypt as you go toward Zoar.",
    11: "Then Lot chose for himself all the plain of Jordan, and Lot journeyed east. And they separated from each other.",
    12: "Abram dwelt in the land of Canaan, and Lot dwelt in the cities of the plain and pitched his tent even as far as Sodom.",
    13: "But the men of Sodom were exceedingly wicked and sinful against the LORD.",
    14: "And the LORD said to Abram, after Lot had separated from him: \"Lift your eyes now and look from the place where you are — northward, southward, eastward, and westward;",
    15: "for all the land which you see I give to you and your descendants forever.",
    16: "And I will make your descendants as the dust of the earth; so that if a man could number the dust of the earth, then your descendants also could be numbered.",
    17: "Arise, walk in the land through its length and its width, for I give it to you.\"",
    18: "Then Abram moved his tent, and went and dwelt by the terebinth trees of Mamre, which are in Hebron, and there he built an altar to the LORD.",
}

# Genesis 17 — covenant of circumcision; new names
ch17 = {
    1: "When Abram was ninety-nine years old, the LORD appeared to Abram and said to him, \"I am Almighty God; walk before Me and be blameless.",
    2: "And I will make My covenant between Me and you, and will multiply you exceedingly.\"",
    3: "Then Abram fell on his face, and God talked with him, saying:",
    4: "\"As for Me, behold, My covenant is with you, and you shall be a father of many nations.",
    5: "No longer shall your name be called Abram, but your name shall be Abraham; for I have made you a father of many nations.",
    6: "I will make you exceedingly fruitful; and I will make nations of you, and kings shall come from you.",
    7: "And I will establish My covenant between Me and you and your descendants after you in their generations, for an everlasting covenant, to be God to you and your descendants after you.",
    8: "Also I give to you and your descendants after you the land in which you are a stranger, all the land of Canaan, as an everlasting possession; and I will be their God.\"",
    9: "And God said to Abraham: \"As for you, you shall keep My covenant, you and your descendants after you throughout their generations.",
    10: "This is My covenant which you shall keep, between Me and you and your descendants after you: Every male child among you shall be circumcised;",
    11: "and you shall be circumcised in the flesh of your foreskins, and it shall be a sign of the covenant between Me and you.",
    12: "He who is eight days old among you shall be circumcised, every male child in your generations, he who is born in your house or bought with money from any foreigner who is not your descendant.",
    13: "He who is born in your house and he who is bought with your money must be circumcised, and My covenant shall be in your flesh for an everlasting covenant.",
    14: "And the uncircumcised male child, who is not circumcised in the flesh of his foreskin, that person shall be cut off from his people; he has broken My covenant.\"",
    15: "Then God said to Abraham, \"As for Sarai your wife, you shall not call her name Sarai, but Sarah shall be her name.",
    16: "And I will bless her and also give you a son by her; then I will bless her, and she shall be a mother of nations; kings of peoples shall be from her.\"",
    17: "Then Abraham fell on his face and laughed, and said in his heart, \"Shall a child be born to a man who is one hundred years old? And shall Sarah, who is ninety years old, bear a child?\"",
    18: "And Abraham said to God, \"Oh, that Ishmael might live before You!\"",
    19: "Then God said: \"No, Sarah your wife shall bear you a son, and you shall call his name Isaac; I will establish My covenant with him for an everlasting covenant, and with his descendants after him.",
    20: "And as for Ishmael, I have heard you. Behold, I have blessed him, and will make him fruitful, and will multiply him exceedingly. He shall beget twelve princes, and I will make him a great nation.",
    21: "But My covenant I will establish with Isaac, whom Sarah shall bear to you at this set time next year.\"",
    22: "Then He finished talking with him, and God went up from Abraham.",
    23: "So Abraham took Ishmael his son, all who were born in his house and all who were bought with his money, every male among the men of Abraham's house, and circumcised the flesh of their foreskins that very same day, as God had said to him.",
    24: "Abraham was ninety-nine years old when he was circumcised in the flesh of his foreskin.",
    25: "And Ishmael his son was thirteen years old when he was circumcised in the flesh of his foreskin.",
    26: "That very same day Abraham was circumcised, and his son Ishmael;",
    27: "and all the men of his house, born in the house or bought with money from a foreigner, were circumcised with him.",
}

# Genesis 18 — three visitors; Sarah's laughter; Sodom intercession
ch18 = {
    1: "Then the LORD appeared to him by the terebinth trees of Mamre, as he was sitting in the tent door in the heat of the day.",
    2: "So he lifted his eyes and looked, and behold, three men were standing by him; and when he saw them, he ran from the tent door to meet them, and bowed himself to the ground,",
    3: "and said, \"My Lord, if I have now found favor in Your sight, do not pass on by Your servant.",
    4: "Please let a little water be brought, and wash your feet, and rest yourselves under the tree.",
    5: "And I will bring a morsel of bread, that you may refresh your hearts. After that you may pass by, inasmuch as you have come to your servant.\" They said, \"Do as you have said.\"",
    6: "So Abraham hurried into the tent to Sarah and said, \"Quickly, make ready three measures of fine meal; knead it and make cakes.\"",
    7: "And Abraham ran to the herd, took a tender and good calf, gave it to a young man, and he hastened to prepare it.",
    8: "So he took butter and milk and the calf which he had prepared, and set it before them; and he stood by them under the tree as they ate.",
    9: "Then they said to him, \"Where is Sarah your wife?\" So he said, \"Here, in the tent.\"",
    10: "And He said, \"I will certainly return to you according to the time of life, and behold, Sarah your wife shall have a son.\" (Sarah was listening in the tent door which was behind Him.)",
    11: "Now Abraham and Sarah were old, well advanced in age; and Sarah had passed the age of childbearing.",
    12: "Therefore Sarah laughed within herself, saying, \"After I have grown old, shall I have pleasure, my lord being old also?\"",
    13: "And the LORD said to Abraham, \"Why did Sarah laugh, saying, 'Shall I surely bear a child, since I am old?'",
    14: "Is anything too hard for the LORD? At the appointed time I will return to you, according to the time of life, and Sarah shall have a son.\"",
    15: "But Sarah denied it, saying, \"I did not laugh,\" for she was afraid. And He said, \"No, but you did laugh!\"",
    16: "Then the men rose from there and looked toward Sodom, and Abraham went with them to send them on the way.",
    17: "And the LORD said, \"Shall I hide from Abraham what I am doing,",
    18: "since Abraham shall surely become a great and mighty nation, and all the nations of the earth shall be blessed in him?",
    19: "For I have known him, in order that he may command his children and his household after him, that they keep the way of the LORD, to do righteousness and justice, that the LORD may bring to Abraham what He has spoken to him.\"",
    20: "And the LORD said, \"Because the outcry against Sodom and Gomorrah is great, and because their sin is very grave,",
    21: "I will go down now and see whether they have done altogether according to the outcry against it that has come to Me; and if not, I will know.\"",
    22: "Then the men turned away from there and went toward Sodom, but Abraham still stood before the LORD.",
    23: "And Abraham came near and said, \"Would You also destroy the righteous with the wicked?",
    24: "Suppose there were fifty righteous within the city; would You also destroy the place and not spare it for the fifty righteous that were in it?",
    25: "Far be it from You to do such a thing as this, to slay the righteous with the wicked, so that the righteous should be as the wicked; far be it from You! Shall not the Judge of all the earth do right?\"",
    26: "So the LORD said, \"If I find in Sodom fifty righteous within the city, then I will spare all the place for their sakes.\"",
    27: "Then Abraham answered and said, \"Indeed now, I who am but dust and ashes have taken it upon myself to speak to the Lord:",
    28: "Suppose there were five less than the fifty righteous; would You destroy all of the city for lack of five?\" So He said, \"If I find there forty-five, I will not destroy it.\"",
    29: "And he spoke to Him yet again and said, \"Suppose there should be forty found there?\" So He said, \"I will not do it for the sake of forty.\"",
    30: "Then he said, \"Let not the Lord be angry, and I will speak: Suppose thirty should be found there?\" So He said, \"I will not do it if I find thirty there.\"",
    31: "And he said, \"Indeed now, I have taken it upon myself to speak to the Lord: Suppose twenty should be found there?\" So He said, \"I will not destroy it for the sake of twenty.\"",
    32: "Then he said, \"Let not the Lord be angry, and I will speak but once more: Suppose ten should be found there?\" And He said, \"I will not destroy it for the sake of ten.\"",
    33: "So the LORD went His way as soon as He had finished speaking with Abraham; and Abraham returned to his place.",
}

ENTRIES = {}
for v, t in ch13.items():
    ENTRIES[f"1_13_{v}"] = t
for v, t in ch17.items():
    ENTRIES[f"1_17_{v}"] = t
for v, t in ch18.items():
    ENTRIES[f"1_18_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Genesis Abraham expansion verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
