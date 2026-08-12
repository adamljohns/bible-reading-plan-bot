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
const eligible = churches.filter(c =>
  SOCIAL ? socialEligible(c)
    : (RETRY ? lanes.retryEligible(c) : lanes.freshEligible(c)));
eligible.sort((a, b) => String(a.id).localeCompare(String(b.id)));

const mode = SOCIAL ? 'SOCIAL: website + no social link' : RETRY ? 'RETRY: one no-pastor strike' : 'never-attempted';
console.log(`Eligible pool (${mode}, pastor-fetchable): ${eligible.length}`);
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
