#!/usr/bin/env node
'use strict';
// full-review-go.js <go-file> — exit 0 only if a standing GO for LIVE full-review
// rounds exists and is valid. Anything else (missing file, bad JSON, live_allowed
// not true, missing/expired "expires", no "granted_by") exits 1 with the reason.
// The GO file is written by a human from Adam's explicit order; no script here
// ever creates it.
//   { "live_allowed": true, "granted_by": "Adam", "granted_at": "2026-..",
//     "expires": "2026-12-31", "max_batch": 20, "source": "<where the GO was given>" }
const fs = require('fs');
function check(file, now = Date.now()) {
  let j;
  try { j = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return { ok: false, reason: `no readable GO file (${e.code || e.message})` }; }
  if (j.live_allowed !== true) return { ok: false, reason: 'live_allowed is not true' };
  if (!j.granted_by || !j.source) return { ok: false, reason: 'GO lacks granted_by/source' };
  const exp = Date.parse(j.expires || '');
  if (!Number.isFinite(exp)) return { ok: false, reason: 'GO has no valid "expires" date' };
  if (now > exp + 86400e3) return { ok: false, reason: `GO expired ${j.expires}` };
  return { ok: true, reason: `standing GO by ${j.granted_by} until ${j.expires}`, max_batch: Number(j.max_batch) || 20 };
}
module.exports = { check };
if (require.main === module) {
  const r = check(process.argv[2] || '');
  console.log(`full-review GO: ${r.ok ? 'VALID' : 'REFUSED'} — ${r.reason}`);
  process.exit(r.ok ? 0 : 1);
}
