"""MBT generator: Proverbs landmark chapters.

Book ID 20. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Sections authored:
- Proverbs 1 (33 verses) — the purpose of Proverbs; Wisdom's call
- Proverbs 3 (35 verses) — "Trust in the LORD with all your heart"
- Proverbs 8 (36 verses) — Wisdom personified
- Proverbs 31 (31 verses) — the virtuous woman

Total: 135 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Proverbs 1 — the prologue and Wisdom's call
ch1 = {
    1: "The proverbs of Solomon the son of David, king of Israel:",
    2: "to know wisdom and instruction, to perceive the words of understanding,",
    3: "to receive the instruction of wisdom, justice, judgment, and equity;",
    4: "to give prudence to the simple, to the young man knowledge and discretion —",
    5: "a wise man will hear and increase learning, and a man of understanding will attain wise counsel,",
    6: "to understand a proverb and an enigma, the words of the wise and their riddles.",
    7: "The fear of the LORD is the beginning of knowledge, but fools despise wisdom and instruction.",
    8: "My son, hear the instruction of your father, and do not forsake the law of your mother;",
    9: "for they will be a graceful ornament on your head, and chains about your neck.",
    10: "My son, if sinners entice you, do not consent.",
    11: "If they say, \"Come with us, let us lie in wait to shed blood; let us lurk secretly for the innocent without cause;",
    12: "let us swallow them alive like Sheol, and whole, like those who go down to the Pit;",
    13: "we shall find all kinds of precious possessions, we shall fill our houses with spoil;",
    14: "cast in your lot among us, let us all have one purse\" —",
    15: "my son, do not walk in the way with them, keep your foot from their path;",
    16: "for their feet run to evil, and they hasten to shed blood.",
    17: "Surely, in vain the net is spread in the sight of any bird;",
    18: "but they lie in wait for their own blood, they lurk secretly for their own lives.",
    19: "So are the ways of everyone who is greedy for gain; it takes away the life of its owners.",
    20: "Wisdom calls aloud outside; she raises her voice in the open squares.",
    21: "She cries out in the chief concourses, at the openings of the gates in the city she speaks her words:",
    22: "\"How long, you simple ones, will you love simplicity? For scorners delight in their scorning, and fools hate knowledge.",
    23: "Turn at my rebuke; surely I will pour out my spirit on you; I will make my words known to you.",
    24: "Because I have called and you refused, I have stretched out my hand and no one regarded,",
    25: "because you disdained all my counsel, and would have none of my rebuke,",
    26: "I also will laugh at your calamity; I will mock when your terror comes,",
    27: "when your terror comes like a storm, and your destruction comes like a whirlwind, when distress and anguish come upon you.",
    28: "Then they will call on me, but I will not answer; they will seek me diligently, but they will not find me.",
    29: "Because they hated knowledge and did not choose the fear of the LORD,",
    30: "they would have none of my counsel and despised my every rebuke.",
    31: "Therefore they shall eat the fruit of their own way, and be filled to the full with their own fancies.",
    32: "For the turning away of the simple will slay them, and the complacency of fools will destroy them;",
    33: "but whoever listens to me will dwell safely, and will be secure, without fear of evil.\"",
}

# Proverbs 3 — Trust in the LORD
ch3 = {
    1: "My son, do not forget my law, but let your heart keep my commands;",
    2: "for length of days and long life and peace they will add to you.",
    3: "Let not mercy and truth forsake you; bind them around your neck, write them on the tablet of your heart,",
    4: "and so find favor and high esteem in the sight of God and man.",
    5: "Trust in the LORD with all your heart, and lean not on your own understanding;",
    6: "in all your ways acknowledge Him, and He shall direct your paths.",
    7: "Do not be wise in your own eyes; fear the LORD and depart from evil.",
    8: "It will be health to your flesh, and strength to your bones.",
    9: "Honor the LORD with your possessions, and with the firstfruits of all your increase;",
    10: "so your barns will be filled with plenty, and your vats will overflow with new wine.",
    11: "My son, do not despise the chastening of the LORD, nor detest His correction;",
    12: "for whom the LORD loves He corrects, just as a father the son in whom he delights.",
    13: "Happy is the man who finds wisdom, and the man who gains understanding;",
    14: "for her proceeds are better than the profits of silver, and her gain than fine gold.",
    15: "She is more precious than rubies, and all the things you may desire cannot compare with her.",
    16: "Length of days is in her right hand, in her left hand riches and honor.",
    17: "Her ways are ways of pleasantness, and all her paths are peace.",
    18: "She is a tree of life to those who take hold of her, and happy are all who retain her.",
    19: "The LORD by wisdom founded the earth; by understanding He established the heavens;",
    20: "by His knowledge the depths were broken up, and clouds drop down the dew.",
    21: "My son, let them not depart from your eyes — keep sound wisdom and discretion;",
    22: "so they will be life to your soul and grace to your neck.",
    23: "Then you will walk safely in your way, and your foot will not stumble.",
    24: "When you lie down, you will not be afraid; yes, you will lie down and your sleep will be sweet.",
    25: "Do not be afraid of sudden terror, nor of trouble from the wicked when it comes;",
    26: "for the LORD will be your confidence, and will keep your foot from being caught.",
    27: "Do not withhold good from those to whom it is due, when it is in the power of your hand to do so.",
    28: "Do not say to your neighbor, \"Go, and come back, and tomorrow I will give it,\" when you have it with you.",
    29: "Do not devise evil against your neighbor, for he dwells by you for safety's sake.",
    30: "Do not strive with a man without cause, if he has done you no harm.",
    31: "Do not envy the oppressor, and choose none of his ways;",
    32: "for the perverse person is an abomination to the LORD, but His secret counsel is with the upright.",
    33: "The curse of the LORD is on the house of the wicked, but He blesses the home of the just.",
    34: "Surely He scorns the scornful, but gives grace to the humble.",
    35: "The wise shall inherit glory, but shame shall be the legacy of fools.",
}

# Proverbs 8 — Wisdom personified
ch8 = {
    1: "Does not wisdom cry out, and understanding lift up her voice?",
    2: "She takes her stand on the top of the high hill, beside the way, where the paths meet.",
    3: "She cries out by the gates, at the entry of the city, at the entrance of the doors:",
    4: "\"To you, O men, I call, and my voice is to the sons of men.",
    5: "O you simple ones, understand prudence, and you fools, be of an understanding heart.",
    6: "Listen, for I will speak of excellent things, and from the opening of my lips will come right things;",
    7: "for my mouth will speak truth; wickedness is an abomination to my lips.",
    8: "All the words of my mouth are with righteousness; nothing crooked or perverse is in them.",
    9: "They are all plain to him who understands, and right to those who find knowledge.",
    10: "Receive my instruction, and not silver, and knowledge rather than choice gold;",
    11: "for wisdom is better than rubies, and all the things one may desire cannot be compared with her.",
    12: "\"I, wisdom, dwell with prudence, and find out knowledge and discretion.",
    13: "The fear of the LORD is to hate evil; pride and arrogance and the evil way and the perverse mouth I hate.",
    14: "Counsel is mine, and sound wisdom; I am understanding, I have strength.",
    15: "By me kings reign, and rulers decree justice.",
    16: "By me princes rule, and nobles, all the judges of the earth.",
    17: "I love those who love me, and those who seek me diligently will find me.",
    18: "Riches and honor are with me, enduring riches and righteousness.",
    19: "My fruit is better than gold, yes, than fine gold, and my revenue than choice silver.",
    20: "I traverse the way of righteousness, in the midst of the paths of justice,",
    21: "that I may cause those who love me to inherit wealth, that I may fill their treasuries.",
    22: "\"The LORD possessed me at the beginning of His way, before His works of old.",
    23: "I have been established from everlasting, from the beginning, before there was ever an earth.",
    24: "When there were no depths I was brought forth, when there were no fountains abounding with water.",
    25: "Before the mountains were settled, before the hills, I was brought forth;",
    26: "while as yet He had not made the earth or the fields, or the primal dust of the world.",
    27: "When He prepared the heavens, I was there, when He drew a circle on the face of the deep,",
    28: "when He established the clouds above, when He strengthened the fountains of the deep,",
    29: "when He assigned to the sea its limit, so that the waters would not transgress His command, when He marked out the foundations of the earth,",
    30: "then I was beside Him as a master craftsman; and I was daily His delight, rejoicing always before Him,",
    31: "rejoicing in His inhabited world, and my delight was with the sons of men.",
    32: "\"Now therefore, listen to me, my children, for blessed are those who keep my ways.",
    33: "Hear instruction and be wise, and do not disdain it.",
    34: "Blessed is the man who listens to me, watching daily at my gates, waiting at the posts of my doors.",
    35: "For whoever finds me finds life, and obtains favor from the LORD;",
    36: "but he who sins against me wrongs his own soul; all those who hate me love death.\"",
}

# Proverbs 31 — the virtuous woman
ch31 = {
    1: "The words of King Lemuel, the utterance which his mother taught him:",
    2: "What, my son? And what, son of my womb? And what, son of my vows?",
    3: "Do not give your strength to women, nor your ways to that which destroys kings.",
    4: "It is not for kings, O Lemuel, it is not for kings to drink wine, nor for princes intoxicating drink;",
    5: "lest they drink and forget the law, and pervert the justice of all the afflicted.",
    6: "Give strong drink to him who is perishing, and wine to those who are bitter of heart.",
    7: "Let him drink and forget his poverty, and remember his misery no more.",
    8: "Open your mouth for the speechless, in the cause of all who are appointed to die.",
    9: "Open your mouth, judge righteously, and plead the cause of the poor and needy.",
    10: "Who can find a virtuous wife? For her worth is far above rubies.",
    11: "The heart of her husband safely trusts her; so he will have no lack of gain.",
    12: "She does him good and not evil all the days of her life.",
    13: "She seeks wool and flax, and willingly works with her hands.",
    14: "She is like the merchant ships, she brings her food from afar.",
    15: "She also rises while it is yet night, and provides food for her household, and a portion for her maidservants.",
    16: "She considers a field and buys it; from her profits she plants a vineyard.",
    17: "She girds herself with strength, and strengthens her arms.",
    18: "She perceives that her merchandise is good, and her lamp does not go out by night.",
    19: "She stretches out her hands to the distaff, and her hand holds the spindle.",
    20: "She extends her hand to the poor, yes, she reaches out her hands to the needy.",
    21: "She is not afraid of snow for her household, for all her household is clothed with scarlet.",
    22: "She makes tapestry for herself; her clothing is fine linen and purple.",
    23: "Her husband is known in the gates, when he sits among the elders of the land.",
    24: "She makes linen garments and sells them, and supplies sashes for the merchants.",
    25: "Strength and honor are her clothing; she shall rejoice in time to come.",
    26: "She opens her mouth with wisdom, and on her tongue is the law of kindness.",
    27: "She watches over the ways of her household, and does not eat the bread of idleness.",
    28: "Her children rise up and call her blessed; her husband also, and he praises her:",
    29: "\"Many daughters have done well, but you excel them all.\"",
    30: "Charm is deceitful and beauty is passing, but a woman who fears the LORD, she shall be praised.",
    31: "Give her of the fruit of her hands, and let her own works praise her in the gates.",
}

ENTRIES = {}
for v, t in ch1.items():
    ENTRIES[f"20_1_{v}"] = t
for v, t in ch3.items():
    ENTRIES[f"20_3_{v}"] = t
for v, t in ch8.items():
    ENTRIES[f"20_8_{v}"] = t
for v, t in ch31.items():
    ENTRIES[f"20_31_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Proverbs landmark verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
