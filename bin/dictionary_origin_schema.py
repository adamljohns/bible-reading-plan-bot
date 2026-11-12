#!/usr/bin/env python3
"""Validation constants and checks for optional Word Origins metadata."""
import re
from urllib.parse import urlparse

ORIGIN_CATEGORIES = {"bible", "marine", "navy", "army", "civil-war", "eponym", "civic", "americana", "trades", "weaponized"}
ORIGIN_LABELS = {"attested", "disputed", "folk-myth"}
ORIGIN_HUBS = {"word-origins", "military-language", "weaponized-words"}


def _visible_text(value):
    return re.sub(r"<[^>]+>", "", value or "").strip()


def validate_origin_fields(entry):
    """Return human-readable errors; old entries with no origin fields pass."""
    errors = []
    category = entry.get("origin_category")
    if category is not None and category not in ORIGIN_CATEGORIES:
        errors.append(f"origin_category must be one of {sorted(ORIGIN_CATEGORIES)}")
    label = entry.get("origin_label")
    if label is not None and label not in ORIGIN_LABELS:
        errors.append(f"origin_label must be one of {sorted(ORIGIN_LABELS)}")
    sources = entry.get("origin_sources")
    if sources is not None:
        if not isinstance(sources, list):
            errors.append("origin_sources must be an array of URLs")
        else:
            for source in sources:
                parsed = urlparse(source) if isinstance(source, str) else None
                if not parsed or parsed.scheme not in ("http", "https") or not parsed.netloc:
                    errors.append(f"origin_sources contains an invalid URL: {source!r}")
    crosslist = entry.get("origin_crosslist")
    if crosslist is not None:
        if not isinstance(crosslist, list) or any(not isinstance(x, str) for x in crosslist):
            errors.append("origin_crosslist must be an array of hub keys")
        else:
            unknown = sorted(set(crosslist) - ORIGIN_HUBS)
            if unknown:
                errors.append(f"origin_crosslist has unknown hub keys: {unknown}")
            if len(crosslist) != len(set(crosslist)):
                errors.append("origin_crosslist must not contain duplicates")
    if (category == "weaponized" or "weaponized-words" in (crosslist or [])) and not _visible_text(entry.get("corruption_summary")):
        errors.append("weaponized entries require a non-empty corruption_summary")
    return errors
