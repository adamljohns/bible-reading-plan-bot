"""MBT generator: Ezekiel landmark chapters.

Book ID 26. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Ezekiel 1 (28 verses) — the throne vision; the four living creatures
- Ezekiel 36 (38 verses) — the new heart and new spirit promise
- Ezekiel 47 (23 verses) — the river flowing from the temple

Total: 89 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Ezekiel 1 — the throne vision
ch1 = {
    1: "Now it came to pass in the thirtieth year, in the fourth month, on the fifth day of the month, as I was among the captives by the River Chebar, that the heavens were opened and I saw visions of God.",
    2: "On the fifth day of the month, which was in the fifth year of King Jehoiachin's captivity,",
    3: "the word of the LORD came expressly to Ezekiel the priest, the son of Buzi, in the land of the Chaldeans by the River Chebar; and the hand of the LORD was upon him there.",
    4: "Then I looked, and behold, a whirlwind was coming out of the north, a great cloud with raging fire engulfing itself; and brightness was all around it and radiating out of its midst like the color of amber, out of the midst of the fire.",
    5: "Also from within it came the likeness of four living creatures. And this was their appearance: they had the likeness of a man.",
    6: "Each one had four faces, and each one had four wings.",
    7: "Their legs were straight, and the soles of their feet were like the soles of calves' feet. They sparkled like the color of burnished bronze.",
    8: "The hands of a man were under their wings on their four sides; and each of the four had faces and wings.",
    9: "Their wings touched one another. The creatures did not turn when they went, but each one went straight forward.",
    10: "As for the likeness of their faces, each had the face of a man; each of the four had the face of a lion on the right side, each of the four had the face of an ox on the left side, and each of the four had the face of an eagle.",
    11: "Thus were their faces. Their wings stretched upward; two wings of each one touched one another, and two covered their bodies.",
    12: "And each one went straight forward; they went wherever the spirit wanted to go, and they did not turn when they went.",
    13: "As for the likeness of the living creatures, their appearance was like burning coals of fire, like the appearance of torches going back and forth among the living creatures. The fire was bright, and out of the fire went lightning.",
    14: "And the living creatures ran back and forth, in appearance like a flash of lightning.",
    15: "Now as I looked at the living creatures, behold, a wheel was on the earth beside each living creature with its four faces.",
    16: "The appearance of the wheels and their workings was like the color of beryl, and all four had the same likeness. The appearance of their workings was, as it were, a wheel in the middle of a wheel.",
    17: "When they moved, they went toward any one of four directions; they did not turn aside when they went.",
    18: "As for their rims, they were so high they were awesome; and their rims were full of eyes, all around the four of them.",
    19: "When the living creatures went, the wheels went beside them; and when the living creatures were lifted up from the earth, the wheels were lifted up.",
    20: "Wherever the spirit wanted to go, they went, because there the spirit went; and the wheels were lifted together with them, for the spirit of the living creatures was in the wheels.",
    21: "When those went, these went; when those stood, these stood; and when those were lifted up from the earth, the wheels were lifted up together with them, for the spirit of the living creatures was in the wheels.",
    22: "The likeness of the firmament above the heads of the living creatures was like the color of an awesome crystal, stretched out over their heads.",
    23: "And under the firmament their wings spread out straight, one toward another. Each one had two which covered one side, and each one had two which covered the other side of the body.",
    24: "When they went, I heard the noise of their wings, like the noise of many waters, like the voice of the Almighty, a tumult like the noise of an army; and when they stood still, they let down their wings.",
    25: "A voice came from above the firmament that was over their heads; whenever they stood, they let down their wings.",
    26: "And above the firmament over their heads was the likeness of a throne, in appearance like a sapphire stone; on the likeness of the throne was a likeness with the appearance of a Man high above it.",
    27: "Also from the appearance of His waist and upward I saw, as it were, the color of amber with the appearance of fire all around within it; and from the appearance of His waist and downward I saw, as it were, the appearance of fire with brightness all around.",
    28: "Like the appearance of a rainbow in a cloud on a rainy day, so was the appearance of the brightness all around it. This was the appearance of the likeness of the glory of the LORD. So when I saw it, I fell on my face, and I heard a voice of One speaking.",
}

# Ezekiel 36 — the new heart and new spirit
ch36 = {
    1: "\"And you, son of man, prophesy to the mountains of Israel, and say, 'O mountains of Israel, hear the word of the LORD!",
    2: "Thus says the Lord GOD: \"Because the enemy has said of you, 'Aha! The ancient heights have become our possession,'\"'",
    3: "therefore prophesy, and say, 'Thus says the Lord GOD: \"Because they made you desolate and swallowed you up on every side, so that you became the possession of the rest of the nations, and you are taken up by the lips of talkers and slandered by the people\" —",
    4: "therefore, O mountains of Israel, hear the word of the Lord GOD! Thus says the Lord GOD to the mountains, the hills, the rivers, the valleys, the desolate wastes, and the cities that have been forsaken, which became plunder and mockery to the rest of the nations all around —",
    5: "therefore thus says the Lord GOD: \"Surely I have spoken in My burning jealousy against the rest of the nations and against all Edom, who gave My land to themselves as a possession, with whole-hearted joy and spiteful minds, in order to plunder its open country.\"'",
    6: "Therefore prophesy concerning the land of Israel, and say to the mountains, the hills, the rivers, and the valleys, 'Thus says the Lord GOD: \"Behold, I have spoken in My jealousy and My fury, because you have borne the shame of the nations.\"",
    7: "Therefore thus says the Lord GOD: \"I have raised My hand in an oath that surely the nations that are around you shall bear their own shame.",
    8: "But you, O mountains of Israel, you shall shoot forth your branches and yield your fruit to My people Israel, for they are about to come.",
    9: "For indeed I am for you, and I will turn to you, and you shall be tilled and sown.",
    10: "I will multiply men upon you, all the house of Israel, all of it; and the cities shall be inhabited and the ruins rebuilt.",
    11: "I will multiply upon you man and beast; and they shall increase and bear young; I will make you inhabited as in former times, and do better for you than at your beginnings. Then you shall know that I am the LORD.",
    12: "Yes, I will cause men to walk on you, My people Israel; they shall take possession of you, and you shall be their inheritance; no more shall you bereave them of children.\"'",
    13: "Thus says the Lord GOD: \"Because they say to you, 'You devour men and bereave your nation of children,'",
    14: "therefore you shall devour men no more, nor bereave your nation anymore,\" says the Lord GOD.",
    15: "\"Nor will I let you hear the taunts of the nations anymore, nor bear the reproach of the peoples anymore, nor shall you cause your nation to stumble anymore,\" says the Lord GOD.\"",
    16: "Moreover the word of the LORD came to me, saying:",
    17: "\"Son of man, when the house of Israel dwelt in their own land, they defiled it by their own ways and deeds; to Me their way was like the uncleanness of a woman in her customary impurity.",
    18: "Therefore I poured out My fury on them for the blood they had shed on the land, and for their idols with which they had defiled it.",
    19: "So I scattered them among the nations, and they were dispersed throughout the countries; I judged them according to their ways and their deeds.",
    20: "When they came to the nations, wherever they went, they profaned My holy name — when they said of them, 'These are the people of the LORD, and yet they have gone out of His land.'",
    21: "But I had concern for My holy name, which the house of Israel had profaned among the nations wherever they went.",
    22: "\"Therefore say to the house of Israel, 'Thus says the Lord GOD: \"I do not do this for your sake, O house of Israel, but for My holy name's sake, which you have profaned among the nations wherever you went.",
    23: "And I will sanctify My great name, which has been profaned among the nations, which you have profaned in their midst; and the nations shall know that I am the LORD,\" says the Lord GOD, \"when I am hallowed in you before their eyes.",
    24: "For I will take you from among the nations, gather you out of all countries, and bring you into your own land.",
    25: "Then I will sprinkle clean water on you, and you shall be clean; I will cleanse you from all your filthiness and from all your idols.",
    26: "I will give you a new heart and put a new spirit within you; I will take the heart of stone out of your flesh and give you a heart of flesh.",
    27: "I will put My Spirit within you and cause you to walk in My statutes, and you will keep My judgments and do them.",
    28: "Then you shall dwell in the land that I gave to your fathers; you shall be My people, and I will be your God.",
    29: "I will deliver you from all your uncleannesses. I will call for the grain and multiply it, and bring no famine upon you.",
    30: "And I will multiply the fruit of your trees and the increase of your fields, so that you need never again bear the reproach of famine among the nations.",
    31: "Then you will remember your evil ways and your deeds that were not good; and you will loathe yourselves in your own sight, for your iniquities and your abominations.",
    32: "Not for your sake do I do this,\" says the Lord GOD, \"let it be known to you. Be ashamed and confounded for your own ways, O house of Israel!\"'",
    33: "Thus says the Lord GOD: \"On the day that I cleanse you from all your iniquities, I will also enable you to dwell in the cities, and the ruins shall be rebuilt.",
    34: "The desolate land shall be tilled instead of lying desolate in the sight of all who pass by.",
    35: "So they will say, 'This land that was desolate has become like the garden of Eden; and the wasted, desolate, and ruined cities are now fortified and inhabited.'",
    36: "Then the nations which are left all around you shall know that I, the LORD, have rebuilt the ruined places and planted what was desolate. I, the LORD, have spoken it, and I will do it.\"",
    37: "Thus says the Lord GOD: \"I will also let the house of Israel inquire of Me to do this for them: I will increase their men like a flock.",
    38: "Like a flock offered as holy sacrifices, like the flock at Jerusalem on its feast days, so shall the ruined cities be filled with flocks of men. Then they shall know that I am the LORD.\"\"",
}

# Ezekiel 47 — the river from the temple
ch47 = {
    1: "Then he brought me back to the door of the temple; and there was water, flowing from under the threshold of the temple toward the east, for the front of the temple faced east; the water was flowing from under the right side of the temple, south of the altar.",
    2: "He brought me out by way of the north gate, and led me around on the outside to the outer gateway that faces east; and there was water, running out on the right side.",
    3: "And when the man went out to the east with the line in his hand, he measured one thousand cubits, and he brought me through the waters; the water came up to my ankles.",
    4: "Again he measured one thousand and brought me through the waters; the water came up to my knees. Again he measured one thousand and brought me through; the water came up to my waist.",
    5: "Again he measured one thousand, and it was a river that I could not cross; for the water was too deep, water in which one must swim, a river that could not be crossed.",
    6: "He said to me, \"Son of man, have you seen this?\" Then he brought me and returned me to the bank of the river.",
    7: "When I returned, there, along the bank of the river, were very many trees on one side and the other.",
    8: "Then he said to me: \"This water flows toward the eastern region, goes down into the valley, and enters the sea. When it reaches the sea, its waters are healed.",
    9: "And it shall be that every living thing that moves, wherever the rivers go, will live. There will be a very great multitude of fish, because these waters go there; for they will be healed, and everything will live wherever the river goes.",
    10: "It shall be that fishermen will stand by it from En Gedi to En Eglaim; they will be places for spreading their nets. Their fish will be of the same kinds as the fish of the Great Sea, exceedingly many.",
    11: "But its swamps and marshes will not be healed; they will be given over to salt.",
    12: "Along the bank of the river, on this side and that, will grow all kinds of trees used for food; their leaves will not wither, and their fruit will not fail. They will bear fruit every month, because their water flows from the sanctuary. Their fruit will be for food, and their leaves for medicine.\"",
    13: "Thus says the Lord GOD: \"These are the borders by which you shall divide the land as an inheritance among the twelve tribes of Israel. Joseph shall have two portions.",
    14: "You shall inherit it equally with one another; for I raised My hand in an oath to give it to your fathers, and this land shall fall to you as your inheritance.",
    15: "\"This shall be the border of the land on the north: from the Great Sea, by the road to Hethlon, as one goes to Zedad,",
    16: "Hamath, Berothah, Sibraim (which is between the border of Damascus and the border of Hamath), to Hazar Hatticon (which is on the border of Hauran).",
    17: "Thus the boundary shall be from the Sea to Hazar Enan, the border of Damascus; and as for the north, northward, it is the border of Hamath. This is the north side.",
    18: "\"On the east side you shall mark out the border from between Hauran and Damascus, and between Gilead and the land of Israel, along the Jordan, and along the eastern side of the sea. This is the east side.",
    19: "\"The south side, toward the South, shall be from Tamar to the waters of Meribah by Kadesh, along the brook to the Great Sea. This is the south side, toward the South.",
    20: "\"The west side shall be the Great Sea, from the southern boundary until one comes to a point opposite Hamath. This is the west side.",
    21: "\"Thus you shall divide this land among yourselves according to the tribes of Israel.",
    22: "It shall be that you will divide it by lot as an inheritance for yourselves, and for the strangers who dwell among you and who bear children among you. They shall be to you as native-born among the children of Israel; they shall have an inheritance with you among the tribes of Israel.",
    23: "And it shall be that in whatever tribe the stranger dwells, there you shall give him his inheritance,\" says the Lord GOD.",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"26_1_{v}"] = t
for v, t in ch36.items():
    ENTRIES[f"26_36_{v}"] = t
for v, t in ch47.items():
    ENTRIES[f"26_47_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Ezekiel landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
