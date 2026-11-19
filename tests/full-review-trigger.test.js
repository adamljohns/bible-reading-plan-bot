#!/usr/bin/env node
'use strict';
// full-review-trigger.test.js — the bounded daily full-review trigger.
// Proves: dry by default, 10-20 batch clamp, grind-lock compatibility, --live
// refused without a valid standing GO, dry output kept out of git.
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const cp = require('child_process');
const REPO = path.join(__dirname, '..');
const SCHED = path.join(REPO, 'scripts/ops/full-review-scheduled.sh');
const TRIG = path.join(REPO, 'scripts/ops/trigger-directory-grind.sh');
const ROUND = path.join(REPO, 'scripts/full-review-round.sh');
const { check } = require(path.join(REPO, 'scripts/lib/full-review-go.js'));
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'frt-'));
const run = (script, args, env) => cp.spawnSync('/bin/bash', [script, ...args], { env: { ...process.env, ...env }, encoding: 'utf8' });

// 1. GO guard: missing / not-true / expired / valid.
{
  const d = tmp(); const f = path.join(d, 'go.json');
  assert.strictEqual(check(f).ok, false, 'missing GO file must refuse');
  fs.writeFileSync(f, JSON.stringify({ live_allowed: false, granted_by: 'x', source: 'y', expires: '2999-01-01' }));
  assert.strictEqual(check(f).ok, false, 'live_allowed false must refuse');
  fs.writeFileSync(f, JSON.stringify({ live_allowed: true, granted_by: 'Adam', source: 'tg', expires: '2020-01-01' }));
  assert.match(check(f).reason, /expired/);
  fs.writeFileSync(f, JSON.stringify({ live_allowed: true, expires: '2999-01-01' }));
  assert.strictEqual(check(f).ok, false, 'GO without granted_by/source must refuse');
  fs.writeFileSync(f, JSON.stringify({ live_allowed: true, granted_by: 'Adam', source: 'tg', expires: '2999-01-01' }));
  assert.strictEqual(check(f).ok, true);
}

// 2. Batch clamp 10..20, dry mode, plan-only (no model, no network).
for (const [asked, want] of [['3', 10], ['15', 15], ['60', 20], ['junk', 15]]) {
  const d = tmp();
  const r = run(SCHED, [], { FULL_REVIEW_PLAN_ONLY: '1', FULL_REVIEW_DAILY_BATCH: asked,
    FULL_REVIEW_LOCK: path.join(d, 'nolock'), FULL_REVIEW_HEALTH: path.join(d, 'h.json'), FULL_REVIEW_OUT_DIR: path.join(d, 'out') });
  assert.strictEqual(r.status, 0, r.stderr);
  assert.match(r.stdout, new RegExp(`batch=${want} mode=dry`), `batch ${asked} -> ${want}: ${r.stdout}`);
}

// 3. Lock held by the grind -> skip with exit 0 and a health record.
{
  const d = tmp(); const lock = path.join(d, 'lock'); fs.mkdirSync(lock);
  const h = path.join(d, 'h.json');
  const r = run(SCHED, [], { FULL_REVIEW_LOCK: lock, FULL_REVIEW_HEALTH: h, FULL_REVIEW_OUT_DIR: path.join(d, 'out') });
  assert.strictEqual(r.status, 0);
  const j = JSON.parse(fs.readFileSync(h, 'utf8'));
  assert.strictEqual(j.verdict, 'skipped-lock'); assert.strictEqual(j.mode, 'dry');
  assert.ok(fs.existsSync(lock), 'the scheduled job must never remove the grind lock');
}

// 4. Already ran today -> no second round.
{
  const d = tmp(); const h = path.join(d, 'h.json');
  const today = new Date().toLocaleDateString('en-CA');
  fs.writeFileSync(h, JSON.stringify({ job: 'full-review-daily', date: today, verdict: 'ok' }));
  const r = run(SCHED, [], { FULL_REVIEW_LOCK: path.join(d, 'nolock'), FULL_REVIEW_HEALTH: h });
  assert.match(r.stdout, /already ran today/);
}

// 5. Manual trigger --live without a standing GO refuses and starts nothing.
{
  const d = tmp();
  const r = run(TRIG, ['full-review', '15', '--live'], { FULL_REVIEW_STANDING_GO: path.join(d, 'absent.json') });
  assert.strictEqual(r.status, 3, `--live without GO must exit 3: ${r.stdout}${r.stderr}`);
  assert.match(r.stdout, /REFUSED/);
}

// 6. Source contracts: the scheduled wrapper never asks for live; the round
//    script guards live with the GO check and routes dry output out of git;
//    the plist calls the wrapper and nothing else.
{
  const sched = fs.readFileSync(SCHED, 'utf8');
  assert.ok(sched.includes('FULL_REVIEW_MODE=dry') && !/FULL_REVIEW_MODE=live|--live/.test(sched.replace(/^#.*$/gm, '')),
    'scheduled wrapper must be dry-only');
  const round = fs.readFileSync(ROUND, 'utf8');
  assert.ok(round.includes('full-review-go.js'), 'live mode must consult the standing-GO guard');
  assert.ok(/FULL_REVIEW_OUT_DIR is for dry runs only/.test(round));
  assert.ok(round.includes('--out "$OUTDIR"'), 'dry output dir must reach build-patch');
  assert.ok(round.includes('/tmp/pastor-refine-local.lock'), 'round must share the grind lock');
  const plist = fs.readFileSync(path.join(REPO, 'scripts/ops/launchd/com.moop.full-review-daily.plist'), 'utf8');
  assert.ok(plist.includes('full-review-scheduled.sh') && !plist.includes('live'));
}
console.log('full-review-trigger: all assertions passed');
