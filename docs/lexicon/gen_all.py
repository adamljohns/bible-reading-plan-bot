#!/usr/bin/env python3
"""
Lexicon Phase 2 Generator — Creates 250 word pages from JSON data files.
Reads template.html and word data from hebrew_words.json + greek_words.json
"""
import json, os, glob

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, 'template.html')) as f:
    TEMPLATE = f.read()

# Load word data
all_words = []
for fn in sorted(glob.glob(os.path.join(DIR, '*_words.json'))):
    with open(fn) as f:
        all_words.extend(json.load(f))

# Collect all IDs for cross-linking
ALL_IDS = set()
for fn in os.listdir(DIR):
    if fn.endswith('.html') and fn[0] in ('H','G'):
        ALL_IDS.add(fn.replace('.html',''))
for w in all_words:
    ALL_IDS.add(w['id'])

def verse_html(verses):
    out = ''
    for ref, text in verses:
        ref_enc = ref.replace(' ','+')
        out += f'''
                <div class="verse-entry">
                    <a href="../bible.html?ref={ref_enc}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>'''
    return out

def related_html(related):
    parts = []
    for rid, trans, gl in related:
        label = f'{rid} — {trans} ({gl})'
        if rid in ALL_IDS:
            parts.append(f'<a href="{rid}.html" class="related-word">{label}</a>')
        else:
            parts.append(f'<span class="related-word">{label}</span>')
    return '\n                    '.join(parts)

count = 0
for w in all_words:
    wid = w['id']
    is_heb = wid.startswith('H')
    
    page = TEMPLATE
    replacements = {
        '{{ID}}': wid,
        '{{ID_LOWER}}': wid.lower(),
        '{{TRANSLIT}}': w['t'],
        '{{ORIGINAL}}': w['o'],
        '{{POS}}': w['p'],
        '{{GLOSS}}': w['g'],
        '{{SHORT_GLOSS}}': w['g'].split(',')[0].strip(),
        '{{LANG}}': 'Hebrew' if is_heb else 'Greek',
        '{{TESTAMENT_LONG}}': 'Old Testament' if is_heb else 'New Testament',
        '{{DIRECTION}}': 'direction:rtl;' if is_heb else '',
        '{{DEFINITION}}': w['d'],
        '{{USAGE}}': w['u'],
        '{{WORD_STUDY}}': w['w'],
        '{{VERSES}}': verse_html(w['v']),
        '{{RELATED}}': related_html(w['r']),
    }
    for k, v in replacements.items():
        page = page.replace(k, v)
    
    with open(os.path.join(DIR, f'{wid}.html'), 'w') as f:
        f.write(page)
    count += 1

print(f"Generated {count} lexicon pages")

# Now update manifest
manifest_path = os.path.join(DIR, '..', 'assets', 'lexicon-manifest.json')
with open(manifest_path) as f:
    manifest = json.load(f)

existing_ids = {e['id'] for e in manifest['entries']}
for w in all_words:
    if w['id'] not in existing_ids:
        manifest['entries'].append({
            'id': w['id'],
            'word': w['o'],
            'transliteration': w['t'],
            'gloss': w['g'],
            'pos': w['p'],
            'testament': 'OT' if w['id'].startswith('H') else 'NT'
        })

manifest['totalEntries'] = len(manifest['entries'])
manifest['entries'].sort(key=lambda e: (0 if e['id'].startswith('H') else 1, int(''.join(c for c in e['id'][1:] if c.isdigit()) or '0')))

with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Updated manifest: {manifest['totalEntries']} total entries")
