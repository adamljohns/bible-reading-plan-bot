#!/usr/bin/env python3
"""Add verse links to HTML files in docs/"""

import os
import re

DOCS_DIR = os.path.expanduser('~/bible-reading-plan-bot/docs')

# Map from verse reference pattern to (slug, display_text)
# Order matters: longer/more specific patterns first
VERSE_MAP = [
    # Multi-verse ranges first
    ("Romans 12:19-21",    "romans-12-19-21"),
    ("Romans 8:28-30",     "romans-8-28-30"),
    ("Ephesians 6:10-18",  "ephesians-6-10-18"),
    ("Ephesians 5:14-16",  "ephesians-5-14-16"),
    ("Deuteronomy 6:6-7",  "deuteronomy-6-6-7"),
    ("Proverbs 3:5-6",     "proverbs-3-5-6"),
    ("Hebrews 12:2-3",     "hebrews-12-2-3"),
    # Single verses
    ("1 Corinthians 6:19", "1-corinthians-6-19"),
    ("1 Timothy 4:12",     "1-timothy-4-12"),
    ("2 Chronicles 20:12", "2-chronicles-20-12"),
    ("2 Timothy 1:7",      "2-timothy-1-7"),
    ("2 Timothy 4:7",      "2-timothy-4-7"),
    ("Deuteronomy 32:35",  "deuteronomy-32-35"),
    ("Ephesians 5:25",     "ephesians-5-25"),
    ("Ezekiel 33:7",       "ezekiel-33-7"),
    ("Ezekiel 36:26",      "ezekiel-36-26"),
    ("Jeremiah 29:11",     "jeremiah-29-11"),
    ("Jeremiah 29:7",      "jeremiah-29-7"),
    ("John 3:16",          "john-3-16"),
    ("Luke 14:33",         "luke-14-33"),
    ("Proverbs 27:17",     "proverbs-27-17"),
    ("Romans 8:28",        "romans-8-28-30"),  # partial ref on bible.html quick links
]

def already_linked(text, ref):
    """Check if ref is already inside an <a> tag"""
    # Simple check: look for the ref preceded by > or followed by </a>
    pattern = r'href=[^>]+>[^<]*' + re.escape(ref)
    return bool(re.search(pattern, text))

def add_links(content, filename):
    """Replace unlinked verse refs with linked versions"""
    changes = 0
    for ref, slug in VERSE_MAP:
        # Skip if already wrapped in <a href="/verse/...">
        # We'll replace occurrences that are NOT already inside an <a> tag for this verse page
        url = f'/verse/{slug}.html'
        link = f'<a href="{url}" class="verse-link">{ref}</a>'
        
        # Pattern: ref NOT preceded by href="..." (i.e., not already linked)
        # Use a negative lookbehind for the href pattern
        # We need to avoid replacing refs that are:
        # 1. Already inside <a> tags
        # 2. Inside javascript strings (quickLook calls)
        # 3. In input placeholders
        
        # Simple approach: find all occurrences and check context
        new_content = []
        last_end = 0
        for m in re.finditer(re.escape(ref), content):
            start, end = m.start(), m.end()
            # Check: is this inside a tag attribute? Look back for unmatched <
            prefix = content[max(0, start-200):start]
            # Find if we're inside a tag (< without matching >)
            last_lt = prefix.rfind('<')
            last_gt = prefix.rfind('>')
            in_tag = last_lt > last_gt
            
            # Check if already inside an <a> href="/verse/ link
            href_check = content[max(0, start-300):end]
            already_verse_link = f'/verse/{slug}' in href_check and 'href=' in href_check
            
            # Check if inside quickLook JS call or placeholder attribute
            in_js = 'quickLook' in prefix[-50:] or 'placeholder' in prefix[-100:]
            
            if in_tag or already_verse_link or in_js:
                new_content.append(content[last_end:end])
            else:
                new_content.append(content[last_end:start])
                new_content.append(link)
                changes += 1
            last_end = end
        
        new_content.append(content[last_end:])
        content = ''.join(new_content)
    
    return content, changes

# Files to process (skip bible.html and backups)
SKIP_FILES = {'bible.html', 'bible-v3.1-backup.html'}

# Add CSS for verse links if not present
VERSE_LINK_CSS = """
        /* BTE Verse links */
        .verse-link {
            color: var(--gold, #D4AF37);
            text-decoration: none;
            border-bottom: 1px dotted var(--gold, #D4AF37);
            transition: opacity 0.2s;
        }
        .verse-link:hover { opacity: 0.8; border-bottom-style: solid; }
"""

total_changes = 0
for fname in os.listdir(DOCS_DIR):
    if not fname.endswith('.html'):
        continue
    if fname in SKIP_FILES:
        print(f"  Skipping: {fname}")
        continue
    
    fpath = os.path.join(DOCS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, changes = add_links(content, fname)
    
    if changes > 0:
        # Add CSS if not already present
        if '.verse-link' not in new_content and '</style>' in new_content:
            new_content = new_content.replace('</style>', VERSE_LINK_CSS + '        </style>', 1)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  {fname}: {changes} verse link(s) added")
        total_changes += changes
    else:
        print(f"  {fname}: no changes")

print(f"\nTotal verse links added: {total_changes}")
