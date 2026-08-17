#!/usr/bin/env node
// Emit the next batch of songs that still need a curated YouTube video, in
// priority order, as JSON an agent can research. Run from the repo root.
//   node video-worklist.js [count=40] [out.json]
//
// Priority: the pages that are thinnest without a video come first.
//   1. linksOnly contemporary/CCM pages — copyright means no lyrics, so the
//      recording IS the page's value.
//   2. Songs with projection slides (Adam actually uses these in services).
//   3. Lyrics-only hymns, then everything else, well-known first.
const fs = require('fs');
const path = require('path');
const REPO = process.cwd();
const songs = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/data/worship-songs.json'), 'utf8'));
const OV_PATH = path.join(REPO, 'docs/data/worship-overrides.json');
const ov = fs.existsSync(OV_PATH) ? JSON.parse(fs.readFileSync(OV_PATH, 'utf8')) : {};

const count = parseInt(process.argv[2] || '40', 10);
const out = process.argv[3] || '.claude/skills/worship-directory/reports/video-worklist.json';

const needs = songs.filter((s) => !s.youtube && !(ov[s.slug] && ov[s.slug].youtube));
const tier = (s) => {
  if (s.linksOnly) return 0;
  if (s.slides) return 1;
  if (s.lyricsOnly) return 2;
  return 3;
};
needs.sort((a, b) => tier(a) - tier(b) || (b.key ? 1 : 0) - (a.key ? 1 : 0) || a.title.localeCompare(b.title));

const batch = needs.slice(0, count).map((s) => ({
  slug: s.slug,
  title: s.title,
  artist: s.artist || s.writer || s.author || '',
  year: (s.copyright || '').match(/\d{4}/) ? (s.copyright.match(/\d{4}/) || [])[0] : '',
  kind: s.linksOnly ? 'contemporary' : s.publicDomain ? 'public-domain hymn' : 'chart',
}));
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify(batch, null, 1));
console.log(`${needs.length} songs still need video | wrote ${batch.length} to ${out}`);
console.log(`  tiers remaining: contemporary ${needs.filter((s) => tier(s) === 0).length}, `
  + `slides ${needs.filter((s) => tier(s) === 1).length}, hymns ${needs.filter((s) => tier(s) === 2).length}, `
  + `charts ${needs.filter((s) => tier(s) === 3).length}`);
