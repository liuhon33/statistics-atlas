(()=>{
  const update=document.querySelector('main').dataset.mode==='update';
  const ids=update?['alpha','beta','success','failure']:['alpha','beta'];
  const el=id=>document.getElementById(id),fmt=x=>Number(x.toFixed(4)).toString();
  const svg=el('plot'),NS='http://www.w3.org/2000/svg';
  function node(tag,attrs,text){const n=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;svg.appendChild(n);return n;}
  function draw(){
    const [a,b,s=0,f=0]=ids.map(id=>+el(id).value);
    ids.forEach(id=>el(id+'-value').textContent=el(id).value);
    const post=BetaMath.posterior(a,b,s,f),cap=6;
    const W=Math.max(280,svg.clientWidth),H=svg.clientHeight,L=44,R=W-16,T=30,B=H-44;
    svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.replaceChildren();
    const X=x=>L+x*(R-L),Y=y=>B-Math.min(cap,y)/cap*(B-T);
    for(let i=0;i<=4;i++){const v=cap*i/4;node('line',{x1:L,y1:Y(v),x2:R,y2:Y(v),stroke:'#344963'});node('text',{x:L-8,y:Y(v)+4,'text-anchor':'end',fill:'#bdcce0','font-size':12},fmt(v));}
    for(let i=0;i<=5;i++){node('text',{x:X(i/5),y:B+20,'text-anchor':'middle',fill:'#bdcce0','font-size':12},fmt(i/5));}
    node('text',{x:L,y:17,fill:'#bdcce0','font-size':13},'Probability density');
    node('text',{x:(L+R)/2,y:H-5,'text-anchor':'middle',fill:'#bdcce0','font-size':13},'p — chance of heads');
    const series=[{a,b,color:'#55dbe2',name:update?'Prior':'Beta'}];
    if(update)series.push({a:post.a,b:post.b,color:'#ffbf69',name:'Posterior'});
    const warnings=[];
    series.forEach((q,index)=>{
      const points=[];let clipped=false;let firstClip=null;let penDown=false;
      for(let i=0;i<=900;i++){
        // Cosine grid resolves steep endpoint behaviour; exact finite endpoint limits retained.
        const x=(1-Math.cos(Math.PI*i/900))/2,y=BetaMath.pdf(x,q.a,q.b);
        if(y>cap){clipped=true;if(firstClip===null)firstClip=x;}
        if(y<=cap){points.push(`${penDown?'L':'M'}${X(x).toFixed(3)},${Y(y).toFixed(3)}`);penDown=true;}else{penDown=false;}
      }
      node('path',{d:points.join(' '),fill:'none',stroke:q.color,'stroke-width':2.6,...(update&&index===0?{'stroke-dasharray':'7 4'}:{})});
      const mean=BetaMath.mean(q.a,q.b);
      node('line',{x1:X(mean),x2:X(mean),y1:T,y2:B,stroke:q.color,'stroke-dasharray':'3 5',opacity:.65});
      if(clipped){node('text',{x:Math.min(R-8,Math.max(L+8,X(firstClip))),y:T+15,fill:q.color,'font-size':20,'text-anchor':'middle'},'↑');warnings.push(`${q.name} clipped above ${cap}.`);}
      if(q.a<1)warnings.push(`${q.name}: density → ∞ as p → 0.`);
      if(q.b<1){warnings.push(`${q.name}: density → ∞ as p → 1.`);if(firstClip<.5)node('text',{x:R-8,y:T+15,fill:q.color,'font-size':20,'text-anchor':'middle'},'↑');}
    });
    el('legend').innerHTML=series.map(q=>`<span style="color:${q.color}">${q.name}(${fmt(q.a)}, ${fmt(q.b)})</span>`).join('');
    el('warning').textContent=warnings.length?warnings.join(' '):'Full curve heights fit within the fixed vertical scale.';
    const m=BetaMath.mean(a,b),sd=Math.sqrt(BetaMath.variance(a,b));
    if(!update){
      const shape=a===1&&b===1?'Uniform: equal-width intervals have equal probability.':a===b&&a<1?'U-shaped: extreme probabilities receive more density than the middle.':a===b?'Symmetric about 0.5.':a>b?'Mean above 0.5.':'Mean below 0.5.';
      el('readout').innerHTML=`<b>${shape}</b><br>Mean = ${fmt(m)} · SD = ${fmt(sd)} · concentration α + β = ${fmt(a+b)}`;
    }else{
      el('readout').innerHTML=`<b>Beta(${fmt(a)}, ${fmt(b)}) → Beta(${fmt(post.a)}, ${fmt(post.b)})</b><br>Mean: ${fmt(m)} → ${fmt(post.mean)} · posterior SD: ${fmt(post.sd)}<br>Next-flip success probability: <b>${fmt(post.mean)}</b> · observed fraction: ${s+f?fmt(s/(s+f)):'not defined (no data)'}`;
    }
  }
  ids.forEach(id=>el(id).addEventListener('input',draw));
  document.querySelectorAll('[data-preset]').forEach(button=>button.addEventListener('click',()=>{button.dataset.preset.split(',').forEach((v,i)=>el(ids[i]).value=v);draw();}));
  new ResizeObserver(draw).observe(svg);draw();
})();
