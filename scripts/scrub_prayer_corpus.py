#!/usr/bin/env python3
"""scrub_prayer_corpus.py — Mechanical prayer/charge/apps scrub (PJG-0810-PRAYSWEEP1).

Rewrites data/readings/<date>.md in place:
  - Prayer headers → 🙏 Prayer
  - Helm/Rudder/Course Set → 🛡️ Watch Charge:
  - One-title close rotation per watch
  - Strip Brother Adam / this father
  - First-personize common corporate prayer openers/closes
  - Cap application bullets at 3
  - Boaz fourteen → fifteen (age lock as of 2026-08-10+)
  - Fix Maria headship muddle line
  - Drop prototype stamp is handled at JSON rebuild (not MD)

Then optionally rebuild index/html for touched dates.

USAGE
  python3 scripts/scrub_prayer_corpus.py --range 2026-08-10 2026-08-24
  python3 scripts/scrub_prayer_corpus.py 2026-08-10 --rebuild
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

CLOSES = {
    "wisdom": "In Jesus' name, I pray. Amen.",
    "first": "In the name of Jesus Christ, I pray. Amen.",
    "second": "Through Christ my Savior, I pray. Amen.",
    "third": "In the name of the risen Lord Jesus, I pray. Amen.",
    "peace": "For the sake of Christ our King, I pray. Amen.",
}

WATCH_KEY = {
    "🌅": "wisdom",
    "🕖": "first",
    "🕚": "second",
    "🕒": "third",
    "🌙": "peace",
}

SPLIT = re.compile(r"\n(?=🌅|🕖|🕚|🕒|🌙)")


def iter_dates(args: list[str]) -> list[str]:
    out: list[str] = []
    if "--range" in args:
        i = args.index("--range")
        s = date.fromisoformat(args[i + 1])
        e = date.fromisoformat(args[i + 2])
        cur = s
        while cur <= e:
            out.append(cur.isoformat())
            cur += timedelta(days=1)
    for a in args:
        if re.match(r"\d{4}-\d{2}-\d{2}$", a):
            if a not in out:
                out.append(a)
    return out


def strip_apps_over_three(sec: str) -> str:
    """Keep first 3 application bullets in each Personal Application block."""
    lines = sec.splitlines(keepends=True)
    out = []
    in_apps = False
    bullets = 0
    for ln in lines:
        if re.search(r"Personal Application", ln):
            in_apps = True
            bullets = 0
            out.append(ln)
            continue
        if in_apps:
            if re.match(r"^[•\-\*]\s+", ln):
                bullets += 1
                if bullets <= 3:
                    out.append(ln)
                continue
            if ln.strip() == "":
                out.append(ln)
                continue
            # left apps block
            in_apps = False
            out.append(ln)
            continue
        out.append(ln)
    return "".join(out)


def rewrite_prayer_block(pray_body: str, watch_key: str) -> str:
    t = pray_body.strip()
    # Drop leading bullet if model put • before Father
    t = re.sub(r"^•\s*", "", t)
    t = t.replace("Grant me, Brother Adam,", "Grant me")
    t = t.replace("Grant me, Brother Adam", "Grant me")
    t = re.sub(r"\bBrother Adam,\s*", "", t)
    t = re.sub(r"\bBrother Adam\b", "", t)
    t = re.sub(r"\bgive this father\b", "give me", t, flags=re.I)
    t = re.sub(r"\bthis father\b", "me", t, flags=re.I)

    # Corporate → personal (common patterns; imperfect but stops the ear-ban)
    reps = [
        (r"\bwe thank You\b", "I thank You"),
        (r"\bWe thank You\b", "I thank You"),
        (r"\bwe ask that You\b", "I ask that You"),
        (r"\bWe ask that You\b", "I ask that You"),
        (r"\bwe ask You\b", "I ask You"),
        (r"\bGrant us\b", "Grant me"),
        (r"\bgrant us\b", "grant me"),
        (r"\bKeep us\b", "Keep me"),
        (r"\bkeep us\b", "keep me"),
        (r"\bstrengthen our hands\b", "strengthen my hands"),
        (r"\bfirm our knees\b", "firm my knees"),
        (r"\bour daily duties\b", "my daily duties"),
        (r"\blead our homes\b", "lead my home"),
        (r"\bfather our children\b", "father my children"),
        (r"\bserve our community\b", "serve my community"),
        (r"\banchor our hearts\b", "anchor my heart"),
        (r"\bour hearts\b", "my heart"),
        (r"\bour flesh\b", "my flesh"),
        (r"\bour fevers\b", "my fevers"),
        (r"\bwho redeemed us\b", "who redeemed me"),
        (r"\bso that we may\b", "so that I may"),
        (r"\bas we face\b", "as I face"),
        (r"\bthat we might\b", "that I might"),
        (r"\bwe may\b", "I may"),
        (r"\bwe might\b", "I might"),
        (r",\s*we pray\.?\s*Amen\.?", ". Amen."),
        (r"\bwe pray\.?\s*Amen\.?", "I pray. Amen."),
    ]
    for a, b in reps:
        t = re.sub(a, b, t)

    close = CLOSES[watch_key]
    # Hard strip any prior close tail (Commander / Name-stack / Amen)
    t = re.sub(
        r"(?:In the name of|In Jesus|Through Christ|For the sake of)[\s\S]*$",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(r"\bmy Lord and Commander\b[^.]*\.??", "", t, flags=re.I)
    t = re.sub(r"\bmy Lord Jesus Christ\b[^.]*\.??", "", t, flags=re.I)
    t = re.sub(r"\s*Amen\.?\s*$", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip().rstrip(" ,;")
    if t and t[-1] not in ".!?":
        t += "."
    t = t + " " + close
    return t


def scrub_section(sec: str) -> str:
    if not sec.strip():
        return sec
    emoji = sec.lstrip()[:1]
    watch_key = WATCH_KEY.get(emoji)
    if not watch_key:
        return sec

    # Headers / charges
    sec = re.sub(r"🙏\s*Prayer from the (?:Stateroom|Wardroom|Bridge|Helm)\s*",
                 "🙏 Prayer\n", sec)
    sec = re.sub(r"^🙏\s*Prayer\s*$", "🙏 Prayer", sec, flags=re.M)
    sec = re.sub(r"⚓\s*Helm Command:\s*", "🛡️ Watch Charge: ", sec)
    sec = re.sub(r"⚓\s*Rudder Steer:\s*", "🛡️ Watch Charge: ", sec)
    sec = re.sub(r"⚓\s*Course Set:\s*", "🛡️ Watch Charge: ", sec)
    sec = re.sub(r"⚓\s*Watch Charge:\s*", "🛡️ Watch Charge: ", sec)
    sec = re.sub(r"🛡️\s*The Charge:\s*", "🛡️ Watch Charge: ", sec)

    # Maria muddle
    sec = re.sub(
        r"As the head of your home,\s*Maria,\s*you are under the covering of Christ’s authority,\s*"
        r"and you are under the covering of your husband’s godly protection\.",
        "As the head of your home, you stand under Christ’s authority, and Maria rests under the covering of your godly protection.",
        sec,
        flags=re.I,
    )
    sec = re.sub(
        r"As the head of your home,\s*Maria,",
        "As the head of your home, brother,",
        sec,
        flags=re.I,
    )

    # Boaz age
    sec = re.sub(r"\bBoaz,\s*at fourteen\b", "Boaz, at fifteen", sec)
    sec = re.sub(r"\bBoaz\s*\(14\)", "Boaz (15)", sec)
    sec = re.sub(r"\bfourteen-year-old Boaz\b", "fifteen-year-old Boaz", sec, flags=re.I)

    sec = strip_apps_over_three(sec)

    def _sub_pray(m: re.Match) -> str:
        body = m.group(1)
        new_body = rewrite_prayer_block(body, watch_key)
        return "🙏 Prayer\n\n" + new_body + "\n"

    sec = re.sub(
        r"🙏[^\n]*\n([\s\S]*?)(?=\n(?:🛡️ Watch Charge:|⚓|⸻⸻|⸻\s*$|---|\Z))",
        _sub_pray,
        sec,
        count=1,
    )
    return sec


def scrub_file(path: Path) -> bool:
    orig = path.read_text(encoding="utf-8")
    # Keep preamble (before first watch)
    parts = SPLIT.split(orig)
    if len(parts) <= 1:
        return False
    new_parts = [parts[0]] + [scrub_section(p) for p in parts[1:]]
    # Re-join with single leading newline already on split parts
    out = new_parts[0]
    if not out.endswith("\n"):
        out += "\n"
    for p in new_parts[1:]:
        if not p.startswith("\n"):
            out += "\n"
        out += p if p.endswith("\n") else p + "\n"
    if out != orig:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def rebuild(ds: str) -> None:
    subprocess.run(
        [sys.executable, "scripts/build_reading_index.py", "scrub", "--date", ds],
        cwd=REPO, check=False,
    )
    subprocess.run(
        [sys.executable, "scripts/build_reading_page_from_md.py", ds],
        cwd=REPO, check=False,
    )


def main() -> int:
    args = sys.argv[1:]
    do_rebuild = "--rebuild" in args
    dates = iter_dates(args)
    if not dates:
        print(__doc__)
        return 1
    changed = []
    for ds in dates:
        p = READINGS / f"{ds}.md"
        if not p.exists():
            print(f"MISS {ds}")
            continue
        if scrub_file(p):
            print(f"SCRUBBED {ds}")
            changed.append(ds)
            if do_rebuild:
                rebuild(ds)
        else:
            print(f"unchanged {ds}")
    print(f"done changed={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
