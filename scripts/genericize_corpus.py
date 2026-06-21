#!/usr/bin/env python3
"""Build the GENERIC corpus from Adam's master readings.

Adam's master is written for him specifically (wife Maria; sons Gideon, Boaz;
daughter Shiloh; Fredericksburg, Virginia, United States). The generic corpus is
what everyone else gets (the SDG-4 group + non-form users) AND the template that
form-personalization swaps names into. A surgical, self-auditing local-LLM pass
rewrites ONLY the lines that carry Adam's specifics -> role words ('your wife',
'your children', 'your city/state/country'), generalizing per-child ages so it
fits any father, while keeping scripture, structure, voice, and American-history
facts exactly. Master is never modified; output -> data/readings-generic/.

  python3 scripts/genericize_corpus.py --only 2026-06-04     # dry run, show diffs
  python3 scripts/genericize_corpus.py --apply               # whole corpus
"""
import argparse, glob, json, re, sys, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data" / "readings"
OUT = REPO / "data" / "readings-generic"
ENGINE = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen3.6-35b-a3b"
DONE_LOG = REPO / "scripts" / ".generic_done.txt"

# Lines containing any of these get rewritten; the rest are copied verbatim.
TRIGGERS = ["Maria", "Gideon", "Boaz", "Shiloh", "Fredericksburg", "Virginia", "United States", "America"]
# Family names MUST be gone from generic output; place names may remain as historical illustration.
PRIVATE = ["Maria", "Gideon", "Boaz", "Shiloh"]

REWRITE_SYS = ("You are a careful copy editor. You change ONLY what you are told and reproduce everything "
               "else verbatim. Output only the rewritten line: no preamble, no quotes, no notes.")
AUDIT_SYS = "You are a strict checker. Reply with compact JSON only."


def rewrite_prompt(line):
    return ("This devotional was written for one specific man (Adam: wife Maria; sons Gideon 19 and Boaz 14; "
            "daughter Shiloh 5; living in Fredericksburg, Virginia, United States). Rewrite the line below for "
            "a GENERAL Christian father so it fits ANY reader:\n"
            "- 'Maria' -> 'your wife'.\n"
            "- the children's names -> general references ('your son', 'your daughter', 'your children', or "
            "'your sons and daughter' as the grammar needs); where a child's specific age or individual "
            "situation is given, generalize it ('your son coming into manhood', 'your little ones') so it fits "
            "any family. Keep sons male and the daughter female.\n"
            "- the reader's OWN location ('Fredericksburg' / 'Virginia' / 'United States' / 'America' used as "
            "HIS hometown/state/country) -> 'your city' / 'your state' / 'your country'.\n"
            "- BUT if the line states a HISTORICAL FACT or a 'This Day in American History' entry, keep "
            "America / United States / the place names EXACTLY — do not generalize history.\n"
            "- If the line uses a SPECIFIC battle or local/state event (e.g., the Battle of Fredericksburg, "
            "the Rappahannock, Virginia in the Civil War) as a personal application, do NOT rename the place "
            "(that makes false claims about the reader's city). Keep the historical example as an ILLUSTRATION, "
            "but aim the application generically — 'wherever God has placed you', 'your own community' — so it "
            "stays TRUE for any reader.\n"
            "Keep the scripture, structure, markdown ('• ', '**'), and the Reformed, patriarchal voice exactly. "
            "Output ONLY the rewritten line.\n\nLINE:\n" + line)


def audit_prompt(text):
    return ('Does the text below still contain any of these private names used for a person or his hometown: '
            'Maria, Gideon, Boaz, Shiloh, Fredericksburg? (Historical mentions of America/United States are '
            'fine.) Reply JSON only: {"clean": true|false, "found": "<=8 words}\n\nTEXT:\n' + text)


def call(sys_msg, user, max_tokens=520, temp=0.2):
    body = json.dumps({"model": MODEL, "temperature": temp, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": sys_msg},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(ENGINE, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()


def clean_one_line(out):
    out = out.strip().strip('"').strip()
    if "\n" in out:
        out = max(out.split("\n"), key=len)
    return out


def genericize_line(line, tries=3):
    best = None
    for t in range(tries):
        try:
            out = clean_one_line(call(REWRITE_SYS, rewrite_prompt(line), temp=0.2 + 0.1 * t))
        except Exception as e:
            print(f"    err: {e}", file=sys.stderr); continue
        if not out or not (0.5 * len(line) <= len(out) <= 1.8 * len(line) + 40):
            continue
        best = out
        if not any(p in out for p in PRIVATE):
            # quick model audit only when the cheap check passes
            try:
                raw = call(AUDIT_SYS, audit_prompt(out), max_tokens=90, temp=0.0)
                a = json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group(0))
            except Exception:
                a = {"clean": True}
            if a.get("clean"):
                return out, True
    return best, (best is not None and not any(p in best for p in PRIVATE))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    done = set(DONE_LOG.read_text().split()) if (args.apply and DONE_LOG.exists()) else set()
    files = sorted(glob.glob(str(SRC / "*.md")))
    if args.only:
        files = [f for f in files if args.only in f]
    if args.limit:
        files = files[:args.limit]

    tot_lines = tot_fixed = tot_flag = 0
    flagged = []
    for f in files:
        name = Path(f).name
        if name in done or name.startswith("_"):
            continue
        lines = Path(f).read_text(encoding="utf-8").split("\n")
        for i, ln in enumerate(lines):
            if not any(tk in ln for tk in TRIGGERS):
                continue
            tot_lines += 1
            new, ok = genericize_line(ln)
            if new and new != ln:
                if not args.apply:
                    print(f"― BEFORE: {ln}\n+ AFTER : {new}\n  [{'ok' if ok else 'FLAG'}]\n")
                lines[i] = new
                tot_fixed += 1
            if not ok:
                tot_flag += 1
                flagged.append(f"{name}:{i+1}")
        if args.apply:
            (OUT / name).write_text("\n".join(lines), encoding="utf-8")
            with open(DONE_LOG, "a") as d:
                d.write(name + "\n")
            print(f"{name}: written", flush=True)
    print(json.dumps({"files": len(files), "lines": tot_lines, "rewritten": tot_fixed, "flagged": tot_flag}))
    if flagged:
        print("FLAGGED:", " ".join(flagged[:50]))


if __name__ == "__main__":
    main()
