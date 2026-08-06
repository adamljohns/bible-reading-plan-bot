# Reversed-word-order duplicate slugs — 49 pairs

**Found:** 2026-08-06 · **Status:** awaiting Adam's approval, nothing merged yet

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

## Three where BOTH slugs read wrong

`land-promise` / `promise-land`, `nations-table` / `table-nations`, and
`babel-tower` / `tower-babel` are all awkward. The natural forms are
**promised-land**, **table-of-nations** and **tower-of-babel**. Merging into
either existing slug preserves a bad title. Recommend merging to the better of
the two and renaming after, or authoring the correct slug and redirecting both.

## Applying

Each is one `bin/merge_entries.py <keep> <drop> --apply`, which repoints inbound
links and leaves a no-index redirect stub, so every old URL survives and the
change is reversible. 49 merges would take the corpus from 7,922 to 7,873.

**Do not run this as a batch until the canonical column is approved** — the
wrong survivor is worse than the duplicate, because it becomes the title readers
see.
