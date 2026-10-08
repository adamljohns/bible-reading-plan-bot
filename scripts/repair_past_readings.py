#!/usr/bin/env python3
"""Re-lay mashed Scripture blocks on already-delivered reading days.

MBP-1007-SPRINT. The 2026-10-06 sweep (bible-engine-1006-reading-scripture-
mismatch.txt) found past days whose Scripture block shows the wrong verses:
01-18 "Psalm 120" shows Psalm 121, 07-25 "Micah 3" shows Ezekiel 34, 06-20 is
labelled "Psalm 19:153-160" (Psalm 119). Future days were repaired one by one
with repair_passage_block.py; this does the same for the past in one pass.

For each watch from --from to --through:

  label  The label is kept unless it names verses that do not exist (no
         canonical text resolves), in which case docs/assets/plan-data.js
         supplies it. A valid label that merely differs from the plan is
         reported, not changed.
  block  Re-laid from docs/assets/chapters (repair_passage_block.canonical_block)
         when the passage-containment gate or the loop gate fails it, or when
         the label changed. Context, Reflection, Prayer and Charge are never
         touched.

Writes (only with --apply): docs/assets/readings/<date>.json (same
serialisation as the file had), data/readings/<date>.md, the scripture div in
docs/readings/<date>.html (surgical — the page template is not regenerated),
and docs/assets/reading-index.json labels. Baked audio is NOT re-baked; the
report lists which repaired watches carry audio.

Usage:
  python3 scripts/repair_past_readings.py --report /tmp/past.txt            # dry run
  python3 scripts/repair_past_readings.py --report /tmp/past.txt --apply
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import check_passage_containment as cpc  # noqa: E402
import check_scripture_loops as csl  # noqa: E402
from build_reading_page_from_md import render_scripture_block  # noqa: E402
from repair_passage_block import canonical_block  # noqa: E402

JSON_DIR = REPO / "docs" / "assets" / "readings"
MD_DIR = REPO / "data" / "readings"
HTML_DIR = REPO / "docs" / "readings"
INDEX = REPO / "docs" / "assets" / "reading-index.json"
PLAN = REPO / "docs" / "assets" / "plan-data.js"

CONTAIN_CODES = {"foreign_content", "duplicate_line"}
LOOP_CODES = {"scripture_loop", "chapter_bleed", "translation_doublet"}
HEADER_RE = re.compile(r"^(📖[^\n]*)$", re.M)


def load_plan() -> dict[str, dict]:
    plan = {}
    for ln in PLAN.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^\s*"(\d{4}-\d{2}-\d{2})"\s*:\s*(\{.*\})\s*,?\s*$', ln)
        if m:
            plan[m.group(1)] = json.loads(m.group(2))
    return plan


def resolves(label: str) -> bool:
    try:
        return bool(label) and canonical_block(label) is not None
    except Exception:
        return False


def same_refs(a: str, b: str) -> bool:
    pa, pb = cpc.parse_passage(a), cpc.parse_passage(b)
    return pa is not None and pa == pb


def json_dump_like(obj, raw: str) -> str:
    """Re-serialise in the exact shape the file already had."""
    for kw in (dict(indent=1, ensure_ascii=False), dict(indent=2, ensure_ascii=False),
               dict(indent=1), dict(indent=2)):
        for nl in ("", "\n"):
            if json.dumps(json.loads(raw), **kw) + nl == raw:
                return json.dumps(obj, **kw) + nl
    raise ValueError("unrecognised JSON serialisation; refusing to rewrite")


def retitle(text: str, old_label: str, new_label: str) -> str:
    """Replace the label on the Scripture header line only."""
    m = HEADER_RE.search(text)
    if not m or old_label == new_label:
        return text
    hdr = m.group(1)
    if old_label not in hdr:
        return text
    return text[: m.start(1)] + hdr.replace(old_label, new_label, 1) + text[m.end(1):]


def repair_watch(date: str, wkey: str, w: dict, plan_label: str | None):
    """Return (row, new_text, new_label) — row is a report dict or None."""
    text = w.get("text") or ""
    old = w.get("passage") or ""
    new = old
    note = []
    if not resolves(old):
        if plan_label and resolves(plan_label):
            new = plan_label
        else:
            return ({"date": date, "watch": wkey, "old": old, "new": old,
                     "action": "UNRESOLVED", "why": "label and plan both unresolvable"},
                    None, None)
    elif plan_label and not same_refs(old, plan_label):
        note.append(f"plan says {plan_label}")

    scr, bounded = cpc.extract_scripture_bounded(text)
    if not scr or not bounded:
        return ({"date": date, "watch": wkey, "old": old, "new": new,
                 "action": "SKIP", "why": "Scripture block not bounded"}, None, None)

    codes = sorted({f["code"] for f in cpc.check_watch(date, wkey, new, text)} & CONTAIN_CODES)
    codes += sorted({f["code"] for f in csl.check_watch(date, wkey, new, text, None)} & LOOP_CODES)
    if not codes and new == old:
        if note:
            return ({"date": date, "watch": wkey, "old": old, "new": old,
                     "action": "NOTE", "why": "; ".join(note)}, None, None)
        return None, None, None

    from repair_passage_block import repair_text
    res = repair_text(text, new)
    if not res:
        return ({"date": date, "watch": wkey, "old": old, "new": new,
                 "action": "SKIP", "why": "canonical block unavailable"}, None, None)
    new_text, old_n, new_n = res
    new_text = retitle(new_text, old, new)
    why = ",".join(codes) or "label"
    if "blended" in old.lower() or "listening" in old.lower() or "selected" in old.lower():
        note.append("label marks a deliberate blended/listening render")
    if w.get("has_audio"):
        note.append("has baked audio (not re-baked)")
    return ({"date": date, "watch": wkey, "old": old, "new": new,
             "action": "RELABEL+RELAY" if new != old else "RELAY",
             "why": f"{why}; {old_n} lines -> {new_n} verses" + ("; " + "; ".join(note) if note else "")},
            new_text, new)


def patch_html(page: str, wkey: str, new_label: str, new_scr: str) -> str | None:
    # Older pages id the middle watches by role, not by key.
    ids = {wkey, {"first": "husband", "second": "father", "third": "citizen"}.get(wkey, wkey)}
    sec = None
    for sid in ids:
        sec = re.search(rf'<section class="watch [^"]*" id="{sid}"[\s\S]*?</section>', page)
        if sec:
            break
    if not sec:
        return None
    body = sec.group(0)
    m = re.search(r'<div class="scripture">\n<div class="scripture-ref">[\s\S]*?</div>\n'
                  r'<div class="scripture-text">\n[\s\S]*?\n</div>\n</div>', body)
    if not m:
        return None
    block = render_scripture_block(f"📖 Scripture — {new_label}", new_scr.split("\n"))
    body = body[: m.start()] + block + body[m.end():]
    return page[: sec.start()] + body + page[sec.end():]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="start", default="2026-01-01")
    ap.add_argument("--through", default="2026-10-07")
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    plan = load_plan()
    rows = []
    index_raw = INDEX.read_text(encoding="utf-8")
    index = json.loads(index_raw)
    index_changed = False

    for jp in sorted(JSON_DIR.glob("2026-*.json")):
        date = jp.stem
        if not (args.start <= date <= args.through):
            continue
        raw = jp.read_text(encoding="utf-8")
        day = json.loads(raw)
        md_p, html_p = MD_DIR / f"{date}.md", HTML_DIR / f"{date}.html"
        md = md_p.read_text(encoding="utf-8") if md_p.exists() else None
        page = html_p.read_text(encoding="utf-8") if html_p.exists() else None
        changed = False
        for wkey, w in (day.get("watches") or {}).items():
            row, new_text, new_label = repair_watch(date, wkey, w, (plan.get(date) or {}).get(wkey))
            if row is None:
                continue
            rows.append(row)
            if new_text is None:
                continue
            old_text = w.get("text") or ""
            old_scr, _ = cpc.extract_scripture_bounded(old_text)
            new_scr, _ = cpc.extract_scripture_bounded(new_text)
            w["text"], w["passage"] = new_text, new_label
            changed = True
            if md is not None:
                if md.count(old_scr) == 1:
                    md = md.replace(old_scr, new_scr, 1)
                    md = retitle_md(md, new_scr, row["old"], new_label)
                else:
                    md2 = replace_md_by_header(md, row["old"], new_label, new_scr)
                    if md2 is None:
                        row["why"] += "; md block not matched (md untouched)"
                    else:
                        md = md2
            if page is not None:
                p2 = patch_html(page, wkey, new_label, new_scr.strip("\n"))
                if p2 is None:
                    row["why"] += "; html block not matched (html untouched)"
                else:
                    page = p2
            idx_day = (index.get("days") or {}).get(date)
            if idx_day and (idx_day.get("passages") or {}).get(wkey) == row["old"] \
                    and row["old"] != new_label:
                idx_day["passages"][wkey] = new_label
                index_changed = True
        if args.apply and changed:
            jp.write_text(json_dump_like(day, raw), encoding="utf-8")
            if md is not None:
                md_p.write_text(md, encoding="utf-8")
            if page is not None:
                html_p.write_text(page, encoding="utf-8")

    if args.apply and index_changed:
        INDEX.write_text(json_dump_like(index, index_raw), encoding="utf-8")

    acts = {}
    for r in rows:
        acts[r["action"]] = acts.get(r["action"], 0) + 1
    out = [
        "# Past reading days — Scripture block repair (MBP-1007-SPRINT). "
        f"Range {args.start}..{args.through}. Tool: scripts/repair_past_readings.py.",
        "# Cols: date, watch, old label, new label, action, why. "
        "RELAY = block re-laid from docs/assets/chapters under the same label; "
        "RELABEL+RELAY = label named non-existent verses, plan-data.js label used; "
        "NOTE = left alone, label differs from plan-data.js; SKIP/UNRESOLVED = left alone.",
        "# Counts: " + ", ".join(f"{k}={v}" for k, v in sorted(acts.items()))
        + f"; days touched={len({r['date'] for r in rows if r['action'].startswith(('RELAY', 'RELABEL'))})}",
    ]
    for r in rows:
        out.append("\t".join([r["date"], r["watch"], r["old"], r["new"], r["action"], r["why"]]))
    args.report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(out[2])
    if not args.apply:
        print("(dry run — pass --apply to write)")
    return 0


def replace_md_by_header(md: str, old_label: str, new_label: str, new_scr: str) -> str | None:
    """md text drifted from the JSON: find the block by its unique 📖 header."""
    heads = [m for m in re.finditer(r"^📖[^\n]*$", md, re.M) if old_label in m.group(0)]
    if len(heads) != 1:
        return None
    h = heads[0]
    m = cpc.SCR_RE.search(md, h.start())
    if not m or m.start() != h.start():
        return None
    tail = md[m.end(1): m.end(1) + 4]
    if not tail.strip():
        return None  # unbounded; refuse
    old = m.group(1)
    lead = len(old) - len(old.lstrip("\n"))
    trail = len(old) - len(old.rstrip("\n"))
    body = ("\n" * lead) + new_scr.strip("\n") + ("\n" * trail)
    hdr = h.group(0).replace(old_label, new_label, 1)
    return md[: h.start()] + hdr + md[h.end(): m.start(1)] + body + md[m.end(1):]


def retitle_md(md: str, new_scr: str, old_label: str, new_label: str) -> str:
    """Fix the 📖 header that sits directly above the replaced block in md."""
    if old_label == new_label:
        return md
    pos = md.find(new_scr)
    if pos < 0:
        return md
    hstart = md.rfind("📖", 0, pos)
    hend = md.find("\n", hstart)
    if hstart < 0 or hend < 0 or hend > pos:
        return md
    hdr = md[hstart:hend]
    return md[:hstart] + hdr.replace(old_label, new_label, 1) + md[hend:]


if __name__ == "__main__":
    sys.exit(main())
