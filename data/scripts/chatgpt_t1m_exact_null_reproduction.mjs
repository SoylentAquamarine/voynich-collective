#!/usr/bin/env node
/**
 * Independent exact-null reproduction of the conjugate-leaf T1/T1m statistics.
 *
 * This is a separate JavaScript implementation of the published design.
 * It does not import or execute the project's Python analysis.
 *
 * Run from the repository root:
 *   node data/scripts/chatgpt_t1m_exact_null_reproduction.mjs
 */
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";

const INPUTS = {
  ZL3b: { path: "data/ZL3b-n.txt", gitBlobSha: "2a4533ab9bdfa85db9bad602d590978953055df1" },
  RF1b: { path: "data/RF1b-e.txt", gitBlobSha: "c36d87683de5fcd24b4bb9ed56ddc4da475d8e99" },
};

function gitBlobSha(text) {
  const bytes = Buffer.from(text, "utf8");
  return createHash("sha1").update(Buffer.concat([
    Buffer.from("blob " + bytes.length + "\0", "utf8"), bytes
  ])).digest("hex");
}

function wordsOf(text) {
  return text
    .replace(/\[([^\]:]*):([^\]]*)\]/g, (_m, first) => first)
    .replace(/<->/g, ".")
    .replace(/<~>/g, ".")
    .replace(/<[^>]*>/g, "")
    .split(/[.,]/)
    .filter(Boolean);
}

function parseLoci(text) {
  const loci = {};
  for (const line of text.split(/\r?\n/)) {
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/);
    if (!m) continue;
    loci[m[1] + "." + m[2]] = { page: m[1], code: m[3], text: m[4] };
  }
  return loci;
}

function parseHeaders(text) {
  const headers = {};
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/);
    if (!m) continue;
    headers[m[1]] = Object.fromEntries(
      [...m[2].matchAll(/\$(\w)=(\w+)/g)].map(x => [x[1], x[2]])
    );
  }
  return headers;
}

function pageWords(loci) {
  const out = {};
  for (const value of Object.values(loci)) {
    (out[value.page] ??= []).push(...wordsOf(value.text));
  }
  return out;
}

function buildPairs(headers) {
  const leafMap = {};
  for (const [page, d] of Object.entries(headers)) {
    if (/^\d+$/.test(d.B ?? "") && d.F) {
      const key = [d.Q, d.B, d.F].join("|");
      (leafMap[key] ??= []).push(page);
    }
  }
  const byBifolium = {};
  for (const key of Object.keys(leafMap)) {
    const [quire, bifolium] = key.split("|");
    (byBifolium[quire + "|" + bifolium] ??= []).push(key);
  }
  return {
    leafMap,
    pairs: Object.entries(byBifolium)
      .filter(([, keys]) => keys.length === 2)
      .map(([fold, keys]) => ({ fold, quire: fold.split("|")[0], keys: keys.slice().sort() })),
  };
}

function classifyLeaves(corpusPageWords, headers, leafMap, pairs) {
  const labelledPages = Object.entries(headers)
    .filter(([, d]) => d.L === "A" || d.L === "B")
    .map(([page]) => page);
  const bifoliumOf = {};
  for (const [page, d] of Object.entries(headers)) {
    if (/^\d+$/.test(d.B ?? "")) bifoliumOf[page] = d.Q + "|" + d.B;
  }

  const predictions = {};
  const detail = {};
  for (const pair of pairs) {
    const trainingPages = labelledPages.filter(page => bifoliumOf[page] !== pair.fold);
    const counts = { A: new Map(), B: new Map() };
    for (const page of trainingPages) {
      const cls = headers[page].L;
      for (const word of corpusPageWords[page] ?? []) {
        counts[cls].set(word, (counts[cls].get(word) ?? 0) + 1);
      }
    }
    const vocabulary = new Set([...counts.A.keys(), ...counts.B.keys()]);
    const V = vocabulary.size + 1;
    const totals = {
      A: [...counts.A.values()].reduce((a, b) => a + b, 0),
      B: [...counts.B.values()].reduce((a, b) => a + b, 0),
    };

    for (const key of pair.keys) {
      const tokens = leafMap[key].flatMap(page => corpusPageWords[page] ?? []);
      if (tokens.length < 30) continue;
      let llA = 0, llB = 0;
      for (const word of tokens) {
        llA += Math.log(((counts.A.get(word) ?? 0) + 1) / (totals.A + V));
        llB += Math.log(((counts.B.get(word) ?? 0) + 1) / (totals.B + V));
      }
      predictions[key] = llA >= llB ? "A" : "B";
      const headerLabels = new Set(leafMap[key].map(page => headers[page].L));
      detail[key] = {
        n_tokens: tokens.length,
        text_label: predictions[key],
        header_label: headerLabels.size === 1 ? [...headerLabels][0] : null,
        pages: leafMap[key],
      };
    }
  }
  return { predictions, detail };
}

function combinations(n, k, visit) {
  const chosen = [];
  function walk(start, remaining) {
    if (remaining === 0) { visit(chosen.slice()); return; }
    for (let i = start; i <= n - remaining; i++) {
      chosen.push(i); walk(i + 1, remaining - 1); chosen.pop();
    }
  }
  walk(0, k);
}

function convolve(left, right) {
  const out = new Map();
  for (const [a, ca] of left) {
    for (const [b, cb] of right) out.set(a + b, (out.get(a + b) ?? 0) + ca * cb);
  }
  return out;
}

function quireDistribution(pairs, labels) {
  const keys = pairs.flatMap(pair => pair.keys);
  const index = Object.fromEntries(keys.map((key, i) => [key, i]));
  const nA = keys.filter(key => labels[key] === "A").length;
  const distribution = new Map();
  let assignments = 0;
  combinations(keys.length, nA, selected => {
    assignments++;
    const isA = new Set(selected);
    let concordant = 0;
    for (const pair of pairs) {
      const left = isA.has(index[pair.keys[0]]);
      const right = isA.has(index[pair.keys[1]]);
      if (left === right) concordant++;
    }
    distribution.set(concordant, (distribution.get(concordant) ?? 0) + 1);
  });
  return { distribution, assignments };
}

function exactTail(usePairs, labels, mixedOnly) {
  const byQuire = {};
  for (const pair of usePairs) (byQuire[pair.quire] ??= []).push(...pair.keys);
  const mixedQuires = Object.entries(byQuire)
    .filter(([, keys]) => new Set(keys.map(key => labels[key])).size === 2)
    .map(([quire]) => quire)
    .sort();
  const testedPairs = mixedOnly
    ? usePairs.filter(pair => mixedQuires.includes(pair.quire))
    : usePairs;
  const groups = {};
  for (const pair of testedPairs) (groups[pair.quire] ??= []).push(pair);

  let distribution = new Map([[0, 1]]);
  let assignments = 1;
  for (const pairs of Object.values(groups)) {
    const q = quireDistribution(pairs, labels);
    distribution = convolve(distribution, q.distribution);
    assignments *= q.assignments;
  }
  const observed = testedPairs.filter(pair =>
    labels[pair.keys[0]] === labels[pair.keys[1]]
  ).length;
  const tail = [...distribution.entries()]
    .filter(([score]) => score >= observed)
    .reduce((sum, [, count]) => sum + count, 0);
  return {
    observed,
    exact_one_sided_p: tail / assignments,
    assignments,
    mixed_quires: mixedQuires,
    n_pairs: testedPairs.length,
  };
}

function analyticNullMean(usePairs, labels, mixedOnly) {
  const byQuire = {};
  for (const pair of usePairs) (byQuire[pair.quire] ??= []).push(...pair.keys);
  const mixedQuires = new Set(Object.entries(byQuire)
    .filter(([, keys]) => new Set(keys.map(key => labels[key])).size === 2)
    .map(([quire]) => quire));
  const tested = mixedOnly ? usePairs.filter(pair => mixedQuires.has(pair.quire)) : usePairs;
  let expected = 0;
  for (const pair of tested) {
    const keys = byQuire[pair.quire];
    const n = keys.length;
    const nA = keys.filter(key => labels[key] === "A").length;
    const nB = n - nA;
    expected += (nA * (nA - 1) + nB * (nB - 1)) / (n * (n - 1));
  }
  return expected;
}

function analyse(name, inputText, headers) {
  const loci = parseLoci(inputText);
  const corpusPageWords = pageWords(loci);
  const { leafMap, pairs } = buildPairs(headers);
  const { predictions, detail } = classifyLeaves(corpusPageWords, headers, leafMap, pairs);
  const use = pairs.filter(pair => pair.keys.every(key => predictions[key]));
  const T1 = exactTail(use, predictions, false);
  const T1m = exactTail(use, predictions, true);
  const T2Leaves = Object.values(detail).filter(d => d.header_label === "A" || d.header_label === "B");
  const T2Agree = T2Leaves.filter(d => d.text_label === d.header_label).length;

  return {
    candidate_pairs: pairs.length,
    pairs_used: use.length,
    T1: {
      concordant: T1.observed,
      null_mean_exact: analyticNullMean(use, predictions, false),
      exact_one_sided_p: T1.exact_one_sided_p,
      assignments: T1.assignments,
    },
    T1m: {
      mixed_quires: T1m.mixed_quires,
      pairs: T1m.n_pairs,
      concordant: T1m.observed,
      null_mean_exact: analyticNullMean(use, predictions, true),
      exact_one_sided_p: T1m.exact_one_sided_p,
      assignments: T1m.assignments,
    },
    T2: { leaves_with_header: T2Leaves.length, agree: T2Agree },
  };
}

const inputs = {};
for (const [name, spec] of Object.entries(INPUTS)) {
  const text = readFileSync(spec.path, "utf8");
  const actual = gitBlobSha(text);
  assert.equal(actual, spec.gitBlobSha, name + " Git blob SHA mismatch");
  inputs[name] = { path: spec.path, git_blob_sha: actual };
}
const headers = parseHeaders(readFileSync(INPUTS.ZL3b.path, "utf8"));
const result = {
  method: "Independent JavaScript leave-one-bifolium-out multinomial naive Bayes (Laplace alpha=1, minimum 30 tokens), followed by exact within-quire label-assignment enumeration; no Monte Carlo RNG.",
  inputs,
  ZL3b: analyse("ZL3b", readFileSync(INPUTS.ZL3b.path, "utf8"), headers),
  RF1b: analyse("RF1b", readFileSync(INPUTS.RF1b.path, "utf8"), headers),
};
assert.equal(result.ZL3b.pairs_used, 50);
assert.equal(result.ZL3b.T1.concordant, 48);
assert.equal(result.ZL3b.T1m.pairs, 21);
assert.equal(result.ZL3b.T1m.concordant, 19);
assert.equal(result.RF1b.pairs_used, 50);
assert.equal(result.RF1b.T1.concordant, 47);
assert.equal(result.RF1b.T1m.pairs, 22);
assert.equal(result.RF1b.T1m.concordant, 19);
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
