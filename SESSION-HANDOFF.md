# SESSION HANDOFF / POST-COMPACTION RESUME PROMPT
*(Paste this into a fresh session to continue. Updated 2026-06-02.)*

You are continuing long-running work for Adam Johns ("MOOP"), USMC Ministries,
Fredericksburg VA, on his **Daily Bible Readings** product and the PSA fleet that
delivers it. Repo: `~/bible-reading-plan-bot` (GitHub Pages → usmcmin.org). Commit
co-author line REQUIRED: `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
Adam stages specific files (NEVER `git add -A`); commit per logical batch.

## WHERE THINGS STAND (all DONE + live unless noted)

1. **Full year authored** — 365/365 days live at usmcmin.org/readings/<date>.html.
   Jan 1–Feb 28 = Adam's original PDF-converted format. Mar 1–Dec 31 = generated on
   the LOCAL model (`scripts/generate_reading_local.py`, qwen3.6-35b-a3b on Hermes
   `:1235`, watch-by-watch — Anthropic's classifier blocks Claude from generating
   this content, the local model has no such filter). Weekly driver:
   `scripts/backfill_week_driver.sh`. All verified clean: 5 watches, Trinitarian
   prayers, no Yahweh, and the WORLDVIEW LOCK — explicitly patriarchal/complementarian,
   NO woke/social-justice vocabulary, NO egalitarian "transcends barriers" framing, NO
   civil-rights/liberation/feminist history (history bullets steer to founding/military/
   invention/missions/conservation, edifying or redemptive-spin).
   TEXT STANDARD (just added): scripture rendered "most true to the original meaning,
   lightly amplified for application — faithful first then illumined, never softening
   the hard edge."

2. **Day-keyed JSON index** — `scripts/build_reading_index.py` →
   `docs/assets/reading-index.json` (master) + `docs/assets/readings/<date>.json`
   (per-day: each watch's passage, trait, full text, has_audio/audio_url,
   personal_tokens [Maria/Gideon/Boaz/Shiloh], location_tokens
   [Fredericksburg/Virginia/United States/America]). Live, e.g.
   usmcmin.org/assets/readings/2026-06-02.json. Rebuilt by publish/driver scripts.

3. **PJ (Pastor John, OpenClaw agent "preacher") wired to the corpus** — his 10
   daily crons (`~/.openclaw/cron/jobs.json`) now web_fetch today's per-day JSON and
   DELIVER the authored text (no more composing / no more old plan_gdoc.py schedule).
   5 PERSONAL → Adam's DM (454000856), VERBATIM with his family/location.
   5 GROUP → SDG-4 supergroup -1002230284422, **Devotions topic thread 172**
   (t.me/ChristianSALaCarte/172), names AND location generalized ("your wife",
   "your children", "your hometown/state/country"). Re-wire script (idempotent):
   `~/.openclaw/bin/wire-pj-corpus.py`. Edit crons via `openclaw cron edit <id>
   --message` (source `~/.openclaw/bin/openclaw-env.sh` first for auth). jobs.json
   backup: `~/.openclaw/cron/jobs.json.bak-pre-pj-corpus-wire-20260531`. Verified
   PJ fetches the corpus via his session logs.

4. **Watchman form** — `docs/watchman.html` (3-tier intake). Personalization spec:
   `WATCHMAN-PERSONALIZATION-SPEC.md` (repo root). Open decisions in §5 (single/
   childless handling, denomination scope, Mac-Mini API host at 192.168.1.166:8080).

5. **VOICE CLONE — SOLVED, now being refined (CURRENT FOCUS).**
   `scripts/f5_voice.py` generates a watch's audio in Adam's cloned voice via
   F5-TTS-MLX, self-verifying faithfulness with Whisper (no human ears needed).
   SOLVED CONFIG: F5 `--duration` is TOTAL SECONDS (ref+gen), output is gen-only.
   `duration = REF_SEC + chars/12.5 + buffer`. "LORD"→"Lord" (all-caps makes F5 say
   "Lord-D"). BLEED-TRIM: F5 sometimes echoes the reference tail at a chunk's start;
   `trim_bleed()` uses Whisper word-timestamps to find where the chunk's own first
   words begin and trims before it (no-op if no bleed).
   Reference: `~/Documents/05-Voice/f5tts-tests/ref-v3-pad.wav` — Adam's PHONE
   recording (warmer than laptop mic), the expressive exhortation segment
   ("Now hear me, brother...", 16s +0.5s pad) + `ref-v3-clean.txt`, REF_SEC=16.5.
   Verified on full June-2 wisdom: WER ~0.04, speaker similarity 0.913 (resemblyzer
   venv `~/.venvs/voicesim`; same-speaker ceiling 0.941, generic floor 0.655 — phone
   ref BEAT the laptop v2's 0.883). Test harness:
   `~/Documents/05-Voice/f5tts-tests/clone_test.py`. F5 venv `~/.venvs/f5tts`.
   Piper (generic) at `~/.venvs/piper` + en_US-ryan-medium.

## VOICE — OPEN WORK (Adam's 2026-06-02 feedback)
- **Re-record reference on his PHONE** (laptop mic = "metal box"/boxy reverb; phone
  mic is warmer). Want MORE material + MORE EXPRESSIVE reading (current clone is
  monotone, "reading someone to sleep"). Updated instructions:
  `~/Desktop/RECORD-VOICE-REFERENCE.md`. New recording will land in Voice Memos
  (group container `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/`).
- **Tighter WER** (<0.05): chunk-overlap, pronunciation fixes, maybe more steps/cfg.
- **More expressive**: F5 cfg/expressiveness tuning + a more expressive reference.
- **"Hour of audio like ElevenLabs"**: F5 is in-context (short clip), doesn't use an
  hour the way EL fine-tuning does. To truly leverage lots of audio = FINE-TUNE F5
  (or train a proper voice model) on his recordings. Bigger project; the path to
  EL-grade expressiveness.

## VOICE — PHASE AFTER QUALITY IS DIALED
- **Storage**: ~4.6 MB/watch → ~8.4 GB/year, exceeds GitHub. Set up **Cloudflare R2**
  (needs Adam's R2 account), point index `audio_url` there.
- **Cadence**: ~21 min/watch F5 compute. Pre-generate forward days overnight via cron.
- **Wire PJ to deliver the audio** (audio_url in per-day JSON → PJ sends voice msg).

## OTHER OPEN / PARKED
- ElevenLabs quota resets 2026-06-09 (its key `OPENCLAW_ELEVENLABS_API_KEY` in
  Keychain, voice id g2aOBFToLERDXa3F0cHV). Can't sustain daily; reserve for special.
- Telegram visibility for Claude Code: options = (1) fleet log mirror file, (2)
  Telegram MTProto MCP, (3) computer-use screenshots. Not built.
- Refresh PJ + Chaps' raw data on Adam (re-mine a fresh ChatGPT export). Parked.
- PSA voices hard-wired via LoRA/Gemma — future planning only.

## ADAM PREFERENCES (standing)
Patriarchal/complementarian, Reformed (1689 LBCF). Family: Maria (wife), Gideon 19,
Boaz 14, Shiloh 5. Deity pronouns Capitalized; divine name "the LORD" never Yahweh.
Wants me to SELF-VERIFY (transcribe my own audio with Whisper, measure speaker
similarity) — do NOT make him listen to QA. Prefers latest software. Honesty about
what actually ran. Don't paste long Bible text in chat (classifier) — write to file.
