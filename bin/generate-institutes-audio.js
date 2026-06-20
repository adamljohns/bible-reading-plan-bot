#!/usr/bin/env node
/* generate-institutes-audio.js — narrate Institutes chapters with Piper (Alan voice).
 *
 * Reads a chapter JSON, prefers the modernized text (sectionsModern) over Beveridge,
 * and renders: a short intro, each numbered section (with a real pause between
 * sections), and the "A Word for 2026" commentary — to one MP3 per chapter.
 *
 * Pipeline: piper (en_GB-alan) per segment -> WAV, concatenated with a silence gap
 * via ffmpeg, -> MP3 (libmp3lame). Output: docs/assets/institutes/audio/b{B}-c{CC}.mp3
 *
 * Prereqs (not in repo): a piper venv + the Alan voice model.
 *   PIPER_PY    (default /tmp/piper-venv/bin/python)   — python with piper-tts
 *   PIPER_MODEL (default ~/.piper-voices/alan.onnx)
 *
 * Run: node bin/generate-institutes-audio.js b1c01 [b1c02 ...]   (ids; default = all)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DATA = path.join(ROOT, 'docs', 'assets', 'institutes');
const OUT = path.join(ROOT, 'docs', 'assets', 'institutes', 'audio');
const PY = process.env.PIPER_PY || '/tmp/piper-venv/bin/python';
const MODEL = process.env.PIPER_MODEL || path.join(os.homedir(), '.piper-voices', 'alan.onnx');
const REPO = 'adamljohns/bible-reading-plan-bot';
const RELEASE_TAG = 'institutes-audio';
const MANIFEST = path.join(DATA, 'audio-manifest.json');
const LENGTH_SCALE = '1.12';      // slightly slower, more deliberate
const SENTENCE_SILENCE = '0.4';   // pause between sentences
const SECTION_GAP = 0.9;          // seconds of silence between sections
const pad = (n) => String(n).padStart(2, '0');

function checkPrereqs() {
  if (!fs.existsSync(MODEL)) throw new Error('Voice model missing: ' + MODEL);
  try { execFileSync(PY, ['-m', 'piper', '--help'], { stdio: 'ignore' }); }
  catch (e) { throw new Error('piper not runnable via ' + PY + ' — set PIPER_PY'); }
  try { execSync('command -v ffmpeg', { stdio: 'ignore' }); }
  catch (e) { throw new Error('ffmpeg not found'); }
}

function synth(text, wavPath) {
  execFileSync(PY, ['-m', 'piper', '-m', MODEL,
    '--length-scale', LENGTH_SCALE, '--sentence-silence', SENTENCE_SILENCE,
    '-f', wavPath], { input: text });
}

function silenceWav(p) {
  execSync('ffmpeg -y -loglevel error -f lavfi -i anullsrc=r=22050:cl=mono -t ' + SECTION_GAP + ' "' + p + '"');
}

function chapterAudio(ch) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'instaudio-'));
  const segs = [];
  const romanBook = ['', 'I', 'II', 'III', 'IV'][ch.book];
  // segments: intro, each section, then the commentary
  const src = (ch.modernized && ch.sectionsModern) ? ch.sectionsModern : ch.sections;
  segs.push('Calvin’s Institutes of the Christian Religion. Book ' + ch.book + ', Chapter ' + ch.chapter + '. ' + ch.title + '.');
  src.forEach((s) => segs.push('Section ' + s.n + '. ' + s.paragraphs.join(' ')));
  if (ch.application) segs.push('A word for 2026, from U.S.M.C. Ministries. ' + ch.application);

  // synth each segment, build a concat list interleaving silence
  const sil = path.join(tmp, 'sil.wav');
  silenceWav(sil);
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
  const outMp3 = path.join(OUT, 'b' + ch.book + '-c' + pad(ch.chapter) + '.mp3');
  execSync('ffmpeg -y -loglevel error -f concat -safe 0 -i "' + listFile + '" -codec:a libmp3lame -q:a 4 "' + outMp3 + '"');
  // cleanup temp
  try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) {}
  const dur = parseFloat(execSync('ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "' + outMp3 + '"').toString().trim());
  return { file: path.basename(outMp3), seconds: Math.round(dur), kb: Math.round(fs.statSync(outMp3).size / 1024), modernized: !!(ch.modernized && ch.sectionsModern) };
}

function uploadAndRecord(book, chapter, mp3Path) {
  execSync('gh release upload ' + RELEASE_TAG + ' "' + mp3Path + '" --repo ' + REPO + ' --clobber', { stdio: 'ignore' });
  let m;
  try { m = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); }
  catch (e) { m = { voice: 'en_GB-alan', release: 'https://github.com/' + REPO + '/releases/download/' + RELEASE_TAG, chapters: {} }; }
  m.chapters['b' + book + 'c' + pad(chapter)] = path.basename(mp3Path);
  fs.writeFileSync(MANIFEST, JSON.stringify(m, null, 2) + '\n');
}

function main() {
  checkPrereqs();
  let ids = process.argv.slice(2);
  if (!ids.length) {
    ids = fs.readdirSync(DATA).filter((f) => /^b\dc\d\d\.json$/.test(f)).map((f) => f.replace('.json', '')).sort();
  }
  ids.forEach((id) => {
    const f = path.join(DATA, id + '.json');
    if (!fs.existsSync(f)) { console.log('skip (no json):', id); return; }
    const ch = JSON.parse(fs.readFileSync(f, 'utf8'));
    const r = chapterAudio(ch);
    if (!process.env.SKIP_UPLOAD) uploadAndRecord(ch.book, ch.chapter, path.join(OUT, r.file));
    console.log(id + ' -> ' + r.file + '  ' + Math.floor(r.seconds / 60) + ':' + pad(r.seconds % 60) +
      ', ' + r.kb + ' KB' + (r.modernized ? '  [modernized text]' : '  [Beveridge text]') +
      (process.env.SKIP_UPLOAD ? '' : '  [uploaded]'));
  });
}
main();
