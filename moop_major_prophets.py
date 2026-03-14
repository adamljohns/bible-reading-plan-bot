#!/usr/bin/env python3
"""
MOOP Translation Generator - Major Prophets
Books 23-27: Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel

Uses OpenAI gpt-4.1 to blend NKJV with ESV/NASB/NLT/CSB clarifications.
Rate-limited batch processing. Saves after each book.
"""

import json
import re
import time
import sys
import os
import subprocess

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
VERSE_CACHE_PATH = "/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json"
MOOP_PATH = "/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json"

BOOKS = {
    23: "Isaiah",
    24: "Jeremiah",
    25: "Lamentations",
    26: "Ezekiel",
    27: "Daniel",
}

BATCH_SIZE = 10       # 10 verses per API call — ~3500 tokens per batch
BATCH_PAUSE = 10.0   # seconds between successful batches
MODEL = "gpt-4.1"

SYSTEM_PROMPT = """You are generating the MOOP Translation — a blended English Bible translation.
Base: NKJV. Weave in 1-2 clarifying words/phrases from ESV, NASB, or NLT where they genuinely sharpen meaning.

Rules:
- ONE unified natural voice. No brackets, no annotations, no explanations.
- Remove all HTML tags (keep words, drop tags).
- Preserve prophetic weight, urgency, and oracular tone.
- Keep poetic line breaks where they exist.
- Output only the verse text.

Input: JSON array of verse objects.
Output: JSON array of blended verse strings, same order, same count.
Return ONLY the JSON array — no markdown fences, no preamble."""


def clean_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()


class RateLimitError(Exception):
    def __init__(self, wait_sec):
        self.wait_sec = wait_sec


def call_api_batch(verses_data):
    """Call OpenAI API. Returns list of blended strings."""
    payload = {
        "model": MODEL,
        "max_tokens": 2048,
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT + "\n\nWrap your array in: {\"verses\": [...]}"},
            {
                "role": "user",
                "content": f"Blend {len(verses_data)} verses. Return {{\"verses\": [array of {len(verses_data)} strings]}}.\n\n{json.dumps(verses_data, ensure_ascii=False)}"
            }
        ]
    }

    result = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://api.openai.com/v1/chat/completions",
         "-H", f"Authorization: Bearer {OPENAI_API_KEY}",
         "-H", "Content-Type: application/json",
         "--data-binary", "@-"],
        input=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        capture_output=True,
        timeout=120
    )

    if result.returncode != 0:
        raise Exception(f"curl failed: {result.stderr.decode()[:200]}")

    response = json.loads(result.stdout.decode('utf-8'))

    if 'error' in response:
        err = response['error']
        if err.get('code') == 'rate_limit_exceeded':
            msg = err.get('message', '')
            match = re.search(r'try again in (\d+\.?\d*)(ms|s)', msg)
            if match:
                val = float(match.group(1))
                wait = (val / 1000.0 if match.group(2) == 'ms' else val) + 3.0
            else:
                wait = 30.0
            raise RateLimitError(wait)
        raise Exception(f"API error: {err}")

    content = response['choices'][0]['message']['content']
    parsed = json.loads(content)

    if isinstance(parsed, dict) and 'verses' in parsed:
        return parsed['verses']
    elif isinstance(parsed, list):
        return parsed
    else:
        raise ValueError(f"Unexpected response format: {str(parsed)[:200]}")


def process_book(book_num, book_name, cache, moop):
    """Process all verses in a book."""
    print(f"\n{'='*60}", flush=True)
    print(f"Processing {book_name} (Book {book_num})", flush=True)
    print(f"{'='*60}", flush=True)

    book_keys = sorted(
        [k for k in cache.keys() if k.startswith(str(book_num) + '_')],
        key=lambda k: tuple(int(x) for x in k.split('_'))
    )

    to_process = [k for k in book_keys if k not in moop]

    total_batches = (len(to_process) + BATCH_SIZE - 1) // BATCH_SIZE
    est_mins = total_batches * (BATCH_PAUSE + 4) / 60
    print(f"Total: {len(book_keys)} | To process: {len(to_process)} | Batches: {total_batches} | Est: {est_mins:.0f}min", flush=True)

    if not to_process:
        print(f"All {book_name} verses already done!", flush=True)
        return 0

    processed = 0
    fallbacks = 0

    for batch_start in range(0, len(to_process), BATCH_SIZE):
        batch_keys = to_process[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1

        verses_data = []
        for key in batch_keys:
            entry = cache[key]
            parts = key.split('_')
            verses_data.append({
                "ref": f"{book_name} {parts[1]}:{parts[2]}",
                "NKJV": clean_html(entry.get('NKJV', '')),
                "ESV": clean_html(entry.get('ESV', '')),
                "NLT": clean_html(entry.get('NLT', '')),
                "NASB": clean_html(entry.get('NASB', ''))
            })

        success = False
        for attempt in range(6):
            try:
                blended = call_api_batch(verses_data)

                for i, key in enumerate(batch_keys):
                    if i < len(blended) and blended[i]:
                        moop[key] = blended[i]
                        processed += 1
                    else:
                        moop[key] = clean_html(cache[key].get('NKJV', ''))
                        fallbacks += 1

                p = batch_keys[-1].split('_')
                pct = (batch_start + len(batch_keys)) / len(to_process) * 100
                print(f"  ✓ [{batch_num}/{total_batches}] {book_name} {p[1]}:{p[2]} — {pct:.0f}% ({processed} done)", flush=True)
                success = True
                break

            except RateLimitError as e:
                print(f"  ⏳ Rate limit, waiting {e.wait_sec:.1f}s...", flush=True)
                time.sleep(e.wait_sec)

            except Exception as e:
                wait = min(60, 15 * (2 ** attempt))
                print(f"  ✗ Attempt {attempt+1}: {str(e)[:100]} | wait {wait}s", flush=True)
                time.sleep(wait)

        if not success:
            print(f"  ✗ BATCH FAILED — using NKJV fallback for {len(batch_keys)} verses", flush=True)
            for key in batch_keys:
                moop[key] = clean_html(cache[key].get('NKJV', ''))
                fallbacks += 1

        time.sleep(BATCH_PAUSE)

    print(f"\n{book_name}: {processed} blended, {fallbacks} NKJV fallbacks", flush=True)
    return processed


def save_moop(moop):
    with open(MOOP_PATH, 'w', encoding='utf-8') as f:
        json.dump(moop, f, ensure_ascii=False, indent=2)
    mb = os.path.getsize(MOOP_PATH) / 1024 / 1024
    print(f"  💾 Saved: {len(moop)} entries ({mb:.1f} MB)", flush=True)


def main():
    print("MOOP Translation Generator — Major Prophets", flush=True)
    print(f"Model: {MODEL} | Batch: {BATCH_SIZE} | Pause: {BATCH_PAUSE}s", flush=True)

    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set!", flush=True)
        sys.exit(1)

    print("Loading data...", flush=True)
    with open(VERSE_CACHE_PATH, encoding='utf-8') as f:
        cache = json.load(f)
    with open(MOOP_PATH, encoding='utf-8') as f:
        moop = json.load(f)

    print(f"Cache: {len(cache)} | MOOP existing: {len(moop)}", flush=True)

    total_new = sum(
        len([k for k in cache if k.startswith(str(b) + '_') and k not in moop])
        for b in BOOKS
    )
    est_batches = (total_new + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Total new verses: {total_new} | ~{est_batches} batches | ~{est_batches*(BATCH_PAUSE+4)/60:.0f} min total", flush=True)

    total_processed = 0

    for book_num, book_name in BOOKS.items():
        count = process_book(book_num, book_name, cache, moop)
        total_processed += count

        print(f"\nSaving after {book_name}...", flush=True)
        save_moop(moop)

    print(f"\n{'='*60}", flush=True)
    print(f"MAJOR PROPHETS COMPLETE!", flush=True)
    print(f"New: {total_processed} | Total MOOP: {len(moop)}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == '__main__':
    main()
