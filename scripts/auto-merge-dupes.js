#!/usr/bin/env node
// Phase 5b — Bulk auto-merge of dupe groups identified in
// /tmp/phase5-real-dupes.json. Each group represents records that share
// the same key (typically name @ address) and are therefore the same
// church recorded under multiple slug variants.
//
// Survivor selection: per group, pick the record with the most populated
// schema fields. Ties broken by: longer enrichment_notes wins (more
// curation history), then better rating (green > yellow > red > unrated).
//
// Field-merge policy: for each non-survivor source, fields where survivor
// has nothing or has a placeholder get filled from source. Array fields
// (cross_listed_in, notable_attendees, tags, enrichment_sources) get
// union'd. Object field signatories: per-ledger array union. Pastor field
// gets the LONGER of the two if both are real (richer description wins);
// placeholder pastor never overrides a real one.
//
// Usage:
//   node scripts/auto-merge-dupes.js [--dry-run]

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DUPES = '/tmp/phase5-real-dupes.json';
const TODAY = new Date().toISOString().slice(0, 10);
const DRY_RUN = process.argv.includes('--dry-run');

const PLACEHOLDER_RE = /^(verify|unknown|various|tba|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church)/i;

function isPlaceholderPastor(p) {
  if (!p || typeof p !== 'string') return true;
  const t = p.trim();
  if (t.length < 5) return true;
  if (PLACEHOLDER_RE.test(t)) return true;
  return false;
}

function fieldScore(c) {
  // Score record by # of meaningfully populated fields.
  let score = 0;
  if (c.name && c.name.length > 4) score++;
  if (c.address && c.address.length > 10) score += 2;
  if (c.website && /^https?:/i.test(c.website)) score++;
  if (c.facebook) score++;
  if (c.instagram) score++;
  if (c.youtube) score++;
  if (c.twitter) score++;
  if (c.pastor && !isPlaceholderPastor(c.pastor)) score += 3;
  if (c.denomination && c.denomination.length > 4) score++;
  if (c.denomination_family) score++;
  if (c.overall_rating && c.overall_rating !== 'unrated') score++;
  if (Array.isArray(c.signatories) || (c.signatories && Object.values(c.signatories).some(v => Array.isArray(v) && v.length))) score += 2;
  if (Array.isArray(c.cross_listed_in) && c.cross_listed_in.length) score++;
  if (Array.isArray(c.notable_attendees) && c.notable_attendees.length) score += 2;
  if (Array.isArray(c.tags) && c.tags.length) score++;
  if (Array.isArray(c.enrichment_sources) && c.enrichment_sources.length) score++;
  if (c.enrichment_notes) score += Math.min(3, Math.floor(c.enrichment_notes.length / 200));
  return score;
}

const RATING_ORDER = { green: 0, yellow: 1, red: 2, black: 3, dead: 4, unrated: 5 };

function pickSurvivor(records) {
  records.sort((a, b) => {
    const sa = fieldScore(a);
    const sb = fieldScore(b);
    if (sa !== sb) return sb - sa;
    const ra = RATING_ORDER[a.overall_rating] ?? 99;
    const rb = RATING_ORDER[b.overall_rating] ?? 99;
    if (ra !== rb) return ra - rb;
    return (a.id || '').length - (b.id || '').length;  // shorter slug = cleaner
  });
  return records[0];
}

function mergeArr(target, source) {
  if (!Array.isArray(target)) target = [];
  if (!Array.isArray(source)) return target;
  for (const item of source) {
    if (item == null) continue;
    if (typeof item === 'string') {
      if (!target.includes(item)) target.push(item);
    } else if (typeof item === 'object' && item.name) {
      const name = String(item.name).toLowerCase().trim();
      if (!target.some(t => String(t.name || '').toLowerCase().trim() === name)) {
        target.push(item);
      }
    } else {
      const key = JSON.stringify(item);
      if (!target.some(t => JSON.stringify(t) === key)) target.push(item);
    }
  }
  return target;
}

function mergeSignatories(target, source) {
  if (typeof target !== 'object' || target == null) target = {};
  if (typeof source !== 'object' || source == null) return target;
  for (const k of Object.keys(source)) {
    if (Array.isArray(source[k])) {
      target[k] = mergeArr(target[k] || [], source[k]);
    }
  }
  return target;
}

function mergeRecord(survivor, source) {
  // Pastor: prefer longer non-placeholder
  if (isPlaceholderPastor(survivor.pastor) && !isPlaceholderPastor(source.pastor)) {
    survivor.pastor = source.pastor;
  } else if (!isPlaceholderPastor(survivor.pastor) && !isPlaceholderPastor(source.pastor)) {
    // Both real — pick longer (more informative)
    if (String(source.pastor).length > String(survivor.pastor).length + 10) {
      survivor.pastor = source.pastor;
    }
  }
  // Fill empty fields from source
  const SIMPLE_FIELDS = ['name', 'address', 'website', 'facebook', 'instagram', 'youtube', 'twitter', 'denomination', 'denomination_family', 'denom_family', 'phone', 'email', 'services', 'pastor_facebook', 'pastor_twitter', 'pastor_instagram', 'pastor_linkedin', 'pastor_youtube'];
  for (const f of SIMPLE_FIELDS) {
    if ((survivor[f] == null || survivor[f] === '' || survivor[f] === 'undefined') && source[f]) {
      survivor[f] = source[f];
    }
  }
  // Better rating wins
  const sr = RATING_ORDER[survivor.overall_rating] ?? 99;
  const ssr = RATING_ORDER[source.overall_rating] ?? 99;
  if (ssr < sr) {
    survivor.overall_rating = source.overall_rating;
    if (source.overall_label) survivor.overall_label = source.overall_label;
  }
  // Arrays: union
  survivor.cross_listed_in   = mergeArr(survivor.cross_listed_in,   source.cross_listed_in);
  survivor.notable_attendees = mergeArr(survivor.notable_attendees, source.notable_attendees);
  survivor.tags              = mergeArr(survivor.tags,              source.tags);
  survivor.enrichment_sources= mergeArr(survivor.enrichment_sources,source.enrichment_sources);
  // Signatories: deep union
  if (source.signatories) {
    survivor.signatories = mergeSignatories(survivor.signatories || {}, source.signatories);
    // Recompute aggregate
    const dirs = new Set();
    const ledgerDir = { warhurst_protest_2020:'red', amr_2026:'red', letter_of_lament_2025:'red', revoice_2018_2026:'red', cbe_egalitarian_2026:'red', dallas_statement_2018:'green', nashville_statement_2017:'green' };
    for (const [k, v] of Object.entries(survivor.signatories || {})) {
      if (Array.isArray(v) && v.length) dirs.add(ledgerDir[k] || 'none');
    }
    let agg = 'none';
    if (dirs.has('green') && dirs.has('red')) agg = 'mixed';
    else if (dirs.has('green')) agg = 'green';
    else if (dirs.has('red')) agg = 'red';
    survivor.signatures_aggregate = agg;
  }
  // Needs_review: if either says needs review, survivor needs review
  if (source.needs_review) survivor.needs_review = true;
  return survivor;
}

const dupes = JSON.parse(fs.readFileSync(DUPES, 'utf8'));
const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const byId = new Map();
for (const c of d.churches) if (c && c.id) byId.set(c.id, c);

let groupsMerged = 0, recordsDeleted = 0, groupsSkipped = 0;
const deletionIds = new Set();
const log = [];

for (const g of dupes) {
  const records = g.ids.map(id => byId.get(id)).filter(r => r);
  if (records.length < 2) { groupsSkipped++; continue; }

  const survivor = pickSurvivor([...records]);
  const sources = records.filter(r => r.id !== survivor.id);
  for (const src of sources) {
    mergeRecord(survivor, src);
    deletionIds.add(src.id);
  }
  // Add merge note
  const noteAppend = `[${TODAY}] Phase 5b auto-merge: absorbed ${sources.length} dupe record${sources.length === 1 ? '' : 's'} (${sources.map(s => s.id).join(', ')}). Group key: "${g.key}".`;
  survivor.enrichment_notes = survivor.enrichment_notes ? survivor.enrichment_notes + '\n' + noteAppend : noteAppend;

  groupsMerged++;
  recordsDeleted += sources.length;
  log.push({ survivor: survivor.id, absorbed: sources.map(s => s.id), name: survivor.name });
}

// Delete absorbed records
const beforeCount = d.churches.length;
d.churches = d.churches.filter(c => !(c && c.id && deletionIds.has(c.id)));
const afterCount = d.churches.length;
d.total_churches = afterCount;
d.directory_updated = TODAY;

if (!DRY_RUN) {
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
}

console.log(`Phase 5b Auto-Merge Results${DRY_RUN ? ' (DRY RUN)' : ''}:`);
console.log(`  Dupe groups in input:   ${dupes.length}`);
console.log(`  Groups merged:          ${groupsMerged}`);
console.log(`  Groups skipped (missing records): ${groupsSkipped}`);
console.log(`  Source records deleted: ${recordsDeleted}`);
console.log(`  Directory size:         ${beforeCount} -> ${afterCount}`);

console.log('\nFirst 15 merges:');
for (const item of log.slice(0, 15)) {
  console.log(`  ${item.survivor.padEnd(48)} <- ${item.absorbed.join(', ')}`);
  console.log(`     [${item.name}]`);
}
