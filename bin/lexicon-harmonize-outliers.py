#!/usr/bin/env python3
"""Same lexicon harmonisation for the 23 pages whose CSS is minified, plus hide the duplicate
legacy theme button on the 47 pages that carry two toggles in the nav. (CID MBP-1004-CRAWL)"""
import re,glob,collections
R=[
 (r'\.container\{max-width:800px;margin:0 auto;padding:20px;?\}', '.container{max-width:820px;margin:0 auto;padding:28px 20px 60px}'),
 (r'(nav a\{color:var\(--gray\);text-decoration:none;font-size:0?\.85rem;font-weight:500;padding:5px 12px;border-radius:20px;border:1px solid transparent;transition:all 0?\.2s(?:;white-space:nowrap)?);?\}',
  r'\1;display:inline-flex;align-items:center;gap:4px}.site-icon{vertical-align:middle;opacity:.8}@media (max-width:640px){nav{gap:4px 6px;padding:10px 12px}nav a{padding:3px 7px;font-size:.8rem}}'),
 (r'\.section\{background:var\(--bg-card\);border:1px solid var\(--border\);border-radius:12px;padding:28px;margin-bottom:24px;?\}',
  '.section{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:18px 22px;margin:18px 0}.section p a:not([class]){color:var(--gold)}'),
 (r'\.section h2\{color:var\(--gold\);font-size:1\.3rem;margin-bottom:16px;?\}', '.section h2{color:var(--gold);font-size:1.15rem;margin-bottom:12px}'),
 (r'(\.verse-ref\{color:var\(--gold\);text-decoration:none;font-weight:600;font-size:0?\.9rem;display:inline-block;margin-bottom:4px);border-bottom:1px dotted var\(--gold\);?\}', r'\1}'),
 (r'\.verse-ref:hover\{color:var\(--gold-light\);border-bottom-style:solid;?\}', '.verse-ref:hover{color:var(--gold-light);text-decoration:underline}'),
 (r'\.back-link\{display:inline-block;color:var\(--gold\);text-decoration:none;margin-bottom:20px;font-size:0?\.9rem;?\}',
  '.back-link{display:block;text-align:center;color:var(--gold);text-decoration:none;margin-bottom:22px;padding:10px 0;border-bottom:1px solid var(--border);font-size:.88rem;font-weight:500}'),
 (r'(@media\s*\(max-width:640px\)\s*\{)\.container\{padding:15px;?\}', r'\1'),
]
st=collections.Counter()
for p in sorted(glob.glob('lexicon/*.html')):
    s=open(p,encoding='utf-8').read(); o=s
    if 'http-equiv="refresh"' in s: continue
    if 'padding:18px 22px' not in s:
        for i,(a,b) in enumerate(R):
            s,n=re.subn(a,b,s,count=1); st['r%d'%i]+=n
        if 'nav a.active' not in s:
            s=s.replace('.site-icon{vertical-align:middle;opacity:.8}','.site-icon{vertical-align:middle;opacity:.8}nav a.active{color:var(--gold)!important;border-color:var(--gold)}',1); st['active']+=1
    if '<button class="theme-toggle" id="themeToggle"' in s and 'bte-theme-toggle nav-theme-toggle' in s and 'nav button.theme-toggle{display:none' not in s:
        i=s.find('</style>'); s=s[:i]+'nav button.theme-toggle{display:none !important;}'+s[i:]; st['dupToggle']+=1
    if s!=o: open(p,'w',encoding='utf-8').write(s); st['files']+=1
print(dict(st))
