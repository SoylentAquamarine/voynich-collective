#!/usr/bin/env python3
"""Line-final 'm'/'g' enrichment vs within-line shuffle null; ZL3b-normalized and RF1b-e, paragraph loci only.
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

GLYPHS = ('m', 'g')

def stats(lines):
    fin = [l[-1] for l in lines]; non = [w for l in lines for w in l[:-1]]
    o = {}
    for g in GLYPHS:
        F = sum(w.endswith(g) for w in fin) / len(fin); N = sum(w.endswith(g) for w in non) / len(non)
        o[g] = (F, N)
    o['len'] = (st.mean(len(w) for w in fin), st.mean(len(w) for w in non))
    return o

def run(lines, rng, B=2000):
    lines = [l for l in lines if len(l) >= 2]
    obs = stats(lines); nul = defaultdict(list)
    for _ in range(B):
        sh = []
        for l in lines:
            l2 = l[:]; rng.shuffle(l2); sh.append(l2)
        s = stats(sh)
        for k in s: nul[k].append(s[k][0])
    out = dict(lines=len(lines), tokens=sum(map(len, lines)))
    for k in obs:
        F, N = obs[k]; mu, sd = st.mean(nul[k]), st.pstdev(nul[k])
        out[k] = dict(final=F, nonfinal=N, enrichment=(F / N if N else None), null_mean=mu, null_sd=sd, z=(F - mu) / sd if sd else None)
    return out

meta = page_meta(); zl, rf = load_zl(), load_rf()
isP = lambda k: k.split(',', 1)[1][1:2] == 'P'
common = sorted(k for k in set(zl) & set(rf) if isP(k))
page = lambda k: re.match(r'^(f[^.,]+)', k).group(1)
rng = random.Random(20261107)
res = {'all': dict(zl=run([zl[k] for k in common], rng), rf=run([rf[k] for k in common], rng))}
byL = defaultdict(list)
for k in common: byL[meta.get(page(k), {}).get('L', 'NA')].append(k)
for s, ks in sorted(byL.items()):
    res['L=' + s] = dict(zl=run([zl[k] for k in ks], rng), rf=run([rf[k] for k in ks], rng))
res['_meta'] = dict(common_paragraph_loci=len(common), seed=20261107, draws=2000)
json.dump(res, open('data/derived/line-final-m-g-shuffle-null-summary.json', 'w'), indent=1)
for s, v in res.items():
    if s.startswith('_'): continue
    for t in ('zl', 'rf'):
        x = v[t]; parts = [f"{s:5} {t} lines={x['lines']}"]
        for g in GLYPHS + ('len',):
            y = x[g]; parts.append(f"{g}: F={y['final']:.4f} N={y['nonfinal']:.4f} E={y['enrichment']:.2f} z={y['z']:.1f}")
        print(' | '.join(parts))
