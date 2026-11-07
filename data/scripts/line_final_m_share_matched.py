#!/usr/bin/env python3
"""(loader section reused) Line-final 'm'/'g' enrichment vs within-line shuffle null; ZL3b-normalized and RF1b-e, paragraph loci only.
Precommitment: logs/2026-11-07-line-final-m-share-matched-selfreview.md (frequency x final-share matched). Parser copied from adjacent_token_repeat_stratified.py."""
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
def bin_(c):
    for i,hi in enumerate((1,2,4,8,16,32)):
        if c<=hi: return i
    return 6
def sbin(f):
    return 0 if f<=0.25 else 1 if f<=0.5 else 2 if f<=0.75 else 3
def analyse(lines, rng, B=2000, skip1=False):
    lines=[l for l in lines if len(l)>=2]
    tot=defaultdict(int); fc=defaultdict(int); mid=set()
    for l in lines:
        for w in l: tot[w]+=1
        fc[l[-1]]+=1; mid.update(l[:-1])
    cell=lambda w:(bin_(tot[w]),sbin(fc[w]/tot[w]))
    fin=[l[-1] for l in lines]
    mf=[w for w in fin if w.endswith('m')]
    if skip1: mf=[w for w in mf if tot[w]>1]
    pool=defaultdict(list)
    for w in fin:
        if not w.endswith('m') and not (skip1 and tot[w]==1): pool[cell(w)].append(w)
    kept=[w for w in mf if pool[cell(w)]]
    dropped=len(mf)-len(kept)
    need=defaultdict(int)
    for w in kept: need[cell(w)]+=1
    Om=sum(w in mid for w in kept)/len(kept)
    m3=[w for w in kept if len(w)>=3]
    Sm=sum(w[:-1] in mid for w in m3)/len(m3)
    oc=[];sc=[]
    for _ in range(B):
        ctrl=[]
        for c,n in need.items():
            p=pool[c]; ctrl+=[rng.choice(p) for _ in range(n)]
        oc.append(sum(w in mid for w in ctrl)/len(ctrl))
        c3=[w for w in ctrl if len(w)>=3]
        sc.append(sum(w[:-1] in mid for w in c3)/len(c3))
    return dict(lines=len(lines),final_m_kept=len(kept),dropped=dropped,
      O_m=Om,O_ctrl=st.mean(oc),O_sd=st.pstdev(oc),O_z=(Om-st.mean(oc))/(st.pstdev(oc) or float("nan")),
      S_m=Sm,S_ctrl=st.mean(sc),S_sd=st.pstdev(sc),S_z=(Sm-st.mean(sc))/(st.pstdev(sc) or float("nan")))
meta=page_meta(); zl,rf=load_zl(),load_rf()
isP=lambda k:k.split(',',1)[1][1:2]=='P'
common=sorted(k for k in set(zl)&set(rf) if isP(k))
page=lambda k:re.match(r'^(f[^.,]+)',k).group(1)
rng=random.Random(20261108)
res={}
byL=defaultdict(list)
for k in common: byL[meta.get(page(k),{}).get('L','NA')].append(k)
groups=[('all',common)]+[('L='+s,ks) for s,ks in sorted(byL.items())]
for skip in (False,True):
    for name,ks in groups:
        res[name+(' [excl freq-1]' if skip else '')]={t:analyse([d[k] for k in ks],rng,skip1=skip) for t,d in (('zl',zl),('rf',rf))}
res['_meta']=dict(seed=20261108,draws=2000,control='with-replacement draw from non-m line-final tokens in same (freq bin x final-share bin) cell')
json.dump(res,open('data/derived/line-final-m-share-matched-summary.json','w'),indent=1)
for s,v in res.items():
    if s.startswith('_'):continue
    for t,x in v.items():
        print(s,t,{k:(round(y,3) if isinstance(y,float) else y) for k,y in x.items()})
