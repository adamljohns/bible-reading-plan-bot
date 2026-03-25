#!/usr/bin/env python3
"""
BTE Cross-Reference Expander - Romans 9-13 & 1Cor 2-9
Focus: OT→NT Christological links, deepen verses at exactly 3 refs
"""
import json, sys

DATA_PATH = "/Users/adamjohns/bible-reading-plan-bot/docs/assets/cross-references.json"

# New refs to add — key = verse, value = list of refs to append (only if not already present)
# Format: "bookId_chapter_verse" (strings only!)
ADDITIONS = {
    # ===== ROMANS 9 =====
    # 9:5 Christ who is God over all — Col 1:15, Heb 1:3
    "45_9_5": ["51_1_15", "58_1_3"],
    # 9:6 not all Israel are Israel — John 1:12-13, Gal 3:29
    "45_9_6": ["43_1_12", "48_3_29"],
    # 9:7 children of Abraham — Isa 41:8, Heb 11:18
    "45_9_7": ["23_41_8", "58_11_18"],
    # 9:8 children of promise = children of God — Gal 3:26, John 11:52
    "45_9_8": ["48_3_26", "43_11_52"],
    # 9:9 promise to Sarah — Heb 11:11, Gen 21:2
    "45_9_9": ["58_11_11", "1_21_2"],
    # 9:10 before born or done anything — Gen 25:22, Acts 4:28
    "45_9_10": ["1_25_22", "44_4_28"],
    # 9:13 Jacob I loved Esau hated — Mal 1:2-3, Heb 12:16
    "45_9_13": ["39_1_3", "58_12_16"],
    # 9:15 I will have mercy — Ex 33:19, Heb 4:16
    "45_9_15": ["2_33_19", "58_4_16"],
    # 9:17 raised up Pharaoh — Ex 9:16, Isa 45:1
    "45_9_17": ["2_9_16", "23_45_1"],
    # 9:19 who resists his will — Job 9:12, Dan 4:35
    "45_9_19": ["18_9_12", "27_4_35"],
    # 9:20 O man who are you — Job 33:12, Isa 29:16
    "45_9_20": ["18_33_12", "23_29_16"],
    # 9:22 vessels of wrath endured — Ezek 18:23, Jer 18:11
    "45_9_22": ["26_18_23", "24_18_11"],
    # 9:25 Hosea — you are my people — 1Pet 2:10, Hos 2:23
    "45_9_25": ["60_2_10", "28_2_23"],
    # 9:26 sons of living God — John 1:12, 1John 3:1
    "45_9_26": ["43_1_12", "62_3_1"],
    # 9:27 remnant saved — Rev 7:4, Amos 5:15
    "45_9_27": ["66_7_4", "30_5_15"],
    # 9:33 stumbling stone cornerstone — 1Pet 2:6, Eph 2:20
    "45_9_33": ["60_2_6", "49_2_20"],

    # ===== ROMANS 10 =====
    # 10:4 Christ end of law → Isa 53:11, Matt 5:17
    "45_10_4": ["23_53_11", "40_5_17"],
    # 10:6 do not say who will ascend — Eph 4:9, John 3:13
    "45_10_6": ["49_4_9", "43_3_13"],
    # 10:8 word near you — Isa 55:11, Acts 10:36
    "45_10_8": ["23_55_11", "44_10_36"],
    # 10:9 confess Jesus Lord — Phil 2:11, Acts 2:36
    "45_10_9": ["50_2_11", "44_2_36"],
    # 10:10 heart believes, mouth confesses — Isa 45:23, Matt 12:34
    "45_10_10": ["23_45_23", "40_12_34"],
    # 10:11 no one who believes ashamed — 1Pet 2:6, John 11:25
    "45_10_11": ["60_2_6", "43_11_25"],
    # 10:13 call on the Lord — Acts 4:12, Joel 2:32
    "45_10_13": ["44_4_12", "29_2_32"],
    # 10:14 how believe without preaching — Matt 10:7, John 6:44
    "45_10_14": ["40_10_7", "43_6_44"],
    # 10:16 not all obeyed gospel — Acts 28:24, Isa 53:1
    "45_10_16": ["44_28_24", "23_53_1"],
    # 10:17 faith from hearing word of Christ — Matt 13:23, Heb 4:2
    "45_10_17": ["40_13_23", "58_4_2"],
    # 10:18 sound to all earth — Rev 14:6, Col 1:23
    "45_10_18": ["66_14_6", "51_1_23"],
    # 10:19 make Israel jealous — Acts 13:46, Deut 32:21
    "45_10_19": ["44_13_46", "5_32_21"],
    # 10:20 found by those not seeking — Matt 8:11, Isa 65:1
    "45_10_20": ["40_8_11", "23_65_1"],
    # 10:21 hands to disobedient — Luke 13:34, Isa 65:2
    "45_10_21": ["42_13_34", "23_65_2"],

    # ===== ROMANS 11 =====
    # 11:1 God not rejected Israel — Hos 14:1, Gen 50:21
    "45_11_1": ["28_14_1", "1_50_21"],
    # 11:5 remnant by grace — Gal 1:6, Exod 32:32
    "45_11_5": ["48_1_6", "2_32_32"],
    # 11:6 grace not works — Eph 2:8, Gal 3:28
    "45_11_6": ["49_2_8", "48_3_28"],
    # 11:7 Israel hardened — Deut 29:4, Isa 6:9
    "45_11_7": ["5_29_4", "23_6_9"],
    # 11:11 through their fall salvation — Acts 13:46, Deut 32:21
    "45_11_11": ["44_13_46", "5_32_21"],
    # 11:17 olive tree — Rom 4:16, Jer 11:16
    "45_11_17": ["45_4_16", "24_11_16"],
    # 11:22 goodness and severity — Jer 8:6, Heb 3:14
    "45_11_22": ["24_8_6", "58_3_14"],
    # 11:25 hardening of Israel until fullness — Acts 28:27, Isa 29:10
    "45_11_25": ["44_28_27", "23_29_10"],
    # 11:26 all Israel saved — Zech 14:1, Isa 27:9
    "45_11_26": ["38_14_1", "23_27_9"],
    # 11:36 all from him, through him, to him — Col 1:17, Rev 1:8
    "45_11_36": ["51_1_17", "66_1_8"],

    # ===== ROMANS 12 =====
    # 12:1 living sacrifice — Heb 13:15, John 17:19
    "45_12_1": ["58_13_15", "43_17_19"],
    # 12:2 transformed by renewing mind — 2Cor 3:18, Col 3:10
    "45_12_2": ["47_3_18", "51_3_10"],
    # 12:3 sober judgment by faith — Luke 14:11, 1Pet 5:6
    "45_12_3": ["42_14_11", "60_5_6"],
    # 12:4 one body many members — 1Cor 12:27, Eph 4:4
    "45_12_4": ["46_12_27", "49_4_4"],
    # 12:6 gifts according to grace — Eph 4:11, 1Pet 4:10
    "45_12_6": ["49_4_11", "60_4_10"],
    # 12:9 love without hypocrisy — John 13:35, 1Pet 1:22
    "45_12_9": ["43_13_35", "60_1_22"],
    # 12:12 rejoicing in hope — Ps 46:1, Heb 6:19
    "45_12_12": ["19_46_1", "58_6_19"],
    # 12:14 bless persecutors — Ps 109:4, Luke 23:34
    "45_12_14": ["19_109_4", "42_23_34"],
    # 12:18 peace with all — Luke 2:14, Ezek 37:26
    "45_12_18": ["42_2_14", "26_37_26"],
    # 12:19 vengeance is mine — Ps 94:1, Nah 1:2
    "45_12_19": ["19_94_1", "34_1_2"],

    # ===== ROMANS 13 =====
    # 13:1 governing authorities from God — Dan 2:21, John 19:11
    "45_13_1": ["27_2_21", "43_19_11"],
    # 13:4 servant of God for good — Dan 4:17, Prov 21:1
    "45_13_4": ["27_4_17", "20_21_1"],
    # 13:8 owe nothing but love — Ps 119:11, Lev 19:18
    "45_13_8": ["19_119_11", "3_19_18"],
    # 13:11 hour to wake from sleep — Rev 22:20, Phil 4:5
    "45_13_11": ["66_22_20", "50_4_5"],
    # 13:12 armor of light — Isa 59:17, Eph 6:13
    "45_13_12": ["23_59_17", "49_6_13"],
    # 13:14 put on Lord Jesus Christ — Isa 61:10, Col 3:10
    "45_13_14": ["23_61_10", "51_3_10"],

    # ===== 1 CORINTHIANS 2 =====
    # 2:1 not eloquent wisdom — Isa 29:14, John 5:39
    "46_2_1": ["23_29_14", "43_5_39"],
    # 2:6 wisdom of this age passing — Isa 44:25, 1Cor 7:31
    "46_2_6": ["23_44_25", "46_7_31"],
    # 2:7 wisdom in a mystery — Deut 29:29, Col 1:26
    "46_2_7": ["5_29_29", "51_1_26"],
    # 2:9 what no eye has seen — Isa 52:15, Gen 49:18
    "46_2_9": ["23_52_15", "1_49_18"],
    # 2:16 mind of Christ — Phil 2:5, John 15:15
    "46_2_16": ["50_2_5", "43_15_15"],

    # ===== 1 CORINTHIANS 3 =====
    # 3:11 no other foundation — Matt 16:18, John 2:19
    "46_3_11": ["40_16_18", "43_2_19"],
    # 3:16 temple of God — John 2:21, Rev 21:22
    "46_3_16": ["43_2_21", "66_21_22"],
    # 3:21 all things are yours — 1Kings 3:13, Col 1:20
    "46_3_21": ["11_3_13", "51_1_20"],

    # ===== 1 CORINTHIANS 4 =====
    # 4:2 required in stewards — Luke 12:42, 1Tim 1:12
    "46_4_2": ["42_12_42", "54_1_12"],
    # 4:5 judge nothing before time — Matt 13:41, Rev 20:12
    "46_4_5": ["40_13_41", "66_20_12"],
    # 4:20 kingdom of God not talk but power — Luke 17:21, Matt 6:10
    "46_4_20": ["42_17_21", "40_6_10"],

    # ===== 1 CORINTHIANS 5 =====
    # 5:7 Christ our Passover — 1Pet 1:19, Heb 9:14
    "46_5_7": ["60_1_19", "58_9_14"],
    # 5:13 put away evil from among you — Isa 52:11, Lev 18:25
    "46_5_13": ["23_52_11", "3_18_25"],

    # ===== 1 CORINTHIANS 6 =====
    # 6:11 washed sanctified justified — Ps 51:7, Heb 9:14
    "46_6_11": ["19_51_7", "58_9_14"],
    # 6:17 joined to Lord one spirit — Ps 27:4, John 15:4
    "46_6_17": ["19_27_4", "43_15_4"],
    # 6:19 body temple of Holy Spirit — John 14:17, Rev 3:20
    "46_6_19": ["43_14_17", "66_3_20"],
    # 6:20 bought with a price — Isa 43:3, 1Pet 1:18
    "46_6_20": ["23_43_3", "60_1_18"],

    # ===== 1 CORINTHIANS 7 =====
    # 7:10 not I but the Lord (divorce) — Gen 2:24, Mal 2:16
    "46_7_10": ["1_2_24", "39_2_16"],
    # 7:14 unbelieving spouse sanctified — 1Cor 7:5, Gen 17:7
    "46_7_14": ["1_17_7", "46_7_5"],
    # 7:19 obeying commandments — Deut 30:6, Gal 5:6
    "46_7_19": ["5_30_6", "48_5_6"],
    # 7:32 devoted to things of Lord — Ps 73:25, Phil 4:6
    "46_7_32": ["19_73_25", "50_4_6"],
    # 7:34 holy in body and spirit — Ps 131:1, 1Thess 5:23
    "46_7_34": ["19_131_1", "52_5_23"],

    # ===== 1 CORINTHIANS 8 =====
    # 8:4 no god but one — Isa 44:6, Deut 6:4
    "46_8_4": ["23_44_6", "5_6_4"],
    # 8:6 one God one Lord — John 17:3, Col 1:15
    "46_8_6": ["43_17_3", "51_1_15"],
    # 8:11 weak brother for whom Christ died — John 3:16, Isa 53:5
    "46_8_11": ["43_3_16", "23_53_5"],

    # ===== 1 CORINTHIANS 9 =====
    # 9:9 muzzle ox treading — Deut 25:4, 1Tim 5:18
    "46_9_9": ["5_25_4", "54_5_18"],
    # 9:16 woe if I do not preach — Jer 20:9, Ezek 33:8
    "46_9_16": ["24_20_9", "26_33_8"],
    # 9:24 run to win prize — Heb 12:1, Ps 119:32
    "46_9_24": ["58_12_1", "19_119_32"],
    # 9:27 discipline body — Isa 41:3, 2Tim 4:7
    "46_9_27": ["23_41_3", "55_4_7"],
}

def add_refs(data, additions):
    added_count = 0
    verses_updated = 0
    
    for verse_key, new_refs in additions.items():
        if verse_key not in data:
            print(f"  WARNING: {verse_key} not in database, skipping")
            continue
        
        existing = data[verse_key]
        added_here = 0
        for ref in new_refs:
            # Validate format
            if not isinstance(ref, str):
                print(f"  ERROR: ref {ref} is not a string!")
                continue
            parts = ref.split("_")
            if len(parts) != 3:
                print(f"  ERROR: ref {ref} has wrong format!")
                continue
            if ref not in existing:
                existing.append(ref)
                added_count += 1
                added_here += 1
        
        if added_here > 0:
            verses_updated += 1
            
    return added_count, verses_updated

if __name__ == "__main__":
    data = json.load(open(DATA_PATH))
    starting_count = len(data)
    
    print(f"Starting: {starting_count} total entries")
    
    added, verses = add_refs(data, ADDITIONS)
    print(f"Added {added} new refs across {verses} verses")
    
    # Validate no bad refs
    bad = [k for k, v in data.items() for r in v if not isinstance(r, str)]
    print(f"Bad refs (non-string): {len(bad)}")
    if bad:
        print("BAD REFS:", bad[:10])
        sys.exit(1)
    
    # Write back
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    
    print(f"Written to {DATA_PATH}")
    print(f"New total entries: {len(data)}")
