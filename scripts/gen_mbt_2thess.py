"""MBT 2 Thessalonians — 3 chapters, 47 verses. Book ID 53."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, Silvanus, and Timothy — to the church of the Thessalonians, in God our Father and the Lord Jesus Christ:",
    2: "Grace to you, and peace, from God our Father and the Lord Jesus Christ.",
    3: "We are bound to thank God always for you, brothers, as is fitting — because your faith is growing exceedingly, and the love of every one of you for one another is abounding.",
    4: "Therefore we ourselves boast about you among the churches of God — for your steadfastness and faith in all your persecutions and the afflictions you are enduring.",
    5: "This is plain evidence of God's righteous judgment — that you may be counted worthy of the kingdom of God, for which you are also suffering.",
    6: "For after all, it is just with God to repay with affliction those who afflict you,",
    7: "and to give relief to you who are afflicted, and to us as well — when the Lord Jesus is revealed from heaven with His mighty angels,",
    8: "in flaming fire, taking vengeance on those who do not know God and who do not obey the gospel of our Lord Jesus.",
    9: "These will pay the penalty of eternal destruction, away from the presence of the Lord and from the glory of His might —",
    10: "when He comes on that Day to be glorified in His saints and to be marveled at by all who have believed (because our testimony among you was believed).",
    11: "To this end we always pray for you — that our God may count you worthy of His calling, and may fulfill every good resolve and every work of faith with power,",
    12: "so that the name of our Lord Jesus may be glorified in you, and you in Him, according to the grace of our God and the Lord Jesus Christ.",
}
ch2 = {
    1: "Now we ask you, brothers, concerning the coming of our Lord Jesus Christ and our being gathered together to Him —",
    2: "that you not be quickly shaken in mind, or alarmed — either by a spirit, or by a word, or by a letter seeming to be from us — to the effect that the day of the Lord has already come.",
    3: "Let no one deceive you in any way. For that day will not come unless the falling away comes first, and the man of lawlessness is revealed — the son of destruction —",
    4: "the one who opposes and exalts himself against every so-called god or object of worship, so that he takes his seat in the temple of God, proclaiming himself to be God.",
    5: "Do you not remember that, while I was still with you, I was telling you these things?",
    6: "And now you know what is restraining him — so that he may be revealed in his own time.",
    7: "For the mystery of lawlessness is already at work; only the One who now restrains will do so until He is taken out of the way.",
    8: "And then the lawless one will be revealed — whom the Lord Jesus will slay with the breath of His mouth, and bring to nothing by the appearance of His coming.",
    9: "The coming of the lawless one will be in accord with the working of Satan — with all power, and with signs and lying wonders,",
    10: "and with all unrighteous deception for those who are perishing — because they refused to love the truth and so be saved.",
    11: "For this reason, God sends them a working of error — so that they will believe the lie,",
    12: "in order that all may be condemned who have not believed the truth, but have taken pleasure in unrighteousness.",
    13: "But we are bound always to thank God for you, brothers beloved by the Lord — because God chose you from the beginning for salvation, through sanctification by the Spirit and faith in the truth,",
    14: "to which He called you by our gospel — for the obtaining of the glory of our Lord Jesus Christ.",
    15: "So then, brothers, stand firm — and hold to the traditions you were taught, whether by spoken word or by letter from us.",
    16: "Now may our Lord Jesus Christ Himself, and God our Father — who has loved us and given us eternal comfort and good hope through grace —",
    17: "comfort your hearts and establish you in every good word and work.",
}
ch3 = {
    1: "Finally, brothers, pray for us — that the word of the Lord may run swiftly and be glorified, just as it is with you,",
    2: "and that we may be delivered from unreasonable and wicked men — for not all have the faith.",
    3: "But the Lord is faithful. He will establish you and guard you from the evil one.",
    4: "And we have confidence in the Lord concerning you — that you are doing, and will do, the things we command.",
    5: "May the Lord direct your hearts into the love of God, and into the steadfastness of Christ.",
    6: "Now we command you, brothers — in the name of our Lord Jesus Christ — that you withdraw from every brother who walks in disorder, and not according to the tradition that you received from us.",
    7: "For you yourselves know how you ought to imitate us — because we did not behave disorderly among you,",
    8: "nor did we eat anyone's bread without paying for it. Rather, with toil and labor we worked night and day, so as not to be a burden to any of you —",
    9: "not because we have no right, but in order to give ourselves to you as a model to imitate.",
    10: "For even when we were with you, we used to give you this command: \"If anyone is not willing to work, neither shall he eat.\"",
    11: "For we hear that some among you are walking in disorder — not working at all, but being busybodies.",
    12: "Now such persons we command and exhort, in the Lord Jesus Christ, to work quietly and to eat their own bread.",
    13: "But as for you, brothers — do not grow weary in doing what is right.",
    14: "If anyone does not obey our word in this letter, take note of him and have nothing to do with him — so that he may be ashamed.",
    15: "Yet do not regard him as an enemy, but admonish him as a brother.",
    16: "Now may the Lord of peace Himself give you peace at all times, in every way. The Lord be with you all.",
    17: "I, Paul, write this greeting with my own hand. This is the sign in every letter — this is how I write.",
    18: "The grace of our Lord Jesus Christ be with you all. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3}

def main():
    new_entries = {f"53_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"2 Thessalonians total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 2 Thess verses")

if __name__ == "__main__":
    main()
