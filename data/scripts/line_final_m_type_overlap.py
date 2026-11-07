#!/usr/bin/env python3
"""(loader section reused) Line-final 'm'/'g' enrichment vs within-line shuffle null; ZL3b-normalized and RF1b-e, paragraph loci only.
Precommitment: logs/2026-11-07-line-final-m-g-shuffle-null-selfreview.md. Parser copied from adjacent_token_repeat_stratified.py."""
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
def analyse(lines, rng, B=2000):
    lines=[l for l in lines if len(l)>=2]
    tot=defaultdict(int); mid=set()
    for l in lines:
        for w in l: tot[w]+=1
        mid.update(l[:-1])
    fin=[l[-1] for l in lines]
    mf=[w for w in fin if w.endswith('m')]
    pool=defaultdict(list)
    for w in fin:
        if not w.endswith('m'): pool[bin_(tot[w])].append(w)
    need=defaultdict(int)
    for w in mf: need[bin_(tot[w])]+=1
    Om=sum(w in mid for w in mf)/len(mf)
    mf3=[w for w in mf if len(w)>=3]
    Sm=sum(w[:-1] in mid for w in mf3)/len(mf3)
    oc=[];sc=[]
    for _ in range(B):
        ctrl=[]
        for b,n in need.items():
            p=pool[b]; ctrl+= [rng.choice(p) for _ in range(n)]   # with replacement (pool may be small)
        oc.append(sum(w in mid for w in ctrl)/len(ctrl))
        c3=[w for w in ctrl if len(w)>=3]
        sc.append(sum(w[:-1] in mid for w in c3)/len(c3))
    r=dict(lines=len(lines),final_m_tokens=len(mf),distinct_final_m_types=len(set(mf)),
      O_m=Om,O_ctrl_mean=st.mean(oc),O_ctrl_sd=st.pstdev(oc),O_z=(Om-st.mean(oc))/st.pstdev(oc),
      S_m=Sm,S_ctrl_mean=st.mean(sc),S_ctrl_sd=st.pstdev(sc),S_z=(Sm-st.mean(sc))/st.pstdev(sc))
    cnt=defaultdict(int)
    for w in mf: cnt[w]+=1
    r['top5_share']=sum(sorted(cnt.values(),reverse=True)[:5])/len(mf)
    r['top5']=sorted(cnt.items(),key=lambda x:-x[1])[:5]
    finc=defaultdict(int)
    for w in fin: finc[w]+=1
    ts=[finc[w]/tot[w] for w in tot if w.endswith('m') and tot[w]>=10]
    r['C_types_ge10']=len(ts)
    if ts:
        r['C_median_final_share']=st.median(ts); r['C_ge0.9']=sum(t>=0.9 for t in ts); r['C_le0.1']=sum(t<=0.1 for t in ts)
        r['C_frac_ge0.9']=r['C_ge0.9']/len(ts)
    return r
meta=page_meta(); zl,rf=load_zl(),load_rf()
isP=lambda k:k.split(',',1)[1][1:2]=='P'
common=sorted(k for k in set(zl)&set(rf) if isP(k))
page=lambda k:re.match(r'^(f[^.,]+)',k).group(1)
rng=random.Random(20261107)
res={'all':{t:analyse([d[k] for k in common],rng) for t,d in (('zl',zl),('rf',rf))}}
byL=defaultdict(list)
for k in common: byL[meta.get(page(k),{}).get('L','NA')].append(k)
for s,ks in sorted(byL.items()):
    res['L='+s]={t:analyse([d[k] for k in ks],rng) for t,d in (('zl',zl),('rf',rf))}
res['_meta']=dict(seed=20261107,draws=2000,control='with-replacement draw from non-m line-final tokens in same type-frequency bin')
json.dump(res,open('data/derived/line-final-m-type-overlap-summary.json','w'),indent=1)
for s,v in res.items():
    if s.startswith('_'):continue
    for t,x in v.items():
        print(s,t,{k:(round(y,3) if isinstance(y,float) else y) for k,y in x.items()})
