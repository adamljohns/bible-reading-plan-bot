#!/usr/bin/env node
/*
 * Build docs/data/worship-extra-songs.json from projection-slide PDFs that have
 * no chord chart in the archive — worship standards we want in the directory as
 * lyrics-only pages (chords can be added later via overrides). Re-runnable.
 *
 *   node scripts/build-worship-extras.js
 *
 * The generator merges this file in at ingest (see EXTRA_JSON), so the songs
 * survive a re-ingest just like overrides do.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const REPO = path.resolve(__dirname, '..');
const SONGS_JSON = path.join(REPO, 'docs/data/worship-songs.json');
const SLIDES_DIR = path.join(REPO, 'docs/worship/slides');
const OUT = path.join(REPO, 'docs/data/worship-extra-songs.json');

const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Existing slugs (so we never duplicate a song already in the directory).
const existing = new Set(JSON.parse(fs.readFileSync(SONGS_JSON, 'utf8')).map((s) => s.slug));

// Title cleanups + confident credits for the well-known standards. Only writer
// and key where I'm confident — no unverified CCLI numbers.
const META = {
  'how-great-is-our-god': { writer: 'Chris Tomlin, Jesse Reeves & Ed Cash', key: 'C' },
  'mighty-to-save': { writer: 'Ben Fielding & Reuben Morgan', key: 'A' },
  'open-the-eyes-of-my-heart': { writer: 'Paul Baloche', key: 'E' },
  'the-heart-of-worship': { writer: 'Matt Redman' },
  'heart-of-worship': { writer: 'Matt Redman' },
  'in-christ-alone': { writer: 'Keith Getty & Stuart Townend', key: 'D' },
  'in-christ-alone-medley': { writer: 'Keith Getty & Stuart Townend', key: 'D' },
  'be-thou-my-vision': { writer: 'Traditional Irish hymn; tr. Mary E. Byrne' },
  'blessed-assurance': { writer: 'Fanny J. Crosby & Phoebe P. Knapp' },
  'come-thou-fount': { writer: 'Robert Robinson & John Wyeth' },
  'come-thou-fount-come-thou-king': { writer: 'Robert Robinson; add. Thankyou Music' },
  'god-of-wonders': { writer: 'Marc Byrd & Steve Hindalong' },
  'indescribable': { writer: 'Laura Story & Jesse Reeves' },
  'agnus-dei': { writer: 'Michael W. Smith' },
  'famous-one': { writer: 'Chris Tomlin & Jesse Reeves' },
  'beautiful-one': { writer: 'Tim Hughes' },
  'everyday': { writer: 'Joel Houston' },
  'hungry': { writer: 'Kathryn Scott' },
  'here-is-our-king': { writer: 'David Crowder' },
  'let-it-rise': { writer: 'Holland Davis' },
  'lord-reign-in-me': { writer: 'Brenton Brown' },
  'once-again': { writer: 'Matt Redman' },
  'you-said': { writer: 'Reuben Morgan' },
  'this-is-my-desire': { writer: 'Reuben Morgan' },
  'let-my-words-be-few': { writer: 'Matt & Beth Redman' },
  'never-let-go': { writer: 'Matt Redman' },
  'you-never-let-go': { writer: 'Matt Redman' },
  'praise-adonai': { writer: 'Paul Baloche' },
  'one-pure-and-holy-passion': { writer: 'Mark Altrogge' },
  'offering': { writer: 'Paul Baloche' },
};
// Title corrections keyed by raw deck name (minus .pdf).
const TITLE_FIX = {
  'Angles We Have Heard On High': 'Angels We Have Heard on High',
  'Oh, Come Emmanuel': 'O Come, O Come Emmanuel',
  'Offering w-Xmas vs': 'Offering',
  'We are Hungry-We fall Down': 'We Are Hungry / We Fall Down',
  'How Great is Our God': 'How Great Is Our God',
  'Let it Rise': 'Let It Rise',
  'I will Not Forget You': 'I Will Not Forget You',
  'I will Walk By Faith': 'I Will Walk by Faith',
  'May the Words of My Mouth': 'May the Words of My Mouth',
};
const CHRISTMAS = /angels we have heard|emmanuel|noel|christmas|nativity/i;

function extractLyrics(pdf, title) {
  let raw;
  try { raw = execFileSync('pdftotext', ['-layout', pdf, '-'], { encoding: 'utf8' }); }
  catch { return ''; }
  const tnorm = title.toLowerCase().replace(/[^a-z0-9]/g, '');
  const out = [];
  let lastBlank = false;
  for (let line of raw.split('\n')) {
    line = line.replace(/\s+$/,'').replace(/^\s{1,}/, (m) => m.length > 6 ? '' : m); // de-indent slide centering
    const t = line.trim();
    if (!t) { if (!lastBlank && out.length) { out.push(''); lastBlank = true; } continue; }
    lastBlank = false;
    if (t.replace(/[^a-z0-9]/gi, '').toLowerCase() === tnorm) continue; // slide title header
    if (/^[\d\s.\-–—]+$/.test(t)) continue;                            // slide numbers / rules
    out.push(t);
  }
  // collapse 3+ blank runs, trim ends
  let body = out.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  return body;
}

const slides = fs.readdirSync(SLIDES_DIR).filter((f) => f.toLowerCase().endsWith('.pdf'));
const extras = [];
const seen = new Set();
let skippedExisting = 0, skippedEmpty = 0;

for (const file of slides.sort()) {
  const base = file.replace(/\.pdf$/i, '');
  const title = (TITLE_FIX[base] || base).replace(/\s+/g, ' ').trim();
  const slug = slugify(title);
  // Only add genuinely-new songs: skip if already a chart OR loosely matches one.
  if (existing.has(slug) || seen.has(slug)) { skippedExisting++; continue; }
  if ([...existing].some((p) => p === slug || p === slug + '-tab')) { skippedExisting++; continue; }
  // loose: slide slug is contained in / contains an existing slug → treat as dupe
  if ([...existing].some((p) => p.includes(slug) || slug.includes(p))) { skippedExisting++; continue; }

  const body = extractLyrics(path.join(SLIDES_DIR, file), title);
  if (!body || body.length < 20) { skippedEmpty++; continue; }

  const meta = META[slug] || {};
  const letter = (title.match(/[A-Za-z]/) || ['#'])[0].toUpperCase();
  extras.push({
    slug, title,
    type: 'praise',
    christmas: CHRISTMAS.test(title),
    key: meta.key || '',
    author: meta.writer || '',
    letter: /[A-Z]/.test(letter) ? letter : '#',
    ext: 'lyrics',
    src: 'slides/' + file,
    body,
    writer: meta.writer || '',
    ccli: '',
    copyright: '',
    youtube: null,
    slides: file,
    lyricsOnly: true,
  });
  seen.add(slug);
}

extras.sort((a, b) => a.title.toLowerCase().localeCompare(b.title.toLowerCase()));
fs.writeFileSync(OUT, JSON.stringify(extras, null, 1));
console.log(`Wrote ${extras.length} extra songs -> ${path.relative(REPO, OUT)}`);
console.log(`  (skipped ${skippedExisting} already-present, ${skippedEmpty} empty/short)`);
console.log('Titles:\n  ' + extras.map((e) => e.title + (e.writer ? '  — ' + e.writer : '')).join('\n  '));
