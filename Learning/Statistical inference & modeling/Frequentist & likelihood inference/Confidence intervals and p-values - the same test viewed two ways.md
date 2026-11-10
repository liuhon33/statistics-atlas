---
id: learning-ci-pvalue-test-duality
title: Confidence intervals and p-values - the same test viewed two ways
layer: learning
primary_home: "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Intervals & test inversion/Inverting a test]]"
subject: statistics
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Intervals & test inversion → Inverting a test
study_band: U–M
note_types: [question, derivation, insight]
question_roles: [concept-distinction, cross-topic-connection, assumption-boundary]
source_format: handwriting-and-legacy-learning-notes
created: 2026-11-10
updated: 2026-11-10
status: active
verification: checked
learning_state: unknown
aliases: [CI and p value relationship, Confidence intervals as inverted tests]
tags: [atlas/learning, subject/statistics, topic/confidence-intervals, topic/hypothesis-testing]
connections:
  - "[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation]]"
sources:
  - "[[raw/notes/2026-11-01-Regression-CI-p-values-and-F-statistics-four-page-original.pdf]]"
  - "[[raw/notes/2026-11-10-ci-pvalue-legacy/question.md.txt]]"
  - "[[raw/notes/2026-11-10-ci-pvalue-legacy/derivation.md.txt]]"
  - "[[raw/notes/2026-11-10-ci-pvalue-legacy/synthesis.md.txt]]"
  - "[[raw/notes/2026-11-10-ci-pvalue-legacy/source-record.md.txt]]"
  - "[[raw/notes/2026-11-10-ci-pvalue-legacy/original-manifest.json]]"
  - "[[assets/figures/2026-11-10-ci-pvalue/draw_ci_pvalue.py]]"
  - "[[assets/figures/2026-11-10-ci-pvalue/render_handwriting.py]]"
  - "[[assets/figures/2026-11-10-ci-pvalue/checks.json]]"
  - "[[assets/figures/ci-unequal-slices/draw_unequal_slices.py]]"
  - "[[assets/figures/ci-unequal-slices/checks.json]]"
---

# Confidence intervals and p-values - the same test viewed two ways

Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Intervals & test inversion → Inverting a test

**A test asks whether to reject one candidate parameter value; a confidence interval collects all the candidates that the matching tests do not reject.** A p-value tells us how the decision for one candidate changes as we vary the significance threshold.

**Another intuition:** a $100(1-\alpha)\%$ confidence interval is the set of candidate null values that our observed data do not reject under the matching level-$\alpha$ tests.

**My handwritten question pair, paraphrased from p. 2:** Are the observed data too far from the model constrained to a candidate slope $b$? Conversely, which values of $b$ give a model close enough to the data?

The useful distinction is what stays fixed:

| View | Hold fixed | Vary or inspect |
|---|---|---|
| Design/calibrate a test | A candidate null and the sampling model | Possible datasets and the resulting rejection probability |
| Compute a p-value | Observed data and a candidate null | How extreme the observed statistic is under that null; equivalently, the significance threshold at which it is rejected |
| Construct a confidence set | Observed data, significance level and testing method | The candidate null value |

## 1. The decision rule becomes a family indexed by the null value

In the [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget#1. What is being optimized?|decision-rule note]], we choose a function that rejects some datasets and retains others. To construct a confidence set, we need a **calibrated test for each candidate value**, not just one rule optimized for one specified null/alternative pair.

For clarity, start with nonrandomized tests. Let $X$ be the random dataset, $x$ its observed value, $b$ a candidate for a scalar parameter $\theta$, and

$$
\phi_\alpha(x;b)=
\begin{cases}
1,&\text{reject }H_0:\theta=b,\\
0,&\text{do not reject }H_0:\theta=b.
\end{cases}
$$

Every candidate's test must satisfy $P_b\{\phi_\alpha(X;b)=1\}\le\alpha$. If there are nuisance parameters, this bound must hold for every nuisance value allowed by that null.

After observing $x$, define

$$
\boxed{C_{1-\alpha}(x)=\{b:\phi_\alpha(x;b)=0\}.}
$$

This is a confidence **set**; in the usual scalar normal/t examples it is an interval. Other test families can produce disconnected or unbounded sets.

![[assets/figures/2026-11-10-ci-pvalue/01-test-inversion-band.svg]]
*New Codex illustration: the same non-rejection band is sliced vertically for a test and horizontally for an interval. Here the sample mean has known standard error 0.1 and the observed mean is 0.2. The band is not a probability distribution over candidate means.*

### Equal decisions do not require equal slice lengths

**The horizontal and vertical slices have equal lengths in the normal diagram above, but not in every two-tailed test.** If a band has the form $L\le x-b\le U$ with fixed $L,U$, its vertical slice is $[b+L,b+U]$ and its horizontal slice is $[x-U,x-L]$: both have length $U-L$. Even asymmetric additive noise can have this property; the asymmetric exponential illustration discussed in chat was therefore not a counterexample to equal lengths.

For an actual counterexample, take one observation from the constructed model

$$
X\sim\operatorname{Uniform}(\theta/2,3\theta/2),\qquad\theta>0.
$$

Here $E_\theta[X]=\theta$, but $\operatorname{SD}_\theta(X)=\theta/\sqrt{12}$: **larger candidate parameters imply wider sampling distributions.** Under $H_0:\theta=b$, the support has width $b$. Removing 2.5% from each tail gives the 95% non-rejection band

$$
\boxed{0.525b\le x\le1.475b.}
$$

![[assets/figures/ci-unequal-slices/unequal-horizontal-vertical-slices.svg]]
*Original Codex example: a widening band with equal axis scales. Blue fixes the null $b=1$; orange fixes the data $x=1$. The right panel puts both lengths on a common ruler. Both segments are fully visible; the difference is not clipping or axis stretching.*

Read the same inequality in the two directions:

| Slice through $(b,x)=(1,1)$ | Interval | Length |
|---|---|---|
| Vertical: fix $b=1$, vary possible data | $x\in[0.525,1.475]$ | $0.950$ |
| Horizontal: fix $x=1$, vary candidate nulls | $b\in[1/1.475,1/0.525]\approx[0.678,1.905]$ | $1.227$ |

The horizontal slice is about **29% longer**. Its endpoints come from dividing by the two boundary slopes, not from copying the vertical slice's endpoints. The exact inverted interval is

$$
C_{0.95}(x)=\left[\frac{x}{1.475},\frac{x}{0.525}\right],\qquad x>0.
$$

It has exactly 95% coverage because $X/\theta\sim\operatorname{Uniform}(0.5,1.5)$ and

$$
P_\theta\{\theta\in C_{0.95}(X)\}
=P_\theta\{0.525\le X/\theta\le1.475\}=0.95.
$$

**The test and CI still agree on every candidate.** Writing $F_b$ for the null CDF, the matching equal-tailed p-value is $p_b(x)=2\min\{F_b(x),1-F_b(x)\}$. Thus

$$
x\in[0.525b,1.475b]
\iff b\in C_{0.95}(x)
\iff p_b(x)\ge0.05.
$$

For example, at $x=1.49$, testing $b=1$ gives $p=0.02$, and the CI is approximately $[1.010,2.838]$, excluding 1. Zero is not an admissible null in this positive-parameter model; the same inversion principle applies to zero in models where it is admissible. **Agreement concerns membership of the same point in the band, not equality of slice lengths.**

The distinction is:

| Property                                    | Always?                                                |
| ------------------------------------------- | ------------------------------------------------------ |
| Equal horizontal and vertical slice lengths | **No**, but yes for both illustrated bands             |
| CI excludes 0 ⇔ matching test rejects 0     | **Yes**, for a CI constructed by inverting those tests |

## 2. A p-value is a threshold, not a probability that the null is true

For a fixed candidate $b$, suppose the rejection regions expand as $\alpha$ increases. Then

$$
p_b(x)=\inf\{\alpha:\phi_\alpha(x;b)=1\}.
$$

The infimum matters: the boundary need not itself be a rejection. In the continuous examples below, we use the explicit convention **reject when $p_b(x)<\alpha$**, so

$$
\boxed{C_{1-\alpha}(x)=\{b:p_b(x)\ge\alpha\}.}
$$

For a two-sided normal-mean test with known $\sigma$, put $\tau=\sigma/\sqrt n$. Under $H_0:\mu=b$, the hypothetical statistic $(\bar X-b)/\tau$ is standard normal. Thus

$$
z_{\mathrm{obs}}(b)=\frac{\bar x-b}{\tau},\qquad
p_b(x)=P_b\!\left\{\left|\frac{\bar X-b}{\tau}\right|\ge |z_{\mathrm{obs}}(b)|\right\}
=2\{1-\Phi(|z_{\mathrm{obs}}(b)|)\}.
$$

The probability ranges over **hypothetical datasets under the specified null**. It is not $P(\mu=b\mid x)$, not a probability that the observed data occurred “by chance,” and not the power of the test under an alternative.

![[assets/figures/2026-11-10-ci-pvalue/02-pvalue-and-interval.svg]]
*New illustration at $b=0$: the two shaded null tails sum to $p=0.04550$. On the right, the 95% interval is the set where the whole p-value curve lies at or above 0.05. The curve is not a posterior density and need not integrate to one.*

![[assets/figures/2026-11-10-ci-pvalue/03-sweep-null-values.gif]]
*The candidate null mean moves; the observed data and the resulting interval do not. For each candidate we use its own hypothetical sampling distribution. This is not a simulation in which the true parameter changes, and it is not a repeated-sampling coverage animation.*

With $\bar x=0.2$ and $\tau=0.1$,

$$
C_{0.95}(x)=[\,0.2-1.959964(0.1),\;0.2+1.959964(0.1)\,]
=[0.004004,\;0.395996].
$$

The null value 0 is outside, exactly matching $p_0(x)=0.045500<0.05$. This uses the same numerical data example as the newer decision-rule note, not a new user-supplied experiment.

## 3. My regression notes give the same equivalence with t

![[assets/figures/2026-11-10-ci-pvalue/handwriting-page-3.png|750]]
*Unretouched full-page rendering of the old PDF's p. 3: my p-value expression, interval algebra, zero-exclusion sketches and repeated-sampling interpretation. The original's 1.96 shorthand, informal null-probability wording and single-predictor claim need the qualifications below; they have not been erased from the source.*

Assume a fixed full-rank design $X\in\mathbb R^{n\times k}$, $n>k$, and

$$
Y=X\beta+\varepsilon,\qquad \varepsilon\sim N_n(0,\sigma^2 I_n),\quad \sigma>0.
$$

For a prespecified coefficient $j$, let $\nu=n-k$ and $\widehat{\mathrm{SE}}_j=s\sqrt{[(X^\top X)^{-1}]_{jj}}$, where $s^2=\mathrm{SSE}_F/\nu$. Assume the observed $s>0$. Then, under $H_0:\beta_j=b$,

$$
T(b)=\frac{\hat\beta_j-b}{\widehat{\mathrm{SE}}_j}\sim t_\nu,\qquad
p_b(y)=2\{1-F_{t_\nu}(|t_{\mathrm{obs}}(b)|)\}.
$$

Writing $t_*=t_{\nu,1-\alpha/2}$, the same inequality can be read three ways:

$$
\begin{aligned}
p_b(y)\ge\alpha
&\iff |t_{\mathrm{obs}}(b)|\le t_*\\
&\iff |\hat\beta_j-b|\le t_*\widehat{\mathrm{SE}}_j\\
&\iff b\in[\hat\beta_j-t_*\widehat{\mathrm{SE}}_j,\;\hat\beta_j+t_*\widehat{\mathrm{SE}}_j].
\end{aligned}
$$

For the matching two-sided 5% test of $\beta_j=0$:

| Exact result | Zero relative to the closed 95% t interval | Decision with $p<0.05$ |
|---|---|---|
| $p<0.05$ | Outside | Reject |
| $p>0.05$ | Strictly inside | Do not reject |
| $p=0.05$ | At an endpoint | Do not reject under this convention |

**Rounded $p=0.050$ is not evidence of exact equality.** Use the unrounded value and the same endpoint convention in both procedures. Choosing $p\le\alpha$ instead changes the retained endpoints; continuity makes this a probability-zero distinction under the model, but not an algebraically interchangeable inequality.

The t formula applies to one coefficient even in multiple regression. Its exact critical value is $t_*$, not generally 1.96; 1.96 is the standard-normal 97.5th percentile. These coefficient formulas and their model dependence are corroborated by [Stanford Stats 203, Inference for Coefficients](https://web.stanford.edu/class/stats203/lectures/lecture4/).

## 4. The original constrained-fit picture explains why

![[assets/figures/2026-11-10-ci-pvalue/handwriting-page-2.png|750]]
*Unretouched p. 2: the blue question pair distinguishes testing one slope from finding all acceptable slopes, followed by two calculations of the added squared distance. The full four-page original remains preserved, including the preceding projection sketch and p. 4's short continuation.*

In simple regression with an intercept, center the predictor as $x_c=x-\bar x\mathbf1$ and set $S_{xx}=\|x_c\|^2>0$. The full fitted point and the fit constrained to slope $b$, **with its intercept refitted**, are

$$
C=\bar y\mathbf1+\hat\beta_1x_c,\qquad D_b=\bar y\mathbf1+b x_c.
$$

My two routes—calculate $\|C-D_b\|^2$ directly, or subtract the residual sums of squares—give

$$
\mathrm{SSE}_R(b)-\mathrm{SSE}_F=\|C-D_b\|^2
=(\hat\beta_1-b)^2S_{xx}.
$$

Hence $F(b)=(\hat\beta_1-b)^2S_{xx}/s^2=t(b)^2$, with $s^2=\mathrm{SSE}_F/(n-2)$. Collecting the slopes whose extra fit cost stays below the F cutoff gives precisely the same interval. The [[Learning/Statistical inference & modeling/Regression & linear models/Why one restriction gives F equals t squared#3. Combine the two pieces to obtain F = t squared|one-restriction derivation]] supplies the full algebra and the multiple-regression generalization; it is not repeated here.

For the original three-observation drawing, residual df is 1, so the 95% multiplier is $12.706$, not $1.96$; the F cutoff is its **square**, about $161.448$. The square root already present in my handwritten interval is correct.

## 5. Why test error control becomes interval coverage

At the true fixed parameter $\theta$, the event that the set misses the truth is exactly the event that its matching test rejects the true null:

$$
\{\theta\notin C_{1-\alpha}(X)\}
=\{\phi_\alpha(X;\theta)=1\}.
$$

Therefore

$$
\boxed{P_\theta\{\theta\in C_{1-\alpha}(X)\}
=1-P_\theta\{\phi_\alpha(X;\theta)=1\}\ge1-\alpha.}
$$

Exact-size tests give equality; conservative tests can give greater coverage. No simultaneous-testing correction is needed merely because we invert all candidates: coverage concerns failure to retain the **one true parameter**, not the event that we reject any false candidate. Simultaneous inference for several estimands is a different requirement.

Before sampling, the data and interval are random. After observing $x$, the interval and true parameter are fixed; the coverage statement does not supply a posterior probability that the parameter lies in this particular interval. It also does not make all retained values equally likely. This is the distinction already written at the bottom of my p. 3. The general duality is stated in [Berkeley Stat 210A, Duality of tests and confidence regions](https://stat210a.berkeley.edu/fall-2025/reader/testing-interpretation.html#duality-of-tests-and-confidence-regions).

## 6. When a reported CI and p-value need not agree

The equivalence requires the **same null value, estimand, model, standard error, reference distribution, sidedness and procedure**, with confidence level $1-\alpha$ and compatible endpoints.

- **One-sided versus two-sided:** a two-sided $z=1.8$ gives $p\approx0.0719$, while the upper-tail p-value is $0.0359$. A two-sided 95% interval can contain 0 even though the one-sided 5% test rejects it. The one-sided partner is a 95% lower confidence bound, not that two-sided interval.
- **Different methods:** a robust-SE test and a classical-SE interval, a Wald test and a bootstrap interval, or an adjusted p-value and an unadjusted interval are not automatically dual procedures.
- **Discrete data:** exact nonrandomized tests often have size below the nominal level and inverted coverage above it. Choose tails and equality conventions explicitly. If a test is randomized, inversion of actual decisions must account for the same auxiliary randomization; a fractional rejection probability is not itself a deterministic accept/reject outcome.
- **Different questions:** an interval for one coefficient does not invert a joint test of several coefficients. Nor does a prediction interval for a future response invert the ordinary coefficient test.

Finally, “0 is excluded” does not say the effect is practically large, and “0 is retained” does not establish no effect. The interval shows the compatible scale and uncertainty; the p-value summarizes one candidate's discrepancy, not scientific importance.

## Connections

- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/p-value interpretation|p-value interpretation]] — Holding the data fixed turns candidate-specific null-tail probabilities into a p-value curve; its level set, not a posterior mass calculation, gives the matching confidence interval.

## Origin

> [!info]- Source details
> Migrates the old vault's CI/p-value question, constrained-slope derivation and relevant regression synthesis, checked against all four pages of the original handwritten PDF; pp. 2–3 are embedded without alteration. The old four-page file is preserved separately from the already-migrated six-page export. Legacy text snapshots retain their exact bytes as `.md.txt` source records, not active old-vault links.
>
> My contribution is the handwritten testing-versus-interval question pair, geometric fit comparison, and repeated-sampling interpretation. The question wording above is a labeled paraphrase, not a recovered conversation quote. Earlier and current Codex explanations supply the precise assumptions and corrections; the acceptance-band diagram, p-value-curve animation, explicit decision-family link and coverage proof are current synthesis. Full regression/F/t derivations remain in their existing note.
>
> The original referenced conversation remains unavailable (R-004); no unseen turns or new coverage of that conversation are claimed. Mathematics, endpoint conventions and numerical examples were checked; the reproducible figure script and checks are linked in sources. Editorial review and mastery are separate from these checks.
>
> The 2026-11-10 slice-length extension follows my clarification that I meant horizontal versus vertical lengths. Codex supplied the uniform-scale counterexample, exact inversion and coverage calculation, and reproducible two-panel SVG. The earlier asymmetric additive-noise example does not demonstrate unequal lengths and is not embedded here. No original handwriting or prior figure was altered.
