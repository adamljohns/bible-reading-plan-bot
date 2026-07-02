## ⏸️ PAUSED BY ADAM 2026-06-17 ~01:20 EDT — DO NOT RUN ROUNDS, DO NOT RE-ARM.
If a stale ScheduleWakeup fires: STOP immediately, do not merge, do not spawn agents, do not re-arm. Resume only on Adam's explicit say-so (he said "pause auto-runs till the end of the week"). R22's agents died on a session limit (resets 3:10am) and produced NO data — last good commit is R21 (32a9e2a12; fleet has since pushed on top). To resume later: pick up at R22 — build a fresh 60-church batch (corrected placeholder def, green-first then yellow, exclude /tmp/c3-attempted.txt which has 1,260 ids) and continue the pattern below.

# MOOP Directory — Enhancement Campaign 3 (Pastor + Social Enrichment)
Started: 2026-06-16 21:39 EDT · **Ends: 2026-06-17 21:39 EDT** (24h) · Event-driven (agent-completion notifications) + ~30-min fallback heartbeat.
Adam's directive (6/16): rapid 24h build to hit the 7,777 high-data-quality target. Scope chosen: **pastors + socials TOGETHER** (each batch fills pastor name AND facebook/youtube/instagram per church).
This file is UNTRACKED — never commit it. Update it at the end of every round.

## The target (CORRECTED 6/16 ~22:10) — ALREADY MET
- ⚠️ The initial "7,193 / 584-short" was a MEASUREMENT ARTIFACT: my placeholder regex had `^pastor\b`, which mislabeled every real "Pastor John Smith" name as a placeholder. With the CORRECTED definition (bare "Pastor"/"verify"/"see website"/"various" = placeholder; "Pastor <Name>" = REAL): high-quality (real pastor + scores) = **7,944 — already PAST 7,777 by 167.** Target met.
- Campaign continues per Adam's "rapid 24h build" intent, REFRAMED to deepen the genuine pool: **5,521 churches with a TRUE placeholder pastor + live website** ("Verify on church website" ×4,540 is the bulk, + empty/See website/Various/Unknown). Green-first. Plus socials across the board.
- CORRECTED placeholder def (used by both merge + batch builder): empty | /^(pastors?|tbd|n\/a|none|unknown|various|staff)\.?$/ | /verify|see website|see site|not published|search in progress|to be (announced|determined)|coming soon|^unknown/.

## Rules (non-negotiable, apply every round)
1. churches.json is ASCII-escaped, NO trailing newline. The merge (scripts/merge-pastor-enrichments.js) now uses scripts/lib/format-preserving-write.js — VERIFIED byte-safe (no-op = 1-line diff). Always `git diff --numstat docs/data/churches.json` before commit; a round is tens-to-hundreds of lines, never 50k.
2. Stage exact paths only; NEVER `git add -A docs/`. Push: `git push || (git pull --rebase --autostash && git push)`, then `git merge-base --is-ancestor HEAD origin/main`.
3. **NEVER guess a pastor. A wrong pastor is worse than none.** Agents return null pastor_name when the senior pastor isn't clearly identifiable. Only the SENIOR/LEAD (primary preaching) pastor — not youth/worship/kids/exec/campus.
4. Rubric enforcement is wired into the merge: a verified FEMALE senior pastor → overall + gender RED + needs-rating-review + note. Do NOT auto-promote any rating to green; enrichment only fills facts.
5. Socials: only real church-account URLs on the right host (facebook.com / youtube.com / instagram.com). Merge applies only if the field is currently empty.
6. After merge: `node generate-church-pages.js --only <changed ids>` (auto-rebuilds index + shards). Commit + push surgically.

## The pastor+social-enrichment pattern (per round)
1. Build batch: placeholder-pastor + website churches, green-first, ~60/round split into 3 files /tmp/c3-batch-{1,2,3}.json (20 each), fields {id,name,website,city_state,rating}.
2. Spawn 3 parallel research agents (Agent tool, general-purpose, run_in_background) — each researches its 20: fetch site /about /staff /leaders etc., extract SENIOR pastor + FB/YT/IG + pastor_is_female, write /tmp/c3-enriched-{1,2,3}.json as array of {id, pastor_name|null, pastor_source_url, website_status, facebook?, youtube?, instagram?, pastor_is_female}.
3. On all-3-complete: (a) NORMALIZE churches.json to ASCII canon FIRST — the fleet enrichment crons sometimes write it in literal-Unicode between my rounds (R8 hit this: 51k-line flip + their +1 church). Re-encoding before merge keeps the merge diff clean and the committed state always canon (idempotent no-op if already canon; data preserved): `node -e "const fs=require('fs');const d=JSON.parse(fs.readFileSync('docs/data/churches.json','utf8'));const esc=s=>s.replace(/[^\x00-\x7F]/g,c=>'\\\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));fs.writeFileSync('docs/data/churches.json',esc(JSON.stringify(d,null,2)))"` — if this produces a 50k diff, the fleet flipped it; that's expected, commit it as canon. (b) CLEAN each enriched file to ONLY its batch's ids: `node -e "for(const n of [1,2,3]){const b=new Set(require('/tmp/c3-batch-'+n+'.json').map(c=>c.id));const e=require('/tmp/c3-enriched-'+n+'.json').filter(x=>b.has(x.id));require('fs').writeFileSync('/tmp/c3-enriched-'+n+'.json',JSON.stringify(e,null,2))}"` (c) Merge: `node scripts/merge-pastor-enrichments.js --input /tmp/c3-enriched-1.json --input /tmp/c3-enriched-2.json --input /tmp/c3-enriched-3.json`. REVIEW summary + `git diff --numstat fa9ba1997 -- docs/data/churches.json` (vs a known-canon commit) should show only real changes before committing.
4. Regen changed ids, commit, push, verify. Re-pre-flag the batch ids as attempted so the next round's batch builder skips them (filter pool by an _c3_attempted set tracked in /tmp/c3-attempted.txt — append each round's ids).
5. `rm -f /tmp/c3-enriched-*.json` (delete BEFORE spawning so stale data can't accumulate), then spawn next round's agents. Re-arm ScheduleWakeup 1800s fallback.

## Round log
- [x] **C3-R1 (21:39) — VALIDATION ROUND, done. Commit 1537b5984.** 3 agents researched 60 green churches; quality EXCELLENT (real senior-pastor names, source URLs, honest blanks on timeouts/404/vacant/first-name-only — verified John Starke@Apostles Uptown, Steve Jeffery@All Saints CREC). Applied 19 pastors + 7 socials to genuine placeholders. KEY FINDING: target already met (see corrected math above). Hardened merge: format-safe write (verified), socials, female→RED, corrected placeholder detection.
- [x] **C3-R2 (~22:10) — done. Commit 478ec5438.** +36 pastors, +28 socials, 43 pages. Female senior pastor Rev. Jenny Davidson (cornerstone-methodist-graham-tx-gmc) auto-flagged RED gender+overall ✅ (rubric enforcement confirmed working). 0 wasted on already-real pastors — corrected targeting clean. Attempted now 120.
- [x] **C3-R3 (~22:24) — done. Commit b61d165ce.** +44 pastors, +40 socials, 51 pages (BEST round). 2 female→RED (Becky Waugaman/Des Moines Vineyard, Jill Jackson-Sears/First GMC Dallas). Stale-file guard caught enriched-1 holding 40 records (20 stale R2) — cleaned to batch ids before merge; added rm-before-spawn + clean-to-batch-ids to the pattern. Attempted 180.
- [x] **C3-R4 (~22:40) — done. Commit f3f1c3d72.** +40 pastors, +34 socials, 49 pages, 0 female. Clean run with hardened pattern. Attempted 240.
- [x] **C3-R5 — done. Commit c440be408.** +29 pastors, +35 socials, 1 female→RED (Rev. Carolyn Poteet, Mt. Lebanon EPC). 5-ROUND MILESTONE: high-quality 7,944→**8,148 (+204)**; social-coverage churches +56 net. Attempted 300.
- [x] **C3-R6 — done. Commit 60fce8255.** +41 pastors, +59 socials (best social round), 1 female→RED (Brenda Wood, Solid Rock GMC). One record's website = a Porsche club → flagged not_a_church. Attempted 360.
- [x] **C3-R7 — done. Commit fa9ba1997.** +40 pastors, +67 socials. Attempted 420.
- [x] **C3-R8 — done. Commits ee02f58de + bc2b1b7f3 (normalize).** +29 pastors, +40 socials, green nearly exhausted (14g/46y). ⚠️ FLEET FORMAT COLLISION: the fleet enrichment cron wrote churches.json in literal-Unicode (uncommitted) between R7 and R8 + added 1 church (28,512→28,513); my R8 merge preserved literal → 51k-line flip. FIXED: re-encoded to ASCII canon (bc2b1b7f3); added normalize-before-merge to the pattern so it self-corrects. Attempted 480.
- [x] **C3-R9 — done. Commit a232d367f.** +30 pastors, +38 socials, normalize-first guard worked (no fleet flip, clean diff). Attempted 540.
- [x] **C3-R10 — done. Commit 0e85c1818.** +24 pastors, +39 socials. An agent caught WebFetch cache cross-contamination + set null (added "distrust cache bleed → null" to agent prompt). 10-ROUND MILESTONE: high-quality 7,944→**8,254 (+310)**; social-coverage churches +172 net. Attempted 600.
- [x] **C3-R11 — done. Commit bf626998b.** +25 pastors, +32 socials. Agents flagged WRONG-WEBSITE records (church's website field points to a different church) + defunct domains. Attempted 660.
- [x] **C3-R12 — done. Commit 0722f59f3.** +35 pastors, +49 socials. Agent flagged a duplicate (Auburn Baptist Tupelo x2). Attempted 720.
- [x] **C3-R13 — done. Commit bce1ced22.** +34 pastors, +37 socials. Attempted 780.
- [x] **C3-R14 — done. Commit 8718eade6.** +39 pastors, +47 socials. Attempted 840.
- [x] **C3-R15 — done. Commit 633f3972b.** +34 pastors, +55 socials. 15-ROUND MILESTONE: high-quality 7,944→**8,303 (+359)**; social-coverage churches +256 net. Attempted 900.
- [x] **C3-R16 — done. Commit dd4636f2e.** +32 pastors, +72 socials. Attempted 960.
- [x] **C3-R17 — done. Commit 765b293de.** +28 pastors, +80 socials. CROSSED 1,000 CHURCHES WORKED (1,020 attempted). Batch 1 hit a cluster of independent Bible Baptist sites with TLS-cert mismatches (HTTPS-forced fetch can't reach http-only) → honest blanks.
- [x] **C3-R18 — done. Commit c48b2ae96.** +38 pastors, +46 socials. Attempted 1,080.
- [x] **C3-R19 — done. Commit ca81d6d28.** +27 pastors, +43 socials. Attempted 1,140.
- [x] **C3-R20 — done. Commit a27656d6d.** +28 pastors, +34 socials. 1,200 CHURCHES WORKED (20 rounds). Added "prefer staff page over stale nav link" to agent prompt.
- [x] **C3-R21 — done. Commit 32a9e2a12.** +38 pastors, +43 socials. 21-ROUND MILESTONE: high-quality 7,944→**8,350 (+406)**; social-coverage churches +476 net. Attempted 1,260.
- [ ] **C3-R22 — in flight.** 3 agents on 60 yellow (pool 4,321). Agent IDs: ae17fdc3f5de24d20, a0175bea7dcc11d04, ac626edf2a9ab96cd. Campaign total through R21: ~664 pastors + ~1,023 socials, 5 female→RED. CLOSEOUT notes: (1) fleet format→ASCII canon; (2) wrong-website records; (3) duplicates/merged churches. R28: next milestone recompute.

## Plan
- [ ] **C3-R4+** Continue 60/round (3 agents × 20) over the ~5,461 TRUE-placeholder pool, green-first then yellow, appending attempted ids each round. ~36 pastors + ~28 socials/round actual (R2 baseline). Recompute high-quality count every ~6 rounds (already 7,944; climbing). When green placeholders exhaust, the sort naturally moves to yellow.
- [ ] Periodic (every ~6 rounds): recompute the high-quality count + social coverage; dedup audit (find_true_duplicates.py) since new pastor data can reveal same-church dups.
- [ ] **Closeout (after 21:39 EDT 6/17 or pool exhausted):** final commit; update memory roadmap with new high-quality count + social/pastor coverage; summary for Adam; delete this file. Do NOT re-arm.

## Notes
- Engine differs from Campaigns 1-2: research AGENTS (Agent tool, token-heavy) not a mechanical scraper, because pastor-name extraction needs judgment (which one is the SENIOR pastor) and the "honest blank" rule. scrape-church-pastors.js (mechanical) is the fallback if agents are too slow/costly.
- Agent IDs R1: a69e21b19fcb87e93 (b1), a0d7ced8bcf0d3820 (b2), a2b0411440bb90f1d (b3).
- Do NOT touch: docs/churches-dc.html, docs/churches-virginia.html (Hermes), any readings/* fleet files, worship-slides.html / sitemap-worship.xml (other-project, currently dirty in tree).
