#!/usr/bin/env node
// Curate website-outreach-candidates.json:
//   - Filter to US-only (drop obvious foreign records; the $100 website ministry
//     is for stateside churches in our outreach reach)
//   - Cross-reference each candidate against current churches.json — drop entries
//     whose record has since been deleted, and refresh fields that may have
//     drifted (rating, denomination, signatures_aggregate, current pastor)
//   - Sort by editorial priority: orthodox-aligned signatures first, then by
//     rating (green > yellow > red > unset), then by network membership
//   - Write back to the same file path
//
// Usage:
//   node scripts/curate-outreach-candidates.js [--dry-run]

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const CANDIDATES = path.join(__dirname, '..', 'docs', 'data', 'research-leads', 'website-outreach-candidates.json');
const DRY_RUN = process.argv.includes('--dry-run');

const FOREIGN_COUNTRY_PATTERN = /\b(philippines|italy|hungary|united kingdom|uk|england|scotland|wales|northern ireland|poland|spain|france|germany|australia|new zealand|canada|mexico|brazil|argentina|south africa|kenya|nigeria|india|japan|south korea|china|netherlands|belgium|sweden|norway|denmark|finland|austria|switzerland|ireland|portugal|greece|turkey|israel|egypt|morocco|peru|colombia|venezuela|chile|ecuador|bolivia|uruguay|paraguay|costa rica|guatemala|el salvador|honduras|nicaragua|panama)\b/i;
const US_STATE_CODE_PATTERN = /,\s*([A-Z]{2})\s*\d{5}/;
const US_STATE_CODE_LOOSE = /\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\b/;

function isUs(record, moopRecord) {
  // Foreign-country hit anywhere → reject
  if (FOREIGN_COUNTRY_PATTERN.test(record.address || '')) return false;
  if (moopRecord) {
    if (FOREIGN_COUNTRY_PATTERN.test(moopRecord.address || '')) return false;
    if (FOREIGN_COUNTRY_PATTERN.test(moopRecord.country || '')) return false;
  }
  // Strong US signal: state code + ZIP, or explicit "USA"/"United States"
  const text = (record.address || '') + ' ' + (moopRecord ? (moopRecord.address || '') : '');
  if (US_STATE_CODE_PATTERN.test(text)) return true;
  if (/\b(USA|United States)\b/i.test(text)) return true;
  // Loose signal: address contains an US state code; slug ends with a state code
  if (US_STATE_CODE_LOOSE.test(text)) return true;
  if (record.id && /-([a-z]{2})$/i.test(record.id)) {
    const slugState = record.id.match(/-([a-z]{2})$/i)[1].toUpperCase();
    if (US_STATE_CODE_LOOSE.test(slugState)) return true;
  }
  return false;
}

const cands = JSON.parse(fs.readFileSync(CANDIDATES, 'utf8'));
const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const moopById = new Map();
for (const c of d.churches) if (c && c.id) moopById.set(c.id, c);

const enriched = [];
let dropped_foreign = 0;
let dropped_missing = 0;
let dropped_already_has_website = 0;
let kept = 0;

for (const cand of cands) {
  const moop = moopById.get(cand.id);
  if (!moop) {
    dropped_missing++;
    continue;
  }
  if (!isUs(cand, moop)) {
    dropped_foreign++;
    continue;
  }
  // If MOOP now has a working website AND/OR Facebook for this church, no
  // longer a $100-build candidate.
  const hasWebsiteNow = moop.website && typeof moop.website === 'string' && /^https?:/i.test(moop.website) && !/website-defunct|404|not-found|defunct/.test(String(moop.enrichment_notes || ''));
  // We don't have a freshness check on the website status, so be conservative:
  // only drop if the original status said website-defunct but they now also
  // have a facebook URL (so we wouldn't be selling a website to a church
  // that has working social).
  if (moop.facebook && /defunct/.test(String(cand.status))) {
    dropped_already_has_website++;
    continue;
  }
  enriched.push({
    id: cand.id,
    name: moop.name || cand.name,
    address: moop.address || cand.address,
    pastor: moop.pastor || cand.pastor,
    denomination: moop.denomination || cand.denomination,
    cross_listed_in: moop.cross_listed_in || cand.cross_listed_in || [],
    overall_rating: moop.overall_rating || 'unrated',
    signatures_aggregate: moop.signatures_aggregate || 'none',
    facebook: moop.facebook || null,
    source_url: cand.source_url,
    status: cand.status,
    pitch: cand.pitch,
  });
  kept++;
}

// Sort by editorial priority:
//   1. signatures_aggregate green records first (orthodox-aligned trajectory)
//   2. overall_rating green/yellow before red/black
//   3. records cross-listed in any conservative network before those not
//   4. alphabetical by name
const RATING_ORDER = { green: 0, yellow: 1, red: 2, black: 3, dead: 4, unrated: 5 };
const SIG_ORDER = { green: 0, mixed: 1, none: 2, red: 3 };

enriched.sort((a, b) => {
  const sa = SIG_ORDER[a.signatures_aggregate] ?? 99;
  const sb = SIG_ORDER[b.signatures_aggregate] ?? 99;
  if (sa !== sb) return sa - sb;
  const ra = RATING_ORDER[a.overall_rating] ?? 99;
  const rb = RATING_ORDER[b.overall_rating] ?? 99;
  if (ra !== rb) return ra - rb;
  const na = (a.cross_listed_in || []).length;
  const nb = (b.cross_listed_in || []).length;
  if (na !== nb) return nb - na;
  return (a.name || '').localeCompare(b.name || '');
});

if (!DRY_RUN) {
  fs.writeFileSync(CANDIDATES, JSON.stringify(enriched, null, 2) + '\n');
}

console.log('Outreach Candidate Curation:');
console.log(`  Original candidates:           ${cands.length}`);
console.log(`  Dropped (foreign):             ${dropped_foreign}`);
console.log(`  Dropped (record missing):      ${dropped_missing}`);
console.log(`  Dropped (now has FB+defunct):  ${dropped_already_has_website}`);
console.log(`  Kept + enriched:               ${kept}`);

console.log('\nDistribution by rating + signatures:');
const dist = {};
for (const e of enriched) {
  const k = `${e.overall_rating || 'unrated'} / sig=${e.signatures_aggregate}`;
  dist[k] = (dist[k] || 0) + 1;
}
for (const [k, v] of Object.entries(dist).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${k.padEnd(35)} ${v}`);
}

console.log('\nTop 20 priority candidates (after sort):');
for (const e of enriched.slice(0, 20)) {
  const sig = e.signatures_aggregate === 'green' ? ' SIG-G' : e.signatures_aggregate === 'red' ? ' SIG-R' : e.signatures_aggregate === 'mixed' ? ' SIG-M' : '      ';
  const networks = (e.cross_listed_in || []).join(',') || '-';
  console.log(`  [${e.overall_rating.padEnd(6)}${sig}] ${(e.name || '').slice(0, 45).padEnd(45)} ${(e.address || '').slice(0, 32).padEnd(32)} (${networks})`);
}
