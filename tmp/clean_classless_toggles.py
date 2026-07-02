#!/usr/bin/env python3
"""Remove the 46 residual classless footer toggle wrappers (matched-div, balance-neutral)."""
import glob, re, sys
APPLY="--apply" in sys.argv
DIV_TOK=re.compile(r'<div\b[^>]*>|</div>')
def div_end(s,start):
    depth=0
    for m in DIV_TOK.finditer(s,start):
        if m.group().startswith("</div"):
            depth-=1
            if depth==0: return m.end()
        else: depth+=1
    return -1
def bal(s):
    b=s[s.find("<body"):s.rfind("</body>")]
    return len(re.findall(r"<div\b",b))-len(re.findall(r"</div>",b))
# wrapper containing a classless onclick toggle that writes bte-theme
WRAP=re.compile(r'<div style="text-align:center;margin:\d+px auto[^"]*">')
n=0; wrote=0
for f in glob.glob("docs/lexicon/*.html"):
    s=open(f,encoding="utf-8").read()
    if "width:28px;height:14px;background:#444" not in s: continue
    orig=s; b0=bal(s)
    for m in list(WRAP.finditer(s)):
        end=div_end(s,m.start())
        if end==-1: continue
        block=s[m.start():end]
        # only remove if this wrapper is a dead toggle (has the toggle onclick / dot, NO nav-theme-toggle, NO real content)
        if "localStorage.setItem('bte-theme'" in block and "nav-theme-toggle" not in block:
            txt=re.sub(r"<[^>]+>","",block)
            assert txt.strip()=="" , f"{f}: wrapper had text {txt!r}"
            s=s[:m.start()]+s[end:]
    if s!=orig:
        assert bal(s)==b0, f"{f}: balance changed {b0}->{bal(s)}"
        assert "width:28px;height:14px;background:#444" not in s, f"{f}: dot div survived"
        n+=1
        if APPLY: open(f,"w",encoding="utf-8").write(s); wrote+=1
print(f"pages with classless footer toggle cleaned: {n} (wrote {wrote})" if APPLY else f"would clean {n}")
