---
name: watch-leadership-changes
description: Catch and record pastoral transitions across the MOOP Church Directory — retirements, resignations, interim seasons, and announced successor candidates — by reading a church's website, Facebook, and recent news. Use whenever the user asks to "check for pastor changes", "watch for retirements", "update [church] leadership", "find pastoral transitions", "who is the new pastor", or wants green-rated churches monitored for a change in the pulpit. Writes a structured pastor_transition record via apply-enrichment-round.js; the current pastor field is left intact until the handoff completes, and a transition never moves a rating on its own (a female candidate is a human-review flag, not an automatic RED, since a nominee is not the installed pastor). Triggers in the bible-reading-plan-bot repo.
---

# Watch Leadership Changes

A church's pulpit changes hands more often than its address does, and a directory that still names a pastor who retired two years ago reads as stale and untrustworthy. This skill turns the public record of a transition (the church's own website, its Facebook, a denominational note, a local news item) into a structured, dated `pastor_transition` field on the record, so a visitor sees "retiring September 2026; successor candidate announced" instead of a name that quietly went out of date.

## What this skill IS

- A way to capture a leadership transition as DATA: status, a human-readable detail, an optional named successor, an effective date, and the source, all stamped with the day it was recorded.
- A monitor that rides along with the address-finding rounds (the agents already open each church's Facebook and website, so they can report a transition in the same pass at almost no extra cost) and can also be run as a standalone sweep of green-rated or watch-listed churches.
- A producer of human-review flags for the cases that touch the rubric, never an automatic rating change.

## What this skill is NOT

- It does not change the `pastor` field. The installed pastor stays current until the handoff actually completes; an announced candidate is recorded as a candidate, not promoted into the pastor slot.
- It does not move a rating. A transition is informational. The one rubric hook is that a *female* successor candidate sets `review_gender` for a human to look at, because the MOOP rule fires on an installed sole female senior pastor, not on a nominee who may or may not be called.
- It is not a headless Facebook scraper. The WebFetch tool cannot read Facebook (a login wall truncates the page), so an announcement that lives only on Facebook is reached the browser way described below, or it comes from a human who saw it (the field records it either way, with `transition_source: church-facebook`).

## The data shape

`apply-enrichment-round.js` accepts these fields per record and assembles `pastor_transition`:

```json
{
  "id": "spotswood-baptist",
  "transition_status": "retiring",
  "transition_note": "Dr. Drew Landry retiring September 2026; a successor candidate has been announced on the church's Facebook.",
  "successor": "(name, if you are recording it)",
  "transition_effective": "September 2026",
  "transition_source": "church-facebook",
  "successor_gender": "female"
}
```

`transition_status` is one of: `retiring`, `resigning`, `interim`, `candidate-announced`, `vacant`, `incoming` (anything else is stored as `announced`). Only `transition_note` is strictly required; the rest sharpen the record. The church page renders the detail as a gold-bordered "Leadership Update" line with the as-of date.

## Workflow

### 1. Pick the scope

- A single church the user named (most common; e.g. a home-church update).
- A cohort worth watching: green-rated churches (a change there is the most consequential), a state, or a network.
- Ride-along: while running an address-finding round, tell each agent to ALSO report a transition if the church's site or Facebook shows one (see the prompt addendum below).

### 2. Read the public record

For each church, in priority order: the church's own website (an /about, /staff, /our-team, or a "pastor search" or "passing the baton" page), then its Facebook, then a denominational directory or local news. Match against `data/transition-lexicon.json`, which carries the phrases that signal a transition (retire, resign, "in view of a call", interim, "called as our next", succession, and so on) with a weight and a note.

### 2a. Reading a church's Facebook in a signed-in browser

Many churches announce a transition on Facebook before their website catches up, and WebFetch cannot read Facebook. The way through is the user's own Chrome via the Claude-in-Chrome tools, since it already carries a Facebook session, so no credential is ever typed:

1. `list_connected_browsers`, then ask the user which Chrome to drive (one of theirs is signed into Facebook); `select_browser` on their choice.
2. `tabs_context_mcp` to get or create a tab, then `navigate` it to `facebook.com/<ChurchPageName>` (find the page slug from the church's website Facebook link).
3. `get_page_text` on that tab and read the recent posts for transition language; the most recent posts usually carry a "meet and greet," a "candidate," or a "vision" announcement.

Hard rule, no exceptions: never type a password into a login field, not even when the user offers their credentials. If a church page is gated and the chosen browser is not already signed in, stop and ask the user to sign in themselves in that window, or to paste what the post says. The Apple-Events bridge to Chrome can also hang mid-session; if a call times out, take the text you already have rather than hammering a stuck browser.

### 3. Verify before you write

Prefer the church's own site for the fact of a transition and the timing. A *name* is the sensitive part: do not publish a successor's name unless a credible source states it and the user is comfortable showing a not-yet-voted candidate on a public directory. When the only source is Facebook and the tools cannot read it, record the transition from what the user reports and set `transition_source: church-facebook`. Never guess a name or a date; a wrong successor is worse than none.

### 4. Apply

Write the verified records to a JSON file and run:

```bash
node scripts/apply-enrichment-round.js /tmp/leadership-updates.json
node generate-church-pages.js
git add docs/data/churches.json docs/churches/ && git commit -m "Leadership update: <church/scope>" && git push
```

### 5. Re-check on a sane cadence

Transitions move slowly. A monthly pass over green-rated churches is reasonable, quarterly is too sparse for the ones people actually use, and weekly is overkill. The cheapest cadence is the ride-along: every address round already visits a fresh batch of churches, so leadership-watch advances for free as the directory is swept.

## Prompt addendum for ride-along rounds

Add this to each address-finding agent's instructions so a transition is caught in the same visit:

> While you are on the church's website or Facebook, also note any LEADERSHIP TRANSITION: a pastor retiring or resigning, an interim pastor, or an announced successor/candidate. If you find one, add `transition_status`, `transition_note` (what was said), `successor` (only if named), `transition_effective` (timing), and `transition_source`. Never guess a name or date.

## Heuristic caveats

- "Passing the baton" or "celebrate his ministry" language signals a retirement in progress even when no successor is named; record the retirement, leave the successor blank.
- A guest or candidate "preaching in view of a call" is a candidate, not the pastor; use `candidate-announced`, not the pastor field.
- A staff page listing an "Associate" or "Teaching" pastor but no senior pastor often means the senior seat is vacant or in transition; treat a missing senior pastor as a signal to look, not as a fact.
- Two-person "co-pastor" or "lead pastor couple" framing is a `review_gender` case, the same as in the main rubric.
