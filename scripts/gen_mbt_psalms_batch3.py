"""MBT generator: Psalms batch 3 — the most-memorized remaining psalms.

Book ID 19. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Psalms authored:
- Psalm 1 (6 verses) — the two ways
- Psalm 23 (6 verses) — the LORD is my shepherd
- Psalm 51 (19 verses) — David's confession after Bathsheba
- Psalm 91 (16 verses) — he who dwells in the secret place
- Psalm 100 (5 verses) — make a joyful shout to the LORD
- Psalm 121 (8 verses) — I will lift up my eyes to the hills
- Psalm 139 (24 verses) — You have searched me and known me

Total: 84 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ps1 = {
    1: "Blessed is the man who walks not in the counsel of the ungodly, nor stands in the path of sinners, nor sits in the seat of the scornful;",
    2: "but his delight is in the law of the LORD, and in His law he meditates day and night.",
    3: "He shall be like a tree planted by the rivers of water, that brings forth its fruit in its season, whose leaf also shall not wither; and whatever he does shall prosper.",
    4: "The ungodly are not so, but are like the chaff which the wind drives away.",
    5: "Therefore the ungodly shall not stand in the judgment, nor sinners in the congregation of the righteous.",
    6: "For the LORD knows the way of the righteous, but the way of the ungodly shall perish.",
}

ps23 = {
    1: "The LORD is my shepherd; I shall not want.",
    2: "He makes me to lie down in green pastures; He leads me beside the still waters.",
    3: "He restores my soul; He leads me in the paths of righteousness for His name's sake.",
    4: "Yea, though I walk through the valley of the shadow of death, I will fear no evil; for You are with me; Your rod and Your staff, they comfort me.",
    5: "You prepare a table before me in the presence of my enemies; You anoint my head with oil; my cup runs over.",
    6: "Surely goodness and mercy shall follow me all the days of my life; and I will dwell in the house of the LORD forever.",
}

ps51 = {
    1: "Have mercy upon me, O God, according to Your lovingkindness; according to the multitude of Your tender mercies, blot out my transgressions.",
    2: "Wash me thoroughly from my iniquity, and cleanse me from my sin.",
    3: "For I acknowledge my transgressions, and my sin is always before me.",
    4: "Against You, You only, have I sinned, and done this evil in Your sight — that You may be found just when You speak, and blameless when You judge.",
    5: "Behold, I was brought forth in iniquity, and in sin my mother conceived me.",
    6: "Behold, You desire truth in the inward parts, and in the hidden part You will make me to know wisdom.",
    7: "Purge me with hyssop, and I shall be clean; wash me, and I shall be whiter than snow.",
    8: "Make me hear joy and gladness, that the bones You have broken may rejoice.",
    9: "Hide Your face from my sins, and blot out all my iniquities.",
    10: "Create in me a clean heart, O God, and renew a steadfast spirit within me.",
    11: "Do not cast me away from Your presence, and do not take Your Holy Spirit from me.",
    12: "Restore to me the joy of Your salvation, and uphold me by Your generous Spirit.",
    13: "Then I will teach transgressors Your ways, and sinners shall be converted to You.",
    14: "Deliver me from the guilt of bloodshed, O God, the God of my salvation, and my tongue shall sing aloud of Your righteousness.",
    15: "O Lord, open my lips, and my mouth shall show forth Your praise.",
    16: "For You do not desire sacrifice, or else I would give it; You do not delight in burnt offering.",
    17: "The sacrifices of God are a broken spirit, a broken and a contrite heart — these, O God, You will not despise.",
    18: "Do good in Your good pleasure to Zion; build the walls of Jerusalem.",
    19: "Then You shall be pleased with the sacrifices of righteousness, with burnt offering and whole burnt offering; then they shall offer bulls on Your altar.",
}

ps91 = {
    1: "He who dwells in the secret place of the Most High shall abide under the shadow of the Almighty.",
    2: "I will say of the LORD, \"He is my refuge and my fortress; my God, in Him I will trust.\"",
    3: "Surely He shall deliver you from the snare of the fowler and from the perilous pestilence.",
    4: "He shall cover you with His feathers, and under His wings you shall take refuge; His truth shall be your shield and buckler.",
    5: "You shall not be afraid of the terror by night, nor of the arrow that flies by day,",
    6: "nor of the pestilence that walks in darkness, nor of the destruction that lays waste at noonday.",
    7: "A thousand may fall at your side, and ten thousand at your right hand; but it shall not come near you.",
    8: "Only with your eyes shall you look, and see the reward of the wicked.",
    9: "Because you have made the LORD, who is my refuge, even the Most High, your dwelling place,",
    10: "no evil shall befall you, nor shall any plague come near your dwelling;",
    11: "for He shall give His angels charge over you, to keep you in all your ways.",
    12: "In their hands they shall bear you up, lest you dash your foot against a stone.",
    13: "You shall tread upon the lion and the cobra, the young lion and the serpent you shall trample underfoot.",
    14: "\"Because he has set his love upon Me, therefore I will deliver him; I will set him on high, because he has known My name.",
    15: "He shall call upon Me, and I will answer him; I will be with him in trouble; I will deliver him and honor him.",
    16: "With long life I will satisfy him, and show him My salvation.\"",
}

ps100 = {
    1: "Make a joyful shout to the LORD, all you lands!",
    2: "Serve the LORD with gladness; come before His presence with singing.",
    3: "Know that the LORD, He is God; it is He who has made us, and not we ourselves; we are His people and the sheep of His pasture.",
    4: "Enter into His gates with thanksgiving, and into His courts with praise. Be thankful to Him, and bless His name.",
    5: "For the LORD is good; His mercy is everlasting, and His truth endures to all generations.",
}

ps121 = {
    1: "I will lift up my eyes to the hills — from whence comes my help?",
    2: "My help comes from the LORD, who made heaven and earth.",
    3: "He will not allow your foot to be moved; He who keeps you will not slumber.",
    4: "Behold, He who keeps Israel shall neither slumber nor sleep.",
    5: "The LORD is your keeper; the LORD is your shade at your right hand.",
    6: "The sun shall not strike you by day, nor the moon by night.",
    7: "The LORD shall preserve you from all evil; He shall preserve your soul.",
    8: "The LORD shall preserve your going out and your coming in from this time forth, and even forevermore.",
}

ps139 = {
    1: "O LORD, You have searched me and known me.",
    2: "You know my sitting down and my rising up; You understand my thought afar off.",
    3: "You comprehend my path and my lying down, and are acquainted with all my ways.",
    4: "For there is not a word on my tongue, but behold, O LORD, You know it altogether.",
    5: "You have hedged me behind and before, and laid Your hand upon me.",
    6: "Such knowledge is too wonderful for me; it is high, I cannot attain it.",
    7: "Where can I go from Your Spirit? Or where can I flee from Your presence?",
    8: "If I ascend into heaven, You are there; if I make my bed in hell, behold, You are there.",
    9: "If I take the wings of the morning, and dwell in the uttermost parts of the sea,",
    10: "even there Your hand shall lead me, and Your right hand shall hold me.",
    11: "If I say, \"Surely the darkness shall fall on me,\" even the night shall be light about me;",
    12: "indeed, the darkness shall not hide from You, but the night shines as the day; the darkness and the light are both alike to You.",
    13: "For You formed my inward parts; You covered me in my mother's womb.",
    14: "I will praise You, for I am fearfully and wonderfully made; marvelous are Your works, and that my soul knows very well.",
    15: "My frame was not hidden from You, when I was made in secret, and skillfully wrought in the lowest parts of the earth.",
    16: "Your eyes saw my substance, being yet unformed. And in Your book they all were written, the days fashioned for me, when as yet there were none of them.",
    17: "How precious also are Your thoughts to me, O God! How great is the sum of them!",
    18: "If I should count them, they would be more in number than the sand; when I awake, I am still with You.",
    19: "Oh, that You would slay the wicked, O God! Depart from me, therefore, you bloodthirsty men.",
    20: "For they speak against You wickedly; Your enemies take Your name in vain.",
    21: "Do I not hate them, O LORD, who hate You? And do I not loathe those who rise up against You?",
    22: "I hate them with perfect hatred; I count them my enemies.",
    23: "Search me, O God, and know my heart; try me, and know my anxieties;",
    24: "and see if there is any wicked way in me, and lead me in the way everlasting.",
}

ENTRIES = {}
for v, t in ps1.items():
    ENTRIES[f"19_1_{v}"] = t
for v, t in ps23.items():
    ENTRIES[f"19_23_{v}"] = t
for v, t in ps51.items():
    ENTRIES[f"19_51_{v}"] = t
for v, t in ps91.items():
    ENTRIES[f"19_91_{v}"] = t
for v, t in ps100.items():
    ENTRIES[f"19_100_{v}"] = t
for v, t in ps121.items():
    ENTRIES[f"19_121_{v}"] = t
for v, t in ps139.items():
    ENTRIES[f"19_139_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Psalms batch 3 verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
