---
id: test-theory-type-i-and-ii-errors
title: Type I and II errors
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles → Type I and II errors
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles]]'
sources:
- '[[_system/Sources/theory]]'
- '[[_system/Sources/asym]]'
- '[[assets/figures/2026-11-10-testing-power/draw_roc_relationships.py]]'
- '[[assets/figures/2026-11-12-classification-errors/build_excerpts.py]]'
- '[[assets/figures/2026-11-12-classification-errors/checks.json]]'
---

# Type I and II errors

Statistical inference & modeling → Frequentist & likelihood inference → Tests & confidence sets → Testing principles → Type I and II errors

Parent: [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles|Testing principles]]

## 1. See it and use it — false alarm versus missed fault

A quality-control alarm checks whether a part is faulty. The **null hypothesis $H_0$** says it works; the **alternative $H_1$** says it has a fault. A high score triggers the alarm: statistically, we **reject $H_0$**.

![[assets/figures/2026-11-12-classification-errors/two-error-areas.svg|700]]
*Same cutoff, two possible truths. Each curve has area 1: red = 5% false alarms; amber = 20% misses. Excerpt of the existing illustration.*

- **Type I error:** flag a working part—a **false alarm**.
- **Type II error:** fail to flag a faulty part—a **miss**.

Across repeated checks, this model averages 5 false alarms per 100 working-part checks. At the specified fault severity, 20 of 100 checks miss the fault; 80 detect it. That 80% detection probability is **power**.

**How to use these ideas:** choose the acceptable false-alarm budget $\alpha$ before looking at results, then seek good power for faults that matter. A stricter cutoff reduces false alarms but increases misses in this model. “Did not reject” means insufficient evidence to flag the part—not proof that it works. [Berkeley Stat 210A, §§1 and 2.1](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html#significance-level-and-power).

## 2. How it connects — one rule, different denominators

### The error budget is not automatically the actual error rate

Let $T$ be the score and reject when $T>c$. Under a specified null distribution $P_0$ and alternative distribution $P_1$,

$$
r_0=P_0(T>c),\qquad
\beta_{\mathrm{II}}=P_1(T\le c),\qquad
\mathrm{Power}=P_1(T>c)=1-\beta_{\mathrm{II}}.
$$

The complement identity uses the **same alternative distribution**: either the fault is missed or it is detected. It does not say that Type I plus Type II error equals 1; they use different distributions.

A level-$\alpha$ test controls rejection probability under **every** parameter value allowed by the [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Null and alternative|null hypothesis]]:

$$
\sup_{\theta\in\Theta_0}P_\theta(\text{reject }H_0)\le\alpha.
$$

Thus $\alpha$ is a ceiling, not necessarily the attained rate. The displayed example attains 5%; a conservative test can be below it. With a composite alternative, power and Type II error depend on the particular true effect or fault severity. Here $\beta_{\mathrm{II}}$ denotes missed-detection probability, not a power-function symbol. [Berkeley Stat 210A, §2.1](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html#significance-level-and-power).

### A confusion matrix and an ROC point describe the same decision

![[assets/figures/2026-11-10-testing-power/roc-error-rates.svg|900]]
*Reused unchanged. The upper panels show conditional probabilities. Only the lower panels add a population with 100 true alternatives and 900 true nulls, producing expected—not guaranteed—counts.*

Treat rejection as a **positive prediction** and the alternative as the **positive truth**. The table is a confusion matrix: it separates true positives, false positives, false negatives and true negatives. Its true-class columns give

$$
\underbrace{\mathrm{FPR}}_{\text{Type I}}=\frac{45}{900}=0.05,
\qquad
\underbrace{\mathrm{TPR}}_{\text{power}}=\frac{80}{100}=0.80,
\qquad
\underbrace{\mathrm{FNR}}_{\text{Type II}}=\frac{20}{100}=0.20.
$$

Specificity is $1-\mathrm{FPR}=0.95$. In [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/ROC and precision–recall|ROC coordinates]], the point is $(r_0,1-\beta_{\mathrm{II}})$. **Maximizing power under an error budget means going as high as possible without moving right of $\alpha$.**

But among the **125 flagged cases**, 45 are false alarms: $45/125=36\%$, not 5%. Precision is the complementary $80/125=64\%$. Reversing the conditioning requires an added prevalence model and [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule|Bayes' rule]]; an ordinary frequentist test with one fixed unknown parameter supplies neither a prior probability of $H_0$ nor a posterior probability given rejection. For composite classes, population rates average over their specified within-class distributions; they are not automatically power at one chosen effect.

### Moving a cutoff is not the only way to improve a test

For fixed score distributions, lowering $c$ enlarges the rejection region: power cannot decrease, but neither can Type I error. Both increase in the continuous example above. This moves along one ROC curve; it does not generally improve power for free.

The [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Neyman–Pearson lemma|Neyman–Pearson lemma]] instead compares **all decision rules** for two specified distributions: ranking possible datasets by alternative-to-null likelihood ratio gives greatest power at the controlled error level, with boundary randomization when needed. [Berkeley Stat 210A, §3.1](https://stat210a.berkeley.edu/fall-2024/reader/hypothesis-testing.html#likelihood-ratio-test).

[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Power and sample size|Power and sample size]] asks a different design question: how much data will a chosen test need to detect a specified effect at the selected $\alpha$? More informative data can increase power without relaxing the false-alarm budget.

## Origin

> [!info]- Source details
> Condensed from the supplied hypothesis-testing learning note's error-budget and ROC explanations; detailed attribution is in the 2026-11-12 enrichment Log entry. The quality-control interpretation is added teaching prose, not observed data. The long note, handwriting and original figures remain unchanged.
>
> Both figures use the original constructed normal-score model: $S\mid H_0\sim N(0,1)$ and $S\mid H_1\sim N(z_{0.95}+z_{0.80},1)$, with cutoff $z_{0.95}\approx1.645$; $z_q$ denotes a standard-normal quantile. Its power is 80%. This is not the separate $N(0,1)$ versus $N(2,1)$ illustration, whose power at that cutoff is about 63.9%. The introductory SVG preserves the plotted geometry and labels in a focused viewport; the full figure is reused unchanged.
>
> Berkeley Stat 210A §§1–3.1 were read to check error definitions, conservative levels, parameter-dependent power and the simple-hypothesis Neyman–Pearson statement. The older theory/asymptotics catalog references are retained, not newly claimed as inspected. Counts, complements, normal tails and preservation checks are in [[assets/figures/2026-11-12-classification-errors/checks.json]]. Static previews were inspected; live Obsidian rendering was not available. Inline links only; no new map relationships.

```atlas
```
