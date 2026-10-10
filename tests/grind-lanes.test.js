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
const cleanStreaks = { fresh: 0, retry: 0, social: 0 };
assert.strictEqual(lanes.chooseLane(counts, null, cleanStreaks), 'fresh');
assert.ok(counts.product_backlog >= 3, 'product backlog must include active fresh/discovery/source work');

// Exhausting the legacy three pools must advance to product-enrichment lanes.
counts = lanes.countLanes([
  c({ id: 'discover' }),
  c({ id: 'sbc', source_url: 'https://churches.sbc.net/church/1' })
]);
assert.strictEqual(counts.website_discovery, 1);
assert.strictEqual(counts.source_recovery, 1);
assert.strictEqual(lanes.chooseLane(counts, 'website-discovery', cleanStreaks), 'source-recovery');
assert.strictEqual(lanes.chooseLane(counts, 'source-recovery', cleanStreaks), 'source-recovery');

// Completed markers prevent quota burn and repeated authoritative-source fetches.
counts = lanes.countLanes([
  c({ id: 'searched', _website_searched: '2026-08-12' }),
  c({ id: 'fetched', source_url: 'https://churches.sbc.net/church/2', sbc_detail_fetched_at: '2026-08-12T00:00:00Z' })
]);
assert.strictEqual(counts.website_discovery, 0);
assert.strictEqual(counts.source_recovery, 0);
assert.strictEqual(lanes.chooseLane(counts, null, cleanStreaks), 'monitoring');

// Authoritative-source failures retry, then leave the automated lane after the cap.
assert.strictEqual(lanes.sourceRecoveryEligible(c({ source_url: 'https://churches.sbc.net/church/retry', _sbc_detail_failures: 2 })), true);
assert.strictEqual(lanes.sourceRecoveryEligible(c({ source_url: 'https://churches.sbc.net/church/identity-hold', _hold_review: 'sbc-source-identity-mismatch' })), false, 'identity holds must leave the automated source-recovery lane');
assert.strictEqual(lanes.sourceRecoveryEligible(c({ source_url: 'https://churches.sbc.net.evil.example/church/lookalike' })), false, 'source recovery must require the exact SBC hostname');
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

// Website discovery is review-only until page/geo corroboration and guarded merge exist.
counts = lanes.countLanes([c({ id: 'discover-only' })]);
assert.strictEqual(counts.website_discovery, 1);
assert.strictEqual(lanes.chooseLane(counts, null, cleanStreaks), 'monitoring');

const html = fs.readFileSync(path.join(ROOT, 'docs/grind-report.html'), 'utf8');
const runner = fs.readFileSync(path.join(ROOT, 'scripts/pastor-refine-local.sh'), 'utf8');
const sbcAutopilot = fs.readFileSync(path.join(ROOT, 'scripts/sbc-detail-autopilot.sh'), 'utf8');
const generator = fs.readFileSync(path.join(ROOT, 'generate-church-pages.js'), 'utf8');
assert.ok(generator.includes("typeof church.service_times === 'string'"), 'profile renderer must expose verified legacy service_times data');
assert.ok(html.includes('CURRENT PASS EXHAUSTED / CONTINUING'), 'dashboard must not claim product completion');
assert.ok(!html.includes('Enrichment complete —'), 'dashboard must not call the product complete');
assert.ok(html.includes('Website discovery'), 'dashboard must expose the discovery lane');
assert.ok(html.includes('Source recovery'), 'dashboard must expose the source-recovery lane');
assert.ok(html.includes("['fresh','retry','social'].includes(r.mode)"), 'pastor hit rate must exclude frontier attempts');
assert.ok(html.includes("card('Validated content applied'"), 'dashboard must report whole-profile content gain, not pastors alone');
assert.ok(html.includes('r.pastors_applied ?? r.found') && html.includes('r.applied ?? r.found'), 'round table must separate pastor and total-content fields');
assert.ok(runner.includes('--found "$APPLIED" --applied "$CONTENT_APPLIED"'), 'dashboard applied count must include all guarded content fields, not extracted candidates');
assert.ok(runner.includes('--pastors-applied "$APPLIED" --socials-applied "$SOC_APPLIED"'), 'dashboard must preserve separate pastor and social counts');
assert.ok(runner.includes('MERGE_MUTATED=1'), 'operational stamp detection must remain wired');
assert.ok(runner.includes('operational checkpoint pushed:'), 'zero-content rounds must persist operational markers so selectors advance');
assert.ok(runner.includes('Directory refine checkpoint: +0 content fields'), 'zero-content checkpoints must be explicitly labeled and skip deploy');
assert.ok(!runner.includes('zero applied — skip qa-sample/grind-stats/regen/commit/push'), 'zero-content rounds must not leave canonical operational mutations dirty');
assert.ok(runner.includes('NOTHING TO GRIND'), 'cold apply lanes must exit without commit');
const salvageCall = runner.indexOf('land_head_on_main || die "push failed after rebase retry — commit stranded in autopilot worktree"');
const salvageRefetch = runner.indexOf('git fetch -q origin main || die "post-salvage refetch failed"');
const destructiveReset = runner.indexOf('git reset -q --hard FETCH_HEAD');
assert.ok(salvageCall >= 0 && salvageRefetch > salvageCall && destructiveReset > salvageRefetch,
  'a successful stranded-commit salvage must refresh FETCH_HEAD before the destructive reset');
assert.ok(sbcAutopilot.includes('sourceRecoveryEligible'),
  'persistent SBC preflight must share the exact source-recovery eligibility predicate');
assert.ok(!sbcAutopilot.includes('const done=new Set()'),
  'autopilot preflight must not hide scraped-but-unmerged rows behind a ledger');
const tickLedgerReset = sbcAutopilot.indexOf('rm -f "$JSONL_PATH"');
const tickScrape = sbcAutopilot.indexOf('node scripts/scrape-sbc-detail.js');
assert.ok(tickLedgerReset >= 0 && tickScrape > tickLedgerReset,
  'each autopilot tick must scrape into a fresh ledger before merging only that batch');

const cold = { fresh: 0, retry: 5, social: 5, source_recovery: 0 };
const streaksCold = { fresh: 0, retry: 3, social: 3 };
assert.strictEqual(lanes.chooseLane(cold, null, streaksCold), 'nothing-to-grind');
assert.strictEqual(lanes.chooseLane({ fresh: 0, retry: 5, social: 5, source_recovery: 10 }, null, streaksCold), 'source-recovery');
assert.strictEqual(lanes.chooseLane({ fresh: 100, retry: 0, social: 0, source_recovery: 10 }, null, { fresh: 3, retry: 3, social: 3 }), 'fresh');
const streaksThaw = { fresh: 0, retry: 3, social: 3 };
assert.strictEqual(lanes.chooseLane({ fresh: 2, retry: 5, social: 5 }, null, streaksThaw), 'fresh');
assert.strictEqual(lanes.chooseLane({ fresh: 0, retry: 5, social: 5 }, null, { fresh: 0, retry: 0, social: 3 }), 'retry');
assert.ok(runner.includes('LANE-DEAD'), 'cold apply lanes must emit LANE-DEAD');

const session = fs.readFileSync(path.join(ROOT, 'scripts/directory-grind-session.sh'), 'utf8');
assert.ok(session.includes('pastor-refine-local.sh'), 'session wrapper must invoke the refine runner');
assert.ok(session.includes('yield gate HALT'), 'wrapper must honor runner exit 3 as a clean dead-pool stop');
assert.ok(!session.includes('aborted: fresh pool'),
  'session wrapper must not abort when fresh < 10; runner yield-gate owns fallthrough to source-recovery');
assert.ok(!session.includes('aborted: 3 consecutive +0 rounds'),
  'session wrapper must not stop while operational checkpoints can advance into frontier work');
assert.ok(session.indexOf('publish verified live:') < session.indexOf('Directory grind — verified live result'),
  'completion notice must only be emitted after live verification');
assert.ok(session.includes('commit-tree'), 'deploy trigger must attach to current origin/main instead of a stale detached HEAD');
assert.ok(session.includes('GRIND_MAX_ROUNDS'), 'wrapper must support a one-round bounded verification run');

const { summarizeLines } = require(path.join(ROOT, 'scripts/summarize-grind-session.js'));
const summary = summarizeLines([
  '[x] frontier lane done: source-recovery attempted=10 applied=11',
  '[x] frontier lane done: source-recovery attempted=10 applied=17',
  '[x] frontier lane done: source-recovery attempted=10 applied=16',
  '[x] pushed: +13 content fields (0 pastors, 13 socials), operational_mutation=1 (11 attempted)',
  '[x] frontier lane done: source-recovery attempted=10 applied=15',
  '[x] operational checkpoint pushed: mode=fresh attempted=4 mutated=1',
]);
assert.deepStrictEqual(summary, {
  attempted: 55,
  content_applied: 72,
  pastors_applied: 0,
  socials_applied: 13,
  frontier_applied: 59,
  productive_rounds: 5,
  zero_content_rounds: 1,
  operational_checkpoints: 1,
  other_profile_applied: 0,
}, 'session summary must report durable structured yield instead of a stale schema snapshot');

const plan = cp.execFileSync('/bin/bash', [path.join(ROOT, 'scripts/continuous-enrichment-lane.sh'), '/tmp/prl-test'], {
  cwd: ROOT,
  env: { ...process.env, CONTINUOUS_PLAN_ONLY: '1' },
  encoding: 'utf8',
});
assert.match(plan, /^lane=(fresh|retry|social|website-discovery|source-recovery|monitoring|nothing-to-grind)\b/, 'planner must report a recognized next lane after live data changes');

console.log('grind-lanes: all assertions passed');
