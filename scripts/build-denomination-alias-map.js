#!/usr/bin/env node
'use strict';
// build-denomination-alias-map.js — classify every distinct churches.json
// `denomination` label with the deterministic rules and write:
//
//   data/denominations/aliases/alias-map.json   canonical bodies (existing schema:
//        id, name, short_name, aliases[]) + per-label classification + generic
//        families (graded_page:false) + unresolved list
//   data/denominations/aliases/alias-coverage.json / .md   counts, body ranking,
//        unresolved list, local-model agreement
//
//   --check   regenerate in memory; exit 1 if the committed files are stale, a
//             label is missing, or an alias maps to two bodies.
//
// Read-only on churches.json. Adds no public page: docs/ is never written.
// The local-model proposals (alias-proposals.json) are compared, never obeyed.
const fs = require('fs');
const path = require('path');
const R = require('./lib/denomination-alias-rules.js');
const D = require('./lib/denominations.js');

const ROOT = path.join(__dirname, '..');
const DIR = path.join(ROOT, 'data', 'denominations', 'aliases');
const MAP = path.join(DIR, 'alias-map.json');
const COV = path.join(DIR, 'alias-coverage.json');
const MD = path.join(DIR, 'alias-coverage.md');
const PROPOSALS = path.join(DIR, 'alias-proposals.json');
const CHECK = process.argv.includes('--check');
// Phase 2 order from the brief (CCW-1119-DIR2).
const PHASE2_FIRST = ['sbc', 'bgav', 'sbcv', 'umc', 'gmc', 'ame', 'pca', 'opc', 'arp', 'acna'];

function labelCounts() {
  const raw = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'data', 'churches.json'), 'utf8'));
  const cs = Array.isArray(raw) ? raw : raw.churches;
  const m = new Map();
  for (const c of cs) { const k = c.denomination == null ? '' : String(c.denomination); m.set(k, (m.get(k) || 0) + 1); }
  return { total: cs.length, labels: [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])) };
}

function build() {
  const { total, labels } = labelCounts();
  const pageDenoms = D.loadDenominations();
  const pageIdx = D.aliasIndex(pageDenoms);
  const classified = labels.map(([label, count]) => {
    const r = R.classifyLabel(label);
    // A body that already has a page owns its labels; the rules must agree.
    const pageId = D.normalizeDenomination(label, pageIdx);
    if (pageId && !(r.status === 'body' && r.id === pageId)) r.conflict = `page alias says ${pageId}`;
    return { label, count, ...r };
  });
  const bodies = R.BODIES.map(b => {
    const rows = classified.filter(c => c.status === 'body' && c.id === b.id);
    const page = pageDenoms.find(d => d.id === b.id);
    return { id: b.id, name: b.name, short_name: b.short_name, family: b.family,
      aliases: [...new Set(rows.map(r => r.label))],
      church_count: rows.reduce((n, r) => n + r.count, 0),
      graded_page: !!page, page: page ? `/denominations/${b.id}.html` : null };
  }).filter(b => b.church_count > 0)
    .sort((a, b) => b.church_count - a.church_count || a.id.localeCompare(b.id));
  // Same alias normalization the page builder uses: one alias, one body.
  D.aliasIndex(bodies.map(b => ({ id: b.id, aliases: b.aliases })));
  const generic = {};
  for (const c of classified.filter(c => c.status === 'generic')) {
    const g = generic[c.family] || (generic[c.family] = { family: c.family, graded_page: false, labels: [], church_count: 0 });
    g.labels.push(c.label); g.church_count += c.count;
  }
  const unresolved = classified.filter(c => c.status === 'unresolved')
    .map(c => ({ label: c.label, count: c.count, reason: c.reason, candidates: c.candidates }));
  const sum = st => classified.filter(c => c.status === st);
  const counts = {
    churches: total, labels: labels.length,
    mapped: { labels: sum('body').length, churches: sum('body').reduce((n, c) => n + c.count, 0) },
    generic: { labels: sum('generic').length, churches: sum('generic').reduce((n, c) => n + c.count, 0) },
    unresolved: { labels: sum('unresolved').length, churches: sum('unresolved').reduce((n, c) => n + c.count, 0) },
    bodies: bodies.length,
  };
  // Local-model comparison (report only).
  let model = null;
  if (fs.existsSync(PROPOSALS)) {
    const p = JSON.parse(fs.readFileSync(PROPOSALS, 'utf8'));
    const prop = new Map(p.proposals.map(x => [x.label, x.proposed]));
    const ruleAns = c => c.status === 'body' ? c.id : c.status;
    let agree = 0, none = 0; const disagree = [];
    for (const c of classified) {
      const v = prop.get(c.label);
      if (v == null) { none++; continue; }
      if (v === ruleAns(c)) agree++; else disagree.push({ label: c.label, count: c.count, rule: ruleAns(c), model: v });
    }
    model = { model: p.model, generated_at: p.generated_at, agree, disagree: disagree.length, no_proposal: none,
      disagreements: disagree.sort((a, b) => b.count - a.count) };
  }
  const phase2 = PHASE2_FIRST.map(id => { const b = bodies.find(x => x.id === id); return { id, church_count: b ? b.church_count : 0 }; });
  const mapDoc = {
    _note: 'Generated by scripts/build-denomination-alias-map.js from scripts/lib/denomination-alias-rules.js. Do not hand-edit; change the rules and rebuild. Generic families never get a graded page. Unresolved labels stay unmapped.',
    schema: 1, bodies, generic: Object.values(generic).sort((a, b) => b.church_count - a.church_count),
    labels: classified.map(({ label, count, status, id, family, reason, conference, presbytery, diocese, convention, region, conflict }) =>
      Object.fromEntries(Object.entries({ label, count, status, id, family, conference, presbytery, diocese, convention, region, reason, conflict }).filter(([, v]) => v !== undefined))),
  };
  const covDoc = { counts, phase2_order: phase2, ranking: bodies.map((b, i) => ({ rank: i + 1, id: b.id, short_name: b.short_name, church_count: b.church_count, labels: b.aliases.length })),
    unresolved, model };
  return { mapDoc, covDoc, classified };
}

function md({ counts, ranking, unresolved, model, phase2_order }) {
  const L = [];
  L.push('# Denomination alias map: coverage report', '', 'Generated by `scripts/build-denomination-alias-map.js`. Rules decide; the local model only proposes.', '');
  L.push(`- Churches: ${counts.churches} · distinct labels: ${counts.labels}`);
  L.push(`- Mapped to a body: ${counts.mapped.labels} labels / ${counts.mapped.churches} churches (${counts.bodies} bodies)`);
  L.push(`- Generic (no graded page): ${counts.generic.labels} labels / ${counts.generic.churches} churches`);
  L.push(`- Unresolved (left unmapped): ${counts.unresolved.labels} labels / ${counts.unresolved.churches} churches`);
  if (model) L.push(`- Local model ${model.model}: agrees with the rules on ${model.agree}, differs on ${model.disagree}, no proposal on ${model.no_proposal}`);
  L.push('', '## Phase 2 order', '', phase2_order.map(p => `${p.id} (${p.church_count})`).join(' · '), '');
  L.push('## Bodies by church count', '', '| # | id | body | churches | labels |', '|---|---|---|---|---|');
  for (const r of ranking) L.push(`| ${r.rank} | ${r.id} | ${r.short_name} | ${r.church_count} | ${r.labels} |`);
  L.push('', '## Unresolved labels', '', '| label | churches | reason | candidates |', '|---|---|---|---|');
  for (const u of unresolved) L.push(`| ${u.label.replace(/\|/g, '\\|') || '(empty)'} | ${u.count} | ${u.reason} | ${(u.candidates || []).join(', ')} |`);
  if (model && model.disagreements.length) {
    L.push('', '## Where the local model differs (rules win)', '', '| label | churches | rule | model |', '|---|---|---|---|');
    for (const d of model.disagreements) L.push(`| ${d.label.replace(/\|/g, '\\|') || '(empty)'} | ${d.count} | ${d.rule} | ${d.model} |`);
  }
  return L.join('\n') + '\n';
}

const { mapDoc, covDoc, classified } = build();
const errors = classified.filter(c => c.conflict).map(c => `"${c.label}": ${c.conflict}`);
const files = [[MAP, JSON.stringify(mapDoc, null, 1) + '\n'], [COV, JSON.stringify(covDoc, null, 1) + '\n'], [MD, md(covDoc)]];
if (errors.length) { console.error('alias map errors:\n  ' + errors.join('\n  ')); process.exit(1); }
if (CHECK) {
  const stale = files.filter(([f, s]) => !fs.existsSync(f) || fs.readFileSync(f, 'utf8') !== s).map(([f]) => path.relative(ROOT, f));
  if (stale.length) { console.error('stale (rebuild with node scripts/build-denomination-alias-map.js): ' + stale.join(', ')); process.exit(1); }
  console.log(`alias map OK: ${covDoc.counts.labels} labels, ${covDoc.counts.mapped.labels} mapped, ${covDoc.counts.generic.labels} generic, ${covDoc.counts.unresolved.labels} unresolved`);
} else {
  fs.mkdirSync(DIR, { recursive: true });
  for (const [f, s] of files) fs.writeFileSync(f, s);
  console.log(JSON.stringify(covDoc.counts));
}
