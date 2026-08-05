#!/usr/bin/env node
//
// merge-church-social.js — fold scrape-church-social.js JSONL results into
// churches.json.
//
// Fill-only by design: an existing handle is never overwritten. The scraper
// reads a church's own website, so a conflict means either the site changed
// or a human curated the old value — either way that is a review question,
// not something a batch job should silently decide. Conflicts are counted
// and can be listed with --show-conflicts.
//
// Usage:
//   node scripts/merge-church-social.js --input /tmp/social-scrapes.jsonl
//   node scripts/merge-church-social.js --input /tmp/social-scrapes.jsonl --dry-run
//   node scripts/merge-church-social.js --input a.jsonl --input b.jsonl
//

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);
const PLATFORMS = ['facebook', 'youtube', 'instagram', 'twitter', 'tiktok'];

const args = process.argv.slice(2);
const inputs = [];
let dryRun = false, showConflicts = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input') inputs.push(args[++i]);
  else if (args[i] === '--dry-run') dryRun = true;
  else if (args[i] === '--show-conflicts') showConflicts = true;
}
if (!inputs.length) {
  const def = '/tmp/social-scrapes.jsonl';
  if (fs.existsSync(def)) inputs.push(def);
}
if (!inputs.length) {
  console.error('No input JSONL. Pass --input <path>.');
  process.exit(1);
}

// Two URLs can name the same profile while differing as strings: a stored
// trailing slash, http vs https, a www, or YouTube's three interchangeable
// handle forms (/user/x, /c/x, /@x). Comparing raw strings reports thousands
// of "conflicts" that are nothing of the kind, which would bury the handful
// of real disagreements worth a human's time.
function canonical(url) {
  if (!url || typeof url !== 'string') return '';
  let u = url.trim().toLowerCase();
  u = u.replace(/^http:\/\//, 'https://');
  u = u.replace(/^https:\/\/(www\.|m\.|web\.|mobile\.)/, 'https://');
  u = u.split('?')[0].split('#')[0].replace(/\/+$/, '');
  // YouTube: compare the bare handle, not which of the three prefixes was used.
  u = u.replace(/^https:\/\/youtube\.com\/(?:user|c)\/(.+)$/, 'https://youtube.com/@$1');
  u = u.replace(/^https:\/\/youtube\.com\/@/, 'https://youtube.com/@');
  return u;
}

function sameProfile(a, b) {
  const ca = canonical(a), cb = canonical(b);
  if (!ca || !cb) return false;
  if (ca === cb) return true;
  // /@handle vs /channel/UC... cannot be compared — treat as a real conflict.
  return false;
}

// Last record for a given id wins — a rerun supersedes an earlier attempt.
const recs = new Map();
for (const p of inputs) {
  let n = 0;
  for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r && r.id) { recs.set(r.id, r); n++; }
    } catch (e) { /* tolerate a torn final line from a killed run */ }
  }
  console.log(`  ${path.basename(p)}: ${n} records`);
}
console.log(`Unique church ids in scrape set: ${recs.size}\n`);

const db = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const stats = { visited: 0, filled: 0, churchesTouched: 0, already: 0, conflict: 0, none: 0, error: 0, missing: 0 };
const byPlatform = Object.fromEntries(PLATFORMS.map(p => [p, 0]));
const conflicts = [];

for (const c of db.churches) {
  if (!c || !c.id) continue;
  const r = recs.get(c.id);
  if (!r) continue;
  stats.visited++;

  if (r.status === 'error') { stats.error++; c._social_scraped = TODAY; continue; }
  if (r.status === 'none') { stats.none++; c._social_scraped = TODAY; continue; }

  const added = [];
  for (const p of PLATFORMS) {
    // Early scrape runs emitted `x_twitter`; the schema's canonical field
    // (and the only one generate-church-pages.js renders) is `twitter`.
    const val = p === 'twitter' ? (r.twitter || r.x_twitter) : r[p];
    if (!val) continue;
    if (!c[p]) {
      c[p] = val;
      added.push(p);
      byPlatform[p]++;
      stats.filled++;
    } else if (!sameProfile(c[p], val)) {
      stats.conflict++;
      conflicts.push({ id: c.id, platform: p, existing: c[p], scraped: val });
    } else {
      stats.already++;
    }
  }

  c._social_scraped = TODAY;
  if (added.length) {
    stats.churchesTouched++;
    c._social_source = r.final_url || r.website;
    const note = `[${TODAY}] Social harvest: ${added.join(', ')} read directly from the church's own website (${r.final_url || r.website}).`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
  }
}

for (const id of recs.keys()) {
  if (!db.churches.some(c => c && c.id === id)) stats.missing++;
}

console.log('Results:');
console.log(`  Church records visited:       ${stats.visited}`);
console.log(`  Churches gaining a handle:    ${stats.churchesTouched}`);
console.log(`  Handles filled (total):       ${stats.filled}`);
for (const p of PLATFORMS) console.log(`      ${p.padEnd(12)}            ${byPlatform[p]}`);
console.log(`  Already had identical value:  ${stats.already}`);
console.log(`  Conflicts (kept existing):    ${stats.conflict}`);
console.log(`  Site had no social links:     ${stats.none}`);
console.log(`  Fetch errors:                 ${stats.error}`);
console.log(`  Scrape ids not in directory:  ${stats.missing}`);

if (showConflicts && conflicts.length) {
  console.log('\nConflicts (existing value kept — review by hand):');
  for (const x of conflicts.slice(0, 60)) {
    console.log(`  ${x.id} [${x.platform}]\n     have: ${x.existing}\n     saw:  ${x.scraped}`);
  }
  if (conflicts.length > 60) console.log(`  ... and ${conflicts.length - 60} more`);
}

if (dryRun) {
  console.log('\n--dry-run: churches.json NOT written.');
  process.exit(0);
}

if (stats.filled > 0 || stats.visited > 0) {
  db.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(db, null, 2) + '\n');
  console.log(`\nWrote ${CHURCHES}`);
} else {
  console.log('\nNothing to write.');
}
