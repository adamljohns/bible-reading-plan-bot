#!/usr/bin/env node
// scripts/merge-image-scrapes.js
//
// Reads /tmp/image-scrapes.jsonl (produced by scrape-church-images.js
// --jsonl) and applies each result to docs/data/churches.json. Runs as the
// SINGLE writer to churches.json during the image-enrichment cycle — the
// scraper itself stays read-only on churches.json, eliminating the race
// condition that bit us with the v1 autopilot.
//
// Idempotent: re-running over the same JSONL just overwrites the same
// fields with the same values. If a record was already applied, no harm.
//
// Usage:
//   node scripts/merge-image-scrapes.js                          # default JSONL path
//   node scripts/merge-image-scrapes.js --jsonl /tmp/foo.jsonl   # custom path
//   node scripts/merge-image-scrapes.js --truncate-after-merge   # clear JSONL once applied

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DEFAULT_JSONL = '/tmp/image-scrapes.jsonl';

function parseArgs() {
  const out = { jsonl: DEFAULT_JSONL, truncate: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--jsonl') out.jsonl = a[++i];
    else if (a[i] === '--truncate-after-merge') out.truncate = true;
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
  console.log(`Reading ${lines.length} scrape results from ${args.jsonl}`);
  const results = [];
  for (const l of lines) {
    try { results.push(JSON.parse(l)); } catch (e) {}
  }

  const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const byId = new Map();
  for (const c of data.churches) {
    byId.set(c.id || c.slug, c);
  }

  let applied = 0, missing = 0, gotImage = 0, gotNoImage = 0, gotFail = 0;
  for (const r of results) {
    const c = byId.get(r.id);
    if (!c) { missing++; continue; }
    // Apply image-related fields. Skip the id field itself.
    for (const [k, v] of Object.entries(r)) {
      if (k === 'id') continue;
      if (v === null) c[k] = null;
      else c[k] = v;
    }
    applied++;
    if (r.image_url || r.image_thumb) gotImage++;
    else if (r.image_source === 'website-no-image') gotNoImage++;
    else if (r.image_source && r.image_source.startsWith('fetch-failed')) gotFail++;
  }
  fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2));
  console.log(`Applied ${applied} results to ${CHURCHES}`);
  console.log(`  with image:   ${gotImage}`);
  console.log(`  no-image:     ${gotNoImage}`);
  console.log(`  fetch-failed: ${gotFail}`);
  if (missing) console.log(`  missing (no matching church.id): ${missing}`);

  // Coverage check
  const withImg = data.churches.filter(c => c.image_url || c.image_thumb).length;
  const fetched = data.churches.filter(c => c.image_fetched_at).length;
  console.log(`\nCoverage now: ${withImg} churches with image (${fetched} total fetched)`);

  if (args.truncate) {
    fs.writeFileSync(args.jsonl, '');
    console.log(`Truncated ${args.jsonl} (applied results cleared)`);
  }
}

main();
