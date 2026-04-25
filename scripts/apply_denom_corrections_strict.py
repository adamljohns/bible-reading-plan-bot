#!/usr/bin/env python3
"""
Apply the strict-accepted denom corrections from
tmp/denom_corrections_strict.json to docs/data/churches.json.

For each church:
  1. Set `denomination` to the proposed_denomination string
  2. Set `denomination_family` to the canonical family for the new denom
  3. Append a one-line note to enrichment_notes documenting the auto-correction
     with date and source

Does NOT change `overall_rating`, `scores`, `score_notes`, or anything else.
Prior agent rounds have already adjusted those — this purely cleans up the
denomination field which had been left stale.

Usage:
    python3 scripts/apply_denom_corrections_strict.py [--dry-run]
"""
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
ACCEPTED = ROOT / "tmp/denom_corrections_strict.json"
CHURCHES = ROOT / "docs/data/churches.json"

# Canonical family for each proposed bucket / denom
FAMILY_MAP = {
    "CBF": "Progressive Mainline",
    "ABC-USA": "Progressive Mainline",
    "ABCUSA": "Progressive Mainline",
    "BGAV": "Baptist (BGAV)",
    "ELCA": "Progressive Mainline",
    "PCUSA": "Presbyterian (PCUSA)",
    "EPC": "Presbyterian (EPC)",
    "UMC": "Methodist (UMC)",
    "GMC": "Methodist (GMC)",
    "IFB": "Independent Baptist",
}


def family_for(prop_bucket: str, prop_full: str) -> str:
    """Map a proposed bucket/full name to a canonical denomination_family."""
    if prop_bucket and prop_bucket in FAMILY_MAP:
        return FAMILY_MAP[prop_bucket]
    pf = (prop_full or "").lower()
    if "cooperative baptist" in pf:
        return FAMILY_MAP["CBF"]
    if "american baptist" in pf:
        return FAMILY_MAP["ABCUSA"]
    if "baptist general association of virginia" in pf:
        return FAMILY_MAP["BGAV"]
    if "evangelical lutheran church in america" in pf:
        return FAMILY_MAP["ELCA"]
    if "presbyterian church (usa)" in pf:
        return FAMILY_MAP["PCUSA"]
    if "evangelical presbyterian church" in pf:
        return FAMILY_MAP["EPC"]
    if "united methodist" in pf:
        return FAMILY_MAP["UMC"]
    if "global methodist" in pf:
        return FAMILY_MAP["GMC"]
    if "independent baptist" in pf:
        return FAMILY_MAP["IFB"]
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    accepted = json.loads(ACCEPTED.read_text())
    data = json.loads(CHURCHES.read_text())
    churches = data if isinstance(data, list) else data.get("churches", data)
    by_id = {c["id"]: c for c in churches if "id" in c}

    today = date.today().isoformat()
    changes = []
    for x in accepted:
        rec = by_id.get(x["id"])
        if not rec:
            continue
        old_denom = rec.get("denomination", "")
        old_family = rec.get("denomination_family", "")
        new_denom = x["proposed_denomination"]
        new_family = family_for(x.get("proposed_bucket", ""), new_denom)

        rec["denomination"] = new_denom
        if new_family:
            rec["denomination_family"] = new_family

        # Append audit note
        marker = (
            f"\n--- {today} V4.9.2 auto-denom-correction: {old_denom!r} -> {new_denom!r}"
            f" (family: {old_family!r} -> {new_family!r}) per V4.9 detector + prior research notes."
        )
        rec["enrichment_notes"] = (rec.get("enrichment_notes") or "") + marker

        changes.append({
            "id": x["id"],
            "name": rec.get("name"),
            "old_denom": old_denom,
            "new_denom": new_denom,
            "old_family": old_family,
            "new_family": new_family,
        })

    print(f"Applying {len(changes)} denomination corrections")
    print()
    print(f"{'ID':50} {'OLD DENOM':30} -> {'NEW DENOM':40}")
    for c in changes:
        old = (c["old_denom"] or "")[:28]
        new = (c["new_denom"] or "")[:38]
        print(f"  {c['id']:50} {old:30} -> {new}")

    if args.dry_run:
        print()
        print("DRY RUN — no changes written")
        return

    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print()
    print(f"Wrote {CHURCHES}")


if __name__ == "__main__":
    main()
