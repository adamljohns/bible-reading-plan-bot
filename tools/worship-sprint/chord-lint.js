#!/usr/bin/env node
// Chord/lyric accuracy lint over the whole songbook. Run from the worktree root.
// Flags per song: garbled chord lines (lines that look chord-ish but carry
// invalid tokens), encoding junk (replacement chars, double-escaped entities),
// and thin bodies. Writes tools/worship-sprint/reports/chord-lint.json and
// prints a summary. Read-only — fixing is the VERIFY lane's job.
const fs = require('fs');
const path = require('path');
const songs = JSON.parse(fs.readFileSync('docs/data/worship-songs.json', 'utf8'));

// Adam's charts use decades of authentic shorthand — treat it all as valid:
// Eno3, C STEP annotations, E15, D6/9, F#15/E, trailing *, (add4), arrows
// between chords (E <---> G), x2 / 2x / (x2) repeats. Only flag what NO
// notation system explains.
const CHORD = /^[\(\[]?([A-G][#b]?)((?:maj|min|m|sus|aug|dim|add|no|M)?\d{0,2}(?:[#b]?\d{1,2})?(?:sus|add|maj|min|dim|aug|no)?\d{0,2}(?:\/\d{1,2})?)\*?(\/[A-G][#b]?)?\*?[\)\],]?$/;
const NOISE_TOKEN = /^(x\d+|\d+x|\(x?\d+x?\)|\||%|N\.?C\.?|\([^)]*\)|\/+|-+|\.+|<?-{1,}>?|<-+>|STEP|riff|Riff|RIFF|intro|Intro|chorus|Chorus|verse|Verse|bridge|Bridge|end|End|hold|Hold|mute|Mute|palm|let|ring)$/i;

function lintSong(s) {
  const issues = { garbledChordLines: 0, encodingJunk: 0, thin: false, samples: [] };
  const body = s.body || '';
  if (/�/.test(body)) issues.encodingJunk += (body.match(/�/g) || []).length;
  if (/&(amp|lt|gt|quot|#\d+);/.test(body)) issues.encodingJunk += (body.match(/&(amp|lt|gt|quot|#\d+);/g) || []).length;
  const lines = body.split('\n');
  // A token is chord-valid if, after stripping parenthesized suffixes, every
  // hyphen-joined part is a chord or noise (covers F6*-F*-F6*, D2(add4)(2x)).
  const tokOk = (t) => {
    const bare = t.replace(/\([^)]*\)/g, '');
    if (!bare) return true;
    return bare.split('-').filter(Boolean).every((p) => CHORD.test(p) || NOISE_TOKEN.test(p));
  };
  for (const raw of lines) {
    // Bracketed chord runs inside lyric lines ([Em D A D]) are intentional style.
    const line = raw.replace(/\[[^\]]*\]/g, '');
    const toks = line.trim().split(/\s+/).filter(Boolean);
    if (toks.length < 2 || toks.length > 24) continue;
    const chordish = toks.filter((t) => tokOk(t) && !NOISE_TOKEN.test(t)).length;
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
