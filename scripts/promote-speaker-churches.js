#!/usr/bin/env node
// Phase 6b — Promote unique speaker home-churches from Phase 3 leads.
//
// Reads /tmp/phase3-grouped-churches.json (built via jq from
// docs/data/research-leads/phase3-speaker-home-churches.json grouping
// by home_church_name+state), filters out non-church / non-MOOP-scope
// entries, builds full MOOP records with notable_attendees entries for
// each speaker, and appends to docs/data/churches.json with dedup.

const fs = require('fs');
const path = require('path');

const GROUPED = '/tmp/phase3-grouped-churches.json';
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

const SCORE_DIMS = ['christology','scripture','gender','leadership','soteriology','cultural','preaching','mission','mens_discipleship','denominational'];
const CANONICAL_SIG_KEYS = ['warhurst_protest_2020','amr_2026','letter_of_lament_2025','revoice_2018_2026','dallas_statement_2018','nashville_statement_2017','cbe_egalitarian_2026'];

// Heuristics: skip these patterns (parachurch / academic / non-Protestant)
const SKIP_NAME_PATTERNS = [
  /\(former(ly)?\)/i,
  /\bacademic ministry context\b/i,
  /\bliterary ministry context\b/i,
  /\bapologetics canada\b/i,
  /\barchdiocese\b/i,
  /\bdiocese\b/i,
  /\bsynagogue\b/i,
  /\bdivinity school\b/i,
  /\bseminary\b/i,
  /^the trinity foundation/i,           // already a MOOP cross-ref
  /\bgirton college\b/i,
  /\bministry context\b/i,
  /\bpara.?church\b/i,
];

const US_STATES = new Set(['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']);

function slug(name, city, state) {
  const namePart = String(name).toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  const cityPart = String(city || '').toLowerCase().replace(/[^\w]+/g, '-').replace(/^-+|-+$/g, '');
  const statePart = String(state || '').toLowerCase().replace(/[^\w]+/g, '-').replace(/^-+|-+$/g, '');
  return [namePart, cityPart, statePart].filter(Boolean).join('-');
}

function conferenceLabel(slug) {
  const map = {
    '250th-anniversary': '250th Anniversary Rededicate 250 (National Mall, May 2026)',
    'Rededicate 250': '250th Anniversary Rededicate 250 (National Mall, May 2026)',
    'g3-conference': 'G3 Conference',
    't4g': 'Together for the Gospel (T4G)',
    'tgc-national': 'TGC National Conference',
    'sing-conference': 'Sing! Conference (Getty Music)',
    'cross-conference': 'Cross Conference',
    'shepherds-conference': "Shepherds' Conference",
    'cbmw-national': 'CBMW National Conference',
  };
  return map[slug] || slug;
}

function buildNotableAttendees(group) {
  // For each speaker → conference pair, create one entry
  // Use the original phase3 leads (raw) since group has been aggregated; we'll back-fill the conferences
  const out = [];
  const seen = new Set();
  for (let i = 0; i < group.speakers.length; i++) {
    const name = group.speakers[i];
    const conf = group.conferences[i % group.conferences.length] || group.conferences[0];
    const key = name.toLowerCase().trim();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      name,
      title: `Conference speaker at ${conferenceLabel(conf)}`,
      branch: 'religious',
      level: 'national',
      association: 'current_pastor',
      period: `Speaker at ${conferenceLabel(conf)}`,
      verified_date: TODAY,
      source_url: group.website || null,
      source_title: `${conferenceLabel(conf)} speaker bio`,
    });
  }
  return out;
}

function newSpeakerChurchRecord(group) {
  const id = slug(group.name, group.city, group.state);
  const country = US_STATES.has(group.state) ? 'USA' : (group.state || '');
  const isUS = US_STATES.has(group.state);
  const addr = group.city && group.state
    ? `${group.city}, ${group.state}${!isUS && country !== group.state ? ` (${country})` : ''}`
    : 'verify';
  const speakersStr = group.speakers.join(', ');
  const conferencesStr = group.conferences.map(conferenceLabel).join('; ');

  return {
    id,
    slug: id,
    name: group.name,
    address: addr,
    pastor: 'Verify on church website',
    pastor_credentials: 'Unknown formal credentials',
    founded: 'verify',
    type: 'Church',
    denomination: 'verify',
    denomination_family: 'verify',
    website: group.website,
    services: { sunday_morning: 'verify on website' },
    has_mens_ministry: false,
    has_kids_ministry: false,
    overall_rating: 'yellow',
    overall_label: 'YELLOW — Speaker-home-church surfaced via Phase 3 conference speaker research; verify before publish',
    scores: Object.fromEntries(SCORE_DIMS.map(d => [d, 'yellow'])),
    score_notes: {},
    assessment: `Home church of conference speaker(s): ${speakersStr} (${conferencesStr}). Added via Phase 6b speaker-church promotion ${TODAY}. Conservative-yellow defaults pending individual MOOP verification.`,
    tags: ['speaker-home-church', 'phase3-surfaced'],
    gender_detail: 'Verify on church website',
    denomination_detail: 'Verify on church website',
    enrichment_sources: [group.website].filter(Boolean),
    enrichment_notes: `[${TODAY}] Promoted via Phase 6b (Phase 3 speaker home-church curation). Speaker(s): ${speakersStr}. Conferences: ${conferencesStr}. Live-fetch + 10-dim scoring + signatory check pending.`,
    signatories: Object.fromEntries(CANONICAL_SIG_KEYS.map(k => [k, []])),
    signatures_aggregate: 'none',
    engagement: { researched_website: !!group.website },
    cross_listed_in: [],
    notable_attendees: buildNotableAttendees(group),
    needs_review: true,
  };
}

function main() {
  const groups = JSON.parse(fs.readFileSync(GROUPED, 'utf8'));
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));

  const existingIds = new Set(d.churches.filter(c => c && c.id).map(c => c.id));
  const existingByDomain = new Map();
  for (const c of d.churches) {
    if (!c || !c.id || !c.website) continue;
    const dom = String(c.website).toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '').replace(/\/$/, '');
    if (dom) existingByDomain.set(dom, c);
  }

  let added = 0, skipped = 0;
  const skipReasons = {};

  for (const g of groups) {
    if (!g.name || !g.website) { skipped++; skipReasons['missing_name_or_website'] = (skipReasons['missing_name_or_website']||0)+1; continue; }

    let bad = false;
    for (const pat of SKIP_NAME_PATTERNS) {
      if (pat.test(g.name)) { bad = true; break; }
    }
    if (bad) { skipped++; skipReasons['filtered_pattern'] = (skipReasons['filtered_pattern']||0)+1; continue; }

    // Country gate — require US state or known non-US format we'll process (UK, Canada, etc.)
    const isUS = US_STATES.has(g.state);
    if (!isUS) { skipped++; skipReasons['non_us_state'] = (skipReasons['non_us_state']||0)+1; continue; }

    // Dedup: domain
    const dom = String(g.website).toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '').replace(/\/$/, '');
    if (dom && existingByDomain.has(dom)) {
      // Already in MOOP — should have been caught in pre-dedup. Augment that record's notable_attendees instead.
      const existing = existingByDomain.get(dom);
      const nas = buildNotableAttendees(g);
      if (!Array.isArray(existing.notable_attendees)) existing.notable_attendees = [];
      for (const na of nas) {
        const exists = existing.notable_attendees.find(a => a && a.name && a.name.toLowerCase() === na.name.toLowerCase());
        if (!exists) existing.notable_attendees.push(na);
      }
      skipped++;
      skipReasons['dedup_existing_augmented'] = (skipReasons['dedup_existing_augmented']||0)+1;
      continue;
    }

    const rec = newSpeakerChurchRecord(g);
    if (existingIds.has(rec.id)) { skipped++; skipReasons['dup_slug'] = (skipReasons['dup_slug']||0)+1; continue; }
    d.churches.push(rec);
    existingIds.add(rec.id);
    added++;
  }

  d.total_churches = d.churches.length;
  d.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');

  console.log(`Added: ${added}`);
  console.log(`Skipped: ${skipped}`);
  for (const k of Object.keys(skipReasons)) console.log(`  ${k}: ${skipReasons[k]}`);
  console.log(`Directory: ${d.churches.length}`);
}

if (require.main === module) main();
