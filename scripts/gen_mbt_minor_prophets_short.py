"""MBT 3 short Minor Prophets — Obadiah, Habakkuk, Haggai.

Obadiah   (1 ch, 21 verses) — judgment on Edom
Habakkuk  (3 ch, 56 verses) — 'the righteous shall live by faith'
Haggai    (2 ch, 38 verses) — rebuild the temple
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Obadiah — judgment on Edom
obad_1 = {
    1: "The vision of Obadiah. Thus says the Lord GOD concerning Edom — we have heard a report from the LORD, and an envoy has been sent among the nations: \"Arise, and let us go against her for battle.\"",
    2: "\"Behold, I will make you small among the nations — you are greatly despised.",
    3: "The arrogance of your heart has deceived you, you who live in the clefts of the rock, in the loftiness of your dwelling place — who say in your heart, 'Who will bring me down to earth?'",
    4: "Though you build high like the eagle — though you set your nest among the stars, from there I will bring you down,\" declares the LORD.",
    5: "\"If thieves came to you, if robbers by night — O how you will be ruined! — would they not steal only until they had enough? If grape gatherers came to you, would they not leave some gleanings?",
    6: "O how Esau will be ransacked! And his hidden treasures searched out!",
    7: "All the men allied with you will send you forth to the border — and the men at peace with you will deceive you and overpower you. They who eat your bread will set an ambush for you. There is no understanding in him.",
    8: "Will I not on that day,\" declares the LORD, \"destroy wise men from Edom, and understanding from the mountain of Esau?",
    9: "Then your mighty men will be dismayed, O Teman — in order that everyone may be cut off from the mountain of Esau by slaughter.",
    10: "Because of violence to your brother Jacob, you will be covered with shame — and you will be cut off forever.",
    11: "On the day that you stood aloof, on the day that strangers carried off his wealth, and foreigners entered his gate and cast lots for Jerusalem — you too were as one of them.",
    12: "Do not gloat over your brother's day, the day of his misfortune. Do not rejoice over the sons of Judah in the day of their destruction — yes, do not boast in the day of their distress.",
    13: "Do not enter the gate of My people in the day of their disaster. Yes, you, do not gloat over their calamity in the day of their disaster. Do not loot their wealth in the day of their disaster.",
    14: "Do not stand at the fork of the road to cut down their fugitives — and do not imprison their survivors in the day of their distress.",
    15: "For the day of the LORD draws near on all the nations. As you have done, it will be done to you — your dealings will return on your own head.",
    16: "For just as you drank on My holy mountain, all the nations will drink continually. They will drink and swallow, and become as if they had never existed.",
    17: "But on Mount Zion there will be those who escape, and it will be holy — and the house of Jacob will possess their possessions.",
    18: "Then the house of Jacob will be a fire, and the house of Joseph a flame. But the house of Esau will be as stubble — and they will set them on fire and consume them, so that there will be no survivor of the house of Esau,\" for the LORD has spoken.",
    19: "Then those of the Negev will possess the mountain of Esau, and those of the Shephelah the Philistine plain. Also, possess the territory of Ephraim and the territory of Samaria, and Benjamin will possess Gilead.",
    20: "And the exiles of this host of the sons of Israel, who are among the Canaanites as far as Zarephath, and the exiles of Jerusalem who are in Sepharad will possess the cities of the Negev.",
    21: "The deliverers will ascend Mount Zion to judge the mountain of Esau, and the kingdom will be the LORD's.",
}

# Habakkuk 1 — The prophet's complaint
hab_1 = {
    1: "The oracle which Habakkuk the prophet saw.",
    2: "How long, O LORD, will I call for help, and You will not hear? I cry out to You, \"Violence!\" — yet You do not save.",
    3: "Why do You make me see iniquity, and cause me to look on wickedness? Yes, destruction and violence are before me — strife exists, and contention arises.",
    4: "Therefore the law is ignored — and justice is never upheld. For the wicked surround the righteous — therefore justice comes out perverted.",
    5: "\"Look among the nations! Observe! Be astonished! Wonder! Because I am doing something in your days — you would not believe if you were told.",
    6: "For behold, I am raising up the Chaldeans, that fierce and impetuous people, who march throughout the earth to seize dwelling places which are not theirs.",
    7: "They are dreaded and feared — their justice and authority originate with themselves.",
    8: "Their horses are swifter than leopards, and keener than wolves in the evening. Their horsemen come galloping — their horsemen come from afar, they fly like an eagle swooping down to devour.",
    9: "All of them come for violence. Their horde of faces moves forward — they collect captives like sand.",
    10: "They mock at kings, and rulers are a laughing matter to them. They laugh at every fortress — and heap up rubble to capture it.",
    11: "Then they will sweep through like the wind, and pass on. But they will be held guilty — they whose strength is their god.\"",
    12: "Are You not from everlasting, O LORD, my God, my Holy One? We will not die. You, O LORD, have appointed them to judge. And You, O Rock, have established them to correct.",
    13: "Your eyes are too pure to approve evil, and You can not look on wickedness with favor. Why do You look with favor on those who deal treacherously? Why are You silent when the wicked swallow up those more righteous than they?",
    14: "Why have You made men like the fish of the sea — like creeping things without a ruler over them?",
    15: "The Chaldeans bring all of them up with a hook, drag them away with their net, and gather them together in their fishing net. Therefore they rejoice and are glad.",
    16: "Therefore they offer a sacrifice to their net, and burn incense to their fishing net — because through these things their catch is large, and their food is plentiful.",
    17: "Will they therefore empty their net, and continually slay nations without sparing?",
}
hab_2 = {
    1: "I will stand on my guard post and station myself on the rampart — and I will keep watch to see what He will speak to me, and how I may reply when I am reproved.",
    2: "Then the LORD answered me and said, \"Record the vision and inscribe it on tablets, that the one who reads it may run.",
    3: "For the vision is yet for the appointed time — it hastens toward the goal, and it will not fail. Though it tarries, wait for it — for it will certainly come, it will not delay.",
    4: "Behold, as for the proud one, his soul is not right within him — but the righteous will live by his faith.",
    5: "Furthermore, wine betrays the haughty man, so that he does not stay at home. He enlarges his appetite like Sheol, and he is like death, never satisfied. He also gathers to himself all nations and collects to himself all peoples.",
    6: "Will not all of these take up a taunt-song against him — even mockery and insinuations against him? And say, 'Woe to him who increases what is not his — for how long? And makes himself rich with loans!'",
    7: "Will not your creditors rise up suddenly, and those who collect from you awaken? Indeed, you will become plunder for them.",
    8: "Because you have looted many nations, all the remainder of the peoples will loot you — because of human bloodshed and violence done to the land, to the town, and all its inhabitants.",
    9: "Woe to him who gets evil gain for his house, to put his nest on high, to be delivered from the hand of calamity!",
    10: "You have devised a shameful thing for your house, by cutting off many peoples — so you are sinning against yourself.",
    11: "Surely the stone will cry out from the wall — and the rafter will answer it from the framework.",
    12: "Woe to him who builds a city with bloodshed, and founds a town with violence!",
    13: "Is it not indeed from the LORD of hosts that peoples toil for fire, and nations grow weary for nothing?",
    14: "For the earth will be filled with the knowledge of the glory of the LORD — as the waters cover the sea.",
    15: "Woe to you who make your neighbors drink, who mix in your venom even to make them drunk so as to look on their nakedness!",
    16: "You will be filled with disgrace rather than honor. Now you yourself drink and expose your own nakedness. The cup in the LORD's right hand will come around to you, and utter disgrace will come upon your glory.",
    17: "For the violence done to Lebanon will overwhelm you, and the devastation of its beasts by which you terrified them — because of human bloodshed, and violence done to the land, to the town and all its inhabitants.",
    18: "What profit is the idol when its maker has carved it, or an image, a teacher of falsehood? For its maker trusts in his own handiwork when he fashions speechless idols.",
    19: "Woe to him who says to a piece of wood, \"Awake!\" — to a dumb stone, \"Arise!\" And that is your teacher? Behold, it is overlaid with gold and silver, and there is no breath at all inside it.",
    20: "But the LORD is in His holy temple — let all the earth be silent before Him.",
}
hab_3 = {
    1: "A prayer of Habakkuk the prophet, according to Shigionoth.",
    2: "LORD, I have heard the report about You, and I fear. O LORD, revive Your work in the midst of the years. In the midst of the years make it known — in wrath remember mercy.",
    3: "God comes from Teman, and the Holy One from Mount Paran. Selah. His splendor covers the heavens, and the earth is full of His praise.",
    4: "His radiance is like the sunlight — He has rays flashing from His hand, and there is the hiding of His power.",
    5: "Before Him goes pestilence — and plague comes after Him.",
    6: "He stood and surveyed the earth. He looked and startled the nations. Yes, the perpetual mountains were shattered — the ancient hills collapsed. His ways are everlasting.",
    7: "I saw the tents of Cushan under distress — the tent curtains of the land of Midian were trembling.",
    8: "Did the LORD rage against the rivers, or was Your anger against the rivers, or was Your wrath against the sea — that You rode on Your horses, on Your chariots of salvation?",
    9: "Your bow was made bare — the rods of chastisement were sworn. Selah. You cleaved the earth with rivers.",
    10: "The mountains saw You and quaked. The downpour of waters swept by. The deep uttered forth its voice — it lifted high its hands.",
    11: "Sun and moon stood in their places. They went away at the light of Your arrows, at the radiance of Your gleaming spear.",
    12: "In indignation You marched through the earth. In anger You trampled the nations.",
    13: "You went forth for the salvation of Your people, for the salvation of Your anointed. You struck the head of the house of the evil — to lay him open from thigh to neck. Selah.",
    14: "You pierced with his own spears the head of his throngs. They stormed in to scatter us. Their exultation was like those who devour the oppressed in secret.",
    15: "You trampled on the sea with Your horses, on the surge of many waters.",
    16: "I heard, and my inward parts trembled. At the sound my lips quivered. Decay enters my bones, and in my place I tremble — because I must wait quietly for the day of distress, for the people to arise who will invade us.",
    17: "Though the fig tree should not blossom, and there be no fruit on the vines, though the yield of the olive should fail, and the fields produce no food, though the flock should be cut off from the fold, and there be no cattle in the stalls —",
    18: "yet I will exult in the LORD — I will rejoice in the God of my salvation.",
    19: "The Lord GOD is my strength. And He has made my feet like hinds' feet, and makes me walk on my high places. For the choir director, on my stringed instruments.",
}

# Haggai 1 — Consider your ways
hag_1 = {
    1: "In the second year of Darius the king, on the first day of the sixth month, the word of the LORD came by the prophet Haggai to Zerubbabel the son of Shealtiel, governor of Judah, and to Joshua the son of Jehozadak, the high priest, saying,",
    2: "\"Thus says the LORD of hosts — 'This people says, \"The time has not come, even the time for the house of the LORD to be rebuilt.\"'\"",
    3: "Then the word of the LORD came by Haggai the prophet, saying,",
    4: "\"Is it time for you yourselves to dwell in your paneled houses, while this house lies desolate?\"",
    5: "Now therefore, thus says the LORD of hosts — \"Consider your ways!",
    6: "You have sown much, but harvest little — you eat, but there is not enough to be satisfied. You drink, but there is not enough to become drunk. You put on clothing, but no one is warm enough — and he who earns, earns wages to put into a purse with holes.\"",
    7: "Thus says the LORD of hosts, \"Consider your ways!",
    8: "Go up to the mountains, bring wood and rebuild the temple, that I may be pleased with it and be glorified,\" says the LORD.",
    9: "\"You look for much, but behold, it comes to little. When you bring it home, I blow it away. Why?\" declares the LORD of hosts, \"Because of My house which lies desolate, while each of you runs to his own house.",
    10: "Therefore, because of you the sky has withheld its dew — and the earth has withheld its produce.",
    11: "And I called for a drought on the land, on the mountains, on the grain, on the new wine, on the oil, on what the ground produces, on men, on cattle, and on all the labor of your hands.\"",
    12: "Then Zerubbabel the son of Shealtiel, and Joshua the son of Jehozadak, the high priest, with all the remnant of the people, obeyed the voice of the LORD their God and the words of Haggai the prophet, as the LORD their God had sent him — and the people showed reverence for the LORD.",
    13: "Then Haggai, the messenger of the LORD, spoke by the commission of the LORD to the people, saying, \"'I am with you,' declares the LORD.\"",
    14: "So the LORD stirred up the spirit of Zerubbabel the son of Shealtiel, governor of Judah, and the spirit of Joshua the son of Jehozadak, the high priest, and the spirit of all the remnant of the people. And they came and worked on the house of the LORD of hosts, their God,",
    15: "on the twenty-fourth day of the sixth month in the second year of Darius the king.",
}
hag_2 = {
    1: "On the twenty-first of the seventh month, the word of the LORD came by Haggai the prophet, saying,",
    2: "\"Speak now to Zerubbabel the son of Shealtiel, governor of Judah, and to Joshua the son of Jehozadak, the high priest, and to the remnant of the people, saying,",
    3: "'Who is left among you who saw this temple in its former glory? And how do you see it now? Does it not seem to you like nothing in comparison?",
    4: "But now take courage, Zerubbabel,' declares the LORD, 'take courage also, Joshua son of Jehozadak, the high priest, and all you people of the land take courage,' declares the LORD, 'and work — for I am with you,' declares the LORD of hosts.",
    5: "'As for the promise which I made you when you came out of Egypt, My Spirit is abiding in your midst. Do not fear!'",
    6: "For thus says the LORD of hosts, 'Once more in a little while, I am going to shake the heavens and the earth, the sea also and the dry land.",
    7: "And I will shake all the nations, and they will come with the wealth of all nations — and I will fill this house with glory,' says the LORD of hosts.",
    8: "'The silver is Mine and the gold is Mine,' declares the LORD of hosts.",
    9: "'The latter glory of this house will be greater than the former,' says the LORD of hosts, 'and in this place I shall give peace,' declares the LORD of hosts.\"",
    10: "On the twenty-fourth of the ninth month, in the second year of Darius, the word of the LORD came to Haggai the prophet, saying,",
    11: "\"Thus says the LORD of hosts, 'Ask now the priests for a ruling:",
    12: "If a man carries holy meat in the fold of his garment, and touches bread with this fold, or cooked food, wine, oil, or any other food, will it become holy?'\" And the priests answered and said, \"No.\"",
    13: "Then Haggai said, \"If one who is unclean from a corpse touches any of these, will the latter become unclean?\" And the priests answered and said, \"It will become unclean.\"",
    14: "Then Haggai said, \"'So is this people. And so is this nation before Me,' declares the LORD, 'and so is every work of their hands. What they offer there is unclean.",
    15: "But now, do consider from this day onward — before one stone was placed on another in the temple of the LORD,",
    16: "from that time when one came to a grain heap of twenty measures, there would be only ten; and when one came to the wine vat to draw fifty measures, there would be only twenty.",
    17: "I smote you and every work of your hands with blasting wind, mildew and hail — yet you did not come back to Me,' declares the LORD.",
    18: "'Do consider from this day onward, from the twenty-fourth day of the ninth month — from the day when the temple of the LORD was founded, consider —",
    19: "Is the seed still in the barn? Even including the vine, the fig tree, the pomegranate and the olive tree — it has not borne fruit. Yet from this day on I will bless you.'\"",
    20: "Then the word of the LORD came a second time to Haggai on the twenty-fourth day of the month, saying,",
    21: "\"Speak to Zerubbabel governor of Judah, saying, 'I am going to shake the heavens and the earth.",
    22: "And I will overthrow the thrones of kingdoms, and destroy the power of the kingdoms of the nations — and I will overthrow the chariots and their riders, and the horses and their riders will go down, every one by the sword of another.'",
    23: "'On that day,' declares the LORD of hosts, 'I will take you, Zerubbabel, son of Shealtiel, My servant,' declares the LORD, 'and I will make you like a signet ring — for I have chosen you,' declares the LORD of hosts.\"",
}

ENTRIES = {}
for v, t in obad_1.items(): ENTRIES[f"31_1_{v}"] = t
for v, t in hab_1.items():  ENTRIES[f"35_1_{v}"] = t
for v, t in hab_2.items():  ENTRIES[f"35_2_{v}"] = t
for v, t in hab_3.items():  ENTRIES[f"35_3_{v}"] = t
for v, t in hag_1.items():  ENTRIES[f"37_1_{v}"] = t
for v, t in hag_2.items():  ENTRIES[f"37_2_{v}"] = t

def main():
    print(f"Short minor prophets verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
