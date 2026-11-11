---
id: learning-normal-threshold-mle-full-versus-signs
title: Normal-threshold MLE - full measurements versus signs
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/Maximum likelihood estimation]]"
subject: statistics
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → Maximum likelihood estimation
study_band: U–M
note_types: [practice, derivation, question]
question_roles: [concept-distinction]
source_format: conversation-pdf
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: introduced
aliases: [Normal threshold estimation, MLE from normal observations and threshold indicators]
tags: [atlas/learning, subject/statistics, topic/mle]
connections:
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/MLE invariance]]"
  - "[[Learning/Probability & mathematical foundations/Limits & concentration/CLT and delta method - scaling and transforming estimation error]]"
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Misspecified-model targets]]"
sources:
  - "[[raw/conversations/2026-10-18-MLE-conversation.pdf]]"
  - "[[raw/conversations/2026-10-18-MLE-source-manifest.json]]"
  - "[[raw/assets/mle-2026-10-18/01-problem.png]]"
  - "[[raw/assets/mle-2026-10-18/02-first-attempt.png]]"
  - "[[raw/assets/mle-2026-10-18/03-revised-attempt.png]]"
---

# Normal-threshold MLE - full measurements versus signs

Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Likelihood methods → Maximum likelihood estimation

**The same probability has two estimators because full measurements and their signs contain different information.** Start by deciding which observations the likelihood describes.

![[raw/assets/mle-2026-10-18/01-problem.png]]

*Original exercise: estimate a normal threshold probability, quantify uncertainty, and compare precision with robustness.*

Assume $X_i\overset{\mathrm{iid}}{\sim}N(\theta,1)$, $\theta\in\mathbb R$, with known variance 1. Define $Y_i=I\{X_i>0\}$. With $\Phi$ and $\phi$ the standard normal CDF and density,

$$
\psi=P_\theta(X>0)=P(Z>-\theta)=1-\Phi(-\theta)=\Phi(\theta),
\qquad Z\sim N(0,1).
$$

## One target, two likelihoods

**Full measurements.** For observed $x_1,\ldots,x_n$, the log-likelihood is

$$
\ell_X(\theta)=C-\frac12\sum_{i=1}^n(x_i-\theta)^2,
\qquad
\ell_X'(\theta)=n(\bar x-\theta),
\qquad
\ell_X''(\theta)=-n<0,
$$

where $C$ does not depend on $\theta$. Hence $\hat\theta=\bar X$. The one-to-one parameter change $\psi=\Phi(\theta)$ gives

$$
\boxed{\hat\psi=\Phi(\bar X).}
$$

This is [MLE invariance](https://stat135.berkeley.edu/fall-2026/Modules/11-DeltaMethod.html#estimating-a-function-of-parameter-with-mle): the observations stay the same while the parameter is relabeled.

**Signs only: my revised derivation.** For $m=\sum_i y_i$ and $0<\psi<1$,

$$
L_Y(\psi)=\psi^m(1-\psi)^{n-m},
\qquad
\ell_Y'(\psi)=\frac m\psi-\frac{n-m}{1-\psi}
=\frac{m-n\psi}{\psi(1-\psi)}.
$$

For $0<m<n$, the score vanishes at $m/n$, and

$$
\ell_Y''(\psi)=-\frac m{\psi^2}-\frac{n-m}{(1-\psi)^2}<0,
\qquad
\boxed{\tilde\psi=\bar Y.}
$$

![[raw/assets/mle-2026-10-18/03-revised-attempt.png|550]]

*My corrected sample-likelihood calculation gives the sign-data estimator. The clean notation uses $\tilde\psi$ for this result and reserves $\hat\psi$ for the full-data MLE.*

On the Bernoulli parameter space $[0,1]$, all-zero/all-one samples give boundary maxima 0/1. If restricted to $\psi=\Phi(\theta)\in(0,1)$, these are boundary suprema, not attained maxima.

My Bernoulli algebra is valid. The earlier assistant's approval as the full-data answer to part (a) was the error: replacing $X_i$ by signs changes the observed-data likelihood. Parts (c)–(d) explicitly distinguish the two estimators.

## If ψ is already a probability, whose distribution do we need?

*My question, paraphrased from PDF p. 4:* “Would finding a distribution for $\psi=P(X>0)$ mean taking a probability of a probability?”

In this model, $\psi$ is a fixed unknown number. Across repeated samples, **$\hat\psi=\Phi(\bar X)$ varies**. Its sampling distribution supplies the confidence interval.

Since $\bar X\sim N(\theta,1/n)$ exactly and $\Phi'=\phi$, the [[Learning/Probability & mathematical foundations/Limits & concentration/CLT and delta method - scaling and transforming estimation error#Delta method: multiply the error by the derivative|delta method]] gives, for fixed finite $\theta$,

$$
\sqrt n(\hat\psi-\psi)\xrightarrow{d}N(0,\phi(\theta)^2),
\qquad
\widehat{\operatorname{SE}}(\hat\psi)=\frac{\phi(\bar X)}{\sqrt n}.
$$

Thus part (b)'s approximate 95% Wald interval is

$$
\boxed{\Phi(\bar X)\pm1.96\,\frac{\phi(\bar X)}{\sqrt n}.}
$$

It can extend outside $[0,1]$. Under the same known-variance normal model, transforming the exact interval for $\theta$ instead gives

$$
\left[\Phi\!\left(\bar X-\frac z{\sqrt n}\right),
\Phi\!\left(\bar X+\frac z{\sqrt n}\right)\right],
\qquad z=\Phi^{-1}(0.975).
$$

This has exact 95% coverage: because $\Phi$ is increasing, it contains $\Phi(\theta)$ exactly when the original interval contains $\theta$. It is generally asymmetric around the estimate.

## What keeping only signs costs

The signs are iid Bernoulli$(\psi)$, so the weak law of large numbers gives $\tilde\psi=\bar Y\xrightarrow{p}\psi$, solving part (c). For part (d),

$$
\operatorname{Var}(\tilde\psi)=\frac{\psi(1-\psi)}n,
\qquad
n\operatorname{Var}(\hat\psi)\longrightarrow\phi(\theta)^2.
$$

Using the exercise's **sign/full** variance-ratio convention,

$$
\boxed{\mathrm{ARE}_{\rm exercise}
=\frac{\Phi(\theta)[1-\Phi(\theta)]}{\phi(\theta)^2}.}
$$

At $\theta=0$, this is $\pi/2$: signs have about 1.57 times the asymptotic variance. Some texts define efficiency with the reciprocal ratio.

The comparison holds for every finite $\theta$. For one observation,

$$
\operatorname{Cov}(Y,X)
=\int_{-\theta}^{\infty}z\phi(z)\,dz=\phi(\theta).
$$

Cauchy–Schwarz and $\operatorname{Var}(X)=1$ give $\phi(\theta)^2<\psi(1-\psi)$; equality would require a binary indicator to be affine in a continuous normal variable. The full measurements retain useful magnitude information.

## What survives when the normal model is wrong

For iid observations from an actual law $F$ with finite mean $\mu_F$, the normal working-model formula and the sign estimator converge to

$$
\hat\psi=\Phi(\bar X)\xrightarrow{p}\Phi(\mu_F),
\qquad
\tilde\psi=\bar Y\xrightarrow{p}P_F(X>0).
$$

The first limit uses the LLN and continuity of $\Phi$. The second holds for any iid $F$, even without a finite mean, because the indicators are bounded.

For $X=E-1$ with $E\sim\operatorname{Exp}(1)$, the mean is 0 and variance is 1, but the desired probability is $e^{-1}$ while $\hat\psi\to1/2$. Thus the full-data working estimator is **not generally consistent** under misspecification. Nonnormality alone does not force failure: $X\sim U[-\sqrt3,\sqrt3]$ has $P(X>0)=1/2=\Phi(0)$. This qualifies the wording of part (e).

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Likelihood methods/MLE invariance|MLE invariance]] — Transforms the normal-mean optimizer into a probability estimate without discarding observations.
- [[Learning/Probability & mathematical foundations/Limits & concentration/CLT and delta method - scaling and transforming estimation error|CLT and delta method]] — Derives the error transformation used for the probability interval and the efficiency comparison.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Large-sample inference/Misspecified-model targets|Misspecified-model targets]] — Separates the actual event probability from the limit of the normal working-model estimator.

## Origin

> [!info]- Source details
> Migrated from the [[raw/conversations/2026-10-18-MLE-conversation.pdf|13-page MLE export]], especially pp. 1–7 and 12–13, its exercise image, and the old vault's checked solutions. The probability-of-a-probability question is mine (p. 4, displayed Oct 4, 1:22 PM); the revised Bernoulli score is my handwriting (image 3, p. 6). The first attempt remains in [[raw/assets/mle-2026-10-18/02-first-attempt.png|the source archive]]. Cropped peripheral writing is not reconstructed.
>
> The full-data correction, completed intervals, efficiency proof and part-(e) examples are earlier assistant corrections/completions, checked again here. The export itself ends with part-(b) guidance; it does not contain user solutions to parts (c)–(e). Image order and original-file hashes are recorded in the [[raw/conversations/2026-10-18-MLE-source-manifest.json|preserved manifest]].
