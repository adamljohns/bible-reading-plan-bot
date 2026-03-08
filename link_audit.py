#!/usr/bin/env python3
"""Link audit for docs/ HTML files"""

import os
import re
import urllib.request
import urllib.error

DOCS_DIR = os.path.expanduser('~/bible-reading-plan-bot/docs')
BASE_URL = 'https://usmcmin.org'

def get_internal_files():
    files = set()
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for f in filenames:
            path = os.path.join(root, f)
            rel = os.path.relpath(path, DOCS_DIR)
            files.add('/' + rel.replace(os.sep, '/'))
    return files

def check_internal_link(href, internal_files):
    """Returns (exists, path)"""
    # Normalize
    if href.startswith('/'):
        path = href.split('?')[0].split('#')[0]
    else:
        return None, href  # relative, skip complex resolution
    
    # Remove trailing slash
    if path.endswith('/'):
        path += 'index.html'
    
    return path in internal_files, path

def audit():
    internal_files = get_internal_files()
    
    broken_internal = []
    external_links = []
    
    html_files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.html')]
    
    for fname in sorted(html_files):
        fpath = os.path.join(DOCS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all href and src
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        srcs = re.findall(r'src=["\']([^"\']+)["\']', content)
        
        all_links = hrefs + srcs
        
        for href in all_links:
            # Skip anchors only, JS, mailto, tel
            if href.startswith('#') or href.startswith('javascript:') or \
               href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            if href.startswith('http://') or href.startswith('https://'):
                external_links.append((fname, href))
            elif href.startswith('/'):
                exists, path = check_internal_link(href, internal_files)
                if exists is False:
                    broken_internal.append((fname, href, path))
            # Relative paths - check against file location
            elif not href.startswith('data:'):
                # Treat as relative to docs/
                full_path = '/' + href.split('?')[0].split('#')[0]
                if full_path not in internal_files:
                    broken_internal.append((fname, href, '(relative: ' + full_path + ')'))
    
    print("=== LINK AUDIT REPORT ===\n")
    
    print(f"BROKEN INTERNAL LINKS ({len(broken_internal)}):")
    if broken_internal:
        for fname, href, path in broken_internal:
            print(f"  [{fname}] {href}")
    else:
        print("  None! ✅")
    
    print(f"\nEXTERNAL LINKS ({len(set(l[1] for l in external_links))}):")
    seen_ext = set()
    for fname, href in external_links:
        if href not in seen_ext:
            print(f"  {href}")
            seen_ext.add(href)
    
    print("\n=== END AUDIT ===")
    return broken_internal

broken = audit()
