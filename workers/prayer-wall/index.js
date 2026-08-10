/* prayer-wall — gated Men's Prayer Wall API for usmcmin.org
 * CID PJG-0809-PRAYWALL1 (built under PJG-0809-MEISTER1)
 *
 * Standalone Worker on route usmcmin.org/api/prayer* — deliberately separate
 * from the static-site Worker so it can never break page serving, same posture
 * as workers/amen-counter.
 *
 * WHY A WORKER AT ALL: docs/ deploys to R2 as flat public files. Anything a
 * static page can read, the whole internet can read. The lock says requests
 * must never sit in plain public R2 without a gate, so the request bodies live
 * only in KV behind this Worker and reach the browser only after a valid
 * session. docs/prayer/wall.html ships with ZERO request data in it.
 *
 * SECRETS — none are in this repo. Set them once, out of band:
 *   wrangler secret put WALL_PIN         # Adam chooses; never pasted in chat/git
 *   wrangler secret put SESSION_SECRET   # any long random string
 *   wrangler secret put MOD_PIN          # moderator (Adam); enables mark/delete/export
 *
 * API
 *   POST /api/prayer/session   {pin}                -> sets HttpOnly cookie
 *   DELETE /api/prayer/session                      -> sign out
 *   GET  /api/prayer/requests                       -> {requests:[...]}      (auth)
 *   POST /api/prayer/requests  {name,text,tag}      -> {ok,id}               (auth)
 *   POST /api/prayer/requests/:id/status {status,praise}                     (moderator)
 *   DELETE /api/prayer/requests/:id                                          (moderator)
 *   GET  /api/prayer/export                         -> JSON download         (moderator)
 *
 * Storage (KV binding PRAYER):
 *   r:<groupId>:<ts>-<rand>  -> request JSON
 *   rl:<sha256(ip|window)>   -> submit rate-limit counter, TTL 1h
 *   fa:<sha256(ip)>          -> failed-PIN counter, TTL 15m (brute-force brake)
 */

const GROUP_ID = 'mens-prayer';
const SESSION_TTL = 60 * 60 * 12;          // 12h — a session, not a permanent key
const MAX_TEXT = 500;                       // lock: ~280-500 char cap
const MAX_NAME = 40;
const SUBMITS_PER_HOUR = 6;
const MAX_PIN_FAILS = 10;                   // per IP per 15 min
const TAGS = ['Family', 'Work', 'Health', 'Church', 'Other'];
const STATUSES = ['open', 'praying', 'answered'];

const JSON_HEADERS = {
  'Content-Type': 'application/json',
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
};

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), { status, headers: { ...JSON_HEADERS, ...extra } });
}

const enc = new TextEncoder();

async function sha256Hex(s) {
  const h = await crypto.subtle.digest('SHA-256', enc.encode(s));
  return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join('');
}

/* Constant-time compare so a wrong PIN can't be discovered a character at a
 * time by timing the response. */
function timingSafeEqual(a, b) {
  const ab = enc.encode(String(a));
  const bb = enc.encode(String(b));
  if (ab.length !== bb.length) return false;
  let diff = 0;
  for (let i = 0; i < ab.length; i++) diff |= ab[i] ^ bb[i];
  return diff === 0;
}

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(msg));
  return btoa(String.fromCharCode(...new Uint8Array(sig)))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

/* Session token = "<role>.<expiry>.<hmac>". Signed, not encrypted — it carries
 * no secret, only a claim this Worker can verify. */
async function mintSession(env, role) {
  const exp = Math.floor(Date.now() / 1000) + SESSION_TTL;
  const body = `${role}.${exp}`;
  return `${body}.${await hmac(env.SESSION_SECRET, body)}`;
}

async function readSession(env, request) {
  const cookie = request.headers.get('Cookie') || '';
  const m = cookie.match(/(?:^|;\s*)pw_session=([^;]+)/);
  if (!m) return null;
  const parts = decodeURIComponent(m[1]).split('.');
  if (parts.length !== 3) return null;
  const [role, exp, sig] = parts;
  if (!['member', 'moderator'].includes(role)) return null;
  if (!/^\d+$/.test(exp) || Number(exp) < Math.floor(Date.now() / 1000)) return null;
  const expected = await hmac(env.SESSION_SECRET, `${role}.${exp}`);
  if (!timingSafeEqual(sig, expected)) return null;
  return { role };
}

function sessionCookie(token, maxAge) {
  return `pw_session=${encodeURIComponent(token)}; Path=/; Max-Age=${maxAge}; ` +
         'HttpOnly; Secure; SameSite=Strict';
}

function clean(s, max) {
  return String(s == null ? '' : s)
    .replace(/[\u0000-\u001F\u007F]/g, ' ')   // strip control characters
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, max);
}

/* Configuration is checked before anything else. A Worker deployed without its
 * secrets must refuse, not silently authenticate everyone. */
function configured(env) {
  return Boolean(env.PRAYER && env.WALL_PIN && env.SESSION_SECRET);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const p = url.pathname;
    const ip = request.headers.get('CF-Connecting-IP') || '0.0.0.0';

    if (!p.startsWith('/api/prayer')) return json({ error: 'not found' }, 404);

    if (!configured(env)) {
      return json({ error: 'not_configured',
                    message: 'The prayer wall is not wired up yet.' }, 503);
    }

    /* ---------- POST /api/prayer/session : exchange PIN for a session ---------- */
    if (p === '/api/prayer/session' && request.method === 'POST') {
      const failKey = 'fa:' + await sha256Hex(ip);
      const fails = parseInt(await env.PRAYER.get(failKey), 10) || 0;
      if (fails >= MAX_PIN_FAILS) {
        return json({ error: 'locked', message: 'Too many attempts. Try again later.' }, 429);
      }

      let body;
      try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }
      const pin = String(body.pin || '');

      const isMod = env.MOD_PIN && timingSafeEqual(pin, env.MOD_PIN);
      const isMember = timingSafeEqual(pin, env.WALL_PIN);

      if (!isMod && !isMember) {
        // Count the failure, and say nothing about which part was wrong.
        ctx.waitUntil(env.PRAYER.put(failKey, String(fails + 1), { expirationTtl: 900 }));
        return json({ error: 'denied' }, 401);
      }

      const role = isMod ? 'moderator' : 'member';
      const token = await mintSession(env, role);
      return json({ ok: true, role },
                  200, { 'Set-Cookie': sessionCookie(token, SESSION_TTL) });
    }

    /* ---------- DELETE /api/prayer/session ---------- */
    if (p === '/api/prayer/session' && request.method === 'DELETE') {
      return json({ ok: true }, 200, { 'Set-Cookie': sessionCookie('', 0) });
    }

    /* ---------- everything below requires a valid session ---------- */
    const session = await readSession(env, request);
    if (!session) return json({ error: 'unauthorized' }, 401);

    const needsMod = () => session.role === 'moderator';

    /* ---------- GET /api/prayer/requests ---------- */
    if (p === '/api/prayer/requests' && request.method === 'GET') {
      const list = await env.PRAYER.list({ prefix: `r:${GROUP_ID}:`, limit: 1000 });
      const rows = await Promise.all(list.keys.map(async k => {
        try { return JSON.parse(await env.PRAYER.get(k.name)); } catch { return null; }
      }));
      const requests = rows.filter(Boolean)
        .sort((a, b) => (b.created_at || '').localeCompare(a.created_at || ''));
      return json({ requests, role: session.role });
    }

    /* ---------- POST /api/prayer/requests ---------- */
    if (p === '/api/prayer/requests' && request.method === 'POST') {
      const window = Math.floor(Date.now() / 3600000);
      const rlKey = 'rl:' + await sha256Hex(`${ip}|${window}`);
      const used = parseInt(await env.PRAYER.get(rlKey), 10) || 0;
      if (used >= SUBMITS_PER_HOUR) {
        return json({ error: 'rate_limited',
                      message: 'That is a lot of requests in one hour. Try again shortly.' }, 429);
      }

      let body;
      try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }

      const text = clean(body.text, MAX_TEXT);
      const name = clean(body.name, MAX_NAME) || 'A brother';
      const tag = TAGS.includes(body.tag) ? body.tag : 'Other';
      if (text.length < 3) return json({ error: 'empty', message: 'Add a short request.' }, 400);

      const id = `${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;
      const rec = {
        id, group_id: GROUP_ID, name, text, tag,
        status: 'open', praise: '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      await env.PRAYER.put(`r:${GROUP_ID}:${id}`, JSON.stringify(rec));
      ctx.waitUntil(env.PRAYER.put(rlKey, String(used + 1), { expirationTtl: 3600 }));
      return json({ ok: true, request: rec }, 201);
    }

    /* ---------- POST /api/prayer/requests/:id/status  (moderator) ---------- */
    let m = p.match(/^\/api\/prayer\/requests\/([A-Za-z0-9-]+)\/status$/);
    if (m && request.method === 'POST') {
      if (!needsMod()) return json({ error: 'forbidden' }, 403);
      let body;
      try { body = await request.json(); } catch { return json({ error: 'bad json' }, 400); }
      const status = STATUSES.includes(body.status) ? body.status : null;
      if (!status) return json({ error: 'bad status' }, 400);

      const key = `r:${GROUP_ID}:${m[1]}`;
      const raw = await env.PRAYER.get(key);
      if (!raw) return json({ error: 'not found' }, 404);
      const rec = JSON.parse(raw);
      rec.status = status;
      if (status === 'answered') {
        rec.praise = clean(body.praise, MAX_TEXT);
        rec.answered_at = new Date().toISOString();
      }
      rec.updated_at = new Date().toISOString();
      await env.PRAYER.put(key, JSON.stringify(rec));
      return json({ ok: true, request: rec });
    }

    /* ---------- DELETE /api/prayer/requests/:id  (moderator) ---------- */
    m = p.match(/^\/api\/prayer\/requests\/([A-Za-z0-9-]+)$/);
    if (m && request.method === 'DELETE') {
      if (!needsMod()) return json({ error: 'forbidden' }, 403);
      await env.PRAYER.delete(`r:${GROUP_ID}:${m[1]}`);
      return json({ ok: true });
    }

    /* ---------- GET /api/prayer/export  (moderator) ---------- */
    if (p === '/api/prayer/export' && request.method === 'GET') {
      if (!needsMod()) return json({ error: 'forbidden' }, 403);
      const list = await env.PRAYER.list({ prefix: `r:${GROUP_ID}:`, limit: 1000 });
      const rows = await Promise.all(list.keys.map(async k => {
        try { return JSON.parse(await env.PRAYER.get(k.name)); } catch { return null; }
      }));
      const stamp = new Date().toISOString().slice(0, 10);
      return json({ exported_at: new Date().toISOString(), group_id: GROUP_ID,
                    requests: rows.filter(Boolean) },
                  200, { 'Content-Disposition':
                         `attachment; filename="prayer-wall-${stamp}.json"` });
    }

    return json({ error: 'not found' }, 404);
  },
};
