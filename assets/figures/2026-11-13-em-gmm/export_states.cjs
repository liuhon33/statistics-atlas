const M = require('./math.js');
const assert = require('node:assert/strict');
const xs = M.data();
const snapshots = [], transitions = [], runs = [];
let maxNormalizationError = 0, minLogLikelihoodGain = Infinity, minQGain = Infinity;
for (const key of Object.keys(M.presets)) for (const weight of [.1,.5,.9]) for (const sd of [.2,.7,1.6]) {
  let p = M.initialize(key,weight,sd), last = M.expectation(xs,p).logLikelihood, stop = null;
  const isDefault = key==='crossed' && weight===.5 && sd===.7;
  if (isDefault) snapshots.push({label:'Initialize: green data',p:M.clone(p),r:null,iteration:0,logLikelihood:last});
  let iterations = 0;
  for(let i=0;i<60;i++) {
    const e=M.expectation(xs,p);
    for(const row of e.r) {
      maxNormalizationError=Math.max(maxNormalizationError,Math.abs(row[0]+row[1]-1));
      assert(row.every(x=>Number.isFinite(x)&&x>=0&&x<=1+1e-14));
    }
    if(isDefault&&i===0)snapshots.push({label:'E-step: recolor only',p:M.clone(p),r:e.r,iteration:0,logLikelihood:last});
    let next;
    try {next=M.maximization(xs,e.r);} catch(error) {stop=error.message;break;}
    const ll=M.expectation(xs,next).logLikelihood, gain=ll-last, qGain=M.qValue(xs,e.r,next)-M.qValue(xs,e.r,p);
    assert(gain>=-1e-7);assert(qGain>=-1e-7);
    minLogLikelihoodGain=Math.min(minLogLikelihoodGain,gain); minQGain=Math.min(minQGain,qGain);
    if(isDefault&&[0,1,4,19].includes(i)) transitions.push({old:M.clone(p),r:e.r,new:M.clone(next)});
    p=next; last=ll; iterations++;
    if(isDefault&&[0,19].includes(i))snapshots.push({label:i===0?'M-step 1: refit; colors frozen':'After 20 M-steps',p:M.clone(p),r:e.r,iteration:i+1,logLikelihood:ll});
  }
  runs.push({preset:key,initialWeight:weight,initialSd:sd,iterations,stop,finalLogLikelihood:last});
}
assert(maxNormalizationError<1e-12);
const trap=M.initialize('identical'), tr=M.expectation(xs,trap), tp=M.maximization(xs,tr.r);
assert(tr.r.every(v=>Math.abs(v[0]-.5)<1e-14));assert.deepEqual(tp.means[0],tp.means[1]);
// Stable likelihood even for data far out in the Gaussian tails.
const far=M.expectation([[1000,-1000]],M.initialize());assert(Number.isFinite(far.logLikelihood));
assert(Math.abs(far.r[0][0]+far.r[0][1]-1)<1e-12);
console.log(JSON.stringify({seed:M.seed,data:xs,snapshots,transitions,runs,small:{data:[[-1,0],[.2,.6],[1,.1]],p:M.initialize('crossed',.4,.9)},jsChecks:{maxNormalizationError,minLogLikelihoodGain,minQGain,symmetryTrap:true,logSpaceTail:true}},null,2));
