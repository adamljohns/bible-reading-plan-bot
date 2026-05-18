#!/usr/bin/env node
// Phase 5 — Resolve specific dupe sets by merging into a survivor record.
//
// For each merge spec, takes union of notable_attendees + cross_listed_in
// + signatories arrays from sources into survivor, then deletes sources.
//
// Edit the MERGES array below to add new dupe sets.

const fs = require('fs');
const path = require('path');
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');

const MERGES = [
  {
    survivor: 'redeemer-presbyterian-new-york-ny',
    sources: ['redeemer-presbyterian-nyc', 'redeemer-pca-new-york-ny'],
    note: 'Redeemer Presbyterian NYC (main campus) — 3 dupe records collapsed; East Side campus kept separate.',
  },
  {
    survivor: 'highview-baptist-church-louisville-sbc',
    sources: ['highview-baptist-church-louisville-ky'],
    note: 'Highview Baptist Louisville — empty-address dupe folded into the Fegenbush 7711 campus record. Shelbyville Rd + Fegenbush 4630 kept as separate campuses.',
  },
  {
    survivor: 'christ-church-moscow-wilson-id',
    sources: ['christ-church-moscow', 'christ-church-pca-moscow-id'],
    note: 'Christ Church Moscow ID (Doug Wilson) — 3 dupes merged; corrected the false "PCA" tag (this church is CREC, not PCA).',
  },
  {
    survivor: 'christ-covenant-pca-matthews-nc',
    sources: ['christ-covenant-matthews'],
    note: 'Christ Covenant Matthews NC (Kevin DeYoung) — 2 dupes merged into the record with full address.',
  },
];

function mergeArr(target, source) {
  if (!Array.isArray(target)) target = [];
  if (!Array.isArray(source)) return target;
  for (const item of source) {
    if (item == null) continue;
    if (typeof item === 'string') {
      if (!target.includes(item)) target.push(item);
    } else if (typeof item === 'object' && item.name) {
      // notable_attendees — dedup by name (case-insensitive)
      const name = String(item.name).toLowerCase().trim();
      if (!target.some(t => String(t.name || '').toLowerCase().trim() === name)) {
        target.push(item);
      }
    } else {
      // fallback: include if not already present (shallow equal)
      const key = JSON.stringify(item);
      if (!target.some(t => JSON.stringify(t) === key)) target.push(item);
    }
  }
  return target;
}

function mergeSignatories(target, source) {
  // signatories is an object: { warhurst_protest_2020: [...], ... }
  if (typeof target !== 'object' || target == null) return source;
  if (typeof source !== 'object' || source == null) return target;
  for (const k of Object.keys(source)) {
    if (Array.isArray(source[k])) {
      target[k] = mergeArr(target[k] || [], source[k]);
    }
  }
  return target;
}

function main() {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  const byId = new Map();
  for (const c of d.churches) {
    if (c && c.id) byId.set(c.id, c);
  }

  let mergedSpecs = 0, totalDeletions = 0;
  const deletionIds = new Set();

  for (const m of MERGES) {
    const survivor = byId.get(m.survivor);
    if (!survivor) {
      console.warn(`Survivor not found: ${m.survivor} — skipping merge`);
      continue;
    }
    let mergedSources = 0;
    for (const sid of m.sources) {
      const src = byId.get(sid);
      if (!src) { console.warn(`  Source not found: ${sid}`); continue; }
      survivor.cross_listed_in = mergeArr(survivor.cross_listed_in, src.cross_listed_in);
      survivor.notable_attendees = mergeArr(survivor.notable_attendees, src.notable_attendees);
      survivor.signatories = mergeSignatories(survivor.signatories, src.signatories);
      survivor.tags = mergeArr(survivor.tags, src.tags);
      // Carry forward enrichment_sources
      survivor.enrichment_sources = mergeArr(survivor.enrichment_sources || [], src.enrichment_sources || []);
      const noteAppend = `[${new Date().toISOString().slice(0,10)}] Merged dupe ${sid} into this record (Phase 5 cleanup).`;
      survivor.enrichment_notes = survivor.enrichment_notes ? (survivor.enrichment_notes + '\n' + noteAppend) : noteAppend;
      deletionIds.add(sid);
      mergedSources++;
    }
    if (mergedSources > 0) {
      mergedSpecs++;
      totalDeletions += mergedSources;
      console.log(`Merged ${mergedSources} into ${m.survivor}: ${m.note}`);
    }
  }

  // Remove sources from .churches
  const before = d.churches.length;
  d.churches = d.churches.filter(c => !(c && c.id && deletionIds.has(c.id)));
  const after = d.churches.length;
  d.total_churches = after;
  d.directory_updated = new Date().toISOString().slice(0, 10);

  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');

  console.log(`\nResults:`);
  console.log(`  Merge specs executed: ${mergedSpecs}`);
  console.log(`  Source records deleted: ${totalDeletions}`);
  console.log(`  Directory: ${before} → ${after}`);
}

if (require.main === module) main();
