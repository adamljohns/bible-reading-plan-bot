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
const CHORD = /^[\(\[]?([A-G][#b]?)((?:maj|min|m|sus|aug|dim|add|no|M)?[+]?\d{0,2}(?:[#b+]?\d{1,2})?(?:sus|add|maj|min|dim|aug|no)?\d{0,2}(?:\/\d{1,2})?)\*?(\/[A-G][#b]?(?:m|maj|min|sus|add|M)?\d{0,2})?\*?[\)\],]?$/;
// Bass-run notation ("/C#  /B  /A"), fret diagrams ("320033", "X02010"),
// and section labels with or without a colon.
const BASS_ONLY = /^\/[A-G][#b]?$/;
const FRET = /^[xX0-9]{4,6}$/;
const LABEL = /^(chords?|intro|outro|chorus|verse|bridge|tag|coda|solo|instrumental|interlude|pre-?chorus|refrain|ending|repeat|capo|key|riff|vamp|turnaround)\d*:?$/i;
const NOISE_TOKEN = new RegExp(
  '^(x\\d+|\\d+x|\\(x?\\d+x?\\)|\\||%|N\\.?C\\.?|\\([^)]*\\)|\\/+|-+|\\.+|<?-{1,}>?|<-+>|STEP|hold|mute|palm|let|ring|end|'
  + '\\/[A-G][#b]?|[xX0-9]{4,6}|'
  + '(chords?|intro|outro|chorus|verse|bridge|tag|coda|solo|instrumental|interlude|pre-?chorus|refrain|ending|repeat|capo|key|riff|vamp|turnaround)\\d*:?)$', 'i');

function lintSong(s) {
  const issues = { garbledChordLines: 0, encodingJunk: 0, thin: false, samples: [] };
  const body = s.body || '';
  if (/�/.test(body)) issues.encodingJunk += (body.match(/�/g) || []).length;
  if (/&(amp|lt|gt|quot|#\d+);/.test(body)) issues.encodingJunk += (body.match(/&(amp|lt|gt|quot|#\d+);/g) || []).length;
  const lines = body.split('\n');
  // A token is chord-valid if, after stripping parenthesized suffixes, every
  // hyphen-joined part is a chord or noise (covers F6*-F*-F6*, D2(add4)(2x)).
  const tokOk = (t) => {
    // Strip an attached fret diagram: G-(320033) -> G
    const bare = t.replace(/-?\([^)]*\)/g, '');
    if (!bare) return true;
    return bare.split('-').filter(Boolean)
      .every((p) => CHORD.test(p) || NOISE_TOKEN.test(p) || BASS_ONLY.test(p) || FRET.test(p) || LABEL.test(p));
  };
  // A chart's own shorthand repeats; corruption doesn't. Tokens used 3+ times in
  // one song (Adam's "Gs" for Gsus, a tabber's "Emag7") are that chart's
  // convention — count them as valid rather than flagging every line they touch.
  const freq = new Map();
  for (const l of lines) for (const t of l.trim().split(/\s+/).filter(Boolean)) freq.set(t, (freq.get(t) || 0) + 1);
  // Chord suffixes are lowercase or symbolic (Gs, Emag7, D2sus) — an all-caps
  // repeated word like GOD or GLORY is a lyric, not a chord, so require the
  // shape to actually look like a chord before honoring it as convention.
  // The suffix must be real chord shorthand (m, sus, maj, s, mag…) and/or
  // digits and symbols — otherwise "God", "For" and "Crown" read as chords.
  const CONV = /^[A-G][#b]?(?:m|M|s|sus|maj|min|add|dim|aug|no|mag)?[0-9#b+\/()*.-]*$/;
  const convention = (t) => (freq.get(t) || 0) >= 3 && t.length <= 8 && CONV.test(t);

  for (const raw of lines) {
    // Bracketed chord runs inside lyric lines ([Em D A D]) are intentional style.
    const line = raw.replace(/\[[^\]]*\]/g, '');
    const toks = line.trim().split(/\s+/).filter(Boolean);
    if (toks.length < 2 || toks.length > 24) continue;
    const chordish = toks.filter((t) => (tokOk(t) || convention(t)) && !NOISE_TOKEN.test(t)).length;
    const noise = toks.filter((t) => NOISE_TOKEN.test(t)).length;
    const ratio = chordish / toks.length;
    // Lines that are mostly-but-not-all chords are the classic garble signature.
    if (ratio >= 0.4 && ratio < 0.9 && chordish + noise < toks.length && chordish >= 2) {
      issues.garbledChordLines++;
      if (issues.samples.length < 2) issues.samples.push(line.trim().slice(0, 80));
    }
  }
  // "Thin" means TRUNCATED, not short. Adam's archive is full of legitimate
  // one-page praise choruses ("I Just Came to Praise the Lord") that are
  // complete at 200 characters. A real chorus still has several lyric lines
  // under its chord lines; a truncated chart has almost none.
  if (!s.linksOnly) {
    const lyricLines = lines.filter((l) => {
      const t = l.trim();
      if (t.length < 3) return false;
      const toks = t.split(/\s+/).filter(Boolean);
      return !toks.every((x) => tokOk(x));
    }).length;
    if (lyricLines < 3) issues.thin = true;
  }
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
