#!/usr/bin/env python3
"""
Build a strict-confidence subset of denom corrections from the
V4.9 detector output.

Rules — INCLUDE only if:
  1. Detector confidence == 'high'
  2. enrichment_notes contains AFFIRMATIVE language for the proposed denom
     (e.g., "is CBF", "confirmed CBF", "actually CBF", "rebranded as ... CBF",
      "data error: ... is ELCA", etc.)
  3. enrichment_notes does NOT contain REJECTION/CONDITIONAL language for
     the proposed change (e.g., "is genuinely LCMS", "stays LCMS",
      "recommend verification", "if this church is...", "likely fabricated")

Output: tmp/denom_corrections_strict.json
"""
import json
import re
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
PROPOSALS = ROOT / "tmp/denom_correction_proposals.json"
CHURCHES = ROOT / "docs/data/churches.json"
OUT = ROOT / "tmp/denom_corrections_strict.json"
REJECTED_OUT = ROOT / "tmp/denom_corrections_rejected.json"

# Map proposed_bucket / proposed_denomination to the keyword set we look for
def proposed_keywords(prop_bucket: str, prop_full: str) -> list[str]:
    pb = (prop_bucket or "").lower()
    pf = (prop_full or "").lower()
    kws = []
    if "cbf" in pb or "cooperative baptist" in pf:
        kws += ["cbf", "cooperative baptist"]
    if "bgav" in pb or "baptist general association of virginia" in pf:
        kws += ["bgav"]
    if "abc" in pb or "american baptist" in pf:
        kws += ["abcusa", "abc-usa", "american baptist"]
    if pb == "ifb" or "independent baptist" in pf:
        kws += ["ifb", "independent baptist"]
    if "elca" in pb or "evangelical lutheran church in america" in pf:
        kws += ["elca"]
    if "umc" in pb or ("united methodist" in pf and "global" not in pf):
        kws += ["umc", "united methodist"]
    if "pcusa" in pb or "presbyterian church (usa)" in pf:
        kws += ["pcusa", "pc(usa)", "presbyterian church usa", "presbyterian church (usa)"]
    if "epc" in pb or "evangelical presbyterian church" in pf:
        kws += ["epc", "evangelical presbyterian"]
    return kws


# Affirmative patterns — strong signals the prior research CONFIRMED the proposal
def has_affirmative(notes: str, keywords: list[str]) -> bool:
    n = notes.lower()
    for kw in keywords:
        # "is <kw>", "confirmed <kw>", "is now <kw>", "actually <kw>",
        # "is a <kw>", "is an <kw>", "<kw>-affiliated", "<kw> affiliated",
        # "<kw> congregation", "<kw> partnership", "rebranded ... <kw>",
        # "is genuinely <kw>", "tagged ... actually <kw>"
        patterns = [
            rf"\bis\s+(?:a\s+|an\s+)?{re.escape(kw)}\b",
            rf"\bconfirmed\s+{re.escape(kw)}\b",
            rf"\bis\s+now\s+{re.escape(kw)}\b",
            rf"\bactually\s+{re.escape(kw)}\b",
            rf"{re.escape(kw)}-affiliated",
            rf"{re.escape(kw)}\s+affiliated",
            rf"{re.escape(kw)}\s+(?:congregation|partnership|membership|triple-affiliation|dual|baptist|lutheran|presbyterian|methodist|church|trajectory)",
            rf"\bis\s+genuinely\s+{re.escape(kw)}\b",
            rf"rebranded.*{re.escape(kw)}",
            rf"data\s+error.*\bis\s+{re.escape(kw)}\b",
            rf"\blisted\s+as\s+\w+.*but\s+is\s+{re.escape(kw)}\b",
            rf"\bnot\s+sbc.*\b{re.escape(kw)}\b",
            rf"\bdowngrad\w*.*{re.escape(kw)}",
            rf"{re.escape(kw)}\s+vs\s+sbc",  # CBF vs SBC ratio analysis
            rf"\bbecame\s+{re.escape(kw)}\b",
            rf"\bjoined\s+{re.escape(kw)}\b",
            rf"pattern\s+confirmed\s+\W+\s*{re.escape(kw)}",  # "Pattern confirmed — BGAV"
            rf"confirmed\s+\W+\s*{re.escape(kw)}\s+",         # "confirmed — BGAV Baptist"
            rf"\bdual\s+{re.escape(kw)}\b",                    # "dual BGAV+CBF"
            rf"\b{re.escape(kw)}\+\w+",                        # "BGAV+CBF" combo tag
            rf"\b\w+\+{re.escape(kw)}\b",                      # "SBC+BGAV"
        ]
        for p in patterns:
            if re.search(p, n):
                return True
    return False


# Rejection patterns — strong signals the prior research REJECTED the proposal
# (e.g., the proposal was "LCMS -> ELCA" but the note says "is genuinely LCMS")
def has_rejection_for(notes: str, current_denom: str) -> bool:
    n = notes.lower()
    cd = (current_denom or "").lower()
    # Extract the short keyword for the CURRENT denom
    cur_kws = []
    if "lcms" in cd:
        cur_kws += ["lcms"]
    if cd in ("sbc",) or "southern baptist" in cd:
        cur_kws += ["sbc"]
    if "pca" in cd:
        cur_kws += ["pca"]
    if "global methodist" in cd or "gmc" in cd:
        cur_kws += ["gmc", "global methodist"]
    if "lutheran" in cd and "lcms" not in cd:
        cur_kws += ["lcms"]  # generic Lutheran tag often defaults to LCMS

    # If the notes affirm the CURRENT denom's correctness, the proposed change is rejected
    for kw in cur_kws:
        patterns = [
            rf"\bis\s+genuinely\s+{re.escape(kw)}\b",
            rf"\bgenuinely\s+{re.escape(kw)}\b",
            rf"\bremains?\s+{re.escape(kw)}\b",
            rf"\bstays?\s+{re.escape(kw)}\b",
            rf"\bconfirmed\s+{re.escape(kw)}\b\s+(?:via|on|per|through)",
            rf"\bcurrent\s+{re.escape(kw)}\s+pastor\b",
            rf"\b{re.escape(kw)}\s+(?:via|per)\s+locator",
            rf"\bupgraded\s+to\s+green\s+based\s+on\s+confessional\s+{re.escape(kw)}",
        ]
        for p in patterns:
            if re.search(p, n):
                return True
    return False


# Conditional/uncertain language — proposal is unverified
CONDITIONAL_PATTERNS = [
    r"\brecommend\s+verification\b",
    r"\brecommend\s+removal\b",
    r"\brecommend\s+deletion\b",
    r"\brecommend\s+(?:re-)?verify\b",
    r"\bif\s+this\s+church\s+is\b",
    r"\blikely\s+fabricated\b",
    r"\blikely\s+phantom\b",
    r"\bphantom\s+entry\b",
    r"\bremove\s+or\s+re-verify\b",
    r"\bremove\s+or\s+verify\b",
    r"\bunverified\s+(?:proposal|claim)\b",
    r"\bcould\s+not\s+confirm\b",
    r"\bunable\s+to\s+confirm\b",
]


def has_conditional(notes: str) -> bool:
    n = notes.lower()
    for p in CONDITIONAL_PATTERNS:
        if re.search(p, n):
            return True
    return False


def main():
    proposals = json.loads(PROPOSALS.read_text())
    data = json.loads(CHURCHES.read_text())
    churches = data if isinstance(data, list) else data.get("churches", data)
    by_id = {c["id"]: c for c in churches if "id" in c}

    accepted, rejected = [], []
    for p in proposals:
        if p.get("confidence") != "high":
            rejected.append({**p, "_reject_reason": "confidence != high"})
            continue
        rec = by_id.get(p["id"])
        if not rec:
            rejected.append({**p, "_reject_reason": "record not in churches.json"})
            continue
        notes = rec.get("enrichment_notes") or ""
        if not notes.strip():
            rejected.append({**p, "_reject_reason": "no enrichment_notes"})
            continue

        # Skip None/empty proposed denomination (those are deletion candidates, not rename)
        if not p.get("proposed_denomination") or p.get("proposed_denomination") == "None":
            rejected.append({**p, "_reject_reason": "proposed denom is None"})
            continue

        kws = proposed_keywords(p.get("proposed_bucket", ""), p.get("proposed_denomination", ""))
        if not kws:
            rejected.append({**p, "_reject_reason": "unmappable proposed bucket"})
            continue

        if has_conditional(notes):
            rejected.append({**p, "_reject_reason": "conditional/uncertain language in notes"})
            continue

        if has_rejection_for(notes, p.get("current_denomination", "")):
            rejected.append({**p, "_reject_reason": "notes affirm CURRENT denom (proposal rejected by prior research)"})
            continue

        if not has_affirmative(notes, kws):
            rejected.append({**p, "_reject_reason": "no affirmative confirmation of proposed denom in notes"})
            continue

        accepted.append(p)

    OUT.write_text(json.dumps(accepted, indent=2))
    REJECTED_OUT.write_text(json.dumps(rejected, indent=2))

    print(f"Total proposals:       {len(proposals)}")
    print(f"Strict-accepted:       {len(accepted)}  -> {OUT.relative_to(ROOT)}")
    print(f"Rejected/skipped:      {len(rejected)}  -> {REJECTED_OUT.relative_to(ROOT)}")

    # Top patterns in accepted
    from collections import Counter
    pats = Counter((x["current_denomination"], x["proposed_denomination"]) for x in accepted)
    print()
    print("Top accepted patterns:")
    for (a, b), n in pats.most_common(10):
        print(f"  {n:3}  {a}  ->  {b}")


if __name__ == "__main__":
    main()
