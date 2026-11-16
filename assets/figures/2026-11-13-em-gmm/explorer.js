(() => {
  'use strict';
  const $ = id => document.getElementById(id), xs = EMToy.data(), colors = ['#3b6cef', '#ef5b52'];
  let p, r = null, qIteration = null, iteration = 0, next = 'E', logL = 0, deltaL = null, deltaQ = null, history = [], timer = null, converged = false;
  const f = (x, d = 3) => Number.isFinite(x) ? x.toFixed(d) : '—';
  const sx = x => 55 + (x + 3.5) * 520 / 7, sy = y => 550 - (y + 3.5) * 520 / 7;
  const path = points => points.map((p, i) => `${i ? 'L' : 'M'}${f(sx(p[0]), 2)},${f(sy(p[1]), 2)}`).join(' ');
  function stop() { if (timer !== null) clearInterval(timer); timer = null; $('play').textContent = 'Play'; }
  function reset() {
    stop(); $('error').hidden = true;
    try {
      const controls = ['m00','m01','m10','m11','weight','spread'].map($);
      if (controls.some(e => e.value === '' || !e.checkValidity())) throw Error('Use starting means between −3 and 3, weight 0.1–0.9, and standard deviation 0.2–1.6.');
      p = EMToy.initialize($('preset').value, +$('weight').value, +$('spread').value, [[+$('m00').value,+$('m01').value],[+$('m10').value,+$('m11').value]]);
      r = null; qIteration = null; iteration = 0; next = 'E'; deltaL = deltaQ = null; converged = false;
      logL = EMToy.expectation(xs, p).logLikelihood; history = [logL]; render();
    } catch (error) { fail(error); }
  }
  function fail(error) { stop(); $('error').textContent = error.message; $('error').hidden = false; $('eStep').disabled = $('mStep').disabled = $('iterate').disabled = $('play').disabled = true; }
  function eStep() {
    const result = EMToy.expectation(xs, p); r = result.r; qIteration = iteration; next = 'M'; deltaL = deltaQ = null; render();
  }
  function mStep() {
    const before = EMToy.qValue(xs, r, p), candidate = EMToy.maximization(xs, r), after = EMToy.expectation(xs, candidate).logLikelihood;
    const gainQ = EMToy.qValue(xs, r, candidate) - before;
    if (after < logL - 1e-7 || gainQ < -1e-7) throw Error('Numerical monotonicity check failed; no update applied. Reset to a different start.');
    deltaL = after - logL; deltaQ = gainQ; p = candidate; logL = after; iteration++; next = 'E'; history.push(logL);
    converged = iteration >= 2 && deltaL <= 1e-8 * (1 + Math.abs(logL));
    if (converged || iteration >= 60) stop(); render();
  }
  function step() { if (next === 'E') eStep(); else mStep(); }
  function safe(action) { try { action(); } catch (error) { fail(error); } }
  function scatter() {
    let s = '<title>Fixed observations and fitted Gaussian components</title><defs><clipPath id="plotclip"><rect x="55" y="30" width="520" height="520"/></clipPath></defs>';
    for (let i = -3; i <= 3; i++) s += `<path d="M${sx(i)},30V550 M55,${sy(i)}H575" stroke="#35445f" stroke-width="1"/><text x="${sx(i)}" y="572" fill="#b6c4dc" text-anchor="middle" font-size="13">${i}</text><text x="43" y="${sy(i)+4}" fill="#b6c4dc" text-anchor="end" font-size="13">${i}</text>`;
    s += '<text x="315" y="601" fill="#d5deee" text-anchor="middle" font-size="15">Observed feature x₁</text><text x="15" y="290" transform="rotate(-90 15 290)" fill="#d5deee" text-anchor="middle" font-size="15">Observed feature x₂</text><g clip-path="url(#plotclip)">';
    xs.forEach((x, i) => {
      const v = r ? r[i][0] : null, color = v === null ? '#73cf9b' : `rgb(${Math.round(59*v+239*(1-v))},${Math.round(108*v+91*(1-v))},${Math.round(239*v+82*(1-v))})`;
      s += `<circle data-point="${i+1}" cx="${sx(x[0])}" cy="${sy(x[1])}" r="3.8" fill="${color}" opacity="0.87"><title>Point ${i+1}: (${f(x[0],2)}, ${f(x[1],2)})${v===null?'':`; stored r₁=${f(v)}`}</title></circle>`;
    });
    const selected = xs[+$('point').value - 1];
    s += `<circle cx="${sx(selected[0])}" cy="${sy(selected[1])}" r="8" stroke="#ffe095" stroke-width="2.5" fill="none" pointer-events="none"/>`;
    p.means.forEach((mean,k) => {
      [1,2].forEach(radius => { s += `<path d="${path(EMToy.ellipse(mean,p.covs[k],radius))} Z" fill="none" stroke="${colors[k]}" stroke-width="${radius===1?3:2}" stroke-dasharray="${radius===2?'7 4':'none'}"/>`; });
      const x=sx(mean[0]), y=sy(mean[1]); s += `<path d="M${x-7},${y}h14 M${x},${y-7}v14" stroke="white" stroke-width="5"/><path d="M${x-7},${y}h14 M${x},${y-7}v14" stroke="${colors[k]}" stroke-width="3"/>`;
    });
    $('scatter').innerHTML = s + '</g>';
  }
  function trace() {
    const low = Math.min(...history)-5, high=Math.max(...history)+5, maxX=Math.max(5,iteration);
    const x=i=>80+740*i/maxX, y=v=>125-100*(v-low)/(high-low);
    let s=`<path d="M80,15V125H820" fill="none" stroke="#8194b5"/><text x="70" y="24" text-anchor="end" fill="#b6c4dc" font-size="13">${f(high,0)}</text><text x="70" y="130" text-anchor="end" fill="#b6c4dc" font-size="13">${f(low,0)}</text><text x="80" y="150" fill="#b6c4dc" font-size="13">0</text><text x="820" y="150" text-anchor="end" fill="#b6c4dc" font-size="13">${maxX}</text><text x="450" y="163" text-anchor="middle" fill="#b6c4dc" font-size="13">Completed M-steps</text>`;
    s+=`<path d="${history.map((v,i)=>`${i?'L':'M'}${x(i)},${y(v)}`).join(' ')}" fill="none" stroke="#e9c66e" stroke-width="3"/>`;
    history.forEach((v,i)=>{s+=`<circle cx="${x(i)}" cy="${y(v)}" r="3" fill="#e9c66e"/>`;}); $('trace').innerHTML=s;
  }
  function render() {
    $('iteration').textContent=iteration; $('likelihood').textContent=f(logL); $('deltaL').textContent=deltaL===null?'—':f(deltaL,6); $('deltaQ').textContent=deltaQ===null?'—':f(deltaQ,6);
    let status = r===null ? 'Initialized θ⁽⁰⁾. The green points have not been assigned posterior colors. Next: E-step.' : next==='M' ? `E-step at θ⁽${iteration}⁾: colors now show its posterior probabilities. θ and the observed log-likelihood did not change. Next: M-step.` : `M-step ${iteration}: centers, covariances and mixing weights updated. Colors are still frozen from E at θ⁽${qIteration}⁾. Next E-step refreshes them.`;
    if (converged) status+=' Small likelihood gain: playback stopped (not a global-optimum certificate).';
    if (iteration>=60) status+=' Demo limit: 60 iterations; Reset to run again.';
    $('phase').textContent=status;
    $('eStep').disabled=next!=='E'||iteration>=60; $('mStep').disabled=next!=='M'||iteration>=60; $('iterate').disabled=iteration>=60; $('play').disabled=iteration>=60;
    $('parameters').innerHTML=p.means.map((mean,k)=>`<div class="component ${k?'red':'blue'}"><strong>${k?'Red · k = 2':'Blue · k = 1'}</strong><code>π = ${f(p.weights[k])}; μ = (${f(mean[0],2)}, ${f(mean[1],2)})<br>Σ = [${f(p.covs[k][0][0],2)}, ${f(p.covs[k][0][1],2)};<br>　　 ${f(p.covs[k][1][0],2)}, ${f(p.covs[k][1][1],2)}]<br>Stored E-step count Nₖ = ${r?f(r.reduce((s,v)=>s+v[k],0),2):'not computed'}</code></div>`).join('');
    const i=+$('point').value-1; $('pointNumber').textContent=i+1;
    $('pointReadout').innerHTML=`x = (${f(xs[i][0],2)}, ${f(xs[i][1],2)})<br>${r?`Stored rₙ₁ = <strong>${f(r[i][0],4)}</strong><br>Stored rₙ₂ = <strong>${f(r[i][1],4)}</strong><br>Posterior computed at θ⁽${qIteration}⁾.`:'Press E-step to compute membership probabilities.'}`;
    scatter(); trace();
  }
  $('eStep').addEventListener('click',()=>{stop();safe(eStep);}); $('mStep').addEventListener('click',()=>{stop();safe(mStep);});
  $('iterate').addEventListener('click',()=>{stop();safe(()=>{if(next==='E')eStep();mStep();});});
  $('play').addEventListener('click',()=>{if(timer!==null){stop();return;} converged=false; $('play').textContent='Pause'; timer=setInterval(()=>safe(step),matchMedia('(prefers-reduced-motion: reduce)').matches?1600:900);});
  $('reset').addEventListener('click',reset); $('point').addEventListener('input',render);
  $('scatter').addEventListener('click',e=>{const point=e.target.closest('[data-point]'); if(point){$('point').value=point.dataset.point;render();}});
  $('preset').addEventListener('change',()=>{const means=EMToy.presets[$('preset').value].means; for(let k=0;k<2;k++)for(let j=0;j<2;j++)$('m'+k+j).value=means[k][j]; $('weight').value=.5; $('spread').value=.7;reset();});
  ['m00','m01','m10','m11','weight','spread'].forEach(id=>$(id).addEventListener('input',reset));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();}); window.addEventListener('pagehide',stop); reset();
})();
