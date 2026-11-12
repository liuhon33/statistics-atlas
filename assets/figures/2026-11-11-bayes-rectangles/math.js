/* Pure probability functions shared by the offline explorers and numeric checks. */
const BayesMath = (() => {
  function update(prior, likelihood) {
    const area = prior.map((p, i) => p * likelihood[i]);
    const evidence = area.reduce((s, x) => s + x, 0);
    return {area, evidence, posterior: evidence > 0 ? area.map(x => x / evidence) : null};
  }
  function steve(p = 1 / 21, a = .4, b = .1) { return update([p, 1-p], [a, b]); }
  function elbo(r) {
    const joint = [2/105, 2/21], prior = [1/21, 20/21], likelihood = [.4, .1];
    const q = [r, 1-r], evidence = joint[0] + joint[1];
    const sumLog = target => q.reduce((s, x, i) => s + (x === 0 ? 0 : x * Math.log(x / target[i])), 0);
    const fit = q.reduce((s, x, i) => s + x * Math.log(likelihood[i]), 0);
    const priorKL = sumLog(prior), gap = sumLog([1/6, 5/6]);
    return {q, evidence, logEvidence: Math.log(evidence), fit, priorKL, gap, bound: fit - priorKL};
  }
  function monty(t = .5, blind = false) {
    return update([1/3, 1/3, 1/3], blind ? [.5, .5, 0] : [t, 1, 0]);
  }
  return {update, steve, elbo, monty};
})();
if (typeof module !== 'undefined') module.exports = BayesMath;
