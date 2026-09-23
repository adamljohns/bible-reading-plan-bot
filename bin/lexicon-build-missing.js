/**
 * lexicon-build-missing.js — create the lexicon entries that other pages link to
 * but that do not exist.
 *
 * 1,327 Strong's codes are linked from live lexicon pages and have no page of
 * their own. That is what fails ~1,600 pages on "dead local link". Cutting the
 * links would clear the gate and shrink the lexicon; building the entries clears
 * the gate and grows it. This builds them.
 *
 * NOTHING HERE IS INVENTED. Every field comes from data already in the repo:
 *   headword, transliteration, gloss, derivation  <- bin/baselines/strongs-*.json
 *                                                    (vendored Open Scriptures)
 *   every cited verse                             <- docs/assets/chapters/*.json,
 *                                                    the KJV tagged <S>NNNN</S>
 *
 * A verse is only cited if its chapter file really carries the code, so the
 * gate's own test is satisfied by construction rather than by hope. The page
 * shell is cloned from a page that already passes, so the theme-toggle, social
 * metadata and broken-link gates are satisfied too. "Related Words" is dropped
 * on purpose — it is the only block on these pages that can carry a dead link.
 *
 * RUN THIS IN AN ISOLATED WORKTREE. ~/bible-reading-plan-bot-autopilot is the
 * directory grind's live checkout and it hard-resets to FETCH_HEAD between
 * rounds, which deletes untracked files out from under you.
 *
 * Usage:
 *   node bin/lexicon-build-missing.js --list
 *   node bin/lexicon-build-missing.js [--limit N] [--out DIR]
 */
const fs = require('fs');
const path = require('path');
const REPO = path.join(__dirname, '..');
const LEX = path.join(REPO, 'docs', 'lexicon');
const CH = path.join(REPO, 'docs', 'assets', 'chapters');
const { BOOK_IDS } = require('./verse-study-scaffold.js');

const greek = JSON.parse(fs.readFileSync(path.join(__dirname, 'baselines/strongs-greek.json'), 'utf8'));
const hebrew = JSON.parse(fs.readFileSync(path.join(__dirname, 'baselines/strongs-hebrew.json'), 'utf8'));

const NAME_BY_ID = {};
for (const [name, id] of Object.entries(BOOK_IDS)) {
  const pretty = name.replace(/\b\w/g, (c) => c.toUpperCase());
  if (!NAME_BY_ID[id] || pretty.length > NAME_BY_ID[id].length) NAME_BY_ID[id] = pretty;
}

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const plain = (s) => String(s == null ? '' : s).replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
const WORDS = (s) => plain(s).split(/\s+/).filter(Boolean).length;

function existing() {
  return new Set(fs.readdirSync(LEX).filter((f) => f.endsWith('.html')).map((f) => f.slice(0, -5)));
}

function missingTargets() {
  const have = existing();
  const want = new Map();
  for (const f of fs.readdirSync(LEX)) {
    if (!f.endsWith('.html')) continue;
    const html = fs.readFileSync(path.join(LEX, f), 'utf8');
    for (const m of new Set(html.match(/href="[GH]\d+\.html"/g) || [])) {
      const code = m.slice(6, -6);
      if (!have.has(code)) want.set(code, (want.get(code) || 0) + 1);
    }
  }
  return want;
}

let INDEX = null;
function buildIndex() {
  if (INDEX) return INDEX;
  INDEX = new Map();
  for (const f of fs.readdirSync(CH)) {
    const m = f.match(/^(\d+)_(\d+)\.json$/);
    if (!m) continue;
    const id = +m[1], ch = +m[2];
    // The tagged KJV writes bare numbers; the testament decides G or H, exactly
    // as bin/lexicon-gate.js decides it. id <= 39 is Old Testament.
    const prefix = id <= 39 ? 'H' : 'G';
    let data;
    try { data = JSON.parse(fs.readFileSync(path.join(CH, f), 'utf8')); } catch { continue; }
    if (!data || !data.KJV) continue;
    for (const [vs, text] of Object.entries(data.KJV)) {
      for (const s of new Set(String(text).match(/<S>\d+<\/S>/g) || [])) {
        const code = prefix + s.slice(3, -4);
        if (!INDEX.has(code)) INDEX.set(code, []);
        INDEX.get(code).push({ id, ch, vs: +vs });
      }
    }
  }
  return INDEX;
}

function chapterText(id, ch, vs) {
  try {
    const d = JSON.parse(fs.readFileSync(path.join(CH, `${id}_${ch}.json`), 'utf8'));
    return (d && d.KJV && d.KJV[String(vs)]) || null;
  } catch { return null; }
}

/** Drop the <S> tags, italicising the word this code actually marks. */
function renderVerse(raw, num) {
  let out = String(raw);
  out = out.replace(new RegExp('([A-Za-z’\'-]+)<S>' + num + '</S>', 'g'), '<em>$1</em>');
  return out.replace(/<S>\d+<\/S>/g, '').replace(/\s+([,.;:!?])/g, '$1').replace(/\s+/g, ' ').trim();
}

/** Up to n citations, spread over as many different books as possible. */
function pickVerses(code, n) {
  const byBook = new Map();
  for (const h of buildIndex().get(code) || []) {
    if (!byBook.has(h.id)) byBook.set(h.id, []);
    byBook.get(h.id).push(h);
  }
  const books = [...byBook.keys()].sort((a, b) => a - b);
  const out = [];
  for (let round = 0; out.length < n && round < 40; round++) {
    let added = false;
    for (const b of books) {
      const list = byBook.get(b);
      if (list.length > round) { out.push(list[round]); added = true; }
      if (out.length >= n) break;
    }
    if (!added) break;
  }
  return out;
}

function buildPage(code, shell) {
  const prefix = code[0];
  const num = code.slice(1);
  const entry = (prefix === 'G' ? greek : hebrew)[code];
  if (!entry) return null;
  const lemma = plain(entry.lemma);
  // The vendored sets disagree on the field name: the Greek file uses
  // `translit`, the Hebrew file uses `xlit`. Reading only the first left 620
  // Hebrew pages with an empty transliteration and failing the gate.
  const translit = plain(entry.translit || entry.xlit || entry.pron);
  if (!lemma || !translit) return null;

  const hits = buildIndex().get(code) || [];
  if (!hits.length) return null;
  const bookIds = [...new Set(hits.map((h) => h.id))].sort((a, b) => a - b);
  const bookNames = bookIds.map((i) => NAME_BY_ID[i]).filter(Boolean);
  const lang = prefix === 'G' ? 'Greek' : 'Hebrew';
  const testament = prefix === 'G' ? 'New Testament' : 'Old Testament';

  const clean = (s) => plain(s).replace(/^[;:,\s]+/, '').replace(/[;\s]+$/, '');
  const sdef = clean(entry.strongs_def);
  const kjv = clean(entry.kjv_def);
  const deriv = clean(entry.derivation);

  const bits = [`<em>${esc(translit)}</em> (${esc(lemma)}) is ${lang} Strong's ${esc(code)}.`];
  if (sdef) bits.push(`Strong's defines it as ${esc(sdef.replace(/\.$/, ''))}.`);
  if (deriv) bits.push(`Strong's traces the form: ${esc(deriv)}.`);
  if (kjv) bits.push(`The Authorised Version renders it ${esc(kjv.replace(/\.$/, ''))}.`);
  bits.push(`The tagged KJV carries this code ${hits.length} time${hits.length === 1 ? '' : 's'}` +
    (bookNames.length
      ? `, across ${bookNames.length} book${bookNames.length === 1 ? '' : 's'}: ` +
        `${esc(bookNames.slice(0, 8).join(', '))}${bookNames.length > 8 ? ', and others' : ''}.`
      : '.'));

  const verses = pickVerses(code, 5).map((h) => {
    const raw = chapterText(h.id, h.ch, h.vs);
    if (!raw) return null;
    return { ref: `${NAME_BY_ID[h.id]} ${h.ch}:${h.vs}`, text: renderVerse(raw, num) };
  }).filter(Boolean);
  if (!verses.length) return null;

  // Strictly what the tagging shows, so the usage section cannot be "invented".
  const usage =
    `Every verse below is one the tagged KJV marks with ${esc(code)}, so each is a place the ` +
    `${lang} word itself stands behind the English rather than a translator's paraphrase. ` +
    `The first is ${esc(verses[0].ref)}. ` +
    (bookNames.length > 1
      ? `The code is spread over ${bookNames.length} books, which is worth weighing before treating any single rendering as the whole sense of the word. `
      : `It appears in one book only, ${esc(bookNames[0] || '')}, so its range in Scripture is narrow. `) +
    `Where the Authorised Version gives more than one English word for it, that difference is the ` +
    `translators' judgement about context, not a second ${lang} word underneath.`;

  const versesHtml = verses.map((v) =>
    `                <div class="verse-entry">\n` +
    `                    <a href="../bible.html?ref=${encodeURIComponent(v.ref).replace(/%20/g, '+')}" class="verse-ref">${esc(v.ref)}</a>\n` +
    `                    <span class="verse-text">${v.text}</span>\n` +
    `                </div>`).join('\n');

  const block =
`<div class="word-header">
            <span class="strongs-badge">${esc(code)} · ${lang} · ${testament}</span>
            <div class="original-word">${esc(lemma)}</div>
            <div class="transliteration">${esc(translit)}</div>
            <div class="gloss">${esc(kjv || sdef || '')}</div>
        </div>
        <div class="section">
            <h2>Definition</h2>
            <p>${bits.join(' ')}</p>
        </div>
        <div class="section">
            <h2>Usage &amp; Theological Significance</h2>
            <p>${usage}</p>
        </div>
        <div class="section">
            <h2>Key Bible Verses</h2>
${versesHtml}
        </div>
        `;

  const start = shell.indexOf('<div class="word-header">');
  const relIdx = shell.indexOf('<h2>Related Words</h2>');
  const endMark = shell.lastIndexOf('<div class="section">', relIdx);
  if (start < 0 || relIdx < 0 || endMark < 0) return null;
  let html = shell.slice(0, start) + block + shell.slice(endMark);

  const desc = `${esc(code)} ${esc(lemma)} (${esc(translit)}) — ${lang} word study from Strong's and the tagged KJV.`;
  html = html.replace(/<title>[\s\S]*?<\/title>/,
    `<title>${esc(code)} ${esc(lemma)} (${esc(translit)}) | ${lang} Lexicon | USMC Ministries</title>`);
  html = html.replace(/<link rel="canonical" href="[^"]*"/,
    `<link rel="canonical" href="https://usmcmin.org/lexicon/${esc(code)}.html"`);
  html = html.replace(/<meta name="description" content="[^"]*"/, `<meta name="description" content="${desc}"`);
  html = html.replace(/<meta property="og:title" content="[^"]*"/,
    `<meta property="og:title" content="${esc(code)} ${esc(lemma)} | USMC Ministries Lexicon"`);
  html = html.replace(/<meta property="og:description" content="[^"]*"/,
    `<meta property="og:description" content="${desc}"`);
  html = html.replace(/G4434/g, esc(code)).replace(/πτωχός/g, esc(lemma)).replace(/ptōchos/g, esc(translit));
  if (WORDS(html.slice(html.indexOf('<div class="word-header">'))) < 140) return null;
  return html;
}

if (require.main === module) {
  const want = [...missingTargets().entries()].sort((a, b) => b[1] - a[1]);
  if (process.argv.includes('--list')) {
    buildIndex();
    const withData = want.filter(([c]) => (c[0] === 'G' ? greek : hebrew)[c]);
    console.log(`linked-but-absent codes: ${want.length}`);
    console.log(`  present in vendored Strong's data: ${withData.length}`);
    console.log(`  carried by a tagged KJV verse:     ${withData.filter(([c]) => (INDEX.get(c) || []).length).length}`);
  } else {
    const i = process.argv.indexOf('--limit');
    const LIMIT = i > -1 ? parseInt(process.argv[i + 1], 10) : Infinity;
    const j = process.argv.indexOf('--out');
    const OUT = j > -1 ? process.argv[j + 1] : LEX;
    const shell = fs.readFileSync(path.join(LEX, 'G4434.html'), 'utf8');
    buildIndex();
    fs.mkdirSync(OUT, { recursive: true });
    let made = 0, skipped = 0;
    for (const [code] of want) {
      if (made >= LIMIT) break;
      const html = buildPage(code, shell);
      if (!html) { skipped++; continue; }
      fs.writeFileSync(path.join(OUT, code + '.html'), html);
      made++;
    }
    console.log(`built ${made}, skipped ${skipped} (no Strong's data, no transliteration, or no tagged verse)`);
  }
}

module.exports = { missingTargets, buildIndex, buildPage, pickVerses };
