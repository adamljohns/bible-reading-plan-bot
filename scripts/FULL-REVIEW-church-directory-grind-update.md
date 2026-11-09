# Draft update for ~/.openclaw/shared-memory/context/church-directory-grind.md

For Max to apply. Insert the section below directly under the title block, above
"## 2026-07-11 deltas". It only adds; nothing in the existing doc is retracted.
Two existing lines also need a touch (listed at the end).

---

## 2026-11-08 deltas — FULL REVIEW mode (read this; it is new)

Adam's order (2026-11-08): "Let's really make the review and enrichment of churches do everything it's supposed to do." The fresh/retry/social lanes only ever look at churches with a PLACEHOLDER pastor, so an imported name is never re-checked and no round ever assesses doctrine. A **full review** reads a church's own site end to end and proposes every correction, with evidence, into a **review patch**. It never writes churches.json directly.

**What one full-review round does, per church (local model only — LM Studio `gemma-4-31b-it` on :1234, the grind's extractor; no paid APIs):**
1. **Exists?** Reads the homepage plus up to 9 inner pages (staff/leadership/clergy, about, beliefs, ministries, worship/times), or the Facebook page when that is all it has. At most one request per second per host. Identity check: the site must name the stored city, street or ZIP. A site that describes a church somewhere else (e.g. `calvary-memorial-church-oak-park-il` carrying Navarre MN data) is flagged **wrong-church data** and everything from it is HOLD-only. One free local SearXNG query (never Brave) looks for the real site.
2. **Pastor.** Extracts the current senior/lead pastor and the roster verbatim, compares with the stored values (real names included, not just placeholders), proposes the replacement, stamps `pastor_source` (exact URL) and `pastor_fetched_at`. A female senior/lead pastor is RED minimum and always HOLD.
3. **Rubric — written rules only.** A category score or overall rating is proposed ONLY when a rule published on `usmcmin.org/directory-methodology.html` maps the evidence to that level, and the patch cites that rule's own text next to the church-page quote. Today's published rules: "Female senior pastor → RED minimum." (gender, leadership, overall), "LGBTQ-affirming denomination → RED minimum." (denominational, overall; fires only when the church's own name/about text states the affiliation), "Prosperity gospel → BLACK." (overall). A score also needs an on-topic quote, or it stays null. Whatever the local model or a keyword signal suggests beyond the rules (e.g. BLACK for an inclusive "orientation" welcome, women in non-senior pastoral office, a model's RED reading of a category) becomes a separate HOLD item titled `needs-ruling: …` with its evidence; Chaps and Adam decide, and a decision that should repeat gets published as a rule first. Female clergy are read only from page evidence (pronouns, spouse, an explicit role); a first-name-list match alone is a HOLD item marked `unconfirmed` and drives no rating. Evidence ranking prefers staff/about prose and the church's own printed name over menu and nav lines.
   *(Superseded wording, kept for the record:)* Scores all 10 categories (scripture, christology, gender, soteriology, preaching, cultural, leadership, mission, mens_discipleship, denominational), each with a one-line note, a verbatim quote and the source URL, and proposes `overall_rating` / `overall_label` per the legend. Strong signals: women ordained as pastors/elders; LGBT-affirming or pride language; the denomination's official position (TEC, ELCA, PCUSA, UCC, UMC post-2024, Disciples, RCA, MCUSA) as a prior that fires only when the church's own site states the affiliation and is overridden only by stronger congregation-specific evidence; confessional statements (WCF, 1689, 3FU, BFM2000); a men's ministry.
4. **Profile fill.** Service times, founded year, `has_mens_ministry`, `has_kids_ministry`, Facebook/Instagram/YouTube, website moves, address corrections (address changes are always HOLD and set `_geocode_stale` for the geocoder).
5. **Duplicates.** Same street+ZIP or same website host as another record → HOLD flag for `scripts/merge-duplicate-churches.js`. Never deleted.

**Safety gates (non-negotiable):**
- Every proposed change carries an evidence quote AND a URL. No quote or no URL = no change. Quotes are mechanically checked to appear verbatim on the fetched page; the model's unquotable claims are dropped before the patch is built.
- Any proposal that moves a church to RED or BLACK, or off GREEN, goes to the **HOLD queue** (`data/full-review/hold-queue.json`) for **Chaps QA**. It never auto-applies.
- Only HIGH-confidence changes auto-apply: a fill of an empty field, or a pastor set/replace where the lead role is explicit, quoted, the stored name is gone from the site, and the site's identity is confirmed. Everything else is HOLD.
- Dry run is the default. The live apply (`FULL_REVIEW_MODE=live`) needs Adam's GO.

**Files (repo `bible-reading-plan-bot`):**
- `scripts/select-enrichment-batch.js --full-review [--count 25] [--include id,id]` — selection order: (a) denominations that ordain women (affirming mainline first, then ABC-USA, CBF, AoG, Nazarene, ...); (b) within 25 mi of Fredericksburg; (c) yellow / assessment pending, oldest review first; (d) the rest. Default 25, max 60. Skips churches fully reviewed in the last 180 days and churches with a pending HOLD.
- `scripts/full-review-fetch.py` — reads the sites, runs the local model, verifies every quote.
- `scripts/full-review-build-patch.js` — rubric engine + gates → `data/full-review/rounds/<round>/review-patch.json`, `.../hold.json`, the cumulative `data/full-review/hold-queue.json`, and one public counts row in `docs/data/full-review-stats.json`. Read-only on churches.json (sha256 checked before/after).
- `scripts/apply-full-review-patch.js` — applies auto changes + QA-approved holds; preview by default; `--apply` regenerates pages and runs `scripts/check-consistency.js`; `--ship` pushes path-scoped via `scripts/full-review-ship.sh` from the autopilot worktree only.
- `scripts/full-review-round.sh` — one round end to end; shares the grind's lock file, so a full review and a grind round never overlap.
- Patch/HOLD files live under `data/` (not `docs/`), so unreviewed RED/BLACK proposals never publish. Only the counts are public.

**How to run one (Chaps + Hermes only — requires `exec`; only when Adam asks):**
```
/bin/bash /Users/moop_bot_pro/.openclaw/bin/trigger-directory-grind.sh full-review 25          # DRY RUN: patch + HOLD queue, nothing applied
/bin/bash /Users/moop_bot_pro/.openclaw/bin/trigger-directory-grind.sh full-review 25 --live   # Adam's GO only: apply auto changes + ship
```
The plain `trigger-directory-grind.sh 25` still starts an ordinary enrichment round, exactly as before. After firing, say it is running; do not claim results you have not seen. Results: `usmcmin.org/grind-report.html` → "Full review rounds" (reviewed, changed, held, applied).

**Chaps QA of the HOLD queue:** rows have `kind` = `change` (a proposed field change; approve/reject), `flag` (duplicate / wrong-church; approved ones are queued for the merge tool), `ruling` (needs-ruling: a judgment no published rule covers — decide it with Adam; it never applies by itself), or `unconfirmed` (female clergy by name only — confirm from the church before anything changes). Open `data/full-review/hold-queue.json`; for each row with `qa_status: "pending"`, open `evidence.url`, confirm `evidence.quote` is on that page and supports the change (for ratings, also that `rule.text` is the published rule and maps the evidence), then set `qa_status` to `approved` or `rejected` with `qa_by` and a one-line `qa_note`. The applier applies `approved` rows only, and never rows marked `dry_run: true`. Duplicate / wrong-church flags that are approved are queued in `data/full-review/approved-duplicates.json` for the merge tool; nothing is deleted.

---

**Two existing lines to touch:**
- "## The moving parts": add a bullet — "`scripts/full-review-round.sh` — FULL REVIEW (see 2026-11-08 deltas): re-checks real pastors and scores the rubric into a review patch + HOLD queue; dry run by default."
- "## How to run a round on demand": add the two `full-review` trigger lines above under the existing command.

The staged trigger is `scripts/ops/trigger-directory-grind.sh` in the branch; it is a drop-in replacement for `~/.openclaw/bin/trigger-directory-grind.sh` (old call shape unchanged). Install it only after `feat/church-full-review` is merged to main and the autopilot worktree has the new scripts, or the `full-review` path reports "runner missing".
