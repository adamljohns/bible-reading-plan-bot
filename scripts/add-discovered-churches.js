#!/usr/bin/env node
// Add newly-DISCOVERED churches (from a local-area discovery pass) to churches.json.
// Input: one or more JSON arrays of {name, address, city, state, website,
// denomination, evidence_url, confidence}. Builds canonical records (empty pastor
// so the local grind enriches them; needs_review=true; honest YELLOW label; existence
// verified via evidence_url), dedups against existing + each other, and appends via
// the format-preserving ASCII writer (no 50k-line diff). Report-first; --apply writes.
//
// Usage: node scripts/add-discovered-churches.js file1.json [file2.json …] [--apply]
const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const TODAY = new Date().toISOString().slice(0, 10);
const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const files = args.filter(a => a.endsWith('.json'));
if (!files.length) { console.error('give at least one discovered-*.json file'); process.exit(1); }

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);
const existingIds = new Set(d.churches.map(c => String(c.id)));
const normName = s => String(s || '').toLowerCase().replace(/\b(the|a)\b/g, '').replace(/church|chapel|fellowship|ministries|ministry|inc|congregation/g, '').replace(/[^a-z0-9]+/g, '').trim();
// Region-aware dedup: a discovered church is a duplicate ONLY if an existing church
// with the same normalized name is itself in the Fredericksburg region. Same name in
// another VA city (Northside Baptist Charlottesville vs Stafford) is a DIFFERENT church.
const FXBG_RE = /fredericksburg|spotsylvania|stafford|partlow|falmouth|thornburg|garrisonville|aquia|snell|hartwood|woodford|\b224(0[1-8]|1[2-9])\b|\b225(5[1-6]|34|65)\b/i;
const existingByName = new Map();
d.churches.forEach(c => { const k = normName(c.name); if (!existingByName.has(k)) existingByName.set(k, []); existingByName.get(k).push(c); });
function existingFxbgDup(r) {
  const matches = existingByName.get(normName(r.name)) || [];
  const hit = matches.find(c => FXBG_RE.test(String(c.address || '') + ' ' + String(c.id) + ' ' + String(c.name || '')));
  return hit ? hit.id : null;
}

function famOf(den) {
  const s = String(den || '').toLowerCase();
  const m = [
    [/southern baptist|sbcv|\bsbc\b/, 'Southern Baptist (SBC)'],
    [/independent baptist/, 'Independent Baptist'],
    [/reformed baptist/, 'Reformed Baptist'],
    [/baptist/, 'Baptist'],
    [/\bpca\b|presbyterian church in america/, 'Presbyterian (PCA)'],
    [/presbyterian|pcusa|\bopc\b|\barp\b/, 'Presbyterian'],
    [/anglican|\bacna\b/, 'Anglican (ACNA)'],
    [/episcopal/, 'Episcopal'],
    [/methodist|\bumc\b|\bgmc\b/, 'Methodist'],
    [/lcms|lutheran.*missouri/, 'Lutheran (LCMS)'],
    [/wels/, 'Lutheran (WELS)'],
    [/elca|lutheran/, 'Lutheran'],
    [/efca|evangelical free/, 'EFCA'],
    [/calvary chapel/, 'Calvary Chapel'],
    [/assembl|pentecost|charismatic|foursquare|\bcog\b|church of god/, 'Pentecostal/Charismatic'],
    [/catholic/, 'Catholic'],
    [/orthodox/, 'Orthodox'],
    [/\bame\b|african methodist|ame zion/, 'AME'],
    [/reformed|\bcrc\b|\brca\b/, 'Reformed'],
    [/bible church|\bbible\b/, 'Bible Church'],
    [/non.?denom|nondenom/, 'Non-Denominational'],
    [/evangelical/, 'Evangelical'],
  ];
  for (const [re, fam] of m) if (re.test(s)) return fam;
  return den ? String(den) : 'Non-Denominational';
}

function uniqueSlug(name, city, state) {
  const base = String(name).toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
  let id = base;
  const suf = [String(city || '').toLowerCase().replace(/[^a-z0-9]+/g, '-'), String(state || 'va').toLowerCase()];
  let si = 0;
  while (existingIds.has(id)) { id = (base + '-' + (suf[si] || si)).replace(/-+/g, '-').replace(/-$/, ''); si++; if (si > 4) id = base + '-' + Date.now().toString(36); }
  existingIds.add(id);
  return id;
}

function build(r) {
  const id = uniqueSlug(r.name, r.city, r.state);
  const state = (r.state || 'VA').toUpperCase();
  const conf = (r.confidence || 'medium').toLowerCase();
  return {
    slug: id, id,
    engagement: { visited_facility: false, attended_services: false, viewed_online_services: false, researched_website: !!r.website, know_members_personally: false, interacted_with_leadership: false, attended_personally: false },
    signatories: { warhurst_protest_2020: [], amr_2026: [], letter_of_lament_2025: [], revoice_2018_2026: [], cbe_egalitarian_2026: [], dallas_statement_2018: [], nashville_statement_2017: [] },
    signatures_aggregate: 'none',
    url_research_status: conf === 'high' ? 'verified' : 'unverified',
    name: r.name,
    address: r.address || `${r.city || 'Fredericksburg'}, ${state}`,
    pastor: '',
    founded: '', type: r.denomination || '',
    denomination: r.denomination || 'Unverified',
    denomination_family: famOf(r.denomination),
    website: (typeof r.website === 'string' && /^https?:\/\//i.test(r.website)) ? r.website : '',
    has_mens_ministry: false, has_kids_ministry: false,
    overall_rating: 'yellow',
    overall_label: `YELLOW — Newly added ${TODAY} from Fredericksburg-area discovery (${r.city || 'region'}, ${state}); existence ${conf}-confidence-verified via an online listing. Doctrine, leadership & complementarian polity NOT yet reviewed — assessment pending.`,
    region: state.toLowerCase(), state, country: 'United States', country_code: 'US',
    scores: {}, assessment: '',
    enrichment_notes: `[${TODAY}] Added via Fredericksburg-area local discovery pass (${conf} confidence). Existence evidence: ${r.evidence_url || 'n/a'}. Pastor + doctrine pending (empty pastor → enters the local enrichment pool).`,
    enrichment_sources: r.evidence_url ? [r.evidence_url] : [],
    last_reviewed: TODAY,
    tags: ['local-discovery-2026-07'],
    needs_review: true,
  };
}

const incoming = files.flatMap(f => JSON.parse(fs.readFileSync(f, 'utf8')));
const seen = new Set();
const toAdd = [], skipped = [];
for (const r of incoming) {
  if (!r || !r.name) { skipped.push('(no name)'); continue; }
  // Zero-presence gate (Adam, 2026-07-11): a discovered church must arrive with a
  // verifiable web presence — a real website or at least one social link. With
  // nothing to verify against, nothing about it can ever be enriched or checked,
  // and honest blanks beat unverifiable listings. (Facebook-only is acceptable.)
  const hasSite = typeof r.website === 'string' && /^https?:\/\//i.test(r.website);
  const hasSocial = !!(r.facebook || r.youtube || r.instagram);
  if (!hasSite && !hasSocial) { skipped.push(`${r.name} — zero web presence (no website, no social); not added per 2026-07-11 policy`); continue; }
  const dupId = existingFxbgDup(r);
  if (dupId) { skipped.push(`${r.name} — already in FXBG directory (${dupId})`); continue; }
  const key = normName(r.name) + '|' + String(r.city || '').toLowerCase().replace(/[^a-z]/g, '');
  if (seen.has(key)) { skipped.push(`${r.name} — dup within discovery batch`); continue; }
  seen.add(key);
  toAdd.push(build(r));
}

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — ${incoming.length} discovered, ${toAdd.length} to add, ${skipped.length} skipped\n`);
for (const c of toAdd) console.log(`  + ${c.id}  [${c.denomination_family}]  ${c.website || '(no site)'}`);
if (skipped.length) { console.log('\n  skipped:'); skipped.forEach(s => console.log(`    - ${s}`)); }

if (APPLY && toAdd.length) {
  d.churches.push(...toAdd);
  if ('total_churches' in d) d.total_churches = d.churches.length;
  write(d);
  console.log(`\nAppended ${toAdd.length}. Total churches now ${d.churches.length}.`);
} else if (!APPLY) {
  console.log('\nDry run — re-run with --apply to write.');
}
