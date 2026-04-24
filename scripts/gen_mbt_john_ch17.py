"""
MBT John 17 — The High Priestly Prayer. Jesus prays for Himself, for
His disciples, and for all who will believe through their word. 26 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch17 = {
    1: 'When Jesus had said these things, He lifted up His eyes to heaven and said: "Father, the hour has come. Glorify Your Son, so that the Son may glorify You —',
    2: "just as You gave Him authority over all flesh, so that He may give eternal life to all whom You have given Him.",
    3: "And this is eternal life — that they may know You, the only true God, and Jesus Christ, whom You have sent.",
    4: "I have glorified You on the earth, having finished the work You gave Me to do.",
    5: "And now, Father, glorify Me at Your own side — with the glory I had with You before the world existed.",
    6: "I have revealed Your name to the ones You gave Me out of the world. They were Yours, and You gave them to Me — and they have kept Your word.",
    7: "Now they know that everything You have given Me is from You.",
    8: "For the words You gave Me I have given to them. They received them, and truly understood that I came from You — and they believed that You sent Me.",
    9: "I am praying for them. I am not praying for the world, but for those You have given Me — because they are Yours.",
    10: "Everything that is Mine is Yours, and Yours is Mine — and I have been glorified in them.",
    11: "I am no longer in the world, but they are in the world, and I am coming to You. Holy Father, keep them in Your name — the name You gave Me — so that they may be one, as We are one.",
    12: "While I was with them, I kept them in Your name — the name You gave Me. I guarded them, and not one of them has been lost, except the son of destruction — so that the Scripture might be fulfilled.",
    13: "But now I am coming to You — and I speak these things while still in the world, so that they may have My joy made full in themselves.",
    14: "I have given them Your word, and the world has hated them, because they are not of the world — just as I am not of the world.",
    15: "I do not ask You to take them out of the world, but that You would keep them from the evil one.",
    16: "They are not of the world, just as I am not of the world.",
    17: "Sanctify them in the truth. Your word is truth.",
    18: "Just as You sent Me into the world, I have also sent them into the world.",
    19: "And for their sake I sanctify Myself — so that they also may be sanctified in truth.",
    20: "I do not pray for these only, but also for those who will believe in Me through their word —",
    21: "that they all may be one, just as You, Father, are in Me, and I in You. May they also be in Us — so that the world may believe that You sent Me.",
    22: "And the glory You have given Me, I have given to them — so that they may be one, just as We are one:",
    23: "I in them, and You in Me — so that they may be perfected into one, and that the world may know that You sent Me, and have loved them just as You have loved Me.",
    24: "Father, I want those You have given Me to be with Me where I am — so that they may see My glory, the glory You have given Me, because You loved Me before the foundation of the world.",
    25: "Righteous Father, the world has not known You, but I have known You. And these have come to know that You sent Me.",
    26: 'I made Your name known to them, and will continue to make it known — so that the love with which You loved Me may be in them, and I in them."',
}

CHAPTERS = {17: ch17}

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
