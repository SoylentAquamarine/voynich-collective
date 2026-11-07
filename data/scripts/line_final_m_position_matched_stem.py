#!/usr/bin/env python3
"""(loader section reused) Line-final m stem test vs position/final-share/length-matched control; ZL3b-normalized and RF1b-e, paragraph loci only.
Precommitment: logs/2026-11-07-line-final-m-position-matched-stem-selfreview.md. Parser copied from adjacent_token_repeat_stratified.py."""
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
FB=(1,2,4,8,16,32)
def fbin(c):
    for i,hi in enumerate(FB):
        if c<=hi: return i
    return 6
def sbin(f): return 0 if f<.25 else 1 if f<.5 else 2 if f<.75 else 3
def analyse(lines, rng, B=5000, glyph=None):
    lines=[l for l in lines if len(l)>=2]
    tot=defaultdict(int); finc=defaultdict(int); mid=set()
    for l in lines:
        for w in l: tot[w]+=1
        mid.update(l[:-1]); finc[l[-1]]+=1
    fin=[l[-1] for l in lines]
    cell=lambda w:(fbin(tot[w]),sbin(finc[w]/tot[w]),len(w))
    tg=[w for w in fin if w.endswith('m') and len(w)>=3]
    pool=defaultdict(list)
    for w in fin:
        if not w.endswith('m') and len(w)>=3 and (glyph is None or w.endswith(glyph)): pool[cell(w)].append(w)
    need=defaultdict(int)
    for w in tg: need[cell(w)]+=1
    kept=[w for w in tg if pool[cell(w)]]
    dropped=len(tg)-len(kept)
    wr=sum(n for c,n in need.items() if pool[c] and len(pool[c])<n)
    Sm=sum(w[:-1] in mid for w in kept)/len(kept) if kept else float('nan')
    sc=[]
    for _ in range(B):
        hit=0;N=0
        for c,n in need.items():
            p=pool[c]
            if not p: continue
            d=rng.sample(p,n) if len(p)>=n else [rng.choice(p) for _ in range(n)]
            hit+=sum(w[:-1] in mid for w in d); N+=n
        sc.append(hit/N)
    mu=st.mean(sc); sd=st.pstdev(sc)
    return dict(lines=len(lines),targets=len(tg),kept=len(kept),dropped_no_pool=dropped,with_replacement_tokens=wr,
                S_m=Sm,S_ctrl_mean=mu,S_ctrl_sd=sd,diff=Sm-mu,z=(Sm-mu)/sd if sd>0 else float('nan'))
meta=page_meta(); zl,rf=load_zl(),load_rf()
isP=lambda k:k.split(',',1)[1][1:2]=='P'
common=sorted(k for k in set(zl)&set(rf) if isP(k))
page=lambda k:re.match(r'^(f[^.,]+)',k).group(1)
rng=random.Random(20261107)
strata={'all':common}
for k in common:
    strata.setdefault('L='+meta.get(page(k),{}).get('L','NA'),[]).append(k)
res={}
for s,ks in strata.items():
    res[s]={t:analyse([d[k] for k in ks],rng) for t,d in (('zl',zl),('rf',rf))}
res['secondary_by_control_glyph']={g:{t:analyse([d[k] for k in common],rng,B=2000,glyph=g) for t,d in (('zl',zl),('rf',rf))} for g in 'ynlrs'}
res['_meta']=dict(seed=20261107,draws=5000,secondary_draws=2000,precommit='logs/2026-11-07-line-final-m-position-matched-stem-selfreview.md',
  control='line-final non-m tokens, len>=3, matched on (type-frequency bin, type final-share bin, exact length); without replacement where pool>=need')
json.dump(res,open('data/derived/line-final-m-position-matched-stem-summary.json','w'),indent=1)
for s,v in res.items():
    if s.startswith('_'):continue
    for t,x in v.items():
        print(s,t,{k:(round(y,3) if isinstance(y,float) else y) for k,y in x.items()} if 'S_m' in x else {tt:{k:round(y,3) if isinstance(y,float) else y for k,y in xx.items()} for tt,xx in x.items()})
