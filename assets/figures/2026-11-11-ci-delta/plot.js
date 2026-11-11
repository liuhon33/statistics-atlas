(()=>{'use strict';
 const C={blue:'#3975b7',orange:'#cd7134',green:'#16866c',purple:'#8060b5',red:'#b64f56',ink:'#344640',muted:'#6c7b75',grid:'#e4e9e5'};
 const el=(tag,parent,attrs={},text)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;parent.appendChild(e);return e;};
 const fmt=(x,d=3)=>{if(Math.abs(x)<1e-12)return'0';if(Math.abs(x)>=10000||Math.abs(x)<.0001)return x.toExponential(2).replace('-','−');return Number(x.toFixed(d)).toString().replace('-','−');};
 function plot(id,xr,yr,xlabel,ylabel,square=false){const svg=document.getElementById(id),W=500,H=square?500:264;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.replaceChildren();const l=53,r=481,t=23,b=square?451:217;const x=v=>l+(v-xr[0])/(xr[1]-xr[0])*(r-l),y=v=>b-(v-yr[0])/(yr[1]-yr[0])*(b-t);const defs=el('defs',svg),clip=el('clipPath',defs,{id:id+'-clip'});el('rect',clip,{x:l,y:t,width:r-l,height:b-t});
  const xdigits=Math.max(2,Math.min(5,2-Math.floor(Math.log10((xr[1]-xr[0])/4))));
  const ydigits=square?xdigits:2;
  for(let k=0;k<=4;k++){const xx=xr[0]+k*(xr[1]-xr[0])/4,yy=yr[0]+k*(yr[1]-yr[0])/4;el('line',svg,{x1:x(xx),x2:x(xx),y1:t,y2:b,stroke:C.grid});el('line',svg,{x1:l,x2:r,y1:y(yy),y2:y(yy),stroke:C.grid});el('text',svg,{x:x(xx),y:b+17,'text-anchor':'middle','font-size':11,fill:C.muted},fmt(xx,xdigits));el('text',svg,{x:l-7,y:y(yy)+4,'text-anchor':'end','font-size':11,fill:C.muted},fmt(yy,ydigits));}
  el('text',svg,{x:(l+r)/2,y:H-8,'text-anchor':'middle','font-size':12,fill:C.ink},xlabel);el('text',svg,{x:l,y:13,'font-size':11,fill:C.ink},ylabel);const g=el('g',svg,{'clip-path':`url(#${id}-clip)`});return{svg,g,x,y,xr,yr,l,r,t,b};
 }
 function path(p,points,color,width=2,dash='',fill='none',opacity=1){return el('path',p.g,{d:points.map((q,i)=>(i?'L':'M')+p.x(q[0]).toFixed(3)+','+p.y(q[1]).toFixed(3)).join(' '),stroke:color,'stroke-width':width,'stroke-dasharray':dash,fill,opacity});}
 const sample=(a,b,n,fn)=>Array.from({length:n+1},(_,i)=>{const x=a+(b-a)*i/n;return[x,fn(x)];});
 const curve=(p,fn,color,width=2,dash='')=>path(p,sample(...p.xr,360,fn),color,width,dash);
 const dot=(p,x,y,color,r=4)=>el('circle',p.g,{cx:p.x(x),cy:p.y(y),r,fill:color,stroke:'white','stroke-width':1});
 const vline=(p,x,color,dash='4 4',width=1)=>path(p,[[x,p.yr[0]],[x,p.yr[1]]],color,width,dash);
 const hline=(p,y,color,dash='4 4',width=1)=>path(p,[[p.xr[0],y],[p.xr[1],y]],color,width,dash);
 const area=(p,points,color,alpha=.15)=>path(p,[[points[0][0],0],...points,[points.at(-1)[0],0]],color,0,'',color,alpha);
 window.InferencePlot={C,el,fmt,plot,path,sample,curve,dot,vline,hline,area};
})();
