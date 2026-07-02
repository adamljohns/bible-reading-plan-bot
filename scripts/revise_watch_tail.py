#!/usr/bin/env python3
"""Revise each watch's tail across the corpus (master data/readings/<date>.md):
  - Personal Application -> 1-2 VARIED action bullets (never 'Read...', not always 'write down';
    rotate identify / reflect / take a step / have a conversation / journal-sometimes).
  - One prayer-type application is WOVEN into the Prayer instead of listed as a bullet.
  - Closer -> '🛡️ The Charge: <imperative>' with WATCHMAN imagery, no ship/helm/rudder/compass words.
Scripture, reflection, and the 🦅 history block are left untouched (history has its own pass).
Resumable. Master is in git, so reverts are clean.

  python3 scripts/revise_watch_tail.py --only 2026-06-04         # dry run, show diffs
  python3 scripts/revise_watch_tail.py --apply                   # whole corpus (in place)
"""
import argparse, glob, json, re, sys, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data" / "readings"
ENGINE = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen3.6-35b-a3b"
DONE = REPO / "scripts" / ".tailrev_done.txt"

WATCH_HDR = re.compile(r"^\s*(🌅|🕖|🕚|🕒|🌙)")
APP_HDR = re.compile(r"^\s*[⛏⸏]")   # both pickaxe variants appear in the corpus
PRAYER_HDR = re.compile(r"^\s*🙏")
HIST_HDR = re.compile(r"^\s*🦅")
CLOSER = re.compile(r"^\s*[⚓🛡]️?\s*(?:\*\*)?\s*(?:The Charge|Helm Command|Rudder Steer|Set Sail|Course Correction|Steady As She Goes|Night Orders)", re.IGNORECASE)
BULLET = re.compile(r"^\s*•")
SEP = re.compile(r"^\s*[⸻\-—]{2,}\s*$")
NAUT = ["helm", "rudder", "steer", "compass", "tiller", "mast", "keel", "sail"]

SYS = ("You are a careful devotional editor in a Reformed, patriarchal, military-watchman voice. "
       "Capitalize a pronoun ONLY when it refers to God (He, His, Him, and You/Your when addressed to God); "
       "the READER is always lowercase 'you / your / yourself'. Output EXACTLY the requested labeled blocks.")


def prompt(bullets, prayer, closer, has_app):
    app_rule = ("###BULLETS\n1, or at most 2, Personal-Application bullets (each line starting with '• '). "
                "Rules: NEVER an application that tells the reader to 'read' anything. VARY the action and its "
                "wording across watches — pick from: identify/name something, reflect on or consider something, "
                "take one concrete step toward something, have a specific conversation with someone, or (only "
                "sometimes) write/journal something. Do NOT default to 'write it down'. Keep it concrete to "
                "today's theme.\n" if has_app else
                "###BULLETS\n(this watch has no Personal Application section — output the word NONE)\n")
    return (
        "Revise the tail of one daily-devotional watch. Keep the Reformed, masculine, watchman voice and God's "
        "capitalized pronouns. Return EXACTLY these three blocks:\n\n" + app_rule +
        "###PRAYER\nThe prayer, lightly revised so that ONE application (a thing to ask God for, drawn from "
        "today's theme) is woven naturally into it as a petition. Keep the rest of the prayer's substance and "
        "end with 'Amen.'\n"
        "###CHARGE\nExactly one line: '🛡️ The Charge: <imperative>'. KEEP the original closer's specific meaning "
        "and as much of its wording as possible; change the label to 'The Charge' and, ONLY if it contains "
        "ship-steering words (helm, rudder, steer, compass, course, tiller, mast, keel, vessel, sail), replace "
        "just those. Root the charge in TODAY's concrete theme and images (visible in the prayer and original "
        "closer above) — never a generic slogan. CRITICAL — vary the opening verb and image EVERY day: do NOT "
        "begin with 'Stand firm at the post', 'Stand at the post', or 'Stand your post' (badly overused). Reach "
        "for fresh, specific verbs from the day's passage: guard, lift, tear down, gird, sound the alarm, raise, "
        "keep, hold fast, drive out, build, kneel, shoulder, light the lamp, war, bind, sever, run.\n\n"
        f"CURRENT APPLICATION BULLETS:\n{bullets or '(none)'}\n\nCURRENT PRAYER:\n{prayer}\n\nCURRENT CLOSER:\n{closer}\n"
    )


def call(user, tries=3, temp=0.3):
    for t in range(tries):
        try:
            body = json.dumps({"model": MODEL, "temperature": temp + 0.1 * t, "max_tokens": 950,
                               "messages": [{"role": "system", "content": SYS},
                                            {"role": "user", "content": user}]}).encode()
            req = urllib.request.Request(ENGINE, body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=220) as r:
                return json.load(r)["choices"][0]["message"]["content"]
        except Exception as e:
            if t == tries - 1:
                print("  call err:", e, file=sys.stderr)
    return None


def parse_blocks(out, has_app):
    if not out:
        return None
    b = re.search(r"###\s*BULLETS\s*(.*?)\s*###\s*PRAYER", out, re.DOTALL | re.IGNORECASE)
    p = re.search(r"###\s*PRAYER\s*(.*?)\s*###\s*CHARGE", out, re.DOTALL | re.IGNORECASE)
    c = re.search(r"###\s*CHARGE\s*(.*)$", out, re.DOTALL | re.IGNORECASE)
    if not (b and p and c):
        return None
    bullets = [re.sub(r"^\s*", "", l) for l in b.group(1).splitlines() if l.strip().startswith("•")]
    if has_app and not (1 <= len(bullets) <= 2):
        return None
    if not has_app:
        bullets = []
    if has_app and any(re.search(r"\bread\b", x, re.IGNORECASE) for x in bullets):
        return None
    prayer = p.group(1).strip()
    charge_lines = [l.strip() for l in c.group(1).strip().splitlines() if l.strip()]
    charge = charge_lines[0] if charge_lines else ""
    if not prayer.rstrip().lower().endswith(("amen.", "amen")) or not charge.startswith("🛡️ The Charge:"):
        return None
    if any(re.search(r"\b" + re.escape(w) + r"\b", charge.lower()) for w in NAUT):
        return None
    return bullets, prayer, charge


def scan_tails(lines):
    tails, cur = [], {}
    for i, ln in enumerate(lines):
        if WATCH_HDR.match(ln):
            cur = {"app_bullets": [], "prayer_body": []}
        if APP_HDR.match(ln):
            cur["app_hdr"] = i
        elif HIST_HDR.match(ln):
            cur["hist"] = i
        elif PRAYER_HDR.match(ln):
            cur["prayer_hdr"] = i
        elif BULLET.match(ln) and "app_hdr" in cur and "prayer_hdr" not in cur and "hist" not in cur:
            cur.setdefault("app_bullets", []).append(i)
        elif "prayer_hdr" in cur and "closer" not in cur and ln.strip() and not SEP.match(ln) and not CLOSER.match(ln):
            cur.setdefault("prayer_body", []).append(i)
        elif CLOSER.match(ln):
            cur["closer"] = i
            if cur.get("prayer_body"):
                tails.append(cur)
            cur = {"app_bullets": [], "prayer_body": []}
    return tails


def revise_file(path, dry=False):
    lines = path.read_text(encoding="utf-8").split("\n")
    tails = scan_tails(lines)
    repl, skip = {}, set()
    ok_all = True
    for t in tails:
        has_app = bool(t["app_bullets"])
        bullets_txt = "\n".join(lines[i].strip() for i in t["app_bullets"])
        prayer_txt = "\n".join(lines[i] for i in t["prayer_body"])
        closer_txt = lines[t["closer"]]
        parsed, raw = None, None
        for _ in range(3):
            raw = call(prompt(bullets_txt, prayer_txt, closer_txt, has_app))
            parsed = parse_blocks(raw, has_app)
            if parsed:
                break
        if not parsed:
            ok_all = False
            print(f"  ! L{t['closer']+1} failed (has_app={has_app}). RAW:\n{(raw or '(none)')[:700]}\n", file=sys.stderr)
            continue
        new_bullets, new_prayer, new_charge = parsed
        if dry:
            print(f"--- watch tail @ L{t['closer']+1} ---")
            if has_app:
                print("BULLETS:\n  " + "\n  ".join([lines[i].strip() for i in t['app_bullets']]))
                print("  -> \n  " + "\n  ".join(new_bullets))
            print("CLOSER:\n  " + closer_txt.strip() + "\n  -> " + new_charge)
            print("PRAYER(woven):\n  " + new_prayer[:300] + "\n")
        if has_app:
            repl[t["app_bullets"][0]] = "\n".join(new_bullets)
            for j in t["app_bullets"][1:]:
                skip.add(j)
        if t["prayer_body"]:
            repl[t["prayer_body"][0]] = new_prayer
            for j in t["prayer_body"][1:]:
                skip.add(j)
        repl[t["closer"]] = new_charge
    if dry:
        return ok_all
    out = [repl.get(i, ln) for i, ln in enumerate(lines) if i not in skip]
    path.write_text("\n".join(out), encoding="utf-8")
    return ok_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    done = set(DONE.read_text().split()) if (args.apply and DONE.exists()) else set()
    files = sorted(glob.glob(str(SRC / "*.md")))
    if args.only:
        files = [f for f in files if args.only in f]
    if args.limit:
        files = files[:args.limit]
    for f in files:
        name = Path(f).name
        if name.startswith("_") or name in done:
            continue
        if name < "2026-03-01.md":   # Jan-Feb = Adam's original hand-authored format (different structure)
            continue
        ok = revise_file(Path(f), dry=not args.apply)
        if args.apply:
            with open(DONE, "a") as d:
                d.write(name + "\n")
            print(f"{name}: {'ok' if ok else 'PARTIAL'}", flush=True)


if __name__ == "__main__":
    main()
