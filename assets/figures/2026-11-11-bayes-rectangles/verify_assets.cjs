// Compare browser-model calculations with exact reference cases and Python results.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const M=require('./math.js');
const ref=JSON.parse(fs.readFileSync(path.join(__dirname,'checks.json'),'utf8'));
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-12,`${a} != ${b}`);
close(M.steve().posterior[0],1/6);
assert.equal(M.steve(.2,0,0).posterior,null);
for(const p of [0,.01,.2,.5,1]){
  close(M.steve(p,.4,.4).posterior[0],p);
  for(const a of [0,.2,.8,1])for(const b of [0,.2,.8,1]){
    const z=M.steve(p,a,b);
    if(z.posterior){close(z.posterior[0]+z.posterior[1],1);assert.ok(z.posterior.every(v=>v>=0&&v<=1));}
  }
}
for(const row of ref.elbo_table){const z=M.elbo(row.r);for(const [a,b] of [['fit','fit'],['priorKL','prior_kl'],['gap','gap'],['bound','elbo']])close(z[a],row[b]);}
for(const r of [0,1]){const z=M.elbo(r);assert.ok(Number.isFinite(z.bound));close(z.logEvidence-z.bound,z.gap);}
const fair=M.monty();close(fair.posterior[0],1/3);close(fair.posterior[1],2/3);
close(M.monty(.5,true).posterior[0],.5);close(M.monty(1).posterior[0],.5);close(M.monty(0).posterior[1],1);
for(const mode of ['bayes','elbo','monty']){
  const file=fs.readFileSync(path.join(__dirname,mode+'-explorer.html'),'utf8');
  assert.ok(file.includes("connect-src 'none'")||file.includes('connect-src &#x27;none&#x27;'));
  assert.ok(!/<script[^>]+src\s*=/.test(file));
  assert.ok(!/@import|url\(https?:/.test(file));
  assert.ok(file.includes('atlas-interactive-ready'));
}
console.log('PASS: browser-model reference values, endpoints, normalization, and offline packaging.');
