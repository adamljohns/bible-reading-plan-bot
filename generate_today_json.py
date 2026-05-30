#!/usr/bin/env python3
"""
Regenerate docs/assets/today.json from the most recent daily reading
(docs/readings/YYYY-MM-DD.md) so the USMC Ministries app's "Today" tab
shows the current day's reading. Run daily (e.g., from the reading cron):

    python3 generate_today_json.py

Extracts: title (devotional name), reference (book · date), body (the
Reflection paragraph, falling back to the first Scripture paragraph).
"""
import re, json, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

def main():
    files = sorted(glob.glob(os.path.join(DOCS, "readings", "*.md")))
    if not files:
        print("no reading files found"); return
    text = open(files[-1], encoding="utf-8").read()

    # H2 like: "## ✝ Morning Wisdom — May 30, 2026"
    m = re.search(r"^##\s*(.+)$", text, re.M)
    h2 = re.sub(r"^[^0-9A-Za-z]+", "", m.group(1)).strip() if m else "Today"
    if "—" in h2:
        name, date = [s.strip() for s in h2.split("—", 1)]
    else:
        name, date = h2, ""

    # reference like: "**📖 Proverbs 30**"
    r = re.search(r"\*\*[^0-9A-Za-z]*([^*]+?)\*\*", text)
    book = re.sub(r"^[^0-9A-Za-z]+", "", r.group(1)).strip() if r else ""
    reference = " · ".join(x for x in (book, date) if x)

    # body: first paragraph after "### … Reflection", else first Scripture paragraph
    body = ""
    mr = re.search(r"###[^\n]*Reflection[^\n]*\n+(.+?)(?:\n\n|\Z)", text, re.S)
    ms = re.search(r"###[^\n]*Scripture[^\n]*\n+(.+?)(?:\n\n|\Z)", text, re.S)
    src = mr or ms
    if src:
        body = re.sub(r"\s+", " ", src.group(1)).strip()[:900]

    out = {"title": name or "Morning Wisdom", "reference": reference, "body": body}
    path = os.path.join(DOCS, "assets", "today.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote", path)
    print(json.dumps(out, ensure_ascii=False, indent=2)[:400])

if __name__ == "__main__":
    main()
