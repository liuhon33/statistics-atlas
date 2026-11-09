---
id: learning-reparameterization-fixed-noise
title: Reparameterization - moving the parameter out of the sampling distribution
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Reparameterization gradient]]"
subject: computing
backbone_path: Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → Reparameterization gradient
study_band: M
note_types: [derivation, insight]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-09
status: active
verification: checked
aliases: [Reparameterization trick, Differentiating a parameter-dependent expectation]
tags: [atlas/learning, subject/computing, topic/reparameterization, study/masters]
connections:
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO]]"
  - "[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Change of variables]]"
sources:
  - "[[raw/assets/2026-11-08-Reparameterization-I01-parameter-dependent-expectation.png]]"
  - "[[raw/assets/2026-11-08-Reparameterization-I02-change-of-variables.png]]"
  - "[[raw/assets/2026-11-08-Reparameterization-I03-normal-toy-example.png]]"
---

# Reparameterization - moving the parameter out of the sampling distribution

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference → Reparameterization gradient

**Differentiating an expectation must account for both the function and the distribution changing.** My notes first identify the missing density-derivative term, then use a change of variables to put all parameter dependence inside a function of fixed-distribution noise. The normal example shows why treating a sampled value as constant gives the wrong answer.

## 1. The missing term when the distribution depends on the parameter

![[raw/assets/2026-11-08-Reparameterization-I01-parameter-dependent-expectation.png]]

*Original page 1: fixed-distribution differentiation, the circled missing term, and the beginning of the change-of-variables argument. Only the handwriting is digested; printed slide content is not a source for the explanation.*

For fixed outcomes $y_i$ and probabilities $\pi_i$ independent of the scalar parameter $\psi$,

$$
J(\psi)=\sum_{i=1}^m\pi_i f(y_i,\psi)
\quad\Longrightarrow\quad
J'(\psi)=\sum_{i=1}^m\pi_i\frac{\partial f(y_i,\psi)}{\partial\psi}.
$$

The continuous version, with a fixed density $r$, is

$$
J(\psi)=\int f(y,\psi)r(y)\,dy,
\qquad
J'(\psi)=\int \partial_\psi f(y,\psi)r(y)\,dy.
$$

But if $Y_\psi\sim p_\psi$, then

$$
\begin{aligned}
J(\psi)&=\mathbb E_{Y\sim p_\psi}[f(Y,\psi)]
=\int f(y,\psi)p_\psi(y)\,dy,\\
J'(\psi)&=\int \partial_\psi f(y,\psi)p_\psi(y)\,dy
+\underbrace{\int f(y,\psi)\partial_\psi p_\psi(y)\,dy}_{\text{the term marked “missed!” in my notes}}.
\end{aligned}
$$

Here $\partial_\psi f(y,\psi)$ holds $y$ fixed. It does not capture changes in how likely different values of $y$ are.

**Conditions added in this digest.** Moving a derivative through an integral needs justification. Sufficient local conditions are differentiability almost everywhere and an integrable bound on the differentiated integrand in a neighborhood of the parameter. The product-rule display assumes a fixed integration domain with this regularity. A moving support can require boundary terms; it cannot automatically be handled by differentiating only the interior density.

## 2. Change variables so the noise distribution is fixed

Choose a transformation $g_\psi$ such that

$$
\varepsilon\sim r,\qquad r\text{ does not depend on }\psi,
\qquad Y_\psi=g_\psi(\varepsilon)\sim p_\psi.
$$

My interval argument preserves probability mass. For a small interval around $\varepsilon$,

$$
\Delta y\approx\left|\frac{\partial g_\psi(\varepsilon)}{\partial\varepsilon}\right|\Delta\varepsilon,
\qquad
r(\varepsilon)\Delta\varepsilon
\approx p_\psi(g_\psi(\varepsilon))\Delta y.
$$

For a one-to-one differentiable transformation with nonzero derivative on the relevant support, the density identity is

$$
p_\psi(g_\psi(\varepsilon))
\left|\frac{\partial g_\psi(\varepsilon)}{\partial\varepsilon}\right|
=r(\varepsilon).
$$

Consequently,

$$
\begin{aligned}
J(\psi)
&=\int f(g_\psi(\varepsilon),\psi)
p_\psi(g_\psi(\varepsilon))
\left|\frac{\partial g_\psi(\varepsilon)}{\partial\varepsilon}\right|\,d\varepsilon\\
&=\int f(g_\psi(\varepsilon),\psi)r(\varepsilon)\,d\varepsilon\\
&=\mathbb E_{\varepsilon\sim r}[f(g_\psi(\varepsilon),\psi)].
\end{aligned}
$$

![[raw/assets/2026-11-08-Reparameterization-I02-change-of-variables.png]]

*Original page 2: the density–Jacobian product becomes $r(\varepsilon)$, followed by the normal substitution. Printed material is ignored.*

**What becomes parameter-independent is the noise law, not $Y_\psi$ or the whole integrand.** The density and Jacobian need not be individually independent of $\psi$; their product equals the fixed density $r$.

The one-to-one condition above justifies this particular density calculation. The expectation identity itself only needs $g_\psi(\varepsilon)$ to have the required distribution; it does not require an invertible map. Differentiating that identity still requires its own regularity conditions.

## 3. Normal substitution and the total derivative

My normal example takes

$$
Y_\psi\sim\mathcal N(\mu(\psi),\sigma(\psi)^2),\qquad
\varepsilon\sim\mathcal N(0,1),\qquad
Y_\psi=\mu(\psi)+\sigma(\psi)\varepsilon,
\quad\sigma(\psi)>0.
$$

At fixed $\psi$,

$$
\varepsilon=\frac{y-\mu(\psi)}{\sigma(\psi)},\qquad
dy=\sigma(\psi)\,d\varepsilon.
$$

The density's $1/\sigma(\psi)$ and the Jacobian $\sigma(\psi)$ cancel:

$$
\begin{aligned}
J(\psi)
&=\int_{-\infty}^{\infty}f(y,\psi)
\frac{1}{\sigma(\psi)\sqrt{2\pi}}
\exp\!\left(-\frac{(y-\mu(\psi))^2}{2\sigma(\psi)^2}\right)\,dy\\
&=\int_{-\infty}^{\infty}f(\mu(\psi)+\sigma(\psi)\varepsilon,\psi)
\frac{e^{-\varepsilon^2/2}}{\sqrt{2\pi}}\,d\varepsilon.
\end{aligned}
$$

Now differentiate while holding $\varepsilon$ fixed:

$$
\boxed{
J'(\psi)=\mathbb E_{\varepsilon\sim\mathcal N(0,1)}
\left[
\partial_y f(Y_\psi,\psi)
\bigl(\mu'(\psi)+\sigma'(\psi)\varepsilon\bigr)
+\partial_\psi f(Y_\psi,\psi)
\right].
}
$$

The first term follows the changing sample value; the second is the explicit parameter dependence of $f$. The distribution-change contribution has not been discarded: in this representation it is accounted for through $g_\psi$.

**Correction to the handwritten chain-rule line:** the scale derivative must be $\sigma'(\psi)\varepsilon$, not just $\sigma'(\psi)$. The original remains unchanged. Also, $\partial_\varepsilon g_\psi$ is the Jacobian used in substitution, whereas $\partial_\psi g_\psi$ is the derivative used for optimization; they are different operations.

## 4. Toy example: a zero partial derivative does not imply a zero gradient

![[raw/assets/2026-11-08-Reparameterization-I03-normal-toy-example.png]]

*Original page 3: $Y_\psi\sim\mathcal N(\psi,1)$ and $f(y,\psi)=y^2$, including the crossed-out zero-gradient calculation. Printed slide equations are excluded.*

My direct calculation gives

$$
J(\psi)=\mathbb E[Y_\psi^2]
=\operatorname{Var}(Y_\psi)+(\mathbb E Y_\psi)^2
=1+\psi^2,
\qquad J'(\psi)=2\psi.
$$

The incorrect route uses $\partial_\psi(y^2)=0$ with $y$ held fixed, and silently treats $p_\psi$ as constant. Reparameterizing instead gives

$$
J(\psi)=\mathbb E_{\varepsilon\sim\mathcal N(0,1)}[(\psi+\varepsilon)^2],
\qquad
J'(\psi)=\mathbb E[2(\psi+\varepsilon)]=2\psi.
$$

**Check added in the digest:** the missing density term gives the same answer. Since $\partial_\psi p_\psi(y)=(y-\psi)p_\psi(y)$,

$$
\int y^2\partial_\psi p_\psi(y)\,dy
=\mathbb E[(\psi+\varepsilon)^2\varepsilon]
=\psi^2\mathbb E\varepsilon+2\psi\mathbb E\varepsilon^2+\mathbb E\varepsilon^3
=2\psi.
$$

Both representations recover the gradient; only the naive fixed-sample partial derivative loses it.

## Connections

- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]] — That note derives the variational objective; this note explains how to differentiate an expectation when its variational sampling distribution depends on the parameter being optimized.
- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Change of variables|Change of variables]] — Probability-mass preservation and the Jacobian rewrite the parameter-dependent density as a fixed noise density, which is the central step of the handwritten derivation.

## Origin

Digested from my three supplied handwritten screenshots, in order. All originals are preserved byte-for-byte and embedded beside their corresponding reasoning. Non-handwritten slide text and equations were deliberately ignored. The notation is standardized to $p_\psi$ for the parameter-dependent density, $r$ for the fixed noise density, and $g_\psi$ for the transformation; the screenshots alternate density symbols.

The missing-term argument, change of variables, normal substitution and toy example are my handwritten work. Codex added the regularity/support qualifications, the distinction between the two derivatives of $g$, the explicit chain-rule correction, and the final density-term check. Verification covers these equations under the stated assumptions, not any unseen lecture or source chat.
