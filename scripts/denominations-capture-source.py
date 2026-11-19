#!/usr/bin/env python3
"""Capture an official denomination source page as a deterministic text snapshot.

  python3 scripts/denominations-capture-source.py <denom_id> <slug> <url>

Writes data/denominations/sources/<denom_id>/<slug>.txt (visible text, the same
normalization the full-review fetcher uses) and <slug>.meta.json (url, final_url,
http_status, retrieved_at, sha256 of the raw HTML and of the text). The builder
validates every evidence quote against these snapshots, so a quote that is not
on the official page can never produce a score. No model, no search engine.
"""
import datetime, hashlib, json, os, re, html, sys, urllib.request, ssl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}

def visible_text(raw):
    t = re.sub(r"<(script|style|svg|head|noscript|template)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()

def main(denom, slug, url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
        raw_b = r.read(); status = r.status; final = r.geturl()
    raw = raw_b.decode("utf-8", "replace")
    text = visible_text(raw)
    d = os.path.join(ROOT, "data", "denominations", "sources", denom); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, slug + ".txt"), "w").write(text + "\n")
    meta = {"url": url, "final_url": final, "http_status": status,
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "sha256_html": hashlib.sha256(raw_b).hexdigest(), "sha256_text": hashlib.sha256(text.encode()).hexdigest(),
            "extractor": "denominations-capture-source.py (urllib + tag strip; no model)"}
    json.dump(meta, open(os.path.join(d, slug + ".meta.json"), "w"), indent=1); open(os.path.join(d, slug + ".meta.json"), "a").write("\n")
    print(slug, status, len(text), meta["sha256_text"][:12])

if __name__ == "__main__":
    main(*sys.argv[1:4])
