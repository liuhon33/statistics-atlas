---
id: elbo
title: ELBO
layer: backbone
level: 5
subject: computing
study_band: M
backbone_path: Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO
created: '2026-11-08'
updated: '2026-11-11'
aliases:
- Calculate the ELBO
tags:
- atlas/backbone
- subject/computing
- level/5
- study/masters
node_kind: knowledge point
parent: '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Variational inference]]'
applied_in:
- '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Selected architectures & latent models]]'
sources:
- '[[_system/Sources/bda]]'
- '[[_system/Sources/vi]]'
- '[[_system/Sources/vi-course]]'
---

# ELBO

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO

Parent: [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Variational inference|Variational inference]]

## Level 1 — See it and use it

**The ground is wet. Was the hidden cause rain or a sprinkler?** A model gives each cause an initial probability and says how likely wet ground is under each. We want the probabilities of the causes *after* seeing the ground. These form the **posterior**.

With many hidden causes, calculating that posterior can be difficult. Instead, choose a manageable distribution $q$ over the causes and improve it using one score: the **evidence lower bound (ELBO)**. The evidence is the model's probability of the observation; the ELBO never exceeds its logarithm. [Blei et al., §2.2](https://arxiv.org/html/1601.00670v9#S2.SS2).

![[assets/figures/2026-11-11-elbo-levels/bound-and-posterior.svg]]

*An exactly solvable teaching example: the model's posterior is 80% rain, 20% sprinkler. Natural-log scores are in nats.*

| Candidate $q$: rain / sprinkler | ELBO |
| --- | ---: |
| 50% / 50% | −0.916 |
| 70% / 30% | −0.721 |
| 80% / 20% | −0.693 |

**Use it:** prefer 70/30 to 50/50 because −0.721 is higher. Here 80/20 reaches the log evidence, −0.693. With the model fixed, raising the ELBO reduces posterior-approximation error—not necessarily error in the model itself.

## Level 2 — How it works

### Define the score without computing the posterior

Fix the observation $x$ and model parameters $\theta$. Write $q(z)=q_\phi(z\mid x)$ for a normalized approximate posterior over hidden variables $z$; $\phi$ controls the approximation. The [[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Prior and posterior|prior and likelihood]] specify

$$
p_\theta(x,z)=p_\theta(x\mid z)p_\theta(z),\qquad
p_\theta(x)=\int p_\theta(x,z)\,dz.
$$

Use sums for discrete $z$. For continuous observations, evidence is a **density**, not the probability of one exact value. Suppress $\theta$ below, but keep it fixed unless stated otherwise.

Assume $0<p(x)<\infty$, $q$ puts mass only where the posterior is positive, and the displayed log terms are absolutely integrable under $q$. These sufficient conditions keep the following identities finite.

$$
\boxed{\mathcal L(q)=\int q(z)\left[\log p(x,z)-\log q(z)\right]dz
=\mathbb E_q\left[\log\frac{p(x,z)}{q(z)}\right].}
$$

The integrand needs the **joint**, not the normalized posterior. Its expectation may still require Monte Carlo; removing the evidence calculation does not guarantee a closed-form ELBO. [Kingma & Welling, §2.2–2.3, equations (2), (5)–(7)](https://arxiv.org/html/1312.6114v11#S2.SS2).

### Why this is a lower bound: one short derivation

[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]] averages a log density ratio under its **first** argument. Substitute Bayes' rule $p(z\mid x)=p(x,z)/p(x)$:

$$
\begin{aligned}
D_{\mathrm{KL}}(q\|p(\cdot\mid x))
&=\int q(z)\log\frac{q(z)p(x)}{p(x,z)}\,dz\\
&=\log p(x)-\mathcal L(q).
\end{aligned}
$$

Since KL is nonnegative,

$$
\boxed{\log p(x)=\mathcal L(q)+D_{\mathrm{KL}}(q\|p(\cdot\mid x))
\ \geq\ \mathcal L(q).}
$$

The [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Posterior KL gap|posterior KL gap]] vanishes exactly when $q=p(\cdot\mid x)$ almost everywhere. At fixed model, maximizing ELBO therefore minimizes this KL. A restricted family of $q$ may not contain the exact posterior. [Blei et al., §2.2, equations (12)–(14)](https://arxiv.org/html/1601.00670v9#S2.SS2).

### The same score as fit minus a prior penalty

Factor $p(x,z)=p(x\mid z)p(z)$ inside the defining integral:

$$
\boxed{\mathcal L(q)
=\underbrace{\mathbb E_q[\log p(x\mid z)]}_{\text{expected data fit}}
-\underbrace{D_{\mathrm{KL}}(q\|p(z))}_{\text{departure from the prior}}.}
$$

This is an equivalent computational form—not a different objective. The prior KL is **not** the posterior-approximation gap. [Kingma & Welling, §2.2, equation (3)](https://arxiv.org/html/1312.6114v11#S2.SS2).

For our wet-ground example, take mutually exclusive causes with

$$
p(R)=p(S)=0.5,\qquad p(w\mid R)=0.8,\quad p(w\mid S)=0.2.
$$

Then $p(w,R)=0.4$, $p(w,S)=0.1$, $p(w)=0.5$, and Bayes gives $p(R\mid w)=0.8$. Let $r=q(R\mid w)$:

$$
\mathcal L(r)
=\underbrace{r\log 0.8+(1-r)\log 0.2}_{\text{fit}}
-\underbrace{\left[r\log\frac r{0.5}+(1-r)\log\frac{1-r}{0.5}\right]}_{\text{prior KL}}.
$$

![[assets/figures/2026-11-11-elbo-levels/fit-versus-prior.svg]]

*Original exact calculation. Data fit alone favors rain with certainty; the prior penalty alone favors 50/50. Their sum is maximized at the posterior, 80/20.*

At $r=0.8$, fit is $-0.5004$ and prior KL is $0.1927$, giving ELBO $-0.6931$. **The posterior KL is zero while the prior KL is positive.** Evidence from the wet ground justifies moving away from the prior.

## Level 3 — Connections to keep in mind

### Jensen and importance sampling are the same route viewed two ways

**The crucial distinction is “average the log” versus “log the average.”** If $q$ also covers all positive posterior mass, the [[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Efficient integration/Importance sampling|importance weight]] $W(z)=p(x,z)/q(z)$ satisfies

$$
\mathbb E_q W=p(x),\qquad
\underbrace{\mathbb E_q\log W}_{\mathcal L(q)}
\leq \underbrace{\log\mathbb E_q W}_{\log p(x)}.
$$

The inequality is [[Backbone/Probability & mathematical foundations/Mathematical tools/Convexity & inequalities/Convex functions & bounds/Jensen inequality|Jensen's inequality]] for concave log; the derivation above identifies its gap as posterior KL. The coverage assumption is stronger than the one needed for that KL identity: a proposal missing posterior mass cannot recover the entire evidence by reweighting. [Stanford CS228, importance sampling](https://ermongroup.github.io/cs228-notes/inference/sampling/#importance-sampling).

For $q=(0.5,0.5)$ in our example, the weights are $(0.8,0.2)$:

$$
\mathbb E_q\log W=\tfrac12\log0.8+\tfrac12\log0.2=-0.9163,
\qquad \log\mathbb E_qW=\log0.5=-0.6931.
$$

At the exact posterior, both weights equal $0.5$: there is no averaging-versus-log gap. A **sample estimate** is different from the expectation: one draw can give $\log0.8>-0.6931$, so an estimated ELBO need not lie below log evidence on every draw.

### A VAE code and a diffusion path can occupy the same slot

**ELBO does not require $z$ to be a single code.** In a [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Variational autoencoders|VAE]], $q_\phi(z\mid x)$ is a learned encoder. In standard fixed-schedule DDPM, use observation $x_0$ and hidden tuple $z=(x_1,\ldots,x_T)$; $q(z\mid x_0)$ is the prescribed noising process. The same expected log-joint/log-proposal ratio gives the bound. [AEVB, §2](https://arxiv.org/html/1312.6114v11#S2); [DDPM, §2, equations (1)–(3)](https://arxiv.org/html/2006.11239v2#S2).

![[assets/figures/2026-11-11-vae-diffusion/binary-paths.svg]]

*Reused unchanged from the existing VAE/diffusion study material: a binary, two-step analogy, not Gaussian diffusion. $A=0$ and $B=1$ are one-pixel images. Here “forward joint $q$” means the data distribution times the chosen noising process; it is not just the conditional proposal used earlier.*

Both tables assign image $A$ probability $0.8$, but their conditional path distributions differ. Direct calculation gives a posterior-path KL of $0.1467$ nats for $A$: correct image probabilities can coexist with a loose ELBO.

**Conversely, zero gap does not certify a correct model.** A model predicting a fair coin can have an exactly computed posterior even if reality produces heads 90% of the time. Improving $q$ fixes inference within the assumed model, not its assumptions. If model parameters $\theta$ also change, both the evidence and posterior target move: a higher ELBO alone no longer proves that the inference gap shrank.

## Origin

> [!info]- Source details
> Three-level reference enrichment, 2026-11-11. The distinctions and connections build on the user's existing ELBO, model-versus-inference, and VAE/diffusion learning material. Their personal derivations and handwriting remain in the learning layer, accessible through the live attached-notes navigation; no originals were changed.
>
> Standard identities were checked against the primary references cited inline. The mutually exclusive rain/sprinkler model, its two figures, and numerical comparisons are assistant-added teaching examples, not user work. Reproducible code and checks: [[assets/figures/2026-11-11-elbo-levels/draw_and_check.py]] and [[assets/figures/2026-11-11-elbo-levels/checks.json]]. The reused path figure and its original generator remain unchanged. Detailed learning-note provenance is recorded in the enrichment Log entry.

## Connections

- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Selected architectures & latent models|Selected architectures & latent models]] — Variational autoencoders train a latent-variable model with an ELBO objective.

```atlas
```
