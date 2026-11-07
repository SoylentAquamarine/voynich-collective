#!/usr/bin/env python3
"""Coarse-cell (4x2x3) common-support glyph contrast with pool>=2x need and >=5 distinct types per glyph; coverage stop rule 0.50.
Precommitment: logs/2026-11-07-line-final-m-coarse-cell-glyph-selfreview.md. Loader copied from line_final_m_common_support_glyph.py."""

import json, random, re, statistics as st
from collections import defaultdict

def page_meta():
    meta = {}
    for ln in open('data/ZL3b-n.txt', encoding='utf-8'):
        m = re.match(r'^<(f[^.>]+)>\s+<!\s+(.*)>', ln)
        if m and m.group(1) not in meta:
            meta[m.group(1)] = dict(re.findall(r'\$([A-Z])=(\S+)', m.group(2)))
    return meta

def load_zl():
    d = {}
    for ln in open('data/derived/ZL3b-normalized.txt', encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln:
            k, t = ln.split('\t', 1); d[k] = t.split()
    return d

def load_rf():
    d = {}
    for ln in open('data/RF1b-e.txt', encoding='utf-8'):
        if ln.startswith('#') or not ln.strip(): continue
        m = re.match(r'<([^>]+)>\s+(.*)$', ln.rstrip('\n'))
        if not m or ',' not in m.group(1): continue
        t = re.sub(r'@\d+;', '?', m.group(2)); t = re.sub(r'\{[^}]*\}', '', t)
        t = re.sub(r'<[^>]*>', '', t).replace(',', '.')
        d[m.group(1)] = [w for w in t.replace('-', '.').split('.') if w]
    return d




import statistics as st
def fbin(c): return 0 if c<=1 else 1 if c<=4 else 2 if c<=16 else 3
def sbin(f): return 0 if f<.5 else 1
def lbin(n): return 0 if n<=4 else 1 if n<=6 else 2
def run(lines, rng, B=5000, G='ynlrs'):
    lines=[l for l in lines if len(l)>=2]
    tot=defaultdict(int); finc=defaultdict(int); mid=set()
    for l in lines:
        for w in l: tot[w]+=1
        mid.update(l[:-1]); finc[l[-1]]+=1
    fin=[l[-1] for l in lines]
    cell=lambda w:(fbin(tot[w]),sbin(finc[w]/tot[w]),lbin(len(w)))
    tg=[w for w in fin if w.endswith('m') and len(w)>=3]
    pools={g:defaultdict(list) for g in G}
    for w in fin:
        if not w.endswith('m') and len(w)>=3 and w[-1] in G: pools[w[-1]][cell(w)].append(w)
    need=defaultdict(int)
    for w in tg: need[cell(w)]+=1
    diag={}
    elig=set()
    for c,n in sorted(need.items()):
        row={g:(len(pools[g][c]),len(set(pools[g][c]))) for g in G}
        ok=all(p>=2*n and t>=5 for p,t in row.values())
        diag[str(c)]=dict(need=n,eligible=ok,**{g:f"{p}tok/{t}typ" for g,(p,t) in row.items()})
        if ok: elig.add(c)
    kept=[w for w in tg if cell(w) in elig]
    out=dict(targets=len(tg),kept=len(kept),coverage=len(kept)/len(tg),cells=diag)
    out['S_m_all']=sum(w[:-1] in mid for w in tg)/len(tg)
    if len(kept)/len(tg)<0.5:
        out['verdict']='NOT EVALUABLE (coverage < 0.50; stop rule)'
        if not kept: return out
    kn=defaultdict(int)
    for w in kept: kn[cell(w)]+=1
    Sm=sum(w[:-1] in mid for w in kept)/len(kept); out['S_m']=Sm; out['glyph']={}; sc={}
    for g in G:
        s=[]
        for _ in range(B):
            s.append(sum(sum(x[:-1] in mid for x in rng.sample(pools[g][c],n)) for c,n in kn.items())/len(kept))
        sc[g]=s; out['glyph'][g]=dict(S=st.mean(s),sd=st.pstdev(s),diff=Sm-st.mean(s))
    d=[(a+b+c)/3-(e+f)/2 for a,b,c,e,f in zip(sc['n'],sc['l'],sc['r'],sc['y'],sc['s'])]
    out['contrast_diff_ys_minus_nlr']=st.mean(d); out['contrast_z']=st.mean(d)/st.pstdev(d) if st.pstdev(d) else None
    return out
zl,rf=load_zl(),load_rf()
isP=lambda k:k.split(',',1)[1][1:2]=='P'
ck=sorted(k for k in set(zl)&set(rf) if isP(k))
rng=random.Random(20261107)
res={t:run([d[k] for k in ck],rng) for t,d in (('zl',zl),('rf',rf))}
res['_meta']=dict(seed=20261107,draws=5000,precommit='logs/2026-11-07-line-final-m-coarse-cell-glyph-selfreview.md')
json.dump(res,open('data/derived/line-final-m-coarse-cell-glyph-summary.json','w'),indent=1)
print(json.dumps(res,indent=1))
