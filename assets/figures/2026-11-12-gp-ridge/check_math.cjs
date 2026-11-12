const fs=require('node:fs'),path=require('node:path');
const M=require('./math.js'),checks=JSON.parse(fs.readFileSync(path.join(__dirname,'checks.json'),'utf8'));
let maxError=0;
for(const r of checks.reference_states){
  const p=M.posterior(r.tau===null?Infinity:r.tau);
  for(const [a,b] of [[p.lambda,r.lambda],...p.mu.map((v,i)=>[v,r.mu[i]]),...p.V.map((v,i)=>[v,r.V[i]])])maxError=Math.max(maxError,Math.abs(a-b));
  for(const z of M.ellipse(p,2)){
    const dx=z[0]-p.mu[0],dy=z[1]-p.mu[1],det=p.V[0]*p.V[3]-p.V[1]**2;
    const q=(p.V[3]*dx*dx-2*p.V[1]*dx*dy+p.V[0]*dy*dy)/det;
    maxError=Math.max(maxError,Math.abs(q-4));
  }
}
if(maxError>1e-10)throw Error('Python/JS or ellipse mismatch '+maxError);
fs.writeFileSync(path.join(__dirname,'js-checks.json'),JSON.stringify({pass:true,maxAbsoluteError:maxError,states:checks.reference_states.length},null,2)+'\n');
console.log('JavaScript agrees with independent Python/NumPy checks; max error',maxError);
