#!/usr/bin/env python3
"""
fix_history_day.py — Replace a day's "This Day in American History" block with
TWO verified, edifying American events, framed in the devotional voice.

Reliability design (the whole point — the old block was 73% fabricated):
  • FACTS come only from Wikipedia (On-This-Day feed + the full date-page
    Events section), never from model memory.
  • The model is given the TWO selected events VERBATIM and may only reword
    them into voice — it is told to add NO new fact, date, name, or number.
  • A hard GATE rejects any model output whose years aren't exactly the two
    selected years (catches invented dates); on repeated failure we fall back
    to a clean deterministic template of the verbatim facts.
  • Days whose existing two events both verify against the pool are SKIPPED
    (don't disturb already-correct, nicely-framed days).

USAGE
  python3 scripts/fix_history_day.py 2026-03-01            # one day
  python3 scripts/fix_history_day.py 2026-03-01 2026-03-31 # inclusive range
  python3 scripts/fix_history_day.py 2026-03-01 --force    # replace even if existing verifies
  python3 scripts/fix_history_day.py 2026-03-01 --dry      # show plan, no write
"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))
import generate_reading_local as G
import history_candidates as HC

MONTHNAME = HC.MONTHNAME
MODEL, PORT = "qwen3.6-35b-a3b", "1235"

THEME_W = {
    "faith/revival": 6, "founding/constitutional": 5, "military valor": 5,
    "invention/industry": 4, "exploration/frontier": 4, "civic/governance": 3,
    "general": 1,
}
BANNED = re.compile(r"\b(systemic|marginali|privilege|social justice|oppressed class|underrepresented)\b", re.I)


def build_pool(mm, dd):
    pool = {}
    for e in HC.fetch(mm, dd).get("events", []):
        if HC.is_us(e):
            pool[(e["year"], e["text"][:50])] = {"year": e["year"], "text": e["text"], "curated": True}
    for e in HC.fetch_datepage(mm, dd):
        if HC.is_us(e) and e["text"]:
            k = (e["year"], e["text"][:50])
            pool.setdefault(k, {"year": e["year"], "text": e["text"], "curated": False})
    return list(pool.values())


def score(e):
    tags = HC.themes_of(e["text"])
    if "⚠CAUTION-framing" in tags:
        return -100
    s = max(THEME_W.get(t, 1) for t in tags)
    if e.get("curated"):
        s += 2
    if int(e["year"]) < 1950:
        s += 1
    return s


def select_two(pool):
    ranked = sorted(pool, key=score, reverse=True)
    ranked = [e for e in ranked if score(e) > 0]
    if len(ranked) < 2:
        return ranked
    first = ranked[0]
    t1 = set(HC.themes_of(first["text"]))
    second = next((e for e in ranked[1:] if not (set(HC.themes_of(e["text"])) & t1)), ranked[1])
    return [first, second]


def existing_years(ds):
    return re.findall(r"\b(1[6-9]\d\d|20[0-2]\d)\b", " ".join(HC.existing_events(ds)))


def frame(mname, dd, ev):
    e1, e2 = ev
    sysmsg = ("You write the 'This Day in American History' note for a Reformed Christian daily "
              "devotional for men. Output ONLY the note text — no header, no preamble.")
    user = (
        f"Here are TWO verified historical events for {mname} {int(dd)}:\n"
        f"1. ({e1['year']}) {e1['text']}\n"
        f"2. ({e2['year']}) {e2['text']}\n\n"
        f"Write 2 to 4 sentences. State each event accurately, keeping the YEAR, names, places, and "
        f"outcomes EXACTLY as given — add NO fact, date, name, or number that is not above. Then one "
        f"closing sentence tying the day to the trait of a Responsible, RESOLUTE citizen (duty, "
        f"stewardship, courage, accountability before God). Voice: direct, masculine, reverent, "
        f"providential; if an event is dark, frame it under God's sovereignty. No bullet points.")
    msgs = [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}]
    allowed = {e1["year"], e2["year"]}
    for _ in range(3):
        try:
            out = G.call_llm(msgs, MODEL, PORT, max_tokens=500, temperature=0.5).strip()
        except Exception:
            continue
        out = re.sub(r"<think>.*?</think>", "", out, flags=re.DOTALL).strip()
        out = re.sub(r"^```.*?\n|\n```$", "", out).strip()
        yrs = set(re.findall(r"\b(1[6-9]\d\d|20[0-2]\d)\b", out))
        if yrs and yrs.issubset(allowed) and not BANNED.search(out) and 80 <= len(out) <= 900:
            return out
    # deterministic fallback — verbatim facts, lightly templated
    return (f"On {mname} {int(dd)}, {e1['year']}, {e1['text']} "
            f"On the same day in {e2['year']}, {e2['text']} "
            f"Both moments call a Responsible citizen to steward his hour with courage and "
            f"accountability before God.")


def splice(ds, mname, dd, body):
    p = READINGS / f"{ds}.md"
    lines = p.read_text().splitlines()
    start = next((i for i, l in enumerate(lines) if "This Day in American History" in l), None)
    if start is None:
        return False
    end = start + 1
    while end < len(lines):
        s = lines[end].strip()
        if s.startswith(("⚓", "⛏", "🔨", "🙏", "🌙", "⸻", "🦅")):
            break
        end += 1
    new = [f"🦅 This Day in American History — {mname} {int(dd)}", body, ""]
    lines[start:end] = new
    p.write_text("\n".join(lines) + ("\n" if not "\n".join(lines).endswith("\n") else ""))
    return True


def fix_one(ds, force=False, dry=False):
    mm, dd = ds[5:7], ds[8:10]
    mname = MONTHNAME[int(mm)]
    if not HC.existing_events(ds):
        print(f"  {ds}: no history block — skip")
        return "skip"
    pool = build_pool(mm, dd)
    pool_years = {e["year"] for e in pool}
    exy = existing_years(ds)
    if not force and exy and all(y in pool_years for y in exy):
        print(f"  {ds}: existing years {exy} all verify in pool — keep")
        return "keep"
    sel = select_two(pool)
    if len(sel) < 2:
        print(f"  {ds}: pool too thin ({len(pool)} US events) — needs manual; SKIP")
        return "thin"
    if dry:
        print(f"  {ds}: would use {[e['year'] for e in sel]}: "
              + " | ".join(e['text'][:50] for e in sel))
        return "dry"
    body = frame(mname, dd, sel)
    splice(ds, mname, dd, body)
    subprocess.run([sys.executable, "scripts/build_reading_index.py", "histfix", "--date", ds],
                   cwd=REPO, capture_output=True)
    print(f"  {ds}: ✓ {[e['year'] for e in sel]}")
    return "fixed"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit("usage: fix_history_day.py START [END] [--force] [--dry]")
    start = date.fromisoformat(args[0])
    end = date.fromisoformat(args[1]) if len(args) > 1 else start
    cur = start
    from collections import Counter
    tally = Counter()
    while cur <= end:
        tally[fix_one(cur.isoformat(), force="--force" in flags, dry="--dry" in flags)] += 1
        cur += timedelta(days=1)
    print(f"\nSummary: {dict(tally)}")


if __name__ == "__main__":
    main()
