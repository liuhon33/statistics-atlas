---
id: learning-geometric-interpretation-t-statistic
title: Geometric interpretation of the t-statistic
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Student t, chi-square and F]]'
subject: probability
backbone_path: Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Student t, chi-square and F
study_band: U–M
note_types: [derivation, insight]
source_format: handwriting
created: '2026-11-09'
updated: '2026-11-09'
status: active
verification: checked
tags: [atlas/learning, subject/probability, topic/t-distribution]
connections:
  - '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Cauchy distribution]]'
  - '[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom]]'
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Hilbert spaces]]'
  - '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Chi-square quadratic forms]]'
  - '[[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation]]'
  - '[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests]]'
sources:
  - '[[raw/assets/2026-11-09-t-statistic-I01-geometric-derivation.png]]'
  - '[[assets/figures/2026-11-09-t-geometry/t-statistic-sphere-and-triangle.svg]]'
  - '[[assets/figures/2026-11-09-t-geometry/draw_t_geometry.py]]'
---

# Geometric interpretation of the t-statistic

Probability & mathematical foundations → Random variables & distributions → Useful distribution families → Continuous families → Student t, chi-square and F

**The one-sample t-statistic is a signed projection-to-residual ratio: $T=\sqrt{n-1}\cot\theta$.** The angle is measured from the positive mean direction to the centered-at-the-population-mean sample vector. Gaussian rotational invariance supplies the distribution; the right triangle supplies the ratio.

![[raw/assets/2026-11-09-t-statistic-I01-geometric-derivation.png]]

*My original handwritten derivation, preserved whole. The explanation below distinguishes a scalar coordinate from a projection vector, and a chi-square squared length from its square root. The two-dimensional drawing depicts a decomposition in $\mathbb R^n$.*

![[assets/figures/2026-11-09-t-geometry/t-statistic-sphere-and-triangle.svg]]

*Codex's enlarged vector redraw, requested after my original: blue is the mean projection $Au$, orange is the residual $r$, and red is the standardized sample vector $\mathbf z$. Left: a schematic sphere at radius $R=\|\mathbf z\|$, with the residual plane illustrated for $n=3$. Right: the exact planar triangle, shown for $A>0$; the sign rule below also covers obtuse angles. The Gaussian vector is not restricted to a fixed radius. Open the SVG to zoom without losing detail.*

## 1. Split the sample into one mean direction and n − 1 residual directions

Assume $X_1,\ldots,X_n\overset{\mathrm{iid}}\sim N(\mu,\sigma^2)$, with $n\ge2$ and $\sigma>0$. Let $\mathbf X=(X_1,\ldots,X_n)^\top$, $\mathbf1=(1,\ldots,1)^\top$, and

$$
\bar X=\frac1n\sum_iX_i,\qquad S^2=\frac1{n-1}\sum_i(X_i-\bar X)^2.
$$

Standardize the whole vector and choose a **unit** mean direction:

$$
\mathbf z=\frac{\mathbf X-\mu\mathbf1}{\sigma}\sim N_n(0,I_n),\qquad
u=\frac{\mathbf1}{\sqrt n},\qquad P=uu^\top.
$$

Write

$$
\mathbf z=Au+r,\qquad
A=u^\top\mathbf z=\frac{\sqrt n(\bar X-\mu)}{\sigma},\qquad
r=(I_n-P)\mathbf z=\frac{\mathbf X-\bar X\mathbf1}{\sigma}.
$$

Thus $P\mathbf z=Au$, $u^\top r=0$, and $\|\mathbf z\|^2=A^2+\|r\|^2$. The signed coordinate $A$ can be negative; the projection length $\|P\mathbf z\|=|A|$ cannot.

The residual constraint $\sum_i r_i=0$ leaves an $(n-1)$-dimensional subspace. This is the geometric meaning of the residual degrees of freedom $\nu=n-1$, not a count of independent entries of $r$ in the original coordinate system.

## 2. Orthogonality is geometry; independence uses the Gaussian law

Complete $u$ to a fixed orthonormal basis $u,v_2,\ldots,v_n$. In that basis,

$$
(A,B_2,\ldots,B_n)\sim N_n(0,I_n),\qquad B_j=v_j^\top\mathbf z.
$$

These coordinates are independent standard normals: an orthogonal transformation preserves the standard multivariate normal density, which factors into its coordinate densities. Therefore

$$
Q:=\|r\|^2=\sum_{j=2}^nB_j^2
=\frac{(n-1)S^2}{\sigma^2}\sim\chi^2_{n-1},\qquad A\perp Q.
$$

This proves $\bar X\perp S^2$. The implication is **not** “perpendicular vectors are always independent.” Here the linear projections are jointly Gaussian and have zero cross-covariance. Without Gaussianity, the projection identity survives but this independence and chi-square argument need not.

The three sums of squares in my page are:

| Quantity | Dimension | Distribution |
| --- | --- | --- |
| $\|\mathbf X-\mu\mathbf1\|^2$ | $n$ | $\sigma^2\chi_n^2$ |
| $\|P(\mathbf X-\mu\mathbf1)\|^2=n(\bar X-\mu)^2$ | $1$ | $\sigma^2\chi_1^2$ |
| $\|(I_n-P)\mathbf X\|^2=(n-1)S^2$ | $n-1$ | $\sigma^2\chi_{n-1}^2$ |

The last two are independent and sum to the first. These sampling laws agree with Richard Lockhart's [STAT 801, *Normal samples: Distribution Theory*](https://www.sfu.ca/~lockhart/richard/801/01_1/lectures/normal_samples/web.html), opening theorem and t-ratio definition.

## 3. The t ratio is a cotangent

With $\nu=n-1$,

$$
T=\frac{\sqrt n(\bar X-\mu)}{S}
=\frac{A}{\sqrt{Q/\nu}}
=\sqrt\nu\frac{A}{\|r\|}\sim t_\nu.
$$

**Scaling correction:** if $Q\sim\chi^2_\nu$, the t denominator is $\sqrt{Q/\nu}$, not $\sqrt Q$. Also, $Q=\|r\|^2$ is chi-square; $\|r\|=\sqrt Q$ has the chi distribution.

Let $\theta\in(0,\pi)$ be the angle between $\mathbf z$ and the fixed **positive** direction $u$. Almost surely $\|r\|>0$, and

$$
A=\|\mathbf z\|\cos\theta,\qquad
\|r\|=\|\mathbf z\|\sin\theta,
\qquad\boxed{T=\sqrt\nu\cot\theta.}
$$

An acute angle gives $T>0$; an obtuse angle gives $T<0$; a right angle gives $T=0$. Large $|T|$ means near alignment with either $+u$ or $-u$. Using the acute angle to the unoriented line instead would yield only $|T|$. The endpoints have zero probability under the model and correspond to zero residual length.

The corresponding rejection region is the [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests#Why the planes become cones|t-test double cone]].

For a test of $\mu=\mu_0$, construct the vector using $\mu_0$; the central $t_\nu$ law holds under that null. Under an alternative, the numerator has a nonzero mean and the statistic is noncentral t.

The density recalled on my page is

$$
f_T(t)=\frac{\Gamma((\nu+1)/2)}{\sqrt{\nu\pi}\,\Gamma(\nu/2)}
\left(1+\frac{t^2}{\nu}\right)^{-(\nu+1)/2},\qquad t\in\mathbb R,
$$

where $\Gamma$ is the gamma function. This is the same Student family defined by the independent normal/chi-square ratio above; see [NIST §1.3.6.6.4](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm).

## 4. Why Cauchy is the two-dimensional case

**Added connection.** For $n=2$, there is one residual coordinate $B\sim N(0,1)$ independent of $A$. Then

$$
Q=B^2,\qquad T=\frac{A}{|B|}=\cot\theta\sim t_1=\operatorname{Cauchy}(0,1).
$$

The isotropic Gaussian direction is uniform on the circle; folding the residual sign makes $\theta$ uniform on $(0,\pi)$. Since $t=\cot\theta$ and $|d\theta/dt|=1/(1+t^2)$, its density is $1/[\pi(1+t^2)]$.

The familiar ratio $A/B$ has the same distribution as $A/|B|$ by symmetry and independence, but they are not the same random variable. In higher dimensions the polar angle is **not uniform**: for $\mathbf z\in\mathbb R^{\nu+1}$ its density is proportional to $\sin^{\nu-1}\theta$. Thus “cotangent of a uniform angle” describes Cauchy, not every t distribution.

## 5. The same triangle in least squares and Hilbert spaces

**Added comparison to my [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation#My drawing connects the same projection to t and F|earlier regression drawing]].** For simple regression with an intercept, nonconstant predictor, $n>2$ and positive residual sum of squares, let $\phi$ be the angle between the centered predictor and response vectors. The zero-slope statistic satisfies

$$
t=r_{xy}\sqrt{\frac{n-2}{1-r_{xy}^2}}=\sqrt{n-2}\cot\phi.
$$

The mean problem removes one fitted direction, leaving $n-1$ residual degrees of freedom. Simple regression removes the intercept and slope directions, leaving $n-2$. Both use a signed coordinate divided by residual length per square root of residual dimension. Exact central t inference in regression additionally needs the Gaussian homoskedastic model and the zero-slope null; the triangle alone gives an algebraic identity.

The current drawing lives in the finite-dimensional Hilbert space $\mathbb R^n$, with inner product $a^\top b$. In the population $L^2$ picture, the vectors are entire random variables and the inner product is $\mathbb E[UV]$. Both have orthogonal projections and Pythagoras, but $\bar X$ as an observation-space projection is not the same operation as projecting a random variable onto constants to obtain its expectation. In neither space does orthogonality alone establish independence.

## Connections

- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Continuous families/Cauchy distribution|Cauchy distribution]] — One residual dimension gives $t_1$, and the cotangent of the uniform planar angle has the standard Cauchy density.
- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Residual variance and degrees of freedom|Residual variance and degrees of freedom]] — Residual subspace dimension explains both the $n-1$ normalization here and the $n-2$ normalization for a simple-regression slope.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Hilbert spaces|Hilbert spaces]] — The Euclidean sample-vector decomposition and the population L2 projection viewpoint share inner-product geometry but have different vectors and inner products.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Chi-square quadratic forms|Chi-square quadratic forms]] — $Q=\mathbf z^\top(I_n-P)\mathbf z$ is a Gaussian squared projection with rank $n-1$, supplying the t denominator $\sqrt{Q/(n-1)}$.
- [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|Three routes from least squares to slope and correlation]] — My earlier projection drawing produces the same signed cotangent statistic, with regression's $n-2$ residual degrees of freedom instead of $n-1$.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests|Geometric interpretation of z, t, and F tests]] — Turns the signed cotangent statistic into a double-cone decision region and compares it with the fixed z-test slab.

## Origin

> [!info]- Source details
> Based on my single supplied handwritten page and my request to connect it to Cauchy, degrees of freedom, Hilbert spaces, chi-square and my least-squares note. The original is embedded unchanged; the filename records receipt on 2026-11-09, not an inferred authorship date. Codex supplied the explicit notation, sign/scaling qualifications, Cauchy explanation, Hilbert-space distinction and regression comparison. No new question is attributed to me. The derivation was checked algebraically, with supporting numerical identity checks; the external references check the distributional definitions and normal-sample theorem, not the provenance of my work.
>
> The large sphere-and-triangle SVG is a new Codex-authored illustration requested on 2026-11-09, not an alteration of my handwriting. Its reproducible Python source is stored beside the SVG; the perspective sphere and exact triangle use the same angle and side-length ratio.
