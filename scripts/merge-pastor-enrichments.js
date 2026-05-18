#!/usr/bin/env node
// Phase 6f — Apply agent-produced pastor enrichments to churches.json.
//
// Reads one or more /tmp/9marks-pastor-enriched-*.json files, each an array
// of { id, pastor_name, pastor_source_url, website_status }.
// For each enriched record:
//   - If pastor_name is real (not null), set church.pastor = pastor_name,
//     append the source to enrichment_sources, append a note, and CLEAR
//     needs_review if it was solely flagged for missing pastor.
//   - If website_status indicates broken site (404 / timeout / not_a_church),
//     downgrade overall_rating to "red" and keep needs_review=true.
//   - "200_no_pastor_found" → leave as-is (still needs human review).
//
// Usage:
//   node scripts/merge-pastor-enrichments.js                  # auto-discover /tmp/9marks-pastor-enriched-*.json
//   node scripts/merge-pastor-enrichments.js --input <path>   # specific file

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
    .filter(f => /^9marks-pastor-enriched-\d+\.json$/.test(f))
    .map(f => path.join('/tmp', f));
}

if (!inputs.length) {
  console.error('No enrichment files found. Place at /tmp/9marks-pastor-enriched-N.json or pass --input.');
  process.exit(1);
}

console.log(`Reading ${inputs.length} enrichment files:`);
const enrichments = new Map();
for (const p of inputs) {
  const arr = JSON.parse(fs.readFileSync(p, 'utf8'));
  console.log(`  ${path.basename(p)}: ${arr.length} entries`);
  for (const e of arr) {
    if (e && e.id) enrichments.set(e.id, e);
  }
}
console.log(`Total unique enrichment entries: ${enrichments.size}\n`);

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
let pastorsApplied = 0, brokenSites = 0, noPastorFound = 0, idsNotFound = 0, alreadyHasPastor = 0;
const stillNeedsReview = [];

for (const c of d.churches) {
  if (!c || !c.id) continue;
  const e = enrichments.get(c.id);
  if (!e) continue;

  // Track website status downgrades
  if (e.website_status && /404|timeout|ssl_error|redirect_loop|not_a_church/.test(e.website_status)) {
    // Downgrade rating; keep needs_review
    if (c.overall_rating !== 'red' && c.overall_rating !== 'black') {
      c.overall_rating = 'red';
      c.overall_label = `${c.overall_label || 'unrated'} (website ${e.website_status} on ${TODAY})`;
    }
    if (!c.scores) c.scores = {};
    // Reduce denominational score on broken-site finding
    c.scores.denominational = 'red';
    brokenSites++;
    const noteAppend = `[${TODAY}] Phase 6f live-fetch verdict: ${e.website_status}. Site does not resolve to a working church homepage.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
    c.needs_review = true;
    continue;
  }

  if (e.pastor_name && typeof e.pastor_name === 'string' && e.pastor_name.trim()) {
    const previouslyVerifyPlaceholder = !c.pastor || /verify|unknown/i.test(String(c.pastor));
    if (previouslyVerifyPlaceholder) {
      c.pastor = e.pastor_name.trim();
      pastorsApplied++;
      if (Array.isArray(c.enrichment_sources)) {
        if (e.pastor_source_url && !c.enrichment_sources.includes(e.pastor_source_url)) {
          c.enrichment_sources.push(e.pastor_source_url);
        }
      } else if (e.pastor_source_url) {
        c.enrichment_sources = [e.pastor_source_url];
      }
      const noteAppend = `[${TODAY}] Phase 6f pastor live-fetched: "${e.pastor_name}" from ${e.pastor_source_url || 'church website'}.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
      // Clear needs_review IF it was set solely because pastor was missing.
      // Heuristic: if record was added by Phase 6 networks integrate and now has
      // a real pastor + working website, clear needs_review.
      if (c.needs_review && /Added via .* Phase 2/.test(String(c.enrichment_notes || ''))) {
        c.needs_review = false;
      }
    } else {
      alreadyHasPastor++;
    }
    continue;
  }

  if (e.website_status === '200_no_pastor_found') {
    noPastorFound++;
    const noteAppend = `[${TODAY}] Phase 6f live-fetched but no parseable pastor name on standard pages (/about, /staff, /leaders). Site OK.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
    stillNeedsReview.push(c.id);
  }
}

// Sanity: how many enrichment IDs did we NOT find in churches.json?
for (const [id] of enrichments) {
  const c = d.churches.find(c => c && c.id === id);
  if (!c) idsNotFound++;
}

d.directory_updated = TODAY;
fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');

console.log('Results:');
console.log(`  Pastors applied:              ${pastorsApplied}`);
console.log(`  Broken websites flagged red:  ${brokenSites}`);
console.log(`  No pastor parseable (200_no_pastor_found): ${noPastorFound}`);
console.log(`  Already had real pastor:       ${alreadyHasPastor}`);
console.log(`  Enrichment IDs not found in MOOP: ${idsNotFound}`);
console.log(`  Still needs_review:            ${stillNeedsReview.length}`);
