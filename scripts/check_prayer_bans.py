#!/usr/bin/env python3
"""check_prayer_bans.py — Pre-ship gate for daily readings (PJG-0810-PRAYSWEEP1).

Refuse publish when any of these hit in MD (or optional JSON text fields):
  - my Lord Jesus Christ / my Lord and Commander / Name-stack close
  - Brother Adam inside 🙏 Prayer
  - subject we/us/our patterns in prayer (we thank/we pray/Grant us/this father)
  - apps > 3 per watch
  - Course Set / Helm Command / Rudder Steer / Stateroom|Wardroom|Bridge prayer labels
  - Maria-as-head muddle: "As the head of your home, Maria"

USAGE
  python3 scripts/check_prayer_bans.py 2026-08-10
  python3 scripts/check_prayer_bans.py 2026-08-10 2026-08-24
  python3 scripts/check_prayer_bans.py --range 2026-08-10:2026-08-24
Exit 0 = clean. Exit 2 = ban hits (print reasons). Exit 1 = usage/IO.
"""
from __future__ import annotations

import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

GLOBAL_BANS = [
    ("name_stack", re.compile(r"my Lord Jesus Christ", re.I)),
    ("commander_close", re.compile(r"my Lord and Commander", re.I)),
    ("double_christ_close", re.compile(
        r"Jesus Christ,\s*my Lord(?:\s+Jesus)?(?:\s+Christ)?", re.I)),
    ("helm", re.compile(r"\bHelm Command\b")),
    ("rudder", re.compile(r"\bRudder Steer\b")),
    ("course_set", re.compile(r"\bCourse Set\b")),
    ("naval_prayer_hdr", re.compile(
        r"Prayer from the (?:Stateroom|Wardroom|Bridge|Helm)")),
    ("maria_head", re.compile(r"As the head of your home,\s*Maria", re.I)),
    ("watch_charge_anchor", re.compile(r"⚓\s*Watch Charge")),
]

PRAYER_BANS = [
    ("brother_adam", re.compile(r"\bBrother Adam\b")),
    ("vocative_adam", re.compile(r"\bGrant me,\s*Adam\b|\bAdam,\s+the courage", re.I)),
    ("this_father", re.compile(r"\bthis father\b", re.I)),
    ("we_thank", re.compile(r"\bwe thank\b", re.I)),
    ("we_ask", re.compile(r"\bwe ask\b", re.I)),
    ("we_pray", re.compile(r"\bwe pray\b", re.I)),
    ("grant_us", re.compile(r"\bGrant us\b")),
    ("our_homes_subj", re.compile(r"\bstrengthen our\b|\bkeep us\b|\bour hearts\b", re.I)),
]

WATCH_SPLIT = re.compile(r"\n(?=🌅|🕖|🕚|🕒|🌙)")
PRAYER_BLOCK = re.compile(
    r"🙏[^\n]*\n([\s\S]*?)(?=\n(?:🛡️ Watch Charge|⚓|⸻|---|🌅|🕖|🕚|🕒|🌙)|\Z)"
)
APP_BULLET = re.compile(r"^[•\-\*]\s+\S", re.M)


def iter_dates(args: list[str]) -> list[str]:
    out: list[str] = []
    for a in args:
        if a.startswith("--range"):
            continue
        if a.startswith("--"):
            continue
        if ":" in a and re.match(r"\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$", a):
            s, e = a.split(":")
            cur = date.fromisoformat(s)
            end = date.fromisoformat(e)
            while cur <= end:
                out.append(cur.isoformat())
                cur += timedelta(days=1)
        elif re.match(r"\d{4}-\d{2}-\d{2}$", a):
            out.append(a)
    # --range S E form
    if "--range" in args:
        i = args.index("--range")
        if i + 2 < len(args):
            s, e = args[i + 1], args[i + 2]
            if ":" not in s:
                cur = date.fromisoformat(s)
                end = date.fromisoformat(e)
                while cur <= end:
                    ds = cur.isoformat()
                    if ds not in out:
                        out.append(ds)
                    cur += timedelta(days=1)
    return sorted(set(out))


def check_md(path: Path) -> list[str]:
    hits: list[str] = []
    text = path.read_text(encoding="utf-8")
    for name, rx in GLOBAL_BANS:
        if rx.search(text):
            hits.append(f"{path.name}:GLOBAL:{name}")
    for sec in WATCH_SPLIT.split(text):
        if not sec.strip():
            continue
        head = sec.splitlines()[0][:40] if sec.splitlines() else "?"
        # apps — only bullets under Personal Application (reflection may use •)
        if not head.startswith("🌙"):
            n_apps = 0
            in_apps = False
            for ln in sec.splitlines():
                if re.search(r"Personal Application", ln):
                    in_apps = True
                    continue
                if in_apps:
                    if APP_BULLET.match(ln):
                        n_apps += 1
                        continue
                    if ln.strip() == "":
                        continue
                    if re.match(r"^(🙏|🛡️|⚓|⸻|🦅)", ln):
                        break
                    # non-bullet ends apps block
                    break
            if n_apps > 3:
                hits.append(f"{path.name}:{head}:apps={n_apps}>3")
        for pm in PRAYER_BLOCK.finditer(sec):
            pray = pm.group(1)
            for name, rx in PRAYER_BANS:
                if rx.search(pray):
                    hits.append(f"{path.name}:{head}:PRAYER:{name}")
            # Name-stack inside prayer close region
            if re.search(r"my Lord Jesus Christ|my Lord and Commander", pray, re.I):
                hits.append(f"{path.name}:{head}:PRAYER:close_ban")
            if re.search(r"Jesus Christ,.+(?:Lord Jesus|my Lord)", pray, re.I):
                hits.append(f"{path.name}:{head}:PRAYER:double_title")
    return hits


def main() -> int:
    args = [a for a in sys.argv[1:] if a not in ("-h", "--help")]
    if not args:
        print(__doc__, file=sys.stderr)
        return 1
    dates = iter_dates(sys.argv[1:])
    if not dates:
        print("No dates parsed", file=sys.stderr)
        return 1
    all_hits: list[str] = []
    missing = 0
    for ds in dates:
        p = READINGS / f"{ds}.md"
        if not p.exists():
            print(f"MISS {ds}", flush=True)
            missing += 1
            continue
        hits = check_md(p)
        if hits:
            print(f"FAIL {ds} ({len(hits)})", flush=True)
            for h in hits:
                print(f"  - {h}", flush=True)
            all_hits.extend(hits)
        else:
            print(f"PASS {ds}", flush=True)
    if missing and not all_hits:
        return 1
    if all_hits:
        print(f"\nREFUSE publish: {len(all_hits)} ban hit(s) across "
              f"{len({h.split(':')[0] for h in all_hits})} file(s)", flush=True)
        return 2
    print("ALL CLEAN", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
