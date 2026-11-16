---
id: learning-diffusion-scores-noise-guidance
title: Diffusion through scores - noise prediction, sampling, and text guidance
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Selected architectures & latent models]]"
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models
study_band: M elective
note_types: [derivation, insight, topic-note]
source_format: video-transcripts-and-primary-papers
created: 2026-11-15
updated: 2026-11-16
status: active
verification: checked
learning_state: unknown
aliases: [Diffusion score matching to noise MSE, DDIM and the diffusion artist analogy, Text conditioning and negative prompt scores]
tags: [atlas/learning, subject/computing, diffusion, score-matching]
sources:
  - "[[raw/articles/2026-11-15-Outlier-score-diffusion-auto-captions.txt]]"
  - "[[raw/articles/2026-11-15-Outlier-score-diffusion-description.txt]]"
  - "[[raw/articles/2026-11-15-Welch-diffusion-captions.txt]]"
  - "[[raw/articles/2026-11-15-Welch-diffusion-description.txt]]"
  - "[[raw/assets/2026-11-15-Outlier-score-I01-noise-target.png]]"
  - "[[raw/assets/2026-11-15-Outlier-score-I02-dsm-objective.png]]"
  - "https://www.youtube.com/watch?v=B4oHJpEJBAA"
  - "https://www.youtube.com/watch?v=iv-5mZ_9CPY"
  - "https://www.jmlr.org/papers/volume6/hyvarinen05a/hyvarinen05a.pdf"
  - "https://arxiv.org/html/2011.13456v2"
  - "https://arxiv.org/html/2010.02502v4"
  - "https://arxiv.org/html/2207.12598v1"
  - "https://arxiv.org/html/2103.00020v1"
  - "https://arxiv.org/html/2112.10752v2"
  - "https://arxiv.org/html/2204.06125v1"
  - "https://arxiv.org/html/2503.20314v2"
  - "https://arxiv.org/abs/2210.02747"
---

# Diffusion through scores - noise prediction, sampling, and text guidance

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Selected architectures & latent models

**The noise-prediction loss is a way to learn a probability distribution's score using a target we can generate ourselves.** We cannot evaluate the noisy-data density $p_t$ directly, but we know exactly how we corrupt each training image. A conditional-expectation identity turns that known corruption process into supervision for the unknown marginal score:

$$
\underbrace{\nabla_{x_t}\log p_t(x_t)}_{\text{unknown marginal score}}
=
\mathbb E\!\left[
\underbrace{-\frac{\epsilon}{b_t}}_{\text{known training target}}
\ \middle|\ X_t=x_t
\right].
$$

With $s_\theta(x_t,t)=-\epsilon_\theta(x_t,t)/b_t$, this produces the familiar loss

$$
\boxed{\mathcal L_{\mathrm{simple}}
=\mathbb E_{t,X_0,\epsilon}
\left[\|\epsilon-\epsilon_\theta(a_tX_0+b_t\epsilon,t)\|_2^2\right].}
$$

The interesting work is explaining **why the conditional target is valid, which weights were removed, and how a noise predictor becomes a sampler**. Those are the bridges between Outlier's derivation, our earlier notes, and Welch's geometric account of modern image/video generation.

![[assets/figures/2026-11-15-diffusion-scores/01-loss-routes.svg]]

*Original diagram: the ELBO and score-matching routes meet at the same regression target. $A_t,B_t$ denote known schedule coefficients in the reverse mean; their values are given in §6.*

## Reading route through the two videos

| Source | Watch for | Where it enters this note |
| --- | --- | --- |
| [Outlier, 3:13–9:10](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=193s) | Score; remove a normalization constant; integrate by parts | §§1–2 |
| [Outlier, 9:10–21:41](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=550s) | Gaussian corruption; marginalize, differentiate, complete the square | §§3–5, the main loss derivation |
| [Outlier, 24:00–33:58](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=1440s) | Multiple noise levels, SDEs, DDPM | §§7–8; the supplied 24:22 link starts here |
| [Welch, 3:37–8:16](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=217s) | CLIP and shared semantic embeddings | §9 |
| [Welch, 8:16–25:25](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=496s) | Vector fields, randomness, DDPM and **DDIM** | §§7–8 |
| [Welch, 25:25–34:27](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=1525s) | Conditioning, guidance, negative prompts | §§9–12 |

The extra algebra below fills in transitions from the videos. The earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#6. Derive noise prediction from mean prediction|mean-to-noise derivation]] provides the parallel ELBO route.

## 1. What is a score, and why learn it?

For a differentiable positive density $p(x)$ on $\mathbb R^d$, its **data score** is the vector

$$
s(x)=\nabla_x\log p(x)\in\mathbb R^d.
$$

It measures the local direction and rate of increase of log density. Here the derivative is with respect to the **image or latent coordinates $x$**, not model parameters.

Suppose we express a model as an energy-based density,

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},
\qquad
Z_\theta=\int_{\mathbb R^d}e^{-E_\theta(u)}\,du.
$$

The normalizing integral can be expensive, but it does not depend on $x$:

$$
\nabla_x\log p_\theta(x)
=\nabla_x[-E_\theta(x)-\log Z_\theta]
=-\nabla_xE_\theta(x).
$$

**Technique 1: differentiate with respect to a variable that eliminates the troublesome constant.** Higher energy means lower density under this sign convention. Alternatively, train a vector network $s_\theta(x)$ directly; such a network is not automatically the gradient of a globally normalized density.

This is the role of the score in [Outlier's score chapter](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=193s), also explained in [Yang Song's score-model introduction](https://yang-song.net/blog/2021/score/).

## 2. First route to a computable objective: integration by parts

Start with an ideal squared-error objective:

$$
J(\theta)=\frac12\mathbb E_{X\sim p}
\|s_\theta(X)-\nabla\log p(X)\|^2.
$$

We can draw data from $p$, but cannot evaluate its score. Expanding the square isolates the troublesome cross term:

$$
J(\theta)
=\frac12\mathbb E_p\|s_\theta\|^2
-\sum_{i=1}^d\int s_{\theta,i}(x)\,\partial_i p(x)\,dx
+C,
$$

where $C=\tfrac12\mathbb E_p\|\nabla\log p\|^2$ is independent of $\theta$. The factor $p$ disappears from the cross term because $p\,\nabla\log p=\nabla p$.

For each coordinate, integration by parts gives

$$
\int s_{\theta,i}\,\partial_i p\,dx
=\underbrace{\text{boundary term}}_{0}
-\int p\,\partial_i s_{\theta,i}\,dx.
$$

Thus

$$
\boxed{
J(\theta)=
\mathbb E_p\!\left[
\frac12\|s_\theta(X)\|^2+
\nabla\cdot s_\theta(X)
\right]+C,
}
\qquad
\nabla\cdot s_\theta=\sum_{i=1}^d\frac{\partial s_{\theta,i}}{\partial x_i}.
$$

**Technique 2: move a derivative from an unknown density onto a known model.** The divergence is the **trace of the Jacobian**, not its norm.

This requires sufficient differentiability, finite expectations, and vanishing boundary flux of $p\,s_\theta$; $p(x)\to0$ alone is not the whole boundary condition. [Hyvärinen (2005), Theorem 1, p. 697; proof in Appendix A](https://www.jmlr.org/papers/volume6/hyvarinen05a/hyvarinen05a.pdf).

The two terms are optimized together. This does not say to set the score to zero at every observed point: data points need not be modes, and zero gradient alone does not establish a maximum.

For image-sized $d$, computing the divergence can be expensive. There is also little direct supervision far from the data. Gaussian corruption gives a second route that supplies an explicit target and covers surrounding space.

## 3. Known corruption kernel, unknown noisy-data density

Use one notation for both videos and the DDPM notes:

$$
X_0\sim p_0,\qquad
\epsilon\sim\mathcal N(0,I_d),\quad \epsilon\perp X_0,
\qquad
X_t=a_tX_0+b_t\epsilon,\quad b_t>0.
$$

| Quantity | Meaning |
| --- | --- |
| $X_0$ | Clean data, an image or a compressed image/video latent |
| $a_t$ | Known signal multiplier |
| $b_t$ | Standard deviation of accumulated forward noise |
| $\epsilon$ | Standard normal noise; $\delta_t=b_t\epsilon$ is the actual added perturbation |
| $q_t(y\mid x_0)$ | Known corruption density $\mathcal N(y;a_tx_0,b_t^2I_d)$ |
| $p_t(y)$ | Marginal density after corrupting the whole data distribution |
| $s_t(y)$ | Marginal score $\nabla_y\log p_t(y)$ |

For Outlier's additive Gaussian setup, $a_t=1$ and $b_t=\sigma_t$. For the usual DDPM setup,

$$
a_t=\sqrt{\bar\alpha_t},\qquad
b_t=\sqrt{1-\bar\alpha_t},\qquad
\alpha_t=1-\beta_t,\quad
\bar\alpha_t=\prod_{j=1}^t\alpha_j.
$$

This is our existing [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#2.3 Extend to an arbitrary timestep|closed-form forward process]].

The key distinction is

$$
\underbrace{q_t(y\mid x_0)}_{\text{known Gaussian for one clean example}}
\quad\text{versus}\quad
\underbrace{p_t(y)=\int p_0(x_0)q_t(y\mid x_0)\,dx_0}_{\text{unknown mixture over all clean examples}}.
$$

Adding Gaussian noise does not generally make the marginal $p_t$ a single Gaussian. It smooths the data distribution. If $p_0$ has no density, the integral can instead be taken with respect to its probability measure.

## 4. The central derivation: replace the marginal score by a conditional score

At a fixed $t$, define the computable teacher

$$
r_t(y,x_0)=\nabla_y\log q_t(y\mid x_0).
$$

We want to show that matching $r_t(X_t,X_0)$ has the same $\theta$-dependent objective as matching $s_t(X_t)$. This expands [Outlier's denoising-score-matching chapter, starting at 12:33](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=753s).

### 4.1 Follow the cross term, one equality at a time

Write

$$
J_{\mathrm{marg}}(\theta)
=\frac12\mathbb E_{p_t}\|s_\theta(X_t,t)-s_t(X_t)\|^2.
$$

Its cross term is

$$
\begin{aligned}
K_\theta
&=\int p_t(y)\,s_\theta(y,t)^\top\nabla_y\log p_t(y)\,dy\\
&=\int s_\theta(y,t)^\top\nabla_y p_t(y)\,dy
&&[p_t\nabla\log p_t=\nabla p_t]\\
&=\int s_\theta(y,t)^\top
\nabla_y\!\left[\int p_0(x_0)q_t(y\mid x_0)\,dx_0\right]dy
&&[\text{marginalize }X_0]\\
&=\iint p_0(x_0)\,s_\theta(y,t)^\top
\nabla_yq_t(y\mid x_0)\,dx_0\,dy
&&[\text{differentiate under the integral}]\\
&=\iint p_0(x_0)q_t(y\mid x_0)\,
s_\theta(y,t)^\top r_t(y,x_0)\,dx_0\,dy
&&[\nabla q_t=q_t\nabla\log q_t]\\
&=\mathbb E_{X_0,X_t}\!\left[s_\theta(X_t,t)^\top r_t(X_t,X_0)\right].
\end{aligned}
$$

**Technique 3: expand the marginal, move the derivative inside, then recognize a joint expectation.** The interchange needs regularity such as an integrable dominating derivative; assume the displayed integrals and squared-score expectations exist.

The model-only term also satisfies

$$
\mathbb E_{X_t}\|s_\theta(X_t,t)\|^2
=\mathbb E_{X_0,X_t}\|s_\theta(X_t,t)\|^2.
$$

Now add and subtract $\tfrac12\mathbb E\|r_t\|^2$:

$$
\begin{aligned}
J_{\mathrm{marg}}(\theta)
&=\frac12\mathbb E\|s_\theta\|^2-\mathbb E[s_\theta^\top r_t]
+\frac12\mathbb E\|s_t\|^2\\
&=\underbrace{\frac12\mathbb E\|s_\theta-r_t\|^2}_{J_{\mathrm{DSM}}(\theta)}
+\underbrace{\frac12\mathbb E\|s_t\|^2-\frac12\mathbb E\|r_t\|^2}_{C_t\text{ independent of }\theta}.
\end{aligned}
$$

**Technique 4: complete a squared error by adding a parameter-independent term.** The losses have the same minimizers and gradients in $\theta$, but their numerical values differ by a constant. The video's shortened equality should be read with this constant retained.

### 4.2 The same result as a conditional-expectation identity

Bayes' rule also gives a compact interpretation:

$$
\begin{aligned}
\mathbb E[r_t(y,X_0)\mid X_t=y]
&=\int \frac{p_0(x_0)q_t(y\mid x_0)}{p_t(y)}
\nabla_y\log q_t(y\mid x_0)\,dx_0\\
&=\frac{\nabla_y p_t(y)}{p_t(y)}
=s_t(y).
\end{aligned}
$$

The computable teacher is noisy, but its conditional average is exactly the desired score. Therefore

$$
J_{\mathrm{DSM}}(\theta)
=J_{\mathrm{marg}}(\theta)
+\frac12\mathbb E\|r_t(X_t,X_0)-s_t(X_t)\|^2.
$$

The cross term vanishes after conditioning on $X_t$. This is the squared-error projection identity underlying the earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9.4 Connect the score identity to the noise network|score/noise connection]].

## 5. Differentiate the Gaussian, then obtain noise MSE

The Gaussian log density is

$$
\log q_t(y\mid x_0)
=-\frac d2\log(2\pi b_t^2)
-\frac{\|y-a_tx_0\|^2}{2b_t^2}.
$$

Differentiate with respect to $y$:

$$
r_t(y,x_0)
=-\frac{y-a_tx_0}{b_t^2}.
$$

Since $y=a_tx_0+b_t\epsilon$,

$$
\boxed{r_t(X_t,X_0)=-\frac{\epsilon}{b_t}.}
$$

Careful translation between notations: **actual perturbation** $\delta_t=b_t\epsilon$ gives $r_t=-\delta_t/b_t^2$; **standard normal noise** $\epsilon$ gives $r_t=-\epsilon/b_t$. Confusing these loses one power of the standard deviation.

Choose a noise-prediction parameterization:

$$
s_\theta(y,t)=-\frac{\epsilon_\theta(y,t)}{b_t}.
$$

Substitution now does all the work:

$$
\begin{aligned}
J_{\mathrm{DSM},t}(\theta)
&=\frac12\mathbb E\left\|-\frac{\epsilon_\theta}{b_t}
+\frac{\epsilon}{b_t}\right\|^2\\
&=\boxed{\frac{1}{2b_t^2}\mathbb E
\|\epsilon-\epsilon_\theta(X_t,t)\|^2.}
\end{aligned}
$$

At a fixed $t$, the prefactor does not change the minimizer. Across timesteps, it changes the relative importance of noise levels. For

$$
\mathcal J(\theta)=\mathbb E_t[\lambda(t)J_{\mathrm{DSM},t}(\theta)],
$$

choosing $\lambda(t)=b_t^2$ yields half the simple noise MSE. Removing the global factor $1/2$ leaves the boxed opening objective. Other timestep sampling distributions and weights define different objectives for a shared finite-capacity network. [Song et al., §2.1 and §3.3, conditional score targets and weighting](https://arxiv.org/html/2011.13456v2).

**The training label is available because we sampled $\epsilon$ ourselves.** A batch constructs $x_t=a_tx_0+b_t\epsilon$, predicts $\epsilon_\theta(x_t,t)$, and evaluates MSE; it does not simulate all earlier noising steps. See the existing [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code#4.2 Generate the supervised pair|supervised-pair code]] and [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code#4.3 What exactly is minimized?|MSE reduction]].

At the population optimum, over unrestricted measurable predictors,

$$
\epsilon^*(y,t)=\mathbb E[\epsilon\mid X_t=y],
\qquad
s_t(y)=-\frac{\epsilon^*(y,t)}{b_t}.
$$

The network estimates a conditional average, not the unknowable identity of the particular noise draw that produced a new input.

## 6. Where this meets the ELBO derivation

In the DDPM notation, the reverse teacher mean and model mean are

$$
\widetilde\mu_t
=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{b_t}\epsilon\right),
\qquad
\mu_\theta
=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{b_t}\epsilon_\theta\right).
$$

Thus the diagram's coefficients are $A_t=1/\sqrt{\alpha_t}$ and $B_t=\beta_t/(\sqrt{\alpha_t}b_t)$. For a fixed reverse covariance $\rho_t^2I_d$ and an intermediate step $t\ge2$, the $\theta$-dependent part of the Gaussian KL is

$$
\frac1{2\rho_t^2}\|\widetilde\mu_t-\mu_\theta\|^2
=
\boxed{
\frac{\beta_t^2}
{2\rho_t^2\alpha_t(1-\bar\alpha_t)}
\|\epsilon-\epsilon_\theta(x_t,t)\|^2.
}
$$

That is the earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.5 Calculate the Gaussian KL instead of sampling its inner variable|Gaussian-KL calculation]], followed by the same noise parameterization.

| Route | Initially inaccessible object | What makes it trainable |
| --- | --- | --- |
| ELBO / reverse transition | Reverse distribution without knowing $X_0$ | During training, condition on $X_0$ and evaluate the Gaussian teacher |
| Score matching | $\nabla\log p_t(x_t)$ of the unknown noisy-data mixture | Use the known Gaussian-kernel score; its posterior average is the marginal score |

Both routes supervise accumulated forward noise. Their default timestep weights need not agree. The full ELBO also has endpoint terms, including the $t=1$ reconstruction term; it is not literally just the unweighted MSE.

## 7. The diffusion artist: coarse structure, uncertainty, then detail

The artist analogy is useful when it means **successive decisions at different noise scales**. At high noise, fine distinctions between plausible images are obscured. As the noise level falls, the learned field can distinguish narrower possibilities: a broad layout, an object shape, then local texture. This is an organizing intuition, not a guarantee that every model fixes all global structure before any detail.

In the additive setup, $p_\sigma=p_0*\mathcal N(0,\sigma^2I)$ is a smoothed density. In the DDPM setup, divide by $a_t>0$ to see the effective noise level $b_t/a_t$. Large effective noise smooths away distinctions; smaller noise reveals them.

![[assets/figures/2026-11-15-diffusion-scores/03-score-scales.gif|620]]

*Original analytic illustration, not generated images or a particle simulation: a three-component Gaussian mixture is progressively less smoothed. Blue arrows show score **directions only**; orange crosses mark clean component centers. Axes are fixed. Density colors are scaled relative to each frame's peak, so color intensity cannot be compared as an absolute density across frames.*

![[assets/figures/2026-11-15-diffusion-scores/02-score-scales.svg]]

*Static keyframes: broad structure → distinct alternatives → local structure. The GIF changes the density and its score field, not the positions of sampled images.*

### Reading the GIF: one point, one distribution, many directions

> [!important] The whole plot is not one photograph
> **Yes, the blue arrows form a score-direction field.** The green background shows the corresponding noisy-data density. One location stands for one complete possible image/state; the whole plot describes a distribution over many such states. The orange crosses are **three cluster means**, not three individual photographs. This particular illustration contains no actual photographs or moving sample points.

>[!info]- One point represents a whole image, not a pixel inside it
>
>Imagine a tiny grayscale image with four pixel intensities:
>
>$$
>\begin{pmatrix}0.2&0.8\\0.1&0.9\end{pmatrix}
>\quad\longleftrightarrow\quad
>x=(0.2,0.8,0.1,0.9)\in\mathbb R^4.
>$$
>
>The **whole four-pixel image is one point in four-dimensional image space**. Changing its coordinates changes its pixels. Likewise, a $64\times64$ RGB image is one point with $64\cdot64\cdot3=12{,}288$ coordinates. In latent diffusion, one point is instead a complete latent tensor, which a decoder maps to an image.
>
>Our figure replaces that large space with an invented two-dimensional space so we can draw it. “Coordinate 1” and “coordinate 2” are **not the horizontal and vertical positions of pixels inside a photograph**, nor verified semantic axes such as “catness” and “dogness.” The figure is not a projection computed from real images.
>
>A point is a **possible state**, not automatically a meaningful picture. A training image, a noisy image and a generated image can all be represented as points. Clean, plausible images are what the data distribution models; a noisy sampling state need not yet look meaningful. This toy distribution has no actual visual semantics.

#### A legend for everything visible

| Visible object | What it represents | What it does **not** mean |
| --- | --- | --- |
| The square coordinate plane | A window onto possible two-coordinate states $x$ | One photograph's pixel canvas |
| Green shading | The scalar density $p_\sigma(x)$; darker means higher density **within this frame** | Image brightness, image quality, or the probability of one exact point |
| All blue arrows together | The direction field of $s_\sigma(x)=\nabla_x\log p_\sigma(x)$ | A collection of generated images or their actual trajectories |
| One blue arrow at $x$ | Which small change of this state increases log density fastest, using Euclidean distance | An object inside the picture moving in that compass direction |
| An orange cross $\mu_k$ | The mean of one clean Gaussian cluster; many different sample points can lie around it | One stored training photograph, a guaranteed mode at every noise level, or a mandatory final destination |
| A GIF frame or static panel | The density and directions at **one noise scale** | A different photograph, or one stage of an individual photograph's trajectory |

For this continuous toy, probabilities belong to regions: $P(X_\sigma\in A)=\int_A p_\sigma(x)\,dx$. White regions still have positive Gaussian-tail density; they fall below the plotted color threshold. Because colors are renormalized separately in each frame, equally dark greens in different panels need not have equal density.

#### What does an arrow's direction tell me to change?

At a fixed noise level,

$$
s_\sigma(x)=
\left(\frac{\partial\log p_\sigma(x)}{\partial x_1},
\frac{\partial\log p_\sigma(x)}{\partial x_2}\right).
$$

- **Right / left:** increase / decrease coordinate 1.
- **Up / down:** increase / decrease coordinate 2.
- **Diagonal:** change both coordinates in the indicated proportions.

Thus “up and right” means a joint edit of the represented state, not “move the photographed object up and right.” In full pixel space, the analogous vector has one entry per pixel-channel value: positive entries suggest brightening those channels and negative entries suggest darkening them, for a small step. In latent space, the edits act on latent coordinates instead.

For a unit direction $u$ and small positive $h$,

$$
\log p_\sigma(x+hu)-\log p_\sigma(x)
=h\,s_\sigma(x)^\top u+O(h^2).
$$

When the score is nonzero, this first-order increase is greatest for $u=s_\sigma(x)/\|s_\sigma(x)\|$. That is the direction drawn. **The arrows have normalized lengths**, so their displayed lengths do not tell us how large the true gradient or a sampler's step is. This is a data-coordinate score, not an image-quality rating or the parameter score $\nabla_\theta\log p_\theta(x)$. See [Song's explanation of the data score](https://yang-song.net/blog/2021/score/#the-score-function-score-based-models-and-score-matching).

#### Why do arrows sometimes point between the orange centers?

The clean toy distribution consists of three **small clouds**, not three isolated data points. Adding Gaussian noise broadens each cloud. When they overlap strongly, the score combines their contributions: it does not simply identify the nearest cross and point straight at it. At low noise, one nearby component often dominates, so arrows look like attraction toward that component's center.

> [!example]- The exact mixture behind this picture
> The generator uses means $\mu_1=(-1.45,-0.8)$, $\mu_2=(1.45,-0.8)$ and $\mu_3=(0,1.35)$, weights $(w_1,w_2,w_3)=(0.35,0.35,0.30)$, and clean within-component standard deviation $\tau=0.12$ in each coordinate. With $v_\sigma=\tau^2+\sigma^2$,
>
> $$
> p_\sigma(x)=\sum_{k=1}^3 w_k\,\mathcal N(x;\mu_k,v_\sigma I_2),
> \qquad
> r_k(x,\sigma)=\frac{w_k\mathcal N(x;\mu_k,v_\sigma I_2)}{p_\sigma(x)}.
> $$
>
> Differentiating each Gaussian and dividing by the mixture density gives
>
> $$
> s_\sigma(x)
> =\frac{\sum_k w_k\mathcal N(x;\mu_k,v_\sigma I_2)(\mu_k-x)/v_\sigma}{p_\sigma(x)}
> =\sum_k r_k(x,\sigma)\frac{\mu_k-x}{v_\sigma}
> =\frac{\sum_k r_k(x,\sigma)\mu_k-x}{v_\sigma}.
> $$
>
> Each component contributes an arrow toward its own mean, weighted by how well that component explains the current $x$. These weights depend on both location and noise. Their combined arrow can point between the means. For one Gaussian alone, $s(x)=(\mu-x)/v$: a point left of its mean is directed rightward, and a point above it downward.
>
> A component mean is not necessarily a mode of the **combined** density. Also, the weighted mean of component centers in the last formula is not generally $\mathbb E[X_0\mid X_\sigma=x]$: the clean clusters themselves have nonzero spread. The clean-state conditional mean is $x+\sigma^2s_\sigma(x)$, as §7.1 explains.

So “does each center represent a picture?” is **not quite right for this figure**. A center summarizes a cluster of states. To imagine an image analogue, think of a cloud of related pictures rather than one photograph pinned to each cross; the three clouds here are not assigned real image classes. Only in a different toy that explicitly places one noise kernel on each individual training example would every kernel center denote a training picture.

#### What each panel means, from left to right

| Panel | Read the density and arrows this way |
| --- | --- |
| **Left: $\sigma=2.00$ — broad structure** | Noise has spread the three clouds so widely that they form one broad mound. Arrows mostly favor the central region of the combined distribution, not three separately resolved destinations. The orange crosses still mark the unchanged **clean** means. |
| **Middle: $\sigma=0.80$ — separate possibilities** | The clouds overlap less, and three lobes become visible. Directions distinguish alternative regions more clearly; between them, contributions can compete or cancel. |
| **Right: $\sigma=0.15$ — local structure** | Three compact neighborhoods are well separated. Nearby arrows mostly point toward the corresponding cluster. Each neighborhood still contains many possible points: the clean spread $\tau=0.12$ remains, and $\sigma=0.15$ is not zero. |

The GIF smoothly lowers $\sigma$ between these regimes while keeping the axes, orange centers and arrow-query locations fixed. **The directions at those locations change; no image-particle is being followed.** Its loop back to high noise is simply animation playback, not a step of a sampler. “Broad to fine” here means resolving the structure of a probability distribution, not literally demonstrating pixels or textures appearing.

#### The whole field versus one generated picture

The whole field describes the score of the **entire noisy-data distribution at the current noise level**, not the noise distribution around one known clean picture. It is a rule defined across possible inputs, rather than a display of the finite training dataset. In this toy it is calculated exactly; a real diffusion network approximates that rule and evaluates it at the current noisy image/latent.

To illustrate **one generated picture**, we would have to add a moving dot $x_t$. A sampler would update that dot using the score, schedule and its chosen stochastic or deterministic rule; rendering or decoding the dot's state would show the evolving picture. Repeating this with different initial draws would produce a collection of samples. **The goal is to sample a distribution, not force every dot onto an orange center.** The arrows alone are not a complete sampler; §8 distinguishes score directions from the actual update dynamics.

### 7.1 Why a clean-image estimate can look like a rough painting

Rearrange the score identity for $a_t>0$:

$$
s_t(y)
=-\frac{y-a_t\mathbb E[X_0\mid X_t=y]}{b_t^2},
\qquad
\boxed{
\mathbb E[X_0\mid X_t=y]
=\frac{y+b_t^2s_t(y)}{a_t}.
}
$$

At large noise, many clean images explain the same $y$. Their posterior mean may average incompatible details: differently positioned edges or textures can blur together. As uncertainty decreases, that conditional estimate can become more specific. This extends the existing [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#6.2 Let the network predict noise|conditional-mean interpretation]].

There are also two different objects one might display during sampling: the current noisy state $x_t$, and the model's clean-image estimate $\widehat x_0$. A sequence of increasingly refined $\widehat x_0$ previews need not mean the sampler repeatedly has a clean painting and then damages it.

### 7.2 What adding noise actually contributes

| Randomness | Role |
| --- | --- |
| Forward noise during training | Creates supervised denoising problems at many uncertainty levels |
| Initial sampling noise $x_T$ | Supplies the random seed from which different outputs can be generated |
| Fresh noise inside a stochastic sampler | Supplies the diffusion part of that sampler's transition; together with its drift, maintains the intended evolving distribution |

For a stochastic sampler, small perturbations can change which plausible completion is pursued. The learned field then supplies structure at the next scale. This supports an artist-like picture of exploring alternatives while refining the work.

**Noise itself does not contain semantic detail, and adding more noise does not monotonically improve detail.** DDIM can produce detailed images without fresh random draws after initialization. Detail comes from the learned distribution and a consistent sequence of updates; randomness is one way to traverse that distribution.

Welch's [noise-removal experiment, 18:58–24:54](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=1138s) is about changing a particular sampler. His description adds a proposed explanation for the blurry example: removing DDPM noise can make the next input inconsistent with the noise level expected by the denoiser. The spiral illustration also shows reduced diversity.

### 7.3 Why predicting accumulated noise can be easier than a particular last step

For the simplified equal-increment random walk $Y_n=x_0+\sum_{k=1}^n\delta_k$, with iid Gaussian $\delta_k\sim\mathcal N(0,\sigma^2I)$,

$$
\mathbb E[\delta_n\mid Y_n,x_0]=\frac{Y_n-x_0}{n},
\qquad
\operatorname{Var}(\delta_n\mid Y_n,x_0)
=\sigma^2\left(1-\frac1n\right)I.
$$

Knowing the total displacement still leaves uncertainty about the last increment. Using the whole corruption as a regression target avoids pretending to recover one particular random path. Welch's random-walk discussion makes this geometry visible. The simple $1/n$ coefficient belongs to this equal-increment toy; DDPM's attenuated, unequal increments require its actual schedule coefficients.

## 8. Sampling: the vector field and randomness must fit together

### 8.1 A score direction alone is not a sampling algorithm

At a fixed noise level, Langevin dynamics uses

$$
Y_{k+1}=Y_k+h\,s_t(Y_k)+\sqrt{2h}\,Z_k,
\qquad Z_k\sim\mathcal N(0,I_d).
$$

The corresponding continuous-time process has invariant density $p_t$ under regularity and boundary conditions; finite Euler steps introduce error and require adequate mixing. Dropping the random term gives gradient ascent on $\log p_t$, which generally seeks modes rather than distributing points according to $p_t$. Annealed Langevin sampling repeats this idea across decreasing noise levels. [Outlier, sampling and multiple perturbations](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=1301s).

### 8.2 Reverse SDE versus probability-flow ODE

For a forward SDE with scalar, state-independent diffusion coefficient $g(t)$,

$$
dX_t=f(X_t,t)\,dt+g(t)\,dW_t,
$$

the corresponding reverse SDE is

$$
dX_t=[f(X_t,t)-g(t)^2s_t(X_t)]\,dt+g(t)\,d\overline W_t,
\qquad t:T\downarrow0.
$$

Here $dt$ is negative, and the reversed Wiener increment has covariance $|dt|I$. The probability-flow ODE is instead

$$
\boxed{
dX_t=\left[f(X_t,t)-\frac12g(t)^2s_t(X_t)\right]dt.
}
$$

With exact scores, matching initial marginals, and regularity, these processes share the prescribed one-time marginal distributions. Their trajectories differ. Approximate networks and numerical solvers do not inherit an exact equality guarantee. [Song et al., §3.2 and §4.3](https://arxiv.org/html/2011.13456v2).

The changed coefficient matters: removing the random term from the reverse SDE leaves a full $g^2s_t$, whereas the probability-flow ODE uses **half** that correction.

> [!example]- Why the factor one-half appears
> The forward SDE's density follows the Fokker–Planck equation:
>
> $$
> \partial_t p_t=-\nabla\cdot(fp_t)+\frac{g(t)^2}{2}\Delta p_t.
> $$
>
> Since $\nabla p_t=p_ts_t$,
>
> $$
> \partial_t p_t
> =-\nabla\cdot\left[\left(f-\frac{g(t)^2}{2}s_t\right)p_t\right].
> $$
>
> This is the continuity equation for the stated deterministic velocity. The same density evolution can therefore be represented by a different drift with no diffusion term.
>
> A one-dimensional check: forward Brownian motion with $X_t\sim\mathcal N(0,v_0+t)$ has $s_t(x)=-x/(v_0+t)$. In increasing reverse time, the reverse SDE's variance rate at the target law is $-2+1=-1$; the correct ODE gives $-1$. Simply deleting the SDE noise gives $-2$, so the variance contracts too fast.

For the variance-preserving DDPM limit, $f(x,t)=-\tfrac12\beta(t)x$ and $g(t)=\sqrt{\beta(t)}$. This follows from

$$
x_{t+\Delta t}=\sqrt{1-\beta(t)\Delta t}\,x_t+
\sqrt{\beta(t)\Delta t}\,z,
\qquad
\sqrt{1-\beta\Delta t}=1-\tfrac12\beta\Delta t+O(\Delta t^2).
$$

This is a continuous-time limit, not an assertion that every finite DDPM update equals an Euler step exactly. Outlier connects these views at [31:36](https://www.youtube.com/watch?v=B4oHJpEJBAA&t=1896s).

### 8.3 DDIM changes the update, not just the random seed

**DDIM** means *denoising diffusion implicit models*; it is the method called “DIM” in the learning request.

Given $\widehat\epsilon=\epsilon_\theta(x_t,t)$, first estimate

$$
\widehat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\,\widehat\epsilon}
{\sqrt{\bar\alpha_t}}.
$$

For a selected earlier time $s<t$, a DDIM-family step is

$$
\boxed{
x_s=\sqrt{\bar\alpha_s}\,\widehat x_0
+\sqrt{1-\bar\alpha_s-\rho_{t\to s}^2}\,\widehat\epsilon
+\rho_{t\to s}z,
}
$$

where $z\sim\mathcal N(0,I)$ and, for $0\le\eta\le1$,

$$
\rho_{t\to s}
=\eta
\sqrt{\frac{1-\bar\alpha_s}{1-\bar\alpha_t}}
\sqrt{1-\frac{\bar\alpha_t}{\bar\alpha_s}}.
$$

- $\eta=0$: deterministic after $x_T$ is chosen; the middle coefficient becomes $\sqrt{1-\bar\alpha_s}$.
- $\eta=1$ and $s=t-1$: recovers the DDPM posterior-variance choice $\widetilde\beta_t$.
- Skipping times allows fewer network evaluations; approximation error and quality depend on the model, schedule and solver.

The middle coefficient changes together with the random-noise coefficient. Setting only the last term to zero in an unchanged DDPM rule does not implement DDIM. The DDIM paper writes $\alpha_t$ for what this note calls $\bar\alpha_t$. [DDIM, §4.1 Eq. (12), §5 Eq. (16)](https://arxiv.org/html/2010.02502v4).

DDIM is a discrete non-Markovian construction related to the ODE viewpoint. “DDIM,” “probability-flow ODE,” and “any deterministic sampler” are not interchangeable names. The existing [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code#5. Sampling turns the noise prediction into a reverse step|DDPM sampling code]] is a useful concrete comparison.

## 9. Text embeddings and image latents serve different purposes

Welch first builds a language–vision bridge with [CLIP, 3:37–8:16](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=217s). CLIP learns an image encoder and a text encoder from matched image–caption pairs. In a batch, normalized embeddings form an image-by-text similarity matrix; the correct pairs lie on its diagonal. A symmetric contrastive cross-entropy objective rewards the matched pair relative to mismatched pairs.

For example, the image-to-text half has

$$
\ell_i=-\log
\frac{\exp(u_i^\top v_i/\tau)}
{\sum_j\exp(u_i^\top v_j/\tau)},
$$

where $u_i$ is an image embedding, $v_j$ a text embedding, and $\tau>0$ a temperature. The text-to-image half swaps the retrieval direction. [CLIP, §2.3 and Figure 3](https://arxiv.org/html/2103.00020v1).

An embedding is a learned representation, not a universal dictionary of exact semantic axes. Vector differences such as “with a hat” minus “without a hat” are useful intuition, but need not isolate a pure, context-independent “hat vector.”

| Representation | Purpose in generation | Usually carries |
| --- | --- | --- |
| Text condition $c$ | Describe the requested content | A sequence of contextual token vectors |
| CLIP image embedding | Align visual semantics with text | A semantic summary of an image |
| VAE image/video latent $z_0$ | Compress data while retaining information needed by a decoder | Spatial, and for video often temporal, structure |
| Noisy latent $z_t$ | State being updated by the diffusion/flow sampler | Compressed signal plus scheduled noise |

A CLIP embedding and a VAE latent are different objects. Welch's visible noise videos were decoded through a VAE, as his description notes; the underlying diffusion state was compressed.

Two useful pipeline examples:

- **DALL·E 2 / unCLIP:** text → a prior that predicts a CLIP image embedding → a diffusion decoder conditioned on that embedding. This is not an exact inverse of the CLIP image encoder. [unCLIP, abstract and §2](https://arxiv.org/html/2204.06125v1).
- **Latent diffusion:** encode a training image into $z_0$, train diffusion in latent space, then decode the sampled final latent. Text features condition the denoiser, often through cross-attention. [Latent Diffusion Models, §§3.1–3.3](https://arxiv.org/html/2112.10752v2).

The video's 512-dimensional CLIP example is not a universal input specification. Text conditioning often uses a **sequence** of token embeddings rather than one pooled vector, and modern systems may use other text encoders.

## 10. Conditioning: information enters the denoiser

The conditional training objective is

$$
\mathbb E_{(X_0,C),t,\epsilon}
\|\epsilon-\epsilon_\theta(a_tX_0+b_t\epsilon,t,C)\|^2.
$$

For latent diffusion, replace $X$ by $Z$. The derivation in §§3–5 works inside each condition:

$$
s_t(x\mid c)
=\nabla_x\log p_t(x\mid c)
=-\frac{\mathbb E[\epsilon\mid X_t=x,C=c]}{b_t}.
$$

Conditioning changes which distribution's score is learned. Time $t$ tells the network the noise level; text, a class label, or another image tells it what kind of sample to model. This extends the earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9.1 Add the conditioning information to the reverse model|conditional reverse model]].

One common mechanism is cross-attention. With $n$ spatial tokens and $m$ text tokens,

$$
Q\in\mathbb R^{n\times d_k},\quad
K\in\mathbb R^{m\times d_k},\quad
V\in\mathbb R^{m\times d_v},
\qquad
\operatorname{Attn}(Q,K,V)=
\operatorname{softmax}_{\mathrm{row}}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
$$

Image/latent features supply queries; text features supply keys and values. Each spatial position gets a weighted combination of text values. Addition, concatenation and adaptive normalization are other conditioning mechanisms. The time embedding is a separate input, like the existing [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code#2. Why does time need its own branch?|time branch]].

![[assets/figures/2026-11-15-diffusion-scores/04-conditioning-flow.svg]]

*Original inference diagram for a latent, noise-prediction model. Both denoiser calls receive the same $z_t$ and $t$, but different text conditions. An empty condition gives ordinary classifier-free guidance; a negative prompt changes the baseline branch. The sampler also uses the current state and schedule. Decode to an image after the sampling loop.*

A U-Net is one implementation of the function $\epsilon_\theta$; a diffusion transformer is another. The U-Net's down/up path happens **within one model evaluation**. It is distinct from the many timesteps of the sampling loop; see [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion in PyTorch - why U-Net and how the formulas become code#1. Why go down, come up, and connect across?|U-Net feature scales]].

## 11. Guidance: use a difference of scores to strengthen a condition

Conditioning and guidance happen at different places. Conditioning supplies $c$ to a model call. Guidance modifies the prediction used for sampling, often by combining multiple calls. An exact conditional score already defines conditional sampling; extra guidance is a practical method for changing adherence, fidelity and diversity, not a mathematical prerequisite for any conditional generation.

### 11.1 Bayes' rule explains the direction difference

At fixed $t$,

$$
\log p_t(x\mid c)=\log p_t(x)+\log p_t(c\mid x)-\log p(c).
$$

Taking $\nabla_x$ gives

$$
\boxed{
s_c(x,t)-s_u(x,t)=\nabla_x\log p_t(c\mid x),
}
$$

where $s_c=\nabla_x\log p_t(x\mid c)$ and $s_u=\nabla_x\log p_t(x)$. The difference isolates how the condition changes the score. This is the earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9.3 Derive the classifier-free gradient identity|Bayes score identity]].

**Classifier guidance** estimates the right-hand side with a classifier trained on noisy inputs. **Classifier-free guidance (CFG)** uses conditional and unconditional generative predictions instead. The latter can come from one network trained with the condition randomly dropped on some examples. [Classifier-Free Diffusion Guidance, §3.2 and Algorithms 1–2](https://arxiv.org/html/2207.12598v1).

### 11.2 Fix the guidance convention before interpreting the scale

Use

$$
s_{\mathrm{cfg}}=s_u+w(s_c-s_u).
$$

| $w$ | Result |
| --- | --- |
| $0$ | Unconditional score |
| $1$ | Ordinary conditional score |
| $>1$ | Extrapolation beyond the conditional score, away from the unconditional baseline |

The CFG paper also uses the convention $(1+\gamma)s_c-\gamma s_u$; it corresponds to $w=1+\gamma$. A scale of “1” therefore means different things under different conventions.

Because both predictions have the same conversion $s=-\epsilon/b_t$,

$$
\boxed{
\epsilon_{\mathrm{cfg}}
=\epsilon_u+w(\epsilon_c-\epsilon_u).
}
$$

The sign does not flip in the final mixing formula: the common factor $-1/b_t$ applies to the entire linear combination. These are vectors in image/latent space, with the shape of the predicted noise.

For exact conservative scores, at a fixed noise level,

$$
s_{\mathrm{cfg}}
=\nabla_x\log\left[p_t(x)\,p_t(c\mid x)^w\right],
$$

up to normalization of the bracketed expression. This explains why larger $w$ favors features diagnostic of the prompt. It can also sacrifice diversity or create artifacts; the video's improving tree is an example, not a monotonic quality law. A fixed-time density identity alone does not prove that a practical guided sampler exactly samples the corresponding clean-data density. Compare the earlier [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#10.1 Guidance strength and diversity|guidance/diversity tradeoff]].

## 12. Negative prompts, flow matching, and modern video models

### 12.1 “Negative score” means subtraction of a vector field

In CFG, the unconditional prediction already appears with coefficient $1-w$, which is negative when $w>1$. A **negative prompt** changes that baseline to a prediction conditioned on undesired content:

$$
\epsilon_+=\epsilon_\theta(x_t,t,c_+),\qquad
\epsilon_-=\epsilon_\theta(x_t,t,c_-),
$$

$$
\boxed{
\epsilon_{\mathrm{guided}}
=\epsilon_-+w(\epsilon_+-\epsilon_-)
=w\epsilon_++(1-w)\epsilon_-.
}
$$

The positive and negative prompts are encoded separately. The two predictions are evaluated at the **same current noisy state and time**. Their difference is taken in the model's output space; we are not required to subtract the raw text embeddings or assign negative probabilities to images.

For exact conditional scores, the analogous field is

$$
s_{\mathrm{guided}}
=w\nabla\log p_t(x\mid c_+)
+(1-w)\nabla\log p_t(x\mid c_-)
=\nabla\log
\left[\frac{p_t(x\mid c_+)^w}{p_t(x\mid c_-)^{w-1}}\right].
$$

When this expression is normalizable, it describes a fixed-time density tilt. It favors locations relatively supported by the positive condition over the negative one. It is not a hard constraint or a guarantee that the unwanted feature disappears. In particular, at $w=1$ the negative branch cancels completely.

This gives the precise score-matching connection behind [Welch's negative-prompt discussion, 33:39](https://www.youtube.com/watch?v=iv-5mZ_9CPY&t=2019s). “Negative” refers to the branch's role in the contrast. A score vector also has signed coordinates, which is a separate meaning.

### 12.2 Flow matching learns a velocity; DDIM specifies a sampling construction

Welch mentions flow matching in the discussion of WAN. A useful distinction is:

- **Flow matching** trains a time-dependent vector field to transport one distribution into another.
- **DDIM** constructs a family of sampling trajectories using a diffusion predictor.

They connect through differential equations, but flow matching is not simply another name for removing DDPM noise. The original flow-matching framework includes both diffusion paths and other probability paths. [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).

For a simple linear path, keep our convention $t=0$ for data and $t=1$ for noise:

$$
X_t=(1-t)X_0+t\epsilon,
\qquad
\frac{dX_t}{dt}=\epsilon-X_0.
$$

An associated conditional flow-matching objective is

$$
\mathbb E_{t,X_0,\epsilon,C}
\left\|v_\theta(X_t,t,C)-(\epsilon-X_0)\right\|^2.
$$

Its population-optimal velocity is

$$
v^*(x,t,c)=\mathbb E[\epsilon-X_0\mid X_t=x,C=c].
$$

At generation time integrate the learned ODE from noise at $t=1$ toward data at $t=0$. WAN's paper uses the opposite endpoint naming; the formula here is reindexed to match this note.

> [!example]- The score–noise–velocity bridge for this path
> For $0<t<1$, the Gaussian-corruption identity gives
>
> $$
> s_t(x\mid c)=-\frac{\mathbb E[\epsilon\mid x,t,c]}{t},
> \qquad
> x=(1-t)\mathbb E[X_0\mid x,t,c]+t\mathbb E[\epsilon\mid x,t,c].
> $$
>
> Solve for the two conditional means and subtract:
>
> $$
> \boxed{v^*(x,t,c)=-\frac{x+t\,s_t(x\mid c)}{1-t}.}
> $$
>
> This is an added derivation for the stated linear Gaussian path. It shows why score, noise and velocity prediction can be related, without claiming that their training weights or all possible paths are identical. The displayed conversion is not used at the singular endpoint $t=1$.
>
> Since this conversion is affine in the score with a condition-independent offset, guidance weights summing to one also give $v_{\mathrm{guided}}=v_-+w(v_+-v_-)$. In implementations, the prediction type and scheduler must agree.

WAN 2.1 provides a concrete modern example: a video VAE, a diffusion transformer, an **umT5** text encoder and a flow-matching objective. It does not use “CLIP everywhere.” Video frames introduce a temporal dimension of the sample; this is different from diffusion/flow time $t$. [Wan technical report, §§4.2.1–4.2.2](https://arxiv.org/html/2503.20314v2).

Welch's example negative prompt is passed in Chinese. Its operation is still text conditioning followed by contrastive combination of model predictions; the language itself does not give the vector a special negative sign.

### 12.3 Keep the moving parts separate

| Choice | What it determines |
| --- | --- |
| Pixel space or VAE latent space | Where the evolving sample lives |
| U-Net or transformer | How the prediction function is implemented |
| Noise, score, clean-data or velocity target | What the network outputs and how to interpret it |
| Noise/path schedule | Which intermediate distributions training and sampling use |
| DDPM, DDIM or another SDE/ODE solver | How predictions update the current sample |
| Text/image/class conditioning | Which information enters each prediction |
| Guidance scale and negative prompt | How predictions are combined before the update |

This separation explains how a modern system can retain the core denoising/score idea while changing its architecture, representation, prediction target and sampler.

## Origin

> [!info]- Source details
> Requested as one new learning note on 2026-11-15, with short inline connections to the two named diffusion notes. The artist/refinement analogy is paraphrased from the user's request. The expanded algebra, corrections, comparison tables and all generated figures are assistant-added synthesis.
>
> Extended on 2026-11-16 at the user's request to explain the selected score-field GIF and static panels: directions, individual image/state points, cluster centers and the whole distribution. The reading guide, four-pixel example and mixture calculation are assistant-added explanations checked against the existing generator and constructed data; the figures themselves are unchanged. This follow-up does not claim additional video coverage.
>
> **Outlier**, *Diffusion Models From Scratch | Score-Based Generative Models Explained | Math Explained* (2024-10-09): [[raw/articles/2026-11-15-Outlier-score-diffusion-auto-captions.txt|full exported auto-captions, 0:00–38:04]] and [[raw/articles/2026-11-15-Outlier-score-diffusion-description.txt|visible description]]. Selected mathematical frames: [[raw/assets/2026-11-15-Outlier-score-I02-dsm-objective.png|DSM objective, about 17:58]] and [[raw/assets/2026-11-15-Outlier-score-I01-noise-target.png|Gaussian noise target, about 20:10]]. Captions omit some displayed symbols; the note's equations were independently checked rather than treated as verbatim transcription.
>
> **Stephen Welch / Welch Labs**, *But how do AI images and videos actually work?*, guest video on 3Blue1Brown (2025-07-25): [[raw/articles/2026-11-15-Welch-diffusion-captions.txt|full exported captions, 0:03–37:18]] and [[raw/articles/2026-11-15-Welch-diffusion-description.txt|visible description and technical notes]]. Learning coverage is the discussion through approximately 35:25; the following guest/promotion segment supplies no additional mathematical content.
>
> Primary references are linked beside the claims they support. The note retains parameter-independent constants in the score-loss equivalence, distinguishes standard noise from actual perturbations, keeps timestep weights explicit, and separates deterministic sampling from simply deleting a stochastic term. Neither existing diffusion note was rewritten.
>
> [[assets/figures/2026-11-15-diffusion-scores/draw_diffusion.py|Reproducible original figure generator]]; [[assets/figures/2026-11-15-diffusion-scores/constructed-data.json|constructed mixture data]]; [[assets/figures/2026-11-15-diffusion-scores/checks.json|mathematical checks and asset hashes]]. Analytic derivations were checked alongside independent quadrature, finite-difference and schedule checks. SVGs and PNG previews were inspected; decoded GIF frames span all phases. Live Obsidian rendering/navigation was not checked.
