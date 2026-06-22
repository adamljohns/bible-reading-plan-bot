#!/usr/bin/env node
/* generate-mbt-audio.js — narrate MBT Bible chapters with Piper (female voice).
 *
 * Pilot scope: Ruth (book 8) + Esther (book 17). One MP3 per chapter. Each chapter
 * reads "<Book>, chapter <N>." then every verse in order, drawn from the MBT text in
 * docs/assets/moop-translation.json (keys are "<bookId>_<chapter>_<verse>").
 *
 * Output:  docs/assets/bible/audio/<bookId>-<chapter>.mp3   (local, git-ignored)
 * Upload:  Cloudflare R2 under bible/  ->  https://audio.usmcmin.org/bible/<bookId>-<chapter>.mp3
 *
 * The BTE reader (docs/bible.html) probes each R2 URL and shows a chapter-page player
 * once the file is live — nothing else to wire after you upload.
 *
 * VOICE — this is the FEMALE counterpart to Mr. Pemberton (en_GB-alan). Default is
 * en_US-amy-medium; swap via PIPER_MODEL. Other good female Piper voices:
 *   en_GB-jenny_dioco-medium, en_GB-southern_english_female-low, en_US-libritts_r-medium,
 *   en_US-hfc_female-medium, en_US-kristin-medium.
 * Download one with:  python3 -m piper.download_voices en_US-amy-medium
 *
 * Run:
 *   node bin/generate-mbt-audio.js                 # all pilot chapters (Ruth + Esther)
 *   node bin/generate-mbt-audio.js 8               # just Ruth (all chapters)
 *   node bin/generate-mbt-audio.js 8:1 17:3        # specific book:chapter targets
 *   SKIP_UPLOAD=1 node bin/generate-mbt-audio.js   # render locally, don't push to R2
 *
 * Mirrors generate-catechism-audio.js: length-scale 1.0, 64 kbps mono, ffmpeg concat.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'docs', 'assets', 'moop-translation.json');
const OUT = path.join(ROOT, 'docs', 'assets', 'bible', 'audio');
const MANIFEST = path.join(ROOT, 'docs', 'assets', 'bible', 'audio-manifest.json');
const PY = process.env.PIPER_PY || '/tmp/piper-venv/bin/python';
const MODEL = process.env.PIPER_MODEL || path.join(os.homedir(), '.piper-voices', 'amy.onnx');
const R2_REMOTE = process.env.R2_REMOTE || 'r2:usmcmin-audio';
const R2_PREFIX = 'bible';
const R2_BASE = 'https://audio.usmcmin.org';
const LENGTH_SCALE = '1.0';
const SENTENCE_SILENCE = '0.35';
const VERSE_GAP = 0.35;        // brief pause between verses

// Pilot books. Chapter counts are derived from the source, not trusted from here.
const BOOK_NAMES = { '8': 'Ruth', '17': 'Esther' };

function checkPrereqs() {
  if (!fs.existsSync(MODEL)) throw new Error('Voice model missing: ' + MODEL + ' (set PIPER_MODEL or download a female voice)');
  try { execFileSync(PY, ['-m', 'piper', '--help'], { stdio: 'ignore' }); }
  catch (e) { throw new Error('piper not runnable via ' + PY + ' — set PIPER_PY'); }
  try { execSync('command -v ffmpeg', { stdio: 'ignore' }); } catch (e) { throw new Error('ffmpeg not found'); }
  if (!process.env.SKIP_UPLOAD) {
    try { execSync('rclone ls ' + R2_REMOTE + ' >/dev/null 2>&1', { stdio: 'ignore' }); }
    catch (e) { throw new Error('rclone remote ' + R2_REMOTE + ' not reachable (or run SKIP_UPLOAD=1)'); }
  }
}

// Build { bookId: { chapter: [ [verseNum, text], ... ] } } for the pilot books.
function indexSource() {
  const data = JSON.parse(fs.readFileSync(SRC, 'utf8'));
  const idx = {};
  for (const key of Object.keys(data)) {
    const m = key.match(/^(\d+)_(\d+)_(\d+)$/);
    if (!m) continue;
    const [, b, c, v] = m;
    if (!BOOK_NAMES[b]) continue;
    (idx[b] = idx[b] || {});
    (idx[b][c] = idx[b][c] || []).push([Number(v), data[key]]);
  }
  for (const b of Object.keys(idx))
    for (const c of Object.keys(idx[b]))
      idx[b][c].sort((a, z) => a[0] - z[0]);
  return idx;
}

function synth(text, wavPath) {
  execFileSync(PY, ['-m', 'piper', '-m', MODEL,
    '--length-scale', LENGTH_SCALE, '--sentence-silence', SENTENCE_SILENCE, '-f', wavPath], { input: text });
}

function chapterAudio(bookId, chapter, verses) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mbtaudio-'));
  const segs = [BOOK_NAMES[bookId] + ', chapter ' + chapter + '.'];
  verses.forEach(([, text]) => segs.push(String(text)));

  const sil = path.join(tmp, 'sil.wav');
  execSync('ffmpeg -y -loglevel error -f lavfi -i anullsrc=r=22050:cl=mono -t ' + VERSE_GAP + ' "' + sil + '"');
  const listLines = [];
  segs.forEach((text, i) => {
    const w = path.join(tmp, 'seg' + i + '.wav');
    synth(text, w);
    if (i > 0) listLines.push("file '" + sil + "'");
    listLines.push("file '" + w + "'");
  });
  const listFile = path.join(tmp, 'list.txt');
  fs.writeFileSync(listFile, listLines.join('\n'));

  fs.mkdirSync(OUT, { recursive: true });
  const outMp3 = path.join(OUT, bookId + '-' + chapter + '.mp3');
  execSync('ffmpeg -y -loglevel error -f concat -safe 0 -i "' + listFile + '" -codec:a libmp3lame -b:a 64k -ac 1 "' + outMp3 + '"');
  try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
  const dur = parseFloat(execSync('ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "' + outMp3 + '"').toString().trim());
  return { file: outMp3, key: R2_PREFIX + '/' + bookId + '-' + chapter + '.mp3', seconds: Math.round(dur), kb: Math.round(fs.statSync(outMp3).size / 1024) };
}

// Keep the manifest's book/chapter coverage honest with what actually exists in the source.
function syncManifest(idx) {
  let m;
  try { m = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); }
  catch (e) { m = { voice: 'en_US-amy-medium', label: 'MBT narration', base: R2_BASE, prefix: R2_PREFIX, books: {} }; }
  m.base = m.base || R2_BASE; m.prefix = m.prefix || R2_PREFIX; m.books = m.books || {};
  for (const b of Object.keys(idx)) {
    const maxCh = Math.max.apply(null, Object.keys(idx[b]).map(Number));
    m.books[b] = { name: BOOK_NAMES[b], chapters: maxCh };
  }
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2) + '\n');
}

function pad2(n) { return String(n).padStart(2, '0'); }

function main() {
  checkPrereqs();
  const idx = indexSource();
  syncManifest(idx);

  // Parse targets: bare bookId (all chapters) or book:chapter.
  const args = process.argv.slice(2);
  let targets = [];
  for (const a of args) {
    const bc = a.match(/^(\d+):(\d+)$/);
    if (bc) { targets.push([bc[1], Number(bc[2])]); continue; }
    if (/^\d+$/.test(a) && idx[a]) { Object.keys(idx[a]).map(Number).sort((x, y) => x - y).forEach((c) => targets.push([a, c])); }
  }
  if (!targets.length) {
    for (const b of Object.keys(idx))
      Object.keys(idx[b]).map(Number).sort((x, y) => x - y).forEach((c) => targets.push([b, c]));
  }

  targets.forEach(([b, c]) => {
    const verses = idx[b] && idx[b][String(c)];
    if (!verses) { console.log('skip (no source): ' + (BOOK_NAMES[b] || b) + ' ' + c); return; }
    const r = chapterAudio(b, c, verses);
    if (!process.env.SKIP_UPLOAD) execSync('rclone copy "' + r.file + '" ' + R2_REMOTE + '/' + R2_PREFIX + '/', { stdio: 'ignore' });
    console.log(BOOK_NAMES[b] + ' ' + c + ' -> ' + r.key + '  ' +
      Math.floor(r.seconds / 60) + ':' + pad2(r.seconds % 60) + ', ' + r.kb + ' KB' +
      (process.env.SKIP_UPLOAD ? '  [local only]' : '  [R2]'));
  });
}
main();
