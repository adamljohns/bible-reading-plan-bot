#!/usr/bin/env python3
"""
Verse Cache Builder — fetches all 11 translations for every verse from bolls.life
Builds/extends docs/assets/verse-cache.json for books not yet cached.
Free API, no cost. Rate-limited to be respectful.
"""
import json, os, time, requests, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE, 'docs/assets/verse-cache.json')
CHUNKS_DIR = os.path.join(BASE, 'docs/assets/verse-chunks')

TRANSLATIONS = ['NKJV', 'KJV', 'ESV', 'NASB', 'NLT', 'WEB', 'CSB17', 'AMP', 'MSG', 'NIV', 'NRSVCE']

# bolls.life translation IDs (some differ from our labels)
BOLLS_MAP = {
    'NKJV': 'NKJV', 'KJV': 'KJV', 'ESV': 'ESV', 'NASB': 'NASB',
    'NLT': 'NLT', 'WEB': 'WEB', 'CSB17': 'CSB17', 'AMP': 'AMP',
    'MSG': 'MSG', 'NIV': 'NIV', 'NRSVCE': 'NRSVCE'
}

CHAPTER_API = 'https://bolls.life/get-chapter'

# Total chapters per book (1-66)
BOOK_CHAPTERS = {
    1:50, 2:40, 3:27, 4:36, 5:34, 6:24, 7:21, 8:4, 9:31, 10:24,
    11:22, 12:25, 13:29, 14:36, 15:10, 16:13, 17:10, 18:42,
    19:150, 20:31, 21:12, 22:8, 23:66, 24:52, 25:5, 26:48, 27:12,
    28:14, 29:3, 30:9, 31:1, 32:4, 33:7, 34:3, 35:3, 36:3, 37:2, 38:14, 39:4,
    40:28, 41:16, 42:24, 43:21, 44:28, 45:16, 46:16, 47:13,
    48:6, 49:6, 50:4, 51:4, 52:5, 53:3, 54:6, 55:4, 56:1, 57:1, 58:13,
    59:5, 60:5, 61:1, 62:1, 63:1, 64:1, 65:3, 66:22
}

BOOK_NAMES = {
    1:'Genesis',2:'Exodus',3:'Leviticus',4:'Numbers',5:'Deuteronomy',
    6:'Joshua',7:'Judges',8:'Ruth',9:'1 Samuel',10:'2 Samuel',
    11:'1 Kings',12:'2 Kings',13:'1 Chronicles',14:'2 Chronicles',
    15:'Ezra',16:'Nehemiah',17:'Esther',18:'Job',19:'Psalms',20:'Proverbs',
    21:'Ecclesiastes',22:'Song of Solomon',23:'Isaiah',24:'Jeremiah',
    25:'Lamentations',26:'Ezekiel',27:'Daniel',28:'Hosea',29:'Joel',30:'Amos',
    31:'Obadiah',32:'Jonah',33:'Micah',34:'Nahum',35:'Habakkuk',36:'Zephaniah',
    37:'Haggai',38:'Zechariah',39:'Malachi',40:'Matthew',41:'Mark',42:'Luke',
    43:'John',44:'Acts',45:'Romans',46:'1 Corinthians',47:'2 Corinthians',
    48:'Galatians',49:'Ephesians',50:'Philippians',51:'Colossians',
    52:'1 Thessalonians',53:'2 Thessalonians',54:'1 Timothy',55:'2 Timothy',
    56:'Titus',57:'Philemon',58:'Hebrews',59:'James',60:'1 Peter',
    61:'2 Peter',62:'1 John',63:'2 John',64:'3 John',65:'Jude',66:'Revelation'
}


def fetch_chapter(book_id, chapter, translation):
    """Fetch an entire chapter from bolls.life. Returns {verse_num: text}."""
    bolls_trans = BOLLS_MAP.get(translation, translation)
    url = f"{CHAPTER_API}/{bolls_trans}/{book_id}/{chapter}/"
    try:
        r = requests.get(url, timeout=10)
        if r.ok:
            data = r.json()
            return {str(v['verse']): v['text'] for v in data if v.get('text')}
    except Exception as e:
        print(f"  ⚠️ Error fetching {translation} {book_id}:{chapter}: {e}")
    return {}


def main():
    sys.stdout.reconfigure(line_buffering=True)

    # Load existing cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            cache = json.load(f)
    
    # Determine which books are already cached
    cached_books = set()
    for key in cache:
        cached_books.add(int(key.split('_')[0]))
    
    print(f"📖 Verse Cache Builder")
    print(f"✅ Already cached: {len(cached_books)} books ({len(cache):,} verses)")
    print(f"⏳ Remaining: {66 - len(cached_books)} books")
    
    # Parse args
    start_book = 1
    if len(sys.argv) > 1:
        start_book = int(sys.argv[1])
        print(f"📍 Starting from book {start_book} ({BOOK_NAMES.get(start_book, '?')})")
    
    new_verses = 0
    
    for book_id in range(start_book, 67):
        if book_id in cached_books:
            continue
        
        book_name = BOOK_NAMES.get(book_id, f'Book{book_id}')
        num_chapters = BOOK_CHAPTERS.get(book_id, 0)
        print(f"\n📚 {book_name} ({num_chapters} chapters)...")
        
        book_verses = 0
        
        for ch in range(1, num_chapters + 1):
            # Fetch all 11 translations for this chapter
            chapter_data = {}
            for trans in TRANSLATIONS:
                verses = fetch_chapter(book_id, ch, trans)
                for vnum, text in verses.items():
                    key = f"{book_id}_{ch}_{vnum}"
                    if key not in chapter_data:
                        chapter_data[key] = {}
                    chapter_data[key][trans] = text
                time.sleep(0.1)  # be respectful
            
            # Merge into cache
            for key, trans_dict in chapter_data.items():
                if key not in cache:
                    cache[key] = {}
                cache[key].update(trans_dict)
                if len(trans_dict) > 0:
                    book_verses += 1
                    new_verses += 1
            
            # Brief status every 10 chapters
            if ch % 10 == 0:
                print(f"  Ch {ch}/{num_chapters} ({book_verses} verses so far)")
            
            time.sleep(0.2)  # rate limit between chapters
        
        print(f"  ✅ {book_name}: {book_verses} verses cached")
        
        # Save after each book
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, separators=(',', ':'))
        
        # Also save per-book chunk
        os.makedirs(CHUNKS_DIR, exist_ok=True)
        book_data = {k: v for k, v in cache.items() if k.startswith(f"{book_id}_")}
        chunk_file = os.path.join(CHUNKS_DIR, f'book-{book_id}.json')
        with open(chunk_file, 'w') as f:
            json.dump(book_data, f, separators=(',', ':'))
        print(f"  📦 Chunk saved: book-{book_id}.json ({len(book_data)} verses)")
    
    print(f"\n🎉 Done! {new_verses:,} new verses cached.")
    print(f"📄 Total cache: {len(cache):,} verses")


if __name__ == '__main__':
    main()
