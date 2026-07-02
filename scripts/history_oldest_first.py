#!/usr/bin/env python3
"""Reorder 'This Day in American History' paragraphs so the OLDEST event is first.

Only touches days whose two events are currently newest-first. Reorders the prose
(keeping both events, all facts/dates/names, and the closing application intact);
NEVER invents or removes events. Self-detecting + resumable + idempotent.

  python3 scripts/history_oldest_first.py --dry          # show what it would change
  python3 scripts/history_oldest_first.py --apply
"""
import argparse, glob, json, re, sys, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data" / "readings"
ENGINE = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen3.6-35b-a3b"

YEAR = re.compile(r"\b(1[5-9]\d{2}|20[0-2]\d)\b")
HIST = re.compile(r"(🦅 This Day in American History[^\n]*\n+)(.*?)(?=\n\s*(?:⸻|🙏|🛡️|⚓))", re.DOTALL)

SYS = "You reorder text without changing facts. Output only the reordered paragraph."


def reorder_prompt(para):
    return ("Below is a 'This Day in American History' paragraph: two historical events and a closing "
            "application sentence. Reorder it so the event with the EARLIER year is described FIRST, then the "
            "later event, then keep the application sentence at the end. Preserve EVERY fact, date, name, and "
            "the application exactly — change only the order and the linking phrases (e.g. 'On the same day in "
            "YEAR ...'). Do not add or drop events. Output ONLY the reordered paragraph.\n\n" + para)


def call(user, tries=3, temp=0.2):
    for t in range(tries):
        try:
            body = json.dumps({"model": MODEL, "temperature": temp, "max_tokens": 700,
                               "messages": [{"role": "system", "content": SYS},
                                            {"role": "user", "content": user}]}).encode()
            req = urllib.request.Request(ENGINE, body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if t == tries - 1:
                print("  err:", e, file=sys.stderr)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    files = sorted(glob.glob(str(SRC / "2026-*.md")))
    if args.only:
        files = [f for f in files if args.only in f]
    changed = skipped = 0
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        m = HIST.search(text)
        if not m:
            continue
        para = m.group(2).strip()
        yrs = [int(y) for y in YEAR.findall(para)]
        if len(yrs) < 2 or yrs == sorted(yrs):
            continue  # already oldest-first (or single event)
        new = None
        for _ in range(3):
            cand = call(reorder_prompt(para))
            if not cand:
                continue
            ny = [int(y) for y in YEAR.findall(cand)]
            # require: same set of years, now ascending, length preserved
            if sorted(ny) == sorted(yrs) and ny == sorted(ny) and abs(len(cand) - len(para)) < 0.4 * len(para):
                new = cand.strip()
                break
        if not new:
            skipped += 1
            print(f"  ! {Path(f).stem}: could not safely reorder {yrs}", file=sys.stderr)
            continue
        if args.apply:
            Path(f).write_text(text[:m.start(2)] + new + text[m.end(2):], encoding="utf-8")
        else:
            print(f"--- {Path(f).stem}  {yrs} -> sorted ---\n{new[:300]}\n")
        changed += 1
    print(json.dumps({"reordered": changed, "skipped": skipped}))


if __name__ == "__main__":
    main()
