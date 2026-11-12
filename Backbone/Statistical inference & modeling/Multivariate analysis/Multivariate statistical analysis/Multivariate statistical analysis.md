---
id: multivariate-course
title: Multivariate statistical analysis
layer: backbone
level: 3
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Multivariate analysis → Multivariate statistical analysis
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/3
- study/undergraduate-masters
node_kind: group
parent: '[[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate analysis]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/mining]]'
---

# Multivariate statistical analysis

Statistical inference & modeling → Multivariate analysis → Multivariate statistical analysis

Parent: [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate analysis|Multivariate analysis]]

## 1. See it and use it

Suppose each person supplies two measurements, such as two test scores. Their separate averages tell us little about whether the same people score highly on both. **Multivariate statistical analysis studies several variables jointly, including how they vary together.** Represent one person's measurements by a vector; place people in rows and variables in columns of a data matrix. [Penn State STAT 505, Lesson 1, overview and mean-vector section](https://online.stat.psu.edu/stat505/Lesson01).

![[assets/figures/2026-11-12-gp-ridge/multivariate-pairing.svg]]
*Original constructed example. Both panels contain the same two lists of values; only their pairing changes. The diagonal direction reveals information absent from the separate means and variances.*

In this example, each variable has mean 0 and sample variance 2.5. The sample covariance is $+2.5$ on the left and $-2.5$ on the right. To begin an analysis, retain each observation's full vector, examine the joint plot, and summarize the mean vector and covariance matrix. These summarize centre and pairwise variation; they need not describe the whole distribution.

The [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Multivariate normal laws|multivariate normal law]] is one useful joint model. In a [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Local methods & kernels/Gaussian process regression|Gaussian process]], the vector's coordinates instead represent function values at selected inputs; their covariance expresses how learning one value helps predict another. Multivariate analysis itself does not require normally distributed data.

## Origin

> [!info]- Source details
> Introductory enrichment requested on 2026-11-12 to support Gaussian-process learning. The standard joint-data viewpoint is sourced above; the paired-data example and diagram are original Codex illustrations. Covariances use the sample denominator $n-1=4$. Reproducible source: [[assets/figures/2026-11-12-gp-ridge/build_visuals.py]]. No new hierarchy or typed map relationship was added.

```atlas
```
