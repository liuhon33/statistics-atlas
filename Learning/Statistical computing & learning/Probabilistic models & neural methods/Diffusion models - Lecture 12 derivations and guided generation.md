---
id: learning-diffusion-lecture12
title: Diffusion models - Lecture 12 derivations and guided generation
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Selected architectures & latent models]]"
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models
study_band: M elective
note_types: [topic-note, derivation]
source_format: lecture-slides
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: introduced
aliases: [Lecture 12 diffusion models, Diffusion lecture derivations]
tags: [atlas/learning, subject/computing, topic/diffusion, study/masters-elective]
sources:
  - "[[raw/notes/2026-11-10-Lec12-diffusion-models.pdf]]"
---

# Diffusion models - Lecture 12 derivations and guided generation

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models

**Diffusion learns to generate data by reversing a known noising process.** The lecture's mathematical route is: Gaussian forward transitions → a tractable noisy-image marginal → a reverse generative model → a variational bound → Gaussian conditional comparisons → a noise-prediction loss. Conditioning and guidance then steer generation toward a label, caption, or image constraint.

This note follows the supplied lecture. The derivations expand algebra omitted by the slides; source-page references identify the starting formulas. Inline links lead to the companion learning note for additional intuition and numerical examples.

## 1. The two processes and the notation

The opening slides place diffusion beside VAEs, GANs, and flow-based models, then distinguish two directions. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=3|Lecture pp. 3–5]].

![[raw/assets/2026-11-11-Diffusion-lecture-P05-processes.png]]

*Source figure: complete render of lecture p. 5, unchanged. Forward diffusion moves from data toward noise; the learned reverse process generates an image from noise. A generated image need not reconstruct a particular original training image.*

Let an image be represented by a vector in $\mathbb R^d$. The notation stays consistent throughout:

| Symbol | Meaning |
| --- | --- |
| $x_0$ | Clean image; training data have distribution $q_0$ |
| $x_t$, $t=1,\ldots,T$ | Noisy states, each also in $\mathbb R^d$ |
| $q(x_t\mid x_{t-1})$ | Specified forward transition |
| $p_\theta(x_{t-1}\mid x_t)$ | Learned reverse transition |
| $\beta_t\in(0,1)$ | Forward noise **variance** per coordinate |
| $\alpha_t=1-\beta_t$ | Retained signal factor in the variance calculation |
| $\bar\alpha_t=\prod_{i=1}^t\alpha_i$, $\bar\alpha_0=1$ | Cumulative signal factor |
| $\xi_t\sim\mathcal N(0,I_d)$ | Independent noise added at forward step $t$ |
| $\epsilon\sim\mathcal N(0,I_d)$ | Aggregate noise used to sample a chosen $x_t$ directly |
| $\sigma_t^2I_d$ | Reverse covariance when it is fixed and isotropic |
| $\epsilon_\theta(x_t,t)$ | Network prediction of aggregate noise |
| $y$ | Conditioning information |
| $s$ | Scalar guidance strength |

The lecture sometimes suppresses $I_d$ when writing an isotropic covariance. Here it is explicit. Also, $\sigma_t$ is a **standard deviation**, so sampling adds $\sigma_t z$ and the covariance is $\sigma_t^2I_d$.

## 2. Forward diffusion and its closed form

### 2.1 One noising step

The forward chain and each Gaussian transition are specified in advance:

$$
q(x_{1:T}\mid x_0)=\prod_{t=1}^Tq(x_t\mid x_{t-1}),
$$

$$
q(x_t\mid x_{t-1})=\mathcal N(\sqrt{\alpha_t}\,x_{t-1},\beta_tI_d).
$$

Equivalently,

$$
x_t=\sqrt{\alpha_t}\,x_{t-1}+\sqrt{\beta_t}\,\xi_t,
\qquad \xi_t\sim\mathcal N(0,I_d),
$$

where the noises are independent across steps and independent of $x_0$. This reindexes the lecture's step noises without changing their distribution. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=6|Lecture p. 6]].

For a random input with finite covariance,

$$
\operatorname{Cov}(X_t)
=\alpha_t\operatorname{Cov}(X_{t-1})+\beta_tI_d.
$$

An identity input covariance remains identity because $\alpha_t+\beta_t=1$. This does not say every dataset initially has unit covariance. If $x_0$ is fixed instead, its conditional variance starts at zero.

### 2.2 Combine two independent Gaussian increments

Substitute the preceding step into the update:

$$
x_t=\sqrt{\alpha_t\alpha_{t-1}}\,x_{t-2}
+\sqrt{\alpha_t\beta_{t-1}}\,\xi_{t-1}
+\sqrt{\beta_t}\,\xi_t.
$$

The last two terms form a mean-zero Gaussian with covariance

$$
\big(\alpha_t\beta_{t-1}+\beta_t\big)I_d
=\big(\alpha_t(1-\alpha_{t-1})+1-\alpha_t\big)I_d
=(1-\alpha_t\alpha_{t-1})I_d.
$$

Consequently,

$$
x_t\overset d=\sqrt{\alpha_t\alpha_{t-1}}\,x_{t-2}
+\sqrt{1-\alpha_t\alpha_{t-1}}\,\epsilon,
\qquad\epsilon\sim\mathcal N(0,I_d).
$$

The $\overset d=$ means **equality in distribution**. A fresh standard normal reproduces the distribution of the combined noise, rather than equaling either original increment sample by sample. One can also define $\epsilon$ as that normalized sum on the original probability space. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=7|Lecture p. 7]].

### 2.3 Extend to an arbitrary timestep

Repeating the expansion gives

$$
x_t=\sqrt{\bar\alpha_t}\,x_0
+\sum_{i=1}^t\sqrt{\beta_i\prod_{j=i+1}^t\alpha_j}\,\xi_i.
$$

The sum is Gaussian. Its variance coefficient telescopes:

$$
\begin{aligned}
\sum_{i=1}^t\beta_i\prod_{j=i+1}^t\alpha_j
&=\sum_{i=1}^t\left(\prod_{j=i+1}^t\alpha_j-\prod_{j=i}^t\alpha_j\right)\\
&=1-\prod_{j=1}^t\alpha_j=1-\bar\alpha_t.
\end{aligned}
$$

Empty products equal one. Therefore

$$
\boxed{q(x_t\mid x_0)
=\mathcal N(\sqrt{\bar\alpha_t}\,x_0,(1-\bar\alpha_t)I_d),}
$$

or, as a sampling rule,

$$
\boxed{x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon,
\qquad\epsilon\sim\mathcal N(0,I_d).}
$$

This samples a **chosen marginal timestep** without simulating every preceding step. Reusing one arbitrary $\epsilon$ at all times would give the correct one-time marginals but generally a different joint trajectory from the independent-increment Markov chain.

### 2.4 Why the endpoint approaches white noise

For fixed $x_0$, as $\bar\alpha_T\to0$, the conditional mean approaches zero and the covariance approaches $I_d$:

$$
\sqrt{\bar\alpha_T}x_0\to0,\qquad(1-\bar\alpha_T)I_d\to I_d.
$$

Hence the endpoint approaches $\mathcal N(0,I_d)$. The same limit holds for the noisy-data marginal under the usual setup in which the data distribution is fixed as the schedule changes. At a finite chosen $T$, this is generally an approximation. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=8|Lecture p. 8]].

#### Why this is not an ever-spreading random walk

Here $T$ counts **forward noising steps**, not reverse denoising steps. Each forward update both shrinks the previous state and adds fresh noise:

$$
x_t=\underbrace{\sqrt{\alpha_t}\,x_{t-1}}_{\text{shrink the previous state}}
+\underbrace{\sqrt{\beta_t}\,\xi_t}_{\text{add fresh noise}}.
$$

For fixed $x_0$, the independent noises have mean zero, so iterating the conditional-mean recursion gives

$$
\mathbb E[x_T\mid x_0]
=\sqrt{\alpha_1\alpha_2\cdots\alpha_T}\,x_0
=\sqrt{\bar\alpha_T}\,x_0.
$$

The original signal is repeatedly multiplied by factors smaller than one. If every $\alpha_t=\alpha$, the mean coefficient is $\alpha^{T/2}$, **not** $\alpha^T$. For example, at $T=100$:

- $\alpha=0.9$: $\alpha^{50}\approx0.0052$, so the mean is about $0.0052x_0$.
- $\alpha=0.999$: $\alpha^{50}\approx0.951$, so the mean is still about $0.951x_0$.

Thus **100 steps alone does not guarantee a near-zero mean**: the schedule must make $\bar\alpha_T$ small. For a varying schedule, merely knowing each $\alpha_t\in(0,1)$ does not by itself guarantee that the infinite product tends to zero. The endpoint statement above is explicitly conditional on $\bar\alpha_T\to0$.

To compare with a random walk, take constant $\beta\in(0,1)$ and independent standard Gaussian noises. In one coordinate, starting from fixed $x_0$:

| Process | Update | Conditional variance after $t$ steps |
| --- | --- | --- |
| Ordinary random walk | $x_t=x_{t-1}+\sqrt\beta\,\xi_t$ | $t\beta$, growing without bound |
| This diffusion | $x_t=\sqrt{1-\beta}\,x_{t-1}+\sqrt\beta\,\xi_t$ | $1-(1-\beta)^t$, approaching $1$ |

![[assets/figures/2026-11-11-diffusion-lecture/random-walk-vs-diffusion.svg]]

*Original illustration in one coordinate, with fixed $x_0=4$ and constant $\beta=0.1$ (an illustrative schedule, not the lecture's schedule). Both top panels use identical axes and the same three noise sequences. Thick lines show exact conditional means; shading shows mean ± two standard deviations, covering about 95% at each fixed step, not bounding entire paths. Thin sample paths keep fluctuating even when the diffusion mean is nearly zero. Below: the random-walk variance keeps growing, whereas the diffusion variance approaches one.*

The crucial difference is that diffusion **shrinks everything already present, including noise added at earlier steps**. Fresh noise enters, but old noise is attenuated; the variance recursion is $v_t=(1-\beta)v_{t-1}+\beta$, starting at $v_0=0$.

Finally, **zero mean does not mean the sample becomes zero**. When $\bar\alpha_T$ is tiny, $x_T\mid x_0\approx\mathcal N(0,I_d)$: the distribution is centered at zero, but each coordinate still has approximately unit variance. Individual trajectories do not move monotonically toward zero, nor are they confined to a fixed bounded region.

Think **“the image is gradually forgotten and replaced by fixed-scale noise,”** not “the image wanders farther and farther away without bound.”

## 3. The reverse model

Ideally, generation would draw $x_T\sim q(x_T)$ and then sample the true reverse conditionals. Bayes' rule gives

$$
q(x_{t-1}\mid x_t)
=\frac{q(x_t\mid x_{t-1})q(x_{t-1})}{q(x_t)}.
$$

Knowing the forward transition does not supply the noisy-data marginals in this expression. That is the difficulty highlighted by the lecture. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=9|Lecture pp. 9–10]].

Choose a simple terminal distribution and parameterized reverse transitions:

$$
p(x_T)=\mathcal N(0,I_d),\qquad
p_\theta(x_{t-1}\mid x_t)=\mathcal N(\mu_\theta(x_t,t),\sigma_t^2I_d).
$$

The lecture motivates Gaussian reverse steps using small forward noise. This is a modeling approximation, not a claim that every finite-step true reverse distribution is exactly Gaussian for arbitrary data.

The complete generative joint is

$$
\boxed{p_\theta(x_{0:T})=p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t).}
$$

The image marginal integrates out every noisy state:

$$
p_\theta(x_0)=\int p_\theta(x_{0:T})\,dx_{1:T}.
$$

The network determines transition parameters. It does not separately output every path posterior or image probability induced by this joint.

## 4. Derive the variational upper bound on negative log likelihood

For one observed image, the goal is to maximize $\log p_\theta(x_0)$. Let $Z=x_{1:T}$ and use the known forward process $q(Z\mid x_0)$ as the variational distribution. Assume matching support sufficient for the displayed KL, $0<p_\theta(x_0)<\infty$, and finite log expectations.

Start from the nonnegative posterior KL:

$$
\begin{aligned}
D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z\mid x_0))
&=\mathbb E_q\log\frac{q(Z\mid x_0)}{p_\theta(Z\mid x_0)}\\
&=\mathbb E_q\log\frac{q(Z\mid x_0)p_\theta(x_0)}{p_\theta(x_0,Z)}\\
&=\underbrace{\mathbb E_q\log\frac{q(Z\mid x_0)}{p_\theta(x_0,Z)}}_{L(x_0)}
+\log p_\theta(x_0).
\end{aligned}
$$

Rearrange:

$$
\boxed{L(x_0)=-\log p_\theta(x_0)
+D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z\mid x_0))
\geq-\log p_\theta(x_0).}
$$

Thus $L$ is an **upper bound on negative log likelihood**, and $-L$ is the **ELBO**, a lower bound on log likelihood. Training averages $L(x_0)$ over the data. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=11|Lecture p. 11]].

The companion note gives the equivalent [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#4. Write the diffusion derivation in exactly the same order|VAE-shaped derivation]]. Here the sign follows the lecture's loss convention throughout.

Minimizing the bound optimizes a surrogate for the original likelihood objective. Since both terms on the right can change with $\theta$, decreasing $L$ does not by itself prove that the likelihood term and posterior gap improved separately.

## 5. Turn one path expectation into tractable Gaussian terms

### 5.1 Condition on the known clean training image

Although $q(x_{t-1}\mid x_t)$ is difficult, $q(x_{t-1}\mid x_t,x_0)$ is tractable. For $t\geq2$, Bayes' rule and the forward Markov property give

$$
q(x_{t-1}\mid x_t,x_0)
=\frac{q(x_t\mid x_{t-1})q(x_{t-1}\mid x_0)}{q(x_t\mid x_0)}.
$$

Every term on the right is a known Gaussian density. The clean image is available in training, even though it is unavailable when generating a new image. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=12|Lecture p. 12]].

### 5.2 Show the cancellation in the path factorization

Solve the previous identity for the forward transition:

$$
q(x_t\mid x_{t-1})
=q(x_{t-1}\mid x_t,x_0)\frac{q(x_t\mid x_0)}{q(x_{t-1}\mid x_0)}.
$$

Insert it for every $t\geq2$:

$$
\require{cancel}
\begin{aligned}
q(x_{1:T}\mid x_0)
&=q(x_1\mid x_0)\prod_{t=2}^T
\left[q(x_{t-1}\mid x_t,x_0)\frac{q(x_t\mid x_0)}{q(x_{t-1}\mid x_0)}\right]\\
&=q(x_1\mid x_0)
\left[q(x_1\mid x_2,x_0)\frac{q(x_2\mid x_0)}{q(x_1\mid x_0)}\right]\\
&\quad\times\left[q(x_2\mid x_3,x_0)\frac{q(x_3\mid x_0)}{q(x_2\mid x_0)}\right]
\cdots
\left[q(x_{T-1}\mid x_T,x_0)\frac{q(x_T\mid x_0)}{q(x_{T-1}\mid x_0)}\right]\\
&=\left[\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0)\right]\\
&\quad\times\underbrace{q(x_1\mid x_0)
\frac{q(x_2\mid x_0)}{q(x_1\mid x_0)}
\frac{q(x_3\mid x_0)}{q(x_2\mid x_0)}
\cdots
\frac{q(x_T\mid x_0)}{q(x_{T-1}\mid x_0)}}_{\text{telescoping marginal-density factors}}\\
&=\left[\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0)\right]
\frac{\cancel{q(x_1\mid x_0)}\,\cancel{q(x_2\mid x_0)}\,\cdots\,\cancel{q(x_{T-1}\mid x_0)}\,q(x_T\mid x_0)}
{\cancel{q(x_1\mid x_0)}\,\cancel{q(x_2\mid x_0)}\,\cdots\,\cancel{q(x_{T-1}\mid x_0)}}\\
&=q(x_T\mid x_0)\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0).
\end{aligned}
$$

The expanded pattern shows the first two and final substitutions (for a sufficiently long chain; for $T=2$, there is just one bracket). Each marginal-density factor $q(x_s\mid x_0)$ for $1\leq s\leq T-1$ occurs once in the numerator and once in the denominator, so the crossed-out factors cancel. Only $q(x_T\mid x_0)$ survives from this telescoping part; the reverse conditionals $q(x_{t-1}\mid x_t,x_0)$ are not canceled. This is a refactorization of the same forward distribution.

### 5.3 Separate the loss into endpoints and intermediate terms

Start from the definition of $L$ in §4, with $Z=x_{1:T}$:

$$
L(x_0)=\mathbb E_{q(x_{1:T}\mid x_0)}
\left[\log\frac{q(x_{1:T}\mid x_0)}{p_\theta(x_{0:T})}\right].
$$

Here $x_0$ is fixed, and the expectation is still over the **whole forward path**. Substitute the refactorized numerator from §5.2 and the generative joint from §3:

$$
\begin{aligned}
L(x_0)
&=\mathbb E_q\left[
\log\frac{q(x_T\mid x_0)\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0)}
{p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t)}\right]\\
&=\mathbb E_q\left[
\log\frac{q(x_T\mid x_0)\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0)}
{p(x_T)\,p_\theta(x_0\mid x_1)\prod_{t=2}^Tp_\theta(x_{t-1}\mid x_t)}\right]\\
&=\mathbb E_q\left[\log\left(
\frac{q(x_T\mid x_0)}{p(x_T)}
\prod_{t=2}^T\frac{q(x_{t-1}\mid x_t,x_0)}{p_\theta(x_{t-1}\mid x_t)}
\frac{1}{p_\theta(x_0\mid x_1)}
\right)\right].
\end{aligned}
$$

The second line pulls out the denominator's $t=1$ factor, $p_\theta(x_0\mid x_1)$, so the remaining products both start at $t=2$. The third line simply groups corresponding factors into ratios; **no $q$ factor is canceled against a $p_\theta$ factor**.

Now use $\log(ABC)=\log A+\log B+\log C$, $\log\prod_t r_t=\sum_t\log r_t$, and $\log(1/p)=-\log p$:

$$
\begin{aligned}
L(x_0)=\mathbb E_q\Bigg[
&\log\frac{q(x_T\mid x_0)}{p(x_T)}
+\sum_{t=2}^T\log\frac{q(x_{t-1}\mid x_t,x_0)}{p_\theta(x_{t-1}\mid x_t)}\\
&-\log p_\theta(x_0\mid x_1)\Bigg].
\end{aligned}
$$

Thus the reconstruction term has a minus sign because it remains in the **denominator**. There is no matching $t=1$ numerator factor: §5.2 already absorbed $q(x_1\mid x_0)$ into the telescoping cancellation. Up to this point, we have only rewritten the same integrand; we have not yet evaluated any expectation or introduced an approximation.

For each summand, average first over $x_{t-1}$ conditional on $x_t,x_0$. That inner expectation is a KL. The result is

$$
\boxed{
\begin{aligned}
L(x_0)={}&\underbrace{D_{\rm KL}(q(x_T\mid x_0)\|p(x_T))}_{L_T(x_0)}\\
&+\sum_{t=2}^T\underbrace{\mathbb E_{q(x_t\mid x_0)}
D_{\rm KL}(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t))}_{L_{t-1}(x_0)}\\
&+\underbrace{\mathbb E_{q(x_1\mid x_0)}[-\log p_\theta(x_0\mid x_1)]}_{L_0(x_0)}.
\end{aligned}}
$$

The subscript $t-1$ names the loss associated with predicting state $x_{t-1}$ from state $x_t$. In particular, $t=2$ contributes $L_1$. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=13|Lecture pp. 13–14]].

For a fixed forward schedule and fixed terminal prior, $L_T$ is independent of the reverse-model parameters, so it can be omitted when optimizing those parameters. It need not be zero. The outer expectations in the intermediate and reconstruction terms still remain.

### 5.4 Complete the square to derive the conditional Gaussian

Set $u=x_{t-1}$ and keep $x_t,x_0$ fixed. Ignoring factors independent of $u$,

$$
\begin{aligned}
\log q(u\mid x_t,x_0)
={}&-\frac{\|x_t-\sqrt{\alpha_t}u\|^2}{2\beta_t}
-\frac{\|u-\sqrt{\bar\alpha_{t-1}}x_0\|^2}{2(1-\bar\alpha_{t-1})}
+C\\
={}&-\frac12[A\|u\|^2-2b^Tu]+C,
\end{aligned}
$$

where

$$
A=\frac{\alpha_t}{\beta_t}+\frac1{1-\bar\alpha_{t-1}},
\qquad
b=\frac{\sqrt{\alpha_t}}{\beta_t}x_t
+\frac{\sqrt{\bar\alpha_{t-1}}}{1-\bar\alpha_{t-1}}x_0.
$$

Since $A>0$, complete the square:[^gp-completing-square]

$$
A\|u\|^2-2b^Tu
=A\|u-A^{-1}b\|^2-A^{-1}\|b\|^2.
$$

[^gp-completing-square]: Future connection: you recall completing the square in your earlier Gaussian-process work, which has not yet been digested. Once that note exists, revisit this step and link the corresponding derivations.

Thus the mean is $A^{-1}b$ and the covariance is $A^{-1}I_d$. Simplify the precision denominator:

$$
\alpha_t(1-\bar\alpha_{t-1})+\beta_t
=1-\bar\alpha_t.
$$

We obtain

$$
\boxed{q(x_{t-1}\mid x_t,x_0)
=\mathcal N(\tilde\mu_t(x_t,x_0),\tilde\beta_tI_d),}
$$

$$
\boxed{\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,}
$$

$$
\boxed{\tilde\mu_t
=\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t
+\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0.}
$$

These equations apply for $t\geq2$. At $t=1$, the clean image is already fixed, so conditioning on it makes the distribution of $x_0$ a point mass. That endpoint is represented by $L_0$, not by inserting a zero variance into a nondegenerate Gaussian KL formula. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=14|Lecture pp. 14–15]].

### 5.5 Calculate the Gaussian KL instead of sampling its inner variable

For fixed $x_t,x_0$, abbreviate $m=\tilde\mu_t$, $\mu=\mu_\theta(x_t,t)$, $v=\tilde\beta_t$, and $w=\sigma_t^2$. The teacher distribution is $\mathcal N(m,vI_d)$ and the model is $\mathcal N(\mu,wI_d)$.

Their log-density ratio is

$$
\log\frac{q(u)}{p_\theta(u)}
=\frac d2\log\frac{w}{v}
-\frac{\|u-m\|^2}{2v}+\frac{\|u-\mu\|^2}{2w}.
$$

Under $q$, the two quadratic expectations are

$$
\mathbb E_q\|U-m\|^2=dv,\qquad
\mathbb E_q\|U-\mu\|^2=dv+\|m-\mu\|^2.
$$

Therefore the exact local KL is

$$
\boxed{D_{\rm KL}(q\|p_\theta)
=\frac12\left[d\left(\log\frac{\sigma_t^2}{\tilde\beta_t}-1+
\frac{\tilde\beta_t}{\sigma_t^2}\right)
+\frac{\|\tilde\mu_t-\mu_\theta(x_t,t)\|^2}{\sigma_t^2}\right].}
$$

When the reverse variance is fixed, the covariance terms are independent of $\theta$. Hence

$$
L_{t-1}(x_0)
=\mathbb E_{q(x_t\mid x_0)}\left[
\frac{\|\tilde\mu_t-\mu_\theta(x_t,t)\|^2}{2\sigma_t^2}\right]+C_t.
$$

This explains the “$+\text{const.}$” on slide 15. The full local KL has been integrated over $x_{t-1}$; the expectation over $x_t$ has not. A [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#7.4 Work through a continuous diffusion step with actual numbers|numerical Gaussian step]] in the companion note illustrates the calculation.

## 6. Derive noise prediction from mean prediction

### 6.1 Substitute the clean image out of the teacher mean

From the forward marginal,

$$
x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\,\epsilon}{\sqrt{\bar\alpha_t}}.
$$

Substitute into $\tilde\mu_t$. Since $\bar\alpha_t=\alpha_t\bar\alpha_{t-1}$,

$$
\begin{aligned}
\tilde\mu_t
={}&\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t
+\frac{\beta_t}{\sqrt{\alpha_t}(1-\bar\alpha_t)}
\left(x_t-\sqrt{1-\bar\alpha_t}\,\epsilon\right)\\
={}&\frac{\alpha_t(1-\bar\alpha_{t-1})+\beta_t}
{\sqrt{\alpha_t}(1-\bar\alpha_t)}x_t
-\frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1-\bar\alpha_t}}\epsilon\\
={}&\boxed{\frac1{\sqrt{\alpha_t}}\left(x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon\right)}.
\end{aligned}
$$

The same cancellation $\alpha_t(1-\bar\alpha_{t-1})+\beta_t=1-\bar\alpha_t$ appears again. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=16|Lecture p. 16]].

### 6.2 Let the network predict noise

Define the model mean using a network prediction $\epsilon_\theta$ in the same expression:

$$
\mu_\theta(x_t,t)=\frac1{\sqrt{\alpha_t}}\left(x_t-
\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right).
$$

Then

$$
\tilde\mu_t-\mu_\theta
=\frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1-\bar\alpha_t}}
(\epsilon_\theta-\epsilon).
$$

Square this difference and divide by $2\sigma_t^2$:

$$
\frac{\|\tilde\mu_t-\mu_\theta\|^2}{2\sigma_t^2}
=\underbrace{\frac{\beta_t^2}{2\sigma_t^2\alpha_t(1-\bar\alpha_t)}}_{\lambda_t}
\|\epsilon_\theta(x_t,t)-\epsilon\|^2.
$$

For $t\geq2$, the intermediate term averaged over training images is therefore

$$
L_{t-1}=\lambda_t\,
\mathbb E_{x_0\sim q_0,\epsilon\sim\mathcal N(0,I_d)}
\|\epsilon_\theta(\sqrt{\bar\alpha_t}x_0+
\sqrt{1-\bar\alpha_t}\epsilon,t)-\epsilon\|^2+C_t.
$$

The lecture then replaces the weights by one to form a simpler loss:

$$
\boxed{L_{\rm simple}(\theta)
=\mathbb E_{x_0,t,\epsilon}\|
\epsilon-\epsilon_\theta(\sqrt{\bar\alpha_t}x_0+
\sqrt{1-\bar\alpha_t}\epsilon,t)\|^2,}
$$

with $t$ sampled uniformly from $\{1,\ldots,T\}$. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=17|Lecture pp. 17–19]].

Replacing $\lambda_t$ by one **changes the relative weighting of timesteps**. It is not an algebraic equality to the complete negative ELBO. Slide 17 reports an empirical motivation for this choice. The exact likelihood bound still includes endpoint terms and its proper weights; slide 19 uses the simplified loss also at $t=1$.

The bound was already trainable before this rearrangement: forward samples and differentiable reverse log densities suffice. The companion note separates [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#9.2 Density evaluation, integration, and optimization are different operations|density evaluation, analytic integration, and optimization]].

## 7. Training, sampling, and the noise schedule

### 7.1 Training uses a randomly selected noise level

The lecture's simplified training algorithm is:

1. Sample a clean training image $x_0\sim q_0$.
2. Sample $t\sim\operatorname{Uniform}\{1,\ldots,T\}$.
3. Sample $\epsilon\sim\mathcal N(0,I_d)$.
4. Form $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$.
5. Evaluate $\epsilon_\theta(x_t,t)$ and take a gradient step on $\|\epsilon-\epsilon_\theta(x_t,t)\|^2$.

The target noise is known because training generated it. One training example does not require running the whole reverse chain. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=19|Lecture p. 19, Algorithm 1]].

### 7.2 Sampling starts from noise

A draw from a Gaussian can be written as mean plus standard deviation times fresh standard noise. Substituting the noise-parameterized mean gives

$$
\boxed{x_{t-1}=\frac1{\sqrt{\alpha_t}}\left(x_t-
\frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right)
+\sigma_t z.}
$$

The equality $1-\alpha_t=\beta_t$ explains the two equivalent numerators used by the lecture. Generation proceeds as follows:

1. Draw $x_T\sim\mathcal N(0,I_d)$.
2. For $t=T,T-1,\ldots,1$, evaluate the noise network and use the update above.
3. Draw fresh $z\sim\mathcal N(0,I_d)$ at each step with $t>1$; use $z=0$ at $t=1$, as specified in the displayed algorithm.
4. Return $x_0$.

Thus the lecture's training uses one selected noise level, while its sampler traverses the reverse sequence. The final-step choice $z=0$ is a sampling convention in Algorithm 2; exact likelihood evaluation still requires a specified image decoder $p_\theta(x_0\mid x_1)$. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=18|Lecture pp. 18–19]].

### 7.3 The concrete schedule in the lecture

The lecture describes $T=1000$, a linearly increasing forward variance from $\beta_1=10^{-4}$ to $\beta_T=0.02$, and the choice $\sigma_t^2=\beta_t$. It also mentions alternative schedules and learned covariance matrices. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=20|Lecture p. 20]].

Calculating from those stated values gives

$$
\bar\alpha_{1000}\approx4.03583\times10^{-5},\qquad
\sqrt{\bar\alpha_{1000}}\approx0.00635282,
$$

$$
\sqrt{1-\bar\alpha_{1000}}\approx0.99997982.
$$

Thus $x_T$ has a very small coefficient on the original image and an almost-unit coefficient on noise. These are values derived from the lecture's schedule, not additional settings taken from another source.

If reverse covariance is learned, its log-determinant and quadratic-form terms also depend on $\theta$ and must be retained. The fixed-variance mean-only simplification in §5.5 would no longer describe the entire trainable KL.

## 8. The lecture's comparison with VAEs

The lecture presents both models as an encoding direction toward a Gaussian latent state and a learned decoding direction. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=21|Lecture pp. 21–22]].

| Piece | VAE design illustrated by the lecture | Diffusion design in the lecture |
| --- | --- | --- |
| Encoding | Learned $q_\phi(z\mid x)$ | Fixed noising chain $q(x_{1:T}\mid x_0)$ |
| Decoding | Learned $p_\theta(x\mid z)$ | Learned reverse transitions |
| Gaussian reference | Standard normal latent prior | Standard normal terminal prior |
| Dimensions | A typically lower-dimensional latent code | Each noisy state $x_t$ has the image dimension $d$ |

Two precise readings keep the comparison useful. A smaller VAE latent dimension is a common design choice, not a defining requirement. Also, one diffusion state has dimension $d$, while the full latent path $x_{1:T}$ has dimension $dT$. The [[Learning/Statistical computing & learning/Simulation & approximate inference/VAE and diffusion ELBO - images, hidden paths, and Gaussian KL#4.1 Identify every counterpart of the VAE pieces|whole-path correspondence]] identifies the pieces needed for a direct ELBO comparison.

## 9. Conditional generation and guidance

### 9.1 Add the conditioning information to the reverse model

The earlier model generates unconditionally. To generate according to a label or caption $y$, train on pairs $(x_0,y)$ and use

$$
\boxed{p_\theta(x_{0:T}\mid y)
=p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t,y).}
$$

The transition parameters can depend on $y$:

$$
p_\theta(x_{t-1}\mid x_t,y)
=\mathcal N(\mu_\theta(x_t,t,y),\Sigma_\theta(x_t,t,y)).
$$

The forward corruption can stay unchanged. It does not use $y$ once $x_0$ is given, so

$$
q(x_{t-1}\mid x_t,x_0,y)=q(x_{t-1}\mid x_t,x_0).
$$

Repeating the ELBO derivation with $y$ held fixed gives

$$
\begin{aligned}
L(x_0,y)={}&L_T(x_0)
+\sum_{t=2}^T\mathbb E_{q(x_t\mid x_0)}
D_{\rm KL}(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t,y))\\
&+\mathbb E_{q(x_1\mid x_0)}[-\log p_\theta(x_0\mid x_1,y)].
\end{aligned}
$$

With fixed isotropic reverse covariance, the corresponding simplified objective is noise MSE with $\epsilon_\theta(x_t,t,y)$, averaged over training pairs. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=23|Lecture pp. 23–25]].

### 9.2 Classifier guidance and the covariance-scaled shift

A **score** here means a gradient of log density with respect to the noisy input, such as $\nabla_{x_t}\log p(x_t)$. It is not a classification accuracy score.

The lecture introduces a classifier $p_\phi(y\mid x_t)$ that works on noisy inputs. Its gradient

$$
g_t=\nabla_{x_t}\log p_\phi(y\mid x_t)
$$

points locally toward increased log probability of the desired condition. With reverse mean $\mu$ and covariance $\Sigma$, the lecture's guided transition is

$$
\boxed{x_{t-1}\sim\mathcal N(\mu+s\Sigma g_t,\Sigma).}
$$

The timestep is implicit in the classifier notation; the classifier must be suitable for the current noise level. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=26|Lecture p. 26]].

To see where the covariance factor comes from, consider a Gaussian transition in a variable $u$ and approximate a guiding log likelihood locally by a linear function with gradient $g$:

$$
\log p_{\rm guided}(u)=
-\tfrac12(u-\mu)^T\Sigma^{-1}(u-\mu)+s\,g^T(u-\mu)+C.
$$

Complete the square, assuming $\Sigma$ is positive definite:

$$
\log p_{\rm guided}(u)=
-\tfrac12(u-\mu-s\Sigma g)^T\Sigma^{-1}(u-\mu-s\Sigma g)+C'.
$$

The new mean is $\mu+s\Sigma g$ and the covariance stays $\Sigma$. This identity is exact for a linear log-likelihood tilt. A nonlinear classifier needs a local approximation; the slide's algorithm evaluates its guiding gradient at $x_t$. It is not an exact Bayes posterior update for an arbitrary nonlinear classifier and finite step size.

### 9.3 Derive the classifier-free gradient identity

The next slide avoids a separate classifier by using conditional and unconditional diffusion predictions. Start with full Bayes' rule:

$$
p(y\mid x_t)=\frac{p(x_t\mid y)p(y)}{p(x_t)}.
$$

For a fixed condition $y$, take logs and differentiate with respect to $x_t$:

$$
\begin{aligned}
\nabla_{x_t}\log p(y\mid x_t)
&=\nabla_{x_t}\log p(x_t\mid y)
+\underbrace{\nabla_{x_t}\log p(y)}_{0}
-\nabla_{x_t}\log p(x_t)\\
&=\boxed{\nabla_{x_t}\log p(x_t\mid y)-\nabla_{x_t}\log p(x_t).}
\end{aligned}
$$

This is the lecture's identity. Its proportionality shorthand is safe when treating $y$ as fixed and varying $x_t$; dropping $p(y)$ when comparing different labels would require additional assumptions such as equal label priors. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=27|Lecture p. 27]].

Write the unconditional and conditional scores as $g_u$ and $g_c$. Using an unconditional base score and guidance strength $s$ gives

$$
\boxed{g_s=g_u+s(g_c-g_u)=(1-s)g_u+s g_c.}
$$

This defines the convention used here: $s=0$ is unconditional, $s=1$ is conditional, and $s>1$ extrapolates in the conditional direction. A convention that adds guidance on top of an already conditional base uses a shifted scale; the underlying linear combination should always be stated.

### 9.4 Connect the score identity to the noise network

This fills the algebraic link between slide 27's score notation and slide 16's noise predictor. Let $q_t(x_t\mid y)$ denote the distribution obtained by adding the lecture's Gaussian noise to clean data conditional on $y$.

First differentiate the known forward log density:

$$
\nabla_{x_t}\log q(x_t\mid x_0)
=-\frac{x_t-\sqrt{\bar\alpha_t}x_0}{1-\bar\alpha_t}
=-\frac{\epsilon}{\sqrt{1-\bar\alpha_t}}.
$$

Next differentiate the mixture

$$
q_t(x_t\mid y)=\int q(x_t\mid x_0)q_0(x_0\mid y)\,dx_0.
$$

Assuming differentiation under the integral is justified, divide its derivative by $q_t(x_t\mid y)$ and recognize the posterior weights:

$$
\begin{aligned}
\nabla_{x_t}\log q_t(x_t\mid y)
&=\int q(x_0\mid x_t,y)\nabla_{x_t}\log q(x_t\mid x_0)\,dx_0\\
&=-\frac{\mathbb E[\epsilon\mid x_t,y]}{\sqrt{1-\bar\alpha_t}}.
\end{aligned}
$$

For squared-error training, the ideal predictor is this conditional mean. Indeed, with $m=\mathbb E[\epsilon\mid x_t,y]$,

$$
\mathbb E[\|\epsilon-a\|^2\mid x_t,y]
=\mathbb E[\|\epsilon-m\|^2\mid x_t,y]+\|m-a\|^2,
$$

so the minimum occurs at $a=m$. A trained network approximates it, giving the score estimate

$$
\widehat g_c(x_t,t)=-\frac{\epsilon_\theta(x_t,t,y)}{\sqrt{1-\bar\alpha_t}},
\qquad
\widehat g_u(x_t,t)=-\frac{\epsilon_\theta(x_t,t)}{\sqrt{1-\bar\alpha_t}}.
$$

The denominator is shared at the same timestep. Therefore the score combination corresponds to the noise combination

$$
\boxed{\epsilon_s
=\epsilon_\theta(x_t,t)
+s\big(\epsilon_\theta(x_t,t,y)-\epsilon_\theta(x_t,t)\big).}
$$

Insert $\epsilon_s$ into the reverse mean formula. This derivation uses the lecture's Gaussian forward law, squared-error objective, and Bayes-gradient identity. The ideal identities concern noisy-data scores; finite neural networks only approximate them.

## 10. What conditioning changes, and what it costs

### 10.1 Guidance strength and diversity

![[raw/assets/2026-11-11-Diffusion-lecture-P28-guidance.png]]

*Source figure: complete render of lecture p. 28, unchanged. The slide compares guidance strengths $s=0,1,3$ to illustrate a quality-versus-diversity tradeoff. It is an illustrative comparison, not a universal monotonic performance guarantee.*

Increasing guidance emphasizes outcomes that strongly support the requested condition. It can also concentrate generation on fewer kinds of outcomes. The score equations explain how the direction is strengthened; the pictured quality and diversity effects are empirical illustrations in the lecture. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=28|Lecture p. 28]].

The slide does not specify the base-model convention behind those scale labels; §9.3 states the convention for its own formula.

### 10.2 The condition can be another image

![[raw/assets/2026-11-11-Diffusion-lecture-P29-conditioning-applications.png]]

*Source figure: complete render of lecture p. 29, unchanged; the slide credits Saharia et al. (2022). It shows colorization, inpainting, uncropping, and JPEG restoration, with wider-scene completions on the right.*

The same conditional formulation can use a grayscale image, visible pixels and a mask, a cropped region, or a degraded image as $y$. What changes is the information given to the reverse model. The principle remains learning plausible clean images conditional on that information. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=29|Lecture p. 29]].

### 10.3 The lecture's generative-model tradeoff

![[raw/assets/2026-11-11-Diffusion-lecture-P30-tradeoffs.png]]

*Source figure: complete render of lecture p. 30, unchanged; the slide credits Xiao et al. (2021). Its three aims are sample quality, fast sampling, and broad mode coverage/diversity.*

In the displayed comparison, diffusion emphasizes quality and coverage, while iterative generation makes sampling expensive. The lecture names acceleration as a way to improve the tradeoff but does not derive an accelerated sampler. The triangle is a conceptual comparison of model families, not an impossibility theorem or a current benchmark ranking. [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf#page=30|Lecture pp. 30–31]].

The distinction between the mathematical stages is useful when rereading the derivation:

| Stage | Status |
| --- | --- |
| Forward marginal from independent Gaussian increments | Exact for the specified forward chain |
| Posterior-KL identity and loss decomposition | Exact under the stated support/integrability conditions |
| $q(x_{t-1}\mid x_t,x_0)$ and its Gaussian KL | Exact for the stated Gaussian conditionals |
| Gaussian model for the unknown true reverse | Modeling choice/approximation |
| Sampling data, noise, and timesteps in training | Monte Carlo estimation |
| Setting timestep weights to one | A change of training objective |
| Gaussian guidance mean shift | Exact for a linear tilt; locally approximate for a nonlinear classifier |
| Bayes score difference | Exact for consistent differentiable distributions |
| Network noise/score predictions | Learned approximations |

## Origin

> [!info]- Source details
> Loss-substitution expansion (2026-11-11): at the user's request, the assistant expanded §5.3 from the earlier definition of $L$, explicitly substituted both path factorizations, separated the $t=1$ decoder factor, and applied the logarithm rules. This is checked explanatory algebra, not new lecture text or source ingestion.
>
> Visual extension (2026-11-11): the user requested an SVG or GIF comparison in §2.4. The original static SVG shows exact conditional moments alongside three seeded illustrative trajectories; it is not lecture data or an empirical proof. [[assets/figures/2026-11-11-diffusion-lecture/draw_random_walk_comparison.py|Generator]], [[assets/figures/2026-11-11-diffusion-lecture/random-walk-comparison-data.npz|constructed data]] and [[assets/figures/2026-11-11-diffusion-lecture/random-walk-comparison-checks.json|checks]] are preserved beside the figure. SVG XML parsed and the generated PNG preview visually inspected; no live Obsidian rendering check.
>
> Algebra expansion (2026-11-11): at the user's request, the assistant expanded §5.2's product and crossed out matching marginal-density factors; no new source material was added.
>
> Conversation extension (2026-11-11): at the user's request, §2.4 adds the assistant's explanation of mean shrinkage versus random-walk spreading, two constant-schedule examples, and the distinction between a zero mean and a zero sample. This is explanatory synthesis prompted by the user's follow-up, not additional lecture text; the original lecture attribution below applies to the initial digest.
>
> Sole learning source: [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf|Diffusion Models]], Thibault Randrianarisoa, University of Toronto, Winter 2026; title page dated March 30, 2026. The supplied file is named *Lec12 diffusion models.pdf*. All 32 pages were read and visually inspected for this separate lecture-based digest. Pages 1–2 and 32 provide attribution/reference context; the mathematical and application content runs through pp. 3–31. The listed external papers/tutorials were not separately ingested for this note.
>
> The assistant supplied the intermediate algebra, conditions, and notation clarifications. In particular: equality in distribution for merged Gaussian noise; fixed-schedule conditions for the constant terminal term; the separate $t=1$ endpoint; the distinction between exact and simplified losses; typical versus required VAE dimension; and the retained class prior before the guidance derivative. Section 9.4 explicitly derives the connection between the lecture's noise network and score formula. These expansions are not presented as verbatim slide text or as the user's handwritten work.
>
> The four images are unmodified full-page renders of pp. 5, 28, 29, and 30. The original annotated PDF is preserved byte-for-byte; ambiguous handwritten marginal remarks are not silently reconstructed. [[assets/figures/2026-11-11-diffusion-lecture/render_lecture_pages.py|Rendering source]] and [[assets/figures/2026-11-11-diffusion-lecture/page-render-manifest.json|page-render hashes]] document the recovered figures.
>
> Verification: forward variance telescoping and recursion, reverse factorization, completion of the square, Gaussian KL moments, noise-mean substitution, and Bayes guidance are derived algebraically above. Independent numerical integration and quadrature checks are in [[assets/figures/2026-11-11-diffusion-lecture/verify_derivations.py|the check script]] and [[assets/figures/2026-11-11-diffusion-lecture/derivation-checks.json|results]]. Source and note boundaries are recorded in [[_system/Digest Checkpoints]]. The companion-note links are user-requested inline navigation, not additional source material or new map relationships.
