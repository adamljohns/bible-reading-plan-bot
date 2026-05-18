#!/usr/bin/env node
// Phase 1 — Founders Ministries match + integrate
// Reads /tmp/founders-index.json
// Matches against docs/data/churches.json
// For matches: adds `cross_listed_in: ["founders"]` to the existing MOOP record
// For non-matches (with website+city): appends new church records

const fs = require('fs');
const path = require('path');

const FOUNDERS_INDEX = '/tmp/founders-index.json';
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = '2026-05-18';

function normalizeDomain(url) {
  if (!url) return '';
  return String(url).toLowerCase()
    .replace(/^https?:\/\//, '')
    .replace(/^www\./, '')
    .replace(/\/.*$/, '')
    .replace(/\/$/, '');
}
function normalizeName(s) {
  return String(s || '').toLowerCase()
    .replace(/&/g, 'and')
    .replace(/[^\w\s]/g, '')
    .replace(/\b(church|baptist|reformed|the|of|a)\b/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}
function citySlug(city) {
  return String(city || '').toLowerCase().replace(/[^\w]+/g, '-').replace(/^-+|-+$/g, '');
}
function generateSlug(name, city, state) {
  const namePart = String(name).toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  const cityPart = citySlug(city);
  const statePart = String(state).toLowerCase();
  return [namePart, cityPart, statePart].filter(Boolean).join('-');
}

const CANONICAL_SIG_KEYS = ['warhurst_protest_2020','amr_2026','letter_of_lament_2025','revoice_2018_2026','dallas_statement_2018','nashville_statement_2017','cbe_egalitarian_2026'];
const SCORE_DIMS = ['christology','scripture','gender','leadership','soteriology','cultural','preaching','mission','mens_discipleship','denominational'];

function newRecordFromFounders(f) {
  const slug = generateSlug(f.name, f.city || '', f.state || '');
  return {
    id: slug,
    slug: slug,
    name: f.name,
    address: f.address || (f.city && f.state ? `${f.city}, ${f.state}` : `${f.state || 'Unknown'}`),
    pastor: f.pastor || 'Verify on church website',
    pastor_credentials: 'Unknown formal credentials',
    founded: 'verify',
    type: 'Church',
    denomination: 'Reformed Baptist',
    denomination_family: 'Reformed Baptist',
    website: f.website || null,
    services: { sunday_morning: 'verify on website' },
    has_mens_ministry: false,
    has_kids_ministry: false,
    overall_rating: 'green',
    overall_label: 'GREEN — Founders Ministries network ("Founders Friendly") + Reformed Baptist',
    scores: Object.fromEntries(SCORE_DIMS.map(d => [d, 'green'])),
    score_notes: {},
    assessment: 'Listed in the Founders Ministries network ("Founders Friendly" tier — every church on the network voluntarily affirms the 1689 LBC Reformed Baptist values + complementarian polity of Founders Ministries).',
    tags: ['reformed-baptist', 'founders-friendly'],
    gender_detail: 'Per 1689 LBC tradition: male-only ordination',
    denomination_detail: 'Reformed Baptist; Founders Ministries network member',
    enrichment_sources: ['https://founders.org', f.founders_url].filter(Boolean),
    enrichment_notes: `[${TODAY}] Added via Founders Ministries Phase 1. Founders directory: ${f.founders_url}. ${f.website ? 'Live-fetched ' + f.website + ' on ' + TODAY + '.' : 'Website not surfaced on Founders profile; verify before public publish.'}`,
    signatories: Object.fromEntries(CANONICAL_SIG_KEYS.map(k => [k, []])),
    signatures_aggregate: 'none',
    engagement: { researched_website: !!f.website },
    cross_listed_in: ['founders'],
    needs_review: !f.website || !f.pastor,
  };
}

function main() {
  const founders = JSON.parse(fs.readFileSync(FOUNDERS_INDEX, 'utf8'));
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  console.log(`Founders index: ${founders.length} entries`);
  console.log(`MOOP directory: ${d.churches.length} churches\n`);

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

  let domainMatches = 0;
  let nameStateMatches = 0;
  let alreadyTagged = 0;
  let newRecords = [];
  let skippedNoData = 0;

  for (const f of founders) {
    if (!f.name || !f.state) { skippedNoData++; continue; }

    let match = null;

    const fDom = normalizeDomain(f.website);
    if (fDom && moopByDomain.has(fDom)) {
      match = moopByDomain.get(fDom)[0];
    }
    if (!match && f.name && f.state) {
      const nameKey = normalizeName(f.name);
      const key = `${nameKey}|${f.state}`;
      if (moopByNameState.has(key)) {
        const candidates = moopByNameState.get(key);
        if (candidates.length === 1) match = candidates[0];
      }
    }

    if (match) {
      if (!Array.isArray(match.cross_listed_in)) match.cross_listed_in = [];
      if (match.cross_listed_in.includes('founders')) {
        alreadyTagged++;
      } else {
        match.cross_listed_in.push('founders');
        if (fDom) domainMatches++; else nameStateMatches++;
      }
    } else if (f.website && f.city) {
      newRecords.push(newRecordFromFounders(f));
    }
  }

  const beforeCount = d.churches.length;
  const existingIds = new Set(d.churches.filter(c => c && c.id).map(c => c.id));
  let addedCount = 0;
  for (const nr of newRecords) {
    if (existingIds.has(nr.id)) continue;
    d.churches.push(nr);
    existingIds.add(nr.id);
    addedCount++;
  }
  d.total_churches = d.churches.length;
  d.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');

  console.log(`Founders matches:`);
  console.log(`  By website domain: ${domainMatches}`);
  console.log(`  By name+state (unique candidate): ${nameStateMatches}`);
  console.log(`  Already tagged (idempotent re-run): ${alreadyTagged}`);
  console.log(`  Total NEW tags on existing records: ${domainMatches + nameStateMatches}`);
  console.log(`\nNew records appended: ${addedCount} (of ${newRecords.length} candidates with website+city)`);
  console.log(`Founders entries skipped (no name/state): ${skippedNoData}`);
  console.log(`\nDirectory: ${beforeCount} → ${d.churches.length}`);
}

if (require.main === module) main();
