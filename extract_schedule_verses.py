#!/usr/bin/env python3
"""Extract all verse keys needed for the reading plan from schedule.json"""
import json, re

SCHEDULE = '/Users/adamjohns/bible-reading-plan-bot/schedule.json'

# Book name to ID mapping (Genesis-Job only, as that's what's in verse-cache)
BOOK_IDS = {
    'Genesis': '1', 'Exodus': '2', 'Leviticus': '3', 'Numbers': '4',
    'Deuteronomy': '5', 'Joshua': '6', 'Judges': '7', 'Ruth': '8',
    '1 Samuel': '9', 'Samuel': '9', '2 Samuel': '10',
    '1 Kings': '11', 'Kings': '11', '2 Kings': '12',
    '1 Chronicles': '13', 'Chronicles': '13', '2 Chronicles': '14',
    'Ezra': '15', 'Nehemiah': '16', 'Esther': '17', 'Job': '18'
}

def parse_reference(ref):
    """Parse 'Genesis 1:1-5' or 'Genesis 1' or 'Job 8' into verse keys."""
    # Match: BookName Chapter:Verse-Verse or BookName Chapter:Verse or BookName Chapter
    match = re.match(r'([A-Za-z\s]+?)\s+(\d+)(?::(\d+))?(?:[–-](\d+))?', ref.strip())
    if not match:
        return []
    
    book, chapter, start_verse, end_verse = match.groups()
    book = book.strip()
    
    # Check if book is in our cache (Genesis-Job only)
    book_id = BOOK_IDS.get(book)
    if not book_id:
        return []  # NT book or Psalms/Proverbs - not in cache
    
    keys = []
    if start_verse:
        # Has verse numbers
        start = int(start_verse)
        end = int(end_verse) if end_verse else start
        for v in range(start, end + 1):
            keys.append(f"{book_id}_{chapter}_{v}")
    else:
        # Whole chapter - we'll need to look this up in the verse cache
        # For now, mark it as needing the whole chapter
        keys.append(f"{book_id}_{chapter}_*")
    
    return keys

def extract_all_refs():
    """Extract all verse references from schedule.json"""
    with open(SCHEDULE) as f:
        schedule = json.load(f)
    
    refs = set()
    # Pattern to match Bible references: "Book Chapter" or "Book Chapter:Verse-Verse"
    # Examples: "Genesis 1", "Genesis 1:1-23", "Job 8", "1 Samuel 5"
    pattern = r'([A-Za-z\s]+?)\s+(\d+)(?::(\d+))?(?:[–-](\d+))?'
    
    for date, watches in schedule.items():
        for watch, text in watches.items():
            # Find all matches in the text
            matches = re.finditer(pattern, text)
            for match in matches:
                book, chapter, start_verse, end_verse = match.groups()
                book = book.strip()
                
                # Clean up book names that might have captured watch labels
                book = re.sub(r'^(Wisdom|1st|2nd|3rd|Peace)$', '', book).strip()
                if not book:
                    continue
                
                # Build reference string
                ref = f"{book} {chapter}"
                if start_verse:
                    ref += f":{start_verse}"
                    if end_verse:
                        ref += f"-{end_verse}"
                
                verse_keys = parse_reference(ref)
                refs.update(verse_keys)
    
    return refs

if __name__ == '__main__':
    refs = extract_all_refs()
    
    # Separate whole chapters from specific verses
    chapter_wildcards = [r for r in refs if r.endswith('_*')]
    specific_verses = [r for r in refs if not r.endswith('_*')]
    
    print(f"Specific verses: {len(specific_verses)}")
    print(f"Whole chapters: {len(chapter_wildcards)}")
    print(f"\nSample specific verses:")
    for v in sorted(specific_verses)[:10]:
        print(f"  {v}")
    print(f"\nSample chapters:")
    for v in sorted(chapter_wildcards)[:10]:
        print(f"  {v}")
    
    # Save to JSON
    output = {
        'specific_verses': sorted(specific_verses),
        'chapter_wildcards': sorted(chapter_wildcards)
    }
    with open('/Users/adamjohns/bible-reading-plan-bot/schedule-verses.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ Saved to schedule-verses.json")
