# Hidden essays ledger — 2026-11-17

Six church-directory essays were hidden from search engines and from the blog
lists on 2026-11-17. Nothing was deleted. Each essay is still served at its
original URL and still opens for anyone who has the link.

**Why.** The blog audit of 16 Nov 2026 found that these six essays state church
counts, ledger directions and ratings that do not agree with each other or with
themselves (above all, which side the 2020 Warhurst Protest signers were on).
Adam's ruling, 16 Nov: "we definitely don't want anything contradicting itself,
so we need to fix that." He accepted hiding them until the data is reconciled.

**Until when.** Until the church-directory QA desk has settled each contradiction
from a cited source and the essay text has been corrected. The reconciliation
packet is at `~/.openclaw/workspace-chaps/inbox/max-1117-directory-essays-reconcile.md`.
Restoring an essay is Adam's call, through Max.

## What was done to every essay

1. Added one line to the essay's `<head>`, directly after the `<meta charset>` line:
   `    <meta name="robots" content="noindex, nofollow">`
2. Removed its entry from the `WP_POSTS` array in `docs/blog.html` (the blog hub).
3. Removed its card from `docs/blog-general.html` (the only category page that listed it).
4. Removed its entry from `docs/assets/blog-manifest.json`.
5. Removed its `<url>` block from `docs/sitemap-blog.xml`.

`docs/sitemap.html` lists no individual blog posts, so there was nothing to remove there.
No site-wide generator was run; all edits were made by hand-written script on these files only.

Counts changed to match: `docs/blog.html` static fallbacks `heroPostCount` 235 -> 229 and
`countNum` 233 -> 229 (a script overwrites both at load from the array length), and the
General filter button `(19)` -> `(14)`; `docs/blog-general.html` "20 posts" -> "14 posts".

## What was deliberately left alone

- The six files themselves, apart from the one added line.
- Links to these essays from other pages. They still work and were not removed:
  `docs/directory-drift.html`, `docs/directory-map.html`, `docs/directory-methodology.html`,
  `docs/directory-networks.html`, and the previous/next or in-text links in
  `docs/blog/bringing-the-1689-back-to-life.html`,
  `docs/blog/fredericksburg-church-directory-theological-due-diligence.html`,
  `docs/blog/the-heroism-of-meddling.html`, plus the previous/next links among the six.
  No page under `docs/churches`, `docs/dictionary`, `docs/lexicon` or `docs/worship` links to them.
- `docs/data/churches.json` and every church page.

## How to restore one essay

Do all five, in a clean worktree off `origin/main`, then push (see `DEPLOY-DOCTRINE.md`).

1. Remove the noindex line from the essay: `python3 bin/approval_gate.py --release docs/blog/<slug>.html`
   (or delete the line by hand).
2. Put the hub entry back into `WP_POSTS` in `docs/blog.html`: paste the JSON object given below,
   followed by `, `, immediately after the object whose `url` is named under "goes after".
   The array is in date order, newest first.
3. Put the card back into `docs/blog-general.html` after the card named below, and add one to the
   "N posts" count in that page's header and to the General button count in `docs/blog.html`.
4. Put the manifest entry back into `docs/assets/blog-manifest.json` after the slug named below
   (the file is sorted by title).
5. Put the `<url>` block back into `docs/sitemap-blog.xml`, or run `python3 bin/generate_sitemap.py`
   (it skips any page that still carries noindex, so do step 1 first).

To restore all six at once, and only if none of the five listing files has been edited since in a
way that conflicts: `git revert <the commit that added this file>`
(`git log --diff-filter=A --format=%H -- HIDDEN-ESSAYS-2026-11-17.md`).

If the neighbour named under "goes after" is itself one of the six and still hidden, place the
entry by date instead (hub and category page run newest first; the manifest runs by title).

After restoring, mark the essay as restored in this file with the date; do not delete its section.

## 1. The Discipline of a Public Rubric: Why We Built the Church Directory This Way &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/the-discipline-of-a-public-rubric.html`
- URL: https://usmcmin.org/blog/the-discipline-of-a-public-rubric.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 75 (0-based); goes after `blog/where-the-warhurst-protesters-lead-today.html`:**

```json
{"title": "The Discipline of a Public Rubric: Why We Built the Church Directory This Way", "date": "May 19, 2026", "url": "blog/the-discipline-of-a-public-rubric.html", "excerpt": "The methodology page tells you what the church directory is. This essay tells you why we built it the way we did — the editorial discipline, the five signal layers, the willingness to be corrected in public, and the spec", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/where-the-warhurst-protesters-lead-today.html`:**

```html
        <a href="blog/the-discipline-of-a-public-rubric.html" class="post-card">
            <div class="post-date">2026-05-19</div>
            <div class="post-title">The Discipline of a Public Rubric: Why We Built the Church Directory This Way</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `the-culmination`:**

```json
{
  "title": "The Discipline of a Public Rubric: Why We Built the Church Directory This Way",
  "slug": "the-discipline-of-a-public-rubric",
  "date": "2026-05-19",
  "category": "general",
  "file": "blog/the-discipline-of-a-public-rubric.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/the-discipline-of-a-public-rubric.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```

## 2. Where the Nashville Statement Signers Lead Today &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/where-the-nashville-statement-signers-lead-today.html`
- URL: https://usmcmin.org/blog/where-the-nashville-statement-signers-lead-today.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 76 (0-based); goes after `blog/the-discipline-of-a-public-rubric.html`:**

```json
{"title": "Where the Nashville Statement Signers Lead Today", "date": "May 19, 2026", "url": "blog/where-the-nashville-statement-signers-lead-today.html", "excerpt": "The Nashville Statement of 2017 was a line in the sand on biblical sexuality. Nine years later, we cross-referenced its signers against every evangelical church in our directory. 296 churches across 38 states. SBC domina", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/where-the-warhurst-protesters-lead-today.html`:**

```html
        <a href="blog/where-the-nashville-statement-signers-lead-today.html" class="post-card">
            <div class="post-date">2026-05-19</div>
            <div class="post-title">Where the Nashville Statement Signers Lead Today</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `where-the-dallas-statement-signers-lead-today`:**

```json
{
  "title": "Where the Nashville Statement Signers Lead Today",
  "slug": "where-the-nashville-statement-signers-lead-today",
  "date": "2026-05-19",
  "category": "general",
  "file": "blog/where-the-nashville-statement-signers-lead-today.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/where-the-nashville-statement-signers-lead-today.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```

## 3. Where the Dallas Statement Signers Lead Today &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/where-the-dallas-statement-signers-lead-today.html`
- URL: https://usmcmin.org/blog/where-the-dallas-statement-signers-lead-today.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 73 (0-based); goes after `blog/the-seven-ledger-map.html`:**

```json
{"title": "Where the Dallas Statement Signers Lead Today", "date": "May 20, 2026", "url": "blog/where-the-dallas-statement-signers-lead-today.html", "excerpt": "One year after Nashville, a different but overlapping group of evangelical leaders drew a second line in the sand — this time against critical-theory drift inside the church. Eight years later, we mapped where the 166 Da", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/the-seven-ledger-map.html`:**

```html
        <a href="blog/where-the-dallas-statement-signers-lead-today.html" class="post-card">
            <div class="post-date">2026-05-20</div>
            <div class="post-title">Where the Dallas Statement Signers Lead Today</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `when-your-ai-reads-the-bible-better-than-you-the-ethics-of-ai-in-christian-ministry`:**

```json
{
  "title": "Where the Dallas Statement Signers Lead Today",
  "slug": "where-the-dallas-statement-signers-lead-today",
  "date": "2026-05-20",
  "category": "general",
  "file": "blog/where-the-dallas-statement-signers-lead-today.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/where-the-dallas-statement-signers-lead-today.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```

## 4. Where the Warhurst Protesters Lead Today &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/where-the-warhurst-protesters-lead-today.html`
- URL: https://usmcmin.org/blog/where-the-warhurst-protesters-lead-today.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 74 (0-based); goes after `blog/where-the-dallas-statement-signers-lead-today.html`:**

```json
{"title": "Where the Warhurst Protesters Lead Today", "date": "May 20, 2026", "url": "blog/where-the-warhurst-protesters-lead-today.html", "excerpt": "In December 2020 a quieter but more institutionally revealing protest was filed inside the Presbyterian Church in America — against the Missouri Presbytery's decision not to discipline a Revoice-affirming Side-B minister", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/the-seven-ledger-map.html`:**

```html
        <a href="blog/where-the-warhurst-protesters-lead-today.html" class="post-card">
            <div class="post-date">2026-05-20</div>
            <div class="post-title">Where the Warhurst Protesters Lead Today</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `where-the-nashville-statement-signers-lead-today`:**

```json
{
  "title": "Where the Warhurst Protesters Lead Today",
  "slug": "where-the-warhurst-protesters-lead-today",
  "date": "2026-05-20",
  "category": "general",
  "file": "blog/where-the-warhurst-protesters-lead-today.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/where-the-warhurst-protesters-lead-today.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```

## 5. The PCA-Progressive Coalition: AMR, Letter of Lament, Revoice, and CBE &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/the-pca-progressive-coalition.html`
- URL: https://usmcmin.org/blog/the-pca-progressive-coalition.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 71 (0-based); goes after `blog/bringing-the-1689-back-to-life.html`:**

```json
{"title": "The PCA-Progressive Coalition: AMR, Letter of Lament, Revoice, and CBE", "date": "May 20, 2026", "url": "blog/the-pca-progressive-coalition.html", "excerpt": "The smallest essay in the statement-ledger series and, in some ways, the most editorially interesting. Read in isolation, four small ledgers look insignificant. Read together as a coordinated coalition, 14 churches map t", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/sbc-2026-willy-rice.html`:**

```html
        <a href="blog/the-pca-progressive-coalition.html" class="post-card">
            <div class="post-date">2026-05-20</div>
            <div class="post-title">The PCA-Progressive Coalition: AMR, Letter of Lament, Revoice, and CBE</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `the-importance-of-clarity`:**

```json
{
  "title": "The PCA-Progressive Coalition: AMR, Letter of Lament, Revoice, and CBE",
  "slug": "the-pca-progressive-coalition",
  "date": "2026-05-20",
  "category": "general",
  "file": "blog/the-pca-progressive-coalition.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/the-pca-progressive-coalition.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```

## 6. The Seven-Ledger Map: Nine Years of Public Theological Statements in American Evangelicalism &mdash; U.S.M.C. Ministries

- File (unchanged location): `docs/blog/the-seven-ledger-map.html`
- URL: https://usmcmin.org/blog/the-seven-ledger-map.html
- Status: HIDDEN since 2026-11-17

**Removed from `docs/blog.html` (`WP_POSTS`), array position 72 (0-based); goes after `blog/the-pca-progressive-coalition.html`:**

```json
{"title": "The Seven-Ledger Map: Nine Years of Public Theological Statements in American Evangelicalism", "date": "May 20, 2026", "url": "blog/the-seven-ledger-map.html", "excerpt": "Across nine years and seven public theological statements — Nashville 2017, Dallas 2018, Revoice 2018–2026, Warhurst 2020, Letter of Lament 2025, AMR 2026, CBE 2026 — 462 American evangelical churches signed at least one", "cat": "General"}
```

**Removed from `docs/blog-general.html`; goes after the card for `blog/sbc-2026-willy-rice.html`:**

```html
        <a href="blog/the-seven-ledger-map.html" class="post-card">
            <div class="post-date">2026-05-20</div>
            <div class="post-title">The Seven-Ledger Map: Nine Years of Public Theological Statements in American Evangelicalism</div>
        </a>
```

**Removed from `docs/assets/blog-manifest.json`; goes after slug `the-sea-of-forgetfulness`:**

```json
{
  "title": "The Seven-Ledger Map: Nine Years of Public Theological Statements in American Evangelicalism",
  "slug": "the-seven-ledger-map",
  "date": "2026-05-20",
  "category": "general",
  "file": "blog/the-seven-ledger-map.html"
}
```

**Removed from `docs/sitemap-blog.xml`:**

```xml
  <url>
    <loc>https://usmcmin.org/blog/the-seven-ledger-map.html</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
```
