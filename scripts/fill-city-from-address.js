#!/usr/bin/env node
/**
 * Backfill the `city` field from each record's OWN address string.
 *
 * 95% of the directory carried no `city` even though the city sits verbatim in
 * `address`. Nothing here is inferred or looked up: every value is a substring of
 * the record's own address. Records whose address genuinely names no city keep an
 * honest blank rather than a guess from a ZIP centroid.
 */
const fs = require('fs'), path = require('path');
const { makeWriter } = require(path.join(__dirname, 'lib', 'format-preserving-write.js'));
const APPLY = process.argv.includes('--apply');
const P = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

const STATES = 'Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming|District of Columbia';
const NAMEPART = "[A-Za-z][A-Za-z .'-]{1,34}?";
const BAD = /^(po box|p ?o ?box|suite|ste|unit|apt|floor|fl|rear|attn|c\/o|\d|@)/i;
// The capture occasionally runs past the street into the city ("11555 St., Marys
// Church Road Charlotte Hall, MD") or swallows a venue ("Virginia Cultural Arts Ctr
// Abingdon"). Every such value ran to 4+ words. A word-count guard catches all of
// them and costs nothing: US city names in this data top out at 3 words.
// Do NOT filter on street/venue WORDS -- a first attempt did, and threw away 307
// real cities including Falls Church (28 records, and a Northern Virginia city),
// St. Louis, Chapel Hill, Port St Lucie, Wesley Chapel and Sioux Center.
const TOO_MANY_WORDS = v => v.trim().split(/\s+/).length >= 4;

function cityFrom(addr) {
  let a = String(addr || '').replace(/\s+/g, ' ').trim();
  if (!a) return '';
  a = a.replace(/,?\s*United States(\s+of\s+America)?\s*/i, ' ').replace(/,?\s*USA\b\s*/i, ' ').replace(/\s+/g, ' ').trim();
  let m;
  if ((m = a.match(new RegExp(',\\s*(' + NAMEPART + ')\\s*,\\s*(?:[A-Z]{2}|' + STATES + ')\\b', 'i')))) return m[1];
  if ((m = a.match(new RegExp(',\\s*(' + NAMEPART + ')\\s+(?:' + STATES + ')\\b', 'i')))) return m[1];
  // ", Royersford PA, 19468" / ", Royersford PA 19468" -- state abbreviation, no comma before it
  if ((m = a.match(new RegExp(',\\s*(' + NAMEPART + ')\\s+[A-Z]{2}\\b\\s*,?\\s*\\d{5}\\b')))) return m[1];
  if ((m = a.match(/,\s*([A-Za-z][A-Za-z .'-]{1,34}?)\s*,\s*\d{5}\b/))) return m[1];
  if ((m = a.match(new RegExp('^\\s*(' + NAMEPART + ')\\s*,\\s*(?:[A-Z]{2}|' + STATES + ')\\b', 'i')))) return m[1];
  return '';
}

const SAMPLE = process.argv.includes('--sample');
const { data, write } = makeWriter(P);
let filled = 0, skipped = 0, blank = 0;
const picks = [], suspicious = [];
const byState = {};
for (const c of data.churches) {
  if (c.city && String(c.city).trim()) continue;
  const v = cityFrom(c.address).trim().replace(/\s+/g, ' ');
  if (!v) { blank++; continue; }
  if (BAD.test(v) || v.length < 2 || TOO_MANY_WORDS(v)) { skipped++; continue; }
  if (APPLY) { c.city = v; c._city_from_address = '2026-09-09'; }
  if (SAMPLE) {
    if (/\d/.test(v) || v.length > 28) suspicious.push([v, c.address]);
    if (filled % 2200 === 0) picks.push([v, c.state || '?', c.address]);
  }
  filled++;
  const s = c.state || '?'; byState[s] = (byState[s] || 0) + 1;
}
console.log((APPLY ? 'APPLIED' : 'DRY RUN') + ` — filled ${filled} | rejected ${skipped} | honest blank ${blank}`);
console.log('  top states:', Object.entries(byState).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => k + ':' + v).join(' '));
if (SAMPLE) {
  console.log('\n  suspicious (digit / overlong):', suspicious.length);
  suspicious.slice(0, 6).forEach(([v, a]) => console.log('     "' + v + '"  <- ' + String(a).slice(0, 58)));
  console.log('\n  spot-check:');
  picks.slice(0, 12).forEach(([v, st, a]) => console.log('     ' + v.padEnd(22) + st + '   <- ' + String(a).slice(0, 54)));
}
if (APPLY) { write(data); console.log('  written; total churches', data.churches.length); }
