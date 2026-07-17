#!/usr/bin/env node
/*
 * Assemble worship-directory additions + removals into the generator's data files.
 *   node scripts/assemble-worship-additions.js <songbook.json> <hymns.json> [removals.json]
 *
 * - songbook.json : array of ready chart song-objects (real chords).
 * - hymns.json    : array of {title,author,year,key,lyrics,source} PD hymns -> lyrics-only songs.
 * - removals.json : optional array of slugs to purge (verified non-worship).
 *
 * Merges new songs into docs/data/worship-extra-songs.json (dedup by slug vs the
 * live directory AND the existing extras), and writes purge slugs to
 * docs/data/worship-purged.json (read by the generator's PURGED set).
 */
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '..');
const DATA = path.join(REPO, 'docs/data');
const slugify = (s) => s.toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const [songbookF, hymnsF, removalsF] = process.argv.slice(2);
const live = new Set(JSON.parse(fs.readFileSync(path.join(DATA, 'worship-songs.json'), 'utf8')).map((s) => s.slug));
const extraPath = path.join(DATA, 'worship-extra-songs.json');
const extras = fs.existsSync(extraPath) ? JSON.parse(fs.readFileSync(extraPath, 'utf8')) : [];
const have = new Set([...live, ...extras.map((s) => s.slug)]);

let added = 0;
function tryAdd(obj) {
  if (!obj.slug || have.has(obj.slug)) return false;
  have.add(obj.slug);
  extras.push(obj);
  added++;
  return true;
}

// 1) Songbook chart songs (already in final schema).
let sb = 0;
if (songbookF && fs.existsSync(songbookF)) {
  for (const s of JSON.parse(fs.readFileSync(songbookF, 'utf8'))) if (tryAdd(s)) sb++;
}

// 2) PD hymns -> lyrics-only song objects.
let hy = 0;
const CH = /(christmas|noel|manger|bethlehem|emmanuel|nativity|come all ye faithful|silent night|first noel|angels we have)/i;
if (hymnsF && fs.existsSync(hymnsF)) {
  for (const h of JSON.parse(fs.readFileSync(hymnsF, 'utf8'))) {
    const title = (h.title || '').replace(/\s+/g, ' ').trim();
    if (!title) continue;
    const slug = slugify(title);
    const letter = (title.match(/[A-Za-z]/) || ['#'])[0].toUpperCase();
    const yr = (h.year || '').toString().replace(/[^0-9c.\-–]/gi, '').slice(0, 12);
    const cop = h.author ? ('Public domain' + (yr ? ' · ' + yr : '') + (h.author ? ' · ' + h.author : '')) : 'Public domain';
    if (tryAdd({
      slug, title, type: 'praise', christmas: CH.test(title),
      key: (h.key || '').slice(0, 4), author: (h.author || '').slice(0, 70),
      letter: /[A-Z]/.test(letter) ? letter : '#', ext: 'hymn',
      src: 'hymn/' + (h.source || 'public-domain'),
      body: (h.lyrics || '').replace(/\r/g, '').replace(/\n{3,}/g, '\n\n').trim(),
      writer: (h.author || '').slice(0, 70), ccli: '', copyright: cop,
      youtube: null, slides: null, lyricsOnly: true, publicDomain: true,
    })) hy++;
  }
}

extras.sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase()));
fs.writeFileSync(extraPath, JSON.stringify(extras, null, 1));

// 3) Removals -> worship-purged.json
let removals = [];
if (removalsF && fs.existsSync(removalsF)) {
  removals = JSON.parse(fs.readFileSync(removalsF, 'utf8')).filter(Boolean);
  const purgedPath = path.join(DATA, 'worship-purged.json');
  const prev = fs.existsSync(purgedPath) ? JSON.parse(fs.readFileSync(purgedPath, 'utf8')) : [];
  const merged = [...new Set([...prev, ...removals])];
  fs.writeFileSync(purgedPath, JSON.stringify(merged, null, 1));
}

console.log(`Added ${added} songs to extras (songbook: ${sb}, hymns: ${hy}). Extras now ${extras.length}.`);
console.log(`Removals staged: ${removals.length}.`);
console.log(`Extras total: ${extras.length}  ->  projected directory: ${live.size + added} (minus removals in live set).`);
