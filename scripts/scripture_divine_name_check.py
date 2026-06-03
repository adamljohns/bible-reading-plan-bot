#!/usr/bin/env python3
"""
scripture_divine_name_check.py — Adjudicate divine-name fidelity in the rendered
scripture of a flagged watch. For each flag it prints, side by side:

  • The KJV reference's divine-name profile for the passage (verse-cache):
    counts of LORD / God / Most High / Almighty / everlasting / Lord GOD.
  • The rendered scripture's profile + the actual rendered text.

This tells real drift (KJV has 'the LORD' where the rendering substituted an
epithet, or dropped it for 'God') from a false positive (the Hebrew genuinely
has Elyon/Shaddai/El-Olam alongside YHWH).

USAGE
  python3 scripts/scripture_divine_name_check.py            # all current A flags
  python3 scripts/scripture_divine_name_check.py 2026-06-01 # one date
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import history_candidates as HC
from build_reading_index import split_watches

VC = json.loads((REPO / "docs/assets/verse-cache.json").read_text())
AUDIT = json.loads((REPO / "data/readings-audit.json").read_text())

BOOKS = HC.__dict__  # not used; use audit's flags directly
NAME_PATS = {
    "LORD": r"\bLORD\b",
    "Lord GOD": r"\bLord GOD\b",
    "God": r"\bGod\b",
    "Most High": r"[Mm]ost\s+[Hh]igh",
    "Almighty": r"[Aa]lmighty",
    "everlasting": r"[Ee]verlasting",
    "Eternal": r"[Ee]ternal",
}
# bookId map for ref parsing
BMAP = {
    "genesis":1,"exodus":2,"leviticus":3,"numbers":4,"deuteronomy":5,"joshua":6,
    "judges":7,"ruth":8,"1 samuel":9,"2 samuel":10,"1 kings":11,"2 kings":12,
    "1 chronicles":13,"2 chronicles":14,"ezra":15,"nehemiah":16,"esther":17,
    "job":18,"psalm":19,"psalms":19,"proverbs":20,"ecclesiastes":21,
    "song of solomon":22,"isaiah":23,"jeremiah":24,"lamentations":25,"ezekiel":26,
    "daniel":27,"hosea":28,"joel":29,"amos":30,"obadiah":31,"jonah":32,"micah":33,
    "nahum":34,"habakkuk":35,"zephaniah":36,"haggai":37,"zechariah":38,"malachi":39,
}
REF_RE = re.compile(r"([1-3]?\s?[A-Za-z][A-Za-z ]+?)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?")


def kjv_for(ref):
    out = []
    for m in REF_RE.finditer(ref):
        book = re.sub(r"\s+", " ", m.group(1).strip().lower())
        bid = BMAP.get(book)
        if not bid:
            continue
        ch, v1 = int(m.group(2)), int(m.group(3))
        v2 = int(m.group(4)) if m.group(4) else v1
        for v in range(v1, v2 + 1):
            out.append(VC.get(f"{bid}_{ch}_{v}", {}).get("KJV", ""))
    return " ".join(out)


def profile(text):
    return {k: len(re.findall(p, text)) for k, p in NAME_PATS.items()}


def rendered_scripture(ds, wk):
    md = (REPO / "data/readings" / f"{ds}.md").read_text()
    w = split_watches(md).get(wk, "")
    lines = w.splitlines()
    out, grab = [], False
    for ln in lines:
        if re.match(r"\s*📖\s*Scripture", ln):
            grab = True
            continue
        if grab:
            if re.match(r"\s*⸻", ln) or re.match(r"\s*(🧭|🛡|🗺|🛰|❤|👨|🌾)", ln):
                break
            if ln.strip():
                out.append(ln.strip())
    return " ".join(out)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    flags = AUDIT["A_scripture_fidelity"]["flags"]
    for f in flags:
        if only and f["date"] != only:
            continue
        ds, wk, ref = f["date"], f["watch"], f["ref"]
        kjv = kjv_for(ref)
        rend = rendered_scripture(ds, wk)
        kp = {k: v for k, v in profile(kjv).items() if v}
        rp = {k: v for k, v in profile(rend).items() if v}
        verdict = "??"
        # Heuristic verdict
        if kp.get("LORD", 0) and not rp.get("LORD", 0):
            verdict = "LIKELY DRIFT (KJV has LORD, rendering 0)"
        elif rp.get("Most High", 0) or rp.get("Almighty", 0) or rp.get("everlasting", 0):
            kjv_has_epithet = kp.get("Most High", 0) or kp.get("Almighty", 0) or kp.get("everlasting", 0)
            verdict = "likely OK (KJV also has epithet)" if kjv_has_epithet else "CHECK (epithet not in KJV)"
        print(f"\n=== {ds} [{wk}] {ref} — {verdict}")
        print(f"  KJV   : {kp}")
        print(f"  RENDER: {rp}")
        print(f"  rendered: {rend[:240]}")


if __name__ == "__main__":
    main()
