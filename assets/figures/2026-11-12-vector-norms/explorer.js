(() => {
  const $ = id => document.getElementById(id);
  const X = x => 240 + 166 * x, Y = y => 240 - 166 * y;
  const fmt = x => Number.isInteger(x) ? String(x) : x.toFixed(4);
  function render(p) {
    const zero = p === 0, inf = p === Infinity, valid = p >= 1;
    $('p-value').textContent = zero ? 'ℓ₀ count selected' : inf ? '∞ selected' : p.toFixed(2);
    if (!zero && !inf) $('p').value = p;
    document.querySelectorAll('[data-p]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.p) === p)));
    $('measure-name').textContent = zero ? 'Support count (ℓ₀)' : inf ? 'Maximum norm (ℓ∞)' : p === 1 ? 'Sum of magnitudes (ℓ₁)' : p === 2 ? 'Euclidean norm (ℓ₂)' : `p = ${fmt(p)}`;
    $('formula').textContent = zero ? 'Count the coordinates that are not zero.' : inf ? 'Size = maxᵢ |vᵢ|' : `Size = (Σᵢ |vᵢ|ᵖ)¹ᐟᵖ, with p = ${fmt(p)}`;
    $('classification').textContent = zero ? 'Not a norm: homogeneity fails' : valid ? 'A norm: the unit ball is convex' : 'Not a norm: triangle inequality fails';
    $('classification').className = 'badge' + (valid ? '' : ' invalid');
    $('meaning').textContent = zero ? 'At most one nonzero coordinate is allowed. Its magnitude is unrestricted. The origin is included in size ≤ 1.' : inf ? 'Both coordinates lie between −1 and 1: a square.' : p === 1 ? 'A total magnitude budget: a diamond.' : p === 2 ? 'Ordinary Euclidean length: a disk.' : valid ? 'As p increases, the unit ball expands toward the square.' : 'The sides bow inward. The set is not convex in two or more dimensions.';
    const midpoint = NormMath.measure([0.5, 0.5], p), inside = midpoint <= 1 + 1e-12;
    $('midpoint').textContent = `Size of m = ${fmt(midpoint)} → ${inside ? 'inside or on the boundary' : 'outside'}.`;
    $('chord').textContent = zero ? 'The endpoints each have one nonzero; the midpoint has two.' : valid ? 'The entire orange segment lies in the ball.' : 'The endpoints are in the set, but their midpoint is outside.';
    $('example').textContent = `Size of v = ${fmt(NormMath.measure([3,-4,0],p))}`;
    let s = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#6cdeca"/></marker></defs>';
    for (const v of [-1,0,1]) {
      s += `<line x1="${X(v)}" y1="35" x2="${X(v)}" y2="445" stroke="#334558"/><line x1="35" y1="${Y(v)}" x2="445" y2="${Y(v)}" stroke="#334558"/>`;
      if (v) s += `<text x="${X(v)}" y="${Y(0)+24}" text-anchor="middle">${v}</text><text x="${X(0)-14}" y="${Y(v)+6}" text-anchor="end">${v}</text>`;
    }
    if(zero) s += '<path d="M 28 240 H 452" fill="none" stroke="#6cdeca" stroke-width="5" marker-start="url(#arrow)" marker-end="url(#arrow)"/><path d="M 240 28 V 452" fill="none" stroke="#6cdeca" stroke-width="5" marker-start="url(#arrow)" marker-end="url(#arrow)"/><circle cx="240" cy="240" r="5" fill="#6cdeca"/>';
    else {
      const d=NormMath.boundary(p).map(([x,y],i)=>`${i?'L':'M'} ${X(x).toFixed(3)} ${Y(y).toFixed(3)}`).join(' ')+' Z';
      s += `<path d="${d}" fill="#60d5bf" fill-opacity=".2" stroke="#6cdeca" stroke-width="3"/>`;
    }
    s += `<line x1="${X(1)}" y1="${Y(0)}" x2="${X(0)}" y2="${Y(1)}" stroke="#ffbd79" stroke-width="2.5" stroke-dasharray="7 5"/>`;
    for(const [x,y] of [[1,0],[0,1]]) s += `<circle cx="${X(x)}" cy="${Y(y)}" r="5" fill="#ffbd79"/>`;
    s += `<circle cx="${X(.5)}" cy="${Y(.5)}" r="6" fill="#ffbd79" stroke="#111923" stroke-width="2"/><text x="${X(.5)+12}" y="${Y(.5)-12}">m</text><text x="447" y="270">x₁</text><text x="260" y="31">x₂</text><text x="257" y="270">0</text>`;
    $('plot').innerHTML=s;
    $('plot').setAttribute('aria-label',`${$('measure-name').textContent}. ${$('midpoint').textContent}`);
  }
  document.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>render(Number(b.dataset.p))));
  $('p').addEventListener('input',e=>render(Number(e.target.value)));
  render(2);
})();
