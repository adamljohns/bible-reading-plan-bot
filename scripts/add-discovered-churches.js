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
const { regionOf: vaRegion } = require('./lib/va-regions.js');

const TODAY = new Date().toISOString().slice(0, 10);
const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const files = args.filter(a => a.endsWith('.json'));
if (!files.length) { console.error('give at least one discovered-*.json file'); process.exit(1); }

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);
const existingIds = new Set(d.churches.map(c => String(c.id)));
const normName = s => String(s || '').toLowerCase().replace(/\b(the|a)\b/g, '').replace(/church|chapel|fellowship|ministries|ministry|inc|congregation/g, '').replace(/[^a-z0-9]+/g, '').trim();

// Duplicate detection, generalized 2026-08-16.
//
// This gate used to ask only "is there a same-named church in the FREDERICKSBURG
// region?" — correct while every discovery wave was an FXBG sweep, and silently
// unsafe the moment one is not: a Roanoke or DC discovery could not collide with
// anything, so a genuine duplicate would sail straight in. That is precisely the
// failure Adam called out (2026-08-12: same church, slightly different name).
//
// Now: same state, same normalized name, corroborated by city or ZIP or street.
// Same name in a different VA city (Northside Baptist Charlottesville vs Stafford)
// is still a DIFFERENT church, which was the original rule's real insight.
const ID = require('./lib/church-identity.js');
const existingByName = new Map();
d.churches.forEach(c => {
  const k = String(c.state || '').toUpperCase() + '|' + normName(c.name);
  if (!existingByName.has(k)) existingByName.set(k, []);
  existingByName.get(k).push(c);
});
function existingDup(r) {
  const st = String(r.state || '').toUpperCase();
  const cands = existingByName.get(st + '|' + normName(r.name)) || [];
  const rCity = ID.norm(r.city || ''), rZip = ID.zipOf(r);
  const hit = cands.find(c => {
    if (ID.streetsDiffer(r, c)) return false;              // different building -> different church
    if (rCity && ID.cityOfLoose(c) === rCity) return true;
    if (rZip && ID.zipOf(c) === rZip) return true;
    return ID.streetFull(r) && ID.streetFull(r) === ID.streetFull(c);
  });
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
    address: r.address || `${r.city || ''}, ${state}`.replace(/^, /, ''),
    // A pastor named by the denomination's own roster is verbatim source data,
    // not a guess. Blank otherwise, which drops the record into the local
    // enrichment pool exactly as before.
    pastor: (typeof r.pastor === 'string' && r.pastor.trim()) ? r.pastor.trim() : '',
    founded: '', type: r.denomination || '',
    denomination: r.denomination || 'Unverified',
    denomination_family: famOf(r.denomination),
    website: (typeof r.website === 'string' && /^https?:\/\//i.test(r.website)) ? r.website : '',
    has_mens_ministry: false, has_kids_ministry: false,
    overall_rating: 'yellow',
    overall_label: `YELLOW — Newly added ${TODAY} from ${r.source_label || 'local discovery'} (${r.city || 'region'}, ${state}); existence ${conf}-confidence-verified via ${r.source_label ? 'the denomination\'s own roster' : 'an online listing'}. Doctrine, leadership & complementarian polity NOT yet reviewed — assessment pending.`,
    // VA gets a real sub-region so the church lands on the right regional page
    // instead of the bare state bucket; everything else keeps the state code.
    region: state === 'VA' ? vaRegion({ address: r.address || '', city: r.city || '' }) : state.toLowerCase(),
    state, country: 'United States', country_code: 'US',
    scores: {}, assessment: '',
    enrichment_notes: `[${TODAY}] Added via ${r.source_label || 'local discovery pass'} (${conf} confidence). Existence evidence: ${r.evidence_url || 'n/a'}.${r.pastor ? ` Pastor "${r.pastor}" taken verbatim from that roster entry.` : ' Pastor pending (empty pastor → enters the local enrichment pool).'}${r.phone ? ` Phone on roster: ${r.phone}.` : ''} Doctrine not yet reviewed.`,
    enrichment_sources: r.evidence_url ? [r.evidence_url] : [],
    last_reviewed: TODAY,
    tags: r.source_tag ? [r.source_tag] : ['local-discovery-2026-07'],
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
  // A denominational roster entry satisfies the presence test on its own (Adam,
  // 2026-08-16). SBCV publishes no church websites, so the original gate would
  // have rejected all 663 of its congregations we are missing — yet each arrives
  // with the denomination's own roster URL, a full street address and often a
  // named pastor. That is stronger provenance than a Facebook page, and it is
  // verifiable: the evidence_url can be re-fetched and checked at any time.
  const hasRoster = typeof r.evidence_url === 'string' && /^https?:\/\//i.test(r.evidence_url)
    && typeof r.address === 'string' && /\d/.test(r.address);
  if (!hasSite && !hasSocial && !hasRoster) { skipped.push(`${r.name} — zero web presence (no website, no social, no roster evidence); not added per 2026-07-11 policy`); continue; }
  const dupId = existingDup(r);
  if (dupId) { skipped.push(`${r.name} — already in the directory (${dupId})`); continue; }
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
