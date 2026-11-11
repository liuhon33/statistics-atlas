(function(root){'use strict';
 const phi=x=>Math.exp(-x*x/2)/Math.sqrt(2*Math.PI),clamp=x=>Math.max(0,Math.min(1,x));
 // If H(x)=integral_0^x exp(-t^2/2)dt / exp(-x^2/2), then H'=1+xH.
 // Its positive-term series is x + x^3/3 + x^5/(3*5) + ... .
 function cdf(x){if(x<=-8)return 0;if(x>=8)return 1;const a=Math.abs(x);let term=a,sum=a;for(let k=3;k<401;k+=2){term*=a*a/k;const next=sum+term;if(next===sum)break;sum=next;}return clamp(.5+Math.sign(x)*phi(a)*sum);}
 function quantile(p){if(!(p>0&&p<1))throw new RangeError('Quantile requires 0 < p < 1.');let lo=-8,hi=8;for(let k=0;k<55;k++){const mid=(lo+hi)/2;if(cdf(mid)<p)lo=mid;else hi=mid;}return(lo+hi)/2;}
 function testModel(kind,alpha){
  if(!(alpha>0&&alpha<1))throw new RangeError('Use 0 < alpha < 1.');
  if(kind==='normal'){const tau=.1,z=quantile(1-alpha/2),h=tau*z;return{kind,alpha,tau,z,h,domain:[-.85,.85],controls:[-.5,.5],acceptance:b=>[b-h,b+h],interval:x=>[x-h,x+h],p:(x,b)=>2*cdf(-Math.abs(x-b)/tau),density:(t,b)=>phi((t-b)/tau)/tau};}
  if(kind==='scale'){const L=.5+alpha/2,U=1.5-alpha/2;return{kind,alpha,L,U,domain:[0,6],controls:[.2,2.8],acceptance:b=>[L*b,U*b],interval:x=>[x/U,x/L],p:(x,b)=>{if(b<=0)return 0;const f=clamp(x/b-.5);return 2*Math.min(f,1-f);},density:(t,b)=>b>0&&t>=b/2&&t<=1.5*b?1/b:0};}
  throw new Error('Unknown model');
 }
 const inside=(x,pair)=>x>=pair[0]-1e-12&&x<=pair[1]+1e-12;
 function testState(kind,x,b,alpha){const model=testModel(kind,alpha),acceptance=model.acceptance(b),interval=model.interval(x),p=model.p(x,b);return{model,x,b,alpha,p,acceptance,interval,inBand:inside(x,acceptance),inCI:inside(b,interval),pRetains:p>=alpha-1e-12};}
 const scaleFactor=(mode,n)=>mode==='raw'?1:mode==='n'?n:Math.sqrt(n);
 function deltaState(mu,n,mode='sqrt'){if(!(n>=1&&Math.abs(mu)<=10))throw new RangeError('Invalid model parameters.');const a=scaleFactor(mode,n),rawVar=4*mu*mu/n+2/(n*n),linearVar=4*mu*mu/n;return{mu,n,mode,a,rawMean:1/n,rawVar,linearVar,mean:a/n,sd:a*Math.sqrt(rawVar),linearSD:a*2*Math.abs(mu)/Math.sqrt(n),share:linearVar/rawVar,support:-a*mu*mu};}
 function exactDeltaCDF(v,s){const r=s.mu*s.mu+v/s.a;if(r<=0)return 0;const t=Math.sqrt(r),sn=Math.sqrt(s.n);return clamp(cdf((t-s.mu)*sn)-cdf((-t-s.mu)*sn));}
 const linearDeltaCDF=(v,s)=>s.linearSD===0?(v<0?0:1):cdf(v/s.linearSD);
 function deltaQuantile(p,s){let lo=s.support,hi=s.a*((Math.abs(s.mu)+8/Math.sqrt(s.n))**2-s.mu*s.mu);for(let k=0;k<55;k++){const mid=(lo+hi)/2;if(exactDeltaCDF(mid,s)<p)lo=mid;else hi=mid;}return(lo+hi)/2;}
 function oneDraw(mu,n,z){const bar=mu+z/Math.sqrt(n),linear=2*mu*z,quadratic=z*z/Math.sqrt(n);return{bar,estimate:bar*bar,linear,quadratic,exact:linear+quadratic};}
 const api={phi,cdf,quantile,testModel,testState,inside,scaleFactor,deltaState,exactDeltaCDF,linearDeltaCDF,deltaQuantile,oneDraw};
 if(typeof module==='object'&&module.exports)module.exports=api;else root.InferenceMath=api;
})(typeof globalThis!=='undefined'?globalThis:this);
