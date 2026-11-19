'use strict';
// denominations.js — canonical denomination schema, alias normalization,
// evidence-ledger validation and deterministic MOOP category scoring.
//
// Law of this module:
//  * A score exists only when a WRITTEN rule (RULES below, published on every
//    denomination page) maps evidence to it AND every quote the rule relies on
//    is verbatim in a captured official source snapshot. Otherwise "unknown".
//  * The denomination grade is CONTEXT for a church page, never its rating.
//    A church's own evidence wins.
//  * No model runs here. Validation is string matching on snapshots.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.join(__dirname, '..', '..');
const DATA_DIR = path.join(ROOT, 'data', 'denominations');
const SRC_DIR = path.join(DATA_DIR, 'sources');

const CATEGORIES = ['scripture', 'christology', 'gender', 'soteriology', 'preaching', 'cultural',
  'leadership', 'mission', 'mens_discipleship', 'denominational'];
const GRADES = ['green', 'yellow', 'red', 'black', 'unknown'];
const GOVERNANCE = ['binding', 'mixed', 'advisory', 'autonomous'];
// The published LGBTQ-affirming list (usmcmin.org/directory-methodology.html).
const AFFIRMING_IDS = new Set(['pcusa', 'elca', 'umc', 'tec', 'ucc', 'disciples', 'rca', 'mcusa']);

// Each rule: grade + id + published text + the patterns that must each be met
// by at least one validated quote supporting that category. First match wins,
// so stricter (worse) grades are listed first.
const RULES = {
  scripture: [
    { grade: 'green', id: 'D-SCR-1', text: 'The official confession affirms Scripture is without error (inerrant) and the final authority (also worded "supreme standard", "ultimate authority" or "only infallible rule of faith and practice") → GREEN. Both halves need a quote.', all: [/without (any mixture of )?error|inerran/i, /supreme standard|ultimate authority|final authority|inerrancy and authority|only infallible rule of faith and practice/i] },
  ],
  christology: [
    { grade: 'green', id: 'D-CHR-1', text: 'The official confession affirms Christ is fully God and fully man (also worded "truly God and truly man" or "very God and very man") → GREEN.', all: [/fully God,? (and )?fully man|truly God and truly man|very God and very man/i] },
  ],
  soteriology: [
    { grade: 'green', id: 'D-SOT-1', text: 'The official confession affirms justification by grace through faith alone in Christ alone (also worded "justified by faith only", not by works, or justification defined as God\'s gracious acquittal of sinners who repent and believe in Christ) → GREEN.', all: [/grace through faith alone|justified by faith,? only|only by faith in our Lord Jesus Christ|justification is God.s gracious and full acquittal/i] },
  ],
  gender: [
    { grade: 'red', id: 'D-GEN-1', text: 'The body ordains women to pastoral office → RED minimum (same line as "Female senior pastor → RED minimum.").', all: [/\bordains? women\b(?!.*not)|ordination of women is permitted|women were ordained[^.]*full clergy rights|men and women respond to God.s call to ordained ministry/i], none: [/does not ordain women/i] },
    { grade: 'green', id: 'D-GEN-2', text: 'An official decision or confession restricts ordination or the pastoral office to qualified men → GREEN. Non-ordained ministry roles for women are noted, not penalized.', all: [/does not ordain women|qualified males|office of pastor[^.]{0,30} is limited to men/i] },
    { grade: 'yellow', id: 'D-GEN-3', text: 'The body leaves the ordination of women to each local church (it neither requires nor forbids it) → YELLOW: the church\'s own evidence decides.', all: [/ordination of women[^.]{0,60}local church matter/i] },
  ],
  leadership: [
    { grade: 'yellow', id: 'D-LDR-1', text: 'Ordination is restricted to men, but elder/leadership policy is left to each local church → YELLOW (mixed): the church\'s own evidence decides.', all: [/does not ordain women|qualified males/i, /local church is free|no official [A-Z]* ?policy for local churches/i] },
    { grade: 'green', id: 'D-LDR-2', text: 'Ordination and elder office are restricted to men by a binding rule → GREEN.', all: [/does not ordain women|qualified males/i, /elders? (must|shall) be (qualified )?men/i] },
    { grade: 'green', id: 'D-LDR-3', text: 'The official confession limits the pastor/elder office to men → GREEN. Where the body is autonomous, each church\'s own evidence still decides.', all: [/(elder|overseer)[^.]{0,20} is limited to men/i] },
    { grade: 'yellow', id: 'D-LDR-4', text: 'Who may be ordained or lead is left to each local church → YELLOW: the church\'s own evidence decides.', all: [/ordination of women[^.]{0,60}local church matter/i] },
    { grade: 'red', id: 'D-LDR-5', text: 'The body ordains women to the pastoral office → RED (same line as D-GEN-1).', all: [/women were ordained[^.]*full clergy rights|men and women respond to God.s call to ordained ministry/i] },
  ],
  cultural: [
    { grade: 'red', id: 'D-CUL-2', text: 'An official statement affirms marriage between two persons of the same sex → RED.', all: [/or two adult persons of consenting age/i] },
    { grade: 'green', id: 'D-CUL-1', text: 'An official statement defines marriage as one man and one woman → GREEN.', all: [/one man and one woman/i] },
  ],
  denominational: [
    { grade: 'red', id: 'D-DEN-1', text: 'LGBTQ-affirming denomination → RED minimum.', listed: true },
    { grade: 'green', id: 'D-DEN-2', text: 'Not on the published LGBTQ-affirming list, and an official statement defines marriage as one man and one woman → GREEN.', all: [/one man and one woman/i] },
  ],
  mission: [
    { grade: 'green', id: 'D-MIS-1', text: 'The official mission is gospel or church multiplication among all people → GREEN.', all: [/multiplying [a-z ]*churches|great commission|make disciples of (all nations|Jesus Christ)/i] },
  ],
  preaching: [],
  mens_discipleship: [],
};

const GOV_RULES = [
  { strength: 'binding', id: 'D-GOV-1', text: 'Doctrine and practice decisions bind every congregation (hierarchical or connectional authority) → BINDING.', all: [/binding on (all|every|member) (churches|congregations)|hierarchical|universally-binding to all|normative teaching is binding and obligatory|full legislative power over all matters that are distinctly connectional/i] },
  { strength: 'autonomous', id: 'D-GOV-5', text: 'Each church is autonomous and the body disclaims any authority over it; its confession binds no church. Cooperation or affiliation can still require agreement with that confession → AUTONOMOUS.', all: [/autonomous/i, /never attempt to exercise any authority over|disclaims all right of exercising authority over any church|shall not be binding upon any local church/i] },
  { strength: 'mixed', id: 'D-GOV-2', text: 'Autonomous congregations united by a required common confession; practice decisions stay local → MIXED.', all: [/autonomous|self-govern|govern its own affairs/i, /united around/i] },
  { strength: 'advisory', id: 'D-GOV-3', text: 'Denominational statements are offered as guidance only → ADVISORY.', all: [/advisory|guidance only|not binding/i] },
  { strength: 'autonomous', id: 'D-GOV-4', text: 'Fully independent congregations with no required common confession → AUTONOMOUS.', all: [/autonomous|self-govern/i] },
];

const nrm = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
  .replace(/[–—]/g, '-').replace(/ /g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
// Same normalization without case folding: quotes are checked case-sensitively
// (BoD ¶120 "the Church" is not the umc.org footer's "the church").
const nrmCase = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
  .replace(/[–—]/g, '-').replace(/ /g, ' ').replace(/\s+/g, ' ').trim();
const aliasKey = s => nrm(s).replace(/[^a-z0-9]+/g, ' ').trim();

function loadDenominations(dir = DATA_DIR) {
  return fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort()
    .map(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
}

function aliasIndex(denoms) {
  const m = new Map();
  for (const d of denoms) {
    for (const a of [d.id, d.name, d.short_name, ...(d.aliases || [])].filter(Boolean)) {
      const k = aliasKey(a);
      if (m.has(k) && m.get(k) !== d.id) throw new Error(`alias "${a}" maps to both ${m.get(k)} and ${d.id}`);
      m.set(k, d.id);
    }
  }
  return m;
}

// Exact alias match only. "Non-Denominational (... EFCA-tagged)" must NOT map.
function normalizeDenomination(label, index) {
  if (!label) return null;
  return index.get(aliasKey(label)) || null;
}

// A snapshot is two files: <slug>.txt (whole page, tag-stripped, kept as the
// archive) and <slug>.body.txt (main content region only: no nav, header,
// footer or aside; written by denominations-capture-source.py). `text` below is
// the BODY. Quotes are validated against the body only, so a phrase found only
// in site chrome never passes. No body snapshot = no validation.
function loadSource(denomId, slug, srcDir = SRC_DIR) {
  const base = path.join(srcDir, denomId, slug);
  const meta = JSON.parse(fs.readFileSync(base + '.meta.json', 'utf8'));
  const full = fs.readFileSync(base + '.txt', 'utf8');
  const text = fs.readFileSync(base + '.body.txt', 'utf8');
  const h = t => crypto.createHash('sha256').update(t.replace(/\n$/, '')).digest('hex');
  return { text, full, meta, sha_ok: !!meta.sha256_body && h(text) === meta.sha256_body && h(full) === meta.sha256_text };
}

function quoteInSource(quote, text) {
  const q = nrmCase(quote).replace(/^[\s.,;:"']+|[\s.,;:"']+$/g, '');
  return q.length >= 12 && nrmCase(text).includes(q);
}

// Build the evidence ledger: each row validated against its snapshot.
function buildLedger(denom, srcDir = SRC_DIR) {
  return (denom.evidence || []).map(e => {
    let src = null, err = null;
    try { src = loadSource(denom.id, e.source, srcDir); } catch (x) { err = x.code || x.message; }
    const urlOk = !!src && (src.meta.url === e.url || src.meta.final_url === e.url);
    const found = !!src && src.sha_ok && urlOk && quoteInSource(e.quote, src.text);
    return {
      id: e.id, quote: e.quote, url: e.url, supports: e.supports,
      retrieved_at: src ? src.meta.retrieved_at : null,
      extractor: src ? src.meta.extractor : null, model: e.model || null,
      body_region: src ? src.meta.body_region || null : null, linked_from: src ? src.meta.linked_from || null : null,
      source_sha256: src ? src.meta.sha256_text : null,
      validated: found,
      confidence: found ? 1.0 : 0,
      error: err || (!src ? 'no snapshot' : !src.sha_ok ? 'snapshot hash mismatch' : !urlOk ? 'url does not match snapshot' : !found ? 'quote not in document body' : null),
    };
  });
}

function matchRule(rule, quotes, denomId) {
  // A listed rule still shows the official quotes that support the category.
  if (rule.listed) return AFFIRMING_IDS.has(denomId) ? { used: quotes.map(q => q.id) } : null;
  if (rule.none && rule.none.some(re => quotes.some(q => re.test(q.quote)))) return null;
  const used = [];
  for (const re of rule.all || []) {
    const hit = quotes.find(q => re.test(q.quote));
    if (!hit) return null;
    if (!used.includes(hit.id)) used.push(hit.id);
  }
  return { used };
}

function scoreDenomination(denom, ledger) {
  const scores = {};
  for (const cat of CATEGORIES) {
    const quotes = ledger.filter(l => l.validated && (l.supports || []).includes(cat));
    let out = { grade: 'unknown', rule: null, evidence: [], note: 'No validated official quote maps to a published rule.' };
    for (const rule of RULES[cat] || []) {
      const m = matchRule(rule, quotes, denom.id);
      if (m) { out = { grade: rule.grade, rule: { id: rule.id, text: rule.text }, evidence: m.used, note: '' }; break; }
    }
    scores[cat] = out;
  }
  const gq = ledger.filter(l => l.validated && (l.supports || []).includes('governance'));
  let governance = { strength: null, rule: null, evidence: [] };
  for (const r of GOV_RULES) {
    const m = matchRule(r, gq, denom.id);
    if (m) { governance = { strength: r.strength, rule: { id: r.id, text: r.text }, evidence: m.used }; break; }
  }
  const graded = Object.values(scores).map(s => s.grade).filter(g => g !== 'unknown');
  const worst = ['black', 'red', 'yellow', 'green'].find(g => graded.includes(g)) || 'unknown';
  return { scores, governance, context_grade: worst };
}

function verifyCongregations(denom, churchesById, srcDir = SRC_DIR) {
  return (denom.verified_congregations || []).map(v => {
    const c = churchesById.get(v.church_id);
    let ok = false, err = null, meta = null;
    try {
      const s = loadSource('_congregations', v.church_id, srcDir); meta = s.meta;
      ok = s.sha_ok && quoteInSource(v.quote, s.text) && (s.meta.url === v.url || s.meta.final_url === v.url);
      if (!ok) err = 'quote/url not validated in congregation snapshot';
    } catch (x) { err = x.code || x.message; }
    if (!c) { ok = false; err = 'church id not in churches.json'; }
    return { ...v, name: c ? c.name : null, city: c ? c.city || '' : '', state: c ? c.state : '', retrieved_at: meta && meta.retrieved_at, validated: ok, error: err };
  });
}

// Phase 1 alias map (data/denominations/aliases/alias-map.json, generated by
// scripts/build-denomination-alias-map.js). Classifies any raw churches.json
// label as { status: 'body', id, conference|presbytery|diocese|... } |
// { status: 'generic', family } (never graded) | { status: 'unresolved' }.
const ALIAS_MAP = path.join(DATA_DIR, 'aliases', 'alias-map.json');
function loadAliasMap(file = ALIAS_MAP) {
  const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  const exact = new Map(), loose = new Map();
  for (const l of doc.labels) {
    exact.set(l.label, l);
    const k = aliasKey(l.label);
    const prev = loose.get(k);
    // A loose key shared by labels with different outcomes is not trusted.
    loose.set(k, prev === null ? null : prev && (prev.status !== l.status || prev.id !== l.id) ? null : (prev || l));
  }
  return { doc, exact, loose, bodies: new Map(doc.bodies.map(b => [b.id, b])) };
}
function classifyDenomination(label, map) {
  const s = label == null ? '' : String(label);
  const hit = map.exact.get(s) || map.exact.get(s.trim()) || map.loose.get(aliasKey(s));
  if (!hit) return { status: 'unresolved', reason: 'label not in alias map' };
  const { count, label: _l, ...rest } = hit; // eslint-disable-line no-unused-vars
  return rest;
}

module.exports = {
  loadAliasMap, classifyDenomination, ALIAS_MAP,
  CATEGORIES, GRADES, GOVERNANCE, RULES, GOV_RULES, AFFIRMING_IDS, DATA_DIR, SRC_DIR,
  nrm, nrmCase, aliasKey, loadDenominations, aliasIndex, normalizeDenomination, loadSource, quoteInSource,
  buildLedger, scoreDenomination, verifyCongregations,
};
