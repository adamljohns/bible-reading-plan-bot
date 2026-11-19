"""Main-body text of an HTML page, for denomination evidence checking.

The quote check must match against what the document itself says, not the
site chrome. This keeps only the main content region (<main>, else
role="main", else <article>, else <body>) and drops every nav, header,
footer, aside, form and banner/navigation/contentinfo landmark inside it,
plus script/style/svg/noscript/template. Pure stdlib; no model.
"""
import re
from html.parser import HTMLParser

SKIP_TAGS = {"nav", "header", "footer", "aside", "form", "script", "style", "svg", "noscript", "template", "head"}
SKIP_ROLES = {"navigation", "banner", "contentinfo", "complementary", "search"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class _Probe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.found.add("main")
        if (a.get("role") or "").lower() == "main":
            self.found.add("role")
        if tag == "article":
            self.found.add("article")


class _Body(HTMLParser):
    def __init__(self, region):
        super().__init__()
        self.region = region  # callable(tag, attrs) -> bool
        self.in_region = 0
        self.region_tag = None
        self.skip_tag = None
        self.skip_depth = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth += 1
            return
        if not self.in_region:
            if self.region(tag, a):
                self.in_region, self.region_tag = 1, tag
            return
        if tag == self.region_tag:
            self.in_region += 1
        if tag in SKIP_TAGS or (a.get("role") or "").lower() in SKIP_ROLES:
            self.skip_tag, self.skip_depth = tag, 1
            return
        self.out.append(" ")

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth == 0:
                    self.skip_tag = None
            return
        if self.in_region and tag == self.region_tag:
            self.in_region -= 1
        self.out.append(" ")

    def handle_data(self, data):
        if self.in_region and not self.skip_tag:
            self.out.append(data)


def body_text(raw):
    p = _Probe()
    p.feed(raw)
    if "main" in p.found:
        region, kind = (lambda t, a: t == "main"), "main"
    elif "role" in p.found:
        region, kind = (lambda t, a: (a.get("role") or "").lower() == "main"), 'role="main"'
    elif "article" in p.found:
        region, kind = (lambda t, a: t == "article"), "article"
    else:
        region, kind = (lambda t, a: t == "body"), "body"
    b = _Body(region)
    b.feed(raw)
    return re.sub(r"\s+", " ", "".join(b.out)).strip(), kind
