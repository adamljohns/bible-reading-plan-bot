#!/usr/bin/env python3
"""
build_reading_index.py — Build the day-keyed reading index (the JSON "API"
layer that PJ's crons and the Watchman form query instead of parsing 365
markdown files).

Outputs:
  docs/assets/reading-index.json          — lightweight master: every date ->
                                             {weekday, page_url, passages, traits,
                                              has_audio per watch, per_day_json url}
  docs/assets/readings/<date>.json         — full per-day payload PJ web_fetches:
                                             each watch's passage, trait, full text,
                                             audio url, and personal-name tokens.

Re-runnable (idempotent), like the inventory builder.
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
AUDIO = REPO / "docs" / "assets" / "audio" / "readings"
OUT_DIR = REPO / "docs" / "assets" / "readings"          # per-day JSON dir
INDEX = REPO / "docs" / "assets" / "reading-index.json"
PLAN = REPO / "docs" / "assets" / "plan-data.js"
SITE = "https://usmcmin.org"

WATCH_ORDER = ["wisdom", "first", "second", "third", "peace"]
WATCH_META = {
    "wisdom": {"time": "0600", "title": "Morning Wisdom",                  "emojis": "🌅☀"},
    "first":  {"time": "0700", "title": "First Watch — The Husband's Post", "emojis": "🕖"},
    "second": {"time": "1100", "title": "Second Watch — The Father's Charge","emojis": "🕚"},
    "third":  {"time": "1500", "title": "Third Watch — The Citizen's Stand", "emojis": "🕒"},
    "peace":  {"time": "2100", "title": "Evening Peace",                    "emojis": "🌙"},
}
# Personal names that a personalized plan would swap out (Adam's household).
PERSONAL_NAMES = ["Maria", "Gideon", "Boaz", "Shiloh"]

SCRIP_RE = re.compile(r"^\s*📖\s*Scripture\s*[—\-–:]\s*(.+?)\s*$")
REFL_RE = re.compile(r"Reflection.*?[—\-–]\s*([A-Z][^\n]+?)\s*$")
WATCH_HDR_RE = re.compile(r"^\s*([🌅☀🕖🕚🕒🌙])\s")


def load_passages():
    """Pull window.PLAN_DATA entries from plan-data.js."""
    text = PLAN.read_text()
    out = {}
    for m in re.finditer(r'"(\d{4}-\d{2}-\d{2})"\s*:\s*(\{[^}]*\})', text):
        try:
            out[m.group(1)] = json.loads(m.group(2))
        except json.JSONDecodeError:
            pass
    return out


def split_watches(md_text):
    """Slice a reading into its 5 watches by the watch-header emoji lines.
    Returns {watch_key: full_text}. Robust to the my-format and the older
    PDF-converted format (handles ☀ as a wisdom header too)."""
    lines = md_text.splitlines()
    # find header line indexes + which watch each is
    marks = []  # (line_idx, watch_key)
    for i, ln in enumerate(lines):
        m = WATCH_HDR_RE.match(ln)
        if not m:
            continue
        emoji = m.group(1)
        for key, meta in WATCH_META.items():
            if emoji in meta["emojis"]:
                # only the FIRST header of each key (avoid stray emoji mid-text)
                if key not in [k for _, k in marks]:
                    marks.append((i, key))
                break
    if not marks:
        return {}
    marks.sort()
    watches = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        body = "\n".join(lines[start:end]).rstrip()
        # trim a trailing watch separator rule if present
        body = re.sub(r"\n⸻{3,}\s*$", "", body).rstrip()
        watches[key] = body
    return watches


def extract_passage(watch_text):
    for ln in watch_text.splitlines():
        m = SCRIP_RE.match(ln)
        if m:
            return m.group(1).strip()
    return None


def extract_trait(watch_text):
    for ln in watch_text.splitlines():
        if "Reflection" in ln:
            # take the segment after the LAST em/en-dash (e.g. "... Husband — Protecting" -> "Protecting")
            parts = re.split(r"\s[—–-]\s", ln)
            if len(parts) >= 2:
                return parts[-1].strip()
    return None


def personal_tokens(watch_text):
    return [n for n in PERSONAL_NAMES if re.search(rf"\b{n}\b", watch_text)]


def build_day(ds, passages):
    md_path = READINGS / f"{ds}.md"
    if not md_path.exists():
        return None
    md = md_path.read_text()
    watches_text = split_watches(md)
    dt = date.fromisoformat(ds)
    plan = passages.get(ds, {})
    plan_map = {"wisdom": "wisdom", "first": "first", "second": "second",
                "third": "third", "peace": "peace"}

    watches = {}
    for key in WATCH_ORDER:
        text = watches_text.get(key)
        mp3 = AUDIO / f"{ds}-{key}.mp3"
        passage = (extract_passage(text) if text else None) or plan.get(plan_map[key])
        watches[key] = {
            "time": WATCH_META[key]["time"],
            "title": WATCH_META[key]["title"],
            "passage": passage,
            "trait": extract_trait(text) if text else None,
            "text": text,
            "has_audio": mp3.exists(),
            "audio_url": f"{SITE}/assets/audio/readings/{ds}-{key}.mp3" if mp3.exists() else None,
            "personal_tokens": personal_tokens(text) if text else [],
        }

    return {
        "date": ds,
        "weekday": dt.strftime("%A"),
        "day_of_year": dt.timetuple().tm_yday,
        "page_url": f"{SITE}/readings/{ds}.html",
        "watches": watches,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("stamp", nargs="?", default="unknown", help="generated_at timestamp")
    ap.add_argument("--date", help="write only this date's per-day JSON (master index always fully rebuilt)")
    args = ap.parse_args()
    stamp = args.stamp
    only = args.date
    passages = load_passages()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_days = {}
    cur, end = date(2026, 1, 1), date(2026, 12, 31)
    n_written = 0
    while cur <= end:
        ds = cur.isoformat()
        day = build_day(ds, passages)
        cur += timedelta(days=1)
        if not day:
            continue
        # write per-day json (all days, or just the requested one)
        if only is None or ds == only:
            (OUT_DIR / f"{ds}.json").write_text(json.dumps(day, ensure_ascii=False, indent=1))
            n_written += 1
        # master index entry (lightweight)
        index_days[ds] = {
            "weekday": day["weekday"],
            "page_url": day["page_url"],
            "per_day_json": f"{SITE}/assets/readings/{ds}.json",
            "passages": {k: day["watches"][k]["passage"] for k in WATCH_ORDER},
            "traits": {k: day["watches"][k]["trait"] for k in WATCH_ORDER},
            "has_audio": {k: day["watches"][k]["has_audio"] for k in WATCH_ORDER},
        }

    index = {
        "generated_at": stamp,
        "count": len(index_days),
        "site": SITE,
        "schema": "date -> {weekday, page_url, per_day_json, passages, traits, has_audio}; "
                  "fetch per_day_json for full watch text + audio + personal_tokens",
        "days": index_days,
    }
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1))
    print(f"  ✓ wrote {n_written} per-day JSON + reading-index.json ({len(index_days)} days)")


if __name__ == "__main__":
    main()
