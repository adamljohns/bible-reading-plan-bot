# Worship Songbook handoff → Cursor (2026-09-13)

Adam's worship-leader resource at **usmcmin.org/worship.html** — chord charts + lyrics,
transposable, printable, with a Set List builder. Was at 5,777 songs a few days ago;
Claude (Opus/Sonnet, this repo) pushed it to **6,007 songs + 438 curated YouTube videos**
across three days of 4-agent research waves. Adam just raised the target again:

> "I think my target will be 7,777 total songs of high quality and impact and pleasing
> to look at, so formatted well, and accurate chords and links"

Read that as **three simultaneous goals, not one**: grow the count (+1,770 from here),
verify/polish what already exists (chords, credits, formatting), and keep every video
link accurate. Do not chase the number at the expense of the other two — Adam has said
"hopefully all the listings are perfect" more than once, and the video-linking pass is
explicitly how attribution errors get caught (see "Known defect classes" below).

## Where everything lives

- **Repo:** `~/bible-reading-plan-bot` (GitHub Pages serves from `docs/`, deploys off `main`).
- **You should work in a clean worktree**, not the primary checkout — a parallel Claude
  session and fleet crons commit to `main` constantly:
  ```bash
  cd ~/bible-reading-plan-bot-worship-sprint   # already exists, branch worship-2777
  git fetch origin main && git rebase origin/main
  ```
  If that worktree is busy/locked, make a new one: `git worktree add ../bible-reading-plan-bot-worship-cursor -b worship-cursor origin/main`.
- **The skill (read this first, it's the whole operating manual):**
  `.claude/skills/worship-directory/SKILL.md` — defines the 4 entry kinds, the 6-step
  add pipeline (source → assemble → **link videos, required every batch** → genre-tag →
  regenerate+QA → publish), and three known defect classes agents keep introducing.
- **Runbook:** `.claude/skills/worship-directory/RUNBOOK.md` — loop/burst procedure if
  you want to automate this on a schedule.
- **Live program state:** `.claude/skills/worship-directory/scripts/state.json` — target,
  phase, which author-wells are used, video backlog count. **Read it before starting,
  update it as you go** — it's the shared memory between whoever works this next.

## The generator pipeline

```
docs/data/worship-songs.json          canonical DB (generated, don't hand-edit)
docs/data/worship-extra-songs.json    durable: manual/agent-added songs, merged at ingest
docs/data/worship-nonworship.json     durable: slugs hidden from "worship only" filter
docs/data/worship-purged.json         durable: hard-removed slugs (deleted-from-JSON-alone
                                       gets resurrected on next --ingest, use this instead)
docs/data/worship-overrides.json      durable: {youtube, slides, key} per slug
data/worship-hymn-bank.json           durable surplus bank — verified hymns not yet needed
generate-worship-pages.js             the generator: --ingest re-reads archive+extras,
                                       --pages regenerates HTML only (faster, no re-merge)
```

Never edit `worship-songs.json` directly — it's overwritten by `--ingest`. Every change
goes into one of the durable `docs/data/*.json` files above, then regenerate.

## Scripts you'll actually run (`.claude/skills/worship-directory/scripts/`)

| Script | Purpose |
|---|---|
| `worship-sprint.js` | Workflow-tool script. Modes: `cat` (hymn category/author well), `psalter` (metrical psalm range), `verify` (lyric fidelity audit), `video` (find a recording). Returns `{hymns, videos}` — a single wave can mix source + video cats. |
| `author-well-bank.json` | **The sourcing backlog now** — 69 sequential author/collection wells (~1,380 potential hymns). The old `category-bank.json` (72 thematic niches) is EXHAUSTED, don't reopen it. |
| `apply-round.js` | Extract PD hymns from a workflow task-output file. |
| `normalize-hymns.js` | **Run this on every batch before assembling.** Dedups by accent-folded title (not slug — see gotcha below), sanitizes keys, strips catalog-number suffixes agents append ("(HLS No. 80)"), tidies author/source strings. |
| `trim-to-gap.js` | Pick exactly N best hymns from a batch, bank the surplus. |
| `video-worklist.js` | Next N songs needing video, thinnest page first (contemporary `linksOnly` pages lead). |
| `apply-video-ids.js` | Gate for researched video IDs — rejects malformed/unknown/low-confidence/duplicate. **Never loosen this. Let it refuse.** |
| `build-linksonly.js` | Turns `[[title,artist,writers,year,key],…]` into copyright-safe contemporary entries. |
| `chord-lint.js` | Accuracy audit → `reports/chord-lint.json`. |
| `../../../scripts/assemble-worship-additions.js` | Merges a batch into extras with generator-consistent dedup. |

## The proven sourcing method (yield ladder — do NOT skip this)

Verified over 60 waves, recorded in `state.json`:

- **Prolific single author, worked SEQUENTIALLY by hymn/scripture number** → 82–99% fresh.
- Multi-work collection, 2nd/3rd pass → 69–87% fresh.
- Mixed anthology → 52–61% fresh.
- **Thematic category → 29% fresh. Avoid.** This is why `category-bank.json` (72 niches)
  is retired — every hymnwriter already wrote on comfort/prayer/praise and it's mined out.

**Deepest unmined wells right now** (from `author-well-bank.json`, index = position used
so far is `wellsUsed` in state.json, currently `[0,5,16,28,1,6,17,29,30,2,18]` — 11 of 69
consumed):
- Charles Wesley — wrote ~6,500 hymns, only ~280 in the DB. *Short Hymns on Select
  Passages of the Holy Scriptures* (1762) alone is 2,030 hymns walking the whole Bible
  sequentially — clean source: Duke Center for Studies in the Wesleyan Tradition PDFs.
- Benjamin Beddome — 830 total, wells for 1–830 in 120-hymn chunks; ~660–830 untouched.
- Thomas Kelly — 765 total, mostly untouched past ~320.
- Horatius Bonar, John Berridge (past 342), James Montgomery, Fanny Crosby (thousands),
  Sternhold & Hopkins *Old Version* 1562 (150 psalms, only ~19 in DB), Catherine
  Winkworth's German-chorale translations, John Mason Neale, Edward Caswall.

Run 4 agents per wave via the Workflow tool, `scriptPath` =
`.claude/skills/worship-directory/scripts/worship-sprint.js`:

```js
Workflow({
  scriptPath: ".../worship-sprint.js",
  args: { round: <next>, cats: [
    {type:"cat", name:"<well text from author-well-bank.json>"},
    {type:"cat", name:"<another well>"},
    {type:"cat", name:"<another well>"},
    {type:"cat", name:"<another well>"},
  ]}
})
```
A wave can mix 2 source cats + 2 `{type:"video", batch:[...]}` cats — the script returns
`hymns` and `videos` together now, so both lanes move under one 4-agent cap.

**Stay at 4 agents per wave.** Waves of 19–26 exhausted the account's usage window four
times running and returned nothing; 4-agent waves have gone through cleanly repeatedly.
If you're hitting session/rate limits with 4, drop to 2.

**⚠️ Gotcha proven in this session:** if a wave partially fails (some agents hit a
session limit), `Workflow({resumeFromRunId: ...})` does **not** cleanly replay only the
failed agents — it can re-run ones that already succeeded (returning the same hymns with
slightly different formatting) while the failed ones fail again. **Launch a fresh
Workflow call with just the failed seams as `cats`, don't rely on resume.**

## After every source wave (steps 2–6 of the SKILL.md pipeline)

```bash
node .claude/skills/worship-directory/scripts/apply-round.js <task-output.json> reports/hymns-rN.json
node .claude/skills/worship-directory/scripts/normalize-hymns.js reports/hymns-rN.json
node scripts/assemble-worship-additions.js .claude/skills/worship-directory/reports/empty.json reports/hymns-rN.json
node generate-worship-pages.js --ingest
node .claude/skills/worship-directory/scripts/chord-lint.js
```

Check before committing: duplicate slugs = 0, hero count moved by what you expected, PD
missing-credit = 0, lint count not worse than the last check (currently steady at 24
flagged, all legitimate authentic notation — see "Accuracy work" below), and spot-check
one new page's credit line.

**Video linking is REQUIRED for every batch, same session** — not deferred polish. Run
`video-worklist.js 20`, feed the entries to a `{type:"video"}` wave, gate with
`apply-video-ids.js`. Contemporary `linksOnly` pages lead the worklist because they have
no lyrics by law — the recording *is* the page, and because **video research is the only
thing that reliably catches wrong-artist/phantom-song errors** in agent-sourced
contemporary batches (see next section).

## Publish

```bash
git add -A
git diff --cached --quiet || git commit -m "Worship wave N: ..."
git fetch origin main -q && git rebase origin/main && git push origin worship-cursor:main
```
`git diff --cached --quiet` before committing matters — zsh/bash word-splitting has
caused at least one silent no-op push in this project's history. **Never
`git checkout --theirs .` to resolve a worktree conflict** — it silently reverted the
worship data files once and got committed with a false count claim. If you hit a rebase
conflict on the worship data files, resolve them by hand and re-check the song count
before committing.

## Known defect classes (from SKILL.md — assume any memory-built batch has these)

1. **Wrong artist** — song is real, credit isn't (*Digno Es el Señor* is Marcela
   Gandara's, not Marcos Witt's).
2. **Phantom songs** — artist never recorded anything by that title. Purge, don't guess
   a substitute.
3. **Duplicates of Adam's own chord charts** — an info page for a song his archive
   already has as a real chart. The chart always wins. Verify by distinctive lyric before
   removing — some title collisions are genuinely different songs.

Never build a contemporary/CCM batch from memory alone for non-English or less-common
artists — verify via the video-research step, which forces a real look-up.

## Legal rules (non-negotiable)

- **Never reproduce copyrighted lyrics.** Contemporary/CCM songs are `linksOnly: true`
  pages — copyright notice + full writer credits + YouTube button, no lyrics, ever.
- **Never invent hymn lyrics.** No verified public-domain source (Hymnary.org,
  CyberHymnal/Hymntime, Timeless Truths, Wikisource, denominational archive PDFs like
  the Duke CSWT Wesley texts) → the hymn doesn't go in.
- Public domain = published before 1929, or author+translator both dead 70+ years.
- Give real credit — writers, year, source. "Give credit where credit is due" is a
  standing instruction from Adam; the credits are the point of these pages.

## Accuracy work (the polish half of "7,777 of high quality")

`chord-lint.js` → `reports/chord-lint.json` currently flags 24 songs, all "garbled
chords" — **before touching any of them, read the actual chart.** The archive has
authentic notation that looks wrong and isn't: fret diagrams (`G-(320033)`), bass runs
(`/C# /B /A`), tuning notes, per-chart shorthand (`Gs` for Gsus). A chord token repeating
3+ times in one chart is that chart's convention, not corruption. Only fix against a
verified source.

Other open polish items, all listed in `state.json.polishQueue`:
- `reports/alternate-title-pairs.json` — songs that legitimately appear twice under
  different titles (*You Are My All in All* / *All in All*); they intentionally share a
  video ID. Not a bug.
- ~94 songs missing a `key`.
- Missing-writer-credit sweep.
- 47 surplus hymns already verified and sitting in `data/worship-hymn-bank.json` — use
  these to backfill before sourcing new ones if you ever need to hit an exact number.

## Formatting / "pleasing to look at"

The page templates are generated by `generate-worship-pages.js` from
`docs/worship.html` (index) and `docs/worship/<slug>.html` (per-song). If Adam wants
visual/layout polish, that's a generator-template change, not a data change — read
`generate-worship-pages.js` before touching HTML structure so the transpose/print/Set
List/video-embed features don't break. Don't hand-edit generated `docs/worship/*.html`
files; edit the generator and re-run `--pages`.

## Current numbers (2026-09-13, last commit `96d0d411885`)

- **6,007 songs** live (5,331+ worship & praise, 446 contemporary, 35 Christmas — re-run
  the hero-line grep after your first wave, it'll have moved).
- **438 curated YouTube videos** applied, all high-confidence, all verified official
  artist/label channels.
- **Gap to 7,777 = 1,770 songs.**
- Video backlog: ~5,570 songs total without video, but only ~215 of those are
  `linksOnly` contemporary pages — **that's the tier that actually matters**, since PD
  hymn pages are already complete without a video (lyrics + chords are the page).
- Lint: 24 flagged, steady, all legitimate.
- Bank: 47 verified hymns ready to deploy.

Good luck — this has been a genuinely fun grind. The deepest well by far is Charles
Wesley; start there.
