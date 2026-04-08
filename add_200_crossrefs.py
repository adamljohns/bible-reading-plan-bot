#!/usr/bin/env python3
"""Add 200 new cross-reference entries connecting OT verses to Romans/Ephesians themes."""
import json

FILE = "/Users/adamjohns/bible-reading-plan-bot/docs/assets/cross-references.json"

# 200 new entries grouped by book and theme
# Book numbers: 1=Gen, 5=Deut, 18=Job, 19=Psalms, 20=Proverbs, 23=Isaiah, 24=Jeremiah, 26=Ezekiel, 27=Daniel
# NT refs: 40=Matt, 41=Mark, 42=Luke, 43=John, 44=Acts, 45=Romans, 46=1Cor, 47=2Cor, 48=Gal, 49=Eph, 50=Phil, 51=Col, 58=Heb, 59=Jas, 60=1Pet, 61=2Pet, 62=1John

NEW_ENTRIES = {
    # === GENESIS (Book 1) — Faith, Righteousness, Adoption, Reconciliation ===
    # Gen 1:26 - Image of God -> new creation in Christ
    "1_1_26": ["45_8_29", "49_4_24", "47_3_18", "51_3_10", "1_5_1"],
    # Gen 1:27 - Male and female created
    "1_1_27": ["49_5_31", "48_3_28", "40_19_4", "46_11_7"],
    # Gen 2:7 - Breath of life -> spiritual life
    "1_2_7": ["45_8_11", "43_20_22", "46_15_45", "49_2_5"],
    # Gen 2:17 - Death through sin
    "1_2_17": ["45_5_12", "45_6_23", "49_2_1", "46_15_22"],
    # Gen 2:24 - One flesh -> Christ and Church
    "1_2_24": ["49_5_31", "49_5_32", "40_19_5", "46_6_16"],
    # Gen 3:6 - The Fall
    "1_3_6": ["45_5_12", "45_5_19", "46_15_21", "54_2_14"],
    # Gen 3:8 - Hiding from God -> reconciliation needed
    "1_3_8": ["45_3_23", "49_2_13", "47_5_18", "23_59_2"],
    # Gen 3:15 - Protoevangelium
    "1_3_15": ["45_16_20", "48_4_4", "49_1_10", "66_12_9", "62_3_8"],
    # Gen 3:21 - God clothes Adam/Eve -> righteousness covering
    "1_3_21": ["45_3_22", "49_6_14", "48_3_27", "23_61_10"],
    # Gen 3:24 - Banishment -> separation from God
    "1_3_24": ["45_5_10", "49_2_12", "49_2_13", "58_10_20"],
    # Gen 4:7 - Sin crouching -> spiritual warfare
    "1_4_7": ["45_6_12", "49_6_11", "60_5_8", "59_4_7"],
    # Gen 5:24 - Enoch walked with God
    "1_5_24": ["45_8_4", "49_5_8", "58_11_5", "33_6_8"],
    # Gen 6:8 - Noah found grace
    "1_6_8": ["45_3_24", "49_2_8", "56_2_11", "60_3_20"],
    # Gen 6:9 - Noah righteous in his generation
    "1_6_9": ["45_1_17", "49_4_1", "58_11_7", "61_2_5"],
    # Gen 8:21 - Heart evil from youth
    "1_8_21": ["45_3_10", "49_2_3", "24_17_9", "40_15_19"],
    # Gen 9:6 - Image of God
    "1_9_6": ["45_13_4", "49_4_24", "59_3_9", "46_11_7"],
    # Gen 12:1 - Call of Abram
    "1_12_1": ["45_4_17", "49_1_18", "58_11_8", "48_3_8"],
    # Gen 12:2 - Blessing promise
    "1_12_2": ["45_4_13", "49_1_3", "48_3_14", "44_3_25"],
    # Gen 12:3 - All families blessed
    "1_12_3": ["45_4_16", "49_2_11", "48_3_8", "48_3_14", "44_3_25"],
    # Gen 12:7 - Seed promise
    "1_12_7": ["45_4_13", "48_3_16", "49_3_6", "58_11_9"],
    # Gen 15:1 - Shield and reward
    "1_15_1": ["49_6_16", "45_8_31", "19_84_11", "58_11_6"],
    # Gen 15:6 - Faith credited as righteousness (KEY verse)
    "1_15_6": ["45_4_3", "45_4_9", "48_3_6", "59_2_23", "49_2_8"],
    # Gen 17:1 - Walk before me blameless
    "1_17_1": ["45_4_11", "49_1_4", "49_5_27", "50_3_12"],
    # Gen 17:7 - Everlasting covenant
    "1_17_7": ["45_9_4", "49_2_12", "48_3_17", "58_8_10"],
    # Gen 18:25 - Judge of all the earth
    "1_18_25": ["45_3_6", "45_2_16", "49_1_11", "44_17_31"],
    # Gen 21:12 - In Isaac your seed
    "1_21_12": ["45_9_7", "48_4_28", "58_11_18", "49_3_6"],
    # Gen 22:8 - God will provide the lamb
    "1_22_8": ["45_8_32", "49_5_2", "43_1_29", "58_10_10"],
    # Gen 22:14 - The Lord will provide
    "1_22_14": ["45_8_32", "49_1_3", "50_4_19", "58_11_17"],
    # Gen 22:18 - In your seed all nations blessed
    "1_22_18": ["45_4_13", "48_3_16", "49_3_6", "44_3_25"],
    # Gen 26:4 - Seed blessing reiterated to Isaac
    "1_26_4": ["45_4_16", "48_3_8", "49_2_12", "58_6_14"],
    # Gen 28:15 - I am with you
    "1_28_15": ["45_8_31", "49_3_17", "40_28_20", "58_13_5"],
    # Gen 32:30 - Jacob sees God face to face
    "1_32_30": ["45_9_13", "49_3_12", "46_13_12", "47_3_18"],
    # Gen 45:5 - God sent me -> sovereignty in salvation
    "1_45_5": ["45_8_28", "49_1_11", "49_1_5", "1_50_20"],
    # Gen 49:10 - Shiloh/scepter prophecy
    "1_49_10": ["45_1_3", "49_1_20", "58_7_14", "66_5_5"],
    # Gen 50:20 - God meant it for good
    "1_50_20": ["45_8_28", "49_1_11", "49_3_11", "50_1_12"],

    # === DEUTERONOMY (Book 5) — Law, Grace, Obedience, Spiritual Warfare ===
    # Deut 4:29 - Seek the Lord with all your heart
    "5_4_29": ["45_10_9", "49_1_17", "24_29_13", "40_7_7"],
    # Deut 5:6 - I am the LORD who brought you out
    "5_5_6": ["45_6_18", "49_2_8", "48_5_1", "56_2_14"],
    # Deut 6:4 - Hear O Israel, the Lord is one
    "5_6_4": ["45_3_30", "49_4_5", "46_8_6", "41_12_29"],
    # Deut 6:5 - Love the Lord with all your heart
    "5_6_5": ["45_13_10", "49_6_24", "40_22_37", "41_12_30"],
    # Deut 6:6 - Words on your heart
    "5_6_6": ["45_10_8", "49_6_17", "51_3_16", "19_119_11"],
    # Deut 7:6 - Chosen people
    "5_7_6": ["45_9_11", "49_1_4", "60_2_9", "56_2_14"],
    # Deut 7:7 - Not because you were numerous
    "5_7_7": ["45_9_11", "49_2_9", "46_1_27", "56_3_5"],
    # Deut 7:8 - Because the Lord loved you
    "5_7_8": ["45_5_8", "49_2_4", "62_4_10", "43_3_16"],
    # Deut 8:3 - Man does not live by bread alone
    "5_8_3": ["49_6_17", "45_10_17", "40_4_4", "43_6_63"],
    # Deut 9:4 - Not because of your righteousness
    "5_9_4": ["45_9_16", "49_2_9", "56_3_5", "47_5_21"],
    # Deut 9:5 - Not your righteousness but promise
    "5_9_5": ["45_4_13", "49_2_8", "48_3_18", "56_3_5"],
    # Deut 10:16 - Circumcise your heart
    "5_10_16": ["45_2_29", "49_2_11", "50_3_3", "24_4_4", "51_2_11"],
    # Deut 10:17 - God of gods, Lord of lords
    "5_10_17": ["45_9_5", "49_1_21", "54_6_15", "66_17_14"],
    # Deut 14:2 - Holy people, treasured possession
    "5_14_2": ["45_9_4", "49_1_4", "60_2_9", "56_2_14"],
    # Deut 18:15 - Prophet like Moses
    "5_18_15": ["45_10_4", "49_4_21", "44_3_22", "43_6_14"],
    # Deut 21:23 - Cursed is everyone hung on a tree
    "5_21_23": ["48_3_13", "45_8_3", "49_2_16", "60_2_24"],
    # Deut 27:26 - Cursed who does not confirm the law
    "5_27_26": ["45_3_20", "48_3_10", "49_2_15", "59_2_10"],
    # Deut 28:1 - Blessings for obedience
    "5_28_1": ["45_2_13", "49_1_3", "48_3_14", "59_1_25"],
    # Deut 29:4 - Eyes that do not see, ears that do not hear
    "5_29_4": ["45_11_8", "49_4_18", "23_6_10", "40_13_14"],
    # Deut 30:6 - Lord will circumcise your heart
    "5_30_6": ["45_2_29", "49_2_10", "26_36_26", "50_3_3", "51_2_11"],
    # Deut 30:11 - Command not too difficult
    "5_30_11": ["45_10_6", "49_2_10", "62_5_3", "40_11_30"],
    # Deut 30:12 - Who will ascend to heaven?
    "5_30_12": ["45_10_6", "49_4_9", "43_3_13", "50_2_6"],
    # Deut 30:14 - Word is near you
    "5_30_14": ["45_10_8", "49_6_17", "51_3_16", "59_1_21"],
    # Deut 32:4 - The Rock, his work is perfect
    "5_32_4": ["45_9_14", "49_2_10", "40_5_48", "19_18_2"],
    # Deut 32:21 - I will make you jealous by a non-nation
    "5_32_21": ["45_10_19", "49_2_12", "45_11_11", "45_11_14"],
    # Deut 32:35 - Vengeance is mine
    "5_32_35": ["45_12_19", "49_4_26", "58_10_30", "53_1_8"],
    # Deut 32:36 - The Lord will judge his people
    "5_32_36": ["45_14_10", "49_6_8", "58_10_30", "60_4_17"],
    # Deut 32:43 - Rejoice, O nations, with his people
    "5_32_43": ["45_15_10", "49_2_14", "49_3_6", "66_7_9"],
    # Deut 33:27 - Eternal God is your refuge
    "5_33_27": ["45_8_39", "49_1_19", "19_46_1", "19_90_1"],

    # === JOB (Book 18) — Suffering, Sovereignty, Righteousness ===
    # Job 1:21 - The Lord gave, the Lord has taken away
    "18_1_21": ["45_8_28", "49_1_11", "54_6_7", "50_4_12"],
    # Job 4:17 - Can a mortal be righteous before God?
    "18_4_17": ["45_3_10", "49_2_8", "18_9_2", "19_143_2"],
    # Job 5:17 - Blessed is the one God corrects
    "18_5_17": ["45_5_3", "49_3_13", "58_12_5", "66_3_19"],
    # Job 9:2 - How can a mortal be righteous before God?
    "18_9_2": ["45_3_20", "49_2_9", "48_2_16", "19_130_3"],
    # Job 9:33 - No arbiter between us
    "18_9_33": ["45_8_34", "49_2_18", "54_2_5", "58_9_15"],
    # Job 13:15 - Though he slay me, I will hope
    "18_13_15": ["45_8_24", "49_1_12", "58_11_1", "35_3_17"],
    # Job 14:1 - Man born of woman, few days and full of trouble
    "18_14_1": ["45_8_20", "49_2_3", "19_90_10", "59_4_14"],
    # Job 14:4 - Who can bring clean from unclean?
    "18_14_4": ["45_3_23", "49_2_1", "19_51_5", "43_3_6"],
    # Job 19:25 - I know my redeemer lives
    "18_19_25": ["45_8_11", "49_1_7", "46_15_20", "60_1_3"],
    # Job 19:26 - In my flesh I shall see God
    "18_19_26": ["45_8_23", "49_1_14", "50_3_21", "62_3_2"],
    # Job 23:10 - He knows the way I take; refined as gold
    "18_23_10": ["45_8_28", "49_2_10", "60_1_7", "59_1_12"],
    # Job 25:4 - How can one born of woman be pure?
    "18_25_4": ["45_3_10", "49_2_3", "19_51_5", "48_2_16"],
    # Job 28:28 - Fear of the Lord is wisdom
    "18_28_28": ["45_11_33", "49_5_15", "20_1_7", "51_2_3"],
    # Job 33:4 - Spirit of God has made me
    "18_33_4": ["45_8_11", "49_2_10", "1_2_7", "43_6_63"],
    # Job 33:24 - Deliver him, I have found a ransom
    "18_33_24": ["45_3_24", "49_1_7", "54_2_6", "41_10_45"],
    # Job 33:26 - Restored to righteous state
    "18_33_26": ["45_5_1", "49_2_18", "47_5_20", "48_4_5"],
    # Job 34:19 - God shows no partiality
    "18_34_19": ["45_2_11", "49_6_9", "44_10_34", "48_2_6"],
    # Job 38:4 - Where were you when I laid the earth's foundation?
    "18_38_4": ["45_9_20", "49_1_4", "23_40_28", "51_1_16"],
    # Job 42:2 - I know you can do all things
    "18_42_2": ["45_8_28", "49_1_11", "49_3_20", "24_32_17"],
    # Job 42:5 - Now my eyes have seen you
    "18_42_5": ["45_1_20", "49_1_17", "47_3_18", "43_14_9"],
    # Job 42:6 - I repent in dust and ashes
    "18_42_6": ["45_2_4", "49_4_22", "47_7_10", "42_18_13"],

    # === PSALMS (Book 19) — Righteousness, Grace, Adoption, Praise ===
    # Ps 2:7 - You are my son
    "19_2_7": ["45_1_4", "49_1_5", "58_1_5", "44_13_33"],
    # Ps 4:1 - God of my righteousness
    "19_4_1": ["45_3_22", "49_6_14", "50_3_9", "47_5_21"],
    # Ps 5:9 - Throat is an open grave
    "19_5_9": ["45_3_13", "49_2_1", "45_3_10", "59_3_6"],
    # Ps 7:11 - God is a righteous judge
    "19_7_11": ["45_2_5", "49_6_8", "47_5_10", "55_4_8"],
    # Ps 8:6 - Dominion over works of hands
    "19_8_6": ["45_8_17", "49_1_22", "58_2_8", "46_15_27"],
    # Ps 10:7 - Mouth full of cursing and deceit
    "19_10_7": ["45_3_14", "49_4_25", "59_3_10", "45_3_10"],
    # Ps 14:1 - Fool says no God
    "19_14_1": ["45_3_10", "49_2_12", "45_1_21", "54_6_5"],
    # Ps 14:2 - Lord looks down from heaven
    "19_14_2": ["45_3_11", "49_2_4", "47_13_5", "19_53_2"],
    # Ps 14:3 - All have turned aside
    "19_14_3": ["45_3_12", "49_2_3", "23_53_6", "45_3_23"],
    # Ps 16:10 - Will not abandon my soul to Sheol
    "19_16_10": ["45_8_11", "49_1_20", "44_2_27", "44_13_35"],
    # Ps 17:15 - Satisfied beholding your likeness
    "19_17_15": ["45_8_29", "49_4_24", "62_3_2", "47_3_18"],
    # Ps 18:2 - The Lord is my rock
    "19_18_2": ["45_9_33", "49_2_20", "46_10_4", "5_32_4"],
    # Ps 19:1 - Heavens declare glory of God
    "19_19_1": ["45_1_20", "49_3_10", "45_10_18", "23_6_3"],
    # Ps 19:7 - Law of the Lord is perfect
    "19_19_7": ["45_7_12", "49_6_17", "19_119_105", "59_1_25"],
    # Ps 22:1 - My God, why have you forsaken me?
    "19_22_1": ["45_8_32", "49_2_16", "40_27_46", "41_15_34"],
    # Ps 22:27 - All ends of earth shall remember and turn
    "19_22_27": ["45_15_9", "49_3_6", "23_45_22", "66_7_9"],
    # Ps 23:1 - The Lord is my shepherd
    "19_23_1": ["45_8_31", "49_5_29", "43_10_11", "58_13_20"],
    # Ps 24:1 - The earth is the Lord's
    "19_24_1": ["45_14_8", "49_1_10", "46_10_26", "51_1_16"],
    # Ps 25:7 - Remember not sins of my youth
    "19_25_7": ["45_4_7", "49_1_7", "23_43_25", "19_103_12"],
    # Ps 27:1 - The Lord is my light and salvation
    "19_27_1": ["45_8_31", "49_5_8", "43_8_12", "62_1_5"],
    # Ps 30:5 - Weeping may tarry but joy comes
    "19_30_5": ["45_8_18", "49_2_7", "47_4_17", "43_16_20"],
    # Ps 32:1 - Blessed whose transgression forgiven
    "19_32_1": ["45_4_7", "49_1_7", "45_4_6", "19_130_4"],
    # Ps 32:2 - Blessed to whom Lord counts no iniquity
    "19_32_2": ["45_4_8", "49_2_8", "47_5_19", "45_5_13"],
    # Ps 32:5 - I acknowledged my sin and you forgave
    "19_32_5": ["45_4_7", "49_4_32", "62_1_9", "20_28_13"],
    # Ps 33:6 - By the word of the Lord heavens made
    "19_33_6": ["45_4_17", "49_3_9", "43_1_3", "58_11_3"],
    # Ps 34:18 - Lord is near to the brokenhearted
    "19_34_18": ["45_8_28", "49_2_13", "23_57_15", "19_147_3"],
    # Ps 36:1 - No fear of God before their eyes
    "19_36_1": ["45_3_18", "49_2_12", "45_3_10", "19_14_1"],
    # Ps 37:5 - Commit your way to the Lord
    "19_37_5": ["45_8_28", "49_5_17", "60_5_7", "20_3_5"],
    # Ps 40:6 - Sacrifice and offering you did not desire
    "19_40_6": ["45_12_1", "49_5_2", "58_10_5", "23_1_11"],
    # Ps 40:8 - I delight to do your will
    "19_40_8": ["45_7_22", "49_6_6", "58_10_7", "43_4_34"],
    # Ps 44:22 - For your sake we are killed all day
    "19_44_22": ["45_8_36", "49_6_12", "47_4_11", "47_11_23"],
    # Ps 46:1 - God is our refuge and strength
    "19_46_1": ["45_8_31", "49_6_10", "23_25_4", "34_1_7"],
    # Ps 49:7 - No one can redeem the life of another
    "19_49_7": ["45_3_24", "49_1_7", "60_1_18", "41_10_45"],
    # Ps 49:15 - God will redeem my soul
    "19_49_15": ["45_8_23", "49_1_14", "58_2_15", "28_13_14"],
    # Ps 51:1 - Have mercy according to steadfast love
    "19_51_1": ["45_9_15", "49_2_4", "42_18_13", "56_3_5"],
    # Ps 51:4 - Against you only have I sinned
    "19_51_4": ["45_3_4", "49_4_30", "42_15_21", "45_3_19"],
    # Ps 51:5 - In sin my mother conceived me
    "19_51_5": ["45_5_12", "49_2_3", "43_3_6", "18_14_4"],
    # Ps 51:10 - Create in me a clean heart
    "19_51_10": ["45_12_2", "49_4_23", "26_36_26", "47_5_17"],
    # Ps 51:17 - Broken spirit, contrite heart
    "19_51_17": ["45_2_4", "49_4_2", "23_57_15", "23_66_2"],
    # Ps 62:12 - You repay each according to his work
    "19_62_12": ["45_2_6", "49_6_8", "47_5_10", "40_16_27"],
    # Ps 65:3 - Iniquities prevail, you atone
    "19_65_3": ["45_3_25", "49_1_7", "62_2_2", "58_9_5"],
    # Ps 68:18 - You ascended on high, led captives
    "19_68_18": ["49_4_8", "51_2_15", "50_2_9", "44_1_9"],
    # Ps 69:9 - Zeal for your house consumed me
    "19_69_9": ["45_15_3", "49_5_25", "43_2_17", "45_10_2"],
    # Ps 71:2 - In your righteousness deliver me
    "19_71_2": ["45_1_17", "49_6_14", "19_31_1", "23_46_13"],
    # Ps 72:17 - All nations blessed through him
    "19_72_17": ["45_15_12", "49_1_10", "48_3_8", "1_22_18"],
    # Ps 78:38 - He is compassionate, forgave
    "19_78_38": ["45_3_25", "49_4_32", "23_55_7", "33_7_18"],
    # Ps 85:10 - Mercy and truth met, righteousness and peace kissed
    "19_85_10": ["45_3_26", "49_2_14", "45_5_1", "23_32_17"],
    # Ps 86:5 - You Lord are good, forgiving
    "19_86_5": ["45_5_20", "49_1_7", "34_1_7", "29_2_13"],
    # Ps 89:14 - Righteousness and justice foundation of throne
    "19_89_14": ["45_3_26", "49_1_6", "23_9_7", "19_97_2"],
    # Ps 89:26 - He shall cry, You are my Father
    "19_89_26": ["45_8_15", "49_1_5", "58_1_5", "40_6_9"],
    # Ps 90:8 - You set our iniquities before you
    "19_90_8": ["45_2_16", "49_5_13", "58_4_13", "19_139_1"],
    # Ps 95:7 - He is our God, we people of his pasture
    "19_95_7": ["45_9_25", "49_2_10", "43_10_14", "58_3_7"],
    # Ps 96:13 - He will judge the world in righteousness
    "19_96_13": ["45_2_5", "49_1_10", "44_17_31", "55_4_1"],
    # Ps 98:2 - The Lord has made known his salvation
    "19_98_2": ["45_1_16", "49_3_5", "42_2_30", "23_52_10"],
    # Ps 100:3 - He made us, we are his people
    "19_100_3": ["45_9_21", "49_2_10", "60_2_10", "43_10_14"],
    # Ps 103:3 - Who forgives all your iniquity
    "19_103_3": ["45_4_7", "49_1_7", "51_1_14", "23_33_24"],
    # Ps 103:10 - Does not deal with us according to sins
    "19_103_10": ["45_8_1", "49_2_4", "19_130_3", "25_3_22"],
    # Ps 103:12 - As far as east from west, removed transgressions
    "19_103_12": ["45_8_33", "49_1_7", "23_43_25", "33_7_19"],
    # Ps 110:1 - Sit at my right hand
    "19_110_1": ["45_8_34", "49_1_20", "58_1_13", "44_2_34"],
    # Ps 110:4 - Priest forever, order of Melchizedek
    "19_110_4": ["45_8_34", "49_2_18", "58_5_6", "58_7_17"],
    # Ps 111:10 - Fear of the Lord is beginning of wisdom
    "19_111_10": ["45_11_33", "49_5_15", "20_9_10", "51_2_3"],
    # Ps 116:3 - Cords of death
    "19_116_3": ["45_6_9", "49_2_1", "58_2_15", "19_18_4"],
    # Ps 117:1 - Praise the Lord all nations
    "19_117_1": ["45_15_11", "49_3_6", "66_7_9", "23_42_10"],
    # Ps 118:22 - Stone the builders rejected
    "19_118_22": ["45_9_33", "49_2_20", "60_2_7", "40_21_42"],
    # Ps 119:11 - Word hidden in heart
    "19_119_11": ["45_10_8", "49_6_17", "51_3_16", "5_6_6"],
    # Ps 119:105 - Word is lamp to my feet
    "19_119_105": ["45_15_4", "49_5_8", "61_1_19", "19_19_8"],
    # Ps 119:130 - Unfolding of your words gives light
    "19_119_130": ["45_1_16", "49_5_8", "47_4_6", "58_4_12"],
    # Ps 130:3 - If you kept record of sins
    "19_130_3": ["45_3_20", "49_2_4", "19_143_2", "62_1_8"],
    # Ps 130:4 - With you there is forgiveness
    "19_130_4": ["45_3_24", "49_1_7", "19_86_5", "27_9_9"],
    # Ps 130:7 - With the Lord is steadfast love and plenteous redemption
    "19_130_7": ["45_3_24", "49_1_7", "56_2_14", "45_5_20"],
    # Ps 139:14 - Fearfully and wonderfully made
    "19_139_14": ["45_9_20", "49_2_10", "1_1_27", "46_12_18"],
    # Ps 143:2 - No living person is righteous before you
    "19_143_2": ["45_3_20", "49_2_8", "48_2_16", "21_7_20"],
    # Ps 145:9 - The Lord is good to all
    "19_145_9": ["45_2_4", "49_2_7", "34_1_7", "25_3_25"],
    # Ps 145:17 - The Lord is righteous in all his ways
    "19_145_17": ["45_3_26", "49_1_6", "27_9_14", "5_32_4"],
    # Ps 147:3 - Heals the brokenhearted
    "19_147_3": ["45_8_28", "49_2_14", "23_61_1", "19_34_18"],

    # === PROVERBS (Book 20) — Wisdom, Righteousness, Walk ===
    # Prov 1:7 - Fear of the Lord beginning of knowledge
    "20_1_7": ["45_11_33", "49_5_15", "18_28_28", "51_2_3"],
    # Prov 2:6 - The Lord gives wisdom
    "20_2_6": ["45_11_33", "49_1_17", "59_1_5", "46_1_30"],
    # Prov 3:5 - Trust in the Lord with all your heart
    "20_3_5": ["45_8_28", "49_1_12", "23_26_3", "19_37_5"],
    # Prov 3:6 - In all your ways acknowledge him
    "20_3_6": ["45_12_1", "49_5_17", "51_3_17", "19_37_5"],
    # Prov 3:7 - Be not wise in your own eyes
    "20_3_7": ["45_12_16", "49_5_15", "23_5_21", "46_3_18"],
    # Prov 3:34 - God opposes proud, gives grace to humble
    "20_3_34": ["45_12_3", "49_4_2", "59_4_6", "60_5_5"],
    # Prov 8:22 - Wisdom before creation
    "20_8_22": ["45_11_33", "49_1_4", "43_1_1", "51_1_15"],
    # Prov 9:10 - Fear of the Lord is beginning of wisdom
    "20_9_10": ["45_11_33", "49_5_15", "19_111_10", "18_28_28"],
    # Prov 10:2 - Righteousness delivers from death
    "20_10_2": ["45_6_23", "49_2_5", "20_11_4", "19_49_15"],
    # Prov 10:12 - Love covers all offenses
    "20_10_12": ["45_13_10", "49_4_32", "60_4_8", "46_13_7"],
    # Prov 11:4 - Righteousness delivers from death
    "20_11_4": ["45_1_17", "49_2_8", "20_10_2", "48_5_5"],
    # Prov 11:30 - Fruit of righteous is tree of life
    "20_11_30": ["45_1_17", "49_5_9", "48_5_22", "43_15_5"],
    # Prov 14:12 - Way seems right but ends in death
    "20_14_12": ["45_6_21", "49_4_17", "40_7_13", "23_55_8"],
    # Prov 14:34 - Righteousness exalts a nation
    "20_14_34": ["45_13_1", "49_5_9", "23_1_27", "19_33_12"],
    # Prov 16:6 - By steadfast love and faithfulness iniquity is atoned
    "20_16_6": ["45_3_25", "49_1_7", "19_85_10", "33_7_18"],
    # Prov 17:3 - The Lord tests the heart
    "20_17_3": ["45_8_27", "49_6_8", "24_17_10", "60_1_7"],
    # Prov 20:9 - Who can say I have made my heart clean?
    "20_20_9": ["45_3_10", "49_2_3", "62_1_8", "21_7_20"],
    # Prov 21:2 - Lord weighs the heart
    "20_21_2": ["45_2_16", "49_6_8", "58_4_13", "24_17_10"],
    # Prov 21:3 - Righteousness more acceptable than sacrifice
    "20_21_3": ["45_12_1", "49_5_10", "28_6_6", "40_9_13"],
    # Prov 24:12 - God renders according to deeds
    "20_24_12": ["45_2_6", "49_6_8", "47_5_10", "40_16_27"],
    # Prov 28:13 - Confesses and forsakes sins finds mercy
    "20_28_13": ["45_10_9", "49_4_22", "62_1_9", "19_32_5"],
    # Prov 28:26 - Trusts own heart is a fool
    "20_28_26": ["45_10_3", "49_4_17", "24_17_9", "48_6_3"],

    # === ISAIAH (Book 23) — Redemption, Suffering Servant, Righteousness ===
    # Isa 1:18 - Though sins be scarlet, white as snow
    "23_1_18": ["45_3_24", "49_1_7", "62_1_7", "19_51_7"],
    # Isa 6:3 - Holy, holy, holy
    "23_6_3": ["45_11_36", "49_1_6", "66_4_8", "19_99_9"],
    # Isa 6:5 - Woe is me, I am undone
    "23_6_5": ["45_3_19", "49_2_1", "42_5_8", "18_42_6"],
    # Isa 6:10 - Make the heart of this people dull
    "23_6_10": ["45_11_8", "49_4_18", "40_13_14", "43_12_40"],
    # Isa 7:14 - Virgin shall conceive, Immanuel
    "23_7_14": ["45_1_3", "49_1_20", "40_1_23", "42_1_35"],
    # Isa 9:6 - For to us a child is born
    "23_9_6": ["45_9_5", "49_1_21", "42_2_11", "43_1_1"],
    # Isa 11:1 - Shoot from stump of Jesse
    "23_11_1": ["45_15_12", "49_1_20", "66_5_5", "66_22_16"],
    # Isa 25:8 - He will swallow up death forever
    "23_25_8": ["45_8_37", "49_1_10", "46_15_54", "66_21_4"],
    # Isa 28:16 - A precious cornerstone, sure foundation
    "23_28_16": ["45_9_33", "49_2_20", "60_2_6", "46_3_11"],
    # Isa 32:17 - Fruit of righteousness shall be peace
    "23_32_17": ["45_5_1", "49_2_14", "50_4_7", "48_5_22"],
    # Isa 40:13 - Who has directed the Spirit of the Lord?
    "23_40_13": ["45_11_34", "49_3_10", "46_2_16", "18_38_4"],
    # Isa 40:31 - They who wait upon the Lord shall renew strength
    "23_40_31": ["45_8_25", "49_3_16", "50_4_13", "48_6_9"],
    # Isa 42:1 - My servant in whom my soul delights
    "23_42_1": ["45_1_1", "49_1_6", "40_3_17", "40_12_18"],
    # Isa 42:6 - A light to the nations
    "23_42_6": ["45_15_9", "49_3_6", "42_2_32", "44_13_47"],
    # Isa 43:1 - I have redeemed you, called you by name
    "23_43_1": ["45_8_30", "49_1_4", "43_10_3", "55_2_19"],
    # Isa 43:25 - I blot out your transgressions
    "23_43_25": ["45_4_7", "49_1_7", "19_103_12", "58_8_12"],
    # Isa 44:22 - I have swept away your transgressions
    "23_44_22": ["45_8_1", "49_1_7", "44_3_19", "19_103_12"],
    # Isa 45:22 - Turn to me and be saved, all ends of earth
    "23_45_22": ["45_10_12", "49_2_13", "44_4_12", "43_12_32"],
    # Isa 46:10 - Declaring end from beginning
    "23_46_10": ["45_8_29", "49_1_11", "49_3_11", "23_55_11"],
    # Isa 48:17 - I am the Lord who teaches you to profit
    "23_48_17": ["45_8_28", "49_4_21", "43_14_26", "19_25_9"],
    # Isa 49:6 - A light to the Gentiles
    "23_49_6": ["45_15_9", "49_3_8", "42_2_32", "44_13_47"],
    # Isa 52:7 - Beautiful feet of him who brings good news
    "23_52_7": ["45_10_15", "49_6_15", "34_1_15", "45_1_16"],
    # Isa 53:3 - Despised and rejected
    "23_53_3": ["45_8_17", "49_2_16", "43_1_11", "60_2_4"],
    # Isa 53:4 - He bore our griefs
    "23_53_4": ["45_4_25", "49_2_16", "40_8_17", "60_2_24"],
    # Isa 53:5 - Wounded for our transgressions
    "23_53_5": ["45_5_6", "49_2_13", "60_2_24", "47_5_21"],
    # Isa 53:6 - All we like sheep have gone astray
    "23_53_6": ["45_3_23", "49_2_3", "60_2_25", "19_14_3"],
    # Isa 53:10 - It pleased the Lord to crush him
    "23_53_10": ["45_8_32", "49_5_2", "43_3_16", "58_10_10"],
    # Isa 53:11 - By knowledge righteous one makes many righteous
    "23_53_11": ["45_5_19", "49_2_8", "47_5_21", "58_9_28"],
    # Isa 53:12 - Numbered with transgressors
    "23_53_12": ["45_4_25", "49_5_2", "42_22_37", "41_15_28"],
    # Isa 54:10 - My steadfast love shall not depart
    "23_54_10": ["45_8_39", "49_2_7", "45_8_35", "24_31_3"],
    # Isa 55:1 - Come, everyone who thirsts
    "23_55_1": ["45_3_24", "49_2_8", "43_7_37", "66_22_17"],
    # Isa 55:6 - Seek the Lord while he may be found
    "23_55_6": ["45_10_13", "49_2_13", "47_6_2", "23_45_22"],
    # Isa 55:7 - Let the wicked forsake his way
    "23_55_7": ["45_2_4", "49_4_22", "44_3_19", "26_18_30"],
    # Isa 55:11 - My word shall not return empty
    "23_55_11": ["45_10_17", "49_6_17", "58_4_12", "23_46_10"],
    # Isa 57:15 - I dwell with contrite and lowly
    "23_57_15": ["45_12_16", "49_4_2", "19_51_17", "42_18_14"],
    # Isa 59:2 - Iniquities have made separation
    "23_59_2": ["45_3_23", "49_2_12", "1_3_8", "23_6_5"],
    # Isa 59:17 - Breastplate of righteousness, helmet of salvation
    "23_59_17": ["49_6_14", "49_6_17", "45_13_12", "52_5_8"],
    # Isa 61:1 - Spirit of the Lord upon me
    "23_61_1": ["45_8_11", "49_1_13", "42_4_18", "19_147_3"],
    # Isa 61:10 - Robe of righteousness
    "23_61_10": ["45_3_22", "49_6_14", "48_3_27", "47_5_21"],
    # Isa 64:6 - All our righteous deeds like filthy rags
    "23_64_6": ["45_3_20", "49_2_9", "56_3_5", "48_2_16", "50_3_9"],

    # === JEREMIAH (Book 24) — New Covenant, Heart, Repentance ===
    # Jer 1:5 - Before I formed you I knew you
    "24_1_5": ["45_8_29", "49_1_4", "48_1_15", "19_139_16"],
    # Jer 4:4 - Circumcise yourselves to the Lord
    "24_4_4": ["45_2_29", "49_2_11", "5_10_16", "51_2_11"],
    # Jer 9:24 - Let him who boasts boast in the Lord
    "24_9_24": ["45_3_27", "49_2_9", "46_1_31", "47_10_17"],
    # Jer 17:9 - Heart is deceitful above all things
    "24_17_9": ["45_3_10", "49_4_22", "1_8_21", "40_15_19"],
    # Jer 17:10 - I the Lord search the heart
    "24_17_10": ["45_8_27", "49_6_8", "58_4_13", "66_2_23"],
    # Jer 23:5 - Righteous Branch
    "24_23_5": ["45_1_3", "49_1_20", "23_11_1", "38_3_8"],
    # Jer 23:6 - The Lord our righteousness
    "24_23_6": ["45_3_22", "49_2_8", "46_1_30", "47_5_21"],
    # Jer 29:11 - Plans for welfare not calamity
    "24_29_11": ["45_8_28", "49_1_11", "49_2_10", "50_1_6"],
    # Jer 29:13 - You will seek me and find me
    "24_29_13": ["45_10_9", "49_3_12", "5_4_29", "40_7_7"],
    # Jer 31:3 - I have loved you with an everlasting love
    "24_31_3": ["45_8_39", "49_2_4", "43_3_16", "62_4_19"],
    # Jer 31:31 - I will make a new covenant
    "24_31_31": ["45_11_27", "49_2_12", "58_8_8", "42_22_20"],
    # Jer 31:33 - I will put my law in their minds
    "24_31_33": ["45_8_4", "49_2_10", "58_8_10", "47_3_3"],
    # Jer 31:34 - I will forgive their wickedness
    "24_31_34": ["45_11_27", "49_1_7", "58_8_12", "58_10_17"],
    # Jer 32:17 - Nothing too hard for you
    "24_32_17": ["45_8_31", "49_3_20", "42_1_37", "18_42_2"],
    # Jer 33:8 - I will cleanse them from all sin
    "24_33_8": ["45_6_22", "49_5_26", "62_1_7", "58_9_14"],
    # Jer 33:16 - The Lord our righteousness
    "24_33_16": ["45_3_22", "49_2_8", "24_23_6", "46_1_30"],
    # Jer 50:20 - Sin of Israel searched for but not found
    "24_50_20": ["45_8_1", "49_1_7", "33_7_19", "23_43_25"],

    # === EZEKIEL (Book 26) — New Heart, Spirit, Restoration ===
    # Ezek 11:19 - I will give them one heart
    "26_11_19": ["45_2_29", "49_4_23", "26_36_26", "47_3_3"],
    # Ezek 16:63 - I make atonement, you will be ashamed
    "26_16_63": ["45_3_25", "49_2_7", "45_6_21", "26_36_31"],
    # Ezek 18:4 - The soul who sins shall die
    "26_18_4": ["45_6_23", "49_2_1", "45_5_12", "1_2_17"],
    # Ezek 18:20 - Son shall not bear father's iniquity
    "26_18_20": ["45_14_12", "49_6_8", "47_5_10", "5_24_16"],
    # Ezek 18:23 - I take no pleasure in death of the wicked
    "26_18_23": ["45_2_4", "49_2_4", "61_3_9", "54_2_4"],
    # Ezek 18:30 - Repent and turn from transgressions
    "26_18_30": ["45_2_4", "49_4_22", "44_3_19", "23_55_7"],
    # Ezek 18:31 - Get a new heart and a new spirit
    "26_18_31": ["45_12_2", "49_4_23", "26_36_26", "19_51_10"],
    # Ezek 18:32 - I take no pleasure in death
    "26_18_32": ["45_6_23", "49_2_4", "61_3_9", "54_2_4"],
    # Ezek 33:11 - I take no pleasure in death of the wicked
    "26_33_11": ["45_2_4", "49_2_4", "42_15_7", "61_3_9", "54_2_4"],
    # Ezek 34:23 - I will set up one shepherd
    "26_34_23": ["45_8_34", "49_4_11", "43_10_11", "58_13_20"],
    # Ezek 34:25 - Covenant of peace
    "26_34_25": ["45_5_1", "49_2_14", "23_54_10", "28_2_18"],
    # Ezek 36:22 - Not for your sake but for my holy name
    "26_36_22": ["45_9_16", "49_1_6", "23_48_11", "49_1_12"],
    # Ezek 36:25 - I will sprinkle clean water on you
    "26_36_25": ["45_6_4", "49_5_26", "58_10_22", "56_3_5"],
    # Ezek 36:26 - New heart and new spirit (KEY verse)
    "26_36_26": ["45_2_29", "49_4_23", "47_5_17", "24_31_33", "19_51_10"],
    # Ezek 36:27 - I will put my Spirit within you
    "26_36_27": ["45_8_4", "49_1_13", "48_5_16", "43_14_17"],
    # Ezek 36:29 - I will save you from all uncleanness
    "26_36_29": ["45_6_22", "49_5_26", "56_2_14", "62_1_7"],
    # Ezek 36:33 - I will cleanse you from all iniquities
    "26_36_33": ["45_6_18", "49_5_27", "62_1_9", "58_9_14"],
    # Ezek 37:5 - I will cause breath to enter you
    "26_37_5": ["45_8_11", "49_2_5", "43_20_22", "1_2_7"],
    # Ezek 37:14 - I will put my Spirit within you and you shall live
    "26_37_14": ["45_8_11", "49_2_5", "43_6_63", "29_2_28"],
    # Ezek 37:26 - Everlasting covenant of peace
    "26_37_26": ["45_5_1", "49_2_14", "58_13_20", "23_54_10"],

    # === DANIEL (Book 27) — Sovereignty, Atonement, Judgment ===
    # Dan 2:21 - He changes times and seasons
    "27_2_21": ["45_13_1", "49_1_10", "44_1_7", "51_1_16"],
    # Dan 2:44 - God of heaven will set up a kingdom
    "27_2_44": ["45_14_17", "49_1_10", "42_1_33", "58_12_28"],
    # Dan 4:35 - He does according to his will
    "27_4_35": ["45_9_19", "49_1_11", "23_46_10", "50_2_13"],
    # Dan 7:13 - Son of Man coming with clouds
    "27_7_13": ["45_1_4", "49_1_20", "40_24_30", "66_1_7"],
    # Dan 7:14 - Dominion and glory and kingdom
    "27_7_14": ["45_14_11", "49_1_21", "50_2_10", "66_11_15"],
    # Dan 7:27 - Kingdom given to the saints
    "27_7_27": ["45_8_17", "49_1_18", "46_6_2", "66_20_4"],
    # Dan 9:5 - We have sinned and done wrong
    "27_9_5": ["45_3_23", "49_2_1", "62_1_8", "19_51_4"],
    # Dan 9:7 - Righteousness belongs to you, shame to us
    "27_9_7": ["45_3_4", "49_1_6", "19_145_17", "27_9_14"],
    # Dan 9:9 - To the Lord belong mercy and forgiveness
    "27_9_9": ["45_3_24", "49_1_7", "19_130_4", "34_1_3"],
    # Dan 9:14 - The Lord is righteous in all he does
    "27_9_14": ["45_3_26", "49_1_6", "19_145_17", "5_32_4"],
    # Dan 9:18 - Not because of our righteousness
    "27_9_18": ["45_3_20", "49_2_9", "56_3_5", "5_9_5"],
    # Dan 9:24 - To finish transgression, make atonement (KEY verse)
    "27_9_24": ["45_3_25", "49_1_7", "58_9_12", "48_4_4"],
    # Dan 9:26 - Anointed One shall be cut off
    "27_9_26": ["45_5_6", "49_2_16", "23_53_8", "42_24_26"],
    # Dan 12:1 - Everyone found written in the book
    "27_12_1": ["45_8_33", "49_1_4", "66_20_15", "50_4_3"],
    # Dan 12:2 - Many who sleep shall awake
    "27_12_2": ["45_6_5", "49_2_6", "43_5_29", "46_15_42"],
    # Dan 12:3 - Those who are wise shall shine
    "27_12_3": ["45_8_18", "49_5_8", "40_13_43", "50_2_15"],
}

# Load existing data
with open(FILE, 'r') as f:
    data = json.load(f)

print(f"Existing keys: {len(data)}")

# Verify no collisions
collisions = [k for k in NEW_ENTRIES if k in data]
if collisions:
    print(f"ERROR: {len(collisions)} keys already exist: {collisions}")
    # Remove collisions
    for k in collisions:
        del NEW_ENTRIES[k]
    print(f"Removed collisions. Remaining new entries: {len(NEW_ENTRIES)}")
    if len(NEW_ENTRIES) < 200:
        print(f"WARNING: Only {len(NEW_ENTRIES)} entries after removing collisions (need 200)")
        exit(1)

print(f"New entries to add: {len(NEW_ENTRIES)}")
assert len(NEW_ENTRIES) == 200, f"Expected 200 entries, got {len(NEW_ENTRIES)}"

# Verify all values are lists of strings and each has a Romans or Ephesians ref
for key, refs in NEW_ENTRIES.items():
    assert isinstance(refs, list), f"{key}: value is not a list"
    assert 4 <= len(refs) <= 6, f"{key}: has {len(refs)} refs (need 4-6)"
    for r in refs:
        assert isinstance(r, str), f"{key}: ref {r} is not a string"
    has_rom_eph = any(r.startswith("45_") or r.startswith("49_") for r in refs)
    assert has_rom_eph, f"{key}: no Romans/Ephesians cross-reference"

# Merge
data.update(NEW_ENTRIES)
print(f"Total keys after merge: {len(data)}")

# Write
with open(FILE, 'w') as f:
    json.dump(data, f, separators=(',', ':'))

print("Done. File written successfully.")
