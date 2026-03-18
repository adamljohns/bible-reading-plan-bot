#!/usr/bin/env python3
"""
BTE Static Chapter Cache Builder
Pre-fetches Bible chapters from bolls.life API and saves as static JSON files.
Each file: docs/assets/chapters/{bookId}_{chapter}.json
Format: {"NKJV": {"1": "text", "2": "text"...}, "KJV": {...}, ...}
"""

import asyncio
import aiohttp
import ssl
import json
import os
import time
from pathlib import Path

# Output directory
OUTPUT_DIR = Path('/Users/adamjohns/bible-reading-plan-bot/docs/assets/chapters')

# 12 translations to cache
TRANSLATIONS = ['NKJV', 'KJV', 'ESV', 'NASB', 'NLT', 'WEB', 'CSB17', 'AMP', 'MSG', 'NIV', 'NRSVCE', 'NET']

# Books to cache: {bookId: num_chapters}
# Priority: NT (40-66), Psalms (19), Proverbs (20)
BOOKS = {
    # NT - Matthew through Revelation
    40: 28,  # Matthew
    41: 16,  # Mark
    42: 24,  # Luke
    43: 21,  # John
    44: 28,  # Acts
    45: 16,  # Romans
    46: 16,  # 1 Corinthians
    47: 13,  # 2 Corinthians
    48: 6,   # Galatians
    49: 6,   # Ephesians
    50: 4,   # Philippians
    51: 4,   # Colossians
    52: 5,   # 1 Thessalonians
    53: 3,   # 2 Thessalonians
    54: 6,   # 1 Timothy
    55: 4,   # 2 Timothy
    56: 3,   # Titus
    57: 1,   # Philemon
    58: 13,  # Hebrews
    59: 5,   # James
    60: 5,   # 1 Peter
    61: 3,   # 2 Peter
    62: 5,   # 1 John
    63: 1,   # 2 John
    64: 1,   # 3 John
    65: 1,   # Jude
    66: 22,  # Revelation
    # Psalms + Proverbs
    19: 150, # Psalms
    20: 31,  # Proverbs
}

BASE_URL = 'https://bolls.life/get-chapter'

# Semaphore to limit concurrent requests (be respectful)
CONCURRENCY = 4  # max simultaneous requests
DELAY_BETWEEN_CHAPTERS = 0.5  # seconds between chapter batches


async def fetch_translation(session, semaphore, book_id, chapter, translation):
    """Fetch one translation for one chapter."""
    url = f"{BASE_URL}/{translation}/{book_id}/{chapter}/"
    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30), ssl=False) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        return translation, {str(v['verse']): v.get('text', '') for v in data}
                    return translation, None
                else:
                    print(f"  ⚠️  {translation} {book_id}:{chapter} → HTTP {resp.status}")
                    return translation, None
        except Exception as e:
            print(f"  ❌  {translation} {book_id}:{chapter} → {e}")
            return translation, None


async def fetch_chapter(session, semaphore, book_id, chapter):
    """Fetch all 12 translations for one chapter concurrently."""
    tasks = [
        fetch_translation(session, semaphore, book_id, chapter, trans)
        for trans in TRANSLATIONS
    ]
    results = await asyncio.gather(*tasks)
    combined = {}
    for trans, data in results:
        if data:
            combined[trans] = data
    return combined


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Build full list of (book_id, chapter) pairs
    all_chapters = []
    for book_id in sorted(BOOKS.keys()):
        num_chapters = BOOKS[book_id]
        for ch in range(1, num_chapters + 1):
            all_chapters.append((book_id, ch))
    
    total = len(all_chapters)
    print(f"📖 BTE Chapter Cache Builder")
    print(f"   Books: {len(BOOKS)} | Chapters: {total} | Translations: {len(TRANSLATIONS)}")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Estimated time: ~{total * DELAY_BETWEEN_CHAPTERS / 60:.1f} minutes")
    print()

    # Skip already-cached chapters
    to_fetch = []
    skipped = 0
    for book_id, ch in all_chapters:
        out_path = OUTPUT_DIR / f"{book_id}_{ch}.json"
        if out_path.exists():
            skipped += 1
        else:
            to_fetch.append((book_id, ch))
    
    if skipped:
        print(f"   ⏭️  Skipping {skipped} already-cached chapters")
    
    if not to_fetch:
        print("✅ All chapters already cached!")
        return

    print(f"   Fetching {len(to_fetch)} chapters...\n")

    semaphore = asyncio.Semaphore(CONCURRENCY)
    completed = 0
    start_time = time.time()

    # Create SSL context that doesn't verify certs (bolls.life cert chain issue on macOS)
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_ctx)
    async with aiohttp.ClientSession(connector=connector) as session:
        for book_id, ch in to_fetch:
            out_path = OUTPUT_DIR / f"{book_id}_{ch}.json"
            
            combined = await fetch_chapter(session, semaphore, book_id, ch)
            
            if combined:
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(combined, f, ensure_ascii=False)
            else:
                print(f"  ⚠️  No data for book {book_id} ch {ch}")
            
            completed += 1
            
            # Log progress every 10 chapters
            if completed % 10 == 0 or completed == len(to_fetch):
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                remaining = (len(to_fetch) - completed) / rate if rate > 0 else 0
                trans_count = len(combined) if combined else 0
                print(f"  ✓ {completed}/{len(to_fetch)} chapters — book {book_id} ch {ch} "
                      f"({trans_count} translations) | "
                      f"⏱ {elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining")
            
            # Rate limiting: pause between chapters
            if completed < len(to_fetch):
                await asyncio.sleep(DELAY_BETWEEN_CHAPTERS)

    elapsed = time.time() - start_time
    cached_count = sum(1 for (b, c) in all_chapters if (OUTPUT_DIR / f"{b}_{c}.json").exists())
    print(f"\n✅ Done! {cached_count}/{total} chapters cached in {elapsed:.0f}s")
    print(f"   Output: {OUTPUT_DIR}")


if __name__ == '__main__':
    asyncio.run(main())
