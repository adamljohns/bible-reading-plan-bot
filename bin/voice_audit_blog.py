#!/usr/bin/env python3
"""voice_audit_blog.py — scan blog posts (or any HTML/MD) for AI-tell phrases.

Modeled on bin/dict_drift_audit.py. Reports each AI-tell hit with file,
line context, suggested human-voice replacement, and category. Does NOT
rewrite automatically — produces a report; the human reviews and revises.

Categories of AI-tell:
  - filler          : "It's worth noting that..." / "It's important to note..."
  - empty-verb      : "delve into" / "navigate" / "embrace" / "leverage"
  - corporate       : "robust" / "comprehensive" / "seamless" / "synergy"
  - tricolon        : Three-item parallel constructions overused
  - x-not-just-y    : "X is not just Y, it's Z" / "not just A, but B"
  - transition-glue : "Furthermore," / "Moreover," / "Additionally,"
  - hedge           : "Some might argue" / "Many would say"
  - empty-intro     : "In today's world" / "In an era of"
  - weasel-quant    : "various" / "numerous" / "myriad" / "plethora"
  - therapy         : "validate" / "harmful" / "unhealthy" / "lived experience"
  - em-dash-overuse : Three or more em-dashes in a single paragraph

Usage:
  python3 bin/voice_audit_blog.py docs/blog/                 # all blog posts
  python3 bin/voice_audit_blog.py docs/blog/specific-post.html
  python3 bin/voice_audit_blog.py docs/blog/ --markdown > voice-audit.md
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# AI-tell catalog.
# Each entry: (category, pattern, severity, suggestion).
# ---------------------------------------------------------------------------

AI_TELLS: list[tuple[str, str, str, str]] = [
    # ----- filler -----
    ("filler", r"\bit['’]s worth noting that\b", "hard", "Cut entirely; if the thing's worth noting, say it."),
    ("filler", r"\bit['’]s important to (?:note|remember|understand) that\b", "hard", "Cut entirely; just say the thing."),
    ("filler", r"\bit should be noted that\b", "hard", "Cut entirely."),
    ("filler", r"\bit goes without saying that\b", "hard", "If it goes without saying, don't say it."),
    ("filler", r"\bneedless to say\b", "hard", "Cut entirely."),
    ("filler", r"\bin conclusion,\b", "hard", "Cut. End the piece with the actual conclusion."),
    ("filler", r"\bto summari[sz]e,\b", "hard", "Cut; or write the actual summary."),
    ("filler", r"\bin essence,\b", "hard", "Cut."),
    ("filler", r"\bat the end of the day,?\b", "soft", "Often filler; cut or rephrase concretely."),
    ("filler", r"\bin today['’]s (?:world|society|economy|landscape)\b", "hard", "Cliché opener; replace with specific date / event."),
    ("filler", r"\bin an era of\b", "hard", "Cliché opener; replace with specific context."),

    # ----- empty verbs -----
    ("empty-verb", r"\bdelv(?:e|ing) into\b", "hard", "Replace: explore, examine, dig into, study."),
    ("empty-verb", r"\bnavigate (?:the|this|these|complex)\b", "soft", "Often AI-corporate; replace: work through, traverse, handle."),
    ("empty-verb", r"\bembrace\b(?!\s+(?:the\s+cross|the\s+gospel|repentance|sanctification))", "soft", "Often AI-corporate; replace: accept, take up, receive."),
    ("empty-verb", r"\bleverage\b", "hard", "Corporate-speak; replace: use, draw on, take advantage of."),
    ("empty-verb", r"\bunlock (?:the\s+)?(?:potential|power)\b", "hard", "Corporate; replace with specific action."),
    ("empty-verb", r"\bgame[- ]?chang(?:e|er|ing)\b", "hard", "Cliché; replace with specific impact."),
    ("empty-verb", r"\btap into\b", "soft", "Often filler; replace: draw on, use, access."),
    ("empty-verb", r"\bharness\b", "soft", "Corporate; replace: use, channel, employ."),

    # ----- corporate buzzwords -----
    ("corporate", r"\brobust\b", "soft", "Corporate; replace: strong, sturdy, well-built, dependable."),
    ("corporate", r"\bcomprehensive\b", "soft", "Corporate; replace: full, complete, thorough, broad."),
    ("corporate", r"\bseamless\b", "soft", "Corporate; replace: smooth, uninterrupted, unbroken."),
    ("corporate", r"\bsynerg(?:y|ies|istic)\b", "hard", "Corporate-jargon; cut or rephrase concretely."),
    ("corporate", r"\bstreamlin\w+\b", "soft", "Corporate; replace: simplify, tighten, speed up."),
    ("corporate", r"\bholistic\b", "soft", "Often vague; replace: full-orbed, whole-person, complete."),
    ("corporate", r"\bcutting[- ]edge\b", "soft", "Cliché; replace: newest, latest, recent."),
    ("corporate", r"\bbest practices?\b", "soft", "Corporate; replace: proven methods, tested approaches."),
    ("corporate", r"\bvalue proposition\b", "hard", "Corporate-jargon."),

    # ----- X not just Y but Z -----
    ("x-not-just-y", r"\b(?:is|are|was|were)\s+not just\s+\w+", "soft", "Overused AI construction; vary the rhetoric."),
    ("x-not-just-y", r"\b(?:isn['’]t|aren['’]t|wasn['’]t|weren['’]t)\s+just\s+about\s+\w+", "soft", "Overused AI construction; vary the rhetoric."),
    ("x-not-just-y", r"\bmore than just\s+a\b", "soft", "Overused construction."),

    # ----- transition glue -----
    ("transition-glue", r"^\s*Furthermore,", "soft", "AI transition glue; cut or replace with concrete bridge."),
    ("transition-glue", r"^\s*Moreover,", "soft", "AI transition glue; cut."),
    ("transition-glue", r"^\s*Additionally,", "soft", "AI transition glue; cut."),
    ("transition-glue", r"^\s*Furthermore,?\s+", "soft", "AI transition glue."),
    ("transition-glue", r"\.\s+Furthermore,", "soft", "AI transition glue; restructure or cut."),
    ("transition-glue", r"\.\s+Moreover,", "soft", "AI transition glue; restructure or cut."),
    ("transition-glue", r"\.\s+Additionally,", "soft", "AI transition glue; restructure or cut."),

    # ----- hedge -----
    ("hedge", r"\bsome (?:might|would|may)\s+argue\b", "soft", "Hedge; name the actual argument or cut."),
    ("hedge", r"\bmany (?:would|might|may)\s+say\b", "soft", "Hedge; name actual speakers or cut."),
    ("hedge", r"\barguably\b", "soft", "Hedge; either argue or drop."),
    ("hedge", r"\bsome\s+(?:believe|think|argue|hold|claim)\b", "soft", "Hedge; name actual people or cut."),

    # ----- weasel quantifiers -----
    ("weasel-quant", r"\bnumerous\b", "soft", "Corporate; replace: many, several, lots of, dozens of (be specific)."),
    ("weasel-quant", r"\bmyriad\b", "soft", "Often filler; replace: many, countless (specific number if possible)."),
    ("weasel-quant", r"\bplethora\b", "hard", "AI-corporate; replace: many, lots of, surplus."),
    ("weasel-quant", r"\bvarious\b", "soft", "Often vague; replace: several / a few / specific list."),
    ("weasel-quant", r"\ba multitude of\b", "soft", "Often AI-pompous; replace: many, lots of."),

    # ----- therapy register -----
    ("therapy", r"\btrauma\b(?!tic\s+event)", "soft", "Therapy-culture; replace: suffering, affliction, the breaking of body / soul."),
    ("therapy", r"\bharmful\b(?!\s+to\s+(?:the\s+soul|the\s+body))", "soft", "Therapy-culture; replace: sinful, against God's law, against the soul's good."),
    ("therapy", r"\bsafe space\b", "hard", "Not a biblical category; reject."),
    ("therapy", r"\blived experience\b", "soft", "Therapy-culture; replace: testimony, witness."),
    ("therapy", r"\bvalidate\b", "soft", "Therapy-culture; replace: confirm, affirm, commend."),
    ("therapy", r"\bunhealthy patterns?\b", "soft", "Therapy-culture; replace: sin patterns, besetting sins."),

    # ----- empty-intro -----
    ("empty-intro", r"^(?:In|For)\s+(?:today|this day and age|the modern world|our modern world)", "hard", "AI-cliché opener; replace with specific date / event."),
    ("empty-intro", r"\bever-(?:changing|evolving|growing)\b", "soft", "AI-cliché; replace with specific change being noted."),

    # ----- mid-sentence semicolons (often AI tell when overused) — flagged as soft -----
    # (We don't ban semicolons; we just note overuse.)
]

OK_MARKER = re.compile(r"(?:#|<!--)\s*voice-ok:\s*([^:]+):\s*(.+?)(?:-->|\n|$)", re.I)


@dataclass
class Finding:
    file: str
    line_hint: int
    category: str
    severity: str
    matched: str
    context: str
    suggestion: str


def _strip_html(s: str) -> str:
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[a-zA-Z][a-zA-Z0-9]*;", " ", s)
    return s


def _context(text: str, start: int, end: int, pad: int = 50) -> str:
    a = max(0, start - pad)
    b = min(len(text), end + pad)
    snippet = text[a:b]
    snippet = re.sub(r"\s+", " ", snippet)
    return ("..." if a > 0 else "") + snippet + ("..." if b < len(text) else "")


def _line_hint(text: str, idx: int) -> int:
    return text[:idx].count("\n") + 1


def scan_file(path: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except Exception:
        return findings

    # Allow file-level opt-out via comment.
    if "<!-- voice-audit-skip -->" in raw or "# voice-audit-skip" in raw:
        return findings

    # We scan the visible text (HTML stripped). For HTML, this loses line numbers,
    # but the matched-context is searchable in the file. Markdown files we keep raw.
    is_html = path.lower().endswith((".html", ".htm"))
    text = _strip_html(raw) if is_html else raw

    for category, pattern, severity, suggestion in AI_TELLS:
        rgx = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        for m in rgx.finditer(text):
            findings.append(
                Finding(
                    file=path,
                    line_hint=_line_hint(text, m.start()),
                    category=category,
                    severity=severity,
                    matched=m.group(0),
                    context=_context(text, m.start(), m.end()),
                    suggestion=suggestion,
                )
            )

    # Em-dash overuse check (paragraph-level: 3+ em-dashes per paragraph)
    paragraphs = re.split(r"\n\s*\n+", text)
    for i, p in enumerate(paragraphs):
        em_count = p.count("—") + p.count("&mdash;")
        if em_count >= 3:
            findings.append(
                Finding(
                    file=path,
                    line_hint=0,
                    category="em-dash-overuse",
                    severity="soft",
                    matched=f"{em_count} em-dashes in one paragraph",
                    context=p[:120] + ("..." if len(p) > 120 else ""),
                    suggestion="Vary punctuation; em-dash overuse is an AI tell. Replace some with commas, colons, or sentence breaks.",
                )
            )

    return findings


def scan_path(path: str) -> list[Finding]:
    p = Path(path)
    if p.is_file():
        return scan_file(str(p))
    if p.is_dir():
        out: list[Finding] = []
        for child in sorted(p.rglob("*")):
            if child.is_file() and child.suffix.lower() in (".html", ".htm", ".md", ".markdown"):
                out.extend(scan_file(str(child)))
        return out
    print(f"  ERROR: {path} not found", file=sys.stderr)
    sys.exit(2)


def report_text(findings: list[Finding]) -> int:
    hard = [f for f in findings if f.severity == "hard"]
    soft = [f for f in findings if f.severity == "soft"]
    if not findings:
        print("\n  CLEAN: no AI-tell phrases found.\n")
        return 0
    print(f"\n  HITS: {len(hard)} hard / {len(soft)} soft / {len(findings)} total\n")

    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    for file, ff in by_file.items():
        print(f"\n  === {os.path.basename(file)} ({len(ff)} hits) ===")
        # Group within file by category for readability
        by_cat: dict[str, list[Finding]] = {}
        for f in ff:
            by_cat.setdefault(f.category, []).append(f)
        for cat, cf in by_cat.items():
            print(f"    --- {cat} ({len(cf)}) ---")
            for f in cf:
                mark = "[H]" if f.severity == "hard" else "[S]"
                print(f"    {mark} '{f.matched}' (~ln {f.line_hint})")
                print(f"        ctx: ...{f.context}...")
                print(f"        fix: {f.suggestion}")
    return 1 if hard else 0


def report_markdown(findings: list[Finding]) -> int:
    hard = [f for f in findings if f.severity == "hard"]
    soft = [f for f in findings if f.severity == "soft"]
    print("# Blog Voice Audit\n")
    print(f"**{len(hard)} hard hits** &middot; **{len(soft)} soft hits** &middot; **{len(findings)} total**\n")
    if not findings:
        print("\nNo AI-tell phrases found.\n")
        return 0
    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)
    for file, ff in sorted(by_file.items()):
        print(f"\n## {os.path.basename(file)} ({len(ff)})\n")
        print("| Severity | Category | Matched | Context | Suggestion |")
        print("|---|---|---|---|---|")
        for f in ff:
            ctx = f.context.replace("|", "&#124;")
            print(f"| {f.severity} | {f.category} | `{f.matched}` | {ctx} | {f.suggestion} |")
    return 1 if hard else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan HTML/MD for AI-tell phrases.")
    ap.add_argument("targets", nargs="+", help="Files or directories to scan.")
    ap.add_argument("--markdown", action="store_true", help="Output as Markdown.")
    args = ap.parse_args()

    all_findings: list[Finding] = []
    for t in args.targets:
        all_findings.extend(scan_path(t))

    if args.markdown:
        return report_markdown(all_findings)
    return report_text(all_findings)


if __name__ == "__main__":
    sys.exit(main())
