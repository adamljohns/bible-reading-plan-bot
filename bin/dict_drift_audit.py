#!/usr/bin/env python3
"""MOOP Dictionary drift audit.

Greps a batch JSON file (or any dictionary entry HTML) for banned-register
patterns defined in DICTIONARY-VOICE-LOCK.md. Reports each hit with file,
slug, field, and surrounding context.

Usage:
    python3 bin/dict_drift_audit.py data/dictionary-batches/batch-NN.json
    python3 bin/dict_drift_audit.py docs/dictionary/some-slug.html
    python3 bin/dict_drift_audit.py data/dictionary-batches/  # all batches in dir

Exit codes:
    0 — clean (no banned-register hits)
    1 — banned-register hits found
    2 — usage / file error

The voice-lock standard is documented in DICTIONARY-VOICE-LOCK.md.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Banned register catalog.
# Each entry: (category, pattern, severity, note).
# Pattern is a case-insensitive regex.
# Severity: "hard" (must be removed), "soft" (review required).
# ---------------------------------------------------------------------------

BANNED: list[tuple[str, str, str, str]] = [
    # ----- 4.1 Academic-ecumenical hedging -----
    ("hedge", r"\btensions? between\b", "hard",
     "Use 'corruption' / 'Reformation as recovery,' not 'tensions between.'"),
    ("hedge", r"\bengages? warily\b", "hard",
     "Replace with explicit Reformed critique."),
    ("hedge", r"\bengages? cautiously\b", "hard",
     "Replace with explicit Reformed critique."),
    ("hedge", r"\bdoctrinally serious\b", "soft",
     "Do not apply this honorific to a non-Reformed framework as a whole. "
     "Specific points within a tradition can be doctrinally serious; the "
     "framework as a whole is not."),
    ("hedge", r"\bscholars debate\b", "hard",
     "Reframe: name the position, name the framework, rebut."),
    ("hedge", r"\bmany scholars believe\b", "hard",
     "Reframe: name the position, name the framework, rebut."),
    ("hedge", r"\bmost scholars argue\b", "hard",
     "Reframe: name the position, name the framework, rebut."),
    ("hedge", r"\brecent scholarship suggests\b", "hard",
     "Reframe: name the position, name the framework, rebut."),
    ("hedge", r"\bthe conversation between\b", "hard",
     "Theology is not a conversation; truth is not a conversation."),
    ("hedge", r"\ball sides agree\b", "hard",
     "Used to flatten real doctrinal difference."),
    ("hedge", r"\bcommon ground\b", "soft",
     "Often used to soft-pedal real doctrinal difference."),
    ("hedge", r"\bshared heritage\b", "soft",
     "Often used to flatten real doctrinal difference."),
    ("hedge", r"\bcomplex view of\b", "soft",
     "Often soft-pedaling; name the position more directly."),
    ("hedge", r"\bcomplicated relationship with\b", "soft",
     "Often soft-pedaling; name the position more directly."),
    ("hedge", r"\bnuanced position\b", "soft",
     "Often soft-pedaling; name the position more directly."),
    ("hedge", r"\bin dialogue with\b", "hard",
     "Theology is not a dialogue with error."),

    # ----- 4.2 Therapy-culture register -----
    ("therapy", r"\btrauma\b", "soft",
     "Substitute biblical: suffering / affliction / the breaking of body or "
     "soul under sin and curse."),
    ("therapy", r"\bharmful\b(?!\s+to\s+(?:the\s+soul|the\s+body))", "soft",
     "Substitute biblical: sinful / against God's law / against the soul's good."),
    ("therapy", r"\bsafe space\b", "hard",
     "Not a biblical category; reject entirely."),
    ("therapy", r"\blived experience\b", "soft",
     "Substitute biblical: testimony / witness."),
    ("therapy", r"\bcentering voices?\b", "hard",
     "Substitute biblical: giving the platform / testifying."),
    ("therapy", r"\bdecentering voices?\b", "hard",
     "Substitute biblical: giving the platform / testifying."),
    ("therapy", r"\bmarginalized\b", "soft",
     "Often autonomous moral-political category; biblical categories are "
     "the oppressed / the poor / the widow / the orphan / the stranger / "
     "the afflicted."),
    ("therapy", r"\bvalidate\b", "soft",
     "Substitute biblical: confirm / affirm / commend."),
    ("therapy", r"\bunhealthy patterns?\b", "soft",
     "Substitute biblical: sin patterns / besetting sins."),

    # ----- 4.3 Progressive race / gender / sexuality framing -----
    ("progressive", r"\bwhite supremacy\b", "hard",
     "Autonomous explanatory category; biblical categories are sin / heart."),
    ("progressive", r"\bpatriarchy\b(?!\s+(?:patriarchal\s+practice|of\s+the\s+ancient))", "soft",
     "Often used as autonomous explanatory category; biblical categories "
     "are creational order / sin / fallen heart."),
    ("progressive", r"\bheteronormativ", "hard",
     "Autonomous explanatory category from queer theory; reject the framing."),
    ("progressive", r"\bcisnormativ", "hard",
     "Autonomous explanatory category from queer theory; reject the framing."),
    ("progressive", r"\bintersectional", "hard",
     "Reject entirely; biblical anthropology is one-in-Adam, one-in-Christ."),
    ("progressive", r"\b(?:cisgender|cis-gender)\b", "hard",
     "Adopts queer-theory categories; reject the framing."),
    ("progressive", r"\bgender (?:assigned|identity)\b", "hard",
     "The categories themselves are corruption of Gen 1:27."),
    ("progressive", r"\bnon-binary\b", "hard",
     "Reject the framing; affirm imago Dei while naming the gender claim as "
     "corruption of Gen 1:27."),
    ("progressive", r"\b(?:they|their|them)/(?:them|their)\b", "soft",
     "Do not adopt individual they/them pronouns; biblical pronouns follow "
     "biological sex."),
    ("progressive", r"\binclusiv(?:e|ity)\b", "soft",
     "Often autonomous virtue; the gospel's inclusion is "
     "repentance-and-faith inclusion."),
    ("progressive", r"\baffirming\b(?!\s+(?:Reformed|the\s+gospel|biblical|creational))", "soft",
     "Often code for LGBTQ-affirming; specify which doctrine is affirmed."),

    # ----- 4.4 Historical-critical assumptions -----
    ("histcrit", r"\bdeutero-isaiah\b", "hard",
     "One Isaiah; reject the source-critical division."),
    ("histcrit", r"\btrito-isaiah\b", "hard",
     "One Isaiah; reject the source-critical division."),
    ("histcrit", r"\b(?:JEDP|J\s+E\s+D\s+P)\b", "hard",
     "Reject documentary hypothesis; affirm Mosaic authorship."),
    ("histcrit", r"\bdocumentary hypothesis\b", "hard",
     "Reject; affirm Mosaic authorship."),
    ("histcrit", r"\b(?:priestly|yahwist|elohist)\s+source\b", "hard",
     "Reject source-criticism's atomization of the Pentateuch."),
    ("histcrit", r"\bdeuteronomistic historian\b", "hard",
     "Reject when used to deny historicity of Kings."),
    ("histcrit", r"\bpost-exilic redactor\b", "hard",
     "Reject when used to deny historicity."),
    ("histcrit", r"\bdeutero-pauline\b", "hard",
     "All 13 Pauline epistles are Paul."),
    ("histcrit", r"\bpastoral(?:s)?\s+(?:are\s+)?(?:not\s+)?pauline\b", "hard",
     "Reject; the Pastoral Epistles are Pauline."),
    ("histcrit", r"\blater (?:addition|composition|redaction)\b", "soft",
     "Often hist-crit signal denying canonical authorship/dating."),

    # ----- 4.5 Soft-pedal patterns -----
    ("softpedal", r"\bsome traditions believe\b", "hard",
     "Relativizes the truth claim; name the position and rebut."),
    ("softpedal", r"\bthe bible can be read as\b", "hard",
     "Makes Scripture's claims optional; name the actual reading and rebut."),
    ("softpedal", r"\bthis is debated\b", "soft",
     "Often implies legitimate alternatives where Scripture is clear."),
    ("softpedal", r"\bit is possible to see\b", "soft",
     "Often softens a hard biblical claim."),
    ("softpedal", r"\bone perspective\b", "soft",
     "Treats Scripture as one perspective among several."),

    # ----- 4.6 Universalist drift -----
    ("universalist", r"\ball people will eventually\b", "hard",
     "Universalist drift; reject."),
    ("universalist", r"\bgod will eventually save all\b", "hard",
     "Universalist drift; reject."),
    ("universalist", r"\bultimate restoration\b", "soft",
     "Can be Origenist universalist code."),
    ("universalist", r"\bgod's love would not allow\b", "soft",
     "Often used to deny eternal conscious punishment."),
    ("universalist", r"\blarger hope\b", "hard",
     "Technical universalist euphemism."),

    # ----- 4.7 Modernist worship register -----
    ("worship-modernist", r"\bworship experience\b", "soft",
     "Substitute: corporate worship / worship of God."),
    ("worship-modernist", r"\bworship encounter\b", "soft",
     "Substitute: corporate worship / worship of God."),
    ("worship-modernist", r"\bjourney of faith\b", "soft",
     "Substitute: the Christian life / sanctification / walking with the Lord."),
    ("worship-modernist", r"\bspirituality\b(?!\s+(?:of\s+the|in\s+the))", "soft",
     "Often used without qualifier as if neutral-good; "
     "substitute: religion / devotion / piety / the Christian life."),
]


# ---------------------------------------------------------------------------
# Voice-lock-ok marker
# An entry can carry an inline marker that suppresses specific findings:
#     "# voice-lock-ok: <pattern-category-or-phrase>: <reason>"
# Place it inside any field's text. The audit ignores hits in the field IF
# the marker mentions the matching category or the matching phrase.
# ---------------------------------------------------------------------------

OK_MARKER = re.compile(r"#\s*voice-lock-ok:\s*([^:]+):\s*(.+?)(?:\n|$)", re.I)


@dataclass
class Finding:
    file: str
    slug: str | None
    field: str
    category: str
    severity: str
    pattern: str
    note: str
    matched_text: str
    context: str


def _strip_html_basic(s: str) -> str:
    """Strip HTML tags + entities to give cleaner regex matching."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&[a-zA-Z][a-zA-Z0-9]*;", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def _context(haystack: str, start: int, end: int, pad: int = 60) -> str:
    a = max(0, start - pad)
    b = min(len(haystack), end + pad)
    snippet = haystack[a:b]
    snippet = snippet.replace("\n", " ")
    return ("..." if a > 0 else "") + snippet + ("..." if b < len(haystack) else "")


def _ok_for_field(field_text: str, category: str, pattern: str) -> bool:
    """Return True if this field has a voice-lock-ok marker covering the cat/pat."""
    for m in OK_MARKER.finditer(field_text):
        tag = m.group(1).strip().lower()
        if tag == category.lower() or tag in pattern.lower():
            return True
    return False


def scan_text(text: str, file: str, slug: str | None, field: str) -> list[Finding]:
    findings: list[Finding] = []
    cleaned = _strip_html_basic(text)
    for category, pattern, severity, note in BANNED:
        rgx = re.compile(pattern, re.IGNORECASE)
        for m in rgx.finditer(cleaned):
            if _ok_for_field(text, category, pattern):
                continue
            findings.append(Finding(
                file=file,
                slug=slug,
                field=field,
                category=category,
                severity=severity,
                pattern=pattern,
                note=note,
                matched_text=m.group(0),
                context=_context(cleaned, m.start(), m.end()),
            ))
    return findings


def scan_batch_json(path: str) -> list[Finding]:
    findings: list[Finding] = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"  WARN: {path} is not a batch (top-level not list)")
        return findings
    SCANNED_FIELDS = (
        "etymology", "biblical_def", "webster_summary",
        "corruption_summary", "roots_summary",
    )
    LIST_FIELDS = ("webster_full", "corruption_paragraphs", "roots_lines", "usage")
    for entry in data:
        slug = entry.get("slug", "(no-slug)")
        for field in SCANNED_FIELDS:
            text = entry.get(field) or ""
            if isinstance(text, str):
                findings.extend(scan_text(text, path, slug, field))
        for field in LIST_FIELDS:
            arr = entry.get(field) or []
            if isinstance(arr, list):
                for i, item in enumerate(arr):
                    if isinstance(item, str):
                        findings.extend(scan_text(item, path, slug, f"{field}[{i}]"))
        # scriptures: only check the kv text, not refs
        for i, sc in enumerate(entry.get("scriptures") or []):
            if isinstance(sc, list) and len(sc) >= 2 and isinstance(sc[1], str):
                findings.extend(scan_text(sc[1], path, slug, f"scriptures[{i}].text"))
    return findings


def scan_html(path: str) -> list[Finding]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    slug = Path(path).stem
    # try to extract sections by class name
    findings = scan_text(html, path, slug, "html-full")
    return findings


def scan_path(path: str) -> list[Finding]:
    p = Path(path)
    findings: list[Finding] = []
    if p.is_file():
        if p.suffix == ".json":
            findings.extend(scan_batch_json(str(p)))
        elif p.suffix == ".html":
            findings.extend(scan_html(str(p)))
        else:
            print(f"  SKIP: {p} (unknown extension)")
    elif p.is_dir():
        for child in sorted(p.iterdir()):
            if child.suffix in (".json", ".html"):
                findings.extend(scan_path(str(child)))
    else:
        print(f"  ERROR: {path} not found", file=sys.stderr)
        sys.exit(2)
    return findings


def report(findings: list[Finding]) -> int:
    hard = [f for f in findings if f.severity == "hard"]
    soft = [f for f in findings if f.severity == "soft"]
    if not findings:
        print("\n  CLEAN: no banned-register hits found.\n")
        return 0

    print(f"\n  HITS: {len(hard)} hard / {len(soft)} soft / "
          f"{len(findings)} total\n")

    by_file: dict[str, list[Finding]] = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    for file, file_findings in by_file.items():
        print(f"\n  === {file} ===")
        by_slug: dict[str | None, list[Finding]] = {}
        for f in file_findings:
            by_slug.setdefault(f.slug, []).append(f)
        for slug, slug_findings in by_slug.items():
            print(f"    --- {slug or '(no-slug)'} ---")
            for f in slug_findings:
                mark = "[H]" if f.severity == "hard" else "[S]"
                print(f"    {mark} {f.category:15} {f.field:30} '{f.matched_text}'")
                print(f"        ctx: ...{f.context.strip()}...")
                print(f"        fix: {f.note}")
            print()
    print(f"\n  {len(hard)} HARD hit(s); {len(soft)} SOFT hit(s).")
    print("  HARD hits must be revised. SOFT hits require review.")
    print("  See DICTIONARY-VOICE-LOCK.md for full rationale.\n")
    return 1 if hard else 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    targets = sys.argv[1:]
    all_findings: list[Finding] = []
    for t in targets:
        print(f"  Auditing {t}")
        all_findings.extend(scan_path(t))
    return report(all_findings)


if __name__ == "__main__":
    sys.exit(main())
