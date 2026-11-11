(()=>{'use strict';
const M=JointDensityMath,$=id=>document.getElementById(id),C={green:'#128768',orange:'#d35b34',purple:'#7563c5',gray:'#87928b',text:'#33453d',grid:'#e5eae7'};
const ids=['y0','x0','rho','mux'],fmt=(v,d=2)=>(Math.abs(v)<.000001?0:v).toFixed(d).replace('-','−');
const controls=Object.fromEntries(ids.map(id=>[id,$(id)]));let state,az=-.68,elev=.6,timer=null,drag=null;
const sample=(a,b,n,fn)=>Array.from({length:n+1},(_,i)=>fn(a+(b-a)*i/n));
const node=(tag,parent,attrs={},text)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;parent.appendChild(e);return e;};
const line=(s,pts,color,width=1,dash='',fill='none',opacity=1)=>node('path',s,{d:pts.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(2)).join(',')).join(' '),stroke:color,'stroke-width':width,'stroke-dasharray':dash,fill,opacity});
function axes(svg,width,height,xrange,yrange,xlabel,ylabel){
 svg.replaceChildren();const box={l:43,r:width-14,t:14,b:height-36};
 const x=v=>box.l+(v-xrange[0])/(xrange[1]-xrange[0])*(box.r-box.l),y=v=>box.b-(v-yrange[0])/(yrange[1]-yrange[0])*(box.b-box.t);
 const defs=node('defs',svg),clip=node('clipPath',defs,{id:svg.id+'-clip'});node('rect',clip,{x:box.l,y:box.t,width:box.r-box.l,height:box.b-box.t});
 for(let i=0;i<=4;i++){const xv=xrange[0]+i*(xrange[1]-xrange[0])/4,yv=yrange[0]+i*(yrange[1]-yrange[0])/4;line(svg,[[x(xv),box.t],[x(xv),box.b]],C.grid);line(svg,[[box.l,y(yv)],[box.r,y(yv)]],C.grid);node('text',svg,{x:x(xv),y:box.b+15,'text-anchor':'middle',fill:C.text,'font-size':10},fmt(xv,1));node('text',svg,{x:box.l-6,y:y(yv)+3,'text-anchor':'end',fill:C.text,'font-size':10},fmt(yv,1));}
 node('text',svg,{x:(box.l+box.r)/2,y:height-5,'text-anchor':'middle',fill:C.text,'font-size':11},xlabel);node('text',svg,{x:box.l,y:10,fill:C.text,'font-size':10},ylabel);
 const g=node('g',svg,{'clip-path':`url(#${svg.id}-clip)`});return{x,y,g,box};
}
function conditional(svg,isX){
 const {y0,x0,rho,mux}=state,a=axes(svg,420,220,[-5,5],[0,1.4],isX?'x':'y','density');
 const fixed=isX?y0:x0,mean=isX?mux+rho*y0:rho*(x0-mux),variance=1-rho*rho;
 const density=t=>isX?M.conditionalX(t,fixed,rho,mux):M.conditionalY(t,fixed,rho,mux),raw=t=>isX?M.joint(t,fixed,rho,mux):M.joint(fixed,t,rho,mux),color=isX?C.green:C.orange;
 const pts=sample(-5,5,240,t=>[a.x(t),a.y(density(t))]);line(a.g,[[a.x(-5),a.y(0)],...pts,[a.x(5),a.y(0)]],color,.5,'',color,.14);line(a.g,pts,color,2.5);
 if($('raw').checked)line(a.g,sample(-5,5,240,t=>[a.x(t),a.y(raw(t))]),color,1.8,'5 4');
 if($('marginals').checked)line(a.g,sample(-5,5,240,t=>[a.x(t),a.y(M.phi(t-(isX?mux:0)))]),C.purple,1.2,'2 3');
 if($('means').checked){line(a.g,[[a.x(mean),a.y(0)],[a.x(mean),a.y(density(mean))]],color,1.4,'3 3');node('circle',a.g,{cx:a.x(mean),cy:a.y(0),r:3.5,fill:color});}
 const area=isX?M.phi(y0):M.phi(x0-mux),varName=isX?'X':'Y',given=isX?'Y':'X';
 $(svg.id+'-formula').textContent=`${varName} | ${given} = ${fmt(fixed)} ∼ N(${fmt(mean)}, ${fmt(variance,3)})`;
 $(svg.id+'-caption').textContent=`Raw slice area = ${fmt(area,3)}. Divide by this → conditional area = 1. Purple dots: marginal density; dashed ${isX?'green':'orange'}: raw slice.`;
}
function surface(){
 const canvas=$('surface'),ctx=canvas.getContext('2d'),rect=canvas.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);if(!rect.width)return;
 const W=680,H=490;canvas.width=Math.round(rect.width*dpr);canvas.height=Math.round(rect.height*dpr);ctx.setTransform(canvas.width/W,0,0,canvas.height/H,0,0);ctx.clearRect(0,0,W,H);
 const{y0,x0,rho,mux}=state,L=4,project=(x,y,z)=>{const p=M.project(x,y,z*10,az,elev);return[W/2+p[0]*48,260+p[1]*48];};
 const draw=(points,color,width=1,alpha=1,dash=[],fill)=>{ctx.beginPath();points.forEach((p,i)=>{const q=project(...p);i?ctx.lineTo(...q):ctx.moveTo(...q);});ctx.strokeStyle=color;ctx.lineWidth=width;ctx.globalAlpha=alpha;ctx.setLineDash(dash);if(fill){ctx.closePath();ctx.fillStyle=color;ctx.fill();}else ctx.stroke();ctx.globalAlpha=1;ctx.setLineDash([]);};
 const dot=(p,r,color)=>{const q=project(...p);ctx.beginPath();ctx.arc(q[0],q[1],r,0,2*Math.PI);ctx.fillStyle=color;ctx.fill();};
 const label=(text,p,color,dx=0,dy=0)=>{const q=project(...p);ctx.font=`${Math.max(13,12*W/rect.width)}px system-ui`;ctx.fillStyle=color;ctx.fillText(text,q[0]+dx,q[1]+dy);};
 for(let k=-4;k<=4;k++){draw([[k,-L,0],[k,L,0]],C.grid);draw([[-L,k,0],[L,k,0]],C.grid);}
 draw([[-L,-L,0],[L,-L,0],[L,L,0],[-L,L,0],[-L,-L,0]],'#bac8bf',1.2);
 if($('marginals').checked){for(const isX of [true,false]){const pts=sample(-L,L,100,t=>isX?[t,L,M.phi(t-mux)]:[-L,t,M.phi(t)]);const ends=isX?[[-L,L,0],[L,L,0]]:[[-L,-L,0],[-L,L,0]];draw([ends[0],...pts,ends[1]],C.purple,1,.11,[],true);draw(pts,C.purple,2,.8);}label('pX(x)',[mux,L,.42],C.purple,2,-3);label('pY(y)',[-L,0,.42],C.purple,-20,-6);}
 const mesh=[];for(let k=-4;k<=4.001;k+=.3){mesh.push(sample(-L,L,65,t=>[k,t,M.joint(k,t,rho,mux)]));mesh.push(sample(-L,L,65,t=>[t,k,M.joint(t,k,rho,mux)]));}for(const pts of mesh)draw(pts,C.gray,.7,.5);
 const xs=sample(-L,L,140,x=>[x,y0,M.joint(x,y0,rho,mux)]),ys=sample(-L,L,140,y=>[x0,y,M.joint(x0,y,rho,mux)]);
 draw([[-L,y0,0],...xs,[L,y0,0]],C.green,1,.19,[],true);draw(xs,C.green,2.2);draw([[x0,-L,0],...ys,[x0,L,0]],C.orange,1,.17,[],true);draw(ys,C.orange,2.2);
 if($('marginals').checked){draw([[-L,y0,0],[-L,y0,M.phi(y0)]],C.green,1.4,1,[4,3]);dot([-L,y0,M.phi(y0)],4,C.green);draw([[x0,L,0],[x0,L,M.phi(x0-mux)]],C.orange,1.4,1,[4,3]);dot([x0,L,M.phi(x0-mux)],4,C.orange);}
 if($('means').checked){const trace=sample(-4,4,80,y=>[mux+rho*y,y,0]).filter(p=>Math.abs(p[0])<=L);draw(trace,C.green,2,1,[5,4]);for(let y=-3;y<=3.001;y+=.5){const x=mux+rho*y;if(Math.abs(x)<=L)dot([x,y,0],Math.sqrt(M.phi(y)*.5)*16,C.green+'88');}draw([[mux,-L,0],[mux,L,0]],C.purple,1.6,1,[4,4]);const m=mux+rho*y0;if(Math.abs(m)<=L){draw([[m,y0,0],[m,y0,M.joint(m,y0,rho,mux)]],C.green,1.3,1,[3,3]);dot([m,y0,0],5,C.green);}dot([mux,0,0],6,C.purple);}
 draw([[-L,-L,0],[-L,-L,.55]],'#74867b',1.1);label('density',[-L,-L,.55],C.text,-24,-7);label('x',[L,-L,0],C.text,6,12);label('y',[L,L,0],C.text,8,12);
 ctx.font=`${Math.max(12,11*W/rect.width)}px system-ui`;ctx.fillStyle=C.green;ctx.fillText(`y₀ = ${fmt(y0)}    slice area = ${fmt(M.phi(y0),3)}`,12,454);ctx.fillStyle=C.orange;ctx.fillText(`x₀ = ${fmt(x0)}    slice area = ${fmt(M.phi(x0-mux),3)}`,12,479);
}
function weighted(){
 const{rho,mux,y0}=state,a=axes($('weighted'),600,255,[-4,4],[-5.5,5.5],'conditioning value y','conditional mean m(y)');
 line(a.g,[[a.x(-4),a.y(mux)],[a.x(4),a.y(mux)]],C.purple,1.5,'5 4');
 line(a.g,[[a.x(-4),a.y(mux-4*rho)],[a.x(4),a.y(mux+4*rho)]],C.green,2);
 for(let y=-3;y<=3.001;y+=.5)node('circle',a.g,{cx:a.x(y),cy:a.y(mux+rho*y),r:Math.sqrt(M.phi(y)*.5)*24,fill:C.green,opacity:.25});
 line(a.g,[[a.x(y0),a.y(-5.5)],[a.x(y0),a.y(mux+rho*y0)]],C.green,1,'3 3');node('circle',a.g,{cx:a.x(y0),cy:a.y(mux+rho*y0),r:5,fill:C.green});
 node('text',$('weighted'),{x:a.box.r-3,y:a.y(mux)-7,'text-anchor':'end',fill:C.purple,'font-size':11},`E[X] = ${fmt(mux)}`);
 $('selected-mean').textContent=fmt(mux+rho*y0);$('overall-mean').textContent=`E[E[X | Y]] = ${fmt(mux)}`;$('conditional-var').textContent=`1 − ρ² = ${fmt(1-rho*rho,3)}`;
 $('explanation').textContent=Math.abs(rho)<.001?'At ρ = 0, both conditional densities equal their marginals: X and Y are independent in this jointly Gaussian model. Moving a slice changes its raw area, but not the normalized density.':'Changing the slice changes its conditional mean. Averaging all those means with Y’s own probability weights gives μₓ. Try shifting μₓ: the selected means and their overall average move together.';
}
function render(){state=Object.fromEntries(ids.map(id=>[id,Number(controls[id].value)]));for(const id of ids)$(id+'-out').textContent=fmt(state[id]);conditional($('cx'),true);conditional($('cy'),false);surface();weighted();}
function stop(){if(timer){clearInterval(timer);timer=null;}$('play').textContent='Play y₀ sweep';}
for(const input of Object.values(controls))input.addEventListener('input',()=>{stop();render();});for(const id of ['marginals','means','raw'])$(id).addEventListener('change',render);
const preset=values=>{stop();for(const[k,v]of Object.entries(values))controls[k].value=v;render();};
$('reference').addEventListener('click',()=>preset({y0:-1.3,x0:1,rho:.8,mux:0}));$('independent').addEventListener('click',()=>preset({rho:0}));$('negative').addEventListener('click',()=>preset({rho:-.8}));
$('play').addEventListener('click',()=>{if(timer){stop();return;}let direction=1;const slow=window.matchMedia('(prefers-reduced-motion: reduce)').matches;timer=setInterval(()=>{let next=Number(controls.y0.value)+direction*.05;if(next>2.5||next< -2.5){direction*=-1;next=Number(controls.y0.value)+direction*.05;}controls.y0.value=next;render();},slow?350:90);$('play').textContent='Pause y₀ sweep';});
$('reset-view').addEventListener('click',()=>{az=-.68;elev=.6;surface();});const canvas=$('surface');canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY,az,elev];canvas.setPointerCapture(e.pointerId);});canvas.addEventListener('pointermove',e=>{if(!drag)return;az=drag[2]+(e.clientX-drag[0])*.006;elev=Math.max(.25,Math.min(1.05,drag[3]+(e.clientY-drag[1])*.005));surface();});for(const type of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,()=>{drag=null;});canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key))return;e.preventDefault();if(e.key==='ArrowLeft')az-=.1;if(e.key==='ArrowRight')az+=.1;if(e.key==='ArrowUp')elev=Math.min(1.05,elev+.05);if(e.key==='ArrowDown')elev=Math.max(.25,elev-.05);surface();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);new ResizeObserver(()=>surface()).observe(canvas);render();
})();
