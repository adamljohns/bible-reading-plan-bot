#!/usr/bin/env python3
"""Detect denomination mis-tags in churches.json.

Heuristic patterns:
  a) ID/family says SBC/PCA but enrichment_notes says CBF/CBFV/BGAV/PCUSA/EPC/independent
  b) denomination_detail or score_notes contains alternate denomination keywords that
     don't match `denomination`
  c) score_notes mention egalitarian/woman-pastor while denomination is conservative-
     complementarian (SBC/PCA/ARP/EPC/OPC/CREC/etc.)
  d) enrichment_notes mention denominational transition ("left PCA", "joined CREC",
     "now ARP", "post-split UMC")
  e) ID has -sbc- infix but actual denomination_detail says CBF/independent

Output: tmp/denom_correction_proposals.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CHURCHES = Path("/Users/adamjohns/bible-reading-plan-bot/docs/data/churches.json")
OUT = Path("/Users/adamjohns/bible-reading-plan-bot/tmp/denom_correction_proposals.json")

# --- denomination canonical buckets ---
# (regex, canonical_label) used to detect what a record is "claimed" to be vs
# what evidence text suggests.
CANONICAL_KEYWORDS = {
    # conservative complementarian
    "SBC":   [r"\bsouthern baptist\b", r"\bSBC\b", r"\bSBCV\b"],
    "PCA":   [r"\bpresbyterian church in america\b", r"\bPCA\b"],
    "OPC":   [r"\borthodox presbyterian\b", r"\bOPC\b"],
    "ARP":   [r"\bassociate reformed presbyterian\b", r"\bARP\b"],
    "EPC":   [r"\bevangelical presbyterian church\b", r"\bEPC\b"],
    "ECO":   [r"\bECO\b", r"\bcovenant order of evangelical presbyterians\b"],
    "CREC":  [r"\bCREC\b", r"\bcommunion of reformed evangelical\b"],
    "URCNA": [r"\bURCNA\b", r"\bunited reformed church\b"],
    "CRC":   [r"\bchristian reformed church\b", r"\bCRCNA\b"],
    "RCA":   [r"\breformed church in america\b", r"\bRCA\b"],
    "FreeMethodist": [r"\bfree methodist\b"],
    "GMC":   [r"\bglobal methodist\b", r"\bGMC\b"],
    "WesleyanChurch": [r"\bwesleyan church\b"],
    "ARC":   [r"\bassociation of related churches\b", r"\bARC\b"],
    "Acts29":[r"\bacts ?29\b"],
    "EvFreeEFCA": [r"\bevangelical free\b", r"\bEFCA\b"],
    "PresbyterianConservative": [r"\bconservative presbyterian\b"],

    # mainline / progressive
    "PCUSA": [r"\bPC\(USA\)\b", r"\bPCUSA\b", r"\bpresbyterian church \(usa\)\b",
              r"\bpresbyterian church usa\b"],
    "UMC":   [r"\bUMC\b", r"\bunited methodist\b"],
    "ELCA":  [r"\bELCA\b", r"\bevangelical lutheran church in america\b"],
    "TEC":   [r"\bepiscopal church\b", r"\bTEC\b"],
    "UCC":   [r"\bunited church of christ\b", r"\bUCC\b"],
    "DOC":   [r"\bdisciples of christ\b"],

    # moderate baptist
    "CBF":   [r"\bcooperative baptist fellowship\b", r"\bCBF\b", r"\bCBFV\b"],
    "BGAV":  [r"\bBGAV\b", r"\bbaptist general association of virginia\b"],
    "ABC":   [r"\bABCUSA\b", r"\bABC-USA\b", r"\bAmerican Baptist Churches\b",
              r"\bABC USA\b"],
    "NBC":   [r"\bNBC[- ]?USA\b", r"\bnational baptist convention\b"],

    # other
    "IndependentBaptist": [r"\bindependent fundamental baptist\b",
                           r"\bindependent baptist\b"],
    "LCMS":  [r"\bLCMS\b", r"\blutheran church[- ]missouri synod\b"],
}

# Compile
COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in CANONICAL_KEYWORDS.items()}

# What canonical bucket(s) does a `denomination` field claim?
def bucket_of_denomination(denom: str, family: str = "") -> set[str]:
    text = f"{denom} {family}".strip()
    if not text:
        return set()
    out = set()
    for label, pats in COMPILED.items():
        for p in pats:
            if p.search(text):
                out.add(label)
                break
    return out


# What canonical buckets are mentioned in evidence text?
def buckets_in_evidence(text: str) -> set[str]:
    if not text:
        return set()
    out = set()
    for label, pats in COMPILED.items():
        for p in pats:
            if p.search(text):
                out.add(label)
                break
    return out


# Pairs of denominations that should never coexist on a single church
# (claimed_set, evidence_set) -> if claimed bucket is in claim_keys and
# evidence bucket is in evidence_keys, that's a mis-tag candidate.
INCOMPATIBLE_PAIRS = {
    # SBC vs moderate/independent baptist family
    ("SBC", "CBF"):   "high",
    ("SBC", "BGAV"):  "high",
    ("SBC", "ABC"):   "high",
    ("SBC", "NBC"):   "high",
    ("SBC", "IndependentBaptist"): "medium",
    # PCA vs other Presbyterian
    ("PCA", "PCUSA"): "high",
    ("PCA", "EPC"):   "high",
    ("PCA", "ECO"):   "high",
    ("PCA", "ARP"):   "medium",
    ("PCA", "OPC"):   "medium",
    ("PCA", "CREC"):  "medium",
    # OPC->other
    ("OPC", "PCA"):   "low",
    ("OPC", "PCUSA"): "high",
    # PCUSA mistagged as conservative
    ("PCUSA", "PCA"): "high",
    ("PCUSA", "EPC"): "medium",
    # Methodist groups
    ("UMC", "GMC"):           "high",
    ("UMC", "FreeMethodist"): "high",
    ("UMC", "WesleyanChurch"): "high",
    ("FreeMethodist", "UMC"): "high",
    ("GMC", "UMC"):           "high",
    # Lutheran
    ("ELCA", "LCMS"): "high",
    ("LCMS", "ELCA"): "high",
    # Reformed
    ("CRC", "RCA"):   "medium",
    ("RCA", "CRC"):   "medium",
}


EGALITARIAN_PATTERNS = [
    r"\bfemale (?:senior|lead|teaching|associate|preaching) pastor\b",
    r"\bwoman (?:senior|lead|teaching|associate|preaching) pastor\b",
    r"\bwomen (?:as )?pastors?\b",
    r"\bwomen (?:as )?elders?\b",
    r"\bwomen (?:as )?deacons?\b",
    r"\bfemale (?:senior |lead |associate )?elder\b",
    r"\begalitarian\b",
    r"\bordains? women\b",
    r"\bordain women\b",
    r"\bRev\.\s+(?:Ms|Mrs|Sister|Dr\.?\s+Mrs|Pastor)\s+[A-Z][a-z]+",
]

# Phrases that NEGATE the egalitarian signal when appearing nearby
EGALITARIAN_NEGATIONS = [
    r"\b(?:does\s+not|do\s+not|doesn['\u2019]?t|don['\u2019]?t|will\s+not|cannot|can['\u2019]?t)\s+",
    r"\b(?:no|never|not)\s+",
    r"\bmale[- ]only\b",
    r"\bcomplementarian\s+by\b",
    r"\bagainst\b",
    r"\bprohibit",
    r"\brestrict",
    r"\bopposes?\b",
    r"\bdeny\s+(?:the\s+ordination|women)\b",
    r"\bwithholds?\s+",
    r"\bbar\s+",
    r"\bbarred\b",
    r"\bbars\b",
    r"\bonly\s+men\b",
    r"\bmen\s+only\b",
    r"\bresist\w*\s+to\s+\w*\s*",
    r"\bresist\w*\s+",
    r"\bdrift\b",  # 'egalitarian drift' = bad, not endorsing
    r"\bagainst\s+\w*\s*",
    r"\brejects?\b",
    r"\bopposed\s+to\b",
]


# Phrases that show the egalitarian-keyword is in a *neutral* / verification
# context (not a positive claim that the church IS egalitarian)
EGALITARIAN_NEUTRAL_CONTEXTS = [
    r"\bverify\b",
    r"\bunclear\b",
    r"\bcomplementarian/egalitarian\b",  # 'verify complementarian/egalitarian'
    r"\bcomplementarian\s+or\s+egalitarian\b",
    r"\bnot\s+verified\b",
    r"\bunknown\b",
    r"\bnot\s+yet\b",
    r"\b(?:to\s+)?be\s+confirmed\b",
    r"\bTBD\b",
    r"\bcheck\b",
    r"\bdetermine\b",
    r"\bconfirm\b",
]


def egalitarian_hits(text: str) -> list[str]:
    """Return phrases suggesting egalitarian / female-pastor practice.
    Skips matches inside negation/contrast/verification contexts."""
    if not text:
        return []
    found: list[str] = []
    for pat in EGALITARIAN_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            ctx_lo = max(0, m.start() - 80)
            ctx_hi = min(len(text), m.end() + 80)
            pre = text[ctx_lo:m.start()]
            window = text[ctx_lo:ctx_hi]
            # Negation prior to match
            negated = any(
                re.search(neg, pre[-60:], re.I) for neg in EGALITARIAN_NEGATIONS
            )
            if negated:
                continue
            # Neutral / verification context anywhere in the window
            neutral = any(
                re.search(np, window, re.I) for np in EGALITARIAN_NEUTRAL_CONTEXTS
            )
            if neutral:
                continue
            found.append(m.group(0))
    return found


# Conservative-complementarian buckets that conflict with egalitarian evidence
CONSERVATIVE_COMP = {"SBC", "PCA", "OPC", "ARP", "PCUSA"}  # (PCUSA tagged but actually
# accepts women — included only because if claimed=PCA/SBC and evidence is egalitarian,
# that often means CBF/PCUSA/UMC underneath. We treat egalitarian as evidence FOR
# mis-tag, not against.)
# Note: EPC permits women's ordination at congregational option, so women-elder
# evidence in an EPC church is NOT a mis-tag. ARP also permits women deacons.
COMPLEMENTARIAN_ONLY = {"SBC", "PCA", "OPC", "CREC", "URCNA", "LCMS"}


# Transition phrases pointing to a denominational change
TRANSITION_PATTERNS = [
    (r"\bleft (?:the )?PCA\b",        "PCA",  None),
    (r"\bleft (?:the )?SBC\b",        "SBC",  None),
    (r"\bleft (?:the )?UMC\b",        "UMC",  None),
    (r"\bleft (?:the )?PC\(?USA\)?\b","PCUSA",None),
    (r"\bjoined (?:the )?CREC\b",     None,   "CREC"),
    (r"\bjoined (?:the )?ARP\b",      None,   "ARP"),
    (r"\bjoined (?:the )?GMC\b",      None,   "GMC"),
    (r"\bjoined (?:the )?EPC\b",      None,   "EPC"),
    (r"\bnow ARP\b",                  None,   "ARP"),
    (r"\bnow GMC\b",                  None,   "GMC"),
    (r"\bnow EPC\b",                  None,   "EPC"),
    (r"\bnow CREC\b",                 None,   "CREC"),
    (r"\bnow PCA\b",                  None,   "PCA"),
    (r"\bdisaffiliated from (?:the )?UMC\b", "UMC", None),
    (r"\bdisaffiliated from (?:the )?SBC\b", "SBC", None),
    (r"\bpost-split UMC\b",           None,   "UMC"),
    (r"\btransitioned to\b",          None,   None),
]


NEGATION_CONTEXTS = [
    # patterns where a denom keyword is mentioned to NEGATE/CONTRAST,
    # not to claim the church belongs there
    r"\bnot\s+(?:also\s+)?{KW}\b",
    r"\bno\s+{KW}\b",
    r"\bnot\s+to\s+be\s+confused\s+with\s+{KW}\b",
    r"\bagainst\s+{KW}\b",
    r"\bagainst\s+(?:modernism\s+in\s+the\s+)?{KW}\b",
    r"\bvs\.?\s+{KW}\b",
    r"\b(?:left|leaving|departed|broke\s+from|disaffiliated?\s+from|disaffiliate\s+from)\s+(?:the\s+)?{KW}\b",
    r"\bbreakaway\s+from\s+{KW}\b",
    r"\bdisaffiliated?\s+from\s+(?:the\s+)?{KW}\b",
    r"\bvoted\s+to\s+disaffiliate\s+from\s+(?:the\s+)?{KW}\b",
    r"\bwithdrew\s+from\s+(?:the\s+)?{KW}\b",
    r"\bexpelled\s+(?:from|by)\s+(?:the\s+)?{KW}\b",
    r"\bremoved\s+from\s+(?:the\s+)?{KW}\b",
    r"\bformerly\s+{KW}\b",
    r"\bex-{KW}\b",
    r"\bpre-{KW}\b",
    r"\bnon-?{KW}\b",
    r"\bdistinguish[a-z]*\s+from\s+{KW}\b",
    r"\bvery\s+different\s+from\s+{KW}\b",
    r"\bunlike\s+{KW}\b",
    r"\bagainst\s+modernism\s+in\s+the\s+{KW}\b",
    # founding-history mentions ("founded ... in 1936 ... PCUSA")
    r"\bfounded\s+\d{4}[^.]{0,60}{KW}\b",
    r"\bsplit\s+from\s+{KW}\b",
    r"\bseparated\s+from\s+{KW}\b",
    r"\bverify\b[^.]{0,60}{KW}\b",
    r"\bcaught\b[^.]{0,40}{KW}[^.]{0,40}mis[- ]tag",
    # broader-context phrases ("conservative churches departed to GMC" — not THIS one)
    r"\b(?:other|many|some|most|conservative|progressive|moderate|several)\s+churches?\b[^.]{0,80}{KW}\b",
    r"\bchurches\s+(?:departed|left|joined|migrated)\s+(?:to\s+)?{KW}\b",
    r"\bdeparted\s+to\s+{KW}\b",
    r"\bremaining\s+(?:post-?disaffiliation|in)\s+{KW}\b",
]


def collect_negated_buckets(text: str) -> set[str]:
    """Look for 'not X, Y, or Z (affiliated|aligned|tagged|...)' patterns and
    return the set of buckets contained inside such lists."""
    if not text:
        return set()
    out: set[str] = set()
    # Find every span like "not <words and commas> (affiliated|aligned|tagged|tied|connected)"
    # Allow up to 80 chars in the list.
    for m in re.finditer(
        r"\bnot\s+([A-Za-z0-9 ,\-\(\)/]{1,80}?)\s*(?:affiliated|aligned|tagged|"
        r"tied|connected|related|associated|members?|in)\b",
        text,
        re.I,
    ):
        chunk = m.group(1)
        out |= buckets_in_evidence(chunk)
    return out


def evidence_negated(text: str, bucket: str) -> bool:
    """Return True if every mention of bucket keywords in text is in a
    negation/contrast context, OR if claim is buttressed elsewhere in text."""
    if not text:
        return True
    pats = COMPILED.get(bucket, [])
    # Find every match span for any keyword of this bucket
    spans: list[tuple[int, int]] = []
    for p in pats:
        for m in p.finditer(text):
            spans.append(m.span())
    if not spans:
        return True
    # For each span, check if surrounding context is negation
    for s, e in spans:
        ctx_lo = max(0, s - 60)
        ctx_hi = min(len(text), e + 60)
        ctx = text[ctx_lo:ctx_hi]
        kw = text[s:e]
        kw_re = re.escape(kw)
        is_neg = False
        for tmpl in NEGATION_CONTEXTS:
            pat = tmpl.replace("{KW}", kw_re)
            if re.search(pat, ctx, re.I):
                is_neg = True
                break
        if not is_neg:
            return False  # at least one positive mention — not negated
    return True  # all mentions are in negation contexts


def claim_corroborated(text: str, bucket: str) -> bool:
    """Returns True if the evidence text positively confirms the claimed bucket
    (so any mention of an alternative is likely contrast)."""
    if not text or bucket not in COMPILED:
        return False
    pats = COMPILED[bucket]
    confirm_phrases = [
        r"affiliation\s+confirmed",
        r"{KW}\s+affiliation",
        r"member\s+of\s+(?:the\s+)?{KW}",
        r"confirmed\s+(?:via|on|through)?\s*{KW}",
        r"locator\.{KW}",
        r"explicitly\s+{KW}",
        r"{KW}\s+congregation\s+confirmed",
    ]
    for p in pats:
        for m in p.finditer(text):
            kw = text[m.start():m.end()]
            kw_re = re.escape(kw)
            for cp in confirm_phrases:
                cp_re = cp.replace("{KW}", kw_re)
                ctx_lo = max(0, m.start() - 80)
                ctx_hi = min(len(text), m.end() + 80)
                if re.search(cp_re, text[ctx_lo:ctx_hi], re.I):
                    return True
    return False


def detect(c: dict) -> dict | None:
    cid = c.get("id", "")
    name = c.get("name", "")
    denom = c.get("denomination", "") or ""
    family = c.get("denomination_family", "") or ""
    detail = c.get("denomination_detail", "") or ""
    enrich = c.get("enrichment_notes", "") or ""
    score_notes = c.get("score_notes", {}) or {}
    if isinstance(score_notes, dict):
        score_text = " | ".join(f"{k}: {v}" for k, v in score_notes.items() if v)
    else:
        score_text = str(score_notes)
    assessment = c.get("assessment", "") or ""

    evidence_text = " || ".join([detail, enrich, score_text, assessment])

    claimed = bucket_of_denomination(denom, family)
    detected = buckets_in_evidence(evidence_text)
    # Buckets explicitly disclaimed via "not X, Y, or Z affiliated"
    excluded = collect_negated_buckets(evidence_text)

    reasons: list[str] = []
    proposed: str | None = None
    confidences: list[str] = []

    # (a/b/e) explicit incompatible pair
    for cl in claimed:
        # If claim is positively corroborated, alternative buckets in text are
        # almost certainly contrast/history, not mis-tag evidence.
        cl_corroborated = claim_corroborated(evidence_text, cl)
        for ev in detected:
            if cl == ev:
                continue
            if ev in excluded:
                continue
            conf = INCOMPATIBLE_PAIRS.get((cl, ev))
            if not conf:
                continue
            # Skip if the alternative bucket only appears in negation/contrast
            if evidence_negated(evidence_text, ev):
                continue
            # Skip if claim is corroborated AND alternative is mentioned only
            # in a clause that doesn't independently affirm membership
            if cl_corroborated:
                continue
            reasons.append(
                f"claimed '{cl}' but evidence text contains '{ev}' keywords"
            )
            proposed = ev
            confidences.append(conf)

    # (e) ID infix vs detail mismatch (catches cases where `denomination` is
    # already vague but the ID is wrong)
    id_low = cid.lower()
    if "-sbc-" in id_low or id_low.startswith("sbc-"):
        for ev in detected:
            if ev != "SBC" and ev in {"CBF", "BGAV", "ABC", "NBC", "IndependentBaptist"}:
                reasons.append(f"ID has -sbc- infix but evidence cites {ev}")
                proposed = proposed or ev
                confidences.append("medium")
    if "-pca-" in id_low or id_low.startswith("pca-"):
        for ev in detected:
            if ev != "PCA" and ev in {"PCUSA", "EPC", "ECO", "ARP", "OPC", "CREC"}:
                reasons.append(f"ID has -pca- infix but evidence cites {ev}")
                proposed = proposed or ev
                confidences.append("medium")

    # (c) egalitarian phrases under complementarian-only claim
    # Only fire if the evidence text itself doesn't ALREADY say the church
    # left/disaffiliated (those go through pattern d below with proper proposal)
    if claimed & COMPLEMENTARIAN_ONLY:
        eg = egalitarian_hits(evidence_text)
        # Don't double-flag if the church is described as left/ex-/now-
        already_transitioned = bool(
            re.search(
                r"\b(?:left|departed|disaffiliated|ex-|now\s+(?:non-?denom|independent))",
                evidence_text,
                re.I,
            )
        )
        if eg and not already_transitioned:
            reasons.append(
                f"complementarian-only denomination tag but evidence shows: "
                f"{', '.join(sorted(set(eg))[:3])}"
            )
            for guess in ("CBF", "BGAV", "ABC", "PCUSA", "UMC", "ELCA"):
                if guess in detected:
                    proposed = proposed or guess
                    break
            confidences.append("medium")

    # (d) transition phrases
    for pat, from_b, to_b in TRANSITION_PATTERNS:
        m = re.search(pat, evidence_text, re.I)
        if m:
            # If currently still tagged as the "from" bucket, that's a mis-tag
            if from_b and from_b in claimed:
                reasons.append(f"transition phrase: '{m.group(0)}' (was {from_b})")
                if to_b:
                    proposed = proposed or to_b
                else:
                    # try to read a "now non-denominational" / "now independent"
                    nd = re.search(
                        r"\bnow\s+(?:explicitly\s+)?(non-?denominational|independent)",
                        evidence_text,
                        re.I,
                    )
                    if nd:
                        proposed = proposed or "Independent/Non-Denominational"
                confidences.append("high")
            elif to_b and to_b not in claimed and claimed:
                # "now ARP" but we didn't tag ARP
                reasons.append(f"transition phrase: '{m.group(0)}' (now {to_b})")
                proposed = proposed or to_b
                confidences.append("high")

    if not reasons:
        return None

    # Compose proposed denomination label (human-friendly)
    PRETTY = {
        "SBC":   "Southern Baptist Convention (SBC)",
        "PCA":   "Presbyterian Church in America (PCA)",
        "OPC":   "Orthodox Presbyterian Church (OPC)",
        "ARP":   "Associate Reformed Presbyterian (ARP)",
        "EPC":   "Evangelical Presbyterian Church (EPC)",
        "ECO":   "ECO: A Covenant Order of Evangelical Presbyterians",
        "CREC":  "Communion of Reformed Evangelical Churches (CREC)",
        "URCNA": "United Reformed Churches in North America (URCNA)",
        "CRC":   "Christian Reformed Church (CRC)",
        "RCA":   "Reformed Church in America (RCA)",
        "PCUSA": "Presbyterian Church (USA)",
        "UMC":   "United Methodist Church (UMC)",
        "ELCA":  "Evangelical Lutheran Church in America (ELCA)",
        "LCMS":  "Lutheran Church-Missouri Synod (LCMS)",
        "TEC":   "The Episcopal Church",
        "UCC":   "United Church of Christ",
        "DOC":   "Christian Church (Disciples of Christ)",
        "CBF":   "Cooperative Baptist Fellowship (CBF)",
        "BGAV":  "Baptist General Association of Virginia (BGAV)",
        "ABC":   "American Baptist Churches USA (ABC-USA)",
        "NBC":   "National Baptist Convention USA (NBC-USA)",
        "IndependentBaptist": "Independent Baptist",
        "FreeMethodist": "Free Methodist",
        "GMC":   "Global Methodist Church (GMC)",
        "WesleyanChurch": "The Wesleyan Church",
        "Independent/Non-Denominational": "Independent / Non-Denominational",
    }

    confidence = "low"
    if "high" in confidences:
        confidence = "high"
    elif "medium" in confidences:
        confidence = "medium"

    return {
        "id": cid,
        "name": name,
        "current_denomination": denom,
        "current_family": family,
        "proposed_denomination": PRETTY.get(proposed, proposed) if proposed else None,
        "proposed_bucket": proposed,
        "evidence": " ; ".join(reasons),
        "confidence": confidence,
        "denomination_detail": detail[:300],
        "enrichment_notes": enrich[:300],
    }


def main() -> None:
    with CHURCHES.open() as f:
        data = json.load(f)
    churches = data["churches"]

    proposals: list[dict] = []
    for c in churches:
        prop = detect(c)
        if prop:
            proposals.append(prop)

    # Sort: high-confidence first, then medium, then low
    rank = {"high": 0, "medium": 1, "low": 2}
    proposals.sort(key=lambda p: (rank.get(p["confidence"], 9), p["id"]))

    OUT.write_text(json.dumps(proposals, indent=2))

    # Summary
    print(f"Total churches scanned: {len(churches)}")
    print(f"Suspect records:        {len(proposals)}")
    print()

    by_conf: dict[str, int] = {}
    pair_counts: dict[str, int] = {}
    for p in proposals:
        by_conf[p["confidence"]] = by_conf.get(p["confidence"], 0) + 1
        # Build a pair key from claimed -> proposed
        cur_buckets = bucket_of_denomination(
            p["current_denomination"], p["current_family"]
        )
        cur = next(iter(cur_buckets), p["current_denomination"][:20] or "?")
        pair = f"{cur} -> {p['proposed_bucket'] or '?'}"
        pair_counts[pair] = pair_counts.get(pair, 0) + 1

    print("By confidence:")
    for k in ("high", "medium", "low"):
        print(f"  {k:6s} {by_conf.get(k, 0)}")
    print()
    print("Top denomination pairs:")
    for pair, n in sorted(pair_counts.items(), key=lambda kv: -kv[1])[:20]:
        print(f"  {n:4d}  {pair}")


if __name__ == "__main__":
    main()
