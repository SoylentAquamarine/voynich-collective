#!/usr/bin/env node
'use strict';

// Independent matched-dose reproduction of the frozen label own-page test.
// Uses the pinned ZL3b/RF1b-er blobs, SHA-256 planting, and an independent
// xoshiro128** permutation RNG. Post-hoc structural sensitivity only.
const fs = require('node:fs');
const crypto = require('node:crypto');

const INPUTS = {
  'data/ZL3b-n.txt': '2a4533ab9bdfa85db9bad602d590978953055df1',
  'data/RF1b-er.txt': '85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2'
};
const SEED = 20261116;
const REPS = 200;
const NPERM = 2000;
const TARGET_HITS = 11.8;
const F_GRID = [0.25, 0.10];
const PAGE_RE = /^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/;
const LOCUS_RE = /^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/;
const ALT_RE = /\[([^\]:]*):([^\]]*)\]/g;

function gitBlobSha(buf) {
  const head = Buffer.from('blob ' + buf.length + '\0', 'utf8');
  return crypto.createHash('sha1').update(Buffer.concat([head, buf])).digest('hex');
}
function hash01(parts) {
  const key = [SEED, ...parts].map(String).join('|');
  const n = crypto.createHash('sha256').update(key, 'utf8').digest().readBigUInt64BE(0);
  return Number(n) / 18446744073709551616;
}
function wordsOf(s) {
  return s.replace(ALT_RE, '$1').replace(/<->/g, '.').replace(/<~>/g, '.')
    .replace(/<[^>]*>/g, '').split(/[.,]/).filter(Boolean);
}
function parseHeaders(buf) {
  const out = {};
  for (const line of buf.toString('utf8').split(/\r?\n/)) {
    const m = line.match(PAGE_RE);
    if (!m) continue;
    out[m[1]] = Object.fromEntries([...m[2].matchAll(/\$(\w)=(\w+)/g)].map(x => [x[1], x[2]]));
  }
  return out;
}
function parseCorpus(buf, headers) {
  const labels = {}, textWords = {};
  for (const line of buf.toString('utf8').split(/\r?\n/)) {
    if (!line || line.startsWith('#') || PAGE_RE.test(line)) continue;
    const m = line.match(LOCUS_RE);
    if (!m) continue;
    const page = m[1], desc = m[3], words = wordsOf(m[4]);
    if (desc.length > 1 && desc[1] === 'L') {
      if (!labels[page]) labels[page] = [];
      labels[page].push(...words.filter(w => w.length >= 3 && !w.includes('?') && !w.includes('*')));
    } else {
      if (!textWords[page]) textWords[page] = [];
      textWords[page].push(...words);
    }
  }
  const pages = Object.keys(labels).filter(p => labels[p].length > 0 &&
    (textWords[p] || []).length >= 20 && headers[p]).sort();
  return {
    pages, labels: Object.fromEntries(pages.map(p => [p, labels[p]])),
    text: Object.fromEntries(pages.map(p => [p, new Set(textWords[p] || [])]))
  };
}
function groupPages(data, keyFn, headers) {
  const groups = new Map();
  data.pages.forEach((p, i) => {
    const key = keyFn(headers[p]);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(i);
  });
  return [...groups.values()];
}
function makeXoshiro128ss(seed) {
  let x = seed >>> 0;
  function splitmix32() {
    x = (x + 0x9e3779b9) >>> 0;
    let z = x;
    z = Math.imul(z ^ (z >>> 16), 0x21f0aaad);
    z = Math.imul(z ^ (z >>> 15), 0x735a2d97);
    return (z ^ (z >>> 15)) >>> 0;
  }
  let s0 = splitmix32(), s1 = splitmix32(), s2 = splitmix32(), s3 = splitmix32();
  const rotl = (v, k) => (v << k) | (v >>> (32 - k));
  return function next() {
    const result = Math.imul(rotl(Math.imul(s1, 5) >>> 0, 7), 9) >>> 0;
    const t = s1 << 9;
    s2 ^= s0; s3 ^= s1; s1 ^= s2; s0 ^= s3; s2 ^= t; s3 = rotl(s3, 11);
    return result / 4294967296;
  };
}
const rng = makeXoshiro128ss(SEED);
function permutationP(matrix, groups) {
  let observed = 0;
  for (let i = 0; i < matrix.length; i++) observed += matrix[i][i];
  const arrays = groups.map(g => g.slice());
  let ge = 0;
  for (let r = 0; r < NPERM; r++) {
    let total = 0;
    for (let z = 0; z < groups.length; z++) {
      const g = groups[z], a = arrays[z];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(rng() * (i + 1));
        const v = a[i]; a[i] = a[j]; a[j] = v;
      }
      for (let i = 0; i < g.length; i++) total += matrix[g[i]][a[i]];
    }
    if (total >= observed) ge++;
  }
  return (ge + 1) / (NPERM + 1);
}
function matrixFor(data, anchor, f, name, rep, rate) {
  const anchored = new Set(anchor), plantedText = [];
  for (const p of data.pages) {
    const s = new Set(data.text[p]);
    if (anchored.has(p)) {
      for (let j = 0; j < data.labels[p].length; j++) {
        const w = data.labels[p][j];
        if (!data.text[p].has(w) && hash01(['md', f, name, rep, p, j]) < rate) s.add(w);
      }
    }
    plantedText.push(s);
  }
  return data.pages.map(p => data.pages.map((q, j) => {
    let n = 0; for (const w of data.labels[p]) if (plantedText[j].has(w)) n++; return n;
  }));
}
function main() {
  const buffers = {}, headers = {};
  for (const [path, expected] of Object.entries(INPUTS)) {
    const buf = fs.readFileSync(path);
    const actual = gitBlobSha(buf);
    if (actual !== expected) throw new Error(path + ' Git blob SHA mismatch: ' + actual);
    buffers[path] = buf;
  }
  Object.assign(headers, parseHeaders(buffers['data/ZL3b-n.txt']));
  const data = {
    ZL3b: parseCorpus(buffers['data/ZL3b-n.txt'], headers),
    'RF1b-er': parseCorpus(buffers['data/RF1b-er.txt'], headers)
  };
  for (const d of Object.values(data)) {
    d.gI = groupPages(d, h => h.I || '?', headers);
    d.gIL = groupPages(d, h => (h.I || '?') + '|' + (h.L || '-'), headers);
  }
  const union = [...new Set(Object.values(data).flatMap(d => d.pages))].sort();
  const richest = union.slice().sort((a, b) => {
    const ca = Math.max(...Object.values(data).map(d => d.labels[a]?.length || 0));
    const cb = Math.max(...Object.values(data).map(d => d.labels[b]?.length || 0));
    return cb - ca || a.localeCompare(b);
  });
  const cells = [];
  for (const f of F_GRID) {
    const k = Math.round(f * union.length), anchor = richest.slice(0, k);
    const eligible = {}, rates = {}, planted = { ZL3b: [], 'RF1b-er': [] };
    for (const [name, d] of Object.entries(data)) {
      eligible[name] = d.pages.reduce((n, p) => n + (anchor.includes(p) ? d.labels[p].filter(w => !d.text[p].has(w)).length : 0), 0);
      rates[name] = Math.min(1, TARGET_HITS / eligible[name]);
    }
    let passes = 0;
    for (let rep = 0; rep < REPS; rep++) {
      let allPass = true;
      for (const [name, d] of Object.entries(data)) {
        let nPlanted = 0;
        for (const p of d.pages) if (anchor.includes(p)) {
          for (let j = 0; j < d.labels[p].length; j++) {
            const w = d.labels[p][j];
            if (!d.text[p].has(w) && hash01(['md', f, name, rep, p, j]) < rates[name]) nPlanted++;
          }
        }
        planted[name].push(nPlanted);
        const M = matrixFor(d, anchor, f, name, rep, rates[name]);
        const pI = permutationP(M, d.gI), pIL = permutationP(M, d.gIL);
        if (!(pI < 0.01 && pIL < 0.05)) allPass = false;
      }
      if (allPass) passes++;
    }
    const power = passes / REPS;
    cells.push({
      f, anchoredPages: k, eligibleTokens: eligible, rates, passes, power,
      mcSE: Math.sqrt(power * (1 - power) / REPS),
      meanPlantedTokens: Object.fromEntries(Object.entries(planted).map(([n, a]) => [n, a.reduce((s, v) => s + v, 0) / a.length]))
    });
  }
  const out = {
    inputGitBlobShas: INPUTS, unionPages: union.length, eligiblePages: Object.fromEntries(Object.entries(data).map(([n, d]) => [n, d.pages.length])),
    labelTokens: Object.fromEntries(Object.entries(data).map(([n, d]) => [n, d.pages.reduce((s, p) => s + d.labels[p].length, 0)])),
    richestTop13: richest.slice(0, 13), richestTop5: richest.slice(0, 5),
    seed: SEED, replicates: REPS, permutationsPerNull: NPERM, targetHitsPerTranscription: TARGET_HITS,
    planting: 'SHA-256 keyed by seed|md|f|transcription|replicate|page|label-index',
    permutationRng: 'xoshiro128** + Fisher-Yates; independent of NumPy PCG64',
    frozenRule: 'within-I p<0.01 and within-IxL p<0.05 in both transcriptions', cells
  };
  fs.writeFileSync('data/derived/chatgpt-label-own-page-richest-matched-dose-check.json', JSON.stringify(out, null, 2) + '\n');
  process.stdout.write(JSON.stringify(out, null, 2) + '\n');
}
main();