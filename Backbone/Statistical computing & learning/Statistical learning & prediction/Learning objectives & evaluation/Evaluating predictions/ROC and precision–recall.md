---
id: prediction-assessment-roc-and-precisionrecall
title: ROC and precision–recall
layer: backbone
level: 5
subject: computing
study_band: U–M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Evaluating predictions → ROC and precision–recall
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/computing
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/Evaluating predictions]]'
sources:
- '[[_system/Sources/isl]]'
- '[[assets/figures/2026-11-10-testing-power/draw_roc_relationships.py]]'
- '[[assets/figures/2026-11-10-testing-power/draw_precision_areas.py]]'
- '[[assets/figures/2026-11-12-classification-errors/build_excerpts.py]]'
- '[[assets/figures/2026-11-12-classification-errors/checks.json]]'
---

# ROC and precision–recall

Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Evaluating predictions → ROC and precision–recall

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/Evaluating predictions|Evaluating predictions]]

## 1. See it and use it — catching faults without too many false alarms

Imagine a factory gives each part a **suspicion score**. Flag a part when its score exceeds a cutoff. Lowering the cutoff can catch more faulty parts, but also flag more working parts.

![[assets/figures/2026-11-12-classification-errors/roc-operating-point.svg|650]]
*Start with the axes and black dot; unpack the error labels below. Excerpt of the existing illustrative graph.*

An **ROC curve** (receiver operating characteristic) plots the results as we vary that cutoff:

- **Horizontal:** false-positive rate (FPR)—the fraction of working parts wrongly flagged.
- **Vertical:** true-positive rate (TPR), also called **recall** or **sensitivity**—the fraction of faulty parts caught.

For example, catching 80 of 100 faulty parts and wrongly flagging 45 of 900 working parts gives **$(0.05,0.80)$**, not $(45,80)$.

**How to use it:** if at most 5% of working parts may be flagged, find the highest reachable point with FPR at most $0.05$. Up is better at the same horizontal position. You—not the curve—choose the acceptable false-alarm rate. [Google ML Crash Course, “ROC” and “Choosing model and threshold”](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc).

## 2. How it connects — the matrix, testing errors, and precision

### One cutoff gives one confusion matrix

A **confusion matrix** cross-tabulates predictions against truth. Here rows are predictions and columns are truth; other presentations may transpose them. **Positive** means “flagged as faulty,” not “good.” [Google ML Crash Course, “Confusion matrix”](https://developers.google.com/machine-learning/crash-course/classification/thresholding).

| Decision | Actually faulty: 100 | Actually working: 900 |
|---|---:|---:|
| Flag / predict positive | **80 true positives (TP)** | **45 false positives (FP)** |
| Do not flag / predict negative | **20 false negatives (FN)** | **855 true negatives (TN)** |

These are the original illustration's **expected counts** for 1,000 cases with 10% faults, not guaranteed counts in every sample. Read within the true-class columns to get the ROC point:

$$
\mathrm{TPR}=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}=\frac{80}{100}=0.80,
\qquad
\mathrm{FPR}=\frac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}=\frac{45}{900}=0.05.
$$

Thus **one matrix gives one point; varying the cutoff gives a curve**. Actual labeled evaluation data give empirical counts and estimated rates; an observed 5% FPR alone does not guarantee 5% population error control. Choose a cutoff on validation data, then assess the frozen choice on separate test data; see [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Train - validation - test splits|train / validation / test splits]] and [Google's validation/test workflow](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets).

If “positive” means rejecting a true-working-part null, these become [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Type I and II errors|Type I error rate and power]]: FPR is Type I error, while $1-\mathrm{TPR}$ is Type II error. A level-$\alpha$ test requires FPR **at most** $\alpha$, not necessarily equal to it.

### Precision changes the denominator

Recall asks **“Of the faulty parts, how many did we catch?”** Precision asks **“Of the flagged parts, how many really are faulty?”** Here precision is $80/(80+45)=64\%$, not 80% and not specificity $855/900=95\%$. [Google ML Crash Course, “Recall,” “False positive rate” and “Precision”](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall).

![[assets/figures/2026-11-10-testing-power/precision-population-area-vs-auc.svg|900]]
*Reused unchanged: green and red are population fractions, whereas purple is area in ROC coordinates. Left: keep only flagged cases, then renormalize. Right: compare rankings across cutoffs.*

Let $\pi$ be the faulty-part fraction (**prevalence**), $y=\mathrm{TPR}$ and $x=\mathrm{FPR}$. Of the whole population, $\pi y$ are true positives and $(1-\pi)x$ are false positives. Therefore [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule|Bayes' rule]] gives

$$
\mathrm{Precision}=\frac{\pi y}{\pi y+(1-\pi)x}
=\frac{0.10(0.80)}{0.10(0.80)+0.90(0.05)}=0.64.
$$

This requires a positive denominator; with no positive predictions, precision is undefined. A **precision–recall (PR) curve** plots recall horizontally and precision vertically while varying the cutoff: this operating point is $(0.80,0.64)$ in PR coordinates.

If prevalence falls to 1% **while both class-conditional score distributions stay fixed**, the ROC curve stays the same but this point's precision falls to $16/115\approx13.9\%$. PR makes the burden of false alerts visible when positives are rare; see [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/Class imbalance|class imbalance]].

### AUC is ranking, not precision at one cutoff

**Area under the ROC curve (AUC)** summarizes ordering: for independently drawn positive and negative scores, it is the probability that the positive scores higher, plus half the tie probability under the usual interpolated-ROC convention. The illustrated continuous-score model has **AUC $\approx96.06\%$**, yet precision is 64% and recall is 80%. Neither AUC nor the area above the curve is a Type I/II error at the chosen cutoff. [Google ML Crash Course, “Area under the curve”](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc).

Maximizing full AUC also need not maximize power at your particular FPR budget. A standard ROC varies thresholds of **one fixed score**; it does not automatically include every possible decision rule.

## Origin

> [!info]- Source details
> Condensed from the supplied hypothesis-testing learning note, especially its ROC, confusion-matrix and population-area explanations; attribution to that note is recorded in the 2026-11-12 enrichment Log entry. The factory language is an added teaching example, not empirical evidence. No learning note or source original was edited.
>
> The existing four-view model uses $S\mid H_0\sim N(0,1)$ and $S\mid H_1\sim N(\delta,1)$, with $\delta=z_{0.95}+z_{0.80}$ and cutoff $z_{0.95}$. Here $z_q$ is the standard-normal $q$-quantile. It deliberately gives FPR $0.05$ and TPR $0.80$; prevalence $0.10$ is an additional population assumption. The focused ROC view preserves the SVG geometry and labels; the population-area/AUC figure is reused unchanged. Original generators are in `sources`; original numerical records are [[assets/figures/2026-11-10-testing-power/roc-error-rates-checks.json]] and [[assets/figures/2026-11-10-testing-power/precision-areas-checks.json]].
>
> The cited Google lessons were read for the metric definitions and ROC/PR/AUC interpretations; the existing ISL catalog reference is retained, without claiming a fresh book-page check. Exact count fractions, Bayes calculations, normal-score probabilities and figure preservation were rechecked in [[assets/figures/2026-11-12-classification-errors/checks.json]]. Introductory excerpts and original figure previews were inspected; live Obsidian rendering was not available. Inline links only; no new map relationships.

```atlas
```
