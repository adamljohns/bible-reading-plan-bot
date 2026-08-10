/* Auth tests for the prayer-wall Worker.  node workers/prayer-wall/test.mjs
 *
 * These are the claims the lock actually cares about — fail closed, no data
 * without a session, moderator-only actions — so they get exercised rather
 * than asserted. No network and no Cloudflare account needed; KV is a Map.
 */
import worker from './index.js';

let pass = 0, fail = 0;
function ok(name, cond, extra = '') {
  if (cond) { pass++; console.log(`  PASS  ${name}`); }
  else { fail++; console.log(`  FAIL  ${name} ${extra}`); }
}

function makeKV() {
  const m = new Map();
  return {
    _m: m,
    async get(k) { return m.has(k) ? m.get(k) : null; },
    async put(k, v) { m.set(k, v); },
    async delete(k) { m.delete(k); },
    async list({ prefix, limit = 1000 }) {
      return { keys: [...m.keys()].filter(k => k.startsWith(prefix))
        .slice(0, limit).map(name => ({ name })) };
    },
  };
}

const ctx = { waitUntil(p) { return p; } };
const envOK = () => ({ PRAYER: makeKV(), WALL_PIN: 'members-1234',
                       MOD_PIN: 'moder-9876', SESSION_SECRET: 'test-secret-abc' });

const req = (path, { method = 'GET', body, cookie, ip = '1.2.3.4' } = {}) =>
  new Request('https://usmcmin.org' + path, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'CF-Connecting-IP': ip,
      ...(cookie ? { Cookie: cookie } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

const cookieFrom = res => {
  const sc = res.headers.get('Set-Cookie') || '';
  const m = sc.match(/pw_session=([^;]+)/);
  return m ? `pw_session=${m[1]}` : '';
};

console.log('prayer-wall auth');

/* --- 1. unconfigured deploy must refuse everyone, not admit everyone --- */
{
  const env = { PRAYER: makeKV() };   // no secrets set
  const r = await worker.fetch(req('/api/prayer/list'), env, ctx);
  ok('unconfigured -> 503 not_configured', r.status === 503, `got ${r.status}`);
  const r2 = await worker.fetch(
    req('/api/prayer/login', { method: 'POST', body: { pin: 'anything' } }), env, ctx);
  ok('unconfigured -> PIN cannot mint a session', r2.status === 503, `got ${r2.status}`);
}

/* --- 2. no session = no data --- */
{
  const env = envOK();
  const r = await worker.fetch(req('/api/prayer/list'), env, ctx);
  ok('no cookie -> 401 on GET requests', r.status === 401, `got ${r.status}`);
  const body = await r.json();
  ok('401 body carries no request arrays', body.open === undefined && body.answered === undefined);
}

/* --- 3. wrong PIN --- */
{
  const env = envOK();
  const r = await worker.fetch(
    req('/api/prayer/login', { method: 'POST', body: { pin: 'members-1235' } }), env, ctx);
  ok('wrong PIN -> 401', r.status === 401, `got ${r.status}`);
  ok('wrong PIN sets no cookie', !cookieFrom(r));
}

/* --- 4. brute force brake --- */
{
  const env = envOK();
  let last;
  for (let i = 0; i < 12; i++) {
    last = await worker.fetch(
      req('/api/prayer/login', { method: 'POST', body: { pin: 'nope' + i } }), env, ctx);
  }
  ok('11th+ wrong PIN from one IP -> 429 locked', last.status === 429, `got ${last.status}`);
}

/* --- 5. correct PIN -> HttpOnly session, then data --- */
let memberCookie, envShared = envOK();
{
  const r = await worker.fetch(
    req('/api/prayer/login', { method: 'POST', body: { pin: 'members-1234' } }), envShared, ctx);
  ok('correct PIN -> 200', r.status === 200, `got ${r.status}`);
  const sc = r.headers.get('Set-Cookie') || '';
  ok('cookie is HttpOnly', /HttpOnly/.test(sc), sc);
  ok('cookie is Secure', /Secure/.test(sc));
  ok('cookie is SameSite=Strict', /SameSite=Strict/.test(sc));
  ok('PIN is not echoed into the cookie', !sc.includes('members-1234'));
  memberCookie = cookieFrom(r);

  const g = await worker.fetch(req('/api/prayer/list', { cookie: memberCookie }), envShared, ctx);
  ok('with session -> 200 on GET requests', g.status === 200, `got ${g.status}`);
  const gb = await g.json();
  ok('empty wall returns empty lists, not an error',
     Array.isArray(gb.open) && gb.open.length === 0 && Array.isArray(gb.answered));
  ok('member session reports role=member', gb.role === 'member');
}

/* --- 6. forged / tampered cookies --- */
{
  const forged = 'pw_session=moderator.9999999999.deadbeef';
  const r = await worker.fetch(req('/api/prayer/list', { cookie: forged }), envShared, ctx);
  ok('forged signature -> 401', r.status === 401, `got ${r.status}`);

  const [role, exp, sig] = decodeURIComponent(memberCookie.split('=')[1]).split('.');
  const escalated = `pw_session=moderator.${exp}.${sig}`;
  const r2 = await worker.fetch(req('/api/prayer/list', { cookie: escalated }), envShared, ctx);
  ok('role swapped member->moderator on a valid sig -> 401', r2.status === 401, `got ${r2.status}`);

  const expired = `pw_session=${role}.1000000000.${sig}`;
  const r3 = await worker.fetch(req('/api/prayer/list', { cookie: expired }), envShared, ctx);
  ok('expired session -> 401', r3.status === 401, `got ${r3.status}`);
}

/* --- 7. posting, caps, and the Open -> Praying -> Answered lifecycle --- */
let postedId;
{
  const r = await worker.fetch(req('/api/prayer/add', {
    method: 'POST', cookie: memberCookie,
    body: { name: 'AJ', tag: 'Family', text: 'Wisdom for a hard conversation this week.' },
  }), envShared, ctx);
  ok('member can post -> 201', r.status === 201, `got ${r.status}`);
  const b = await r.json();
  postedId = b.request.id;
  ok('new request starts status=open', b.request.status === 'open');

  const long = await worker.fetch(req('/api/prayer/add', {
    method: 'POST', cookie: memberCookie,
    body: { name: 'x'.repeat(200), tag: 'Nonsense', text: 'y'.repeat(9000) },
  }), envShared, ctx);
  const lb = await long.json();
  ok('text capped at 500', lb.request.text.length === 500, `len ${lb.request.text.length}`);
  ok('name capped at 40', lb.request.name.length === 40);
  ok('unknown tag falls back to Other', lb.request.tag === 'Other', lb.request.tag);

  const empty = await worker.fetch(req('/api/prayer/add', {
    method: 'POST', cookie: memberCookie, body: { text: '  ' },
  }), envShared, ctx);
  ok('empty request rejected -> 400', empty.status === 400, `got ${empty.status}`);
}

/* --- 8. member must NOT be able to moderate or export --- */
{
  const s = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: memberCookie, body: { id: postedId, action: 'answered', praise: 'nope' },
  }), envShared, ctx);
  ok('member marking answered -> 403', s.status === 403, `got ${s.status}`);

  const d = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: memberCookie, body: { id: postedId, action: 'delete' } }), envShared, ctx);
  ok('member deleting -> 403', d.status === 403, `got ${d.status}`);

  const e = await worker.fetch(req('/api/prayer/export.json', { cookie: memberCookie }), envShared, ctx);
  ok('member exporting -> 403', e.status === 403, `got ${e.status}`);
}

/* --- 9. moderator can --- */
{
  const m = await worker.fetch(
    req('/api/prayer/login', { method: 'POST', body: { pin: 'moder-9876' }, ip: '5.6.7.8' }),
    envShared, ctx);
  ok('moderator PIN -> 200', m.status === 200, `got ${m.status}`);
  const modCookie = cookieFrom(m);

  const s = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: modCookie, body: { id: postedId, action: 'praying' },
  }), envShared, ctx);
  ok('moderator can mark praying', s.status === 200, `got ${s.status}`);

  const a = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: modCookie, body: { id: postedId, action: 'answered', praise: 'He gave the words.' },
  }), envShared, ctx);
  const ab = await a.json();
  ok('moderator can mark answered with praise',
     ab.request.status === 'answered' && ab.request.praise === 'He gave the words.');
  ok('answered stamps answeredAt', Boolean(ab.request.answeredAt));

  const bad = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: modCookie, body: { id: postedId, action: 'deleted-by-me' },
  }), envShared, ctx);
  ok('invalid action rejected -> 400', bad.status === 400, `got ${bad.status}`);

  // Reopening must clear the answered stamp, or the card keeps reading as done.
  const re = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: modCookie, body: { id: postedId, action: 'open' },
  }), envShared, ctx);
  const rb = await re.json();
  ok('reopen clears answeredAt',
     rb.request.status === 'open' && rb.request.answeredAt === undefined);

  const e = await worker.fetch(req('/api/prayer/export.json', { cookie: modCookie }), envShared, ctx);
  ok('moderator export -> 200', e.status === 200, `got ${e.status}`);
  ok('export is a file download',
     /attachment; filename="prayer-wall-/.test(e.headers.get('Content-Disposition') || ''));

  const del = await worker.fetch(req('/api/prayer/update', {
    method: 'POST', cookie: modCookie, body: { id: postedId, action: 'delete' } }), envShared, ctx);
  ok('moderator can delete', del.status === 200, `got ${del.status}`);
}

/* --- 10. submit rate limit --- */
{
  const env = envOK();
  const s = await worker.fetch(
    req('/api/prayer/login', { method: 'POST', body: { pin: 'members-1234' } }), env, ctx);
  const c = cookieFrom(s);
  let last;
  for (let i = 0; i < 8; i++) {
    last = await worker.fetch(req('/api/prayer/add', {
      method: 'POST', cookie: c, body: { text: 'request number ' + i } }), env, ctx);
  }
  ok('7th+ submit in an hour -> 429', last.status === 429, `got ${last.status}`);
}

/* --- 11. sign out clears the cookie --- */
{
  const r = await worker.fetch(req('/api/prayer/logout', { method: 'POST', cookie: memberCookie }),
                               envShared, ctx);
  ok('sign out -> Max-Age=0', /Max-Age=0/.test(r.headers.get('Set-Cookie') || ''));
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
