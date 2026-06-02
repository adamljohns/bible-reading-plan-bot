"""MBT generator: 1 Samuel landmark chapters.

Book ID 9. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- 1 Samuel 1 (28 verses) — Hannah's prayer and the birth of Samuel
- 1 Samuel 2:1-10 (10 verses) — Hannah's song
- 1 Samuel 3 (21 verses) — the call of Samuel
- 1 Samuel 16 (23 verses) — Samuel anoints David

Total: 82 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# 1 Samuel 1 — Hannah's prayer and Samuel's birth
ch1 = {
    1: "Now there was a certain man of Ramathaim Zophim, of the mountains of Ephraim, and his name was Elkanah the son of Jeroham, the son of Elihu, the son of Tohu, the son of Zuph, an Ephraimite.",
    2: "And he had two wives: the name of one was Hannah, and the name of the other Peninnah. Peninnah had children, but Hannah had no children.",
    3: "This man went up from his city yearly to worship and sacrifice to the LORD of hosts in Shiloh. Also the two sons of Eli, Hophni and Phinehas, the priests of the LORD, were there.",
    4: "And whenever the time came for Elkanah to make an offering, he would give portions to Peninnah his wife and to all her sons and daughters.",
    5: "But to Hannah he would give a double portion, for he loved Hannah, although the LORD had closed her womb.",
    6: "And her rival also provoked her severely, to make her miserable, because the LORD had closed her womb.",
    7: "So it was, year by year, when she went up to the house of the LORD, that she provoked her; therefore she wept and did not eat.",
    8: "Then Elkanah her husband said to her, \"Hannah, why do you weep? Why do you not eat? And why is your heart grieved? Am I not better to you than ten sons?\"",
    9: "So Hannah arose after they had finished eating and drinking in Shiloh. Now Eli the priest was sitting on the seat by the doorpost of the tabernacle of the LORD.",
    10: "And she was in bitterness of soul, and prayed to the LORD and wept in anguish.",
    11: "Then she made a vow and said, \"O LORD of hosts, if You will indeed look on the affliction of Your maidservant and remember me, and not forget Your maidservant, but will give Your maidservant a male child, then I will give him to the LORD all the days of his life, and no razor shall come upon his head.\"",
    12: "And it happened, as she continued praying before the LORD, that Eli watched her mouth.",
    13: "Now Hannah spoke in her heart; only her lips moved, but her voice was not heard. Therefore Eli thought she was drunk.",
    14: "So Eli said to her, \"How long will you be drunk? Put your wine away from you!\"",
    15: "But Hannah answered and said, \"No, my lord, I am a woman of sorrowful spirit. I have drunk neither wine nor intoxicating drink, but have poured out my soul before the LORD.",
    16: "Do not consider your maidservant a wicked woman, for out of the abundance of my complaint and grief I have spoken until now.\"",
    17: "Then Eli answered and said, \"Go in peace, and the God of Israel grant your petition which you have asked of Him.\"",
    18: "And she said, \"Let your maidservant find favor in your sight.\" So the woman went her way and ate, and her face was no longer sad.",
    19: "Then they rose early in the morning and worshiped before the LORD, and returned and came to their house at Ramah. And Elkanah knew Hannah his wife, and the LORD remembered her.",
    20: "So it came to pass in the process of time that Hannah conceived and bore a son, and called his name Samuel, saying, \"Because I have asked for him from the LORD.\"",
    21: "Now the man Elkanah and all his house went up to offer to the LORD the yearly sacrifice and his vow.",
    22: "But Hannah did not go up, for she said to her husband, \"Not until the child is weaned; then I will take him, that he may appear before the LORD and remain there forever.\"",
    23: "So Elkanah her husband said to her, \"Do what seems best to you; wait until you have weaned him. Only let the LORD establish His word.\" Then the woman stayed and nursed her son until she had weaned him.",
    24: "Now when she had weaned him, she took him up with her, with three bulls, one ephah of flour, and a skin of wine, and brought him to the house of the LORD in Shiloh. And the child was young.",
    25: "Then they slaughtered a bull, and brought the child to Eli.",
    26: "And she said, \"O my lord! As your soul lives, my lord, I am the woman who stood by you here, praying to the LORD.",
    27: "For this child I prayed, and the LORD has granted me my petition which I asked of Him.",
    28: "Therefore I also have lent him to the LORD; as long as he lives he shall be lent to the LORD.\" So they worshiped the LORD there.",
}

# 1 Samuel 2:1-10 — Hannah's song
ch2 = {
    1: "And Hannah prayed and said: \"My heart rejoices in the LORD; my horn is exalted in the LORD. I smile at my enemies, because I rejoice in Your salvation.",
    2: "\"No one is holy like the LORD, for there is none besides You, nor is there any rock like our God.",
    3: "Talk no more so very proudly; let no arrogance come from your mouth, for the LORD is the God of knowledge; and by Him actions are weighed.",
    4: "\"The bows of the mighty men are broken, and those who stumbled are girded with strength.",
    5: "Those who were full have hired themselves out for bread, and those who were hungry have ceased to hunger. Even the barren has borne seven, and she who has many children has become feeble.",
    6: "\"The LORD kills and makes alive; He brings down to the grave and brings up.",
    7: "The LORD makes poor and makes rich; He brings low and lifts up.",
    8: "He raises the poor from the dust and lifts the beggar from the ash heap, to set them among princes and make them inherit the throne of glory. \"For the pillars of the earth are the LORD's, and He has set the world upon them.",
    9: "He will guard the feet of His saints, but the wicked shall be silent in darkness. For by strength no man shall prevail.",
    10: "The adversaries of the LORD shall be broken in pieces; from heaven He will thunder against them. The LORD will judge the ends of the earth. He will give strength to His king, and exalt the horn of His anointed.\"",
}

# 1 Samuel 3 — the call of Samuel
ch3 = {
    1: "Then the boy Samuel ministered to the LORD before Eli. And the word of the LORD was rare in those days; there was no widespread revelation.",
    2: "And it came to pass at that time, while Eli was lying down in his place, and when his eyes had begun to grow so dim that he could not see,",
    3: "and before the lamp of God went out in the tabernacle of the LORD where the ark of God was, and while Samuel was lying down,",
    4: "that the LORD called Samuel. And he answered, \"Here I am!\"",
    5: "So he ran to Eli and said, \"Here I am, for you called me.\" And he said, \"I did not call; lie down again.\" And he went and lay down.",
    6: "Then the LORD called yet again, \"Samuel!\" So Samuel arose and went to Eli, and said, \"Here I am, for you called me.\" He answered, \"I did not call, my son; lie down again.\"",
    7: "(Now Samuel did not yet know the LORD, nor was the word of the LORD yet revealed to him.)",
    8: "And the LORD called Samuel again the third time. Then he arose and went to Eli, and said, \"Here I am, for you did call me.\" Then Eli perceived that the LORD had called the boy.",
    9: "Therefore Eli said to Samuel, \"Go, lie down; and it shall be, if He calls you, that you must say, 'Speak, LORD, for Your servant hears.'\" So Samuel went and lay down in his place.",
    10: "Now the LORD came and stood and called as at other times, \"Samuel! Samuel!\" And Samuel answered, \"Speak, for Your servant hears.\"",
    11: "Then the LORD said to Samuel: \"Behold, I will do something in Israel at which both ears of everyone who hears it will tingle.",
    12: "In that day I will perform against Eli all that I have spoken concerning his house, from beginning to end.",
    13: "For I have told him that I will judge his house forever for the iniquity which he knows, because his sons made themselves vile, and he did not restrain them.",
    14: "And therefore I have sworn to the house of Eli that the iniquity of Eli's house shall not be atoned for by sacrifice or offering forever.\"",
    15: "So Samuel lay down until morning, and opened the doors of the house of the LORD. And Samuel was afraid to tell Eli the vision.",
    16: "Then Eli called Samuel, and said, \"Samuel, my son!\" He answered, \"Here I am.\"",
    17: "And he said, \"What is the word that the LORD spoke to you? Please do not hide it from me. God do so to you, and more also, if you hide anything from me of all the things that He said to you.\"",
    18: "Then Samuel told him everything, and hid nothing from him. And he said, \"It is the LORD. Let Him do what seems good to Him.\"",
    19: "So Samuel grew, and the LORD was with him and let none of his words fall to the ground.",
    20: "And all Israel from Dan to Beersheba knew that Samuel had been established as a prophet of the LORD.",
    21: "Then the LORD appeared again in Shiloh. For the LORD revealed Himself to Samuel in Shiloh by the word of the LORD.",
}

# 1 Samuel 16 — Samuel anoints David
ch16 = {
    1: "Now the LORD said to Samuel, \"How long will you mourn for Saul, seeing I have rejected him from reigning over Israel? Fill your horn with oil, and go; I am sending you to Jesse the Bethlehemite. For I have provided Myself a king among his sons.\"",
    2: "And Samuel said, \"How can I go? If Saul hears it, he will kill me.\" But the LORD said, \"Take a heifer with you, and say, 'I have come to sacrifice to the LORD.'",
    3: "Then invite Jesse to the sacrifice, and I will show you what you shall do; you shall anoint for Me the one I name to you.\"",
    4: "So Samuel did what the LORD said, and went to Bethlehem. And the elders of the town trembled at his coming, and said, \"Do you come peaceably?\"",
    5: "And he said, \"Peaceably; I have come to sacrifice to the LORD. Sanctify yourselves, and come with me to the sacrifice.\" Then he consecrated Jesse and his sons, and invited them to the sacrifice.",
    6: "So it was, when they came, that he looked at Eliab and said, \"Surely the LORD's anointed is before Him.\"",
    7: "But the LORD said to Samuel, \"Do not look at his appearance or at his physical stature, because I have refused him. For the LORD does not see as man sees; for man looks at the outward appearance, but the LORD looks at the heart.\"",
    8: "So Jesse called Abinadab, and made him pass before Samuel. And he said, \"Neither has the LORD chosen this one.\"",
    9: "Then Jesse made Shammah pass by. And he said, \"Neither has the LORD chosen this one.\"",
    10: "Thus Jesse made seven of his sons pass before Samuel. And Samuel said to Jesse, \"The LORD has not chosen these.\"",
    11: "And Samuel said to Jesse, \"Are all the young men here?\" Then he said, \"There remains yet the youngest, and there he is, keeping the sheep.\" And Samuel said to Jesse, \"Send and bring him. For we will not sit down till he comes here.\"",
    12: "So he sent and brought him in. Now he was ruddy, with bright eyes, and good-looking. And the LORD said, \"Arise, anoint him; for this is the one!\"",
    13: "Then Samuel took the horn of oil and anointed him in the midst of his brothers; and the Spirit of the LORD came upon David from that day forward. So Samuel arose and went to Ramah.",
    14: "But the Spirit of the LORD departed from Saul, and a distressing spirit from the LORD troubled him.",
    15: "And Saul's servants said to him, \"Surely, a distressing spirit from God is troubling you.",
    16: "Let our master now command your servants, who are before you, to seek out a man who is a skillful player on the harp. And it shall be that he will play it with his hand when the distressing spirit from God is upon you, and you shall be well.\"",
    17: "So Saul said to his servants, \"Provide me now a man who can play well, and bring him to me.\"",
    18: "Then one of the servants answered and said, \"Look, I have seen a son of Jesse the Bethlehemite, who is skillful in playing, a mighty man of valor, a man of war, prudent in speech, and a handsome person; and the LORD is with him.\"",
    19: "Therefore Saul sent messengers to Jesse, and said, \"Send me your son David, who is with the sheep.\"",
    20: "And Jesse took a donkey loaded with bread, a skin of wine, and a young goat, and sent them by his son David to Saul.",
    21: "So David came to Saul and stood before him. And he loved him greatly, and he became his armorbearer.",
    22: "Then Saul sent to Jesse, saying, \"Please let David stand before me, for he has found favor in my sight.\"",
    23: "And so it was, whenever the spirit from God was upon Saul, that David would take a harp and play it with his hand. Then Saul would become refreshed and well, and the distressing spirit would depart from him.",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"9_1_{v}"] = t
for v, t in ch2.items():
    ENTRIES[f"9_2_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"9_3_{v}"] = t
for v, t in ch16.items():
    ENTRIES[f"9_16_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"1 Samuel landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
