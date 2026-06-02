"""MBT generator: Micah (complete book, 7 chapters, 105 verses).

Book ID 33. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Micah 6 was previously authored in the wisdom/prophets landmark
batch. This run fills in the rest of the book while preserving 6.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The word of the LORD that came to Micah of Moresheth in the days of Jotham, Ahaz, and Hezekiah, kings of Judah, which he saw concerning Samaria and Jerusalem.",
    2: "Hear, all you peoples! Listen, O earth, and all that is in it! Let the Lord GOD be a witness against you, the Lord from His holy temple.",
    3: "For behold, the LORD is coming out of His place; He will come down and tread on the high places of the earth.",
    4: "The mountains will melt under Him, and the valleys will split like wax before the fire, like waters poured down a steep place.",
    5: "All this is for the transgression of Jacob and for the sins of the house of Israel. What is the transgression of Jacob? Is it not Samaria? And what are the high places of Judah? Are they not Jerusalem?",
    6: "\"Therefore I will make Samaria a heap of ruins in the field, places for planting a vineyard; I will pour down her stones into the valley, and I will uncover her foundations.",
    7: "All her carved images shall be beaten to pieces, and all her pay as a harlot shall be burned with the fire; all her idols I will lay desolate, for she gathered it from the pay of a harlot, and they shall return to the pay of a harlot.\"",
    8: "Therefore I will wail and howl, I will go stripped and naked; I will make a wailing like the jackals and a mourning like the ostriches,",
    9: "for her wounds are incurable. For it has come to Judah; it has come to the gate of My people — to Jerusalem.",
    10: "Tell it not in Gath, weep not at all; in Beth Aphrah roll yourself in the dust.",
    11: "Pass by in naked shame, you inhabitant of Shaphir; the inhabitant of Zaanan does not go out. Beth Ezel mourns; its place to stand is taken away from you.",
    12: "For the inhabitant of Maroth pined for good, but disaster came down from the LORD to the gate of Jerusalem.",
    13: "O inhabitant of Lachish, harness the chariot to the swift steeds (she was the beginning of sin to the daughter of Zion), for the transgressions of Israel were found in you.",
    14: "Therefore you shall give presents to Moresheth Gath; the houses of Achzib shall be a lie to the kings of Israel.",
    15: "I will yet bring an heir to you, O inhabitant of Mareshah; the glory of Israel shall come to Adullam.",
    16: "Make yourself bald and cut off your hair, because of your precious children; enlarge your baldness like an eagle, for they shall go from you into captivity.",
}

ch2 = {
    1: "Woe to those who devise iniquity, and work out evil on their beds! At morning light they practice it, because it is in the power of their hand.",
    2: "They covet fields and take them by violence, also houses, and seize them. So they oppress a man and his house, a man and his inheritance.",
    3: "Therefore thus says the LORD: \"Behold, against this family I am devising disaster, from which you cannot remove your necks; nor shall you walk haughtily, for this is an evil time.",
    4: "In that day one shall take up a proverb against you, and lament with a bitter lamentation, saying: 'We are utterly destroyed! He has changed the heritage of my people; how He has removed it from me! To a turncoat He has divided our fields.'\"",
    5: "Therefore you will have no one to determine boundaries by lot in the assembly of the LORD.",
    6: "\"Do not prattle,\" you say to those who prophesy. So they shall not prophesy to you; they shall not return insult for insult.",
    7: "You who are named the house of Jacob: \"Is the Spirit of the LORD restricted? Are these His doings? Do not My words do good to him who walks uprightly?",
    8: "\"Lately My people have risen up as an enemy — you pull off the robe with the garment from those who trust you, as they pass by, like men returned from war.",
    9: "The women of My people you cast out from their pleasant houses; from their children you have taken away My glory forever.",
    10: "\"Arise and depart, for this is not your rest; because it is defiled, it shall destroy, yes, with utter destruction.",
    11: "If a man should walk in a false spirit and speak a lie, saying, 'I will prophesy to you of wine and drink,' even he would be the prattler of this people.",
    12: "\"I will surely assemble all of you, O Jacob, I will surely gather the remnant of Israel; I will put them together like sheep of the fold, like a flock in the midst of their pasture; they shall make a loud noise because of so many people.",
    13: "The one who breaks open will come up before them; they will break out, pass through the gate, and go out by it; their king will pass before them, with the LORD at their head.\"",
}

ch3 = {
    1: "And I said: \"Hear now, O heads of Jacob, and you rulers of the house of Israel: is it not for you to know justice?",
    2: "You who hate good and love evil; who strip the skin from My people, and the flesh from their bones;",
    3: "who also eat the flesh of My people, flay their skin from them, break their bones, and chop them in pieces like meat for the pot, like flesh in the caldron.\"",
    4: "Then they will cry to the LORD, but He will not hear them; He will even hide His face from them at that time, because they have been evil in their deeds.",
    5: "Thus says the LORD concerning the prophets who make My people stray; who chant \"Peace\" while they chew with their teeth, but who prepare war against him who puts nothing into their mouths:",
    6: "\"Therefore you shall have night without vision, and you shall have darkness without divination; the sun shall go down on the prophets, and the day shall be dark for them.",
    7: "So the seers shall be ashamed, and the diviners abashed; indeed they shall all cover their lips; for there is no answer from God.\"",
    8: "But truly I am full of power by the Spirit of the LORD, and of justice and might, to declare to Jacob his transgression and to Israel his sin.",
    9: "Now hear this, you heads of the house of Jacob and rulers of the house of Israel, who abhor justice and pervert all equity,",
    10: "who build up Zion with bloodshed and Jerusalem with iniquity:",
    11: "her heads judge for a bribe, her priests teach for pay, and her prophets divine for money. Yet they lean on the LORD, and say, \"Is not the LORD among us? No harm can come upon us.\"",
    12: "Therefore because of you Zion shall be plowed like a field, Jerusalem shall become heaps of ruins, and the mountain of the temple like the bare hills of the forest.",
}

ch4 = {
    1: "Now it shall come to pass in the latter days that the mountain of the LORD's house shall be established on the top of the mountains, and shall be exalted above the hills; and peoples shall flow to it.",
    2: "Many nations shall come and say, \"Come, and let us go up to the mountain of the LORD, to the house of the God of Jacob; He will teach us His ways, and we shall walk in His paths.\" For out of Zion the law shall go forth, and the word of the LORD from Jerusalem.",
    3: "He shall judge between many peoples, and rebuke strong nations afar off; they shall beat their swords into plowshares, and their spears into pruning hooks; nation shall not lift up sword against nation, neither shall they learn war anymore.",
    4: "But everyone shall sit under his vine and under his fig tree, and no one shall make them afraid; for the mouth of the LORD of hosts has spoken.",
    5: "For all people walk each in the name of his god, but we will walk in the name of the LORD our God forever and ever.",
    6: "\"In that day,\" says the LORD, \"I will assemble the lame, I will gather the outcast and those whom I have afflicted;",
    7: "I will make the lame a remnant, and the outcast a strong nation; so the LORD will reign over them in Mount Zion from now on, even forever.",
    8: "And you, O tower of the flock, the stronghold of the daughter of Zion, to you shall it come, even the former dominion shall come, the kingdom of the daughter of Jerusalem.\"",
    9: "Now why do you cry aloud? Is there no king in your midst? Has your counselor perished? For pangs have seized you like a woman in labor.",
    10: "Be in pain, and labor to bring forth, O daughter of Zion, like a woman in birth pangs. For now you shall go forth from the city, you shall dwell in the field, and to Babylon you shall go. There you shall be delivered; there the LORD will redeem you from the hand of your enemies.",
    11: "Now also many nations have gathered against you, who say, \"Let her be defiled, and let our eye look upon Zion.\"",
    12: "But they do not know the thoughts of the LORD, nor do they understand His counsel; for He will gather them like sheaves to the threshing floor.",
    13: "\"Arise and thresh, O daughter of Zion; for I will make your horn iron, and I will make your hooves bronze; you shall beat in pieces many peoples; I will consecrate their gain to the LORD, and their substance to the Lord of the whole earth.\"",
}

ch5 = {
    1: "Now gather yourself in troops, O daughter of troops; he has laid siege against us; they will strike the judge of Israel with a rod on the cheek.",
    2: "\"But you, Bethlehem Ephrathah, though you are little among the thousands of Judah, yet out of you shall come forth to Me the One to be Ruler in Israel, whose goings forth are from of old, from everlasting.\"",
    3: "Therefore He shall give them up, until the time that she who is in labor has given birth; then the remnant of His brethren shall return to the children of Israel.",
    4: "And He shall stand and feed His flock in the strength of the LORD, in the majesty of the name of the LORD His God; and they shall abide, for now He shall be great to the ends of the earth;",
    5: "and this One shall be peace. When the Assyrian comes into our land, and when he treads in our palaces, then we will raise against him seven shepherds and eight princely men.",
    6: "They shall waste with the sword the land of Assyria, and the land of Nimrod at its entrances; thus He shall deliver us from the Assyrian, when he comes into our land and when he treads within our borders.",
    7: "Then the remnant of Jacob shall be in the midst of many peoples, like dew from the LORD, like showers on the grass, that tarry for no man nor wait for the sons of men.",
    8: "And the remnant of Jacob shall be among the Gentiles, in the midst of many peoples, like a lion among the beasts of the forest, like a young lion among flocks of sheep, who, if he passes through, both treads down and tears in pieces, and none can deliver.",
    9: "Your hand shall be lifted against your adversaries, and all your enemies shall be cut off.",
    10: "\"And it shall be in that day,\" says the LORD, \"that I will cut off your horses from your midst and destroy your chariots.",
    11: "I will cut off the cities of your land and throw down all your strongholds.",
    12: "I will cut off sorceries from your hand, and you shall have no soothsayers.",
    13: "Your carved images I will also cut off, and your sacred pillars from your midst; you shall no more worship the work of your hands;",
    14: "I will pluck your wooden images from your midst; thus I will destroy your cities.",
    15: "And I will execute vengeance in anger and fury on the nations that have not heard.\"",
}

ch6 = {
    1: "Hear now what the LORD says: \"Arise, plead your case before the mountains, and let the hills hear your voice.",
    2: "Hear, O you mountains, the LORD's complaint, and you strong foundations of the earth; for the LORD has a complaint against His people, and He will contend with Israel.",
    3: "\"O My people, what have I done to you? And how have I wearied you? Testify against Me.",
    4: "For I brought you up from the land of Egypt, I redeemed you from the house of bondage; and I sent before you Moses, Aaron, and Miriam.",
    5: "O My people, remember now what Balak king of Moab counseled, and what Balaam the son of Beor answered him, from Acacia Grove to Gilgal, that you may know the righteousness of the LORD.\"",
    6: "With what shall I come before the LORD, and bow myself before the High God? Shall I come before Him with burnt offerings, with calves a year old?",
    7: "Will the LORD be pleased with thousands of rams, or ten thousand rivers of oil? Shall I give my firstborn for my transgression, the fruit of my body for the sin of my soul?",
    8: "He has shown you, O man, what is good; and what does the LORD require of you but to do justly, to love mercy, and to walk humbly with your God?",
    9: "The LORD's voice cries to the city — wisdom shall see Your name: \"Hear the rod! Who has appointed it?",
    10: "Are there yet the treasures of wickedness in the house of the wicked, and the short measure that is an abomination?",
    11: "Shall I count pure those with the wicked scales, and with the bag of deceitful weights?",
    12: "For her rich men are full of violence, her inhabitants have spoken lies, and their tongue is deceitful in their mouth.",
    13: "\"Therefore I will also make you sick by striking you, by making you desolate because of your sins.",
    14: "You shall eat, but not be satisfied; hunger shall be in your midst. You may carry some away, but shall not save them; and what you do rescue I will give over to the sword.",
    15: "You shall sow, but not reap; you shall tread the olives, but not anoint yourselves with oil; and make sweet wine, but not drink wine.",
    16: "For the statutes of Omri are kept; all the works of Ahab's house are done; and you walk in their counsels, that I may make you a desolation, and your inhabitants a hissing. Therefore you shall bear the reproach of My people.\"",
}

ch7 = {
    1: "Woe is me! For I am like those who gather summer fruits, like those who glean vintage grapes; there is no cluster to eat of the first-ripe fruit which my soul desires.",
    2: "The faithful man has perished from the earth, and there is no one upright among men. They all lie in wait for blood; every man hunts his brother with a net.",
    3: "That they may successfully do evil with both hands — the prince asks for gifts, the judge seeks a bribe, and the great man utters his evil desire; so they scheme together.",
    4: "The best of them is like a brier; the most upright is sharper than a thorn hedge; the day of your watchman and your punishment comes; now shall be their perplexity.",
    5: "Do not trust in a friend; do not put your confidence in a companion; guard the doors of your mouth from her who lies in your bosom.",
    6: "For son dishonors father, daughter rises against her mother, daughter-in-law against her mother-in-law; a man's enemies are the men of his own household.",
    7: "Therefore I will look to the LORD; I will wait for the God of my salvation; my God will hear me.",
    8: "Do not rejoice over me, my enemy; when I fall, I will arise; when I sit in darkness, the LORD will be a light to me.",
    9: "I will bear the indignation of the LORD, because I have sinned against Him, until He pleads my case and executes justice for me. He will bring me forth to the light; I will see His righteousness.",
    10: "Then she who is my enemy will see, and shame will cover her who said to me, \"Where is the LORD your God?\" My eyes will see her; now she will be trampled down like mud in the streets.",
    11: "In the day when your walls are to be built, in that day the decree shall go far and wide.",
    12: "In that day they shall come to you from Assyria and the fortified cities, from the fortress to the River, from sea to sea, and mountain to mountain.",
    13: "Yet the land shall be desolate because of those who dwell in it, and for the fruit of their deeds.",
    14: "Shepherd Your people with Your staff, the flock of Your heritage, who dwell solitarily in a woodland, in the midst of Carmel; let them feed in Bashan and Gilead, as in days of old.",
    15: "\"As in the days when you came out of the land of Egypt, I will show them wonders.\"",
    16: "The nations shall see and be ashamed of all their might; they shall put their hand over their mouth; their ears shall be deaf.",
    17: "They shall lick the dust like a serpent; they shall crawl from their holes like snakes of the earth. They shall be afraid of the LORD our God, and shall fear because of You.",
    18: "Who is a God like You, pardoning iniquity and passing over the transgression of the remnant of His heritage? He does not retain His anger forever, because He delights in mercy.",
    19: "He will again have compassion on us, and will subdue our iniquities. You will cast all our sins into the depths of the sea.",
    20: "You will give truth to Jacob and mercy to Abraham, which You have sworn to our fathers from days of old.",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5, 6: ch6, 7: ch7}


def main():
    data = json.loads(MOOP_PATH.read_text())
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"33_{ch}_{v}"] = text
    data.update(new_entries)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Micah verses authored: {len(new_entries)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
