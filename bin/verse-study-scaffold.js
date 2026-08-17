#!/usr/bin/env node
/* verse-study-scaffold.js — assemble the research kit for a deep verse study.
 *
 * A deep study is hand-authored prose, but the *facts* underneath it should never
 * be. Every Hebrew/Greek word, every cross-reference, every confession quote in a
 * study has to come from something already in this repo, so it can be checked
 * verbatim later by bin/verse-study-gate.js. This script pulls that material
 * together so the writer (a human, a Claude session, or a local model) never has
 * to recall a fact from memory.
 *
 * Sources, all local:
 *   docs/assets/chapters/<book>_<ch>.json   12 translations; KJV carries <S>NNNN</S>
 *   docs/lexicon/<G|H>NNNN.html             7,835 word pages: script, translit, gloss
 *   docs/assets/cross-references.json       17,777 verse->verses chains
 *   docs/lbcf/chapter-NN.html               1689 Baptist Confession
 *   docs/catechism.html                     Baptist Catechism Q&A
 *   docs/institutes/bN-cNN.html             Calvin, Institutes (572k words)
 *
 * Usage:
 *   node bin/verse-study-scaffold.js "Romans 8:1"            # one kit to stdout
 *   node bin/verse-study-scaffold.js --memorize --out DIR    # every memorize verse
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const CH_DIR = path.join(DOCS, 'assets', 'chapters');
const LEX_DIR = path.join(DOCS, 'lexicon');

const BOOK_IDS = {
  'genesis':1,'exodus':2,'leviticus':3,'numbers':4,'deuteronomy':5,'joshua':6,'judges':7,'ruth':8,
  '1 samuel':9,'2 samuel':10,'1 kings':11,'2 kings':12,'1 chronicles':13,'2 chronicles':14,
  'ezra':15,'nehemiah':16,'esther':17,'job':18,'psalms':19,'psalm':19,'proverbs':20,'ecclesiastes':21,
  'song of solomon':22,'song of songs':22,'isaiah':23,'jeremiah':24,'lamentations':25,'ezekiel':26,
  'daniel':27,'hosea':28,'joel':29,'amos':30,'obadiah':31,'jonah':32,'micah':33,'nahum':34,
  'habakkuk':35,'zephaniah':36,'haggai':37,'zechariah':38,'malachi':39,
  'matthew':40,'mark':41,'luke':42,'john':43,'acts':44,'romans':45,'1 corinthians':46,'2 corinthians':47,
  'galatians':48,'ephesians':49,'philippians':50,'colossians':51,'1 thessalonians':52,'2 thessalonians':53,
  '1 timothy':54,'2 timothy':55,'titus':56,'philemon':57,'hebrews':58,'james':59,'1 peter':60,'2 peter':61,
  '1 john':62,'2 john':63,'3 john':64,'jude':65,'revelation':66,
};
const BOOK_NAMES = {};
Object.entries(BOOK_IDS).forEach(([n, id]) => {
  const title = n.replace(/\b\w/g, (c) => c.toUpperCase());
  if (!BOOK_NAMES[id] || title.length < BOOK_NAMES[id].length) BOOK_NAMES[id] = title;
});
BOOK_NAMES[19] = 'Psalm';

const stripTags = (s) => String(s).replace(/<[^>]+>/g, '');
const unent = (s) => String(s)
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<')
  .replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
  .replace(/&mdash;/g, '—').replace(/&ldquo;/g, '“').replace(/&rdquo;/g, '”');
const squash = (s) => unent(stripTags(s)).replace(/\s+/g, ' ').trim();
// KJV fuses Strong's as <S>NNNN</S>; other translations are clean prose.
const cleanVerse = (s) => squash(String(s).replace(/<S>\d+<\/S>/g, ''));
const normalizeDivineNames = (s) => s
  .replace(/\bYahweh of Armies\b/g, 'the LORD of Hosts').replace(/\bYahweh\b/g, 'the LORD');

function parseRef(ref) {
  const m = String(ref).trim().match(/^(.+?)\s+(\d+):(\d+)(?:\s*[-–—]\s*(\d+))?$/);
  if (!m) return null;
  const bookId = BOOK_IDS[m[1].trim().toLowerCase()];
  if (!bookId) return null;
  const v1 = parseInt(m[3], 10);
  return {
    book: BOOK_NAMES[bookId], bookId, ch: parseInt(m[2], 10),
    v1, v2: m[4] ? parseInt(m[4], 10) : v1,
    testament: bookId <= 39 ? 'OT' : 'NT',
    tongue: bookId <= 39 ? 'Hebrew' : 'Greek',
  };
}
const slugFor = (ref) => String(ref).toLowerCase().replace(/[–—]/g, '-').replace(/[ :]/g, '-') + '.html';

function chapterData(p) {
  const fp = path.join(CH_DIR, `${p.bookId}_${p.ch}.json`);
  if (!fs.existsSync(fp)) return null;
  try { return JSON.parse(fs.readFileSync(fp, 'utf8')); } catch (e) { return null; }
}

/* Verse text in the translations a study actually cites. KJV and WEB are public
 * domain and safe to bake into the page; the rest are for the writer's eyes only
 * so the exposition doesn't lean on one rendering. */
const PUBLIC_DOMAIN = ['KJV', 'WEB'];
const REFERENCE_ONLY = ['NKJV', 'ESV', 'NASB', 'CSB17', 'NET', 'NIV'];

function verseTexts(data, p) {
  const out = { publicDomain: {}, referenceOnly: {} };
  const pull = (trans) => {
    const t = data[trans];
    if (!t) return null;
    const parts = [];
    for (let v = p.v1; v <= p.v2; v++) if (t[String(v)]) parts.push(cleanVerse(t[String(v)]));
    return parts.length ? parts.join(' ') : null;
  };
  PUBLIC_DOMAIN.forEach((t) => { const s = pull(t); if (s) out.publicDomain[t] = t === 'WEB' ? normalizeDivineNames(s) : s; });
  REFERENCE_ONLY.forEach((t) => { const s = pull(t); if (s) out.referenceOnly[t] = s; });
  return out;
}

/* ── word study ────────────────────────────────────────────────────────────
 * The KJV in the chapter store tags each word with its Strong's number, which
 * gives us the verse's actual vocabulary without guessing. Each number is then
 * resolved against the local lexicon page for script, transliteration and gloss.
 * Anything with no lexicon page is reported rather than silently dropped. */
function strongsFor(data, p) {
  const kjv = data.KJV;
  if (!kjv) return [];
  const hits = [];
  for (let v = p.v1; v <= p.v2; v++) {
    const raw = kjv[String(v)];
    if (!raw) continue;
    const re = /([^<>]*?)<S>(\d+)<\/S>/g;
    let m;
    while ((m = re.exec(raw)) !== null) {
      const word = squash(m[1]).replace(/^[^A-Za-z’']+/, '').trim();
      const num = parseInt(m[2], 10);
      if (word) hits.push({ verse: v, word, strongs: (p.testament === 'OT' ? 'H' : 'G') + num });
    }
  }
  return hits;
}

/* Roughly a fifth of the 7,835 lexicon pages are stubs: real headword, but the
 * definition reads "Definition not found." followed by generated filler ("its
 * meaning of 'see definition' is foundational..."). That filler is worse than an
 * empty page, because it looks like scholarship. Detect it and say so, loudly —
 * a writer who quotes it produces a study that is confidently wrong. */
const STUB_MARKERS = [
  'definition not found',
  'is a key term in the original scriptures',
  'meaning of "see definition"',
  'meaning of “see definition”',
  'reveals its rich usage throughout the bible',
];

function lexiconEntry(code) {
  const fp = path.join(LEX_DIR, code + '.html');
  if (!fs.existsSync(fp)) return null;
  const s = fs.readFileSync(fp, 'utf8');
  const body = s.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '');
  const grab = (label) => {
    const re = new RegExp('>\\s*' + label + '\\s*<\\/h\\d>([\\s\\S]{0,1800})', 'i');
    const m = body.match(re);
    return m ? squash(m[1]).slice(0, 900) : '';
  };
  // Prefer the page body over the <title>: 1,608 pages have a malformed or absent title.
  // Stub pages carry malformed markup — `<div class="original-word"></span>
  // <span class="hebrew">לֵב</span></div>` — so read the whole div and strip tags
  // rather than grabbing the first text node.
  const divText = (cls) => squash(((body.match(new RegExp('class="' + cls + '"[^>]*>([\\s\\S]*?)</div>')) || [])[1] || ''));
  const script = divText('original-word');
  const lemma = divText('transliteration');
  const pos = divText('part-of-speech') || divText('word-type');
  const title = unent((s.match(/<title>([^<]*)<\/title>/) || [])[1] || '');
  const tm = title.match(/^(\w+)\s*—\s*([^(]+?)\s*\(([^)]*)\)/);
  const definition = grab('Definition');
  const significance = grab('Usage &amp; Theological Significance') || grab('Usage & Theological Significance');
  const hay = (definition + ' ' + significance).toLowerCase();
  const stub = !definition || STUB_MARKERS.some((m) => hay.includes(m));
  return {
    code,
    lemma: lemma || (tm ? tm[2].trim() : ''),
    gloss: tm && tm[3].trim() ? tm[3].trim() : '',
    partOfSpeech: pos,
    script,
    definition: stub ? '' : definition,
    significance: stub ? '' : significance,
    stub,
    // A stub still proves the headword exists; it just carries no usable content.
    stubNote: stub ? `Lexicon page ${code} is a stub (no real definition). Do NOT quote or paraphrase it — source this word elsewhere or leave it out.` : '',
    page: `/lexicon/${code}.html`,
  };
}

/* Content words carry the study; the KJV tags articles and particles too, and a
 * word study built on "the" and "and" wastes the writer's attention. */
const FUNCTION_WORDS = new Set(['the','a','an','and','but','or','of','to','in','for','with','that','which','who','is','are','was','were','be','not','no','shall','will','unto','they','them','him','his','her','it','this','these','all','as','so','then','there','now','ye','you','thou','thy','we','us','our','me','my','i','he','she','from','by','on','at','up','out','have','had','hath','do','did','doth','also','when','if','than','thing','things']);

function wordStudy(data, p) {
  const hits = strongsFor(data, p);
  const seen = new Set();
  const out = [];
  hits.forEach((h) => {
    if (seen.has(h.strongs)) return;
    seen.add(h.strongs);
    const entry = lexiconEntry(h.strongs);
    const isContent = !FUNCTION_WORDS.has(h.word.toLowerCase().replace(/[^a-z’']/g, ''));
    out.push({ ...h, priority: isContent ? 'content' : 'function', lexicon: entry, lexiconMissing: !entry });
  });
  return out;
}

/* ── cross-references ─────────────────────────────────────────────────────── */
function crossRefs(p, limit) {
  const fp = path.join(DOCS, 'assets', 'cross-references.json');
  if (!fs.existsSync(fp)) return [];
  let map;
  try { map = JSON.parse(fs.readFileSync(fp, 'utf8')); } catch (e) { return []; }
  const out = [];
  for (let v = p.v1; v <= p.v2 && out.length < limit; v++) {
    const chain = map[`${p.bookId}_${p.ch}_${v}`] || [];
    chain.forEach((key) => {
      if (out.length >= limit) return;
      const m = String(key).match(/^(\d+)_(\d+)_(\d+)$/);
      if (!m) return;
      const [, b, c, vv] = m;
      const ref = `${BOOK_NAMES[+b] || ('Book' + b)} ${c}:${vv}`;
      const cd = chapterData({ bookId: +b, ch: +c });
      let text = '';
      if (cd && cd.WEB && cd.WEB[vv]) text = normalizeDivineNames(cleanVerse(cd.WEB[vv]));
      else if (cd && cd.KJV && cd.KJV[vv]) text = cleanVerse(cd.KJV[vv]);
      out.push({ ref, text });
    });
  }
  return out;
}

/* ── confessional + Reformed sources ───────────────────────────────────────
 * Candidates only. The writer picks; the gate later re-checks that whatever was
 * quoted appears verbatim in one of these files. Nothing here is a license to
 * paraphrase a dead man inside quotation marks. */
function textOf(fp) {
  if (!fs.existsSync(fp)) return '';
  const s = fs.readFileSync(fp, 'utf8').replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '');
  return squash(s);
}

function sentencesWith(body, terms, cap, sourceLabel, href) {
  if (!body) return [];
  const sents = body.split(/(?<=[.?!])\s+/);
  const scored = [];
  sents.forEach((s) => {
    if (s.length < 60 || s.length > 700) return;
    const low = s.toLowerCase();
    let score = 0;
    terms.forEach((t) => { if (t.length > 3 && low.includes(t)) score += 1; });
    if (score) scored.push({ score, quote: s.trim(), source: sourceLabel, href });
  });
  scored.sort((a, b) => b.score - a.score || a.quote.length - b.quote.length);
  return scored.slice(0, cap);
}

function keyTerms(study, texts) {
  const terms = new Set();
  study.filter((w) => w.priority === 'content').forEach((w) => {
    if (w.lexicon && w.lexicon.gloss) w.lexicon.gloss.split(/[\/,;]/).forEach((g) => terms.add(g.trim().toLowerCase()));
    terms.add(w.word.toLowerCase());
  });
  Object.values(texts.publicDomain).forEach((t) => {
    t.toLowerCase().replace(/[^a-z ]/g, ' ').split(/\s+/).forEach((w) => { if (w.length > 4 && !FUNCTION_WORDS.has(w)) terms.add(w); });
  });
  return [...terms].filter(Boolean);
}

/* Keyword matching against the confessions is noisy — asking it about Romans 8:1
 * ("flesh", "spirit", "walk") returns the chapters on baptism and the Lord's
 * Supper, which is worse than useless. But the LBCF and the Catechism both cite
 * their proof-texts inline ("Proof-texts Rom 3:24 · Rom 8:30 · …"). A paragraph
 * that already cites this verse is, by the confession's own reckoning, the place
 * this verse belongs. That is a precise signal, so it goes first and is labelled
 * as the strong one. */
const ABBREV = {
  1:['Gen'],2:['Ex','Exod'],3:['Lev'],4:['Num'],5:['Deut'],6:['Josh'],7:['Judg'],8:['Ruth'],
  9:['1 Sam'],10:['2 Sam'],11:['1 Kings','1 Kgs'],12:['2 Kings','2 Kgs'],13:['1 Chron','1 Chr'],14:['2 Chron','2 Chr'],
  15:['Ezra'],16:['Neh'],17:['Esth'],18:['Job'],19:['Ps','Psa'],20:['Prov'],21:['Eccl'],22:['Song'],
  23:['Isa'],24:['Jer'],25:['Lam'],26:['Ezek'],27:['Dan'],28:['Hos'],29:['Joel'],30:['Amos'],31:['Obad'],
  32:['Jonah'],33:['Mic'],34:['Nah'],35:['Hab'],36:['Zeph'],37:['Hag'],38:['Zech'],39:['Mal'],
  40:['Matt','Mat'],41:['Mark'],42:['Luke'],43:['John'],44:['Acts'],45:['Rom'],46:['1 Cor'],47:['2 Cor'],
  48:['Gal'],49:['Eph'],50:['Phil'],51:['Col'],52:['1 Thess'],53:['2 Thess'],54:['1 Tim'],55:['2 Tim'],
  56:['Titus'],57:['Philem'],58:['Heb'],59:['James','Jas'],60:['1 Peter','1 Pet'],61:['2 Peter','2 Pet'],
  62:['1 John'],63:['2 John'],64:['3 John'],65:['Jude'],66:['Rev'],
};

/* Does a proof-text citation cover our verse? Handles "Rom 8:1", "Rom 8:1-4",
 * and "James 2:17,22,26". */
function citationCovers(cit, p) {
  const names = ABBREV[p.bookId] || [];
  const m = cit.match(/^\s*([1-3]?\s*[A-Za-z]+)\s*(\d+):([\d,\-–\s]+)/);
  if (!m) return false;
  const book = m[1].replace(/\s+/g, ' ').trim();
  if (!names.some((n) => n.toLowerCase() === book.toLowerCase())) return false;
  if (parseInt(m[2], 10) !== p.ch) return false;
  return m[3].split(',').some((part) => {
    const r = part.trim().match(/^(\d+)(?:\s*[-–]\s*(\d+))?$/);
    if (!r) return false;
    const a = parseInt(r[1], 10), b = r[2] ? parseInt(r[2], 10) : a;
    return !(b < p.v1 || a > p.v2); // ranges overlap
  });
}

function proofTextMatches(p) {
  const out = [];
  const scan = (fp, label, href) => {
    const body = textOf(fp);
    if (!body) return;
    // Each paragraph ends with its proof-text list; take the prose before it.
    const re = /Proof-texts\s*([^¶]{0,400})/g;
    let m;
    while ((m = re.exec(body)) !== null) {
      const cites = m[1].split(/·|&middot;/).map((s) => s.trim()).filter(Boolean);
      if (!cites.some((c) => citationCovers(c, p))) continue;
      // Take the text after the LAST paragraph marker before this proof-text list,
      // so the quote is one whole numbered paragraph rather than a chunk that
      // starts mid-word.
      const before = body.slice(Math.max(0, m.index - 2000), m.index);
      const cut = before.lastIndexOf('¶');
      const para = (cut >= 0 ? before.slice(cut + 1) : before).replace(/^\s*\d*\s*/, '').trim();
      if (para.length > 40) out.push({ source: label, href, quote: para, why: `cites ${cites.filter((c) => citationCovers(c, p)).join(', ')}` });
    }
  };
  const lbcfDir = path.join(DOCS, 'lbcf');
  if (fs.existsSync(lbcfDir)) {
    fs.readdirSync(lbcfDir).filter((f) => /^chapter-\d+\.html$/.test(f)).forEach((f) => {
      const n = parseInt(f.match(/\d+/)[0], 10);
      scan(path.join(lbcfDir, f), `1689 LBCF, ch. ${n}`, `/lbcf/${f}`);
    });
  }
  scan(path.join(DOCS, 'catechism.html'), 'The Baptist Catechism', '/catechism.html');
  return out.slice(0, 8);
}

function confessionalCandidates(terms) {
  const out = { lbcf: [], catechism: [], institutes: [] };
  const lbcfDir = path.join(DOCS, 'lbcf');
  if (fs.existsSync(lbcfDir)) {
    fs.readdirSync(lbcfDir).filter((f) => /^chapter-\d+\.html$/.test(f)).forEach((f) => {
      const n = parseInt(f.match(/\d+/)[0], 10);
      out.lbcf.push(...sentencesWith(textOf(path.join(lbcfDir, f)), terms, 2, `1689 LBCF, ch. ${n}`, `/lbcf/${f}`));
    });
    out.lbcf.sort((a, b) => b.score - a.score);
    out.lbcf = out.lbcf.slice(0, 6);
  }
  out.catechism = sentencesWith(textOf(path.join(DOCS, 'catechism.html')), terms, 6, 'The Baptist Catechism', '/catechism.html');
  const instDir = path.join(DOCS, 'institutes');
  if (fs.existsSync(instDir)) {
    const roman = ['', 'I', 'II', 'III', 'IV'];
    fs.readdirSync(instDir).filter((f) => /^b\d+-c\d+\.html$/.test(f)).forEach((f) => {
      const m = f.match(/^b(\d+)-c(\d+)\.html$/);
      const label = `Calvin, Institutes ${roman[+m[1]] || m[1]}.${parseInt(m[2], 10)}`;
      out.institutes.push(...sentencesWith(textOf(path.join(instDir, f)), terms, 1, label, `/institutes/${f}`));
    });
    out.institutes.sort((a, b) => b.score - a.score);
    out.institutes = out.institutes.slice(0, 8);
  }
  return out;
}

/* ── memorize context ─────────────────────────────────────────────────────── */
function memorizePacks() {
  const fp = path.join(DOCS, 'data', 'memory-packs.json');
  if (!fs.existsSync(fp)) return [];
  try { return JSON.parse(fs.readFileSync(fp, 'utf8')).packs || []; } catch (e) { return []; }
}

function buildKit(ref) {
  const p = parseRef(ref);
  if (!p) return { ref, error: 'unparseable-ref' };
  const data = chapterData(p);
  if (!data) return { ref, error: 'no-chapter-data' };
  const texts = verseTexts(data, p);
  const study = wordStudy(data, p);
  const terms = keyTerms(study, texts);
  const packs = memorizePacks()
    .filter((pk) => pk.verses.some((v) => v.ref === ref))
    .map((pk) => ({ id: pk.id, name: pk.name }));
  return {
    ref,
    slug: slugFor(ref),
    parsed: p,
    memorizePacks: packs,
    texts,
    wordStudy: study,
    crossReferences: crossRefs(p, 12),
    // Proof-text hits first: the confession itself says this verse belongs here.
    proofTexts: proofTextMatches(p),
    sources: confessionalCandidates(terms),
    existingPage: fs.existsSync(path.join(DOCS, 'verse', slugFor(ref))),
  };
}

function main() {
  const argv = process.argv.slice(2);
  const outIdx = argv.indexOf('--out');
  const outDir = outIdx >= 0 ? argv[outIdx + 1] : null;
  const wantMemorize = argv.includes('--memorize');
  let refs = argv.filter((a, i) => !a.startsWith('--') && i !== outIdx - 0 + (outIdx >= 0 ? 1 : 0) - (outIdx >= 0 ? 0 : 0) && a !== (outDir || ' '));
  if (wantMemorize) {
    const seen = new Set();
    refs = [];
    memorizePacks().forEach((pk) => pk.verses.forEach((v) => { if (!seen.has(v.ref)) { seen.add(v.ref); refs.push(v.ref); } }));
  }
  if (!refs.length) {
    console.error('usage: verse-study-scaffold.js "Romans 8:1" [...]  |  --memorize --out DIR');
    process.exit(2);
  }
  if (outDir) fs.mkdirSync(outDir, { recursive: true });
  let ok = 0;
  const failures = [];
  refs.forEach((r) => {
    const kit = buildKit(r);
    if (kit.error) { failures.push(`${r}: ${kit.error}`); return; }
    ok++;
    if (outDir) fs.writeFileSync(path.join(outDir, kit.slug.replace(/\.html$/, '.json')), JSON.stringify(kit, null, 1));
    else console.log(JSON.stringify(kit, null, 1));
  });
  if (outDir) {
    console.log(`Study kits written: ${ok}/${refs.length} -> ${outDir}`);
    const thin = [];
    refs.forEach((r) => {
      const f = path.join(outDir, slugFor(r).replace(/\.html$/, '.json'));
      if (!fs.existsSync(f)) return;
      const k = JSON.parse(fs.readFileSync(f, 'utf8'));
      const usable = k.wordStudy.filter((w) => w.priority === 'content' && w.lexicon && !w.lexicon.stub);
      if (usable.length < 2) thin.push(`${r} (${usable.length} content words with a real lexicon entry)`);
    });
    if (thin.length) { console.log(`  Thin kits — writer needs to work harder on the word study (${thin.length}):`); thin.forEach((t) => console.log('   - ' + t)); }
  }
  if (failures.length) { console.log('  Failures:'); failures.forEach((f) => console.log('   - ' + f)); process.exitCode = 1; }
}

if (require.main === module) main();
module.exports = { buildKit, parseRef, slugFor, BOOK_IDS, BOOK_NAMES, squash };
