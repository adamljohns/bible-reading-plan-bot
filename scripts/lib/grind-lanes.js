#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const AB = new Set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' '));
const FULL = new Set(['ALABAMA','ALASKA','ARIZONA','ARKANSAS','CALIFORNIA','COLORADO','CONNECTICUT','DELAWARE','FLORIDA','GEORGIA','HAWAII','IDAHO','ILLINOIS','INDIANA','IOWA','KANSAS','KENTUCKY','LOUISIANA','MAINE','MARYLAND','MASSACHUSETTS','MICHIGAN','MINNESOTA','MISSISSIPPI','MISSOURI','MONTANA','NEBRASKA','NEVADA','NEW HAMPSHIRE','NEW JERSEY','NEW MEXICO','NEW YORK','NORTH CAROLINA','NORTH DAKOTA','OHIO','OKLAHOMA','OREGON','PENNSYLVANIA','RHODE ISLAND','SOUTH CAROLINA','SOUTH DAKOTA','TENNESSEE','TEXAS','UTAH','VERMONT','VIRGINIA','WASHINGTON','WEST VIRGINIA','WISCONSIN','WYOMING']);

const APPLY_LANES = ['fresh', 'retry', 'social'];
const EMPTY_STREAK_SKIP = 3;

function isPlaceholderPastor(p) {
  const s = String(p || '').trim();
  return !s || /^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s) ||
    /verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s);
}
function isUS(c) {
  const s = String(c.state || '').toUpperCase().trim();
  return AB.has(s) || FULL.has(s);
}
const isEnglish = n => typeof n === 'string' && !/[^\x00-\x7F]/.test(n);
const hasWebsite = c => typeof c.website === 'string' && /^https?:\/\/[^/\s]/i.test(c.website);
const notesText = c => Array.isArray(c.enrichment_notes) ? c.enrichment_notes.join(' ') : String(c.enrichment_notes || '');
function alreadyAttempted(c) {
  const n = notesText(c);
  if (n.lastIndexOf('junk-pastor-reset') > n.lastIndexOf('Phase 6f')) return false;
  return !!c._loop_round_attempted || !!c._verify_round_attempted || /Phase 6f/i.test(n);
}
const noPastorStrikes = c => (notesText(c).match(/no parseable pastor/gi) || []).length;
const pastorFetchable = c => isPlaceholderPastor(c.pastor) && hasWebsite(c) && !c._dead_site && isEnglish(c.name) && isUS(c);
const freshEligible = c => pastorFetchable(c) && !c._hold_review && !alreadyAttempted(c);
const retryEligible = c => pastorFetchable(c) && !c._hold_review && alreadyAttempted(c) && noPastorStrikes(c) === 1;
const socialEligible = c => hasWebsite(c) && !c.facebook && !c.youtube && !c.instagram &&
  isEnglish(c.name) && isUS(c) && !c._social_attempted && !c._social_scraped;
const websiteDiscoveryEligible = c => !hasWebsite(c) && isEnglish(c.name) && isUS(c) && !c._website_searched &&
  !String(c.source_url || '').includes('churches.sbc.net');
const isSbcSource = c => { try { return new URL(String(c.source_url || '')).hostname === 'churches.sbc.net'; } catch (_) { return false; } };
const sourceRecoveryEligible = c => isSbcSource(c) &&
  (!hasWebsite(c) || typeof c.latitude !== 'number' || typeof c.longitude !== 'number') && !c.sbc_detail_fetched_at &&
  Number(c._sbc_detail_failures || 0) < 3;
const sourceRecoveryExhausted = c => isSbcSource(c) &&
  (!hasWebsite(c) || typeof c.latitude !== 'number' || typeof c.longitude !== 'number') && !c.sbc_detail_fetched_at &&
  Number(c._sbc_detail_failures || 0) >= 3;
const pastorExhausted = c => pastorFetchable(c) && !c._hold_review && alreadyAttempted(c) && noPastorStrikes(c) >= 2;

function grindStatsPath(root) {
  return path.join(root || path.join(__dirname, '..', '..'), 'docs/data/grind-stats.json');
}

function defaultEmptyStreaks() {
  return { fresh: 0, retry: 0, social: 0 };
}

function streakStorePath() {
  return process.env.GRIND_STREAK_STORE ||
    path.join(process.env.HOME || '', 'Library/Logs/grind-lane-empty-streaks.json');
}

function loadEmptyStreaks(root) {
  if (process.env.GRIND_EMPTY_STREAKS) {
    try {
      return { ...defaultEmptyStreaks(), ...JSON.parse(process.env.GRIND_EMPTY_STREAKS) };
    } catch (_) { /* fall through */ }
  }
  try {
    const j = JSON.parse(fs.readFileSync(streakStorePath(), 'utf8'));
    return { ...defaultEmptyStreaks(), ...j };
  } catch (_) { /* fall through */ }
  try {
    const j = JSON.parse(fs.readFileSync(grindStatsPath(root), 'utf8'));
    return { ...defaultEmptyStreaks(), ...(j.lane_empty_streaks || {}) };
  } catch (_) {
    return defaultEmptyStreaks();
  }
}

function persistEmptyStreaks(streaks, root) {
  fs.mkdirSync(path.dirname(streakStorePath()), { recursive: true });
  fs.writeFileSync(streakStorePath(), JSON.stringify({ ...defaultEmptyStreaks(), ...streaks }, null, 1));
  try {
    const P = grindStatsPath(root);
    let j = { series: [] };
    try { j = JSON.parse(fs.readFileSync(P, 'utf8')); } catch (_) { /* new file */ }
    j.lane_empty_streaks = { ...defaultEmptyStreaks(), ...streaks };
    fs.writeFileSync(P, JSON.stringify(j, null, 1));
  } catch (_) { /* grind-stats mirror is best-effort */ }
}

function isApplyLaneCold(lane, streaks) {
  return (streaks[lane] || 0) >= EMPTY_STREAK_SKIP;
}

function recordLaneHop(lane, appliedCount, root) {
  if (!APPLY_LANES.includes(lane)) return loadEmptyStreaks(root);
  const streaks = loadEmptyStreaks(root);
  if (appliedCount > 0) streaks[lane] = 0;
  else streaks[lane] = (streaks[lane] || 0) + 1;
  persistEmptyStreaks(streaks, root);
  return streaks;
}

function countLanes(churches) {
  const unresolved = new Set();
  const count = predicate => churches.filter(predicate).length;
  churches.forEach(c => {
    if (freshEligible(c) || retryEligible(c) || socialEligible(c) || websiteDiscoveryEligible(c) || sourceRecoveryEligible(c) || sourceRecoveryExhausted(c) || pastorExhausted(c) || c._dead_site || c.needs_review === true || c._hold_review) {
      unresolved.add(String(c.id || c.slug));
    }
  });
  return {
    fresh: count(freshEligible),
    retry: count(retryEligible),
    social: count(socialEligible),
    website_discovery: count(websiteDiscoveryEligible),
    source_recovery: count(sourceRecoveryEligible),
    source_recovery_exhausted: count(sourceRecoveryExhausted),
    pastor_exhausted: count(pastorExhausted),
    dead_site_recovery: count(c => !!c._dead_site),
    human_review: count(c => c.needs_review === true || !!c._hold_review || sourceRecoveryExhausted(c)),
    product_backlog: unresolved.size,
  };
}

function chooseLane(counts, lastMode, streaksIn) {
  const streaks = streaksIn || loadEmptyStreaks();
  const applyOrder = [
    ['fresh', counts.fresh],
    ['retry', counts.retry],
    ['social', counts.social],
  ];
  for (const [lane, n] of applyOrder) {
    if (n > 0 && !isApplyLaneCold(lane, streaks)) return lane;
  }
  // Cold apply lanes fall through. Do not delete retry/social; just stop
  // selecting them after EMPTY_STREAK_SKIP consecutive empties.
  if (counts.source_recovery > 0) return 'source-recovery';
  const anyApplyEligible = applyOrder.some(([, n]) => n > 0);
  if (anyApplyEligible) return 'nothing-to-grind';
  return 'monitoring';
}

module.exports = {
  APPLY_LANES, EMPTY_STREAK_SKIP,
  isPlaceholderPastor, isUS, isEnglish, hasWebsite, notesText, alreadyAttempted,
  noPastorStrikes, pastorFetchable, freshEligible, retryEligible, socialEligible,
  websiteDiscoveryEligible, isSbcSource, sourceRecoveryEligible, sourceRecoveryExhausted, pastorExhausted,
  countLanes, chooseLane, loadEmptyStreaks, persistEmptyStreaks, recordLaneHop, isApplyLaneCold,
};
