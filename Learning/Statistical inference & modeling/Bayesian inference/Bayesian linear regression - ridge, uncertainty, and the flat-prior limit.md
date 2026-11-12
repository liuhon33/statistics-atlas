---
id: learning-bayesian-regression-ridge-flat-prior
title: Bayesian linear regression - ridge, uncertainty, and the flat-prior limit
layer: learning
primary_home: '[[Backbone/Statistical inference & modeling/Bayesian inference/Bayesian inference foundations/Prior, likelihood & posterior/Conjugate updating]]'
subject: statistics
backbone_path: Statistical inference & modeling → Bayesian inference → Bayesian inference foundations → Prior, likelihood & posterior → Conjugate updating
study_band: U–M
note_types: [derivation, insight, question]
question_roles: [cross-topic-connection, reconcile-approaches, assumption-boundary]
source_format: annotated-lecture-pdf
created: '2026-11-12'
updated: 2026-11-12
status: active
verification: checked
learning_state: unknown
tags: [atlas/learning, subject/statistics]
connections:
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression]]'
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso]]'
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net]]'
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization]]'
- '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws]]'
sources:
- '[[raw/assets/private-course-slides/2026-03-09-Lec09-I01-p14-ridge.png]]'
---

# Bayesian linear regression - ridge, uncertainty, and the flat-prior limit

Statistical inference & modeling → Bayesian inference → Bayesian inference foundations → Prior, likelihood & posterior → Conjugate updating

Your connection is exact for a Gaussian likelihood and a zero-centred isotropic Gaussian prior: **the posterior mean and MAP coefficient equal the ridge solution**. Increasing the prior standard deviation weakens the penalty. With a full-rank feature matrix, the mean approaches ordinary least squares (OLS).

The Bayesian calculation also returns a covariance and a predictive distribution. These do not disappear when the point estimates coincide.

## Watch the prior widen

```atlas-interactive
path: assets/figures/2026-11-12-gp-ridge/explorer.html
title: Prior width, ridge shrinkage, and the least-squares limit
height: 1350
```

[[assets/figures/2026-11-12-gp-ridge/explorer.html|Open the standalone explorer]]

Try **Strong prior → τ = 1 → Weak prior → OLS limit**. Predict what happens to the estimate and its uncertainty before moving the slider. The observations, feature map, noise and axes stay fixed. The prior applies to both intercept and slope.

> [!example]- Animation and inspectable endpoints
> ![[assets/figures/2026-11-12-gp-ridge/ridge-prior-to-ols.gif]]
> *Original analytic illustration: widen the prior, weaken ridge shrinkage, then hold the flat-prior endpoint. Teal is the posterior; gray dashed is the OLS/flat-prior reference; gold is the prior slope density. The band is pointwise latent-function mean ± 2 posterior SD. The final state has no normalized prior density.*
>
> ![[assets/figures/2026-11-12-gp-ridge/ridge-strong.svg]]
> ![[assets/figures/2026-11-12-gp-ridge/ridge-limit.svg]]

## 1. The model and the dimensions in your handwriting

For fixed inputs $x_i\in\mathbb R^D$, let $\psi(x_i)\in\mathbb R^M$ be a chosen feature vector. Stack its transpose into row $i$ of $\Psi\in\mathbb R^{N\times M}$. The coefficients are $w\in\mathbb R^M$, and the responses are $y\in\mathbb R^N$:

$$
y=\Psi w+\epsilon,\qquad
\epsilon\sim\mathcal N(0,\sigma^2 I_N),\qquad
w\sim\mathcal N(m_0,S),\quad S\succ0,\ \sigma^2>0.
$$

The prior and observation noise are independent; $S$ and $\sigma^2$ are treated as known. Your p. 6 annotations identify exactly why the product works: $(N\times M)(M\times1)=N\times1$. A nonlinear feature map still gives a model **linear in the coefficients**.

Your p. 8 note connects least squares to maximum likelihood. Independent Gaussian errors give

$$
\log p(y\mid w,\Psi)
=C-\frac{1}{2\sigma^2}\|y-\Psi w\|_2^2.
$$

For fixed positive $\sigma^2$, maximizing this likelihood over $w$ minimizes the residual sum of squares.

## 2. How the prior becomes an L2 penalty

Take $m_0=0$ and $S=\tau^2I_M$, where $\tau$ is a coefficient's **prior standard deviation**. Bayes' rule gives

$$
\begin{aligned}
\log p(w\mid y,\Psi)
&=\log p(y\mid w,\Psi)+\log p(w)+C\\
&=-\frac{\|y-\Psi w\|_2^2}{2\sigma^2}
-\frac{\|w\|_2^2}{2\tau^2}+C.
\end{aligned}
$$

Multiply the negative log posterior by $\sigma^2$, a positive constant independent of $w$:

$$
\hat w_{\mathrm{MAP}}
=\arg\min_w\left\{\frac12\|y-\Psi w\|_2^2+\frac\lambda2\|w\|_2^2\right\},
\qquad \boxed{\lambda=\frac{\sigma^2}{\tau^2}}.
$$

This is ridge's objective on lecture p. 7. Thus

$$
\boxed{\hat w_{\mathrm{ridge}}=(\Psi^T\Psi+\lambda I_M)^{-1}\Psi^Ty.}
$$

The scale matters: if the loss is $\|y-\Psi w\|^2/(2N)+\lambda\|w\|^2/2$, the matching penalty is $\lambda=\sigma^2/(N\tau^2)$. The slides use $\eta$ for the prior **variance** on p. 9, so $\eta=\tau^2$, not $\tau$.

In the unscaled negative log posterior, a general Gaussian prior contributes $(w-m_0)^TS^{-1}(w-m_0)/2$; multiply this by $\sigma^2$ when using the half-SSE convention above. It can prefer a nonzero centre and shrink directions differently. To match a ridge implementation that leaves the intercept unpenalized, give that intercept zero prior precision too; the explorer deliberately penalizes both coefficients.

> [!note] Compare L2, L1, and both
> The coefficient size here is the **squared** Euclidean norm, not the norm itself; see [[Learning/Probability & mathematical foundations/Mathematical tools/Vector norms - unit balls, convexity, and the zero-count exception#1. The rules and every size measure in this segment|the norm definitions]]. Replacing the Gaussian prior by independent Laplace priors gives [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso#2. How it works — a corner, a threshold, and a Laplace prior|lasso's L1 penalty]] at the MAP, generally not at the posterior mean. Multiplying the Gaussian and Laplace prior factors gives [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net#2. How it works — both penalties, one objective|elastic net]], not a mixture of priors. These are three concrete forms of [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|regularization]]. The linked pages use the same half-SSE convention as this derivation.

### Your gradient-descent calculation

Your blue derivation on p. 7 expands the gradient step into shrinkage plus a data-fit update:

$$
\begin{aligned}
w_{\mathrm{new}}
&=w-a\{(\Psi^T\Psi+\lambda I)w-\Psi^Ty\}\\
&=(1-a\lambda)w-a\Psi^T(\Psi w-y).
\end{aligned}
$$

Here $a>0$ is the step size. The first handwritten gradient line has an extra inverse; the subsequent expansion uses the correct gradient above. The inverse belongs in the optimum, not the gradient. For convergence of this fixed-step quadratic iteration, $0<a<2/\lambda_{\max}(\Psi^T\Psi+\lambda I)$.

## 3. Complete the square to get the whole posterior

The recurring Gaussian identity is, for a symmetric positive-definite matrix $A$ and vector $b$,

$$
\begin{aligned}
w^TAw-2b^Tw
&=(w-A^{-1}b)^TA(w-A^{-1}b)-b^TA^{-1}b,\\
\exp\{-\tfrac12 w^TAw+b^Tw\}
&\propto\mathcal N(w;A^{-1}b,A^{-1}).
\end{aligned}
$$

The matrix $A$ is the **precision**, the inverse covariance. The linear coefficient is precision times mean. Expanding the likelihood and prior gives

$$
A=\sigma^{-2}\Psi^T\Psi+S^{-1},\qquad
b=\sigma^{-2}\Psi^Ty+S^{-1}m_0.
$$

Therefore

$$
\boxed{w\mid y,\Psi\sim\mathcal N(\mu,V),\qquad V=A^{-1},\quad\mu=Vb.}
$$

For the lecture's zero-mean prior,

$$
\mu=(\Psi^T\Psi+\sigma^2S^{-1})^{-1}\Psi^Ty,
\qquad
V=\sigma^2(\Psi^T\Psi+\sigma^2S^{-1})^{-1}.
$$

Your red matching of the quadratic and linear terms on pp. 13–14 is the key step. Written consistently as column vectors, $V^{-1}\mu=\sigma^{-2}\Psi^Ty$, so **$\mu=V\sigma^{-2}\Psi^Ty$**. The matrix order in the handwritten continuation needs this repair; the final circled result is correct. Because this posterior is Gaussian, its unique mean is also its mode. Substituting $S=\tau^2I$ proves the ridge equality for both.

![[raw/assets/private-course-slides/2026-03-09-Lec09-I01-p14-ridge.png]]
*Your annotated p. 14, rendered from the preserved private PDF. The checked transcription above repairs the intermediate matrix order; the prior-width connection below preserves your main insight.*

The general completing the square identity is also the engine of [[Learning/Statistical computing & learning/Statistical learning & prediction/Gaussian processes - conditioning by completing the square#3. Complete the square in the joint Gaussian|GP conditioning]] and [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.4 Complete the square to derive the conditional Gaussian|the diffusion bridge]]. [Rasmussen & Williams, §2.1, equations (2.7)–(2.9)](https://gaussianprocess.org/gpml/chapters/RW2.pdf) independently confirms the Gaussian posterior and mean–mode equality, using the transposed design-matrix convention.

## 4. Your flat-prior connection, with its rank condition

Your p. 14 annotations connect “not penalizing” with removing the prior's preference for small weights. In scalar notation,

$$
\tau\to\infty\quad\Longrightarrow\quad
S^{-1}=\tau^{-2}I\to0\quad\Longrightarrow\quad\lambda\to0.
$$

If $\operatorname{rank}(\Psi)=M$, then

$$
\mu\longrightarrow(\Psi^T\Psi)^{-1}\Psi^Ty=\hat w_{\mathrm{OLS}},
\qquad
V\longrightarrow\sigma^2(\Psi^T\Psi)^{-1}.
$$

So your “exactly the same” observation concerns the coefficient mean/MAP. The limiting covariance remains positive: data still leave uncertainty about the weights.

To see why uncertainty **increases** as this prior widens, diagonalize $\Psi^T\Psi=Q\operatorname{diag}(d_j)Q^T$. Along eigenvector $j$,

$$
\operatorname{Var}(q_j^Tw\mid y)
=\frac{\sigma^2}{d_j+\sigma^2/\tau^2}.
$$

A larger $\tau$ removes prior information. This differs from adding more observations, which usually adds information. For $d_j>0$, the variance tends to $\sigma^2/d_j$.

Shrinkage is simplest in these eigenvector directions: $q_j^T\mu=\frac{d_j}{d_j+\lambda}q_j^T\hat w_{\mathrm{OLS}}$. Individual original coefficients need not move monotonically. In the explorer, the intercept briefly exceeds its OLS value before approaching it, because the two feature columns are not orthogonal.

**If the design is rank deficient**, an isotropic ridge mean still tends to the minimum-Euclidean-norm least-squares solution $\Psi^+y$. But for a null direction $d_j=0$, its posterior variance is $\tau^2\to\infty$: the data cannot identify that coefficient direction. A globally flat prior then gives an improper coefficient posterior. $N<M$ guarantees rank deficiency; $N\ge M$ alone does not guarantee full rank.

The handwritten p. 15 phrase “any number is equally likely” is a useful local-flatness intuition, not a proper uniform probability distribution on $\mathbb R^M$. A Gaussian of finite variance is never uniform, and an infinite-variance Gaussian is not a normalized limiting prior on that space.

## 5. Predicting a new response: average over the weights

Your pp. 10–11 derivation starts with marginalization:

$$
\begin{aligned}
p(y_*\mid x_*,\mathcal D)
&=\int p(y_*,w\mid x_*,\mathcal D)\,dw\\
&=\int p(y_*\mid w,x_*,\mathcal D)\,p(w\mid x_*,\mathcal D)\,dw\\
&=\int p(y_*\mid w,x_*)\,p(w\mid\mathcal D)\,dw.
\end{aligned}
$$

The final line uses this regression model's conditional-independence assumptions: the new response's noise is independent of the training data given $w,x_*$, and the fixed new input alone does not update $w$. Here $\mathcal D=(\Psi,y)$; the last line is not a rule for every possible model of inputs and weights.

Let $\psi_*=\psi(x_*)$. Applying a linear transformation to the Gaussian posterior, then adding independent noise, gives

$$
\begin{aligned}
f_*\mid\mathcal D&\sim\mathcal N(\psi_*^T\mu,\psi_*^TV\psi_*),\\
y_*\mid\mathcal D&\sim\mathcal N(\psi_*^T\mu,\psi_*^TV\psi_*+\sigma^2).
\end{aligned}
$$

The first variance is uncertainty about the latent function; the second includes a future observation's noise. This explains the lecture's function samples and uncertainty bands on pp. 12, 16–18. They are posterior credible/predictive summaries under the chosen model; a pointwise band is not automatically a simultaneous band for an entire curve.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression|Ridge regression]] — a zero-centred isotropic Gaussian prior produces its quadratic penalty, with $\lambda=\sigma^2/\tau^2$ for the stated loss.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso|Lasso]] — replacing the Gaussian coefficient prior by independent Laplace priors replaces the squared-L2 penalty by L1 at the posterior mode; the mean-mode equality need not survive.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net|Elastic net]] — multiplying Gaussian-shaped and Laplace-shaped prior factors adds their quadratic and absolute penalties in the MAP objective.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|Regularization]] — the negative log prior supplies a coefficient penalty, with its strength depending on both prior scale and likelihood normalization.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws|Multivariate normal laws]] — completing a quadratic gives the coefficient posterior, and linear transformations give its predictive distribution.

## Origin

> [!info]- Source details
> Thibault Randrianarisoa, Gaussian Processes, University of Toronto, 2026-03-09 (original course PDF retained privately).
> Thibault Randrianarisoa, *Gaussian Processes*, University of Toronto, Winter 2026, dated 2026-03-09; supplied annotated PDF, pp. 4–19. The user's 2026-11-12 request explicitly selected the Bayesian/L2/flat-prior connection. The exact phrase in that request was “when prior sd goes to ininity similar to non regularized”.
>
> User handwriting: dimensions (p. 6), gradient rearrangement (p. 7), Gaussian-likelihood interpretation (p. 8), prior density/determinant (p. 9), predictive marginalization (pp. 10–11), square completion and ridge limit (pp. 13–15). These are transcribed or explicitly paraphrased in place. Matrix-order, rank, intercept, improper-prior and interval qualifications, the nonzero-prior formula and the constructed animation are added checked explanation.
>
> Analytic checks accompany the derivations. Independent augmented least squares, covariance, nullspace and primal/dual checks: [[assets/figures/2026-11-12-gp-ridge/build_visuals.py|generator]], [[assets/figures/2026-11-12-gp-ridge/checks.json|Python results]], [[assets/figures/2026-11-12-gp-ridge/js-checks.json|JavaScript agreement]]. Only the original PDF is private and Git-ignored; selected handwritten page images can be tracked and included with these notes. No slide layout has been disguised or substituted for an original.
