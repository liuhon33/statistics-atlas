---
id: learning-gp-conditioning-completing-square
title: Gaussian processes - conditioning by completing the square
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Local methods & kernels/Gaussian process regression]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Local methods & kernels → Gaussian process regression
study_band: U–M
note_types: [derivation, insight, question, topic-note]
question_roles: [reconcile-approaches, cross-topic-connection, special-to-general, concept-distinction, mechanism]
source_format: [annotated-lecture-pdf, conversation-json]
created: '2026-11-12'
updated: 2026-11-12
status: active
verification: checked
learning_state: unknown
tags: [atlas/learning, subject/computing]
connections:
- '[[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]]'
- '[[Learning/Probability & mathematical foundations/Stochastic processes/Kernels - feature inner products and Gaussian covariances]]'
- '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws]]'
- '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian conditioning]]'
sources:
- '[[raw/assets/private-course-slides/2026-03-09-Lec09-I04-p28-covariance.png]]'
- '[[raw/conversations/2026-08-13-Feature-Map-and-Kernel.json]]'
---

# Gaussian processes - conditioning by completing the square

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Local methods & kernels → Gaussian process regression

Gaussian-process regression predicts an unobserved function value by conditioning a joint Gaussian vector on the observed responses. **The familiar conditional mean and variance come from completing a square.** The same algebra gives the Bayesian regression posterior and the known Gaussian bridge in diffusion.

![[assets/figures/2026-11-12-gp-ridge/gp-conditioning.svg]]
*Original analytic example: squared-exponential covariance with variance 1 and length scale 0.8; four fixed observations with noise SD 0.2. The shaded region is pointwise latent-function mean ± 2 posterior SD. It widens away from the observations. These are new illustrative data, not a recovered lecture figure.*

## 1. A Gaussian vector at every finite collection of inputs

A Gaussian process (GP) is a collection of random variables $\{f(x):x\in\mathcal X\}$ such that every finite vector $(f(x_1),\ldots,f(x_N))^T$ is jointly Gaussian. Its mean and covariance functions are

$$
m(x)=\mathbb E[f(x)],\qquad
k(x,z)=\operatorname{Cov}(f(x),f(z)).
$$

Writing $f\sim\operatorname{GP}(m,k)$ means that, at fixed inputs,

$$
f_X=(f(x_1),\ldots,f(x_N))^T\sim\mathcal N(m_X,K),
\quad (m_X)_i=m(x_i),\quad K_{ij}=k(x_i,x_j).
$$

The input index can be continuous; an actual calculation selects a finite set. A multivariate-normal vector is the resulting finite view of the process. $K$ may be singular, which still defines a degenerate Gaussian vector. [Rasmussen & Williams, §2.2, p. 13](https://gaussianprocess.org/gpml/chapters/RW2.pdf).

### Your proof that the covariance is a kernel matrix

On p. 28 you identify this as the reason for the kernel covariance. With fixed features $\Psi\in\mathbb R^{N\times M}$ and $w\sim\mathcal N(0,\alpha^{-1}I_M)$, where $\alpha>0$,

$$
f_X=\Psi w,\qquad \mathbb E[f_X]=\Psi\mathbb E[w]=0,
$$

$$
\begin{aligned}
\operatorname{Cov}(f_X)
&=\mathbb E[(\Psi w)(\Psi w)^T]\\
&=\mathbb E[\Psi ww^T\Psi^T]\\
&=\Psi\mathbb E[ww^T]\Psi^T\\
&=\alpha^{-1}\Psi\Psi^T=K.
\end{aligned}
$$

The expectation is over the random weights; the feature matrix is fixed. Linear transformation preserves joint Gaussianity, so this is a GP with a finite feature representation. More generally $w\sim\mathcal N(m_0,S)$ gives $m(x)=\psi(x)^Tm_0$ and $k(x,z)=\psi(x)^TS\psi(z)$.

![[raw/assets/private-course-slides/2026-03-09-Lec09-I04-p28-covariance.png]]
*Your p. 28 covariance derivation, rendered from the preserved private PDF. “Before seeing any data, model predicts 0” refers to the prior mean; individual function draws are generally nonzero.*

Your p. 30 annotation adds the characterization “every linear combination is Gaussian”. In finite dimensions,

$$
a^Tf_X\sim\mathcal N(a^Tm_X,a^TKa)\quad\text{for every fixed }a\in\mathbb R^N.
$$

That is stronger than each coordinate separately having a normal marginal. Zero cross-covariance implies independence **for jointly Gaussian vectors**; normal marginals alone are not enough. The [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws|multivariate-normal reference]] now develops this distinction.

### Why the three model equations imply a jointly Gaussian output

*Your chat question, paraphrased: Why do a Gaussian weight prior, $\hat y(x)=w^T\psi(x)$, and a Gaussian observation model imply that the whole output vector is multivariate normal?*

The covariance calculation above is not, by itself, a proof of Gaussianity. Here is the missing step. Hold all inputs fixed, use the **same** weight vector $w\sim\mathcal N(m_0,S)$ at every input, and take any fixed $a\in\mathbb R^N$:

$$
a^Tf_X=a^T\Psi w=(\Psi^Ta)^Tw.
$$

Since $\Psi^Ta\in\mathbb R^M$ is fixed, this is a linear combination of the jointly Gaussian weights. Hence

$$
a^Tf_X\sim\mathcal N\left(a^T\Psi m_0,\ a^T\Psi S\Psi^Ta\right)
\qquad\text{for every }a.
$$

This is exactly the all-linear-combinations definition, so $f_X\sim\mathcal N(\Psi m_0,\Psi S\Psi^T)$, including singular cases.

Now add a vector of independent Gaussian errors, independent also of $w$:

$$
\epsilon\sim\mathcal N(0,\sigma^2I_N),\qquad y=f_X+\epsilon.
$$

For every $a$,

$$
a^Ty=(\Psi^Ta)^Tw+a^T\epsilon
$$

is a sum of **independent** normal variables. Its variance is

$$
a^T\Psi S\Psi^Ta+\sigma^2a^Ta
=a^T(\Psi S\Psi^T+\sigma^2I_N)a.
$$

Therefore

$$
\boxed{y\mid X\sim\mathcal N(\Psi m_0,\ \Psi S\Psi^T+\sigma^2I_N).}
$$

The scalar likelihood must be written $y_i\mid x_i,w\sim\mathcal N(\psi(x_i)^Tw,\sigma^2)$ **together with conditional independence of the errors**. A list of scalar normal distributions alone does not specify a joint distribution. The first two equations establish the latent Gaussian vector; the third, with these independence assumptions, adds observation noise.

For a tiny example, let $\psi(x)=(1,x)^T$, $w\sim\mathcal N(0,I_2)$ and $X=(1,2)$. Then

$$
f_X=\begin{pmatrix}w_0+w_1\\w_0+2w_1\end{pmatrix},\qquad
\Psi=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
K=\Psi\Psi^T=\begin{pmatrix}2&3\\3&5\end{pmatrix}.
$$

The covariance $3$ comes from sharing $w_0,w_1$. **One draw of $w$ selects one whole function**, not a new independently drawn slope at every input. With noise variance $1/4$, $y$ instead has covariance $\begin{pmatrix}2.25&3\\3&5.25\end{pmatrix}$; its cross-covariance remains $3$.

> [!example]- Why normal marginals do not suffice: the chat's random-sign counterexample
> Let $U\sim\mathcal N(0,1)$ and independently choose $R=+1$ or $-1$ with equal probability; put $V=RU$. Both $U$ and $V$ are standard normal, and $\operatorname{Cov}(U,V)=\mathbb E[R]\mathbb E[U^2]=0$.
>
> Nevertheless $|U|=|V|$, so they are dependent. More decisively, $U+V$ equals zero with probability $1/2$, yet has variance $2$. A nondegenerate normal variable has no point mass. Thus $(U,V)$ is not jointly Gaussian. The all-linear-combinations test detects what separate histograms miss.

### How the sample curves on p. 31 can be generated

Choose a finite input grid, form its covariance $K$, and factor $K=LL^T$ (Cholesky if positive definite; an eigenvalue square root also handles semidefinite $K$). Draw $z\sim\mathcal N(0,I)$ and set $f_X=m_X+Lz$. Connecting these grid values displays a finite-grid sample; the interpolation between grid points is a plotting choice.

Different kernels change the covariance among nearby values. The lecture contrasts a squared-exponential kernel with an exponential kernel; the latter gives rougher paths. In the usual parameterization they are $v^2e^{-r^2/(2\ell^2)}$ and $v^2e^{-r/\ell}$, where $r=\|x-z\|$. The lecture writes a different scale parameter for the second one. A zero prior mean does not require flat sample paths.

These are **prior samples**: no observed responses are needed and there is no conditioning step. The chat's question about sampling “by conditioning” mixes this operation with posterior sampling. The worked comparison in §5 below shows both. This finite-grid sampling procedure also appears in [Rasmussen & Williams, §2.2, equation (2.17), p. 14](https://gaussianprocess.org/gpml/chapters/RW2.pdf).

## 2. Put noisy observations and a new value in one vector

Assume independent observation errors,

$$
y_i=f(x_i)+\epsilon_i,\qquad
\epsilon_i\overset{\mathrm{iid}}\sim\mathcal N(0,\sigma^2),\qquad
\epsilon\perp f,\quad \sigma^2>0.
$$

Use a zero mean for now, and let $C=K+\sigma^2I_N$. Marginally $y\sim\mathcal N(0,C)$; the observed $y_i$ are generally **dependent**, even though their errors are independent and their responses are conditionally independent given $f_X$.

At a new fixed input $x_*$, define $k_*=(k(x_1,x_*),\ldots,k(x_N,x_*))^T$ and $k_{**}=k(x_*,x_*)$. For a new noisy response $z=y_*$, let $c=k_{**}+\sigma^2$. Then

$$
\begin{bmatrix}y\\z\end{bmatrix}
\sim\mathcal N\left(0,
J=\begin{bmatrix}C&k_*\\k_*^T&c\end{bmatrix}\right).
$$

Here $C$ is $N\times N$, $k_*$ is $N\times1$, and $c$ is a scalar. Independent new noise adds to $c$, not to the cross-covariance vector. For a latent target $z=f_*$, use $c=k_{**}$ instead.

The noise diagonal is $\sigma^2\mathbf1\{i=j\}$. The input-equality notation on lecture p. 32 can mislead with duplicate inputs: two separate measurements at the same $x$ have independent errors, so their off-diagonal noise covariance is still zero.

## 3. Complete the square in the joint Gaussian

Assume $J\succ0$. Define

$$
q=C^{-1}k_*,\qquad
r=c-k_*^TC^{-1}k_*>0.
$$

The scalar $r$ is the **Schur complement** of $C$. Block multiplication verifies that

$$
J^{-1}=
\begin{bmatrix}
C^{-1}+qq^T/r&-q/r\\
-q^T/r&1/r
\end{bmatrix}.
$$

Expand the joint Gaussian's quadratic form, keeping $y$ fixed:

$$
\begin{aligned}
\begin{bmatrix}y\\z\end{bmatrix}^T J^{-1}
\begin{bmatrix}y\\z\end{bmatrix}
&=y^TC^{-1}y+\frac{(q^Ty)^2}{r}-\frac{2zq^Ty}{r}+\frac{z^2}{r}\\
&=y^TC^{-1}y+\frac{z^2-2zq^Ty+(q^Ty)^2}{r}\\
&=y^TC^{-1}y+\frac{(z-q^Ty)^2}{r}.
\end{aligned}
$$

The first term does not depend on $z$. Divide the joint density by the marginal density of $y$, or simply normalize the remaining one-variable Gaussian kernel:

$$
p(z\mid y)\propto\exp\left[-\frac{(z-q^Ty)^2}{2r}\right].
$$

Consequently,

$$
\boxed{z\mid y\sim\mathcal N\left(k_*^TC^{-1}y,\ c-k_*^TC^{-1}k_*\right).}
$$

This derives the formula displayed on pp. 35–36 rather than treating it as an unrelated rule. If a latent conditional variance is zero, the conditional law is a point mass; the density derivation above requires $r>0$. Positive independent noise on a fresh response ensures positive $r$.

The general vector formula, with $u\in\mathbb R^p$, $v\in\mathbb R^q$, and positive-definite joint covariance, is

$$
v\mid u=a\sim\mathcal N\left(
\mu_v+\Sigma_{vu}\Sigma_{uu}^{-1}(a-\mu_u),
\Sigma_{vv}-\Sigma_{vu}\Sigma_{uu}^{-1}\Sigma_{uv}\right).
$$

Its covariance subtraction describes the uncertainty removed by observing $u$. This is [Rasmussen & Williams, Appendix A.2, equation (A.6)](https://gaussianprocess.org/gpml/chapters/RWA.pdf), with the roles of the blocks labelled explicitly.

## 4. The promised connection to diffusion

Your earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.4 Complete the square to derive the conditional Gaussian|Lecture 12 square-completion step]] and [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#7.2 Derive the known Gaussian bridge by completing the square|VAE–diffusion comparison]] use the same template:

$$
\log p(u\mid\text{fixed information})
=-\tfrac12u^TAu+b^Tu+C
\quad\Longrightarrow\quad
\text{mean}=A^{-1}b,\quad\text{covariance}=A^{-1}.
$$

| Application | Unknown being squared | Precision $A$ | Linear coefficient $b$ |
| --- | --- | --- | --- |
| Bayesian regression | coefficient vector $w$ | $S^{-1}+\sigma^{-2}\Psi^T\Psi$ | $S^{-1}m_0+\sigma^{-2}\Psi^Ty$ |
| GP prediction above | scalar future value $z$ | $1/r$ | $(k_*^TC^{-1}y)/r$ |
| Diffusion bridge, $t\ge2$ | $u=x_{t-1}$, with $x_t,x_0$ fixed | $a_t I$ | $\sqrt{\alpha_t}x_t/\beta_t+\sqrt{\bar\alpha_{t-1}}x_0/(1-\bar\alpha_{t-1})$ |

In the last row, the forward step is $x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon_t$, where $\epsilon_t\sim\mathcal N(0,I)$, $\alpha_t=1-\beta_t$, $0<\beta_t<1$, $\bar\alpha_{t-1}=\prod_{s=1}^{t-1}\alpha_s$, and

$$
a_t=\frac{\alpha_t}{\beta_t}+\frac{1}{1-\bar\alpha_{t-1}}.
$$

Regression combines prior and likelihood precisions. The diffusion bridge combines two Gaussian factors in the previous state. GP prediction isolates the new coordinate from a joint Gaussian precision matrix. **The unknown changes; the algebraic operation is identical.** The diffusion bridge conditions on the original $x_0$ and is analytically known; this does not make the learned reverse distribution conditioned only on $x_t$ automatically known.

## 5. Weight space and function space give the same prediction

For a finite feature prior $w\sim\mathcal N(0,S)$ with $S\succ0$, and observation noise variance $\sigma^2>0$, define

$$
K=\Psi S\Psi^T,\qquad k_*=\Psi S\psi_*,\qquad
k_{**}=\psi_*^TS\psi_*.
$$

The regression posterior covariance and mean can be written

$$
\begin{aligned}
V&=(S^{-1}+\sigma^{-2}\Psi^T\Psi)^{-1}
=S-S\Psi^TC^{-1}\Psi S,\\
\mu&=\sigma^{-2}V\Psi^Ty=S\Psi^TC^{-1}y.
\end{aligned}
$$

Substitute these into the Bayesian regression prediction:

$$
\psi_*^T\mu=k_*^TC^{-1}y,\qquad
\psi_*^TV\psi_*=k_{**}-k_*^TC^{-1}k_*.
$$

Both the latent mean **and variance** agree. Add $\sigma^2$ in either representation for a fresh noisy response. Choosing a kernel directly lets the function-space calculation remain finite even when no finite feature map represents that kernel.

At multiple test inputs, with $K_{*X}$ of shape $N_*\times N$,

$$
f_*\mid y\sim\mathcal N\left(
K_{*X}C^{-1}y,\ K_{**}-K_{*X}C^{-1}K_{X*}\right).
$$

For a nonzero known mean function, replace $y$ by $y-m_X$ and add $m_*$ to the predictive mean. The covariance is unchanged. In computation, solve linear systems using a Cholesky factor of $C$ rather than explicitly constructing $C^{-1}$.

With fixed inputs, kernel parameters and noise variance, the conditional covariance does not depend on the numerical response values $y$. Its mean does. Fitting kernel parameters to $y$ creates an indirect dependence of the fitted uncertainty on those responses.

### Prediction is conditioning, not sampling

*Your chat question, paraphrased: Instead of fitting a model and plugging in a test input, am I now sampling from a joint training-and-test distribution?*

The useful part of this intuition is **jointly model the outputs, then condition on the observed outputs**. The inputs $X,x_*$ are fixed indices, not quantities being sampled. Adding a test location to the covariance matrix does not use its unknown target value. With noisy training data, condition on $y$ through $C=K+\sigma^2I$, not on the false equality $f_X=y$.

| Operation | What it does |
| --- | --- |
| Prior sampling | Draws $f_*\sim\mathcal N(m_*,K_{**})$ before observing any responses. |
| Prediction by conditioning | Computes the distribution $f_*\mid y$; no random draw is required. Its mean is a point prediction. |
| Posterior sampling | Optionally draws a possible function-value vector from that conditional distribution. |

This is not an absolute split between GP and “traditional” regression: Bayesian linear regression also returns a predictive distribution, and §5 shows the equivalence. A GP posterior mean can itself be evaluated as a fitted function. For the zero-mean model, solve $C\beta=y$ once; then

$$
\mu(x_*)=k_*^T\beta=\sum_{i=1}^N\beta_i k(x_i,x_*).
$$

So you **can** plug a new input into a learned GP mean function. What changes is its representation and the accompanying uncertainty, not whether evaluation is allowed. The coefficients depend on the whole training covariance; they are not simply normalized positive similarity weights.

### Drawing prior and posterior curves in Python

*Your chat question, paraphrased: Were the p. 31 curves made by choosing an input grid, building its covariance matrix and sampling—and where does conditioning enter?*

For $n_*$ grid inputs and $L_*L_*^T=\Sigma_*$, one posterior draw is

$$
f_*^{(s)}=\mu_*+L_*z^{(s)},\qquad z^{(s)}\sim\mathcal N(0,I_{n_*}).
$$

For a prior draw, substitute $m_*,K_{**}$ for $\mu_*,\Sigma_*$. Sample the **entire vector jointly**. Drawing independently from each one-dimensional posterior marginal preserves the individual means and variances but destroys the cross-input covariance, so it is generally not a GP function draw.

![[assets/figures/2026-11-12-kernel-chat-extension/gp-prior-posterior.svg]]
*Original reproducible example, not a reconstruction of the slide's exact curves. Top: five prior draws under each kernel. Bottom: five latent-function posterior draws after four constructed noisy observations (orange), with dashed means and pointwise ±2-SD bands. All panels share axes; signal variance is 1, $\ell=0.55$, observation SD is 0.15. The exponential convention is $e^{-|x-z|/\ell}$. Colored prior and posterior curves are separate draws, not tracked transformations. A pointwise band need not contain a whole sampled curve.*

> [!example]- Minimal executable Python: grid → covariance → joint draw → conditioning
> ```python
> import numpy as np
> import matplotlib.pyplot as plt
>
> rng = np.random.default_rng(42)
> x = np.linspace(-2, 2, 201)          # fixed prediction grid
> X = np.array([-1.2, -.4, .5, 1.3])  # fixed training inputs
> y = np.array([-.8, .65, .35, -.55])  # constructed observations
> noise_sd, jitter = .15, 1e-10
>
> def k(a, b, ell=.55):
>     d = a[:, None] - b[None, :]     # all pairwise input differences
>     return np.exp(-d**2 / (2*ell**2))
>     # For exponential: return np.exp(-np.abs(d) / ell)
>
> def draw(mean, cov, count=5):
>     cov = (cov + cov.T) / 2
>     L = np.linalg.cholesky(cov + jitter*np.eye(len(mean)))
>     Z = rng.standard_normal((len(mean), count))
>     return mean[:, None] + L @ Z    # each COLUMN is one curve
>
> Kss = k(x, x)
> prior = draw(np.zeros(len(x)), Kss) # no conditioning here
> C = k(X, X) + noise_sd**2*np.eye(len(X))
> B = k(X, x)                        # shape: n_train x n_grid
> L = np.linalg.cholesky(C)
> beta = np.linalg.solve(L.T, np.linalg.solve(L, y))
> V = np.linalg.solve(L, B)
> mu = B.T @ beta
> Sigma = Kss - V.T @ V              # latent posterior covariance
> post = draw(mu, Sigma)
>
> fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)
> axes[0].plot(x, prior)
> axes[0].set_title("Prior: no data")
> axes[1].plot(x, post)
> axes[1].plot(x, mu, "k--", label="Posterior mean")
> axes[1].scatter(X, y, c="red", label="Noisy observations")
> axes[1].set_title("Posterior: conditioned on y")
> axes[1].legend()
> for ax in axes:
>     ax.set(xlabel="x", ylabel="latent f(x)")
> fig.tight_layout()
> plt.show()
> ```

Here `noise_sd**2` is a **model assumption** in $C$. The much smaller `jitter` is a **numerical perturbation** used only for the sampling Cholesky factor; the code actually draws from covariance $K_{**}+\delta I$ or $\Sigma_*+\delta I$, with $\delta=10^{-10}$. Do not reinterpret it as measured observation noise or use it to rescue an invalid kernel. To draw future noisy responses instead of latent functions, add independent noise with variance $\sigma^2$ to the sampled values. The plotted lines merely connect the sampled grid values.

The [[assets/figures/2026-11-12-kernel-chat-extension/build_examples.py|complete figure generator]] runs both kernels, saves its constructed data and records independent covariance/formula checks in [[assets/figures/2026-11-12-kernel-chat-extension/checks.json|checks.json]].

## 6. What changes for classification and hyperparameter learning

For binary responses, pp. 38–40 put a GP prior on a latent score $a(x)$ and use

$$
p(y_i=1\mid a_i)=s(a_i)=\frac{1}{1+e^{-a_i}},\qquad
p(y\mid a)=\prod_i s(a_i)^{y_i}(1-s(a_i))^{1-y_i}.
$$

The log likelihood is no longer quadratic in $a$. The score has a Gaussian **prior**, but its posterior is generally non-Gaussian. Likewise $s(a(x))$ is a bounded probability-valued process, not a GP. Prediction averages the Bernoulli probability over the latent posterior:

$$
p(y_*=1\mid y)=\int s(a_*)p(a_*\mid y)\,da_*.
$$

For the logistic link this does not generally reduce to the Gaussian-regression formulas; approximations or sampling are needed. The lecture's classification picture illustrates a curved decision boundary and predicted class probabilities, not a Gaussian response distribution.

In regression, choose kernel/noise parameters $\theta$, for example an amplitude, length scale and noise SD. With $C_\theta=K_\theta+\sigma_\theta^2I$ and zero mean,

$$
\log p(y\mid X,\theta)
=-\frac12y^TC_\theta^{-1}y
-\frac12\log|C_\theta|
-\frac N2\log(2\pi).
$$

This is the exact marginal likelihood after integrating out the Gaussian latent values/weights. The quadratic term scores fit relative to the covariance; the determinant is the covariance-volume normalization. Optimizing it is empirical Bayes (type-II maximum likelihood); full Bayesian treatment also integrates uncertainty in $\theta$.

The p. 41 phrase “didn't do any learning other than choosing a kernel” should be read as **hyperparameters were held fixed**. Conditioning on responses already learned a posterior function. Hyperparameter fitting is an additional step, and its plug-in uncertainty bands condition on the fitted values.

## Connections

- [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit|Bayesian regression and ridge]] — the finite-feature GP and weight-space model give identical predictive means and covariances.
- [[Learning/Probability & mathematical foundations/Stochastic processes/Kernels - feature inner products and Gaussian covariances|Kernels and feature maps]] — positive semidefiniteness makes the chosen pairwise function a consistent covariance on every finite input collection.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws|Multivariate normal laws]] — finite function-value vectors inherit Gaussian linear transformations, marginals and independence properties.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian conditioning|Gaussian conditioning]] — the Schur-complement formula is the finite-dimensional prediction step, derived here by square completion.

## Origin

> [!info]- Source details
> Thibault Randrianarisoa, Gaussian Processes, University of Toronto, 2026-03-09 (original course PDF retained privately).
> Thibault Randrianarisoa, *Gaussian Processes*, University of Toronto, 2026-03-09: pp. 28–41, plus the square-completion identity on p. 4. The p. 29 margin's feature-series derivation is assigned to the kernel note; p. 27's handwritten feature map is also assigned there. Pages 1–3, 20 and 27 supply lecture framing/dividers, not separate topics.
>
> Your p. 28 covariance derivation and p. 30 joint-normal/independence annotations are retained with precise conditions. The full block-precision proof, primal/dual comparison, diffusion connection, source-wording repairs, numerical example and original plots are added checked synthesis requested on 2026-11-12.
>
> Checked by quadratic expansion, block multiplication, covariance transformation, and independent precision versus covariance/primal versus dual calculations in [[assets/figures/2026-11-12-gp-ridge/checks.json|the shared check record]]. The linked diffusion notes were read at their square-completion sections; this does not claim access to an unseen older GP chat. The private original is preserved with its author and page locators.
>
> Chat extension, 2026-11-12: the user subsequently supplied [[raw/conversations/2026-08-13-Feature-Map-and-Kernel.json|Feature Map and Kernel]], conversation `6a7e0ad5-f974-83ea-9890-37fcdecd0169`. Its visible branch has eight user/assistant exchanges. The joint-Gaussian proof question is `e9e9262d-c652-4cfc-8418-91b148772b36`; the conditioning-versus-sampling question is `e7be153c-3589-4e95-b19e-aeda9de8834a`; the final grid/code question is `9d8f0bc6-52fb-4530-889c-ace13b917843`, answered by `ca541cee-0890-46fd-a36b-fdcb5e3e7515`. Their wording is explicitly paraphrased above. The random-sign example comes from assistant reply `7f0901ae-e94c-4aa0-bc70-09333db878b5`; the shared-weight example and linear-combination proof come from `d47db8f3-8f39-4419-b5fa-87373c74976b`.
>
> Added synthesis supplies the atom-based counterexample check, explicit joint-noise assumptions, noisy-data qualification, covariance-preserving sampling comparison, jitter distinction and reproducible new figures/code. These are not attributed to the user's handwriting. Already-covered ridge, square-completion, hyperparameter and classification explanations were not duplicated. The whole visible chat text was read, but 29 slide-image pointers contain no image bytes; no recovery or byte identity with the separately preserved lecture is claimed. [[_system/Digest Checkpoints|Coverage and source hash]] and [[_system/Review Queue|attachment gap]] are recorded separately.
