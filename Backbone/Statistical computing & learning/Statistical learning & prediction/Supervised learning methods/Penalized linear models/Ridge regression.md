---
id: ridge
title: Ridge regression
layer: backbone
level: 5
subject: computing
study_band: U–M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Ridge regression
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
related:
- '[[Backbone/Statistical inference & modeling/Bayesian inference/Hierarchical Bayesian modeling/Hierarchies & pooling/Hierarchies & pooling]]'
sources:
- '[[_system/Sources/isl]]'
---

# Ridge regression

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Ridge regression

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Penalized linear models|Penalized linear models]]

## 1. See it and use it

Suppose two measured features help predict a response. An ordinary least-squares fit chooses their coefficients using training error alone. **Ridge regression adds a cost for large coefficients**, so fitting the observed data perfectly is no longer the only goal. This is L2 regularization for a squared-error regression loss.

![[assets/figures/2026-11-12-l1-l2-elastic-net/ridge-intro.svg]]

*Constructed two-coefficient example; gray is the unpenalized fit and blue is ridge.*

The penalty is $\frac{\lambda_2}{2}\sum_j\beta_j^2$, where $\beta_j$ is a feature's coefficient and $\lambda_2\ge0$ controls its strength. In the figure's deliberately separable example, $\lambda_2=1$ changes $(3,0.6)$ to $(1.5,0.3)$: both estimates move toward zero, but neither is discarded.

Use ridge when you want a more stable predictor, especially with overlapping information among features, rather than a short list of selected variables. Put features on comparable scales first; normally leave the intercept unpenalized. Choose the penalty using validation, not the smallest training error. More shrinkage can help prediction, but excessive shrinkage underfits. Unlike [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso|lasso]], ridge has no threshold that deliberately zeros small coefficients. [CMU, *Regularization*, ridge-regression slides](https://www.stat.cmu.edu/cmsac/sure/2022/materials/lectures/slides/13-Regularization.html).

## 2. How it works — squared norm and Gaussian prior

Let $X\in\mathbb R^{n\times p}$ and $y\in\mathbb R^n$ be centred predictors and responses; $\beta\in\mathbb R^p$ contains the slopes. Centring handles an unpenalized intercept separately. Use the **half-sum-of-squares** convention throughout this comparison:

$$
\hat\beta=\arg\min_\beta\left\{
\frac12\|y-X\beta\|_2^2+\frac{\lambda_2}{2}\|\beta\|_2^2\right\}.
$$

The [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|Euclidean norm]] is $\|\beta\|_2=\sqrt{\sum_j\beta_j^2}$. Ridge penalizes its **square**, not the norm itself. A squared norm is not a norm: doubling $\beta$ quadruples it.

For $\lambda_2>0$, differentiating gives

$$
\begin{aligned}
0&=X^T(X\hat\beta-y)+\lambda_2\hat\beta,\\
(X^TX+\lambda_2I_p)\hat\beta&=X^Ty,\\
\hat\beta&=(X^TX+\lambda_2I_p)^{-1}X^Ty.
\end{aligned}
$$

The matrix is positive definite even if $X$ is rank deficient, since $v^T(X^TX+\lambda_2I_p)v=\|Xv\|^2+\lambda_2\|v\|^2>0$ for $v\ne0$. When $X^TX=I_p$, writing $z=X^Ty$ gives $\hat\beta_j=z_j/(1+\lambda_2)$, which produces the opening example. This coordinate-wise formula does **not** hold for a general correlated design.

![[assets/figures/2026-11-12-l1-l2-elastic-net/ridge-mechanics.svg]]

*Left: a squared-norm budget is a disk in coefficient space; the nearest loss contour touches its smooth boundary. Right: a Gaussian prior. Both are original illustrations with the opening example's parameters, not observational data.*

For a Bayesian reading, assume independent Gaussian noise with known variance $\sigma^2>0$ and a prior $\beta\sim\mathcal N(0,\tau^2I_p)$, independent of that noise. Dropping terms constant in $\beta$,

$$
-\log p(\beta\mid y,X)
=\frac{\|y-X\beta\|^2}{2\sigma^2}
+\frac{\|\beta\|^2}{2\tau^2}+C.
$$

Multiplication by $\sigma^2$ gives exactly ridge with $\boxed{\lambda_2=\sigma^2/\tau^2}$. The Gaussian posterior's **mode and mean** coincide; its covariance is still additional information, not supplied by the ridge point estimate alone. [Rasmussen & Williams, §2.1, equations (2.7)–(2.9), printed pp. 9–11](https://gaussianprocess.org/gpml/chapters/RW2.pdf#page=3).

Two boundaries matter: using mean loss $\|y-X\beta\|^2/(2n)$ divides the matching $\lambda_2$ by $n$; and shrinkage is toward zero in the eigenvector directions of $X^TX$, not necessarily monotone for every original coefficient. A zero ridge coefficient is possible by symmetry/cancellation—it is not selected by a zeroing threshold. [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net|Elastic net]] adds such a threshold through an L1 term.

## Origin

> [!info]- Source details
> Introductory reference and requested norm/Bayesian bridge added on 2026-11-12. The toy loss, algebraic checks and figures are original explanatory synthesis, not a transcription of user handwriting. Sources were read at the cited passages. The existing ISL source record remains a curriculum reference; no unread book chapter is claimed as verified.
>
> Reproduce the figures and checks with [[assets/figures/2026-11-12-l1-l2-elastic-net/draw_and_check.py|the shared generator]]; numerical evidence is in [[assets/figures/2026-11-12-l1-l2-elastic-net/checks.json|checks.json]]. The derivation supplies the mathematical argument; numerical agreement is supporting evidence. Static previews were inspected; live Obsidian rendering was not verified.

## Connections

- [[Backbone/Statistical inference & modeling/Bayesian inference/Hierarchical Bayesian modeling/Hierarchies & pooling/Hierarchies & pooling|Hierarchies & pooling]] — Gaussian-prior shrinkage connects ridge-style penalties with partial-pooling models.

```atlas
```
