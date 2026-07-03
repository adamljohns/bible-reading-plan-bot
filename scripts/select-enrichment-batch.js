#!/usr/bin/env node
/**
 * Select a batch of churches eligible for pastor enrichment — and write ready-to-run
 * batch files for the research agents.
 *
 * EXCLUDES already-attempted churches on TWO signals:
 *   1. the `_loop_round_attempted` / `_verify_round_attempted` flags, and
 *   2. any church whose `enrichment_notes` already carry a "Phase 6f" live-fetch
 *      marker (found / no-pastor / broken).
 * Selecting on the flags alone re-attempts churches tried on a prior run and stacks
 * DUPLICATE "no parseable pastor" notes — the selection gap found 2026-07-02, when a
 * batch re-hit ~6 Acts2 CA churches already attempted 2026-06-17.
 *
 * Eligible = needs_review && placeholder-pastor && http(s) website && US state &&
 *            ASCII/English name && not previously attempted.
 *
 * Usage:
 *   node scripts/select-enrichment-batch.js [--count 60] [--batches 3] [--out /tmp]
 *
 * Writes <out>/enrich-batch-1.json .. -<batches>.json (deterministic id-sorted,
 * round-robin split) — each an array of {id,name,city,state,website,denomination}.
 * Prints the eligible pool size and what it wrote. Read-only on churches.json.
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 && args[i + 1] ? args[i + 1] : def; };
const COUNT = parseInt(opt('--count', '60'), 10);
const BATCHES = parseInt(opt('--batches', '3'), 10);
const OUT = opt('--out', '/tmp');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const churches = JSON.parse(fs.readFileSync(CHURCHES, 'utf8')).churches;

const AB = new Set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' '));
const FULL = new Set(['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']);

// A pastor field is a PLACEHOLDER (safe to overwrite with a researched name) when it's
// empty, a bare honorific/word, or a "look it up" phrase. Mirrors merge-pastor-enrichments.js.
function isPlaceholderPastor(p) {
  if (!p || !String(p).trim()) return true;
  const s = String(p).trim();
  if (/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)) return true;
  if (/verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s)) return true;
  return false;
}
const isUS = c => { const s = String(c.state || '').toUpperCase().trim(); return AB.has(s) || FULL.has(s); };
const isEnglish = n => typeof n === 'string' && !/[^\x00-\x7F]/.test(n);
const notesText = c => Array.isArray(c.enrichment_notes) ? c.enrichment_notes.join(' ') : String(c.enrichment_notes || '');
const alreadyAttempted = c => !!c._loop_round_attempted || !!c._verify_round_attempted || /Phase 6f/i.test(notesText(c));

const eligible = churches.filter(c =>
  c.needs_review === true &&
  isPlaceholderPastor(c.pastor) &&
  typeof c.website === 'string' && /^https?:\/\//i.test(c.website) &&
  isEnglish(c.name) &&
  isUS(c) &&
  !alreadyAttempted(c)
);
eligible.sort((a, b) => String(a.id).localeCompare(String(b.id)));

console.log(`Eligible pool (never-attempted, pastor-fetchable): ${eligible.length}`);
const pick = eligible.slice(0, COUNT);
const slim = c => ({ id: c.id, name: c.name, city: c.city || null, state: c.state, website: c.website, denomination: c.denomination || c.denomination_family || null });
const batches = Array.from({ length: BATCHES }, () => []);
pick.forEach((c, i) => batches[i % BATCHES].push(slim(c)));
batches.forEach((b, i) => {
  const f = path.join(OUT, `enrich-batch-${i + 1}.json`);
  fs.writeFileSync(f, JSON.stringify(b, null, 2));
  console.log(`  wrote ${f}: ${b.length} churches`);
});
console.log(`Selected ${pick.length} of ${eligible.length} eligible into ${BATCHES} batch file(s).`);
