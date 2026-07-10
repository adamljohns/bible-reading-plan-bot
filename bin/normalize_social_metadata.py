#!/usr/bin/env python3
"""Normalize Open Graph and Twitter metadata across the static usmcmin.org site.

Designed for deployment-time use: it updates the checked-out docs/ tree before
R2 sync without creating tens of thousands of generated-file commits.
Uses Python standard library only so it runs on GitHub Actions without setup.
"""
from __future__ import annotations

import argparse
import html
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

SITE = "https://usmcmin.org"
VERSION = "2026-07"

CARD_URLS = {
    "default": f"{SITE}/assets/og/og-default-{VERSION}.png",
    "bible": f"{SITE}/assets/og/og-bible-{VERSION}.png",
    "dictionary": f"{SITE}/assets/og/og-dictionary-{VERSION}.png",
    "churches": f"{SITE}/assets/og/og-churches-{VERSION}.png",
    "worship": f"{SITE}/assets/og/og-worship-{VERSION}.png",
    "assessments": f"{SITE}/assets/og/og-assessments-{VERSION}.png",
    "blog": f"{SITE}/assets/og/og-blog-{VERSION}.png",
    "resources": f"{SITE}/assets/og/og-resources-{VERSION}.png",
    "connect": f"{SITE}/assets/og/og-connect-{VERSION}.png",
}
HOME_CARD_URL = f"{SITE}/assets/og/og-home-{VERSION}.png"

SECTION_LABELS = {
    "default": "U.S.M.C. Ministries",
    "bible": "Bible Tools",
    "dictionary": "The MOOP Dictionary",
    "churches": "Church Directory",
    "worship": "Worship & Devotion",
    "assessments": "Biblical Assessments",
    "blog": "Ministry Blog",
    "resources": "Ministry Resources",
    "connect": "Connect with U.S.M.C. Ministries",
}

GENERIC_DESCRIPTIONS = {
    "default": "Christ-centered tools for faith, family, freedom, and fraternity from U.S.M.C. Ministries.",
    "bible": "Scripture text, translation tools, reading plans, cross-references, and biblical word-study resources from U.S.M.C. Ministries.",
    "dictionary": "Biblical definitions, theological context, word origins, and Scripture references from the MOOP Dictionary.",
    "churches": "Church profile and directory information—including location, doctrine, leadership, and ministry details when available.",
    "worship": "Christ-centered worship, songs, Scripture connections, prayer, and devotional resources from U.S.M.C. Ministries.",
    "assessments": "Biblical self-assessments for husbands, fathers, men, and citizens—built for honest reflection and practical action.",
    "blog": "Faith, family, freedom, fraternity, and ministry field notes from Adam ‘MOOP’ Johns and U.S.M.C. Ministries.",
    "resources": "Practical ministry tools, studies, downloads, and biblical resources from U.S.M.C. Ministries.",
    "connect": "Connect with U.S.M.C. Ministries for mentoring, counseling, brotherhood, and service opportunities.",
}

META_RE = re.compile(r"<meta\b[^>]*>", re.I)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title\s*>", re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1\s*>", re.I | re.S)
CANON_RE = re.compile(r"<link\b(?=[^>]*\brel\s*=\s*(['\"])canonical\1)[^>]*>", re.I)
HEAD_END_RE = re.compile(r"</head\s*>", re.I)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")
ATTR_RE = re.compile(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", re.I | re.S)


def attrs(tag: str) -> dict[str, str]:
    return {m.group(1).lower(): html.unescape(m.group(3)) for m in ATTR_RE.finditer(tag)}


def clean_text(raw: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", raw))).strip()


def clipped(value: str, limit: int) -> str:
    value = SPACE_RE.sub(" ", value).strip()
    if len(value) <= limit:
        return value
    cut = value[: limit - 1].rsplit(" ", 1)[0]
    return (cut or value[: limit - 1]).rstrip(" ,;:-") + "…"


def section_for(rel: Path) -> str:
    parts = [p.lower() for p in rel.parts]
    first = parts[0] if len(parts) > 1 else ""
    name = rel.stem.lower()

    if first in {"chapters", "verse", "readings", "proverbs", "lbcf", "institutes"}:
        return "bible"
    if first in {"dictionary", "lexicon"}:
        return "dictionary"
    if first == "churches" or name in {"churches", "near-me", "directory-overview"}:
        return "churches"
    if first == "worship" or name.startswith("worship"):
        return "worship"
    if first == "blog" or name.startswith("blog"):
        return "blog"
    if name in {"assessments", "real-man-assessment", "happy-husband", "fulfilled-father",
                "purity-assessment", "resolute-citizen-assessment"}:
        return "assessments"
    if name in {"connect", "contacts", "mentoring", "counseling", "serving-intake", "prayer"}:
        return "connect"
    if name in {"bible", "bible-plan", "bible-reading-plan", "chronological", "crossrefs",
                "catechism", "lbcf-full", "mbt", "atlas"}:
        return "bible"
    if name in {"resources", "dev-resources", "military-ministry-resources", "downloads", "mops",
                "retirement", "about", "gospel", "watchman"}:
        return "resources"
    return "default"


def canonical_for(rel: Path, source: str) -> str:
    match = CANON_RE.search(source)
    if match:
        a = attrs(match.group(0))
        href = a.get("href", "").strip()
        if href.startswith("https://usmcmin.org/") or href == "https://usmcmin.org":
            return href
    if rel.as_posix() == "index.html":
        return SITE + "/"
    # Quote spaces and non-ASCII while preserving URL path separators.
    return SITE + "/" + quote(rel.as_posix(), safe="/-._~")


def title_for(source: str, rel: Path, existing: dict[str, list[str]], section: str) -> str:
    candidates = []
    candidates.extend(existing.get("og:title", []))
    m = TITLE_RE.search(source)
    if m:
        candidates.append(clean_text(m.group(1)))
    m = H1_RE.search(source)
    if m:
        candidates.append(clean_text(m.group(1)))
    candidates.append(rel.stem.replace("-", " ").replace("_", " ").title())
    for candidate in candidates:
        if candidate:
            return clipped(candidate, 110)
    return SECTION_LABELS[section]


def description_for(source: str, title: str, existing: dict[str, list[str]], section: str) -> str:
    # Legacy church pages often contain a false copied phrase saying every
    # church is in Fredericksburg, VA. Do not preserve that bad boilerplate.
    if section == "churches":
        return clipped(f"{title}. {GENERIC_DESCRIPTIONS[section]}", 200)
    for key in ("description", "og:description", "twitter:description"):
        for value in existing.get(key, []):
            value = clean_text(value)
            if value:
                return clipped(value, 200)
    generic = GENERIC_DESCRIPTIONS[section]
    if section in {"dictionary", "churches", "bible", "blog", "worship"}:
        return clipped(f"{title}. {generic}", 200)
    return generic


def meta_values(source: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for tag in META_RE.findall(source):
        a = attrs(tag)
        key = (a.get("property") or a.get("name") or "").lower()
        if key:
            found.setdefault(key, []).append(a.get("content", ""))
    return found


def is_social_meta(tag: str) -> bool:
    a = attrs(tag)
    prop = a.get("property", "").lower()
    name = a.get("name", "").lower()
    # Some older pages incorrectly used name="og:*" instead of property="og:*".
    return prop.startswith("og:") or name.startswith("og:") or name.startswith("twitter:")


def is_description_meta(tag: str) -> bool:
    a = attrs(tag)
    return a.get("name", "").lower() == "description"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def normalized_block(title: str, description: str, url: str, image: str, section: str,
                     og_type: str = "website") -> str:
    alt = f"{SECTION_LABELS[section]} — U.S.M.C. Ministries"
    return "\n".join([
        f'    <meta name="description" content="{esc(description)}">',
        f'    <meta property="og:title" content="{esc(title)}">',
        f'    <meta property="og:description" content="{esc(description)}">',
        f'    <meta property="og:type" content="{og_type}">',
        f'    <meta property="og:url" content="{esc(url)}">',
        '    <meta property="og:site_name" content="U.S.M.C. Ministries">',
        f'    <meta property="og:image" content="{esc(image)}">',
        f'    <meta property="og:image:secure_url" content="{esc(image)}">',
        '    <meta property="og:image:type" content="image/png">',
        '    <meta property="og:image:width" content="1200">',
        '    <meta property="og:image:height" content="630">',
        f'    <meta property="og:image:alt" content="{esc(alt)}">',
        '    <meta name="twitter:card" content="summary_large_image">',
        f'    <meta name="twitter:title" content="{esc(title)}">',
        f'    <meta name="twitter:description" content="{esc(description)}">',
        f'    <meta name="twitter:image" content="{esc(image)}">',
        f'    <meta name="twitter:image:alt" content="{esc(alt)}">',
    ])


def normalize(source: str, rel: Path) -> tuple[str, str]:
    if not HEAD_END_RE.search(source):
        return source, "no-head"
    existing = meta_values(source)
    section = section_for(rel)
    title = title_for(source, rel, existing, section)
    description = description_for(source, title, existing, section)
    url = canonical_for(rel, source)
    image = HOME_CARD_URL if rel.as_posix() == "index.html" else CARD_URLS[section]

    # Remove all existing social tags and duplicate descriptions, then add one
    # canonical set immediately before </head>.
    source = META_RE.sub(lambda m: "" if is_social_meta(m.group(0)) or is_description_meta(m.group(0)) else m.group(0), source)
    og_type = "article" if section == "blog" and len(rel.parts) > 1 else "website"
    block = normalized_block(title, description, url, image, section, og_type)
    source = HEAD_END_RE.sub(block + "\n</head>", source, count=1)
    return source, section


def verify(source: str) -> list[str]:
    values = meta_values(source)
    required = [
        "description", "og:title", "og:description", "og:type", "og:url", "og:site_name",
        "og:image", "og:image:secure_url", "og:image:type", "og:image:width",
        "og:image:height", "og:image:alt", "twitter:card", "twitter:title",
        "twitter:description", "twitter:image", "twitter:image:alt",
    ]
    errors = []
    for key in required:
        if len(values.get(key, [])) != 1:
            errors.append(f"{key} count={len(values.get(key, []))}")
    if values.get("og:image") != values.get("twitter:image"):
        errors.append("og:image/twitter:image mismatch")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("docs"))
    ap.add_argument("--check", action="store_true", help="plan and validate without writing")
    ap.add_argument("--limit", type=int, default=0, help="process only N files (tests)")
    args = ap.parse_args()

    files = sorted(args.root.rglob("*.html"))
    if args.limit:
        files = files[:args.limit]
    counts = Counter()
    failures = []
    for path in files:
        rel = path.relative_to(args.root)
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            updated, section = normalize(source, rel)
            if section == "no-head":
                counts["skipped:no-head"] += 1
                continue
            errors = verify(updated)
            if errors:
                failures.append(f"{rel}: {', '.join(errors)}")
                continue
            counts[f"section:{section}"] += 1
            if updated != source:
                counts["changed"] += 1
                if not args.check:
                    path.write_text(updated, encoding="utf-8")
            else:
                counts["unchanged"] += 1
        except Exception as exc:
            failures.append(f"{rel}: {type(exc).__name__}: {exc}")

    print(f"social metadata: scanned={len(files)} changed={counts['changed']} unchanged={counts['unchanged']} skipped={counts['skipped:no-head']} mode={'check' if args.check else 'write'}")
    print("sections: " + ", ".join(f"{k[8:]}={v}" for k, v in sorted(counts.items()) if k.startswith("section:")))
    if failures:
        print(f"FAILURES: {len(failures)}")
        for failure in failures[:50]:
            print(" - " + failure)
        return 1
    print("PASS: every processed page has one complete, internally consistent social metadata set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
