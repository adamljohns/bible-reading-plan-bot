#!/usr/bin/env python3
"""Capture an official denomination source page as a deterministic text snapshot.

  python3 scripts/denominations-capture-source.py <denom_id> <slug> <url>

Writes data/denominations/sources/<denom_id>/<slug>.txt (visible text, the same
normalization the full-review fetcher uses) and <slug>.meta.json (url, final_url,
http_status, retrieved_at, sha256 of the raw HTML and of the text). The builder
validates every evidence quote against these snapshots, so a quote that is not
on the official page can never produce a score. No model, no search engine.

It also writes <slug>.body.txt: the main-body text only (main / role="main" /
article region, with nav, header, footer and aside removed; for a PDF the
whole document text). The quote check matches against the body file ONLY, so
a phrase that appears only in site navigation or a footer can never pass.

  python3 scripts/denominations-capture-source.py --recapture-all
re-fetches every existing snapshot from its recorded url (body + full text).
"""
import glob, datetime, hashlib, json, os, re, html, subprocess, sys, tempfile, urllib.request, ssl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from denomination_body_text import body_text  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}

def visible_text(raw):
    t = re.sub(r"<(script|style|svg|head|noscript|template)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()

def pdf_text(raw_b):
    # Official PDFs (Book of Discipline, constitutions): poppler pdftotext, then
    # the same whitespace normalization as HTML. No OCR, no model.
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(raw_b); f.flush()
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", f.name, "-"], capture_output=True, check=True).stdout
    return re.sub(r"\s+", " ", out.decode("utf-8", "replace")).strip()

def main(denom, slug, url, extra=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
        raw_b = r.read(); status = r.status; final = r.geturl()
    is_pdf = raw_b[:5] == b"%PDF-"
    text = pdf_text(raw_b) if is_pdf else visible_text(raw_b.decode("utf-8", "replace"))
    body, region = (text, "pdf (whole document)") if is_pdf else body_text(raw_b.decode("utf-8", "replace"))
    d = os.path.join(ROOT, "data", "denominations", "sources", denom); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, slug + ".txt"), "w").write(text + "\n")
    open(os.path.join(d, slug + ".body.txt"), "w").write(body + "\n")
    meta = {"url": url, "final_url": final, "http_status": status,
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "sha256_html": hashlib.sha256(raw_b).hexdigest(), "sha256_text": hashlib.sha256(text.encode()).hexdigest(),
            "sha256_body": hashlib.sha256(body.encode()).hexdigest(), "body_region": region,
            "extractor": "denominations-capture-source.py (urllib + pdftotext; no model)" if is_pdf else "denominations-capture-source.py (urllib + tag strip; no model)"}
    if extra:
        meta.update({k: v for k, v in extra.items() if k != "links_to"})
    if extra and extra.get("links_to"):
        # Provenance page: prove at capture time that this official page links
        # to the off-domain file (e.g. a Webflow-hosted PDF).
        target = extra["links_to"]
        raw = raw_b.decode("utf-8", "replace")
        meta["links_to"] = target
        meta["links_to_verified"] = ('href="%s"' % target) in raw or ('href="%s"' % html.escape(target)) in raw
        if not meta["links_to_verified"]:
            sys.exit("%s does not link to %s" % (url, target))
    json.dump(meta, open(os.path.join(d, slug + ".meta.json"), "w"), indent=1); open(os.path.join(d, slug + ".meta.json"), "a").write("\n")
    print(denom, slug, status, region, len(text), len(body), meta["sha256_body"][:12])

def recapture_all():
    for m in sorted(glob.glob(os.path.join(ROOT, "data", "denominations", "sources", "*", "*.meta.json"))):
        denom = os.path.basename(os.path.dirname(m)); slug = os.path.basename(m)[:-len(".meta.json")]
        old = json.load(open(m))
        keep = {k: v for k, v in old.items() if k in ("linked_from", "linked_from_snapshot", "links_to")}
        main(denom, slug, old["url"], keep)

if __name__ == "__main__":
    if sys.argv[1:2] == ["--recapture-all"]:
        recapture_all()
    else:
        # optional 4th arg: --links-to=<url> (assert and record the link)
        ex = {"links_to": sys.argv[4].split("=", 1)[1]} if len(sys.argv) > 4 and sys.argv[4].startswith("--links-to=") else None
        main(*sys.argv[1:4], ex)
