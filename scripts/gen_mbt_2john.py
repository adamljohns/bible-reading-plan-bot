"""
MBT 2 John — single chapter, 13 verses. Book ID 63. The shortest letter
in the New Testament after 3 John. Theme: walk in truth and love;
reject deceivers who deny Christ in the flesh.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-1-3-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The elder, to the chosen lady and her children — whom I love in truth, and not I only, but also all who have come to know the truth —",
    2: "for the sake of the truth that remains in us, and will be with us forever:",
    3: "Grace, mercy, and peace will be with us, from God the Father and from Jesus Christ the Son of the Father, in truth and in love.",
    4: "I rejoiced greatly to find some of your children walking in truth, just as we received commandment from the Father.",
    5: "And now, lady, I am asking you — not as though I were writing a new commandment to you, but the one we have had from the beginning — that we love one another.",
    6: "And this is love: that we walk according to His commandments. This is the commandment, just as you have heard from the beginning, that you should walk in it.",
    7: "For many deceivers have gone out into the world — those who do not confess Jesus Christ as coming in the flesh. This is the deceiver and the Antichrist.",
    8: "Watch yourselves, so that you do not lose what we have worked for, but receive a full reward.",
    9: "Anyone who runs ahead and does not remain in the teaching of Christ does not have God. The one who remains in the teaching has both the Father and the Son.",
    10: "If anyone comes to you and does not bring this teaching, do not receive him into your house, nor give him a greeting.",
    11: "For the one who gives him a greeting shares in his evil works.",
    12: "Having many things to write to you, I did not want to do it with paper and ink. But I hope to come to you and speak face to face — so that our joy may be made full.",
    13: "The children of your chosen sister greet you.",
}

CHAPTERS = {1: ch1}

def main():
    new_entries = {f"63_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"2 John total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-1-3-john.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 2 John verses")

if __name__ == "__main__":
    main()
