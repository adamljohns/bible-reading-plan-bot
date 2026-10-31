// Local SearXNG client (self-hosted, free, no key) with the same result shape as
// lib/brave.js (array of {url,title,description}). Default backend for directory
// website-discovery since 2026-10-31 (Principal: "I'm good with the free search").
// Base URL: SEARX_URL env or http://127.0.0.1:8888.
const http = require('http');
const https = require('https');

function searxSearch(query, { count = 10 } = {}) {
  const base = (process.env.SEARX_URL || 'http://127.0.0.1:8888').replace(/\/+$/, '');
  const u = `${base}/search?q=${encodeURIComponent(query)}&format=json&language=en-US&safesearch=0`;
  const mod = u.startsWith('https') ? https : http;
  return new Promise((resolve, reject) => {
    const req = mod.get(u, { headers: { Accept: 'application/json' } }, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        if (res.statusCode !== 200) return reject(new Error('SearXNG HTTP ' + res.statusCode + ': ' + body.slice(0, 200)));
        try {
          const j = JSON.parse(body);
          resolve((j.results || []).slice(0, count).map(r => ({ url: r.url, title: r.title, description: r.content })));
        } catch (e) { reject(new Error('SearXNG parse: ' + e.message)); }
      });
    });
    req.on('error', reject);
    req.setTimeout(20000, () => req.destroy(new Error('SearXNG timeout')));
  });
}

module.exports = { searxSearch };
