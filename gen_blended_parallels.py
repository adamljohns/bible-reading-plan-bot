#!/usr/bin/env python3
"""
BTE v4.1 — Verse Cache Generator
=================================
Fetches ALL 11 translations for every verse in the Bible (all 66 books).
NO AI/Claude blending. Raw translation text cached for client-side rotation.

Output:  docs/assets/verse-cache.json
Format:  {"43_3_16": {"NKJV": "...", "NLT": "...", "ESV": "...", ...}}

Progress: verse-cache-progress.json  (key: "book_id_chapter" = done)

Usage:
  python3 gen_blended_parallels.py              # Full run (all 66 books)
  python3 gen_blended_parallels.py --test       # Quick test: Genesis 1 + John 3
  python3 gen_blended_parallels.py --book 43    # Single book (John)

bolls.life chapter API: GET /get-chapter/{translation}/{book_id}/{chapter}/
Returns: [{"verse": 1, "text": "..."}, ...]
Rate: 0.2s between calls → 11 trans × 1,189 chapters = 13,079 calls ≈ 44 min
"""

import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ─── Config ────────────────────────────────────────────────────────────────────
REPO_DIR    = Path("/Users/adamjohns/bible-reading-plan-bot")
OUTPUT_FILE = REPO_DIR / "docs/assets/verse-cache.json"
PROGRESS    = REPO_DIR / "verse-cache-progress.json"

# Verified working codes on bolls.life (CSB→CSB17, NRSV→NRSVCE)
TRANSLATIONS = ['NKJV', 'KJV', 'ESV', 'NASB', 'NLT', 'WEB', 'CSB17', 'AMP', 'MSG', 'NIV', 'NRSVCE']

CHAPTER_API  = 'https://bolls.life/get-chapter/{trans}/{book_id}/{chapter}/'
FETCH_DELAY  = 0.2   # seconds between API calls
SAVE_EVERY   = 5     # save output every N chapters

# ─── Full Bible: 66 books ──────────────────────────────────────────────────────
BIBLE_BOOKS = [
    (1,'Genesis',50),(2,'Exodus',40),(3,'Leviticus',27),(4,'Numbers',36),(5,'Deuteronomy',34),
    (6,'Joshua',24),(7,'Judges',21),(8,'Ruth',4),(9,'1 Samuel',31),(10,'2 Samuel',24),
    (11,'1 Kings',22),(12,'2 Kings',25),(13,'1 Chronicles',29),(14,'2 Chronicles',36),
    (15,'Ezra',10),(16,'Nehemiah',13),(17,'Esther',10),(18,'Job',42),(19,'Psalms',150),
    (20,'Proverbs',31),(21,'Ecclesiastes',12),(22,'Song of Solomon',8),(23,'Isaiah',66),
    (24,'Jeremiah',52),(25,'Lamentations',5),(26,'Ezekiel',48),(27,'Daniel',12),
    (28,'Hosea',14),(29,'Joel',3),(30,'Amos',9),(31,'Obadiah',1),(32,'Jonah',4),
    (33,'Micah',7),(34,'Nahum',3),(35,'Habakkuk',3),(36,'Zephaniah',3),(37,'Haggai',2),
    (38,'Zechariah',14),(39,'Malachi',4),
    (40,'Matthew',28),(41,'Mark',16),(42,'Luke',24),(43,'John',21),(44,'Acts',28),
    (45,'Romans',16),(46,'1 Corinthians',16),(47,'2 Corinthians',13),(48,'Galatians',6),
    (49,'Ephesians',6),(50,'Philippians',4),(51,'Colossians',4),(52,'1 Thessalonians',5),
    (53,'2 Thessalonians',3),(54,'1 Timothy',6),(55,'2 Timothy',4),(56,'Titus',3),
    (57,'Philemon',1),(58,'Hebrews',13),(59,'James',5),(60,'1 Peter',5),(61,'2 Peter',3),
    (62,'1 John',5),(63,'2 John',1),(64,'3 John',1),(65,'Jude',1),(66,'Revelation',22),
]

TOTAL_CHAPTERS = sum(c for _, _, c in BIBLE_BOOKS)  # 1,189

# ─── HTTP session with retries ─────────────────────────────────────────────────
def make_session():
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": "BTE/4.1"})
    return s

SESSION = make_session()

# ─── Text cleaning ─────────────────────────────────────────────────────────────
_STRONGS_RE = re.compile(r'<S>\d+</S>')
_HTML_RE    = re.compile(r'<[^>]+>')
_WS_RE      = re.compile(r'\s{2,}')
# Unicode circled letters (NRSVCE footnote markers like ⓐ ⓑ etc.)
_CIRCLE_RE  = re.compile(r'[\u24b6-\u24ff\u2460-\u2473]')
# Bracketed footnote numbers like [5], [6]
_FOOTNOTE_RE = re.compile(r'\[\d+\]')

def clean_text(text: str) -> str:
    """Strip HTML tags, Strong's numbers, footnote markers."""
    text = _STRONGS_RE.sub('', text)
    text = _HTML_RE.sub('', text)
    text = _CIRCLE_RE.sub('', text)
    text = _FOOTNOTE_RE.sub('', text)
    text = _WS_RE.sub(' ', text)
    return text.strip()


# ─── Fetch one chapter for one translation ─────────────────────────────────────
def fetch_chapter(translation: str, book_id: int, chapter: int) -> dict:
    """Returns {verse_num: cleaned_text} or {} on failure."""
    url = CHAPTER_API.format(trans=translation, book_id=book_id, chapter=chapter)
    try:
        resp = SESSION.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            return {}
        result = {}
        for v in data:
            t = clean_text(v.get('text', ''))
            if t and 'not found' not in t.lower():
                result[int(v['verse'])] = t
        return result
    except Exception:
        return {}


# ─── Progress & output ────────────────────────────────────────────────────────
def load_cache() -> dict:
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def load_progress() -> set:
    if PROGRESS.exists():
        try:
            with open(PROGRESS) as f:
                data = json.load(f)
            return set(data.get('done', []))
        except Exception:
            pass
    return set()

def save_cache(cache: dict):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix('.json.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, separators=(',', ':'))
    tmp.replace(OUTPUT_FILE)

def save_progress(done: set):
    with open(PROGRESS, 'w') as f:
        json.dump({'done': sorted(done)}, f)


# ─── Process one chapter ───────────────────────────────────────────────────────
def process_chapter(book_id: int, chapter: int) -> dict:
    """
    Fetch all 11 translations for this chapter.
    Returns dict of {key: {trans: text, ...}} for all verses found.
    """
    # Fetch all translations sequentially (rate-limited)
    trans_data = {}
    for t in TRANSLATIONS:
        trans_data[t] = fetch_chapter(t, book_id, chapter)
        time.sleep(FETCH_DELAY)

    # Gather all verse numbers from NKJV (primary)
    nkjv_verses = set(trans_data.get('NKJV', {}).keys())
    if not nkjv_verses:
        return {}

    result = {}
    for vnum in sorted(nkjv_verses):
        key = f"{book_id}_{chapter}_{vnum}"
        verse_texts = {}
        for t in TRANSLATIONS:
            text = trans_data[t].get(vnum, '')
            if text:
                verse_texts[t] = text
        if verse_texts.get('NKJV'):  # only cache if we have NKJV
            result[key] = verse_texts

    return result


# ─── Quick Test Mode ──────────────────────────────────────────────────────────
def run_test():
    print("=" * 65)
    print("BTE v4.1 — TEST MODE: Genesis 1 + John 3")
    print("=" * 65)

    test_cases = [
        (1, 'Genesis', 1),
        (43, 'John', 3),
    ]

    total_verses = 0
    for book_id, book_name, chapter in test_cases:
        print(f"\n📖 Fetching {book_name} {chapter} (all {len(TRANSLATIONS)} translations)...")
        chap_data = process_chapter(book_id, chapter)
        verse_count = len(chap_data)
        total_verses += verse_count
        print(f"   ✓ {verse_count} verses cached")

    print(f"\n{'─'*65}")
    print(f"SAMPLE: John 3:16 in all translations")
    print(f"{'─'*65}")
    key = "43_3_16"
    # Re-fetch to show sample
    trans_data = {}
    for t in TRANSLATIONS:
        trans_data[t] = fetch_chapter(t, 43, 3)
        time.sleep(FETCH_DELAY)
    for t in TRANSLATIONS:
        text = trans_data[t].get(16, '[not found]')
        label = 'CSB' if t == 'CSB17' else ('NRSV' if t == 'NRSVCE' else t)
        print(f"  [{label:6s}] {text[:120]}")

    print(f"\n✅ Test complete — {total_verses} verses")


# ─── Full Run ─────────────────────────────────────────────────────────────────
def run_full(book_filter: int = None):
    print("=" * 65)
    print("BTE v4.1 — FULL VERSE CACHE: All 66 Books")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 65)

    cache   = load_cache()
    done    = load_progress()
    start   = time.time()

    print(f"Resuming: {len(cache):,} verses already cached, {len(done)} chapters done\n")

    books = [(bid, nm, nc) for bid, nm, nc in BIBLE_BOOKS
             if book_filter is None or bid == book_filter]

    total_chapters  = sum(nc for _, _, nc in books)
    chaps_processed = 0
    chaps_skipped   = 0
    new_verses      = 0
    save_counter    = 0
    book_idx        = 0

    for book_id, book_name, num_chapters in books:
        book_idx += 1
        book_new = 0
        print(f"\n{'━'*65}")
        print(f"[Book {book_id:2d}/66 — {book_name}]  ({num_chapters} chapters)")
        print(f"{'━'*65}")

        for chapter in range(1, num_chapters + 1):
            prog_key = f"{book_id}_{chapter}"

            if prog_key in done:
                chaps_skipped += 1
                chaps_processed += 1
                if chapter % 20 == 0:
                    print(f"  Ch {chapter:3d}/{num_chapters}: ✓ skip")
                continue

            chap_data = process_chapter(book_id, chapter)

            if not chap_data:
                print(f"  Ch {chapter:3d}/{num_chapters}: ⚠️  no data")
                done.add(prog_key)
                chaps_processed += 1
                continue

            # Merge into cache
            cache.update(chap_data)
            done.add(prog_key)

            v_count   = len(chap_data)
            book_new += v_count
            new_verses += v_count
            chaps_processed += 1
            save_counter += 1

            pct = chaps_processed / total_chapters * 100
            elapsed = time.time() - start
            eta_s   = (elapsed / chaps_processed) * (total_chapters - chaps_processed) if chaps_processed else 0
            eta_m   = eta_s / 60

            print(f"  Ch {chapter:3d}/{num_chapters}: {v_count:3d} verses | "
                  f"{pct:5.1f}% done | ETA {eta_m:.0f}m")

            if save_counter >= SAVE_EVERY:
                save_cache(cache)
                save_progress(done)
                save_counter = 0

        print(f"  ✓ {book_name} done: {book_new} new verses")

    # Final save
    save_cache(cache)
    save_progress(done)

    elapsed = time.time() - start
    sz_mb   = OUTPUT_FILE.stat().st_size / 1024 / 1024

    print("\n" + "=" * 65)
    print("✅ COMPLETE")
    print(f"   Total verses in cache : {len(cache):,}")
    print(f"   New verses this run   : {new_verses:,}")
    print(f"   Chapters processed    : {chaps_processed:,}")
    print(f"   Chapters skipped      : {chaps_skipped:,}")
    print(f"   File size             : {sz_mb:.1f} MB")
    print(f"   Time elapsed          : {elapsed/60:.1f} min")
    print("=" * 65)


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if '--test' in args:
        run_test()
    elif '--book' in args:
        idx = args.index('--book')
        bid = int(args[idx + 1])
        book_map = {b[0]: b for b in BIBLE_BOOKS}
        if bid not in book_map:
            print(f"Unknown book ID: {bid} (range 1-66)")
            sys.exit(1)
        run_full(book_filter=bid)
    else:
        run_full()
