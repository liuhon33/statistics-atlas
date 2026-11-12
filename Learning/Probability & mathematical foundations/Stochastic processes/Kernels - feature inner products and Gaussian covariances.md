---
id: learning-kernels-features-gaussian-covariance
title: Kernels - feature inner products and Gaussian covariances
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Stochastic processes/Continuous-time models/Gaussian processes & Brownian motion/Covariance kernels]]'
subject: probability
backbone_path: Probability & mathematical foundations → Stochastic processes → Continuous-time models → Gaussian processes & Brownian motion → Covariance kernels
study_band: M elective
note_types: [derivation, insight, topic-note]
source_format: [annotated-lecture-pdf, conversation-json]
created: '2026-11-12'
updated: 2026-11-12
status: active
verification: checked
learning_state: unknown
tags: [atlas/learning, subject/probability]
connections:
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms]]'
sources:
- '[[raw/assets/private-course-slides/2026-03-09-Lec09-I02-p27-feature-map.png]]'
- '[[raw/assets/private-course-slides/2026-03-09-Lec09-I03-p29-rbf-handwriting.png]]'
- '[[raw/conversations/2026-08-13-Feature-Map-and-Kernel.json]]'
---

# Kernels - feature inner products and Gaussian covariances

Probability & mathematical foundations → Stochastic processes → Continuous-time models → Gaussian processes & Brownian motion → Covariance kernels

A kernel lets us compute a feature-space inner product from the original inputs. With Gaussian random coefficients, that same inner product becomes a covariance between function values. Your annotations connect these two uses, including an explicit infinite feature map for the Gaussian kernel.

## 1. Why positive semidefiniteness is the right requirement

A real covariance kernel $k:\mathcal X\times\mathcal X\to\mathbb R$ is symmetric, and for **every** finite collection $x_1,\ldots,x_N$ its Gram matrix $K_{ij}=k(x_i,x_j)$ is positive semidefinite:

$$
a^TKa\ge0\qquad\text{for all }a\in\mathbb R^N.
$$

If $K$ is a covariance matrix of $F=(f(x_1),\ldots,f(x_N))^T$, then $a^TKa=\operatorname{Var}(a^TF)$. A negative value would be an impossible variance. Symmetry and this condition across every finite input set—not merely one convenient dataset—are essential. [Rasmussen & Williams, §4.1, p. 80](https://gaussianprocess.org/gpml/chapters/RW4.pdf).

For a finite feature map $\psi(x)\in\mathbb R^M$, define

$$
k_0(x,z)=\psi(x)^T\psi(z),\qquad K_0=\Psi\Psi^T,
$$

where row $i$ of $\Psi$ is $\psi(x_i)^T$. Then

$$
a^TK_0a=(\Psi^Ta)^T(\Psi^Ta)=\|\Psi^Ta\|^2\ge0.
$$

This is the lecture's p. 22 proof: the norm is the reason the Gram matrix works. $K_0$ can be singular when features or inputs are redundant; a valid kernel need not yield a strictly positive-definite matrix on every input list.

## 2. Two concrete feature maps from your annotations

For $x=(x_1,x_2)^T$, the homogeneous degree-two polynomial kernel has

$$
\psi(x)=(x_1^2,\sqrt2x_1x_2,x_2^2)^T,
\qquad
\psi(x)^T\psi(z)=(x^Tz)^2.
$$

Your p. 23 annotation contrasts computing the kernel directly with building the feature vector. The $\sqrt2$ factors produce the cross-term coefficient $2$. A feature map including linear terms would define a different kernel; the map above is specifically for the displayed **homogeneous** square.

Your separate orange example on p. 27 is:

$$
\psi(a,b)=(a,b,a^2+b^2)^T,\qquad \mathbb R^2\longrightarrow\mathbb R^3.
$$

Writing $x=(a_1,b_1)^T$ and $z=(a_2,b_2)^T$, your dot-product calculation gives

$$
\begin{aligned}
k_0(x,z)
&=a_1a_2+b_1b_2+(a_1^2+b_1^2)(a_2^2+b_2^2)\\
&=x^Tz+\|x\|^2\|z\|^2.
\end{aligned}
$$

For example, $x=(1,2)$ and $z=(2,-1)$ have $x^Tz=0$ but $k_0(x,z)=25$: the added squared-radius feature makes them align in feature space.

![[raw/assets/private-course-slides/2026-03-09-Lec09-I02-p27-feature-map.png]]
*Your p. 27 construction, rendered from the private PDF. This is its own kernel, distinct from the preceding homogeneous polynomial example.*

### A simpler starting point from the chat: nonlinear in the input, linear in the weights

For a scalar input, take

$$
\psi(x)=(1,x,x^2)^T,\qquad
f(x)=w^T\psi(x)=w_0+w_1x+w_2x^2.
$$

This can describe a parabola even though the model is **linear in its coefficients**. Its kernel is just

$$
k_0(x,z)=1+xz+x^2z^2.
$$

For $x=2,z=3$, explicitly dotting $(1,2,4)$ with $(1,3,9)$ gives $43$; evaluating $1+6+36$ gives the same answer without constructing either feature vector. That substitution is the kernel trick **when the algorithm uses features only through their inner products**. It is not a way to replace an arbitrary use of $\psi(x)$ by one scalar.

Do not silently identify this with $(1+xz)^2=1+2xz+x^2z^2$. The latter uses $(1,\sqrt2x,x^2)^T$ and gives $49$ for the same pair. The feature weights, not just which powers appear, determine the kernel.

### A circle gives two different periodic kernels

The chat's trigonometric example is particularly useful for time or phase. For period $p>0$, map the line onto the unit circle:

$$
u(x)=\left(\cos\frac{2\pi x}{p},\ \sin\frac{2\pi x}{p}\right)^T.
$$

Then $u(x+p)=u(x)$: one full cycle returns to the same feature vector. **Taking its dot product** gives

$$
k_{\cos}(x,z)=u(x)^Tu(z)=\cos\frac{2\pi(x-z)}p.
$$

At separation $p/2$ the kernel is $-1$, but it is still PSD because it is a feature inner product. With independent standard-normal coefficients $A,B$, the associated GP is $f(x)=A\cos(2\pi x/p)+B\sin(2\pi x/p)$: every draw is a sinusoid, with random amplitude and phase. It is a two-feature model, not a model of every possible periodic shape.

**Applying an RBF kernel to those circle coordinates** gives a different construction. First,

$$
\begin{aligned}
\|u(x)-u(z)\|^2
&=2-2\cos\frac{2\pi(x-z)}p\\
&=4\sin^2\frac{\pi(x-z)}p.
\end{aligned}
$$

Thus, for circle-space length scale $\ell_\circ>0$,

$$
k_{\mathrm{per}}(x,z)
=\exp\left[-\frac{\|u(x)-u(z)\|^2}{2\ell_\circ^2}\right]
=\exp\left[-\frac{2\sin^2(\pi(x-z)/p)}{\ell_\circ^2}\right].
$$

This is the periodic squared-exponential construction in [Rasmussen & Williams, §4.2.3, equation (4.31), p. 92](https://gaussianprocess.org/gpml/chapters/RW4.pdf), with the input rescaled to period $p$. Here $u$ is an **intermediate input transformation**, not the complete two-dimensional feature map of $k_{\mathrm{per}}$: the RBF introduces its own richer feature space. The chat presented both periodic ideas; this extra step makes their difference explicit.

![[assets/figures/2026-11-12-kernel-chat-extension/circle-kernels.svg]]
*Original comparison. The left panel identifies inputs modulo $p$; the right compares the circle dot product with the RBF-on-circle kernel ($\ell_\circ=0.7$). Both repeat after $p$, but only the cosine kernel becomes negative. [[assets/figures/2026-11-12-kernel-chat-extension/build_examples.py|Reproducible source]].*

## 3. Your Gaussian-kernel expansion

For scalar inputs and length scale $\ell=1$, your p. 29 handwriting splits the exponent and expands the middle exponential:

$$
\begin{aligned}
k_0(x,z)&=e^{-(x-z)^2/2}\\
&=e^{-x^2/2}e^{xz}e^{-z^2/2}\\
&=e^{-x^2/2}\left(\sum_{n=0}^{\infty}\frac{x^nz^n}{n!}\right)e^{-z^2/2}\\
&=\sum_{n=0}^{\infty}
\left(e^{-x^2/2}\frac{x^n}{\sqrt{n!}}\right)
\left(e^{-z^2/2}\frac{z^n}{\sqrt{n!}}\right).
\end{aligned}
$$

Hence the feature vector you found is

$$
\psi(x)=e^{-x^2/2}\left(1,x,\frac{x^2}{\sqrt{2!}},\frac{x^3}{\sqrt{3!}},\ldots\right).
$$

The vector has infinitely many coordinates, yet its squared norm is finite:

$$
\sum_{n=0}^{\infty}\psi_n(x)^2
=e^{-x^2}\sum_{n=0}^{\infty}\frac{x^{2n}}{n!}=1.
$$

Thus the inner product is well-defined in the square-summable sequence space. For $\ell>0$, replace $x$ and $z$ by $x/\ell$ and $z/\ell$. In higher input dimensions the factorization uses products of these one-dimensional features.

![[raw/assets/private-course-slides/2026-03-09-Lec09-I03-p29-rbf-handwriting.png]]
*Your p. 29 right-margin derivation, extracted as a labelled source crop. The full annotated page remains in the immutable private PDF. The displayed infinite vector and the convergence check above are a clean transcription plus an added justification.*

![[assets/figures/2026-11-12-gp-ridge/kernel-series.svg]]
*Original analytic illustration with first input 0.9 and $\ell=1$. Truncating the feature vector approximates the full kernel; direct evaluation of the exponential avoids explicitly storing infinitely many features. A truncated inner product can be negative off the diagonal while its Gram matrices remain positive semidefinite.*

Your “similarity in feature space” interpretation is useful here. A kernel is not necessarily a distance or a correlation coefficient: its diagonal can vary, and off-diagonal entries can be negative.

## 4. From feature inner products to function covariances

Hold inputs fixed and put $w\sim\mathcal N(0,S)$, with covariance $S\succeq0$, on the coefficients of $f(x)=\psi(x)^Tw$. Then

$$
\operatorname{Cov}(f(x),f(z))=\psi(x)^TS\psi(z).
$$

For $S=\tau^2I$, the covariance is $k(x,z)=\tau^2 k_0(x,z)$. The lecture uses $\tau^2=1/\alpha$. This distinguishes the unscaled feature Gram matrix on p. 22 from the prior covariance matrix on pp. 28–29.

The [[Learning/Statistical computing & learning/Statistical learning & prediction/Gaussian processes - conditioning by completing the square#1. A Gaussian vector at every finite collection of inputs|GP note]] develops your p. 28 covariance proof. It also explains how choosing a covariance kernel directly specifies joint function-value distributions without explicitly introducing a finite weight vector.

## 5. Building kernels, and what the RBF pictures mean

The rules on p. 24 have simple checks. For valid $k_1,k_2$:

| Construction | Why its Gram matrix remains PSD |
| --- | --- |
| $c\,k_1$, $c\ge0$ | Scales every quadratic form by $c$. |
| $h(x)k_1(x,z)h(z)$ | $K=DK_1D$, so $a^TKa=(Da)^TK_1(Da)\ge0$. |
| $k_1+k_2$ | Adds nonnegative quadratic forms. |
| $k_1k_2$ pointwise | Tensor-product features, equivalently the Schur product theorem. |
| $x^TAz$, $A\succeq0$ | Feature map $A^{1/2}x$. |
| $q(k_1)$, with nonnegative polynomial coefficients | Nonnegative sums of pointwise powers, including the constant kernel. |
| $\exp(k_1)$ pointwise | Limit of its nonnegative-coefficient Taylor polynomials; the finite PSD cone is closed. |

The exponential here is entrywise, not a matrix exponential. The standard closure rules are also discussed in [Rasmussen & Williams, §4.2.4](https://gaussianprocess.org/gpml/chapters/RW4.pdf).

The Gaussian **basis functions** on pp. 15 and 25–26 are features centred at selected locations, for example $\psi_j(x)=\exp(-\|x-c_j\|^2/(2s^2))$. A linear combination in feature space can give a nonlinear curve or decision boundary in input space. Its finite-feature kernel $\sum_j\psi_j(x)\psi_j(z)$ is generally not exactly the translation-invariant Gaussian kernel $\exp(-\|x-z\|^2/(2\ell^2))$. Neither expression needs a probability-density normalization constant merely to serve as a feature or kernel.

The p. 25 picture shows ordinary shifted sigmoid features. Such $h(x-c_j)$ features need not be radial; a truly radial feature depends on $\|x-c_j\|$ and is symmetric around its centre in one dimension. This distinction keeps the slide's illustration from redefining “radial”.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|Inner products and norms]] — a feature inner product creates a Gram matrix, whose quadratic form is a nonnegative squared norm.

## Origin

> [!info]- Source details
> Thibault Randrianarisoa, Gaussian Processes, University of Toronto, 2026-03-09 (original course PDF retained privately).
> Thibault Randrianarisoa, *Gaussian Processes*, University of Toronto, 2026-03-09: kernel section pp. 20–26, the user's custom feature map on p. 27, and the Gaussian-kernel series in the p. 29 margin. The other content on pp. 28–29 belongs to the sibling GP note. All 41 supplied pages were read and visually inspected.
>
> The custom $\mathbb R^2\to\mathbb R^3$ map and exponential-series construction are the user's work. The finite-norm argument, numerical example, closure explanations, feature/kernel distinction and original plot are added synthesis. Kernel identities and series agreement were checked in [[assets/figures/2026-11-12-gp-ridge/checks.json|the shared numerical record]]; the algebra above supplies the proofs. No question from the slide deck is attributed to the user.
>
> Extended on 2026-11-12 from the supplied ChatGPT export [[raw/conversations/2026-08-13-Feature-Map-and-Kernel.json|Feature Map and Kernel]], conversation `6a7e0ad5-f974-83ea-9890-37fcdecd0169`. The opening exchange (`7eb6e36a-23c7-425d-bad9-e28263830270` → `f0877b2a-b4b7-4922-b632-27e09c963035`) supplies the simple scalar and trigonometric examples. These are explanations from the earlier assistant, not newly attributed user derivations. The polynomial-weight comparison, explicit distinction between the two periodic constructions, and circle figure are added checked synthesis. The existing Gaussian-series and feature-covariance explanations were already covered and were not duplicated.
>
> The export's complete visible text was read; its 29 slide-image pointers contain no image bytes and were not visually recovered. The previously archived lecture PDF and handwriting remain separate sources; byte identity with those chat attachments is not asserted. Source boundary/hash and this attachment gap are recorded in [[_system/Digest Checkpoints]] and [[_system/Review Queue]]. New algebra/figure checks: [[assets/figures/2026-11-12-kernel-chat-extension/checks.json]].
