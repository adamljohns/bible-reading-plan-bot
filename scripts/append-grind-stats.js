#!/usr/bin/env node
// Append one row to docs/data/grind-stats.json (the dashboard time-series).
// Unlike the old inline snippet, this records the TOTAL remaining enrichment work
// across all three tiers (fresh+retry+social) — so the dashboard stops showing "0"
// the moment the fresh tier drains — plus US coverage vs the ~350k-congregation
// national universe (the real frontier is DISCOVERY, not enrichment).
//
// Usage: append-grind-stats.js --mode fresh --attempted 50 --found 12
const fs = require('fs'), path = require('path');
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };

const ROOT = path.join(__dirname, '..');
const d = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/data/churches.json'), 'utf8')).churches;

// ── eligibility, mirrored from select-enrichment-batch.js (keep in sync) ──
const AB = new Set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' '));
const FULL = new Set(['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']);
const isPh = p => { const s = String(p || '').trim(); return !s || /^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s) || /verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s); };
const isUS = c => { const s = String(c.state || '').toUpperCase().trim(); return AB.has(s) || FULL.has(s); };
const isEnglish = n => typeof n === 'string' && !/[^\x00-\x7F]/.test(n);
const hasWebsite = c => typeof c.website === 'string' && /^https?:\/\//i.test(c.website);
const notesText = c => Array.isArray(c.enrichment_notes) ? c.enrichment_notes.join(' ') : String(c.enrichment_notes || '');
const attempted = c => { const n = notesText(c); if (n.lastIndexOf('junk-pastor-reset') > n.lastIndexOf('Phase 6f')) return false; return !!c._loop_round_attempted || !!c._verify_round_attempted || /Phase 6f/i.test(n); };
const strikes = c => (notesText(c).match(/no parseable pastor/gi) || []).length;
const fetchable = c => isPh(c.pastor) && hasWebsite(c) && isEnglish(c.name) && isUS(c);

const pool_fresh = d.filter(c => fetchable(c) && !attempted(c)).length;
const pool_retry = d.filter(c => fetchable(c) && attempted(c) && strikes(c) === 1).length;
const pool_social = d.filter(c => hasWebsite(c) && !c.facebook && !c.youtube && !c.instagram && isEnglish(c.name) && isUS(c) && !c._social_attempted).length;

const US_UNIVERSE = 350000; // ~congregations, 2020 U.S. Religion Census
const us_total = d.filter(c => c.country_code === 'US' || !c.country_code).length;

const row = {
  ts: arg('--ts', new Date().toISOString().slice(0, 16)),
  mode: arg('--mode', 'fresh'),
  attempted: parseInt(arg('--attempted', '0'), 10),
  found: parseInt(arg('--found', '0'), 10),
  pool_fresh, pool_retry, pool_social,
  enrich_remaining: pool_fresh + pool_retry + pool_social,
  total_churches: d.length,
  us_total,
  us_coverage_pct: +(us_total / US_UNIVERSE * 100).toFixed(1),
  real_pastors: d.filter(c => !isPh(c.pastor)).length,
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
