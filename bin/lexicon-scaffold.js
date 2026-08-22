#!/usr/bin/env node
/* lexicon-scaffold.js — build a compact, verified brief for a Strong's code.
 *
 * Written after preacher-john hit context overflow twice on the lexicon repair.
 * The cause was the task shape, not the agent: he was told to read a 12KB
 * exemplar page and work from it, inside an already-loaded session. Reading a
 * few lexicon pages in a tool loop is enough to blow the window.
 *
 * So this does for the lexicon what verse-study-scaffold does for the studies —
 * hands the writer everything derivable, in a few hundred bytes, so the only
 * thing left is the part that needs a mind.
 *
 * Everything below comes from the Strong's-tagged KJV in docs/assets/chapters/,
 * which means the usage data is already what bin/lexicon-gate.js will check the
 * finished page against. A writer who builds on this brief cannot fabricate a
 * proof-text, because the proof-texts are supplied.
 *
 * Usage:
 *   node bin/lexicon-scaffold.js G4434
 *   node bin/lexicon-scaffold.js --codes G4434,G4995,G26 --out /tmp/lexbriefs
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { BOOK_NAMES } = require('./verse-study-scaffold.js');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const CH = path.join(DOCS, 'assets', 'chapters');
const LEX = path.join(DOCS, 'lexicon');

const clean = (s) => String(s).replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();

function profile(code) {
  const m = code.match(/^([GH])(\d{1,4})$/);
  if (!m) return { code, error: 'not a Strong\'s code' };
  const num = m[2];
  const tag = `<S>${num}</S>`;
  const refs = [];
  const renders = new Map();

  fs.readdirSync(CH).filter((f) => f.endsWith('.json')).forEach((f) => {
    let d;
    try { d = JSON.parse(fs.readFileSync(path.join(CH, f), 'utf8')); } catch (e) { return; }
    const kjv = d.KJV;
    if (!kjv) return;
    const [b, c] = f.replace(/\.json$/, '').split('_').map(Number);
    // Bare Strong's numbers are testament-scoped: H in the OT, G in the NT.
    if (m[1] === 'G' && b <= 39) return;
    if (m[1] === 'H' && b > 39) return;
    Object.keys(kjv).forEach((v) => {
      const txt = kjv[v];
      if (!txt.includes(tag)) return;
      refs.push({ b, c, v: Number(v), ref: `${BOOK_NAMES[b] || 'Book' + b} ${c}:${v}`, text: clean(txt) });
      // What English word does the KJV put in front of this tag?
      const re = new RegExp('([^<>]*?)<S>' + num + '</S>', 'g');
      let mm;
      while ((mm = re.exec(txt)) !== null) {
        const w = clean(mm[1]).split(/\s+/).slice(-2).join(' ').replace(/^[^A-Za-z]+|[^A-Za-z]+$/g, '');
        if (w) renders.set(w.toLowerCase(), (renders.get(w.toLowerCase()) || 0) + 1);
      }
    });
  });

  refs.sort((a, b2) => a.b - b2.b || a.c - b2.c || a.v - b2.v);
  const testament = m[1] === 'H' ? 'OT (Hebrew)' : 'NT (Greek)';
  const pageFp = path.join(LEX, code + '.html');
  const exists = fs.existsSync(pageFp);
  let stub = false;
  if (exists) {
    const s = fs.readFileSync(pageFp, 'utf8').toLowerCase();
    stub = s.includes('definition not found') || s.includes('is a key term in the original scriptures');
  }

  return {
    code, testament,
    pageExists: exists,
    pageIsStub: stub,
    action: !exists ? 'CREATE this page' : (stub ? 'REWRITE this stub' : 'page already has real content — skip'),
    occurrencesInKJV: refs.length,
    kjvRenderings: [...renders.entries()].sort((a, b2) => b2[1] - a[1]).slice(0, 10).map(([w, n]) => `${w} (${n})`),
    // Verses the gate will accept, because it reads the same tags.
    verifiedCitations: refs.slice(0, 8).map((r) => r.ref),
    sampleVerses: refs.slice(0, 4).map((r) => ({ ref: r.ref, kjv: r.text.slice(0, 190) })),
    spread: (() => {
      const books = [...new Set(refs.map((r) => BOOK_NAMES[r.b]))];
      return `${books.length} book(s): ${books.slice(0, 8).join(', ')}${books.length > 8 ? '…' : ''}`;
    })(),
  };
}

function brief(p) {
  if (p.error) return `${p.code}: ${p.error}\n`;
  const L = [];
  L.push(`## ${p.code} — ${p.testament}`);
  L.push(`ACTION: ${p.action}`);
  L.push(`Occurrences in the tagged KJV: ${p.occurrencesInKJV}`);
  L.push(`KJV renders it: ${p.kjvRenderings.join(', ') || '(none found)'}`);
  L.push(`Spread: ${p.spread}`);
  L.push(`VERIFIED citations — use these, the gate reads the same tags:`);
  p.verifiedCitations.forEach((r) => L.push(`   ${r}`));
  L.push(`Sample text:`);
  p.sampleVerses.forEach((s) => L.push(`   ${s.ref} — ${s.kjv}`));
  L.push(`YOU SUPPLY: headword in original script, transliteration, part of speech, and a real definition.`);
  L.push(`If you cannot source the headword honestly, leave ${p.code} undone and report it.`);
  return L.join('\n') + '\n';
}

function main() {
  const argv = process.argv.slice(2);
  let codes = argv.filter((a) => !a.startsWith('--'));
  const ci = argv.indexOf('--codes');
  if (ci >= 0 && argv[ci + 1]) codes = argv[ci + 1].split(',').map((c) => c.trim());
  const oi = argv.indexOf('--out');
  const out = oi >= 0 ? argv[oi + 1] : null;
  if (!codes.length) { console.error('usage: lexicon-scaffold.js G4434 [...] | --codes A,B --out DIR'); process.exit(2); }
  const briefs = codes.map((c) => brief(profile(c)));
  if (out) {
    fs.mkdirSync(out, { recursive: true });
    const fp = path.join(out, 'briefs.md');
    fs.writeFileSync(fp, briefs.join('\n'));
    console.log(`${codes.length} briefs -> ${fp} (${Math.round(fs.statSync(fp).size / 1024)}KB)`);
  } else console.log(briefs.join('\n'));
}

if (require.main === module) main();
module.exports = { profile, brief };
