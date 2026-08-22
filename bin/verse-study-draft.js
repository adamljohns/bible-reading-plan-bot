#!/usr/bin/env node
/* verse-study-draft.js — emit a v1 draft deep-study page from a scaffold kit.
 *
 * What this does and does not do matters. It fills in everything that can be
 * derived from the repo with certainty — verse text, the original-language line,
 * the word study with real lexicon definitions, surrounding context, cross
 * references, the Go Deeper pills, memorize-pack membership — and it leaves the
 * prose to a writer.
 *
 * It deliberately does NOT auto-insert the confessional and Institutes quotes the
 * scaffold turned up. Those are keyword matches; dropping one into the page
 * unread is how you end up quoting half a sentence of Calvin that argues the
 * opposite of your paragraph. They go into an HTML comment for the writer to
 * read and choose from. The whole point of this pipeline is that a quotation is
 * something a mind selected, not something a regex did.
 *
 * Drafts are written to drafts/verse/ with study-status=draft and robots=noindex,
 * so an unreviewed draft cannot leak into the live index or search results.
 *
 * Usage:
 *   node bin/verse-study-draft.js /tmp/vs-kits/romans-8-1.json
 *   node bin/verse-study-draft.js /tmp/vs-kits/*.json
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const EXEMPLAR = path.join(DOCS, 'verse', 'genesis-1-1.html');
/* Drafts live under docs/ so Adam can open one on his phone, but they carry
 * noindex+nofollow, are disallowed in robots.txt, and are linked from nothing.
 * Reachable by URL, invisible to search, absent from the verse index. */
const OUT_DIR = path.join(DOCS, 'drafts', 'verse');

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = (s) => esc(s).replace(/"/g, '&quot;');

/* Nav and CSS are lifted from the approved exemplar at generation time so drafts
 * inherit chrome changes instead of drifting into a second house style. */
function chromeFromExemplar() {
  const s = fs.readFileSync(EXEMPLAR, 'utf8');
  const style = (s.match(/<style>[\s\S]*?<\/style>/) || [])[0] || '';
  const nav = (s.match(/<nav[\s\S]*?<\/nav>/) || [])[0] || '';
  const head = (s.match(/<link rel="preconnect"[\s\S]*?<link rel="stylesheet" href="\/assets\/css\/print\.css" media="print">/) || [])[0] || '';
  const script = [...s.matchAll(/<script>[\s\S]*?<\/script>/g)].map((m) => m[0]).join('\n');
  // Rewrite ../ to root-absolute so the same markup works at docs/drafts/verse/
  // and, once approved, at docs/verse/ — no link rot on promotion.
  const abs = (x) => x.replace(/(href|src)="\.\.\//g, '$1="/');
  return { style: abs(style), nav: abs(nav), head: abs(head), script: abs(script) };
}

const TODO = (what) => `  <p class="vs-todo">[WRITE — ${esc(what)}]</p>`;

function contextVerses(k) {
  const p = k.parsed;
  const fp = path.join(DOCS, 'assets', 'chapters', `${p.bookId}_${p.ch}.json`);
  if (!fs.existsSync(fp)) return { before: '', after: '' };
  const web = (JSON.parse(fs.readFileSync(fp, 'utf8')).WEB) || {};
  const clean = (s) => String(s || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  return { before: clean(web[String(p.v1 - 1)]), after: clean(web[String(p.v2 + 1)]) };
}

function wordStudyHtml(k) {
  const usable = k.wordStudy.filter((w) => w.priority === 'content' && w.lexicon && !w.lexicon.stub);
  const picks = usable.slice(0, 5);
  if (!picks.length) return '  <!-- No non-stub lexicon entries for this verse. Build the word study from context, or leave it out. -->\n';
  const cls = k.parsed.testament === 'OT' ? 'heb' : 'grk';
  const lang = k.parsed.testament === 'OT' ? 'he' : 'el';
  const items = picks.map((w) => {
    const lx = w.lexicon;
    const def = (lx.definition || '').split(/(?<=[.?!])\s+/).slice(0, 2).join(' ');
    // The script shown is the lexicon's dictionary form, labelled as such — the
    // inflected form in the verse itself is not something this repo stores.
    return `    <li>
      <div class="w"><span class="${cls}" lang="${lang}">${esc(lx.script)}</span> ${esc(lx.lemma)} <span class="strongs">· ${esc(w.word)} · Strong's ${esc(lx.code)}${lx.partOfSpeech ? ' · ' + esc(lx.partOfSpeech) : ''}</span></div>
      <p>${esc(def)}</p>
${TODO(`what "${w.word}" is doing in this verse specifically — not a dictionary entry`)}
    </li>`;
  }).join('\n');
  const stubbed = k.wordStudy.filter((w) => w.priority === 'content' && w.lexicon && w.lexicon.stub);
  const stubNote = stubbed.length
    ? `  <!-- Stub lexicon pages, unusable — do not quote or paraphrase these: ${stubbed.map((w) => `${w.strongs} (${w.word})`).join(', ')} -->\n`
    : '';
  return `${stubNote}  <ul class="vs-words">\n${items}\n  </ul>\n`;
}

/* The one class of quote this script will insert on its own. A proof-text hit is
 * not a keyword coincidence: it is a whole numbered paragraph that the confession
 * itself cites this very verse to support. It is quoted verbatim from the local
 * file, so the gate can confirm it. Everything else stays in a comment for a
 * human to choose. */
function proofTextHtml(k) {
  const hits = (k.proofTexts || []).slice(0, 2);
  if (!hits.length) return '  <!-- No LBCF/Catechism paragraph cites this verse as a proof-text. Pick an anchor by doctrine instead, from the candidates at the foot of this file. -->\n';
  return hits.map((h) => {
    // Keep it to a readable pull; the link carries the reader to the whole paragraph.
    const sentences = h.quote.split(/(?<=[.?!])\s+/);
    let quote = '';
    for (const s of sentences) { if ((quote + ' ' + s).trim().length > 520) break; quote = (quote + ' ' + s).trim(); }
    if (!quote) quote = h.quote.slice(0, 520);
    return `  <blockquote class="vs-q">
    <p>${esc(quote)}</p>
    <footer><a href="${escAttr(h.href)}">${esc(h.source)}</a> — cites ${esc(h.why.replace(/^cites /, ''))}</footer>
  </blockquote>\n`;
  }).join('');
}

function sourceCandidatesComment(k) {
  const lines = [];
  const add = (label, arr) => {
    if (!arr || !arr.length) return;
    lines.push(`  ${label}:`);
    arr.forEach((s) => lines.push(`    - [${s.source}] ${s.quote.replace(/--/g, '- -').slice(0, 320)}`));
  };
  add('1689 LBCF candidates', k.sources.lbcf);
  add('Baptist Catechism candidates', k.sources.catechism);
  add('Calvin, Institutes candidates', k.sources.institutes);
  if (!lines.length) return '';
  return `<!-- QUOTE CANDIDATES — keyword matches from the local corpora, NOT vetted.
  Read each one in its own chapter before using it. A match is not an argument;
  half a sentence can say the opposite of the whole. Quote verbatim, attribute in
  a <footer>, and let bin/verse-study-gate.js confirm it.

${lines.join('\n')}
-->`;
}

function crossRefsHtml(k) {
  const xs = k.crossReferences.filter((x) => x.text).slice(0, 6);
  if (!xs.length) return '';
  return `  <ul class="vs-words">\n${xs.map((x) => `    <li><div class="w">${esc(x.ref)}</div><p>${esc(x.text)}</p></li>`).join('\n')}\n  </ul>\n`;
}

function build(k) {
  const c = chromeFromExemplar();
  const ref = k.ref;
  const p = k.parsed;
  const web = k.texts.publicDomain.WEB || '';
  const kjv = k.texts.publicDomain.KJV || '';
  const snippet = (web || kjv).slice(0, 155).replace(/\s+\S*$/, '');
  const ctx = contextVerses(k);
  /* No auto-generated original-language line. The repo stores Strong's numbers,
   * which resolve to dictionary *lemmas* — stringing them together produces
   * "ἄρα νῦν κατάκριμα ἐν Χριστός Ἰησοῦς…", which looks like the Greek of
   * Romans 8:1 and is not: wrong cases, wrong forms, wrong word order. A reader
   * who knows Greek sees nonsense; a reader who doesn't is misled. If a study
   * wants the original line, a writer types it from a real text by hand. */
  const origLine = '  <!-- No original-language line: the repo has lemmas, not the inflected text. Add one by hand from a real edition, or leave it out. -->\n';
  const packs = k.memorizePacks.map((x) => x.name);
  const chLink = `/bible.html?ref=${encodeURIComponent(p.book + ' ' + p.ch)}`;
  const vLink = `/bible.html?ref=${encodeURIComponent(ref)}`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/verse/${escAttr(k.slug)}">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Deep study page (hand-authored exposition, not the generated landing shell).
         bin/add-verse-page.js reads verse-ref/verse-snippet for the index; the SSG baker skips it. -->
    <meta name="study-status" content="draft">
    <meta name="robots" content="noindex, nofollow">
    <meta name="verse-ref" content="${escAttr(ref)}">
    <meta name="verse-snippet" content="${escAttr(snippet)}">
    <title>${esc(ref)} — Verse Study (draft) | U.S.M.C. Ministries</title>
    <meta name="description" content="${escAttr(ref + ' — a full verse study: the ' + p.tongue + ' behind the words, where the verse sits, the confessional anchor, and what it means for the man reading it.')}">
    <meta property="og:title" content="${escAttr(ref + ' — Verse Study')}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://usmcmin.org/verse/${escAttr(k.slug)}">
    <meta property="og:image" content="https://usmcmin.org/assets/og/og-bible.png">
    <meta name="twitter:card" content="summary_large_image">
${c.head}
${c.style}
    <style>
      /* Draft-only chrome. All of it disappears when the study is finished:
         the banner and the [WRITE] slots are removed, and the gate refuses an
         approved page that still contains a vs-todo. */
      .vs-draft-banner { border:1px solid #b4553a; background:rgba(180,85,58,.12); color:#e39a80; border-radius:8px; padding:.55rem .9rem; font-size:.82rem; letter-spacing:.02em; margin-bottom:1.2rem; }
      .vs-todo { border-left:3px solid #b4553a; background:rgba(180,85,58,.07); padding:.5rem .85rem; margin:.5rem 0 1rem; color:#d99a83; font-size:.9rem; font-style:italic; }
      .vs-ctx { color:var(--gray); font-size:.94rem; border-left:2px solid rgba(212,175,55,.25); padding-left:.9rem; margin-bottom:.7rem; }
      .vs-grk { direction:ltr; font-family:'Times New Roman',serif; }
      .vs-words .grk { font-family:'Times New Roman',serif; font-size:1.2rem; margin-right:.35rem; }
      body.light-mode .vs-draft-banner { color:#8a3c22; }
      body.light-mode .vs-todo { color:#8a3c22; }
    </style>
</head>
<body>
${c.nav}
<div class="container">
<div class="vs-wrap">
  <div class="vs-draft-banner">Draft — version 1. Not reviewed, not indexed, not linked from the verse index.</div>
  <div class="vs-eyebrow">Verse Study · ${esc(p.book)}</div>
  <h1>${esc(ref)}</h1>
${TODO('the deck — one or two sentences that give the reader the point of this verse before they read a word of exposition. Model: "Seven words in Hebrew. Everything else in Scripture stands on them."')}

  <div class="vs-text">
    <p>${esc(web)}<cite>— World English Bible (public domain)</cite></p>
  </div>
  <div class="vs-text">
    <p>${esc(kjv)}<cite>— King James Version (public domain)</cite></p>
  </div>
${origLine}
  <h2>1. The Text and Its Words</h2>
${TODO('open the exposition — what is this verse actually claiming, and what does the sentence assume that the reader may not have noticed')}
${wordStudyHtml(k)}
  <h2>2. Where It Sits</h2>
${ctx.before ? `  <p class="vs-ctx"><strong>${esc(p.book)} ${p.ch}:${p.v1 - 1}</strong> — ${esc(ctx.before)}</p>\n` : ''}${ctx.after ? `  <p class="vs-ctx"><strong>${esc(p.book)} ${p.ch}:${p.v2 + 1}</strong> — ${esc(ctx.after)}</p>\n` : ''}${TODO('the argument of the surrounding paragraph, the book, and why this verse lands where it does')}
${crossRefsHtml(k)}
  <h2>3. What the Witnesses Saw</h2>
${TODO('the Reformed reading. Quote ONLY what you can verify — Institutes chapters are local; anything else must be registered in data/verse-study-sources.json with verified:true. If a quote will not verify, summarize the argument in your own prose and drop the quotation marks.')}

  <h2>4. Confessional Anchor</h2>
${proofTextHtml(k)}${TODO('tie the confession to the verse — why the divines reached for this text here, and what it settles for the reader')}

  <h2>5. For the Man Reading This</h2>
${packs.length ? `  <p>This verse is in the ${packs.map((n) => `<strong>${esc(n)}</strong>`).join(' and ')} memorize ${packs.length > 1 ? 'packs' : 'pack'}${packs.length ? ` — <a href="/memorize.html">carry it</a>` : ''}.</p>\n` : ''}${TODO('application. Concrete, costly, unsentimental. What does believing this change on a Tuesday? No pep talk, no guilt.')}

  <h2>6. Go Deeper</h2>
  <div class="vs-deeper">
    <a href="${escAttr(vLink)}">${esc(ref)} in the Translation Engine</a>
    <a href="${escAttr(chLink)}">Read all of ${esc(p.book + ' ' + p.ch)}</a>
    <a href="/cross-references.html">Cross-Chain Reference Bible</a>
    <a href="/lexicon.html">Greek &amp; Hebrew Lexicon</a>
    <a href="/memorize.html">Memorize this verse</a>
    <a href="/verse/index.html">All Verse Studies</a>
  </div>

  <div class="vs-foot">
    <p>Scripture shown in the World English Bible and the King James Version, both public domain. Free to copy, quote, and share.</p>
  </div>
</div>
</div>
${sourceCandidatesComment(k)}
${c.script}
</body>
</html>
`;
}

function main() {
  const files = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  if (!files.length) {
    console.error('usage: verse-study-draft.js <kit.json> [...]');
    process.exit(2);
  }
  fs.mkdirSync(OUT_DIR, { recursive: true });
  let written = 0, skipped = 0;
  files.forEach((f) => {
    const k = JSON.parse(fs.readFileSync(f, 'utf8'));
    const out = path.join(OUT_DIR, k.slug);
    // Never clobber a draft someone has started writing.
    if (fs.existsSync(out) && !/vs-todo/.test(fs.readFileSync(out, 'utf8'))) {
      console.log(`skip (already written): drafts/verse/${k.slug}`);
      skipped++;
      return;
    }
    fs.writeFileSync(out, build(k));
    written++;
  });
  console.log(`Drafts written: ${written}${skipped ? `, skipped ${skipped} already-written` : ''} -> drafts/verse/`);
}

if (require.main === module) main();
module.exports = { build };
