---
id: learning-fisher-score-curvature-precision
title: Fisher information - score spread, curvature, and parameter precision
layer: learning
primary_home: '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Fisher information]]'
subject: statistics
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → Fisher information
study_band: U–M
note_types: [topic-note, derivation, insight, question]
question_roles: [reconcile-approaches, surprising-result, cross-topic-connection]
source_format: youtube-video
created: 2026-11-11
updated: 2026-11-12
status: active
verification: checked
learning_state: introduced
aliases: [Fisher information visual intuition, Why score variance equals negative expected curvature]
tags: [atlas/learning, subject/statistics, topic/fisher-information]
connections:
  - '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Score and observed information]]'
  - '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation]]'
  - '[[Learning/Statistical computing & learning/Simulation & approximate inference/Reparameterization - moving the parameter out of the sampling distribution]]'
  - '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence]]'
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors]]'
  - '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Asymptotic normality]]'
  - '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Cramer–Rao bound]]'
  - '[[Learning/Statistical inference & modeling/Regression & linear models/OLS coefficients through algebra, projection, and likelihood]]'
  - "[[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]]"
sources:
  - 'https://www.youtube.com/watch?v=pneluWj-U-o'
  - '[[raw/articles/2026-11-11-Fisher-Information-youtube-captions.txt]]'
  - '[[raw/articles/2026-11-11-Fisher-source-manifest.json]]'
  - '[[raw/assets/2026-11-11-Fisher-I03-six-panels-8m06.jpg]]'
  - '[[raw/assets/2026-11-11-Fisher-I06-two-dimensional-12m13.jpg]]'
  - 'https://arxiv.org/pdf/1705.01064'
  - 'https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture14.pdf'
  - 'https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture15.pdf'
---

# Fisher information - score spread, curvature, and parameter precision

Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → Fisher information

**Fisher information measures how sensitively a probability model changes when its parameter moves.** Its two regular-model expressions describe the same sensitivity: the spread of log-likelihood slopes across possible observations, and the average downward curvature of the log likelihood. Greater sensitivity makes nearby parameter values easier to distinguish; this is why information appears inversely in estimation uncertainty.

This note develops DJ's [*The Fisher Information*, Mutual Information (2021)](https://www.youtube.com/watch?v=pneluWj-U-o). The lecture's route is especially useful: likelihood curves → their slopes → the distribution of those slopes → the same construction in two dimensions. The expanded proofs and connections below complete that route.

## 1. What is random, and what are we differentiating?

Let $p_\theta(y)$ be a density or probability mass function for an observation $Y$. The parameter $\theta$ is fixed but unknown. Write

$$
\ell(y;\theta)=\log p_\theta(y),\qquad
s_\theta(y)=\frac{\partial\ell(y;\theta)}{\partial\theta},\qquad
h_\theta(y)=\frac{\partial^2\ell(y;\theta)}{\partial\theta^2}.
$$

The [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Score and observed information|score]] is the first derivative **with respect to the parameter, holding the observation fixed**. For a small parameter displacement $\delta$,

$$
\ell(y;\theta+\delta)-\ell(y;\theta)
=s_\theta(y)\delta+O(\delta^2).
$$

A positive score favors a small increase in the parameter; a negative score favors a decrease. Its magnitude measures the *local rate* of change, not the distance to the maximum. In particular, a slope of $0.001$ does not justify extrapolating a tangent line through a parameter change of $1000$: curvature can invalidate that extrapolation.

Why take the logarithm? It preserves the maximizer used in [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation|maximum likelihood estimation]], turns independent likelihood products into sums, and converts absolute density change into relative change:

$$
s_\theta(y)=\frac{\partial_\theta p_\theta(y)}{p_\theta(y)}.
$$

For a continuous observation, $p_\theta(y)$ is a density height, not the probability of the single point $y$. Fixing $\theta$ gives a distribution over $y$; fixing $y$ gives a likelihood function over $\theta$, which need not integrate to one over parameter values.

**One-observation Fisher information** is

$$
\boxed{I(\theta)=\mathbb E_{Y\sim p_\theta}\big[s_\theta(Y)^2\big].}
$$

In a regular model, $\mathbb E_\theta[s_\theta(Y)]=0$, so this is also $\operatorname{Var}_\theta(s_\theta(Y))$. The **same parameter** specifies the sampling distribution and the point where the derivative is evaluated. This is the weighting in [Ly et al., Definition 1.1, p. 5](https://arxiv.org/pdf/1705.01064#page=5).

We can define $I(\theta)$ at every admissible parameter value without knowing which one is true. If data actually come from $p_{\theta^*}$ while scores are evaluated at $\theta_0\ne\theta^*$, their moments are instead $\mathbb E_{\theta^*}[s_{\theta_0}(Y)]$, etc.; these generally differ from the defining moments of $I(\theta_0)$.

## 2. Replaying the one-dimensional case with six graphs

The lecture's [1D construction, 1:50–8:57](https://www.youtube.com/watch?v=pneluWj-U-o&t=110s), estimates a normal **mean** with known variance:

$$
Y\sim\mathcal N(\mu^*,\sigma^2),\qquad \mu^*=5.
$$

Each simulated observation $y_i$ contributes its own curve $\mu\mapsto\ell(y_i;\mu)$. The graphs on the right collect the heights where the vertical evaluation line $\mu_0$ cuts the curves on the left.

| Row | Left: vary candidate $\mu$, keep $y_i$ fixed | Right: fix $\mu_0$, vary the observation |
| --- | --- | --- |
| Top | $h_\mu(y_i)$, second derivatives | Distribution of $h_{\mu_0}(Y)$ |
| Middle | $s_\mu(y_i)$, scores | Distribution of $s_{\mu_0}(Y)$ |
| Bottom | $\ell(y_i;\mu)$, log likelihoods | Distribution of $\ell(Y;\mu_0)$ |

**Try this:** compare the two variance presets at $\mu_0=5$, then move the evaluation slider away from 5. The likelihood curves flatten as the data become noisier, while their score distribution becomes *narrower*. The controls work in Reading view and rendered Live Preview blocks; the standalone HTML and static figures remain available too.

```atlas-interactive
path: assets/figures/2026-11-11-fisher/fisher-1d.html
title: Fisher information — six linked graphs with adjustable mean and variance
height: 1120
```

[[assets/figures/2026-11-11-fisher/fisher-1d.html|Open the standalone 1D explorer]]

> [!example]- Static six-panel view
> ![[assets/figures/2026-11-11-fisher/six-panels.svg]]
> *Original analytic illustration, Codex. Normal mean model with $\sigma=1$; simulated histograms accompany the exact score density. The curvature distribution is a point mass, represented by a stem rather than an artificial bell curve.*

> [!info]- Compare with the lecturer's animation
> ![[raw/assets/2026-11-11-Fisher-I03-six-panels-8m06.jpg]]
> *Direct video-player capture near 8:06, Mutual Information. The explorer is an original reconstruction of the six-panel relationship, not the lecturer's animation code.*

### Why noisier data give less spread in the scores

Write out the three rows:

$$
\ell(y;\mu)=-\frac12\log(2\pi\sigma^2)-\frac{(y-\mu)^2}{2\sigma^2},
\qquad
s_\mu(y)=\frac{y-\mu}{\sigma^2},
\qquad
h_\mu(y)=-\frac1{\sigma^2}.
$$

Because $Y=\mu^*+\sigma Z$, with $Z\sim\mathcal N(0,1)$,

$$
s_{\mu_0}(Y)
=\frac{\mu^*-\mu_0}{\sigma^2}+\frac Z\sigma
\sim\mathcal N\left(\frac{\mu^*-\mu_0}{\sigma^2},\frac1{\sigma^2}\right).
$$

The observation's random deviation grows like $\sigma$, but the score divides it by $\sigma^2$. The resulting score therefore fluctuates like $1/\sigma$. At the truth,

$$
\boxed{I(\mu)=\operatorname{Var}_\mu(s_\mu(Y))=\frac1{\sigma^2}
=-\mathbb E_\mu[h_\mu(Y)].}
$$

| Known data variance | Score standard deviation $\sqrt I$ | Fisher information $I$ | SD of the mean of $n$ observations |
| --- | --- | --- | --- |
| $\sigma^2=1$ | $1$ | $1$ | $1/\sqrt n$ |
| $\sigma^2=25$ | $1/5$ | $1/25$ | $5/\sqrt n$ |

**Keep the units straight:** information is the score *variance*. A horizontal span from $-\sqrt I$ to $+\sqrt I$ has length $2\sqrt I$, not $2I$ or $2I^2$. The automatic captions around 6:55 mistranscribe this; the displayed animation label is $2\sqrt{\mathrm{FI}}$.

### A zero population score is different from a zero fitted sample score

At the true mean, $\mathbb E_{\mu^*}[s_{\mu^*}(Y)]=0$. A finite sample instead gives

$$
\frac1n\sum_i s_{\mu^*}(y_i)=\frac{\bar y-\mu^*}{\sigma^2},
$$

which generally is not zero. The sample score vanishes at $\widehat\mu=\bar y$, the MLE. Thus the true parameter maximizes the **population expected log likelihood**, whereas a particular sample's maximizer fluctuates around it. This is the precise version of the lecturer's intuition at 5:03–5:30.

In this particular normal location model, moving $\mu_0$ shifts the score distribution without changing its variance. Its uncentered second moment does change:

$$
\mathbb E_{\mu^*}[s_{\mu_0}(Y)^2]
=\frac1{\sigma^2}+\frac{(\mu^*-\mu_0)^2}{\sigma^4}.
$$

The invariance of the variance is a special property of this model. It is not permission to mix sampling and evaluation parameters in a general Fisher-information calculation.

## 3. Why score variance equals negative expected second derivative

My question in requesting this note was to fill in “why the expectation of the second derivative happens to be the same as the variance of the spread of the scores.” The identity needs a **minus sign**:

$$
\boxed{\operatorname{Var}_\theta(s_\theta(Y))=-\mathbb E_\theta[h_\theta(Y)].}
$$

The lecturer explicitly leaves the proof open at [8:15–8:41](https://www.youtube.com/watch?v=pneluWj-U-o&t=495s). The reason is probability normalization, not a general rule that arbitrary slopes and curvatures must have equal moments.

### Assumptions that permit the calculation

Work in a neighborhood of an interior parameter value. Assume the density is positive on a common, parameter-independent support, is twice differentiable in $\theta$, and admits integrable bounds that justify moving both derivatives through its integral. Assume the displayed score-square and curvature expectations are finite. These are sufficient local conditions for the identities below; discrete models use sums in place of integrals. Conditions for the later MLE limit theorem are additional.

### Step 1 — normalization forces the average score to be zero

Every member of the model integrates to one:

$$
\int p_\theta(y)\,dy=1.
$$

Differentiate with respect to $\theta$:

$$
0=\int\partial_\theta p_\theta(y)\,dy
=\int s_\theta(y)p_\theta(y)\,dy
=\mathbb E_\theta[s_\theta(Y)].
$$

Increasing a parameter redistributes probability. Its positive and negative changes must cancel because total probability stays one.

### Step 2 — differentiate the zero expectation, including its weights

This is exactly the issue in [[Learning/Statistical computing & learning/Simulation & approximate inference/Reparameterization - moving the parameter out of the sampling distribution#1. The missing term when the distribution depends on the parameter|my reparameterization note's missing density derivative]]: the distribution in an expectation can depend on the parameter too. Apply the product rule to the full integral:

$$
\begin{aligned}
0
&=\frac{\partial}{\partial\theta}
  \int s_\theta(y)p_\theta(y)\,dy\\
&=\int\left[
  \underbrace{\partial_\theta s_\theta(y)}_{h_\theta(y)}p_\theta(y)
  +s_\theta(y)\underbrace{\partial_\theta p_\theta(y)}_{s_\theta(y)p_\theta(y)}
  \right]dy\\
&=\mathbb E_\theta[h_\theta(Y)]
  +\mathbb E_\theta[s_\theta(Y)^2].
\end{aligned}
$$

Since Step 1 gives mean zero, the last expectation is the variance. Rearranging proves the identity. The square appears because differentiating the probability weight contributes **another copy of the score**. See [Stanford STATS 200, Lecture 14, Lemma 14.1, pp. 14-3–14-4](https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture14.pdf#page=3).

Equivalently, twice differentiating the density directly gives the compact identity

$$
\partial_\theta^2p_\theta(y)
=p_\theta(y)\{h_\theta(y)+s_\theta(y)^2\},
$$

whose integral is zero. This also explains the negative sign: expected log curvature must be nonpositive because the squared-score expectation is nonnegative.

### A nonconstant-curvature example that makes the averaging visible

Choose **Logistic** in the explorer. This is an added, fully specified example; the lecture's unlabeled deformation around 8:09 is not assumed to be this distribution.

For logistic location $\mu$ and known scale $b>0$,

$$
p_\mu(y)=\frac1{4b}\operatorname{sech}^2\!\left(\frac{y-\mu}{2b}\right),
\qquad
\ell=-\log(4b)-2\log\cosh\!\left(\frac{y-\mu}{2b}\right).
$$

Direct differentiation gives

$$
s_\mu(y)=\frac1b\tanh\!\left(\frac{y-\mu}{2b}\right),\qquad
h_\mu(y)=-\frac1{2b^2}\operatorname{sech}^2\!\left(\frac{y-\mu}{2b}\right).
$$

Now $h_\mu(Y)$ varies with the observation. To compute the expectations cleanly, let $U=F_\mu(Y)$, where $F_\mu$ is the continuous logistic CDF. Under the matched model $U\sim\operatorname{Uniform}(0,1)$, and

$$
s_\mu(Y)=\frac{2U-1}{b},\qquad
h_\mu(Y)=-\frac{2U(1-U)}{b^2}.
$$

Therefore

$$
\mathbb E[s]=0,\qquad
\mathbb E[s^2]=\frac1{b^2}\int_0^1(2u-1)^2\,du=\frac1{3b^2},
$$

$$
-\mathbb E[h]=\frac2{b^2}\int_0^1u(1-u)\,du=\frac1{3b^2}.
$$

The scores are uniform here, rather than normal, but the information identity still holds. The explorer's $\sigma$ remains the **data standard deviation** in both families: it uses $b=\sigma\sqrt3/\pi$ for the logistic model, whose variance is $\pi^2b^2/3$. Hence its information is $\pi^2/(9\sigma^2)$.

### Why twice differentiable is not enough

Take $Y\sim\operatorname{Uniform}(0,\theta)$ with $\theta>0$. Inside its support, $\ell=-\log\theta$, so $s=-1/\theta$ and $h=1/\theta^2$. Then the naive quantities give

$$
\mathbb E[s]=-1/\theta,\quad
\operatorname{Var}(s)=0,\quad
\mathbb E[s^2]=1/\theta^2,\quad
-\mathbb E[h]=-1/\theta^2.
$$

The regular identities fail. The support endpoint moves, and Leibniz's rule supplies the missing boundary contribution:

$$
\frac d{d\theta}\int_0^\theta\frac1\theta\,dy
=\underbrace{-\frac1\theta}_{\text{interior derivative}}
+\underbrace{\frac1\theta}_{\text{moving boundary}}=0.
$$

This is why the lecturer's curvature formula needs more than the existence of a second derivative. The regular information identities and their usual estimation bounds cannot simply be applied to this example.

## 4. Two parameters turn score variance into a covariance matrix

The lecture's [2D construction, 8:58–14:23](https://www.youtube.com/watch?v=pneluWj-U-o&t=538s), estimates **two means**, with the covariance matrix known. Two dimensions here refer to the parameter vector; they do not mean two observations.

For $\theta\in\mathbb R^d$, the score is a $d\times1$ column vector and the Hessian is a $d\times d$ matrix:

$$
s_\theta(y)=\nabla_\theta\log p_\theta(y),\qquad
H_\theta(y)=\nabla_\theta^2\log p_\theta(y).
$$

The regular-model result becomes

$$
\boxed{I(\theta)=\mathbb E_\theta[s_\theta s_\theta^\top]
=\operatorname{Cov}_\theta(s_\theta)
=-\mathbb E_\theta[H_\theta].}
$$

There is no new trick in the proof. Differentiate $\mathbb E_\theta[s_i]=0$ with respect to $\theta_j$, again differentiating both factors:

$$
0=\int\left[(\partial_{\theta_j}s_i)p_\theta
+s_i\partial_{\theta_j}p_\theta\right]dy
=\mathbb E_\theta[H_{ij}]+\mathbb E_\theta[s_i s_j].
$$

Thus every matrix entry has the same product-rule explanation. [Ly et al., Appendix A, pp. 39–40](https://arxiv.org/pdf/1705.01064#page=39) gives the vector formulation.

### The lecture's normal-mean model, worked out

Let $Y\in\mathbb R^2$ and $Y\sim\mathcal N_2(\mu,\Sigma)$, with known symmetric positive-definite $\Sigma$. Up to a constant independent of $\mu$,

$$
\ell(y;\mu)=-\frac12(y-\mu)^\top\Sigma^{-1}(y-\mu).
$$

For a displacement $\delta$, expanding the quadratic shows

$$
\ell(y;\mu+\delta)-\ell(y;\mu)
=\delta^\top\Sigma^{-1}(y-\mu)
-\frac12\delta^\top\Sigma^{-1}\delta.
$$

Read the linear and quadratic coefficients:

$$
s_\mu(y)=\Sigma^{-1}(y-\mu),\qquad
H_\mu(y)=-\Sigma^{-1}.
$$

Since $\operatorname{Cov}(Y)=\Sigma$,

$$
\operatorname{Cov}(s_\mu(Y))
=\Sigma^{-1}\Sigma(\Sigma^{-1})^\top
=\Sigma^{-1},
\qquad \boxed{I(\mu)=\Sigma^{-1}.}
$$

This makes the lecture's two pictures computable: likelihood ellipses describe variation in parameter space; score histograms describe the gradients of those likelihoods. The reconstruction translates the true mean to $(0,0)$, so the two coordinate systems are easier to compare.

```atlas-interactive
path: assets/figures/2026-11-11-fisher/fisher-2d.html
title: Fisher information matrix — covariance, gradients, and uncertainty
height: 1400
```

[[assets/figures/2026-11-11-fisher/fisher-2d.html|Open the standalone 2D explorer]]

> [!example]- Static 2D geometry
> ![[assets/figures/2026-11-11-fisher/two-dimensional.svg]]
> *Original reconstruction, Codex: $\Sigma=\left(\begin{smallmatrix}4&3\\3&4\end{smallmatrix}\right)$. The first two panels describe individual observations; the last shows the exact sampling covariance $\Sigma/10$ of the mean of ten observations. These are unit Mahalanobis contours, not 95% regions; the panels use different axis limits.*

> [!info]- Lecturer's two-panel reference
> ![[raw/assets/2026-11-11-Fisher-I06-two-dimensional-12m13.jpg]]
> *Direct capture at 12:13, Mutual Information: overlapping likelihood ellipses and the distribution of score vectors. The new third panel adds the estimator-uncertainty connection.*

### Which direction is well determined?

Choose a unit vector $v$ in parameter space. Along the line $\theta+t v$, the score with respect to $t$ is $v^\top s$. Its variance is

$$
I_v=v^\top I v.
$$

This is **directional information**: a large value means changes in that parameter direction strongly affect the distribution. It also proves $I$ is positive semidefinite, since $v^\top I v=\mathbb E[(v^\top s)^2]\ge0$.

The [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors|eigenvectors]] identify directions where this comparison is simplest. If $I v_j=\lambda_j v_j$, then the score's standard deviation in direction $v_j$ is $\sqrt{\lambda_j}$. Under regular efficient estimation, the parameter estimate's standard deviation in that same direction is approximately $1/\sqrt{n\lambda_j}$.

For the correlated preset,

$$
\Sigma=\begin{pmatrix}4&3\\3&4\end{pmatrix},\qquad
I=\frac17\begin{pmatrix}4&-3\\-3&4\end{pmatrix}.
$$

The common-movement direction $(1,1)/\sqrt2$ has data variance $7$ and information $1/7$. The difference direction $(1,-1)/\sqrt2$ has data variance $1$ and information $1$. The latter is easier to locate: the observation cloud is narrow there, while the score cloud is wide there. This inversion also explains the opposite signs of the off-diagonal entries.

For a general direction, distinguish a **slice along a fixed line**, whose unit information-contour radius is $1/\sqrt{n v^\top I v}$, from the **projection of a random estimate**, whose SD is $\sqrt{v^\top I^{-1}v/n}$. They agree along eigenvectors; generally a slice and a projection answer different questions. The two readouts in the explorer make this distinction visible.

## 5. How the same quantity controls MLE precision

For $n$ independent, identically distributed observations, let the full log likelihood and its score be

$$
\ell_n(\theta)=\sum_{i=1}^n\ell(Y_i;\theta),\qquad
U_n(\theta)=\sum_{i=1}^n s_\theta(Y_i).
$$

At the matched parameter, independent, mean-zero scores have additive covariance:

$$
I_n(\theta)=\operatorname{Cov}_\theta(U_n)=nI(\theta).
$$

For an interior MLE, $U_n(\widehat\theta)=0$. Expand the score near the truth:

$$
0\approx U_n(\theta^*)+H_n(\theta^*)(\widehat\theta-\theta^*).
$$

With a consistent estimator, positive-definite information and the regularity needed for a local Hessian law of large numbers and a negligible Taylor remainder, $H_n/n$ approaches $-I$. Therefore

$$
\widehat\theta-\theta^*
\approx I(\theta^*)^{-1}\frac1n\sum_i s_{\theta^*}(Y_i).
$$

The average score has covariance $I/n$. Multiplying by $I^{-1}$ on both sides gives

$$
\boxed{\operatorname{Cov}(\widehat\theta)\approx\frac1nI(\theta^*)^{-1}.}
$$

More precisely, [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Asymptotic normality|asymptotic normality]] states $\sqrt n(\widehat\theta-\theta^*)\xrightarrow{d}\mathcal N_d(0,I^{-1})$ under the appropriate regular-model hypotheses. A limit in distribution alone does not guarantee convergence of actual variances; interpreting the displayed covariance approximation also requires suitable moment control. The normal-mean examples here have the covariance formula **exactly** for every $n$.

This calculation resolves the apparent paradox: more variable individual scores come with a more rapidly changing *total score*. Dividing the score noise by that larger curvature yields **less** parameter error. [Stanford Lecture 14, proof sketch, p. 14-4](https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture14.pdf#page=4); the video description identifies MLE asymptotics as a connection beyond its narrated scope.

### Expected information, observed information, and empirical score products

These agree in expectation under the stated conditions, but their realized values can differ:

| Quantity for $n$ observations | Definition | What it describes |
| --- | --- | --- |
| Expected information | $I_n(\theta)=nI(\theta)$ | Model average across possible datasets |
| Observed information | $J_n(\theta)=-\nabla_\theta^2\ell_n(\theta)$ | Curvature of this dataset's log likelihood |
| Empirical score outer products | $\sum_i s_\theta(y_i)s_\theta(y_i)^\top$ | A sample-based estimate of the matched second moment |

The last expression is a sum of **individual** outer products, not $U_nU_n^\top$, which vanishes at an interior MLE. Even the individual-product estimate can fail dramatically in tiny samples: one normal observation fitted with $\widehat\mu=y$ gives individual score zero, while the model information remains $1/\sigma^2$. The logistic switch illustrates why a realized observed curvature need not equal a realized score variance either.

### The same inverse already appears in OLS

In [[Learning/Statistical inference & modeling/Regression & linear models/OLS coefficients through algebra, projection, and likelihood#5. Gaussian maximum likelihood produces the same objective|my Gaussian OLS derivation]], with fixed full-column-rank design $X\in\mathbb R^{n\times p}$ and known $\sigma^2$,

$$
Y\mid X\sim\mathcal N_n(X\beta,\sigma^2\mathbf I_n),\qquad
U(\beta)=\frac1{\sigma^2}X^\top(Y-X\beta).
$$

The information for the **whole dataset** is

$$
\mathcal I_X(\beta)=\frac1{\sigma^2}X^\top X,
\qquad
\operatorname{Cov}(\widehat\beta\mid X)
=\sigma^2(X^\top X)^{-1}=\mathcal I_X(\beta)^{-1}.
$$

A nearly collinear coefficient direction gives a small eigenvalue of $X^\top X$, hence little information and large estimator variance in that direction. This is the same narrow-score / broad-uncertainty geometry as the 2D explorer, now in regression coordinates.

A Gaussian prior [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit#3. Complete the square to get the whole posterior|adds prior precision]] to this matrix.

## 6. Why this deserves the name information

### Local distinguishability is curvature of KL divergence

Fix the sampling law $p_\theta$ and compare a nearby model $p_{\theta+\delta}$. Using [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]],

$$
D_{\mathrm{KL}}(p_\theta\Vert p_{\theta+\delta})
=\mathbb E_\theta[\ell(Y;\theta)-\ell(Y;\theta+\delta)].
$$

Taylor-expand the second log likelihood, with sufficient regularity to average the remainder:

$$
D_{\mathrm{KL}}(p_\theta\Vert p_{\theta+\delta})
=-\delta^\top\underbrace{\mathbb E_\theta[s]}_{0}
-\frac12\delta^\top\underbrace{\mathbb E_\theta[H]}_{-I}\delta
+o(\|\delta\|^2)
=\boxed{\frac12\delta^\top I(\theta)\delta+o(\|\delta\|^2)}.
$$

Thus information quantifies how quickly nearby distributions become distinguishable. For normal means with the same covariance, this quadratic KL formula is exact, not merely local. KL's nonnegativity also makes the population expected log likelihood maximal at the generating distribution; uniqueness of the parameter additionally needs identifiability.

Information depends on parameter units. Under a smooth invertible change $\theta=g(\eta)$, the chain rule gives $I_\eta=Dg^\top I_\theta Dg$. The scalar entries can change when units change, while the quadratic expression $\delta^\top I\delta$ represents the same local change of distribution. Fisher information is therefore not generally a count of bits.

### The Cramér–Rao connection supplies an estimation bound

For a scalar parameter with $0<I(\theta)<\infty$ and an estimator $T(Y_1,\ldots,Y_n)$ unbiased throughout a neighborhood, differentiating $\mathbb E_\theta[T]=\theta$ under the same kind of regularity gives

$$
1=\mathbb E_\theta[T U_n]
=\operatorname{Cov}_\theta(T,U_n),
$$

because $T$ itself is a statistic independent of the unknown parameter in its definition, and $\mathbb E[U_n]=0$. Cauchy–Schwarz now yields

$$
1\le\operatorname{Var}_\theta(T)\operatorname{Var}_\theta(U_n)
=\operatorname{Var}_\theta(T)nI(\theta),
\qquad
\boxed{\operatorname{Var}_\theta(T)\ge\frac1{nI(\theta)}}.
$$

This is the [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Cramer–Rao bound|Cramér–Rao bound]], for finite-variance unbiased estimators in the regular scalar setting; it is not a universal variance bound for biased estimators. [Stanford Lecture 15, §15.2, Theorem 15.4 and proof](https://web.stanford.edu/class/archive/stats/stats200/stats200.1172/Lecture15.pdf#page=3). The normal sample mean attains it exactly. General regular MLEs approach the corresponding precision asymptotically under stronger assumptions.

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Score and observed information|Score and observed information]] — Separates individual slopes, realized negative curvature, and their model expectations.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation|Maximum likelihood estimation]] — The sample score vanishes at an interior optimum; curvature turns random score fluctuations into parameter error.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/Reparameterization - moving the parameter out of the sampling distribution|Reparameterization]] — Differentiating the probability weights supplies the extra score factor in the information identity.
- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]] — Fisher information is the quadratic term of local model distinguishability.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors|Eigenvalues and eigenvectors]] — The eigenvectors give information directions; reciprocal eigenvalues describe estimation uncertainty.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Asymptotic normality|Asymptotic normality]] — A score CLT and local Hessian averaging explain the regular MLE's inverse-information limit.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Cramer–Rao bound|Cramér–Rao bound]] — Unbiasedness and Cauchy–Schwarz convert score variance into a lower bound on estimator variance.
- [[Learning/Statistical inference & modeling/Regression & linear models/OLS coefficients through algebra, projection, and likelihood|OLS through algebra, projection, and likelihood]] — Gaussian regression information is $X^\top X/\sigma^2$; its inverse is the familiar coefficient covariance.

- [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit|Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]] — Adding Gaussian prior precision to the likelihood information gives the posterior precision and explains ridge shrinkage.

## Origin

> [!info]- Source details
> Main source: DJ, Mutual Information, *The Fisher Information*, published 2021-05-04, duration 17:27. The complete available English automatic captions, 0:07–17:25, were read and preserved as [[raw/articles/2026-11-11-Fisher-Information-youtube-captions.txt]]. The six-panel and 2D frames were inspected separately; full continuous audiovisual viewing is not claimed.
>
> User-selected focus: an interactive reconstruction of the 1D and 2D examples, the omitted curvature proof, and connections within the explanation. The normal examples follow the lecture. The product-rule proof, explicit regularity conditions, logistic example, support counterexample, MLE/OLS/KL/Cramér–Rao derivations and uncertainty panel are added synthesis, not mathematics attributed to the user or to unspoken lecture content.
>
> The lecture's non-normal deformation has no identified formula in the available captions/frame; the logistic example is independently specified. Direct source images remain unchanged. [[assets/figures/2026-11-11-fisher/build_visuals.py|Figure/HTML builder]], [[assets/figures/2026-11-11-fisher/math.js|interactive mathematics]], [[assets/figures/2026-11-11-fisher/test_math.cjs|finite-difference and matrix checks]], and [[assets/figures/2026-11-11-fisher/checks.json|quadrature results]] reproduce and check the additions. Source hashes and exact coverage are in [[_system/Digest Checkpoints]].
