/* Exact full-covariance, two-component EM. No covariance regularizer is added. */
const EMToy = (() => {
  const seed = 20261113;
  function random(seedValue) {
    let s = seedValue >>> 0;
    return () => { s = (1664525 * s + 1013904223) >>> 0; return (s + 0.5) / 4294967296; };
  }
  function data() {
    const u = random(seed);
    const normal = () => Math.sqrt(-2 * Math.log(u())) * Math.cos(2 * Math.PI * u());
    return Array.from({length: 240}, () => {
      const k = u() < 0.42 ? 0 : 1, a = normal(), b = normal();
      // Cholesky factors of [[.16,.04],[.04,.24]] and [[.28,.12],[.12,.22]].
      if (k === 0) return [-1.4 + 0.4 * a, -1.1 + 0.1 * a + Math.sqrt(0.23) * b];
      return [1.2 + Math.sqrt(0.28) * a, 0.9 + 0.12 / Math.sqrt(0.28) * a + Math.sqrt(0.22 - 0.12 ** 2 / 0.28) * b];
    });
  }
  const presets = {
    crossed: {label: 'Crossed centers — like slide 13', means: [[-1.4, 1.1], [1.5, -1.0]]},
    close: {label: 'Centers near the two clouds', means: [[-1.6, -1.0], [1.3, 0.8]]},
    left: {label: 'Both centers start on the left', means: [[-2.1, -1.8], [-0.9, -0.2]]},
    identical: {label: 'Identical centers — symmetry trap', means: [[0, 0], [0, 0]]}
  };
  const clone = x => JSON.parse(JSON.stringify(x));
  function initialize(key = 'crossed', weight = 0.5, sd = 0.7, means = null) {
    if (!(weight > 0 && weight < 1 && sd > 0)) throw Error('Use positive spread and weights strictly between 0 and 1.');
    const mus = means || presets[key].means;
    if (!mus.flat().every(Number.isFinite)) throw Error('Enter finite starting coordinates.');
    return {weights: [weight, 1 - weight], means: clone(mus), covs: [[[sd * sd, 0], [0, sd * sd]], [[sd * sd, 0], [0, sd * sd]]]};
  }
  function logGaussian(x, mean, c) {
    const a = c[0][0], b = c[0][1], d = c[1][1], det = a * d - b * b;
    if (!(a > 0 && det > 0)) throw Error('A covariance is not positive definite. Reset to a different initialization.');
    const dx = x[0] - mean[0], dy = x[1] - mean[1];
    return -Math.log(2 * Math.PI) - 0.5 * Math.log(det) - 0.5 * (d * dx * dx - 2 * b * dx * dy + a * dy * dy) / det;
  }
  function expectation(xs, p) {
    let logLikelihood = 0;
    const r = xs.map(x => {
      const v = p.weights.map((w, k) => Math.log(w) + logGaussian(x, p.means[k], p.covs[k]));
      const m = Math.max(...v), logDen = m + Math.log(Math.exp(v[0] - m) + Math.exp(v[1] - m));
      logLikelihood += logDen;
      return v.map(z => Math.exp(z - logDen));
    });
    return {r, logLikelihood};
  }
  function maximization(xs, r) {
    const counts = [0, 0], means = [[0, 0], [0, 0]];
    for (let n = 0; n < xs.length; n++) for (let k = 0; k < 2; k++) {
      counts[k] += r[n][k];
      for (let j = 0; j < 2; j++) means[k][j] += r[n][k] * xs[n][j];
    }
    if (counts.some(v => v < 1e-7)) throw Error('A component has almost no effective data. No update applied; reset with less extreme starting values.');
    for (let k = 0; k < 2; k++) for (let j = 0; j < 2; j++) means[k][j] /= counts[k];
    const covs = [[[0, 0], [0, 0]], [[0, 0], [0, 0]]];
    for (let n = 0; n < xs.length; n++) for (let k = 0; k < 2; k++) {
      const d = xs[n].map((v, j) => v - means[k][j]);
      for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) covs[k][i][j] += r[n][k] * d[i] * d[j] / counts[k];
    }
    for (const c of covs) {
      const eigenMin = (c[0][0] + c[1][1] - Math.hypot(c[0][0] - c[1][1], 2 * c[0][1])) / 2;
      if (!(eigenMin > 1e-7)) throw Error('A covariance is nearly singular. No update applied; reset. This is a known GMM likelihood pathology.');
    }
    return {weights: counts.map(n => n / xs.length), means, covs};
  }
  function qValue(xs, r, p) {
    let q = 0;
    for (let n = 0; n < xs.length; n++) for (let k = 0; k < 2; k++) {
      if (r[n][k] > 0) q += r[n][k] * (Math.log(p.weights[k]) + logGaussian(xs[n], p.means[k], p.covs[k]));
    }
    return q;
  }
  function entropy(r) { return -r.flat().reduce((s, p) => s + (p > 0 ? p * Math.log(p) : 0), 0); }
  function ellipse(mean, c, radius = 1, count = 100) {
    const a = Math.sqrt(c[0][0]), b = c[1][0] / a, d = Math.sqrt(c[1][1] - b * b);
    return Array.from({length: count + 1}, (_, i) => {
      const t = 2 * Math.PI * i / count;
      return [mean[0] + radius * a * Math.cos(t), mean[1] + radius * (b * Math.cos(t) + d * Math.sin(t))];
    });
  }
  return {seed, data, presets, clone, initialize, logGaussian, expectation, maximization, qValue, entropy, ellipse};
})();
if (typeof module !== 'undefined' && module.exports) module.exports = EMToy;
