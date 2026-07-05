#!/usr/bin/env node
/* generate-verse-pages.js — server-render (SSG) the 22 curated verse landing pages.
 *
 * Problem: docs/verse/*.html render their Scripture client-side into #results, so
 * a non-JS client (search crawler, RAG scraper, agent fetch) sees only
 * "Loading Proverbs 27:17…". That directly undercuts the Layer-B moat: the whole
 * point is agent-fetchable, hyperlinkable, addressable Scripture.
 *
 * Fix: bake the actual verse text into the static HTML in two PUBLIC-DOMAIN
 * translations (KJV primary — uses "LORD", matches house style; WEB secondary,
 * with WEB's "Yahweh" normalized to "the LORD"). Copyright-safe by construction,
 * which is exactly what we want crawled and quoted. The page's existing JS still
 * runs lookupVerse() on load and replaces #results with the full interactive
 * multi-translation study — so JS users are unaffected and non-JS clients finally
 * get real content. Also rebuilds the description meta tags to lead with the verse.
 *
 * Idempotent: re-run any time. Source of verse text: docs/assets/chapters/<id>_<ch>.json.
 * Run: node bin/generate-verse-pages.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const VERSE_DIR = path.join(ROOT, 'docs', 'verse');
const CH_DIR = path.join(ROOT, 'docs', 'assets', 'chapters');

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

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escAttr = (s) => esc(s).replace(/"/g, '&quot;');
// The local chapter store keeps some translations (e.g. KJV) with Strong's numbers
// fused to each word — "loved25 the world2889". Those aren't tags, so strip the
// digit-run that immediately follows a letter/apostrophe. KJV spells its numerals
// out ("threescore"), so no legitimate number is lost.
const stripStrongs = (s) => String(s).replace(/([A-Za-z’'])\d+/g, '$1');
const cleanText = (s) => stripStrongs(String(s).replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ')).replace(/\s+/g, ' ').trim();
// WEB renders the divine name "Yahweh"; Adam's house style (and the MBT) use "the LORD".
// WEB is public domain, so normalizing is a free editorial choice for on-brand display.
const normalizeDivineNames = (s) => s
  .replace(/\bYahweh of Armies\b/g, 'the LORD of Hosts')
  .replace(/\bYahweh\b/g, 'the LORD');

function parseRef(ref) {
  const m = ref.match(/^(.+?)\s+(\d+):(\d+)(?:[-–](\d+))?$/);
  if (!m) return null;
  const bookId = BOOK_IDS[m[1].trim().toLowerCase()];
  if (!bookId) return null;
  return { book: m[1].trim(), bookId, ch: m[2], v1: parseInt(m[3], 10), v2: m[4] ? parseInt(m[4], 10) : parseInt(m[3], 10) };
}

function versesFor(bookId, ch, v1, v2, trans) {
  const p = path.join(CH_DIR, `${bookId}_${ch}.json`);
  if (!fs.existsSync(p)) return null;
  let data;
  try { data = JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return null; }
  const t = data[trans];
  if (!t) return null;
  const out = [];
  for (let v = v1; v <= v2; v++) {
    if (t[String(v)]) out.push({ v, text: cleanText(t[String(v)]) });
  }
  return out.length ? out : null;
}

const S = {
  wrap: 'margin:0 auto;max-width:640px;text-align:left;',
  ref: 'font-family:Georgia,serif;color:#D4AF37;font-size:1.05rem;font-weight:600;margin-bottom:10px;letter-spacing:0.3px;',
  bq: 'margin:0 0 14px;padding:10px 16px;border-left:3px solid #D4AF37;background:rgba(212,175,55,0.06);border-radius:0 8px 8px 0;font-size:1.08rem;line-height:1.75;color:#eae3d0;',
  cite: 'display:block;margin-top:6px;font-size:0.78rem;font-style:normal;color:#9a8f6f;letter-spacing:0.4px;',
  sup: 'color:#D4AF37;font-weight:700;font-size:0.72em;margin-right:2px;',
  load: 'margin:6px 0 0;font-size:0.85rem;color:#8a8a8a;font-style:italic;',
};

function renderVerses(arr, range) {
  return arr.map((x) => (range ? `<sup style="${S.sup}">${x.v}</sup>` : '') + esc(x.text)).join(' ');
}

function buildSsrBlock(ref, p) {
  const kjv = versesFor(p.bookId, p.ch, p.v1, p.v2, 'KJV');
  let web = versesFor(p.bookId, p.ch, p.v1, p.v2, 'WEB');
  if (web) web = web.map((x) => ({ v: x.v, text: normalizeDivineNames(x.text) }));
  if (!kjv && !web) return null;
  const range = p.v2 > p.v1;
  let html = '<!-- SSR-VERSE: baked public-domain Scripture for no-JS clients / crawlers / agents.\n';
  html += '     JS enhances via lookupVerse() on load, replacing #results with the full study. -->\n';
  html += `        <div class="ssr-verse" style="${S.wrap}">\n`;
  html += `          <div class="ssr-ref" style="${S.ref}">${esc(ref)}</div>\n`;
  if (web) html += `          <blockquote style="${S.bq}">${renderVerses(web, range)}<cite style="${S.cite}">— World English Bible (public domain)</cite></blockquote>\n`;
  if (kjv) html += `          <blockquote style="${S.bq}">${renderVerses(kjv, range)}<cite style="${S.cite}">— King James Version (public domain)</cite></blockquote>\n`;
  html += `          <p class="ssr-loading" style="${S.load}">Loading the full interlinear word study and 9-translation blend…</p>\n`;
  html += '        </div>\n        <!-- /SSR-VERSE -->';
  // Snippet for the meta description: prefer modern WEB, fall back to KJV.
  const snippetArr = web || kjv;
  let snippet = snippetArr.map((x) => x.text).join(' ');
  if (snippet.length > 155) snippet = snippet.slice(0, 155).replace(/\s+\S*$/, '') + '…';
  return { html, snippet };
}

function rebuildMeta(html, ref, snippet, isOT) {
  const tongue = isOT ? 'Hebrew' : 'Greek';
  const desc = `${ref} — “${snippet}” Interlinear ${tongue} word study with Strong's Concordance and a 9-translation blend at the MOOP Bible Translation Engine.`;
  const twDesc = `${ref}: “${snippet}” — interlinear word study + Strong's on usmcmin.org.`;
  const set = (h, attrKind, attrName, value) => {
    const re = new RegExp('(<meta ' + attrKind + '="' + attrName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '" content=")[^"]*(">)');
    return re.test(h) ? h.replace(re, '$1' + escAttr(value) + '$2') : h;
  };
  html = set(html, 'name', 'description', desc);
  html = set(html, 'property', 'og:description', desc);
  html = set(html, 'name', 'twitter:description', twDesc);
  return html;
}

function processFile(fp) {
  const fn = path.basename(fp);
  let html = fs.readFileSync(fp, 'utf8');
  const rm = html.match(/id="refInput"\s+value="([^"]+)"/);
  if (!rm) return { fn, status: 'no-ref' };
  const ref = rm[1].trim();
  const p = parseRef(ref);
  if (!p) return { fn, status: 'unparseable(' + ref + ')' };
  const block = buildSsrBlock(ref, p);
  if (!block) return { fn, status: 'no-verse-data(' + ref + ')' };

  // Idempotent inject: replace an existing SSR block, else the Loading stub inside #results.
  if (/<!-- SSR-VERSE:[\s\S]*?<!-- \/SSR-VERSE -->/.test(html)) {
    html = html.replace(/<!-- SSR-VERSE:[\s\S]*?<!-- \/SSR-VERSE -->/, () => block.html);
  } else {
    const loadingRe = /<div class="loading">[\s\S]*?Loading[\s\S]*?<\/div>/;
    if (!loadingRe.test(html)) return { fn, status: 'no-injection-point(' + ref + ')' };
    html = html.replace(loadingRe, () => block.html);
  }

  html = rebuildMeta(html, ref, block.snippet, p.bookId <= 39);
  fs.writeFileSync(fp, html);
  return { fn, status: 'ok(' + ref + ')' };
}

function main() {
  const files = fs.readdirSync(VERSE_DIR).filter((f) => f.endsWith('.html'));
  let ok = 0;
  const problems = [];
  files.forEach((f) => {
    const r = processFile(path.join(VERSE_DIR, f));
    if (r.status.startsWith('ok')) ok++;
    else problems.push(r.fn + ': ' + r.status);
  });
  console.log(`Verse-page SSG: ${ok}/${files.length} pages baked.`);
  if (problems.length) { console.log('  Problems:'); problems.forEach((p) => console.log('   - ' + p)); }
}

main();
