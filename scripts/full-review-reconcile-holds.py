#!/usr/bin/env python3
"""Reconcile the full-review HOLD queue against current data and the live web.

For every row in data/full-review/hold-queue.json this script records, under
`reconcile`, the retrieval evidence a QA decision needs:

  retrieved_at, http_status, final_url    - a fresh fetch of evidence.url
  quote_found                             - evidence.quote is on that page
                                            (raw HTML or visible text, normalized
                                            exactly like full-review-fetch.py)
  current_value, old_matches_current      - the stored value today vs the row's
                                            `old` (a mismatch = stale row; the
                                            applier would skip it anyway)

It NEVER changes qa_status, never touches churches.json, and keeps the row's
source URL, verbatim quote and rule untouched. QA decisions are separate.
Network: plain HTTP GETs of the church's own pages, 1 request/second/host.
No search engine and no model is called.

Usage: python3 scripts/full-review-reconcile-holds.py [--queue PATH] [--write]
"""
import datetime
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("frf", os.path.join(ROOT, "scripts", "full-review-fetch.py"))
frf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frf)


def get_path(obj, dotted):
    cur = obj
    for k in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def same(a, b):
    norm = lambda v: None if v in (None, "", []) else v
    return json.dumps(norm(a), sort_keys=True) == json.dumps(norm(b), sort_keys=True)


def quote_on_page(quote, raw):
    if not quote or not raw:
        return False
    q = frf.nrm(quote).strip(" .,;:\"'")
    if len(q) < 4:
        return False
    return q in frf.nrm(raw) or q in frf.nrm(frf.page_text(raw))


def main():
    args = sys.argv[1:]
    qpath = args[args.index("--queue") + 1] if "--queue" in args else os.path.join(ROOT, "data/full-review/hold-queue.json")
    queue = json.load(open(qpath))
    data = json.load(open(os.path.join(ROOT, "docs/data/churches.json")))
    churches = {c.get("id"): c for c in (data if isinstance(data, list) else data["churches"])}
    cache = {}
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    for h in queue["holds"]:
        ev = h.get("evidence") or {}
        url = ev.get("url")
        if url and url not in cache:
            cache[url] = frf.polite_fetch(url, timeout=20)
        final_url, status, raw = cache.get(url, (None, None, ""))
        c = churches.get(h["church_id"])
        rec = {"retrieved_at": now, "http_status": status, "final_url": final_url,
               "church_exists": c is not None}
        etype = ev.get("evidence_type")
        if etype == "http_redirect":
            rec["quote_found"] = bool(final_url) and final_url.rstrip("/") == str(h.get("new") or "").rstrip("/")
        elif etype in ("stored_value",) or (h["kind"] == "flag" and ev.get("this_website")):
            rec["quote_found"] = bool(c) and ev.get("quote", "").rstrip("/").split("//")[-1].lstrip("w.") in json.dumps(c)
            rec["quote_check"] = "stored-record"
        else:
            rec["quote_found"] = quote_on_page(ev.get("quote"), raw)
        if h["kind"] == "change" and c is not None:
            cur = get_path(c, h["field"])
            rec["current_value"] = cur
            rec["old_matches_current"] = same(cur, h.get("old"))
            rec["already_new"] = same(cur, h.get("new"))
        h["reconcile"] = rec
    stale = [h["hold_id"] for h in queue["holds"] if h["kind"] == "change" and not h["reconcile"].get("old_matches_current", True)]
    missing = [h["hold_id"] for h in queue["holds"] if not h["reconcile"]["quote_found"]]
    print(f"rows={len(queue['holds'])} stale={len(stale)} quote_missing={len(missing)}")
    for s in stale:
        print("  STALE", s)
    for m in missing:
        print("  QUOTE-NOT-FOUND", m)
    if "--write" in args:
        with open(qpath, "w") as f:
            json.dump(queue, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print("wrote", qpath)


if __name__ == "__main__":
    main()
