#!/usr/bin/env node
// Pick exactly N best-quality NEW hymns (not already in the directory) from a
// round's hymns.json. Run from the worktree root. Writes the surplus (unpicked
// fresh hymns) to <out>.surplus.json so they can be banked durably.
//   node trim-to-gap.js <hymns.json> <N> <out.json>
const fs = require('fs');
const [inp, nStr, out] = process.argv.slice(2);
const N = parseInt(nStr, 10);
const slugify = (s) => s.toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const live = new Set(JSON.parse(fs.readFileSync('docs/data/worship-songs.json', 'utf8')).map((s) => s.slug));
const extras = new Set(JSON.parse(fs.readFileSync('docs/data/worship-extra-songs.json', 'utf8')).map((s) => s.slug));

const hymns = JSON.parse(fs.readFileSync(inp, 'utf8'));
const seen = new Set();
const fresh = [];
for (const h of hymns) {
  const slug = slugify(h.title || '');
  if (!slug || live.has(slug) || extras.has(slug) || seen.has(slug)) continue;
  seen.add(slug);
  fresh.push(h);
}
const score = (h) => {
  let p = 0;
  const verses = (h.lyrics || '').split(/\n\s*\n/).filter((v) => v.trim().length > 40).length;
  p += Math.min(verses, 5) * 10;
  if (h.key) p += 8;
  if (/\d{4}/.test(h.year || '')) p += 6;
  if ((h.author || '').length > 3) p += 6;
  if (/hymnary|hymnal\.net|cyberhymnal|hymntime|timelesstruths|wikisource|ccel|westminsterstandard/i.test(h.source || '')) p += 10;
  p += Math.min((h.lyrics || '').length, 2000) / 200;
  return p;
};
fresh.sort((a, b) => score(b) - score(a));
const pick = fresh.slice(0, N);
const surplus = fresh.slice(N);
fs.writeFileSync(out, JSON.stringify(pick, null, 1));
fs.writeFileSync(out.replace(/\.json$/, '') + '.surplus.json', JSON.stringify(surplus, null, 1));
console.log(`fresh: ${fresh.length} | picked ${pick.length}/${N} | surplus banked: ${surplus.length}`);
