# Two-Track Plan — Dictionary 7,777 & Churches 37,000
*Drafted 2026-06-12. Owner: Adam. Execution: Claude Code (cloud) + OpenClaw fleet (local) + deterministic scripts. Companion to DICTIONARY-ROADMAP.md.*

## The targets and where we stand

| Track | Now | Target | Gap | Glide path |
|---|---|---|---|---|
| MOOP Dictionary | **5,425** | 7,777 | 2,352 | ~100/night × 24 nights → **~July 6-8** |
| Church Directory | **28,513** | 37,000 | 8,487 | 3 ingest waves/wk × ~1,500-3,000 → **~June 28-30** |

**On "more word studies than churches":** recommend NOT racing these numbers against each other. They are different kinds of weight — a word study is authored doctrine, a church record is directory data. Counting surfaces, the word-study side already runs deep: 5,425 dictionary entries + the Greek & Hebrew Lexicon's 7,700+ studies. 7,777 deep entries will outweigh 37,000 shallow records on every axis that matters for the mission. Keep both targets as they are.

## Usage discipline (the "don't burn it in 24 hours" rules)

1. **Fixed-scope scheduled runs, never marathons.** Every run has a hard cap baked into its prompt; it finishes its scope, reports, and stops. No open-ended loops, no retry storms.
2. **Right engine for the job.**
   - **Cloud Claude (costs usage):** entry authoring (voice-lock theology demands it), corpus audits, judgment passes.
   - **OpenClaw fleet ($0 local):** church socials/pastor enrichment, review-queue triage, freshness watchdogs, alerting via notify-adam.
   - **Deterministic scripts (free):** bulk church ingest, dedup guard, link audits, rebuilds, manifests — the pipeline already exists and costs nothing.
3. **Off-peak nightly windows** for the dictionary run (~2h each), so daytime interactive capacity stays free for Adam.
4. **Graceful degradation:** if a week runs hot on usage, halve the dictionary pace (50/night) — completion slips ~2 weeks, nothing breaks.
5. **One weekly SITREP** instead of constant check-ins: counts vs glide path, debt burned down, drift findings, usage spent.

## Week 1 — June 13-19

**Dictionary (5,425 → ~6,100)**
- Nightly authoring run: 10 batches × 10 entries through `bin/batch_pipeline.sh`, sourced FIRST from `data/dictionary-candidates-from-dangling.txt` (794 corpus-demanded slugs), then the open veins (OT towns, tribal-allotment places, Puritans/hymn-writers/missionaries detail, Rom 16 households).
- Chapter-linker sweep every 3rd night (places/figures batches feed it); skip after pure-figure nights.
- **Corruption-section backfill, half (~160 of ~320)** — the highest-value era-debt; caveat templates exist in `bin/fix_corruption_sections.py`.
- Decoder freshness micro-pass: any new slang Adam flags goes in as singles batches (policy + how-to already in `.claude/skills/dict-batch/`).

**Churches (28,513 → ~31,500)**
- 2 ingest waves (~1,500 each) from the next unmined denominational rosters; every wave ends with dedup guard + site-wide link audit (the 2-cities lesson).
- **Logo autopilot pass 1**: green churches first (memory: 92% of pages lack logo/hero).
- Review-queue intake: wire the Know-A-Church-We-Should-Review form to a fleet cron (triage → review-queue JSON → weekly human-grade list). $0 usage.
- Update `enrich-churches` skill target text 7,777 → 37,000.

## Week 2 — June 20-26

**Dictionary (→ ~6,800)**
- Same nightly cadence.
- Corruption backfill complete (320/320). Usage-section debt (642 entries): triage week — decide backfill vs. accept-as-is per era; don't blind-author 642 sections.
- Mid-point corpus review (batch-142 style): full link crawl, voice-lock scan, dangling-chip harvest refresh.

**Churches (→ ~34,500-35,000)**
- 2-3 more ingest waves + quality pass: substantiation upgrades (yellow→green) on DC/VA metro first.
- **Street View API decision needed from Adam** (key + billing) for bulk building photos — blocks the photo backfill, nothing else.
- Logo autopilot pass 2.

## Week 3+ — glide to done

- Dictionary: nightly runs continue → **7,777 ≈ July 6-8**. Final week includes a full Fable-style fidelity audit (counts ≠ fidelity) before declaring victory.
- Churches: final wave → **37,000 ≈ June 28-30**, then directory flips to maintenance mode.
- Both: switch to **maintenance cadence** — weekly integrity sweep, intake crons (church form, decoder words, corpus-demanded slugs), monthly SITREP.

## "Happy with status" definition (the finish line, not just the number)

**Dictionary:** 7,777 entries · 0 hard voice-lock drift · 0 integrity-audit failures · corruption + usage era-debt resolved or formally accepted · all entries reachable via index/letter-bar/topic/decoder surfaces · cross-link sweeps current.

**Churches:** 37,000 records · dedup-guard clean · 0 broken internal links · every green church has logo + hero · review-queue intake automated · state-coverage map with no embarrassing holes.

## Standing automation (what Adam already built that carries this)

The skills are the right bones — `dict-batch` encodes the whole authoring pipeline with pre/post-flight, `enrich-churches` fans out enrichment agents, `batch_pipeline.sh` + integrity/drift audits catch regressions, the fleet handles watchdogs and alerts. What was missing is **cadence** (skills fire when invoked; they need scheduled invocation) and **one rolled-up scoreboard** — this plan + the weekly SITREP supply both.

## Dependencies / asks for Adam
1. Street View API key decision (week 2, churches photos).
2. ~~Confirm next denominational source lists~~ **DECIDED 2026-06-12: 100% of SBC churches first.** (Note: the SBC alone runs ~45-47k congregations nationally, so full SBC coverage will overshoot the 37,000 target on its own — wave sessions should ingest by state, dedup against the existing 28.5k, and re-read the target when SBC coverage completes.)
3. ~~Approve the nightly schedule window~~ **DONE: `nightly-dictionary-batch-run` created 2026-06-12, 02:10 AM daily.** First run will pause on its first permission prompts until Adam approves them once (approvals then persist for all future runs).
