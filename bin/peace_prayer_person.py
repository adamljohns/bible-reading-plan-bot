#!/usr/bin/env python3
"""PJG-0910-PEACE1 — rewrite the praying subject in baked Evening Peace prayers.

The Principal's ear failed the 2026-09-10 Peace prayer: it opened "Grant me"
and then slid into "our wives and children ... convict us ... we have failed".
The generator gate now refuses that shape on NEW generation, but days already
baked into docs/assets/readings/*.json keep their corporate text.

This is a MECHANICAL person rewrite of the existing prayer, not new authorship.
Passage-specific petitions are preserved word for word; only the pray-er moves
from first-person plural to first-person singular.

"our" inside a divine title ("Christ our King") is the mandated close, not a
corporate pray-er, so those phrases are protected before anything is rewritten
and restored afterwards.

Dry run (default) prints what would change and writes nothing:
    python3 bin/peace_prayer_person.py --from 2026-09-12 --to 2026-12-31
Apply:
    python3 bin/peace_prayer_person.py --from 2026-09-12 --to 2026-12-31 --apply
"""
import argparse
import glob
import json
import os
import re

READINGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "docs", "assets", "readings")

PRAYER_BLOCK = re.compile(r"(🙏[^\n]*\n\n)([\s\S]*?)(\n\n🛡️)")

# Close titles. These carry "our" legitimately and must survive untouched.
DIVINE_TITLE = re.compile(
    r"\bour\s+(?:Lord\s+Jesus\s+Christ|Lord\s+Jesus|Lord|God|King|Christ|Jesus|"
    r"Savior|Saviour|Redeemer|Father|Shepherd|Master|Rock|Refuge|Judge|Maker|Creator)\b"
    # "our God-given duties" / "our God-ordained roles" are NOT address to God;
    # the pray-er is still plural there and must be rewritten.
    r"(?!-)",
    re.I,
)
SENTINEL = "@@DIVINE%d@@"

# Ordered: longest / most specific first, so "our home" cannot pre-empt
# "our homes" and leave a dangling plural.
PAIRS = [
    (r"\bour communities\b", "my community"),
    (r"\bour community\b", "my community"),
    (r"\bour families\b", "my family"),
    (r"\bour family\b", "my family"),
    (r"\bour homes\b", "my home"),
    (r"\bour home\b", "my home"),
    (r"\bour lives\b", "my life"),
    (r"\bour life\b", "my life"),
    (r"\bour wives\b", "my wife"),
    (r"\bour children\b", "my children"),
    (r"\bour neighbors\b", "my neighbors"),
    (r"\bour neighbours\b", "my neighbours"),
    (r"\bour actions\b", "my actions"),
    # Singular-per-person nouns. "our hands"/"our eyes" stay plural, because
    # one man still has two of each; "our minds" must not become "my minds".
    (r"\bour minds\b", "my mind"),
    (r"\bour hearts\b", "my heart"),
    (r"\bour souls\b", "my soul"),
    (r"\bour spirits\b", "my spirit"),
    (r"\bour wills\b", "my will"),
    (r"\bour tongues\b", "my tongue"),
    (r"\bour voices\b", "my voice"),
    (r"\bour households\b", "my household"),
    (r"\bour marriages\b", "my marriage"),
    (r"\bGrant us\b", "Grant me"),
    (r"\bconvict us\b", "convict me"),
    (r"\bstrengthen us\b", "strengthen me"),
    (r"\ballow us\b", "allow me"),
    (r"\bwe have failed\b", "I have failed"),
    (r"\bwe confess\b", "I confess"),
    (r"\bwe thank\b", "I thank"),
    (r"\bwe ask\b", "I ask"),
    (r"\bwe acknowledge\b", "I acknowledge"),
    (r"\bwe have\b", "I have"),
    (r"\bwe do\b", "I do"),
    (r"\bwe are\b", "I am"),
    (r"\bwe were\b", "I was"),
    (r"\bwe may\b", "I may"),
    (r"\bwe would\b", "I would"),
    (r"\bwe\b", "I"),
    (r"\bus\b", "me"),
    (r"\bours\b", "mine"),
    (r"\bour\b", "my"),
    # Role lists that belong to the now-singular pray-er. Without these,
    # "our duties as husbands, fathers, and citizens" lands as "my duties as
    # husbands, fathers, and citizens" — one man, three plurals.
    # Corporate-identity idiom ("as citizens of heaven") is deliberately left
    # plural: it describes the church, not the pray-er's own offices.
    (r"\bas husbands, fathers, and citizens\b", "as a husband, father, and citizen"),
    (r"\bas husbands, fathers and citizens\b", "as a husband, father and citizen"),
    (r"\bas husbands, fathers, and men of God\b", "as a husband, father, and man of God"),
    (r"\bas fathers and husbands\b", "as a father and husband"),
    (r"\bas husbands and fathers\b", "as a husband and father"),
    (r"\bas citizens and servants\b", "as a citizen and servant"),
]


def rewrite_prayer(pray):
    """Return the prayer with the praying subject in first-person singular."""
    titles = []

    def stash(m):
        titles.append(m.group(0))
        return SENTINEL % (len(titles) - 1)

    out = DIVINE_TITLE.sub(stash, pray)
    for pat, repl in PAIRS:
        # Match case-insensitively so a sentence-initial "We confess" / "Our
        # homes" is caught, then restore the original capitalisation. A
        # lowercase-only pass left 20 days half-rewritten on the first run.
        def sub(m, repl=repl):
            return repl[0].upper() + repl[1:] if m.group(0)[0].isupper() else repl
        out = re.sub(pat, sub, out, flags=re.I)
    # "I" as a verb subject can leave "I has/have" style agreement damage only
    # where the source said "we have"; that pair is handled above. Guard the
    # common leftovers rather than silently shipping bad grammar.
    out = re.sub(r"\bI has\b", "I have", out)
    out = re.sub(r"\bmy own selves\b", "myself", out)
    for i, t in enumerate(titles):
        out = out.replace(SENTINEL % i, t)
    return out


def is_corporate(pray):
    """True when a first-person plural is still acting as the pray-er."""
    return bool(re.search(r"\b(?:we|us|our|ours)\b", DIVINE_TITLE.sub("", pray), re.I))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--to", dest="end", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    changed, skipped, failed = [], 0, []
    for path in sorted(glob.glob(os.path.join(READINGS, "*.json"))):
        day = os.path.basename(path)[:10]
        if not (a.start <= day <= a.end):
            continue
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        doc = json.loads(raw)
        peace = doc.get("watches", {}).get("peace")
        if not peace or not peace.get("text"):
            continue
        m = PRAYER_BLOCK.search(peace["text"])
        if not m:
            continue
        pray = m.group(2)
        if not is_corporate(pray):
            skipped += 1
            continue
        new_pray = rewrite_prayer(pray)
        if is_corporate(new_pray):
            failed.append(day)          # refuse to ship a half-fixed prayer
            continue
        peace["text"] = peace["text"][:m.start()] + m.group(1) + new_pray + m.group(3) + peace["text"][m.end():]
        changed.append(day)
        if a.apply:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(doc, indent=1, ensure_ascii=False))

    print(f"{'APPLIED' if a.apply else 'DRY RUN'}: {len(changed)} rewritten, "
          f"{skipped} already first-person, {len(failed)} refused")
    if failed:
        print("REFUSED (still corporate after rewrite — hand these to PJ):")
        for d in failed:
            print("   ", d)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
