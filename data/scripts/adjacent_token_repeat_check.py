#!/usr/bin/env python3
"""Adjacent exact-token repeat rate vs within-line shuffle null (ZL3b-normalized and RF1b)."""
import json, random, re, statistics as st

def load_zl():
    d = {}
    for ln in open('data/derived/ZL3b-normalized.txt', encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln: continue
        k, t = ln.split('\t', 1)
        d[k] = t.split()
    return d

def load_rf():
    d = {}
    for ln in open('data/RF1b-e.txt', encoding='utf-8'):
        if ln.startswith('#') or not ln.strip(): continue
        m = re.match(r'<([^>]+)>\s+(.*)$', ln.rstrip('\n'))
        if not m or ',' not in m.group(1): continue
        t = re.sub(r'@\d+;', '?', m.group(2))
        t = re.sub(r'\{[^}]*\}', '', t)
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
    obs = r / n
    nulls = []
    for _ in range(B):
        sh = []
        for l in lines:
            l2 = l[:]; rng.shuffle(l2); sh.append(l2)
        rr, nn = rate(sh); nulls.append(rr / nn)
    mu, sd = st.mean(nulls), st.pstdev(nulls)
    return dict(pairs=n, repeats=r, observed=obs, null_mean=mu, null_sd=sd, excess=obs - mu, z=(obs - mu) / sd)

zl, rf = load_zl(), load_rf()
common = sorted(set(zl) & set(rf))
rng = random.Random(20261021)
out = {'n_zl': len(zl), 'n_rf': len(rf), 'n_common': len(common)}
out['zl_all'] = run([zl[k] for k in zl], rng)
out['zl_common'] = run([zl[k] for k in common], rng)
out['rf_common'] = run([rf[k] for k in common], rng)
json.dump(out, open('data/derived/adjacent-token-repeat-summary.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
