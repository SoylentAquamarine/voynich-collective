#!/usr/bin/env python3
"""Adjacent exact-token repeat rate vs within-line shuffle null, stratified by Currier language ($L) and illustration type ($I)."""
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

def rate(lines):
    n = r = 0
    for l in lines:
        for a, b in zip(l, l[1:]):
            n += 1; r += (a == b)
    return r, n

def run(lines, rng, B=2000):
    r, n = rate(lines)
    if n == 0: return dict(pairs=0)
    obs = r / n; nulls = []
    for _ in range(B):
        sh = []
        for l in lines:
            l2 = l[:]; rng.shuffle(l2); sh.append(l2)
        nulls.append(rate(sh)[0] / n)
    mu, sd = st.mean(nulls), st.pstdev(nulls)
    return dict(pairs=n, repeats=r, observed=obs, null_mean=mu, null_sd=sd, excess=obs - mu, z=(obs - mu) / sd if sd else None)

meta = page_meta(); zl, rf = load_zl(), load_rf()
common = sorted(set(zl) & set(rf))
page = lambda k: re.match(r'^(f[^.,]+)', k).group(1)
rng = random.Random(20261022)
out = {}
for var in ('L', 'I'):
    strata = defaultdict(list)
    for k in common: strata[meta.get(page(k), {}).get(var, 'NA')].append(k)
    out[var] = {}
    for s, ks in sorted(strata.items()):
        out[var][s] = dict(loci=len(ks), zl=run([zl[k] for k in ks], rng), rf=run([rf[k] for k in ks], rng))
json.dump(out, open('data/derived/adjacent-token-repeat-stratified-summary.json', 'w'), indent=1)
for var in out:
    for s, v in out[var].items():
        f = lambda x: f"{x['pairs']:>6} {100*x['observed']:.2f}% z={x['z']:.2f}" if x['pairs'] else 'none'
        print(var, s, v['loci'], 'ZL', f(v['zl']), '| RF', f(v['rf']))
