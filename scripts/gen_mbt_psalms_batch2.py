"""MBT Psalms expansion batch 2 — Psalms 42-43, 46, 63, 84, 90, 103, 107, 116, 117, 145, 150. ~190 verses."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

# Psalm 42 — As the deer pants
ps_42 = {
    1: "For the choir director. A Maskil of the sons of Korah. As the deer pants for the water brooks, so my soul pants for You, O God.",
    2: "My soul thirsts for God, for the living God. When shall I come and appear before God?",
    3: "My tears have been my food day and night, while they say to me all day long, \"Where is your God?\"",
    4: "These things I remember, and I pour out my soul within me — for I used to go along with the throng and lead them in procession to the house of God, with the voice of joy and thanksgiving, a multitude keeping festival.",
    5: "Why are you in despair, O my soul? And why have you become disturbed within me? Hope in God — for I shall again praise Him for the help of His presence.",
    6: "O my God, my soul is in despair within me — therefore I remember You from the land of the Jordan, and the peaks of Hermon, from Mount Mizar.",
    7: "Deep calls to deep at the sound of Your waterfalls — all Your breakers and Your waves have rolled over me.",
    8: "The LORD will command His lovingkindness in the daytime — and His song will be with me in the night, a prayer to the God of my life.",
    9: "I will say to God my rock, \"Why have You forgotten me? Why do I go mourning because of the oppression of the enemy?\"",
    10: "As a shattering of my bones, my adversaries revile me — while they say to me all day long, \"Where is your God?\"",
    11: "Why are you in despair, O my soul? And why have you become disturbed within me? Hope in God — for I shall yet praise Him, the help of my countenance, and my God.",
}

# Psalm 43 — Vindicate me, O God (continuation of Ps 42)
ps_43 = {
    1: "Vindicate me, O God, and plead my case against an ungodly nation — deliver me from the deceitful and unjust man!",
    2: "For You are the God of my strength — why have You rejected me? Why do I go mourning because of the oppression of the enemy?",
    3: "O send out Your light and Your truth — let them lead me. Let them bring me to Your holy hill, and to Your dwelling places.",
    4: "Then I will go to the altar of God, to God my exceeding joy — and upon the lyre I shall praise You, O God, my God.",
    5: "Why are you in despair, O my soul? And why are you disturbed within me? Hope in God — for I shall again praise Him, the help of my countenance, and my God.",
}

# Psalm 46 — God is our refuge
ps_46 = {
    1: "For the choir director. A Psalm of the sons of Korah, set to Alamoth. A Song. God is our refuge and strength — a very present help in trouble.",
    2: "Therefore we will not fear, though the earth should change, and though the mountains slip into the heart of the sea —",
    3: "though its waters roar and foam, though the mountains quake at its swelling pride.",
    4: "There is a river whose streams make glad the city of God — the holy dwelling places of the Most High.",
    5: "God is in the midst of her — she will not be moved. God will help her when morning dawns.",
    6: "The nations made an uproar — the kingdoms tottered. He raised His voice — the earth melted.",
    7: "The LORD of hosts is with us — the God of Jacob is our stronghold.",
    8: "Come, behold the works of the LORD, who has wrought desolations in the earth.",
    9: "He makes wars to cease to the end of the earth — He breaks the bow and cuts the spear in two. He burns the chariots with fire.",
    10: "Cease striving, and know that I am God. I will be exalted among the nations. I will be exalted in the earth.",
    11: "The LORD of hosts is with us — the God of Jacob is our stronghold.",
}

# Psalm 63 — O God, You are my God
ps_63 = {
    1: "A Psalm of David, when he was in the wilderness of Judah. O God, You are my God. I shall seek You earnestly — my soul thirsts for You, my flesh yearns for You, in a dry and weary land where there is no water.",
    2: "Thus I have beheld You in the sanctuary — to see Your power and Your glory.",
    3: "Because Your lovingkindness is better than life, my lips will praise You.",
    4: "So I will bless You as long as I live — I will lift up my hands in Your name.",
    5: "My soul is satisfied as with marrow and fatness, and my mouth offers praises with joyful lips.",
    6: "When I remember You on my bed, I meditate on You in the night watches.",
    7: "For You have been my help — and in the shadow of Your wings I sing for joy.",
    8: "My soul clings to You — Your right hand upholds me.",
    9: "But those who seek my life, to destroy it, will go into the depths of the earth.",
    10: "They will be delivered over to the power of the sword — they will be a prey for foxes.",
    11: "But the king will rejoice in God — everyone who swears by Him will glory. For the mouths of those who speak lies will be stopped.",
}

# Psalm 84 — How lovely are Your dwelling places
ps_84 = {
    1: "For the choir director. On the Gittith. A Psalm of the sons of Korah. How lovely are Your dwelling places, O LORD of hosts!",
    2: "My soul longed and even yearned for the courts of the LORD — my heart and my flesh sing for joy to the living God.",
    3: "The bird also has found a house, and the swallow a nest for herself, where she may lay her young — even Your altars, O LORD of hosts, my King and my God.",
    4: "How blessed are those who dwell in Your house! They are ever praising You.",
    5: "How blessed is the man whose strength is in You — in whose heart are the highways to Zion!",
    6: "Passing through the valley of Baca, they make it a spring — the early rain also covers it with blessings.",
    7: "They go from strength to strength — every one of them appears before God in Zion.",
    8: "O LORD God of hosts, hear my prayer — give ear, O God of Jacob!",
    9: "Behold our shield, O God — and look upon the face of Your anointed.",
    10: "For a day in Your courts is better than a thousand outside. I would rather stand at the threshold of the house of my God, than dwell in the tents of wickedness.",
    11: "For the LORD God is a sun and shield — the LORD gives grace and glory. No good thing does He withhold from those who walk uprightly.",
    12: "O LORD of hosts — how blessed is the man who trusts in You!",
}

# Psalm 90 — Lord, You have been our dwelling place
ps_90 = {
    1: "A Prayer of Moses, the man of God. Lord, You have been our dwelling place in all generations.",
    2: "Before the mountains were born, or You gave birth to the earth and the world — even from everlasting to everlasting, You are God.",
    3: "You turn man back into dust, and say, \"Return, O children of men.\"",
    4: "For a thousand years in Your sight are like yesterday when it passes by — or as a watch in the night.",
    5: "You have swept them away like a flood. They fall asleep — in the morning they are like grass which sprouts anew.",
    6: "In the morning it flourishes, and sprouts anew — toward evening it fades, and withers away.",
    7: "For we have been consumed by Your anger — and by Your wrath we have been dismayed.",
    8: "You have placed our iniquities before You — our secret sins in the light of Your presence.",
    9: "For all our days have declined in Your fury — we have finished our years like a sigh.",
    10: "As for the days of our life, they contain seventy years — or if due to strength, eighty years. Yet their pride is but labor and sorrow — for soon it is gone, and we fly away.",
    11: "Who understands the power of Your anger? And Your fury, according to the fear that is due You?",
    12: "So teach us to number our days, that we may present to You a heart of wisdom.",
    13: "Do return, O LORD — how long will it be? And be sorry for Your servants.",
    14: "O satisfy us in the morning with Your lovingkindness — that we may sing for joy and be glad all our days.",
    15: "Make us glad according to the days You have afflicted us, and the years we have seen evil.",
    16: "Let Your work appear to Your servants — and Your majesty to their children.",
    17: "And let the favor of the Lord our God be upon us — and confirm for us the work of our hands. Yes, confirm the work of our hands.",
}

# Psalm 103 — Bless the LORD, O my soul
ps_103 = {
    1: "A Psalm of David. Bless the LORD, O my soul — and all that is within me, bless His holy name.",
    2: "Bless the LORD, O my soul — and forget none of His benefits.",
    3: "Who pardons all your iniquities — who heals all your diseases.",
    4: "Who redeems your life from the pit — who crowns you with lovingkindness and compassion.",
    5: "Who satisfies your years with good things — so that your youth is renewed like the eagle.",
    6: "The LORD performs righteous deeds, and judgments for all who are oppressed.",
    7: "He made known His ways to Moses — His acts to the sons of Israel.",
    8: "The LORD is compassionate and gracious — slow to anger and abounding in lovingkindness.",
    9: "He will not always strive with us — nor will He keep His anger forever.",
    10: "He has not dealt with us according to our sins — nor rewarded us according to our iniquities.",
    11: "For as high as the heavens are above the earth, so great is His lovingkindness toward those who fear Him.",
    12: "As far as the east is from the west, so far has He removed our transgressions from us.",
    13: "Just as a father has compassion on his children — so the LORD has compassion on those who fear Him.",
    14: "For He Himself knows our frame — He is mindful that we are but dust.",
    15: "As for man, his days are like grass — as a flower of the field, so he flourishes.",
    16: "When the wind has passed over it, it is no more — and its place acknowledges it no longer.",
    17: "But the lovingkindness of the LORD is from everlasting to everlasting on those who fear Him — and His righteousness to children's children,",
    18: "to those who keep His covenant — and remember His precepts to do them.",
    19: "The LORD has established His throne in the heavens — and His sovereignty rules over all.",
    20: "Bless the LORD, you His angels, mighty in strength, who perform His word, obeying the voice of His word!",
    21: "Bless the LORD, all you His hosts, you who serve Him, doing His will.",
    22: "Bless the LORD, all you works of His, in all places of His dominion. Bless the LORD, O my soul!",
}

# Psalm 107 — Oh give thanks to the LORD, for He is good
ps_107 = {
    1: "Oh give thanks to the LORD, for He is good — for His lovingkindness is everlasting.",
    2: "Let the redeemed of the LORD say so, whom He has redeemed from the hand of the adversary —",
    3: "and gathered from the lands, from the east and from the west, from the north and from the south.",
    4: "They wandered in the wilderness in a desert region — they did not find a way to an inhabited city.",
    5: "They were hungry and thirsty — their soul fainted within them.",
    6: "Then they cried out to the LORD in their trouble — He delivered them out of their distresses.",
    7: "And He led them also by a straight way, to go to an inhabited city.",
    8: "Let them give thanks to the LORD for His lovingkindness — and for His wonders to the sons of men!",
    9: "For He has satisfied the thirsty soul — and the hungry soul He has filled with what is good.",
    10: "There were those who dwelt in darkness and in the shadow of death, prisoners in misery and chains,",
    11: "because they had rebelled against the words of God — and spurned the counsel of the Most High.",
    12: "Therefore He humbled their heart with labor — they stumbled, and there was none to help.",
    13: "Then they cried out to the LORD in their trouble — He saved them out of their distresses.",
    14: "He brought them out of darkness and the shadow of death — and broke their bands apart.",
    15: "Let them give thanks to the LORD for His lovingkindness — and for His wonders to the sons of men!",
    16: "For He has shattered gates of bronze — and cut bars of iron asunder.",
    17: "Fools, because of their rebellious way, and because of their iniquities, were afflicted.",
    18: "Their soul abhorred all kinds of food — and they drew near to the gates of death.",
    19: "Then they cried out to the LORD in their trouble — He saved them out of their distresses.",
    20: "He sent His word and healed them — and delivered them from their destructions.",
    21: "Let them give thanks to the LORD for His lovingkindness — and for His wonders to the sons of men!",
    22: "Let them also offer sacrifices of thanksgiving — and tell of His works with joyful singing.",
    23: "Those who go down to the sea in ships, who do business on great waters —",
    24: "they have seen the works of the LORD, and His wonders in the deep.",
    25: "For He spoke and raised up a stormy wind — which lifted up the waves of the sea.",
    26: "They rose up to the heavens, they went down to the depths — their soul melted away in their misery.",
    27: "They reeled and staggered like a drunken man — and were at their wits' end.",
    28: "Then they cried to the LORD in their trouble — and He brought them out of their distresses.",
    29: "He caused the storm to be still — so that the waves of the sea were hushed.",
    30: "Then they were glad because they were quiet — so He guided them to their desired haven.",
    31: "Let them give thanks to the LORD for His lovingkindness — and for His wonders to the sons of men!",
    32: "Let them extol Him also in the congregation of the people — and praise Him at the seat of the elders.",
    33: "He changes rivers into a wilderness, and springs of water into a thirsty ground.",
    34: "A fruitful land into a salt waste — because of the wickedness of those who dwell in it.",
    35: "He changes a wilderness into a pool of water — and a dry land into springs of water.",
    36: "And there He makes the hungry to dwell — so that they may establish an inhabited city,",
    37: "and sow fields, and plant vineyards, and gather a fruitful harvest.",
    38: "Also He blesses them and they multiply greatly — and He does not let their cattle decrease.",
    39: "When they are diminished and bowed down through oppression, misery, and sorrow,",
    40: "He pours contempt upon princes — and makes them wander in a pathless waste.",
    41: "But He sets the needy securely on high away from affliction — and makes his families like a flock.",
    42: "The upright see it, and are glad — but all unrighteousness shuts its mouth.",
    43: "Who is wise? Let him give heed to these things — and consider the lovingkindnesses of the LORD.",
}

# Psalm 116 — I love the LORD
ps_116 = {
    1: "I love the LORD, because He hears my voice and my supplications.",
    2: "Because He has inclined His ear to me, therefore I shall call upon Him as long as I live.",
    3: "The cords of death encompassed me, and the terrors of Sheol came upon me — I found distress and sorrow.",
    4: "Then I called upon the name of the LORD — \"O LORD, I beseech You, save my life!\"",
    5: "Gracious is the LORD, and righteous — yes, our God is compassionate.",
    6: "The LORD preserves the simple — I was brought low, and He saved me.",
    7: "Return to your rest, O my soul — for the LORD has dealt bountifully with you.",
    8: "For You have rescued my soul from death — my eyes from tears, my feet from stumbling.",
    9: "I shall walk before the LORD in the land of the living.",
    10: "I believed when I said, \"I am greatly afflicted.\"",
    11: "I said in my alarm, \"All men are liars.\"",
    12: "What shall I render to the LORD for all His benefits toward me?",
    13: "I shall lift up the cup of salvation — and call upon the name of the LORD.",
    14: "I shall pay my vows to the LORD — oh may it be in the presence of all His people.",
    15: "Precious in the sight of the LORD is the death of His godly ones.",
    16: "O LORD, surely I am Your servant. I am Your servant, the son of Your handmaid — You have loosed my bonds.",
    17: "To You I shall offer a sacrifice of thanksgiving — and call upon the name of the LORD.",
    18: "I shall pay my vows to the LORD — oh may it be in the presence of all His people,",
    19: "in the courts of the LORD's house — in the midst of you, O Jerusalem. Praise the LORD!",
}

# Psalm 117 — Praise the LORD, all nations
ps_117 = {
    1: "Praise the LORD, all nations — laud Him, all peoples.",
    2: "For His lovingkindness is great toward us — and the truth of the LORD is everlasting. Praise the LORD!",
}

# Psalm 145 — I will extol You, my God, O King
ps_145 = {
    1: "A Psalm of Praise of David. I will extol You, my God, O King — and I will bless Your name forever and ever.",
    2: "Every day I will bless You — and I will praise Your name forever and ever.",
    3: "Great is the LORD, and highly to be praised — and His greatness is unsearchable.",
    4: "One generation shall praise Your works to another, and shall declare Your mighty acts.",
    5: "On the glorious splendor of Your majesty, and on Your wonderful works, I will meditate.",
    6: "And men shall speak of the power of Your awesome acts — and I will tell of Your greatness.",
    7: "They shall eagerly utter the memory of Your abundant goodness — and shall shout joyfully of Your righteousness.",
    8: "The LORD is gracious and merciful — slow to anger and great in lovingkindness.",
    9: "The LORD is good to all — and His mercies are over all His works.",
    10: "All Your works shall give thanks to You, O LORD — and Your godly ones shall bless You.",
    11: "They shall speak of the glory of Your kingdom — and talk of Your power,",
    12: "to make known to the sons of men Your mighty acts — and the glory of the majesty of Your kingdom.",
    13: "Your kingdom is an everlasting kingdom — and Your dominion endures throughout all generations.",
    14: "The LORD sustains all who fall — and raises up all who are bowed down.",
    15: "The eyes of all look to You — and You give them their food in due time.",
    16: "You open Your hand — and satisfy the desire of every living thing.",
    17: "The LORD is righteous in all His ways — and kind in all His deeds.",
    18: "The LORD is near to all who call upon Him — to all who call upon Him in truth.",
    19: "He will fulfill the desire of those who fear Him — He will also hear their cry and will save them.",
    20: "The LORD keeps all who love Him — but all the wicked, He will destroy.",
    21: "My mouth will speak the praise of the LORD — and all flesh will bless His holy name forever and ever.",
}

# Psalm 150 — Praise the LORD!
ps_150 = {
    1: "Praise the LORD! Praise God in His sanctuary — praise Him in His mighty expanse.",
    2: "Praise Him for His mighty deeds — praise Him according to His excellent greatness.",
    3: "Praise Him with trumpet sound — praise Him with harp and lyre.",
    4: "Praise Him with timbrel and dancing — praise Him with stringed instruments and pipe.",
    5: "Praise Him with loud cymbals — praise Him with resounding cymbals.",
    6: "Let everything that has breath praise the LORD. Praise the LORD!",
}

ENTRIES = {}
for v, t in ps_42.items():   ENTRIES[f"19_42_{v}"] = t
for v, t in ps_43.items():   ENTRIES[f"19_43_{v}"] = t
for v, t in ps_46.items():   ENTRIES[f"19_46_{v}"] = t
for v, t in ps_63.items():   ENTRIES[f"19_63_{v}"] = t
for v, t in ps_84.items():   ENTRIES[f"19_84_{v}"] = t
for v, t in ps_90.items():   ENTRIES[f"19_90_{v}"] = t
for v, t in ps_103.items():  ENTRIES[f"19_103_{v}"] = t
for v, t in ps_107.items():  ENTRIES[f"19_107_{v}"] = t
for v, t in ps_116.items():  ENTRIES[f"19_116_{v}"] = t
for v, t in ps_117.items():  ENTRIES[f"19_117_{v}"] = t
for v, t in ps_145.items():  ENTRIES[f"19_145_{v}"] = t
for v, t in ps_150.items():  ENTRIES[f"19_150_{v}"] = t

def main():
    print(f"Psalms batch 2 verses: {len(ENTRIES)}")
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(ENTRIES)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print("moop-translation.json updated.")

if __name__ == "__main__":
    main()
