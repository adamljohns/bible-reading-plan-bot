#!/usr/bin/env node
// Phase 7 — Pastor-signatory cross-reference pass.
//
// For each church in MOOP, parses the pastor field, normalizes names, and
// cross-references against 7 canonical pastor/leadership ledgers. Matches
// are written to church.signatories[] and an aggregate signal is computed.
//
// Ledgers and their "direction" (green = orthodox marker, red = drift marker):
//   nashville_statement_2017   green  (22,916 signers; needs state corroboration)
//   dallas_statement_2018      green  (13,169 signers; needs state corroboration)
//   warhurst_protest_2020      red    (109 PCA signers)
//   amr_2026                   red    (17 PCA Kellerite-adjacent leaders)
//   letter_of_lament_2025      red    (17 PCA progressive signers)
//   revoice_2018_2026          red    (60 Side B speakers/endorsers)
//   cbe_egalitarian_2026       red    (241 egalitarian network)
//
// Aggregate computation:
//   - Has any green ledger only           → signatures_aggregate='green'
//   - Has any red ledger only             → signatures_aggregate='red'
//   - Has both green and red              → signatures_aggregate='mixed' (warrants human review)
//   - No matches                          → signatures_aggregate='none'
//
// Per the manifest's cross_check_methodology:
//   - Strict first+last match (after stripping honorifics + suffixes)
//   - For Dallas/Nashville: state corroboration required
//   - For Nashville-attributed signers: institution token overlap supplement
//   - All matches dedup by ledger+normalized name
//
// Usage:
//   node scripts/cross-reference-signatories.js [--dry-run] [--verbose]

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const DATA_DIR = path.join(__dirname, '..', 'docs', 'data');
const TODAY = new Date().toISOString().slice(0, 10);
const DRY_RUN = process.argv.includes('--dry-run');
const VERBOSE = process.argv.includes('--verbose');

// Each ledger has a `scope_denom` regex that filters candidate matches by
// the church's denomination field. This is a critical false-positive guard
// for common-name homonyms (e.g., a "James Miller" who's a Ruling Elder in
// PCA does NOT mean every James Miller in MOOP is the same person).
const LEDGERS = [
  { key: 'warhurst_protest_2020',   file: 'pca-warhurst-signers-2020.json',     arr: 'signers',                    label: 'Warhurst Protest 2020',          year: 2020, direction: 'red',   source: 'warhornmedia.com',                    strict_state: false, scope_denom: /\bpca\b|presbyterian church in america|reformed presbyterian/i },
  { key: 'amr_2026',                file: 'pca-amr-leadership-2026.json',       arr: 'members_and_contributors',  label: 'Alliance for Mission and Renewal',year: 2026, direction: 'red',   source: 'a4mr.org',                            strict_state: false, scope_denom: /\bpca\b|presbyterian|reformed/i },
  { key: 'letter_of_lament_2025',   file: 'pca-letter-of-lament-2025.json',     arr: 'publicly_named_signers',    label: 'PCA Letter of Lament 2025',      year: 2025, direction: 'red',   source: 'pcaprayerandlament.com',              strict_state: false, scope_denom: /\bpca\b|presbyterian church in america|reformed presbyterian/i },
  { key: 'revoice_2018_2026',       file: 'revoice-speakers-and-endorsers.json',arr: 'people',                    label: 'Revoice Speakers/Endorsers',     year: 2018, direction: 'red',   source: 'revoice.us',                          strict_state: false, scope_denom: /\bpca\b|presbyterian|reformed|sbc|southern baptist|anglican|acna|non-denominational|evangelical/i },
  { key: 'cbe_egalitarian_2026',    file: 'cbe-egalitarian-network-2026.json',  arr: 'people',                    label: 'CBE Egalitarian Network',        year: 2026, direction: 'red',   source: 'cbeinternational.org',                strict_state: false, scope_denom: /umc|methodist|wesleyan|free methodist|anglican|\bcma\b|covenant|non-denominational|presbyterian|reformed|baptist|evangelical/i },
  { key: 'dallas_statement_2018',   file: 'dallas-statement-signers-2018.json', arr: 'signers',                    label: 'Dallas Statement 2018',          year: 2018, direction: 'green', source: 'statementonsocialjustice.com',        strict_state: true,  scope_denom: null },
  { key: 'nashville_statement_2017',file: 'nashville-statement-signers-2017.json',arr: 'signers',                  label: 'Nashville Statement 2017',       year: 2017, direction: 'green', source: 'cbmw.org/nashville-statement',        strict_state: true,  scope_denom: null },
];

// ---------- Name normalization ----------

const HONORIFICS = /\b(the\s+rev|very\s+rev|right\s+rev|most\s+rev|rev|reverend|fr|father|dr|pastor|pr|elder|deacon|deaconess|bishop|archbishop|cardinal|monsignor|sister|brother|br|sr|mother)\b\.?/gi;
const SUFFIXES   = /\b(jr|sr|ii|iii|iv|v|esq|phd|dmin|thd|dd|stm|ma|md)\b\.?/gi;

function normalizeName(name) {
  if (!name || typeof name !== 'string') return '';
  let s = name;
  // Strip parenthetical / bracketed annotations
  s = s.replace(/\([^)]*\)/g, ' ');
  s = s.replace(/\[[^\]]*\]/g, ' ');
  // Strip honorifics + suffixes
  s = s.replace(HONORIFICS, ' ');
  s = s.replace(SUFFIXES, ' ');
  // Strip punctuation except hyphens (preserve hyphenated surnames)
  s = s.replace(/[.,;:'"`]/g, ' ');
  // Strip stray quotes
  s = s.replace(/[“”‘’]/g, ' ');
  // Collapse whitespace; lowercase
  s = s.replace(/\s+/g, ' ').trim().toLowerCase();
  return s;
}

function extractFirstLast(name) {
  const norm = normalizeName(name);
  if (!norm) return null;
  // Tokenize on whitespace; drop single-letter middle initials.
  const tokens = norm.split(/\s+/).filter(t => t.length > 1);
  if (tokens.length < 2) return null;
  return tokens[0] + ' ' + tokens[tokens.length - 1];
}

// Parse pastor field that may contain multiple pastors and/or qualifiers.
function parsePastorField(pastorField) {
  if (!pastorField || typeof pastorField !== 'string') return [];
  // Pre-strip qualifying notes
  let s = pastorField;
  // Split on common separators: ; , " and " " & "
  let parts = s.split(/\s*(?:;|,|\s+and\s+|&)\s*/);
  // Map to normalized first+last
  const seen = new Set();
  const result = [];
  for (let p of parts) {
    p = p.trim();
    if (!p) continue;
    // Skip non-name fragments (placeholder strings, etc.)
    if (/^(verify|various|unknown|currently|none|tba|listed|see\s+website|the\s+church|associate\s+pastor|senior\s+pastor|lead\s+pastor|co-pastor|pastor)/i.test(p)) continue;
    // Skip phrases describing role/timing only
    if (/^(senior|associate|assistant|co-?|lead|teaching|preaching|interim|founding|emeritus|sr|jr)\b/i.test(p)) continue;
    // Skip pure descriptions
    if (p.length < 3 || p.length > 80) continue;
    // Skip if doesn't contain at least two word chars-runs (need two name parts)
    if (!/\b[A-Za-z]+\b.*\b[A-Za-z]+\b/.test(p)) continue;
    const fl = extractFirstLast(p);
    if (fl && !seen.has(fl)) {
      seen.add(fl);
      result.push({ raw: p, firstLast: fl });
    }
  }
  return result;
}

// ---------- State extraction ----------

const STATE_NAMES = {
  alabama:'AL',alaska:'AK',arizona:'AZ',arkansas:'AR',california:'CA',colorado:'CO',connecticut:'CT',delaware:'DE',florida:'FL',georgia:'GA',hawaii:'HI',idaho:'ID',illinois:'IL',indiana:'IN',iowa:'IA',kansas:'KS',kentucky:'KY',louisiana:'LA',maine:'ME',maryland:'MD',massachusetts:'MA',michigan:'MI',minnesota:'MN',mississippi:'MS',missouri:'MO',montana:'MT',nebraska:'NE',nevada:'NV','new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY','north carolina':'NC','north dakota':'ND',ohio:'OH',oklahoma:'OK',oregon:'OR',pennsylvania:'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',tennessee:'TN',texas:'TX',utah:'UT',vermont:'VT',virginia:'VA',washington:'WA','west virginia':'WV',wisconsin:'WI',wyoming:'WY','district of columbia':'DC'
};
const STATE_CODES_SET = new Set(Object.values(STATE_NAMES));

function extractState(text) {
  if (!text) return null;
  // 1. Try ", XX " (comma + two-letter code + boundary or zip)
  const m1 = text.match(/,\s*([A-Z]{2})\s*\d{5}/);
  if (m1 && STATE_CODES_SET.has(m1[1])) return m1[1];
  // 2. Try ", XX$" (end of string)
  const m2 = text.match(/,\s*([A-Z]{2})\s*$/);
  if (m2 && STATE_CODES_SET.has(m2[1])) return m2[1];
  // 3. Try " XX$" (space + state + end-of-string; for "Louisville KY"-style)
  const m3 = text.match(/\s([A-Z]{2})\s*$/);
  if (m3 && STATE_CODES_SET.has(m3[1])) return m3[1];
  // 4. Try ", XX " (comma + 2-letter code + whitespace; bounded mid-string)
  const m4 = text.match(/,\s*([A-Z]{2})\b/);
  if (m4 && STATE_CODES_SET.has(m4[1])) return m4[1];
  // 5. Try full state name (preceded by space/comma or at start)
  const lower = text.toLowerCase();
  for (const [name, code] of Object.entries(STATE_NAMES)) {
    if (lower.endsWith(name) || lower.includes(', ' + name) || lower.includes(' ' + name + ',') || lower.includes(' ' + name + ' ')) return code;
  }
  return null;
}

function getChurchState(c) {
  if (c.state && /^[A-Z]{2}$/.test(c.state)) return c.state;
  return extractState(c.address || '') || extractState(c.location && c.location.address) || null;
}

// ---------- Institution token overlap (for Nashville-attributed) ----------

function tokenize(text) {
  if (!text) return new Set();
  return new Set(text.toLowerCase().replace(/[.,;:'"()]/g, ' ').split(/\s+/).filter(t => t.length >= 4 && !/^(the|of|in|and|for|with|from|seminary|church|christian|presbyterian|baptist|reformed|college|university|community|fellowship)$/.test(t)));
}

function tokenOverlap(a, b) {
  if (!a || !b) return 0;
  const tA = tokenize(a);
  const tB = tokenize(b);
  let n = 0;
  for (const t of tA) if (tB.has(t)) n++;
  return n;
}

// ---------- Build index from ledgers ----------

console.log('Loading 7 ledger files...');
const ledgerEntries = [];
for (const meta of LEDGERS) {
  const filePath = path.join(DATA_DIR, meta.file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const arr = data[meta.arr] || [];
  for (const entry of arr) {
    if (!entry || !entry.name) continue;
    const fl = extractFirstLast(entry.name);
    if (!fl) continue;
    ledgerEntries.push({
      ledgerKey: meta.key,
      ledgerLabel: meta.label,
      ledgerYear: meta.year,
      ledgerDirection: meta.direction,
      ledgerSource: meta.source,
      requiresState: meta.strict_state,
      name: entry.name,
      firstLast: fl,
      institution: entry.church_or_institution || entry.church || '',
      denomination: entry.denomination || '',
      presbytery: entry.presbytery || '',
      sourceUrl: entry.source_url || '',
      institutionState: extractState(entry.church_or_institution || entry.church || entry.denomination || ''),
    });
  }
  console.log('  ' + meta.label.padEnd(35) + ' ' + String(arr.length).padStart(6) + ' loaded');
}
console.log('Total ledger entries indexed:', ledgerEntries.length);

// Build first+last → entries multimap
const nameIndex = new Map();
for (const e of ledgerEntries) {
  if (!nameIndex.has(e.firstLast)) nameIndex.set(e.firstLast, []);
  nameIndex.get(e.firstLast).push(e);
}
console.log('Unique first+last names in index:', nameIndex.size);

// ---------- Cross-reference each church ----------

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
let churchesMatched = 0;
let totalSigMatches = 0;
let rejectedNoState = 0;
let aggregateCounts = { green: 0, red: 0, mixed: 0, none: 0 };
const matchesPerLedger = {};
const sampleMatches = [];

for (const c of d.churches) {
  if (!c || !c.pastor) continue;
  const pastors = parsePastorField(c.pastor);
  if (!pastors.length) continue;

  const churchState = getChurchState(c);
  const matches = [];
  const seenLedgerNamePairs = new Set();

  for (const p of pastors) {
    const candidates = nameIndex.get(p.firstLast) || [];
    for (const cand of candidates) {
      const dedupKey = cand.ledgerKey + '|' + cand.firstLast;
      if (seenLedgerNamePairs.has(dedupKey)) continue;
      // Apply denomination scope filter for the small targeted lists.
      const ledgerMeta = LEDGERS.find(l => l.key === cand.ledgerKey);
      if (ledgerMeta && ledgerMeta.scope_denom) {
        const denomText = [c.denomination, c.denomination_family, c.denom_family].filter(Boolean).join(' | ');
        if (!denomText || !ledgerMeta.scope_denom.test(denomText)) {
          continue;
        }
      }
      // Apply state corroboration for big lists
      if (cand.requiresState) {
        if (!churchState) { rejectedNoState++; continue; }
        if (!cand.institutionState) { rejectedNoState++; continue; }
        if (churchState !== cand.institutionState) {
          if (VERBOSE) console.log('   state-mismatch reject: ' + p.firstLast + ' (' + churchState + ' vs ' + cand.institutionState + ')');
          continue;
        }
        // For Nashville's signers with institution metadata, also require token overlap
        if (cand.ledgerKey === 'nashville_statement_2017' && cand.institution && c.name) {
          const overlap = tokenOverlap(cand.institution, c.name);
          if (overlap === 0) {
            if (VERBOSE) console.log('   token-overlap reject: ' + cand.name + ' / ' + c.name);
            continue;
          }
        }
      }
      // Accepted
      seenLedgerNamePairs.add(dedupKey);
      matches.push({
        ledger: cand.ledgerKey,
        ledger_label: cand.ledgerLabel,
        year: cand.ledgerYear,
        direction: cand.ledgerDirection,
        source_url: cand.sourceUrl || cand.ledgerSource,
        signer_name: cand.name,
        matched_via: cand.requiresState ? 'name+state' : 'name',
        moop_pastor: p.raw,
      });
      matchesPerLedger[cand.ledgerKey] = (matchesPerLedger[cand.ledgerKey] || 0) + 1;
    }
  }

  if (matches.length) {
    // MERGE with any pre-existing signatories (don't overwrite — earlier curation may
    // have captured matches we'd otherwise miss, e.g. relaxed-state-corroboration matches).
    // Schema: signatories = { ledger_key: [signer_name, ...] }
    // (Matches existing per-church HTML template at generate-church-pages.js:117-148.)
    const existing = (c.signatories && typeof c.signatories === 'object') ? c.signatories : {};
    const merged = { ...existing };
    let newlyAddedCount = 0;
    for (const m of matches) {
      if (!Array.isArray(merged[m.ledger])) merged[m.ledger] = [];
      if (!merged[m.ledger].includes(m.signer_name)) {
        merged[m.ledger].push(m.signer_name);
        newlyAddedCount++;
      }
    }
    c.signatories = merged;
    // Recompute aggregate from FULL merged set, not just my matches.
    const allDirs = new Set();
    for (const [k, names] of Object.entries(merged)) {
      if (!Array.isArray(names) || !names.length) continue;
      const ledgerMeta = LEDGERS.find(l => l.key === k);
      if (ledgerMeta) allDirs.add(ledgerMeta.direction);
    }
    let agg = 'none';
    if (allDirs.has('green') && allDirs.has('red')) agg = 'mixed';
    else if (allDirs.has('green')) agg = 'green';
    else if (allDirs.has('red')) agg = 'red';
    c.signatures_aggregate = agg;
    aggregateCounts[agg] += 1;
    churchesMatched++;
    totalSigMatches += newlyAddedCount;
    if (newlyAddedCount > 0 && sampleMatches.length < 30) {
      sampleMatches.push({ id: c.id, name: c.name, pastor: c.pastor, agg, matches });
    }
    // Append enrichment note only when we actually added new entries.
    if (newlyAddedCount > 0) {
      const ledgerSummary = matches.map(m => m.ledger_label).join(', ');
      const noteLine = `[${TODAY}] Phase 7 signatory cross-reference: +${newlyAddedCount} new ledger entr${newlyAddedCount === 1 ? 'y' : 'ies'} (${ledgerSummary}). Final aggregate: ${agg}.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteLine : noteLine;
    }
  } else {
    // No matches this run — but if the church has prior populated signatories,
    // recompute aggregate from those (preserves prior data).
    if (c.signatories && typeof c.signatories === 'object') {
      const allDirs = new Set();
      for (const [k, names] of Object.entries(c.signatories)) {
        if (!Array.isArray(names) || !names.length) continue;
        const ledgerMeta = LEDGERS.find(l => l.key === k);
        if (ledgerMeta) allDirs.add(ledgerMeta.direction);
      }
      let agg = 'none';
      if (allDirs.has('green') && allDirs.has('red')) agg = 'mixed';
      else if (allDirs.has('green')) agg = 'green';
      else if (allDirs.has('red')) agg = 'red';
      if (allDirs.size > 0) {
        c.signatures_aggregate = agg;
        aggregateCounts[agg] += 1;
        continue;
      }
    }
    if (!c.signatures_aggregate) c.signatures_aggregate = 'none';
    aggregateCounts.none++;
  }
}

if (!DRY_RUN) {
  d.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
}

console.log('\n========== Cross-Reference Results ==========');
console.log(`Total churches scanned:           ${d.churches.length}`);
console.log(`Churches with ≥1 signatory match: ${churchesMatched}`);
console.log(`Total signatory entries written:  ${totalSigMatches}`);
console.log(`Rejected for no state info:       ${rejectedNoState}`);
console.log('\nAggregate signal distribution:');
for (const [k, v] of Object.entries(aggregateCounts)) console.log(`  ${k.padEnd(8)} ${String(v).padStart(6)}`);
console.log('\nMatches per ledger:');
for (const [k, v] of Object.entries(matchesPerLedger).sort((a, b) => b[1] - a[1])) {
  const meta = LEDGERS.find(l => l.key === k);
  console.log(`  ${k.padEnd(28)} ${String(v).padStart(5)} (${meta.direction})`);
}

console.log('\nFirst 25 sample matches:');
for (const sm of sampleMatches.slice(0, 25)) {
  const ledgers = sm.matches.map(m => m.ledger_label + (m.direction === 'green' ? ' (G)' : ' (R)')).join('; ');
  console.log(`  [${sm.agg.padEnd(5)}] ${(sm.name || '').slice(0, 45).padEnd(45)} <- ${(sm.pastor || '').slice(0, 40)}`);
  console.log(`            ${ledgers}`);
}
