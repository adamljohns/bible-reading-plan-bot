#!/usr/bin/env python3
"""Dictionary 'Related Words': words whose link was stripped (2b14d846933, 2026-05-16) were left as bare
text jammed between the chips. Wrap each in a plain (unlinked) chip. Word boundaries come from the labels
the page carried before that commit - never guessed. (CID MBP-1004-CRAWL)"""
import re,glob,subprocess,sys,html,collections
APPLY='--apply' in sys.argv
SPAN='<span class="related-plain" style="background:var(--card);border:1px dashed var(--border);padding:6px 14px;border-radius:20px;color:var(--gray);font-size:0.85rem;">'
p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
def old(path):
    p.stdin.write(('2b14d846933^:'+path+'\n').encode()); p.stdin.flush()
    hdr=p.stdout.readline().split()
    if hdr[-1]==b'missing': return None
    n=int(hdr[2]); d=p.stdout.read(n); p.stdout.read(1); return d.decode('utf-8','replace')
REL=re.compile(r'(<div class="related">)(.*?)(</div>)',re.S)
TOK=re.compile(r'(<a\b[^>]*>.*?</a>|<span\b[^>]*>.*?</span>|<!--.*?-->)',re.S)
def norm(t): return html.unescape(t).strip()
def segment(run, labels):
    """split run into known labels, longest-first, must consume everything"""
    run=run.strip(); out=[]
    labs=sorted(set(labels),key=len,reverse=True)
    def rec(s):
        if not s: return []
        for l in labs:
            if l and s.startswith(l):
                r=rec(s[len(l):].lstrip())
                if r is not None: return [l]+r
        return None
    return rec(run)
st=collections.Counter(); unresolved=[]
for path in sorted(glob.glob('docs/dictionary/*.html')):
    s=open(path,encoding='utf-8').read()
    if '<div class="related">' not in s or 'http-equiv="refresh"' in s: continue
    o=None; changed=False
    def fix(m):
        global o,changed
        parts=TOK.split(m.group(2)); newparts=[]; 
        for i,part in enumerate(parts):
            if i%2==1 or not part.strip() or '<' in part: newparts.append(part); continue
            if o is None: o=old(path) or ''
            labels=[re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'<a\b[^>]*>(.*?)</a>',''.join(mm.group(2) for mm in REL.finditer(o)),re.S)]
            seg=segment(part,labels)
            if seg is None:
                # single word run with no internal ambiguity is still unknown -> leave
                st['runs_unresolved']+=1; unresolved.append((path,part.strip()[:70])); newparts.append(part); continue
            lead=part[:len(part)-len(part.lstrip())]; trail=part[len(part.rstrip()):]
            newparts.append(lead+''.join(SPAN+x+'</span>' for x in seg)+trail); st['runs_fixed']+=1; st['chips']+=len(seg); changed=True
        return m.group(1)+''.join(newparts)+m.group(3)
    t=REL.sub(fix,s)
    if changed:
        st['pages']+=1
        if APPLY: open(path,'w',encoding='utf-8').write(t)
print(dict(st)); print('unresolved sample',unresolved[:12])
