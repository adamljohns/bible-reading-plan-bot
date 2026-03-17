#!/usr/bin/env python3
"""Generate lexicon HTML pages from words.json using template.html"""
import json, os, html

DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(DIR, 'template.html')) as f:
    TEMPLATE = f.read()
with open(os.path.join(DIR, 'words.json')) as f:
    WORDS = json.load(f)

# Collect all IDs (existing + new) for linking
ALL_IDS = set()
# existing
for fn in os.listdir(DIR):
    if fn.endswith('.html') and (fn.startswith('H') or fn.startswith('G')):
        ALL_IDS.add(fn.replace('.html',''))
for w in WORDS:
    ALL_IDS.add(w['id'])

def make_verse(ref, text):
    ref_enc = ref.replace(' ', '+')
    return f'''
                <div class="verse-entry">
                    <a href="../bible.html?ref={ref_enc}" class="verse-ref">{ref}</a>
                    <span class="verse-text">{text}</span>
                </div>'''

def make_related(rel_list):
    parts = []
    for r in rel_list:
        rid = r[0]; trans = r[1]; gl = r[2]
        label = f'{rid} — {trans} ({gl})'
        if rid in ALL_IDS:
            parts.append(f'<a href="{rid}.html" class="related-word">{label}</a>')
        else:
            parts.append(f'<span class="related-word">{label}</span>')
    return "\n                    ".join(parts)

count = 0
for w in WORDS:
    wid = w['id']
    is_hebrew = wid.startswith('H')
    lang = 'Hebrew' if is_hebrew else 'Greek'
    testament = 'OT' if is_hebrew else 'NT'
    testament_long = 'Old Testament' if is_hebrew else 'New Testament'
    direction = 'direction:rtl;' if is_hebrew else ''
    
    verses_html = ''.join(make_verse(v[0], v[1]) for v in w['verses'])
    related_html = make_related(w['related'])
    short_gloss = w['gloss'].split(',')[0].strip()
    
    page = TEMPLATE
    page = page.replace('{{ID}}', wid)
    page = page.replace('{{ID_LOWER}}', wid.lower())
    page = page.replace('{{TRANSLIT}}', w['transliteration'])
    page = page.replace('{{ORIGINAL}}', w['original'])
    page = page.replace('{{POS}}', w['pos'])
    page = page.replace('{{GLOSS}}', w['gloss'])
    page = page.replace('{{SHORT_GLOSS}}', short_gloss)
    page = page.replace('{{LANG}}', lang)
    page = page.replace('{{TESTAMENT_LONG}}', testament_long)
    page = page.replace('{{DIRECTION}}', direction)
    page = page.replace('{{DEFINITION}}', w['definition'])
    page = page.replace('{{USAGE}}', w['usage'])
    page = page.replace('{{WORD_STUDY}}', w['word_study'])
    page = page.replace('{{VERSES}}', verses_html)
    page = page.replace('{{RELATED}}', related_html)
    
    outpath = os.path.join(DIR, f'{wid}.html')
    with open(outpath, 'w') as f:
        f.write(page)
    count += 1

print(f"Generated {count} lexicon pages")
