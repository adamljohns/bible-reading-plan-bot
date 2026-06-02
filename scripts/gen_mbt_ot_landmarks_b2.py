"""MBT OT landmark batch 2 — more Pentateuch + prophetic landmarks.

Gen 22:1-19 (Akedah / sacrifice of Isaac)
Exodus 12:1-30 (Passover instituted)
Exodus 14 (Crossing the Red Sea)
Numbers 6:22-27 (Aaronic blessing)
Jeremiah 1:4-10 (Call of Jeremiah)
Jeremiah 31:31-34 (New Covenant)
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 22:1-19 — Abraham offers Isaac
gen_22 = {
    1: "Now it came about after these things, that God tested Abraham, and said to him, \"Abraham!\" And he said, \"Here I am.\"",
    2: "And He said, \"Take now your son, your only son, whom you love, Isaac — and go to the land of Moriah, and offer him there as a burnt offering on one of the mountains of which I will tell you.\"",
    3: "So Abraham rose early in the morning and saddled his donkey, and took two of his young men with him and Isaac his son — and he split wood for the burnt offering, and arose and went to the place of which God had told him.",
    4: "On the third day Abraham raised his eyes and saw the place from a distance.",
    5: "And Abraham said to his young men, \"Stay here with the donkey, and I and the lad will go yonder. And we will worship and return to you.\"",
    6: "And Abraham took the wood of the burnt offering and laid it on Isaac his son — and he took in his hand the fire and the knife. So the two of them walked on together.",
    7: "And Isaac spoke to Abraham his father and said, \"My father!\" And he said, \"Here I am, my son.\" And he said, \"Behold, the fire and the wood — but where is the lamb for the burnt offering?\"",
    8: "And Abraham said, \"God will provide for Himself the lamb for the burnt offering, my son.\" So the two of them walked on together.",
    9: "Then they came to the place of which God had told him — and Abraham built the altar there, and arranged the wood, and bound his son Isaac, and laid him on the altar, on top of the wood.",
    10: "And Abraham stretched out his hand and took the knife to slay his son.",
    11: "But the angel of the LORD called to him from heaven, and said, \"Abraham, Abraham!\" And he said, \"Here I am.\"",
    12: "And he said, \"Do not stretch out your hand against the lad, and do nothing to him — for now I know that you fear God, since you have not withheld your son, your only son, from Me.\"",
    13: "Then Abraham raised his eyes and looked, and behold, behind him a ram caught in the thicket by his horns. And Abraham went and took the ram, and offered him up for a burnt offering in the place of his son.",
    14: "And Abraham called the name of that place The LORD Will Provide — as it is said to this day, \"In the mount of the LORD it will be provided.\"",
    15: "Then the angel of the LORD called to Abraham a second time from heaven,",
    16: "and said, \"By Myself I have sworn, declares the LORD — because you have done this thing, and have not withheld your son, your only son,",
    17: "indeed I will greatly bless you, and I will greatly multiply your seed as the stars of the heavens, and as the sand which is on the seashore — and your seed shall possess the gate of their enemies.",
    18: "And in your seed all the nations of the earth shall be blessed — because you have obeyed My voice.\"",
    19: "So Abraham returned to his young men, and they arose and went together to Beersheba — and Abraham lived at Beersheba.",
}

# Exodus 12:1-30 — Passover instituted, the death of the firstborn
ex_12 = {
    1: "Now the LORD said to Moses and Aaron in the land of Egypt,",
    2: "\"This month shall be the beginning of months for you — it is to be the first month of the year to you.",
    3: "Speak to all the congregation of Israel, saying, 'On the tenth of this month they are each one to take a lamb for themselves, according to their fathers' households, a lamb for each household.",
    4: "Now if the household is too small for a lamb, then he and his neighbor nearest to his house are to take one according to the number of persons in them — according to what each man should eat, you are to divide the lamb.",
    5: "Your lamb shall be an unblemished male a year old. You may take it from the sheep or from the goats.",
    6: "And you shall keep it until the fourteenth day of the same month — then the whole assembly of the congregation of Israel is to kill it at twilight.",
    7: "Moreover, they shall take some of the blood and put it on the two doorposts and on the lintel of the houses in which they eat it.",
    8: "And they shall eat the flesh that same night, roasted with fire — and they shall eat it with unleavened bread and bitter herbs.",
    9: "Do not eat any of it raw or boiled at all with water — but rather roasted with fire, both its head and its legs along with its entrails.",
    10: "And you shall not leave any of it over until morning, but whatever is left of it until morning, you shall burn with fire.",
    11: "Now you shall eat it in this manner — with your loins girded, your sandals on your feet, and your staff in your hand. And you shall eat it in haste — it is the LORD's Passover.",
    12: "For I will go through the land of Egypt on that night, and will strike down all the firstborn in the land of Egypt, both man and beast — and against all the gods of Egypt I will execute judgments. I am the LORD.",
    13: "And the blood shall be a sign for you on the houses where you live. And when I see the blood, I will pass over you — and no plague will befall you to destroy you, when I strike the land of Egypt.",
    14: "Now this day will be a memorial to you — and you shall celebrate it as a feast to the LORD. Throughout your generations you are to celebrate it as a permanent ordinance.",
    15: "Seven days you shall eat unleavened bread — but on the first day you shall remove leaven from your houses, for whoever eats anything leavened from the first day until the seventh day, that person shall be cut off from Israel.",
    16: "And on the first day you shall have a holy assembly, and another holy assembly on the seventh day — no work at all shall be done on them, except what must be eaten by every person, that alone may be prepared by you.",
    17: "You shall also observe the Feast of Unleavened Bread — for on this very day I brought your hosts out of the land of Egypt. Therefore you shall observe this day throughout your generations as a permanent ordinance.",
    18: "In the first month, on the fourteenth day of the month at evening, you shall eat unleavened bread, until the twenty-first day of the month at evening.",
    19: "Seven days there shall be no leaven found in your houses — for whoever eats what is leavened, that person shall be cut off from the congregation of Israel, whether he is an alien or a native of the land.",
    20: "You shall not eat anything leavened — in all your dwellings you shall eat unleavened bread.\"",
    21: "Then Moses called for all the elders of Israel, and said to them, \"Go and take for yourselves lambs according to your families, and slay the Passover lamb.",
    22: "And you shall take a bunch of hyssop and dip it in the blood which is in the basin, and apply some of the blood that is in the basin to the lintel and the two doorposts — and none of you shall go outside the door of his house until morning.",
    23: "For the LORD will pass through to smite the Egyptians — and when He sees the blood on the lintel and on the two doorposts, the LORD will pass over the door and will not allow the destroyer to come in to your houses to smite you.",
    24: "And you shall observe this event as an ordinance for you and your children forever.",
    25: "And it will come about when you enter the land which the LORD will give you, as He has promised, that you shall observe this rite.",
    26: "And it will come about when your children will say to you, 'What does this rite mean to you?'",
    27: "that you shall say, 'It is a Passover sacrifice to the LORD who passed over the houses of the sons of Israel in Egypt when He smote the Egyptians, but spared our homes.'\" And the people bowed low and worshiped.",
    28: "Then the sons of Israel went and did so — just as the LORD had commanded Moses and Aaron, so they did.",
    29: "Now it came about at midnight that the LORD struck all the firstborn in the land of Egypt — from the firstborn of Pharaoh who sat on his throne, to the firstborn of the captive who was in the dungeon, and all the firstborn of cattle.",
    30: "And Pharaoh arose in the night, he and all his servants and all the Egyptians, and there was a great cry in Egypt — for there was no home where there was not someone dead.",
}

# Exodus 14 — Crossing the Red Sea
ex_14 = {
    1: "Now the LORD spoke to Moses, saying,",
    2: "\"Tell the sons of Israel to turn back and camp before Pi-hahiroth, between Migdol and the sea — you shall camp in front of Baal-zephon, opposite it by the sea.",
    3: "For Pharaoh will say of the sons of Israel, 'They are wandering aimlessly in the land — the wilderness has shut them in.'",
    4: "Thus I will harden Pharaoh's heart, and he will chase after them — and I will be honored through Pharaoh and all his army, and the Egyptians will know that I am the LORD.\" And they did so.",
    5: "When the king of Egypt was told that the people had fled, Pharaoh and his servants had a change of heart toward the people, and they said, \"What is this we have done, that we have let Israel go from serving us?\"",
    6: "So he made his chariot ready, and took his people with him.",
    7: "And he took six hundred select chariots, and all the other chariots of Egypt, with officers over all of them.",
    8: "And the LORD hardened the heart of Pharaoh, king of Egypt, and he chased after the sons of Israel as the sons of Israel were going out boldly.",
    9: "Then the Egyptians chased after them with all the horses and chariots of Pharaoh, his horsemen and his army, and they overtook them camping by the sea, beside Pi-hahiroth, in front of Baal-zephon.",
    10: "And as Pharaoh drew near, the sons of Israel looked, and behold, the Egyptians were marching after them. And they became very frightened. So the sons of Israel cried out to the LORD.",
    11: "Then they said to Moses, \"Is it because there were no graves in Egypt that you have taken us away to die in the wilderness? Why have you dealt with us in this way, bringing us out of Egypt?",
    12: "Is this not the word that we spoke to you in Egypt, saying, 'Leave us alone that we may serve the Egyptians'? For it would have been better for us to serve the Egyptians than to die in the wilderness.\"",
    13: "But Moses said to the people, \"Do not fear! Stand by and see the salvation of the LORD which He will accomplish for you today — for the Egyptians whom you have seen today, you will never see them again forever.",
    14: "The LORD will fight for you, while you keep silent.\"",
    15: "Then the LORD said to Moses, \"Why are you crying out to Me? Tell the sons of Israel to go forward.",
    16: "And as for you, lift up your staff and stretch out your hand over the sea, and divide it — and the sons of Israel shall go through the midst of the sea on dry land.",
    17: "And as for Me, behold, I will harden the hearts of the Egyptians so that they will go in after them — and I will be honored through Pharaoh and all his army, through his chariots and his horsemen.",
    18: "Then the Egyptians will know that I am the LORD, when I am honored through Pharaoh, through his chariots and his horsemen.\"",
    19: "And the angel of God, who had been going before the camp of Israel, moved and went behind them. And the pillar of cloud moved from before them and stood behind them.",
    20: "So it came between the camp of Egypt and the camp of Israel — and there was the cloud along with the darkness, yet it gave light at night. And the one did not come near the other all night.",
    21: "Then Moses stretched out his hand over the sea — and the LORD swept the sea back by a strong east wind all night, and turned the sea into dry land, so the waters were divided.",
    22: "And the sons of Israel went through the midst of the sea on the dry land — and the waters were like a wall to them on their right hand and on their left.",
    23: "Then the Egyptians took up the pursuit, and all Pharaoh's horses, his chariots and his horsemen went in after them into the midst of the sea.",
    24: "And it came about at the morning watch, that the LORD looked down on the army of the Egyptians through the pillar of fire and cloud, and brought the army of the Egyptians into confusion.",
    25: "And He caused their chariot wheels to swerve, and He made them drive with difficulty — so the Egyptians said, \"Let us flee from Israel, for the LORD is fighting for them against the Egyptians.\"",
    26: "Then the LORD said to Moses, \"Stretch out your hand over the sea, so that the waters may come back over the Egyptians, over their chariots and their horsemen.\"",
    27: "So Moses stretched out his hand over the sea, and the sea returned to its normal state at daybreak, while the Egyptians were fleeing right into it — then the LORD overthrew the Egyptians in the midst of the sea.",
    28: "And the waters returned and covered the chariots and the horsemen, even Pharaoh's entire army that had gone into the sea after them — not even one of them remained.",
    29: "But the sons of Israel walked on dry land through the midst of the sea — and the waters were like a wall to them on their right hand and on their left.",
    30: "Thus the LORD saved Israel that day from the hand of the Egyptians — and Israel saw the Egyptians dead on the seashore.",
    31: "And when Israel saw the great power which the LORD had used against the Egyptians, the people feared the LORD — and they believed in the LORD and in His servant Moses.",
}

# Numbers 6:22-27 — Aaronic blessing
num_6 = {
    22: "Then the LORD spoke to Moses, saying,",
    23: "\"Speak to Aaron and to his sons, saying, 'Thus you shall bless the sons of Israel. You shall say to them:",
    24: "The LORD bless you and keep you.",
    25: "The LORD make His face shine on you and be gracious to you.",
    26: "The LORD lift up His countenance on you and give you peace.'",
    27: "So they shall invoke My name on the sons of Israel — and I then will bless them.\"",
}

# Jeremiah 1:4-10 — The call of Jeremiah
jer_1 = {
    4: "Now the word of the LORD came to me, saying,",
    5: "\"Before I formed you in the womb I knew you — and before you were born I consecrated you. I have appointed you a prophet to the nations.\"",
    6: "Then I said, \"Alas, Lord GOD! Behold, I do not know how to speak — because I am a youth.\"",
    7: "But the LORD said to me, \"Do not say, 'I am a youth' — because everywhere I send you, you shall go, and all that I command you, you shall speak.",
    8: "Do not be afraid of them — for I am with you to deliver you,\" declares the LORD.",
    9: "Then the LORD stretched out His hand and touched my mouth. And the LORD said to me, \"Behold, I have put My words in your mouth.",
    10: "See, I have appointed you this day over the nations and over the kingdoms — to pluck up and to break down, to destroy and to overthrow, to build and to plant.\"",
}

# Jeremiah 31:31-34 — The New Covenant
jer_31 = {
    31: "\"Behold, days are coming,\" declares the LORD, \"when I will make a new covenant with the house of Israel and with the house of Judah —",
    32: "not like the covenant which I made with their fathers in the day I took them by the hand to bring them out of the land of Egypt, My covenant which they broke, although I was a husband to them,\" declares the LORD.",
    33: "\"But this is the covenant which I will make with the house of Israel after those days,\" declares the LORD. \"I will put My law within them, and on their heart I will write it — and I will be their God, and they shall be My people.",
    34: "And they shall not teach again, each man his neighbor and each man his brother, saying, 'Know the LORD' — for they shall all know Me, from the least of them to the greatest of them,\" declares the LORD, \"for I will forgive their iniquity, and their sin I will remember no more.\"",
}

ENTRIES = {}
for v, t in gen_22.items(): ENTRIES[f"1_22_{v}"] = t
for v, t in ex_12.items():  ENTRIES[f"2_12_{v}"] = t
for v, t in ex_14.items():  ENTRIES[f"2_14_{v}"] = t
for v, t in num_6.items():  ENTRIES[f"4_6_{v}"] = t
for v, t in jer_1.items():  ENTRIES[f"24_1_{v}"] = t
for v, t in jer_31.items(): ENTRIES[f"24_31_{v}"] = t

def main():
    print(f"OT landmark batch 2 verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
