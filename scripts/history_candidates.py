#!/usr/bin/env python3
"""
history_candidates.py — Reliable source material for the "This Day in American
History" block. For a given date it:

  1. Pulls VERIFIED events from Wikipedia's "On This Day" feed (date-keyed,
     community-sourced, each with a year + linked articles) — this is the
     authority we check against, NOT model memory.
  2. Filters to American-relevant events and tags each by theme
     (founding/constitutional, military, faith/revival, invention/industry,
     exploration, civic) so it's easy to pick edifying, providentially-framed
     entries that fit the day's trait.
  3. Prints the EXISTING events currently in data/readings/<date>.md beside the
     verified candidates, so a day can be reviewed and corrected one at a time.

Responses are cached to data/history-cache/MM-DD.json (the calendar day is what
matters, not the year, so the cache is reusable).

USAGE
  python3 scripts/history_candidates.py 2026-01-01
  python3 scripts/history_candidates.py 01-01           # date-only also works
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
CACHE = REPO / "data" / "history-cache"
UA = "usmcmin-readings/1.0 (ministry devotional fact-check; contact bowandarrowstudiollc@gmail.com)"

US_HINTS = [
    "United States", "U.S.", "U.S.A", "America", "American", "Congress",
    "President", "Continental", "Confederate", "Union Army", "Founding",
    "Constitution", "Colon", "Virginia", "Massachusetts", "Philadelphia",
    "Washington", "NASA", "Apollo", "Civil War", "Revolutionary War",
]
THEME = [
    ("founding/constitutional", r"constitution|congress|declaration|founding|ratif|independence|federal|amendment|union|state is admitted|admitted to the union"),
    ("military valor",          r"war|battle|army|navy|marine|soldier|siege|fort|d-day|regiment|uss |general |medal of honor"),
    ("faith/revival",           r"church|revival|preacher|missionar|baptist|presbyter|methodist|bible|gospel|pastor|christian|prayer"),
    ("invention/industry",      r"patent|invent|railroad|telegraph|telephone|electric|factory|first .* (flight|car|engine|machine)|bridge|canal"),
    ("exploration/frontier",    r"explor|frontier|expedition|territor|trail|gold|settle|pioneer|lewis and clark"),
    ("civic/governance",        r"elect|inaugurat|supreme court|governor|treaty|proclamation|act of congress|law"),
]
CAUTION = r"protest|march on|liberation|riot|strike|civil rights movement|feminis|suffrage parade|labor union"


MONTHNAME = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]


def fetch(mm, dd):
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / f"{mm}-{dd}.json"
    if cf.exists():
        return json.loads(cf.read_text())
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/{mm}/{dd}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    cf.write_text(json.dumps(data, ensure_ascii=False))
    return data


def fetch_datepage(mm, dd):
    """Full Wikipedia '<Month> <Day>' Events section — richer than the curated
    On-This-Day subset. Returns [{year, text}] (best-effort wikitext parse)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cf = CACHE / f"datepage-{mm}-{dd}.json"
    if cf.exists():
        return json.loads(cf.read_text())
    page = f"{MONTHNAME[int(mm)]}_{int(dd)}"
    url = (f"https://en.wikipedia.org/w/api.php?action=parse&page={page}"
           f"&prop=wikitext&format=json&section=1")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            wt = json.loads(r.read())["parse"]["wikitext"]["*"]
    except Exception:
        wt = ""
    out = []
    for ln in wt.splitlines():
        m = re.match(r"\*\s*\[\[(\d{3,4})", ln)
        if not m:
            continue
        year = m.group(1)
        # strip wiki markup to plain text
        txt = ln
        txt = re.sub(r"\[\[[^]|]*\|", "", txt)
        txt = txt.replace("[[", "").replace("]]", "")
        txt = re.sub(r"^\*\s*\d{3,4}\s*&ndash;\s*", "", txt)
        txt = re.sub(r"^\*\s*\d{3,4}\s*[–—-]\s*", "", txt)
        txt = txt.replace("&ndash;", "–").replace("'''", "").replace("''", "")
        txt = re.sub(r"<ref[^>]*>.*?</ref>", "", txt)
        txt = re.sub(r"<[^>]+>", "", txt)
        txt = re.sub(r"\{\{[^}]*\}\}", "", txt).strip()
        out.append({"year": year, "text": txt})
    cf.write_text(json.dumps(out, ensure_ascii=False))
    return out


def is_us(e):
    text = e.get("text", "")
    if any(h in text for h in US_HINTS):
        return True
    for p in e.get("pages", []):
        if any(h in (p.get("title", "") or "") for h in ("United_States", "American", "U.S.")):
            return True
    return False


def themes_of(text):
    t = text.lower()
    out = [name for name, pat in THEME if re.search(pat, t)]
    if re.search(CAUTION, t):
        out.append("⚠CAUTION-framing")
    return out or ["general"]


def existing_events(ds):
    p = READINGS / f"{ds}.md"
    if not p.exists():
        return []
    md = p.read_text().splitlines()
    out, grab = [], False
    for ln in md:
        if "This Day in American History" in ln:
            grab = True
            continue
        if grab:
            s = ln.strip()
            if s.startswith(("⚓", "⛏", "🔨", "🙏", "🌙", "⸻", "🦅")):
                break
            if s:
                out.append(s)
    return out


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    m = re.search(r"(\d{2})-(\d{2})$", arg)
    if not m:
        sys.exit("usage: history_candidates.py YYYY-MM-DD | MM-DD")
    mm, dd = m.group(1), m.group(2)
    ds = arg if re.match(r"^\d{4}-", arg) else f"2026-{mm}-{dd}"

    print(f"=== {ds}  (calendar {mm}/{dd}) ===\n")
    print("EXISTING events in the reading:")
    ex = existing_events(ds)
    if ex:
        for e in ex:
            print(f"  | {e}")
    else:
        print("  (none / not found)")

    data = fetch(mm, dd)
    us = sorted((e for e in data.get("events", []) if is_us(e)), key=lambda x: x["year"])
    print(f"\nVERIFIED American candidates from Wikipedia On-This-Day ({len(us)}):")
    for e in us:
        tags = ",".join(themes_of(e["text"]))
        pg = e.get("pages", [{}])[0].get("content_urls", {}).get("desktop", {}).get("page", "")
        print(f"  {e['year']}  [{tags}]")
        print(f"     {e['text']}")


if __name__ == "__main__":
    main()
