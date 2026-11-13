#!/usr/bin/env node
'use strict';

// Independent JavaScript/V8 pilot of the concentrated-anchor design.
// Inputs are pinned by Git blob SHA; no external packages are required.
const fs = require('node:fs');
const crypto = require('node:crypto');

const INPUTS = {
  'data/ZL3b-n.txt': '2a4533ab9bdfa85db9bad602d590978953055df1',
  'data/RF1b-er.txt': '85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2'
};
const HASH_SEED = '20261114';
const RNG_SEED = 0x20261114;
const REPS = 50;
const NPERM = 500;
const F_GRID = [['1.0', 1.0], ['0.5', 0.5], ['0.25', 0.25], ['0.1', 0.1]];
const Q_GRID = ['0.0125', '0.02', '0.04', '0.08'];
const PAGE_RE = /^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/;
const LOCUS_RE = /^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/;
const ALT_RE = /\[([^\]:]*):([^\]]*)\]/g;

function gitBlobSha(buffer) {
  const header = Buffer.from('blob ' + buffer.length + '\0', 'utf8');
  return crypto.createHash('sha1').update(Buffer.concat([header, buffer])).digest('hex');
}
function h01(parts) {
  const key = [HASH_SEED, ...parts].join('|');
  const n = crypto.createHash('sha256').update(key, 'utf8').digest().readBigUInt64BE(0);
  return Number(n) / 18446744073709551616;
}
function wordsOf(text) {
  return text.replace(ALT_RE, '$1').replace(/<->/g, '.').replace(/<~>/g, '.')
    .replace(/<[^>]*>/g, '').split(/[.,]/).filter(Boolean);
}
function parseCorpus(buffer) {
  const headers = {}, labels = {}, textWords = {};
  for (const line of buffer.toString('utf8').split(/\r?\n/)) {
    if (!line || line.startsWith('#')) continue;
    let m = line.match(PAGE_RE);
    if (m) {
      headers[m[1]] = Object.fromEntries(
        [...m[2].matchAll(/\$(\w)=(\w+)/g)].map(x => [x[1], x[2]])
      );
      continue;
    }
    m = line.match(LOCUS_RE);
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
  const pages = Object.keys(labels).filter(p =>
    labels[p].length > 0 && (textWords[p] || []).length >= 20 && headers[p]
  ).sort();
  return {
    pages, headers,
    labels: Object.fromEntries(pages.map(p => [p, labels[p]])),
    text: Object.fromEntries(pages.map(p => [p, new Set(textWords[p] || [])]))
  };
}
function mulberry32(seed) {
  let a = seed >>> 0;
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const rng = mulberry32(RNG_SEED);
function groupsFor(data, keyFn) {
  const m = new Map();
  data.pages.forEach((p, i) => {
    const k = keyFn(data.headers[p]);
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(i);
  });
  return [...m.values()];
}
function shuffled(values) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}
function permutationP(matrix, groups) {
  let observed = 0;
  for (let i = 0; i < matrix.length; i++) observed += matrix[i][i];
  let ge = 0, sum = 0;
  for (let b = 0; b < NPERM; b++) {
    let total = 0;
    for (const g of groups) {
      if (g.length === 1) { total += matrix[g[0]][g[0]]; continue; }
      const targets = shuffled(g);
      for (let i = 0; i < g.length; i++) total += matrix[g[i]][targets[i]];
    }
    sum += total;
    if (total >= observed) ge++;
  }
  return { p: (ge + 1) / (NPERM + 1), mean: sum / NPERM };
}
let CURRENT_F = '', CURRENT_Q = '', CURRENT_REP = '';
function makeMatrix(data, anchored, rate) {
  const anchorSet = new Set(anchored), plantedText = {};
  let planted = 0;
  for (const p of data.pages) {
    const s = new Set(data.text[p]);
    if (anchorSet.has(p)) {
      for (let j = 0; j < data.labels[p].length; j++) {
        const w = data.labels[p][j];
        if (!data.text[p].has(w) && h01(['pl', CURRENT_F, CURRENT_Q, CURRENT_REP, p, String(j)]) < rate) {
          s.add(w); planted++;
        }
      }
    }
    plantedText[p] = s;
  }
  const matrix = data.pages.map(p =>
    data.pages.map(q => data.labels[p].reduce((n, w) => n + (plantedText[q].has(w) ? 1 : 0), 0))
  );
  return { matrix, planted };
}
function analyticNullMean(matrix, groups) {
  let total = 0;
  for (const g of groups) {
    let s = 0;
    for (const i of g) for (const j of g) s += matrix[i][j];
    total += s / g.length;
  }
  return total;
}
function main() {
  const data = {};
  for (const [path, expected] of Object.entries(INPUTS)) {
    const buf = fs.readFileSync(path);
    const actual = gitBlobSha(buf);
    if (actual !== expected) throw new Error(path + ' Git blob SHA mismatch: ' + actual);
    data[path.includes('ZL3b') ? 'ZL3b' : 'RF1b-er'] = parseCorpus(buf);
  }
  for (const d of Object.values(data)) {
    d.gI = groupsFor(d, h => h.I || '?');
    d.gIL = groupsFor(d, h => (h.I || '?') + '|' + (h.L || '-'));
    d.baseMatrix = d.pages.map(p =>
      d.pages.map(q => d.labels[p].reduce((n, w) => n + (d.text[q].has(w) ? 1 : 0), 0))
    );
  }
  const unionPages = [...new Set(Object.values(data).flatMap(d => d.pages))].sort();
  const baseline = {};
  for (const [name, d] of Object.entries(data)) {
    baseline[name] = {
      pages: d.pages.length,
      labelTokens: d.pages.reduce((n, p) => n + d.labels[p].length, 0),
      exactHits: d.baseMatrix.reduce((n, row, i) => n + row[i], 0),
      analyticNullMeanWithinI: +analyticNullMean(d.baseMatrix, d.gI).toFixed(3)
    };
  }
  const results = [];
  for (const [fText, f] of F_GRID) {
    const k = fText === '0.5' ? 26 : Math.round(f * unionPages.length); // Python round(26.5) = 26
    for (const qText of Q_GRID) {
      const rate = Math.min(1, Number(qText) / f);
      let passes = 0;
      const planted = Object.fromEntries(Object.keys(data).map(n => [n, []]));
      for (let rep = 0; rep < REPS; rep++) {
        const anchored = unionPages.slice().sort((a, b) =>
          h01(['sel', fText, String(rep), a]) - h01(['sel', fText, String(rep), b])
        ).slice(0, k);
        let allPass = true;
        for (const [name, d] of Object.entries(data)) {
          CURRENT_F = fText; CURRENT_Q = qText; CURRENT_REP = String(rep);
          const built = makeMatrix(d, anchored, rate);
          const p1 = permutationP(built.matrix, d.gI).p;
          const p2 = permutationP(built.matrix, d.gIL).p;
          planted[name].push(built.planted);
          if (!(p1 < 0.01 && p2 < 0.05)) allPass = false;
        }
        if (allPass) passes++;
      }
      results.push({
        f: fText, anchoredPages: k, q: qText, rateOnAnchoredPages: +rate.toFixed(4),
        passes, replicates: REPS, power: passes / REPS,
        meanPlantedTokens: Object.fromEntries(Object.entries(planted).map(([n, a]) =>
          [n, +(a.reduce((x, y) => x + y, 0) / a.length).toFixed(2)]
        ))
      });
    }
  }
  const out = {
    inputGitBlobShas: INPUTS, unionPages: unionPages.length, baseline,
    hashSeed: HASH_SEED, permutationSeed: '0x20261114', replicates: REPS, permutationsPerNull: NPERM,
    fGrid: F_GRID.map(x => x[0]), qGrid: Q_GRID,
    permutationRng: 'Mulberry32 + Fisher-Yates; independent of NumPy PCG64',
    planting: 'SHA-256 keyed by seed|sel/pl|f|q|rep|page|label-token-index',
    frozenRule: 'primary within-I p<0.01 in both inputs AND secondary within-IxL p<0.05 in both',
    results
  };
  fs.writeFileSync('data/derived/chatgpt-label-own-page-concentrated-power-check.json', JSON.stringify(out, null, 2) + '\n');
  process.stdout.write(JSON.stringify(out, null, 2) + '\n');
}
main();
