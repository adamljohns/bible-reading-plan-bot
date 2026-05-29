# Blog Voice Guide (and AI-Tell Catalog)

> Editorial standards for the U.S.M.C. Ministries blog. Companion to
> `DICTIONARY-VOICE-LOCK.md` (which governs the dictionary's confessional
> standpoint). This file governs the blog's *prose voice* &mdash; how it
> sounds, not just what it says.

---

## 1. The voice in two sentences

**Long prose, flowing, with em-dashes and subordinate clauses. Not staccato AI
bullet-cadence; not corporate-buzzword polish; not therapy-culture
softness. Reformed, KJV-honoring, plain-American, conversational with a
pastor's seriousness.**

Where the dictionary entry is precise and definitional, the blog post is
discursive and warm. The dictionary names the doctrine; the blog talks the
reader through it.

---

## 2. House style positives

- **Conversational opener.** Start where the reader is, not with an
  abstract claim. "Last Tuesday at the grocery store..." rather than "In
  today's complex landscape of consumer choices..."
- **Specific examples over abstract generalizations.** "My son Gideon"
  rather than "many children." "The 2008 financial collapse" rather than
  "various economic downturns."
- **Subordinate clauses welcomed.** Multiple clauses in one sentence is
  fine; the prose flows. Don't force every idea into its own short sentence.
- **Em-dashes are house-style.** Use them. Don't avoid them just because
  AI overuses them. The remedy is *variety*, not abstention.
- **First-person voice when appropriate.** "I" and "we" carry the
  pastoral relationship. "The reader" or "one might consider" reads cold.
- **Concrete biblical anchoring.** When you quote Scripture, quote KJV
  unless you've established a different working text. Cite the reference.
  The `autolink_blog_scripture.py` will turn canonical refs into BTE links
  automatically.
- **Dictionary cross-linking.** The `autolink_blog.py` already links
  matching dictionary terms on first occurrence per post. You don't need
  to write the links by hand &mdash; just use the actual term.
- **Pastor's seriousness on serious topics.** Sin is sin; grace is grace;
  judgment is judgment. The blog doesn't soft-pedal the gospel's hard
  edges in service of cultural niceness.
- **Concrete reformer / Puritan citations welcome.** When Owen or Spurgeon
  or Calvin made the point first and better, give them the credit.

---

## 3. Banned phrases (AI-tell catalog)

The audit script `bin/voice_audit_blog.py` flags these. Each gets a
category, a severity, and a suggested replacement.

### 3.1. Filler

| Phrase | Severity | Replacement |
|---|---|---|
| "It's worth noting that..." | hard | Cut entirely. If the thing's worth noting, say it. |
| "It's important to note / remember / understand that..." | hard | Cut. Say the thing. |
| "It should be noted that..." | hard | Cut. |
| "It goes without saying that..." | hard | If it goes without saying, don't say it. |
| "Needless to say..." | hard | Cut. |
| "In conclusion," | hard | Cut. End with the actual conclusion. |
| "To summarize," | hard | Cut, or write the actual summary. |
| "In essence," | hard | Cut. |
| "At the end of the day," | soft | Often filler; cut or rephrase concretely. |
| "In today's world / society / economy / landscape" | hard | Replace with specific date or event. |
| "In an era of..." | hard | Replace with specific context. |

### 3.2. Empty verbs / corporate-speak

| Phrase | Severity | Replacement |
|---|---|---|
| "delve into" | hard | explore / examine / dig into / study |
| "navigate the complex..." | soft | work through / handle |
| "embrace" (non-doctrinal) | soft | accept / take up / receive |
| "leverage" | hard | use / draw on / take advantage of |
| "unlock the potential / power" | hard | Replace with specific action. |
| "game-changer / game-changing" | hard | Replace with specific impact. |
| "tap into" | soft | draw on / use / access |
| "harness" | soft | use / channel / employ |
| "robust" | soft | strong / sturdy / well-built / dependable |
| "comprehensive" | soft | full / complete / thorough / broad |
| "seamless" | soft | smooth / uninterrupted / unbroken |
| "synergy / synergies / synergistic" | hard | Cut or rephrase concretely. |
| "streamline" | soft | simplify / tighten / speed up |
| "holistic" | soft | full-orbed / whole-person / complete |
| "cutting-edge" | soft | newest / latest / recent |
| "best practices" | soft | proven methods / tested approaches |
| "value proposition" | hard | Corporate-jargon; cut. |

### 3.3. The "X not just Y, but Z" construction

AI uses this rhetorical pattern relentlessly. Vary it. Soft-flagged when
it appears.

### 3.4. Transition glue

Sentence-starting "Furthermore," / "Moreover," / "Additionally," are AI
transition glue. Cut them; restructure the paragraph so the flow is
implicit rather than glued together with cold transition words.

### 3.5. Hedge

| Phrase | Severity | Replacement |
|---|---|---|
| "Some might argue..." | soft | Name the actual argument or cut. |
| "Many would say..." | soft | Name actual speakers or cut. |
| "Arguably..." | soft | Either argue or drop. |
| "Some believe / think / hold / claim" | soft | Name actual people or cut. |

### 3.6. Empty intros

"In today's day and age..." "In our modern world..." "In an era of
ever-changing..." All cliché AI openers. Replace with a specific date,
event, or anchor in the reader's actual experience.

### 3.7. Weasel quantifiers

| Phrase | Severity | Replacement |
|---|---|---|
| "numerous" | soft | many / several / lots of / dozens of (be specific) |
| "myriad" | soft | many / countless |
| "plethora" | hard | many / lots of / surplus |
| "various" | soft | several / a few / specific list |
| "a multitude of" | soft | many / lots of |

### 3.8. Therapy register

Substitute Reformed moral vocabulary (mirrors the dictionary's voice-lock):

| Phrase | Severity | Replacement |
|---|---|---|
| "trauma" | soft | suffering / affliction / the breaking of body or soul under sin and curse |
| "harmful" (as primary moral category) | soft | sinful / against God's law / against the soul's good |
| "safe space" | hard | Reject; not a biblical category. |
| "lived experience" | soft | testimony / witness |
| "validate" (as moral category) | soft | confirm / affirm / commend |
| "unhealthy patterns" | soft | sin patterns / besetting sins |

### 3.9. Em-dash overuse &mdash; STANDING DECISION REQUIRED

**Conflict to resolve:** The most-downloaded humanize-AI-writing skill on
GitHub (@blader/humanizer, 16,800+ stars) takes a hard line: em-dashes
(`—`) are one of the strongest AI tells and must be cut from all final
rewrites. The Wikipedia "Signs of AI Writing" guide that skill is built
on agrees.

This guide's §2 ("Em-dashes are house-style") was written BEFORE the
@blader/humanizer skill was installed. The two positions conflict:

- **Position A (this guide, until 2026-05-28):** em-dashes are Adam's
  natural flowing-prose voice and should be kept. AI tell or not, it's
  the house rhythm.
- **Position B (@blader/humanizer):** em-dashes are a strong AI tell;
  replace with periods, commas, colons, parentheses, or restructure.

**Until Adam decides which position governs**, the `usmcmin-content`
prep skill follows Position A (keep em-dashes) for blog posts at
`usmcmin.org` and Position B (strip em-dashes) for ALL other content
(Telegram replies, professional emails, dictionary entries, LBCF
chapters, citizen page additions).

The voice audit script (`bin/voice_audit_blog.py`) still soft-flags
3+ em-dashes in a single paragraph as a heads-up; it does not hard-fail.

When Adam decides, this section should be updated and the
`usmcmin-content` skill spec adjusted accordingly.

---

## 4. Audit workflow

Before publishing a new blog post (or revising an old one):

1. **Run the dictionary auto-linker** (or let the periodic sweep do it):
   ```
   python3 bin/autolink_blog.py
   ```
2. **Run the Scripture auto-linker:**
   ```
   python3 bin/autolink_blog_scripture.py
   ```
3. **Run the voice audit:**
   ```
   python3 bin/voice_audit_blog.py docs/blog/your-new-post.html
   ```
4. **Review each hit.** Hard hits must be revised. Soft hits require
   judgment &mdash; some are legitimate in context.
5. **Use the file-level opt-out sparingly.** A blog post that legitimately
   needs to use banned register to discuss it (e.g., a critique of
   therapy-culture vocabulary) can add `<!-- voice-audit-skip -->` near
   the top to suppress the audit for that file. Use rarely; the audit
   exists for a reason.

---

## 5. Periodic full-sweep maintenance

Every 3-6 months, run the audit on all blog posts:

```
python3 bin/voice_audit_blog.py docs/blog/ --markdown > voice-audit-YYYY-MM-DD.md
```

Review the report. Triage hard hits to revise. Note recurring soft
patterns &mdash; if a particular phrase keeps slipping in, add it to your
working revision checklist.

---

## 6. What this guide does NOT do

- It does not enforce theological positions. Those live in
  `DICTIONARY-VOICE-LOCK.md` and apply across the site.
- It does not micromanage your sentence length, paragraph structure, or
  rhetorical arc. Your voice is yours; the audit catches AI-tells, not
  stylistic preferences.
- It does not auto-rewrite. The risk of auto-rewriting blog prose is too
  high; the audit produces a report and the human revises.

---

## 7. Reference: existing infrastructure

- `bin/voice_audit_blog.py` &mdash; the scanner
- `bin/autolink_blog.py` &mdash; dictionary auto-linker (already running)
- `bin/autolink_blog_scripture.py` &mdash; Scripture &rarr; BTE linker (new)
- `bin/autolink_chapters.py` &mdash; Bible chapter auto-linker (dict terms in
  chapter pages)
- `bin/autolink_lexicon_from_dict.py` &mdash; lexicon back-links to dict
- `DICTIONARY-VOICE-LOCK.md` &mdash; dictionary confessional standpoint
- `bin/dict_drift_audit.py` &mdash; dictionary drift audit (parallel to this
  one)

Same pattern across the suite: scanners and linkers in `bin/`; doctrinal
standards in markdown at repo root; periodic sweeps with markdown report
output.
