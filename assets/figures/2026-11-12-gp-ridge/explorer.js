(()=>{
  const M=BayesRidgeMath,$=id=>document.getElementById(id),teal='#087f83',gold='#b77418',gray='#788793';
  let atLimit=false,playing=false,last=0,elapsed=0,raf=0;
  function plot(id,xmin,xmax,ymin,ymax,xlabel,ylabel,xticks,yticks){
    const el=$(id),W=el.viewBox.baseVal.width,H=350,l=62,r=18,t=24,b=49;
    const X=x=>l+(x-xmin)/(xmax-xmin)*(W-l-r),Y=y=>H-b-(y-ymin)/(ymax-ymin)*(H-b-t);
    let s=`<defs><clipPath id="clip-${id}"><rect x="${l}" y="${t}" width="${W-l-r}" height="${H-b-t}"/></clipPath></defs>`;
    for(const x of xticks)s+=`<path d="M${X(x)},${t}V${H-b}" stroke="#e7ecee"/><text x="${X(x)}" y="${H-b+20}" text-anchor="middle">${x}</text>`;
    for(const y of yticks)s+=`<path d="M${l},${Y(y)}H${W-r}" stroke="#e7ecee"/><text x="${l-9}" y="${Y(y)+4}" text-anchor="end">${y}</text>`;
    s+=`<path d="M${l},${t}V${H-b}H${W-r}" stroke="#7b8a92" fill="none"/><text x="${(W+l-r)/2}" y="${H-5}" text-anchor="middle">${xlabel}</text><text x="18" y="${H/2}" transform="rotate(-90 18 ${H/2})" text-anchor="middle">${ylabel}</text>`;
    const path=(pts,color,width=2,dash='',fill='none')=>`<path clip-path="url(#clip-${id})" d="${pts.map((p,i)=>(i?'L':'M')+X(p[0])+','+Y(p[1])).join(' ')}" stroke="${color}" stroke-width="${width}" stroke-dasharray="${dash}" fill="${fill}"/>`;
    const point=(x,y,color,radius=5)=>`<circle cx="${X(x)}" cy="${Y(y)}" r="${radius}" fill="${color}"/>`;
    return {path,point,X,Y,finish:extra=>{el.innerHTML=`<g font-family="system-ui,sans-serif" font-size="13" fill="#344650">${s}${extra}</g>`;}};
  }
  function render(){
    $('fit').setAttribute('viewBox',`0 0 ${document.documentElement.clientWidth<620?500:900} 350`);
    const tau=atLimit?Infinity:10**Number($('tau').value),p=M.posterior(tau),ols=M.posterior(Infinity);
    $('tau-value').textContent=atLimit?'∞ (limit)':tau.toFixed(3);
    $('lambda').textContent=p.lambda.toFixed(p.lambda<.01?6:3);$('intercept').textContent=p.mu[0].toFixed(4);$('slope').textContent=p.mu[1].toFixed(4);$('sd').textContent=Math.sqrt(p.V[3]).toFixed(4);
    $('state').textContent=atLimit?'Flat-prior endpoint: λ = 0; the posterior remains proper because the design has full rank.':'Only the prior changes. The data and observation noise remain fixed.';
    $('takeaway').textContent=atLimit?'The posterior mean equals OLS, while posterior uncertainty stays positive. Removing regularization does not remove uncertainty.':'As τ grows, λ falls. The posterior mean approaches OLS; the posterior covariance grows toward the data-only limit.';
    const g=plot('geometry',-1.4,2.6,-.5,3.5,'intercept w₀','slope w₁',[-1,0,1,2],[0,1,2,3]);
    let s='';for(const r of [1,2])s+=g.path(M.ellipse(ols,r),gray,1.5,'5 4');
    const trajectory=Array.from({length:130},(_,i)=>M.posterior(10**(-2+5*i/129)).mu);s+=g.path(trajectory,'#bac8ca',1.4);
    for(const r of [1,2])s+=g.path(M.ellipse(p,r),teal,2);
    s+=g.path([[ols.mu[0]-.07,ols.mu[1]-.07],[ols.mu[0]+.07,ols.mu[1]+.07]],gray,3)+g.path([[ols.mu[0]-.07,ols.mu[1]+.07],[ols.mu[0]+.07,ols.mu[1]-.07]],gray,3);
    s+=g.point(p.mu[0],p.mu[1],teal);g.finish(s);
    const d=plot('density',-2.5,4,0,4.3,'slope w₁','probability density',[-2,-1,0,1,2,3,4],[0,1,2,3,4]);
    const grid=Array.from({length:600},(_,i)=>-2.5+6.5*i/599);
    s=d.path(grid.map(z=>[z,M.density(z,ols.mu[1],ols.V[3])]),gray,2,'6 4');
    if(!atLimit)s+=d.path(grid.map(z=>[z,M.density(z,0,tau*tau)]),gold,2.5);
    s+=d.path(grid.map(z=>[z,M.density(z,p.mu[1],p.V[3])]),teal,2.6);d.finish(s);
    const f=plot('fit',-2.3,3,-4.8,6.8,'input x','latent value f(x)',[-2,-1,0,1,2,3],[-4,-2,0,2,4,6]);
    const xs=Array.from({length:180},(_,i)=>-2.3+5.3*i/179),upper=[],lower=[];
    for(const x of xs){const q=M.predict(p,x);upper.push([x,q.mean+2*Math.sqrt(q.variance)]);lower.push([x,q.mean-2*Math.sqrt(q.variance)]);}
    s=f.path([...upper,...lower.reverse(),upper[0]],'none',0,'','#dceeee');
    s+=f.path(xs.map(x=>[x,M.predict(ols,x).mean]),gray,2,'6 4')+f.path(xs.map(x=>[x,M.predict(p,x).mean]),teal,3);
    M.x.forEach((x,i)=>s+=f.point(x,M.y[i],'#223d4a',4.8));f.finish(s);
  }
  function stop(){playing=false;cancelAnimationFrame(raf);$('play').textContent='Play';$('play').setAttribute('aria-pressed','false');}
  function preset(value,limit=false){stop();atLimit=limit;$('tau').value=value;render();}
  $('tau').addEventListener('input',()=>{stop();atLimit=false;render();});
  $('strong').onclick=()=>preset(-1);$('moderate').onclick=()=>preset(0);$('weak').onclick=()=>preset(1.5);$('limit').onclick=()=>preset(1.5,true);$('reset').onclick=()=>preset(-1);
  function frame(t){if(!playing)return;if(last)elapsed+=t-last;last=t;
    if(elapsed>=13000){atLimit=true;render();stop();return;}
    $('tau').value=-1+2.5*Math.min(1,Math.max(0,(elapsed-1200)/10000));render();raf=requestAnimationFrame(frame);
  }
  $('play').onclick=()=>{if(playing){stop();return;}atLimit=false;playing=true;elapsed=0;last=0;$('play').textContent='Pause';$('play').setAttribute('aria-pressed','true');raf=requestAnimationFrame(frame);};
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  const motion=matchMedia('(prefers-reduced-motion: reduce)');if(motion.matches)$('play').title='Motion is optional; use the presets or slider for still comparisons.';
  window.addEventListener('resize',render);
  render();
})();
