#!/usr/bin/env python3
"""Regression suite for the translation-doublet check in check_scripture_loops.py.

MBP-1007-SPRINT: the near-duplicate check flagged Scripture that really does
repeat itself — Isaiah 40:7-8 ("the grass withers, the flower fades" twice)
and the Psalm 67:3/5 refrain. A repeat is now excused only when the shared
phrase occurs at least twice in the canonical passage. Both directions are
pinned: genuine repeats pass, and invented doublets still fail.

Run: python3 scripts/test_scripture_loops.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from check_scripture_loops import check_watch  # noqa: E402


def wrap(passage: str, block: str) -> str:
    return f"📖 Scripture — {passage}\n{block}\n⸻\n🙏 Prayer\nAmen."


# (name, passage, scripture_block) — must come back with no doublet hit.
MUST_PASS = [
    (
        "isaiah40_grass_withers",
        "Isaiah 40:1-11",
        "All flesh is grass,\n"
        "And all its glory is like the flower of the field.\n"
        "The grass withers, the flower fades,\n"
        "Because the breath of the LORD blows on it;\n"
        "Surely the people are grass.\n"
        "The grass withers, the flower fades,\n"
        "But the word of our God stands forever.",
    ),
    (
        "psalm67_refrain",
        "Psalm 67",
        "That Your way may be known on earth, Your saving power among all nations.\n"
        "Let the peoples praise You, O God; let all the peoples praise You.\n"
        "Let the nations be glad and sing for joy, for You judge the peoples "
        "with equity and guide the nations on earth.\n"
        "Selah.\n"
        "Let the peoples praise You, O God; let all the peoples praise You.\n"
        "Then the land will yield its increase, and God, our God, will bless us.",
    ),
]

# (name, passage, scripture_block) — must still raise translation_doublet.
MUST_FLAG = [
    (
        "proverbs15_soft_gentle_doublet",
        "Proverbs 15",
        "A soft answer turns away wrath, but a harsh word stirs up anger.\n"
        "A gentle answer turns away wrath, but a harsh word stirs up anger.\n"
        "The tongue of the wise uses knowledge rightly.",
    ),
    (
        "psalm67_invented_repeat",
        # The refrain is canonical; a repeated line 1 is not.
        "Psalm 67",
        "May God be gracious to us and bless us and cause His face to shine upon us.\n"
        "Selah.\n"
        "May God be gracious to us and bless us and cause His face to shine upon us.\n"
        "That Your way may be known on earth, Your saving power among all nations.",
    ),
    (
        "unresolvable_label_keeps_old_behaviour",
        "Isaiah 99",
        "The grass withers, the flower fades,\n"
        "Surely the people are grass.\n"
        "The grass withers, the flower fades,",
    ),
]


def doublets(passage: str, block: str) -> list[dict]:
    fails = check_watch("2099-01-01", "t", passage, wrap(passage, block), None)
    return [f for f in fails if f["code"] == "translation_doublet"]


def main() -> int:
    bad = 0
    for name, passage, block in MUST_PASS:
        hits = doublets(passage, block)
        ok = not hits
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} pass {name}" + ("" if ok else f" -> {hits[0]['bleed']}"))
    for name, passage, block in MUST_FLAG:
        ok = bool(doublets(passage, block))
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} flag {name}")
    total = len(MUST_PASS) + len(MUST_FLAG)
    print(f"{total - bad}/{total} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
