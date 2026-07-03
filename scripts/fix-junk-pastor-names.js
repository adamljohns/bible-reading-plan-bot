#!/usr/bin/env node
// Reset scraper-artifact pastor names back to honest placeholders.
//
// The regex-scraper era (Phase 6c/6f, May 2026) left values like:
//   "Chris Bolt Equipping"        name + ministry title glued together
//   "Tony" / "Justin" / "Wallie"  bare first names
//   "Vacant" / "Interim"          pulpit-status words as a "name"
//   "Calvary Kids" / "of our Kids" nav fragments
//   "Not named on visible pages; JC Neely is lead pastor at ..." notes-as-name
//
// A wrong name is worse than a blank (MOOP hard rule), so anything matching the
// junk shapes is RESET: pastor -> "", needs_review -> true, and a dated
// `junk-pastor-reset` note quoting the old value. The note re-opens the record
// for research (select-enrichment-batch.js treats a junk-pastor-reset stamped
// after the last Phase-6f attempt as eligible again).
//
// Rules mirror looksJunkName() in merge-pastor-enrichments.js and the validator
// in local-pastor-extract.py — keep the three in sync.
//
// Usage:
//   node scripts/fix-junk-pastor-names.js            # report only (default)
//   node scripts/fix-junk-pastor-names.js --apply    # write the resets
//   node scripts/fix-junk-pastor-names.js --skip id1,id2   # exclude ids

const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);
const APPLY = process.argv.includes('--apply');
const skipIdx = process.argv.indexOf('--skip');
const SKIP = new Set(skipIdx >= 0 && process.argv[skipIdx + 1] ? process.argv[skipIdx + 1].split(',') : []);

const MINISTRY_TAIL = /^(equipping|ministries|ministry|worship|connect|missions|discipleship|outreach|groups|media|communications|operations|administration|families|students|children|youth|music|preaching|teaching|counseling|evangelism|education|admin|online|campus|creative|tech|production|next|steps|generations|kids|college|network|resources|giving|generosity|connections|nursery)$/i;

function isPlaceholderPastor(p) {
  if (!p || !String(p).trim()) return true;
  const s = String(p).trim();
  if (/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)) return true;
  if (/verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s)) return true;
  return false;
}

// Returns a reason string when the value is junk, else null.
//
// ⚠️ CONSERVATIVE BY DESIGN (lesson of 2026-07-03): an earlier draft treated any
// value >32 chars as "prose-as-name" and would have wiped ~1,600 LEGITIMATE rich
// values like "Todd Wagner (Senior Pastor, founder)" or "Rev. Keith M. Dewell
// (M.Div., RPTS)" — real names with parenthetical detail from the 2026-05 manual
// era. A long value is junk ONLY when it is clearly status-prose with NO
// recoverable person in the name position. When in doubt, KEEP the value.
// (This is deliberately looser than looksJunkName() in merge-pastor-enrichments.js:
// that guard vets INCOMING candidates, which must be clean bare names; this tool
// judges EXISTING data, where messy-but-true beats blank.)
function junkReason(name) {
  const s = String(name).trim();
  if (/[\n]/.test(s)) return 'multi-line';
  if (/[<>{}|]|https?:/i.test(s)) return 'markup/URL fragment';
  if (/^[([]/.test(s)) return 'parenthetical status (no name)';
  if (/^(pulpit|vacant|interim|elder-led|unknown|unspecified|not |no |none$|tbd|see |search |contact |outreach |primitive |finding )/i.test(s)) return 'status/meta prose (no name)';
  if (/name not on|not listed|not named|visible pages|serves as pastor|is lead pastor at/i.test(s)) return 'provenance-note-as-name';
  if (/^(lead|senior) pastor \(/i.test(s)) return 'title + parenthetical (no name)';
  // ASCII-lowercase start only: "of our Kids" is junk, but "이명훈 (Myung-hoon Lee)"
  // (Korean) and "+Philip Jones" (Anglican bishop notation) are real names.
  if (/^[a-z]/.test(s)) return 'starts lowercase (nav/prose fragment)';
  const t = s.split(/\s+/);
  if (t.length === 1) return 'single token (first name / status word)';
  // Name+title glued by the scraper ("Chris Bolt Equipping", "Daniel Groff Youth").
  // Only short values WITHOUT a parenthetical — parentheticals mark the legit
  // "Name (Role, since YYYY)" era, which must be left alone.
  if (!s.includes('(') && t.length <= 4 && MINISTRY_TAIL.test(t[t.length - 1])) return 'ministry-word tail (name+title glued)';
  if (t.length === 2 && /^(lead|senior|executive|associate|teaching|campus|interim|worship|youth|assistant|our|the)$/i.test(t[0]) && /^pastors?\.?$/i.test(t[1])) return 'title-as-name';
  return null;
}

const { data: d, write } = makeWriter(CHURCHES);
const hits = [];
for (const c of d.churches) {
  if (!c || !c.id || SKIP.has(String(c.id))) continue;
  const p = String(c.pastor || '').trim();
  if (!p || isPlaceholderPastor(p)) continue;
  const why = junkReason(p);
  if (why) hits.push({ c, old: p, why });
}

console.log(`${APPLY ? 'APPLYING' : 'REPORT (dry run)'} — ${hits.length} junk pastor value(s):`);
for (const h of hits) {
  console.log(`  [${h.why}] ${h.c.id} (${h.c.state || '?'}) -> "${h.old.replace(/\n/g, '\\n').slice(0, 60)}"`);
  if (APPLY) {
    h.c.pastor = '';
    h.c.needs_review = true;
    const note = `[${TODAY}] junk-pastor-reset: cleared scraper artifact "${h.old.replace(/\n/g, ' ').slice(0, 80)}" (${h.why}) — pastor unknown, re-research.`;
    h.c.enrichment_notes = h.c.enrichment_notes ? h.c.enrichment_notes + '\n' + note : note;
  }
}
if (APPLY && hits.length) {
  write(d);
  console.log(`\nWrote ${hits.length} reset(s) to churches.json (format-preserving).`);
} else if (!APPLY) {
  console.log('\nDry run — re-run with --apply to write the resets.');
}
