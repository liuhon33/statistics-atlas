(()=>{'use strict';const M=InferenceMath,P=InferencePlot,C=P.C,$=id=>document.getElementById(id);let timer=null,direction=1;
 const get=()=>M.testState($('model').value,Number($('x').value),Number($('b').value),Number($('alpha').value));
 function stop(){if(timer){clearInterval(timer);timer=null;}$('play').textContent='Play null sweep';}
 function render(){const s=get(),m=s.model,normal=m.kind==='normal',range=m.domain;for(const id of ['x','b','alpha'])$(id+'-out').textContent=P.fmt(s[id],4);
  $('model-info').textContent=normal?'Known standard error τ = 0.1. The observed sample mean is x; under H₀: θ = b, its sampling distribution is N(b, 0.01).':'One observation X ∼ Uniform(θ/2, 3θ/2), θ > 0. Larger candidate parameters imply wider sampling distributions.';
  $('pval').textContent=s.p<.0001?'< 0.0001':P.fmt(s.p,5);$('interval').textContent=`[${P.fmt(s.interval[0])}, ${P.fmt(s.interval[1])}]`;$('vertical-length').textContent=P.fmt(s.acceptance[1]-s.acceptance[0],4);$('horizontal-length').textContent=P.fmt(s.interval[1]-s.interval[0],4);
  const retained=s.inBand;$('decision').className='notice'+(retained?'':' reject');$('decision').textContent=retained?'One agreement: the observed point is in the band, b is in the confidence interval, and p ≥ α. Retain this candidate null.':'One agreement: the observed point is outside the band, b is outside the confidence interval, and p < α. Reject this candidate null.';
  const band=P.plot('band',range,range,'candidate parameter b','possible observed value x',true),bs=P.sample(...range,180,b=>m.acceptance(b)[0]),tops=P.sample(...range,180,b=>m.acceptance(b)[1]);P.path(band,[...bs,...tops.reverse()],C.blue,0,'',C.blue,.09);P.path(band,bs,C.blue,1);P.path(band,tops,C.blue,1);
  P.vline(band,s.b,C.blue,'4 4');P.hline(band,s.x,C.orange,'4 4');P.path(band,[[s.b,s.acceptance[0]],[s.b,s.acceptance[1]]],C.blue,5);P.path(band,[[s.interval[0],s.x],[s.interval[1],s.x]],C.orange,5);P.dot(band,s.b,s.x,retained?C.green:C.red,5);
  $('band-formula').textContent=normal?`b − ${P.fmt(m.h,4)} ≤ x ≤ b + ${P.fmt(m.h,4)}`:`${P.fmt(m.L,4)}b ≤ x ≤ ${P.fmt(m.U,4)}b`;
  const tails=P.plot('tails',range,[0,normal?4.4:5.5],'possible observation t','sampling density under b'),d=Math.abs(s.x-s.b);
  if(normal){for(const [a,b] of [[range[0],Math.min(range[1],s.b-d)],[Math.max(range[0],s.b+d),range[1]]])if(b>a)P.area(tails,P.sample(a,b,100,t=>m.density(t,s.b)),C.green,.24);P.curve(tails,t=>m.density(t,s.b),C.ink,2);}
  else{const lo=s.b/2,hi=1.5*s.b;for(const[a,b]of[[lo,Math.min(hi,s.b-d)],[Math.max(lo,s.b+d),hi]])if(b>a)P.area(tails,[[a,1/s.b],[b,1/s.b]],C.green,.24);P.path(tails,[[lo,0],[lo,1/s.b],[hi,1/s.b],[hi,0]],C.ink,2);}
  for(const cutoff of s.acceptance)P.vline(tails,cutoff,C.blue);P.vline(tails,s.x,C.orange,'',2);
  const pv=P.plot('pcurve',range,[0,1.05],'candidate parameter b','p-value');P.hline(pv,s.alpha,C.orange,'5 4',1.4);P.curve(pv,b=>m.p(s.x,b),C.green,2.5);P.path(pv,[[s.interval[0],s.alpha],[s.interval[1],s.alpha]],C.orange,5);P.vline(pv,s.b,C.blue);P.dot(pv,s.b,s.p,retained?C.green:C.red,5);
 }
 function reset(){stop();const normal=$('model').value==='normal';for(const id of ['x','b']){const input=$(id);input.min=normal?-.5:.2;input.max=normal?.5:2.8;input.value=normal?(id==='x'?.2:0):1;}$('alpha').value=.05;render();}
 $('model').addEventListener('change',reset);for(const id of ['x','b','alpha'])$(id).addEventListener('input',()=>{stop();render();});$('reset').addEventListener('click',reset);
 $('boundary').addEventListener('click',()=>{stop();const kind=$('model').value,m=M.testModel(kind,Number($('alpha').value)),b=kind==='normal'?0:1;$('b').value=b;$('x').value=m.acceptance(b)[1];render();});
 $('play').addEventListener('click',()=>{if(timer){stop();return;}direction=1;const input=$('b'),lo=Number(input.min),hi=Number(input.max);timer=setInterval(()=>{let b=Number(input.value)+direction*(hi-lo)/160;if(b>hi||b<lo){direction*=-1;b=Math.max(lo,Math.min(hi,b));}input.value=b;render();},matchMedia('(prefers-reduced-motion: reduce)').matches?350:90);$('play').textContent='Pause null sweep';});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);reset();
})();
