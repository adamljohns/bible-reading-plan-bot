#!/usr/bin/env node
/**
 * Apply pre-verified geocode leads to churches.json — fills BLANK coordinates only.
 *
 * Each lead carries the exact US Census Geocoder query URL that produced it, the
 * address it was asked about and the address Census matched. A lead is applied
 * only when the record is still ungeocoded AND its address is still the one that
 * was geocoded, so a stale leads file can never move a pin. The query URL stays
 * in the leads file (in git) as the audit trail; the record gets geocode_source.
 *
 * NEVER run while the grind holds /tmp/directory-grind-session.lock — the grind
 * owns churches.json while it runs. Afterwards: node scripts/build-directory-map.js
 * && node scripts/check-consistency.js.
 *
 * Report-first; --apply writes. Usage:
 *   node scripts/apply-geocode-leads.js --leads scripts/qa/fxbg-geocode-leads-2026-10-06.json [--apply]
 */
const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const APPLY = args.includes('--apply');
const LEADS = opt('--leads', '');
if (!LEADS) { console.error('--leads <file> required'); process.exit(1); }
if (APPLY && fs.existsSync('/tmp/directory-grind-session.lock')) {
  console.error('REFUSING: /tmp/directory-grind-session.lock exists — the grind owns churches.json. Re-run when the session ends.');
  process.exit(2);
}

const TODAY = new Date().toISOString().slice(0, 10);
const leads = JSON.parse(fs.readFileSync(LEADS, 'utf8'));
const { data: d, write } = makeWriter(path.join(__dirname, '..', 'docs/data/churches.json'));
const byId = new Map(d.churches.map(c => [String(c.id), c]));

let ok = 0, skip = 0;
for (const L of leads) {
  const c = byId.get(String(L.id));
  const why = !c ? 'id not found'
    : (c.latitude != null && c.longitude != null) ? 'already geocoded'
    : String(c.address || '') !== L.address ? `address changed to "${c.address || ''}"`
    : !(Number.isFinite(L.latitude) && Number.isFinite(L.longitude)) ? 'bad coordinates in lead' : '';
  if (why) { skip++; console.log(`SKIP ${L.id} — ${why}`); continue; }
  ok++;
  if (!APPLY) continue;
  c.latitude = L.latitude;
  c.longitude = L.longitude;
  c.geocoded_at = TODAY;
  c.geocode_source = 'census';
}
console.log(`${APPLY ? 'applied' : 'would apply'} ${ok}, skipped ${skip}`);
if (APPLY && ok) write(d);
