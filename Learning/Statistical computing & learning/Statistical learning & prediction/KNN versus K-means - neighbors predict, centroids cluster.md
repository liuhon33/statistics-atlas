---
id: learning-knn-versus-k-means
title: KNN versus K-means - neighbors predict, centroids cluster
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Local methods & kernels/Nearest neighbors]]"
subject: computing
backbone_path: "Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Local methods & kernels → Nearest neighbors"
study_band: U–M
note_types: [insight, topic-note]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
aliases: [KNN and K-means difference]
tags: [atlas/learning, subject/computing]
connections:
  - "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/K-means]]"
sources:
  - "[[raw/assets/2026-11-08-Train-test-split-and-KNN-I01-original-notes.png]]"
  - "https://scikit-learn.org/stable/modules/neighbors.html"
  - "https://scikit-learn.org/stable/modules/clustering.html#k-means"
---

# KNN versus K-means - neighbors predict, centroids cluster

Statistical computing & learning → Statistical learning & prediction → Supervised learning methods → Local methods & kernels → Nearest neighbors

**KNN asks nearby labeled examples to predict a target; K-means learns centers that partition unlabeled examples.** Their shared use of distance does not give the letter $k$ the same meaning.

## The comparison in my notes

| | K-nearest neighbors (KNN) | K-means |
| --- | --- | --- |
| Task | Supervised classification or regression | Unsupervised clustering |
| Input | Features $x_i$ and target values $y_i$ | Features $x_i$; no target labels required |
| Meaning of $k$ | Number of neighboring training examples consulted | Number of clusters/centroids fitted |
| Output | Predicted class or numerical target | Cluster assignment |
| Main operation | Vote or average over neighbors | Assign points to centers and update centers |

Sources: [scikit-learn nearest neighbors, §§1.6.2–1.6.3](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-classification) and [K-means, §2.3.2](https://scikit-learn.org/stable/modules/clustering.html#k-means).

The original sketches are on the **right side** of [[raw/assets/2026-11-08-Train-test-split-and-KNN-I01-original-notes.png|my preserved handwritten page]]. The full page is embedded once in the train–test split note rather than duplicated here. In my KNN drawing the pink query receives a yellow prediction from nearby labeled points; in the K-means drawing, the colored circles represent discovered groups, not supplied target classes.

## KNN: aggregate targets locally

Let $N_k(x)$ be the indices of the $k$ nearest training points to a query $x$. With uniform weights,

$$
\hat y_{\mathrm{classification}}(x)
=\operatorname*{arg\,max}_{c}\sum_{i\in N_k(x)}\mathbf 1\{y_i=c\},
\qquad
\hat y_{\mathrm{regression}}(x)
=\frac1k\sum_{i\in N_k(x)}y_i.
$$

Ties need a rule. Distance-weighted variants give nearer observations more influence. “Lazy learning” means prediction uses retained examples rather than a fitted global regression equation; fitting may still construct a search index.

*Added illustration:* if three selected neighbors have labels yellow, yellow, green, classification predicts yellow. If their numerical targets are 2, 4, 9, uniform-weight regression predicts 5. The nearest-neighbor search is the same kind of step; the target aggregation changes.

[Reference: scikit-learn, nearest-neighbor classification and regression](https://scikit-learn.org/stable/modules/neighbors.html).

## K-means: learn centers before assigning new points

For observations $x_i\in\mathbb R^d$, K-means seeks $k$ centroids $\mu_j\in\mathbb R^d$ that minimize

$$
J(\mu_1,\ldots,\mu_k)
=\sum_{i=1}^{n}\min_{1\le j\le k}\|x_i-\mu_j\|_2^2.
$$

Lloyd's algorithm alternates nearest-centroid assignments and replacement of each nonempty cluster's centroid by its members' mean. Empty clusters require implementation-specific handling. Training stops under a convergence criterion or iteration limit; initialization can lead to different local solutions, not a guaranteed global optimum.

For a new point, the fitted model can return

$$
\hat c(x)=\operatorname*{arg\,min}_{1\le j\le k}\|x-\mu_j\|_2^2.
$$

**A cluster index is not a target prediction:** “cluster 2” has no intrinsic class meaning. Also, a centroid is an average, not necessarily an observed training example. [Reference: scikit-learn, K-means](https://scikit-learn.org/stable/modules/clustering.html#k-means).

## What “lazy versus eager” does—and does not—mean

My contrast describes where the main work happens: KNN retains examples for query-time aggregation; K-means iteratively fits centroids beforehand. It does **not** mean KNN has no fitting work, or that K-means cannot process new points. Likewise, neighbor search alone can be unsupervised; “supervised KNN” here specifically means the classifier/regressor that uses $y_i$.

## Connections

- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/K-means|K-means]] — Contrasts labeled-neighbor prediction with centroid-based clustering, including the different meanings of k and of an output label.

## Origin

My supplied handwritten page, right-hand KNN/K-means comparison and two sketches. The comparison and lazy/eager distinction are mine; notation, numerical aggregation examples and qualifications are assistant-added synthesis checked against the linked official documentation. The unchanged original is shared as a source, not a second conceptual attachment.
