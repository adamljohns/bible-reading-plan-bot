#!/usr/bin/env python3
"""Build the "What the Confessions Say" index for bible.html from symbolics.dev data.

Source: symbolics.sqlite from https://symbolics.dev/downloads/ (CC0, public domain).
Local copy: ~/Documents/Active/symbolics/downloads/symbolics.sqlite

Writes docs/assets/confessions/proofs/<bookId>.json (bookId 1-66, the BTE numbering):
  {"u": {"<doc>:<unit>": [label, href, question, full text]},
   "v": {"<chapter>:<verse>": [["<doc>:<unit>", start, end], ...]}}   in DOCS order
start/end mark the exact words the proof was printed against inside the full paragraph
or answer (-1 if not found), so the page shows the whole text and highlights the cited
part. Nothing is reworded.

Usage: python3 bin/build-confession-proofs.py [path/to/symbolics.sqlite]
"""
import json
import os
import pathlib
import re
import sqlite3
import sys

DEFAULT_DB = os.path.expanduser("~/Documents/Active/symbolics/downloads/symbolics.sqlite")
OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets" / "confessions" / "proofs"

# Order shown on the page. The 1689 first: it is this ministry's confession of record.
DOCS = [
    ("lbcf1689-modernized", "1689 Confession", "para"),
    ("wcf1646-modernized", "Westminster Confession", "para"),
    ("bc1695-modernized", "Baptist Catechism", "q"),
    ("wsc-modernized", "Shorter Catechism", "q"),
    ("wlc-modernized", "Larger Catechism", "q"),
    ("heidelberg", "Heidelberg Catechism", "q"),
]

OSIS_BOOKS = ["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
              "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
              "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
              "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
              "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph",
              "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb",
              "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"]
BOOK_ID = {b: i + 1 for i, b in enumerate(OSIS_BOOKS)}
POINT = re.compile(r"^([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?$")
MAX_VERSE = 176  # a range that crosses chapters marks the rest of the first chapter


def verses(osis):
    """Yield (bookId, chapter, verse) for one OSIS ref. Whole-chapter refs yield nothing:
    a proof for "Romans 8" is not a proof for every verse in it."""
    a, _, b = osis.partition("-")
    m1 = POINT.match(a)
    if not m1 or not m1.group(3) or m1.group(1) not in BOOK_ID:
        return
    book, c1, v1 = BOOK_ID[m1.group(1)], int(m1.group(2)), int(m1.group(3))
    if not b:
        yield book, c1, v1
        return
    m2 = POINT.match(b)
    if not m2 or not m2.group(3) or BOOK_ID.get(m2.group(1)) != book:
        yield book, c1, v1
        return
    c2, v2 = int(m2.group(2)), int(m2.group(3))
    if c2 == c1:
        for v in range(v1, v2 + 1):
            yield book, c1, v
        return
    # Whole middle chapters are skipped, for the same reason as whole-chapter refs.
    for v in range(v1, MAX_VERSE + 1):
        yield book, c1, v
    for v in range(1, v2 + 1):
        yield book, c2, v


def label_and_href(doc, name, kind, unit_id, unit):
    if kind == "para":
        ch, _, p = unit_id.partition(".")
        if doc.startswith("lbcf1689"):
            href = "/lbcf/chapter-%02d.html#p%s" % (int(ch), p)
        else:
            href = "https://symbolics.dev/%s/%s" % (doc, unit_id)
        return "%s %s" % (name, unit_id), href
    return "%s Q%s" % (name, unit.get("number", unit_id)), "https://symbolics.dev/%s/%s" % (doc, unit_id)


def main():
    db = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
    books = {}
    order = {d[0]: i for i, d in enumerate(DOCS)}
    for doc, name, kind in DOCS:
        rows = con.execute("SELECT id, json FROM units WHERE document=? ORDER BY position", (doc,))
        for unit_id, raw in rows:
            unit = json.loads(raw)
            label, href = label_and_href(doc, name, kind, unit_id, unit)
            question = unit.get("question") or ""
            full = (unit.get("text") or unit.get("answer") or "").strip()
            key = "%s:%s" % (doc, unit_id)
            cursor = 0
            for seg in unit.get("segments") or []:
                text = (seg.get("text") or "").strip()
                if not text:
                    continue
                # Where the cited words sit in the whole paragraph, so the page can mark them.
                start = full.find(text, cursor)
                if start < 0:
                    start = full.find(text)
                span = [start, start + len(text)] if start >= 0 else [-1, -1]
                if start >= 0:
                    cursor = start + len(text)
                for ref in seg.get("refs") or []:
                    for o in ref.get("osis") or []:
                        for book, c, v in verses(o):
                            bk = books.setdefault(book, {"u": {}, "v": {}})
                            bk["u"][key] = [label, href, question, full]
                            lst = bk["v"].setdefault("%d:%d" % (c, v), [])
                            if not any(e[0] == key for e in lst):
                                lst.append([key] + span)
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for book, data in sorted(books.items()):
        for k in data["v"]:
            data["v"][k].sort(key=lambda e: order[e[0].split(":", 1)[0]])
        total += sum(len(x) for x in data["v"].values())
        (OUT / ("%d.json" % book)).write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    size = sum(p.stat().st_size for p in OUT.glob("*.json"))
    print("books=%d verse-links=%d bytes=%d" % (len(books), total, size))


if __name__ == "__main__":
    main()
