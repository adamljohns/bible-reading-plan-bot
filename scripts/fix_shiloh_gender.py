#!/usr/bin/env python3
"""Correct Shiloh's gender across the readings corpus.

Shiloh is Adam's 5-year-old DAUGHTER, not a son. The local model generated the
year treating her as a boy (male pronouns, "your sons … Shiloh", manhood
guidance). This rewrites ONLY the lines that reference Shiloh — feminine
pronouns + feminine-flourishing guidance — leaving Gideon and Boaz (sons) and
all other content verbatim. Each rewrite is self-verified by a second model
"audit" pass; failures are flagged. Resumable via a done-log.

  python3 scripts/fix_shiloh_gender.py --only 2026-06-04        # dry run, show diffs
  python3 scripts/fix_shiloh_gender.py --apply                  # fix whole corpus
"""
import argparse, glob, json, re, sys, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENGINE = "http://localhost:1235/v1/chat/completions"
MODEL = "qwen3.6-35b-a3b"
DONE_LOG = REPO / "scripts" / ".shiloh_done.txt"

REWRITE_SYS = ("You are a careful copy editor. You change ONLY what you are told and reproduce "
               "everything else verbatim. Output only the corrected line: no preamble, no quotes, no notes.")
AUDIT_SYS = "You are a strict checker. Reply with compact JSON only."


def rewrite_prompt(line):
    return ("Adam has three children: sons Gideon (19) and Boaz (14), and a DAUGHTER, Shiloh (5). "
            "The line below wrongly treats Shiloh as a son. Rewrite it so Shiloh is correctly a girl: "
            "use she/her for Shiloh, and reframe any fatherly guidance about Shiloh toward raising a "
            "godly young woman and her feminine flourishing (gentleness, modesty, godly womanhood) "
            "rather than manhood. If the three children are grouped as 'sons' ANYWHERE — including "
            "collective phrases like 'my sons', 'each of my sons', 'all my sons', 'his sons' that refer "
            "to all of them — change that to 'children' (or 'sons and daughter'), because one of them, "
            "Shiloh, is a daughter. Keep Gideon and Boaz exactly as sons — do NOT change "
            "their pronouns. Preserve every other word, all markdown (leading '• ', '**bold**'), "
            "scripture, and meaning not about Shiloh's gender. Output ONLY the corrected line.\n\nLINE:\n" + line)


def audit_prompt(text):
    return ('Shiloh is a GIRL (daughter). In the text below: (1) is Shiloh anywhere referred to with '
            'masculine pronouns (he/him/his) or called/grouped as a son? (2) are Gideon and Boaz still '
            'present and still treated as sons? Reply JSON only: '
            '{"shiloh_clean": true|false, "brothers_ok": true|false, "issue": "<=8 words}\n\nTEXT:\n' + text)


def call(sys_msg, user, max_tokens=420, temp=0.2):
    body = json.dumps({"model": MODEL, "temperature": temp, "max_tokens": max_tokens,
                       "messages": [{"role": "system", "content": sys_msg},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(ENGINE, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()


def clean_one_line(out, orig):
    out = out.strip().strip('"').strip()
    if "\n" in out:                                  # strip any preamble the model added
        cands = [l for l in out.split("\n") if "Shiloh" in l]
        out = max(cands, key=len) if cands else max(out.split("\n"), key=len)
    return out


def fix_line(line, tries=3):
    best = None
    for t in range(tries):
        try:
            out = clean_one_line(call(REWRITE_SYS, rewrite_prompt(line), temp=0.2 + 0.12 * t), line)
        except Exception as e:
            print(f"    rewrite err: {e}", file=sys.stderr); continue
        if "Shiloh" not in out: continue
        if ("Gideon" in line) != ("Gideon" in out): continue
        if ("Boaz" in line) != ("Boaz" in out): continue
        if not (0.6 * len(line) <= len(out) <= 1.7 * len(line) + 40): continue
        try:
            raw = call(AUDIT_SYS, audit_prompt(out), max_tokens=120, temp=0.0)
            a = json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group(0))
        except Exception:
            a = {"shiloh_clean": False, "brothers_ok": True}
        best = out
        if a.get("shiloh_clean") and a.get("brothers_ok", True):
            return out, True
    return best, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    done = set(DONE_LOG.read_text().split()) if (args.apply and DONE_LOG.exists()) else set()
    files = sorted(glob.glob(str(REPO / "data/readings/*.md")))
    if args.only:
        files = [f for f in files if args.only in f]
    if args.limit:
        files = files[:args.limit]

    tot_lines = tot_fixed = tot_flag = 0
    flagged = []
    for f in files:
        name = Path(f).name
        if name in done:
            continue
        lines = Path(f).read_text(encoding="utf-8").split("\n")
        changed = False
        for i, ln in enumerate(lines):
            if "Shiloh" not in ln:
                continue
            tot_lines += 1
            new, ok = fix_line(ln)
            if new and new != ln:
                if not args.apply:
                    print(f"― BEFORE: {ln}")
                    print(f"+ AFTER : {new}")
                    print(f"  [audit {'PASS' if ok else 'FLAG'}]\n")
                lines[i] = new
                changed = True
                tot_fixed += 1
            if not ok:
                tot_flag += 1
                flagged.append(f"{name}:{i+1}")
        if changed and args.apply:
            Path(f).write_text("\n".join(lines), encoding="utf-8")
        if args.apply:
            with open(DONE_LOG, "a") as d:
                d.write(name + "\n")
            print(f"{name}: {'fixed' if changed else 'no-op'}", flush=True)
    print(json.dumps({"files": len(files), "shiloh_lines": tot_lines,
                      "rewritten": tot_fixed, "flagged": tot_flag}))
    if flagged:
        print("FLAGGED:", " ".join(flagged[:60]))


if __name__ == "__main__":
    main()
