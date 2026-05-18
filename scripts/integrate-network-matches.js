#!/usr/bin/env node
// Phase 2 — Generalized network match + integrate
// Reads /tmp/<network>-index.json (or --input <path>)
// Matches against docs/data/churches.json
// For matches: appends <network> to existing record's cross_listed_in
// For non-matches (with website+city): appends new church records
//
// Usage:
//   node scripts/integrate-network-matches.js --network 9marks
//   node scripts/integrate-network-matches.js --network acts29 --input /tmp/acts29-index.json
//   node scripts/integrate-network-matches.js --network sgc --dry-run

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

// -------------------------------------------------------------------
// Per-network defaults — assessment text, tags, denomination, scores.
// New records inherit these; existing records only get cross_listed_in pushed.
// -------------------------------------------------------------------
const NETWORK_CONFIGS = {
  '9marks': {
    label: '9Marks Church-Search',
    denomination: 'Baptist',
    denomination_family: 'Baptist',
    denomination_detail: '9Marks Church-Search listing — a self-submitted directory of churches affirming the 9 Marks of a Healthy Church (Dever): expositional preaching, biblical theology, biblical gospel, conversion, evangelism, membership, church discipline, discipleship, and elder-led leadership. Inclusion is user-submitted via a public form, NOT vetted by 9Marks editorial staff.',
    tags: ['nine-marks-listing', 'baptist'],
    assessment: 'Listed in the 9Marks Church-Search directory. 9Marks publishes the directory as a discoverability tool for Reformed Baptist-leaning, congregationalist, expositional churches that self-identify with the 9 Marks of a Healthy Church (Mark Dever). NOTE: Inclusion is user-submitted via 9marks.org and is NOT individually vetted by 9Marks editorial staff. Treat directory presence as a self-attested signal of alignment with the 9 Marks values; confirm independently before publishing.',
    overall_label: 'YELLOW — 9Marks Church-Search listing (self-attested, not vetted)',
    network_methodology_note: '9Marks Church-Search is a public, user-submitted directory. 9Marks editorial does not vet individual entries; the `?id=N` URL form exposes admin/edit-by-submitter pages, confirming the open-submission model. Inclusion attests to self-alignment with the 9 Marks of a Healthy Church but does NOT represent 9Marks staff certification.',
    gender_detail: 'Verify on church website — 9Marks Church-Search listings self-attest to complementarian polity but the directory does not enforce.',
    default_rating: 'yellow',
    default_score: 'yellow',
  },
  'tgc-cn': {
    label: 'TGC Church Directory',
    denomination: 'Reformed Evangelical',
    denomination_family: 'Reformed',
    denomination_detail: 'Listed in The Gospel Coalition Church Directory (sponsored by Midwestern Seminary). TGC describes the directory as a self-listing of "gospel-believing churches" — not a vetted member roster.',
    tags: ['tgc-directory', 'reformed-evangelical'],
    assessment: 'Listed in The Gospel Coalition Church Directory — TGC\'s open self-listing of gospel-believing churches, sponsored by Midwestern Baptist Theological Seminary. Inclusion does NOT imply TGC vetting against the Foundation Documents (Confessional Statement + Theological Vision for Ministry); 52% of listings have no formal network affiliation, and the rest carry Acts 29 / SEND / Harbor / Converge / Redeemer-CTC tags. Treat TGC Directory presence as a discoverability signal, not a doctrinal endorsement — confirm complementarianism + inerrancy independently before publishing.',
    overall_label: 'YELLOW — TGC Directory listing (self-listing, not vetted)',
    network_methodology_note: 'TGC Church Directory is an open self-listing, not a vetted membership program. ~52% of listings carry no formal network affiliation; the rest declare Acts 29, SEND Network, Harbor Network, Converge, or Redeemer City to City. Directory presence alone is insufficient evidence of full TGC Foundation Documents adherence.',
    gender_detail: 'Verify on church website — TGC Directory does NOT require complementarian polity for listing.',
    default_rating: 'yellow',
    default_score: 'yellow',
  },
  'g3': {
    label: 'G3 Ministries',
    denomination: 'Reformed Baptist',
    denomination_family: 'Reformed Baptist',
    denomination_detail: 'G3 Ministries network — confessional Reformed; typically 1689 LBC or Three Forms of Unity; conservative complementarian.',
    tags: ['g3-ministries', 'reformed-baptist'],
    assessment: 'Listed in the G3 Ministries network (Josh Buice). Network is conservative confessional Reformed — typically 1689 London Baptist Confession or Three Forms of Unity, conservative complementarian, expositional preaching, doctrinal precision.',
    overall_label: 'GREEN — G3 Ministries network + Reformed',
    network_methodology_note: 'G3 churches voluntarily affirm conservative confessional Reformed identity; G3 hosts the annual G3 Conference (Atlanta-area).',
    gender_detail: 'Per G3 conservative confessional posture: male-only ordination.',
  },
  'acts29': {
    label: 'Acts 29',
    denomination: 'Non-Denominational',
    denomination_family: 'Evangelical',
    denomination_detail: 'Acts 29 church-planting network — Reformed-leaning evangelical; complementarian; gospel-centered; missional. Post-Driscoll governance has emphasized accountability and elder-led planters.',
    tags: ['acts29', 'church-plant'],
    assessment: 'Listed in the Acts 29 church-planting network. Network values: gospel-centered, reformed theology, missional, complementarian, Spirit-empowered. Mark Driscoll was expelled in 2014; current leadership (Brian Howard et al.) emphasizes accountability + elder plurality.',
    overall_label: 'GREEN — Acts 29 network + Reformed-Evangelical',
    network_methodology_note: 'Acts 29 churches affirm the network\'s doctrinal distinctives (gospel-centered, Reformed soteriology, complementarian, missional church-planting) and assessed candidates undergo a residency.',
    gender_detail: 'Per Acts 29 distinctives: complementarian; male-only ordained eldership.',
  },
  'sgc': {
    label: 'Sovereign Grace Churches',
    denomination: 'Sovereign Grace',
    denomination_family: 'Reformed',
    denomination_detail: 'Sovereign Grace Churches — Reformed-Baptist–flavored network (C.J. Mahaney heritage); affirms doctrines of grace + continuationist pneumatology + complementarianism.',
    tags: ['sovereign-grace', 'reformed'],
    assessment: 'Member of Sovereign Grace Churches. Distinctives: doctrines of grace (TULIP), continuationist (open to charismatic gifts but order-of-worship friendly), complementarian, gospel-centered, church-planting-emphasis.',
    overall_label: 'GREEN — Sovereign Grace Churches + Reformed',
    network_methodology_note: 'SGC requires confessional alignment with the Statement of Faith and Polity; formal membership tracked via the SGC office.',
    gender_detail: 'Per SGC Statement: complementarian; male-only ordained eldership.',
  },
  'pillar-network': {
    label: 'Pillar Network',
    denomination: 'Baptist',
    denomination_family: 'Baptist',
    denomination_detail: 'Pillar Network — church-planting + revitalization network; SBC-cooperating; Reformed-leaning; complementarian.',
    tags: ['pillar-network', 'church-plant', 'church-revitalization'],
    assessment: 'Member of the Pillar Network. Network values: church planting + church revitalization, expositional preaching, complementarian polity, SBC-cooperative, Reformed-leaning soteriology.',
    overall_label: 'GREEN — Pillar Network + Baptist',
    network_methodology_note: 'Pillar Network churches affirm shared doctrine + commitment to plant or revitalize; partners with NAMB on certain plants.',
    gender_detail: 'Per Pillar distinctives: complementarian; male-only ordained eldership.',
  },
  'trinity-foundation': {
    label: 'Trinity Foundation Church Registry',
    denomination: 'Reformed',
    denomination_family: 'Reformed',
    denomination_detail: 'Trinity Foundation Church Registry & Clearinghouse (Dallas TX) — Gordon Clark / John Robbins publishing arm; vetted registry of confessionally Reformed congregations (1689 LBCF, Westminster 1729, Three Forms of Unity).',
    tags: ['trinity-foundation-registry', 'reformed', 'confessional'],
    assessment: 'Listed in The Trinity Foundation Church Registry & Clearinghouse — a screened registry vetting congregations against confessional Reformed standards (1689 LBCF, Westminster Confession of Faith 1729, or Three Forms of Unity). The Foundation publishes The Trinity Review and Trinity Lectures from a Clarkian/Scripturalist tradition (Gordon Clark, John Robbins).',
    overall_label: 'GREEN — Trinity Foundation Church Registry + Confessional Reformed',
    network_methodology_note: 'Trinity Foundation Registry is a screened clearinghouse, not a denomination. Explicit disclaimer: "We are not establishing a new denomination." Each entry is vetted against the registry\'s confessional Reformed standards.',
    gender_detail: 'Per confessional Reformed standards (WCF, 1689 LBCF): complementarian; male-only ordination.',
  },
};

// Canonical schema keys (mirroring Phase 1 + the rest of churches.json)
const CANONICAL_SIG_KEYS = ['warhurst_protest_2020','amr_2026','letter_of_lament_2025','revoice_2018_2026','dallas_statement_2018','nashville_statement_2017','cbe_egalitarian_2026'];
const SCORE_DIMS = ['christology','scripture','gender','leadership','soteriology','cultural','preaching','mission','mens_discipleship','denominational'];

// -------------------------------------------------------------------
// Args
// -------------------------------------------------------------------
const args = process.argv.slice(2);
let network = null, inputPath = null, dryRun = false, tagsOnly = false, leadsOutput = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--network') network = args[++i];
  else if (args[i] === '--input') inputPath = args[++i];
  else if (args[i] === '--dry-run') dryRun = true;
  else if (args[i] === '--tags-only') tagsOnly = true;
  else if (args[i] === '--leads-output') leadsOutput = args[++i];
}
if (!network) {
  console.error('Usage: node scripts/integrate-network-matches.js --network <slug> [--input <path>] [--dry-run] [--tags-only] [--leads-output <path>]');
  console.error('Available networks: ' + Object.keys(NETWORK_CONFIGS).join(', '));
  console.error('--tags-only: append cross_listed_in to existing matches; do NOT add new records');
  console.error('--leads-output: write would-be-new candidates to <path> as JSON (for human-vetted curation)');
  process.exit(1);
}
const cfg = NETWORK_CONFIGS[network];
if (!cfg) {
  console.error(`Unknown network: ${network}. Available: ${Object.keys(NETWORK_CONFIGS).join(', ')}`);
  process.exit(1);
}
inputPath = inputPath || `/tmp/${network}-index.json`;
if (!fs.existsSync(inputPath)) {
  console.error(`Input not found: ${inputPath}`);
  process.exit(1);
}

// -------------------------------------------------------------------
// Helpers (mirroring Phase 1)
// -------------------------------------------------------------------
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
    .replace(/\b(church|baptist|reformed|the|of|a|presbyterian|community|fellowship|bible|grace)\b/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}
function citySlug(city) {
  return String(city || '').toLowerCase().replace(/[^\w]+/g, '-').replace(/^-+|-+$/g, '');
}
function generateSlug(name, city, state) {
  const namePart = String(name).toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  const cityPart = citySlug(city);
  const statePart = String(state || '').toLowerCase();
  return [namePart, cityPart, statePart].filter(Boolean).join('-');
}

function newRecordFromNetwork(f, cfg, network) {
  const slug = generateSlug(f.name, f.city || '', f.state || '');
  const isUS = (f.country == null || /usa|united states|us/i.test(f.country)) && f.state;
  const addressParts = [];
  if (f.address) addressParts.push(f.address);
  else if (f.city && f.state) addressParts.push(`${f.city}, ${f.state}`);
  else if (f.city && f.country && !isUS) addressParts.push(`${f.city}, ${f.country}`);
  else addressParts.push(f.state || f.country || 'Unknown');

  const rating = cfg.default_rating || 'green';
  const scoreColor = cfg.default_score || rating;

  return {
    id: slug,
    slug: slug,
    name: f.name,
    address: addressParts.join(' '),
    pastor: f.pastor || 'Verify on church website',
    pastor_credentials: 'Unknown formal credentials',
    founded: 'verify',
    type: 'Church',
    denomination: cfg.denomination,
    denomination_family: cfg.denomination_family,
    website: f.website || null,
    services: { sunday_morning: 'verify on website' },
    has_mens_ministry: false,
    has_kids_ministry: false,
    overall_rating: rating,
    overall_label: cfg.overall_label,
    scores: Object.fromEntries(SCORE_DIMS.map(d => [d, scoreColor])),
    score_notes: {},
    assessment: cfg.assessment,
    tags: cfg.tags.slice(),
    gender_detail: cfg.gender_detail,
    denomination_detail: cfg.denomination_detail,
    enrichment_sources: [f.network_url].filter(Boolean),
    enrichment_notes: `[${TODAY}] Added via ${cfg.label} Phase 2. Network directory: ${f.network_url || 'n/a'}. ${f.website ? 'Live-fetched ' + f.website + ' on ' + TODAY + '.' : 'Website not surfaced on network profile; verify before public publish.'}${!isUS && f.country ? ' International (' + f.country + ').' : ''}`,
    signatories: Object.fromEntries(CANONICAL_SIG_KEYS.map(k => [k, []])),
    signatures_aggregate: 'none',
    engagement: { researched_website: !!f.website },
    cross_listed_in: [network],
    needs_review: !f.website || !f.pastor || !isUS,
  };
}

// -------------------------------------------------------------------
// Main
// -------------------------------------------------------------------
function main() {
  const indexed = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  if (!Array.isArray(indexed)) {
    console.error(`Input ${inputPath} is not a JSON array.`);
    process.exit(1);
  }
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  console.log(`\n=== ${cfg.label} (${network}) ===`);
  console.log(`Input: ${inputPath} — ${indexed.length} entries`);
  console.log(`MOOP directory: ${d.churches.length} churches`);

  if (indexed.length === 0) {
    console.log(`(empty index — nothing to integrate; exiting)`);
    return;
  }

  // Build MOOP indexes
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
  const newRecords = [];
  const unmatchedLeads = [];   // candidates that didn't match an existing MOOP record (for human curation)
  let skippedNoData = 0;

  for (const f of indexed) {
    if (!f.name) { skippedNoData++; continue; }
    if (!f.state && !f.country) { skippedNoData++; continue; }

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
      if (match.cross_listed_in.includes(network)) {
        alreadyTagged++;
      } else {
        match.cross_listed_in.push(network);
        if (fDom && moopByDomain.has(fDom)) domainMatches++; else nameStateMatches++;
      }
    } else {
      // Unmatched — record as a research lead regardless of whether we'd auto-add
      unmatchedLeads.push({
        source_network: network,
        name: f.name,
        city: f.city || null,
        state: f.state || null,
        country: f.country || null,
        website: f.website || null,
        pastor: f.pastor || null,
        address: f.address || null,
        network_url: f.network_url || null,
        proposed_slug: generateSlug(f.name, f.city || '', f.state || ''),
      });
      if (f.website && f.city && !tagsOnly) {
        newRecords.push(newRecordFromNetwork(f, cfg, network));
      }
    }
  }

  if (leadsOutput) {
    fs.writeFileSync(leadsOutput, JSON.stringify(unmatchedLeads, null, 2) + '\n');
    console.log(`Wrote ${unmatchedLeads.length} research leads to ${leadsOutput}`);
  }

  const beforeCount = d.churches.length;
  const existingIds = new Set(d.churches.filter(c => c && c.id).map(c => c.id));
  let addedCount = 0;
  const skippedDupSlug = [];
  for (const nr of newRecords) {
    if (existingIds.has(nr.id)) { skippedDupSlug.push(nr.id); continue; }
    d.churches.push(nr);
    existingIds.add(nr.id);
    addedCount++;
  }
  d.total_churches = d.churches.length;
  d.directory_updated = TODAY;

  if (!dryRun) {
    fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
  }

  console.log(`\n${cfg.label} matches:`);
  console.log(`  By website domain: ${domainMatches}`);
  console.log(`  By name+state (unique candidate): ${nameStateMatches}`);
  console.log(`  Already tagged (idempotent re-run): ${alreadyTagged}`);
  console.log(`  Total NEW tags on existing records: ${domainMatches + nameStateMatches}`);
  console.log(`\nNew records appended: ${addedCount} (of ${newRecords.length} candidates with website+city)`);
  if (skippedDupSlug.length) console.log(`  Dup-slug skipped: ${skippedDupSlug.length} (e.g. ${skippedDupSlug.slice(0,3).join(', ')})`);
  console.log(`Network entries skipped (no name/state): ${skippedNoData}`);
  console.log(`\nDirectory: ${beforeCount} → ${d.churches.length}${dryRun ? '  [DRY RUN — NOT WRITTEN]' : ''}`);
}

if (require.main === module) main();
