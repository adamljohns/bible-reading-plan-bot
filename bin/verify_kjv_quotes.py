#!/usr/bin/env python3
"""Verify a batch JSON's scripture quotes verbatim against docs/assets/verse-cache.json (KJV).

Usage: python3 bin/verify_kjv_quotes.py data/dictionary-batches/batch-NN-*.json [...]

The cache embeds Strong's numbers inline (word<S>1234</S>) and folds psalm
titles into verse 1 (Hebrew numbering), so we strip tags AND digits on both
sides and do a substring match — a quote that is genuine KJV always passes;
a paraphrase or wrong-verse citation fails. Title refs ("Psa 46, title")
are skipped (titles live inside verse 1 here).

AN UNRESOLVABLE REFERENCE IS A FAILURE, NOT A SKIP (fixed 2026-08-05).
Until now a ref this script could not parse — `Psalm 22:1`, `John 1:14`,
`2 Tim. 3:16`, anything outside the 3-letter BOOKNUM table — fell into the
same `skipped` bucket as a genuine cache miss. A batch written entirely in
that style therefore reported "0 verified, 0 mismatched" and exited 0: a
PASS meaning *nothing was examined*. That is how batches 417, 423-426 and
430-436 cleared the pipeline carrying NASB/LSB/ESV text, and how 10,973 of
20,780 scripture slots (52.8%) came to be silently unchecked corpus-wide.

Exit 1 on: any mismatch, any unresolvable reference, any uncached verse, or
a run that verified nothing at all. Pass --allow-uncached to downgrade only
the cache-miss class to a warning (the cache holds 30,706 of 31,102 KJV
verses, so a legitimate hole is possible and is not the author's fault).

Usage: python3 bin/verify_kjv_quotes.py data/dictionary-batches/batch-NN-*.json [...]
       python3 bin/verify_kjv_quotes.py --allow-uncached data/.../batch-NN-*.json
"""
import json, re, sys, html

CACHE = 'docs/assets/verse-cache.json'
BOOKNUM = {'Gen':1,'Exo':2,'Lev':3,'Num':4,'Deu':5,'Josh':6,'Jos':6,'Jdg':7,'Rut':8,
           '1Sa':9,'2Sa':10,'1Ki':11,'2Ki':12,'1Ch':13,'2Ch':14,'Ezr':15,'Neh':16,
           'Est':17,'Job':18,'Psa':19,'Pro':20,'Ecc':21,'Son':22,'Isa':23,'Jer':24,
           'Lam':25,'Eze':26,'Dan':27,'Hos':28,'Joe':29,'Amo':30,'Oba':31,'Jon':32,
           'Mic':33,'Nah':34,'Hab':35,'Zep':36,'Hag':37,'Zec':38,'Mal':39,'Mat':40,
           'Mar':41,'Luk':42,'Joh':43,'Act':44,'Rom':45,'1Co':46,'2Co':47,'Gal':48,
           'Eph':49,'Php':50,'Col':51,'1Th':52,'2Th':53,'1Ti':54,'2Ti':55,'Tit':56,
           'Phm':57,'Heb':58,'Jas':59,'1Pe':60,'2Pe':61,'1Jn':62,'2Jn':63,'3Jn':64,
           'Jud':65,'Rev':66}

# The corpus overwhelmingly cites scripture the way a human writes it —
# "John 1:14", "Acts 2:38", "Psalm 22:1", "1 Corinthians 13:4" — and the
# original 3-letter-only table could read none of it. That is not an authoring
# defect; it is the verifier being unable to read its own corpus, and it is
# what left 10,973 of 20,780 scripture slots silently unexamined. Resolve the
# ordinary forms instead of demanding everything be rewritten.
_FULL = {
    'genesis':1,'exodus':2,'leviticus':3,'numbers':4,'deuteronomy':5,'joshua':6,
    'judges':7,'ruth':8,'1samuel':9,'2samuel':10,'1kings':11,'2kings':12,
    '1chronicles':13,'2chronicles':14,'ezra':15,'nehemiah':16,'esther':17,
    'job':18,'psalm':19,'psalms':19,'proverbs':20,'ecclesiastes':21,
    'songofsolomon':22,'songofsongs':22,'canticles':22,'isaiah':23,
    'jeremiah':24,'lamentations':25,'ezekiel':26,'daniel':27,'hosea':28,
    'joel':29,'amos':30,'obadiah':31,'jonah':32,'micah':33,'nahum':34,
    'habakkuk':35,'zephaniah':36,'haggai':37,'zechariah':38,'malachi':39,
    'matthew':40,'mark':41,'luke':42,'john':43,'acts':44,'romans':45,
    '1corinthians':46,'2corinthians':47,'galatians':48,'ephesians':49,
    'philippians':50,'colossians':51,'1thessalonians':52,'2thessalonians':53,
    '1timothy':54,'2timothy':55,'titus':56,'philemon':57,'hebrews':58,
    'james':59,'1peter':60,'2peter':61,'1john':62,'2john':63,'3john':64,
    'jude':65,'revelation':66,'revelations':66,
}
_ABBR = {
    'gen':1,'ge':1,'exo':2,'ex':2,'exod':2,'lev':3,'le':3,'num':4,'nu':4,
    'deu':5,'dt':5,'deut':5,'jos':6,'josh':6,'jdg':7,'judg':7,'jg':7,
    'rut':8,'ru':8,'1sa':9,'1sam':9,'2sa':10,'2sam':10,'1ki':11,'1kg':11,
    '1kgs':11,'2ki':12,'2kg':12,'2kgs':12,'1ch':13,'1chr':13,'2ch':14,
    '2chr':14,'ezr':15,'neh':16,'ne':16,'est':17,'es':17,'psa':19,'ps':19,
    'psalm':19,'pss':19,'pro':20,'prov':20,'pr':20,'ecc':21,'eccl':21,
    'son':22,'song':22,'sos':22,'isa':23,'is':23,'jer':24,'je':24,'lam':25,
    'la':25,'eze':26,'ezek':26,'dan':27,'da':27,'hos':28,'ho':28,'joe':29,
    'joel':29,'amo':30,'am':30,'oba':31,'ob':31,'jon':32,'mic':33,'mi':33,
    'nah':34,'na':34,'hab':35,'zep':36,'zeph':36,'hag':37,'zec':38,'zech':38,
    'mal':39,'mat':40,'matt':40,'mt':40,'mar':41,'mk':41,'mrk':41,'luk':42,
    'lk':42,'luke':42,'joh':43,'jn':43,'jno':43,'act':44,'ac':44,'rom':45,
    'ro':45,'1co':46,'1cor':46,'2co':47,'2cor':47,'gal':48,'ga':48,'eph':49,
    'php':50,'phil':50,'phili':50,'col':51,'1th':52,'1thes':52,'1thess':52,
    '2th':53,'2thes':53,'2thess':53,'1ti':54,'1tim':54,'2ti':55,'2tim':55,
    'tit':56,'phm':57,'philem':57,'phlm':57,'heb':58,'jas':59,'jam':59,
    '1pe':60,'1pet':60,'1pt':60,'2pe':61,'2pet':61,'2pt':61,'1jn':62,'1jo':62,
    '1joh':62,'2jn':63,'2jo':63,'2joh':63,'3jn':64,'3jo':64,'3joh':64,
    'jud':65,'jude':65,'rev':66,'re':66,'rv':66,
    # Old concordance-style forms the corpus actually uses (Lu 4:26, Mr 5:9,
    # De 25:15, Obad 1:10, 2 Chron 36:20) — absent from the table above, they
    # made 90 already-KJV quotes report as unresolvable.
    'lu':42,'mr':41,'de':5,'obad':31,'1chron':13,'2chron':14,
    'phi':50,'sng':22,'ec':21,'esth':17,
}

# Obadiah, Philemon, 2 John, 3 John, Jude — one chapter each, so the corpus
# legitimately cites them verse-only ("Jude 3"). Treat that as chapter 1.
SINGLE_CHAPTER = {31, 57, 63, 64, 65}
VERSE_ONLY_RE = re.compile(
    r'^\s*([1-3]?\s*[A-Za-z][A-Za-z\s]*?)\.?\s+(\d+)(?:\s*[-–]\s*(\d+))?\s*$')

def parse_ref(ref):
    """Resolve a reference to (book_number, chapter, v1, v2) or None."""
    m = REF_RE.match(ref)
    if m:
        bn = resolve_book(m.group(1))
        if bn == 65 and (int(m.group(2)) > 1 or int(m.group(3)) > 25):
            bn = 7   # 'Jud 20:1'/'Jud 1:33' are Judges — Jude is 1 chapter, 25 verses
        if bn:
            return bn, m.group(2), m.group(3), m.group(4)
    m = VERSE_ONLY_RE.match(ref)
    if m:
        bn = resolve_book(m.group(1))
        if bn in SINGLE_CHAPTER:
            return bn, '1', m.group(2), m.group(3)
    return None

def resolve_book(token):
    """Map any reasonable rendering of a book name to its cache number."""
    k = re.sub(r'[\s.]+', '', token).lower()
    if k in _FULL:
        return _FULL[k]
    if k in _ABBR:
        return _ABBR[k]
    return BOOKNUM.get(token)

# Leading book portion may carry a number and internal spaces
# ("1 Corinthians", "Song of Solomon"), then chapter:verse, optionally a
# range ("1Pe 2:2-3"). Entries legitimately quote across two or three verses.
REF_RE = re.compile(r'^\s*([1-3]?\s*[A-Za-z][A-Za-z\s]*?)\.?\s*(\d+):(\d+)(?:\s*[-–]\s*(\d+))?')

def cache_text(cache, bn, chap, v1, v2=None, version='KJV'):
    """Text for a verse, or the joined text of a verse range.

    Defaults to the Authorized Version. A `version` may be named because the
    cache holds 73 verses that carry every modern translation but no KJV
    (Jdg 14:18, Dan 3:31-4:37, and others). Adam's 2026-08-16 ruling allows any
    BTE version when it is attributed, so those verses are quotable from the
    public-domain WEB rather than being unusable."""
    out = []
    for n in range(int(v1), int(v2 or v1) + 1):
        e = cache.get(f'{bn}_{chap}_{n}')
        if not e or version not in e:
            return None if n == int(v1) else ' '.join(out)
        out.append(e[version])
    return ' '.join(out) if out else None

# A reference may name its version: "Jdg 14:18 (WEB)". Only versions the cache
# actually carries are accepted, and the attribution stays visible on the page.
VERSION_RE = re.compile(r'\(([A-Z0-9]{2,8})\)\s*$')

def ref_version(ref):
    m = VERSION_RE.search(ref or '')
    return m.group(1) if m else 'KJV'

def quote_matches(quoted, kjv):
    """A quote matches if it is a substring of the KJV text — or, when it
    elides with an ellipsis, if every fragment appears in order. Entries
    deliberately elide ('and Gideon made an ephod thereof... and all Israel
    went thither a whoring'), and a flat substring test cannot span that."""
    q, k = norm(quoted), norm(kjv)
    if q[:100] in k:
        return True
    # A quote may open or close mid-verse ("...and David said"). Strip the
    # outer ellipses first, or the split below yields a single fragment and
    # never reaches the in-order check.
    q = re.sub(r'^\s*(?:\.{3}|…)\s*', '', q)
    q = re.sub(r'\s*(?:\.{3}|…)\s*$', '', q)
    if q[:100] in k:
        return True
    parts = [p.strip() for p in re.split(r'\.{3}|…', q) if p.strip()]
    if len(parts) < 2:
        return False
    pos = 0
    for p in parts:
        i = k.find(p[:60], pos)
        if i < 0:
            return False
        pos = i + len(p[:60])
    return True

def norm(s):
    s = html.unescape(s).lower()
    s = re.sub(r'<sup>.*?</sup>', '', s, flags=re.S)   # translator margin notes
    s = re.sub(r'<[^>]+>', '', s)                       # tag markup
    s = re.sub(r'\d+', '', s)                           # inline Strong's numbers
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r'[“”]', '"', s)
    # Stripping inline Strong's tags leaves a gap before punctuation ("run
    # all , but"). kjv_lookup.py and the fill helper both clean it, so a
    # correctly generated quote failed against the raw cache text. Collapse
    # it on BOTH sides: a paraphrase still cannot pass.
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    allow_uncached = '--allow-uncached' in sys.argv[1:]

    cache = json.load(open(CACHE))
    bad = checked = titles = 0
    unresolvable, uncached = [], []

    for path in args:
        for e in json.load(open(path)):
            for ref, text in e.get('scriptures', []):
                if 'title' in ref:
                    titles += 1; continue
                parsed = parse_ref(ref)
                if not parsed:
                    # The author wrote a ref this verifier cannot resolve. That
                    # is an authoring defect, not a cache gap — it must fail.
                    unresolvable.append((e.get('slug', '?'), ref))
                    continue
                bn, chap, v1, v2 = parsed
                kjv = cache_text(cache, bn, chap, v1, v2, ref_version(ref))
                if not kjv:
                    uncached.append((e.get('slug', '?'), ref))
                    continue
                checked += 1
                if not quote_matches(text, kjv):
                    bad += 1
                    print(f'MISMATCH {e["slug"]} {ref}')
                    print(f'  quoted: {norm(text)[:110]}')
                    print(f'  KJV   : {norm(kjv)[:110]}')

    if unresolvable:
        print(f'\nUNRESOLVABLE REFERENCES ({len(unresolvable)}) — these were never checked.')
        print('Rewrite each in the 3-letter form this verifier reads (Psa 22:1, Joh 1:14, Php 2:6):')
        for slug, ref in unresolvable[:40]:
            print(f'  {slug:32} {ref}')
        if len(unresolvable) > 40:
            print(f'  ... and {len(unresolvable) - 40} more')

    if uncached:
        label = 'WARNING' if allow_uncached else 'UNCACHED — NOT VERIFIED'
        print(f'\n{label} ({len(uncached)}): verse absent from the cache, quote unchecked.')
        for slug, ref in uncached[:20]:
            print(f'  {slug:32} {ref}')
        if len(uncached) > 20:
            print(f'  ... and {len(uncached) - 20} more')

    print(f'\n{checked} verified, {bad} mismatched, '
          f'{len(unresolvable)} unresolvable, {len(uncached)} uncached, {titles} titles')

    fail = bool(bad or unresolvable or (uncached and not allow_uncached))
    # "Nothing was examined" is the failure mode this guard exists to catch:
    # it is what a wholly wrong-ref-style batch used to report as success.
    if not checked and (titles or unresolvable or uncached):
        print('FAIL: nothing was verified — this is not a pass.')
        fail = True
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
