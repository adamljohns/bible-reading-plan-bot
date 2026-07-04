#!/usr/bin/env python3
"""Ingest public-domain foreign-language Bibles into a PARALLEL chapter store
(docs/assets/chapters-ml/<book>_<chapter>.json), keyed by language code — so the
English BTE files in chapters/ stay byte-for-byte untouched. The bible.html
language selector fetches from chapters-ml/ when a non-English language is chosen.

Source: getbible.net v2 (per-book fetch, polite). Only PD texts are used here;
fr/es/pt are sourced separately (open-bibles/eBible) in a later pass.

  python3 scripts/ingest_ml_bible.py --books 43     # one book (test)
  python3 scripts/ingest_ml_bible.py                # all 66 books
"""
import argparse, json, time, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "assets" / "chapters-ml"
BASE = "https://api.getbible.net/v2"

# language key -> (getbible code, human label, public-domain source note)
LANGS = {
    "zh": ("cus",        "中文 (和合本)",   "Chinese Union, Simplified — Public Domain"),
    "la": ("vulgate",    "Latina",          "Vulgata Clementina — Public Domain"),
    "de": ("luther1545", "Deutsch (Luther)", "Luther 1545 — Public Domain"),
    "ja": ("japbungo",   "日本語",          "Meiji/Taisho — Public Domain"),
    "es": ("sse",        "Español",         "Sagradas Escrituras 1569 — Public Domain"),
    "fr": ("darby",      "Français",        "Darby (French) — Public Domain"),
}


def fetch_book(code, booknr, tries=3):
    url = f"{BASE}/{code}/{booknr}.json"
    req = urllib.request.Request(url, headers={"User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120 Safari/537.36"})
    for t in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if t == tries - 1:
                print(f"  FAIL {code} book {booknr}: {e}", flush=True)
                return None
            time.sleep(1.5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--books", help="comma list; default 1-66")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    books = [int(x) for x in args.books.split(",")] if args.books else list(range(1, 67))

    for booknr in books:
        perlang = {}
        for lang, (code, _, _) in LANGS.items():
            d = fetch_book(code, booknr)
            time.sleep(0.2)
            if not d:
                continue
            cmap = {}
            for ch in (d.get("chapters") or []):
                cnum = str(ch.get("chapter"))
                verses = {str(v.get("verse")): (v.get("text") or "").strip()
                          for v in (ch.get("verses") or []) if (v.get("text") or "").strip()}
                if verses:
                    cmap[cnum] = verses
            perlang[lang] = cmap

        allchaps = set()
        for lang in perlang:
            allchaps |= set(perlang[lang].keys())
        for cnum in sorted(allchaps, key=int):
            path = OUT / f"{booknr}_{cnum}.json"
            data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            for lang in perlang:
                if cnum in perlang[lang]:
                    data[lang] = perlang[lang][cnum]
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"book {booknr}: {len(allchaps)} chapters x {len(perlang)} langs", flush=True)
    print("done")


if __name__ == "__main__":
    main()
