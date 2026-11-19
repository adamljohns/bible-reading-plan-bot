#!/usr/bin/env node
'use strict';
// refine-yield-gate.test.js
//
// A gate that has only ever passed has not been tested (rclone-guards-must-be-tested,
// and the delete guard before it). This suite exists primarily to DEMONSTRATE THE
// GATE FAILING on a synthetic dead pool — the halt path is the one that matters.

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');

const REPO = path.join(__dirname, '..');
const GATE = path.join(REPO, 'scripts/refine-yield-gate.js');

const base = {
  id: 'sample', name: 'Sample Church', state: 'VA', country_code: 'US',
  website: 'https://sample.example', pastor: 'Verify', enrichment_notes: '', source_url: ''
};
const church = extra => ({ ...base, ...extra });

// A synthetic root: churches.json only, so nothing here can touch live data.
function makeRoot(churches) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'yield-gate-'));
  fs.mkdirSync(path.join(root, 'docs/data'), { recursive: true });
  fs.writeFileSync(path.join(root, 'docs/data/churches.json'),
    JSON.stringify({ total_churches: churches.length, churches }, null, 1));
  return root;
}

function runGate(root, { streaks, store, args = [] } = {}) {
  const env = { ...process.env, GRIND_ROOT: root, HOME: root };
  if (streaks) env.GRIND_EMPTY_STREAKS = JSON.stringify(streaks);
  else delete env.GRIND_EMPTY_STREAKS;
  env.GRIND_STREAK_STORE = store || path.join(root, 'streaks.json');
  const r = cp.spawnSync(process.execPath, [GATE, '--json', '--no-notify', ...args], { env, encoding: 'utf8' });
  let parsed = null;
  try { parsed = JSON.parse(r.stdout); } catch (_) { /* record mode prints text */ }
  return { code: r.status, json: parsed, stdout: r.stdout, stderr: r.stderr };
}

// ── 1. LIVE POOL → PROCEED ──────────────────────────────────────────────────
{
  const root = makeRoot([church({ id: 'a' }), church({ id: 'b' })]);
  const r = runGate(root, { streaks: { fresh: 0, retry: 0, social: 0 } });
  assert.strictEqual(r.code, 0, `live pool must PROCEED, got ${r.code}: ${r.stderr}`);
  assert.strictEqual(r.json.verdict, 'PROCEED');
}

// ── 2. THE FAILING CASE: a pool with work left, but three +0 batches on every
//       apply lane and no fallback. This is the 129-wasted-batches scenario. ──
{
  const root = makeRoot([church({ id: 'a' }), church({ id: 'b' }), church({ id: 'c' })]);
  // Streaks need a fresh *_last_empty_at: since the 24h thaw, an undated streak
  // is "unknown age" and gets one re-test (isApplyLaneCold).
  const now = new Date().toISOString();
  const r = runGate(root, { streaks: { fresh: 3, retry: 3, social: 3,
    fresh_last_empty_at: now, retry_last_empty_at: now, social_last_empty_at: now } });
  assert.strictEqual(r.code, 3, `DEAD POOL MUST HALT with exit 3, got ${r.code}: ${r.stdout}${r.stderr}`);
  assert.strictEqual(r.json.verdict, 'HALT');
  assert.match(r.json.reason, /COLD after 3 consecutive \+0 batches/);
  assert.ok(r.json.counts.fresh > 0, 'the halt must fire while records REMAIN — a drained pool is a different case');
}

// ── 3. Cold apply lanes but a real fallback → PROCEED, not HALT.
//       The gate stops waste; it must not stop the lane that works. ──────────
{
  const root = makeRoot([
    church({ id: 'a' }),
    church({ id: 'sbc', website: '', source_url: 'https://churches.sbc.net/church/1' }),
  ]);
  const ts = new Date().toISOString();
  const r = runGate(root, { streaks: { fresh: 3, retry: 3, social: 3,
    fresh_last_empty_at: ts, retry_last_empty_at: ts, social_last_empty_at: ts } });
  assert.strictEqual(r.code, 0, 'source-recovery fallback must keep the run alive');
  assert.match(r.json.reason, /source-recovery/);
}

// ── 4. RULE 6: a gate that examines nothing has not passed. ─────────────────
{
  const root = makeRoot([]);
  const r = runGate(root);
  assert.strictEqual(r.code, 2, 'zero records examined must exit non-zero, not report a cheerful pass');
  assert.strictEqual(r.json.verdict, 'VACUOUS');
}

// ── 5. END TO END: three real empty hops must actually FLIP a live lane to
//       HALT. This is the hole that made the pre-existing lane-cold predicate
//       unreachable — empty rounds never called recordLaneHop(), so the streak
//       could only ever be reset to 0. ─────────────────────────────────────
{
  const root = makeRoot([church({ id: 'a' }), church({ id: 'b' }), church({ id: 'c' })]);
  const store = path.join(root, 'streaks.json');
  const opts = { store };

  assert.strictEqual(runGate(root, opts).code, 0, 'starts live');
  for (let i = 1; i <= 3; i++) {
    const rec = runGate(root, { store, args: ['--record', 'fresh', '0'] });
    assert.strictEqual(rec.code, 0, 'recording a hop must succeed');
  }
  // retry/social share the same eligibility as fresh here, so cool them too.
  for (const lane of ['retry', 'social']) {
    for (let i = 1; i <= 3; i++) runGate(root, { store, args: ['--record', lane, '0'] });
  }
  const after = runGate(root, opts);
  assert.strictEqual(after.code, 3, `three recorded +0 hops per lane must HALT, got ${after.code}: ${after.stdout}${after.stderr}`);

  // ...and a single real yield must thaw it again. A gate that cannot be
  // un-stuck is an outage, not a gate.
  runGate(root, { store, args: ['--record', 'fresh', '4'] });
  const thawed = runGate(root, opts);
  assert.strictEqual(thawed.code, 0, 'one non-zero yield must thaw the lane');
}

// ── 6. The runner must actually consult the gate. ──────────────────────────
{
  const runner = fs.readFileSync(path.join(REPO, 'scripts/pastor-refine-local.sh'), 'utf8');
  assert.ok(runner.includes('refine-yield-gate.js'), 'pastor-refine-local.sh must call the yield gate');
  assert.ok(/--record"? *"?\$MODE/.test(runner) || runner.includes('--record "$MODE"'),
    'the runner must record every hop, including empty ones');
}

// ── 7. REGRESSION (2026-11-19): cold apply lanes + website-discovery pool →
//       PROCEED. The selector returned website-discovery (2,962 eligible) while
//       the gate only knew source-recovery and HALTED with "no fallback". ──────
{
  const root = makeRoot([
    church({ id: 'r', enrichment_notes: 'Phase 6f no parseable pastor' }),
    church({ id: 'w1', website: '' }), church({ id: 'w2', website: '' }),
  ]);
  const now = new Date().toISOString();
  const r = runGate(root, { streaks: { fresh: 3, retry: 3, social: 3,
    fresh_last_empty_at: now, retry_last_empty_at: now, social_last_empty_at: now } });
  assert.strictEqual(r.json.selected, 'website-discovery', `selector should pick website-discovery, got ${r.json.selected}`);
  assert.strictEqual(r.code, 0, `website-discovery fallback must PROCEED, got ${r.code}: ${r.json.reason}`);
  assert.match(r.json.reason, /website-discovery \(2 eligible\)/);
}

// ── 8. CONTRACT: every lane chooseLane() can return is either an apply lane,
//       a gate-approved fallback, or an explicit idle verdict. Adding a new
//       selector lane without teaching the gate now fails here. ───────────────
{
  const lanes = require(path.join(REPO, 'scripts/lib/grind-lanes.js'));
  const src = fs.readFileSync(path.join(REPO, 'scripts/lib/grind-lanes.js'), 'utf8');
  const body = src.slice(src.indexOf('function chooseLane'), src.indexOf('module.exports'));
  const returned = new Set([...body.matchAll(/return '([a-z-]+)'/g)].map(m => m[1]));
  const IDLE = new Set(['nothing-to-grind', 'monitoring']);
  for (const l of returned) {
    assert.ok(lanes.APPLY_LANES.includes(l) || lanes.FALLBACK_LANES.includes(l) || IDLE.has(l),
      `chooseLane can return "${l}" but the yield gate has no rule for it`);
  }
  for (const l of lanes.FALLBACK_LANES) {
    assert.ok(lanes.FALLBACK_COUNT_KEY[l], `fallback ${l} needs a count key`);
    assert.ok(returned.has(l), `gate allows ${l} but the selector never returns it`);
  }
  // Each fallback, when it is the only work, must PROCEED end to end.
  const now = new Date().toISOString();
  const cold = { fresh: 3, retry: 3, social: 3, fresh_last_empty_at: now, retry_last_empty_at: now, social_last_empty_at: now };
  const fixtures = {
    'source-recovery': [church({ id: 's', website: '', source_url: 'https://churches.sbc.net/church/1' })],
    'website-discovery': [church({ id: 'w', website: '' })],
  };
  for (const l of lanes.FALLBACK_LANES) {
    const r = runGate(makeRoot(fixtures[l]), { streaks: cold });
    assert.strictEqual(r.json.selected, l);
    assert.strictEqual(r.code, 0, `fallback ${l} must PROCEED: ${r.json.reason}`);
  }
  // ...and the idle verdicts still HALT.
  const idle = runGate(makeRoot([church({ id: 'r', enrichment_notes: 'Phase 6f no parseable pastor' })]), { streaks: cold });
  assert.strictEqual(idle.json.selected, 'nothing-to-grind');
  assert.strictEqual(idle.code, 3, 'nothing-to-grind must still HALT');
}

console.log('refine-yield-gate: all assertions passed (incl. HALT demonstrated on a dead pool)');
