#!/usr/bin/env node
/* lexicon-diagnose-misfiled.js — find lexicon pages filed under the WRONG
 * Strong's code.
 *
 * The 2026-09-03 audit called ~2,100 lexicon pages "fabricated". They are
 * mostly not. They are real scholarship filed under a neighbouring number:
 * docs/lexicon/G14.html carries the word for G15 (agathopoieo), G1177 cites
 * G1427's verses, G1018 holds G1017's content. Scattered near-misses, ~33%
 * within +/-3 of the filed code — the signature of a generator whose word list
 * drifted out of sync with its code list.
 *
 * That matters because re-filing a page is far cheaper than rewriting it.
 *
 * Method: for each page, take its cited verses, read which Strong's codes the
 * tagged KJV actually puts in them, and see whether one RARE code dominates.
 * Rarity is essential — G2532 (kai, "and") appears in 5,237 of 31,112 verses
 * and will "win" on any page. Codes present in >0.5% of verses are treated as
 * function words and ignored.
 *
 * Writes bin/baselines/lexicon-misfiled.json. Read-only; proposes, never edits.
 *   node bin/lexicon-diagnose-misfiled.js
 */
'use strict';
const fs = require('fs'), path = require('path');
const { BOOK_IDS } = require('./verse-study-scaffold.js');
const ROOT = path.resolve(__dirname, '..');
const LEX = path.join(ROOT, 'docs/lexicon'), CH = path.join(ROOT, 'docs/assets/chapters');
const DF = (()=>{const j=JSON.parse(fs.readFileSync(path.join(__dirname,'baselines','strongs-doc-freq.json'),'utf8'));
  return {verses:j.verses, df:new Map(j.df)};})();
// A code in a large share of all verses is a function word (G2532 kai "and",
// G1161 de "but", H3068 the divine name). It dominates any verse list and tells
// us nothing about the page's subject. Only rare codes identify content.
const COMMON = c => (DF.df.get(c)||0) > DF.verses * 0.005;
const chCache = new Map();
function chapter(b, c) { const k = b + '_' + c;
  if (!chCache.has(k)) { const fp = path.join(CH, k + '.json');
    chCache.set(k, fs.existsSync(fp) ? JSON.parse(fs.readFileSync(fp,'utf8')) : null); }
  return chCache.get(k); }
const strip = s => s.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g,'');
const text = s => s.replace(/<[^>]+>/g,' ').replace(/&[a-z#0-9]+;/g,' ').replace(/\s+/g,' ').trim();
function codesFor(ref, prefix) {
  const m = String(ref).match(/^([1-3]?\s*[A-Za-z ]+?)\s+(\d+):(\d+)/); if (!m) return null;
  let b = m[1].trim(), id = BOOK_IDS[b.toLowerCase()];
  while (!id && b.includes(' ')) { b = b.slice(b.indexOf(' ')+1).trim(); id = BOOK_IDS[b.toLowerCase()]; }
  if (!id) return null;
  if (prefix === 'G' && id <= 39) return null;
  if (prefix === 'H' && id > 39) return null;
  const d = chapter(id, +m[2]); if (!d || !d.KJV) return null;
  const v = d.KJV[String(+m[3])]; if (!v) return null;
  return [...v.matchAll(/<S>(\d+)<\/S>/g)].map(x => x[1]);
}
const rows = [];
for (const fn of fs.readdirSync(LEX).filter(f=>/^[GH]\d+\.html$/.test(f)).sort()) {
  const cm = fn.match(/^([GH])(\d+)\.html$/); const prefix = cm[1], num = cm[2];
  const body = strip(fs.readFileSync(path.join(LEX,fn),'utf8'));
  const refs = [...new Set((text(body).match(/\b(?:[1-3]\s*)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s+\d+:\d+/g)||[]))];
  const tally = new Map(); let usable = 0;
  for (const r of refs) { const cs = codesFor(r, prefix); if (!cs) continue; usable++;
    for (const c of new Set(cs)) tally.set(c, (tally.get(c)||0)+1); }
  if (usable < 2) continue;
  const own = tally.get(num) || 0;
  const ranked = [...tally.entries()].filter(([c])=>!COMMON(c)).sort((a,b)=>b[1]-a[1]);
  if (!ranked.length) continue;
  const [topCode, topN] = ranked[0];
  if (own === 0 && topCode !== num && topN >= Math.max(2, Math.ceil(usable*0.6))) {
    rows.push({ page:`docs/lexicon/${fn}`, filedAs:prefix+num, actual:prefix+topCode,
                hits:topN, usable, exists: fs.existsSync(path.join(LEX, prefix+topCode+'.html')) });
  }
}
fs.writeFileSync(path.join(ROOT,'bin','baselines','lexicon-misfiled.json'), JSON.stringify(rows,null,1));
console.log(`pages with a confident single-code diagnosis: ${rows.length}`);
console.log(`  target page already exists:  ${rows.filter(r=>r.exists).length}`);
console.log(`  target page does NOT exist:  ${rows.filter(r=>!r.exists).length}`);
console.log('samples:'); rows.slice(0,6).forEach(r=>console.log(`  ${r.filedAs} -> ${r.actual}  (${r.hits}/${r.usable} cited verses, target exists=${r.exists})`));
