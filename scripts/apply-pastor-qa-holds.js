#!/usr/bin/env node
/**
 * Put already-PUBLISHED lead-pastor names back on HOLD after QA.
 *
 * merge-pastor-enrichments.js holds a typically-female lead name before it is
 * ever written. A name that slipped past an older guard (or arrived by a harvest
 * replay) is already on the page; this moves it into the same held state the
 * guard would have produced: `pastor` / `pastors[]` cleared, the exact published
 * values and their source kept verbatim in enrichment_notes, `_hold_review`
 * stamped so the church leaves the automated pools, `needs_review` set for the
 * Principal's rubric review. Nothing is discarded and nothing is invented.
 *
 * Acts only when the record's current `pastor` still equals the held name, so a
 * stale holds file can never clear a name someone has since corrected.
 *
 * NEVER run while the grind holds /tmp/directory-grind-session.lock or the
 * round lock — the grind owns churches.json while it runs.
 *
 * Report-first; --apply writes. Usage:
 *   node scripts/apply-pastor-qa-holds.js --holds scripts/qa/pastor-holds-2026-10-06.json [--apply]
 */
const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const APPLY = args.includes('--apply');
const HOLDS = opt('--holds', '');
if (!HOLDS) { console.error('--holds <file> required'); process.exit(1); }
if (APPLY && fs.existsSync('/tmp/directory-grind-session.lock')) {
  console.error('REFUSING: /tmp/directory-grind-session.lock exists — the grind owns churches.json. Re-run when the session ends.');
  process.exit(2);
}

const TODAY = new Date().toISOString().slice(0, 10);
const holds = JSON.parse(fs.readFileSync(HOLDS, 'utf8'));
const { data: d, write } = makeWriter(path.join(__dirname, '..', 'docs/data/churches.json'));
const byId = new Map(d.churches.map(c => [String(c.id), c]));

let held = 0;
for (const h of holds) {
  const c = byId.get(String(h.id));
  if (!c) { console.log(`SKIP ${h.id} — id not found`); continue; }
  if (String(c.pastor || '').trim() !== h.pastor) { console.log(`SKIP ${h.id} — pastor is now "${c.pastor || ''}", not "${h.pastor}"`); continue; }
  const roster = Array.isArray(c.pastors) && c.pastors.length ? ` Published roster was: ${JSON.stringify(c.pastors)}.` : '';
  const note = `[${TODAY}] QA hold: published lead-pastor "${h.pastor}" has a typically-female first name and was never rubric-reviewed — moved back to HOLD for manual MOOP-rubric review (name removed from page, kept here). Source: ${h.source}. ${h.evidence}${roster}`;
  console.log(`HOLD ${h.id} — "${h.pastor}"${roster ? ' (+roster)' : ''}`);
  if (!APPLY) continue;
  c.pastor = '';
  delete c.pastors;
  c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
  c.needs_review = true;
  c._hold_review = TODAY;
  held++;
}
if (APPLY) { write(d); console.log(`applied ${held} hold(s) — now rebuild pages/indexes and run check-consistency.js`); }
else console.log('(report only — pass --apply to write)');
