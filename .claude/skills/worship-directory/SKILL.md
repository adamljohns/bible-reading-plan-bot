---
name: worship-directory
description: Grow and maintain the Worship Songbook at docs/data/worship-songs.json (usmcmin.org/worship.html) — add public-domain hymns via research agents, add contemporary/CCM songs as copyright-safe info pages, attach curated YouTube videos, audit chord and lyric accuracy, and publish. Use whenever the user wants to grow the songbook toward its target ("more worship songs," "add contemporary," "push to 3,777"), add a genre or artist (gospel, Spanish worship, kids/VBS, southern gospel, metrical psalms, a specific hymnwriter), fix or verify chords and lyrics, link videos to songs, adjust the worship-vs-CCM split, or run a dream-loop/hourly burst on the directory. Triggers on "worship songbook," "worship directory," "worship.html," "add songs," "chord accuracy," or any song-count target for usmcmin.org.
---

# Worship Songbook — grow, verify, publish

The songbook is a worship-leader resource: chords charted over the lyrics, transposable,
printable, with a Set List builder. It mixes four kinds of entries, and **which kind you are
adding decides everything else**:

| Kind | `ext` | Body | Legal rule |
| --- | --- | --- | --- |
| Adam's chord charts | `crd` / `tab` | real chords over lyrics, from his archive | never edit the source archive |
| Public-domain hymns | `hymn` | verified lyrics, `publicDomain: true` | pre-1929 / author dead 70+ yrs, **lyrics from a real source, never invented** |
| Contemporary & CCM | `contemporary` | copyright notice only, `linksOnly: true` | **never reproduce lyrics** — credits + video + SongSelect pointer |
| Songbook charts | `crd` | parsed from his `.doc` songbooks | same as charts |

## At-a-glance

| Path (relative to this SKILL.md) | Purpose |
| --- | --- |
| `RUNBOOK.md` | The loop/burst procedure: gates, GROW/VERIFY lanes, publish steps. Read when running hourly bursts. |
| `scripts/state.json` | Live program state — target, phase, wave queue, capacity gate, cron id. |
| `scripts/worship-sprint.js` | Workflow script. Modes: hymn categories, `psalter` ranges, `verify` (lyric fidelity), `video` (find recordings). |
| `scripts/category-bank.json` | 72 untapped public-domain hymn niches for sourcing waves. |
| `scripts/apply-round.js` | Task output → hymns JSON for the assembler. |
| `scripts/trim-to-gap.js` | Land exactly on a target; surplus banks to `data/worship-hymn-bank.json`. |
| `scripts/build-linksonly.js` | `[[title, artist, writers, year, key], …]` → copyright-safe contemporary entries. |
| `scripts/video-worklist.js` | Next N songs needing a video, thinnest-page-first. |
| `scripts/apply-video-ids.js` | Validates + merges researched video IDs. Rejects malformed, duplicate, low-confidence. |
| `scripts/chord-lint.js` | Chord/lyric accuracy audit → `reports/chord-lint.json`. |
| `../../../scripts/assemble-worship-additions.js` | Repo script: merges songs into extras with generator-consistent dedup. |

Work in a clean worktree (fleet crons commit to main constantly). Publish = commit, `git fetch origin main`,
`git rebase origin/main`, `git push origin <branch>:main`. **Never `git add -A` in the main checkout.**

## The add pipeline — every addition runs all six steps

Steps 1–2 vary by what you're adding. **Steps 3–6 are the same every time, and step 3 is not optional:
a song without a video is a thinner page than it needs to be, so new songs get videos in the same
session they're added.**

### 1. Source

**Public-domain hymns** — spawn a wave with the Workflow tool, `scriptPath` = `scripts/worship-sprint.js`:

```
args: {"round": 8, "cats": [{"type":"cat","name":"<niche from category-bank.json>"}, …]}
```

**Keep waves to 4 agents.** Waves of 19–26 exhausted the account's usage window four times running
and returned nothing; 4-agent waves have gone 4-for-4. Pop niches off `category-bank.json` and
advance `catIndex` in state. Psalm ranges use `{"type":"psalter","range":"1-19"}`.

**Contemporary/CCM** — no agents needed. Write `[[title, artist, writers, year, key], …]` to
`reports/batch-<name>.json` and run:

```bash
node .claude/skills/worship-directory/scripts/build-linksonly.js reports/batch-<name>.json reports/<name>-songs.json
```

Get the writers right — the credits are the whole point of these pages ("give credit where credit is due").

### 2. Assemble

```bash
node tools/../scripts/assemble-worship-additions.js <songbook.json> <hymns.json>
```

Pass `.claude/skills/worship-directory/reports/empty.json` for whichever slot you aren't using.
Dedup against the live directory and extras is automatic. For hymns, run `apply-round.js` on the
task output first; normalize keys like `"E-flat (Martyrdom)"` → `"Eb"`.

### 3. Link videos — REQUIRED for every batch

```bash
node .claude/skills/worship-directory/scripts/video-worklist.js 40
```

That writes `reports/video-worklist.json`, thinnest pages first (contemporary `linksOnly` pages lead —
with no lyrics by law, the recording *is* the page). Feed it to a video wave (4 agents, ~10 songs each):

```
args: {"mode":"video", "round": 8, "cats": [{"type":"video","batch":"<JSON of ~10 worklist entries>"}, …]}
```

Then gate the results:

```bash
node .claude/skills/worship-directory/scripts/apply-video-ids.js <task-output.json>
```

It refuses malformed IDs, unknown slugs, duplicates, and anything the agent marked low-confidence.
**Let it refuse.** A wrong video on a worship song is worse than no video — never loosen the gate,
never hand-add an ID you have not seen, and never paste a full URL where an ID belongs.

One known-good exception to the duplicate rule: the directory carries some songs twice under
alternate titles (*You Are My All in All* / *All in All*) and some carols as both chart and tab, so a
shared ID there is correct, not a mistake. Those pairs are listed in
`reports/alternate-title-pairs.json`; add such a link by hand after confirming the pair, and keep the
gate strict for everything else.

If agent capacity is dry, the batch still ships — leave the videos for the next burst and note the
backlog in state. That's the only acceptable reason to skip step 3.

### 4. Genre-tag honestly

The hero splits the count into worship & praise vs Christian contemporary & rock, and the
"🎵 Worship only" chip filters to congregational songs. Add slugs of radio/performance pieces to
`docs/data/worship-nonworship.json`; leave genuinely congregational songs (including gospel like
*Total Praise* or *Every Praise*) out of it. Hiding real worship songs, or counting radio singles as
worship, both make the number a lie.

### 5. Regenerate + QA

```bash
node generate-worship-pages.js --ingest     # re-reads archive + merges extras
node .claude/skills/worship-directory/scripts/chord-lint.js
```

Check: duplicate slugs = 0, the hero count moved by what you expected, one new page spot-checked for
its credit line, lint count not worse than before.

### 6. Publish

```bash
git add -A && git commit -m "Worship: …"
git fetch origin main -q && git rebase origin/main && git push origin <branch>:main
```

## Accuracy work (the VERIFY lane)

`chord-lint.js` flags garbled chord lines, encoding junk, and truncated charts. Before "fixing"
anything it flags, **read the actual chart** — the archive is full of authentic notation that looks
wrong and isn't: fret diagrams (`G-(320033)`), bass runs (`/C# /B /A`), tuning notes, per-chart
shorthand (`Gs` for Gsus, `Emag7`), and complete-but-short praise choruses. The lint already knows
these; when it flags something new, assume the chart is right until a source says otherwise. A token
that repeats 3+ times in one chart is that chart's convention, not corruption.

Lyric fidelity for agent-added hymns uses `{"mode":"verify"}` waves against Hymnary /
thewestminsterstandard.org / Wikisource. Fix from the source or remove via `docs/data/worship-purged.json`.

## Invariants

- **Never reproduce copyrighted lyrics.** Contemporary songs are `linksOnly` pages, always.
- **Never invent hymn lyrics.** No verified source → the hymn doesn't go in.
- **Never edit the source chord archive.** Corrections go in extras or overrides.
- Removals go in `docs/data/worship-purged.json` (durable) — deleting from the JSON alone gets
  resurrected by the next `--ingest`.
- Surplus verified hymns bank to `data/worship-hymn-bank.json`. Nothing verified is ever thrown away.
- Watch for parallel sessions (Adam runs more than one agent) — re-read state and rebase before writing.
