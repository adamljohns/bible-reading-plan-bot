#!/usr/bin/env python3
"""mbt-chapter-kit.py <bookId> <chapter>

Assemble the COPYRIGHT-SAFE source kit for one chapter so a local LLM (or Claude)
can draft MBT verses anchored to the original language. Pulls:
  - Strong's-tagged KJV  (the interlinear anchor: each word carries its Greek/Hebrew
    Strong's number)            -> rendered as  word[G1234] / word[H1234]
  - WEB                   (clean, modern, public-domain phrasing)

Both are public domain. The copyrighted columns (NKJV/ESV/NASB/NLT/CSB/AMP/MSG/NIV/
NRSVCE) are NEVER written into the kit — they exist in the cache only for the post-hoc
near-verbatim check in build-mbt.py, and must not reach the drafting model.

Source: docs/assets/chapters/<book>_<ch>.json (has Strong's-tagged KJV + WEB for all 27
NT books + Psalms + Proverbs); falls back to docs/assets/verse-cache.json (KJV+WEB, no
Strong's) for books without a chapters file.

Output: data/mbt-kits/<book>_<ch>.kit.json   (zero tokens — pure local assembly)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOOKUP_PATH = os.path.join(ROOT, "data", "mbt-kits", "strongs-lookup.json")
_STRONGS: dict = {}

def _load_strongs():
    global _STRONGS
    if _STRONGS or not os.path.exists(_LOOKUP_PATH):
        return
    _STRONGS = json.load(open(_LOOKUP_PATH))
# Protestant canon: id -> (name, testament). NT (>=40) anchors Strong's as Greek.
BOOKS = {
 1:"Genesis",2:"Exodus",3:"Leviticus",4:"Numbers",5:"Deuteronomy",6:"Joshua",7:"Judges",
 8:"Ruth",9:"1 Samuel",10:"2 Samuel",11:"1 Kings",12:"2 Kings",13:"1 Chronicles",
 14:"2 Chronicles",15:"Ezra",16:"Nehemiah",17:"Esther",18:"Job",19:"Psalms",20:"Proverbs",
 21:"Ecclesiastes",22:"Song of Solomon",23:"Isaiah",24:"Jeremiah",25:"Lamentations",
 26:"Ezekiel",27:"Daniel",28:"Hosea",29:"Joel",30:"Amos",31:"Obadiah",32:"Jonah",33:"Micah",
 34:"Nahum",35:"Habakkuk",36:"Zephaniah",37:"Haggai",38:"Zechariah",39:"Malachi",
 40:"Matthew",41:"Mark",42:"Luke",43:"John",44:"Acts",45:"Romans",46:"1 Corinthians",
 47:"2 Corinthians",48:"Galatians",49:"Ephesians",50:"Philippians",51:"Colossians",
 52:"1 Thessalonians",53:"2 Thessalonians",54:"1 Timothy",55:"2 Timothy",56:"Titus",
 57:"Philemon",58:"Hebrews",59:"James",60:"1 Peter",61:"2 Peter",62:"1 John",63:"2 John",
 64:"3 John",65:"Jude",66:"Revelation",
}

def strong_prefix(book_id):
    return "G" if int(book_id) >= 40 else "H"

def _enrich(num, prefix):
    """Return [G1198 desmios — prisoner, one in chains] when lookup has the entry."""
    sid   = f"{prefix}{num}"
    entry = _STRONGS.get(sid)
    if not entry:
        return f"[{sid}]"
    parts = []
    if entry.get("translit"):
        parts.append(entry["translit"])
    if entry.get("gloss"):
        parts.append("—")
        parts.append(entry["gloss"])
    return f"[{sid} {' '.join(parts)}]" if parts else f"[{sid}]"

def render_strongs(text, book_id):
    """<S>1234</S> -> [G1234 translit — gloss] (or bare [G1234] if no lookup)."""
    if not isinstance(text, str):
        return ""
    p = strong_prefix(book_id)
    text = re.sub(r"</?i>", "", text)
    text = re.sub(r"\s*<S>(\d+)</S>", lambda m: _enrich(m.group(1), p), text)
    return re.sub(r"\s+", " ", text).strip()

def clean(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"</?i>", "", re.sub(r"<S>\d+</S>", "", text))
    return re.sub(r"\s+", " ", text).strip()

def load_chapter(book_id, chapter):
    cf = os.path.join(ROOT, "docs", "assets", "chapters", f"{book_id}_{chapter}.json")
    if os.path.exists(cf):
        d = json.load(open(cf))
        kjv, web = d.get("KJV", {}), d.get("WEB", {})
        verses = sorted((int(v) for v in kjv.keys()), key=int)
        out = {}
        for v in verses:
            out[str(v)] = {
                "kjv_strongs": render_strongs(kjv.get(str(v), ""), book_id),
                "web": clean(web.get(str(v), "")),
            }
        return out, "chapters (Strong's-tagged)"
    # fallback: verse-cache (no Strong's)
    cache = json.load(open(os.path.join(ROOT, "docs", "assets", "verse-cache.json")))
    keys = sorted((k for k in cache if k.startswith(f"{book_id}_{chapter}_")),
                  key=lambda k: int(k.split("_")[2]))
    out = {}
    for k in keys:
        v = k.split("_")[2]
        out[v] = {"kjv_strongs": clean(cache[k].get("KJV", "")),
                  "web": clean(cache[k].get("WEB", ""))}
    return out, "verse-cache (no Strong's)"

def main():
    if len(sys.argv) != 3:
        sys.exit("usage: mbt-chapter-kit.py <bookId> <chapter>")
    _load_strongs()
    if _STRONGS:
        print(f"Lexicon loaded: {len(_STRONGS)} Strong's entries (enriched tags)")
    else:
        print("Lexicon not found — run bin/mbt-build-lexicon.py first (bare [G####] tags)")
    book_id, chapter = int(sys.argv[1]), int(sys.argv[2])
    verses, src = load_chapter(book_id, chapter)
    if not verses:
        sys.exit(f"no source for {book_id}:{chapter}")
    kit = {
        "book": book_id,
        "bookName": BOOKS.get(book_id, str(book_id)),
        "chapter": chapter,
        "strongLang": strong_prefix(book_id),
        "source": src,
        "verseCount": len(verses),
        "verses": verses,
    }
    outdir = os.path.join(ROOT, "data", "mbt-kits")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"{book_id}_{chapter}.kit.json")
    json.dump(kit, open(outpath, "w"), ensure_ascii=False, indent=1)
    print(f"{kit['bookName']} {chapter}: {len(verses)} verses, source={src}")
    print(f"  -> {outpath}")

if __name__ == "__main__":
    main()
