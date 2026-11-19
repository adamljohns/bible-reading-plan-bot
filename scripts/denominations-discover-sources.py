#!/usr/bin/env python3
"""Find candidate official doctrine pages for a stub body (no model).

  python3 scripts/denominations-discover-sources.py <denom_id> [--max 3]

Reads the VERIFIED official site from data/denominations/sites/official-sites.json
(ok=true only), fetches the home page, and prints "<slug> <url>" lines for
same-domain links whose URL or link text names a doctrinal page (beliefs,
statement of faith, confession, doctrine, position statements, constitution).
grind/queue.json "sources" entries come first when present. Exit 3 when the
body has no verified site and no queued sources: the grind holds it.
"""
import html, json, os, re, ssl, sys, urllib.request
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
KEY = re.compile(r"belie|statement[- ]of[- ]faith|confession|doctrin|position|constitution|what[- ]we[- ]teach|standards|theolog|faith[- ]and[- ]message|articles[- ]of[- ]religion", re.I)
SKIP = re.compile(r"\.(jpg|png|gif|mp3|mp4|zip|docx?)$|mailto:|tel:|#|/(tag|category|author|news|events?|blog|store|shop|donate|login)/", re.I)


def host(u):
    h = (urlparse(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def slugify(u):
    p = urlparse(u).path.strip("/").split("/")[-1] or "home"
    p = re.sub(r"\.(html?|php|aspx|pdf)$", "", p, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", p.lower()).strip("-")[:50] or "page"


def main():
    denom = sys.argv[1]
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 3
    q = json.load(open(os.path.join(ROOT, "data", "denominations", "grind", "queue.json")))
    out = list((q.get("sources") or {}).get(denom, {}).items())
    sites = json.load(open(os.path.join(ROOT, "data", "denominations", "sites", "official-sites.json")))
    v = sites["verified"].get(denom)
    if v and v.get("ok") and len(out) < mx:
        try:
            raw = urllib.request.urlopen(urllib.request.Request(v["url"], headers=UA), timeout=30,
                                         context=ssl.create_default_context()).read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"home page fetch failed: {e}", file=sys.stderr)
            raw = ""
        seen = {u for _, u in out}
        for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', raw, re.S | re.I):
            href, text = html.unescape(m.group(1)), re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
            u = urljoin(v["url"], href).split("#")[0]
            if SKIP.search(u) or not u.startswith("http"):
                continue
            h, base = host(u), host(v["url"])
            if not (h == base or h.endswith("." + base)):
                continue
            if not (KEY.search(u) or KEY.search(text)) or u in seen:
                continue
            seen.add(u)
            out.append((slugify(u), u))
            if len(out) >= mx:
                break
    if not out:
        print("no verified official site and no queued sources", file=sys.stderr)
        sys.exit(3)
    used = set()
    for slug, u in out[:mx]:
        s = slug
        while s in used:
            s += "-2"
        used.add(s)
        print(s, u)


if __name__ == "__main__":
    main()
