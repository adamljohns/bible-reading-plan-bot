'use strict';
/**
 * Denomination priors for the full-review round (Chaps ticket, 2026-11-08).
 *
 * Two questions the selector and the rubric engine both ask:
 *   1. Does this denomination ordain women as pastors/elders?  (selection tier a)
 *   2. Is the denomination's OFFICIAL position LGBT-affirming?  (rubric prior)
 *
 * The affirming list is exactly the one published on
 * https://usmcmin.org/directory-methodology.html ("LGBTQ-affirming denomination
 * -> RED minimum"). That page is the cited evidence when a prior fires, so the
 * two lists must not drift: change the page and this file together.
 *
 * A prior is only a prior. full-review-build-patch.js applies it only when the
 * congregation's OWN site confirms the affiliation, and stronger
 * congregation-specific evidence overrides it in either direction.
 */

const METHODOLOGY_URL = 'https://usmcmin.org/directory-methodology.html';
const METHODOLOGY_QUOTE = 'LGBTQ-affirming denomination → RED minimum. Applies to PCUSA, ELCA, the United Methodist Church (post-Charlotte 2024), The Episcopal Church, the United Church of Christ, the Christian Church (Disciples of Christ), the mainline Reformed Church in America, and Mennonite Church USA.';

// Order matters: the first match wins, so conservative look-alikes come first
// and are explicitly NOT affirming (methodology: "Conservative cousin
// denominations ... are explicitly excluded by the auto-flagger").
const DENOMS = [
  // conservative look-alikes (never affirming; do not ordain women as pastors)
  { key: 'acna', re: /anglican church in north america|\bacna\b|reformed episcopal|\brec\b/i, label: 'ACNA / Reformed Episcopal', ordains_women: false, affirming: false },
  { key: 'gmc', re: /global methodist|\bgmc\b/i, label: 'Global Methodist', ordains_women: true, affirming: false },
  { key: 'lcms', re: /missouri synod|\blcms\b|\bwels\b|wisconsin evangelical lutheran|\blcmc\b|\bnalc\b|north american lutheran/i, label: 'Confessional Lutheran', ordains_women: false, affirming: false },
  { key: 'pca', re: /presbyterian church in america|\bpca\b|\bopc\b|orthodox presbyterian|\barp\b|associate reformed|\beco\b|covenant order of evangelical presbyterians|\bepc\b|evangelical presbyterian/i, label: 'Conservative Presbyterian', ordains_women: false, affirming: false },
  { key: 'restoration', re: /christian churches and churches of christ|independent christian church|^\s*churches? of christ\b/i, label: 'Independent Christian Church / Churches of Christ', ordains_women: false, affirming: false },
  { key: 'urc', re: /\burcna\b|united reformed churches|\bprca\b|protestant reformed|canadian reformed|heritage reformed|free reformed/i, label: 'Conservative Reformed', ordains_women: false, affirming: false },

  // Methodist "Episcopal" bodies must match before TEC's bare /episcopal/.
  { key: 'ame', re: /african methodist episcopal|\bame\b|\bame ?zion\b|\bamez\b|christian methodist episcopal|\bcme\b|methodist episcopal/i, label: 'AME / AMEZ / CME', ordains_women: true, affirming: false },

  // affirming mainline (methodology list) — ordain women AND officially affirming
  { key: 'tec', re: /\bepiscopal\b|\btec\b/i, label: 'The Episcopal Church', ordains_women: true, affirming: true },
  { key: 'elca', re: /\belca\b|evangelical lutheran church in america/i, label: 'ELCA', ordains_women: true, affirming: true },
  { key: 'pcusa', re: /pc\s*\(?\s*usa\s*\)?|presbyterian church\s*\(?u\.?s\.?a\.?\)?|\bpcusa\b/i, label: 'PCUSA', ordains_women: true, affirming: true },
  { key: 'ucc', re: /united church of christ|\bucc\b/i, label: 'United Church of Christ', ordains_women: true, affirming: true },
  { key: 'umc', re: /united methodist|\bumc\b/i, label: 'United Methodist Church (post-2024)', ordains_women: true, affirming: true },
  { key: 'disciples', re: /disciples of christ|christian church\s*\(disciples/i, label: 'Christian Church (Disciples of Christ)', ordains_women: true, affirming: true },
  { key: 'rca', re: /reformed church in america|\brca\b/i, label: 'Reformed Church in America', ordains_women: true, affirming: true },
  { key: 'mcusa', re: /mennonite church usa/i, label: 'Mennonite Church USA', ordains_women: true, affirming: true },
  { key: 'mcc', re: /metropolitan community church/i, label: 'Metropolitan Community Churches', ordains_women: true, affirming: true },

  // ordain women, not officially affirming
  { key: 'abc', re: /american baptist|\babc[- ]?usa\b|\babcusa\b/i, label: 'American Baptist Churches USA', ordains_women: true, affirming: false },
  { key: 'cbf', re: /cooperative baptist|\bcbf\b/i, label: 'Cooperative Baptist Fellowship', ordains_women: true, affirming: false },
  { key: 'ecc', re: /evangelical covenant|covenant church\b/i, label: 'Evangelical Covenant Church', ordains_women: true, affirming: false },
  { key: 'brethren', re: /church of the brethren/i, label: 'Church of the Brethren', ordains_women: true, affirming: false },
  { key: 'moravian', re: /moravian/i, label: 'Moravian', ordains_women: true, affirming: false },
  { key: 'quaker', re: /quaker|religious society of friends|friends meeting/i, label: 'Friends', ordains_women: true, affirming: false },
  { key: 'nazarene', re: /nazarene/i, label: 'Church of the Nazarene', ordains_women: true, affirming: false },
  { key: 'wesleyan', re: /wesleyan|free methodist/i, label: 'Wesleyan / Free Methodist', ordains_women: true, affirming: false },
  { key: 'aog', re: /assembl(y|ies) of god|\baog\b|foursquare/i, label: 'Assemblies of God / Foursquare', ordains_women: true, affirming: false },
  { key: 'cog-anderson', re: /church of god \(anderson|anderson,? in/i, label: 'Church of God (Anderson)', ordains_women: true, affirming: false },
  { key: 'salvation-army', re: /salvation army/i, label: 'Salvation Army', ordains_women: true, affirming: false },
];

// Affirming mainline ranks ahead of "ordains women only" inside selection tier (a).
// denomination_detail is deliberately NOT read: it carries prose such as
// "Independent Christian Church ..., not Disciples of Christ (DOC)".
const denomText = c => [c.denomination, c.denomination_family, c.type]
  .filter(v => typeof v === 'string').join(' | ');

function denomPrior(c) {
  const t = denomText(c);
  if (!t) return null;
  for (const d of DENOMS) if (d.re.test(t)) return d;
  return null;
}

// Strings a congregation's own site uses to state the affiliation. Used to
// CONFIRM the stored denomination before its prior may drive a change.
const AFFILIATION_RE = {
  tec: /\bepiscopal church\b|\bepiscopal diocese\b|\bthe episcopal\b|[A-Z][a-z']+ episcopal church|\bepiscopal\b(?! church in north america)/i,
  elca: /\belca\b|evangelical lutheran church in america/i,
  pcusa: /pc\s*\(?usa\)?|presbyterian church \(u\.?s\.?a\.?\)/i,
  ucc: /united church of christ|\bucc\b/i,
  umc: /united methodist|\bumc\b/i,
  disciples: /disciples of christ/i,
  rca: /reformed church in america/i,
  mcusa: /mennonite church usa/i,
  mcc: /metropolitan community church/i,
};

module.exports = { DENOMS, denomPrior, denomText, AFFILIATION_RE, METHODOLOGY_URL, METHODOLOGY_QUOTE };
