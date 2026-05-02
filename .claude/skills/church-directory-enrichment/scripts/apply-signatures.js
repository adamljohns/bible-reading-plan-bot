#!/usr/bin/env node
// Apply the signature-matches.json report to churches.json.
//
// Usage:
//   node .claude/skills/church-directory-enrichment/scripts/apply-signatures.js
//   node .claude/skills/church-directory-enrichment/scripts/apply-signatures.js --report /custom/path.json
//
// Behavior:
// - Default report path: /tmp/signature-matches.json (output of signature-crossref.js).
// - For every match, populates church.signatories[list_key] with the candidate name
//   (deduped) and recomputes signatures_aggregate from current state.
// - For confirmed-red drift cases (listed in confirmed-red-drift.json sidecar),
//   ALSO downgrades overall_rating to "yellow" if it was "green", sets
//   scores.cultural = "red", and adds tags ["needs-rating-review", "cultural-drift-flag"].
//
// Important: does NOT auto-downgrade based on red signatures alone — only if the
// church ID is in the confirmed-red-drift sidecar. Common-name false-positives
// are real (22,901 Nashville signers, 13,167 Dallas signers) and the bar for
// rating impact is geographic/presbytery corroboration.

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..', '..', '..');
const CHURCHES_PATH = path.join(REPO_ROOT, 'docs', 'data', 'churches.json');
const DRIFT_PATH = path.join(SCRIPT_DIR, 'confirmed-red-drift.json');

let reportPath = '/tmp/signature-matches.json';
const argReport = process.argv.indexOf('--report');
if (argReport !== -1 && process.argv[argReport + 1]) {
  reportPath = process.argv[argReport + 1];
}

if (!fs.existsSync(reportPath)) {
  console.error(`Report not found: ${reportPath}`);
  console.error('Run signature-crossref.js first to generate it.');
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(CHURCHES_PATH, 'utf8'));
const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

let confirmedRedIds = new Set();
if (fs.existsSync(DRIFT_PATH)) {
  const drift = JSON.parse(fs.readFileSync(DRIFT_PATH, 'utf8'));
  confirmedRedIds = new Set((drift.confirmed_red_drift || []).map(d => String(d.id)));
  console.log(`Loaded ${confirmedRedIds.size} confirmed-red-drift IDs from sidecar.`);
} else {
  console.log('No confirmed-red-drift.json sidecar — proceeding with no auto-downgrades.');
}

// Direction map per manifest (kept inline so this script doesn't need the manifest at runtime;
// if the canonical lists change, update both.)
const dirMap = {
  warhurst_protest_2020: 'red',
  amr_2026: 'red',
  letter_of_lament_2025: 'red',
  revoice_2018_2026: 'red',
  cbe_egalitarian_2026: 'red',
  dallas_statement_2018: 'green',
  nashville_statement_2017: 'green',
};

const churchById = new Map();
for (const c of data.churches) churchById.set(String(c.id), c);

let appliedSignatures = 0;
let driftDowngrades = 0;

for (const m of report.matches) {
  const church = churchById.get(String(m.church_id));
  if (!church) continue;
  if (!church.signatories) {
    church.signatories = {
      warhurst_protest_2020: [], amr_2026: [], letter_of_lament_2025: [],
      revoice_2018_2026: [], cbe_egalitarian_2026: [],
      dallas_statement_2018: [], nashville_statement_2017: [],
    };
  }
  for (const ml of m.matches) {
    if (!church.signatories[ml.key]) church.signatories[ml.key] = [];
    if (!church.signatories[ml.key].includes(m.candidate_name)) {
      church.signatories[ml.key].push(m.candidate_name);
      appliedSignatures++;
    }
  }
  // Recompute signatures_aggregate.
  const dirsPresent = new Set();
  for (const [k, arr] of Object.entries(church.signatories)) {
    if (arr.length > 0) dirsPresent.add(dirMap[k]);
  }
  if (dirsPresent.has('red') && dirsPresent.has('green')) church.signatures_aggregate = 'mixed';
  else if (dirsPresent.has('red')) church.signatures_aggregate = 'red';
  else if (dirsPresent.has('green')) church.signatures_aggregate = 'green';
  else church.signatures_aggregate = 'none';
}

// Apply confirmed-red drift downgrades (idempotent).
for (const id of confirmedRedIds) {
  const c = churchById.get(id);
  if (!c) {
    console.error(`DRIFT MISS: ${id} not in directory`);
    continue;
  }
  const prevRating = c.overall_rating;
  if (c.overall_rating === 'green') c.overall_rating = 'yellow';
  if (!c.scores) c.scores = {};
  c.scores.cultural = 'red';
  if (!c.score_notes) c.score_notes = {};
  if (!c.score_notes.cultural || !/cultural drift marker/i.test(c.score_notes.cultural)) {
    c.score_notes.cultural =
      'Pastor matches a red-direction signature list (Warhurst/AMR/Lament/Revoice/CBE) WITH state/presbytery corroboration — cultural drift marker per drift-watch protocol. Auto-applied YELLOW + cultural=red downgrade. ' +
      (c.score_notes.cultural || '');
    c.score_notes.cultural = c.score_notes.cultural.trim();
  }
  if (!c.tags) c.tags = [];
  if (!c.tags.includes('needs-rating-review')) c.tags.push('needs-rating-review');
  if (!c.tags.includes('cultural-drift-flag')) c.tags.push('cultural-drift-flag');
  console.log(`DRIFT DOWNGRADE: ${id} ${prevRating} -> ${c.overall_rating}`);
  driftDowngrades++;
}

data.directory_updated = new Date().toISOString().slice(0, 10);
fs.writeFileSync(CHURCHES_PATH, JSON.stringify(data, null, 2) + '\n');

console.log('');
console.log(`Applied ${appliedSignatures} signature populations across ${report.matches.length} matched records.`);
console.log(`Confirmed-red drift downgrades touched: ${driftDowngrades}.`);
console.log(`Total churches: ${data.churches.length}.`);
