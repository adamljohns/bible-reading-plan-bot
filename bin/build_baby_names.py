#!/usr/bin/env python3
"""build_baby_names.py — generate docs/dictionary/baby-names.html

Curated baby-name directory split off from the broader biblical-names
index. Three biblical sections (Boys / Girls / Unisex) + a Christian-
Tradition section (Charles, William, Catherine, Augustine, Theresa,
virtue names, etc.) for popular non-biblical-but-Christian names.

Each card shows:
  * Primary headword (linked to the dictionary entry when one exists)
  * Popularity (1-5 stars)
  * One-line meaning / origin
  * Common nicknames + language variants

Each card also embeds a hidden data-search attribute containing the
primary name, every variant, and the meaning — so a single search box
at the top of the page can find a card by typing any nickname (typing
"Susie" finds Susanna; typing "Pete" finds Peter).

Tuple format: (slug_or_name, meaning, variants, popularity_1_to_5)
  * slug_or_name: dictionary slug if entry exists, OR plain display name
    for info-only cards (Christian-tradition names without dict entries).
  * popularity: 1 = very rare, 2 = rare/historic, 3 = uncommon,
    4 = common, 5 = very common in modern use.
"""
import os
import re
import html as html_mod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(ROOT, 'docs', 'dictionary')
OUT = os.path.join(DICT_DIR, 'baby-names.html')

WORD_TITLE_PAT = re.compile(r'<div class="word-title">(.*?)</div>', re.DOTALL)
H1_TITLE_PAT = re.compile(r'<h1[^>]*class="[^"]*word-title[^"]*"[^>]*>(.*?)</h1>', re.DOTALL)
BARE_H1_PAT = re.compile(r'<body[^>]*>.*?<h1[^>]*>(.*?)</h1>', re.DOTALL)
TAG_STRIP = re.compile(r'<[^>]+>')


def get_headword(slug):
    """Look up the canonical headword from the dictionary HTML.
    Returns None if the slug has no dictionary entry."""
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        return None
    with open(fp, 'r', encoding='utf-8') as f:
        h = f.read()
    for pat in (WORD_TITLE_PAT, H1_TITLE_PAT, BARE_H1_PAT):
        m = pat.search(h)
        if m:
            t = TAG_STRIP.sub('', m.group(1))
            t = t.replace('&mdash;', '—').replace('&amp;', '&').replace('&#39;', "'")
            t = re.sub(r'\s+', ' ', t).strip()
            t = re.sub(r'\s*\([^)]*\)\s*$', '', t)
            return t
    return None


# =========================================================================
#                          BIBLICAL — BOYS
# =========================================================================
MALE = [
    # Patriarchs
    ('adam',            'man, earth; the first human',
                        ['Adamo', 'Adan', 'Adi'], 4),
    ('abel',            'breath, vapor; the first martyr (Gen 4)',
                        ['Abe'], 3),
    ('seth-son',        'appointed; son of Adam after Abel',
                        ['Sett'], 3),
    ('enoch',           'dedicated; walked with God, was not (Gen 5:24)',
                        ['Hanoch', 'Enok'], 3),
    ('noah',            'rest; the ark-builder',
                        ['Noé', 'Noach'], 5),
    ('abraham',         'father of many nations; the friend of God',
                        ['Abe', 'Avi', 'Avram', 'Bram', 'Ibrahim'], 4),
    ('isaac',           'laughter; son of promise to Abraham',
                        ['Ike', 'Izaak', 'Yitzhak', 'Isak'], 5),
    ('jacob',           'supplanter; renamed Israel; the patriarch',
                        ['Jake', 'Jakob', 'Yakov', 'Iago', 'Diego', 'Jago'], 5),
    # Twelve tribe sons of Jacob
    ('reuben',          'see, a son! (Gen 29:32); Jacob\'s firstborn',
                        ['Reuven', 'Rueben', 'Ruben'], 3),
    ('simeon',          'hearing (Gen 29:33); Jacob\'s second son',
                        ['Simon', 'Shimon', 'Sim'], 3),
    ('levi-son',        'joined (Gen 29:34); ancestor of the priestly tribe',
                        ['Lev', 'Levy', 'Levi'], 5),
    ('judah',           'praised; the tribe through which Messiah came',
                        ['Jude', 'Judas', 'Yehuda'], 4),
    ('dan-tribe',       'judge (Gen 30:6); son of Jacob and Bilhah',
                        ['Dann'], 4),
    ('naphtali',        'my wrestling (Gen 30:8); tribe of Galilee',
                        ['Naftali'], 2),
    ('gad',             'fortune / a troop cometh (Gen 30:11); warrior tribe',
                        [], 2),
    ('asher',           'happy / blessed (Gen 30:13); coastal tribe',
                        ['Ash'], 5),
    ('issachar',        'there is reward (Gen 30:18); tribe of \'understanding the times\'',
                        ['Issa'], 2),
    ('zebulun',         'dwelling / honor (Gen 30:20); maritime-trade Galilean tribe',
                        ['Zebulon', 'Zeb'], 2),
    ('joseph-figure',   'he will add; the dreamer-savior of Egypt',
                        ['Joe', 'Joey', 'Yosef', 'Yousef', 'Yusuf', 'Pepe', 'Giuseppe', 'José'], 5),
    ('benjamin',        'son of the right hand (Gen 35:18); tribe of Saul and Paul',
                        ['Ben', 'Benny', 'Benji', 'Bennett'], 5),
    ('ephraim',         'fruitful (Gen 41:52); Joseph\'s younger son',
                        ['Efraim', 'Efrem', 'Efren'], 3),
    # Other OT figures
    ('moses',           'drawn out; the lawgiver and deliverer',
                        ['Moshe', 'Mose', 'Musa'], 3),
    ('aaron',           'mountain of strength; the first high priest',
                        ['Aron', 'Ari', 'Aharon'], 4),
    ('caleb-doctrine',  'whole-hearted; one of two faithful spies',
                        ['Cale', 'Kaleb', 'Kayleb'], 5),
    ('joshua-figure',   'Yahweh is salvation; led Israel into the land',
                        ['Josh', 'Yeshua', 'Jeshua', 'Hoshea', 'Joshuah'], 5),
    ('gideon',          'mighty warrior; judge of three hundred',
                        ['Gid', 'Gidi'], 3),
    ('samson',          'sun, brightness; the long-haired Nazirite judge',
                        ['Sam', 'Shimshon'], 3),
    ('boaz-doctrine',   'swift, strong; kinsman-redeemer of Ruth',
                        ['Boz'], 3),
    ('samuel',          'heard by God; last judge, first prophet of kings',
                        ['Sam', 'Sammy', 'Shmuel'], 5),
    ('saul',            'asked of God; the first king of Israel',
                        ['Shaul', 'Sol'], 3),
    ('david',           'beloved; king after God\'s own heart',
                        ['Dave', 'Davy', 'Davis', 'Davide', 'Dawid', 'Dovid'], 5),
    ('solomon',         'peace; David\'s wise son; temple-builder',
                        ['Sol', 'Solly', 'Salomon', 'Salman', 'Shlomo', 'Suleyman'], 3),
    ('elijah',          'my God is Yahweh; great prophet of Mount Carmel',
                        ['Eli', 'Elias', 'Elia', 'Ilya'], 5),
    ('elisha',          'God is salvation; successor of Elijah',
                        ['Elish', 'Elisée'], 3),
    ('hezekiah',        'Yahweh strengthens; reforming king of Judah',
                        ['Hez', 'Heskiah', 'Chizkiyahu'], 3),
    ('josiah',          'the LORD heals; the boy-king of reform',
                        ['Josias', 'Josi'], 4),
    ('asa-king',        'physician / healer; reforming king of Judah',
                        [], 2),
    ('uzziah-king',     'my strength is Yahweh; king of Judah',
                        ['Azariah'], 2),
    ('rehoboam',        'enlarger of the people; Solomon\'s son',
                        ['Roboam'], 1),
    ('manasseh-king',   'making to forget; the wicked-then-repentant king of Judah',
                        ['Menasseh', 'Manasses'], 2),
    ('phinehas',        'mouth of brass; Aaron\'s zealous grandson (Num 25)',
                        ['Pinchas', 'Phineas'], 2),
    # Writing prophets
    ('isaiah',          'the LORD is salvation; the messianic prophet',
                        ['Isiah', 'Izzy', 'Yeshayahu', 'Esaias', 'Isaias'], 5),
    ('jeremiah',        'the LORD exalts; the weeping prophet',
                        ['Jerry', 'Jem', 'Yirmeyahu', 'Jeremias'], 4),
    ('ezekiel',         'God will strengthen; the prophet of the exile',
                        ['Zeke', 'Ezekial', 'Yechezkel'], 4),
    ('daniel',          'God is my judge; the prophet in exile',
                        ['Dan', 'Danny', 'Dani'], 5),
    ('hosea',           'salvation; prophet of God\'s covenant love',
                        ['Hoshea', 'Oshea', 'Osee'], 2),
    ('joel-prophet',    'Yahweh is God; prophet of the day of the LORD',
                        ['Yoel'], 3),
    ('amos-prophet',    'burden-bearer; prophet of justice',
                        [], 3),
    ('obadiah',         'servant of Yahweh; shortest OT book',
                        ['Obadias'], 2),
    ('jonah',           'dove; the reluctant prophet',
                        ['Jonas', 'Yonah', 'Yunus'], 4),
    ('micah',           'who is like God; the prophet of Bethlehem',
                        ['Micaiah', 'Mica', 'Mika'], 4),
    ('nahum',           'comforter; prophet of Nineveh\'s fall',
                        ['Naum'], 1),
    ('habakkuk',        'embrace; prophet of \'the just shall live by faith\'',
                        ['Habacuc'], 1),
    ('zephaniah',       'Yahweh hides; prophet of the coming day',
                        ['Tzefania'], 1),
    ('haggai',          'festal; prophet of the second-temple build',
                        ['Aggeus'], 1),
    ('zechariah',       'Yahweh remembers; prophet of post-exile vision',
                        ['Zach', 'Zac', 'Zacharias'], 4),
    ('malachi',         'my messenger; last prophet of the OT',
                        ['Mal', 'Malakai'], 4),
    ('ezra',            'help; the priest-scribe of the return',
                        ['Esdras', 'Ezri'], 5),
    ('nehemiah',        'the LORD comforts; wall-builder of Jerusalem',
                        ['Neh', 'Nechemiah'], 3),
    ('mordecai',        'devoted to Marduk; Esther\'s cousin and guardian',
                        ['Mort', 'Modi'], 2),
    # NT figures
    ('zacharias-prophet', 'Yahweh remembers; father of John the Baptist',
                        ['Zach', 'Zachary', 'Zac', 'Zak', 'Zachariah'], 4),
    ('john-the-baptist', 'Yahweh is gracious; the forerunner of Christ',
                        ['Jack', 'Johnny', 'Sean', 'Ian', 'Evan', 'Juan', 'Hans', 'Ivan', 'Giovanni', 'Jonas', 'João', 'Yohanan'], 5),
    ('andrew',          'manly, courageous; brought Peter to Jesus',
                        ['Andy', 'Drew', 'Andre', 'Anders', 'Andreas', 'Anderson'], 5),
    ('peter',           'rock; chief apostle, fisherman',
                        ['Pete', 'Petros', 'Pedro', 'Pierre', 'Pyotr', 'Cephas', 'Piotr'], 4),
    ('james-apostle',   'supplanter (Greek for Jacob); apostle and brother of John',
                        ['Jim', 'Jimmy', 'Jamie', 'Jaime', 'Iago', 'Diego', 'Santiago'], 5),
    ('philip',          'lover of horses; apostle and evangelist',
                        ['Phil', 'Felipe', 'Filippo', 'Philippos', 'Phillip'], 3),
    ('nathanael',       'gift of God; \'in whom is no guile\' (John 1:47)',
                        ['Nat', 'Natty', 'Nathaniel', 'Nathan'], 4),
    ('matthew-apostle', 'gift of God; tax collector turned apostle',
                        ['Matt', 'Matty', 'Mateo', 'Matias', 'Mathieu', 'Matthias'], 5),
    ('thomas',          'twin; the doubting-then-believing apostle',
                        ['Tom', 'Tommy', 'Thom', 'Tomás', 'Tomasso', 'Toma'], 5),
    ('mark-book',       'warrior (Latin); the second evangelist',
                        ['Marc', 'Marcus', 'Markos', 'Marko', 'Marcos'], 4),
    ('luke',            'light; physician and evangelist',
                        ['Lucas', 'Lukas', 'Loukas', 'Luca', 'Luc'], 5),
    ('paul',            'small; apostle to the Gentiles',
                        ['Paolo', 'Pablo', 'Pasha', 'Pavel', 'Paulo'], 4),
    ('barnabas-doctrine', 'son of encouragement; companion of Paul',
                        ['Barney', 'Barnaby'], 2),
    ('silas',           'woods, forest; Paul\'s missionary companion',
                        ['Silvanus', 'Cy'], 4),
    ('timothy',         'honored by God; Paul\'s son in the faith',
                        ['Tim', 'Timmy', 'Timotheus', 'Timoteo'], 4),
    ('titus-doctrine',  'honored; Paul\'s Gentile companion',
                        ['Tito'], 3),
    ('apollos',         'destroyer; eloquent Alexandrian Christian (Acts 18-19)',
                        [], 1),
    ('jude',            'praise (same root as Judah); author of Jude',
                        ['Judah', 'Judas', 'Yehuda'], 4),
    ('philemon',        'affectionate; addressee of Paul\'s letter',
                        [], 1),
    ('onesimus',        'profitable; the runaway slave restored by Paul\'s letter',
                        [], 1),
    ('epaphras',        'lovely; servant of the Colossian church (Col 1:7)',
                        [], 1),
    ('epaphroditus',    'lovely / charming; Philippian messenger to Paul (Phil 2:25)',
                        ['Aphro'], 1),
    ('tychicus',        'fortunate; Paul\'s trusted letter-carrier',
                        [], 1),
    ('aristarchus',     'best ruler; companion of Paul in Macedonia and Rome',
                        [], 1),
    ('crispus',         'curly-haired; synagogue ruler at Corinth converted by Paul',
                        [], 1),
    ('trophimus',       'nourishing; Ephesian companion of Paul',
                        [], 1),
    ('sosthenes',       'safe in strength; ruler of synagogue at Corinth',
                        [], 1),
    ('tertius',         'third (Latin); scribe of Romans (Rom 16:22)',
                        [], 1),
    ('agabus',          'locust; prophet who foretold famine and Paul\'s arrest',
                        [], 1),
    ('stephen',         'crown; the first Christian martyr',
                        ['Steve', 'Stefan', 'Stephan', 'Esteban', 'Etienne', 'Stefano', 'Stevie'], 4),
    ('cornelius-the-centurion', 'horn (Latin); first Gentile baptized into the church (Acts 10)',
                        ['Corny', 'Cornel', 'Corneliu'], 3),
    ('gabriel',         'man of God; the announcing angel',
                        ['Gabe', 'Gabby', 'Gavriel', 'Gabriele'], 5),
    # Obscure / biblical-faith-line additions (batch 110)
    ('shem',            'name, renown; eldest son of Noah; patriarch of the covenant line',
                        ['Sem'], 1),
    ('eber',            'the other side; great-grandson of Shem; root of the word "Hebrew"',
                        ['Heber', 'Ever'], 1),
    ('eliezer',         '"my God is help"; Abraham\'s trusted servant (Gen 15:2); Moses\'s second son',
                        ['Lazar', 'Lazaro', 'Eli'], 3),
    ('jubal',           '"stream" or "ram\'s-horn"; son of Lamech; originator of instrumental music (Gen 4:21)',
                        [], 1),
    ('jabal',           '"river" or "to lead"; eldest son of Lamech; originator of nomadic pastoralism (Gen 4:20)',
                        [], 1),
    ('cleopas',         '"glory of the father"; Emmaus-road disciple to whom the risen Christ appeared (Luke 24)',
                        [], 1),
    ('abijah-king',     '"my father is Yahweh"; the third king of Judah; also the priestly course of Zacharias (Luke 1:5)',
                        ['Abia', 'Aviya'], 2),
    # Editor's family
    ('malachi-andrew',  'memorial — Adam & Maria\'s first child (2017)',
                        [], 2),
]

# =========================================================================
#                          BIBLICAL — GIRLS
# =========================================================================
FEMALE = [
    ('sarah',           'princess; Abraham\'s wife; mother of nations',
                        ['Sara', 'Sally', 'Sarai', 'Zara'], 5),
    ('hagar',           'flight, stranger; Egyptian handmaid; mother of Ishmael',
                        ['Hajar'], 1),
    ('rebekah',         'to bind; Isaac\'s wife; mother of Jacob and Esau',
                        ['Rebecca', 'Becky', 'Becca', 'Reba', 'Beck'], 4),
    ('leah',            'weary; Jacob\'s first wife; mother of Judah',
                        ['Lea', 'Lia', 'Lee', 'Léa'], 5),
    ('rachel',          'ewe; Jacob\'s beloved wife; mother of Joseph and Benjamin',
                        ['Rae', 'Raquel', 'Rachelle', 'Rakel', 'Rahel'], 4),
    ('miriam',          'bitter; prophetess, sister of Moses and Aaron',
                        ['Mariam', 'Mira', 'Miri'], 3),
    ('asenath',         'gift of the sun-god (Egyptian); wife of Joseph',
                        ['Aseneth'], 1),
    ('rahab',           'broad / wide; the Jericho harlot in Christ\'s line',
                        ['Rachab'], 2),
    ('deborah',         'bee; prophetess and judge',
                        ['Deb', 'Debbie', 'Debby', 'Devorah'], 3),
    ('jael',            'mountain goat; the tent-peg woman of Judges 4',
                        ['Yael', 'Jaella'], 2),
    ('naomi',           'pleasant; Ruth\'s mother-in-law',
                        ['Nomi', 'Noemi', 'Noémie'], 5),
    ('ruth',            'companion, friend; Moabite great-grandmother of David',
                        ['Ruthie'], 4),
    ('hannah',          'grace; the long-barren mother of Samuel',
                        ['Hanna', 'Hana', 'Anna', 'Anne', 'Ann', 'Annie'], 5),
    ('abigail',         'father is joy; David\'s wife of wisdom',
                        ['Abby', 'Abbie', 'Gail', 'Abi'], 5),
    ('bathsheba',       'daughter of the oath; mother of Solomon',
                        ['Sheba'], 1),
    ('tamar',           'palm tree; mother in the line of Christ (Matt 1:3)',
                        ['Tamara', 'Tammy'], 3),
    ('huldah-prophetess', 'weasel; prophetess of Josiah\'s reform (2 Kings 22)',
                        ['Hulda'], 1),
    ('hadassah',        'myrtle tree; the Hebrew (covenant) name of Queen Esther (Esth 2:7)',
                        ['Hadasa', 'Hadas'], 4),
    ('jemima',          'dove; first of Job\'s three restored daughters (Job 42:14)',
                        ['Jemimah', 'Yemima', 'Mimi'], 3),
    ('keziah',          'cassia (priestly anointing-spice); second of Job\'s restored daughters',
                        ['Kezia', 'Kessie', 'Ketziah'], 3),
    ('vashti',          'beautiful; the queen Ahasuerus deposed before Esther',
                        ['Vasht'], 2),
    ('esther',          'star; queen who saved her people',
                        ['Hadassah', 'Essie', 'Hettie', 'Estee', 'Ester'], 4),
    ('elisabeth-mother-of-john', 'God is my oath; mother of John the Baptist',
                        ['Liz', 'Beth', 'Betsy', 'Eliza', 'Lisbeth', 'Elsa', 'Elise', 'Lisa', 'Bess', 'Lizzie', 'Elspeth'], 5),
    ('mary',            'bitter, beloved; mother of Christ',
                        ['Maria', 'Marie', 'Maryam', 'Molly', 'Polly', 'Mae', 'May', 'Mariah'], 4),
    ('anna-the-prophetess', 'grace; temple-prophetess at Christ\'s presentation',
                        ['Anne', 'Ann', 'Annie', 'Anya', 'Anita'], 5),
    ('martha',          'lady, mistress; sister of Mary and Lazarus',
                        ['Marta', 'Marty', 'Mattie', 'Marthe'], 3),
    ('mary-magdalene',  'of Magdala; first witness of the resurrection',
                        ['Maggie', 'Madeline', 'Madeleine', 'Magda', 'Magdalena'], 4),
    ('salome',          'peace; mother of James and John; at the resurrection',
                        ['Sal', 'Salma'], 2),
    ('joanna',          'Yahweh is gracious; faithful woman at the resurrection',
                        ['Jo', 'Joan', 'Joanne', 'Johanna', 'Jana'], 3),
    ('tabitha',         'gazelle (Hebrew); raised by Peter (Acts 9:36-42)',
                        ['Tabby', 'Dorcas'], 3),
    ('dorcas',          'gazelle (Greek for Tabitha); same disciple raised by Peter',
                        ['Tabitha'], 2),
    ('lydia',           'woman from Lydia; first European convert (Acts 16)',
                        ['Liddy', 'Lyddie', 'Lydie'], 4),
    ('phoebe',          'radiant; deacon of Cenchrea (Rom 16:1)',
                        ['Phebe'], 4),
    ('priscilla',       'ancient; co-worker with Paul (with husband Aquila)',
                        ['Prisca', 'Cilla', 'Priscille'], 3),
    ('rhoda',           'rose; the maid who knew Peter\'s voice (Acts 12)',
                        ['Rhody'], 2),
    ('lois',            'unfeigned-faith grandmother of Timothy (2 Tim 1:5)',
                        ['Lo'], 3),
    ('eunice',          'good victory; believing Jewish mother of Timothy',
                        ['Uni'], 3),
    ('chloe',           'green sprout; Christian woman who reported Corinthian divisions to Paul',
                        ['Clo', 'Khloe', 'Cloe'], 5),
    ('damaris',         'gentle; convert at Athens through Paul\'s Mars\' Hill sermon',
                        ['Mara'], 2),
    ('susanna',         'lily; supporter of Christ\'s Galilean ministry (Luke 8:3)',
                        ['Susan', 'Sue', 'Susie', 'Suzy', 'Suzanne', 'Shoshana', 'Susannah'], 3),
    ('claudia',         'noble Roman gens; Christian woman in Paul\'s final epistle',
                        ['Claudette', 'Claudine'], 3),
    ('julia',           'noble Roman gens; Christian woman in Paul\'s greeting (Rom 16:15)',
                        ['Julie', 'Juliet', 'Juliana', 'Yulia', 'Giulia'], 5),
    ('eve',             'life-giver; the first woman, mother of all living',
                        ['Eva', 'Evie', 'Eveline', 'Chava'], 5),
    ('bethany',         'house of figs; the village of Lazarus, Mary, Martha',
                        ['Beth', 'Bethy'], 3),
    # Editor's family
    ('maria',           'the Latin form of Mary; the editor\'s wife — bitter made sweet',
                        ['Mary', 'Marie', 'Mariana'], 5),
    ('hope-twin',       'memorial — Adam & Maria\'s twin daughter (2018)',
                        [], 2),
    ('mercy-twin',      'memorial — Adam & Maria\'s twin daughter (2018)',
                        [], 2),
]

# =========================================================================
#                          BIBLICAL — UNISEX
# =========================================================================
UNISEX = [
    ('shiloh-doctrine', 'he whose right it is (Gen 49:10); Messianic title + place; modern unisex',
                        [], 3),
    ('jordan-river',    'descend, flow down; the river of baptism; modern unisex',
                        ['Jordy', 'Jordana'], 4),
    ('eden',            'delight, pleasure; the garden of original creation',
                        ['Edie', 'Edyn'], 4),
    ('carmel',          'vineyard, garden; mountain where Elijah called down fire',
                        ['Carmela', 'Carmen'], 3),
    ('zion',            'fortification; God\'s holy hill; modern unisex',
                        ['Zionie'], 3),
    ('tamar',           'palm tree; primarily female but used both in modern use',
                        ['Tamara'], 3),
    ('hannah',          'grace; primarily female but rare male use in some traditions',
                        ['Hanna'], 2),
]

# =========================================================================
#                      CHRISTIAN TRADITION — BOYS
#  (Most have no dictionary entry yet — info-only cards. A few link to
#   the dict where the figure already has an entry.)
# =========================================================================
CHRISTIAN_MALE = [
    # Virtue / theological-concept names (used as boys' names rarely)
    ('Theodore',        'Greek <em>Theodōros</em> — \"God\'s gift\"; many early-church saints; biblical Theophilus shares root',
                        ['Theo', 'Ted', 'Teddy', 'Fyodor', 'Tudor'], 5),
    ('Christopher',     'Greek <em>Christophoros</em> — \"Christ-bearer\"; legendary 3rd-century saint',
                        ['Chris', 'Topher', 'Kit', 'Christo', 'Cristóbal'], 5),
    ('Charles',         'Germanic <em>karl</em> — \"free man\"; Charlemagne, Charles Spurgeon, Charles Wesley',
                        ['Charlie', 'Chas', 'Carlos', 'Karl', 'Carl', 'Cary'], 4),
    ('William',         'Germanic <em>Wilhelm</em> — \"resolute protector\"; William Tyndale, William Carey, William of Orange',
                        ['Will', 'Willy', 'Billy', 'Bill', 'Liam', 'Guillermo', 'Wilhelm', 'Guillaume'], 5),
    ('Henry',           'Germanic <em>Heimric</em> — \"estate ruler\"; many English Christian kings',
                        ['Hank', 'Harry', 'Hal', 'Heinrich', 'Enrique', 'Henri', 'Enrico'], 5),
    ('Edward',          'Old English <em>Eadweard</em> — \"rich guard\"; Edward the Confessor (saint-king)',
                        ['Ed', 'Eddie', 'Ted', 'Teddy', 'Eduardo', 'Edouard'], 3),
    ('George',          'Greek <em>Geōrgios</em> — \"farmer, earth-worker\"; St. George (dragon-slayer); George Whitefield, George Müller',
                        ['Georgie', 'Jorge', 'Giorgio', 'Yuri', 'Jürgen'], 4),
    ('Patrick',         'Latin <em>Patricius</em> — \"noble\"; Patrick of Ireland (5th-century missionary)',
                        ['Pat', 'Paddy', 'Patricio', 'Patrik'], 3),
    ('Francis',         'Latin <em>Franciscus</em> — \"Frenchman\"; Francis of Assisi; Francis Schaeffer',
                        ['Frank', 'Frankie', 'Francesco', 'Francisco', 'François'], 3),
    ('Anthony',         'Latin <em>Antonius</em> — Roman gens, possibly \"priceless\"; Anthony the Great (desert father)',
                        ['Tony', 'Antoine', 'Antonio', 'Anton'], 5),
    ('Vincent',         'Latin <em>Vincens</em> — \"conquering\"; Vincent de Paul; Vincent of Lérins',
                        ['Vince', 'Vinny', 'Vincenzo', 'Vicente'], 4),
    ('Gregory',         'Greek <em>Grēgorios</em> — \"watchful\"; Gregory the Great; Gregory of Nazianzus; Gregory of Nyssa',
                        ['Greg', 'Gregor', 'Grigorii', 'Gregorio'], 3),
    ('Augustine',       'Latin <em>Augustinus</em> — \"venerable\"; Augustine of Hippo (354-430); Augustine of Canterbury',
                        ['Gus', 'Augustin', 'Agustín'], 2),
    ('Benedict',        'Latin <em>Benedictus</em> — \"blessed\"; Benedict of Nursia (founder of Western monasticism)',
                        ['Ben', 'Benny', 'Bennett', 'Benedikt'], 2),
    ('Bernard',         'Germanic <em>Bernhard</em> — \"brave as a bear\"; Bernard of Clairvaux (12th-century mystic)',
                        ['Bernie', 'Bernardo', 'Barney'], 2),
    ('Calvin',           'Latin <em>Calvinus</em> — \"bald\"; John Calvin (Reformer, 1509-1564)',
                        ['Cal', 'Cale', 'Kelvin'], 4),
    ('Martin',          'Latin <em>Martinus</em> — \"of Mars\"; Martin of Tours; Martin Luther (Reformer)',
                        ['Marty', 'Martino', 'Martín'], 4),
    ('Justin',          'Latin <em>Justus</em> — \"just, righteous\"; Justin Martyr (2nd-century apologist)',
                        ['Justus', 'Justino'], 4),
    ('Anselm',          'Germanic — \"helmet of God\"; Anselm of Canterbury (ontological argument)',
                        ['Ansel', 'Anselmo'], 1),
    ('Ambrose',         'Greek <em>Ambrosios</em> — \"immortal\"; Ambrose of Milan (mentor of Augustine)',
                        ['Amby', 'Ambrosio'], 2),
    ('Jerome',          'Greek <em>Hieronymos</em> — \"sacred name\"; Jerome (Vulgate translator)',
                        ['Jerry', 'Geronimo', 'Gerome', 'Hieronymus'], 2),
    ('Cyril',           'Greek <em>Kyrillos</em> — \"lordly\"; Cyril of Jerusalem; Cyril of Alexandria',
                        ['Kiril', 'Cirilo'], 1),
    ('Athanasius',      'Greek <em>Athanasios</em> — \"immortal\"; Athanasius the Great (defender of Nicaea)',
                        ['Athan'], 1),
    ('Polycarp',        'Greek <em>Polykarpos</em> — \"much fruit\"; bishop of Smyrna, disciple of John the Apostle, martyred AD 155',
                        [], 1),
    ('Ignatius',        'Latin <em>Ignatius</em> — \"fiery\"; Ignatius of Antioch (early-church martyr)',
                        ['Iggy', 'Ignacio'], 2),
    ('Eusebius',        'Greek <em>Eusebios</em> — \"pious\"; Eusebius of Caesarea (church historian)',
                        [], 1),
    ('Origen',          'Greek <em>Origenes</em> — \"born of mountains\"; great-but-controversial 3rd-century theologian',
                        [], 1),
    ('Wesley',          'Old English — \"western meadow\"; John & Charles Wesley (founders of Methodism)',
                        ['Wes'], 4),
    ('Spurgeon',        'Old English (surname) — \"sparrow town\"; Charles Spurgeon (Prince of Preachers, 1834-1892)',
                        ['Spurge'], 1),
    ('Edwards',         'Surname — \"son of Edward\"; Jonathan Edwards (the Great Awakening preacher-theologian)',
                        [], 2),
    ('Whitefield',      'Surname — \"white field\"; George Whitefield (Great Awakening evangelist)',
                        [], 1),
    ('Tyndale',         'Surname — \"valley of the Tyne\"; William Tyndale (English Bible translator, martyred 1536)',
                        [], 1),
    ('Knox',            'Surname — \"round hill\"; John Knox (Scottish Reformer)',
                        [], 4),
    # Other common Christian boy names
    ('Michael',         'Hebrew <em>Mikha\'el</em> — \"who is like God?\"; the archangel (Dan 10:13; Jude 9; Rev 12:7)',
                        ['Mike', 'Mick', 'Mikey', 'Mikhail', 'Miguel', 'Michel'], 5),
    ('Stephen',         'Greek <em>Stephanos</em> — \"crown\"; the first Christian martyr (Acts 7) and a Christian classic',
                        ['Steve', 'Stefan', 'Esteban'], 5),
    ('Lawrence',        'Latin <em>Laurentius</em> — \"from Laurentum\"; Lawrence of Rome (3rd-century martyr)',
                        ['Larry', 'Lance', 'Lorenzo', 'Laurent'], 3),
    ('Sebastian',       'Greek — \"from Sebaste\"; Sebastian of Milan (early-church martyr)',
                        ['Seb', 'Bastien', 'Sebastián'], 5),
    ('Dominic',         'Latin <em>Dominicus</em> — \"belonging to the Lord\"; Dominic de Guzmán (founder of Dominicans)',
                        ['Dom', 'Dominik', 'Doménico'], 4),
    ('Maximilian',      'Latin — \"greatest\"; many emperors and saints; Maximilian Kolbe (20th-c martyr)',
                        ['Max', 'Maxim', 'Maximilien'], 3),
    ('Adrian',          'Latin <em>Hadrianus</em> — \"from Hadria\"; Pope Adrian; many saints',
                        ['Ade', 'Adrien'], 4),
    ('Damon',           'Greek — \"loyal one\"; Damon (legend of friendship with Pythias); used by Christian families',
                        [], 3),
    ('Owen',            'Welsh <em>Owain</em> — \"young warrior\"; many Welsh saints',
                        ['Eoin', 'Evan-related'], 5),
    ('Liam',            'Irish form of William — \"resolute protector\"',
                        ['William-related'], 5),
    ('Ezra',            '(see Biblical Boys) — popular modern Christian name',
                        [], 0),  # 0 = duplicate, skip rendering
]

# =========================================================================
#                      CHRISTIAN TRADITION — GIRLS
# =========================================================================
CHRISTIAN_FEMALE = [
    # Christian-saint female names
    ('Catherine',       'Greek <em>Aikaterinē</em> — \"pure\"; Catherine of Siena, Catherine of Alexandria',
                        ['Cathy', 'Cate', 'Cat', 'Kate', 'Katie', 'Katy', 'Kathryn', 'Caterina', 'Catalina', 'Karen'], 4),
    ('Margaret',        'Greek <em>Margaritēs</em> — \"pearl\"; many saints; the pearl of great price (Matt 13:46) echo',
                        ['Maggie', 'Meg', 'Megan', 'Margot', 'Margarita', 'Margie', 'Peggy'], 4),
    ('Theresa',         'Greek — \"harvester\" or \"summer\"; Teresa of Avila, Thérèse of Lisieux, Mother Teresa',
                        ['Terry', 'Tess', 'Teresa', 'Reese', 'Tracy'], 4),
    ('Cecilia',         'Latin — possibly \"blind\"; Cecilia of Rome (patron of music, early-church martyr)',
                        ['Cee', 'Celia', 'Sissy', 'Cécile', 'Cecily'], 4),
    ('Agnes',           'Greek <em>hagne</em> — \"chaste, pure\"; Agnes of Rome (early-church virgin martyr)',
                        ['Aggie', 'Inés', 'Agnese'], 2),
    ('Lucy',            'Latin <em>Lux</em> — \"light\"; Lucia of Syracuse (early-church martyr)',
                        ['Lucia', 'Lucille', 'Lucinda', 'Lulu'], 5),
    ('Anastasia',       'Greek <em>Anastasis</em> — \"resurrection\"; Anastasia of Sirmium (early martyr)',
                        ['Anya', 'Stasia', 'Stacey', 'Stacy'], 3),
    ('Beatrice',        'Latin <em>Beatrix</em> — \"she who brings happiness\"; Dante\'s Beatrice; many saints',
                        ['Bea', 'Bee', 'Beatrix', 'Trixie'], 4),
    ('Theodora',        'Greek <em>Theodōra</em> — \"God\'s gift\" (feminine of Theodore)',
                        ['Thea', 'Dora', 'Teddi'], 3),
    ('Bridget',         'Irish <em>Brigid</em> — \"high\"; Brigid of Kildare (Irish saint)',
                        ['Brigid', 'Bree', 'Bridie', 'Brigitte'], 3),
    ('Helena',          'Greek <em>Helenē</em> — \"light\" or \"shining one\"; Helena mother of Constantine; many saints',
                        ['Helen', 'Ellen', 'Nellie', 'Lena', 'Elena', 'Helle'], 4),
    ('Monica',          'Latin (uncertain) — possibly \"to advise\"; Monica mother of Augustine',
                        ['Mona', 'Moni'], 3),
    ('Veronica',        'Latin / Greek — \"true image\"; tradition of veronica\'s veil at the cross',
                        ['Vero', 'Ronnie', 'Roni', 'Vera'], 3),
    ('Felicity',        'Latin <em>Felicitas</em> — \"happiness, good fortune\"; Felicity of Rome (martyr with Perpetua)',
                        ['Felix-related', 'Felicia'], 3),
    ('Perpetua',        'Latin — \"everlasting\"; Perpetua of Carthage (3rd-century martyr, with Felicity)',
                        [], 1),
    ('Constance',       'Latin <em>Constantia</em> — \"steadfastness\"; many Christian queens and saints',
                        ['Connie', 'Constanze', 'Costanza'], 2),
    ('Christina',       'Greek — \"follower of Christ, anointed\"; many saints',
                        ['Tina', 'Chrissy', 'Christine', 'Kristina', 'Cristina'], 4),
    ('Joan',            'Feminine of John — \"Yahweh is gracious\"; Joan of Arc; classic Christian name',
                        ['Joanie', 'Jane', 'Janet', 'Jeanne', 'Juana'], 3),
    ('Brigida',         'Latin form of Bridget; many saints',
                        ['Birgit'], 1),
    ('Hilda',           'Germanic <em>Hild</em> — \"battle\"; Hilda of Whitby (English abbess)',
                        ['Hildegard'], 2),
    ('Clare',           'Latin <em>Clara</em> — \"clear, bright\"; Clare of Assisi (friend of Francis)',
                        ['Clara', 'Claire', 'Clarissa'], 4),
    ('Cecily',          'Variant of Cecilia',
                        ['Sissy'], 3),
    ('Genevieve',       'Germanic — \"woman of the tribe\"; Genevieve of Paris (patron of Paris)',
                        ['Gen', 'Jenny', 'Gina'], 4),
    ('Augusta',         'Feminine of Augustus / Augustine — \"venerable, majestic\"',
                        ['Gus-related', 'Auggie'], 2),
    ('Antonia',         'Feminine of Anthony',
                        ['Toni', 'Tonia', 'Antonella'], 3),
    # Christian-virtue (Puritan) names
    ('Faith',           'English virtue name — confident trust in God (Heb 11)',
                        [], 5),
    ('Hope',            'English virtue name — confident expectation of God\'s promise (Rom 8:24)',
                        [], 4),
    ('Charity',         'Latin <em>caritas</em> — \"love\"; the greatest of the three (1 Cor 13:13)',
                        [], 2),
    ('Grace',           'Latin <em>gratia</em> — \"favor\"; the gospel virtue itself',
                        ['Gracie', 'Grazia'], 5),
    ('Joy',             'English virtue name — fruit of the Spirit (Gal 5:22)',
                        [], 4),
    ('Patience',        'Latin <em>patientia</em> — \"endurance\"; fruit of the Spirit',
                        [], 2),
    ('Prudence',        'Latin <em>prudentia</em> — \"wisdom in conduct\"',
                        ['Pru'], 1),
    ('Verity',          'Latin <em>veritas</em> — \"truth\"',
                        [], 1),
    ('Felicity',        'Latin — \"happiness\" (see also early-martyr entry above)',
                        [], 3),
    ('Honor',           'Latin — \"esteem, dignity\"; English virtue name',
                        ['Honora'], 2),
    ('Trinity',         'Latin <em>trinitas</em> — \"three-in-one\"; modern Christian name honoring the Triune God',
                        ['Trini'], 4),
    ('Glory',           'English virtue name — the kingly weight of God (Hebrew <em>kabod</em>)',
                        [], 1),
    ('Mercy',           'English virtue name — covenant lovingkindness (see Mercy (Twin) for editor\'s family memorial)',
                        [], 2),
    ('Selah',           'Hebrew (Psalms) — possibly \"pause and consider\"',
                        [], 3),
]


def is_dict_slug(slug):
    """Check if slug has a real dictionary entry."""
    return os.path.exists(os.path.join(DICT_DIR, f'{slug}.html'))


def render_stars(p):
    """Render popularity stars (1-5)."""
    if p <= 0:
        return ''
    filled = '★' * p
    empty = '☆' * (5 - p)
    label = {5: 'very common', 4: 'common', 3: 'uncommon', 2: 'rare', 1: 'very rare'}.get(p, '')
    return f'<span class="pop" title="Popularity in modern use: {label}">{filled}<span class="pop-empty">{empty}</span></span>'


def render_card(slug_or_name, meaning, variants, popularity, headword=None):
    """Render a single name card. If slug_or_name is a dictionary slug,
    renders as a link; otherwise renders as an info-only div."""
    is_link = headword is not None and is_dict_slug(slug_or_name)
    display_name = headword if headword else slug_or_name
    safe_h = html_mod.escape(display_name)
    safe_m = meaning  # may contain <em> tags — don't escape

    # Build search-haystack: name + variants + plain-text meaning
    plain_m = re.sub(r'<[^>]+>', '', meaning)
    haystack_parts = [display_name.lower(), plain_m.lower()]
    haystack_parts.extend(v.lower() for v in variants)
    data_search = html_mod.escape(' '.join(haystack_parts), quote=True)

    stars_html = render_stars(popularity)
    variants_html = ''
    if variants:
        v_safe = [html_mod.escape(v) for v in variants]
        variants_html = (
            f'<div class="name-variants"><span class="vk">Also:</span> '
            f'{", ".join(v_safe)}</div>'
        )

    inner = (
        f'<div class="name-head"><div class="name-word">{safe_h}</div>{stars_html}</div>'
        f'<div class="name-meaning">{safe_m}</div>'
        f'{variants_html}'
    )

    if is_link:
        return f'<a class="name-card" href="{slug_or_name}.html" data-search="{data_search}">{inner}</a>'
    else:
        return f'<div class="name-card name-card-info" data-search="{data_search}">{inner}</div>'


def render_biblical_section(title, anchor, intro, names):
    cards = []
    primaries = 0
    variant_count = 0
    for slug, meaning, variants, popularity in names:
        if popularity == 0:
            continue  # skip duplicate placeholder rows
        hw = get_headword(slug)
        if hw is None:
            print(f'  WARN: no headword for biblical slug {slug} (skipping)')
            continue
        cards.append(render_card(slug, meaning, variants, popularity, hw))
        primaries += 1
        variant_count += len(variants)
    cards_html = '\n        '.join(cards)
    total = primaries + variant_count
    sec = f'''
    <section class="names-section" id="{anchor}">
        <h2>{title} <span class="count-badge-lg">{primaries} primary <span style="opacity:0.7;font-weight:400;">· {total} w/ variants</span></span></h2>
        <p class="sec-intro">{intro}</p>
        <div class="names-grid">
        {cards_html}
        </div>
    </section>
    '''
    return (sec, primaries, variant_count)


def render_tradition_section(title, anchor, intro, names):
    cards = []
    primaries = 0
    variant_count = 0
    # Aliases for tradition names where the most-famous bearer has a more
    # specific slug than the simple lower-case form. The DISPLAY name on
    # the card stays the popular form; the link goes to the specific entry.
    alias = {
        'Catherine': 'catherine-of-siena',
        'Theresa':   'teresa-of-avila',
        'Gregory':   'gregory-the-great',
        'Bernard':   'bernard-of-clairvaux',
    }
    for name, meaning, variants, popularity in names:
        if popularity == 0:
            continue
        # 1) check explicit alias map first
        # 2) then check direct lower-case-and-dashed form
        # 3) fall back to info-only card
        if name in alias and is_dict_slug(alias[name]):
            cards.append(render_card(alias[name], meaning, variants, popularity, name))
        else:
            slug_lower = name.lower().replace(' ', '-')
            if is_dict_slug(slug_lower):
                cards.append(render_card(slug_lower, meaning, variants, popularity, name))
            else:
                cards.append(render_card(name, meaning, variants, popularity, name))
        primaries += 1
        variant_count += len(variants)
    cards_html = '\n        '.join(cards)
    total = primaries + variant_count
    sec = f'''
    <section class="names-section" id="{anchor}">
        <h2>{title} <span class="count-badge-lg">{primaries} primary <span style="opacity:0.7;font-weight:400;">· {total} w/ variants</span></span></h2>
        <p class="sec-intro">{intro}</p>
        <div class="names-grid">
        {cards_html}
        </div>
    </section>
    '''
    return (sec, primaries, variant_count)


def main():
    print('Building baby-names.html (variants + popularity + search)…')
    male_html, male_p, male_v = render_biblical_section(
        'Biblical Boy Names', 'boys',
        'Biblical names suited for boys — patriarchs, prophets, judges, kings, and apostles. Each card shows the canonical headword, popularity rating (1-5 stars), one-line meaning, and common nicknames/variants. Click any card for the full dictionary entry.',
        MALE,
    )
    female_html, female_p, female_v = render_biblical_section(
        'Biblical Girl Names', 'girls',
        'Biblical names suited for girls — matriarchs, prophetesses, queens, and disciples. Each card shows the canonical headword, popularity rating, one-line meaning, and common nicknames/variants.',
        FEMALE,
    )
    unisex_html, unisex_p, unisex_v = render_biblical_section(
        'Biblical Unisex Names', 'unisex',
        'Biblical place-names and concept-names used for both boys and girls — Shiloh, Eden, Jordan, Zion, Carmel.',
        UNISEX,
    )
    christ_male_html, cm_p, cm_v = render_tradition_section(
        'Christian Tradition — Boys', 'christian-male',
        'Names not from the Bible itself but carried in the Christian tradition — Charles, William, Augustine, Wesley, virtue names, early-church saints, Reformers. Info-only cards (no dictionary entry unless one already exists).',
        CHRISTIAN_MALE,
    )
    christ_female_html, cf_p, cf_v = render_tradition_section(
        'Christian Tradition — Girls', 'christian-female',
        'Non-biblical Christian names — Catherine, Theresa, Lucy; the Christian virtue names (Faith, Hope, Charity, Grace, Joy); early-church martyrs (Cecilia, Agnes, Perpetua, Felicity).',
        CHRISTIAN_FEMALE,
    )

    total_p = male_p + female_p + unisex_p + cm_p + cf_p
    total_v = male_v + female_v + unisex_v + cm_v + cf_v
    grand = total_p + total_v

    html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/dictionary/baby-names.html">
    <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baby Names from the Bible &mdash; The MOOP Dictionary</title>
    <meta name="description" content="Biblical baby names with Hebrew and Greek meaning, plus Christian-tradition names — boys, girls, and unisex. Search by primary name OR by nickname (typing 'Susie' finds Susanna).">
    <meta property="og:title" content="Biblical Baby Names &mdash; The MOOP Dictionary">
    <meta property="og:description" content="Boy, girl, unisex, and Christian-tradition names with original-language meaning and common nicknames.">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1, h2, h3 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px; border-bottom:1px solid var(--border); position:sticky; top:0; background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.8rem; padding:3px 6px; border-radius:6px; }}
        nav a:hover, nav a.active {{ color:var(--gold); }}
        .container {{ max-width:1100px; margin:0 auto; padding:30px 20px 60px; }}
        .hero {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .hero h1 {{ font-size:2.6rem; color:var(--gold-light); margin-bottom:12px; }}
        .hero .lead {{ color:var(--gray); max-width:720px; margin:10px auto; font-size:1rem; }}
        .hero .totals {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin-top:14px; }}
        .hero .totals > span {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; padding:4px 14px; border-radius:14px; font-size:0.82rem; }}

        /* Search box */
        .search-wrap {{ margin:24px auto 8px; max-width:600px; }}
        .search-wrap input {{ width:100%; padding:14px 18px; font-size:1rem; font-family:inherit; background:var(--card); border:1px solid var(--border); border-radius:30px; color:var(--white); outline:none; transition:border-color 0.2s; }}
        .search-wrap input:focus {{ border-color:var(--gold); }}
        .search-wrap input::placeholder {{ color:var(--gray); font-style:italic; }}
        .search-hint {{ text-align:center; color:var(--gray); font-size:0.78rem; margin-top:4px; }}
        .search-empty {{ display:none; text-align:center; color:var(--gold); padding:40px 20px; font-style:italic; }}
        body.searching .search-empty.active {{ display:block; }}

        /* Quick nav pills */
        .quick-nav {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:22px 0 10px; }}
        .quick-nav a {{ background:var(--card); border:1px solid var(--border); color:var(--white) !important; text-decoration:none; padding:8px 16px; border-radius:20px; font-size:0.85rem; }}
        .quick-nav a:hover {{ border-color:var(--gold); color:var(--gold) !important; }}

        /* Editor note */
        .editor-note {{ background:rgba(212,175,55,0.05); border:1px solid var(--border); border-radius:10px; padding:18px 22px; margin:24px 0 0; font-size:0.92rem; }}
        .editor-note h3 {{ color:var(--gold); font-size:1rem; margin-bottom:6px; font-family:'Inter',sans-serif; font-weight:600; }}

        /* Sections + cards */
        .names-section {{ margin:48px 0; scroll-margin-top:80px; }}
        .names-section.empty {{ display:none; }}
        .names-section h2 {{ color:var(--gold-light); font-size:1.7rem; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:8px; }}
        .sec-intro {{ color:var(--gray); font-size:0.92rem; margin-bottom:20px; max-width:780px; }}
        .count-badge-lg {{ display:inline-block; background:var(--gold); color:#000; font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:10px; margin-left:8px; vertical-align:middle; }}
        .names-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:12px; }}
        .name-card {{ display:block; background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 18px; text-decoration:none; color:var(--white) !important; transition:border-color 0.2s, transform 0.15s; }}
        .name-card:hover {{ border-color:var(--gold); transform:translateY(-1px); }}
        .name-card-info {{ cursor:default; }}
        .name-card-info:hover {{ transform:none; }}
        .name-head {{ display:flex; align-items:baseline; justify-content:space-between; gap:8px; margin-bottom:5px; }}
        .name-word {{ font-family:'Playfair Display',serif; font-size:1.18rem; color:var(--gold-light); line-height:1.2; }}
        .pop {{ font-size:0.78rem; color:var(--gold); letter-spacing:0.5px; white-space:nowrap; line-height:1; }}
        .pop-empty {{ opacity:0.25; }}
        .name-meaning {{ font-size:0.83rem; color:var(--gray); line-height:1.5; }}
        .name-meaning em {{ color:var(--gold); font-style:italic; }}
        .name-variants {{ font-size:0.78rem; color:var(--gold); margin-top:7px; padding-top:6px; border-top:1px dashed rgba(212,175,55,0.25); font-style:italic; }}
        .name-variants .vk {{ font-style:normal; opacity:0.7; font-size:0.72rem; letter-spacing:0.04em; }}

        /* Hidden by search */
        .name-card.hidden {{ display:none; }}

        footer {{ text-align:center; padding:32px 20px; border-top:1px solid var(--border); margin-top:50px; color:var(--gray); font-size:0.88rem; }}
        footer a {{ color:var(--gray); text-decoration:none; }}
        footer a:hover {{ color:var(--gold); }}

        body.light-mode {{ --bg:#F5F3EF; --card:#FFF; --white:#1a1a1a; --gray:#666; --border:#d4d0c8; background:#F5F3EF; color:#1a1a1a; }}
        body.light-mode nav {{ background:rgba(245,243,239,0.97); }}
        body.light-mode img[src*="/icons/shield-"]:not([src*="-bronze"]) {{ filter:brightness(.72) saturate(1.18) hue-rotate(-12deg); }}
        body.light-mode .name-card,
        body.light-mode .quick-nav a,
        body.light-mode .editor-note,
        body.light-mode .search-wrap input {{ background:#fff; border-color:#d4d0c8; }}
        body.light-mode .editor-note {{ background:rgba(212,175,55,0.04); }}
        a, a:link, a:visited {{ color:var(--gold) !important; }}
        @media (max-width:560px) {{ .hero h1 {{ font-size:2rem; }} .names-grid {{ grid-template-columns:1fr; }} }}
    </style>
    <link rel="stylesheet" href="/assets/css/light-icons.css">
    <link rel="stylesheet" href="/assets/css/print.css" media="print">
</head>
<body>
    <nav>
        <a href="../index.html">Home</a>
        <a href="../bible.html">BTE</a>
        <a href="index.html" class="active">Dictionary</a>
        <a href="names.html">Biblical Names</a>
        <a href="baby-names.html" class="active">Baby Names</a>
        <a href="../blog.html">Blog</a>
    </nav>
    <div class="container">
        <div class="hero">
            <h1>Biblical Baby Names</h1>
            <p class="lead">Biblical boy, girl, and unisex names &mdash; plus Christian-tradition names (Charles, William, Catherine, virtue names like Grace/Faith/Hope, early-church saints, Reformers). Each card has a 1-5 popularity star rating and lists common nicknames + language variants.</p>
            <div class="totals">
                <span>{total_p} primary names</span>
                <span>{total_v} variants</span>
                <span>{grand} total displayed</span>
            </div>

            <div class="search-wrap">
                <input type="search" id="name-search" placeholder="Search by name or nickname &mdash; try 'Susie', 'Pete', 'Becky', 'Liam'..." autocomplete="off">
                <div class="search-hint">Searches primary names + nicknames + meanings. Variants like &ldquo;Susie&rdquo; find Susanna; &ldquo;Pete&rdquo; finds Peter.</div>
            </div>

            <div class="quick-nav">
                <a href="#boys">Bib. Boys &#9662;</a>
                <a href="#girls">Bib. Girls &#9662;</a>
                <a href="#unisex">Unisex &#9662;</a>
                <a href="#christian-male">Christian Boys &#9662;</a>
                <a href="#christian-female">Christian Girls &#9662;</a>
                <a href="names.html">Full Names Index &rarr;</a>
            </div>
            <div class="editor-note">
                <h3>&#128153; A Note from the Editor</h3>
                <p>This baby-name directory is split off from the larger biblical-names index to serve expecting parents and curious readers. Curated by Adam Johns, editor of the MOOP Dictionary. The biblical sections link to full dictionary entries; the Christian-tradition section covers popular non-biblical Christian names (Charles, William, Catherine, virtue names, etc.) as info-only cards. Personal-family entries (Maria, Malachi Andrew, Hope, Mercy) represent his wife and three children lost too soon.</p>
            </div>
        </div>

        <div class="search-empty">No names match your search. Try a shorter query, or browse the sections below.</div>

        {male_html}
        {female_html}
        {unisex_html}
        {christ_male_html}
        {christ_female_html}

        <section class="names-section">
            <h2>Looking for More?</h2>
            <p class="sec-intro">The full <a href="names.html">Biblical Names index</a> covers every name in the dictionary (not just baby names). The full <a href="index.html">dictionary index</a> covers all 5,000+ entries across doctrine, persons, places, and Hebrew/Greek word studies.</p>
        </section>
    </div>
    <footer>
        <p>Baby Names from the Bible &middot; Part of <a href="index.html">The MOOP Dictionary</a> &middot; <a href="../bible.html">Bible Translation Engine</a></p>
        <p style="margin-top:8px;font-size:0.78rem;">&copy; 2026 U.S.M.C. Ministries</p>
    </footer>

    <script>
    (function() {{
        var input = document.getElementById('name-search');
        var sections = Array.prototype.slice.call(document.querySelectorAll('.names-section'));
        var emptyMsg = document.querySelector('.search-empty');
        if (!input) return;

        function filter() {{
            var q = input.value.trim().toLowerCase();
            var any = false;
            sections.forEach(function(sec) {{
                var cards = sec.querySelectorAll('.name-card');
                var visible = 0;
                cards.forEach(function(c) {{
                    var hay = c.getAttribute('data-search') || '';
                    if (!q || hay.indexOf(q) !== -1) {{
                        c.classList.remove('hidden');
                        visible++;
                    }} else {{
                        c.classList.add('hidden');
                    }}
                }});
                if (cards.length === 0) return; // \"Looking for more\" section has no cards
                if (visible === 0 && q) {{ sec.classList.add('empty'); }}
                else {{ sec.classList.remove('empty'); any = true; }}
            }});
            if (q && !any) {{ emptyMsg.classList.add('active'); document.body.classList.add('searching'); }}
            else {{ emptyMsg.classList.remove('active'); document.body.classList.remove('searching'); }}
        }}

        input.addEventListener('input', filter);
        // Allow Escape to clear
        input.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{ input.value = ''; filter(); input.blur(); }}
        }});
    }})();
    </script>
</body>
</html>'''

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f'Wrote {OUT}')
    print(f'  Biblical Boys:           {male_p:3d} primary  ({male_p + male_v:3d} w/ variants)')
    print(f'  Biblical Girls:          {female_p:3d} primary  ({female_p + female_v:3d} w/ variants)')
    print(f'  Biblical Unisex:         {unisex_p:3d} primary  ({unisex_p + unisex_v:3d} w/ variants)')
    print(f'  Christian Tradition (M): {cm_p:3d} primary  ({cm_p + cm_v:3d} w/ variants)')
    print(f'  Christian Tradition (F): {cf_p:3d} primary  ({cf_p + cf_v:3d} w/ variants)')
    print(f'  ---------------------------------------------------')
    print(f'  TOTAL:                  {total_p:3d} primary  ({grand:3d} w/ variants)')


if __name__ == '__main__':
    main()
