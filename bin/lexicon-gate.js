#!/usr/bin/env node
/* lexicon-gate.js — verify a lexicon entry is real scholarship, not filler.
 *
 * The 38 stub pages in docs/lexicon/ exist because something generated plausible
 * prose without a source: "Definition not found." followed by "this word is a key
 * term in the original Scriptures... its meaning of 'see definition' is
 * foundational." That reads like scholarship and teaches nothing, which makes it
 * worse than an empty page.
 *
 * So a new or rewritten entry has to prove itself, and the strongest available
 * proof is local: the KJV in docs/assets/chapters/ carries <S>NNNN</S> tags on
 * every word. If a page claims a verse is a key use of G4434, that verse must
 * actually carry the G4434 tag. A fabricated proof-text fails here.
 *
 * Usage:
 *   node bin/lexicon-gate.js docs/lexicon/G4434.html [...]
 *   node bin/lexicon-gate.js --codes G4434,G4995     # by Strong's code
 *   node bin/lexicon-gate.js --all                   # every page (slow)
 * Exit: 0 all pass, 1 any fail.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { BOOK_IDS } = require('./verse-study-scaffold.js');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const LEX = path.join(DOCS, 'lexicon');
const CH = path.join(DOCS, 'assets', 'chapters');

const MIN_DEF_WORDS = 25;
const MIN_BODY_WORDS = 120;

/* The tells of generated filler. Any one of these means the page is not finished,
 * no matter how much prose surrounds it. */
const FILLER = [
  'definition not found',
  'is a key term in the original scriptures',
  'meaning of "see definition"',
  'meaning of “see definition”',
  'reveals its rich usage throughout the bible',
  'connecting to themes of god’s character and his relationship with humanity',
  'connecting to themes of god\'s character and his relationship with humanity',
  'further study of',
];

const strip = (s) => s.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '');
const text = (s) => s.replace(/<[^>]+>/g, ' ')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&#39;/g, "'")
  .replace(/&quot;/g, '"').replace(/&[a-z]+;/g, ' ')
  .replace(/\s+/g, ' ').trim();
const words = (s) => text(s).split(/\s+/).filter(Boolean).length;

function section(body, label) {
  const re = new RegExp('>\\s*' + label + '\\s*<\\/h\\d>([\\s\\S]{0,2600})', 'i');
  const m = body.match(re);
  return m ? m[1] : '';
}

const chCache = new Map();
function chapter(bookId, ch) {
  const key = bookId + '_' + ch;
  if (!chCache.has(key)) {
    const fp = path.join(CH, key + '.json');
    chCache.set(key, fs.existsSync(fp) ? JSON.parse(fs.readFileSync(fp, 'utf8')) : null);
  }
  return chCache.get(key);
}

/* Does <ref> actually carry this Strong's number in the tagged KJV? */
function verseCarriesCode(ref, num) {
  const m = String(ref).match(/^([1-3]?\s*[A-Za-z ]+?)\s+(\d+):(\d+)/);
  if (!m) return null;                       // unparseable — reported separately
  const id = BOOK_IDS[m[1].trim().toLowerCase()];
  if (!id) return null;
  const data = chapter(id, parseInt(m[2], 10));
  if (!data || !data.KJV) return null;       // no local text — cannot check
  const v = data.KJV[String(parseInt(m[3], 10))];
  if (!v) return false;
  return new RegExp('<S>' + num + '</S>').test(v);
}

function checkPage(fp) {
  const rel = path.relative(ROOT, fp);
  const fails = [];
  const warns = [];
  if (!fs.existsSync(fp)) return { rel, fails: ['file does not exist'], warns };

  const raw = fs.readFileSync(fp, 'utf8');
  const body = strip(raw);
  const code = path.basename(fp, '.html');
  const codeM = code.match(/^([GH])(\d{1,4})$/);
  if (!codeM) return { rel, fails: [`filename "${code}" is not a Strong's code`], warns };
  const num = codeM[2];

  // ── headword must be present ──────────────────────────────────────────
  const div = (cls) => text((body.match(new RegExp('class="' + cls + '"[^>]*>([\\s\\S]*?)</div>')) || [])[1] || '');
  const script = div('original-word');
  const translit = div('transliteration');
  if (!script) fails.push('no original-language headword (.original-word is empty)');
  if (!translit) fails.push('no transliteration (.transliteration is empty)');
  if (script && codeM[1] === 'G' && !/[Ͱ-Ͽἀ-῿]/.test(script)) {
    fails.push(`headword "${script}" contains no Greek characters but ${code} is Greek`);
  }
  if (script && codeM[1] === 'H' && !/[֐-׿]/.test(script)) {
    fails.push(`headword "${script}" contains no Hebrew characters but ${code} is Hebrew`);
  }

  // ── definition must say something ─────────────────────────────────────
  const def = section(body, 'Definition');
  const defW = words(def);
  if (!defW) fails.push('no Definition section');
  else if (defW < MIN_DEF_WORDS) fails.push(`Definition is ${defW} words, below the ${MIN_DEF_WORDS}-word floor`);

  const hay = text(body).toLowerCase();
  FILLER.forEach((f) => {
    if (hay.includes(f)) fails.push(`contains generated filler: "${f}"`);
  });

  const bodyW = words(body);
  if (bodyW < MIN_BODY_WORDS) fails.push(`page is ${bodyW} words total, below the ${MIN_BODY_WORDS}-word floor`);

  // ── cited verses must actually contain the word ───────────────────────
  // This is the anti-fabrication check. A page may cite verses the local KJV
  // cannot confirm, but it may not cite verses the local KJV *contradicts*.
  const refs = [...new Set((text(body).match(/\b(?:[1-3]\s*)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+\d+:\d+/g) || []))];
  let checked = 0, confirmed = 0;
  const contradicted = [];
  refs.forEach((r) => {
    const res = verseCarriesCode(r, num);
    if (res === null) return;
    checked++;
    if (res) confirmed++; else contradicted.push(r);
  });
  if (checked >= 3 && confirmed === 0) {
    fails.push(`none of the ${checked} checkable verse citations actually carry ${code} in the tagged KJV — the usage section appears invented`);
  } else if (contradicted.length && confirmed === 0) {
    fails.push(`cited verses do not carry ${code}: ${contradicted.slice(0, 4).join(', ')}`);
  } else if (contradicted.length) {
    warns.push(`${contradicted.length} cited verse(s) do not carry ${code} in the KJV tagging (may be a related form or a different translation's wording): ${contradicted.slice(0, 3).join(', ')}`);
  }
  if (!checked) warns.push('no verse citation could be checked against the local KJV tagging');

  // ── links must resolve ────────────────────────────────────────────────
  [...body.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1]).forEach((href) => {
    if (/^(https?:|mailto:|data:|#|tel:)/.test(href)) return;
    const clean = href.split(/[?#]/)[0];
    if (!clean) return;
    const target = clean.startsWith('/') ? path.join(DOCS, clean.slice(1)) : path.resolve(path.dirname(fp), clean);
    if (!fs.existsSync(target)) fails.push(`dead local link: ${href}`);
  });

  return { rel, code, fails, warns, defW, bodyW, confirmed, checked };
}

function main() {
  const argv = process.argv.slice(2);
  let targets = argv.filter((a) => !a.startsWith('--'));
  const ci = argv.indexOf('--codes');
  if (ci >= 0 && argv[ci + 1]) {
    targets = argv[ci + 1].split(',').map((c) => path.join(LEX, c.trim() + '.html'));
  }
  if (argv.includes('--all')) {
    targets = fs.readdirSync(LEX).filter((f) => f.endsWith('.html')).map((f) => path.join(LEX, f));
  }
  if (!targets.length) {
    console.error("usage: lexicon-gate.js <page.html> [...] | --codes G4434,G26 | --all");
    process.exit(2);
  }
  let failed = 0;
  targets.forEach((t) => {
    const r = checkPage(path.resolve(t));
    if (r.fails.length) {
      failed++;
      console.log(`FAIL  ${r.rel}`);
      r.fails.forEach((f) => console.log('        ✗ ' + f));
    } else {
      console.log(`pass  ${r.rel}  (def ${r.defW}w, page ${r.bodyW}w, ${r.confirmed}/${r.checked} citations confirmed in tagged KJV)`);
    }
    r.warns.forEach((w) => console.log('        ! ' + w));
  });
  console.log(`\nLexicon gate: ${targets.length - failed}/${targets.length} passed.`);
  if (failed) { console.log('Nothing ships until these are fixed.'); process.exit(1); }
}

if (require.main === module) main();
module.exports = { checkPage, verseCarriesCode };
