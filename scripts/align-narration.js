#!/usr/bin/env node
/* align-narration.js — find the real spoken time of each beat marker.
 *
 * Beat lengths used to be derived from each section's share of the narrated
 * WORDS, which silently assumes a uniform speaking rate. It is not uniform:
 * the voice pauses at paragraph breaks and slows at punctuation, so the picture
 * drifts ahead of the voice and the cuts land early. This reads the actual
 * audio instead.
 *
 *   ffmpeg -i narration.mp3 -ar 16000 -ac 1 -c:a pcm_s16le narration.wav
 *   whisper-cli -m ggml-large-v3.bin -f narration.wav -oj -ml 1 -of words
 *   node scripts/align-narration.js words.json markers.json > cuts.json
 *
 * markers.json is a plain array of marker phrases, in order. Output is an array
 * of start seconds, one per marker. Exits non-zero if any marker cannot be
 * located — a silently missing cut is worse than a failed build.
 */
'use strict';
const fs = require('fs');

const norm = s => s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();

function main() {
  const [wordsFile, markersFile] = process.argv.slice(2);
  if (!wordsFile || !markersFile) {
    console.error('usage: align-narration.js <whisper-words.json> <markers.json>');
    process.exit(2);
  }
  const tr = JSON.parse(fs.readFileSync(wordsFile, 'utf8')).transcription || [];
  const words = tr
    .map(s => ({ t: s.offsets.from / 1000, w: norm(s.text) }))
    .filter(x => x.w);

  /* Match on the character stream with spaces removed, not on word tokens.
     Whisper's tokenisation does not have to agree with the script's — it split
     "Navigators" into "navig" + "ators", which defeats any word-by-word
     comparison. Concatenating sidesteps the question entirely. */
  let stream = '';
  const startOfChar = [];             // char index -> index into `words`
  words.forEach((x, i) => {
    const bare = x.w.replace(/ /g, '');
    for (let c = 0; c < bare.length; c++) startOfChar.push(i);
    stream += bare;
  });

  const markers = JSON.parse(fs.readFileSync(markersFile, 'utf8'));
  const cuts = [];
  let fromChar = 0;                   // markers are in order; never search backwards

  for (const marker of markers) {
    if (marker === null) { cuts.push(0); continue; }
    const need = norm(marker).replace(/ /g, '');
    let at = stream.indexOf(need, fromChar);
    /* One mis-heard word should not kill the build: retry on the leading
       portion, but never below 12 characters or it can match noise. */
    for (let n = need.length - 4; at === -1 && n >= 12; n -= 4) {
      at = stream.indexOf(need.slice(0, n), fromChar);
    }
    if (at === -1) {
      console.error(`marker not found in audio: "${marker}"`);
      process.exit(1);
    }
    cuts.push(+words[startOfChar[at]].t.toFixed(3));
    fromChar = at + 1;
  }
  process.stdout.write(JSON.stringify(cuts));
}

main();
