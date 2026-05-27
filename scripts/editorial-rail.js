// scripts/editorial-rail.js
// Shared snippet emitter — renders the "Editorial Series" rail used on every
// /directory-* page. Each card links to one of the blog essays that backs
// the directory's editorial layer.
//
// Usage:
//   const { editorialRailHtml, editorialRailCss } = require('./editorial-rail');
//   ... html += editorialRailCss; ... html += editorialRailHtml({ activeSlug: 'nashville' });

const ESSAYS = [
  {
    slug: 'founding-manifesto',
    href: '/blog/fredericksburg-church-directory-theological-due-diligence.html',
    title: 'Theological Due Diligence',
    sub: 'Founding manifesto — why this work exists',
    date: 'Mar 2026 (rev. May)',
  },
  {
    slug: 'methodology',
    href: '/blog/the-discipline-of-a-public-rubric.html',
    title: 'The Discipline of a Public Rubric',
    sub: 'Methodology essay — five signal layers + limits',
    date: 'May 19',
  },
  {
    slug: 'nashville',
    href: '/blog/where-the-nashville-statement-signers-lead-today.html',
    title: 'Nashville Statement Signers',
    sub: '296 churches · 38 states · biblical sexuality',
    date: 'May 19',
  },
  {
    slug: 'dallas',
    href: '/blog/where-the-dallas-statement-signers-lead-today.html',
    title: 'Dallas Statement Signers',
    sub: '166 churches · social justice / critical theory',
    date: 'May 20',
  },
  {
    slug: 'warhurst',
    href: '/blog/where-the-warhurst-protesters-lead-today.html',
    title: 'Warhurst Protesters',
    sub: '78 churches · 87% PCA · the red mirror',
    date: 'May 20',
  },
  {
    slug: 'coalition',
    href: '/blog/the-pca-progressive-coalition.html',
    title: 'PCA-Progressive Coalition',
    sub: '14 churches across 4 small ledgers',
    date: 'May 20',
  },
  {
    slug: 'synthesis',
    href: '/blog/the-seven-ledger-map.html',
    title: 'The Seven-Ledger Map',
    sub: 'Synthesis · 462 churches · 9 years',
    date: 'May 20',
  },
];

const editorialRailCss = `
  .editorial-rail { max-width:1100px; margin:24px auto 12px; padding:0 22px; }
  .editorial-rail h2 { color:var(--gold-light, #F4D470); font-size:0.92rem; text-transform:uppercase; letter-spacing:3px; margin-bottom:12px; font-family:'Inter', sans-serif; font-weight:600; }
  .editorial-rail h2 .count { color:var(--gray, #888); font-weight:400; letter-spacing:1px; margin-left:6px; font-size:0.78rem; text-transform:none; }
  .editorial-rail .rail { display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:10px; }
  .editorial-rail .essay { display:block; background:var(--card, #111); border:1px solid var(--border, #333); border-radius:8px; padding:12px 14px; text-decoration:none; color:inherit; transition:all 0.15s; border-left:3px solid var(--gold, #D4AF37); }
  .editorial-rail .essay:hover { border-color:var(--gold, #D4AF37); transform:translateY(-1px); background:rgba(212,175,55,0.05); }
  .editorial-rail .essay.active { border-left-width:4px; background:rgba(212,175,55,0.08); }
  .editorial-rail .essay .title { display:block; color:var(--white, #e8e8e8); font-weight:600; font-size:0.93rem; line-height:1.3; font-family:'Playfair Display', serif; }
  .editorial-rail .essay .sub { display:block; color:var(--gray, #888); font-size:0.78rem; margin-top:4px; line-height:1.4; }
  .editorial-rail .essay .date { display:block; color:var(--gold, #D4AF37); font-size:0.7rem; margin-top:6px; letter-spacing:0.5px; font-variant-numeric:tabular-nums; }
  @media (max-width:600px) { .editorial-rail { padding:0 16px; } .editorial-rail .rail { grid-template-columns:1fr; } }
`;

function editorialRailHtml(opts = {}) {
  const active = opts.activeSlug || null;
  const cards = ESSAYS.map(e => {
    const cls = e.slug === active ? 'essay active' : 'essay';
    return `<a class="${cls}" href="${e.href}">
      <span class="title">${e.title}</span>
      <span class="sub">${e.sub}</span>
      <span class="date">${e.date}</span>
    </a>`;
  }).join('\n    ');
  return `
<section class="editorial-rail" aria-label="Editorial essay series">
  <h2>Editorial Series<span class="count">${ESSAYS.length} essays · the directory's "why" layer</span></h2>
  <div class="rail">
    ${cards}
  </div>
</section>
`;
}

module.exports = { editorialRailHtml, editorialRailCss, ESSAYS };
