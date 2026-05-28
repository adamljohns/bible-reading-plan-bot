#!/usr/bin/env python3
"""
Build per-state shards of docs/data/churches.json.

WHY:
  churches.json is 58 MB and growing. GitHub warns at 50 MB; the next
  bulk-add waves will push past 100 MB. Page loaders that fetch the
  whole file (e.g., the churches.html footer count, per-state pages)
  pay the full transfer cost even when they only need a single state.

  This script produces narrow per-state JSON shards alongside the
  monolithic file. The monolith remains the source of truth (no other
  workflow needs to change immediately) — pages and scripts can
  migrate to shards opportunistically.

OUTPUTS:
  docs/data/churches/by-state/{xx}.json      One file per US state +
                                              DC; lowercase 2-letter
                                              code. Each shard has the
                                              same top-level shape as
                                              churches.json but with a
                                              subset of `churches`.
  docs/data/churches/by-state/_unstated.json  Records that have no
                                              `state` field. (Should
                                              be ~1,063 after V7.0.1.)
  docs/data/churches/by-state/_index.json     Summary: per-state counts,
                                              shard byte sizes, total
                                              records, generated_at.

INVARIANT:
  sum(shard.churches for shard in {xx}.json) + _unstated.churches
    == churches.json.churches

RE-RUN:
  python3 scripts/build_state_shards.py
  (idempotent — safe to re-run after any churches.json change)
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/adamjohns/bible-reading-plan-bot")
SOURCE = ROOT / "docs/data/churches.json"
OUT_DIR = ROOT / "docs/data/churches/by-state"

US_STATES = sorted('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split())


def main():
    print(f"Reading {SOURCE.relative_to(ROOT)}...")
    data = json.loads(SOURCE.read_text())
    churches = data.get("churches", [])
    total_input = len(churches)
    print(f"  {total_input} records")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Shared metadata copied to every shard so each shard is self-describing.
    # The rubric is included so page loaders can render the per-record scorecard
    # WITHOUT a second fetch of the 58 MB monolith just for rubric labels.
    meta = {
        "directory_version": data.get("directory_version"),
        "directory_updated": data.get("directory_updated"),
        "shard_source": "docs/data/churches.json",
        "shard_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "shard_format_version": 2,  # bumped: shards now carry rubric
        "rubric": data.get("rubric"),
    }

    # Group records by state. Records with a country_code != 'US' get routed
    # to the international shard instead of _unstated, since they're properly
    # classified, just not US.
    by_state = defaultdict(list)
    by_country = defaultdict(list)  # international shard contents
    unstated = []
    case_warning = []
    foreign_or_unknown = []  # records with state field that's not a US code

    for c in churches:
        state = c.get("state")
        country_code = c.get("country_code")

        # Path 1: Has a US state — route to state shard
        if state and isinstance(state, str):
            state_upper = state.strip().upper()
            if state_upper in US_STATES:
                if state != state_upper:
                    case_warning.append(c["id"])
                by_state[state_upper].append(c)
                continue
            else:
                # State field but not a US code — anomalous
                foreign_or_unknown.append(c)
                continue

        # Path 2: No state, but has a non-US country code — international shard
        if country_code and country_code != 'US':
            country_name = c.get("country") or country_code
            by_country[country_name].append(c)
            continue

        # Path 3: No state, no country — truly unstated
        unstated.append(c)

    # Write per-state shards
    shard_stats = {}
    for state in US_STATES:
        records = by_state.get(state, [])
        shard_path = OUT_DIR / f"{state.lower()}.json"
        shard_data = {
            **meta,
            "state": state,
            "record_count": len(records),
            "churches": records,
        }
        shard_path.write_text(json.dumps(shard_data, indent=2, ensure_ascii=False))
        size_kb = shard_path.stat().st_size / 1024
        shard_stats[state] = {
            "count": len(records),
            "size_kb": round(size_kb, 1),
            "path": f"docs/data/churches/by-state/{state.lower()}.json",
        }

    # Write _unstated shard
    unstated_path = OUT_DIR / "_unstated.json"
    unstated_data = {
        **meta,
        "state": None,
        "note": "Records with no `state` field. After V7.0.1 backfill these are records where slug-suffix, address-regex, and long-state-name extraction all failed.",
        "record_count": len(unstated),
        "churches": unstated,
    }
    unstated_path.write_text(json.dumps(unstated_data, indent=2, ensure_ascii=False))

    # Write _foreign shard if any (state field set to non-US code — anomaly)
    if foreign_or_unknown:
        foreign_path = OUT_DIR / "_foreign.json"
        foreign_data = {
            **meta,
            "state": None,
            "note": "Records with a `state` field that is NOT a US state code (international, malformed, etc.).",
            "record_count": len(foreign_or_unknown),
            "churches": foreign_or_unknown,
        }
        foreign_path.write_text(json.dumps(foreign_data, indent=2, ensure_ascii=False))

    # Write _international shard (records with country_code != US and no state)
    international_path = OUT_DIR / "_international.json"
    international_total = sum(len(v) for v in by_country.values())
    international_data = {
        **meta,
        "state": None,
        "note": "Records outside the US, classified by country_code. Each church record retains its `country` and `country_code` fields; grouped here for filtered loading on per-country queries.",
        "record_count": international_total,
        "by_country": {k: len(v) for k, v in sorted(by_country.items())},
        "churches": [c for k in sorted(by_country.keys()) for c in by_country[k]],
    }
    international_path.write_text(json.dumps(international_data, indent=2, ensure_ascii=False))

    # Verify invariant
    total_sharded = sum(s["count"] for s in shard_stats.values()) + len(unstated) + len(foreign_or_unknown) + international_total
    invariant_ok = total_sharded == total_input

    # Write _index.json
    index_data = {
        **meta,
        "total_records": total_input,
        "total_in_state_shards": sum(s["count"] for s in shard_stats.values()),
        "total_international": international_total,
        "total_unstated": len(unstated),
        "total_foreign_or_unknown": len(foreign_or_unknown),
        "invariant_ok": invariant_ok,
        "shards_present": len([s for s in shard_stats.values() if s["count"] > 0]),
        "shards_empty": len([s for s in shard_stats.values() if s["count"] == 0]),
        "case_warnings": len(case_warning),  # records where state field was not uppercase
        "by_state": shard_stats,
    }
    index_path = OUT_DIR / "_index.json"
    index_path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False))

    # Report
    print()
    print(f"Wrote shards to {OUT_DIR.relative_to(ROOT)}/")
    print(f"  state shards present:    {index_data['shards_present']}/51 (50 states + DC)")
    print(f"  total in state shards:   {index_data['total_in_state_shards']}")
    print(f"  international shard:     {index_data['total_international']}")
    print(f"  unstated shard:          {index_data['total_unstated']}")
    print(f"  foreign/unknown shard:   {index_data['total_foreign_or_unknown']}")
    print(f"  case warnings:           {index_data['case_warnings']}")
    print()
    print(f"  invariant (sum == input total {total_input}): {'OK' if invariant_ok else 'FAIL'}")

    # Top 10 shards by size
    print()
    print("Top 10 shards by record count:")
    sorted_stats = sorted(shard_stats.items(), key=lambda x: -x[1]["count"])[:10]
    for state, stat in sorted_stats:
        print(f"  {state}: {stat['count']:>5} records  {stat['size_kb']:>7.1f} KB")

    # Size summary
    total_shard_bytes = sum(
        (OUT_DIR / f"{s.lower()}.json").stat().st_size
        for s in US_STATES
    ) + unstated_path.stat().st_size + (OUT_DIR / "_foreign.json").stat().st_size if foreign_or_unknown else 0
    source_bytes = SOURCE.stat().st_size
    print()
    print(f"Source file:       {source_bytes/1024/1024:.1f} MB")
    print(f"All shards total:  {total_shard_bytes/1024/1024:.1f} MB")
    print(f"  (some overhead from per-shard metadata duplication)")


if __name__ == "__main__":
    main()
