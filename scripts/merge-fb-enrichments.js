#!/usr/bin/env node
// Merge Facebook URL enrichments into churches.json.
//
// Reads one or more JSON files (arrays of {id, facebook_url, status}),
// applies facebook_url to the matching church record, and notes that the
// church may primarily use Facebook instead of (or alongside) a website.
//
// This supports Adam's "we may offer to build $100 websites" ministry
// outreach — every record where status='found' becomes a potential
// outreach candidate.
//
// Usage:
//   node scripts/merge-fb-enrichments.js               # auto-discover /tmp/fb-enriched-*.json
//   node scripts/merge-fb-enrichments.js --input <path>

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

const args = process.argv.slice(2);
let inputs = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input') inputs.push(args[++i]);
}
if (inputs.length === 0) {
  inputs = fs.readdirSync('/tmp')
    .filter(f => /^fb-enriched-\d+\.json$/.test(f))
    .map(f => path.join('/tmp', f));
}

if (!inputs.length) {
  console.error('No FB enrichment files found. Pass --input <path> or place at /tmp/fb-enriched-N.json');
  process.exit(1);
}

function normalizeFB(url) {
  if (!url || typeof url !== 'string') return null;
  let u = url.trim();
  if (!/^https?:/i.test(u)) u = 'https://' + u;
  // Strip facebook.com or m.facebook.com or web.facebook.com → use canonical www.facebook.com
  u = u.replace(/^https?:\/\/(m\.|web\.|mobile\.)?facebook\.com/i, 'https://www.facebook.com');
  // Strip query strings + trailing slash
  u = u.split('?')[0].split('#')[0].replace(/\/$/, '');
  if (!/^https?:\/\/www\.facebook\.com\//.test(u)) return null;
  if (/\/groups\//.test(u)) return null;  // Reject groups
  return u;
}

const enrichments = new Map();
console.log(`Reading ${inputs.length} FB enrichment files:`);
for (const p of inputs) {
  const arr = JSON.parse(fs.readFileSync(p, 'utf8'));
  console.log(`  ${path.basename(p)}: ${arr.length} entries`);
  for (const e of arr) {
    if (e && e.id) enrichments.set(e.id, e);
  }
}
console.log(`Total unique enrichment entries: ${enrichments.size}\n`);

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
let fbApplied = 0, alreadyHadFB = 0, notFound = 0, groupOnly = 0, uncertain = 0, idsNotInMoop = 0;

for (const c of d.churches) {
  if (!c || !c.id) continue;
  const e = enrichments.get(c.id);
  if (!e) continue;

  if (e.status === 'found' && e.facebook_url) {
    const normalized = normalizeFB(e.facebook_url);
    if (!normalized) {
      // Couldn't normalize — treat as not_found
      notFound++;
      continue;
    }
    if (c.facebook && c.facebook === normalized) {
      alreadyHadFB++;
      continue;
    }
    c.facebook = normalized;
    fbApplied++;
    const note = `[${TODAY}] FB-finder live-search: official Facebook page identified at ${normalized}. Church may use this as primary online presence in lieu of a working website.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
  } else if (e.status === 'not_found') {
    notFound++;
    const note = `[${TODAY}] FB-finder live-search: no official Facebook page found for this church. Possible candidate for the "MOOP $100 website build" ministry outreach.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
  } else if (e.status === 'facebook_group_only') {
    groupOnly++;
  } else if (e.status === 'uncertain') {
    uncertain++;
  }
}

// Sanity: how many enrichment IDs did we NOT find in churches.json?
for (const [id] of enrichments) {
  const c = d.churches.find(c => c && c.id === id);
  if (!c) idsNotInMoop++;
}

d.directory_updated = TODAY;
fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');

console.log('Results:');
console.log(`  Facebook URLs applied:           ${fbApplied}`);
console.log(`  Already had same FB URL:         ${alreadyHadFB}`);
console.log(`  Not found (potential outreach):  ${notFound}`);
console.log(`  Group-only (won't use):          ${groupOnly}`);
console.log(`  Uncertain matches (skipped):     ${uncertain}`);
console.log(`  Enrichment IDs not in MOOP:       ${idsNotInMoop}`);
