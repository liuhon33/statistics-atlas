(() => {
  const root = document.querySelector('main'), mode = root.dataset.mode;
  const blue='#307eae', amber='#d49b43', gray='#e6ebf0', purple='#8664b7';
  const pct=x=>(100*x).toFixed(1)+'%', fmt=x=>x.toFixed(4);
  const rect=(x,y,w,h,c)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${c}" stroke="white"/>`;
  const txt=(x,y,s,anchor='start')=>`<text x="${x}" y="${y}" text-anchor="${anchor}">${s}</text>`;
  const svg=(inner,h)=>`<svg viewBox="0 0 780 ${h}" role="img" aria-label="${mode==='elbo'?'Approximate and exact posterior shares':'Prior widths, evidence heights, and posterior shares'}">${inner}</svg>`;
  const metric=(label,value)=>`<div class="metric">${label}<strong>${value}</strong></div>`;
  const range=(id,label,v,min=0,max=1,step=.001)=>`<label for="${id}">${label}: <output id="${id}-value"></output><input type="range" id="${id}" min="${min}" max="${max}" step="${step}" value="${v}"></label>`;
  let title, intro, controls, buttons;
  if(mode==='bayes'){
    title='Width × height → retained area';
    intro='Steve is either a librarian (blue) or farmer (amber). The shaded areas are cases that fit the description. These are illustrative assumptions.';
    controls=range('prior','Prior: librarian',1/21,0,1,'any')+range('lh','Fits description: librarian',.4)+range('lf','Fits description: farmer',.1);
    buttons='<button id="reset">Steve example</button><button id="equal">Equal likelihoods</button><button id="impossible">Impossible evidence</button>';
  }else if(mode==='elbo'){
    title='Fit the normalized rectangle shares';
    intro='Steve’s model stays fixed: prior (1/21, 20/21), likelihood (.4, .1), exact posterior (1/6, 5/6). Only q changes. All log values use natural logarithms (nats).';
    controls=range('r','q(librarian)',.5,0,1,'any');
    buttons='<button id="reset">q = 50–50</button><button id="prior-q">q = prior</button><button id="posterior-q">q = posterior</button>';
  }else{
    title='What does Monty’s reveal retain?';
    intro='You chose door 1. Evidence E: the host opens door 3 and shows a goat. The car is initially equally likely behind each door.';
    controls='<label for="policy">Host policy<select id="policy"><option value="informed">Knows the car location</option><option value="blind">Opens door 2 or 3 blindly</option></select></label>'+range('bias','If car is at 1: chance host opens 3',.5);
    buttons='<button id="reset">Standard fair host</button><button id="always-three">Always opens 3 when allowed</button>';
  }
  root.innerHTML=`<h1>${title}</h1><p class="sub">${intro}</p><div class="controls">${controls}</div><div class="buttons">${buttons}</div><div id="graphic" class="figure"></div><div id="metrics" class="metrics" aria-live="polite"></div><p id="explanation" class="tip"></p>`;
  const get=id=>document.getElementById(id), value=id=>Number(get(id).value);
  function areas(prior, likelihood, post, names, colors){
    let s='', x=0;
    prior.forEach((p,i)=>{s+=rect(x,0,720*p,210,gray)+rect(x,210-210*likelihood[i],720*p,210*likelihood[i],colors[i]);x+=720*p;});
    const top=`<svg viewBox="0 0 720 210" role="img" aria-label="Prior widths multiplied by likelihood heights">${s}</svg>`;
    const rows=names.map((n,i)=>`<div><strong>${n}</strong>Width ${pct(prior[i])} × height ${pct(likelihood[i])} = area ${fmt(prior[i]*likelihood[i])}</div>`).join('');
    s='';x=0;
    if(post)post.forEach((p,i)=>{s+=rect(x,0,720*p,52,colors[i]);x+=720*p;});
    const bottom=post?`<svg viewBox="0 0 720 52" role="img" aria-label="Normalized posterior shares">${s}</svg><p>${post.map((p,i)=>`${names[i]}: ${pct(p)}`).join(' · ')}</p>`:'<p class="warning">No retained area: conditioning is undefined.</p>';
    return `<h3>1. Prior widths × evidence heights</h3>${top}<p class="sub">Whole area = 1. Height runs from 0 at the bottom to 1 at the top.</p><div class="breakdown">${rows}</div><h3>2. Normalize the retained areas</h3>${bottom}`;
  }
  function update(){
    if(mode==='bayes'){
      const p=value('prior'), a=value('lh'), b=value('lf'), z=BayesMath.steve(p,a,b);
      for(const [id,v] of [['prior',p],['lh',a],['lf',b]])get(id+'-value').textContent=pct(v);
      get('graphic').innerHTML=areas([p,1-p],[a,b],z.posterior,['Librarian','Farmer'],[blue,amber]);
      get('metrics').innerHTML=metric('Total retained area P(E)',fmt(z.evidence))+metric('P(librarian | E)',z.posterior?pct(z.posterior[0]):'Undefined');
      get('explanation').textContent=!z.posterior?'Both retained areas are zero. The model assigns this evidence probability zero, so Bayes cannot normalize it.':Math.abs(a-b)<1e-10?'Equal positive likelihoods retain the same fraction of both groups: the posterior equals the prior.':'Try equal likelihoods, then raise only the librarian height. Watch the posterior change while the prior widths stay fixed.';
    }else if(mode==='elbo'){
      const r=value('r'), z=BayesMath.elbo(r);get('r-value').textContent=pct(r);
      const strip=(p,label)=>`<svg viewBox="0 0 720 45" role="img" aria-label="${label}">${rect(0,0,720*p,45,blue)+rect(720*p,0,720*(1-p),45,amber)}</svg>`;
      const bars=`<h3>Exact posterior shares (fixed)</h3>${strip(1/6,'Exact posterior')}<p>Librarian 16.7% · Farmer 83.3%</p><h3>Approximation q</h3>${strip(r,'Approximate posterior')}<p>Librarian ${pct(r)} · Farmer ${pct(1-r)}</p>`;
      const px=x=>75+650*x, py=y=>30+220*(-2.0-y)/2.1;
      let s=`<line x1="75" y1="250" x2="725" y2="250" stroke="#607086"/><line x1="75" y1="30" x2="75" y2="250" stroke="#607086"/>`;
      s+=`<line x1="75" y1="${py(z.logEvidence)}" x2="725" y2="${py(z.logEvidence)}" stroke="#607086" stroke-dasharray="6 4"/>`;
      const d=Array.from({length:201},(_,i)=>`${i?'L':'M'}${px(i/200)},${py(BayesMath.elbo(i/200).bound)}`).join(' ');
      s+=`<path d="${d}" fill="none" stroke="${purple}" stroke-width="3"/><line x1="${px(r)}" y1="${py(z.bound)}" x2="${px(r)}" y2="${py(z.logEvidence)}" stroke="${blue}" stroke-width="3"/><circle cx="${px(r)}" cy="${py(z.bound)}" r="5" fill="${purple}"/>`;
      for(const y of [-2,-3,-4])s+=txt(62,py(y)+7,String(y),'end');
      s+=txt(75,282,'0')+txt(725,282,'1','end')+txt(400,282,'r = q(librarian)','middle');
      get('graphic').innerHTML=bars+'<h3>ELBO and posterior KL (nats)</h3><p>Dashed: log evidence = −2.1691.</p>'+svg(s,310)+'<p>Purple: ELBO. Blue gap: KL(q || posterior).</p>';
      get('metrics').innerHTML=metric('ELBO',fmt(z.bound))+metric('Posterior KL gap',fmt(Math.max(0,z.gap)))+metric('Expected log likelihood',fmt(z.fit))+metric('Prior KL',fmt(Math.max(0,z.priorKL)));
      get('explanation').textContent='At q = posterior, the bound reaches log evidence and posterior KL is zero. Prior KL need not be zero. At q = prior, prior KL is zero, but the posterior gap remains.';
    }else{
      const blind=get('policy').value==='blind', t=value('bias'), z=BayesMath.monty(t,blind);get('bias').disabled=blind;get('bias-value').textContent=blind?'not used':pct(t);
      get('graphic').innerHTML=areas([1/3,1/3,1/3],blind?[.5,.5,0]:[t,1,0],z.posterior,['Car at 1','Car at 2','Car at 3'],[blue,amber,'#9aa7b5']);
      get('metrics').innerHTML=metric('P(E)',fmt(z.evidence))+metric('Stay, given E',pct(z.posterior[0]))+metric('Switch, given E',pct(z.posterior[1]));
      get('explanation').textContent=blind?'A blind host produces this exact goat reveal half the time under either surviving car location. Equal heights give 50–50. Games where the car is revealed are excluded by E.':'A knowledgeable host must open door 3 when the car is at 2. When the car is at 1, the host has a choice. The slider changes that choice rule; the conditional answer can change, while always switching still wins 2/3 before any reveal.';
    }
  }
  root.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',update));
  get('reset').addEventListener('click',()=>{if(mode==='bayes'){get('prior').value=1/21;get('lh').value=.4;get('lf').value=.1;}else if(mode==='elbo')get('r').value=.5;else{get('policy').value='informed';get('bias').value=.5;}update();});
  const on=(id,fn)=>{if(get(id))get(id).addEventListener('click',()=>{fn();update();});};
  on('equal',()=>{get('lh').value=.4;get('lf').value=.4;});
  on('impossible',()=>{get('lh').value=0;get('lf').value=0;});
  on('prior-q',()=>{get('r').value=1/21;});on('posterior-q',()=>{get('r').value=1/6;});
  on('always-three',()=>{get('policy').value='informed';get('bias').value=1;});
  update();
})();
