"""
MBT John 9 — The Man Born Blind. 41 verses. The extended healing-and-
interrogation narrative. Key theme: spiritual vs. physical blindness.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch9 = {
    1: "As Jesus was passing by, He saw a man who had been blind from birth.",
    2: 'His disciples asked Him, "Rabbi, who sinned — this man, or his parents — that he was born blind?"',
    3: 'Jesus answered, "Neither this man nor his parents sinned. But this happened so that the works of God might be revealed in him.',
    4: "We must do the works of the One who sent Me while it is day. Night is coming, when no one can work.",
    5: 'While I am in the world, I am the Light of the world."',
    6: "Having said this, He spat on the ground, made mud with the saliva, and anointed the man's eyes with the mud.",
    7: 'Then He said to him, "Go, wash in the pool of Siloam" (which means Sent). So he went and washed, and came back seeing.',
    8: 'The neighbors, and those who had seen him before as a beggar, began saying, "Is this not the man who used to sit and beg?"',
    9: 'Some said, "This is he." Others said, "No, but he is like him." He himself kept saying, "I am the one."',
    10: 'So they said to him, "Then how were your eyes opened?"',
    11: 'He answered, "The Man called Jesus made mud, anointed my eyes, and said to me, \'Go to Siloam and wash.\' So I went and washed, and I received my sight."',
    12: 'And they said to him, "Where is He?" He said, "I do not know."',
    13: "They brought him — the one formerly blind — to the Pharisees.",
    14: "Now it was the Sabbath on the day Jesus made the mud and opened his eyes.",
    15: 'So the Pharisees also began to ask him how he had received his sight. He said to them, "He put mud on my eyes, and I washed, and I see."',
    16: 'So some of the Pharisees were saying, "This Man is not from God, because He does not keep the Sabbath." But others were saying, "How can a sinful man perform such signs?" And there was a division among them.',
    17: 'So they said to the blind man again, "What do you say about Him, since He opened your eyes?" He said, "He is a prophet."',
    18: "But the Jewish leaders did not believe this about him — that he had been blind and received his sight — until they called the parents of the one who had received his sight.",
    19: 'And they questioned them: "Is this your son, whom you say was born blind? How then does he now see?"',
    20: 'His parents answered them, "We know that this is our son, and that he was born blind.',
    21: 'But how he now sees, we do not know. And who opened his eyes, we do not know. Ask him — he is of age, he will speak for himself."',
    22: "His parents said this because they were afraid of the Jewish leaders, for the leaders had already agreed that if anyone confessed Him to be the Christ, he would be put out of the synagogue.",
    23: 'That is why his parents said, "He is of age; ask him."',
    24: 'So a second time they called the man who had been blind, and said to him, "Give glory to God! We know that this Man is a sinner."',
    25: 'He answered, "Whether He is a sinner, I do not know. One thing I do know — I was blind, and now I see."',
    26: 'They said to him, "What did He do to you? How did He open your eyes?"',
    27: 'He answered them, "I told you already, and you did not listen. Why do you want to hear it again? You do not want to become His disciples also, do you?"',
    28: 'They railed at him and said, "You are His disciple; we are disciples of Moses!',
    29: 'We know that God has spoken to Moses. But this Man — we do not know where He comes from."',
    30: 'The man answered and said to them, "Why, this is an amazing thing! You do not know where He is from — and yet He opened my eyes.',
    31: "We know that God does not listen to sinners. But if anyone is a worshiper of God and does His will, God listens to him.",
    32: "From the beginning of time it has never been heard that anyone opened the eyes of a man born blind.",
    33: 'If this Man were not from God, He could do nothing."',
    34: 'They answered and said to him, "You were born entirely in sin, and you teach us?" And they cast him out.',
    35: 'Jesus heard that they had cast him out. And when He found him, He said, "Do you believe in the Son of Man?"',
    36: 'He answered, "Who is He, sir, that I might believe in Him?"',
    37: 'Jesus said to him, "You have both seen Him — and He is the One speaking to you."',
    38: 'He said, "Lord, I believe!" And he worshiped Him.',
    39: 'And Jesus said, "For judgment I came into this world — so that those who do not see may see, and those who see may become blind."',
    40: 'Some of the Pharisees who were with Him heard this, and said to Him, "Are we blind also?"',
    41: 'Jesus said to them, "If you were blind, you would have no sin. But now you say, \'We see\' — so your sin remains."',
}

CHAPTERS = {9: ch9}

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
