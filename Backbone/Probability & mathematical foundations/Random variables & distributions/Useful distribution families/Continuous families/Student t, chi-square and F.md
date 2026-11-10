---
id: continuous-student-t-chi-square-and-f
title: Student t, chi-square and F
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Student t, chi-square and F
created: '2026-11-08'
updated: '2026-11-10'
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

# Student t, chi-square and F

Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Student t, chi-square and F

Parent: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Continuous families|Continuous families]]

## 1. See it and use it — chi-square

You have two dice: one fair, one loaded. Which is which? Roll each independently 60 times. A fair die **expects 10 of each face**, but random variation means the counts will not match perfectly.

![[assets/figures/2026-11-10-chi-square/chi-square-intro.png]]

*Illustrative counts, not an experiment: compare each die against fairness, not against the other die.*

Measure the overall mismatch by squaring each observed-minus-expected difference, dividing by its expected count, then adding:

$$
Q=\sum_{i=1}^{6}\frac{(O_i-10)^2}{10},
\qquad O_i=\text{count of face }i.
$$

Die A's counts $(8,11,10,9,12,10)$ give **$Q=1$**; die B's $(4,6,8,10,12,20)$ give **$Q=16$**. For example, B's twenty sixes contribute $(20-10)^2/10=10$ alone.

The **chi-square distribution** describes sums of squared independent standard normal variables. Here it is an **approximate reference under fairness**, not the distribution of individual rolls. Use **5 degrees of freedom**: six counts minus their fixed-total constraint. Independent rolls and sufficiently large expected counts are needed; ours are 10. [NIST: distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm); [goodness-of-fit test](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35f.htm).

At a prechosen 5% significance level, flag $Q>11.07$. **B is flagged; A is not.** This is evidence of bias in B, not proof of cheating or proof that A is fair.

## 2. How it works — density, dice and degrees of freedom

Two claims need different justifications: a sum of independent squared standard normals is **exactly** chi-square; the dice mismatch score is **asymptotically** chi-square **under fairness**. The second claim does not say that die rolls are normal.

### 2.1 Deriving the chi-square density

Let $Z_1,\ldots,Z_k$ be independent $N(0,1)$ variables, where $k$ is a positive integer, and write $Q_k=\sum_{j=1}^k Z_j^2$.

**Start with one square.** For $Y=Z^2$ and $y>0$, both $+\sqrt y$ and $-\sqrt y$ map to $y$. With $\phi(z)=(2\pi)^{-1/2}e^{-z^2/2}$,

$$
\begin{aligned}
F_Y(y)&=P(-\sqrt y\le Z\le\sqrt y),\\
f_Y(y)&=\frac{\phi(\sqrt y)+\phi(-\sqrt y)}{2\sqrt y}
=\frac{y^{-1/2}e^{-y/2}}{\sqrt{2\pi}}.
\end{aligned}
$$

The two branches matter: keeping only the positive root would lose half the probability. This is the one-degree-of-freedom density. [Taboga, “Chi-square distribution,” subsection on the square of a standard normal](https://www.statlect.com/probability-distributions/chi-square-distribution).

**Add independent squares using [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Convolution of independent sums|convolution]].** Introduce the convenient family

$$
g_a(q)=\frac{q^{a-1}e^{-q/2}}{2^a\Gamma(a)},\quad q>0,\qquad
\Gamma(a)=\int_0^\infty t^{a-1}e^{-t}\,dt,\quad a>0.
$$

Substituting $q=2t$ verifies that $g_a$ integrates to 1. Since $\Gamma(1/2)=\sqrt\pi$, the density just derived is $g_{1/2}$. For independent variables with densities $g_a,g_b$,

$$
\begin{aligned}
(g_a*g_b)(q)
&=\int_0^q g_a(x)g_b(q-x)\,dx\\
&=\frac{e^{-q/2}}{2^{a+b}\Gamma(a)\Gamma(b)}
  \int_0^q x^{a-1}(q-x)^{b-1}\,dx\\
&=\frac{e^{-q/2}q^{a+b-1}}{2^{a+b}\Gamma(a)\Gamma(b)}
  \underbrace{\int_0^1 v^{a-1}(1-v)^{b-1}\,dv}_{\Gamma(a)\Gamma(b)/\Gamma(a+b)}\\
&=g_{a+b}(q).
\end{aligned}
$$

The third line uses $x=qv$. The integral identity follows by writing $\Gamma(a)\Gamma(b)$ as a double integral and substituting $s=x+y$, $v=x/(x+y)$: its Jacobian is $s$, and the integral separates into $\Gamma(a+b)$ times the displayed integral on $(0,1)$.

Thus adding $k$ independent squares adds $k$ copies of the shape parameter $1/2$:

$$
\boxed{f_{Q_k}(q)=\frac{q^{k/2-1}e^{-q/2}}{2^{k/2}\Gamma(k/2)},\quad q>0.}
$$

The density is zero for $q<0$, and $P(Q_k=0)=0$. This is [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Exponential and gamma|Gamma]] with **shape $k/2$, scale $2$** (equivalently, rate $1/2$). The density also defines a distribution for noninteger $k>0$; the literal “$k$ independent squares” construction uses integer $k$. The calculation above spells out the convolution route to the gamma addition law. [Sun, *The Art of Chance*, §38.1 and §38.3, Propositions 38.4–38.5](https://dlsun.github.io/skis/sums/gamma.html#chi-square-distribution).

### 2.2 Why the dice statistic has five degrees of freedom

**Assumptions:** a fixed number $n$ of independent, identically distributed rolls; under $H_0$, each of the six faces has probability $1/6$. No probabilities are fitted from the observed counts. Keep six faces fixed while letting $n$ grow.

**Step 1 — count jointly, not as six independent experiments.** The vector of counts has a [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Discrete families/Multinomial|multinomial distribution]]:

$$
O=(O_1,\ldots,O_6)^T\sim\operatorname{Multinomial}(n;1/6,\ldots,1/6).
$$

For one roll, the six face-indicators sum to 1: distinct faces cannot both occur. Adding $n$ such indicator vectors gives

$$
E[O_i]=\frac n6,\qquad
\operatorname{Var}(O_i)=\frac{5n}{36},\qquad
\operatorname{Cov}(O_i,O_j)=-\frac n{36}\quad(i\ne j).
$$

**Step 2 — expose the constraint.** Define the Pearson residuals and score

$$
R_i=\frac{O_i-n/6}{\sqrt{n/6}},\qquad
Q_n=\sum_{i=1}^6 R_i^2=\|R\|^2.
$$

Exactly, $\sum_iR_i=0$. Therefore the vector lives in the **five-dimensional subspace** $S=\{r\in\mathbb R^6:\sum_i r_i=0\}$. This is the [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom|degrees-of-freedom]] idea: six coordinates, one independent linear constraint. It counts free directions, not rolls. Five counts determine the sixth, but they are **not independent**.

**Step 3 — show that the limiting variability is one in each free direction.** Constraint-counting alone is not enough to prove a chi-square law. Let $\mathbf1$ be the six-vector of ones, $u=\mathbf1/\sqrt6$, and $I_6$ the identity matrix. From the covariance formulas,

$$
\operatorname{Cov}(R)=P=I_6-uu^T.
$$

$P$ is the orthogonal projection onto $S$: $Pu=0$, while $Pr=r$ for $r\in S$. Its eigenvalues are five 1s and one 0. The [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Multivariate CLT|multivariate CLT]], applied to the iid face-indicator vectors, gives

$$
R\xrightarrow{d}G,\qquad G\sim N_6(0,P).
$$

This is a Gaussian confined to $S$, not a full six-dimensional Gaussian. In particular, each original $R_i$ has variance $5/6$, **not** 1; calling them six independent standard normals would be wrong.

**Step 4 — rotate to five orthonormal coordinates.** Choose a $6\times5$ matrix $H$ whose columns are an orthonormal basis of $S$. Then $H^TH=I_5$, $HH^T=P$, and

$$
H^TR\xrightarrow{d}N_5(0,H^TPH)=N_5(0,I_5).
$$

The five limiting coordinates are independent standard normals: joint Gaussianity is what turns their zero covariances into independence. Since $R\in S$, changing to these coordinates preserves squared length:

$$
Q_n=\|R\|^2=\|H^TR\|^2
\xrightarrow{d}\sum_{j=1}^{5}Z_j^2
\sim\boxed{\chi_5^2}.
$$

The last limit uses continuity of squared length. **We rotate all six dependent residuals; we do not simply discard the sixth squared term.** This is the projection-coordinate version of the multinomial CLT proof of Pearson's limit theorem. [Guntuboyina, Berkeley Statistics 210B, Lecture 1, §1.1, p. 1](https://www.stat.berkeley.edu/~aditya/resources/Lecture-ONE-210b-2014.pdf#page=1).

![[assets/figures/2026-11-10-chi-square/dice-limit.png]]

*Top: why six counts leave five Gaussian directions. Bottom: seeded simulations compare the finite-sample fair-die score with its continuous $\chi_5^2$ reference. The steps are real discreteness; the curves illustrate the approximation, not prove the limit.*

For the opening's $n=60$, this justifies an **approximation**, not an exact distribution: $Q_n$ has finitely many possible values, whereas $\chi_5^2$ is continuous. The reference applies to a **fair** die. A loaded die's score need not follow this central chi-square law; that mismatch is what the test seeks. Its displayed value $16$ is compared against what fairness would predict.

### 2.3 Properties and what changes with degrees of freedom

For $Q_k\sim\chi_k^2$:

| Property | Formula | Interpretation |
| --- | --- | --- |
| Mean | $E[Q_k]=k$ | Each independent squared standard normal contributes 1 on average. |
| Variance | $\operatorname{Var}(Q_k)=2k$ | Absolute spread grows: standard deviation is $\sqrt{2k}$. |
| Relative spread | $\operatorname{SD}(Q_k)/E[Q_k]=\sqrt{2/k}$ | Spread becomes smaller **relative to the mean**. |
| Mode | $k-2$ for $k>2$ | The peak moves right; for $k=1,2$ the density decreases from the boundary at 0. |
| Skewness | $\sqrt{8/k}$ | Right-skew decreases, but remains positive for every finite $k$. |
| Independent addition | $\chi_a^2+\chi_b^2\sim\chi_{a+b}^2$ | Degrees of freedom add **when the summands are independent**. |

**Quick checks from the density.** Substitution $q=2t$ gives $E[Q_k^m]=2^m\Gamma(k/2+m)/\Gamma(k/2)$ for nonnegative integer $m$. Using $\Gamma(a+1)=a\Gamma(a)$ yields $E[Q_k]=k$, $E[Q_k^2]=k(k+2)$ and variance $2k$. The third central moment is $8k$, giving the listed skewness. Also,

$$
\frac{d}{dq}\log f_{Q_k}(q)=\frac{k/2-1}{q}-\frac12,
$$

so the interior peak is at $q=k-2$ when $k>2$. At $k=1$ the density diverges as $q\downarrow0$ but remains integrable; at $k=2$ it is $\tfrac12 e^{-q/2}$. [NIST, §1.3.6.6.6, density and common statistics](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm).

![[assets/figures/2026-11-10-chi-square/chi-square-shapes.png]]

*Left: increasing $k$ shifts and widens the distribution. Right: centering and scaling removes that shift/spread, revealing the increasingly bell-shaped form. These are evaluated densities, not fitted curves.*

### 2.4 Why more degrees of freedom looks more bell-shaped

Write $Q_k=\sum_{j=1}^k Y_j$ with $Y_j=Z_j^2$. The $Y_j$ are iid with mean 1 and variance 2. Applying the [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT|classical iid central limit theorem]] gives

$$
\boxed{\frac{Q_k-k}{\sqrt{2k}}
=\frac{\sum_{j=1}^k(Y_j-1)}{\sqrt{2k}}
\xrightarrow{d}N(0,1)\quad\text{as }k\to\infty.}
$$

So for large $k$, $Q_k$ is approximately $N(k,2k)$—not $N(0,1)$ unless standardized. The declining skewness $\sqrt{8/k}$ makes the observation quantitative. Repeated [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Convolution of independent sums|convolution]] constructs the sums exactly; the CLT explains their limiting standardized shape. [Sun, *The Art of Chance*, §36.1, Theorem 36.1](https://dlsun.github.io/skis/sums/clt.html#statement-and-proof).

**Do not mix up the two limits:** rolling the same six-sided die more often sends $n\to\infty$ but leaves **df = 5**. It improves the chi-square approximation; it does **not** make $\chi_5^2$ itself more bell-shaped. The shape comparison above sends **$k\to\infty$**, adding independent squared-normal contributions. A normal approximation can still be poor in the tails, especially for small $k$.

## Origin

> [!info]- Source details
> NIST/SEMATECH e-Handbook of Statistical Methods, §1.3.6.6.6, “Chi-Square Distribution,” and §1.3.5.15, “Chi-Square Goodness-of-Fit Test,” read 2026-11-10. The dice example and diagram are original explanatory additions; counts are invented for illustration. Fairness specifies all six probabilities as 1/6, with no fitted parameters, so the reference degrees of freedom are 6−1=5. The six counts are dependent because their sum is fixed; they are not six independent normal variables. The 95th percentile is approximately 11.0705; right-tail probabilities are approximately 0.9626 for A and 0.00684 for B, using the chi-square approximation rather than an exact multinomial calculation. The 5% false-alarm level applies to each die's test separately, not a combined guarantee across both tests. Reproducible drawing code and numerical checks: [[assets/figures/2026-11-10-chi-square/draw_chi_square.py|Python source]] and [[assets/figures/2026-11-10-chi-square/checks.json|checks]]. This introduction covers only chi-square; Student t and F are not developed in this pass.

>
> Tier 2 added 2026-11-10 at the user's request, preserving the dice opening. Source-checked reference results: Taboga's square-of-normal transformation; Sun, *The Art of Chance*, §38.1/§38.3 (gamma addition and chi-square) and §36.1 (iid CLT); Guntuboyina, Berkeley Statistics 210B Lecture 1, §1.1 p. 1 (Pearson's multinomial CLT limit); NIST's density and common statistics. The detailed convolution calculation and fair-die projection-coordinate proof are explanatory derivations added here, not quotations or user-authored work. The proof uses the projection matrix directly, not the inverse-matrix formula printed in the Berkeley notes.
>
> New original visuals and reproducible checks: [[assets/figures/2026-11-10-chi-square/draw_tier2.py|tier-2 Python source]] and [[assets/figures/2026-11-10-chi-square/tier2-checks.json|check results]]. Numerical integration checks density mass and two moments for k=1,2,5,10,30 and three gamma convolutions; linear algebra checks the rank-five covariance, orthonormal basis and preserved squared length. Fair-die simulations use seed 20261110 and 150,000 repetitions at each n=6,60,600. They are illustrative Monte Carlo evidence, not exact multinomial calibration or proof. Both static figures were visually inspected; no live Obsidian rendering is claimed.

```atlas
```
