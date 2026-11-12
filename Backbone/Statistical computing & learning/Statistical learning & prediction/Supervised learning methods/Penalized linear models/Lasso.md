---
id: penalized-lasso
title: Lasso
layer: backbone
level: 5
subject: computing
study_band: U–M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Lasso
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/computing
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Penalized linear models]]'
sources:
- '[[_system/Sources/isl]]'
---

# Lasso

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Lasso

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Penalized linear models|Penalized linear models]]

## 1. See it and use it

Suppose a prediction model has many candidate features, but you want a smaller set of useful coefficients. **Lasso adds the sum of the coefficients' absolute sizes to squared prediction error.** It is L1 regularization for linear regression. Its distinctive feature is that some fitted coefficients can become **exactly zero**, removing those features from the fitted formula.

![[assets/figures/2026-11-12-l1-l2-elastic-net/lasso-intro.svg]]

*Constructed example: the smaller coefficient is removed, while the larger one is reduced.*

The penalty is $\lambda_1\sum_j|\beta_j|$, with strength $\lambda_1\ge0$. In this deliberately separable example, the unpenalized coefficients are $(3,0.6)$. At $\lambda_1=1$, lasso subtracts $1$ from each magnitude, stopping at zero, and returns $(2,0)$. Zero means “unused by this fitted model,” not “proved scientifically irrelevant.”

Use lasso when a sparse predictive description is useful. Scale features comparably, normally do not penalize the intercept, and choose the penalty by validation. Strongly correlated features can substitute for one another, making the selected list unstable; [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net|elastic net]] adds a quadratic term to help with that situation. [Friedman, Hastie & Tibshirani (2010), §2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/#S2).

## 2. How it works — a corner, a threshold, and a Laplace prior

For centred $X\in\mathbb R^{n\times p}$ and $y\in\mathbb R^n$, fit slopes $\beta\in\mathbb R^p$ by

$$
\hat\beta=\arg\min_\beta\left\{
\frac12\|y-X\beta\|_2^2+\lambda_1\|\beta\|_1\right\},
\qquad \|\beta\|_1=\sum_j|\beta_j|.
$$

Unlike the squared Euclidean penalty in [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression|ridge]], this is the [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|L1 norm]] itself. Its absolute-value corner is the important difference.

For the opening toy loss, each coordinate minimizes $q(b)=\frac12(b-z)^2+\lambda_1|b|$. Check all three possibilities:

$$
\begin{array}{lll}
b>0:&q'(b)=b-z+\lambda_1=0&\Rightarrow b=z-\lambda_1>0\quad(z>\lambda_1),\\
b<0:&q'(b)=b-z-\lambda_1=0&\Rightarrow b=z+\lambda_1<0\quad(z<-\lambda_1),\\
b=0:&0\in-z+\lambda_1[-1,1]&\Leftrightarrow |z|\le\lambda_1.
\end{array}
$$

The interval $[-1,1]$ contains the possible supporting slopes of $|b|$ at zero (its **subgradient**). Thus

$$
\boxed{\hat b=S(z,\lambda_1)
=\operatorname{sign}(z)\max(|z|-\lambda_1,0)}.
$$

For $X^TX=I_p$, this applies independently to $z=X^Ty$. For a general design, it is **not** a recipe to threshold the OLS vector: the residuals couple the coefficients. In particular, a zero coordinate at an optimum must satisfy $|X_j^T(y-X\hat\beta)|\le\lambda_1$. The objective is convex, but its coefficient solution need not be unique when columns are dependent. [Friedman et al., §2, equations (5)–(6)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/#S2).

![[assets/figures/2026-11-12-l1-l2-elastic-net/lasso-mechanics.svg]]

*The L1 budget is a diamond. A loss contour can first reach it at an axis corner, where one coefficient is zero. The pictured Laplace prior has a density cusp—not a point mass—at zero.*

For independent Gaussian errors with known variance $\sigma^2>0$, take independent Laplace priors with scale $s>0$:

$$
p(\beta_j)=\frac1{2s}e^{-|\beta_j|/s},\qquad
-\log p(\beta\mid y,X)
=\frac{\|y-X\beta\|^2}{2\sigma^2}+\frac{\|\beta\|_1}{s}+C.
$$

Multiplying by $\sigma^2$ gives lasso with $\boxed{\lambda_1=\sigma^2/s}$. This identifies its **posterior mode (MAP)**, not generally its posterior mean. For example, with scalar observation $z=0.6$, noise variance $1$ and Laplace scale $1$, MAP is zero but the posterior mean is approximately $0.2911$. The continuous prior and posterior both assign probability zero to the singleton $\{\beta_j=0\}$; a zero mode does not change that. The mode/mean distinction is stated in [ISLR, 2nd ed., §6.2.2, printed p. 249 (CMU-hosted copy)](https://www.stat.cmu.edu/~brian/valerie/617-2022/0%20-%20books/ISLRv2_website.pdf); the scalar example is an independently integrated illustration.

## Origin

> [!info]- Source details
> Added on 2026-11-12 as a beginner opening plus the requested norm/Bayesian bridge. The toy coefficients, piecewise derivation and figures are original synthesis. The paper's §2 and the indexed textbook passage on printed p. 249 were read; the whole book was not retrieved. The textbook's informal suggestion of “exactly zero” prior coefficients must not be read as an atom in a continuous Laplace prior.
>
> [[assets/figures/2026-11-12-l1-l2-elastic-net/draw_and_check.py|Generator]] and [[assets/figures/2026-11-12-l1-l2-elastic-net/checks.json|checks]] cover thresholds, optimality conditions, boundaries and the scalar posterior mean. Static previews inspected; no live Obsidian rendering claim.

```atlas
```
