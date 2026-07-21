#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const htmlPath = new URL('../docs/bible.html', import.meta.url);
const html = fs.readFileSync(htmlPath, 'utf8');

function extractFunction(source, name) {
  const marker = `function ${name}`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} must exist`);
  const open = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = open; i < source.length; i++) {
    const ch = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { quote = ch; continue; }
    if (ch === '{') depth++;
    if (ch === '}' && --depth === 0) return source.slice(start, i + 1);
  }
  throw new Error(`Could not extract ${name}`);
}

function extractBetween(source, startMarker, endMarker) {
  const start = source.indexOf(startMarker);
  const end = source.indexOf(endMarker, start);
  assert.ok(start >= 0 && end > start, `Could not extract ${startMarker}`);
  return source.slice(start, end);
}

const booksSource = extractBetween(html, 'const BOOKS = {', '// ═══════════════════════════════════════════════════════════════════');
const parseRefSource = extractBetween(html, 'function parseRef(ref) {', "// Strip Strong's concordance numbers");
const parserContext = { BIBLE_INDEX: {} };
vm.createContext(parserContext);
vm.runInContext(`${booksSource}\n${parseRefSource}\nthis.parseRef = parseRef;`, parserContext);

for (const dash of ['-', '–', '—', '‑']) {
  const parsed = parserContext.parseRef(`Revelation 1:12${dash}18`);
  assert.ok(parsed, `Revelation range must parse with ${JSON.stringify(dash)}`);
  assert.equal(parsed.bookId, 66);
  assert.equal(parsed.chapter, 1);
  assert.equal(parsed.startVerse, 12);
  assert.equal(parsed.endVerse, 18);
}

const john = parserContext.parseRef('John 3:16');
assert.deepEqual(
  [john.bookId, john.chapter, john.startVerse, john.endVerse],
  [43, 3, 16, 16],
  'John 3:16 must parse exactly'
);

const fetchVerseSource = extractFunction(html, 'fetchVerse');
assert.match(
  fetchVerseSource,
  /fetchChapterData\s*\(/,
  'Single-verse lookup must try the local chapter cache before the external API'
);

const homeStart = html.indexOf('<div id="home-panel">');
const homeEnd = html.indexOf('<div id="back-to-home"', homeStart);
const home = html.slice(homeStart, homeEnd);
assert.ok(
  home.indexOf('class="search-box"') < home.indexOf('id="bibleNav"'),
  'Search must appear above Browse by Book'
);

const introLinkSource = extractBetween(html, 'function bteIntroLinkHtml', 'async function showBookIntro');
assert.doesNotMatch(introLinkSource, /📖/, 'Book-introduction links must not use stock emoji');
assert.match(introLinkSource, /assets\/icons\/shield-(?:bible|book)\.png/, 'Book-introduction links must use a branded shield icon');

assert.match(html, /\.hero\s*\{[^}]*padding:\s*24px 20px 12px;/s, 'Hero spacing must be compact');
assert.match(html, /\.hero \.desc\s*\{[^}]*margin:\s*0 auto 12px;/s, 'Description bottom margin must be compact');

console.log('Bible engine regression tests passed.');
