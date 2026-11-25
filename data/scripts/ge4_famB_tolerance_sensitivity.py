import json
d=json.load(open('data/derived/ge4-famB-seed-panel.json'))
V=d['voynich_ext_rescored']; V={k:V[k] for k in('d1','d2','d3')}
out={'targets':V,'committed_d1':d['voynich_committed']['d1'],'results':{}}
for p,r in d['panel'].items():
    vals={k:r[k]['values'] for k in V}; n=len(vals['d1'])
    res={}
    for t in (0.10,0.05,0.03):
        f={k:sum(abs(x-V[k])<=t for x in vals[k])/n for k in V}
        j=sum(max(abs(vals[k][i]-V[k]) for k in V)<=t for i in range(n))/n
        f['joint']=j
        f['joint_reading']='not distinguishable' if j>=.25 else 'distinguishable' if j<.10 else 'ambiguous'
        res[str(t)]=f
    res['d1_vs_committed_0.10']=sum(abs(x-d['voynich_committed']['d1'])<=0.10 for x in vals['d1'])/n
    out['results'][p]=res
json.dump(out,open('data/derived/ge4-famB-tolerance-sensitivity.json','w'),indent=1)
for p,r in out['results'].items():
    print(p)
    for t,f in r.items(): print(' ',t,f)
