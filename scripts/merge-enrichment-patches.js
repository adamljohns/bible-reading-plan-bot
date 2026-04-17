#!/usr/bin/env node
/**
 * merge-enrichment-patches.js — consume the 4 enrichment patch files
 * in /tmp/enrich-results-*.json and apply them atomically to
 * docs/data/churches.json.
 *
 * Input patches (written by parallel enrichment agents):
 *   /tmp/enrich-results-fb-1.json
 *   /tmp/enrich-results-fb-2.json
 *   /tmp/enrich-results-yt-1.json
 *   /tmp/enrich-results-new-1.json
 *
 * Patch schema:
 *   { batch_id, updates: [{id, fields}], new_churches: [{...}], skipped: [...], summary: {...} }
 *
 * This script:
 *   1. Reads all 4 patches (missing files are tolerated — warn and continue)
 *   2. Reads existing churches.json
 *   3. Applies field-level updates by ID — only writes non-empty new values,
 *      never overwrites an existing value with empty/null
 *   4. Appends new_churches with dedup against existing IDs + slugified names
 *   5. Writes the result back to churches.json with stable key order
 *   6. Prints a summary report
 */

const fs = require('fs');
const path = require('path');

const CHURCHES_PATH = path.resolve(__dirname, '../docs/data/churches.json');
const PATCH_DIR = '/tmp';
const ARCHIVE_DIR = '/tmp/enrich-archive';
// Auto-discover all unprocessed patch files at run time
function discoverPatchFiles() {
  if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  return fs
    .readdirSync(PATCH_DIR)
    .filter((n) => /^enrich-results-.+\.json$/.test(n))
    .map((n) => path.join(PATCH_DIR, n));
}
const PATCH_FILES = discoverPatchFiles();

function readJSONSafe(p) {
  if (!fs.existsSync(p)) {
    console.warn(`  ⚠️  missing: ${p} (agent may not have finished)`);
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    console.error(`  ❌ failed to parse ${p}: ${e.message}`);
    return null;
  }
}

function slugify(s) {
  return (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

function main() {
  console.log('==> Loading existing churches.json...');
  const root = JSON.parse(fs.readFileSync(CHURCHES_PATH, 'utf8'));
  const churches = root.churches;
  const byId = new Map(churches.map((c) => [String(c.id), c]));
  const nameSet = new Set(churches.map((c) => slugify(c.name)));
  console.log(`   ${churches.length} existing churches`);

  const totals = { updated: 0, fieldsAdded: 0, added: 0, skippedUpdates: 0, skippedNew: 0, conflicts: 0, byBatch: {} };

  for (const pf of PATCH_FILES) {
    const patch = readJSONSafe(pf);
    if (!patch) continue;
    const bId = patch.batch_id || path.basename(pf, '.json');
    const bStat = { updated: 0, fieldsAdded: 0, added: 0, skipped: 0 };

    // Apply field-level updates
    for (const u of patch.updates || []) {
      const target = byId.get(String(u.id));
      if (!target) {
        console.warn(`   [${bId}] update references unknown id ${u.id} — skipping`);
        totals.conflicts++;
        continue;
      }
      let touchedThisChurch = false;
      for (const [k, v] of Object.entries(u.fields || {})) {
        if (v == null || v === '' || v === false) continue;
        // Don't clobber existing non-empty values unless explicitly blank
        if (target[k] && target[k] === v) continue;
        if (target[k] && target[k] !== v) {
          // Existing value is different — prefer the patch (fresher research)
          // but log it so we can review
          console.log(`   [${bId}] ${u.id}.${k}: "${String(target[k]).slice(0, 60)}" → "${String(v).slice(0, 60)}"`);
        }
        target[k] = v;
        bStat.fieldsAdded++;
        touchedThisChurch = true;
      }
      if (touchedThisChurch) bStat.updated++;
    }

    // Append new churches
    for (const nc of patch.new_churches || []) {
      const id = String(nc.id || '');
      if (!id) {
        console.warn(`   [${bId}] new church with no id — skipping`);
        bStat.skipped++;
        continue;
      }
      if (byId.has(id) || nameSet.has(slugify(nc.name))) {
        console.warn(`   [${bId}] duplicate: ${id} / ${nc.name} — skipping`);
        bStat.skipped++;
        continue;
      }
      // Basic sanity — require name, address, pastor
      if (!nc.name || !nc.address || !nc.pastor) {
        console.warn(`   [${bId}] incomplete record ${id} (name/address/pastor missing) — skipping`);
        bStat.skipped++;
        continue;
      }
      if (!nc.slug) nc.slug = id;
      churches.push(nc);
      byId.set(id, nc);
      nameSet.add(slugify(nc.name));
      bStat.added++;
    }

    totals.byBatch[bId] = bStat;
    totals.updated += bStat.updated;
    totals.fieldsAdded += bStat.fieldsAdded;
    totals.added += bStat.added;
    totals.skippedNew += bStat.skipped;
  }

  root.churches = churches;
  fs.writeFileSync(CHURCHES_PATH, JSON.stringify(root, null, 2) + '\n');

  console.log('\n==> Merge complete.');
  console.log(`   Total churches now: ${churches.length}`);
  console.log(`   Churches updated: ${totals.updated}`);
  console.log(`   Fields added: ${totals.fieldsAdded}`);
  console.log(`   New churches added: ${totals.added}`);
  console.log(`   Skipped (dup/incomplete): ${totals.skippedNew}`);
  console.log(`   Unknown-id conflicts: ${totals.conflicts}`);
  console.log('\n   Per-batch:');
  for (const [b, s] of Object.entries(totals.byBatch)) {
    console.log(`     ${b}: ${s.updated} updated, ${s.fieldsAdded} fields, ${s.added} new, ${s.skipped} skipped`);
  }

  // Emit a summary file for the commit message
  fs.writeFileSync(
    '/tmp/enrich-merge-summary.json',
    JSON.stringify({ final_count: churches.length, ...totals }, null, 2)
  );

  // Archive processed patches so a future merge run doesn't reapply them
  const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  for (const pf of PATCH_FILES) {
    const dst = path.join(ARCHIVE_DIR, `${ts}__${path.basename(pf)}`);
    try {
      fs.renameSync(pf, dst);
    } catch (e) {
      console.warn(`   could not archive ${pf}: ${e.message}`);
    }
  }
  console.log(`\n==> Archived ${PATCH_FILES.length} patch file(s) to ${ARCHIVE_DIR}/`);
}

main();
