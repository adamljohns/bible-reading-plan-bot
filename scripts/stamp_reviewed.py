#!/usr/bin/env python3
"""Mark daily readings as reviewed by MOOP (Principal 2026-11-06).

Replaces the "Original Draft Prototype" footer with "MOOP v1.0 / Reviewed by MOOP" on
each date given, in all three places a day lives, so a later rebuild keeps it:
  data/readings/<date>.md                 <!-- version: {...} --> (read by both builders)
  docs/readings/<date>.html               footer draft-tag / draft-note
  docs/assets/readings/<date>.json        "version" and "stamp"

Usage (repo root):
  python3 scripts/stamp_reviewed.py 2026-11-06 [2026-11-05 ...] [--on 2026-11-06]
  python3 scripts/stamp_reviewed.py --file dates.txt
A day already at MOOP v1.0 or higher is left alone. Idempotent.
"""
import argparse
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION_RE = re.compile(r"<!--\s*version:\s*\{.*?\}\s*-->\n?", re.S)
FOOTER_RE = re.compile(r'<div class="draft-tag">[^<]*</div>(\s*<div class="draft-note">[^<]*</div>)?')


def version_for(on):
    v = {"label": "MOOP v1.0", "status": "moop_v1", "reviewed_by": "Adam",
         "note": "Reviewed by MOOP"}
    if on:
        v["reviewed_at_display"] = on
    return v


def already_reviewed(json_path):
    try:
        cur = json.loads(json_path.read_text(encoding="utf-8")).get("version") or {}
    except FileNotFoundError:
        return False
    return str(cur.get("status", "")).startswith("moop_v")


def stamp(date, on):
    md = ROOT / "data" / "readings" / f"{date}.md"
    page = ROOT / "docs" / "readings" / f"{date}.html"
    js = ROOT / "docs" / "assets" / "readings" / f"{date}.json"
    if not (md.exists() and page.exists() and js.exists()):
        return "missing"
    if already_reviewed(js):
        return "already"
    v = version_for(on)

    text = VERSION_RE.sub("", md.read_text(encoding="utf-8")).rstrip("\n")
    md.write_text(text + "\n\n<!-- version: " + json.dumps(v, ensure_ascii=False) + " -->\n", encoding="utf-8")

    h = page.read_text(encoding="utf-8")
    new_footer = (f'<div class="draft-tag">{html.escape(v["label"])}</div>\n'
                  f'<div class="draft-note">{html.escape(v["note"])}</div>')
    h2, n = FOOTER_RE.subn(new_footer, h, count=1)
    if n != 1:
        return "no-footer"
    page.write_text(h2, encoding="utf-8")

    data = json.loads(js.read_text(encoding="utf-8"))
    data["version"] = v
    data["stamp"] = v["label"]
    js.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return "stamped"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--on", help="date he reviewed it, shown in the JSON only")
    a = ap.parse_args()
    dates = list(a.dates)
    if a.file:
        dates += [l.split()[0] for l in open(a.file) if re.match(r"\d{4}-\d{2}-\d{2}", l)]
    if not dates:
        ap.error("no dates")
    out = {}
    for d in sorted(set(dates)):
        out.setdefault(stamp(d, a.on), []).append(d)
    for k, v in out.items():
        print(f"{k}: {len(v)} {' '.join(v) if len(v) <= 12 else v[0] + ' .. ' + v[-1]}")
    sys.exit(1 if set(out) - {"stamped", "already"} else 0)


if __name__ == "__main__":
    main()
