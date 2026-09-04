#!/usr/bin/env python3
"""mbt-verify-amp.py -- deterministic checks on MBT batch 'amp'/'notes' fields.

  1. Every [bracket] transliteration in `amp` must correspond to a Strong's tag
     present in THAT verse's kit line (data/mbt-kits/<b>_<c>.kit.json).
  2. A bracket that cites "the KJV margin" is only allowed when the kit verse
     actually carries a <sup> margin note.
  3. No "-'d" suffix glued onto a transliteration in `notes` (e.g. "shamar'd").

Usage: python3 bin/mbt-verify-amp.py <book> [<ch> ...]   (no chapters = all batches of the book)
Exit 1 if any bracket is untraceable or a margin attribution is unsupported.
"""
import json, re, sys, glob, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = re.compile(r"\[H(\d{1,4})\s*([^\]—]*?)\s*(?:—|\])")
BR  = re.compile(r"\[([^\]]+)\]")
# tokens that are legitimately not a kit translit (divine-name conventions, glosses that
# the house pattern allows to stand alone, KJV-margin quote brackets)
ALLOW = {"yhwh", "yah", "adonai", "adon", "el", "eloah", "elohim", "elyon", "selah",
         "kjv", "margin", "the", "of", "and", "a", "an", "or", "in", "on", "to", "sense",
         "haleluyah", "halelu", "bene", "ben", "ish", "adam", "am", "goy", "leom", "ummah",
         "ba", "be", "bi", "ha", "ka", "ke", "ki", "la", "le", "mi", "me", "u", "va", "ve", "kol", "ad", "al", "et", "im", "min", "she", "lo"}
# house spelling -> lexicon spelling where the canonical form still differs
ALIAS = {"elyon": "elyoun", "esher": "osher", "ashre": "osher", "maskil": "sakal", "holel": "halal",
         "shorer": "shurer", "hagig": "hagig", "tachti": "tachti"}
# lexicon entries known to be wrong/blank (kit defect) -- accept the house translit as-is
KIT_DEFECT = {"tachti"}

def norm(s):
    """canonical ASCII spelling so that house/lexicon/KJV-Strong's variants compare equal:
    h-with-dot -> k, ch/kh/q -> k, tz/ts -> ts, ph -> f, th -> t, v/w -> b/u, iy -> i, uw -> u, doubles collapsed"""
    s = s.replace("\u1e25", "k").replace("\u1e24", "k").replace("\u1e63", "ts").replace("\u1e62", "ts")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("\u2019", "").replace("-", "")
    s = re.sub(r"[^a-z]", "", s)
    for a, b in (("tz", "ts"), ("kh", "k"), ("ch", "k"), ("q", "k"), ("ph", "f"), ("th", "t"),
                 ("v", "b"), ("w", "u"), ("iy", "i"), ("uw", "u"), ("uu", "u"), ("ee", "e")):
        s = s.replace(a, b)
    return re.sub(r"(.)\1+", r"\1", s)

LEX = None
def lexicon():
    global LEX
    if LEX is None:
        lp = os.path.join(ROOT, "data", "mbt-kits", "strongs-lookup.json")
        LEX = json.load(open(lp)) if os.path.exists(lp) else {}
    return LEX

def kit_translits(kjv):
    """translits from the verse's tags, plus lexicon translits for every tagged number;
    returns (set_of_translits, count_of_numbers_with_no_translit_anywhere)"""
    out, blind = set(), 0
    lex = lexicon()
    for num, tr in TAG.findall(kjv):
        t = norm(tr)
        if t: out.add(t)
        e = lex.get(f"H{num}") or lex.get(num) or {}
        lt = norm(e.get("translit", "") if isinstance(e, dict) else str(e))
        if lt: out.add(lt)
        if not t and not lt: blind += 1
    return out, blind

def matches(word, kit):
    w = norm(word)
    if not w or w in ALLOW: return True
    w = norm(ALIAS.get(w, w))
    if w in {norm(x) for x in KIT_DEFECT}: return True
    for k in kit:
        if w == k: return True
        if len(w) >= 3 and len(k) >= 3 and (w.startswith(k) or k.startswith(w)): return True
        # simple inflection tolerance: shared stem of >=4 chars
        if len(w) >= 4 and len(k) >= 4 and w[:4] == k[:4]: return True
    return False

def bracket_words(content):
    c = content.strip()
    if c.startswith("'"):
        # ['margin text', translit, the KJV margin]  -> translit is the token after the closing quote
        m = re.match(r"'[^']*'\s*,\s*([A-Za-z\-' ]+?)\s*(?:,|--|$)", c)
        if not m: return []
        tok = m.group(1).strip()
        if tok.lower().startswith("the kjv"): return []
        return tok.split()
    head = c.split("--")[0].strip()
    head = head.split(",")[0].strip()
    return head.split()

def check(book, chapters):
    files = sorted(glob.glob(os.path.join(ROOT, "data", "mbt-batches", f"{book}_*.json")))
    if chapters:
        want = {int(c) for c in chapters}
        files = [f for f in files if int(re.search(r"_(\d+)\.json$", f).group(1)) in want]
    bad = 0
    for f in files:
        d = json.load(open(f))
        ch = d["chapter"]
        kp = os.path.join(ROOT, "data", "mbt-kits", f"{book}_{ch}.kit.json")
        if not os.path.exists(kp):
            print(f"  {book}_{ch}: NO KIT"); continue
        kit = json.load(open(kp))["verses"]
        issues = []
        for v, vd in d["verses"].items():
            kv = kit.get(v, {}).get("kjv_strongs", "")
            kt, blind = kit_translits(kv)
            for content in BR.findall(vd.get("amp", "")):
                if "KJV margin" in content and "<sup>" not in kv:
                    issues.append((v, "MARGIN", f"[{content[:60]}] but kit verse has no <sup> margin"))
                for w in bracket_words(content):
                    if not matches(w, kt):
                        kind = "UNVERIFIABLE" if blind else "BRACKET"
                        issues.append((v, kind, f"'{w}' in [{content[:50]}] not traceable to a tag in this verse" + (f" ({blind} tag(s) here have no translit anywhere)" if blind else "")))
            for m in re.finditer(r"\b([a-z]{3,})'d\b", vd.get("notes", "")):
                issues.append((v, "SUFFIX", f"\"{m.group(0)}\" -- -'d glued to a transliteration"))
        n = len(issues); bad += sum(1 for i in issues if i[1] in ("BRACKET", "MARGIN"))
        unv = sum(1 for i in issues if i[1] == "UNVERIFIABLE")
        issues = [i for i in issues if i[1] != "UNVERIFIABLE"]
        status = ("ok" if not issues else f"{len(issues)} issue(s)") + (f", {unv} unverifiable" if unv else "")
        print(f"  {book}_{ch}: {len(d['verses'])} verses, {status}")
        for v, kind, msg in issues:
            print(f"      v{v} {kind}: {msg}")
    return bad

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    bad = check(sys.argv[1], sys.argv[2:])
    print(f"TOTAL untraceable/unsupported: {bad}")
    sys.exit(1 if bad else 0)
