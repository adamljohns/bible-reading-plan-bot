"""MBT 1 Timothy — 6 chapters, 113 verses. Book ID 54."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, an apostle of Christ Jesus by the command of God our Savior, and of Christ Jesus our hope —",
    2: "to Timothy, my true child in the faith: Grace, mercy, and peace from God the Father and Christ Jesus our Lord.",
    3: "As I urged you when I was leaving for Macedonia — remain in Ephesus, so that you may instruct certain men not to teach a different doctrine,",
    4: "nor to give attention to myths and endless genealogies, which give rise to mere speculations rather than the stewardship from God which is by faith.",
    5: "But the goal of our instruction is love — out of a pure heart, and a good conscience, and a sincere faith.",
    6: "Some have wandered away from these things, and have turned aside to fruitless discussion —",
    7: "wanting to be teachers of the Law, even though they do not understand either what they are saying, or the matters about which they make confident assertions.",
    8: "But we know that the Law is good, if anyone uses it lawfully —",
    9: "knowing this: that the Law is not made for a righteous man, but for those who are lawless and rebellious, for the ungodly and sinners, for the unholy and profane, for those who kill their fathers or mothers, for murderers,",
    10: "for the sexually immoral, for those who practice homosexuality, for kidnappers, for liars, for perjurers, and whatever else is contrary to sound teaching —",
    11: "according to the gospel of the glory of the blessed God, with which I have been entrusted.",
    12: "I thank Him who has strengthened me — Christ Jesus our Lord — because He considered me faithful, putting me into service,",
    13: "even though I was formerly a blasphemer and a persecutor and a violent aggressor. Yet I was shown mercy, because I had acted ignorantly in unbelief.",
    14: "And the grace of our Lord overflowed for me — with the faith and love which are in Christ Jesus.",
    15: "This saying is faithful and worthy of full acceptance: Christ Jesus came into the world to save sinners — of whom I am foremost.",
    16: "Yet for this reason I was shown mercy: so that in me, the foremost, Jesus Christ might display His perfect patience as an example to those who would believe in Him for eternal life.",
    17: "Now to the King eternal — immortal, invisible, the only God — be honor and glory forever and ever. Amen.",
    18: "This charge I entrust to you, Timothy my child — in accordance with the prophecies previously made concerning you — that by them you may fight the good fight,",
    19: "keeping faith and a good conscience. Some have rejected these and have suffered shipwreck in regard to their faith.",
    20: "Among these are Hymenaeus and Alexander — whom I have handed over to Satan, so that they will be taught not to blaspheme.",
}
ch2 = {
    1: "First of all, then, I urge that supplications, prayers, intercessions, and thanksgivings be made on behalf of all people —",
    2: "for kings and all who are in authority — so that we may lead a tranquil and quiet life in all godliness and dignity.",
    3: "This is good and acceptable in the sight of God our Savior,",
    4: "who desires all people to be saved, and to come to the full knowledge of the truth.",
    5: "For there is one God — and one mediator also between God and men: the man Christ Jesus,",
    6: "who gave Himself as a ransom for all — the testimony given at the proper time.",
    7: "For this purpose I was appointed a herald and an apostle — I am telling the truth, I am not lying — a teacher of the Gentiles in faith and truth.",
    8: "Therefore I want the men in every place to pray, lifting up holy hands — without anger and disputing.",
    9: "Likewise, I want women to adorn themselves with proper clothing, modestly and discreetly — not with braided hair, and gold, or pearls, or costly garments,",
    10: "but rather, by means of good works, as is fitting for women making a claim to godliness.",
    11: "Let a woman quietly receive instruction with full submissiveness.",
    12: "But I do not allow a woman to teach or to exercise authority over a man — but to remain quiet.",
    13: "For it was Adam who was first formed, and then Eve.",
    14: "And it was not Adam who was deceived, but the woman, being deceived, fell into transgression.",
    15: "But women will be preserved through the bearing of children — if they continue in faith and love and sanctity, with self-restraint.",
}
ch3 = {
    1: "This saying is faithful: if any man aspires to the office of overseer, it is a fine work he desires to do.",
    2: "An overseer, then, must be above reproach — the husband of one wife, sober-minded, prudent, respectable, hospitable, able to teach,",
    3: "not addicted to wine, not violent — but gentle, not quarrelsome, not loving money;",
    4: "managing his own household well — keeping his children under control with all dignity",
    5: "(for if a man does not know how to manage his own household, how will he take care of the church of God?);",
    6: "and not a new convert — so that he will not become conceited and fall into the condemnation incurred by the devil.",
    7: "And he must have a good reputation with those outside the church — so that he will not fall into reproach and the snare of the devil.",
    8: "Deacons likewise must be men of dignity — not double-tongued, or addicted to much wine, or fond of dishonest gain;",
    9: "but holding the mystery of the faith with a clear conscience.",
    10: "And these too should first be tested — then let them serve as deacons, if they are beyond reproach.",
    11: "Women must likewise be dignified, not malicious gossips, but sober-minded — faithful in all things.",
    12: "Deacons must be husbands of only one wife — managing their children and their own households well.",
    13: "For those who have served well as deacons obtain for themselves a high standing — and great confidence in the faith that is in Christ Jesus.",
    14: "I am writing these things to you — hoping to come to you before long.",
    15: "But in case I am delayed, I write so that you will know how one ought to conduct himself in the household of God — which is the church of the living God, the pillar and support of the truth.",
    16: "And by common confession, great is the mystery of godliness: He who was revealed in the flesh, was vindicated in the Spirit, was seen by angels, was proclaimed among the nations, was believed on in the world, was taken up in glory.",
}
ch4 = {
    1: "But the Spirit explicitly says that in later times some will fall away from the faith — paying attention to deceitful spirits and to doctrines of demons,",
    2: "by means of the hypocrisy of liars seared in their own conscience as with a branding iron,",
    3: "men who forbid marriage, and who advocate abstaining from foods which God has created to be gratefully shared in by those who believe and know the truth.",
    4: "For everything created by God is good — and nothing is to be rejected, if it is received with gratitude;",
    5: "for it is sanctified by means of the word of God and prayer.",
    6: "In pointing out these things to the brothers, you will be a good servant of Christ Jesus — constantly nourished on the words of the faith and of the sound doctrine which you have been following.",
    7: "But have nothing to do with worldly fables fit only for old women. On the other hand, train yourself for the purpose of godliness.",
    8: "For bodily training is of little profit — but godliness is profitable for all things, since it holds promise for the present life and also for the life to come.",
    9: "This saying is faithful and worthy of full acceptance.",
    10: "For it is for this we labor and strive — because we have set our hope on the living God, who is the Savior of all men, especially of believers.",
    11: "Prescribe and teach these things.",
    12: "Let no one look down on your youthfulness — but rather, in speech, conduct, love, faith, and purity, show yourself an example of those who believe.",
    13: "Until I come, give your attention to the public reading, to exhortation, and to teaching.",
    14: "Do not neglect the spiritual gift within you — which was given to you through prophecy with the laying on of hands by the council of elders.",
    15: "Take pains with these things — be absorbed in them, so that your progress will be evident to all.",
    16: "Pay close attention to yourself and to your teaching. Persevere in these things — for as you do this, you will save both yourself and those who hear you.",
}
ch5 = {
    1: "Do not sharply rebuke an older man — but rather appeal to him as a father; and to the younger men, as brothers;",
    2: "the older women, as mothers; the younger women, as sisters — in all purity.",
    3: "Honor widows who are widows indeed.",
    4: "But if any widow has children or grandchildren, let them first learn to practice piety in regard to their own family — and to make some return to their parents. For this is acceptable in the sight of God.",
    5: "Now she who is truly a widow — and who has been left alone — has fixed her hope on God, and continues in supplications and prayers night and day.",
    6: "But she who lives in indulgent pleasure is dead, even while she lives.",
    7: "Prescribe these things as well, so that they may be above reproach.",
    8: "But if anyone does not provide for his own — and especially for those of his household — he has denied the faith, and is worse than an unbeliever.",
    9: "Let a widow be enrolled who is not less than sixty years old — having been the wife of one man,",
    10: "having a reputation for good works: if she has brought up children, if she has shown hospitality to strangers, if she has washed the saints' feet, if she has assisted those in distress, and if she has devoted herself to every good work.",
    11: "But refuse to enroll younger widows — for when they feel sensual desires in disregard of Christ, they want to get married,",
    12: "thus incurring condemnation, because they have set aside their previous pledge.",
    13: "And at the same time they also learn to be idle — going from house to house. And not merely idle, but also gossips and busybodies, talking about things they ought not to mention.",
    14: "Therefore, I want younger widows to get married, bear children, keep house, and give the enemy no occasion for reproach.",
    15: "For some have already turned aside to follow Satan.",
    16: "If any believing woman has dependent widows, she must assist them — and the church must not be burdened, so that it may assist those who are widows indeed.",
    17: "The elders who rule well are to be considered worthy of double honor — especially those who work hard at preaching and teaching.",
    18: "For the Scripture says, \"You shall not muzzle the ox while it is threshing,\" and, \"The laborer is worthy of his wages.\"",
    19: "Do not receive an accusation against an elder, except on the basis of two or three witnesses.",
    20: "Those who continue in sin, rebuke in the presence of all — so that the rest also may be fearful of sinning.",
    21: "I solemnly charge you in the presence of God and of Christ Jesus and of His chosen angels — to maintain these principles without bias, doing nothing in a spirit of partiality.",
    22: "Do not lay hands upon anyone too hastily — and do not share responsibility for the sins of others. Keep yourself pure.",
    23: "No longer drink water exclusively, but use a little wine for the sake of your stomach and your frequent ailments.",
    24: "The sins of some men are quite evident, going before them to judgment. For others, their sins follow after.",
    25: "Likewise also, deeds that are good are quite evident — and those which are otherwise cannot be concealed.",
}
ch6 = {
    1: "All who are under the yoke as slaves are to regard their own masters as worthy of all honor — so that the name of God and our doctrine will not be spoken against.",
    2: "Those who have believers as their masters must not be disrespectful to them because they are brothers — but they must serve them all the more, because those who partake of the benefit are believers and beloved. Teach and preach these principles.",
    3: "If anyone advocates a different doctrine, and does not agree with sound words — those of our Lord Jesus Christ — and with the doctrine conforming to godliness,",
    4: "he is conceited, and understands nothing. But he has a sick craving for controversial questions and disputes about words — out of which arise envy, strife, abusive language, evil suspicions,",
    5: "and constant friction between men of depraved mind and deprived of the truth — who suppose that godliness is a means of gain.",
    6: "But godliness, with contentment, is great gain.",
    7: "For we have brought nothing into the world — and we cannot take anything out of it either.",
    8: "And if we have food and covering, with these we shall be content.",
    9: "But those who want to get rich fall into temptation and a snare, and many foolish and harmful desires — which plunge men into ruin and destruction.",
    10: "For the love of money is a root of all sorts of evil — and some, by longing for it, have wandered away from the faith and pierced themselves with many griefs.",
    11: "But you, O man of God — flee from these things, and pursue righteousness, godliness, faith, love, perseverance, and gentleness.",
    12: "Fight the good fight of faith. Take hold of the eternal life to which you were called — and for which you made the good confession in the presence of many witnesses.",
    13: "I charge you in the presence of God — who gives life to all things — and of Christ Jesus, who testified the good confession before Pontius Pilate,",
    14: "that you keep the commandment without stain or reproach until the appearing of our Lord Jesus Christ —",
    15: "which He will bring about at the proper time. He is the blessed and only Sovereign — the King of kings and Lord of lords —",
    16: "who alone has immortality — dwelling in unapproachable light, whom no man has seen or can see. To Him be honor and eternal dominion. Amen.",
    17: "Instruct those who are rich in this present world not to be conceited, or to fix their hope on the uncertainty of riches — but on God, who richly supplies us with all things to enjoy.",
    18: "Instruct them to do good, to be rich in good works, to be generous and ready to share —",
    19: "storing up for themselves the treasure of a good foundation for the future — so that they may take hold of that which is life indeed.",
    20: "O Timothy, guard what has been entrusted to you — avoiding worldly and empty chatter, and the opposing arguments of what is falsely called knowledge.",
    21: "Some have professed it, and have gone astray from the faith. Grace be with you.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5, 6: ch6}

def main():
    new_entries = {f"54_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"1 Timothy total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 1 Timothy verses")

if __name__ == "__main__":
    main()
