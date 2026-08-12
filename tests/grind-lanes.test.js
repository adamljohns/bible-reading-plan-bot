#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const ROOT = path.join(__dirname, '..');
const lanes = require(path.join(ROOT, 'scripts/lib/grind-lanes.js'));

const base = {
  id: 'sample', name: 'Sample Church', state: 'VA', country_code: 'US',
  website: '', pastor: 'Verify', enrichment_notes: '', source_url: ''
};
const c = extra => ({ ...base, ...extra });

// Current extractor work always outranks frontier recovery.
let counts = lanes.countLanes([
  c({ id: 'fresh', website: 'https://fresh.example' }),
  c({ id: 'discover' }),
  c({ id: 'sbc', source_url: 'https://churches.sbc.net/church/1' })
]);
assert.strictEqual(counts.fresh, 1);
assert.strictEqual(lanes.chooseLane(counts, null), 'fresh');
assert.ok(counts.product_backlog >= 3, 'product backlog must include active fresh/discovery/source work');

// Exhausting the legacy three pools must advance to product-enrichment lanes.
counts = lanes.countLanes([
  c({ id: 'discover' }),
  c({ id: 'sbc', source_url: 'https://churches.sbc.net/church/1' })
]);
assert.strictEqual(counts.website_discovery, 1);
assert.strictEqual(counts.source_recovery, 1);
assert.strictEqual(lanes.chooseLane(counts, 'website-discovery'), 'source-recovery');
assert.strictEqual(lanes.chooseLane(counts, 'source-recovery'), 'website-discovery');

// Completed markers prevent quota burn and repeated authoritative-source fetches.
counts = lanes.countLanes([
  c({ id: 'searched', _website_searched: '2026-08-12' }),
  c({ id: 'fetched', source_url: 'https://churches.sbc.net/church/2', sbc_detail_fetched_at: '2026-08-12T00:00:00Z' })
]);
assert.strictEqual(counts.website_discovery, 0);
assert.strictEqual(counts.source_recovery, 0);
assert.strictEqual(lanes.chooseLane(counts, null), 'monitoring');

// Authoritative-source failures retry, then leave the automated lane after the cap.
assert.strictEqual(lanes.sourceRecoveryEligible(c({ source_url: 'https://churches.sbc.net/church/retry', _sbc_detail_failures: 2 })), true);
assert.strictEqual(lanes.sourceRecoveryEligible(c({ source_url: 'https://churches.sbc.net/church/capped', _sbc_detail_failures: 3 })), false);
counts = lanes.countLanes([c({ id: 'source-capped', source_url: 'https://churches.sbc.net/church/capped', _sbc_detail_failures: 3 })]);
assert.strictEqual(counts.source_recovery_exhausted, 1);
assert.strictEqual(counts.human_review, 1, 'capped source recovery must move into visible review');
assert.strictEqual(counts.product_backlog, 1, 'capped source recovery must remain in product backlog');

// Exhausted pastor attempts remain visible as product backlog, not automated work.
counts = lanes.countLanes([
  c({ id: 'exhausted', website: 'https://exhausted.example', _loop_round_attempted: true,
      enrichment_notes: 'Phase 6f no parseable pastor\nPhase 6f no parseable pastor' }),
  c({ id: 'dead', website: 'https://dead.example', _dead_site: true }),
  c({ id: 'review', pastor: 'John Smith', needs_review: true })
]);
assert.strictEqual(counts.pastor_exhausted, 1);
assert.strictEqual(counts.dead_site_recovery, 1);
assert.strictEqual(counts.human_review, 1);
assert.ok(counts.product_backlog >= 3);

const html = fs.readFileSync(path.join(ROOT, 'docs/grind-report.html'), 'utf8');
const runner = fs.readFileSync(path.join(ROOT, 'scripts/pastor-refine-local.sh'), 'utf8');
assert.ok(html.includes('CURRENT PASS EXHAUSTED / CONTINUING'), 'dashboard must not claim product completion');
assert.ok(!html.includes('Enrichment complete —'), 'dashboard must not call the product complete');
assert.ok(html.includes('Website discovery'), 'dashboard must expose the discovery lane');
assert.ok(html.includes('Source recovery'), 'dashboard must expose the source-recovery lane');
assert.ok(html.includes("['fresh','retry','social'].includes(r.mode)"), 'pastor hit rate must exclude frontier attempts');
assert.ok(runner.includes('--found "$APPLIED" --applied "$APPLIED"'), 'dashboard rows must count guarded pastor applications, not extracted candidates');

const plan = cp.execFileSync('/bin/bash', [path.join(ROOT, 'scripts/continuous-enrichment-lane.sh'), '/tmp/prl-test'], {
  cwd: ROOT,
  env: { ...process.env, CONTINUOUS_PLAN_ONLY: '1' },
  encoding: 'utf8',
});
assert.match(plan, /^lane=(website-discovery|source-recovery)\b/, 'controller must advance into an executable frontier lane');

console.log('grind-lanes: all assertions passed');
