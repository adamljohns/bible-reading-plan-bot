#!/usr/bin/env node
// Phase 6f — Apply agent-produced pastor enrichments to churches.json.
//
// Reads one or more /tmp/9marks-pastor-enriched-*.json files, each an array
// of { id, pastor_name, pastor_source_url, website_status }.
// For each enriched record:
//   - If pastor_name is real (not null), set church.pastor = pastor_name,
//     append the source to enrichment_sources, append a note, and CLEAR
//     needs_review if it was solely flagged for missing pastor.
//   - If website_status indicates broken site (404 / timeout / not_a_church),
//     downgrade overall_rating to "red" and keep needs_review=true.
//   - "200_no_pastor_found" → leave as-is (still needs human review).
//
// Usage:
//   node scripts/merge-pastor-enrichments.js                  # auto-discover /tmp/9marks-pastor-enriched-*.json
//   node scripts/merge-pastor-enrichments.js --input <path>   # specific file

const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');

const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

// A pastor field is a PLACEHOLDER (safe to overwrite with a researched name) when it's
// empty, a bare honorific/word, or a "look it up" phrase. A real "Pastor John Smith" is
// NOT a placeholder — the `\bpastor\b` honorific must not match real names.
function isPlaceholderPastor(p) {
  if (!p || !String(p).trim()) return true;
  const s = String(p).trim();
  if (/^(pastors?|tbd|n\/?a|none|unknown|various|staff)\.?$/i.test(s)) return true;
  if (/verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/i.test(s)) return true;
  return false;
}

// ── Junk-name guard (2026-07-03) ─────────────────────────────────────────────
// The regex-scraper era left artifacts like "Chris Bolt Equipping" (name+title
// glued), bare first names ("Tony"), nav fragments ("of our Kids"), and whole
// error notes stuffed into the pastor field. NOTHING that fails these mechanical
// checks may ever be written to church.pastor again, regardless of source
// (Claude agent, local LLM, scraper). Mirrors scripts/fix-junk-pastor-names.js
// and the validator in scripts/local-pastor-extract.py — keep the three in sync.
const MINISTRY_TAIL = /^(equipping|ministries|ministry|worship|connect|missions|discipleship|outreach|groups|media|communications|operations|administration|families|students|children|youth|music|preaching|teaching|counseling|evangelism|education|admin|online|campus|creative|tech|production|next|steps|generations|kids|college|network|resources|giving|generosity|connections|nursery)$/i;
function looksJunkName(name) {
  const s = String(name).trim();
  if (!s || s.length > 32) return true;                       // prose/notes-as-name
  if (/[\n;<>{}|]|https?:/i.test(s)) return true;             // markup / multi-line / URL
  if (/^[a-z]/.test(s)) return true;                          // "of our Kids" — but allow "+Philip Jones" / non-Latin names
  const t = s.split(/\s+/);
  if (t.length < 2 || t.length > 5) return true;              // "Tony", "Vacant", run-on prose
  if (MINISTRY_TAIL.test(t[t.length - 1])) return true;       // "Chris Bolt Equipping"
  if (/^(lead|senior|executive|associate|teaching|campus|interim|worship|youth|assistant|our|the)$/i.test(t[0]) && /^pastors?\.?$/i.test(t[1] || '')) return true; // "Senior Pastor" as a name
  return false;
}

// Conservative female-first-name hold (2026-07-03): the MOOP rubric requires a
// verified female senior/lead pastor to be RED-flagged, but automated extractors
// (especially the local-LLM pipeline) can't reliably judge gender. If the lead
// candidate's first name is on this common-female-names list and the entry does
// NOT already carry pastor_is_female (Claude agents set that flag explicitly),
// HOLD the record for manual review instead of applying. Conservative-only:
// a false positive costs a manual look, never bad published data.
const FEMALE_FIRST = new Set(['mary','patricia','jennifer','linda','elizabeth','barbara','susan','jessica','sarah','karen','lisa','nancy','betty','margaret','sandra','ashley','kimberly','emily','donna','michelle','carol','amanda','dorothy','melissa','deborah','stephanie','rebecca','sharon','laura','cynthia','kathleen','amy','angela','shirley','anna','brenda','pamela','emma','nicole','helen','samantha','katherine','christine','debra','rachel','carolyn','janet','catherine','maria','heather','diane','ruth','julie','olivia','joyce','virginia','victoria','lauren','christina','joan','evelyn','judith','megan','andrea','cheryl','hannah','jacqueline','martha','gloria','teresa','ann','sara','madison','frances','kathryn','janice','jean','abigail','alice','julia','judy','sophia','denise','amber','doris','marilyn','danielle','beverly','isabella','theresa','diana','natalie','brittany','charlotte','kayla','alexis','lori']);
function looksFemaleFirstName(name) {
  const t = String(name).trim().split(/\s+/);
  const first = (t[0] && /^(dr|rev|pastor|fr|bro|mrs|ms|miss)\.?$/i.test(t[0]) ? t[1] : t[0]) || '';
  return FEMALE_FIRST.has(first.toLowerCase().replace(/[^a-z]/g, ''));
}

// Apply a verified social URL only if the church lacks it and the value is a real
// http(s) URL on the expected platform host. Verified-only; never guess.
const SOCIAL_HOST = { facebook: /facebook\.com/i, youtube: /youtube\.com|youtu\.be/i, instagram: /instagram\.com/i };
function applySocials(c, e) {
  let n = 0;
  for (const k of ['facebook', 'youtube', 'instagram']) {
    const v = e[k];
    if (typeof v === 'string' && /^https?:\/\//i.test(v) && SOCIAL_HOST[k].test(v) && !c[k]) {
      c[k] = v.trim();
      n++;
    }
  }
  return n;
}

const args = process.argv.slice(2);
// --social (2026-07-04): social-fill pass. Apply verified social links, mark
// _social_attempted, and do NOT stamp a "no parseable pastor" note (we're not
// hunting pastors here). A pastor found as a bonus still applies via the guards.
const SOCIAL_MODE = args.includes('--social');
let inputs = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--input') inputs.push(args[++i]);
}
if (inputs.length === 0) {
  inputs = fs.readdirSync('/tmp')
    .filter(f => /^9marks-pastor-enriched-\d+\.json$/.test(f))
    .map(f => path.join('/tmp', f));
}

if (!inputs.length) {
  console.error('No enrichment files found. Place at /tmp/9marks-pastor-enriched-N.json or pass --input.');
  process.exit(1);
}

console.log(`Reading ${inputs.length} enrichment files:`);
const enrichments = new Map();
for (const p of inputs) {
  const arr = JSON.parse(fs.readFileSync(p, 'utf8'));
  console.log(`  ${path.basename(p)}: ${arr.length} entries`);
  for (const e of arr) {
    if (e && e.id) enrichments.set(e.id, e);
  }
}
console.log(`Total unique enrichment entries: ${enrichments.size}\n`);

// Byte-format-preserving read+write (ASCII-escaped, no trailing newline) — plain
// JSON.stringify here re-encodes every non-ASCII char into a ~50k-line diff.
const { data: d, write: writeChurches } = makeWriter(CHURCHES);
let pastorsApplied = 0, brokenSites = 0, noPastorFound = 0, idsNotFound = 0, alreadyHasPastor = 0, socialsApplied = 0, femaleSeniorPastors = 0, junkRejected = 0, femaleHeld = 0, rostersApplied = 0;
const stillNeedsReview = [];

for (const c of d.churches) {
  if (!c || !c.id) continue;
  const e = enrichments.get(c.id);
  if (!e) continue;

  // A social-batch member was ATTEMPTED regardless of how the fetch went — stamp it
  // FIRST. (2026-07-17: this stamp used to sit below the website-status `continue`,
  // so dead-site churches at the alphabetical head of the social pool were never
  // stamped, got re-selected every round, and 48 of 52 overnight rounds re-fetched
  // the same 50 dead sites while stacking duplicate timeout notes.)
  if (SOCIAL_MODE) c._social_attempted = TODAY;

  // Track website status — broken websites are NOT a doctrinal red flag
  // (small churches often use Facebook or other social instead of a website).
  // Note the issue + keep needs_review for follow-up social-channel research,
  // but DO NOT downgrade the overall rating.
  if (e.website_status && /404|timeout|ssl_error|redirect_loop|not_a_church/.test(e.website_status)) {
    brokenSites++;
    // One note per distinct verdict — a dead site stays dead; re-observations
    // must not stack duplicate lines (one church collected 8 identical notes).
    const verdictLine = `Phase 6f live-fetch verdict: ${e.website_status}.`;
    if (!String(c.enrichment_notes || '').includes(verdictLine)) {
      const noteAppend = `[${TODAY}] ${verdictLine} Site may be defunct or church may use Facebook/social instead of website. NOT a doctrinal flag — research social channel before publishing.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
    }
    c.needs_review = true;
    continue;
  }

  // Apply any verified social links the agent found (independent of the pastor outcome —
  // a church can have a real FB/YouTube/IG even when no pastor name is parseable).
  const nSocial = applySocials(c, e);
  socialsApplied += nSocial;
  if (SOCIAL_MODE && nSocial) {
    const sNote = `[${TODAY}] Social-fill: added ${nSocial} verified social link(s) from ${c.website || 'church website'}.`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + sNote : sNote;
  }

  if (e.pastor_name && typeof e.pastor_name === 'string' && e.pastor_name.trim()) {
    const candidate = e.pastor_name.trim();

    // Gate 1: mechanical junk check — scraper-artifact shapes never land again.
    if (looksJunkName(candidate)) {
      junkRejected++;
      const jNote = `[${TODAY}] Enrichment guard: rejected junk-looking pastor value "${candidate}" (source: ${e.extractor || 'agent'}). Left unset.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + jNote : jNote;
      c.needs_review = true;
      c._hold_review = TODAY; // exits the automated pools — a re-fetch would re-extract the same junk
      continue;
    }

    // Gate 2: female-first-name hold — apply nothing, queue for manual rubric review.
    if (e.pastor_is_female !== true && looksFemaleFirstName(candidate)) {
      femaleHeld++;
      const fNote = `[${TODAY}] Enrichment guard: lead-pastor candidate "${candidate}" has a typically-female first name — HELD for manual MOOP-rubric review (name not applied). Source: ${e.pastor_source_url || 'n/a'}.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + fNote : fNote;
      c.needs_review = true;
      c._hold_review = TODAY; // exits the automated pools until a human clears the hold (2026-07-11: an unstamped hold pinned pool_fresh=1 and spun the grind for 5 days)
      continue;
    }

    const previouslyVerifyPlaceholder = isPlaceholderPastor(c.pastor);
    if (previouslyVerifyPlaceholder) {
      c.pastor = candidate;
      pastorsApplied++;

      // Multi-pastor roster (2026-07-03): when the researcher also verified other
      // pastors/elders, store the full team as pastors[] — lead first, roles kept.
      // Generator renders them; search haystack + schema.org include them.
      const others = Array.isArray(e.other_pastors) ? e.other_pastors
        .filter(p => p && typeof p.name === 'string' && p.name.trim() && !looksJunkName(p.name.trim()))
        .map(p => ({ name: p.name.trim(), role: (typeof p.role === 'string' && p.role.trim()) ? p.role.trim().slice(0, 60) : 'Pastor' }))
        .slice(0, 8) : [];
      if (others.length) {
        c.pastors = [{ name: candidate, role: (typeof e.pastor_role === 'string' && e.pastor_role.trim()) ? e.pastor_role.trim().slice(0, 60) : 'Lead Pastor' }, ...others];
        rostersApplied++;
      }
      // Rubric enforcement: a verified FEMALE senior/lead pastor is RED minimum on
      // Gender and overall. Enriching the name must not leave a now-known
      // egalitarian church sitting green/yellow. Flag for human confirmation.
      if (e.pastor_is_female === true) {
        c.overall_rating = 'red';
        c.scores = c.scores || {};
        c.scores.gender = 'red';
        c.tags = Array.isArray(c.tags) ? c.tags : [];
        if (!c.tags.includes('needs-rating-review')) c.tags.push('needs-rating-review');
        c.needs_review = true;
        femaleSeniorPastors++;
        const gNote = `[${TODAY}] Female senior/lead pastor identified ("${e.pastor_name}") — auto-set Gender + overall to RED per MOOP rubric; confirm egalitarian polity before publishing.`;
        c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + gNote : gNote;
      }
      if (Array.isArray(c.enrichment_sources)) {
        if (e.pastor_source_url && !c.enrichment_sources.includes(e.pastor_source_url)) {
          c.enrichment_sources.push(e.pastor_source_url);
        }
      } else if (e.pastor_source_url) {
        c.enrichment_sources = [e.pastor_source_url];
      }
      const noteAppend = `[${TODAY}] Phase 6f pastor live-fetched: "${e.pastor_name}" from ${e.pastor_source_url || 'church website'}.${e.extractor ? ` (extractor: ${e.extractor})` : ''}`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
      // Clear needs_review IF it was set solely because pastor was missing.
      // Heuristic: if record was added by Phase 6 networks integrate and now has
      // a real pastor + working website, clear needs_review.
      if (c.needs_review && /Added via .* Phase 2/.test(String(c.enrichment_notes || ''))) {
        c.needs_review = false;
      }
    } else {
      alreadyHasPastor++;
    }
    continue;
  }

  if (e.website_status === '200_no_pastor_found') {
    noPastorFound++;
    // Social-fill pass isn't hunting pastors — don't stamp a no-pastor note (that
    // would wrongly mark the church "pastor-attempted"); the _social_attempted flag
    // set above is the record for this pass.
    if (!SOCIAL_MODE) {
      const noteAppend = `[${TODAY}] Phase 6f live-fetched but no parseable pastor name on standard pages (/about, /staff, /leaders). Site OK.`;
      c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + noteAppend : noteAppend;
      stillNeedsReview.push(c.id);
    }
  }
}

// Sanity: how many enrichment IDs did we NOT find in churches.json?
for (const [id] of enrichments) {
  const c = d.churches.find(c => c && c.id === id);
  if (!c) idsNotFound++;
}

d.directory_updated = TODAY;
writeChurches(d);

console.log('Results:');
console.log(`  Pastors applied:              ${pastorsApplied}`);
console.log(`  Multi-pastor rosters stored:  ${rostersApplied}`);
console.log(`  Social links applied:         ${socialsApplied}`);
console.log(`  Female senior pastor → RED:   ${femaleSeniorPastors}`);
console.log(`  Female-name HELD for review:  ${femaleHeld}`);
console.log(`  Junk names rejected by guard: ${junkRejected}`);
console.log(`  Broken websites noted (rating unchanged): ${brokenSites}`);
console.log(`  No pastor parseable (200_no_pastor_found): ${noPastorFound}`);
console.log(`  Already had real pastor:       ${alreadyHasPastor}`);
console.log(`  Enrichment IDs not found in MOOP: ${idsNotFound}`);
console.log(`  Still needs_review:            ${stillNeedsReview.length}`);
