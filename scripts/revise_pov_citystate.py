#!/usr/bin/env python3
"""Apply two June-30-model fixes the tail-revision doesn't cover:

 1. POV: the Father's Charge reflection must coach the FATHER about his children,
    never address the children directly ("Gideon, you... I charge you" -> "Brother,
    charge Gideon to..."). Only rewrites reflections that actually address a child.
 2. City/State takeaway: the Citizen's Stand application gets one concrete LOCAL
    civic bullet naming the reader's city/state (Fredericksburg / Virginia).

Run AFTER revise_watch_tail (which trims the apps) to avoid a write race. Resumable.

  python3 scripts/revise_pov_citystate.py --only 2026-07
  python3 scripts/revise_pov_citystate.py --apply --from 2026-07-01 --to 2026-07-31
"""
import argparse, glob, json, re, sys, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data" / "readings"
ENGINE = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen3.6-35b-a3b"
DONE = REPO / "scripts" / ".povcs_done.txt"

# Father's Charge reflection: from the 👨 header to the next section marker.
FATHER_REFL = re.compile(r"(👨[^\n]*Reflection for Your Children[^\n]*\n+)(.*?)(?=\n\s*(?:⛏|⸏|🦅|🙏))", re.DOTALL)
# Direct address to a child = the POV problem.
CHILD_ADDR = re.compile(r"\b(Gideon|Boaz|Shiloh)\b[^.?!]{0,18}\byou(?:r|rself)?\b|\byou(?:r|rself)?\b[^.?!]{0,18}\b(Gideon|Boaz|Shiloh)\b|I charge you|you (?:must|are|stand|will) ", re.IGNORECASE)
# Citizen's Stand application block (the ⛏ app between the Citizen header and Evening Peace).
CITIZEN_APP = re.compile(r"(Citizen's Stand.*?[⛏⸏][^\n]*Personal Application[^\n]*\n+)((?:•[^\n]*\n+)+)", re.DOTALL)

SYS = ("You are a careful Reformed devotional editor. Capitalize a pronoun ONLY for God; the reader is "
       "lowercase 'you'. Keep the masculine, watchman voice. Output only what is asked, nothing else.")


def call(user, tries=3, temp=0.3, max_tokens=900):
    for t in range(tries):
        try:
            body = json.dumps({"model": MODEL, "temperature": temp + 0.1 * t, "max_tokens": max_tokens,
                               "messages": [{"role": "system", "content": SYS},
                                            {"role": "user", "content": user}]}).encode()
            req = urllib.request.Request(ENGINE, body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=200) as r:
                return json.load(r)["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if t == tries - 1:
                print("  err:", e, file=sys.stderr)
    return None


def fix_pov(refl):
    p = ("Rewrite this Father's Charge reflection so it speaks ONLY to the father (the man reading), "
         "coaching him about his children. NEVER address a child directly in second person. Turn any direct "
         "address ('Gideon, you...', 'I charge you', 'you must learn') into third-person coaching of the father "
         "('Brother, charge Gideon to...', 'Guard Boaz's heart...', 'teach little Shiloh to...'). Keep the "
         "children's names and genders (Gideon/Boaz sons, Shiloh daughter), the content, length, and voice. "
         "Output only the rewritten reflection.\n\n" + refl)
    for _ in range(3):
        out = call(p)
        if out and "Shiloh" in out + refl and not re.search(r"\b(Gideon|Boaz|Shiloh),?\s+you\b|I charge you", out, re.I):
            return out.strip()
    return None


def fix_citystate(bullets):
    p = ("These are the Citizen's Stand application bullets. Keep them to 1-2 bullets, concrete and actionable, "
         "and make ONE of them a specific LOCAL civic takeaway that names the reader's city or state "
         "(Fredericksburg, Virginia) — engaging a local issue, a neighbor, a school-board/council matter, or a "
         "civic duty where he lives, as a man who fears God more than man. Each bullet starts with '• '. "
         "Output only the bullets.\n\n" + bullets)
    for _ in range(3):
        out = call(p, max_tokens=300)
        if out:
            bl = [l.strip() for l in out.splitlines() if l.strip().startswith("•")]
            if 1 <= len(bl) <= 2 and any(re.search(r"Fredericksburg|Virginia", b) for b in bl):
                return "\n".join(bl)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    done = set(DONE.read_text().split()) if (args.apply and DONE.exists()) else set()
    files = sorted(glob.glob(str(SRC / "2026-*.md")))
    if args.only:
        files = [f for f in files if args.only in f]
    npov = ncs = 0
    for f in files:
        name = Path(f).name
        if name.startswith("_") or name in done:
            continue
        text = Path(f).read_text(encoding="utf-8")
        orig = text
        m = FATHER_REFL.search(text)
        if m and CHILD_ADDR.search(m.group(2)):
            new = fix_pov(m.group(2).strip())
            if new:
                text = text[:m.start(2)] + new + text[m.end(2):]
                npov += 1
                if not args.apply:
                    print(f"[{name}] POV fixed:\n  {new[:160]}...\n")
        m = CITIZEN_APP.search(text)
        if m and not re.search(r"Fredericksburg|Virginia", m.group(2)):
            new = fix_citystate(m.group(2).strip())
            if new:
                text = text[:m.start(2)] + new + "\n" + text[m.end(2):]
                ncs += 1
                if not args.apply:
                    print(f"[{name}] city/state:\n  {new[:160]}\n")
        if args.apply:
            if text != orig:
                Path(f).write_text(text, encoding="utf-8")
            with open(DONE, "a") as d:
                d.write(name + "\n")
            print(f"{name}: pov={'y' if m else '-'}", flush=True)
    print(json.dumps({"pov_fixed": npov, "citystate_fixed": ncs}))


if __name__ == "__main__":
    main()
