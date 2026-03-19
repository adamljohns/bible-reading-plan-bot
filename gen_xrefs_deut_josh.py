#!/usr/bin/env python3
"""
BTE Cross-Reference Expander: Deuteronomy & Joshua
Adds 2-4 cross-references per verse with genuine theological connections.
OT→NT Christological links prioritized.
"""

import json
import sys

XREF_FILE = "docs/assets/cross-references.json"

# Load existing data
with open(XREF_FILE, "r") as f:
    data = json.load(f)

before_count = len(data)

# New cross-references
# Format: "book_chapter_verse": ["book_chapter_verse", ...]
# Book numbers: 1=Gen, 2=Ex, 3=Lev, 4=Num, 5=Deut, 6=Josh, 7=Judg, 8=Ruth
# 9=1Sam, 10=2Sam, 11=1Kgs, 12=2Kgs, 18=Job, 19=Ps, 20=Prov, 21=Eccl
# 22=Song, 23=Isa, 24=Jer, 25=Lam, 26=Ezek, 27=Dan, 28=Hos, 29=Joel, 30=Amos
# 33=Mic, 35=Hab, 38=Zech, 39=Mal
# 40=Matt, 41=Mark, 42=Luke, 43=John, 44=Acts, 45=Rom, 46=1Cor, 47=2Cor
# 48=Gal, 49=Eph, 50=Phil, 51=Col, 52=1Thess, 54=1Tim, 55=2Tim
# 58=Heb, 59=Jas, 60=1Pet, 61=2Pet, 62=1Jn, 65=Jude, 66=Rev

new_xrefs = {

    # ===== DEUTERONOMY =====

    # Chapter 1 - Moses recounts the wilderness journey
    "5_1_3":  ["4_14_20", "45_15_4"],       # Moses spoke God's words / OT written for our instruction
    "5_1_8":  ["1_12_7", "58_6_15"],        # Promised land / God's oath to Abraham, unchanging promise
    "5_1_21": ["40_14_27", "50_4_13"],      # Do not fear / I can do all things through Christ
    "5_1_30": ["45_8_31", "23_41_10"],      # God fights for you / if God for us / do not fear I am with you
    "5_1_31": ["58_12_7", "42_15_22"],      # God carried you as father / discipline / waiting father
    "5_1_32": ["58_3_18", "45_11_23"],      # Did not trust the Lord / unbelief prevents entry
    "5_1_38": ["4_27_18", "43_14_16"],      # Joshua commissioned / another Helper (Spirit)
    "5_1_43": ["45_10_3", "48_1_4"],        # Refused to listen / persecuted church / disobedience

    # Chapter 2-3
    "5_2_7":  ["45_11_33", "23_40_31"],     # God's provision, no lack in wilderness / wisdom unfathomable / renewed strength
    "5_2_25": ["58_11_33", "23_26_17"],     # Terror upon nations / hall of faith / wrath of God
    "5_3_22": ["45_8_31", "19_118_6"],      # Do not fear, God fights / what can man do
    "5_3_23": ["45_8_26", "19_86_6"],       # Moses' prayer / Spirit intercedes / cry for mercy

    # Chapter 4
    "5_4_2":  ["66_22_18", "20_30_6"],      # Do not add to the word / warning against adding to Scripture
    "5_4_7":  ["45_10_12", "19_34_18"],     # No nation has God so near / call on him / near to brokenhearted
    "5_4_9":  ["19_78_4", "49_6_4"],        # Teach children / make known God's deeds / fathers bring up children
    "5_4_10": ["40_28_20", "59_3_17"],      # Learn to fear / discipleship / wisdom from above
    "5_4_12": ["43_1_18", "43_4_24"],       # Heard voice, saw no form / no one has seen God / God is spirit
    "5_4_13": ["45_7_12", "47_3_3"],        # Written on tablets / law is holy / letter of Christ on hearts
    "5_4_24": ["58_12_29", "23_33_14"],     # God is consuming fire / Heb 12:29 direct / Isaiah fire
    "5_4_29": ["24_29_13", "40_7_7"],       # Seek with whole heart / Jer you will find me / ask and receive
    "5_4_30": ["45_2_4", "24_3_22"],        # Return to Lord / God's kindness leads to repentance / great is faithfulness
    "5_4_31": ["45_8_39", "23_49_15"],      # God will not forget covenant / nothing separates from love / God never forgets
    "5_4_35": ["23_45_5", "46_8_4"],        # No other God / Isaiah I am God / no god but one
    "5_4_39": ["23_45_22", "54_2_5"],       # God in heaven above, none else / turn to me all ends / one mediator

    # Chapter 5
    "5_5_6":  ["44_7_36", "42_1_74"],       # I am Lord who brought you out / Acts references exodus / Zechariah's song
    "5_5_7":  ["40_4_10", "23_44_6"],       # Worship God alone / Jesus quotes in temptation / first and last
    "5_5_12": ["40_12_8", "66_1_10"],       # Sabbath command / Son of Man Lord of Sabbath / Lord's Day
    "5_5_16": ["49_6_2", "40_15_4"],        # Honor father and mother / promise attached / Jesus affirms command
    "5_5_17": ["59_4_2", "40_5_21"],        # Do not murder / James on murder from desire / Jesus intensifies
    "5_5_18": ["40_5_27", "59_4_4"],        # Do not commit adultery / Jesus intensifies / desire = adultery
    "5_5_19": ["45_13_9", "49_4_28"],       # Do not steal / love fulfills law / work to give to needy
    "5_5_21": ["45_7_7", "45_13_9"],        # Do not covet / law reveals covetousness / love fulfills law
    "5_5_29": ["26_36_26", "24_32_39"],     # Oh that they would always fear / new heart prophecy / new covenant

    # Chapter 6
    "5_6_4":  ["41_12_29", "40_22_37"],     # Shema - God is one / Jesus quotes Mark 12:29 / greatest commandment
    "5_6_5":  ["40_22_37", "41_12_30"],     # Love God with all heart / greatest commandment Matt / Mark
    "5_6_6":  ["24_31_33", "45_10_8"],      # Commands on heart / new covenant law on hearts / word near you
    "5_6_7":  ["49_6_4", "20_22_6"],        # Teach children diligently / fathers in Christ / train a child
    "5_6_13": ["40_4_10", "42_4_8"],        # Worship God alone / Jesus quotes Deut against Satan / Luke parallel
    "5_6_16": ["40_4_7", "42_4_12"],        # Do not test God / Jesus quotes Deut / Luke parallel
    "5_6_18": ["40_5_6", "43_10_10"],       # Do what is right / blessed are those who hunger / life abundant
    "5_6_24": ["23_48_17", "59_1_25"],      # Fear God for our good / God teaches what is best / law of liberty
    "5_6_25": ["45_10_4", "48_2_16"],       # Righteousness from keeping commands → Christ our righteousness

    # Chapter 7
    "5_7_6":  ["60_2_9", "49_1_4"],         # Holy people, treasured possession / royal priesthood / chosen in him
    "5_7_9":  ["45_8_28", "24_32_40"],      # Faithful God keeping covenant / all works for good / everlasting covenant
    "5_7_13": ["48_3_14", "40_6_33"],       # God blesses obedience / Christ redeems curse / seek kingdom first
    "5_7_21": ["45_8_31", "66_19_15"],      # God mighty among you / who can stand against / God's power
    "5_7_26": ["44_19_19", "46_10_21"],     # Do not bring abomination home / Ephesus book burning / flee idolatry

    # Chapter 8
    "5_8_2":  ["40_4_1", "42_4_2"],         # Led in wilderness to test / Jesus led by Spirit to wilderness
    "5_8_3":  ["40_4_4", "42_4_4"],         # Man not live by bread alone / Jesus quotes against Satan / Luke parallel
    "5_8_5":  ["20_3_12", "58_12_6"],       # Lord disciplines as father / do not despise discipline / Heb12 discipline
    "5_8_10": ["42_22_19", "54_4_4"],       # Eat and bless the Lord / thanksgiving at Supper / godliness with contentment
    "5_8_17": ["46_4_7", "44_3_12"],        # My power got this wealth / God's power in weakness / by God's grace
    "5_8_18": ["44_14_16", "19_24_1"],      # God gives power to get wealth / Spirit given / earth is Lord's
    "5_8_19": ["44_14_15", "45_1_18"],      # Turn to other gods = perish / wrath of God / death

    # Chapter 9-11
    "5_9_4":  ["45_3_27", "45_9_30"],       # Not by your righteousness / no boasting / righteousness by faith
    "5_9_6":  ["48_2_16", "45_3_28"],       # Stubborn; not because righteous / not by works / justified by faith
    "5_10_12": ["33_6_8", "40_22_37"],      # What God requires / Micah parallel / great commandment
    "5_10_16": ["45_2_29", "51_2_11"],      # Circumcise heart / true Jew inward / circumcision not made by hands
    "5_10_17": ["44_10_34", "45_2_11"],     # No partiality / Cornelius / God shows no partiality
    "5_10_18": ["59_1_27", "42_18_7"],      # Loves stranger, widow, orphan / pure religion / God vindicates
    "5_10_20": ["40_4_10", "45_14_11"],     # Fear and serve only God / Jesus quotes / every knee shall bow
    "5_11_1":  ["62_5_3", "43_14_15"],      # Love God and keep commands / love shown by obedience / 1 John 5
    "5_11_13": ["43_14_21", "62_2_5"],      # Love me, keep commands / if you love me / 1 John 2
    "5_11_18": ["51_3_16", "49_6_17"],      # Store up words / let word dwell richly / sword of Spirit
    "5_11_26": ["48_3_13", "48_3_10"],      # Blessing and curse / Christ redeemed curse of law / under law's curse

    # Chapter 12-16
    "5_12_32": ["66_22_18", "20_30_6"],     # Do not add/subtract / Rev warning / Proverbs warning
    "5_13_3":  ["40_24_24", "65_3"],        # Test - false prophets with signs / false christs / contend for faith
    "5_13_4":  ["62_5_3", "40_4_10"],       # Follow God alone / love and obey / worship God only
    "5_14_2":  ["60_2_9", "66_5_10"],       # Holy people chosen / royal priesthood / kingdom of priests
    "5_15_4":  ["44_4_34", "47_8_14"],      # No poor among you / early church sharing / Macedonian generosity
    "5_15_7":  ["42_6_30", "47_9_6"],       # Give to the poor / give to who asks / generous sowing
    "5_15_11": ["40_26_11", "43_12_8"],     # Poor always with you / Jesus' response / always poor among you
    "5_16_16": ["43_7_2", "44_2_5"],        # Appear before God 3 times / Passover / gathering in Jerusalem

    # Chapter 17-20
    "5_17_6":  ["40_18_16", "43_8_17"],     # Two witnesses required / church discipline / testimony of two
    "5_17_15": ["43_1_49", "45_13_1"],      # King from among brothers / Nathanael's confession / governing authorities
    "5_17_17": ["54_6_10", "40_6_24"],      # King not multiply gold / love of money / cannot serve God and money
    "5_18_15": ["44_3_22", "44_7_37"],      # Prophet like Moses = Christ / Peter quotes / Stephen quotes
    "5_18_18": ["43_6_14", "43_1_21"],      # I will raise prophet like you / Jesus as prophet / people asked
    "5_18_19": ["44_3_23", "58_2_3"],       # Listen to the prophet / whoever doesn't hear = cut off / great salvation
    "5_18_20": ["40_7_15", "24_14_14"],     # False prophets test / beware false prophets / false prophets
    "5_19_15": ["40_18_16", "47_13_1"],     # Two or three witnesses / church discipline / confirmed by witnesses
    "5_20_1":  ["45_8_31", "40_10_28"],     # Do not fear enemy armies / God for us / fear not those who kill body
    "5_20_4":  ["23_41_10", "66_19_11"],    # God fights for you / do not fear I am with you / warrior on white horse

    # Chapter 21-26
    "5_21_23": ["48_3_13", "60_2_24"],      # Cursed who hangs on tree / Christ redeemed curse / bore our sins on tree
    "5_22_12": ["40_23_5", "4_15_38"],      # Tassels on garments / Pharisees make them long / God's command
    "5_23_25": ["40_12_1", "41_2_23"],      # Plucking grain on Sabbath / disciples pluck grain / Pharisees question
    "5_24_1":  ["40_5_31", "40_19_7"],      # Certificate of divorce / Jesus on divorce Sermon / Pharisees question Jesus
    "5_24_14": ["59_5_4", "54_5_18"],       # Do not oppress worker / wages withheld cry out / laborer deserves wages
    "5_24_15": ["42_10_7", "59_5_4"],       # Pay worker same day / laborer deserves pay / James on withheld wages
    "5_25_4":  ["46_9_9", "54_5_18"],       # Do not muzzle ox / applied to ministers / elder who leads well
    "5_26_5":  ["44_7_9", "1_46_3"],        # Wandering Aramean my father / Stephen's speech / Jacob in Egypt
    "5_26_17": ["45_6_16", "62_4_15"],      # You have proclaimed Lord your God / God's children / abide in him

    # Chapter 27-28
    "5_27_26": ["48_3_10", "48_3_13"],      # Cursed who doesn't keep all law / all under curse / Christ redeems
    "5_28_1":  ["40_6_33", "23_1_19"],      # Obey = blessings / seek kingdom first / if willing and obedient
    "5_28_2":  ["40_5_3", "19_1_1"],        # Blessings overtake obedient / Beatitudes / Psalm 1 blessed man
    "5_28_10": ["45_1_7", "66_3_12"],       # Called by God's name / predestined / new name on pillar
    "5_28_12": ["42_6_38", "39_3_10"],      # God opens treasury / give and it shall be given / tithe and test God
    "5_28_15": ["48_3_10", "45_6_23"],      # Curses for disobedience / all under law's curse / wages of sin is death
    "5_28_66": ["43_5_24", "45_8_1"],       # Life hanging in doubt / passed from death to life / no condemnation in Christ

    # Chapter 29-30
    "5_29_4":  ["45_11_8", "23_6_10"],      # Spirit of stupor / God gave them over / ears heavy, eyes shut
    "5_29_18": ["58_12_15", "44_8_23"],     # Bitter root / Heb warning against root of bitterness / gall and bitterness
    "5_29_23": ["42_17_29", "65_7"],        # Like Sodom and Gomorrah / fire on Sodom / Sodom as example
    "5_29_29": ["45_11_33", "46_2_10"],     # Secret things belong to God / depth of God's wisdom / Spirit searches
    "5_30_2":  ["44_3_19", "24_3_22"],      # Return to Lord / repent and turn / return for mercies are new
    "5_30_6":  ["26_36_26", "45_2_29"],     # Circumcise your heart / new heart and spirit / Jew inwardly
    "5_30_10": ["42_15_20", "24_29_13"],    # Return with whole heart / prodigal father runs / seek me and find
    "5_30_12": ["45_10_6", "45_10_7"],      # Not in heaven / don't say who will bring Christ down / righteousness by faith
    "5_30_14": ["45_10_8", "45_10_9"],      # Word near you in mouth / confess and believe / word of faith
    "5_30_15": ["43_10_10", "45_6_23"],     # Life or death set before you / life abundant / gift of God = life
    "5_30_19": ["43_3_16", "19_27_1"],      # Choose life / God so loved / Lord is my life / light

    # Chapter 31-34
    "5_31_6":  ["58_13_5", "43_14_18"],     # Be strong, God will not forsake / I will never leave / not leave orphans
    "5_31_8":  ["40_28_20", "45_8_38"],     # God goes before you / I am with you always / nothing separates
    "5_31_12": ["44_2_42", "49_4_11"],      # Gather all to hear / devoted to teaching / pastors to equip
    "5_31_19": ["51_3_16", "19_119_11"],    # Write this song / Word to dwell / Word hidden in heart
    "5_32_4":  ["60_1_17", "66_15_3"],      # The Rock, perfect work / God judges rightly / true and just ways
    "5_32_8":  ["44_17_26", "45_9_5"],      # God divided nations / he made every nation / Israel's adoption
    "5_32_17": ["46_10_20", "19_106_37"],   # Sacrificed to demons / idol sacrifices are demonic / child sacrifice
    "5_32_21": ["45_10_19", "45_11_11"],    # Make them jealous / I will make Israel jealous / have they stumbled
    "5_32_35": ["45_12_19", "58_10_30"],    # Vengeance is mine / do not avenge / Lord will judge
    "5_32_36": ["58_10_30", "19_135_14"],   # Lord judges his people / Lord vindicates / Lord will vindicate
    "5_32_43": ["45_15_10", "66_19_2"],     # Rejoice O Gentiles / praise the Lord O Gentiles Rom15 / hallelujah
    "5_33_2":  ["48_3_19", "44_7_53"],      # Law given through angels / law ordained through angels / received law
    "5_33_12": ["43_13_23", "49_1_4"],      # Beloved rests securely / disciple whom Jesus loved / chosen in him
    "5_34_5":  ["65_9", "44_2_11"],         # Death of Moses / Michael and Moses' body in Jude / Moses at transfiguration
    "5_34_9":  ["58_6_2", "44_6_3"],        # Joshua filled with wisdom / elementary teachings / wisdom given by Spirit
    "5_34_10": ["40_11_27", "43_1_18"],     # No prophet like Moses / Jesus reveals Father / the Son alone knows

    # ===== JOSHUA =====

    # Chapter 1
    "6_1_2":  ["58_4_1", "40_11_28"],       # Enter the land / Sabbath rest / come to me for rest
    "6_1_5":  ["58_13_5", "40_28_20"],      # No man shall stand / I will never leave / with you always
    "6_1_6":  ["55_2_1", "49_6_10"],        # Be strong and courageous / be strong in grace / put on full armor
    "6_1_7":  ["19_1_2", "54_4_13"],        # Meditate on law / Psalm 1 blessed man / godliness with contentment
    "6_1_8":  ["19_119_11", "59_1_25"],     # Meditate day and night / word hidden in heart / law of liberty
    "6_1_9":  ["40_28_20", "43_14_27"],     # Be strong God is with you / I am with you always / my peace I give
    "6_1_11": ["43_14_2", "58_4_9"],        # Cross over to possess / rooms in Father's house / Sabbath rest remains
    "6_1_18": ["55_2_1", "44_5_29"],        # Obey and be strong / be strong in grace / obey God not men

    # Chapter 2
    "6_2_1":  ["58_11_31", "59_2_25"],      # Rahab / by faith Rahab / justified by works (Rahab)
    "6_2_9":  ["44_4_13", "23_41_14"],      # Nations melted in fear / with God all are filled / none against us
    "6_2_11": ["43_3_16", "1_14_22"],       # God of heaven and earth / so God loved world / Abram believed God
    "6_2_12": ["40_10_32", "45_1_16"],      # Rahab's kindness / confess Christ publicly / not ashamed of gospel
    "6_2_18": ["58_9_12", "60_1_18"],       # Scarlet cord / blood of Christ / redeemed by precious blood
    "6_2_21": ["40_1_21", "45_5_9"],        # Salvation by scarlet / Jesus saves / justified by his blood

    # Chapter 3
    "6_3_4":  ["43_10_27", "23_40_3"],      # Follow the ark (God's presence) / sheep follow shepherd / prepare the way
    "6_3_5":  ["40_3_2", "23_35_8"],        # Consecrate yourselves / repent kingdom near / holy way
    "6_3_10": ["58_10_31", "40_22_32"],     # Living God / fall into hands of living God / God of the living
    "6_3_13": ["44_7_36", "45_6_4"],        # Waters cut off / Red Sea typology / buried with Christ in baptism
    "6_3_17": ["46_10_2", "60_3_21"],       # Crossed on dry ground / in the cloud and sea / baptism now saves

    # Chapter 4
    "6_4_6":  ["42_22_19", "44_2_42"],      # Stone memorial / do this in remembrance / breaking of bread
    "6_4_7":  ["19_77_11", "23_51_10"],     # Memorial of crossing / I will remember deeds of Lord / arm of Lord
    "6_4_14": ["43_5_23", "40_8_27"],       # Magnified Joshua / who is this that men follow / men marveled
    "6_4_21": ["19_78_4", "49_6_4"],        # Tell your children / declare to next generation / fathers teach
    "6_4_24": ["23_52_10", "19_98_3"],      # All earth sees hand of Lord / revealed arm / all ends of earth

    # Chapter 5
    "6_5_2":  ["51_2_11", "45_2_29"],       # Circumcision at Gilgal / not made by hands / inward circumcision
    "6_5_6":  ["58_3_18", "19_95_11"],      # Wilderness generation died / they shall not enter / rest
    "6_5_9":  ["47_5_17", "48_6_15"],       # Reproach of Egypt rolled away / new creation / circumcision of Christ
    "6_5_10": ["46_5_7", "40_26_17"],       # Kept Passover / Christ our Passover sacrificed / Last Supper
    "6_5_12": ["43_6_31", "43_6_49"],       # Manna ceased in promised land / bread from heaven / ancestors ate manna
    "6_5_14": ["66_19_10", "40_4_10"],      # Do not worship angel / angel says don't worship / worship God alone
    "6_5_15": ["44_7_33", "2_3_5"],         # Remove sandals, holy ground / Moses holy ground / holy place

    # Chapter 6
    "6_6_2":  ["58_11_30", "40_17_20"],     # God gave Jericho / by faith walls fell / faith moves mountains
    "6_6_17": ["59_2_25", "58_11_31"],      # Rahab shall live / Rahab justified by works / by faith Rahab
    "6_6_20": ["58_11_30", "47_10_4"],      # Walls fell by faith / Heb 11 Jericho / weapons not carnal
    "6_6_26": ["11_16_34", "40_5_37"],      # Curse on Jericho rebuilder / fulfilled under Ahab / let your yes be yes

    # Chapter 7
    "6_7_1":  ["46_5_6", "58_12_15"],       # Achan's sin troubled Israel / sin leavens the whole lump / bitter root
    "6_7_11": ["1_3_11", "45_5_12"],        # Israel has sinned / Adam's sin / sin entered through one man
    "6_7_19": ["43_9_24", "45_3_23"],       # Give glory to God and confess / give glory to God / all have sinned
    "6_7_24": ["46_15_22", "45_5_12"],      # Achan's family suffered / in Adam all die / sin's corporate consequences
    "6_7_25": ["45_6_23", "48_3_10"],       # Achan destroyed / wages of sin / cursed is everyone who sins

    # Chapter 8
    "6_8_1":  ["40_14_27", "23_41_10"],     # Do not fear or be dismayed / be of good cheer / do not fear
    "6_8_30": ["5_27_5", "43_4_20"],        # Altar on Ebal / blessings and curses enacted / Samaritan worship
    "6_8_34": ["45_10_4", "42_4_16"],       # Read all the law / Christ is end of law / scripture fulfilled
    "6_8_35": ["40_4_4", "2_24_7"],         # Read every word / live by every word / book of covenant read

    # Chapter 9
    "6_9_14": ["20_3_6", "59_4_13"],        # Did not ask counsel of God / trust God not self / plans without God
    "6_9_15": ["48_3_15", "19_105_8"],      # Covenant with Gibeonites honored / covenant / God remembers forever
    "6_9_27": ["43_4_23", "40_12_6"],       # Temple servants / true worshipers / one greater than temple

    # Chapter 10
    "6_10_12": ["44_2_22", "23_38_8"],      # Sun stood still / signs and wonders / sun went back
    "6_10_14": ["45_8_28", "43_11_43"],     # No day like it / God works all / commanded and it was done
    "6_10_25": ["45_8_31", "66_19_21"],     # Do not fear / if God for us / enemies defeated under feet
    "6_10_42": ["45_8_31", "19_44_3"],      # God fought for Israel / God for us / not by their sword

    # Chapter 11
    "6_11_6":  ["23_41_10", "40_10_28"],    # Do not be afraid / do not fear / fear God not man
    "6_11_15": ["43_15_10", "58_5_9"],      # Joshua obeyed fully / if you keep my commands / obedient to death
    "6_11_23": ["58_4_1", "40_11_28"],      # Rest from war / sabbath rest remains / come to me for rest

    # Chapters 12-15
    "6_12_24": ["45_4_8", "66_5_5"],        # Many kings defeated / more than conquerors / elders before throne
    "6_13_1":  ["43_14_2", "66_21_7"],      # Much land still to take / many dwelling places / overcomer inherits
    "6_13_14": ["4_18_20", "45_15_27"],     # Levites inherit God not land / ministers of altar / share spiritual blessings
    "6_14_9":  ["40_5_5", "58_4_3"],        # Land promised to Caleb / meek inherit earth / fear to enter rest
    "6_14_11": ["23_40_31", "50_4_13"],     # Still strong at 85 / renewed strength / through Christ who strengthens
    "6_14_12": ["50_4_13", "40_17_20"],     # Give me this hill country / all things through Christ / faith moves mountains
    "6_14_14": ["58_3_14", "4_14_24"],      # Wholly followed the Lord / hold firm if we hold / Caleb's faith

    # Chapter 15-19
    "6_15_63": ["7_1_19", "40_1_17"],       # Jebusites not driven out / Judah couldn't drive out / partial obedience
    "6_17_13": ["7_1_28", "45_7_23"],       # Forced labor not driven out / compromise / slave to sin
    "6_19_51": ["43_14_2", "66_21_22"],     # Finished dividing the land / many rooms / no temple for God is temple

    # Chapter 20
    "6_20_2":  ["58_6_18", "4_35_11"],      # Cities of refuge / flee to lay hold of hope / cities designated
    "6_20_3":  ["45_8_1", "45_8_34"],       # Manslayer flees for mercy / no condemnation / Christ condemns sin
    "6_20_9":  ["45_8_33", "43_5_24"],      # Not die before standing trial / who brings charge / passed from death

    # Chapter 21
    "6_21_43": ["1_13_15", "1_15_18"],      # God gave all land / Abrahamic promise / covenant land grant
    "6_21_44": ["23_55_11", "45_4_21"],     # Not one word failed / word does not return void / hope does not disappoint
    "6_21_45": ["40_5_18", "66_3_14"],      # Every promise fulfilled / not one jot of law / I am coming soon

    # Chapter 22
    "6_22_5":  ["43_14_15", "5_6_5"],       # Love God, walk in ways / if you love me obey / Shema
    "6_22_22": ["43_17_3", "5_4_35"],       # God of gods knows / eternal life to know God / no other God
    "6_22_27": ["40_10_32", "45_1_16"],     # Witness to future generations / confess before men / not ashamed

    # Chapter 23
    "6_23_6":  ["54_4_16", "45_15_4"],      # Be careful to keep law / profitable Scripture / written for learning
    "6_23_8":  ["44_11_23", "62_2_6"],      # Hold fast to Lord / with purpose of heart / abide in him
    "6_23_11": ["5_6_5", "40_22_37"],       # Love the Lord your God / Shema / greatest commandment
    "6_23_14": ["23_55_11", "47_1_20"],     # Every good promise fulfilled / word doesn't fail / all God's promises Yes
    "6_23_15": ["48_6_7", "45_1_18"],       # Bad things will come for disobedience / reap what you sow / wrath revealed
    "6_23_16": ["45_1_18", "48_3_10"],      # Break covenant = perish / wrath against ungodliness / law's curse

    # Chapter 24
    "6_24_2":  ["1_11_31", "44_7_2"],       # Your fathers served other gods / Abraham's father / Stephen's speech
    "6_24_14": ["42_16_13", "40_6_24"],     # Serve God sincerely / can't serve two masters / God or mammon
    "6_24_15": ["44_16_31", "45_6_23"],     # Choose whom to serve / believe in Lord Jesus / gift of God is life
    "6_24_19": ["43_17_11", "23_5_16"],     # Holy God, jealous God / keep them in your name / holy city
    "6_24_22": ["40_10_32", "44_5_32"],     # You are witnesses / confess before men / witnesses
    "6_24_24": ["45_10_9", "43_14_6"],      # We will serve the Lord / confess Jesus is Lord / I am the way
    "6_24_26": ["1_28_18", "40_21_42"],     # Stone as witness / pillar/gateway / cornerstone
    "6_24_31": ["43_15_5", "58_3_19"],      # Served Lord all Joshua's days / abide in me / enter his rest
}

# Add new refs, merging with existing
added = 0
merged = 0
for key, refs in new_xrefs.items():
    if key in data:
        existing = data[key]
        new_refs = [r for r in refs if r not in existing]
        if new_refs:
            data[key] = existing + new_refs
            merged += 1
            added += len(new_refs)
    else:
        data[key] = refs
        added += len(refs)

with open(XREF_FILE, "w") as f:
    json.dump(data, f, separators=(",", ":"))

after_count = len(data)
new_entries = after_count - before_count

print(f"Before: {before_count} entries")
print(f"After:  {after_count} entries")
print(f"New keys added: {new_entries}")
print(f"Merged refs into existing: {merged} keys")
print(f"Total new refs added: {added}")

# Verify Deut and Josh coverage
deut_keys = [k for k in data if k.startswith("5_")]
josh_keys = [k for k in data if k.startswith("6_")]
print(f"Deuteronomy entries: {len(deut_keys)}")
print(f"Joshua entries: {len(josh_keys)}")
