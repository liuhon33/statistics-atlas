---
id: penalized-elastic-net
title: Elastic net
layer: backbone
level: 5
subject: computing
study_band: U–M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Elastic net
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

# Elastic net

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Penalized linear models → Elastic net

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Penalized linear models|Penalized linear models]]

## 1. See it and use it

Imagine two measurements carry almost the same predictive information. You want to remove unhelpful features, but do not want the fitted model to depend too strongly on which near-duplicate is chosen. **Elastic net combines L1 and squared-L2 penalties:** one can create zeros; the other adds smooth shrinkage and stabilizes the coefficient fit.

![[assets/figures/2026-11-12-l1-l2-elastic-net/elastic-net-intro.svg]]

*Constructed separable example: threshold first, then shrink the surviving coefficient.*

Its penalty is $\lambda_1\sum_j|\beta_j|+\frac{\lambda_2}{2}\sum_j\beta_j^2$, with nonnegative strengths. Here the unpenalized coefficients are $(3,0.6)$. With $\lambda_1=\lambda_2=1$, subtract $1$ from the magnitudes, stopping at zero, then divide by $2$: $(3,0.6)\to(2,0)\to(1,0)$. This two-step calculation is special to the figure's separable loss, not a general recipe of fitting lasso and then ridge.

Use it when sparsity and correlated predictors both matter. Put features on comparable scales and select the strengths by validation, with scaling fitted inside each training fold. It can retain correlated features together, but does not guarantee the best predictions or identify causal variables. [scikit-learn, *Linear Models*, §1.1.5](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net).

## 2. How it works — both penalties, one objective

For centred $X\in\mathbb R^{n\times p}$ and $y\in\mathbb R^n$, with an unpenalized intercept handled separately, the modern penalized elastic-net objective is

$$
\hat\beta=\arg\min_\beta\left\{
\frac12\|y-X\beta\|_2^2
+\lambda_1\|\beta\|_1
+\frac{\lambda_2}{2}\|\beta\|_2^2\right\}.
$$

Set $\lambda_2=0$ for [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso|lasso]], or $\lambda_1=0$ for [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression|ridge]]. Both zero gives ordinary least squares. The mixed penalty is convex but, when $\lambda_2>0$, is **not itself a norm**: its two parts scale differently when $\beta$ is multiplied by a constant. Compare [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|norm homogeneity]].

For $X^TX=I_p$, put $z=X^Ty$. The positive-coordinate equation is

$$
(b-z)+\lambda_1+\lambda_2b=0
\quad\Longrightarrow\quad b=\frac{z-\lambda_1}{1+\lambda_2}.
$$

Checking the negative and zero cases gives $\boxed{\hat\beta_j=S(z_j,\lambda_1)/(1+\lambda_2)}$, where $S$ is lasso's soft threshold. With general $X$, coordinate descent instead uses the **partial residual** $r_{-j}=y-\sum_{k\ne j}X_k\beta_k$:

$$
\beta_j\leftarrow
\frac{S(X_j^Tr_{-j},\lambda_1)}{X_j^TX_j+\lambda_2}.
$$

This is a coordinate update, not an independent closed-form fit of every column. [Friedman, Hastie & Tibshirani (2010), §2, equations (1)–(6)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2929880/#S2).

![[assets/figures/2026-11-12-l1-l2-elastic-net/elastic-net-mechanics.svg]]

*The budget has curved sides but retains axis corners when $\lambda_1>0$. Its prior multiplies Gaussian-shaped and Laplace-shaped factors; it does not average their densities.*

**Why the quadratic part helps with duplicates.** When $\lambda_2>0$, the smooth part has Hessian $X^TX+\lambda_2I_p\succ0$, so the whole objective has a unique minimizer. For two identical columns, exchanging their coefficients leaves the objective unchanged; uniqueness therefore forces equal coefficients. Equivalently, for fixed sum $c$, $\beta_1^2+\beta_2^2=c^2/2+(\beta_1-\beta_2)^2/2$ is smallest at equal shares. The L1 cost alone is constant over nonnegative splits of a positive $c$. This proves the exact-duplicate case; it is not a guarantee that every correlated pair is selected together.

**Bayesian bridge.** With Gaussian errors of known variance $\sigma^2>0$, choose the coefficient prior

$$
p(\beta)\propto
\exp\!\left[-\frac{\lambda_1}{\sigma^2}\|\beta\|_1
-\frac{\lambda_2}{2\sigma^2}\|\beta\|_2^2\right].
$$

The negative log posterior, multiplied by $\sigma^2$, is the displayed objective plus a constant. This is an original direct derivation of the MAP interpretation. With at least one positive penalty the prior is proper; with both zero it is flat and improper on $\mathbb R^p$. The product is **not** a Gaussian–Laplace mixture or a spike-and-slab prior. Mean and mode generally differ when the L1 part is present.

> [!note] Keep tuning conventions consistent
> Another common objective is $\|y-X\beta\|^2/(2n)+\lambda[\rho\|\beta\|_1+(1-\rho)\|\beta\|_2^2/2]$, where $0\le\rho\le1$. Multiplying by $n$ shows $\lambda_1=n\lambda\rho$ and $\lambda_2=n\lambda(1-\rho)$. Here $\rho=1$ means lasso and $\rho=0$ means ridge. Never compare numerical penalty strengths without also comparing loss scaling. This is the convention of [the modern elastic-net documentation](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net); no additional coefficient rescaling is performed here.

## Origin

> [!info]- Source details
> Added on 2026-11-12 with a beginner example and the explicitly requested norm/Bayesian connections. Objective and update convention checked against Friedman et al. §2 and the official scikit-learn elastic-net formulation. The identical-column argument, mixed-prior derivation and all figures are original synthesis. The historical Zou–Hastie paper was located but could not be fetched; its original rescaled-estimator convention is not claimed as the convention used here.
>
> [[assets/figures/2026-11-12-l1-l2-elastic-net/draw_and_check.py|Reproducible generator]] and [[assets/figures/2026-11-12-l1-l2-elastic-net/checks.json|checks]] include the shared toy solutions, optimality conditions, exact-duplicate example, prior-objective identity and geometric boundaries. Static previews inspected; live Obsidian rendering unverified.

```atlas
```
