#!/usr/bin/env python3
"""One-off: build the 'The Word, Closer to Hand' blog post page from the site's
existing post template, and register it in blog.html's WP_POSTS listing."""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
TEMPLATE = os.path.join(DOCS, "blog", "resolute-citizen-7580-candidates-all-50-states-one-standard.html")
SLUG = "the-word-closer-to-hand"
URL = f"https://usmcmin.org/blog/{SLUG}.html"
TITLE = "The Word, Closer to Hand"
DESC = ("How we're making Scripture, the MOOP Dictionary, and sound doctrine easier to reach "
        "— an installable site, an offline dictionary, and a phone app on the way.")

CONTENT = """    <div class="meta"><a href="/blog.html">&larr; Blog</a> &nbsp;&middot;&nbsp; Spiritual Formation</div>
    <h1>The Word, Closer to Hand</h1>
    <div class="byline">By <strong>Adam &ldquo;MOOP&rdquo; Johns</strong> &nbsp;&middot;&nbsp; U.S.M.C. Ministries &nbsp;&middot;&nbsp; Published May 30, 2026</div>

    <p>There is a quiet conviction beneath everything we do at U.S.M.C. Ministries — that the men we're called to serve are rarely lacking in hunger so much as in access, and that the Word, together with the sound doctrine handed down to us, ought to be near, ready, and unburdened by the friction of clumsy tools. A man reaching for Scripture late on a Tuesday night, or a father wanting to settle what a word <em>actually</em> means before he teaches it to his children, should not have to fight his phone or his laptop to get there. So over the past few days we've done some quiet building — not the kind of work that announces itself with fanfare, but the kind that simply makes the well easier to draw from.</p>

    <p>The first piece is the dictionary. You may already know the MOOP Dictionary — our growing labor of nearly five thousand entries, where every word is weighed not only by its modern usage but by its biblical meaning, its Webster's 1828 definition, its Greek and Hebrew roots, and, where it matters most, by an honest reckoning with how our age has bent and hollowed out plain language. Words like <em>truth</em>, <em>love</em>, <em>justice</em>, and <em>tolerance</em> have been quietly redefined out from under us, and a man who cannot say what a word means will struggle to stand on what it teaches. That dictionary now reaches further than ever — it lives online, searchable and open to anyone, and it has been woven into the very tools we use every day, so that looking up a word is no longer a chore but a reflex.</p>

    <p>The second piece is perhaps the one you'll feel most. Our home on the web, usmcmin.org, can now be <em>installed</em> — added to the home screen of your phone or the dock of your computer, where it opens like any other app, full-screen and unhurried, without the clutter of a browser. And here is the part that matters for the man in the deer stand, the truck cab, or the hospital waiting room where the signal is thin: once you've opened a passage or an entry, it stays with you. The Bible reader and the dictionary keep working even when the bars run out. The Word, it turns out, was never meant to depend on a strong connection — and now, in a small and practical way, it doesn't have to.</p>

    <p>There is more taking shape behind the curtain. A dedicated app for the iPhone is now under construction — one home for the daily reading, the Bible, the dictionary, and the rest of what we publish, built in the same spirit of order and reverence that we hope marks the whole ministry. And beneath all of it we've begun laying the quiet plumbing that lets your place in a reading plan follow you from one device to the next, so that the discipline you've kept on your phone in the morning is waiting for you on your laptop that evening. None of this is finished, and we're in no hurry to rush it — but the foundation is poured, and it is good.</p>

    <p>I want to be plain about <em>why</em> we bother with any of this, because it would be easy to mistake it for a fascination with gadgets. It is not. We are stewards — of time, of attention, of the means God has placed in our hands — and in this generation a great deal of a man's attention is captured, for better or worse, by the screen he carries in his pocket. We would rather that screen be a doorway to Scripture and sound teaching than one more corridor of noise. Every bit of friction we remove between a man and the Word is friction that won't talk him out of opening it. That is the whole of it. The tools are not the point; the tools are the scaffolding around the point.</p>

    <p>So consider this a small invitation. Visit usmcmin.org, and if it suits you, add it to your home screen and carry it with you. Search a word you thought you understood and see whether Scripture and history have more to say about it than the culture does. And pray with us that these ordinary instruments — a dictionary, a reading plan, an app — would be bent, like everything else here, toward the one end that gives them any worth at all: that men would know the Truth, and that the Truth would set them free.</p>

    <blockquote><p>&ldquo;Your word is a lamp to my feet and a light to my path.&rdquo; &mdash; Psalm 119:105</p></blockquote>
"""

def main():
    h = open(TEMPLATE, encoding="utf-8").read()
    h = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{URL}">', h, count=1)
    h = re.sub(r'<title>.*?</title>', f'<title>{TITLE} &mdash; U.S.M.C. Ministries</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta property="og:title"[^>]*>', f'<meta property="og:title" content="{TITLE}">', h, count=1)
    h = re.sub(r'<meta property="og:description"[^>]*>', f'<meta property="og:description" content="{DESC}">', h, count=1)
    h = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{URL}">', h, count=1)
    h = re.sub(r'<meta property="og:image"[^>]*>', '<meta property="og:image" content="https://usmcmin.org/assets/usmc-ministries-full-crest.png">', h, count=1)
    h = re.sub(r'<meta name="article:modified_time"[^>]*>', '<meta name="article:modified_time" content="2026-05-30">', h, count=1)
    # drop the hero image + caption (this post has none)
    h = re.sub(r'\s*<img class="hero-img"[^>]*>', '', h, count=1)
    h = re.sub(r'\s*<div class="img-caption">.*?</div>', '', h, count=1, flags=re.S)
    # swap the article body
    h = re.sub(r'(<article class="article">).*?(</article>)',
               lambda m: m.group(1) + "\n" + CONTENT + "\n" + m.group(2), h, count=1, flags=re.S)
    out = os.path.join(DOCS, "blog", f"{SLUG}.html")
    open(out, "w", encoding="utf-8").write(h)
    print("wrote", out, len(h), "bytes")

    # register in blog.html WP_POSTS (prepend, newest first)
    bp_path = os.path.join(DOCS, "blog.html")
    bp = open(bp_path, encoding="utf-8").read()
    if SLUG in bp:
        print("already registered in blog.html")
        return
    entry = ('{"title":"The Word, Closer to Hand","date":"May 30, 2026",'
             f'"url":"blog/{SLUG}.html",'
             '"excerpt":"What began as simply wanting a dictionary definition turned into something bigger: '
             'the MOOP Dictionary searchable everywhere, usmcmin.org installable and usable offline, and a '
             'phone app on the way. A reflection on removing every bit of friction between a man and the Word.",'
             '"cat":"Spiritual Formation"},')
    bp2 = bp.replace("const WP_POSTS = [", "const WP_POSTS = [" + entry, 1)
    if bp2 == bp:
        print("WARNING: WP_POSTS anchor not found — blog.html not updated")
    else:
        open(bp_path, "w", encoding="utf-8").write(bp2)
        print("registered in blog.html")

if __name__ == "__main__":
    main()
