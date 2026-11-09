#!/usr/bin/env node
'use strict';
/**
 * Full-review patch builder (Chaps ticket, 2026-11-08).
 *
 * Stage 3 of a full-review round:
 *   select-enrichment-batch.js --full-review -> full-review-fetch.py ->
 *   full-review-build-patch.js -> apply-full-review-patch.js (Adam's GO only)
 *
 * READ-ONLY on churches.json. Turns the fetcher's verified observations into
 *   data/full-review/rounds/<round>/review-patch.json   every proposed change, per church
 *   data/full-review/rounds/<round>/hold.json          the HOLD items for Chaps QA
 *   data/full-review/rounds/<round>/observations.json  fetcher output incl. page text (git-ignored)
 *   data/full-review/hold-queue.json                   cumulative HOLD queue (sidecar)
 *   docs/data/full-review-stats.json                   one row per round (public dashboard counts)
 *
 * SAFETY GATES (ticket, verbatim intent):
 *  - Every change carries an evidence quote AND a URL, or it is dropped.
 *  - A proposal that moves a church to RED or BLACK, or off GREEN, is HOLD.
 *  - Pastor replacements and other changes auto-apply only at HIGH confidence;
 *    everything else is HOLD.
 *  - Nothing is ever deleted. Duplicates and wrong-church data are flagged to
 *    HOLD for the existing merge tooling (scripts/merge-duplicate-churches.js).
 *
 * Usage:
 *   node scripts/full-review-build-patch.js --input obs.json --round <id> [--out docs/data/full-review] [--dry-run]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { looksFemaleFirstName } = require('./lib/female-first-names.js');
const { isPlaceholderPastor } = require('./lib/grind-lanes.js');
const { denomPrior, AFFILIATION_RE, METHODOLOGY_URL, METHODOLOGY_QUOTE } = require('./lib/denomination-priors.js');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const ROOT = path.join(__dirname, '..');
const CHURCHES = process.env.FULL_REVIEW_CHURCHES_PATH || path.join(ROOT, 'docs', 'data', 'churches.json');
const INPUT = opt('--input', null);
// Working files live OUTSIDE docs/ (docs/ is the public site): unreviewed RED/BLACK
// proposals and cached page text must not publish. Only the counts in
// docs/data/full-review-stats.json are public (the grind-report dashboard).
const OUT = path.resolve(opt('--out', path.join(ROOT, 'data', 'full-review')));
const STATS = path.resolve(opt('--stats', path.join(ROOT, 'docs', 'data', 'full-review-stats.json')));
const DRY = args.includes('--dry-run');
// Local (Eastern) calendar date, not UTC — a 10 pm round must not stamp tomorrow.
const TODAY = new Date().toLocaleDateString('en-CA');
const ROUND = opt('--round', 'fr-' + new Date().toISOString().replace(/[-:]/g, '').slice(0, 13));
if (!INPUT) { console.error('usage: --input <observations.json> [--round id] [--out dir] [--dry-run]'); process.exit(2); }

const sha256 = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const SHA_BEFORE = sha256(CHURCHES);
const all = JSON.parse(fs.readFileSync(CHURCHES, 'utf8')).churches.filter(c => c && c.id);
const byId = new Map(all.map(c => [c.id, c]));
const obsFile = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const observations = obsFile.observations || obsFile;

const SEV = { green: 0, yellow: 1, red: 2, black: 3 };
const DIMS = ['scripture', 'christology', 'gender', 'soteriology', 'preaching', 'cultural', 'leadership', 'mission', 'mens_discipleship', 'denominational'];
const LABEL = { scripture: 'Scripture', christology: 'Christology', gender: 'Gender', soteriology: 'Soteriology', preaching: 'Preaching', cultural: 'Cultural', leadership: 'Leadership', mission: 'Mission', mens_discipleship: "Men's discipleship", denominational: 'Accountability' };
const nrm = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim().toLowerCase();
const clip = (s, n = 240) => { s = String(s || '').trim(); return s.length > n ? s.slice(0, n - 1) + '…' : s; };
const hostOf = u => { try { return new URL(u).hostname.replace(/^www\./, '').toLowerCase(); } catch (_) { return null; } };
const urlPath = u => { try { return new URL(u).pathname.replace(/\/+$/, '').toLowerCase(); } catch (_) { return String(u || '').toLowerCase(); } };
const pageUrl = id =>`https://usmcmin.org/churches/${id}.html`;

// Names: compare on surname + first initial, titles stripped.
const TITLE_RE = /\b(the|rev|reverend|very|right|dr|pastor|fr|father|mother|elder|bishop|rector|senior|lead|associate|interim|mr|mrs|ms|jr|sr|ii|iii|op|o\.p\.a?|d\.?min|ph\.?d|m\.?div)\b\.?/gi;
const nameKey = n => {
  const t = String(n || '').replace(/\(.*?\)/g, ' ').replace(TITLE_RE, ' ').replace(/[^A-Za-z' -]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase().split(' ').filter(Boolean);
  return t.length ? { first: t[0][0], last: t[t.length - 1], full: t.join(' ') } : null;
};
const sameName = (a, b) => { const x = nameKey(a), y = nameKey(b); return !!(x && y && x.last === y.last && x.first === y.first); };
const LEAD_ROLE = /senior|lead|rector|priest[- ]in[- ]charge|vicar|^pastor$|^the pastor|head pastor|sole pastor|minister$|senior minister|pastor\/teacher|^pastor\b(?!.*(youth|children|kids|student|worship|music|care|family|women|outreach|executive|associate|assistant))/i;
const NONLEAD_ROLE = /youth|kids|children|students|worship|music|executive|associate|assistant|admin|outreach|discipleship|family|women|care|counseling|education|operations|deacon|emerit|retired|interim|supply/i;
const PASTORAL_ROLE = /pastor|priest|rector|vicar|elder|minister|reverend|\brev\b|curate|chaplain/i;

// ── duplicate indexes (whole directory, read-only) ───────────────────────────
const GENERIC_HOSTS = /^(facebook\.com|m\.facebook\.com|youtube\.com|instagram\.com|sites\.google\.com|google\.com|linktr\.ee|umc\.org|episcopalassetmap\.org|churches\.sbc\.net|yelp\.com|wixsite\.com|squarespace\.com)$/;
const addrKey = c => {
  const a = String(c.address || '');
  const m = a.match(/^\s*(\d{1,6})\s+([A-Za-z]+)/), z = a.match(/\b(\d{5})(?:-\d{4})?\b(?!.*\b\d{5}\b)/);
  return m && z ? `${m[1]}|${m[2].toLowerCase()}|${z[1]}` : null;
};
const byAddr = new Map(), byHost = new Map();
for (const c of all) {
  const k = addrKey(c); if (k) (byAddr.get(k) || byAddr.set(k, []).get(k)).push(c.id);
  const h = hostOf(c.website); if (h && !GENERIC_HOSTS.test(h)) (byHost.get(h) || byHost.set(h, []).get(h)).push(c.id);
}

// ── evidence helpers ─────────────────────────────────────────────────────────
const ev = (quote, url, extra = {}) => (quote && url ? { quote: clip(quote, 300), url, ...extra } : null);
// "Women's Bible Study" must never count as a men's ministry: re-check each
// stored hit with a word boundary (fetcher regex fixed too; this guards old obs).
const SIGNAL_GUARD = { mens_ministry: /(^|[^A-Za-z])(men'?s|brotherhood|united methodist men|episcopal church men|men of|man church)/i };
function firstSignal(o, key) {
  const s = ((o.signals || {})[key] || []).filter(h => !SIGNAL_GUARD[key] || SIGNAL_GUARD[key].test(String(h.quote).replace(/women'?s/gi, ' ')));
  return s.length ? s[0] : null;
}
function pagesText(o) { return (o.pages || []).map(p => ({ url: p.url, norm: nrm(p.text || '') })); }
// Verbatim window of page text around a name (word-bounded), for roster evidence.
function around(o, name, url) {
  const p = (o.pages || []).find(x => x.url === url && x.text) || (o.pages || []).find(x => x.text && x.text.includes(name));
  if (!p) return null;
  const i = p.text.indexOf(name);
  if (i < 0) return null;
  let a = Math.max(0, i - 60), b = Math.min(p.text.length, i + name.length + 100);
  while (a > 0 && /\S/.test(p.text[a - 1])) a--;
  while (b < p.text.length && /\S/.test(p.text[b])) b++;
  return { quote: p.text.slice(a, b).trim(), url: p.url };
}
function onPages(o, needle) { const n = nrm(needle); return n.length > 3 && pagesText(o).some(p => p.norm.includes(n)); }

// ── published rules (docs/directory-methodology.html) ────────────────────────
// Ratings follow WRITTEN rules only. A category score or overall rating is
// proposed only when one of these rules — whose text must appear verbatim on the
// methodology page at build time — maps the evidence to that level. The rule's
// own text is cited next to the church-page quote. Anything the model or a
// keyword signal suggests beyond what a rule supports becomes a separate HOLD
// item ("needs-ruling: …") for Chaps and Adam, never a proposed score.
// To let the engine score something new (e.g. a men's-ministry GREEN), publish
// the rule on the methodology page first, then add it here.
const METH_PATH = path.join(ROOT, 'docs', 'directory-methodology.html');
const METH_TEXT = (() => { try { return nrm(fs.readFileSync(METH_PATH, 'utf8').replace(/<[^>]+>/g, ' ').replace(/&amp;/g, '&').replace(/&rarr;/g, '→')); } catch (_) { return ''; } })();
const RULES = {
  female_senior: { text: 'Female senior pastor → RED minimum.', context: 'The directory holds a complementarian position on the church office of elder / pastor.',
    level: 'red', dims: ['gender', 'leadership'], short: 'female senior pastor' },
  affirming_denom: { text: 'LGBTQ-affirming denomination → RED minimum.', context: METHODOLOGY_QUOTE.replace(/^LGBTQ-affirming denomination → RED minimum\.\s*/, ''),
    level: 'red', dims: ['denominational'], short: 'LGBTQ-affirming denomination' },
  prosperity: { text: 'Prosperity gospel → BLACK.', context: null, level: 'black', dims: [], short: 'prosperity gospel' },
};
for (const [k, r] of Object.entries(RULES)) {
  r.key = k;
  r.published = !!METH_TEXT && METH_TEXT.includes(nrm(r.text)) && (!r.context || METH_TEXT.includes(nrm(r.context)));
  if (!r.published) console.error(`WARNING: rule "${r.text}" not found verbatim on ${METH_PATH} — rule disabled`);
}
const ruleCite = r => ({ text: r.text, context: r.context, url: METHODOLOGY_URL });

// A category score needs an on-topic quote: one that actually addresses it.
const TOPIC = {
  scripture: /scripture|bible|word of god|inerran|infallib|inspired|authority/i,
  christology: /jesus|christ|son of god|savio|trinity|deity|incarnat/i,
  gender: /\b(wom[ae]n|m[ae]n|male|female|she|her|husband|wife|spouse|gender|sexual|orientation|lgbt\w*|marriage|ordain\w*|complementarian|egalitarian)\b/i,
  soteriology: /salvation|saved|grace|faith alone|justif|redeem|atone|forgive|\bsin/i,
  preaching: /preach|sermon|homil|exposit|pulpit|verse.by.verse/i,
  cultural: /justice|diversity|equity|inclusi|orientation|lgbt|pride|gender|racial|affirming|prosperity|wealth/i,
  leadership: /pastor|elder|rector|priest|vicar|minister|vestry|deacon|bishop|leader|board|session|council|staff/i,
  mission: /mission|gospel|evangel|great commission|disciple|nations|outreach|share/i,
  mens_discipleship: /(^|[^A-Za-z])men(['’]s)?\b|brotherhood/i,
  denominational: /denominat|diocese|conference|synod|presbytery|convention|association|network|episcopal|methodist|lutheran|presbyterian|baptist|anglican|united church|communion/i,
};
const onTopic = (d, q) => !!(TOPIC[d] && TOPIC[d].test(String(q || '').replace(/wom[ae]n['’]?s?/gi, d === 'mens_discipleship' ? ' ' : '$&')));

// ── evidence ranking: prefer staff/about prose over menu and nav lines ───────
const PAGE_KIND = u => { const p = urlPath(u); if (/staff|leader|clergy|team|rector|pastor|priest|who-we-are|meet|elder|our-priest/.test(p)) return 'staff'; if (/about|history|story|believ|faith|mission|welcome|new/.test(p)) return 'about'; return p === '' ? 'home' : 'other'; };
function navLike(q) { const w = String(q).split(/\s+/).filter(Boolean); const caps = w.filter(x => /^[A-Z&|]/.test(x)).length; return w.length >= 6 && caps / w.length > 0.55 && !/[a-z][.!?]["'”’)]?(\s|$)/.test(q); }
function quality(q, url, prefer = []) {
  let s = ({ staff: 3, about: 2, home: 0, other: 1 })[PAGE_KIND(url)];
  if (/[a-z][.!?]["'”’)]?(\s|$)/.test(q)) s += 2;
  if (navLike(q)) s -= 5;
  if (/send email|\(\d{3}\)\s?\d{3}-\d{4}|menu|log ?in|member area/i.test(q)) s -= 2;
  if (q.length >= 30 && q.length <= 280) s += 1;
  for (const [rx, w] of prefer) if (rx.test(q)) s += w;
  return s;
}
// Sentence boundaries that are not abbreviations ("St. Mary's", "The Rev. Jay").
const ABBR = /\b(St|Rev|Dr|Mr|Mrs|Ms|Fr|Jr|Sr|Mt|Ft|Hon|Msgr|Ave|Rd|Blvd|Inc|[A-Z])$/;
function isBoundary(text, i) { return /[.!?]/.test(text[i]) && text[i + 1] === ' ' && !(text[i] === '.' && ABBR.test(text.slice(Math.max(0, i - 5), i))); }
function prevBoundary(text, from) { for (let i = from - 1; i >= 0; i--) if (isBoundary(text, i)) return i; return -1; }
function nextBoundary(text, from) { for (let i = from; i < text.length - 1; i++) if (isBoundary(text, i)) return i; return -1; }
// Verbatim, word-bounded, roughly sentence-bounded window around [start,end).
function sentenceAt(text, start, end, cap = 280) {
  const back = prevBoundary(text, start);
  let a = back >= 0 && start - back <= cap ? back + 2 : start;
  if (a === start) { // nav/menu text has no sentence boundary: keep only a leading title word or two
    const pre = text.slice(Math.max(0, start - 40), start).match(/((?:(?:Meet|Our|The|Senior|Lead|Pastor|Rev\.?|Reverend|Fr\.|Father|Mother|Rector|Dr\.|St\.|Saint)\s+){1,3})$/);
    if (pre) a = start - pre[1].length;
  }
  const nb = nextBoundary(text, end);
  let b = nb >= 0 ? nb + 1 : text.length;
  if (b - end > cap) b = Math.min(text.length, end + 120);
  if (b - a > cap + 120) { a = Math.max(a, start - 120); b = Math.min(b, end + 160); }
  while (a > 0 && /\S/.test(text[a - 1])) a--;
  while (b < text.length && /\S/.test(text[b])) b++;
  return text.slice(a, b).trim();
}
function scan(o, rx, prefer = []) {
  const out = [];
  for (const p of (o && o.pages) || []) {
    if (!p.text) continue;
    const g = new RegExp(rx.source, rx.flags.includes('g') ? rx.flags : rx.flags + 'g');
    let m, n = 0;
    while ((m = g.exec(p.text)) && n++ < 25) {
      const q = sentenceAt(p.text, m.index, m.index + m[0].length);
      if (!out.some(x => x.quote === q)) out.push({ quote: q, url: p.url, match: m[0] });
      if (!m[0].length) g.lastIndex++;
    }
  }
  return out.map(x => ({ ...x, score: quality(x.quote, x.url, prefer) })).sort((a, b) => b.score - a.score);
}
function best(cands, prefer = []) {
  return cands.filter(x => x && x.quote && x.url).map(x => ({ ...x, score: quality(x.quote, x.url, prefer) })).sort((a, b) => b.score - a.score)[0] || null;
}
// Drop evidence that repeats (or merely wraps) a quote already cited.
function dedupeEv(list, primary) {
  const seen = primary ? [nrm(primary.quote)] : [];
  return (list || []).filter(Boolean).filter(e => { const q = nrm(e.quote); if (!q || seen.some(x => x.includes(q) || q.includes(x))) return false; seen.push(q); return true; });
}
const esc = s => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Gender must rest on page evidence: pronouns or a spouse in the person's own
// bio. A first-name list alone is never enough (it goes to HOLD "unconfirmed").
const FEM_RX = /\b(she|her|hers|herself)\b/gi, MASC_RX = /\b(he|him|his|himself)\b/gi;
function genderEvidence(o, name) {
  const k = nameKey(name);
  if (!k) return null;
  const parts = String(name).replace(/\(.*?\)/g, ' ').replace(TITLE_RE, ' ').trim().split(/\s+/);
  const first = parts[0], last = parts[parts.length - 1];
  const needles = [name, `${first} ${last}`, /^[A-Z][a-z]{2,}$/.test(first) ? first : null].filter(Boolean);
  const found = [];
  for (const p of (o && o.pages) || []) {
    if (!p.text) continue;
    for (const nd of new Set(needles)) {
      const g = new RegExp(`\\b${esc(nd)}\\b`, 'g');
      let m, n = 0;
      while ((m = g.exec(p.text)) && n++ < 10) {
        const win = p.text.slice(m.index, m.index + 420);
        // stop the bio window at the next titled person who is not this one
        const nextP = win.slice(nd.length).search(/\b(Pastor|Rev\.?|Reverend|Fr\.|Father|Mother|Deacon|Elder)\s+(?!${esc(first)}\b|${esc(last)}\b)[A-Z][a-z]+/);
        const bio = nextP > 0 ? win.slice(0, nd.length + nextP) : win;
        const fem = (bio.match(FEM_RX) || []).length, masc = (bio.match(MASC_RX) || []).length;
        const verdict = fem > masc ? 'female' : masc > fem ? 'male' : null;
        if (!verdict) continue;
        const mk = (verdict === 'female' ? /\b(she|her|hers|herself)\b/i : /\b(he|him|his|himself)\b/i).exec(bio);
        const mAbs = m.index + mk.index;
        const sb = nextBoundary(p.text, mAbs);
        const qEnd = sb >= 0 && sb - mAbs < 240 ? sb + 1 : Math.min(p.text.length, mAbs + 120);
        const titled = p.text.slice(Math.max(0, m.index - 20), m.index).match(/((?:Pastor|Rev\.?|Reverend|Fr\.|Father|Mother|Dr\.|The)\s+)+$/);
        let quote = p.text.slice(m.index - (titled ? titled[0].length : 0), qEnd).trim();
        let more = [];
        if (quote.length > 420) { quote = sentenceAt(p.text, mAbs, mAbs + mk[0].length); more = [{ quote: sentenceAt(p.text, m.index, m.index + nd.length), url: p.url }]; }
        const sp = /\b(husband|wife|spouse|partner)\b/i.exec(bio);
        const spouse = sp ? { quote: sentenceAt(p.text, m.index + sp.index, m.index + sp.index + sp[0].length), url: p.url } : null;
        found.push({ verdict, fem, masc, quote, url: p.url, evidence_more: more, spouse, score: quality(quote, p.url) + Math.abs(fem - masc) - (mAbs - m.index) / 60 });
      }
    }
  }
  return found.sort((a, b) => b.score - a.score)[0] || null;
}
const FEMALE_MARK = /\b(she|her|hers|wife|woman|women|mother|mrs\.?|ms\.?|female|sister)\b/i;
const LGBT_RX = /open and affirming|reconciling (congregation|ministries|community|church)|more light (presbyterian|congregation)|reconciling in christ|\blgbtq?i?a?\+?|\bpride (month|sunday|service|celebration|parade|flag)|all sexual orientations|regardless of (your |their )?(sexual orientation|gender identity)|\bhis husband\b|\bher wife\b|marriage equality|\b(inclusive of|regardless of)\b[^.]{0,60}\b(sexual )?orientation/i;
const PROSPERITY_RX = /prosperity gospel|seed[- ]faith|sow (a|your) seed|word of faith|name it and claim it|hundred-?fold return/i;
const MENS_RX = /(?<![A-Za-z])men['’]?s (ministry|ministries|bible study|breakfast|group|fellowship|retreat|prayer|discipleship|small group)|\bbrotherhood\b|united methodist men|episcopal church men|\bmen of (faith|god|valor|the word|honor|grace)\b/i;
const KIDS_RX = /children['’]?s (ministry|ministries|church|chapel|programs?)|kids['’]? ?(ministry|church|zone|club)|sunday school|\bnursery\b|vacation bible school|\bvbs\b|\bawana\b|youth group|youth ministry/i;
const BIO_PENALTY = [/\b(served|serving) as\b|\bordain|seminary|graduat|\bpastor for\b|his wife|her husband|married|members at|call(ed)? to (ministry|serve)|appointed|degree|school for/i, -4];
// The church's own name as printed on its site, e.g. "St. Mary's Episcopal Church":
// the cleanest affiliation evidence there is.
function nameAffiliation(o, c, rx) {
  const toks = String(c.name || '').replace(/[’]/g, "'").replace(/\b(st\.?|saint|church|the|of|chapel|umc|parish|united|methodist|episcopal|lutheran|presbyterian)\b/gi, ' ').trim().split(/\s+/).filter(t => t.length >= 3);
  if (!toks.length) return null;
  const out = [];
  for (const p of (o && o.pages) || []) {
    if (!p.text) continue;
    const g = new RegExp(rx.source, rx.flags.includes('g') ? rx.flags : rx.flags + 'g');
    let m, n = 0;
    while ((m = g.exec(p.text)) && n++ < 30) {
      const w0 = Math.max(0, m.index - 50);
      const win = p.text.slice(w0, m.index + m[0].length).replace(/[’]/g, "'");
      const hitsT = [...win.matchAll(new RegExp(`\\b${esc(toks[0])}\\b`, 'g'))];
      if (!hitsT.length) continue;
      let a = w0 + hitsT[hitsT.length - 1].index;
      const pre = p.text.slice(Math.max(0, a - 20), a).match(/((?:St\.|Saint|The|Church of the)\s+)$/);
      if (pre) a -= pre[1].length;
      let b = m.index + m[0].length;
      const tail = p.text.slice(b).match(/^(\s+(Church|Parish|Chapel))\b/);
      if (tail) b += tail[1].length;
      const q = p.text.slice(a, b).trim();
      if (q.length <= 90 && !out.some(x => x.quote === q)) out.push({ quote: q, url: p.url, score: 6 + ({ about: 1, staff: 0, home: 1, other: 0 })[PAGE_KIND(p.url)] });
    }
  }
  return out.sort((x, y) => y.score - x.score)[0] || null;
}

// ── roster: only people the page ties to THIS church, with a real role ───────
// A role is an office (Rector, Associate Rector, Senior Pastor, Youth Pastor),
// never an honorific (Rev., Dr., Fr.). A name counts only with its surname on
// the cited page, only where the page ties it to this church (staff/clergy page,
// or prose naming the role here), and never in a joint-ministry, guest or
// partner context ("… with Aquia Episcopal Church … led by Fr. James …").
const ROLE_RX = /\b((?:senior|lead|associate|assistant|executive|youth|children['’]?s|student|worship|music|family|interim|teaching|discipleship|outreach|care|pastoral|parish)\s+)?(pastor|rector|vicar|priest[- ]in[- ]charge|priest|curate|deacon|minister|elder|chaplain)\b/i;
const HONORIFIC_ONLY = /^\s*(the\s+)?((very|right)\s+)?(rev\.?|reverend|dr\.?|fr\.?|father|mother|mtr\.?|pastor|bishop|mr\.?|mrs\.?|ms\.?)(\s+(dr\.?|rev\.?))?\s*\.?\s*$/i;
const NONCLERGY_RX = /\b(administrat\w*|assistant(?!\s+(pastor|rector|minister|priest|vicar))|director|coordinator|secretary|leader|treasurer|custodian|sexton|organist|pianist|accompanist|attendant|chair(man|woman|person)?|president|clerk|bookkeeper|manager|warden|vestry|music|staff member|volunteer)\b/i;
const GUEST_RX = /\b(guest|visiting|partner(ship)?|joint(ly)?|co-?host(ed)?|hosted by|special speaker|preacher from|formerly|former|retired|emerit\w*|in memory|memorial service)\b/i;
const CHURCH_PHRASE_RX = /\b(?:with|from|at|of|or)\s+(?:the\s+)?((?:[A-Z][\w'’.-]*\s+){1,5}(?:Church|Parish|Cathedral|Chapel|UMC))\b/g;
const titleCase = s => s.toLowerCase().replace(/\b[a-z]/g, m => m.toUpperCase()).replace(/\bIn\b/g, 'in');
function roleFrom(s) { const m = ROLE_RX.exec(String(s || '')); return m ? titleCase(m[0].replace(/\s+/g, ' ')) : null; }
function ourTokens(c) {
  return String(c.name || '').replace(/[’]/g, "'").replace(/\b(st\.?|saint|church|the|of|chapel|umc|parish|united|methodist|episcopal|lutheran|presbyterian|baptist)\b/gi, ' ').split(/\s+/).filter(t => t.length >= 3);
}
function rosterTie(o, c, person, isLead) {
  const name = String(person.name || '').trim();
  const k = nameKey(name);
  if (!k || name.split(/\s+/).length < 2) return { ok: false, why: 'no surname' };
  const toks = ourTokens(c);
  const cands = [];
  for (const p of (o && o.pages) || []) {
    if (!p.text) continue;
    const g = new RegExp(`\\b${esc(name)}\\b`, 'g');
    let m, n = 0;
    while ((m = g.exec(p.text)) && n++ < 10) {
      // the section around the name (a joint-ministry heading can sit a paragraph above it)
      const win = p.text.slice(Math.max(0, m.index - 420), Math.min(p.text.length, m.index + name.length + 220));
      const quote = sentenceAt(p.text, m.index, m.index + name.length);
      const foreign = [...win.matchAll(CHURCH_PHRASE_RX)].map(x => x[1]).filter(ph => !toks.some(t => ph.includes(t)) && !/Diocese/.test(ph));
      if (foreign.length || GUEST_RX.test(quote)) { cands.push({ bad: foreign.length ? `named alongside ${foreign[0]}` : 'guest/partner/former context', url: p.url }); continue; }
      // The role phrase attached to THIS name: "Name – Associate Rector", "Name, Pastor",
      // or "Associate Rector Name" — but not the previous person's role in a
      // "Name – Role Name – Role" list (a role right after a dash belongs to the name before it).
      const after = p.text.slice(m.index + name.length, m.index + name.length + 80);
      const am = after.match(/^\s*(?:[,–—:|]|-\s|\s-)?\s*(?:the\s+)?((?:[A-Z][\w'’]*|of|and|&)(?:\s+(?:[A-Z][\w'’]*|of|and|&)){0,5})/);
      const afterPhrase = am ? am[1] : '';
      const before = p.text.slice(Math.max(0, m.index - 45), m.index).replace(/((the\s+)?(rev\.?|reverend|dr\.?|fr\.?|father|mother)\s*)+$/i, '');
      const bm = before.match(new RegExp(`(${ROLE_RX.source})\\s+$`, 'i'));
      const beforeRole = bm && !/[–—-]\s*$/.test(before.slice(0, before.length - bm[0].length)) ? bm[1] : null;
      const roleProse = new RegExp(`\\b${esc(name)}\\b[^.]{0,80}\\b(is|serves as|was called (to be |as )?|became|has served as|joined us as)\\s+(our|the|an?)?\\s*${ROLE_RX.source}`, 'i').test(quote);
      const phrase = [afterPhrase, beforeRole, roleProse ? quote : null, !HONORIFIC_ONLY.test(person.role || '') ? person.role : null].find(x => x && (ROLE_RX.test(x) || NONCLERGY_RX.test(x)));
      const rawRole = phrase ? (ROLE_RX.test(phrase) && !(NONCLERGY_RX.test(phrase) && NONCLERGY_RX.exec(phrase).index < ROLE_RX.exec(phrase).index) ? roleFrom(phrase) : null) : null;
      const nonClergy = phrase && (!rawRole || /^(music|worship)\b/i.test(rawRole)) ? (phrase.match(NONCLERGY_RX) || [rawRole])[0] : null;
      if (nonClergy) { cands.push({ bad: `non-clergy role ("${clip(phrase, 40)}")`, nonclergy: true, url: p.url }); continue; }
      const role = rawRole;
      const tied = PAGE_KIND(p.url) === 'staff' || roleProse || (role && PAGE_KIND(p.url) !== 'other');
      if (!tied) { cands.push({ bad: 'not tied to this church on the page (no staff page, no role here)', url: p.url }); continue; }
      cands.push({ ok: true, name, role, quote, url: p.url, score: quality(quote, p.url, [[ROLE_RX, 2], [new RegExp(esc(name)), 1]]) + (role ? 2 : 0) });
    }
  }
  const good = cands.filter(x => x.ok).sort((a, b) => b.score - a.score);
  if (!good.length) return { ok: false, why: ((cands.find(x => /named alongside|guest/.test(x.bad || '')) || cands.find(x => x.nonclergy) || cands.find(x => x.bad)) || {}).bad || 'full name not on any fetched page' };
  const g0 = good[0];
  const role = g0.role || good.map(x => x.role).find(Boolean) || null;
  if (!role) return { ok: false, why: 'no pastoral role stated (non-clergy or unknown)', nonclergy: true };
  return { ok: true, name, role, quote: g0.quote, url: g0.url };
}

// ── service times as a SET of day+time tokens ("Sun 10:30 AM") ───────────────
// A page sentence and a stored value that list the same services are the same
// value; only a different SET is a change, and the change writes the structured
// value, never the page sentence.
const DAYS = [['Sun', /^sun/i], ['Mon', /^mon/i], ['Tue', /^tue/i], ['Wed', /^wed/i], ['Thu', /^thu/i], ['Fri', /^fri/i], ['Sat', /^sat/i]];
const NOT_WORSHIP = /^\s*[-–—:]?\s*(\(?[a-z ]{0,12}\)?\s*)?(sunday school|school|fellowship|class|classes|bible study|study|coffee|breakfast|office|hours|choir|rehearsal|adult ed|education|youth|nursery|meeting|lunch|dinner|potluck)/i;
function parseServiceTimes(str) {
  const s = String(str || '');
  const toks = new Set();
  const rx = /\b(sun(?:day)?s?|mon(?:day)?s?|tue(?:s(?:day)?)?s?|wed(?:nesday)?s?|thu(?:r(?:s(?:day)?)?)?s?|fri(?:day)?s?|sat(?:urday)?s?)\b|\b(noon)\b|\b(\d{1,2})(?::(\d{2}))?\s*(a\.?\s?m\.?|p\.?\s?m\.?)?(?![\d/])/gi;
  let day = null, m;
  const anyDay = /\b(sun|mon|tue|wed|thu|fri|sat)/i.test(s);
  const worshipy = /worship|service|eucharist|mass|liturg|rite|prayer|celebrat/i.test(s);
  while ((m = rx.exec(s))) {
    if (m[1]) { day = (DAYS.find(([, r]) => r.test(m[1])) || [null])[0]; continue; }
    let h, mi = '00', ap;
    if (m[2]) { h = 12; ap = 'PM'; }
    else {
      h = +m[3]; mi = m[4] || '00'; ap = m[5] ? (/p/i.test(m[5]) ? 'PM' : 'AM') : null;
      if (!m[4] && !m[5]) continue;                 // a bare number is not a time
      if (h < 1 || h > 12 || +mi > 59) continue;
      if (!ap) ap = h >= 7 && h <= 11 ? 'AM' : 'PM';
    }
    if (NOT_WORSHIP.test(s.slice(m.index + m[0].length, m.index + m[0].length + 30))) continue;
    const d = day || (!anyDay && worshipy ? 'Sun' : null);
    if (!d) continue;
    toks.add(`${d} ${h}:${mi} ${ap}`);
  }
  return toks;
}
const DAY_ORDER = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
const tmin = t => { const [, hm, ap] = t.split(' '); let [h, m] = hm.split(':').map(Number); if (ap === 'PM' && h !== 12) h += 12; if (ap === 'AM' && h === 12) h = 0; return h * 60 + m; };
function formatServiceTimes(set) {
  const by = {};
  for (const t of set) { const d = t.split(' ')[0]; (by[d] = by[d] || []).push(t); }
  return Object.keys(by).sort((a, b) => DAY_ORDER[a] - DAY_ORDER[b]).map(d => `${d} ` + by[d].sort((a, b) => tmin(a) - tmin(b)).map(t => t.split(' ').slice(1).join(' ')).join(', ')).join('; ');
}
const sameSet = (a, b) => a.size === b.size && [...a].every(x => b.has(x));

// ── per-church review ────────────────────────────────────────────────────────
function review(o) {
  const c = byId.get(o.id);
  const out = { id: o.id, name: o.name, page: pageUrl(o.id), selection_tier: o.selection_tier || null, status: o.status,
    source_kind: o.source_kind, site_read: o.final_url || null, pages_read: (o.pages || []).map(p => p.url),
    identity: o.identity ? { status: o.identity.status, matched: o.identity.matched, conflicting: o.identity.conflicting_locations || [] } : null,
    current: c ? { pastor: c.pastor || '', overall_rating: c.overall_rating || null, overall_label: c.overall_label || null } : null,
    changes: [], flags: [], rubric: {}, proposed_overall: null };
  if (!c) { out.status = 'missing_from_directory'; return out; }
  const add = ch => { if (ch.evidence && ch.evidence.quote && ch.evidence.url) out.changes.push(ch); };
  const holdAll = [];
  // A site that answered 200 but yielded no readable text is JS-rendered, not dead.
  if (o.status === 'unreachable' && (o.attempts || []).some(a => a.status === 200)) out.status = o.status = 'unreadable';
  if (o.website_is_social) {
    const k = /youtu/i.test(o.website_is_social) ? 'youtube' : /instagram/i.test(o.website_is_social) ? 'instagram' : 'facebook';
    add({ field: 'website', op: 'replace', old: c.website, new: '', confidence: 'medium', hold_reasons: ['website field holds a social URL'],
      reason: `website field is a ${k} URL; move it to ${k}`, evidence: ev(c.website, c.website, { evidence_type: 'stored_value' }),
      also_sets: c[k] ? null : { [k]: o.website_is_social } });
  }

  if (o.status === 'unreachable' || o.status === 'unreadable') {
    out.flags.push({ type: o.status === 'unreadable' ? 'site_unreadable_js' : 'site_unreachable', detail: (o.attempts || []).map(a => `${a.url} -> ${a.status}`).slice(0, 3).join('; '),
      gate: 'info', note: 'No change proposed. A dead site is not a doctrinal flag (methodology §III).' });
  }

  // Wrong-church data: everything read from this site describes someone else.
  let L = o.llm || {}, src = o, siteHost = hostOf(o.final_url || '');
  if (o.status === 'identity_mismatch') {
    const conf = (o.identity.conflicting_locations || [])[0];
    const e = ev(conf && conf.quote, conf && conf.url);
    out.flags.push({ type: 'data_belongs_to_other_church', gate: 'hold', evidence: e,
      detail: `Stored website ${c.website} describes a congregation outside ${o.identity.stored.city}, ${o.identity.stored.state}; nothing on it names the stored city, street or ZIP.` });
    const rec = o.recovery || {};
    const recovered = rec.site && rec.review && (rec.review.identity || {}).status === 'confirmed' ? rec.review : null;
    // A recovered site is proposed with the quote that carries the stored street
    // address on it (always HOLD; a new website is an identity change).
    const stA = o.identity.stored || {};
    const addrQ = recovered && stA.street_no && stA.street_word
      ? best(scan(recovered, new RegExp(`\\b${esc(stA.street_no)}\\s+${esc(stA.street_word)}`, 'i')), [[new RegExp(esc(stA.city || '#'), 'i'), 3]]) : null;
    const via = recovered ? ((rec.candidates || []).find(x => x.url === rec.site) || {}).via || 'search' : null;
    if (recovered && addrQ) {
      add({ field: 'website', op: 'replace', old: c.website || null, new: rec.site, confidence: 'low',
        reason: `${via} found a site that prints the stored address (${(rec.review.identity.matched || []).join(', ')})`,
        evidence: ev(addrQ.quote, addrQ.url), evidence_more: e ? [{ ...e, why: 'stored website describes another church' }] : [] });
    } else {
      add({ field: 'website', op: 'research', old: c.website || null, new: null, confidence: 'low',
        reason: 'stored site is another church; no candidate site (name-domain probe, local search) prints the stored address',
        evidence: e, evidence_more: [{ quote: `tried: ${(rec.candidates || []).map(x => x.url).join(', ') || 'none'}; search: ${rec.query || 'n/a'}`, url: 'http://127.0.0.1:8888 (SearXNG, local)' }] });
    }
    holdAll.push('identity_mismatch');
    // Stored pastor/roster that came off the wrong site.
    const wrongLead = L.lead_pastor;
    if (c.pastor && !isPlaceholderPastor(c.pastor) && onPages(o, nameKey(c.pastor) ? c.pastor.replace(/\(.*?\)/g, '').trim() : '')) {
      const q = wrongLead && sameName(wrongLead.name, c.pastor) ? (wrongLead.quote || wrongLead.name) : c.pastor;
      const u = wrongLead && sameName(wrongLead.name, c.pastor) ? wrongLead.url : (o.pages[0] || {}).url;
      add({ field: 'pastor', op: 'clear', old: c.pastor, new: '', confidence: 'medium', reason: 'stored pastor is listed on the other church\'s site', evidence: ev(q, u), evidence_more: e ? [e] : [] });
      if (Array.isArray(c.pastors) && c.pastors.length) add({ field: 'pastors', op: 'clear', old: c.pastors, new: [], confidence: 'medium', reason: 'roster came from the other church\'s site', evidence: ev(q, u) });
    }
    if (!recovered) { finishGates(out, c, holdAll); dupFlags(out, c, o); return out; }
    L = recovered.llm || {}; src = recovered; siteHost = hostOf(rec.site);
    holdAll.push('recovered_site');
  }
  if (o.status !== 'reviewed' && src === o) { finishGates(out, c, holdAll); dupFlags(out, c, o); return out; }
  if (src.identity && src.identity.status !== 'confirmed') holdAll.push('identity_unconfirmed');

  // ── 1. pastor + roster ────────────────────────────────────────────────────
  const lead = L.lead_pastor;
  const rulings = out.rulings = [];
  const ruling = r => { if (r.evidence && r.evidence.quote && r.evidence.url) rulings.push(r); };
  let femaleLead = null;          // { name, g } — confirmed by page evidence
  let genderPerson = null;        // the lead (or stored pastor) whose gender we test
  if (lead && lead.name) genderPerson = { name: lead.name, url: lead.url };
  else if (c.pastor && !isPlaceholderPastor(c.pastor)) {
    const bare = c.pastor.replace(/\(.*?\)/g, ' ').replace(TITLE_RE, ' ').replace(/\s+/g, ' ').trim();
    if (onPages(src, bare)) genderPerson = { name: bare, url: null, stored: true };
  }
  if (genderPerson) {
    const g = genderEvidence(src, genderPerson.name);
    if (g && g.verdict === 'female') femaleLead = { name: genderPerson.name, g };
    else if (!g && (looksFemaleFirstName(genderPerson.name) || (lead && lead.pronoun === 'she' && !genderPerson.stored))) {
      const nq = best(scan(src, new RegExp(`\\b${esc(genderPerson.name)}\\b`), [[/pastor|rector|priest|minister|vicar/i, 2]]));
      ruling({ type: 'unconfirmed', title: `unconfirmed: female lead pastor "${genderPerson.name}" (first-name list only; no pronoun, spouse or explicit role on the page)`,
        suggested: 'red', supported: null, evidence: nq ? ev(nq.quote, nq.url) : null,
        note: 'No rating is proposed from a name list. QA: confirm from the church (bio, photo, phone) before any RED.' });
    }
    if (g) genderPerson.g = g;
  }
  if (lead && lead.name) {
    // Strongest quote naming the lead: a staff/about sentence beats nav text.
    // For a female lead the pronoun bio is the better pastor evidence (it carries name, role and gender).
    const gq = femaleLead && !genderPerson.stored && /pastor|rector|priest|minister|vicar/i.test(femaleLead.g.quote) ? { quote: femaleLead.g.quote, url: femaleLead.g.url } : null;
    const hasName = x => x && nrm(x.quote).includes(nrm(lead.name));
    const leadQ = best([lead.quote ? { quote: lead.quote, url: lead.url } : null,
      ...scan(src, new RegExp(`\\b${esc(lead.name)}\\b`))].filter(hasName), [[/pastor|rector|priest|minister|vicar|senior|lead/i, 2]]) || { quote: lead.name, url: lead.url };
    const e = ev(leadQ.quote, leadQ.url, gq && !nrm(leadQ.quote).includes(nrm(gq.quote)) ? { bio_quote: gq.quote, bio_url: gq.url } : {});
    const leadRole = LEAD_ROLE.test(lead.role || '') && !NONLEAD_ROLE.test(lead.role || '');
    const unconfirmedFemale = rulings.some(r => r.type === 'unconfirmed');
    if (c.pastor && !isPlaceholderPastor(c.pastor) && sameName(lead.name, c.pastor)) {
      add({ field: 'pastor_source', op: 'confirm', old: c.pastor_source || null, new: leadQ.url, confidence: 'high', reason: `stored pastor "${c.pastor}" confirmed on the church's own site`, evidence: e });
      add({ field: 'pastor_fetched_at', op: 'confirm', old: c.pastor_fetched_at || null, new: TODAY, confidence: 'high', reason: 'stamp', evidence: e });
    } else {
      const placeholder = isPlaceholderPastor(c.pastor);
      const storedStillListed = !placeholder && onPages(src, (nameKey(c.pastor) || {}).full ? c.pastor.replace(/\(.*?\)/g, '').replace(TITLE_RE, ' ').replace(/\s+/g, ' ').trim() : '');
      const reasons = [];
      if (!lead.quote) reasons.push('no role sentence quoted');
      if (!leadRole) reasons.push(`role "${lead.role || '?'}" not clearly senior/lead`);
      if (femaleLead) reasons.push('female senior/lead pastor (page evidence) -> RED minimum; QA');
      if (unconfirmedFemale) reasons.push('female lead unconfirmed (first-name list only)');
      if (storedStillListed) reasons.push(`stored "${c.pastor}" still appears on the site`);
      const high = !reasons.length;
      add({ field: 'pastor', op: placeholder ? 'set' : 'replace', old: c.pastor || '', new: lead.name, role: lead.role || null,
        confidence: high ? 'high' : 'medium', reason: high ? (placeholder ? 'lead named verbatim with role on own site' : `stored "${c.pastor}" not on the site; current lead named verbatim with role`) : reasons.join('; '),
        hold_reasons: high ? [] : reasons, evidence: e });
      add({ field: 'pastor_source', op: 'set', old: c.pastor_source || null, new: leadQ.url, confidence: high ? 'high' : 'medium', hold_reasons: high ? [] : ['rides with pastor change'], reason: 'source of the pastor value', evidence: e, rides_with: 'pastor' });
      add({ field: 'pastor_fetched_at', op: 'set', old: c.pastor_fetched_at || null, new: TODAY, confidence: high ? 'high' : 'medium', hold_reasons: high ? [] : ['rides with pastor change'], reason: 'stamp', evidence: e, rides_with: 'pastor' });
    }
    const leadTie = rosterTie(src, c, lead, true);
    const tied = [], excluded = [];
    for (const p of (L.roster || []).filter(p => !sameName(p.name, lead.name)).slice(0, 12)) {
      const t = rosterTie(src, c, p, false);
      if (t.ok) tied.push(t); else excluded.push({ name: p.name, model_role: p.role || null, why: t.why });
    }
    out.roster = { kept: tied.map(t => ({ name: t.name, role: t.role, url: t.url })), excluded };
    if (tied.length && leadTie.ok) {
      const team = [{ name: lead.name, role: (leadTie.role || roleFrom(lead.role) || 'Pastor').slice(0, 60) }, ...tied.slice(0, 8).map(t => ({ name: t.name, role: t.role.slice(0, 60) }))];
      const cur = Array.isArray(c.pastors) ? c.pastors : [];
      const same = cur.length === team.length && cur.every((p, i) => sameName(p.name, team[i].name));
      if (!same) add({ field: 'pastors', op: cur.length ? 'replace' : 'set', old: cur, new: team, confidence: 'medium', reason: 'clergy roster as the church site lists it (each name tied to this church with a role)', hold_reasons: [],
        evidence: ev(leadQ.quote, leadQ.url), evidence_more: tied.slice(0, 8).map(t => ev(t.quote, t.url, { name: t.name, role: t.role })), rides_with: 'pastor' });
    }
  }

  // ── 2. rubric: written rules only ─────────────────────────────────────────
  const hits = []; // { rule, evidence, evidence_more, basis }
  if (femaleLead && RULES.female_senior.published) {
    const g = femaleLead.g;
    hits.push({ rule: RULES.female_senior, basis: `female senior/lead pastor (${femaleLead.name}); the site's own bio uses "${g.fem > 0 ? 'she/her' : ''}"`,
      evidence: ev(g.quote, g.url), evidence_more: dedupeEv([...(g.evidence_more || []), g.spouse].filter(Boolean).map(x => ev(x.quote, x.url)), g) });
  }
  const prior = denomPrior(c);
  if (prior && prior.affirming && RULES.affirming_denom.published) {
    // Affiliation from the church's own name/about text, not a pastor's bio.
    const nameTok = String(c.name || '').replace(/\b(st\.?|saint|church|the|of|chapel|umc|parish)\b/gi, ' ').trim().split(/\s+/).filter(t => t.length >= 3)[0];
    const prefer = [[/\b(our (church|parish|congregation)|we are|is (a|an) (member|part|parish|congregation)|part of the|member of)\b/i, 2], BIO_PENALTY];
    if (nameTok) prefer.push([new RegExp(`\\b${esc(nameTok)}`, 'i'), 3]);
    const rx = AFFILIATION_RE[prior.key];
    const named = rx && nameAffiliation(src, c, rx);
    const aff = named || (rx && best([L.denomination_affiliation && rx.test(L.denomination_affiliation.quote) ? L.denomination_affiliation : null, ...scan(src, rx, prefer)], prefer));
    if (aff && (named || quality(aff.quote, aff.url, prefer) > -2)) {
      hits.push({ rule: RULES.affirming_denom, basis: `${prior.label} (stated on the church's own site) is on the published LGBTQ-affirming list`, evidence: ev(aff.quote, aff.url), evidence_more: [] });
    }
  }
  const pros = RULES.prosperity.published ? scan(src, PROSPERITY_RX)[0] : null;
  if (pros) hits.push({ rule: RULES.prosperity, basis: 'prosperity-gospel language on the church site', evidence: ev(pros.quote, pros.url), evidence_more: [] });

  // Category scores: only from a rule that names that category, with an on-topic quote.
  for (const d of DIMS) {
    const cur = (c.scores || {})[d] || null;
    const hs = hits.filter(h => h.rule.dims.includes(d) && h.evidence && onTopic(d, h.evidence.quote)).sort((a, b) => SEV[b.rule.level] - SEV[a.rule.level]);
    const model = (L.rubric || {})[d];
    const modelInfo = model ? { level: model.lean, quote: model.quote, url: model.url, on_topic: onTopic(d, model.quote) } : null;
    if (!hs.length) {
      out.rubric[d] = { current: cur, proposed: null, reason: 'no published rule maps the evidence to a level', model_suggested: modelInfo };
      continue;
    }
    const h = hs[0];
    const note = `${LABEL[d]}: ${h.rule.text} — "${clip(h.evidence.quote, 150)}"`;
    out.rubric[d] = { current: cur, proposed: h.rule.level, rule: ruleCite(h.rule), basis: h.basis, evidence: h.evidence, note, model_suggested: modelInfo };
    if (cur !== h.rule.level && SEV[h.rule.level] > SEV[cur || 'green'] - (cur ? 0 : 99)) {
      add({ field: `scores.${d}`, op: cur ? 'replace' : 'set', old: cur, new: h.rule.level, confidence: 'medium',
        hold_reasons: [`category to ${h.rule.level.toUpperCase()}`, ...(cur === 'green' ? ['category off GREEN'] : [])], reason: h.basis,
        rule: ruleCite(h.rule), evidence: h.evidence, evidence_more: h.evidence_more,
        also_sets: { [`score_notes.${d}`]: note, [`score_sources.${d}`]: h.evidence.url } });
    }
  }

  // Overall: the highest level any fired rule supports. No rule, no change.
  const curO = c.overall_rating || null;
  const ovHits = hits.filter(h => h.evidence).sort((a, b) => SEV[b.rule.level] - SEV[a.rule.level]);
  const supported = ovHits.length ? ovHits[0].rule.level : null;
  if (supported && SEV[supported] > SEV[curO || 'green'] - (curO ? 0 : 99) && supported !== curO) {
    const top = ovHits[0];
    const label = `${supported.toUpperCase()} — ${ovHits.map(h => h.rule.short).filter((v, i, a) => a.indexOf(v) === i).join('; ')}. Rule: "${top.rule.text}" (${METHODOLOGY_URL}). Evidence: "${clip(top.evidence.quote, 140)}" (${top.evidence.url}). Full review ${TODAY}.`;
    out.proposed_overall = { current: curO, proposed: supported, label, rules: ovHits.map(h => ruleCite(h.rule)), drivers: ovHits.map(h => h.basis), evidence: top.evidence };
    add({ field: 'overall_rating', op: 'replace', old: curO, new: supported, confidence: 'medium',
      hold_reasons: [`moves to ${supported.toUpperCase()}`, ...(curO === 'green' ? ['moves off GREEN'] : [])], reason: ovHits.map(h => h.basis).join('; '),
      rule: ruleCite(top.rule), evidence: top.evidence,
      evidence_more: dedupeEv(ovHits.slice(1).map(h => ({ ...h.evidence, rule: h.rule.text })).concat(top.evidence_more || []), top.evidence),
      also_sets: { overall_label: label } });
  } else {
    out.proposed_overall = { current: curO, proposed: curO, label: null, rules: ovHits.map(h => ruleCite(h.rule)), note: ovHits.length ? 'published rules agree with the current rating' : 'no published rule fired; rating unchanged' };
  }

  // Needs-ruling: what the model or a keyword signal suggests beyond the rules.
  const lgbtCands = [L.lgbt_affirming, ...scan(src, LGBT_RX)].filter(x => x && x.quote);
  const gp = genderPerson && genderPerson.g;
  const sameSexSpouse = gp && gp.verdict === 'male' && gp.spouse && (/\bhusband\b/i.test(gp.spouse.quote) ||
    (/\bspouse,?\s+([A-Z][a-z]+)/.test(gp.spouse.quote) && !looksFemaleFirstName(/\bspouse,?\s+([A-Z][a-z]+)/.exec(gp.spouse.quote)[1] + ' X')));
  if (lgbtCands.length || sameSexSpouse) {
    const lb = best(lgbtCands, [[/affirming|lgbt|pride|reconciling|husband|wife/i, 2]]);
    const evid = lb ? ev(lb.quote, lb.url) : ev(gp.spouse.quote, gp.spouse.url);
    const more = [];
    if (sameSexSpouse && lb) more.push({ ...ev(gp.spouse.quote, gp.spouse.url), why: `the ${genderPerson.stored ? 'stored pastor' : 'lead pastor'} (${genderPerson.name}, referred to as "he") has a spouse named on the page` });
    lgbtCands.filter(x => x !== lb && nrm(x.quote).replace(/^st\.? /, '') !== nrm(lb && lb.quote).replace(/^st\.? /, '') && !nrm(lb && lb.quote).includes(nrm(x.quote)) && !nrm(x.quote).includes(nrm(lb && lb.quote)))
      .slice(0, 2).forEach(x => more.push(ev(x.quote, x.url)));
    if (SEV.black > SEV[supported || 'yellow']) ruling({ type: 'needs-ruling', title: 'needs-ruling: model suggests BLACK', suggested: 'black', supported: supported || null,
      dims: ['overall', 'gender', 'cultural'], evidence: evid, evidence_more: more.filter(Boolean),
      note: `No published rule maps this evidence to BLACK (the only BLACK rule is "${RULES.prosperity.text}"). Highest level a rule supports: ${(supported || 'none').toUpperCase()}. Chaps and Adam decide; if they rule, publish the rule on the methodology page.` });
  }
  const womenQ = [L.women_in_office && FEMALE_MARK.test(L.women_in_office.quote) ? L.women_in_office : null];
  for (const p of ((out.roster || {}).kept || []).filter(p => !/deacon/i.test(p.role || ''))) {
    const g = genderEvidence(src, p.name);
    if (g && g.verdict === 'female') womenQ.push({ quote: g.quote, url: g.url, who: p.name });
    else if (!g && looksFemaleFirstName(p.name)) {
      const nq = best(scan(src, new RegExp(`\\b${esc(p.name)}\\b`)));
      ruling({ type: 'unconfirmed', title: `unconfirmed: "${p.name}" (${p.role}) read as a woman in pastoral office from the first-name list only`, suggested: 'red', supported: null, dims: ['gender', 'leadership'], evidence: nq ? ev(nq.quote, nq.url) : null, note: 'No rating proposed from a name list.' });
    }
  }
  const wq = best(womenQ.filter(Boolean));
  if (wq && !femaleLead) ruling({ type: 'needs-ruling', title: 'needs-ruling: women in pastoral office (not the senior pastor) — model suggests gender/leadership RED', suggested: 'red', supported: null,
    dims: ['gender', 'leadership'], evidence: ev(wq.quote, wq.url), note: `The published rule covers a female SENIOR pastor only ("${RULES.female_senior.text}"). Chaps and Adam decide whether women in other pastoral offices map to RED.` });
  // model leans of RED/BLACK on-topic, in a category no rule scored
  for (const d of DIMS) {
    const r = out.rubric[d];
    const m = r && r.model_suggested;
    if (!m || r.proposed || !m.on_topic || SEV[m.level] < 2) continue;
    if (rulings.some(x => (x.dims || []).includes(d))) continue;
    ruling({ type: 'needs-ruling', title: `needs-ruling: model suggests ${LABEL[d]} ${m.level.toUpperCase()}`, suggested: m.level, supported: null, dims: [d], evidence: ev(m.quote, m.url), note: 'Local-model reading; no published rule maps it.' });
  }

  // ── 3. profile fill ───────────────────────────────────────────────────────
  const st = L.service_times;
  if (st) {
    const have = c.service_times || (typeof c.services === 'string' ? c.services : '');
    const placeholder = !have || /see website|verify|^sunday morning \(see/i.test(have);
    const pageSet = parseServiceTimes(st.quote), haveSet = parseServiceTimes(have);
    out.service_times = { stored: have || null, stored_tokens: [...haveSet], page_tokens: [...pageSet] };
    if (pageSet.size && (placeholder || !haveSet.size || !sameSet(pageSet, haveSet))) {
      const value = formatServiceTimes(pageSet);
      if (placeholder || !have) add({ field: 'service_times', op: 'fill', old: have || null, new: value, confidence: 'high', reason: `times read from the church site: {${[...pageSet].join(', ')}}`, evidence: ev(st.quote, st.url) });
      else add({ field: 'service_times', op: 'replace', old: have, new: value, confidence: 'medium', hold_reasons: [haveSet.size ? `stored {${[...haveSet].join(', ')}} != site {${[...pageSet].join(', ')}}` : 'stored value has no parseable day+time'], reason: 'site lists a different set of service times', evidence: ev(st.quote, st.url) });
    }
  }
  const sig = k => firstSignal(src, k);
  const fd = L.founded || (sig('founded') ? { quote: sig('founded').quote, url: sig('founded').url, year: +((sig('founded').match.match(/\d{4}/) || [])[0]) } : null);
  if (fd && fd.year) {
    const have = String(c.founded || '');
    if (!have || /see website|unknown|verify/i.test(have)) add({ field: 'founded', op: 'fill', old: have || null, new: String(fd.year), confidence: 'high', reason: 'founding year stated on site', evidence: ev(fd.quote, fd.url) });
    else if (!have.includes(String(fd.year))) add({ field: 'founded', op: 'replace', old: have, new: String(fd.year), confidence: 'medium', hold_reasons: ['replaces existing founded value'], reason: 'site states a different year', evidence: ev(fd.quote, fd.url) });
  }
  for (const [field, q, rx] of [['has_mens_ministry', L.mens_ministry, MENS_RX], ['has_kids_ministry', L.kids_ministry, KIDS_RX]]) {
    const e = best([q && rx.test(q.quote) ? q : null, ...scan(src, rx)].filter(Boolean), [[rx, 1]]);
    if (e && c[field] !== true) add({ field, op: 'set', old: c[field] ?? null, new: true, confidence: 'high', reason: 'ministry named on the church site', evidence: ev(e.quote, e.url) });
  }
  const homeUrl = src.final_url || (src.pages && src.pages[0] && src.pages[0].url);
  for (const k of ['facebook', 'instagram', 'youtube']) {
    const v = (src.socials || {})[k];
    if (!v) continue;
    // harvest junk: numeric post/photo ids and share widgets are not an account
    const seg = urlPath(v).split('/').filter(Boolean)[0] || '';
    if (/^\d{1,6}$/.test(seg) || /^(sharer|share|plugins|tr|dialog|groups|events|watch)$/i.test(seg)) continue;
    if (!c[k]) add({ field: k, op: 'fill', old: null, new: v, confidence: 'high', reason: 'link published on the church site', evidence: ev(`<a href="${v}">`, homeUrl, { evidence_type: 'html_link' }) });
    else if (hostOf(c[k]) === hostOf(v) && urlPath(c[k]) !== urlPath(v) && !/facebook\.com\/(people|pages)\//i.test(v)) add({ field: k, op: 'replace', old: c[k], new: v, confidence: 'medium', hold_reasons: ['replaces existing social link'], reason: 'site links a different account', evidence: ev(`<a href="${v}">`, homeUrl, { evidence_type: 'html_link' }) });
  }
  if (src === o && o.final_url && hostOf(o.final_url) && hostOf(c.website) && hostOf(o.final_url) !== hostOf(c.website) && !/wix|squarespace/.test(hostOf(o.final_url))) {
    add({ field: 'website', op: 'replace', old: c.website, new: o.final_url, confidence: 'medium', hold_reasons: ['site redirects to a new domain'], reason: 'stored site redirects here', evidence: ev(`redirect ${c.website} -> ${o.final_url}`, o.final_url, { evidence_type: 'http_redirect' }) });
  }
  // Address: only a full street + ZIP quote that disagrees with the stored one.
  const loc = L.location;
  const ak = addrKey(c);
  if (loc && ak) {
    const m = loc.quote.replace(/(\d)\s+(?=\d)/g, '$1').match(/\b(\d{1,6})\s+([A-Za-z]+)[^]*?\b(\d{5})\b/);
    if (m && `${m[1]}|${m[2].toLowerCase()}|${m[3]}` !== ak && (m[3] !== ak.split('|')[2] || m[1] !== ak.split('|')[0])) {
      add({ field: 'address', op: 'replace', old: c.address, new: clip(loc.quote, 160), confidence: 'medium', hold_reasons: ['address correction (re-geocode after approval)'], reason: 'site gives a different street address/ZIP', evidence: ev(loc.quote, loc.url) });
    }
  }

  // A recovered site that names the current pastor supersedes the plain "clear"
  // of the wrong-church name: keep one pastor change, carrying both pieces of evidence.
  const rep = out.changes.find(x => x.field === 'pastor' && x.op !== 'clear');
  const clr = out.changes.find(x => x.field === 'pastor' && x.op === 'clear');
  if (rep && clr) {
    rep.evidence_more = dedupeEv([...(rep.evidence_more || []), { ...clr.evidence, why: 'stored pastor is listed on the other church\'s site' }], rep.evidence);
    out.changes = out.changes.filter(x => x !== clr);
  }
  finishGates(out, c, holdAll);
  dupFlags(out, c, src);
  return out;
}

// ── duplicates (flag only; merge is the existing tool's job) ─────────────────
function dupFlags(out, c, o) {
  const seen = new Set();
  const k = addrKey(c);
  for (const other of (k && byAddr.get(k)) || []) {
    if (other === c.id || seen.has(other)) continue;
    seen.add(other);
    const oc = byId.get(other);
    out.flags.push({ type: 'possible_duplicate', basis: 'same street address + ZIP', other_id: other, gate: 'hold',
      evidence: ev(oc.address, pageUrl(other), { this_address: c.address }),
      action: 'QA: confirm same congregation, then merge with scripts/merge-duplicate-churches.js (never delete; merged_from + redirect stub).' });
  }
  for (const h of [hostOf(c.website), hostOf(o && o.final_url)].filter(x => x && !GENERIC_HOSTS.test(x))) {
    for (const other of byHost.get(h) || []) {
      if (other === c.id || seen.has(other)) continue;
      seen.add(other);
      const oc = byId.get(other);
      out.flags.push({ type: 'possible_duplicate', basis: 'same website host', other_id: other, gate: 'hold',
        evidence: ev(oc.website, pageUrl(other), { this_website: c.website }),
        action: 'QA: same church (merge with scripts/merge-duplicate-churches.js) or a shared/borrowed site (fix the wrong record).' });
    }
  }
}

// ── gates ────────────────────────────────────────────────────────────────────
function finishGates(out, c, holdAll) {
  // A church whose overall rating is held holds its rubric changes with it.
  const ov = out.changes.find(x => x.field === 'overall_rating');
  const ovHeld = ov && ((ov.hold_reasons || []).length || ov.confidence !== 'high' || holdAll.length);
  const pastorCh = out.changes.find(x => x.field === 'pastor');
  const pastorHeld = pastorCh && ((pastorCh.hold_reasons || []).length || pastorCh.confidence !== 'high' || holdAll.length);
  for (const ch of out.changes) {
    const reasons = [...(ch.hold_reasons || []), ...holdAll];
    if (ch.field.startsWith('scores.') && ovHeld) reasons.push('rides with held overall rating');
    if (ch.rides_with === 'pastor' && pastorHeld) reasons.push('rides with held pastor change');
    if (ch.confidence !== 'high' && !reasons.length) reasons.push(`${ch.confidence} confidence`);
    ch.hold_reasons = [...new Set(reasons)];
    ch.gate = ch.hold_reasons.length ? 'hold' : 'auto';
    delete ch.rides_with;
  }
  // Last line of defence: no quote or no URL = no change.
  out.changes = out.changes.filter(ch => ch.evidence && ch.evidence.quote && ch.evidence.url);
  out.changes.forEach((ch, i) => { ch.change_id = `${ROUND}:${out.id}:${i + 1}`; });
}

// ── run ──────────────────────────────────────────────────────────────────────
const results = observations.map(review);
const holds = [];
for (const r of results) {
  for (const ch of r.changes.filter(x => x.gate === 'hold')) {
    holds.push({ hold_id: ch.change_id, round: ROUND, dry_run: DRY, church_id: r.id, church_name: r.name, page: r.page, kind: 'change',
      field: ch.field, old: ch.old, new: ch.new, also_sets: ch.also_sets || null, hold_reasons: ch.hold_reasons, reason: ch.reason,
      rule: ch.rule || null, evidence: ch.evidence, evidence_more: ch.evidence_more || [], qa_status: 'pending', qa_by: null, qa_note: null });
  }
  // Rulings never apply. They ask Chaps/Adam for a decision (and, if ruled, a published rule).
  for (const [i, x] of (r.rulings || []).entries()) {
    holds.push({ hold_id: `${ROUND}:${r.id}:ruling${i + 1}`, round: ROUND, dry_run: DRY, church_id: r.id, church_name: r.name, page: r.page,
      kind: x.type === 'unconfirmed' ? 'unconfirmed' : 'ruling', field: null, title: x.title, suggested: x.suggested, supported_by_rule: x.supported,
      dims: x.dims || null, note: x.note || null, evidence: x.evidence, evidence_more: x.evidence_more || [], qa_status: 'pending', qa_by: null, qa_note: null });
  }
  for (const [i, f] of r.flags.filter(x => x.gate === 'hold').entries()) {
    holds.push({ hold_id: `${ROUND}:${r.id}:flag${i + 1}`, round: ROUND, dry_run: DRY, church_id: r.id, church_name: r.name, page: r.page, kind: 'flag',
      field: null, flag: f.type, other_id: f.other_id || null, detail: f.detail || f.basis, action: f.action || null,
      evidence: f.evidence || null, qa_status: 'pending', qa_by: null, qa_note: null });
  }
}
const changedChurches = results.filter(r => r.changes.length);
const summary = {
  reviewed: results.filter(r => r.status === 'reviewed').length,
  identity_mismatch: results.filter(r => r.status === 'identity_mismatch').length,
  unreachable: results.filter(r => r.status === 'unreachable').length,
  unreadable_js: results.filter(r => r.status === 'unreadable').length,
  churches_total: results.length,
  churches_with_changes: changedChurches.length,
  churches_with_auto_changes: results.filter(r => r.changes.some(c => c.gate === 'auto')).length,
  churches_with_holds: new Set(holds.map(h => h.church_id)).size,
  changes_total: results.reduce((a, r) => a + r.changes.length, 0),
  changes_auto: results.reduce((a, r) => a + r.changes.filter(c => c.gate === 'auto').length, 0),
  changes_held: holds.filter(h => h.kind === 'change').length,
  flags_held: holds.filter(h => h.kind === 'flag').length,
  rulings_held: holds.filter(h => h.kind === 'ruling').length,
  unconfirmed_held: holds.filter(h => h.kind === 'unconfirmed').length,
  ratings_proposed: Object.fromEntries(['red', 'black', 'green', 'yellow'].map(l => [l, results.filter(r => (r.changes || []).some(c => c.field === 'overall_rating' && c.new === l)).length])),
  pastor_changes: results.reduce((a, r) => a + r.changes.filter(c => c.field === 'pastor').length, 0),
  overall_changes: results.reduce((a, r) => a + r.changes.filter(c => c.field === 'overall_rating').length, 0),
};
const roundDir = path.join(OUT, 'rounds', ROUND);
fs.mkdirSync(roundDir, { recursive: true });
const SHA_AFTER = sha256(CHURCHES);
const patch = {
  round: ROUND, generated_at: new Date().toISOString(), dry_run: DRY, applied: false,
  model: obsFile.model || null, llm_base: obsFile.llm_base || null, searches_used: obsFile.searches_used ?? null,
  churches_json_sha256: SHA_BEFORE, churches_json_sha256_after_build: SHA_AFTER,
  gates: {
    evidence: 'every change carries evidence.quote + evidence.url; anything without both was dropped',
    ratings: 'a category score or overall rating is proposed only when a rule published on docs/directory-methodology.html maps the evidence to that level; the rule text is cited (change.rule) next to the page quote (change.evidence). Anything beyond the rules is a needs-ruling HOLD item.',
    on_topic: 'a category score needs a quote that addresses that category; otherwise the score stays null',
    gender: 'female clergy only from page evidence (pronouns, spouse, explicit role); a first-name match alone is an unconfirmed HOLD item',
    hold: 'to RED/BLACK, off GREEN, medium/low confidence, unconfirmed identity, wrong-church data, duplicates, needs-ruling, unconfirmed',
    auto: 'high confidence only: verbatim quote on the church\'s own identity-confirmed site; fills of empty fields; pastor set/replace with explicit lead role',
  },
  summary, churches: results,
};
fs.writeFileSync(path.join(roundDir, 'review-patch.json'), JSON.stringify(patch, null, 1));
fs.writeFileSync(path.join(roundDir, 'hold.json'), JSON.stringify({ round: ROUND, dry_run: DRY, holds }, null, 1));
fs.copyFileSync(INPUT, path.join(roundDir, 'observations.json'));

// cumulative HOLD queue (sidecar). Re-running a round replaces its own rows.
const QP = path.join(OUT, 'hold-queue.json');
let q = { note: 'Full-review HOLD queue. Chaps QA sets qa_status to approved|rejected (+ qa_by, qa_note). apply-full-review-patch.js applies approved rows only. Rows with dry_run=true came from a dry run and are never applied.', holds: [] };
try { q = JSON.parse(fs.readFileSync(QP, 'utf8')); } catch (_) { }
q.holds = (q.holds || []).filter(h => h.round !== ROUND).concat(holds);
q.updated = new Date().toISOString();
fs.writeFileSync(QP, JSON.stringify(q, null, 1));

// dashboard series
let s = { series: [] };
try { s = JSON.parse(fs.readFileSync(STATS, 'utf8')); } catch (_) { }
s.series = (s.series || []).filter(r => r.round !== ROUND);
s.series.push({ round: ROUND, ts: new Date().toISOString().slice(0, 16), dry_run: DRY, reviewed: summary.churches_total - summary.unreachable - summary.unreadable_js,
  reachable_reviewed: summary.reviewed, identity_mismatch: summary.identity_mismatch, unreachable: summary.unreachable, unreadable_js: summary.unreadable_js,
  changed: summary.churches_with_changes, changes_total: summary.changes_total, auto: summary.changes_auto,
  held: summary.changes_held + summary.flags_held + summary.rulings_held + summary.unconfirmed_held, needs_ruling: summary.rulings_held, unconfirmed: summary.unconfirmed_held, held_churches: summary.churches_with_holds, applied: 0, applied_holds: 0 });
s.pending_holds = q.holds.filter(h => h.qa_status === 'pending' && !h.dry_run).length;
s.updated = new Date().toISOString();
fs.writeFileSync(STATS, JSON.stringify(s, null, 1));

console.log(`full-review patch ${ROUND}${DRY ? ' (DRY RUN)' : ''}: ${JSON.stringify(summary)}`);
console.log(`  patch: ${path.join(roundDir, 'review-patch.json')}`);
console.log(`  holds: ${path.join(roundDir, 'hold.json')} (${holds.length}) + ${QP}`);
console.log(`  churches.json sha256 ${SHA_BEFORE} -> ${SHA_AFTER} ${SHA_BEFORE === SHA_AFTER ? '(unchanged)' : '(CHANGED — investigate!)'}`);
if (SHA_BEFORE !== SHA_AFTER) process.exit(4);
