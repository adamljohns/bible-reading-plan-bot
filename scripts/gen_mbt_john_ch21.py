"""
MBT John 21 — Jesus Appears by the Sea; 'Do You Love Me?'; John's
Testimony True. 25 verses. The final chapter — Peter restored,
disciple prediction, narrator's closing note.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch21 = {
    1: "After these things, Jesus revealed Himself again to the disciples by the Sea of Tiberias — and He revealed Himself in this way.",
    2: "Simon Peter, Thomas (called the Twin), Nathanael of Cana in Galilee, the sons of Zebedee, and two others of His disciples were together.",
    3: 'Simon Peter said to them, "I am going fishing." They said to him, "We are going with you." So they went out and got into the boat — but that night they caught nothing.',
    4: "Just as day was breaking, Jesus stood on the shore — but the disciples did not know it was Jesus.",
    5: 'So Jesus said to them, "Children, do you have any fish?" They answered Him, "No."',
    6: 'He said to them, "Cast the net on the right side of the boat, and you will find some." So they cast it — and now they were not able to haul it in, because of the quantity of fish.',
    7: 'That disciple whom Jesus loved said to Peter, "It is the Lord!" When Simon Peter heard that it was the Lord, he pulled his outer garment around him — for he was stripped for work — and threw himself into the sea.',
    8: "The other disciples came in the little boat, dragging the net full of fish — for they were not far from the land, only about a hundred yards off.",
    9: "When they got out on the land, they saw a charcoal fire laid there, with fish on it, and bread.",
    10: 'Jesus said to them, "Bring some of the fish you just caught."',
    11: "So Simon Peter went aboard and hauled the net to land — full of large fish, a hundred and fifty-three of them. And though there were so many, the net was not torn.",
    12: 'Jesus said to them, "Come, have breakfast." Now none of the disciples dared to ask Him, "Who are You?" — because they knew it was the Lord.',
    13: "Jesus came, took the bread, and gave it to them. And He did the same with the fish.",
    14: "This was now the third time Jesus was revealed to the disciples after He was raised from the dead.",
    15: 'When they had finished breakfast, Jesus said to Simon Peter, "Simon, son of John, do you love Me more than these?" Peter said to Him, "Yes, Lord — You know that I love You." Jesus said to him, "Feed My lambs."',
    16: 'He said to him again, a second time, "Simon, son of John, do you love Me?" Peter said to Him, "Yes, Lord — You know that I love You." Jesus said to him, "Take care of My sheep."',
    17: 'He said to him a third time, "Simon, son of John, do you love Me?" Peter was grieved because He had said to him the third time, "Do you love Me?" And he said to Him, "Lord, You know all things — You know that I love You." Jesus said to him, "Feed My sheep.',
    18: "Truly, truly, I tell you — when you were young, you used to dress yourself and walk wherever you wanted. But when you grow old, you will stretch out your hands, and another will dress you and carry you where you do not want to go.",
    19: 'He said this to show by what kind of death Peter would glorify God. And after saying this, He said to him, "Follow Me."',
    20: 'Peter turned and saw the disciple whom Jesus loved following them — the one who had also leaned back against Jesus at the supper and said, "Lord, who is the one who is going to betray You?"',
    21: 'When Peter saw him, he said to Jesus, "Lord, what about this man?"',
    22: 'Jesus said to him, "If I want him to remain until I come, what is that to you? You follow Me."',
    23: 'So the rumor spread among the brothers that this disciple was not going to die. Yet Jesus did not tell him that he was not going to die — but, "If I want him to remain until I come, what is that to you?"',
    24: "This is the disciple who is bearing witness to these things, and has written these things. And we know that his testimony is true.",
    25: "There are also many other things that Jesus did. If every one of them were written down, I suppose that even the world itself could not contain the books that would be written.",
}

CHAPTERS = {21: ch21}

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
