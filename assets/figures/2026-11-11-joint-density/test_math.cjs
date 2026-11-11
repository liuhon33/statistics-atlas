const assert=require('node:assert/strict'),M=require('./math.js');
const close=(a,b,tol=2e-9)=>assert.ok(Math.abs(a-b)<=tol,`${a} != ${b}`);
function simpson(fn,a,b,n=1600){let sum=fn(a)+fn(b),h=(b-a)/n;for(let i=1;i<n;i++)sum+=(i%2?4:2)*fn(a+i*h);return sum*h/3;}
let checked=0;
for(const rho of [-.95,-.8,0,.8,.95])for(const mux of [-1.5,0,1.5])for(const fixed of [-2.5,-1.3,0,1,2.5]){
  for(const isX of [true,false]){
    const raw=t=>isX?M.joint(t,fixed,rho,mux):M.joint(fixed,t,rho,mux);
    const density=t=>isX?M.conditionalX(t,fixed,rho,mux):M.conditionalY(t,fixed,rho,mux);
    const marginal=M.phi(isX?fixed:fixed-mux),mean=isX?mux+rho*fixed:rho*(fixed-mux),variance=1-rho*rho;
    close(simpson(raw,-12,12),marginal);close(simpson(density,-12,12),1);
    close(simpson(t=>t*density(t),-12,12),mean);close(simpson(t=>(t-mean)**2*density(t),-12,12),variance);
    for(const t of [-4,-1,0,2,4])close(raw(t)/marginal,density(t));
    checked++;
  }
  close(simpson(y=>(mux+rho*y)*M.phi(y),-12,12),mux);
}
const v=M.values(-1.3,1,.8);close(v.meanX,-1.04);close(v.meanY,.8);close(v.variance,.36);
for(const az of [-3,0,.8,3])for(const el of [.25,.6,1.05]){
  const xyz=[1.2,-.8,.4],p=M.project(...xyz,az,el);close(p.reduce((s,x)=>s+x*x,0),xyz.reduce((s,x)=>s+x*x,0));
}
assert.throws(()=>M.joint(0,0,1),RangeError);assert.throws(()=>M.values(0,0,-1),RangeError);
console.log(`PASS: ${checked} conditional slices; normalization, means, variances, density ratios, total expectation, reference values and camera isometry.`);
