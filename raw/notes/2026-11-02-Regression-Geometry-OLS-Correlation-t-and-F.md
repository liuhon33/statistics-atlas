---
title: "Regression geometry: OLS, correlation, t, F, and confidence intervals"
created: 2026-11-01
tags:
  - statistics
  - linear-regression
  - linear-algebra
  - hypothesis-testing
  - geometry
aliases:
  - OLS geometry and cotangent t-test
---

# Regression geometry — from vector derivatives to correlation, $t$, $F$, and confidence intervals

> [!abstract] Scope
> Notes from the conversation beginning around **11:45 p.m.**, when we asked how the slope standard error relates to $\hat\beta_1=r_{XY}s_Y/s_X$, through the vector-calculus derivation and my hand-drawn rejection-region diagram. The final sections connect this to the earlier discussions of confidence intervals, the squared-Cauchy $F$ distribution, and orthogonality.

## 0. One-page map of the ideas

For **simple OLS regression with an intercept**, with $n>2$, nonconstant $x$ and $y$, and nonzero residual variation:

$$
\boxed{\hat\beta_1=\frac{\mathbf x_c^\top\mathbf y_c}{\|\mathbf x_c\|^2}
=r_{XY}\frac{s_Y}{s_X}}
$$

$$
\boxed{\widehat{\mathrm{SE}}(\hat\beta_1)
=\frac{\hat\sigma}{\|\mathbf x_c\|}
=\frac{s_Y}{s_X}\sqrt{\frac{1-r_{XY}^2}{n-2}}}
$$

$$
\boxed{t=\frac{\hat\beta_1}{\widehat{\mathrm{SE}}(\hat\beta_1)}
=r_{XY}\sqrt{\frac{n-2}{1-r_{XY}^2}}
=\sqrt{n-2}\,\cot\theta}
$$

$$
\boxed{F=t^2=(n-2)\cot^2\theta}
$$

Here $\theta\in(0,\pi)$ is the **angle between $\mathbf x_c$ and $\mathbf y_c$**, retaining the sign of the slope. The last two identities are algebraic identities; using Student's $t$ or $F$ *distributions* for inference additionally requires the usual regression-error assumptions.

**Logic:** minimize squared distance $\to$ gradient $=0$ $\to$ orthogonal residual $\to$ projection slope $\to$ correlation $\to$ $R^2$ $\to$ $t$ and $F$ $\to$ rejection region and confidence interval.

---

## 1. Notation: data as vectors

Let

$$
\mathbf x=(x_1,\ldots,x_n)^\top,\qquad
\mathbf y=(y_1,\ldots,y_n)^\top,\qquad
\mathbf1=(1,\ldots,1)^\top.
$$

The model is

$$
\mathbf y=\beta_0\mathbf1+\beta_1\mathbf x+\boldsymbol\varepsilon.
$$

Define the centering matrix and centered vectors:

$$
H=I-\frac1n\mathbf1\mathbf1^\top,\quad
\mathbf x_c=H\mathbf x=\mathbf x-\bar x\mathbf1,\quad
\mathbf y_c=H\mathbf y=\mathbf y-\bar y\mathbf1.
$$

Properties: $H^\top=H$, $H^2=H$, $H\mathbf1=0$; thus $\mathbf1^\top\mathbf x_c=\mathbf1^\top\mathbf y_c=0$.

Define

$$
S_{xx}=\|\mathbf x_c\|^2,\qquad
S_{yy}=\|\mathbf y_c\|^2,\qquad
S_{xy}=\mathbf x_c^\top\mathbf y_c.
$$

Sample standard deviations and Pearson correlation are

$$
s_X=\sqrt{\frac{S_{xx}}{n-1}},\qquad
s_Y=\sqrt{\frac{S_{yy}}{n-1}},\qquad
r_{XY}=\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}.
$$

> [!important] Observation space, not a conventional scatterplot
> For $n$ observations, $\mathbf x$ and $\mathbf y$ live in $\mathbb R^n$; the coordinate axes correspond to **observations** (not to education vs. income axes, nor necessarily to categories). Regression is projection onto a subspace of this $n$-dimensional space.

## 2. Derive OLS by vector derivatives and setting them to zero

The OLS loss is

$$
L(\beta_0,\beta_1)=\|\mathbf y-\beta_0\mathbf1-\beta_1\mathbf x\|^2.
$$

Expand the inner product:

$$
\begin{aligned}
L={}&\mathbf y^\top\mathbf y-2\beta_0\mathbf1^\top\mathbf y-2\beta_1\mathbf x^\top\mathbf y\\
&+n\beta_0^2+2\beta_0\beta_1\mathbf1^\top\mathbf x+\beta_1^2\mathbf x^\top\mathbf x.
\end{aligned}
$$

**Derivative with respect to the intercept:**

$$
\frac{\partial L}{\partial\beta_0}=-2\mathbf1^\top\mathbf y+2n\beta_0+2\beta_1\mathbf1^\top\mathbf x=0.
$$

Thus

$$
\boxed{\hat\beta_0=\bar y-\hat\beta_1\bar x}.
$$

**Derivative with respect to the slope:**

$$
\frac{\partial L}{\partial\beta_1}=-2\mathbf x^\top\mathbf y+2\beta_0\mathbf x^\top\mathbf1+2\beta_1\mathbf x^\top\mathbf x=0.
$$

Insert $\hat\beta_0=\bar y-\hat\beta_1\bar x$ and $\mathbf x^\top\mathbf1=n\bar x$:

$$
\hat\beta_1=\frac{\mathbf x^\top\mathbf y-n\bar x\bar y}{\mathbf x^\top\mathbf x-n\bar x^2}.
$$

Recognize the centered products:

$$
\mathbf x_c^\top\mathbf y_c=\mathbf x^\top\mathbf y-n\bar x\bar y,
\quad
\mathbf x_c^\top\mathbf x_c=\mathbf x^\top\mathbf x-n\bar x^2.
$$

So

$$
\boxed{\hat\beta_1=\frac{\mathbf x_c^\top\mathbf y_c}{\mathbf x_c^\top\mathbf x_c}}.
$$

### An even shorter derivative after removing the intercept

For a candidate slope $b$, minimize

$$
L(b)=\|\mathbf y_c-b\mathbf x_c\|^2
=\|\mathbf y_c\|^2-2b\mathbf x_c^\top\mathbf y_c+b^2\|\mathbf x_c\|^2.
$$

Then

$$
\frac{dL}{db}=-2\mathbf x_c^\top\mathbf y_c+2b\|\mathbf x_c\|^2=0
\quad\Longrightarrow\quad
\boxed{\hat\beta_1=\frac{\mathbf x_c^\top\mathbf y_c}{\|\mathbf x_c\|^2}}.
$$

Since $d^2L/db^2=2\|\mathbf x_c\|^2>0$ (provided $\mathbf x_c\ne0$), the minimizer is unique.

**Geometric meaning of the derivative:** rearrange the first-order condition as

$$
\boxed{\mathbf x_c^\top(\mathbf y_c-\hat\beta_1\mathbf x_c)=0}.
$$

The residual $\mathbf e=\mathbf y_c-\hat\beta_1\mathbf x_c$ is orthogonal to the predictor direction. **Calculus and orthogonal projection express the same fact.**

### Multiple regression generalization

Using $Z$ for the full design matrix (to avoid confusing it with the predictor vector $\mathbf x$):

$$
L(\boldsymbol\beta)=\|\mathbf y-Z\boldsymbol\beta\|^2,
\qquad \nabla_\beta L=-2Z^\top(\mathbf y-Z\boldsymbol\beta).
$$

Setting the gradient to zero gives the normal equations

$$
Z^\top Z\hat{\boldsymbol\beta}=Z^\top\mathbf y,
\qquad
\boxed{\hat{\boldsymbol\beta}=(Z^\top Z)^{-1}Z^\top\mathbf y}
$$

if $Z$ has full column rank. Consequently $Z^\top\mathbf e=0$: residuals are orthogonal to **every** design-matrix column.

## 3. Prove slope = correlation × ratio of standard deviations

By definition,

$$
r_{XY}=\frac{\mathbf x_c^\top\mathbf y_c}{\|\mathbf x_c\|\|\mathbf y_c\|}.
$$

Insert $\mathbf x_c^\top\mathbf y_c=r_{XY}\|\mathbf x_c\|\|\mathbf y_c\|$ into the OLS slope:

$$
\begin{aligned}
\hat\beta_1&=\frac{r_{XY}\|\mathbf x_c\|\|\mathbf y_c\|}{\|\mathbf x_c\|^2}\\
&=r_{XY}\frac{\|\mathbf y_c\|}{\|\mathbf x_c\|}\\
&=\boxed{r_{XY}\frac{s_Y}{s_X}}.
\end{aligned}
$$

The last equality works because the $\sqrt{n-1}$ factors cancel. If both variables are standardized, $s_X=s_Y=1$, hence $\hat\beta_1=r_{XY}$.

For the angle $\theta$ between the centered vectors,

$$
\cos\theta=\frac{\mathbf x_c^\top\mathbf y_c}{\|\mathbf x_c\|\|\mathbf y_c\|}=r_{XY}.
$$

So slope also equals $\cos\theta\,s_Y/s_X$: correlation is **orientation**, while $s_Y/s_X$ is **scale**.

## 4. The regression right triangle and explained vs. unexplained variation

The centered fitted vector and residual are

$$
\hat{\mathbf y}_c=\hat\beta_1\mathbf x_c,
\qquad\mathbf e=\mathbf y_c-\hat{\mathbf y}_c,
\qquad\hat{\mathbf y}_c\perp\mathbf e.
$$

Hence $\mathbf y_c=\hat{\mathbf y}_c+\mathbf e$ is a right triangle, yielding

$$
\underbrace{\|\mathbf y_c\|^2}_{\mathrm{TSS}}
=\underbrace{\|\hat{\mathbf y}_c\|^2}_{\mathrm{ESS}}
+\underbrace{\|\mathbf e\|^2}_{\mathrm{RSS}}.
$$

Therefore

$$
R^2=\frac{\mathrm{ESS}}{\mathrm{TSS}}=r_{XY}^2=\cos^2\theta,
\qquad
\mathrm{RSS}=(1-r_{XY}^2)S_{yy}.
$$

**Two angles must be distinguished:**

1. $\theta=\angle(\mathbf x_c,\mathbf y_c)\in[0,\pi]$; $\cos\theta=r$ may be negative.
2. $\phi=\angle(\hat{\mathbf y}_c,\mathbf y_c)\in[0,\pi/2]$ (if the fitted vector is nonzero); $\cos\phi=|r|$.

The right triangle's adjacent/opposite side ratio is

$$
\cot\phi=\frac{\|\hat{\mathbf y}_c\|}{\|\mathbf e\|}
=\sqrt{\frac{\mathrm{ESS}}{\mathrm{RSS}}}
=|\cot\theta|.
$$

Using $\theta$ instead of $\phi$ retains the **sign** of the slope.

## 5. Your handwritten diagram: the significance cone / rejection region

![[assets/my_handdrawn_regression_geometry.png]]

[Open original diagram](assets/my_handdrawn_regression_geometry.png)

**What the drawing captures:**

- The black vectors and colored planes convey a projection in observation space.
- The dark green wedge labeled **“fail to reject”** corresponds to directions where $\mathbf y_c$ is not sufficiently aligned with $\pm\mathbf x_c$ for a significant slope.
- The red **“reject”** regions correspond to an outcome vector sufficiently close in angle to the positive or negative predictor direction.
- Your handwritten $\cot\theta=b/a$ can be made precise as the **fitted length / residual length**, with the sign convention noted above.

**Formal rule** for a two-sided slope test at level $\alpha$:

$$
\boxed{\text{Reject }H_0:\beta_1=0
\iff |\cot\theta|>\frac{t_{1-\alpha/2,n-2}}{\sqrt{n-2}}.}
$$

For a positive correlation, $\theta$ close to $0^\circ$ gives a large positive $t$; for a negative correlation, $\theta$ close to $180^\circ$ gives a large negative $t$. At $90^\circ$, $r=t=0$. The sketch is conceptual: the actual critical angular boundary depends on sample size $n$ and significance level $\alpha$.

## 6. Derive standard error, $t$, and $F$ from the geometry

For an intercept-and-one-predictor regression, define

$$
\hat\sigma^2=\frac{\mathrm{RSS}}{n-2}.
$$

The usual OLS estimated slope standard error is

$$
\widehat{\mathrm{SE}}(\hat\beta_1)=\frac{\hat\sigma}{\sqrt{S_{xx}}}.
$$

Use $\mathrm{RSS}=(1-r^2)S_{yy}$:

$$
\begin{aligned}
\widehat{\mathrm{SE}}(\hat\beta_1)
&=\sqrt{\frac{(1-r^2)S_{yy}}{(n-2)S_{xx}}}\\
&=\boxed{\frac{s_Y}{s_X}\sqrt{\frac{1-r^2}{n-2}}}.
\end{aligned}
$$

Combine with $\hat\beta_1=r\,s_Y/s_X$:

$$
\begin{aligned}
t&=\frac{\hat\beta_1}{\widehat{\mathrm{SE}}(\hat\beta_1)}\\
&=\boxed{r\sqrt{\frac{n-2}{1-r^2}}}\\
&=\boxed{\sqrt{n-2}\,\cot\theta}.
\end{aligned}
$$

The last step uses $r=\cos\theta$ and $\sqrt{1-r^2}=\sin\theta$ for $\theta\in(0,\pi)$.

Squaring gives

$$
\boxed{F=t^2=(n-2)\cot^2\theta
=\frac{\mathrm{ESS}/1}{\mathrm{RSS}/(n-2)}}.
$$

This is the ordinary overall $F$-statistic for **simple regression with an intercept**. For multiple predictors the global $F$-test and an individual coefficient's $t$-test are generally different.

**Inference assumptions:** under $H_0:\beta_1=0$ with fixed, nonconstant $x$ and independent homoskedastic Gaussian errors, $t\sim t_{n-2}$ and $F\sim F_{1,n-2}$. The algebraic identities do not need Gaussian errors, but these exact reference distributions do.

> [!note] Why we cannot derive the signed slope from the SE alone
> Standard error measures uncertainty and does not retain the sign of the slope. We first derive $\hat\beta_1$ from least squares; only afterward combine it with SE to get $t$.

## 7. Confidence intervals are inverted geometric tests

For a **two-sided** test, the ordinary 95% confidence interval for the slope is

$$
\boxed{\hat\beta_1\pm t_{0.975,n-2}\widehat{\mathrm{SE}}(\hat\beta_1)}.
$$

A p-value of **exactly $0.05$** when testing $H_0:\beta_1=0$ corresponds to zero lying on one boundary of this 95% interval (with no rounding error).

The other, equally valid, mental picture from our earlier discussion is to **center an acceptance region on the null value** and see whether $\hat\beta_1$ lands outside. That null-centered region is not conventionally called a CI; the CI is centered on the observed $\hat\beta_1$.

### F-test inversion derived directly from distances

To test *any* candidate slope $b$, constrain the regression to $\beta_1=b$ and re-optimize the intercept. Let $C$ denote the full fitted vector and $D_b$ the constrained fitted vector. Then

$$
C=\bar y\mathbf1+\hat\beta_1\mathbf x_c,\qquad
D_b=\bar y\mathbf1+b\mathbf x_c.
$$

So

$$
\|C-D_b\|^2=(\hat\beta_1-b)^2S_{xx}.
$$

The one-restriction statistic is

$$
\boxed{F(b)=\frac{(\hat\beta_1-b)^2S_{xx}}{\mathrm{RSS}/(n-2)}}.
$$

The **95% confidence interval** consists of all $b$ for which

$$
F(b)\le F_{1,n-2;0.95}.
$$

Solving yields

$$
\boxed{\hat\beta_1\pm\sqrt{F_{1,n-2;0.95}}\frac{\hat\sigma}{\sqrt{S_{xx}}}}
=\boxed{\hat\beta_1\pm t_{0.975,n-2}\widehat{\mathrm{SE}}(\hat\beta_1)}.
$$

**Interpretation:** the confidence interval is the set of all proposed slopes whose restricted fitted lines are not *too far* from the unconstrained fit, relative to residual noise.

### Why the video showed a squared Cauchy distribution

With **three observations** and two regression coefficients, the residual degrees of freedom are $n-2=1$. Thus

$$
t\sim t_1=\mathrm{Cauchy}(0,1),\qquad F=t^2\sim F_{1,1}.
$$

For $f\ge0$,

$$
P(F\le f)=\frac2\pi\arctan\sqrt f.
$$

Its 95th percentile is

$$
F_{1,1;0.95}=\tan^2(0.475\pi)\approx161.45,
\qquad \sqrt{F_{1,1;0.95}}\approx12.706.
$$

That's why a 95% slope interval with only three observations is generally much wider than a normal approximation would suggest. **Cauchy only appears here because the residual degrees of freedom equal one**, not because ordinary regression coefficients always follow a Cauchy distribution.

## 8. Related Hilbert-space distinction: orthogonality ≠ always zero covariance

In the random-variable Hilbert space $L^2$ with inner product $\langle U,V\rangle=E[UV]$,

$$
U\perp V\iff E[UV]=0.
$$

But

$$
\operatorname{Cov}(U,V)=E[UV]-E[U]E[V].
$$

Therefore orthogonality of **uncentered** random variables need not imply zero covariance. Centering fixes this:

$$
\boxed{\langle U-EU,V-EV\rangle=\operatorname{Cov}(U,V)}.
$$

This should not be confused with OLS projection orthogonality, $\hat{\mathbf y}^\top\mathbf e=0$, in the Euclidean observation space $\mathbb R^n$. With an intercept, $\mathbf1^\top\mathbf e=0$, so fitted values and residuals have zero **sample** covariance. Neither fact alone implies independence. For jointly Gaussian random components, however, zero covariance implies independence, which is useful in the classical proof of the $F$ distribution.

## 9. Common mistakes to avoid

- $\hat\beta_1$ (estimated slope) is **not** $\widehat{\mathrm{SE}}(\hat\beta_1)$ (uncertainty in that slope).
- $r=\cos\theta$ requires **centered vectors** in simple regression with an intercept.
- $R^2=r^2$ and $F=t^2$ in the forms above are specific to **simple regression with an intercept** (and the corresponding single-parameter test).
- The acute right-triangle angle $\phi$ yields $|t|$; to retain the signed $t$, use $\theta=\angle(\mathbf x_c,\mathbf y_c)$.
- A $p$-value is **not** the probability that $\beta_1\ne0$; it is a tail probability computed under a specified null.
- A 95% frequentist CI is a procedure with 95% long-run coverage, not a posterior 95% probability for the fixed coefficient.
- Exact $t$ and $F$ reference distributions use assumptions about the regression errors; these are not guaranteed by the projection geometry alone.

## 10. Recall questions (for future Obsidian review)

1. Why does the derivative of the OLS loss imply $\mathbf x_c^\top\mathbf e=0$?
2. Derive $\hat\beta_1=r\,s_Y/s_X$ without ever writing a scalar summation.
3. Why can a negative correlation produce a very large *negative* $t$ even though the right-triangle ratio of lengths is nonnegative?
4. How can the Pythagorean theorem yield $R^2=r^2$?
5. If $n$ increases while the observed correlation stays fixed, what happens to $|t|$?
6. How would you obtain a confidence interval by moving the null-hypothesis line $D_b$ instead of centering an interval at $\hat\beta_1$?
7. What is special about $n=3$ that makes the Cauchy distribution appear in the video?

---

**Summary in one line:** *OLS calculus forces orthogonality; orthogonality gives a projection triangle; its angle determines correlation, fit, $t$, and $F$; and inverting those tests gives a confidence interval.*
