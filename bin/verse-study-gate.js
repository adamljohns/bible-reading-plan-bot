#!/usr/bin/env node
/* verse-study-gate.js — the hard quality gate for deep verse studies.
 *
 * A deep study is the one page type on this site where a model writes extended
 * theological prose, which makes it the one page type where a model can be
 * confidently, fluently wrong: a Calvin quote he never wrote, a Hebrew word that
 * isn't in the verse, a Strong's number pointing at a stub. None of that is
 * caught by looking at the page — it reads beautifully either way.
 *
 * So every checkable claim gets checked against the repo's own corpora, and the
 * gate exits non-zero if anything fails. Nothing ships on a failed gate. That is
 * the whole point: a gate that can't fail isn't a gate.
 *
 * Usage:
 *   node bin/verse-study-gate.js docs/verse/romans-8-1.html [...]
 *   node bin/verse-study-gate.js --all          # every deep study in docs/verse
 *   node bin/verse-study-gate.js --all --drafts # include drafts/ too
 * Exit: 0 all pass, 1 any fail.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { parseRef, BOOK_NAMES, squash } = require('./verse-study-scaffold.js');

const ROOT = path.resolve(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');

const MIN_WORDS = 1200;
/* The house structure for a deep study. Each entry is a set of accepted <h2>
 * wordings for the same job, so a writer can title the section in the page's own
 * voice ("For the Man Reading This") without the gate losing track of what it is. */
const REQUIRED_SECTIONS = [
  { job: 'the text and its words', any: ['text', 'words', 'language'] },
  { job: 'where the verse sits', any: ['where it sits', 'context', 'setting', 'in its place'] },
  { job: 'the witnesses (Reformed/patristic reading)', any: ['fathers', 'witness', 'saw', 'reformers', 'commentators'] },
  { job: 'confessional anchor', any: ['confession', 'doctrine', 'catechism', 'anchor'] },
  { job: 'application', any: ['application', 'for the man', 'for you', 'living it', 'so what'] },
  { job: 'go deeper', any: ['go deeper', 'further', 'related'] },
];

/* Normalize for verbatim comparison: quote marks, dashes, whitespace and case are
 * presentation, not substance. Everything else must match exactly. */
/* Compare on words, not typography. Editions differ on curly vs straight quotes,
 * em-dash style, and stray commas inside parentheses; the CCEL Calvin even prints
 * "(yatsar,)". None of that is what the gate is defending against. A fabricated
 * quotation fails on its words, which is what survives this normalization. */
const norm = (s) => String(s)
  .replace(/<[^>]+>/g, ' ')
  .replace(/&nbsp;/g, ' ').replace(/&amp;/g, ' and ').replace(/&#39;|&quot;|&ldquo;|&rdquo;/g, ' ')
  .replace(/&[a-z]+;/g, ' ')
  .toLowerCase()
  // Keep letters (any script), digits and whitespace; everything else is presentation.
  .replace(/[^\p{L}\p{N}\s]+/gu, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const corpusCache = new Map();
function corpus(fp) {
  if (!corpusCache.has(fp)) {
    corpusCache.set(fp, fs.existsSync(fp)
      ? norm(fs.readFileSync(fp, 'utf8').replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, ''))
      : '');
  }
  return corpusCache.get(fp);
}

/* An ellipsis in a quote means elision, which is legitimate. Require every
 * fragment to appear, in order, inside the same source — that permits honest
 * trimming while still refusing an invented sentence. */
function verbatimIn(quote, haystack) {
  // Split on the ellipsis BEFORE normalizing — normalization strips punctuation,
  // and the ellipsis is the one mark that carries meaning here.
  const fragments = String(quote).split(/\s*\.\.\.\s*|\s*…\s*/).map((f) => norm(f)).filter((f) => f.length > 12);
  if (!fragments.length) return true;
  let cursor = 0;
  for (const f of fragments) {
    const at = haystack.indexOf(f, cursor);
    if (at === -1) return false;
    cursor = at + f.length;
  }
  return true;
}

/* Which local file backs a given <cite>. Anything not listed here can't be
 * verified, and an unverifiable attribution is a failure, not a pass. */
function sourceFilesFor(cite) {
  const c = cite.toLowerCase();
  const files = [];
  const lbcf = c.match(/lbcf|confession/) && c.match(/ch(?:apter|\.)?\s*(\d+)/);
  if (lbcf) {
    const n = String(parseInt(lbcf[1], 10)).padStart(2, '0');
    files.push(path.join(DOCS, 'lbcf', `chapter-${n}.html`));
  }
  if (/catechism/.test(c)) files.push(path.join(DOCS, 'catechism.html'));
  const inst = c.match(/institutes\s*([ivx]+)\.(\d+)/i);
  if (inst) {
    const roman = { i: 1, ii: 2, iii: 3, iv: 4 };
    const b = roman[inst[1].toLowerCase()];
    if (b) files.push(path.join(DOCS, 'institutes', `b${b}-c${String(parseInt(inst[2], 10)).padStart(2, '0')}.html`));
  }
  // Scripture citations are checked against the chapter store.
  const scr = cite.match(/^([1-3]?\s*[A-Za-z ]+?)\s+(\d+):(\d+)/);
  if (scr && !files.length) {
    const { BOOK_IDS } = require('./verse-study-scaffold.js');
    const id = BOOK_IDS[scr[1].trim().toLowerCase()];
    if (id) files.push(path.join(DOCS, 'assets', 'chapters', `${id}_${parseInt(scr[2], 10)}.json`));
  }
  return files;
}

/* Not every source worth quoting lives in this repo. Augustine's Confessions,
 * Calvin's commentaries and Matthew Henry are all public domain and all absent
 * here. Rather than either banning them or trusting a model's recall, they go in
 * data/verse-study-sources.json — a human or agent pastes the verbatim text once,
 * records where it was checked, and only then may a study quote it. An entry that
 * has not been verified against a real source is not a license; the gate still
 * refuses it. */
let SOURCES = null;
function registeredSources() {
  if (SOURCES) return SOURCES;
  const fp = path.join(ROOT, 'data', 'verse-study-sources.json');
  SOURCES = fs.existsSync(fp) ? JSON.parse(fs.readFileSync(fp, 'utf8')).quotes || [] : [];
  return SOURCES;
}

function registeredQuote(claim, cite) {
  const hits = registeredSources().filter((q) => verbatimIn(claim, norm(q.text)));
  if (!hits.length) {
    return { ok: false, why: `no local corpus contains it and it is not registered in data/verse-study-sources.json` };
  }
  const verified = hits.find((q) => q.verified === true);
  if (!verified) {
    return { ok: false, why: `registered in verse-study-sources.json but marked verified:false (${hits[0].note || 'not yet checked against a real edition'})` };
  }
  // Match on the surname — pages cite "Calvin", the register records "John Calvin".
  const parts = norm(verified.author || '').split(' ').filter(Boolean);
  const wantAuthor = parts[parts.length - 1];
  if (wantAuthor && !norm(cite).includes(wantAuthor)) {
    return { ok: false, why: `registered text is attributed to "${verified.author}" but the page cites "${cite}"` };
  }
  return { ok: true };
}

function checkPage(fp) {
  const rel = path.relative(ROOT, fp);
  const fails = [];
  const warns = [];
  if (!fs.existsSync(fp)) return { rel, fails: ['file does not exist'], warns };
  const html = fs.readFileSync(fp, 'utf8');

  // ── identity ────────────────────────────────────────────────────────────
  const refM = html.match(/<meta name="verse-ref" content="([^"]*)"/);
  if (!refM || !refM[1].trim()) fails.push('missing <meta name="verse-ref"> — the SSG baker will overwrite this page');
  const ref = refM ? refM[1].trim() : null;
  const p = ref ? parseRef(ref) : null;
  if (ref && !p) fails.push(`verse-ref "${ref}" does not parse`);
  if (!/<meta name="verse-snippet" content="[^"]{10,}"/.test(html)) fails.push('missing <meta name="verse-snippet"> — index entry will have no subtitle');
  if (!/<link rel="canonical" href="https:\/\/usmcmin\.org\/verse\/[^"]+"/.test(html)) fails.push('missing or non-canonical <link rel="canonical">');

  // ── draft safety ────────────────────────────────────────────────────────
  const status = (html.match(/<meta name="study-status" content="([^"]*)"/) || [])[1] || '';
  if (!status) fails.push('missing <meta name="study-status"> (draft | approved)');
  if (status === 'draft' && !/<meta name="robots" content="[^"]*noindex/.test(html)) {
    fails.push('draft without <meta name="robots" content="noindex"> — an unreviewed draft must not be indexable');
  }
  if (status === 'approved' && /<meta name="robots" content="[^"]*noindex/.test(html)) {
    fails.push('approved study still carries noindex');
  }
  const todos = (html.match(/vs-todo/g) || []).length;
  if (status === 'approved' && todos) fails.push(`approved study still has ${todos} unwritten [WRITE …] slot(s)`);
  if (status === 'approved' && /vs-draft-banner/.test(html)) fails.push('approved study still shows the draft banner');
  if (status === 'draft' && todos) warns.push(`${todos} [WRITE …] slot(s) still unwritten — this draft is not finished`);

  // ── substance ───────────────────────────────────────────────────────────
  const body = html.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, '');
  const words = squash(body).split(/\s+/).filter(Boolean).length;
  if (words < MIN_WORDS) fails.push(`body is ${words} words, below the ${MIN_WORDS}-word floor for a deep study`);
  const headings = [...body.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/g)].map((m) => squash(m[1]).toLowerCase());
  REQUIRED_SECTIONS.forEach((sec) => {
    if (!headings.some((h) => sec.any.some((a) => h.includes(a)))) {
      fails.push(`no <h2> section doing the job "${sec.job}" (accepted wordings: ${sec.any.join(', ')}; found: ${headings.join(' / ') || 'none'})`);
    }
  });

  // ── quote verification: the anti-fabrication check ──────────────────────
  const quotes = [...body.matchAll(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/g)];
  quotes.forEach((q, i) => {
    const inner = q[1];
    // House idiom attributes with <footer>; <cite> is accepted too.
    const citeM = inner.match(/<footer[^>]*>([\s\S]*?)<\/footer>/) || inner.match(/<cite[^>]*>([\s\S]*?)<\/cite>/);
    const quoteText = squash(inner.replace(/<(footer|cite)[^>]*>[\s\S]*?<\/\1>/g, ''));
    if (quoteText.length < 25) return; // pull-quote or verse fragment, not an attribution
    if (!citeM) { fails.push(`blockquote #${i + 1} has no <footer>/<cite> — an unattributed quotation cannot be verified`); return; }
    const cite = squash(citeM[1]).replace(/^[—-]\s*/, '');
    // Split multi-paragraph quotes: each <p> is its own claim to verify.
    const claims = [...inner.matchAll(/<p[^>]*>([\s\S]*?)<\/p>/g)].map((m) => squash(m[1])).filter((t) => t.length > 25);
    const toCheck = claims.length ? claims : [quoteText];
    const files = sourceFilesFor(cite);
    toCheck.forEach((claim) => {
      const bare = claim.replace(/^["“]|["”]$/g, '');
      if (files.some((f) => verbatimIn(bare, corpus(f)))) return;
      const reg = registeredQuote(bare, cite);
      if (reg.ok) return;
      fails.push(`blockquote #${i + 1} attributed to "${cite}" cannot be verified — ${reg.why}. Quote: “${bare.slice(0, 80)}…”`);
    });
  });

  // ── word study integrity ────────────────────────────────────────────────
  const codes = [...new Set([...body.matchAll(/\b([GH]\d{1,4})\b/g)].map((m) => m[1]))];
  codes.forEach((code) => {
    const lp = path.join(DOCS, 'lexicon', code + '.html');
    if (!fs.existsSync(lp)) { fails.push(`cites Strong's ${code}, which has no lexicon page`); return; }
    const lex = fs.readFileSync(lp, 'utf8').toLowerCase();
    if (lex.includes('definition not found') || lex.includes('is a key term in the original scriptures')) {
      fails.push(`cites Strong's ${code}, whose lexicon page is a stub with no real definition — the word study would be built on filler`);
    }
    if (p) {
      const expectPrefix = p.testament === 'OT' ? 'H' : 'G';
      if (!code.startsWith(expectPrefix)) warns.push(`cites ${code} but ${ref} is ${p.testament} (${p.tongue}) — check this is a deliberate cross-language note`);
    }
  });

  // ── scripture accuracy ──────────────────────────────────────────────────
  if (p) {
    const chFp = path.join(DOCS, 'assets', 'chapters', `${p.bookId}_${p.ch}.json`);
    if (fs.existsSync(chFp)) {
      const data = JSON.parse(fs.readFileSync(chFp, 'utf8'));
      const has = (trans) => {
        const t = data[trans]; if (!t) return '';
        let s = '';
        for (let v = p.v1; v <= p.v2; v++) if (t[String(v)]) s += ' ' + t[String(v)];
        return norm(s.replace(/<S>\d+<\/S>/g, ''));
      };
      const kjv = has('KJV'), web = has('WEB');
      const primary = squash((body.match(/class="vs-text"[^>]*>([\s\S]*?)<\/(?:div|blockquote)>/) || [])[1] || '');
      if (primary) {
        const stripped = primary.replace(/—\s*(world english bible|king james version)[^]*$/i, '');
        const core = norm(stripped).split(/\s+/).slice(0, 12).join(' ');
        if (core.length > 20 && !kjv.includes(core) && !web.includes(core)) {
          fails.push(`the quoted verse text does not match KJV or WEB for ${ref} — “${core}…”`);
        }
      }
    } else warns.push(`no local chapter file for ${ref}; verse text unverified`);
  }

  // ── links + markup ──────────────────────────────────────────────────────
  const dir = path.dirname(fp);
  [...body.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1]).forEach((href) => {
    if (/^(https?:|mailto:|data:|#|tel:)/.test(href)) return;
    const clean = href.split(/[?#]/)[0];
    if (!clean) return;
    const target = clean.startsWith('/') ? path.join(DOCS, clean.slice(1)) : path.resolve(dir, clean);
    if (!fs.existsSync(target)) fails.push(`dead local link: ${href}`);
  });
  ['div', 'section', 'blockquote', 'nav', 'body', 'html'].forEach((t) => {
    const o = (body.match(new RegExp('<' + t + '[\\s>]', 'g')) || []).length;
    const c = (body.match(new RegExp('</' + t + '>', 'g')) || []).length;
    if (o !== c) fails.push(`unbalanced <${t}>: ${o} open, ${c} close`);
  });

  return { rel, ref, words, status, fails, warns };
}

function main() {
  const argv = process.argv.slice(2);
  let targets = argv.filter((a) => !a.startsWith('--'));
  if (argv.includes('--all')) {
    const dirs = [path.join(DOCS, 'verse')];
    if (argv.includes('--drafts')) dirs.push(path.join(ROOT, 'drafts', 'verse'));
    targets = [];
    dirs.forEach((d) => {
      if (!fs.existsSync(d)) return;
      fs.readdirSync(d).filter((f) => f.endsWith('.html')).forEach((f) => {
        const fp = path.join(d, f);
        if (/<meta name="verse-ref"/.test(fs.readFileSync(fp, 'utf8'))) targets.push(fp);
      });
    });
  }
  if (!targets.length) {
    console.error('usage: verse-study-gate.js <page.html> [...] | --all [--drafts]');
    process.exit(2);
  }
  let failed = 0;
  const results = targets.map((t) => checkPage(path.resolve(t)));
  results.forEach((r) => {
    if (r.fails.length) {
      failed++;
      console.log(`FAIL  ${r.rel}  (${r.ref || '?'}, ${r.words || 0} words, ${r.status || 'no status'})`);
      r.fails.forEach((f) => console.log('        ✗ ' + f));
    } else {
      console.log(`pass  ${r.rel}  (${r.ref}, ${r.words} words, ${r.status})`);
    }
    r.warns.forEach((w) => console.log('        ! ' + w));
  });
  console.log(`\nGate: ${results.length - failed}/${results.length} passed.`);
  if (failed) {
    console.log('Nothing ships until these are fixed.');
    process.exit(1);
  }
}

if (require.main === module) main();
module.exports = { checkPage, verbatimIn, norm };
