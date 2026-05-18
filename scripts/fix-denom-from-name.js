#!/usr/bin/env node
// Phase 6 — Fix default-Baptist denomination for 9Marks records whose
// name explicitly indicates a different denomination.
//
// Detects: Presbyterian (PCA/OPC/ARP/EPC), Anglican (ACNA/Episcopal),
// Lutheran (LCMS/WELS), Methodist, Mennonite, Calvary Chapel, Vineyard,
// Christian Reformed (CRC/URCNA/URC/RCA), C&MA, EFCA, etc.

const fs = require('fs');
const path = require('path');
const CHURCHES = path.join(__dirname, '..', 'docs', 'data', 'churches.json');
const TODAY = new Date().toISOString().slice(0, 10);

// Detection rules: regex → {denomination, denomination_family}
const DENOM_RULES = [
  { rx: /\bPCA\b|\bPresbyterian Church in America\b/i, denom: 'PCA (Presbyterian Church in America)', family: 'Presbyterian' },
  { rx: /\bOPC\b|\bOrthodox Presbyterian Church\b/i, denom: 'OPC (Orthodox Presbyterian Church)', family: 'Presbyterian' },
  { rx: /\bARP\b|\bAssociate Reformed Presbyterian\b/i, denom: 'ARP (Associate Reformed Presbyterian)', family: 'Presbyterian' },
  { rx: /\bEPC\b|\bEvangelical Presbyterian Church\b/i, denom: 'EPC (Evangelical Presbyterian Church)', family: 'Presbyterian' },
  { rx: /\bACNA\b|\bAnglican Church in North America\b/i, denom: 'ACNA (Anglican Church in North America)', family: 'Anglican' },
  { rx: /\bAnglican\b/i, denom: 'Anglican', family: 'Anglican' },
  { rx: /\bEpiscopal\b/i, denom: 'Episcopal', family: 'Anglican' },
  { rx: /\bLCMS\b|\bLutheran Church.Missouri Synod\b/i, denom: 'LCMS (Lutheran Church-Missouri Synod)', family: 'Lutheran' },
  { rx: /\bWELS\b|\bWisconsin Evangelical Lutheran\b/i, denom: 'WELS (Wisconsin Evangelical Lutheran Synod)', family: 'Lutheran' },
  { rx: /\bELS\b/, denom: 'ELS (Evangelical Lutheran Synod)', family: 'Lutheran' },
  { rx: /\bLutheran\b/i, denom: 'Lutheran', family: 'Lutheran' },
  { rx: /\bChristian Reformed Church\b|\bCRC\b/i, denom: 'Christian Reformed Church (CRC)', family: 'Reformed (Dutch)' },
  { rx: /\bURCNA\b|\bUnited Reformed Church\b/i, denom: 'URCNA (United Reformed Churches of North America)', family: 'Reformed (Dutch)' },
  { rx: /\bURC\b/, denom: 'URC (United Reformed)', family: 'Reformed (Dutch)' },
  { rx: /\bRCA\b|\bReformed Church in America\b/i, denom: 'RCA (Reformed Church in America)', family: 'Reformed (Dutch)' },
  { rx: /\bPresbyterian\b/i, denom: 'Presbyterian', family: 'Presbyterian' },
  { rx: /\bMethodist\b/i, denom: 'Methodist', family: 'Methodist' },
  { rx: /\bC.MA\b|\bChristian and Missionary Alliance\b/i, denom: 'C&MA (Christian and Missionary Alliance)', family: 'Evangelical' },
  { rx: /\bEFCA\b|\bEvangelical Free Church of America\b/i, denom: 'EFCA (Evangelical Free Church of America)', family: 'Evangelical' },
  { rx: /\bMennonite\b/i, denom: 'Mennonite', family: 'Anabaptist' },
  { rx: /\bAmish\b/i, denom: 'Amish', family: 'Anabaptist' },
  { rx: /\bCalvary Chapel\b/i, denom: 'Calvary Chapel', family: 'Non-Denominational (Calvary Chapel)' },
  { rx: /\bVineyard\b/i, denom: 'Vineyard', family: 'Vineyard' },
  { rx: /\bFoursquare\b/i, denom: 'Foursquare', family: 'Pentecostal' },
  { rx: /\bAssemblies of God\b|\bAoG\b/i, denom: 'Assemblies of God', family: 'Pentecostal' },
  { rx: /\bPentecostal\b/i, denom: 'Pentecostal', family: 'Pentecostal' },
];

function detectDenom(name) {
  for (const rule of DENOM_RULES) {
    if (rule.rx.test(name)) {
      return { denomination: rule.denom, denomination_family: rule.family };
    }
  }
  return null;
}

function main() {
  const d = JSON.parse(fs.readFileSync(CHURCHES, 'utf8'));
  let fixed = 0;
  const samples = [];
  for (const c of d.churches) {
    if (!c || typeof c !== 'object' || !c.id || !c.name) continue;
    // Only consider records whose denomination is generic-default
    if (c.denomination !== 'Baptist' && c.denomination !== 'verify' && c.denomination !== 'Reformed Evangelical') continue;
    const det = detectDenom(c.name);
    if (!det) continue;
    const oldDenom = c.denomination;
    c.denomination = det.denomination;
    c.denomination_family = det.denomination_family;
    const note = `[${TODAY}] Phase 6 denom auto-detect from name: "${oldDenom}" → "${det.denomination}".`;
    c.enrichment_notes = c.enrichment_notes ? c.enrichment_notes + '\n' + note : note;
    fixed++;
    if (samples.length < 5) samples.push(`${c.name} → ${det.denomination}`);
  }
  d.directory_updated = TODAY;
  fs.writeFileSync(CHURCHES, JSON.stringify(d, null, 2) + '\n');
  console.log(`Fixed ${fixed} records' denomination via name-detect.`);
  if (samples.length) console.log('Samples:', samples.join('; '));
}

if (require.main === module) main();
