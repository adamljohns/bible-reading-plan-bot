#!/usr/bin/env node
/* generate-lbcf-audio.js — narrate 1689 LBCF chapters with Piper (Mr. Pemberton).
 *
 * Per chapter: intro ("Chapter N of the 1689 London Baptist Confession of Faith.
 * <title>. <subtitle>") + each paragraph's modernized text. Renders one MP3 per
 * chapter, uploads to Cloudflare R2 under lbcf/ (audio.usmcmin.org/lbcf/...), and
 * records it in docs/assets/lbcf/audio-manifest.json.
 *
 * New-wave audio settings (Adam, 2026-06-20): slightly faster than the first
 * Institutes batch (length-scale 1.0 vs 1.12) and mid-grade 64 kbps mono to save
 * R2 space — fidelity isn't needed for spoken narration.
 *
 * Prereqs (not in repo): piper venv + Alan voice model + rclone r2 remote.
 *   PIPER_PY    (default /tmp/piper-venv/bin/python)
 *   PIPER_MODEL (default ~/.piper-voices/alan.onnx)
 *   R2_REMOTE   (default r2:usmcmin-audio)
 *
 * Run: node bin/generate-lbcf-audio.js [N ...]   (chapter numbers; default = all)
 *      SKIP_UPLOAD=1 to render locally without pushing to R2.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'docs', 'assets', 'lbcf');
const OUT = path.join(DATA, 'audio');
const PY = process.env.PIPER_PY || '/tmp/piper-venv/bin/python';
const MODEL = process.env.PIPER_MODEL || path.join(os.homedir(), '.piper-voices', 'alan.onnx');
const R2_REMOTE = process.env.R2_REMOTE || 'r2:usmcmin-audio';
const R2_PREFIX = 'lbcf';
const R2_BASE = 'https://audio.usmcmin.org';
const MANIFEST = path.join(DATA, 'audio-manifest.json');
const LENGTH_SCALE = '1.0';       // a touch faster than the first Institutes batch (1.12)
const SENTENCE_SILENCE = '0.35';
const SECTION_GAP = 0.7;          // seconds of silence between segments
const pad = (n) => String(n).padStart(2, '0');

function checkPrereqs() {
  if (!fs.existsSync(MODEL)) throw new Error('Voice model missing: ' + MODEL);
  try { execFileSync(PY, ['-m', 'piper', '--help'], { stdio: 'ignore' }); }
  catch (e) { throw new Error('piper not runnable via ' + PY + ' — set PIPER_PY (recreate /tmp/piper-venv)'); }
  try { execSync('command -v ffmpeg', { stdio: 'ignore' }); } catch (e) { throw new Error('ffmpeg not found'); }
  if (!process.env.SKIP_UPLOAD) {
    try { execSync('rclone ls ' + R2_REMOTE + ' >/dev/null 2>&1', { stdio: 'ignore' }); }
    catch (e) { throw new Error('rclone remote ' + R2_REMOTE + ' not reachable (or run SKIP_UPLOAD=1)'); }
  }
}

function synth(text, wavPath) {
  execFileSync(PY, ['-m', 'piper', '-m', MODEL,
    '--length-scale', LENGTH_SCALE, '--sentence-silence', SENTENCE_SILENCE, '-f', wavPath], { input: text });
}

function chapterAudio(ch) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lbcfaudio-'));
  const segs = [];
  segs.push('Chapter ' + ch.number + ' of the 1689 London Baptist Confession of Faith. ' +
    ch.title + '.' + (ch.subtitle ? ' ' + ch.subtitle : ''));
  ch.paragraphs.forEach((p, i) => { if (p && p.text) segs.push('Paragraph ' + (i + 1) + '. ' + p.text); });

  const sil = path.join(tmp, 'sil.wav');
  execSync('ffmpeg -y -loglevel error -f lavfi -i anullsrc=r=22050:cl=mono -t ' + SECTION_GAP + ' "' + sil + '"');
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
  const outMp3 = path.join(OUT, 'chapter-' + pad(ch.number) + '.mp3');
  // 64 kbps mono — mid-grade, transparent for a single narration voice
  execSync('ffmpeg -y -loglevel error -f concat -safe 0 -i "' + listFile + '" -codec:a libmp3lame -b:a 64k -ac 1 "' + outMp3 + '"');
  try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
  const dur = parseFloat(execSync('ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "' + outMp3 + '"').toString().trim());
  return { file: outMp3, key: R2_PREFIX + '/chapter-' + pad(ch.number) + '.mp3', seconds: Math.round(dur), kb: Math.round(fs.statSync(outMp3).size / 1024) };
}

function record(chapter, key) {
  let m;
  try { m = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); }
  catch (e) { m = { voice: 'en_GB-alan', label: 'Mr. Pemberton', base: R2_BASE, chapters: {} }; }
  if (!m.base) m.base = R2_BASE;
  m.chapters['chapter-' + pad(chapter)] = key;
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2) + '\n');
}

function main() {
  checkPrereqs();
  let nums = process.argv.slice(2).filter((a) => /^\d+$/.test(a)).map(Number);
  if (!nums.length) nums = Array.from({ length: 32 }, (_, i) => i + 1);
  nums.forEach((n) => {
    const f = path.join(DATA, 'chapter-' + pad(n) + '.json');
    if (!fs.existsSync(f)) { console.log('skip (no json): chapter', n); return; }
    const ch = JSON.parse(fs.readFileSync(f, 'utf8'));
    const r = chapterAudio(ch);
    if (!process.env.SKIP_UPLOAD) { execSync('rclone copy "' + r.file + '" ' + R2_REMOTE + '/' + R2_PREFIX + '/', { stdio: 'ignore' }); record(n, r.key); }
    console.log('chapter ' + n + ' -> ' + r.key + '  ' + Math.floor(r.seconds / 60) + ':' + pad(r.seconds % 60) +
      ', ' + r.kb + ' KB' + (process.env.SKIP_UPLOAD ? '  [local only]' : '  [R2]'));
  });
}
main();
