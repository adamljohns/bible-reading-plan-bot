#!/usr/bin/env node
// Append one row to docs/data/grind-stats.json (the dashboard time-series).
// Unlike the old inline snippet, this records the TOTAL remaining enrichment work
// across all three tiers (fresh+retry+social) — so the dashboard stops showing "0"
// the moment the fresh tier drains — plus US coverage vs the ~350k-congregation
// national universe (the real frontier is DISCOVERY, not enrichment).
//
// Usage: append-grind-stats.js --mode fresh --attempted 50 --found 12
const fs = require('fs'), path = require('path');
const lanes = require('./lib/grind-lanes.js');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

const ROOT = path.join(__dirname, '..');
const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/data/churches.json'), 'utf8')).churches;

const counts = lanes.countLanes(d);
const pool_fresh = counts.fresh, pool_retry = counts.retry, pool_social = counts.social;

const US_UNIVERSE = 350000; // ~congregations, 2020 U.S. Religion Census
const us_total = d.filter(c => c.country_code === 'US' || !c.country_code).length;

const mode = arg('--mode', 'fresh');
const applied = parseInt(arg('--applied', arg('--found', '0')), 10);
if (lanes.APPLY_LANES.includes(mode)) {
  lanes.recordLaneHop(mode, applied, ROOT);
}

const row = {
  ts: arg('--ts', new Date().toISOString().slice(0, 16)),
  mode,
  attempted: parseInt(arg('--attempted', '0'), 10),
  found: parseInt(arg('--found', '0'), 10),
  applied,
  pastors_applied: parseInt(arg('--pastors-applied', arg('--found', '0')), 10),
  socials_applied: parseInt(arg('--socials-applied', '0'), 10),
  records_updated: parseInt(arg('--records-updated', '0'), 10),
  pool_fresh, pool_retry, pool_social,
  enrich_remaining: pool_fresh + pool_retry + pool_social,
  pool_website_discovery: counts.website_discovery,
  pool_source_recovery: counts.source_recovery,
  pool_source_recovery_exhausted: counts.source_recovery_exhausted,
  pool_pastor_exhausted: counts.pastor_exhausted,
  pool_dead_site_recovery: counts.dead_site_recovery,
  pool_human_review: counts.human_review,
  product_backlog: counts.product_backlog,
  total_churches: d.length,
  us_total,
  us_coverage_pct: +(us_total / US_UNIVERSE * 100).toFixed(1),
  real_pastors: d.filter(c => !lanes.isPlaceholderPastor(c.pastor)).length,
  rosters: d.filter(c => Array.isArray(c.pastors) && c.pastors.length).length,
  socials_any: d.filter(c => c.facebook || c.youtube || c.instagram).length,
  needs_review: d.filter(c => c.needs_review === true).length,
  // legacy field kept so old dashboard code doesn't break
  pool_after: pool_fresh + pool_retry + pool_social,
};

const P = path.join(ROOT, 'docs/data/grind-stats.json');
let j = { series: [] };
try { j = JSON.parse(fs.readFileSync(P, 'utf8')); } catch (_) { }
j.series.push(row);
j.series = j.series.slice(-500);
fs.writeFileSync(P, JSON.stringify(j, null, 1));
console.log('grind-stats row:', JSON.stringify({ mode: row.mode, found: row.found, enrich_remaining: row.enrich_remaining, us_coverage_pct: row.us_coverage_pct }));
