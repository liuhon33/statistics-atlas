---
id: learning-likelihood-aic-bic-introduction
title: Likelihood and information criteria - AIC and BIC
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Validation & model selection]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Validation & model selection
study_band: U–M
note_types:
  - topic-note
  - derivation
source_format: conversation
created: 2026-11-11
updated: 2026-11-12
status: active
verification: checked
aliases:
  - AIC and BIC introduction
tags:
  - atlas/learning
  - subject/computing
  - topic/model-selection
---

# Likelihood and information criteria - AIC and BIC

Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Validation & model selection

**Likelihood asks how well a parameter setting explains the observed data. AIC and BIC ask whether a model's better fit is worth its extra adjustable parameters.**

## Part 1 — See it and use it

### 1. Likelihood starts with a fixed observation

Imagine tossing a coin independently three times and observing the ordered sequence **H, H, T**. Let $p$ be the coin's unknown probability of heads. The probability of this particular sequence, for a proposed $p$, is

$$
L(p)=p\times p\times(1-p)=p^2(1-p).
$$

| Proposed $p$ | Likelihood of H, H, T |
| --- | ---: |
| $0.5$ | $0.125$ |
| $2/3$ | $4/27\approx0.148$ |
| $0.9$ | $0.081$ |

The data stay fixed; **we vary $p$**. The maximum occurs at $\hat p=2/3$: the **maximum likelihood estimate (MLE)**. This does **not** say there is a 14.8% probability that $p=2/3$.

More generally, a **likelihood function** is $L(\theta)=f_\theta(x)$, viewed as a function of the unknown parameter(s) $\theta$ with the observed data $x$ fixed. For continuous data, $f$ is a density, not the probability of one exact observation. The **log-likelihood** is $\ell(\theta)=\ln L(\theta)$; logarithms turn products into sums and preserve which value is largest. [Geyer, *Likelihood Inference*, §§3–4](https://www.stat.umn.edu/geyer/5421/notes/likelihood.html).

### 2. Fitting a parameter is not yet choosing a model

Now observe **100 independent flips: 60 heads and 40 tails**. Compare two models for the same ordered data:

- **Fair coin:** $p=0.5$ fixed in advance. Nothing is fitted: $k=0$ free parameters.
- **Free coin:** $p$ is estimated from the data; its fitted value is $0.6$. One adjustable parameter: $k=1$.

The free model includes the fair model as an option, so its maximized likelihood cannot be worse. But some improvement can come from fitting random noise. **Information criteria add a complexity cost to the fitted-data score.**

![[assets/figures/2026-11-11-aic-bic/01-coin-fit-and-selection.svg]]

*Left: which $p$ fits these flips best? Right: after charging for the fitted parameter, AIC favors free $p$, while BIC favors the fixed fair coin. Relative likelihood is scaled to peak at 1; it is not a probability distribution over $p$.*

### 3. The two definitions

Write $\hat\ell=\ell(\hat\theta)$ for the **maximized total log-likelihood**, $k$ for the number of freely fitted parameters, and $n$ for the sample size. Use natural logarithms.

$$
\boxed{\mathrm{AIC}=-2\hat\ell+2k}
\qquad
\boxed{\mathrm{BIC}=-2\hat\ell+k\ln n}.
$$

**AIC** means *Akaike information criterion*; **BIC** means *Bayesian information criterion*. In this convention, **smaller is better**. The first term rewards fit; the second charges for flexibility. [MathWorks, *Information Criteria for Model Selection*, definitions](https://www.mathworks.com/help/econ/information-criteria.html).

For our 100 flips:

$$
\hat\ell_{\rm fair}=100\ln(0.5)=-69.315,
\qquad
\hat\ell_{\rm free}=60\ln(0.6)+40\ln(0.4)=-67.301.
$$

| Model | $k$ | $-2\hat\ell$ | AIC | BIC |
| --- | ---: | ---: | ---: | ---: |
| Fair coin | 0 | 138.629 | 138.629 | **138.629** |
| Free coin | 1 | 134.602 | **136.602** | 139.208 |

The free model improves $-2\hat\ell$ by **4.027**. That pays AIC's cost of **2**, but not BIC's cost of $\ln100\approx\mathbf{4.605}$. Different winners are not an arithmetic error.

As a second scenario, **80 heads in the same 100-flip experiment** gives an improvement of about **38.55**: both criteria then favor free $p$. A complexity penalty does not mean “always choose the simpler model.” These are invented teaching examples, not evidence about a real coin.

### 4. How to use them

1. **Specify plausible candidates.** For example, a straight line versus a quadratic curve for the same response.
2. **Fit each by maximum likelihood to exactly the same observations.** Obtain its total log-likelihood, parameter count and sample size.
3. **Compute one criterion for every candidate and rank it.** Compare AIC with AIC, or BIC with BIC—not one model's AIC with another's BIC.
4. **Interpret the ranking, not an absolute cutoff.** There is no universal “AIC below 10 is good” rule. Negative values are possible. The winner is preferred *among these candidates*, not certified true or adequate.

Keep the response scale and likelihood normalization consistent; do not compare a model for $y$ with a model for $\log y$ naively, or models fitted after different missing-row exclusions. Model-dependent omitted constants can change the ranking. [R documentation, `AIC`, “Details”](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/AIC.html).

**Counting parameters: a tiny regression example.** With independent Gaussian errors of unknown variance, a straight line $y=a+bx+\varepsilon$ has $k=3$: $a,b,\sigma^2$. A quadratic $y=a+bx+cx^2+\varepsilon$ has $k=4$. Count the estimated noise variance, not just the slopes; known fixed quantities cost no fitted parameter.

**Which criterion?** AIC targets predictive fit through an approximate correction for using the training data to fit and evaluate. BIC arises from a large-sample approximation to model evidence. For $n\ge8$, BIC charges more per parameter, often preferring simpler models. Neither is universally superior. [Balakrishnan, *36-705 Lecture 34*, §34.1, pp. 2–3](https://www.stat.cmu.edu/~siva/teaching/705/lec34.pdf).

These standard penalties assume regular, finite-dimensional fitting conditions. Tiny samples, boundary estimates or highly flexible models need additional care; AICc is a small-sample correction in applicable settings. AIC/BIC do not replace checking the model's assumptions or predictions. [MathWorks, AICc definition](https://www.mathworks.com/help/econ/information-criteria.html).

**Stop here on a first reading.** You can already read a fitted-model comparison table and explain why extra fit may not win.

## Part 2 — Optional derivations

### 5. Why the fitted coin probability is the fraction of heads

For $h$ heads in $n$ independent ordered flips, with $0<h<n$,

$$
\ell(p)=h\ln p+(n-h)\ln(1-p),
$$
$$
\ell'(p)=\frac hp-\frac{n-h}{1-p}=0
\iff h(1-p)=p(n-h)
\iff \hat p=\frac hn.
$$

Since $\ell''(p)=-h/p^2-(n-h)/(1-p)^2<0$, this is the unique maximum. All heads or all tails instead puts the estimate at a boundary, outside this interior argument.

If we record only the count of heads, a binomial likelihood includes $\binom nh$. For these two coin models that factor is identical, so it shifts both scores equally and leaves their **differences** unchanged. The table above consistently uses the ordered-sequence likelihood.

### 6. Exactly how much improvement pays for another parameter?

Let $\Delta\ell=\hat\ell_{\rm larger}-\hat\ell_{\rm smaller}$ and $\Delta k=k_{\rm larger}-k_{\rm smaller}>0$. Subtract the scores:

$$
\Delta\mathrm{AIC}=-2\Delta\ell+2\Delta k,
\qquad
\Delta\mathrm{BIC}=-2\Delta\ell+\Delta k\ln n.
$$

The larger model wins precisely when

$$
\mathrm{AIC}:\quad 2\Delta\ell>2\Delta k,
\qquad
\mathrm{BIC}:\quad 2\Delta\ell>\Delta k\ln n.
$$

This is exact algebra once the criteria are defined—not yet a proof that either criterion selects the best model.

### 7. Why AIC needs a correction: an exact one-parameter proof

![[assets/figures/2026-11-11-aic-bic/02-why-penalties-arise.svg]]

*Left: training error is optimistic after fitting a mean. Right: the parameter region fitting the data well narrows as $n$ increases. These illustrate different origins of the two penalties; they are not the same argument.*

Take $X_1,\ldots,X_n$ independent $N(\mu,1)$ measurements, with **known variance 1**. Only the mean is fitted, so $k=1$ and $\hat\mu=\bar X$. The fitted training score is

> [!note]- From the MLE to the fitted training score
> **The MLE is a parameter value. The fitted score is a number calculated using that parameter value.** The bridge is: write the log-likelihood, find its maximizing mean, then evaluate it at that mean.
>
> **1. Write the likelihood before fitting anything.** Let $m$ denote a *candidate* mean, with the variance still fixed at $1$. Its density for observation $X_i$ is
>
> $$
> f_m(X_i)=\frac{1}{\sqrt{2\pi}}\exp\left[-\frac{(X_i-m)^2}{2}\right].
> $$
>
> Independence means we multiply these densities:
>
> $$
> L(m)=\prod_{i=1}^n f_m(X_i)
> =(2\pi)^{-n/2}\exp\left[-\frac12\sum_{i=1}^n(X_i-m)^2\right].
> $$
>
> Taking the natural logarithm gives
>
> $$
> \ell(m)=-\frac n2\ln(2\pi)-\frac12\sum_{i=1}^n(X_i-m)^2.
> $$
>
> This is the log-likelihood for **any proposed mean $m$**, not yet the fitted one. The observed data stay fixed while $m$ varies.
>
> **2. Find the MLE: which mean makes this largest?** The term $-\frac n2\ln(2\pi)$ does not depend on $m$, so
>
> $$
> \underbrace{\arg\max_m\ell(m)}_{\text{maximum likelihood}}
> =\underbrace{\arg\min_m\sum_i(X_i-m)^2}_{\text{least squared error}}.
> $$
>
> Differentiate, including the minus sign from differentiating $X_i-m$:
>
> $$
> \begin{aligned}
> \ell'(m)
> &=-\frac12\sum_i 2(X_i-m)(-1)\\
> &=\sum_i(X_i-m)\\
> &=n(\bar X-m).
> \end{aligned}
> $$
>
> Setting this equal to zero gives $\hat\mu=\bar X$. Since $\ell''(m)=-n<0$, this is the unique maximum.
>
> **3. Substitute the MLE back into the log-likelihood.** These are two different objects:
>
> $$
> \underbrace{\hat\mu=\arg\max_m\ell(m)}_{\text{location of the maximum}},
> \qquad
> \underbrace{\hat\ell=\ell(\hat\mu)=\max_m\ell(m)}_{\text{height of the maximum}}.
> $$
>
> Substituting $\hat\mu=\bar X$ gives
>
> $$
> \hat\ell=-\frac n2\ln(2\pi)-\frac12\sum_i(X_i-\bar X)^2.
> $$
>
> Finally, multiply by $-2$, cancelling both factors of $1/2$ and reversing both minus signs:
>
> $$
> \begin{aligned}
> -2\hat\ell
> &=-2\left[-\frac n2\ln(2\pi)-\frac12\sum_i(X_i-\bar X)^2\right]\\
> &=n\ln(2\pi)+\sum_i(X_i-\bar X)^2.
> \end{aligned}
> $$
>
> The appearance of $\bar X$, rather than an arbitrary $m$, is what makes this the **fitted** score.
>
> **4. Why a fitted training score?**
>
> - **Fitted:** the likelihood is evaluated at the estimated mean $\hat\mu=\bar X$.
> - **Training:** the same observations $X_i$ both determine $\bar X$ and assess its fit.
> - **Smaller is better:** maximizing $\ell$ is equivalent to minimizing $-2\ell$.
>
> Here the score is a constant plus the sum of squared residuals around the fitted mean. AIC then adds its complexity penalty:
>
> $$
> \mathrm{AIC}
> =\underbrace{n\ln(2\pi)+\sum_i(X_i-\bar X)^2}_{-2\hat\ell:\ \text{fitted training score}}
> +\underbrace{2}_{2k,\ k=1}.
> $$
>
> **Terminology:** “score” here is informal. The technical *score function* is $\ell'(m)$, a different object. The exact expression above assumes the variance is known and fixed at $1$; it does not fit an unknown variance.

$$
-2\hat\ell=n\ln(2\pi)+\sum_i(X_i-\bar X)^2.
$$

Using the identity

$$
\sum_i(X_i-\bar X)^2=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2
$$

and $\operatorname{Var}(\bar X)=1/n$ gives

$$
\mathbb E\!\left[\sum_i(X_i-\bar X)^2\right]=n-n\frac1n=n-1.
$$

Now take an independent fresh sample $Y_1,\ldots,Y_n$ from the same distribution, **without refitting** $\bar X$. Each fresh error has expectation zero and variance $1+1/n$:

$$
\mathbb E\!\left[\sum_i(Y_i-\bar X)^2\right]
=n\left(1+\frac1n\right)=n+1.
$$

The fresh-sample score exceeds the training score by **2 in expectation**. Thus adding $2k=2$ exactly corrects the average optimism in this particular model. It does not predict every fresh sample's error exactly.

For regular, correctly specified models, a large-sample expansion gives the familiar $2k$ correction; this one-mean calculation explains it but does **not** prove the general theorem or cover estimated variance. The general result is asymptotic, not a penalty valid for arbitrary model fitting. See [Lecture 34, §34.1](https://www.stat.cmu.edu/~siva/teaching/705/lec34.pdf); that lecture uses the sign-reversed, **maximize** convention.

### 8. Why BIC contains $\ln n$: a large-sample derivation sketch

Define the model's **evidence** as its likelihood averaged over a proper prior density $\pi(\theta)$:

$$
p(x\mid M)=\int e^{\ell(\theta)}\pi(\theta)\,d\theta.
$$

For a smooth, identifiable model with fixed $k$, an interior maximum, nonsingular curvature and a fixed prior positive and continuous near the limiting parameter, the likelihood becomes approximately Gaussian near its peak. Its width in each parameter direction scales as $n^{-1/2}$. Hence its $k$-dimensional volume scales as $n^{-k/2}$:

$$
p(x\mid M)\approx e^{\hat\ell}\,n^{-k/2}C_M,
$$

where $C_M$ collects prior and curvature factors of order one. Taking $-2\ln$ gives

$$
-2\ln p(x\mid M)\approx-2\hat\ell+k\ln n-2\ln C_M.
$$

BIC retains the first two terms and drops the order-one terms. This is a **Laplace approximation**, not an exact finite-sample identity or a posterior model probability. The right-hand plot shows the width/area scaling for one normal mean. [Ghahramani, *Bayesian Machine Learning Overview*, PDF pp. 25–26, “Laplace Approximation” and “Bayesian Information Criterion”](https://www.stat.cmu.edu/~larry/=sml2008/lect1.pdf).

## Origin

> [!info]- Source details
> Requested as a beginner starter before studying the topic. No document, handwriting or worked solution was supplied. Explanations, coin examples, normal-mean demonstration and figures are agent-added teaching material, not attributed to the user.
>
> The vault already contains Likelihood function and Validation & model selection, but the title/alias/body search found no dedicated AIC/BIC backbone page or matching learning note. This note uses the latter as its single home; no taxonomy changes or extra conceptual map links were made. Deeper connections are deliberately deferred.
>
> Read sources: Geyer §§3–4; MathWorks definitions and AICc paragraph; R `AIC` description/details; Balakrishnan §34.1; Ghahramani PDF pp. 25–26. Inline citations indicate their scope. No claim of reading the original Akaike or Schwarz papers.
>
> Reproduction: [[assets/figures/2026-11-11-aic-bic/draw_and_check.py]] and [[assets/figures/2026-11-11-aic-bic/checks.json]]. Coin arithmetic and rankings, normal expectation identities and Gaussian-area calculations checked; simulation and quadrature support, rather than prove, the derivations. Static previews inspected; live Obsidian rendering not verified.
>
> Extension (2026-11-12): at the user's request, the current conversation's agent-authored explanation connecting the normal-mean MLE to the fitted training score is saved in a collapsed callout immediately above that score in §7. The density, log-likelihood, derivative, maximum and substitution are shown explicitly, with the known-variance assumption and the informal-versus-technical meaning of “score” distinguished. No new supplied originals or external sources.
