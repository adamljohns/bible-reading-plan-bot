"""MBT James — 5 chapters, 108 verses. Book ID 59. James (Jesus' brother)
on practical wisdom, faith and works, the tongue, prayer."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "James, a bondservant of God and of the Lord Jesus Christ — to the twelve tribes scattered abroad: Greetings.",
    2: "Consider it pure joy, my brothers, whenever you encounter trials of various kinds —",
    3: "knowing that the testing of your faith produces steadfastness.",
    4: "And let steadfastness have its full effect — so that you may be mature and complete, lacking in nothing.",
    5: "If any of you lacks wisdom, let him ask of God — who gives generously to all without reproach — and it will be given to him.",
    6: "But let him ask in faith, doubting nothing — for the one who doubts is like the surf of the sea, driven and tossed by the wind.",
    7: "That person should not expect to receive anything from the Lord —",
    8: "he is a double-minded man, unstable in all his ways.",
    9: "But let the brother of humble circumstances boast in his exaltation,",
    10: "and the rich man, in his humiliation — because like a flower of the grass, he will pass away.",
    11: "For the sun rises with its scorching heat, and withers the grass — and its flower falls off, and the beauty of its appearance is destroyed. So also the rich man, in the midst of his pursuits, will fade away.",
    12: "Blessed is the man who endures trial — for once he has been approved, he will receive the crown of life, which the Lord has promised to those who love Him.",
    13: "Let no one say when he is tempted, \"I am being tempted by God.\" For God cannot be tempted by evil, and He Himself tempts no one.",
    14: "But each one is tempted, when he is dragged away and enticed by his own lust.",
    15: "Then, when lust has conceived, it gives birth to sin — and sin, when it has run its course, brings forth death.",
    16: "Do not be deceived, my beloved brothers.",
    17: "Every good gift and every perfect gift is from above — coming down from the Father of lights, with whom there is no variation, nor shifting shadow.",
    18: "In the exercise of His will He brought us forth by the word of truth — so that we would be a kind of firstfruits among His creatures.",
    19: "Know this, my beloved brothers: let everyone be quick to hear, slow to speak, slow to anger.",
    20: "For the anger of man does not produce the righteousness of God.",
    21: "Therefore, putting aside all filthiness and all the abundance of wickedness, in humility receive the implanted word — which is able to save your souls.",
    22: "But be doers of the word, and not hearers only — deceiving yourselves.",
    23: "For if anyone is a hearer of the word and not a doer, he is like a man who looks at his natural face in a mirror.",
    24: "For he looks at himself, and goes away, and immediately forgets what kind of man he was.",
    25: "But the one who looks intently into the perfect law — the law of liberty — and continues in it, not having become a forgetful hearer but a doer of the work — this man will be blessed in what he does.",
    26: "If anyone considers himself religious, and yet does not bridle his tongue, but deceives his own heart — this man's religion is worthless.",
    27: "Pure religion and undefiled before our God and Father is this: to visit orphans and widows in their distress — and to keep oneself unstained by the world.",
}
ch2 = {
    1: "My brothers, do not hold the faith of our Lord Jesus Christ, the Lord of glory, with an attitude of partiality.",
    2: "For if a man comes into your assembly with a gold ring and fine clothing — and a poor man also comes in dirty clothes —",
    3: "and you pay special attention to the one wearing the fine clothing, and say, \"You sit here in a good place,\" and to the poor one, \"You stand there,\" or, \"Sit down by my footstool\" —",
    4: "have you not made distinctions among yourselves, and become judges with evil thoughts?",
    5: "Listen, my beloved brothers — did not God choose the poor of this world to be rich in faith, and heirs of the kingdom which He promised to those who love Him?",
    6: "But you have dishonored the poor man. Is it not the rich who oppress you and personally drag you into court?",
    7: "Do they not blaspheme the fair name by which you have been called?",
    8: "If, however, you fulfill the royal law according to the Scripture, \"You shall love your neighbor as yourself,\" you are doing well.",
    9: "But if you show partiality, you are committing sin — and are convicted by the law as transgressors.",
    10: "For whoever keeps the whole law and yet stumbles in one point — he has become guilty of all.",
    11: "For He who said, \"Do not commit adultery,\" also said, \"Do not commit murder.\" Now if you do not commit adultery, but do commit murder — you have become a transgressor of the law.",
    12: "So speak and so act, as those who are to be judged by the law of liberty.",
    13: "For judgment will be merciless to one who has shown no mercy. Mercy triumphs over judgment.",
    14: "What use is it, my brothers, if a man says he has faith but he has no works? Can that faith save him?",
    15: "If a brother or sister is without clothing and lacks the daily food,",
    16: "and one of you says to them, \"Go in peace, be warmed and be filled\" — and yet you do not give them what is needed for the body — what use is that?",
    17: "Even so, faith — if it has no works — is dead, being by itself.",
    18: "But someone may well say, \"You have faith, and I have works.\" Show me your faith without the works, and I will show you my faith by my works.",
    19: "You believe that God is one. You do well — the demons also believe, and shudder.",
    20: "But are you willing to recognize, you foolish man, that faith without works is useless?",
    21: "Was not Abraham our father justified by works, when he offered up Isaac his son on the altar?",
    22: "You see that faith was working with his works — and as a result of the works, faith was made complete.",
    23: "And the Scripture was fulfilled, which says, \"And Abraham believed God, and it was reckoned to him as righteousness,\" and he was called the friend of God.",
    24: "You see that a man is justified by works, and not by faith alone.",
    25: "And in the same way, was not Rahab the prostitute also justified by works, when she received the messengers and sent them out by another way?",
    26: "For just as the body without the spirit is dead, so also faith without works is dead.",
}
ch3 = {
    1: "Let not many of you become teachers, my brothers — knowing that as such we will incur a stricter judgment.",
    2: "For we all stumble in many ways. If anyone does not stumble in word, he is a perfect man — able to bridle the whole body as well.",
    3: "Now if we put the bits into the horses' mouths so that they will obey us, we direct their entire body as well.",
    4: "Look at the ships also — though they are so large, and are driven by strong winds — they are turned by a very small rudder, wherever the inclination of the pilot desires.",
    5: "So also the tongue is a small part of the body, and yet it boasts of great things. Behold, how great a forest is set ablaze by such a small fire!",
    6: "And the tongue is a fire — the very world of iniquity. The tongue is set among our members as that which defiles the entire body, and sets on fire the course of our life — and is set on fire by hell.",
    7: "For every species of beasts and birds, of reptiles and creatures of the sea, is tamed and has been tamed by the human race.",
    8: "But no one among men can tame the tongue — it is a restless evil, full of deadly poison.",
    9: "With it we bless our Lord and Father — and with it we curse men, who have been made in the likeness of God.",
    10: "From the same mouth come both blessing and cursing. My brothers, these things ought not to be this way.",
    11: "Does a fountain send out from the same opening both fresh and bitter water?",
    12: "My brothers, can a fig tree produce olives, or a vine, figs? Nor can salt water produce fresh.",
    13: "Who among you is wise and understanding? Let him show by his good behavior his works in the gentleness of wisdom.",
    14: "But if you have bitter envy and selfish ambition in your heart, do not be arrogant and so lie against the truth.",
    15: "This wisdom is not the kind that comes down from above — but is earthly, natural, demonic.",
    16: "For where envy and selfish ambition are, there is disorder and every evil thing.",
    17: "But the wisdom from above is first pure, then peaceable, gentle, willing to yield, full of mercy and good fruits, without partiality, without hypocrisy.",
    18: "And the seed whose fruit is righteousness is sown in peace by those who make peace.",
}
ch4 = {
    1: "What is the source of quarrels and of conflicts among you? Is it not this — that your pleasures wage war within your members?",
    2: "You lust and do not have, so you murder. You are envious and cannot obtain, so you fight and quarrel. You do not have, because you do not ask.",
    3: "You ask and do not receive, because you ask with wrong motives — so that you may spend it on your pleasures.",
    4: "You adulteresses, do you not know that friendship with the world is hostility toward God? Therefore whoever wishes to be a friend of the world makes himself an enemy of God.",
    5: "Or do you think that the Scripture speaks in vain: \"He jealously desires the Spirit which He has made to dwell in us\"?",
    6: "But He gives a greater grace. Therefore it says, \"God opposes the proud, but gives grace to the humble.\"",
    7: "Submit therefore to God. Resist the devil — and he will flee from you.",
    8: "Draw near to God, and He will draw near to you. Cleanse your hands, you sinners — and purify your hearts, you double-minded.",
    9: "Be miserable and mourn and weep. Let your laughter be turned into mourning, and your joy to gloom.",
    10: "Humble yourselves in the presence of the Lord, and He will exalt you.",
    11: "Do not speak against one another, brothers. The one who speaks against a brother, or judges his brother, speaks against the law and judges the law. But if you judge the law, you are not a doer of the law but a judge of it.",
    12: "There is only one Lawgiver and Judge — the One who is able to save and to destroy. But who are you, who judges your neighbor?",
    13: "Come now, you who say, \"Today or tomorrow we will go into such and such a city, and spend a year there, and engage in business and make a profit\" —",
    14: "yet you do not know what your life will be like tomorrow. You are just a vapor that appears for a little while, and then vanishes away.",
    15: "Instead, you ought to say, \"If the Lord wills, we will live and also do this or that.\"",
    16: "But as it is, you boast in your arrogance. All such boasting is evil.",
    17: "Therefore, to one who knows the right thing to do, and does not do it — to him it is sin.",
}
ch5 = {
    1: "Come now, you rich — weep and howl over your miseries which are coming upon you.",
    2: "Your riches have rotted, and your garments have become moth-eaten.",
    3: "Your gold and your silver have rusted; and their rust will be a witness against you, and will consume your flesh like fire. You have stored up your treasure in the last days!",
    4: "Behold, the pay of the laborers who mowed your fields — and which has been withheld by you — cries out against you. And the cries of the harvesters have reached the ears of the Lord of hosts.",
    5: "You have lived luxuriously on the earth, and led a life of wanton pleasure. You have fattened your hearts in a day of slaughter.",
    6: "You have condemned and put to death the righteous one — he does not resist you.",
    7: "Therefore be patient, brothers, until the coming of the Lord. Behold, the farmer waits for the precious produce of the soil — being patient about it, until it gets the early and the late rains.",
    8: "You too be patient. Strengthen your hearts, for the coming of the Lord is near.",
    9: "Do not complain, brothers, against one another — so that you yourselves may not be judged. Behold, the Judge is standing right at the door.",
    10: "As an example, brothers, of suffering and patience, take the prophets who spoke in the name of the Lord.",
    11: "Behold, we count those blessed who have endured. You have heard of the endurance of Job, and have seen the outcome of the Lord's dealings — that the Lord is full of compassion and is merciful.",
    12: "But above all, my brothers, do not swear — neither by heaven, nor by earth, nor by any other oath. But let your yes be yes, and your no, no — so that you may not fall under judgment.",
    13: "Is anyone among you suffering? Let him pray. Is anyone cheerful? Let him sing praises.",
    14: "Is anyone among you sick? Let him call for the elders of the church, and let them pray over him — anointing him with oil in the name of the Lord.",
    15: "And the prayer of faith will save the one who is sick — and the Lord will raise him up. And if he has committed sins, they will be forgiven him.",
    16: "Therefore, confess your sins to one another, and pray for one another, so that you may be healed. The effective prayer of a righteous man can accomplish much.",
    17: "Elijah was a man with a nature like ours — and he prayed earnestly that it would not rain, and it did not rain on the earth for three years and six months.",
    18: "And he prayed again, and the sky poured rain — and the earth produced its fruit.",
    19: "My brothers, if any among you strays from the truth, and one turns him back —",
    20: "let him know that he who turns a sinner from the error of his way will save his soul from death, and will cover a multitude of sins.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5}

def main():
    new_entries = {f"59_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"James total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT James verses")

if __name__ == "__main__":
    main()
