#!/usr/bin/env python3
"""
refresh_closers.py — Diversify formulaic Helm Command / Rudder Steer closers.

~27% of watch closers are built from the same stock phrases ("hold the line",
"hold fast", "tide/wave of compromise", "breach your deck"). This regenerates
each such closer as ONE fresh imperative GROUNDED in that watch's own scripture
and reflection, via the local model, with a banned-phrase + dedup gate so we
don't trade one cliché for another.

USAGE
  python3 scripts/refresh_closers.py --test 8       # regenerate 8, print, no write
  python3 scripts/refresh_closers.py --apply        # all formulaic closers
  python3 scripts/refresh_closers.py --apply 2026-06-01 2026-06-30   # date range
"""
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))
import generate_reading_local as G
from build_reading_index import split_watches

MODEL, PORT = "qwen3.6-35b-a3b", "1235"
STOCK = re.compile(r"hold (the|your) line|hold fast|tide of compromise|wave of compromise|"
                   r"hold the wall|breach your deck|no wave of", re.I)
CLOSER_RE = re.compile(r"^(\s*⚓\s*(?:Helm Command|Rudder Steer)\s*[:：]\s*)(.+?)\s*$")
BANNED = re.compile(r"hold (the|your) line|hold fast|tide of|wave of|breach your deck|"
                    r"compromise|stand firm in the truth|sword of the spirit", re.I)
_seen = set()


def watch_parts(wt):
    scrip, refl, closer_line_idx, label = [], [], None, None
    lines = wt.splitlines()
    in_s = in_r = False
    for i, ln in enumerate(lines):
        if re.match(r"\s*📖\s*Scripture", ln): in_s = True; continue
        if re.match(r"\s*(🛡|❤|👨|🌾).*Reflection", ln): in_r = True; in_s = False; continue
        if re.match(r"\s*(⸻|⛏|🙏|⚓|🦅|🧭|🗺|🛰)", ln): in_s = False; in_r = False
        if in_s and ln.strip(): scrip.append(ln.strip())
        if in_r and ln.strip(): refl.append(ln.strip())
    return " ".join(scrip)[:280], " ".join(refl)[:280]


def gen_closer(label, scrip, refl):
    sysmsg = ("You write a single closing imperative for one watch of a Reformed devotional "
              "for men. Output ONLY the one-sentence command, nothing else.")
    user = (f"Watch passage (excerpt): {scrip}\n"
            f"Reflection (excerpt): {refl}\n\n"
            f"Write ONE fresh '{label}' — a vivid nautical, military, watchman, forge, or "
            f"harvest command drawn from the SPECIFIC imagery of THIS passage. Direct, masculine, "
            f"reverent; you may address the reader as 'brother'. BANNED (never use): 'hold the "
            f"line', 'hold fast', 'tide of compromise', 'wave of compromise', 'breach your deck', "
            f"'stand firm in the truth', 'sword of the Spirit'. Make it specific to this text, not "
            f"a stock phrase. One sentence ending in a period.")
    msgs = [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}]
    for _ in range(4):
        try:
            out = G.call_llm(msgs, MODEL, PORT, max_tokens=80, temperature=0.8).strip()
        except Exception:
            continue
        out = re.sub(r"<think>.*?</think>", "", out, flags=re.DOTALL).strip()
        out = out.strip().strip('"').splitlines()[0].strip() if out else ""
        # match the project standard: covenant name in small-caps
        out = re.sub(r"\b([Tt]he )Lord\b(?!\s+(Jesus|Christ|God|GOD))", lambda m: m.group(1) + "LORD", out)
        out = out.replace("Lord’s", "LORD’s").replace("Lord's", "LORD's")
        if out and not out.endswith((".", "!")):
            out += "."
        key = out.lower()
        if out and 20 <= len(out) <= 170 and not BANNED.search(out) and key not in _seen:
            _seen.add(key)
            return out
    return None


def process(ds, test=False):
    p = READINGS / f"{ds}.md"
    if not p.exists():
        return 0
    md = p.read_text()
    new_md = md
    changed = 0
    for wk, wt in split_watches(md).items():
        for ln in wt.splitlines():
            m = CLOSER_RE.match(ln)
            if not m or not STOCK.search(m.group(2)):
                continue
            scrip, refl = watch_parts(wt)
            fresh = gen_closer("Rudder Steer" if "Rudder" in m.group(1) else "Helm Command", scrip, refl)
            if not fresh:
                print(f"    {ds} [{wk}]: gen failed, keeping")
                continue
            newln = m.group(1) + fresh
            if test:
                print(f"    {ds} [{wk}]\n       OLD: {m.group(2)}\n       NEW: {fresh}")
            else:
                new_md = new_md.replace(ln, newln, 1)
            changed += 1
    if not test and changed:
        p.write_text(new_md)
        subprocess.run([sys.executable, "scripts/build_reading_index.py", "closers", "--date", ds],
                       cwd=REPO, capture_output=True)
        print(f"  {ds}: {changed} closer(s) refreshed")
    return changed


def main():
    test_n = int(sys.argv[sys.argv.index("--test") + 1]) if "--test" in sys.argv else 0
    apply = "--apply" in sys.argv
    dates_args = [a for a in sys.argv[1:] if re.match(r"\d{4}-\d{2}-\d{2}", a)]
    all_days = sorted(p.stem for p in READINGS.glob("2026-*.md"))
    if len(dates_args) == 2:
        s, e = date.fromisoformat(dates_args[0]), date.fromisoformat(dates_args[1])
        all_days = [d for d in all_days if s <= date.fromisoformat(d) <= e]
    total = 0
    done = 0
    for ds in all_days:
        if test_n and done >= test_n:
            break
        n = process(ds, test=bool(test_n))
        total += n
        if n:
            done += n
    print(f"\n{'TEST' if test_n else ('APPLIED' if apply else 'DRY')} — {total} closers")


if __name__ == "__main__":
    main()
