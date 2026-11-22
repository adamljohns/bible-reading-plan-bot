#!/usr/bin/env node
'use strict';
// recheck-discovered-websites.js — re-run every website-discovery hit since --since
// through the current checker (lib/church-website-match.js). With --apply, each
// failure has its website and EVERY field harvested from it restored to the value it
// held the day before discovery (per-day baselines in --baseline-dir, one
// YYYY-MM-DD.json per UTC date = churches.json as of 00:00Z that day). The
// _website_searched stamp is kept and a REVERTED note is appended.
//
// Also re-checks Facebook pages recorded by the discovery slug-match since --since.
//
// Usage:
//   node scripts/recheck-discovered-websites.js --since 2026-11-16 \
//     --baseline-dir /tmp/webdisc-snap --out /tmp/recheck.json [--apply] [--cid CM-1122-WEBDISC]
const fs = require('fs');
const path = require('path');
const M = require('./lib/church-website-match.js');
const { fetchText } = require('./lib/site-fetch.js');
const { makeWriter } = require('./lib/format-preserving-write.js');

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const SINCE = arg('--since', '2026-11-16');
const BASE_DIR = arg('--baseline-dir', '');
const OUT = arg('--out', '');
const CID = arg('--cid', 'CM-1122-WEBDISC');
const APPLY = process.argv.includes('--apply');
const CONC = parseInt(arg('--concurrency', '8'), 10);
const TODAY = new Date().toISOString().slice(0, 10);
if (!BASE_DIR) { console.error('--baseline-dir is required'); process.exit(2); }

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const { data: d, write } = makeWriter(CHURCHES);

// Fields the site-fed lanes (social fill, profile fill, pastor extract, live-fetch
// verdicts) write from a church's website. Restored to baseline on a failure.
const HARVESTED = ['website', 'facebook', 'instagram', 'youtube', 'twitter', 'tiktok', 'x', 'phone', 'email', 'pastor', 'pastors', 'pastor_credentials', 'pastor_source', 'service_times', 'services', 'enrichment_sources', 'logo', 'logo_url', '_dead_site', '_site_timeout_strikes', '_social_attempted', '_pastor_attempted', '_profile_filled'];
const NESTED = { score_notes: null, engagement: ['researched_website'] };
// Keys that legitimately change for other reasons; never restored, reported only.
const UNTOUCHED = new Set(['enrichment_notes', '_website_searched', 'needs_review', '_hold_review', 'last_reviewed', 'full_review_at']);

const snapCache = new Map();
function baselineFor(date) {
  if (!snapCache.has(date)) {
    const f = path.join(BASE_DIR, `${date}.json`);
    snapCache.set(date, fs.existsSync(f) ? new Map(JSON.parse(fs.readFileSync(f, 'utf8')).churches.map(c => [c.id, c])) : null);
  }
  return snapCache.get(date);
}
const lastDated = (c, re) => { const m = String(c.enrichment_notes || '').match(re); return m ? m[m.length - 1].slice(1, 11) : ''; };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const clone = v => v === undefined ? undefined : JSON.parse(JSON.stringify(v));

function restore(c, b, keys) {
  const changed = [];
  for (const k of keys) {
    if (same(c[k], b[k])) continue;
    if (b[k] === undefined) delete c[k]; else c[k] = clone(b[k]);
    changed.push(k);
  }
  for (const [k, sub] of Object.entries(NESTED)) {
    const cur = c[k] || {}, base = b[k] || {};
    const subs = sub || [...new Set([...Object.keys(cur), ...Object.keys(base)])];
    for (const s of subs) {
      if (same(cur[s], base[s])) continue;
      c[k] = c[k] || {};
      if (base[s] === undefined) delete c[k][s]; else c[k][s] = clone(base[s]);
      changed.push(`${k}.${s}`);
    }
    if (b[k] === undefined && c[k] && !Object.keys(c[k]).length) delete c[k];
  }
  return changed;
}

async function pool(items, n, fn) {
  const out = new Array(items.length); let i = 0;
  await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const j = i++; out[j] = await fn(items[j], j); } }));
  return out;
}

(async () => {
  const assigned = M.buildAssignedDomains(d.churches);
  const discRe = /\[(\d{4}-\d{2}-\d{2})\] Website discovered via/g;
  const sites = d.churches.filter(c => c.website && c._website_searched >= SINCE && lastDated(c, discRe) >= SINCE);
  const fbRe = /\[(\d{4}-\d{2}-\d{2})\] Facebook page discovered via/g;
  const fbs = d.churches.filter(c => c.facebook && lastDated(c, fbRe) >= SINCE && !sites.includes(c));

  const fetchMemo = new Map();
  const memoFetch = u => { if (!fetchMemo.has(u)) fetchMemo.set(u, fetchText(u)); return fetchMemo.get(u); };
  const rows = await pool(sites, CONC, async c => {
    const v = await M.checkCandidate(c, c.website, { assigned, fetchText: memoFetch });
    return { id: c.id, name: c.name, city: M.cityOf(c), state: M.stateOf(c), website: c.website, ok: v.ok, reason: v.reason, segs: v.segs || [], others: (v.others || []).length, discovered: lastDated(c, discRe) };
  });
  const fbRows = fbs.map(c => {
    const m = String(c.facebook).match(/facebook\.com\/([^/?#]+)/i);
    const v = M.facebookSlugVerdict(c, m && m[1]);
    return { id: c.id, name: c.name, facebook: c.facebook, ok: v.ok, reason: v.reason, discovered: lastDated(c, fbRe) };
  });

  const byId = new Map(d.churches.map(c => [c.id, c]));
  const reverted = [], extraDiffs = [];
  for (const r of rows.filter(r => !r.ok)) {
    const c = byId.get(r.id), base = baselineFor(r.discovered);
    const b = base && base.get(r.id);
    if (!b) { r.revert = 'NO-BASELINE'; continue; }
    const before = clone(c);
    const changed = restore(c, b, HARVESTED);
    if (c.website === undefined) c.website = '';
    for (const k of new Set([...Object.keys(before), ...Object.keys(b)])) if (!UNTOUCHED.has(k) && !HARVESTED.includes(k) && !(k in NESTED) && !same(before[k], b[k])) extraDiffs.push(`${r.id}:${k}`);
    const note = `[${TODAY}] REVERTED: website ${M.regDomain(r.website) || r.website} failed the whole-token website check (${r.reason}); a domain shared with other churches or an unrelated organisation is not this church's site. Cleared it and the fields harvested from it (${changed.filter(x => x !== 'website').join(', ') || 'none'}); _website_searched kept. (${CID})`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    r.revert = changed;
    reverted.push(r.id);
    if (!APPLY) Object.assign(c, before); // dry run: undo in memory
    if (!APPLY) { for (const k of Object.keys(c)) if (!(k in before)) delete c[k]; }
  }
  const fbReverted = [];
  for (const r of fbRows.filter(r => !r.ok)) {
    const c = byId.get(r.id), base = baselineFor(r.discovered);
    const b = base && base.get(r.id);
    if (!b) { r.revert = 'NO-BASELINE'; continue; }
    if (same(c.facebook, b.facebook)) continue;
    if (APPLY) {
      if (b.facebook === undefined) delete c.facebook; else c.facebook = b.facebook;
      const note = `[${TODAY}] REVERTED: Facebook page ${r.facebook} came from a substring slug match (${r.reason}) and is not verified as this church's page. Cleared. (${CID})`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    }
    fbReverted.push(r.id);
  }
  if (APPLY && (reverted.length || fbReverted.length)) write(d);
  const summary = { since: SINCE, checked: rows.length, kept: rows.filter(r => r.ok).length, reverted: reverted.length, fb_checked: fbRows.length, fb_reverted: fbReverted.length, reasons: rows.reduce((a, r) => (a[r.reason] = (a[r.reason] || 0) + 1, a), {}), extra_diffs: extraDiffs, applied: APPLY };
  if (OUT) fs.writeFileSync(OUT, JSON.stringify({ summary, rows, fbRows }, null, 1));
  console.log(JSON.stringify(summary, null, 1));
})();
