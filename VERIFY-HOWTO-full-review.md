# How to verify the full-review dry run (for the independent verifier)

Ticket item 2: pick 10 proposed changes from the dry run and confirm, independently, that each
one is supported by its cited evidence. This file tells you where everything is. It does not
contain any verification results; write those yourself.

Worktree: `/Users/moop_bot_pro/worktrees/church-full-review` (branch `feat/church-full-review`).
Do not edit `docs/data/churches.json` here or in `~/bible-reading-plan-bot`. Read-only work.

## Files

| What | Path (relative to the worktree) |
|---|---|
| Review patch (every proposal, per church) | `data/full-review/rounds/fr-20261108-2343/review-patch.json` |
| This round's HOLD items | `data/full-review/rounds/fr-20261108-2343/hold.json` |
| Cumulative HOLD queue (same rows, `dry_run: true`) | `data/full-review/hold-queue.json` |
| Fetcher output: pages read + cached page text | `data/full-review/rounds/fr-20261108-2343/observations.json` (git-ignored) |
| Public dashboard counts | `docs/data/full-review-stats.json` (rendered in `docs/grind-report.html`) |
| Round log | `~/Library/Logs/full-review-round.log` and `/tmp/cfr/dryrun4.log` |
| Previous rounds (verify 8/10 each) | `data/full-review/rounds/fr-20261108-2220/`, `data/full-review/rounds/fr-20261108-2250/`, `data/full-review/rounds/fr-20261108-2316/` — superseded, kept for comparison |
| churches.json checksums | `/tmp/cfr/sha-before-4.txt` vs `shasum -a 256 docs/data/churches.json` |

## How a proposed change maps to its evidence

In `review-patch.json`, `churches[]` has one object per church. Each `changes[]` entry is:

```
change_id      "<round>:<church id>:<n>"   (same id as hold_id in hold.json)
field          the churches.json field, dotted for nested (e.g. "scores.gender")
op             set | replace | fill | confirm | clear | research
old            the value in churches.json when the patch was built
new            the proposed value
also_sets      extra fields written with it (overall_label, score_notes.<cat>, score_sources.<cat>)
confidence     high | medium | low
gate           auto (would apply on a live run) | hold (waits for Chaps QA)
hold_reasons   why it is held
evidence.quote the verbatim passage
evidence.url   the page that passage is on
```

To check one change:
1. Open `evidence.url` in a browser (browser user agent; some church hosts 403 bare fetches).
2. Find `evidence.quote` on that page. Matching ignores case, whitespace, and curly vs straight
   quotes; the rest must match character for character. If the live page changed since the round
   ran, the cached text is in `observations.json` → `observations[] (by id)` → `pages[]` → `text`.
3. Judge whether the quote supports `field: old -> new`, and whether the `gate` is correct under
   the ticket's rules: to RED/BLACK or off GREEN must be `hold`; only high confidence may be `auto`.

Ratings (round fr-20261108-2343 onward) follow written rules only. Every `scores.*` and
`overall_rating` change carries `rule` = `{text, context, url}`: the rule's own text as published
on https://usmcmin.org/directory-methodology.html. Check that `rule.text` is on that page and that
it maps `evidence.quote` (a church-page quote) to `new`. Judgments no published rule covers are not
changes. They are HOLD rows with `kind: "ruling"` (title `needs-ruling: …`, e.g. "needs-ruling: model
suggests BLACK") or `kind: "unconfirmed"` (female clergy by first-name list only). Each has its own
`evidence` and `evidence_more`. They never apply; Chaps and Adam decide them.

Rosters (`pastors`, from fr-20261108-2343): each kept name has its own quote in `evidence_more`
(with `name` and `role`); `evidence` is the quote naming the lead pastor. A name is kept only with its
surname on the cited page, tied to this church (staff/clergy page or role prose), with an office as
the role (never "Rev."/"Dr."/"Fr."). Excluded names and the reason (joint-ministry/guest context,
non-clergy role, not tied) are listed per church in `churches[].roster.excluded`.

Service times (from fr-20261108-2343): stored and page values are compared as sets of day+time tokens
(`churches[].service_times.stored_tokens` / `page_tokens`). A change is proposed only when the sets
differ, and `new` is the structured value (e.g. "Sun 8:30 AM, 11:00 AM"); `evidence.quote` is the page
sentence it was read from.

Website recovery for wrong-church records: a name-domain probe (.com/.org/.church) runs before the
local search. A candidate is proposed (always HOLD) only when its page prints the stored street
address; `evidence.quote` is that address passage on the candidate site.

Fill scope (from fr-20261108-2343): every profile fill's quote must be about this congregation. Fills
from a pastor's bio about other churches, partner/joint-ministry passages, or sections naming another
church are dropped and listed in `churches[].scope_dropped` with the reason. On a multi-church parish
site (`churches[].multi_church`, with the quote that shows it), a fill not taken from this
congregation's own subpage is HOLD, and service-time changes there are always HOLD.

Social links (from fr-20261108-2343): `evidence_type: "html_link"` means `evidence.quote` is the exact
`<a …href…>` tag in the HTML of `evidence.url`; `evidence_type: "site-config"` means the link is only in
the page's config/JSON, and `evidence.quote` is the exact raw snippet (view source to find it). Site-config
fills are always HOLD.

`data/full-review/hold-queue.json` holds only each church's latest round; earlier rows live in the
per-round `hold.json` files.

Three evidence types are not plain page quotes. Check them like this:
- `evidence.evidence_type: "html_link"` (social links): the quote is the exact `<a …>` tag; find it in
  the raw HTML of `evidence.url`. `"site-config"`: find the quoted JSON snippet in the raw HTML.
- Denomination rule (`rule.text` = "LGBTQ-affirming denomination → RED minimum."): `evidence` is the
  church's own printed name or about text stating the affiliation (e.g. "St. Mary's Episcopal
  Church"); the rule itself is in `rule`. (In the superseded round fr-20261108-2220 the rule text sat
  in `evidence` and the affiliation in `evidence.affiliation_quote`.)
- `evidence.evidence_type: "http_redirect"`: request the stored website and confirm it redirects to
  `evidence.url`.

Flags (duplicates, wrong-church data) are in `churches[].flags[]` and in `hold.json` with
`kind: "flag"`. Their `evidence` is the other record's value (`url` is its usmcmin.org page) or
the site's own location statement.

## Quick listing

```
cd /Users/moop_bot_pro/worktrees/church-full-review
node -e 'const p=require("./data/full-review/rounds/fr-20261108-2343/review-patch.json");
for (const c of p.churches) for (const x of c.changes)
  console.log([x.change_id, x.gate, x.field, JSON.stringify(x.old), "->", JSON.stringify(x.new), x.evidence.url, JSON.stringify(x.evidence.quote)].join(" | "))'
```

Suggested spread for the 10: the St. Mary's pastor, overall rating and needs-ruling item
(`st-mary-s-church-colonial-beach`), the Calvary Memorial wrong-church flag and pastor clear
(`calvary-memorial-church-oak-park-il`), at least two other pastor changes, two rubric category
changes, one profile fill (service times / founded / ministry flag), and one social link.
