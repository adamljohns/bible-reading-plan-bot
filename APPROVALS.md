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

Release any of these with `--release` once the text is written and APPROVEd.

## Scope note

The gate applies to content published on or after **2026-07-09**, the day Adam
set the rule. The legacy archive — 199 posts migrated 2026-03-15, some going
back to the 2007 Iraq deployment — is his own historical writing and is out of
scope. Retroactively flagging it would bury the handful that actually matter.
