#!/usr/bin/env python3
"""
apply_history_blocks.py — Splice subagent-authored, fact-verified history blocks
back into the readings and rebuild their JSON.

Input: data/history-fixes/<MM>.json, a list of
  {"date":"2026-MM-DD", "block":"<2-4 sentence prose>", "events":[{"year","fact"}]}

For each entry it replaces the day's "🦅 This Day in American History — ..." block
with the new prose (header preserved, regenerated from the date), then rebuilds
that day's per-day JSON.

USAGE
  python3 scripts/apply_history_blocks.py 03            # apply data/history-fixes/03.json
  python3 scripts/apply_history_blocks.py 03 --dry      # show, no write
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from fix_history_day import splice, MONTHNAME

FIXES = REPO / "data" / "history-fixes"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    if not args:
        sys.exit("usage: apply_history_blocks.py MM [--dry]")
    mm = args[0].zfill(2)
    data = json.loads((FIXES / f"{mm}.json").read_text())
    applied = 0
    for e in data:
        ds = e["date"]
        block = e["block"].strip()
        # basic sanity: must mention at least one 4-digit year and be prose
        import re
        if not re.search(r"\b(1[6-9]\d\d|20[0-2]\d)\b", block):
            print(f"  {ds}: SKIP — block has no year")
            continue
        dd = ds[8:10]
        if dry:
            print(f"  {ds}: {block[:90]}...")
            continue
        ok = splice(ds, MONTHNAME[int(mm)], dd, block)
        if ok:
            subprocess.run([sys.executable, "scripts/build_reading_index.py",
                            "histfix", "--date", ds], cwd=REPO, capture_output=True)
            applied += 1
            print(f"  {ds}: ✓")
        else:
            print(f"  {ds}: FAIL — no history header found")
    print(f"\nApplied {applied}/{len(data)} blocks for {mm}.")


if __name__ == "__main__":
    main()
