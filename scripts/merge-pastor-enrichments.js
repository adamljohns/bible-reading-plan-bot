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
const { makeWriter } = require('./lib/format-preserving-write.js');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

// A pastor field is a PLACEHOLDER (safe to overwrite with a researched name) when it's
// empty, a bare honorific/word, or a "look it up" phrase. A real "Pastor John Smith" is
// NOT a placeholder — the `\bpastor\b` honorific must not match real names.
function isPlaceholderPastor(p) {
  if (!p || !String(p).trim()) return true;
  const s = String(p).trim();
  if (/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)) return true;
  if (/verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s)) return true;
  return false;
}

// Apply a verified social URL only if the church lacks it and the value is a real
// http(s) URL on the expected platform host. Verified-only; never guess.
const SOCIAL_HOST = { facebook: /facebook\.com/i, youtube: /youtube\.com|youtu\.be/i, instagram: /instagram\.com/i };
function applySocials(c, e) {
  let n = 0;
  for (const k of ['facebook', 'youtube', 'instagram']) {
    const v = e[k];
    if (typeof v === 'string' && /^https?:\/\//i.test(v) && SOCIAL_HOST[k].test(v) && !c[k]) {
      c[k] = v.trim();
      n++;
    }
  }
  return n;
}

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

// Byte-format-preserving read+write (ASCII-escaped, no trailing newline) — plain
// JSON.stringify here re-encodes every non-ASCII char into a ~50k-line diff.
const { data: d, write: writeChurches } = makeWriter(CHURCHES);
let pastorsApplied = 0, brokenSites = 0, noPastorFound = 0, idsNotFound = 0, alreadyHasPastor = 0, socialsApplied = 0, femaleSeniorPastors = 0;
const stillNeedsReview = [];

for (const c of d.churches) {
  if (!c || !c.id) continue;
  const e = enrichments.get(c.id);
  if (!e) continue;

  // Track website status — broken websites are NOT a doctrinal red flag
  // (small churches often use Facebook or other social instead of a website).
  // Note the issue + keep needs_review for follow-up social-channel research,
  // but DO NOT downgrade the overall rating.
  if (e.website_status && /404|timeout|ssl_error|redirect_loop|not_a_church/.test(e.website_status)) {
    brokenSites++;
    const noteAppend = `[${TODAY}] Phase 6f live-fetch verdict: ${e.website_status}. Site may be defunct or church may use Facebook/social instead of website. NOT a doctrinal flag — research social channel before publishing.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
    c.needs_review = true;
    continue;
  }

  // Apply any verified social links the agent found (independent of the pastor outcome —
  // a church can have a real FB/YouTube/IG even when no pastor name is parseable).
  socialsApplied += applySocials(c, e);

  if (e.pastor_name && typeof e.pastor_name === 'string' && e.pastor_name.trim()) {
    const previouslyVerifyPlaceholder = isPlaceholderPastor(c.pastor);
    if (previouslyVerifyPlaceholder) {
      c.pastor = e.pastor_name.trim();
      pastorsApplied++;
      // Rubric enforcement: a verified FEMALE senior/lead pastor is RED minimum on
      // Gender and overall. Enriching the name must not leave a now-known
      // egalitarian church sitting green/yellow. Flag for human confirmation.
      if (e.pastor_is_female === true) {
        c.overall_rating = 'red';
        c.scores = c.scores || {};
        c.scores.gender = 'red';
        c.tags = Array.isArray(c.tags) ? c.tags : [];
        if (!c.tags.includes('needs-rating-review')) c.tags.push('needs-rating-review');
        c.needs_review = true;
        femaleSeniorPastors++;
        const gNote = `[${TODAY}] Female senior/lead pastor identified ("${e.pastor_name}") — auto-set Gender + overall to RED per MOOP rubric; confirm egalitarian polity before publishing.`;
        c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + gNote : gNote;
      }
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
writeChurches(d);

console.log('Results:');
console.log(`  Pastors applied:              ${pastorsApplied}`);
console.log(`  Social links applied:         ${socialsApplied}`);
console.log(`  Female senior pastor → RED:   ${femaleSeniorPastors}`);
console.log(`  Broken websites flagged red:  ${brokenSites}`);
console.log(`  No pastor parseable (200_no_pastor_found): ${noPastorFound}`);
console.log(`  Already had real pastor:       ${alreadyHasPastor}`);
console.log(`  Enrichment IDs not found in MOOP: ${idsNotFound}`);
console.log(`  Still needs_review:            ${stillNeedsReview.length}`);
