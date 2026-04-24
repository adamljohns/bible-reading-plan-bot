"""
MBT John 15 — The Vine and the Branches; The World's Hatred. 27 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch15 = {
    1: '"I am the true vine, and My Father is the vinedresser.',
    2: "Every branch in Me that does not bear fruit, He takes away; and every branch that does bear fruit, He prunes — so that it may bear more fruit.",
    3: "You are already clean because of the word I have spoken to you.",
    4: "Remain in Me, and I in you. Just as the branch cannot bear fruit by itself, unless it remains in the vine — neither can you, unless you remain in Me.",
    5: "I am the vine; you are the branches. The one who remains in Me, and I in him — he bears much fruit. For apart from Me, you can do nothing.",
    6: "If anyone does not remain in Me, he is cast out like a branch and withers. They gather them, throw them into the fire — and they are burned.",
    7: "If you remain in Me, and My words remain in you, ask whatever you wish — and it will be done for you.",
    8: "By this My Father is glorified — that you bear much fruit, and show yourselves to be My disciples.",
    9: "As the Father has loved Me, so have I loved you. Remain in My love.",
    10: "If you keep My commandments, you will remain in My love — just as I have kept My Father's commandments, and remain in His love.",
    11: "These things I have spoken to you, so that My joy may be in you, and that your joy may be made full.",
    12: "This is My commandment: that you love one another, just as I have loved you.",
    13: "No one has greater love than this — that one lays down his life for his friends.",
    14: "You are My friends, if you do what I command you.",
    15: "No longer do I call you servants — for the servant does not know what his master is doing. But I have called you friends, because everything I have heard from My Father I have made known to you.",
    16: "You did not choose Me — I chose you. And I appointed you to go and bear fruit, fruit that would last — so that whatever you ask the Father in My name, He may give you.",
    17: "These things I command you — that you love one another.",
    18: "If the world hates you, know this: it hated Me before it hated you.",
    19: "If you were of the world, the world would love its own. But because you are not of the world, and I chose you out of the world — for this reason the world hates you.",
    20: "Remember the word I spoke to you: 'A servant is not greater than his master.' If they persecuted Me, they will also persecute you. If they kept My word, they will also keep yours.",
    21: "But all these things they will do to you on account of My name — because they do not know the One who sent Me.",
    22: "If I had not come and spoken to them, they would not be guilty of sin. But now they have no excuse for their sin.",
    23: "The one who hates Me also hates My Father.",
    24: "If I had not done among them the works no one else has done, they would not be guilty of sin. But now they have both seen and hated both Me and My Father.",
    25: "Yet this happened to fulfill the word written in their Law: 'They hated Me without a cause.'",
    26: "When the Helper comes, whom I will send to you from the Father — the Spirit of truth, who proceeds from the Father — He will bear witness about Me.",
    27: 'And you too will bear witness, because you have been with Me from the beginning."',
}

CHAPTERS = {15: ch15}

def main():
    new_entries = {f"43_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Chapter {list(CHAPTERS.keys())[0]}: {len(new_entries)} verses")
    with open(MBT_JOHN_PATH) as f: mbt_john = json.load(f)
    mbt_john.update(new_entries)
    with open(MBT_JOHN_PATH, "w") as f: json.dump(mbt_john, f, indent=2, ensure_ascii=False)
    print(f"mbt-john.json: {len(mbt_john)} total verses")
    with open(MOOP_PATH) as f: moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f: json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT John verses")

if __name__ == "__main__":
    main()
