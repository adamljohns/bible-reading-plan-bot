#!/usr/bin/env python3
"""
MOOP Translation Generator
Blends NKJV (base) with ESV/NASB/NLT/CSB clarifications.
Natural voice, no brackets, no annotations.
"""

import json
import os
import sys
import time
from openai import OpenAI

CACHE_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json'
MOOP_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json'
OPENAI_KEY = os.environ.get('OPENAI_API_KEY', '')

client = OpenAI(api_key=OPENAI_KEY)

BOOKS = [
    (52, '1 Thessalonians', 5),
    (53, '2 Thessalonians', 3),
    (54, '1 Timothy', 6),
    (55, '2 Timothy', 4),
    (59, 'James', 5),
    (60, '1 Peter', 5),
]

SYSTEM_PROMPT = """You are the MOOP Translation generator. Your job is to create a blended English Bible translation.

Rules:
- NKJV is the base text (~70% of the words)
- Weave in 1-2 clarifying words/phrases from ESV/NASB/NLT/CSB where they genuinely add clarity or nuance
- ONE natural voice — no brackets, no annotations, no source labels, no footnotes
- Subtler than the Amplified Bible — natural reading flow
- Do NOT add theology not in the text; only blend what's there
- Output ONLY the blended verse text, nothing else
- Remove any HTML tags like <br/> or <sup> tags from the input
- Strip Strongs concordance numbers like <S>1234</S>
"""

def clean_text(text):
    """Remove HTML tags and Strongs numbers from text."""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def blend_verse(key, verse_data):
    """Generate a single blended verse using GPT."""
    nkjv = clean_text(verse_data.get('NKJV', ''))
    esv = clean_text(verse_data.get('ESV', ''))
    nasb = clean_text(verse_data.get('NASB', ''))
    nlt = clean_text(verse_data.get('NLT', ''))
    csb = clean_text(verse_data.get('CSB17', ''))
    
    prompt = f"""Verse {key}:
NKJV: {nkjv}
ESV: {esv}
NASB: {nasb}
NLT: {nlt}
CSB: {csb}

Generate the MOOP blended translation (NKJV base with 1-2 clarifying phrases from others woven in naturally):"""
    
    return prompt

def blend_batch(verses_batch):
    """Blend a batch of verses in one API call."""
    batch_prompt = "Generate MOOP blended translations for these verses. For each verse, output ONLY the key followed by a pipe | followed by the blended text, one per line. Nothing else.\n\n"
    
    for key, verse_data in verses_batch:
        nkjv = clean_text(verse_data.get('NKJV', ''))
        esv = clean_text(verse_data.get('ESV', ''))
        nasb = clean_text(verse_data.get('NASB', ''))
        nlt = clean_text(verse_data.get('NLT', ''))
        csb = clean_text(verse_data.get('CSB17', ''))
        
        batch_prompt += f"KEY:{key}\nNKJV: {nkjv}\nESV: {esv}\nNASB: {nasb}\nNLT: {nlt}\nCSB: {csb}\n\n"
    
    batch_prompt += "Output format: KEY:52_1_1 | blended text here\nOne line per verse, NOTHING else."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": batch_prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    
    result = response.choices[0].message.content.strip()
    
    # Parse the output
    blended = {}
    for line in result.split('\n'):
        line = line.strip()
        if '|' in line and line.startswith('KEY:'):
            parts = line.split('|', 1)
            if len(parts) == 2:
                key_part = parts[0].replace('KEY:', '').strip()
                text_part = parts[1].strip()
                blended[key_part] = text_part
    
    return blended

def main():
    print("Loading files...")
    with open(CACHE_PATH) as f:
        cache = json.load(f)
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    
    print(f"Cache: {len(cache)} verses. MOOP already has: {len(moop)} verses.")
    
    BATCH_SIZE = 20  # verses per API call
    
    for book_num, book_name, chapters in BOOKS:
        print(f"\n=== Processing {book_name} (Book {book_num}) ===")
        
        # Get all verse keys for this book
        book_keys = sorted([k for k in cache.keys() if k.startswith(f'{book_num}_')],
                          key=lambda x: tuple(int(n) for n in x.split('_')))
        
        # Find which ones we still need to generate
        todo_keys = [k for k in book_keys if k not in moop]
        
        print(f"Total: {len(book_keys)} verses. Already done: {len(book_keys) - len(todo_keys)}. To do: {len(todo_keys)}")
        
        if not todo_keys:
            print("Already complete! Skipping.")
            continue
        
        # Process in batches
        success_count = 0
        for i in range(0, len(todo_keys), BATCH_SIZE):
            batch_keys = todo_keys[i:i+BATCH_SIZE]
            batch_data = [(k, cache[k]) for k in batch_keys if k in cache]
            
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(todo_keys) + BATCH_SIZE - 1) // BATCH_SIZE
            print(f"  Batch {batch_num}/{total_batches} ({len(batch_data)} verses)...", end=' ', flush=True)
            
            try:
                blended = blend_batch(batch_data)
                
                # Write results
                for key in batch_keys:
                    if key in blended:
                        moop[key] = blended[key]
                        success_count += 1
                    else:
                        # Fallback: just use NKJV if blend failed
                        nkjv = clean_text(cache.get(key, {}).get('NKJV', ''))
                        if nkjv:
                            moop[key] = nkjv
                            print(f"\n  [FALLBACK NKJV for {key}]", end='')
                        
                print(f"OK ({len(blended)} blended)")
                
            except Exception as e:
                print(f"ERROR: {e}")
                # Fallback to NKJV for this batch
                for key in batch_keys:
                    nkjv = clean_text(cache.get(key, {}).get('NKJV', ''))
                    if nkjv and key not in moop:
                        moop[key] = nkjv
                
            # Small delay to avoid rate limits
            time.sleep(0.5)
        
        # Save after each book
        print(f"  Saving {book_name}...")
        with open(MOOP_PATH, 'w') as f:
            json.dump(moop, f, indent=2)
        print(f"  Saved! Total MOOP entries: {len(moop)}")
    
    print(f"\n=== ALL DONE === Total MOOP entries: {len(moop)}")

if __name__ == '__main__':
    main()
