#!/usr/bin/env python3
"""Fix BTE navigation + Bible index for usmcmin.org"""

import os
import re
import glob

BIBLE_INDEX_JS = """
        // BTE v3.3: Complete NKJV Bible Index (verse counts per chapter, 66 books)
        const BIBLE_INDEX = {
            1: [31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26], // Genesis
            2: [22,25,22,31,23,30,25,32,35,29,10,51,22,31,27,36,16,27,25,26,36,31,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38], // Exodus
            3: [17,16,17,35,19,30,38,36,24,20,47,8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34], // Leviticus
            4: [54,34,51,49,31,27,89,26,23,36,35,16,33,45,41,50,13,32,22,29,35,41,30,25,18,65,23,31,40,16,54,42,56,29,34,13], // Numbers
            5: [46,37,29,49,33,25,26,20,29,22,32,32,18,29,23,22,20,22,21,20,23,30,25,22,19,19,26,68,29,20,30,52,29,12], // Deuteronomy
            6: [18,24,17,24,15,27,26,35,27,43,23,24,33,15,63,10,18,28,51,9,45,34,16,33], // Joshua
            7: [36,23,31,24,31,40,25,35,57,18,40,15,25,20,20,31,13,31,30,48,25], // Judges
            8: [22,23,18,22], // Ruth
            9: [28,36,21,22,12,21,17,22,27,27,15,25,23,52,35,23,58,30,24,43,15,23,28,23,44,25,12,25,11,31,13], // 1 Samuel
            10: [27,32,39,12,25,23,29,18,13,19,27,31,39,33,37,23,29,33,43,26,22,51,39,25], // 2 Samuel
            11: [53,46,28,34,18,38,51,66,28,29,43,33,34,31,34,34,24,46,21,43,29,53], // 1 Kings
            12: [18,25,27,44,27,33,20,29,37,36,21,21,25,29,38,20,41,37,37,21,26,20,37,20,30], // 2 Kings
            13: [54,55,24,43,26,81,40,40,44,14,47,40,14,17,29,43,27,17,19,8,30,19,32,31,31,32,34,21,30], // 1 Chronicles
            14: [17,18,17,22,14,42,22,18,31,19,23,16,22,15,19,14,19,34,11,37,20,12,21,27,28,23,9,27,36,27,21,33,25,33,27,23], // 2 Chronicles
            15: [11,70,13,24,17,22,28,36,15,44], // Ezra
            16: [11,20,32,23,19,19,73,18,38,39,36,47,31], // Nehemiah
            17: [22,23,15,17,14,14,10,17,32,3], // Esther
            18: [22,13,26,21,27,30,21,22,35,22,20,25,28,22,35,22,16,21,29,29,34,30,17,25,6,14,23,28,25,31,40,22,33,37,16,33,24,41,30,24,34,17], // Job
            19: [6,12,8,8,12,10,17,9,20,18,7,8,6,7,5,11,15,50,14,9,13,31,6,10,22,12,14,9,11,12,24,11,22,22,28,12,40,22,13,17,13,11,5,26,17,11,9,14,20,23,19,9,6,7,23,13,11,11,17,12,8,12,11,10,13,20,7,35,36,5,24,20,28,23,10,12,20,72,13,19,16,8,18,12,13,17,7,18,52,17,16,15,5,23,11,13,12,9,9,5,8,28,22,35,45,48,43,13,31,7,10,10,9,8,18,19,2,29,176,7,8,9,4,8,5,6,5,6,8,8,3,18,3,3,21,26,9,8,24,13,10,7,12,15,21,10,20,14,9,6], // Psalms
            20: [33,22,35,27,23,35,27,36,18,32,31,28,25,35,33,33,28,24,29,30,31,29,35,34,28,28,27,28,27,33,31], // Proverbs
            21: [18,26,22,16,20,12,29,17,18,20,10,14], // Ecclesiastes
            22: [17,17,11,16,16,13,13,14], // Song of Solomon
            23: [31,22,26,6,30,13,25,22,21,34,16,6,22,32,9,14,14,7,25,6,17,25,18,23,12,21,13,29,24,33,9,20,24,17,10,22,38,22,8,31,29,25,28,28,25,13,15,22,26,11,23,15,12,17,13,12,21,14,21,22,11,12,19,12,25,24], // Isaiah
            24: [19,37,25,31,31,30,34,22,26,25,23,17,27,22,21,21,27,23,15,18,14,30,40,10,38,24,22,17,32,24,40,44,26,22,19,32,21,28,18,16,18,22,13,30,5,28,7,47,39,46,64,34], // Jeremiah
            25: [22,22,66,22,22], // Lamentations
            26: [28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35], // Ezekiel
            27: [21,49,30,37,31,28,28,27,27,21,45,13], // Daniel
            28: [11,23,5,19,15,11,16,14,17,15,12,14,16,9], // Hosea
            29: [20,32,21], // Joel
            30: [15,16,15,13,27,14,17,14,15], // Amos
            31: [21], // Obadiah
            32: [17,10,10,11], // Jonah
            33: [16,13,12,13,15,16,20], // Micah
            34: [15,13,19], // Nahum
            35: [17,20,19], // Habakkuk
            36: [18,15,20], // Zephaniah
            37: [15,23], // Haggai
            38: [21,13,10,14,11,15,14,23,17,12,17,14,9,21], // Zechariah
            39: [14,18,6,24], // Malachi
            40: [25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20], // Matthew
            41: [45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20], // Mark
            42: [80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53], // Luke
            43: [51,25,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25], // John
            44: [26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31], // Acts
            45: [32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27], // Romans
            46: [31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24], // 1 Corinthians
            47: [24,17,18,18,21,18,16,24,15,18,33,21,14], // 2 Corinthians
            48: [24,21,29,31,26,18], // Galatians
            49: [23,22,21,32,33,24], // Ephesians
            50: [30,30,21,23], // Philippians
            51: [29,23,25,18], // Colossians
            52: [10,20,13,18,28], // 1 Thessalonians
            53: [12,17,18], // 2 Thessalonians
            54: [20,15,16,16,25,21], // 1 Timothy
            55: [18,26,17,22], // 2 Timothy
            56: [16,15,15], // Titus
            57: [25], // Philemon
            58: [14,18,19,16,14,20,28,13,28,39,40,29,25], // Hebrews
            59: [27,26,18,17,20], // James
            60: [25,25,22,19,14], // 1 Peter
            61: [21,22,18], // 2 Peter
            62: [28,29,24,21,18], // 1 John
            63: [13], // 2 John
            64: [14], // 3 John
            65: [25], // Jude
            66: [20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21] // Revelation
        };
"""

NAV_FUNCTIONS_BIBLE = """
        // BTE v3.3: BIBLE_INDEX-aware navigation
        function navVerse(delta) {
            if (!currentRef) return;
            viewMode = 'verse';
            var bookId = currentRef.bookId;
            var ch = currentRef.chapter;
            var v = currentRef.startVerse + delta;
            var maxV = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 200;

            if (v > maxV) {
                ch++;
                var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;
                if (ch > maxCh) {
                    bookId++;
                    if (bookId > 66) return;
                    ch = 1;
                }
                v = 1;
            } else if (v < 1) {
                ch--;
                if (ch < 1) {
                    bookId--;
                    if (bookId < 1) return;
                    ch = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
                }
                v = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 1;
            }

            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + ch + ':' + v;
            lookupVerse();
        }

        function navChapter(delta) {
            if (!currentRef) return;
            var bookId = currentRef.bookId;
            var newCh = currentRef.chapter + delta;
            var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;

            if (newCh > maxCh) {
                bookId++;
                if (bookId > 66) return;
                newCh = 1;
            } else if (newCh < 1) {
                bookId--;
                if (bookId < 1) return;
                newCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
            }

            viewMode = 'chapter';
            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + newCh;
            lookupVerse();
        }

        function nav3Verses(delta) {
            if (!currentRef) return;
            viewMode = 'verse';
            var bookId = currentRef.bookId;
            var ch = currentRef.chapter;
            var v = currentRef.startVerse + (delta * 3);
            var maxV = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 200;

            if (v > maxV) {
                ch++;
                var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;
                if (ch > maxCh) {
                    bookId++;
                    if (bookId > 66) return;
                    ch = 1;
                }
                v = 1;
            } else if (v < 1) {
                ch--;
                if (ch < 1) {
                    bookId--;
                    if (bookId < 1) return;
                    ch = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
                }
                v = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 1;
            }

            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + ch + ':' + v;
            lookupVerse();
        }

"""

def fix_bible_html(filepath):
    """Fix the main bible.html file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert BIBLE_INDEX after BOOK_NAMES definition
    # Find the pattern after BOOK_NAMES is built
    book_names_pattern = r'(        const BOOK_NAMES = \{\};\s*Object\.entries\(BOOKS\)\.forEach[^;]+;\s*\}?\);)'
    match = re.search(book_names_pattern, content, re.DOTALL)
    if match:
        insert_pos = match.end()
        # Check if BIBLE_INDEX already exists
        if 'BIBLE_INDEX' not in content:
            content = content[:insert_pos] + '\n' + BIBLE_INDEX_JS + content[insert_pos:]
            print(f"  ✓ Inserted BIBLE_INDEX")
        else:
            print(f"  ✓ BIBLE_INDEX already present")
    else:
        print(f"  ✗ Could not find BOOK_NAMES insertion point!")

    # 2. Replace old nav functions with new ones
    # Remove old navChapter, navVerse, nav3Verses functions
    old_nav_pattern = r'\s*// BTE 3\.2: Navigation System\s*\n.*?const LEFT_SVG.*?const RIGHT_SVG.*?\n\s*function navChapter.*?function goToVerse'
    
    # More targeted: replace from navChapter through nav3Verses
    # Find and replace navChapter function
    nav_ch_pattern = r'        function navChapter\(delta\) \{[^}]+\}'
    nav_vs_pattern = r'        function navVerse\(delta\) \{[^}]+\}'
    nav3_pattern = r'        function nav3Verses\(delta\) \{[^}]+\}'

    # Find the block containing all three nav functions
    # Strategy: find the marker comment and replace the block
    nav_block_pattern = r'(        // BTE 3\.2: Navigation System\s*\n        const LEFT_SVG.*?const RIGHT_SVG.*?\n\n)(        function navChapter.*?)(        function navVerse.*?)(        function nav3Verses.*?)(        function goToVerse)'
    
    nav_block_match = re.search(nav_block_pattern, content, re.DOTALL)
    if nav_block_match:
        start = nav_block_match.start(2)
        end = nav_block_match.start(5)
        content = content[:start] + NAV_FUNCTIONS_BIBLE + content[end:]
        print(f"  ✓ Replaced nav functions (3-function block)")
    else:
        # Try replacing individually
        print(f"  ! Nav block pattern not found, trying individual replacement...")
        
        # Replace navChapter
        old_navch = re.search(r'        function navChapter\(delta\) \{.*?\n        \}', content, re.DOTALL)
        old_navvs = re.search(r'        function navVerse\(delta\) \{.*?\n        \}', content, re.DOTALL)
        old_nav3 = re.search(r'        function nav3Verses\(delta\) \{.*?\n        \}', content, re.DOTALL)
        
        if old_navch and old_navvs and old_nav3:
            # Replace from start of navChapter to end of nav3Verses
            start = old_navch.start()
            end = old_nav3.end()
            content = content[:start] + NAV_FUNCTIONS_BIBLE.strip() + '\n\n' + content[end:]
            print(f"  ✓ Replaced nav functions (individual)")
        else:
            print(f"  ✗ Could not find nav functions to replace!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved {filepath}")


def fix_verse_page(filepath):
    """Fix a verse page HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    
    # 1. Fix duplicate let viewMode / let isFullChapter declarations
    # The second block appears right after the LEFT_SVG/RIGHT_SVG constants
    # Pattern: after RIGHT_SVG definition, there's a blank line, then the duplicate declarations
    dup_pattern = r'(const RIGHT_SVG = \'[^\']+\';)\s*\n\s*\n\s*let viewMode = \'verse\';\s*\n\s*let isFullChapter = false;\s*\n'
    dup_match = re.search(dup_pattern, content)
    if dup_match:
        # Remove the duplicate declarations (keep just the RIGHT_SVG line and blank line)
        content = content[:dup_match.start()] + dup_match.group(1) + '\n\n' + content[dup_match.end():]
        print(f"  ✓ Fixed duplicate let viewMode/isFullChapter")
    else:
        # Check if duplicates exist at all
        viewmode_count = content.count("let viewMode = 'verse';")
        if viewmode_count > 1:
            print(f"  ! Found {viewmode_count} viewMode declarations, trying alternate fix...")
            # Find and remove the second occurrence
            first = content.index("let viewMode = 'verse';")
            second = content.index("let viewMode = 'verse';", first + 1)
            # Remove second occurrence line
            line_start = content.rfind('\n', 0, second) + 1
            line_end = content.index('\n', second) + 1
            # Also remove isFullChapter if it follows
            next_line = content[line_end:line_end+100]
            if "let isFullChapter" in next_line:
                ifc_end = content.index('\n', line_end) + 1
                content = content[:line_start] + content[ifc_end:]
            else:
                content = content[:line_start] + content[line_end:]
            print(f"  ✓ Removed duplicate viewMode via alternate method")
        elif viewmode_count == 0:
            print(f"  ! No viewMode declarations found")
        else:
            print(f"  ✓ No duplicate viewMode (only 1)")

    # 2. Insert BIBLE_INDEX after BOOK_NAMES definition
    if 'BIBLE_INDEX' not in content:
        book_names_pattern = r'(        const BOOK_NAMES = \{\};\s*Object\.entries\(BOOKS\)\.forEach[^;]+;\s*\}?\);)'
        match = re.search(book_names_pattern, content, re.DOTALL)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + '\n' + BIBLE_INDEX_JS + content[insert_pos:]
            print(f"  ✓ Inserted BIBLE_INDEX")
        else:
            print(f"  ✗ Could not find BOOK_NAMES insertion point!")
    else:
        print(f"  ✓ BIBLE_INDEX already present")

    # 3. Replace nav functions
    # In verse pages, navChapter, navVerse, nav3Verses are individual functions
    # Find them and replace
    old_navch = re.search(r'        function navChapter\(delta\) \{.*?\n        \}', content, re.DOTALL)
    old_navvs = re.search(r'        function navVerse\(delta\) \{.*?\n        \}', content, re.DOTALL)
    old_nav3 = re.search(r'        function nav3Verses\(delta\) \{.*?\n        \}', content, re.DOTALL)

    if old_navch and old_navvs and old_nav3:
        # Sort by position to find the contiguous block
        positions = sorted([
            (old_navch.start(), old_navch.end(), 'navChapter'),
            (old_navvs.start(), old_navvs.end(), 'navVerse'),
            (old_nav3.start(), old_nav3.end(), 'nav3Verses'),
        ])
        # They may not be contiguous, replace each individually
        # Replace in reverse order to preserve positions
        for start, end, name in reversed(positions):
            if name == 'navChapter':
                new_func = '''        function navChapter(delta) {
            if (!currentRef) return;
            var bookId = currentRef.bookId;
            var newCh = currentRef.chapter + delta;
            var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;

            if (newCh > maxCh) {
                bookId++;
                if (bookId > 66) return;
                newCh = 1;
            } else if (newCh < 1) {
                bookId--;
                if (bookId < 1) return;
                newCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
            }

            viewMode = 'chapter';
            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + newCh;
            lookupVerse();
        }'''
            elif name == 'navVerse':
                new_func = '''        function navVerse(delta) {
            if (!currentRef) return;
            viewMode = 'verse';
            var bookId = currentRef.bookId;
            var ch = currentRef.chapter;
            var v = currentRef.startVerse + delta;
            var maxV = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 200;

            if (v > maxV) {
                ch++;
                var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;
                if (ch > maxCh) {
                    bookId++;
                    if (bookId > 66) return;
                    ch = 1;
                }
                v = 1;
            } else if (v < 1) {
                ch--;
                if (ch < 1) {
                    bookId--;
                    if (bookId < 1) return;
                    ch = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
                }
                v = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 1;
            }

            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + ch + ':' + v;
            lookupVerse();
        }'''
            elif name == 'nav3Verses':
                new_func = '''        function nav3Verses(delta) {
            if (!currentRef) return;
            viewMode = 'verse';
            var bookId = currentRef.bookId;
            var ch = currentRef.chapter;
            var v = currentRef.startVerse + (delta * 3);
            var maxV = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 200;

            if (v > maxV) {
                ch++;
                var maxCh = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 999;
                if (ch > maxCh) {
                    bookId++;
                    if (bookId > 66) return;
                    ch = 1;
                }
                v = 1;
            } else if (v < 1) {
                ch--;
                if (ch < 1) {
                    bookId--;
                    if (bookId < 1) return;
                    ch = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId].length : 1;
                }
                v = BIBLE_INDEX[bookId] ? BIBLE_INDEX[bookId][ch - 1] : 1;
            }

            document.getElementById('refInput').value = BOOK_NAMES[bookId].replace(/\\b\\w/g, c => c.toUpperCase()) + ' ' + ch + ':' + v;
            lookupVerse();
        }'''
            content = content[:start] + new_func + content[end:]
        print(f"  ✓ Replaced nav functions")
    else:
        missing = []
        if not old_navch: missing.append('navChapter')
        if not old_navvs: missing.append('navVerse')
        if not old_nav3: missing.append('nav3Verses')
        print(f"  ✗ Could not find nav functions: {missing}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved {filename}")


def main():
    base = os.path.expanduser('~/bible-reading-plan-bot')
    
    print("\n=== Fixing bible.html ===")
    fix_bible_html(os.path.join(base, 'docs', 'bible.html'))
    
    print("\n=== Fixing verse pages ===")
    verse_pages = sorted(glob.glob(os.path.join(base, 'docs', 'verse', '*.html')))
    for page in verse_pages:
        print(f"\n--- {os.path.basename(page)} ---")
        fix_verse_page(page)
    
    print(f"\n✅ Processed {len(verse_pages)} verse pages + bible.html")


if __name__ == '__main__':
    main()
