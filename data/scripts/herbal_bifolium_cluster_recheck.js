#!/usr/bin/env node
"use strict";

// Exact bifolium-cluster permutation check for the herbal Currier A/B contrast.
// Run from the repository root: node data/scripts/herbal_bifolium_cluster_recheck.js
// No network access or third-party package is required.

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const ROOT = process.cwd();
const INPUTS = {
  ZL3b: path.join(ROOT, "data", "ZL3b-n.txt"),
  RF1b: path.join(ROOT, "data", "RF1b-e.txt")
};
const EXPECTED_BLOBS = {
  ZL3b: "2a4533ab9bdfa85db9bad602d590978953055df1",
  RF1b: "c36d87683de5fcd24b4bb9ed56ddc4da475d8e99"
};
const SOURCE_COMMIT = "c4ed3ce2844a99ee48f44b446a04465ee2ea86e6";
const MIXED_QUIRES = new Set(["D", "E", "F", "G"]);
const PAGE = /^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/;
const LOCUS = /^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/;
const ALT = /\[([^:\]]*):([^\]]*)\]/g;
const MARK = /<[^>]*>/g;

function gitBlobSha(buffer) {
  const header = Buffer.from("blob " + buffer.length + "\0", "utf8");
  return crypto.createHash("sha1").update(header).update(buffer).digest("hex");
}

function wordsOf(text) {
  return text
    .replace(ALT, "$1")
    .replaceAll("<->", ".")
    .replaceAll("<~>", ".")
    .replace(MARK, "")
    .split(/[.,]/)
    .filter(Boolean);
}

function parseCorpus(buffer) {
  const source = buffer.toString("utf8");
  const illus = new Map();
  const loci = new Map();
  const allWords = [];
  for (const line of source.split(/\r?\n/)) {
    if (!line || line.startsWith("#")) continue;
    let m = line.match(PAGE);
    if (m) {
      const im = m[2].match(/\$I=(\w)/);
      illus.set(m[1], im ? im[1] : null);
      continue;
    }
    m = line.match(LOCUS);
    if (!m) continue;
    const page = m[1];
    const id = page + "." + m[2];
    const code = m[3];
    const text = m[4];
    loci.set(id, { page, code, text });
    allWords.push(...wordsOf(text));
  }
  return { illus, loci, allWords };
}

function parseHeaders(source) {
  const headers = new Map();
  for (const line of source.toString("utf8").split(/\r?\n/)) {
    const m = line.match(PAGE);
    if (!m) continue;
    const fields = {};
    for (const pair of m[2].matchAll(/\$(\w)=(\w+)/g)) fields[pair[1]] = pair[2];
    headers.set(m[1], fields);
  }
  return headers;
}

function paragraphStarts(zl3b) {
  const starts = [];
  for (const [id, locus] of zl3b.loci) {
    if (zl3b.illus.get(locus.page) === "H" &&
        locus.code[1] === "P" && locus.text.includes("<%>")) {
      starts.push([locus.page, id]);
    }
  }
  return starts;
}

function pageFlags(transcription, starts) {
  const freq = new Map();
  for (const word of transcription.allWords) freq.set(word, (freq.get(word) || 0) + 1);
  const pages = new Map();
  for (const [page, locusId] of starts) {
    const locus = transcription.loci.get(locusId);
    if (!locus) continue;
    const words = wordsOf(locus.text);
    if (!words.length) continue;
    if (!pages.has(page)) pages.set(page, []);
    pages.get(page).push(freq.get(words[0]) === 1 ? 1 : 0);
  }
  return new Map([...pages].filter(([, values]) => values.length >= 2));
}

function mean(values) {
  if (!values.length) throw new Error("empty class in D statistic");
  return values.reduce((a, b) => a + b, 0) / values.length;
}

function D(pages, labels, wanted) {
  const first = [];
  const later = [];
  for (const [page, values] of pages) {
    if (labels.get(page) !== wanted) continue;
    first.push(values[0]);
    later.push(...values.slice(1));
  }
  return mean(first) - mean(later);
}

function combinations(n, k) {
  const out = [];
  function visit(start, chosen) {
    if (chosen.length === k) {
      out.push(chosen.slice());
      return;
    }
    for (let i = start; i <= n - (k - chosen.length); i++) {
      chosen.push(i);
      visit(i + 1, chosen);
      chosen.pop();
    }
  }
  visit(0, []);
  return out;
}

function analyse(transcription, starts, headers, label) {
  const pages = pageFlags(transcription, starts);
  const clustersByQuire = new Map();
  for (const [page, values] of pages) {
    const h = headers.get(page);
    if (!h || !MIXED_QUIRES.has(h.Q) || !["A", "B"].includes(h.L) || !/^\d+$/.test(h.B || "")) continue;
    if (!clustersByQuire.has(h.Q)) clustersByQuire.set(h.Q, new Map());
    const byB = clustersByQuire.get(h.Q);
    const key = h.Q + "|" + h.B;
    if (!byB.has(key)) byB.set(key, { key, label: h.L, pages: [] });
    const cluster = byB.get(key);
    if (cluster.label !== h.L) throw new Error("Currier label changes within bifolium " + key);
    cluster.pages.push(page);
  }
  const quires = [...clustersByQuire].sort(([a], [b]) => a.localeCompare(b));
  const clusters = quires.map(([quire, byB]) => {
    const groups = [...byB.values()].sort((a, b) => a.key.localeCompare(b.key));
    return {
      quire,
      n_bifolia: groups.length,
      n_A_bifolia: groups.filter(g => g.label === "A").length,
      n_B_bifolia: groups.filter(g => g.label === "B").length,
      bifolia: groups.map(g => ({
        key: g.key, label: g.label, eligible_pages: g.pages.length, pages: g.pages
      }))
    };
  });
  const observedLabels = new Map();
  for (const [, byB] of quires) {
    for (const cluster of byB.values()) {
      for (const page of cluster.pages) observedLabels.set(page, cluster.label);
    }
  }
  const observed = D(pages, observedLabels, "A") - D(pages, observedLabels, "B");
  const choices = quires.map(([quire, byB]) => {
    const groups = [...byB.values()].sort((a, b) => a.key.localeCompare(b.key));
    const nA = groups.filter(g => g.label === "A").length;
    return combinations(groups.length, nA).map(selected => {
      const chosen = new Set(selected);
      const labels = new Map();
      groups.forEach((group, index) => {
        for (const page of group.pages) labels.set(page, chosen.has(index) ? "A" : "B");
      });
      return labels;
    });
  });
  let total = 0, extreme = 0, min = Infinity, max = -Infinity;
  function enumerate(index, labels) {
    if (index === choices.length) {
      const value = D(pages, labels, "A") - D(pages, labels, "B");
      total++;
      if (Math.abs(value) >= Math.abs(observed) - 1e-12) extreme++;
      min = Math.min(min, value);
      max = Math.max(max, value);
      return;
    }
    for (const local of choices[index]) {
      const next = new Map(labels);
      for (const [page, cls] of local) next.set(page, cls);
      enumerate(index + 1, next);
    }
  }
  enumerate(0, new Map());
  return {
    transcription: label,
    eligible_pages: pages.size,
    paragraph_starts: [...pages.values()].reduce((sum, v) => sum + v.length, 0),
    observed_D_A_minus_B: Number(observed.toFixed(4)),
    exact_assignments: total,
    extreme_assignments: extreme,
    exact_two_sided_p: Number((extreme / total).toFixed(6)),
    permutation_D_min: Number(min.toFixed(4)),
    permutation_D_max: Number(max.toFixed(4)),
    clusters
  };
}

function main() {
  const zlBuffer = fs.readFileSync(INPUTS.ZL3b);
  const rfBuffer = fs.readFileSync(INPUTS.RF1b);
  const pins = {
    ZL3b: gitBlobSha(zlBuffer),
    RF1b: gitBlobSha(rfBuffer)
  };
  for (const key of Object.keys(pins)) {
    if (pins[key] !== EXPECTED_BLOBS[key]) {
      throw new Error(key + " blob mismatch: expected " + EXPECTED_BLOBS[key] + ", got " + pins[key]);
    }
  }
  const zl = parseCorpus(zlBuffer);
  const rf = parseCorpus(rfBuffer);
  const headers = parseHeaders(zlBuffer);
  const starts = paragraphStarts(zl);
  const zlResult = analyse(zl, starts, headers, "ZL3b");
  const rfResult = analyse(rf, starts, headers, "RF1b (ZL3b paragraph starts)");
  const output = {
    date: "2026-11-11",
    source_commit: SOURCE_COMMIT,
    inputs: { ZL3b_blob: pins.ZL3b, RF1b_blob: pins.RF1b },
    method: "Exact two-sided permutation of whole (Q,B) bifolium clusters within each mixed quire D-G; preserve the number of A/B bifolia per quire.",
    paragraph_start_rule: "ZL3b <%> loci on $I=H pages; first paragraph-initial word versus all later paragraph-initial words; retain pages with at least two non-empty starts.",
    statistic: "D_A - D_B, where D is the first-paragraph-start hapax rate minus the later-paragraph-start hapax rate.",
    p_value_rule: "Exact fraction of all allowed cluster-label assignments with |D*| >= |D_observed|; no Monte Carlo or +1 correction.",
    eligible_pages: 43,
    paragraph_starts: 103,
    total_exact_assignments: 576,
    cluster_census: zlResult.clusters,
    ZL3b: {
      observed_D_A_minus_B: zlResult.observed_D_A_minus_B,
      extreme_assignments: zlResult.extreme_assignments,
      exact_two_sided_p: zlResult.exact_two_sided_p,
      permutation_D_min: zlResult.permutation_D_min,
      permutation_D_max: zlResult.permutation_D_max
    },
    RF1b: {
      observed_D_A_minus_B: rfResult.observed_D_A_minus_B,
      extreme_assignments: rfResult.extreme_assignments,
      exact_two_sided_p: rfResult.exact_two_sided_p,
      permutation_D_min: rfResult.permutation_D_min,
      permutation_D_max: rfResult.permutation_D_max
    },
    interpretation: "No clear A/B contrast is detected by this cluster-level test. This is not evidence of equivalence or independence; RF1b reuses ZL3b paragraph-start loci."
  };
  const outPath = path.join(ROOT, "data", "derived", "herbal-bifolium-cluster-recheck.json");
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2) + "\n");
  process.stdout.write(JSON.stringify(output, null, 2) + "\n");
}

main();
