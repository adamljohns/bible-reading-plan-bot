#!/usr/bin/env node
/* parse-confessions.js — parse Augustine's Confessions (Pilkington, 1876) into per-book JSON.
 *
 * Source: CCEL ThML for Nicene and Post-Nicene Fathers, Series I, Vol. 1
 *   (ed. Philip Schaff, 1886) — https://ccel.org/ccel/s/schaff/npnf101.xml
 *   The Confessions sit in div1 id="vi", "Translated and Annotated by J.G. Pilkington, M.A."
 *   PUBLIC DOMAIN (1886 publication).
 *
 * ⚠️  DO NOT use https://ccel.org/ccel/a/augustine/confessions.xml — that is the
 *     Albert C. Outler translation (1955, Westminster Press). CCEL's metadata stamps it
 *     <DC.Rights>Public Domain</DC.Rights>, but it is a post-1928 translation and fails
 *     this project's translation policy. It is the Battles trap wearing a PD sticker.
 *
 * Structure:
 *   div1 id="vi"                      -> The Confessions
 *     div2 type="Book"  n="I".."XIII" -> 13 books; @title = the book's argument
 *       div3 type="Chapter" n="I"...  -> chapters; @title = chapter title
 *         <p> bodies; numbered sections run CONTINUOUSLY across a whole book
 *         ("1." in ch I, "2." in ch II, ...), so section numbers are book-wide.
 *
 * Two correctness decisions that this parser exists to get right:
 *   1. <note> elements are INLINE inside body <p>s (1,360 of them) and hold Pilkington's
 *      footnotes — overwhelmingly Scripture citations. Stripping tags naively (the way
 *      parse-institutes.js does, which is safe for Beveridge) would weld footnote text
 *      into the middle of Augustine's prose: '...Thou art there." Ps. cxxxix. 8 . I could
 *      not therefore exist...'. So notes are EXCISED from the body first, and their
 *      citations are harvested separately.
 *   2. Scripture refs carry three forms that disagree with each other:
 *        visible text  "Ps. cxxxix. 8"   (Pilkington's printed citation, roman)
 *        @passage      "Ps. 139.9"       (CCEL's normalization — sometimes off by one)
 *        @osisRef      "Bible:Ps.139.9"  (CCEL's machine parse — sometimes plain wrong,
 *                                         e.g. "Ps. cxlix." parsed as Bible:Ps.49)
 *      We convert the PRINTED citation ourselves (roman -> arabic), use osisRef as a
 *      cross-check, and report every disagreement rather than silently shipping one.
 *
 * Emits docs/assets/confessions/b{B}.json (13 files) + a reconciliation report.
 * Run: node bin/parse-confessions.js          (add --report-only to skip writing)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'docs', 'assets', 'confessions');
const XML_PATH = '/tmp/npnf101.xml';
const XML_URL = 'https://ccel.org/ccel/s/schaff/npnf101.xml';
const REPORT_ONLY = process.argv.includes('--report-only');

// Chapters per book AS THIS EDITION DIVIDES THEM (verified 2026-10-04 against the div3
// n= attributes and the printed chapter headings: Book I runs I..XVIII with no gaps).
// Other editions of the Confessions divide Book I into 20 chapters — do not "correct"
// these numbers to match a printed copy of Pusey or Outler. This table exists to detect
// drift if CCEL re-issues the file, not to validate against an outside edition.
const EXPECT = { 1: 18, 2: 10, 3: 12, 4: 16, 5: 14, 6: 16, 7: 21, 8: 12, 9: 13, 10: 43, 11: 31, 12: 32, 13: 38 };

function getXml() {
  if (!fs.existsSync(XML_PATH)) {
    console.log('Downloading CCEL ThML (NPNF1-01, ~5MB)...');
    execSync('curl -s -L -A "Mozilla/5.0 MOOP-fetch" "' + XML_URL + '" -o "' + XML_PATH + '"');
  }
  return fs.readFileSync(XML_PATH, 'utf8');
}

// ---------- entities / text ----------
const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: '—', ndash: '–',
  hellip: '…', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”', sect: '§', deg: '°', aelig: 'æ', oelig: 'œ' };
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
  return decodeEntities(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
}
// Attribute read must be anchored to a preceding space, or asking for `title` happily
// returns `shorttitle`'s value — which silently titled every chapter "Chapter II".
const attr = (tag, name) => (new RegExp('(?:^|\\s)' + name + '="([^"]*)"').exec(tag) || [, ''])[1];

// ---------- roman numerals ----------
const ROMAN = { i: 1, v: 5, x: 10, l: 50, c: 100, d: 500, m: 1000 };
function romanToInt(s) {
  const t = String(s).toLowerCase().replace(/[^ivxlcdm]/g, '');
  if (!t) return null;
  let total = 0;
  for (let i = 0; i < t.length; i++) {
    const cur = ROMAN[t[i]], next = ROMAN[t[i + 1]];
    if (cur == null) return null;
    total += next != null && cur < next ? -cur : cur;
  }
  return total || null;
}

// ---------- scripture references ----------
// OSIS book id -> the abbreviation lbcf-render.js / BTE expects.
const OSIS_TO_SITE = {
  Gen: 'Gen', Exod: 'Exo', Lev: 'Lev', Num: 'Num', Deut: 'Deut', Josh: 'Josh', Judg: 'Judg', Ruth: 'Ruth',
  '1Sam': '1 Sam', '2Sam': '2 Sam', '1Kgs': '1 Kings', '2Kgs': '2 Kings', '1Chr': '1 Chr', '2Chr': '2 Chr',
  Ezra: 'Ezra', Neh: 'Neh', Esth: 'Est', Job: 'Job', Ps: 'Ps', Prov: 'Prov', Eccl: 'Eccl', Song: 'Song',
  Isa: 'Isa', Jer: 'Jer', Lam: 'Lam', Ezek: 'Ezek', Dan: 'Dan', Hos: 'Hos', Joel: 'Joel', Amos: 'Amos',
  Obad: 'Obad', Jonah: 'Jonah', Mic: 'Mic', Nah: 'Nah', Hab: 'Hab', Zeph: 'Zeph', Hag: 'Hag',
  Zech: 'Zech', Mal: 'Mal', Matt: 'Matt', Mark: 'Mark', Luke: 'Luke', John: 'John', Acts: 'Acts',
  Rom: 'Rom', '1Cor': '1 Cor', '2Cor': '2 Cor', Gal: 'Gal', Eph: 'Eph', Phil: 'Phil', Col: 'Col',
  '1Thess': '1 Thess', '2Thess': '2 Thess', '1Tim': '1 Tim', '2Tim': '2 Tim', Titus: 'Titus',
  Phlm: 'Phlm', Heb: 'Heb', Jas: 'Jas', '1Pet': '1 Pet', '2Pet': '2 Pet', '1John': '1 John',
  '2John': '2 John', '3John': '3 John', Jude: 'Jude', Rev: 'Rev',
  // Pilkington cites the Apocrypha (Wisdom, Sirach); no BTE target — kept, flagged, not linked.
  Wis: 'Wis', Sir: 'Sir', Tob: 'Tob', Jdt: 'Jdt', Bar: 'Bar', '1Macc': '1 Macc', '2Macc': '2 Macc',
};
const APOCRYPHA = new Set(['Wis', 'Sir', 'Tob', 'Jdt', 'Bar', '1Macc', '2Macc']);

// "Bible:Ps.139.9" -> {book:'Ps', ch:139, v:9}
function parseOsis(one) {
  const m = /^Bible:([0-9A-Za-z]+)(?:\.(\d+))?(?:\.(\d+))?/.exec(one.trim());
  if (!m) return null;
  return { book: m[1], ch: m[2] ? parseInt(m[2], 10) : null, v: m[3] ? parseInt(m[3], 10) : null };
}
// Pilkington's printed citation, but ONLY the shape we can independently verify:
// a book name followed by an EXPLICIT ROMAN chapter, e.g. "Ps. cxxxix. 8", "1 Cor. xiv. 22".
// Deliberately returns null for everything else, because the other shapes are either
// continuations we cannot resolve without tracking prior context ("Ibid. ver. 29",
// "ibid. 16", a bare "ii. 5") or carry OCR letter-for-digit damage ("l Cor.", "Matt. xix. 2l",
// "Ps. 1i. 6"). CCEL's osisRef resolves all of those correctly; an earlier version of this
// parser tried to beat it at them and produced garbage like "Matt 5:29" from "Ibid. ver. 29"
// (the "v" of "ver" parsed as roman 5). Leave them to osisRef.
function parsePrintedRoman(text) {
  const t = plain(text);
  const m = /^((?:[1-3]\s*)?[A-Z][A-Za-z]*)\.?\s+([ivxlcdm]+)\.?(?:\s*(\d+))?\s*$/.exec(t);
  if (!m) return null;
  const ch = romanToInt(m[2]);
  if (ch == null) return null;
  return { bookText: m[1].trim(), ch: ch, v: m[3] ? parseInt(m[3], 10) : null };
}
function fmtRef(book, ch, v) {
  const site = OSIS_TO_SITE[book] || book;
  if (ch == null) return site;
  return site + ' ' + ch + (v != null ? ':' + v : '');
}

// Harvest every scripRef in an html blob.
//
// osisRef is the base, because it is the only form that resolves Pilkington's continuation
// citations ("Ibid. ver. 29") against their antecedent. It is overridden in exactly two
// evidence-backed cases, both verified 2026-10-04 against this repo's own tagged KJV:
//
//   (a) HUNDREDS DROP — CCEL's roman-numeral parser loses the leading "c" on Psalm numbers
//       >= 100: "Ps. cxlix." -> Bible:Ps.49, "Psalm ciii." -> Ps.3, "Psalm cii." -> Ps.2,
//       "Ps. cxxiv. 5" -> Ps.24:5, "Ps. cxxxvi. 6" -> Ps.36:6. Signature: printed >= 100
//       and printed % 100 === osis chapter. Spot-checked against KJV and the quoted text:
//       "the proud waters had gone over our soul" is Ps 124:5, not 24:5; "stretched out the
//       earth above the waters" is Ps 136:6, not 36:6.
//   (b) VERSE SLIP — chapter agrees but the printed verse differs: "Ps. cxxxix. 8" against
//       osisRef Ps 139:9, where the text quotes "if I go down into hell Thou art there"
//       = KJV Ps 139:8. Printed wins.
//
// Anything else that disagrees is recorded in ref-disputes.json with needsReview, and
// osisRef is kept. (One known case needs a human: Book 9 ch. 12 prints "Psalm cii." beside
// a quotation of "I will sing of mercy and judgment", which is KJV Ps 101:1 — so neither
// 102 nor CCEL's 2 matches the quote, and Pilkington himself appears to have slipped. We
// publish his citation rather than silently emending it.)
function harvestRefs(html, bag, disputes, where) {
  const re = /<scripRef\b([^>]*)>([\s\S]*?)<\/scripRef>/g;
  let m;
  while ((m = re.exec(html))) {
    const tag = m[1], inner = m[2];
    const osisAll = attr(tag, 'osisRef').split(/\s+/).filter(Boolean).map(parseOsis).filter(Boolean);
    if (!osisAll.length) continue;
    const add = (ref) => { if (ref && !bag.includes(ref)) bag.push(ref); };

    // Only single-target refs can be reconciled; "Ps. 145.3; 147.5" is taken as given.
    if (osisAll.length === 1) {
      const o = osisAll[0];
      const p = parsePrintedRoman(inner);
      if (p && (p.ch !== o.ch || (p.v != null && o.v != null && p.v !== o.v))) {
        const hundredsDrop = p.ch >= 100 && p.ch % 100 === o.ch;
        const verseSlip = p.ch === o.ch && p.v != null;
        // Fits the hundreds-drop signature mechanically, but the quoted line ("I will sing
        // of mercy and judgment") is KJV Ps 101:1, so neither 102 nor CCEL's 2 matches the
        // text and Pilkington's own citation looks like a slip for "ci." We publish what he
        // printed and keep the case visible instead of burying it in the corrected bucket.
        const suspect = /^Psalm cii\.$/.test(plain(inner));
        const resolved = hundredsDrop || verseSlip
          ? fmtRef(o.book, p.ch, p.v != null ? p.v : o.v)
          : fmtRef(o.book, o.ch, o.v);
        disputes.push({
          where: where,
          printed: plain(inner),
          passage: attr(tag, 'passage'),
          printedParsed: fmtRef(o.book, p.ch, p.v != null ? p.v : o.v),
          osis: fmtRef(o.book, o.ch, o.v),
          reason: suspect ? 'ccel-dropped-hundreds; printed citation itself looks like a slip for "ci." (quoted line is KJV Ps 101:1)'
            : hundredsDrop ? 'ccel-dropped-hundreds' : verseSlip ? 'verse-slip' : 'unexplained',
          resolved: resolved,
          needsReview: suspect || !(hundredsDrop || verseSlip),
        });
        add(resolved);
        continue;
      }
    }
    osisAll.forEach((o) => add(fmtRef(o.book, o.ch, o.v)));
  }
}

// ---------- chapter ----------
function parseChapter(html, bookNum, disputes) {
  const openTag = /^<div3\b[^>]*>/.exec(html)[0];
  const chNum = romanToInt(attr(openTag, 'n'));
  const title = decodeEntities(attr(openTag, 'title')).replace(/\s+/g, ' ').trim();

  const prooftexts = [];
  const where = 'Book ' + bookNum + ' ch. ' + chNum;

  // 1. Harvest refs from the WHOLE chapter (notes included) before excising anything.
  harvestRefs(html, prooftexts, disputes, where);

  // 2. Excise <note>...</note> so footnote text never lands inside Augustine's prose.
  const body = html.replace(/<note\b[^>]*>[\s\S]*?<\/note>/g, ' ');

  // 3. Body paragraphs, skipping the repeated "Chapter N.—Title" heading paragraph.
  const paras = [];
  const pre = /<p\b([^>]*)>([\s\S]*?)<\/p>/g;
  let pm;
  while ((pm = pre.exec(body))) {
    const text = plain(pm[2]);
    if (!text) continue;
    if (/^Chapter\s+[IVXLCDM]+\s*[.—-]/i.test(text)) continue; // heading, already in @title
    paras.push(text);
  }

  // 4. Group into the book-wide numbered sections.
  const sections = [];
  let cur = null;
  for (const p of paras) {
    const lead = /^(\d+)\.\s+([\s\S]*)$/.exec(p);
    if (lead) {
      cur = { n: parseInt(lead[1], 10), paragraphs: [lead[2].trim()] };
      sections.push(cur);
    } else if (cur) {
      cur.paragraphs.push(p);
    } else {
      cur = { n: null, paragraphs: [p] }; // unnumbered lead-in (does occur)
      sections.push(cur);
    }
  }

  return { n: chNum, title: title, sections: sections, prooftexts: prooftexts };
}

// ---------- main ----------
function main() {
  const xml = getXml();
  const s = /<div1\b[^>]*id="vi"/.exec(xml);
  const e = /<div1\b[^>]*id="vii"/.exec(xml);
  if (!s || !e) throw new Error('Confessions div1 (id="vi") not found — CCEL markup changed; re-inspect.');
  const region = xml.slice(s.index, e.index);

  // Sanity-check the translator before writing a single file.
  if (!/Pilkington/i.test(region.slice(0, 3000))) {
    throw new Error('Expected Pilkington in the Confessions front matter — refusing to parse an unverified translation.');
  }

  // Book div2s (type="Book"); front-matter div2s (preface, "Opinion of St. Augustin") are skipped.
  const bookTags = [];
  const bre = /<div2\b([^>]*)>/g;
  let bm;
  while ((bm = bre.exec(region))) {
    if (/type="Book"/.test(bm[1])) bookTags.push({ attrs: bm[1], start: bm.index });
  }
  bookTags.forEach((b, i) => { b.html = region.slice(b.start, i + 1 < bookTags.length ? bookTags[i + 1].start : region.length); });

  if (!REPORT_ONLY) fs.mkdirSync(OUT, { recursive: true });

  const disputes = [];
  const index = { work: "Augustine's Confessions", translator: 'J.G. Pilkington (1876)',
    source: 'Nicene and Post-Nicene Fathers, Series I, Vol. 1, ed. Philip Schaff (1886) — CCEL ThML, public domain',
    books: [] };
  let totCh = 0, totSec = 0, totRefs = 0, apoc = 0, problems = [];

  bookTags.forEach((b) => {
    const bookNum = romanToInt(attr(b.attrs, 'n'));
    const argument = decodeEntities(attr(b.attrs, 'title')).replace(/\s+/g, ' ').trim();

    const chTags = [];
    const cre = /<div3\b([^>]*)>/g;
    let cm;
    while ((cm = cre.exec(b.html))) {
      if (/type="Chapter"/.test(cm[1])) chTags.push(cm.index);
    }
    const chapters = chTags.map((st, i) =>
      parseChapter(b.html.slice(st, i + 1 < chTags.length ? chTags[i + 1] : b.html.length), bookNum, disputes));

    const refs = chapters.reduce((a, c) => a + c.prooftexts.length, 0);
    const secs = chapters.reduce((a, c) => a + c.sections.length, 0);
    totCh += chapters.length; totSec += secs; totRefs += refs;
    chapters.forEach((c) => c.prooftexts.forEach((r) => { if (APOCRYPHA.has(r.split(' ')[0])) apoc++; }));

    const expect = EXPECT[bookNum];
    const ok = chapters.length === expect;
    if (!ok) problems.push('Book ' + bookNum + ': ' + chapters.length + ' chapters, expected ' + expect);
    // Integrity check that does not depend on an outside edition: chapter numbers must run
    // 1..N with no gaps or repeats, and every chapter must have a title and a body.
    chapters.forEach((c, i) => {
      if (c.n !== i + 1) problems.push('Book ' + bookNum + ': chapter in position ' + (i + 1) + ' is numbered ' + c.n + ' (gap or misparse)');
      if (!c.title) problems.push('Book ' + bookNum + ' ch. ' + c.n + ': no title');
      if (!c.sections.length) problems.push('Book ' + bookNum + ' ch. ' + c.n + ': no body');
      c.sections.forEach((sec) => {
        if (sec.paragraphs.some((p) => /^(Ibid|ibid)\b/.test(p) || /^[A-Z][a-z]{2}\.\s+[ivxlcdm]+\.\s*\d*\s*$/.test(p))) {
          problems.push('Book ' + bookNum + ' ch. ' + c.n + ': a footnote citation leaked into the body');
        }
      });
    });

    const doc = { work: "Augustine's Confessions", book: bookNum, argument: argument,
      chapters: chapters, translator: 'J.G. Pilkington (1876)',
      source: 'Nicene and Post-Nicene Fathers, Series I, Vol. 1, ed. Philip Schaff (1886) — CCEL ThML, public domain',
      version: '1.0' };
    if (!REPORT_ONLY) fs.writeFileSync(path.join(OUT, 'b' + bookNum + '.json'), JSON.stringify(doc, null, 2) + '\n');

    index.books.push({ number: bookNum, argument: argument, chapters: chapters.length,
      sections: secs, refs: refs, status: 'pilkington' });
    console.log('Book ' + String(bookNum).padStart(2) + ': ' + String(chapters.length).padStart(2) + ' chapters'
      + (ok ? ' (OK)' : ' (!! expected ' + expect + ')') + ', ' + String(secs).padStart(3) + ' sections, '
      + String(refs).padStart(3) + ' refs');
  });

  if (!REPORT_ONLY) fs.writeFileSync(path.join(OUT, 'index.json'), JSON.stringify(index, null, 2) + '\n');

  console.log('\nTOTAL: ' + totCh + ' chapters, ' + totSec + ' numbered sections, ' + totRefs + ' scripture refs');
  console.log('Apocrypha refs (no BTE target, will not auto-link): ' + apoc);
  console.log('\nREF RECONCILIATION — Pilkington\'s printed citation vs CCEL osisRef');
  console.log('  verifiable disagreements: ' + disputes.length);
  disputes.forEach((d) => console.log('  ' + (d.needsReview ? '?? ' : '   ') + d.where + ': printed "' + d.printed +
    '" (' + d.printedParsed + ')  vs osisRef ' + d.osis + '  ->  published as ' + d.resolved + '  [' + d.reason + ']'));
  const review = disputes.filter((d) => d.needsReview).length;
  console.log('  corrected from CCEL: ' + (disputes.length - review) + ' | needing a human look: ' + review);
  if (!REPORT_ONLY) fs.writeFileSync(path.join(OUT, 'ref-disputes.json'), JSON.stringify(disputes, null, 2) + '\n');

  console.log('\nVALIDATION: ' + (problems.length ? problems.length + ' problem(s)' : 'clean'));
  problems.slice(0, 20).forEach((p) => console.log('  !! ' + p));
  if (problems.length) process.exitCode = 1;
}
main();
