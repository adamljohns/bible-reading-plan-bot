#!/usr/bin/env node
'use strict';
/**
 * Full-review patch builder (Chaps ticket, 2026-11-08).
 *
 * Stage 3 of a full-review round:
 *   select-enrichment-batch.js --full-review -> full-review-fetch.py ->
 *   full-review-build-patch.js -> apply-full-review-patch.js (Adam's GO only)
 *
 * READ-ONLY on churches.json. Turns the fetcher's verified observations into
 *   data/full-review/rounds/<round>/review-patch.json   every proposed change, per church
 *   data/full-review/rounds/<round>/hold.json          the HOLD items for Chaps QA
 *   data/full-review/rounds/<round>/observations.json  fetcher output incl. page text (git-ignored)
 *   data/full-review/hold-queue.json                   cumulative HOLD queue (sidecar)
 *   docs/data/full-review-stats.json                   one row per round (public dashboard counts)
 *
 * SAFETY GATES (ticket, verbatim intent):
 *  - Every change carries an evidence quote AND a URL, or it is dropped.
 *  - A proposal that moves a church to RED or BLACK, or off GREEN, is HOLD.
 *  - Pastor replacements and other changes auto-apply only at HIGH confidence;
 *    everything else is HOLD.
 *  - Nothing is ever deleted. Duplicates and wrong-church data are flagged to
 *    HOLD for the existing merge tooling (scripts/merge-duplicate-churches.js).
 *
 * Usage:
 *   node scripts/full-review-build-patch.js --input obs.json --round <id> [--out docs/data/full-review] [--dry-run]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { looksFemaleFirstName } = require('./lib/female-first-names.js');
const { isPlaceholderPastor } = require('./lib/grind-lanes.js');
const { denomPrior, AFFILIATION_RE, METHODOLOGY_URL, METHODOLOGY_QUOTE } = require('./lib/denomination-priors.js');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const ROOT = path.join(__dirname, '..');
const CHURCHES = process.env.FULL_REVIEW_CHURCHES_PATH || path.join(ROOT, 'docs', 'data', 'churches.json');
const INPUT = opt('--input', null);
// Working files live OUTSIDE docs/ (docs/ is the public site): unreviewed RED/BLACK
// proposals and cached page text must not publish. Only the counts in
// docs/data/full-review-stats.json are public (the grind-report dashboard).
const OUT = path.resolve(opt('--out', path.join(ROOT, 'data', 'full-review')));
const STATS = path.resolve(opt('--stats', path.join(ROOT, 'docs', 'data', 'full-review-stats.json')));
const DRY = args.includes('--dry-run');
// Local (Eastern) calendar date, not UTC — a 10 pm round must not stamp tomorrow.
const TODAY = new Date().toLocaleDateString('en-CA');
const ROUND = opt('--round', 'fr-' + new Date().toISOString().replace(/[-:]/g, '').slice(0, 13));
if (!INPUT) { console.error('usage: --input <observations.json> [--round id] [--out dir] [--dry-run]'); process.exit(2); }

const sha256 = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const SHA_BEFORE = sha256(CHURCHES);
const all = JSON.parse(fs.readFileSync(CHURCHES, 'utf8')).churches.filter(c => c && c.id);
const byId = new Map(all.map(c => [c.id, c]));
const obsFile = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const observations = obsFile.observations || obsFile;

const SEV = { green: 0, yellow: 1, red: 2, black: 3 };
const DIMS = ['scripture', 'christology', 'gender', 'soteriology', 'preaching', 'cultural', 'leadership', 'mission', 'mens_discipleship', 'denominational'];
const LABEL = { scripture: 'Scripture', christology: 'Christology', gender: 'Gender', soteriology: 'Soteriology', preaching: 'Preaching', cultural: 'Cultural', leadership: 'Leadership', mission: 'Mission', mens_discipleship: "Men's discipleship", denominational: 'Accountability' };
const nrm = s => String(s || '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim().toLowerCase();
const clip = (s, n = 240) => { s = String(s || '').trim(); return s.length > n ? s.slice(0, n - 1) + '…' : s; };
const hostOf = u => { try { return new URL(u).hostname.replace(/^www\./, '').toLowerCase(); } catch (_) { return null; } };
const urlPath = u => { try { return new URL(u).pathname.replace(/\/+$/, '').toLowerCase(); } catch (_) { return String(u || '').toLowerCase(); } };
const pageUrl = id =>`https://usmcmin.org/churches/${id}.html`;

// Names: compare on surname + first initial, titles stripped.
const TITLE_RE = /\b(the|rev|reverend|very|right|dr|pastor|fr|father|mother|elder|bishop|rector|senior|lead|associate|interim|mr|mrs|ms|jr|sr|ii|iii|op|o\.p\.a?|d\.?min|ph\.?d|m\.?div)\b\.?/gi;
const nameKey = n => {
  const t = String(n || '').replace(/\(.*?\)/g, ' ').replace(TITLE_RE, ' ').replace(/[^A-Za-z' -]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase().split(' ').filter(Boolean);
  return t.length ? { first: t[0][0], last: t[t.length - 1], full: t.join(' ') } : null;
};
const sameName = (a, b) => { const x = nameKey(a), y = nameKey(b); return !!(x && y && x.last === y.last && x.first === y.first); };
const LEAD_ROLE = /senior|lead|rector|priest[- ]in[- ]charge|vicar|^pastor$|^the pastor|head pastor|sole pastor|minister$|senior minister|pastor\/teacher|^pastor\b(?!.*(youth|children|kids|student|worship|music|care|family|women|outreach|executive|associate|assistant))/i;
const NONLEAD_ROLE = /youth|kids|children|students|worship|music|executive|associate|assistant|admin|outreach|discipleship|family|women|care|counseling|education|operations|deacon|emerit|retired|interim|supply/i;
const PASTORAL_ROLE = /pastor|priest|rector|vicar|elder|minister|reverend|\brev\b|curate|chaplain/i;

// ── duplicate indexes (whole directory, read-only) ───────────────────────────
const GENERIC_HOSTS = /^(facebook\.com|m\.facebook\.com|youtube\.com|instagram\.com|sites\.google\.com|google\.com|linktr\.ee|umc\.org|episcopalassetmap\.org|churches\.sbc\.net|yelp\.com|wixsite\.com|squarespace\.com)$/;
const addrKey = c => {
  const a = String(c.address || '');
  const m = a.match(/^\s*(\d{1,6})\s+([A-Za-z]+)/), z = a.match(/\b(\d{5})(?:-\d{4})?\b(?!.*\b\d{5}\b)/);
  return m && z ? `${m[1]}|${m[2].toLowerCase()}|${z[1]}` : null;
};
const byAddr = new Map(), byHost = new Map();
for (const c of all) {
  const k = addrKey(c); if (k) (byAddr.get(k) || byAddr.set(k, []).get(k)).push(c.id);
  const h = hostOf(c.website); if (h && !GENERIC_HOSTS.test(h)) (byHost.get(h) || byHost.set(h, []).get(h)).push(c.id);
}

// ── evidence helpers ─────────────────────────────────────────────────────────
const ev = (quote, url, extra = {}) => (quote && url ? { quote: clip(quote, 300), url, ...extra } : null);
// "Women's Bible Study" must never count as a men's ministry: re-check each
// stored hit with a word boundary (fetcher regex fixed too; this guards old obs).
const SIGNAL_GUARD = { mens_ministry: /(^|[^A-Za-z])(men'?s|brotherhood|united methodist men|episcopal church men|men of|man church)/i };
function firstSignal(o, key) {
  const s = ((o.signals || {})[key] || []).filter(h => !SIGNAL_GUARD[key] || SIGNAL_GUARD[key].test(String(h.quote).replace(/women'?s/gi, ' ')));
  return s.length ? s[0] : null;
}
function pagesText(o) { return (o.pages || []).map(p => ({ url: p.url, norm: nrm(p.text || '') })); }
// Verbatim window of page text around a name (word-bounded), for roster evidence.
function around(o, name, url) {
  const p = (o.pages || []).find(x => x.url === url && x.text) || (o.pages || []).find(x => x.text && x.text.includes(name));
  if (!p) return null;
  const i = p.text.indexOf(name);
  if (i < 0) return null;
  let a = Math.max(0, i - 60), b = Math.min(p.text.length, i + name.length + 100);
  while (a > 0 && /\S/.test(p.text[a - 1])) a--;
  while (b < p.text.length && /\S/.test(p.text[b])) b++;
  return { quote: p.text.slice(a, b).trim(), url: p.url };
}
function onPages(o, needle) { const n = nrm(needle); return n.length > 3 && pagesText(o).some(p => p.norm.includes(n)); }

// ── per-church review ────────────────────────────────────────────────────────
function review(o) {
  const c = byId.get(o.id);
  const out = { id: o.id, name: o.name, page: pageUrl(o.id), selection_tier: o.selection_tier || null, status: o.status,
    source_kind: o.source_kind, site_read: o.final_url || null, pages_read: (o.pages || []).map(p => p.url),
    identity: o.identity ? { status: o.identity.status, matched: o.identity.matched, conflicting: o.identity.conflicting_locations || [] } : null,
    current: c ? { pastor: c.pastor || '', overall_rating: c.overall_rating || null, overall_label: c.overall_label || null } : null,
    changes: [], flags: [], rubric: {}, proposed_overall: null };
  if (!c) { out.status = 'missing_from_directory'; return out; }
  const add = ch => { if (ch.evidence && ch.evidence.quote && ch.evidence.url) out.changes.push(ch); };
  const holdAll = [];
  // A site that answered 200 but yielded no readable text is JS-rendered, not dead.
  if (o.status === 'unreachable' && (o.attempts || []).some(a => a.status === 200)) out.status = o.status = 'unreadable';
  if (o.website_is_social) {
    const k = /youtu/i.test(o.website_is_social) ? 'youtube' : /instagram/i.test(o.website_is_social) ? 'instagram' : 'facebook';
    add({ field: 'website', op: 'replace', old: c.website, new: '', confidence: 'medium', hold_reasons: ['website field holds a social URL'],
      reason: `website field is a ${k} URL; move it to ${k}`, evidence: ev(c.website, c.website, { evidence_type: 'stored_value' }),
      also_sets: c[k] ? null : { [k]: o.website_is_social } });
  }

  if (o.status === 'unreachable' || o.status === 'unreadable') {
    out.flags.push({ type: o.status === 'unreadable' ? 'site_unreadable_js' : 'site_unreachable', detail: (o.attempts || []).map(a => `${a.url} -> ${a.status}`).slice(0, 3).join('; '),
      gate: 'info', note: 'No change proposed. A dead site is not a doctrinal flag (methodology §III).' });
  }

  // Wrong-church data: everything read from this site describes someone else.
  let L = o.llm || {}, src = o, siteHost = hostOf(o.final_url || '');
  if (o.status === 'identity_mismatch') {
    const conf = (o.identity.conflicting_locations || [])[0];
    const e = ev(conf && conf.quote, conf && conf.url);
    out.flags.push({ type: 'data_belongs_to_other_church', gate: 'hold', evidence: e,
      detail: `Stored website ${c.website} describes a congregation outside ${o.identity.stored.city}, ${o.identity.stored.state}; nothing on it names the stored city, street or ZIP.` });
    const rec = o.recovery || {};
    const recovered = rec.site && rec.review && (rec.review.identity || {}).status === 'confirmed' ? rec.review : null;
    add({ field: 'website', op: recovered ? 'replace' : 'research', old: c.website || null, new: recovered ? rec.site : null,
      confidence: 'low', reason: recovered ? `local search found a site naming ${o.identity.stored.city}` : 'stored site is another church; real site not found by local search',
      evidence: e, evidence_more: recovered ? [{ quote: (rec.review.identity.matched || []).join(', '), url: rec.site }] : [{ quote: `search: ${rec.query || 'n/a'}`, url: 'http://127.0.0.1:8888 (SearXNG, local)' }] });
    holdAll.push('identity_mismatch');
    // Stored pastor/roster that came off the wrong site.
    const wrongLead = L.lead_pastor;
    if (c.pastor && !isPlaceholderPastor(c.pastor) && onPages(o, nameKey(c.pastor) ? c.pastor.replace(/\(.*?\)/g, '').trim() : '')) {
      const q = wrongLead && sameName(wrongLead.name, c.pastor) ? (wrongLead.quote || wrongLead.name) : c.pastor;
      const u = wrongLead && sameName(wrongLead.name, c.pastor) ? wrongLead.url : (o.pages[0] || {}).url;
      add({ field: 'pastor', op: 'clear', old: c.pastor, new: '', confidence: 'medium', reason: 'stored pastor is listed on the other church\'s site', evidence: ev(q, u), evidence_more: e ? [e] : [] });
      if (Array.isArray(c.pastors) && c.pastors.length) add({ field: 'pastors', op: 'clear', old: c.pastors, new: [], confidence: 'medium', reason: 'roster came from the other church\'s site', evidence: ev(q, u) });
    }
    if (!recovered) { finishGates(out, c, holdAll); dupFlags(out, c, o); return out; }
    L = recovered.llm || {}; src = recovered; siteHost = hostOf(rec.site);
    holdAll.push('recovered_site');
  }
  if (o.status !== 'reviewed' && src === o) { finishGates(out, c, holdAll); dupFlags(out, c, o); return out; }
  if (src.identity && src.identity.status !== 'confirmed') holdAll.push('identity_unconfirmed');

  // ── 1. pastor + roster ────────────────────────────────────────────────────
  const lead = L.lead_pastor;
  let femaleLead = null;
  if (lead && lead.name) {
    const isFemale = lead.pronoun === 'she' || looksFemaleFirstName(lead.name);
    if (isFemale) femaleLead = lead;
    const e = ev(lead.quote || lead.name, lead.url);
    const leadRole = LEAD_ROLE.test(lead.role || '') && !NONLEAD_ROLE.test(lead.role || '');
    if (c.pastor && !isPlaceholderPastor(c.pastor) && sameName(lead.name, c.pastor)) {
      add({ field: 'pastor_source', op: 'confirm', old: c.pastor_source || null, new: lead.url, confidence: 'high', reason: `stored pastor "${c.pastor}" confirmed on the church's own site`, evidence: e });
      add({ field: 'pastor_fetched_at', op: 'confirm', old: c.pastor_fetched_at || null, new: TODAY, confidence: 'high', reason: 'stamp', evidence: e });
    } else {
      const placeholder = isPlaceholderPastor(c.pastor);
      const storedStillListed = !placeholder && onPages(src, (nameKey(c.pastor) || {}).full ? c.pastor.replace(/\(.*?\)/g, '').replace(TITLE_RE, ' ').replace(/\s+/g, ' ').trim() : '');
      const reasons = [];
      if (!lead.quote) reasons.push('no role sentence quoted');
      if (!leadRole) reasons.push(`role "${lead.role || '?'}" not clearly senior/lead`);
      if (isFemale) reasons.push('female senior/lead pastor -> RED minimum; QA');
      if (storedStillListed) reasons.push(`stored "${c.pastor}" still appears on the site`);
      const high = !reasons.length;
      add({ field: 'pastor', op: placeholder ? 'set' : 'replace', old: c.pastor || '', new: lead.name, role: lead.role || null,
        confidence: high ? 'high' : 'medium', reason: high ? (placeholder ? 'lead named verbatim with role on own site' : `stored "${c.pastor}" not on the site; current lead named verbatim with role`) : reasons.join('; '),
        hold_reasons: high ? [] : reasons, evidence: e });
      add({ field: 'pastor_source', op: 'set', old: c.pastor_source || null, new: lead.url, confidence: high ? 'high' : 'medium', hold_reasons: high ? [] : ['rides with pastor change'], reason: 'source of the pastor value', evidence: e, rides_with: 'pastor' });
      add({ field: 'pastor_fetched_at', op: 'set', old: c.pastor_fetched_at || null, new: TODAY, confidence: high ? 'high' : 'medium', hold_reasons: high ? [] : ['rides with pastor change'], reason: 'stamp', evidence: e, rides_with: 'pastor' });
    }
    const roster = (L.roster || []).filter(p => !sameName(p.name, lead.name));
    if (roster.length) {
      const team = [{ name: lead.name, role: (lead.role || 'Lead Pastor').slice(0, 60) }, ...roster.slice(0, 8).map(p => ({ name: p.name, role: (p.role || 'Pastor').slice(0, 60) }))];
      const cur = Array.isArray(c.pastors) ? c.pastors : [];
      const same = cur.length === team.length && cur.every((p, i) => sameName(p.name, team[i].name));
      // Evidence is a verbatim window around each listed name (one per member).
      const wins = roster.slice(0, 8).map(p => around(src, p.name, p.url)).filter(Boolean);
      if (!same && wins.length) add({ field: 'pastors', op: cur.length ? 'replace' : 'set', old: cur, new: team, confidence: 'medium', reason: 'roster as listed on the church site', hold_reasons: [], evidence: ev(wins[0].quote, wins[0].url), evidence_more: wins.slice(1), rides_with: 'pastor' });
    }
  }

  // ── 2. rubric ─────────────────────────────────────────────────────────────
  const cand = Object.fromEntries(DIMS.map(d => [d, []]));
  const put = (dims, rating, strength, basis, e) => { if (!e) return; for (const d of dims) cand[d].push({ rating, strength, basis, evidence: e }); };
  const sig = k => firstSignal(src, k);
  const lgbt = L.lgbt_affirming || sig('lgbt_affirming');
  if (lgbt) put(['gender', 'cultural'], 'black', 3, 'LGBT-affirming statement on the church\'s own site', ev(lgbt.quote, lgbt.url));
  if (femaleLead) put(['gender', 'leadership'], 'red', 3, `female senior/lead pastor (${femaleLead.name})`, ev(femaleLead.quote || femaleLead.name, femaleLead.url));
  const womenRoster = (L.roster || []).find(p => PASTORAL_ROLE.test(p.role || '') && !/deacon/i.test(p.role || '') && looksFemaleFirstName(p.name));
  const rosterQuote = womenRoster ? (around(src, womenRoster.name, womenRoster.url) || { quote: womenRoster.name, url: womenRoster.url }) : null;
  const women = L.women_in_office || sig('women_ordained') || (womenRoster ? { ...rosterQuote, role: womenRoster.role } : null);
  if (women) put(['gender', 'leadership'], 'red', 3, womenRoster && women.role ? `woman listed in pastoral office (${womenRoster.name}, ${womenRoster.role})` : 'women in pastoral/elder office', ev(women.quote, women.url));
  const comp = L.complementarian || sig('complementarian');
  if (comp) put(['gender', 'leadership'], 'green', 2, 'pastor/elder office limited to men', ev(comp.quote, comp.url));
  const conf = L.confession || sig('confession');
  if (conf) {
    const nm = conf.name || conf.match || 'confession';
    put(['scripture', 'soteriology', 'christology'], 'green', 2, `confessional standard (${nm})`, ev(conf.quote, conf.url));
    if (/baptist faith (and|&) message|bf&m/i.test(nm + ' ' + conf.quote) && /2000/.test(nm + ' ' + conf.quote)) put(['gender'], 'green', 2, 'BFM 2000: office of pastor limited to men', ev(conf.quote, conf.url));
  }
  const mens = L.mens_ministry || sig('mens_ministry');
  if (mens) put(['mens_discipleship'], 'green', 2, "men's ministry", ev(mens.quote, mens.url));
  const prosperity = sig('prosperity');
  if (prosperity) put(['cultural'], 'black', 2, 'prosperity-gospel language', ev(prosperity.quote, prosperity.url));
  // Denomination prior — only when the church's OWN site confirms the affiliation.
  const prior = denomPrior(c);
  let priorFired = null;
  if (prior && prior.affirming) {
    const affQuotes = [L.denomination_affiliation, ...(((src.signals || {}).affiliation) || [])].filter(Boolean);
    const rx = AFFILIATION_RE[prior.key];
    const conf2 = rx && affQuotes.find(a => rx.test(a.quote));
    if (conf2) {
      priorFired = { prior, affiliation: conf2 };
      const e = ev(METHODOLOGY_QUOTE, METHODOLOGY_URL, { affiliation_quote: clip(conf2.quote, 200), affiliation_url: conf2.url });
      put(['gender', 'leadership', 'scripture', 'cultural', 'denominational'], 'red', 1.5, `${prior.label} is officially LGBT-affirming (denominational prior; congregation states the affiliation)`, e);
    }
  }
  for (const [d, r] of Object.entries(L.rubric || {})) put([d], r.lean, 1, 'local-model reading of the quoted passage', ev(r.quote, r.url));

  for (const d of DIMS) {
    const list = cand[d];
    if (!list.length) continue;
    const top = Math.max(...list.map(x => x.strength));
    const best = list.filter(x => x.strength === top).sort((a, b) => SEV[b.rating] - SEV[a.rating])[0];
    const curR = (c.scores || {})[d] || null;
    out.rubric[d] = { current: curR, proposed: best.rating, basis: best.basis, strength: best.strength, note: `${LABEL[d]}: ${best.basis} — "${clip(best.evidence.quote, 160)}"`, evidence: best.evidence };
    if (curR !== best.rating) {
      const reasons = [];
      if (SEV[best.rating] >= 2) reasons.push(`category to ${best.rating.toUpperCase()}`);
      if (curR === 'green') reasons.push('category off GREEN');
      if (best.strength < 2) reasons.push(best.strength === 1 ? 'local-model reading only (no deterministic signal)' : 'denominational prior only');
      add({ field: `scores.${d}`, op: curR ? 'replace' : 'set', old: curR, new: best.rating, confidence: reasons.length ? 'medium' : 'high', hold_reasons: reasons, reason: best.basis, evidence: best.evidence, also_sets: { [`score_notes.${d}`]: out.rubric[d].note, [`score_sources.${d}`]: best.evidence.url } });
    }
  }

  // Overall per the legend: black > red > green > yellow.
  const R = d => (out.rubric[d] || {}).proposed || (c.scores || {})[d] || null;
  const strongOf = (d, rating) => (cand[d] || []).some(x => x.rating === rating && x.strength >= 2);
  let rating = 'yellow'; const drivers = []; let ovEvidence = null;
  if (DIMS.some(d => (out.rubric[d] || {}).proposed === 'black')) {
    rating = 'black';
    if (lgbt) { drivers.push('LGBT-affirming statement on parish site'); ovEvidence = ev(lgbt.quote, lgbt.url); }
    if (prosperity) { drivers.push('prosperity-gospel language'); ovEvidence = ovEvidence || ev(prosperity.quote, prosperity.url); }
  } else if (femaleLead || women || (priorFired && !strongOf('gender', 'green'))) {
    rating = 'red';
    if (femaleLead) { drivers.push(`female senior/lead pastor (${femaleLead.name})`); ovEvidence = ev(femaleLead.quote || femaleLead.name, femaleLead.url); }
    else if (women) { drivers.push('women in pastoral/elder office'); ovEvidence = ev(women.quote, women.url); }
  } else if (['gender', 'scripture', 'soteriology'].every(d => R(d) === 'green') && !DIMS.some(d => SEV[R(d)] >= 2)) {
    rating = 'green';
    drivers.push('gender, Scripture and soteriology green with no red category');
    ovEvidence = (conf && ev(conf.quote, conf.url)) || (comp && ev(comp.quote, comp.url)) || (out.rubric.scripture || {}).evidence;
  }
  if (priorFired) { drivers.push(`${priorFired.prior.label} is officially LGBT-affirming`); ovEvidence = ovEvidence || ev(METHODOLOGY_QUOTE, METHODOLOGY_URL); }
  if (femaleLead && rating === 'black') drivers.push(`female senior/lead pastor (${femaleLead.name})`);
  const curO = c.overall_rating || null;
  if (rating !== curO && (rating !== 'yellow' || drivers.length)) {
    const reasons = [];
    if (rating === 'red' || rating === 'black') reasons.push(`moves to ${rating.toUpperCase()}`);
    if (curO === 'green') reasons.push('moves off GREEN');
    if (rating === 'green' && !(conf || comp)) reasons.push('green without a confessional or complementarian statement');
    const label = `${rating.toUpperCase()} — ${drivers.join('; ')}. Evidence: "${clip(ovEvidence && ovEvidence.quote, 140)}" (${ovEvidence && ovEvidence.url}). Full review ${TODAY}.`;
    out.proposed_overall = { current: curO, proposed: rating, label, drivers, evidence: ovEvidence };
    add({ field: 'overall_rating', op: 'replace', old: curO, new: rating, confidence: reasons.length ? 'medium' : 'high', hold_reasons: reasons, reason: drivers.join('; '), evidence: ovEvidence, also_sets: { overall_label: label } });
  } else {
    out.proposed_overall = { current: curO, proposed: curO, label: null, drivers, note: drivers.length ? 'evidence agrees with current rating' : 'no decisive evidence; rating unchanged' };
  }

  // ── 3. profile fill ───────────────────────────────────────────────────────
  const st = L.service_times;
  if (st) {
    const have = c.service_times || (typeof c.services === 'string' ? c.services : '');
    const placeholder = !have || /see website|verify|^sunday morning \(see/i.test(have);
    if (placeholder) add({ field: 'service_times', op: 'fill', old: have || null, new: st.quote, confidence: 'high', reason: 'times quoted from the church site', evidence: ev(st.quote, st.url) });
    else if (nrm(have) !== nrm(st.quote) && !nrm(st.quote).includes(nrm(have).slice(0, 20))) add({ field: 'service_times', op: 'replace', old: have, new: st.quote, confidence: 'medium', hold_reasons: ['replaces existing times'], reason: 'site lists different times', evidence: ev(st.quote, st.url) });
  }
  const fd = L.founded || (sig('founded') ? { quote: sig('founded').quote, url: sig('founded').url, year: +((sig('founded').match.match(/\d{4}/) || [])[0]) } : null);
  if (fd && fd.year) {
    const have = String(c.founded || '');
    if (!have || /see website|unknown|verify/i.test(have)) add({ field: 'founded', op: 'fill', old: have || null, new: String(fd.year), confidence: 'high', reason: 'founding year stated on site', evidence: ev(fd.quote, fd.url) });
    else if (!have.includes(String(fd.year))) add({ field: 'founded', op: 'replace', old: have, new: String(fd.year), confidence: 'medium', hold_reasons: ['replaces existing founded value'], reason: 'site states a different year', evidence: ev(fd.quote, fd.url) });
  }
  for (const [field, q, sigKey] of [['has_mens_ministry', L.mens_ministry, 'mens_ministry'], ['has_kids_ministry', L.kids_ministry, 'kids_ministry']]) {
    const e = q || sig(sigKey);
    if (e && c[field] !== true) add({ field, op: 'set', old: c[field] ?? null, new: true, confidence: 'high', reason: 'ministry named on the church site', evidence: ev(e.quote, e.url) });
  }
  const homeUrl = src.final_url || (src.pages && src.pages[0] && src.pages[0].url);
  for (const k of ['facebook', 'instagram', 'youtube']) {
    const v = (src.socials || {})[k];
    if (!v) continue;
    if (!c[k]) add({ field: k, op: 'fill', old: null, new: v, confidence: 'high', reason: 'link published on the church site', evidence: ev(`<a href="${v}">`, homeUrl, { evidence_type: 'html_link' }) });
    else if (hostOf(c[k]) === hostOf(v) && urlPath(c[k]) !== urlPath(v) && !/facebook\.com\/(people|pages)\//i.test(v)) add({ field: k, op: 'replace', old: c[k], new: v, confidence: 'medium', hold_reasons: ['replaces existing social link'], reason: 'site links a different account', evidence: ev(`<a href="${v}">`, homeUrl, { evidence_type: 'html_link' }) });
  }
  if (src === o && o.final_url && hostOf(o.final_url) && hostOf(c.website) && hostOf(o.final_url) !== hostOf(c.website) && !/wix|squarespace/.test(hostOf(o.final_url))) {
    add({ field: 'website', op: 'replace', old: c.website, new: o.final_url, confidence: 'medium', hold_reasons: ['site redirects to a new domain'], reason: 'stored site redirects here', evidence: ev(`redirect ${c.website} -> ${o.final_url}`, o.final_url, { evidence_type: 'http_redirect' }) });
  }
  // Address: only a full street + ZIP quote that disagrees with the stored one.
  const loc = L.location;
  const ak = addrKey(c);
  if (loc && ak) {
    const m = loc.quote.replace(/(\d)\s+(?=\d)/g, '$1').match(/\b(\d{1,6})\s+([A-Za-z]+)[^]*?\b(\d{5})\b/);
    if (m && `${m[1]}|${m[2].toLowerCase()}|${m[3]}` !== ak && (m[3] !== ak.split('|')[2] || m[1] !== ak.split('|')[0])) {
      add({ field: 'address', op: 'replace', old: c.address, new: clip(loc.quote, 160), confidence: 'medium', hold_reasons: ['address correction (re-geocode after approval)'], reason: 'site gives a different street address/ZIP', evidence: ev(loc.quote, loc.url) });
    }
  }

  finishGates(out, c, holdAll);
  dupFlags(out, c, src);
  return out;
}

// ── duplicates (flag only; merge is the existing tool's job) ─────────────────
function dupFlags(out, c, o) {
  const seen = new Set();
  const k = addrKey(c);
  for (const other of (k && byAddr.get(k)) || []) {
    if (other === c.id || seen.has(other)) continue;
    seen.add(other);
    const oc = byId.get(other);
    out.flags.push({ type: 'possible_duplicate', basis: 'same street address + ZIP', other_id: other, gate: 'hold',
      evidence: ev(oc.address, pageUrl(other), { this_address: c.address }),
      action: 'QA: confirm same congregation, then merge with scripts/merge-duplicate-churches.js (never delete; merged_from + redirect stub).' });
  }
  for (const h of [hostOf(c.website), hostOf(o && o.final_url)].filter(x => x && !GENERIC_HOSTS.test(x))) {
    for (const other of byHost.get(h) || []) {
      if (other === c.id || seen.has(other)) continue;
      seen.add(other);
      const oc = byId.get(other);
      out.flags.push({ type: 'possible_duplicate', basis: 'same website host', other_id: other, gate: 'hold',
        evidence: ev(oc.website, pageUrl(other), { this_website: c.website }),
        action: 'QA: same church (merge with scripts/merge-duplicate-churches.js) or a shared/borrowed site (fix the wrong record).' });
    }
  }
}

// ── gates ────────────────────────────────────────────────────────────────────
function finishGates(out, c, holdAll) {
  // A church whose overall rating is held holds its rubric changes with it.
  const ov = out.changes.find(x => x.field === 'overall_rating');
  const ovHeld = ov && ((ov.hold_reasons || []).length || ov.confidence !== 'high' || holdAll.length);
  const pastorCh = out.changes.find(x => x.field === 'pastor');
  const pastorHeld = pastorCh && ((pastorCh.hold_reasons || []).length || pastorCh.confidence !== 'high' || holdAll.length);
  for (const ch of out.changes) {
    const reasons = [...(ch.hold_reasons || []), ...holdAll];
    if (ch.field.startsWith('scores.') && ovHeld) reasons.push('rides with held overall rating');
    if (ch.rides_with === 'pastor' && pastorHeld) reasons.push('rides with held pastor change');
    if (ch.confidence !== 'high' && !reasons.length) reasons.push(`${ch.confidence} confidence`);
    ch.hold_reasons = [...new Set(reasons)];
    ch.gate = ch.hold_reasons.length ? 'hold' : 'auto';
    delete ch.rides_with;
  }
  // Last line of defence: no quote or no URL = no change.
  out.changes = out.changes.filter(ch => ch.evidence && ch.evidence.quote && ch.evidence.url);
  out.changes.forEach((ch, i) => { ch.change_id = `${ROUND}:${out.id}:${i + 1}`; });
}

// ── run ──────────────────────────────────────────────────────────────────────
const results = observations.map(review);
const holds = [];
for (const r of results) {
  for (const ch of r.changes.filter(x => x.gate === 'hold')) {
    holds.push({ hold_id: ch.change_id, round: ROUND, dry_run: DRY, church_id: r.id, church_name: r.name, page: r.page, kind: 'change',
      field: ch.field, old: ch.old, new: ch.new, also_sets: ch.also_sets || null, hold_reasons: ch.hold_reasons, reason: ch.reason,
      evidence: ch.evidence, evidence_more: ch.evidence_more || [], qa_status: 'pending', qa_by: null, qa_note: null });
  }
  for (const [i, f] of r.flags.filter(x => x.gate === 'hold').entries()) {
    holds.push({ hold_id: `${ROUND}:${r.id}:flag${i + 1}`, round: ROUND, dry_run: DRY, church_id: r.id, church_name: r.name, page: r.page, kind: 'flag',
      field: null, flag: f.type, other_id: f.other_id || null, detail: f.detail || f.basis, action: f.action || null,
      evidence: f.evidence || null, qa_status: 'pending', qa_by: null, qa_note: null });
  }
}
const changedChurches = results.filter(r => r.changes.length);
const summary = {
  reviewed: results.filter(r => r.status === 'reviewed').length,
  identity_mismatch: results.filter(r => r.status === 'identity_mismatch').length,
  unreachable: results.filter(r => r.status === 'unreachable').length,
  unreadable_js: results.filter(r => r.status === 'unreadable').length,
  churches_total: results.length,
  churches_with_changes: changedChurches.length,
  churches_with_auto_changes: results.filter(r => r.changes.some(c => c.gate === 'auto')).length,
  churches_with_holds: new Set(holds.map(h => h.church_id)).size,
  changes_total: results.reduce((a, r) => a + r.changes.length, 0),
  changes_auto: results.reduce((a, r) => a + r.changes.filter(c => c.gate === 'auto').length, 0),
  changes_held: holds.filter(h => h.kind === 'change').length,
  flags_held: holds.filter(h => h.kind === 'flag').length,
  pastor_changes: results.reduce((a, r) => a + r.changes.filter(c => c.field === 'pastor').length, 0),
  overall_changes: results.reduce((a, r) => a + r.changes.filter(c => c.field === 'overall_rating').length, 0),
};
const roundDir = path.join(OUT, 'rounds', ROUND);
fs.mkdirSync(roundDir, { recursive: true });
const SHA_AFTER = sha256(CHURCHES);
const patch = {
  round: ROUND, generated_at: new Date().toISOString(), dry_run: DRY, applied: false,
  model: obsFile.model || null, llm_base: obsFile.llm_base || null, searches_used: obsFile.searches_used ?? null,
  churches_json_sha256: SHA_BEFORE, churches_json_sha256_after_build: SHA_AFTER,
  gates: {
    evidence: 'every change carries evidence.quote + evidence.url; anything without both was dropped',
    hold: 'to RED/BLACK, off GREEN, medium/low confidence, unconfirmed identity, wrong-church data, duplicates',
    auto: 'high confidence only: verbatim quote on the church\'s own identity-confirmed site; fills of empty fields; pastor set/replace with explicit lead role',
  },
  summary, churches: results,
};
fs.writeFileSync(path.join(roundDir, 'review-patch.json'), JSON.stringify(patch, null, 1));
fs.writeFileSync(path.join(roundDir, 'hold.json'), JSON.stringify({ round: ROUND, dry_run: DRY, holds }, null, 1));
fs.copyFileSync(INPUT, path.join(roundDir, 'observations.json'));

// cumulative HOLD queue (sidecar). Re-running a round replaces its own rows.
const QP = path.join(OUT, 'hold-queue.json');
let q = { note: 'Full-review HOLD queue. Chaps QA sets qa_status to approved|rejected (+ qa_by, qa_note). apply-full-review-patch.js applies approved rows only. Rows with dry_run=true came from a dry run and are never applied.', holds: [] };
try { q = JSON.parse(fs.readFileSync(QP, 'utf8')); } catch (_) { }
q.holds = (q.holds || []).filter(h => h.round !== ROUND).concat(holds);
q.updated = new Date().toISOString();
fs.writeFileSync(QP, JSON.stringify(q, null, 1));

// dashboard series
let s = { series: [] };
try { s = JSON.parse(fs.readFileSync(STATS, 'utf8')); } catch (_) { }
s.series = (s.series || []).filter(r => r.round !== ROUND);
s.series.push({ round: ROUND, ts: new Date().toISOString().slice(0, 16), dry_run: DRY, reviewed: summary.churches_total - summary.unreachable - summary.unreadable_js,
  reachable_reviewed: summary.reviewed, identity_mismatch: summary.identity_mismatch, unreachable: summary.unreachable, unreadable_js: summary.unreadable_js,
  changed: summary.churches_with_changes, changes_total: summary.changes_total, auto: summary.changes_auto,
  held: summary.changes_held + summary.flags_held, held_churches: summary.churches_with_holds, applied: 0, applied_holds: 0 });
s.pending_holds = q.holds.filter(h => h.qa_status === 'pending' && !h.dry_run).length;
s.updated = new Date().toISOString();
fs.writeFileSync(STATS, JSON.stringify(s, null, 1));

console.log(`full-review patch ${ROUND}${DRY ? ' (DRY RUN)' : ''}: ${JSON.stringify(summary)}`);
console.log(`  patch: ${path.join(roundDir, 'review-patch.json')}`);
console.log(`  holds: ${path.join(roundDir, 'hold.json')} (${holds.length}) + ${QP}`);
console.log(`  churches.json sha256 ${SHA_BEFORE} -> ${SHA_AFTER} ${SHA_BEFORE === SHA_AFTER ? '(unchanged)' : '(CHANGED — investigate!)'}`);
if (SHA_BEFORE !== SHA_AFTER) process.exit(4);
