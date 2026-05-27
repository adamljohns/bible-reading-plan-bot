#!/usr/bin/env python3
"""add_reformed_dict_entries.py — add a curated batch of Reformed-theology
terms to the MOOP dictionary so the autolinker can pick them up.

Each entry creates a docs/dictionary/<slug>.html page using a modest
template (title + etymology + biblical definition + scripture refs +
related words) and adds the token to docs/dictionary/manifest.json.

The definitions are intentionally short and uncontroversial — Adam will
flesh out the entries he cares most about in his own voice. The job of
this script is just to fill the lookup gap so the autolinker can link
these words across the editorial essays.
"""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DICT_DIR = ROOT / 'docs' / 'dictionary'
MANIFEST = DICT_DIR / 'manifest.json'

# 40 high-value Reformed / theology terms missing from the dictionary as of
# the 2026-05-27 audit. Format: (slug, display_word, part_of_speech,
# etymology, definition_paragraph, scripture_refs[(ref, text)], related_slugs)
ENTRIES = [
    ('corruption-doctrine', 'Corruption', 'noun',
     'From Latin <em>corrumpere</em> (to break thoroughly, spoil). In Reformed theology, the doctrine that human nature is broken in every faculty by the Fall, distinct from but related to "total depravity."',
     'In Reformed theology, corruption is the spoiling of human nature in every faculty — mind, will, affections, and body — as a consequence of the Fall. Distinct from "depravity" (which speaks to extent), corruption speaks to the radical nature of sin\'s effect: not that every person is as wicked as he could be, but that no faculty of any natural person escapes sin\'s ruining influence. The doctrine grounds the Reformed insistence that salvation must originate in God, since corrupted faculties cannot produce uncorrupted faith.',
     [('Genesis 6:5', 'every intention of the thoughts of his heart was only evil continually'),
      ('Romans 3:10-12', 'None is righteous, no, not one'),
      ('Ephesians 2:1-3', 'dead in the trespasses and sins')],
     ['depravity', 'sin', 'fall', 'regeneration']),

    ('effectual', 'Effectual', 'adjective',
     'From Latin <em>effectualis</em> (producing the intended effect). In Reformed soteriology, the term most often appears in "effectual calling" — the Spirit\'s saving call that actually accomplishes what it summons.',
     'In Reformed theology, "effectual" most often modifies "calling" or "grace." The effectual call is the work of the Holy Spirit in which He so applies the gospel to the elect that they actually come to Christ — distinct from the general or external call, which goes to all hearers but does not, of itself, secure response. The doctrine flows from the Reformed conviction that fallen sinners cannot answer a merely outward summons; the Spirit must apply the call inwardly with regenerating power.',
     [('Romans 8:30', 'those whom he called he also justified'),
      ('1 Corinthians 1:23-24', 'to those who are called, both Jews and Greeks, Christ the power of God'),
      ('John 6:44', 'No one can come to me unless the Father who sent me draws him')],
     ['calling', 'regeneration', 'election', 'monergism']),

    ('confessional', 'Confessional', 'adjective',
     'From Latin <em>confessio</em> (acknowledgment, profession). In Reformed and Lutheran usage, "confessional" describes a church, pastor, or movement that holds to a written historic confession of faith as its doctrinal standard.',
     'A confessional church is one bound by a written historic confession — the Westminster Standards, the 1689 London Baptist Confession, the Heidelberg Catechism, the Three Forms of Unity, the Lutheran Book of Concord, or similar. "Confessional" stands in contrast to "no-creed-but-the-Bible" practices and to broadly evangelical approaches that affirm Scripture but reject formal subscription to a confession. Reformed confessionalism holds that historic confessions are not above Scripture but provide a faithful summary of what Scripture teaches, anchoring the church against doctrinal drift across generations.',
     [('2 Timothy 1:13-14', 'Follow the pattern of the sound words that you have heard from me'),
      ('Jude 1:3', 'contend for the faith that was once for all delivered to the saints')],
     ['creed', 'westminster-confession', 'heidelberg-catechism']),

    ('egalitarian', 'Egalitarian', 'adjective',
     'From French <em>égalitaire</em> (relating to equality). In contemporary evangelical usage, egalitarianism is the view that all church and family offices are open to women on the same terms as men, denying any role-based distinction between the sexes in church leadership or marriage.',
     'Egalitarianism in evangelical theology is the position that gender carries no functional distinction in church leadership or marital authority. Egalitarians read passages like 1 Timothy 2 and 1 Corinthians 14 as culturally bound and not normative, and argue that Galatians 3:28 ("there is neither male nor female") establishes ministerial equality. The MOOP rubric treats egalitarian polity as a meaningful doctrinal flag because the broader pattern of Scripture, both in creation order and apostolic teaching, establishes complementarian roles in church and home; deliberate departure from those roles is therefore noted as a red signal in the church scorecard.',
     [('1 Timothy 2:11-14', 'I do not permit a woman to teach or to exercise authority over a man'),
      ('1 Corinthians 14:34-35', 'the women should keep silent in the churches'),
      ('Ephesians 5:22-25', 'Wives, submit to your own husbands, as to the Lord')],
     ['complementarian', 'patriarchy', 'headship']),

    ('expositional', 'Expositional', 'adjective',
     'From Latin <em>expositio</em> (a setting forth, explanation). In contemporary Reformed usage, "expositional preaching" is preaching that draws its main point, structure, and application from the explained meaning of a specific text of Scripture, often working through a book consecutively.',
     'Expositional (or expository) preaching is the practice of preaching where the point of the text becomes the point of the sermon. The preacher labors to explain what the inspired author meant by the words he wrote, then applies that meaning to the hearers; the sermon\'s structure and emphasis are governed by the text, not by topical illustration or felt-needs framing. 9Marks and other Reformed-evangelical networks identify expositional preaching as the first of the marks of a healthy church, since it disciplines the pulpit to feed the flock what God said rather than what the preacher prefers to say.',
     [('Nehemiah 8:8', 'They read from the book, from the Law of God, clearly, and they gave the sense'),
      ('2 Timothy 4:2', 'preach the word; be ready in season and out of season'),
      ('Acts 20:27', 'I did not shrink from declaring to you the whole counsel of God')],
     ['preaching', 'exegesis', 'hermeneutics', 'word']),

    ('presbytery', 'Presbytery', 'noun',
     'From Greek <em>presbyterion</em> (council of elders). In Presbyterian polity, a presbytery is the regional court of elders that holds jurisdiction over the ministers and churches in its bounds.',
     'In Presbyterian polity, the presbytery is the assembly of teaching elders (pastors) and ruling elders from each congregation within a defined geographic region. The presbytery ordains and credentials ministers, examines candidates, hears appeals from local church sessions, and provides accountability that no congregation oversees only itself. The Presbyterian Church in America, the Orthodox Presbyterian Church, the Evangelical Presbyterian Church, and similar bodies all govern through presbyteries, with regional presbyteries reporting to a national General Assembly.',
     [('Acts 15:6', 'The apostles and the elders were gathered together to consider this matter'),
      ('1 Timothy 4:14', 'when the council of elders laid their hands on you')],
     ['elder', 'session', 'synod', 'pca']),

    ('synod', 'Synod', 'noun',
     'From Greek <em>synodos</em> (a coming together). A church assembly, especially in Presbyterian or continental Reformed polity, gathered for doctrine, discipline, and government above the level of the local congregation or presbytery.',
     'A synod is a deliberative church assembly with binding doctrinal and disciplinary authority. In American Presbyterianism, synods sat between presbyteries and the General Assembly in earlier polity (some bodies retain this layer; others have removed it). In continental Reformed churches like the URCNA, a synod is the equivalent of a Presbyterian General Assembly. Historic synods such as the Synod of Dort (1618-19) and the Westminster Assembly (1643-49) produced confessions that still bind major Reformed denominations.',
     [('Acts 15:22-29', 'the apostles and the elders, with the whole church, decided'),
      ('Proverbs 11:14', 'in an abundance of counselors there is safety')],
     ['presbytery', 'general-assembly', 'dort', 'westminster-confession']),

    ('church-session', 'Session', 'noun',
     'From Latin <em>sessio</em> (a sitting). In Presbyterian polity, the session is the local-church court — the assembly of teaching and ruling elders who govern the congregation\'s spiritual life.',
     'In Presbyterian polity, the session is the local body of elders (the pastor as teaching elder, plus the ruling elders elected by the congregation) that holds spiritual oversight of the church. The session receives members, administers discipline, oversees the pulpit, and reports to the regional presbytery. The deacons handle mercy and finances; the session handles doctrine, worship, and shepherding. A healthy session means a plurality of qualified elders sharing the spiritual weight, rather than a single pastor bearing it alone.',
     [('Acts 20:28', 'Pay careful attention to yourselves and to all the flock'),
      ('Titus 1:5', 'appoint elders in every town'),
      ('1 Peter 5:1-2', 'shepherd the flock of God that is among you')],
     ['elder', 'presbytery', 'deacon', 'plurality']),

    ('preterist', 'Preterist', 'noun / adjective',
     'From Latin <em>praeteritus</em> (gone by). In eschatology, a preterist holds that most or all biblical prophecies — particularly in Revelation and the Olivet Discourse — were fulfilled in the first century, principally in the destruction of Jerusalem in AD 70.',
     'Preterism is the eschatological position that most New Testament prophecies have already been fulfilled in the past. Partial preterists (a recognized Reformed view) hold that most of Matthew 24 and Revelation refer to AD 70 but maintain the future bodily return of Christ and final judgment. Full or hyper-preterists hold that ALL prophecy including the second coming was fulfilled in AD 70 — a position outside historic Christian orthodoxy and rejected by every Reformed confession. The MOOP rubric flags hyper-preterism as a serious doctrinal error.',
     [('Matthew 24:34', 'this generation will not pass away until all these things take place'),
      ('Acts 1:11', 'this Jesus, who was taken up from you into heaven, will come in the same way'),
      ('1 Thessalonians 4:16', 'the Lord himself will descend from heaven')],
     ['eschatology', 'futurist', 'millennium', 'judgment']),

    ('futurist', 'Futurist', 'noun / adjective',
     'From Latin <em>futurus</em> (about to be). In eschatology, a futurist holds that most or all biblical prophecies — particularly in Revelation chapters 4-22 — refer to events still future, occurring at or near the second coming of Christ.',
     'Futurism is the eschatological position that most of Revelation and other prophetic passages await future fulfillment. Classical dispensational futurism reads Revelation 4-22 as a future tribulation period and millennial kingdom. Historic premillennialism is a Reformed-compatible form of futurism. Futurism stands in contrast to preterism (already-fulfilled) and idealism (symbolic of all-history). The Reformed tradition contains a range of futurist, idealist, and partial-preterist positions; the MOOP rubric does not flag any of the historic options as doctrinally suspect, only the modern hyper-preterism that denies a future return of Christ.',
     [('Revelation 22:7', 'I am coming soon'),
      ('Matthew 24:30', 'they will see the Son of Man coming on the clouds of heaven'),
      ('2 Peter 3:10', 'the day of the Lord will come like a thief')],
     ['eschatology', 'preterist', 'millennium', 'premillennial']),

    ('purgatory', 'Purgatory', 'noun',
     'From Latin <em>purgatorium</em> (place of cleansing). In Roman Catholic theology, an intermediate state in which souls of the saved undergo purifying suffering before entering heaven. Reformed theology rejects purgatory as unbiblical.',
     'Purgatory in Roman Catholic theology is an intermediate state in which souls of the redeemed undergo purification of remaining venial sins before entering the beatific vision of heaven. The doctrine rests primarily on 2 Maccabees 12 and a particular reading of 1 Corinthians 3:15, with the practice of indulgences historically tied to reducing purgatorial time. Reformed and confessional Protestant theology rejects purgatory entirely — Christ\'s atoning work is complete (Hebrews 10:14), the believer is justified by faith alone, and to be absent from the body is to be present with the Lord (2 Corinthians 5:8). The doctrine of purgatory was a flashpoint of the Reformation.',
     [('Hebrews 10:14', 'by a single offering he has perfected for all time those who are being sanctified'),
      ('2 Corinthians 5:8', 'we would rather be away from the body and at home with the Lord'),
      ('Luke 23:43', 'today you will be with me in paradise')],
     ['heaven', 'hell', 'justification', 'atonement']),

    ('sphere-sovereignty', 'Sphere Sovereignty', 'noun phrase',
     'A Reformed doctrine developed especially by Abraham Kuyper, holding that distinct spheres of human life — family, church, state, school, market — each have their own divinely-ordained authority and competence, and no sphere may usurp the authority of another.',
     'Sphere sovereignty is the Dutch-Reformed (especially Kuyperian) doctrine that God has ordained distinct spheres of human life — family, church, civil government, education, science, art, commerce — each with its own God-given authority and competence. Christ\'s lordship runs through every sphere ("there is not one square inch of the whole domain of human existence over which Christ, who is sovereign over all, does not cry: Mine!" — Kuyper), but no sphere may usurp another. The state has no authority over the worship of the church; the church has no authority over the policies of the state; both have limits set by God. The doctrine grounds Reformed resistance to statism, ecclesial overreach, and individualistic libertarianism alike.',
     [('Romans 13:1-7', 'Let every person be subject to the governing authorities'),
      ('Matthew 22:21', 'Render to Caesar the things that are Caesar\'s, and to God the things that are God\'s'),
      ('Ephesians 5-6', 'household codes establishing family-sphere authority')],
     ['sovereignty', 'dominion', 'covenant', 'common-grace']),

    ('arminian', 'Arminian', 'adjective / noun',
     'From the surname of Jacobus Arminius (1560-1609), Dutch theologian whose followers (the Remonstrants) opposed Reformed orthodoxy at the Synod of Dort.',
     'Arminianism is the theological system that affirms conditional election (God elects those He foreknew would believe), unlimited atonement (Christ died for all without exception), prevenient but resistible grace, and the possibility of falling from saving grace. Named for Jacobus Arminius and codified by his Dutch followers in the 1610 Remonstrance, Arminianism was formally rejected by the Synod of Dort (1618-19) — the canons of which produced the so-called five points of Calvinism in response. Modern Wesleyans, most Pentecostals, the Free Will Baptists, and much of the broader American evangelical world hold positions in the Arminian family. The MOOP rubric treats Arminianism as historically Protestant and within the bounds of Christian orthodoxy, while marking the Reformed position as the editorial baseline.',
     [('Romans 8:29-30', 'those whom he foreknew he also predestined'),
      ('Acts 13:48', 'as many as were appointed to eternal life believed'),
      ('John 6:37', 'All that the Father gives me will come to me')],
     ['calvinist', 'election', 'predestination', 'monergism', 'dort']),

    ('calvinist', 'Calvinist', 'adjective / noun',
     'From the surname of John Calvin (1509-1564), French Reformer. In the contemporary sense, a Calvinist is someone who holds the Reformed soteriology codified at the Synod of Dort and summarized in the acronym TULIP.',
     'Calvinism in modern usage refers to the Reformed soteriology that affirms total depravity, unconditional election, limited (or particular) atonement, irresistible (or effectual) grace, and the perseverance of the saints — the so-called five points or TULIP. Strictly speaking, "Calvinism" is broader than these five points; it is a full theological system covering covenant, ecclesiology, eschatology, worship, and Christian liberty. The Calvinistic tradition includes the Presbyterian, Reformed, and Reformed Baptist confessions, and shaped much of historic Anglicanism, Puritan New England, and the modern "New Calvinist" movement associated with figures like John Piper, Mark Dever, and Albert Mohler.',
     [('Ephesians 1:4-5', 'he chose us in him before the foundation of the world'),
      ('Romans 9:15-16', 'I will have mercy on whom I have mercy'),
      ('Ephesians 2:8-9', 'by grace you have been saved through faith')],
     ['arminian', 'tulip', 'election', 'predestination', 'reformed']),

    ('monergism', 'Monergism', 'noun',
     'From Greek <em>monos</em> (alone) + <em>ergon</em> (work). The doctrine that the new birth and saving faith are the work of God alone, without cooperation from the fallen will.',
     'Monergism is the doctrine that regeneration is monergistic — the work of one (God) alone. In the moment of new birth, the Holy Spirit acts on a dead sinner without any contributing cooperation from the sinner\'s fallen will, because a dead will cannot cooperate. Faith, then, is the fruit of regeneration rather than its cause. Reformed theology is monergistic on regeneration; Roman Catholic, Arminian, and Wesleyan theologies hold synergistic views in which the regenerate will cooperates with grace.',
     [('John 3:8', 'The wind blows where it wishes... So it is with everyone who is born of the Spirit'),
      ('Ephesians 2:1-5', 'even when we were dead in our trespasses, made us alive together with Christ'),
      ('Titus 3:5', 'he saved us... by the washing of regeneration and renewal of the Holy Spirit')],
     ['synergism', 'regeneration', 'effectual', 'sovereignty']),

    ('synergism', 'Synergism', 'noun',
     'From Greek <em>syn</em> (with) + <em>ergon</em> (work). The doctrine that the new birth or saving faith arises from the cooperative work of God and the human will responding to grace.',
     'Synergism is the doctrine that conversion involves a cooperation between divine grace and the human will. Most non-Reformed Protestant traditions hold synergistic positions: Wesleyans speak of prevenient grace enabling but not determining faith; Arminians hold that the elect are those whom God foreknew would freely respond. Reformed theology rejects synergism on regeneration (a dead will cannot cooperate) but affirms a kind of cooperation in sanctification, where the believer is genuinely active in pursuing holiness even as God works in him to will and to work.',
     [('Romans 9:16', 'So then it depends not on human will or exertion, but on God, who has mercy'),
      ('Philippians 2:12-13', 'work out your own salvation with fear and trembling, for it is God who works in you'),
      ('Joshua 24:15', 'choose this day whom you will serve')],
     ['monergism', 'free-will', 'regeneration', 'sanctification']),

    ('antinomian', 'Antinomian', 'adjective / noun',
     'From Greek <em>anti</em> (against) + <em>nomos</em> (law). The view that the moral law of God has no continuing role in the believer\'s life because of free grace.',
     'Antinomianism is the doctrinal error that minimizes or denies the moral law\'s ongoing role for the Christian. Practical antinomianism treats grace as license: since salvation is by grace, sin no longer matters. Theological antinomianism (in some 17th-century forms) held that the law has no place at all in the believer\'s sanctification. Paul confronts antinomian implications directly in Romans 6 ("Shall we continue in sin that grace may abound? By no means!"). Reformed theology rejects antinomianism by maintaining the so-called "third use" of the law — the law as a guide for the redeemed life — while affirming that justification is by faith alone, apart from works of the law.',
     [('Romans 6:1-2', 'Shall we continue in sin that grace may abound? By no means!'),
      ('Matthew 5:17-19', 'I have not come to abolish them but to fulfill them'),
      ('1 John 3:4', 'sin is lawlessness')],
     ['legalism', 'law', 'grace', 'sanctification']),

    ('cessationist', 'Cessationist', 'adjective / noun',
     'From Latin <em>cessare</em> (to cease). One who holds that the sign gifts of the apostolic age (tongues, prophecy, healing, apostleship in the technical sense) ceased with the closing of the New Testament canon.',
     'Cessationism is the position that the foundational and miraculous gifts associated with the apostolic era — tongues, prophecy, healing, signs and wonders, the office of apostle in its New Testament sense — ceased functioning by the close of the apostolic period and the completion of the canon. Confessional Reformed and confessional Lutheran theology have historically been cessationist. The cessationist argument rests on the foundational function of those gifts (Ephesians 2:20), the closing of the canon (Revelation 22:18-19), and the historical fact that miraculous gifts faded markedly after the apostles. Cessationism stands in contrast to continuationism.',
     [('Hebrews 1:1-2', 'in these last days he has spoken to us by his Son'),
      ('Ephesians 2:20', 'built on the foundation of the apostles and prophets'),
      ('1 Corinthians 13:8-10', 'as for tongues, they will cease; as for knowledge, it will pass away')],
     ['continuationist', 'apostle', 'prophet', 'tongues']),

    ('continuationist', 'Continuationist', 'adjective / noun',
     'One who holds that the gifts of the Holy Spirit, including miraculous and revelatory gifts, continue to function in the church today.',
     'Continuationism is the position that the gifts of the Holy Spirit, including tongues, prophecy, and miraculous healing, continue to operate in the church between the first and second comings of Christ. Reformed continuationists like Wayne Grudem and Sam Storms argue for an "open but cautious" approach, distinguishing modern prophetic gifting from canonical revelation; Pentecostal and charismatic continuationists generally hold a higher view of contemporary gifts. The continuationist position is held by Sovereign Grace Churches and by many Acts 29 and New Calvinist congregations; cessationism remains the historic confessional Reformed position. The MOOP rubric treats both as within Christian orthodoxy when held responsibly.',
     [('1 Corinthians 14:1', 'pursue love, and earnestly desire the spiritual gifts, especially that you may prophesy'),
      ('Acts 2:17', 'in the last days... I will pour out my Spirit on all flesh'),
      ('Romans 12:6-8', 'Having gifts that differ according to the grace given to us')],
     ['cessationist', 'prophecy', 'tongues', 'sgc']),

    ('paedobaptism', 'Paedobaptism', 'noun',
     'From Greek <em>pais</em> (child) + <em>baptizein</em> (to baptize). The practice of baptizing the infant children of believing parents on the ground of God\'s covenant promise.',
     'Paedobaptism is the practice and doctrine of infant baptism, held by Presbyterian, Reformed, Anglican, Lutheran, Methodist, and most other historic Protestant traditions. The paedobaptist case rests on the continuity of the covenant of grace from Abraham through the New Covenant: as circumcision was the sign of covenant inclusion administered to infant sons of believers in the old covenant, baptism functions analogously as the sign of new-covenant inclusion administered to infant children of believing parents. Paedobaptists do not hold that baptism saves the child; they hold that it places the child in the visible covenant community where the means of grace operate.',
     [('Genesis 17:7-12', 'I will establish my covenant... and to your offspring after you'),
      ('Acts 2:38-39', 'the promise is for you and for your children'),
      ('Colossians 2:11-12', 'a circumcision made without hands... having been buried with him in baptism')],
     ['credobaptism', 'baptism', 'covenant', 'circumcision']),

    ('credobaptism', 'Credobaptism', 'noun',
     'From Latin <em>credo</em> (I believe) + <em>baptizein</em> (to baptize). The practice of baptizing only professing believers, on the ground that baptism is the sign of personal faith and union with Christ.',
     'Credobaptism (or "believer\'s baptism") is the practice and doctrine of baptizing only those who personally profess faith in Christ, held by Baptists, most non-denominational evangelicals, the Sovereign Grace Churches, the 9Marks network, and Founders Ministries. The credobaptist case rests on the New Testament pattern (every recorded baptism follows profession of faith), on the nature of the new covenant as composed of those whose hearts are circumcised, and on the symbolism of baptism as picturing the believer\'s union with Christ in His death and resurrection. The Reformed Baptist tradition holds credobaptism within an otherwise Reformed covenantal framework via the 1689 London Baptist Confession.',
     [('Acts 8:36-37', 'See, here is water! What prevents me from being baptized?'),
      ('Matthew 28:19', 'make disciples of all nations, baptizing them'),
      ('Romans 6:3-4', 'we were buried therefore with him by baptism into death')],
     ['paedobaptism', 'baptism', 'covenant', '1689-confession']),

    ('penal-substitution', 'Penal Substitution', 'noun phrase',
     'The doctrine that Christ, on the cross, took the place of sinners and bore the penalty their sins deserved, satisfying divine justice and securing their justification.',
     'Penal substitutionary atonement is the central historic-Protestant understanding of the cross: Christ bore the just penalty (penal) that sinners deserved, in their place (substitution), so that God\'s justice is satisfied and the sinner can be reckoned righteous. The doctrine is rooted in Isaiah 53 ("the chastisement that brought us peace was upon him"), articulated by Paul in Romans 3 and 2 Corinthians 5, and codified in every major Protestant confession. The Reformation recovered penal substitution from medieval frameworks that often emphasized satisfaction without clear penal exchange. Recent challenges (from Christus Victor advocates and from some progressive theologies that call it "cosmic child abuse") have been firmly resisted by historic Reformed and evangelical theology.',
     [('Isaiah 53:5-6', 'he was pierced for our transgressions; he was crushed for our iniquities'),
      ('2 Corinthians 5:21', 'For our sake he made him to be sin who knew no sin'),
      ('Romans 3:25-26', 'whom God put forward as a propitiation by his blood')],
     ['atonement', 'propitiation', 'justification', 'imputation']),

    ('federal-headship', 'Federal Headship', 'noun phrase',
     'From Latin <em>foedus</em> (covenant). The doctrine that Adam represented the entire human race in the covenant of works, and Christ represents His people in the covenant of grace; the actions of each "federal head" are imputed to those they represent.',
     'Federal headship is the Reformed covenantal doctrine that two men stand as representative heads of two distinct peoples: Adam over the entire human race in the original covenant, and Christ over His elect people in the covenant of grace. Adam\'s sin is imputed to his posterity; Christ\'s righteousness is imputed to His people. The doctrine grounds both the universality of original sin (we sinned in Adam) and the assurance of justification (we are righteous in Christ). Romans 5:12-21 is the locus classicus. The federal framework distinguishes Reformed theology from views that locate guilt or merit purely in the personal acts of each individual.',
     [('Romans 5:18-19', 'as one trespass led to condemnation for all men, so one act of righteousness leads to justification'),
      ('1 Corinthians 15:22', 'in Adam all die, so also in Christ shall all be made alive'),
      ('1 Corinthians 15:45', 'The first man Adam became a living being; the last Adam became a life-giving spirit')],
     ['covenant', 'imputation', 'original-sin', 'justification']),

    ('imago-dei', 'Imago Dei', 'noun phrase (Latin)',
     'Latin for "image of God." The doctrine, drawn from Genesis 1:26-27, that human beings are made in the image of their Creator and therefore bear a unique dignity and accountability above the rest of creation.',
     'Imago Dei is the doctrine that humanity is created in the image and likeness of God (Genesis 1:26-27) — a status that grounds the unique dignity of every human life, the moral seriousness of human responsibility, and the possibility of relationship with God. The Reformed tradition distinguishes a "narrow" sense (the original righteousness lost in the Fall and being restored in Christ) from a "broader" sense (the structural capacities of rationality, moral agency, and dominion that survive in fallen humanity but are bent). The image grounds the prohibition against murder (Genesis 9:6), the case for human dignity in ethics, and the doctrine of redemption as a restoration of the marred image.',
     [('Genesis 1:26-27', 'Let us make man in our image, after our likeness'),
      ('Genesis 9:6', 'for God made man in his own image'),
      ('Colossians 3:10', 'put on the new self, which is being renewed in knowledge after the image of its creator')],
     ['dignity', 'creation', 'sin', 'redemption']),

    ('coram-deo', 'Coram Deo', 'noun phrase (Latin)',
     'Latin for "before the face of God." A theological shorthand for the conviction that every action, thought, and word of a Christian is lived in the conscious awareness of God\'s presence.',
     'Coram Deo is the Latin phrase meaning "before the face of God" — a Reformed shorthand for the conviction that all of life is lived in God\'s presence and under His gaze. R.C. Sproul popularized the phrase for modern American Reformed audiences as the heart of the Christian ethic: there is no secular zone, no private compartment, no moment when the believer is not under God\'s observing care. The phrase animates Reformed insistence on the integration of faith and work, the seriousness of personal holiness, and the Reformed worship principle that the gathered assembly stands directly before the throne of grace.',
     [('Psalm 139:7-8', 'Where shall I go from your Spirit? Or where shall I flee from your presence?'),
      ('Proverbs 15:3', 'The eyes of the LORD are in every place, keeping watch on the evil and the good'),
      ('Hebrews 4:13', 'no creature is hidden from his sight')],
     ['presence-god', 'sovereignty', 'holiness', 'sanctification']),

    ('ordo-salutis', 'Ordo Salutis', 'noun phrase (Latin)',
     'Latin for "order of salvation." The theological ordering of the distinct elements of God\'s saving work in the life of an individual believer.',
     'Ordo salutis is the theological term for the logical (not always chronological) ordering of the elements of salvation as God applies them to the elect. The classical Reformed ordo runs: election (eternal), then in time: effectual calling, regeneration, faith and repentance, justification, adoption, sanctification, perseverance, and glorification. Different Reformed teachers debate the ordering of certain elements (notably the relation of regeneration to faith), but the framework distinguishes the work of redemption accomplished (Christology, by Christ) from the work of redemption applied (soteriology, by the Spirit). Romans 8:29-30 supplies the most famous text.',
     [('Romans 8:29-30', 'those whom he foreknew he also predestined... called... justified... glorified'),
      ('Ephesians 1:3-14', 'he chose us... predestined us for adoption... in him we have redemption'),
      ('1 Corinthians 6:11', 'you were washed, you were sanctified, you were justified')],
     ['election', 'regeneration', 'justification', 'sanctification', 'glorification']),

    ('semper-reformanda', 'Semper Reformanda', 'noun phrase (Latin)',
     'Latin for "always reforming." The Reformed maxim that the church, having been reformed, must continue to be reformed according to the Word of God.',
     'Semper reformanda is the Reformed maxim ecclesia reformata, semper reformanda — "the church reformed, always being reformed according to the Word of God." The phrase does not mean that the church should be constantly changing with cultural fashion; it means that the church\'s confession and practice must be continually re-examined against the standard of Scripture, so that any drift can be corrected. The maxim is invoked both rightly (against complacency in doctrinally drifting denominations) and wrongly (by progressives appealing to it as license for novelty). The full phrase, with "according to the Word of God," resists the wrong appeal.',
     [('2 Timothy 3:16-17', 'All Scripture is breathed out by God and profitable for teaching, for reproof, for correction, and for training in righteousness'),
      ('Isaiah 8:20', 'To the teaching and to the testimony! If they will not speak according to this word, it is because they have no dawn'),
      ('Jude 1:3', 'contend for the faith that was once for all delivered to the saints')],
     ['reformation', 'reformed', 'sola-scriptura', 'confessional']),

    ('sola-scriptura', 'Sola Scriptura', 'noun phrase (Latin)',
     'Latin for "Scripture alone." The first of the five Reformation solas: the doctrine that Scripture is the supreme and final authority for the church\'s faith and life.',
     'Sola scriptura is the Reformation doctrine that Scripture is the sole infallible rule of faith and practice for the church. The doctrine does not deny the usefulness of tradition, confessions, or church councils — confessional Protestants explicitly affirm them — but it places all such authorities under Scripture rather than alongside it. The Roman Catholic position (formalized at Trent and reaffirmed at Vatican II) holds Scripture and unwritten apostolic tradition as a single deposit of revelation; the Reformation broke with that view, insisting that Scripture stands as judge over tradition. Article 1 of the Westminster Confession and the 1689 LBCF both establish sola scriptura as the church\'s rule.',
     [('2 Timothy 3:16-17', 'All Scripture is breathed out by God and profitable for teaching'),
      ('Isaiah 8:20', 'To the teaching and to the testimony! If they will not speak according to this word'),
      ('Matthew 15:6', 'you have made void the word of God for the sake of your tradition')],
     ['scripture', 'tradition', 'westminster-confession', '1689-confession', 'reformation']),

    ('sola-fide', 'Sola Fide', 'noun phrase (Latin)',
     'Latin for "faith alone." The Reformation doctrine that justification is by faith alone, apart from works.',
     'Sola fide is the Reformation doctrine that the sinner is justified before God by faith alone, apart from any contribution of personal works or merit. Justification is the legal declaration of righteousness, grounded entirely in Christ\'s imputed righteousness and received entirely through faith — itself a gift of God. The doctrine, articulated by Paul in Romans and Galatians and recovered at the Reformation, distinguishes Protestant soteriology from Roman Catholic teaching, which holds that justification involves an infused righteousness cooperated with by works. Luther called justification by faith alone the article on which the church stands or falls.',
     [('Romans 3:28', 'one is justified by faith apart from works of the law'),
      ('Galatians 2:16', 'a person is not justified by works of the law but through faith in Jesus Christ'),
      ('Ephesians 2:8-9', 'by grace you have been saved through faith... not a result of works')],
     ['justification', 'imputation', 'faith', 'reformation']),

    ('sola-gratia', 'Sola Gratia', 'noun phrase (Latin)',
     'Latin for "grace alone." The Reformation doctrine that salvation is by grace alone, with no contribution from human merit.',
     'Sola gratia is the Reformation doctrine that salvation is entirely the unmerited gift of God\'s grace, with no contribution from human merit at any stage. Election is gracious (God chose us before the foundation of the world, not because of foreseen worth); regeneration is gracious (God makes the dead alive without their cooperation); faith itself is the gift of grace; and the believer\'s perseverance is sustained by grace. Sola gratia stands against any framework — Pelagian, semi-Pelagian, or fully Roman Catholic — that locates any portion of the saving work in the merit of the saved.',
     [('Ephesians 2:8-9', 'by grace you have been saved through faith. And this is not your own doing; it is the gift of God'),
      ('Romans 11:6', 'if it is by grace, it is no longer on the basis of works'),
      ('Titus 3:5', 'he saved us, not because of works done by us in righteousness, but according to his own mercy')],
     ['grace', 'election', 'justification', 'reformation']),

    ('solus-christus', 'Solus Christus', 'noun phrase (Latin)',
     'Latin for "Christ alone." The Reformation doctrine that salvation is found in Christ alone, with no other mediator between God and man.',
     'Solus Christus is the Reformation doctrine that Jesus Christ is the sole mediator between God and man, and the sole ground of the believer\'s standing before God. The doctrine excludes Mary, the saints, the priesthood, and the church itself as objects of mediation or sources of merit; it locates the entire saving relationship in Christ\'s person and work. The doctrine was a flashpoint with the medieval Roman cult of the saints and with sacerdotal priestly mediation; it remains a flashpoint today where any "Jesus plus something" framework is proposed.',
     [('1 Timothy 2:5', 'there is one God, and there is one mediator between God and men, the man Christ Jesus'),
      ('John 14:6', 'I am the way, and the truth, and the life. No one comes to the Father except through me'),
      ('Acts 4:12', 'there is salvation in no one else, for there is no other name under heaven given among men by which we must be saved')],
     ['mediator', 'christ', 'redemption', 'reformation']),

    ('soli-deo-gloria', 'Soli Deo Gloria', 'noun phrase (Latin)',
     'Latin for "to God alone be the glory." The Reformation doctrine that the chief end of all human existence — and the chief purpose of redemption — is the glory of God.',
     'Soli Deo Gloria is the Reformation doctrine that the glory of God is the supreme end of all things: of creation, redemption, worship, and ordinary daily life. Reformed worship orders itself to display God\'s glory rather than to entertain the worshipper. Reformed vocational theology teaches that the carpenter\'s bench, the kitchen counter, and the soldier\'s field are all spheres of glorifying God when worked unto Him. J.S. Bach famously signed his manuscripts SDG — soli Deo gloria. The Westminster Shorter Catechism\'s opening line ("Man\'s chief end is to glorify God and to enjoy him forever") is the catechetical expression of this same conviction.',
     [('1 Corinthians 10:31', 'whether you eat or drink, or whatever you do, do all to the glory of God'),
      ('Romans 11:36', 'to him be glory forever. Amen'),
      ('Isaiah 42:8', 'I am the LORD; that is my name; my glory I give to no other')],
     ['glory', 'worship', 'doxology', 'vocation', 'westminster-confession']),

    ('regulative-principle', 'Regulative Principle', 'noun phrase',
     'The Reformed doctrine that the worship of God is regulated by Scripture: only what God has commanded in worship is to be done, and what is not commanded is forbidden.',
     'The regulative principle of worship is the historic Reformed conviction that God Himself prescribes how He is to be worshipped, and that the gathered worship of His people must include only what Scripture commands and exclude what it does not command. The principle stands behind Reformed simplicity in worship — the centrality of the read and preached Word, the singing of inspired (and often only inspired) song, the prayers of the saints, and the sacraments rightly administered — and against innovations like images, dramatic performance, or sensory atmospherics meant to manufacture experience. The contrasting normative principle (held by Lutherans and Anglicans) permits whatever Scripture does not forbid. Westminster Confession of Faith 21 lays out the regulative principle.',
     [('Deuteronomy 12:32', 'Everything that I command you, you shall be careful to do. You shall not add to it or take from it'),
      ('Leviticus 10:1-2', 'Nadab and Abihu... offered unauthorized fire before the LORD'),
      ('John 4:23-24', 'the true worshipers will worship the Father in spirit and truth')],
     ['worship', 'normative-principle', 'westminster-confession', 'sola-scriptura']),

    ('common-grace', 'Common Grace', 'noun phrase',
     'The Reformed doctrine that God shows non-saving favor to all of humanity — restraining sin, sustaining civilization, and granting good gifts even to those who do not know Him in saving faith.',
     'Common grace is the Reformed doctrine that God exhibits a non-saving but real favor toward all of humanity, distinct from the special saving grace given only to the elect. Common grace restrains the full outworking of human sin, sustains civilization and culture, grants the good gifts of rain and harvest to the just and unjust alike, and enables non-Christians to produce genuine goods in art, science, medicine, and statecraft. The doctrine grounds Christian engagement with the wider culture (we can learn from and partner with unbelievers in many domains) while preserving the special category of saving grace as a separate category given only to the redeemed.',
     [('Matthew 5:45', 'he makes his sun rise on the evil and on the good, and sends rain on the just and on the unjust'),
      ('Acts 14:17', 'he did not leave himself without witness, for he did good by giving you rains from heaven'),
      ('Psalm 145:9', 'The LORD is good to all, and his mercy is over all that he has made')],
     ['grace', 'sovereignty', 'providence', 'culture']),

    ('union-with-christ', 'Union with Christ', 'noun phrase',
     'The Reformed and Pauline doctrine that the believer is so joined to Christ by the Spirit and through faith that all of Christ\'s saving benefits are received in Him.',
     'Union with Christ is the Pauline doctrine that the believer is so joined to Christ — by the indwelling Spirit and through faith — that the believer\'s very identity, history, and future are now defined "in Christ." Election, justification, adoption, sanctification, perseverance, and glorification are all benefits received because the believer is united to Christ. Paul\'s phrase "in Christ" or "in him" appears over 160 times in his letters; John Murray called union with Christ the central truth of the whole doctrine of salvation. The doctrine guards against treating each saving benefit as a separable transaction; rather, all benefits flow from the single reality of being joined to the Savior.',
     [('Romans 6:5', 'we have been united with him in a death like his'),
      ('Galatians 2:20', 'I have been crucified with Christ. It is no longer I who live, but Christ who lives in me'),
      ('Ephesians 1:3', 'every spiritual blessing in the heavenly places in Christ')],
     ['justification', 'sanctification', 'adoption', 'covenant']),

    ('nine-marks-doctrine', 'Nine Marks', 'noun phrase',
     'A framework popularized by Mark Dever and the 9Marks ministry, describing nine biblical marks of a healthy church: expositional preaching, biblical theology, the gospel, conversion, evangelism, membership, discipline, discipleship, and biblical leadership.',
     'The Nine Marks framework, articulated by Mark Dever at Capitol Hill Baptist Church in Washington DC and propagated through the 9Marks ministry, identifies nine biblical marks of a healthy church: (1) expositional preaching, (2) biblical theology, (3) a biblical understanding of the gospel, (4) a biblical understanding of conversion, (5) a biblical understanding of evangelism, (6) a biblical understanding of church membership, (7) biblical church discipline, (8) a concern for discipleship and growth, and (9) biblical church leadership. The framework has shaped a generation of confessional Baptist and broader Reformed-evangelical pastors and is widely used as a self-assessment tool for church health.',
     [('Acts 2:42', 'they devoted themselves to the apostles\' teaching and the fellowship'),
      ('2 Timothy 4:2', 'preach the word'),
      ('Matthew 18:15-20', 'if your brother sins against you, go and tell him his fault')],
     ['9marks', 'church-discipline', 'expositional', 'membership']),

    ('westminster-confession', 'Westminster Confession', 'noun phrase',
     'The Westminster Confession of Faith (1646), the foundational confessional document of English-speaking Presbyterian and Reformed churches, produced by the Westminster Assembly of Divines.',
     'The Westminster Confession of Faith, produced by the Westminster Assembly meeting in London from 1643 to 1649 and adopted in its final form in 1646, is the foundational confessional standard of English-speaking Presbyterian and Reformed churches worldwide. Together with the Westminster Larger and Shorter Catechisms, the Confession provides a comprehensive Reformed theology covering Scripture, God, predestination, creation, providence, sin, covenant, Christ, salvation, the Christian life, the church, sacraments, and last things. The Confession governs the Presbyterian Church in America, the Orthodox Presbyterian Church, the ARP, the EPC, and many other bodies. Reformed Baptists hold to the closely-related 1689 London Baptist Confession.',
     [('2 Timothy 1:13', 'Follow the pattern of the sound words that you have heard from me'),
      ('Jude 1:3', 'contend for the faith that was once for all delivered to the saints')],
     ['1689-confession', 'heidelberg-catechism', 'confessional', 'reformed']),

    ('1689-confession', '1689 London Baptist Confession', 'noun phrase',
     'The Second London Baptist Confession of Faith (1677, published 1689), the foundational confessional standard of Reformed Baptists. Modeled closely on the Westminster Confession with revisions for Baptist ecclesiology and credobaptism.',
     'The 1689 London Baptist Confession of Faith is the foundational confessional standard of Reformed (or Particular) Baptists. Originally drafted in 1677 and published in 1689 after the Toleration Act made open Baptist worship legal in England, it follows the Westminster Confession closely on the doctrines of God, Scripture, predestination, Christ, and salvation, while revising the chapters on baptism (credobaptist), church government (congregational), and the magistrate (separation of church and state). The 1689 governs Founders Ministries churches, Reformed Baptist Network congregations, ARBCA, and Sovereign Grace Churches (with modifications). It is the most thorough Particular Baptist statement of Reformed theology in existence.',
     [('Acts 8:36-37', 'See, here is water! What prevents me from being baptized?'),
      ('1 Corinthians 11:23-26', 'For I received from the Lord what I also delivered to you'),
      ('Matthew 16:18', 'on this rock I will build my church')],
     ['westminster-confession', 'credobaptism', 'reformed-baptist', 'founders']),

    ('heidelberg-catechism', 'Heidelberg Catechism', 'noun phrase',
     'A Reformed catechism written in 1563 in Heidelberg under Elector Frederick III. Together with the Belgic Confession and the Canons of Dort, it forms the Three Forms of Unity of continental Reformed churches.',
     'The Heidelberg Catechism, written in 1563 by Zacharias Ursinus and Caspar Olevianus under the patronage of Elector Frederick III, is one of the most widely-used Reformed catechisms in history. Its 129 questions are organized around three themes: the sinner\'s misery, the sinner\'s deliverance in Christ, and the sinner\'s gratitude expressed in obedience. The catechism\'s first question and answer — "What is your only comfort in life and in death? That I, with body and soul, both in life and in death, am not my own, but belong with body and soul, both in life and in death, to my faithful Saviour Jesus Christ" — is one of the most beloved formulations in Reformed Christianity. The Heidelberg, the Belgic Confession (1561), and the Canons of Dort (1619) together comprise the Three Forms of Unity governing the URCNA, the Christian Reformed Church, and the continental Reformed tradition.',
     [('Romans 14:7-9', 'If we live, we live to the Lord, and if we die, we die to the Lord'),
      ('1 Corinthians 6:19-20', 'You are not your own, for you were bought with a price')],
     ['catechism', 'belgic-confession', 'dort', 'three-forms-of-unity']),

    ('belgic-confession', 'Belgic Confession', 'noun phrase',
     'A confession of faith written in 1561 by Guido de Brès, defining the faith of the Reformed churches in the Low Countries (modern Belgium and the Netherlands). One of the Three Forms of Unity.',
     'The Belgic Confession of Faith was written in 1561 by Guido de Brès as a defense of the Reformed faith to King Philip II of Spain, who was then persecuting Reformed Christians in the Low Countries. De Brès was martyred in 1567. The confession\'s 37 articles cover the standard Reformed loci — God and Scripture, creation and providence, sin and salvation, the church and sacraments, and the last judgment. Together with the Heidelberg Catechism (1563) and the Canons of Dort (1619), the Belgic Confession forms the Three Forms of Unity, the governing confessional standard of continental Reformed churches including the URCNA, HRC, FRCNA, PRC, and RCUS.',
     [('Romans 1:18-23', 'what can be known about God is plain to them'),
      ('Hebrews 11:1-3', 'By faith we understand that the universe was created by the word of God')],
     ['heidelberg-catechism', 'dort', 'three-forms-of-unity', 'reformed']),

    ('canons-of-dort', 'Canons of Dort', 'noun phrase',
     'The doctrinal pronouncements of the Synod of Dort (1618-19), responding to the Five Articles of the Remonstrance and codifying the so-called five points of Calvinism. One of the Three Forms of Unity.',
     'The Canons of Dort were issued by the Synod of Dort (Dordrecht, Netherlands) meeting from November 1618 to May 1619, in response to the 1610 Remonstrance of the Arminians. The Canons systematically address the five disputed points: unconditional election, particular redemption, total depravity, irresistible grace, and the perseverance of the saints — what later became known by the acronym TULIP. The Synod was the most international Reformed gathering in history, with delegates from England, Scotland, the Palatinate, Hesse, Bremen, Switzerland, Geneva, and the Netherlands. The Canons, the Heidelberg Catechism (1563), and the Belgic Confession (1561) form the Three Forms of Unity that govern continental Reformed churches.',
     [('Romans 9:11-13', 'though they were not yet born and had done nothing either good or bad — in order that God\'s purpose of election might continue'),
      ('John 6:37-39', 'All that the Father gives me will come to me'),
      ('Ephesians 1:4-5', 'he chose us in him before the foundation of the world')],
     ['tulip', 'arminian', 'calvinist', 'belgic-confession', 'heidelberg-catechism']),

    ('new-calvinism', 'New Calvinism', 'noun phrase',
     'A contemporary movement, sometimes called "Young, Restless, Reformed," that recovers Reformed soteriology within broadly evangelical (often non-confessional) ecclesial settings. Associated with figures like John Piper, Mark Dever, Albert Mohler, and Tim Keller.',
     'New Calvinism (or "Young, Restless, Reformed," from Collin Hansen\'s 2008 book of the same name) is a contemporary movement among American evangelicals that recovers the doctrines of grace — total depravity, unconditional election, particular redemption, irresistible grace, and perseverance — while often retaining broadly evangelical (rather than strictly confessional) ecclesial commitments. Leading figures include John Piper, Mark Dever, Albert Mohler, Tim Keller, John MacArthur, and Matt Chandler; key institutional carriers include 9Marks, Together for the Gospel (now ended), The Gospel Coalition, Acts 29, and Founders Ministries. The movement\'s relationship to historic confessional Presbyterianism and Reformed Baptist confessionalism is complicated; some adherents move toward confessional subscription, others remain in broadly evangelical settings.',
     [('Ephesians 2:8-9', 'by grace you have been saved through faith'),
      ('Romans 9:15-16', 'I will have mercy on whom I have mercy')],
     ['calvinist', 'reformed', 'tulip', '9marks', 'tgc']),

    ('imputation-doctrine', 'Imputation', 'noun',
     'From Latin <em>imputare</em> (to reckon, to credit). The doctrine that righteousness or sin can be reckoned to a person\'s account by virtue of representation rather than personal performance.',
     'Imputation is the doctrine that righteousness or sin can be reckoned (credited, charged, accounted) to a person\'s legal standing on the basis of representation. The doctrine grounds three connected Reformed truths: Adam\'s sin is imputed to all his posterity, so that we are guilty in him; the sin of the elect is imputed to Christ on the cross, so that He bore the penalty; and Christ\'s active and passive righteousness is imputed to the believer through faith, so that the believer stands before God reckoned righteous. The doctrine of imputed righteousness is, with sola fide, the central recovery of the Reformation against medieval views of infused righteousness.',
     [('Romans 4:3-6', 'Abraham believed God, and it was counted to him as righteousness'),
      ('2 Corinthians 5:21', 'For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God'),
      ('Romans 5:18-19', 'as one trespass led to condemnation for all men, so one act of righteousness leads to justification')],
     ['justification', 'federal-headship', 'sola-fide', 'penal-substitution']),
]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://usmcmin.org/dictionary/{slug}.html">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_word} &mdash; The MOOP Dictionary</title>
    <meta name="description" content="{display_word}: {short_def}">
    <meta property="og:title" content="{display_word} — The MOOP Dictionary">
    <meta property="og:description" content="{display_word}: {short_def}">
    <meta property="og:image" content="https://usmcmin.org/assets/icons/icon-512.png">
    <meta property="og:url" content="https://usmcmin.org/dictionary/{slug}.html">
    <meta property="og:type" content="article">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{display_word} — The MOOP Dictionary">
    <meta name="twitter:image" content="https://usmcmin.org/assets/icons/icon-512.png">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        :root {{ --bg:#000; --card:#111; --gold:#D4AF37; --gold-light:#F4D470; --white:#FFF; --gray:#888; --border:#333; }}
        body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--white); min-height:100vh; line-height:1.7; }}
        h1,h2,h3,h4 {{ font-family:'Playfair Display',serif; }}
        nav {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 8px; padding:10px 16px; border-bottom:1px solid var(--border); position:sticky; top:0; background:rgba(0,0,0,0.95); backdrop-filter:blur(8px); z-index:100; }}
        nav a {{ color:var(--gray); text-decoration:none; font-size:0.8rem; padding:3px 6px; }}
        nav a:hover, nav a.active {{ color:var(--gold); }}
        .container {{ max-width:820px; margin:0 auto; padding:28px 20px 60px; }}
        .word-header {{ text-align:center; padding:40px 0 30px; border-bottom:1px solid var(--border); margin-bottom:30px; }}
        .word-title {{ font-size:2.6rem; color:var(--gold-light); margin-bottom:6px; }}
        .pos {{ display:inline-block; background:var(--gold); color:#000; font-weight:700; font-size:0.78rem; padding:3px 14px; border-radius:15px; margin:10px 0; }}
        .etymology {{ color:var(--gray); font-size:0.92rem; margin:14px auto; max-width:650px; }}
        .section {{ margin:18px 0; padding:18px 22px; background:var(--card); border:1px solid var(--border); border-radius:10px; }}
        .section > h3 {{ color:var(--gold); margin-bottom:12px; font-size:1.05rem; }}
        .section p {{ margin:7px 0; color:#c9d1d9; }}
        .biblical-def {{ border-left:3px solid var(--gold); padding-left:15px; }}
        .verse-ref {{ color:var(--gold); text-decoration:none; font-weight:600; }}
        .verse-ref:hover {{ color:var(--gold-light); text-decoration:underline; }}
        .related {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }}
        .related a {{ background:var(--card); border:1px solid var(--border); padding:6px 14px; border-radius:20px; color:var(--white); text-decoration:none; font-size:0.85rem; }}
        .related a:hover {{ border-color:var(--gold); color:var(--gold); }}
        footer {{ text-align:center; padding:28px 20px; border-top:1px solid var(--border); margin-top:40px; color:var(--gray); font-size:0.85rem; }}
        footer a {{ color:var(--gold); text-decoration:none; }}
        .dict-back-nav {{ display:flex; align-items:center; justify-content:center; margin-bottom:22px; padding:10px 0; border-bottom:1px solid var(--border); }}
        .dict-back-nav a {{ color:var(--gold); text-decoration:none; font-size:0.88rem; }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
<nav>
    <a href="../index.html">&larr; Home</a>
    <a href="index.html" class="active">Dictionary</a>
    <a href="../blog.html">Blog</a>
    <a href="../churches.html">Churches</a>
</nav>
<div class="container">
    <div class="dict-back-nav"><a href="index.html">&larr; Back to Dictionary</a></div>
    <div class="word-header">
        <div class="word-title">{display_word}</div>
        <span class="pos">{pos}</span>
        <div class="etymology">{etymology}</div>
    </div>
    <div class="section">
        <h3>&#128214; Biblical Definition</h3>
        <div class="biblical-def">
            <p>{definition}</p>
        </div>
    </div>
    <div class="section">
        <h3>&#128214; Key Scripture</h3>
        {scripture_html}
    </div>
    {related_html}
</div>
<footer>
    <p>The MOOP Dictionary &middot; A growing reference of biblical and Reformed terminology.</p>
    <p style="margin-top:8px;font-size:0.78rem;color:#666;">Stub entry &mdash; this term was added to support cross-linking in the editorial essays. Fuller treatment forthcoming.</p>
</footer>
</body>
</html>
"""


def short_def(definition):
    """First sentence of the definition, capped at ~160 chars for meta tags."""
    first = re.split(r'(?<=[.!?])\s+', definition)[0]
    if len(first) > 200:
        first = first[:197] + '...'
    return first.replace('"', "'").replace('<em>', '').replace('</em>', '').replace('<strong>', '').replace('</strong>', '')


def render_scripture(refs):
    parts = []
    for ref, text in refs:
        parts.append(
            f'<p>&#x2022; <a href="../bible.html?ref={ref.replace(" ", "+")}" class="verse-ref">{ref}</a> &mdash; "{text}"</p>'
        )
    return '\n        '.join(parts)


def render_related(related_slugs):
    if not related_slugs:
        return ''
    links = []
    for s in related_slugs:
        # Check if the page exists or is being created in this batch; either way emit a link
        label = s.replace('-', ' ').title()
        links.append(f'<a href="{s}.html">{label}</a>')
    return (
        '<div class="section">\n'
        '        <h3>Related</h3>\n'
        '        <div class="related">' + ''.join(links) + '</div>\n'
        '    </div>'
    )


def main():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    tokens = manifest.setdefault('tokens', {})

    created = 0
    skipped = 0
    added_tokens = 0

    for slug, display, pos, etym, defn, scripture, related in ENTRIES:
        page_path = DICT_DIR / f'{slug}.html'
        # Pick the primary lookup word (lowercase, first word)
        primary_token = display.split()[0].lower()
        if page_path.exists():
            print(f'  exists, skipping: {slug}.html')
            skipped += 1
        else:
            html = PAGE_TEMPLATE.format(
                slug=slug,
                display_word=display,
                short_def=short_def(defn),
                pos=pos,
                etymology=etym,
                definition=defn,
                scripture_html=render_scripture(scripture),
                related_html=render_related(related),
            )
            page_path.write_text(html, encoding='utf-8')
            print(f'  created: {slug}.html')
            created += 1

        # Add token mapping if not already there
        if primary_token not in tokens:
            tokens[primary_token] = slug
            added_tokens += 1

    # Also write the cleaned-up manifest
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    print()
    print(f'Created pages:   {created}')
    print(f'Already existed: {skipped}')
    print(f'New tokens added to manifest: {added_tokens}')
    print(f'Total manifest tokens now: {len(tokens)}')


if __name__ == '__main__':
    main()
