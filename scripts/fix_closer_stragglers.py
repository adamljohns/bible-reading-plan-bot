#!/usr/bin/env python3
"""Regenerate the handful of closers that still OPEN with a stock phrase
("Anchor ...", "Steadfastly anchor ...") or contain the banned "hold the line"
cliche — the diversify run's "no fresh opener" keeps. Small, targeted."""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))
from build_reading_index import split_watches
from refresh_closers import watch_parts, CLOSER_RE
import diversify_closers as D

STOCK = re.compile(r"^(Anchor|Steadfastly|Drop the anchor|Cast the anchor)\b|"
                   r"hold (the|your) line|tide of compromise", re.I)

# seed cap with current opener distribution so new lines stay spread
running = Counter()
targets = []
for p in sorted(READINGS.glob("2026-*.md")):
    for wk, wt in split_watches(p.read_text()).items():
        for ln in wt.splitlines():
            m = CLOSER_RE.match(ln)
            if m:
                running[D.opener(m.group(2))] += 1
                if STOCK.search(m.group(2)):
                    targets.append((p.stem, wk, ln, m.group(2)))

print(f"stragglers: {len(targets)}", flush=True)
for ds, wk, line, old in targets:
    wt = split_watches((READINGS / f"{ds}.md").read_text())[wk]
    scrip, refl = watch_parts(wt)
    label = "Rudder Steer" if "Rudder" in line else "Helm Command"
    avoid = {"anchor", "steadfastly", "hold", "drop", "cast"}
    new = None
    for _ in range(8):
        try:
            cand = D.gen(label, scrip, refl, avoid)
        except Exception:
            continue
        if not cand or D.BANNED.search(cand) or not (20 <= len(cand) <= 175):
            continue
        op = D.opener(cand)
        if running[op] >= D.CAP:
            avoid.add(op.split()[0]); continue
        new = cand; break
    if not new:
        print(f"  {ds} [{wk}]: still no fresh opener", flush=True); continue
    running[D.opener(new)] += 1
    md = (READINGS / f"{ds}.md").read_text().replace(line, line.replace(old, new), 1)
    (READINGS / f"{ds}.md").write_text(md)
    subprocess.run([sys.executable, "scripts/build_reading_index.py", "straggler", "--date", ds],
                   capture_output=True)
    print(f"  {ds} [{wk}]: {new}", flush=True)
print("done", flush=True)
