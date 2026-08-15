#!/usr/bin/env node
// Chord/lyric accuracy lint over the whole songbook. Run from the worktree root.
// Flags per song: garbled chord lines (lines that look chord-ish but carry
// invalid tokens), encoding junk (replacement chars, double-escaped entities),
// and thin bodies. Writes tools/worship-sprint/reports/chord-lint.json and
// prints a summary. Read-only — fixing is the VERIFY lane's job.
const fs = require('fs');
const path = require('path');
const songs = JSON.parse(fs.readFileSync('docs/data/worship-songs.json', 'utf8'));

const CHORD = /^[\(\[]?([A-G][#b]?)((?:maj|min|m|sus|aug|dim|add|M)?\d{0,2}(?:[#b]?\d{1,2})?(?:sus|add|maj|min|dim|aug)?\d{0,2})(\/[A-G][#b]?)?[\)\],]?$/;
const NOISE_TOKEN = /^(x\d+|\d+x|\||%|N\.?C\.?|\(.*\)|\/+|-+|\.+)$/i;

function lintSong(s) {
  const issues = { garbledChordLines: 0, encodingJunk: 0, thin: false, samples: [] };
  const body = s.body || '';
  if (/�/.test(body)) issues.encodingJunk += (body.match(/�/g) || []).length;
  if (/&(amp|lt|gt|quot|#\d+);/.test(body)) issues.encodingJunk += (body.match(/&(amp|lt|gt|quot|#\d+);/g) || []).length;
  const lines = body.split('\n');
  for (const line of lines) {
    const toks = line.trim().split(/\s+/).filter(Boolean);
    if (toks.length < 2 || toks.length > 24) continue;
    const chordish = toks.filter((t) => CHORD.test(t)).length;
    const noise = toks.filter((t) => NOISE_TOKEN.test(t)).length;
    const ratio = chordish / toks.length;
    // Lines that are mostly-but-not-all chords are the classic garble signature.
    if (ratio >= 0.4 && ratio < 0.9 && chordish + noise < toks.length && chordish >= 2) {
      issues.garbledChordLines++;
      if (issues.samples.length < 2) issues.samples.push(line.trim().slice(0, 80));
    }
  }
  if (!s.linksOnly && body.replace(/\s/g, '').length < 120) issues.thin = true;
  return issues;
}

const report = [];
for (const s of songs) {
  const r = lintSong(s);
  if (r.garbledChordLines >= 3 || r.encodingJunk > 0 || r.thin) {
    report.push({ slug: s.slug, ext: s.ext || 'crd', lyricsOnly: !!s.lyricsOnly, ...r });
  }
}
report.sort((a, b) => (b.garbledChordLines + b.encodingJunk * 2) - (a.garbledChordLines + a.encodingJunk * 2));
const outDir = path.join('tools/worship-sprint/reports');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'chord-lint.json'), JSON.stringify(report, null, 1));
const enc = report.filter((r) => r.encodingJunk).length;
const garb = report.filter((r) => r.garbledChordLines >= 3).length;
const thin = report.filter((r) => r.thin).length;
console.log(`linted ${songs.length} songs -> ${report.length} flagged (${garb} garbled-chords, ${enc} encoding-junk, ${thin} thin) -> ${outDir}/chord-lint.json`);
