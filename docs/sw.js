// U.S.M.C. Ministries — Service Worker v10
// App-shell precache + network-first runtime caching (installable, offline-capable).
// Scope "/" controls the whole site, including /dictionary/* once registered from any page.
// v9 (2026-06-11): cache bump to flush any stale tacc.html after the double-PIN-gate fix.
// v10 (2026-06-25): precache the Baptist Catechism + its assets; flush stale LBCF
//   renderer/JSON after the single-chapter proof-text fix.
const CACHE = 'usmc-v10';

// Core "app shell": the public ministry pages + key assets. Small + high-value.
// Big data (Bible JSON, dictionary entries) caches on first visit via network-first below.
const SHELL = [
  '/', '/index.html', '/manifest.json', '/offline.html',
  '/bible.html', '/bible-plan.html', '/proverbs.html', '/mbt.html',
  '/dictionary/', '/dictionary/index.html',
  '/lexicon.html', '/cross-references.html', '/watchman.html',
  '/institutes.html', '/lbcf.html', '/lbcf-full.html', '/catechism.html', '/blog.html', '/connect.html', '/about.html',
  // LBCF shared assets (chapter shells/JSON cache on first visit via network-first).
  // The ?v= must match the query string the pages request with, or the precache never hits.
  '/assets/js/lbcf-render.js?v=20260613', '/assets/css/lbcf.css', '/assets/lbcf/index.json',
  '/assets/js/scripture-preview.js', // inline verse-preview popovers (LBCF + catechism)
  // Catechism assets (the page itself is baked; these are its styles/data/progress tracker).
  '/assets/css/catechism.css', '/assets/catechism/catechism.json',
  '/assets/js/study-progress.js', '/assets/css/study-progress.css',
  '/crew-quarters.html', // preserve existing Crew Chores PWA offline support
  '/assets/icons/favicon.svg', '/assets/icons/icon-192.png',
  '/assets/icons/icon-512.png', '/assets/icons/apple-touch-icon.png'
];

self.addEventListener('install', e => {
  // Cache each item independently so one 404 can't abort the whole precache.
  e.waitUntil(
    caches.open(CACHE).then(c => Promise.all(SHELL.map(u => c.add(u).catch(() => {}))))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return; // leave cross-origin requests alone

  // Network-first: fresh when online, cached fallback when offline.
  e.respondWith(
    fetch(e.request)
      .then(res => {
        if (res && res.ok && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() =>
        caches.match(e.request).then(hit =>
          hit || (e.request.mode === 'navigate' ? caches.match('/offline.html') : Response.error())
        )
      )
  );
});
