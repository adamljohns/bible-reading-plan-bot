#!/usr/bin/env node
/**
 * Select a batch of churches eligible for pastor enrichment — and write ready-to-run
 * batch files for the research agents.
 *
 * EXCLUDES already-attempted churches on TWO signals:
 *   1. the `_loop_round_attempted` / `_verify_round_attempted` flags, and
 *   2. any church whose `enrichment_notes` already carry a "Phase 6f" live-fetch
 *      marker (found / no-pastor / broken).
 * Selecting on the flags alone re-attempts churches tried on a prior run and stacks
 * DUPLICATE "no parseable pastor" notes — the selection gap found 2026-07-02, when a
 * batch re-hit ~6 Acts2 CA churches already attempted 2026-06-17.
 *
 * Eligible = needs_review && placeholder-pastor && http(s) website && US state &&
 *            ASCII/English name && not previously attempted.
 *
 * Usage:
 *   node scripts/select-enrichment-batch.js [--count 60] [--batches 3] [--out /tmp]
 *   node scripts/select-enrichment-batch.js --full-review [--count 25] [--include id1,id2] [--out /tmp]
 *     (full-review mode writes <out>/full-review-batch.json; see full-review-round.sh)
 *
 * Writes <out>/enrich-batch-1.json .. -<batches>.json (deterministic id-sorted,
 * round-robin split) — each an array of {id,name,city,state,website,denomination}.
 * Prints the eligible pool size and what it wrote. Read-only on churches.json.
 */
const fs = require('fs');
const path = require('path');
const lanes = require('./lib/grind-lanes.js');

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 && args[i + 1] ? args[i + 1] : def; };
const COUNT = parseInt(opt('--count', '60'), 10);
const BATCHES = parseInt(opt('--batches', '3'), 10);
const OUT = opt('--out', '/tmp');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const churches = JSON.parse(fs.readFileSync(CHURCHES, 'utf8')).churches;


// Base fetchability: placeholder pastor + real website + US + ASCII name.
// (2026-07-03: the needs_review===true gate was dropped — it was an accident of
// which import wave set the flag, not a statement about enrichability, and it
// hid ~600 fetchable churches.)
// _dead_site (2026-08-07): the live fetch already returned 404 / timeout /
// ssl_error / redirect_loop / not_a_church. No pastor can be scraped from a
// site that does not answer, so such a church is not fetchable in ANY mode.
// Without this the retry pool recycled the same 50 dead sites indefinitely.
const fetchable = lanes.pastorFetchable;

// --retry mode (2026-07-03): second pass over churches attempted EXACTLY once
// that came back "no parseable pastor" — the extractor's smarter page discovery
// (homepage link-following) often finds the staff page the fixed paths missed.
// Two strikes and the record leaves the automated pool for good.
const RETRY = args.includes('--retry');
const noPastorStrikes = lanes.noPastorStrikes;

// --social mode (2026-07-04): fill social links (fb/yt/ig) for churches that have a
// website but no social on file — a huge second tranche (~7k) so the local sessions
// stay productive for a week after the pastor pool dries. Pastor status is irrelevant
// here; the extractor harvests socials deterministically (regex, no LLM) on the fetch.
const SOCIAL = args.includes('--social');

// _social_scraped (2026-08-06) is the marker left by scripts/scrape-church-social.js,
// which harvested 10,200 church sites directly. Without honouring it the grind
// re-fetches every site that harvest already visited and found nothing on —
// thousands of churches whose only possible outcome is another empty round.
const socialEligible = lanes.socialEligible;

// _hold_review (2026-07-11): the merge guard HELD an extracted name (junk-looking or
// typically-female lead) for manual MOOP-rubric review. Re-fetching would only re-extract
// the same held candidate, so held records leave BOTH pastor pools until a human clears
// the flag. Without this, a held church pinned pool_fresh at 1 and the grind spun on it
// for 5 days (500 rounds, zero net pastors).
// --state / --region (2026-10-03): the lanes are nationwide, so there was no way
// to aim a session at the churches a reader is actually likely to open. Both
// narrow the lane pool AFTER lane eligibility, so a targeted run can never pull
// in a record the lane itself would have refused (dead site, held review, etc).
//   --state VA          one or more postal codes, comma-separated
//   --region <regex>    case-insensitive, matched against name/city/address/id
// Omit both and behaviour is exactly as before.
const STATES = opt('--state', '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
const REGION = opt('--region', '');
const regionRe = REGION ? new RegExp(REGION, 'i') : null;
const inScope = c => {
  if (STATES.length && !STATES.includes(String(c.state || '').toUpperCase())) return false;
  if (regionRe && !regionRe.test([c.name, c.city, c.address, c.id].filter(Boolean).join(' '))) return false;
  return true;
};

// --full-review (2026-11-08, Chaps ticket): select for a FULL review round —
// pastor re-check (real names included), all ten rubric categories, profile
// fill, duplicate/identity flags. Output goes to scripts/full-review-fetch.py,
// whose findings become a review patch + HOLD queue (never a direct write).
// Selection order (lexicographic):
//   (a) denomination ordains women (affirming mainline first: TEC, ELCA,
//       PCUSA, UCC, UMC, Disciples, RCA, MCUSA; then ABC-USA, CBF, ...)
//   (b) within FULL_REVIEW_RADIUS_MI (25) of Fredericksburg, VA
//   (c) yellow / assessment pending, oldest review first
//   (d) everything else, oldest review first
//   --count N (default 25, max 60)   --include id1,id2 (forced to the front)
if (args.includes('--full-review')) {
  const { denomPrior } = require('./lib/denomination-priors.js');
  const FXBG = [38.3032, -77.4605];
  const RADIUS = Number(process.env.FULL_REVIEW_RADIUS_MI || 25);
  const N = Math.max(1, Math.min(60, parseInt(opt('--count', '25'), 10) || 25));
  const include = opt('--include', '').split(',').map(s => s.trim()).filter(Boolean);
  const miles = (a, b) => {
    const R = 3958.8, rad = x => x * Math.PI / 180;
    const dLa = rad(b[0] - a[0]), dLo = rad(b[1] - a[1]);
    const h = Math.sin(dLa / 2) ** 2 + Math.cos(rad(a[0])) * Math.cos(rad(b[0])) * Math.sin(dLo / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  };
  const nearFxbg = c => {
    const la = parseFloat(c.latitude), lo = parseFloat(c.longitude);
    if (Number.isFinite(la) && Number.isFinite(lo)) return miles(FXBG, [la, lo]) <= RADIUS;
    return c.region === 'fxbg';
  };
  const pending = c => c.overall_rating === 'yellow' || /assessment pending|not yet reviewed|needs local evaluation/i.test(String(c.overall_label || ''));
  // "Oldest" = the most recent review-ish date we hold; none on file = oldest of all.
  const reviewedAt = c => {
    const ds = [c.last_reviewed, c.pastor_fetched_at, c.full_review_at]
      .map(v => Date.parse(v || '')).filter(Number.isFinite);
    return ds.length ? Math.max(...ds) : 0;
  };
  // Churches with a PENDING hold from an earlier (not yet applied) full review
  // stay out until Chaps clears them, exactly like _hold_review in the pastor lanes.
  const heldIds = new Set();
  try {
    const hq = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'full-review', 'hold-queue.json'), 'utf8'));
    (hq.holds || []).filter(h => h.qa_status === 'pending' && !h.dry_run).forEach(h => heldIds.add(h.church_id));
  } catch (_) { /* no queue yet */ }
  const now = Date.now();
  const pool = churches.filter(c => lanes.fullReviewEligible(c, now) && !heldIds.has(c.id) && inScope(c));
  const key = c => {
    const d = denomPrior(c);
    const a = d && d.ordains_women ? (d.affirming ? 0 : 1) : 2;
    return [a, nearFxbg(c) ? 0 : 1, pending(c) ? 0 : 1, reviewedAt(c)];
  };
  const cmp = (x, y) => { for (let i = 0; i < x.k.length; i++) if (x.k[i] !== y.k[i]) return x.k[i] - y.k[i]; return String(x.c.id).localeCompare(String(y.c.id)); };
  const ranked = pool.map(c => ({ c, k: key(c) })).sort(cmp);
  const byId = new Map(churches.map(c => [c.id, c]));
  const forced = include.map(id => byId.get(id)).filter(Boolean);
  const missing = include.filter(id => !byId.has(id));
  const pick = [...forced, ...ranked.map(r => r.c).filter(c => !include.includes(c.id))].slice(0, N);
  const tierOf = c => { const k = key(c); return k[0] < 2 ? 'a-ordains-women' : k[1] === 0 ? 'b-fxbg-25mi' : k[2] === 0 ? 'c-yellow-pending' : 'd-rest'; };
  const rich = c => ({
    id: c.id, name: c.name, city: c.city || null, state: c.state, address: c.address || null,
    website: hasWebsiteStr(c.website) ? c.website : null, facebook: c.facebook || null,
    denomination: c.denomination || c.denomination_family || null, denomination_family: c.denomination_family || null,
    pastor: c.pastor || null, overall_rating: c.overall_rating || null,
    latitude: c.latitude ?? null, longitude: c.longitude ?? null,
    selection_tier: include.includes(c.id) ? 'forced (--include)' : tierOf(c),
  });
  const tiers = {};
  ranked.forEach(r => { const t = tierOf(r.c); tiers[t] = (tiers[t] || 0) + 1; });
  // Same line shape as the other modes so shell callers can size the round.
  console.log(`Eligible pool (FULL-REVIEW, pastor-fetchable): ${pool.length}`);
  console.log(`  tiers: ${Object.entries(tiers).sort().map(([k, v]) => `${k}=${v}`).join(' ')}`);
  if (missing.length) console.log(`  WARNING --include ids not found: ${missing.join(', ')}`);
  const f = path.join(OUT, 'full-review-batch.json');
  fs.writeFileSync(f, JSON.stringify(pick.map(rich), null, 2));
  console.log(`  wrote ${f}: ${pick.length} churches`);
  console.log(`Selected ${pick.length} of ${pool.length} eligible (full review).`);
  process.exit(0);
}
function hasWebsiteStr(w) { return typeof w === 'string' && /^https?:\/\/[^/\s]/i.test(w); }

const laneEligible = churches.filter(c =>
  SOCIAL ? socialEligible(c)
    : (RETRY ? lanes.retryEligible(c) : lanes.freshEligible(c)));
const eligible = laneEligible.filter(inScope);
eligible.sort((a, b) => String(a.id).localeCompare(String(b.id)));

const mode = SOCIAL ? 'SOCIAL: website + no social link' : RETRY ? 'RETRY: one no-pastor strike' : 'never-attempted';
// Keep this string shape verbatim — pastor-refine-local.sh greps
// /pastor-fetchable\): [0-9]+/ out of it to size the round.
console.log(`Eligible pool (${mode}, pastor-fetchable): ${eligible.length}`);
if (STATES.length || regionRe) {
  console.log(`  scope filter: ${[STATES.length ? 'state=' + STATES.join('/') : '', REGION ? 'region=/' + REGION + '/i' : ''].filter(Boolean).join(' ')} — narrowed ${laneEligible.length} -> ${eligible.length}`);
}
const pick = eligible.slice(0, COUNT);
const slim = c => ({ id: c.id, name: c.name, city: c.city || null, state: c.state, website: c.website, denomination: c.denomination || c.denomination_family || null });
const batches = Array.from({ length: BATCHES }, () => []);
pick.forEach((c, i) => batches[i % BATCHES].push(slim(c)));
batches.forEach((b, i) => {
  const f = path.join(OUT, `enrich-batch-${i + 1}.json`);
  fs.writeFileSync(f, JSON.stringify(b, null, 2));
  console.log(`  wrote ${f}: ${b.length} churches`);
});
console.log(`Selected ${pick.length} of ${eligible.length} eligible into ${BATCHES} batch file(s).`);
