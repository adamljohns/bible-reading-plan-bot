"""
MBT John 10 — The Good Shepherd, At the Feast of Dedication. 42 verses.
'I am the door' / 'I am the good shepherd' / 'I and the Father are one.'
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch10 = {
    1: '"Truly, truly, I tell you — the one who does not enter the sheepfold by the door, but climbs in another way, he is a thief and a robber.',
    2: "But the one who enters by the door is the shepherd of the sheep.",
    3: "To him the doorkeeper opens, and the sheep hear his voice. He calls his own sheep by name and leads them out.",
    4: "When he has brought out all his own, he goes on ahead of them, and the sheep follow him — because they know his voice.",
    5: 'They will not follow a stranger; they will flee from him — because they do not know the voice of strangers."',
    6: "Jesus spoke this figure of speech to them, but they did not understand what He was saying to them.",
    7: 'So Jesus said to them again, "Truly, truly, I tell you — I am the door of the sheep.',
    8: "All who came before Me are thieves and robbers — but the sheep did not listen to them.",
    9: "I am the door. Whoever enters through Me will be saved, and will go in and out and find pasture.",
    10: "The thief comes only to steal, and kill, and destroy. I came that they might have life — and have it abundantly.",
    11: "I am the good shepherd. The good shepherd lays down his life for the sheep.",
    12: "The hired hand, who is not the shepherd — the sheep are not his own — when he sees the wolf coming, leaves the sheep and runs away. And the wolf snatches them and scatters them.",
    13: "He runs because he is a hired hand, and does not care about the sheep.",
    14: "I am the good shepherd. I know My own, and My own know Me —",
    15: "just as the Father knows Me and I know the Father — and I lay down My life for the sheep.",
    16: "And I have other sheep that are not of this fold. I must bring them also, and they will hear My voice. And there will be one flock, one shepherd.",
    17: "For this reason the Father loves Me — because I lay down My life so that I may take it up again.",
    18: 'No one takes it from Me; I lay it down of My own accord. I have authority to lay it down, and I have authority to take it up again. This command I received from My Father."',
    19: "Again there was a division among the Jewish leaders because of these words.",
    20: 'Many of them were saying, "He has a demon. He is out of His mind. Why listen to Him?"',
    21: 'Others were saying, "These are not the words of one who is demon-possessed. Can a demon open the eyes of the blind?"',
    22: "Then came the Feast of Dedication in Jerusalem. It was winter,",
    23: "and Jesus was walking in the temple, in Solomon's Colonnade.",
    24: 'So the Jewish leaders surrounded Him and said to Him, "How long will You keep us in suspense? If You are the Christ, tell us plainly."',
    25: 'Jesus answered them, "I did tell you — and you do not believe. The works I do in My Father\'s name — these bear witness about Me.',
    26: "But you do not believe, because you are not of My sheep.",
    27: "My sheep hear My voice, and I know them, and they follow Me.",
    28: "I give them eternal life, and they shall never perish — ever. And no one will snatch them out of My hand.",
    29: "My Father, who has given them to Me, is greater than all. And no one can snatch them out of the Father's hand.",
    30: 'I and the Father are one."',
    31: "Again the Jewish leaders picked up stones to stone Him.",
    32: 'Jesus answered them, "I have shown you many good works from the Father. For which of these works are you stoning Me?"',
    33: 'The Jewish leaders answered Him, "We are not stoning You for a good work, but for blasphemy — because You, being a man, make Yourself God."',
    34: 'Jesus answered them, "Is it not written in your Law, \'I said, you are gods\'?',
    35: "If He called them 'gods,' to whom the word of God came — and the Scripture cannot be broken —",
    36: "do you say of the One whom the Father consecrated and sent into the world, 'You are blaspheming' — because I said, 'I am the Son of God'?",
    37: "If I am not doing the works of My Father, do not believe Me.",
    38: 'But if I am doing them, even though you do not believe Me, believe the works — so that you may know and understand that the Father is in Me, and I in the Father."',
    39: "Then they tried again to seize Him, but He escaped out of their hand.",
    40: "He went away again across the Jordan to the place where John had been baptizing at first, and stayed there.",
    41: 'Many came to Him. And they kept saying, "John did no sign — but everything John said about this Man was true."',
    42: "And many believed in Him there.",
}

CHAPTERS = {10: ch10}

def main():
    new_entries = {f"43_{ch}_{v}": text for ch, verses in CHAPTERS.items() for v, text in verses.items()}
    print(f"Chapter {list(CHAPTERS.keys())[0]}: {len(new_entries)} verses")

    with open(MBT_JOHN_PATH) as f:
        mbt_john = json.load(f)
    mbt_john.update(new_entries)
    with open(MBT_JOHN_PATH, "w") as f:
        json.dump(mbt_john, f, indent=2, ensure_ascii=False)
    print(f"mbt-john.json: {len(mbt_john)} total verses")

    with open(MOOP_PATH) as f:
        moop = json.load(f)
    moop.update(new_entries)
    with open(MOOP_PATH, "w") as f:
        json.dump(moop, f, ensure_ascii=False)
    print(f"moop-translation.json: merged {len(new_entries)} MBT John verses")

if __name__ == "__main__":
    main()
