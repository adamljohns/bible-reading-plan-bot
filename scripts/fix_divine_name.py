#!/usr/bin/env python3
"""
fix_divine_name.py — Restore the small-caps covenant name "the LORD" (YHWH) in
the SCRIPTURE BLOCK of flagged watches, where the rendering used plain "the Lord"
or substituted an epithet.

Only operates inside the 📖 Scripture block (never the reflection/prose), and
only on dates passed in. Conservative replacements:
  • "the Lord" -> "the LORD", "The Lord" -> "The LORD"   (YHWH in OT passages)
  • but PRESERVE "Lord GOD" / "Lord God" handled as "LORD God" (YHWH Elohim),
    and never touch "Lord Jesus", "my lord", lowercase "lord".
Word-substitution fixes (epithet used for YHWH) are passed explicitly per date.

USAGE
  python3 scripts/fix_divine_name.py --dry 2026-01-07 2026-01-10 ...
  python3 scripts/fix_divine_name.py --apply 2026-01-07 ...
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))
from build_reading_index import split_watches, _classify_line

# Per-date explicit word-substitution fixes (epithet -> the LORD) where the
# original Hebrew is YHWH, not Elyon/Shaddai. Verified case by case.
WORD_SUBS = {
    "2026-06-01": [("the law of the Most High", "the law of the LORD")],
}


def fix_scripture_block(text, date):
    """Return (new_text, n_changes) operating only on lines inside the
    📖 Scripture block of a single watch's text."""
    lines = text.splitlines()
    out = []
    n = 0
    in_scrip = False
    for ln in lines:
        if re.match(r"\s*📖\s*Scripture", ln):
            in_scrip = True
            out.append(ln)
            continue
        if in_scrip:
            # block ends at a separator or the next section emoji
            if re.match(r"\s*⸻", ln) or re.match(r"\s*(🧭|🛡|🗺|🛰|❤|👨|🌾|🙏|⚓|⛏)", ln):
                in_scrip = False
                out.append(ln)
                continue
            new = ln
            # explicit word-subs first
            for a, b in WORD_SUBS.get(date, []):
                if a in new:
                    new = new.replace(a, b); n += 1
            # "Lord GOD"/"Lord God" -> "LORD God" (YHWH Elohim) — do BEFORE generic
            new2 = re.sub(r"\b([Tt]he )Lord God\b", lambda m: m.group(1) + "LORD God", new)
            # generic "the Lord" -> "the LORD" but NOT "Lord Jesus", "Lord GOD", possessive
            new2 = re.sub(r"\b([Tt]he )Lord\b(?!\s+(GOD|Jesus|Christ|God))", lambda m: m.group(1) + "LORD", new2)
            if new2 != ln:
                n += new2.count("LORD") - ln.count("LORD") if new2.count("LORD") > ln.count("LORD") else 1
            out.append(new2)
        else:
            out.append(ln)
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), n


def main():
    apply = "--apply" in sys.argv
    dry = "--dry" in sys.argv or not apply
    dates = [a for a in sys.argv[1:] if re.match(r"\d{4}-\d{2}-\d{2}", a)]
    total = 0
    for ds in dates:
        p = READINGS / f"{ds}.md"
        md = p.read_text()
        watches = split_watches(md)
        # apply to every watch's scripture block on this date (flags can be any watch)
        new_md = md
        changed = 0
        for wk, wtext in watches.items():
            fixed, n = fix_scripture_block(wtext, ds)
            if n and fixed != wtext:
                new_md = new_md.replace(wtext, fixed, 1)
                changed += n
        if changed:
            total += changed
            print(f"  {ds}: {changed} LORD restoration(s)")
            if dry:
                # show a sample changed line
                for a, b in WORD_SUBS.get(ds, []):
                    print(f"     word-sub: {a} -> {b}")
            if apply:
                p.write_text(new_md)
                subprocess.run([sys.executable, "scripts/build_reading_index.py",
                                "divine-name", "--date", ds], cwd=REPO, capture_output=True)
        else:
            print(f"  {ds}: no change")
    print(f"\n{'APPLIED' if apply else 'DRY'} — {total} restorations across {len(dates)} dates")


if __name__ == "__main__":
    main()
