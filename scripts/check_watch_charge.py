#!/usr/bin/env python3
"""check_watch_charge.py — Watch Charge gate (PJG-1109-EAR1, tightened PJG-1116-EAR3).

Fails when:
  - a Watch Charge does not open with an imperative verb (stop-list of
    determiners/pronouns/conjunctions/proper nouns/abstract nouns, plus a
    suffix heuristic; an allow-list of known imperatives always passes);
  - any banned spoken phrase appears anywhere in the reading ("not a looser one").

USAGE
  python3 scripts/check_watch_charge.py 2026-11-17
  python3 scripts/check_watch_charge.py --range 2026-11-17:2026-12-31
Exit 0 clean, 2 hits, 1 usage/IO.
"""
from __future__ import annotations
import re, sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"

# Spoken-phrase bans (whole reading). "looser" is heard as "loser" (Principal 11-16).
PHRASE_BANS = [
    ("not_a_looser_one", re.compile(r"\bnot a looser one\b", re.I)),
]

STOP = {
    # determiners / articles / quantifiers
    "a", "an", "the", "this", "that", "these", "those", "every", "each", "no", "all",
    "some", "any", "many", "much", "more", "most", "such", "nothing", "everything",
    "something", "anything", "none", "whatever", "whoever", "whichever",
    # pronouns / possessives
    "i", "me", "my", "you", "your", "yours", "he", "him", "his", "she", "her", "it", "its",
    "we", "us", "our", "they", "them", "their", "there", "here", "who", "what", "which",
    # conjunctions / adverbial openers / prepositions
    "when", "while", "if", "because", "since", "as", "and", "but", "or", "so", "yet", "for",
    "though", "although", "until", "unless", "before", "after", "then", "now", "today",
    "tonight", "tomorrow", "in", "on", "at", "by", "with", "from", "to", "of", "through",
    "where", "how", "why", "only", "even", "just", "not",
    # proper nouns / divine names / abstract nouns seen as openers
    "god", "christ", "jesus", "lord", "spirit", "paul", "peter", "moses", "david", "maria",
    "adam", "gideon", "boaz", "shiloh", "fredericksburg", "virginia", "america", "grace",
    "freedom", "faith", "love", "hope", "peace", "liberty", "scripture", "his", "men", "man",
    "husbands", "fathers", "citizens", "children", "sons", "today's",
}

# Sanity allow-list: verbs that also look like nouns/months or would trip the heuristic.
ALLOW = {
    "march", "name", "pray", "worship", "work", "love", "honor", "bless", "rest", "fast",
    "hope", "stand", "guard", "watch", "lead", "keep", "be", "do", "say", "tell", "make",
    "give", "ask", "pick", "write", "walk", "surrender", "step", "stay", "put", "pay",
    "open", "come", "call", "seal", "steel", "plant", "point", "own", "owe", "speak",
    "serve", "secure", "settle", "sit", "silence", "sacrifice", "pull", "provide",
    "protect", "read", "rend", "test", "turn", "treat", "submit", "strip", "strap",
    "strain", "stoke", "smooth", "swing", "overcome", "confess", "forgive", "go", "let",
    "take", "hold", "set", "teach", "train", "thank", "bring", "build", "carry", "check",
    "choose", "close", "commit", "count", "cover", "end", "face", "fight", "finish",
    "follow", "gather", "hand", "hear", "help", "kneel", "listen", "look", "mark", "meet",
    "obey", "plan", "praise", "preach", "receive", "refuse", "remember", "repent", "return",
    "rise", "run", "see", "seek", "send", "show", "sing", "start", "stop", "trust", "wait",
    "wake", "welcome", "win", "yield", "draw", "fix", "lay", "leave", "lift", "light",
    "measure", "pass", "pour", "press", "prepare", "raise", "redeem", "reject", "rejoice",
    "release", "renew", "reset", "resist", "restore", "sharpen", "shepherd", "shoulder",
    "spend", "stir", "strengthen", "study", "tend", "think", "throw", "wash", "weigh",
}

CHARGE = re.compile(r"Watch Charge:\**\s*\**\s*([^\n]*)")


def first_word(line: str) -> str:
    m = re.match(r"[\s\"'“‘*_]*([A-Za-z][A-Za-z'’\-]*)", line)
    return m.group(1) if m else ""


def is_directive(line: str) -> tuple[bool, str]:
    w = first_word(line)
    lw = w.lower().replace("’", "'")
    if not w:
        return False, "empty"
    if lw in ALLOW:
        return True, w
    if lw in STOP:
        return False, w
    if lw.endswith("'s") or re.search(r"(?:ly|ing|ness|tion|ment|ity|ed)$", lw):
        return False, w
    return True, w


def check_text(text: str, label: str = "") -> list[str]:
    hits = []
    for name, rx in PHRASE_BANS:
        if rx.search(text):
            hits.append(f"{label}:PHRASE:{name}")
    for m in CHARGE.finditer(text):
        ok, w = is_directive(m.group(1))
        if not ok:
            hits.append(f"{label}:CHARGE_NOT_DIRECTIVE:{w}: {m.group(1)[:80]}")
    return hits


def dates_from(args):
    out = []
    for a in args:
        if re.match(r"\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$", a):
            s, e = (date.fromisoformat(x) for x in a.split(":"))
            while s <= e:
                out.append(s.isoformat()); s += timedelta(days=1)
        elif re.match(r"\d{4}-\d{2}-\d{2}$", a):
            out.append(a)
    return out


def main() -> int:
    ds = dates_from(sys.argv[1:])
    if not ds:
        print(__doc__, file=sys.stderr); return 1
    total = 0
    for d in ds:
        p = READINGS / f"{d}.md"
        if not p.exists():
            print(f"MISS {d}"); continue
        h = check_text(p.read_text(encoding="utf-8"), d)
        total += len(h)
        print(("FAIL " if h else "PASS ") + d)
        for x in h:
            print("  - " + x)
    print(f"\nTOTAL hits: {total}")
    return 2 if total else 0


if __name__ == "__main__":
    sys.exit(main())
