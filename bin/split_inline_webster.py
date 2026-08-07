#!/usr/bin/env python3
"""Split inline `Webster 1828: "..."` out of the etymology block into a proper
house Webster 1828 Definition section, for the 7 converted pages that carry
real Webster content the converter deliberately left alone.
Dry run unless --apply. Refuses any page where the quote cannot be parsed.
"""
import re, sys, html, os
APPLY = '--apply' in sys.argv
SLUGS = ['temperance-virtue','sloth-sin','kindness-virtue','manhood',
         'lamb-of-god','patience-virtue','wifehood']
PAT = re.compile(r'\s*Webster\s*1828:\s*&quot;(.+?)&quot;\.?|\s*Webster\s*1828:\s*"(.+?)"\.?', re.S)

def section(word, body):
    return ('\n        <div class="section" id="webster">\n'
            '            <h3><img src="../assets/icons/shield-scroll-quill-24.png" alt="" '
            'width="20" height="20" style="vertical-align:middle;margin-right:6px;">'
            'Webster 1828 Definition</h3>\n'
            f'            <p class="section-summary">{word}</p>\n'
            '            <details>\n'
            '                <summary><em style="color:var(--gray)">expand to see more</em></summary>\n'
            '                <div class="webster-inner">\n'
            f'                    <p><strong>{word}</strong> {body}</p>\n'
            '                </div>\n'
            '            </details>\n'
            '        </div>\n')

ok = fail = 0
for s in SLUGS:
    p = f'docs/dictionary/{s}.html'
    h = open(p, encoding='utf-8').read()
    if 'class="webster-inner"' in h:
        print(f'  skip {s} — already has a Webster section'); continue
    m = re.search(r'(<div class="etymology"[^>]*>)(.*?)(</div>)', h, re.S)
    if not m:
        print(f'  FAIL {s} — no etymology block'); fail += 1; continue
    ety = m.group(2)
    q = PAT.search(ety)
    if not q:
        print(f'  FAIL {s} — no parseable Webster quote'); fail += 1; continue
    body = (q.group(1) or q.group(2)).strip()
    if not body.endswith('.'): body += '.'
    word = s.split('-')[0].upper() + ', n.'
    new_ety = PAT.sub('', ety, count=1)
    new_ety = re.sub(r'\s{2,}', ' ', new_ety).strip()
    # sanity: etymology must still have real content left
    plain = re.sub('<[^>]+>', '', html.unescape(new_ety)).strip()
    if len(plain) < 40:
        print(f'  FAIL {s} — etymology would be gutted'); fail += 1; continue
    out = h[:m.start()] + m.group(1) + new_ety + m.group(3) + h[m.end():]
    # insert the Webster section right after the definition section closes
    di = out.find('<div class="section" id="scriptures"')
    if di < 0:
        print(f'  FAIL {s} — no scriptures anchor to insert before'); fail += 1; continue
    out = out[:di] + section(word, body).lstrip('\n') + '\n        ' + out[di:]
    print(f'  {"apply" if APPLY else "would"} {s}: "{body[:64]}..."')
    if APPLY: open(p,'w',encoding='utf-8').write(out)
    ok += 1
print(f'\n{ok} ready, {fail} failed' + ('' if APPLY else '  (dry run)'))
