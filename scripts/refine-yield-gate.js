#!/usr/bin/env node
'use strict';
// refine-yield-gate.js — the P5 yield gate (governance rule 6).
//
// The refine loop's job is to fill fields. A pool that returns +0 three times in
// a row is dead, and re-running it is the single largest wasted budget line in
// the fleet (129 of 213 refine commits returned +0 in the 8/23–8/30 sprint).
//
// The lane-cold predicate already existed in lib/grind-lanes.js. It could never
// fire, because the ONLY caller of recordLaneHop() is append-grind-stats.js,
// which pastor-refine-local.sh runs exclusively on the NON-zero branch. Empty
// rounds therefore never incremented a streak; non-empty rounds reset it to 0.
// The counter could only go down. This gate closes that hole and makes the
// verdict loud instead of an `exit 0`.
//
// Modes:
//   --record <lane> <applied>   record one hop (0 applied => streak+1)
//   --check                     evaluate and exit non-zero on HALT (default)
//   --json                      machine-readable verdict on stdout
//
// Exit codes:
//   0  PROCEED  — a live apply lane, or a real fallback lane, exists
//   2  VACUOUS  — the gate examined nothing (rule 6: a gate that examines
//                 nothing has not passed)
//   3  HALT     — every apply lane is cold and there is nothing to fall through
//                 to. Do not spend another batch on this pool.

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const lanes = require('./lib/grind-lanes.js');

const ROOT = process.env.GRIND_ROOT || path.join(__dirname, '..');
const argv = process.argv.slice(2);
const has = f => argv.includes(f);
const JSON_OUT = has('--json');
const QUIET = has('--quiet');

function out(s) { if (!JSON_OUT && !QUIET) console.log(s); }

function loadChurches() {
  const p = path.join(ROOT, 'docs/data/churches.json');
  const raw = JSON.parse(fs.readFileSync(p, 'utf8'));
  return Array.isArray(raw) ? raw : (raw.churches || []);
}

// ── --record ────────────────────────────────────────────────────────────────
if (has('--record')) {
  const i = argv.indexOf('--record');
  const lane = argv[i + 1];
  const applied = parseInt(argv[i + 2], 10);
  if (!lanes.APPLY_LANES.includes(lane) || Number.isNaN(applied)) {
    console.error(`refine-yield-gate: --record needs <${lanes.APPLY_LANES.join('|')}> <appliedCount>`);
    process.exit(2);
  }
  const streaks = lanes.recordLaneHop(lane, applied, ROOT);
  const n = streaks[lane] || 0;
  out(`yield-gate: recorded ${lane} hop applied=${applied} -> empty_streak=${n}/${lanes.EMPTY_STREAK_SKIP}`);
  process.exit(0);
}

// ── --check (default) ───────────────────────────────────────────────────────
const churches = loadChurches();
const counts = lanes.countLanes(churches);
const streaks = lanes.loadEmptyStreaks(ROOT);

// Rule 6: a verifier that can report "0 checked / 0 failed" must exit non-zero.
// Nothing to examine is not a pass.
if (!churches.length) {
  const v = { verdict: 'VACUOUS', reason: 'churches.json holds 0 records — the gate examined nothing', counts, streaks };
  if (JSON_OUT) console.log(JSON.stringify(v, null, 1));
  else console.error(`yield-gate: VACUOUS — ${v.reason}`);
  process.exit(2);
}

const live = lanes.APPLY_LANES
  .map(l => ({ lane: l, pool: counts[l] || 0, streak: streaks[l] || 0, cold: lanes.isApplyLaneCold(l, streaks) }));
const usable = live.filter(l => l.pool > 0 && !l.cold);
const coldWithWork = live.filter(l => l.pool > 0 && l.cold);
const selected = lanes.chooseLane(counts, '', streaks);

const report = [
  `yield-gate  (${churches.length.toLocaleString()} churches examined)`,
  ...live.map(l =>
    `  ${l.lane.padEnd(7)} pool=${String(l.pool).padStart(6)}  empty_streak=${l.streak}/${lanes.EMPTY_STREAK_SKIP}` +
    (l.cold ? '  ← COLD (halted)' : '')),
  `  source_recovery   pool=${counts.source_recovery}`,
  `  website_discovery pool=${counts.website_discovery}`,
  `  selected lane: ${selected}`,
].join('\n');

let verdict, code, reason;
if (usable.length) {
  verdict = 'PROCEED'; code = 0;
  reason = `live lane "${usable[0].lane}" has ${usable[0].pool} eligible records`;
} else if (selected === 'source-recovery') {
  verdict = 'PROCEED'; code = 0;
  reason = `all apply lanes cold — falling through to source-recovery (${counts.source_recovery} eligible)`;
} else {
  verdict = 'HALT'; code = 3;
  reason = coldWithWork.length
    ? `every apply lane is COLD after ${lanes.EMPTY_STREAK_SKIP} consecutive +0 batches ` +
      `(${coldWithWork.map(l => `${l.lane}:${l.pool} left`).join(', ')}) and no fallback lane has work. ` +
      `Re-running this pool spends budget to fill nothing.`
    : `no apply lane has eligible records and no fallback lane has work (selected=${selected})`;
}

if (JSON_OUT) {
  console.log(JSON.stringify({ verdict, reason, selected, counts, streaks, examined: churches.length }, null, 1));
} else {
  out(report);
  (code === 0 ? console.log : console.error)(`yield-gate: ${verdict} — ${reason}`);
}

// A HALT that reaches no human is a HARD failure (delivery doctrine). Report it
// once per halt, not once per round, so the gate does not become its own noise.
if (code === 3 && !has('--no-notify')) {
  const stamp = path.join(process.env.HOME || '/tmp', 'Library/Logs/refine-yield-gate-last-halt.txt');
  const today = new Date().toISOString().slice(0, 10);
  let last = '';
  try { last = fs.readFileSync(stamp, 'utf8').trim(); } catch (_) { /* first halt */ }
  if (last !== today) {
    try {
      fs.mkdirSync(path.dirname(stamp), { recursive: true });
      fs.writeFileSync(stamp, today);
      const tg = path.join(process.env.HOME || '', 'Scripts/tg-send.sh');
      if (fs.existsSync(tg)) {
        execFileSync('/bin/bash', [tg,
          `Church directory: yield gate HALTED the refine loop.\n\n${reason}\n\nNo budget is being spent on a dead pool. Harvest and source-recovery lanes are unaffected.`],
          { stdio: 'ignore', timeout: 20000 });
      }
    } catch (_) { /* notification is best-effort; the exit code is the contract */ }
  }
}

process.exit(code);
