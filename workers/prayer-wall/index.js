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
 * API (contract set by docs/prayer/wall.html, which Max shipped UI-first)
 *   GET  /api/prayer/session      -> {success} — does this browser hold one?
 *   POST /api/prayer/login  {pin} -> {success} + HttpOnly session cookie
 *   POST /api/prayer/logout       -> {success} + cleared cookie
 *   GET  /api/prayer/list         -> {success, open[], answered[], role}   (auth)
 *   POST /api/prayer/add    {name,text,tag}                                 (auth)
 *   POST /api/prayer/update {id,action,praise}  action: praying|answered|open|delete
 *                                                                     (moderator)
 *   GET  /api/prayer/export.json  -> JSON download                    (moderator)
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

/* The wall UI (docs/prayer/wall.html) branches on `success` and renders
 * `error` straight to the operator, so every response carries both. */
const ok = (obj = {}, status = 200, extra = {}) =>
  json({ success: true, ...obj }, status, extra);
const fail = (error, status) => json({ success: false, error }, status);

async function readAll(env) {
  const list = await env.PRAYER.list({ prefix: `r:${GROUP_ID}:`, limit: 1000 });
  const rows = await Promise.all(list.keys.map(async k => {
    try { return JSON.parse(await env.PRAYER.get(k.name)); } catch { return null; }
  }));
  return rows.filter(Boolean)
    .sort((a, b) => String(b.createdAt || '').localeCompare(String(a.createdAt || '')));
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
    const p = url.pathname.replace(/^\/api\/prayer\/?/, '');
    const ip = request.headers.get('CF-Connecting-IP') || '0.0.0.0';
    const method = request.method;

    if (!url.pathname.startsWith('/api/prayer')) return fail('Not found', 404);

    if (!configured(env)) {
      return fail('The prayer wall is not wired up yet — the group PIN has not been set.', 503);
    }

    /* ---------- GET session : does this browser already hold one? ---------- */
    if (p === 'session' && method === 'GET') {
      const s = await readSession(env, request);
      return s ? ok({ role: s.role }) : fail('Locked', 401);
    }

    /* ---------- POST login ---------- */
    if (p === 'login' && method === 'POST') {
      const failKey = 'fa:' + await sha256Hex(ip);
      const fails = parseInt(await env.PRAYER.get(failKey), 10) || 0;
      if (fails >= MAX_PIN_FAILS) {
        return fail('Too many attempts from here. Give it a few minutes.', 429);
      }

      let body;
      try { body = await request.json(); } catch { return fail('Bad request', 400); }
      const pin = String(body.pin || '');

      const isMod = Boolean(env.MOD_PIN) && timingSafeEqual(pin, env.MOD_PIN);
      const isMember = timingSafeEqual(pin, env.WALL_PIN);

      if (!isMod && !isMember) {
        // Count it, and say nothing about which PIN was close.
        ctx.waitUntil(env.PRAYER.put(failKey, String(fails + 1), { expirationTtl: 900 }));
        return fail('Incorrect PIN.', 401);
      }

      const role = isMod ? 'moderator' : 'member';
      const token = await mintSession(env, role);
      return ok({ role }, 200, { 'Set-Cookie': sessionCookie(token, SESSION_TTL) });
    }

    /* ---------- POST logout ---------- */
    if (p === 'logout' && method === 'POST') {
      return ok({}, 200, { 'Set-Cookie': sessionCookie('', 0) });
    }

    /* ---------- everything below needs a valid session ---------- */
    const session = await readSession(env, request);
    if (!session) return fail('Locked', 401);
    const isMod = session.role === 'moderator';

    /* ---------- GET list ---------- */
    if (p === 'list' && method === 'GET') {
      const all = await readAll(env);
      return ok({
        open: all.filter(r => r.status !== 'answered'),
        answered: all.filter(r => r.status === 'answered'),
        role: session.role,
      });
    }

    /* ---------- POST add ---------- */
    if (p === 'add' && method === 'POST') {
      const window = Math.floor(Date.now() / 3600000);
      const rlKey = 'rl:' + await sha256Hex(`${ip}|${window}`);
      const used = parseInt(await env.PRAYER.get(rlKey), 10) || 0;
      if (used >= SUBMITS_PER_HOUR) {
        return fail('That is a lot of requests in one hour. Try again shortly.', 429);
      }

      let body;
      try { body = await request.json(); } catch { return fail('Bad request', 400); }

      const text = clean(body.text, MAX_TEXT);
      if (text.length < 3) return fail('Add a short request first.', 400);

      const rec = {
        id: `${Date.now()}-${crypto.randomUUID().slice(0, 8)}`,
        groupId: GROUP_ID,
        name: clean(body.name, MAX_NAME) || 'A brother',
        text,
        tag: TAGS.includes(body.tag) ? body.tag : 'Other',
        status: 'open',
        praise: '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      await env.PRAYER.put(`r:${GROUP_ID}:${rec.id}`, JSON.stringify(rec));
      ctx.waitUntil(env.PRAYER.put(rlKey, String(used + 1), { expirationTtl: 3600 }));
      return ok({ request: rec }, 201);
    }

    /* ---------- POST update  {id, action, praise} ---------- */
    if (p === 'update' && method === 'POST') {
      // Marking and removing another man's request is Adam's lane, not the
      // group's. The wall UI shows these buttons to everyone, so a member who
      // presses one gets this sentence back rather than a silent success.
      if (!isMod) return fail('Only a moderator can change requests on the wall.', 403);

      let body;
      try { body = await request.json(); } catch { return fail('Bad request', 400); }
      const id = String(body.id || '');
      if (!/^[A-Za-z0-9-]{1,64}$/.test(id)) return fail('Bad request', 400);
      const action = String(body.action || '');
      const key = `r:${GROUP_ID}:${id}`;

      if (action === 'delete') {
        await env.PRAYER.delete(key);
        return ok({ deleted: id });
      }
      if (!STATUSES.includes(action)) return fail('Unknown action.', 400);

      const raw = await env.PRAYER.get(key);
      if (!raw) return fail('That request is no longer on the wall.', 404);
      const rec = JSON.parse(raw);
      rec.status = action;
      if (action === 'answered') {
        rec.praise = clean(body.praise, MAX_TEXT);
        rec.answeredAt = new Date().toISOString();
      } else {
        // Reopening clears the answered stamp so the card stops reading as done.
        delete rec.answeredAt;
      }
      rec.updatedAt = new Date().toISOString();
      await env.PRAYER.put(key, JSON.stringify(rec));
      return ok({ request: rec });
    }

    /* ---------- GET export.json ---------- */
    if (p === 'export.json' && method === 'GET') {
      if (!isMod) return fail('Only a moderator can export the wall.', 403);
      const all = await readAll(env);
      const stamp = new Date().toISOString().slice(0, 10);
      return ok({ exportedAt: new Date().toISOString(), groupId: GROUP_ID, requests: all },
                200, { 'Content-Disposition': `attachment; filename="prayer-wall-${stamp}.json"` });
    }

    return fail('Not found', 404);
  },
};
