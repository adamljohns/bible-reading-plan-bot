#!/usr/bin/env node
/* build-pressure-check-video.js — the Pressure Check walkthrough.
 *
 * Every screen is the real page driven in a real browser, never a mockup.
 *
 * What makes it read as film rather than a deck: each beat gets a slow
 * push-in or pull-out (zoompan) and the beats crossfade into each other
 * (xfade). Hard cuts between static frames are what made the first attempt
 * feel like slides with a voice over them.
 *
 * Runtime per beat is that section's share of the narrated words, scaled to
 * the measured audio length, so the picture turns when the narrator does and
 * the deck can never drift or outrun the voice.
 *
 * usage: (cd docs && python3 -m http.server 8944 &) ; node scripts/build-pressure-check-video.js
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { webkit } = require('/Users/moop_bot_pro/Scripts/cdp-tmc/node_modules/playwright-core');

const WORK  = '/tmp/pcvid2';
const AUDIO = process.env.PC_AUDIO || '/tmp/pc2-narration.mp3';
const NARR  = process.env.PC_NARR  || '/tmp/pc2-narration.txt';
const OUT   = process.env.PC_OUT   || '/tmp/pressure-check-walkthrough-1080p.mp4';
const URL   = 'http://127.0.0.1:8944/memorize.html';
const FPS = 30, XF = 0.9;            // crossfade seconds
fs.mkdirSync(WORK, { recursive: true });

/* marker = the phrase in the narration where this beat starts.
   push  = 'in' | 'out' — alternating keeps the motion from feeling mechanical. */
const BEATS = [
  { id:'title',  k:'Uniting, Serving, Mentoring & Counseling Ministries', t:'Pressure Check',
    s:'Scripture memory, word perfect', marker:null, shot:null, push:'in' },
  { id:'why',    k:'The Question', t:'A round in the chamber',
    s:'Why walk out with the weapon loaded and the word empty?', marker:'So here is the question', shot:null, push:'out' },
  { id:'home',   k:'Free. In Your Pocket.', t:'Built the way they taught it',
    s:'Index cards and a pencil, carried into your phone', marker:'This is Pressure Check', shot:'home', push:'in' },
  { id:'hand',   k:'The Word Hand', t:'Five ways to take hold',
    s:'Hear · Read · Study · Memorize · Meditate', marker:'Now, they had a picture', shot:'hand', push:'out' },
  { id:'hear',   k:'Little Finger', t:'Hearing is the weakest grip',
    s:'A lifetime under good preaching, holding almost nothing', marker:'The little finger is hearing', shot:'hand', push:'in' },
  { id:'study',  k:'Middle Finger', t:'Now you are digging',
    s:'They searched the Scriptures daily', marker:'The middle finger is study', shot:'hand', push:'out' },
  { id:'hide',   k:'Index Finger', t:'Hidden. Not bookmarked.',
    s:'Thy word have I hid in mine heart', marker:'The index finger is memory', shot:'hand', push:'in' },
  { id:'thumb',  k:'The Thumb', t:'It touches every finger',
    s:'Meditation is what makes the grip hold', marker:'And the thumb is meditation', shot:'hand', push:'out' },
  { id:'wheel',  k:'The Wheel', t:'Christ at the hub',
    s:'Obedience is the rim. Four spokes carry the load.', marker:'The Navigators drew a second', shot:'wheel', push:'in' },
  { id:'spoke',  k:'Word · Prayer · Fellowship · Witness', t:'Pull one and it stops carrying weight',
    s:'The wheel still rolls for a while. That is the danger.', marker:'Take out a spoke', shot:'wheel', push:'out' },
  { id:'tap',    k:'Tap Anything', t:'The diagram teaches',
    s:'Every finger and spoke opens its own verses', marker:'Tap any finger', shot:'browse', push:'in' },
  { id:'fore',   k:'Fore and Aft', t:'A verse you can find',
    s:'Reference, verse, reference — the way it was taught', marker:'Then the work', shot:'card', push:'out' },
  { id:'diff',   k:'The Check', t:'Exactly where you drifted',
    s:'Every word missed. Every word invented.', marker:'And when you are done', shot:'diff', push:'in' },
  { id:'score',  k:'Not Pass or Fail', t:'Eighty percent is not failure',
    s:'It is a man who did the work and is not finished', marker:'Word perfect means every word', shot:'score', push:'out' },
  { id:'ladder', k:'The Ladder', t:'Read. Blank. First letter. Cold.',
    s:'As much help as you need, and no more', marker:'Read it. Let it take', shot:'ladder', push:'in' },
  { id:'paper',  k:'Paper', t:'It prints a real card',
    s:'Three by five, reference on both ends', marker:'And it will print you', shot:'print', push:'out' },
  { id:'cta',    k:'Begin', t:'usmcmin.org/memorize',
    s:'Be faithful. Be fruitful. Keep one in the chamber.', marker:'Brothers, you already know', shot:null, push:'in' },
];

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

/* Beat boundaries come from the ACTUAL audio, not a word-count proxy.
   whisper gives every word a timestamp; scripts/align-narration.js finds when
   each marker phrase is really spoken. The old word-share model assumed a
   uniform speaking rate and ran the picture up to 2.9s ahead of the voice,
   which is exactly what "the slides advance too quickly" felt like.

   Each beat is its spoken length plus one crossfade, which makes the xfade
   offset for beat i fall naturally on cut[i]; the offset is then pulled back
   half a fade so the dissolve straddles the line rather than starting on it. */
function cutTimes(total) {
  const markers = BEATS.map(b => b.marker);
  fs.writeFileSync(path.join(WORK, 'markers.json'), JSON.stringify(markers));
  const wordsJson = process.env.PC_WORDS || '/tmp/pc2-words.json';
  if (!fs.existsSync(wordsJson)) {
    throw new Error(`no word timings at ${wordsJson}. Run:\n` +
      `  ffmpeg -y -i ${AUDIO} -ar 16000 -ac 1 -c:a pcm_s16le /tmp/pc2.wav\n` +
      `  whisper-cli -m ~/.openclaw/whisper_models/ggml-large-v3.bin -f /tmp/pc2.wav -oj -ml 1 -of /tmp/pc2-words`);
  }
  const out = execFileSync('node',
    [path.join(__dirname, 'align-narration.js'), wordsJson, path.join(WORK, 'markers.json')]).toString();
  const cuts = JSON.parse(out);
  if (cuts.length !== BEATS.length) throw new Error('cut count does not match beat count');
  for (let i = 1; i < cuts.length; i++) {
    if (cuts[i] <= cuts[i - 1]) throw new Error(`cuts not increasing at beat ${i}`);
  }
  const segs = cuts.map((c, i) => (i + 1 < cuts.length ? cuts[i + 1] : total) - c);
  return { cuts, durs: segs.map(d => d + XF) };
}

async function capture() {
  const b = await webkit.launch({ headless: true });
  const ctx = await b.newContext({ viewport:{width:430,height:900}, deviceScaleFactor:2, colorScheme:'dark' });
  const page = await ctx.newPage();
  const shot = n => page.screenshot({ path: path.join(WORK, `shot-${n}.png`) });

  await page.goto(URL, { waitUntil:'networkidle' });
  await page.waitForTimeout(1200);
  await shot('home');
  await page.locator('#handSvg').screenshot({ path: path.join(WORK,'shot-hand.png') });
  await page.locator('#wheelSvg').screenshot({ path: path.join(WORK,'shot-wheel.png') });

  /* Click the hit rect, not the group: the group's bounding box also contains
     its offset label, so the box centre sits in dead space between the two. */
  await page.locator('#handSvg [data-part="index"] .hit').click();
  await page.waitForTimeout(900);
  await shot('browse');

  await page.click('#btnBrowseBack'); await page.waitForTimeout(400);
  await page.locator('#packs .pack').first().click(); await page.waitForTimeout(600);
  await page.click('[data-step="read"]'); await page.waitForTimeout(400);
  await shot('card');

  const ref = (await page.locator('#refFore').textContent()).trim();
  const truth = (await page.locator('#vBack').textContent()).trim();
  const w = truth.split(/\s+/);
  await page.fill('#answer', `${ref} ${w.slice(0,4).concat(['and']).concat(w.slice(6)).join(' ')}`);
  await page.click('#btnCheck'); await page.waitForTimeout(800);
  await shot('diff');
  await page.locator('.score').scrollIntoViewIfNeeded(); await page.waitForTimeout(400);
  await shot('score');

  await page.click('#btnAgain'); await page.waitForTimeout(400);
  await page.click('[data-step="blank"]'); await page.waitForTimeout(400);
  await shot('ladder');

  const p2 = await (await b.newContext({ viewport:{width:820,height:1060}, deviceScaleFactor:2, colorScheme:'dark' })).newPage();
  await p2.goto(URL, { waitUntil:'networkidle' }); await p2.waitForTimeout(900);
  await p2.evaluate(() => { window.print = () => {}; });
  await p2.click('#btnPrint'); await p2.waitForTimeout(500);
  await p2.emulateMedia({ media:'print' }); await p2.waitForTimeout(400);
  await p2.screenshot({ path: path.join(WORK,'shot-print.png') });
  await b.close();
}

function slideHTML(beat, uri) {
  const wide = beat.shot === 'print';
  const art = uri ? `<img class="shot${wide?' wide':''}" src="${uri}">` : '';
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{width:1920px;height:1080px;background:#000;color:#fff;font-family:Inter,sans-serif;
      display:flex;align-items:center;gap:70px;padding:110px 165px;overflow:hidden;
      background-image:radial-gradient(ellipse at 20% -10%,rgba(212,175,55,.15),transparent 60%)}
 .copy{flex:1;min-width:0}
 .kicker{color:#D4AF37;font-size:20px;font-weight:700;letter-spacing:.26em;
         text-transform:uppercase;margin-bottom:20px}
 .kicker::after{content:"";display:block;width:68px;height:2px;background:#D4AF37;opacity:.85;margin-top:18px}
 h1{font-family:"Playfair Display",serif;font-size:62px;line-height:1.08;margin-bottom:24px}
 p{color:#b9c2cc;font-size:26px;line-height:1.5;max-width:23ch}
 .shot{height:840px;border-radius:20px;border:1px solid #2a2a2a;box-shadow:0 30px 80px rgba(0,0,0,.75)}
 .shot.wide{height:800px;border-radius:8px}
 .brand{position:absolute;bottom:52px;left:165px;color:#7d858e;font-size:17px;
        letter-spacing:.17em;text-transform:uppercase}
 .full{justify-content:center;text-align:center}
 .full .copy{flex:none;max-width:1180px}
 .full p{max-width:none;margin:0 auto}
 .full .kicker::after{margin-left:auto;margin-right:auto}
</style></head>
<body class="${art?'':'full'}">
  <div class="copy">
    <div class="kicker">${esc(beat.k)}</div>
    <h1>${esc(beat.t)}</h1>
    <p>${esc(beat.s)}</p>
  </div>
  ${art}
  <div class="brand">Uniting, Serving, Mentoring and Counseling Ministries &middot; usmcmin.org</div>
</body></html>`;
}

(async () => {
  console.log('capturing the live page…');
  await capture();

  const audioSecs = parseFloat(execFileSync('ffprobe',
    ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1', AUDIO]).toString().trim());
  const { cuts, durs } = cutTimes(audioSecs);
  console.log(`audio ${audioSecs.toFixed(1)}s across ${BEATS.length} beats, cut to the spoken word`);

  const b = await webkit.launch({ headless: true });
  const page = await (await b.newContext({ viewport:{width:1920,height:1080} })).newPage();
  for (let i = 0; i < BEATS.length; i++) {
    const beat = BEATS[i];
    let uri = null;
    if (beat.shot) {
      const f = path.join(WORK, `shot-${beat.shot}.png`);
      if (fs.existsSync(f)) uri = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    }
    await page.setContent(slideHTML(beat, uri), { waitUntil:'load' });
    await page.waitForTimeout(750);                    // let the webfonts land
    await page.screenshot({ path: path.join(WORK, `slide-${String(i).padStart(2,'0')}.png`) });
    console.log(`  cut ${String(cuts[i].toFixed(1)).padStart(6)}s  hold ${String((durs[i]-XF).toFixed(1)).padStart(5)}s  ${beat.t.slice(0,38)}`);
  }
  await b.close();

  /* Motion. Each still is oversampled to 2x then zoompan'd, because zoompan on
     a 1:1 source stair-steps visibly. Alternating in/out keeps a 17-beat film
     from feeling like one long dolly. */
  /* ONE frame per input — no -loop. zoompan's `d` expands a single frame into
     the whole beat. Feeding it a looped stream instead makes it expand EVERY
     incoming frame by d, which pins `on` near zero and yields a perfectly
     static "pan": the first cut of this video had no motion at all and the
     frames one second apart were byte-identical. */
  const inputs = [];
  for (let i = 0; i < BEATS.length; i++) {
    inputs.push('-i', path.join(WORK, `slide-${String(i).padStart(2,'0')}.png`));
  }
  let fc = '';
  BEATS.forEach((beat, i) => {
    const frames = Math.round(durs[i] * FPS);
    /* Accumulate through zoompan's `zoom` variable rather than computing from
       `on`. With a single input frame `on` never advances, so an `on`-based
       expression renders a perfectly static frame — which is how the first two
       cuts of this shipped with no motion at all despite the filter running. */
    /* Every beat pushes IN, and the rate is derived from that beat's own frame
       count so the move lasts exactly as long as the beat. A fixed rate made
       short beats crawl and long beats hit the ceiling early and then sit
       perfectly still for the remainder — which is how a "cinematic" cut ended
       up with dead stretches. A pull-out would need `on` to seed a high
       starting zoom, and `on` never advances on a single input frame. */
    const cap = beat.push === 'in' ? 1.09 : 1.055;   // alternating depth, not direction
    const z = `min(zoom+${((cap - 1) / frames).toFixed(6)},${cap})`;
    fc += `[${i}:v]scale=3840:-1,zoompan=z='${z}':d=${frames}:` +
          `x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=${FPS},setsar=1[v${i}];`;
  });
  let prev = 'v0';
  for (let i = 1; i < BEATS.length; i++) {
    const out = i === BEATS.length - 1 ? 'vout' : `x${i}`;
    // Straddle the line: the dissolve is centred on the moment it is spoken.
    const off = Math.max(0.1, cuts[i] - XF / 2);
    fc += `[${prev}][v${i}]xfade=transition=fade:duration=${XF}:offset=${off.toFixed(3)}[${out}];`;
    prev = out;
  }
  fc = fc.replace(/;$/, '');

  console.log('encoding (zoompan + crossfades — this takes a few minutes)…');
  execFileSync('ffmpeg', ['-hide_banner','-v','error','-y', ...inputs,
    '-i', AUDIO,
    '-filter_complex', fc, '-map','[vout]', '-map', `${BEATS.length}:a`,
    '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r',String(FPS),
    '-c:a','aac','-b:a','192k',
    '-t', String(audioSecs),      // -shortest does not bound this graph; -t does
    '-movflags','+faststart', OUT], { stdio:'inherit' });

  const secs = parseFloat(execFileSync('ffprobe',
    ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1', OUT]).toString().trim());
  console.log(`\nwrote ${OUT}  ${Math.floor(secs/60)}:${String(Math.round(secs%60)).padStart(2,'0')}  ${(fs.statSync(OUT).size/1048576).toFixed(1)} MB`);
})();
