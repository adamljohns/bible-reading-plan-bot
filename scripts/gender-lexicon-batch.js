#!/usr/bin/env node
/**
 * CCW-0831-GENDER — batch relabel Strong Reformed Baptist gender notes.
 * "complementarian" is a feminism halfway house; Strong RB → Scriptural patriarchy /
 * biblical manhood / Christlike headship. See workspace-chaps/drafts/cursor-rbcnc-gender-lexicon-2026-08-31.md
 *
 * Usage:
 *   node scripts/gender-lexicon-batch.js --list
 *   node scripts/gender-lexicon-batch.js --batch 20
 *   node scripts/gender-lexicon-batch.js --batch 20 --apply
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const DATA_PATH = path.join(ROOT, 'docs/data/churches.json');
const CID = 'CCW-0831-GENDER';
const STAMP = `[2026-08-31] Gender lexicon batch (CID ${CID}): Strong gender relabeled to Scriptural patriarchy / biblical manhood / Christlike headship. Score color unchanged.`;
const TODAY = new Date().toLocaleDateString('en-CA', { timeZone: 'America/New_York' });

const OLD_SCORE_DESC = "Biblical manhood and womanhood by God's design — patriarchal, complementarian, egalitarian, or affirming gender ideology?";
const NEW_SCORE_DESC = "Biblical manhood and womanhood by God's design — Scriptural patriarchy, biblical manhood, Christlike headship, egalitarian, or affirming gender ideology?";

const REPLACEMENTS = [
  [/Complementarian\s*[—–-]\s*male elders\/pastors per 1689 LBCF \+ Scripture\.?/gi, 'Scriptural patriarchy — male elders/pastors per 1689 LBCF + Scripture.'],
  [/Reformed Baptist complementarian\s*[—–-]\s*male elders\/pastors per 1689 LBCF \+ Scripture\.?/gi, 'Reformed Baptist — Scriptural patriarchy — male elders/pastors per 1689 LBCF + Scripture.'],
  [/Complementarian\s*[—–-]\s*male elders\/pastors only per 1689\.?/gi, 'Scriptural patriarchy — male elders/pastors only per 1689.'],
  [/Complementarian\/patriarchal\s*[—–-]\s*male elders only per RB practice\.?/gi, 'Scriptural patriarchy — male elders only per RB practice.'],
  [/Per confessional Reformed standards \(WCF, 1689 LBCF\): complementarian; male-only ordination\.?/gi, 'Scriptural patriarchy — male elders/pastors per 1689 LBCF + Scripture.'],
  [/Complementarian;\s*male-only elder\/pastor standard per 1689 LBCF \+ 9Marks norms\.?/gi, 'Scriptural patriarchy — male-only elder/pastor standard per 1689 LBCF + 9Marks norms.'],
  [/Green\s*[—–-]\s*Complementarian Reformed Baptist led by a plurality of male elders[^.]*\.?/gi, 'Scriptural patriarchy — Reformed Baptist plurality of male elders per 1689 LBCF + Scripture.'],
  [/GREEN\s*[—–-]\s*strong complementarian\/patriarchal vision\. Male elders only\.[^.]*/gi, 'Scriptural patriarchy — male elders only. Christlike headship per biblical manhood.'],
  [/Per Pillar distinctives: complementarian; male-only ordained eldership\.?/gi, 'Scriptural patriarchy — male-only ordained eldership per 1689 LBCF + Scripture.'],
  [/SBC complementarian per BF&M 2000 Article VI\.?/gi, 'Scriptural patriarchy — male elders/pastors per 1689 LBCF + Scripture.'],
  [/Complementarian per Elder Affirmation of Faith\s*[—–-]\s*male-only elders[^.]*\.?/gi, 'Scriptural patriarchy — male-only elders per Elder Affirmation of Faith.'],
];

function applyReplacements(text) {
  if (!text || typeof text !== 'string') return text;
  let out = text;
  for (const [re, rep] of REPLACEMENTS) out = out.replace(re, rep);
  // Residual standalone label at start of gender notes (Strong only — not verify boilerplate)
  out = out.replace(/^Complementarian\s*[—–-]\s*/i, 'Scriptural patriarchy — ');
  out = out.replace(/^Green\s*[—–-]\s*Complementarian\s*/i, 'Scriptural patriarchy — ');
  return out;
}

function isReformedBaptist(c) {
  const denom = String(c.denomination || '').toLowerCase();
  const name = String(c.name || '').toLowerCase();
  const assess = String(c.assessment || '').toLowerCase();
  const tags = (c.tags || []).join(' ').toLowerCase();
  const df = String(c.denomination_family || '').toLowerCase();
  const gd = String(c.gender_detail || '').toLowerCase();
  const gn = String((c.score_notes || {}).gender || '').toLowerCase();
  const lbcf1689 = /\b1689 lbcf\b/.test(`${gd} ${gn} ${assess} ${denom}`);

  if (/converge/.test(denom) && !name.includes('reformed baptist')) return false;
  if (/southern baptist|\bsbc\b/.test(denom) && !name.includes('reformed baptist') && !assess.includes('reformed baptist')) {
    return false;
  }

  return (
    denom.includes('reformed baptist') ||
    name.includes('reformed baptist') ||
    df.includes('reformed-baptist') ||
    tags.includes('reformed-baptist') ||
    (lbcf1689 && name.includes('baptist')) ||
    (assess.includes('reformed baptist') && lbcf1689)
  );
}

function hasWomenPastor(c) {
  const blob = JSON.stringify(c).toLowerCase();
  if (/female\s+(senior\s+)?pastor|woman\s+pastor|women\s+pastor|pastrix|she\/her.*pastor|co-pastor.*female/i.test(blob)) return true;
  for (const p of c.pastors || []) {
    const role = String(p.role || '').toLowerCase();
    const name = String(p.name || '');
    if (/pastor|elder/.test(role) && /\((f|female)\)/i.test(name)) return true;
    if (/pastor|elder/.test(role) && /^(rev\.?\s*)?(pastor\s+)?(sister|mother)\b/i.test(name)) return true;
  }
  return false;
}

function hasLgbtqPower(c) {
  const blob = JSON.stringify(c).toLowerCase();
  return /lgbtq|affirming|same-sex marriage|gay pastor|transgender.*(pastor|elder|leader)|pride flag/i.test(blob);
}

function genderBlob(c) {
  const sn = c.score_notes || {};
  return `${sn.gender || ''} ${c.gender_detail || ''}`;
}

function isVerifyBoilerplate(text) {
  return /verify on church website.*complementarian polity/i.test(text);
}

function needsRelabel(c) {
  if ((c.scores || {}).gender !== 'green') return false;
  if (!isReformedBaptist(c)) return false;
  if (hasWomenPastor(c)) return false;
  if (hasLgbtqPower(c)) return false;
  const blob = genderBlob(c);
  if (!/\bcomplementarian\b/i.test(blob)) return false;
  if (isVerifyBoilerplate(blob)) return false;
  return true;
}

function stampNotes(notes) {
  const base = Array.isArray(notes) ? notes.join(' ') : String(notes || '');
  if (base.includes(CID)) return notes;
  const add = STAMP;
  if (Array.isArray(notes)) return [...notes, add];
  return base ? `${base} ${add}` : add;
}

function patchChurch(c) {
  const before = JSON.stringify({ gn: c.score_notes?.gender, gd: c.gender_detail });
  if (c.score_notes && c.score_notes.gender) {
    c.score_notes.gender = applyReplacements(c.score_notes.gender);
  }
  if (c.gender_detail) {
    c.gender_detail = applyReplacements(c.gender_detail);
  }
  const after = JSON.stringify({ gn: c.score_notes?.gender, gd: c.gender_detail });
  if (before === after) return false;
  c.last_reviewed = TODAY;
  c.enrichment_notes = stampNotes(c.enrichment_notes);
  return true;
}

function loadData() {
  return JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
}

function saveData(data) {
  fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2) + '\n');
}

function listEligible(data) {
  return data.churches.filter(c => needsRelabel(c)).map(c => c.id || c.slug);
}

function main() {
  const args = process.argv.slice(2);
  const listOnly = args.includes('--list');
  const apply = args.includes('--apply');
  const batchIdx = args.indexOf('--batch');
  const batchSize = batchIdx >= 0 ? parseInt(args[batchIdx + 1], 10) || 20 : 20;

  const data = loadData();
  const eligible = listEligible(data);
  console.log(`Eligible RB Strong + complementarian: ${eligible.length}`);
  if (listOnly || !apply) {
    eligible.slice(0, 50).forEach(id => console.log(' ', id));
    if (!apply) {
      console.log('\nDry run. Pass --apply to write + regenerate pages.');
      return;
    }
  }

  const batch = eligible.slice(0, batchSize);
  if (!batch.length) {
    console.log('Nothing to apply.');
    return;
  }

  const idSet = new Set(batch);
  let changed = 0;
  for (const c of data.churches) {
    const id = c.id || c.slug;
    if (!idSet.has(id)) continue;
    if (patchChurch(c)) changed++;
  }
  saveData(data);
  console.log(`Patched ${changed} records in churches.json`);

  const onlyArg = batch.map(id => JSON.stringify(id)).join(',');
  execSync(`node generate-church-pages.js --only ${onlyArg}`, { cwd: ROOT, stdio: 'inherit' });
  console.log(`\nBatch ready: ${batch.join(', ')}`);
}

main();
