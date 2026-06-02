"""MBT generator: Zephaniah (complete book, 3 chapters, 53 verses).

Book ID 36. NKJV-faithful skeleton, modern English flow.
Reverential capitalization for divine pronouns.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The word of the LORD which came to Zephaniah the son of Cushi, the son of Gedaliah, the son of Amariah, the son of Hezekiah, in the days of Josiah the son of Amon, king of Judah.",
    2: "\"I will utterly consume everything from the face of the land,\" says the LORD;",
    3: "\"I will consume man and beast; I will consume the birds of the heavens, the fish of the sea, and the stumbling blocks along with the wicked. I will cut off man from the face of the land,\" says the LORD.",
    4: "\"I will stretch out My hand against Judah, and against all the inhabitants of Jerusalem. I will cut off every trace of Baal from this place, the names of the idolatrous priests with the pagan priests —",
    5: "those who worship the host of heaven on the housetops; those who worship and swear oaths by the LORD, but who also swear by Milcom;",
    6: "those who have turned back from following the LORD, and have not sought the LORD, nor inquired of Him.\"",
    7: "Be silent in the presence of the Lord GOD; for the day of the LORD is at hand, for the LORD has prepared a sacrifice; He has invited His guests.",
    8: "\"And it shall be, in the day of the LORD's sacrifice, that I will punish the princes and the king's children, and all such as are clothed with foreign apparel.",
    9: "In the same day I will punish all those who leap over the threshold, who fill their masters' houses with violence and deceit.",
    10: "\"And there shall be on that day,\" says the LORD, \"the sound of a mournful cry from the Fish Gate, a wailing from the Second Quarter, and a loud crashing from the hills.",
    11: "Wail, you inhabitants of Maktesh! For all the merchant people are cut down; all those who handle money are cut off.",
    12: "\"And it shall come to pass at that time that I will search Jerusalem with lamps, and punish the men who are settled in complacency, who say in their heart, 'The LORD will not do good, nor will He do evil.'",
    13: "Therefore their goods shall become booty, and their houses a desolation; they shall build houses, but not inhabit them; they shall plant vineyards, but not drink their wine.\"",
    14: "The great day of the LORD is near; it is near and hastens quickly. The noise of the day of the LORD is bitter; there the mighty men shall cry out.",
    15: "That day is a day of wrath, a day of trouble and distress, a day of devastation and desolation, a day of darkness and gloominess, a day of clouds and thick darkness,",
    16: "a day of trumpet and alarm against the fortified cities and against the high towers.",
    17: "\"I will bring distress upon men, and they shall walk like blind men, because they have sinned against the LORD; their blood shall be poured out like dust, and their flesh like refuse.\"",
    18: "Neither their silver nor their gold shall be able to deliver them in the day of the LORD's wrath; but the whole land shall be devoured by the fire of His jealousy, for He will make speedy riddance of all those who dwell in the land.",
}

ch2 = {
    1: "Gather yourselves together, yes, gather together, O undesirable nation,",
    2: "before the decree is issued, or the day passes like chaff, before the LORD's fierce anger comes upon you, before the day of the LORD's anger comes upon you!",
    3: "Seek the LORD, all you meek of the earth, who have upheld His justice. Seek righteousness, seek humility. It may be that you will be hidden in the day of the LORD's anger.",
    4: "For Gaza shall be forsaken, and Ashkelon desolate; they shall drive out Ashdod at noonday, and Ekron shall be uprooted.",
    5: "Woe to the inhabitants of the seacoast, the nation of the Cherethites! The word of the LORD is against you, O Canaan, land of the Philistines: \"I will destroy you, so there shall be no inhabitant.\"",
    6: "The seacoast shall be pastures, with shelters for shepherds and folds for flocks.",
    7: "The coast shall be for the remnant of the house of Judah; they shall feed their flocks there; in the houses of Ashkelon they shall lie down at evening. For the LORD their God will intervene for them, and return their captives.",
    8: "\"I have heard the reproach of Moab, and the insults of the people of Ammon, with which they have reproached My people, and made arrogant threats against their borders.",
    9: "Therefore, as I live,\" says the LORD of hosts, the God of Israel, \"surely Moab shall be like Sodom, and the people of Ammon like Gomorrah — overrun with weeds and saltpits, and a perpetual desolation. The residue of My people shall plunder them, and the remnant of My people shall possess them.\"",
    10: "This they shall have for their pride, because they have reproached and made arrogant threats against the people of the LORD of hosts.",
    11: "The LORD will be awesome to them, for He will reduce to nothing all the gods of the earth; people shall worship Him, each one from his place, indeed all the shores of the nations.",
    12: "\"You Ethiopians also, you shall be slain by My sword.\"",
    13: "And He will stretch out His hand against the north, destroy Assyria, and make Nineveh a desolation, as dry as the wilderness.",
    14: "The herds shall lie down in her midst, every beast of the nation. Both the pelican and the bittern shall lodge on the capitals of her pillars; their voice shall sing in the windows; desolation shall be at the threshold; for He will lay bare the cedar work.",
    15: "This is the rejoicing city that dwelt securely, that said in her heart, \"I am it, and there is none besides me.\" How has she become a desolation, a place for beasts to lie down! Everyone who passes by her shall hiss and shake his fist.",
}

ch3 = {
    1: "Woe to her who is rebellious and polluted, to the oppressing city!",
    2: "She has not obeyed His voice, she has not received correction; she has not trusted in the LORD, she has not drawn near to her God.",
    3: "Her princes in her midst are roaring lions; her judges are evening wolves that leave not a bone till morning.",
    4: "Her prophets are insolent, treacherous people; her priests have polluted the sanctuary, they have done violence to the law.",
    5: "The LORD is righteous in her midst, He will do no unrighteousness. Every morning He brings His justice to light; He never fails, but the unjust knows no shame.",
    6: "\"I have cut off nations, their fortresses are devastated; I have made their streets desolate, with none passing by. Their cities are destroyed; there is no one, no inhabitant.",
    7: "I said, 'Surely you will fear Me, you will receive instruction' — so that her dwelling would not be cut off, despite everything for which I punished her. But they rose early and corrupted all their deeds.",
    8: "\"Therefore wait for Me,\" says the LORD, \"until the day I rise up for plunder; My determination is to gather the nations to My assembly of kingdoms, to pour on them My indignation, all My fierce anger; all the earth shall be devoured with the fire of My jealousy.",
    9: "\"For then I will restore to the peoples a pure language, that they all may call on the name of the LORD, to serve Him with one accord.",
    10: "From beyond the rivers of Ethiopia My worshipers, the daughter of My dispersed ones, shall bring My offering.",
    11: "In that day you shall not be shamed for any of your deeds in which you transgress against Me; for then I will take away from your midst those who rejoice in your pride, and you shall no longer be haughty in My holy mountain.",
    12: "I will leave in your midst a meek and humble people, and they shall trust in the name of the LORD.",
    13: "The remnant of Israel shall do no unrighteousness and speak no lies, nor shall a deceitful tongue be found in their mouth; for they shall feed their flocks and lie down, and no one shall make them afraid.\"",
    14: "Sing, O daughter of Zion! Shout, O Israel! Be glad and rejoice with all your heart, O daughter of Jerusalem!",
    15: "The LORD has taken away your judgments, He has cast out your enemy. The King of Israel, the LORD, is in your midst; you shall see disaster no more.",
    16: "In that day it shall be said to Jerusalem: \"Do not fear; Zion, let not your hands be weak.",
    17: "The LORD your God in your midst, the Mighty One, will save; He will rejoice over you with gladness, He will quiet you with His love, He will rejoice over you with singing.\"",
    18: "\"I will gather those who sorrow over the appointed assembly, who are among you, to whom its reproach is a burden.",
    19: "Behold, at that time I will deal with all who afflict you; I will save the lame, and gather those who were driven out; I will appoint them for praise and fame in every land where they were put to shame.",
    20: "At that time I will bring you back, even at the time I gather you; for I will give you fame and praise among all the peoples of the earth, when I return your captives before your eyes,\" says the LORD.",
}

CHAPTERS = {1: ch1, 2: ch2, 3: ch3}


def main():
    data = json.loads(MOOP_PATH.read_text())
    new_entries = {}
    for ch, verses in CHAPTERS.items():
        for v, text in verses.items():
            new_entries[f"36_{ch}_{v}"] = text
    data.update(new_entries)
    MOOP_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Zephaniah verses authored: {len(new_entries)}")
    print("moop-translation.json updated.")


if __name__ == "__main__":
    main()
