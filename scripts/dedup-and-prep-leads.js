#!/usr/bin/env node
// Phase 6 — Re-dedup research leads against current churches.json
//
// Reads a leads JSON array and a current churches.json snapshot.
// For each lead, attempts to match against existing MOOP records via:
//   1) website-domain (canonical match)
//   2) name+state (with denom-family guard from Phase 5)
//   3) phone (if available)
//   4) full-address sub-string (e.g. street + city)
//
// If matched → emit to --matched-out (so we can tag, not add).
// If unmatched → emit to --safe-to-add (for live-fetch agent enrichment).
// Records missing minimum data (no website OR no city) → emit to --skip-out.
//
// Usage:
//   node scripts/dedup-and-prep-leads.js \
//     --input docs/data/research-leads/phase2-network-leads.json \
//     --network acts29 \
//     --safe-out /tmp/leads-acts29-safe.json \
//     --matched-out /tmp/leads-acts29-already-in-moop.json \
//     --skip-out /tmp/leads-acts29-skip.json \
//     [--limit 100]

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

const args = process.argv.slice(2);
let inputPath = null, network = null, safeOut = null, matchedOut = null, skipOut = null, limit = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input') inputPath = args[++i];
  else if (args[i] === '--network') network = args[++i];
  else if (args[i] === '--safe-out') safeOut = args[++i];
  else if (args[i] === '--matched-out') matchedOut = args[++i];
  else if (args[i] === '--skip-out') skipOut = args[++i];
  else if (args[i] === '--limit') limit = parseInt(args[++i]);
}
if (!inputPath || !safeOut) {
  console.error('Usage: node scripts/dedup-and-prep-leads.js --input <path> [--network <slug>] --safe-out <path> [--matched-out <path>] [--skip-out <path>] [--limit N]');
  process.exit(1);
}

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
    .replace(/\b(church|baptist|reformed|the|of|a|presbyterian|community|fellowship|bible)\b/g, '')
    .replace(/\s+/g, ' ').trim();
}
function normalizeCity(s) {
  return String(s || '').toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
}
function normalizePhone(p) {
  return String(p || '').replace(/\D/g, '').replace(/^1/, '').slice(-10);
}

const INCOMPATIBLE_DENOM_PATTERN = /(?:pentecostal|charismatic|word of faith|^church of god$|church of god \(|^cog$|assemblies of god|catholic|^orthodox$|eastern orthodox|mormon|^lds$|latter.day saints|jehov|seventh.day adventist|^sda$|^unity$|unitarian|universalist|new thought|metaphysical|church of christ.scientist|christian science)/i;
function isDenomCompatible(existingChurch) {
  const d = String(existingChurch.denomination || '');
  return !INCOMPATIBLE_DENOM_PATTERN.test(d);
}

function buildIndexes(d) {
  const byDomain = new Map();
  const byNameState = new Map();
  const byNameCityState = new Map();
  const byPhone = new Map();
  for (const c of d.churches) {
    if (!c || typeof c !== 'object' || !c.id) continue;
    const dom = normalizeDomain(c.website);
    if (dom) {
      if (!byDomain.has(dom)) byDomain.set(dom, []);
      byDomain.get(dom).push(c);
    }
    const stateMatch = String(c.address || '').match(/,\s*([A-Z]{2})\b/);
    const stateCode = stateMatch ? stateMatch[1] : null;
    const cityMatch = String(c.address || '').match(/^([^,]+),\s*[A-Z]{2}\b/) || String(c.address || '').match(/^([^,]+),/);
    const city = cityMatch ? normalizeCity(cityMatch[1].replace(/^\d+\s+/, '').replace(/.*\b(in|on|at)\s+/i, '')) : '';
    const nameKey = normalizeName(c.name);
    if (nameKey && stateCode) {
      const k1 = `${nameKey}|${stateCode}`;
      if (!byNameState.has(k1)) byNameState.set(k1, []);
      byNameState.get(k1).push(c);
      if (city) {
        const k2 = `${nameKey}|${city}|${stateCode}`;
        if (!byNameCityState.has(k2)) byNameCityState.set(k2, []);
        byNameCityState.get(k2).push(c);
      }
    }
    // Phone match (if we have it)
    const ph = normalizePhone(c.phone);
    if (ph && ph.length === 10) {
      if (!byPhone.has(ph)) byPhone.set(ph, []);
      byPhone.get(ph).push(c);
    }
  }
  return { byDomain, byNameState, byNameCityState, byPhone };
}

function findExistingMatch(lead, ix) {
  // 1. Website domain (strongest)
  const dom = normalizeDomain(lead.website);
  if (dom && ix.byDomain.has(dom)) {
    return { match: ix.byDomain.get(dom)[0], matched_by: 'website-domain', confidence: 'high' };
  }
  // 2. Phone (strong but rarely present)
  const ph = normalizePhone(lead.phone);
  if (ph && ph.length === 10 && ix.byPhone.has(ph)) {
    return { match: ix.byPhone.get(ph)[0], matched_by: 'phone', confidence: 'high' };
  }
  // 3. Name+city+state (precise)
  if (lead.name && lead.state && lead.city) {
    const k = `${normalizeName(lead.name)}|${normalizeCity(lead.city)}|${lead.state}`;
    if (ix.byNameCityState.has(k)) {
      const cands = ix.byNameCityState.get(k).filter(isDenomCompatible);
      if (cands.length === 1) return { match: cands[0], matched_by: 'name+city+state', confidence: 'high' };
      if (cands.length > 1) return { match: cands[0], matched_by: 'name+city+state-ambiguous', confidence: 'medium' };
    }
  }
  // 4. Name+state (fuzzy, denom-guarded; only if uniquely-resolvable)
  if (lead.name && lead.state) {
    const k = `${normalizeName(lead.name)}|${lead.state}`;
    if (ix.byNameState.has(k)) {
      const cands = ix.byNameState.get(k).filter(isDenomCompatible);
      if (cands.length === 1) return { match: cands[0], matched_by: 'name+state', confidence: 'medium' };
    }
  }
  return null;
}

function main() {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  let leads = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

  // Network filter — both Phase 2 (source_network) and Phase 3 (conference) leads are in scope
  if (network) {
    leads = leads.filter(l => l.source_network === network);
  }
  if (limit) leads = leads.slice(0, limit);

  console.log(`Input: ${inputPath}`);
  if (network) console.log(`Network filter: ${network}`);
  console.log(`Leads to check: ${leads.length}`);

  const ix = buildIndexes(d);

  const safeToAdd = [];
  const matched = [];
  const skipped = [];

  for (const lead of leads) {
    // Minimum data check
    if (!lead.name || (!lead.state && !lead.country)) {
      skipped.push({ ...lead, skip_reason: 'missing_name_or_state_country' });
      continue;
    }
    if (!lead.website) {
      skipped.push({ ...lead, skip_reason: 'no_website' });
      continue;
    }
    if (!lead.city) {
      skipped.push({ ...lead, skip_reason: 'no_city' });
      continue;
    }

    const m = findExistingMatch(lead, ix);
    if (m) {
      matched.push({ ...lead, moop_match: { id: m.match.id, name: m.match.name, matched_by: m.matched_by, confidence: m.confidence } });
    } else {
      safeToAdd.push(lead);
    }
  }

  fs.writeFileSync(safeOut, JSON.stringify(safeToAdd, null, 2) + '\n');
  if (matchedOut) fs.writeFileSync(matchedOut, JSON.stringify(matched, null, 2) + '\n');
  if (skipOut) fs.writeFileSync(skipOut, JSON.stringify(skipped, null, 2) + '\n');

  console.log(`\nResults:`);
  console.log(`  Safe to add (no existing match):    ${safeToAdd.length}  → ${safeOut}`);
  console.log(`  Already in MOOP (matched):           ${matched.length}${matchedOut ? `  → ${matchedOut}` : ''}`);
  console.log(`  Skipped (insufficient data):         ${skipped.length}${skipOut ? `  → ${skipOut}` : ''}`);
}

if (require.main === module) main();
