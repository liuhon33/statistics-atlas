---
id: likelihood-mle-invariance
title: MLE invariance
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → MLE invariance
created: '2026-11-08'
updated: '2026-11-11'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Likelihood methods]]'
sources:
- '[[_system/Sources/estimate]]'
- '[[_system/Sources/theory]]'
- '[[_system/Sources/asym]]'
---

# MLE invariance

Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → MLE invariance

Parent: [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Likelihood methods|Likelihood methods]]

## 1. See it and use it — estimate first, transform second

Suppose a normal-model fit to measurements gives a **maximum-likelihood estimate (MLE)** of variance of $4\,\mathrm{cm}^2$. You want standard deviation: spread measured in centimetres, not squared centimetres. Take the square root:

$$
\hat\sigma=\sqrt{\widehat{\sigma^2}}
=\sqrt{4\,\mathrm{cm}^2}=2\,\mathrm{cm}.
$$

![[assets/figures/2026-11-11-mle-invariance/mle-invariance.svg]]

*The peak represents the same fitted model on two parameter scales.*

An MLE is a parameter value that makes the observed data's **likelihood** largest. **MLE invariance** says: if $\hat\theta$ is an MLE of a parameter $\theta$, then applying a specified function $g$ gives an MLE of the target $\eta=g(\theta)$:

$$
\boxed{\hat\eta=g(\hat\theta).}
$$

The input is an existing MLE and the transformation you want; the output is the transformed parameter's MLE. The MLE must exist, and $g$ must be defined on the parameter space. This is an exact rule, not a large-sample approximation. [UC Berkeley STAT 135, Theorem 1 and standard-deviation example.](https://stat135.berkeley.edu/fall-2026/Modules/11-DeltaMethod.html#estimating-a-function-of-parameter-with-mle)

**Use it to avoid fitting again.** Keep the observations and model fixed; transform the estimate, not the observations. “Invariant” means the maximizing fit is preserved, not that its reported numerical value stays unchanged.

## Origin

> [!info]- Source details
> The cited Berkeley section's theorem, standard-deviation example and one-to-one proof were read on 2026-11-11. The numerical example and diagram are original explanatory additions.
>
> Figure construction: independent normal measurements $8$ and $12$ cm, known mean $10$ cm and unknown variance $v>0$. The two plots show the same likelihood using $v$ and $\sigma=\sqrt v$, divided by its common maximum. These are not probability densities over the parameter.
>
> Reproducible source: [[assets/figures/2026-11-11-mle-invariance/draw_mle_invariance.py]]. Numerical checks: [[assets/figures/2026-11-11-mle-invariance/checks.json]]. Static PNG alternative: [[assets/figures/2026-11-11-mle-invariance/mle-invariance.png]].

```atlas
```
