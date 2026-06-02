"""MBT OT historical narrative landmarks.

Joshua 1:1-9 (be strong + courageous), Joshua 24:14-15 (as for me),
1 Samuel 17 (David & Goliath), 1 Kings 18 (Elijah on Carmel),
1 Kings 19 (still small voice), 2 Kings 2:1-15 (Elijah taken up),
Nehemiah 8 (Ezra reads the Law).
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Joshua 1:1-9 — Be strong and courageous
josh_1 = {
    1: "Now it came about after the death of Moses the servant of the LORD, that the LORD spoke to Joshua the son of Nun, Moses' servant, saying,",
    2: "\"Moses My servant is dead. Now therefore arise, cross this Jordan, you and all this people, to the land which I am giving to them, to the sons of Israel.",
    3: "Every place on which the sole of your foot treads, I have given it to you, just as I spoke to Moses.",
    4: "From the wilderness and this Lebanon, even as far as the great river, the river Euphrates, all the land of the Hittites — and as far as the Great Sea toward the setting of the sun, shall be your territory.",
    5: "No man will be able to stand before you all the days of your life. Just as I have been with Moses, I will be with you — I will not fail you or forsake you.",
    6: "Be strong and courageous, for you shall give this people possession of the land which I swore to their fathers to give them.",
    7: "Only be strong and very courageous — be careful to do according to all the law which Moses My servant commanded you. Do not turn from it to the right or to the left, so that you may have success wherever you go.",
    8: "This book of the law shall not depart from your mouth, but you shall meditate on it day and night — so that you may be careful to do according to all that is written in it. For then you will make your way prosperous, and then you will have success.",
    9: "Have I not commanded you? Be strong and courageous! Do not tremble or be dismayed — for the LORD your God is with you wherever you go.\"",
}

# Joshua 24:14-15 — As for me and my house
josh_24 = {
    14: "\"Now therefore, fear the LORD and serve Him in sincerity and truth — and put away the gods which your fathers served beyond the River and in Egypt, and serve the LORD.",
    15: "And if it is disagreeable in your sight to serve the LORD, choose for yourselves today whom you will serve — whether the gods which your fathers served, which were beyond the River, or the gods of the Amorites in whose land you are living. But as for me and my house, we will serve the LORD.\"",
}

# 1 Samuel 17 — David and Goliath
sam_17 = {
    1: "Now the Philistines gathered their armies for battle, and they were gathered at Socoh which belongs to Judah. And they camped between Socoh and Azekah, in Ephes-dammim.",
    2: "And Saul and the men of Israel were gathered, and camped in the valley of Elah, and drew up in battle array to encounter the Philistines.",
    3: "And the Philistines stood on the mountain on one side while Israel stood on the mountain on the other side, with the valley between them.",
    4: "Then a champion came out from the armies of the Philistines, named Goliath, from Gath — whose height was six cubits and a span.",
    5: "And he had a bronze helmet on his head, and he was clothed with scale armor — and the weight of the armor was five thousand shekels of bronze.",
    6: "He also had bronze greaves on his legs and a bronze javelin slung between his shoulders.",
    7: "And the shaft of his spear was like a weaver's beam, and the head of his spear weighed six hundred shekels of iron. His shield-carrier also walked before him.",
    8: "And he stood and shouted to the ranks of Israel, and said to them, \"Why do you come out to draw up in battle array? Am I not the Philistine, and you servants of Saul? Choose a man for yourselves, and let him come down to me.",
    9: "If he is able to fight with me and kill me, then we will become your servants. But if I prevail against him and kill him, then you shall become our servants and serve us.\"",
    10: "Again the Philistine said, \"I defy the ranks of Israel this day. Give me a man, that we may fight together.\"",
    11: "And when Saul and all Israel heard these words of the Philistine, they were dismayed and greatly afraid.",
    12: "Now David was the son of the Ephrathite of Bethlehem in Judah, whose name was Jesse — and he had eight sons. And Jesse was old in the days of Saul, advanced in years among men.",
    13: "And the three older sons of Jesse had gone after Saul to the battle. And the names of his three sons who went to the battle were Eliab the first-born, and the second to him Abinadab, and the third Shammah.",
    14: "And David was the youngest. Now the three oldest followed Saul,",
    15: "but David went back and forth from Saul to tend his father's flock at Bethlehem.",
    16: "And the Philistine came forward morning and evening for forty days, and took his stand.",
    17: "Then Jesse said to David his son, \"Take now for your brothers an ephah of this roasted grain and these ten loaves, and run to the camp to your brothers.",
    18: "Bring also these ten cuts of cheese to the commander of their thousand, and look into the welfare of your brothers — and bring back news of them.",
    19: "For Saul and they and all the men of Israel are in the valley of Elah, fighting with the Philistines.\"",
    20: "So David arose early in the morning and left the flock with a keeper. And he took the supplies and went as Jesse had commanded him. And he came to the circle of the camp while the army was going out in battle array shouting the war cry.",
    21: "And Israel and the Philistines drew up in battle array, army against army.",
    22: "Then David left his baggage in the care of the baggage keeper, and ran to the battle line and entered in order to greet his brothers.",
    23: "And as he was talking with them, behold, the champion, the Philistine from Gath named Goliath, was coming up from the army of the Philistines, and he spoke these same words — and David heard them.",
    24: "And when all the men of Israel saw the man, they fled from him and were greatly afraid.",
    25: "And the men of Israel said, \"Have you seen this man who is coming up? Surely he is coming up to defy Israel. And it will be that the king will enrich the man who kills him with great riches, and will give him his daughter, and make his father's house free in Israel.\"",
    26: "Then David spoke to the men who were standing by him, saying, \"What will be done for the man who kills this Philistine, and takes away the reproach from Israel? For who is this uncircumcised Philistine, that he should taunt the armies of the living God?\"",
    27: "And the people answered him in accord with this word, saying, \"Thus it will be done for the man who kills him.\"",
    28: "Now Eliab his oldest brother heard when he spoke to the men. And Eliab's anger burned against David and he said, \"Why have you come down? And with whom have you left those few sheep in the wilderness? I know your insolence and the wickedness of your heart — for you have come down in order to see the battle.\"",
    29: "But David said, \"What have I done now? Was it not just a question?\"",
    30: "Then he turned away from him to another and said the same thing. And the people answered the same thing as before.",
    31: "When the words which David spoke were heard, they told them to Saul — and he sent for him.",
    32: "And David said to Saul, \"Let no man's heart fail on account of him. Your servant will go and fight with this Philistine.\"",
    33: "Then Saul said to David, \"You are not able to go against this Philistine to fight with him — for you are but a youth, while he has been a warrior from his youth.\"",
    34: "But David said to Saul, \"Your servant was tending his father's sheep. When a lion or a bear came and took a lamb from the flock,",
    35: "I went out after him and attacked him, and rescued it from his mouth. And when he rose up against me, I seized him by his beard and struck him and killed him.",
    36: "Your servant has killed both the lion and the bear — and this uncircumcised Philistine will be like one of them, since he has taunted the armies of the living God.\"",
    37: "And David said, \"The LORD who delivered me from the paw of the lion and from the paw of the bear, He will deliver me from the hand of this Philistine.\" And Saul said to David, \"Go, and may the LORD be with you.\"",
    38: "Then Saul clothed David with his garments and put a bronze helmet on his head, and he clothed him with armor.",
    39: "And David girded his sword over his armor and tried to walk, for he had not tested them. So David said to Saul, \"I cannot go with these, for I have not tested them.\" And David took them off.",
    40: "And he took his stick in his hand and chose for himself five smooth stones from the brook, and put them in the shepherd's bag which he had, even in his pouch. And his sling was in his hand, and he approached the Philistine.",
    41: "And the Philistine came on and approached David, with the shield-bearer in front of him.",
    42: "And when the Philistine looked and saw David, he disdained him — for he was but a youth, and ruddy, with a handsome appearance.",
    43: "And the Philistine said to David, \"Am I a dog, that you come to me with sticks?\" And the Philistine cursed David by his gods.",
    44: "The Philistine also said to David, \"Come to me, and I will give your flesh to the birds of the sky and the beasts of the field.\"",
    45: "Then David said to the Philistine, \"You come to me with a sword, a spear, and a javelin — but I come to you in the name of the LORD of hosts, the God of the armies of Israel, whom you have taunted.",
    46: "This day the LORD will deliver you up into my hands. And I will strike you down and remove your head from you, and I will give the dead bodies of the army of the Philistines this day to the birds of the sky and the wild beasts of the earth — that all the earth may know that there is a God in Israel.",
    47: "And that all this assembly may know that the LORD does not deliver by sword or by spear. For the battle is the LORD's, and He will give you into our hands.\"",
    48: "Then it happened when the Philistine rose and came and drew near to meet David, that David ran quickly toward the battle line to meet the Philistine.",
    49: "And David put his hand into his bag and took from it a stone, and slung it, and struck the Philistine on his forehead — and the stone sank into his forehead, so that he fell on his face to the ground.",
    50: "Thus David prevailed over the Philistine with a sling and a stone, and he struck the Philistine and killed him — but there was no sword in David's hand.",
    51: "Then David ran and stood over the Philistine, and took his sword and drew it out of its sheath and killed him, and cut off his head with it. When the Philistines saw that their champion was dead, they fled.",
    52: "And the men of Israel and Judah arose and shouted and pursued the Philistines as far as the valley, and to the gates of Ekron. And the slain Philistines lay along the way to Shaaraim, even to Gath and Ekron.",
    53: "And the sons of Israel returned from chasing the Philistines and plundered their camps.",
    54: "Then David took the Philistine's head and brought it to Jerusalem — but he put his weapons in his tent.",
    55: "Now when Saul saw David going out against the Philistine, he said to Abner the commander of the army, \"Abner, whose son is this young man?\" And Abner said, \"By your life, O king, I do not know.\"",
    56: "And the king said, \"You inquire whose son the youth is.\"",
    57: "So when David returned from killing the Philistine, Abner took him and brought him before Saul with the Philistine's head in his hand.",
    58: "And Saul said to him, \"Whose son are you, young man?\" And David answered, \"I am the son of your servant Jesse the Bethlehemite.\"",
}

# 1 Kings 18:20-46 — Elijah on Carmel (the showdown)
kings_18 = {
    20: "So Ahab sent a message among all the sons of Israel, and brought the prophets together at Mount Carmel.",
    21: "And Elijah came near to all the people and said, \"How long will you hesitate between two opinions? If the LORD is God, follow Him — but if Baal, follow him.\" But the people did not answer him a word.",
    22: "Then Elijah said to the people, \"I alone am left a prophet of the LORD, but Baal's prophets are 450 men.",
    23: "Now let them give us two oxen. And let them choose one ox for themselves, and cut it up, and place it on the wood — but put no fire under it. And I will prepare the other ox, and lay it on the wood, and I will not put a fire under it.",
    24: "Then you call on the name of your god, and I will call on the name of the LORD — and the God who answers by fire, He is God.\" And all the people answered and said, \"That is a good idea.\"",
    25: "So Elijah said to the prophets of Baal, \"Choose one ox for yourselves and prepare it first, for you are many. And call on the name of your god, but put no fire under it.\"",
    26: "Then they took the ox which was given them, and they prepared it and called on the name of Baal from morning until noon, saying, \"O Baal, answer us!\" But there was no voice and no one answered. And they leaped about the altar which they had made.",
    27: "And it came about at noon, that Elijah mocked them, and said, \"Call out with a loud voice — for he is a god. Either he is occupied or gone aside, or is on a journey, or perhaps he is asleep and needs to be awakened.\"",
    28: "So they cried with a loud voice and cut themselves according to their custom with swords and lances until the blood gushed out on them.",
    29: "And it came about when midday was past, that they raved until the time of the offering of the evening sacrifice — but there was no voice, no one answered, and no one paid attention.",
    30: "Then Elijah said to all the people, \"Come near to me.\" So all the people came near to him. And he repaired the altar of the LORD which had been torn down.",
    31: "And Elijah took twelve stones according to the number of the tribes of the sons of Jacob, to whom the word of the LORD had come, saying, \"Israel shall be your name.\"",
    32: "So with the stones he built an altar in the name of the LORD. And he made a trench around the altar, large enough to hold two measures of seed.",
    33: "Then he arranged the wood and cut the ox in pieces and laid it on the wood. And he said, \"Fill four pitchers with water and pour it on the burnt offering and on the wood.\"",
    34: "And he said, \"Do it a second time.\" And they did it a second time. And he said, \"Do it a third time.\" And they did it a third time.",
    35: "And the water flowed around the altar — and he also filled the trench with water.",
    36: "Then it came about at the time of the offering of the evening sacrifice, that Elijah the prophet came near and said, \"O LORD, the God of Abraham, Isaac and Israel, today let it be known that You are God in Israel, and that I am Your servant, and that I have done all these things at Your word.",
    37: "Answer me, O LORD, answer me — that this people may know that You, O LORD, are God, and that You have turned their heart back again.\"",
    38: "Then the fire of the LORD fell, and consumed the burnt offering and the wood and the stones and the dust, and licked up the water that was in the trench.",
    39: "And when all the people saw it, they fell on their faces and said, \"The LORD, He is God! The LORD, He is God!\"",
    40: "Then Elijah said to them, \"Seize the prophets of Baal. Do not let one of them escape.\" So they seized them — and Elijah brought them down to the brook Kishon, and slew them there.",
    41: "Now Elijah said to Ahab, \"Go up, eat and drink — for there is the sound of the roar of a heavy shower.\"",
    42: "So Ahab went up to eat and drink. But Elijah went up to the top of Carmel, and he crouched down on the earth, and put his face between his knees.",
    43: "And he said to his servant, \"Go up now, look toward the sea.\" So he went up and looked and said, \"There is nothing.\" And he said, \"Go back\" seven times.",
    44: "And it came about at the seventh time, that he said, \"Behold, a cloud as small as a man's hand is coming up from the sea.\" And he said, \"Go up, say to Ahab, 'Prepare your chariot and go down, so that the heavy shower does not stop you.'\"",
    45: "And it came about in a little while, that the sky grew black with clouds and wind, and there was a heavy shower. And Ahab rode and went to Jezreel.",
    46: "Then the hand of the LORD was on Elijah, and he girded up his loins and outran Ahab to Jezreel.",
}

# 1 Kings 19 — Elijah at Horeb, still small voice
kings_19 = {
    1: "Now Ahab told Jezebel all that Elijah had done, and how he had killed all the prophets with the sword.",
    2: "Then Jezebel sent a messenger to Elijah, saying, \"So may the gods do to me and even more, if I do not make your life as the life of one of them by tomorrow about this time.\"",
    3: "And he was afraid, and arose and ran for his life — and came to Beersheba which belongs to Judah, and left his servant there.",
    4: "But he himself went a day's journey into the wilderness, and came and sat down under a juniper tree. And he requested for himself that he might die, and said, \"It is enough — now, O LORD, take my life, for I am not better than my fathers.\"",
    5: "And he lay down and slept under a juniper tree. And behold, an angel touched him and said to him, \"Arise — eat.\"",
    6: "Then he looked, and behold, there was at his head a bread cake baked on hot stones, and a jar of water. So he ate and drank, and lay down again.",
    7: "And the angel of the LORD came again a second time and touched him and said, \"Arise — eat, because the journey is too great for you.\"",
    8: "So he arose and ate and drank, and went in the strength of that food forty days and forty nights to Horeb, the mountain of God.",
    9: "Then he came there to a cave, and lodged there. And behold, the word of the LORD came to him, and He said to him, \"What are you doing here, Elijah?\"",
    10: "And he said, \"I have been very zealous for the LORD, the God of hosts. For the sons of Israel have forsaken Your covenant, torn down Your altars, and killed Your prophets with the sword. And I alone am left — and they seek my life, to take it away.\"",
    11: "So He said, \"Go forth, and stand on the mountain before the LORD.\" And behold, the LORD was passing by — and a great and strong wind was rending the mountains and breaking in pieces the rocks before the LORD, but the LORD was not in the wind. And after the wind an earthquake, but the LORD was not in the earthquake.",
    12: "And after the earthquake a fire, but the LORD was not in the fire. And after the fire — a sound of a gentle blowing.",
    13: "And it came about when Elijah heard it, that he wrapped his face in his mantle and went out and stood in the entrance of the cave. And behold, a voice came to him and said, \"What are you doing here, Elijah?\"",
    14: "Then he said, \"I have been very zealous for the LORD, the God of hosts — for the sons of Israel have forsaken Your covenant, torn down Your altars, and killed Your prophets with the sword. And I alone am left — and they seek my life, to take it away.\"",
    15: "And the LORD said to him, \"Go, return on your way to the wilderness of Damascus. And when you have arrived, you shall anoint Hazael king over Aram.",
    16: "And Jehu the son of Nimshi you shall anoint king over Israel — and Elisha the son of Shaphat of Abel-meholah you shall anoint as prophet in your place.",
    17: "And it shall come about, the one who escapes from the sword of Hazael, Jehu shall put to death — and the one who escapes from the sword of Jehu, Elisha shall put to death.",
    18: "Yet I will leave 7,000 in Israel — all the knees that have not bowed to Baal, and every mouth that has not kissed him.\"",
    19: "So he departed from there and found Elisha the son of Shaphat, while he was plowing with twelve pairs of oxen before him, and he with the twelfth. And Elijah passed over to him and threw his mantle on him.",
    20: "And he left the oxen and ran after Elijah, and said, \"Please let me kiss my father and my mother — then I will follow you.\" And he said to him, \"Go back again, for what have I done to you?\"",
    21: "So he returned from following him, and took the pair of oxen and sacrificed them, and boiled their flesh with the implements of the oxen, and gave it to the people, and they ate. Then he arose and followed Elijah and ministered to him.",
}

# 2 Kings 2:1-15 — Elijah taken up
kings_2 = {
    1: "And it came about when the LORD was about to take up Elijah by a whirlwind to heaven, that Elijah went with Elisha from Gilgal.",
    2: "And Elijah said to Elisha, \"Stay here please, for the LORD has sent me as far as Bethel.\" But Elisha said, \"As the LORD lives, and as you yourself live, I will not leave you.\" So they went down to Bethel.",
    3: "Then the sons of the prophets who were at Bethel came out to Elisha and said to him, \"Do you know that the LORD will take away your master from over you today?\" And he said, \"Yes, I know — be still.\"",
    4: "And Elijah said to him, \"Elisha, please stay here, for the LORD has sent me to Jericho.\" But he said, \"As the LORD lives, and as you yourself live, I will not leave you.\" So they came to Jericho.",
    5: "And the sons of the prophets who were at Jericho approached Elisha and said to him, \"Do you know that the LORD will take away your master from over you today?\" And he answered, \"Yes, I know — be still.\"",
    6: "Then Elijah said to him, \"Please stay here, for the LORD has sent me to the Jordan.\" But he said, \"As the LORD lives, and as you yourself live, I will not leave you.\" So the two of them went on.",
    7: "Now fifty men of the sons of the prophets went and stood opposite them at a distance, while the two of them stood by the Jordan.",
    8: "And Elijah took his mantle and folded it together and struck the waters, and they were divided here and there — so that the two of them crossed over on dry ground.",
    9: "Now it came about when they had crossed over, that Elijah said to Elisha, \"Ask what I shall do for you before I am taken from you.\" And Elisha said, \"Please, let a double portion of your spirit be upon me.\"",
    10: "And he said, \"You have asked a hard thing. Nevertheless, if you see me when I am taken from you, it shall be so for you — but if not, it shall not be so.\"",
    11: "And as they were going along and talking, behold, there appeared a chariot of fire and horses of fire which separated the two of them — and Elijah went up by a whirlwind to heaven.",
    12: "And Elisha saw it and cried out, \"My father, my father — the chariots of Israel and its horsemen!\" And he saw Elijah no more. Then he took hold of his own clothes and tore them in two pieces.",
    13: "He also took up the mantle of Elijah that fell from him, and returned and stood by the bank of the Jordan.",
    14: "And he took the mantle of Elijah that fell from him and struck the waters, and said, \"Where is the LORD, the God of Elijah?\" And when he also had struck the waters, they were divided here and there — and Elisha crossed over.",
    15: "Now when the sons of the prophets who were at Jericho opposite him saw him, they said, \"The spirit of Elijah rests on Elisha.\" And they came to meet him and bowed themselves to the ground before him.",
}

# Nehemiah 8 — Ezra reads the Law
neh_8 = {
    1: "And all the people gathered as one man at the square which was in front of the Water Gate. And they asked Ezra the scribe to bring the book of the law of Moses which the LORD had given to Israel.",
    2: "Then Ezra the priest brought the law before the assembly of men, women, and all who could listen with understanding, on the first day of the seventh month.",
    3: "And he read from it before the square which was in front of the Water Gate from early morning until midday, in the presence of men and women, those who could understand. And all the people were attentive to the book of the law.",
    4: "And Ezra the scribe stood at a wooden podium which they had made for the purpose. And beside him stood Mattithiah, Shema, Anaiah, Uriah, Hilkiah, and Maaseiah on his right hand — and Pedaiah, Mishael, Malchijah, Hashum, Hashbaddanah, Zechariah, and Meshullam on his left hand.",
    5: "Then Ezra opened the book in the sight of all the people, for he was standing above all the people. And when he opened it, all the people stood up.",
    6: "Then Ezra blessed the LORD the great God — and all the people answered, \"Amen, Amen!\" while lifting up their hands. Then they bowed low and worshiped the LORD with their faces to the ground.",
    7: "Also Jeshua, Bani, Sherebiah, Jamin, Akkub, Shabbethai, Hodiah, Maaseiah, Kelita, Azariah, Jozabad, Hanan, Pelaiah, and the Levites explained the law to the people, while the people remained in their place.",
    8: "And they read from the book, from the law of God, translating to give the sense so that they understood the reading.",
    9: "Then Nehemiah, who was the governor, and Ezra the priest and scribe, and the Levites who taught the people, said to all the people, \"This day is holy to the LORD your God. Do not mourn or weep.\" For all the people were weeping when they heard the words of the law.",
    10: "Then he said to them, \"Go, eat of the fat, drink of the sweet, and send portions to him who has nothing prepared — for this day is holy to our Lord. Do not be grieved, for the joy of the LORD is your strength.\"",
    11: "So the Levites calmed all the people, saying, \"Be still, for the day is holy. Do not be grieved.\"",
    12: "And all the people went away to eat, to drink, to send portions, and to celebrate a great festival, because they understood the words which had been made known to them.",
    13: "Then on the second day the heads of fathers' households of all the people, the priests and the Levites were gathered to Ezra the scribe that they might gain insight into the words of the law.",
    14: "And they found written in the law how the LORD had commanded through Moses that the sons of Israel should live in booths during the feast of the seventh month.",
    15: "So they proclaimed and circulated a proclamation in all their cities and in Jerusalem, saying, \"Go out to the hills, and bring olive branches and wild olive branches, myrtle branches, palm branches and branches of other leafy trees, to make booths, as it is written.\"",
    16: "So the people went out and brought them and made booths for themselves, each on his roof, and in their courts, and in the courts of the house of God, and in the square at the Water Gate and in the square at the Gate of Ephraim.",
    17: "And the entire assembly of those who had returned from the captivity made booths and lived in them. The sons of Israel had indeed not done so from the days of Joshua the son of Nun to that day. And there was great rejoicing.",
    18: "And he read from the book of the law of God daily, from the first day to the last day. And they celebrated the feast seven days, and on the eighth day there was a solemn assembly, according to the ordinance.",
}

ENTRIES = {}
for v, t in josh_1.items():   ENTRIES[f"6_1_{v}"] = t
for v, t in josh_24.items():  ENTRIES[f"6_24_{v}"] = t
for v, t in sam_17.items():   ENTRIES[f"9_17_{v}"] = t
for v, t in kings_18.items(): ENTRIES[f"11_18_{v}"] = t
for v, t in kings_19.items(): ENTRIES[f"11_19_{v}"] = t
for v, t in kings_2.items():  ENTRIES[f"12_2_{v}"] = t
for v, t in neh_8.items():    ENTRIES[f"16_8_{v}"] = t

def main():
    print(f"MBT OT historical narrative landmark verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
