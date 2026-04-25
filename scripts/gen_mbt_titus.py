"""MBT Titus — 3 chapters, 46 verses. Book ID 56."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, a bondservant of God and an apostle of Jesus Christ — for the faith of God's chosen ones, and for the full knowledge of the truth that leads to godliness,",
    2: "in the hope of eternal life — which God, who cannot lie, promised before the ages of time began,",
    3: "and at the proper time has manifested His word through the proclamation entrusted to me by the command of God our Savior:",
    4: "to Titus, my true son in our common faith — grace and peace from God the Father, and the Lord Jesus Christ our Savior.",
    5: "For this reason I left you in Crete: that you might set in order what was lacking, and appoint elders in every city, just as I commanded you —",
    6: "if anyone is above reproach, the husband of one wife, having children who believe and who are not accused of dissipation or rebellion.",
    7: "For an overseer must be above reproach as God's steward — not arrogant, not quick-tempered, not given to wine, not violent, not greedy for gain;",
    8: "but hospitable, a lover of what is good, sober-minded, righteous, holy, and self-controlled —",
    9: "holding fast to the faithful word as he was taught, so that he may be able both to encourage by sound doctrine and to refute those who contradict.",
    10: "For there are many rebellious men, empty talkers and deceivers — especially those of the circumcision —",
    11: "whose mouths must be silenced. They are upsetting whole households by teaching, for the sake of dishonest gain, things they ought not to teach.",
    12: "One of them — a prophet of their own — said, \"Cretans are always liars, evil beasts, lazy gluttons.\"",
    13: "This testimony is true. For this reason, rebuke them sharply — so that they may be sound in the faith,",
    14: "not paying attention to Jewish myths or to the commands of men who turn away from the truth.",
    15: "To the pure, all things are pure — but to those who are defiled and unbelieving, nothing is pure. Both their mind and their conscience are defiled.",
    16: "They claim to know God, but by their deeds they deny Him — being detestable, disobedient, and unfit for any good work.",
}
ch2 = {
    1: "But as for you, speak the things that are fitting for sound doctrine.",
    2: "Older men are to be sober-minded, dignified, self-controlled — sound in faith, in love, and in steadfastness.",
    3: "Older women likewise — that they be reverent in behavior, not slanderers, not enslaved to much wine, teachers of what is good —",
    4: "so that they may train the younger women to love their husbands, to love their children,",
    5: "to be self-controlled, pure, working at home, kind, submissive to their own husbands — so that the word of God will not be discredited.",
    6: "Likewise, urge the younger men to be self-controlled.",
    7: "In all things show yourself to be an example of good works — in your teaching showing integrity, dignity,",
    8: "and sound speech that cannot be condemned — so that the opponent may be put to shame, having nothing evil to say about us.",
    9: "Bondservants are to be subject to their own masters in everything, and to be well-pleasing — not arguing back,",
    10: "not pilfering, but showing all good faith — so that in everything they may adorn the doctrine of God our Savior.",
    11: "For the grace of God has appeared, bringing salvation to all people,",
    12: "training us to renounce ungodliness and worldly desires, and to live sensibly, righteously, and godly in this present age,",
    13: "looking for the blessed hope and glorious appearing of our great God and Savior, Jesus Christ —",
    14: "who gave Himself for us, to redeem us from all lawlessness and to purify for Himself a people for His own possession, zealous for good works.",
    15: "These things speak — and exhort and rebuke with all authority. Let no one disregard you.",
}
ch3 = {
    1: "Remind them to be subject to rulers and authorities, to be obedient, to be ready for every good work,",
    2: "to malign no one, to be peaceable and gentle, showing all humility to all people.",
    3: "For we ourselves were once foolish, disobedient, deceived — slaves to various lusts and pleasures, living in malice and envy, hateful, and hating one another.",
    4: "But when the kindness and the love of God our Savior toward man appeared,",
    5: "He saved us — not by works of righteousness which we have done, but according to His mercy — through the washing of regeneration and the renewing of the Holy Spirit,",
    6: "which He poured out on us abundantly through Jesus Christ our Savior,",
    7: "so that, having been justified by His grace, we should become heirs according to the hope of eternal life.",
    8: "This saying is faithful — and concerning these things I want you to insist confidently, so that those who have believed in God may be careful to engage in good works. These things are good and profitable for people.",
    9: "But avoid foolish controversies, genealogies, strife, and quarrels about the law — for they are useless and worthless.",
    10: "Reject a divisive man after the first and second admonition,",
    11: "knowing that such a one is warped and sinful — being self-condemned.",
    12: "When I send Artemas to you, or Tychicus, make every effort to come to me at Nicopolis — for I have decided to spend the winter there.",
    13: "Diligently send Zenas the lawyer and Apollos on their way, so that nothing is lacking for them.",
    14: "And let our people learn to engage in good works for cases of urgent need — so that they will not be unfruitful.",
    15: "All who are with me greet you. Greet those who love us in the faith. Grace be with you all. Amen.",
}
CHAPTERS = {1: ch1, 2: ch2, 3: ch3}

def main():
    new_entries = {f"56_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Titus total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Titus verses")

if __name__ == "__main__":
    main()
