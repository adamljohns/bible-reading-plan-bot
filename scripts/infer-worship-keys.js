#!/usr/bin/env node
/* infer-worship-keys.js — fill the `key` field for chord-chart worship songs
 * by reading the chart itself.
 *
 * 94 of 2,258 songs ship with an empty key. They split two ways: charts that
 * carry real chords in `body` (recoverable) and lyrics-only entries where no
 * key exists to find (correctly left blank forever).
 *
 * The inference is deliberately conservative. Songs overwhelmingly begin and
 * end on their tonic, so when the first and last chord of a chart agree, that
 * chord is the key. When they disagree the chart may be modulating, may end on
 * a IV/V turnaround, or may just be transcribed loosely — and a wrong key on a
 * worship chart is worse than a blank one, because a musician will trust it and
 * count off in the wrong place. So disagreement yields nothing.
 *
 * Gates, all of which must pass before a key is written:
 *   - the banner comment block is stripped (it is boilerplate, not content)
 *   - at least MIN_CHORD_LINES chord lines, so a stray capo note cannot decide
 *   - first chord === last chord (bare triad compared, so G and G7 agree)
 *   - the candidate is the most common root, or tied for it
 *
 * usage:
 *   node scripts/infer-worship-keys.js            # report only, writes nothing
 *   node scripts/infer-worship-keys.js --apply    # write docs/data/worship-songs.json
 */
'use strict';

const fs = require('fs');
const path = require('path');

const DB = path.join(__dirname, '..', 'docs', 'data', 'worship-songs.json');
const APPLY = process.argv.includes('--apply');
const MIN_CHORD_LINES = 3;

/* A chord token: root, optional accidental, optional quality, optional bass.
   Anchored, because a lyric word like "Am" only counts when the WHOLE line is
   chords — see chordLine() below. */
const CHORD = /^[A-G](?:#|b)?(?:maj|min|m|dim|aug|sus|add|M)?[0-9]*(?:sus|add|dim|aug)?[0-9]*(?:\/[A-G](?:#|b)?)?$/;

/* Strip the boilerplate banner and any other full-line comments. */
const stripBanner = body =>
  body.split('\n').filter(l => !l.trimStart().startsWith('#'));

/* The archive carries two chart dialects and a song may only use one:
     over-lyric   a bare chord line sitting above the words it belongs to
     inline       chords bracketed at the end of the lyric  "...now [D A7 G D]"
   Both are read, in document order, into one chord stream. Reading only the
   first dialect is what made an early version of this script report every one
   of the 94 as lyrics-only. */
function chordLine(line) {
  const toks = line.trim().split(/\s+/).filter(Boolean);
  if (!toks.length) return null;
  return toks.every(t => CHORD.test(t)) ? toks : null;
}

/* Bracketed runs, e.g. "[D A7 G D]". A bracket group counts only when every
   token inside it is a chord, so an annotation like [Chorus] or [x2] is
   ignored rather than mistaken for a root. */
function inlineChords(line) {
  const out = [];
  for (const m of line.matchAll(/\[([^\]]+)\]/g)) {
    const toks = m[1].trim().split(/\s+/).filter(Boolean);
    if (toks.length && toks.every(t => CHORD.test(t))) out.push(...toks);
  }
  return out;
}

/* Compare tonics, not full chords: a chart may open on G and close on G7, and
   those are the same key. Accidental is part of the root; quality is not. */
const root = ch => (ch.match(/^[A-G](?:#|b)?/) || [''])[0];

function inferKey(body) {
  if (!body) return { key: null, why: 'no body' };
  const lines = stripBanner(body);

  const chordLines = [];
  for (const l of lines) {
    const inline = inlineChords(l);
    if (inline.length) { chordLines.push(inline); continue; }
    const toks = chordLine(l);
    if (toks) chordLines.push(toks);
  }
  if (chordLines.length < MIN_CHORD_LINES) {
    return { key: null, why: `only ${chordLines.length} chord line(s)` };
  }

  const flat = chordLines.flat();
  const first = flat[0];
  const last = flat[flat.length - 1];
  if (root(first) !== root(last)) {
    return { key: null, why: `opens ${first}, closes ${last}` };
  }

  /* Guard against a chart that merely happens to be bookended: the tonic
     should also be the (or a) most-used root across the whole chart. */
  const counts = {};
  for (const c of flat) counts[root(c)] = (counts[root(c)] || 0) + 1;
  const top = Math.max(...Object.values(counts));
  if (counts[root(first)] < top) {
    const winner = Object.keys(counts).find(k => counts[k] === top);
    return { key: null, why: `bookended ${root(first)} but ${winner} dominates` };
  }

  /* Keep the opening chord's quality — "Em" is a more useful key than "E". */
  return { key: first, why: `${chordLines.length} chord lines, opens+closes ${first}` };
}

function main() {
  const raw = JSON.parse(fs.readFileSync(DB, 'utf8'));
  const songs = Array.isArray(raw) ? raw : raw.songs;
  if (!Array.isArray(songs)) throw new Error('unexpected worship-songs.json shape');

  const keyless = songs.filter(s => s && !(s.key || '').trim());
  const filled = [];
  const skipped = [];

  for (const s of keyless) {
    const { key, why } = inferKey(s.body);
    if (key) {
      filled.push({ slug: s.slug, title: s.title, key, why });
      if (APPLY) s.key = key;
    } else {
      skipped.push({ slug: s.slug, title: s.title, why });
    }
  }

  console.log(`keyless songs: ${keyless.length}`);
  console.log(`  inferable:   ${filled.length}`);
  console.log(`  left blank:  ${skipped.length}\n`);

  for (const f of filled.slice(0, 15)) {
    console.log(`  ${f.key.padEnd(6)} ${f.title.slice(0, 44).padEnd(46)} ${f.why}`);
  }
  if (filled.length > 15) console.log(`  … and ${filled.length - 15} more`);

  const reasons = {};
  for (const s of skipped) {
    const bucket = /^opens /.test(s.why) ? 'opens/closes disagree'
      : /chord line/.test(s.why) ? 'too few chord lines (lyrics-only)'
      : /dominates/.test(s.why) ? 'tonic not dominant'
      : s.why;
    reasons[bucket] = (reasons[bucket] || 0) + 1;
  }
  console.log('\nleft blank, by reason:');
  for (const [r, n] of Object.entries(reasons).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${String(n).padStart(3)}  ${r}`);
  }

  if (APPLY) {
    fs.writeFileSync(DB, JSON.stringify(raw, null, 2) + '\n');
    console.log(`\napplied ${filled.length} keys -> ${path.relative(process.cwd(), DB)}`);
  } else {
    console.log('\nreport only — pass --apply to write');
  }
}

main();
