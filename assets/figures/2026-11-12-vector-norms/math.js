/* Finite real vectors. p=0 means support count; Infinity means max norm. */
const NormMath = (() => {
  function measure(v, p) {
    if (p === 0) return v.filter(x => x !== 0).length;
    const a = v.map(Math.abs), m = Math.max(...a);
    if (p === Infinity || m === 0) return m;
    if (!(p > 0)) throw new RangeError('Use p > 0, infinity, or support count.');
    return m * Math.pow(a.reduce((s, x) => s + Math.pow(x / m, p), 0), 1 / p);
  }
  function boundary(p, steps = 960) {
    if (p === 0) return [];
    return Array.from({length: steps + 1}, (_, i) => {
      const t = 2 * Math.PI * i / steps, v = [Math.cos(t), Math.sin(t)];
      const r = 1 / measure(v, p);
      return v.map(x => x * r);
    });
  }
  return {measure, boundary};
})();
if (typeof module !== 'undefined') module.exports = NormMath;
