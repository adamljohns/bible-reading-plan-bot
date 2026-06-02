"""MBT OT landmark passages — Wisdom & Psalms.

Psalm 51 (19v), Psalm 91 (16v), Psalm 100 (5v), Psalm 121 (8v),
Psalm 139 (24v), Proverbs 31:10-31 (22v). 94 verses total.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Psalm 51 — David's prayer of repentance after the Bathsheba incident
ps_51 = {
    1: "For the Chief Musician. A Psalm of David, when Nathan the prophet came to him after he had gone in to Bathsheba. Be gracious to me, O God, according to Your lovingkindness — according to the greatness of Your compassion, blot out my transgressions.",
    2: "Wash me thoroughly from my iniquity, and cleanse me from my sin.",
    3: "For I know my transgressions — and my sin is ever before me.",
    4: "Against You, You only, I have sinned, and done what is evil in Your sight — so that You are justified when You speak, and blameless when You judge.",
    5: "Behold, I was brought forth in iniquity — and in sin my mother conceived me.",
    6: "Behold, You desire truth in the innermost being — and in the hidden part You will make me know wisdom.",
    7: "Purify me with hyssop, and I shall be clean. Wash me, and I shall be whiter than snow.",
    8: "Make me to hear joy and gladness — let the bones which You have broken rejoice.",
    9: "Hide Your face from my sins, and blot out all my iniquities.",
    10: "Create in me a clean heart, O God — and renew a steadfast spirit within me.",
    11: "Do not cast me away from Your presence — and do not take Your Holy Spirit from me.",
    12: "Restore to me the joy of Your salvation — and sustain me with a willing spirit.",
    13: "Then I will teach transgressors Your ways — and sinners will be converted to You.",
    14: "Deliver me from bloodguiltiness, O God — the God of my salvation. And my tongue will joyfully sing of Your righteousness.",
    15: "O Lord, open my lips — that my mouth may declare Your praise.",
    16: "For You do not delight in sacrifice — otherwise I would give it. You are not pleased with burnt offering.",
    17: "The sacrifices of God are a broken spirit — a broken and a contrite heart, O God, You will not despise.",
    18: "In Your favor do good to Zion — build the walls of Jerusalem.",
    19: "Then You will delight in righteous sacrifices, in burnt offering and whole burnt offering — then young bulls will be offered on Your altar.",
}

# Psalm 91 — Dwelling in the shelter of the Most High
ps_91 = {
    1: "He who dwells in the shelter of the Most High will abide in the shadow of the Almighty.",
    2: "I will say to the LORD, \"My refuge and my fortress — my God, in whom I trust.\"",
    3: "For it is He who delivers you from the snare of the trapper, and from the deadly pestilence.",
    4: "He will cover you with His pinions, and under His wings you may seek refuge. His faithfulness is a shield and bulwark.",
    5: "You will not be afraid of the terror by night, or of the arrow that flies by day,",
    6: "of the pestilence that stalks in darkness, or of the destruction that lays waste at noon.",
    7: "A thousand may fall at your side, and ten thousand at your right hand — but it shall not approach you.",
    8: "You will only look on with your eyes, and see the recompense of the wicked.",
    9: "For you have made the LORD, my refuge — even the Most High, your dwelling place.",
    10: "No evil will befall you, nor will any plague come near your tent.",
    11: "For He will give His angels charge concerning you, to guard you in all your ways.",
    12: "They will bear you up in their hands, lest you strike your foot against a stone.",
    13: "You will tread upon the lion and cobra — the young lion and the serpent you will trample down.",
    14: "\"Because he has loved Me, therefore I will deliver him. I will set him securely on high, because he has known My name.",
    15: "He will call upon Me, and I will answer him — I will be with him in trouble. I will rescue him, and honor him.",
    16: "With a long life I will satisfy him, and let him behold My salvation.\"",
}

# Psalm 100 — A psalm for thanksgiving
ps_100 = {
    1: "A Psalm for Thanksgiving. Shout joyfully to the LORD, all the earth.",
    2: "Serve the LORD with gladness — come before Him with joyful singing.",
    3: "Know that the LORD Himself is God — it is He who has made us, and not we ourselves; we are His people and the sheep of His pasture.",
    4: "Enter His gates with thanksgiving, and His courts with praise. Give thanks to Him — bless His name.",
    5: "For the LORD is good — His lovingkindness is everlasting, and His faithfulness to all generations.",
}

# Psalm 121 — I lift up my eyes
ps_121 = {
    1: "A Song of Ascents. I will lift up my eyes to the mountains — from where shall my help come?",
    2: "My help comes from the LORD — who made heaven and earth.",
    3: "He will not allow your foot to slip. He who keeps you will not slumber.",
    4: "Behold, He who keeps Israel will neither slumber nor sleep.",
    5: "The LORD is your keeper. The LORD is your shade on your right hand.",
    6: "The sun will not smite you by day, nor the moon by night.",
    7: "The LORD will protect you from all evil. He will keep your soul.",
    8: "The LORD will guard your going out and your coming in — from this time forth, and forever.",
}

# Psalm 139 — Search me, O God
ps_139 = {
    1: "For the Chief Musician. A Psalm of David. O LORD, You have searched me, and known me.",
    2: "You know when I sit down and when I rise up — You understand my thought from afar.",
    3: "You scrutinize my path and my lying down — and are intimately acquainted with all my ways.",
    4: "Even before there is a word on my tongue — behold, O LORD, You know it all.",
    5: "You have enclosed me behind and before — and laid Your hand upon me.",
    6: "Such knowledge is too wonderful for me — it is too high, I cannot attain to it.",
    7: "Where can I go from Your Spirit? Or where can I flee from Your presence?",
    8: "If I ascend to heaven, You are there. If I make my bed in Sheol, behold, You are there.",
    9: "If I take the wings of the dawn — if I dwell in the remotest part of the sea,",
    10: "even there Your hand will lead me — and Your right hand will lay hold of me.",
    11: "If I say, \"Surely the darkness will overwhelm me, and the light around me will be night\" —",
    12: "even the darkness is not dark to You — and the night is as bright as the day. Darkness and light are alike to You.",
    13: "For You formed my inward parts — You wove me in my mother's womb.",
    14: "I will give thanks to You — for I am fearfully and wonderfully made. Wonderful are Your works — and my soul knows it very well.",
    15: "My frame was not hidden from You — when I was made in secret, and skillfully wrought in the depths of the earth.",
    16: "Your eyes have seen my unformed substance — and in Your book they were all written, the days that were ordained for me, when as yet there was not one of them.",
    17: "How precious also are Your thoughts to me, O God! How vast is the sum of them!",
    18: "If I should count them, they would outnumber the sand. When I awake, I am still with You.",
    19: "O that You would slay the wicked, O God — depart from me, therefore, O men of bloodshed.",
    20: "For they speak against You wickedly — and Your enemies take Your name in vain.",
    21: "Do I not hate those who hate You, O LORD? And do I not loathe those who rise up against You?",
    22: "I hate them with the utmost hatred — they have become my enemies.",
    23: "Search me, O God, and know my heart — try me, and know my anxious thoughts.",
    24: "And see if there be any hurtful way in me — and lead me in the everlasting way.",
}

# Proverbs 31:10-31 — The Excellent Wife
prov_31 = {
    10: "An excellent wife — who can find her? For her worth is far above jewels.",
    11: "The heart of her husband trusts in her — and he will have no lack of gain.",
    12: "She does him good and not evil all the days of her life.",
    13: "She looks for wool and flax, and works with her hands in delight.",
    14: "She is like merchant ships — she brings her food from afar.",
    15: "She rises also while it is still night, and gives food to her household — and portions to her maidens.",
    16: "She considers a field and buys it — from her earnings she plants a vineyard.",
    17: "She girds herself with strength, and makes her arms strong.",
    18: "She senses that her gain is good — her lamp does not go out at night.",
    19: "She stretches out her hands to the distaff — and her hands grasp the spindle.",
    20: "She extends her hand to the poor — and she stretches out her hands to the needy.",
    21: "She is not afraid of the snow for her household — for all her household are clothed with scarlet.",
    22: "She makes coverings for herself — her clothing is fine linen and purple.",
    23: "Her husband is known in the gates, when he sits among the elders of the land.",
    24: "She makes linen garments and sells them — and supplies belts to the tradesmen.",
    25: "Strength and dignity are her clothing — and she smiles at the future.",
    26: "She opens her mouth in wisdom — and the teaching of kindness is on her tongue.",
    27: "She looks well to the ways of her household — and does not eat the bread of idleness.",
    28: "Her children rise up and bless her — her husband also, and he praises her, saying:",
    29: "\"Many daughters have done nobly — but you excel them all.\"",
    30: "Charm is deceitful, and beauty is vain — but a woman who fears the LORD, she shall be praised.",
    31: "Give her the product of her hands — and let her works praise her in the gates.",
}

ENTRIES = {}
for v, t in ps_51.items():   ENTRIES[f"19_51_{v}"] = t
for v, t in ps_91.items():   ENTRIES[f"19_91_{v}"] = t
for v, t in ps_100.items():  ENTRIES[f"19_100_{v}"] = t
for v, t in ps_121.items():  ENTRIES[f"19_121_{v}"] = t
for v, t in ps_139.items():  ENTRIES[f"19_139_{v}"] = t
for v, t in prov_31.items(): ENTRIES[f"20_31_{v}"] = t

def main():
    print(f"MBT OT Wisdom/Psalms landmark verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json updated.")

if __name__ == "__main__":
    main()
