#!/usr/bin/env python3
"""
BTE v4.0 — Pre-generate blended parallels for all 66 books of the Bible
=======================================================================
Batch mode: one Haiku call per chapter (blends all verses at once).
Fully resumable: skips chapters already completed in blended-parallels.json.

Usage:
  python3 gen_blended_parallels.py           # Full run (all 66 books)
  python3 gen_blended_parallels.py --test    # Test 5 specific verses only
  python3 gen_blended_parallels.py --book 43 # Single book (John = 43)
"""

import json
import os
import re
import sys
import time
import threading
import urllib.request
import urllib.error
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ─── Config ────────────────────────────────────────────────────────────────────
REPO_DIR     = Path("/Users/adamjohns/bible-reading-plan-bot")
OUTPUT_FILE  = REPO_DIR / "docs/assets/blended-parallels.json"
LOG_FILE     = REPO_DIR / "docs/assets/blended-parallels-log.json"

ANTHROPIC_KEY = "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"
CLAUDE_MODEL  = "claude-haiku-4-5-20251001"

FETCH_WORKERS  = 10   # concurrent bolls.life requests
BLEND_WORKERS  = 3    # concurrent Haiku calls
FETCH_DELAY    = 0.1  # seconds between fetch batches
SAVE_INTERVAL  = 5    # save output every N chapters
BATCH_SIZE     = 45   # max verses per Haiku call (split long chapters)

# Translations: (id, weight, display_pct)
TRANSLATIONS = [
    ("NKJV",   0.33),
    ("ESV",    0.12),
    ("NASB",   0.12),
    ("CSB17",  0.10),
    ("NLT",    0.09),
    ("KJV",    0.07),
    ("WEB",    0.07),
    ("NRSVCE", 0.04),  # NRSV → NRSVCE (works on bolls.life)
    ("AMP",    0.03),
    ("MSG",    0.02),
    ("NIV",    0.01),
]

# ─── Complete Bible structure: book_id → (name, num_chapters) ──────────────────
BIBLE_BOOKS = {
    # Old Testament
     1: ("Genesis",         50),
     2: ("Exodus",          40),
     3: ("Leviticus",       27),
     4: ("Numbers",         36),
     5: ("Deuteronomy",     34),
     6: ("Joshua",          24),
     7: ("Judges",          21),
     8: ("Ruth",             4),
     9: ("1 Samuel",        31),
    10: ("2 Samuel",        24),
    11: ("1 Kings",         22),
    12: ("2 Kings",         25),
    13: ("1 Chronicles",    29),
    14: ("2 Chronicles",    36),
    15: ("Ezra",            10),
    16: ("Nehemiah",        13),
    17: ("Esther",          10),
    18: ("Job",             42),
    19: ("Psalms",         150),
    20: ("Proverbs",        31),
    21: ("Ecclesiastes",    12),
    22: ("Song of Solomon",  8),
    23: ("Isaiah",          66),
    24: ("Jeremiah",        52),
    25: ("Lamentations",     5),
    26: ("Ezekiel",         48),
    27: ("Daniel",          12),
    28: ("Hosea",           14),
    29: ("Joel",             3),
    30: ("Amos",             9),
    31: ("Obadiah",          1),
    32: ("Jonah",            4),
    33: ("Micah",            7),
    34: ("Nahum",            3),
    35: ("Habakkuk",         3),
    36: ("Zephaniah",        3),
    37: ("Haggai",           2),
    38: ("Zechariah",       14),
    39: ("Malachi",          4),
    # New Testament
    40: ("Matthew",         28),
    41: ("Mark",            16),
    42: ("Luke",            24),
    43: ("John",            21),
    44: ("Acts",            28),
    45: ("Romans",          16),
    46: ("1 Corinthians",   16),
    47: ("2 Corinthians",   13),
    48: ("Galatians",        6),
    49: ("Ephesians",        6),
    50: ("Philippians",      4),
    51: ("Colossians",       4),
    52: ("1 Thessalonians",  5),
    53: ("2 Thessalonians",  3),
    54: ("1 Timothy",        6),
    55: ("2 Timothy",        4),
    56: ("Titus",            3),
    57: ("Philemon",         1),
    58: ("Hebrews",         13),
    59: ("James",            5),
    60: ("1 Peter",          5),
    61: ("2 Peter",          3),
    62: ("1 John",           5),
    63: ("2 John",           1),
    64: ("3 John",           1),
    65: ("Jude",             1),
    66: ("Revelation",      22),
}

TOTAL_CHAPTERS = sum(v[1] for v in BIBLE_BOOKS.values())  # 1,189

# ─── HTTP Session ──────────────────────────────────────────────────────────────

def make_session() -> requests.Session:
    """Create a requests session with retry logic."""
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": "BTE/4.0"})
    return s

# Thread-local session for bolls.life fetches
_thread_local = threading.local()

def get_session() -> requests.Session:
    if not hasattr(_thread_local, 'session'):
        _thread_local.session = make_session()
    return _thread_local.session

# Shared session for Anthropic calls (used with lock)
_anthropic_session = make_session()
_anthropic_lock = threading.Lock()


# ─── Helpers ───────────────────────────────────────────────────────────────────

_HTML_TAG_RE   = re.compile(r'<[^>]+>')
_FOOTNOTE_RE   = re.compile(r'\[[\d,\s]+\]')
_STRONGS_RE    = re.compile(r'<S>\d+</S>')
_BRACKETS_RE   = re.compile(r'\s{2,}')

def clean_text(text: str) -> str:
    """Strip HTML tags, Strong's numbers, footnote markers from verse text."""
    text = _STRONGS_RE.sub('', text)
    text = _HTML_TAG_RE.sub('', text)
    text = _FOOTNOTE_RE.sub('', text)
    text = _BRACKETS_RE.sub(' ', text)
    return text.strip()


def fetch_chapter(translation: str, book_id: int, chapter: int) -> dict:
    """Fetch all verses of a chapter from bolls.life. Returns {verse_num: text}."""
    url = f"https://bolls.life/get-chapter/{translation}/{book_id}/{chapter}/"
    try:
        resp = get_session().get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            result = {}
            for v in data:
                t = clean_text(v.get('text', ''))
                if t and t.lower() not in ('', 'the verse is not found'):
                    result[int(v['verse'])] = t
            return result
    except Exception:
        pass
    return {}


def fetch_all_translations(book_id: int, chapter: int) -> dict:
    """
    Fetch chapter from all 11 translations concurrently.
    Returns {verse_num: {trans_id: text, ...}, ...}
    """
    results_by_trans = {}
    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
        futures = {
            pool.submit(fetch_chapter, trans, book_id, chapter): trans
            for trans, _ in TRANSLATIONS
        }
        for fut in as_completed(futures):
            trans = futures[fut]
            try:
                results_by_trans[trans] = fut.result()
            except Exception:
                results_by_trans[trans] = {}

    # Pivot: verse_num → {trans: text}
    all_verses = set()
    for verses in results_by_trans.values():
        all_verses.update(verses.keys())

    verse_data = {}
    for vnum in sorted(all_verses):
        trans_texts = {}
        for trans, _ in TRANSLATIONS:
            t = results_by_trans.get(trans, {}).get(vnum, '')
            if t:
                trans_texts[trans] = t
        if len(trans_texts) >= 3:   # need at least 3 translations to blend
            verse_data[vnum] = trans_texts

    return verse_data


def build_blend_prompt(book_name: str, chapter: int, verse_data: dict,
                       verse_nums: list) -> str:
    """Build compact prompt for blending a set of verses."""
    lines = []
    for vnum in verse_nums:
        trans = verse_data[vnum]
        parts = []
        for tname, weight in TRANSLATIONS:
            if tname in trans:
                pct = int(round(weight * 100))
                parts.append(f"{tname}({pct}%): {trans[tname]}")
        if parts:
            lines.append(f"V{vnum}: " + " | ".join(parts))

    if not lines:
        return ""

    prompt = (
        f"Blend each verse from multiple Bible translations into ONE unified text per verse.\n"
        f"Book: {book_name}, Chapter: {chapter}\n"
        f"Weights: NKJV 33%, ESV 12%, NASB 12%, CSB17 10%, NLT 9%, KJV 7%, WEB 7%, "
        f"NRSVCE 4%, AMP 3%, MSG 2%, NIV 1%\n"
        f"Rules: Natural single voice, faithful to meaning, higher-weight translations "
        f"influence more, result meaningfully richer than NKJV alone.\n\n"
        f"Return ONLY valid JSON: {{\"1\": \"blended text\", \"2\": \"blended text\", ...}}\n\n"
        f"Verses:\n"
        + "\n".join(lines)
    )
    return prompt


def call_haiku(prompt: str, retries: int = 3) -> dict:
    """Call Claude Haiku to blend verses. Returns parsed dict or {}."""
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    for attempt in range(retries):
        try:
            with _anthropic_lock:
                resp = _anthropic_session.post(
                    "https://api.anthropic.com/v1/messages",
                    json=payload,
                    headers=headers,
                    timeout=120
                )
            if resp.status_code == 529 or (resp.status_code == 200 and 'overloaded' in resp.text.lower()):
                wait = 15 * (attempt + 1)
                print(f"    [overloaded] waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"    [rate limit] waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            result = resp.json()
            text = result['content'][0]['text'].strip()
            # Extract JSON block
            m = re.search(r'\{.*\}', text, re.DOTALL)
            if m:
                return json.loads(m.group())
        except requests.exceptions.RequestException as e:
            print(f"    [HTTP error] {e}")
            if attempt < retries - 1:
                time.sleep(5)
        except Exception as e:
            print(f"    [error] {e}")
            if attempt < retries - 1:
                time.sleep(5)
    return {}


def blend_chapter(book_id: int, chapter: int, book_name: str,
                  verse_data: dict, existing: dict) -> dict:
    """
    Blend all verses in a chapter. Skips verses already in existing.
    Returns {key: blended_text} for new verses only.
    """
    # Filter to verses not yet done
    todo_verses = [
        v for v in sorted(verse_data.keys())
        if f"{book_id}_{chapter}_{v}" not in existing
    ]
    if not todo_verses:
        return {}

    new_results = {}

    # Split into batches if chapter is very long
    for batch_start in range(0, len(todo_verses), BATCH_SIZE):
        batch = todo_verses[batch_start:batch_start + BATCH_SIZE]
        prompt = build_blend_prompt(book_name, chapter, verse_data, batch)
        if not prompt:
            continue

        blended = call_haiku(prompt)
        if not blended:
            print(f"    WARNING: no blend returned for {book_name} {chapter} batch {batch_start//BATCH_SIZE+1}")
            continue

        for vnum in batch:
            key = f"{book_id}_{chapter}_{vnum}"
            str_vnum = str(vnum)
            if str_vnum in blended and blended[str_vnum]:
                new_results[key] = blended[str_vnum]

        if batch_start + BATCH_SIZE < len(todo_verses):
            time.sleep(0.5)  # brief pause between batches

    return new_results


# ─── Save / load ───────────────────────────────────────────────────────────────
_save_lock = threading.Lock()

def load_existing() -> dict:
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_results(data: dict):
    with _save_lock:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix('.json.tmp')
        with open(tmp, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=None, separators=(',', ':'))
        tmp.replace(OUTPUT_FILE)


# ─── Test mode ─────────────────────────────────────────────────────────────────
TEST_VERSES = [
    (43,  3, 16, "John",      "John 3:16"),
    (19, 23,  1, "Psalms",    "Psalm 23:1"),
    (49,  6, 10, "Ephesians", "Ephesians 6:10"),
    (45,  8,  1, "Romans",    "Romans 8:1"),
    ( 1,  1,  1, "Genesis",   "Genesis 1:1"),
]

def run_test():
    print("=" * 60)
    print("BTE v4.0 — TEST MODE (5 verses)")
    print("=" * 60)
    existing = load_existing()

    for book_id, chapter, verse, book_name, label in TEST_VERSES:
        print(f"\n{'─'*50}")
        print(f"Testing: {label}")
        print(f"{'─'*50}")

        # Fetch this one chapter's translations
        verse_data = fetch_all_translations(book_id, chapter)
        if verse not in verse_data:
            print(f"  ERROR: verse {verse} not found in chapter data")
            print(f"  Available verses: {sorted(verse_data.keys())[:10]}")
            continue

        trans = verse_data[verse]
        print(f"  Translations received: {len(trans)} — {list(trans.keys())}")

        # Blend just this verse
        prompt = build_blend_prompt(book_name, chapter, {verse: trans}, [verse])
        blended = call_haiku(prompt)

        if blended and str(verse) in blended:
            result_text = blended[str(verse)]
            print(f"\n  📖 BLENDED: {result_text}")
            print(f"\n  NKJV ref:  {trans.get('NKJV', '[not found]')[:120]}")
        else:
            print(f"  ERROR: Haiku returned nothing. Raw: {blended}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


# ─── Full run ───────────────────────────────────────────────────────────────────
def run_full(book_filter: int = None):
    print("=" * 60)
    print("BTE v4.0 — FULL RUN: All 66 Books of the Bible")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)

    existing = load_existing()
    print(f"Resuming from {len(existing):,} previously blended verses\n")

    stats = {
        "chapters_done": 0,
        "chapters_skipped": 0,
        "verses_blended": 0,
        "verses_skipped": len(existing),
        "errors": [],
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    books_to_process = (
        [(book_filter, BIBLE_BOOKS[book_filter])]
        if book_filter
        else list(BIBLE_BOOKS.items())
    )

    total_chapters = sum(n for _, (_, n) in books_to_process)
    chapters_processed = 0
    save_counter = 0

    for book_id, (book_name, num_chapters) in books_to_process:
        print(f"\n{'━'*60}")
        print(f"📖 Book {book_id}/66: {book_name} ({num_chapters} chapters)")
        print(f"{'━'*60}")

        book_new = 0
        book_start = time.time()

        for ch in range(1, num_chapters + 1):
            ch_key_prefix = f"{book_id}_{ch}_"
            already_done = sum(1 for k in existing if k.startswith(ch_key_prefix))

            # Fetch chapter data from all translations
            verse_data = fetch_all_translations(book_id, ch)
            total_in_ch = len(verse_data)

            if total_in_ch == 0:
                print(f"  Ch {ch:3d}: no verse data — skipping")
                stats["chapters_skipped"] += 1
                chapters_processed += 1
                continue

            if already_done >= total_in_ch:
                stats["chapters_skipped"] += 1
                chapters_processed += 1
                if ch % 10 == 0:
                    print(f"  Ch {ch:3d}/{num_chapters}: ✓ already done ({total_in_ch}v)")
                continue

            # Blend remaining verses
            new_verses = blend_chapter(book_id, ch, book_name, verse_data, existing)
            existing.update(new_verses)

            book_new += len(new_verses)
            stats["verses_blended"] += len(new_verses)
            stats["chapters_done"] += 1
            chapters_processed += 1
            save_counter += 1

            pct = (chapters_processed / total_chapters) * 100
            print(f"  Ch {ch:3d}/{num_chapters}: {len(new_verses):3d} new / "
                  f"{total_in_ch:3d} total  [{pct:5.1f}% overall]")

            # Save periodically
            if save_counter >= SAVE_INTERVAL:
                save_results(existing)
                save_counter = 0

            time.sleep(FETCH_DELAY)

        elapsed = time.time() - book_start
        print(f"  ✓ {book_name} done: {book_new} new verses in {elapsed:.0f}s")

    # Final save
    save_results(existing)

    stats["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    stats["total_verses"] = len(existing)

    # Save log
    with open(LOG_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

    print("\n" + "=" * 60)
    print("✅ COMPLETE")
    print(f"   Total verses in file : {len(existing):,}")
    print(f"   New verses blended   : {stats['verses_blended']:,}")
    print(f"   Chapters processed   : {stats['chapters_done']:,}")
    print(f"   Chapters skipped     : {stats['chapters_skipped']:,}")
    sz = OUTPUT_FILE.stat().st_size / 1024 / 1024
    print(f"   File size            : {sz:.1f} MB")
    print("=" * 60)


# ─── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if "--test" in args:
        run_test()
    elif "--book" in args:
        idx = args.index("--book")
        book_id = int(args[idx + 1])
        if book_id not in BIBLE_BOOKS:
            print(f"Unknown book ID: {book_id}. Range: 1-66")
            sys.exit(1)
        run_full(book_filter=book_id)
    else:
        run_full()
