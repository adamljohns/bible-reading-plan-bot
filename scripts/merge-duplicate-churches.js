#!/usr/bin/env node
// Merge duplicate church records (Adam, 2026-08-12: "I don't want duplicates —
// often the same church with a slightly different name; tell them by city+state
// and crosscheck address or pastor").
//
// Report-first. Two tiers:
//   AUTO   — high-confidence same-church pairs, merged when --apply is passed.
//   REVIEW — plausible but uncorroborated; written to
//            docs/data/research-leads/duplicate-review-queue.json, never auto-merged.
//
// Candidate blocking: (a) same state + identical normalized name-signature
// (word-order/punctuation/1st→first insensitive), (b) same state + same website
// domain (catches renames — ids and even names can differ).
//
// AUTO requires corroboration, and hard guards demote to REVIEW:
//   - both records carry REAL but DIFFERENT pastors (could be two congregations)
//   - denomination families disagree coarsely and the domains don't match
//   - both have street addresses that disagree AND zips disagree (multi-campus /
//     same-name-different-town) unless domain+pastor both corroborate
//
// Merge semantics: keep the RICHER record, absorb missing fields from the dup,
// record merged_from + a provenance note, delete the dup, add a redirect stub
// page (docs/churches/<dup>.html, marked <!-- merged-redirect -->) so old links
// and search results never 404, and append to docs/data/merged-redirects.json.
//
// Usage:
//   node scripts/merge-duplicate-churches.js                # dry-run report
//   node scripts/merge-duplicate-churches.js --apply        # merge AUTO tier
//   node scripts/merge-duplicate-churches.js --apply --max 200

const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const ROOT = path.join(__dirname, '..');
const APPLY = process.argv.includes('--apply');
const MAXi = process.argv.indexOf('--max');
const MAX = MAXi > -1 ? parseInt(process.argv[MAXi + 1], 10) || Infinity : Infinity;
const TODAY = new Date().toISOString().slice(0, 10);

const { data: d, write } = makeWriter(path.join(ROOT, 'docs/data/churches.json'));

// ── normalization ────────────────────────────────────────────────────────────
const norm = s => String(s || '').toLowerCase().replace(/&/g, ' and ')
  .replace(/[^a-z0-9 ]/g, ' ').replace(/\b1st\b/g, 'first').replace(/\b2nd\b/g, 'second')
  .replace(/\bmt\b/g, 'mount').replace(/\s+/g, ' ').trim();
const NOISE = new Set(['the', 'of', 'at', 'in', 'inc', 'a']);
const sig = n => norm(n).split(' ').filter(t => t && !NOISE.has(t)).sort().join('|');

// Generic tokens — a name is DISTINCTIVE if it carries a ≥5-char token outside this set.
const GENERIC = new Set(['church', 'churches', 'baptist', 'first', 'second', 'community', 'grace', 'christ', 'christian', 'fellowship', 'bible', 'ministries', 'ministry', 'chapel', 'saint', 'trinity', 'calvary', 'cornerstone', 'hope', 'faith', 'life', 'family', 'worship', 'center', 'centre', 'assembly', 'gospel', 'covenant', 'reformed', 'presbyterian', 'lutheran', 'methodist', 'pentecostal', 'catholic', 'orthodox', 'missionary', 'memorial', 'mount', 'valley', 'river', 'creek', 'lake', 'park', 'north', 'south', 'east', 'west', 'springs', 'heights', 'hills', 'grove', 'road', 'street', 'avenue', 'united', 'evangelical', 'emmanuel', 'immanuel', 'bethel', 'bethany', 'zion', 'antioch', 'shiloh', 'ebenezer', 'providence', 'redeemer', 'resurrection', 'ascension', 'nazarene', 'wesleyan', 'anglican', 'episcopal', 'apostolic', 'temple', 'tabernacle', 'house', 'living', 'light', 'truth', 'word', 'spirit', 'holy', 'good', 'shepherd', 'sovereign', 'victory', 'harvest', 'heritage', 'liberty', 'freedom', 'pleasant', 'friendship', 'union', 'central', 'highland', 'ridge', 'point', 'pointe', 'crossroads', 'journey', 'mission', 'anchor', 'lighthouse', 'kings', 'kingdom']);
const distinctive = n => norm(n).split(' ').some(t => t.length >= 5 && !GENERIC.has(t));

const zipOf = c => { const m = String(c.address || '').match(/\b(\d{5})(?:-\d{4})?\s*$/); return m ? m[1] : null; };
const cityOf = c => {
  const a = String(c.address || '');
  let m = a.match(/,\s*([A-Za-z .'-]+?),?\s+(?:[A-Z]{2}|Virginia|Texas|Florida|Georgia|Alabama|Tennessee|Carolina|Kentucky|Ohio|Indiana|Illinois|Missouri|Michigan|California|Oklahoma|Arkansas|Louisiana|Mississippi|Washington|Oregon|Colorado|Arizona|Pennsylvania|York|Jersey|Maryland|Massachusetts)\b/);
  return m ? norm(m[1]) : null;
};
const streetOf = c => { const m = String(c.address || '').match(/\b(\d{1,6})\s+([A-Za-z]+)/); return m ? (m[1] + '|' + m[2].toLowerCase()) : null; };
const isPh = p => { p = String(p || '').trim().toLowerCase(); return !p || /verify|see website|see site|not published|search in progress|to be announced|to be determined|coming soon/.test(p) || /^((the |a )?(pastor|pastors|elder|elders|staff|tbd|n\/a|none|unknown|various))$/.test(p); };
const pastorKey = c => { if (isPh(c.pastor)) return null; return norm(String(c.pastor).replace(/\b(rev|dr|pastor|elder|bro|mr|fr|bishop|min)\.?\b/gi, '')).split(' ').slice(0, 3).join(' ') || null; };
const domainOf = c => { try { const h = new URL(c.website).hostname.replace(/^www\./, ''); return h.split('.').slice(-2).join('.'); } catch (_) { return null; } };
const fbOf = c => { const m = String(c.facebook || '').match(/facebook\.com\/([^/?#]+)/i); return m ? m[1].toLowerCase() : null; };
const famCoarse = c => {
  const s = String(c.denomination_family || c.denomination || '').toLowerCase();
  for (const f of ['anabaptist', 'baptist', 'presbyterian|reformed|pca|opc', 'anglican|episcopal', 'lutheran', 'methodist|wesleyan|nazarene', 'pentecostal|charismatic|assembl|foursquare|vineyard|calvary chapel', 'catholic|orthodox']) {
    if (new RegExp(f).test(s)) return f;
  }
  return 'other';
};
const richness = c => {
  let s = 0;
  if (!isPh(c.pastor)) s += 4;
  if (typeof c.website === 'string' && /^https?:/.test(c.website)) s += 2;
  if (c.facebook || c.youtube || c.instagram) s += 1;
  if (c.scores && Object.values(c.scores).some(v => v && v !== 'gray')) s += 3;
  if (c.assessment) s += 2;
  if (isFinite(parseFloat(c.latitude))) s += 1;
  return s + Object.keys(c).length * 0.01;
};

// ── candidate pairs ──────────────────────────────────────────────────────────
const bySig = new Map(), byDom = new Map();
for (const c of d.churches) {
  if (!c || !c.id) continue;
  const st = String(c.state || '').toUpperCase();
  const s = sig(c.name);
  if (s) { const k = st + '|' + s; (bySig.get(k) || bySig.set(k, []).get(k)).push(c); }
  const dom = domainOf(c);
  if (dom) { const k = st + '|' + dom; (byDom.get(k) || byDom.set(k, []).get(k)).push(c); }
}
const pairKeys = new Set(); const pairs = [];
const addPairs = (group, via) => {
  for (let i = 0; i < group.length; i++) for (let j = i + 1; j < group.length; j++) {
    const [a, b] = [group[i], group[j]];
    const k = a.id < b.id ? a.id + '||' + b.id : b.id + '||' + a.id;
    if (!pairKeys.has(k)) { pairKeys.add(k); pairs.push([a, b, via]); }
  }
};
for (const g of bySig.values()) if (g.length > 1 && g.length <= 6) addPairs(g, 'name');
for (const g of byDom.values()) if (g.length > 1 && g.length <= 6) addPairs(g, 'domain');

// ── classify ─────────────────────────────────────────────────────────────────
const auto = [], review = [];
for (const [a, b, via] of pairs) {
  const ev = [];
  const zA = zipOf(a), zB = zipOf(b), sameZip = zA && zB && zA === zB;
  const cA = cityOf(a), cB = cityOf(b), sameCity = cA && cB && cA === cB;
  const stA = streetOf(a), stB = streetOf(b), sameStreet = stA && stB && stA === stB;
  const pA = pastorKey(a), pB = pastorKey(b), samePastor = pA && pB && pA === pB;
  const dA = domainOf(a), dB = domainOf(b), sameDomain = dA && dB && dA === dB;
  const fA = fbOf(a), fB = fbOf(b), sameFB = fA && fB && fA === fB;
  const sigEqual = sig(a.name) === sig(b.name);
  if (sameZip) ev.push('zip'); if (sameCity) ev.push('city'); if (sameStreet) ev.push('street');
  if (samePastor) ev.push('pastor'); if (sameDomain) ev.push('domain'); if (sameFB) ev.push('facebook');
  if (sigEqual) ev.push('name-sig');

  // guards → REVIEW
  const conflictingPastors = pA && pB && pA !== pB;
  const famMismatch = famCoarse(a) !== famCoarse(b) && !sameDomain;
  const bothStreetsDiffer = stA && stB && stA !== stB && zA && zB && zA !== zB && !(sameDomain && samePastor);
  const idSuffix = (a.id.startsWith(b.id) && /^-(2|3|4|inc|the)\b/.test(a.id.slice(b.id.length))) ||
                   (b.id.startsWith(a.id) && /^-(2|3|4|inc|the)\b/.test(b.id.slice(a.id.length)));

  let cls = 'review';
  if (!conflictingPastors && !famMismatch && !bothStreetsDiffer) {
    if (sameDomain && (sameZip || sameCity || sigEqual)) cls = 'auto';
    else if (sigEqual && sameZip && (sameStreet || samePastor || sameFB || distinctive(a.name))) cls = 'auto';
    else if (sigEqual && sameCity && (sameStreet || samePastor || sameFB)) cls = 'auto';
    else if (idSuffix && (sameZip || sameCity)) cls = 'auto';
  }
  const rec = { a: a.id, b: b.id, nameA: a.name, nameB: b.name, via, evidence: ev, guards: [conflictingPastors && 'pastors-differ', famMismatch && 'family-mismatch', bothStreetsDiffer && 'addresses-differ'].filter(Boolean) };
  (cls === 'auto' ? auto : review).push(rec);
}

console.log(`Candidate pairs: ${pairs.length} | AUTO: ${auto.length} | REVIEW: ${review.length}`);
auto.slice(0, 15).forEach(r => console.log(`  AUTO  ${r.a}  <->  ${r.b}  [${r.evidence.join(',')}]`));
review.slice(0, 6).forEach(r => console.log(`  REVW  ${r.a}  <->  ${r.b}  [${r.evidence.join(',')}]${r.guards.length ? ' guards:' + r.guards.join(',') : ''}`));

// Always (re)write the review queue — it's a leads file, not site data.
const qPath = path.join(ROOT, 'docs/data/research-leads/duplicate-review-queue.json');
fs.mkdirSync(path.dirname(qPath), { recursive: true });
fs.writeFileSync(qPath, JSON.stringify({ generated: TODAY, count: review.length, pairs: review }, null, 1).replace(/[^\x00-\x7F]/g, ch => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0')));
console.log(`review queue → ${path.relative(ROOT, qPath)} (${review.length} pairs)`);

if (!APPLY) { console.log('\nDRY RUN — pass --apply to merge the AUTO tier.'); process.exit(0); }

// ── merge AUTO tier ──────────────────────────────────────────────────────────
const byId = new Map(d.churches.map(c => [c.id, c]));
const redirPath = path.join(ROOT, 'docs/data/merged-redirects.json');
let redirects = {};
try { redirects = JSON.parse(fs.readFileSync(redirPath, 'utf8')).redirects || {}; } catch (_) { }
const gone = new Set();
let merged = 0;
const ABSORB = ['website', 'facebook', 'youtube', 'instagram', 'twitter', 'founded', 'services', 'image_url', 'image_thumb', 'pastor_credentials'];
for (const r of auto) {
  if (merged >= MAX) break;
  const a = byId.get(r.a), b = byId.get(r.b);
  if (!a || !b || gone.has(a.id) || gone.has(b.id)) continue;
  const keep = richness(a) >= richness(b) ? a : b;
  const dup = keep === a ? b : a;
  const absorbed = [];
  for (const f of ABSORB) if ((keep[f] === undefined || keep[f] === '' || keep[f] === null) && dup[f]) { keep[f] = dup[f]; absorbed.push(f); }
  if (isPh(keep.pastor) && !isPh(dup.pastor)) { keep.pastor = dup.pastor; if (dup.pastors) keep.pastors = dup.pastors; absorbed.push('pastor'); }
  if (!isFinite(parseFloat(keep.latitude)) && isFinite(parseFloat(dup.latitude))) { keep.latitude = dup.latitude; keep.longitude = dup.longitude; absorbed.push('geo'); }
  if ((!keep.region || ['va', 'none', 'rest_of_us'].includes(keep.region)) && dup.region && !['va', 'none', 'rest_of_us'].includes(dup.region)) { keep.region = dup.region; absorbed.push('region'); }
  if (Array.isArray(dup.tags) && dup.tags.length) keep.tags = [...new Set([...(keep.tags || []), ...dup.tags])];
  if (Array.isArray(dup.enrichment_sources) && dup.enrichment_sources.length) keep.enrichment_sources = [...new Set([...(keep.enrichment_sources || []), ...dup.enrichment_sources])];
  keep.merged_from = [...new Set([...(keep.merged_from || []), dup.id])];
  keep.needs_review = keep.needs_review || dup.needs_review || false;
  const note = `[${TODAY}] Merged duplicate record '${dup.id}' ("${dup.name}") — same church (evidence: ${r.evidence.join(', ')}).${absorbed.length ? ' Absorbed: ' + absorbed.join(', ') + '.' : ''}`;
  keep.enrichment_notes = keep.enrichment_notes ? keep.enrichment_notes + '\n' + note : note;
  redirects[dup.id] = keep.id;
  gone.add(dup.id);
  merged++;
  console.log(`  MERGED ${dup.id}  →  ${keep.id}${absorbed.length ? '  (+' + absorbed.join(',') + ')' : ''}`);
}
d.churches = d.churches.filter(c => !gone.has(c.id));
d.total_churches = d.churches.length;
write(d);
fs.writeFileSync(redirPath, JSON.stringify({ updated: TODAY, redirects }, null, 1));

// Redirect stubs so old URLs / search results land on the keeper.
for (const [dupId, keepId] of Object.entries(redirects)) {
  if (!gone.has(dupId)) continue; // only write stubs for THIS run's merges
  const stub = `<!doctype html><!-- merged-redirect --><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/churches/${keepId}.html"><link rel="canonical" href="https://usmcmin.org/churches/${keepId}.html"><title>Moved</title></head><body><p>This listing was merged. <a href="/churches/${keepId}.html">Continue to the church page →</a></p></body></html>`;
  fs.writeFileSync(path.join(ROOT, 'docs/churches', dupId + '.html'), stub);
}
console.log(`\nMerged ${merged} duplicates. churches: ${d.churches.length}. Redirect stubs written. Regenerate + check-consistency before pushing.`);
