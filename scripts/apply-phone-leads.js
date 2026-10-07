#!/usr/bin/env node
/**
 * Apply pre-verified phone leads to churches.json — fills BLANK phones only.
 *
 * Each lead was read off the church's OWN website (the record's `website`): a
 * single local tel: link, or the single local-area-code number in the page text.
 * The lead keeps the source URL and the verbatim text around the number. Leads
 * whose number appeared on more than one record were dropped at harvest — those
 * point at duplicate records or a borrowed website, not at a phone.
 *
 * NEVER run while the grind holds /tmp/directory-grind-session.lock — the grind
 * owns churches.json while it runs. Afterwards regenerate pages + indexes and run
 * node scripts/check-consistency.js.
 *
 * Report-first; --apply writes. Usage:
 *   node scripts/apply-phone-leads.js --leads scripts/qa/fxbg-phone-leads-2026-10-06.json [--apply]
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
    : c.phone ? `already has phone ${c.phone}`
    : !/^\(\d{3}\) \d{3}-\d{4}$/.test(L.phone) ? 'malformed phone in lead' : '';
  if (why) { skip++; console.log(`SKIP ${L.id} — ${why}`); continue; }
  ok++;
  if (!APPLY) continue;
  c.phone = L.phone;
  const note = `[${TODAY}] Phone ${L.phone} from the church's own website (${L.method}): ${L.source}`;
  c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
}
console.log(`${APPLY ? 'applied' : 'would apply'} ${ok}, skipped ${skip}`);
if (APPLY && ok) write(d);
