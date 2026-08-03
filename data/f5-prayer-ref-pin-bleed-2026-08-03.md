# F5 prayer PIN/studio bleed — 2026-08-03 (PJG-0803-PIN1)

## Symptom
Adam ear-QA: prayer-clone voice interjected studio/PIN copy (~3× per prayer) on today's watches:
location-list + "not a public website" + PIN phrase (fit20 Studio Command class).

## Contaminated (pre-fix whisper scan)
ALL five 2026-08-03 watches: wisdom, husband, father, citizen, peace.
Bleed confined to Adam-clone **prayer** segments (F5 path), not narrator/scripture.

## Root cause
`~/.openclaw/voice/f5tts-tests/ref-calm.txt` contained Studio Command dashboard copy
instead of Psalm 23. `ref-calm.wav` was **missing** from the TCC-safe dir (only bad txt + README).
`generate-watch-audio.py` resolved DEFAULT txt (poison) and fell through / failed closed poorly
until wav was restored; F5 `--ref-text` is concatenated conditioning → product copy leaked into prayer TTS.

Related: PJG-0802-AUD2 (wrong/substitute ref); shared-memory `f5-prayer-ref-tcc-2026-08-02.md`.

## Fix
1. Restored canonical pair from `~/Documents/05-Voice/f5tts-tests/ref-calm.{wav,txt}` (Psalm 23).
2. Quarantined poison txt as `ref-calm.txt.BAD-fit20-studio-command-20260803`.
3. Regenerated all five 2026-08-03 watches with clean ref; post-bake whisper ban-scan CLEAN.
4. Hard gate `scripts/check_f5_prayer_ref.py` — pre-bake (adam_prayer_ready + render_f5_text) and D-1 cadence.
5. LOOP1 Malachi wisdom text fix already live; wisdom audio re-baked again on clean ref.

## Never again
ONLY `~/.openclaw/voice/f5tts-tests/ref-calm.*` for prayer clone. Never Studio Command, location lists, PIN scripts.
