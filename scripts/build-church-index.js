#!/usr/bin/env node
// Build the directory-page data artifacts from docs/data/churches.json:
//
//   1. docs/data/churches-index.json        — LEGACY full card index (~21 MB). Kept byte-for-byte
//      compatible for everything that still reads it (sitemap.html count, regional pages,
//      external scripts). churches.html no longer loads this.
//   2. docs/data/churches-index-slim.json   — what churches.html now downloads up front (~9 MB):
//      card-grid + filter + search + geo essentials ONLY. Same top-level shape as the legacy
//      index (directory_version/directory_updated/total_churches/rubric/churches) so the
//      footer-count contract is unchanged.
//   3. docs/data/churches/detail/<key>.json — expand-only detail shards, keyed by the first two
//      characters of the church id (lowercased, non-alphanumeric → '_' — ids can contain spaces
//      and accents, which are hostile as filenames/URLs). Each shard maps id → {assessment,
//      score_notes, services, gender_detail, pastor_credentials, tags, pastors}. churches.html
//      fetches a shard lazily the first time a card with that prefix is expanded.
//
// History: churches.json is ~61 MB pretty-printed and the page used to download ALL of it on
// every visit (twice — main load + footer count). The 2026-06 index cut that to ~21 MB; this
// split cuts the up-front payload again by moving the expand-only ~13 MB into lazy shards.
//
// What is deliberately EXCLUDED everywhere (lives on the per-church pages, not the card grid):
// enrichment_notes, signatories, engagement, sources, quick_links, image_url, image_thumb,
// last_reviewed, pastor_transition, slug, url_research_status, social links.
//
// Usage:
//   node scripts/build-church-index.js          # standalone rebuild (all three artifacts)
// Also invoked automatically at the end of generate-church-pages.js via writeIndex() (including
// --only runs), so none of the artifacts can drift from churches.json under the standard
// regen-then-push workflow.

const fs = require('fs');
const path = require('path');

// Card fields copied verbatim when non-empty into the LEGACY index (unchanged since 2026-06).
const FIELDS = [
  'id', 'name', 'overall_rating', 'denomination', 'denomination_family', 'founded',
  'pastor', 'pastors', 'pastor_credentials', 'address', 'website', 'services',
  'has_mens_ministry', 'has_kids_ministry', 'tags',
  'score_notes', 'gender_detail', 'assessment', 'region', 'type',
];

// Slim split of the same set: SLIM feeds the card grid, filters, search blob and geo lookup;
// DETAIL is only needed once a card is expanded (scorecard notes, assessment, services…).
// `pastors` appears in both worlds: slim carries names only (search blob), detail the full
// {name, role} objects. Keep the two lists in lockstep with buildCardEl/buildExpandedHtml
// in docs/churches.html.
const SLIM_FIELDS = [
  'id', 'name', 'overall_rating', 'denomination', 'denomination_family', 'founded',
  'pastor', 'address', 'website',
  'has_mens_ministry', 'has_kids_ministry', 'region', 'type',
];
const DETAIL_FIELDS = [
  'assessment', 'score_notes', 'services', 'gender_detail', 'pastor_credentials', 'tags', 'pastors',
];

const COLOR_CHAR = { green: 'g', yellow: 'y', red: 'r', black: 'b', gray: '-' };

function compactScores(scores, rubric, warnings) {
  return rubric.map(r => {
    const v = scores ? scores[r.id] : undefined;
    if (v === undefined || v === null || v === '') return '-';
    const c = COLOR_CHAR[String(v).toLowerCase().trim()];
    if (!c) { warnings.add(String(v)); return '-'; }
    return c;
  }).join('');
}

function isEmpty(v) {
  if (v === undefined || v === null || v === '') return true;
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === 'object') return Object.keys(v).length === 0;
  return v === false; // booleans: absent reads as false on the page, so drop false
}

// Geo for the "City, State or ZIP" radius lookup (2026-07-11): each index entry
// gets ll:[lat,lng] — the church's own geocode when present (11k records), else
// the Census centroid of the trailing 5-digit ZIP in its address (13k more).
// Coordinates rounded to 3 dp (~110 m) to keep the index lean. Entries with no
// geocode and no parseable ZIP simply omit ll (they can't appear in radius results).
let ZCTA = null;
function loadZcta() {
  if (ZCTA) return ZCTA;
  try {
    ZCTA = JSON.parse(fs.readFileSync(path.join(__dirname, '../docs/data/geo/zcta-centroids.json'), 'utf8')).zcta || {};
  } catch (_) { ZCTA = {}; }
  return ZCTA;
}
const round3 = n => Math.round(parseFloat(n) * 1000) / 1000;
function churchLatLng(c) {
  if (isFinite(parseFloat(c.latitude)) && isFinite(parseFloat(c.longitude))) {
    return [round3(c.latitude), round3(c.longitude)];
  }
  const m = String(c.address || '').match(/\b(\d{5})(?:-\d{4})?\s*$/);
  return (m && loadZcta()[m[1]]) || null;
}

// vf=1 — "verifiable web presence" (real website or at least one social). Absent
// means zero-presence: the page badges these "unverified" and ranks them last
// (Adam's 2026-07-11 demote-and-rescue policy).
const isVerifiable = c =>
  (typeof c.website === 'string' && /^https?:\/\//i.test(c.website)) ||
  !!(c.facebook || c.youtube || c.instagram);

function buildIndex(data) {
  const rubric = data.rubric || [];
  const warnings = new Set();
  const churches = data.churches.map(c => {
    const slim = {};
    for (const k of FIELDS) {
      if (!isEmpty(c[k])) slim[k] = c[k];
    }
    const sc = compactScores(c.scores, rubric, warnings);
    if (sc.replace(/-/g, '') !== '') slim.scores = sc; // all-gray ⇒ omit entirely
    const ll = churchLatLng(c);
    if (ll) slim.ll = ll;
    if (isVerifiable(c)) slim.vf = 1;
    return slim;
  });
  if (warnings.size) {
    console.warn(`⚠️  Unrecognized score values mapped to gray: ${[...warnings].join(', ')}`);
  }
  return {
    directory_version: data.directory_version,
    directory_updated: data.directory_updated,
    total_churches: data.total_churches,
    rubric,
    churches,
  };
}

// Slim index — same wrapper as the legacy index (footer reads total_churches +
// directory_updated from it), entries limited to SLIM_FIELDS + derived fields.
function buildSlimIndex(data) {
  const rubric = data.rubric || [];
  const warnings = new Set(); // buildIndex already prints these; stay quiet here
  const churches = data.churches.map(c => {
    const slim = {};
    for (const k of SLIM_FIELDS) {
      if (!isEmpty(c[k])) slim[k] = c[k];
    }
    // Names only — search-blob material; the {name, role} objects ride in the detail shard.
    if (Array.isArray(c.pastors)) {
      const names = c.pastors.map(p => p && p.name).filter(Boolean);
      if (names.length) slim.pastors = names;
    }
    const sc = compactScores(c.scores, rubric, warnings);
    if (sc.replace(/-/g, '') !== '') slim.scores = sc; // all-gray ⇒ omit entirely
    const ll = churchLatLng(c);
    if (ll) slim.ll = ll;
    if (isVerifiable(c)) slim.vf = 1;
    return slim;
  });
  return {
    directory_version: data.directory_version,
    directory_updated: data.directory_updated,
    total_churches: data.total_churches,
    rubric,
    churches,
  };
}

// Shard key = first two id chars, lowercased, anything outside [a-z0-9] → '_'.
// MUST stay identical to shardKeyOf() in docs/churches.html (plain String ops only —
// slice/toLowerCase/replace behave the same in Node and every browser).
function shardKey(id) {
  return String(id).slice(0, 2).toLowerCase().replace(/[^a-z0-9]/g, '_');
}

// key → { id → {detail fields} }, ids sorted inside each shard for stable output.
// Every key that has at least one church gets a bucket (possibly {}) so the page
// never 404s on a legitimate prefix.
function buildDetailShards(data) {
  const shards = new Map();
  for (const c of data.churches) {
    const key = shardKey(c.id);
    if (!shards.has(key)) shards.set(key, {});
    const det = {};
    for (const k of DETAIL_FIELDS) {
      if (!isEmpty(c[k])) det[k] = c[k];
    }
    if (Object.keys(det).length) shards.get(key)[c.id] = det;
  }
  // Stable ordering regardless of churches.json ordering.
  const sorted = new Map();
  for (const key of [...shards.keys()].sort()) {
    const bucket = shards.get(key);
    const obj = {};
    for (const id of Object.keys(bucket).sort()) obj[id] = bucket[id];
    sorted.set(key, obj);
  }
  return sorted;
}

// ASCII-escaped (repo canon for data files), minified, no trailing newline.
const jsonAscii = obj => JSON.stringify(obj)
  .replace(/[^\x00-\x7F]/g, ch => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'));

// Write only when the bytes actually changed — keeps mtimes/rclone/git quiet on no-op regens
// (same philosophy as the state/denomination shard builders).
function writeIfChanged(p, buf) {
  try { if (fs.readFileSync(p, 'utf8') === buf) return false; } catch (_) { /* new file */ }
  fs.writeFileSync(p, buf);
  return true;
}

// Slim index + detail shards, written next to the legacy index. Prunes orphan shard
// files (a prefix that vanished would otherwise keep serving stale detail forever).
function writeSlimAndShards(data, dataDir) {
  const slimBuf = jsonAscii(buildSlimIndex(data));
  writeIfChanged(path.join(dataDir, 'churches-index-slim.json'), slimBuf);

  const detailDir = path.join(dataDir, 'churches', 'detail');
  fs.mkdirSync(detailDir, { recursive: true });
  const shards = buildDetailShards(data);
  let shardBytes = 0, maxBytes = 0;
  for (const [key, bucket] of shards) {
    const buf = jsonAscii(bucket);
    writeIfChanged(path.join(detailDir, key + '.json'), buf);
    shardBytes += Buffer.byteLength(buf);
    maxBytes = Math.max(maxBytes, Buffer.byteLength(buf));
  }
  const keep = new Set([...shards.keys()].map(k => k + '.json'));
  for (const f of fs.readdirSync(detailDir)) {
    if (f.endsWith('.json') && !keep.has(f)) fs.unlinkSync(path.join(detailDir, f));
  }
  return { slimBytes: Buffer.byteLength(slimBuf), shardCount: shards.size, shardBytes, maxBytes };
}

// Legacy entry point (generate-church-pages.js calls this): writes the legacy index at
// outPath exactly as before AND the slim index + detail shards beside it, so all three
// artifacts always regenerate together. Returns the legacy byte count (unchanged contract).
function writeIndex(data, outPath) {
  const buf = jsonAscii(buildIndex(data));
  fs.writeFileSync(outPath, buf);
  writeSlimAndShards(data, path.dirname(outPath));
  return Buffer.byteLength(buf);
}

module.exports = { buildIndex, buildSlimIndex, buildDetailShards, shardKey, writeIndex, writeSlimAndShards };

if (require.main === module) {
  const REPO_ROOT = path.resolve(__dirname, '..');
  const data = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'docs/data/churches.json'), 'utf8'));
  const outPath = path.join(REPO_ROOT, 'docs/data/churches-index.json');
  const bytes = writeIndex(data, outPath);
  // writeIndex already produced them; rebuild the stats cheaply for the log line.
  const s = writeSlimAndShards(data, path.dirname(outPath));
  const mb = b => (b / 1048576).toFixed(1);
  console.log(`✅ churches-index.json — ${data.churches.length} churches, ${mb(bytes)} MB (legacy)`);
  console.log(`✅ churches-index-slim.json — ${mb(s.slimBytes)} MB up-front payload`);
  console.log(`✅ churches/detail/ — ${s.shardCount} shards, ${mb(s.shardBytes)} MB total, largest ${mb(s.maxBytes)} MB`);
}
