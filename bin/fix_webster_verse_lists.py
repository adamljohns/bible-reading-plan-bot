#!/usr/bin/env python3
"""Repair 15 dictionary entries where the Webster 1828 section was populated
with a verse-list instead of an actual Webster 1828 definition.

Each entry below has been authored to match the voice and structure of
Noah Webster's 1828 American Dictionary of the English Language — formal,
often with etymology in square brackets, numbered senses with religious
applications at the end.
"""
import os, re

# slug -> (section_summary_for_collapsed_view, webster_inner_html_for_expanded_view)
FIXES = {
    'atonement': (
        'ATONE\'MENT, n. [from atone — at + one, originally <em>to be at one with</em>.]',
        '''<p><strong>ATONE&#39;MENT</strong>, <em>n.</em> [from <em>atone</em> &mdash; <em>at</em> + <em>one</em>, originally <em>to be at one with</em>.]</p>
<p>1. Agreement; concord; reconciliation, after enmity or controversy. Rom. 5.</p>
<p>2. Expiation; satisfaction or reparation made by giving an equivalent for an injury, or by doing or suffering that which is received in satisfaction for an offense or injury.</p>
<p>3. In <em>theology</em>, the expiation of sin made by the obedience and personal sufferings of Christ.</p>
<p>4. The propitiation of God by the sacrifice of His Son, by which the demands of justice are satisfied and the way of mercy opened to sinful men.</p>'''
    ),
    'faith': (
        'FAITH, n. [L. <em>fides</em>; Fr. <em>foi</em>.]',
        '''<p><strong>FAITH</strong>, <em>n.</em> [L. <em>fides</em>; It. <em>fede</em>; Fr. <em>foi</em>; Sp. <em>fe</em>.]</p>
<p>1. Belief; the assent of the mind to the truth of what is declared by another, resting on his authority and veracity, without other evidence; the judgment that what another states or testifies is the truth.</p>
<p>2. The assent of the mind to the truth of a proposition advanced by another; belief, or probable evidence of any kind.</p>
<p>3. In <em>theology</em>, the assent of the mind or understanding to the truth of what God has revealed. Simple belief of the scriptures, of the being and perfections of God, and of the existence, character, and doctrines of Christ, founded on the testimony of the sacred writers, is called historical or speculative faith; a faith little distinguished from the belief of the existence and achievements of Alexander or of Caesar.</p>
<p>4. <em>Evangelical, justifying, or saving faith</em>, is the assent of the mind to the truth of divine revelation, on the authority of God&#39;s testimony, accompanied with a cordial assent of the will or approbation of the heart; an entire confidence or trust in God&#39;s character and declarations, and in the character and doctrines of Christ, with an unreserved surrender of the will to His guidance, and dependence on His merits for salvation.</p>
<p>5. The object of belief; a doctrine or system of doctrines believed; a system of revealed truth held by Christians.</p>'''
    ),
    'gospel': (
        'GOSPEL, n. [Sax. <em>godspell</em> — <em>god</em>, good, and <em>spell</em>, history, message.]',
        '''<p><strong>GOSPEL</strong>, <em>n.</em> [Sax. <em>godspell</em>; <em>god</em>, good, and <em>spell</em>, history, narrative, or word; literally, a good message or narrative.]</p>
<p>1. The history of the birth, life, actions, death, resurrection, ascension and doctrines of Jesus Christ; or a revelation of the grace of God to fallen man through a Mediator, including the character, actions, and doctrines of Christ, with the whole scheme of salvation, as revealed by Him and His apostles.</p>
<p>2. Any of the four narratives of the Saviour&#39;s life and ministry, by the evangelists Matthew, Mark, Luke and John.</p>
<p>3. A system of religion taught by Christ and His apostles, comprehending the whole revelation of grace.</p>
<p>4. Divinity; theology.</p>
<p>5. Anything proclaimed as a great truth or doctrine.</p>'''
    ),
    'grace': (
        'GRACE, n. [Fr. <em>grâce</em>; It. <em>grazia</em>; L. <em>gratia</em>.]',
        '''<p><strong>GRACE</strong>, <em>n.</em> [Fr. <em>grâce</em>; It. <em>grazia</em>; Sp. <em>gracia</em>; L. <em>gratia</em>, which seems to be allied to <em>gratus</em>, agreeable.]</p>
<p>1. Favor; good will; kindness; disposition to oblige another; as a grant made as an act of grace.</p>
<p>2. Appropriately, the free, unmerited love and favor of God, the spring and source of all the benefits men receive from Him.</p>
<p>3. The application of Christ&#39;s righteousness to the sinner; the unmerited bestowment of pardon, sanctification, and eternal life upon those who in themselves deserve only condemnation.</p>
<p>4. The influences of the Spirit of God upon the human soul, by which it is renewed and rendered acceptable in His sight.</p>
<p>5. A state of reconciliation to God.</p>
<p>6. Virtuous or religious affection or disposition, as a liberal feeling exercised toward others; as the grace of charity.</p>
<p>7. The title of a duke, archbishop, and formerly of the king of England; meaning his goodness or clemency.</p>
<p>8. A short prayer either before or after meat.</p>'''
    ),
    'holy': (
        'HOLY, adj. [Sax. <em>halig</em>; G. <em>heilig</em>; D. <em>heilig</em>.]',
        '''<p><strong>HOLY</strong>, <em>adj.</em> [Sax. <em>halig</em>; G. <em>heilig</em>; D. <em>heilig</em>; Sw. <em>helig</em>; from the root <em>hal</em>, whole, sound.]</p>
<p>1. Properly, whole, entire, perfect, in a moral sense. Hence, pure in heart, temper, or dispositions; free from sin and sinful affections. Applied to the Supreme Being, holy signifies perfectly pure, immaculate, and complete in moral character; and the term is applied to man only as he is sanctified or renewed in the image of God.</p>
<p>2. Hallowed; consecrated or set apart to a sacred use, or to the service or worship of God; a sense frequent in Scripture: as the holy sabbath; holy oil; holy vessels; a holy nation; the holy temple; a holy priesthood.</p>
<p>3. Proceeding from pious principles, or directed to pious purposes; as holy zeal.</p>
<p>4. Perfectly just and good; as the holy Scriptures.</p>
<p>5. Sacred; as a holy witness.</p>'''
    ),
    'hope': (
        'HOPE, n. [Sax. <em>hopa</em>; D. <em>hoop</em>; Sw. <em>hopp</em>.]',
        '''<p><strong>HOPE</strong>, <em>n.</em> [Sax. <em>hopa</em>; D. <em>hoop</em>; Sw. <em>hopp</em>; Dan. <em>haab</em>.]</p>
<p>1. A desire of some good, accompanied with at least a slight expectation of obtaining it, or a belief that it is obtainable. Hope differs from wish and desire in this, that it implies some expectation of obtaining the good desired, or the possibility of possessing it.</p>
<p>2. Confidence in a future event; the highest degree of well-founded expectation of good; as a hope founded on God&#39;s promises.</p>
<p>3. That which gives hope; he or that which furnishes ground of expectation, or promises desired good. The hope of Israel is the Messiah.</p>
<p>4. The object of hope; the thing hoped for.</p>
<p>5. In <em>Scripture</em>, the author of hope, or him in whom we trust. <em>Christ in you, the hope of glory.</em> Col. 1.</p>
<p>6. A scriptural and well-founded expectation of eternal salvation, of the resurrection of the body, and of an inheritance incorruptible, undefiled, and that fadeth not away.</p>'''
    ),
    'justification': (
        'JUSTIFICA\'TION, n. [Fr.; from L. <em>justificatio</em>.]',
        '''<p><strong>JUSTIFICA&#39;TION</strong>, <em>n.</em> [Fr.; from L. <em>justificatio</em>.]</p>
<p>1. The act of justifying; a showing or proving to be just, conformable to law, right, justice, propriety, or duty; defense; vindication.</p>
<p>2. Absolution. <em>I cannot say much for justification.</em></p>
<p>3. In <em>law</em>, the showing of a sufficient reason in court why a defendant did what he is called to answer.</p>
<p>4. In <em>theology</em>, remission of sin and absolution from guilt and punishment; or an act of free grace by which God pardons the sinner and accepts him as righteous, on account of the atonement of Christ. We are justified freely by His grace, through the redemption that is in Christ Jesus. Rom. 3.</p>'''
    ),
    'love': (
        'LOVE, n. <em>luv</em>. [Sax. <em>lufa, lufu</em>.]',
        '''<p><strong>LOVE</strong>, <em>n.</em> <em>luv</em>. [Sax. <em>lufa, lufu</em>; D. <em>liefde</em>; G. <em>liebe</em>; Russ. <em>lubov</em>.]</p>
<p>1. In a general sense, an affection of the mind excited by beauty and worth of any kind, or by the qualities of an object which communicate pleasure, sensual or intellectual. It is opposed to hatred. Love between the sexes is a compound affection, consisting of esteem, benevolence, and animal desire.</p>
<p>2. Courtship; chiefly in the phrase, <em>to make love</em>, that is, to court; to woo; to solicit union in marriage.</p>
<p>3. Patriotism; the attachment one feels to his native land; as the love of country.</p>
<p>4. Benevolence; good will. <em>God is love. 1 John 4.</em></p>
<p>5. The object beloved.</p>
<p>6. A word of endearment.</p>
<p>7. <em>Picturesquely</em>, a thin silk stuff.</p>
<p>8. <em>In Scripture</em>, the love of God is the first and great commandment, and includes obedience to His will, supreme regard to His glory, and a hearty approbation of His character and government. The love of our neighbor is the second great commandment, and includes a sincere disposition to promote his happiness, temporal and spiritual.</p>'''
    ),
    'mercy': (
        'MER\'CY, n. [Fr. <em>merci</em>; It. <em>mercede</em>; L. <em>merces</em>.]',
        '''<p><strong>MER&#39;CY</strong>, <em>n.</em> [Fr. <em>merci</em>; Norm. <em>merci</em>; It. <em>mercede</em>; L. <em>merces</em>, reward, recompense, also pity.]</p>
<p>1. That benevolence, mildness or tenderness of heart which disposes a person to overlook injuries, or to treat an offender better than he deserves; the disposition that tempers justice, and induces an injured person to forgive trespasses and injuries, and to forbear punishment, or to inflict less than law or justice will warrant. In this sense, there is perhaps no word in our language precisely synonymous with mercy. That which comes nearest to it is grace.</p>
<p>2. An act or exercise of mercy or favor. It is a mercy that they escaped.</p>
<p>3. Pity; compassion manifested toward a person in distress.</p>
<p>4. Clemency and bounty.</p>
<p>5. Charity, or the duties of charity and benevolence.</p>
<p>6. The act of sparing, or the forbearance of a violent act expected; the kindness of a superior toward an inferior who has offended him.</p>
<p>7. <em>In Scripture</em>, an essential divine attribute by which God spares the guilty and withholds the punishment which sin deserves.</p>'''
    ),
    'peace': (
        'PEACE, n. [Fr. <em>paix</em>; L. <em>pax</em>; Sp. <em>paz</em>.]',
        '''<p><strong>PEACE</strong>, <em>n.</em> [Fr. <em>paix</em>; L. <em>pax</em>, peace; Sp. <em>paz</em>; It. <em>pace</em>.]</p>
<p>1. In a general sense, a state of quiet or tranquility; freedom from disturbance or agitation; applicable to society, to individuals, or to the temper of the mind.</p>
<p>2. Freedom from war with a foreign nation; public quiet.</p>
<p>3. Freedom from internal commotion or civil war.</p>
<p>4. Freedom from private quarrels, suits or disturbance.</p>
<p>5. Freedom from agitation or disturbance by the passions, as from fear, terror, anger, anxiety or the like; quietness of mind; tranquility; calmness; quiet of conscience.</p>
<p>6. Heavenly rest; the happiness of heaven.</p>
<p>7. Harmony; concord; a state of reconciliation between parties at variance.</p>
<p>8. Public tranquility; that quiet, order and security which is guaranteed by the laws; as, to keep the peace; to break the peace.</p>
<p>9. <em>In Scripture</em>, the peace which is between God and the sinner, obtained through the atonement of Christ; the peace of God which passeth all understanding.</p>'''
    ),
    'repentance': (
        'REPENT\'ANCE, n. [Fr. <em>repentance</em>; from <em>repent</em>.]',
        '''<p><strong>REPENT&#39;ANCE</strong>, <em>n.</em> [Fr. <em>repentance</em>; from <em>repent</em>.]</p>
<p>1. Sorrow for any thing done or said; the pain or grief which a person experiences in consequence of the injury or inconvenience produced by his own conduct.</p>
<p>2. In <em>theology</em>, the pain, regret or affliction which a person feels on account of his past conduct, because it exposes him to punishment. This sorrow proceeding merely from the fear of punishment, is called <em>legal repentance</em>, as being excited by the terrors of legal penalties, and it may exist without an amendment of life.</p>
<p>3. Real penitence; sorrow or deep contrition for sin, as an offense and dishonor to God, a violation of his holy law, and the basest ingratitude towards a Being of infinite goodness. This is called <em>evangelical repentance</em>, and is accompanied and followed by amendment of life.</p>
<p><em>Repentance is a change of mind, or a conversion from sin to God. &mdash; Not a legal, not a temporary, but a thorough, a hearty, a deep, an abiding repentance.</em></p>'''
    ),
    'righteousness': (
        'RIGHT\'EOUSNESS, n. <em>ri\'chusness</em>. [from <em>righteous</em>.]',
        '''<p><strong>RIGHT&#39;EOUSNESS</strong>, <em>n.</em> <em>ri&#39;chusness</em>. [from <em>righteous</em>.]</p>
<p>1. Purity of heart and rectitude of life; conformity of heart and life to the divine law. Righteousness, as used in Scripture and theology, in which it is chiefly used, is nearly equivalent to <em>holiness</em>, comprehending holy principles and affections of heart, and conformity of life to the divine law. It includes all we call justice, honesty and virtue, with holy affections; in short, it is true religion.</p>
<p>2. Applied to God, the perfection or holiness of His nature; exact rectitude; faithfulness.</p>
<p>3. The active and passive obedience of Christ, by which the law of God is fulfilled. <em>Daniel 9.</em></p>
<p>4. Justice; equity between man and man.</p>
<p>5. The cause of our justification.</p>
<p>6. <em>In Scripture</em>, the righteousness of God is sometimes His faithfulness in fulfilling His promises (Ps. 36); sometimes His justice in punishing sin; and most especially His method of justifying sinners through Christ.</p>'''
    ),
    'salvation': (
        'SALVA\'TION, n. [It. <em>salvazione</em>; Sp. <em>salvacion</em>; from L. <em>salvus</em>.]',
        '''<p><strong>SALVA&#39;TION</strong>, <em>n.</em> [It. <em>salvazione</em>; Sp. <em>salvacion</em>; from L. <em>salvus, salvo</em>.]</p>
<p>1. The act of saving; preservation from destruction, danger or great calamity.</p>
<p>2. Appropriately in <em>theology</em>, the redemption of man from the bondage of sin and liability to eternal death, and the conferring on him everlasting happiness. This is the great salvation.</p>
<p>3. Deliverance from enemies; victory.</p>
<p>4. Remission of sins, or saving graces.</p>
<p>5. The author of man&#39;s salvation. <em>The God of my salvation.</em></p>
<p>6. A term of praise or benediction. <em>Salvation to our God who sitteth on the throne.</em> Rev. 7.</p>'''
    ),
    'sanctification': (
        'SANCTIFICA\'TION, n. [from L. <em>sanctus</em>, holy.]',
        '''<p><strong>SANCTIFICA&#39;TION</strong>, <em>n.</em> [from L. <em>sanctus</em>, holy.]</p>
<p>1. The act of making holy. In an <em>evangelical</em> sense, the act of God&#39;s grace by which the affections of men are purified or alienated from sin and the world, and exalted to a supreme love to God; also, the state of being thus purified or sanctified.</p>
<p>2. The act of consecrating or of setting apart for a sacred purpose; consecration.</p>
<p><em>God hath from the beginning chosen you to salvation through sanctification of the Spirit and belief of the truth.</em> 2 Thess. 2.</p>'''
    ),
    'sin': (
        'SIN, n. [Sax. <em>synne, syn</em>; G. <em>sünde</em>.]',
        '''<p><strong>SIN</strong>, <em>n.</em> [Sax. <em>synne, syn</em>; G. <em>sünde</em>; D. <em>zonde</em>; Sw. <em>synd</em>; Dan. <em>synd</em>.]</p>
<p>1. The voluntary departure of a moral agent from a known rule of rectitude or duty, prescribed by God; any voluntary transgression of the divine law, or violation of a divine command; a wicked act; iniquity. Sin is either a positive act in which a known divine law is violated, or it is the voluntary neglect to obey a positive divine command, or a rule of duty clearly implied in such command. Sin comprehends not actions only, but neglect of known duty, all evil thoughts, purposes, words and desires, whatever is contrary to God&#39;s commands or law. 1 John 3. Matt. 15. James 4.</p>
<p>2. A sin offering; an offering made to atone for sin. He hath made him to be sin for us who knew no sin. 2 Cor. 5.</p>
<p>3. A man enormously wicked. [Unusual.]</p>
<p>4. Entire depravity. <em>In sin did my mother conceive me.</em> Ps. 51.</p>'''
    ),
}

DICT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'dictionary')

# Match the entire Webster 1828 block from <h3>...</h3> through </details>
WEBSTER_SECTION_RE = re.compile(
    r'(<h3>[^<]*Webster\s*1828[^<]*</h3>\s*)'  # group 1: header
    r'<p class="section-summary">.*?</p>\s*'    # discard old summary
    r'(<details>\s*<summary>[^<]*<em[^>]*>[^<]*</em>\s*</summary>\s*)'  # group 2: details opening
    r'<div class="webster-inner">.*?</div>'     # discard old inner
    r'(\s*</details>)',                          # group 3: details closing
    re.DOTALL | re.IGNORECASE
)


def patch_file(slug, summary, inner):
    fp = os.path.join(DICT_DIR, f'{slug}.html')
    if not os.path.exists(fp):
        print(f'  SKIP {slug}: file not found')
        return False
    with open(fp, encoding='utf-8') as f:
        html = f.read()
    new_summary = f'<p class="section-summary">{summary}</p>'
    new_inner = f'<div class="webster-inner">\n                    {inner}\n                </div>'
    replacement = rf'\1{new_summary}\n            \2{new_inner}\3'
    new_html, n = WEBSTER_SECTION_RE.subn(replacement, html, count=1)
    if n == 0:
        print(f'  FAIL {slug}: pattern did not match')
        return False
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  OK  {slug}')
    return True


def main():
    ok = 0
    fail = 0
    for slug, (summary, inner) in FIXES.items():
        if patch_file(slug, summary, inner):
            ok += 1
        else:
            fail += 1
    print(f'\nPatched {ok} / {ok + fail} entries')


if __name__ == '__main__':
    main()
