"""
MBT John 8 — Woman Caught in Adultery (8:1-11, bracketed in earliest mss
but retained in most English Bibles and in moop-translation.json),
I Am the Light of the World, Where I Go You Cannot Come, Truth Will Set
You Free, Before Abraham Was, I Am. 59 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch8 = {
    1: "But Jesus went to the Mount of Olives.",
    2: "Early in the morning, He came again into the temple. All the people came to Him, and He sat down and began teaching them.",
    3: "Then the scribes and Pharisees brought in a woman caught in adultery. They stood her in the middle of the assembly",
    4: 'and said to Him, "Teacher, this woman was caught in the very act of adultery.',
    5: 'In the Law, Moses commanded us to stone such women. Now what do You say?"',
    6: "They said this to test Him, so that they would have grounds to accuse Him. But Jesus stooped down and began writing on the ground with His finger.",
    7: 'When they kept on questioning Him, He straightened up and said to them, "Let the one among you without sin be the first to throw a stone at her."',
    8: "And He stooped down again and went on writing on the ground.",
    9: "When they heard it, they went out one by one, beginning with the eldest — down to the last one. Jesus was left alone, with the woman standing there in the middle.",
    10: 'Jesus straightened up and said to her, "Woman, where are they? Has no one condemned you?"',
    11: 'She said, "No one, Lord." And Jesus said, "Neither do I condemn you. Go, and from now on sin no more."',
    12: 'Then Jesus spoke to them again and said, "I am the Light of the world. The one who follows Me will never walk in the darkness, but will have the light of life."',
    13: 'So the Pharisees said to Him, "You are bearing witness about Yourself. Your testimony is not true."',
    14: 'Jesus answered them, "Even if I bear witness about Myself, My testimony is true — because I know where I came from and where I am going. But you do not know where I come from or where I am going.',
    15: "You judge by the flesh; I judge no one.",
    16: "And even if I judge, My judgment is true — because I am not alone, but I and the Father who sent Me.",
    17: "Even in your own Law it is written that the testimony of two men is true.",
    18: 'I am the One who bears witness about Myself, and the Father who sent Me also bears witness about Me."',
    19: 'So they said to Him, "Where is Your Father?" Jesus answered, "You do not know Me, nor My Father. If you knew Me, you would know My Father also."',
    20: "He spoke these words in the treasury, as He was teaching in the temple. But no one arrested Him, because His hour had not yet come.",
    21: 'Then He said to them again, "I am going away, and you will look for Me, and you will die in your sin. Where I am going, you cannot come."',
    22: 'So the Jewish leaders were saying, "Will He kill Himself? Is that why He says, \'Where I am going, you cannot come\'?"',
    23: 'And He was saying to them, "You are from below; I am from above. You are of this world; I am not of this world.',
    24: 'I told you that you would die in your sins — for unless you believe that I am He, you will die in your sins."',
    25: 'So they said to Him, "Who are You?" Jesus said to them, "What I have been telling you from the beginning.',
    26: "I have many things to say about you and to judge. But the One who sent Me is true — and what I have heard from Him, these are the things I speak to the world.",
    27: "They did not understand that He had been speaking to them about the Father.",
    28: 'So Jesus said, "When you have lifted up the Son of Man, then you will know that I am He — and that I do nothing on My own authority, but speak just as the Father taught Me.',
    29: 'And the One who sent Me is with Me. He has not left Me alone — for I always do what is pleasing to Him."',
    30: "As He was saying these things, many believed in Him.",
    31: 'So Jesus said to the Jews who had believed in Him, "If you abide in My word, you are truly My disciples.',
    32: 'And you will know the truth, and the truth will set you free."',
    33: 'They answered Him, "We are Abraham\'s offspring, and we have never been slaves to anyone! How is it that You say, \'You will be made free\'?"',
    34: 'Jesus answered them, "Truly, truly, I tell you — everyone who commits sin is a slave to sin.',
    35: "A slave does not remain in the household forever; a son remains forever.",
    36: "So if the Son sets you free, you will be free indeed.",
    37: "I know that you are Abraham's offspring. Yet you seek to kill Me, because My word finds no place in you.",
    38: 'I speak of what I have seen with My Father, and you do what you have heard from your father."',
    39: 'They answered and said to Him, "Abraham is our father." Jesus said to them, "If you were Abraham\'s children, you would do the works of Abraham.',
    40: "But now you seek to kill Me — a Man who has told you the truth I heard from God. This is not what Abraham did.",
    41: 'You do the works of your own father." They said to Him, "We are not born of fornication. We have one Father — God."',
    42: 'Jesus said to them, "If God were your Father, you would love Me — for I came out from God, and I have come here. For I have not come on My own; He sent Me.',
    43: "Why do you not understand what I am saying? Because you cannot listen to My word.",
    44: "You are of your father, the devil — and the desires of your father you want to do. He was a murderer from the beginning, and has not stood in the truth, because there is no truth in him. Whenever he speaks a lie, he speaks from his own nature — for he is a liar, and the father of lies.",
    45: "But because I tell the truth, you do not believe Me.",
    46: "Which of you convicts Me of sin? And if I speak the truth, why do you not believe Me?",
    47: 'The one who is of God listens to God\'s words. The reason you do not listen is that you are not of God."',
    48: 'The Jewish leaders answered and said to Him, "Are we not right in saying that You are a Samaritan, and have a demon?"',
    49: 'Jesus answered, "I do not have a demon. I honor My Father, and you dishonor Me.',
    50: "I do not seek My own glory. There is One who seeks it — and He is the Judge.",
    51: 'Truly, truly, I tell you — if anyone keeps My word, he will never see death — ever."',
    52: 'The Jewish leaders said to Him, "Now we know You have a demon! Abraham died, and the prophets too — and You say, \'If anyone keeps My word, he will never taste death.\'',
    53: 'Are You greater than our father Abraham, who died? And the prophets died. Who do You make Yourself out to be?"',
    54: 'Jesus answered, "If I glorify Myself, My glory is nothing. It is My Father who glorifies Me — the One of whom you say, \'He is our God.\'',
    55: "And yet you have not known Him. But I know Him. If I said I did not know Him, I would be a liar like you. But I do know Him, and I keep His word.",
    56: 'Your father Abraham rejoiced to see My day. He saw it, and was glad."',
    57: 'So the Jewish leaders said to Him, "You are not yet fifty years old, and You have seen Abraham?"',
    58: 'Jesus said to them, "Truly, truly, I tell you — before Abraham was, I AM."',
    59: "So they picked up stones to throw at Him. But Jesus hid Himself and went out of the temple.",
}

CHAPTERS = {8: ch8}

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
