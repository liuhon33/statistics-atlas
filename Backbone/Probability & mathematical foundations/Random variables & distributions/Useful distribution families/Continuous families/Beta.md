---
id: continuous-beta
title: Beta
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Beta
created: '2026-11-08'
updated: '2026-11-11'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Continuous families]]'
sources:
- '[[_system/Sources/prob]]'
---

# Beta

Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Beta

Parent: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Continuous families|Continuous families]]

## 1. See it first — uncertainty about a probability

Imagine a coin whose chance of heads, $p$, is unknown. A **Beta distribution** describes uncertainty about that number between 0 and 1—not whether the next flip itself is heads or tails.

Start with **$\operatorname{Beta}(1,1)$**: a flat density of height 1. The intervals $0.2<p<0.3$ and $0.7<p<0.8$ each have probability $0.1$. Flat does **not** mean the coin is known to be fair; it means equal-width ranges of possible $p$ receive equal weight.

Two positive shape parameters, $\alpha$ and $\beta$, reshape the curve. Equal values give symmetry; larger equal values concentrate it around $0.5$. Increasing $\alpha$ alone shifts the mean right; increasing $\beta$ shifts it left.

A standard use is a **Bayesian prior** for an unknown success probability. Start with $\operatorname{Beta}(1,1)$; after 3 heads and 1 tail, the updated distribution is $\operatorname{Beta}(4,2)$. Its mean is $4/6$, also the predicted chance of the next head. We retain uncertainty instead of declaring $p=3/4$ exactly. [Stanford CS109, lecture 21, pp. 18–27](https://web.stanford.edu/class/archive/cs/cs109/cs109.1244/lectures/21_beta.pdf).

```atlas-interactive
path: assets/figures/2026-11-11-beta/shapes.html
title: Beta shapes — move alpha and beta
height: 850
```

**Try:** compare $(2,2)$ and $(10,10)$, then move just one slider. The horizontal axis is $p$; the vertical axis is **density**, not point probability. The U-shaped preset puts more weight near the extremes, not at exactly 0 or 1.

[[assets/figures/2026-11-11-beta/shapes.html|Open the standalone shape explorer]]

> [!example]- Static view — the simplest shape and two variations
> ![[assets/figures/2026-11-11-beta/shapes.svg]]
> Original analytic curves. A flat density is broad uncertainty; the central peak favours probabilities near one half; the right-shifted curve favours larger probabilities.

## 2. How it works — derive the family and prove conjugacy

### Start with the coin, not a memorized density

Assume $X_1,\ldots,X_n\mid p$ are **conditionally independent Bernoulli$(p)$** observations, with the same fixed $p$ for all trials. Write $s=\sum_i X_i$ for successes and $f=n-s$ for failures. Their likelihood is

$$
L(p)=\prod_{i=1}^n p^{X_i}(1-p)^{1-X_i}=p^s(1-p)^f.
$$

If only the count $s$ is recorded, its binomial likelihood includes $\binom ns$. This factor is constant **with respect to $p$**, so it cancels from the posterior. Conditional independence is essential to this product; an unknown $p$ shared across observations does not make their prior-predictive joint law independent. [Duke Math 231, §15.1](https://sites.math.duke.edu/~jonm/Math231/estimation.html#likelihoods-and-prior-and-posterior-distributions).

With a uniform prior and our $s=3,f=1$ example, Bayes' rule gives

$$
\pi(p\mid x)\propto p^3(1-p),\qquad
\int_0^1p^3(1-p)\,dp=\frac14-\frac15=\frac1{20}.
$$

Thus the normalized posterior is $20p^3(1-p)$ on $(0,1)$. **This is where the Beta shape comes from in this model:** powers of $p$ and $1-p$ appear naturally when successes and failures accumulate.

### Generalize the powers and normalize

Use positive real parameters—not necessarily integers—and define

$$
\boxed{\pi(p)=\frac{p^{\alpha-1}(1-p)^{\beta-1}}{B(\alpha,\beta)},\quad 0<p<1,\quad \alpha,\beta>0,}
$$

$$
B(\alpha,\beta)=\int_0^1u^{\alpha-1}(1-u)^{\beta-1}\,du.
$$

The integral is finite: near 0 the relevant power is $u^{\alpha-1}$, integrable when $\alpha>0$; near 1 the analogous condition is $\beta>0$. Dividing by this integral makes total probability exactly 1. This defines $\operatorname{Beta}(\alpha,\beta)$. [NIST/SEMATECH Handbook, §1.3.6.6.17, density and Beta function](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366h.htm).

The $-1$ convention makes $(1,1)$ uniform; $(2,1)$ has density $2p$, and $(1,2)$ has density $2(1-p)$. If a shape is below 1, density can diverge at an endpoint while its integral remains finite. This continuous distribution still assigns zero probability to either exact endpoint.

### Multiply by the likelihood: the proof

Bayes' rule yields

$$
\begin{aligned}
\pi(p\mid x)
&\propto \underbrace{p^s(1-p)^f}_{\text{likelihood}}
\underbrace{p^{\alpha-1}(1-p)^{\beta-1}}_{\text{prior kernel}}\\
&=p^{(\alpha+s)-1}(1-p)^{(\beta+f)-1}.
\end{aligned}
$$

The new exponents are another Beta kernel; normalization gives

$$
\boxed{p\mid x\sim\operatorname{Beta}(\alpha+s,\beta+f).}
$$

**Conjugate** means that prior and posterior belong to the same family. A success adds 1 to $\alpha$; a failure adds 1 to $\beta$. This is a proved algebraic closure property, not a claim that every Bayesian model should use Beta. [The Book of Statistical Proofs, “Conjugate prior distribution for binomial observations”](https://statproofbook.github.io/P/bin-prior.html).

```atlas-interactive
path: assets/figures/2026-11-11-beta/update.html
title: Beta prior to posterior — add successes and failures
height: 900
```

**Try:** hold the prior fixed and compare 3 heads / 1 tail with 30 heads / 10 tails. Then hold the data fixed and choose the stronger middle prior. Notice how both the centre and width matter.

[[assets/figures/2026-11-11-beta/update.html|Open the standalone Bayesian-update explorer]]

> [!example]- Static view — a prior becomes a posterior
> ![[assets/figures/2026-11-11-beta/update.svg]]
> Cyan: the uniform prior. Orange: $\operatorname{Beta}(4,2)$ after 3 successes and 1 failure. Dashed vertical lines mark means; the posterior mean $2/3$ differs from its mode $3/4$.

### Why this is a useful prior—not automatically the right one (all models are wrong but some are useful)

The Beta integral gives moments directly:

$$
E[p]=\frac{B(\alpha+1,\beta)}{B(\alpha,\beta)}=\frac{\alpha}{\alpha+\beta},\qquad
E[p^2]=\frac{\alpha(\alpha+1)}{(\alpha+\beta)(\alpha+\beta+1)}.
$$

For the first equality's simplification, combine
$B(a,b)=B(a+1,b)+B(a,b+1)$ with
$aB(a,b+1)=bB(a+1,b)$, obtained by integrating the derivative of $u^a(1-u)^b$; its boundary terms vanish for $a,b>0$. Apply the same recurrence again for the second moment. Subtracting $E[p]^2$ gives

$$
\operatorname{Var}(p)=\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}
=\frac{m(1-m)}{\kappa+1},\quad m=\frac{\alpha}{\alpha+\beta},\quad\kappa=\alpha+\beta.
$$

So $m$ sets the prior mean and, **at fixed $m$**, increasing $\kappa$ reduces its spread. Conversely choose $\alpha=m\kappa$, $\beta=(1-m)\kappa$. These moments agree with [NIST, “Common Statistics”](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366h.htm).

For $n>0$, the posterior mean is an interpretable compromise:

$$
\boxed{E[p\mid x]=\frac{\alpha+s}{\kappa+n}
=\underbrace{\frac{\kappa}{\kappa+n}}_{\text{prior weight}}m
+\underbrace{\frac{n}{\kappa+n}}_{\text{data weight}}\frac{s}{n}.}
$$

This explains the *pseudo-count* interpretation: $\kappa$ acts as a prior sample size in this mean-weighting formula. It is not a record of actual observations. Starting from a uniform prior, literal past counts would instead produce $\operatorname{Beta}(1+s_0,1+f_0)$, so the baseline matters.

Finally, averaging the next trial's conditional success probability gives

$$
P(X_{n+1}=1\mid x)=\int_0^1 p\,\pi(p\mid x)\,dp
=\frac{\alpha+s}{\alpha+\beta+n}.
$$

For the example, this is $(1+3)/(1+1+4)=2/3$, not the raw fraction $3/4$. Sequential updating needs only the two accumulated parameters; no numerical integration is needed for this prediction. The underlying Beta–Bernoulli update is described in [Duke Math 231, §15.2](https://sites.math.duke.edu/~jonm/Math231/estimation.html#conjugate-priors); the mean-weighting and prediction identities above follow directly from it.

**What “good” means here:** correct support, flexible shapes and tractable updating. Suitability still depends on whether the chosen shape expresses your prior knowledge and whether the constant-$p$, conditionally independent trial model fits. A single Beta cannot represent every belief (for example, two separated interior peaks or a positive point mass at $p=0$). Conjugacy proves convenience, not universal optimality; uniform on $p$ is a choice, not a uniquely information-free prior.

## 3. Deeper understanding and connections

## Origin

> [!info]- Source details
> Requested progressive enrichment of the existing Beta backbone page: introduction and mechanics developed; third level intentionally empty. The coin examples, slider explorers, static diagrams and expanded algebra are original explanatory constructions, not transcribed user work.
>
> Definitions and moments: NIST/SEMATECH Handbook §1.3.6.6.17. Introductory shapes: Stanford CS109 lecture 21, pp. 18–27. Bernoulli likelihood and conjugacy: Duke Math 231 §§15.1–15.2 and the linked Statistical Proofs entry. Sources read on 2026-11-11.
>
> Reproducible source and independent numerical checks: [[assets/figures/2026-11-11-beta/build.py|build and checks]], [[assets/figures/2026-11-11-beta/math.js|pure formulas]], [[assets/figures/2026-11-11-beta/checks.json|check results]]. Curves use fixed vertical limits with disclosed clipping; no random samples or external assets are used.

```atlas
```
