#!/usr/bin/env python3
"""
MOOP Translation Generator — Batch: 1 Kings + 2 Kings + 1 Chronicles + 2 Chronicles
Takes NKJV as base and weaves in 1-2 clarifying words/phrases from ESV/NASB/NLT/CSB.
ONE natural voice — no brackets, no annotations.
"""

import json
import os
import time
import sys
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

CACHE_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json'
MOOP_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json'

SYSTEM_PROMPT = """You are a Bible translation blender creating the MOOP Translation.

RULES:
1. Start with the NKJV as the base text
2. Weave in 1-2 clarifying words or phrases from ESV, NASB, NLT, or CSB where they add clarity or meaning
3. The result must sound like ONE natural, unified English sentence — not a patchwork
4. NO brackets, NO annotations, NO source labels, NO commentary
5. Keep the reverent, literary tone of NKJV
6. Only improve clarity — don't change meaning or modernize unnecessarily
7. If NKJV is already perfectly clear, return it nearly unchanged

You will receive a JSON object with verse keys mapping to translation objects.
Return a JSON object with the SAME verse keys mapping to ONLY the blended text string.
Return ONLY valid JSON, no markdown, no explanation."""

def blend_batch(verses_dict):
    """Send a batch of verses to GPT-4o and return blended texts."""
    user_content = json.dumps(verses_dict, ensure_ascii=False)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Blend these verses:\n{user_content}"}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    result_text = response.choices[0].message.content
    return json.loads(result_text)

def load_files():
    with open(CACHE_PATH, 'r') as f:
        cache = json.load(f)
    with open(MOOP_PATH, 'r') as f:
        moop = json.load(f)
    return cache, moop

def save_moop(moop):
    with open(MOOP_PATH, 'w') as f:
        json.dump(moop, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  ✅ Saved moop-translation.json ({len(moop)} entries)")

def get_book_keys(cache, book_num):
    prefix = f"{book_num}_"
    keys = sorted([k for k in cache.keys() if k.startswith(prefix)],
                  key=lambda x: tuple(int(n) for n in x.split('_')))
    return keys

def process_book(cache, moop, book_num, book_name, batch_size=50):
    print(f"\n{'='*60}")
    print(f"Processing {book_name} (Book {book_num})")
    print(f"{'='*60}")
    
    all_keys = get_book_keys(cache, book_num)
    
    # Skip already-done keys
    todo_keys = [k for k in all_keys if k not in moop]
    already_done = len(all_keys) - len(todo_keys)
    
    print(f"Total verses: {len(all_keys)}")
    print(f"Already done: {already_done}")
    print(f"To process: {len(todo_keys)}")
    
    if not todo_keys:
        print(f"  ⚡ {book_name} already complete!")
        return
    
    # Process in batches
    total_batches = (len(todo_keys) + batch_size - 1) // batch_size
    processed = 0
    errors = 0
    
    for batch_idx in range(0, len(todo_keys), batch_size):
        batch_keys = todo_keys[batch_idx:batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1
        
        # Build input dict with only the translations we need
        verses_input = {}
        for key in batch_keys:
            entry = cache.get(key, {})
            verses_input[key] = {
                "NKJV": entry.get("NKJV", ""),
                "ESV": entry.get("ESV", ""),
                "NASB": entry.get("NASB", ""),
                "NLT": entry.get("NLT", ""),
                "CSB": entry.get("CSB17", entry.get("CSB", ""))
            }
        
        print(f"  Batch {batch_num}/{total_batches} ({len(batch_keys)} verses: {batch_keys[0]} → {batch_keys[-1]})...", end=' ', flush=True)
        
        retry_count = 0
        max_retries = 3
        success = False
        
        while retry_count < max_retries and not success:
            try:
                result = blend_batch(verses_input)
                
                # Validate and store results
                for key in batch_keys:
                    if key in result and isinstance(result[key], str) and result[key].strip():
                        moop[key] = result[key].strip()
                        processed += 1
                    else:
                        # Fallback to NKJV if key missing from response
                        fallback = cache[key].get("NKJV", "")
                        if fallback:
                            moop[key] = fallback
                            processed += 1
                        else:
                            errors += 1
                            print(f"\n  ⚠️  Missing key in response: {key}")
                
                print(f"✓ ({processed} total done)")
                success = True
                
            except json.JSONDecodeError as e:
                retry_count += 1
                print(f"\n  ⚠️  JSON decode error (attempt {retry_count}/{max_retries}): {e}")
                if retry_count < max_retries:
                    time.sleep(2)
                    
            except Exception as e:
                retry_count += 1
                err_str = str(e)
                print(f"\n  ⚠️  Error (attempt {retry_count}/{max_retries}): {err_str[:100]}")
                
                if "rate_limit" in err_str.lower() or "429" in err_str:
                    wait = 30 * retry_count
                    print(f"  ⏳ Rate limit hit, waiting {wait}s...")
                    time.sleep(wait)
                elif retry_count < max_retries:
                    time.sleep(5)
        
        if not success:
            # Final fallback: use NKJV for all keys in this batch
            print(f"\n  ❌ Batch {batch_num} failed after {max_retries} retries. Using NKJV fallback.")
            for key in batch_keys:
                if key not in moop:
                    moop[key] = cache[key].get("NKJV", "")
                    processed += 1
            errors += len(batch_keys)
        
        # Small delay between batches to be nice to the API
        if batch_idx + batch_size < len(todo_keys):
            time.sleep(0.5)
    
    print(f"\n  📖 {book_name} complete: {processed} verses processed, {errors} fallbacks used")
    save_moop(moop)

def main():
    print("MOOP Translation Generator — Kings & Chronicles")
    print("Using GPT-4o for translation blending")
    print()
    
    cache, moop = load_files()
    print(f"Cache loaded: {len(cache)} total verses")
    print(f"Moop loaded: {len(moop)} existing entries")
    
    books = [
        (11, "1 Kings"),
        (12, "2 Kings"),
        (13, "1 Chronicles"),
        (14, "2 Chronicles"),
    ]
    
    # Check command line args for specific book
    if len(sys.argv) > 1:
        book_filter = int(sys.argv[1])
        books = [(num, name) for num, name in books if num == book_filter]
        print(f"Filtering to book {book_filter}")
    
    start_time = time.time()
    
    for book_num, book_name in books:
        process_book(cache, moop, book_num, book_name, batch_size=50)
        print(f"\n⏱️  Time elapsed: {(time.time()-start_time)/60:.1f} minutes")
    
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🎉 ALL DONE!")
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Final moop-translation.json: {len(moop)} entries")
    
    # Final save
    save_moop(moop)

if __name__ == '__main__':
    main()
