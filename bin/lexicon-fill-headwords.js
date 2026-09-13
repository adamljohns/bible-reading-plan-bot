#!/usr/bin/env node
/**
 * Fill empty .original-word and .transliteration on lexicon pages from
 * vendored Open Scriptures Strong's data (bin/baselines/strongs-*.json).
 *
 * Normalizes headword divs so bin/lexicon-gate.js can read them:
 *   greek-word / hebrew-word → original-word
 *   original-word greek/heb/grk/hebrew → original-word
 *   broken class="original-word class="greek"" → original-word
 *
 * Does NOT touch definitions, usage prose, or page filenames.
 *
 * Usage: node bin/lexicon-fill-headwords.js [--dry-run]
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const LEX = path.join(ROOT, 'docs', 'lexicon');
const DRY = process.argv.includes('--dry-run');

const greek = JSON.parse(fs.readFileSync(path.join(__dirname, 'baselines/strongs-greek.json'), 'utf8'));
const hebrew = JSON.parse(fs.readFileSync(path.join(__dirname, 'baselines/strongs-hebrew.json'), 'utf8'));

function innerText(s) {
  return s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function lookup(code) {
  if (code.startsWith('G')) return greek[code];
  if (code.startsWith('H')) return hebrew[code];
  return null;
}

/** Extract headword + transliteration from word-header block. */
function readHeader(html) {
  const wh = (html.match(/<div class="word-header">([\s\S]*?)<\/div>\s*<div class="section">/) || [])[1] || '';
  let ow = '';
  let tr = '';
  let owMatch = null;
  let trMatch = null;

  const owRe = /<div class="([^"]*(?:original-word|greek-word|hebrew-word)[^"]*)"([^>]*)>([\s\S]*?)<\/div>/;
  const trRe = /<div class="([^"]*transliteration[^"]*)"([^>]*)>([\s\S]*?)<\/div>/;
  owMatch = wh.match(owRe);
  trMatch = wh.match(trRe);
  if (owMatch) ow = innerText(owMatch[3]);
  if (trMatch) tr = innerText(trMatch[3]);
  return { wh, ow, tr, owMatch, trMatch };
}

function renderDiv(kind, extraAttrs, body) {
  const attrs = extraAttrs ? extraAttrs.trim() : '';
  const attrStr = attrs ? ' ' + attrs : '';
  return `<div class="${kind}"${attrStr}>${body}</div>`;
}

const STUB_MARK = '<p style="color:var(--gray);font-size:1.1rem;font-style:italic">Strong&#39;s ';

const stats = {
  scanned: 0,
  changed: 0,
  filledOw: 0,
  filledTr: 0,
  normClass: 0,
  renamedClass: 0,
  fixedBroken: 0,
  stubInjected: 0,
  skippedNoData: [],
};

for (const fn of fs.readdirSync(LEX).sort()) {
  const m = fn.match(/^([GH])(\d{1,4})\.html$/);
  if (!m) continue;
  stats.scanned++;
  const code = m[1] + m[2];
  const fp = path.join(LEX, fn);
  let html = fs.readFileSync(fp, 'utf8');
  const entry = lookup(code);

  // Compact stub pages (no word-header) — inject headword divs after Strong's line
  if (!html.includes('word-header') && html.includes(STUB_MARK)) {
    if (html.includes('class="original-word"')) continue;
    if (!entry || !entry.lemma) {
      stats.skippedNoData.push(code);
      continue;
    }
    const tr = entry.translit || entry.xlit || '';
    const inject =
      `\n<div class="original-word">${entry.lemma}</div>` +
      `\n<div class="transliteration">${tr}</div>`;
    const anchor = STUB_MARK + code + '</p>';
    if (!html.includes(anchor)) {
      stats.skippedNoData.push(code);
      continue;
    }
    html = html.replace(anchor, anchor + inject);
    stats.stubInjected++;
    stats.filledOw++;
    if (tr) stats.filledTr++;
    stats.changed++;
    if (!DRY) fs.writeFileSync(fp, html);
    continue;
  }

  const { wh, ow, tr, owMatch, trMatch } = readHeader(html);
  if (!wh || !owMatch || !trMatch) continue;

  let newOw = ow;
  let newTr = tr;
  let fileChanged = false;

  // Fix broken class="original-word class="greek"" pattern
  let owClass = owMatch[1];
  let owExtra = owMatch[2] || '';
  if (/original-word class=/.test(owClass)) {
    stats.fixedBroken++;
    owClass = 'original-word';
    owExtra = owExtra.replace(/\s*class="[^"]*"/, '');
    fileChanged = true;
  } else if (/greek-word|hebrew-word/.test(owClass)) {
    stats.renamedClass++;
    owClass = 'original-word';
    fileChanged = true;
  } else if (owClass !== 'original-word') {
    stats.normClass++;
    owClass = 'original-word';
    fileChanged = true;
  }

  let trClass = trMatch[1];
  let trExtra = trMatch[2] || '';
  if (trClass !== 'transliteration') {
    stats.normClass++;
    trClass = 'transliteration';
    fileChanged = true;
  }

  if (!newOw && entry && entry.lemma) {
    newOw = entry.lemma;
    stats.filledOw++;
    fileChanged = true;
  }
  if (!newTr && entry) {
    const t = entry.translit || entry.xlit;
    if (t) {
      newTr = t;
      stats.filledTr++;
      fileChanged = true;
    }
  }

  if (!fileChanged) continue;

  const newOwDiv = renderDiv(owClass, owExtra, newOw || owMatch[3]);
  const newTrDiv = renderDiv(trClass, trExtra, newTr || trMatch[3]);

  let newWh = wh.replace(owMatch[0], newOwDiv).replace(trMatch[0], newTrDiv);
  html = html.replace(
    /<div class="word-header">([\s\S]*?)<\/div>\s*<div class="section">/,
    `<div class="word-header">${newWh}</div>\n        <div class="section">`
  );
  stats.changed++;
  if (!DRY) fs.writeFileSync(fp, html);
}

const stillEmpty = [];
for (const fn of fs.readdirSync(LEX)) {
  const m = fn.match(/^([GH]\d{1,4})\.html$/);
  if (!m) continue;
  const code = m[1];
  const raw = fs.readFileSync(path.join(LEX, fn), 'utf8');
  const { ow, tr } = readHeader(raw);
  const gateOw = (raw.match(/class="original-word"[^>]*>([\s\S]*?)<\/div>/) || [])[1];
  const gateTr = (raw.match(/class="transliteration"[^>]*>([\s\S]*?)<\/div>/) || [])[1];
  if (!innerText(gateOw || '')) stillEmpty.push(code + ':gate-ow');
  else if (!innerText(gateTr || '')) stillEmpty.push(code + ':gate-tr');
  if ((!ow || !tr) && !lookup(code)) stats.skippedNoData.push(code);
}

console.log(JSON.stringify({
  ...stats,
  skippedNoData: [...new Set(stats.skippedNoData)],
  stillEmptyCount: stillEmpty.length,
  stillEmptySample: stillEmpty.slice(0, 25),
}, null, 2));
if (DRY) console.log('(dry run — no files written)');
