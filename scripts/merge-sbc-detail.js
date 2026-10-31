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
const { validateSourceIdentity } = require('./lib/sbc-detail-identity.js');

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

  let applied = 0, missing = 0, addedWebsite = 0, addedGeo = 0, addedPhone = 0, errored = 0, identityHeld = 0, identitySkipped = 0;
  for (const line of lines) {
    let r; try { r = JSON.parse(line); } catch (e) { continue; }
    const c = byId.get(r.id);
    if (!c) { missing++; continue; }
    const identityError = validateSourceIdentity(c, r);
    if (identityError) {
      if (identityError === 'missing source postal identity evidence') {
        // Old JSONL rows (no sbc_detail_fetched_at) lack identity evidence; ignore
        // them without mutating canonical state. A FRESH scrape that still cannot
        // supply a source postal code (PR / non-US-format source pages) is a real
        // strike: without it the same records re-entered source-recovery every
        // round forever (2026-10-29..31: 420 rounds, 0 fields, 5 records).
        if (r.sbc_detail_fetched_at) {
          const failedAt = r.sbc_detail_fetched_at;
          if (c.sbc_detail_failed_at !== failedAt) {
            c._sbc_detail_failures = Number(c._sbc_detail_failures || 0) + 1;
          }
          c.sbc_detail_failed_at = failedAt;
          c.sbc_detail_error = `IDENTITY: ${identityError}`;
          errored++;
          applied++;
          continue;
        }
        identitySkipped++;
        continue;
      }
      identityHeld++;
      c._hold_review = 'sbc-source-identity-mismatch';
      c.sbc_detail_failed_at = r.sbc_detail_fetched_at || new Date().toISOString();
      c.sbc_detail_error = `IDENTITY: ${identityError}`;
      applied++;
      continue;
    }
    if (r.sbc_detail_error) {
      errored++;
      const failedAt = r.sbc_detail_failed_at || new Date().toISOString();
      if (c.sbc_detail_failed_at !== failedAt) {
        c._sbc_detail_failures = Number(c._sbc_detail_failures || 0) + 1;
      }
      c.sbc_detail_failed_at = failedAt;
      c.sbc_detail_error = r.sbc_detail_error;
    }
    // Apply website only if missing AND the URL actually has a host (the scraper
    // also guards this; defense in depth here in case an older JSONL still has
    // scheme-only artifacts).
    if (r.website && /^https?:\/\/[^\/\s]/i.test(r.website) && (!c.website || args.force)) {
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
    if (r.sbc_detail_fetched_at) {
      c.sbc_detail_fetched_at = r.sbc_detail_fetched_at;
      if (c._hold_review === 'sbc-source-identity-mismatch') delete c._hold_review;
      delete c._sbc_detail_failures;
      delete c.sbc_detail_failed_at;
      delete c.sbc_detail_error;
    }
    applied++;
  }
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));

  console.log(`Applied ${applied} results from ${args.jsonl}`);
  console.log(`  +${addedWebsite} websites`);
  console.log(`  +${addedGeo} geocodes (sbc.net coords)`);
  console.log(`  +${addedPhone} phones`);
  console.log(`  ${errored} had scrape-time errors`);
  if (identityHeld) console.log(`  ${identityHeld} held for source-identity review`);
  if (identitySkipped) console.log(`  ${identitySkipped} legacy results skipped without identity evidence`);
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
