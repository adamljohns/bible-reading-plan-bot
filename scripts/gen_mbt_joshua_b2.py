"""MBT generator: Joshua landmarks batch 2.

Book ID 6. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Joshua 2 (24 verses) — Rahab hides the spies; the scarlet cord
- Joshua 3 (17 verses) — crossing the Jordan on dry ground
- Joshua 4 (24 verses) — the twelve memorial stones at Gilgal
- Joshua 24 (33 verses) — Joshua's covenant at Shechem; "Choose you this day"

Total: 98 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Joshua 2 — Rahab and the spies
ch2 = {
    1: "Now Joshua the son of Nun sent out two men from Acacia Grove to spy secretly, saying, \"Go, view the land, especially Jericho.\" So they went, and came to the house of a harlot named Rahab, and lodged there.",
    2: "And it was told the king of Jericho, saying, \"Behold, men have come here tonight from the children of Israel to search out the country.\"",
    3: "So the king of Jericho sent to Rahab, saying, \"Bring out the men who have come to you, who have entered your house, for they have come to search out all the country.\"",
    4: "Then the woman took the two men and hid them. So she said, \"Yes, the men came to me, but I did not know where they were from.",
    5: "And it happened as the gate was being shut, when it was dark, that the men went out. Where the men went I do not know; pursue them quickly, for you may overtake them.\"",
    6: "(But she had brought them up to the roof and hidden them with the stalks of flax, which she had laid in order on the roof.)",
    7: "Then the men pursued them by the road to the Jordan, to the fords. And as soon as those who pursued them had gone out, they shut the gate.",
    8: "Now before they lay down, she came up to them on the roof,",
    9: "and said to the men: \"I know that the LORD has given you the land, that the terror of you has fallen on us, and that all the inhabitants of the land are fainthearted because of you.",
    10: "For we have heard how the LORD dried up the water of the Red Sea for you when you came out of Egypt, and what you did to the two kings of the Amorites who were on the other side of the Jordan, Sihon and Og, whom you utterly destroyed.",
    11: "And as soon as we heard these things, our hearts melted; neither did there remain any more courage in anyone because of you, for the LORD your God, He is God in heaven above and on earth beneath.",
    12: "Now therefore, I beg you, swear to me by the LORD, since I have shown you kindness, that you also will show kindness to my father's house, and give me a true token,",
    13: "and spare my father, my mother, my brothers, my sisters, and all that they have, and deliver our lives from death.\"",
    14: "So the men answered her, \"Our lives for yours, if none of you tell this business of ours. And it shall be, when the LORD has given us the land, that we will deal kindly and truly with you.\"",
    15: "Then she let them down by a rope through the window, for her house was on the city wall; she dwelt on the wall.",
    16: "And she said to them, \"Get to the mountain, lest the pursuers meet you. Hide there three days, until the pursuers have returned. Afterward you may go your way.\"",
    17: "So the men said to her: \"We will be blameless of this oath of yours which you have made us swear,",
    18: "unless, when we come into the land, you bind this line of scarlet cord in the window through which you let us down, and unless you bring your father, your mother, your brothers, and all your father's household to your own home.",
    19: "So it shall be that whoever goes outside the doors of your house into the street, his blood shall be on his own head, and we will be guiltless. And whoever is with you in the house, his blood shall be on our head if a hand is laid on him.",
    20: "And if you tell this business of ours, then we will be free from your oath which you made us swear.\"",
    21: "Then she said, \"According to your words, so be it.\" And she sent them away, and they departed. And she bound the scarlet cord in the window.",
    22: "They departed and went to the mountain, and stayed there three days until the pursuers returned. The pursuers sought them all along the way, but did not find them.",
    23: "So the two men returned, descended from the mountain, and crossed over; and they came to Joshua the son of Nun, and told him all that had happened to them.",
    24: "And they said to Joshua, \"Truly the LORD has delivered all the land into our hands, for indeed all the inhabitants of the country are fainthearted because of us.\"",
}

# Joshua 3 — crossing the Jordan
ch3 = {
    1: "Then Joshua rose early in the morning; and they set out from Acacia Grove and came to the Jordan, he and all the children of Israel, and lodged there before they crossed over.",
    2: "So it was, after three days, that the officers went through the camp;",
    3: "and they commanded the people, saying, \"When you see the ark of the covenant of the LORD your God, and the priests, the Levites, bearing it, then you shall set out from your place and go after it.",
    4: "Yet there shall be a space between you and it, about two thousand cubits by measure. Do not come near it, that you may know the way by which you must go, for you have not passed this way before.\"",
    5: "And Joshua said to the people, \"Sanctify yourselves, for tomorrow the LORD will do wonders among you.\"",
    6: "Then Joshua spoke to the priests, saying, \"Take up the ark of the covenant and cross over before the people.\" So they took up the ark of the covenant and went before the people.",
    7: "And the LORD said to Joshua, \"This day I will begin to exalt you in the sight of all Israel, that they may know that, as I was with Moses, so I will be with you.",
    8: "You shall command the priests who bear the ark of the covenant, saying, 'When you have come to the edge of the water of the Jordan, you shall stand in the Jordan.'\"",
    9: "So Joshua said to the children of Israel, \"Come here, and hear the words of the LORD your God.\"",
    10: "And Joshua said, \"By this you shall know that the living God is among you, and that He will without fail drive out from before you the Canaanites and the Hittites and the Hivites and the Perizzites and the Girgashites and the Amorites and the Jebusites:",
    11: "behold, the ark of the covenant of the Lord of all the earth is crossing over before you into the Jordan.",
    12: "Now therefore, take for yourselves twelve men from the tribes of Israel, one man from every tribe.",
    13: "And it shall come to pass, as soon as the soles of the feet of the priests who bear the ark of the LORD, the Lord of all the earth, shall rest in the waters of the Jordan, that the waters of the Jordan shall be cut off, the waters that come down from upstream, and they shall stand as a heap.\"",
    14: "So it was, when the people set out from their camp to cross over the Jordan, with the priests bearing the ark of the covenant before the people,",
    15: "and as those who bore the ark came to the Jordan, and the feet of the priests who bore the ark dipped in the edge of the water (for the Jordan overflows all its banks during the whole time of harvest),",
    16: "that the waters which came down from upstream stood still, and rose in a heap very far away at Adam, the city that is beside Zaretan. So the waters that went down into the Sea of the Arabah, the Salt Sea, failed, and were cut off; and the people crossed over opposite Jericho.",
    17: "Then the priests who bore the ark of the covenant of the LORD stood firm on dry ground in the midst of the Jordan; and all Israel crossed over on dry ground, until all the people had crossed completely over the Jordan.",
}

# Joshua 4 — the twelve memorial stones
ch4 = {
    1: "And it came to pass, when all the people had completely crossed over the Jordan, that the LORD spoke to Joshua, saying:",
    2: "\"Take for yourselves twelve men from the people, one man from every tribe,",
    3: "and command them, saying, 'Take for yourselves twelve stones from here, out of the midst of the Jordan, from the place where the priests' feet stood firm. You shall carry them over with you and leave them in the lodging place where you lodge tonight.'\"",
    4: "Then Joshua called the twelve men whom he had appointed from the children of Israel, one man from every tribe;",
    5: "and Joshua said to them: \"Cross over before the ark of the LORD your God into the midst of the Jordan, and each one of you take up a stone on his shoulder, according to the number of the tribes of the children of Israel,",
    6: "that this may be a sign among you when your children ask in time to come, saying, 'What do these stones mean to you?'",
    7: "Then you shall answer them that the waters of the Jordan were cut off before the ark of the covenant of the LORD; when it crossed over the Jordan, the waters of the Jordan were cut off. And these stones shall be for a memorial to the children of Israel forever.\"",
    8: "And the children of Israel did so, just as Joshua commanded, and took up twelve stones from the midst of the Jordan, as the LORD had spoken to Joshua, according to the number of the tribes of the children of Israel, and carried them over with them to the place where they lodged, and laid them down there.",
    9: "Then Joshua set up twelve stones in the midst of the Jordan, in the place where the feet of the priests who bore the ark of the covenant stood; and they are there to this day.",
    10: "So the priests who bore the ark stood in the midst of the Jordan until everything was finished that the LORD had commanded Joshua to speak to the people, according to all that Moses had commanded Joshua; and the people hurried and crossed over.",
    11: "Then it came to pass, when all the people had completely crossed over, that the ark of the LORD and the priests crossed over in the presence of the people.",
    12: "And the men of Reuben, the men of Gad, and half the tribe of Manasseh crossed over armed before the children of Israel, as Moses had spoken to them.",
    13: "About forty thousand prepared for war crossed over before the LORD for battle, to the plains of Jericho.",
    14: "On that day the LORD exalted Joshua in the sight of all Israel; and they feared him, as they had feared Moses, all the days of his life.",
    15: "Then the LORD spoke to Joshua, saying,",
    16: "\"Command the priests who bear the ark of the Testimony to come up from the Jordan.\"",
    17: "Joshua therefore commanded the priests, saying, \"Come up from the Jordan.\"",
    18: "And it came to pass, when the priests who bore the ark of the covenant of the LORD had come up from the midst of the Jordan, and the soles of the priests' feet touched the dry land, that the waters of the Jordan returned to their place and overflowed all its banks as before.",
    19: "Now the people came up from the Jordan on the tenth day of the first month, and they camped in Gilgal on the east border of Jericho.",
    20: "And those twelve stones which they took out of the Jordan, Joshua set up in Gilgal.",
    21: "Then he spoke to the children of Israel, saying: \"When your children ask their fathers in time to come, saying, 'What are these stones?'",
    22: "then you shall let your children know, saying, 'Israel crossed over this Jordan on dry land';",
    23: "for the LORD your God dried up the waters of the Jordan before you until you had crossed over, as the LORD your God did to the Red Sea, which He dried up before us until we had crossed over,",
    24: "that all the peoples of the earth may know the hand of the LORD, that it is mighty, that you may fear the LORD your God forever.\"",
}

# Joshua 24 — the covenant at Shechem; "Choose you this day"
ch24 = {
    1: "Then Joshua gathered all the tribes of Israel to Shechem and called for the elders of Israel, for their heads, for their judges, and for their officers; and they presented themselves before God.",
    2: "And Joshua said to all the people, \"Thus says the LORD God of Israel: 'Your fathers, including Terah, the father of Abraham and the father of Nahor, dwelt on the other side of the River in old times; and they served other gods.",
    3: "Then I took your father Abraham from the other side of the River, led him throughout all the land of Canaan, and multiplied his descendants and gave him Isaac.",
    4: "To Isaac I gave Jacob and Esau. To Esau I gave the mountains of Seir to possess, but Jacob and his children went down to Egypt.",
    5: "Also I sent Moses and Aaron, and I plagued Egypt, according to what I did among them. Afterward I brought you out.",
    6: "Then I brought your fathers out of Egypt, and you came to the sea; and the Egyptians pursued your fathers with chariots and horsemen to the Red Sea.",
    7: "So they cried out to the LORD; and He put darkness between you and the Egyptians, brought the sea upon them, and covered them. And your eyes saw what I did in Egypt. Then you dwelt in the wilderness a long time.",
    8: "And I brought you into the land of the Amorites, who dwelt on the other side of the Jordan, and they fought with you. But I gave them into your hand, that you might possess their land, and I destroyed them from before you.",
    9: "Then Balak the son of Zippor, king of Moab, arose to make war against Israel, and sent and called Balaam the son of Beor to curse you.",
    10: "But I would not listen to Balaam; therefore he continued to bless you. So I delivered you out of his hand.",
    11: "Then you went over the Jordan and came to Jericho. And the men of Jericho fought against you — also the Amorites, the Perizzites, the Canaanites, the Hittites, the Girgashites, the Hivites, and the Jebusites. But I delivered them into your hand.",
    12: "I sent the hornet before you which drove them out from before you, also the two kings of the Amorites, but not with your sword or with your bow.",
    13: "I have given you a land for which you did not labor, and cities which you did not build, and you dwell in them; you eat of the vineyards and olive groves which you did not plant.'",
    14: "Now therefore, fear the LORD, serve Him in sincerity and in truth, and put away the gods which your fathers served on the other side of the River and in Egypt. Serve the LORD!",
    15: "And if it seems evil to you to serve the LORD, choose for yourselves this day whom you will serve, whether the gods which your fathers served that were on the other side of the River, or the gods of the Amorites, in whose land you dwell. But as for me and my house, we will serve the LORD.\"",
    16: "So the people answered and said: \"Far be it from us that we should forsake the LORD to serve other gods;",
    17: "for the LORD our God is He who brought us and our fathers up out of the land of Egypt, from the house of bondage, who did those great signs in our sight, and preserved us in all the way that we went and among all the people through whom we passed.",
    18: "And the LORD drove out from before us all the people, including the Amorites who dwelt in the land. We also will serve the LORD, for He is our God.\"",
    19: "But Joshua said to the people, \"You cannot serve the LORD, for He is a holy God. He is a jealous God; He will not forgive your transgressions nor your sins.",
    20: "If you forsake the LORD and serve foreign gods, then He will turn and do you harm and consume you, after He has done you good.\"",
    21: "And the people said to Joshua, \"No, but we will serve the LORD!\"",
    22: "So Joshua said to the people, \"You are witnesses against yourselves that you have chosen the LORD for yourselves, to serve Him.\" And they said, \"We are witnesses!\"",
    23: "\"Now therefore,\" he said, \"put away the foreign gods which are among you, and incline your heart to the LORD God of Israel.\"",
    24: "And the people said to Joshua, \"The LORD our God we will serve, and His voice we will obey!\"",
    25: "So Joshua made a covenant with the people that day, and made for them a statute and an ordinance in Shechem.",
    26: "Then Joshua wrote these words in the Book of the Law of God. And he took a large stone, and set it up there under the oak that was by the sanctuary of the LORD.",
    27: "And Joshua said to all the people, \"Behold, this stone shall be a witness to us, for it has heard all the words of the LORD which He spoke to us. It shall therefore be a witness to you, lest you deny your God.\"",
    28: "So Joshua let the people depart, each to his own inheritance.",
    29: "Now it came to pass after these things that Joshua the son of Nun, the servant of the LORD, died, being one hundred and ten years old.",
    30: "And they buried him within the border of his inheritance at Timnath Serah, which is in the mountains of Ephraim, on the north side of Mount Gaash.",
    31: "Israel served the LORD all the days of Joshua, and all the days of the elders who outlived Joshua, who had known all the works of the LORD which He had done for Israel.",
    32: "The bones of Joseph, which the children of Israel had brought up out of Egypt, they buried at Shechem, in the plot of ground which Jacob had bought from the sons of Hamor the father of Shechem for one hundred pieces of silver, and which had become an inheritance of the children of Joseph.",
    33: "And Eleazar the son of Aaron died. They buried him in a hill belonging to Phinehas his son, which was given to him in the mountains of Ephraim.",
}

ENTRIES = {}
for v, t in ch2.items():
    ENTRIES[f"6_2_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"6_3_{v}"] = t
for v, t in ch4.items():
    ENTRIES[f"6_4_{v}"] = t
for v, t in ch24.items():
    ENTRIES[f"6_24_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Joshua landmarks batch 2 verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
