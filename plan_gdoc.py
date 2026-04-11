#!/usr/bin/env python3
"""
Bible Reading Plan Bot — MOOP's Five-Watch Daily Reading System
Reads directly from the master Google Doc instead of schedule.json.
"""
import re, sys, os, subprocess
from datetime import datetime

# Google Doc ID for the master plan
GDOC_ID = "15jNBnR-f3FgoLYXCFcdTWAxrejlFHzvCA9IsfhSs1Bc"
GDOC_ACCOUNT = "adam.l.johns@gmail.com"

# Month name → number for date normalization
MONTHS = {
    'JANUARY': 'January', 'FEBRUARY': 'February', 'MARCH': 'March',
    'APRIL': 'April', 'MAY': 'May', 'JUNE': 'June',
    'JULY': 'July', 'AUGUST': 'August', 'SEPTEMBER': 'September',
    'OCTOBER': 'October', 'NOVEMBER': 'November', 'DECEMBER': 'December'
}

# Month ordering for sorting
MONTH_ORDER = list(MONTHS.values())

# Regex patterns
DATE_PATTERN = re.compile(
    r'^(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|'
    r'SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+(\d{1,2})\s*$'
)

# Watch line: optional "Lu " prefix, then key, optional " Watch", then ":"
WATCH_PATTERN = re.compile(
    r'^(?:Lu\s+)?(Wisdom|1st(?:\s+Watch)?|2nd(?:\s+Watch)?|3rd(?:\s+Watch)?|Peace)\s*:\s*(.*)',
    re.IGNORECASE
)

# Map raw watch key → canonical key
WATCH_KEY_MAP = {
    'wisdom': 'Wisdom',
    '1st': '1st',
    '1st watch': '1st',
    '2nd': '2nd',
    '2nd watch': '2nd',
    '3rd': '3rd',
    '3rd watch': '3rd',
    'peace': 'Peace',
}

SEPARATOR_PATTERN = re.compile(r'^[⸻—\-]{2,}\s*$')


def fetch_gdoc_text():
    """Fetch the Google Doc as plain text via gog CLI."""
    result = subprocess.run(
        ['gog', 'docs', 'cat', GDOC_ID, '--account', GDOC_ACCOUNT],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"gog docs cat failed: {result.stderr.strip()}")
    return result.stdout


def clean_passage(text):
    """
    Clean up a passage reference:
    - Strip parenthetical notes like (covenant faithfulness — wedding themes)
    - Normalize em dash — to -
    - Strip trailing separator characters (⸻ —)
    - Collapse whitespace
    """
    # Remove complete parenthetical notes: anything from ( to matching )
    cleaned = re.sub(r'\s*\([^)]*\)', '', text)
    # Remove trailing incomplete parenthetical (no closing paren on this fragment)
    cleaned = re.sub(r'\s*\([^)]*$', '', cleaned)
    # Normalize em dash — to hyphen (for display consistency)
    # Keep the en dash – as-is (used in verse ranges like 1–18)
    cleaned = cleaned.replace('\u2014', '-')  # em dash → hyphen
    # Strip trailing horizontal rule / separator chars (⸻ U+2E3B, — U+2014, - hyphens)
    cleaned = re.sub(r'[\u2E3B\u2014\-\s]+$', '', cleaned)
    # Collapse whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned.strip()


def parse_gdoc(text):
    """
    Parse the Google Doc text into a schedule dict:
    { "April 10": { "Wisdom": "Proverbs 10", "1st": "Ruth 3", ... }, ... }
    """
    lines = text.splitlines()
    schedule = {}

    current_date = None
    current_watch = None
    current_ref_parts = []
    in_paren_note = False  # True when inside a multi-line parenthetical note

    def flush_watch():
        nonlocal current_watch, current_ref_parts, in_paren_note
        if current_date and current_watch and current_ref_parts:
            raw = ' '.join(current_ref_parts)
            ref = clean_passage(raw)
            if ref:
                schedule.setdefault(current_date, {})[current_watch] = ref
        current_watch = None
        current_ref_parts = []
        in_paren_note = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and separators
        if not stripped or SEPARATOR_PATTERN.match(stripped):
            continue

        # Check for date header (e.g., "APRIL 10")
        date_match = DATE_PATTERN.match(stripped)
        if date_match:
            flush_watch()
            month_upper = date_match.group(1)
            day = int(date_match.group(2))
            current_date = f"{MONTHS[month_upper]} {day}"
            continue

        # Check for watch line (e.g., "Wisdom: Proverbs 10" or "1st Watch: Ruth 3")
        watch_match = WATCH_PATTERN.match(stripped)
        if watch_match:
            flush_watch()
            raw_key = watch_match.group(1).lower()
            canonical_key = WATCH_KEY_MAP.get(raw_key)
            if canonical_key and current_date:
                current_watch = canonical_key
                ref_text = watch_match.group(2).strip()
                current_ref_parts = [ref_text] if ref_text else []
                # Check if this line itself starts a multi-line note
                # e.g. "Wisdom: Job 42 (Job" — the paren isn't closed yet
                combined = ref_text
                open_count = combined.count('(')
                close_count = combined.count(')')
                if open_count > close_count:
                    in_paren_note = True
            continue

        # If we're in the middle of a watch reference, handle continuations
        if current_watch and current_date:
            # Skip emoji/header lines
            if stripped.startswith('📅') or stripped.startswith('✅') or stripped.startswith('🧭'):
                continue

            # Handle multi-line parenthetical tracking
            if in_paren_note:
                # We're inside a note — check if it closes here
                if stripped.endswith(')'):
                    in_paren_note = False
                # Either way, skip this note line (don't append to ref)
                continue

            if stripped.startswith('('):
                # Starting a note on its own line
                if not stripped.endswith(')'):
                    in_paren_note = True
                # Skip note lines entirely
                continue

            # Otherwise treat as continuation of current reference
            # (e.g., a verse ref split across lines: "1 Thessalonians 3:11–\n13")
            current_ref_parts.append(stripped)
            continue

    # Flush any remaining watch
    flush_watch()

    return schedule


_schedule_cache = None


def load_schedule():
    """Load and cache the schedule from Google Doc."""
    global _schedule_cache
    if _schedule_cache is None:
        text = fetch_gdoc_text()
        _schedule_cache = parse_gdoc(text)
    return _schedule_cache


def get_reading(date_str=None):
    """Get readings for a specific date."""
    schedule = load_schedule()

    if date_str is None:
        now = datetime.now()
        keys_to_try = [
            now.strftime("%B %-d"),   # "April 11"
            now.strftime("%B %d").replace(" 0", " "),  # "April  1" → "April 1"
        ]
    else:
        keys_to_try = [date_str]

    for key in keys_to_try:
        if key in schedule:
            return key, schedule[key]

    return None, None


def format_reading(date, readings):
    """Format readings for display."""
    if not readings:
        return f"No readings found for {date}"

    output = [f"📅 {date} — Daily Bible Reading Plan\n"]

    watch_map = [
        ('Wisdom', '🌅', 'Morning Wisdom (0600)'),
        ('1st',    '⚓', "1st Watch — Husband's Post (0700)"),
        ('2nd',    '🛡️', "2nd Watch — Father's Charge (1100)"),
        ('3rd',    '🏛️', "3rd Watch — Citizen's Stand (1500)"),
        ('Peace',  '🌙', 'Evening Peace (2100)'),
    ]

    for key, emoji, label in watch_map:
        if key in readings:
            output.append(f"{emoji} {label}")
            output.append(f"   📖 {readings[key]}")
            output.append("")

    return "\n".join(output)


def list_all():
    """List all scheduled readings."""
    schedule = load_schedule()

    for month in MONTH_ORDER:
        month_entries = {k: v for k, v in schedule.items() if k.startswith(month)}
        if month_entries:
            print(f"\n=== {month} ({len(month_entries)} days) ===")
            for date in sorted(month_entries.keys(),
                               key=lambda d: int(d.split()[-1])):
                readings = month_entries[date]
                watches = len(readings)
                first_reading = list(readings.values())[0] if readings else "?"
                print(f"  {date}: {watches} watches — starts with {first_reading}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: plan_gdoc.py [today|list|<date>]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "today":
        date, readings = get_reading()
        if date:
            print(format_reading(date, readings))
        else:
            print(f"No readings found for today ({datetime.now().strftime('%B %-d')})")
            print("Check Google Doc: https://docs.google.com/document/d/" + GDOC_ID)

    elif cmd == "list":
        list_all()

    else:
        # Treat as date string (e.g., "April 11")
        date_str = " ".join(sys.argv[1:])
        date, readings = get_reading(date_str)
        if date:
            print(format_reading(date, readings))
        else:
            print(f"No readings found for '{date_str}'")
