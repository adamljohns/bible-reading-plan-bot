"""MBT generator: Deuteronomy landmark chapters.

Book ID 5. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Deut 6 (25v) — the Shema; "love the LORD your God with all your heart"
- Deut 8 (20v) — wilderness lessons; "man does not live by bread alone"
- Deut 30 (20v) — "I have set before you life and death; choose life"
- Deut 32 (52v) — the Song of Moses

Total: 117 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Deuteronomy 6 — the Shema
ch6 = {
    1: "\"Now this is the commandment, and these are the statutes and judgments which the LORD your God has commanded to teach you, that you may observe them in the land which you are crossing over to possess,",
    2: "that you may fear the LORD your God, to keep all His statutes and His commandments which I command you, you and your son and your grandson, all the days of your life, and that your days may be prolonged.",
    3: "Therefore hear, O Israel, and be careful to observe it, that it may be well with you, and that you may multiply greatly as the LORD God of your fathers has promised you — a land flowing with milk and honey.",
    4: "\"Hear, O Israel: The LORD our God, the LORD is one!",
    5: "You shall love the LORD your God with all your heart, with all your soul, and with all your strength.",
    6: "And these words which I command you today shall be in your heart.",
    7: "You shall teach them diligently to your children, and shall talk of them when you sit in your house, when you walk by the way, when you lie down, and when you rise up.",
    8: "You shall bind them as a sign on your hand, and they shall be as frontlets between your eyes.",
    9: "You shall write them on the doorposts of your house and on your gates.",
    10: "\"So it shall be, when the LORD your God brings you into the land of which He swore to your fathers, to Abraham, Isaac, and Jacob, to give you large and beautiful cities which you did not build,",
    11: "houses full of all good things, which you did not fill, hewn-out wells which you did not dig, vineyards and olive trees which you did not plant — when you have eaten and are full —",
    12: "then beware, lest you forget the LORD who brought you out of the land of Egypt, from the house of bondage.",
    13: "You shall fear the LORD your God and serve Him, and shall take oaths in His name.",
    14: "You shall not go after other gods, the gods of the peoples who are all around you",
    15: "(for the LORD your God is a jealous God among you), lest the anger of the LORD your God be aroused against you and destroy you from the face of the earth.",
    16: "\"You shall not tempt the LORD your God as you tempted Him in Massah.",
    17: "You shall diligently keep the commandments of the LORD your God, His testimonies, and His statutes which He has commanded you.",
    18: "And you shall do what is right and good in the sight of the LORD, that it may be well with you, and that you may go in and possess the good land of which the LORD swore to your fathers,",
    19: "to cast out all your enemies from before you, as the LORD has spoken.",
    20: "\"When your son asks you in time to come, saying, 'What is the meaning of the testimonies, the statutes, and the judgments which the LORD our God has commanded you?'",
    21: "then you shall say to your son: 'We were slaves of Pharaoh in Egypt, and the LORD brought us out of Egypt with a mighty hand;",
    22: "and the LORD showed signs and wonders before our eyes, great and severe, against Egypt, Pharaoh, and all his household.",
    23: "Then He brought us out from there, that He might bring us in, to give us the land of which He swore to our fathers.",
    24: "And the LORD commanded us to observe all these statutes, to fear the LORD our God, for our good always, that He might preserve us alive, as it is this day.",
    25: "Then it will be righteousness for us, if we are careful to observe all these commandments before the LORD our God, as He has commanded us.'",
}

# Deuteronomy 8 — wilderness lessons
ch8 = {
    1: "\"Every commandment which I command you today you must be careful to observe, that you may live and multiply, and go in and possess the land of which the LORD swore to your fathers.",
    2: "And you shall remember that the LORD your God led you all the way these forty years in the wilderness, to humble you and test you, to know what was in your heart, whether you would keep His commandments or not.",
    3: "So He humbled you, allowed you to hunger, and fed you with manna which you did not know nor did your fathers know, that He might make you know that man shall not live by bread alone; but man lives by every word that proceeds from the mouth of the LORD.",
    4: "Your garments did not wear out on you, nor did your foot swell these forty years.",
    5: "You should know in your heart that as a man chastens his son, so the LORD your God chastens you.",
    6: "\"Therefore you shall keep the commandments of the LORD your God, to walk in His ways and to fear Him.",
    7: "For the LORD your God is bringing you into a good land, a land of brooks of water, of fountains and springs, that flow out of valleys and hills;",
    8: "a land of wheat and barley, of vines and fig trees and pomegranates, a land of olive oil and honey;",
    9: "a land in which you will eat bread without scarcity, in which you will lack nothing; a land whose stones are iron and out of whose hills you can dig copper.",
    10: "When you have eaten and are full, then you shall bless the LORD your God for the good land which He has given you.",
    11: "\"Beware that you do not forget the LORD your God by not keeping His commandments, His judgments, and His statutes which I command you today,",
    12: "lest — when you have eaten and are full, and have built beautiful houses and dwell in them;",
    13: "and when your herds and your flocks multiply, and your silver and your gold are multiplied, and all that you have is multiplied;",
    14: "when your heart is lifted up, and you forget the LORD your God who brought you out of the land of Egypt, from the house of bondage;",
    15: "who led you through that great and terrible wilderness, in which were fiery serpents and scorpions and thirsty land where there was no water; who brought water for you out of the flinty rock;",
    16: "who fed you in the wilderness with manna, which your fathers did not know, that He might humble you and that He might test you, to do you good in the end —",
    17: "then you say in your heart, 'My power and the might of my hand have gained me this wealth.'",
    18: "And you shall remember the LORD your God, for it is He who gives you power to get wealth, that He may establish His covenant which He swore to your fathers, as it is this day.",
    19: "Then it shall be, if you by any means forget the LORD your God, and follow other gods, and serve them and worship them, I testify against you this day that you shall surely perish.",
    20: "As the nations which the LORD destroys before you, so you shall perish, because you would not be obedient to the voice of the LORD your God.",
}

# Deuteronomy 30 — "choose life"
ch30 = {
    1: "\"Now it shall come to pass, when all these things come upon you, the blessing and the curse which I have set before you, and you call them to mind among all the nations where the LORD your God drives you,",
    2: "and you return to the LORD your God and obey His voice, according to all that I command you today, you and your children, with all your heart and with all your soul,",
    3: "that the LORD your God will bring you back from captivity, and have compassion on you, and gather you again from all the nations where the LORD your God has scattered you.",
    4: "If any of you are driven out to the farthest parts under heaven, from there the LORD your God will gather you, and from there He will bring you.",
    5: "Then the LORD your God will bring you to the land which your fathers possessed, and you shall possess it. He will prosper you and multiply you more than your fathers.",
    6: "And the LORD your God will circumcise your heart and the heart of your descendants, to love the LORD your God with all your heart and with all your soul, that you may live.",
    7: "Also the LORD your God will put all these curses on your enemies and on those who hate you, who persecuted you.",
    8: "And you will again obey the voice of the LORD and do all His commandments which I command you today.",
    9: "The LORD your God will make you abound in all the work of your hand, in the fruit of your body, in the increase of your livestock, and in the produce of your land for good. For the LORD will again rejoice over you for good as He rejoiced over your fathers,",
    10: "if you obey the voice of the LORD your God, to keep His commandments and His statutes which are written in this Book of the Law, and if you turn to the LORD your God with all your heart and with all your soul.",
    11: "\"For this commandment which I command you today is not too mysterious for you, nor is it far off.",
    12: "It is not in heaven, that you should say, 'Who will ascend into heaven for us and bring it to us, that we may hear it and do it?'",
    13: "Nor is it beyond the sea, that you should say, 'Who will go over the sea for us and bring it to us, that we may hear it and do it?'",
    14: "But the word is very near you, in your mouth and in your heart, that you may do it.",
    15: "\"See, I have set before you today life and good, death and evil,",
    16: "in that I command you today to love the LORD your God, to walk in His ways, and to keep His commandments, His statutes, and His judgments, that you may live and multiply; and the LORD your God will bless you in the land which you go to possess.",
    17: "But if your heart turns away so that you do not hear, and are drawn away, and worship other gods and serve them,",
    18: "I announce to you today that you shall surely perish; you shall not prolong your days in the land which you cross over the Jordan to go in and possess.",
    19: "I call heaven and earth as witnesses today against you, that I have set before you life and death, blessing and cursing; therefore choose life, that both you and your descendants may live;",
    20: "that you may love the LORD your God, that you may obey His voice, and that you may cling to Him, for He is your life and the length of your days; and that you may dwell in the land which the LORD swore to your fathers, to Abraham, Isaac, and Jacob, to give them.\"",
}

# Deuteronomy 32 — the Song of Moses
ch32 = {
    1: "\"Give ear, O heavens, and I will speak; and hear, O earth, the words of my mouth.",
    2: "Let my teaching drop as the rain, my speech distill as the dew, as raindrops on the tender herb, and as showers on the grass.",
    3: "For I proclaim the name of the LORD: ascribe greatness to our God.",
    4: "He is the Rock, His work is perfect; for all His ways are justice, a God of truth and without injustice; righteous and upright is He.",
    5: "They have corrupted themselves; they are not His children, because of their blemish — a perverse and crooked generation.",
    6: "Do you thus deal with the LORD, O foolish and unwise people? Is He not your Father, who bought you? Has He not made you and established you?",
    7: "\"Remember the days of old, consider the years of many generations. Ask your father, and he will show you; your elders, and they will tell you:",
    8: "when the Most High divided their inheritance to the nations, when He separated the sons of Adam, He set the boundaries of the peoples according to the number of the children of Israel.",
    9: "For the LORD's portion is His people; Jacob is the place of His inheritance.",
    10: "He found him in a desert land and in the wasteland, a howling wilderness; He encircled him, He instructed him, He kept him as the apple of His eye.",
    11: "As an eagle stirs up its nest, hovers over its young, spreading out its wings, taking them up, carrying them on its wings,",
    12: "so the LORD alone led him, and there was no foreign god with him.",
    13: "\"He made him ride in the heights of the earth, that he might eat the produce of the fields; He made him draw honey from the rock, and oil from the flinty rock;",
    14: "curds from the cattle, and milk of the flock, with fat of lambs; and rams of the breed of Bashan, and goats, with the choicest wheat; and you drank wine, the blood of the grapes.",
    15: "\"But Jeshurun grew fat and kicked; you grew fat, you grew thick, you are obese! Then he forsook God who made him, and scornfully esteemed the Rock of his salvation.",
    16: "They provoked Him to jealousy with foreign gods; with abominations they provoked Him to anger.",
    17: "They sacrificed to demons, not to God, to gods they did not know, to new gods, new arrivals that your fathers did not fear.",
    18: "Of the Rock who begot you, you are unmindful, and have forgotten the God who fathered you.",
    19: "\"And when the LORD saw it, He spurned them, because of the provocation of His sons and His daughters.",
    20: "And He said: 'I will hide My face from them, I will see what their end will be, for they are a perverse generation, children in whom is no faith.",
    21: "They have provoked Me to jealousy by what is not God; they have moved Me to anger by their foolish idols. But I will provoke them to jealousy by those who are not a nation; I will move them to anger by a foolish nation.",
    22: "For a fire is kindled in My anger, and shall burn to the lowest hell; it shall consume the earth with her increase, and set on fire the foundations of the mountains.",
    23: "'I will heap disasters on them; I will spend My arrows on them.",
    24: "They shall be wasted with hunger, devoured by pestilence and bitter destruction; I will also send against them the teeth of beasts, with the poison of serpents of the dust.",
    25: "The sword shall destroy outside; there shall be terror within for the young man and virgin, the nursing child with the man of gray hairs.",
    26: "I would have said, \"I will dash them in pieces, I will make the memory of them to cease from among men,\"",
    27: "had I not feared the wrath of the enemy, lest their adversaries should misunderstand, lest they should say, \"Our hand is high; and it is not the LORD who has done all this.\"'",
    28: "\"For they are a nation void of counsel, nor is there any understanding in them.",
    29: "Oh, that they were wise, that they understood this, that they would consider their latter end!",
    30: "How could one chase a thousand, and two put ten thousand to flight, unless their Rock had sold them, and the LORD had surrendered them?",
    31: "For their rock is not like our Rock, even our enemies themselves being judges.",
    32: "For their vine is of the vine of Sodom and of the fields of Gomorrah; their grapes are grapes of gall, their clusters are bitter.",
    33: "Their wine is the poison of serpents, and the cruel venom of cobras.",
    34: "'Is this not laid up in store with Me, sealed up among My treasures?",
    35: "Vengeance is Mine, and recompense; their foot shall slip in due time; for the day of their calamity is at hand, and the things to come hasten upon them.'",
    36: "\"For the LORD will judge His people and have compassion on His servants, when He sees that their power is gone, and there is no one remaining, bond or free.",
    37: "He will say: 'Where are their gods, the rock in which they sought refuge?",
    38: "Who ate the fat of their sacrifices, and drank the wine of their drink offering? Let them rise and help you, and be your refuge.",
    39: "'Now see that I, even I, am He, and there is no God besides Me; I kill and I make alive; I wound and I heal; nor is there any who can deliver from My hand.",
    40: "For I raise My hand to heaven, and say, \"As I live forever,",
    41: "if I whet My glittering sword, and My hand takes hold on judgment, I will render vengeance to My enemies, and repay those who hate Me.",
    42: "I will make My arrows drunk with blood, and My sword shall devour flesh, with the blood of the slain and the captives, from the heads of the leaders of the enemy.\"'",
    43: "\"Rejoice, O Gentiles, with His people; for He will avenge the blood of His servants, and render vengeance to His adversaries; He will provide atonement for His land and His people.\"",
    44: "So Moses came with Joshua the son of Nun and spoke all the words of this song in the hearing of the people.",
    45: "Moses finished speaking all these words to all Israel,",
    46: "and he said to them: \"Set your hearts on all the words which I testify among you today, which you shall command your children to be careful to observe — all the words of this law.",
    47: "For it is not a futile thing for you, because it is your life, and by this word you shall prolong your days in the land which you cross over the Jordan to possess.\"",
    48: "Then the LORD spoke to Moses that very same day, saying:",
    49: "\"Go up this mountain of the Abarim, Mount Nebo, which is in the land of Moab, across from Jericho; view the land of Canaan, which I give to the children of Israel as a possession;",
    50: "and die on the mountain which you ascend, and be gathered to your people, just as Aaron your brother died on Mount Hor and was gathered to his people;",
    51: "because you trespassed against Me among the children of Israel at the waters of Meribah Kadesh, in the Wilderness of Zin, because you did not hallow Me in the midst of the children of Israel.",
    52: "Yet you shall see the land before you, though you shall not go there, into the land which I am giving to the children of Israel.\"",
}

ENTRIES = {}
for v, t in ch6.items():
    ENTRIES[f"5_6_{v}"] = t
for v, t in ch8.items():
    ENTRIES[f"5_8_{v}"] = t
for v, t in ch30.items():
    ENTRIES[f"5_30_{v}"] = t
for v, t in ch32.items():
    ENTRIES[f"5_32_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Deuteronomy landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
