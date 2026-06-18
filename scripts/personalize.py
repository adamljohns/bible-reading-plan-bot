#!/usr/bin/env python3
"""Personalize a daily reading from ONE shared template + a tiny per-user profile.

Storage model (the key idea): we do NOT grind and store a full 365-day plan per
user. We keep ONE shared corpus (~8 MB for the year) and a ~0.4 KB profile per
user, and RENDER each day on demand by swapping tokens. Scripture in the user's
chosen version/language is pulled by reference from the existing BTE data
(assets/chapters/ + assets/chapters-ml/) — no re-translation, no extra storage.

  1 000 users  =  ~8 MB template  +  1 000 × 0.4 KB profiles  ≈  8.4 MB total
  (vs. a naive full-copy-per-user ≈ 8.4 GB — a ~1000× saving.)

Layer A (this file): deterministic name + location swaps — works for everyone,
no LLM, instant. Layer B (separate, optional): a local-LLM "grind" that re-authors
the child-specific / archetype-specific commentary for a given profile, stored as
a compact delta. Most users only need Layer A.

  python3 scripts/personalize.py --date 2026-06-04 --demo
"""
import argparse, json, re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Adam's master tokens (the fixed strings that appear in the master corpus)
MASTER = {"wife": "Maria", "sons": ["Gideon", "Boaz"], "daughters": ["Shiloh"],
          "city": "Fredericksburg", "state": "Virginia", "nation": "United States"}

# A profile is just: {wife, sons[], daughters[], city, state, nation, version, lang}
GENERIC = {"wife": None, "sons": [], "daughters": [], "city": None, "state": None,
           "nation": None, "version": "NKJV", "lang": "en"}


def grammatical_list(names):
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"


def personalize_text(text, profile):
    """Deterministic Layer-A render: swap Adam's specifics for this profile's."""
    p = {**GENERIC, **(profile or {})}
    master_group = grammatical_list(MASTER["sons"] + MASTER["daughters"])  # "Gideon, Boaz, and Shiloh"

    # 1) grouped children appositive — handle before individual names
    user_kids = (p["sons"] or []) + (p["daughters"] or [])
    if user_kids:
        text = text.replace(master_group, grammatical_list(user_kids))
    else:
        text = re.sub(r",?\s*" + re.escape(master_group), " your children", text)

    # 2) location (longest first so "United States" wins over a bare token)
    text = text.replace("United States", p["nation"] or "your country")
    text = text.replace("America", p["nation"] or "your country")
    text = text.replace("Fredericksburg", p["city"] or "your city")
    text = text.replace("Virginia", p["state"] or "your state")

    # 3) wife
    text = text.replace("Maria", p["wife"] or "your wife")

    # 4) individual children (positional map; generic -> role word)
    for i, s in enumerate(MASTER["sons"]):
        repl = (p["sons"][i] if i < len(p["sons"] or []) else None) or "your son"
        text = re.sub(r"\b" + s + r"\b", repl, text)
    for i, d in enumerate(MASTER["daughters"]):
        repl = (p["daughters"][i] if i < len(p["daughters"] or []) else None) or "your daughter"
        text = re.sub(r"\b" + d + r"\b", repl, text)
    return text


def personalize_day(day_json, profile):
    out = {"date": day_json["date"], "watches": {}}
    for key, w in day_json["watches"].items():
        out["watches"][key] = {**w, "text": personalize_text(w["text"], profile)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="2026-06-04")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    day = json.load(open(REPO / f"docs/assets/readings/{args.date}.json", encoding="utf-8"))

    sample = {"wife": "Sarah", "sons": ["Caleb", "Levi"], "daughters": ["Grace"],
              "city": "Dallas", "state": "Texas", "nation": "United States",
              "version": "ESV", "lang": "en"}

    if args.demo:
        father = day["watches"]["second"]["text"]
        intro = father.split("\n")[0][:430]
        print("================ ONE TEMPLATE, THREE RENDERS (Father's Charge intro) ================\n")
        print("— ADAM (master profile) —\n" + intro + "\n")
        print("— GENERIC (everyone else / SDG-4 group) —\n" + personalize_text(intro, GENERIC) + "\n")
        print("— SAMPLE FORM USER (Dave: wife Sarah; sons Caleb, Levi; daughter Grace; Dallas TX) —\n"
              + personalize_text(intro, sample) + "\n")
        import sys
        prof_bytes = len(json.dumps(sample))
        print(f"profile size for that user: {prof_bytes} bytes  ·  shared template/day: "
              f"{(REPO / f'docs/assets/readings/{args.date}.json').stat().st_size} bytes")


if __name__ == "__main__":
    main()
