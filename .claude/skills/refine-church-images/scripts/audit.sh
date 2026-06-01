#!/bin/bash
# audit.sh — per-church logo/hero quality audit for a scope.
# Flags cross-contamination, bare favicons, and missing images.
#
# Usage:
#   bash audit.sh Fredericksburg
#   bash audit.sh VA
#   bash audit.sh                # whole directory (long)

set -u
cd "$(dirname "$0")/../../../.." || { echo "repo root not found"; exit 1; }

export AUDIT_SCOPE="${1:-}"

node -e "
const fs = require('fs');
const scope = process.env.AUDIT_SCOPE || null;
const d = JSON.parse(fs.readFileSync('docs/data/churches.json', 'utf8'));
let pool = d.churches;
if (scope) {
  const s = scope;
  if (s.length === 2) pool = pool.filter(c => new RegExp(',\\\\s*'+s.toUpperCase()+'\\\\b').test(c.address||''));
  else pool = pool.filter(c => new RegExp(s, 'i').test(c.address||''));
}

const CDN_OK = /squarespace-cdn|squarespace\.com|googleusercontent|ggpht|cloudinary|thechurchco|wixstatic|wix\.com|parastorage|wp\.com|gstatic|amazonaws|cloudfront|imgix|nucleus-cdn|cdn-website|files\.|\bcdn\d*\./i;
const BARE_FAVICON = /\/favicon\.(ico|png)(\?|\$)|cropped-favicon/i;
function root(u){ try { return new URL(u).hostname.replace(/^www\./,'').split('.').slice(-2).join('.'); } catch(e){ return null; } }

function verdict(imgUrl, webRoot) {
  if (!imgUrl) return 'MISSING';
  if (BARE_FAVICON.test(imgUrl)) return 'BARE-FAVICON';
  const ir = root(imgUrl);
  if (!webRoot || !ir) return 'OK?';
  if (ir === webRoot) return 'OK';
  if (CDN_OK.test(imgUrl)) return 'OK(cdn)';
  return 'CONTAMINATION';
}

let counts = { logoOK:0, logoBare:0, logoContam:0, logoMissing:0, heroOK:0, heroContam:0, heroMissing:0 };
const flagged = [];
for (const c of pool) {
  const wr = root(c.website);
  const lv = verdict(c.image_thumb, wr);
  const hv = verdict(c.image_url, wr);
  if (lv.startsWith('OK')) counts.logoOK++; else if (lv==='BARE-FAVICON') counts.logoBare++; else if (lv==='CONTAMINATION') counts.logoContam++; else counts.logoMissing++;
  if (hv.startsWith('OK')) counts.heroOK++; else if (hv==='CONTAMINATION') counts.heroContam++; else counts.heroMissing++;
  if (lv === 'CONTAMINATION' || lv === 'BARE-FAVICON' || hv === 'CONTAMINATION') {
    flagged.push({ name: c.name, slug: c.slug || c.id, lv, hv, logo: (c.image_thumb||'').slice(0,55), hero: (c.image_url||'').slice(0,55) });
  }
}

console.log('=== Image/Logo Audit · scope: ' + (scope||'ALL') + ' · ' + pool.length + ' churches ===');
console.log('');
console.log('LOGO:  OK=' + counts.logoOK + '  bare-favicon=' + counts.logoBare + '  CONTAMINATION=' + counts.logoContam + '  missing=' + counts.logoMissing);
console.log('HERO:  OK=' + counts.heroOK + '  CONTAMINATION=' + counts.heroContam + '  missing=' + counts.heroMissing);
console.log('');
console.log('FLAGGED (' + flagged.length + ' need attention):');
for (const f of flagged) {
  console.log('  ' + f.name.slice(0,34).padEnd(34) + ' logo=' + f.lv.padEnd(13) + ' hero=' + f.hv);
  if (f.lv === 'CONTAMINATION' || f.lv === 'BARE-FAVICON') console.log('      logo: ' + f.logo);
  if (f.hv === 'CONTAMINATION') console.log('      hero: ' + f.hero);
}
"
