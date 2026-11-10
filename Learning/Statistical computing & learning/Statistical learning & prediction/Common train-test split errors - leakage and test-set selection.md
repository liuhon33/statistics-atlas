---
id: learning-train-test-split-errors
title: Common train-test split errors - leakage and test-set selection
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Train - validation - test splits]]"
subject: computing
backbone_path: "Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Validation & model selection → Train / validation / test splits"
study_band: U–M
note_types: [derivation, insight, topic-note]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
aliases: [train test split bias in ML]
tags: [atlas/learning, subject/computing]
connections:
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Data leakage]]"
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Group and temporal splits]]"
sources:
  - "[[raw/assets/2026-11-08-Train-test-split-and-KNN-I01-original-notes.png]]"
  - "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage"
  - "https://scikit-learn.org/stable/modules/cross_validation.html"
---

# Common train-test split errors - leakage and test-set selection

Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Validation & model selection → Train / validation / test splits

**Separate rows are not enough: the test set must remain outside the decisions that construct or select the model.** My examples expose three different failures: repeated subjects across a split, choosing the best model on test scores, and choosing features using test labels.

## My original notes

![[raw/assets/2026-11-08-Train-test-split-and-KNN-I01-original-notes.png]]

*Original page, preserved unchanged. The left and middle sections support this note; the right-hand KNN/K-means comparison is digested separately. Feature A in training row 3 was confirmed by me as 0.9 during transcription.*

## 1. Repeated visits are not independent new subjects

The upper-left sketch puts A with label 1 and B with label 0 in both train and test. If these are repeated visits from the same people, a model could recognize the people rather than learn a rule that transfers to unseen people. This is **group leakage relative to a new-person prediction goal**; it is not the same mechanism as choosing between random guessers below.

For performance on new people, hold out entire people. For future observations, respect time and ensure every predictor is available at the intended prediction time. Predicting later visits for already-known people is a different target: sharing a person across sets is not automatically wrong for that target, but using future information still is. [Reference: scikit-learn, grouped and time-series cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

## 2. Picking the better test score makes guessing look useful

My 68.75% calculation is correct under an explicit experiment:

- Two candidate models each make independent fair binary guesses on the same two held-out cases.
- All four guess outcomes are independent, conditional on the two true labels.
- I inspect both test scores, select the larger, and report that same score.

For one guesser, let $S$ be its accuracy on those two cases. Then

$$
P(S=0)=\frac14,\qquad P(S=\tfrac12)=\frac12,\qquad P(S=1)=\frac14.
$$

The reported score is $M=\max(S_1,S_2)$, not the score of a model chosen independently of the test data:

| Reported score | Event | Probability |
| --- | --- | --- |
| 0% | Both scores are 0 | $(1/4)^2=1/16$ |
| 50% | Neither score is 100%, and at least one is 50% | $(3/4)^2-(1/4)^2=8/16$ |
| 100% | At least one score is 100% | $1-(3/4)^2=7/16$ |

Therefore

$$
\mathbb E[M]
=0\frac1{16}+\frac12\frac8{16}+1\frac7{16}
=\frac{11}{16}=68.75\%.
$$

**The selected guesser still has 50% expected accuracy on fresh independent cases.** The 18.75-percentage-point uplift is optimism in the reused test score, not acquired predictive ability. Selecting on a separate validation set would not produce this uplift on an untouched test set under these assumptions.

The same construction with $m$ independent guessers gives

$$
\mathbb E\!\left[\max_{1\le j\le m}S_j\right]
=1-\frac12\left(\frac34\right)^m-\frac12\left(\frac14\right)^m.
$$

This tends to 1 even though every guesser remains useless on fresh cases. This extension is added synthesis; real candidate models often have correlated errors, so the independence formula is not a universal bias correction.

## 3. Feature selection is part of training

My middle example uses the following values:

| Split | Row | Feature A | Feature B | $y$ |
| --- | --- | --- | --- | --- |
| Train | 1 | 0.0 | 0.0 | 0 |
| Train | 2 | 0.1 | 0.4 | 0 |
| Train | 3 | 0.9 | 0.6 | 1 |
| Train | 4 | 1.0 | 1.0 | 1 |
| Test | 5 | 1.0 | 0.0 | 0 |
| Test | 6 | 0.9 | 0.1 | 0 |
| Test | 7 | 0.1 | 0.8 | 1 |
| Test | 8 | 0.0 | 1.0 | 1 |

Make the rule explicit: predict 1 when the selected feature exceeds 0.5. Both features classify the training rows perfectly. **Suppose the training-only selection rule breaks this tie in favor of A.** Its test predictions are $(1,1,0,0)$, opposite to the labels, so test accuracy is 0%.

If the pipeline peeks at the last four labels and selects B instead, its test predictions are $(0,0,1,1)$ and the reported accuracy is 100%. But those labels helped select the predictor: the score no longer independently evaluates that selection procedure.

Two qualifications sharpen the example:

- A training-only pipeline does not necessarily select A; the tie-breaking assumption matters. Selecting B without peeking would not itself be leakage.
- Honest splitting does not guarantee high accuracy. This deliberately constructed example shows an honest failure versus a contaminated success, not that clean pipelines generally score 0%.

My “10,000 generated features” observation is the same mechanism at scale: if labels are independent of the features, searching many features can find accidental alignment. Using all labels for the search makes even test-label coincidences available to the selector. With selection restricted to training data and fresh fair independent test labels, expected test accuracy stays 50%, though a finite test sample can fluctuate. The official example demonstrates this with random features and labels. [Reference: scikit-learn, leakage during preprocessing](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage-during-pre-processing).

## Practical boundary

1. Choose the split unit and time direction to match the intended deployment.
2. Fit imputation, scaling, feature selection and the estimator on training data only. Inside cross-validation, refit the whole pipeline within each training fold.
3. Use validation data or inner CV for model choices; reserve test data or outer folds for evaluating the selected procedure.
4. Once a test score drives another choice, that set is serving as validation, not an untouched final test.

[References: preprocessing boundaries](https://scikit-learn.org/stable/common_pitfalls.html#how-to-avoid-data-leakage) and [model-selection/evaluation boundaries](https://scikit-learn.org/stable/modules/cross_validation.html).

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Data leakage|Data leakage]] — Feature selection and model selection can transmit held-out information even when the estimator never directly fits the test rows.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Group and temporal splits|Group and temporal splits]] — The repeated-visit sketch requires choosing a split unit and time boundary that match the intended generalization target.

## Origin

> [!info]- Source details
> My supplied handwritten page, left and middle sections. The examples and $11/16$ result are mine; the explicit independence assumptions, tie-breaking condition, distinction between leakage mechanisms, $m$-model extension and practical summary are assistant-added clarification. The row-3 digit was confirmed by me as 0.9. The probability derivation and both threshold prediction vectors were checked analytically and by exhaustive finite enumeration; reference guidance was checked against the linked official documentation. No original ink was altered.
