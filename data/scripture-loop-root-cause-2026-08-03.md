# Scripture loop root cause — 2026-08-03 (PJG-0803-LOOP1)

## Symptom
Morning Wisdom Malachi 2 live text repeated the marriage-covenant unit ~6×, opened mid-stream at Mal 2:17, and bled Malachi 1 polluted-offering / blind-animal material into a Malachi 2 watch. Contaminated wisdom MP3 was already live (has_audio true).

## Not the cause
- BTE chapter source `docs/assets/chapters/39_2.json` NKJV 1–17 was clean (no dups).
- HTML renderer did not invent the loop — JSON/MD source already contained it.
- Other 2026-08-03 watches (first/second/third/peace) were clean on manual read.

## Likely assembly class
Authoring path that writes `watches.*.text` Scripture blocks (day MD → JSON via `build_reading_index.py`):
1. Incomplete / wrong-chapter slice from BTE (Mal 1 fragments + Mal 2:17 open), **and**
2. Retry/append of the marriage-covenant unit without replacing the block (fill-loop), **and/or**
3. A generator that concatenates partial pulls until a length target is met.

Exact generator function not pinned this turn (multiple historical authoring paths: F5 watch gen, local reading gen, manual MD). Gate fails closed regardless of which writer misfires.

## Fix shipped this turn
1. Replace 2026-08-03 wisdom Scripture with single clean BTE NKJV Malachi 2:1–17; scrub doubled prayer close; rebuild HTML/JSON; regen wisdom MP3 only.
2. Corpus mechanical-loop scan over all `docs/assets/readings/*.json`; auto-fix clear loops:
   - 2026-06-26 first — Jeremiah 29 (false-prophet unit ×5)
   - 2026-09-26 wisdom — Proverbs 26 (fool-simile unit ×3)
3. Hard gate: `scripts/check_scripture_loops.py` wired into:
   - `bin/generate-watch-audio.py` (pre-bake)
   - `scripts/publish_reading.sh` (pre-publish)
   - `~/Scripts/pj-day-prior-watch-audio.sh` (D-1 cadence)

## Owner
Max (engineering gate) · Pastor John (content QA after ship)
