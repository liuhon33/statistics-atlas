---
id: learning-bootstrap-size-repetitions-clt
title: Bootstrap means - resample size, repetitions, and the CLT
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Nonparametric & robust inference/Resampling inference/Bootstrap & jackknife/Nonparametric bootstrap]]"
subject: statistics
backbone_path: Statistical inference & modeling → Nonparametric & robust inference → Resampling inference → Bootstrap & jackknife → Nonparametric bootstrap
study_band: U–M
note_types: [conversation-digest, question, derivation, insight]
question_roles: [concept-distinction, cross-topic-connection, assumption-boundary]
source_format: conversation
created: 2026-11-12
updated: 2026-11-12
status: active
verification: checked
learning_state: introduced
aliases:
  - Bootstrap resample size versus repetitions
  - Conditional CLT for bootstrap means
tags: [atlas/learning, subject/statistics, topic/bootstrap, topic/asymptotics]
connections:
  - "[[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness]]"
  - "[[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT]]"
  - "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Random generation & Monte Carlo/Monte Carlo standard error]]"
sources:
  - "[[raw/conversations/2026-11-09-Bootstrap-Comparison-Diagram-read-thread.json]]"
---

# Bootstrap means - resample size, repetitions, and the CLT

Statistical inference & modeling → Nonparametric & robust inference → Resampling inference → Bootstrap & jackknife → Nonparametric bootstrap

**The number of draws in each resample controls averaging. The number of repetitions controls how accurately we see the resulting distribution.** For means, larger resamples allow a conditional CLT; more repetitions alone do not make the distribution normal. Ordinary bootstrap inference matches the resample size to the original sample size.

## 1. Which number changes the bootstrap distribution?

*My question, paraphrased: Does taking many bootstrap repetitions make the result normal, or is the number of observations averaged in each repetition what matters?*

Keep three numbers separate:

| Symbol | Meaning | Role |
| --- | --- | --- |
| $n$ | Number of original observations | Defines the empirical distribution and the original estimator's sample size |
| $m$ | Number of draws within one resample | Determines how much each bootstrap mean averages |
| $B$ | Number of independent repetitions | Determines Monte Carlo accuracy when estimating that bootstrap distribution |

Fix a dataset $D=(x_1,\ldots,x_n)$ of finite real values, with $n\geq2$. Define

$$
\bar x=\frac1n\sum_{i=1}^n x_i,
\qquad
v_n=\frac1n\sum_{i=1}^n(x_i-\bar x)^2.
$$

Here $v_n$ is the **empirical variance with denominator $n$**. If $s^2$ uses denominator $n-1$, then $v_n=(n-1)s^2/n$.

In repetition $b$, draw indices $J_{b1},\ldots,J_{bm}$ independently and uniformly from $\{1,\ldots,n\}$, with replacement, and set $X_{bj}^*=x_{J_{bj}}$. All repetitions are independent conditional on $D$. One repetition produces one statistic:

$$
(X_{b1}^*,\ldots,X_{bm}^*)
\quad\longrightarrow\quad
\bar X_m^{*(b)}=\frac1m\sum_{j=1}^m X_{bj}^*.
$$

After $B$ repetitions there are $B$ bootstrap means, possibly with ties. Keep their spread to estimate uncertainty; averaging them into one number discards that distribution. The same resample-and-recompute principle applies to a median or another chosen statistic. The ordinary nonparametric procedure uses $m=n$; see [the CMU bootstrap chapter, §§11.2–11.3, pp. 210–211](https://www.stat.cmu.edu/~larry/=sml/Boot.pdf#page=2).

Each **index** has probability $1/n$. Repeated observed values combine their masses: in $(1,2,2,3,4,4,4,5,7,8)$, a draw equals 4 with probability $3/10$.

Write $E_*$, $\operatorname{Var}_*$ and $P_*$ for calculations conditional on $D$. Then

$$
E_*[X_{bj}^*]=\bar x,
\qquad
\operatorname{Var}_*(X_{bj}^*)=v_n,
$$

and conditional independence gives the exact identities

$$
\boxed{
E_*[\bar X_m^{*(b)}]=\bar x,\qquad
\operatorname{Var}_*(\bar X_m^{*(b)})=\frac{v_n}{m}.
}
$$

There is no $B$ in these formulas.

### One draw, an average, or a copy

For the ten-value dataset above, $\bar x=4$ and $v_n=4.4$:

| Procedure in each repetition | Resulting distribution | Exact conditional SD |
| --- | --- | --- |
| Copy all ten observations and average | Always 4 | $0$ |
| Draw one observation, $m=1$ | The empirical distribution itself | $\sqrt{4.4}\approx2.098$ |
| Draw ten observations and average, $m=10$ | Distribution of means of ten iid empirical draws | $\sqrt{4.4/10}\approx0.663$ |

With $m=1$, the “mean” is just the selected observation. Drawing more such observations reveals the empirical distribution more accurately.

![[assets/figures/bootstrap-size-repetitions/bootstrap-size-repetitions.png]]

*Original Codex illustration using the conversation's ten-value dataset. Columns change $m$; rows change $B$. The dark outlines are exact bin probabilities calculated by convolution; colored bars are simulated proportions. Both axes and bin widths are shared. Increasing $B$ leaves each column's exact law unchanged. This is a new illustration, not the unavailable original chat image.*

### Why more repetitions only improve the approximation

For a fixed threshold $t$, let $G_m(t)=P_*(\bar X_m^*\leq t)$. Estimate it by the fraction of repetitions below $t$:

$$
\widehat G_{m,B}(t)
=\frac1B\sum_{b=1}^B
\mathbf1\{\bar X_m^{*(b)}\leq t\}.
$$

The indicators are iid Bernoulli variables with success probability $G_m(t)$, so

$$
E_*[\widehat G_{m,B}(t)]=G_m(t),
\qquad
\operatorname{Var}_*(\widehat G_{m,B}(t))
=\frac{G_m(t)[1-G_m(t)]}{B}
\leq\frac1{4B}.
$$

Thus $\widehat G_{m,B}(t)\to G_m(t)$ in probability as $B\to\infty$: the Monte Carlo error vanishes, while the target law $G_m$ stays fixed. The same argument applies to a fixed histogram bin. A CLT across repetitions can describe the error in this estimated fraction; it does not make the individual bootstrap means normal.

## 2. Can the CLT make bootstrap means approximately normal?

*My question, paraphrased: If each resample is large enough, can the central limit theorem prove that the resulting means become normally distributed?*

**Yes, conditional on a fixed dataset with $v_n>0$, as the number of draws $m$ tends to infinity.**

The [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT|classical iid CLT]] applies to independent, identically distributed variables with finite positive variance. Here the empirical distribution has finite support, so finiteness is automatic; positivity excludes an all-equal dataset. [Theorem: Pishro-Nik, §7.1.2](https://www.probabilitycourse.com/chapter7/7_1_2_central_limit_theorem.php).

For one repetition, suppress $b$ and standardize each draw:

$$
Y_j=\frac{X_j^*-\bar x}{\sqrt{v_n}},
\qquad
E_*[Y_j]=0,\qquad
\operatorname{Var}_*(Y_j)=1.
$$

Conditional iid sampling permits the direct substitution

$$
\frac1{\sqrt m}\sum_{j=1}^mY_j
=
\frac{\sqrt m(\bar X_m^*-\bar x)}{\sqrt{v_n}}
\xrightarrow[\ m\to\infty\ ]{d,\;P_*}N(0,1).
$$

Equivalently, for sufficiently large $m$,

$$
\bar X_m^*\ \approx\
N\!\left(\bar x,\frac{v_n}{m}\right),
$$

where the second normal parameter is the **variance**. This is approximate normality of the resample **mean**. The individual draws retain their empirical distribution.

The nondegenerate limit is for the **standardized** mean. Without scaling,

$$
P_*(|\bar X_m^*-\bar x|>\varepsilon)
\leq\frac{v_n}{m\varepsilon^2}\longrightarrow0
\qquad(\varepsilon>0),
$$

so the means concentrate at $\bar x$. If $v_n=0$, every bootstrap mean is already identical and the standardization is undefined. For a fixed finite dataset and finite $m$, the exact bootstrap law is discrete; “approximately normal” refers to a distributional approximation.

### A rare observation can delay the normal approximation

The conversation's counterexample fixes $n=100$ observations: 99 zeros and one 100. Then $\bar x=1$ and $v_n=99$. If $K$ counts how often 100 is selected,

$$
K\sim\operatorname{Binomial}(m,0.01),
\qquad
\bar X_m^*=\frac{100K}{m},
\qquad
P_*(\bar X_m^*=0)=0.99^m.
$$

| Draws per resample $m$ | Probability of a zero mean |
| --- | --- |
| $20$ | $81.79\%$ |
| $100$ | $36.60\%$ |
| $1{,}000$ | $0.004317\%$ |

With $m=20$, even a million repetitions will reveal a distribution with about 82% of its mass at zero. More repetitions expose that non-normal shape. There is no universal resample-size threshold that guarantees a good normal approximation across all datasets.

The mean's CLT also does not automatically cover other statistics such as medians or maxima; those require their own assumptions and limiting arguments.

## Match the resample size to the uncertainty being estimated

For iid original observations from a population with finite variance $\sigma^2$, the original mean has variance $\sigma^2/n$. The ordinary bootstrap substitutes $v_n$ for the unknown population variance and uses $m=n$, giving

$$
\widehat{\operatorname{SE}}_{\mathrm{boot}}(\bar X_n)
=\sqrt{\frac{v_n}{n}}
$$

for the ideal conditional bootstrap SD. Its simulated estimate is the SD across the $B$ bootstrap means. This is an approximation to the population standard error, with the finite-sample factor explained in [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness#4. Which variance does the bootstrap use?|the earlier bootstrap-moments note]].

Holding the observed data fixed, the ratio between the SD at another resample size and the ordinary-bootstrap SD is

$$
\frac{\sqrt{v_n/m}}{\sqrt{v_n/n}}=\sqrt{\frac nm}
\qquad(v_n>0).
$$

For $n=100$, using $m=20$ makes the raw spread $\sqrt5\approx2.236$ times as large; using $m=10{,}000$ makes it one tenth as large. Special methods using $m\ne n$ need their own calibration before their spread is used for the original estimator.

**A normal-looking bootstrap histogram is not a validity check.** Increasing $m$ changes the uncertainty scale, and increasing $B$ adds no new information about the population. The fixed-dataset CLT establishes a property of empirical draws; whether bootstrap inference approximates the original sampling distribution still depends on the data and statistic.

## Connections

- [[Learning/Statistical inference & modeling/Nonparametric & robust inference/Bootstrap mean - two layers of randomness|Bootstrap mean - two layers of randomness]] — Supplies the conditional-versus-unconditional distinction: the iid draws, variance $v_n/m$, and CLT here all hold with the original dataset fixed.
- [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT|Classical iid CLT]] — Applied to iid empirical draws, it gives the standardized-mean limit as $m$ grows and explains why unscaled means instead concentrate.
- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Random generation & Monte Carlo/Monte Carlo standard error|Monte Carlo standard error]] — Increasing $B$ reduces the error in estimated probabilities at order $B^{-1/2}$ while leaving the bootstrap law being estimated unchanged.

## Origin

> [!info]- Source details
> Source: [Bootstrap Comparison Diagram](chatgpt-conversation://6af212be-6d04-83e9-9016-dffd6e21a4f1), 2026-11-09; [[raw/conversations/2026-11-09-Bootstrap-Comparison-Diagram-read-thread.json|retrieved text snapshot]], captured 2026-11-12. The two retained questions consolidate my resampling/normality distinction and CLT conjecture (user messages 575c77e0-4943-4958-978f-9239e8335c65, dc87f6f7-0b45-40e3-9fb6-0dae27721f75, and 5e170f8e-5230-406d-b610-40d5027869e0). The routine confirmation and repeated spoken phrasing are integrated into the explanation.
>
> The ten-value example, rare-value counterexample, and conditional CLT were supplied by the source assistant. The index construction fixes its ambiguous probability notation when values repeat. The explicit Monte Carlo-error argument, exact SD comparison, and new plot are Codex additions; the source's reported SDs from 100 simulations are not treated as exact quantities or reproduced without its simulation state.
>
> The original comparison PNG is linked in source message 80005375-4e60-56c8-8548-613372080c8a but was not retrievable from the returned chat attachment data. Its image content remains unreviewed. The rare-value chart's embedded data were available in the text and checked. No handwriting or exercise screenshot was supplied.
>
> Verification: conditional moment algebra, iid CLT assumptions and substitution, Chebyshev bounds, binomial probabilities, and uncertainty ratios were checked. [[assets/figures/bootstrap-size-repetitions/generate.py|Reproducible figure code]] and [[assets/figures/bootstrap-size-repetitions/checks.json|numeric checks]] verify the exact convolution laws and plotted quantities. The source-image gap is tracked in [[_system/Review Queue]].
