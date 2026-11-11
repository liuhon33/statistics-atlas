'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const M=require('./math.js'),ref=JSON.parse(fs.readFileSync(path.join(__dirname,'reference-values.json'),'utf8'));
const max=(a,b)=>Math.max(a,Math.abs(b));
let cdfError=0,quantileError=0,deltaError=0,identityError=0,coverageError=0,decisions=0;
for(const[x,y]of ref.normal_cdf)cdfError=max(cdfError,M.cdf(x)-y);
for(const[p,q]of ref.normal_quantiles)quantileError=max(quantileError,M.quantile(p)-q);
for(const row of ref.delta_cdf){const s=M.deltaState(row.mu,row.n,row.mode);for(const[v,p]of row.points)deltaError=max(deltaError,M.exactDeltaCDF(v,s)-p);}
assert(cdfError<2e-14);assert(quantileError<2e-12);assert(deltaError<2e-11);
for(const kind of ['normal','scale'])for(const alpha of [.01,.05,.2]){
 const m=M.testModel(kind,alpha),[lo,hi]=m.controls;
 for(let i=0;i<=50;i++)for(let j=0;j<=50;j++){
  const x=lo+(hi-lo)*i/50,b=lo+(hi-lo)*j/50;
  const inBand=M.inside(x,m.acceptance(b)),inCI=M.inside(b,m.interval(x)),retained=m.p(x,b)>=alpha-1e-12;
  assert.equal(inBand,inCI);assert.equal(inCI,retained);decisions++;
 }
 const b=kind==='normal'?0:1;
 for(const bound of m.acceptance(b)){
  const s=M.testState(kind,bound,b,alpha);assert(s.inBand&&s.inCI&&s.pRetains);assert(Math.abs(s.p-alpha)<1e-12);
  const outside=bound+(bound>b?1:-1)*1e-7,inside=bound-(bound>b?1:-1)*1e-7;
  assert(!M.testState(kind,outside,b,alpha).pRetains);assert(M.testState(kind,inside,b,alpha).pRetains);
 }
 const probability=kind==='normal'?M.cdf(m.z)-M.cdf(-m.z):m.U-m.L;
 coverageError=max(coverageError,probability-(1-alpha));
}
for(const mu of [-1.5,-.3,0,.05,.8,1.5])for(const n of [1,5,25,100,500])for(const z of [-3,-1,0,.4,3]){
 const d=M.oneDraw(mu,n,z);identityError=max(identityError,Math.sqrt(n)*(d.estimate-mu*mu)-d.exact);
}
assert(identityError<1e-12);assert(coverageError<1e-12);
for(const n of [1,5,25,100,500]){
 const a=M.deltaState(0,n,'n'),b=M.deltaState(0,n,'sqrt');
 assert.equal(a.linearSD,0);assert.equal(a.share,0);assert(Math.abs(a.sd-Math.sqrt(2))<1e-12);
 assert(Math.abs(b.sd-Math.sqrt(2/n))<1e-12);
 for(const v of [-1,0,.01,.5,1,4,9])assert(Math.abs(M.exactDeltaCDF(v,a)-M.exactDeltaCDF(v,M.deltaState(0,1,'n')))<1e-12);
 assert.equal(M.linearDeltaCDF(-.001,a),0);assert.equal(M.linearDeltaCDF(0,a),1);
}
const normal=M.testState('normal',.2,0,.05),scale=M.testState('scale',1,1,.05);
assert(Math.abs(normal.p-.04550026389635839)<1e-12);assert(!normal.pRetains);
const lengths={normal:normal.acceptance[1]-normal.acceptance[0],scaleVertical:scale.acceptance[1]-scale.acceptance[0],scaleHorizontal:scale.interval[1]-scale.interval[0]};
assert(Math.abs(lengths.normal-(normal.interval[1]-normal.interval[0]))<1e-12);
assert(lengths.scaleHorizontal>lengths.scaleVertical);
const results={pass:true,normalCDFComparisons:ref.normal_cdf.length,normalQuantileComparisons:ref.normal_quantiles.length,deltaCDFComparisons:ref.delta_cdf.reduce((n,r)=>n+r.points.length,0),decisionComparisons:decisions,maxNormalCDFError:cdfError,maxNormalQuantileError:quantileError,maxExactCDFError:deltaError,maxExpansionError:identityError,maxCoverageError:coverageError,referenceLengths:lengths,independentPythonChecks:ref.scipy_checks,limits:'Numerical comparisons support the analytic derivations. No simulation-based proof of asymptotics; boundary comparisons tolerate 1e-12 floating-point roundoff.'};
fs.writeFileSync(path.join(__dirname,'math-checks.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results,null,2));
