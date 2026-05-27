#!/usr/bin/env python3
"""add_personal_notes.py — inject Johns-family personal-note sections.

For specific dictionary entries that carry a family name (Gideon, Boaz,
Shiloh, etc.), inject a small "In This Editor's House" section just
before the <footer>. Idempotent via the marker comment.

Run once after generating entries to surface the family annotations the
editor (Adam Johns) wanted on entries that name his living children, his
siblings, and the unborn children he and Maria carried but did not get
to hold.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = os.path.join(ROOT, 'docs', 'dictionary')

MARK_START = '<!-- PERSONAL-NOTE-START -->'
MARK_END = '<!-- PERSONAL-NOTE-END -->'

NOTES = {
    'gideon': {
        'who': 'son',
        'body': (
            'The editor of this dictionary, Adam Johns, has a living son named '
            '<strong>Gideon</strong>. The biblical Gideon’s story (Judges 6–8) '
            '— from threshing wheat in a winepress for fear of the Midianites to '
            'leading three hundred to victory with torches and trumpets — is a '
            'gospel of God’s strength made perfect in human weakness. The hope of '
            'the editor and his wife <a href="maria.html">Maria</a> is that their son '
            'will grow up to know the LORD who is with him as God was with the biblical '
            'Gideon, and to take down the high places of his generation by faith.'
        ),
    },
    'boaz-doctrine': {
        'who': 'son',
        'body': (
            'The editor of this dictionary, Adam Johns, has a living son named '
            '<strong>Boaz</strong>. The biblical Boaz is the kinsman-redeemer of Ruth, '
            'a man of “wealth and standing” (Ruth 2:1) whose generosity in the '
            'field, courage at the gate, and covenant fidelity make him one of the great '
            'OT pictures of Christ. The hope of the editor and his wife '
            '<a href="maria.html">Maria</a> is that their son will grow up to embody the '
            'biblical Boaz’s pattern — industrious in the field, gracious to the '
            'vulnerable, and faithful to the redeeming work the Lord gives him.'
        ),
    },
    'shiloh-doctrine': {
        'who': 'daughter',
        'body': (
            'The editor of this dictionary, Adam Johns, has a living daughter named '
            '<strong>Shiloh</strong>. The biblical Shiloh — the Messianic title '
            'in Jacob’s blessing of Judah (Gen 49:10), and the town where the '
            'tabernacle stood for 369 years — is also occasionally given as a '
            'name to sons (it is one of several biblical place-names that have crossed '
            'into modern use as both girl’s and boy’s names). The hope of the '
            'editor and his wife <a href="maria.html">Maria</a> is that their daughter '
            'will grow up to find her place in the One to whom the scepter belongs.'
        ),
    },
    'hannah': {
        'who': 'sister',
        'body': (
            'The editor of this dictionary, Adam Johns, has a sister named '
            '<strong>Hannah</strong>. The biblical Hannah — the long-barren mother '
            'of Samuel whose prayer in 1 Samuel 2 foreshadows Mary’s Magnificat '
            '— is one of the great figures of female faith in the OT. The editor '
            'is thankful for the Hannah in his own family, whose name carries the '
            '<em>chanan</em> root of grace.'
        ),
    },
    'david': {
        'who': 'brother',
        'body': (
            'The editor of this dictionary, Adam Johns, has a brother named '
            '<strong>David</strong>. The biblical David is the king after God’s own '
            'heart, the psalmist, the type of Christ in his royal-priestly mediation, '
            'and the line through which Messiah came. The editor is thankful for the '
            'brother in his own family who carries the name.'
        ),
    },
    'joshua-figure': {
        'who': 'brother',
        'body': (
            'The editor of this dictionary, Adam Johns, has a brother named '
            '<strong>Joshua</strong>. The biblical Joshua — successor to Moses, '
            'who led Israel into the promised land — bears the Hebrew name '
            '<em>Yeshua</em>, the same name given to our Lord Jesus Christ in His '
            'incarnation. The editor is thankful for the brother in his own family '
            'who carries the name.'
        ),
    },
    'hope': {
        'who': 'lost daughter',
        'body': (
            'The editor of this dictionary, Adam Johns, and his wife '
            '<a href="maria.html">Maria</a> named one of their twin daughters '
            '<strong>Hope</strong>. She was lost to miscarriage in 2018 in Okinawa, '
            'Japan, alongside her sister <a href="mercy-twin.html">Mercy</a>. See '
            '<a href="hope-twin.html">Hope (Twin)</a> for the full memorial entry. '
            'The biblical hope she was named for is now hers in the morning of the '
            'resurrection.'
        ),
    },
    'mercy': {
        'who': 'lost daughter',
        'body': (
            'The editor of this dictionary, Adam Johns, and his wife '
            '<a href="maria.html">Maria</a> named one of their twin daughters '
            '<strong>Mercy</strong>. She was lost to miscarriage in 2018 in Okinawa, '
            'Japan, alongside her sister <a href="hope-twin.html">Hope</a>. See '
            '<a href="mercy-twin.html">Mercy (Twin)</a> for the full memorial entry. '
            'The biblical mercy she was named for is now hers in the kingdom of the '
            'Father of Mercies.'
        ),
    },
}


SECTION_TEMPLATE = '''
        {start}
        <div class="section" style="border-color:var(--gold);background:rgba(212,175,55,0.04);">
            <h3>&#128153; In This Editor's House</h3>
            <p style="font-size:0.95rem;line-height:1.7;">{body}</p>
            <p style="margin-top:8px;font-size:0.82rem;color:var(--gray);font-style:italic;">From the editor of this dictionary, Adam Johns &mdash; one of the personal annotations linking the canonical entry to the family that bears the name.</p>
        </div>
        {end}
'''


def process(slug, note):
    fp = os.path.join(DICT, f'{slug}.html')
    if not os.path.exists(fp):
        print(f'SKIP {slug}: file not found')
        return False
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    section = SECTION_TEMPLATE.format(
        start=MARK_START, body=note['body'], end=MARK_END
    )
    if MARK_START in html:
        # Replace existing
        new_html = re.sub(
            re.escape(MARK_START) + r'.*?' + re.escape(MARK_END),
            section.strip(),
            html,
            flags=re.DOTALL,
        )
    else:
        # Insert before <footer>
        if '<footer>' not in html:
            print(f'SKIP {slug}: no <footer> found')
            return False
        new_html = html.replace('<footer>', section + '    <footer>', 1)
    if new_html == html:
        print(f'NOOP {slug}')
        return False
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'OK   {slug} ({note["who"]})')
    return True


def main():
    print('Adding personal-note sections to family-name entries...')
    n = 0
    for slug, note in NOTES.items():
        if process(slug, note):
            n += 1
    print(f'\n{n} entries annotated.')


if __name__ == '__main__':
    main()
