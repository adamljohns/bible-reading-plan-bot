#!/usr/bin/env node
// Signature cross-reference report.
// Loads all 7 reference signature lists per the manifest, normalizes pastor
// names from churches.json, and emits /tmp/signature-matches.json with the
// candidates that AREN'T already recorded in their target signatories field.
//
// Usage:
//   node .claude/skills/church-directory-enrichment/scripts/signature-crossref.js
//
// Output:
//   /tmp/signature-matches.json — feed to apply-signatures.js to populate.
//
// Direction key (per manifest):
//   red  = soft-progressive / drift markers (warhurst, amr, lament, revoice, cbe)
//   green = orthodox sexual ethics + anti-CRT (dallas, nashville)
//
// FALSE-POSITIVE WARNING: name-only matching is real-FP risk. apply-signatures.js
// gates rating downgrades to STATE-CORROBORATED red matches only.

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..', '..', '..');
const DATA_DIR = path.join(REPO_ROOT, 'docs', 'data');
const CHURCHES_PATH = path.join(DATA_DIR, 'churches.json');
const MANIFEST_PATH = path.join(DATA_DIR, 'statement-lists-manifest.json');
const OUTPUT_PATH = '/tmp/signature-matches.json';

const churches = JSON.parse(fs.readFileSync(CHURCHES_PATH, 'utf8'));
const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));

function norm(name) {
  if (!name || typeof name !== 'string') return '';
  return name
    .toLowerCase()
    .replace(/\b(rev|pastor|dr|elder|deacon|te|re|fr|prof)\.?\s+/gi, '')
    .replace(/\s+(jr|sr|ii|iii|iv|v|m\.div|d\.min|ph\.d|d\.d|esq)\.?$/gi, '')
    .replace(/[.,;:'"()]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

// nameIndex: normalized-name -> [{ key, label, direction, signer }, ...]
const nameIndex = new Map();
let totalSigners = 0;

for (const list of manifest.lists) {
  const filePath = path.join(DATA_DIR, list.file);
  if (!fs.existsSync(filePath)) {
    console.error(`MISSING: ${filePath}`);
    continue;
  }
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const signers = data[list.signers_array_key] || [];
  if (!Array.isArray(signers)) {
    console.error(`Not array: ${list.key} -> ${list.signers_array_key}`);
    continue;
  }
  let count = 0;
  for (const s of signers) {
    const name = (typeof s === 'string') ? s : (s.name || s.full_name || '');
    if (!name) continue;
    const k = norm(name);
    if (k.split(' ').length < 2) continue; // require first + last
    if (!nameIndex.has(k)) nameIndex.set(k, []);
    nameIndex.get(k).push({
      key: list.key,
      label: list.label,
      direction: list.direction,
      signer: typeof s === 'string' ? { name } : s,
    });
    count++;
  }
  console.error(`Loaded ${list.key}: ${count} signers`);
  totalSigners += count;
}
console.error(`Total signer records: ${totalSigners}; unique normalized names: ${nameIndex.size}`);

const matches = [];
for (const c of churches.churches) {
  if (!c.pastor || typeof c.pastor !== 'string') continue;
  // Extract bare names from pastor field. Common patterns:
  //   "John Smith"
  //   "Pastor John Smith"
  //   "John Smith (verify)"
  //   "John Smith and Bob Jones"
  //   "Rev. John Smith (Senior); Bob Jones (Associate)"
  const candidates = c.pastor
    .replace(/\([^)]*\)/g, '')
    .replace(/[—\-]\s+(verified|verify|unknown|.*?\b20\d\d\b).*/i, '')
    .replace(/;\s*verify.*/i, '')
    .split(/\s+(?:and|&|;|,)\s+/i)
    .map(s => s.trim())
    .filter(s => s.length > 0);

  for (const candidate of candidates) {
    const k = norm(candidate);
    if (k.split(' ').length < 2) continue;
    if (!nameIndex.has(k)) continue;
    const lists = nameIndex.get(k);
    matches.push({
      church_id: c.id,
      church_name: c.name,
      church_state: (c.address || '').match(/, ([A-Z]{2}) \d{5}/)?.[1] || null,
      church_denom: c.denomination_family,
      pastor_field: c.pastor,
      candidate_name: candidate,
      normalized: k,
      existing_signatories: c.signatories || {},
      matches: lists.map(l => ({
        key: l.key,
        label: l.label,
        direction: l.direction,
        signer_state: l.signer.state || l.signer.presbytery || null,
        signer_church: l.signer.church || l.signer.affiliation || null,
      })),
    });
  }
}

// Filter to "new" matches — at least one matched list_key has empty existing signatories.
const newMatches = matches.filter(m => {
  for (const ml of m.matches) {
    if ((m.existing_signatories[ml.key] || []).length === 0) return true;
  }
  return false;
});

const summary = { green_only: 0, red_only: 0, mixed: 0 };
for (const m of newMatches) {
  const dirs = new Set(m.matches.map(x => x.direction));
  if (dirs.has('red') && dirs.has('green')) summary.mixed++;
  else if (dirs.has('red')) summary.red_only++;
  else if (dirs.has('green')) summary.green_only++;
}

console.error(`\nScanned ${churches.churches.length} churches; found ${matches.length} potential matches; ${newMatches.length} are new.`);
console.error(`Direction breakdown: ${JSON.stringify(summary)}`);

fs.writeFileSync(OUTPUT_PATH, JSON.stringify({
  scanned: churches.churches.length,
  total_matches: matches.length,
  new_matches: newMatches.length,
  summary,
  matches: newMatches,
}, null, 2));

console.log(`Wrote ${OUTPUT_PATH} with ${newMatches.length} candidate matches.`);
console.log(`Next: review the red_only and mixed entries (state-corroborated reds become drift downgrades), then run apply-signatures.js`);
