"""
MBT John 20 — The Empty Tomb; Jesus Appears to Mary; to the Disciples;
Jesus and Thomas; Purpose of This Book. 31 verses.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch20 = {
    1: "Now on the first day of the week, Mary Magdalene came to the tomb early, while it was still dark, and she saw that the stone had been taken away from the tomb.",
    2: 'So she ran and came to Simon Peter, and to the other disciple whom Jesus loved, and said to them, "They have taken the Lord out of the tomb, and we do not know where they have laid Him!"',
    3: "So Peter and the other disciple went out and were going toward the tomb.",
    4: "The two were running together, but the other disciple outran Peter and arrived at the tomb first.",
    5: "And stooping down, he saw the linen cloths lying there — but he did not go in.",
    6: "Then Simon Peter came, following him, and went into the tomb. He saw the linen cloths lying there,",
    7: "and the face cloth that had been on Jesus' head — not lying with the linen cloths, but folded up in a place by itself.",
    8: "Then the other disciple, who had reached the tomb first, also went in. He saw — and he believed.",
    9: "For as yet they did not know the Scripture — that He must rise from the dead.",
    10: "Then the disciples went back to their homes.",
    11: "But Mary stood outside at the tomb, weeping. And as she wept, she stooped down to look into the tomb,",
    12: "and she saw two angels in white — seated, one at the head, and one at the feet, where the body of Jesus had been lying.",
    13: 'They said to her, "Woman, why are you weeping?" She said to them, "They have taken away my Lord, and I do not know where they have laid Him."',
    14: "When she had said this, she turned around and saw Jesus standing there — but she did not know it was Jesus.",
    15: 'Jesus said to her, "Woman, why are you weeping? Whom are you looking for?" Thinking He was the gardener, she said to Him, "Sir, if you have carried Him away, tell me where you have laid Him — and I will take Him away."',
    16: 'Jesus said to her, "Mary." She turned and said to Him in Hebrew, "Rabboni!" — which means \'Teacher.\'',
    17: 'Jesus said to her, "Do not cling to Me, for I have not yet ascended to the Father. But go to My brothers and tell them, \'I am ascending to My Father and your Father, to My God and your God.\'"',
    18: 'Mary Magdalene came and announced to the disciples, "I have seen the Lord!" — and that He had said these things to her.',
    19: 'On the evening of that first day of the week, when the doors were locked where the disciples were, for fear of the Jewish leaders, Jesus came and stood among them. And He said to them, "Peace be with you."',
    20: "Having said this, He showed them His hands and His side. The disciples rejoiced when they saw the Lord.",
    21: 'So Jesus said to them again, "Peace be with you. As the Father has sent Me, I also send you."',
    22: 'And having said this, He breathed on them and said to them, "Receive the Holy Spirit.',
    23: 'If you forgive the sins of any, their sins are forgiven them. If you withhold forgiveness from any, it is withheld."',
    24: "But Thomas, one of the twelve, called the Twin, was not with them when Jesus came.",
    25: 'So the other disciples were saying to him, "We have seen the Lord!" But he said to them, "Unless I see in His hands the mark of the nails, and put my finger where the nails were, and put my hand into His side — I will never believe."',
    26: 'Eight days later, His disciples were again inside, and Thomas was with them. Jesus came, though the doors were locked, and stood among them and said, "Peace be with you."',
    27: 'Then He said to Thomas, "Put your finger here, and see My hands. Reach your hand out and put it into My side. And do not be unbelieving — but believing."',
    28: 'Thomas answered and said to Him, "My Lord and my God!"',
    29: 'Jesus said to him, "Because you have seen Me, you have believed. Blessed are those who have not seen — and yet have believed."',
    30: "Jesus performed many other signs in the presence of His disciples, which are not written in this book.",
    31: "But these have been written so that you may believe that Jesus is the Christ, the Son of God — and so that by believing, you may have life in His name.",
}

CHAPTERS = {20: ch20}

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
