#!/usr/bin/env python3
"""
strip_leaks.py — Remove prompt-skeleton instruction text that leaked into
published readings, WITHOUT touching real content. Two operations:

  1. TAIL-TRIM: a real section header with an instruction tail appended, e.g.
       "⛏️ Personal Application — Protecting  then four '• ' bulleted concrete actions."
     -> "⛏️ Personal Application — Protecting"
  2. LINE-DROP: a standalone leaked instruction line, e.g.
       "The scripture text of James 4 ONLY. Render only this reference. ..."
       "then 2-4 sentences placing the passage."
       "A line with a single ⸻ character."
       "2-4 paragraphs of reflection in the voice below."
     -> removed entirely.

Intro leaks ("A one-sentence intro.") are handled separately (they need a real
intro written, not just a deletion). Skeleton-only watches are regenerated, not
stripped.

Run:  python3 scripts/strip_leaks.py [--apply]
Default is a dry run (prints planned changes); --apply writes the files.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

TAIL_RE = re.compile(r"\s+then four\s+'[^']*'\s+bulleted concrete actions\.\s*$")
DROP_RES = [
    re.compile(r"^\s*The scripture text of .*ONLY\.\s*Render only this reference.*$"),
    re.compile(r"^\s*then 2-4 sentences placing the passage\.\s*$"),
    re.compile(r"^\s*A line with a single ⸻ character\.\s*$"),
    re.compile(r"^\s*2-4 paragraphs of reflection.*$"),
    re.compile(r"^\s*A line exactly:\s*$"),
]


def process(text):
    out = []
    changes = []
    for ln in text.splitlines():
        if any(r.match(ln) for r in DROP_RES):
            changes.append(("drop", ln.strip()[:70]))
            continue
        m = TAIL_RE.search(ln)
        if m:
            trimmed = ln[:m.start()].rstrip()
            changes.append(("trim", ln.strip()[:70]))
            out.append(trimmed)
            continue
        out.append(ln)
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), changes


def main():
    apply = "--apply" in sys.argv
    total_files = 0
    total_changes = 0
    for p in sorted(READINGS.glob("2026-*.md")):
        text = p.read_text()
        new, changes = process(text)
        if not changes:
            continue
        total_files += 1
        total_changes += len(changes)
        print(f"{p.name}: {len(changes)} change(s)")
        for kind, snip in changes:
            print(f"    {kind}: {snip}")
        if apply:
            p.write_text(new)
    print(f"\n{'APPLIED' if apply else 'DRY RUN'} — {total_changes} changes in {total_files} files")
    if not apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()
