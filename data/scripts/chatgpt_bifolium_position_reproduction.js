#!/usr/bin/env node
"use strict";

// Independent JavaScript reproduction of the preregistered bifolium-position
// analysis. Run from the repository root:
//   node data/scripts/chatgpt_bifolium_position_reproduction.js
// Uses only Node built-ins and pinned repository transcriptions.

const fs = require("node:fs");
const crypto = require("node:crypto");

const INPUTS = {
  ZL3b: "data/ZL3b-n.txt",
  RF1b: "data/RF1b-e.txt"
};
const EXPECTED_BLOBS = {
  ZL3b: "2a4533ab9bdfa85db9bad602d590978953055df1",
  RF1b: "c36d87683de5fcd24b4bb9ed56ddc4da475d8e99"
};
const SOURCE_COMMIT = "c4ed3ce2844a99ee48f44b446a04465ee2ea86e6";
const SEED = 20261112;
const Q1_PERMUTATIONS = 50000;
const Q2_PERMUTATIONS = 100000;
const HERBAL_QUIRES = new Set(["A","B","C","D","E","F","G"]);
const PAGE = /^<(f[^>.]+)>\s*<!\s*(.*?)\s*>/;
const LOCUS = /^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$/;

function gitBlobSha(buffer) {
  const header = Buffer.from("blob " + buffer.length + "\0", "utf8");
  return crypto.createHash("sha1").update(header).update(buffer).digest("hex");
}
function wordsOf(text) {
  return text
    .replace(/\[([^\]:]*):([^\]]*)\]/g, "$1")
    .replaceAll("<->", ".")
    .replaceAll("<~>", ".")
    .replace(/<[^>]*>/g, "")
    .split(/[.,]/).filter(Boolean);
}
function parseCorpus(buffer) {
  const illus = new Map(), headers = new Map(), loci = new Map(), allWords = [];
  for (const raw0 of buffer.toString("utf8").split(/\r?\n/)) {
    const raw = raw0.replace(/\r$/, "");
    if (!raw || raw.startsWith("#")) continue;
    let m = raw.match(PAGE);
    if (m) {
      const fields = {};
      for (const pair of m[2].matchAll(/\$(\w)=(\w+)/g)) fields[pair[1]] = pair[2];
      headers.set(m[1], fields);
      illus.set(m[1], fields.I || null);
      continue;
    }
    m = raw.match(LOCUS);
    if (!m) continue;
    const id = m[1] + "." + m[2];
    loci.set(id, {page:m[1], code:m[3], text:m[4]});
    allWords.push(...wordsOf(m[4]));
  }
  return {illus,headers,loci,allWords};
}
function paragraphStarts(zl) {
  const out=[];
  for (const [id,l] of zl.loci) {
    if (zl.illus.get(l.page)==="H" && l.code[1]==="P" && l.text.includes("<%>")) out.push([l.page,id]);
  }
  return out;
}
function position(headers) {
  const maxB={};
  for (const [page,h] of headers) if (/^\d+$/.test(h.B||"")) maxB[h.Q]=Math.max(maxB[h.Q]||0,Number(h.B));
  const pos={};
  for (const [page,h] of headers) if (/^\d+$/.test(h.B||"")) pos[page]=Number(h.B)<=maxB[h.Q]/2?"outer":"inner";
  return {pos,maxB};
}
function pageFlags(ds,starts) {
  const freq=new Map();
  for(const w of ds.allWords) freq.set(w,(freq.get(w)||0)+1);
  const pages=new Map();
  for(const [pg,id] of starts) {
    const l=ds.loci.get(id); if(!l) continue;
    const ws=wordsOf(l.text); if(!ws.length) continue;
    if(!pages.has(pg)) pages.set(pg,[]);
    pages.get(pg).push(freq.get(ws[0])===1?1:0);
  }
  return new Map([...pages].filter(([pg,v])=>v.length>=2));
}
function D(pages,labels,wanted) {
  const f=[],l=[];
  for(const [pg,v] of pages) if(labels[pg]===wanted){f.push(v[0]);l.push(...v.slice(1));}
  if(!f.length||!l.length) throw new Error("empty class in D");
  return f.reduce((a,b)=>a+b,0)/f.length-l.reduce((a,b)=>a+b,0)/l.length;
}
function mulberry32(a) {
  return function() {
    let t=a+=0x6D2B79F5;
    t=Math.imul(t^t>>>15,t|1); t^=t+Math.imul(t^t>>>7,t|61);
    return ((t^t>>>14)>>>0)/4294967296;
  };
}
function shuffle(a,rng) {
  for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
function contrast(pages,labels,strata,seed,nperm=Q1_PERMUTATIONS) {
  const groups={};
  for(const pg of pages.keys()) (groups[strata[pg]]??=[]).push(pg);
  const keep=Object.fromEntries(Object.entries(groups).filter(([s,ps])=>new Set(ps.map(p=>labels[p])).size===2));
  const use=Object.values(keep).flat();
  const selected=new Map(use.map(p=>[p,pages.get(p)]));
  const groupD=(c,lab)=>D(selected,Object.fromEntries(use.map(p=>[p,lab[p]])),c);
  const obs=groupD("outer",labels)-groupD("inner",labels);
  const nO=Object.fromEntries(Object.entries(keep).map(([s,ps])=>[s,ps.filter(p=>labels[p]==="outer").length]));
  const rng=mulberry32(seed); let extreme=0;
  for(let i=0;i<nperm;i++){
    const lab={};
    for(const [s,ps0] of Object.entries(keep)){
      const ps=shuffle([...ps0],rng), no=nO[s];
      ps.forEach((p,j)=>lab[p]=j<no?"outer":"inner");
    }
    if(Math.abs(groupD("outer",lab)-groupD("inner",lab))>=Math.abs(obs)-1e-12) extreme++;
  }
  return {n_pages_used:use.length,n_strata:Object.keys(keep).length,n_outer:use.filter(p=>labels[p]==="outer").length,
    n_inner:use.filter(p=>labels[p]==="inner").length,diff_outer_minus_inner:+obs.toFixed(4),
    permutations:nperm,extreme_assignments:extreme,p_two_sided:(extreme+1)/(nperm+1)};
}
function withinPage(pages,seed,nperm=Q1_PERMUTATIONS) {
  const obs=D(pages,Object.fromEntries([...pages.keys()].map(p=>[p,"x"])),"x");
  const entries=[...pages],rng=mulberry32(seed);let extreme=0;
  for(let i=0;i<nperm;i++){
    const f=[],l=[];
    for(const [pg,v] of entries){const k=Math.floor(rng()*v.length);f.push(v[k]);for(let j=0;j<v.length;j++)if(j!==k)l.push(v[j]);}
    const d=f.reduce((a,b)=>a+b,0)/f.length-l.reduce((a,b)=>a+b,0)/l.length;
    if(d>=obs-1e-12)extreme++;
  }
  return {D:+obs.toFixed(4),permutations:nperm,extreme_assignments:extreme,p_one_sided:(extreme+1)/(nperm+1)};
}
function holm(ps) {
  const order=ps.map((p,i)=>({p,i})).sort((a,b)=>a.p-b.p),out=[];
  let run=0;
  order.forEach((x,r)=>{run=Math.max(run,Math.min(1,(ps.length-r)*x.p));out[x.i]=run;});
  return out;
}
function q1(ds,zl,starts,pos,seed) {
  const pages=pageFlags(ds,starts),labels={},q={},ql={};
  for(const pg of pages.keys()){const h=zl.headers.get(pg);if(pos[pg]){labels[pg]=pos[pg];q[pg]=h.Q;ql[pg]=h.Q+"|"+(h.L||"?");}}
  const m=new Map([...pages].filter(([pg])=>!!pos[pg]));
  const outer=new Map([...m].filter(([pg])=>labels[pg]==="outer"));
  const inner=new Map([...m].filter(([pg])=>labels[pg]==="inner"));
  const op=withinPage(outer,seed+1),ip=withinPage(inner,seed+2),adj=holm([op.p_one_sided,ip.p_one_sided]);
  op.p_holm=adj[0];ip.p_holm=adj[1];
  return {n_eligible:Object.keys(Object.fromEntries(pages)).length,n_positioned:m.size,
    Q1:contrast(m,labels,q,seed),Q1a:{outer:op,inner:ip},
    Q1s_quire_x_language:contrast(m,labels,ql,seed+3)};
}
function q2(zl) {
  const leaves={},pagesWithoutF=[];
  for(const [pg,h] of zl.headers) if(/^\d+$/.test(h.B||"")){
    if(!h.F){pagesWithoutF.push(pg);continue;}
    const k=[h.Q,h.B,h.F].join("|");(leaves[k]??=[]).push(h);
  }
  const groups={};
  for(const k of Object.keys(leaves)){const [Q,B]=k.split("|");(groups[Q+"|"+B]??=[]).push(k);}
  const pairs=Object.values(groups).filter(v=>v.length===2).map(v=>v.sort());
  const leafLab=(k,field)=>{const vals=[...new Set(leaves[k].map(h=>h[field]||null))];return vals.length===1?vals[0]:null;};
  const scopes={}; let seed=SEED+20;
  for(const scope of ["all_quires","herbal_quires_A_G"]){
    const pp=pairs.filter(pair=>scope==="all_quires"||HERBAL_QUIRES.has(pair[0].split("|")[0]));
    const labels={},used=[],dropped=[];
    for(const [a,b] of pp){const la=leafLab(a,"L"),lb=leafLab(b,"L");if(["A","B"].includes(la)&&["A","B"].includes(lb)){labels[a]=la;labels[b]=lb;used.push([a,b]);}else dropped.push([a,b]);}
    const observed=used.filter(([a,b])=>labels[a]===labels[b]).length;
    const byq={};for(const k of Object.keys(labels)){const quire=k.split("|")[0];(byq[quire]??=[]).push(k);}
    const rng=mulberry32(seed);let extreme=0,total=0,nperm=Q2_PERMUTATIONS;
    for(let i=0;i<nperm;i++){
      const permuted={};
      for(const [quire,keys] of Object.entries(byq)){const values=shuffle(keys.map(k=>labels[k]),rng);keys.forEach((k,j)=>permuted[k]=values[j]);}
      let concordant=0;for(const [a,b] of used)if(permuted[a]===permuted[b])concordant++;
      total+=concordant;if(concordant>=observed)extreme++;
    }
    const mixedPairs=used.filter(([a,b])=>new Set(byq[a.split("|")[0]].map(k=>labels[k])).size===2);
    let handMatch=0,handN=0;
    for(const [a,b] of pp){const ha=leafLab(a,"H"),hb=leafLab(b,"H");if(ha&&hb){handN++;if(ha===hb)handMatch++;}}
    scopes[scope]={n_pairs_used:used.length,n_pairs_dropped:dropped.length,concordant:observed,
      null_mean:total/nperm,permutations:nperm,extreme_assignments:extreme,p_one_sided:(extreme+1)/(nperm+1),
      n_pairs_in_mixed_quires:mixedPairs.length,concordant_in_mixed_quires:mixedPairs.filter(([a,b])=>labels[a]===labels[b]).length,
      hand_concordance:handMatch+"/"+handN};
    seed+=100;
  }
  return {pages_without_F_dropped:pagesWithoutF,n_QB_groups:Object.keys(groups).length,n_conjugate_pairs:pairs.length,
    group_sizes:Object.values(groups).reduce((o,v)=>(o[v.length]=(o[v.length]||0)+1,o),{}),scopes};
}
function main() {
  const zb=fs.readFileSync(INPUTS.ZL3b),rb=fs.readFileSync(INPUTS.RF1b);
  const pins={ZL3b:gitBlobSha(zb),RF1b:gitBlobSha(rb)};
  for(const key of Object.keys(pins))if(pins[key]!==EXPECTED_BLOBS[key])throw new Error(key+" blob mismatch: "+pins[key]);
  const zl=parseCorpus(zb),rf=parseCorpus(rb),starts=paragraphStarts(zl),{pos,maxB}=position(zl.headers);
  const output={source_commit:SOURCE_COMMIT,input_git_blob_sha:pins,seed:SEED,q1_permutations:Q1_PERMUTATIONS,q2_permutations:Q2_PERMUTATIONS,
    corpus:{headers:zl.headers.size,ZL3b_loci:zl.loci.size,RF1b_loci:rf.loci.size,herbal_paragraph_starts:starts.length,maxB_by_quire:maxB},
    ZL3b:q1(zl,zl,starts,pos,SEED),RF1b:q1(rf,zl,starts,pos,SEED),Q2:q2(zl),
    interpretation:"Independent structural reproduction only. Q1 does not show position independence; Q2 reproduces a known header-level pattern and may be partly definitional if $L/$H were assigned at bifolium level. No source-language reading or translation follows."};
  fs.writeFileSync("data/derived/chatgpt-bifolium-position-reproduction.json",JSON.stringify(output,null,2)+"\n");
  console.log(JSON.stringify(output,null,2));
}
main();
