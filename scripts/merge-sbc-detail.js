#!/usr/bin/env node
// scripts/merge-sbc-detail.js
//
// Reads /tmp/sbc-detail.jsonl (from scrape-sbc-detail.js) and applies each
// result to docs/data/churches.json. Single-writer pattern — same race-free
// approach as merge-image-scrapes.js.
//
// Fields applied per matched church:
//   - website (only if missing — never overwrite a curated website)
//   - latitude + longitude (only if missing or geocode_source != 'census')
//   - phone (only if missing)
//   - sbc_detail_fetched_at (audit)

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/sbc-detail.jsonl';

function parseArgs() {
  const out = { jsonl: DEFAULT_JSONL, force: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--jsonl') out.jsonl = a[++i];
    else if (a[i] === '--force') out.force = true;
  }
  return out;
}

function main() {
  const args = parseArgs();
  if (!fs.existsSync(args.jsonl)) {
    console.log(`No JSONL at ${args.jsonl} — nothing to merge.`);
    return;
  }
  const lines = fs.readFileSync(args.jsonl, 'utf8').split('\n').filter(Boolean);
  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const byId = new Map();
  for (const c of data.churches) byId.set(c.id || c.slug, c);

  let applied = 0, missing = 0, addedWebsite = 0, addedGeo = 0, addedPhone = 0, errored = 0;
  for (const line of lines) {
    let r; try { r = JSON.parse(line); } catch (e) { continue; }
    const c = byId.get(r.id);
    if (!c) { missing++; continue; }
    if (r.sbc_detail_error) { errored++; }
    // Apply website only if missing (don't overwrite curated)
    if (r.website && (!c.website || args.force)) {
      c.website = r.website;
      addedWebsite++;
    }
    // Apply geo if missing OR if our previous geocode came from Census (sbc.net's coords are likely more accurate since they're official-registered)
    if (typeof r.latitude === 'number' && (typeof c.latitude !== 'number' || c.geocode_source === 'census' || args.force)) {
      c.latitude = r.latitude;
      c.longitude = r.longitude;
      c.geocode_source = r.geocode_source || 'sbc.net';
      addedGeo++;
    }
    // Apply phone if missing
    if (r.phone && (!c.phone || args.force)) {
      c.phone = r.phone;
      addedPhone++;
    }
    if (r.sbc_detail_fetched_at) c.sbc_detail_fetched_at = r.sbc_detail_fetched_at;
    applied++;
  }
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));

  console.log(`Applied ${applied} results from ${args.jsonl}`);
  console.log(`  +${addedWebsite} websites`);
  console.log(`  +${addedGeo} geocodes (sbc.net coords)`);
  console.log(`  +${addedPhone} phones`);
  console.log(`  ${errored} had scrape-time errors`);
  if (missing) console.log(`  ${missing} JSONL records had no matching church.id`);

  // Coverage check on SBC subset
  const sbc = data.churches.filter(c => c.source_url && c.source_url.includes('churches.sbc.net'));
  const sbcWithWebsite = sbc.filter(c => c.website && /^https?:/i.test(c.website)).length;
  const sbcGeocoded = sbc.filter(c => typeof c.latitude === 'number').length;
  console.log(`\nSBC coverage now: ${sbc.length} records total`);
  console.log(`  with website:  ${sbcWithWebsite} (${Math.round(sbcWithWebsite/sbc.length*100)}%)`);
  console.log(`  with geocode:  ${sbcGeocoded} (${Math.round(sbcGeocoded/sbc.length*100)}%)`);
}

main();
