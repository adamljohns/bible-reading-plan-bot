"""Build red-letter-map.json — verse ranges that are the words of Christ.

Drives the BTE red-letter edition: verses in these ranges render in red when
Verse Tools are shown (and revert to normal under Hide Tools, matching the
dictionary-underline behavior).

Scope (v1): the large, UNAMBIGUOUS discourses + high-confidence sayings where
Jesus is clearly the speaker. Authored conservatively — we'd rather under-color
(miss a little red, easily added later) than over-color a narrator's line. The
map is keyed bookId -> chapter -> [[start,end], ...] and is trivially extensible:
add verified ranges here and re-run; no engine changes needed.

Coloring is whole-verse within a range (the standard print red-letter behavior),
which is exactly right for continuous discourses (the bulk of red text).
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "red-letter-map.json"

def R(*pairs):
    return [list(p) for p in pairs]

# bookId -> { chapter(str) -> [[start,end], ...] }
RED = {
    # ── Matthew (40) ──
    "40": {
        "3": R((15,15)),
        "4": R((4,4),(7,7),(10,10),(17,17),(19,19)),
        "5": R((3,48)), "6": R((1,34)), "7": R((1,27)),          # Sermon on the Mount
        "8": R((3,3),(4,4),(7,7),(10,13),(20,20),(22,22),(26,26),(32,32)),
        "9": R((2,2),(4,6),(9,9),(12,13),(15,17),(22,22),(24,24),(28,28),(29,30),(37,38)),
        "10": R((5,42)),                                          # Missionary discourse
        "11": R((4,6),(7,19),(21,24),(25,30)),
        "12": R((3,8),(11,13),(25,37),(39,45),(48,50)),
        "13": R((3,9),(11,23),(24,30),(31,35),(37,52),(57,57)),   # Parables
        "15": R((3,9),(10,11),(13,14),(16,20),(24,24),(26,26),(28,28),(32,32),(34,34)),
        "16": R((2,4),(6,6),(8,11),(15,15),(17,20),(23,28)),
        "18": R((3,35)),                                          # Community discourse
        "19": R((4,6),(8,9),(11,12),(14,14),(17,26),(28,30)),
        "20": R((1,16),(18,19),(21,23),(25,28),(32,32)),
        "21": R((13,13),(16,16),(21,22),(24,27),(28,44)),
        "22": R((18,21),(29,32),(37,40),(42,45)),
        "23": R((2,39)),                                          # Woes to the Pharisees
        "24": R((2,51)), "25": R((1,46)),                         # Olivet Discourse
        "26": R((10,13),(18,18),(21,21),(26,29),(31,32),(34,34),(45,46),(52,54),(64,64)),
        "28": R((10,10),(18,20)),                                 # Great Commission
    },
    # ── Mark (41) ──
    "41": {
        "1": R((15,15),(17,17),(38,38)),
        "2": R((5,5),(8,11),(17,17),(19,22),(25,28)),
        "3": R((23,29),(33,35)),
        "4": R((3,9),(11,13),(21,32),(39,40)),
        "7": R((6,16),(18,23),(27,27)),
        "8": R((34,38)),
        "9": R((1,1),(39,50)),
        "10": R((5,9),(14,15),(18,21),(23,27),(29,31),(42,45)),
        "12": R((1,11),(24,27),(29,31),(38,40)),
        "13": R((5,37)),                                          # Olivet Discourse
        "14": R((6,9),(22,25),(27,28),(36,36),(62,62)),
        "16": R((15,18)),
    },
    # ── Luke (42) ──
    "42": {
        "4": R((4,4),(8,8),(12,12),(18,21),(23,27)),
        "6": R((20,49)),                                          # Sermon on the Plain
        "8": R((11,18)),
        "9": R((22,27),(58,60),(62,62)),
        "10": R((2,16),(18,24),(30,37)),                          # incl. Good Samaritan
        "11": R((2,13),(17,26),(29,36),(39,52)),
        "12": R((1,40),(42,59)),                                  # Do not be anxious, etc.
        "13": R((24,30),(32,35)),
        "14": R((8,14),(16,24),(28,35)),
        "15": R((3,32)),                                          # Lost sheep/coin/son
        "16": R((1,13),(19,31)),                                  # incl. Rich man & Lazarus
        "17": R((1,4),(20,37)),
        "18": R((1,8),(9,14),(16,17),(19,30)),
        "19": R((12,27),(42,44),(46,46)),
        "20": R((9,18),(34,38),(41,44),(46,47)),
        "21": R((8,36)),                                          # Olivet Discourse
        "22": R((15,18),(19,20),(25,30),(35,38)),
        "23": R((28,31),(34,34),(43,43),(46,46)),
        "24": R((25,26),(38,49)),
    },
    # ── John (43) — discourse-heavy. Ranges exclude the disciples'/crowd's
    #    interjections so only Jesus' words are red (whole-verse within each range). ──
    "43": {
        "3": R((3,21)),                                           # To Nicodemus (incl. 3:16)
        "4": R((10,10),(13,14),(21,24),(26,26),(32,32),(34,38)),
        "5": R((19,47)),                                          # The authority of the Son
        "6": R((26,27),(29,29),(32,40),(43,51),(53,58),(61,65)),  # Bread of Life (excl. crowd 28,30-31,41-42,52)
        "7": R((16,24),(37,38)),
        "8": R((12,12),(31,32),(34,38),(42,47),(54,56),(58,58)),  # excl. the Jews' replies 33,39-41,48-53,57
        "10": R((1,18),(25,30),(32,32),(34,38)),                  # Good Shepherd (excl. 19-24,31,33,39)
        "12": R((23,28),(30,32),(35,36),(44,50)),
        "13": R((12,20),(31,35),(38,38)),                         # excl. Peter's question 36-37
        "14": R((1,4),(6,7),(9,21),(23,31)),                      # excl. Thomas 5, Philip 8, Judas 22
        "15": R((1,27)),                                          # all Jesus
        "16": R((1,16),(19,28),(31,33)),                          # excl. disciples 17-18, 29-30
        "17": R((1,26)),                                          # High Priestly Prayer (all Jesus)
        "18": R((20,21),(23,23),(36,37)),
        "20": R((15,15),(16,16),(17,17),(19,19),(21,23),(26,29)),
        "21": R((15,17),(18,19),(22,22)),
    },
    # ── Acts (44) — risen/ascended Christ speaks ──
    "44": {
        "1": R((7,8)),
        "9": R((4,6),(10,16)),
        "18": R((9,10)),
        "22": R((7,8),(10,10),(18,21)),
        "23": R((11,11)),
        "26": R((14,18)),
    },
    # ── Revelation (66) — the glorified Christ speaks ──
    "66": {
        "1": R((8,8),(11,11),(17,20)),
        "2": R((1,29)), "3": R((1,22)),                           # Letters to the seven churches
        "16": R((15,15)),
        "22": R((7,7),(12,16),(20,20)),
    },
}

def main():
    # Validate ranges are well-formed
    problems = 0
    for bk, chs in RED.items():
        for ch, ranges in chs.items():
            for r in ranges:
                if r[0] > r[1]:
                    print(f"  ERR {bk} {ch}: start>end {r}"); problems += 1
    if problems:
        raise SystemExit(f"{problems} problem(s)")

    meta = {"_meta": {
        "description": "BTE red-letter edition — verse ranges that are the words of Christ. "
                       "Whole-verse coloring within each range; shown only when Verse Tools are "
                       "active (hidden under Hide Tools). v1 covers the major discourses + "
                       "high-confidence sayings, authored conservatively; extensible.",
        "coverage": "Gospels + Acts + Revelation (major discourses, v1)",
    }}
    out = {**meta, **RED}
    nranges = sum(len(r) for chs in RED.values() for r in chs.values())
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT}: {len(RED)} books, {nranges} red-letter ranges")

if __name__ == "__main__":
    main()
