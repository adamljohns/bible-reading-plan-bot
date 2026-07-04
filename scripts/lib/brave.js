// Brave Search API client. Reads the SAME key the OpenClaw fleet already uses
// (~/.openclaw/openclaw.json → plugins.entries.brave.config.webSearch.apiKey), so
// there is ONE key, never duplicated into a second file. Used by the church- and
// website-discovery scripts to grow the directory past the enrichment sliver.
//
// Brave free tier = 1 query/sec, 2,000/mo; paid tiers higher. CALLERS MUST throttle
// (≥1.1s between calls) — see the sleep in the discovery scripts.
const fs = require('fs');
const https = require('https');
const os = require('os');
const path = require('path');

let _key = null;
function apiKey() {
  if (_key) return _key;
  const p = process.env.BRAVE_API_KEY_FILE || path.join(os.homedir(), '.openclaw/openclaw.json');
  if (process.env.BRAVE_API_KEY) return (_key = process.env.BRAVE_API_KEY);
  const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
  const k = cfg && cfg.plugins && cfg.plugins.entries && cfg.plugins.entries.brave &&
    cfg.plugins.entries.brave.config && cfg.plugins.entries.brave.config.webSearch &&
    cfg.plugins.entries.brave.config.webSearch.apiKey;
  if (!k) throw new Error('Brave API key not found (env BRAVE_API_KEY or openclaw.json plugins.entries.brave.config.webSearch.apiKey)');
  return (_key = k);
}

function braveSearch(query, { count = 10, country = 'us', freshness = null } = {}) {
  return new Promise((resolve, reject) => {
    let u = 'https://api.search.brave.com/res/v1/web/search?q=' + encodeURIComponent(query) +
      '&count=' + count + '&country=' + country + '&result_filter=web';
    if (freshness) u += '&freshness=' + freshness;
    const req = https.get(u, { headers: { Accept: 'application/json', 'Accept-Encoding': 'gzip', 'X-Subscription-Token': apiKey() } }, res => {
      const chunks = [];
      const gunzip = res.headers['content-encoding'] === 'gzip' ? require('zlib').createGunzip() : null;
      const stream = gunzip ? res.pipe(gunzip) : res;
      stream.on('data', d => chunks.push(d));
      stream.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        if (res.statusCode !== 200) return reject(new Error('Brave HTTP ' + res.statusCode + ': ' + body.slice(0, 200)));
        try {
          const j = JSON.parse(body);
          resolve((j.web && j.web.results) || []);
        } catch (e) { reject(new Error('Brave parse: ' + e.message)); }
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => req.destroy(new Error('Brave timeout')));
  });
}

module.exports = { braveSearch };
