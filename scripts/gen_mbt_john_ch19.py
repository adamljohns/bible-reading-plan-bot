"""
MBT John 19 — Flogged and Sentenced; The Crucifixion; Pierced and Buried.
42 verses. The crucifixion chapter, rendered with restraint — no
embellishment of horror, no flattening of dignity.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MBT_JOHN_PATH = ROOT / "docs" / "assets" / "mbt-john.json"
MOOP_PATH = ROOT / "docs" / "assets" / "moop-translation.json"

ch19 = {
    1: "Then Pilate took Jesus and had Him flogged.",
    2: "The soldiers wove a crown out of thorns and placed it on His head — and they dressed Him in a purple robe.",
    3: 'And they kept coming up to Him, saying, "Hail, King of the Jews!" And they struck Him with their hands.',
    4: 'Pilate went out again and said to them, "Look — I am bringing Him out to you, so that you may know I find no guilt in Him."',
    5: 'So Jesus came out, wearing the crown of thorns and the purple robe. And Pilate said to them, "Here is the Man!"',
    6: 'When the chief priests and the officers saw Him, they cried out, "Crucify Him! Crucify Him!" Pilate said to them, "Take Him yourselves and crucify Him — for I find no guilt in Him."',
    7: 'The Jewish leaders answered him, "We have a law, and by that law He ought to die — because He made Himself out to be the Son of God."',
    8: "When Pilate heard this, he was even more afraid,",
    9: 'and he went back into the headquarters and said to Jesus, "Where are You from?" But Jesus did not answer him.',
    10: 'So Pilate said to Him, "You will not speak to me? Do You not know that I have the authority to release You, and I have the authority to crucify You?"',
    11: 'Jesus answered him, "You would have no authority over Me at all, unless it had been given to you from above. For this reason, the one who handed Me over to you has the greater sin."',
    12: 'From then on, Pilate sought to release Him. But the Jewish leaders kept crying out, "If you release this Man, you are not a friend of Caesar. Anyone who makes himself out to be a king opposes Caesar."',
    13: "So when Pilate heard these words, he brought Jesus out and sat down on the judgment seat at a place called The Stone Pavement — in Hebrew, Gabbatha.",
    14: 'Now it was the day of preparation of the Passover. It was about the sixth hour. And he said to the Jewish leaders, "Here is your King!"',
    15: 'They cried out, "Take Him away! Take Him away! Crucify Him!" Pilate said to them, "Shall I crucify your King?" The chief priests answered, "We have no king but Caesar."',
    16: "Then he handed Him over to them to be crucified. So they took Jesus.",
    17: "And He, carrying His own cross, went out to the place called The Place of a Skull — in Hebrew, Golgotha —",
    18: "where they crucified Him, and with Him two others, one on either side, with Jesus in the middle.",
    19: 'Pilate also wrote an inscription and put it on the cross. It read: "JESUS OF NAZARETH, THE KING OF THE JEWS."',
    20: "Many of the Jews read this inscription, for the place where Jesus was crucified was near the city. And it was written in Hebrew, in Latin, and in Greek.",
    21: 'So the chief priests of the Jews said to Pilate, "Do not write, \'The King of the Jews,\' but rather, \'This Man said, I am King of the Jews.\'"',
    22: 'Pilate answered, "What I have written, I have written."',
    23: "The soldiers, when they had crucified Jesus, took His outer garments and divided them into four parts — a part for each soldier — and also the tunic. Now the tunic was seamless, woven in one piece from top to bottom.",
    24: "So they said to one another, \"Let us not tear it, but cast lots for it to decide whose it shall be\" — so that the Scripture might be fulfilled: 'They divided My garments among them, and for My clothing they cast lots.' So the soldiers did these things.",
    25: "Standing by the cross of Jesus were His mother, His mother's sister, Mary the wife of Clopas, and Mary Magdalene.",
    26: 'When Jesus saw His mother, and the disciple whom He loved standing beside her, He said to His mother, "Woman, behold your son!"',
    27: 'Then He said to the disciple, "Behold your mother!" And from that hour, the disciple took her into his own home.',
    28: 'After this, Jesus — knowing that all was now finished, and to fulfill the Scripture — said, "I thirst."',
    29: "A jar of sour wine was standing there, so they put a sponge full of the sour wine on a hyssop branch and held it to His mouth.",
    30: 'When Jesus had received the sour wine, He said, "It is finished." And bowing His head, He gave up His spirit.',
    31: "Since it was the day of preparation, and so that the bodies would not remain on the cross on the Sabbath — for that Sabbath was a high day — the Jewish leaders asked Pilate that their legs be broken, and that they be taken away.",
    32: "So the soldiers came and broke the legs of the first, and of the other who had been crucified with Him.",
    33: "But when they came to Jesus and saw that He was already dead, they did not break His legs.",
    34: "Instead, one of the soldiers pierced His side with a spear — and at once blood and water came out.",
    35: "The one who saw it has testified — and his testimony is true. He knows that he is telling the truth, so that you also may believe.",
    36: "For these things took place to fulfill the Scripture: 'Not one of His bones shall be broken.'",
    37: "And again, another Scripture says: 'They will look on the One they have pierced.'",
    38: "After this, Joseph of Arimathea — a disciple of Jesus, but secretly, for fear of the Jewish leaders — asked Pilate for permission to take away the body of Jesus. Pilate gave him permission, so he came and took away His body.",
    39: "Nicodemus also — the one who had first come to Him by night — came bringing a mixture of myrrh and aloes, about a hundred pounds in weight.",
    40: "So they took the body of Jesus and bound it in linen cloths with the spices, according to the burial custom of the Jews.",
    41: "Now in the place where He was crucified there was a garden, and in the garden a new tomb — in which no one had yet been laid.",
    42: "So because it was the Jewish day of preparation, and the tomb was nearby, they laid Jesus there.",
}

CHAPTERS = {19: ch19}

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
