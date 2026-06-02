"""MBT generator: Hosea landmark chapters.

Book ID 28. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Hosea 1 (11 verses) — Gomer the unfaithful wife; the children named
- Hosea 2 (23 verses) — the wilderness wooing; "I will betroth you"
- Hosea 6 (11 verses) — "Come, and let us return to the LORD"
- Hosea 11 (12 verses) — "When Israel was a child, I loved him"
- Hosea 14 (9 verses) — the great return; "I will heal their backsliding"

Total: 66 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Hosea 1 — Gomer and the prophetic marriage
ch1 = {
    1: "The word of the LORD that came to Hosea the son of Beeri, in the days of Uzziah, Jotham, Ahaz, and Hezekiah, kings of Judah, and in the days of Jeroboam the son of Joash, king of Israel.",
    2: "When the LORD began to speak by Hosea, the LORD said to Hosea: \"Go, take yourself a wife of harlotry and children of harlotry, for the land has committed great harlotry by departing from the LORD.\"",
    3: "So he went and took Gomer the daughter of Diblaim, and she conceived and bore him a son.",
    4: "Then the LORD said to him: \"Call his name Jezreel, for in a little while I will avenge the bloodshed of Jezreel on the house of Jehu, and bring an end to the kingdom of the house of Israel.",
    5: "It shall come to pass in that day that I will break the bow of Israel in the Valley of Jezreel.\"",
    6: "And she conceived again and bore a daughter. Then God said to him: \"Call her name Lo-Ruhamah, for I will no longer have mercy on the house of Israel, but I will utterly take them away.",
    7: "Yet I will have mercy on the house of Judah, will save them by the LORD their God, and will not save them by bow, nor by sword or battle, by horses or horsemen.\"",
    8: "Now when she had weaned Lo-Ruhamah, she conceived and bore a son.",
    9: "Then God said: \"Call his name Lo-Ammi, for you are not My people, and I will not be your God.",
    10: "Yet the number of the children of Israel shall be as the sand of the sea, which cannot be measured or numbered. And it shall come to pass in the place where it was said to them, 'You are not My people,' there it shall be said to them, 'You are sons of the living God.'",
    11: "Then the children of Judah and the children of Israel shall be gathered together, and appoint for themselves one head; and they shall come up out of the land, for great will be the day of Jezreel!\"",
}

# Hosea 2 — the wilderness wooing
ch2 = {
    1: "Say to your brethren, 'My people,' and to your sisters, 'Mercy is shown.'",
    2: "\"Bring charges against your mother, bring charges; for she is not My wife, nor am I her Husband! Let her put away her harlotries from her sight, and her adulteries from between her breasts;",
    3: "lest I strip her naked and expose her, as in the day she was born, and make her like a wilderness, and set her like a dry land, and slay her with thirst.",
    4: "I will not have mercy on her children, for they are the children of harlotry.",
    5: "For their mother has played the harlot; she who conceived them has behaved shamefully. For she said, 'I will go after my lovers, who give me my bread and my water, my wool and my linen, my oil and my drink.'",
    6: "\"Therefore, behold, I will hedge up your way with thorns, and wall her in, so that she cannot find her paths.",
    7: "She will chase her lovers, but not overtake them; yes, she will seek them, but not find them. Then she will say, 'I will go and return to my first husband, for then it was better for me than now.'",
    8: "For she did not know that I gave her grain, new wine, and oil, and multiplied her silver and gold — which they prepared for Baal.",
    9: "Therefore I will return and take away My grain in its time and My new wine in its season, and will take back My wool and My linen, given to cover her nakedness.",
    10: "Now I will uncover her lewdness in the sight of her lovers, and no one shall deliver her from My hand.",
    11: "I will also cause all her mirth to cease, her feast days, her New Moons, her Sabbaths — all her appointed feasts.",
    12: "\"And I will destroy her vines and her fig trees, of which she has said, 'These are my wages that my lovers have given me.' So I will make them a forest, and the beasts of the field shall eat them.",
    13: "I will punish her for the days of the Baals to which she burned incense. She decked herself with her earrings and jewelry, and went after her lovers; but Me she forgot,\" says the LORD.",
    14: "\"Therefore, behold, I will allure her, will bring her into the wilderness, and speak comfort to her.",
    15: "I will give her her vineyards from there, and the Valley of Achor as a door of hope; she shall sing there, as in the days of her youth, as in the day when she came up from the land of Egypt.",
    16: "\"And it shall be, in that day,\" says the LORD, \"that you will call Me 'My Husband,' and no longer call Me 'My Master,'",
    17: "for I will take from her mouth the names of the Baals, and they shall be remembered by their name no more.",
    18: "In that day I will make a covenant for them with the beasts of the field, with the birds of the air, and with the creeping things of the ground. Bow and sword of battle I will shatter from the earth, to make them lie down safely.",
    19: "I will betroth you to Me forever; yes, I will betroth you to Me in righteousness and justice, in lovingkindness and mercy;",
    20: "I will betroth you to Me in faithfulness, and you shall know the LORD.",
    21: "\"It shall come to pass in that day that I will answer,\" says the LORD; \"I will answer the heavens, and they shall answer the earth.",
    22: "The earth shall answer with grain, with new wine, and with oil; they shall answer Jezreel.",
    23: "Then I will sow her for Myself in the earth, and I will have mercy on her who had not obtained mercy; then I will say to those who were not My people, 'You are My people!' And they shall say, 'You are my God!'\"",
}

# Hosea 6 — "Come, and let us return"
ch6 = {
    1: "Come, and let us return to the LORD; for He has torn, but He will heal us; He has stricken, but He will bind us up.",
    2: "After two days He will revive us; on the third day He will raise us up, that we may live in His sight.",
    3: "Let us know, let us pursue the knowledge of the LORD. His going forth is established as the morning; He will come to us like the rain, like the latter and former rain to the earth.",
    4: "\"O Ephraim, what shall I do to you? O Judah, what shall I do to you? For your faithfulness is like a morning cloud, and like the early dew it goes away.",
    5: "Therefore I have hewn them by the prophets, I have slain them by the words of My mouth; and your judgments are like light that goes forth.",
    6: "For I desire mercy and not sacrifice, and the knowledge of God more than burnt offerings.",
    7: "\"But like men they transgressed the covenant; there they dealt treacherously with Me.",
    8: "Gilead is a city of evildoers and defiled with blood.",
    9: "As bands of robbers lie in wait for a man, so the company of priests murder on the way to Shechem; surely they commit lewdness.",
    10: "I have seen a horrible thing in the house of Israel: there is the harlotry of Ephraim; Israel is defiled.",
    11: "Also, O Judah, a harvest is appointed for you, when I return the captives of My people.",
}

# Hosea 11 — the Father's love for Israel
ch11 = {
    1: "\"When Israel was a child, I loved him, and out of Egypt I called My son.",
    2: "As they called them, so they went from them; they sacrificed to the Baals, and burned incense to carved images.",
    3: "I taught Ephraim to walk, taking them by their arms; but they did not know that I healed them.",
    4: "I drew them with gentle cords, with bands of love, and I was to them as those who take the yoke from their neck. I stooped and fed them.",
    5: "\"He shall not return to the land of Egypt; but the Assyrian shall be his king, because they refused to repent.",
    6: "And the sword shall slash in his cities, devour his districts, and consume them, because of their own counsels.",
    7: "My people are bent on backsliding from Me. Though they call to the Most High, none at all exalt Him.",
    8: "\"How can I give you up, Ephraim? How can I hand you over, Israel? How can I make you like Admah? How can I set you like Zeboiim? My heart churns within Me; My sympathy is stirred.",
    9: "I will not execute the fierceness of My anger; I will not again destroy Ephraim. For I am God, and not man, the Holy One in your midst; and I will not come with terror.",
    10: "\"They shall walk after the LORD. He will roar like a lion. When He roars, then His sons shall come trembling from the west;",
    11: "they shall come trembling like a bird from Egypt, like a dove from the land of Assyria. And I will let them dwell in their houses,\" says the LORD.",
    12: "\"Ephraim has encircled Me with lies, and the house of Israel with deceit; but Judah still walks with God, even with the Holy One who is faithful.\"",
}

# Hosea 14 — the great return
ch14 = {
    1: "O Israel, return to the LORD your God, for you have stumbled because of your iniquity;",
    2: "take words with you, and return to the LORD. Say to Him, \"Take away all iniquity; receive us graciously, for we will offer the sacrifices of our lips.",
    3: "Assyria shall not save us, we will not ride on horses, nor will we say anymore to the work of our hands, 'You are our gods.' For in You the fatherless finds mercy.\"",
    4: "\"I will heal their backsliding, I will love them freely, for My anger has turned away from him.",
    5: "I will be like the dew to Israel; he shall grow like the lily, and lengthen his roots like Lebanon.",
    6: "His branches shall spread; his beauty shall be like an olive tree, and his fragrance like Lebanon.",
    7: "Those who dwell under his shadow shall return; they shall be revived like grain, and grow like a vine. Their scent shall be like the wine of Lebanon.",
    8: "\"Ephraim shall say, 'What have I to do anymore with idols?' I have heard and observed him. I am like a green cypress tree; your fruit is found in Me.\"",
    9: "Who is wise? Let him understand these things. Who is prudent? Let him know them. For the ways of the LORD are right; the righteous walk in them, but transgressors stumble in them.",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"28_1_{v}"] = t
for v, t in ch2.items():
    ENTRIES[f"28_2_{v}"] = t
for v, t in ch6.items():
    ENTRIES[f"28_6_{v}"] = t
for v, t in ch11.items():
    ENTRIES[f"28_11_{v}"] = t
for v, t in ch14.items():
    ENTRIES[f"28_14_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Hosea landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
