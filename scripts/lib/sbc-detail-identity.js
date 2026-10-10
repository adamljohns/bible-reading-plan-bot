'use strict';

function firstPostal(value) {
  const match = String(value || '').match(/\b(\d{5})(?:-\d{4})?\b/);
  return match ? match[1] : null;
}

function extractSourcePostal(html) {
  const address = String(html || '').match(/<h3[^>]+class=["'][^"']*heading__address[^"']*["'][^>]*>([\s\S]*?)<\/h3>/i);
  return address ? firstPostal(address[1]) : null;
}

function validateSourceIdentity(church, result) {
  if (result && result.sbc_detail_error) return null;
  const sourcePostal = firstPostal(result && result.sbc_detail_source_postal);
  if (!sourcePostal) return 'missing source postal identity evidence';
  const canonicalPostal = firstPostal(church && church.address);
  if (!canonicalPostal) return 'missing canonical postal identity evidence';
  if (canonicalPostal !== sourcePostal) {
    return `postal mismatch: canonical ${canonicalPostal}, source ${sourcePostal}`;
  }
  return null;
}

function isIdentityCompleteResult(result) {
  return !!(result && result.id && firstPostal(result.sbc_detail_source_postal));
}

module.exports = { firstPostal, extractSourcePostal, validateSourceIdentity, isIdentityCompleteResult };
