#!/usr/bin/env node
'use strict';
/**
 * Apply a full-review patch to churches.json (Chaps ticket, 2026-11-08).
 *
 * BUILT, NOT RUN LIVE. The live apply waits for Adam's GO.
 *
 * Applies:
 *   - every change with gate "auto" in the patch, and
 *   - every HOLD row in data/full-review/hold-queue.json that Chaps QA
 *     marked qa_status "approved" (rows from a dry run are never applied).
 * Skips a change whose `old` no longer matches the live value (stale patch).
 * Never deletes an entry or a value: cleared values are kept verbatim in
 * enrichment_notes; duplicates are only queued for scripts/merge-duplicate-churches.js.
 *
 * Modes:
 *   (default)  PREVIEW — print what would change; writes nothing.
 *   --apply    write churches.json (format-preserving), stamp full_review_at,
 *              regenerate pages (generate-church-pages.js), run the existing
 *              consistency check (scripts/check-consistency.js) with the same
 *              mechanical self-heal as pastor-refine-local.sh; a failure restores
 *              churches.json from git and exits non-zero.
 *   --ship     after --apply, commit + push via scripts/full-review-ship.sh, the
 *              path-scoped route (refuses ~/bible-reading-plan-bot; see DEPLOY-DOCTRINE.md).
 *   --accept-dry-run-patch   allow applying a patch built with --dry-run (its
 *              auto changes only; dry-run HOLD rows still never apply).
 *
 * Usage:
 *   node scripts/apply-full-review-patch.js --patch docs/data/full-review/rounds/<round>/review-patch.json [--apply [--ship]]
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { makeWriter } = require('./lib/format-preserving-write.js');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const ROOT = path.join(__dirname, '..');
const CHURCHES = process.env.FULL_REVIEW_CHURCHES_PATH || path.join(ROOT, 'docs', 'data', 'churches.json');
const PATCH = opt('--patch', null);
const QUEUE = opt('--holds', path.join(ROOT, 'data', 'full-review', 'hold-queue.json'));
const STATS = opt('--stats', path.join(ROOT, 'docs', 'data', 'full-review-stats.json'));
const APPLY = args.includes('--apply');
const SHIP = args.includes('--ship');
const ACCEPT_DRY = args.includes('--accept-dry-run-patch');
// Local (Eastern) calendar date, not UTC — a 10 pm round must not stamp tomorrow.
const TODAY = new Date().toLocaleDateString('en-CA');
if (!PATCH) { console.error('usage: --patch <review-patch.json> [--apply [--ship]]'); process.exit(2); }

const patch = JSON.parse(fs.readFileSync(PATCH, 'utf8'));
if (patch.dry_run && !ACCEPT_DRY) {
  console.error(`REFUSED: ${patch.round} was built as a DRY RUN. Re-run the round live, or pass --accept-dry-run-patch after Adam's GO.`);
  process.exit(3);
}
if (patch.applied && APPLY) { console.error(`REFUSED: ${patch.round} already applied at ${patch.applied_at}.`); process.exit(3); }
let queue = { holds: [] };
try { queue = JSON.parse(fs.readFileSync(QUEUE, 'utf8')); } catch (_) { }
const approved = new Map((queue.holds || [])
  .filter(h => h.round === patch.round && h.qa_status === 'approved' && !h.dry_run && h.kind === 'change')
  .map(h => [h.hold_id, h]));
const approvedFlags = (queue.holds || []).filter(h => h.round === patch.round && h.qa_status === 'approved' && !h.dry_run && h.kind === 'flag');

const { data, write } = makeWriter(CHURCHES);
const byId = new Map(data.churches.filter(c => c && c.id).map(c => [c.id, c]));
const getP = (o, p) => p.split('.').reduce((a, k) => (a == null ? undefined : a[k]), o);
const setP = (o, p, v) => { const ks = p.split('.'); let a = o; for (const k of ks.slice(0, -1)) a = a[k] = (a[k] && typeof a[k] === 'object') ? a[k] : {}; a[ks[ks.length - 1]] = v; };
const blank = v => v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length);
const same = (a, b) => (blank(a) && blank(b)) || JSON.stringify(a) === JSON.stringify(b);
const note = (c, s) => { c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + s : s; };
const short = v => (typeof v === 'string' ? v : JSON.stringify(v ?? null)).slice(0, 120);

const log = { round: patch.round, mode: APPLY ? 'apply' : 'preview', at: new Date().toISOString(), applied: [], skipped: [], flags_queued: [] };
for (const r of patch.churches || []) {
  const c = byId.get(r.id);
  if (!c) { log.skipped.push({ church_id: r.id, reason: 'not in churches.json' }); continue; }
  let touched = 0;
  for (const ch of r.changes || []) {
    const go = ch.gate === 'auto' || approved.has(ch.change_id);
    if (!go) continue;
    if (!ch.evidence || !ch.evidence.quote || !ch.evidence.url) { log.skipped.push({ change_id: ch.change_id, reason: 'no evidence' }); continue; }
    const cur = getP(c, ch.field);
    if (ch.op !== 'confirm' && !same(cur, ch.old)) { log.skipped.push({ change_id: ch.change_id, reason: `stale: live value ${short(cur)} != patch old ${short(ch.old)}` }); continue; }
    // Notes render on public pages: keep the URL, redact contact details of
    // private individuals that a quote may carry (the patch keeps the verbatim quote).
    const redact = q => String(q).replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, '[email]').replace(/\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}/g, '[phone]');
    const cite = `"${redact(ch.evidence.quote).slice(0, 160)}" (${ch.evidence.url})` + (ch.rule ? `; rule: "${ch.rule.text}" (${ch.rule.url})` : '');
    if (ch.op === 'research') {
      // Identity problem approved by QA: keep every value, flag the record for research.
      c._identity_hold = TODAY; c.needs_review = true;
      note(c, `[${TODAY}] Full review ${patch.round}: stored website appears to belong to a different church — ${cite}. Values kept; record held for research.`);
    } else if (ch.op === 'clear') {
      setP(c, ch.field, Array.isArray(cur) ? [] : '');
      note(c, `[${TODAY}] Full review ${patch.round}: cleared ${ch.field} (was ${short(cur)}) — ${ch.reason}. Evidence: ${cite}.`);
    } else {
      setP(c, ch.field, ch.new);
      for (const [k, v] of Object.entries(ch.also_sets || {})) setP(c, k, v);
      if (ch.field === 'address') c._geocode_stale = TODAY;
      if (ch.op !== 'confirm') note(c, `[${TODAY}] Full review ${patch.round}: ${ch.field} ${short(ch.old)} -> ${short(ch.new)}${approved.has(ch.change_id) ? ' (QA-approved hold)' : ''}. Evidence: ${cite}.`);
    }
    if (ch.evidence.url && /^https?:/.test(ch.evidence.url)) {
      c.enrichment_sources = Array.isArray(c.enrichment_sources) ? c.enrichment_sources : [];
      if (!c.enrichment_sources.includes(ch.evidence.url)) c.enrichment_sources.push(ch.evidence.url);
    }
    log.applied.push({ change_id: ch.change_id, church_id: r.id, field: ch.field, old: ch.old, new: ch.new, via: ch.gate === 'auto' ? 'auto' : 'qa-approved' });
    touched++;
  }
  const pendingHere = (queue.holds || []).some(h => h.church_id === r.id && h.round === patch.round && h.qa_status === 'pending' && !h.dry_run);
  c.full_review_at = TODAY;
  c.full_review_round = patch.round;
  if (pendingHere) { c.full_review_hold = TODAY; c.needs_review = true; } else delete c.full_review_hold;
  if (touched) c.last_reviewed = TODAY;
}
for (const f of approvedFlags) log.flags_queued.push({ church_id: f.church_id, flag: f.flag, other_id: f.other_id, action: f.action });

console.log(`${log.mode.toUpperCase()} ${patch.round}: ${log.applied.length} change(s) (${log.applied.filter(a => a.via === 'auto').length} auto, ${log.applied.filter(a => a.via !== 'auto').length} QA-approved), ${log.skipped.length} skipped, ${log.flags_queued.length} approved flag(s) queued`);
for (const a of log.applied) console.log(`  ${a.via.padEnd(11)} ${a.church_id} ${a.field}: ${short(a.old)} -> ${short(a.new)}`);
for (const s of log.skipped) console.log(`  SKIP ${s.change_id || s.church_id}: ${s.reason}`);
if (!APPLY) { console.log('PREVIEW only — nothing written. Re-run with --apply after Adam\'s GO.'); process.exit(0); }

// ── write + regen + consistency ──────────────────────────────────────────────
data.directory_updated = TODAY;
write(data);
const run = (cmd, a) => execFileSync(cmd, a, { cwd: ROOT, stdio: 'inherit' });
const restore = why => {
  try { execFileSync('git', ['checkout', '--', path.relative(ROOT, CHURCHES)], { cwd: ROOT }); } catch (_) { }
  console.error(`ABORT: ${why} — churches.json restored from git; nothing shipped.`); process.exit(1);
};
try { run('node', ['generate-church-pages.js']); } catch (_) { restore('page regeneration failed'); }
try { run('node', ['scripts/check-consistency.js']); } catch (_) {
  console.log('consistency FAILED — mechanical self-heal (sitemap + index), same as pastor-refine-local.sh');
  try { run('node', ['scripts/build-sitemap-churches.js']); run('node', ['scripts/build-church-index.js']); run('node', ['scripts/check-consistency.js']); }
  catch (_) { restore('consistency check failed after self-heal'); }
}
if (approvedFlags.length) {
  const AF = path.join(ROOT, 'data', 'full-review', 'approved-duplicates.json');
  let j = { note: 'QA-approved duplicate / wrong-church flags from full review. Feed to scripts/merge-duplicate-churches.js; never delete records.', items: [] };
  try { j = JSON.parse(fs.readFileSync(AF, 'utf8')); } catch (_) { }
  j.items.push(...log.flags_queued.map(x => ({ ...x, round: patch.round, at: TODAY })));
  fs.writeFileSync(AF, JSON.stringify(j, null, 1));
}
patch.applied = true; patch.applied_at = new Date().toISOString();
fs.writeFileSync(PATCH, JSON.stringify(patch, null, 1));
fs.writeFileSync(path.join(path.dirname(PATCH), 'applied.json'), JSON.stringify(log, null, 1));
for (const h of queue.holds || []) if (approved.has(h.hold_id) && log.applied.some(a => a.change_id === h.hold_id)) h.qa_status = 'applied';
fs.writeFileSync(QUEUE, JSON.stringify(queue, null, 1));
try {
  const s = JSON.parse(fs.readFileSync(STATS, 'utf8'));
  const row = (s.series || []).find(x => x.round === patch.round);
  if (row) { row.applied = log.applied.filter(a => a.via === 'auto').length; row.applied_holds = log.applied.filter(a => a.via !== 'auto').length; row.applied_at = TODAY; }
  fs.writeFileSync(STATS, JSON.stringify(s, null, 1));
} catch (_) { }
console.log(`APPLIED ${patch.round}: churches.json written, pages regenerated, consistency GREEN.`);

if (SHIP) {
  try { run('/bin/bash', ['scripts/full-review-ship.sh', `Directory full review ${patch.round}: ${log.applied.length} evidence-cited change(s)`]); }
  catch (_) { console.error('SHIP failed — see full-review-ship.sh output; the local commit (if any) is kept for salvage.'); process.exit(1); }
}
