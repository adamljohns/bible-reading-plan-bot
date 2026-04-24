"""
MBT John 14 — I Am the Way, the Truth, the Life; the first promise of
the Holy Spirit. 31 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch14 = {
    1: '"Do not let your heart be troubled. You believe in God — believe also in Me.',
    2: "In My Father's house are many rooms. If it were not so, would I have told you that I am going there to prepare a place for you?",
    3: "And if I go and prepare a place for you, I will come again and take you to Myself — so that where I am, you may be also.",
    4: 'And where I am going, you know the way."',
    5: 'Thomas said to Him, "Lord, we do not know where You are going. How can we know the way?"',
    6: 'Jesus said to him, "I am the Way, and the Truth, and the Life. No one comes to the Father except through Me.',
    7: 'If you had known Me, you would have known My Father also. From now on, you do know Him — and you have seen Him."',
    8: 'Philip said to Him, "Lord, show us the Father — and that will be enough for us."',
    9: 'Jesus said to him, "Have I been with you so long, Philip, and you still do not know Me? The one who has seen Me has seen the Father. How then can you say, \'Show us the Father\'?',
    10: "Do you not believe that I am in the Father, and the Father is in Me? The words I say to you, I do not speak on My own authority — but the Father, living in Me, is doing His works.",
    11: "Believe Me — I am in the Father and the Father is in Me. Or else, believe on account of the works themselves.",
    12: "Truly, truly, I tell you — the one who believes in Me, the works that I do, he will do also. And greater works than these he will do, because I am going to the Father.",
    13: "And whatever you ask in My name, this I will do — so that the Father may be glorified in the Son.",
    14: "If you ask Me anything in My name, I will do it.",
    15: "If you love Me, you will keep My commandments.",
    16: "And I will ask the Father, and He will give you another Helper — the Paraclete — to be with you forever,",
    17: "the Spirit of truth, whom the world cannot receive, because it does not see Him or know Him. You know Him, for He lives with you — and will be in you.",
    18: "I will not leave you as orphans. I will come to you.",
    19: "A little while longer, and the world will see Me no more. But you will see Me — because I live, you also will live.",
    20: "On that day you will know that I am in My Father, and you in Me, and I in you.",
    21: "The one who has My commandments and keeps them — he is the one who loves Me. And the one who loves Me will be loved by My Father. And I will love him, and will reveal Myself to him.",
    22: 'Judas (not Iscariot) said to Him, "Lord, how is it that You are about to reveal Yourself to us, and not to the world?"',
    23: 'Jesus answered him, "If anyone loves Me, he will keep My word — and My Father will love him, and We will come to him and make Our home with him.',
    24: "The one who does not love Me does not keep My words. And the word you are hearing is not Mine, but the Father's — who sent Me.",
    25: "I have spoken these things to you while remaining with you.",
    26: "But the Helper — the Holy Spirit, whom the Father will send in My name — He will teach you all things, and bring to your remembrance everything I have said to you.",
    27: "Peace I leave with you; My peace I give to you. I do not give to you as the world gives. Do not let your heart be troubled — and do not be afraid.",
    28: "You heard Me say to you, 'I am going away, and I will come to you.' If you loved Me, you would rejoice that I am going to the Father — for the Father is greater than I.",
    29: "And now I have told you before it happens — so that when it does happen, you may believe.",
    30: "I will no longer talk much with you — for the ruler of this world is coming. He has no hold on Me,",
    31: 'but he comes so that the world may know that I love the Father, and that I do exactly as the Father has commanded Me. Rise — let us go from here.',
}

CHAPTERS = {14: ch14}

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
