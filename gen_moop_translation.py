#!/usr/bin/env python3
"""
MOOP Translation Generator
Creates a proprietary blended Bible rendering using Claude Sonnet.
Reads from verse-cache.json, outputs moop-translation.json

The MOOP Translation:
- Takes NKJV as the base text
- Weaves in 1-2 clarifying words/phrases from ESV/NASB/NLT where they add meaning
- Reads as ONE natural voice — not annotated, not fragmented
- Subtler than the Amplified Bible

Format: {"1_1_1": "blended verse text", ...}
"""
import json, os, time, requests, sys, re
from datetime import datetime

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
VERSE_CACHE = os.path.join(BASE, 'docs/assets/verse-cache.json')
OUTPUT = os.path.join(BASE, 'docs/assets/moop-translation.json')
PROGRESS = os.path.join(BASE, 'moop-translation-progress.json')
SCHEDULE = os.path.join(BASE, 'schedule.json')
READING_PLAN_KEYS = os.path.join(BASE, 'reading-plan-keys.json')

# Anthropic API key (from openclaw auth-profiles - usmcmin20max profile)
ANTHROPIC_KEY = 'REDACTED_API_KEY'

# Translation weights (display order for prompt)
TRANS_ORDER = ['NKJV', 'ESV', 'NASB', 'NLT', 'CSB17', 'KJV', 'WEB', 'AMP', 'MSG', 'NIV', 'NRSVCE']
TRANS_WEIGHT_LABELS = {
    'NKJV': '33%', 'ESV': '12%', 'NASB': '12%', 'NLT': '9%', 'CSB17': '10%',
    'KJV': '7%', 'WEB': '7%', 'AMP': '3%', 'MSG': '2%', 'NIV': '1%', 'NRSVCE': '4%'
}

# Book ID to name mapping (verse-cache.json uses numeric IDs 1-18 = Gen-Job)
BOOK_NAMES = {
    '1': 'Genesis', '2': 'Exodus', '3': 'Leviticus', '4': 'Numbers',
    '5': 'Deuteronomy', '6': 'Joshua', '7': 'Judges', '8': 'Ruth',
    '9': '1 Samuel', '10': '2 Samuel', '11': '1 Kings', '12': '2 Kings',
    '13': '1 Chronicles', '14': '2 Chronicles', '15': 'Ezra', '16': 'Nehemiah',
    '17': 'Esther', '18': 'Job'
}


def blend_verse(ref, translations):
    """Call Claude Sonnet to create the MOOP blended translation."""
    nkjv = translations.get('NKJV', '')
    if not nkjv:
        return None

    # Build translation lines (skip NKJV, include up to 5 others)
    trans_lines = []
    for t in TRANS_ORDER:
        if t != 'NKJV' and translations.get(t):
            label = TRANS_WEIGHT_LABELS.get(t, '')
            trans_lines.append(f"{t} ({label}): {translations[t]}")
        if len(trans_lines) >= 5:
            break

    prompt = f"""Create the MOOP Translation for this verse. Base: NKJV. Weave in 1-2 clarifying words from other translations where they add meaning. One natural sentence. No brackets, no annotations.

{ref}
NKJV: {nkjv}
{chr(10).join(trans_lines)}

Return ONLY the blended verse text."""

    headers = {
        'x-api-key': ANTHROPIC_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    body = {
        'model': 'claude-sonnet-4-5',
        'max_tokens': 250,
        'messages': [{'role': 'user', 'content': prompt}]
    }

    for attempt in range(3):
        try:
            resp = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=body,
                timeout=30
            )
            if resp.status_code == 529:  # overloaded
                time.sleep(5 * (attempt + 1))
                continue
            if resp.status_code == 429:  # rate limited
                time.sleep(10 * (attempt + 1))
                continue
            resp.raise_for_status()
            data = resp.json()
            return data['content'][0]['text'].strip()
        except Exception as e:
            print(f"  ⚠️  API error for {ref} (attempt {attempt+1}): {e}", file=sys.stderr, flush=True)
            if attempt < 2:
                time.sleep(3)
    return None


def load_output():
    if os.path.exists(OUTPUT):
        with open(OUTPUT) as f:
            return json.load(f)
    return {}


def save_output(data):
    with open(OUTPUT, 'w') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))


def get_human_ref(key):
    """Convert '1_3_16' to 'Genesis 3:16'"""
    parts = key.split('_')
    book_id, chapter, verse = parts[0], parts[1], parts[2]
    book_name = BOOK_NAMES.get(book_id, f'Book{book_id}')
    return f"{book_name} {chapter}:{verse}"


def test_verses(verse_cache, output):
    """Run test on 5 specific verses before full run."""
    # Key test verses — note: only books 1-18 available in cache
    # John 3:16 (book 43) and others are NT — not in cache yet
    # Use available OT verses instead
    test_keys = [
        ('18_1_1', 'Job 1:1'),       # Job opening
        ('18_3_3', 'Job 3:3'),       # Famous lament
        ('1_1_1', 'Genesis 1:1'),    # Creation
        ('1_1_3', 'Genesis 1:3'),    # Let there be light
        ('5_6_4', 'Deuteronomy 6:4'), # Shema
    ]

    print("\n" + "="*60)
    print("MOOP TRANSLATION — TEST RUN (5 verses)")
    print("="*60)

    for key, label in test_keys:
        if key not in verse_cache:
            print(f"\n--- {label} ---")
            print(f"  NOT IN CACHE")
            continue

        translations = verse_cache[key]
        nkjv = translations.get('NKJV', 'N/A')

        print(f"\n--- {label} ---")
        print(f"NKJV: {nkjv}")

        if key in output:
            print(f"MOOP: {output[key]} (cached)")
            continue

        moop = blend_verse(label, translations)
        if moop:
            output[key] = moop
            save_output(output)
            print(f"MOOP: {moop}")
        else:
            print(f"MOOP: [FAILED]")
        time.sleep(0.5)

    print("\n" + "="*60)
    print("Test run complete. Proceed to full run? (y/n): ", end='', flush=True)
    answer = input().strip().lower()
    return answer in ('y', 'yes', '')


def run_full(verse_cache, output, test_mode=False, plan_only=False):
    """Process all verses in the cache."""
    # Load reading plan filter if requested
    filter_keys = None
    if plan_only and os.path.exists(READING_PLAN_KEYS):
        with open(READING_PLAN_KEYS) as f:
            filter_keys = set(json.load(f))
        print(f"📋 Filtering to {len(filter_keys):,} reading plan verses")
    
    # Group by book+chapter
    by_chapter = {}
    for key in verse_cache:
        # Skip if not in reading plan (when filtering)
        if filter_keys and key not in filter_keys:
            continue
        
        parts = key.split('_')
        book_id, chapter = parts[0], parts[1]
        chapter_key = f"{book_id}_{chapter}"
        if chapter_key not in by_chapter:
            by_chapter[chapter_key] = []
        by_chapter[chapter_key].append(key)

    # Sort chapters: book 1 ch 1, book 1 ch 2, ..., book 18 ch 42
    sorted_chapters = sorted(by_chapter.keys(),
                             key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))

    total_verses = sum(len(v) for v in by_chapter.values())
    total_done = len(output)
    print(f"\n📖 Total verses in cache: {total_verses:,}")
    print(f"✅ Already blended: {total_done:,}")
    print(f"⏳ Remaining: {total_verses - total_done:,}")
    print(f"📚 Chapters to process: {len(sorted_chapters)}")
    print()

    chapter_count = 0
    new_this_run = 0
    errors = 0

    for chapter_key in sorted_chapters:
        verse_keys = sorted(by_chapter[chapter_key], key=lambda x: int(x.split('_')[2]))
        book_id, chapter = chapter_key.split('_')
        book_name = BOOK_NAMES.get(book_id, f'Book{book_id}')

        # Check if all verses in this chapter are already done
        already_done = sum(1 for k in verse_keys if k in output)
        if already_done == len(verse_keys):
            continue

        chapter_count += 1
        chapter_new = 0

        for key in verse_keys:
            if key in output:
                continue

            translations = verse_cache[key]
            ref = get_human_ref(key)
            moop = blend_verse(ref, translations)

            if moop:
                output[key] = moop
                chapter_new += 1
                new_this_run += 1
            else:
                errors += 1

            time.sleep(0.5)  # rate limit

        if chapter_new > 0:
            save_output(output)
            total_done = len(output)
            print(f"[{book_name} {chapter}] {chapter_new} verses blended (total: {total_done:,})")

        # Save progress file
        with open(PROGRESS, 'w') as f:
            json.dump({
                'last_chapter': chapter_key,
                'total_blended': len(output),
                'timestamp': datetime.now().isoformat()
            }, f)

        if test_mode and chapter_count >= 2:
            print("\n[TEST MODE] Stopping after 2 chapters.")
            break

    print(f"\n✅ Done! {new_this_run:,} new verses blended.")
    print(f"⚠️  Errors: {errors}")
    print(f"📄 Output: {OUTPUT}")
    size = os.path.getsize(OUTPUT) if os.path.exists(OUTPUT) else 0
    print(f"📦 File size: {size/1024:.1f} KB")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='MOOP Translation Generator')
    parser.add_argument('--test', action='store_true', help='Test 5 verses only')
    parser.add_argument('--full', action='store_true', help='Run full generation (no confirm)')
    parser.add_argument('--plan-only', action='store_true', help='Only process reading plan verses')
    parser.add_argument('--chapter-test', action='store_true', help='Run 2 chapters then stop')
    args = parser.parse_args()

    # Force unbuffered output
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    print("📖 MOOP Translation Generator")
    print(f"📂 Cache: {VERSE_CACHE}")
    print(f"📤 Output: {OUTPUT}")

    # Load verse cache
    print("\nLoading verse cache...", end='', flush=True)
    with open(VERSE_CACHE) as f:
        verse_cache = json.load(f)
    print(f" {len(verse_cache):,} verses loaded")

    # Load existing output
    output = load_output()
    print(f"Existing MOOP verses: {len(output):,}")

    if args.test:
        test_verses(verse_cache, output)
        return

    if args.chapter_test:
        run_full(verse_cache, output, test_mode=True, plan_only=args.plan_only)
        return

    if args.full:
        run_full(verse_cache, output, plan_only=args.plan_only)
    else:
        # Interactive: test 5 verses first, then ask
        proceed = test_verses(verse_cache, output)
        if proceed:
            run_full(verse_cache, output, plan_only=args.plan_only)
        else:
            print("Stopped. Run with --full to skip confirmation.")


if __name__ == '__main__':
    main()
