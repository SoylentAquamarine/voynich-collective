#!/usr/bin/env node
"use strict";

// Independent arithmetic audit of the committed per-page mechanism table.
// This does NOT reparse the transcription files or rerun the planting/permutation
// simulations. It checks the published weighted aggregation and singleton-stratum
// identity from the committed JSON table.

const fs = require("node:fs");
const path = require("node:path");
const input = path.join(__dirname, "..", "derived", "label-own-page-foldout-mechanism.json");
const data = JSON.parse(fs.readFileSync(input, "utf8"));

function aggregate(x, pageNames, field) {
  const rows = pageNames.map((name) => x.pages[name]);
  const eligible = rows.reduce((sum, row) => sum + row.n_eligible, 0);
  const weighted = rows.reduce(
    (sum, row) => sum + row.n_eligible * row[field].mean_net_signal_per_hit,
    0
  ) / eligible;
  return { eligible_tokens: eligible, weighted_mean: Number(weighted.toFixed(4)) };
}

const report = {};
for (const [name, x] of Object.entries(data.per_transcription)) {
  const top5Secondary = aggregate(x, data.top5, "secondary_IxL");
  const restSecondary = aggregate(x, data.ranks6_13, "secondary_IxL");
  const top5Primary = aggregate(x, data.top5, "primary_I");
  const restPrimary = aggregate(x, data.ranks6_13, "primary_I");
  const fRos = x.pages.fRos;
  if (fRos.secondary_IxL.stratum_size !== 1 ||
      fRos.secondary_IxL.mean_net_signal_per_hit !== 0) {
    throw new Error(name + ": fRos singleton identity did not hold");
  }
  const secondarySdRatio =
    x["cell_f0.1"].secondary_IxL.sd_ratio_vs_baseline /
    x["cell_f0.25"].secondary_IxL.sd_ratio_vs_baseline;
  const primarySdRatio =
    x["cell_f0.1"].primary_I.sd_ratio_vs_baseline /
    x["cell_f0.25"].primary_I.sd_ratio_vs_baseline;
  if (Math.abs(secondarySdRatio - 1) >= 0.10 ||
      Math.abs(primarySdRatio - 1) >= 0.10) {
    throw new Error(name + ": planted-null SD ratio exceeded the precommitted 10% bound");
  }
  report[name] = {
    top5_secondary: top5Secondary,
    ranks6_13_secondary: restSecondary,
    secondary_top5_to_rest_ratio: Number((top5Secondary.weighted_mean / restSecondary.weighted_mean).toFixed(4)),
    top5_primary: top5Primary,
    ranks6_13_primary: restPrimary,
    fRos_secondary_stratum_size: fRos.secondary_IxL.stratum_size,
    fRos_secondary_net_signal: fRos.secondary_IxL.mean_net_signal_per_hit,
    fRos_share_of_top5_eligible_tokens: Number((fRos.n_eligible / top5Secondary.eligible_tokens).toFixed(4)),
    secondary_sd_ratio_f10_over_f25: Number(secondarySdRatio.toFixed(4)),
    primary_sd_ratio_f10_over_f25: Number(primarySdRatio.toFixed(4))
  };
}
console.log(JSON.stringify({ input, top5: data.top5, ranks6_13: data.ranks6_13, report }, null, 2));
