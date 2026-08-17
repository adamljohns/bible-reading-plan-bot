# Worship Dream-Loop Runbook — target 3,777 songs (full songbook count)

SKILL = <repo>/.claude/skills/worship-directory   (this dir; REPO-COMMITTED — never keep loop assets in /tmp scratchpads, they get wiped)
See SKILL.md for the add pipeline (video-linking is a REQUIRED step of every batch).
STATE = SKILL/scripts/state.json
WORKTREE = /Users/moop_bot_pro/bible-reading-plan-bot-worship-sprint  (branch worship-2777, publishes to origin main)

Each burst ≈15 min. Status = 1-2 sentences in transcript. notify-adam.sh (--level report --title --body)
ONLY on: target hit, schedule end, or breakage. Current song count = DB length of docs/data/worship-songs.json
(equals the hero count in the full-songbook view).

## 0. Gates (in order)
1. NOW > STATE.endEpoch → CronDelete the hourly job, final notify, update memory, DONE.
2. STATE.activeWorkflowTaskId set → "wave in flight, skipping", END (the completion handler applies + clears it).
3. count ≥ STATE.target → phase="polish" (see POLISH).
4. NOW < STATE.resumeNotBefore → subagent window dry: run an INLINE lane this burst (chord-lint fixes,
   or a links-only batch via build-linksonly.js if you can name 10+ solid fresh CCM/worship songs), publish, END.

## 1. Lane alternation
STATE.nextLane alternates "grow" ↔ "verify" each burst (set it to the OTHER value when you start a burst).

### GROW lane
1. `cd WORKTREE && git fetch origin main -q && git rebase origin/main` (conflict → abort, continue; publish step rebases again).
2. Wave via Workflow tool, scriptPath=SKILL/scripts/worship-sprint.js:
   - STATE.pendingResumeRunId set → resume {scriptPath, resumeFromRunId, args: STATE.pendingArgs (IDENTICAL JSON)}; clear both on success.
   - else new wave: args {round:<hour>, cats: next STATE.waveSize of SKILL/scripts/category-bank.json from catIndex} as [{"type":"cat","name":...}]; catIndex+=waveSize; bank exhausted → reuse categories + " — second pass, go even deeper".
   - Mark STATE.activeWorkflowTaskId = task id, END turn (notification drives apply).
3. ALL agents fail "session limit"/"out of usage credits" → STATE.pendingResumeRunId=runId, pendingArgs=args,
   resumeNotBefore=reset-time+60s (out-of-credits: now+4h), clear activeWorkflowTaskId, one status line, END.
4. Apply on completion: `node SKILL/scripts/apply-round.js <task .output path> SKILL/reports/hymns-<round>.json`
   - gap = target − count; extracted > gap → `cd WORKTREE && node SKILL/scripts/trim-to-gap.js <hymns> <gap> <out>` and
     append the .surplus.json entries to WORKTREE/data/worship-hymn-bank.json (dedup by slugified title).
   - `node scripts/assemble-worship-additions.js /dev/null <hymns file>` — NOTE: pass SKILL/reports/empty.json ([]) not /dev/null.
5. Regenerate + QA: `node generate-worship-pages.js --ingest`; dup slugs 0; spot-check one new page's credit line.
6. Publish: `git status --short` = worship paths + tools/worship-sprint only → `git add -A && git commit -m "Worship burst <HH>:00 — ..." && git fetch origin main -q && git rebase origin/main && git push origin worship-2777:main`. Push rejected → fetch+rebase+retry once, else leave for next burst.
7. count == target first time → notify Adam (report), phase="polish".

### VERIFY lane (accuracy of chords + lyrics — Adam's 8/12 directive)
Pick ONE per burst, publish fixes like GROW step 6:
- **chord-lint**: `node SKILL/scripts/chord-lint.js` writes SKILL/reports/chord-lint.json (garbled chord lines, encoding
  junk, thin bodies). Fix the top offenders IN docs/data/worship-extra-songs.json (extras) or flag archive charts
  in the report (NEVER edit Adam's source archive). Re-run to confirm shrinking counts.
- **lyrics-fidelity** (needs subagents): sample 40 agent-added hymns (ext:'hymn', rotate via STATE.verifyCursor),
  wave with args {mode:"verify", cats:[{type:"verify", batch:"<JSON of 10 {title,author,lyrics-first-120-chars,slug}>"}...]};
  entries reported unfaithful (publicDomain:false) → fix from source or remove via worship-purged.json; log in SKILL/reports/.
- **missing-keys / missing-writers**: fill from Hymnary (subagents) or safe inference; publish.
- **near-dup titles**: inline scan for same hymn under variant titles; merge via worship-purged.json + redirect note.

## POLISH (after target)
Work polishQueue like VERIFY until empty → CronDelete, final notify, update memory, DONE.

## Rules
- PD lyrics only ever from verified sources; contemporary/CCM = linksOnly pages, NEVER reproduced lyrics.
- Fresh CCM batches: add entries to a JSON list and run SKILL/scripts/build-linksonly.js (see header) — genre-tag
  non-congregational slugs into docs/data/worship-nonworship.json (keep the worship/CCM hero split honest).
- Surplus verified hymns → data/worship-hymn-bank.json (durable). Land EXACTLY on 3,777 via trim-to-gap.
- Never git add -A in the MAIN checkout. Never edit the source archive. Two sessions may share account
  limits + this state file (Adam's "claude meister") — expect races, last-writer-wins, re-read before writing.
