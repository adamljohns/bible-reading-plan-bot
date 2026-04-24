"""
MBT John 5 — Bethesda healing, The Authority of the Son, Witnesses to Jesus.
47 verses. Dense Christological discourse — needs care with 'sent', 'life',
'judgment', 'witness' terminology.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch5 = {
    1: "After this, there was a feast of the Jews, and Jesus went up to Jerusalem.",
    2: "Now in Jerusalem, by the Sheep Gate, there is a pool — called Bethesda in Hebrew — which has five covered colonnades.",
    3: "In these lay a crowd of disabled people — blind, lame, paralyzed — waiting for the water to be stirred.",
    4: "For at certain times an angel of the Lord went down into the pool and stirred the water. Whoever stepped in first, after the water was stirred, was healed of whatever ailment he had.",
    5: "And there was a certain man there who had been in his sickness for thirty-eight years.",
    6: 'When Jesus saw him lying there, and knew that he had already been there a long time, He said to him, "Do you want to be healed?"',
    7: 'The sick man answered Him, "Sir, I have no one to put me into the pool when the water is stirred. And while I am trying to get there, someone else steps down ahead of me."',
    8: 'Jesus said to him, "Get up. Pick up your mat and walk."',
    9: "At once the man was made whole — he picked up his mat and began walking. Now that day was a Sabbath.",
    10: 'So the Jewish leaders said to the man who had been healed, "It is the Sabbath. It is not lawful for you to carry your mat."',
    11: 'He answered them, "The one who made me whole — He Himself said to me, \'Pick up your mat and walk.\'"',
    12: 'They asked him, "Who is this Man who told you, \'Pick up your mat and walk\'?"',
    13: "But the healed man did not know who it was — Jesus had slipped away, for there was a crowd in the place.",
    14: 'Afterward, Jesus found him in the temple and said to him, "Look — you have been made whole. Do not sin anymore, so that nothing worse happens to you."',
    15: "The man went off and told the Jewish leaders that it was Jesus who had made him whole.",
    16: "So the Jewish leaders began to persecute Jesus, because He was doing these things on the Sabbath.",
    17: 'But Jesus answered them, "My Father has been working until now, and I too am working."',
    18: "This was why the Jewish leaders were all the more trying to kill Him — because He had not only broken the Sabbath, but was also calling God His own Father, making Himself equal with God.",
    19: 'So Jesus answered them, "Truly, truly, I tell you — the Son can do nothing on His own initiative; He can do only what He sees the Father doing. For whatever the Father does, the Son does likewise.',
    20: "For the Father loves the Son and shows Him everything He Himself is doing. And He will show Him greater works than these, so that you will be amazed.",
    21: "Just as the Father raises the dead and gives them life, so also the Son gives life to whomever He wills.",
    22: "For the Father judges no one; instead, He has given all judgment into the hands of the Son,",
    23: "so that everyone may honor the Son just as they honor the Father. The one who does not honor the Son does not honor the Father who sent Him.",
    24: "Truly, truly, I tell you — the one who hears My word and believes the One who sent Me has eternal life. He does not come into judgment, but has crossed over from death into life.",
    25: "Truly, truly, I tell you — an hour is coming, and is already here, when the dead will hear the voice of the Son of God, and those who hear will live.",
    26: "For just as the Father has life in Himself, so He has granted the Son to have life in Himself.",
    27: "And He has given Him the authority to carry out judgment — because He is the Son of Man.",
    28: "Do not be amazed at this, for an hour is coming when all who are in the tombs will hear His voice",
    29: "and will come out — those who have done good into a resurrection of life, and those who have practiced evil into a resurrection of judgment.",
    30: 'I can do nothing on My own initiative. As I hear, I judge — and My judgment is just, because I do not seek My own will but the will of the One who sent Me.',
    31: "If I bear witness about Myself, My testimony does not stand as proof.",
    32: "There is another who bears witness about Me, and I know that the testimony He bears about Me is true.",
    33: "You yourselves sent to John, and he has borne witness to the truth.",
    34: "Not that I rely on human testimony — but I say these things so that you may be saved.",
    35: "He was the lamp that was burning and shining, and you were willing for a while to rejoice in his light.",
    36: "But the witness I have is greater than John's. For the very works the Father has given Me to finish — the works I am doing — bear witness about Me, that the Father has sent Me.",
    37: "And the Father who sent Me — He Himself has borne witness about Me. You have never heard His voice, nor seen His form,",
    38: "and you do not have His word abiding in you — because you do not believe the One He sent.",
    39: "You search the Scriptures because you think that in them you have eternal life. And these very Scriptures bear witness about Me.",
    40: "Yet you are not willing to come to Me, that you may have life.",
    41: "I do not receive glory from people.",
    42: "But I know you — you do not have the love of God within you.",
    43: "I have come in My Father's name, and you do not receive Me. If another comes in his own name, him you will receive.",
    44: "How can you believe, when you receive glory from one another, but do not seek the glory that comes from the only God?",
    45: "Do not think that I will accuse you before the Father. The one who accuses you is Moses — the one in whom you have set your hope.",
    46: "If you believed Moses, you would believe Me — for he wrote about Me.",
    47: 'But if you do not believe his writings, how will you believe My words?"',
}

CHAPTERS = {5: ch5}

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
