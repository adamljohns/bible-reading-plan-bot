#!/usr/bin/env python3
"""Remove WITHIN-watch duplicate Personal Application bullets — 24 watches were
generated with their 4 bullets doubled (08-02 tripled), a concatenation artifact.
Deterministic: keep the first occurrence of each bullet text inside a watch,
drop later exact copies. Resets per watch at the between-watch separator so an
identical generic bullet in two different watches is left alone.

USAGE
  python3 scripts/dedupe_bullets.py --dry
  python3 scripts/dedupe_bullets.py --apply
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
SEP_RE = re.compile(r"^\s*⸻{4,}\s*$")          # between-watch separator
BULLET_RE = re.compile(r"^(\s*•\s+)(.+\S)\s*$")


def dedupe(md):
    out, seen, dropped = [], set(), 0
    for ln in md.splitlines():
        if SEP_RE.match(ln):
            seen.clear()
            out.append(ln)
            continue
        m = BULLET_RE.match(ln)
        if m:
            key = m.group(2).strip().lower()
            if key in seen:
                dropped += 1
                continue            # drop the duplicate copy
            seen.add(key)
        out.append(ln)
    return "\n".join(out) + ("\n" if md.endswith("\n") else ""), dropped


def main():
    apply = "--apply" in sys.argv
    total_dropped = total_files = 0
    for p in sorted(READINGS.glob("2026-*.md")):
        md = p.read_text()
        new, dropped = dedupe(md)
        if dropped:
            total_dropped += dropped
            total_files += 1
            print(f"  {p.stem}: -{dropped} duplicate bullet(s)")
            if apply:
                p.write_text(new)
                subprocess.run([sys.executable, "scripts/build_reading_index.py", "dedupe",
                                "--date", p.stem], cwd=REPO, capture_output=True)
    print(f"\n{'APPLIED' if apply else 'DRY'} — removed {total_dropped} duplicate bullets "
          f"in {total_files} watches/days")


if __name__ == "__main__":
    main()
