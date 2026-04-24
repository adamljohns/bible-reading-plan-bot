"""
MBT John 16 — The Work of the Holy Spirit; Sorrow Will Turn to Joy;
I Have Overcome the World. 33 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch16 = {
    1: '"These things I have spoken to you so that you will not fall away.',
    2: "They will put you out of the synagogues. In fact, an hour is coming when everyone who kills you will think he is offering a service to God.",
    3: "And they will do these things because they have not known the Father or Me.",
    4: "But I have spoken these things to you so that, when their hour comes, you may remember that I told you about them. I did not say these things to you from the beginning, because I was with you.",
    5: "But now I am going to the One who sent Me — and none of you asks Me, 'Where are You going?'",
    6: "But because I have told you these things, sorrow has filled your heart.",
    7: "Still, I tell you the truth — it is to your advantage that I go away. For if I do not go away, the Helper will not come to you. But if I go, I will send Him to you.",
    8: "And when He comes, He will convict the world concerning sin, and righteousness, and judgment:",
    9: "concerning sin — because they do not believe in Me;",
    10: "concerning righteousness — because I am going to the Father, and you will see Me no more;",
    11: "concerning judgment — because the ruler of this world has been judged.",
    12: "I still have many things to say to you, but you cannot bear them now.",
    13: "But when He — the Spirit of truth — comes, He will guide you into all truth. For He will not speak on His own initiative — He will speak whatever He hears. And He will declare to you the things that are to come.",
    14: "He will glorify Me, because He will take what is Mine and declare it to you.",
    15: "Everything the Father has is Mine. That is why I said He will take what is Mine and declare it to you.",
    16: 'A little while, and you will no longer see Me — and again a little while, and you will see Me."',
    17: 'So some of His disciples said to one another, "What does He mean by this — \'A little while, and you will not see Me, and again a little while, and you will see Me,\' and, \'because I am going to the Father\'?"',
    18: 'They kept saying, "What is this \'little while\' He speaks of? We do not know what He is talking about."',
    19: 'Jesus knew they wanted to ask Him — so He said to them, "Are you discussing with one another what I meant by \'A little while and you will not see Me, and again a little while and you will see Me\'?',
    20: "Truly, truly, I tell you — you will weep and mourn, while the world rejoices. You will be sorrowful, but your sorrow will turn into joy.",
    21: "A woman in labor has sorrow, because her hour has come. But as soon as she has given birth to the child, she no longer remembers the anguish — for joy that a human being has been born into the world.",
    22: "So also you have sorrow now. But I will see you again, and your heart will rejoice — and no one will take your joy from you.",
    23: "In that day you will ask Me nothing. Truly, truly, I tell you — whatever you ask the Father in My name, He will give you.",
    24: "Until now you have asked for nothing in My name. Ask, and you will receive — so that your joy may be made full.",
    25: "I have spoken these things to you in figures of speech. An hour is coming when I will no longer speak to you in figures, but will tell you plainly about the Father.",
    26: "In that day you will ask in My name. I am not saying to you that I will ask the Father on your behalf —",
    27: "for the Father Himself loves you, because you have loved Me, and have believed that I came from God.",
    28: "I came from the Father and have come into the world. Again, I am leaving the world and going to the Father.",
    29: 'His disciples said, "Look — now You are speaking plainly, not in a figure of speech!',
    30: 'Now we know that You know all things, and do not need anyone to question You. By this we believe that You came from God."',
    31: 'Jesus answered them, "Do you now believe?',
    32: "Look — an hour is coming, and has already come, when you will be scattered, each to his own, and will leave Me alone. Yet I am not alone — for the Father is with Me.",
    33: 'I have spoken these things to you so that in Me you may have peace. In the world you will have trouble. But take heart — I have overcome the world."',
}

CHAPTERS = {16: ch16}

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
