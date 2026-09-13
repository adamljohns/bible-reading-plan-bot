# Approval Ledger — usmcmin.org

Adam's standing rule (MOOP-MASTER-PLAN governance #1, set 2026-07-09):

> Nothing public auto-posts. All outward-facing content drafts HIDDEN and waits
> for Adam's explicit APPROVE. Above reproach, always.

Until 2026-08-20 that rule had no mechanism behind it, and it failed three
times. This file is the mechanism's memory. `bin/approval_gate.py` reads it.

## How it works

1. A new post is written into `docs/_drafts/` (robots.txt already `Disallow`s
   that path) **or** written in place carrying
   `<meta name="robots" content="noindex, nofollow">`.
2. Adam says APPROVE.
3. Whoever has the session records it here, one line, this exact shape:

   ```
   YYYY-MM-DD | docs/blog/the-slug.html | APPROVE (where he said it)
   ```

4. Then, and only then: `python3 bin/approval_gate.py --release docs/blog/the-slug.html`
   The tool refuses to release a page that is still a scaffold or that has no
   line here, so step 3 cannot be skipped.
5. The weekly gate audit (`com.moop.approval-gate-audit`, Sat 07:30) re-checks
   the whole site and reports any page that went public without passing through
   this file.

Lines that do not begin with a date are ignored, so notes and prose are safe.

---

## Approved

<!-- Add APPROVE lines here. Format: DATE | path | APPROVE (source) -->

2026-08-25 | docs/blog/thdb-try-harder-do-better.html | APPROVE (Adam in Claude Code session, "ship it!", after reviewing the upgraded post and the Pops explainer video)
2026-09-04 | docs/verse/genesis-1-1.html | APPROVE (Adam via Telegram, "I'm good with the Gen 1:1 deep word study", and asked for the remaining verses built out the same way)
2026-09-13 | docs/verse/1-corinthians-10-13.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-corinthians-16-13.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-corinthians-6-19.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-john-1-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-peter-3-15.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-peter-5-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-peter-5-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-thessalonians-5-16-18.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-timothy-3-4.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/1-timothy-4-12.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-chronicles-20-12.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-corinthians-10-5.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-corinthians-5-17.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-corinthians-7-10.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-timothy-1-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-timothy-2-15.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-timothy-3-16.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/2-timothy-4-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/acts-1-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/acts-17-11.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/colossians-3-19.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/colossians-3-23.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/deuteronomy-17-19.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/deuteronomy-32-35.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/deuteronomy-6-6-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/deuteronomy-6-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/deuteronomy-6-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-2-8-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-2-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-4-2.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-5-14-16.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-5-25.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-5-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-6-10-18.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-6-11.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ephesians-6-4.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ezekiel-33-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/ezekiel-36-26.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/galatians-2-20.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/galatians-5-22-23.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/hebrews-10-24-25.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/hebrews-11-1.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/hebrews-12-2-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/hebrews-13-5.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/isaiah-26-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/isaiah-40-31.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/isaiah-41-10.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/james-1-19-20.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/james-1-21-22.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/james-4-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/jeremiah-29-11.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/jeremiah-29-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/john-14-21.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/john-14-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/john-15-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/john-16-33.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/john-3-16.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/joshua-1-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/joshua-1-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/joshua-24-15.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/luke-11-28.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/luke-14-33.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/luke-9-23.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-11-28-30.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-18-20.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-22-36-39.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-28-19-20.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-4-19.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-1.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-10.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-11.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-12.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-13.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-14.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-15.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-16.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-2.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-4.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-5.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-5-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/matthew-6-33.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/micah-6-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/philippians-2-19.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/philippians-4-13.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/philippians-4-6-7.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/philippians-4-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/philippians-4-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/proverbs-18-10.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/proverbs-22-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/proverbs-27-17.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/proverbs-3-5-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/proverbs-3-5.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-1-2-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-119-105.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-119-11.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-119-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-127-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-23-1-6.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-46-1.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/psalm-91-1-2.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/revelation-1-3.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-1-16-17.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-1-16.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-10-17.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-10-9.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-12-1-2.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-12-1.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-12-19-21.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-3-23.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-5-8.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-6-23.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-8-1.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/romans-8-28-30.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)
2026-09-13 | docs/verse/zephaniah-3-17.html | APPROVE (Adam in Cursor, "let's make sure it's live on our website" — quality deep studies matching Genesis 1:1)

---

## Unrecorded gap — logged 2026-08-20, awaiting Adam's call

These 14 posts are **live right now** and carry no recorded approval. They were
found by the first run of `bin/approval_gate.py`. The master plan tracked four
of them (P0#5); the audit found fourteen.

They have deliberately **not** been touched. Pulling down posts Adam may well
have approved verbally would be its own breach, and unpublishing is his call,
not the fleet's. Adam: for each, either say APPROVE (and it gets a line above)
or say pull, and it gets noindexed.

| Published | Post |
|---|---|
| 2026-07-11 | `docs/blog/solo-leveling-13-jeju-the-strong-fall.html` |
| 2026-07-11 | `docs/blog/solo-leveling-14-king-of-humans.html` |
| 2026-07-11 | `docs/blog/solo-leveling-15-the-healer.html` |
| 2026-07-11 | `docs/blog/solo-leveling-16-raised-a-shadow.html` |
| 2026-07-22 | `docs/blog/denominationalism-is-dead-and-men-need-to-hear-it.html` |
| 2026-07-22 | `docs/blog/imprecatory-prayer-and-governmental-leaders.html` |
| 2026-07-27 | `docs/blog/teach-them-how-to-say-goodbye.html` |
| 2026-08-07 | `docs/blog/neither-rot-nor-break.html` |
| 2026-08-07 | `docs/blog/twenty-five-years-later-enlightenment.html` |
| 2026-08-10 | `docs/blog/how-to-disagree-without-lying.html` |
| 2026-08-11 | `docs/blog/bear-much-fruit.html` |
| 2026-08-14 | `docs/blog/the-easy-yoke-is-not-an-easy-exit.html` |
| 2026-08-15 | `docs/blog/a-charge-is-not-a-verdict.html` |
| 2026-08-15 | `docs/blog/before-you-decide.html` |

### Machine-readable (read by bin/approval_gate.py)

```
2026-08-20 | docs/blog/solo-leveling-13-jeju-the-strong-fall.html | LOGGED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-14-king-of-humans.html | LOGGED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-15-the-healer.html | LOGGED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-16-raised-a-shadow.html | LOGGED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/denominationalism-is-dead-and-men-need-to-hear-it.html | LOGGED-GAP (published 2026-07-22; awaiting Adam's ruling)
2026-08-20 | docs/blog/imprecatory-prayer-and-governmental-leaders.html | LOGGED-GAP (published 2026-07-22; awaiting Adam's ruling)
2026-08-20 | docs/blog/teach-them-how-to-say-goodbye.html | LOGGED-GAP (published 2026-07-27; awaiting Adam's ruling)
2026-08-20 | docs/blog/neither-rot-nor-break.html | LOGGED-GAP (published 2026-08-07; awaiting Adam's ruling)
2026-08-20 | docs/blog/twenty-five-years-later-enlightenment.html | LOGGED-GAP (published 2026-08-07; awaiting Adam's ruling)
2026-08-20 | docs/blog/how-to-disagree-without-lying.html | LOGGED-GAP (published 2026-08-10; awaiting Adam's ruling)
2026-08-20 | docs/blog/bear-much-fruit.html | LOGGED-GAP (published 2026-08-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/the-easy-yoke-is-not-an-easy-exit.html | LOGGED-GAP (published 2026-08-14; awaiting Adam's ruling)
2026-08-20 | docs/blog/a-charge-is-not-a-verdict.html | LOGGED-GAP (published 2026-08-15; awaiting Adam's ruling)
2026-08-20 | docs/blog/before-you-decide.html | LOGGED-GAP (published 2026-08-15; awaiting Adam's ruling)
```

The four Solo Leveling posts are likely fine — that lane closed at "16 of 12
shipped" and Adam was reading along. They are listed for completeness, not
suspicion.

## Mechanism gap — logged 2026-09-03

`bin/approval_gate.py` enforces the APPROVE requirement on `blog/` only
(`docs_path.startswith('blog/')`). Everything else is treated as site
furniture. That was fine when blog posts were the only outward-facing prose,
and it is no longer true: `docs/verse/` now holds hand-authored deep studies of
1,200-4,000 words, which is exactly the doctrinal teaching governance rule 1
was written for.

Measured tonight, the exposure is **one page**, not the whole directory:

| Page | Words | State |
|---|---|---|
| `docs/verse/genesis-1-1.html` | 1,738 | live, indexable, in `sitemap-main.xml`, **no APPROVE on record** |

The other 50 files in `docs/verse/` are not a gap: 45 are short generated verse
landing pages (~100-140 words, from `bin/add-verse-page.js`) which are site
furniture like dictionary entries; 4 of the 5 remaining deep studies already
carry `noindex`; and `index.html` is the public hub.

Not pulled, per the same reasoning as the 14 above. **Adam's two calls:**

1. `docs/verse/genesis-1-1.html` — APPROVE it, or say pull and it gets `noindex`.
2. Should deep verse studies be gated like blog posts going forward? If yes,
   the change is to add a `verse/` prefix to the approval test in
   `approval_gate.py` **and** a length threshold, so the 45 short landing pages
   are not swept in. Naively adding `verse/` to `CONTENT_PREFIXES` fails the
   deploy on those 45 as "thin pages" -- tried on 2026-09-03, reverted.

**RESOLVED 2026-09-04.** Adam approved `genesis-1-1.html` (line recorded above)
and ruled that deep verse studies should be gated like blog posts. Implemented
in `bin/approval_gate.py` as `is_approval_gated()`: `verse/` pages are gated
only above `DEEP_STUDY_MIN_CHARS` (6,000 chars visible, ~1,000 words), so the
45 short generated landing pages stay ungated furniture.

## Gated on 2026-08-20 (no approval needed — these were never meant to be public)

- **31 scaffold pages** — `docs/confessions/book-01..13`, `docs/bfm/article-01..18`,
  every one still reading *"Text pending — this page is scaffolding."* Live and
  in the sitemap since 2026-08-07. Now `noindex` and pulled from the sitemap.
- **2 hub pages** — `docs/confessions/index.html`, `docs/bfm/index.html`. Real
  text, but they advertise 31 chapters that do not exist yet.
- **11 MHA drafts** — `docs/blog/mha-*.html`, crawlable since 2026-07-12,
  waiting on Adam to read them post by post. Now `noindex` and out of
  `sitemap-blog.xml`. Links from `docs/blog-anime.html` left alone deliberately:
  no link surgery, per the plan.
  **Correction 2026-09-03:** it is not only the anime hub. **`docs/blog.html`,
  the main blog index, links all 11 as well**, and both hubs are themselves
  indexable and listed in `sitemap-main.xml`. The drafts return 200 and are one
  click from a live, indexed page; `noindex` on the target keeps them out of
  search results, it does not make them unreachable. Still not touched, for the
  same reason as the 14 above: unpublishing is Adam's call, not the fleet's.
  Adam: say *pull* and both hubs drop the 11 cards in one commit.

Release any of these with `--release` once the text is written and APPROVEd.

## Scope note

The gate applies to content published on or after **2026-07-09**, the day Adam
set the rule. The legacy archive — 199 posts migrated 2026-03-15, some going
back to the 2007 Iraq deployment — is his own historical writing and is out of
scope. Retroactively flagging it would bury the handful that actually matter.
2026-09-06 | docs/blog/know-your-marines-total-fitness.html | APPROVE (Telegram)
2026-09-10 | docs/blog/do-not-baptize-total-fitness.html | APPROVE (Telegram; Principal GO recorded in PJG-0903-MCTF1)
2026-09-10 | docs/blog/before-the-boots-come-off.html | APPROVE (Telegram; Principal GO 2026-09-10 20:51 EDT relayed to Max by BG Hartwell, CID BGH-0910-BOOTS — relayed, not witnessed directly by the recording session)
