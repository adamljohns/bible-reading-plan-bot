#!/usr/bin/env node
/* parse-institutes.js — parse CCEL's Beveridge ThML into per-chapter JSON.
 *
 * Source: CCEL ThML XML (clean, structured, with <scripRef> tags). One bulk
 * download, parsed deterministically — no per-chapter web fetches.
 *   div1 id iii/iv/v/vi = Books 1-4. Within a book, div2s = [ARGUMENT, ch1, ch2, ...].
 *   A chapter div2 = introHead(title), optional intro(argument), introHead "Sections.",
 *   intro(s) (section summaries), then class-less <p> body paragraphs each opening
 *   with "N. " (the numbered section). <scripRef passage="..."> = scripture cited.
 *
 * Emits docs/assets/institutes/b{B}c{CC}.json. Reads /tmp/inst.xml (or downloads).
 * Run: node bin/parse-institutes.js
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'docs', 'assets', 'institutes');
const XML_PATH = '/tmp/inst.xml';
const XML_URL = 'https://ccel.org/ccel/c/calvin/institutes.xml';
const BOOK_DIV1 = { iii: 1, iv: 2, v: 3, vi: 4 }; // div1 id -> book number
const EXPECT = { 1: 18, 2: 17, 3: 25, 4: 20 };

function getXml() {
  if (!fs.existsSync(XML_PATH)) {
    console.log('Downloading CCEL ThML...');
    execSync('curl -s -L "' + XML_URL + '" -o "' + XML_PATH + '"');
  }
  return fs.readFileSync(XML_PATH, 'utf8');
}

// ---- entity + tag helpers ----
const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: '—', ndash: '–', hellip: '…', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”' };
function decodeEntities(s) {
  return s.replace(/&(#x?[0-9a-fA-F]+|[a-zA-Z]+);/g, (m, e) => {
    if (e[0] === '#') {
      const code = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return isNaN(code) ? m : String.fromCodePoint(code);
    }
    return NAMED[e] != null ? NAMED[e] : m;
  });
}
function plain(html) {
  return decodeEntities(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
}
// clean a scripRef passage into the site's ref format ("Prov. 29:18" -> "Prov 29:18")
function cleanRef(p) {
  return decodeEntities(p).replace(/\.(?=\s|\d)/g, '').replace(/\s+/g, ' ').trim();
}

function extractScripRefs(html) {
  const out = [];
  const re = /<scripRef[^>]*\bpassage="([^"]*)"/g; let m;
  while ((m = re.exec(html))) { const r = cleanRef(m[1]); if (r && out.indexOf(r) < 0) out.push(r); }
  return out;
}

function parseChapter(div2Html, bookNum, chapNum, scaffoldTitle) {
  // collect <p> with class + raw inner (raw kept for scripRef)
  const ps = [];
  const re = /<p\b([^>]*)>([\s\S]*?)<\/p>/g; let m;
  while ((m = re.exec(div2Html))) {
    const cls = (m[1].match(/class="([^"]*)"/) || [, ''])[1];
    ps.push({ cls, raw: m[2], text: plain(m[2]) });
  }
  let argument = '';
  const sectionSummaries = [];
  const bodyPs = [];
  let seenSections = false, seenTitle = false;
  for (const p of ps) {
    if (!p.text) continue;
    if (p.cls === 'introHead') {
      if (/^sections\.?$/i.test(p.text)) { seenSections = true; continue; }
      if (!seenTitle) { seenTitle = true; continue; } // chapter title (use scaffold instead)
      continue;
    }
    if (p.cls === 'intro') {
      if (!seenSections) { argument = argument ? argument + ' ' + p.text : p.text; }
      else { sectionSummaries.push(p.text); }
      continue;
    }
    bodyPs.push(p); // class-less = body
  }
  // group body into numbered sections
  const sections = [];
  let cur = null;
  for (const p of bodyPs) {
    const lead = p.text.match(/^(\d+)\.\s+([\s\S]*)$/);
    if (lead) {
      cur = { n: parseInt(lead[1], 10), paragraphs: [lead[2].trim()], prooftexts: extractScripRefs(p.raw) };
      sections.push(cur);
    } else if (cur) {
      cur.paragraphs.push(p.text);
      extractScripRefs(p.raw).forEach((r) => { if (cur.prooftexts.indexOf(r) < 0) cur.prooftexts.push(r); });
    } else {
      // body before any numbered section (rare) -> seed section 1
      cur = { n: 1, paragraphs: [p.text], prooftexts: extractScripRefs(p.raw) };
      sections.push(cur);
    }
  }
  return {
    book: bookNum, chapter: chapNum,
    title: scaffoldTitle || '',
    argument: argument,
    sectionSummaries: sectionSummaries,
    sections: sections,
    translator: 'Henry Beveridge (1845)',
    source: 'CCEL ThML (public domain)',
  };
}

function main() {
  const xml = getXml();
  const scaffold = JSON.parse(fs.readFileSync(path.join(OUT, 'index.json'), 'utf8'));
  const titlesByBook = {};
  scaffold.books.forEach((b) => { titlesByBook[b.number] = {}; b.chapters.forEach((c) => { titlesByBook[b.number][c.number] = c.title; }); });

  let totalCh = 0, totalSec = 0, totalRefs = 0;
  const report = [];
  Object.keys(BOOK_DIV1).forEach((div1id) => {
    const bookNum = BOOK_DIV1[div1id];
    // slice this book's div1 region
    const bm = new RegExp('<div1 [^>]*id="' + div1id + '"[^>]*>([\\s\\S]*?)(?=<div1 |</ThML.body>|$)').exec(xml);
    if (!bm) { console.log('!! book div1 not found:', div1id); return; }
    const region = bm[1];
    // all div2s in order
    const div2s = [];
    const dre = /<div2\b([^>]*)>([\s\S]*?)(?=<div2\b|<\/div1>|$)/g; let dm;
    while ((dm = dre.exec(region))) div2s.push({ attrs: dm[1], html: dm[2] });
    // first div2 = ARGUMENT (book preamble); rest = chapters
    const bookArg = div2s.length ? plain(div2s[0].html) : '';
    const chapDiv2s = div2s.slice(1);
    let chNum = 0;
    chapDiv2s.forEach((d) => {
      chNum++;
      const ch = parseChapter(d.html, bookNum, chNum, (titlesByBook[bookNum] || {})[chNum]);
      ch.bookArgument = chNum === 1 ? bookArg : undefined; // attach book argument once
      fs.writeFileSync(path.join(OUT, 'b' + bookNum + 'c' + String(chNum).padStart(2, '0') + '.json'), JSON.stringify(ch, null, 2));
      totalCh++; totalSec += ch.sections.length; ch.sections.forEach((s) => totalRefs += s.prooftexts.length);
      report.push('  B' + bookNum + ' C' + String(chNum).padStart(2, '0') + ': ' + ch.sections.length + ' sections, ' +
        ch.sections.reduce((a, s) => a + s.prooftexts.length, 0) + ' refs' + (ch.title ? '' : '  [NO TITLE]'));
    });
    const ok = chNum === EXPECT[bookNum] ? 'OK' : '!! EXPECTED ' + EXPECT[bookNum];
    console.log('Book ' + bookNum + ': ' + chNum + ' chapters (' + ok + ')');
  });
  console.log(report.join('\n'));
  console.log('TOTAL: ' + totalCh + ' chapters, ' + totalSec + ' sections, ' + totalRefs + ' scripture refs');
}
main();
