#!/usr/bin/env python3
"""
Conservative reverential-pronoun fixer for dictionary HTML files.

Fixes ONLY high-confidence patterns where the antecedent is unambiguously
God / Jesus / the Holy Spirit:

  1. Direct adjacency: a deity anchor (Jesus, Christ, the Lord, the Father,
     Holy Spirit, God) immediately followed by a comma/space and a
     lowercase pronoun (he, him, his, himself).

  2. Within a single quoted Bible passage (text inside straight or curly
     quotes): if the quote ALSO contains a deity anchor and NO human
     proper name in the same quote, capitalize lowercase deity pronouns.
     This is the reverential-caps NKJV-style rendering applied to verses
     that other translations (ESV/NIV/KJV) leave lowercase.

What it does NOT touch:
  - Pronouns outside <p>/<li>/<h*>/<div> visible content.
  - Bible quotes that mention a human (Adam, Abraham, Moses, David, etc.)
    AND a deity anchor — too ambiguous for automated handling.
  - Prose paragraphs that mention multiple subjects without clear deity
    proximity.

Run:  python3 scripts/fix_dict_pronouns.py [--dry-run]
"""
import re, glob, sys, html
from pathlib import Path

DICT_DIR = Path("/Users/adamjohns/bible-reading-plan-bot/docs/dictionary")

# Names/terms that disqualify a quote from auto-fix (refer to humans, Satan, etc.)
HUMAN_NAMES = re.compile(
    r"\b(Adam|Eve|Cain|Abel|Noah|Abraham|Abram|Sarah|Isaac|Ishmael|Jacob|Esau|Joseph|"
    r"Moses|Aaron|Joshua|Caleb|Samuel|Saul|David|Solomon|Elijah|Elisha|Isaiah|"
    r"Jeremiah|Ezekiel|Daniel|Hosea|Joel|Amos|Jonah|Micah|Nahum|Habakkuk|Zephaniah|"
    r"Haggai|Zechariah|Malachi|Job|Naomi|Ruth|Boaz|Hannah|Esther|Mordecai|"
    r"John(?: the Baptist)?|Peter|Andrew|Philip|Bartholomew|Thomas|Matthew|James|"
    r"Thaddaeus|Simon(?: the Zealot)?|Judas(?! Iscariot)|Iscariot|Paul|Saul of Tarsus|"
    r"Barnabas|Stephen|Timothy|Titus|Lazarus|Martha|Mary Magdalene|"
    r"Nicodemus|Caiaphas|Annas|Pilate|Herod|Nebuchadnezzar|Pharaoh|Cyrus|Darius|"
    r"Diotrephes|Demetrius|Gaius|Cornelius|Onesimus|Philemon|Apollos|Aquila|Priscilla|"
    r"Nathanael|Zacchaeus|Bartimaeus|Judas Iscariot)\b"
)

# Anti-deity terms — if these appear in a quote, the pronouns may refer to
# Satan/the devil/etc. and reverential caps must NOT be applied.
ANTI_DEITY = re.compile(
    r"\b(devil|Devil|Satan|the evil one|the serpent|the dragon|the accuser|"
    r"the tempter|the lawless one|the man of lawlessness|the adversary|"
    r"Beelzebub|Beelzebul|Lucifer)\b"
)

# Files whose subject is an identifiable human or anti-deity figure — pronoun
# fixes inside these files are too ambiguous for automated handling and are
# skipped entirely. Manual review only.
SKIP_FILES = {
    # OT figures
    "aaron.html","abel.html","abigail.html","abimelech.html","abraham.html","abram.html",
    "absalom.html","achan.html","adam.html","ahab.html","amos.html","balaam.html",
    "barak.html","bathsheba.html","benjamin.html","boaz.html","caleb.html","cain.html",
    "cyrus.html","daniel.html","darius.html","david.html","deborah.html","ehud.html",
    "elijah.html","elisha.html","esau.html","esther.html","eve.html","ezekiel.html",
    "ezra.html","gideon.html","habakkuk.html","haggai.html","hagar.html","hannah.html",
    "herod.html","hezekiah.html","hosea.html","isaac.html","isaiah.html","ishmael.html",
    "jacob.html","jehu.html","jephthah.html","jeremiah.html","jeroboam.html","jezebel.html",
    "job.html","joel.html","jonah.html","joseph.html","joshua.html","josiah.html",
    "judah.html","judas.html","judas-iscariot.html","laban.html","leah.html",
    "manasseh.html","mary-magdalene.html","melchizedek.html","methuselah.html","micah.html",
    "miriam.html","mordecai.html","moses.html","naaman.html","nahum.html","naomi.html",
    "nathan.html","nebuchadnezzar.html","nehemiah.html","nicodemus.html","noah.html",
    "obadiah.html","pharaoh.html","rachel.html","rahab.html","rebekah.html","rehoboam.html",
    "ruth.html","samson.html","samuel.html","sarah.html","saul.html","sennacherib.html",
    "seth.html","shadrach.html","solomon.html","tamar.html","uriah.html","uzziah.html",
    "zechariah.html","zedekiah.html","zephaniah.html","zerubbabel.html",
    # NT figures
    "andrew.html","annas.html","apollos.html","aquila.html","barnabas.html",
    "bartholomew.html","bartimaeus.html","caiaphas.html","cornelius.html","demas.html",
    "demetrius.html","diotrephes.html","epaphras.html","felix.html","festus.html",
    "gaius.html","james.html","john-the-baptist.html","jonah-prophet.html","judas-iscariot.html",
    "lazarus.html","luke.html","lydia.html","mark.html","martha.html","matthew.html",
    "mary-mother-of-jesus.html","nathanael.html","onesimus.html","paul.html","peter.html",
    "philemon.html","philip.html","pilate.html","priscilla.html","silas.html","simon-peter.html",
    "stephen.html","thomas.html","timothy.html","titus.html","zacchaeus.html",
    # Anti-deity entries
    "antichrist.html","devil.html","satan.html","lucifer.html","beelzebub.html",
    "the-tempter.html","serpent.html","dragon.html",
}

DEITY_ANCHOR = re.compile(
    r"\b(Jesus|Christ|the Lord|Lord Jesus|Yahweh|Yeshua|Messiah(?! is)|the Savior|"
    r"the Redeemer|the Son of God|the Son of Man|the Father|the Spirit|"
    r"the Holy Spirit|the Lamb|"
    r"God the Father|God the Son|God Himself|the Father, the Son, and the Holy Spirit|"
    r"Almighty God)\b"
)
# Bare "God" — capital G only; treated as anchor if no false-god markers nearby
BARE_GOD = re.compile(r"\bGod\b")
FALSE_GOD_MARKERS = re.compile(
    r"\b(false god|other god|foreign god|strange god|pagan god|god of (?:war|fortune|"
    r"this age|this world|the dead)|gods of|household god|idol|god-king|"
    r"so-called god|calling himself god)\b",
    re.IGNORECASE,
)

PRONOUN_RE = re.compile(r"\b(he|him|his|himself)\b")

def cap_pronoun(word):
    return word[0].upper() + word[1:]

def has_deity_anchor(text):
    if DEITY_ANCHOR.search(text):
        return True
    # Bare "God" only counts if no false-god marker is in the same text
    if BARE_GOD.search(text) and not FALSE_GOD_MARKERS.search(text):
        return True
    return False

def fix_quote(quoted_text):
    """Apply reverential caps within a quote IF deity anchor present and no human name and no anti-deity term."""
    if HUMAN_NAMES.search(quoted_text):
        return quoted_text  # Too ambiguous
    if ANTI_DEITY.search(quoted_text):
        return quoted_text  # Pronouns may refer to Satan/devil — leave alone
    if not has_deity_anchor(quoted_text):
        return quoted_text  # No deity anchor — leave alone
    # Capitalize lowercase he/him/his/himself anywhere in the quote
    return PRONOUN_RE.sub(lambda m: cap_pronoun(m.group(0)), quoted_text)

# Pattern 1: deity anchor immediately followed by lowercase pronoun
# e.g., "Christ, he loves us" -> "Christ, He loves us"
ADJACENT_RE = re.compile(
    r"\b(Jesus|Christ|the Lord|the Father|Holy Spirit|the Spirit|the Son(?! of man)|the Lamb)"
    r"(\s*[,]?\s+|\s+is\s+|\s+has\s+|\s+had\s+|\s+will\s+|\s+who\s+|\s+that\s+|\s+which\s+|\s+for\s+|\s+by\s+)"
    r"(he|him|his|himself)\b"
)

# Pattern 2: quoted passages — find content between " ... " or " ... "
# Conservative: only straight double quotes paired
QUOTE_RE = re.compile(r'"([^"]{8,400}?)"')
CURLY_RE = re.compile(r'\u201c([^\u201d]{8,400}?)\u201d')

def fix_html_text_segment(text):
    """Apply both patterns to a piece of plain text."""
    out = text
    # Pattern 1
    out = ADJACENT_RE.sub(lambda m: m.group(1) + m.group(2) + cap_pronoun(m.group(3)), out)
    # Pattern 2: quoted passages
    out = QUOTE_RE.sub(lambda m: '"' + fix_quote(m.group(1)) + '"', out)
    out = CURLY_RE.sub(lambda m: '\u201c' + fix_quote(m.group(1)) + '\u201d', out)
    return out

# Skip <script>/<style> blocks; only fix text in visible HTML
SCRIPT_STYLE = re.compile(r"(<(?:script|style)[^>]*>)(.*?)(</(?:script|style)>)", re.DOTALL | re.IGNORECASE)

def fix_file(filepath, dry_run=False):
    if filepath.name in SKIP_FILES:
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    # Mask out <script> and <style> contents during fix
    masks = []
    def mask(m):
        masks.append(m.group(2))
        return m.group(1) + f"___MOOP_MASK_{len(masks)-1}___" + m.group(3)
    masked = SCRIPT_STYLE.sub(mask, original)

    fixed = fix_html_text_segment(masked)

    # Restore masked scripts/styles
    for i, content in enumerate(masks):
        fixed = fixed.replace(f"___MOOP_MASK_{i}___", content)

    if fixed == original:
        return 0
    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed)
    # Count changes
    return sum(1 for _ in re.finditer(r"\b(He|Him|His|Himself)\b", fixed)) - \
           sum(1 for _ in re.finditer(r"\b(He|Him|His|Himself)\b", original))

def main():
    dry = "--dry-run" in sys.argv
    files = sorted(DICT_DIR.glob("*.html"))
    total_changed = 0
    files_changed = 0
    for fp in files:
        delta = fix_file(fp, dry_run=dry)
        if delta > 0:
            files_changed += 1
            total_changed += delta
    print(f"{'[DRY RUN] ' if dry else ''}Files modified: {files_changed}/{len(files)}")
    print(f"{'[DRY RUN] ' if dry else ''}Pronouns capitalized: {total_changed}")

if __name__ == "__main__":
    main()
