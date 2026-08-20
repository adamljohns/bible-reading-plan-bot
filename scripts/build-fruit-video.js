#!/usr/bin/env node
/* build-fruit-video.js — a narrated "video overview" for the Bear Much Fruit study.
 *
 * NotebookLM-style: brand slides carrying the study's own artwork, timed against
 * the narration that already exists at docs/assets/media/bear-much-fruit.mp3.
 *
 * Slide durations are NOT guessed. Each slide maps to a section of the narration
 * script, and its share of the runtime is its share of the narrated words — so
 * the picture changes roughly when the narrator does. Total is then scaled to the
 * measured audio duration, which means the deck can never drift out of sync with
 * the voice track or end early over silence.
 *
 * Slides are rendered in the browser rather than drawn with ffmpeg filters so the
 * type is the real brand type (Playfair + Inter), not a system fallback.
 *
 * usage: node scripts/build-fruit-video.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('/Users/moop_bot_pro/Scripts/cdp-tmc/node_modules/playwright-core');

const REPO = path.dirname(__dirname);
const WORK = '/tmp/fruitvid';
const AUDIO = path.join(REPO, 'docs/assets/media/bear-much-fruit.mp3');
const OUT = path.join(REPO, 'docs/assets/media/bear-much-fruit-overview.mp4');
const NARRATION = '/tmp/fruit-narration.txt';

/* Each slide: the heading shown, the artwork panel, and the phrase in the
   narration where this section begins. The marker is what ties runtime to voice. */
const SLIDES = [
  { art: 'full.png',        kicker: 'A John 15 Study',        title: 'Bear Much Fruit',
    sub: 'Abide in Christ · Walk by the Spirit · Bear fruit that glorifies the Father', marker: null },
  { art: 'banners.png',     kicker: 'The Floor and the Ceiling', title: 'Two verses that fence in everything else',
    sub: '“Without me ye can do nothing.” · “Herein is my Father glorified.”', marker: 'Two verses that fence' },
  { art: 'center.png',      kicker: 'John 15:4',              title: 'Abide is not a mood',
    sub: 'The branch does not generate sap. We abide, He works.', marker: 'Abide is not a mood' },
  { art: 'center.png',      kicker: 'John 15:2',              title: 'The pruning nobody volunteers for',
    sub: 'The fruitful branch gets cut too — because it is fruitful.', marker: 'The pruning nobody' },
  { art: 'left.png',        kicker: 'Eight Kinds',            title: 'Fruit in us',
    sub: 'What God grows on the inside — character before conduct.', marker: 'Fruit in us' },
  { art: 'right.png',       kicker: 'Eight More',             title: 'Fruit through us',
    sub: 'Same vine, same sap, now running into somebody else’s life.', marker: 'Fruit through us' },
  { art: 'progression.png', kicker: 'The Chain',              title: 'The progression, and why the order will not bend',
    sub: 'Abide → Walk → Character → Obedience → Service → Witness → Multiply → Glory', marker: 'The progression, and why' },
  { art: 'footer.png',      kicker: 'John 15:13',             title: 'Not my fruit. His fruit. His glory.',
    sub: 'Faithful Marines. Fruitful disciples. Glorious God.', marker: 'Not my fruit' },
  { art: 'full.png',        kicker: 'This Week',              title: 'What to do with this',
    sub: 'Find your entry point · Name the pruning · Pick the fruit you avoid · Name one faithful man', marker: 'What to do with this' },
];

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function slideHTML(s, artDataUri) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1920px;height:1080px;background:#0d1117;color:#e6edf3;
       font-family:Inter,system-ui,sans-serif;display:flex;flex-direction:column;
       align-items:center;justify-content:center;padding:52px 90px 78px;overflow:hidden;
       background-image:radial-gradient(ellipse at 50% 0%,rgba(30,58,95,.45),transparent 62%)}
  .kicker{color:#d4af37;font-size:22px;font-weight:700;letter-spacing:.22em;
          text-transform:uppercase;margin-bottom:14px}
  .kicker::after{content:"";display:block;width:64px;height:2px;background:#d4af37;
          opacity:.8;margin:16px auto 0}
  h1{font-family:"Playfair Display",serif;font-size:56px;line-height:1.14;text-align:center;
     max-width:24ch;margin-bottom:14px}
  .sub{color:#a9b4c0;font-size:24px;line-height:1.45;text-align:center;max-width:64ch;margin-bottom:28px}
  /* A fixed box with object-fit:contain SCALES UP the narrow column panels as
     well as shrinking the wide ones; max-height alone only ever shrinks, which
     left the tall crops floating small in a 1080p frame. No border here — the
     artwork carries its own card edge and a border would frame the empty box
     rather than the picture. */
  .art{height:620px;width:1560px;object-fit:contain;
       filter:drop-shadow(0 18px 44px rgba(0,0,0,.55))}
  .brand{position:absolute;bottom:38px;color:#8b949e;font-size:19px;letter-spacing:.14em;
         text-transform:uppercase}
</style></head><body>
  <div class="kicker">${esc(s.kicker)}</div>
  <h1>${esc(s.title)}</h1>
  <div class="sub">${esc(s.sub)}</div>
  <img class="art" src="${artDataUri}">
  <div class="brand">Uniting, Serving, Mentoring and Counseling Ministries · usmcmin.org</div>
</body></html>`;
}

/* Runtime per slide = that section's share of the narrated words. */
function durations(totalSeconds) {
  const text = fs.readFileSync(NARRATION, 'utf8');
  const idx = SLIDES.map(s => (s.marker ? text.indexOf(s.marker) : 0));
  for (let i = 0; i < idx.length; i++) {
    if (idx[i] === -1) throw new Error(`marker not found in narration: "${SLIDES[i].marker}"`);
  }
  const words = idx.map((start, i) => {
    const end = i + 1 < idx.length ? idx[i + 1] : text.length;
    return text.slice(start, end).split(/\s+/).filter(Boolean).length;
  });
  const total = words.reduce((a, b) => a + b, 0);
  return words.map(w => Math.max(6, (w / total) * totalSeconds));
}

(async () => {
  const audioSecs = parseFloat(execFileSync('ffprobe',
    ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1', AUDIO])
    .toString().trim());
  const durs = durations(audioSecs);
  console.log(`audio ${audioSecs.toFixed(1)}s across ${SLIDES.length} slides`);

  const browser = await chromium.launch({ headless: true });
  const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();

  for (let i = 0; i < SLIDES.length; i++) {
    const s = SLIDES[i];
    const art = fs.readFileSync(path.join(WORK, s.art)).toString('base64');
    await page.setContent(slideHTML(s, `data:image/png;base64,${art}`), { waitUntil: 'load' });
    await page.waitForTimeout(600);   // let the webfonts land before capturing
    const out = path.join(WORK, `slide-${String(i).padStart(2, '0')}.png`);
    await page.screenshot({ path: out });
    console.log(`  slide ${i}  ${durs[i].toFixed(1).padStart(6)}s  ${s.title.slice(0, 46)}`);
  }
  await browser.close();

  const list = SLIDES.map((s, i) =>
    `file '${path.join(WORK, `slide-${String(i).padStart(2,'0')}.png`)}'\nduration ${durs[i].toFixed(3)}`
  ).join('\n') + `\nfile '${path.join(WORK, `slide-${String(SLIDES.length-1).padStart(2,'0')}.png`)}'\n`;
  fs.writeFileSync(path.join(WORK, 'slides.txt'), list);

  console.log('encoding…');
  execFileSync('ffmpeg', ['-hide_banner','-v','error','-y',
    '-f','concat','-safe','0','-i', path.join(WORK,'slides.txt'),
    '-i', AUDIO,
    '-c:v','libx264','-pix_fmt','yuv420p','-r','30',
    '-vf','scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1:color=0x0d1117',
    '-c:a','aac','-b:a','160k','-t', String(audioSecs),
    '-movflags','+faststart', OUT],
    { stdio: 'inherit' });

  const secs = parseFloat(execFileSync('ffprobe',
    ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1', OUT]).toString().trim());
  const mb = (fs.statSync(OUT).size / 1048576).toFixed(1);
  console.log(`\nwrote ${path.relative(REPO, OUT)}  ${Math.floor(secs/60)}:${String(Math.round(secs%60)).padStart(2,'0')}  ${mb} MB`);
})();
