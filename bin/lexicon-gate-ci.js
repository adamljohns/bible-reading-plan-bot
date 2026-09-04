#!/usr/bin/env node
/**
 * CI ratchet around bin/lexicon-gate.js.
 *
 * The gate itself is all-or-nothing: 4,460 of 7,878 lexicon pages fail it
 * today, so wiring `--all` straight into the deploy would fail every build,
 * and a gate that fails every build gets deleted. Governance rule 7 --
 * silencing is not fixing -- so instead this ratchets.
 *
 * A baseline file records the pages already known to fail. This step fails the
 * deploy only when a page fails that is NOT in the baseline: new fabrication
 * cannot ship, while the existing backlog burns down without blocking anyone.
 * Same shape as the approval gate's "fails only on a NEW breach".
 *
 * Governance rule 6: a gate that examined nothing has not passed. If zero
 * pages get checked, or the baseline is missing, this exits non-zero.
 *
 *   node bin/lexicon-gate-ci.js                    # CI mode
 *   node bin/lexicon-gate-ci.js --update-baseline  # after a deliberate change
 */
const fs = require('fs');
const path = require('path');
const { checkPage } = require('./lexicon-gate.js');

const REPO = path.dirname(__dirname);
const LEX = path.join(REPO, 'docs', 'lexicon');
const BASELINE = path.join(REPO, 'bin', 'baselines', 'lexicon-failures.txt');

function currentFailures() {
  if (!fs.existsSync(LEX)) {
    console.error(`FAIL: ${LEX} does not exist — nothing was checked.`);
    process.exit(2);
  }
  const files = fs.readdirSync(LEX).filter((f) => f.endsWith('.html')).sort();
  const failing = [];
  files.forEach((f) => {
    const r = checkPage(path.join(LEX, f));
    if (r.fails.length) failing.push(`docs/lexicon/${f}`);
  });
  return { checked: files.length, failing };
}

function main() {
  const update = process.argv.includes('--update-baseline');
  const { checked, failing } = currentFailures();

  // Rule 6: examining nothing is not a pass.
  if (checked === 0) {
    console.error('FAIL: 0 lexicon pages checked. A gate that examines nothing has not passed.');
    process.exit(2);
  }

  if (update) {
    fs.mkdirSync(path.dirname(BASELINE), { recursive: true });
    fs.writeFileSync(BASELINE,
      `# Lexicon pages known to fail bin/lexicon-gate.js.\n` +
      `# The CI ratchet (bin/lexicon-gate-ci.js) fails the deploy on any page\n` +
      `# failing that is NOT listed here. Shrink this file; never grow it.\n` +
      `# Regenerate deliberately: node bin/lexicon-gate-ci.js --update-baseline\n` +
      `# Updated: ${new Date().toISOString().slice(0, 10)} — ${failing.length} of ${checked} pages.\n` +
      failing.join('\n') + '\n');
    console.log(`baseline written: ${failing.length} known failures of ${checked} pages checked`);
    return;
  }

  if (!fs.existsSync(BASELINE)) {
    console.error(`FAIL: baseline missing at ${BASELINE}.`);
    console.error('Create it deliberately: node bin/lexicon-gate-ci.js --update-baseline');
    process.exit(2);
  }

  const baseline = new Set(
    fs.readFileSync(BASELINE, 'utf8').split('\n')
      .map((l) => l.trim()).filter((l) => l && !l.startsWith('#'))
  );
  const novel = failing.filter((f) => !baseline.has(f));
  const fixed = [...baseline].filter((f) => !failing.includes(f));

  console.log(`Lexicon ratchet: ${checked} pages checked, ${failing.length} failing, ` +
              `${baseline.size} in baseline.`);
  if (fixed.length) {
    console.log(`  ${fixed.length} baseline page(s) now pass — prune them:`);
    console.log('    node bin/lexicon-gate-ci.js --update-baseline');
  }
  if (novel.length) {
    console.error(`\nFAIL: ${novel.length} lexicon page(s) newly fail the gate:`);
    novel.slice(0, 25).forEach((f) => {
      const r = checkPage(path.join(REPO, f));
      console.error(`  ${f}`);
      r.fails.slice(0, 3).forEach((x) => console.error(`      ✗ ${x}`));
    });
    if (novel.length > 25) console.error(`  ...and ${novel.length - 25} more`);
    console.error('\nFix the page, or if this is deliberate, update the baseline explicitly.');
    process.exit(1);
  }
  console.log('PASS: no new lexicon failures.');
}

main();
