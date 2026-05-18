#!/usr/bin/env node
// Phase 3 — Conference speakers integrate
//
// Reads /tmp/phase3-speakers-<conference>.json files (an array of speaker objects),
// finds each speaker's home_church in MOOP, and either:
//   - Appends a notable_attendees entry (with dedup against existing entries by name)
//   - Queues the home_church as a research lead
//
// Usage:
//   node scripts/integrate-speakers.js --input /tmp/phase3-speakers-shepherds-conference.json --conference shepherds-conference [--dry-run] [--leads-output <path>]
//   node scripts/integrate-speakers.js --all   # process every /tmp/phase3-speakers-*.json in one go
//
// Input format per entry:
//   { speaker_name, speaker_role, conference, conference_year OR conference_years,
//     home_church_name, home_church_city, home_church_state, home_church_website,
//     verification_source, notes }
//
// Output:
//   - Updated docs/data/churches.json (notable_attendees on matched records)
//   - JSON array at --leads-output path with unmatched home churches

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);
const LEADS_DIR = path.join(__dirname, '..', 'docs', 'data', 'research-leads');

// -------------------------------------------------------------------
const args = process.argv.slice(2);
let inputs = [], conference = null, dryRun = false, leadsOutput = null, processAll = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input') inputs.push(args[++i]);
  else if (args[i] === '--conference') conference = args[++i];
  else if (args[i] === '--dry-run') dryRun = true;
  else if (args[i] === '--leads-output') leadsOutput = args[++i];
  else if (args[i] === '--all') processAll = true;
}

if (processAll) {
  const tmpFiles = fs.readdirSync('/tmp').filter(f => /^phase3-speakers-.+\.json$/.test(f));
  inputs = tmpFiles.map(f => path.join('/tmp', f));
  if (!leadsOutput) leadsOutput = path.join(LEADS_DIR, 'phase3-speaker-home-churches.json');
}

if (!inputs.length) {
  console.error('Usage: node scripts/integrate-speakers.js [--all] | [--input <path> --conference <slug>] [--dry-run] [--leads-output <path>]');
  process.exit(1);
}

// -------------------------------------------------------------------
function normalizeDomain(url) {
  if (!url) return '';
  return String(url).toLowerCase()
    .replace(/^https?:\/\//, '').replace(/^www\./, '')
    .replace(/\/.*$/, '').replace(/\/$/, '');
}
function normalizeName(s) {
  return String(s || '').toLowerCase()
    .replace(/&/g, 'and')
    .replace(/[^\w\s]/g, '')
    .replace(/\b(church|baptist|reformed|the|of|a|presbyterian|community|fellowship|bible|grace)\b/g, '')
    .replace(/\s+/g, ' ').trim();
}
function normalizePerson(n) {
  return String(n || '').toLowerCase()
    .replace(/^(dr|rev|pastor|pr|fr|mr|mrs|ms)\.?\s+/i, '')
    .replace(/\s+(jr|sr|ii|iii|iv)\.?$/i, '')
    .replace(/[^\w\s]/g, '')
    .replace(/\s+/g, ' ').trim();
}

function conferenceLabel(slug) {
  const map = {
    '250th-anniversary': "250th Anniversary (National Mall, May 2026)",
    'g3-conference': "G3 Conference",
    't4g': "Together for the Gospel (T4G)",
    'tgc-national': "TGC National Conference",
    'sing-conference': "Sing! Conference (Getty Music)",
    'cross-conference': "Cross Conference",
    'shepherds-conference': "Shepherds' Conference",
    'cbmw-national': "CBMW National Conference",
  };
  return map[slug] || slug;
}

function fmtConferenceMention(entry) {
  const label = conferenceLabel(entry.conference);
  const years = entry.conference_years ? (Array.isArray(entry.conference_years) ? entry.conference_years.join(', ') : entry.conference_years) : entry.conference_year;
  return years ? `${label} ${years}` : label;
}

// -------------------------------------------------------------------
function buildMoopIndexes(d) {
  const moopByDomain = new Map();
  const moopByNameState = new Map();
  for (const c of d.churches) {
    if (!c || !c.id) continue;
    const dom = normalizeDomain(c.website);
    if (dom) {
      if (!moopByDomain.has(dom)) moopByDomain.set(dom, []);
      moopByDomain.get(dom).push(c);
    }
    const stateMatch = String(c.address || '').match(/,\s*([A-Z]{2})\b/);
    const stateCode = stateMatch ? stateMatch[1] : null;
    const nameKey = normalizeName(c.name);
    if (nameKey && stateCode) {
      const key = `${nameKey}|${stateCode}`;
      if (!moopByNameState.has(key)) moopByNameState.set(key, []);
      moopByNameState.get(key).push(c);
    }
  }
  return { moopByDomain, moopByNameState };
}

function findMatch(entry, indexes) {
  const dom = normalizeDomain(entry.home_church_website);
  if (dom && indexes.moopByDomain.has(dom)) {
    return { match: indexes.moopByDomain.get(dom)[0], matched_by: 'website-domain' };
  }
  if (entry.home_church_name && entry.home_church_state) {
    const key = `${normalizeName(entry.home_church_name)}|${entry.home_church_state}`;
    if (indexes.moopByNameState.has(key)) {
      const cands = indexes.moopByNameState.get(key);
      if (cands.length === 1) return { match: cands[0], matched_by: 'name+state' };
    }
  }
  return { match: null, matched_by: null };
}

function buildNotableAttendeesEntry(entry) {
  const confMention = fmtConferenceMention(entry);
  const titleParts = [];
  if (entry.speaker_role) titleParts.push(entry.speaker_role);
  titleParts.push(`Conference speaker at ${confMention}`);
  if (entry.notes) titleParts.push(entry.notes.replace(/\.$/, ''));
  return {
    name: entry.speaker_name,
    title: titleParts.join('; '),
    branch: 'religious',
    level: 'national',
    association: 'current_pastor',
    period: `Speaker at ${confMention}`,
    verified_date: TODAY,
    source_url: entry.verification_source || null,
    source_title: `${conferenceLabel(entry.conference)} speaker bio`,
  };
}

// -------------------------------------------------------------------
function main() {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const indexes = buildMoopIndexes(d);

  const allSpeakers = [];
  for (const p of inputs) {
    if (!fs.existsSync(p)) { console.warn(`(skipping missing input: ${p})`); continue; }
    const arr = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (!Array.isArray(arr)) { console.warn(`(skipping non-array: ${p})`); continue; }
    for (const e of arr) allSpeakers.push(e);
  }

  console.log(`Total speaker entries loaded: ${allSpeakers.length} across ${inputs.length} input file(s)`);
  if (!allSpeakers.length) { console.log('Nothing to integrate.'); return; }

  let matched = 0, unmatched = 0, dedupedAugmented = 0, dedupedSkipped = 0;
  const unmatchedLeads = [];

  for (const entry of allSpeakers) {
    if (!entry.speaker_name) continue;
    if (!entry.home_church_name) {
      unmatched++;
      unmatchedLeads.push({ ...entry, lead_reason: 'no_home_church_name' });
      continue;
    }

    const { match, matched_by } = findMatch(entry, indexes);
    if (!match) {
      unmatched++;
      unmatchedLeads.push({ ...entry, lead_reason: 'home_church_not_in_moop' });
      continue;
    }

    matched++;
    if (!Array.isArray(match.notable_attendees)) match.notable_attendees = [];
    const newEntry = buildNotableAttendeesEntry(entry);
    const existingIdx = match.notable_attendees.findIndex(a =>
      a && a.name && normalizePerson(a.name) === normalizePerson(newEntry.name)
    );
    if (existingIdx >= 0) {
      const existing = match.notable_attendees[existingIdx];
      const confLabel = conferenceLabel(entry.conference);
      if (String(existing.title || '').includes(confLabel)) {
        dedupedSkipped++;
      } else {
        const yearsPart = entry.conference_years ? (Array.isArray(entry.conference_years) ? entry.conference_years.join(', ') : entry.conference_years) : entry.conference_year;
        const mention = yearsPart ? `Conference speaker at ${confLabel} ${yearsPart}` : `Conference speaker at ${confLabel}`;
        existing.title = `${existing.title}; ${mention}`;
        existing.verified_date = TODAY;
        dedupedAugmented++;
      }
    } else {
      match.notable_attendees.push(newEntry);
    }
  }

  // Write leads
  if (leadsOutput && unmatchedLeads.length) {
    fs.writeFileSync(leadsOutput, JSON.stringify(unmatchedLeads, null, 2) + '\n');
    console.log(`Wrote ${unmatchedLeads.length} speaker-home-church leads to ${leadsOutput}`);
  }

  // Write churches
  d.directory_updated = TODAY;
  if (!dryRun) {
    fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
  }

  console.log(`\nResults:`);
  console.log(`  Speakers matched to existing MOOP records: ${matched}`);
  console.log(`    - New notable_attendees entries added:     ${matched - dedupedAugmented - dedupedSkipped}`);
  console.log(`    - Existing entries augmented (conf added): ${dedupedAugmented}`);
  console.log(`    - Already had conf mentioned (skipped):    ${dedupedSkipped}`);
  console.log(`  Speakers UNmatched (home church not in MOOP or missing): ${unmatched}`);
  console.log(`  Directory churches: ${d.churches.length}${dryRun ? '  [DRY RUN — not written]' : ''}`);
}

if (require.main === module) main();
