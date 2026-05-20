#!/usr/bin/env node
// Stage 4 of SBC bulk-load: merge /tmp/sbc-scraped/*.jsonl into
// docs/data/churches.json with proper schema.
//
// Each new record is created with:
//   id / slug    = SBC's URL slug
//   name         = cleaned page title (strips " – SBC Churches Directory" suffix + decodes &#8211; etc.)
//   address      = "<city>, <state> <zip>"
//   denomination = "Baptist"
//   denomination_family = "Southern Baptist (SBC)"
//   cross_listed_in     = ["sbc"]
//   overall_rating      = "yellow"   (default — awaiting individual evaluation)
//   source_url          = original SBC.net URL
//   needs_review        = true
//   notes               = ["Bulk-imported from sbc.net directory YYYY-MM-DD"]
//
// Dedup: skips records whose slug or normalized name already matches an
// existing entry. Conservative — when in doubt, skip.
//
// After merging, run `node generate-church-pages.js` to materialize per-church
// HTML pages and `node scripts/build-sitemap-churches.js` to update the sitemap.

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs/data/churches.json');
const SCRAPED_DIR = '/tmp/sbc-scraped';
const TODAY = new Date().toISOString().slice(0, 10);

function cleanName(raw) {
  if (!raw) return null;
  // Strip the " – SBC Churches Directory" suffix (note the en-dash, may be HTML-encoded)
  let s = raw
    .replace(/&#8211;|&#8212;|&ndash;|&mdash;/g, '–')
    .replace(/\s*[–—-]\s*SBC Churches Directory\s*$/i, '')
    .replace(/&amp;/g, '&')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&nbsp;/g, ' ')
    .trim();
  return s;
}

function normalizeForMatch(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .replace(/\b(the|a|an|of|at|on|in|for|to|and|&)\b/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
console.log(`Loaded ${d.churches.length} existing churches.`);

// Existing-record indexes for dedup
const slugIndex = new Set();
const nameStateIndex = new Set();
for (const c of d.churches) {
  if (c.slug) slugIndex.add(c.slug.toLowerCase());
  if (c.id) slugIndex.add(c.id.toLowerCase());
  const addr = c.address || '';
  const stMatch = addr.match(/,\s*([A-Z]{2})\b/);
  const state = stMatch ? stMatch[1] : '';
  const key = normalizeForMatch(c.name) + '|' + state;
  if (c.name && key !== '|') nameStateIndex.add(key);
}

// Read all scraped batches
const scrapedRecs = [];
if (fs.existsSync(SCRAPED_DIR)) {
  for (const f of fs.readdirSync(SCRAPED_DIR)) {
    if (!f.endsWith('.jsonl')) continue;
    const lines = fs.readFileSync(path.join(SCRAPED_DIR, f), 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const o = JSON.parse(line);
        if (!o.fetch_error && o.city && o.state) scrapedRecs.push(o);
      } catch {}
    }
  }
}
console.log(`Found ${scrapedRecs.length} successfully-scraped records across all batches.`);

let added = 0;
let skippedSlug = 0;
let skippedName = 0;
let skippedBadData = 0;

for (const rec of scrapedRecs) {
  const slug = rec.slug.toLowerCase();
  const cleanedName = cleanName(rec.name);
  if (!cleanedName || cleanedName.length < 3) { skippedBadData++; continue; }

  if (slugIndex.has(slug)) { skippedSlug++; continue; }

  const stateKey = normalizeForMatch(cleanedName) + '|' + (rec.state || '');
  if (nameStateIndex.has(stateKey)) { skippedName++; continue; }

  // Build address
  let addr = rec.city + ', ' + rec.state;
  if (rec.zip) addr += ' ' + rec.zip;

  const newRec = {
    id: rec.slug,
    slug: rec.slug,
    name: cleanedName,
    address: addr,
    pastor: 'Verify on church website',
    denomination: 'Baptist',
    denomination_family: 'Southern Baptist (SBC)',
    cross_listed_in: ['sbc'],
    overall_rating: 'yellow',
    signatures_aggregate: 'none',
    needs_review: true,
    source_url: rec.url,
    notes: [`Bulk-imported from sbc.net directory ${TODAY}; awaiting individual evaluation against the MOOP rubric.`],
    engagement: { researched_website: false },
    // Empty scorecard so generate-church-pages.js can render without crashing.
    // The rubric rows default to yellow until a human evaluator fills these in.
    scores: {},
    score_notes: {},
    assessment: '',
    _sbc_bulkload: TODAY,
  };

  d.churches.push(newRec);
  slugIndex.add(slug);
  nameStateIndex.add(stateKey);
  added++;
}

console.log(`\nMerge results:`);
console.log(`  Added (net-new):           ${added}`);
console.log(`  Skipped (slug match):      ${skippedSlug}`);
console.log(`  Skipped (name+state match): ${skippedName}`);
console.log(`  Skipped (bad data):        ${skippedBadData}`);

if (added > 0) {
  // Bump directory version metadata
  d.churches.sort((a, b) => (a.id || a.slug || '').localeCompare(b.id || b.slug || ''));
  d.directory_updated = TODAY;
  d.last_sbc_bulkload = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2));
  console.log(`\nWrote ${CHURCHES} — ${d.churches.length} churches total.`);
  console.log(`\nNext steps:`);
  console.log(`  1. node generate-church-pages.js          (regenerate per-church HTML)`);
  console.log(`  2. node scripts/build-sitemap-churches.js (update sitemap)`);
  console.log(`  3. git add docs/data/churches.json docs/churches/ docs/sitemap-churches.xml`);
  console.log(`  4. git commit + push`);
} else {
  console.log('\nNothing to add; churches.json unchanged.');
}
