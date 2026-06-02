"""MBT generator: Genesis Joseph cycle (key chapters).

Book ID 1. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Genesis 37 (36 verses) — Joseph's dreams; sold into Egypt
- Genesis 39 (23 verses) — Potiphar's house; Potiphar's wife; prison
- Genesis 45 (28 verses) — Joseph reveals himself to his brothers
- Genesis 50 (26 verses) — Jacob buried; Joseph forgives; Joseph dies

Total: 113 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Genesis 37 — Joseph's dreams and sale into Egypt
ch37 = {
    1: "Now Jacob dwelt in the land where his father was a stranger, in the land of Canaan.",
    2: "This is the history of Jacob. Joseph, being seventeen years old, was feeding the flock with his brothers. And the lad was with the sons of Bilhah and the sons of Zilpah, his father's wives; and Joseph brought a bad report of them to his father.",
    3: "Now Israel loved Joseph more than all his children, because he was the son of his old age. Also he made him a tunic of many colors.",
    4: "But when his brothers saw that their father loved him more than all his brothers, they hated him and could not speak peaceably to him.",
    5: "Now Joseph had a dream, and he told it to his brothers; and they hated him even more.",
    6: "So he said to them, \"Please hear this dream which I have dreamed:",
    7: "There we were, binding sheaves in the field. Then behold, my sheaf arose and also stood upright; and indeed your sheaves stood all around and bowed down to my sheaf.\"",
    8: "And his brothers said to him, \"Shall you indeed reign over us? Or shall you indeed have dominion over us?\" So they hated him even more for his dreams and for his words.",
    9: "Then he dreamed still another dream and told it to his brothers, and said, \"Look, I have dreamed another dream. And this time, the sun, the moon, and the eleven stars bowed down to me.\"",
    10: "So he told it to his father and his brothers; and his father rebuked him and said to him, \"What is this dream that you have dreamed? Shall your mother and I and your brothers indeed come to bow down to the earth before you?\"",
    11: "And his brothers envied him, but his father kept the matter in mind.",
    12: "Then his brothers went to feed their father's flock in Shechem.",
    13: "And Israel said to Joseph, \"Are not your brothers feeding the flock in Shechem? Come, I will send you to them.\" So he said to him, \"Here I am.\"",
    14: "Then he said to him, \"Please go and see if it is well with your brothers and well with the flocks, and bring back word to me.\" So he sent him out of the Valley of Hebron, and he went to Shechem.",
    15: "Now a certain man found him, and there he was, wandering in the field. And the man asked him, saying, \"What are you seeking?\"",
    16: "So he said, \"I am seeking my brothers. Please tell me where they are feeding their flocks.\"",
    17: "And the man said, \"They have departed from here, for I heard them say, 'Let us go to Dothan.'\" So Joseph went after his brothers and found them in Dothan.",
    18: "Now when they saw him afar off, even before he came near them, they conspired against him to kill him.",
    19: "Then they said to one another, \"Look, this dreamer is coming!",
    20: "Come therefore, let us now kill him and cast him into some pit; and we shall say, 'Some wild beast has devoured him.' We shall see what will become of his dreams!\"",
    21: "But Reuben heard it, and he delivered him out of their hands, and said, \"Let us not kill him.\"",
    22: "And Reuben said to them, \"Shed no blood, but cast him into this pit which is in the wilderness, and do not lay a hand on him\" — that he might deliver him out of their hands, and bring him back to his father.",
    23: "So it came to pass, when Joseph had come to his brothers, that they stripped Joseph of his tunic, the tunic of many colors that was on him.",
    24: "Then they took him and cast him into a pit. And the pit was empty; there was no water in it.",
    25: "And they sat down to eat a meal. Then they lifted their eyes and looked, and there was a company of Ishmaelites, coming from Gilead with their camels, bearing spices, balm, and myrrh, on their way to carry them down to Egypt.",
    26: "So Judah said to his brothers, \"What profit is there if we kill our brother and conceal his blood?",
    27: "Come and let us sell him to the Ishmaelites, and let not our hand be upon him, for he is our brother and our flesh.\" And his brothers listened.",
    28: "Then Midianite traders passed by; so the brothers pulled Joseph up and lifted him out of the pit, and sold him to the Ishmaelites for twenty shekels of silver. And they took Joseph to Egypt.",
    29: "Then Reuben returned to the pit, and indeed Joseph was not in the pit; and he tore his clothes.",
    30: "And he returned to his brothers and said, \"The lad is no more; and I, where shall I go?\"",
    31: "So they took Joseph's tunic, killed a kid of the goats, and dipped the tunic in the blood.",
    32: "Then they sent the tunic of many colors, and they brought it to their father and said, \"We have found this. Do you know whether it is your son's tunic or not?\"",
    33: "And he recognized it and said, \"It is my son's tunic. A wild beast has devoured him. Without doubt Joseph is torn to pieces.\"",
    34: "Then Jacob tore his clothes, put sackcloth on his waist, and mourned for his son many days.",
    35: "And all his sons and all his daughters arose to comfort him; but he refused to be comforted, and he said, \"For I shall go down into the grave to my son in mourning.\" Thus his father wept for him.",
    36: "Now the Midianites had sold him in Egypt to Potiphar, an officer of Pharaoh and captain of the guard.",
}

# Genesis 39 — Potiphar's house, Potiphar's wife, prison
ch39 = {
    1: "Now Joseph had been taken down to Egypt. And Potiphar, an officer of Pharaoh, captain of the guard, an Egyptian, bought him from the Ishmaelites who had taken him down there.",
    2: "The LORD was with Joseph, and he was a successful man; and he was in the house of his master the Egyptian.",
    3: "And his master saw that the LORD was with him and that the LORD made all he did to prosper in his hand.",
    4: "So Joseph found favor in his sight, and served him. Then he made him overseer of his house, and all that he had he put under his authority.",
    5: "So it was, from the time that he had made him overseer of his house and all that he had, that the LORD blessed the Egyptian's house for Joseph's sake; and the blessing of the LORD was on all that he had in the house and in the field.",
    6: "Thus he left all that he had in Joseph's hand, and he did not know what he had except for the bread which he ate. Now Joseph was handsome in form and appearance.",
    7: "And it came to pass after these things that his master's wife cast longing eyes on Joseph, and she said, \"Lie with me.\"",
    8: "But he refused and said to his master's wife, \"Look, my master does not know what is with me in the house, and he has committed all that he has to my hand.",
    9: "There is no one greater in this house than I, nor has he kept back anything from me but you, because you are his wife. How then can I do this great wickedness, and sin against God?\"",
    10: "So it was, as she spoke to Joseph day by day, that he did not heed her, to lie with her or to be with her.",
    11: "But it happened about this time, when Joseph went into the house to do his work, and none of the men of the house was inside,",
    12: "that she caught him by his garment, saying, \"Lie with me.\" But he left his garment in her hand, and fled and ran outside.",
    13: "And so it was, when she saw that he had left his garment in her hand and fled outside,",
    14: "that she called to the men of her house and spoke to them, saying, \"See, he has brought in to us a Hebrew to mock us. He came in to me to lie with me, and I cried out with a loud voice.",
    15: "And it happened, when he heard that I lifted my voice and cried out, that he left his garment with me, and fled and went outside.\"",
    16: "So she kept his garment with her until his master came home.",
    17: "Then she spoke to him with words like these, saying, \"The Hebrew servant whom you brought to us came in to me to mock me;",
    18: "so it happened, as I lifted my voice and cried out, that he left his garment with me and fled outside.\"",
    19: "So it was, when his master heard the words which his wife spoke to him, saying, \"Your servant did to me after this manner,\" that his anger was aroused.",
    20: "Then Joseph's master took him and put him into the prison, a place where the king's prisoners were confined. And he was there in the prison.",
    21: "But the LORD was with Joseph and showed him mercy, and He gave him favor in the sight of the keeper of the prison.",
    22: "And the keeper of the prison committed to Joseph's hand all the prisoners who were in the prison; whatever they did there, it was his doing.",
    23: "The keeper of the prison did not look into anything that was under Joseph's authority, because the LORD was with him; and whatever he did, the LORD made it prosper.",
}

# Genesis 45 — Joseph reveals himself to his brothers
ch45 = {
    1: "Then Joseph could not restrain himself before all those who stood by him, and he cried out, \"Make everyone go out from me!\" So no one stood with him while Joseph made himself known to his brothers.",
    2: "And he wept aloud, and the Egyptians and the house of Pharaoh heard it.",
    3: "Then Joseph said to his brothers, \"I am Joseph; does my father still live?\" But his brothers could not answer him, for they were dismayed in his presence.",
    4: "And Joseph said to his brothers, \"Please come near to me.\" So they came near. Then he said: \"I am Joseph your brother, whom you sold into Egypt.",
    5: "But now, do not therefore be grieved or angry with yourselves because you sold me here; for God sent me before you to preserve life.",
    6: "For these two years the famine has been in the land, and there are still five years in which there will be neither plowing nor harvesting.",
    7: "And God sent me before you to preserve a posterity for you in the earth, and to save your lives by a great deliverance.",
    8: "So now it was not you who sent me here, but God; and He has made me a father to Pharaoh, and lord of all his house, and a ruler throughout all the land of Egypt.",
    9: "Hurry and go up to my father, and say to him, 'Thus says your son Joseph: \"God has made me lord of all Egypt; come down to me, do not tarry.",
    10: "You shall dwell in the land of Goshen, and you shall be near to me, you and your children, your children's children, your flocks and your herds, and all that you have.",
    11: "There I will provide for you, lest you and your household, and all that you have, come to poverty; for there are still five years of famine.\"'",
    12: "And behold, your eyes and the eyes of my brother Benjamin see that it is my mouth that speaks to you.",
    13: "So you shall tell my father of all my glory in Egypt, and of all that you have seen; and you shall hurry and bring my father down here.\"",
    14: "Then he fell on his brother Benjamin's neck and wept, and Benjamin wept on his neck.",
    15: "Moreover he kissed all his brothers and wept over them, and after that his brothers talked with him.",
    16: "Now the report of it was heard in Pharaoh's house, saying, \"Joseph's brothers have come.\" So it pleased Pharaoh and his servants well.",
    17: "And Pharaoh said to Joseph, \"Say to your brothers, 'Do this: Load your animals and depart; go to the land of Canaan.",
    18: "Bring your father and your households and come to me; I will give you the best of the land of Egypt, and you will eat the fat of the land.",
    19: "Now you are commanded — do this: Take carts out of the land of Egypt for your little ones and your wives; bring your father and come.",
    20: "Also do not be concerned about your goods, for the best of all the land of Egypt is yours.'\"",
    21: "Then the sons of Israel did so; and Joseph gave them carts, according to the command of Pharaoh, and he gave them provisions for the journey.",
    22: "He gave to all of them, to each man, changes of garments; but to Benjamin he gave three hundred pieces of silver and five changes of garments.",
    23: "And he sent to his father these things: ten donkeys loaded with the good things of Egypt, and ten female donkeys loaded with grain, bread, and food for his father for the journey.",
    24: "So he sent his brothers away, and they departed; and he said to them, \"See that you do not become troubled along the way.\"",
    25: "Then they went up out of Egypt, and came to the land of Canaan to Jacob their father.",
    26: "And they told him, saying, \"Joseph is still alive, and he is governor over all the land of Egypt.\" And Jacob's heart stood still, because he did not believe them.",
    27: "But when they told him all the words which Joseph had said to them, and when he saw the carts which Joseph had sent to carry him, the spirit of Jacob their father revived.",
    28: "Then Israel said, \"It is enough. Joseph my son is still alive. I will go and see him before I die.\"",
}

# Genesis 50 — Jacob buried; Joseph forgives; Joseph dies
ch50 = {
    1: "Then Joseph fell on his father's face, and wept over him, and kissed him.",
    2: "And Joseph commanded his servants the physicians to embalm his father. So the physicians embalmed Israel.",
    3: "Forty days were required for him, for such are the days required for those who are embalmed; and the Egyptians mourned for him seventy days.",
    4: "Now when the days of his mourning were past, Joseph spoke to the household of Pharaoh, saying, \"If now I have found favor in your eyes, please speak in the hearing of Pharaoh, saying,",
    5: "'My father made me swear, saying, \"Behold, I am dying; in my grave which I dug for myself in the land of Canaan, there you shall bury me.\" Now therefore, please let me go up and bury my father, and I will come back.'\"",
    6: "And Pharaoh said, \"Go up and bury your father, as he made you swear.\"",
    7: "So Joseph went up to bury his father; and with him went up all the servants of Pharaoh, the elders of his house, and all the elders of the land of Egypt,",
    8: "as well as all the house of Joseph, his brothers, and his father's house. Only their little ones, their flocks, and their herds they left in the land of Goshen.",
    9: "And there went up with him both chariots and horsemen, and it was a very great gathering.",
    10: "Then they came to the threshing floor of Atad, which is beyond the Jordan, and they mourned there with a great and very solemn lamentation. He observed seven days of mourning for his father.",
    11: "And when the inhabitants of the land, the Canaanites, saw the mourning at the threshing floor of Atad, they said, \"This is a deep mourning of the Egyptians.\" Therefore its name was called Abel Mizraim, which is beyond the Jordan.",
    12: "So his sons did for him just as he had commanded them.",
    13: "For his sons carried him to the land of Canaan, and buried him in the cave of the field of Machpelah, before Mamre, which Abraham bought with the field from Ephron the Hittite as property for a burial place.",
    14: "And after he had buried his father, Joseph returned to Egypt, he and his brothers and all who went up with him to bury his father.",
    15: "When Joseph's brothers saw that their father was dead, they said, \"Perhaps Joseph will hate us, and may actually repay us for all the evil which we did to him.\"",
    16: "So they sent messengers to Joseph, saying, \"Before your father died he commanded, saying,",
    17: "'Thus you shall say to Joseph: \"I beg you, please forgive the trespass of your brothers and their sin; for they did evil to you.\"' Now, please, forgive the trespass of the servants of the God of your father.\" And Joseph wept when they spoke to him.",
    18: "Then his brothers also went and fell down before his face, and they said, \"Behold, we are your servants.\"",
    19: "Joseph said to them, \"Do not be afraid, for am I in the place of God?",
    20: "But as for you, you meant evil against me; but God meant it for good, in order to bring it about as it is this day, to save many people alive.",
    21: "Now therefore, do not be afraid; I will provide for you and your little ones.\" And he comforted them and spoke kindly to them.",
    22: "So Joseph dwelt in Egypt, he and his father's household. And Joseph lived one hundred and ten years.",
    23: "Joseph saw Ephraim's children to the third generation. The children of Machir, the son of Manasseh, were also brought up on Joseph's knees.",
    24: "And Joseph said to his brothers, \"I am dying; but God will surely visit you, and bring you out of this land to the land of which He swore to Abraham, to Isaac, and to Jacob.\"",
    25: "Then Joseph took an oath from the children of Israel, saying, \"God will surely visit you, and you shall carry up my bones from here.\"",
    26: "So Joseph died, being one hundred and ten years old; and they embalmed him, and he was put in a coffin in Egypt.",
}

ENTRIES = {}
for v, t in ch37.items():
    ENTRIES[f"1_37_{v}"] = t
for v, t in ch39.items():
    ENTRIES[f"1_39_{v}"] = t
for v, t in ch45.items():
    ENTRIES[f"1_45_{v}"] = t
for v, t in ch50.items():
    ENTRIES[f"1_50_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Genesis Joseph cycle verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
