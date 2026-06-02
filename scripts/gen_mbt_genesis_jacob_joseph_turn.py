"""MBT generator: Genesis Jacob narrative + the Joseph turn.

Book ID 1. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Genesis 28 (22 verses) — Jacob's ladder at Bethel
- Genesis 32 (32 verses) — Peniel: Jacob wrestles with God
- Genesis 41 (57 verses) — Pharaoh's dreams; Joseph elevated

Total: 111 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 28 — Jacob's ladder at Bethel
ch28 = {
    1: "Then Isaac called Jacob and blessed him, and charged him, and said to him: \"You shall not take a wife from the daughters of Canaan.",
    2: "Arise, go to Padan Aram, to the house of Bethuel your mother's father; and take yourself a wife from there of the daughters of Laban your mother's brother.",
    3: "May God Almighty bless you, and make you fruitful and multiply you, that you may be an assembly of peoples;",
    4: "and give you the blessing of Abraham, to you and your descendants with you, that you may inherit the land in which you are a stranger, which God gave to Abraham.\"",
    5: "So Isaac sent Jacob away, and he went to Padan Aram, to Laban the son of Bethuel the Syrian, the brother of Rebekah, the mother of Jacob and Esau.",
    6: "Esau saw that Isaac had blessed Jacob and sent him away to Padan Aram to take himself a wife from there, and that as he blessed him he gave him a charge, saying, \"You shall not take a wife from the daughters of Canaan,\"",
    7: "and that Jacob had obeyed his father and his mother and had gone to Padan Aram.",
    8: "Also Esau saw that the daughters of Canaan did not please his father Isaac.",
    9: "So Esau went to Ishmael and took Mahalath the daughter of Ishmael, Abraham's son, the sister of Nebajoth, to be his wife in addition to the wives he had.",
    10: "Now Jacob went out from Beersheba and went toward Haran.",
    11: "So he came to a certain place and stayed there all night, because the sun had set. And he took one of the stones of that place and put it at his head, and he lay down in that place to sleep.",
    12: "Then he dreamed, and behold, a ladder was set up on the earth, and its top reached to heaven; and there the angels of God were ascending and descending on it.",
    13: "And behold, the LORD stood above it and said: \"I am the LORD God of Abraham your father and the God of Isaac; the land on which you lie I will give to you and your descendants.",
    14: "Also your descendants shall be as the dust of the earth; you shall spread abroad to the west and the east, to the north and the south; and in you and in your seed all the families of the earth shall be blessed.",
    15: "Behold, I am with you and will keep you wherever you go, and will bring you back to this land; for I will not leave you until I have done what I have spoken to you.\"",
    16: "Then Jacob awoke from his sleep and said, \"Surely the LORD is in this place, and I did not know it.\"",
    17: "And he was afraid and said, \"How awesome is this place! This is none other than the house of God, and this is the gate of heaven!\"",
    18: "Then Jacob rose early in the morning, and took the stone that he had put at his head, set it up as a pillar, and poured oil on top of it.",
    19: "And he called the name of that place Bethel; but the name of that city had been Luz previously.",
    20: "Then Jacob made a vow, saying, \"If God will be with me, and keep me in this way that I am going, and give me bread to eat and clothing to put on,",
    21: "so that I come back to my father's house in peace, then the LORD shall be my God.",
    22: "And this stone which I have set as a pillar shall be God's house, and of all that You give me I will surely give a tenth to You.\"",
}

# Genesis 32 — Peniel: wrestling with God
ch32 = {
    1: "So Jacob went on his way, and the angels of God met him.",
    2: "When Jacob saw them, he said, \"This is God's camp.\" And he called the name of that place Mahanaim.",
    3: "Then Jacob sent messengers before him to Esau his brother in the land of Seir, the country of Edom.",
    4: "And he commanded them, saying, \"Speak thus to my lord Esau, 'Thus your servant Jacob says: \"I have dwelt with Laban and stayed there until now.",
    5: "I have oxen, donkeys, flocks, and male and female servants; and I have sent to tell my lord, that I may find favor in your sight.\"'\"",
    6: "Then the messengers returned to Jacob, saying, \"We came to your brother Esau, and he also is coming to meet you, and four hundred men are with him.\"",
    7: "So Jacob was greatly afraid and distressed; and he divided the people that were with him, and the flocks and herds and camels, into two companies.",
    8: "And he said, \"If Esau comes to the one company and attacks it, then the other company which is left will escape.\"",
    9: "Then Jacob said, \"O God of my father Abraham and God of my father Isaac, the LORD who said to me, 'Return to your country and to your kindred, and I will deal well with you':",
    10: "I am not worthy of the least of all the mercies and of all the truth which You have shown Your servant; for I crossed over this Jordan with my staff, and now I have become two companies.",
    11: "Deliver me, I pray, from the hand of my brother, from the hand of Esau; for I fear him, lest he come and attack me and the mother with the children.",
    12: "For You said, 'I will surely treat you well, and make your descendants as the sand of the sea, which cannot be numbered for multitude.'\"",
    13: "So he lodged there that same night, and took what came to his hand as a present for Esau his brother:",
    14: "two hundred female goats and twenty male goats, two hundred ewes and twenty rams,",
    15: "thirty milk camels with their colts, forty cows and ten bulls, twenty female donkeys and ten foals.",
    16: "Then he delivered them to the hand of his servants, every drove by itself, and said to his servants, \"Pass over before me, and put some distance between successive droves.\"",
    17: "And he commanded the first one, saying, \"When Esau my brother meets you and asks you, saying, 'To whom do you belong, and where are you going? Whose are these in front of you?'",
    18: "then you shall say, 'They are your servant Jacob's. It is a present sent to my lord Esau; and behold, he also is behind us.'\"",
    19: "So he commanded the second, the third, and all who followed the droves, saying, \"In this manner you shall speak to Esau when you find him;",
    20: "and also say, 'Behold, your servant Jacob is behind us.'\" For he said, \"I will appease him with the present that goes before me, and afterward I will see his face; perhaps he will accept me.\"",
    21: "So the present went on over before him, but he himself lodged that night in the camp.",
    22: "And he arose that night and took his two wives, his two female servants, and his eleven sons, and crossed over the ford of Jabbok.",
    23: "He took them, sent them over the brook, and sent over what he had.",
    24: "Then Jacob was left alone; and a Man wrestled with him until the breaking of day.",
    25: "Now when He saw that He did not prevail against him, He touched the socket of his hip; and the socket of Jacob's hip was out of joint as He wrestled with him.",
    26: "And He said, \"Let Me go, for the day breaks.\" But he said, \"I will not let You go unless You bless me!\"",
    27: "So He said to him, \"What is your name?\" He said, \"Jacob.\"",
    28: "And He said, \"Your name shall no longer be called Jacob, but Israel; for you have struggled with God and with men, and have prevailed.\"",
    29: "Then Jacob asked, saying, \"Tell me Your name, I pray.\" And He said, \"Why is it that you ask about My name?\" And He blessed him there.",
    30: "So Jacob called the name of the place Peniel: \"For I have seen God face to face, and my life is preserved.\"",
    31: "Just as he crossed over Penuel the sun rose on him, and he limped on his hip.",
    32: "Therefore to this day the children of Israel do not eat the muscle that shrank, which is on the hip socket, because He touched the socket of Jacob's hip in the muscle that shrank.",
}

# Genesis 41 — Pharaoh's dreams and Joseph's elevation
ch41 = {
    1: "Then it came to pass, at the end of two full years, that Pharaoh had a dream; and behold, he stood by the river.",
    2: "Suddenly there came up out of the river seven cows, fine looking and fat; and they fed in the meadow.",
    3: "Then behold, seven other cows came up after them out of the river, ugly and gaunt, and stood by the other cows on the bank of the river.",
    4: "And the ugly and gaunt cows ate up the seven fine looking and fat cows. So Pharaoh awoke.",
    5: "He slept and dreamed a second time; and behold, seven heads of grain came up on one stalk, plump and good.",
    6: "Then behold, seven thin heads, blighted by the east wind, sprang up after them.",
    7: "And the seven thin heads devoured the seven plump and full heads. So Pharaoh awoke; and indeed, it was a dream.",
    8: "Now it came to pass in the morning that his spirit was troubled, and he sent and called for all the magicians of Egypt and all its wise men. And Pharaoh told them his dreams, but there was no one who could interpret them for Pharaoh.",
    9: "Then the chief butler spoke to Pharaoh, saying: \"I remember my faults this day.",
    10: "When Pharaoh was angry with his servants, and put me in custody in the house of the captain of the guard, both me and the chief baker,",
    11: "we each had a dream in one night, he and I. Each of us dreamed according to the interpretation of his own dream.",
    12: "Now there was a young Hebrew man with us there, a servant of the captain of the guard. And we told him, and he interpreted our dreams for us; to each man he interpreted according to his own dream.",
    13: "And it came to pass, just as he interpreted for us, so it happened. He restored me to my office, and he hanged him.\"",
    14: "Then Pharaoh sent and called Joseph, and they brought him quickly out of the dungeon; and he shaved, changed his clothing, and came to Pharaoh.",
    15: "And Pharaoh said to Joseph, \"I have had a dream, and there is no one who can interpret it. But I have heard it said of you that you can understand a dream, to interpret it.\"",
    16: "So Joseph answered Pharaoh, saying, \"It is not in me; God will give Pharaoh an answer of peace.\"",
    17: "Then Pharaoh said to Joseph: \"Behold, in my dream I stood on the bank of the river.",
    18: "Suddenly seven cows came up out of the river, fine looking and fat; and they fed in the meadow.",
    19: "Then behold, seven other cows came up after them, poor and very ugly and gaunt, such ugliness as I have never seen in all the land of Egypt.",
    20: "And the gaunt and ugly cows ate up the first seven, the fat cows.",
    21: "When they had eaten them up, no one would have known that they had eaten them, for they were just as ugly as at the beginning. So I awoke.",
    22: "Also I saw in my dream, and suddenly seven heads came up on one stalk, full and good.",
    23: "Then behold, seven heads, withered, thin, and blighted by the east wind, sprang up after them.",
    24: "And the thin heads devoured the seven good heads. So I told this to the magicians, but there was no one who could explain it to me.\"",
    25: "Then Joseph said to Pharaoh, \"The dreams of Pharaoh are one; God has shown Pharaoh what He is about to do:",
    26: "The seven good cows are seven years, and the seven good heads are seven years; the dreams are one.",
    27: "And the seven thin and ugly cows which came up after them are seven years, and the seven empty heads blighted by the east wind are seven years of famine.",
    28: "This is the thing which I have spoken to Pharaoh. God has shown Pharaoh what He is about to do.",
    29: "Indeed seven years of great plenty will come throughout all the land of Egypt;",
    30: "but after them seven years of famine will arise, and all the plenty will be forgotten in the land of Egypt; and the famine will deplete the land.",
    31: "So the plenty will not be known in the land because of the famine following, for it will be very severe.",
    32: "And the dream was repeated to Pharaoh twice because the thing is established by God, and God will shortly bring it to pass.",
    33: "Now therefore, let Pharaoh select a discerning and wise man, and set him over the land of Egypt.",
    34: "Let Pharaoh do this, and let him appoint officers over the land, to collect one-fifth of the produce of the land of Egypt in the seven plentiful years.",
    35: "And let them gather all the food of those good years that are coming, and store up grain under the authority of Pharaoh, and let them keep food in the cities.",
    36: "Then that food shall be as a reserve for the land for the seven years of famine which shall be in the land of Egypt, that the land may not perish during the famine.\"",
    37: "So the advice was good in the eyes of Pharaoh and in the eyes of all his servants.",
    38: "And Pharaoh said to his servants, \"Can we find such a one as this, a man in whom is the Spirit of God?\"",
    39: "Then Pharaoh said to Joseph, \"Inasmuch as God has shown you all this, there is no one as discerning and wise as you.",
    40: "You shall be over my house, and all my people shall be ruled according to your word; only in regard to the throne will I be greater than you.\"",
    41: "And Pharaoh said to Joseph, \"See, I have set you over all the land of Egypt.\"",
    42: "Then Pharaoh took his signet ring off his hand and put it on Joseph's hand; and he clothed him in garments of fine linen and put a gold chain around his neck.",
    43: "And he had him ride in the second chariot which he had; and they cried out before him, \"Bow the knee!\" So he set him over all the land of Egypt.",
    44: "Pharaoh also said to Joseph, \"I am Pharaoh, and without your consent no man may lift his hand or foot in all the land of Egypt.\"",
    45: "And Pharaoh called Joseph's name Zaphnath-Paaneah. And he gave him as a wife Asenath, the daughter of Poti-Pherah priest of On. So Joseph went out over all the land of Egypt.",
    46: "Joseph was thirty years old when he stood before Pharaoh king of Egypt. And Joseph went out from the presence of Pharaoh, and went throughout all the land of Egypt.",
    47: "Now in the seven plentiful years the ground brought forth abundantly.",
    48: "So he gathered up all the food of the seven years which were in the land of Egypt, and laid up the food in the cities; he laid up in every city the food of the fields which surrounded them.",
    49: "Joseph gathered very much grain, as the sand of the sea, until he stopped counting, for it was immeasurable.",
    50: "And to Joseph were born two sons before the years of famine came, whom Asenath, the daughter of Poti-Pherah priest of On, bore to him.",
    51: "Joseph called the name of the firstborn Manasseh: \"For God has made me forget all my toil and all my father's house.\"",
    52: "And the name of the second he called Ephraim: \"For God has caused me to be fruitful in the land of my affliction.\"",
    53: "Then the seven years of plenty which were in the land of Egypt ended,",
    54: "and the seven years of famine began to come, as Joseph had said. The famine was in all lands, but in all the land of Egypt there was bread.",
    55: "So when all the land of Egypt was famished, the people cried to Pharaoh for bread. Then Pharaoh said to all the Egyptians, \"Go to Joseph; whatever he says to you, do.\"",
    56: "The famine was over all the face of the earth, and Joseph opened all the storehouses and sold to the Egyptians. And the famine became severe in the land of Egypt.",
    57: "So all countries came to Joseph in Egypt to buy grain, because the famine was severe in all lands.",
}

ENTRIES = {}
for v, t in ch28.items():
    ENTRIES[f"1_28_{v}"] = t
for v, t in ch32.items():
    ENTRIES[f"1_32_{v}"] = t
for v, t in ch41.items():
    ENTRIES[f"1_41_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Genesis Jacob + Joseph turn verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
