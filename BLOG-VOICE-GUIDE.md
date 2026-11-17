# Blog Voice Guide (and AI-Tell Catalog)

> Editorial standards for the U.S.M.C. Ministries blog. Companion to
> `DICTIONARY-VOICE-LOCK.md` (which governs the dictionary's confessional
> standpoint). This file governs the blog's *prose voice* &mdash; how it
> sounds, not just what it says.

---

## 0. Cadence (Adam's ruling, 17 Nov 2026) &mdash; read this first

**The finding.** A full read of the blog on 16 Nov 2026 found that the 146
posts dated 2007&ndash;2024 (Adam's own hand) contain almost no staccato prose,
and the 90 posts dated 2026 (mostly machine-drafted) are full of it. The
catalog in section 3 cannot see this. The script now counts it: 32 cadence
faults in his 58,500 words (0.5 per 1,000) against 798 in the 113,600 words
of 2026 (7.0 per 1,000). His sentences average 24 words; the 2026 drafts
average 14.

Adam, 17 Nov 2026: "the choppiness, the two-word sentences &hellip; That needs
to be codified in the brain, in the mind of all of my agents so that they
don't write like that."

**What is out, and the fix for each.**

| Fault | Example (from the 2026 posts) | Fix |
|---|---|---|
| Staccato pair | "That is not courage. That is laziness with a loudspeaker." | One sentence, with the reason attached: say what the thing is and why. |
| The same turn inside one sentence | "This is not toxic masculinity; this is just a normal Tuesday" | Say the positive thing. Keep a contrast only where the post is answering a real objection. |
| Fragment run | "Not a factory. Not an army. Not a marketplace. A vine." | A full sentence that holds all of it: "Of all the pictures He might have used, He chose a vine." |
| One-line paragraph for effect | A slogan closing each section | Fold it into the paragraph it belongs to, or cut it. |
| Briefing-deck structure | A heading every few lines, "Script A / Script B", bulleted takeaways, bold summary lines, a table where an argument should be | Carry the argument in paragraphs. A list is for things that are a list (verses, steps, names). |
| Chronology in clipped notes | "Paris for letters, Orl&eacute;ans and Bourges for law. Flight after the affair of the placards in 1534." | Tell it as a story with verbs and a subject. |

**How to write it instead.** Long sentences that carry one thought through a
turn; the argument in paragraphs; a concrete moment near the top where the
post has one; "I", "we" and "you" doing the talking. Do not overcorrect into
one endless sentence per paragraph: his posts mix a long sentence with a
plain short one. The short one is a whole sentence, and it does not come in
pairs.

**Two rulings the rest of this guide now follows.**

- **Scripture.** Keep the wording Adam chose and add a version label; do not
  swap versions. Adam, 16 Nov 2026: "It doesn't have to be King James. New
  King James I like &hellip; I might have chosen the Bible version on purpose,
  so version label makes sense." Label only when the words match a
  translation in the site's Bible data exactly (`docs/assets/verse-cache.json`);
  a paraphrase gets no label and no quotation marks. Never quote from memory.
  Label style: `(John 15:4, NKJV)` in parentheses, `John 15:8 (NKJV):` in a
  sentence.
- **Bylines.** AI-drafted posts carry "By U.S.M.C. Ministries &middot; drafted
  with AI assistance, reviewed by Adam Johns". Adam's name alone stays on
  what he wrote. No AI persona is ever named as an author, a voice or a
  desk, and no staff or drafting note is printed in a post.

**The check.** `python3 bin/voice_audit_blog.py <file>` prints one PASS/FAIL
line per post. It fails a post on cadence faults above 2.0 per 1,000 words,
avoid-list words above 4.0 per 1,000, "actually" above 2.5 per 1,000, or an
average sentence under 13 words. Thresholds were set so that Adam's own
posts pass (143 of 146; the three that do not are a reposted article, a
page of links, and one playful run of "No way!!! Ya way!"). 85 of the 90
posts dated 2026 failed on the day the check was added.

---

## 0.2. Adam's own words (from his 2007&ndash;2024 posts)

> **How to use the lists below (Max, 2026-11-17).** The hard list is short: "actually", the staccato turns ("that is not…", "here is the…", "read that again", "the whole point", "the question is"), "quietly", "the shape of", and staff shorthand. Those are counted by the checker. Everything else in the frequency tables (toward, nobody, rather than, a single, carries, honest, a man who, and the like) is an ordinary word that the machine drafts overuse. Adam uses them too. Notice a pile-up of them; never swap one for a synonym just to satisfy the list, and never change what a sentence says to avoid one.


Built by script on 17 Nov 2026 from the article bodies of the 146 posts
dated 2007&ndash;2024 (about 60,500 words) set against the 90 posts dated 2026
(about 114,600 words). Rates are per 10,000 words. Every example is verbatim
and names its file in `docs/blog/`. Nothing here is a habit the corpus does
not show.

Adam, 17 Nov 2026: "one of the words that I've seen used a lot by AI is
'actually'. I want to limit my use of the word actually. I want to use a
different word. I want to use words that I use, from all my writings."

### What to avoid, and what he says in its place

| Avoid | 2026 posts | His posts | Use instead |
|---|---|---|---|
| **actually** | 10.0 (115 uses, 54 of 90 posts) | 5.8 (35 uses, 26 of 146) | "really" (18.3 in his posts), "definitely", "in fact", or nothing. He did use it, lightly ("It actually cleared up later", `cancelled-again.html`); the ruling is to limit it, so reach for his other words first. |
| that is not / this is not | 6.8 (76 uses) | 0 | Say what it is. He never once wrote "That is not&hellip;" |
| a man who / the man who / every man who | 11.2 (125 uses) | 0.2 (1 use) | "I", "we", "you", "men", "those who", or the man's name. His posts talk to people; the drafts talk about an abstract man. |
| here is the / here is what / here's the thing | 7.6 | 0.8 | Start with the thing. ("Here's a&hellip;" introducing a link or a photo is his.) |
| a real / the real | 7.3 | 0.3 | "really", "true", or name it |
| honest ("the honest answer") | 5.1 | 0.3 | "Full disclosure:" where he is owning something |
| toward | 5.2 | 0.2 | "towards", "to" |
| rather than | 4.2 | 0.2 | "instead of" |
| is the whole / the whole point | 3.6 | 0.3 | "my point is", "the bottom line" |
| is exactly / the exact | 3.5 | 0 | cut it |
| nobody | 3.3 | 0.3 | "no one" |
| is where | 3.3 | 0.7 | say what happens |
| the very | 3.0 | 0.3 | "the same", or cut |
| a single | 2.9 | 0.2 | "one", "a" |
| was never | 2.9 | 0 | "wasn't", "isn't" |
| quietly | 2.4 | 0 | cut |
| carries ("carries the weight") | 2.4 | 0 | "has", "holds", "bears" |
| on purpose | 2.1 | 0.2 | "intentionally", or cut |
| in the room | 2.0 | 0 | name the place |
| read that again / read that twice | 2.0 | 0 | cut; let the sentence stand |
| not because &hellip; but because | 1.9 | 0 | give the reason straight |
| the shape of / shaped | 1.8 | 0 | describe it |
| the question is / the only question | 1.3 | 0 | ask the question |
| the part where / the part that | 1.2 | 0 | say it directly |
| "this desk", "formation stack", "our locked &hellip; doctrine" | staff shorthand | 0 | never in a post |

Two things that are not words but show up in the same count:

- **He contracts.** "don't, isn't, can't, didn't" run 59.8 in his posts and
  29.6 in 2026; the spelled-out "do not, is not, cannot, did not" run 10.6 in
  his and 96.3 in 2026. Write "I don't think", not "I do not think", outside
  Scripture and formal quotation.
- **He exclaims, trails off and asks.** Exclamation marks: 85.9 in his posts,
  0.2 in 2026. Ellipses: 56.2 against 1.1. Question marks: 39.8 against 17.1.
  Semicolons run the other way (22.0 against 52.7). Do not sprinkle these in
  to imitate him; just stop sanding them off.

### His connectives and turns of phrase

Each of these is far more frequent in his posts than in the 2026 set.

- **I hope / hopefully** (42 and 26 uses; 0 and 0 in 2026). "I hope my words
  are encouraging and not antagonistic, but either way, I love hearing from
  you." (`10-days-without-words.html`) "Hopefully my wife and two boys will
  stay sound asleep until I finish this!!!" (`a-30-mighty-men-new-year.html`)
- **I think / I believe / I really / I don't think** (13.2, 8.3, 24 uses, 23
  uses; near zero in 2026). He owns an opinion as his. "I really believe that
  we need to be able to articulate our faith extremely well and concisely
  enough to benefit the hearers and keep their attention."
  (`drawing-on-the-past.html`) "I really like that." (`781.html`)
- **I guess / probably / maybe / pretty** (he hedges like a man talking, not
  like a lawyer). "So showing up late and going home early, I guess I can't
  complain too much." (`cancelled-again.html`) "There probably won't be any
  cool pictures of those flights, but when I fly to the ship I'll be sure to
  take a camera." (`a-week-late-and-still-no-pictures.html`) "The family
  resemblance is pretty clear, don't you think?" (`baby-boaz-is-born.html`)
- **definitely** (28 uses; 0 in 2026). "Well, the weather definitely has not
  been our friend recently, and I didn't get to go fly tonight because of
  it." (`cancelled-again.html`)
- **So / Well / Anyway to start a sentence** (34.9, 10.0 and 6.2 per 1,000
  sentences). "Well we just got back from a weekend in NY."
  (`10-days-without-words.html`) "So I echo that question here."
  (`a-calming-storm.html`)
- **though, as well, of course, after all, however, although, also** (though
  9.7 against 0.7; as well 58 uses against 3; of course 5.6 against 0.3).
  "Tonight, though, we experienced the joy of being in the moment&hellip;
  instead of re-living, we were be-living." (`be-living-the-glory-days.html`)
  "I hope this might start a new tradition as well."
  (`a-mark-631-morning.html`)
- **Full disclosure** (16 uses in 14 posts; 0 in 2026), his way of owning a
  gap. "Full disclosure: I haven't read the workbook pictured, just found the
  photo and thought it was cool." (`a-30-mighty-men-new-year.html`)
- **I figured I'd / I wanted to / I just** (how he explains why he is
  writing). "I haven't posted anything lately, so I figured I'd just grab
  something from the past few months and throw it on here."
  (`fast-roping.html`)
- **My point / the bottom line** (19 uses; 1 in 2026). "But my point in all
  of this is that there is a way the Bible says we can hear &ndash; it's by the
  Word of God." (`781.html`)
- **"I" at the front.** 16% of his sentences begin with "I"; 2.7% of the 2026
  sentences do, where "The" (13%), "He" (5%) and "That is" (2.4%) lead.

### Forms of address

He writes to people he knows: "everyone" (7.4), "friends" (4.5), "thanks"
(4.1), "y'all" and "folks" now and then, his wife and sons by name, and the
men of his "30 Mighty Men" lists. "Again, thanks everyone for your prayers
and support as always." (`june-2007-update.html`) He does not address "the
reader" or "a man".

### How he opens

On what just happened to him, in the first person, usually with the time of
day or the reason he is writing. Never on a thesis.

- "So I turned 33 yesterday, and started the day with this Facebook post"
  (`a-once-a-year-elevation-opportunity-hoping-i-have-at-least-33-more.html`)
- "Well it's getting late so this will be short, but we got here"
  (`flyin-wjesus.html`)
- "I was just writing an e-mail to my Bible study group this morning"
  (`its-not-all-good-but-it-can-be.html`)

### How he closes

- **"Peace, Adam"** signs 94 of the 146 posts. It belongs only on posts under
  his own byline.
- The last line before it is a charge, a question or a wish, not a slogan:
  "So how will you apply this?" (`crazy-late-post.html`) "Keep it elevated!"
  (`who-do-you-know.html`) "Well, I'm still learning&hellip; and may you learn
  from my mistakes as I hopefully will as well!"
  (`time-mgmt-vs-priority-mgmt.html`)
- After the signature he often adds a **"PS:"** (27 posts) or a **"Linked
  verses:"** line (17 posts) listing the references he leaned on.

### How he brings Scripture in

- Inside his own sentence, with the speaker named: "like James says, be doers
  of the word also, not just hearers (James 1:22)" (`781.html`); "After all,
  1 John 1:9 says" (`forgiveness-without-apology.html`); "just as Jesus said
  in John 15:15" (`friendship-foundations.html`).
- The reference follows the words, and the version follows the reference
  when he names one: "Jeremiah 9:23-24 (NKJV)" (`who-do-you-know.html`),
  "Philippians 2:3 (NLT)" (`the-4-as-adams-adoration-for-acronyms-and-alliterations.html`).
- He chose versions on purpose and used many. Labels in his posts: NLT 20,
  NKJV 19, NIV 14, HCSB 10, KJV 10, NASB 9, ESV 8, AMP 7, MSG 3. The 2026
  posts name only NKJV (49) and KJV (10). This is why the ruling is "keep his
  wording, add the label".
- He does not stack three or four verse blocks under a heading with no
  sentence of his own between them.

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
- **Concrete biblical anchoring.** When you quote Scripture, keep the
  wording Adam chose and label the version (section 0; NKJV is his usual,
  and the KJV is always welcome). Cite the reference.
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
   judgment &mdash; some are legitimate in context. The post must also show
   `PASS` on its cadence line (section 0); a `FAIL` is not published.
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
- It does not micromanage your rhetorical arc. Since 17 Nov 2026 it does
  measure cadence (section 0), because staccato pairs and fragment runs are
  the tell Adam named; within that, your paragraphs are yours.
- It does not auto-rewrite. The risk of auto-rewriting blog prose is too
  high; the audit produces a report and the human revises.

---

## 7. Reference: existing infrastructure

- `bin/voice_audit_blog.py` &mdash; the scanner (catalog phrases, cadence, and the
  avoid list in section 0.2; one PASS/FAIL line per post)
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
