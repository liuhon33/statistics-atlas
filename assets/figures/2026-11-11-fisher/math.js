/* Original Fisher-information illustrations, Codex, 2026-11-11. No dependencies. */
(function(root){
  'use strict';
  const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
  const variance=a=>{const m=mean(a);return mean(a.map(x=>(x-m)**2));};
  function rng(seed){return ()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
  function normals(n,seed=20261111){const r=rng(seed),a=[];while(a.length<n){const q=Math.sqrt(-2*Math.log(Math.max(r(),1e-12))),t=2*Math.PI*r();a.push(q*Math.cos(t));if(a.length<n)a.push(q*Math.sin(t));}return a;}
  function logisticUnits(n,seed=20261111){const r=rng(seed);return Array.from({length:n},()=>{const u=Math.max(1e-12,Math.min(1-1e-12,r()));return Math.sqrt(3)/Math.PI*Math.log(u/(1-u));});}
  function model(family,sigma){
    const b=sigma*Math.sqrt(3)/Math.PI;
    const logCosh=x=>Math.abs(x)+Math.log1p(Math.exp(-2*Math.abs(x)))-Math.LN2;
    if(family==='logistic')return {
      info:1/(3*b*b), b,
      log:(y,mu)=>-Math.log(4*b)-2*logCosh((y-mu)/(2*b)),
      score:(y,mu)=>Math.tanh((y-mu)/(2*b))/b,
      hessian:(y,mu)=>-(1-Math.tanh((y-mu)/(2*b))**2)/(2*b*b)
    };
    return {info:1/(sigma*sigma),log:(y,mu)=>-Math.log(sigma*Math.sqrt(2*Math.PI))-(y-mu)**2/(2*sigma*sigma),score:(y,mu)=>(y-mu)/(sigma*sigma),hessian:()=>-1/(sigma*sigma)};
  }
  function covariance(a,b,angle){const c=Math.cos(angle),s=Math.sin(angle);return [[a*c*c+b*s*s,(a-b)*c*s],[(a-b)*c*s,a*s*s+b*c*c]];}
  const inv=M=>{const d=M[0][0]*M[1][1]-M[0][1]*M[1][0];return [[M[1][1]/d,-M[0][1]/d],[-M[1][0]/d,M[0][0]/d]];};
  const mv=(M,v)=>[M[0][0]*v[0]+M[0][1]*v[1],M[1][0]*v[0]+M[1][1]*v[1]];
  const quad=(M,v)=>{const w=mv(M,v);return v[0]*w[0]+v[1]*w[1];};
  function normal2(a,b,angle,n=240){const z=normals(n*2),c=Math.cos(angle),s=Math.sin(angle);return Array.from({length:n},(_,i)=>{const x=Math.sqrt(a)*z[2*i],y=Math.sqrt(b)*z[2*i+1];return [c*x-s*y,s*x+c*y];});}
  function ellipse(a,b,angle,center=[0,0]){const c=Math.cos(angle),s=Math.sin(angle);return Array.from({length:101},(_,i)=>{const t=2*Math.PI*i/100,x=Math.sqrt(a)*Math.cos(t),y=Math.sqrt(b)*Math.sin(t);return [center[0]+c*x-s*y,center[1]+s*x+c*y];});}
  const api={mean,variance,rng,normals,logisticUnits,model,covariance,inv,mv,quad,normal2,ellipse};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.FisherMath=api;
})(typeof window==='undefined'?{}:window);
