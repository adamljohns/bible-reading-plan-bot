#!/usr/bin/env node
//
// apply-enrichment-round.js — apply a verified research-round result file to
// churches.json. Used by the overnight agent-research enrichment rounds.
//
// Input JSON: array of {
//   id, address?, pastor?, pastor_credentials?,
//   facebook?, youtube?, instagram?,
//   enrichment_note?, review_gender?, gender_flag?,
//   // leadership transition (a retirement / resignation / interim / announced
//   // successor candidate). Informational only; NEVER changes a rating:
//   transition_status?,   // one of: retiring | resigning | interim | candidate-announced | vacant | incoming
//   transition_note?,     // human-readable detail ("Dr. X retiring Sept 2026; ...")
//   successor?,           // named successor / candidate, if any
//   transition_effective?,// e.g. "September 2026"
//   transition_source?,   // church-website | church-facebook | news | agent-research
//   successor_gender?     // 'female' -> records a review flag (NOT auto-RED; not installed yet)
// }
//
// Safety:
//   - address written only when the church lacks a street address and the new
//     one is a real, geocodable street address (shared goodAddress predicate)
//   - pastor applied only if it passes the placeholder/junk filter
//   - social URLs applied only if they match the expected domain + https
//   - gender_flag === 'female-senior-pastor' on a green church -> downgrade to
//     red (per the MOOP rubric: a SOLE female senior pastor is RED minimum)
//   - review_gender (co-pastor couples etc.) records a flag for human review
//   - a leadership transition is recorded as data only; a female *candidate*
//     records a review flag but does not move the rating until she is installed
//
// Usage: node apply-enrichment-round.js /tmp/round-results.json

const fs = require('fs');
const path = require('path');
const { hasStreetAddress, goodAddress } = require('./lib/address-util');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const INPUT = process.argv[2] || '/tmp/round-results.json';
// Local calendar day (America/New_York), not UTC, so a church touched on the
// evening of the 2nd is stamped the 2nd rather than rolling to the 3rd.
const TODAY = new Date().toLocaleDateString('en-CA', { timeZone: 'America/New_York' });

const PH = /^(verify|various|unknown|see\s+website|currently|none|listed|tbd|n\/a|the\s+pastor|the\s+church|pastoral|pastor\s*\(|check |contact |not\s+(listed|published)|vacant|interim)/i;
const JUNK = /(black hawk|hawk down|enjoy|movie|video|book|sermon|story|message|search|committee|jesus|christ|^god$|^lord$|spirit|gospel|kingdom|salvation|baptism|sunday|service)/i;

function realPastor(p) {
  p = String(p || '').trim();
  if (p.length < 4) return false;
  if (PH.test(p)) return false;
  if (JUNK.test(p)) return false;
  // Must look like a human name: at least two words OR a title+name
  if (!/\s/.test(p) && !/^[A-Z][a-z]+$/.test(p)) return false;
  return true;
}

const TRANSITION_STATUSES = new Set(['retiring', 'resigning', 'interim', 'candidate-announced', 'vacant', 'incoming']);

const results = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const data = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
const byId = new Map(data.churches.map(c => [String(c.id || c.slug), c]));

let pastors = 0, social = 0, downgrades = 0, flags = 0, addresses = 0, transitions = 0;
for (const r of results) {
  const c = byId.get(String(r.id));
  if (!c) continue;
  const _before = pastors + social + downgrades + flags + addresses + transitions;

  // Address: set only when the church currently lacks a street address and the
  // researched one is a real, geocodable street address. Clear _geocode_failed
  // so the geocode autopilot re-attempts this church on its next tick.
  if (r.address && goodAddress(r.address)) {
    if (!hasStreetAddress(c.address || '')) {
      c.address = r.address.trim();
      c.address_source = 'agent-research-verified';
      delete c._geocode_failed;
      addresses++;
    }
  }

  if (r.pastor && realPastor(r.pastor)) {
    c.pastor = r.pastor.trim();
    c.pastor_source = 'agent-research-verified';
    pastors++;
    if (r.pastor_credentials && (!c.pastor_credentials || c.pastor_credentials === 'Unknown')) {
      c.pastor_credentials = r.pastor_credentials.trim();
    }
  }
  for (const [field, host] of [['facebook','facebook.com'],['youtube','youtube.com'],['instagram','instagram.com']]) {
    const v = r[field];
    if (v && /^https:\/\//i.test(v) && v.toLowerCase().includes(host) && !c[field]) {
      c[field] = v; social++;
    }
  }

  // Leadership transition (retirement / resignation / interim / announced
  // successor). Stored as structured data and shown on the church page; it does
  // NOT touch the pastor field (the installed pastor stays current until the
  // handoff completes) and never moves a rating on its own.
  if (r.transition_status || r.transition_note) {
    const status = TRANSITION_STATUSES.has(String(r.transition_status)) ? r.transition_status : 'announced';
    const detail = String(r.transition_note || '').trim();
    if (detail) {
      c.pastor_transition = {
        status,
        detail,
        ...(r.successor ? { successor: String(r.successor).trim() } : {}),
        ...(r.transition_effective ? { effective: String(r.transition_effective).trim() } : {}),
        source: r.transition_source || 'agent-research',
        updated: TODAY,
      };
      transitions++;
      // A female *candidate* is a human-review flag, not an automatic downgrade;
      // the rubric acts on an installed sole female senior pastor, not a nominee.
      if (String(r.successor_gender || '').toLowerCase() === 'female') {
        c.review_gender = true;
        flags++;
      }
    }
  }

  if (r.enrichment_note) {
    if (!Array.isArray(c.enrichment_notes)) c.enrichment_notes = c.enrichment_notes ? [String(c.enrichment_notes)] : [];
    const stamp = '[' + TODAY + '] [agent-research] ' + r.enrichment_note;
    if (!c.enrichment_notes.includes(stamp)) c.enrichment_notes.push(stamp);
  }
  // SOLE female senior pastor -> RED per rubric
  if (r.gender_flag === 'female-senior-pastor' && c.overall_rating === 'green') {
    c.overall_rating = 'red';
    c.overall_label = 'RED — female senior pastor (rubric: complementarian leadership)';
    if (c.scores) c.scores.gender = 'red';
    downgrades++;
  }
  // Co-pastor / ambiguous gender cases -> flag for human review, no auto-change
  if (r.review_gender) { c.review_gender = true; flags++; }

  // Stamp a per-church review date whenever this round actually changed the record,
  // so each church page shows an honest "Last reviewed" date (read by lastReviewed()
  // in generate-church-pages.js). Untouched churches keep whatever date they had.
  if (pastors + social + downgrades + flags + addresses + transitions > _before) c.last_reviewed = TODAY;
}

fs.writeFileSync(CHURCHES, JSON.stringify(data, null, 2) + '\n');
console.log('Applied: +' + addresses + ' addresses, +' + pastors + ' pastors, +' + social + ' social URLs, +' + transitions + ' leadership updates, ' + downgrades + ' rubric downgrades, ' + flags + ' gender-review flags');
