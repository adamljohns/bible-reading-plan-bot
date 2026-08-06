#!/usr/bin/env python3
"""mbt_word_sweep.py — find verses where the MOOP Bible Translation softens a
word the Authorized Version uses, and report whether ANY parallel rendering on
the verse page still carries the stronger word.

Adam, 2026-08-05, on James 1:20: "I prefer 'the wrath of man does not produce
the righteousness of God' — that's just a weightier word. It has to be in there
at least once in the parallel thing, because every parallel rendering on the
verse page says anger and none say wrath."

The verse page shows twelve translations. If the MBT softens a term AND no
parallel keeps the strong one, the reader never encounters it at all — that is
the case worth flagging. If KJV or NKJV still carry it, the word is present on
the page and the MBT's choice is a legitimate editorial one.

Usage:
  python3 bin/mbt_word_sweep.py                    # default wrath/anger sweep
  python3 bin/mbt_word_sweep.py --strong wrath --soft anger,angry
  python3 bin/mbt_word_sweep.py --strong repent --soft "change,turn"
  python3 bin/mbt_word_sweep.py --all              # include verses a parallel covers
"""
import json, re, os, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'docs/assets/verse-cache.json')
MBT = os.path.join(ROOT, 'docs/assets/moop-translation.json')

BOOKS = ['', 'Gen','Exo','Lev','Num','Deu','Jos','Jdg','Rut','1Sa','2Sa','1Ki','2Ki',
         '1Ch','2Ch','Ezr','Neh','Est','Job','Psa','Pro','Ecc','Son','Isa','Jer','Lam',
         'Eze','Dan','Hos','Joe','Amo','Oba','Jon','Mic','Nah','Hab','Zep','Hag','Zec',
         'Mal','Mat','Mar','Luk','Joh','Act','Rom','1Co','2Co','Gal','Eph','Php','Col',
         '1Th','2Th','1Ti','2Ti','Tit','Phm','Heb','Jas','1Pe','2Pe','1Jn','2Jn','3Jn',
         'Jud','Rev']

def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|\d+', '', s)).strip().lower()

def flatten(obj, out):
    """MBT nesting has varied over time; collect any book_chapter_verse key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and re.fullmatch(r'\d+_\d+_\d+', k):
                out[k] = v
            else:
                flatten(v, out)

def ref(key):
    b, c, v = key.split('_')
    b = int(b)
    return f'{BOOKS[b] if b < len(BOOKS) else b} {c}:{v}'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strong', default='wrath')
    ap.add_argument('--soft', default='anger,angry')
    ap.add_argument('--all', action='store_true',
                    help='also list verses where a parallel still carries the strong word')
    args = ap.parse_args()

    strong = args.strong.lower()
    softs = [s.strip().lower() for s in args.soft.split(',') if s.strip()]

    cache = json.load(open(CACHE))
    mbt = {}
    flatten(json.load(open(MBT)), mbt)

    uncovered, covered = [], []
    for key, entry in cache.items():
        if not isinstance(entry, dict) or 'KJV' not in entry:
            continue
        kjv = clean(entry['KJV'])
        if strong not in kjv:
            continue
        m = mbt.get(key)
        if not m:
            continue
        mc = clean(m)
        if strong in mc:
            continue                      # MBT already carries it
        if not any(s in mc for s in softs):
            continue                      # MBT used some third word; not this sweep
        others = [v for k, v in entry.items() if k != 'KJV' and isinstance(v, str)]
        keeps = [k for k, v in entry.items()
                 if k != 'KJV' and isinstance(v, str) and strong in clean(v)]
        (covered if keeps else uncovered).append((key, keeps, kjv, mc))

    print(f'KJV carries "{strong}", MBT uses {softs}: {len(uncovered) + len(covered)} verses')
    print(f'  no parallel keeps "{strong}"  -> {len(uncovered)}   ** reader never sees the word **')
    print(f'  a parallel keeps "{strong}"   -> {len(covered)}   (word is on the page; MBT choice stands)')

    def show(rows, title):
        if not rows:
            return
        print(f'\n{title}')
        for key, keeps, kjv, mc in sorted(rows, key=lambda r: [int(x) for x in r[0].split('_')]):
            print(f'  {ref(key)}' + (f'   [kept by: {", ".join(keeps)}]' if keeps else '   [NO parallel]'))
            print(f'     KJV: {kjv[:96]}')
            print(f'     MBT: {mc[:96]}')

    show(uncovered, f'--- MBT softened and NO parallel carries "{strong}" ---')
    if args.all:
        show(covered, f'--- MBT softened but a parallel still carries "{strong}" ---')

if __name__ == '__main__':
    main()
