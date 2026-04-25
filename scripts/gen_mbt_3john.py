"""
MBT 3 John — single chapter, 15 verses. Book ID 64. The shortest book
in the New Testament. The elder writes Gaius commending his hospitality,
warning against Diotrephes, and commending Demetrius.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-1-3-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "The elder, to the beloved Gaius, whom I love in truth.",
    2: "Beloved, I pray that in everything you may prosper and be in good health, just as your soul prospers.",
    3: "For I rejoiced greatly when brothers came and testified to your truth — that you walk in the truth.",
    4: "I have no greater joy than this: to hear that my children walk in the truth.",
    5: "Beloved, you are acting faithfully in whatever you do for the brothers, and especially when they are strangers.",
    6: "They have testified to your love before the church. You will do well to send them on their way in a manner worthy of God.",
    7: "For they went out for the sake of the Name, accepting nothing from the Gentiles.",
    8: "We therefore ought to support such men, so that we may be fellow workers in the truth.",
    9: "I have written something to the church, but Diotrephes — who loves to be first among them — does not accept us.",
    10: "So if I come, I will call attention to the works he is doing — talking nonsense against us with malicious words. And not content with this, he himself does not receive the brothers, and even hinders those who want to do so, and casts them out of the church.",
    11: "Beloved, do not imitate what is evil — but what is good. The one who does good is of God; the one who does evil has not seen God.",
    12: "Demetrius has received a good testimony from everyone — and from the truth itself. We also bear witness, and you know that our testimony is true.",
    13: "I had many things to write to you, but I do not want to write them with pen and ink.",
    14: "I hope to see you soon, and we will speak face to face.",
    15: "Peace to you. The friends greet you. Greet the friends by name.",
}

CHAPTERS = {1: ch1}

def main():
    new_entries = {f"64_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"3 John total verses authored: {len(new_entries)}")
    with open(MBT_PATH) as f: existing = json.load(f)
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-1-3-john.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT 3 John verses")

if __name__ == "__main__":
    main()
