#!/usr/bin/env node
// MOOP rubric enforcement: LGBTQ-affirming denomination auto-flag.
//
// Bulk-applies overall_rating='red' to churches whose denomination string
// indicates membership in a national-level denomination that has officially
// adopted LGBTQ-affirming theology. Already-red and already-black records
// receive a rubric-note for transparency (no rating change). Records that
// have explicitly DISAFFILIATED from an affirming body are skipped, as
// are records in conservative cousin denominations (e.g. PRCA vs RCA,
// REC vs TEC, LCMS vs ELCA).
//
// Denominations covered (with adoption year):
//   PCUSA               (2014) — Presbyterian Church (U.S.A.)
//   ELCA                (2009) — Evangelical Lutheran Church in America
//   UMC                 (2024) — United Methodist Church post-Charlotte
//   TEC / ECUSA         (2003) — The Episcopal Church
//   UCC                 (2005) — United Church of Christ
//   Disciples of Christ (2013) — Christian Church (Disciples of Christ)
//   RCA (mainline)      (2021) — Reformed Church in America
//   Mennonite Church USA(2022) — MCUSA (post resolution)
//
// Usage:
//   node scripts/flag-affirming-denoms.js [--dry-run]

const fs = require('fs');
const path = require('path');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);
const DRY_RUN = process.argv.includes('--dry-run');

// Phrases that mean the church has LEFT the affirming denom — never auto-flag.
const DISAFFILIATED = /disaffiliat|formerly|ex-sbc|ex-umc|ex-pcusa|ex-elca|departed|withdrew|left the|expelled|non-denominational \(formerly|independent \(formerly|post-umc|post-pcusa|post-elca/i;

// Each rule: short label, year of formal affirmation, match regex, exclude regex.
const RULES = [
  {
    label: 'PCUSA',
    since: 2014,
    match: /\bpcusa\b|pc\s*\(\s*u\.?\s*s\.?\s*a\.?\s*\)|presbyterian church\s*\(\s*u\.?\s*s\.?\s*a\.?/i,
    exclude: /\bpca\b|\bopc\b|\barp\b|\bepc\b|\bcrc\b|orthodox presbyterian|presbyterian church in america|associate reformed presbyterian|cumberland presbyterian|bible presbyterian|reformed presbyterian|rpcna|\beco:|covenant order/i,
  },
  {
    label: 'ELCA',
    since: 2009,
    match: /\belca\b|evangelical lutheran church in america/i,
    exclude: /\blcms\b|\bwels\b|\blcmc\b|\bnalc\b|missouri synod|wisconsin evangelical|lutheran congregations in mission|confessional/i,
  },
  {
    label: 'UMC',
    since: 2024,
    match: /\bumc\b|united methodist/i,
    exclude: /global methodist|free methodist|evangelical methodist|wesleyan methodist|\bame\b|african methodist|gmc\b|\bemc\b|independent.*method|method.*independent|post-umc|former.*umc|umc\/gmc/i,
  },
  {
    label: 'TEC',
    since: 2003,
    match: /\btec\b|\becusa\b|^episcopal$|^episcopal church$|^the episcopal church|episcopal church \(tec\)|^the episcopal church \(tec\)|diocese of (southern|virginia|new york|los angeles|massachusetts|washington|chicago|atlanta|north carolina|texas)/i,
    exclude: /reformed episcopal|\bacna\b|anglican church in north america|continuing anglican|\brec\b|\bame\b|african methodist|\bamez\b|\bcme\b|christian methodist episcopal/i,
  },
  {
    label: 'UCC',
    since: 2005,
    match: /\bucc\b|united church of christ/i,
    exclude: /(^$)/, // no exclusions — UCC is unambiguous
  },
  {
    label: 'Disciples of Christ',
    since: 2013,
    match: /disciples of christ/i,
    exclude: /(^$)/,
  },
  {
    label: 'RCA (mainline)',
    since: 2021,
    match: /reformed church in america/i,
    exclude: /\burcna\b|\bprca\b|\bcrc\b|christian reformed|protestant reformed|united reformed|canadian reformed|free reformed|american reformed church.*canadian|reformed church in the united states|non-denominational/i,
  },
  {
    label: 'Mennonite Church USA',
    since: 2022,
    match: /mennonite church usa|\bmcusa\b/i,
    exclude: /mennonite brethren|conservative mennonite|beachy|\bbma\b|\bcmc\b|\bsmc\b|old order|keystone|mid-atlantic mennonite|eastern pennsylvania mennonite|pilgrim mennonite|fellowship$/i,
  },
];

const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
let flagged = 0;
let alreadyRedNoted = 0;
let alreadyBlackNoted = 0;
let skippedDisaffiliated = 0;
let skippedExcluded = 0;
const byLabel = {};
const changes = [];
const alreadyFlaggedChurches = [];

for (const c of d.churches) {
  if (!c) continue;
  const denomText = [c.denomination, c.denomination_family, c.denom_family]
    .filter(Boolean).join(' | ');
  if (!denomText) continue;

  if (DISAFFILIATED.test(denomText)) {
    // Don't auto-flag — these have explicitly left the affirming body.
    skippedDisaffiliated++;
    continue;
  }

  for (const rule of RULES) {
    if (!rule.match.test(denomText)) continue;
    if (rule.exclude.test(denomText)) {
      skippedExcluded++;
      break;
    }

    // Real match.
    const rubricMarker = `MOOP rubric: ${rule.label} — affirming since ${rule.since}`;
    if (c.overall_rating === 'red' || c.overall_rating === 'black') {
      const noted = String(c.enrichment_notes || '').includes(rubricMarker);
      if (!noted) {
        const note = `[${TODAY}] ${rubricMarker}. Already rated ${c.overall_rating}.`;
        c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
        if (c.overall_rating === 'red') alreadyRedNoted++;
        else alreadyBlackNoted++;
        alreadyFlaggedChurches.push({id: c.id, name: c.name, rating: c.overall_rating, denom: c.denomination, label: rule.label});
      }
      break;
    }

    // New auto-flag: downgrade to RED.
    const prevRating = c.overall_rating || 'unrated';
    c.overall_rating = 'red';
    const note = `[${TODAY}] MOOP rubric auto-flag: ${rule.label} — denomination has officially adopted LGBTQ-affirming theology since ${rule.since}. Was ${prevRating}; downgraded to red. Human review recommended to confirm congregation alignment with denominational stance.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    c.needs_review = true;
    flagged++;
    byLabel[rule.label] = (byLabel[rule.label] || 0) + 1;
    changes.push({id: c.id, name: c.name, prev: prevRating, denom: c.denomination, label: rule.label});
    break;
  }
}

if (!DRY_RUN) {
  d.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
}

console.log(`LGBTQ-Affirming Denomination Auto-Flag${DRY_RUN ? ' (DRY RUN)' : ''}:`);
console.log(`  Newly flagged RED:                ${flagged}`);
console.log(`  Already red (rubric note added):  ${alreadyRedNoted}`);
console.log(`  Already black (rubric note added):${alreadyBlackNoted}`);
console.log(`  Skipped (disaffiliated/former):   ${skippedDisaffiliated}`);
console.log(`  Skipped (denom-excluded sibling): ${skippedExcluded}`);

console.log('\nNewly flagged by denomination:');
for (const [label, count] of Object.entries(byLabel).sort((a,b) => b[1]-a[1])) {
  console.log(`  ${label.padEnd(28)} ${count}`);
}

if (changes.length) {
  console.log('\nFirst 30 newly-flagged records:');
  for (const ch of changes.slice(0, 30)) {
    const name = (ch.name || '').slice(0, 50);
    const denom = (ch.denom || '').slice(0, 40);
    console.log(`  ${String(ch.id).padEnd(35)} prev=${ch.prev.padEnd(7)} ${ch.label.padEnd(12)} ${name.padEnd(50)} (${denom})`);
  }
}

if (alreadyFlaggedChurches.length) {
  console.log(`\n${alreadyFlaggedChurches.length} already-rated churches got rubric notes. First 10:`);
  for (const ch of alreadyFlaggedChurches.slice(0, 10)) {
    const name = (ch.name || '').slice(0, 50);
    console.log(`  ${String(ch.id).padEnd(35)} ${ch.rating.padEnd(6)} ${ch.label.padEnd(12)} ${name}`);
  }
}
