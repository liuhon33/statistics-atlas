---
id: learning-model-versus-inference-error
title: Model error versus inference error in variational inference
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Variational inference]]"
subject: computing
backbone_path: "Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference"
study_band: M
note_types: [insight, topic-note]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-09
status: active
verification: checked
learning_state: unknown
aliases: [Model errors vs inference errors]
tags: [atlas/learning, subject/computing, topic/variational-inference]
connections:
  - "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO]]"
  - "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Posterior KL gap]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Misspecified-model targets]]"
  - "[[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO]]"
sources:
  - "[[raw/assets/2026-11-08-Variational-inference-I01-model-versus-inference-errors.png]]"
  - "[[_system/Sources/vi]]"
---

# Model error versus inference error in variational inference

Statistical computing & learning → Simulation & approximate inference → Approximate & latent-variable inference → Variational inference

**An exact posterior can still come from a wrong model.** My red/purple distinction separates two failures: $p_\theta$ may describe reality poorly, and $q_\phi$ may approximate the posterior implied by $p_\theta$ poorly. Improving the second does not automatically fix the first.

![[raw/assets/2026-11-08-Variational-inference-I01-model-versus-inference-errors.png]]

*My original annotations, preserved unchanged. The red model-error and purple inference-error statements at the bottom are the focus; the upper reparameterization calculation is context, not a second topic digested here.*

## Two parameter sets, two different jobs

For observed data $x$ and latent variables $z$,

$$
p_\theta(x,z)=p_\theta(x\mid z)p_\theta(z),\qquad
p_\theta(z\mid x)=\frac{p_\theta(x,z)}{p_\theta(x)},\qquad
p_\theta(x)=\int p_\theta(x,z)\,dz.
$$

The prior may be fixed rather than depend on $\theta$. For discrete $z$, use a sum; for continuous $z\in\mathbb R^d$, use an integral, rather than the schematic sum in my handwriting. High dimension can make this normalization difficult, but does not by itself guarantee intractability.

- **$\theta$: model parameters.** They specify the assumed joint distribution, hence also its posterior. Learning $\theta$ changes the model we are making inferences about.
- **$\phi$: variational parameters.** They specify a tractable $q_\phi(z\mid x)$ intended to approximate that posterior. With $\theta$ fixed, changing $\phi$ changes the approximation, not the target.

| Error | What is being compared? | What would address it? |
| --- | --- | --- |
| **Model error** | The model's assumptions/distribution versus the real data-generating process | Reconsider the model family, likelihood, prior, or fit of $\theta$ |
| **Inference error** | $q_\phi(z\mid x)$ versus the exact **model-implied** $p_\theta(z\mid x)$ | Use a more expressive variational family or improve inference optimization |

Here “inference error” specifically means posterior-approximation error, not every possible error in statistical inference. “Model error” is broader than misspecification: a poor fitted $\theta$ can also hurt even when the family contains a suitable model. Structural misspecification means changing $\theta$ within that family cannot make it correct.

## The ELBO gap measures inference error, not model truth

Fix $x,\theta$. Assume $0<p_\theta(x)<\infty$, normalized $q_\phi$, absolute continuity of $q_\phi$ with respect to the model posterior, and finite log expectations. Define

$$
\mathcal L(\theta,\phi;x)
=\mathbb E_{q_\phi(z\mid x)}
\left[\log p_\theta(x,z)-\log q_\phi(z\mid x)\right].
$$

Substituting $\log p_\theta(x,z)=\log p_\theta(z\mid x)+\log p_\theta(x)$ gives

$$
\boxed{\log p_\theta(x)-\mathcal L(\theta,\phi;x)
=D_{\mathrm{KL}}\!\left(q_\phi(z\mid x)\,\|\,p_\theta(z\mid x)\right).}
$$

At fixed $\theta$, maximizing the ELBO minimizes this posterior KL. Zero gap means $q_\phi=p_\theta(\cdot\mid x)$ almost everywhere; it does **not** mean $p_\theta$ is true. The target here is the **posterior**, not the prior. [Blei, Kucukelbir & McAuliffe (2017), §2.2, equations (12)–(14), p. 862](https://www.cs.columbia.edu/~blei/papers/BleiKucukelbirMcAuliffe2017.pdf#page=5).

Two useful qualifications:

- Even perfect optimization cannot remove the best-achievable KL gap of a restrictive variational family. Failure to reach that best approximation is an additional optimization issue.
- If $\theta$ and $\phi$ are trained together, $\log p_\theta(x)$ and the posterior target both move. A higher ELBO alone therefore does not prove that inference error fell, or that the model became closer to reality.

## A small counterexample: perfect inference, wrong model

*Assistant-added example.* Suppose reality produces $X\sim\operatorname{Bernoulli}(0.9)$, but our fixed model assumes $X\sim\operatorname{Bernoulli}(0.5)$ and an independent latent $Z\sim\operatorname{Bernoulli}(0.5)$.

For either observation $x$, the exact model posterior is $p_\theta(z\mid x)=\operatorname{Bernoulli}(0.5)$. Choose $q_\phi$ to equal it. The inference KL is **zero**, and the ELBO equals $\log p_\theta(x)=\log(0.5)$. Yet the model still predicts heads half the time when reality produces heads 90% of the time.

Conversely, keeping the latent independent but correcting the model to $X\sim\operatorname{Bernoulli}(0.9)$ fixes its observed-data distribution. Choosing $q_\phi(Z=1\mid x)=0.8$ would still give an incorrect posterior approximation: the target remains $0.5$.

**Takeaway:** first ask whether the model is adequate; separately ask whether its posterior is approximated accurately. The handwritten “+” flags two sources of error, not a universal additive decomposition of prediction loss.

## Connections

- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO|ELBO]] — Optimizing the bound has different interpretations when only the approximation changes versus when the generative model also changes.
- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/Posterior KL gap|Posterior KL gap]] — The exact evidence-minus-ELBO gap measures disagreement with the model posterior, not disagreement with reality.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Misspecified-model targets|Misspecified-model targets]] — A model family may remain wrong even after its parameters are well fitted; exact inference does not enlarge that family.
- [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO|My four approaches to the ELBO]] — Its posterior-KL derivation supplies the identity used here; this note separates that inference gap from model adequacy.

## Origin

One supplied annotated screenshot, specifically its red/purple model-versus-inference distinction and the roles of $\theta$ and $\phi$. No new question wording is attributed to me. The assistant added the comparison table, notation cleanup, ELBO interpretation, qualifications, and Bernoulli counterexample; checked the identity algebraically against the cited review and checked the example by direct enumeration. The clipped upper slide and reparameterization derivation are preserved in the image but not reconstructed or claimed verified. Original bytes and source boundary are recorded in [[_system/Digest Checkpoints]].
