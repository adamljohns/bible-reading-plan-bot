#!/usr/bin/env python3
"""
MOOP Translation Generator - Psalms + Proverbs
Blends NKJV base with ESV/NASB/NLT/CSB clarifications into one natural voice.
"""

import json
import re
import os
import time
import sys
from openai import OpenAI

# Config
VERSE_CACHE = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json'
MOOP_FILE = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json'
BATCH_SIZE = 40  # verses per API call
BOOKS = [
    (19, 'Psalms'),
    (20, 'Proverbs'),
]

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def strip_html(text):
    """Remove HTML tags and clean up whitespace."""
    if not text:
        return ''
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove Strong's numbers like <S>835</S> (already stripped above)
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_batch_prompt(verses_batch):
    """Build prompt for a batch of verses."""
    lines = []
    for key, data in verses_batch:
        nkjv = strip_html(data.get('NKJV', ''))
        esv = strip_html(data.get('ESV', ''))
        nasb = strip_html(data.get('NASB', ''))
        nlt = strip_html(data.get('NLT', ''))
        csb = strip_html(data.get('CSB17', ''))
        lines.append(f"""KEY: {key}
NKJV: {nkjv}
ESV: {esv}
NASB: {nasb}
NLT: {nlt}
CSB: {csb}""")
    
    verses_text = '\n\n'.join(lines)
    
    prompt = f"""You are generating the MOOP Translation — a blended Bible text for Psalms and Proverbs.

RULES:
1. Use NKJV as the base text
2. Weave in 1-2 clarifying words/phrases from ESV/NASB/NLT/CSB ONLY where they genuinely add meaning or clarity
3. ONE natural, flowing voice — no brackets, no footnotes, no annotations, no "OR" variants
4. PRESERVE poetic beauty and rhythm — these are poetry books
5. Keep NKJV's majesty and elevated diction
6. Strip ALL italics markers and formatting artifacts — clean, pure text
7. Do NOT add anything not in the source texts

For each KEY, output EXACTLY one line in this format:
KEY: <verse_key> | MOOP: <blended verse text>

Verses to process:

{verses_text}

Output (one line per verse, KEY: xxx | MOOP: blended text):"""
    
    return prompt

def process_batch(verses_batch, retries=3):
    """Send a batch to OpenAI and parse results."""
    prompt = build_batch_prompt(verses_batch)
    
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a Bible scholar blending translations. Output exactly as instructed — one line per verse in KEY: xxx | MOOP: text format. No other commentary.'
                    },
                    {'role': 'user', 'content': prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
            )
            
            raw = response.choices[0].message.content.strip()
            results = {}
            
            for line in raw.split('\n'):
                line = line.strip()
                if line.startswith('KEY:') and '| MOOP:' in line:
                    parts = line.split('| MOOP:', 1)
                    key = parts[0].replace('KEY:', '').strip()
                    text = parts[1].strip()
                    if key and text:
                        results[key] = text
            
            return results
            
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                print(f"  Batch failed after {retries} attempts, using NKJV fallback")
                # Fallback: just use cleaned NKJV
                results = {}
                for key, data in verses_batch:
                    results[key] = strip_html(data.get('NKJV', ''))
                return results

def get_book_keys(cache, book_num):
    """Get all verse keys for a book, sorted."""
    prefix = f'{book_num}_'
    keys = [k for k in cache.keys() if k.startswith(prefix)]
    # Sort by book_chapter_verse
    def sort_key(k):
        parts = k.split('_')
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    keys.sort(key=sort_key)
    return keys

def main():
    print("Loading verse cache and moop translation...")
    cache = load_json(VERSE_CACHE)
    moop = load_json(MOOP_FILE)
    
    print(f"Cache: {len(cache)} verses | MOOP: {len(moop)} verses")
    
    for book_num, book_name in BOOKS:
        keys = get_book_keys(cache, book_num)
        # Filter to only keys not yet processed
        todo = [k for k in keys if k not in moop]
        
        print(f"\n=== {book_name} ===")
        print(f"Total: {len(keys)} | Already done: {len(keys)-len(todo)} | To do: {len(todo)}")
        
        if not todo:
            print(f"  {book_name} already complete!")
            continue
        
        processed = 0
        total = len(todo)
        
        # Process in batches
        for i in range(0, len(todo), BATCH_SIZE):
            batch_keys = todo[i:i+BATCH_SIZE]
            batch_data = [(k, cache[k]) for k in batch_keys if k in cache]
            
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(todo) + BATCH_SIZE - 1) // BATCH_SIZE
            
            print(f"  Batch {batch_num}/{total_batches} ({len(batch_data)} verses)...", end='', flush=True)
            
            results = process_batch(batch_data)
            
            # Merge results into moop
            moop.update(results)
            processed += len(results)
            
            print(f" done ({len(results)} verses). Total so far: {processed}/{total}")
            
            # Small delay to be nice to the API
            time.sleep(0.5)
        
        # Save after each book
        print(f"\nSaving {book_name}... ({len(moop)} total MOOP verses)")
        save_json(MOOP_FILE, moop)
        print(f"Saved!")
    
    print(f"\n=== COMPLETE ===")
    print(f"Total MOOP verses: {len(moop)}")
    
    # Verify
    for book_num, book_name in BOOKS:
        keys = get_book_keys(cache, book_num)
        done = sum(1 for k in keys if k in moop)
        print(f"{book_name}: {done}/{len(keys)} verses")

if __name__ == '__main__':
    main()
