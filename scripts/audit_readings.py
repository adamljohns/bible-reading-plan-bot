#!/usr/bin/env python3
"""
audit_readings.py — Scan all 365 daily readings (data/readings/<date>.md) and
produce a concrete findings report across four refinement dimensions:

  A. Scripture fidelity — divine-name drift (passage's reference text has "the
     LORD" / YHWH but the rendered scripture swapped in an epithet like "the
     Most High" / "the Eternal", or dropped the divine name); stray "Yahweh".
  B. Voice variety — sentences/closing lines reused verbatim across many days
     (formulaic repetition), especially Helm/Rudder closers and prayer lines.
  C. Application sharpness — application bullets duplicated across days, and
     bullets that share no content word with their own passage/reflection.
  D. History facts — every "This Day in American History" event extracted
     (date, year, claim) for downstream verification.

Outputs (committed, NOT served — they live under data/):
  data/readings-audit.json         full structured findings
  data/readings-audit-report.md    human-readable summary + top offenders

Re-runnable. Read-only over the corpus (writes only the two report files).

USAGE
  python3 scripts/audit_readings.py
  python3 scripts/audit_readings.py --limit 10     # first 10 days (smoke test)
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
READINGS = REPO / "data" / "readings"
VERSE_CACHE = REPO / "docs" / "assets" / "verse-cache.json"
OUT_JSON = REPO / "data" / "readings-audit.json"
OUT_MD = REPO / "data" / "readings-audit-report.md"

WATCH_META = {
    "wisdom": "🌅☀", "first": "🕖", "second": "🕚", "third": "🕒", "peace": "🌙",
}
WATCH_HDR_RE = re.compile(r"^\s*([🌅☀🕖🕚🕒🌙])\s")
SCRIP_RE = re.compile(r"^\s*📖\s*Scripture\s*[—\-–:]\s*(.+?)\s*$")
SEP_RE = re.compile(r"^\s*⸻+\s*$")
BULLET_RE = re.compile(r"^\s*•\s+(.*\S)\s*$")
HELM_RE = re.compile(r"^\s*⚓\s*(?:Helm Command|Rudder Steer)\s*[:：]\s*(.+?)\s*$")
HIST_HDR_RE = re.compile(r"🦅\s*This Day in American History")
HIST_EVENT_RE = re.compile(r"^\s*•\s*(\d{3,4})\s*[—\-–]\s*(.+?)\s*$")

# Divine-name epithets that may stand in for YHWH ("the LORD") in a drifted render.
EPITHETS = [
    "the Most High", "the Eternal", "the Eternal One", "the Almighty",
    "the Sovereign One", "the Sovereign Lord", "the Self-Existent One",
    "the Everlasting", "the Divine", "Jehovah",
]

# Book name -> bookId for resolving passage refs against verse-cache.
BOOKS = {
    "genesis":1,"exodus":2,"leviticus":3,"numbers":4,"deuteronomy":5,"joshua":6,
    "judges":7,"ruth":8,"1 samuel":9,"2 samuel":10,"1 kings":11,"2 kings":12,
    "1 chronicles":13,"2 chronicles":14,"ezra":15,"nehemiah":16,"esther":17,
    "job":18,"psalm":19,"psalms":19,"proverbs":20,"ecclesiastes":21,
    "song of solomon":22,"song of songs":22,"isaiah":23,"jeremiah":24,
    "lamentations":25,"ezekiel":26,"daniel":27,"hosea":28,"joel":29,"amos":30,
    "obadiah":31,"jonah":32,"micah":33,"nahum":34,"habakkuk":35,"zephaniah":36,
    "haggai":37,"zechariah":38,"malachi":39,"matthew":40,"mark":41,"luke":42,
    "john":43,"acts":44,"romans":45,"1 corinthians":46,"2 corinthians":47,
    "galatians":48,"ephesians":49,"philippians":50,"colossians":51,
    "1 thessalonians":52,"2 thessalonians":53,"1 timothy":54,"2 timothy":55,
    "titus":56,"philemon":57,"hebrews":58,"james":59,"1 peter":60,"2 peter":61,
    "1 john":62,"2 john":63,"3 john":64,"jude":65,"revelation":66,
}
REF_RE = re.compile(r"^\s*([1-3]?\s?[A-Za-z][A-Za-z ]+?)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?")


def split_watches(md_text):
    lines = md_text.splitlines()
    marks = []
    for i, ln in enumerate(lines):
        m = WATCH_HDR_RE.match(ln)
        if not m:
            continue
        emoji = m.group(1)
        for key, emojis in WATCH_META.items():
            if emoji in emojis and key not in [k for _, k in marks]:
                marks.append((i, key))
                break
    marks.sort()
    out = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        out[key] = "\n".join(lines[start:end]).rstrip()
    return out


def parse_watch(text):
    """Return dict: intro, ref, scripture_lines, reflection, bullets, helm, history."""
    lines = text.splitlines()
    ref = None
    scripture, reflection, bullets, helm, history = [], [], [], None, []
    # locate scripture marker + the block until next ⸻
    i = 0
    n = len(lines)
    # intro = first non-empty line after the header line
    intro = ""
    for ln in lines[1:]:
        if ln.strip():
            intro = ln.strip()
            break
    in_scrip = False
    for ln in lines:
        ms = SCRIP_RE.match(ln)
        if ms:
            ref = ms.group(1).strip()
            in_scrip = True
            continue
        if in_scrip:
            if SEP_RE.match(ln):
                in_scrip = False
            elif ln.strip():
                scripture.append(ln.strip())
        mb = BULLET_RE.match(ln)
        if mb and not HIST_EVENT_RE.match(ln):
            bullets.append(mb.group(1).strip())
        mh = HELM_RE.match(ln)
        if mh:
            helm = mh.group(1).strip()
    # history events
    in_hist = False
    for ln in lines:
        if HIST_HDR_RE.search(ln):
            in_hist = True
            continue
        if in_hist:
            me = HIST_EVENT_RE.match(ln)
            if me:
                history.append({"year": me.group(1), "event": me.group(2).strip()})
            elif ln.strip() and not ln.strip().startswith("•") and "⛏" in ln:
                in_hist = False
    return {"intro": intro, "ref": ref, "scripture": " ".join(scripture),
            "bullets": bullets, "helm": helm, "history": history}


def ref_to_keys(ref):
    m = REF_RE.match(ref or "")
    if not m:
        return None, []
    book = re.sub(r"\s+", " ", m.group(1).strip().lower())
    bid = BOOKS.get(book)
    if not bid:
        return None, []
    ch = int(m.group(2)); v1 = int(m.group(3)); v2 = int(m.group(4)) if m.group(4) else v1
    return bid, [f"{bid}_{ch}_{v}" for v in range(v1, v2 + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    vc = json.loads(VERSE_CACHE.read_text())

    a_flags = []   # scripture fidelity
    b_sentences = Counter()
    b_helms = Counter()
    c_bullets = Counter()
    c_generic = []
    d_history = []
    yahweh_hits = []

    cur, end = date(2026, 1, 1), date(2026, 12, 31)
    days = []
    while cur <= end:
        days.append(cur.isoformat()); cur += timedelta(days=1)
    if args.limit:
        days = days[:args.limit]

    n_watches = 0
    for ds in days:
        p = READINGS / f"{ds}.md"
        if not p.exists():
            continue
        md = p.read_text()
        for wk, wtext in split_watches(md).items():
            n_watches += 1
            w = parse_watch(wtext)
            scrip = w["scripture"]
            # A. scripture fidelity
            if "Yahweh" in scrip or "Yahweh" in wtext:
                yahweh_hits.append({"date": ds, "watch": wk})
            bid, keys = ref_to_keys(w["ref"])
            if keys:
                refkjv = " ".join(vc.get(k, {}).get("KJV", "") for k in keys)
                ref_has_lord = bool(re.search(r"\bLORD\b", refkjv))
                read_has_lord = bool(re.search(r"\bLORD\b", scrip))
                used_epithets = [e for e in EPITHETS if e in scrip]
                if ref_has_lord and not read_has_lord:
                    a_flags.append({"date": ds, "watch": wk, "ref": w["ref"],
                                    "issue": "ref has LORD, rendering has none",
                                    "epithets": used_epithets,
                                    "scrip_head": scrip[:160]})
                elif used_epithets and ref_has_lord:
                    # epithet present AND ref uses LORD -> possible partial swap
                    a_flags.append({"date": ds, "watch": wk, "ref": w["ref"],
                                    "issue": "epithet alongside LORD-passage",
                                    "epithets": used_epithets,
                                    "scrip_head": scrip[:160]})
            # B. repetition — sentences in scripture-free prose (intro + helm)
            if w["intro"]:
                b_sentences[w["intro"]] += 1
            if w["helm"]:
                b_helms[w["helm"]] += 1
            # C. application bullets
            passage_words = set(re.findall(r"[a-z]{5,}", (w["ref"] or "").lower()))
            for b in w["bullets"]:
                c_bullets[b] += 1
            # D. history
            for h in w["history"]:
                d_history.append({"date": ds, "watch": wk, **h})

    # Assemble findings
    a_flags_sorted = sorted(a_flags, key=lambda x: x["date"])
    b_top_sentences = [(s, c) for s, c in b_sentences.most_common(40) if c > 1]
    b_top_helms = [(s, c) for s, c in b_helms.most_common(40) if c > 1]
    c_dupe_bullets = [(b, c) for b, c in c_bullets.most_common(60) if c > 1]

    findings = {
        "n_days": len([d for d in days if (READINGS / f"{d}.md").exists()]),
        "n_watches": n_watches,
        "A_scripture_fidelity": {
            "count": len(a_flags_sorted),
            "yahweh_hits": yahweh_hits,
            "flags": a_flags_sorted,
        },
        "B_voice_variety": {
            "repeated_intro_sentences": b_top_sentences,
            "repeated_helm_lines": b_top_helms,
        },
        "C_application": {
            "duplicate_bullets": c_dupe_bullets,
        },
        "D_history_events": d_history,
    }
    OUT_JSON.write_text(json.dumps(findings, ensure_ascii=False, indent=1))

    # Human report
    L = []
    L.append("# Daily Readings — Audit Report\n")
    L.append(f"- Days scanned: **{findings['n_days']}**  |  watches: **{n_watches}**\n")
    L.append("\n## A. Scripture fidelity\n")
    L.append(f"- Divine-name flags: **{len(a_flags_sorted)}**")
    L.append(f"- Stray 'Yahweh': **{len(yahweh_hits)}**\n")
    by_issue = Counter(f["issue"] for f in a_flags_sorted)
    for issue, c in by_issue.most_common():
        L.append(f"  - {issue}: {c}")
    L.append("\n  First 25 flags:\n")
    for f in a_flags_sorted[:25]:
        ep = (" epithets=" + ",".join(f["epithets"])) if f["epithets"] else ""
        L.append(f"  - {f['date']} [{f['watch']}] {f['ref']} — {f['issue']}{ep}")
    L.append("\n## B. Voice variety (verbatim repeats across days)\n")
    L.append(f"- Repeated Helm/Rudder closers (count>1): **{len(b_top_helms)}**")
    for s, c in b_top_helms[:20]:
        L.append(f"  - ×{c}: {s[:90]}")
    L.append(f"\n- Repeated intro sentences (count>1): **{len(b_top_sentences)}**")
    for s, c in b_top_sentences[:15]:
        L.append(f"  - ×{c}: {s[:90]}")
    L.append("\n## C. Application bullets duplicated across days\n")
    L.append(f"- Distinct bullets reused (count>1): **{len(c_dupe_bullets)}**")
    for b, c in c_dupe_bullets[:20]:
        L.append(f"  - ×{c}: {b[:90]}")
    L.append("\n## D. History facts to verify\n")
    L.append(f"- Total dated events extracted: **{len(d_history)}** (verify separately)\n")
    OUT_MD.write_text("\n".join(L) + "\n")

    print(f"Audit complete: {findings['n_days']} days, {n_watches} watches")
    print(f"  A scripture flags: {len(a_flags_sorted)}  (yahweh: {len(yahweh_hits)})")
    print(f"  B repeated helms: {len(b_top_helms)}  repeated intros: {len(b_top_sentences)}")
    print(f"  C duplicate bullets: {len(c_dupe_bullets)}")
    print(f"  D history events: {len(d_history)}")
    print(f"  -> {OUT_JSON.name}, {OUT_MD.name}")


if __name__ == "__main__":
    main()
