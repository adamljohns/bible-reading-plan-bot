// U.S.M.C. Ministries — Service Worker v4
// Network-first for everything, cache as backup only
// Updated to support Crew Chores PWA
const CACHE_NAME = 'usmc-v4';
const PRECACHE = [
  '/crew-quarters.html',
  '/manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Skip non-GET requests
  if (e.request.method !== 'GET') return;
  
  // Network-first for everything
  e.respondWith(
    fetch(e.request)
      .then(response => {
        // Cache successful responses for offline fallback
        if (response.ok && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
