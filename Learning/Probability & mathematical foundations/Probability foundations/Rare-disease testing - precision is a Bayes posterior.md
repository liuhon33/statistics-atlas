---
id: learning-rare-disease-precision-bayes
title: Rare-disease testing - precision is a Bayes posterior
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule]]'
subject: probability
backbone_path: Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule
study_band: U
note_types: [question, insight, topic-note]
question_roles: [concept-distinction, cross-topic-connection, surprising-result]
source_format: conversation
created: '2026-11-15'
updated: 2026-11-16
status: active
verification: checked
learning_state: unknown
aliases: [99 percent accurate test, Base-rate fallacy and precision]
tags: [atlas/learning, subject/probability, topic/bayes, topic/classification]
connections:
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/ROC and precision–recall]]'
- '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles]]'
sources:
- '[[assets/figures/2026-11-10-testing-power/precision-population-area-vs-auc.svg]]'
- '[[assets/figures/2026-11-15-rare-disease-precision/draw_rectangles.py]]'
- '[[assets/figures/2026-11-15-rare-disease-precision/checks.json]]'
---

# Rare-disease testing - precision is a Bayes posterior

Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule

**Why does a “99%-accurate” test not mean a positive patient is 99% likely to have the disease?**

**The key insight:** that patient question asks for **precision**, not accuracy or sensitivity. The green/red bar is Bayes' rule: **keep only positive tests, then divide green by green + red.**

## 1. The classic case

Suppose disease prevalence is **1%**, sensitivity is **99%**, and specificity is **99%**. For a hypothetical population of 10,000, the expected counts are:

| Actual condition | Test positive $+$ | Test negative $-$ |
| --- | ---: | ---: |
| Disease: 100 | TP = **99** | FN = 1 |
| No disease: 9,900 | FP = **99** | TN = 9,801 |

TP/TN mean true positives/negatives; FP/FN mean false positives/negatives. These are model-based counts, not a guarantee for every sample.

**Among the 198 positive tests, only 99 have disease: precision is 50%.** A 1% false-alarm rate applied to the much larger disease-free group creates as many positives as the diseased group.

## 2. Same counts, different denominators

Let $D$ mean disease, $D^c$ no disease, and $N=10{,}000$.

| Quantity | Which group is the denominator? | Formula | Here |
| --- | --- | --- | ---: |
| Prevalence / prior | Everyone | $\pi=P(D)$ | 1% |
| Sensitivity / recall / TPR | People with disease | $P(+\mid D)=TP/(TP+FN)$ | 99% |
| Specificity / TNR | People without disease | $P(-\mid D^c)=TN/(TN+FP)$ | 99% |
| False-positive rate (FPR) | People without disease | $P(+\mid D^c)=FP/(FP+TN)$ | 1% |
| False-negative rate (FNR) | People with disease | $P(-\mid D)=FN/(FN+TP)$ | 1% |
| **Precision / positive predictive value (PPV)** | **People testing positive** | **$P(D\mid +)=TP/(TP+FP)$** | **50%** |
| Negative predictive value (NPV) | People testing negative | $P(D^c\mid -)=TN/(TN+FN)$ | $9801/9802\approx99.99\%$ |
| Accuracy | Everyone | $(TP+TN)/N$ | 99% |

Accuracy really is $(99+9801)/10000=99\%$, but its denominator is **not** the positive-test group. “99% accurate” alone does not specify the conditional error rates. [Metric definitions: Google ML Crash Course](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall).

## 3. The rectangles are the Bayesian calculation

![[assets/figures/2026-11-15-rare-disease-precision/rare-disease-rectangles.svg|1000]]
*Original illustration. Left: widths are prior probabilities; retained heights are positive-test rates. Green and red have equal area despite their different shapes. Right: their combined 1.98% population mass becomes the new 100%; the bar is renormalized, not on the population scale.*

Write $y=\mathrm{TPR}$ and $x=\mathrm{FPR}$. The retained joint areas are **green $=\pi y$** and **red $=(1-\pi)x$**. Therefore

$$
\begin{aligned}
\underbrace{P(D\mid +)}_{\text{precision / posterior}}
&=\frac{\overbrace{P(D)}^{\text{prior}}\,\overbrace{P(+\mid D)}^{\text{likelihood}}}{P(+)}\\
&=\frac{\pi y}{\pi y+(1-\pi)x}\\
&=\frac{0.01(0.99)}{0.01(0.99)+0.99(0.01)}=\frac12.
\end{aligned}
$$

This requires $P(+)>0$ and a population/prior and test rates applicable to the person; additional individual information can change the posterior. **If “99%” actually meant precision in that population, it would answer the positive-patient question.** [Bayes' rule and the false-positive paradox: Pishro-Nik, §1.4.3](https://www.probabilitycourse.com/chapter1/1_4_3_bayes_rule.php).

> [!info]- The original ROC-note picture — same mechanism, different numbers
> ![[assets/figures/2026-11-10-testing-power/precision-population-area-vs-auc.svg|900]]
>
> *Reused unchanged. Factory example: prevalence 10%, TPR 80%, FPR 5%; green $=8\%$, red $=4.5\%$, so precision $=8/(8+4.5)=64\%$. The purple ROC area is AUC, not this posterior.*

## 4. ROC and hypothesis testing: what carries over?

- **ROC:** this disease example is the point $(\mathrm{FPR},\mathrm{TPR})=(0.01,0.99)$. Those coordinates describe the two groups separately; **precision also needs their prevalence**. Holding both rates fixed while changing prevalence changes precision, not the point.
- **Testing:** let $H_0$ mean no disease, $H_1$ disease, and “positive” mean reject $H_0$. Here Type I error is 1%, Type II error is 1%, and power is 99%. Yet **$P(H_0\mid\text{reject})=1-\mathrm{precision}=50\%$**, not 1%. A frequentist test alone does not supply probabilities for the hypotheses; this posterior additionally uses the population/prior model.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/ROC and precision–recall|ROC and precision–recall]] — Its green/red population areas give precision once the ROC rates are weighted by prevalence.
- [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Tests & confidence sets/Testing principles/Testing principles|Testing principles]] — Type I error and power condition on truth; precision reverses that conditioning and needs a prior/base rate.

## Origin

> [!info]- Source details
> Current conversation, 2026-11-15: the user's rare-disease question and recognition that “the red/green bar is exactly showing the bayesian!” The question above is a labelled paraphrase. The numerical example, comparison table and new rectangle figure are assistant-added explanations; the selected ROC figure is unchanged. No clinical data or individualized diagnosis is claimed.
>
> Metric definitions and Bayes' identity were checked against the linked sources; the 1%/99%/99% inputs are this conversation's teaching example, not the textbook's different numerical example. Exact fractions, count denominators, rectangle areas and the original 64% example were independently checked in the linked figure record. Both figure previews were inspected; live Obsidian rendering was not tested.
