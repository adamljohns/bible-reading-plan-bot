"""MBT generator: Job landmark chapters.

Book ID 18. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Job 1 (22 verses) — the prologue; Satan's first wager; Job's first loss
- Job 2 (13 verses) — Satan's second wager; "though He slay me" beginnings
- Job 19 (29 verses) — "I know that my Redeemer lives"
- Job 38 (41 verses) — God answers Job out of the whirlwind
- Job 42 (17 verses) — Job's repentance and restoration

Total: 122 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Job 1 — the prologue and the first wager
ch1 = {
    1: "There was a man in the land of Uz, whose name was Job; and that man was blameless and upright, a man of complete integrity who feared God and turned away from evil.",
    2: "And seven sons and three daughters were born to him.",
    3: "Also, his possessions were seven thousand sheep, three thousand camels, five hundred yoke of oxen, five hundred female donkeys, and a very large household, so that this man was the greatest of all the people of the East.",
    4: "And his sons would go and feast in their houses, each on his appointed day, and would send and invite their three sisters to eat and drink with them.",
    5: "So it was, when the days of feasting had run their course, that Job would send and sanctify them, and he would rise early in the morning and offer burnt offerings according to the number of them all. For Job said, \"It may be that my sons have sinned and cursed God in their hearts.\" Thus Job did regularly.",
    6: "Now there was a day when the sons of God came to present themselves before the LORD, and Satan also came among them.",
    7: "And the LORD said to Satan, \"From where do you come?\" So Satan answered the LORD and said, \"From going to and fro on the earth, and from walking back and forth on it.\"",
    8: "Then the LORD said to Satan, \"Have you considered My servant Job, that there is none like him on the earth, a blameless and upright man, one who fears God and shuns evil?\"",
    9: "So Satan answered the LORD and said, \"Does Job fear God for nothing?",
    10: "Have You not made a hedge around him, around his household, and around all that he has on every side? You have blessed the work of his hands, and his possessions have increased in the land.",
    11: "But now, stretch out Your hand and touch all that he has, and he will surely curse You to Your face!\"",
    12: "And the LORD said to Satan, \"Behold, all that he has is in your power; only do not lay a hand on his person.\" So Satan went out from the presence of the LORD.",
    13: "Now there was a day when his sons and daughters were eating and drinking wine in their oldest brother's house;",
    14: "and a messenger came to Job and said, \"The oxen were plowing and the donkeys feeding beside them,",
    15: "when the Sabeans raided them and took them away — indeed they have killed the servants with the edge of the sword; and I alone have escaped to tell you!\"",
    16: "While he was still speaking, another also came and said, \"The fire of God fell from heaven and burned up the sheep and the servants, and consumed them; and I alone have escaped to tell you!\"",
    17: "While he was still speaking, another also came and said, \"The Chaldeans formed three bands, raided the camels and took them away, yes, and killed the servants with the edge of the sword; and I alone have escaped to tell you!\"",
    18: "While he was still speaking, another also came and said, \"Your sons and daughters were eating and drinking wine in their oldest brother's house,",
    19: "and suddenly a great wind came from across the wilderness and struck the four corners of the house, and it fell on the young people, and they are dead; and I alone have escaped to tell you!\"",
    20: "Then Job arose, tore his robe, and shaved his head; and he fell to the ground and worshiped.",
    21: "And he said: \"Naked I came from my mother's womb, and naked shall I return there. The LORD gave, and the LORD has taken away; blessed be the name of the LORD.\"",
    22: "In all this Job did not sin nor charge God with wrong.",
}

# Job 2 — the second wager
ch2 = {
    1: "Again there was a day when the sons of God came to present themselves before the LORD, and Satan came also among them to present himself before the LORD.",
    2: "And the LORD said to Satan, \"From where do you come?\" Satan answered the LORD and said, \"From going to and fro on the earth, and from walking back and forth on it.\"",
    3: "Then the LORD said to Satan, \"Have you considered My servant Job, that there is none like him on the earth, a blameless and upright man, one who fears God and shuns evil? And still he holds fast to his integrity, although you incited Me against him, to destroy him without cause.\"",
    4: "So Satan answered the LORD and said, \"Skin for skin! Yes, all that a man has he will give for his life.",
    5: "But stretch out Your hand now, and touch his bone and his flesh, and he will surely curse You to Your face!\"",
    6: "And the LORD said to Satan, \"Behold, he is in your hand, but spare his life.\"",
    7: "So Satan went out from the presence of the LORD, and struck Job with painful boils from the sole of his foot to the crown of his head.",
    8: "And he took for himself a potsherd with which to scrape himself while he sat in the midst of the ashes.",
    9: "Then his wife said to him, \"Do you still hold fast to your integrity? Curse God and die!\"",
    10: "But he said to her, \"You speak as one of the foolish women speaks. Shall we indeed accept good from God, and shall we not accept adversity?\" In all this Job did not sin with his lips.",
    11: "Now when Job's three friends heard of all this adversity that had come upon him, each one came from his own place — Eliphaz the Temanite, Bildad the Shuhite, and Zophar the Naamathite. For they had made an appointment together to come and mourn with him, and to comfort him.",
    12: "And when they raised their eyes from afar, and did not recognize him, they lifted their voices and wept; and each one tore his robe and sprinkled dust on his head toward heaven.",
    13: "So they sat down with him on the ground seven days and seven nights, and no one spoke a word to him, for they saw that his grief was very great.",
}

# Job 19 — "I know that my Redeemer lives"
ch19 = {
    1: "Then Job answered and said:",
    2: "\"How long will you torment my soul, and break me in pieces with words?",
    3: "These ten times you have reproached me; you are not ashamed that you have wronged me.",
    4: "And if indeed I have erred, my error remains with me.",
    5: "If indeed you exalt yourselves against me, and plead my disgrace against me,",
    6: "know then that God has wronged me, and has surrounded me with His net.",
    7: "\"If I cry out concerning wrong, I am not heard. If I cry aloud, there is no justice.",
    8: "He has fenced up my way, so that I cannot pass; and He has set darkness in my paths.",
    9: "He has stripped me of my glory, and taken the crown from my head.",
    10: "He breaks me down on every side, and I am gone; my hope He has uprooted like a tree.",
    11: "He has also kindled His wrath against me, and He counts me as one of His enemies.",
    12: "His troops come together and build up their road against me; they encamp all around my tent.",
    13: "\"He has removed my brothers far from me, and my acquaintances are completely estranged from me.",
    14: "My relatives have failed, and my close friends have forgotten me.",
    15: "Those who dwell in my house, and my maidservants, count me as a stranger; I am an alien in their sight.",
    16: "I call my servant, but he gives no answer; I beg him with my mouth.",
    17: "My breath is offensive to my wife, and I am repulsive to the children of my own body.",
    18: "Even young children despise me; I arise, and they speak against me.",
    19: "All my close friends abhor me, and those whom I love have turned against me.",
    20: "My bone clings to my skin and to my flesh, and I have escaped by the skin of my teeth.",
    21: "Have pity on me, have pity on me, O you my friends, for the hand of God has struck me!",
    22: "Why do you persecute me as God does, and are not satisfied with my flesh?",
    23: "\"Oh, that my words were written! Oh, that they were inscribed in a book!",
    24: "That they were engraved on a rock with an iron pen and lead, forever!",
    25: "For I know that my Redeemer lives, and He shall stand at last on the earth;",
    26: "and after my skin is destroyed, this I know, that in my flesh I shall see God,",
    27: "whom I shall see for myself, and my eyes shall behold, and not another. How my heart yearns within me!",
    28: "If you should say, 'How shall we persecute him?' — since the root of the matter is found in me,",
    29: "be afraid of the sword for yourselves; for wrath brings the punishment of the sword, that you may know there is a judgment.\"",
}

# Job 38 — God answers Job out of the whirlwind
ch38 = {
    1: "Then the LORD answered Job out of the whirlwind, and said:",
    2: "\"Who is this who darkens counsel by words without knowledge?",
    3: "Now prepare yourself like a man; I will question you, and you shall answer Me.",
    4: "Where were you when I laid the foundations of the earth? Tell Me, if you have understanding.",
    5: "Who determined its measurements? Surely you know! Or who stretched the line upon it?",
    6: "To what were its foundations fastened? Or who laid its cornerstone,",
    7: "when the morning stars sang together, and all the sons of God shouted for joy?",
    8: "\"Or who shut in the sea with doors, when it burst forth and issued from the womb;",
    9: "when I made the clouds its garment, and thick darkness its swaddling band;",
    10: "when I fixed My limit for it, and set bars and doors;",
    11: "when I said, 'This far you may come, but no farther, and here your proud waves must stop!'?",
    12: "\"Have you commanded the morning since your days began, and caused the dawn to know its place,",
    13: "that it might take hold of the ends of the earth, and the wicked be shaken out of it?",
    14: "It takes on form like clay under a seal, and stands out like a garment.",
    15: "From the wicked their light is withheld, and the upraised arm is broken.",
    16: "\"Have you entered the springs of the sea? Or have you walked in search of the depths?",
    17: "Have the gates of death been revealed to you? Or have you seen the doors of the shadow of death?",
    18: "Have you comprehended the breadth of the earth? Tell Me, if you know all this.",
    19: "\"Where is the way to the dwelling of light? And darkness, where is its place,",
    20: "that you may take it to its territory, that you may know the paths to its home?",
    21: "Do you know it, because you were born then, or because the number of your days is great?",
    22: "\"Have you entered the treasury of snow, or have you seen the treasury of hail,",
    23: "which I have reserved for the time of trouble, for the day of battle and war?",
    24: "By what way is light diffused, or the east wind scattered over the earth?",
    25: "\"Who has divided a channel for the overflowing water, or a path for the thunderbolt,",
    26: "to cause it to rain on a land where there is no one, a wilderness in which there is no man;",
    27: "to satisfy the desolate waste, and cause to spring forth the growth of tender grass?",
    28: "Has the rain a father? Or who has begotten the drops of dew?",
    29: "From whose womb comes the ice? And the frost of heaven, who gives it birth?",
    30: "The waters harden like stone, and the surface of the deep is frozen.",
    31: "\"Can you bind the cluster of the Pleiades, or loose the belt of Orion?",
    32: "Can you bring out Mazzaroth in its season? Or can you guide the Great Bear with its cubs?",
    33: "Do you know the ordinances of the heavens? Can you set their dominion over the earth?",
    34: "\"Can you lift up your voice to the clouds, that an abundance of water may cover you?",
    35: "Can you send out lightnings, that they may go, and say to you, 'Here we are!'?",
    36: "Who has put wisdom in the mind? Or who has given understanding to the heart?",
    37: "Who can number the clouds by wisdom? Or who can pour out the bottles of heaven,",
    38: "when the dust hardens in clumps, and the clods cling together?",
    39: "\"Can you hunt the prey for the lion, or satisfy the appetite of the young lions,",
    40: "when they crouch in their dens, or lurk in their lairs to lie in wait?",
    41: "Who provides food for the raven, when its young ones cry to God, and wander about for lack of food?",
}

# Job 42 — Job's repentance and restoration
ch42 = {
    1: "Then Job answered the LORD and said:",
    2: "\"I know that You can do everything, and that no purpose of Yours can be withheld from You.",
    3: "You asked, 'Who is this who hides counsel without knowledge?' Therefore I have uttered what I did not understand, things too wonderful for me, which I did not know.",
    4: "Listen, please, and let me speak; You said, 'I will question you, and you shall answer Me.'",
    5: "I have heard of You by the hearing of the ear, but now my eye sees You.",
    6: "Therefore I abhor myself, and repent in dust and ashes.\"",
    7: "And so it was, after the LORD had spoken these words to Job, that the LORD said to Eliphaz the Temanite, \"My wrath is aroused against you and your two friends, for you have not spoken of Me what is right, as My servant Job has.",
    8: "Now therefore, take for yourselves seven bulls and seven rams, go to My servant Job, and offer up for yourselves a burnt offering; and My servant Job shall pray for you. For I will accept him, lest I deal with you according to your folly; because you have not spoken of Me what is right, as My servant Job has.\"",
    9: "So Eliphaz the Temanite and Bildad the Shuhite and Zophar the Naamathite went and did as the LORD commanded them; for the LORD had accepted Job.",
    10: "And the LORD restored Job's losses when he prayed for his friends. Indeed the LORD gave Job twice as much as he had before.",
    11: "Then all his brothers, all his sisters, and all those who had been his acquaintances before, came to him and ate food with him in his house; and they consoled him and comforted him for all the adversity that the LORD had brought upon him. Each one gave him a piece of silver and each a ring of gold.",
    12: "Now the LORD blessed the latter days of Job more than his beginning; for he had fourteen thousand sheep, six thousand camels, one thousand yoke of oxen, and one thousand female donkeys.",
    13: "He also had seven sons and three daughters.",
    14: "And he called the name of the first Jemimah, the name of the second Keziah, and the name of the third Keren-Happuch.",
    15: "In all the land were found no women so beautiful as the daughters of Job; and their father gave them an inheritance among their brothers.",
    16: "After this Job lived one hundred and forty years, and saw his children and grandchildren for four generations.",
    17: "So Job died, old and full of days.",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"18_1_{v}"] = t
for v, t in ch2.items():
    ENTRIES[f"18_2_{v}"] = t
for v, t in ch19.items():
    ENTRIES[f"18_19_{v}"] = t
for v, t in ch38.items():
    ENTRIES[f"18_38_{v}"] = t
for v, t in ch42.items():
    ENTRIES[f"18_42_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Job landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
