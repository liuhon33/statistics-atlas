---
id: continuous-cauchy-distribution
title: Cauchy distribution
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Cauchy distribution
created: '2026-11-09'
updated: '2026-11-09'
status: active
tags: [atlas/backbone, subject/probability, level/5, study/undergraduate]
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Continuous families]]'
related:
  - '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F]]'
---

# Cauchy distribution

Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Cauchy distribution

Parent: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Continuous families|Continuous families]]

## Definition and scope

For location $a\in\mathbb R$ and scale $b>0$, $X\sim\operatorname{Cauchy}(a,b)$ has density

$$
f_X(x)=\frac{1}{\pi b\{1+[(x-a)/b]^2\}},\qquad x\in\mathbb R.
$$

The standard case has $a=0$, $b=1$, and CDF $F(x)=\tfrac12+\pi^{-1}\arctan x$. Its mean and variance do not exist as finite moments; symmetry does not make its expectation zero. The location is its median and mode, not its mean. Scale is not a standard deviation.

The standard Cauchy is Student's $t$ distribution with one degree of freedom. Substituting $\nu=1$ into the $t$ density gives $1/[\pi(1+x^2)]$. This connects a familiar heavy-tailed family to the smallest residual dimension in Gaussian sampling.

Sources: NIST/SEMATECH, *e-Handbook of Statistical Methods*, [§1.3.6.6.3, Cauchy Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3663.htm) (density, CDF and moments), and [§1.3.6.6.4, t Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm) ($t_1$ identity).

## Connections

- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F|Student t, chi-square and F]] — The standard Cauchy is exactly the one-degree-of-freedom Student t distribution.

```atlas
```
