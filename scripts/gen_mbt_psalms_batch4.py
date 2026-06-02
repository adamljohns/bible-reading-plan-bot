"""MBT generator: Psalms batch 4 — more beloved psalms.

Book ID 19. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.

Psalms authored:
- Psalm 2 (12v) — the royal Messianic psalm; "kiss the Son"
- Psalm 24 (10v) — "lift up your heads, O you gates"
- Psalm 40 (17v) — "He brought me up out of the horrible pit"
- Psalm 47 (9v) — "Clap your hands, all you peoples!"
- Psalm 67 (7v) — "let the peoples praise You"
- Psalm 95 (11v) — "come, let us sing to the LORD"
- Psalm 96 (13v) — "Sing to the LORD a new song"
- Psalm 98 (9v) — "the LORD has done marvelous things"
- Psalm 110 (7v) — "the LORD said to my Lord, 'Sit at My right hand'"
- Psalm 118 (29v) — "the stone the builders rejected has become the chief cornerstone"
- Psalm 130 (8v) — "out of the depths I have cried to You, O LORD"
- Psalm 133 (3v) — "how good and how pleasant it is for brethren to dwell together in unity"
- Psalm 137 (9v) — "by the rivers of Babylon, there we sat down and wept"

Total: 144 verses
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ps2 = {
    1: "Why do the nations rage, and the people plot a vain thing?",
    2: "The kings of the earth set themselves, and the rulers take counsel together, against the LORD and against His Anointed, saying,",
    3: "\"Let us break Their bonds in pieces and cast away Their cords from us.\"",
    4: "He who sits in the heavens shall laugh; the Lord shall hold them in derision.",
    5: "Then He shall speak to them in His wrath, and distress them in His deep displeasure:",
    6: "\"Yet I have set My King on My holy hill of Zion.\"",
    7: "\"I will declare the decree: the LORD has said to Me, 'You are My Son, today I have begotten You.",
    8: "Ask of Me, and I will give You the nations for Your inheritance, and the ends of the earth for Your possession.",
    9: "You shall break them with a rod of iron; You shall dash them to pieces like a potter's vessel.'\"",
    10: "Now therefore, be wise, O kings; be instructed, you judges of the earth.",
    11: "Serve the LORD with fear, and rejoice with trembling.",
    12: "Kiss the Son, lest He be angry, and you perish in the way, when His wrath is kindled but a little. Blessed are all those who put their trust in Him.",
}

ps24 = {
    1: "The earth is the LORD's, and all its fullness, the world and those who dwell in it.",
    2: "For He has founded it upon the seas, and established it upon the waters.",
    3: "Who may ascend into the hill of the LORD? Or who may stand in His holy place?",
    4: "He who has clean hands and a pure heart, who has not lifted up his soul to an idol, nor sworn deceitfully.",
    5: "He shall receive blessing from the LORD, and righteousness from the God of his salvation.",
    6: "This is Jacob, the generation of those who seek Him, who seek Your face. Selah",
    7: "Lift up your heads, O you gates! And be lifted up, you everlasting doors! And the King of glory shall come in.",
    8: "Who is this King of glory? The LORD strong and mighty, the LORD mighty in battle.",
    9: "Lift up your heads, O you gates! Lift up, you everlasting doors! And the King of glory shall come in.",
    10: "Who is this King of glory? The LORD of hosts, He is the King of glory. Selah",
}

ps40 = {
    1: "I waited patiently for the LORD; and He inclined to me, and heard my cry.",
    2: "He also brought me up out of a horrible pit, out of the miry clay, and set my feet upon a rock, and established my steps.",
    3: "He has put a new song in my mouth — praise to our God; many will see it and fear, and will trust in the LORD.",
    4: "Blessed is that man who makes the LORD his trust, and does not respect the proud, nor such as turn aside to lies.",
    5: "Many, O LORD my God, are Your wonderful works which You have done; and Your thoughts toward us cannot be recounted to You in order; if I would declare and speak of them, they are more than can be numbered.",
    6: "Sacrifice and offering You did not desire; My ears You have opened. Burnt offering and sin offering You did not require.",
    7: "Then I said, \"Behold, I come; in the scroll of the book it is written of Me.",
    8: "I delight to do Your will, O My God, and Your law is within My heart.\"",
    9: "I have proclaimed the good news of righteousness in the great assembly; indeed, I do not restrain my lips, O LORD, You Yourself know.",
    10: "I have not hidden Your righteousness within my heart; I have declared Your faithfulness and Your salvation; I have not concealed Your lovingkindness and Your truth from the great assembly.",
    11: "Do not withhold Your tender mercies from me, O LORD; let Your lovingkindness and Your truth continually preserve me.",
    12: "For innumerable evils have surrounded me; my iniquities have overtaken me, so that I am not able to look up; they are more than the hairs of my head; therefore my heart fails me.",
    13: "Be pleased, O LORD, to deliver me; O LORD, make haste to help me!",
    14: "Let them be ashamed and brought to mutual confusion who seek to destroy my life; let them be driven backward and brought to dishonor who wish me evil.",
    15: "Let them be confounded because of their shame, who say to me, \"Aha, aha!\"",
    16: "Let all those who seek You rejoice and be glad in You; let such as love Your salvation say continually, \"The LORD be magnified!\"",
    17: "But I am poor and needy; yet the LORD thinks upon me. You are my help and my deliverer; do not delay, O my God.",
}

ps47 = {
    1: "Oh, clap your hands, all you peoples! Shout to God with the voice of triumph!",
    2: "For the LORD Most High is awesome; He is a great King over all the earth.",
    3: "He will subdue the peoples under us, and the nations under our feet.",
    4: "He will choose our inheritance for us, the excellence of Jacob whom He loves. Selah",
    5: "God has gone up with a shout, the LORD with the sound of a trumpet.",
    6: "Sing praises to God, sing praises! Sing praises to our King, sing praises!",
    7: "For God is the King of all the earth; sing praises with understanding.",
    8: "God reigns over the nations; God sits on His holy throne.",
    9: "The princes of the people have gathered together, the people of the God of Abraham. For the shields of the earth belong to God; He is greatly exalted.",
}

ps67 = {
    1: "God be merciful to us and bless us, and cause His face to shine upon us, Selah",
    2: "that Your way may be known on earth, Your salvation among all nations.",
    3: "Let the peoples praise You, O God; let all the peoples praise You.",
    4: "Oh, let the nations be glad and sing for joy! For You shall judge the people righteously, and govern the nations on earth. Selah",
    5: "Let the peoples praise You, O God; let all the peoples praise You.",
    6: "Then the earth shall yield her increase; God, our own God, shall bless us.",
    7: "God shall bless us, and all the ends of the earth shall fear Him.",
}

ps95 = {
    1: "Oh come, let us sing to the LORD! Let us shout joyfully to the Rock of our salvation.",
    2: "Let us come before His presence with thanksgiving; let us shout joyfully to Him with psalms.",
    3: "For the LORD is the great God, and the great King above all gods.",
    4: "In His hand are the deep places of the earth; the heights of the hills are His also.",
    5: "The sea is His, for He made it; and His hands formed the dry land.",
    6: "Oh come, let us worship and bow down; let us kneel before the LORD our Maker.",
    7: "For He is our God, and we are the people of His pasture, and the sheep of His hand. Today, if you will hear His voice:",
    8: "\"Do not harden your hearts, as in the rebellion, as in the day of trial in the wilderness,",
    9: "when your fathers tested Me; they tried Me, though they saw My work.",
    10: "For forty years I was grieved with that generation, and said, 'It is a people who go astray in their hearts, and they do not know My ways.'",
    11: "So I swore in My wrath, 'They shall not enter My rest.'\"",
}

ps96 = {
    1: "Oh, sing to the LORD a new song! Sing to the LORD, all the earth.",
    2: "Sing to the LORD, bless His name; proclaim the good news of His salvation from day to day.",
    3: "Declare His glory among the nations, His wonders among all peoples.",
    4: "For the LORD is great and greatly to be praised; He is to be feared above all gods.",
    5: "For all the gods of the peoples are idols, but the LORD made the heavens.",
    6: "Honor and majesty are before Him; strength and beauty are in His sanctuary.",
    7: "Give to the LORD, O families of the peoples, give to the LORD glory and strength.",
    8: "Give to the LORD the glory due His name; bring an offering, and come into His courts.",
    9: "Oh, worship the LORD in the beauty of holiness! Tremble before Him, all the earth.",
    10: "Say among the nations, \"The LORD reigns; the world also is firmly established, it shall not be moved; He shall judge the peoples righteously.\"",
    11: "Let the heavens rejoice, and let the earth be glad; let the sea roar, and all its fullness;",
    12: "let the field be joyful, and all that is in it. Then all the trees of the woods will rejoice before the LORD.",
    13: "For He is coming, for He is coming to judge the earth. He shall judge the world with righteousness, and the peoples with His truth.",
}

ps98 = {
    1: "Oh, sing to the LORD a new song! For He has done marvelous things; His right hand and His holy arm have gained Him the victory.",
    2: "The LORD has made known His salvation; His righteousness He has revealed in the sight of the nations.",
    3: "He has remembered His mercy and His faithfulness to the house of Israel; all the ends of the earth have seen the salvation of our God.",
    4: "Shout joyfully to the LORD, all the earth; break forth in song, rejoice, and sing praises.",
    5: "Sing to the LORD with the harp, with the harp and the sound of a psalm,",
    6: "with trumpets and the sound of a horn; shout joyfully before the LORD, the King.",
    7: "Let the sea roar, and all its fullness, the world and those who dwell in it;",
    8: "let the rivers clap their hands; let the hills be joyful together",
    9: "before the LORD, for He is coming to judge the earth. With righteousness He shall judge the world, and the peoples with equity.",
}

ps110 = {
    1: "The LORD said to my Lord, \"Sit at My right hand, till I make Your enemies Your footstool.\"",
    2: "The LORD shall send the rod of Your strength out of Zion. Rule in the midst of Your enemies!",
    3: "Your people shall be volunteers in the day of Your power; in the beauties of holiness, from the womb of the morning, You have the dew of Your youth.",
    4: "The LORD has sworn and will not relent, \"You are a priest forever according to the order of Melchizedek.\"",
    5: "The Lord is at Your right hand; He shall execute kings in the day of His wrath.",
    6: "He shall judge among the nations, He shall fill the places with dead bodies, He shall execute the heads of many countries.",
    7: "He shall drink of the brook by the wayside; therefore He shall lift up the head.",
}

ps118 = {
    1: "Oh, give thanks to the LORD, for He is good! For His mercy endures forever.",
    2: "Let Israel now say, \"His mercy endures forever.\"",
    3: "Let the house of Aaron now say, \"His mercy endures forever.\"",
    4: "Let those who fear the LORD now say, \"His mercy endures forever.\"",
    5: "I called on the LORD in distress; the LORD answered me and set me in a broad place.",
    6: "The LORD is on my side; I will not fear. What can man do to me?",
    7: "The LORD is for me among those who help me; therefore I shall see my desire on those who hate me.",
    8: "It is better to trust in the LORD than to put confidence in man.",
    9: "It is better to trust in the LORD than to put confidence in princes.",
    10: "All nations surrounded me, but in the name of the LORD I will destroy them.",
    11: "They surrounded me, yes, they surrounded me; but in the name of the LORD I will destroy them.",
    12: "They surrounded me like bees; they were quenched like a fire of thorns; for in the name of the LORD I will destroy them.",
    13: "You pushed me violently, that I might fall, but the LORD helped me.",
    14: "The LORD is my strength and song, and He has become my salvation.",
    15: "The voice of rejoicing and salvation is in the tents of the righteous; the right hand of the LORD does valiantly.",
    16: "The right hand of the LORD is exalted; the right hand of the LORD does valiantly.",
    17: "I shall not die, but live, and declare the works of the LORD.",
    18: "The LORD has chastened me severely, but He has not given me over to death.",
    19: "Open to me the gates of righteousness; I will go through them, and I will praise the LORD.",
    20: "This is the gate of the LORD, through which the righteous shall enter.",
    21: "I will praise You, for You have answered me, and have become my salvation.",
    22: "The stone which the builders rejected has become the chief cornerstone.",
    23: "This was the LORD's doing; it is marvelous in our eyes.",
    24: "This is the day the LORD has made; we will rejoice and be glad in it.",
    25: "Save now, I pray, O LORD; O LORD, I pray, send now prosperity.",
    26: "Blessed is he who comes in the name of the LORD! We have blessed you from the house of the LORD.",
    27: "God is the LORD, and He has given us light; bind the sacrifice with cords to the horns of the altar.",
    28: "You are my God, and I will praise You; You are my God, I will exalt You.",
    29: "Oh, give thanks to the LORD, for He is good! For His mercy endures forever.",
}

ps130 = {
    1: "Out of the depths I have cried to You, O LORD;",
    2: "Lord, hear my voice! Let Your ears be attentive to the voice of my supplications.",
    3: "If You, LORD, should mark iniquities, O Lord, who could stand?",
    4: "But there is forgiveness with You, that You may be feared.",
    5: "I wait for the LORD, my soul waits, and in His word I do hope.",
    6: "My soul waits for the Lord more than those who watch for the morning — yes, more than those who watch for the morning.",
    7: "O Israel, hope in the LORD; for with the LORD there is mercy, and with Him is abundant redemption.",
    8: "And He shall redeem Israel from all his iniquities.",
}

ps133 = {
    1: "Behold, how good and how pleasant it is for brethren to dwell together in unity!",
    2: "It is like the precious oil upon the head, running down on the beard, the beard of Aaron, running down on the edge of his garments.",
    3: "It is like the dew of Hermon, descending upon the mountains of Zion; for there the LORD commanded the blessing — life forevermore.",
}

ps137 = {
    1: "By the rivers of Babylon, there we sat down, yea, we wept when we remembered Zion.",
    2: "We hung our harps upon the willows in the midst of it.",
    3: "For there those who carried us away captive asked of us a song, and those who plundered us requested mirth, saying, \"Sing us one of the songs of Zion!\"",
    4: "How shall we sing the LORD's song in a foreign land?",
    5: "If I forget you, O Jerusalem, let my right hand forget its skill!",
    6: "If I do not remember you, let my tongue cling to the roof of my mouth — if I do not exalt Jerusalem above my chief joy.",
    7: "Remember, O LORD, against the sons of Edom the day of Jerusalem, who said, \"Raze it, raze it, to its very foundation!\"",
    8: "O daughter of Babylon, who are to be destroyed, happy the one who repays you as you have served us!",
    9: "Happy the one who takes and dashes your little ones against the rock!",
}

ENTRIES = {}
for psnum, psdict in [
    (2, ps2), (24, ps24), (40, ps40), (47, ps47), (67, ps67),
    (95, ps95), (96, ps96), (98, ps98), (110, ps110), (118, ps118),
    (130, ps130), (133, ps133), (137, ps137),
]:
    for v, t in psdict.items():
        ENTRIES[f"19_{psnum}_{v}"] = t


def main():
    data = json.loads(MOOP_PATH.read_text())
    data.update(ENTRIES)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Psalms batch 4 verses authored: {len(ENTRIES)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
