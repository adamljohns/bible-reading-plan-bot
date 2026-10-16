# Generational dictionary grind — 100 per cohort (MBP-1015-GENDICT)

Principal, Telegram 2026-10-15 19:57 EDT: "Our MOOP dictionary doesn't have 'baddie' in it.
And I heard that's a genz term. We need to beef up our generational [entries] by 100 each
generation I think." Proof entry `baddie-genz` shipped the same night. This file is the
PLAN for the rest; nothing in it is built yet. Queue: `generational-100-per-gen-2026-10-15.json`
(same folder). The pipeline's batch glob (`data/dictionary-batches/*.json`) does not descend
into `_queue/`, so nothing here is picked up until an author copies words out into a real
`batch-*.json`.

## Where the corpus stands (2026-10-15, origin/main c6c0a26b189 + baddie)

Counted two ways, because they disagree. (a) is what the task asked for; (b) is what a visitor
sees on the Decoded pages, which are hand-curated card lists in `rebuild-dictionary.py`
(`genz-card` / `mill-card` / `genx-card` / `boomer-card`) and not derived from `pos`.

| Cohort | (a) entries whose `pos` names the cohort | (b) cards on the Decoded page |
|---|---|---|
| Silent (b. ~1928–45) | 0 | no page |
| Boomer (b. 1946–64) | 22 | 33 |
| Gen X (b. 1965–80) | 24 | 34 |
| Millennial (b. 1981–96) | 24 | 40 |
| Gen Z (b. 1997–2012) | 47 before baddie, 48 after | 61 before baddie, 62 after |
| Gen Alpha (b. 2013–) | 10 (all double-tagged "Gen-Z / Gen Alpha") | folded into Gen-Z page |
| "modern slang" / internet, no cohort named | 16 | — |

Counting method for (a): regex over `pos` in every `data/dictionary-batches/*.json` for
`silent`, `boomer`, `gen[- ]?x`, `millennial`, `gen[- ]?z`, `gen alpha`; an entry tagged
with two cohorts counts in both. Many generational words are already live under a non-cohort
tag or no tag at all (groovy, far-out, right-on, hippie "Boomer-era cultural label", sus
"modern slang", gigachad "internet meme / Gen-Z slang"); the queue dedup caught 145 of those
and dropped them, so the queue is net-new only.

## Target

100 net-new entries per cohort × 6 cohorts = 600 entries. The queue holds 669 candidates
(spare for authoring attrition: a candidate that turns out vulgar on research, or that the
pre-flight VARIANT-FORM / INFLECTION guard rejects, is skipped, not forced).

| Cohort | listed | dropped as already live or already queued | queued (dup: false) |
|---|---|---|---|
| Silent | 136 | 16 | 120 |
| Boomer | 142 | 33 | 109 |
| Gen X | 134 | 32 | 102 |
| Millennial | 138 | 35 | 103 |
| Gen Z | 133 | 23 | 110 |
| Gen Alpha | 131 | 6 | 125 |
| total | 814 | 145 | 669 |

Dedup set: every `word` and `slug` in the batches, every line of `data/dictionary-slugs.txt`,
every `docs/dictionary/*.html` basename, with `-genz` / `-slang` / decade suffixes stripped
(14,925 normalized keys). Cross-cohort: a term goes to the cohort that coined it and is listed
once (e.g. "noob" is Millennial; the Gen Alpha copy was dropped). Vulgarity and slurs were
left out at the list stage; "baddie"-class edgy-but-clean words are in.

Selection bias, on purpose: words a Fredericksburg father of a Gen-Z son and a Gen-Alpha
daughter in a Millennial-adjacent household will actually hear — Roblox / Fortnite /
Minecraft / YouTube vocabulary for Alpha, TikTok and dating-stage vocabulary for Z, the
2000s–10s internet for Millennials, Valley / hip-hop / grunge for X, counterculture and CB
radio for Boomers, swing-era and WWII GI slang for the Silent Generation (the grandparents'
dialect, which is why it belongs in a family dictionary).

## How the pipeline takes it (from the 2026-10-14 org-content run, 34 words)

- Batch size the pipeline handled per run: **10–12 entries** (oc1014-a 12, -b 12, -c 10).
  Pre-flight, KJV gate, and drift audit are per-batch; generate → rebuild → slugs → manifest
  → search-index → sitemaps → enhance → integrity audit run once per batch regardless of size
  and dominate wall-clock (the 1-entry baddie run took roughly five minutes, not timed to the
  second). Larger batches amortize that; 20–25 per batch is realistic once an author is warm,
  and the dict-batch skill's own norm is 10.
- At 12/batch: **50 pipeline runs** for 600 entries (6 cohorts × ~8–9 batches). At 20/batch:
  30 runs.
- Pushes: batch several pipeline runs per push (the 10-14 lane did 3 pushes for 34 words; the
  overnight contract caps a lane at 3–4 pushes). Suggest **1 push per cohort** = 6 pushes,
  each followed by the 5–7 min serial deploy, live 200 proof, and `bin/post-deploy-smoke.sh org`.
- Authoring is the real cost, not the pipeline. The 10-14 lane produced 34 Webster words in
  ~38 min of worker time on Opus 5.5 with a live Webster fetch per word. Slang entries skip the
  Webster fetch but need an etymology date check and a biblical reframe in the Aura/Cheugy
  register (~900–1,200 words of HTML-entity prose each, 4–5 verbatim KJV pairs pulled with
  `bin/kjv_lookup.py`). Working figure: **~1.5 min/entry authored + ~5 min per pipeline run**
  → one cohort of 100 ≈ 2.5 h author + 45 min pipeline + 1 deploy ≈ **3.5 h per cohort**,
  **~21 h for all six** if one worker runs it serially. Six parallel cohort lanes (one worktree
  each, one push each) collapse that to a single evening, at the price of six serial deploys.
- Tokens: ~2k output + ~6k context per entry ≈ 5M tokens for 600 entries, plus pipeline
  tool output. On the Claude Max subscription that is budget, not invoice; on API Opus 5.5
  pricing it is on the order of $75–150. Local models are not recommended for this lane:
  every entry has to pass the KJV fidelity gate verbatim and the drift audit's register check.

## Per-entry rules the author must keep (learned on baddie)

1. Slug suffix `-genz` only when the bare word already exists or is a common English word
   that will someday deserve its own entry (`cringe-genz`, `bet-genz`, `baddie-genz`). Otherwise
   bare (`aura`, `huzz`). For other cohorts no suffix convention exists yet; propose `-boomer`,
   `-genx`, `-mill`, `-alpha`, `-silent` on the same rule.
2. `pos` must name the cohort in the fixed form so the count above stays exact:
   `(Gen-Z slang)`, `(Gen Alpha slang)`, `(Millennial slang)`, `(Gen X slang)`,
   `(Boomer slang)`, `(Silent Generation slang)`.
3. Scriptures in 3-letter form (`Pro 31:30`, `1Pe 3:4`), text verbatim from
   `bin/kjv_lookup.py`; the gate exits 1 on any paraphrase.
4. `roots_lines` = list of strings (the Cheugy entry's list-of-lists shape is legacy and now
   fails pre-flight).
5. Add the card by hand to the right Decoded grid in `rebuild-dictionary.py` with a verdict
   (Redeemable / Neutral / Examine / Reject); the section pages are rebuilt from it. A Silent
   Generation page does not exist yet — building it needs a new section in
   `rebuild-dictionary.py` + `bin/build_section_pages.py` (one-time, ~1 h) and an entry in the
   `grep -vxE` exclusion list inside `bin/batch_pipeline.sh`'s regen-slugs step.
6. After the pipeline: `git checkout docs/sitemap.xml docs/sitemap-main.xml
   docs/sitemap-lexicon.xml docs/sitemap-dictionary.xml`, then hand-append the new `<url>`
   blocks to `sitemap-dictionary.xml` (the generator rewrites every lastmod and drops a child).
7. Expect `enhance_entry_pages.py` to touch ~50 unrelated pages (In-the-Text sections the
   grind never added). Benign; commit them with `git add docs/dictionary`.

## Proposed as the next org-content grind lane

Order: **Gen Z first** (the Principal's trigger, the son's dialect, and the richest existing
page to extend), then Gen Alpha (the daughter's), then Millennial, Gen X, Boomer, Silent
(needs the new Decoded page first). Awaiting Adam's confirmation on the 100-per-cohort scope
("I think") and on which cohort goes first.
