(() => {
const cloud=document.getElementById('cloud'),strip=document.getElementById('strip');
const angle=document.getElementById('angle');
const line=(x1,y1,x2,y2,color,width=1)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}"/>`;
const text=(x,y,label,anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="13">${label}</text>`;
const dot=(x,y,color,r=4)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${color}"/>`;
const pos=p=>[220+p[0]*28,205-p[1]*28];
function draw(){
 const degrees=Number(angle.value),s=PcaMath.project(degrees);
 document.getElementById('angle-label').textContent=degrees+'°';
 let plot='';
 for(let t=-6;t<=6;t+=2){plot+=line(...pos([t,-6]),...pos([t,6]),'#e9edf0');plot+=line(...pos([-6,t]),...pos([6,t]),'#e9edf0');plot+=text(pos([t,0])[0],390,t);plot+=text(35,pos([0,t])[1]+4,t);}
 plot+=line(...pos([-6,0]),...pos([6,0]),'#b8c3ce');plot+=line(...pos([0,-6]),...pos([0,6]),'#b8c3ce');
 plot+=line(...pos(s.v.map(x=>-7*x)),...pos(s.v.map(x=>7*x)),'#d97724',2.5);
 PcaMath.points.forEach((p,i)=>{plot+=line(...pos(p),...pos(s.feet[i]),'#929da8');});
 PcaMath.points.forEach(p=>{plot+=dot(...pos(p),'#2864a0',4.5);});
 s.feet.forEach(p=>{plot+=dot(...pos(p),'#d97724',3.8);});
 plot+=text(220,421,'Measurement A, centered');
 plot+='<text transform="translate(14 205) rotate(-90)" text-anchor="middle" font-size="13">Measurement B, centered</text>';
 cloud.innerHTML=plot;
 let row=line(35,80,405,80,'#d97724',2);
 for(let t=-6;t<=6;t+=2){row+=line(220+t*27,75,220+t*27,85,'#263447');row+=text(220+t*27,111,t);}
 // Vertical offsets only separate coincident markers; vertical position is not a second score.
 s.scores.forEach((t,i)=>{row+=dot(220+t*27,80+(i%3-1)*13,'#d97724',5);});
 row+=text(220,144,'One score per sample');row+=text(220,170,'Small vertical offsets reveal overlapping dots');
 strip.innerHTML=row;
 document.getElementById('variance').textContent=s.variance.toFixed(4);
 document.getElementById('error').textContent=s.error.toFixed(4);
 document.getElementById('fraction').textContent=(100*s.fraction).toFixed(2)+'%';
 document.getElementById('hint').textContent=degrees===45?'PC1 keeps the most variance. Its reconstruction has the least squared error.':degrees===135?'This is PC2. Keeping this direction alone discards the larger PC1 variation.':'Rotate the line toward 45° to retain more of this dataset’s variation.';
}
angle.addEventListener('input',draw);
for(const [id,value] of [['pc1',45],['horizontal',0],['pc2',135]])document.getElementById(id).addEventListener('click',()=>{angle.value=value;draw();});
draw();
})();
