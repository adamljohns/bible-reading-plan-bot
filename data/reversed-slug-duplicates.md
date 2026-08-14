# Reversed-word-order duplicate slugs — 49 pairs

**Found:** 2026-08-06 · **Status:** the 49 merges below have since been applied
(corpus settled at 7,873; every merge-away slug is now a redirect stub in
`data/dictionary-redirects.txt`). Two of the three awkward survivors were
renamed on 2026-08-06 — see "Three where BOTH slugs read wrong" below.

Hermes flagged "158 words with multiple slugs — potential duplicates from
different model generations." Most of that number is **intentional
disambiguation** the roadmap says to KEEP (`joshua` / `joshua-figure` /
`joshua-book` are a man, a person-entry and a book). Filtering to slugs that are
literal word-order reversals of each other isolates the real artifact — the
class Hermes named with "john-wesley vs wesley-john".

**49 pairs. Every one is the same concept written twice.**

## Why the canonical column is hand-picked

Neither automatic signal works. Inbound links are 1-vs-1 for all 49. Article
length picks the wrong survivor repeatedly — it would keep `counselor-wonderful`
over **wonderful-counselor**, `creed-apostles` over **apostles-creed**, and
`vine-true` over **true-vine**. Canonical here is natural English word order,
which is a judgment call, so it is listed for review rather than applied.

| Keep (natural order) | Merge away | Note |
|---|---|---|
| wonderful-counselor | counselor-wonderful | Isa 9:6 |
| apostles-creed | creed-apostles | |
| true-vine | vine-true | Joh 15:1 |
| righteous-anger | anger-righteous | |
| false-teacher | teacher-false | |
| pure-heart | heart-pure | Mat 5:8 |
| new-heart | heart-new | Eze 36:26 |
| promised-land → land-promise | promise-land | **both are wrong; see below** |
| table-of-nations → nations-table | table-nations | **both are wrong; see below** |
| spiritual-adultery | adultery-spiritual | |
| incense-altar | altar-incense | |
| anointing-oil | oil-anointing | |
| tower-of-babel → babel-tower | tower-babel | **both are wrong; see below** |
| babylonian-captivity | captivity-babylonian | |
| believer-baptism | baptism-believer | |
| biblical-meditation | meditation-biblical | |
| binding-of-isaac → binding-isaac | isaac-binding | |
| bronze-laver | laver-bronze | |
| glory-cloud | cloud-glory | |
| collective-guilt | guilt-collective | |
| common-grace | grace-common | |
| cost-of-discipleship → cost-discipleship | discipleship-cost | |
| jerusalem-council | council-jerusalem | |
| marriage-covenant | covenant-marriage | |
| rainbow-covenant | covenant-rainbow | |
| covenant-sign | sign-covenant | |
| peter-denial | denial-peter | |
| divine-foreknowledge | foreknowledge-divine | |
| divine-protection | protection-divine | |
| divine-simplicity | simplicity-divine | |
| unconditional-election | election-unconditional | |
| love-of-enemy → enemy-love | love-enemy | |
| realized-eschatology | eschatology-realized | |
| theistic-evolution | evolution-theistic | |
| first-love | love-first | Rev 2:4 |
| spiritual-formation | formation-spiritual | |
| narrow-gate | gate-narrow | Mat 7:13 |
| prevenient-grace | grace-prevenient | |
| verbal-inspiration | inspiration-verbal | |
| jc-ryle | ryle-jc | |
| john-wesley | wesley-john | Hermes's example |
| last-trumpet | trumpet-last | 1Co 15:52 |
| servant-leadership | leadership-servant | |
| renewal-of-mind → mind-renewal | renewal-mind | |
| peter-restoration | restoration-peter | |
| pilgrim-stranger | stranger-pilgrim | |
| prayer-warrior | warrior-prayer | |
| progressive-sanctification | sanctification-progressive | |
| rejected-stone | stone-rejected | Psa 118:22 |

## Three where BOTH slugs read wrong — two fixed, one blocked

`land-promise` / `promise-land`, `nations-table` / `table-nations`, and
`babel-tower` / `tower-babel` are all awkward. The natural forms are
**promised-land**, **table-of-nations** and **tower-of-babel**.

**Done 2026-08-06 — the two clean ones.** `tower-babel` → **tower-of-babel** and
`table-nations` → **table-of-nations**. Both pages already *displayed* the right
title ("Tower of Babel", "Table of Nations"); only the slug read wrong. Each was
copied to the correct slug, self-references (canonical, og:url, ld+json) fixed,
then `bin/merge_entries.py <new> <old> --apply` repointed inbound links and left
a no-index stub, so all four old URLs still resolve:

| Old URL | Resolves to |
|---|---|
| `tower-babel.html` | tower-of-babel.html |
| `babel-tower.html` | tower-of-babel.html |
| `table-nations.html` | table-of-nations.html |
| `nations-table.html` | table-of-nations.html |

The two legacy sibling stubs were de-chained to point straight at the new
canonical (a stub pointing at a stub costs a hop and confuses SEO), and
`dictionary-redirects.txt` was rewritten to match. Derived artifacts were
hand-patched, not regenerated: `manifest.json`, `search-index.json`,
`sitemap-dictionary.xml`, `dictionary-slugs.txt`. Verified in Chromium — all six
URLs land on the right page in one hop. Integrity audit: PASS.

**Blocked — `promise-land` needs Adam's call.** This one is NOT a rename. A
separate live entry **`promised-land` already exists** (24.3 KB, title "Promised
Land") alongside `promise-land` (18.5 KB, title "Promise Land"). So the natural
slug is already taken by a real, longer entry, and this is a three-way merge of
two substantive pages, not a rename. Per the rule at the bottom of this file —
the wrong survivor is worse than the duplicate — nothing was touched. Adam
decides which body text survives (or whether they are genuinely two ideas:
the land promised to Abraham vs. Canaan itself).

*Read side by side 2026-08-14 — they are NOT two ideas.* Both open on the same
definition (the land sworn to Abraham, Gen 15:18, inherited under Joshua) and
both run the same typology out to the greater rest in Hebrews. This is one
concept written twice by two model generations. Decision-ready recommendation,
**not applied**:

| | `promised-land` (recommend KEEP) | `promise-land` (recommend MERGE AWAY) |
|---|---|---|
| Display title | "Promised Land" — correct | "Promise Land" — a common misspelling |
| Size | 25.0 KB | 19.6 KB |
| Has | Hebrew Roots | In the Text (chapter links) |

`promised-land` wins on slug, title and depth. **One merge detail if approved:**
`promise-land` carries an *In the Text* section that `promised-land` lacks —
port those chapter links across before merging, or the reading-Bible links are
lost. Then it is one `bin/merge_entries.py promised-land promise-land --apply`.

## Applying

Each is one `bin/merge_entries.py <keep> <drop> --apply`, which repoints inbound
links and leaves a no-index redirect stub, so every old URL survives and the
change is reversible. 49 merges would take the corpus from 7,922 to 7,873.

**Do not run this as a batch until the canonical column is approved** — the
wrong survivor is worse than the duplicate, because it becomes the title readers
see.
