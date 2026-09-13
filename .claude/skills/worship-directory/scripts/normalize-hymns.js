#!/usr/bin/env node
// Normalize agent-sourced hymns in place and report how many are FRESH against the
// live directory + extras, comparing accent-folded titles (not raw slugs — the
// generator slugifies "gwêl" as "gw-l" while other sessions transliterate to "gwel").
//   node normalize-hymns.js <hymns.json>
const fs = require('fs');
const f = process.argv[2];
const deaccent = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ø/gi, 'o').replace(/æ/gi, 'ae').replace(/ß/g, 'ss');
const fold = (t) => deaccent(String(t || '')).toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
const live = JSON.parse(fs.readFileSync('docs/data/worship-songs.json', 'utf8'));
const extras = JSON.parse(fs.readFileSync('docs/data/worship-extra-songs.json', 'utf8'));
const have = new Set([...live, ...extras].map((s) => fold(s.title)));
const hymns = JSON.parse(fs.readFileSync(f, 'utf8'));
const seen = new Set(); const out = [];
let dupLive = 0, dupInRound = 0;
for (const x of hymns) {
  if (x.key) x.key = String(x.key).replace(/♭/g, 'b').replace(/♯/g, '#').replace(/[-\s]?flat/i, 'b').replace(/[-\s]?sharp/i, '#').replace(/\s*minor/i, 'm').replace(/\s*major/i, '').replace(/\s*\([^)]*\)/, '').trim().slice(0, 4);
  if (x.key && !/^[A-G][#b]?m?$/.test(x.key)) x.key = '';   // "/", "C.M.", "unknown" are not keys
  let a = String(x.author || '');
  if (/Joint Committee on Versification|Anonymous versifier, The Psalter/i.test(a)) a = 'The Psalter (1912)';
  x.author = a.replace(/\s*\(\d{4}[-–]\d{0,4}\)/g, '').replace(/\s+/g, ' ').trim();
  if (x.source) {                       // agents stuff prose provenance in here; keep the first URL, else the first token
    const src = String(x.source); const u = src.match(/https?:\/\/[^\s;,]+/);
    x.source = (u ? u[0] : src.split(/[\s;(]/)[0]).slice(0, 120);
  }
  // Agents append catalog refs to titles — "(HLS No. 80)", "(Hymn 412)", "(No. 7)". Strip them;
  // keep "(Psalm N)" which is how psalter titles are written.
  x.title = String(x.title || '')
    .replace(/\s*\([^)]*\b(?:No\.?|Hymn|#)\s*\d+[a-z]?[^)]*\)\s*$/i, '')   // "(HLS No. 80)", "(Hymns on the Lord's Supper, 1745, No. 80)"
    .replace(/\s*\[[^\]]*\]\s*$/, '')                                        // "[Hymn 412]"
    .replace(/\s+/g, ' ').trim();
  const k = fold(x.title);
  if (!k) continue;
  if (have.has(k)) { dupLive++; continue; }
  if (seen.has(k)) { dupInRound++; continue; }
  seen.add(k); out.push(x);
}
fs.writeFileSync(f, JSON.stringify(out, null, 1));
console.log(`normalized ${hymns.length} -> fresh ${out.length} (already in directory: ${dupLive}, dup within round: ${dupInRound})`);
