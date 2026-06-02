"""MBT generator: Numbers landmark chapters.

Book ID 4. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Numbers 21 (35 verses) — complaints + bronze serpent + Sihon and Og
- Numbers 22 (41 verses) — Balaam summoned; the talking donkey
- Numbers 23 (30 verses) — Balaam's first two oracles
- Numbers 24 (25 verses) — Balaam's third and fourth oracles; Star of Jacob

Total: 131 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Numbers 21 — bronze serpent + Sihon and Og
ch21 = {
    1: "The king of Arad, the Canaanite, who dwelt in the South, heard that Israel was coming on the road to Atharim. Then he fought against Israel and took some of them prisoners.",
    2: "So Israel made a vow to the LORD, and said, \"If You will indeed deliver this people into my hand, then I will utterly destroy their cities.\"",
    3: "And the LORD listened to the voice of Israel and delivered up the Canaanites, and they utterly destroyed them and their cities. So the name of that place was called Hormah.",
    4: "Then they journeyed from Mount Hor by the Way of the Red Sea, to go around the land of Edom; and the soul of the people became very discouraged on the way.",
    5: "And the people spoke against God and against Moses: \"Why have you brought us up out of Egypt to die in the wilderness? For there is no food and no water, and our soul loathes this worthless bread.\"",
    6: "So the LORD sent fiery serpents among the people, and they bit the people; and many of the people of Israel died.",
    7: "Therefore the people came to Moses, and said, \"We have sinned, for we have spoken against the LORD and against you; pray to the LORD that He take away the serpents from us.\" So Moses prayed for the people.",
    8: "Then the LORD said to Moses, \"Make a fiery serpent, and set it on a pole; and it shall be that everyone who is bitten, when he looks at it, shall live.\"",
    9: "So Moses made a bronze serpent, and put it on a pole; and so it was, if a serpent had bitten anyone, when he looked at the bronze serpent, he lived.",
    10: "Now the children of Israel moved on and camped in Oboth.",
    11: "And they journeyed from Oboth and camped at Ije Abarim, in the wilderness which is east of Moab, toward the sunrise.",
    12: "From there they moved and camped in the Valley of Zered.",
    13: "From there they moved and camped on the other side of the Arnon, which is in the wilderness that extends from the border of the Amorites; for the Arnon is the border of Moab, between Moab and the Amorites.",
    14: "Therefore it is said in the Book of the Wars of the LORD: \"Waheb in Suphah, the brooks of the Arnon,",
    15: "and the slope of the brooks that reaches to the dwelling of Ar, and lies on the border of Moab.\"",
    16: "From there they went to Beer, which is the well where the LORD said to Moses, \"Gather the people together, and I will give them water.\"",
    17: "Then Israel sang this song: \"Spring up, O well! All of you sing to it —",
    18: "the well the leaders sank, dug by the nation's nobles, by the lawgiver, with their staves.\" And from the wilderness they went to Mattanah,",
    19: "from Mattanah to Nahaliel, from Nahaliel to Bamoth,",
    20: "and from Bamoth, in the valley that is in the country of Moab, to the top of Pisgah which looks down on the wasteland.",
    21: "Then Israel sent messengers to Sihon king of the Amorites, saying,",
    22: "\"Let me pass through your land. We will not turn aside into fields or vineyards; we will not drink water from wells. We will go by the King's Highway until we have passed through your territory.\"",
    23: "But Sihon would not allow Israel to pass through his territory. So Sihon gathered all his people together and went out against Israel in the wilderness, and he came to Jahaz and fought against Israel.",
    24: "Then Israel defeated him with the edge of the sword, and took possession of his land from the Arnon to the Jabbok, as far as the people of Ammon; for the border of the people of Ammon was fortified.",
    25: "So Israel took all these cities, and Israel dwelt in all the cities of the Amorites, in Heshbon and in all its villages.",
    26: "For Heshbon was the city of Sihon king of the Amorites, who had fought against the former king of Moab, and had taken all his land from his hand as far as the Arnon.",
    27: "Therefore those who speak in proverbs say: \"Come to Heshbon, let it be built; let the city of Sihon be repaired.",
    28: "For fire went out from Heshbon, a flame from the city of Sihon; it consumed Ar of Moab, the lords of the heights of the Arnon.",
    29: "Woe to you, Moab! You have perished, O people of Chemosh! He has given his sons as fugitives, and his daughters into captivity, to Sihon king of the Amorites.",
    30: "But we have shot at them; Heshbon has perished as far as Dibon. Then we laid waste as far as Nophah, which reaches to Medeba.\"",
    31: "Thus Israel dwelt in the land of the Amorites.",
    32: "Then Moses sent to spy out Jazer; and they took its villages and drove out the Amorites who were there.",
    33: "And they turned and went up by the way to Bashan. So Og king of Bashan went out against them, he and all his people, to battle at Edrei.",
    34: "Then the LORD said to Moses, \"Do not fear him, for I have delivered him into your hand, with all his people and his land; and you shall do to him as you did to Sihon king of the Amorites, who dwelt at Heshbon.\"",
    35: "So they defeated him, his sons, and all his people, until there was no survivor left him; and they took possession of his land.",
}

# Numbers 22 — Balaam summoned; the talking donkey
ch22 = {
    1: "Then the children of Israel moved, and camped in the plains of Moab on the side of the Jordan across from Jericho.",
    2: "Now Balak the son of Zippor saw all that Israel had done to the Amorites.",
    3: "And Moab was exceedingly afraid of the people because they were many, and Moab was sick with dread because of the children of Israel.",
    4: "So Moab said to the elders of Midian, \"Now this company will lick up everything around us, as an ox licks up the grass of the field.\" And Balak the son of Zippor was king of the Moabites at that time.",
    5: "Then he sent messengers to Balaam the son of Beor at Pethor, which is near the River in the land of the sons of his people, to call him, saying: \"Look, a people has come from Egypt. See, they cover the face of the earth, and are settling next to me!",
    6: "Therefore please come at once, curse this people for me, for they are too mighty for me. Perhaps I shall be able to defeat them and drive them out of the land, for I know that he whom you bless is blessed, and he whom you curse is cursed.\"",
    7: "So the elders of Moab and the elders of Midian departed with the diviner's fee in their hand, and they came to Balaam and spoke to him the words of Balak.",
    8: "And he said to them, \"Lodge here tonight, and I will bring back word to you, as the LORD speaks to me.\" So the princes of Moab stayed with Balaam.",
    9: "Then God came to Balaam and said, \"Who are these men with you?\"",
    10: "So Balaam said to God, \"Balak the son of Zippor, king of Moab, has sent to me, saying,",
    11: "'Look, a people has come out of Egypt, and they cover the face of the earth. Come now, curse them for me; perhaps I shall be able to overpower them and drive them out.'\"",
    12: "And God said to Balaam, \"You shall not go with them; you shall not curse the people, for they are blessed.\"",
    13: "So Balaam rose in the morning and said to the princes of Balak, \"Go back to your land, for the LORD has refused to give me permission to go with you.\"",
    14: "And the princes of Moab rose and went to Balak, and said, \"Balaam refuses to come with us.\"",
    15: "Then Balak again sent princes, more numerous and more honorable than they.",
    16: "And they came to Balaam and said to him, \"Thus says Balak the son of Zippor: 'Please let nothing hinder you from coming to me;",
    17: "for I will certainly honor you greatly, and I will do whatever you say to me. Therefore please come, curse this people for me.'\"",
    18: "Then Balaam answered and said to the servants of Balak, \"Though Balak were to give me his house full of silver and gold, I could not go beyond the word of the LORD my God, to do less or more.",
    19: "Now therefore, please, you also stay here tonight, that I may know what more the LORD will say to me.\"",
    20: "And God came to Balaam at night and said to him, \"If the men come to call you, rise and go with them; but only the word which I speak to you — that you shall do.\"",
    21: "So Balaam rose in the morning, saddled his donkey, and went with the princes of Moab.",
    22: "Then God's anger was aroused because he went, and the Angel of the LORD took His stand in the way as an adversary against him. And he was riding on his donkey, and his two servants were with him.",
    23: "Now the donkey saw the Angel of the LORD standing in the way with His drawn sword in His hand, and the donkey turned aside out of the way and went into the field. So Balaam struck the donkey to turn her back onto the road.",
    24: "Then the Angel of the LORD stood in a narrow path between the vineyards, with a wall on this side and a wall on that side.",
    25: "And when the donkey saw the Angel of the LORD, she pushed herself against the wall and crushed Balaam's foot against the wall; so he struck her again.",
    26: "Then the Angel of the LORD went further, and stood in a narrow place where there was no way to turn either to the right hand or to the left.",
    27: "And when the donkey saw the Angel of the LORD, she lay down under Balaam; so Balaam's anger was aroused, and he struck the donkey with his staff.",
    28: "Then the LORD opened the mouth of the donkey, and she said to Balaam, \"What have I done to you, that you have struck me these three times?\"",
    29: "And Balaam said to the donkey, \"Because you have abused me. I wish there were a sword in my hand, for now I would kill you!\"",
    30: "So the donkey said to Balaam, \"Am I not your donkey on which you have ridden, ever since I became yours, to this day? Was I ever disposed to do this to you?\" And he said, \"No.\"",
    31: "Then the LORD opened Balaam's eyes, and he saw the Angel of the LORD standing in the way with His drawn sword in His hand; and he bowed his head and fell flat on his face.",
    32: "And the Angel of the LORD said to him, \"Why have you struck your donkey these three times? Behold, I have come out to stand against you, because your way is perverse before Me.",
    33: "The donkey saw Me and turned aside from Me these three times. If she had not turned aside from Me, surely I would also have killed you by now, and let her live.\"",
    34: "And Balaam said to the Angel of the LORD, \"I have sinned, for I did not know You stood in the way against me. Now therefore, if it displeases You, I will turn back.\"",
    35: "Then the Angel of the LORD said to Balaam, \"Go with the men, but only the word that I speak to you, that you shall speak.\" So Balaam went with the princes of Balak.",
    36: "Now when Balak heard that Balaam was coming, he went out to meet him at the city of Moab, which is on the border at the Arnon, the boundary of the territory.",
    37: "Then Balak said to Balaam, \"Did I not earnestly send to you, calling for you? Why did you not come to me? Am I not able to honor you?\"",
    38: "And Balaam said to Balak, \"Look, I have come to you! Now, have I any power at all to say anything? The word that God puts in my mouth, that I must speak.\"",
    39: "So Balaam went with Balak, and they came to Kirjath Huzoth.",
    40: "Then Balak offered oxen and sheep, and he sent some to Balaam and to the princes who were with him.",
    41: "So it was, the next day, that Balak took Balaam and brought him up to the high places of Baal, that from there he might observe the extent of the people.",
}

# Numbers 23 — Balaam's first two oracles
ch23 = {
    1: "Then Balaam said to Balak, \"Build seven altars for me here, and prepare for me here seven bulls and seven rams.\"",
    2: "And Balak did just as Balaam had spoken, and Balak and Balaam offered a bull and a ram on each altar.",
    3: "Then Balaam said to Balak, \"Stand by your burnt offering, and I will go; perhaps the LORD will come to meet me, and whatever He shows me I will tell you.\" So he went to a desolate height.",
    4: "And God met Balaam, and he said to Him, \"I have prepared the seven altars, and I have offered on each altar a bull and a ram.\"",
    5: "Then the LORD put a word in Balaam's mouth, and said, \"Return to Balak, and thus you shall speak.\"",
    6: "So he returned to him, and there he was, standing by his burnt offering, he and all the princes of Moab.",
    7: "And he took up his oracle and said: \"Balak the king of Moab has brought me from Aram, from the mountains of the east. 'Come, curse Jacob for me, and come, denounce Israel!'",
    8: "How shall I curse whom God has not cursed? And how shall I denounce whom the LORD has not denounced?",
    9: "For from the top of the rocks I see him, and from the hills I behold him; there! A people dwelling alone, not reckoning itself among the nations.",
    10: "Who can count the dust of Jacob, or number one-fourth of Israel? Let me die the death of the righteous, and let my end be like his!\"",
    11: "Then Balak said to Balaam, \"What have you done to me? I took you to curse my enemies, and look, you have blessed them bountifully!\"",
    12: "So he answered and said, \"Must I not take heed to speak what the LORD has put in my mouth?\"",
    13: "Then Balak said to him, \"Please come with me to another place from which you may see them; you shall see only the outer part of them, and shall not see them all; curse them for me from there.\"",
    14: "So he brought him to the field of Zophim, to the top of Pisgah, and built seven altars, and offered a bull and a ram on each altar.",
    15: "And he said to Balak, \"Stand here by your burnt offering while I meet the LORD over there.\"",
    16: "Then the LORD met Balaam, and put a word in his mouth, and said, \"Go back to Balak, and thus you shall speak.\"",
    17: "So he came to him, and there he was, standing by his burnt offering, and the princes of Moab were with him. And Balak said to him, \"What has the LORD spoken?\"",
    18: "Then he took up his oracle and said: \"Rise up, Balak, and hear! Listen to me, son of Zippor!",
    19: "God is not a man, that He should lie, nor a son of man, that He should repent. Has He said, and will He not do? Or has He spoken, and will He not make it good?",
    20: "Behold, I have received a command to bless; He has blessed, and I cannot reverse it.",
    21: "He has not observed iniquity in Jacob, nor has He seen wickedness in Israel. The LORD his God is with him, and the shout of a King is among them.",
    22: "God brings them out of Egypt; He has strength like a wild ox.",
    23: "For there is no sorcery against Jacob, nor any divination against Israel. It now must be said of Jacob and of Israel, 'Oh, what God has done!'",
    24: "Look, a people rises like a lioness, and lifts itself up like a lion; it shall not lie down until it devours the prey, and drinks the blood of the slain.\"",
    25: "Then Balak said to Balaam, \"Neither curse them at all, nor bless them at all!\"",
    26: "So Balaam answered and said to Balak, \"Did I not tell you, saying, 'All that the LORD speaks, that I must do'?\"",
    27: "Then Balak said to Balaam, \"Please come, I will take you to another place; perhaps it will please God that you may curse them for me from there.\"",
    28: "So Balak took Balaam to the top of Peor, that overlooks the wasteland.",
    29: "Then Balaam said to Balak, \"Build for me here seven altars, and prepare for me here seven bulls and seven rams.\"",
    30: "And Balak did as Balaam had said, and offered a bull and a ram on every altar.",
}

# Numbers 24 — Balaam's third and fourth oracles; Star of Jacob
ch24 = {
    1: "Now when Balaam saw that it pleased the LORD to bless Israel, he did not go as at other times, to seek to use sorcery, but he set his face toward the wilderness.",
    2: "And Balaam raised his eyes, and saw Israel encamped according to their tribes; and the Spirit of God came upon him.",
    3: "Then he took up his oracle and said: \"The utterance of Balaam the son of Beor, the utterance of the man whose eyes are opened,",
    4: "the utterance of him who hears the words of God, who sees the vision of the Almighty, who falls down, with eyes wide open:",
    5: "\"How lovely are your tents, O Jacob! Your dwellings, O Israel!",
    6: "Like valleys that stretch out, like gardens by the riverside, like aloes planted by the LORD, like cedars beside the waters.",
    7: "He shall pour water from his buckets, and his seed shall be in many waters. \"His king shall be higher than Agag, and his kingdom shall be exalted.",
    8: "\"God brings him out of Egypt; He has strength like a wild ox; he shall consume the nations, his enemies; he shall break their bones and pierce them with his arrows.",
    9: "'He bows down, he lies down as a lion; and as a lion, who shall rouse him?' \"Blessed is he who blesses you, and cursed is he who curses you.\"",
    10: "Then Balak's anger was aroused against Balaam, and he struck his hands together; and Balak said to Balaam, \"I called you to curse my enemies, and look, you have bountifully blessed them these three times!",
    11: "Now therefore, flee to your place. I said I would greatly honor you, but in fact, the LORD has kept you back from honor.\"",
    12: "So Balaam said to Balak, \"Did I not also speak to your messengers whom you sent to me, saying,",
    13: "'If Balak were to give me his house full of silver and gold, I could not go beyond the word of the LORD, to do good or bad of my own will. What the LORD says, that I must speak'?",
    14: "And now, indeed, I am going to my people. Come, I will advise you what this people will do to your people in the latter days.\"",
    15: "So he took up his oracle and said: \"The utterance of Balaam the son of Beor, and the utterance of the man whose eyes are opened;",
    16: "the utterance of him who hears the words of God, and has the knowledge of the Most High, who sees the vision of the Almighty, who falls down, with eyes wide open:",
    17: "\"I see Him, but not now; I behold Him, but not near; a Star shall come out of Jacob; a Scepter shall rise out of Israel, and batter the brow of Moab, and destroy all the sons of tumult.",
    18: "\"And Edom shall be a possession; Seir also, his enemies, shall be a possession, while Israel does valiantly.",
    19: "Out of Jacob One shall have dominion, and destroy the remains of the city.\"",
    20: "Then he looked on Amalek, and he took up his oracle and said: \"Amalek was first among the nations, but shall be last until he perishes.\"",
    21: "Then he looked on the Kenites, and he took up his oracle and said: \"Firm is your dwelling place, and your nest is set in the rock;",
    22: "nevertheless Kain shall be burned. How long until Asshur carries you away captive?\"",
    23: "Then he took up his oracle and said: \"Alas! Who shall live when God does this?",
    24: "But ships shall come from the coasts of Cyprus, and they shall afflict Asshur and afflict Eber, and so shall Amalek, until he perishes.\"",
    25: "So Balaam rose and departed and returned to his place; Balak also went his way.",
}

ENTRIES = {}
for v, t in ch21.items():
    ENTRIES[f"4_21_{v}"] = t
for v, t in ch22.items():
    ENTRIES[f"4_22_{v}"] = t
for v, t in ch23.items():
    ENTRIES[f"4_23_{v}"] = t
for v, t in ch24.items():
    ENTRIES[f"4_24_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Numbers landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
