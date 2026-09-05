#!/usr/bin/env python3
"""Add N curated songs to worship-listen-directory.json from worship-overrides.

Picks the next songs from PRIORITY that have a YouTube id in overrides and a
songbook page, skipping ids already in the listen directory.

Usage:
  python3 scripts/worship-listen-batch-add.py [--count 5] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "docs" / "data" / "worship-listen-directory.json"
OVERRIDES = REPO / "docs" / "data" / "worship-overrides.json"
WORSHIP_DIR = REPO / "docs" / "worship"

# Well-known, doctrinally solid — expand this list as batches ship.
PRIORITY = [
    ("come-thou-fount", "Come Thou Fount", ["Robert Robinson", "John Wyeth"], ["grace", "longing", "covenant"], "hymn", "nPDz7DZoK30"),
    ("10-000-reasons-bless-the-lord", "10,000 Reasons (Bless the Lord)", ["Matt Redman"], ["praise", "gratitude", "worship"], "modern-hymn", None),
    ("as-the-deer", "As the Deer", ["Martin Nystrom"], ["longing", "trust", "psalm"], "modern-hymn", None),
    ("all-glory-be-to-christ", "All Glory Be to Christ", ["Keith Getty", "Kristyn Getty", "Leslie Jordan"], ["christ", "advent", "glory"], "modern-hymn", None),
    ("here-i-am-to-worship", "Here I Am to Worship", ["Tim Hughes"], ["worship", "adoration", "cross"], "modern-hymn", None),
    ("revelation-song", "Revelation Song", ["Jennie Lee Riddle", "Kari Jobe"], ["worship", "holiness", "revelation"], "modern-hymn", None),
    ("cornerstone", "Cornerstone", ["Keith Getty", "Stuart Townend", "William B. Bradbury"], ["christ", "foundation", "grace"], "modern-hymn", None),
    ("shout-to-the-lord", "Shout to the Lord", ["Darlene Zschech"], ["praise", "love", "worship"], "modern-hymn", None),
    ("how-great-is-our-god", "How Great Is Our God", ["Chris Tomlin", "Jesse Reeves", "Ed Cash"], ["majesty", "praise", "creation"], "modern-hymn", "KBDER3pOp0Y"),
    ("mighty-to-save", "Mighty to Save", ["Ben Fielding", "Reuben Morgan"], ["salvation", "cross", "praise"], "modern-hymn", "hwZNLlDVrV4"),
    ("the-heart-of-worship", "The Heart of Worship", ["Matt Redman"], ["worship", "surrender", "simplicity"], "modern-hymn", "7mJdJ2SnB3Y"),
    ("open-the-eyes-of-my-heart", "Open the Eyes of My Heart", ["Paul Baloche"], ["worship", "longing", "holiness"], "modern-hymn", "yQ0x2LJ8J8Y"),
    ("what-a-beautiful-name", "What a Beautiful Name", ["Ben Fielding", "Brooke Ligertwood"], ["cross", "name-of-jesus", "worship"], "modern-hymn", "rA2IaNArZeQ"),
    ("amazing-grace-my-chains-are-gone", "Amazing Grace (My Chains Are Gone)", ["John Newton", "Chris Tomlin", "Louie Giglio"], ["grace", "freedom", "cross"], "modern-hymn", "Jbe7OrHLoFI"),
]


def amazon_url(title: str, artists: list[str]) -> str:
    q = urllib.parse.quote(f"{title} {artists[0]} music")
    return f"https://music.amazon.com/search/{q}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    catalog = json.loads(DATA.read_text())
    overrides = json.loads(OVERRIDES.read_text())
    existing = {s["id"] for s in catalog["songs"]}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    added = []
    for slug, title, artists, themes, style, yt_override in PRIORITY:
        if slug in existing:
            continue
        if len(added) >= args.count:
            break
        page = WORSHIP_DIR / f"{slug}.html"
        if not page.exists():
            continue
        yt_id = yt_override or overrides.get(slug, {}).get("youtube")
        if not yt_id:
            continue
        entry = {
            "id": slug,
            "title": title,
            "artists": artists,
            "themes": themes,
            "scripture_hooks": [],
            "youtube_url": f"https://www.youtube.com/watch?v={yt_id}",
            "amazon_music_url": amazon_url(title, artists),
            "songbook_path": f"/worship/{slug}.html",
            "style": style,
            "doctrinal_status": "approved",
            "notes": "",
            "link_checked_at": now,
        }
        added.append(entry)

    if not added:
        print("No songs to add — priority list exhausted or all already present.")
        return

    print(f"Adding {len(added)}:")
    for e in added:
        print(f"  + {e['title']}")

    if args.dry_run:
        return

    catalog["songs"].extend(added)
    approved = [s for s in catalog["songs"] if s.get("doctrinal_status") == "approved"]
    catalog["updated_at"] = now
    catalog["counts"] = {
        "total_seed": len(approved),
        "approved_linked": len(approved),
        "pending_link": 0,
    }
    DATA.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")

    subprocess.run(
        ["node", str(REPO / "scripts" / "build-worship-directory.js")],
        check=True,
        cwd=REPO,
    )
    print(f"Done — {len(approved)} total in listen directory.")


if __name__ == "__main__":
    main()
