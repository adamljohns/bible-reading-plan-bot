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

2026-10-18 | docs/blog/self-care-is-the-wrong-word.html | APPROVE (Adam via Telegram, "Alright push it live")
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
2026-09-13 | docs/blog/solo-leveling-13-jeju-the-strong-fall.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/solo-leveling-14-king-of-humans.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/solo-leveling-15-the-healer.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/solo-leveling-16-raised-a-shadow.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/denominationalism-is-dead-and-men-need-to-hear-it.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/imprecatory-prayer-and-governmental-leaders.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/teach-them-how-to-say-goodbye.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/neither-rot-nor-break.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/twenty-five-years-later-enlightenment.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/how-to-disagree-without-lying.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/bear-much-fruit.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/the-easy-yoke-is-not-an-easy-exit.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/a-charge-is-not-a-verdict.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/before-you-decide.html | APPROVE (Adam in Cursor, "sure publish all")
2026-09-13 | docs/blog/mha-1-you-can-be-a-hero.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-10-why-villains-are-made.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-11-now-its-your-turn.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-12-go-beyond.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-2-the-hero-notebook.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-4-i-am-here.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-5-one-for-all.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-6-a-worthy-vessel.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-7-plus-ultra.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-8-hidden-form.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex
2026-09-13 | docs/blog/mha-9-all-for-one.html | APPROVE (Adam in Cursor, "sure publish all") — MHA series released from noindex

---

## Unrecorded gap — RESOLVED 2026-09-13

Adam in Cursor: "sure publish all." These 14 posts were already live; they now
have APPROVE lines in the Approved section. The LOGGED-GAP machine lines below
were retired so the weekly audit stops treating them as an open ruling.

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

### Machine-readable (retired 2026-09-13 — APPROVE lines live above)

```
2026-08-20 | docs/blog/solo-leveling-13-jeju-the-strong-fall.html | RETIRED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-14-king-of-humans.html | RETIRED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-15-the-healer.html | RETIRED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/solo-leveling-16-raised-a-shadow.html | RETIRED-GAP (published 2026-07-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/denominationalism-is-dead-and-men-need-to-hear-it.html | RETIRED-GAP (published 2026-07-22; awaiting Adam's ruling)
2026-08-20 | docs/blog/imprecatory-prayer-and-governmental-leaders.html | RETIRED-GAP (published 2026-07-22; awaiting Adam's ruling)
2026-08-20 | docs/blog/teach-them-how-to-say-goodbye.html | RETIRED-GAP (published 2026-07-27; awaiting Adam's ruling)
2026-08-20 | docs/blog/neither-rot-nor-break.html | RETIRED-GAP (published 2026-08-07; awaiting Adam's ruling)
2026-08-20 | docs/blog/twenty-five-years-later-enlightenment.html | RETIRED-GAP (published 2026-08-07; awaiting Adam's ruling)
2026-08-20 | docs/blog/how-to-disagree-without-lying.html | RETIRED-GAP (published 2026-08-10; awaiting Adam's ruling)
2026-08-20 | docs/blog/bear-much-fruit.html | RETIRED-GAP (published 2026-08-11; awaiting Adam's ruling)
2026-08-20 | docs/blog/the-easy-yoke-is-not-an-easy-exit.html | RETIRED-GAP (published 2026-08-14; awaiting Adam's ruling)
2026-08-20 | docs/blog/a-charge-is-not-a-verdict.html | RETIRED-GAP (published 2026-08-15; awaiting Adam's ruling)
2026-08-20 | docs/blog/before-you-decide.html | RETIRED-GAP (published 2026-08-15; awaiting Adam's ruling)
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
- **11 MHA posts — RESOLVED 2026-09-13.** Adam: "sure publish all."
  `noindex` removed via `--release`, APPROVE recorded, URLs added to
  `sitemap-blog.xml`. There is no `mha-3` file; it was never written.
  Hubs already linked the 11 cards; those links stay.

Release any of these with `--release` once the text is written and APPROVEd.

## Scope note

The gate applies to content published on or after **2026-07-09**, the day Adam
set the rule. The legacy archive — 199 posts migrated 2026-03-15, some going
back to the 2007 Iraq deployment — is his own historical writing and is out of
scope. Retroactively flagging it would bury the handful that actually matter.
2026-09-06 | docs/blog/know-your-marines-total-fitness.html | APPROVE (Telegram)
2026-09-10 | docs/blog/do-not-baptize-total-fitness.html | APPROVE (Telegram; Principal GO recorded in PJG-0903-MCTF1)
2026-09-10 | docs/blog/before-the-boots-come-off.html | APPROVE (Telegram; Principal GO 2026-09-10 20:51 EDT relayed to Max by BG Hartwell, CID BGH-0910-BOOTS — relayed, not witnessed directly by the recording session)
2026-10-01 | docs/blog/the-reformers-are-not-a-headcount.html | APPROVE (Telegram; Adam 2026-10-01 "sure; I approve indexing them" — the 14 reformer profiles + this hub post, approved as one set)
2026-10-01 | docs/blog/reformer-john-wycliffe.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-jan-hus.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-martin-luther.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-huldrych-zwingli.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-william-tyndale.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-philip-melanchthon.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-martin-bucer.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-heinrich-bullinger.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-john-calvin.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-thomas-cranmer.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-hugh-latimer.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-nicholas-ridley.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-john-knox.html | APPROVE (Telegram)
2026-10-01 | docs/blog/reformer-theodore-beza.html | APPROVE (Telegram)
2026-10-03 | docs/blog/who-holds-the-scorecard.html | APPROVE (Adam via Telegram to Gus, "Go ahead and publish the draft but run it by Chaps; make sure it doesn't read like AI" — Chaps GO-WITH-FIXES, BGH-1003-SCORECARD; video + infographic added on Adam's "produce the products and then modify them and add them")
2026-10-04 | docs/blog/church-closings-check-the-men.html | APPROVE (Adam via Telegram to Chaps 2026-10-04 09:07 ET, "push the markdown file on church closings over to PJ and have him publish the blog post about it" — relayed by Chaps, CID CCW-1004-BLOG, not witnessed directly by the recording session; theology pass by Preacher John)
2026-10-07 | docs/verse/hebrews-4-15.html | APPROVE (Adam via Telegram to Max, relayed as a Preacher John subagent task 2026-10-07 08:01 ET — condition: one verified Calvin witness per study, Acts heading must not assume a home setting; not witnessed directly by the recording session)
2026-10-07 | docs/verse/2-thessalonians-2-15.html | APPROVE (Adam via Telegram to Max, relayed as a Preacher John subagent task 2026-10-07 08:01 ET — condition: one verified Calvin witness per study, Acts heading must not assume a home setting; not witnessed directly by the recording session)
2026-10-07 | docs/verse/acts-18-26.html | APPROVE (Adam via Telegram to Max, relayed as a Preacher John subagent task 2026-10-07 08:01 ET — condition: one verified Calvin witness per study, Acts heading must not assume a home setting; not witnessed directly by the recording session)
2026-10-19 | docs/blog/self-care-is-the-wrong-word.html (humanized revision) | APPROVE (Adam via Telegram 16:54, "revise and finalize please")
2026-10-19 | docs/blog/self-care-is-the-wrong-word.html (add SgtMaj Mac audio player) | APPROVE (Adam via Telegram 21:24, "good with publishing the update. Use SgtMaj Mac’s voice for the audio")
2026-10-20 | docs/blog/self-care-is-the-wrong-word.html (Pops audio, video, infographic, slides) | APPROVE (Adam via Telegram 07:15, "upload the slides, the infographic, and the video embedded into the blog post")
2026-10-20 | docs/blog/cheap-answers-are-not-a-trained-mind.html | APPROVE (Adam via Telegram 12:35 ET, “Let’s review the blog ProfX wrote for me and push it live today.”)
2026-11-20 | docs/verse/2-corinthians-6-14.html | APPROVE (Adam via Telegram 21:26 ET, message 9386, "I've reviewed this, remove the warning banner and index it with the rest.")
2026-11-20 | docs/blog/unequally-yoked-early-church-to-ballot-box.html | APPROVE (Adam via Telegram 21:27 ET, message 9388, "Publish the blog post too…")
2026-11-20 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (Dallas section revision, "option A": the fault is the program and the last word, not the banner; Scripture refs linked to the reader; narration re-recorded) | APPROVE (Adam via Telegram 22:25 ET)

## Voice revisions of already-published posts — Adam's authority, 17 Nov 2026

Not an APPROVE line for a new post. This records why posts that were already
public were revised in place on 17 Nov 2026 without a line each.

Adam was shown five pilot rewrites of 2026 blog posts on 16 Nov. In a voice
note on 17 Nov 2026 at 04:38 he said of them, "I looked at it real quick and I
definitely like most of the changes," and, on changing the live posts: "the
changes that you can make, if you wanted to make changes to the actual live
blogs, is yes. Like you were pointing out, the choppiness, the two-word
sentences … That needs to be codified in the brain, in the mind of all of my
agents so that they don't write like that. And one of the words that I've
seen used a lot by AI is 'actually'. I want to limit my use of the word
actually. I want to use a different word. I want to use words that I use,
from all my writings."

On that authority the five pilot posts and the next ten posts on the audit's
ranked rewrite list were revised for cadence and wording only. The limits
kept in every one: no new fact, story, quotation or statistic; every idea,
argument, reference and example of the published post kept; Scripture left in
the wording he chose, with a version label added only where the words match a
translation in the site's Bible data (his ruling of 16 Nov: "I might have
chosen the Bible version on purpose, so version label makes sense"); bylines
as he ruled (his own name on what he wrote; "By U.S.M.C. Ministries · drafted
with AI assistance, reviewed by Adam Johns" on AI-drafted posts). Posts with a
doctrine flag for the pastor desk, the six hidden directory essays and the two
related directory posts were left alone. The open questions each revision
raised are held for Adam and were not answered on his behalf. The rule and
the check are in `BLOG-VOICE-GUIDE.md` (sections 0 and 0.2) and
`bin/voice_audit_blog.py`.
2026-11-20 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (rewrite: cut from about 2,900 to about 2,000 words, humanized; Dallas section keeps the fault on the program and the last word, adds Psalm 2 "Kiss the Son" and 1 Corinthians 8:9, and says plainly the hall sounded like a political rally; narration re-recorded) | APPROVE (Adam via Telegram 22:27 ET)
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (Dallas verdict reversed on the Principal's direction: the four marks find no yoke at "Christ Is King"; the closing keynote is a fair concern but the last word is not one of the marks, and the host closed the night; card, opening and closing section brought into line; correction noted in the text; narration re-recorded) | APPROVE (Adam via Telegram 14:17 ET, message 9766, "Need to do a little rewriting and show that the NXR conference is actually the 1 out of 4 that doesn't have an unequal yoking…")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (one sentence corrected: he was in the hall the day before and listened to the closing night live; narration re-recorded with Scripture quotations in their Bible-reading voices, Calvin and the 1689 Confession in the Institutes voice, negative contractions spoken in full, pronunciation fixes) | APPROVE (Adam via Telegram 15:04 and 15:07 ET, messages 9769 and 9770, "I'd like the audio to be redone…" and "one more edit, I wasn't in the hall that night, but I was the previous day…")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (banner image at the top of the post: the image he made and sent for this post; sharing image left as the standard blog card on his word) | APPROVE (Adam via Telegram 18:20 ET, message 9794, "I also went ahead and made a banner photo for the top of the blog post for you on this one too… I made one for the unequally yoked post.")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (added: infographic built in his Gemini Notebook from this post and checked against it, with one added phrase replaced by the post's own words and the generator's mark covered; the verdict card's hidden description brought into line with the corrected Dallas verdict; slide deck, conversation audio and video still in review) | APPROVE (Adam via Telegram 15:57 ET, message 9778, "beef up these blog posts please with the Gemini notebook products… when they're ready to download")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (added: 10-slide deck built in his Gemini Notebook from this post; first version rejected for five faulty slides, including a wrong mark on the CPAC slide and a truncated verse; revised twice and every slide re-read against the post; generator's mark covered) | APPROVE (Adam via Telegram 15:57 ET, message 9778, "beef up these blog posts please with the Gemini notebook products… when they're ready to download")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (added: 3.5-minute conversation audio built in his Gemini Notebook from this post; the first 21-minute version was rejected for an argument the post does not make, added doctrine commentary and remarks pinned on a named speaker; the second was read against the post and one loose sentence cut; video still in work) | APPROVE (Adam via Telegram 15:57 ET, message 9778, "beef up these blog posts please with the Gemini notebook products… when they're ready to download")
2026-11-21 | docs/verse/ecclesiastes-7-8.html | APPROVE (Adam via Telegram voice note 11:23 ET: "publish it as final, version 1.0, reviewed by Moop"; humanized redraft with Max voice pass, KJV above WEB, "The Verse in Context", share card + PDF)
2026-11-21 | docs/blog/the-intimacy-ledger.html | APPROVE (Adam, "short and sweet, publish it" — relayed to the publishing session by the MOOP Claude session, not witnessed directly by the recording session; post with embedded video and the one-page brief PDF)
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html | APPROVE (Adam via Telegram 09:37 ET: "Sure, go ahead and publish it"; sequel to The Common Denominator (2012); quotes verified against source texts; NKJV via scripture-lookup)
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html (added: infographic, a 4.5-minute conversation audio and a 14-slide deck, each built in his Gemini Notebook from this post and checked against it; first versions rejected for errors; video still in work) | APPROVE (Adam via Telegram 15:57 ET, message 9778, "beef up these blog posts please with the Gemini notebook products… when they're ready to download")
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html (banner image at the top of the post: the image he made in ChatGPT and sent for this use; also set as the sharing image) | APPROVE (Adam via Telegram 17:56 ET, message 9788, "We can use ChatGPT like I did as well and put good custom images at the top of our blogs too")
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html (added: 4-minute video overview from his Gemini Notebook, re-voiced in the male narrator from a script made of the post's own sentences, ministry badge over the generator's mark, ministry end card; one inserted portrait photograph removed) | APPROVE (Adam via Telegram 15:57 and 16:35 ET, messages 9778 and 9780, "beef up these blog posts… with the Gemini notebook products" and "revise the videos with a male voice")
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html (narration re-recorded with different voices: Scripture quotations in their Bible-reading voices, C. S. Lewis and G. K. Chesterton quotations each in a voice of their own, negative contractions spoken in full; no change to the wording of the post) | APPROVE (Adam via Telegram 18:20 ET, message 9794, "I'd like the same treatment for the Pride one with different voices at different times as appropriate.")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (footnote numbers added: 22 superscript links from the cited sentences down to the 10 entries in Sources, each with a way back; Sources list numbered; no change to the wording of the post or to its narration) | APPROVE (Adam via Telegram voice note 21:46 ET, message 9806, "use the footnote scheme where we have superscript numbers at the end of sentences that go down to the source that's cited… you can do it for the last several posts")
2026-11-26 | docs/blog/pride-doesnt-think-pride-knows.html (footnote numbers added: 7 superscript links from the cited sentences down to the 6 entries in Sources, each with a way back; Sources list numbered; no change to the wording of the post or to its narration) | APPROVE (Adam via Telegram voice note 21:46 ET, message 9806, "use the footnote scheme where we have superscript numbers at the end of sentences that go down to the source that's cited… you can do it for the last several posts")
2026-11-26 | docs/blog/the-intimacy-ledger.html (footnote numbers added: 6 superscript links from the cited sentences down to the 2 entries in Sources, each with a way back; Sources list numbered; no change to the wording of the post or to its narration) | APPROVE (Adam via Telegram voice note 21:46 ET, message 9806, "use the footnote scheme where we have superscript numbers at the end of sentences that go down to the source that's cited… you can do it for the last several posts")
2026-11-26 | docs/blog/church-closings-check-the-men.html (footnote numbers added: 12 superscript links from the cited sentences down to the 5 entries in Sources, each with a way back; Sources list numbered; no change to the wording of the post or to its narration) | APPROVE (Adam via Telegram voice note 21:46 ET, message 9806, "use the footnote scheme where we have superscript numbers at the end of sentences that go down to the source that's cited… you can do it for the last several posts")
2026-11-26 | docs/blog/unequally-yoked-early-church-to-ballot-box.html (added: 7-minute video overview from his Gemini Notebook, re-voiced in the male narrator from a script made of the post's own sentences, ministry badge over the generator's mark, ministry end card; news-style photographs of real events and a real person, and six diagrams whose captions went beyond the post, removed) | APPROVE (Adam via Telegram 15:57 and 16:35 ET, messages 9778 and 9780, "beef up these blog posts… with the Gemini notebook products" and "revise the videos with a male voice"; 21:54 ET, message 9810, "Let me know if the video is up")
