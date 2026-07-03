#!/usr/bin/env python3
"""
Build per-denomination_family shards of docs/data/churches.json.

Mirrors `build_state_shards.py` but splits by `denomination_family` instead
of `state`. Powers per-network filter views (directory-networks.html,
politicians-by-church-network joins).

OUTPUTS:
  docs/data/churches/by-denomination-family/
  ├── _index.json           summary: per-family counts, generated_at, invariant
  ├── _empty.json           records with empty/null denomination_family (currently 0)
  └── {family-slug}.json    one per distinct denomination_family value (155)

SHARD SCHEMA:
  Same as state shards. Each shard carries `directory_version`,
  `directory_updated`, `rubric`, and a `denomination_family` field naming
  the bucket. Records inside `churches[]` are byte-identical to the source
  monolith.

INVARIANT:
  sum(shard.record_count) + _empty.record_count == churches.json.total_churches
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]  # repo root (scripts/ is one level down)
SOURCE = ROOT / "docs/data/churches.json"
OUT_DIR = ROOT / "docs/data/churches/by-denomination-family"


def write_if_changed(path, payload):
    """Write a shard only when content (ignoring shard_generated_at) actually changed.

    Mirrors build_state_shards.py: invoked from generate-church-pages.js, so an
    unchanged shard must not churn a fresh timestamp into every commit."""
    if path.exists():
        try:
            old = json.loads(path.read_text())
            # Ignore volatile stamps — a shard must churn ONLY when its church CONTENT
            # changes. shard_generated_at is per-run; directory_updated is bumped to today
            # by merge-pastor-enrichments on every enrichment and lives in every shard's
            # meta, so without excluding it too all ~200 shards rewrite each run (bloat).
            probe = dict(payload,
                         shard_generated_at=old.get("shard_generated_at"),
                         directory_updated=old.get("directory_updated"))
            if old == probe:
                return False
        except (json.JSONDecodeError, OSError):
            pass
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return True


def slugify(value):
    """Turn 'Presbyterian (PCA)' into 'presbyterian-pca'."""
    s = (value or "").lower().strip()
    s = re.sub(r'[()/\\,]', ' ', s)
    s = re.sub(r'[^a-z0-9 -]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s.strip('-') or 'unknown'


def main():
    print(f"Reading {SOURCE.relative_to(ROOT)}...")
    data = json.loads(SOURCE.read_text())
    churches = data.get("churches", [])
    total_input = len(churches)
    print(f"  {total_input} records")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    meta = {
        "directory_version": data.get("directory_version"),
        "directory_updated": data.get("directory_updated"),
        "shard_source": "docs/data/churches.json",
        "shard_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "shard_format_version": 2,
        "rubric": data.get("rubric"),
    }

    by_family = defaultdict(list)
    by_slug_collision = defaultdict(list)  # detect slug collisions across different families
    empty_family = []

    for c in churches:
        fam = c.get("denomination_family")
        if not fam or not isinstance(fam, str) or not fam.strip():
            empty_family.append(c)
            continue
        fam_clean = fam.strip()
        slug = slugify(fam_clean)
        by_family[fam_clean].append(c)
        by_slug_collision[slug].append(fam_clean)

    # Detect any slug collisions (two different family names producing same slug)
    collisions = {slug: set(names) for slug, names in by_slug_collision.items()
                  if len(set(names)) > 1}
    if collisions:
        print(f"\n⚠ slug collisions detected (will MERGE these family names):")
        for slug, names in collisions.items():
            print(f"  {slug}: {names}")
            # Merge logic: pick the first name alphabetically as canonical,
            # combine records from all colliding families
        for slug, names_set in collisions.items():
            names = sorted(names_set)
            canonical = names[0]
            for n in names[1:]:
                if n != canonical:
                    by_family[canonical].extend(by_family[n])
                    del by_family[n]

    # Write shards
    shard_stats = {}
    for fam_name, records in sorted(by_family.items()):
        slug = slugify(fam_name)
        shard_path = OUT_DIR / f"{slug}.json"
        shard_data = {
            **meta,
            "denomination_family": fam_name,
            "record_count": len(records),
            "churches": records,
        }
        write_if_changed(shard_path, shard_data)
        size_kb = shard_path.stat().st_size / 1024
        shard_stats[slug] = {
            "family": fam_name,
            "count": len(records),
            "size_kb": round(size_kb, 1),
            "path": f"docs/data/churches/by-denomination-family/{slug}.json",
        }

    # Empty-family shard
    empty_path = OUT_DIR / "_empty.json"
    empty_data = {
        **meta,
        "denomination_family": None,
        "note": "Records with no denomination_family field. Should be 0 after V7.0.x cleanup.",
        "record_count": len(empty_family),
        "churches": empty_family,
    }
    write_if_changed(empty_path, empty_data)

    # Verify invariant
    total_sharded = sum(s["count"] for s in shard_stats.values()) + len(empty_family)
    invariant_ok = total_sharded == total_input

    # _index.json
    index_data = {
        **meta,
        "rubric_included": True,
        "total_records": total_input,
        "total_in_family_shards": sum(s["count"] for s in shard_stats.values()),
        "total_empty_family": len(empty_family),
        "invariant_ok": invariant_ok,
        "shard_count": len(shard_stats),
        "by_family": shard_stats,
    }
    # Strip rubric from _index to keep it lightweight
    del index_data["rubric"]

    index_path = OUT_DIR / "_index.json"
    write_if_changed(index_path, index_data)

    # Report
    print()
    print(f"Wrote {len(shard_stats)} family shards to {OUT_DIR.relative_to(ROOT)}/")
    print(f"  total in family shards:  {index_data['total_in_family_shards']}")
    print(f"  empty-family shard:      {index_data['total_empty_family']}")
    print(f"  invariant: {'OK' if invariant_ok else 'FAIL'} (sum == {total_input})")

    # Top 15 shards
    print()
    print("Top 15 family shards by record count:")
    top = sorted(shard_stats.items(), key=lambda x: -x[1]["count"])[:15]
    for slug, stat in top:
        print(f"  {stat['family']:40} {stat['count']:>5} records  {stat['size_kb']:>7.1f} KB")


if __name__ == "__main__":
    main()
