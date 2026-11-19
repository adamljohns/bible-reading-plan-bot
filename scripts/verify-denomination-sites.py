#!/usr/bin/env python3
"""Verify proposed official sites for denomination stub pages.

  python3 scripts/verify-denomination-sites.py [id ...]

Fetches each proposed URL in data/denominations/sites/official-sites.json (browser
UA, follows redirects) and records http_status, final_url, checked_at and ok
under "verified". ok = HTTP 200 AND the final host is the proposed domain or a
subdomain of it (www. ignored). The page builder links only ok entries, so a
dead, parked or redirected-away domain never ships as a link. No model.
"""
import datetime, json, os, ssl, sys, urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(ROOT, "data", "denominations", "sites", "official-sites.json")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}


def host(u):
    h = (urlparse(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def same_site(proposed, final):
    p, f = host(proposed), host(final)
    return bool(p) and (f == p or f.endswith("." + p))


def check(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25, context=ssl.create_default_context()) as r:
            return r.status, r.geturl(), None
    except urllib.error.HTTPError as e:
        return e.code, e.geturl() or url, str(e)
    except Exception as e:  # noqa: BLE001
        return None, url, str(e)[:160]


def main():
    doc = json.load(open(FILE))
    ids = sys.argv[1:] or sorted(doc["proposed"])
    for i in ids:
        url = doc["proposed"][i]
        status, final, err = check(url)
        ok = status == 200 and same_site(url, final)
        doc["verified"][i] = {"url": url, "http_status": status, "final_url": final, "ok": ok,
                              "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
        if err:
            doc["verified"][i]["error"] = err
        print(f"{i}: {status} {'OK' if ok else 'NO LINK'} {final}")
    doc["verified"] = dict(sorted(doc["verified"].items()))
    with open(FILE, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
