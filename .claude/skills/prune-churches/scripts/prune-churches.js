#!/usr/bin/env node
/* prune-churches.js — remove church record(s) from churches.json by id (the source of truth).
 * Format-preserving: Node JSON.stringify(d,null,2)+'\n' (verified byte-identical round-trip;
 * Python does NOT reproduce this file — float formatting differs — so churches.json MUST be
 * edited with Node). Atomic temp+rename. Round-trip guarded. Re-syncs total_churches.
 * Usage: node prune-churches.js [--dry-run] <id> [<id> ...]
 * Does NOT touch shards/sitemap/HTML (see prune-derived.py / prune.sh) and does NOT commit. */
const fs = require('fs');
const path = require('path');

function findRoot(start) {
  let d = start;
  for (let i = 0; i < 12; i++) {
    if (fs.existsSync(path.join(d, 'docs/data/churches.json'))) return d;
    const up = path.dirname(d);
    if (up === d) break;
    d = up;
  }
  throw new Error('could not locate repo root (docs/data/churches.json) above ' + start);
}

const argv = process.argv.slice(2);
const dry = argv.includes('--dry-run');
const ids = new Set(argv.filter(a => a !== '--dry-run').map(String));
if (ids.size === 0) { console.error('usage: node prune-churches.js [--dry-run] <id> [<id> ...]'); process.exit(2); }

const ROOT = findRoot(__dirname);
const p = path.join(ROOT, 'docs/data/churches.json');
const orig = fs.readFileSync(p);
const d = JSON.parse(orig);

// churches.json has been written by both Node (JSON.stringify -> literal Unicode, trailing
// newline) and Python (json.dump ensure_ascii=True -> \uXXXX escapes, no trailing newline)
// tools over its life, so the on-disk format is not fixed. Find the serialization that
// reproduces THIS file and reuse it, so a removal preserves the exact byte format (no whole-file
// reformat, no em-dash re-encode that would explode the diff to ~50k cosmetic lines).
const asciiEscape = s => s.replace(/[-￿]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
function serializerFor(origBuf, obj) {
  const body = JSON.stringify(obj, null, 2);
  for (const esc of [false, true]) {
    for (const nl of ['\n', '']) {
      const cand = (esc ? asciiEscape(body) : body) + nl;
      if (origBuf.equals(Buffer.from(cand))) {
        return o => (esc ? asciiEscape(JSON.stringify(o, null, 2)) : JSON.stringify(o, null, 2)) + nl;
      }
    }
  }
  return null;
}

// Round-trip guard: confirm SOME known serialization reproduces the file byte-for-byte BEFORE
// editing. Self-adapts to escaped/literal Unicode and trailing-newline-or-not.
const serialize = serializerFor(orig, d);
if (!serialize) {
  console.error('ABORT: no known serialization reproduces churches.json byte-for-byte.');
  console.error('       The file may have been written by a different tool — resolve formatting first.');
  process.exit(1);
}

const present = d.churches.filter(c => ids.has(String(c.id))).map(c => String(c.id));
const missing = [...ids].filter(id => !present.includes(id));
console.log('churches.json: ' + d.churches.length + ' records; matched ' + present.length + '/' + ids.size +
  (present.length ? ' [' + present.join(', ') + ']' : '') + (missing.length ? '; NOT FOUND: ' + missing.join(', ') : ''));
if (present.length === 0) { console.log('  nothing to remove'); process.exit(0); }

if (dry) {
  console.log('  [dry-run] would remove ' + present.length + '; total_churches ' + d.total_churches + ' -> ' + (d.churches.length - present.length));
  process.exit(0);
}

const before = d.churches.length;
d.churches = d.churches.filter(c => !ids.has(String(c.id)));
const oldTotal = d.total_churches;
d.total_churches = d.churches.length;            // schema invariant: total_churches == churches.length
const tmp = p + '.tmp' + process.pid;
fs.writeFileSync(tmp, serialize(d));
fs.renameSync(tmp, p);

const v = JSON.parse(fs.readFileSync(p, 'utf8'));
const still = v.churches.filter(c => ids.has(String(c.id))).map(c => String(c.id));
console.log('  removed ' + (before - v.churches.length) + '; total_churches ' + oldTotal + ' -> ' + v.total_churches +
  '; remaining matches: ' + (still.length ? still.join(', ') : 'NONE'));
if (still.length) process.exit(1);
console.log('  TOUCHED: docs/data/churches.json');
