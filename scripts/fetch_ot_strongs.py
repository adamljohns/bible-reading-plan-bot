#!/usr/bin/env python3
"""
Backfill OT chapter JSONs (Strong's-tagged KJV + 11 other translations)
for every Old Testament book except Psalms (19) and Proverbs (20), which
are already cached.

This is what unlocks Strong's-link clickability for Genesis–Malachi in
the Bible Translation Engine (docs/bible.html): bolls.life ships KJV
text with inline <S>####</S> Strong's tags, and bible.html pulls those
into the verse render path.

Resume-able: chapters with existing JSON files in docs/assets/chapters/
are skipped. Run from repo root:
    python3 scripts/fetch_ot_strongs.py
"""

import json
import time
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO / "docs/assets/chapters"

# 12 translations to fetch — must match what bible.html consumes.
TRANSLATIONS = ['NKJV', 'KJV', 'ESV', 'NASB', 'NLT', 'WEB',
                'CSB17', 'AMP', 'MSG', 'NIV', 'NRSVCE', 'NET']

# OT books minus Psalms (19) + Proverbs (20) — those are already cached.
# {bookId: chapter_count}
OT_BOOKS = {
    1: 50,    # Genesis
    2: 40,    # Exodus
    3: 27,    # Leviticus
    4: 36,    # Numbers
    5: 34,    # Deuteronomy
    6: 24,    # Joshua
    7: 21,    # Judges
    8: 4,     # Ruth
    9: 31,    # 1 Samuel
    10: 24,   # 2 Samuel
    11: 22,   # 1 Kings
    12: 25,   # 2 Kings
    13: 29,   # 1 Chronicles
    14: 36,   # 2 Chronicles
    15: 10,   # Ezra
    16: 13,   # Nehemiah
    17: 10,   # Esther
    18: 42,   # Job
    21: 12,   # Ecclesiastes
    22: 8,    # Song of Solomon
    23: 66,   # Isaiah
    24: 52,   # Jeremiah
    25: 5,    # Lamentations
    26: 48,   # Ezekiel
    27: 12,   # Daniel
    28: 14,   # Hosea
    29: 3,    # Joel
    30: 9,    # Amos
    31: 1,    # Obadiah
    32: 4,    # Jonah
    33: 7,    # Micah
    34: 3,    # Nahum
    35: 3,    # Habakkuk
    36: 3,    # Zephaniah
    37: 2,    # Haggai
    38: 14,   # Zechariah
    39: 4,    # Malachi
}

BASE_URL = "https://bolls.life/get-chapter"
MAX_WORKERS = 4               # max concurrent in-flight requests
DELAY_BETWEEN_CHAPTERS = 0.3  # courtesy pause between chapter batches
REQUEST_TIMEOUT = 30

# bolls.life cert chain occasionally fails verification on macOS — silence warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_translation(book_id, chapter, translation):
    """Return (translation, {verseNum: text} | None)."""
    url = f"{BASE_URL}/{translation}/{book_id}/{chapter}/"
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
        if r.status_code != 200:
            print(f"  WARN  {translation} {book_id}:{chapter} -> HTTP {r.status_code}")
            return translation, None
        data = r.json()
        if not isinstance(data, list):
            return translation, None
        return translation, {str(v['verse']): v.get('text', '') for v in data}
    except Exception as e:
        print(f"  ERR   {translation} {book_id}:{chapter} -> {e}")
        return translation, None


def fetch_chapter(book_id, chapter):
    """Fetch all 12 translations for one chapter in parallel; return combined dict."""
    combined = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(fetch_translation, book_id, chapter, t) for t in TRANSLATIONS]
        for fut in as_completed(futures):
            trans, data = fut.result()
            if data:
                combined[trans] = data
    return combined


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_chapters = []
    for book_id in sorted(OT_BOOKS):
        for ch in range(1, OT_BOOKS[book_id] + 1):
            all_chapters.append((book_id, ch))

    total = len(all_chapters)
    print(f"OT Strong's backfill")
    print(f"  Books: {len(OT_BOOKS)}   Chapters: {total}   Translations: {len(TRANSLATIONS)}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    # Resume: skip already-cached chapters.
    to_fetch, skipped = [], 0
    for book_id, ch in all_chapters:
        out_path = OUTPUT_DIR / f"{book_id}_{ch}.json"
        if out_path.exists():
            skipped += 1
        else:
            to_fetch.append((book_id, ch))

    if skipped:
        print(f"  Skipping {skipped} already-cached chapters")
    if not to_fetch:
        print("All chapters already cached.")
        return
    print(f"  Fetching {len(to_fetch)} chapters...\n")

    start = time.time()
    for i, (book_id, ch) in enumerate(to_fetch, 1):
        out_path = OUTPUT_DIR / f"{book_id}_{ch}.json"
        combined = fetch_chapter(book_id, ch)
        if combined:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(combined, f, ensure_ascii=False)
        else:
            print(f"  WARN  no data for book {book_id} ch {ch}")

        if i % 10 == 0 or i == len(to_fetch):
            elapsed = time.time() - start
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(to_fetch) - i) / rate if rate > 0 else 0
            trans_count = len(combined) if combined else 0
            print(f"  {i:4d}/{len(to_fetch)}  book {book_id:2d} ch {ch:3d}"
                  f"  ({trans_count} translations) | "
                  f"{elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining")

        if i < len(to_fetch):
            time.sleep(DELAY_BETWEEN_CHAPTERS)

    elapsed = time.time() - start
    cached = sum(1 for (b, c) in all_chapters if (OUTPUT_DIR / f"{b}_{c}.json").exists())
    print(f"\nDone. {cached}/{total} chapters cached in {elapsed:.0f}s.")


if __name__ == '__main__':
    main()
