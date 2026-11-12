/* Original deterministic example. All coefficients, including the intercept, have the prior. */
var BayesRidgeMath = (() => {
  const x = [-1, 0, 0.5, 1.5, 2], y = [-1.2, 0.8, 1.1, 2.9, 3.7], sigma = 0.75;
  const n = x.length, sx = x.reduce((a,b)=>a+b,0), sxx=x.reduce((a,b)=>a+b*b,0);
  const sy=y.reduce((a,b)=>a+b,0), sxy=x.reduce((a,b,i)=>a+b*y[i],0);
  function posterior(tau) {
    const lambda = tau === Infinity ? 0 : sigma*sigma/(tau*tau);
    const a=n+lambda,b=sx,d=sxx+lambda,det=a*d-b*b;
    const mu=[(d*sy-b*sxy)/det,(a*sxy-b*sy)/det];
    const V=[sigma*sigma*d/det,-sigma*sigma*b/det,-sigma*sigma*b/det,sigma*sigma*a/det];
    return {tau,lambda,mu,V};
  }
  function predict(p,t){return {mean:p.mu[0]+t*p.mu[1],variance:p.V[0]+2*t*p.V[1]+t*t*p.V[3]};}
  function density(t,m,v){return Math.exp(-((t-m)**2)/(2*v))/Math.sqrt(2*Math.PI*v);}
  function ellipse(p,r=1){
    const a=p.V[0],b=p.V[1],d=p.V[3],q=Math.hypot(a-d,2*b);
    const e1=Math.sqrt((a+d+q)/2),e2=Math.sqrt((a+d-q)/2),angle=Math.atan2(2*b,a-d)/2;
    return Array.from({length:121},(_,i)=>{const t=2*Math.PI*i/120,u=r*e1*Math.cos(t),v=r*e2*Math.sin(t);
      return [p.mu[0]+u*Math.cos(angle)-v*Math.sin(angle),p.mu[1]+u*Math.sin(angle)+v*Math.cos(angle)];});
  }
  return {x,y,sigma,posterior,predict,density,ellipse};
})();
if(typeof module!=='undefined') module.exports=BayesRidgeMath;
