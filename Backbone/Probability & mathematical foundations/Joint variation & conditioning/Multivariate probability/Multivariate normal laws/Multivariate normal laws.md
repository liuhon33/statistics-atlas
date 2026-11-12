---
id: gaussian
title: Multivariate normal laws
layer: backbone
level: 4
subject: probability
study_band: U–M
backbone_path: Probability & mathematical foundations → Joint variation & conditioning → Multivariate probability → Multivariate normal laws
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/4
- study/undergraduate-masters
node_kind: group
parent: '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate probability]]'
prerequisite_for:
- '[[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Regression uncertainty]]'
applied_in:
- '[[Backbone/Statistical inference & modeling/Time series & forecasting/State-space & dynamic models/Latent dynamic states/Latent dynamic states]]'
sources:
- '[[_system/Sources/prob]]'
- '[[_system/Sources/bda]]'
---

# Multivariate normal laws

Probability & mathematical foundations → Joint variation & conditioning → Multivariate probability → Multivariate normal laws

Parent: [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate probability|Multivariate probability]]

## 1. See it and use it

Two measurements may each have a bell-shaped histogram yet still move together. A **multivariate normal (Gaussian) distribution** models their whole vector. Formally, $X\in\mathbb R^p$ is jointly Gaussian when every linear combination $a^TX$ is univariate normal, allowing a constant as a zero-variance case. Its mean vector $\mu$ gives the coordinate means, and its covariance matrix $\Sigma$ gives variances on the diagonal and covariances off the diagonal. We write $X\sim\mathcal N_p(\mu,\Sigma)$. [Johns Hopkins, *The Multivariate Normal Distribution*, §4, theorem 4.9, p. 13](https://biostat.jhsph.edu/~iruczins/teaching/140.752/notes/ch4.pdf).

![[assets/figures/2026-11-12-gp-ridge/mvn-contours.svg]]
*Original density contours for mean $(0,0)^T$, unit variances and correlation 0.8. The tilted shape shows positive association. Contour height is a density, not the probability of a point.*

Use the covariance to calculate uncertainty in a combined measurement. Here

$$
\operatorname{Var}(X_1+X_2)=1+1+2(0.8)=3.6.
$$

Therefore $X_1+X_2\sim\mathcal N(0,3.6)$. Ignoring their association would give the wrong variance, 2. Normal-looking separate histograms alone do not establish joint Gaussianity; the definition concerns every linear combination.

## 2. How it works: transform a sphere into an ellipse

Start with independent $Z_1,\ldots,Z_r\sim\mathcal N(0,1)$, put them in a vector $Z$, and choose a fixed $p\times r$ matrix $L$:

$$
X=\mu+LZ,\qquad
\mathbb E[X]=\mu,\qquad \operatorname{Cov}(X)=LL^T=\Sigma.
$$

Every $a^TX=a^T\mu+(L^Ta)^TZ$ is normal. Conversely, every Gaussian mean/covariance pair can be represented this way. $\Sigma$ must be symmetric positive semidefinite. It may be singular, in which case the distribution lies on a lower-dimensional affine subspace. A full $p$-dimensional density requires $\Sigma\succ0$. [Johns Hopkins §4, definitions 4.1–4.3 and theorem 4.4, p. 13](https://biostat.jhsph.edu/~iruczins/teaching/140.752/notes/ch4.pdf).

![[assets/figures/2026-11-12-gp-ridge/mvn-transform.svg]]
*Original linear transformation for $\Sigma=\begin{pmatrix}1&0.8\\0.8&1\end{pmatrix}$. The circle maps to a constant-Mahalanobis-distance ellipse. The coloured arrows are images of the unit basis vectors, of lengths $\sqrt{0.2}$ and $\sqrt{1.8}$.*

For $\Sigma\succ0$, the density is

$$
p(x)=\frac{\exp[-\tfrac12(x-\mu)^T\Sigma^{-1}(x-\mu)]}
{(2\pi)^{p/2}|\Sigma|^{1/2}}.
$$

The inverse covariance $\Sigma^{-1}$ measures squared distance relative to the distribution's own scale and orientation. Writing $\Sigma=Q\Lambda Q^T$ makes this explicit: rotate the centred vector by $Q^T$, divide coordinate $j$ by $\sqrt{\Lambda_{jj}}$, then sum its squared coordinates. The determinant factor accounts for the change in volume. [Rasmussen & Williams, Appendix A.2, equation (A.4)](https://gaussianprocess.org/gpml/chapters/RWA.pdf).

For any fixed $q\times p$ matrix $B$ and $c\in\mathbb R^q$,

$$
BX+c\sim\mathcal N_q(B\mu+c,B\Sigma B^T).
$$

Selecting coordinates is a special case: a marginal Gaussian simply keeps the corresponding mean entries and covariance submatrix. This is why a weight distribution can become a function-value distribution, $w\mapsto\Psi w$. The output can be singular when $B$ has too few independent rows.

## 3. Deeper connection: conditioning removes predictable variation

Observing one coordinate changes what we expect of another. In the unit-variance example,

$$
X_2\mid X_1=a\sim\mathcal N(0.8a,\ 1-0.8^2).
$$

At $a=1$, the mean is 0.8 and variance is 0.36. The unconditional marginal remains $X_2\sim\mathcal N(0,1)$.

![[assets/figures/2026-11-12-gp-ridge/mvn-conditioning.svg]]
*Original illustration. Fixing $X_1=1$ takes a vertical slice of the joint density; dividing by the marginal density of $X_1$ normalizes that slice. Integrating over all $X_1$ gives the different, dashed marginal density.*

For a jointly Gaussian partition $X=(U^T,V^T)^T$, with $U\in\mathbb R^p$, $V\in\mathbb R^q$ and positive-definite joint covariance,

$$
\begin{aligned}
\mathbb E[V\mid U=u]&=\mu_V+\Sigma_{VU}\Sigma_{UU}^{-1}(u-\mu_U),\\
\operatorname{Cov}(V\mid U=u)&=\Sigma_{VV}-\Sigma_{VU}\Sigma_{UU}^{-1}\Sigma_{UV}.
\end{aligned}
$$

One way to see the result is to form the residual

$$
R=V-\mu_V-\Sigma_{VU}\Sigma_{UU}^{-1}(U-\mu_U).
$$

Direct multiplication gives $\operatorname{Cov}(R,U)=0$. Since $(R,U)$ is jointly Gaussian, they are independent. The residual covariance is the subtracted matrix above; conditioning on $U$ fixes the predictable part and leaves $R$ unchanged. [Rasmussen & Williams, Appendix A.2, equation (A.6)](https://gaussianprocess.org/gpml/chapters/RWA.pdf).

This is the operation used in [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Local methods & kernels/Gaussian process regression|Gaussian-process regression]]: observed responses form $U$, and new function values form $V$. It is also what [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian conditioning|Gaussian conditioning]] computes by completing the joint density's quadratic expression. With fixed covariance parameters, the conditional covariance does not depend on the observed value $u$.

Your lecture-p. 30 annotation correctly highlights the independence shortcut, with the necessary qualification **jointly Gaussian**. Zero covariance alone is not enough for arbitrary random variables. For a jointly Gaussian pair with zero cross-covariance, the characteristic function factors into a function of each block, which proves independence even when a block is degenerate.

## Origin

> [!info]- Source details
> Enriched on 2026-11-12 at the user's request to support the supplied GP lecture. Levels 1–3 cover the relevant definition, linear transformations, and conditioning. The user's p. 30 annotations motivate the linear-combination characterization and joint-Gaussian independence qualification; the p. 35 slide supplies the conditional block formula. Preserved source: Thibault Randrianarisoa, Gaussian Processes, University of Toronto, 2026-03-09 (original course PDF retained privately); external theorem checks are cited beside the claims.
>
> Examples, proofs and figures are original checked synthesis. [[assets/figures/2026-11-12-gp-ridge/build_visuals.py|Reproducible code]] constructs the covariance ellipses and conditional density; [[assets/figures/2026-11-12-gp-ridge/checks.json|checks]] compare precision and covariance calculations. The original backbone identity, hierarchy and typed connections are preserved.

## Connections

- [[Backbone/Statistical inference & modeling/Regression & linear models/Linear regression/Regression uncertainty/Regression uncertainty|Regression uncertainty]] — Gaussian errors yield exact normal coefficient laws and independent residual quadratic forms.
- [[Backbone/Statistical inference & modeling/Time series & forecasting/State-space & dynamic models/Latent dynamic states/Latent dynamic states|Latent dynamic states]] — Linear Gaussian conditioning is the update behind the Kalman filter.

```atlas
```
