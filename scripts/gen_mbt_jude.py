"""
MBT Jude — single chapter, 25 verses. Book ID 65. Jude (brother of James,
half-brother of Jesus) writes a fierce defense of the faith against
infiltrating false teachers. Reverential caps applied.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Jude, a servant of Jesus Christ and brother of James — to those who are called, beloved in God the Father, and kept for Jesus Christ:",
    2: "May mercy, peace, and love be multiplied to you.",
    3: "Beloved, while I was making every effort to write to you about our common salvation, I found it necessary to write urging you to contend earnestly for the faith — once for all delivered to the saints.",
    4: "For certain men have crept in unnoticed — those who long ago were marked out for this condemnation. They are ungodly, perverting the grace of our God into licentiousness, and denying the only Master and our Lord, Jesus Christ.",
    5: "Now I want to remind you — though you already know all this — that the Lord, having once saved a people out of the land of Egypt, afterward destroyed those who did not believe.",
    6: "And the angels who did not keep their proper position, but abandoned their own dwelling — He has kept in eternal chains under darkness for the judgment of the great Day.",
    7: "Just so, Sodom and Gomorrah and the surrounding cities — which in like manner gave themselves over to sexual immorality and went after strange flesh — are set forth as an example, undergoing the punishment of eternal fire.",
    8: "Yet in the same way these dreamers also defile the flesh, reject authority, and revile glorious beings.",
    9: "But Michael the archangel, when contending with the devil and disputing about the body of Moses, did not dare bring against him a railing accusation — but said, \"The Lord rebuke you!\"",
    10: "But these revile whatever they do not understand, and what they do understand by instinct — like irrational animals — these are the things by which they are destroyed.",
    11: "Woe to them! For they have gone the way of Cain. They have rushed for profit into Balaam's error. They have perished in Korah's rebellion.",
    12: "These are the hidden reefs at your love feasts — feasting with you fearlessly, shepherding only themselves: clouds without water, carried along by winds; autumn trees, fruitless, twice dead, uprooted;",
    13: "wild waves of the sea, foaming up their own shame; wandering stars, for whom the gloom of darkness has been reserved forever.",
    14: "It was also about these men that Enoch — the seventh from Adam — prophesied, saying: \"Behold, the Lord came with myriads of His holy ones,",
    15: "to execute judgment upon all, and to convict every soul of all the ungodly works they have committed in their ungodliness, and of all the harsh things ungodly sinners have spoken against Him.\"",
    16: "These are grumblers, complainers, walking according to their own lusts. Their mouths speak arrogant words, flattering people for the sake of advantage.",
    17: "But you, beloved, remember the words spoken beforehand by the apostles of our Lord Jesus Christ —",
    18: "how they kept telling you, \"In the last time there will be mockers, walking according to their own ungodly lusts.\"",
    19: "These are the ones who divide, who are unspiritual, devoid of the Spirit.",
    20: "But you, beloved, building yourselves up in your most holy faith, praying in the Holy Spirit,",
    21: "keep yourselves in the love of God — waiting for the mercy of our Lord Jesus Christ that brings eternal life.",
    22: "And on some have mercy — those who waver;",
    23: "save others, snatching them out of the fire; and on some have mercy with fear — hating even the garment stained by the flesh.",
    24: "Now to Him who is able to keep you from stumbling, and to present you faultless before the presence of His glory with great joy —",
    25: "to the only God our Savior, through Jesus Christ our Lord, be glory and majesty, dominion and authority, before all time, now, and forevermore. Amen.",
}

CHAPTERS = {1: ch1}

def main():
    new_entries = {f"65_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Jude total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Jude verses")

if __name__ == "__main__":
    main()
