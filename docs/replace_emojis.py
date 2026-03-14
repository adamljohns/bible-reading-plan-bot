#!/usr/bin/env python3
"""Replace all emojis with shield icons or brand SVGs across all HTML files."""
import os
import re
import sys

DOCS_DIR = '/Users/adamjohns/bible-reading-plan-bot/docs'

def shield(name, size=20):
    return f'<img src="assets/icons/shield-{name}.png" class="site-icon" alt="{name}" width="{size}" height="{size}">'

def brand(name, size=20):
    return f'<img src="assets/icons/brand-{name}.svg" class="site-icon" alt="{name}" width="{size}" height="{size}">'

# Map emoji (with optional variation selectors) to shield icon name
EMOJI_MAP = {
    '🏠': 'anchor',
    '🏛️': 'anchor',
    '🏛': 'anchor',
    '📖': 'bible',
    '📗': 'bible',
    '⚓': 'anchor',
    '⚓️': 'anchor',
    '📅': 'calendar',
    '🗓️': 'calendar',
    '🗓': 'calendar',
    '📆': 'calendar',
    '👤': 'leader',
    '👨': 'leader',
    '👩': 'leader',
    '🎯': 'target',
    '❤️': 'uniting',
    '❤': 'uniting',
    '💕': 'uniting',
    '💛': 'uniting',
    '✝️': 'cross',
    '✝': 'cross',
    '✞': 'cross',
    '✠': 'cross',
    '💪': 'fitness',
    '🧠': 'mentoring',
    '💰': 'finance',
    '💵': 'finance',
    '🏢': 'finance',
    '💼': 'finance',
    '💲': 'finance',
    '💳': 'finance',
    '🏦': 'finance',
    '📕': 'book',
    '📘': 'book',
    '📚': 'book',
    '📓': 'book',
    '⭐': 'star',
    '⭐️': 'star',
    '🌟': 'star',
    '🏅': 'star',
    '🏆': 'star',
    '🥇': 'star',
    '🥈': 'star',
    '🕊️': 'dove',
    '🕊': 'dove',
    '🌍': 'globe',
    '🌎': 'globe',
    '🌐': 'globe',
    '🤝': 'handshake',
    '⚙️': 'gear',
    '⚙': 'gear',
    '🔧': 'gear',
    '🛠': 'gear',
    '🛠️': 'gear',
    '👑': 'crown',
    '🚢': 'ship',
    '🔍': 'compass',
    '🔎': 'compass',
    '📡': 'comms',
    '📣': 'megaphone',
    '📢': 'megaphone',
    '💍': 'family',
    '💑': 'family',
    '🎓': 'book',
    # Additional emojis found in the files
    '📋': 'book',
    '📜': 'book',
    '📝': 'book',
    '🔒': 'gear',
    '🔐': 'gear',
    '🔓': 'gear',
    '🔗': 'handshake',
    '💡': 'star',
    '📸': 'compass',
    '📷': 'compass',
    '🖨': 'gear',
    '🖨️': 'gear',
    '🖥': 'gear',
    '🖥️': 'gear',
    '🔭': 'compass',
    '📊': 'finance',
    '📈': 'finance',
    '📌': 'target',
    '📍': 'target',
    '🚀': 'star',
    '🦅': 'star',
    '🔥': 'star',
    '🌱': 'dove',
    '🌿': 'dove',
    '🤸': 'fitness',
    '🏃': 'fitness',
    '🤖': 'gear',
    '📱': 'gear',
    '📵': 'gear',
    '🎨': 'star',
    '🌅': 'star',
    '🌄': 'star',
    '🌙': 'star',
    '🧸': 'family',
    '👗': 'family',
    '👧': 'family',
    '👦': 'family',
    '🛏': 'anchor',
    '🗑': 'gear',
    '🧺': 'gear',
    '🍽': 'gear',
    '🍽️': 'gear',
    '🧹': 'gear',
    '🏡': 'anchor',
    '🏥': 'cross',
    '📏': 'gear',
    '🥗': 'fitness',
    '😴': 'dove',
    '🧭': 'compass',
    '💬': 'comms',
    '🙏': 'cross',
    '🙌': 'cross',
    '📤': 'comms',
    '📥': 'comms',
    '📬': 'comms',
    '✉': 'comms',
    '✉️': 'comms',
    '🎁': 'star',
    '🎖': 'star',
    '🎖️': 'star',
    '🛡': 'anchor',
    '🛡️': 'anchor',
    '🌤': 'star',
    '🌤️': 'star',
    '🎵': 'star',
    '🎙': 'comms',
    '🎙️': 'comms',
    '🎧': 'comms',
    '📎': 'gear',
    '🔴': 'target',
    '🟡': 'target',
    '🧴': 'gear',
    '🌹': 'uniting',
    '✍': 'book',
    '✍️': 'book',
    '🛒': 'gear',
    '📦': 'gear',
    '✈': 'globe',
    '✈️': 'globe',
    '🦎': 'star',
    '💾': 'gear',
    '🔄': 'gear',
    '✅': 'star',
    '✕': 'cross',
    '✗': 'cross',
    '✓': 'star',
    '✦': 'star',
    '✨': 'star',
    '🎯': 'target',
}

# Emojis for mood/face - these are special (used in forms), skip or replace contextually
FACE_EMOJIS = {'😫', '😔', '😐', '😊', '🔥', '😢', '😕', '😄', '🥳'}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    filename = os.path.basename(filepath)
    
    # Skip verse files - they're simple scripture pages
    if filepath.startswith(os.path.join(DOCS_DIR, 'verse/')):
        return False
    
    # Don't replace emojis inside <script> tags or specific form contexts where face emojis are functional
    # We'll do a simple approach: replace all mapped emojis
    
    changes = 0
    
    # Sort by length descending to match longer sequences first (e.g., emoji + variation selector)
    sorted_emojis = sorted(EMOJI_MAP.keys(), key=len, reverse=True)
    
    for emoji in sorted_emojis:
        icon_name = EMOJI_MAP[emoji]
        replacement = shield(icon_name)
        
        if emoji in content:
            # Don't replace inside alt="" attributes or title="" attributes
            # Simple approach: just replace
            count = content.count(emoji)
            content = content.replace(emoji, replacement)
            if count > 0:
                changes += count
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {filename}: {changes} replacements")
        return True
    else:
        print(f"  ⏭️  {filename}: no emojis found")
        return False

def main():
    print("🔄 Replacing emojis with shield icons across all HTML files...\n")
    
    changed = 0
    total = 0
    
    for root, dirs, files in os.walk(DOCS_DIR):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fn in sorted(files):
            if fn.endswith('.html') and fn != 'preview.html':
                filepath = os.path.join(root, fn)
                total += 1
                if process_file(filepath):
                    changed += 1
    
    print(f"\n✅ Done! Modified {changed}/{total} files.")

if __name__ == '__main__':
    main()
