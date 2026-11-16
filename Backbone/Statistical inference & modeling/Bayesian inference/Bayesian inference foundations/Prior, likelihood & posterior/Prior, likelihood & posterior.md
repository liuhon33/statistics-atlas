---
id: posterior
title: Prior, likelihood & posterior
layer: backbone
level: 4
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Bayesian inference → Bayesian inference foundations → Prior, likelihood & posterior
created: '2026-11-08'
updated: '2026-11-15'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/4
- study/undergraduate-masters
node_kind: group
parent: '[[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Bayesian inference foundations]]'
prerequisite_for:
- '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Markov chain Monte Carlo/Markov chain Monte Carlo]]'
- '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Approximate & latent-variable inference]]'
sources:
- '[[_system/Sources/bda]]'
- '[[assets/figures/2026-11-15-prior-likelihood-posterior/draw_update.py]]'
- '[[assets/figures/2026-11-15-prior-likelihood-posterior/checks.json]]'
- '[[assets/figures/2026-11-15-mle-map/draw_mle_map.py]]'
- '[[assets/figures/2026-11-15-mle-map/checks.json]]'
---

# Prior, likelihood & posterior

Statistical inference & modeling → Bayesian inference → Bayesian inference foundations → Prior, likelihood & posterior

Parent: [[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Bayesian inference foundations|Bayesian inference foundations]]

## 1. See it and use it — before, evidence, after

Suppose a person tests positive for a rare disease. Before this test, **1%** of the relevant population has it. The test is positive for **99%** of people with disease and **1%** without it. Let $D$ mean disease and $+$ the observed result.

![[assets/figures/2026-11-15-prior-likelihood-posterior/prior-likelihood-posterior.svg|1000]]
*Green means disease; red means no disease. The likelihood bars describe separate groups, not posterior shares.*

| Concept | What it describes | Here |
| --- | --- | --- |
| **Prior** $P(D)$ | Uncertainty before this observation | 1% disease |
| **Likelihood** $P(+\mid D)$ | Probability of the fixed observed result under each possibility | 99% with disease; 1% without |
| **Posterior** $P(D\mid +)$ | Updated uncertainty after combining prior and observation | 50% disease |

Likelihood scores the **data under a hypothesis**, not the hypothesis given the data. For continuous observations it uses a density, not an event probability. [Pishro-Nik, §8.2.3, likelihood definition](https://www.probabilitycourse.com/chapter8/8_2_3_max_likelihood_estimation.php).

**Use it:** multiply each prior by its likelihood, then divide by the total weight—[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule|Bayes' rule]]:

$$
P(D\mid +)=\frac{0.01\times0.99}{0.01\times0.99+0.99\times0.01}=50\%.
$$

The posterior raises disease probability from **1% to 50%**, not 99%. Use it as updated uncertainty, not certainty. The prior and test rates must fit the relevant population. [Pishro-Nik, §9.1.0, Bayesian inference](https://www.probabilitycourse.com/chapter9/9_1_0_bayesian_inference.php).

## 2. How it works — likelihood versus posterior: MLE and MAP

Same Bayes update, a new unknown: **a coin's probability of heads**, $\theta\in[0,1]$. Observe the sequence `HHTHHHTHHH`: **8 heads, 2 tails**. Assume tosses are independent with the same head probability, conditional on $\theta$.

Use an illustrative prior favoring near-fair coins: $\pi(\theta)=30\theta^2(1-\theta)^2$, a [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Beta|Beta]]$(3,3)$ density. The factor 30 makes its area 1; it does **not** assert that the coin is exactly fair.

![[assets/figures/2026-11-15-mle-map/mle-map-comparison.svg|1100]]
*Shared horizontal scale, separate vertical scales. Colors now identify functions: blue prior, orange likelihood, green posterior—not disease groups. The prior moves the peak from 0.80 to about 0.714.*

### Keep the data fixed; vary the candidate parameter

Call the observed sequence $x$. Its [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Likelihood function|likelihood]] is

$$
L(\theta;x)=p(x\mid\theta)=\theta^8(1-\theta)^2.
$$

Each head contributes $\theta$, each tail $1-\theta$; independence gives the product. This is the probability of **this exact sequence**, not the probability that $\theta$ is correct. Its integral over $\theta$ is $1/495$, not 1: likelihood is not a parameter distribution.

| Estimate                       | Question                                               | What is maximized over $\theta$?                         |
| ------------------------------ | ------------------------------------------------------ | -------------------------------------------------------- |
| **MLE** — maximum likelihood   | Which parameter makes these observed data most likely? | $L(\theta;x)$                                            |
| **MAP** — maximum a posteriori | Which parameter has the highest posterior **density**? | $p(\theta\mid x)$, equivalently $L(\theta;x)\pi(\theta)$ |

The [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation|MLE]] uses no prior; MAP combines likelihood with a specified prior. [Pishro-Nik, §8.2.3, MLE](https://www.probabilitycourse.com/chapter8/8_2_3_max_likelihood_estimation.php) and [§9.1.2, MAP](https://www.probabilitycourse.com/chapter9/9_1_2_MAP_estimation.php).

### Why multiplying by the prior changes the answer

Bayes' rule for this continuous parameter is

$$
p(\theta\mid x)=\frac{L(\theta;x)\pi(\theta)}{\underbrace{\int_0^1 L(t;x)\pi(t)\,dt}_{Z(x)}}.
$$

$t$ is just an integration variable. **$Z(x)$ does not change as the candidate $\theta$ changes**, so dividing by it cannot move the maximum. Here

$$
\begin{aligned}
L(\theta;x)\pi(\theta)
&=\theta^8(1-\theta)^2\cdot30\theta^2(1-\theta)^2\\
&=30\theta^{8+2}(1-\theta)^{2+2}
=30\theta^{10}(1-\theta)^4,\\
Z(x)&=\frac{2}{1001},\qquad
p(\theta\mid x)=15015\theta^{10}(1-\theta)^4.
\end{aligned}
$$

That normalized posterior is Beta$(11,5)$: the exponents, not the normalizing constant, determine its peak. This is a worked instance of beta–Bernoulli updating. [Cornell CS 4/5780, “The Bayesian Way” and “Maximum a Posteriori Probability Estimation”](https://www.cs.cornell.edu/courses/cs5780/2024sp/lectures/lecturenote04.html).

### Find the two peaks

Logarithms preserve maxima and turn products into sums. For $0<\theta<1$:

$$
\begin{aligned}
\log L(\theta;x)&=8\log\theta+2\log(1-\theta),\\
\frac{d}{d\theta}\log L(\theta;x)&=\frac8\theta-\frac2{1-\theta}=0\\
&\Longrightarrow 8(1-\theta)=2\theta
\Longrightarrow \boxed{\hat\theta_{\mathrm{MLE}}=\frac8{10}=0.80}.
\end{aligned}
$$

For MAP, add the log prior. The constant $C$ below does not depend on $\theta$:

$$
\begin{aligned}
\log p(\theta\mid x)&=C+10\log\theta+4\log(1-\theta),\\
\frac{d}{d\theta}\log p(\theta\mid x)&=\frac{10}\theta-\frac4{1-\theta}=0\\
&\Longrightarrow 10(1-\theta)=4\theta
\Longrightarrow \boxed{\hat\theta_{\mathrm{MAP}}=\frac{10}{14}=\frac57\approx0.714}.
\end{aligned}
$$

Both are unique maxima: the log second derivative is $-a/\theta^2-b/(1-\theta)^2<0$, with $(a,b)=(8,2)$ or $(10,4)$; both original curves vanish at the endpoints.

### Interpret the shift, not just the numbers

$$
\hat\theta_{\mathrm{MAP}}
=\frac{8+2}{10+4}
=\underbrace{\frac{10}{14}}_{\text{data weight}}\underbrace{0.80}_{\text{MLE}}
+\underbrace{\frac4{14}}_{\text{prior weight}}\underbrace{0.50}_{\text{prior mode}}.
$$

In this example the prior pulls the estimate toward 0.50. Its exponents act algebraically like two extra heads and two extra tails **for the MAP calculation**—not actual new observations. A poorly chosen prior can pull the wrong way. With a uniform prior on $[0,1]$, MAP equals MLE on this same $\theta$ scale.

**Do not swap the meanings again:** 0.714 is an estimated head probability, not a 71.4% probability that this estimate is correct. MAP is one point summarizing the posterior; posterior probabilities for a continuous parameter come from **areas over intervals**, not the height of the curve.

## Connections

- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Markov chain Monte Carlo/Markov chain Monte Carlo|Markov chain Monte Carlo]] — Posterior expectations define the quantities that MCMC approximates.
- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Approximate & latent-variable inference|Approximate & latent-variable inference]] — Intractable posterior integrals motivate deterministic approximations.

## Origin

> [!info]- Source details
> Introductory level only, 2026-11-15. The hypothetical disease inputs continue the user's current study example; the definitions, synthesis and focused three-stage visual are assistant-added. Linked textbook sections were read; the existing BDA catalog source is retained without claiming a new book-page check. Exact weights, normalization and bar lengths were checked; the PNG preview was inspected. Live Obsidian rendering was not tested. Existing identity, hierarchy and typed connections are unchanged.
>
> Follow-up level 2, 2026-11-15: the user selected the proposed likelihood-versus-posterior / MLE-versus-MAP connection. The 8-head/2-tail sequence, Beta(3,3) prior, worked arithmetic and three-curve visual are assistant-added examples, not quoted source data or the user's own derivation. Pishro-Nik §§8.2.3 and 9.1.2 and the linked Cornell lecture were read for the definitions and beta updating. Symbolic integrals, score equations, curvature and endpoint checks support the displayed derivation; independent SciPy checks confirm the plotted densities and modes. Reproducible source and checks are in the figure folder. The PNG preview was inspected; live Obsidian rendering was not tested. Level 1, identity, hierarchy and existing typed connections are preserved; the new backbone pointers are inline navigation only.

```atlas
```
