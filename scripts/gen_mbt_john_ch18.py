"""
MBT John 18 — Betrayal and Arrest; Before Annas; Peter's Denials;
Before Pilate. 40 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch18 = {
    1: "Having said these things, Jesus went out with His disciples across the brook Kidron, where there was a garden — and He and His disciples went into it.",
    2: "Now Judas, who was betraying Him, also knew the place — because Jesus often met there with His disciples.",
    3: "So Judas, having obtained a cohort of soldiers and some officers from the chief priests and the Pharisees, came there with lanterns, torches, and weapons.",
    4: 'Jesus, knowing everything that was coming upon Him, stepped forward and said to them, "Whom are you looking for?"',
    5: 'They answered Him, "Jesus the Nazarene." He said to them, "I am He." (Judas, who was betraying Him, was standing with them.)',
    6: 'When He said to them, "I am He," they drew back and fell to the ground.',
    7: 'So He asked them again, "Whom are you looking for?" And they said, "Jesus the Nazarene."',
    8: 'Jesus answered, "I told you that I am He. So if you are looking for Me, let these men go."',
    9: "This was to fulfill the word He had spoken: 'Of those You gave Me, I have not lost one.'",
    10: "Then Simon Peter, who had a sword, drew it and struck the high priest's servant and cut off his right ear. The servant's name was Malchus.",
    11: 'So Jesus said to Peter, "Put the sword back into its sheath. Shall I not drink the cup the Father has given Me?"',
    12: "So the cohort, the commander, and the officers of the Jewish leaders arrested Jesus and bound Him.",
    13: "They led Him first to Annas, for he was the father-in-law of Caiaphas, who was high priest that year.",
    14: "It was Caiaphas who had advised the Jewish leaders that it was better that one man should die for the people.",
    15: "Now Simon Peter and another disciple were following Jesus. That disciple was known to the high priest, and entered with Jesus into the courtyard of the high priest.",
    16: "But Peter stood outside at the door. So the other disciple, who was known to the high priest, went out and spoke to the doorkeeper, and brought Peter in.",
    17: 'The servant girl at the door said to Peter, "You are not one of this Man\'s disciples, are you?" He said, "I am not."',
    18: "Now the servants and the officers had made a charcoal fire because it was cold — and they were standing and warming themselves. Peter also was standing with them, warming himself.",
    19: "The high priest then questioned Jesus about His disciples and His teaching.",
    20: 'Jesus answered him, "I have spoken openly to the world. I always taught in a synagogue and in the temple, where all the Jews come together — and I said nothing in secret.',
    21: 'Why do you question Me? Question those who heard what I said to them. They know what I said."',
    22: 'When He had said this, one of the officers standing nearby struck Jesus with his hand, saying, "Is that how You answer the high priest?"',
    23: 'Jesus answered him, "If I have spoken wrongly, testify to the wrong. But if rightly, why do you strike Me?"',
    24: "Then Annas sent Him, still bound, to Caiaphas the high priest.",
    25: 'Meanwhile, Simon Peter was standing and warming himself. So they said to him, "You are not one of His disciples, are you?" He denied it and said, "I am not."',
    26: 'One of the high priest\'s servants — a relative of the one whose ear Peter had cut off — said, "Did I not see you in the garden with Him?"',
    27: "Peter again denied it — and at once a rooster crowed.",
    28: "Then they led Jesus from Caiaphas to the governor's headquarters. It was early morning. They themselves did not go into the headquarters, so that they would not be defiled, but could eat the Passover.",
    29: 'So Pilate went out to them and said, "What accusation do you bring against this Man?"',
    30: 'They answered him, "If He were not a criminal, we would not have handed Him over to you."',
    31: 'Pilate said to them, "Take Him yourselves and judge Him by your own law." The Jewish leaders said to him, "We are not permitted to put anyone to death."',
    32: "This was so that the word of Jesus might be fulfilled, which He had spoken to show by what kind of death He was about to die.",
    33: 'So Pilate went back into the headquarters, called Jesus, and said to Him, "Are You the King of the Jews?"',
    34: 'Jesus answered, "Are you saying this on your own — or have others told you about Me?"',
    35: 'Pilate answered, "Am I a Jew? Your own nation and the chief priests have delivered You to me. What have You done?"',
    36: 'Jesus answered, "My kingdom is not of this world. If My kingdom were of this world, My servants would have been fighting, so that I would not be handed over to the Jewish leaders. But as it is, My kingdom is not from here."',
    37: 'So Pilate said to Him, "So You are a king?" Jesus answered, "You say that I am a king. For this reason I was born, and for this reason I came into the world — to testify to the truth. Everyone who is of the truth listens to My voice."',
    38: 'Pilate said to Him, "What is truth?" And having said this, he went out again to the Jewish leaders and said to them, "I find no guilt in Him.',
    39: 'But it is your custom that I release one prisoner to you at the Passover. So do you want me to release to you the King of the Jews?"',
    40: 'They cried out again, "Not this Man, but Barabbas!" Now Barabbas was a robber.',
}

CHAPTERS = {18: ch18}

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
