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

def common(lines, rng, B=5000, G='ynlrs'):
    lines=[l for l in lines if len(l)>=2]
    tot=defaultdict(int); finc=defaultdict(int); mid=set()
    for l in lines:
        for w in l: tot[w]+=1
        mid.update(l[:-1]); finc[l[-1]]+=1
    fin=[l[-1] for l in lines]
    cell=lambda w:(fbin(tot[w]),sbin(finc[w]/tot[w]),len(w))
    tg=[w for w in fin if w.endswith('m') and len(w)>=3]
    pools={g:defaultdict(list) for g in G}
    for w in fin:
        if not w.endswith('m') and len(w)>=3 and w[-1] in G: pools[w[-1]][cell(w)].append(w)
    kept=[w for w in tg if all(pools[g][cell(w)] for g in G)]
    need=defaultdict(int)
    for w in kept: need[cell(w)]+=1
    Sm=sum(w[:-1] in mid for w in kept)/len(kept)
    out=dict(targets=len(tg),kept=len(kept),dropped=len(tg)-len(kept),S_m=Sm,glyph={})
    for g in G:
        wr=sum(n for c,n in need.items() if len(pools[g][c])<n)
        sc=[]
        for _ in range(B):
            hit=0
            for c,n in need.items():
                p=pools[g][c]
                d=rng.sample(p,n) if len(p)>=n else [rng.choice(p) for _ in range(n)]
                hit+=sum(w[:-1] in mid for w in d)
            sc.append(hit/len(kept))
        out['glyph'][g]=dict(S=st.mean(sc),sd=st.pstdev(sc),diff=Sm-st.mean(sc),wr_share=wr/len(kept),_sc=sc)
    # contrast: mean(diff y,s) - mean(diff n,l,r) using paired draws
    ys=[(a+b)/2 for a,b in zip(out['glyph']['y']['_sc'],out['glyph']['s']['_sc'])]
    nlr=[(a+b+c)/3 for a,b,c in zip(*(out['glyph'][g]['_sc'] for g in 'nlr'))]
    # S_ctrl higher for n/l/r => diff more negative for y/s means S_ctrl(y,s) > S_ctrl(nlr)? report contrast = diff_ys - diff_nlr
    d=[b-a for a,b in zip(ys,nlr)]  # diff_ys - diff_nlr = S_nlr - S_ys
    out['contrast_diff_ys_minus_nlr']=st.mean(d); out['contrast_sd']=st.pstdev(d)
    out['contrast_z']=st.mean(d)/st.pstdev(d) if st.pstdev(d)>0 else float('nan')
    for g in G: del out['glyph'][g]['_sc']
    return out
zl,rf=load_zl(),load_rf()
isP=lambda k:k.split(',',1)[1][1:2]=='P'
ck=sorted(k for k in set(zl)&set(rf) if isP(k))
rng=random.Random(20261107)
res={t:common([d[k] for k in ck],rng) for t,d in (('zl',zl),('rf',rf))}
res['_meta']=dict(seed=20261107,draws=5000,precommit='logs/2026-11-07-line-final-m-common-support-glyph-selfreview.md')
json.dump(res,open('data/derived/line-final-m-common-support-glyph-summary.json','w'),indent=1)
print(json.dumps(res,indent=1))
