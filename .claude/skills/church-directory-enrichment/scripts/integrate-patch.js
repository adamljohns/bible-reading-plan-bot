#!/usr/bin/env node
// Integrate a {"new_churches":[...]} patch into churches.json with default-fills.
//
// Usage:
//   node .claude/skills/church-directory-enrichment/scripts/integrate-patch.js /tmp/patch-foo.json
//
// Behavior:
// - Locates docs/data/churches.json relative to this script (no hardcoded user path).
// - Skips ID collisions (logs them).
// - Fills schema defaults: slug=id, engagement (researched_website=true), signatories
//   (7-key shape), signatures_aggregate=none, region (parsed from address state),
//   url_research_status.
// - Strips empty social placeholders ("" -> deleted).
// - Auto-downgrades to YELLOW with pulpit-vacant + needs-rating-review tags if
//   pastor matches /^vacant/i.
// - Honors records flagged with `_dedup_skip: true` (no-op, just logs).
// - Bumps total_churches and directory_updated.
// - Writes back with 2-space indent + trailing newline (preserves repo convention).
//
// Accepts both shapes:
//   { "new_churches": [...] }
//   [...]              (top-level array of church objects)

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const REPO_ROOT = path.resolve(SCRIPT_DIR, '..', '..', '..', '..');
const DATA_PATH = path.join(REPO_ROOT, 'docs', 'data', 'churches.json');

const patchArg = process.argv[2];
if (!patchArg) {
  console.error('Usage: integrate-patch.js <patch-path>');
  process.exit(2);
}
if (!fs.existsSync(patchArg)) {
  console.error(`Patch not found: ${patchArg}`);
  process.exit(2);
}
if (!fs.existsSync(DATA_PATH)) {
  console.error(`Data file not found: ${DATA_PATH}`);
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
const patch = JSON.parse(fs.readFileSync(patchArg, 'utf8'));

const baseEng = {
  visited_facility: false,
  attended_services: false,
  viewed_online_services: false,
  researched_website: true,
  know_members_personally: false,
  interacted_with_leadership: false,
  attended_personally: false,
};

const baseSig = {
  warhurst_protest_2020: [],
  amr_2026: [],
  letter_of_lament_2025: [],
  revoice_2018_2026: [],
  cbe_egalitarian_2026: [],
  dallas_statement_2018: [],
  nashville_statement_2017: [],
};

const SOCIAL_KEYS = [
  'facebook', 'youtube', 'instagram', 'twitter', 'vimeo',
  'pastor_facebook', 'pastor_twitter', 'pastor_instagram', 'pastor_linkedin',
];

function fill(c) {
  for (const k of SOCIAL_KEYS) {
    if (c[k] === '' || c[k] === null) delete c[k];
  }
  const stateMatch = (c.address || '').match(/, ([A-Z]{2}) \d{5}/);
  const stateCode = stateMatch ? stateMatch[1] : null;
  return {
    ...c,
    slug: c.id,
    engagement: c.engagement || baseEng,
    signatories: c.signatories || baseSig,
    signatures_aggregate: c.signatures_aggregate || 'none',
    region: c.region || (stateCode ? stateCode.toLowerCase() : 'rest_of_us'),
    url_research_status: c.url_research_status || 'verified',
  };
}

const list = Array.isArray(patch) ? patch : (patch.new_churches || []);
if (!Array.isArray(list)) {
  console.error('Patch must be an array or have a top-level "new_churches" array.');
  process.exit(2);
}

const existingIds = new Set(data.churches.map(c => String(c.id)));
let added = 0, skipped = 0, dedupSkip = 0, vacancyDowngrades = 0;

for (const c of list) {
  if (c._dedup_skip === true) {
    dedupSkip++;
    continue;
  }
  if (existingIds.has(String(c.id))) {
    console.error(`SKIP (slug exists): ${c.id}`);
    skipped++;
    continue;
  }
  const filled = fill({ ...c });
  delete filled._dedup_skip;
  if (typeof filled.pastor === 'string' && /^vacant/i.test(filled.pastor)) {
    filled.overall_rating = 'yellow';
    filled.tags = [...(filled.tags || [])];
    if (!filled.tags.includes('needs-rating-review')) filled.tags.push('needs-rating-review');
    if (!filled.tags.includes('pulpit-vacant')) filled.tags.push('pulpit-vacant');
    if (!filled.score_notes) filled.score_notes = {};
    filled.score_notes.leadership =
      `Pulpit currently vacant — verify status before publishing as full GREEN. Auto-downgraded to YELLOW + needs-rating-review on integration. ${filled.score_notes.leadership || ''}`.trim();
    vacancyDowngrades++;
  }
  data.churches.push(filled);
  existingIds.add(String(c.id));
  added++;
  console.log(`ADDED: ${c.id}`);
}

data.total_churches = data.churches.length;
data.directory_updated = new Date().toISOString().slice(0, 10);

fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2) + '\n');

console.log('');
console.log(`Added: ${added}`);
console.log(`Skipped (slug collision): ${skipped}`);
console.log(`Dedup-skip markers (no-op): ${dedupSkip}`);
console.log(`Vacancy auto-downgrades: ${vacancyDowngrades}`);
console.log(`Total: ${data.churches.length}`);
