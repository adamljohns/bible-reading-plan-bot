"""MBT generator: Joel (complete book, 3 chapters, 73 verses).

Book ID 29. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Joel 2:28-32 was previously authored in the earlier wisdom/prophets
landmark batch. This idempotent rerun preserves them and fills in
the rest of the book.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Joel 1 — the locust plague
ch1 = {
    1: "The word of the LORD that came to Joel the son of Pethuel.",
    2: "Hear this, you elders, and give ear, all you inhabitants of the land! Has anything like this happened in your days, or even in the days of your fathers?",
    3: "Tell your children about it, let your children tell their children, and their children another generation.",
    4: "What the chewing locust left, the swarming locust has eaten; what the swarming locust left, the crawling locust has eaten; and what the crawling locust left, the consuming locust has eaten.",
    5: "Awake, you drunkards, and weep; and wail, all you drinkers of wine, because of the new wine, for it has been cut off from your mouth.",
    6: "For a nation has come up against My land, strong, and without number; his teeth are the teeth of a lion, and he has the fangs of a fierce lion.",
    7: "He has laid waste My vine, and ruined My fig tree; he has stripped it bare and thrown it away; its branches are made white.",
    8: "Lament like a virgin girded with sackcloth for the husband of her youth.",
    9: "The grain offering and the drink offering have been cut off from the house of the LORD; the priests mourn, who minister to the LORD.",
    10: "The field is wasted, the land mourns; for the grain is ruined, the new wine is dried up, the oil fails.",
    11: "Be ashamed, you farmers, wail, you vinedressers, for the wheat and the barley; because the harvest of the field has perished.",
    12: "The vine has dried up, and the fig tree has withered; the pomegranate tree, the palm tree also, and the apple tree — all the trees of the field are withered; surely joy has withered away from the sons of men.",
    13: "Gird yourselves and lament, you priests; wail, you who minister before the altar; come, lie all night in sackcloth, you who minister to my God; for the grain offering and the drink offering are withheld from the house of your God.",
    14: "Consecrate a fast, call a sacred assembly; gather the elders and all the inhabitants of the land into the house of the LORD your God, and cry out to the LORD.",
    15: "Alas for the day! For the day of the LORD is at hand; it shall come as destruction from the Almighty.",
    16: "Is not the food cut off before our eyes, joy and gladness from the house of our God?",
    17: "The seed shrivels under the clods, storehouses are in shambles; barns are broken down, for the grain has withered.",
    18: "How the animals groan! The herds of cattle are restless, because they have no pasture; even the flocks of sheep suffer punishment.",
    19: "O LORD, to You I cry out; for fire has devoured the open pastures, and a flame has burned all the trees of the field.",
    20: "The beasts of the field also cry out to You, for the water brooks are dried up, and fire has devoured the open pastures.",
}

# Joel 2 — day of the LORD + outpouring of the Spirit
# (vv 28-32 already in MBT from earlier batch; included here verbatim to keep idempotent)
ch2 = {
    1: "Blow the trumpet in Zion, and sound an alarm in My holy mountain! Let all the inhabitants of the land tremble; for the day of the LORD is coming, for it is at hand:",
    2: "a day of darkness and gloominess, a day of clouds and thick darkness, like the morning clouds spread over the mountains. A people come, great and strong, the like of whom has never been; nor will there ever be any such after them, even for many successive generations.",
    3: "A fire devours before them, and behind them a flame burns; the land is like the Garden of Eden before them, and behind them a desolate wilderness; surely nothing shall escape them.",
    4: "Their appearance is like the appearance of horses; and like swift steeds, so they run.",
    5: "With a noise like chariots, over mountaintops they leap, like the noise of a flaming fire that devours the stubble, like a strong people set in battle array.",
    6: "Before them the people writhe in pain; all faces are drained of color.",
    7: "They run like mighty men, they climb the wall like men of war; every one marches in formation, and they do not break ranks.",
    8: "They do not push one another; every one marches in his own column. Though they lunge between the weapons, they are not cut down.",
    9: "They run to and fro in the city, they run on the wall; they climb into the houses, they enter at the windows like a thief.",
    10: "The earth quakes before them, the heavens tremble; the sun and moon grow dark, and the stars diminish their brightness.",
    11: "The LORD gives voice before His army, for His camp is very great; for strong is the One who executes His word. For the day of the LORD is great and very terrible; who can endure it?",
    12: "\"Now, therefore,\" says the LORD, \"turn to Me with all your heart, with fasting, with weeping, and with mourning.\"",
    13: "So rend your heart, and not your garments; return to the LORD your God, for He is gracious and merciful, slow to anger, and of great kindness; and He relents from doing harm.",
    14: "Who knows if He will turn and relent, and leave a blessing behind Him — a grain offering and a drink offering for the LORD your God?",
    15: "Blow the trumpet in Zion, consecrate a fast, call a sacred assembly;",
    16: "gather the people, sanctify the congregation, assemble the elders, gather the children and nursing babes; let the bridegroom go out from his chamber, and the bride from her dressing room.",
    17: "Let the priests, who minister to the LORD, weep between the porch and the altar; let them say, \"Spare Your people, O LORD, and do not give Your heritage to reproach, that the nations should rule over them. Why should they say among the peoples, 'Where is their God?'\"",
    18: "Then the LORD will be zealous for His land, and pity His people.",
    19: "The LORD will answer and say to His people, \"Behold, I will send you grain and new wine and oil, and you will be satisfied by them; I will no longer make you a reproach among the nations.",
    20: "But I will remove far from you the northern army, and will drive him away into a barren and desolate land, with his face toward the eastern sea and his back toward the western sea; his stench will come up, and his foul odor will rise, because he has done monstrous things.\"",
    21: "Fear not, O land; be glad and rejoice, for the LORD has done marvelous things!",
    22: "Do not be afraid, you beasts of the field; for the open pastures are springing up, and the tree bears its fruit; the fig tree and the vine yield their strength.",
    23: "Be glad then, you children of Zion, and rejoice in the LORD your God; for He has given you the former rain faithfully, and He will cause the rain to come down for you — the former rain, and the latter rain in the first month.",
    24: "The threshing floors shall be full of wheat, and the vats shall overflow with new wine and oil.",
    25: "\"So I will restore to you the years that the swarming locust has eaten, the crawling locust, the consuming locust, and the chewing locust, My great army which I sent among you.",
    26: "You shall eat in plenty and be satisfied, and praise the name of the LORD your God, who has dealt wondrously with you; and My people shall never be put to shame.",
    27: "Then you shall know that I am in the midst of Israel; I am the LORD your God and there is no other. My people shall never be put to shame.",
    28: "\"And it shall come to pass afterward that I will pour out My Spirit on all flesh; your sons and your daughters shall prophesy, your old men shall dream dreams, your young men shall see visions.",
    29: "And also on My menservants and on My maidservants I will pour out My Spirit in those days.",
    30: "And I will show wonders in the heavens and in the earth: blood and fire and pillars of smoke.",
    31: "The sun shall be turned into darkness, and the moon into blood, before the coming of the great and awesome day of the LORD.",
    32: "And it shall come to pass that whoever calls on the name of the LORD shall be saved. For in Mount Zion and in Jerusalem there shall be deliverance, as the LORD has said, among the remnant whom the LORD calls.\"",
}

# Joel 3 — the valley of decision
ch3 = {
    1: "\"For behold, in those days and at that time, when I bring back the captives of Judah and Jerusalem,",
    2: "I will also gather all nations, and bring them down to the Valley of Jehoshaphat; and I will enter into judgment with them there on account of My people, My heritage Israel, whom they have scattered among the nations; they have also divided up My land.",
    3: "They have cast lots for My people, have given a boy as payment for a harlot, and sold a girl for wine, that they may drink.",
    4: "\"Indeed, what have you to do with Me, O Tyre and Sidon, and all the coasts of Philistia? Will you retaliate against Me? But if you retaliate against Me, swiftly and speedily I will return your retaliation upon your own head;",
    5: "because you have taken My silver and My gold, and have carried into your temples My prized possessions.",
    6: "Also the people of Judah and the people of Jerusalem you have sold to the Greeks, that you may remove them far from their borders.",
    7: "\"Behold, I will raise them out of the place to which you have sold them, and will return your retaliation upon your own head.",
    8: "I will sell your sons and your daughters into the hand of the people of Judah, and they will sell them to the Sabeans, to a people far off; for the LORD has spoken.\"",
    9: "Proclaim this among the nations: \"Prepare for war! Wake up the mighty men, let all the men of war draw near, let them come up.",
    10: "Beat your plowshares into swords and your pruning hooks into spears; let the weak say, 'I am strong.'\"",
    11: "Assemble and come, all you nations, and gather together all around. Cause Your mighty ones to go down there, O LORD.",
    12: "\"Let the nations be wakened, and come up to the Valley of Jehoshaphat; for there I will sit to judge all the surrounding nations.",
    13: "Put in the sickle, for the harvest is ripe. Come, go down; for the winepress is full, the vats overflow — for their wickedness is great.\"",
    14: "Multitudes, multitudes in the valley of decision! For the day of the LORD is near in the valley of decision.",
    15: "The sun and moon will grow dark, and the stars will diminish their brightness.",
    16: "The LORD also will roar from Zion, and utter His voice from Jerusalem; the heavens and earth will shake; but the LORD will be a shelter for His people, and the strength of the children of Israel.",
    17: "\"So you shall know that I am the LORD your God, dwelling in Zion My holy mountain. Then Jerusalem shall be holy, and no aliens shall ever pass through her again.\"",
    18: "And it will come to pass in that day that the mountains shall drip with new wine, the hills shall flow with milk, and all the brooks of Judah shall be flooded with water; a fountain shall flow from the house of the LORD and water the Valley of Acacias.",
    19: "\"Egypt shall be a desolation, and Edom a desolate wilderness, because of violence against the people of Judah, for they have shed innocent blood in their land.",
    20: "But Judah shall abide forever, and Jerusalem from generation to generation.",
    21: "For I will acquit them of the guilt of bloodshed, whom I had not acquitted; for the LORD dwells in Zion.\"",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"29_1_{v}"] = t
for v, t in ch2.items():
    ENTRIES[f"29_2_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"29_3_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Joel verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
