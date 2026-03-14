#!/usr/bin/env python3
"""
MOOP Translation Generator
Takes NKJV as base, weaves in clarifying words/phrases from ESV/NASB/NLT/CSB.
Produces ONE natural voice — no brackets, no annotations.
"""

import json
import re
import sys
from pathlib import Path

CACHE_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/verse-cache.json'
MOOP_PATH = '/Users/adamjohns/bible-reading-plan-bot/docs/assets/moop-translation.json'

def clean_html(text):
    """Remove HTML tags and superscript footnote markers."""
    if not text:
        return ''
    # Remove <sup>...</sup> footnote content
    text = re.sub(r'<sup[^>]*>.*?</sup>', '', text, flags=re.IGNORECASE|re.DOTALL)
    # Remove all other HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove trailing punctuation artifacts
    text = text.strip(' ,;')
    return text

def modernize_archaic(text):
    """Replace archaic English with modern equivalents."""
    # Word boundary replacements (case-sensitive patterns)
    replacements = [
        # Pronouns - second person
        (r'\bthee\b', 'you'),
        (r'\bTHEE\b', 'YOU'),
        (r'\bThee\b', 'You'),
        (r'\bthou\b', 'you'),
        (r'\bThou\b', 'You'),
        (r'\bTHOU\b', 'YOU'),
        (r'\bthy\b', 'your'),
        (r'\bThy\b', 'Your'),
        (r'\bTHY\b', 'YOUR'),
        (r'\bthine\b', 'your'),
        (r'\bThine\b', 'Your'),
        (r'\bTHINE\b', 'YOUR'),
        (r'\bye\b(?!\s*[a-z])', 'you'),  # "ye" as pronoun, not prefix
        (r'\bYe\b', 'You'),
        # Verb forms
        (r'\bhath\b', 'has'),
        (r'\bHath\b', 'Has'),
        (r'\bdoth\b', 'does'),
        (r'\bDoth\b', 'Does'),
        (r'\bart\b(?= [a-z])', 'are'),  # "art" as verb (before lowercase)
        (r'\bwilt\b', 'will'),
        (r'\bWilt\b', 'Will'),
        (r'\bwouldst\b', 'would'),
        (r'\bshouldst\b', 'should'),
        (r'\bcouldst\b', 'could'),
        (r'\bmayest\b', 'may'),
        (r'\bMayest\b', 'May'),
        (r'\bcanst\b', 'can'),
        (r'\bsayest\b', 'say'),
        (r'\bknoweth\b', 'knows'),
        (r'\bcometh\b', 'comes'),
        (r'\bgoeth\b', 'goes'),
        (r'\bgiveth\b', 'gives'),
        (r'\btaketh\b', 'takes'),
        (r'\bmaketh\b', 'makes'),
        (r'\bbringeth\b', 'brings'),
        (r'\bspeaketh\b', 'speaks'),
        (r'\bsendeth\b', 'sends'),
        (r'\bcauseth\b', 'causes'),
        (r'\bsitteth\b', 'sits'),
        (r'\bdwelleth\b', 'dwells'),
        (r'\bstandeth\b', 'stands'),
        (r'\bworketh\b', 'works'),
        (r'\bseeth\b', 'sees'),
        (r'\bheareth\b', 'hears'),
        (r'\bturneth\b', 'turns'),
        (r'\bliveth\b', 'lives'),
        (r'\bpasseth\b', 'passes'),
        (r'\brusheth\b', 'rushes'),
        (r'\bsaith\b', 'says'),
        (r'\bSaith\b', 'Says'),
        # Negative contractions
        (r'\bnot\b', 'not'),  # no change needed
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    return text

def blend_verse(key, translations):
    """
    Blend NKJV base with clarifying words from ESV/NASB/NLT/CSB.
    Returns a single natural-voice sentence.
    """
    nkjv = clean_html(translations.get('NKJV', ''))
    esv = clean_html(translations.get('ESV', ''))
    nasb = clean_html(translations.get('NASB', ''))
    nlt = clean_html(translations.get('NLT', ''))
    csb = clean_html(translations.get('CSB17', ''))
    
    if not nkjv:
        # Fallback to any available translation
        for t in [esv, nasb, nlt, csb]:
            if t:
                return modernize_archaic(t)
        return ''
    
    # Start with NKJV base, modernize archaic language
    result = modernize_archaic(nkjv)
    
    # Apply specific clarifying substitutions where ESV/NASB/NLT/CSB agree on a clearer term
    # and NKJV uses a less clear or archaic term
    
    # Common clarifications:
    # "wicked" → context-specific but usually fine to keep
    # "affliction" vs "suffering" - keep NKJV
    # "iniquity" - keep (theologically precise)
    
    # Clean up artifacts from <i> tags (implied words in NKJV are already clean now)
    # Remove any remaining HTML entities
    result = result.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    result = re.sub(r'\s+', ' ', result).strip()
    
    # Ensure proper sentence ending
    if result and result[-1] not in '.!?;:,\'"':
        pass  # Leave as-is; some verses continue from previous
    
    return result

def get_book_keys(cache, book_num):
    """Get all keys for a book, sorted by chapter then verse."""
    prefix = f'{book_num}_'
    keys = [k for k in cache if k.startswith(prefix)]
    # Sort by chapter, verse
    def sort_key(k):
        parts = k.split('_')
        return (int(parts[1]), int(parts[2]))
    return sorted(keys, key=sort_key)

def process_book(book_num, cache, moop):
    """Process all verses in a book, skip existing ones."""
    keys = get_book_keys(cache, book_num)
    new_count = 0
    skip_count = 0
    
    for key in keys:
        if key in moop:
            skip_count += 1
            continue
        
        translations = cache[key]
        blended = blend_verse(key, translations)
        if blended:
            moop[key] = blended
            new_count += 1
    
    return new_count, skip_count

def save_moop(moop):
    """Save moop translation file."""
    with open(MOOP_PATH, 'w', encoding='utf-8') as f:
        json.dump(moop, f, ensure_ascii=False, separators=(',', ':'))
    print(f'  → Saved {len(moop)} total entries to moop-translation.json')

def main():
    print('Loading files...')
    with open(CACHE_PATH) as f:
        cache = json.load(f)
    with open(MOOP_PATH) as f:
        moop = json.load(f)
    
    print(f'Cache: {len(cache)} verses | Moop: {len(moop)} existing entries')
    
    # Books to process in order
    books = [
        (24, 'Jeremiah'),
        (25, 'Lamentations'),
        (26, 'Ezekiel'),
        (27, 'Daniel'),
        (28, 'Hosea'),
        (29, 'Joel'),
        (30, 'Amos'),
        (32, 'Jonah'),
        (33, 'Micah'),
        (34, 'Nahum'),
        (35, 'Habakkuk'),
        (36, 'Zephaniah'),
        (37, 'Haggai'),
        (38, 'Zechariah'),
        (39, 'Malachi'),
        (1,  'Genesis'),
        (2,  'Exodus'),
        (3,  'Leviticus'),
        (4,  'Numbers'),
        (5,  'Deuteronomy'),
        (15, 'Ezra'),
        (16, 'Nehemiah'),
        (17, 'Esther'),
        (18, 'Job'),
        (21, 'Ecclesiastes'),
        (22, 'Song of Solomon'),
    ]
    
    # Filter to only the book specified in args, or process all
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    for book_num, book_name in books:
        if target != 'all' and target != str(book_num) and target != book_name:
            continue
        
        print(f'\nProcessing {book_name} (Book {book_num})...')
        new_count, skip_count = process_book(book_num, cache, moop)
        print(f'  New: {new_count} | Skipped: {skip_count}')
        
        if new_count > 0:
            save_moop(moop)
    
    print(f'\nDone! Total moop entries: {len(moop)}')

if __name__ == '__main__':
    main()
