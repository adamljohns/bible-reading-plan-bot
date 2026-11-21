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
const crypto = require('crypto');
const { buildKit, slugFor } = require('./verse-study-scaffold.js');
// Adam 2026-11-20: drafts may be listed on the public index (labelled, noindex on
// the page); draft note is yellow at the bottom, never red.
const { DRAFT_NOTE_CSS, DRAFT_NOTE_HTML } = require('./verse-study-draft-note.js');

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
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
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
    script: [...s.matchAll(/<script(?:\s+defer)?(?:\s+src="[^"]*")?>[\s\S]*?<\/script>/g)].map((m) => m[0]).join('\n').replace(/(href|src)="\.\.\//g, '$1="/'),
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
      // Adam 2026-11-21: approved studies carry "Version 1.0 · Reviewed by Moop".
      case 'version': flush(); doc.version = rest.trim(); break;
      case 'reviewed': flush(); doc.reviewed = rest.trim(); break;
      case 'deck': flush(); cur = { kind: 'deck', blocks: [] }; doc.sections.push(cur); break;
      case 'section': flush(); cur = { kind: 'section', title: rest.trim(), blocks: [] }; doc.sections.push(cur); break;
      case 'h3': flush(); if (cur) cur.blocks.push({ type: 'h3', text: rest.trim() }); break;
      case 'word': {
        flush();
        // "@word H8159 | dismayed" — the optional label overrides the English word
        // shown. The KJV's Strong's tags sometimes span a whole clause rather than
        // the single word ("thou not; for I am with thee: be not dismayed"), and
        // printing that verbatim looks like a bug on the page.
        const [codePart, labelPart] = rest.split('|').map((x) => x.trim());
        if (cur) cur.blocks.push({ type: 'word', code: codePart.split(/\s+/)[0], label: labelPart || '', text: [] });
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
/* ── narration hooks ──────────────────────────────────────────────────────────
 * Every study carries these inert attributes so bin/generate-study-audio.py can
 * narrate it and read-scroll.js can follow it, audio or not:
 *   data-read-follow   the follow root (its id keys the words file)
 *   data-no-follow     on the page but not read aloud (WEB text, citations)
 *   data-say           what an element says instead of its text
 *   data-say-before    a spoken line before an element (quote attributions)
 *   data-voice="book"  read in the book's Scripture voice, like the watches
 */
function spokenAttribution(cite) {
  const c = String(cite || '').trim();
  let m;
  if ((m = c.match(/^1689 LBCF, ch\. ?(\d+)(?:\s*[—–-]\s*(.+))?$/))) {
    return `The 1689 Confession, chapter ${m[1]}${m[2] ? ', ' + m[2].trim() + ',' : ''} says:`;
  }
  if (/^(The )?Baptist Catechism/i.test(c)) return 'The Baptist Catechism answers:';
  if (/^Calvin, Institutes/.test(c)) return 'Calvin writes in the Institutes:';
  if (/^Calvin, Commentary/.test(c)) return 'Calvin writes in his commentary:';
  if (/^\d?\s?[A-Z][a-z]+(?: [A-Z][a-z]+)* \d+:\d+/.test(c)) return `${c} reads:`;
  const who = c.split(',')[0].trim();
  return who ? `${who} writes:` : 'It is written:';
}

/* The player is included only when a words file exists for the slug. That file
 * is written by bin/generate-study-audio.py and names the R2 audio URL. */
function audioFor(slug) {
  const f = path.join(DOCS, 'assets', 'studies', `${slug.replace(/\.html$/, '')}-words.json`);
  if (!fs.existsSync(f)) return null;
  try {
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    if (!d.audio || !d.duration) return null;
    const v = (String(d.audio).match(/[?&]v=([\w-]+)/) || [])[1] || '';
    return { audio: d.audio, duration: d.duration, words: `/assets/studies/${path.basename(f)}${v ? '?v=' + v : ''}` };
  } catch (e) {
    return null;
  }
}

function fmtMin(secs) {
  return `${Math.round(secs / 60)} min`;
}

function renderPlayer(a, ref) {
  return `  <div class="audio-slot vs-audio" data-no-follow data-follow-player data-read-scroll-anchor>
    <audio class="watch-audio" controls preload="metadata" style="width:100%;">
      <source src="${escAttr(a.audio)}" type="audio/mpeg">
      Your browser does not support audio.
    </audio>
    <div class="audio-speed" role="group" aria-label="Playback speed">
      <button type="button" class="audio-speed-btn is-active" data-rate="1" aria-pressed="true">1&times;</button>
      <button type="button" class="audio-speed-btn" data-rate="1.25" aria-pressed="false">1.25&times;</button>
      <button type="button" class="audio-speed-btn" data-rate="1.5" aria-pressed="false">1.5&times;</button>
      <button type="button" class="audio-speed-btn" data-rate="2" aria-pressed="false">2&times;</button>
    </div>
    <div class="audio-cap">Listen to this study &middot; ${esc(fmtMin(a.duration))} &middot; the words light up as they are read</div>
  </div>`;
}

function renderWord(block, kit) {
  const hit = kit.wordStudy.find((w) => w.lexicon && w.lexicon.code === block.code);
  if (!hit) return `  <!-- @word ${esc(block.code)}: not present in this verse's Strong's tags — check the code -->\n`;
  const lx = hit.lexicon;
  if (lx.stub) return `  <!-- @word ${esc(block.code)}: lexicon page is a stub, no usable definition. Refusing to render filler. -->\n`;
  const cls = kit.parsed.testament === 'OT' ? 'heb' : 'grk';
  const lang = kit.parsed.testament === 'OT' ? 'he' : 'el';
  const def = (lx.definition || '').split(/(?<=[.?!])\s+/).slice(0, 2).join(' ');
  const notes = block.text.map((t) => `      <p>${inline(t)}</p>`).join('\n');
  const say = `${lx.lemma}, rendered “${block.label || hit.word}”.`;
  return `    <li>
      <div class="w" data-say="${escAttr(say)}"><span class="${cls}" lang="${lang}" data-no-follow>${esc(lx.script)}</span> ${esc(lx.lemma)} <span class="strongs">· &ldquo;${esc(block.label || hit.word)}&rdquo; · <a href="${escAttr(lx.page)}">Strong&rsquo;s ${esc(lx.code)}</a>${lx.partOfSpeech ? ' · ' + esc(lx.partOfSpeech) : ''}</span></div>
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
      out.push(`  <blockquote class="vs-q" data-say-before="${escAttr(spokenAttribution(b.cite))}">\n${paras}\n    <footer data-no-follow>${cite}</footer>\n  </blockquote>`);
    }
  });
  flushWords();
  return out.join('\n');
}

/* Share card + PDF (Adam 2026-11-21). If docs/assets/verse-cards/<slug>.png or
 * docs/assets/verse-pdfs/<slug>.pdf exists, the page shows it under the deck.
 * The ?v= is a content hash so a redrawn card or reprinted PDF busts the cache. */
function cardAndPdf(slug) {
  const base = slug.replace(/\.html$/, '');
  const ver = (f) => crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex').slice(0, 10);
  const card = path.join(DOCS, 'assets', 'verse-cards', base + '.png');
  const pdf = path.join(DOCS, 'assets', 'verse-pdfs', base + '.pdf');
  const links = [];
  let img = '';
  if (fs.existsSync(card)) {
    const u = `/assets/verse-cards/${base}.png?v=${ver(card)}`;
    img = `    <img src="${u}" alt="${esc(base)} verse card" width="1080" height="1350">\n`;
    links.push(`<a href="${u}" download>Save / Share PNG</a>`);
  }
  if (fs.existsSync(pdf)) links.push(`<a href="/assets/verse-pdfs/${base}.pdf?v=${ver(pdf)}" download>Download PDF</a>`);
  if (!links.length) return '';
  return `  <figure class="vs-verse-card">\n${img}    <figcaption>${links.join(' &middot; ')}</figcaption>\n  </figure>\n`;
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
  const audio = audioFor(kit.slug);
  const FP_V = '20261120a';
  const audioHead = audio ? `    <meta name="read-follow-words" content="${escAttr(audio.words)}">
    <meta name="read-follow-docks" content="bottom">
    <link rel="stylesheet" href="/assets/css/follow-player.css?v=${FP_V}">
` : '';
  const audioScripts = audio ? `
<script defer src="/assets/js/follow-player.js?v=${FP_V}"></script>
<script defer src="/assets/js/read-scroll.js?v=${FP_V}"></script>` : '';

  const goDeeper = `  <h2>Go Deeper</h2>
  <div class="vs-deeper">
    <a href="/bible.html?ref=${encodeURIComponent(ref)}">${esc(ref)} in the Translation Engine</a>
    <a href="/bible.html?ref=${encodeURIComponent(p.book + ' ' + p.ch)}">Read all of ${esc(p.book + ' ' + p.ch)}</a>
    <a href="/cross-references.html">Cross-Chain Reference Bible</a>
    <a href="/lexicon.html">Greek &amp; Hebrew Lexicon</a>
    <a href="/memorize.html">Memorize this verse</a>
    <a href="/verse/index.html">All Verse Studies</a>
    <a href="/verse/method/">How these studies are built</a>
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
${audioHead}${c.head}
${c.style}
    <style>
${isDraft ? DRAFT_NOTE_CSS : ''}      .vs-ctx { color:var(--gray); font-size:.94rem; border-left:2px solid rgba(212,175,55,.25); padding-left:.9rem; margin-bottom:.7rem; }
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
  <div class="vs-eyebrow">Verse Study · ${esc(p.book)}</div>
  <div class="vs-read" id="study" data-read-follow>
  <h1>${esc(ref)}</h1>
${deck ? `  <p class="vs-deck">${inline(deck)}</p>\n` : ''}${cardAndPdf(kit.slug)}${audio ? renderPlayer(audio, ref) + '\n' : ''}
  <div class="vs-text" data-voice="book" data-say-before="The King James Version reads:">
    <p>${esc(kjv)}<cite data-no-follow>— King James Version (public domain)</cite></p>
  </div>
  <div class="vs-text" data-no-follow>
    <p>${esc(web)}<cite>— World English Bible (public domain)</cite></p>
  </div>

${body}
  </div>

${packs.length ? `  <p class="vs-ctx">In the ${packs.map((n) => `<strong>${esc(n)}</strong>`).join(' and ')} memorize ${packs.length > 1 ? 'packs' : 'pack'} — <a href="/memorize.html">carry it</a>.</p>\n` : ''}
${goDeeper}

  <div class="vs-foot">
    <p>Every quotation on this page is checked verbatim against the source cited before it ships. Scripture shown in the King James Version and the World English Bible, both public domain. Free to copy, quote, and share.</p>${doc.version || doc.reviewed ? `\n    <p class="vs-version">${[doc.version ? 'Version ' + esc(doc.version) : '', doc.reviewed ? 'Reviewed by ' + esc(doc.reviewed) : ''].filter(Boolean).join(' · ')}</p>` : ''}
  </div>
${isDraft ? DRAFT_NOTE_HTML : ''}</div>
</div>
${c.script}${audioScripts}
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
