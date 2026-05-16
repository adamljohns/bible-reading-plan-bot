#!/usr/bin/env python3
"""Rebuild the MOOP Dictionary index page from all word HTML files.

Usage:
    python3 rebuild-dictionary.py

Scans docs/dictionary/*.html (excluding index.html and template.html),
extracts each word's <h1> and .pos element, groups by first letter,
then regenerates docs/dictionary/index.html from scratch.
"""

import os
import re
import subprocess
import sys
from collections import defaultdict

DICT_DIR = os.path.join(os.path.dirname(__file__), 'docs', 'dictionary')
INDEX_FILE = os.path.join(DICT_DIR, 'index.html')


def extract_word_info(filepath):
    """Extract word name and part of speech from a dictionary HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Word from <h1>
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    word = h1_m.group(1).strip() if h1_m else ''
    word = re.sub(r'<[^>]+>', '', word).strip()
    if not word:
        word = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()

    # Part of speech from class="pos"
    pos_m = re.search(r'class=["\']pos["\'][^>]*>(.*?)</[^>]+>', content, re.DOTALL)
    pos = pos_m.group(1).strip() if pos_m else ''
    pos = re.sub(r'<[^>]+>', '', pos).strip()

    return word, pos


def render_letter_section(letter, entries):
    """Render one <div class="category"> block for a letter."""
    cards = '\n'.join(
        f'                        <a href="{e["file"]}" class="word-card">'
        f'<div class="word">{e["word"]}</div>'
        f'<div class="pos">{e["pos"]}</div></a>'
        for e in entries
    )
    return (
        f'                <div class="category">\n'
        f'                    <h2>{letter} <span class="count-badge">{len(entries)}</span></h2>\n'
        f'                    <div class="word-grid">\n'
        f'{cards}\n'
        f'                    </div>\n'
        f'                </div>'
    )


def render_range(letters, by_letter):
    return '\n'.join(
        render_letter_section(l, by_letter[l])
        for l in letters
        if by_letter.get(l)
    )


def build_index(words, by_letter, total):
    """Generate the complete index.html string."""

    AD = render_range(['A', 'B', 'C', 'D'], by_letter)
    EI = render_range(['E', 'F', 'G', 'H', 'I'], by_letter)
    JN = render_range(['J', 'K', 'L', 'M', 'N'], by_letter)
    OS = render_range(['O', 'P', 'Q', 'R', 'S'], by_letter)
    TZ = render_range(['T', 'U', 'V', 'W', 'X', 'Y', 'Z'], by_letter)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The MOOP Dictionary of the English Language</title>
    <!-- Open Graph / Twitter / SEO -->
    <meta name="description" content="The MOOP Dictionary — 4000+ entries with biblical definition, Webster 1828, Greek/Hebrew roots, and modern corruption analysis. Doctrinal anchors, the most corrupted words of our age, and generational dialect decoded.">
    <meta property="og:title" content="The MOOP Dictionary of the English Language">
    <meta property="og:description" content="Biblical definition, Webster 1828, Greek/Hebrew roots, and modern corruption analysis. Doctrinal anchors, most corrupted words, generational decoded — 4000+ entries.">
    <meta property="og:image" content="https://usmcmin.org/assets/icons/icon-512.png">
    <meta property="og:url" content="https://usmcmin.org/dictionary/">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="The MOOP Dictionary">
    <meta name="twitter:image" content="https://usmcmin.org/assets/icons/icon-512.png">
    <link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../assets/icons/favicon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../assets/icons/favicon-16.png">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1,h2,h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center; padding:14px 20px; border-bottom:1px solid var(--border); background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); position:sticky; top:0; z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.85rem; font-weight:500; padding:5px 12px; border-radius:20px; border:1px solid transparent; transition:all 0.2s; white-space:nowrap; display:inline-flex; align-items:center; gap:4px; }}
        nav a:hover {{ color:var(--gold); border-color:var(--border); }}
        nav a:link,nav a:visited,nav a:active {{ color:var(--gray) !important; text-decoration:none !important; }}
        nav a.active {{ color:var(--gold) !important; border-color:var(--gold); }}
        .site-icon {{ vertical-align:middle; opacity:0.8; }}
        .bte-theme-toggle {{
            justify-content: center; margin: 8px auto 0; width: fit-content;
            display: flex; align-items: center; gap: 0;
            background: rgba(30,30,30,0.85); border: 1px solid #333;
            border-radius: 20px; padding: 3px 6px; cursor: pointer;
            font-size: 0.7rem; user-select: none; backdrop-filter: blur(6px);
            transition: all 0.3s;
        }}
        .bte-theme-toggle:hover {{ border-color: #D4AF37; }}
        .bte-theme-toggle .toggle-icon {{ width: 18px; text-align: center; line-height: 1; }}
        .bte-theme-toggle .toggle-track {{
            width: 28px; height: 14px; background: #444; border-radius: 7px;
            position: relative; margin: 0 4px; transition: background 0.3s;
        }}
        .bte-theme-toggle .toggle-knob {{
            width: 10px; height: 10px; background: #D4AF37; border-radius: 50%;
            position: absolute; top: 2px; left: 2px; transition: left 0.3s;
        }}
        body.light-mode .bte-theme-toggle {{ background: rgba(240,238,233,0.9); border-color: #ccc; }}
        body.light-mode .bte-theme-toggle .toggle-track {{ background: #bbb; }}
        body.light-mode .bte-theme-toggle .toggle-knob {{ left: 16px; }}
        .bte-theme-toggle .moon-icon {{ color: #888; }}
        .bte-theme-toggle .sun-icon {{ color: #888; }}
        body.light-mode .bte-theme-toggle .sun-icon {{ color: #D4AF37; }}
        body:not(.light-mode) .bte-theme-toggle .moon-icon {{ color: #D4AF37; }}
        .container {{ max-width:900px; margin:0 auto; padding:20px; }}
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:40px; }}
        .hero h1 {{ font-size:2.8rem; color:var(--gold-light); margin-bottom:10px; }}
        .hero p {{ color:var(--gray); max-width:600px; margin:10px auto; }}
        .subtitle {{ font-size:1.1rem; color:var(--gray); font-style:italic; }}
        .category {{ margin:35px 0; }}
        .category h2 {{ color:var(--gold); font-size:1.3rem; margin-bottom:15px; border-bottom:1px solid var(--border); padding-bottom:8px; }}
        .word-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(160px, 1fr)); gap:10px; }}
        .word-card {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:12px 16px; text-decoration:none; color:var(--white); transition:border-color 0.2s, color 0.2s; }}
        .word-card:hover {{ border-color:var(--gold); color:var(--gold-light); }}
        .word-card .word {{ font-family:'Playfair Display',serif; font-size:1rem; }}
        .word-card .pos {{ font-size:0.75rem; color:var(--gray); margin-top:2px; }}
        .count-badge {{ display:inline-block; background:var(--gold); color:#000; font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:10px; margin-left:8px; vertical-align:middle; }}
        footer {{ text-align:center; padding:28px 20px; border-top:1px solid var(--border); margin-top:40px; color:var(--gray); font-size:0.88rem; }}
        footer a {{ color:var(--gray); text-decoration:none; }}
        footer a:hover {{ color:var(--gold); }}
        .cross-divider {{ margin-bottom:10px; }}
        body.light-mode {{ --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(245,243,239,0.97); }}
        body.light-mode .word-card {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode footer {{ border-top-color:#d4d0c8; }}
        a, a:link, a:visited {{ color: var(--gold, #D4AF37) !important; }}
        a:hover {{ color: var(--gold-light, #F4D470) !important; }}
        .search-wrap {{ max-width:500px; margin:0 auto 24px; position:relative; }}
        .search-wrap input {{ width:100%; padding:12px 18px 12px 42px; background:var(--card); border:1px solid var(--border); border-radius:50px; color:var(--white); font-size:0.95rem; outline:none; transition:border-color 0.2s; font-family:'Inter',sans-serif; }}
        .search-wrap input:focus {{ border-color:var(--gold); }}
        .search-wrap input::placeholder {{ color:#555; }}
        .search-icon {{ position:absolute; left:15px; top:50%; transform:translateY(-50%); color:var(--gray); pointer-events:none; }}
        .range-bar {{ display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:28px; }}
        .range-btn {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:8px 18px; color:var(--gray); font-size:0.88rem; font-family:'Inter',sans-serif; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:6px; }}
        .range-btn:hover {{ border-color:var(--gold); color:var(--gold); }}
        .range-btn.open {{ border-color:var(--gold); background:rgba(212,175,55,0.12); color:var(--gold); }}
        .range-btn .rarrow {{ display:inline-block; width:0; height:0; border-top:5px solid transparent; border-bottom:5px solid transparent; border-left:8px solid #D4AF37; transition:transform 0.25s; }}
        .range-btn.open .rarrow {{ transform:rotate(90deg); }}
        .range-panel {{ overflow:hidden; max-height:0; transition:max-height 0.35s ease; }}
        .range-panel.open {{ max-height:30000px; }}
        #searchResults {{ display:none; }}
        #searchResults.visible {{ display:block; }}
        /* Suggest a Word Form */
        .suggest-section {{
            max-width: 600px;
            margin: 50px auto 40px;
            padding: 32px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
        }}
        .suggest-section h2 {{ color: var(--gold-light); font-size: 1.5rem; margin-bottom: 8px; }}
        .suggest-section .suggest-sub {{ color: var(--gray); font-size: 0.9rem; margin-bottom: 24px; line-height: 1.6; }}
        .suggest-section label {{ display: block; color: var(--gray); font-size: 0.85rem; margin-bottom: 6px; font-weight: 500; }}
        .suggest-section input[type="text"],
        .suggest-section textarea {{
            width: 100%; background: #1a1a1a; border: 1px solid var(--border);
            border-radius: 8px; color: var(--white); font-family: 'Inter', sans-serif;
            font-size: 0.95rem; padding: 12px 16px; margin-bottom: 18px; outline: none;
            transition: border-color 0.2s; resize: vertical;
        }}
        .suggest-section input[type="text"]:focus,
        .suggest-section textarea:focus {{ border-color: var(--gold); }}
        .suggest-section input[type="text"]::placeholder,
        .suggest-section textarea::placeholder {{ color: #555; }}
        .suggest-section .btn-suggest {{
            background: var(--gold); color: #000; border: none; border-radius: 8px;
            padding: 12px 32px; font-size: 0.95rem; font-weight: 700;
            font-family: 'Inter', sans-serif; cursor: pointer; transition: background 0.2s;
        }}
        .suggest-section .btn-suggest:hover {{ background: var(--gold-light); }}
        body.light-mode .suggest-section {{ background: #fff; border-color: #d4d0c8; }}
        body.light-mode .suggest-section input[type="text"],
        body.light-mode .suggest-section textarea {{ background: #f5f3ef; border-color: #d4d0c8; color: #1a1a1a; }}
        @media (min-width: 1025px) {{ .container {{ max-width: 1100px; }} }}
        .names-callout {{ text-align:center; margin:0 auto 24px; }}
        .names-callout a {{ display:inline-flex; align-items:center; gap:8px; padding:10px 22px; background:rgba(212,175,55,0.08); border:1px solid var(--gold); border-radius:30px; font-size:0.95rem; font-weight:500; color:var(--gold) !important; text-decoration:none; transition:all 0.2s; }}
        .names-callout a:hover {{ background:rgba(212,175,55,0.18); color:var(--gold-light) !important; }}
        .names-callout img {{ width:20px; height:20px; opacity:0.9; }}
        /* Word of the Day */
        .wotd-widget {{ background:linear-gradient(135deg,rgba(212,175,55,0.08) 0%,rgba(212,175,55,0.02) 100%); border:1px solid rgba(212,175,55,0.2); border-radius:12px; padding:20px 24px; margin:20px 0; text-align:center; }}
        .wotd-widget h4 {{ color:var(--gold); font-family:'Playfair Display',serif; font-size:1rem; margin-bottom:10px; display:inline-flex; align-items:center; gap:8px; }}
        .wotd-word {{ font-family:'Playfair Display',serif; font-size:1.8rem; color:var(--white); margin-bottom:4px; }}
        .wotd-word a {{ color:var(--white); text-decoration:none; }}
        .wotd-word a:hover {{ color:var(--gold); }}
        .wotd-pos {{ color:var(--gray); font-size:0.82rem; font-style:italic; margin-bottom:8px; }}
        .wotd-def {{ color:var(--gray); font-size:0.92rem; line-height:1.6; max-width:600px; margin:0 auto; }}
        body.light-mode .wotd-widget {{ background:linear-gradient(135deg,rgba(212,175,55,0.06) 0%,rgba(212,175,55,0.02) 100%); }}
        /* Expressly Prohibited (deep crimson) — Lev 18-20, Deut 18, Gal 5, Rev 21 prohibitions */
        .forbidden-section {{ background:rgba(139,21,21,0.06); border:1px solid rgba(139,21,21,0.22); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .forbidden-section h3 {{ color:#8b1515; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .forbidden-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .forbidden-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px; }}
        .forbidden-card {{ background:rgba(139,21,21,0.08); border:1px solid rgba(139,21,21,0.18); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; }}
        .forbidden-card:hover {{ border-color:#8b1515; background:rgba(139,21,21,0.16); }}
        .forbidden-card .pword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .forbidden-card .ptag {{ color:#8b1515; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.5px; }}
        body.light-mode .forbidden-section {{ background:rgba(139,21,21,0.04); }}
        body.light-mode .forbidden-card .pword {{ color:#1a1a1a; }}

        /* Biblical Order (scarlet) — patriarchy / headship / NXR vocabulary */
        .order-section {{ background:rgba(184,80,66,0.05); border:1px solid rgba(184,80,66,0.20); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .order-section h3 {{ color:#b85042; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .order-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .order-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px; }}
        .order-card {{ background:rgba(184,80,66,0.07); border:1px solid rgba(184,80,66,0.15); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; }}
        .order-card:hover {{ border-color:#b85042; background:rgba(184,80,66,0.14); }}
        .order-card .oword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .order-card .otag {{ color:#b85042; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.5px; }}
        body.light-mode .order-section {{ background:rgba(184,80,66,0.04); }}
        body.light-mode .order-card .oword {{ color:#1a1a1a; }}

        /* Most Corrupted Words */
        .corrupted-section {{ background:rgba(244,67,54,0.04); border:1px solid rgba(244,67,54,0.15); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .corrupted-section h3 {{ color:#f44336; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .corrupted-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .corrupted-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:8px; }}
        .corrupted-card {{ background:rgba(244,67,54,0.06); border:1px solid rgba(244,67,54,0.12); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; }}
        .corrupted-card:hover {{ border-color:#f44336; background:rgba(244,67,54,0.12); }}
        .corrupted-card .cword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .corrupted-card .ctag {{ color:#f44336; font-size:0.65rem; text-transform:uppercase; letter-spacing:0.5px; }}
        body.light-mode .corrupted-section {{ background:rgba(244,67,54,0.03); }}
        body.light-mode .corrupted-card .cword {{ color:#1a1a1a; }}
        /* Gen-Z Decoded section (pink) */
        .genz-section {{ background:rgba(236,72,153,0.04); border:1px solid rgba(236,72,153,0.18); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .genz-section h3 {{ color:#EC4899; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .genz-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .genz-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }}
        .genz-card {{ background:rgba(236,72,153,0.06); border:1px solid rgba(236,72,153,0.15); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; display:block; }}
        .genz-card:hover {{ border-color:#EC4899; background:rgba(236,72,153,0.13); }}
        .genz-card .gzword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .genz-card .gzverdict {{ font-size:0.62rem; text-transform:uppercase; letter-spacing:0.6px; margin-top:3px; font-weight:700; }}
        .gzv-green {{ color:#10B981; }}
        .gzv-yellow {{ color:#F59E0B; }}
        .gzv-orange {{ color:#F97316; }}
        .gzv-red {{ color:#EF4444; }}
        body.light-mode .genz-section {{ background:rgba(236,72,153,0.03); }}
        body.light-mode .genz-card .gzword {{ color:#1a1a1a; }}
        /* Millennial Decoded section (teal) */
        .mill-section {{ background:rgba(20,184,166,0.04); border:1px solid rgba(20,184,166,0.18); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .mill-section h3 {{ color:#14B8A6; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .mill-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .mill-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }}
        .mill-card {{ background:rgba(20,184,166,0.06); border:1px solid rgba(20,184,166,0.15); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; display:block; }}
        .mill-card:hover {{ border-color:#14B8A6; background:rgba(20,184,166,0.13); }}
        .mill-card .mword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .mill-card .mverdict {{ font-size:0.62rem; text-transform:uppercase; letter-spacing:0.6px; margin-top:3px; font-weight:700; }}
        body.light-mode .mill-section {{ background:rgba(20,184,166,0.03); }}
        body.light-mode .mill-card .mword {{ color:#1a1a1a; }}
        /* Gen X Decoded section (lime) */
        .genx-section {{ background:rgba(132,204,22,0.04); border:1px solid rgba(132,204,22,0.20); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .genx-section h3 {{ color:#84CC16; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .genx-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .genx-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }}
        .genx-card {{ background:rgba(132,204,22,0.06); border:1px solid rgba(132,204,22,0.18); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; display:block; }}
        .genx-card:hover {{ border-color:#84CC16; background:rgba(132,204,22,0.13); }}
        .genx-card .xword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .genx-card .xverdict {{ font-size:0.62rem; text-transform:uppercase; letter-spacing:0.6px; margin-top:3px; font-weight:700; }}
        body.light-mode .genx-section {{ background:rgba(132,204,22,0.03); }}
        body.light-mode .genx-card .xword {{ color:#1a1a1a; }}
        /* Boomer Decoded section (amber) */
        .boomer-section {{ background:rgba(217,119,6,0.04); border:1px solid rgba(217,119,6,0.20); border-radius:12px; padding:20px 24px; margin:30px 0; }}
        .boomer-section h3 {{ color:#D97706; font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .boomer-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .boomer-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }}
        .boomer-card {{ background:rgba(217,119,6,0.06); border:1px solid rgba(217,119,6,0.18); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; display:block; }}
        .boomer-card:hover {{ border-color:#D97706; background:rgba(217,119,6,0.13); }}
        .boomer-card .bword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .boomer-card .bverdict {{ font-size:0.62rem; text-transform:uppercase; letter-spacing:0.6px; margin-top:3px; font-weight:700; }}
        body.light-mode .boomer-section {{ background:rgba(217,119,6,0.03); }}
        body.light-mode .boomer-card .bword {{ color:#1a1a1a; }}
        /* Featured Entries (Doctrinal Anchors) */
        .featured-section {{ background:rgba(212,175,55,0.04); border:1px solid rgba(212,175,55,0.15); border-radius:12px; padding:20px 24px; margin:20px 0 30px; }}
        .featured-section h3 {{ color:var(--gold); font-family:'Playfair Display',serif; font-size:1.1rem; margin-bottom:6px; display:inline-flex; align-items:center; gap:8px; }}
        .featured-section .subtitle {{ color:var(--gray); font-size:0.82rem; margin-bottom:16px; font-style:italic; }}
        .featured-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:8px; }}
        .featured-card {{ background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.12); border-radius:8px; padding:10px 14px; text-decoration:none; transition:all 0.2s; text-align:center; }}
        .featured-card:hover {{ border-color:var(--gold); background:rgba(212,175,55,0.12); }}
        .featured-card .fword {{ color:var(--white); font-weight:600; font-size:0.9rem; }}
        .featured-card .ftag {{ color:var(--gold); font-size:0.65rem; text-transform:uppercase; letter-spacing:0.5px; }}
        body.light-mode .featured-section {{ background:rgba(212,175,55,0.03); }}
        body.light-mode .featured-card .fword {{ color:#1a1a1a; }}
        /* Featured-section expand/collapse */
        .featured-section details, .order-section details, .forbidden-section details, .corrupted-section details,
        .genz-section details, .mill-section details,
        .genx-section details, .boomer-section details {{ margin-top:12px; }}
        .featured-section details summary, .order-section details summary, .forbidden-section details summary, .corrupted-section details summary,
        .genz-section details summary, .mill-section details summary,
        .genx-section details summary, .boomer-section details summary {{
            color:var(--gold); font-size:0.82rem; cursor:pointer; user-select:none;
            padding:6px 0; list-style:none; display:inline-flex; align-items:center;
            gap:8px;
        }}
        .featured-section details summary::-webkit-details-marker,
        .order-section details summary::-webkit-details-marker,
        .forbidden-section details summary::-webkit-details-marker,
        .corrupted-section details summary::-webkit-details-marker,
        .genz-section details summary::-webkit-details-marker,
        .mill-section details summary::-webkit-details-marker,
        .genx-section details summary::-webkit-details-marker,
        .boomer-section details summary::-webkit-details-marker {{ display:none; }}
        .featured-section details summary::before, .order-section details summary::before, .forbidden-section details summary::before, .corrupted-section details summary::before,
        .genz-section details summary::before, .mill-section details summary::before,
        .genx-section details summary::before, .boomer-section details summary::before {{
            content:""; display:inline-block; width:0; height:0;
            border-left:5px solid transparent; border-right:5px solid transparent;
            border-top:7px solid var(--gold);
            transition:transform 0.18s ease;
            transform:rotate(-90deg);
        }}
        .featured-section details[open] summary::before, .order-section details[open] summary::before, .forbidden-section details[open] summary::before, .corrupted-section details[open] summary::before,
        .genz-section details[open] summary::before, .mill-section details[open] summary::before,
        .genx-section details[open] summary::before, .boomer-section details[open] summary::before {{ transform:rotate(0deg); }}
        .featured-section details summary:hover, .order-section details summary:hover, .forbidden-section details summary:hover, .corrupted-section details summary:hover,
        .genz-section details summary:hover, .mill-section details summary:hover,
        .genx-section details summary:hover, .boomer-section details summary:hover {{ color:var(--gold-light); }}
        .order-section details summary::before {{ border-top-color:#b85042; }}
        .order-section details summary {{ color:#b85042; }}
        .forbidden-section details summary::before {{ border-top-color:#8b1515; }}
        .forbidden-section details summary {{ color:#8b1515; }}
        .corrupted-section details summary::before {{ border-top-color:#f44336; }}
        .corrupted-section details summary {{ color:#f44336; }}
        .genz-section details summary::before {{ border-top-color:#EC4899; }}
        .genz-section details summary {{ color:#EC4899; }}
        .mill-section details summary::before {{ border-top-color:#14B8A6; }}
        .mill-section details summary {{ color:#14B8A6; }}
        .genx-section details summary::before {{ border-top-color:#84CC16; }}
        .genx-section details summary {{ color:#84CC16; }}
        .boomer-section details summary::before {{ border-top-color:#D97706; }}
        .boomer-section details summary {{ color:#D97706; }}
        .more-grid {{ margin-top:8px; }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <nav>
        <a href="../index.html"><img src="../assets/icons/shield-home-48.png" class="site-icon" alt="" width="16" height="16"> Home</a>
        <a href="../watchman.html"><img src="../assets/icons/shield-bible.png" class="site-icon" alt="" width="16" height="16"> Watchman</a>
        <a href="../bible.html"><img src="../assets/icons/shield-compass.png" class="site-icon" alt="" width="16" height="16"> BTE</a>
        <a href="../lexicon.html"><img src="../assets/icons/shield-alpha-omega-48.png" class="site-icon" alt="" width="16" height="16"> Lexicon</a>
        <a href="../cross-references.html"><img src="../assets/icons/shield-infinity-rope-48.png" class="site-icon" alt="" width="16" height="16"> Cross-Refs</a>
        <a href="index.html" class="active"><img src="../assets/icons/shield-book-greek-48.png" class="site-icon" alt="" width="16" height="16"> Dictionary</a>
        <a href="../blog.html"><img src="../assets/icons/shield-blog-quill-48.png" class="site-icon" alt="" width="16" height="16"> Blog</a>
        <a href="../connect.html"><img src="../assets/icons/shield-handshake.png" class="site-icon" alt="" width="16" height="16"> Connect</a>
    </nav>
    <div style="text-align:center; margin-top:8px; margin-bottom:4px;">
        <div class="bte-theme-toggle" onclick="bteToggleTheme()" title="Toggle dark/light mode">
            <span class="toggle-icon moon-icon">🌙</span>
            <div class="toggle-track"><div class="toggle-knob"></div></div>
            <span class="toggle-icon sun-icon">☀️</span>
        </div>
    </div>
    <div class="container">

        <section class="hero">
            <img src="../assets/icons/shield-book-greek-48.png" alt="Dictionary" width="96" height="96" style="margin-bottom:16px;opacity:0.9;">
            <h1>The MOOP Dictionary</h1>
            <p class="subtitle">of the English Language</p>
            <p style="margin-top:20px;">Words have been stolen, redefined, and weaponized. This dictionary reclaims them &mdash; returning to the etymological roots, the biblical meaning, and the Webster 1828 definitions that shaped Western civilization, against which modern corruptions are measured.</p>
            <p style="margin-top:10px;font-size:0.85rem;color:var(--gold);">{total} entries &middot; Proto-language roots &middot; Collapsible deep-dive sections</p>
        </section>

        <!-- Word of the Day -->
        <div class="wotd-widget" id="wotdWidget"></div>

        <!-- Names sub-page callout -->
        <div class="names-callout">
            <a href="names.html"><img src="../assets/icons/shield-book-greek-48.png" alt=""> Biblical Names &mdash; focused word-study index &rarr;</a>
        </div>

        <!-- Search -->
        <div class="search-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="dictSearch" placeholder="Search entries&hellip;" autocomplete="off" oninput="filterDict(this.value)">
        </div>

        <!-- Search results (shown when searching) -->
        <div id="searchResults">
            <div class="word-grid" id="searchGrid"></div>
            <p id="searchEmpty" style="display:none;color:var(--gray);text-align:center;padding:20px;">No entries found.</p>
        </div>

        <!-- Range buttons (hidden during search) -->
        <div id="rangeSection">
            <div class="range-bar">
                <button class="range-btn" id="btn-AD" onclick="toggleRange('range-AD','btn-AD')"><span class="rarrow"></span> A &ndash; D</button>
                <button class="range-btn" id="btn-EI" onclick="toggleRange('range-EI','btn-EI')"><span class="rarrow"></span> E &ndash; I</button>
                <button class="range-btn" id="btn-JN" onclick="toggleRange('range-JN','btn-JN')"><span class="rarrow"></span> J &ndash; N</button>
                <button class="range-btn" id="btn-OS" onclick="toggleRange('range-OS','btn-OS')"><span class="rarrow"></span> O &ndash; S</button>
                <button class="range-btn" id="btn-TZ" onclick="toggleRange('range-TZ','btn-TZ')"><span class="rarrow"></span> T &ndash; Z</button>
            </div>

            <!-- A-D -->
            <div class="range-panel" id="range-AD">
{AD}
            </div>

            <!-- E-I -->
            <div class="range-panel" id="range-EI">
{EI}
            </div>

            <!-- J-N -->
            <div class="range-panel" id="range-JN">
{JN}
            </div>

            <!-- O-S -->
            <div class="range-panel" id="range-OS">
{OS}
            </div>

            <!-- T-Z -->
            <div class="range-panel" id="range-TZ">
{TZ}
            </div>
        </div><!-- /#rangeSection -->

        <!-- Featured Entries — Doctrinal Anchors -->
        <div class="featured-section">
            <h3><img src="../assets/icons/shield-chain-salvation-48.png" alt="" width="20" height="20"> Doctrinal Anchors</h3>
            <p class="subtitle">Words that hold the line. Foundational entries every man should know cold.</p>
            <div class="featured-grid">
                <a href="trinity.html" class="featured-card"><div class="fword">Trinity</div><div class="ftag">Triune God</div></a>
                <a href="sovereignty.html" class="featured-card"><div class="fword">Sovereignty</div><div class="ftag">Authority</div></a>
                <a href="atonement.html" class="featured-card"><div class="fword">Atonement</div><div class="ftag">The Cross</div></a>
                <a href="resurrection.html" class="featured-card"><div class="fword">Resurrection</div><div class="ftag">Risen Lord</div></a>
                <a href="justification.html" class="featured-card"><div class="fword">Justification</div><div class="ftag">Verdict</div></a>
                <a href="sanctification.html" class="featured-card"><div class="fword">Sanctification</div><div class="ftag">Process</div></a>
                <a href="repentance.html" class="featured-card"><div class="fword">Repentance</div><div class="ftag">Turning</div></a>
                <a href="propitiation.html" class="featured-card"><div class="fword">Propitiation</div><div class="ftag">Satisfaction</div></a>
                <a href="faith.html" class="featured-card"><div class="fword">Faith</div><div class="ftag">Trust</div></a>
                <a href="holiness.html" class="featured-card"><div class="fword">Holiness</div><div class="ftag">Set Apart</div></a>
                <a href="mercy.html" class="featured-card"><div class="fword">Mercy</div><div class="ftag">Compassion</div></a>
                <a href="wrath.html" class="featured-card"><div class="fword">Wrath</div><div class="ftag">Divine Anger</div></a>
                <a href="election.html" class="featured-card"><div class="fword">Election</div><div class="ftag">Chosen</div></a>
                <a href="predestination.html" class="featured-card"><div class="fword">Predestination</div><div class="ftag">Foreordained</div></a>
                <a href="incarnation.html" class="featured-card"><div class="fword">Incarnation</div><div class="ftag">God in Flesh</div></a>
                <a href="mediator.html" class="featured-card"><div class="fword">Mediator</div><div class="ftag">Between</div></a>
                <a href="imputation.html" class="featured-card"><div class="fword">Imputation</div><div class="ftag">Reckoned</div></a>
                <a href="substitution.html" class="featured-card"><div class="fword">Substitution</div><div class="ftag">In Our Place</div></a>
                <a href="glorification.html" class="featured-card"><div class="fword">Glorification</div><div class="ftag">Final Stage</div></a>
                <a href="adoption.html" class="featured-card"><div class="fword">Adoption</div><div class="ftag">Sonship</div></a>
                <a href="regeneration.html" class="featured-card"><div class="fword">Regeneration</div><div class="ftag">New Birth</div></a>
                <a href="redemption.html" class="featured-card"><div class="fword">Redemption</div><div class="ftag">Ransom</div></a>
                <a href="reconciliation.html" class="featured-card"><div class="fword">Reconciliation</div><div class="ftag">Peace</div></a>
                <a href="covenant.html" class="featured-card"><div class="fword">Covenant</div><div class="ftag">Binding</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="featured-grid more-grid">
                    <a href="sola-scriptura.html" class="featured-card"><div class="fword">Sola Scriptura</div><div class="ftag">Scripture Alone</div></a>
                    <a href="sola-fide.html" class="featured-card"><div class="fword">Sola Fide</div><div class="ftag">Faith Alone</div></a>
                    <a href="sola-gratia.html" class="featured-card"><div class="fword">Sola Gratia</div><div class="ftag">Grace Alone</div></a>
                    <a href="solus-christus.html" class="featured-card"><div class="fword">Solus Christus</div><div class="ftag">Christ Alone</div></a>
                    <a href="soli-deo-gloria.html" class="featured-card"><div class="fword">Soli Deo Gloria</div><div class="ftag">For God's Glory</div></a>
                    <a href="gospel.html" class="featured-card"><div class="fword">Gospel</div><div class="ftag">Good News</div></a>
                    <a href="salvation.html" class="featured-card"><div class="fword">Salvation</div><div class="ftag">Saved</div></a>
                    <a href="forgiveness.html" class="featured-card"><div class="fword">Forgiveness</div><div class="ftag">Pardon</div></a>
                    <a href="logos.html" class="featured-card"><div class="fword">Logos</div><div class="ftag">The Word</div></a>
                    <a href="christ.html" class="featured-card"><div class="fword">Christ</div><div class="ftag">Messiah</div></a>
                    <a href="christology.html" class="featured-card"><div class="fword">Christology</div><div class="ftag">Doctrine of Christ</div></a>
                    <a href="providence.html" class="featured-card"><div class="fword">Providence</div><div class="ftag">God's Care</div></a>
                    <a href="omnipotence.html" class="featured-card"><div class="fword">Omnipotence</div><div class="ftag">All-Powerful</div></a>
                    <a href="omniscience.html" class="featured-card"><div class="fword">Omniscience</div><div class="ftag">All-Knowing</div></a>
                    <a href="omnipresence.html" class="featured-card"><div class="fword">Omnipresence</div><div class="ftag">Everywhere</div></a>
                    <a href="immutability.html" class="featured-card"><div class="fword">Immutability</div><div class="ftag">Unchanging</div></a>
                    <a href="eternality.html" class="featured-card"><div class="fword">Eternality</div><div class="ftag">Without End</div></a>
                    <a href="aseity.html" class="featured-card"><div class="fword">Aseity</div><div class="ftag">Self-Existent</div></a>
                    <a href="assurance.html" class="featured-card"><div class="fword">Assurance</div><div class="ftag">Confidence</div></a>
                    <a href="perseverance.html" class="featured-card"><div class="fword">Perseverance</div><div class="ftag">Endurance</div></a>
                    <a href="inerrancy.html" class="featured-card"><div class="fword">Inerrancy</div><div class="ftag">Without Error</div></a>
                    <a href="inspiration.html" class="featured-card"><div class="fword">Inspiration</div><div class="ftag">Breathed Out</div></a>
                    <a href="longsuffering.html" class="featured-card"><div class="fword">Longsuffering</div><div class="ftag">Patient</div></a>
                    <a href="effectual-call.html" class="featured-card"><div class="fword">Effectual Call</div><div class="ftag">Drawn by God</div></a>
                </div>
            </details>
        </div>

        <!-- Biblical Order — patriarchy, headship, the Long House, NXR vocabulary -->
        <div class="order-section" id="orderSection">
            <h3><img src="../assets/icons/shield-crown.png" alt="" width="20" height="20"> Biblical Order</h3>
            <p class="subtitle">Patriarchy, headship, helpmeet, and the recovered vocabulary the modern church has tried to retire &mdash; including the New Christian Right / Kings Hall diagnosis of the Long House, the reviling wife, and the white-knight pattern.</p>
            <div class="order-grid">
                <a href="patriarchy.html" class="order-card"><div class="oword">Patriarchy</div><div class="otag">Father-Rule</div></a>
                <a href="headship.html" class="order-card"><div class="oword">Headship</div><div class="otag">Eph 5:23</div></a>
                <a href="submission.html" class="order-card"><div class="oword">Submission</div><div class="otag">1 Pet 3</div></a>
                <a href="helpmeet.html" class="order-card"><div class="oword">Helpmeet</div><div class="otag">Ezer Kenegdo</div></a>
                <a href="complementarianism.html" class="order-card"><div class="oword">Complementarianism</div><div class="otag">Halfway House</div></a>
                <a href="egalitarianism.html" class="order-card"><div class="oword">Egalitarianism</div><div class="otag">Dressed-up Feminism</div></a>
                <a href="feminism.html" class="order-card"><div class="oword">Feminism</div><div class="otag">Inversion</div></a>
                <a href="long-house.html" class="order-card"><div class="oword">The Long House</div><div class="otag">Soft Matriarchy</div></a>
                <a href="white-knight.html" class="order-card"><div class="oword">White Knight</div><div class="otag">Class Loyalty</div></a>
                <a href="reviling-wife.html" class="order-card"><div class="oword">Reviling Wife</div><div class="otag">Prov 21:9</div></a>
                <a href="contentious-wife.html" class="order-card"><div class="oword">Contentious Wife</div><div class="otag">Prov 27:15</div></a>
                <a href="hypergamy.html" class="order-card"><div class="oword">Hypergamy</div><div class="otag">Observed Pattern</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="order-grid more-grid">
                    <a href="manosphere.html" class="order-card"><div class="oword">Manosphere</div><div class="otag">Digital Subculture</div></a>
                    <a href="new-christian-right.html" class="order-card"><div class="oword">New Christian Right</div><div class="otag">NXR</div></a>
                    <a href="christian-nationalism.html" class="order-card"><div class="oword">Christian Nationalism</div><div class="otag">Ps 2:10</div></a>
                    <a href="kings-hall.html" class="order-card"><div class="oword">Kings Hall</div><div class="otag">Podcast</div></a>
                    <a href="white-knighting.html" class="order-card"><div class="oword">White Knighting</div><div class="otag">Man-Pleasing</div></a>
                    <a href="man-pleasing.html" class="order-card"><div class="oword">Man-Pleasing</div><div class="otag">Gal 1:10</div></a>
                    <a href="partiality.html" class="order-card"><div class="oword">Partiality</div><div class="otag">Lev 19:15</div></a>
                    <a href="quietness.html" class="order-card"><div class="oword">Quietness</div><div class="otag">1 Pet 3:4</div></a>
                    <a href="chivalry.html" class="order-card"><div class="oword">Chivalry</div><div class="otag">Ordered Courage</div></a>
                </div>
            </details>
        </div>

        <!-- Expressly Prohibited — Lev 18-20, Deut 18, Gal 5, Rev 21 prohibitions -->
        <div class="forbidden-section" id="forbiddenSection">
            <h3><img src="../assets/icons/shield-chain-fire-48.png" alt="" width="20" height="20"> Expressly Prohibited</h3>
            <p class="subtitle">Practices Scripture names directly &mdash; in Leviticus, Deuteronomy, the Gospels, the Epistles, or the Revelation &mdash; as forbidden, abomination, or grounds for exclusion from the kingdom. The modern church has retired many of these; the MOOP Dictionary holds them.</p>
            <div class="forbidden-grid">
                <a href="tattoo.html" class="forbidden-card"><div class="pword">Tattoo</div><div class="ptag">Lev 19:28</div></a>
                <a href="cross-dressing.html" class="forbidden-card"><div class="pword">Cross-Dressing</div><div class="ptag">Deut 22:5</div></a>
                <a href="witchcraft.html" class="forbidden-card"><div class="pword">Witchcraft</div><div class="ptag">Ex 22:18</div></a>
                <a href="sorcery.html" class="forbidden-card"><div class="pword">Sorcery</div><div class="ptag">Pharmakeia</div></a>
                <a href="divination.html" class="forbidden-card"><div class="pword">Divination</div><div class="ptag">Deut 18:10</div></a>
                <a href="astrology.html" class="forbidden-card"><div class="pword">Astrology</div><div class="ptag">Isa 47:13</div></a>
                <a href="occult.html" class="forbidden-card"><div class="pword">Occult</div><div class="ptag">Hidden Arts</div></a>
                <a href="sodomy.html" class="forbidden-card"><div class="pword">Sodomy</div><div class="ptag">Lev 18:22</div></a>
                <a href="homosexuality.html" class="forbidden-card"><div class="pword">Homosexuality</div><div class="ptag">Rom 1:26-27</div></a>
                <a href="effeminate.html" class="forbidden-card"><div class="pword">Effeminate</div><div class="ptag">1 Cor 6:9</div></a>
                <a href="molech.html" class="forbidden-card"><div class="pword">Molech</div><div class="ptag">Child Sacrifice</div></a>
                <a href="yoking-unbelievers.html" class="forbidden-card"><div class="pword">Yoking w/ Unbelievers</div><div class="ptag">2 Cor 6:14</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="forbidden-grid more-grid">
                    <a href="transvestism.html" class="forbidden-card"><div class="pword">Transvestism</div><div class="ptag">Deut 22:5</div></a>
                    <a href="necromancy.html" class="forbidden-card"><div class="pword">Necromancy</div><div class="ptag">Deut 18:11</div></a>
                    <a href="bestiality.html" class="forbidden-card"><div class="pword">Bestiality</div><div class="ptag">Lev 18:23</div></a>
                    <a href="incest.html" class="forbidden-card"><div class="pword">Incest</div><div class="ptag">Lev 18:6-18</div></a>
                    <a href="cutting.html" class="forbidden-card"><div class="pword">Cutting / Self-Harm</div><div class="ptag">Lev 19:28</div></a>
                    <a href="cursing-parents.html" class="forbidden-card"><div class="pword">Cursing Parents</div><div class="ptag">Ex 21:17</div></a>
                    <a href="adultery.html" class="forbidden-card"><div class="pword">Adultery</div><div class="ptag">Ex 20:14</div></a>
                    <a href="fornication.html" class="forbidden-card"><div class="pword">Fornication</div><div class="ptag">1 Cor 6:18</div></a>
                    <a href="child-sacrifice.html" class="forbidden-card"><div class="pword">Child Sacrifice</div><div class="ptag">Lev 18:21</div></a>
                    <a href="drunkenness.html" class="forbidden-card"><div class="pword">Drunkenness</div><div class="ptag">Eph 5:18</div></a>
                    <a href="gluttony.html" class="forbidden-card"><div class="pword">Gluttony</div><div class="ptag">Prov 23:21</div></a>
                    <a href="idolatry.html" class="forbidden-card"><div class="pword">Idolatry</div><div class="ptag">Ex 20:3-5</div></a>
                    <a href="murder.html" class="forbidden-card"><div class="pword">Murder</div><div class="ptag">Ex 20:13</div></a>
                    <a href="slander.html" class="forbidden-card"><div class="pword">Slander</div><div class="ptag">Eph 4:31</div></a>
                    <a href="gossip.html" class="forbidden-card"><div class="pword">Gossip</div><div class="ptag">Prov 16:28</div></a>
                    <a href="covetousness.html" class="forbidden-card"><div class="pword">Covetousness</div><div class="ptag">Ex 20:17</div></a>
                </div>
            </details>
        </div>

        <!-- Most Corrupted Words -->
        <div class="corrupted-section" id="corruptedSection">
            <h3><img src="../assets/icons/shield-chain-fire-48.png" alt="" width="20" height="20"> Most Corrupted Words</h3>
            <p class="subtitle">Words that modern culture has stolen, redefined, or weaponized beyond recognition. Click any word to see what it actually means.</p>
            <div class="corrupted-grid">
                <a href="love.html" class="corrupted-card"><div class="cword">Love</div><div class="ctag">Redefined</div></a>
                <a href="tolerance.html" class="corrupted-card"><div class="cword">Tolerance</div><div class="ctag">Weaponized</div></a>
                <a href="equity.html" class="corrupted-card"><div class="cword">Equity</div><div class="ctag">Hijacked</div></a>
                <a href="justice.html" class="corrupted-card"><div class="cword">Justice</div><div class="ctag">Distorted</div></a>
                <a href="diversity.html" class="corrupted-card"><div class="cword">Diversity</div><div class="ctag">Weaponized</div></a>
                <a href="inclusion.html" class="corrupted-card"><div class="cword">Inclusion</div><div class="ctag">Hijacked</div></a>
                <a href="pride.html" class="corrupted-card"><div class="cword">Pride</div><div class="ctag">Inverted</div></a>
                <a href="empathy.html" class="corrupted-card"><div class="cword">Empathy</div><div class="ctag">Weaponized</div></a>
                <a href="truth.html" class="corrupted-card"><div class="cword">Truth</div><div class="ctag">Relativized</div></a>
                <a href="marriage.html" class="corrupted-card"><div class="cword">Marriage</div><div class="ctag">Redefined</div></a>
                <a href="grace.html" class="corrupted-card"><div class="cword">Grace</div><div class="ctag">Cheapened</div></a>
                <a href="identity.html" class="corrupted-card"><div class="cword">Identity</div><div class="ctag">Detached</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="corrupted-grid more-grid">
                    <a href="privilege.html" class="corrupted-card"><div class="cword">Privilege</div><div class="ctag">Weaponized</div></a>
                    <a href="toxic.html" class="corrupted-card"><div class="cword">Toxic</div><div class="ctag">Weaponized</div></a>
                    <a href="authenticity.html" class="corrupted-card"><div class="cword">Authenticity</div><div class="ctag">Corrupted</div></a>
                    <a href="safe-space.html" class="corrupted-card"><div class="cword">Safe Space</div><div class="ctag">Weaponized</div></a>
                    <a href="trauma.html" class="corrupted-card"><div class="cword">Trauma</div><div class="ctag">Inflated</div></a>
                    <a href="problematic.html" class="corrupted-card"><div class="cword">Problematic</div><div class="ctag">Weaponized</div></a>
                    <a href="trigger-warning.html" class="corrupted-card"><div class="cword">Trigger Warning</div><div class="ctag">Invented</div></a>
                    <a href="gender.html" class="corrupted-card"><div class="cword">Gender</div><div class="ctag">Stolen</div></a>
                    <a href="woke.html" class="corrupted-card"><div class="cword">Woke</div><div class="ctag">Hijacked</div></a>
                    <a href="deconstruction.html" class="corrupted-card"><div class="cword">Deconstruction</div><div class="ctag">Repurposed</div></a>
                    <a href="masculinity.html" class="corrupted-card"><div class="cword">Masculinity</div><div class="ctag">Vilified</div></a>
                    <a href="judgment.html" class="corrupted-card"><div class="cword">Judgment</div><div class="ctag">Forbidden</div></a>
                </div>
            </details>
        </div>

        <!-- Gen-Z Decoded -->
        <div class="genz-section" id="genzSection">
            <h3><img src="../assets/icons/shield-blog-quill-48.png" alt="" width="20" height="20"> Gen-Z Decoded</h3>
            <p class="subtitle">Every generation speaks a new dialect. Every dialect reveals a heart. Here is what the words mean and what Scripture says about them.</p>
            <div class="genz-grid">
                <a href="based.html" class="genz-card"><div class="gzword">Based</div><div class="gzverdict gzv-green">Redeemable</div></a>
                <a href="bet-genz.html" class="genz-card"><div class="gzword">Bet</div><div class="gzverdict gzv-green">Redeemable</div></a>
                <a href="bussin.html" class="genz-card"><div class="gzword">Bussin</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                <a href="clutch.html" class="genz-card"><div class="gzword">Clutch</div><div class="gzverdict gzv-green">Redeemable</div></a>
                <a href="cringe-genz.html" class="genz-card"><div class="gzword">Cringe</div><div class="gzverdict gzv-orange">Examine</div></a>
                <a href="delulu.html" class="genz-card"><div class="gzword">Delulu</div><div class="gzverdict gzv-red">Reject</div></a>
                <a href="rizz.html" class="genz-card"><div class="gzword">Rizz</div><div class="gzverdict gzv-orange">Examine</div></a>
                <a href="touch-grass.html" class="genz-card"><div class="gzword">Touch Grass</div><div class="gzverdict gzv-red">Reject</div></a>
                <a href="goat-genz.html" class="genz-card"><div class="gzword">GOAT</div><div class="gzverdict gzv-green">Redeemable</div></a>
                <a href="no-cap.html" class="genz-card"><div class="gzword">No Cap</div><div class="gzverdict gzv-green">Redeemable</div></a>
                <a href="vibe.html" class="genz-card"><div class="gzword">Vibe</div><div class="gzverdict gzv-orange">Examine</div></a>
                <a href="mid.html" class="genz-card"><div class="gzword">Mid</div><div class="gzverdict gzv-orange">Examine</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="genz-grid more-grid">
                    <a href="ate.html" class="genz-card"><div class="gzword">Ate</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="bestie.html" class="genz-card"><div class="gzword">Bestie</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="cap.html" class="genz-card"><div class="gzword">Cap</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="cooked.html" class="genz-card"><div class="gzword">Cooked</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="fire.html" class="genz-card"><div class="gzword">Fire</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="fr-for-real.html" class="genz-card"><div class="gzword">Fr (For Real)</div><div class="gzverdict gzv-green">Redeemable</div></a>
                    <a href="glaze.html" class="genz-card"><div class="gzword">Glaze</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="gyat.html" class="genz-card"><div class="gzword">Gyat</div><div class="gzverdict gzv-red">Reject</div></a>
                    <a href="hit-different.html" class="genz-card"><div class="gzword">Hit Different</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="lock-in.html" class="genz-card"><div class="gzword">Lock In</div><div class="gzverdict gzv-green">Redeemable</div></a>
                    <a href="lowkey.html" class="genz-card"><div class="gzword">Lowkey</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="main-character.html" class="genz-card"><div class="gzword">Main Character</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="npc.html" class="genz-card"><div class="gzword">NPC</div><div class="gzverdict gzv-red">Reject</div></a>
                    <a href="periodt.html" class="genz-card"><div class="gzword">Periodt</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="rent-free.html" class="genz-card"><div class="gzword">Rent Free</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="sheesh.html" class="genz-card"><div class="gzword">Sheesh</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="sigma.html" class="genz-card"><div class="gzword">Sigma</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="slay.html" class="genz-card"><div class="gzword">Slay</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="soft-launch.html" class="genz-card"><div class="gzword">Soft Launch</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="stan.html" class="genz-card"><div class="gzword">Stan</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="the-ick.html" class="genz-card"><div class="gzword">The Ick</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="w-win.html" class="genz-card"><div class="gzword">W (Win)</div><div class="gzverdict gzv-green">Redeemable</div></a>
                    <a href="yapping.html" class="genz-card"><div class="gzword">Yapping</div><div class="gzverdict gzv-yellow">Neutral</div></a>
                    <a href="brainrot.html" class="genz-card"><div class="gzword">Brainrot</div><div class="gzverdict gzv-red">Reject</div></a>
                    <a href="demure.html" class="genz-card"><div class="gzword">Demure</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="doomscrolling.html" class="genz-card"><div class="gzword">Doomscrolling</div><div class="gzverdict gzv-red">Reject</div></a>
                    <a href="looksmaxxing.html" class="genz-card"><div class="gzword">Looksmaxxing</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="mewing.html" class="genz-card"><div class="gzword">Mewing</div><div class="gzverdict gzv-orange">Examine</div></a>
                    <a href="on-god.html" class="genz-card"><div class="gzword">On God</div><div class="gzverdict gzv-red">Reject</div></a>
                </div>
            </details>
        </div>

        <!-- Millennial Decoded -->
        <div class="mill-section" id="millSection">
            <h3><img src="../assets/icons/shield-blog-quill-48.png" alt="" width="20" height="20"> Millennial Decoded</h3>
            <p class="subtitle">Generation 1981&ndash;1996. They delayed adulthood, invented #squadgoals friendship, and turned YOLO into a life-philosophy. Here is what the words mean and what Scripture says.</p>
            <div class="mill-grid">
                <a href="adulting.html" class="mill-card"><div class="mword">Adulting</div><div class="mverdict gzv-orange">Examine</div></a>
                <a href="fomo.html" class="mill-card"><div class="mword">FOMO</div><div class="mverdict gzv-orange">Examine</div></a>
                <a href="ghosting.html" class="mill-card"><div class="mword">Ghosting</div><div class="mverdict gzv-red">Reject</div></a>
                <a href="humblebrag.html" class="mill-card"><div class="mword">Humblebrag</div><div class="mverdict gzv-orange">Examine</div></a>
                <a href="selfie.html" class="mill-card"><div class="mword">Selfie</div><div class="mverdict gzv-orange">Examine</div></a>
                <a href="yolo.html" class="mill-card"><div class="mword">YOLO</div><div class="mverdict gzv-orange">Examine</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="mill-grid more-grid">
                    <a href="bae.html" class="mill-card"><div class="mword">Bae</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="basic.html" class="mill-card"><div class="mword">Basic</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="canceled.html" class="mill-card"><div class="mword">Canceled</div><div class="mverdict gzv-red">Reject</div></a>
                    <a href="cope.html" class="mill-card"><div class="mword">Cope</div><div class="mverdict gzv-red">Reject</div></a>
                    <a href="girlboss.html" class="mill-card"><div class="mword">Girlboss</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="hashtag-life.html" class="mill-card"><div class="mword">Hashtag Life</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="lit.html" class="mill-card"><div class="mword">Lit</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="mood.html" class="mill-card"><div class="mword">Mood</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="narcissism.html" class="mill-card"><div class="mword">Narcissism</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="on-fleek.html" class="mill-card"><div class="mword">On Fleek</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="salty.html" class="mill-card"><div class="mword">Salty</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="side-hustle.html" class="mill-card"><div class="mword">Side Hustle</div><div class="mverdict gzv-green">Redeemable</div></a>
                    <a href="squad-goals.html" class="mill-card"><div class="mword">Squad Goals</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="swipe-right.html" class="mill-card"><div class="mword">Swipe Right</div><div class="mverdict gzv-red">Reject</div></a>
                    <a href="tea.html" class="mill-card"><div class="mword">Tea</div><div class="mverdict gzv-red">Reject</div></a>
                    <a href="throw-shade.html" class="mill-card"><div class="mword">Throw Shade</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="triggered.html" class="mill-card"><div class="mword">Triggered</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="unhinged.html" class="mill-card"><div class="mword">Unhinged</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="avocado-toast.html" class="mill-card"><div class="mword">Avocado Toast</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="doggo.html" class="mill-card"><div class="mword">Doggo</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="millennial-pause.html" class="mill-card"><div class="mword">Millennial Pause</div><div class="mverdict gzv-yellow">Neutral</div></a>
                    <a href="nope.html" class="mill-card"><div class="mword">Nope</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="the-feels.html" class="mill-card"><div class="mword">The Feels</div><div class="mverdict gzv-orange">Examine</div></a>
                    <a href="totes.html" class="mill-card"><div class="mword">Totes</div><div class="mverdict gzv-orange">Examine</div></a>
                </div>
            </details>
        </div>

        <!-- Gen X Decoded -->
        <div class="genx-section" id="genxSection">
            <h3><img src="../assets/icons/shield-blog-quill-48.png" alt="" width="20" height="20"> Gen X Decoded</h3>
            <p class="subtitle">Generation 1965&ndash;1980. Ironic, skeptical, and allergic to earnestness. They taught America the dismissive shrug. Here is what the vocabulary reveals and what Scripture corrects.</p>
            <div class="genx-grid">
                <a href="as-if.html" class="genx-card"><div class="xword">As If!</div><div class="xverdict gzv-yellow">Neutral</div></a>
                <a href="gnarly.html" class="genx-card"><div class="xword">Gnarly</div><div class="xverdict gzv-yellow">Neutral</div></a>
                <a href="my-bad.html" class="genx-card"><div class="xword">My Bad</div><div class="xverdict gzv-green">Redeemable</div></a>
                <a href="slacker.html" class="genx-card"><div class="xword">Slacker</div><div class="xverdict gzv-orange">Examine</div></a>
                <a href="whatever.html" class="genx-card"><div class="xword">Whatever</div><div class="xverdict gzv-orange">Examine</div></a>
                <a href="word-agreement.html" class="genx-card"><div class="xword">Word</div><div class="xverdict gzv-green">Redeemable</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="genx-grid more-grid">
                    <a href="all-that-and-bag-of-chips.html" class="genx-card"><div class="xword">All That &amp; Bag of Chips</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="bling.html" class="genx-card"><div class="xword">Bling</div><div class="xverdict gzv-orange">Examine</div></a>
                    <a href="couch-potato.html" class="genx-card"><div class="xword">Couch Potato</div><div class="xverdict gzv-orange">Examine</div></a>
                    <a href="crib.html" class="genx-card"><div class="xword">Crib</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="diss.html" class="genx-card"><div class="xword">Diss</div><div class="xverdict gzv-red">Reject</div></a>
                    <a href="dope.html" class="genx-card"><div class="xword">Dope</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="homie.html" class="genx-card"><div class="xword">Homie</div><div class="xverdict gzv-green">Redeemable</div></a>
                    <a href="peace-out.html" class="genx-card"><div class="xword">Peace Out</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="phat.html" class="genx-card"><div class="xword">Phat</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="psyche.html" class="genx-card"><div class="xword">Psyche!</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="the-bomb.html" class="genx-card"><div class="xword">The Bomb</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="wack.html" class="genx-card"><div class="xword">Wack</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="chillax.html" class="genx-card"><div class="xword">Chillax</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="da-bomb.html" class="genx-card"><div class="xword">Da Bomb</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="foshizzle.html" class="genx-card"><div class="xword">Foshizzle</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="raise-the-roof.html" class="genx-card"><div class="xword">Raise the Roof</div><div class="xverdict gzv-green">Redeemable</div></a>
                    <a href="tubular.html" class="genx-card"><div class="xword">Tubular</div><div class="xverdict gzv-yellow">Neutral</div></a>
                    <a href="word-up.html" class="genx-card"><div class="xword">Word Up</div><div class="xverdict gzv-green">Redeemable</div></a>
                </div>
            </details>
        </div>

        <!-- Boomer Decoded -->
        <div class="boomer-section" id="boomerSection">
            <h3><img src="../assets/icons/shield-blog-quill-48.png" alt="" width="20" height="20"> Boomer Decoded</h3>
            <p class="subtitle">Generation 1946&ndash;1964. The counterculture vocabulary that built modern America&rsquo;s permissive moral imagination, plus some harmless retro-flavor. Here is what held up and what did not.</p>
            <div class="boomer-grid">
                <a href="far-out.html" class="boomer-card"><div class="bword">Far Out</div><div class="bverdict gzv-yellow">Neutral</div></a>
                <a href="groovy.html" class="boomer-card"><div class="bword">Groovy</div><div class="bverdict gzv-yellow">Neutral</div></a>
                <a href="hang-loose.html" class="boomer-card"><div class="bword">Hang Loose</div><div class="bverdict gzv-orange">Examine</div></a>
                <a href="right-on.html" class="boomer-card"><div class="bword">Right On</div><div class="bverdict gzv-green">Redeemable</div></a>
                <a href="solid.html" class="boomer-card"><div class="bword">Solid</div><div class="bverdict gzv-green">Redeemable</div></a>
                <a href="stoked.html" class="boomer-card"><div class="bword">Stoked</div><div class="bverdict gzv-yellow">Neutral</div></a>
            </div>
            <details>
                <summary><em>expand to see more</em></summary>
                <div class="boomer-grid more-grid">
                    <a href="bread-money.html" class="boomer-card"><div class="bword">Bread</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="bummer.html" class="boomer-card"><div class="bword">Bummer</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="cool-cat.html" class="boomer-card"><div class="bword">Cool Cat</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="dig-it.html" class="boomer-card"><div class="bword">Dig It</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="flower-power.html" class="boomer-card"><div class="bword">Flower Power</div><div class="bverdict gzv-green">Redeemable</div></a>
                    <a href="heavy.html" class="boomer-card"><div class="bword">Heavy</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="hippie.html" class="boomer-card"><div class="bword">Hippie</div><div class="bverdict gzv-orange">Examine</div></a>
                    <a href="jive.html" class="boomer-card"><div class="bword">Jive</div><div class="bverdict gzv-orange">Examine</div></a>
                    <a href="outta-sight.html" class="boomer-card"><div class="bword">Outta Sight</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="square.html" class="boomer-card"><div class="bword">Square</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="swell.html" class="boomer-card"><div class="bword">Swell</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="the-man.html" class="boomer-card"><div class="bword">The Man</div><div class="bverdict gzv-orange">Examine</div></a>
                    <a href="daddy-o.html" class="boomer-card"><div class="bword">Daddy-O</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="dynamite.html" class="boomer-card"><div class="bword">Dynamite</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="foxy.html" class="boomer-card"><div class="bword">Foxy</div><div class="bverdict gzv-orange">Examine</div></a>
                    <a href="funky.html" class="boomer-card"><div class="bword">Funky</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="nifty.html" class="boomer-card"><div class="bword">Nifty</div><div class="bverdict gzv-yellow">Neutral</div></a>
                    <a href="pad-place.html" class="boomer-card"><div class="bword">Pad</div><div class="bverdict gzv-orange">Examine</div></a>
                </div>
            </details>
        </div>

    </div><!-- /.container -->

    <!-- Suggest a Word -->
    <div class="suggest-section">
        <h2>📝 Suggest a Word</h2>
        <p class="suggest-sub">Know a word that should be in the MOOP Dictionary? We&rsquo;re always expanding. Submit your suggestion and we&rsquo;ll review it.</p>
        <form action="https://formsubmit.co/usmcministries2022@gmail.com" method="POST">
            <input type="hidden" name="_subject" value="MOOP Dictionary &mdash; Word Suggestion">
            <input type="hidden" name="_next" value="https://usmcmin.org/dictionary/index.html">
            <input type="hidden" name="_captcha" value="false">
            <label for="suggest-word">Suggested Word *</label>
            <input type="text" id="suggest-word" name="word" placeholder="e.g., Sanctity, Providence, Logos&hellip;" required>
            <label for="suggest-why">Why should it be defined? <span style="color:var(--gray);font-weight:400;">(optional)</span></label>
            <textarea id="suggest-why" name="reason" rows="4" placeholder="Share why this word matters, or how you&rsquo;d like to see it defined&hellip;"></textarea>
            <button type="submit" class="btn-suggest">Submit Suggestion &rarr;</button>
        </form>
    </div>

    <footer>
        <div class="cross-divider"><img src="../assets/icons/shield-cross-bible-48.png" alt="" width="48" height="48" style="opacity:0.8;margin-bottom:10px;"></div>
        <p>
            <a href="../index.html#uniting"><img src="../assets/icons/shield-hands-joining.png" class="site-icon" alt="" width="20" height="20"> Uniting</a>
            &nbsp;&nbsp;
            <a href="../serving.html"><img src="../assets/icons/shield-serving.png" class="site-icon" alt="" width="20" height="20"> Serving</a>
            &nbsp;&nbsp;
            <a href="../mentoring.html"><img src="../assets/icons/shield-mentoring.png" class="site-icon" alt="" width="20" height="20"> Mentoring</a>
            &nbsp;&nbsp;
            <a href="../counseling.html"><img src="../assets/icons/shield-family.png" class="site-icon" alt="" width="20" height="20"> Counseling</a>
            &nbsp;&nbsp;
            <a href="../about.html"><img src="../assets/icons/shield-about-person-24.png" class="site-icon" alt="" width="20" height="20"> About the Founder</a>
        </p>
        <p style="margin-top:10px; font-size:0.82rem; font-style:italic; color:#555;">&ldquo;Iron sharpens iron, and one man sharpens another.&rdquo; &mdash; Proverbs 27:17</p>
        <p style="margin-top:8px; font-size:0.8rem; color:#555;">For more info on our services or products to purchase in support of this ministry, check out our other website: <a href="https://usmcmin.com" style="color:var(--gold);">usmcmin.com</a></p>
        <p style="margin-top:6px; font-size:0.8rem; color:#555;"><a href="../sitemap.html" style="color:var(--gray);font-size:0.85rem;">🗺️ Site Map</a> &nbsp;&nbsp; Powered by MOOPbot Pro</p>
    </footer>
    <script>
    function toggleRange(panelId, btnId) {{
        var panel = document.getElementById(panelId);
        var btn = document.getElementById(btnId);
        var isOpen = panel.classList.contains('open');
        document.querySelectorAll('.range-panel').forEach(function(p) {{ p.classList.remove('open'); }});
        document.querySelectorAll('.range-btn').forEach(function(b) {{ b.classList.remove('open'); }});
        if (!isOpen) {{
            panel.classList.add('open');
            btn.classList.add('open');
        }}
    }}
    function filterDict(q) {{
        var sr = document.getElementById('searchResults');
        var rs = document.getElementById('rangeSection');
        var sg = document.getElementById('searchGrid');
        var se = document.getElementById('searchEmpty');
        q = q.trim().toLowerCase();
        if (!q) {{
            sr.classList.remove('visible');
            rs.style.display = '';
            return;
        }}
        rs.style.display = 'none';
        sr.classList.add('visible');
        var cards = document.querySelectorAll('#rangeSection .word-card');
        var hits = [];
        cards.forEach(function(c) {{
            var w = c.querySelector('.word');
            if (w && w.textContent.toLowerCase().indexOf(q) !== -1) hits.push(c.cloneNode(true));
        }});
        sg.innerHTML = '';
        hits.forEach(function(c) {{ sg.appendChild(c); }});
        se.style.display = hits.length ? 'none' : 'block';
    }}
    function bteToggleTheme(){{document.body.classList.toggle('light-mode');localStorage.setItem('bte-theme',document.body.classList.contains('light-mode')?'light':'dark');}}
    (function(){{if(localStorage.getItem('bte-theme')==='light')document.body.classList.add('light-mode');}})();

    // Featured-section details toggle — swap "expand to see more" ↔ "show less"
    document.querySelectorAll('.corrupted-section details, .order-section details, .forbidden-section details, .genz-section details, .mill-section details, .genx-section details, .boomer-section details, .featured-section details').forEach(function(d){{
        var label = d.querySelector('summary em');
        if(!label) return;
        var update = function(){{ label.textContent = d.open ? 'show less' : 'expand to see more'; }};
        update();
        d.addEventListener('toggle', update);
    }});

    // Word of the Day — curated entries rotating by day of year
    (function(){{
        var WOTD = [
            {{word:'Repentance',slug:'repentance',pos:'noun',def:'A complete turning — not just feeling sorry, but a full reversal of direction. The Greek metanoia means a change of mind that changes everything.'}},
            {{word:'Covenant',slug:'covenant',pos:'noun',def:'A binding, unbreakable agreement initiated by the stronger party. God does not negotiate — He commits.'}},
            {{word:'Sanctification',slug:'sanctification',pos:'noun',def:'The lifelong process of being set apart. You are holy; now be holy. Positional truth becoming practical reality.'}},
            {{word:'Sovereignty',slug:'sovereignty',pos:'noun',def:'God\\u2019s absolute authority over all things. Nothing surprises Him. Nothing thwarts Him. Nothing escapes His governance.'}},
            {{word:'Justification',slug:'justification',pos:'noun',def:'God declares the sinner righteous — not because of what you did, but because of what Christ did. A courtroom verdict, not a gradual process.'}},
            {{word:'Atonement',slug:'atonement',pos:'noun',def:'The covering of sin. Yom Kippur — the Day of Covering. Christ\\u2019s once-for-all sacrifice that satisfied the justice of God.'}},
            {{word:'Redemption',slug:'redemption',pos:'noun',def:'Buying back a slave. Christ paid the ransom price to free us from sin\\u2019s bondage. You were purchased — act like it.'}},
            {{word:'Longsuffering',slug:'longsuffering',pos:'noun',def:'Patience under provocation — endurance without retaliation. The capacity to absorb offense and keep loving. God\\u2019s posture toward sinners.'}},
            {{word:'Abide',slug:'abide',pos:'verb',def:'To remain, to dwell, to stay connected. Jesus said remain in Me. Not visit — abide. Make your home there.'}},
            {{word:'Watchman',slug:'watchman',pos:'noun',def:'One who stands on the wall and sounds the alarm. Not a spectator — a guardian. Called to see what others miss and speak what others won\\u2019t.'}},
            {{word:'Patriarch',slug:'patriarch',pos:'noun',def:'The founding father of a family or nation. Abraham, Isaac, Jacob — men who carried the covenant forward by faith and obedience.'}},
            {{word:'Fortress',slug:'fortress',pos:'noun',def:'A place of absolute safety built on unshakable ground. God Himself is the fortress — not the walls, but the Presence behind them.'}},
            {{word:'Disciple',slug:'disciple',pos:'noun',def:'A learner who follows, imitates, and obeys. Not a fan — a student under authority. The cost is everything; the reward is Christ.'}},
            {{word:'Integrity',slug:'integrity',pos:'noun',def:'Wholeness. The state of being undivided. When your public life and private life are the same man. No cracks, no compartments.'}},
            {{word:'Prudence',slug:'prudence',pos:'noun',def:'Wisdom applied to action. Seeing the consequences before they arrive and adjusting course. The opposite of recklessness.'}},
            {{word:'Valor',slug:'valor',pos:'noun',def:'Strength of mind in the face of danger. Not the absence of fear — the mastery of it. Moral courage under fire.'}},
            {{word:'Meekness',slug:'meekness',pos:'noun',def:'Strength under control. Not weakness — a warhorse reined in. Power submitted to purpose. Jesus was meek and He flipped tables.'}},
            {{word:'Obedience',slug:'obedience',pos:'noun',def:'The willful submission to rightful authority. Not blind compliance — joyful alignment with God\\u2019s revealed will.'}},
            {{word:'Steadfast',slug:'steadfast',pos:'adjective',def:'Immovably faithful. The refusal to be moved by circumstances, feelings, or opposition. Anchored to the Rock.'}},
            {{word:'Kindness',slug:'kindness',pos:'noun',def:'Goodness in action toward another — not softness, but deliberate generosity of spirit. God\\u2019s kindness leads to repentance.'}},
            {{word:'Mercy',slug:'mercy',pos:'noun',def:'Not getting what you deserve. Active compassion that moves you to help — not just feeling sorry but doing something about it.'}},
            {{word:'Grace',slug:'grace',pos:'noun',def:'Getting what you don\\u2019t deserve. God\\u2019s unmerited favor that costs us nothing and cost Him everything. The engine of salvation.'}},
            {{word:'Calling',slug:'calling',pos:'noun',def:'Not a career — a summons. God doesn\\u2019t suggest; He calls. Your life has a purpose that preceded your birth.'}},
            {{word:'Armor',slug:'armor-of-god',pos:'noun',def:'The full equipment of God for spiritual warfare. Belt of truth, breastplate of righteousness, shield of faith — every piece is Christ Himself.'}},
            {{word:'Perseverance',slug:'perseverance-of-saints',pos:'noun',def:'The grit to keep going when everything says stop. Not talent — endurance. The saints who overcome are the ones who simply refused to quit.'}},
            {{word:'Humility',slug:'humility',pos:'noun',def:'Accurate self-assessment before God. Not thinking less of yourself — thinking of yourself less. The prerequisite for every other virtue.'}},
            {{word:'Sacrifice',slug:'sacrifice',pos:'noun',def:'To make sacred by giving up. Real sacrifice costs something you value. If it doesn\\u2019t hurt, it\\u2019s not a sacrifice — it\\u2019s a donation.'}},
            {{word:'Dominion',slug:'dominion',pos:'noun',def:'Rightful rule and stewardship. God gave man dominion over creation — not exploitation, but responsible governance under His authority.'}},
            {{word:'Faithfulness',slug:'faithfulness',pos:'noun',def:'The quality of keeping your word when it costs you. Showing up when no one\\u2019s watching. God is faithful — and He calls us to mirror it.'}},
            {{word:'Reverence',slug:'reverence',pos:'noun',def:'Deep respect born of awe. The fear of the LORD is the beginning of wisdom — not terror, but the breathtaking awareness of who He is.'}}
        ];
        var now = new Date();
        var dayOfYear = Math.floor((now - new Date(now.getFullYear(),0,0)) / 86400000);
        var entry = WOTD[dayOfYear % WOTD.length];
        var el = document.getElementById('wotdWidget');
        if (el) {{
            el.innerHTML = '<h4><img src="../assets/icons/shield-star.png" alt="" width="20" height="20"> Word of the Day</h4>' +
                '<div class="wotd-word"><a href="' + entry.slug + '.html">' + entry.word + '</a></div>' +
                '<div class="wotd-pos">' + entry.pos + '</div>' +
                '<div class="wotd-def">' + entry.def + '</div>';
        }}
    }})();
    </script>
</body>
</html>'''


def main():
    # Scan all word files
    files = sorted(
        f for f in os.listdir(DICT_DIR)
        if f.endswith('.html') and f not in ('index.html', 'template.html')
    )

    words = []
    for fname in files:
        fpath = os.path.join(DICT_DIR, fname)
        try:
            word, pos = extract_word_info(fpath)
            words.append({'file': fname, 'word': word, 'pos': pos})
        except Exception as e:
            print(f'  SKIP {fname}: {e}')

    words.sort(key=lambda w: w['word'].lower())

    # Group by first letter
    by_letter = defaultdict(list)
    for w in words:
        first = w['word'][0].upper() if w['word'] else '#'
        if not first.isalpha():
            first = '#'
        by_letter[first].append(w)

    total = len(words)
    print(f'Total entries: {total}')
    for letter in sorted(by_letter.keys()):
        print(f'  {letter}: {len(by_letter[letter])}')

    html = build_index(words, by_letter, total)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\nWrote {INDEX_FILE}')

    # Rebuild the names sub-page too so it stays in sync.
    names_script = os.path.join(os.path.dirname(__file__), 'bin', 'build_names_index.py')
    if os.path.exists(names_script):
        print('\n--- Rebuilding names sub-page ---')
        subprocess.run([sys.executable, names_script], check=True)


if __name__ == '__main__':
    main()
