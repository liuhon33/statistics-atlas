---
id: learning-vae-diffusion-elbo-paths
title: VAE and diffusion ELBO - images, hidden paths, and Gaussian KL
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO]]"
subject: computing
backbone_path: Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO
study_band: M
note_types: [conversation-digest, derivation, question, insight]
question_roles: [concept-distinction, reconcile-approaches, modeling-consequence]
source_format: conversation-and-handwriting
created: 2026-11-11
updated: '2026-11-12'
status: active
verification: checked
learning_state: practicing
aliases: [Diffusion as a hierarchical VAE, Closed-form KL versus optimizable ELBO]
tags: [atlas/learning, subject/computing, topic/elbo, topic/diffusion, study/masters]
connections:
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO]]"
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/Model error versus inference error in variational inference]]"
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/Reparameterization - moving the parameter out of the sampling distribution]]"
  - "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Variational autoencoders]]"
sources:
  - "[[raw/conversations/2026-11-10-Diffusion-Approximation-Order.json]]"
  - "[[raw/notes/2026-11-10-Lec12-diffusion-models.pdf]]"
  - "[[raw/assets/2026-11-10-VAE-diffusion-I01-handwritten-ELBO.jpg]]"
---

# VAE and diffusion ELBO - images, hidden paths, and Gaussian KL

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → ELBO

Start with two possible images and count their hidden paths. Then use my likelihood → importance sampling → Jensen derivation to obtain both the VAE and diffusion ELBOs. The final sections calculate the Gaussian KL and show exactly which expectations still need sampling.

## 1. Numbers first — the same images can come from different paths

There are only two possible images: $A$ appears with probability $0.8$, and $B$ with probability $0.2$. We add noise twice, so a full record is $(x_0,x_1,x_2)$ and its hidden part is $Z=(x_1,x_2)$.

![[assets/figures/2026-11-11-vae-diffusion/binary-paths.svg]]

*Original assistant illustration. The top panels have equal row totals but different entries. The bottom panels divide each row by its total, exposing different distributions over paths conditional on the same image.*

**Toy-image notes:** each “photo” is just **one pixel taking a value in $\{0,1\}$**: $A=0$ is black and $B=1$ is white. The noisy states $x_1,x_2$ are also binary in this example. This finite bit-flipping chain illustrates probability bookkeeping; the Gaussian diffusion model introduced later has continuous noisy states.

### 1.1 Construct the known forward process

Write $q_0$ for the data distribution. First choose the image:

$$
q_0(A)=0.8,\qquad q_0(B)=0.2.
$$

The first noising step keeps the bit with probability $0.75$; the second keeps it with probability $0.60$:

| Starting value | $q(x_1=0\mid x_0)$ | $q(x_1=1\mid x_0)$ |
| --- | ---: | ---: |
| $x_0=A=0$ | 0.75 | 0.25 |
| $x_0=B=1$ | 0.25 | 0.75 |

| Starting value | $q(x_2=0\mid x_1)$ | $q(x_2=1\mid x_1)$ |
| --- | ---: | ---: |
| $x_1=0$ | 0.60 | 0.40 |
| $x_1=1$ | 0.40 | 0.60 |

Multiply along a path. For example,

$$
q(A,0,0)=0.8\times0.75\times0.60=0.36.
$$

Doing this for every path gives:

| Image $x_0$ | $Z=(0,0)$ | $Z=(0,1)$ | $Z=(1,0)$ | $Z=(1,1)$ | Sum over paths |
| --- | ---: | ---: | ---: | ---: | ---: |
| $A$ | 0.36 | 0.24 | 0.08 | 0.12 | **0.80** |
| $B$ | 0.03 | 0.02 | 0.06 | 0.09 | **0.20** |

At the intermediate and final times,

$$
q(x_1=0)=0.8(0.75)+0.2(0.25)=0.65,
$$

$$
q(x_2=0)=0.65(0.60)+0.35(0.40)=0.53.
$$

Thus $q(x_1)=(0.65,0.35)$ and $q(x_2)=(0.53,0.47)$.

### 1.2 Construct a reverse model that gets the images right

The model generates in the opposite order: $x_2\to x_1\to x_0$. Specify it completely:

1. Draw $x_2$ from $p(x_2)=(0.53,0.47)$.
2. For either $x_2$, choose $x_1=0$ or $1$ with probability $0.5$ each.
3. For either $x_1$, choose $A$ with probability $0.8$ and $B$ with probability $0.2$.

The last step deliberately ignores $x_1$. This is a valid model, even if it is an uninteresting way to generate a one-pixel image.

For the same path as above,

$$
p_\theta(A,0,0)=p(x_2=0)p_\theta(x_1=0\mid x_2=0)p_\theta(A\mid x_1=0)
=0.53(0.5)(0.8)=0.212.
$$

| Image $x_0$ | $Z=(0,0)$ | $Z=(0,1)$ | $Z=(1,0)$ | $Z=(1,1)$ | Sum over paths |
| --- | ---: | ---: | ---: | ---: | ---: |
| $A$ | 0.212 | 0.188 | 0.212 | 0.188 | **0.800** |
| $B$ | 0.053 | 0.047 | 0.053 | 0.047 | **0.200** |

The model has $p_\theta(x_1)=(0.5,0.5)$ instead of $(0.65,0.35)$, but its final image probabilities are exactly correct. Marginalizing means adding cells; it does not require the individual cells to agree.

### 1.3 Now condition on an observed image

Given $A$, divide the first row of each joint table by $0.8$:

$$
q(Z\mid A)=(0.45,0.30,0.10,0.15),
$$

$$
p_\theta(Z\mid A)=(0.265,0.235,0.265,0.235).
$$

For instance, $q(Z=(0,0)\mid A)=0.36/0.8=0.45$, whereas the model gives $0.212/0.8=0.265$.

Given $B$,

$$
q(Z\mid B)=(0.15,0.10,0.30,0.45),\qquad
p_\theta(Z\mid B)=(0.265,0.235,0.265,0.235).
$$

These are distributions over alternative hidden histories compatible with a specified image. Correct probabilities for the two images do not determine those histories uniquely.

### 1.4 A model that also matches every path

Bayes' rule gives the exact reverse of the forward chain. For the last generation step,

$$
q(A\mid x_1=0)=\frac{0.8(0.75)}{0.65}=\frac{12}{13},\qquad
q(A\mid x_1=1)=\frac{0.8(0.25)}{0.35}=\frac47.
$$

For the earlier generation step,

$$
q(x_1=0\mid x_2=0)=\frac{0.65(0.60)}{0.53}=\frac{39}{53},\qquad
q(x_1=0\mid x_2=1)=\frac{0.65(0.40)}{0.47}=\frac{26}{47}.
$$

Use these conditionals and the same terminal distribution $(0.53,0.47)$. Then

$$
p_\theta(A,0,0)=\frac{53}{100}\frac{39}{53}\frac{12}{13}=0.36,
$$

and all eight path probabilities match. This demonstrates a sufficient construction for correct images. It is stronger than necessary, as the preceding model already showed.

### 1.5 Why care about paths if generation already works?

My question: “So if the model already generates A and B with the correct probabilities, why do we still care whether the hidden paths match? Isn't generating the right image distribution our actual goal?”

**Yes. Correct image probabilities are the generative goal.** The model in §1.2 already achieves it. Matching auxiliary noising histories is useful because it gives a tractable training objective; those histories are not a uniquely correct physical explanation of how an image arose.

Here is the numerical difference between likelihood and the bound. All logarithms in this note are natural logs, so KL and log losses are in **nats**. For discrete probability vectors,

$$
D_{\rm KL}(q\|p)=\sum_j q_j\log\frac{q_j}{p_j}.
$$

For image $A$,

$$
\begin{aligned}
D_{\rm KL}(q(Z\mid A)\|p_\theta(Z\mid A))
={}&0.45\log\frac{0.45}{0.265}+0.30\log\frac{0.30}{0.235}\\
&+0.10\log\frac{0.10}{0.265}+0.15\log\frac{0.15}{0.235}\\
={}&0.146744.
\end{aligned}
$$

The ELBO, calculated directly from these four paths, is

$$
\begin{aligned}
\mathcal L(A)
&=\sum_Z q(Z\mid A)\log\frac{p_\theta(A,Z)}{q(Z\mid A)}\\
&=0.45\log\frac{0.212}{0.45}+0.30\log\frac{0.188}{0.30}
+0.10\log\frac{0.212}{0.10}+0.15\log\frac{0.188}{0.15}\\
&=-0.369887.
\end{aligned}
$$

Therefore

$$
\underbrace{\log p_\theta(A)}_{\log(0.8)=-0.223144}
=\underbrace{\mathcal L(A)}_{-0.369887}
+\underbrace{D_{\rm KL}(q(Z\mid A)\|p_\theta(Z\mid A))}_{0.146744}.
$$

For $B$, the gap is $0.158758$ and the ELBO is $-1.768196$, although $\log p_\theta(B)=\log(0.2)=-1.609438$ is already correct.

Compare three specified models; these are illustrative candidates, not recorded training iterations:

| Model | Image probabilities $(A,B)$ | Image KL | Average posterior-path KL | Average negative ELBO |
| --- | --- | ---: | ---: | ---: |
| Uniform reverse steps | $(0.5,0.5)$ | 0.192745 | 0.149146 | 0.842294 |
| Images correct, paths different | $(0.8,0.2)$ | **0** | 0.149146 | 0.649549 |
| Exact reverse chain | $(0.8,0.2)$ | **0** | **0** | 0.500402 |

Every model here starts from $(0.53,0.47)$. The average is over $q_0(A)=0.8,q_0(B)=0.2$. The data entropy is $H(q_0)=0.500402$, and

$$
\boxed{
-\mathbb E_{q_0}\mathcal L(X_0)
=H(q_0)+D_{\rm KL}(q_0\|p_\theta(X_0))
+\mathbb E_{q_0}D_{\rm KL}(q(Z\mid X_0)\|p_\theta(Z\mid X_0)).
}
$$

Equivalently, the KL between the **joint** forward and reverse distributions equals image KL plus average posterior-path KL. This follows by splitting $\log[q_0(x_0)q(Z\mid x_0)/(p_\theta(x_0)p_\theta(Z\mid x_0))]$ and summing.

The extra term measures looseness of the bound. It is not evidence that already-correct generated images are wrong. In a restricted model family, improving the ELBO can trade off marginal fit against posterior agreement; maximizing the ELBO need not give the exact maximum-likelihood solution.

## 2. One numerical preview of a closed-form Gaussian KL

Now leave the binary toy and consider a continuous scalar latent variable. Suppose

$$
q(z)=\mathcal N(1,0.25),\qquad p(z)=\mathcal N(0,1),
$$

where the second argument is **variance**, so the standard deviation of $q$ is $0.5$. The Gaussian formula gives

$$
D_{\rm KL}(q\|p)
=\frac12\left[\log\frac{1}{0.25}+\frac{0.25+(1-0)^2}{1}-1\right]
=0.818147.
$$

This calculates the entire integral $\int q(z)\log(q(z)/p(z))\,dz$ without drawing samples. Section 6 derives the formula instead of treating it as a lookup rule.

By contrast, evaluating a log density at one sample is only one number. At $z=1$,

$$
\log\frac{q(1)}{p(1)}=\log 2+\frac12=1.193147,
$$

which is not the KL $0.818147$. KL averages the log ratio over **all** possible $z$ under $q$.

## 3. My VAE derivation, typeset and checked

This follows the sequence in my uploaded photograph. Let $x$ be an observed image, $z\in\mathbb R^k$ a latent variable, $p(z)$ a fixed prior, $p_\theta(x\mid z)$ the decoder, and $q_\phi(z\mid x)$ the encoder/proposal. Parameters $\theta$ belong to the generator and $\phi$ to the encoder.

The likelihood is obtained by integrating the joint over $z$:

$$
p_\theta(x,z)=p_\theta(x\mid z)p(z),\qquad
p_\theta(x)=\int p_\theta(x\mid z)p(z)\,dz.
$$

For the identities below, assume normalized distributions, $0<p_\theta(x)<\infty$, a proposal positive on the relevant model support, and finite displayed log expectations. Replace integrals by sums for discrete latents. For continuous observations, $p_\theta(x)$ is a density, not a positive probability assigned to one exact image value.

### 3.1 Start from maximum likelihood

For training images $x^{(1)},\ldots,x^{(N)}$, the goal is to maximize $\sum_i\log p_\theta(x^{(i)})$. The derivation works with one image at a time:

$$
\log p_\theta(x)
=\log\int p_\theta(x\mid z)p(z)\,dz
=\log\mathbb E_{p(z)}[p_\theta(x\mid z)].
$$

My handwritten “$p(z)$ is not good enough” concerns sampling efficiency. Prior sampling is valid, but many samples may explain this particular image poorly. The exact model posterior $p_\theta(z\mid x)$ would be an ideal importance proposal, but usually needs the very normalizing constant $p_\theta(x)$ we cannot readily compute. Introduce a tractable encoder $q_\phi$ instead.

### 3.2 Change the sampling distribution exactly

Multiply and divide by $q_\phi(z\mid x)$:

$$
\begin{aligned}
\log p_\theta(x)
&=\log\int q_\phi(z\mid x)
\frac{p_\theta(x\mid z)p(z)}{q_\phi(z\mid x)}\,dz\\
&=\log\mathbb E_{q_\phi(z\mid x)}
\left[\frac{p_\theta(x\mid z)p(z)}{q_\phi(z\mid x)}\right].
\end{aligned}
$$

The ratio $p(z)/q_\phi(z\mid x)$ compensates for changing where samples come from. No lower bound has appeared yet.

### 3.3 Apply Jensen, then separate the log ratio

Because $\log$ is concave, $\log\mathbb E[W]\geq\mathbb E[\log W]$ for a positive integrable $W$:

$$
\begin{aligned}
\log p_\theta(x)
&\geq\mathbb E_{q_\phi(z\mid x)}
\left[\log\frac{p_\theta(x\mid z)p(z)}{q_\phi(z\mid x)}\right]\\
&=\mathbb E_{q_\phi}[\log p_\theta(x\mid z)]
+\mathbb E_{q_\phi}\left[\log\frac{p(z)}{q_\phi(z\mid x)}\right]\\
&=\boxed{\mathbb E_{q_\phi}[\log p_\theta(x\mid z)]
-D_{\rm KL}(q_\phi(z\mid x)\|p(z))}\\
&\equiv\mathcal L_{\rm VAE}(x).
\end{aligned}
$$

An **evidence lower bound (ELBO)** is this expected joint log density minus the proposal's expected log density. Its gap is exactly

$$
\boxed{\log p_\theta(x)-\mathcal L_{\rm VAE}(x)
=D_{\rm KL}(q_\phi(z\mid x)\|p_\theta(z\mid x)).}
$$

The KL subtracted inside the bound compares the encoder with the **prior**. The KL measuring the gap compares it with the **model posterior**. These are different quantities. The same distinction underlies my [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|four approaches to the ELBO]]. The standard VAE formulation and stochastic estimator are given in [Kingma & Welling, §2.2–2.4](https://arxiv.org/html/1312.6114v11#S2).

## 4. Write the diffusion derivation in exactly the same order

Use a finite-time diffusion model with observed image $x_0\in\mathbb R^d$ and noisy states $x_1,\ldots,x_T\in\mathbb R^d$. Treat the entire path as one latent vector:

$$
\boxed{z\ \longleftrightarrow\ Z=(x_1,\ldots,x_T)\in\mathbb R^{dT}.}
$$

The known [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#2. Forward diffusion and its closed form|noising process]] is

$$
q(Z\mid x_0)=\prod_{t=1}^Tq(x_t\mid x_{t-1}),
$$

and the generative model runs backward:

$$
p_\theta(x_0,Z)=p(x_T)\prod_{t=1}^Tp_\theta(x_{t-1}\mid x_t).
$$

Here $q(x_0,Z)=q_0(x_0)q(Z\mid x_0)$ denotes the training-data/noising joint. Each $p_\theta$ marginal or posterior below is induced by the **same** generative joint; introducing new conditional notation does not introduce another learned model.

### 4.1 Identify every counterpart of the VAE pieces

Separate the final image-producing step:

$$
p_\theta(x_0,Z)
=\underbrace{p_\theta(x_0\mid x_1)}_{\text{decoder}}
\underbrace{p(x_T)\prod_{t=2}^Tp_\theta(x_{t-1}\mid x_t)}_{p_\theta(Z):\ \text{latent-path prior}}.
$$

| VAE | Diffusion |
| --- | --- |
| Image $x$ | Image $x_0$ |
| Latent variable $z$ | Entire path $Z=x_{1:T}$ |
| Prior $p(z)$ | Path prior $p_\theta(Z)$ |
| Decoder $p_\theta(x\mid z)$ | $p_\theta(x_0\mid x_1)$ |
| Encoder/proposal $q_\phi(z\mid x)$ | Forward process $q(Z\mid x_0)$ |
| Model posterior $p_\theta(z\mid x)$ | Model path posterior $p_\theta(Z\mid x_0)$ |

The prior analog is the distribution over **all of $Z$**, not just $p(x_T)$. It depends on $\theta$ through the reverse transitions. The decoder only uses $x_1$ because of the reverse Markov structure. In standard fixed-schedule DDPM, $q$ has no learned encoder parameters.

### 4.2 Likelihood → change of proposal → Jensen → ELBO

Under the same support and integrability conditions as in §3,

$$
\begin{aligned}
\log p_\theta(x_0)
&=\log\int p_\theta(x_0\mid x_1)p_\theta(Z)\,dZ\\
&=\log\mathbb E_{p_\theta(Z)}[p_\theta(x_0\mid x_1)]\\
&=\log\int q(Z\mid x_0)
\frac{p_\theta(x_0\mid x_1)p_\theta(Z)}{q(Z\mid x_0)}\,dZ\\
&=\log\mathbb E_{q(Z\mid x_0)}
\left[\frac{p_\theta(x_0\mid x_1)p_\theta(Z)}{q(Z\mid x_0)}\right]\\
&\geq\mathbb E_{q(Z\mid x_0)}
\left[\log\frac{p_\theta(x_0\mid x_1)p_\theta(Z)}{q(Z\mid x_0)}\right]\\
&=\boxed{\mathbb E_q[\log p_\theta(x_0\mid x_1)]
-D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z))}\\
&\equiv\mathcal L_{\rm diff}(x_0).
\end{aligned}
$$

Every equality before Jensen is exact. This is the direct counterpart of the last line in my photograph.

As in the VAE,

$$
\boxed{\log p_\theta(x_0)=\mathcal L_{\rm diff}(x_0)
+D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z\mid x_0)).}
$$

Again distinguish **path prior** $p_\theta(Z)$ in the reconstruction-minus-KL formula from **path posterior** $p_\theta(Z\mid x_0)$ in the gap formula. The binary example supplied actual numbers for this gap.

When $\theta$ changes, both the likelihood and the posterior-gap term can change. An increase in the ELBO alone does not guarantee that the likelihood increased and the gap decreased separately. With the generative model fixed, optimizing the variational distribution does minimize the gap; these are different optimization settings.

## 5. Why this diffusion ELBO is already optimizable

Insert the two factorizations into the bound:

$$
\boxed{
\mathcal L_{\rm diff}(x_0)=\mathbb E_{q(Z\mid x_0)}
\left[\log p(x_T)+\sum_{t=1}^T\log p_\theta(x_{t-1}\mid x_t)
-\sum_{t=1}^T\log q(x_t\mid x_{t-1})\right].
}
$$

For fixed forward process and fixed terminal prior, the part of the **negative** ELBO that depends on $\theta$ is

$$
\boxed{J(\theta;x_0)=\mathbb E_{q(Z\mid x_0)}
\left[-\sum_{t=1}^T\log p_\theta(x_{t-1}\mid x_t)\right].}
$$

“Parameter-dependent part” means $-\mathcal L_{\rm diff}=J+C(x_0)$, with $C$ independent of $\theta$. We can omit $C$ to train $\theta$, but must restore it to report the numerical ELBO. If the noising schedule or terminal prior is learned, the omitted terms need reconsideration.

### 5.1 What one training example actually computes

Sample a forward trajectory from a training image. At one step, suppose the reverse model has fixed positive variance $s_t^2$ and predicts a mean $\mu_\theta(x_t,t)$:

$$
p_\theta(x_{t-1}\mid x_t)
=\mathcal N(x_{t-1};\mu_\theta(x_t,t),s_t^2I_d).
$$

At the sampled pair $(x_{t-1},x_t)$, its negative log density is explicitly

$$
-\log p_\theta(x_{t-1}\mid x_t)
=\frac d2\log(2\pi s_t^2)
+\frac{\|x_{t-1}-\mu_\theta(x_t,t)\|^2}{2s_t^2}.
$$

Here, **loss** means this one sampled step's negative log-likelihood, $-\log p_\theta(x_{t-1}\mid x_t)$: minimizing it makes the model assign higher density to the sampled target $x_{t-1}$.

For a scalar sample $x_{t-1}=0.7$, predicted mean $0.2$, and variance $0.25$,

$$
\text{loss}=\tfrac12\log(2\pi\cdot0.25)+\frac{(0.7-0.2)^2}{2(0.25)}
=0.725791,
$$

$$
\frac{\partial\text{loss}}{\partial\mu_\theta}
=\frac{\mu_\theta-x_{t-1}}{0.25}=-2.
$$

Holding the sample and variance fixed, the log term has derivative zero, and the chain rule gives $\frac{\partial}{\partial\mu_\theta}\frac{(x_{t-1}-\mu_\theta)^2}{2s_t^2}=\frac{2(x_{t-1}-\mu_\theta)(-1)}{2s_t^2}=\frac{\mu_\theta-x_{t-1}}{s_t^2}$; substitute $\mu_\theta=0.2$ only after differentiating.

The network can backpropagate this derivative immediately. We did not analytically integrate over all paths.

With $M$ sampled paths, an estimator is

$$
\widehat J=\frac1M\sum_{m=1}^M\left[-\sum_{t=1}^T
\log p_\theta(x_{t-1}^{(m)}\mid x_t^{(m)})\right].
$$

Because $q$ is fixed with respect to $\theta$, and assuming differentiation and expectation may be interchanged,

$$
\nabla_\theta J
=\mathbb E_q\left[-\sum_t\nabla_\theta\log p_\theta(x_{t-1}\mid x_t)\right].
$$

A sampled version is an unbiased gradient estimator under these conditions. Training needs samples and differentiable log densities; it does not require a symbolic formula for the full expectation, an analytic optimizer, $p_\theta(x_0)$, or the normalized posterior $p_\theta(Z\mid x_0)$. The chain-form variational objective appears in [DDPM, equation (3)](https://arxiv.org/html/2006.11239v2#S2).

### 5.2 What “the whole-path KL has no Gaussian closed form” means

For a Gaussian forward process with fixed $x_0$, $q(Z\mid x_0)$ is jointly Gaussian. But the reverse path prior $p_\theta(Z)$ generally is **not** jointly Gaussian, even when each reverse conditional is Gaussian.

A small counterexample makes the distinction concrete:

$$
X_2\sim\mathcal N(0,1),\qquad
X_1\mid X_2\sim\mathcal N(X_2^2,s^2),\quad s^2>0.
$$

The conditional is Gaussian, but its conditional mean $X_2^2$ is nonlinear. In a nonsingular jointly Gaussian pair, a conditional mean must be affine in the conditioning variable. Thus this pair is not jointly Gaussian. Neural-network transition means have the same general obstacle.

Consequently, we cannot normally insert two mean vectors and two covariance matrices into the multivariate Gaussian KL formula for $D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z))$. The path density itself remains evaluable as a product of transitions. Special linear-Gaussian reverse models can have a Gaussian joint, but that is an additional model restriction.

This claim concerns that **particular full-path integral**. It does not say the ELBO is untrainable or that none of its parts can be integrated analytically.

## 6. Derive the closed form, then apply it to VAE and diffusion

### 6.1 Scalar Gaussian KL, starting from its definition

Let $q=\mathcal N(m_q,v_q)$ and $p=\mathcal N(m_p,v_p)$ with positive variances. By definition,

$$
D_{\rm KL}(q\|p)=\mathbb E_q[\log q(Z)-\log p(Z)].
$$

Write out both log densities and cancel the $\log(2\pi)$ terms:

$$
\log\frac{q(z)}{p(z)}
=\frac12\log\frac{v_p}{v_q}
-\frac{(z-m_q)^2}{2v_q}
+\frac{(z-m_p)^2}{2v_p}.
$$

Only two expectations remain. The first is the variance:

$$
\mathbb E_q[(Z-m_q)^2]=v_q.
$$

For the second, expand $Z-m_p=(Z-m_q)+(m_q-m_p)$. Its cross term vanishes because $\mathbb E_q[Z-m_q]=0$:

$$
\mathbb E_q[(Z-m_p)^2]=v_q+(m_q-m_p)^2.
$$

Substitute these moments:

$$
\boxed{D_{\rm KL}(q\|p)
=\frac12\left[\log\frac{v_p}{v_q}-1+\frac{v_q}{v_p}
+\frac{(m_q-m_p)^2}{v_p}\right].}
$$

That is what “calculate the closed form” means: perform the expectation algebraically using known moments. It yields §2's $0.818147$ exactly up to rounding.

### 6.2 Vector Gaussian KL

For $q=\mathcal N(m_q,S_q)$ and $p=\mathcal N(m_p,S_p)$ on $\mathbb R^k$, let both covariance matrices be symmetric positive definite. Put $\delta=m_q-m_p$.

The analogous expected quadratic forms are

$$
\mathbb E_q[(Z-m_q)^TS_q^{-1}(Z-m_q)]=k,
$$

$$
\mathbb E_q[(Z-m_p)^TS_p^{-1}(Z-m_p)]
=\operatorname{tr}(S_p^{-1}S_q)+\delta^TS_p^{-1}\delta.
$$

To see the second identity, write $U=Z-m_q$, expand $(U+\delta)^TS_p^{-1}(U+\delta)$, use $\mathbb E U=0$, and use $\mathbb E[U^TAU]=\operatorname{tr}(A\mathbb E[UU^T])$. Consequently,

$$
\boxed{D_{\rm KL}(q\|p)=\frac12\left[
\log\frac{\det S_p}{\det S_q}-k+\operatorname{tr}(S_p^{-1}S_q)
+(m_q-m_p)^TS_p^{-1}(m_q-m_p)\right].}
$$

The log-determinant ratio, covariance ratio, and mean mismatch together determine the divergence. For equal covariances $S_q=S_p=S$, the covariance terms cancel and only $\tfrac12\delta^TS^{-1}\delta$ remains.

### 6.3 Which part of a standard VAE is closed form?

For the common choice

$$
q_\phi(z\mid x)=\mathcal N(\mu_\phi(x),\operatorname{diag}(\sigma_\phi^2(x))),
\qquad p(z)=\mathcal N(0,I_k),
$$

substitute $S_p=I_k$, $m_p=0$, $S_q=\operatorname{diag}(\sigma_j^2)$:

$$
\boxed{D_{\rm KL}(q_\phi(z\mid x)\|p(z))
=\frac12\sum_{j=1}^k[\mu_j^2+\sigma_j^2-1-\log\sigma_j^2].}
$$

This is the standard analytic VAE prior KL. [Kingma & Welling, Appendix B](https://arxiv.org/html/1312.6114v11#A2) derives the same Gaussian integral.

It does **not** give an analytic formula for the posterior-gap KL $D_{\rm KL}(q_\phi(z\mid x)\|p_\theta(z\mid x))$. The nonlinear decoder usually makes that model posterior non-Gaussian and its normalization intractable. The encoder is Gaussian by choice; the exact model posterior need not be.

But the reconstruction expectation

$$
\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]
$$

generally has no simple analytic integral through a nonlinear decoder. For example, with a Gaussian decoder mean $f_\theta(z)$, it contains $\mathbb E_q\|x-f_\theta(Z)\|^2$. Knowing $q$ is Gaussian does not provide all these nonlinear network expectations in closed form.

A common estimator therefore combines sampled reconstruction with exact KL:

$$
z^{(m)}=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon^{(m)},\qquad
\epsilon^{(m)}\sim\mathcal N(0,I_k),
$$

$$
\widehat{\mathcal L}_{\rm VAE}
=\frac1M\sum_{m=1}^M\log p_\theta(x\mid z^{(m)})
-\frac12\sum_{j=1}^k[\mu_j^2+\sigma_j^2-1-\log\sigma_j^2].
$$

Here $\odot$ means componentwise multiplication. Reparameterization lets gradients also reach the encoder parameters $\phi$ through the sampled latents. Thus a standard VAE already combines analytic terms with stochastic optimization; it does not generally have a closed-form full ELBO or exact marginal likelihood. Different VAE priors/encoders may also lose the analytic prior KL.

## 7. Rearrange the diffusion bound into local Gaussian comparisons

The extra diffusion algebra improves how we estimate and train the same bound. It does not make an otherwise impossible objective trainable.

### 7.1 Reverse-factor the known forward distribution, keeping $x_0$ fixed

Conditioned on the clean image, the forward chain can also be written

$$
q(Z\mid x_0)=q(x_T\mid x_0)\prod_{t=2}^Tq(x_{t-1}\mid x_t,x_0).
$$

This is a factorization of the same distribution, not a newly learned encoder. Substitute it into $\mathbb E_q\log[p_\theta(x_0,Z)/q(Z\mid x_0)]$:

$$
\begin{aligned}
\mathcal L_{\rm diff}(x_0)=\mathbb E_q\Bigg[
&\log p_\theta(x_0\mid x_1)
+\log\frac{p(x_T)}{q(x_T\mid x_0)}\\
&+\sum_{t=2}^T\log\frac{p_\theta(x_{t-1}\mid x_t)}{q(x_{t-1}\mid x_t,x_0)}\Bigg].
\end{aligned}
$$

Take each expectation over the variables it actually uses:

$$
\boxed{
\begin{aligned}
\mathcal L_{\rm diff}(x_0)={}&
\mathbb E_{q(x_1\mid x_0)}\log p_\theta(x_0\mid x_1)\\
&-D_{\rm KL}(q(x_T\mid x_0)\|p(x_T))\\
&-\sum_{t=2}^T\mathbb E_{q(x_t\mid x_0)}
D_{\rm KL}(q(x_{t-1}\mid x_t,x_0)\|p_\theta(x_{t-1}\mid x_t)).
\end{aligned}}
$$

The three pieces are reconstruction, terminal-prior KL, and intermediate-step KLs. This identity is exact. [DDPM, equations (5)–(7)](https://arxiv.org/html/2006.11239v2#S2) gives this rearrangement and the Gaussian bridge below; the uploaded lecture develops it on PDF pages 12–17.

### 7.2 Derive the known Gaussian bridge by completing the square

The same precision-and-linear-term calculation appears in [[Learning/Statistical computing & learning/Statistical learning & prediction/Gaussian processes - conditioning by completing the square#4. The promised connection to diffusion|Gaussian-process conditioning and Bayesian regression]]. There the unknown is a function value or a coefficient; here it is the previous diffusion state.

Assume the standard forward noising rule, with independent standard Gaussian noises:

$$
x_t=\sqrt{\alpha_t}\,x_{t-1}+\sqrt{\beta_t}\,\epsilon_t,
\qquad\alpha_t=1-\beta_t,\quad0<\beta_t<1,
$$

$$
\bar\alpha_t=\prod_{s=1}^t\alpha_s,\qquad
q(x_t\mid x_0)=\mathcal N(\sqrt{\bar\alpha_t}\,x_0,(1-\bar\alpha_t)I_d).
$$

For $t\geq2$, put $y=x_{t-1}$. Bayes' rule and the forward Markov property give

$$
q(y\mid x_t,x_0)\ \propto\ q(x_t\mid y)q(y\mid x_0).
$$

Terms depending on $y$ in the log density are

$$
-\frac{\|x_t-\sqrt{\alpha_t}y\|^2}{2\beta_t}
-\frac{\|y-\sqrt{\bar\alpha_{t-1}}x_0\|^2}{2(1-\bar\alpha_{t-1})}.
$$

The coefficient of $\|y\|^2$ gives the precision, and the linear coefficient gives precision times mean:

$$
\frac1{\tilde\beta_t}=\frac{\alpha_t}{\beta_t}+\frac1{1-\bar\alpha_{t-1}},
$$

$$
\frac{\tilde\mu_t}{\tilde\beta_t}
=\frac{\sqrt{\alpha_t}}{\beta_t}x_t
+\frac{\sqrt{\bar\alpha_{t-1}}}{1-\bar\alpha_{t-1}}x_0.
$$

Since $\alpha_t+\beta_t=1$ and $\alpha_t\bar\alpha_{t-1}=\bar\alpha_t$, simplify to

$$
\boxed{\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,}
$$

$$
\boxed{\tilde\mu_t(x_t,x_0)
=\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x_t
+\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x_0.}
$$

Thus $q(x_{t-1}\mid x_t,x_0)=\mathcal N(\tilde\mu_t,\tilde\beta_t I_d)$ exactly.

The condition on **$x_0$** matters. The unconditional true reverse is

$$
q(x_{t-1}\mid x_t)=\int q(x_{t-1}\mid x_t,x_0)q(x_0\mid x_t)\,dx_0,
$$

which is generally a mixture over possible clean images and need not be Gaussian. We use the known clean training image to calculate a tractable teacher distribution. The reverse model still receives only $(x_t,t)$ when generating.

### 7.3 Apply the Gaussian KL formula to one step

Choose a Gaussian reverse conditional

$$
p_\theta(x_{t-1}\mid x_t)=\mathcal N(\mu_\theta(x_t,t),s_t^2I_d),\qquad s_t^2>0.
$$

For **fixed** $x_0,x_t,t$, substitute $m_q=\tilde\mu_t$, $S_q=\tilde\beta_tI_d$, $m_p=\mu_\theta$, $S_p=s_t^2I_d$ into §6:

$$
\boxed{K_t(x_0,x_t)=\frac12\left[
d\left(\frac{\tilde\beta_t}{s_t^2}-1+\log\frac{s_t^2}{\tilde\beta_t}\right)
+\frac{\|\tilde\mu_t-\mu_\theta(x_t,t)\|^2}{s_t^2}\right].}
$$

This has integrated out $x_{t-1}$. The **outer expectation** $\mathbb E_{q(x_t\mid x_0)}K_t(x_0,x_t)$ generally still requires sampling, because $\mu_\theta(x_t,t)$ is nonlinear in the random $x_t$.

If $s_t^2$ is fixed independently of $\theta$, the variance terms are constant with respect to $\theta$. The trainable local part is

$$
\frac1{2s_t^2}\|\tilde\mu_t-\mu_\theta(x_t,t)\|^2.
$$

If the reverse variance is learned, its log and ratio terms must also be optimized; simply discarding them would change the objective.

The terminal KL is analytic as well when $p(x_T)=\mathcal N(0,I_d)$:

$$
D_{\rm KL}(q(x_T\mid x_0)\|p(x_T))
=\frac12\left[\bar\alpha_T\|x_0\|^2
+d\big(-\bar\alpha_T-\log(1-\bar\alpha_T)\big)\right].
$$

It is constant with respect to the reverse-model parameters for a fixed schedule, though it need not be zero. At $t=1$, conditioning on $x_0$ makes the bridge to $x_0$ degenerate, so the nondegenerate Gaussian-KL formula above is not used: keep the reconstruction term separately.

### 7.4 Work through a continuous diffusion step with actual numbers

Use one scalar dimension, two noising steps, and

$$
\alpha_1=\alpha_2=\tfrac12,\qquad
\beta_2=\tfrac12,\qquad \bar\alpha_1=\tfrac12,\quad\bar\alpha_2=\tfrac14.
$$

Take the known clean value $x_0=1$ and a noisy value $x_2=0.5$. This is a continuous example, separate from the binary chain in §1.

First calculate the teacher variance:

$$
\tilde\beta_2=\frac{1-1/2}{1-1/4}\frac12=\frac13.
$$

Both mean coefficients equal $\sqrt2/3$, so

$$
\tilde\mu_2=\frac{\sqrt2}{3}(x_2+x_0)
=\frac{\sqrt2}{3}(0.5+1)=0.707107.
$$

Thus the teacher is $q(x_1\mid x_2=0.5,x_0=1)=\mathcal N(0.707107,1/3)$. Suppose the network predicts $p_\theta(x_1\mid x_2=0.5)=\mathcal N(0.2,1/3)$. Equal variances cancel every covariance term:

$$
K_2=\frac{(0.707107-0.2)^2}{2(1/3)}=0.385736.
$$

There is no need to sample $x_1$ to calculate this local KL. Its derivative with respect to the predicted mean is

$$
\frac{\partial K_2}{\partial\mu_\theta}
=\frac{0.2-0.707107}{1/3}=-1.521320.
$$

As a scalar illustration of gradient descent, updating this mean with step size $0.1$ gives

$$
\mu_{\rm new}=0.2-0.1(-1.521320)=0.352132,
$$

and reduces the local KL to $0.189011$. A neural network propagates the mean gradient through its shared weights; this scalar update is not a claim that every input's mean is an independent parameter.

### 7.5 Why the teacher can use the clean image when the model cannot

In the binary example, for $x_2=0$,

$$
q(x_1=0\mid x_2=0,A)=\frac{0.36}{0.36+0.08}=\frac9{11},
$$

$$
q(x_1=0\mid x_2=0,B)=\frac{0.03}{0.03+0.06}=\frac13.
$$

One model prediction given $x_2=0$ cannot equal both teacher predictions. Averaging the teachers over the clean images compatible with this noisy state recovers the true reverse:

$$
\frac{44}{53}\frac9{11}+\frac9{53}\frac13=\frac{39}{53}.
$$

More generally, the $\theta$-dependent part of the averaged teacher KL is

$$
-\mathbb E_{q(x_0,x_t,x_{t-1})}\log p_\theta(x_{t-1}\mid x_t)
=-\mathbb E_{q(x_t,x_{t-1})}\log p_\theta(x_{t-1}\mid x_t).
$$

So averaging over real training images trains the model toward the true reverse conditional. Over unrestricted conditional distributions, this cross-entropy is minimized by that true reverse. A Gaussian model class need not represent a non-Gaussian reverse exactly. Also, individual teacher KLs need not vanish even for the exact reverse; the teacher knows more than the model input does.

This also answers the original Monte Carlo question. The exact value of $D_{\rm KL}(q(x_{t-1}\mid x_t)\|p_\theta(x_{t-1}\mid x_t))$ involves the generally unknown log density of the true reverse. But that log-$q$ contribution is constant with respect to $\theta$. We can train its model-dependent cross-entropy from forward-generated pairs without evaluating the true reverse density.

At the whole-chain level, reverse factorization gives another useful identity, assuming the displayed divergences are finite:

$$
\begin{aligned}
D_{\rm KL}(q(x_{0:T})\|p_\theta(x_{0:T}))
={}&D_{\rm KL}(q(x_T)\|p(x_T))\\
&+\sum_{t=1}^T\mathbb E_{q(x_t)}
D_{\rm KL}(q(x_{t-1}\mid x_t)\|p_\theta(x_{t-1}\mid x_t)).
\end{aligned}
$$

Combined with §1.5's joint-KL decomposition, it connects the original two targets: reverse-step matching and posterior-path matching are views of one joint model. Exact reverse steps **and** the correct terminal marginal make this joint KL zero, hence also make image KL zero. There is no second independent training stage that must fit a new path-posterior network.

## 8. From local Gaussian KL to the noise-prediction loss

Generate a chosen noisy state directly:

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon,
\qquad\epsilon\sim\mathcal N(0,I_d).
$$

Here $\epsilon$ is the aggregate noise in the marginal $q(x_t\mid x_0)$; it is not necessarily the individual forward increment $\epsilon_t$.

Substituting for $x_0$ in the teacher mean yields

$$
\tilde\mu_t=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon\right).
$$

Parameterize the network mean in the same way using its prediction $\epsilon_\theta$:

$$
\mu_\theta(x_t,t)=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right).
$$

Subtract the means, square, and divide by $2s_t^2$. For $t\geq2$, the parameter-dependent local loss becomes

$$
\boxed{\lambda_t\|\epsilon-\epsilon_\theta(x_t,t)\|^2,
\qquad \lambda_t=\frac{\beta_t^2}{2s_t^2\alpha_t(1-\bar\alpha_t)}.}
$$

Thus the weighted noise-prediction loss is an algebraic reparameterization of the mean loss, under the stated fixed-variance assumptions. For the scalar numbers in §7.4, $\epsilon=0$, $\epsilon_\theta=0.621076$, and $\lambda_2=1$, giving the same $0.385736$.

The intermediate sum can be estimated by choosing $t$ uniformly from $\{2,\ldots,T\}$, sampling $\epsilon$, forming $x_t$, and using $(T-1)K_t(x_0,x_t)$. This is an unbiased estimator of that sum; reconstruction and terminal terms remain separate. Training therefore need not simulate or differentiate through the full [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#7.2 Sampling starts from noise|reverse sampling chain]].

Integrating the teacher's $x_{t-1}$ analytically replaces a random local target with its conditional expectation. This removes that source of Monte Carlo variance; randomness in $x_0$, $t$, and $x_t$ remains.

The widely used simplified objective drops the $\lambda_t$ weights and averages plain noise MSE over timesteps. That is a **reweighted training objective**, not an additional exact equality to the complete ELBO. The $t=1$ decoder also deserves separate treatment when evaluating likelihood, especially for discrete pixel values. See [DDPM, equations (12)–(14) and §3.3–3.4](https://arxiv.org/html/2006.11239v2#S3.S4).

## 9. Is a closed form the essential difference between VAE and diffusion?

My follow-up, paraphrased: *Does a VAE have a closed form, and is the absence of one why diffusion needs more algebra before it becomes optimizable?*

**No. Both models usually optimize an ELBO using sampled expectations.** The difference here is the chosen latent structure and inference distribution. A standard VAE learns an encoder for a latent code. A standard DDPM uses a fixed Gaussian noising chain as an encoder for many latent states, and learns the reverse transitions.

| Quantity                                           | Standard Gaussian-encoder VAE                                    | Standard Gaussian DDPM                                                     |
| -------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Exact marginal image likelihood                    | Usually intractable with nonlinear decoder                       | Usually intractable after marginalizing the nonlinear chain                |
| Prior KL in the direct VAE-shaped expression       | Analytic for diagonal Gaussian encoder and standard normal prior | Full-path prior KL generally has no joint-Gaussian formula                 |
| Posterior-gap KL                                   | Generally not analytic                                           | Generally not analytic                                                     |
| Reconstruction expectation                         | Usually sampled                                                  | Usually sampled                                                            |
| Analytic KLs used in practice                      | Encoder-versus-prior Gaussian KL                                 | Terminal KL and each teacher-versus-reverse Gaussian KL at fixed $x_0,x_t$ |
| Remaining randomness                               | Data and latent samples                                          | Data, noisy state, and sampled timestep                                    |
| Is a fully analytic expectation required to train? | No                                                               | No                                                                         |
| What requires care with sampling gradients?        | Learned encoder sampling depends on $\phi$                       | Fixed forward sampling does not depend on reverse parameters $\theta$      |

### 9.1 Is “no joint-Gaussian formula” the key difference at this step?

My follow-up: “is this line going to be the essential difference?” — referring to the table's “no joint-Gaussian formula”.

**Yes, as a computational distinction at this particular step of the ELBO derivation; no, as the defining difference between VAE and diffusion.** It is a consequence of the chosen latent structure and distributions.

For a standard Gaussian-encoder VAE and fixed image $x$,

$$
D_{\rm KL}(q_\phi(z\mid x)\|p(z))
$$

already compares two Gaussians, so we can immediately apply the Gaussian KL formula (§6.3).

For diffusion, the analogous latent variable is the **whole path** $Z=(x_1,\ldots,x_T)$, and the corresponding prior KL is

$$
D_{\rm KL}(q(Z\mid x_0)\|p_\theta(Z)),
\qquad
p_\theta(Z)=p(x_T)\prod_{t=2}^Tp_\theta(x_{t-1}\mid x_t).
$$

- $q(Z\mid x_0)$ **is jointly Gaussian** for the standard fixed linear-Gaussian forward process and fixed clean image $x_0$.
- $p_\theta(Z)$ **generally is not jointly Gaussian**, because the reverse-transition means are nonlinear neural-network functions (§5.2). Gaussian conditionals do not imply a Gaussian joint.
- **The whole-path prior $p_\theta(Z)$ is not just the Gaussian terminal prior $p(x_T)$.** The former also includes all the reverse transitions among the latent states.

Thus two means and covariance matrices cannot generally evaluate the whole-path KL. Instead, §7's exact rearrangement exposes the terminal KL and local terms

$$
D_{\rm KL}\!\left(q(x_{t-1}\mid x_t,x_0)\,\|\,p_\theta(x_{t-1}\mid x_t)\right),
\qquad t\geq2.
$$

**Once $x_0,x_t$ are fixed, both distributions in each local term are Gaussian.** We integrate over $x_{t-1}$ analytically; the outer expectation over $x_t$ generally still requires sampling. This is the variance-reducing rearrangement in [DDPM, equations (5)–(7)](https://arxiv.org/html/2006.11239v2#S2).

> **VAE:** apply the Gaussian KL formula directly to the latent prior KL.  
> **Diffusion:** factor the path comparison into conditional KLs, then apply that formula locally.  
> **Qualification:** diffusion was already trainable by Monte Carlo before this rearrangement. The algebra improves training efficiency rather than making optimization possible for the first time.

### 9.2 Density evaluation, integration, and optimization are different operations

The useful distinction is among three operations:

1. **Evaluate a density at a sampled point.** A network outputs its parameters, then a density formula gives a number.
2. **Integrate an expectation analytically.** Gaussian KLs permit this through known means and covariances.
3. **Optimize parameters.** Stochastic gradients often suffice even when operation 2 is unavailable.

Diffusion's extra rearrangement exposes analytic **inner** expectations and an efficient training procedure. It neither removes all sampling nor supplies a closed-form optimizer for neural-network weights.

## 10. Keep importance sampling separate from Jensen

My photograph also contains a logarithm of a Monte Carlo average. For either model, use $Z$ to denote all its latent variables and sample $Z^{(m)}\sim q(Z\mid x)$. Define

$$
w_m=\frac{p_\theta(x,Z^{(m)})}{q(Z^{(m)}\mid x)}.
$$

These two expressions estimate different quantities:

$$
\underbrace{\log\left(\frac1M\sum_mw_m\right)}_{\text{log of an importance estimate of }p_\theta(x)},
\qquad
\underbrace{\frac1M\sum_m\log w_m}_{\text{Monte Carlo estimate of the ELBO}}.
$$

The likelihood estimate before taking the log is unbiased under the usual support/integrability assumptions. Its logarithm is generally biased downward in expectation; an individual realization need not be below the true log likelihood. The average of log weights is unbiased for the ELBO when the log weight is integrable. For $M=1$, the two sample expressions coincide, but their target distinction still matters.

At the population level, moving from $\log\mathbb E_q[w]$ to $\mathbb E_q[\log w]$ is precisely Jensen's lower-bound step. Choosing a Gaussian reverse family, estimating expectations by sampling, and discarding timestep weights are separate modeling or computational decisions.

## Connections

- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]] — Supplies the likelihood, importance-sampling, Jensen, and posterior-gap routes; replacing one latent code by a path applies the same reasoning to diffusion.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/Model error versus inference error in variational inference|Model error versus inference error in variational inference]] — The binary example complements its counterexample: here the image distribution is correct while posterior-path agreement is imperfect.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/Reparameterization - moving the parameter out of the sampling distribution|Reparameterization - moving the parameter out of the sampling distribution]] — Explains how VAE encoder gradients pass through sampled latents, and how diffusion samples a chosen noisy state from parameter-free noise.
- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Variational autoencoders|Variational autoencoders]] — Provides the model being compared with diffusion; the shared ELBO principle accommodates different latent structures and inference distributions.

## Origin

> [!info]- Source details
> First digest of Codex chat `01a1c712-3362-7152-bbd4-5935a3c601b0`, through the request to add closed-form calculations and create this new note. Preserves my substantive questions about correct images versus hidden paths and the VAE analogy. My uploaded likelihood/importance-sampling/Jensen derivation is typeset in §3; the original [[raw/assets/2026-11-10-VAE-diffusion-I01-handwritten-ELBO.jpg|handwriting]] is preserved unchanged and linked rather than displayed, as requested.
>
> Earlier context: [[raw/conversations/2026-11-10-Diffusion-Approximation-Order.json|supplied ChatGPT export]], its active public user/assistant branch; and [[raw/notes/2026-11-10-Lec12-diffusion-models.pdf|Lec12 diffusion models]], focused PDF pages 6–19 and 21–22. The complete original files are preserved, but the remaining lecture pages and export metadata/alternative branches are not claimed as digested learning content.
>
> Extension (2026-11-11): at my request, §9.1 preserves the assistant's explanation of the selected “no joint-Gaussian formula” line: a computational distinction at the prior-KL step, not a definition of diffusion or a barrier to stochastic training. No new original files or conceptual connections were added.
>
> The assistant added the binary counterexample, Gaussian numerical examples, checked derivations, and original figure. Qualifications: prior sampling is valid; output agreement does not require path agreement; the ELBO is already trainable before the Gaussian-KL rearrangement; analytic local KLs do not make the full expectation analytic; dropping timestep weights changes the objective. Primary references are cited next to the relevant formulas.
>
> Verification combines analytic factorization/completing-square arguments with exact finite enumeration, scalar quadrature, and multivariate Gaussian quadrature. [[assets/figures/2026-11-11-vae-diffusion/draw_and_check.py|Reproducible figure and checks]] and [[assets/figures/2026-11-11-vae-diffusion/checks.json|numeric results]] accompany the note. The rendered figure was inspected; this does not claim inspection in the live Obsidian app. Boundaries, original hashes, and vault validation are in [[_system/Digest Checkpoints]] and [[_system/Log]].
