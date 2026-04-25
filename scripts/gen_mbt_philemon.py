"""
MBT Philemon — single chapter, 25 verses. Book ID 57. Paul's pastoral
letter to a slaveowner about a runaway (now-converted) slave Onesimus.
Reverential caps applied.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_PATH = ROOT / "docs" / "assets" / "mbt-nt-extra.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch1 = {
    1: "Paul, a prisoner of Christ Jesus, and Timothy our brother, to Philemon — our beloved friend and fellow worker —",
    2: "and to Apphia our sister, and to Archippus our fellow soldier, and to the church that meets in your house:",
    3: "Grace to you, and peace, from God our Father and the Lord Jesus Christ.",
    4: "I thank my God always when I remember you in my prayers,",
    5: "because I keep hearing of your love and of the faith you have toward the Lord Jesus and toward all the saints.",
    6: "And I pray that the fellowship of your faith may become effective — through the full knowledge of every good thing that is in us for Christ's sake.",
    7: "For I have had much joy and encouragement from your love, brother — because the hearts of the saints have been refreshed through you.",
    8: "Therefore, although I have plenty of boldness in Christ to order you to do what is fitting,",
    9: "yet for love's sake I prefer to appeal to you. I — Paul, an old man, and now also a prisoner of Christ Jesus —",
    10: "I appeal to you for my child, whom I have begotten in my chains: Onesimus.",
    11: "Once he was useless to you — but now he has become truly useful, both to you and to me.",
    12: "I am sending him back to you — that is, my own heart.",
    13: "I would have liked to keep him with me, so that on your behalf he might serve me in my chains for the gospel.",
    14: "But without your consent I did not want to do anything, so that your good deed would not be by compulsion, but of your own free will.",
    15: "For perhaps this is why he was separated from you for a little while — so that you might have him back forever:",
    16: "no longer as a slave, but more than a slave — a beloved brother, especially to me, but how much more to you, both in the flesh and in the Lord.",
    17: "So if you consider me a partner, welcome him as you would welcome me.",
    18: "And if he has wronged you in any way, or owes you anything, charge that to my account.",
    19: "I, Paul, am writing this with my own hand: I will repay it — without mentioning that you owe me even your own self.",
    20: "Yes, brother — let me have some benefit from you in the Lord. Refresh my heart in Christ.",
    21: "Confident of your obedience, I write to you — knowing that you will do even more than I say.",
    22: "And one thing more — prepare a guest room for me, for I am hoping that through your prayers I will be given back to you.",
    23: "Epaphras — my fellow prisoner in Christ Jesus — sends you greetings,",
    24: "as do Mark, Aristarchus, Demas, and Luke — my fellow workers.",
    25: "The grace of the Lord Jesus Christ be with your spirit. Amen.",
}

CHAPTERS = {1: ch1}

def main():
    new_entries = {f"57_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Philemon total verses authored: {len(new_entries)}")
    if MBT_PATH.exists():
        with open(MBT_PATH) as f: existing = json.load(f)
    else:
        existing = {}
    existing.update(new_entries)
    with open(MBT_PATH, "w") as f: json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"mbt-nt-extra.json: {len(existing)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT Philemon verses")

if __name__ == "__main__":
    main()
