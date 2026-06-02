"""MBT generator: Zechariah landmark chapters.

Book ID 38. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Zechariah 8 (23 verses) — Zion restored; old men and women in the streets
- Zechariah 9 (17 verses) — the King on a donkey
- Zechariah 12 (14 verses) — "they will look on Me whom they pierced"
- Zechariah 13 (9 verses) — a fountain opened for sin and uncleanness
- Zechariah 14 (21 verses) — "the LORD shall be King over all the earth"

Total: 84 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Zechariah 8 — Zion restored
ch8 = {
    1: "Again the word of the LORD of hosts came, saying,",
    2: "\"Thus says the LORD of hosts: 'I am zealous for Zion with great zeal; with great fervor I am zealous for her.'",
    3: "Thus says the LORD: 'I will return to Zion, and dwell in the midst of Jerusalem. Jerusalem shall be called the City of Truth, the Mountain of the LORD of hosts, the Holy Mountain.'",
    4: "Thus says the LORD of hosts: 'Old men and old women shall again sit in the streets of Jerusalem, each one with his staff in his hand because of great age.",
    5: "The streets of the city shall be full of boys and girls playing in its streets.'",
    6: "Thus says the LORD of hosts: 'If it is marvelous in the eyes of the remnant of this people in these days, will it also be marvelous in My eyes?' says the LORD of hosts.",
    7: "Thus says the LORD of hosts: 'Behold, I will save My people from the land of the east and from the land of the west;",
    8: "I will bring them back, and they shall dwell in the midst of Jerusalem. They shall be My people and I will be their God, in truth and righteousness.'",
    9: "Thus says the LORD of hosts: 'Let your hands be strong, you who have been hearing in these days these words by the mouth of the prophets, who spoke in the day the foundation was laid for the house of the LORD of hosts, that the temple might be built.",
    10: "For before these days there were no wages for man nor any hire for beast; there was no peace from the enemy for whoever went out or came in; for I set all men, everyone, against his neighbor.",
    11: "But now I will not treat the remnant of this people as in the former days,' says the LORD of hosts.",
    12: "'For the seed shall be prosperous, the vine shall give its fruit, the ground shall give her increase, and the heavens shall give their dew — I will cause the remnant of this people to possess all these.",
    13: "And it shall come to pass that just as you were a curse among the nations, O house of Judah and house of Israel, so I will save you, and you shall be a blessing. Do not fear, let your hands be strong.'",
    14: "For thus says the LORD of hosts: 'Just as I determined to punish you when your fathers provoked Me to wrath,' says the LORD of hosts, 'and I would not relent,",
    15: "so again in these days I am determined to do good to Jerusalem and to the house of Judah. Do not fear.",
    16: "These are the things you shall do: speak each man the truth to his neighbor; give judgment in your gates for truth, justice, and peace;",
    17: "let none of you think evil in your heart against your neighbor; and do not love a false oath. For all these are things that I hate,' says the LORD.\"",
    18: "Then the word of the LORD of hosts came to me, saying,",
    19: "\"Thus says the LORD of hosts: 'The fast of the fourth month, the fast of the fifth, the fast of the seventh, and the fast of the tenth, shall be joy and gladness and cheerful feasts for the house of Judah. Therefore love truth and peace.'",
    20: "\"Thus says the LORD of hosts: 'Peoples shall yet come, inhabitants of many cities;",
    21: "the inhabitants of one city shall go to another, saying, \"Let us continue to go and pray before the LORD, and seek the LORD of hosts. I myself will go also.\"",
    22: "Yes, many peoples and strong nations shall come to seek the LORD of hosts in Jerusalem, and to pray before the LORD.'",
    23: "\"Thus says the LORD of hosts: 'In those days ten men from every language of the nations shall grasp the sleeve of a Jewish man, saying, \"Let us go with you, for we have heard that God is with you.\"'\"",
}

# Zechariah 9 — the King on a donkey
ch9 = {
    1: "The burden of the word of the LORD against the land of Hadrach, and Damascus its resting place (for the eyes of men and all the tribes of Israel are on the LORD);",
    2: "also against Hamath, which borders on it, and against Tyre and Sidon, though they are very wise.",
    3: "For Tyre built herself a tower, heaped up silver like the dust, and gold like the mire of the streets.",
    4: "Behold, the Lord will cast her out; He will destroy her power in the sea, and she will be devoured by fire.",
    5: "Ashkelon shall see it and fear; Gaza also shall be very sorrowful, and Ekron, for He dried up her expectation. The king shall perish from Gaza, and Ashkelon shall not be inhabited.",
    6: "A mixed race shall settle in Ashdod, and I will cut off the pride of the Philistines.",
    7: "I will take away the blood from his mouth, and the abominations from between his teeth. But he who remains, even he shall be for our God, and shall be like a leader in Judah, and Ekron like a Jebusite.",
    8: "I will camp around My house because of the army, because of him who passes by and him who returns. No more shall an oppressor pass through them, for now I have seen with My eyes.",
    9: "Rejoice greatly, O daughter of Zion! Shout, O daughter of Jerusalem! Behold, your King is coming to you; He is just and having salvation, lowly and riding on a donkey, a colt, the foal of a donkey.",
    10: "I will cut off the chariot from Ephraim and the horse from Jerusalem; the battle bow shall be cut off. He shall speak peace to the nations; His dominion shall be from sea to sea, and from the River to the ends of the earth.",
    11: "As for you also, because of the blood of your covenant, I will set your prisoners free from the waterless pit.",
    12: "Return to the stronghold, you prisoners of hope. Even today I declare that I will restore double to you.",
    13: "For I have bent Judah, My bow, fitted the bow with Ephraim, and raised up your sons, O Zion, against your sons, O Greece, and made you like the sword of a mighty man.",
    14: "Then the LORD will be seen over them, and His arrow will go forth like lightning. The Lord GOD will blow the trumpet, and go with whirlwinds from the south.",
    15: "The LORD of hosts will defend them; they shall devour and subdue with slingstones. They shall drink and roar as if with wine; they shall be filled with blood like basins, like the corners of the altar.",
    16: "The LORD their God will save them in that day, as the flock of His people. For they shall be like the jewels of a crown, lifted like a banner over His land —",
    17: "for how great is its goodness and how great its beauty! Grain shall make the young men thrive, and new wine the young women.",
}

# Zechariah 12 — "they will look on Me whom they pierced"
ch12 = {
    1: "The burden of the word of the LORD against Israel. Thus says the LORD, who stretches out the heavens, lays the foundation of the earth, and forms the spirit of man within him:",
    2: "\"Behold, I will make Jerusalem a cup of drunkenness to all the surrounding peoples, when they lay siege against Judah and Jerusalem.",
    3: "And it shall happen in that day that I will make Jerusalem a very heavy stone for all peoples; all who would heave it away will surely be cut in pieces, though all nations of the earth are gathered against it.",
    4: "In that day,\" says the LORD, \"I will strike every horse with confusion, and its rider with madness; I will open My eyes on the house of Judah, and will strike every horse of the peoples with blindness.",
    5: "And the governors of Judah shall say in their heart, 'The inhabitants of Jerusalem are my strength in the LORD of hosts, their God.'",
    6: "In that day I will make the governors of Judah like a firepan in the woodpile, and like a fiery torch in the sheaves; they shall devour all the surrounding peoples on the right hand and on the left, but Jerusalem shall be inhabited again in her own place — Jerusalem.",
    7: "The LORD will save the tents of Judah first, so that the glory of the house of David and the glory of the inhabitants of Jerusalem shall not become greater than that of Judah.",
    8: "In that day the LORD will defend the inhabitants of Jerusalem; the one who is feeble among them in that day shall be like David, and the house of David shall be like God, like the Angel of the LORD before them.",
    9: "It shall be in that day that I will seek to destroy all the nations that come against Jerusalem.",
    10: "\"And I will pour on the house of David and on the inhabitants of Jerusalem the Spirit of grace and supplication; then they will look on Me whom they pierced. Yes, they will mourn for Him as one mourns for his only son, and grieve for Him as one grieves for a firstborn.",
    11: "In that day there shall be a great mourning in Jerusalem, like the mourning at Hadad Rimmon in the plain of Megiddo.",
    12: "And the land shall mourn, every family by itself: the family of the house of David by itself, and their wives by themselves; the family of the house of Nathan by itself, and their wives by themselves;",
    13: "the family of the house of Levi by itself, and their wives by themselves; the family of Shimei by itself, and their wives by themselves;",
    14: "all the families that remain, every family by itself, and their wives by themselves.",
}

# Zechariah 13 — the fountain opened
ch13 = {
    1: "\"In that day a fountain shall be opened for the house of David and for the inhabitants of Jerusalem, for sin and for uncleanness.",
    2: "It shall be in that day,\" says the LORD of hosts, \"that I will cut off the names of the idols from the land, and they shall no longer be remembered. I will also cause the prophets and the unclean spirit to depart from the land.",
    3: "It shall come to pass that if anyone still prophesies, then his father and mother who begot him will say to him, 'You shall not live, because you have spoken lies in the name of the LORD.' And his father and mother who begot him shall thrust him through when he prophesies.",
    4: "And it shall be in that day that every prophet will be ashamed of his vision when he prophesies; they will not wear a robe of coarse hair to deceive.",
    5: "But he will say, 'I am no prophet, I am a farmer; for a man taught me to keep cattle from my youth.'",
    6: "And one will say to him, 'What are these wounds between your arms?' Then he will answer, 'Those with which I was wounded in the house of my friends.'",
    7: "\"Awake, O sword, against My Shepherd, against the Man who is My Companion,\" says the LORD of hosts. \"Strike the Shepherd, and the sheep will be scattered; then I will turn My hand against the little ones.",
    8: "And it shall come to pass in all the land,\" says the LORD, \"that two-thirds in it shall be cut off and die, but one-third shall be left in it:",
    9: "I will bring the one-third through the fire, will refine them as silver is refined, and test them as gold is tested. They will call on My name, and I will answer them. I will say, 'This is My people'; and each one will say, 'The LORD is my God.'\"",
}

# Zechariah 14 — "the LORD shall be King over all the earth"
ch14 = {
    1: "Behold, the day of the LORD is coming, and your spoil will be divided in your midst.",
    2: "For I will gather all the nations to battle against Jerusalem; the city shall be taken, the houses rifled, and the women ravished. Half of the city shall go into captivity, but the remnant of the people shall not be cut off from the city.",
    3: "Then the LORD will go forth and fight against those nations, as He fights in the day of battle.",
    4: "And in that day His feet will stand on the Mount of Olives, which faces Jerusalem on the east. And the Mount of Olives shall be split in two, from east to west, making a very large valley; half of the mountain shall move toward the north and half of it toward the south.",
    5: "Then you shall flee through My mountain valley, for the mountain valley shall reach to Azal. Yes, you shall flee as you fled from the earthquake in the days of Uzziah king of Judah. Thus the LORD my God will come, and all the saints with You.",
    6: "It shall come to pass in that day that there will be no light; the lights will diminish.",
    7: "It shall be one day which is known to the LORD — neither day nor night. But at evening time it shall happen that it will be light.",
    8: "And in that day it shall be that living waters shall flow from Jerusalem, half of them toward the eastern sea and half of them toward the western sea; in both summer and winter it shall occur.",
    9: "And the LORD shall be King over all the earth. In that day it shall be — \"The LORD is one,\" and His name one.",
    10: "All the land shall be turned into a plain from Geba to Rimmon south of Jerusalem. Jerusalem shall be raised up and inhabited in her place from Benjamin's Gate to the place of the First Gate and the Corner Gate, and from the Tower of Hananel to the king's winepresses.",
    11: "The people shall dwell in it; and no longer shall there be utter destruction, but Jerusalem shall be safely inhabited.",
    12: "And this shall be the plague with which the LORD will strike all the people who fought against Jerusalem: their flesh shall dissolve while they stand on their feet, their eyes shall dissolve in their sockets, and their tongues shall dissolve in their mouths.",
    13: "It shall come to pass in that day that a great panic from the LORD will be among them. Everyone will seize the hand of his neighbor, and raise his hand against his neighbor's hand;",
    14: "Judah also will fight at Jerusalem. And the wealth of all the surrounding nations shall be gathered together: gold, silver, and apparel in great abundance.",
    15: "Such also shall be the plague on the horse and the mule, on the camel and the donkey, and on all the cattle that will be in those camps. So shall this plague be.",
    16: "And it shall come to pass that everyone who is left of all the nations which came against Jerusalem shall go up from year to year to worship the King, the LORD of hosts, and to keep the Feast of Tabernacles.",
    17: "And it shall be that whichever of the families of the earth do not come up to Jerusalem to worship the King, the LORD of hosts, on them there will be no rain.",
    18: "If the family of Egypt will not come up and enter in, they shall have no rain; they shall receive the plague with which the LORD strikes the nations who do not come up to keep the Feast of Tabernacles.",
    19: "This shall be the punishment of Egypt and the punishment of all the nations that do not come up to keep the Feast of Tabernacles.",
    20: "In that day \"HOLINESS TO THE LORD\" shall be engraved on the bells of the horses. The pots in the LORD's house shall be like the bowls before the altar.",
    21: "Yes, every pot in Jerusalem and Judah shall be holiness to the LORD of hosts. Everyone who sacrifices shall come and take them and cook in them. In that day there shall no longer be a Canaanite in the house of the LORD of hosts.",
}

ENTRIES = {}
for v, t in ch8.items():
    ENTRIES[f"38_8_{v}"] = t
for v, t in ch9.items():
    ENTRIES[f"38_9_{v}"] = t
for v, t in ch12.items():
    ENTRIES[f"38_12_{v}"] = t
for v, t in ch13.items():
    ENTRIES[f"38_13_{v}"] = t
for v, t in ch14.items():
    ENTRIES[f"38_14_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Zechariah landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
