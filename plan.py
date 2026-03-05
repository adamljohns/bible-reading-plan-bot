#!/usr/bin/env python3
"""
Bible Reading Plan Bot — MOOP's Five-Watch Daily Reading System
Generates daily Bible readings from the master schedule.
"""
import json, sys, os
from datetime import datetime, timedelta

SCHEDULE_PATH = os.path.join(os.path.dirname(__file__), "schedule.json")

def load_schedule():
    if os.path.exists(SCHEDULE_PATH):
        with open(SCHEDULE_PATH) as f:
            return json.load(f)
    return {}

def get_reading(date_str=None):
    """Get readings for a specific date."""
    schedule = load_schedule()
    
    if date_str is None:
        now = datetime.now()
        # Try multiple formats
        keys_to_try = [
            now.strftime("%B %d").replace(" 0", " "),  # "March 5"
            now.strftime("%B %-d") if os.name != 'nt' else now.strftime("%B %d"),
            now.strftime("%b %d").replace(" 0", " "),   # "Mar 5"
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
    
    watch_map = {
        'Wisdom': ('🌅', 'Morning Wisdom (0600)'),
        '1st': ('⚓', '1st Watch — Husband\'s Post (0700)'),
        '2nd': ('🛡️', '2nd Watch — Father\'s Charge (1100)'),
        '3rd': ('🏛️', '3rd Watch — Citizen\'s Stand (1500)'),
        'Peace': ('🌙', 'Evening Peace (2100)')
    }
    
    for key, (emoji, label) in watch_map.items():
        if key in readings:
            output.append(f"{emoji} {label}")
            output.append(f"   📖 {readings[key]}")
            output.append("")
    
    return "\n".join(output)

def list_all():
    """List all scheduled readings."""
    schedule = load_schedule()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    for month in months:
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
        print("Usage: plan.py [today|list|<date>]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "today":
        date, readings = get_reading()
        if date:
            print(format_reading(date, readings))
        else:
            print(f"No readings found for today ({datetime.now().strftime('%B %-d')})")
            print("Schedule may need to be extended. Check schedule.json.")
    
    elif cmd == "list":
        list_all()
    
    else:
        # Treat as date string
        date_str = " ".join(sys.argv[1:])
        date, readings = get_reading(date_str)
        if date:
            print(format_reading(date, readings))
        else:
            print(f"No readings found for '{date_str}'")
