'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright-core');

const DOCS_ROOT = path.resolve(__dirname, '..', 'docs');
const CASES = [
  ['real-man-assessment.html', 3],
  ['resolute-citizen-assessment.html', 3],
  ['happy-husband.html', 2],
  ['fulfilled-father.html', 3],
  ['purity-assessment.html', 3],
];

function findChrome() {
  const windowsPaths = [
    process.env.PROGRAMFILES,
    process.env['PROGRAMFILES(X86)'],
    process.env.LOCALAPPDATA,
  ].filter(Boolean).flatMap(base => [
    path.join(base, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    path.join(base, 'Chromium', 'Application', 'chrome.exe'),
  ]);
  const candidates = [
    process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    ...windowsPaths,
  ].filter(Boolean);
  return candidates.find(candidate => fs.existsSync(candidate));
}

function contentType(filePath) {
  if (filePath.endsWith('.html')) return 'text/html; charset=utf-8';
  if (filePath.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (filePath.endsWith('.css')) return 'text/css; charset=utf-8';
  if (filePath.endsWith('.png')) return 'image/png';
  return 'application/octet-stream';
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
      response.writeHead(200, { 'Content-Type': contentType(filePath) });
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

(async () => {
  const chromePath = findChrome();
  assert.ok(chromePath, 'Chrome/Chromium not found; set CHROME_PATH to its executable');

  let localServer = null;
  let baseUrl = process.env.ASSESSMENT_BASE_URL;
  if (!baseUrl) {
    localServer = await startDocsServer();
    baseUrl = localServer.baseUrl;
  }

  let browser = null;
  const failures = [];

  try {
    browser = await chromium.launch({ headless: true, executablePath: chromePath });
    for (const [pageName, expectedAreas] of CASES) {
      const page = await browser.newPage();
      page.setDefaultTimeout(10000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));

      try {
        await page.goto(`${baseUrl}/${pageName}`, { waitUntil: 'networkidle' });
        await page.locator('input[type="range"]').first().evaluate((slider) => {
          slider.value = '2';
          slider.dispatchEvent(new Event('input', { bubbles: true }));
        });
        await page.getByRole('button', { name: /Generate Formation Plan/ }).click();

        const formation = page.locator('#formation-plan');
        await formation.waitFor({ state: 'visible' });
        const areas = await formation.locator('.formation-area').count();
        assert.equal(areas, expectedAreas, `${pageName} formation area count`);
        assert.equal(errors.length, 0, `${pageName} browser errors: ${errors.join(' | ')}`);
        console.log(`PASS ${pageName}: ${areas} formation areas`);
      } catch (error) {
        failures.push(`${pageName}: ${error.message}; page errors: ${errors.join(' | ') || 'none'}`);
        console.error(`FAIL ${failures[failures.length - 1]}`);
      } finally {
        await page.close();
      }
    }
  } finally {
    if (browser) await browser.close();
    if (localServer) await new Promise(resolve => localServer.server.close(resolve));
  }

  if (failures.length) {
    console.error(`\n${failures.length} assessment(s) failed`);
    process.exitCode = 1;
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
