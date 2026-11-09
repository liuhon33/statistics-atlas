---
id: tower
title: Tower property
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → Tower property
created: '2026-11-08'
updated: '2026-11-08'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Conditional expectation (L4)]]'
applied_in:
- '[[Backbone/Statistical inference & modeling/Bayesian inference/Hierarchical Bayesian modeling/Hierarchies & pooling/Hierarchies & pooling]]'
related:
- '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation]]'
sources:
- '[[_system/Sources/prob]]'
---

# Tower property

Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → Tower property

Parent: [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Conditional expectation (L4)|Conditional expectation]]

## Statement and intuition

**Averaging in stages gives the same result as averaging directly, provided the stages use nested information and the correct probability weights.**

Let $X$ be a real random variable with $\mathbb E|X|<\infty$, and let $\mathcal G\subseteq\mathcal H$ be sigma-algebras representing less and more information. The **tower property** is

$$
\boxed{\mathbb E[\mathbb E[X\mid\mathcal H]\mid\mathcal G]
=\mathbb E[X\mid\mathcal G]}
\qquad\text{almost surely}.
$$

The inner expectation is itself a random variable: the mean associated with the observed group. The outer expectation averages those group means, weighted by their conditional probabilities. No independence is required. Without nested information, one cannot generally simplify $\mathbb E[\mathbb E[X\mid Y]\mid Z]$ to $\mathbb E[X\mid Z]$.

![[assets/figures/tower-property/tower-property.png]]

*Original illustration (Codex); reproducible with [[assets/figures/tower-property/draw.ps1|the drawing script]]. Classes are nested within grades. Grade A's mean is $(2/6)3+(4/6)9=7$, not the unweighted class average $6$.*

## Relationship to the law of total expectation

**The nested-information tower property generalizes the law of total expectation.** The names are also sometimes used interchangeably (Rougier, §1.3.3, equation (1.19), cited below).

The **law of total expectation** averages subgroup means to obtain the overall mean; no conditioning remains:

$$
\boxed{\mathbb E[\mathbb E[X\mid Y]]=\mathbb E[X].}
$$

$$
\begin{aligned}
\mathbb E[\mathbb E[X\mid Y]]
&=\int\left(\int x\,f_{X\mid Y}(x\mid y)\,dx\right)f_Y(y)\,dy\\
&=\iint x\,f_{X,Y}(x,y)\,dx\,dy\\
&=\int x\left(\int f_{X,Y}(x,y)\,dy\right)dx\\
&=\int x\,f_X(x)\,dx=\mathbb E[X].
\end{aligned}
$$

With densities assumed (sums replace integrals in the discrete case), the second line uses $f_{X\mid Y}(x\mid y)\,f_Y(y)=f_{X,Y}(x,y)$. The third integrates $y$ first. Fubini's theorem allows this order swap because $\iint|x|\,f_{X,Y}(x,y)\,dx\,dy=\mathbb E|X|<\infty$. Since $x$ does not depend on $y$, it comes out of the $y$-integral, and integrating out $y$ leaves the marginal $f_X$.

The **general tower property** averages finer subgroup means while retaining the information in $Y$:

$$
\boxed{\mathbb E[\mathbb E[X\mid Y,Z]\mid Y]=\mathbb E[X\mid Y].}
$$

$$
\begin{aligned}
\mathbb E[\mathbb E[X\mid Y,Z]\mid Y=y]
&=\int\left(\int x\,f_{X\mid Y,Z}(x\mid y,z)\,dx\right)f_{Z\mid Y}(z\mid y)\,dz\\
&=\iint x\,f_{X,Z\mid Y}(x,z\mid y)\,dx\,dz\\
&=\int x\left(\int f_{X,Z\mid Y}(x,z\mid y)\,dz\right)dx\\
&=\int x\,f_{X\mid Y}(x\mid y)\,dx=\mathbb E[X\mid Y=y].
\end{aligned}
$$

The steps are the same, carried out inside the fixed grade $Y=y$. The second line uses $f_{X\mid Y,Z}(x\mid y,z)\,f_{Z\mid Y}(z\mid y)=f_{X,Z\mid Y}(x,z\mid y)$. The third integrates $z$ first. Fubini's theorem allows this because $\iint|x|\,f_{X,Z\mid Y}(x,z\mid y)\,dx\,dz=\mathbb E[|X|\mid Y=y]$, which is finite for almost every $y$ when $\mathbb E|X|<\infty$. This is why the identity holds almost surely. Integrating out $z$ leaves the conditional marginal $f_{X\mid Y}$, and $y$ is never integrated out.

In the diagram, take $Y$ to be the grade and $Z$ the class:

- **Total expectation:** class means → whole-school mean.
- **General tower property:** class means → grade means, keeping the grade known.

Intuitively, the second is **the law of total expectation applied separately within each grade**. Formally, the first is the special case of the sigma-algebra statement where the outer information is trivial, $\mathcal G=\{\varnothing,\Omega\}$, with $\Omega$ the sample space: no information is retained.

## Short proof

Set $U=\mathbb E[X\mid\mathcal H]$ and $V=\mathbb E[U\mid\mathcal G]$. Then $V$ is integrable and $\mathcal G$-measurable. For every event $A\in\mathcal G\subseteq\mathcal H$, the defining integral property gives

$$
\mathbb E[V\mathbf 1_A]
=\mathbb E[U\mathbf 1_A]
=\mathbb E[X\mathbf 1_A],
$$

where $\mathbf 1_A$ is the indicator of $A$. Thus $V$ satisfies the definition of $\mathbb E[X\mid\mathcal G]$; uniqueness up to probability-zero events proves the identity.

## Two short applications

1. **Expected workload.** Let $N\sim\operatorname{Poisson}(\lambda)$ be the number of jobs. Each job takes an independent time $T_i$, with mean $m$, and the times are independent of $N$. For total time $S=\sum_{i=1}^{N}T_i$,
   $$
   \mathbb E[S\mid N]=Nm
   \quad\Longrightarrow\quad
   \mathbb E[S]=\mathbb E[Nm]=\lambda m.
   $$
   Conditioning avoids deriving the distribution of the random sum.

2. **Bayesian prediction.** Given observed data $D$ and an uncertain parameter $\theta$, average the parameter-specific prediction over its posterior:
   $$
   \mathbb E[Y_{\mathrm{new}}\mid D]
   =\mathbb E_{\theta\mid D}
   [\mathbb E[Y_{\mathrm{new}}\mid\theta,D]].
   $$
   For a Bernoulli outcome with success probability $\theta$ and posterior $\theta\mid D\sim\operatorname{Beta}(a,b)$, $a,b>0$, this is $a/(a+b)$.

**Sources.** Nicholas Georgiou and Hugo Lo, *APTS Applied Stochastic Processes* (2024; notes originally by Wilfrid Kendall), [§§2.7–2.8: conditional expectation and tower property](https://maths.dur.ac.uk/users/nicholas.georgiou/ASP24/prelim/_book/expectation-and-probability.html#conditional-expectation-i-property-based-definition); Jonathan Rougier, *APTS Notes on Statistical Inference* (2015), [§1.3.3, p. 15, equation (1.19) and its nested extension](https://warwick.ac.uk/fac/sci/statistics/apts/students/resources-1516/apts_si_prelim.pdf#page=15). Proof restated from the defining property; diagram and applications are explanatory additions.

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation|Law of total expectation]] — The law of total expectation is the special case of the nested tower property in which no outer conditioning information is retained.
- [[Backbone/Statistical inference & modeling/Bayesian inference/Hierarchical Bayesian modeling/Hierarchies & pooling/Hierarchies & pooling|Hierarchies & pooling]] — Hierarchical predictions average over latent parameters and groups.

```atlas
```
