#!/usr/bin/env python3
"""
Reverential-pronoun fixer for the lexicon (Greek + Hebrew word study pages).

Reuses the dictionary fixer's filters but with a different SKIP_FILES list:
- Strong's-numbered files (G1.html, H1.html etc.) where the lemma itself
  is a person's name (e.g., G2424 Iesous = Jesus, but lexicon entries for
  human names like Moses, Abraham, etc., would be skipped).

For lexicon, almost all entries that quote scripture about God/Christ are
GOOD candidates — the lemma is a Greek/Hebrew word, not a person.

Run:  python3 scripts/fix_lex_pronouns.py [--dry-run]
"""
import re, sys
from pathlib import Path

# Reuse logic from the dictionary fixer
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_dict_pronouns import (
    SCRIPT_STYLE, fix_html_text_segment,
    HUMAN_NAMES, ANTI_DEITY, has_deity_anchor, PRONOUN_RE, cap_pronoun,
)

LEX_DIR = Path("/Users/adamjohns/bible-reading-plan-bot/docs/lexicon")

# Strong's numbers for lemmas that are PERSONAL NAMES of humans or anti-deity.
# In these entries, pronouns within quoted scripture might refer to the named
# human (Moses, Abraham, etc.) rather than to God, so auto-fixing is unsafe.
# Conservative skip list — all the major OT/NT human-name lemmas.
SKIP_LEMMA_NAMES = {
    # Hebrew lemmas naming humans (frequently appearing)
    "H120",   # Adam (the man)
    "H121",   # Adam (proper name)
    "H85",    # Abraham
    "H87",    # Abram
    "H1893",  # Abel
    "H7014",  # Cain
    "H5146",  # Noah
    "H8283",  # Sarah
    "H3327",  # Isaac
    "H3458",  # Ishmael
    "H3290",  # Jacob
    "H6215",  # Esau
    "H3130",  # Joseph
    "H4872",  # Moses
    "H175",   # Aaron
    "H3091",  # Joshua
    "H3612",  # Caleb
    "H8050",  # Samuel
    "H7586",  # Saul
    "H1732",  # David
    "H8010",  # Solomon
    "H452",   # Elijah
    "H477",   # Elisha
    "H3470",  # Isaiah
    "H3414",  # Jeremiah
    "H3168",  # Ezekiel
    "H1840",  # Daniel
    "H1949",  # Hosea
    "H3415",  # Joel  (varies)
    "H5986",  # Amos
    "H3124",  # Jonah
    "H4318",  # Micah
    "H5151",  # Nahum
    "H2265",  # Habakkuk
    "H6846",  # Zephaniah
    "H2292",  # Haggai
    "H2148",  # Zechariah
    "H4401",  # Malachi
    "H347",   # Job
    "H7327",  # Ruth
    "H829",   # Esther
    "H4782",  # Mordecai
    # Greek lemmas naming humans (NT)
    "G2491",  # John
    "G4074",  # Peter
    "G3972",  # Paul
    "G2638",  # John Mark, etc.
    "G3137",  # Maria/Miriam (Mary — could be Magdalene OR mother of Jesus)
    "G2455",  # Judas Iscariot
    "G2585",  # Caiaphas
    "G4091",  # Pilate
    "G2264",  # Herod
    "G408",   # Andrew
    "G5376",  # Philip
    "G918",   # Bartholomew
    "G2381",  # Thomas
    "G2385",  # James
    "G3156",  # Matthew
    "G2280",  # Thaddaeus
    "G4613",  # Simon
    "G2976",  # Lazarus
    "G3137",  # Mary
    "G3092",  # Martha (G3136)
    "G3136",  # Martha
    "G3478",  # Nathanael
    # Anti-deity / Satan-related lemmas
    "G4567",  # Satan
    "G1228",  # diabolos (devil)
    "G500",   # antichristos
    "G954",   # Beelzebul
    "G3789",  # ophis (serpent — though also literal serpent)
    "G1404",  # drakon (dragon)
}

# Lexicon-specific: verse text is inside <span class="verse-text">...</span>,
# not enclosed in quote marks. Match that span and apply quote-style filters.
VERSE_SPAN_RE = re.compile(
    r'(<span\s+class=["\']verse-text["\'][^>]*>)([^<]+)(</span>)',
    re.IGNORECASE
)
# Page-level deity context: extract <title>, h1, .gloss, .original-word.
# If any of these contain a deity term, the article is ABOUT deity and quotes
# can be treated as deity-context regardless of internal anchors.
PAGE_TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.IGNORECASE | re.DOTALL)
GLOSS_RE = re.compile(r'<div class=["\']gloss["\'][^>]*>(.*?)</div>', re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r'<meta name=["\']description["\']\s+content=["\']([^"\']+)["\']', re.IGNORECASE)

DEITY_TOPIC_TERMS = re.compile(
    r"\b(God|Lord|YHWH|Yahweh|Yeshua|Yahveh|Jesus|Christ|Messiah|Holy Spirit|"
    r"Spirit of God|Spirit of the Lord|Almighty|Most High|Father|Son of God|"
    r"Son of Man|Lamb of God|Word of God|Logos|Alpha|Omega|Aleph|Tav|"
    r"the Beginning|the End|the First|the Last|theos|kyrios|Elohim|"
    r"Adonai|El Shaddai|Ruach|pneuma|Christos|Iesous|hagios|holy)\b"
)

def page_is_about_deity(html_str):
    """Check if the article's title/gloss/description suggests it's about deity."""
    bits = []
    m = PAGE_TITLE_RE.search(html_str)
    if m: bits.append(m.group(1))
    m = GLOSS_RE.search(html_str)
    if m: bits.append(m.group(1))
    m = META_DESC_RE.search(html_str)
    if m: bits.append(m.group(1))
    combined = " | ".join(bits)
    return bool(DEITY_TOPIC_TERMS.search(combined))

# First-person divine speech: God / Jesus speaking. Capitalize me/my/myself.
# Triggered when quote contains "I am" + deity anchor, or "thus says the LORD",
# or quote ends with "—Lord" / "the Lord" attribution.
DIVINE_SPEECH = re.compile(
    r"\bI am\b|"
    r"\bthus says the (?:LORD|Lord)\b|"
    r"\bsays the (?:LORD|Lord)\b|"
    r"\bdeclares the (?:LORD|Lord)\b",
    re.IGNORECASE
)
FIRST_PERSON_PRONOUN = re.compile(r"\b(me|my|mine|myself)\b")

def fix_quote_with_context(quoted_text, deity_context=False):
    """Like fix_quote but also accepts page-level deity context, AND
    handles first-person pronouns (me/my/mine/myself) when divine speech
    is detected within the quote."""
    from fix_dict_pronouns import HUMAN_NAMES, ANTI_DEITY, has_deity_anchor, PRONOUN_RE, cap_pronoun
    if HUMAN_NAMES.search(quoted_text):
        return quoted_text
    if ANTI_DEITY.search(quoted_text):
        return quoted_text
    # Either internal anchor OR external page-level context establishes deity
    if not (has_deity_anchor(quoted_text) or deity_context):
        return quoted_text
    # Capitalize he/him/his/himself
    out = PRONOUN_RE.sub(lambda m: cap_pronoun(m.group(0)), quoted_text)
    # If divine speech detected, also capitalize first-person pronouns
    if DIVINE_SPEECH.search(out):
        out = FIRST_PERSON_PRONOUN.sub(lambda m: cap_pronoun(m.group(0)), out)
    return out

def fix_lex_quotes(text, deity_context=False):
    """Apply lexicon-specific span filtering."""
    return VERSE_SPAN_RE.sub(
        lambda m: m.group(1) + fix_quote_with_context(m.group(2), deity_context) + m.group(3),
        text
    )

def fix_file_lex(filepath, dry_run=False):
    name = filepath.stem  # e.g., "G1", "H120"
    if name in SKIP_LEMMA_NAMES:
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()
    masks = []
    def mask(m):
        masks.append(m.group(2))
        return m.group(1) + f"___MOOP_MASK_{len(masks)-1}___" + m.group(3)
    masked = SCRIPT_STYLE.sub(mask, original)
    deity_ctx = page_is_about_deity(masked)
    # Apply both the dictionary-style fixes AND the lexicon span-aware quote fix
    fixed = fix_html_text_segment(masked)
    fixed = fix_lex_quotes(fixed, deity_context=deity_ctx)
    for i, content in enumerate(masks):
        fixed = fixed.replace(f"___MOOP_MASK_{i}___", content)
    if fixed == original:
        return 0
    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(fixed)
    return sum(1 for _ in re.finditer(r"\b(He|Him|His|Himself)\b", fixed)) - \
           sum(1 for _ in re.finditer(r"\b(He|Him|His|Himself)\b", original))

def main():
    dry = "--dry-run" in sys.argv
    files = sorted(LEX_DIR.glob("*.html"))
    total = 0
    n_changed = 0
    for fp in files:
        delta = fix_file_lex(fp, dry_run=dry)
        if delta > 0:
            n_changed += 1
            total += delta
    print(f"{'[DRY RUN] ' if dry else ''}Lexicon files modified: {n_changed}/{len(files)}")
    print(f"{'[DRY RUN] ' if dry else ''}Pronouns capitalized: {total}")

if __name__ == "__main__":
    main()
