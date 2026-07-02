#!/usr/bin/env node
/* generate-catechism-audio.js — narrate the Baptist Catechism with Piper (Mr. Pemberton).
 *
 * One MP3 per editorial section (15 of them). Each section: intro ("Section N.
 * <title>") + every Q&A in its range ("Question N. <q> Answer: <a>"). Uploads to
 * Cloudflare R2 under catechism/ (audio.usmcmin.org/catechism/...) and records in
 * docs/assets/catechism/audio-manifest.json.
 *
 * Same new-wave settings as the LBCF batch: length-scale 1.0, 64 kbps mono.
 *
 * Run: node bin/generate-catechism-audio.js [sectionIndex ...]  (1-based; default all)
 *      SKIP_UPLOAD=1 to render locally without pushing to R2.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'docs', 'assets', 'catechism');
const OUT = path.join(DATA, 'audio');
const SRC = path.join(DATA, 'catechism.json');
const PY = process.env.PIPER_PY || require('os').homedir() + '/.piper-venv/bin/python';
const MODEL = process.env.PIPER_MODEL || path.join(os.homedir(), '.piper-voices', 'alan.onnx');
const R2_REMOTE = process.env.R2_REMOTE || 'r2:usmcmin-audio';
const R2_PREFIX = 'catechism';
const R2_BASE = 'https://audio.usmcmin.org';
const MANIFEST = path.join(DATA, 'audio-manifest.json');
const LENGTH_SCALE = '1.0';
const SENTENCE_SILENCE = '0.35';
const SECTION_GAP = 0.7;
const pad = (n) => String(n).padStart(2, '0');

function checkPrereqs() {
  if (!fs.existsSync(MODEL)) throw new Error('Voice model missing: ' + MODEL);
  try { execFileSync(PY, ['-m', 'piper', '--help'], { stdio: 'ignore' }); }
  catch (e) { throw new Error('piper not runnable via ' + PY + ' — set PIPER_PY'); }
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

function sectionAudio(sec, idx, byNum) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'cataudio-'));
  const segs = [];
  segs.push('Section ' + (idx + 1) + '. ' + sec.title + '.');
  for (let n = sec.start; n <= sec.end; n++) {
    const q = byNum.get(n);
    if (!q) continue;
    segs.push('Question ' + q.number + '. ' + q.question + ' Answer: ' + q.answer);
  }
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
  const outMp3 = path.join(OUT, 'section-' + pad(idx + 1) + '.mp3');
  execSync('ffmpeg -y -loglevel error -f concat -safe 0 -i "' + listFile + '" -codec:a libmp3lame -b:a 64k -ac 1 "' + outMp3 + '"');
  try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
  const dur = parseFloat(execSync('ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "' + outMp3 + '"').toString().trim());
  return { file: outMp3, key: R2_PREFIX + '/section-' + pad(idx + 1) + '.mp3', seconds: Math.round(dur), kb: Math.round(fs.statSync(outMp3).size / 1024) };
}

function record(idx, key) {
  let m;
  try { m = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); }
  catch (e) { m = { voice: 'en_GB-alan', label: 'Mr. Pemberton', base: R2_BASE, sections: {} }; }
  if (!m.base) m.base = R2_BASE;
  if (!m.sections) m.sections = {};
  m.sections['section-' + pad(idx + 1)] = key;
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2) + '\n');
}

function main() {
  checkPrereqs();
  const data = JSON.parse(fs.readFileSync(SRC, 'utf8'));
  const byNum = new Map(data.questions.map((q) => [q.number, q]));
  const sections = data.sections || [];
  let idxs = process.argv.slice(2).filter((a) => /^\d+$/.test(a)).map((n) => Number(n) - 1);
  if (!idxs.length) idxs = sections.map((_, i) => i);
  idxs.forEach((i) => {
    const sec = sections[i];
    if (!sec) { console.log('skip (no section): index', i + 1); return; }
    const r = sectionAudio(sec, i, byNum);
    if (!process.env.SKIP_UPLOAD) { execSync('rclone copy "' + r.file + '" ' + R2_REMOTE + '/' + R2_PREFIX + '/', { stdio: 'ignore' }); record(i, r.key); }
    console.log('section ' + (i + 1) + ' (' + sec.title + ') -> ' + r.key + '  ' + Math.floor(r.seconds / 60) + ':' + pad(r.seconds % 60) +
      ', ' + r.kb + ' KB' + (process.env.SKIP_UPLOAD ? '  [local only]' : '  [R2]'));
  });
}
main();
