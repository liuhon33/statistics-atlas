/* Original implementation, 2026-11-11. Success-probability boundary convention. */
(function(root){
  'use strict';
  const TOL=1e-10;
  function initial(n){const v=Array(n+1).fill(0);v[n]=1;return v;}
  function actions(n,s){return Array.from({length:Math.min(s,n-s)},(_,i)=>i+1);}
  function row(v,p,s){const n=v.length-1;return actions(n,s).map(a=>({a,up:s+a,down:s-a,win:p*v[s+a],loss:(1-p)*v[s-a],q:p*v[s+a]+(1-p)*v[s-a]}));}
  function choice(rows,previous=null){const best=Math.max(...rows.map(r=>r.q));const tied=rows.filter(r=>best-r.q<=TOL).map(r=>r.a);return {best,tied,a:previous!==null&&tied.includes(previous)?previous:tied[0]};}
  function greedy(v,p,old=null){return v.map((_,s)=>s===0||s===v.length-1?0:choice(row(v,p,s),old?old[s]:null).a);}
  function sweep(v,p){const out=initial(v.length-1);let delta=0;for(let s=1;s<v.length-1;s++){out[s]=choice(row(v,p,s)).best;delta=Math.max(delta,Math.abs(out[s]-v[s]));}return {v:out,delta};}
  function solve(a,b){
    const n=b.length,m=a.map((r,i)=>[...r,b[i]]);
    for(let k=0;k<n;k++){
      let pivot=k;for(let i=k+1;i<n;i++)if(Math.abs(m[i][k])>Math.abs(m[pivot][k]))pivot=i;
      if(Math.abs(m[pivot][k])<1e-14)throw Error('Singular policy evaluation');
      [m[k],m[pivot]]=[m[pivot],m[k]];
      for(let i=k+1;i<n;i++){const f=m[i][k]/m[k][k];m[i][k]=0;for(let j=k+1;j<=n;j++)m[i][j]-=f*m[k][j];}
    }
    const x=Array(n).fill(0);for(let i=n-1;i>=0;i--){let z=m[i][n];for(let j=i+1;j<n;j++)z-=m[i][j]*x[j];x[i]=z/m[i][i];}return x;
  }
  function evaluate(n,p,pi){
    const a=Array.from({length:n-1},(_,i)=>Array.from({length:n-1},(_,j)=>Number(i===j))),b=Array(n-1).fill(0);
    for(let s=1;s<n;s++)for(const [t,w] of [[s+pi[s],p],[s-pi[s],1-p]]){if(t===n)b[s-1]+=w;else if(t>0)a[s-1][t-1]-=w;}
    return [0,...solve(a,b),1];
  }
  function residual(v,p){return sweep(v,p).delta;}
  function valueHistory(n,p,max=10000){
    let v=initial(n);const hist=[{v:[...v],phase:'Initial values',iteration:0,delta:null}];
    for(let k=1;k<=max;k++){const next=sweep(v,p);v=next.v;hist.push({v:[...v],phase:'Value sweep',iteration:k,delta:next.delta});if(next.delta<1e-12){hist[hist.length-1].phase='Converged value estimates';return hist;}}
    throw Error('Value iteration did not converge within the iteration limit');
  }
  function policyHistory(n,p){
    let pi=Array.from({length:n+1},(_,s)=>s>0&&s<n?1:0),v=initial(n);
    const hist=[{v:[...v],pi:[...pi],phase:'Initial policy: bet 1',iteration:0,unevaluated:true}];
    for(let k=1;k<=100;k++){
      v=evaluate(n,p,pi);hist.push({v:[...v],pi:[...pi],phase:'Evaluate current policy',iteration:k,unevaluated:false});
      const next=greedy(v,p,pi),changed=next.filter((a,s)=>a!==pi[s]).length;
      hist.push({v:[...v],pi:[...next],previousPi:[...pi],phase:changed?'Improve policy':'Policy stable',iteration:k,changed,unevaluated:changed>0});
      if(!changed)return hist;pi=next;
    }
    throw Error('Policy iteration did not stabilize');
  }
  const api={TOL,initial,actions,row,choice,greedy,sweep,evaluate,residual,valueHistory,policyHistory};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.GamblerMath=api;
})(typeof window!=='undefined'?window:this);
