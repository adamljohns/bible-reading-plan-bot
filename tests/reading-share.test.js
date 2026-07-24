'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright-core');

const DOCS_ROOT = path.resolve(__dirname, '..', 'docs');
const PAGE_PATH = '/readings/2026-07-24.html';
const SLUGS = ['wisdom', 'husband', 'father', 'citizen', 'peace'];

function findChrome() {
  const windowsPaths = [
    process.env.PROGRAMFILES,
    process.env['PROGRAMFILES(X86)'],
    process.env.LOCALAPPDATA,
  ].filter(Boolean).flatMap(base => [
    path.join(base, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    path.join(base, 'Chromium', 'Application', 'chrome.exe'),
  ]);
  return [
    process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    ...windowsPaths,
  ].filter(Boolean).find(candidate => fs.existsSync(candidate));
}

function startDocsServer() {
  const server = http.createServer((request, response) => {
    const requestPath = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const filePath = path.resolve(DOCS_ROOT, `.${requestPath}`);
    if (filePath !== DOCS_ROOT && !filePath.startsWith(`${DOCS_ROOT}${path.sep}`)) {
      response.writeHead(403).end('Forbidden');
      return;
    }
    fs.readFile(filePath, (error, data) => {
      if (error) {
        response.writeHead(error.code === 'ENOENT' ? 404 : 500).end();
        return;
      }
      response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      response.end(data);
    });
  });
  return new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

async function nativeShareTest(browser, baseUrl) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await context.addInitScript(() => {
    window.__sharePayloads = [];
    Object.defineProperty(navigator, 'share', {
      configurable: true,
      value: async payload => window.__sharePayloads.push(payload),
    });
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${baseUrl}${PAGE_PATH}?utm_source=private&recipient=adam#all`, { waitUntil: 'networkidle' });

  assert.equal(await page.locator('button.share-reading').count(), 6, 'six share buttons');
  const allButton = page.getByRole('button', { name: 'Share all of today’s readings' });
  await allButton.click();
  let payloads = await page.evaluate(() => window.__sharePayloads);
  assert.equal(payloads.length, 1, 'all-readings share invoked');
  assert.match(payloads[0].url, /\/readings\/2026-07-24\.html#all$/);
  assert.equal(new URL(payloads[0].url).search, '', 'all-reading share strips query data');

  for (const slug of SLUGS) {
    await page.locator(`.watch-tab[data-tab="${slug}"]`).click();
    assert.equal(await page.locator('section.watch:visible').count(), 1, `${slug} is isolated`);
    assert.equal(await allButton.isHidden(), true, 'all-share button hidden on individual watch');
    const button = page.locator(`section[data-watch="${slug}"] button.share-reading`);
    await button.click();
    payloads = await page.evaluate(() => window.__sharePayloads);
    assert.match(payloads.at(-1).url, new RegExp(`#${slug}$`));
    assert.equal(new URL(payloads.at(-1).url).search, '', `${slug} share strips query data`);
  }

  assert.equal(errors.length, 0, `browser errors: ${errors.join(' | ')}`);
  await context.close();
  console.log('PASS native share: #all plus five individual watch links');
}

async function clipboardFallbackTest(browser, baseUrl) {
  const context = await browser.newContext();
  await context.addInitScript(() => {
    window.__copiedLinks = [];
    Object.defineProperty(navigator, 'share', { configurable: true, value: undefined });
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText: async value => window.__copiedLinks.push(value) },
    });
  });
  const page = await context.newPage();
  await page.goto(`${baseUrl}${PAGE_PATH}?utm_source=private&recipient=adam#wisdom`, { waitUntil: 'networkidle' });
  await page.locator('section[data-watch="wisdom"] button.share-reading').click();
  const copied = await page.evaluate(() => window.__copiedLinks);
  assert.equal(copied.length, 1, 'clipboard fallback invoked');
  assert.match(copied[0], /\/readings\/2026-07-24\.html#wisdom$/);
  assert.equal(new URL(copied[0]).search, '', 'clipboard share strips query data');
  const status = page.locator('section[data-watch="wisdom"] .share-status');
  assert.equal(await status.getAttribute('aria-live'), 'polite', 'share status is announced');
  assert.equal(await status.textContent(), '✓ Link copied', 'clipboard result reaches live region');
  await context.close();
  console.log('PASS clipboard fallback: Morning Wisdom link copied');
}

(async () => {
  const chromePath = findChrome();
  assert.ok(chromePath, 'Chrome/Chromium not found; set CHROME_PATH');
  const localServer = await startDocsServer();
  let browser = null;
  try {
    browser = await chromium.launch({ headless: true, executablePath: chromePath });
    await nativeShareTest(browser, localServer.baseUrl);
    await clipboardFallbackTest(browser, localServer.baseUrl);
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => localServer.server.close(resolve));
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
