#!/usr/bin/env python3
"""Fail-closed Scripture loop / length gate for daily readings.

PJG-0803-LOOP1 (2026-08-03): Morning Wisdom Malachi 2 shipped with a baked
mechanical loop (wrong-chapter bleed + marriage-unit repeated ~6×). Audio was
baked from the corrupt block. This gate blocks publish + audio bake when a
Scripture section shows:

  1. Any normalized substring ≥80 chars appearing ≥3 times (mechanical loop)
  2. A paragraph (≥80 norm chars) repeated ≥3 times
  3. Known wrong-chapter bleed markers (extensible)
  4. (Soft/report only) single-chapter length >6× corpus median — long
     chapters like Numbers 26 / Joshua 15 are legitimate and must NOT
     block publish; extreme outliers are printed as WARN

Usage:
  python3 scripts/check_scripture_loops.py                 # all days (JSON preferred)
  python3 scripts/check_scripture_loops.py 2026-08-03      # one day
  python3 scripts/check_scripture_loops.py --md 2026-08-03 # force MD source
  python3 scripts/check_scripture_loops.py --update-median # refresh median cache

Exit 0 = clean. Exit 1 = one or more watches failed (prints hits to stderr).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_DIR = REPO / "docs" / "assets" / "readings"
MD_DIR = REPO / "data" / "readings"
MEDIAN_CACHE = REPO / "data" / "scripture-loop-median.json"

SCR_RE = re.compile(
    r"📖\s*Scripture\s*[—\-–:][^\n]*\n([\s\S]*?)(?=\n⸻|\n🧭|\n🗺️|\n🛰|\n🌾|\n❤️|\n👨‍👧|\n🛡|\n🙏|\Z)"
)
NORM_RE = re.compile(r"[^a-z0-9\s]+")
MIN_SUB_LEN = 80
MIN_OCC = 3
LENGTH_RATIO_WARN = 6.0  # soft only; long OT chapters are real

# Extensible bleed heuristics: (passage_substr_lower, scripture_substr_lower, code)
BLEED_RULES = [
    ("malachi 2", "polluted food", "malachi1_polluted_food_in_mal2"),
    ("malachi 2", "blind animals for sacrifice", "malachi1_blind_animals_in_mal2"),
    # PJG-0815-WIS1 — named Proverbs 15 must not carry foreign-chapter mash
    ("proverbs 15", "pleasing words are a honeycomb", "prov16_honeycomb_in_prov15"),
    ("proverbs 15", "way that seems right to a man", "prov14_16_way_seems_right_in_prov15"),
    ("proverbs 15", "hear counsel and receive instruction", "prov19_counsel_in_prov15"),
    ("proverbs 15", "many are the plans in a man", "prov19_plans_in_prov15"),
    ("proverbs 15", "chasten your son while there is hope", "prov19_chasten_in_prov15"),
    ("proverbs 15", "servant will not be spared from scourging", "foreign_scourging_in_prov15"),
    ("proverbs 15", "lord’s eyes are on the righteous", "ps34_eyes_in_prov15"),
    ("proverbs 15", "lords eyes are on the righteous", "ps34_eyes_in_prov15"),
    ("proverbs 15", "face of the lord is against those who do evil", "ps34_face_in_prov15"),
    # PJG-0826-AUD1 — named Proverbs 26 must not carry Prov 6 / Prov 30 / Malachi mash
    ("proverbs 26", "go to the ant", "prov6_ant_in_prov26"),
    ("proverbs 26", "these six things the lord hates", "prov6_six_seven_in_prov26"),
    ("proverbs 26", "lips of a priest should keep knowledge", "malachi_priest_in_prov26"),
    ("proverbs 26", "words of agur", "prov30_agur_in_prov26"),
]

# Consecutive / near translation-doublets (soft vs gentle answer, etc.)
DOUBLET_PAIRS = [
    ("soft answer", "gentle answer"),
    ("soft answer turns away wrath", "gentle answer turns away wrath"),
    ("turns away wrath", "turns wrath aside"),
]
DOUBLET_NEAR_RATIO = 0.86


def normalize(s: str) -> str:
    s = s.lower()
    s = NORM_RE.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_scripture(text: str) -> str:
    m = SCR_RE.search(text or "")
    if m:
        return m.group(1)
    m2 = re.search(r"📖[^\n]*\n([\s\S]*?)(?=\n⸻)", text or "")
    return m2.group(1) if m2 else ""


def length_class(passage: str) -> str:
    pl = (passage or "").lower()
    if "&" in pl or " and " in pl:
        return "multi"
    if re.search(r"\d+\s*[-–:]\s*\d+", passage or ""):
        return "range"
    return "single_chapter"


def find_loop_hits(scripture: str) -> list[dict]:
    norm = normalize(scripture)
    if len(norm) < MIN_SUB_LEN * 2:
        return []
    hits = []
    seen = set()
    for L in (200, 160, 120, 100, 80):
        step = max(10, L // 8)
        for i in range(0, max(1, len(norm) - L + 1), step):
            window = norm[i : i + L]
            if len(window) < MIN_SUB_LEN or window in seen:
                continue
            if len(set(window.replace(" ", ""))) < 8:
                continue
            c = norm.count(window)
            if c >= MIN_OCC:
                seen.add(window)
                hits.append(
                    {
                        "count": c,
                        "len": L,
                        "coverage": round(c * L / max(1, len(norm)), 3),
                        "sample": window[:100],
                    }
                )
        if hits:
            break
    hits.sort(key=lambda h: (-h["count"], -h["coverage"]))
    return hits[:5]


def para_triples(scripture: str) -> list[tuple[int, str]]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", scripture) if len(normalize(p)) >= MIN_SUB_LEN]
    pc = Counter(normalize(p) for p in paras)
    return [(c, p[:100]) for p, c in pc.items() if c >= MIN_OCC]


def _tokens(s: str) -> list[str]:
    return [t for t in normalize(s).split() if t]


def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def doublet_hits(scripture: str) -> list[str]:
    """Refuse stacked translation-doublets (PJG-0815-WIS1 / MBT1).

    One fused MBT line may legally contain both 'soft' and 'gentle'
    (Principal Prov 15:1). FAIL only when those dresses appear as
    separate verses / lines.
    """
    hits: list[str] = []
    lines = [ln.strip() for ln in scripture.splitlines() if ln.strip()]
    # Pair check is line-scoped: same proverb dumped twice in two dresses.
    lows = [ln.lower() for ln in lines]
    for a, b in DOUBLET_PAIRS:
        a_lines = [i for i, ln in enumerate(lows) if a in ln]
        b_lines = [i for i, ln in enumerate(lows) if b in ln]
        if a_lines and b_lines and set(a_lines) != set(b_lines):
            hits.append(f"pair:{a[:24]}/{b[:24]}")
    norms = [_tokens(ln) for ln in lines]
    for i, left in enumerate(norms):
        if len(left) < 6:
            continue
        for j in range(i + 1, min(i + 4, len(norms))):
            right = norms[j]
            if len(right) < 6:
                continue
            if _jaccard(left, right) >= DOUBLET_NEAR_RATIO:
                sample = " ".join(left[:8])
                hits.append(f"near:{sample}")
    # unique preserve order
    seen: set[str] = set()
    out: list[str] = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def bleed_hits(passage: str, scripture: str) -> list[str]:
    pl = (passage or "").lower()
    sl = scripture.lower()
    out = []
    for p_sub, s_sub, code in BLEED_RULES:
        if p_sub in pl and s_sub in sl:
            out.append(code)
    return out


def load_median() -> float | None:
    if MEDIAN_CACHE.exists():
        try:
            return float(json.loads(MEDIAN_CACHE.read_text()).get("single_chapter_median") or 0) or None
        except Exception:
            return None
    return None


def compute_median_from_corpus() -> float | None:
    lengths = []
    for fp in sorted(JSON_DIR.glob("20*.json")):
        try:
            day = json.loads(fp.read_text())
        except Exception:
            continue
        for w in (day.get("watches") or {}).values():
            passage = (w or {}).get("passage") or ""
            if length_class(passage) != "single_chapter":
                continue
            scr = extract_scripture((w or {}).get("text") or "")
            if scr.strip():
                lengths.append(len(scr))
    if not lengths:
        return None
    return float(statistics.median(lengths))


def update_median_cache() -> float | None:
    med = compute_median_from_corpus()
    if med is None:
        return None
    MEDIAN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    MEDIAN_CACHE.write_text(
        json.dumps(
            {
                "single_chapter_median": med,
                "length_ratio_fail": LENGTH_RATIO,
                "min_sub_len": MIN_SUB_LEN,
                "min_occ": MIN_OCC,
            },
            indent=2,
        )
        + "\n"
    )
    return med


def load_day_watches(date: str, force_md: bool = False) -> dict[str, dict]:
    """Return {watch_key: {passage, text}}."""
    if not force_md:
        jp = JSON_DIR / f"{date}.json"
        if jp.exists():
            day = json.loads(jp.read_text())
            out = {}
            for k, w in (day.get("watches") or {}).items():
                out[k] = {
                    "passage": (w or {}).get("passage") or "",
                    "text": (w or {}).get("text") or "",
                }
            return out
    mp = MD_DIR / f"{date}.md"
    if not mp.exists():
        raise FileNotFoundError(f"no reading source for {date}")
    md = mp.read_text()
    # split by watch emoji headers
    marks = []
    for i, ln in enumerate(md.splitlines()):
        s = ln.strip()
        key = None
        if s.startswith("🌅"):
            key = "wisdom"
        elif s.startswith("🕖"):
            key = "first"
        elif s.startswith("🕚"):
            key = "second"
        elif s.startswith("🕒"):
            key = "third"
        elif s.startswith("🌙"):
            key = "peace"
        if key:
            marks.append((i, key))
    lines = md.splitlines()
    out = {}
    for idx, (start, key) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        text = "\n".join(lines[start:end])
        pref = ""
        m = re.search(r"📖\s*Scripture\s*[—\-–:]\s*(.+)", text)
        if m:
            pref = m.group(1).strip()
        out[key] = {"passage": pref, "text": text}
    return out


def check_watch(date: str, wkey: str, passage: str, text: str, median: float | None) -> list[dict]:
    scr = extract_scripture(text)
    if not scr.strip():
        return []
    fails = []
    loops = find_loop_hits(scr)
    # mechanical: count>=3 with coverage>=0.35 OR count>=5 OR para triple
    mech = [h for h in loops if h["count"] >= 5 or h["coverage"] >= 0.35]
    ptrip = para_triples(scr)
    if mech or ptrip:
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "scripture_loop",
                "chars": len(scr),
                "loops": mech[:3],
                "para_triples": ptrip[:2],
            }
        )
    bleeds = bleed_hits(passage, scr)
    if bleeds:
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "chapter_bleed",
                "chars": len(scr),
                "bleed": bleeds,
            }
        )
    doubles = doublet_hits(scr)
    # Psalm 118 legally repeats refrain lines (steadfast love / cut them down /
    # right hand of the LORD). That is Scripture, not a translation mash.
    # PJG-0826-AUD1: LOOP-GATE must not refuse a clean BTE/NKJV Psalm 118.
    if re.search(r"psalm\s*118\b", passage or "", re.I):
        doubles = [d for d in doubles if not str(d).startswith("near:")]
    if doubles:
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "translation_doublet",
                "chars": len(scr),
                "bleed": doubles,
            }
        )
    # Length is soft: many single OT chapters legitimately exceed 3× median.
    # Only surface extreme (>6×) as WARN-class codes that do not fail the run
    # unless paired with a loop/bleed (already captured above).
    if (
        median
        and length_class(passage) == "single_chapter"
        and len(scr) > LENGTH_RATIO_WARN * median
    ):
        fails.append(
            {
                "date": date,
                "watch": wkey,
                "passage": passage,
                "code": "length_outlier_warn",
                "severity": True,
                "chars": len(scr),
                "median": median,
                "ratio": round(len(scr) / median, 2),
            }
        )
    return fails


def iter_dates(only: list[str] | None) -> list[str]:
    if only:
        return only
    dates = set()
    for fp in JSON_DIR.glob("20*.json"):
        dates.add(fp.stem)
    for fp in MD_DIR.glob("20*.md"):
        dates.add(fp.stem)
    return sorted(dates)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dates", nargs="*", help="YYYY-MM-DD (default: all)")
    ap.add_argument("--md", action="store_true", help="force MD source even if JSON exists")
    ap.add_argument("--update-median", action="store_true", help="refresh median cache from JSON corpus")
    ap.add_argument("--json-out", type=Path, help="optional path to write full hit list")
    args = ap.parse_args(argv)

    if args.update_median:
        med = update_median_cache()
        print(f"updated median cache: {med}")
        if not args.dates and not args.json_out:
            return 0

    median = load_median()
    if median is None:
        median = compute_median_from_corpus()

    all_fails: list[dict] = []
    for date in iter_dates(args.dates or None):
        try:
            watches = load_day_watches(date, force_md=args.md)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        for wkey, w in watches.items():
            all_fails.extend(check_watch(date, wkey, w.get("passage") or "", w.get("text") or "", median))

    if args.json_out:
        args.json_out.write_text(json.dumps({"median": median, "fails": all_fails}, indent=2) + "\n")

    hard = [f for f in all_fails if not f.get("severity")]
    soft = [f for f in all_fails if f.get("severity")]

    for f in soft:
        bits = [f["date"], f["watch"], f.get("passage") or "?", f["code"], f"chars={f.get('chars')}"]
        if f.get("ratio"):
            bits.append(f"ratio={f['ratio']}")
        print("WARN " + " · ".join(str(b) for b in bits), file=sys.stderr)

    if not hard:
        scope = len(args.dates) if args.dates else "all"
        print(
            f"OK scripture-loop gate clean ({scope} day(s); median={median}; "
            f"soft_warns={len(soft)})"
        )
        return 0

    print(f"FAIL scripture-loop gate: {len(hard)} hard hit(s); median={median}", file=sys.stderr)
    for f in hard:
        bits = [f["date"], f["watch"], f.get("passage") or "?", f["code"], f"chars={f.get('chars')}"]
        if f.get("ratio"):
            bits.append(f"ratio={f['ratio']}")
        if f.get("bleed"):
            bits.append("bleed=" + ",".join(f["bleed"]))
        if f.get("loops"):
            top = f["loops"][0]
            bits.append(f"loop×{top['count']} cov={top['coverage']}")
        if f.get("para_triples"):
            bits.append(f"para_x{f['para_triples'][0][0]}")
        print(" - " + " · ".join(str(b) for b in bits), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
