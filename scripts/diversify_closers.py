#!/usr/bin/env python3
"""
diversify_closers.py — Round 2 of the closer refresh. Round 1 removed the
"hold the line" cliche but the model converged on a NEW opener monoculture
("Anchor your soul in the Word" x170+, "Secure the...", "Keep your...").
The dedup gate only caught duplicate full LINES, not opener convergence.

This regenerates every closer whose opening two words are over-represented,
enforcing a GLOBAL PER-OPENER CAP: a candidate whose opener-bigram has already
hit the cap is rejected and retried with that opening word banned. The model
keeps its freedom to pick a fitting opener from the passage — it just can't
pile onto an over-used one. Result: a genuinely flat opener distribution.

USAGE
  python3 scripts/diversify_closers.py --test 20      # sample, no write
  python3 scripts/diversify_closers.py --apply        # full run
  python3 scripts/diversify_closers.py --apply 2026-03-01 2026-03-31
"""
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
sys.path.insert(0, str(REPO / "scripts"))
import generate_reading_local as G
from build_reading_index import split_watches
from refresh_closers import watch_parts, CLOSER_RE

MODEL, PORT = "qwen3.6-35b-a3b", "1235"
OVER_THRESHOLD = 20   # an opener-bigram appearing more than this is "converged"
CAP = 14              # no opener-bigram may exceed this after the pass
BANNED = re.compile(r"hold (the|your) line|hold fast|tide of|wave of|breach your deck|"
                    r"\bcompromise\b|stand firm in the truth|sword of the spirit|"
                    r"\banchor\b|spiritual perimeter", re.I)


def opener(text):
    return " ".join(text.split()[:2]).lower().rstrip(",.;:")


def gen(label, scrip, refl, avoid_words):
    sysmsg = ("You write a single closing imperative for one watch of a Reformed devotional "
              "for men. Output ONLY the one-sentence command, nothing else.")
    avoid = ""
    if avoid_words:
        avoid = (" Do NOT begin the sentence with any of these words: "
                 + ", ".join(sorted(avoid_words)) + ".")
    user = (f"Watch passage (excerpt): {scrip}\n"
            f"Reflection (excerpt): {refl}\n\n"
            f"Write ONE fresh '{label}' — a vivid command drawn from the SPECIFIC imagery of THIS "
            f"passage (nautical, military, watchman, forge, harvest, shepherd, courtroom — whatever "
            f"the text evokes). Direct, masculine, reverent; do not open with 'Brother,'. BANNED "
            f"words/phrases: 'anchor', 'hold the line', 'hold fast', 'tide/wave of compromise', "
            f"'breach your deck', 'stand firm in the truth', 'sword of the Spirit', 'spiritual "
            f"perimeter'.{avoid} One sentence ending in a period.")
    msgs = [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}]
    out = G.call_llm(msgs, MODEL, PORT, max_tokens=90, temperature=0.85).strip()
    out = re.sub(r"<think>.*?</think>", "", out, flags=re.DOTALL).strip()
    out = out.strip().strip('"').splitlines()[0].strip() if out else ""
    out = re.sub(r"^Brother,\s*", "", out)
    if out:
        out = out[0].upper() + out[1:]
    out = re.sub(r"\b([Tt]he )Lord\b(?!\s+(Jesus|Christ|God|GOD))", lambda m: m.group(1) + "LORD", out)
    out = out.replace("Lord’s", "LORD’s").replace("Lord's", "LORD's")
    if out and not out.endswith((".", "!")):
        out += "."
    return out


def main():
    test_n = int(sys.argv[sys.argv.index("--test") + 1]) if "--test" in sys.argv else 0
    dates_args = [a for a in sys.argv[1:] if re.match(r"\d{4}-\d{2}-\d{2}", a)]
    all_days = sorted(p.stem for p in READINGS.glob("2026-*.md"))
    if len(dates_args) == 2:
        s, e = date.fromisoformat(dates_args[0]), date.fromisoformat(dates_args[1])
        all_days = [d for d in all_days if s <= date.fromisoformat(d) <= e]

    # Pass 1: collect every closer + its opener; decide the converged openers.
    closers = []  # (ds, wk, label, line, text)
    for ds in all_days:
        for wk, wt in split_watches((READINGS / f"{ds}.md").read_text()).items():
            for ln in wt.splitlines():
                m = CLOSER_RE.match(ln)
                if m:
                    label = "Rudder Steer" if "Rudder" in m.group(1) else "Helm Command"
                    closers.append((ds, wk, label, ln, m.group(2)))
    opener_counts = Counter(opener(t) for *_, t in closers)
    converged = {o for o, c in opener_counts.items() if c > OVER_THRESHOLD}
    # seed the running cap-counter with the openers we are KEEPING (non-converged)
    running = Counter(opener(t) for *_, t in closers if opener(t) not in converged)
    targets = [c for c in closers if opener(c[4]) in converged]
    print(f"closers={len(closers)}  converged openers={len(converged)}  targets={len(targets)}", flush=True)

    seen_lines = set(t.lower() for *_, t in closers)
    done = 0

    def flush(ds, pairs):
        if not pairs:
            return
        md = (READINGS / f"{ds}.md").read_text()
        for old, new in pairs:
            md = md.replace(old, new, 1)
        (READINGS / f"{ds}.md").write_text(md)
        subprocess.run([sys.executable, "scripts/build_reading_index.py", "diversify", "--date", ds],
                       cwd=REPO, capture_output=True)
        print(f"  {ds}: {len(pairs)} closer(s) diversified", flush=True)

    cur_ds, cur_pairs = None, []
    for ds, wk, label, line, oldtext in targets:
        if test_n and done >= test_n:
            break
        if not test_n and ds != cur_ds:
            flush(cur_ds, cur_pairs)   # write completed date incrementally (resumable)
            cur_ds, cur_pairs = ds, []
        scrip, refl = watch_parts(split_watches((READINGS / f"{ds}.md").read_text())[wk])
        avoid = set()
        new = None
        for attempt in range(6):
            try:
                cand = gen(label, scrip, refl, avoid)
            except Exception:
                continue
            if not cand or BANNED.search(cand) or not (20 <= len(cand) <= 175):
                continue
            op = opener(cand)
            if cand.lower() in seen_lines:
                continue
            if running[op] >= CAP:
                avoid.add(op.split()[0])   # ban this opening word, retry
                continue
            new = cand
            break
        if not new:
            print(f"  {ds} [{wk}]: no fresh opener found, keeping", flush=True)
            continue
        running[opener(new)] += 1
        seen_lines.add(new.lower())
        cur_pairs.append((line, line.replace(oldtext, new)))
        done += 1
        if test_n:
            print(f"  {ds} [{wk}]\n     OLD: {oldtext}\n     NEW: {new}", flush=True)

    if test_n:
        print(f"\nTEST — {done} regenerated")
        return
    flush(cur_ds, cur_pairs)
    print(f"\nAPPLIED — {done} closers", flush=True)


if __name__ == "__main__":
    main()
