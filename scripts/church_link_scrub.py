#!/usr/bin/env python3
"""
church_link_scrub.py — parallel HTTP probe of every church.website in churches.json.

Emits a JSON triage report sorted by severity:
  - dns_fail   (DNS never resolved)
  - timeout    (connected but never responded)
  - http_4xx   (404, 410, etc. — likely dead)
  - http_5xx   (server error — could be transient)
  - parked     (resolves + 200 OK but heuristic flags as parked/for-sale)
  - redirect_offsite (permanent redirect to a suspicious domain)
  - ok         (2xx, no parked indicators)

Usage:
    python3 scripts/church_link_scrub.py \
        --input docs/data/churches.json \
        --output docs/data/link_scrub_report.json \
        --workers 40 --timeout 15
"""

import argparse
import concurrent.futures as cf
import json
import re
import socket
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip3 install requests", file=sys.stderr)
    sys.exit(2)

# Common parked-domain / for-sale signatures. Keep these narrow — false positives are costly.
PARKED_SIGNATURES = [
    r"this\s+domain\s+is\s+for\s+sale",
    r"buy\s+this\s+domain",
    r"domain\s+may\s+be\s+for\s+sale",
    r"godaddy\.com/domainfind",
    r"sedoparking\.com",
    r"parkingcrew\.net",
    r"hugedomains\.com",
    r"afternic\.com",
    r"dan\.com\"",
    r"<title>[^<]*for sale[^<]*</title>",
]
PARKED_RE = re.compile("|".join(PARKED_SIGNATURES), re.IGNORECASE)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

def probe(church, timeout):
    url = church.get("website") or ""
    result = {
        "id": church.get("id"),
        "name": church.get("name"),
        "address": church.get("address"),
        "url": url,
        "overall_rating": church.get("overall_rating"),
    }
    if not url or not url.startswith(("http://", "https://")):
        result["status"] = "no_url"
        return result

    host = urlparse(url).hostname or ""
    # DNS first — quick fail path
    try:
        socket.gethostbyname(host)
    except socket.gaierror as e:
        result["status"] = "dns_fail"
        result["error"] = str(e)
        return result

    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"}
    try:
        # HEAD first (cheap). If server rejects, fall back to GET.
        r = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        if r.status_code in (405, 501) or r.status_code >= 500:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)
            body = next(r.iter_content(chunk_size=16384, decode_unicode=True), "") or ""
            r.close()
        else:
            body = ""
        result["http_status"] = r.status_code
        final_url = r.url
        result["final_url"] = final_url

        final_host = urlparse(final_url).hostname or ""
        if final_host and host and not final_host.endswith(host.split(".", 1)[-1]):
            result["redirect_offsite"] = True

        if r.status_code >= 400 and r.status_code < 500:
            result["status"] = "http_4xx"
            return result
        if r.status_code >= 500:
            result["status"] = "http_5xx"
            return result

        # If we need body to sniff for parked, do one GET with limited content
        if not body:
            try:
                g = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)
                body = next(g.iter_content(chunk_size=32768, decode_unicode=True), "") or ""
                g.close()
            except Exception:
                body = ""

        if body and PARKED_RE.search(body):
            result["status"] = "parked"
            return result

        if result.get("redirect_offsite"):
            result["status"] = "redirect_offsite"
            return result

        result["status"] = "ok"
        return result
    except requests.exceptions.ConnectTimeout:
        result["status"] = "timeout"
        result["error"] = "connect timeout"
        return result
    except requests.exceptions.ReadTimeout:
        result["status"] = "timeout"
        result["error"] = "read timeout"
        return result
    except requests.exceptions.SSLError as e:
        result["status"] = "ssl_error"
        result["error"] = str(e)[:200]
        return result
    except requests.exceptions.ConnectionError as e:
        result["status"] = "conn_error"
        result["error"] = str(e)[:200]
        return result
    except Exception as e:
        result["status"] = "unknown_error"
        result["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workers", type=int, default=40)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--limit", type=int, default=0, help="Only probe first N (debugging)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    churches = data.get("churches") or []
    if args.limit:
        churches = churches[: args.limit]
    total = len(churches)
    print(f"Probing {total} churches with {args.workers} workers, timeout={args.timeout}s", file=sys.stderr)

    start = time.time()
    results = []
    severity_order = {
        "dns_fail": 0,
        "conn_error": 1,
        "ssl_error": 2,
        "timeout": 3,
        "http_4xx": 4,
        "http_5xx": 5,
        "parked": 6,
        "redirect_offsite": 7,
        "unknown_error": 8,
        "no_url": 9,
        "ok": 10,
    }

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, c, args.timeout): c for c in churches}
        done = 0
        for fut in cf.as_completed(futures):
            results.append(fut.result())
            done += 1
            if done % 200 == 0:
                elapsed = time.time() - start
                print(f"  {done}/{total} probed ({elapsed:.0f}s)", file=sys.stderr)

    elapsed = time.time() - start

    results.sort(key=lambda r: (severity_order.get(r.get("status", "ok"), 99), r.get("name") or ""))
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": total,
        "elapsed_sec": round(elapsed, 1),
        "counts": counts,
        "results": results,
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nCompleted in {elapsed:.0f}s. Summary:", file=sys.stderr)
    for s, n in sorted(counts.items(), key=lambda kv: severity_order.get(kv[0], 99)):
        print(f"  {s:20s} {n}", file=sys.stderr)
    print(f"\nWrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
