#!/usr/bin/env node
'use strict';

const fs = require('fs');
const crypto = require('crypto');

const SEED = 20261113;
const REPS = 50;
const NPERM = 500;
const QS = [0, 0.01, 0.0125, 0.02];
const EXPECTED = {
  'data/ZL3b-n.txt': '2a4533ab9bdfa85db9bad602d590978953055df1',
  'data/RF1b-er.txt': '85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2'
};

const pageRe = /^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/;
const locusRe = /^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/;
const altRe = /\[([^:\]]*):([^\]]*)\]/g;

function gitBlobSha(buffer) {
  const header = Buffer.from('blob ' + buffer.length + '\0', 'utf8');
  return crypto.createHash('sha1').update(Buffer.concat([header, buffer])).digest('hex');
}

function wordsOf(text) {
  return text.replace(altRe, '$1')
    .replace(/<->/g, '.')
    .replace(/<~>/g, '.')
    .replace(/<[^>]*>/g, '')
    .split(/[.,]/)
    .filter(Boolean);
}

function parseCorpus(buffer, path) {
  const content = buffer.toString('utf8');
  const headers = {};
  const labels = {};
  const textWords = {};

  for (const line of content.split(/\r?\n/)) {
    if (!line || line.startsWith('#')) continue;

    let m = line.match(pageRe);
    if (m) {
      headers[m[1]] = Object.fromEntries(
        [...m[2].matchAll(/\$(\w)=(\w+)/g)].map(x => [x[1], x[2]])
      );
      continue;
    }

    m = line.match(locusRe);
    if (!m) continue;

    const page = m[1];
    const desc = m[3];
    const words = wordsOf(m[4]);

    if (desc.length > 1 && desc[1] === 'L') {
      if (!labels[page]) labels[page] = [];
      labels[page].push(...words.filter(w =>
        w.length >= 3 && !w.includes('?') && !w.includes('*')
      ));
    } else {
      if (!textWords[page]) textWords[page] = [];
      textWords[page].push(...words);
    }
  }

  const pages = Object.keys(labels)
    .filter(p => labels[p].length > 0 &&
      (textWords[p] || []).length >= 20 && headers[p])
    .sort();

  return {
    path,
    pages,
    labels: Object.fromEntries(pages.map(p => [p, labels[p]])),
    text: Object.fromEntries(pages.map(p => [p, new Set(textWords[p] || [])])),
    headers
  };
}

function keyedUniform(q, rep, page, k) {
  const key = [SEED, q, rep, page, k].join('|');
  const digest = crypto.createHash('sha256').update(key, 'utf8').digest();
  const n = digest.readBigUInt64BE(0);
  return Number(n >> 11n) / 9007199254740992;
}

let rngState = SEED >>> 0;
function random01() {
  rngState ^= rngState << 13;
  rngState ^= rngState >>> 17;
  rngState ^= rngState << 5;
  return (rngState >>> 0) / 4294967296;
}

function shuffled(values) {
  const out = values.slice();
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random01() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function makeGroups(data) {
  const I = {};
  const IL = {};
  data.pages.forEach((page, i) => {
    const h = data.headers[page];
    const a = h.I || '?';
    const b = a + '|' + (h.L || '-');
    if (!I[a]) I[a] = [];
    if (!IL[b]) IL[b] = [];
    I[a].push(i);
    IL[b].push(i);
  });
  return { I: Object.values(I), IL: Object.values(IL) };
}

function makeMatrix(data, q, rep) {
  const plantedText = {};
  let planted = 0;

  for (const page of data.pages) {
    const words = new Set(data.text[page]);
    const labels = data.labels[page];
    for (let k = 0; k < labels.length; k++) {
      const word = labels[k];
      if (!data.text[page].has(word) &&
          q > 0 && keyedUniform(q, rep, page, k) < q) {
        words.add(word);
        planted++;
      }
    }
    plantedText[page] = words;
  }

  const n = data.pages.length;
  const matrix = Array.from({ length: n }, () => new Int32Array(n));
  for (let i = 0; i < n; i++) {
    const sourceLabels = data.labels[data.pages[i]];
    for (let j = 0; j < n; j++) {
      const targetText = plantedText[data.pages[j]];
      let hits = 0;
      for (const word of sourceLabels) if (targetText.has(word)) hits++;
      matrix[i][j] = hits;
    }
  }
  return { matrix, groups: makeGroups(data), planted };
}

function permutationP(matrix, groups) {
  let observed = 0;
  for (let i = 0; i < matrix.length; i++) observed += matrix[i][i];

  let greaterOrEqual = 0;
  for (let b = 0; b < NPERM; b++) {
    let total = 0;
    for (const group of groups) {
      const target = shuffled(group);
      for (let k = 0; k < group.length; k++) {
        total += matrix[group[k]][target[k]];
      }
    }
    if (total >= observed) greaterOrEqual++;
  }
  return (greaterOrEqual + 1) / (NPERM + 1);
}

function run() {
  const buffers = {};
  const data = {};
  for (const path of Object.keys(EXPECTED)) {
    buffers[path] = fs.readFileSync(path);
    const actual = gitBlobSha(buffers[path]);
    if (actual !== EXPECTED[path]) {
      throw new Error(path + ' Git blob SHA mismatch: ' + actual);
    }
    data[path.includes('ZL3b') ? 'ZL3b' : 'RF1b-er'] =
      parseCorpus(buffers[path], path);
  }

  const result = {
    seed: SEED,
    reps: REPS,
    permutationsPerNull: NPERM,
    inputs: {
      ZL3b: { path: EXPECTED['data/ZL3b-n.txt'], pages: data.ZL3b.pages.length,
        labelTokens: data.ZL3b.pages.reduce((n, p) => n + data.ZL3b.labels[p].length, 0) },
      'RF1b-er': { path: EXPECTED['data/RF1b-er.txt'], pages: data['RF1b-er'].pages.length,
        labelTokens: data['RF1b-er'].pages.reduce((n, p) => n + data['RF1b-er'].labels[p].length, 0) }
    },
    permutationRng: 'xorshift32 + Fisher-Yates; distinct from NumPy PCG64',
    planting: 'SHA-256 keyed by seed|q|rep|page|label-token-index',
    rule: 'primary p<0.01 in both inputs AND secondary I×L p<0.05 in both',
    curve: []
  };

  for (const q of QS) {
    let passes = 0;
    const totals = {};
    for (const name of Object.keys(data)) {
      totals[name] = { planted: 0, primaryP: 0, secondaryP: 0 };
    }

    for (let rep = 0; rep < REPS; rep++) {
      let allPass = true;
      for (const [name, corpus] of Object.entries(data)) {
        const built = makeMatrix(corpus, q, rep);
        const pPrimary = permutationP(built.matrix, built.groups.I);
        const pSecondary = permutationP(built.matrix, built.groups.IL);
        totals[name].planted += built.planted;
        totals[name].primaryP += pPrimary;
        totals[name].secondaryP += pSecondary;
        if (!(pPrimary < 0.01 && pSecondary < 0.05)) allPass = false;
      }
      if (allPass) passes++;
    }

    const row = { q, passes, power: passes / REPS, inputs: {} };
    for (const [name, v] of Object.entries(totals)) {
      row.inputs[name] = {
        meanPlantedTokens: +(v.planted / REPS).toFixed(2),
        meanPrimaryP: +(v.primaryP / REPS).toFixed(4),
        meanSecondaryP: +(v.secondaryP / REPS).toFixed(4)
      };
    }
    result.curve.push(row);
  }

  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

run();
