#!/usr/bin/env node
'use strict';
// denominations-grind-promote.js <id> — turn a body's verbatim-valid local-model
// proposals into data/denominations/<id>.json (CCW-1119-DIR3 grind lane).
//
// Only proposals with validated=true are copied, and each one is re-checked here
// against the body-only snapshot (same check the builder runs). The builder's
// written rules then decide every grade; nothing here assigns a grade. Fewer than
// 5 graded categories shows "Limited evidence" on the page, never a color.
// Exit 0 = written and at least one category grades; 3 = nothing gradeable (hold).
const fs = require('fs');
const path = require('path');
const D = require('./lib/denominations.js');

const id = process.argv[2];
if (!id) { console.error('usage: denominations-grind-promote.js <id>'); process.exit(2); }
const amap = D.loadAliasMap();
const body = amap.bodies.get(id);
if (!body) { console.error(`${id}: not in alias map`); process.exit(2); }
const out = path.join(D.DATA_DIR, `${id}.json`);
if (fs.existsSync(out)) { console.error(`${id}: already graded (${out}); refusing to overwrite`); process.exit(2); }
const props = JSON.parse(fs.readFileSync(path.join(D.DATA_DIR, 'proposals', `${id}.json`), 'utf8')).proposals;
const sites = JSON.parse(fs.readFileSync(path.join(D.DATA_DIR, 'sites', 'official-sites.json'), 'utf8'));
const v = sites.verified[id];
const site = v && v.ok ? v.url : null;
const siteHost = site ? new URL(site).hostname.replace(/^www\./, '') : null;

const evidence = [];
const seen = new Map();
for (const p of props.filter(x => x.validated)) {
  const src = D.loadSource(id, p.source);
  if (!src.sha_ok || !D.quoteInSource(p.quote, src.text)) continue;
  // Official-only: the snapshot must be on the verified official domain.
  const h = new URL(src.meta.final_url || src.meta.url).hostname.replace(/^www\./, '');
  if (!siteHost || !(h === siteHost || h.endsWith('.' + siteHost))) continue;
  const key = D.nrm(p.quote);
  if (seen.has(key)) { const e = seen.get(key); if (!e.supports.includes(p.category)) e.supports.push(p.category); continue; }
  const e = { id: `${id}-${p.source}-${evidence.length + 1}`, source: p.source, url: src.meta.url, quote: p.quote.trim(),
    supports: [p.category], model: p.model || null };
  seen.set(key, e); evidence.push(e);
}
// Aliases: the alias-map body's labels, minus any another page already owns.
const others = D.aliasIndex(D.loadDenominations());
const aliases = [...new Set([body.short_name, body.name, ...(body.aliases || [])])].filter(a => { const o = others.get(D.aliasKey(a)); return !o || o === id; });
const doc = { id, name: body.name, short_name: body.short_name, aliases, official_site: site,
  source_policy: `Official ${body.short_name} sources only (${siteHost}). Quotes were proposed by a local model (LM Studio, no cloud) and each one is checked word for word against the main body of a captured snapshot of the official page; grades come only from the published rules.`,
  graded_by: 'denomination-grind (local model + deterministic rules)', evidence };
const sc = D.scoreDenomination(doc, D.buildLedger(doc));
if (!evidence.length || sc.graded_count === 0) {
  console.error(`${id}: ${evidence.length} verbatim quotes, 0 categories grade under the published rules`);
  process.exit(3);
}
fs.writeFileSync(out, JSON.stringify(doc, null, 1) + '\n');
console.log(`${id}: wrote ${evidence.length} evidence rows; graded ${sc.graded_count}/10; overall=${sc.overall_grade}; because=${sc.because.join(',')}`);
