#!/usr/bin/env python3
"""
merge_enrichment_patches.py - merge N enrichment patch files into churches.json.

Input: one or more patch files (JSON array of patch objects with church id).
Output: updated docs/data/churches.json + a merge report.

Rules:
  - Patches never create new churches - they only update existing ones.
  - Only non-null, non-empty fields from the patch are applied.
  - scores and score_notes are merged per-key (patch values win where present).
  - If flag_for_review is true, the entry gets a tag 'needs-review' and a
    top-level 'review_flag' field (not lost on regen).
  - A summary report prints counts: patched, skipped, flagged, rating changes.
"""

import argparse
import json
import sys
from pathlib import Path


SCALAR_FIELDS_PATCHABLE = [
    "overall_rating",
    "overall_label",
    "pastor",
    "pastor_credentials",
    "founded",
    "denomination_detail",
    "gender_detail",
    "assessment",
]


def load_patches(paths):
    patches = []
    for p in paths:
        with open(p) as f:
            data = json.load(f)
        if isinstance(data, list):
            patches.extend(data)
        elif isinstance(data, dict) and "patches" in data:
            patches.extend(data["patches"])
        else:
            print(f"WARN: {p} is not a list or {{patches:[...]}} object — skipping", file=sys.stderr)
    return patches


def apply_patch(church, patch):
    changes = []
    # Rating change tracking
    old_rating = church.get("overall_rating")
    new_rating = patch.get("overall_rating")
    if new_rating and new_rating != old_rating:
        changes.append(("overall_rating", old_rating, new_rating))

    # Scalars
    for field in SCALAR_FIELDS_PATCHABLE:
        v = patch.get(field)
        if v not in (None, "", "null") and v != church.get(field):
            church[field] = v

    # scores dict — per-key merge
    if isinstance(patch.get("scores"), dict):
        sc = church.setdefault("scores", {})
        for dim, val in patch["scores"].items():
            if val and val != sc.get(dim):
                sc[dim] = val

    # score_notes dict — per-key merge (only overwrite Verify/Unknown/empty)
    if isinstance(patch.get("score_notes"), dict):
        notes = church.setdefault("score_notes", {})
        for dim, val in patch["score_notes"].items():
            if not val:
                continue
            existing = (notes.get(dim) or "").strip().lower()
            # Overwrite placeholders, or overwrite if new note is substantively different
            if existing in ("", "verify", "verify.", "unknown", "unknown."):
                notes[dim] = val
            elif len(val) > 20 and val != notes.get(dim):
                # Trust the patch if it's a substantive note (not just a single word)
                notes[dim] = val

    # Flag for review
    if patch.get("flag_for_review"):
        church["review_flag"] = {
            "flagged": True,
            "reason": patch.get("review_reason") or "flagged by enrichment agent",
            "website_status": patch.get("website_status"),
        }
        tags = church.setdefault("tags", [])
        if "needs-review" not in tags:
            tags.append("needs-review")

    # sources_consulted -> store for audit
    if patch.get("sources_consulted"):
        church["enrichment_sources"] = patch["sources_consulted"]
    if patch.get("enrichment_notes"):
        church["enrichment_notes"] = patch["enrichment_notes"]

    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--churches", default="docs/data/churches.json")
    ap.add_argument("--patches", nargs="+", required=True, help="One or more patch JSON files")
    ap.add_argument("--output", default=None, help="Defaults to overwriting --churches")
    ap.add_argument("--report", default="tmp/enrichment_merge_report.json")
    args = ap.parse_args()

    churches_path = Path(args.churches)
    with open(churches_path) as f:
        data = json.load(f)

    by_id = {c["id"]: c for c in data["churches"]}
    patches = load_patches(args.patches)

    report = {
        "input_patch_count": len(patches),
        "patched": 0,
        "skipped_unknown_id": [],
        "flagged_for_review": [],
        "rating_changes": [],
    }

    for p in patches:
        cid = p.get("id")
        if not cid:
            continue
        church = by_id.get(cid)
        if not church:
            report["skipped_unknown_id"].append(cid)
            continue
        changes = apply_patch(church, p)
        report["patched"] += 1
        for field, old, new in changes:
            if field == "overall_rating":
                report["rating_changes"].append({
                    "id": cid,
                    "name": church.get("name"),
                    "old": old,
                    "new": new,
                })
        if p.get("flag_for_review"):
            report["flagged_for_review"].append({
                "id": cid,
                "name": church.get("name"),
                "reason": p.get("review_reason"),
                "website_status": p.get("website_status"),
            })

    output_path = Path(args.output) if args.output else churches_path
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    with open(args.report, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Merged {report['patched']} patches into {output_path}")
    print(f"Skipped unknown ids: {len(report['skipped_unknown_id'])}")
    print(f"Flagged for review: {len(report['flagged_for_review'])}")
    print(f"Rating changes: {len(report['rating_changes'])}")
    for rc in report["rating_changes"]:
        print(f"  {rc['old']:6s} -> {rc['new']:6s}  {rc['id']}")


if __name__ == "__main__":
    main()
