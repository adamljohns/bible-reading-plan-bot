#!/usr/bin/env node
/* verse-study-render.js — render a study page from a prose source file.
 *
 * Writing 71 studies as raw HTML means re-emitting the same head, nav, stylesheet
 * and section skeleton 71 times. That is a lot of tokens and a lot of chances to
 * fumble a tag, and it buries the only part that needs a mind — the prose — in
 * boilerplate. So the writer writes prose in content/verse-studies/<slug>.md and
 * this renders the page around it, pulling Scripture, the word study and the
 * page chrome from the same verified sources the scaffold uses.
 *
 * Source format (all sections optional except deck and the six headings):
 *
 *   @deck
 *   One or two sentences setting up the verse.
 *
 *   @section 1. The Text and Its Words
 *   Prose paragraphs, blank-line separated.
 *
 *   @word G2631
 *   What this word is doing in THIS verse. Script, transliteration and the
 *   lexicon definition are filled in automatically — write only the comment.
 *
 *   @section 3. What the Witnesses Saw
 *   @quote Calvin, Institutes III.11 | /institutes/b3-c11.html
 *   Verbatim text of the quotation, one paragraph per line-group.
 *   @endquote
 *   More prose.
 *
 *   @h3 A note on the longer reading
 *   Prose under a subheading.
 *
 * Everything the gate checks still applies: quotes are verified verbatim against
 * the local corpora, so a quotation typed here that Calvin never wrote fails.
 *
 * Usage:
 *   node bin/verse-study-render.js content/verse-studies/romans-8-1.md
 *   node bin/verse-study-render.js --all
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { buildKit, slugFor } = require('./verse-study-scaffold.js');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const SRC_DIR = path.join(ROOT, 'content', 'verse-studies');
const OUT_DIR = path.join(DOCS, 'drafts', 'verse');
const EXEMPLAR = path.join(DOCS, 'verse', 'genesis-1-1.html');

const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = (s) => esc(s).replace(/"/g, '&quot;');

/* Light inline markup only — the prose is prose, not a document format.
 * *emphasis*, _emphasis_, and "curly quotes" get typographic treatment. */
function inline(s) {
  let out = esc(s);
  out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>').replace(/(^|\s)_([^_]+)_/g, '$1<em>$2</em>');
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m, t, h) => `<a href="${escAttr(h)}">${t}</a>`);
  // Straight quotes to curly, apostrophes included. Site style: typographic glyphs.
  out = out.replace(/"([^"]*)"/g, '“$1”').replace(/(\w)'(\w)/g, '$1’$2');
  out = out.replace(/(^|[\s(])'([^']*)'/g, '$1‘$2’');
  out = out.replace(/\.\.\./g, '…').replace(/ -- /g, ' — ');
  return out;
}

function chrome() {
  const s = fs.readFileSync(EXEMPLAR, 'utf8');
  const grab = (re) => (s.match(re) || [''])[0];
  const abs = (x) => x.replace(/(href|src)="\.\.\//g, '$1="/');
  return {
    style: abs(grab(/<style>[\s\S]*?<\/style>/)),
    nav: abs(grab(/<nav[\s\S]*?<\/nav>/)),
    head: abs(grab(/<link rel="preconnect"[\s\S]*?<link rel="stylesheet" href="\/assets\/css\/print\.css" media="print">/)),
    script: [...s.matchAll(/<script>[\s\S]*?<\/script>/g)].map((m) => m[0]).join('\n').replace(/(href|src)="\.\.\//g, '$1="/'),
  };
}

/* ── source parsing ───────────────────────────────────────────────────────── */
function parseSource(text) {
  const doc = { ref: null, status: 'draft', deck: '', sections: [] };
  const lines = text.split('\n');
  let cur = null;          // current section
  let quote = null;        // open @quote block
  let buf = [];            // paragraph buffer

  const flush = () => {
    const para = buf.join('\n').trim();
    buf = [];
    if (!para || !cur) return;
    para.split(/\n\s*\n/).forEach((p) => cur.blocks.push({ type: 'p', text: p.replace(/\s*\n\s*/g, ' ').trim() }));
  };

  lines.forEach((raw) => {
    const line = raw.replace(/\s+$/, '');
    const dir = line.match(/^@(\w+)\s*(.*)$/);
    if (quote && (!dir || dir[1] !== 'endquote')) { quote.text.push(line); return; }
    if (!dir) { buf.push(line); return; }
    const [, key, rest] = dir;
    switch (key) {
      case 'ref': flush(); doc.ref = rest.trim(); break;
      case 'status': flush(); doc.status = rest.trim(); break;
      case 'deck': flush(); cur = { kind: 'deck', blocks: [] }; doc.sections.push(cur); break;
      case 'section': flush(); cur = { kind: 'section', title: rest.trim(), blocks: [] }; doc.sections.push(cur); break;
      case 'h3': flush(); if (cur) cur.blocks.push({ type: 'h3', text: rest.trim() }); break;
      case 'word': {
        flush();
        if (cur) cur.blocks.push({ type: 'word', code: rest.trim().split(/\s+/)[0], text: [] });
        break;
      }
      case 'quote': {
        flush();
        const [cite, href] = rest.split('|').map((x) => x.trim());
        quote = { type: 'quote', cite, href: href || '', text: [] };
        break;
      }
      case 'endquote': {
        if (quote && cur) {
          quote.paras = quote.text.join('\n').trim().split(/\n\s*\n/).map((p) => p.replace(/\s*\n\s*/g, ' ').trim()).filter(Boolean);
          delete quote.text;
          cur.blocks.push(quote);
        }
        quote = null;
        break;
      }
      default: buf.push(line);
    }
  });
  flush();

  // Prose that follows an @word belongs to that word, not the section.
  doc.sections.forEach((s) => {
    const blocks = [];
    let openWord = null;
    s.blocks.forEach((b) => {
      if (b.type === 'word') { openWord = b; blocks.push(b); return; }
      if (openWord && b.type === 'p') { openWord.text.push(b.text); return; }
      openWord = null;
      blocks.push(b);
    });
    s.blocks = blocks;
  });
  return doc;
}

/* ── rendering ────────────────────────────────────────────────────────────── */
function renderWord(block, kit) {
  const hit = kit.wordStudy.find((w) => w.lexicon && w.lexicon.code === block.code);
  if (!hit) return `  <!-- @word ${esc(block.code)}: not present in this verse's Strong's tags — check the code -->\n`;
  const lx = hit.lexicon;
  if (lx.stub) return `  <!-- @word ${esc(block.code)}: lexicon page is a stub, no usable definition. Refusing to render filler. -->\n`;
  const cls = kit.parsed.testament === 'OT' ? 'heb' : 'grk';
  const lang = kit.parsed.testament === 'OT' ? 'he' : 'el';
  const def = (lx.definition || '').split(/(?<=[.?!])\s+/).slice(0, 2).join(' ');
  const notes = block.text.map((t) => `      <p>${inline(t)}</p>`).join('\n');
  return `    <li>
      <div class="w"><span class="${cls}" lang="${lang}">${esc(lx.script)}</span> ${esc(lx.lemma)} <span class="strongs">· &ldquo;${esc(hit.word)}&rdquo; · <a href="${escAttr(lx.page)}">Strong&rsquo;s ${esc(lx.code)}</a>${lx.partOfSpeech ? ' · ' + esc(lx.partOfSpeech) : ''}</span></div>
      <p class="vs-def">${esc(def)}</p>
${notes}
    </li>`;
}

function renderSection(sec, kit) {
  const out = [];
  if (sec.kind === 'section') out.push(`  <h2>${inline(sec.title)}</h2>`);
  let wordRun = [];
  const flushWords = () => {
    if (!wordRun.length) return;
    out.push(`  <ul class="vs-words">\n${wordRun.join('\n')}\n  </ul>`);
    wordRun = [];
  };
  sec.blocks.forEach((b) => {
    if (b.type === 'word') { wordRun.push(renderWord(b, kit)); return; }
    flushWords();
    if (b.type === 'p') out.push(`  <p>${inline(b.text)}</p>`);
    else if (b.type === 'h3') out.push(`  <h3>${inline(b.text)}</h3>`);
    else if (b.type === 'quote') {
      const paras = b.paras.map((p) => `    <p>${inline(p)}</p>`).join('\n');
      const cite = b.href ? `<a href="${escAttr(b.href)}">${esc(b.cite)}</a>` : esc(b.cite);
      out.push(`  <blockquote class="vs-q">\n${paras}\n    <footer>${cite}</footer>\n  </blockquote>`);
    }
  });
  flushWords();
  return out.join('\n');
}

function render(doc, kit) {
  const c = chrome();
  const p = kit.parsed;
  const ref = kit.ref;
  const web = kit.texts.publicDomain.WEB || '';
  const kjv = kit.texts.publicDomain.KJV || '';
  const deckSec = doc.sections.find((s) => s.kind === 'deck');
  const deck = deckSec ? deckSec.blocks.filter((b) => b.type === 'p').map((b) => b.text).join(' ') : '';
  const body = doc.sections.filter((s) => s.kind === 'section').map((s) => renderSection(s, kit)).join('\n\n');
  const snippet = (web || kjv).replace(/\s+/g, ' ').slice(0, 150).replace(/\s+\S*$/, '');
  const isDraft = doc.status !== 'approved';
  const packs = kit.memorizePacks.map((x) => x.name);

  const goDeeper = `  <h2>Go Deeper</h2>
  <div class="vs-deeper">
    <a href="/bible.html?ref=${encodeURIComponent(ref)}">${esc(ref)} in the Translation Engine</a>
    <a href="/bible.html?ref=${encodeURIComponent(p.book + ' ' + p.ch)}">Read all of ${esc(p.book + ' ' + p.ch)}</a>
    <a href="/cross-references.html">Cross-Chain Reference Bible</a>
    <a href="/lexicon.html">Greek &amp; Hebrew Lexicon</a>
    <a href="/memorize.html">Memorize this verse</a>
    <a href="/verse/index.html">All Verse Studies</a>
  </div>`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/verse/${escAttr(kit.slug)}">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Deep study page — hand-authored exposition rendered from
         content/verse-studies/${escAttr(kit.slug.replace(/\.html$/, '.md'))} by bin/verse-study-render.js.
         verse-ref keeps bin/generate-verse-pages.js from overwriting it. -->
    <meta name="study-status" content="${escAttr(doc.status)}">
${isDraft ? '    <meta name="robots" content="noindex, nofollow">\n' : ''}    <meta name="verse-ref" content="${escAttr(ref)}">
    <meta name="verse-snippet" content="${escAttr(snippet)}">
    <title>${esc(ref)} — Verse Study${isDraft ? ' (draft)' : ''} | U.S.M.C. Ministries</title>
    <meta name="description" content="${escAttr(ref + ' — ' + (deck || 'a full verse study') + ' Word study, context, the Reformed witnesses, the confessional anchor, and application.').slice(0, 300)}">
    <meta property="og:title" content="${escAttr(ref + ' — Verse Study')}">
    <meta property="og:description" content="${escAttr(deck || snippet)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://usmcmin.org/verse/${escAttr(kit.slug)}">
    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${escAttr(ref + ' — Verse Study')}">
    <meta name="twitter:description" content="${escAttr(deck || snippet)}">
${c.head}
${c.style}
    <style>
      .vs-draft-banner { border:1px solid #b4553a; background:rgba(180,85,58,.12); color:#e39a80; border-radius:8px; padding:.55rem .9rem; font-size:.82rem; margin-bottom:1.2rem; }
      body.light-mode .vs-draft-banner { color:#8a3c22; }
      .vs-ctx { color:var(--gray); font-size:.94rem; border-left:2px solid rgba(212,175,55,.25); padding-left:.9rem; margin-bottom:.7rem; }
      .vs-def { color:var(--gray); font-size:.92rem; }
      .vs-words .grk { font-family:'Times New Roman',serif; font-size:1.2rem; margin-right:.35rem; }
      .vs-words .w a { color:inherit; text-decoration:none; }
      .vs-words .w a:hover { text-decoration:underline; }
    </style>
</head>
<body>
${c.nav}
<div class="container">
<div class="vs-wrap">
${isDraft ? `  <div class="vs-draft-banner">Draft — version 1. Written, not yet reviewed. Not indexed.</div>\n` : ''}  <div class="vs-eyebrow">Verse Study · ${esc(p.book)}</div>
  <h1>${esc(ref)}</h1>
${deck ? `  <p class="vs-deck">${inline(deck)}</p>\n` : ''}
  <div class="vs-text">
    <p>${esc(web)}<cite>— World English Bible (public domain)</cite></p>
  </div>
  <div class="vs-text">
    <p>${esc(kjv)}<cite>— King James Version (public domain)</cite></p>
  </div>

${body}

${packs.length ? `  <p class="vs-ctx">In the <strong>${esc(packs.join('</strong> and <strong>'))}</strong> memorize ${packs.length > 1 ? 'packs' : 'pack'} — <a href="/memorize.html">carry it</a>.</p>\n` : ''}
${goDeeper}

  <div class="vs-foot">
    <p>Every quotation on this page is checked verbatim against the source cited before it ships. Scripture shown in the World English Bible and the King James Version, both public domain. Free to copy, quote, and share.</p>
  </div>
</div>
</div>
${c.script}
</body>
</html>
`;
}

function renderFile(srcPath) {
  const text = fs.readFileSync(srcPath, 'utf8');
  const doc = parseSource(text);
  const slug = path.basename(srcPath).replace(/\.md$/, '');
  const ref = doc.ref || slug;
  const kit = buildKit(ref);
  if (kit.error) return { slug, error: `${ref}: ${kit.error} (add "@ref Book C:V" at the top)` };
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const outName = doc.status === 'approved' ? path.join(DOCS, 'verse', kit.slug) : path.join(OUT_DIR, kit.slug);
  fs.writeFileSync(outName, render(doc, kit));
  return { slug, ref: kit.ref, out: path.relative(ROOT, outName) };
}

function main() {
  let files = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  if (process.argv.includes('--all')) {
    files = fs.existsSync(SRC_DIR)
      ? fs.readdirSync(SRC_DIR).filter((f) => f.endsWith('.md')).map((f) => path.join(SRC_DIR, f))
      : [];
  }
  if (!files.length) { console.error('usage: verse-study-render.js <source.md> [...] | --all'); process.exit(2); }
  let ok = 0;
  const errs = [];
  files.forEach((f) => {
    const r = renderFile(f);
    if (r.error) { errs.push(r.error); return; }
    ok++;
    console.log(`rendered ${r.ref} -> ${r.out}`);
  });
  if (errs.length) { console.log('Errors:'); errs.forEach((e) => console.log('  - ' + e)); process.exitCode = 1; }
  console.log(`\n${ok}/${files.length} rendered.`);
}

if (require.main === module) main();
module.exports = { parseSource, render, renderFile };
