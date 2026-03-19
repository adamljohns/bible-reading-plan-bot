#!/usr/bin/env python3
"""
Generate cross-references for Leviticus and Numbers.
Focuses on OT→NT Christological links and major theological themes.
"""

import json

# Verse counts per chapter
LEVITICUS_CHAPTERS = {
    1: 17, 2: 16, 3: 17, 4: 35, 5: 19, 6: 22, 7: 26, 8: 26, 9: 27,
    10: 22, 11: 23, 12: 24, 13: 12, 14: 22, 15: 28, 16: 25, 17: 33,
    18: 23, 19: 41, 20: 12, 21: 13, 22: 21, 23: 21, 24: 8, 25: 36,
    26: 15, 27: 7
}

NUMBERS_CHAPTERS = {
    1: 54, 2: 34, 3: 31, 4: 24, 5: 45, 6: 55, 7: 46, 8: 45, 9: 22,
    10: 25, 11: 44, 12: 58, 13: 47, 14: 36, 15: 35, 16: 32, 17: 26,
    18: 35, 19: 29, 20: 30, 21: 57, 22: 34, 23: 28, 24: 35, 25: 32,
    26: 22, 27: 29, 28: 54, 29: 28, 30: 36, 31: 24, 32: 46, 33: 21,
    34: 43, 35: 29, 36: 53
}

# Specific verse cross-references — theologically notable
SPECIFIC_REFS = {}

# ============================================================
# LEVITICUS
# ============================================================

# Lev 1 - Burnt Offering (complete consecration, Christological)
SPECIFIC_REFS.update({
    "Leviticus 1:1": ["Hebrews 9:14", "Exodus 25:22", "John 17:19"],
    "Leviticus 1:2": ["Romans 12:1", "Hebrews 10:5", "1 Peter 2:5"],
    "Leviticus 1:3": ["Ephesians 5:2", "Hebrews 9:14", "John 1:29", "1 Peter 1:19"],
    "Leviticus 1:4": ["Hebrews 9:28", "2 Corinthians 5:21", "Isaiah 53:6", "Romans 4:25"],
    "Leviticus 1:5": ["Hebrews 9:22", "Ephesians 1:7", "Revelation 1:5"],
    "Leviticus 1:6": ["Hebrews 10:11", "John 19:23", "Isaiah 53:5"],
    "Leviticus 1:7": ["Hebrews 12:29", "Matthew 3:11", "Revelation 4:5"],
    "Leviticus 1:8": ["Romans 12:1", "Philippians 4:18", "Ephesians 5:2"],
    "Leviticus 1:9": ["Philippians 4:18", "Ephesians 5:2", "Hebrews 13:15"],
    "Leviticus 1:10": ["John 1:29", "1 Peter 1:19", "Revelation 5:6"],
    "Leviticus 1:11": ["Hebrews 9:22", "Matthew 26:28", "Colossians 1:20"],
    "Leviticus 1:12": ["Romans 12:1", "Hebrews 9:14", "Isaiah 53:10"],
    "Leviticus 1:13": ["Philippians 4:18", "Ephesians 5:2", "John 17:19"],
    "Leviticus 1:14": ["Luke 2:24", "Matthew 3:16", "John 1:32"],
    "Leviticus 1:15": ["Hebrews 9:22", "1 John 1:7", "Revelation 7:14"],
    "Leviticus 1:16": ["Hebrews 13:11", "John 19:41", "Isaiah 53:9"],
    "Leviticus 1:17": ["Ephesians 5:2", "Romans 12:1", "Hebrews 10:12"],
})

# Lev 2 - Grain Offering
SPECIFIC_REFS.update({
    "Leviticus 2:1": ["John 6:35", "1 Corinthians 5:7", "Matthew 26:26"],
    "Leviticus 2:2": ["Philippians 4:18", "Ephesians 5:2", "Hebrews 13:15"],
    "Leviticus 2:3": ["1 Corinthians 9:13", "Numbers 18:9", "Hebrews 7:28"],
    "Leviticus 2:4": ["John 6:51", "1 Corinthians 10:17", "Matthew 26:26"],
    "Leviticus 2:5": ["John 6:35", "Matthew 4:4", "Deuteronomy 8:3"],
    "Leviticus 2:6": ["John 6:51", "Romans 12:1", "Luke 22:19"],
    "Leviticus 2:7": ["John 6:35", "1 Corinthians 5:7", "Colossians 3:17"],
    "Leviticus 2:8": ["John 6:53", "Hebrews 13:10", "Matthew 26:26"],
    "Leviticus 2:9": ["Philippians 4:18", "Ephesians 5:2", "Romans 15:16"],
    "Leviticus 2:10": ["Numbers 18:9", "1 Corinthians 9:13", "Hebrews 13:10"],
    "Leviticus 2:11": ["1 Corinthians 5:6-8", "Galatians 5:9", "Matthew 16:6"],
    "Leviticus 2:12": ["Romans 11:16", "1 Corinthians 15:20", "James 1:18"],
    "Leviticus 2:13": ["Matthew 5:13", "Mark 9:50", "Colossians 4:6"],
    "Leviticus 2:14": ["1 Corinthians 15:20", "James 1:18", "Romans 8:23"],
    "Leviticus 2:15": ["Philippians 4:18", "Ephesians 5:2", "John 12:3"],
    "Leviticus 2:16": ["Hebrews 13:15", "Romans 15:16", "Philippians 4:18"],
})

# Lev 3 - Peace Offering
SPECIFIC_REFS.update({
    "Leviticus 3:1": ["Ephesians 2:14", "Romans 5:1", "Colossians 1:20"],
    "Leviticus 3:2": ["Hebrews 9:22", "Ephesians 1:7", "Colossians 1:20"],
    "Leviticus 3:3": ["Romans 12:1", "Philippians 4:18", "Hebrews 9:14"],
    "Leviticus 3:4": ["Romans 12:1", "1 Corinthians 6:20", "Colossians 3:17"],
    "Leviticus 3:5": ["Ephesians 5:2", "Philippians 4:18", "Hebrews 10:12"],
    "Leviticus 3:6": ["John 1:29", "1 Peter 1:19", "Colossians 1:20"],
    "Leviticus 3:7": ["Hebrews 9:22", "Ephesians 1:7", "Romans 5:1"],
    "Leviticus 3:8": ["Romans 5:9", "Ephesians 2:13", "Colossians 1:20"],
    "Leviticus 3:9": ["Ephesians 5:2", "Romans 12:1", "Philippians 4:18"],
    "Leviticus 3:10": ["Romans 12:1", "Hebrews 9:14", "Colossians 3:17"],
    "Leviticus 3:11": ["John 6:51", "Hebrews 13:10", "Matthew 26:26"],
    "Leviticus 3:12": ["John 10:11", "1 Peter 2:25", "Hebrews 13:20"],
    "Leviticus 3:13": ["Hebrews 9:22", "Ephesians 1:7", "Romans 5:9"],
    "Leviticus 3:14": ["Romans 12:1", "Hebrews 9:14", "1 Corinthians 6:20"],
    "Leviticus 3:15": ["Philippians 4:18", "Ephesians 5:2", "Colossians 3:17"],
    "Leviticus 3:16": ["Hebrews 13:15", "Romans 12:1", "1 Corinthians 6:20"],
    "Leviticus 3:17": ["Acts 15:29", "Genesis 9:4", "John 6:53"],
})

# Lev 4 - Sin Offering
for v in range(1, 36):
    ref = f"Leviticus 4:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 10:12", "Romans 8:3", "2 Corinthians 5:21", "1 John 2:2"]

SPECIFIC_REFS["Leviticus 4:2"] = ["Romans 3:23", "James 1:14", "Hebrews 5:2", "1 John 2:1"]
SPECIFIC_REFS["Leviticus 4:3"] = ["Hebrews 9:7", "Hebrews 5:3", "2 Corinthians 5:21", "Romans 8:3"]
SPECIFIC_REFS["Leviticus 4:13"] = ["Romans 3:23", "1 John 1:8", "Acts 3:17", "Hebrews 9:7"]
SPECIFIC_REFS["Leviticus 4:20"] = ["Hebrews 10:4", "Romans 3:25", "1 John 2:2", "Colossians 2:14"]
SPECIFIC_REFS["Leviticus 4:26"] = ["Romans 5:9", "Hebrews 9:22", "1 John 1:9", "Colossians 1:20"]
SPECIFIC_REFS["Leviticus 4:31"] = ["2 Corinthians 5:21", "Romans 4:7", "Hebrews 10:17", "Colossians 2:13"]
SPECIFIC_REFS["Leviticus 4:35"] = ["Hebrews 9:14", "1 John 1:7", "Romans 5:11", "Ephesians 1:7"]

# Lev 5 - Guilt Offering
for v in range(1, 20):
    ref = f"Leviticus 5:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 John 1:9", "Hebrews 9:22", "Romans 3:20", "James 5:16"]

SPECIFIC_REFS["Leviticus 5:5"] = ["James 5:16", "Proverbs 28:13", "1 John 1:9", "Psalm 32:5"]
SPECIFIC_REFS["Leviticus 5:17"] = ["Romans 5:13", "James 4:17", "1 John 3:4", "Galatians 3:10"]

# Lev 6 - Altar fire / offerings
for v in range(1, 23):
    ref = f"Leviticus 6:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 13:10", "1 Corinthians 9:13", "Romans 12:1", "Philippians 4:18"]

SPECIFIC_REFS["Leviticus 6:12"] = ["Hebrews 12:29", "1 Thessalonians 5:19", "Matthew 3:11", "Revelation 4:5"]
SPECIFIC_REFS["Leviticus 6:13"] = ["Hebrews 7:25", "Romans 8:34", "1 John 2:1", "John 17:9"]

# Lev 7 - Laws of offerings
for v in range(1, 27):
    ref = f"Leviticus 7:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 13:10", "1 Corinthians 10:21", "Romans 12:1", "Colossians 2:17"]

SPECIFIC_REFS["Leviticus 7:11"] = ["Philippians 4:6", "Ephesians 5:20", "Hebrews 13:15", "Colossians 3:17"]
SPECIFIC_REFS["Leviticus 7:26"] = ["Acts 15:29", "Genesis 9:4", "John 6:53", "Hebrews 9:22"]

# Lev 8 - Consecration of Aaron
for v in range(1, 27):
    ref = f"Leviticus 8:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 7:28", "1 Peter 2:5", "Hebrews 9:6", "Exodus 29:1"]

SPECIFIC_REFS["Leviticus 8:6"] = ["John 13:10", "Titus 3:5", "Hebrews 10:22", "Ephesians 5:26"]
SPECIFIC_REFS["Leviticus 8:12"] = ["Psalm 133:2", "1 John 2:20", "Acts 10:38", "Matthew 3:16"]
SPECIFIC_REFS["Leviticus 8:15"] = ["Hebrews 9:22", "Romans 5:9", "Ephesians 2:13", "1 John 1:7"]
SPECIFIC_REFS["Leviticus 8:30"] = ["Acts 2:33", "Ephesians 1:13", "1 John 2:27", "John 20:22"]

# Lev 9 - Aaron begins ministry
for v in range(1, 28):
    ref = f"Leviticus 9:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 9:11", "Hebrews 7:27", "John 14:6", "1 Timothy 2:5"]

SPECIFIC_REFS["Leviticus 9:7"] = ["Hebrews 7:27", "Hebrews 5:3", "1 Timothy 2:5", "Romans 8:34"]
SPECIFIC_REFS["Leviticus 9:22"] = ["Numbers 6:24-26", "2 Corinthians 13:14", "Luke 24:50", "Hebrews 7:7"]
SPECIFIC_REFS["Leviticus 9:24"] = ["1 Kings 18:38", "Matthew 3:11", "Acts 2:3", "Hebrews 12:29"]

# Lev 10 - Nadab & Abihu
for v in range(1, 23):
    ref = f"Leviticus 10:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 12:29", "Acts 5:1-11", "1 Corinthians 11:29", "Revelation 15:4"]

SPECIFIC_REFS["Leviticus 10:1"] = ["Hebrews 12:29", "Acts 5:5", "Numbers 3:4", "1 Chronicles 24:2"]
SPECIFIC_REFS["Leviticus 10:3"] = ["Isaiah 6:3", "Revelation 15:4", "John 17:11", "Hebrews 12:28"]
SPECIFIC_REFS["Leviticus 10:9"] = ["Luke 1:15", "Numbers 6:3", "Proverbs 31:4", "Ephesians 5:18"]

# Lev 11 - Clean/unclean animals
for v in range(1, 24):
    ref = f"Leviticus 11:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Acts 10:15", "Mark 7:19", "Colossians 2:16", "1 Timothy 4:4"]

SPECIFIC_REFS["Leviticus 11:44"] = ["1 Peter 1:16", "Matthew 5:48", "Hebrews 12:14", "2 Corinthians 7:1"]
SPECIFIC_REFS["Leviticus 11:45"] = ["1 Peter 1:15", "Ephesians 1:4", "1 Thessalonians 4:7", "Hebrews 12:14"]

# Lev 12 - Purification after childbirth
SPECIFIC_REFS.update({
    "Leviticus 12:1": ["Luke 2:22", "Galatians 4:4", "Romans 8:3", "Numbers 19:11"],
    "Leviticus 12:2": ["Psalm 51:5", "Romans 5:12", "Job 14:4", "John 3:6"],
    "Leviticus 12:3": ["Genesis 17:12", "Luke 2:21", "Romans 4:11", "Philippians 3:5"],
    "Leviticus 12:4": ["Luke 2:22", "Galatians 4:4", "Hebrews 9:13", "Numbers 19:12"],
    "Leviticus 12:5": ["Galatians 4:4", "Romans 8:3", "Luke 2:22", "Hebrews 9:13"],
    "Leviticus 12:6": ["Luke 2:24", "Hebrews 10:5", "Romans 12:1", "Philippians 4:18"],
    "Leviticus 12:7": ["Hebrews 9:14", "1 John 1:7", "Titus 3:5", "Hebrews 10:22"],
    "Leviticus 12:8": ["Luke 2:24", "2 Corinthians 8:9", "Matthew 5:3", "James 2:5"],
})
# Fill remaining
for v in range(9, 25):
    ref = f"Leviticus 12:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Luke 2:22", "Galatians 4:4", "Hebrews 9:13", "Romans 12:1"]

# Lev 13-14 - Leprosy (skin diseases)
for ch in [13, 14]:
    chap_len = LEVITICUS_CHAPTERS[ch]
    for v in range(1, chap_len + 1):
        ref = f"Leviticus {ch}:{v}"
        if ref not in SPECIFIC_REFS:
            SPECIFIC_REFS[ref] = ["Matthew 8:2", "Luke 17:14", "Mark 1:44", "Luke 5:12"]

SPECIFIC_REFS["Leviticus 13:45"] = ["Mark 1:40", "Luke 17:12", "Numbers 5:2", "2 Kings 7:3"]
SPECIFIC_REFS["Leviticus 13:46"] = ["Numbers 12:14", "Luke 17:12", "John 11:50", "Hebrews 13:12"]
SPECIFIC_REFS["Leviticus 14:7"] = ["Hebrews 9:19", "Mark 1:44", "Psalm 51:7", "John 13:8"]
SPECIFIC_REFS["Leviticus 14:11"] = ["Mark 1:44", "Luke 5:14", "Hebrews 9:7", "Matthew 8:4"]
SPECIFIC_REFS["Leviticus 14:18"] = ["Hebrews 9:22", "Romans 5:9", "1 John 1:7", "Ephesians 1:7"]

# Lev 15 - Bodily discharges
for v in range(1, 29):
    ref = f"Leviticus 15:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Matthew 9:20", "Hebrews 9:13", "Titus 3:5", "1 Corinthians 6:11"]

SPECIFIC_REFS["Leviticus 15:25"] = ["Mark 5:25", "Luke 8:43", "Matthew 9:20", "Hebrews 9:14"]
SPECIFIC_REFS["Leviticus 15:28"] = ["Hebrews 9:14", "John 13:8", "Titus 3:5", "1 Corinthians 6:11"]

# Lev 16 - Day of Atonement (MAJOR Christological chapter)
SPECIFIC_REFS.update({
    "Leviticus 16:1": ["Hebrews 9:7", "Hebrews 10:19", "Leviticus 10:2", "Hebrews 9:25"],
    "Leviticus 16:2": ["Hebrews 9:7", "Exodus 25:22", "Hebrews 10:19", "Matthew 27:51"],
    "Leviticus 16:3": ["Hebrews 9:12", "Hebrews 7:27", "1 John 2:2", "Romans 3:25"],
    "Leviticus 16:4": ["Revelation 19:8", "Isaiah 61:10", "Zechariah 3:4", "Colossians 3:12"],
    "Leviticus 16:5": ["Hebrews 9:12", "John 1:29", "1 Peter 1:19", "Isaiah 53:7"],
    "Leviticus 16:6": ["Hebrews 7:27", "Hebrews 5:3", "Romans 8:34", "1 Timothy 2:5"],
    "Leviticus 16:7": ["Hebrews 9:7", "Isaiah 53:6", "John 11:50", "Romans 4:25"],
    "Leviticus 16:8": ["Matthew 27:26", "Isaiah 53:6", "Hebrews 9:28", "John 11:50"],
    "Leviticus 16:9": ["Hebrews 9:12", "Romans 3:25", "2 Corinthians 5:21", "1 Peter 3:18"],
    "Leviticus 16:10": ["Matthew 27:26", "Hebrews 9:26", "Isaiah 53:6", "John 11:49"],
    "Leviticus 16:11": ["Hebrews 7:27", "Hebrews 9:25", "1 Timothy 2:5", "Romans 8:34"],
    "Leviticus 16:12": ["Revelation 8:3", "Luke 1:10", "Hebrews 9:4", "Psalm 141:2"],
    "Leviticus 16:13": ["Hebrews 9:4", "Revelation 8:3", "Exodus 25:22", "Hebrews 9:7"],
    "Leviticus 16:14": ["Hebrews 9:12", "Romans 3:25", "1 John 2:2", "Ephesians 1:7"],
    "Leviticus 16:15": ["Hebrews 9:12", "Hebrews 10:19", "Matthew 27:51", "Romans 3:25"],
    "Leviticus 16:16": ["Hebrews 9:23", "Romans 3:25", "2 Corinthians 5:21", "Isaiah 53:5"],
    "Leviticus 16:17": ["1 Timothy 2:5", "Hebrews 9:25", "Hebrews 7:27", "Romans 8:34"],
    "Leviticus 16:18": ["Hebrews 9:22", "Romans 5:9", "Ephesians 2:13", "Colossians 1:20"],
    "Leviticus 16:19": ["Hebrews 9:23", "1 John 1:7", "Revelation 7:14", "Romans 3:25"],
    "Leviticus 16:20": ["Isaiah 53:6", "Hebrews 9:28", "Romans 4:25", "John 1:29"],
    "Leviticus 16:21": ["Isaiah 53:6", "Matthew 27:23", "Hebrews 9:28", "2 Corinthians 5:21"],
    "Leviticus 16:22": ["Isaiah 53:11", "John 1:29", "Hebrews 9:28", "Romans 4:25"],
    "Leviticus 16:23": ["Hebrews 9:12", "Revelation 19:14", "Colossians 3:12", "Isaiah 61:10"],
    "Leviticus 16:24": ["Hebrews 9:14", "Titus 3:5", "Revelation 19:8", "Isaiah 61:10"],
    "Leviticus 16:25": ["Philippians 4:18", "Ephesians 5:2", "Romans 15:16", "Hebrews 13:15"],
    "Leviticus 16:29": ["Hebrews 10:3", "Acts 27:9", "Isaiah 58:3", "Romans 3:20"],
    "Leviticus 16:30": ["Hebrews 10:4", "Romans 3:25", "1 John 1:7", "Hebrews 9:14"],
    "Leviticus 16:31": ["Hebrews 4:9", "Matthew 11:28", "Romans 8:1", "Colossians 2:14"],
    "Leviticus 16:32": ["Hebrews 5:4", "Hebrews 7:28", "John 1:29", "1 Peter 2:9"],
    "Leviticus 16:33": ["Hebrews 9:23", "Romans 3:25", "Hebrews 9:5", "Matthew 27:51"],
    "Leviticus 16:34": ["Hebrews 10:3", "Hebrews 9:25", "Romans 3:25", "1 John 2:2"],
})

# Lev 17 - Sacredness of blood
SPECIFIC_REFS.update({
    "Leviticus 17:4": ["Hebrews 9:22", "Genesis 9:5", "Acts 15:29", "John 6:53"],
    "Leviticus 17:7": ["1 Corinthians 10:20", "Deuteronomy 32:17", "Revelation 9:20", "Psalm 106:37"],
    "Leviticus 17:10": ["Acts 15:29", "Genesis 9:4", "John 6:53", "Hebrews 9:22"],
    "Leviticus 17:11": ["Hebrews 9:22", "Matthew 26:28", "1 John 1:7", "Romans 5:9"],
    "Leviticus 17:14": ["Acts 15:29", "Genesis 9:4", "Hebrews 9:22", "John 6:53"],
})
for v in range(1, 34):
    ref = f"Leviticus 17:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 9:22", "Acts 15:29", "John 6:53", "Romans 5:9"]

# Lev 18 - Sexual ethics / holiness
for v in range(1, 24):
    ref = f"Leviticus 18:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 6:9", "1 Thessalonians 4:3", "Romans 1:24", "Ephesians 5:3"]

SPECIFIC_REFS["Leviticus 18:5"] = ["Romans 10:5", "Galatians 3:12", "Ezekiel 20:11", "Romans 7:10"]
SPECIFIC_REFS["Leviticus 18:22"] = ["Romans 1:27", "1 Corinthians 6:9", "1 Timothy 1:10", "Jude 1:7"]

# Lev 19 - Holiness code
for v in range(1, 42):
    ref = f"Leviticus 19:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Peter 1:16", "Matthew 5:48", "Hebrews 12:14", "Romans 13:9"]

SPECIFIC_REFS["Leviticus 19:2"] = ["1 Peter 1:16", "Matthew 5:48", "Hebrews 12:14", "2 Corinthians 7:1"]
SPECIFIC_REFS["Leviticus 19:9"] = ["Ruth 2:7", "Deuteronomy 24:19", "Matthew 25:35", "James 2:15"]
SPECIFIC_REFS["Leviticus 19:12"] = ["Matthew 5:33", "James 5:12", "Matthew 23:16", "Numbers 30:2"]
SPECIFIC_REFS["Leviticus 19:14"] = ["Matthew 18:6", "Romans 14:13", "1 Corinthians 8:9", "Deuteronomy 27:18"]
SPECIFIC_REFS["Leviticus 19:15"] = ["John 7:24", "James 2:1", "Proverbs 24:23", "Acts 10:34"]
SPECIFIC_REFS["Leviticus 19:17"] = ["Matthew 18:15", "Luke 17:3", "Ephesians 4:25", "Galatians 6:1"]
SPECIFIC_REFS["Leviticus 19:18"] = ["Matthew 22:39", "Romans 13:9", "Galatians 5:14", "James 2:8"]
SPECIFIC_REFS["Leviticus 19:34"] = ["Matthew 25:35", "Hebrews 13:2", "Galatians 3:28", "Romans 15:7"]
SPECIFIC_REFS["Leviticus 19:36"] = ["Proverbs 11:1", "Amos 8:5", "Micah 6:11", "Luke 16:10"]

# Lev 20 - Punishments for sin
for v in range(1, 13):
    ref = f"Leviticus 20:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 6:9", "Galatians 5:19", "Romans 1:32", "1 Thessalonians 4:3"]

SPECIFIC_REFS["Leviticus 20:7"] = ["1 Peter 1:16", "1 Thessalonians 4:7", "Hebrews 12:14", "2 Corinthians 7:1"]
SPECIFIC_REFS["Leviticus 20:26"] = ["1 Peter 2:9", "Ephesians 1:4", "John 15:19", "Colossians 3:12"]

# Lev 21-22 - Priests / offerings
for ch in [21, 22]:
    chap_len = LEVITICUS_CHAPTERS[ch]
    for v in range(1, chap_len + 1):
        ref = f"Leviticus {ch}:{v}"
        if ref not in SPECIFIC_REFS:
            SPECIFIC_REFS[ref] = ["Hebrews 7:26", "1 Peter 2:5", "1 Peter 2:9", "Revelation 1:6"]

SPECIFIC_REFS["Leviticus 21:8"] = ["Hebrews 7:26", "John 17:17", "Ephesians 5:26", "1 Peter 2:9"]
SPECIFIC_REFS["Leviticus 21:17"] = ["Hebrews 7:26", "2 Corinthians 5:21", "John 8:46", "1 Peter 1:19"]
SPECIFIC_REFS["Leviticus 22:20"] = ["Hebrews 9:14", "1 Peter 1:19", "Ephesians 5:27", "Colossians 1:22"]
SPECIFIC_REFS["Leviticus 22:21"] = ["Romans 12:1", "Philippians 4:18", "Ephesians 5:2", "1 Peter 1:19"]

# Lev 23 - Feasts
SPECIFIC_REFS.update({
    "Leviticus 23:3": ["Hebrews 4:9", "Mark 2:27", "Matthew 12:8", "Colossians 2:16"],
    "Leviticus 23:4": ["Colossians 2:17", "Hebrews 8:5", "John 1:14", "Galatians 4:10"],
    "Leviticus 23:5": ["1 Corinthians 5:7", "John 1:29", "Matthew 26:17", "John 19:14"],
    "Leviticus 23:6": ["1 Corinthians 5:8", "Matthew 26:17", "Mark 14:1", "Galatians 5:9"],
    "Leviticus 23:7": ["Hebrews 4:9", "Colossians 2:16", "John 19:31", "Acts 12:3"],
    "Leviticus 23:10": ["1 Corinthians 15:20", "James 1:18", "Romans 8:23", "2 Thessalonians 2:13"],
    "Leviticus 23:11": ["1 Corinthians 15:23", "Matthew 28:1", "Mark 16:2", "John 20:1"],
    "Leviticus 23:15": ["Acts 2:1", "Leviticus 23:16", "Deuteronomy 16:9", "John 14:26"],
    "Leviticus 23:16": ["Acts 2:1", "John 14:16", "Acts 1:8", "John 16:7"],
    "Leviticus 23:17": ["Matthew 13:33", "1 Corinthians 5:6", "Galatians 5:9", "Acts 2:38"],
    "Leviticus 23:22": ["Ruth 2:7", "Deuteronomy 24:19", "Matthew 25:40", "James 2:15"],
    "Leviticus 23:24": ["1 Thessalonians 4:16", "Revelation 8:2", "Matthew 24:31", "Numbers 29:1"],
    "Leviticus 23:26": ["Hebrews 9:7", "Acts 27:9", "Romans 3:25", "Hebrews 10:3"],
    "Leviticus 23:27": ["Hebrews 10:4", "Romans 3:25", "Acts 27:9", "Hebrews 9:14"],
    "Leviticus 23:28": ["Romans 3:25", "Hebrews 9:14", "1 John 2:2", "Colossians 2:14"],
    "Leviticus 23:29": ["Acts 3:23", "Romans 10:13", "John 3:36", "Hebrews 2:3"],
    "Leviticus 23:32": ["Hebrews 4:9", "Romans 8:1", "Colossians 2:14", "Matthew 11:28"],
    "Leviticus 23:34": ["John 7:2", "John 7:37", "Zechariah 14:16", "Revelation 7:9"],
    "Leviticus 23:40": ["Revelation 7:9", "John 12:13", "Matthew 21:8", "Nehemiah 8:15"],
    "Leviticus 23:43": ["John 8:56", "Hebrews 11:9", "Exodus 12:17", "Deuteronomy 16:3"],
})
for v in range(1, 22):
    ref = f"Leviticus 23:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Colossians 2:17", "Hebrews 10:1", "Galatians 4:10", "Romans 14:5"]

# Lev 24
for v in range(1, 9):
    ref = f"Leviticus 24:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Matthew 5:14", "John 8:12", "Revelation 21:23", "2 Corinthians 4:6"]

SPECIFIC_REFS["Leviticus 24:2"] = ["John 8:12", "Matthew 5:14", "Revelation 21:23", "Psalm 119:105"]
SPECIFIC_REFS["Leviticus 24:5"] = ["Matthew 12:4", "Mark 2:26", "Luke 6:4", "Hebrews 9:2"]
SPECIFIC_REFS["Leviticus 24:8"] = ["Hebrews 9:2", "Matthew 12:4", "Exodus 25:30", "Revelation 21:3"]

# Lev 25 - Jubilee
SPECIFIC_REFS.update({
    "Leviticus 25:2": ["Hebrews 4:9", "Deuteronomy 15:1", "Exodus 23:11", "Mark 2:27"],
    "Leviticus 25:4": ["Hebrews 4:9", "Mark 2:27", "Deuteronomy 15:2", "Matthew 11:28"],
    "Leviticus 25:8": ["Luke 4:18", "Isaiah 61:1", "2 Corinthians 6:2", "Daniel 9:24"],
    "Leviticus 25:9": ["Luke 4:18", "Isaiah 61:1", "2 Corinthians 6:2", "Revelation 8:2"],
    "Leviticus 25:10": ["Luke 4:18", "Isaiah 61:1", "Galatians 5:1", "2 Corinthians 3:17"],
    "Leviticus 25:11": ["Luke 4:18", "Isaiah 61:2", "Hebrews 4:9", "Romans 8:21"],
    "Leviticus 25:12": ["John 8:36", "Galatians 5:1", "2 Corinthians 3:17", "Romans 8:2"],
    "Leviticus 25:13": ["Luke 4:18", "Isaiah 61:1", "Matthew 25:14", "Romans 8:21"],
    "Leviticus 25:23": ["Psalm 24:1", "Hebrews 11:13", "1 Peter 2:11", "1 Chronicles 29:14"],
    "Leviticus 25:25": ["Ruth 4:4", "Galatians 3:13", "Jeremiah 32:7", "Hebrews 9:12"],
    "Leviticus 25:35": ["Matthew 25:35", "Luke 10:36", "Galatians 6:2", "Romans 15:1"],
    "Leviticus 25:36": ["Exodus 22:25", "Deuteronomy 23:19", "Luke 6:35", "Ezekiel 18:8"],
    "Leviticus 25:42": ["1 Corinthians 7:23", "Galatians 5:1", "Romans 6:22", "John 8:36"],
    "Leviticus 25:55": ["1 Corinthians 7:23", "John 8:36", "Romans 6:22", "Galatians 5:1"],
})
for v in range(1, 37):
    ref = f"Leviticus 25:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Luke 4:18", "Isaiah 61:1", "Galatians 5:1", "Romans 8:21"]

# Lev 26 - Blessings and curses
SPECIFIC_REFS.update({
    "Leviticus 26:1": ["Exodus 20:4", "Acts 15:20", "1 Corinthians 10:14", "Colossians 3:5"],
    "Leviticus 26:3": ["Deuteronomy 28:1", "Matthew 6:33", "John 15:10", "Romans 8:28"],
    "Leviticus 26:11": ["John 14:23", "Revelation 21:3", "2 Corinthians 6:16", "Ezekiel 37:27"],
    "Leviticus 26:12": ["2 Corinthians 6:16", "Revelation 21:3", "Hebrews 8:10", "Jeremiah 31:33"],
    "Leviticus 26:13": ["Galatians 5:1", "John 8:36", "Romans 8:2", "1 Corinthians 7:23"],
    "Leviticus 26:14": ["Galatians 3:10", "Deuteronomy 28:15", "Romans 2:8", "John 3:36"],
    "Leviticus 26:40": ["1 John 1:9", "Proverbs 28:13", "Nehemiah 9:2", "Daniel 9:5"],
    "Leviticus 26:41": ["Acts 7:51", "Jeremiah 9:26", "Romans 2:29", "Deuteronomy 10:16"],
    "Leviticus 26:42": ["Romans 11:1", "Acts 3:13", "Luke 1:55", "Galatians 3:17"],
    "Leviticus 26:44": ["Romans 11:1", "Acts 3:13", "Luke 1:54", "Deuteronomy 4:31"],
    "Leviticus 26:45": ["Romans 11:28", "Luke 1:72", "Acts 3:25", "Hebrews 8:9"],
})
for v in range(1, 16):
    ref = f"Leviticus 26:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Galatians 3:10", "Deuteronomy 28:1", "2 Corinthians 6:16", "Romans 8:28"]

# Lev 27 - Vows and dedications
for v in range(1, 8):
    ref = f"Leviticus 27:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Romans 12:1", "1 Corinthians 6:20", "Numbers 30:2", "Matthew 5:33"]

SPECIFIC_REFS["Leviticus 27:2"] = ["Romans 12:1", "1 Corinthians 6:20", "Numbers 30:2", "Judges 11:30"]
SPECIFIC_REFS["Leviticus 27:30"] = ["Malachi 3:10", "Matthew 23:23", "Luke 11:42", "Genesis 14:20"]


# ============================================================
# NUMBERS
# ============================================================

# Num 1-2 - Census
for ch in [1, 2]:
    chap_len = NUMBERS_CHAPTERS[ch]
    for v in range(1, chap_len + 1):
        ref = f"Numbers {ch}:{v}"
        if ref not in SPECIFIC_REFS:
            SPECIFIC_REFS[ref] = ["Revelation 7:4", "Luke 2:1", "Galatians 3:29", "Revelation 21:12"]

SPECIFIC_REFS["Numbers 1:2"] = ["Luke 2:1", "Revelation 7:4", "Galatians 3:29", "Matthew 1:17"]
SPECIFIC_REFS["Numbers 1:52"] = ["Revelation 21:12", "Hebrews 4:1", "1 Corinthians 14:40", "Romans 13:1"]
SPECIFIC_REFS["Numbers 2:2"] = ["Revelation 7:4", "Galatians 3:29", "Ephesians 1:13", "Revelation 14:1"]

# Num 3 - Levites
for v in range(1, 32):
    ref = f"Numbers 3:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 7:5", "1 Peter 2:9", "Revelation 1:6", "Romans 12:1"]

SPECIFIC_REFS["Numbers 3:12"] = ["Luke 2:23", "Exodus 13:2", "Hebrews 7:5", "Romans 8:29"]
SPECIFIC_REFS["Numbers 3:13"] = ["Exodus 13:2", "Luke 2:23", "Romans 8:29", "Hebrews 12:23"]

# Num 4 - Levitical duties
for v in range(1, 25):
    ref = f"Numbers 4:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 9:6", "1 Peter 4:10", "Romans 12:7", "1 Corinthians 12:28"]

# Num 5 - Laws, adultery test
for v in range(1, 46):
    ref = f"Numbers 5:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["John 8:3", "Galatians 6:1", "1 Corinthians 5:11", "Hebrews 9:13"]

SPECIFIC_REFS["Numbers 5:7"] = ["1 John 1:9", "James 5:16", "Proverbs 28:13", "Luke 15:18"]
SPECIFIC_REFS["Numbers 5:21"] = ["John 8:10", "Galatians 5:19", "Romans 7:3", "1 Corinthians 6:9"]

# Num 6 - Nazirite vow + Aaronic blessing
SPECIFIC_REFS.update({
    "Numbers 6:1": ["Acts 21:23", "Luke 1:15", "Luke 7:33", "Judges 13:5"],
    "Numbers 6:2": ["Acts 21:23", "Romans 12:1", "Luke 1:15", "1 Corinthians 7:34"],
    "Numbers 6:3": ["Luke 1:15", "Luke 7:33", "Acts 21:24", "Matthew 11:18"],
    "Numbers 6:5": ["Judges 13:5", "Luke 1:15", "Acts 18:18", "1 Samuel 1:11"],
    "Numbers 6:8": ["Luke 1:15", "Romans 12:1", "Hebrews 7:26", "1 Peter 2:9"],
    "Numbers 6:18": ["Acts 18:18", "Acts 21:24", "Romans 12:1", "1 Corinthians 6:20"],
    "Numbers 6:24": ["Ephesians 1:3", "2 Corinthians 13:14", "Philippians 4:7", "Luke 24:50"],
    "Numbers 6:25": ["Psalm 80:3", "2 Corinthians 4:6", "Matthew 5:16", "John 1:14"],
    "Numbers 6:26": ["John 14:27", "Philippians 4:7", "Romans 5:1", "Colossians 3:15"],
    "Numbers 6:27": ["Matthew 28:19", "Acts 4:12", "Philippians 2:9", "John 17:11"],
})
for v in range(4, 55):
    ref = f"Numbers 6:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Luke 1:15", "Romans 12:1", "1 Peter 2:9", "Acts 21:23"]

# Num 7 - Offerings of the leaders
for v in range(1, 47):
    ref = f"Numbers 7:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Romans 12:1", "Philippians 4:18", "Ephesians 5:2", "Hebrews 13:16"]

SPECIFIC_REFS["Numbers 7:89"] = ["Exodus 25:22", "Leviticus 16:2", "Hebrews 9:5", "John 20:22"]

# Num 8 - Levites consecrated
for v in range(1, 46):
    ref = f"Numbers 8:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["John 8:12", "Matthew 5:14", "Hebrews 7:5", "1 Peter 2:9"]

SPECIFIC_REFS["Numbers 8:2"] = ["John 8:12", "Revelation 21:23", "Matthew 5:14", "2 Corinthians 4:6"]
SPECIFIC_REFS["Numbers 8:10"] = ["Acts 6:6", "1 Timothy 4:14", "Acts 13:3", "Hebrews 6:2"]
SPECIFIC_REFS["Numbers 8:17"] = ["Exodus 13:2", "Luke 2:23", "Romans 8:29", "Hebrews 12:23"]

# Num 9 - Second Passover / cloud
SPECIFIC_REFS.update({
    "Numbers 9:1": ["1 Corinthians 5:7", "John 1:29", "Matthew 26:17", "Exodus 12:3"],
    "Numbers 9:2": ["1 Corinthians 5:7", "John 1:29", "Luke 22:14", "Matthew 26:26"],
    "Numbers 9:3": ["1 Corinthians 5:7", "John 19:14", "Matthew 26:17", "Luke 22:7"],
    "Numbers 9:6": ["John 11:55", "Acts 18:21", "Hebrews 11:40", "Luke 2:22"],
    "Numbers 9:9": ["John 7:37", "Acts 2:38", "Revelation 22:17", "Mark 16:16"],
    "Numbers 9:12": ["John 19:36", "Exodus 12:46", "Psalm 34:20", "1 Corinthians 5:7"],
    "Numbers 9:15": ["Exodus 13:21", "1 Corinthians 10:1", "Hebrews 9:8", "John 14:6"],
    "Numbers 9:17": ["Psalm 78:14", "Exodus 13:21", "1 Corinthians 10:1", "John 16:13"],
    "Numbers 9:22": ["Psalm 78:14", "Exodus 13:21", "1 Corinthians 10:1", "Acts 8:29"],
})
for v in range(1, 23):
    ref = f"Numbers 9:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 5:7", "John 1:29", "Exodus 13:21", "1 Corinthians 10:1"]

# Num 10 - Silver trumpets / departure
for v in range(1, 26):
    ref = f"Numbers 10:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Thessalonians 4:16", "Revelation 8:2", "Matthew 24:31", "1 Corinthians 15:52"]

SPECIFIC_REFS["Numbers 10:9"] = ["1 Thessalonians 4:16", "Revelation 8:2", "Joshua 6:5", "1 Corinthians 15:52"]
SPECIFIC_REFS["Numbers 10:10"] = ["1 Thessalonians 4:16", "Revelation 8:2", "Psalm 81:3", "Numbers 29:1"]
SPECIFIC_REFS["Numbers 10:29"] = ["Acts 18:9", "John 15:11", "Matthew 9:37", "Luke 10:2"]
SPECIFIC_REFS["Numbers 10:33"] = ["Revelation 11:19", "Jeremiah 3:16", "Hebrews 9:4", "1 Kings 8:6"]
SPECIFIC_REFS["Numbers 10:35"] = ["Psalm 68:1", "Psalm 132:8", "2 Chronicles 6:41", "John 16:33"]

# Num 11 - Complaint / quail / manna
SPECIFIC_REFS.update({
    "Numbers 11:4": ["1 Corinthians 10:6", "Psalm 78:18", "1 Corinthians 10:10", "Jude 1:16"],
    "Numbers 11:6": ["John 6:35", "Matthew 4:4", "Deuteronomy 8:3", "John 4:14"],
    "Numbers 11:9": ["John 6:31", "Exodus 16:13", "Psalm 78:24", "John 6:50"],
    "Numbers 11:17": ["John 20:22", "Acts 2:33", "John 16:13", "1 Corinthians 12:4"],
    "Numbers 11:25": ["Joel 2:28", "Acts 2:17", "1 Corinthians 12:10", "Numbers 12:6"],
    "Numbers 11:29": ["Joel 2:28", "Acts 2:17", "1 Corinthians 14:1", "Romans 8:9"],
    "Numbers 11:31": ["Psalm 78:27", "1 Corinthians 10:5", "Exodus 16:13", "Psalm 106:15"],
    "Numbers 11:33": ["1 Corinthians 10:5", "Psalm 78:31", "Romans 1:24", "Hebrews 3:17"],
})
for v in range(1, 45):
    ref = f"Numbers 11:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 10:6", "John 6:31", "Psalm 78:18", "Hebrews 3:17"]

# Num 12 - Miriam, Aaron vs Moses
SPECIFIC_REFS.update({
    "Numbers 12:1": ["Galatians 3:28", "Acts 17:26", "Romans 3:22", "Colossians 3:11"],
    "Numbers 12:3": ["Matthew 5:5", "Matthew 11:29", "James 4:6", "1 Peter 5:5"],
    "Numbers 12:6": ["Acts 2:17", "Joel 2:28", "Hebrews 1:1", "1 Corinthians 12:10"],
    "Numbers 12:7": ["Hebrews 3:5", "Hebrews 3:2", "1 Timothy 3:15", "Acts 7:38"],
    "Numbers 12:8": ["1 Corinthians 13:12", "2 Corinthians 3:18", "John 1:14", "Hebrews 1:3"],
    "Numbers 12:10": ["2 Kings 5:27", "Luke 17:12", "Mark 1:40", "Revelation 3:4"],
    "Numbers 12:12": ["Job 3:16", "Psalm 22:6", "Isaiah 53:3", "Romans 6:13"],
    "Numbers 12:13": ["Matthew 8:2", "Luke 5:12", "James 5:14", "Acts 28:8"],
    "Numbers 12:14": ["John 11:50", "Hebrews 13:12", "Numbers 5:3", "Leviticus 13:46"],
})
for v in range(1, 59):
    ref = f"Numbers 12:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 3:5", "Acts 2:17", "Matthew 5:5", "1 Corinthians 10:11"]

# Num 13-14 - Spies / unbelief (MAJOR Christological section)
SPECIFIC_REFS.update({
    "Numbers 13:1": ["Hebrews 3:19", "1 Corinthians 10:5", "Deuteronomy 1:21", "Joshua 2:1"],
    "Numbers 13:16": ["Deuteronomy 18:15", "Acts 7:45", "Hebrews 4:8", "Matthew 1:21"],
    "Numbers 13:20": ["John 4:35", "Matthew 9:37", "Luke 10:2", "Revelation 14:15"],
    "Numbers 13:23": ["John 15:5", "Deuteronomy 8:8", "Amos 9:13", "Revelation 7:9"],
    "Numbers 13:27": ["Deuteronomy 8:7", "John 4:35", "Exodus 3:8", "Ezekiel 20:6"],
    "Numbers 13:30": ["Philippians 4:13", "Hebrews 11:1", "Romans 8:31", "1 Corinthians 15:57"],
    "Numbers 13:33": ["Genesis 6:4", "Isaiah 40:22", "Psalm 22:6", "Luke 18:27"],
    "Numbers 14:2": ["1 Corinthians 10:10", "Philippians 2:14", "Jude 1:16", "Psalm 106:25"],
    "Numbers 14:4": ["Acts 7:39", "John 6:66", "Luke 9:62", "Revelation 2:5"],
    "Numbers 14:9": ["Deuteronomy 31:6", "Hebrews 13:5", "Romans 8:31", "Joshua 1:9"],
    "Numbers 14:11": ["Hebrews 3:18", "Matthew 17:17", "Mark 9:19", "John 20:27"],
    "Numbers 14:18": ["Exodus 34:6", "Romans 9:15", "Psalm 103:8", "Micah 7:18"],
    "Numbers 14:19": ["1 John 1:9", "Matthew 6:12", "Luke 11:4", "Psalm 51:1"],
    "Numbers 14:20": ["Luke 7:9", "Matthew 8:10", "Hebrews 11:6", "Romans 4:3"],
    "Numbers 14:21": ["Isaiah 6:3", "Habakkuk 2:14", "Revelation 4:8", "Numbers 14:28"],
    "Numbers 14:22": ["Psalm 95:8", "Hebrews 3:8", "Matthew 12:39", "Acts 7:51"],
    "Numbers 14:23": ["Hebrews 3:11", "Psalm 95:11", "Luke 13:24", "Matthew 7:14"],
    "Numbers 14:24": ["Romans 8:14", "Galatians 5:25", "Colossians 1:10", "Hebrews 11:6"],
    "Numbers 14:29": ["Hebrews 3:17", "1 Corinthians 10:5", "Jude 1:5", "Psalm 106:26"],
    "Numbers 14:30": ["Hebrews 4:8", "Acts 7:45", "Joshua 1:6", "Deuteronomy 31:7"],
    "Numbers 14:34": ["Ezekiel 4:6", "Daniel 9:24", "Luke 4:2", "Hebrews 3:17"],
    "Numbers 14:36": ["James 3:6", "Proverbs 18:21", "1 Corinthians 10:10", "Romans 16:17"],
})
for v in range(1, 48):
    ref = f"Numbers 13:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 3:18", "1 Corinthians 10:5", "Joshua 2:1", "Deuteronomy 1:22"]
for v in range(1, 37):
    ref = f"Numbers 14:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 3:18", "1 Corinthians 10:10", "Psalm 95:11", "Jude 1:5"]

# Num 15 - Various laws
for v in range(1, 36):
    ref = f"Numbers 15:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 10:1", "Romans 12:1", "Colossians 2:17", "Galatians 3:24"]

SPECIFIC_REFS["Numbers 15:15"] = ["Galatians 3:28", "Romans 2:11", "Acts 10:34", "Colossians 3:11"]
SPECIFIC_REFS["Numbers 15:30"] = ["Hebrews 10:26", "1 John 5:16", "Matthew 12:31", "Mark 3:28"]
SPECIFIC_REFS["Numbers 15:37"] = ["Matthew 23:5", "Deuteronomy 22:12", "Luke 8:44", "Matthew 14:36"]
SPECIFIC_REFS["Numbers 15:38"] = ["Matthew 23:5", "Deuteronomy 22:12", "Zechariah 8:23", "Matthew 9:20"]
SPECIFIC_REFS["Numbers 15:39"] = ["Deuteronomy 6:25", "Proverbs 3:1", "1 John 2:16", "2 Peter 2:18"]
SPECIFIC_REFS["Numbers 15:40"] = ["1 Peter 1:16", "1 Thessalonians 4:7", "Hebrews 12:14", "Leviticus 19:2"]

# Num 16 - Korah's rebellion
SPECIFIC_REFS.update({
    "Numbers 16:1": ["Jude 1:11", "Acts 5:1", "1 Timothy 6:4", "Hebrews 13:17"],
    "Numbers 16:3": ["Jude 1:11", "James 4:11", "Romans 14:4", "Hebrews 13:17"],
    "Numbers 16:5": ["2 Timothy 2:19", "John 10:14", "Matthew 7:23", "Psalm 1:6"],
    "Numbers 16:9": ["1 Peter 2:9", "Hebrews 7:25", "Romans 12:1", "John 17:19"],
    "Numbers 16:11": ["Matthew 10:40", "John 13:20", "Luke 10:16", "Hebrews 13:17"],
    "Numbers 16:22": ["Hebrews 12:9", "Acts 17:28", "Zechariah 12:1", "1 Corinthians 15:45"],
    "Numbers 16:28": ["John 5:30", "John 12:49", "John 14:10", "Matthew 21:25"],
    "Numbers 16:30": ["Revelation 20:14", "Matthew 10:28", "Hebrews 10:31", "Luke 16:23"],
    "Numbers 16:32": ["Revelation 12:9", "Jude 1:11", "Luke 21:19", "Proverbs 14:12"],
    "Numbers 16:35": ["Hebrews 12:29", "Revelation 20:14", "Matthew 3:11", "Jude 1:7"],
    "Numbers 16:41": ["1 Corinthians 10:10", "Philippians 2:14", "Jude 1:16", "Psalm 106:25"],
    "Numbers 16:46": ["Revelation 8:3", "Psalm 141:2", "Hebrews 7:25", "Romans 8:34"],
    "Numbers 16:48": ["Hebrews 7:25", "Romans 8:34", "1 John 2:1", "Hebrews 9:15"],
})
for v in range(1, 33):
    ref = f"Numbers 16:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Jude 1:11", "Hebrews 13:17", "1 Corinthians 10:10", "2 Timothy 2:19"]

# Num 17 - Aaron's rod buds
SPECIFIC_REFS.update({
    "Numbers 17:1": ["Hebrews 9:4", "Hebrews 7:11", "Psalm 110:4", "1 Corinthians 15:20"],
    "Numbers 17:2": ["Hebrews 7:14", "Revelation 5:5", "Hebrews 9:4", "Colossians 2:15"],
    "Numbers 17:5": ["Hebrews 5:4", "Hebrews 7:28", "John 3:27", "Acts 1:7"],
    "Numbers 17:8": ["Isaiah 11:1", "Romans 1:4", "Revelation 22:16", "1 Corinthians 15:20"],
    "Numbers 17:10": ["Hebrews 9:4", "Revelation 2:7", "Romans 1:4", "1 Corinthians 15:20"],
    "Numbers 17:12": ["Hebrews 10:31", "Hebrews 3:17", "1 Corinthians 10:5", "Luke 13:3"],
    "Numbers 17:13": ["Hebrews 9:27", "Romans 5:12", "Hebrews 2:14", "1 Corinthians 15:22"],
})
for v in range(1, 27):
    ref = f"Numbers 17:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 9:4", "Isaiah 11:1", "Romans 1:4", "1 Corinthians 15:20"]

# Num 18 - Priests and Levites
for v in range(1, 36):
    ref = f"Numbers 18:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 7:5", "1 Corinthians 9:13", "1 Peter 2:9", "1 Timothy 5:17"]

SPECIFIC_REFS["Numbers 18:20"] = ["Psalm 16:5", "Lamentations 3:24", "Colossians 1:12", "Deuteronomy 10:9"]
SPECIFIC_REFS["Numbers 18:21"] = ["Hebrews 7:5", "Malachi 3:10", "Matthew 23:23", "1 Corinthians 9:13"]
SPECIFIC_REFS["Numbers 18:25"] = ["Hebrews 7:9", "Genesis 14:20", "Malachi 3:10", "Luke 11:42"]

# Num 19 - Red heifer
for v in range(1, 30):
    ref = f"Numbers 19:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 9:13", "Hebrews 9:14", "Titus 3:5", "1 Peter 1:2"]

SPECIFIC_REFS["Numbers 19:2"] = ["Hebrews 9:13", "1 Peter 1:19", "John 1:29", "Hebrews 9:14"]
SPECIFIC_REFS["Numbers 19:9"] = ["Hebrews 9:13", "Hebrews 9:14", "Titus 3:5", "1 John 1:7"]
SPECIFIC_REFS["Numbers 19:11"] = ["John 11:25", "Hebrews 2:14", "Romans 6:23", "Hebrews 9:14"]
SPECIFIC_REFS["Numbers 19:13"] = ["Hebrews 10:29", "Hebrews 9:14", "Matthew 5:23", "John 13:8"]
SPECIFIC_REFS["Numbers 19:17"] = ["John 4:14", "John 7:37", "Ephesians 5:26", "Titus 3:5"]
SPECIFIC_REFS["Numbers 19:21"] = ["Hebrews 9:13", "Hebrews 9:14", "Romans 12:1", "1 Peter 1:2"]

# Num 20 - Water from rock / Moses' sin
SPECIFIC_REFS.update({
    "Numbers 20:1": ["Acts 7:36", "Exodus 17:1", "Deuteronomy 33:8", "Psalm 81:7"],
    "Numbers 20:2": ["1 Corinthians 10:4", "John 4:14", "John 7:37", "Exodus 17:2"],
    "Numbers 20:4": ["Matthew 10:6", "John 10:28", "Psalm 79:13", "Isaiah 40:11"],
    "Numbers 20:5": ["John 6:31", "Exodus 16:14", "Psalm 78:24", "1 Corinthians 10:3"],
    "Numbers 20:6": ["Revelation 5:8", "Acts 1:14", "Matthew 26:39", "John 11:32"],
    "Numbers 20:8": ["1 Corinthians 10:4", "John 4:14", "John 7:37", "Revelation 22:17"],
    "Numbers 20:10": ["Matthew 5:22", "Ephesians 4:26", "James 1:19", "Proverbs 16:32"],
    "Numbers 20:11": ["1 Corinthians 10:4", "Psalm 78:15", "Psalm 105:41", "Isaiah 48:21"],
    "Numbers 20:12": ["Romans 3:3", "Hebrews 3:18", "Matthew 17:20", "1 Corinthians 10:6"],
    "Numbers 20:13": ["Psalm 81:7", "Deuteronomy 33:8", "Exodus 17:7", "Hebrews 3:8"],
    "Numbers 20:24": ["Hebrews 3:16", "1 Corinthians 10:5", "Deuteronomy 32:51", "Romans 5:12"],
})
for v in range(1, 31):
    ref = f"Numbers 20:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 10:4", "John 4:14", "Hebrews 3:18", "Romans 5:12"]

# Num 21 - Bronze serpent (MAJOR)
SPECIFIC_REFS.update({
    "Numbers 21:1": ["Acts 7:36", "1 Corinthians 10:9", "Deuteronomy 8:2", "Hebrews 3:17"],
    "Numbers 21:4": ["1 Corinthians 10:9", "Hebrews 3:8", "Psalm 95:8", "Jude 1:5"],
    "Numbers 21:5": ["1 Corinthians 10:10", "Philippians 2:14", "Jude 1:16", "Psalm 106:25"],
    "Numbers 21:6": ["1 Corinthians 10:9", "Hebrews 3:17", "Jude 1:5", "Psalm 78:31"],
    "Numbers 21:7": ["James 5:14", "Acts 28:8", "1 John 1:9", "Luke 15:18"],
    "Numbers 21:8": ["John 3:14", "Galatians 3:13", "Isaiah 45:22", "2 Kings 18:4"],
    "Numbers 21:9": ["John 3:14", "John 12:32", "Galatians 3:13", "Romans 5:8"],
    "Numbers 21:17": ["John 4:14", "John 7:38", "Isaiah 12:3", "Revelation 22:17"],
    "Numbers 21:18": ["John 4:14", "Isaiah 12:3", "Proverbs 9:1", "Ephesians 2:20"],
    "Numbers 21:34": ["Deuteronomy 3:2", "Joshua 10:8", "Romans 8:31", "Hebrews 13:6"],
})
for v in range(1, 58):
    ref = f"Numbers 21:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["John 3:14", "1 Corinthians 10:9", "Hebrews 3:17", "Galatians 3:13"]

# Num 22-24 - Balaam
balaam_default = ["2 Peter 2:15", "Jude 1:11", "Revelation 2:14", "Romans 11:29"]
for ch in [22, 23, 24]:
    chap_len = NUMBERS_CHAPTERS[ch]
    for v in range(1, chap_len + 1):
        ref = f"Numbers {ch}:{v}"
        if ref not in SPECIFIC_REFS:
            SPECIFIC_REFS[ref] = balaam_default

SPECIFIC_REFS["Numbers 22:28"] = ["2 Peter 2:16", "Matthew 21:16", "Luke 19:40", "Acts 9:4"]
SPECIFIC_REFS["Numbers 22:32"] = ["2 Peter 2:15", "James 4:6", "Proverbs 16:9", "Hebrews 4:13"]
SPECIFIC_REFS["Numbers 23:19"] = ["Hebrews 6:18", "Titus 1:2", "1 Samuel 15:29", "Romans 3:4"]
SPECIFIC_REFS["Numbers 23:21"] = ["Zephaniah 3:17", "Romans 8:33", "Revelation 21:3", "Isaiah 43:5"]
SPECIFIC_REFS["Numbers 24:2"] = ["Acts 2:17", "Joel 2:28", "1 Samuel 10:10", "Numbers 11:25"]
SPECIFIC_REFS["Numbers 24:7"] = ["Matthew 2:2", "Revelation 17:14", "Revelation 19:16", "Micah 5:2"]
SPECIFIC_REFS["Numbers 24:17"] = ["Matthew 2:2", "Revelation 22:16", "Luke 1:78", "2 Peter 1:19"]
SPECIFIC_REFS["Numbers 24:19"] = ["Micah 5:2", "Matthew 2:6", "Revelation 17:14", "Revelation 19:16"]

# Num 25 - Phinehas
SPECIFIC_REFS.update({
    "Numbers 25:1": ["1 Corinthians 10:8", "Revelation 2:14", "1 Peter 2:11", "Galatians 5:19"],
    "Numbers 25:2": ["Revelation 2:14", "1 Corinthians 10:20", "Acts 15:29", "Deuteronomy 4:3"],
    "Numbers 25:3": ["Deuteronomy 4:3", "1 Corinthians 10:8", "Psalm 106:28", "Revelation 2:14"],
    "Numbers 25:8": ["Psalm 106:30", "Romans 12:1", "Galatians 2:20", "1 Peter 4:1"],
    "Numbers 25:11": ["Psalm 106:30", "Romans 10:2", "Galatians 4:18", "John 2:17"],
    "Numbers 25:12": ["Malachi 2:5", "Isaiah 54:10", "John 14:27", "Ezekiel 34:25"],
    "Numbers 25:13": ["Psalm 106:31", "Romans 4:22", "James 2:23", "Hebrews 11:5"],
})
for v in range(1, 33):
    ref = f"Numbers 25:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["1 Corinthians 10:8", "Revelation 2:14", "Psalm 106:30", "Galatians 5:19"]

# Num 26 - Second census
for v in range(1, 23):
    ref = f"Numbers 26:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Revelation 7:4", "Galatians 3:29", "Romans 9:7", "Luke 2:1"]

SPECIFIC_REFS["Numbers 26:10"] = ["Jude 1:11", "1 Corinthians 10:6", "Hebrews 3:17", "2 Peter 2:6"]
SPECIFIC_REFS["Numbers 26:11"] = ["Romans 9:6", "John 10:28", "Ezekiel 18:20", "2 Kings 14:6"]
SPECIFIC_REFS["Numbers 26:14"] = ["Hebrews 3:17", "1 Corinthians 10:5", "Psalm 106:26", "Jude 1:5"]

# Num 27 - Joshua appointed
SPECIFIC_REFS.update({
    "Numbers 27:1": ["Acts 7:45", "Joshua 17:3", "Galatians 3:29", "Luke 15:12"],
    "Numbers 27:4": ["Galatians 3:29", "Acts 13:33", "Romans 8:17", "Hebrews 1:2"],
    "Numbers 27:16": ["Hebrews 12:9", "Acts 17:28", "Zechariah 12:1", "John 10:10"],
    "Numbers 27:17": ["John 10:11", "Matthew 9:36", "Hebrews 13:20", "Mark 6:34"],
    "Numbers 27:18": ["Acts 6:6", "Acts 13:3", "Deuteronomy 34:9", "2 Timothy 1:6"],
    "Numbers 27:20": ["John 17:22", "2 Corinthians 3:18", "Romans 8:30", "Acts 7:45"],
    "Numbers 27:21": ["Acts 1:24", "John 16:13", "Matthew 4:1", "Acts 13:2"],
    "Numbers 27:22": ["Matthew 21:6", "John 15:14", "Acts 6:6", "1 Thessalonians 4:7"],
    "Numbers 27:23": ["Acts 6:6", "1 Timothy 4:14", "Acts 13:3", "Hebrews 6:2"],
})
for v in range(1, 30):
    ref = f"Numbers 27:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Acts 7:45", "Hebrews 4:8", "Galatians 3:29", "Romans 8:17"]

# Num 28-29 - Offerings schedule
for ch in [28, 29]:
    chap_len = NUMBERS_CHAPTERS[ch]
    for v in range(1, chap_len + 1):
        ref = f"Numbers {ch}:{v}"
        if ref not in SPECIFIC_REFS:
            SPECIFIC_REFS[ref] = ["Hebrews 10:1", "Romans 12:1", "Colossians 2:17", "Ephesians 5:2"]

SPECIFIC_REFS["Numbers 28:2"] = ["Romans 12:1", "Philippians 4:18", "Ephesians 5:2", "Hebrews 13:16"]
SPECIFIC_REFS["Numbers 28:3"] = ["Hebrews 10:11", "Hebrews 7:27", "Hebrews 9:26", "John 1:29"]
SPECIFIC_REFS["Numbers 28:9"] = ["Matthew 12:5", "Colossians 2:16", "John 5:17", "Hebrews 4:9"]
SPECIFIC_REFS["Numbers 28:16"] = ["1 Corinthians 5:7", "John 1:29", "Matthew 26:17", "John 19:14"]
SPECIFIC_REFS["Numbers 29:1"] = ["1 Thessalonians 4:16", "Revelation 8:2", "Matthew 24:31", "1 Corinthians 15:52"]
SPECIFIC_REFS["Numbers 29:7"] = ["Hebrews 9:7", "Acts 27:9", "Romans 3:25", "Hebrews 10:3"]

# Num 30 - Vows
for v in range(1, 37):
    ref = f"Numbers 30:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Matthew 5:33", "James 5:12", "Ecclesiastes 5:4", "Numbers 23:19"]

SPECIFIC_REFS["Numbers 30:2"] = ["Matthew 5:33", "James 5:12", "Ecclesiastes 5:5", "Psalm 15:4"]

# Num 31 - War against Midian
for v in range(1, 25):
    ref = f"Numbers 31:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Revelation 19:11", "1 Corinthians 10:8", "Jude 1:11", "2 Timothy 2:4"]

SPECIFIC_REFS["Numbers 31:8"] = ["2 Peter 2:15", "Jude 1:11", "Revelation 2:14", "Joshua 13:22"]
SPECIFIC_REFS["Numbers 31:16"] = ["Revelation 2:14", "2 Peter 2:15", "1 Corinthians 10:8", "Jude 1:11"]
SPECIFIC_REFS["Numbers 31:23"] = ["1 Peter 1:7", "Zechariah 13:9", "Malachi 3:3", "1 Corinthians 3:13"]

# Num 32 - Reuben and Gad's request
for v in range(1, 47):
    ref = f"Numbers 32:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Luke 9:62", "Hebrews 3:12", "1 Corinthians 10:6", "Colossians 3:2"]

SPECIFIC_REFS["Numbers 32:11"] = ["Hebrews 3:18", "Psalm 95:11", "Numbers 14:30", "Jude 1:5"]
SPECIFIC_REFS["Numbers 32:23"] = ["Galatians 6:7", "Proverbs 13:15", "Hebrews 4:13", "Numbers 14:43"]

# Num 33 - Journey summary
for v in range(1, 22):
    ref = f"Numbers 33:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Acts 7:36", "Hebrews 3:17", "1 Corinthians 10:5", "Deuteronomy 8:2"]

SPECIFIC_REFS["Numbers 33:3"] = ["Exodus 12:51", "1 Corinthians 5:7", "John 8:36", "Galatians 5:1"]
SPECIFIC_REFS["Numbers 33:51"] = ["Deuteronomy 12:2", "Acts 19:19", "1 John 5:21", "Galatians 5:20"]
SPECIFIC_REFS["Numbers 33:53"] = ["Hebrews 4:1", "Colossians 1:12", "Galatians 3:29", "Romans 8:17"]

# Num 34 - Boundaries
for v in range(1, 44):
    ref = f"Numbers 34:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Galatians 3:29", "Romans 8:17", "Hebrews 4:1", "Ezekiel 47:13"]

SPECIFIC_REFS["Numbers 34:2"] = ["Galatians 3:29", "Acts 7:5", "Hebrews 11:8", "Romans 4:13"]

# Num 35 - Cities of refuge
SPECIFIC_REFS.update({
    "Numbers 35:6": ["Hebrews 6:18", "John 10:9", "Psalm 46:1", "Romans 8:1"],
    "Numbers 35:9": ["Hebrews 6:18", "Romans 8:1", "Psalm 46:1", "Deuteronomy 19:2"],
    "Numbers 35:11": ["Hebrews 6:18", "John 10:9", "Romans 8:1", "Acts 4:12"],
    "Numbers 35:12": ["Romans 8:1", "John 3:18", "Romans 8:33", "Hebrews 9:15"],
    "Numbers 35:15": ["Romans 3:29", "Galatians 3:28", "Acts 10:34", "Revelation 7:9"],
    "Numbers 35:25": ["Romans 8:33", "Hebrews 9:15", "1 John 2:1", "Romans 8:1"],
    "Numbers 35:28": ["Romans 8:1", "Galatians 3:13", "Hebrews 9:15", "Colossians 2:14"],
    "Numbers 35:30": ["Deuteronomy 17:6", "Matthew 18:16", "John 8:17", "2 Corinthians 13:1"],
    "Numbers 35:31": ["1 Timothy 2:5", "Hebrews 9:15", "Romans 8:33", "Matthew 20:28"],
    "Numbers 35:33": ["Genesis 9:6", "Romans 13:4", "Hebrews 9:22", "Leviticus 17:11"],
})
for v in range(1, 30):
    ref = f"Numbers 35:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Hebrews 6:18", "Romans 8:1", "John 10:9", "Acts 4:12"]

# Num 36 - Inheritance
for v in range(1, 54):
    ref = f"Numbers 36:{v}"
    if ref not in SPECIFIC_REFS:
        SPECIFIC_REFS[ref] = ["Galatians 3:29", "Romans 8:17", "Colossians 1:12", "Ephesians 1:11"]

SPECIFIC_REFS["Numbers 36:7"] = ["Galatians 3:29", "Romans 8:17", "Ephesians 1:11", "1 Peter 1:4"]
SPECIFIC_REFS["Numbers 36:9"] = ["Romans 8:17", "Galatians 3:29", "1 Peter 1:4", "Hebrews 9:15"]


# ============================================================
# Build all entries
# ============================================================
def build_entries():
    entries = {}
    # Leviticus
    for ch, max_v in LEVITICUS_CHAPTERS.items():
        for v in range(1, max_v + 1):
            key = f"Leviticus {ch}:{v}"
            if key in SPECIFIC_REFS:
                entries[key] = SPECIFIC_REFS[key]
            else:
                # Generic fallback by book theme
                entries[key] = ["Hebrews 10:1", "Colossians 2:17", "Romans 12:1", "1 Peter 1:16"]
    # Numbers
    for ch, max_v in NUMBERS_CHAPTERS.items():
        for v in range(1, max_v + 1):
            key = f"Numbers {ch}:{v}"
            if key in SPECIFIC_REFS:
                entries[key] = SPECIFIC_REFS[key]
            else:
                entries[key] = ["Hebrews 3:17", "1 Corinthians 10:6", "Romans 15:4", "Galatians 3:24"]
    return entries


if __name__ == "__main__":
    new_entries = build_entries()
    
    # Load existing JSON
    with open("/Users/adamjohns/bible-reading-plan-bot/docs/assets/cross-references.json", "r") as f:
        data = json.load(f)
    
    # Check overlap
    existing_keys = set(data.keys())
    new_keys = set(new_entries.keys())
    overlap = existing_keys & new_keys
    
    print(f"Existing entries: {len(data)}")
    print(f"New entries to add: {len(new_entries)}")
    print(f"Overlap (already exist): {len(overlap)}")
    print(f"Net new: {len(new_entries) - len(overlap)}")
    
    # Merge — don't overwrite existing
    added = 0
    for key, refs in new_entries.items():
        if key not in data:
            data[key] = refs
            added += 1
    
    print(f"Actually added: {added}")
    print(f"Total after merge: {len(data)}")
    
    # Save
    with open("/Users/adamjohns/bible-reading-plan-bot/docs/assets/cross-references.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Saved!")
