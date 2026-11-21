import json,sys
j=json.load(open(sys.argv[1])); S=j['streams']; bad=[]
bins=['d0_identical','d1','d2','d3','d4plus']
for n,s in S.items():
    tot=0
    for b in bins:
        r=s[b]; tot+=r['obs']
        if abs(r['obs']/r['null_mean']-r['ratio'])>1e-9: bad.append((n,b,'ratio'))
        if abs((r['obs']-r['null_mean'])/r['null_sd']-r['z'])>1e-9: bad.append((n,b,'z'))
    if tot!=s['pairs']: bad.append((n,'sum',tot,s['pairs']))
v=S['voynich_ZL3b_eva']
for fam,pre,key in [('A_q0.8_S2_last10','A_q0.8_S2_last10_seed','A_q0.8_S2_last10'),('B_p0.01','B_p0.01_seed','B_p0.01')]:
    seeds=[s for n,s in S.items() if n.startswith(pre)]
    fails=[]
    for d in ('d1','d2','d3'):
        rs=[x[d]['obs']/x[d]['null_mean'] for x in seeds]
        lo,hi=min(rs)-0.1,max(rs)+0.1
        rv=v[d]['obs']/v[d]['null_mean']
        if not lo<=rv<=hi: fails.append((d,round(rv,4),round(lo,4),round(hi,4)))
    stored=j['verdicts'][key]
    print(fam,'n_seeds',len(seeds),'consistent',not fails,'fails',fails,'stored',stored['consistent'],[f['bin'] for f in stored['failing_bins']])
    if (not fails)!=stored['consistent'] or [f[0] for f in fails]!=[f['bin'] for f in stored['failing_bins']]: bad.append((fam,'verdict'))
print('mismatches:',bad)
