#!/usr/bin/env node
/**
 * Re-file Virginia churches into their correct region using scripts/lib/va-regions.js.
 *
 * Report-first: prints every move and writes nothing without --apply. Uses the
 * format-preserving ASCII writer so churches.json keeps its canon and the diff
 * stays proportional to the change (not 50k lines).
 *
 * Adam, 2026-08-16: add a real "Roanoke / Southwest VA" region rather than
 * folding the far southwest into Shenandoah.
 *
 * Usage: node scripts/reclassify-va-regions.js [--apply]
 */
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');
const { reclassify } = require('./lib/va-regions.js');

const APPLY = process.argv.includes('--apply');
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);

const moves = [];
for (const c of d.churches) {
  if (c.state !== 'VA') continue;
  const next = reclassify(c);
  if (!next) continue;
  moves.push({ c, from: c.region || '(none)', to: next });
}

const tally = {};
for (const m of moves) {
  const k = `${m.from} -> ${m.to}`;
  tally[k] = (tally[k] || 0) + 1;
}

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — ${moves.length} Virginia churches change region\n`);
Object.entries(tally).sort((a, b) => b[1] - a[1]).forEach(([k, n]) => console.log(`  ${String(n).padStart(4)}  ${k}`));

if (APPLY && moves.length) {
  const TODAY = new Date().toISOString().slice(0, 10);
  for (const m of moves) {
    m.c.region = m.to;
    const note = `[${TODAY}] Region re-filed ${m.from} -> ${m.to} by ZIP/city classifier (scripts/lib/va-regions.js).`;
    if (!String(m.c.enrichment_notes || '').includes(note)) {
      m.c.enrichment_notes = m.c.enrichment_notes ? `${m.c.enrichment_notes}\n${note}` : note;
    }
  }
  write(d);
  console.log(`\nWrote ${moves.length} region changes.`);
} else if (!APPLY) {
  console.log('\nDry run — re-run with --apply to write.');
}
