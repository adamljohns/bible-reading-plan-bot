"""
MBT John 13 — Jesus Washes the Disciples' Feet, Predicts His Betrayal,
New Commandment, Peter's Denial Foretold. 38 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch13 = {
    1: "Now before the Feast of the Passover, Jesus — knowing that His hour had come to depart out of this world to the Father, having loved His own who were in the world — loved them to the very end.",
    2: "During supper, the devil had already put it into the heart of Judas Iscariot, Simon's son, to betray Him.",
    3: "Jesus — knowing that the Father had given all things into His hands, and that He had come from God, and was going back to God —",
    4: "got up from supper, laid aside His outer garments, took a towel, and tied it around His waist.",
    5: "Then He poured water into the basin and began to wash the disciples' feet, and to dry them with the towel that was tied around Him.",
    6: 'He came to Simon Peter, who said to Him, "Lord — You are going to wash my feet?"',
    7: 'Jesus answered him, "What I am doing, you do not understand now — but afterward you will understand."',
    8: 'Peter said to Him, "You will never wash my feet — ever!" Jesus answered him, "If I do not wash you, you have no share with Me."',
    9: 'Simon Peter said to Him, "Lord — not my feet only, but also my hands and my head!"',
    10: 'Jesus said to him, "The one who has bathed does not need to wash, except for his feet. He is completely clean. And you are clean — though not every one of you."',
    11: 'For He knew the one who would betray Him. That is why He said, "You are not all clean."',
    12: 'So when He had washed their feet, and taken His garments and reclined again, He said to them, "Do you understand what I have done for you?',
    13: "You call Me 'Teacher' and 'Lord' — and rightly so, for that is what I am.",
    14: "So if I — your Lord and Teacher — have washed your feet, you also ought to wash one another's feet.",
    15: "For I have given you an example — so that you also should do just as I have done for you.",
    16: "Truly, truly, I tell you — a servant is not greater than his master, nor is a messenger greater than the one who sent him.",
    17: "If you know these things, blessed are you if you do them.",
    18: "I am not speaking about all of you. I know the ones I have chosen. But this is so that the Scripture may be fulfilled: 'The one who ate My bread has lifted up his heel against Me.'",
    19: "From now on I am telling you before it happens, so that when it does happen, you may believe that I am He.",
    20: 'Truly, truly, I tell you — whoever receives anyone I send receives Me, and whoever receives Me receives the One who sent Me."',
    21: 'Having said these things, Jesus was troubled in spirit and testified: "Truly, truly, I tell you — one of you will betray Me."',
    22: "The disciples began looking at one another, at a loss as to whom He was speaking about.",
    23: "One of His disciples, the one Jesus loved, was reclining at the table close beside Him.",
    24: "So Simon Peter motioned to him to ask who it was He was speaking about.",
    25: 'Leaning back on Jesus\' chest, he said to Him, "Lord, who is it?"',
    26: 'Jesus answered, "It is the one to whom I will give this morsel of bread when I have dipped it." So when He had dipped the bread, He took and gave it to Judas Iscariot, son of Simon.',
    27: 'And after the morsel, then Satan entered him. Jesus said to him, "What you are about to do, do quickly."',
    28: "None of those reclining at table knew why He said this to him.",
    29: "Some thought, because Judas had the money box, that Jesus was telling him, 'Buy what we need for the feast,' or that he should give something to the poor.",
    30: "So after receiving the morsel, Judas went out at once. And it was night.",
    31: 'So when he had gone out, Jesus said, "Now the Son of Man is glorified, and God is glorified in Him.',
    32: "If God is glorified in Him, God will also glorify Him in Himself — and He will glorify Him at once.",
    33: "Little children, I am with you only a little while longer. You will look for Me — and just as I said to the Jewish leaders, 'Where I am going, you cannot come' — so now I say to you.",
    34: "A new commandment I give to you: love one another. Just as I have loved you, you also are to love one another.",
    35: 'By this everyone will know that you are My disciples — if you have love for one another."',
    36: 'Simon Peter said to Him, "Lord, where are You going?" Jesus answered, "Where I am going, you cannot follow Me now — but you will follow afterward."',
    37: 'Peter said to Him, "Lord, why can I not follow You now? I will lay down my life for You!"',
    38: 'Jesus answered, "You will lay down your life for Me? Truly, truly, I tell you — the rooster will not crow until you have denied Me three times."',
}

CHAPTERS = {13: ch13}

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
