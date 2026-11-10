---
id: reg-inference-residual-variance-and-degrees-of-freedom
title: Residual variance and degrees of freedom
layer: backbone
level: 5
subject: statistics
study_band: U
backbone_path: Statistical inference & modeling → Regression & linear models → Linear regression → Regression uncertainty → Residual variance and degrees of freedom
created: '2026-11-08'
updated: '2026-11-10'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Regression uncertainty]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/isl]]'
---

# Residual variance and degrees of freedom

Statistical inference & modeling → Regression & linear models → Linear regression → Regression uncertainty → Residual variance and degrees of freedom

Parent: [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Regression uncertainty|Regression uncertainty]]

## 1. See it and use it — about one minute

Fit a line to five people's heights and weights. How much scatter remains around it? A **residual** is an observed weight minus its fitted value.

![[assets/figures/2026-11-10-residual-df/residual-df.png]]

*Original example: five residuals remain, but fitting the line uses two degrees of freedom.*

**Residual degrees of freedom count how many residual values can vary freely after the fitting constraints are imposed.** Estimating the intercept and slope imposes two relationships among the residuals, leaving $n-2=3$ degrees of freedom—not three remaining people.

**Use it:** square the residuals, add them, and divide by the residual degrees of freedom. Here the residuals are $3,-3,0,-3,3$ kg:

$$
s^2=\frac{\text{sum of squared residuals}}{n-2}
=\frac{9+9+0+9+9}{5-2}=12\ \text{kg}^2.
$$

**Interpret it:** $s=\sqrt{12}\approx3.46$ kg estimates the noise's standard deviation around the true mean line. Dividing by five would underestimate noise on average: fitting already made the residuals smaller. This correction assumes a correct straight-line mean, distinct predictor values, and uncorrelated, zero-mean errors with common variance; normality is unnecessary. [Weisberg, *Applied Linear Regression*, 3rd ed., §2.3, pp. 25–26](https://www.stat.cmu.edu/~brian/valerie/617-2022/617-2021/0%20-%20books/weissberg%20ALR%203rd%20ed.pdf#page=38).

## 2. How it works — why sample variance and covariance divide by n − 1

The opening fitted **two** coefficients. Sample variance fits only a **constant mean**, so its divisor is $n-1$. The algebra below explains why this produces an unbiased estimate—not merely why the centered values satisfy a constraint.

### Sample variance: estimating the mean removes one variance-unit on average

Let $X_1,\ldots,X_n$ be independent, identically distributed (iid), with $n\ge2$, mean $\mu$ and finite variance $\sigma^2$. Write $\bar X=n^{-1}\sum_iX_i$. Uppercase letters denote random samples; lowercase letters denote observed values. Normality is not required.

For every sample, expand $X_i-\mu=(X_i-\bar X)+(\bar X-\mu)$:

$$
\begin{aligned}
\sum_{i=1}^n(X_i-\mu)^2
&=\sum_i(X_i-\bar X)^2
 +2(\bar X-\mu)\underbrace{\sum_i(X_i-\bar X)}_{0}
 +n(\bar X-\mu)^2,\\
\therefore\quad \sum_i(X_i-\bar X)^2
&=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2.
\end{aligned}
$$

This identity is deterministic. **Now** use the sampling assumptions: $\mathbb E\bar X=\mu$ and $\operatorname{Var}(\bar X)=\sigma^2/n$. Taking expectations gives

$$
\mathbb E\!\left[\sum_i(X_i-\bar X)^2\right]
=n\sigma^2-n\frac{\sigma^2}{n}
=\boxed{(n-1)\sigma^2}.
$$

![[assets/figures/2026-11-10-residual-df/bessel-expectation.png]]

*Original diagram for $n=3$: the mean-estimation component has expected squared length $\sigma^2$, leaving $2\sigma^2$. These are expectations, not fixed proportions for each sample.*

Consequently,

$$
\boxed{S^2=\frac{\sum_i(X_i-\bar X)^2}{n-1},\qquad \mathbb E[S^2]=\sigma^2.}
$$

Using $n$ instead gives expectation $(n-1)\sigma^2/n$. Fitting the mean to these same observations reduces their squared deviations; the correction compensates for that reduction **on average**. This is Bessel's correction. See Kyle Siegrist, [*The Sample Variance*, “The Standard Sample Variance,” unbiasedness and proof](https://www.randomservices.org/random/sample/Variance.html).

**Two boundaries:** if the true mean $\mu$ is known and used, $n^{-1}\sum_i(X_i-\mu)^2$ is already unbiased. If the task is simply to describe the empirical distribution that assigns probability $1/n$ to each observed value, its variance uses $n$. The $n-1$ formula answers the different question of unbiased estimation of a population variance from an iid sample. Nor does unbiased $S^2$ imply unbiased $S=\sqrt{S^2}$.

### Sample covariance: the same correction, not n − 2

Now observe iid **pairs** $(X_i,Y_i)$ with finite second moments. Let their means be $\mu_X,\mu_Y$ and their covariance be $\sigma_{XY}$. The pairs are independent across observations; $X_i$ and $Y_i$ within a pair need **not** be independent.

Expanding around the two true means, with the centered sums equal to zero, gives

$$
\sum_i(X_i-\bar X)(Y_i-\bar Y)
=\sum_i(X_i-\mu_X)(Y_i-\mu_Y)
-n(\bar X-\mu_X)(\bar Y-\mu_Y).
$$

The key expectation is

$$
\begin{aligned}
\mathbb E[(\bar X-\mu_X)(\bar Y-\mu_Y)]
&=\operatorname{Cov}(\bar X,\bar Y)\\
&=\frac1{n^2}\sum_{i,j}\operatorname{Cov}(X_i,Y_j)
=\frac{n\sigma_{XY}}{n^2}=\frac{\sigma_{XY}}n.
\end{aligned}
$$

Only the $i=j$ terms survive, because different pairs are independent. Therefore

$$
\begin{aligned}
\mathbb E\!\left[\sum_i(X_i-\bar X)(Y_i-\bar Y)\right]
&=n\sigma_{XY}-n\frac{\sigma_{XY}}n=(n-1)\sigma_{XY},\\
\boxed{S_{XY}=\frac{\sum_i(X_i-\bar X)(Y_i-\bar Y)}{n-1}}
&\quad\Longrightarrow\quad\mathbb E[S_{XY}]=\sigma_{XY}.
\end{aligned}
$$

Setting $Y_i=X_i$ recovers the variance proof. This is also why every entry of the [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Vector means & covariance/Sample covariance matrix|sample covariance matrix]] uses the same divisor. See Siegrist, [*Sample Correlation and Regression*, “Sample Covariance,” unbiasedness proof](https://www.randomservices.org/random/sample/Covariance.html).

**Why not subtract two for two means?** We center two vectors in the *same* observation space, then pair their remaining coordinates. We do not fit two different directions to one response vector as in a regression with intercept and slope. The geometry below makes this distinction precise.

## 3. Deeper understanding — projection, t statistics, and Hilbert spaces

### Three observations become one vector in 3D

Here the axes represent **observations**, not measured features. Three observations $x_1,x_2,x_3$ of one feature form one vector $\mathbf x=(x_1,x_2,x_3)^\top\in\mathbb R^3$. Another feature on those same three observations gives another vector in the same space.

Let $\mathbf1=(1,\ldots,1)^\top$. The line $\operatorname{span}(\mathbf1)$ contains the constant vectors. Projecting onto it gives

$$
P\mathbf x=\frac{\mathbf1^\top\mathbf x}{\mathbf1^\top\mathbf1}\mathbf1
=\bar x\mathbf1,
\qquad P=\frac{\mathbf1\mathbf1^\top}{n}.
$$

The projection is the **vector** $\bar x\mathbf1$, not the scalar $\bar x$. What remains is

$$
\mathbf c=\mathbf x-\bar x\mathbf1=(I-P)\mathbf x,
\qquad \mathbf1^\top\mathbf c=0.
$$

![[assets/figures/2026-11-09-standardization/02-project-and-center.svg]]

*Reused original three-observation diagram. Gold is the all-ones direction. Colored arrows represent entire features, each with three coordinates. Subtracting each mean projection leaves a vector in the common plane $H: c_1+c_2+c_3=0$. The translucent disk is only a patch of this infinite plane. The middle panel translates the residual arrow to the origin without rotating it.*

For three observations, $c_3=-c_1-c_2$: choose two coordinates and the third is determined. Thus $H=\mathbf1^\perp$ is a **two-dimensional plane through the origin**. In general, it has dimension $n-1$. We remove one **direction**, not one observation. For cyan A in the figure,

$$
\mathbf x=(1,2,3)^\top,\quad P\mathbf x=(2,2,2)^\top,\quad
\mathbf c=(-1,0,1)^\top,\quad
s^2=\frac{\|\mathbf c\|^2}{2}=1.
$$

Pythagoras gives exactly section 2's algebra, now as squared lengths:

$$
\|\mathbf x-\mu\mathbf1\|^2
=n(\bar x-\mu)^2+\|\mathbf c\|^2.
$$

### Dimension explains the divisor only together with the noise model

Set $C=I-P$. This centering matrix is symmetric, satisfies $C^2=C$, and projects onto $H$, with $\operatorname{tr}(C)=\operatorname{rank}(C)=n-1$. For an iid sample, write $\mathbf X=\mu\mathbf1+\boldsymbol\varepsilon$, where $\mathbb E\boldsymbol\varepsilon=0$ and $\operatorname{Cov}(\boldsymbol\varepsilon)=\sigma^2I$. Then

$$
\begin{aligned}
\mathbb E\|C\mathbf X\|^2
&=\mathbb E[\boldsymbol\varepsilon^\top C\boldsymbol\varepsilon]\\
&=\sum_{i,j}C_{ij}\mathbb E[\varepsilon_i\varepsilon_j]
=\sigma^2\sum_iC_{ii}
=(n-1)\sigma^2.
\end{aligned}
$$

Equivalently, in any orthonormal basis of $H$, there are $n-1$ centered coordinates, each with variance $\sigma^2$. Their squared values add to the residual squared length. They are uncorrelated, but not necessarily independent unless extra assumptions such as Gaussianity hold. **A dimension count alone does not prove unbiasedness:** correlated or unequal-variance errors instead give $\mathbb E\|C\boldsymbol\varepsilon\|^2=\operatorname{tr}(C\Sigma)$, where $\Sigma$ is their covariance matrix.

For covariance, both centered vectors occupy the same $H$:

$$
s_{xy}=\frac{(C\mathbf x)^\top(C\mathbf y)}{n-1}.
$$

In a common orthonormal basis of $H$, their dot product sums **$n-1$ paired-coordinate products**. Algebraically, for iid pairs $\operatorname{Cov}(\mathbf X,\mathbf Y)=\sigma_{XY}I$, so its expectation is $\sigma_{XY}\operatorname{tr}(C)=(n-1)\sigma_{XY}$. Centering both vectors applies the same projection: $C^\top C=C$, not a projection of rank $n-2$.

This also connects to standardization: $s_x=\|C\mathbf x\|/\sqrt{n-1}$, while sample correlation is the cosine between the two centered vectors, because their common $n-1$ factors cancel.

### Where n − 1 enters the t statistic

For the one-sample mean test, the statistic is

$$
T=\frac{\bar X-\mu_0}{S/\sqrt n},
\qquad S^2=\frac{\|C\mathbf X\|^2}{n-1}.
$$

**We do not divide $T$ directly by $n-1$.** We divide the centered squared length by $n-1$ to estimate the noise variance, and then use $S/\sqrt n$ as the estimated standard error of the mean.

Under the null, if the observations are iid $N(\mu_0,\sigma^2)$ with $\sigma>0$, use $u=\mathbf1/\sqrt n$ and $\mathbf Z=(\mathbf X-\mu_0\mathbf1)/\sigma$. In an orthonormal basis starting with $u$, the coordinates are independent standard normals. Thus

$$
A=u^\top\mathbf Z\sim N(0,1),\qquad
Q=\|C\mathbf Z\|^2=\frac{(n-1)S^2}{\sigma^2}\sim\chi^2_{n-1},
\qquad A\perp Q,
$$

and

$$
\boxed{T=\frac{A}{\sqrt{Q/(n-1)}}\sim t_{n-1}.}
$$

For three observations, the residual plane supplies two independent Gaussian coordinates, so $Q\sim\chi^2_2$ and $T\sim t_2$. The dimension survives without normality; this exact distributional conclusion generally does not. See [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F|Student t, chi-square and F]] and Lockhart, [STAT 801, “Normal samples: Distribution Theory,” opening theorem and proof](https://www.sfu.ca/~lockhart/richard/801/01_1/lectures/normal_samples/web.html).

### Hilbert spaces: the same projection principle, different objects

[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Hilbert spaces|Hilbert spaces]] generalize this geometry: projection onto a closed linear subspace leaves an orthogonal residual. But distinguish the two settings:

| | Finite observed sample | Population random variables |
| --- | --- | --- |
| Space and inner product | $\mathbb R^n$, $\langle\mathbf x,\mathbf y\rangle=\mathbf x^\top\mathbf y$ | $L^2$, $\langle X,Y\rangle=\mathbb E[XY]$ |
| Constant direction | All-ones vector $\mathbf1$ | Constant random variable $1$ |
| Projection onto constants | $\bar x\mathbf1$ | $\mathbb E[X]\,1$ |
| Orthogonal remainder | $\mathbf x-\bar x\mathbf1$ | $X-\mathbb E[X]$ |
| Squared residual norm | $\sum_i(x_i-\bar x)^2$ | $\operatorname{Var}(X)$ |

The population projection coefficient follows from $\langle X,1\rangle/\langle1,1\rangle=\mathbb E[X]$. Likewise, covariance is the inner product of the two population-centered random variables. Replacing the constants by the closed subspace of square-integrable functions of $Z$ gives [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection|conditional expectation as an L² projection]]. The projection theorem supplies the common structure; it does **not** insert a sample-size correction into the population variance. [Dufour, *Hilbert spaces*, Theorems 2.4 and 3.4–3.6, pp. 4–5](https://jeanmariedufour.github.io/ResE/Dufour_1999_C_TS_HilbertSpaces.pdf#page=7).

Even on a finite sample, using the empirical inner product $\langle\mathbf x,\mathbf y\rangle_n=n^{-1}\mathbf x^\top\mathbf y$ gives the **same projection** but a squared residual norm with divisor $n$. Switching to $n-1$ is an inferential bias correction, not a requirement for being a Hilbert space.

### Back to regression: n − 1 is the intercept-only case

For a fixed design matrix $D$ of rank $p<n$, OLS projects a response vector onto the $p$-dimensional column space of $D$. Its residual lies in a space of dimension $n-p$. Under a correct linear mean and zero-mean errors with covariance $\sigma^2I$, the same calculation gives $\mathbb E[\mathrm{RSS}]=(n-p)\sigma^2$.

| Fitted mean space | Dimension used | Residual divisor |
| --- | --- | --- |
| Constants only: $\operatorname{span}(\mathbf1)$ | $1$ | $n-1$ |
| Intercept plus a nonconstant predictor: $\operatorname{span}(\mathbf1,\mathbf x)$ | $2$ | $n-2$ |
| General OLS design, including any intercept | $p=\operatorname{rank}(D)$ | $n-p$ |

Count **independent fitted directions**, not simply written coefficient symbols. This explains why the opening example divides by three, while a sample variance computed from the same five weights would divide by four. See [Weisberg, §3.4.4, p. 57, equation (3.14)](https://www.stat.cmu.edu/~brian/valerie/617-2022/617-2021/0%20-%20books/weissberg%20ALR%203rd%20ed.pdf#page=70); his $p+1$ counts predictors plus intercept, whereas $p$ here counts all independent fitted directions.

## Origin and checks

> [!info]- Source details
> Introductory enrichment only, prepared by Codex for review. The invented height–weight pairs reuse the example in the Linear regression introduction; this new static diagram highlights residuals and degrees of freedom rather than prediction. No external figure was copied. A static view suffices because the comparison is a count and a set of fixed residual gaps, not a temporal process.
>
> [[assets/figures/2026-11-10-residual-df/draw_residual_df.py|Reproducible figure and checks]]; [[assets/figures/2026-11-10-residual-df/checks.json|example check results]]. Checks verify the fitted line, residuals, both fitting constraints, squared sum, degrees of freedom and variance. These example checks do not prove the general unbiasedness result, which is sourced above.
>
> Follow-up: the user requested algebraic variance/covariance proofs and the three-observation projection rationale, with t-statistic and Hilbert-space connections, then explicitly chose sections 2 and 3 on this same backbone page rather than a separate digest. The first-level opening remains unchanged. Codex expanded the proofs, distinguished geometry from sampling assumptions, and clarified that the t denominator is a standard error rather than n−1 itself. The existing standardization and t-geometry learning material informed this standalone treatment; the original learning notes remain unchanged.
>
> The reused projection figure and its reproducible source are in `assets/figures/2026-11-09-standardization/`. The new [[assets/figures/2026-11-10-residual-df/draw_bessel_correction.py|expectation diagram and exact checks]] and [[assets/figures/2026-11-10-residual-df/bessel-checks.json|check results]] enumerate all 27 equiprobable size-three samples from a small paired population, verify both algebraic identities and expectations with rational arithmetic, and check centering matrices for n=2,…,8. These checks support the illustrations; the general proofs are in the text. Sources were read directly, and static renders inspected. The existing three-panel projection diagram already shows the required subtraction without a new animation.

```atlas
```
