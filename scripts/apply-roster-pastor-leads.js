#!/usr/bin/env node
/**
 * Apply pastor names from a denominational roster onto churches we already hold
 * but left blank.
 *
 * The name is copied verbatim from the denomination's own roster entry and the
 * exact source URL is recorded, so every write is checkable after the fact. This
 * only ever fills a BLANK: a pastor already on file is never overwritten, because
 * ours may be fresher than the roster and a silent overwrite is unreviewable.
 *
 * Female-lead guard: Adam's rubric puts a female senior pastor at RED minimum, so
 * such a name is HELD for manual review rather than written — the same rule the
 * local grind follows via _hold_review.
 *
 * Report-first; --apply writes. Usage:
 *   node scripts/apply-roster-pastor-leads.js --leads /tmp/sbcv-leads/sbcv-pastor-leads.json [--apply]
 */
const fs = require('fs');
const path = require('path');
const { makeWriter } = require('./lib/format-preserving-write.js');
const ID = require('./lib/church-identity.js');

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const APPLY = args.includes('--apply');
const LEADS = opt('--leads', '');
if (!LEADS) { console.error('--leads <file> required'); process.exit(1); }

const TODAY = new Date().toISOString().slice(0, 10);
const leads = JSON.parse(fs.readFileSync(LEADS, 'utf8'));
const { data: d, write } = makeWriter(path.join(__dirname, '..', 'docs/data/churches.json'));
const byId = new Map(d.churches.map(c => [String(c.id), c]));

// Typically-female given names. Shared intent with merge-pastor-enrichments.js:
// hold, never silently write, and never discard.
const FEMALE_FIRST = /^(mary|linda|patricia|barbara|elizabeth|jennifer|susan|jessica|sarah|karen|nancy|lisa|betty|margaret|sandra|ashley|dorothy|kimberly|emily|donna|michelle|carol|amanda|melissa|deborah|stephanie|rebecca|laura|sharon|cynthia|kathleen|amy|angela|shirley|anna|brenda|pamela|nicole|ruth|katherine|samantha|christine|catherine|virginia|rachel|janet|heather|diane|julie|joyce|victoria|kelly|christina|joan|evelyn|judith|andrea|hannah|megan|cheryl|jacqueline|martha|madison|teresa|gloria|sara|janice|marie|julia|kathryn|grace|judy|theresa|beverly|denise|marilyn|amber|danielle|abigail|brittany|rose|diana|natalie|sophia|alexis|lori|kayla|jane|annemarie|maryann|maryanne|marybeth|jo|jodi|jodie|lynn|lynne|dawn|tracy|tracey|robin|leslie|shannon|erin|holly|crystal|tina|tammy|wendy|stacy|stacey|monica|allison|rhonda|vicki|vickie|bonnie|charlotte|paula|april|kristin|kristen|renee|colleen|tonya|lindsay|lindsey|whitney|courtney|jenna|alicia|felicia|regina|priscilla|phoebe|naomi|esther|miriam|deborah|dianne|suzanne|roberta|marcia|geraldine|josephine|eileen|lorraine|constance|yvonne|claudia|jeanette|kristina|marlene|gwendolyn|sylvia|melinda|jill|erica|tiffany|jasmine|kari|kara|krista)\b/i;

const applied = [], held = [], skipped = [];
for (const L of leads) {
  const c = byId.get(String(L.id));
  if (!c) { skipped.push(`${L.id} — not found`); continue; }
  if (!ID.isPh(c.pastor)) { skipped.push(`${L.id} — pastor already on file (${c.pastor})`); continue; }
  const name = String(L.pastor || '').trim();
  if (!name || name.length < 4) { skipped.push(`${L.id} — no usable name`); continue; }
  // The roster's pastor field is not always a person. SBCV publishes a literal
  // "None" for vacant pulpits and sometimes just the office ("Senior Pastor").
  // Strip role words and require a real first+last remainder, or this writes a
  // job title into the pastor field of a live church page.
  if (ID.isPh(name)) { skipped.push(`${L.id} — roster says "${name}" (vacant/placeholder)`); continue; }
  const bare = name.replace(/\b(senior|lead|leading|associate|assistant|interim|acting|executive|teaching|founding|co)\b/gi, ' ')
    .replace(/\b(rev|reverend|dr|pastor|pastors|elder|minister|bro|brother|mr|mrs|ms|fr|father|bishop|min)\b\.?/gi, ' ')
    .replace(/[^A-Za-z.'\- ]/g, ' ').replace(/\s+/g, ' ').trim();
  if (bare.split(' ').filter(t => t.length > 1).length < 2) {
    skipped.push(`${L.id} — "${name}" is a title, not a name`); continue;
  }
  const first = bare.split(' ')[0];
  if (FEMALE_FIRST.test(first)) { held.push({ id: L.id, name, why: 'typically-female given name -> MOOP rubric review' }); continue; }
  applied.push({ c, L, name });
}

console.log(`${APPLY ? 'APPLYING' : 'DRY RUN'} — ${leads.length} leads: ${applied.length} apply, ${held.length} held, ${skipped.length} skipped\n`);
applied.forEach(a => console.log(`  + ${a.c.id.padEnd(46)} ${a.name}`));
held.forEach(h => console.log(`  ! HELD ${h.id} — ${h.name} (${h.why})`));
if (skipped.length) skipped.slice(0, 10).forEach(s => console.log(`    - ${s}`));

if (APPLY && (applied.length || held.length)) {
  for (const a of applied) {
    a.c.pastor = a.name;
    const note = `[${TODAY}] Pastor "${a.name}" from ${a.L.source} roster entry ${a.L.evidence_url} (verbatim; matched on ${(a.L.match_evidence || []).join('+')}).`;
    a.c.enrichment_notes = a.c.enrichment_notes ? `${a.c.enrichment_notes}\n${note}` : note;
    if (!Array.isArray(a.c.enrichment_sources)) a.c.enrichment_sources = [];
    if (a.L.evidence_url && !a.c.enrichment_sources.includes(a.L.evidence_url)) a.c.enrichment_sources.push(a.L.evidence_url);
  }
  for (const h of held) {
    const c = byId.get(String(h.id));
    if (!c) continue;
    c._hold_review = `${TODAY}: roster names "${h.name}" — ${h.why}`;
  }
  write(d);
  console.log(`\nWrote ${applied.length} pastors, ${held.length} holds.`);
} else if (!APPLY) {
  console.log('\nDry run — re-run with --apply to write.');
}
