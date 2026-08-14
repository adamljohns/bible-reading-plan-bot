#!/usr/bin/env node
/* test-memorize.js — drive /memorize.html in WebKit (iPhone is the target) and
 * assert behaviour. Exits non-zero on any failure; a gate that cannot fail is
 * not a gate. Lives in the repo rather than /tmp so it survives cleanup.
 *
 * usage: (cd docs && python3 -m http.server 8944 &) ; node scripts/test-memorize.js
 */
const { webkit } = require('/Users/moop_bot_pro/Scripts/cdp-tmc/node_modules/playwright-core');

const URL = process.env.MEM_URL || 'http://127.0.0.1:8944/memorize.html';
let failures = 0;
const check = (name, got, want) => {
  const ok = typeof want === 'function' ? want(got) : got === want;
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `  got=${JSON.stringify(got)}`}`);
  if (!ok) failures++;
};

(async () => {
  const b = await webkit.launch({ headless: true });
  const page = await (await b.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
  })).newPage();

  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  console.log('\n— load —');
  check('no JS errors', errs.length, 0);
  check('packs rendered', await page.locator('#packs .pack').count(), n => n >= 5);
  check('translations populated', await page.locator('#tr option').count(), n => n >= 8);

  console.log('\n— drill —');
  await page.locator('#packs .pack').first().click();
  await page.waitForTimeout(400);
  const ref = (await page.locator('#refFore').textContent()).trim();
  const truth = (await page.locator('#vBack').textContent()).trim();
  check('reference fore and aft match', (await page.locator('#refAftF').textContent()).trim(), ref);
  /* Not tautological: comparing the app's text to itself once let Strong's
     markup score 100%. Assert against the shape of real prose instead. */
  check('no markup in verse', truth, t => !/[<>]/.test(t));
  check('no Strong\'s digits', truth, t => !/\d{3,}/.test(t));
  check('no KJV margin note', truth, t => !/\b[a-z][\w-]*:\s+(or|Heb|Gr|Gk)\b/.test(t));
  check('answer hidden before flip', await page.locator('#vBack').isVisible(), false);
  const cardH = await page.locator('#card').evaluate(el => el.getBoundingClientRect().height);
  const textH = await page.locator('#vBack').evaluate(el => el.scrollHeight);
  check('card sized to verse', cardH, h => h >= textH);

  await page.fill('#answer', `${ref} ${truth} ${ref}`);
  await page.click('#btnCheck'); await page.waitForTimeout(300);
  check('word perfect scores 100%', (await page.locator('.pct').textContent()).trim(), '100%');

  await page.click('#btnAgain');
  const w = truth.split(/\s+/);
  await page.fill('#answer', `${ref} ${w.slice(0,3).concat(w.slice(4)).join(' ')} ${ref}`);
  await page.click('#btnCheck'); await page.waitForTimeout(300);
  check('one dropped word stays >80', parseInt(await page.locator('.pct').textContent(), 10), n => n > 80 && n < 100);
  check('missed word marked', await page.locator('.diff .want').count(), n => n >= 1);

  await page.click('#btnAgain');
  await page.fill('#answer', 'the quick brown fox jumped over something unrelated entirely');
  await page.click('#btnCheck'); await page.waitForTimeout(300);
  check('gibberish scores low', parseInt(await page.locator('.pct').textContent(), 10), n => n < 40);

  console.log('\n— drill modes —');
  await page.click('#btnNext'); await page.waitForTimeout(200);
  await page.click('[data-step="first"]'); await page.waitForTimeout(200);
  check('first-letter mode', (await page.locator('#vFront').textContent()).trim(),
        t => t.split(/\s+/).every(x => x.replace(/[^A-Za-z]/g, '').length <= 1));
  await page.click('[data-step="blank"]'); await page.waitForTimeout(200);
  check('fill-blank shows blanks', await page.locator('#vFront .blank').count(), n => n >= 1);
  await page.click('#btnFlag'); await page.waitForTimeout(150);
  check('flag toggles', await page.locator('#btnFlag').textContent(), t => /Flagged/.test(t));
  check('flag forces daily', await page.evaluate(() => {
    const st = JSON.parse(localStorage.getItem('moop.memorize.v1'));
    return Object.values(st.cards).some(c => c.flagged && c.bucket === 'daily');
  }), true);

  console.log('\n— browse + stack —');
  await page.evaluate(() => localStorage.removeItem('moop.memorize.v1'));
  await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(600);
  await page.click('#btnBrowse'); await page.waitForTimeout(300);
  check('browse opens', await page.locator('#browse').isVisible(), true);
  const r1 = (await page.locator('#bRefFore').textContent()).trim();
  check('browse shows a verse', (await page.locator('#bText').textContent()).trim().length, n => n > 15);
  check('browse ref fore and aft match', (await page.locator('#bRefAft').textContent()).trim(), r1);
  await page.click('#btnNextV'); await page.waitForTimeout(200);
  check('Next advances', (await page.locator('#bRefFore').textContent()).trim(), t => t !== r1);
  check('browsing never grades', await page.locator('#browse .pct').count(), 0);
  await page.click('#btnPrev'); await page.waitForTimeout(200);
  check('Prev goes back', (await page.locator('#bRefFore').textContent()).trim(), r1);

  await page.click('#btnAdd'); await page.waitForTimeout(250);
  check('add flips to remove', await page.locator('#btnAdd').textContent(), t => /remove/i.test(t));
  const st1 = await page.evaluate(() => JSON.parse(localStorage.getItem('moop.memorize.v1')).cards);
  check('verse entered the stack', Object.keys(st1).length, 1);
  await page.click('#btnAdd'); await page.waitForTimeout(200);
  check('add is reversible', await page.evaluate(() =>
    Object.keys(JSON.parse(localStorage.getItem('moop.memorize.v1')).cards).length), 0);
  await page.click('#btnAdd'); await page.waitForTimeout(200);
  await page.click('#btnBrowseBack'); await page.waitForTimeout(250);
  check('My Stack pack appears', await page.locator('[data-pack="__stack"]').count(), 1);
  await page.locator('[data-pack="__stack"]').click(); await page.waitForTimeout(300);
  check('My Stack is drillable', await page.locator('#drill').isVisible(), true);
  await page.click('#btnQuit'); await page.waitForTimeout(250);

  console.log('\n— two-verse cards —');
  const rng = await page.evaluate(async () => {
    const d = await (await fetch('/data/memory-packs.json')).json();
    const v = d.packs.flatMap(p => p.verses).find(x => /:\d+-\d+$/.test(x.ref));
    return v ? { ref: v.ref, words: v.text.KJV.split(/\s+/).length, txt: v.text.KJV } : null;
  });
  check('a two-verse card exists', !!rng, true);
  check('range ref reads as a range', rng && rng.ref, t => /:\d+-\d+$/.test(t || ''));
  check('holds both verses', rng && rng.words, n => n > 30);
  check('range text still clean', rng && rng.txt, t => !/[<>]/.test(t || '') && !/\s{2,}/.test(t || ''));

  console.log('\n— privacy —');
  check('page source has no personal names', await page.content(),
        t => !/\b(Kenny|Ward Collins|Josiah|Mayhew|LaBounty|McManus)\b/.test(t));
  check('pack data has no personal names',
        await page.evaluate(async () => (await (await fetch('/data/memory-packs.json')).text())),
        t => !/\b(Kenny|Ward|Josiah)\b/.test(t));
  check('stored progress has no names',
        await page.evaluate(() => localStorage.getItem('moop.memorize.v1') || ''),
        t => !/\b(Kenny|Ward|Josiah|Adam)\b/i.test(t));

  console.log('\n— layout —');
  check('no horizontal overflow at 390px',
        await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth),
        n => n <= 0);
  check('still no JS errors', errs.length, 0);

  await page.screenshot({ path: '/tmp/memorize-home.png' });
  await page.click('#btnBrowse'); await page.waitForTimeout(300);
  await page.screenshot({ path: '/tmp/memorize-browse.png' });

  await b.close();
  console.log(`\n${failures ? `${failures} FAILURE(S)` : 'ALL CHECKS PASSED'}`);
  if (errs.length) console.log('errors:', errs.slice(0, 4));
  process.exit(failures ? 1 : 0);
})();
