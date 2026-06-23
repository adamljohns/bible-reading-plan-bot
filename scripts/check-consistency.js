#!/usr/bin/env node
// Audit churches.json against every derived artifact the live site reads, so a
// data change that didn't propagate — the classic "fixed one place, forgot the
// others" — gets caught immediately instead of discovered months later.
//
// Checks: total_churches count, churches-index.json (slim search index),
// per-state shards, per-denomination-family shards, sitemap-churches.xml,
// directory-map-points.json, per-church HTML pages (missing + orphan), and
// duplicate ids.
//
// Usage:
//   node scripts/check-consistency.js            # summary; exit 1 if any HARD drift
//   node scripts/check-consistency.js --verbose  # also list drifting ids (capped)
//
// Exit 0 = in sync, 1 = hard drift (so it can gate a pre-push hook or CI). The
// map-points check is advisory (⚠, never fails the run): the map legitimately
// excludes a few geocoded records (territories, dedup-suffixed stubs).

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');
const DATA = path.join(DOCS, 'data');
const VERBOSE = process.argv.includes('--verbose');
const CAP = 15; // max ids printed per drift in --verbose

const results = [];
const record = (name, ok, detail, ids = [], optional = false) =>
  results.push({ name, ok, detail, ids, optional });
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
// Shards may be a bare array or { churches: [...] }; ids may be `id` or `s` (slug).
const shardIds = (a) => (Array.isArray(a) ? a : (a && a.churches) || [])
  .map((c) => c && (c.id || c.s)).filter(Boolean);

function shardUnion(dirName) {
  const dir = path.join(DATA, 'churches', dirName);
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json') && f !== '_index.json');
  const set = new Set();
  for (const f of files) shardIds(readJSON(path.join(dir, f))).forEach((id) => set.add(id));
  return { files: files.length, set };
}

const d = readJSON(path.join(DATA, 'churches.json'));
const churches = d.churches.filter((c) => c && c.id);
const ids = new Set(churches.map((c) => c.id));
const N = churches.length;
const diff = (have, want) => [...want].filter((id) => !have.has(id)); // in want, not in have

// 1. total_churches field (the live footer reads this first)
record('total_churches field', d.total_churches === N, `field=${d.total_churches} vs length=${N}`);

// 2. churches-index.json (the slim index the directory page actually loads)
try {
  const idx = readJSON(path.join(DATA, 'churches-index.json'));
  const idxIds = new Set((Array.isArray(idx) ? idx : idx.churches || []).map((c) => c.id).filter(Boolean));
  const missing = diff(idxIds, ids), orphan = diff(ids, idxIds);
  record('churches-index.json', !missing.length && !orphan.length,
    `${idxIds.size} indexed | missing ${missing.length}, orphan ${orphan.length}`,
    [...missing, ...orphan.map((x) => 'orphan:' + x)]);
} catch (e) { record('churches-index.json', false, 'ERROR ' + e.message); }

// 3. per-state shards
try {
  const { files, set } = shardUnion('by-state');
  const missing = diff(set, ids), orphan = diff(ids, set);
  record('by-state shards', !missing.length && !orphan.length,
    `${files} files, ${set.size} ids | missing ${missing.length}, orphan ${orphan.length}`,
    [...missing, ...orphan.map((x) => 'orphan:' + x)]);
} catch (e) { record('by-state shards', false, 'ERROR ' + e.message); }

// 4. per-denomination-family shards
try {
  const { files, set } = shardUnion('by-denomination-family');
  const missing = diff(set, ids), orphan = diff(ids, set);
  record('by-denomination shards', !missing.length && !orphan.length,
    `${files} files, ${set.size} ids | missing ${missing.length}, orphan ${orphan.length}`,
    [...missing, ...orphan.map((x) => 'orphan:' + x)]);
} catch (e) { record('by-denomination shards', false, 'ERROR ' + e.message); }

// 5. sitemap-churches.xml — exact-string membership (handles ids with spaces/accents)
try {
  const xml = fs.readFileSync(path.join(DOCS, 'sitemap-churches.xml'), 'utf8');
  const missing = churches.filter((c) => !xml.includes(`/churches/${c.id}.html<`)).map((c) => c.id);
  const locs = (xml.match(/<loc>/g) || []).length;
  record('sitemap-churches.xml', !missing.length, `${locs} <loc> | missing ${missing.length}`, missing);
} catch (e) { record('sitemap-churches.xml', false, 'ERROR ' + e.message); }

// 6. directory-map-points.json — every GEOCODED church should have a pin (advisory)
try {
  const pts = readJSON(path.join(DATA, 'directory-map-points.json'));
  const arr = Array.isArray(pts) ? pts : pts.points || pts.features || [];
  const ptIds = new Set(arr.map((p) => p.id || p.s || (p.properties && p.properties.id)).filter(Boolean));
  const geocoded = churches.filter((c) => c.latitude != null && c.longitude != null);
  const missing = geocoded.filter((c) => !ptIds.has(c.id)).map((c) => c.id);
  record('directory-map-points.json', !missing.length,
    `${ptIds.size} pins vs ${geocoded.length} geocoded | missing ${missing.length}`, missing, true);
} catch (e) { record('directory-map-points.json', false, 'ERROR ' + e.message, [], true); }

// 7. per-church HTML pages (missing + orphan)
try {
  const dir = path.join(DOCS, 'churches');
  const files = new Set(fs.readdirSync(dir)
    .filter((f) => f.endsWith('.html') && f !== 'index.html').map((f) => f.slice(0, -5)));
  const missing = churches.filter((c) => !files.has(c.id)).map((c) => c.id);
  const orphan = diff(ids, files);
  record('per-church HTML pages', !missing.length && !orphan.length,
    `${files.size} pages | missing ${missing.length}, orphan ${orphan.length}`,
    [...missing, ...orphan.map((x) => 'orphan:' + x)]);
} catch (e) { record('per-church HTML pages', false, 'ERROR ' + e.message); }

// 8. duplicate ids
const seen = new Set(), dups = new Set();
for (const c of churches) { if (seen.has(c.id)) dups.add(c.id); seen.add(c.id); }
record('unique church ids', !dups.size, `${dups.size} duplicate id(s)`, [...dups]);

// ---- report ----
console.log(`\nMOOP Directory consistency — ${N.toLocaleString()} churches\n`);
let hardDrift = 0;
for (const r of results) {
  const mark = r.ok ? '✓' : r.optional ? '⚠' : '✗';
  console.log(`  ${mark}  ${r.name.padEnd(28)} ${r.detail}`);
  if (!r.ok) {
    if (!r.optional) hardDrift++;
    if (VERBOSE && r.ids.length) {
      console.log('       ' + r.ids.slice(0, CAP).join(', ') + (r.ids.length > CAP ? ` …(+${r.ids.length - CAP})` : ''));
    }
  }
}
console.log('');
if (hardDrift) {
  console.log(`  ${hardDrift} artifact(s) DRIFTED. Rebuild the affected ones (see CLAUDE.md "Change workflow") then re-run.${VERBOSE ? '' : ' Use --verbose for ids.'}\n`);
  process.exit(1);
}
console.log('  All derived artifacts in sync ✓\n');
