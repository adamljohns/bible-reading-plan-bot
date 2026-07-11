/* amen-counter — global Amen counts for usmcmin.org (MOOP interactive toolkit)
 *
 * Standalone Worker on route usmcmin.org/api/amen* — deliberately separate from
 * the static-site Worker so it can never break page serving.
 *
 * API (consumed by docs/assets/js/moop-tools.js, already deployed site-wide):
 *   GET  /api/amen?slug=dictionary:grace      -> {slug, count}
 *   POST /api/amen  {"slug":"dictionary:grace"} -> {slug, count, counted}
 *   GET  /api/amen/top?limit=20               -> {top:[{slug,count},...]} (cached 5 min)
 *
 * Storage: KV binding AMEN.
 *   c:<slug>                    -> count (stringified int)
 *   d:<sha256(ip|slug|utcday)>  -> "1" TTL 86400  (per-IP per-day dedupe; the
 *                                  client's localStorage already stops casual repeats)
 * KV read-modify-write is not atomic; at ministry traffic the occasional lost
 * increment is acceptable. Move to Durable Objects only if counts ever matter
 * to the cent.
 */
const SLUG_RE = /^[a-z0-9:._-]{1,80}$/;

const JSON_HEADERS = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Cache-Control': 'no-store',
};

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), { status, headers: { ...JSON_HEADERS, ...extra } });
}

async function dedupeKey(ip, slug) {
  const day = new Date().toISOString().slice(0, 10);
  const data = new TextEncoder().encode(`${ip}|${slug}|${day}`);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return 'd:' + [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2, '0')).join('');
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: JSON_HEADERS });

    /* ---- GET /api/amen/top ---- */
    if (request.method === 'GET' && url.pathname === '/api/amen/top') {
      const cache = caches.default;
      const cacheKey = new Request(url.origin + '/api/amen/top');
      const hit = await cache.match(cacheKey);
      if (hit) return hit;
      const limit = Math.min(parseInt(url.searchParams.get('limit') || '20', 10) || 20, 100);
      const list = await env.AMEN.list({ prefix: 'c:', limit: 1000 });
      const rows = await Promise.all(list.keys.map(async k => ({
        slug: k.name.slice(2),
        count: parseInt(await env.AMEN.get(k.name), 10) || 0,
      })));
      rows.sort((a, b) => b.count - a.count);
      const res = json({ top: rows.slice(0, limit), asOf: new Date().toISOString() },
                       200, { 'Cache-Control': 'public, max-age=300' });
      ctx.waitUntil(cache.put(cacheKey, res.clone()));
      return res;
    }

    /* ---- GET /api/amen?slug= ---- */
    if (request.method === 'GET' && url.pathname === '/api/amen') {
      const slug = (url.searchParams.get('slug') || '').toLowerCase();
      if (!SLUG_RE.test(slug)) return json({ error: 'bad slug' }, 400);
      const count = parseInt(await env.AMEN.get('c:' + slug), 10) || 0;
      return json({ slug, count });
    }

    /* ---- POST /api/amen ---- */
    if (request.method === 'POST' && url.pathname === '/api/amen') {
      let body;
      try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }
      const slug = String(body.slug || '').toLowerCase();
      if (!SLUG_RE.test(slug)) return json({ error: 'bad slug' }, 400);

      const ip = request.headers.get('CF-Connecting-IP') || '0.0.0.0';
      const dkey = await dedupeKey(ip, slug);
      const key = 'c:' + slug;
      let count = parseInt(await env.AMEN.get(key), 10) || 0;

      if (await env.AMEN.get(dkey)) {
        return json({ slug, count, counted: false });
      }
      count += 1;
      await env.AMEN.put(key, String(count));
      ctx.waitUntil(env.AMEN.put(dkey, '1', { expirationTtl: 86400 }));
      return json({ slug, count, counted: true });
    }

    return json({ error: 'not found' }, 404);
  },
};
