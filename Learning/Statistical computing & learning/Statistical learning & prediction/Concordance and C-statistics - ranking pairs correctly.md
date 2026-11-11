---
id: learning-concordance-c-statistics
title: Concordance and C-statistics - ranking pairs correctly
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Evaluating predictions/ROC and precision–recall]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Evaluating predictions → ROC and precision–recall
study_band: U–M
note_types: [topic-note, derivation]
source_format: conversation
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
aliases: [C-statistic, Concordance index, C-index]
tags: [atlas/learning, subject/computing, topic/model-evaluation]
---

# Concordance and C-statistics - ranking pairs correctly

Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Evaluating predictions → ROC and precision–recall

**Concordance asks whether a model puts two observations in the correct order. The C-statistic summarizes how often it succeeds.** It evaluates ranking, not the accuracy of the numerical predictions themselves.

Unlike [[Learning/Statistical inference & modeling/Regression & linear models/Categorical association and Cramér's V#6. What V does not tell you|Cramér's V]], concordance uses ordering.

## Part 1 — See it and use it

### Start with four predictions

Suppose a model scores whether a machine will fail within one year. Higher scores mean greater predicted risk. All four machines have a known one-year outcome.

| Machine | Actually failed? | Predicted score |
| --- | --- | --- |
| A | Yes | 0.9 |
| B | Yes | 0.4 |
| C | No | 0.6 |
| D | No | 0.2 |

Compare **each failed machine with each nonfailed machine**. A beats C and D; B beats D but loses to C. Three of four comparisons are correct, so the C-statistic is $3/4=0.75$.

![[assets/figures/2026-11-11-concordance/01-pair-grid.svg]]

*Each cell is one positive–negative pair, not one machine. Green earns 1; orange earns 0. The mean of the four cells is 0.75.*

### Definition and interpretation

A **concordant pair** has its scores ordered in the direction indicated by the outcomes; a **discordant pair** has the reverse order. With the usual half-credit rule for equal scores,

$$
\widehat C=
\frac{N_{\mathrm{concordant}}+\tfrac12N_{\mathrm{score\ ties}}}
{N_{\mathrm{comparable\ pairs}}}.
$$

The denominator includes score ties, but excludes pairs whose outcomes cannot be ordered. For binary outcomes, only positive–negative pairs count. Here, A–B and C–D are excluded: they have the same outcome, regardless of their scores. For binary outcomes this C-statistic equals the usual **[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Hypothesis testing - maximizing power under an error budget#ROC area: AUC is a ranking probability, not precision|area under the ROC curve (AUROC)]]**. [Therneau and Atkinson, *Concordance*, §1.1, pp. 1–2](https://stat.ethz.ch/R-manual/R-devel/library/survival/doc/concordance.pdf).

- **1:** every comparable pair is correctly ranked.
- **0.5:** chance-level ranking; independent random scores give 0.5 in expectation, not necessarily in every sample. All-equal scores also give exactly 0.5.
- **0:** every comparable pair is reversed. Below 0.5 can indicate reversed score direction or genuinely poor ranking.

Thus **0.75 means 75% pairwise credit**, not “75% of individual machines classified correctly.” No classification threshold was chosen.

### Toy example 2 — A tie earns half

Change B's score from 0.4 to 0.6. Now A–C, A–D and B–D earn 1 each, while B–C earns $1/2$:

$$
\widehat C=\frac{3+0.5}{4}=0.875.
$$

If both classes are not present, there are no positive–negative pairs: the binary statistic is **undefined**, not zero.

### Toy example 3 — Survival times and censoring

Instead of a one-year yes/no outcome, suppose we predict **how early a machine fails**. A larger risk score should now correspond to a **shorter** failure time.

| Machine | Observed time | What was observed? | Risk score |
| --- | --- | --- | --- |
| A | 2 months | Failed | 0.9 |
| B | 4 months | Still working when observation stopped | 0.8 |
| C | 6 months | Failed | 0.3 |
| D | 8 months | Failed | 0.6 |

B is **right-censored**: its true failure time is later than month 4, but unknown.

![[assets/figures/2026-11-11-concordance/02-survival-pairs.svg]]

*Circles mark observed failures; the arrow marks B's unknown future. The four scored pairs are A–B, A–C, A–D and C–D.*

- A–B is comparable: B was still working after A failed. So are A–C and A–D. All three are concordant.
- C–D is comparable, but discordant: C failed first despite receiving the lower risk score.
- B–C and B–D are **not comparable**: B could have failed before or after either machine.

Harrell's C is therefore $3/4=0.75$, **not $3/6$**. The discarded pairs are unknown, not mistakes.

For distinct observed times, a pair is comparable when the earlier observation is an actual event, not censoring; equal risk scores receive half credit. Equal failure times are excluded. Event/censor ties at the same recorded time need an explicit software convention; this example avoids them. [scikit-survival, `concordance_index_censored`, definition and parameters](https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.metrics.concordance_index_censored.html).

### How to use it

1. **Fix the outcome and score direction.** Binary: larger means more likely positive. Survival risk: larger means earlier event. A predicted survival *duration* has the opposite direction.
2. **[[Learning/Statistical computing & learning/Statistical learning & prediction/Common train-test split errors - leakage and test-set selection#Practical boundary|Evaluate predictions on held-out observations]]**, not only the training sample. Compare models on the same evaluation cases and outcome definition.
3. **Keep scores, not thresholded labels.** For fully observed binary labels coded 0/1, use the score for class 1:

   ```python
   from sklearn.metrics import roc_auc_score
   y = [1, 1, 0, 0]
   score = [0.9, 0.4, 0.6, 0.2]
   print(roc_auc_score(y, score))  # 0.75
   ```

   Probabilities or non-thresholded decision scores are accepted. [scikit-learn, `roc_auc_score`, `y_score` parameter](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html).

4. **Report what C does not answer.** Scores 0.9, 0.4, 0.6, 0.2 and 0.99, 0.94, 0.96, 0.92 give the same ranking and C, but make very different probability claims. C alone does not assess **calibration**—whether predicted probabilities match observed frequencies—or select an operating threshold.
5. **For censored outcomes, name the estimator.** Harrell's C can be biased upward with substantial censoring; censoring-adjusted alternatives exist. Overall survival concordance is not automatically the AUC for “failure by month 12.” Do not code a machine censored before month 12 as a known nonfailure at month 12. [scikit-survival, *Evaluating Survival Models*, introduction and “Bias of Harrell's Concordance Index”](https://scikit-survival.readthedocs.io/en/stable/user_guide/evaluating-survival-models.html).

## Part 2 — Why binary C equals ROC area

This proof is for **fully observed binary outcomes**, with at least one observation in each class, equally weighted observations, and the empirical ROC curve joined linearly through score-tie blocks. It is not a proof that censored-survival C equals an ordinary binary AUC.

### Write pair-counting as a formula

Let $n_+$ and $n_-$ be the positive and negative counts; $s_i^+$ and $s_j^-$ are their scores. Define

$$
h(a,b)=\mathbf 1\{a>b\}+\tfrac12\mathbf 1\{a=b\},
\qquad
\widehat C=\frac1{n_+n_-}\sum_{i=1}^{n_+}\sum_{j=1}^{n_-}h(s_i^+,s_j^-).
$$

There are $n_+n_-$ eligible pairs. Choosing one positive and one negative uniformly from the sample makes this average their expected comparison credit. The population counterpart, for independently drawn class-conditional scores $S^+$ and $S^-$, is

$$
C=P(S^+>S^-)+\tfrac12P(S^+=S^-).
$$

### Count the same pairs through ROC strips

Lower a threshold from above all scores to below them. A machine becomes predicted-positive when its score crosses that threshold. The horizontal coordinate is the **false-positive rate**, the fraction of negatives admitted; the vertical coordinate is the **true-positive rate**, the fraction of positives admitted.

![[assets/figures/2026-11-11-concordance/03-roc-area.svg]]

*For the first example, entering negative C makes a strip of width 1/2 and height 1/2; entering negative D makes a strip of width 1/2 and height 1. Total area: 1/4 + 1/2 = 3/4.*

Without ties, a positive contributes a vertical step and no area. Each negative $j$ contributes a horizontal strip of width $1/n_-$ at height

$$
\frac{\#\{i:s_i^+>s_j^-\}}{n_+}.
$$

Adding strips counts exactly the positive–negative pairs that the score ranks correctly.

**Now allow ties.** At a score value $v$, suppose $a$ positives and $b$ negatives are tied, and $A$ positives have strictly higher scores. The ROC segment has width $b/n_-$ and rises from height $A/n_+$ to $(A+a)/n_+$. Its trapezoidal area is

$$
\frac{b}{n_-}\frac{A+(A+a)}{2n_+}
=\frac{Ab+\tfrac12ab}{n_+n_-}.
$$

Here $Ab$ counts strict wins against those negatives, and $ab$ counts tied positive–negative pairs. Sum over score values:

$$
\boxed{\widehat{\mathrm{AUROC}}
=\frac{N_{\mathrm{concordant}}+\tfrac12N_{\mathrm{score\ ties}}}{n_+n_-}
=\widehat C.}
$$

This is an original step-by-step derivation of the binary equivalence stated in [Therneau and Atkinson, §1.1, p. 2](https://stat.ethz.ch/R-manual/R-devel/library/survival/doc/concordance.pdf). Deeper rank-statistic connections and censoring-adjusted derivations are deliberately left for another visit.

## Origin

> [!info]- Source details
> Requested as a starter learning note when no dedicated concordance/C-statistic backbone page was found. No source document, personal derivation or handwritten image was supplied. Explanations, machine examples, proof presentation and all three figures are agent-added synthesis, not attributed to the user.
>
> Read: Therneau and Atkinson, *Concordance*, §1.1 and the opening of §2; the linked scikit-survival definition and evaluation guidance; and scikit-learn's binary AUC API definition. Web citations are inline. Scope excludes deeper connections and survival-estimator proofs; no additional conceptual map links were added.
>
> Reproducible figures and checks: [[assets/figures/2026-11-11-concordance/draw_concordance.py]] and [[assets/figures/2026-11-11-concordance/checks.json]]. Toy arithmetic and the empirical tie-block identity were checked computationally; the proof above provides the algebraic justification. Static previews were inspected, not live Obsidian rendering.
