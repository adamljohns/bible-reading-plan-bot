#!/usr/bin/env node
/* verse-study-status.js — where the deep-study backlog actually stands.
 *
 * The working list is the 71 verses in the memorize app, because those are the
 * ones Adam's people are carrying around in their heads. A verse counts as done
 * only when it is approved AND passes bin/verse-study-gate.js — a draft with
 * unwritten slots is not progress, and reporting it as progress is how a backlog
 * quietly lies to you.
 *
 * Usage: node bin/verse-study-status.js [--verbose]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { slugFor } = require('./verse-study-scaffold.js');
const { checkPage } = require('./verse-study-gate.js');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DRAFTS = path.join(DOCS, 'drafts', 'verse');

function memorizeRefs() {
  const fp = path.join(DOCS, 'data', 'memory-packs.json');
  const packs = JSON.parse(fs.readFileSync(fp, 'utf8')).packs || [];
  const seen = new Set();
  const out = [];
  packs.forEach((p) => p.verses.forEach((v) => {
    if (!seen.has(v.ref)) { seen.add(v.ref); out.push({ ref: v.ref, pack: p.name }); }
  }));
  return out;
}

function classify(ref) {
  const slug = slugFor(ref);
  const live = path.join(DOCS, 'verse', slug);
  const draft = path.join(DRAFTS, slug);
  // A published deep study wins. A short landing page does not — it is what the
  // study will replace, so a draft in flight is the more useful thing to report.
  if (fs.existsSync(live) && /<meta name="verse-ref"/.test(fs.readFileSync(live, 'utf8'))) {
    const r = checkPage(live);
    return r.fails.length
      ? { state: 'published-FAILING', detail: r.fails[0], words: r.words }
      : { state: 'published', words: r.words };
  }
  const hasLanding = fs.existsSync(live);
  if (fs.existsSync(draft)) {
    const note = hasLanding ? ' · replaces existing landing page' : '';
    const cls = (s) => ({ ...s, detail: (s.detail || '') + note });
    return cls(draftState(draft));
  }
  if (hasLanding) return { state: 'landing-page-only' };
  return { state: 'not-started' };
}

function draftState(draft) {
  {
    const html = fs.readFileSync(draft, 'utf8');
    const todos = (html.match(/class="vs-todo"/g) || []).length;
    const r = checkPage(draft);
    return todos
      ? { state: 'draft-scaffolded', detail: `${todos} slots unwritten`, words: r.words }
      : { state: 'draft-written', detail: r.fails.length ? `gate: ${r.fails[0]}` : 'gate clean — ready for review', words: r.words };
  }
}

function main() {
  const verbose = process.argv.includes('--verbose');
  const refs = memorizeRefs();
  const rows = refs.map((r) => ({ ...r, ...classify(r.ref) }));
  const order = ['published', 'published-FAILING', 'draft-written', 'draft-scaffolded', 'landing-page-only', 'not-started'];
  const counts = {};
  rows.forEach((r) => { counts[r.state] = (counts[r.state] || 0) + 1; });

  // --next / --json exist so the unattended writing loop
  // (~/Scripts/verse-study-loop.sh) can pick the next verse without scraping
  // this report's prose. --next prints one ref and nothing else; it exits 3
  // when the backlog is empty, which is the loop's stop signal.
  if (process.argv.includes('--json')) {
    console.log(JSON.stringify({ total: refs.length, counts, rows }, null, 1));
    return;
  }
  if (process.argv.includes('--next')) {
    const n = rows.find((r) => r.state === 'draft-scaffolded' || r.state === 'not-started');
    if (!n) { console.error('backlog empty — every memorize verse is written'); process.exit(3); }
    console.log(n.ref);
    return;
  }

  console.log(`Deep verse studies — memorize backlog (${refs.length} verses)\n`);
  order.forEach((s) => {
    if (!counts[s]) return;
    console.log(`  ${String(counts[s]).padStart(3)}  ${s}`);
  });
  const done = counts.published || 0;
  console.log(`\n  Done (approved + gate-passing): ${done}/${refs.length}`);
  if (counts['published-FAILING']) {
    console.log(`  ${counts['published-FAILING']} published page(s) FAILING the gate — fix these before writing anything new:`);
    rows.filter((r) => r.state === 'published-FAILING').forEach((r) => console.log(`     ${r.ref} — ${r.detail}`));
  }
  if (verbose) {
    console.log('');
    order.forEach((s) => {
      rows.filter((r) => r.state === s).forEach((r) => {
        console.log(`  ${s.padEnd(20)} ${r.ref.padEnd(22)} ${r.words ? r.words + 'w ' : ''}${r.detail || ''}`);
      });
    });
  } else {
    const next = rows.filter((r) => r.state === 'not-started' || r.state === 'draft-scaffolded').slice(0, 5);
    if (next.length) {
      console.log('\n  Next up:');
      next.forEach((r) => console.log(`     ${r.ref}  (${r.pack})`));
    }
  }
}

if (require.main === module) main();
