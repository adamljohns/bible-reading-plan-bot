#!/usr/bin/env node
'use strict';
// lexicon-gate-headword.test.js
//
// The gate matched the headword with class="original-word" — an exact-quote
// match. Pages written as class="original-word " (trailing space) or
// class="original-word heb" therefore failed with "no original-language
// headword" while displaying the headword perfectly. On one revision of the
// corpus that was 1,876 false failures, which is how a stale-tree audit came
// to report a formatting crisis that did not exist.
//
// Per rclone-guards-must-be-tested: the halt path is the one that matters, so
// the cases that MUST still fail are tested first and carry the most weight.

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

const { checkPage } = require('../bin/lexicon-gate.js');

const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lexgate-'));

// A page with enough real body to clear the word floors, so the only thing
// under test is the headword/transliteration extraction.
const filler = 'The word carries a settled sense across its uses in the text, and the '
  + 'translators rendered it consistently where the context allowed. '.repeat(14);

function page({ wordClass = 'original-word', word = 'ἀγάπη', translitClass = 'transliteration', translit = 'Agapē' }) {
  return `<!DOCTYPE html><html><body>
  <div class="word-header">
    <div class="${wordClass}">${word}</div>
    <div class="${translitClass}">${translit}</div>
  </div>
  <div class="section"><h2>Definition</h2><p>${filler}</p></div>
  </body></html>`;
}

function run(name, html) {
  const fp = path.join(dir, name + '.html');
  fs.writeFileSync(fp, html);
  return checkPage(fp);
}

const headwordFail = (r) => r.fails.some((f) => /no original-language headword/.test(f));
const translitFail = (r) => r.fails.some((f) => /no transliteration/.test(f));

let n = 0;
const ok = (label, cond) => { assert.ok(cond, 'FAILED: ' + label); n++; console.log('  ok  ' + label); };

console.log('must STILL FAIL (the halt path):');
ok('empty headword div is caught',
  headwordFail(run('G26', page({ word: '' }))));
ok('missing headword div entirely is caught',
  headwordFail(checkPage((() => {
    const fp = path.join(dir, 'G27.html');
    fs.writeFileSync(fp, `<!DOCTYPE html><html><body><div class="transliteration">Agapē</div>
      <div class="section"><h2>Definition</h2><p>${filler}</p></div></body></html>`);
    return fp;
  })())));
ok('a different class is NOT silently accepted as the headword',
  headwordFail(run('G28', page({ wordClass: 'gloss' }))));
ok('substring class does not count ("original-wordmark")',
  headwordFail(run('G29', page({ wordClass: 'original-wordmark' }))));
ok('empty transliteration is caught',
  translitFail(run('G30', page({ translit: '' }))));
ok('Greek code with a Hebrew headword is caught',
  run('G31', page({ word: 'אָהַב' })).fails.some((f) => /contains no Greek characters/.test(f)));

console.log('must now PASS (the false-failure the fix removes):');
ok('trailing space: class="original-word "',
  !headwordFail(run('G32', page({ wordClass: 'original-word ' }))));
ok('leading space: class=" original-word"',
  !headwordFail(run('G33', page({ wordClass: ' original-word' }))));
ok('extra class: class="original-word heb"',
  !headwordFail(run('G34', page({ wordClass: 'original-word heb' }))));
ok('extra class first: class="heb original-word"',
  !headwordFail(run('G35', page({ wordClass: 'heb original-word' }))));
ok('transliteration tolerates extra classes too',
  !translitFail(run('G36', page({ translitClass: 'transliteration small' }))));
ok('the plain house markup still passes clean',
  !headwordFail(run('G37', page({}))) && !translitFail(run('G37', page({}))));

fs.rmSync(dir, { recursive: true, force: true });
console.log(`\nlexicon-gate headword matching: ${n}/${n} assertions passed.`);
