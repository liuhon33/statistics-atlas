(() => {
  const $ = id => document.getElementById(id);
  const presets = {study:[-4,.8,5],decreasing:[4,-.8,5],flat:[0,0,5],steep:[-10,2,5]};
  const fmt = n => Math.abs(n) >= 10000 || (Math.abs(n) < .001 && n !== 0) ? n.toExponential(3) : n.toFixed(4);
  const svgText = (x,y,text,anchor='middle',color='#607382') => `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${color}" font-size="13">${text}</text>`;
  function plot(id,b0,b1,selected,isSlope) {
    const left=58,right=480,top=20,bottom=267;
    const ymin=isSlope?-.5:0, ymax=isSlope?.5:1;
    const sx=x=>left+x/10*(right-left),sy=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);
    let html='';
    for(const x of [0,2,4,6,8,10]) {
      html+=`<line x1="${sx(x)}" x2="${sx(x)}" y1="${top}" y2="${bottom}" stroke="#e1e8ed"/>`+svgText(sx(x),bottom+23,x);
    }
    for(const y of isSlope?[-.5,-.25,0,.25,.5]:[0,.25,.5,.75,1]) {
      html+=`<line x1="${left}" x2="${right}" y1="${sy(y)}" y2="${sy(y)}" stroke="${y===0?'#90a1ad':'#e1e8ed'}"/>`+svgText(left-9,sy(y)+4,y,'end');
    }
    const points=[];
    for(let i=0;i<=250;i++) {
      const x=i/25,v=LogisticMath.values(b0,b1,x);
      points.push(`${i?'L':'M'}${sx(x).toFixed(3)},${sy(isSlope?v.slope:v.p).toFixed(3)}`);
    }
    const color=isSlope?'#7757a6':'#176b91', v=LogisticMath.values(b0,b1,selected);
    html+=`<path d="${points.join(' ')}" fill="none" stroke="${color}" stroke-width="3"/>`;
    html+=`<line x1="${sx(selected)}" x2="${sx(selected)}" y1="${top}" y2="${bottom}" stroke="#bc6429" stroke-dasharray="4 4"/>`;
    html+=`<circle cx="${sx(selected)}" cy="${sy(isSlope?v.slope:v.p)}" r="5" fill="#bc6429"/>`;
    html+=svgText((left+right)/2,312,'Predictor x');
    $(id).innerHTML=html;
  }
  function render() {
    const b0=+$('b0').value,b1=+$('b1').value,x=+$('x').value;
    const v=LogisticMath.values(b0,b1,x);
    for(const id of ['b0','b1','x']) $(id+'-value').textContent=(+$(id).value).toFixed(2);
    $('formula').textContent=`η = ${b0.toFixed(2)} ${b1<0?'−':'+'} ${Math.abs(b1).toFixed(2)}x;  p = 1 / (1 + exp(−η))`;
    $('p-out').textContent=(100*v.p).toFixed(2)+'%';$('odds-out').textContent=fmt(v.odds);
    $('eta-out').textContent=v.eta.toFixed(3);$('slope-out').textContent=fmt(v.slope);
    const middle=b1===0?'There is no unique midpoint: the model is flat.':`The p = 0.5 midpoint is x = ${(-b0/b1).toFixed(2)}${(-b0/b1<0||-b0/b1>10)?' (outside this window)':''}.`;
    $('interpretation').textContent=`At x = ${x.toFixed(1)}, the local probability change is ${(100*v.slope).toFixed(2)} percentage points per unit of x. ${middle}`;
    plot('probability',b0,b1,x,false);plot('derivative',b0,b1,x,true);
  }
  for(const id of ['b0','b1','x']) $(id).addEventListener('input',render);
  document.querySelectorAll('[data-preset]').forEach(button=>button.addEventListener('click',()=>{
    presets[button.dataset.preset].forEach((v,i)=>$( ['b0','b1','x'][i]).value=v);render();
  }));
  render();
})();
