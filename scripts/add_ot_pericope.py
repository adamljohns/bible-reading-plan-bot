"""Add Old Testament (books 1-39) pericope coverage to pericope-map.json.

Goal: eliminate the crude "break every 4 verses" paragraph-mode fallback across
the whole OT, giving every book real (or at minimum chapter-level) paragraph
structure — completing 66-book coverage.

Approach:
  • AUTHORED_STARTS holds real editorial section-start verses for books/chapters
    we divide in detail (anchored on standard narrative/poetic divisions).
  • Every other OT chapter defaults to a single chapter-level paragraph (start=1).
    That is never *wrong* (a chapter as one flowing paragraph is a legitimate
    reading unit) — just coarser than a fully subdivided pericope. Subsequent
    batches enrich more books.

Only `start` verses drive paragraph breaks in the engine; `end`/`title` are
metadata. The script reads true verse counts from docs/assets/chapters/<bid>_<ch>.json
so section ends are exact and validation is real.

Idempotent: re-running re-sets the same keys; merges, never clobbers other books.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "assets" / "pericope-map.json"
CH_DIR = ROOT / "docs" / "assets" / "chapters"

# (bookId, name, chapterCount) for all 39 OT books.
OT_BOOKS = [
    (1,"Genesis",50),(2,"Exodus",40),(3,"Leviticus",27),(4,"Numbers",36),
    (5,"Deuteronomy",34),(6,"Joshua",24),(7,"Judges",21),(8,"Ruth",4),
    (9,"1 Samuel",31),(10,"2 Samuel",24),(11,"1 Kings",22),(12,"2 Kings",25),
    (13,"1 Chronicles",29),(14,"2 Chronicles",36),(15,"Ezra",10),(16,"Nehemiah",13),
    (17,"Esther",10),(18,"Job",42),(19,"Psalms",150),(20,"Proverbs",31),
    (21,"Ecclesiastes",12),(22,"Song of Solomon",8),(23,"Isaiah",66),(24,"Jeremiah",52),
    (25,"Lamentations",5),(26,"Ezekiel",48),(27,"Daniel",12),(28,"Hosea",14),
    (29,"Joel",3),(30,"Amos",9),(31,"Obadiah",1),(32,"Jonah",4),(33,"Micah",7),
    (34,"Nahum",3),(35,"Habakkuk",3),(36,"Zephaniah",3),(37,"Haggai",2),
    (38,"Zechariah",14),(39,"Malachi",4),
]

# ── Detailed section starts (verse where each pericope begins) + titles ───────
# Genesis — standard narrative divisions.
GENESIS = {
    1:  [(1,"In the Beginning"),(3,"The First Day"),(6,"The Second Day"),(9,"The Third Day"),(14,"The Fourth Day"),(20,"The Fifth Day"),(24,"The Sixth Day"),(26,"The Creation of Man")],
    2:  [(1,"The Seventh Day, God Rests"),(4,"The Garden of Eden"),(15,"Man Placed in the Garden"),(18,"The Creation of Woman")],
    3:  [(1,"The Fall of Man"),(8,"Hiding from God"),(14,"The Curse and the Promise"),(20,"Expelled from Eden")],
    4:  [(1,"Cain and Abel"),(17,"The Line of Cain"),(25,"The Birth of Seth")],
    5:  [(1,"Adam's Descendants to Noah")],
    6:  [(1,"The Wickedness of Mankind"),(5,"Noah Pleases God"),(9,"Noah and the Flood"),(14,"The Ark")],
    7:  [(1,"Entering the Ark"),(11,"The Flood Begins"),(17,"The Flood Prevails")],
    8:  [(1,"The Flood Recedes"),(13,"The Earth Dries"),(20,"Noah's Offering")],
    9:  [(1,"God's Covenant with Noah"),(18,"Noah's Sons")],
    10: [(1,"The Table of Nations")],
    11: [(1,"The Tower of Babel"),(10,"Shem's Descendants"),(27,"Terah's Descendants")],
    12: [(1,"The Call of Abram"),(10,"Abram in Egypt")],
    13: [(1,"Abram and Lot Separate")],
    14: [(1,"Abram Rescues Lot"),(17,"Abram and Melchizedek")],
    15: [(1,"God's Covenant with Abram")],
    16: [(1,"Hagar and Ishmael")],
    17: [(1,"The Covenant of Circumcision")],
    18: [(1,"The Three Visitors"),(16,"Abraham Intercedes for Sodom")],
    19: [(1,"Sodom and Gomorrah Destroyed"),(30,"Lot and His Daughters")],
    20: [(1,"Abraham and Abimelech")],
    21: [(1,"The Birth of Isaac"),(8,"Hagar and Ishmael Sent Away"),(22,"A Treaty at Beersheba")],
    22: [(1,"The Binding of Isaac"),(20,"The Sons of Nahor")],
    23: [(1,"The Death and Burial of Sarah")],
    24: [(1,"Isaac and Rebekah"),(62,"Rebekah Meets Isaac")],
    25: [(1,"The Death of Abraham"),(12,"Ishmael's Descendants"),(19,"Jacob and Esau Born"),(29,"Esau Sells His Birthright")],
    26: [(1,"Isaac and Abimelech"),(34,"Esau's Wives")],
    27: [(1,"Jacob Gets Isaac's Blessing"),(41,"Jacob Flees from Esau")],
    28: [(1,"Jacob Sent to Laban"),(10,"Jacob's Dream at Bethel")],
    29: [(1,"Jacob Meets Rachel"),(31,"Jacob's Children")],
    30: [(1,"Jacob's Children Continued"),(25,"Jacob's Flocks Increase")],
    31: [(1,"Jacob Flees from Laban"),(22,"Laban Pursues Jacob"),(43,"The Covenant at Mizpah")],
    32: [(1,"Jacob Fears Esau"),(22,"Jacob Wrestles with God")],
    33: [(1,"Jacob Meets Esau")],
    34: [(1,"Dinah and the Shechemites")],
    35: [(1,"Jacob Returns to Bethel"),(16,"The Death of Rachel"),(23,"Jacob's Sons"),(28,"The Death of Isaac")],
    36: [(1,"Esau's Descendants")],
    37: [(1,"Joseph's Dreams"),(12,"Joseph Sold by His Brothers")],
    38: [(1,"Judah and Tamar")],
    39: [(1,"Joseph and Potiphar's Wife")],
    40: [(1,"The Cupbearer and the Baker")],
    41: [(1,"Pharaoh's Dreams"),(37,"Joseph Rises to Power")],
    42: [(1,"Joseph's Brothers Go to Egypt")],
    43: [(1,"The Brothers Return with Benjamin")],
    44: [(1,"Joseph's Silver Cup")],
    45: [(1,"Joseph Reveals Himself")],
    46: [(1,"Jacob Goes to Egypt")],
    47: [(1,"Jacob Before Pharaoh"),(13,"The Famine"),(27,"Jacob's Final Days")],
    48: [(1,"Jacob Blesses Ephraim and Manasseh")],
    49: [(1,"Jacob Blesses His Sons"),(29,"The Death of Jacob")],
    50: [(1,"The Burial of Jacob"),(15,"Joseph Reassures His Brothers"),(22,"The Death of Joseph")],
}

# Exodus — narrative + law/tabernacle divisions.
EXODUS = {
    1:  [(1,"Israel Oppressed in Egypt"),(8,"A New King Over Egypt"),(15,"The Hebrew Midwives")],
    2:  [(1,"The Birth of Moses"),(11,"Moses Flees to Midian"),(23,"God Hears Israel's Groaning")],
    3:  [(1,"The Burning Bush"),(11,"The Name of God Revealed")],
    4:  [(1,"Signs for Moses"),(18,"Moses Returns to Egypt"),(27,"Aaron Meets Moses")],
    5:  [(1,"Moses Before Pharaoh"),(22,"Moses Complains to God")],
    6:  [(1,"God Promises Deliverance"),(14,"The Family Record of Moses and Aaron")],
    7:  [(1,"Aaron's Staff Becomes a Serpent"),(14,"The Plague of Blood")],
    8:  [(1,"The Plague of Frogs"),(16,"The Plague of Gnats"),(20,"The Plague of Flies")],
    9:  [(1,"The Plague on Livestock"),(8,"The Plague of Boils"),(13,"The Plague of Hail")],
    10: [(1,"The Plague of Locusts"),(21,"The Plague of Darkness")],
    11: [(1,"The Death of the Firstborn Announced")],
    12: [(1,"The Passover Instituted"),(29,"The Exodus from Egypt"),(43,"Passover Regulations")],
    13: [(1,"Consecration of the Firstborn"),(17,"The Pillar of Cloud and Fire")],
    14: [(1,"Crossing the Red Sea"),(15,"The Sea Parts")],
    15: [(1,"The Song of Moses"),(22,"Bitter Water at Marah")],
    16: [(1,"Manna and Quail")],
    17: [(1,"Water from the Rock"),(8,"Amalek Defeated")],
    18: [(1,"Jethro's Visit"),(13,"Judges Appointed")],
    19: [(1,"Israel at Mount Sinai"),(16,"The Lord Descends")],
    20: [(1,"The Ten Commandments"),(18,"The People Fear"),(22,"Idolatry Forbidden")],
    21: [(1,"Laws About Servants"),(12,"Laws About Personal Injury")],
    22: [(1,"Laws About Property"),(16,"Social and Moral Laws")],
    23: [(1,"Justice and Mercy"),(10,"Sabbath Laws"),(14,"The Three Annual Feasts"),(20,"God's Angel to Guard Israel")],
    24: [(1,"The Covenant Confirmed"),(12,"Moses on the Mountain")],
    25: [(1,"Offerings for the Tabernacle"),(10,"The Ark"),(23,"The Table"),(31,"The Lampstand")],
    26: [(1,"The Tabernacle")],
    27: [(1,"The Bronze Altar"),(9,"The Courtyard"),(20,"Oil for the Lamp")],
    28: [(1,"The Priestly Garments")],
    29: [(1,"Consecration of the Priests")],
    30: [(1,"The Altar of Incense"),(11,"The Atonement Money"),(17,"The Bronze Basin"),(22,"The Anointing Oil"),(34,"The Incense")],
    31: [(1,"Bezalel and Oholiab"),(12,"The Sabbath")],
    32: [(1,"The Golden Calf"),(15,"Moses' Anger"),(30,"Moses Intercedes")],
    33: [(1,"The Command to Leave Sinai"),(7,"The Tent of Meeting"),(12,"Moses Sees God's Glory")],
    34: [(1,"The New Stone Tablets"),(10,"The Covenant Renewed"),(29,"The Radiant Face of Moses")],
    35: [(1,"Sabbath Regulations"),(4,"Materials for the Tabernacle"),(30,"Bezalel and Oholiab")],
    36: [(1,"Building the Tabernacle")],
    37: [(1,"Making the Ark, Table, and Lampstand")],
    38: [(1,"The Altar and the Courtyard"),(21,"Materials Used for the Tabernacle")],
    39: [(1,"The Priestly Garments Made"),(32,"The Tabernacle Completed")],
    40: [(1,"The Tabernacle Set Up"),(34,"The Glory of the Lord")],
}

# Proverbs — discourses (1-9) + the virtuous-life acrostic (31); the aphorism
# collections (10-29) read as chapter-level units.
PROVERBS = {
    1:  [(1,"The Purpose of Proverbs"),(7,"Wisdom's Call to the Young"),(20,"Wisdom Cries Aloud")],
    2:  [(1,"The Benefits of Wisdom")],
    3:  [(1,"Trust in the Lord"),(13,"Blessings of Wisdom"),(21,"Wisdom and Security")],
    4:  [(1,"Get Wisdom"),(10,"The Two Paths"),(20,"Guard Your Heart")],
    5:  [(1,"Warning Against Adultery")],
    6:  [(1,"Warnings Against Folly"),(16,"Seven Things the Lord Hates"),(20,"Warning Against Adultery")],
    7:  [(1,"Warning Against the Adulteress")],
    8:  [(1,"Wisdom's Call"),(22,"Wisdom in Creation")],
    9:  [(1,"The Way of Wisdom"),(13,"The Way of Folly")],
    30: [(1,"The Words of Agur")],
    31: [(1,"The Words of King Lemuel"),(10,"The Virtuous Wife")],
}

# Psalm 119 — the 22 acrostic stanzas (8 verses each).
PS119 = [(s, f"Stanza {i+1}") for i, s in enumerate(range(1, 177, 8))]

# Deuteronomy — landmark chapters (others stay chapter-level).
DEUTERONOMY = {
    1:  [(1,"The Command to Leave Horeb"),(19,"Spies Sent Out"),(34,"The Lord's Anger")],
    4:  [(1,"A Call to Obedience"),(41,"Cities of Refuge")],
    5:  [(1,"The Ten Commandments"),(22,"The People's Fear")],
    6:  [(1,"The Greatest Commandment — the Shema"),(10,"Remember the Lord")],
    8:  [(1,"Remember the Lord Your God")],
    28: [(1,"Blessings for Obedience"),(15,"Curses for Disobedience")],
    30: [(1,"Return and Prosper"),(11,"The Choice of Life and Death")],
    31: [(1,"Joshua to Succeed Moses")],
    32: [(1,"The Song of Moses"),(48,"Moses to Die on Mount Nebo")],
    33: [(1,"Moses Blesses the Tribes")],
    34: [(1,"The Death of Moses")],
}
RUTH = {
    1: [(1,"Naomi and Ruth"),(6,"Ruth Clings to Naomi"),(19,"Arrival in Bethlehem")],
    2: [(1,"Ruth Meets Boaz"),(17,"Ruth Returns to Naomi")],
    3: [(1,"Ruth at the Threshing Floor")],
    4: [(1,"Boaz Redeems Ruth"),(13,"The Genealogy of David")],
}
ECCLESIASTES = {
    1:  [(1,"Everything Is Meaningless"),(12,"The Vanity of Wisdom")],
    2:  [(1,"The Vanity of Pleasure"),(12,"Wisdom and Folly"),(18,"The Vanity of Toil")],
    3:  [(1,"A Time for Everything"),(9,"The God-Given Task")],
    4:  [(1,"Oppression, Toil, and Friendship")],
    5:  [(1,"Fear God"),(8,"The Vanity of Wealth")],
    6:  [(1,"The Vanity of Wealth Without Enjoyment")],
    7:  [(1,"Wisdom and Folly")],
    8:  [(1,"Obey the King"),(10,"Those Who Fear God")],
    9:  [(1,"Death Comes to All"),(13,"Wisdom Better Than Folly")],
    10: [(1,"Wisdom and Folly")],
    11: [(1,"Cast Your Bread Upon the Waters"),(7,"Remember Your Creator")],
    12: [(1,"Remember Your Creator"),(9,"The Conclusion of the Matter")],
}
SONG = {
    1: [(1,"The Bride and the Daughters"),(9,"The Bridegroom")],
    2: [(1,"The Bride and Bridegroom Delight"),(8,"The Bride's Longing")],
    3: [(1,"The Bride's Dream"),(6,"Solomon's Wedding Procession")],
    4: [(1,"The Bridegroom Praises the Bride")],
    5: [(1,"The Bride Seeks Her Beloved")],
    6: [(1,"Together in the Garden")],
    7: [(1,"The Bridegroom's Delight")],
    8: [(1,"The Power of Love")],
}
HOSEA = {
    1:[(1,"Hosea's Wife and Children")], 2:[(1,"Israel's Unfaithfulness"),(14,"The Lord's Mercy")],
    3:[(1,"Hosea Redeems His Wife")], 4:[(1,"The Lord's Charge Against Israel")],
    5:[(1,"Judgment Against Israel and Judah")], 6:[(1,"A Call to Repentance")],
    7:[(1,"Israel's Corruption")], 8:[(1,"Israel Reaps the Whirlwind")],
    9:[(1,"Punishment for Israel")], 10:[(1,"Israel's Guilt and Punishment")],
    11:[(1,"God's Love for Israel")], 12:[(1,"Israel's Sin")],
    13:[(1,"The Lord's Anger Against Israel")], 14:[(1,"Repentance Brings Blessing")],
}
JOEL = {
    1: [(1,"The Locust Plague"),(13,"A Call to Repentance")],
    2: [(1,"The Day of the Lord"),(12,"Return to the Lord"),(18,"The Lord's Response"),(28,"The Promise of the Spirit")],
    3: [(1,"Judgment on the Nations"),(17,"Blessing for God's People")],
}
AMOS = {
    1:[(1,"Judgment on Israel's Neighbors")], 2:[(1,"Judgment on Judah and Israel")],
    3:[(1,"Israel's Guilt and Punishment")], 4:[(1,"Israel Has Not Returned to God")],
    5:[(1,"A Call to Repentance"),(18,"The Day of the Lord")], 6:[(1,"Woe to the Complacent")],
    7:[(1,"Visions of Judgment"),(10,"Amos and Amaziah")], 8:[(1,"The Basket of Summer Fruit")],
    9:[(1,"The Destruction of Israel"),(11,"The Restoration of Israel")],
}
OBADIAH = {1: [(1,"The Judgment of Edom"),(15,"The Day of the Lord"),(17,"The Deliverance of Israel")]}
JONAH = {
    1: [(1,"Jonah Flees from the Lord"),(17,"Jonah and the Great Fish")],
    2: [(1,"Jonah's Prayer")],
    3: [(1,"Jonah Goes to Nineveh"),(6,"Nineveh Repents")],
    4: [(1,"Jonah's Anger and the Lord's Compassion")],
}
MICAH = {
    1:[(1,"Judgment Against Samaria and Judah")], 2:[(1,"Woe to Oppressors")],
    3:[(1,"Rulers and Prophets Rebuked")], 4:[(1,"The Mountain of the Lord"),(9,"Deliverance from Babylon")],
    5:[(1,"The Ruler from Bethlehem")], 6:[(1,"The Lord's Case Against Israel"),(9,"Israel's Guilt")],
    7:[(1,"Israel's Misery"),(8,"Israel's Confession and Comfort")],
}
NAHUM = {1:[(1,"The Lord's Anger Against Nineveh")], 2:[(1,"The Fall of Nineveh")], 3:[(1,"Woe to Nineveh")]}
HABAKKUK = {
    1: [(1,"Habakkuk's Complaint"),(5,"The Lord's Answer"),(12,"Habakkuk's Second Complaint")],
    2: [(1,"The Lord's Answer"),(6,"Woes to the Wicked")],
    3: [(1,"Habakkuk's Prayer")],
}
ZEPHANIAH = {
    1: [(1,"The Coming Day of the Lord")],
    2: [(1,"A Call to Repentance"),(4,"Judgment on the Nations")],
    3: [(1,"Jerusalem's Sin and Redemption"),(14,"A Song of Joy")],
}
HAGGAI = {
    1: [(1,"A Call to Rebuild the Temple"),(12,"The People Obey")],
    2: [(1,"The Promised Glory"),(10,"Blessings for a Defiled People"),(20,"Zerubbabel the Lord's Signet")],
}
ZECHARIAH = {
    1:[(1,"A Call to Return"),(7,"The Horseman Among the Myrtles"),(18,"The Four Horns")],
    2:[(1,"A Man with a Measuring Line")], 3:[(1,"Cleansing of the High Priest")],
    4:[(1,"The Golden Lampstand")], 5:[(1,"The Flying Scroll"),(5,"The Woman in the Basket")],
    6:[(1,"The Four Chariots"),(9,"The Crown and the Branch")], 7:[(1,"Justice and Mercy, Not Fasting")],
    8:[(1,"The Lord Promises to Bless Jerusalem")], 9:[(1,"Judgment on Israel's Enemies"),(9,"The Coming King")],
    10:[(1,"The Lord Will Restore His People")], 11:[(1,"The Flock Doomed to Slaughter")],
    12:[(1,"Jerusalem's Deliverance"),(10,"Mourning for the Pierced One")],
    13:[(1,"Idolatry Cut Off"),(7,"The Shepherd Struck")], 14:[(1,"The Lord Comes and Reigns")],
}
MALACHI = {
    1: [(1,"The Lord's Love for Israel"),(6,"Polluted Offerings")],
    2: [(1,"Corrupt Priests"),(10,"Judah's Faithlessness")],
    3: [(1,"The Messenger of the Lord"),(6,"Robbing God"),(13,"The Faithful Remnant")],
    4: [(1,"The Day of the Lord")],
}

AUTHORED = {
    "1": GENESIS,
    "2": EXODUS,
    "5": DEUTERONOMY,
    "8": RUTH,
    "19": {119: PS119},   # all other psalms default to one paragraph (per-psalm)
    "20": PROVERBS,       # chapters 10-29 default to chapter-level
    "21": ECCLESIASTES,
    "22": SONG,
    "28": HOSEA,
    "29": JOEL,
    "30": AMOS,
    "31": OBADIAH,
    "32": JONAH,
    "33": MICAH,
    "34": NAHUM,
    "35": HABAKKUK,
    "36": ZEPHANIAH,
    "37": HAGGAI,
    "38": ZECHARIAH,
    "39": MALACHI,
    # Lamentations (25): each chapter is one acrostic poem — chapter-level is correct, left as-is.
}

def last_verse(bid, ch):
    p = CH_DIR / f"{bid}_{ch}.json"
    d = json.loads(p.read_text())
    verses = d.get("NKJV") or next(iter(d.values()), {})
    return max(int(k) for k in verses.keys()) if verses else 1

def build_sections(starts_titles, chap_last):
    """starts_titles: list of (start, title). Returns contiguous section dicts."""
    out = []
    for i, (start, title) in enumerate(starts_titles):
        end = (starts_titles[i+1][0] - 1) if i + 1 < len(starts_titles) else chap_last
        out.append({"start": start, "end": end, "title": title})
    return out

def main():
    pmap = json.loads(MAP_PATH.read_text())
    before_books = sum(1 for k in pmap if not k.startswith('_'))

    problems, added_detail, preserved, baseline = 0, 0, 0, 0
    for bid, name, nch in OT_BOOKS:
        bk = str(bid)
        pmap.setdefault(bk, {})
        book_authored = AUTHORED.get(bk, {})
        for ch in range(1, nch + 1):
            chs = str(ch)
            existing = pmap[bk].get(chs)
            # NON-DESTRUCTIVE: never downgrade a chapter that's already subdivided
            # (whether by an earlier run or a concurrent fleet/PJ edit).
            if existing and len(existing) > 1:
                preserved += 1
                continue
            authored = book_authored.get(ch)
            if authored:
                clast = last_verse(bid, ch)
                if authored[0][0] != 1:
                    print(f"  ERR {name} {ch}: first start != 1"); problems += 1
                for i in range(1, len(authored)):
                    if authored[i][0] <= authored[i-1][0]:
                        print(f"  ERR {name} {ch}: non-increasing starts"); problems += 1
                    if authored[i][0] > clast:
                        print(f"  ERR {name} {ch}: start {authored[i][0]} > last verse {clast}"); problems += 1
                pmap[bk][chs] = build_sections(authored, clast)
                added_detail += 1
            elif not existing:
                clast = last_verse(bid, ch)
                pmap[bk][chs] = [{"start": 1, "end": clast, "title": f"{name} {ch}"}]
                baseline += 1
            else:
                baseline += 1  # leave existing chapter-level [1] untouched

    if problems:
        raise SystemExit(f"{problems} validation problem(s) — fix before writing.")
    print(f"Chapters: +{added_detail} newly subdivided | {preserved} preserved (already detailed) | {baseline} chapter-level")

    after_books = sum(1 for k in pmap if not k.startswith('_'))
    after_sections = sum(sum(len(pmap[k][c]) for c in pmap[k]) for k in pmap if not k.startswith('_'))
    print(f"Books: {before_books} -> {after_books}  (+{after_books - before_books})")
    print(f"Total sections now: {after_sections}")

    MAP_PATH.write_text(json.dumps(pmap, indent=2, ensure_ascii=False))
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
