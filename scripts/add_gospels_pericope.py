"""Add Matthew (40), Mark (41), Luke (42) to pericope-map.json — completing the NT.

The map already covers John (43) through Revelation (66). The three Synoptic
Gospels fell back to the crude "break every 4 verses" heuristic in paragraph
mode. This adds editorial section breaks for them, anchored on NKJV + ESV
section-header consensus (same standard as the existing 24-book map).

Only the `start` verse of each section drives paragraph breaks; `end`/`title`
are metadata. Sections are contiguous (each start = previous end + 1) and the
final section of each chapter ends on that chapter's true last verse.

Idempotent: re-running re-sets the same keys. Merges, never clobbers other books.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "docs" / "assets" / "pericope-map.json"

def S(start, end, title):
    return {"start": start, "end": end, "title": title}

# ── Matthew (40) ─────────────────────────────────────────────────────────────
MATTHEW = {
    1:  [S(1,17,"The Genealogy of Jesus"), S(18,25,"The Birth of Jesus Christ")],
    2:  [S(1,12,"The Visit of the Wise Men"), S(13,15,"The Flight to Egypt"), S(16,18,"Herod Kills the Children"), S(19,23,"The Return to Nazareth")],
    3:  [S(1,12,"John the Baptist Prepares the Way"), S(13,17,"The Baptism of Jesus")],
    4:  [S(1,11,"The Temptation of Jesus"), S(12,17,"Jesus Begins His Ministry"), S(18,22,"Jesus Calls the First Disciples"), S(23,25,"Jesus Ministers to the Crowds")],
    5:  [S(1,12,"The Beatitudes"), S(13,16,"Salt and Light"), S(17,20,"Christ and the Law"), S(21,26,"Anger"), S(27,30,"Lust"), S(31,32,"Divorce"), S(33,37,"Oaths"), S(38,42,"Retaliation"), S(43,48,"Love Your Enemies")],
    6:  [S(1,4,"Giving to the Needy"), S(5,15,"The Lord's Prayer"), S(16,18,"Fasting"), S(19,24,"Treasures in Heaven"), S(25,34,"Do Not Worry")],
    7:  [S(1,6,"Judging Others"), S(7,12,"Ask, Seek, Knock"), S(13,14,"The Narrow Gate"), S(15,20,"A Tree and Its Fruit"), S(21,23,"I Never Knew You"), S(24,29,"The Wise and Foolish Builders")],
    8:  [S(1,4,"Jesus Cleanses a Leper"), S(5,13,"The Faith of the Centurion"), S(14,17,"Jesus Heals Many"), S(18,22,"The Cost of Following Jesus"), S(23,27,"Jesus Calms a Storm"), S(28,34,"Jesus Heals Two Demon-Possessed Men")],
    9:  [S(1,8,"Jesus Heals a Paralytic"), S(9,13,"The Calling of Matthew"), S(14,17,"A Question About Fasting"), S(18,26,"A Girl Restored and a Woman Healed"), S(27,34,"Jesus Heals the Blind and Mute"), S(35,38,"The Harvest Is Plentiful")],
    10: [S(1,15,"Jesus Sends Out the Twelve"), S(16,25,"Persecution Will Come"), S(26,33,"Have No Fear"), S(34,39,"Not Peace, but a Sword"), S(40,42,"Rewards")],
    11: [S(1,19,"Messengers from John the Baptist"), S(20,24,"Woe to Unrepentant Cities"), S(25,30,"Come to Me and Rest")],
    12: [S(1,8,"Jesus Is Lord of the Sabbath"), S(9,21,"The Man with a Withered Hand"), S(22,32,"Jesus and Beelzebul"), S(33,37,"A Tree and Its Fruit"), S(38,45,"The Sign of Jonah"), S(46,50,"Jesus' Mother and Brothers")],
    13: [S(1,23,"The Parable of the Sower"), S(24,30,"The Parable of the Weeds"), S(31,35,"Mustard Seed and Leaven"), S(36,43,"The Weeds Explained"), S(44,52,"Hidden Treasure, Pearl, and Net"), S(53,58,"A Prophet Without Honor")],
    14: [S(1,12,"The Death of John the Baptist"), S(13,21,"Jesus Feeds the Five Thousand"), S(22,33,"Jesus Walks on the Water"), S(34,36,"Jesus Heals at Gennesaret")],
    15: [S(1,9,"Traditions and Commandments"), S(10,20,"What Defiles a Person"), S(21,28,"The Faith of a Canaanite Woman"), S(29,39,"Jesus Feeds the Four Thousand")],
    16: [S(1,4,"The Pharisees Demand a Sign"), S(5,12,"The Leaven of the Pharisees"), S(13,20,"Peter Confesses Jesus as the Christ"), S(21,28,"Jesus Foretells His Death")],
    17: [S(1,13,"The Transfiguration"), S(14,21,"Jesus Heals a Boy with a Demon"), S(22,23,"Jesus Again Foretells His Death"), S(24,27,"The Temple Tax")],
    18: [S(1,9,"Who Is the Greatest"), S(10,14,"The Parable of the Lost Sheep"), S(15,20,"If Your Brother Sins"), S(21,35,"The Unforgiving Servant")],
    19: [S(1,12,"Teaching About Divorce"), S(13,15,"Let the Children Come"), S(16,30,"The Rich Young Man")],
    20: [S(1,16,"Laborers in the Vineyard"), S(17,19,"A Third Time Jesus Foretells His Death"), S(20,28,"A Mother's Request"), S(29,34,"Jesus Heals Two Blind Men")],
    21: [S(1,11,"The Triumphal Entry"), S(12,17,"Jesus Cleanses the Temple"), S(18,22,"The Fig Tree Cursed"), S(23,27,"Jesus' Authority Questioned"), S(28,32,"The Parable of the Two Sons"), S(33,46,"The Parable of the Tenants")],
    22: [S(1,14,"The Parable of the Wedding Feast"), S(15,22,"Paying Taxes to Caesar"), S(23,33,"The Resurrection and Marriage"), S(34,40,"The Great Commandment"), S(41,46,"Whose Son Is the Christ")],
    23: [S(1,36,"Woes to the Scribes and Pharisees"), S(37,39,"Lament over Jerusalem")],
    24: [S(1,14,"Signs of the End of the Age"), S(15,28,"The Great Tribulation"), S(29,31,"The Coming of the Son of Man"), S(32,35,"The Lesson of the Fig Tree"), S(36,44,"No One Knows the Day or Hour"), S(45,51,"The Faithful Servant")],
    25: [S(1,13,"The Ten Virgins"), S(14,30,"The Parable of the Talents"), S(31,46,"The Sheep and the Goats")],
    26: [S(1,5,"The Plot to Kill Jesus"), S(6,13,"The Anointing at Bethany"), S(14,16,"Judas Agrees to Betray Jesus"), S(17,30,"The Passover and the Lord's Supper"), S(31,35,"Peter's Denial Foretold"), S(36,46,"Gethsemane"), S(47,56,"The Betrayal and Arrest"), S(57,68,"Jesus Before the Council"), S(69,75,"Peter Denies Jesus")],
    27: [S(1,10,"The Death of Judas"), S(11,26,"Jesus Before Pilate"), S(27,31,"The Soldiers Mock Jesus"), S(32,44,"The Crucifixion"), S(45,56,"The Death of Jesus"), S(57,61,"The Burial of Jesus"), S(62,66,"The Guard at the Tomb")],
    28: [S(1,10,"The Resurrection"), S(11,15,"The Report of the Guard"), S(16,20,"The Great Commission")],
}

# ── Mark (41) ────────────────────────────────────────────────────────────────
MARK = {
    1:  [S(1,8,"John the Baptist Prepares the Way"), S(9,13,"The Baptism and Temptation"), S(14,20,"Jesus Calls the First Disciples"), S(21,28,"Jesus Heals a Man with an Unclean Spirit"), S(29,39,"Jesus Heals Many"), S(40,45,"Jesus Cleanses a Leper")],
    2:  [S(1,12,"Jesus Heals a Paralytic"), S(13,17,"The Calling of Levi"), S(18,22,"A Question About Fasting"), S(23,28,"Jesus Is Lord of the Sabbath")],
    3:  [S(1,6,"A Man with a Withered Hand"), S(7,12,"A Great Crowd Follows Jesus"), S(13,19,"Jesus Appoints the Twelve"), S(20,30,"Jesus and Beelzebul"), S(31,35,"Jesus' Mother and Brothers")],
    4:  [S(1,20,"The Parable of the Sower"), S(21,25,"A Lamp Under a Basket"), S(26,29,"The Seed Growing"), S(30,34,"The Mustard Seed"), S(35,41,"Jesus Calms a Storm")],
    5:  [S(1,20,"Jesus Heals the Gerasene Demoniac"), S(21,43,"A Girl Restored and a Woman Healed")],
    6:  [S(1,6,"Jesus Rejected at Nazareth"), S(7,13,"Jesus Sends Out the Twelve"), S(14,29,"The Death of John the Baptist"), S(30,44,"Jesus Feeds the Five Thousand"), S(45,52,"Jesus Walks on the Water"), S(53,56,"Jesus Heals at Gennesaret")],
    7:  [S(1,13,"Traditions and Commandments"), S(14,23,"What Defiles a Person"), S(24,30,"The Syrophoenician Woman's Faith"), S(31,37,"Jesus Heals a Deaf Man")],
    8:  [S(1,10,"Jesus Feeds the Four Thousand"), S(11,21,"The Pharisees Demand a Sign"), S(22,26,"Jesus Heals a Blind Man at Bethsaida"), S(27,30,"Peter Confesses Jesus as the Christ"), S(31,38,"Jesus Foretells His Death")],
    9:  [S(1,13,"The Transfiguration"), S(14,29,"Jesus Heals a Boy with an Unclean Spirit"), S(30,32,"Jesus Again Foretells His Death"), S(33,37,"Who Is the Greatest"), S(38,50,"Anyone Not Against Us Is for Us")],
    10: [S(1,12,"Teaching About Divorce"), S(13,16,"Let the Children Come"), S(17,31,"The Rich Young Man"), S(32,34,"A Third Time Jesus Foretells His Death"), S(35,45,"The Request of James and John"), S(46,52,"Jesus Heals Blind Bartimaeus")],
    11: [S(1,11,"The Triumphal Entry"), S(12,14,"Jesus Curses the Fig Tree"), S(15,19,"Jesus Cleanses the Temple"), S(20,26,"The Lesson from the Fig Tree"), S(27,33,"Jesus' Authority Questioned")],
    12: [S(1,12,"The Parable of the Tenants"), S(13,17,"Paying Taxes to Caesar"), S(18,27,"The Resurrection and Marriage"), S(28,34,"The Great Commandment"), S(35,37,"Whose Son Is the Christ"), S(38,40,"Beware of the Scribes"), S(41,44,"The Widow's Offering")],
    13: [S(1,13,"Signs of the End of the Age"), S(14,23,"The Great Tribulation"), S(24,31,"The Coming of the Son of Man"), S(32,37,"No One Knows the Day or Hour")],
    14: [S(1,11,"The Plot and the Anointing at Bethany"), S(12,25,"The Passover and the Lord's Supper"), S(26,31,"Peter's Denial Foretold"), S(32,42,"Gethsemane"), S(43,52,"The Betrayal and Arrest"), S(53,65,"Jesus Before the Council"), S(66,72,"Peter Denies Jesus")],
    15: [S(1,15,"Jesus Before Pilate"), S(16,20,"The Soldiers Mock Jesus"), S(21,32,"The Crucifixion"), S(33,41,"The Death of Jesus"), S(42,47,"The Burial of Jesus")],
    16: [S(1,8,"The Resurrection"), S(9,13,"Jesus Appears After the Resurrection"), S(14,20,"The Great Commission")],
}

# ── Luke (42) ────────────────────────────────────────────────────────────────
LUKE = {
    1:  [S(1,4,"Dedication to Theophilus"), S(5,25,"The Birth of John the Baptist Foretold"), S(26,38,"The Birth of Jesus Foretold"), S(39,45,"Mary Visits Elizabeth"), S(46,56,"Mary's Song of Praise"), S(57,66,"The Birth of John the Baptist"), S(67,80,"Zechariah's Prophecy")],
    2:  [S(1,7,"The Birth of Jesus"), S(8,20,"The Shepherds and the Angels"), S(21,40,"Jesus Presented at the Temple"), S(41,52,"The Boy Jesus at the Temple")],
    3:  [S(1,20,"John the Baptist Prepares the Way"), S(21,22,"The Baptism of Jesus"), S(23,38,"The Genealogy of Jesus")],
    4:  [S(1,13,"The Temptation of Jesus"), S(14,30,"Jesus Rejected at Nazareth"), S(31,37,"Jesus Heals a Man with an Unclean Spirit"), S(38,44,"Jesus Heals Many")],
    5:  [S(1,11,"Jesus Calls the First Disciples"), S(12,16,"Jesus Cleanses a Leper"), S(17,26,"Jesus Heals a Paralytic"), S(27,32,"The Calling of Levi"), S(33,39,"A Question About Fasting")],
    6:  [S(1,11,"Jesus Is Lord of the Sabbath"), S(12,16,"Jesus Chooses the Twelve"), S(17,26,"Blessings and Woes"), S(27,36,"Love Your Enemies"), S(37,42,"Judging Others"), S(43,49,"A Tree and Its Fruit")],
    7:  [S(1,10,"The Faith of the Centurion"), S(11,17,"Jesus Raises a Widow's Son"), S(18,35,"Messengers from John the Baptist"), S(36,50,"A Sinful Woman Forgiven")],
    8:  [S(1,3,"Women Accompanying Jesus"), S(4,15,"The Parable of the Sower"), S(16,18,"A Lamp Under a Jar"), S(19,21,"Jesus' Mother and Brothers"), S(22,25,"Jesus Calms a Storm"), S(26,39,"Jesus Heals the Gerasene Demoniac"), S(40,56,"A Girl Restored and a Woman Healed")],
    9:  [S(1,9,"Jesus Sends Out the Twelve"), S(10,17,"Jesus Feeds the Five Thousand"), S(18,27,"Peter Confesses Jesus as the Christ"), S(28,36,"The Transfiguration"), S(37,43,"Jesus Heals a Boy with a Demon"), S(44,50,"Jesus Again Foretells His Death"), S(51,62,"The Cost of Following Jesus")],
    10: [S(1,24,"Jesus Sends Out the Seventy-Two"), S(25,37,"The Parable of the Good Samaritan"), S(38,42,"Martha and Mary")],
    11: [S(1,13,"The Lord's Prayer"), S(14,28,"Jesus and Beelzebul"), S(29,36,"The Sign of Jonah"), S(37,54,"Woes to the Pharisees and Lawyers")],
    12: [S(1,12,"Beware of Hypocrisy"), S(13,21,"The Parable of the Rich Fool"), S(22,34,"Do Not Be Anxious"), S(35,48,"You Must Be Ready"), S(49,59,"Not Peace, but Division")],
    13: [S(1,9,"Repent or Perish"), S(10,17,"A Woman Healed on the Sabbath"), S(18,21,"The Mustard Seed and the Leaven"), S(22,30,"The Narrow Door"), S(31,35,"Lament over Jerusalem")],
    14: [S(1,6,"Jesus Heals on the Sabbath"), S(7,14,"The Places of Honor"), S(15,24,"The Parable of the Great Banquet"), S(25,35,"The Cost of Discipleship")],
    15: [S(1,7,"The Parable of the Lost Sheep"), S(8,10,"The Parable of the Lost Coin"), S(11,32,"The Parable of the Prodigal Son")],
    16: [S(1,13,"The Parable of the Dishonest Manager"), S(14,18,"The Law and the Kingdom"), S(19,31,"The Rich Man and Lazarus")],
    17: [S(1,10,"Temptations, Faith, and Duty"), S(11,19,"Jesus Cleanses Ten Lepers"), S(20,37,"The Coming of the Kingdom")],
    18: [S(1,8,"The Parable of the Persistent Widow"), S(9,14,"The Pharisee and the Tax Collector"), S(15,17,"Let the Children Come"), S(18,30,"The Rich Ruler"), S(31,34,"Jesus Foretells His Death"), S(35,43,"Jesus Heals a Blind Beggar")],
    19: [S(1,10,"Jesus and Zacchaeus"), S(11,27,"The Parable of the Ten Minas"), S(28,40,"The Triumphal Entry"), S(41,44,"Jesus Weeps over Jerusalem"), S(45,48,"Jesus Cleanses the Temple")],
    20: [S(1,8,"Jesus' Authority Questioned"), S(9,18,"The Parable of the Tenants"), S(19,26,"Paying Taxes to Caesar"), S(27,40,"The Resurrection and Marriage"), S(41,44,"Whose Son Is the Christ"), S(45,47,"Beware of the Scribes")],
    21: [S(1,4,"The Widow's Offering"), S(5,19,"Signs of the End of the Age"), S(20,24,"The Destruction of Jerusalem"), S(25,28,"The Coming of the Son of Man"), S(29,38,"The Lesson of the Fig Tree")],
    22: [S(1,6,"The Plot to Kill Jesus"), S(7,23,"The Passover and the Lord's Supper"), S(24,30,"A Dispute About Greatness"), S(31,38,"Peter's Denial Foretold"), S(39,46,"Jesus Prays on the Mount of Olives"), S(47,53,"The Betrayal and Arrest"), S(54,62,"Peter Denies Jesus"), S(63,71,"Jesus Before the Council")],
    23: [S(1,5,"Jesus Before Pilate"), S(6,12,"Jesus Before Herod"), S(13,25,"Pilate Delivers Jesus to Be Crucified"), S(26,43,"The Crucifixion"), S(44,49,"The Death of Jesus"), S(50,56,"The Burial of Jesus")],
    24: [S(1,12,"The Resurrection"), S(13,35,"On the Road to Emmaus"), S(36,49,"Jesus Appears to His Disciples"), S(50,53,"The Ascension")],
}

NEW_MAPS = {"40": MATTHEW, "41": MARK, "42": LUKE}

# True last-verse per chapter (from docs/assets/chapters/*.json) for end-of-chapter validation.
LAST_VERSE = {
    "40": {1:25,2:23,3:17,4:25,5:48,6:34,7:29,8:34,9:38,10:42,11:30,12:50,13:58,14:36,15:39,16:28,17:27,18:35,19:30,20:34,21:46,22:46,23:39,24:51,25:46,26:75,27:66,28:20},
    "41": {1:45,2:28,3:35,4:41,5:43,6:56,7:37,8:38,9:50,10:52,11:33,12:44,13:37,14:72,15:47,16:20},
    "42": {1:80,2:52,3:38,4:44,5:39,6:49,7:50,8:56,9:62,10:42,11:54,12:59,13:35,14:35,15:32,16:31,17:37,18:43,19:48,20:47,21:38,22:71,23:56,24:53},
}

def main():
    with open(MAP_PATH) as f:
        pmap = json.load(f)
    before_books = sum(1 for k in pmap if not k.startswith('_'))

    # Validate: section 1 starts at verse 1, sections are contiguous, last end = chapter end.
    problems = 0
    for bk, ch_map in NEW_MAPS.items():
        for ch, sections in ch_map.items():
            if sections[0]['start'] != 1:
                print(f"  ERR {bk} ch {ch}: first section does not start at v1"); problems += 1
            for i, s in enumerate(sections):
                if s['start'] > s['end']:
                    print(f"  ERR {bk} ch {ch} sec {i}: start>end"); problems += 1
                if i > 0 and s['start'] != sections[i-1]['end'] + 1:
                    print(f"  ERR {bk} ch {ch}: gap/overlap at sec {i}"); problems += 1
            true_last = LAST_VERSE.get(bk, {}).get(ch)
            if true_last and sections[-1]['end'] != true_last:
                print(f"  ERR {bk} ch {ch}: last end {sections[-1]['end']} != true {true_last}"); problems += 1
    if problems:
        raise SystemExit(f"{problems} validation problem(s) — fix before writing.")

    for bk, ch_map in NEW_MAPS.items():
        pmap.setdefault(bk, {})
        for ch, sections in ch_map.items():
            pmap[bk][str(ch)] = sections

    after_books = sum(1 for k in pmap if not k.startswith('_'))
    after_sections = sum(sum(len(pmap[k][c]) for c in pmap[k]) for k in pmap if not k.startswith('_'))
    print(f"Books: {before_books} -> {after_books}  (+{after_books - before_books})")
    print(f"Total sections now: {after_sections}")

    with open(MAP_PATH, "w") as f:
        json.dump(pmap, f, indent=2, ensure_ascii=False)
    print(f"Wrote {MAP_PATH}")

if __name__ == "__main__":
    main()
