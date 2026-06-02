"""Expand pericope-map.json to cover key OT books.

Adds Genesis, Exodus, Proverbs, Isaiah, Daniel, and major Psalms
(those long enough to benefit from internal section breaks).
Most psalms are 1-section poems and don't need explicit mapping
since the fallback heuristic handles them gracefully.

Anchored on NKJV + ESV section-header consensus.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "assets" / "pericope-map.json"

def S(start, end, title):
    return {"start": start, "end": end, "title": title}

# Book 1: Genesis (50 chapters)
GENESIS = {
    1:  [S(1,2,"In the Beginning"), S(3,5,"Day One: Light"), S(6,8,"Day Two: Sky"), S(9,13,"Day Three: Land and Seas"), S(14,19,"Day Four: Sun, Moon, Stars"), S(20,23,"Day Five: Sea Creatures and Birds"), S(24,31,"Day Six: Land Animals and Man")],
    2:  [S(1,3,"The Seventh Day"), S(4,17,"Garden of Eden"), S(18,25,"Woman Created")],
    3:  [S(1,7,"The Fall"), S(8,13,"God Confronts"), S(14,19,"The Curses"), S(20,24,"Exiled from Eden")],
    4:  [S(1,16,"Cain and Abel"), S(17,24,"Cain's Descendants"), S(25,26,"Seth and Enosh")],
    5:  [S(1,32,"From Adam to Noah")],
    6:  [S(1,8,"The Wickedness of Man"), S(9,22,"Noah Commanded to Build")],
    7:  [S(1,24,"The Flood Begins")],
    8:  [S(1,19,"The Waters Recede"), S(20,22,"Noah's Sacrifice")],
    9:  [S(1,17,"Covenant with Noah"), S(18,29,"Noah and His Sons")],
    10: [S(1,32,"The Table of Nations")],
    11: [S(1,9,"The Tower of Babel"), S(10,26,"From Shem to Abram"), S(27,32,"Terah's Family")],
    12: [S(1,9,"The Call of Abram"), S(10,20,"Abram in Egypt")],
    13: [S(1,18,"Abram and Lot Separate")],
    14: [S(1,16,"Abram Rescues Lot"), S(17,24,"Melchizedek Blesses Abram")],
    15: [S(1,21,"God's Covenant with Abram")],
    16: [S(1,16,"Hagar and Ishmael")],
    17: [S(1,27,"The Covenant of Circumcision")],
    18: [S(1,15,"The Three Visitors"), S(16,33,"Abraham Pleads for Sodom")],
    19: [S(1,29,"The Destruction of Sodom"), S(30,38,"Lot and His Daughters")],
    20: [S(1,18,"Abraham and Abimelech")],
    21: [S(1,7,"The Birth of Isaac"), S(8,21,"Hagar and Ishmael Sent Away"), S(22,34,"Covenant at Beersheba")],
    22: [S(1,19,"The Sacrifice of Isaac"), S(20,24,"Nahor's Family")],
    23: [S(1,20,"The Death and Burial of Sarah")],
    24: [S(1,67,"A Bride for Isaac")],
    25: [S(1,18,"Abraham's Other Children + Ishmael's Line"), S(19,34,"Esau Sells His Birthright")],
    26: [S(1,33,"Isaac and Abimelech"), S(34,35,"Esau's Hittite Wives")],
    27: [S(1,40,"Jacob Steals the Blessing"), S(41,46,"Esau's Anger; Jacob Sent Away")],
    28: [S(1,9,"Isaac Sends Jacob to Laban"), S(10,22,"Jacob's Ladder at Bethel")],
    29: [S(1,30,"Jacob Marries Leah and Rachel"), S(31,35,"Leah's Sons")],
    30: [S(1,24,"Jacob's Children"), S(25,43,"Jacob Prospers")],
    31: [S(1,55,"Jacob Flees from Laban")],
    32: [S(1,21,"Jacob Prepares to Meet Esau"), S(22,32,"Jacob Wrestles with God")],
    33: [S(1,20,"Jacob Meets Esau")],
    34: [S(1,31,"Dinah and the Shechemites")],
    35: [S(1,15,"Jacob Returns to Bethel"), S(16,29,"Death of Rachel and Isaac")],
    36: [S(1,43,"The Descendants of Esau")],
    37: [S(1,36,"Joseph Sold into Slavery")],
    38: [S(1,30,"Judah and Tamar")],
    39: [S(1,23,"Joseph and Potiphar's Wife")],
    40: [S(1,23,"The Cupbearer and the Baker")],
    41: [S(1,40,"Pharaoh's Dreams Interpreted"), S(41,57,"Joseph Rules Egypt")],
    42: [S(1,38,"Joseph's Brothers Come to Egypt")],
    43: [S(1,34,"The Second Journey to Egypt")],
    44: [S(1,34,"Joseph's Silver Cup")],
    45: [S(1,28,"Joseph Reveals Himself")],
    46: [S(1,27,"Jacob's Family Goes to Egypt"), S(28,34,"Jacob Settles in Goshen")],
    47: [S(1,12,"Jacob Before Pharaoh"), S(13,26,"Joseph's Administration"), S(27,31,"Jacob's Last Days Approach")],
    48: [S(1,22,"Manasseh and Ephraim Blessed")],
    49: [S(1,28,"Jacob Blesses His Sons"), S(29,33,"The Death of Jacob")],
    50: [S(1,14,"The Burial of Jacob"), S(15,21,"Joseph Reassures His Brothers"), S(22,26,"The Death of Joseph")],
}

# Book 2: Exodus (40 chapters)
EXODUS = {
    1:  [S(1,22,"Israel Oppressed in Egypt")],
    2:  [S(1,10,"The Birth of Moses"), S(11,22,"Moses Flees to Midian"), S(23,25,"God Remembers His Covenant")],
    3:  [S(1,12,"The Burning Bush"), S(13,22,"The Divine Name Revealed")],
    4:  [S(1,17,"Signs for Moses"), S(18,31,"Moses Returns to Egypt")],
    5:  [S(1,23,"Pharaoh Increases Israel's Burden")],
    6:  [S(1,13,"God's Renewed Promise"), S(14,30,"The Family Tree of Moses and Aaron")],
    7:  [S(1,13,"Aaron's Staff Becomes a Serpent"), S(14,25,"The Plague of Blood")],
    8:  [S(1,15,"Frogs"), S(16,19,"Gnats"), S(20,32,"Flies")],
    9:  [S(1,7,"Livestock Pestilence"), S(8,12,"Boils"), S(13,35,"Hail")],
    10: [S(1,20,"Locusts"), S(21,29,"Darkness")],
    11: [S(1,10,"The Plague on the Firstborn Foretold")],
    12: [S(1,28,"The Passover Instituted"), S(29,42,"The Exodus"), S(43,51,"Passover Regulations")],
    13: [S(1,16,"Consecration of the Firstborn"), S(17,22,"Pillar of Cloud and Fire")],
    14: [S(1,31,"Crossing the Red Sea")],
    15: [S(1,21,"The Song of Moses and Miriam"), S(22,27,"Bitter Water at Marah")],
    16: [S(1,36,"Manna and Quail in the Wilderness")],
    17: [S(1,7,"Water from the Rock"), S(8,16,"Victory over Amalek")],
    18: [S(1,27,"Jethro Visits Moses")],
    19: [S(1,25,"At Mount Sinai")],
    20: [S(1,17,"The Ten Commandments"), S(18,26,"The People's Fear")],
    21: [S(1,11,"Laws Concerning Servants"), S(12,36,"Laws Concerning Violence")],
    22: [S(1,15,"Laws on Restitution"), S(16,31,"Social and Religious Laws")],
    23: [S(1,9,"Laws of Justice"), S(10,19,"Sabbath and Festivals"), S(20,33,"The Angel of God's Presence")],
    24: [S(1,18,"The Covenant Sealed")],
    25: [S(1,9,"Offerings for the Tabernacle"), S(10,22,"The Ark"), S(23,30,"The Table"), S(31,40,"The Lampstand")],
    26: [S(1,37,"The Tabernacle")],
    27: [S(1,8,"The Altar of Burnt Offering"), S(9,19,"The Courtyard"), S(20,21,"Oil for the Lamp")],
    28: [S(1,43,"Priestly Garments")],
    29: [S(1,46,"Consecration of Priests")],
    30: [S(1,10,"The Altar of Incense"), S(11,16,"The Atonement Money"), S(17,21,"The Bronze Basin"), S(22,38,"Anointing Oil and Incense")],
    31: [S(1,11,"Bezalel and Oholiab"), S(12,18,"The Sabbath")],
    32: [S(1,35,"The Golden Calf")],
    33: [S(1,23,"The Tent of Meeting; Moses Sees God's Glory")],
    34: [S(1,35,"The Covenant Renewed")],
    35: [S(1,35,"Sabbath Regulations + Offerings for the Tabernacle")],
    36: [S(1,38,"Construction of the Tabernacle")],
    37: [S(1,29,"Making the Ark, Table, Lampstand, and Altar of Incense")],
    38: [S(1,31,"The Altar of Burnt Offering and the Court")],
    39: [S(1,43,"The Priestly Garments + Inspection of the Work")],
    40: [S(1,33,"Setting Up the Tabernacle"), S(34,38,"The Glory of the LORD")],
}

# Book 20: Proverbs (31 chapters)
PROVERBS = {
    1:  [S(1,7,"The Beginning of Knowledge"), S(8,19,"Avoid Evil Companions"), S(20,33,"The Call of Wisdom")],
    2:  [S(1,22,"The Value of Wisdom")],
    3:  [S(1,12,"Wisdom Brings Long Life"), S(13,26,"Blessings of Wisdom"), S(27,35,"Doing Good to Others")],
    4:  [S(1,9,"A Father's Wise Instruction"), S(10,19,"The Path of the Righteous"), S(20,27,"Guard Your Heart")],
    5:  [S(1,14,"Warning Against Adultery"), S(15,23,"Drink from Your Own Well")],
    6:  [S(1,19,"Warnings Against Folly"), S(20,35,"Warning Against the Adulteress")],
    7:  [S(1,27,"The Crafty Harlot")],
    8:  [S(1,21,"Wisdom Calls"), S(22,36,"Wisdom Before Creation")],
    9:  [S(1,12,"Wisdom's Feast"), S(13,18,"The Woman of Folly")],
    10: [S(1,32,"Proverbs of Solomon")],
    11: [S(1,31,"Contrast of the Righteous and the Wicked")],
    12: [S(1,28,"The Words of the Wicked and the Righteous")],
    13: [S(1,25,"The Wise Child")],
    14: [S(1,35,"Wisdom Builds the House")],
    15: [S(1,33,"A Soft Answer")],
    16: [S(1,33,"Plans of the Heart")],
    17: [S(1,28,"The Foolish and the Wise")],
    18: [S(1,24,"The Power of the Tongue")],
    19: [S(1,29,"The Poor and the Foolish")],
    20: [S(1,30,"Wine, Strife, and Honor")],
    21: [S(1,31,"The King's Heart")],
    22: [S(1,16,"A Good Name"), S(17,29,"Words of the Wise")],
    23: [S(1,35,"More Sayings of the Wise")],
    24: [S(1,22,"More Sayings of the Wise"), S(23,34,"More Wise Sayings")],
    25: [S(1,28,"More Proverbs of Solomon")],
    26: [S(1,28,"Fools and Sluggards")],
    27: [S(1,27,"Boasting About Tomorrow")],
    28: [S(1,28,"The Bold and the Just")],
    29: [S(1,27,"A Hardened Neck")],
    30: [S(1,33,"The Words of Agur")],
    31: [S(1,9,"The Words of King Lemuel"), S(10,31,"The Excellent Wife")],
}

# Book 23: Isaiah (66 chapters)
ISAIAH = {
    1:  [S(1,9,"Judah's Rebellion"), S(10,20,"Worthless Worship"), S(21,31,"Rebellious Jerusalem")],
    2:  [S(1,5,"The Mountain of the LORD"), S(6,22,"The Day of the LORD")],
    3:  [S(1,15,"Judgment on Judah and Jerusalem"), S(16,26,"The Daughters of Zion")],
    4:  [S(1,6,"The Branch of the LORD Glorified")],
    5:  [S(1,7,"The Song of the Vineyard"), S(8,30,"Woes and Judgments")],
    6:  [S(1,13,"Isaiah's Vision and Call")],
    7:  [S(1,9,"Isaiah Sent to Ahaz"), S(10,25,"The Sign of Immanuel")],
    8:  [S(1,22,"The Coming Assyrian Invasion")],
    9:  [S(1,7,"Unto Us a Child Is Born"), S(8,21,"The LORD's Anger Against Israel")],
    10: [S(1,19,"Woe to Assyria"), S(20,34,"The Remnant of Israel Will Return")],
    11: [S(1,16,"The Reign of Jesse's Offspring")],
    12: [S(1,6,"A Song of Praise")],
    13: [S(1,22,"The Burden Against Babylon")],
    14: [S(1,23,"Israel Restored, Babylon Fallen"), S(24,32,"Judgments on Assyria and Philistia")],
    15: [S(1,9,"The Oracle Against Moab")],
    16: [S(1,14,"More on Moab")],
    17: [S(1,14,"The Oracle Against Damascus")],
    18: [S(1,7,"The Oracle Against Cush")],
    19: [S(1,25,"The Oracle Against Egypt")],
    20: [S(1,6,"A Sign Against Egypt and Cush")],
    21: [S(1,17,"Oracles Against Babylon, Edom, and Arabia")],
    22: [S(1,25,"The Oracle Against Jerusalem")],
    23: [S(1,18,"The Oracle Against Tyre")],
    24: [S(1,23,"Judgment on the Whole Earth")],
    25: [S(1,12,"A Song of Praise")],
    26: [S(1,21,"You Keep Him in Perfect Peace")],
    27: [S(1,13,"The Vineyard of the LORD")],
    28: [S(1,29,"Woe to Drunken Ephraim and Mockers")],
    29: [S(1,24,"Woe to Ariel")],
    30: [S(1,33,"Woe to the Stubborn Nation")],
    31: [S(1,9,"Woe to Those Who Trust in Egypt")],
    32: [S(1,20,"A King Will Reign in Righteousness")],
    33: [S(1,24,"Distress and Help")],
    34: [S(1,17,"Judgment Against the Nations")],
    35: [S(1,10,"The Ransomed Shall Return")],
    36: [S(1,22,"Sennacherib Threatens Jerusalem")],
    37: [S(1,38,"Hezekiah's Prayer; Assyrians Destroyed")],
    38: [S(1,22,"Hezekiah's Illness and Recovery")],
    39: [S(1,8,"Envoys from Babylon")],
    40: [S(1,11,"Comfort for God's People"), S(12,31,"The Greatness of God")],
    41: [S(1,29,"Israel Reassured")],
    42: [S(1,9,"The Servant of the LORD"), S(10,25,"Praise the LORD")],
    43: [S(1,28,"Israel's Only Savior")],
    44: [S(1,8,"Israel the Chosen"), S(9,20,"The Folly of Idolatry"), S(21,28,"Cyrus Foretold")],
    45: [S(1,25,"Cyrus, the LORD's Anointed")],
    46: [S(1,13,"The Idols of Babylon Compared")],
    47: [S(1,15,"The Fall of Babylon")],
    48: [S(1,22,"Israel Refined for God's Glory")],
    49: [S(1,13,"The Servant a Light to the Nations"), S(14,26,"Zion Comforted")],
    50: [S(1,11,"Israel's Sin and the Servant's Obedience")],
    51: [S(1,23,"Comfort for the Exiles")],
    52: [S(1,12,"The Lord Will Rescue Jerusalem"), S(13,15,"The Suffering Servant Introduced")],
    53: [S(1,12,"The Suffering Servant")],
    54: [S(1,17,"The Eternal Covenant of Peace")],
    55: [S(1,13,"The Compassion of the LORD")],
    56: [S(1,12,"Salvation for the Gentiles")],
    57: [S(1,21,"Israel's Idolatry Rebuked")],
    58: [S(1,14,"True Fasting")],
    59: [S(1,21,"Separation from God")],
    60: [S(1,22,"The Future Glory of Zion")],
    61: [S(1,11,"The Year of the LORD's Favor")],
    62: [S(1,12,"Zion's New Name")],
    63: [S(1,19,"God's Vengeance and Mercy")],
    64: [S(1,12,"A Prayer for Deliverance")],
    65: [S(1,25,"Judgment and Salvation"), ],
    66: [S(1,24,"The Final Vindication")],
}

# Book 27: Daniel (12 chapters)
DANIEL = {
    1:  [S(1,21,"Daniel's Faithfulness in Babylon")],
    2:  [S(1,30,"Nebuchadnezzar's Dream"), S(31,49,"Daniel Interprets the Dream")],
    3:  [S(1,18,"The Image of Gold; the Three Refuse"), S(19,30,"The Fiery Furnace")],
    4:  [S(1,37,"Nebuchadnezzar's Humbling")],
    5:  [S(1,31,"The Handwriting on the Wall")],
    6:  [S(1,28,"Daniel in the Lions' Den")],
    7:  [S(1,28,"Vision of the Four Beasts")],
    8:  [S(1,27,"Vision of the Ram and the Goat")],
    9:  [S(1,19,"Daniel's Prayer of Confession"), S(20,27,"The Seventy Weeks")],
    10: [S(1,21,"Daniel's Vision of a Man")],
    11: [S(1,45,"Prophecy of the Kings")],
    12: [S(1,13,"The Time of the End")],
}

# Book 19: Select major Psalms with internal divisions
# Most psalms are single-section poems; we map only those with natural breaks.
PSALMS = {
    18: [S(1,19,"Deliverance from Enemies"), S(20,30,"God Rewards Righteousness"), S(31,50,"The God Who Trains for Battle")],
    19: [S(1,6,"The Heavens Declare"), S(7,11,"The Law of the LORD Is Perfect"), S(12,14,"Cleanse Me")],
    22: [S(1,21,"My God, Why Have You Forsaken Me?"), S(22,31,"All the Earth Will Worship the LORD")],
    27: [S(1,6,"The LORD Is My Light"), S(7,14,"Wait on the LORD")],
    37: [S(1,11,"Do Not Fret Because of Evildoers"), S(12,22,"The LORD Upholds the Righteous"), S(23,40,"The Steps of a Good Man")],
    42: [S(1,11,"My Soul Thirsts for God")],
    51: [S(1,9,"A Prayer for Cleansing"), S(10,19,"A Heart Renewed")],
    73: [S(1,14,"The Prosperity of the Wicked"), S(15,28,"The End of the Wicked")],
    78: [S(1,16,"Lessons from the Past"), S(17,39,"Israel's Rebellion"), S(40,72,"God's Faithful Care")],
    89: [S(1,18,"The LORD's Covenant"), S(19,37,"The Davidic Covenant"), S(38,52,"A Lament Over the Broken Covenant")],
    103: [S(1,5,"Bless the LORD, O My Soul"), S(6,18,"The LORD's Compassion"), S(19,22,"Bless the LORD, All You His Hosts")],
    105: [S(1,15,"Remember His Wonderful Works"), S(16,45,"Israel's History Recounted")],
    106: [S(1,12,"Praise for Past Mercies"), S(13,46,"Israel's Disobedience"), S(47,48,"A Prayer for Deliverance")],
    107: [S(1,9,"The Wanderers"), S(10,16,"The Prisoners"), S(17,22,"The Sick"), S(23,32,"The Sea Travelers"), S(33,43,"The LORD's Reversals")],
    119: [
        S(1,8,"Aleph: Blessed Are the Blameless"),
        S(9,16,"Beth: How Shall a Young Man Cleanse His Way"),
        S(17,24,"Gimel: Open My Eyes"),
        S(25,32,"Daleth: My Soul Clings to the Dust"),
        S(33,40,"He: Teach Me, O LORD"),
        S(41,48,"Vav: Let Your Mercies Come"),
        S(49,56,"Zayin: Remember the Word to Your Servant"),
        S(57,64,"Heth: You Are My Portion"),
        S(65,72,"Teth: You Have Dealt Well"),
        S(73,80,"Yodh: Your Hands Have Made Me"),
        S(81,88,"Kaph: My Soul Faints for Your Salvation"),
        S(89,96,"Lamedh: Forever, O LORD, Your Word Is Settled"),
        S(97,104,"Mem: Oh, How I Love Your Law"),
        S(105,112,"Nun: Your Word Is a Lamp to My Feet"),
        S(113,120,"Samekh: I Hate the Double-Minded"),
        S(121,128,"Ayin: I Have Done Justice"),
        S(129,136,"Pe: Your Testimonies Are Wonderful"),
        S(137,144,"Tsadhe: Righteous Are You, O LORD"),
        S(145,152,"Qoph: I Cry Out with My Whole Heart"),
        S(153,160,"Resh: Consider My Affliction"),
        S(161,168,"Shin: Princes Persecute Me Without Cause"),
        S(169,176,"Tav: Let My Cry Come Before You"),
    ],
    139: [S(1,6,"The LORD's Omniscience"), S(7,12,"The LORD's Omnipresence"), S(13,18,"The LORD's Creative Work"), S(19,24,"Search Me, O God")],
}

NEW_MAPS = {
    "1": GENESIS,
    "2": EXODUS,
    "19": PSALMS,
    "20": PROVERBS,
    "23": ISAIAH,
    "27": DANIEL,
}

def main():
    with open(MAP_PATH) as f:
        pmap = json.load(f)
    before_books = sum(1 for k in pmap if not k.startswith('_'))
    before_sections = sum(
        sum(len(pmap[k][c]) for c in pmap[k])
        for k in pmap if not k.startswith('_')
    )
    print(f"Before: {before_books} books, {before_sections} sections")

    for bk, ch_map in NEW_MAPS.items():
        if bk not in pmap:
            pmap[bk] = {}
        for ch, sections in ch_map.items():
            # Validate
            for i, s in enumerate(sections):
                if s['start'] > s['end']:
                    raise ValueError(f"Book {bk} ch {ch} section {i}: start>end")
                if i > 0 and s['start'] != sections[i-1]['end'] + 1:
                    print(f"  WARN Book {bk} ch {ch}: gap/overlap between {i-1} and {i}")
            pmap[bk][str(ch)] = sections

    after_books = sum(1 for k in pmap if not k.startswith('_'))
    after_sections = sum(
        sum(len(pmap[k][c]) for c in pmap[k])
        for k in pmap if not k.startswith('_')
    )
    print(f"After:  {after_books} books, {after_sections} sections")
    print(f"Delta:  +{after_books - before_books} books, +{after_sections - before_sections} sections")

    with open(MAP_PATH, "w") as f:
        json.dump(pmap, f, indent=2, ensure_ascii=False)
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
