#!/usr/bin/env python3
"""
Append new church records (from a green-hunter agent or similar) to
docs/data/churches.json.

Validates:
  - No ID collisions with existing records
  - Required fields present (id, name, address, denomination, website,
    overall_rating, scores, score_notes)
  - score_notes is a dict (NOT a string — prior agent bug)
  - scores is a dict

Usage:
    python3 scripts/append_new_churches.py tmp/va_green_hunter_out.json
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
CHURCHES = ROOT / "docs/data/churches.json"

REQUIRED = ["id", "name", "address", "denomination", "website",
            "overall_rating", "scores", "score_notes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patches", help="JSON file with new church records (array)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    new = json.loads(Path(args.patches).read_text())
    if not isinstance(new, list):
        sys.exit("ERROR: patches file must be an array of church records")

    data = json.loads(CHURCHES.read_text())
    churches = data if isinstance(data, list) else data.get("churches", data)
    existing_ids = {c.get("id") for c in churches}

    issues = []
    valid = []
    for r in new:
        for f in REQUIRED:
            if not r.get(f):
                # pastor is REQUIRED but accept empty string with placeholder fill
                if f == "pastor":
                    r["pastor"] = r.get("pastor") or "Verify on visit"
                    continue
                issues.append(f'{r.get("id","?")}: missing {f}')
                break
        else:
            if r["id"] in existing_ids:
                issues.append(f'{r["id"]}: ID collision with existing record')
                continue
            if not isinstance(r.get("score_notes"), dict):
                issues.append(f'{r["id"]}: score_notes not dict (got {type(r.get("score_notes")).__name__})')
                continue
            if not isinstance(r.get("scores"), dict):
                issues.append(f'{r["id"]}: scores not dict')
                continue
            # Set pastor placeholder if empty
            if not r.get("pastor"):
                r["pastor"] = "Verify on visit"
            valid.append(r)

    print(f"Input records:      {len(new)}")
    print(f"Valid for append:   {len(valid)}")
    print(f"Issues:             {len(issues)}")
    for i in issues:
        print(f"  - {i}")

    if args.dry_run:
        print("DRY RUN — not writing")
        return

    if isinstance(data, list):
        data.extend(valid)
        new_total = len(data)
    else:
        data.setdefault("churches", []).extend(valid)
        data["total_churches"] = len(data["churches"])
        new_total = len(data["churches"])

    CHURCHES.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nAppended {len(valid)} records. Total churches: {new_total}")


if __name__ == "__main__":
    main()
