#!/usr/bin/env python3
"""Build the three dictionary origin hubs from optional entry metadata."""
import argparse
import glob
import html
import json
import os
import re
from urllib.parse import urlparse
from dictionary_origin_schema import validate_origin_fields

WORD_ORIGIN_CATEGORIES = ("bible", "civil-war", "eponym", "civic", "americana", "trades")
MILITARY_AUTO_CATEGORIES = ("marine", "navy", "army")
MILITARY_SECTIONS = (*MILITARY_AUTO_CATEGORIES, "civil-war")
CATEGORY_LABELS = {"bible": "Bible", "marine": "Marine Corps", "navy": "Navy", "army": "Army", "civil-war": "Civil War", "eponym": "Eponyms", "civic": "Civic Life", "americana": "Americana", "trades": "Trades", "weaponized": "Weaponized Words"}
HUB_SPECS = {
    "word-origins": ("Word Origins", "The histories carried in the words we use."),
    "military-language": ("Military Language", "Words formed in service, conflict, and command."),
    "weaponized-words": ("Weaponized Words", "Words whose meanings are bent into instruments of confusion or accusation."),
}
# Live entries hand-built before batch JSON existed; they can be tagged only
# through the overlay file and take their display word from the live page.
LEGACY_SLUGS = ("tolerance", "equity", "equality", "diversity", "inclusion", "gaslighting", "woke",
                "privilege", "justice", "compassion", "gender", "identity", "culture-war")
OVERLAY_FIELDS = {"origin_category", "origin_label", "origin_sources", "origin_crosslist",
                  "corruption_summary", "etymology"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def legacy_word(slug, dict_dir):
    path = os.path.join(dict_dir, f"{slug}.html")
    with open(path, encoding="utf-8") as stream:
        match = re.search(r"<h1[^>]*>(.*?)</h1>", stream.read(), re.DOTALL)
    word = re.sub(r"<[^>]+>", "", match.group(1)).strip() if match else ""
    return word or slug.replace("-", " ").title()


def apply_overlay(records, overlay_path, dict_dir):
    """Merge slug-keyed origin tags onto batch records and the legacy entries."""
    if not overlay_path or not os.path.exists(overlay_path):
        return records
    with open(overlay_path, encoding="utf-8") as stream:
        overlay = json.load(stream)
    if not isinstance(overlay, dict):
        raise ValueError(f"{overlay_path}: root must be an object keyed by slug")
    for slug, tags in overlay.items():
        if not isinstance(tags, dict):
            raise ValueError(f"{overlay_path}/{slug}: value must be an object")
        extra = sorted(set(tags) - OVERLAY_FIELDS)
        if extra:
            raise ValueError(f"{overlay_path}/{slug}: unsupported overlay fields {extra}")
        if slug in records:
            record = {**records[slug], **tags}
        elif slug in LEGACY_SLUGS:
            record = {"slug": slug, "word": legacy_word(slug, dict_dir), **tags}
        else:
            raise ValueError(f"{overlay_path}/{slug}: unknown slug (not in a batch or the legacy list)")
        errors = validate_origin_fields(record)
        if errors:
            raise ValueError(f"{overlay_path}/{slug}: " + "; ".join(errors))
        records[slug] = record
    return records


def load_entries(patterns, overlay_path=None, dict_dir=os.path.join(ROOT, "docs", "dictionary")):
    entries = {}
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            if os.path.basename(path).startswith("_"):
                continue
            with open(path, encoding="utf-8") as stream:
                records = json.load(stream)
            if not isinstance(records, list):
                raise ValueError(f"{path}: batch root must be an array")
            for record in records:
                errors = validate_origin_fields(record)
                if errors:
                    slug = record.get("slug", "(missing)")
                    raise ValueError(f"{path}/{slug}: " + "; ".join(errors))
                entries[record["slug"]] = record
    entries = apply_overlay(entries, overlay_path, dict_dir)
    return [r for r in entries.values() if r.get("origin_category") or r.get("origin_crosslist")]


def in_hub(entry, hub):
    category = entry.get("origin_category")
    explicit = hub in entry.get("origin_crosslist", [])
    if hub == "word-origins":
        return category in WORD_ORIGIN_CATEGORIES or explicit
    if hub == "military-language":
        return category in MILITARY_AUTO_CATEGORIES or explicit
    return category == "weaponized" or explicit


def source_links(entry):
    links = []
    for number, url in enumerate(entry.get("origin_sources", []), 1):
        host = urlparse(url).netloc.removeprefix("www.")
        links.append(f'<a href="{html.escape(url, quote=True)}" rel="noopener">{html.escape(host or f"Source {number}")}</a>')
    return " · ".join(links) or "—"


def row(entry, weaponized=False):
    label = entry.get("origin_label")
    badge = f'<span class="badge {html.escape(label)}">{html.escape(label.replace("-", " ").title())}</span>' if label else ""
    summary = entry.get("corruption_summary") if weaponized else entry.get("etymology", "")
    return (f'<tr data-origin-category="{html.escape(entry.get("origin_category", ""))}">'
            f'<th scope="row"><a href="{html.escape(entry["slug"])}.html">{html.escape(entry["word"])}</a>{badge}</th>'
            f'<td>{summary}</td><td>{source_links(entry)}</td></tr>')


def empty_state():
    return '<p class="empty">No entries have been assigned to this hub yet.</p>'


def sections(hub, entries):
    selected = sorted((e for e in entries if in_hub(e, hub)), key=lambda e: e["word"].casefold())
    if hub == "weaponized-words":
        body = "".join(row(e, True) for e in selected)
        return f'<section><h2>Words and their corruptions</h2><table><thead><tr><th>Word</th><th>Corruption summary</th><th>Sources</th></tr></thead><tbody>{body}</tbody></table></section>' if body else empty_state()
    categories = MILITARY_SECTIONS if hub == "military-language" else WORD_ORIGIN_CATEGORIES
    chunks = []
    for category in categories:
        group = [e for e in selected if e.get("origin_category") == category]
        body = "".join(row(e) for e in group)
        if not body:
            body = '<tr><td colspan="3" class="empty">No entries yet.</td></tr>'
        chunks.append(f'<section id="{category}"><h2>{CATEGORY_LABELS[category]}</h2><table><thead><tr><th>Word</th><th>Origin</th><th>Sources</th></tr></thead><tbody>{body}</tbody></table></section>')
    other = [e for e in selected if e.get("origin_category") not in categories]
    if other:
        body = "".join(row(e) for e in other)
        chunks.append(f'<section><h2>Cross-listed</h2><table><thead><tr><th>Word</th><th>Origin</th><th>Sources</th></tr></thead><tbody>{body}</tbody></table></section>')
    return "".join(chunks) or empty_state()


def render(hub, entries):
    title, intro = HUB_SPECS[hub]
    content = sections(hub, entries)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://usmcmin.org/dictionary/{hub}.html"><title>{title} — The MOOP Dictionary</title>
<style>:root{{--bg:#000;--card:#111;--gold:#D4AF37;--text:#fff;--muted:#aaa;--border:#333}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 Inter,system-ui,sans-serif}}main{{max-width:1000px;margin:auto;padding:32px 20px 64px}}nav{{padding:14px 20px;border-bottom:1px solid var(--border);text-align:center}}a{{color:var(--gold)}}h1,h2{{font-family:Georgia,serif;color:var(--gold)}}.lead,.empty{{color:var(--muted)}}section{{margin:28px 0}}table{{width:100%;border-collapse:collapse;background:var(--card)}}th,td{{padding:12px;text-align:left;vertical-align:top;border:1px solid var(--border)}}thead th{{color:var(--gold)}}tbody th{{width:24%}}.badge{{display:inline-block;margin-left:8px;padding:1px 7px;border:1px solid var(--border);border-radius:12px;color:var(--muted);font-size:.72rem;font-weight:400}}@media(max-width:640px){{table,thead,tbody,tr,th,td{{display:block}}thead{{position:absolute;left:-9999px}}tr{{border:1px solid var(--border);margin-bottom:12px}}th,td{{border:0;border-bottom:1px solid var(--border)}}}}</style></head>
<body><nav><a href="index.html">Dictionary A–Z</a> · <a href="word-origins.html">Word Origins</a> · <a href="military-language.html">Military Language</a> · <a href="weaponized-words.html">Weaponized Words</a></nav>
<main><h1>{title}</h1><p class="lead">{intro}</p>{content}</main><script defer src="../assets/js/moop-tools.js"></script></body></html>'''


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-glob", action="append", dest="patterns", default=[])
    parser.add_argument("--output-dir", default=os.path.join(ROOT, "docs", "dictionary"))
    parser.add_argument("--origin-tags", default=os.path.join(ROOT, "data", "dictionary-origin-tags.json"))
    parser.add_argument("--dict-dir", default=os.path.join(ROOT, "docs", "dictionary"))
    args = parser.parse_args(argv)
    patterns = args.patterns or [os.path.join(ROOT, "data", "dictionary-batches", "batch-*.json")]
    entries = load_entries(patterns, args.origin_tags, args.dict_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    for hub in HUB_SPECS:
        path = os.path.join(args.output_dir, f"{hub}.html")
        with open(path, "w", encoding="utf-8") as stream:
            stream.write(render(hub, entries))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
