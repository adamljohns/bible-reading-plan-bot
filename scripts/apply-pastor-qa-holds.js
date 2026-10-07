#!/usr/bin/env node
/**
 * Put already-PUBLISHED lead-pastor names back on HOLD after QA.
 *
 * merge-pastor-enrichments.js holds a typically-female lead name before it is
 * ever written. A name that slipped past an older guard (or arrived by a harvest
 * replay) is already on the page; this moves it into the same held state the
 * guard would have produced: `pastor` / `pastors[]` cleared, the exact published
 * values and their source kept verbatim in enrichment_notes, `_hold_review`
 * stamped so the church leaves the automated pools, `needs_review` set for the
 * Principal's rubric review. Nothing is discarded and nothing is invented.
 *
 * An entry with "action": "clear" is for a name that is not the church's pastor
 * at all (a parish administrator, a pantry coordinator, a job title). It is
 * cleared the same way but NOT stamped _hold_review, so the grind's pastor lanes
 * can go and find the real one from the church's own site.
 *
 * Three more actions carry a desk QA pass (2026-10-06 round 2):
 *   "set"   — replace the published `pastor` with `value`, read verbatim at `source`.
 *   "stamp" — keep the published value, stamp `_hold_review` + `needs_review` (the
 *             desk could not re-verify it, or the record has a wider problem).
 *   "text"  — replace the exact substring `find` with `replace` in the string at
 *             dotted path `field` (e.g. "score_notes.leadership"); SKIPs unless
 *             `find` occurs exactly once.
 *   "fill"  — write `value` at dotted path `field` only when it is missing or "";
 *             SKIPs any field that already holds a value (2026-10-07 round 3).
 *   "annotate" — keep the published pastor and write `pastor_role_annotation`
 *             {role, source, source_type, quote, verified}: the role exactly as the
 *             church site or denominational roster states it (Principal ruling
 *             2026-10-07: female-named leads are annotated, not suppressed).
 *
 * Acts only when the record's current `pastor` still equals the held name, so a
 * stale holds file can never clear a name someone has since corrected. ("text"
 * rows may omit `pastor`; their guard is the exact-once `find`.)
 *
 * NEVER run while the grind holds /tmp/directory-grind-session.lock or the
 * round lock — the grind owns churches.json while it runs.
 *
 * Report-first; --apply writes. Usage:
 *   node scripts/apply-pastor-qa-holds.js --holds scripts/qa/pastor-holds-2026-10-06.json [--apply]
 */
const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const APPLY = args.includes('--apply');
const HOLDS = opt('--holds', '');
if (!HOLDS) { console.error('--holds <file> required'); process.exit(1); }
if (APPLY && fs.existsSync('/tmp/directory-grind-session.lock')) {
  console.error('REFUSING: /tmp/directory-grind-session.lock exists — the grind owns churches.json. Re-run when the session ends.');
  process.exit(2);
}

const TODAY = new Date().toISOString().slice(0, 10);
const holds = JSON.parse(fs.readFileSync(HOLDS, 'utf8'));
const { data: d, write } = makeWriter(path.join(__dirname, '..', 'docs/data/churches.json'));
const byId = new Map(d.churches.map(c => [String(c.id), c]));

let held = 0;
const getPath = (o, f) => f.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
const setPath = (o, f, v) => { const ks = f.split('.'); const last = ks.pop(); ks.reduce((a, k) => a[k], o)[last] = v; };
const addNote = (c, note) => { c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note; };
for (const h of holds) {
  const c = byId.get(String(h.id));
  if (!c) { console.log(`SKIP ${h.id} — id not found`); continue; }
  if (h.pastor !== undefined && String(c.pastor || '').trim() !== h.pastor) { console.log(`SKIP ${h.id} — pastor is now "${c.pastor || ''}", not "${h.pastor}"`); continue; }
  if (h.action === 'text') {
    const cur = getPath(c, h.field);
    if (typeof cur === 'string' && h.replace && h.replace.includes(h.find) && cur.includes(h.replace)) { console.log(`SKIP ${h.id} — "${h.field}" already holds the replacement`); continue; }
    const n = typeof cur === 'string' ? cur.split(h.find).length - 1 : 0;
    if (n !== 1) { console.log(`SKIP ${h.id} — "${h.field}" holds the target text ${n} time(s), expected 1`); continue; }
    console.log(`TEXT  ${h.id} — ${h.field}: "${h.find}" → "${h.replace}"`);
    if (!APPLY) continue;
    setPath(c, h.field, cur.replace(h.find, h.replace));
    addNote(c, `[${TODAY}] QA text fix (${h.field}): "${h.find}" → "${h.replace}". Source: ${h.source}. ${h.evidence || ''}`.trim());
    held++; continue;
  }
  if (h.action === 'fill') {
    const cur = getPath(c, h.field);
    if (cur != null && cur !== '') { console.log(`SKIP ${h.id} — "${h.field}" already holds a value, fill only writes blanks`); continue; }
    if (h.field.includes('.') && getPath(c, h.field.split('.').slice(0, -1).join('.')) == null) { console.log(`SKIP ${h.id} — parent of "${h.field}" missing`); continue; }
    console.log(`FILL  ${h.id} — ${h.field}: "${h.value}"`);
    if (!APPLY) continue;
    setPath(c, h.field, h.value);
    addNote(c, `[${TODAY}] QA fill (${h.field}): "${h.value}". Source: ${h.source}. ${h.evidence || ''}`.trim());
    held++; continue;
  }
  if (h.action === 'annotate') {
    const a = h.annotation || {};
    if (!a.role || !a.source || !a.quote) { console.log(`SKIP ${h.id} — annotation needs role, source and quote`); continue; }
    const cur = c.pastor_role_annotation;
    if (cur && cur.role === a.role && cur.source === a.source) { console.log(`SKIP ${h.id} — already annotated`); continue; }
    console.log(`NOTE  ${h.id} — "${c.pastor}" role "${a.role}" (${a.source_type || 'site'})`);
    if (!APPLY) continue;
    c.pastor_role_annotation = { role: a.role, source: a.source, source_type: a.source_type || 'site', quote: a.quote, verified: a.verified || TODAY };
    addNote(c, `[${TODAY}] Pastor-role annotation: "${c.pastor}" listed as "${a.role}", verbatim at ${a.source}. ${h.evidence || ''}`.trim());
    held++; continue;
  }
  if (h.action === 'set') {
    console.log(`SET   ${h.id} — "${h.pastor}" → "${h.value}"`);
    if (!APPLY) continue;
    c.pastor = h.value;
    if (Array.isArray(c.pastors) && c.pastors[0] && c.pastors[0].name === h.pastor) c.pastors[0].name = h.value;
    addNote(c, `[${TODAY}] QA set: published pastor "${h.pastor}" → "${h.value}" (${h.role || 'pastor'}), verbatim at ${h.source}. ${h.evidence || ''}`.trim());
    held++; continue;
  }
  if (h.action === 'stamp') {
    if (c._hold_review) { console.log(`SKIP ${h.id} — already on hold since ${c._hold_review}`); continue; }
    console.log(`STAMP ${h.id} — "${h.pastor || c.pastor || ''}" kept, _hold_review`);
    if (!APPLY) continue;
    addNote(c, `[${TODAY}] QA hold: ${h.reason} Source: ${h.source}. ${h.evidence || ''}`.trim());
    c.needs_review = true;
    c._hold_review = TODAY;
    held++; continue;
  }
  if (h.action && h.action !== 'hold' && h.action !== 'clear') { console.log(`SKIP ${h.id} — unknown action "${h.action}"`); continue; }
  const roster = Array.isArray(c.pastors) && c.pastors.length ? ` Published roster was: ${JSON.stringify(c.pastors)}.` : '';
  const clear = h.action === 'clear';
  const note = clear
    ? `[${TODAY}] QA clear: published pastor "${h.pastor}" is not this church's pastor — the source lists them as ${h.role}. Removed from page (kept here); pastor left for re-research. Source: ${h.source}. ${h.evidence || ''}${roster}`.trim()
    : `[${TODAY}] QA hold: published lead-pastor "${h.pastor}" has a typically-female first name and was never rubric-reviewed — moved back to HOLD for manual MOOP-rubric review (name removed from page, kept here). Source: ${h.source}. ${h.evidence}${roster}`;
  console.log(`${clear ? 'CLEAR' : 'HOLD '} ${h.id} — "${h.pastor}"${roster ? ' (+roster)' : ''}`);
  if (!APPLY) continue;
  c.pastor = '';
  delete c.pastors;
  addNote(c, note);
  c.needs_review = true;
  if (!clear) c._hold_review = TODAY;
  held++;
}
if (APPLY) { write(d); console.log(`applied ${held} correction(s) — now rebuild pages/indexes and run check-consistency.js`); }
else console.log('(report only — pass --apply to write)');
