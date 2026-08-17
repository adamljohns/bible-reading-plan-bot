#!/usr/bin/env node
// Build songbook-format linksOnly entries (credits + YouTube + SongSelect, NO
// lyrics) from a simple JSON list: [[title, artist, writers, year, key], ...].
// Optionally tags non-congregational slugs for worship-nonworship.json.
//   node build-linksonly.js <list.json> <out-songs.json> [out-nonworship-slugs.json] [comma,separated,worship,exception,slugs]
const fs = require('fs');
const [listF, outSongs, outSlugs, exceptions] = process.argv.slice(2);
// Transliterate accents so Spanish titles slug cleanly (cuan-grande-es-el).
const deaccent = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ø/gi, 'o').replace(/æ/gi, 'ae').replace(/ß/g, 'ss');
const slugify = (s) => deaccent(s).toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const EXCEPT = new Set((exceptions || '').split(',').filter(Boolean));

const NOTICE = 'This song is under copyright, so the full lyrics are not reproduced here.\n\n'
  + 'Worship along with the official recording using the YouTube button below, or find\n'
  + 'the complete chart and lyrics on CCLI SongSelect under your church’s license.';

const entries = JSON.parse(fs.readFileSync(listF, 'utf8')).map(([t, a, w, y, k]) => {
  const title = String(t).replace(/\s+/g, ' ').trim();
  const letter = (title.match(/[A-Za-z]/) || ['#'])[0].toUpperCase();
  return {
    slug: slugify(title), title, type: 'praise', christmas: false,
    key: k || '', author: a, artist: a, letter: /[A-Z]/.test(letter) ? letter : '#',
    ext: 'contemporary', src: 'linksonly/curated',
    body: NOTICE, writer: w, ccli: '',
    copyright: '© ' + y + ' · ' + w + ' — see CCLI SongSelect',
    youtube: null, slides: null, lyricsOnly: true, linksOnly: true,
    publicDomain: false,
  };
});
fs.writeFileSync(outSongs, JSON.stringify(entries, null, 1));
if (outSlugs) {
  fs.writeFileSync(outSlugs, JSON.stringify(entries.map((e) => e.slug).filter((s) => !EXCEPT.has(s)), null, 1));
}
console.log('built ' + entries.length + ' linksOnly entries');
