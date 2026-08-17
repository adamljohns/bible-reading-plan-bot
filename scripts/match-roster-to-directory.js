#!/usr/bin/env node
/**
 * Match a harvested denominational roster against the directory.
 *
 * Every roster congregation lands in exactly one bucket:
 *
 *   MATCHED   we already have it. If the roster knows a pastor and our record
 *             is blank, that becomes a PASTOR LEAD -- the denomination's own
 *             record of who leads its own congregation.
 *   NEW       no plausible candidate. Feeds add-discovered-churches.js.
 *   AMBIGUOUS a candidate exists but corroboration is weak. Goes to a review
 *             queue; never auto-applied and never auto-added, because guessing
 *             wrong in EITHER direction is costly: a false match writes the
 *             wrong pastor onto a real church, and a false miss creates the
 *             duplicate Adam explicitly does not want.
 *
 * Identity rules come from scripts/lib/church-identity.js, the same module the
 * duplicate-merge engine uses, so "already have it" means precisely what
 * "duplicate" means.
 *
 * Read-only. Writes report files only; applying is a separate, explicit step.
 *
 * Usage: node scripts/match-roster-to-directory.js --roster /tmp/roster-sbcv.json
 *          [--out docs/data/research-leads] [--state VA]
 */
const fs = require('fs');
const path = require('path');
const ID = require('./lib/church-identity.js');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };

const ROSTER = opt('--roster', '/tmp/roster-sbcv.json');
const ROOT = path.join(__dirname, '..');
const OUT = opt('--out', path.join(ROOT, 'docs/data/research-leads'));
const ONLY_STATE = opt('--state', '');

const roster = JSON.parse(fs.readFileSync(ROSTER, 'utf8'));
const dir = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs/data/churches.json'), 'utf8')).churches;

// Index the directory by state+city and by state+zip for cheap blocking.
// A third block on street catches rows whose city failed to parse: SBCV listed
// Catalyst Church as "311 Selden Road, , VA" while we hold the identical street
// in Newport News, and city-only blocking never put them in the same pool.
const byCity = new Map(), byZip = new Map(), byStreet = new Map();
const push = (m, k, v) => { if (!k) return; if (!m.has(k)) m.set(k, []); m.get(k).push(v); };
for (const c of dir) {
  const st = String(c.state || '').toUpperCase();
  push(byCity, st + "|" + ID.cityOfLoose(c), c);
  push(byZip, st + '|' + ID.zipOf(c), c);
  push(byStreet, st + '|' + ID.streetOf(c), c);
}

/** Roster rows arrive already split into fields; present them like a church record. */
const asChurch = r => ({
  name: r.name,
  address: [r.street, `${r.city}, ${r.state} ${r.zip}`].filter(Boolean).join(', '),
  city: r.city, state: r.state, pastor: r.pastor || '',
});

const matched = [], pastorLeads = [], fresh = [], ambiguous = [];

for (const r of roster.churches) {
  const st = String(r.state || '').toUpperCase();
  if (ONLY_STATE && st !== ONLY_STATE.toUpperCase()) continue;

  const rc = asChurch(r);
  const rSig = ID.sig(r.name), rStreet = ID.streetOf(rc), rZip = r.zip || null;
  const rPastor = ID.pastorKey(rc);

  // Candidate pool: same state and (same city OR same ZIP).
  const pool = new Map();
  for (const c of (byCity.get(st + '|' + ID.norm(r.city)) || [])) pool.set(c.id, c);
  for (const c of (byZip.get(st + '|' + rZip) || [])) pool.set(c.id, c);
  for (const c of (byStreet.get(st + '|' + rStreet) || [])) pool.set(c.id, c);

  let best = null, bestScore = -1, bestWhy = [];
  for (const c of pool.values()) {
    const why = [];
    let score = 0;
    if (ID.sig(c.name) === rSig) { score += 5; why.push('name-signature'); }
    else if (ID.norm(c.name).includes(ID.norm(r.name)) || ID.norm(r.name).includes(ID.norm(c.name))) { score += 3; why.push('name-substring'); }
    // A shared ZIP is not evidence of anything on its own -- a first pass without
    // this gate produced 323 "ambiguous" pairs whose entire case was city+zip,
    // and paired Charlottesville Community Church with Church of the Good
    // Shepherd because they share a ZIP. Geography corroborates a name match; it
    // never substitutes for one.
    if (!why.length) continue;
    if (rStreet && ID.streetOf(c) === rStreet) { score += 4; why.push('street'); }
    if (rZip && ID.zipOf(c) === rZip) { score += 2; why.push('zip'); }
    if (rPastor && ID.pastorKey(c) === rPastor) { score += 4; why.push('pastor'); }
    const cCity = ID.cityOfLoose(c);
    if (cCity && r.city && cCity === ID.norm(r.city)) { score += 2; why.push('city'); }
    if (score > bestScore) { best = c; bestScore = score; bestWhy = why; }
  }

  const nameHit = bestWhy.includes('name-signature') || bestWhy.includes('name-substring');
  const geo = bestWhy.includes('zip') || bestWhy.includes('city');
  // Do BOTH records name a street, and are they different? That is the one
  // pattern that stays ambiguous no matter how well the names agree -- it is
  // either a relocation or two congregations sharing a name, and the merge
  // engine treats it the same way (bothStreetsDiffer demotes to review).
  const bestStreet = best ? ID.streetOf(best) : null;
  const streetConflict = best ? ID.streetsDiffer(rc, best) : false;

  // An EXACT full-name signature inside the same ZIP or city is decisive even
  // for a generic name: "Central Baptist Church" is common statewide but not
  // twice within one Norfolk ZIP. Requiring distinctive() here left 8 plainly
  // identical pairs (Camo Church, Shiloh Baptist Carson, Highland Baptist
  // Monterey ...) sitting in review purely because our record lacked a street.
  // A mere SUBSTRING match still needs a distinctive name to count.
  const corroborated = bestWhy.includes('street') || bestWhy.includes('pastor')
    || (geo && bestWhy.includes('name-signature') && !streetConflict)
    || (geo && ID.distinctive(r.name) && !streetConflict);

  if (best && nameHit && corroborated) {
    matched.push({ roster: r.name, id: best.id, evidence: bestWhy, score: bestScore });
    // The denomination's own record of who leads its own congregation.
    if (r.pastor && ID.isPh(best.pastor)) {
      pastorLeads.push({
        id: best.id, name: best.name, city: best.city || r.city, state: st,
        pastor: r.pastor, source: roster.source, evidence_url: r.detail_url,
        match_evidence: bestWhy,
      });
    }
  } else if (best && bestScore >= 3) {
    ambiguous.push({
      roster: r.name, roster_address: rc.address, roster_pastor: r.pastor || '',
      candidate_id: best.id, candidate_name: best.name, candidate_address: best.address || '',
      evidence: bestWhy, score: bestScore, detail_url: r.detail_url,
    });
  } else {
    fresh.push({
      name: r.name, address: rc.address, city: r.city, state: st,
      website: r.website || '', denomination: roster.denomination,
      pastor: r.pastor || '', phone: r.phone || '',
      evidence_url: r.detail_url, confidence: 'high',
      source_label: `the ${roster.source} roster`,
      source_tag: `roster-${roster.source_key || 'roster'}-${roster.harvested}`,
    });
  }
}

fs.mkdirSync(OUT, { recursive: true });
const key = roster.source_key || 'roster';
const files = {
  [`${key}-pastor-leads.json`]: pastorLeads,
  [`${key}-new-churches.json`]: fresh,
  [`${key}-ambiguous.json`]: ambiguous,
};
for (const [f, v] of Object.entries(files)) fs.writeFileSync(path.join(OUT, f), JSON.stringify(v, null, 2));

const considered = matched.length + fresh.length + ambiguous.length;
console.log(`Roster: ${roster.source} — ${considered} congregations considered${ONLY_STATE ? ` (state ${ONLY_STATE})` : ''}\n`);
console.log(`  MATCHED    ${String(matched.length).padStart(4)}  already in the directory`);
console.log(`     └─ pastor leads ${String(pastorLeads.length).padStart(3)}  (roster knows the pastor, we had a blank)`);
console.log(`  NEW        ${String(fresh.length).padStart(4)}  not in the directory`);
console.log(`  AMBIGUOUS  ${String(ambiguous.length).padStart(4)}  candidate exists, corroboration weak -> review`);
console.log(`\nWrote ${Object.keys(files).length} files to ${OUT}`);
if (fresh.length) {
  const noWeb = fresh.filter(f => !f.website).length;
  console.log(`\nNOTE: ${noWeb} of ${fresh.length} NEW churches have no website. The 2026-07-11`);
  console.log('zero-presence gate in add-discovered-churches.js will skip those. They do carry a');
  console.log('denominational roster URL, an address and often a pastor — whether that clears the');
  console.log("gate is Adam's policy call, not this script's.");
}
