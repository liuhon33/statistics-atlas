const LogisticMath = (() => {
  const sigmoid = z => z >= 0 ? 1 / (1 + Math.exp(-z)) : Math.exp(z) / (1 + Math.exp(z));
  const values = (b0, b1, x) => {
    const eta = b0 + b1 * x, p = sigmoid(eta);
    return {eta, p, odds: Math.exp(eta), slope: b1*p*(1-p)};
  };
  return {sigmoid, values};
})();
if(typeof module !== 'undefined') module.exports = LogisticMath;
