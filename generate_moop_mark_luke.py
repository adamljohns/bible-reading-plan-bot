#!/usr/bin/env python3
"""
MOOP Translation Generator — Mark (41) + Luke (42)
Uses OAuth token through Anthropic API with claude-haiku-4-5.
Batches 40 verses per API call for efficiency.
"""

import json
import re
import os
import sys
import time
import requests

CACHE_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json'
MOOP_PATH  = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json'

OAT_TOKEN = "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"

HEADERS = {
    "Content-Type": "application/json",
    "anthropic-version": "2023-06-01",
    "Authorization": f"Bearer {OAT_TOKEN}",
    "anthropic-beta": "oauth-2025-04-20",
}

API_URL = "https://api.anthropic.com/v1/messages"

def clean(text: str) -> str:
    """Strip HTML tags, Strong's numbers, superscripts, and extra whitespace."""
    if not text:
        return ''
    t = re.sub(r'<[^>]+>', ' ', text)
    t = re.sub(r'<S>\d+</S>', '', t)
    t = re.sub(r'\[[\d\w]+\]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

SYSTEM = """You are a Bible translation blender creating the MOOP Translation.

Rules:
- Take NKJV as the primary base text (keep its tone and wording as much as possible)
- Weave in 1-2 clarifying words or short phrases from ESV, NASB, NLT, or CSB ONLY where they genuinely add clarity or precision
- The result is ONE flowing, natural English sentence — no brackets, no annotations, no footnotes
- Subtler than the Amplified Bible — do NOT over-explain
- If NKJV is already clear and no other translation adds meaningful insight, just use NKJV as-is
- Preserve poetic structure where present (e.g. Psalms quotations within the text)
- Output ONLY the verse text — no references, no labels

You will receive a JSON array of verse objects. Return ONLY a valid JSON object mapping each key to the blended MOOP text.
Example input: [{"key":"41_1_1","NKJV":"...","ESV":"...","NASB":"...","NLT":"...","CSB":"..."}]
Example output: {"41_1_1":"Blended text here.","41_1_2":"..."}

Return ONLY the JSON object, no markdown, no explanation."""

def blend_batch(verses: list) -> dict:
    """Call Claude Haiku to blend a batch of verses. Returns {key: blended_text}."""
    payload = json.dumps(verses, ensure_ascii=False)
    
    body = {
        "model": "claude-haiku-4-5",
        "max_tokens": 4096,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": f"Blend these verses:\n{payload}"}]
    }
    
    for attempt in range(5):
        try:
            r = requests.post(API_URL, headers=HEADERS, json=body, timeout=120)
            
            if r.status_code == 429:
                retry_after = int(r.headers.get('retry-after', 30 * (attempt + 1)))
                print(f"\n  Rate limited — waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            
            if r.status_code == 529:  # Overloaded
                wait = 30 * (attempt + 1)
                print(f"\n  Overloaded — waiting {wait}s...")
                time.sleep(wait)
                continue
            
            if r.status_code != 200:
                print(f"\n  API error {r.status_code}: {r.text[:200]}")
                if attempt < 4:
                    time.sleep(10)
                    continue
                return {}
            
            data = r.json()
            raw = data['content'][0]['text'].strip()
            
            # Extract JSON from possible markdown code blocks
            m = re.search(r'\{[\s\S]+\}', raw)
            if m:
                return json.loads(m.group(0))
            return json.loads(raw)
            
        except json.JSONDecodeError as e:
            print(f"\n  JSON parse error attempt {attempt+1}: {e}")
            print(f"  Raw response: {raw[:300]}")
            if attempt == 4:
                # Return empty for this batch rather than crash
                return {}
            time.sleep(2)
        except Exception as e:
            print(f"\n  Error attempt {attempt+1}: {e}")
            if attempt == 4:
                return {}
            time.sleep(5)
    
    return {}

def process_book(book_id: int, cache: dict, moop: dict, batch_size: int = 40) -> int:
    prefix = f"{book_id}_"
    keys = sorted([k for k in cache.keys() if k.startswith(prefix)],
                  key=lambda k: tuple(int(x) for x in k.split('_')))
    
    # Skip already done
    todo = [k for k in keys if k not in moop]
    print(f"Book {book_id}: {len(keys)} total verses, {len(todo)} remaining")
    
    done = 0
    failed = []
    
    for i in range(0, len(todo), batch_size):
        batch_keys = todo[i:i+batch_size]
        batch = []
        for k in batch_keys:
            entry = cache[k]
            batch.append({
                "key": k,
                "NKJV": clean(entry.get('NKJV', '')),
                "ESV":  clean(entry.get('ESV', '')),
                "NASB": clean(entry.get('NASB', '')),
                "NLT":  clean(entry.get('NLT', '')),
                "CSB":  clean(entry.get('CSB17', '')),
            })
        
        print(f"  Verses {i+1}-{min(i+batch_size, len(todo))}/{len(todo)}", end=' ... ', flush=True)
        
        result = blend_batch(batch)
        
        if result:
            for k, v in result.items():
                moop[k] = v
            done += len(result)
            missing = [k for k in batch_keys if k not in result]
            if missing:
                failed.extend(missing)
                print(f"got {len(result)} ✓  (missed: {missing})")
            else:
                print(f"got {len(result)} ✓")
        else:
            failed.extend(batch_keys)
            print(f"FAILED — will retry")
        
        # Polite pause between batches
        time.sleep(1.5)
    
    # Retry failed verses one at a time
    if failed:
        print(f"\n  Retrying {len(failed)} failed verses individually...")
        for k in failed:
            entry = cache[k]
            single = [{
                "key": k,
                "NKJV": clean(entry.get('NKJV', '')),
                "ESV":  clean(entry.get('ESV', '')),
                "NASB": clean(entry.get('NASB', '')),
                "NLT":  clean(entry.get('NLT', '')),
                "CSB":  clean(entry.get('CSB17', '')),
            }]
            result = blend_batch(single)
            if result:
                for rk, rv in result.items():
                    moop[rk] = rv
                    done += 1
                print(f"    {k} ✓")
            else:
                # Last resort: use NKJV directly
                nkjv = clean(entry.get('NKJV', ''))
                if nkjv:
                    moop[k] = nkjv
                    done += 1
                    print(f"    {k} → NKJV fallback")
            time.sleep(2)
    
    return done

def main():
    print("Loading cache and MOOP file...")
    with open(CACHE_PATH) as f:
        cache = json.load(f)
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    
    total = 0
    
    # --- MARK (Book 41) ---
    print("\n=== MARK (Book 41) ===")
    n = process_book(41, cache, moop, batch_size=40)
    total += n
    
    print(f"\nSaving after Mark ({n} verses added)...")
    with open(MOOP_PATH, 'w') as f:
        json.dump(moop, f, indent=2, ensure_ascii=False)
    print("Saved ✓")
    
    # --- LUKE (Book 42) ---
    print("\n=== LUKE (Book 42) ===")
    n = process_book(42, cache, moop, batch_size=40)
    total += n
    
    print(f"\nSaving after Luke ({n} verses added)...")
    with open(MOOP_PATH, 'w') as f:
        json.dump(moop, f, indent=2, ensure_ascii=False)
    print("Saved ✓")
    
    print(f"\nDone! Total verses written: {total}")
    
    # Verification
    with open(MOOP_PATH) as f:
        final = json.load(f)
    mark_done = len([k for k in final if k.startswith('41_')])
    luke_done = len([k for k in final if k.startswith('42_')])
    print(f"Verification — Mark: {mark_done}/678, Luke: {luke_done}/1151")

if __name__ == '__main__':
    main()
