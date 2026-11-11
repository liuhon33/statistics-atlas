(function(){
  'use strict';
  const M=window.GamblerMath,$=id=>document.getElementById(id),NS='http://www.w3.org/2000/svg';
  let n=100,p=.4,method='value',history=[],index=0,selected=25,timer=null;
  const fmt=x=>Math.abs(x)<1e-13?'0':x.toFixed(6),pct=x=>(100*x).toFixed(3)+'%';
  function el(tag,attrs,text){const e=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e;}
  function chart(id,data,ymax,color,xlabel,ylabel,focus){
    const svg=$(id),w=svg.parentElement.clientWidth,h=svg.parentElement.clientHeight,L=48,R=12,T=24,B=39,iw=w-L-R,ih=h-T-B;
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.replaceChildren();svg.append(el('title',{},`${ylabel} by ${xlabel}`));
    const yTicks=ymax===1?4:5;
    for(let j=0;j<=yTicks;j++){const y=T+ih*(1-j/yTicks),val=ymax*j/yTicks;svg.append(el('line',{x1:L,y1:y,x2:w-R,y2:y,class:'grid'}));svg.append(el('text',{x:L-7,y:y+4,'text-anchor':'end'},ymax===1?val.toFixed(2):String(val)));}
    const band=iw/data.length;
    data.forEach((d,i)=>{const bh=Math.max(0,Math.min(ymax,d.y))/ymax*ih;const bar=el('rect',{x:L+i*band+band*.13,y:T+ih-bh,width:Math.max(.5,band*.74),height:bh,fill:d.x===focus?'var(--orange)':color,opacity:d.x===0||d.x===n?.5:1});bar.append(el('title',{},`${xlabel} ${d.x}: ${d.y.toPrecision(7)}`));svg.append(bar);if(d.x===focus)svg.append(el('line',{x1:L+(i+.5)*band,y1:T,x2:L+(i+.5)*band,y2:T+ih,stroke:'var(--orange)','stroke-dasharray':'3 3','stroke-opacity':.5}));});
    const tickCount=Math.min(data.length-1,w<450?4:8),tickIndices=new Set(Array.from({length:tickCount+1},(_,j)=>Math.round(j*(data.length-1)/Math.max(1,tickCount))));
    data.forEach((d,i)=>{if(tickIndices.has(i))svg.append(el('text',{x:L+(i+.5)*band,y:T+ih+17,'text-anchor':'middle'},d.x));});
    svg.append(el('text',{x:L,y:14},ylabel));svg.append(el('text',{x:L+iw/2,y:h-3,'text-anchor':'middle'},xlabel));
  }
  function stop(){if(timer)clearInterval(timer);timer=null;$('play').textContent='Play';}
  function rebuild(){stop();n=+$('goal').value;p=+$('prob').value;method=$('method').value;history=method==='value'?M.valueHistory(n,p):M.policyHistory(n,p);index=0;selected=Math.min(Math.max(1,selected),n-1);if(n===10&&selected>5)selected=3;$('state').max=n-1;$('state').value=selected;$('step').max=history.length-1;render();}
  function render(){
    const cur=history[index],v=cur.v,rows=M.row(v,p,selected),pick=M.choice(rows),preview=M.greedy(v,p),pi=method==='value'?preview:cur.pi,res=M.residual(v,p),done=index===history.length-1;
    $('step').value=index;$('stepLabel').textContent=`${index} / ${history.length-1}`;
    $('status').textContent=method==='value'?`Sweep ${cur.iteration} · ${cur.phase} · Bellman residual ${res.toExponential(2)}`:`Round ${cur.iteration} · ${cur.phase}${cur.changed!==undefined?' · '+cur.changed+' changed states':''}`;
    $('phaseHelp').textContent=method==='value'?'The displayed V is the current table. Action values and policy use this table; Next sweep writes max Q into every state simultaneously.':cur.unevaluated?(index===0?'Initial V is only an estimate. Next phase evaluates the bet-1 policy.':'The policy has changed; the displayed V still evaluates the previous policy. Next phase evaluates the new policy.'):'The displayed V evaluates the displayed policy. Improvement compares every legal action using this V.';
    $('next').textContent=method==='value'?'Next sweep':'Next phase';$('back').disabled=index===0;$('next').disabled=done;$('play').disabled=done;$('finish').disabled=done;
    $('valueLabel').textContent=method==='value'?`V${cur.iteration} · success probability`:cur.unevaluated?'Estimates before evaluating this policy':'Vπ · exact policy evaluation';
    $('policyLabel').textContent=method==='value'?'Greedy preview from current V':'Current deterministic policy';$('tablePolicyLabel').textContent=method==='value'?'Greedy stake':'Policy stake';
    chart('values',v.map((y,x)=>({x,y})),1,'var(--blue)','Capital s','Success probability',selected);
    chart('policy',pi.slice(1,n).map((y,i)=>({x:i+1,y})),n/2,'var(--green)','Capital s','Stake',selected);
    chart('actionPlot',rows.map(r=>({x:r.a,y:r.q})),1,'var(--blue)','Stake a','One-step action value Q',pi[selected]);
    $('stateLabel').textContent=selected;
    $('selected').textContent=`V(${selected}) = ${fmt(v[selected])} (${pct(v[selected])}) · ${method==='value'?'Greedy':'Current'} stake = ${pi[selected]} · Best one-step Q = ${fmt(pick.best)}`;
    const r=rows.find(z=>z.a===pi[selected]);$('backup').textContent=`Q(${selected}, ${r.a}) = ${p} × V(${r.up}) + ${(1-p).toFixed(1)} × V(${r.down}) = ${fmt(r.win)} + ${fmt(r.loss)} = ${fmt(r.q)}`;
    $('actionRows').innerHTML=rows.map(r=>`<tr class="${r.a===pi[selected]?'chosen':''}"><td>${r.a}</td><td>${r.up}</td><td>${r.down}</td><td>${fmt(r.win)}</td><td>${fmt(r.loss)}</td><td>${fmt(r.q)}</td><td>${r.a===pi[selected]?'Chosen':pick.tied.includes(r.a)?'Tied best':''}</td></tr>`).join('');
    $('stateRows').innerHTML=v.map((val,s)=>{const term=s===0||s===n;return `<tr class="${s===selected?'selected-row':''}"><td>${s}${term?' (terminal)':''}</td><td>${term?'—':'1 … '+Math.min(s,n-s)}</td><td>${fmt(val)}</td><td>${term?'—':pi[s]}</td><td>${term?'—':fmt(M.choice(M.row(v,p,s)).best)}</td></tr>`;}).join('');
    $('tieHelp').textContent='Ties mean action values differ by at most 10⁻¹⁰. Value iteration shows the smallest tied stake. Policy iteration retains the current stake if tied; otherwise it chooses the smallest maximizer. Early ties reflect current estimates, not proven optimality. Multiple final policies can have the same success probability.';
    if(done)stop();
  }
  for(const id of ['goal','prob','method'])$(id).addEventListener('change',rebuild);
  $('state').addEventListener('input',e=>{selected=+e.target.value;render();});$('step').addEventListener('input',e=>{stop();index=+e.target.value;render();});
  $('next').addEventListener('click',()=>{stop();index=Math.min(index+1,history.length-1);render();});$('back').addEventListener('click',()=>{stop();index=Math.max(0,index-1);render();});
  $('reset').addEventListener('click',()=>{stop();index=0;render();});$('finish').addEventListener('click',()=>{stop();index=history.length-1;render();});
  $('play').addEventListener('click',()=>{if(timer){stop();return;} $('play').textContent='Pause';timer=setInterval(()=>{index=Math.min(index+1,history.length-1);render();},window.matchMedia('(prefers-reduced-motion: reduce)').matches?1500:700);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('resize',render);rebuild();
})();
