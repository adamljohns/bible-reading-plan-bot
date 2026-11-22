'use strict';
// Redirect-following homepage fetch shared by the website checker callers.
// Resolves to the final 200 page's HTML, or '' on any failure/non-200.
const http = require('http');
const https = require('https');

function fetchText(url, depth = 0, timeoutMs = 12000) {
  return new Promise(resolve => {
    if (depth > 4) return resolve('');
    let done = false; const fin = v => { if (!done) { done = true; resolve(v); } };
    try {
      const lib = url.startsWith('https') ? https : http;
      const req = lib.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 MOOPDirectoryBot/1.1 (+https://usmcmin.org)', 'Accept': 'text/html,application/xhtml+xml' }, rejectUnauthorized: false }, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          res.resume();
          let next; try { next = new URL(res.headers.location, url).href; } catch (_) { return fin(''); }
          return fetchText(next, depth + 1, timeoutMs).then(fin);
        }
        if (res.statusCode !== 200) { res.resume(); return fin(''); }
        let b = ''; res.setEncoding('utf8');
        res.on('data', d => { b += d; if (b.length > 400000) { req.destroy(); fin(b); } });
        res.on('end', () => fin(b)); res.on('error', () => fin(b));
      });
      req.on('error', () => fin('')); req.setTimeout(timeoutMs, () => { req.destroy(); fin(''); });
    } catch (_) { fin(''); }
  });
}

module.exports = { fetchText };
