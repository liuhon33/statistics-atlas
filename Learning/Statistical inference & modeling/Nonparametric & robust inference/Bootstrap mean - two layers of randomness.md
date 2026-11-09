---
id: learning-bootstrap-mean-two-layers
title: Bootstrap mean - two layers of randomness
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Nonparametric & robust inference/Resampling inference/Bootstrap & jackknife/Conditional versus unconditional bootstrap variation]]"
subject: statistics
backbone_path: "Statistical inference & modeling → Nonparametric & robust inference → Resampling inference → Bootstrap & jackknife → Conditional versus unconditional bootstrap variation"
study_band: U–M
note_types: [practice, derivation, question]
question_roles: [concept-distinction, assumption-boundary]
source_format: conversation-pdf
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
learning_state: practicing
aliases: [Conditional and unconditional bootstrap mean moments]
tags: [atlas/learning, subject/statistics, topic/bootstrap, study/undergraduate-masters]
connections:
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Total variance]]"
  - "[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional independence]]"
sources:
  - "[[raw/conversations/2026-10-18-Estimating-Interval-Probability.pdf]]"
  - "[[raw/conversations/2026-10-18-Estimating-Interval-Probability-manifest.json]]"
  - "[[raw/assets/2026-10-18-interval-probability-03-bootstrap-exercise.png]]"
  - "[[raw/assets/2026-10-18-interval-probability-04-bootstrap-moments.png]]"
---

# Bootstrap mean - two layers of randomness

Statistical inference & modeling → Nonparametric & robust inference → Resampling inference → Bootstrap & jackknife → Conditional versus unconditional bootstrap variation

**A bootstrap mean varies in two ways:** resampling changes the mean within one fixed dataset, and drawing a new original dataset changes the center around which those resamples fluctuate.

**My core question, paraphrased from the exercise-5 discussion:** What changes when we calculate moments under the population law $F$, rather than conditional on the observed sample?

## The exercise and the two experiments

![[raw/assets/2026-10-18-interval-probability-03-bootstrap-exercise.png]]

*Original exercise 5: find the bootstrap mean's conditional and unconditional mean and variance.*

| Experiment | What stays fixed? | What varies? |
| --- | --- | --- |
| Conditional bootstrap | The observed dataset $D$ and its empirical distribution | The resampling indices and bootstrap sample |
| Unconditional two-stage experiment | The population law $F$ | First the original dataset, then its bootstrap sample |

Use the standard iid model: $D=(X_1,\ldots,X_n)$ with $n\geq1$, $X_i\sim F$, $\mu=E[X_i]$, and finite variance $\sigma^2=\operatorname{Var}(X_i)$. All observations are scalar.

To resample, draw $J_1,\ldots,J_n$ independently and uniformly from $\{1,\ldots,n\}$, independently of $D$, and set $X_j^*=X_{J_j}$. Given $D$, these are iid draws from the empirical distribution $\widehat F_n$. This is sampling with replacement; see [the CMU-hosted bootstrap chapter, §11.2, p. 210](https://www.stat.cmu.edu/~larry/=sml/Boot.pdf#page=2).

The exercise assumes no ties. The same calculations work with ties because indices still have probability $1/n$ and repeated values combine their masses. For $(2,2,5,7)$, the resampled value 2 has probability $1/2$.

Write

$$
\bar X=\frac1n\sum_{i=1}^nX_i,\qquad
\bar X^*=\frac1n\sum_{j=1}^nX_j^*,\qquad
v_n=\frac1n\sum_{i=1}^n(X_i-\bar X)^2.
$$

The empirical variance $v_n$ uses denominator $n$. For $n\geq2$, the usual unbiased sample variance is $s^2=nv_n/(n-1)$.

The exercise's $E_{\widehat F_n}$ and $V_{\widehat F_n}$ mean conditioning on $D$. Its $E_F$ and $V_F$ average over **both** stages, while $F$ itself stays fixed.

## 1. Hold the data fixed

A single resampled observation has

$$
E[X_j^*\mid D]=\frac1n\sum_iX_i=\bar X,
\qquad
\operatorname{Var}(X_j^*\mid D)=v_n.
$$

Conditional independence gives

$$
\boxed{E[\bar X^*\mid D]=\bar X,\qquad
\operatorname{Var}(\bar X^*\mid D)=\frac{v_n}{n}.}
$$

The conditional distribution is centered at the observed sample mean. Neither $\bar X$ nor $v_n$ varies during this fixed-data experiment.

## 2. Let the original data vary: my total-variance derivation

![[raw/assets/2026-10-18-interval-probability-04-bootstrap-moments.png]]

*My handwritten calculation separates the two variance components and obtains $(2n-1)\sigma^2/n^2$. The equations below make the notation explicit.*

Total expectation immediately gives

$$
\boxed{E[\bar X^*]=E\{E[\bar X^*\mid D]\}=E[\bar X]=\mu.}
$$

For the variance, first average the empirical variance across original samples:

$$
\begin{aligned}
E[v_n]
&=E\left[\frac1n\sum_iX_i^2-\bar X^2\right]\\
&=(\sigma^2+\mu^2)-(\sigma^2/n+\mu^2)\\
&=\frac{n-1}{n}\sigma^2.
\end{aligned}
$$

Now apply total variance:

$$
\begin{aligned}
\operatorname{Var}(\bar X^*)
&=\underbrace{E\{\operatorname{Var}(\bar X^*\mid D)\}}_{\text{within datasets}}
+\underbrace{\operatorname{Var}\{E[\bar X^*\mid D]\}}_{\text{between dataset centers}}\\
&=E[v_n/n]+\operatorname{Var}(\bar X)\\
&=\frac{n-1}{n^2}\sigma^2+\frac{\sigma^2}{n}\\
&=\boxed{\frac{2n-1}{n^2}\sigma^2.}
\end{aligned}
$$

The second term is essential: different original datasets have different sample means. These conditioning laws are reviewed in [ProbabilityCourse §5.1.5](https://www.probabilitycourse.com/chapter5/5_1_5_conditional_expectation.php).

## 3. A second explanation: conditional independence disappears after averaging

For two distinct resampling positions $j\ne k$ with $n\geq2$, conditional independence implies

$$
E[X_j^*X_k^*\mid D]=\bar X^2.
$$

But without conditioning,

$$
\operatorname{Cov}(X_j^*,X_k^*)
=E[\bar X^2]-\mu^2
=\operatorname{Var}(\bar X)
=\frac{\sigma^2}{n}.
$$

Both draws share the same random original dataset. When that dataset's center is high, both draws tend to be high; when it is low, both tend to be low. For $\sigma^2>0$, their positive covariance rules out unconditional independence.

Each individual $X_j^*$ still has marginal distribution $F$, since its independently selected index is uniform over iid observations. Thus

$$
\begin{aligned}
\operatorname{Var}(\bar X^*)
&=\frac1{n^2}\left[n\sigma^2+n(n-1)\frac{\sigma^2}{n}\right]\\
&=\frac{2n-1}{n^2}\sigma^2.
\end{aligned}
$$

This recovers my total-variance result by accounting for covariance between resampled observations. Saying only “the bootstrap draws are iid” hides the conditioning needed for that statement.

## 4. Which variance does the bootstrap use?

The ordinary bootstrap variance estimate for the original sample mean is

$$
\widehat{\operatorname{Var}}_{\mathrm{boot}}(\bar X)
=\operatorname{Var}(\bar X^*\mid D)=\frac{v_n}{n}.
$$

It estimates $\operatorname{Var}_F(\bar X)=\sigma^2/n$. Its finite-sample expectation is $(n-1)\sigma^2/n^2$. The larger unconditional variance also includes the movement of $\bar X$ between original datasets.

Centering makes that difference explicit:

$$
E[\bar X^*-\bar X\mid D]=0,
\qquad
\operatorname{Var}(\bar X^*-\bar X)
=E[v_n/n]
=\frac{n-1}{n^2}\sigma^2.
$$

### A small illustration

*Assistant-added example.* Take $n=2$ and $X_i\sim\operatorname{Bernoulli}(1/2)$, so $\mu=1/2$ and $\sigma^2=1/4$. This uses the ties-allowed form of the resampling construction above.

| Original dataset | Probability | Conditional bootstrap mean | Conditional bootstrap variance |
| --- | --- | --- | --- |
| $(0,0)$ | $1/4$ | $0$ | $0$ |
| $(0,1)$ or $(1,0)$ | $1/2$ | $1/2$ | $1/8$ |
| $(1,1)$ | $1/4$ | $1$ | $0$ |

The average within-dataset variance is $1/16$. The variance of the conditional centers is $1/8$. Their sum is $3/16$, matching $(2n-1)\sigma^2/n^2$.

At $n=1$, every bootstrap draw equals the single observed value: conditional variance is zero, while unconditional variance is still $\sigma^2$. No Gaussian assumption is needed for any of these identities; finite second moments suffice.

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Total variance|Total variance]] — My handwritten solution separates resampling variation within one dataset from movement of the sample mean across original datasets.
- [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional independence|Conditional independence]] — Bootstrap draws are independent given the data, but sharing a random dataset creates unconditional covariance $\sigma^2/n$.

## Origin

This note consolidates my exercise-5 discussion in [[raw/conversations/2026-10-18-Estimating-Interval-Probability.pdf|the archived conversation]], pp. 6–10, together with the original exercise screenshot and supplemental handwritten solution. The page-8 question is paraphrased to retain its mathematical issue. The earlier interval-probability exercise on pp. 1–5 is outside this note. The [[raw/conversations/2026-10-18-Estimating-Interval-Probability-manifest.json|original capture manifest]] records the full source bundle; images 1–2 belong to that earlier exercise.

The total-variance calculation and final coefficient are in my handwriting. The resampling explanation, explicit assumptions, and covariance proof include earlier assistant explanations. The centered-error identity and binary illustration are added synthesis for this consolidation. The two original images are preserved unchanged; cropped peripheral handwriting is not reconstructed.
