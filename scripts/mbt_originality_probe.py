#!/usr/bin/env python3
"""
Honest originality probe for the MBT (bigram-provenance method).

For each authored verse, classify every two-word phrase (bigram) of the MBT text:
  - PD-covered   : appears in the public-domain KJV or WEB  -> legitimate
  - BORROWED     : appears in copyrighted NKJV/ESV but in NEITHER KJV nor WEB
                   -> genuine convergence on copyrighted phrasing (must fix)
  - original     : appears in none of them -> our own wording

Reports per-verse PD coverage and the literal borrowed phrases, so revision is
targeted. A verse is healthy when PD coverage is high and borrowed == 0.
"""
import json, re, glob, os
REPO = "/Users/moop_bot_pro/bible-reading-plan-bot"
cache = json.load(open(os.path.join(REPO, "docs/assets/verse-cache.json")))
_w = re.compile(r"[a-z]+")
def toks(s):
    s = (s or "").lower()
    s = re.sub(r"<s>\d+</s>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return _w.findall(s)
def bigrams(t): return {f"{t[i]} {t[i+1]}" for i in range(len(t)-1)}
STOP = set("the a an of in on and or but to for with his my your their its it he she "
           "they you i we him them me us is are was were be been being will shall would "
           "do does did not no when that which who whom this these those as at by from "
           "into up out over under so then than before after all any if".split())
def content(bg):  # True unless BOTH words are stopwords (generic modern function pairs)
    w1, w2 = bg.split(); return not (w1 in STOP and w2 in STOP)

need_fix = []
clean = 0
total_borrowed = 0
print(f"{'verse':11s} {'PDcov':>5s} {'borrowed bigrams (in NKJV/ESV, not in KJV/WEB)'}")
rows = []
for bf in sorted(glob.glob(os.path.join(REPO, "data/mbt-batches/*.json"))):
    b = json.load(open(bf))
    book, ch = b["book"], b["chapter"]
    for v, obj in b["verses"].items():
        key = f"{book}_{ch}_{v}"
        c = cache.get(key, {})
        mb = bigrams(toks(obj["text"]))
        if not mb: continue
        pd = bigrams(toks(c.get("KJV",""))) | bigrams(toks(c.get("WEB","")))
        cr = bigrams(toks(c.get("NKJV",""))) | bigrams(toks(c.get("ESV","")))
        borrowed = sorted(bg for bg in mb if bg in cr and bg not in pd and content(bg))
        pdcov = sum(1 for bg in mb if bg in pd)/len(mb)
        rows.append((key, pdcov, borrowed))
        total_borrowed += len(borrowed)
        if len(borrowed) >= 2: need_fix.append(key)
        elif len(borrowed) == 0: clean += 1

for key, pdcov, borrowed in sorted(rows, key=lambda r: -len(r[2])):
    tag = "  <== REVISE" if len(borrowed) >= 2 else ""
    print(f"{key:11s} {pdcov*100:4.0f}% {', '.join(borrowed) if borrowed else '(none)'}{tag}")

n = len(rows)
print(f"\nVerses: {n}   clean (0 borrowed): {clean}   need revision (>=2 borrowed): {len(need_fix)}")
print(f"Total borrowed bigrams across pilot: {total_borrowed}  (avg {total_borrowed/n:.1f}/verse)")
print(f"Mean PD coverage: {sum(r[1] for r in rows)/n*100:.0f}%")
print("Revise:", need_fix)
