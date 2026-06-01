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

# Psalm 119 — the 22 acrostic stanzas (8 verses each).
PS119 = [(s, f"Stanza {i+1}") for i, s in enumerate(range(1, 177, 8))]

AUTHORED = {
    "1": GENESIS,
    "19": {119: PS119},   # all other psalms default to one paragraph (per-psalm)
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

    problems, authored_books, chapterlevel_books = 0, 0, 0
    for bid, name, nch in OT_BOOKS:
        bk = str(bid)
        pmap.setdefault(bk, {})
        book_authored = AUTHORED.get(bk, {})
        is_authored = bool(book_authored) or bk == "19"
        if is_authored: authored_books += 1
        else: chapterlevel_books += 1
        for ch in range(1, nch + 1):
            clast = last_verse(bid, ch)
            starts_titles = book_authored.get(ch)
            if not starts_titles:
                # default: whole chapter = one paragraph
                starts_titles = [(1, f"{name} {ch}")]
            # validate
            if starts_titles[0][0] != 1:
                print(f"  ERR {name} {ch}: first start != 1"); problems += 1
            for i in range(1, len(starts_titles)):
                if starts_titles[i][0] <= starts_titles[i-1][0]:
                    print(f"  ERR {name} {ch}: non-increasing starts"); problems += 1
                if starts_titles[i][0] > clast:
                    print(f"  ERR {name} {ch}: start {starts_titles[i][0]} > last verse {clast}"); problems += 1
            pmap[bk][str(ch)] = build_sections(starts_titles, clast)

    if problems:
        raise SystemExit(f"{problems} validation problem(s) — fix before writing.")

    after_books = sum(1 for k in pmap if not k.startswith('_'))
    after_sections = sum(sum(len(pmap[k][c]) for c in pmap[k]) for k in pmap if not k.startswith('_'))
    print(f"Books: {before_books} -> {after_books}  (+{after_books - before_books})")
    print(f"OT books detailed/per-psalm: {authored_books} | chapter-level baseline: {chapterlevel_books}")
    print(f"Total sections now: {after_sections}")

    MAP_PATH.write_text(json.dumps(pmap, indent=2, ensure_ascii=False))
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
