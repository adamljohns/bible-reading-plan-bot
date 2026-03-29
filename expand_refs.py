import json

path = "docs/assets/cross-references.json"
d = json.load(open(path))

def add_refs(verse_key, new_refs):
    existing = set(d.get(verse_key, []))
    added = 0
    for r in new_refs:
        if r not in existing:
            d.setdefault(verse_key, []).append(r)
            existing.add(r)
            added += 1
    return added

total_added = 0

# ==========================================
# 2 PETER (Book 61) - expand low-coverage verses
# ==========================================

# 61_1_6 (patience/self-control in faith progression)
total_added += add_refs("61_1_6", [
    "45_5_3",   # Rom 5:3 - tribulation works patience
    "59_1_3",   # James 1:3 - trying of faith worketh patience
    "58_12_1",  # Heb 12:1 - run with patience
    "66_3_10",  # Rev 3:10 - kept in hour of temptation
])

# 61_1_9 (blind, cannot see afar off - spiritual blindness)
total_added += add_refs("61_1_9", [
    "23_6_10",  # Isa 6:10 - eyes closed, heart fat
    "43_9_25",  # John 9:25 - once blind now see
    "60_2_9",   # 1Pet 2:9 - called out of darkness into light
    "58_9_14",  # Heb 9:14 - purge conscience from dead works
])

# 61_1_13 (stir you up by putting in remembrance)
total_added += add_refs("61_1_13", [
    "43_14_26", # John 14:26 - Holy Spirit will remind you
    "44_2_42",  # Acts 2:42 - steadfast in apostles doctrine
    "52_5_11",  # 1Thess 5:11 - exhort one another
])

# 61_1_15 (Peter about to depart, preserve memory)
total_added += add_refs("61_1_15", [
    "43_21_19", # John 21:19 - what manner of death to glorify God
    "50_3_20",  # Phil 3:20 - citizenship in heaven
    "51_1_13",  # Col 1:13 - delivered from domain of darkness
    "55_4_7",   # 2Tim 4:7 - I have finished the race
])

# 61_1_18 (Transfiguration - holy mountain - voice from heaven)
total_added += add_refs("61_1_18", [
    "40_17_5",  # Matt 17:5 - This is my beloved Son
    "19_48_1",  # Ps 48:1 - great is the Lord in holy mountain
    "23_2_2",   # Isa 2:2 - mountain of the Lord established
    "27_7_13",  # Dan 7:13 - Son of Man coming in clouds
])

# 61_1_19 (prophetic word, lamp shining in dark place)
total_added += add_refs("61_1_19", [
    "19_19_8",  # Ps 19:8 - commandment pure, enlightening eyes
    "60_1_10",  # 1Pet 1:10 - prophets searched this salvation
    "43_5_35",  # John 5:35 - burning and shining lamp
])

# 61_1_21 (prophecy not by will of man, Spirit moved)
total_added += add_refs("61_1_21", [
    "54_3_16",  # 2Tim 3:16 - all Scripture God-breathed
    "38_7_12",  # Zech 7:12 - words Spirit sent by prophets
    "24_1_9",   # Jer 1:9 - put words in mouth
    "47_3_17",  # 2Cor 3:17 - Lord is the Spirit
])

# 61_2_2 (blaspheme the way of truth)
total_added += add_refs("61_2_2", [
    "44_9_2",   # Acts 9:2 - the Way (early name for Christians)
    "45_1_25",  # Rom 1:25 - changed truth for a lie
    "60_2_8",   # 1Pet 2:8 - stumble at the word
])

# 61_2_8 (righteous Lot vexed by wickedness of Sodom)
total_added += add_refs("61_2_8", [
    "1_19_1",   # Gen 19:1 - Lot sat in gate of Sodom
    "23_57_1",  # Isa 57:1 - the righteous perishes
    "19_97_10", # Ps 97:10 - love Lord, hate evil
    "45_7_24",  # Rom 7:24 - wretched man that I am
])

# 61_2_12 (natural brute beasts, made to be taken/destroyed)
total_added += add_refs("61_2_12", [
    "19_32_9",  # Ps 32:9 - be not as horse/mule without understanding
    "20_7_22",  # Prov 7:22 - ox to slaughter
    "26_34_2",  # Ezek 34:2 - woe to shepherds of Israel
])

# 61_2_14 (eyes full of adultery, insatiable for sin)
total_added += add_refs("61_2_14", [
    "18_31_1",  # Job 31:1 - covenant with my eyes
    "62_2_16",  # 1John 2:16 - lust of the eyes
    "40_6_22",  # Matt 6:22 - eye is lamp of the body
])

# 61_2_17 (wells without water, clouds driven by storm)
total_added += add_refs("61_2_17", [
    "43_4_14",  # John 4:14 - water springing to eternal life
    "29_2_28",  # Joel 2:28 - pour out Spirit like latter rain
    "19_1_3",   # Ps 1:3 - tree planted by rivers of water
])

# 61_2_18 (great swelling words of vanity)
total_added += add_refs("61_2_18", [
    "65_1_16",  # Jude 1:16 - great swelling words
    "27_11_36", # Dan 11:36 - king exalts himself above every god
    "19_12_3",  # Ps 12:3 - cut off flattering lips/boastful tongue
])

# 61_2_20 (escaped pollutions, entangled again, worse state)
total_added += add_refs("61_2_20", [
    "43_8_34",  # John 8:34 - everyone who sins is slave to sin
    "48_4_9",   # Gal 4:9 - turning back to weak/beggarly elements
    "45_6_16",  # Rom 6:16 - slaves to whom you obey
])

# 61_3_1 (stir up pure minds by way of reminder)
total_added += add_refs("61_3_1", [
    "58_10_24", # Heb 10:24 - stir up one another to love
    "44_20_31", # Acts 20:31 - warning everyone night and day
    "52_5_11",  # 1Thess 5:11 - encourage one another
])

# 61_3_4 (where is promise of His coming? scoffers)
total_added += add_refs("61_3_4", [
    "42_18_8",  # Luke 18:8 - when Son of Man comes, find faith?
    "60_4_17",  # 1Pet 4:17 - judgment begins at house of God
    "23_5_19",  # Isa 5:19 - let Him hasten His work
])

# 61_3_14 (diligent, without spot, blameless in peace)
total_added += add_refs("61_3_14", [
    "60_1_16",  # 1Pet 1:16 - be holy for I am holy
    "43_17_17", # John 17:17 - sanctify them through truth
    "58_12_14", # Heb 12:14 - pursue peace and holiness
    "49_1_4",   # Eph 1:4 - chosen holy and blameless
])

# 61_3_16 (Paul's letters hard to understand)
total_added += add_refs("61_3_16", [
    "43_6_60",  # John 6:60 - this is a hard saying
    "23_28_9",  # Isa 28:9 - whom will he teach knowledge?
    "44_8_30",  # Acts 8:30 - do you understand what you read?
])

# ==========================================
# TITUS (Book 56) - expand low-coverage verses
# ==========================================

# 56_1_5 (ordain elders in every city)
total_added += add_refs("56_1_5", [
    "44_20_17", # Acts 20:17 - elders of church at Ephesus
    "60_5_1",   # 1Pet 5:1 - exhort elders among you
    "4_11_16",  # Num 11:16 - seventy elders of Israel
])

# 56_2_3 (aged women to be holy in behavior)
total_added += add_refs("56_2_3", [
    "20_31_30", # Prov 31:30 - woman who fears Lord praised
    "54_2_9",   # 1Tim 2:9 - modest apparel for women
    "19_45_13", # Ps 45:13 - king's daughter glorious within
])

# 56_2_5 (keepers at home, obedient to husbands)
total_added += add_refs("56_2_5", [
    "1_3_16",   # Gen 3:16 - desire toward husband
    "49_5_33",  # Eph 5:33 - wife reverence her husband
    "20_14_1",  # Prov 14:1 - wise woman builds her house
])

# 56_2_6 (exhort young men to be sober minded)
total_added += add_refs("56_2_6", [
    "20_20_29", # Prov 20:29 - glory of young men is strength
    "21_11_9",  # Eccl 11:9 - rejoice in youth but know God will judge
    "54_6_11",  # 1Tim 6:11 - flee these things, man of God
])

# 56_2_7 (yourself a pattern of good works)
total_added += add_refs("56_2_7", [
    "53_3_9",   # 2Thess 3:9 - make ourselves a model
    "44_20_35", # Acts 20:35 - example of laboring to support weak
    "45_12_2",  # Rom 12:2 - transformed by renewing of mind
])

# 56_2_9 (servants obedient to masters in all things)
total_added += add_refs("56_2_9", [
    "49_6_6",   # Eph 6:6 - not with eyeservice as men-pleasers
    "3_25_43",  # Lev 25:43 - do not rule with rigor
    "51_3_23",  # Col 3:23 - work heartily as to the Lord
])

# 56_2_14 (gave Himself to redeem, zealous of good works)
total_added += add_refs("56_2_14", [
    "26_37_23", # Ezek 37:23 - I will cleanse them
    "19_72_14", # Ps 72:14 - precious is their blood in His sight
    "43_1_29",  # John 1:29 - Lamb of God who takes away sin
    "60_1_18",  # 1Pet 1:18 - redeemed with precious blood of Christ
])

# 56_2_15 (speak/exhort/rebuke with all authority)
total_added += add_refs("56_2_15", [
    "40_7_29",  # Matt 7:29 - taught as one having authority
    "44_5_20",  # Acts 5:20 - speak all words of life to people
    "54_4_2",   # 1Tim 4:2 - preach the word in season and out
])

# 56_3_3 (foolish disobedient deceived before conversion)
total_added += add_refs("56_3_3", [
    "51_1_21",  # Col 1:21 - once alienated, enemies in mind
    "60_1_18",  # 1Pet 1:18 - vain manner of life
    "19_14_1",  # Ps 14:1 - fool says no God
    "5_32_6",   # Deut 32:6 - foolish and unwise people
])

# 56_3_5 (washing of regeneration, renewing of Holy Spirit)
total_added += add_refs("56_3_5", [
    "26_36_26", # Ezek 36:26 - new heart and new spirit
    "24_31_33", # Jer 31:33 - law written on their hearts
    "45_6_4",   # Rom 6:4 - buried/raised with Christ in baptism
    "44_2_38",  # Acts 2:38 - baptized for remission of sins
])

# 56_3_7 (justified by grace, heirs of eternal life)
total_added += add_refs("56_3_7", [
    "1_12_3",   # Gen 12:3 - all families of earth blessed
    "48_3_14",  # Gal 3:14 - receive promise of Spirit
    "45_5_1",   # Rom 5:1 - justified by faith, peace with God
    "49_2_7",   # Eph 2:7 - exceeding riches of His grace
])

# 56_3_9 (avoid foolish questions, genealogies, strivings)
total_added += add_refs("56_3_9", [
    "51_2_8",   # Col 2:8 - beware of philosophy and vain deceit
    "54_1_7",   # 1Tim 1:7 - desiring to be teachers of the law
    "44_18_15", # Acts 18:15 - questions about words and law
])

# 56_3_12 (be diligent to come to Nicopolis)
total_added += add_refs("56_3_12", [
    "45_15_24", # Rom 15:24 - hope to see you in my journey
    "47_13_11", # 2Cor 13:11 - farewell, be of good comfort
    "52_3_10",  # 1Thess 3:10 - see your face, perfect what lacks
])

print(f"Total new cross-references added: {total_added}")

# Validate - no bad refs (non-strings)
bad = [k for k, v in d.items() for r in v if not isinstance(r, str)]
print(f"Bad refs: {len(bad)}")

# Write updated JSON
with open(path, "w") as f:
    json.dump(d, f, separators=(",", ":"))
print(f"Written. Total entries: {len(d)}")
