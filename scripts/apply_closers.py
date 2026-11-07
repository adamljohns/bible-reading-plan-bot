#!/usr/bin/env python3
"""Apply new watch closers and varied prayer openings to readings markdown (Principal 2026-11-07).

  python3 scripts/apply_closers.py closers.json [closers2.json ...]

closers.json: {"YYYY-MM-DD": {"wisdom": {"label","text"}, "husband": {"text"}, "father": {"text"},
               "citizen": {"text"}, "peace": {"label","text"}}}

Rules applied to data/readings/<date>.md:
  - Morning Wisdom closes with a wisdom label (🔑), Evening Peace with a peace label (🕊️);
    the three watches keep 🛡️ Watch Charge.
  - A prayer that opens "Father," gets a rotating address so the five prayers of a day,
    and the same watch on consecutive days, do not all open the same way.
Rebuild pages and JSON afterward with build_reading_page_from_md.py and build_reading_index.py.
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = ["wisdom", "husband", "father", "citizen", "peace"]
HEADERS = re.compile(r"^(🌅|🕖|🕚|🕒|🌙)")
CLOSER = re.compile(r"^\s*(?:🛡️?|⚓|🔑|🕊️?)\s*(?:Watch Charge|Helm Command|Rudder Steer|The Charge|"
                    r"Wisdom Key|Wise Takeaway|Key to Wisdom|Word to the Wise|Wisdom to Carry|"
                    r"Prompt for Peace|Peaceful Focus|Evening Reminder|Rest in This|Peace to Carry)\s*:")
PRAYER_HDR = re.compile(r"^\s*🙏")
ADDRESSES = ["Heavenly Father", "Dear Lord", "Father God", "God on High", "Lord God",
             "Dear Heavenly Father", "Almighty God", "Father"]
ICON = {"wisdom": "🔑", "peace": "🕊️"}


def address_for(date, watch_i):
    day = datetime.date.fromisoformat(date).toordinal()
    return ADDRESSES[(day * 3 + watch_i) % len(ADDRESSES)]


def apply_day(date, spec):
    path = ROOT / "data" / "readings" / f"{date}.md"
    lines = path.read_text(encoding="utf-8").split("\n")
    watch_i = -1
    in_prayer = False
    out, done_closer, done_open = [], set(), set()
    skip_cont = False
    for line in lines:
        if HEADERS.match(line):
            watch_i += 1
            in_prayer = False
        key = ORDER[watch_i] if 0 <= watch_i < 5 else None
        if skip_cont:
            if line.strip():
                continue          # drop wrapped continuation of the old closer
            skip_cont = False
        if key and CLOSER.match(line):
            item = spec[key]
            label = item.get("label") or "Watch Charge"
            icon = ICON.get(key, "🛡️")
            out.append(f"{icon} {label}: {item['text'].strip()}")
            done_closer.add(key)
            skip_cont = True
            in_prayer = False
            continue
        if key and PRAYER_HDR.match(line):
            in_prayer = True
            out.append(line)
            continue
        if key and in_prayer and line.strip() and key not in done_open:
            done_open.add(key)
            m = re.match(r"^(\s*)Father,\s*(.*)$", line)
            if m:
                rest = m.group(2)
                addr = address_for(date, watch_i)
                if re.match(r"(God|Lord)\b", rest) and addr not in ("Heavenly Father", "Father"):
                    addr = "Heavenly Father"
                line = f"{m.group(1)}{addr}, {rest}"
        out.append(line)
    missing = [k for k in ORDER if k not in done_closer]
    if missing:
        raise SystemExit(f"{date}: no closer line found for {missing}")
    path.write_text("\n".join(out), encoding="utf-8")


def main():
    spec = {}
    for f in sys.argv[1:]:
        spec.update(json.load(open(f, encoding="utf-8")))
    for date in sorted(spec):
        apply_day(date, spec[date])
    print(f"applied {len(spec)} days")


if __name__ == "__main__":
    main()
