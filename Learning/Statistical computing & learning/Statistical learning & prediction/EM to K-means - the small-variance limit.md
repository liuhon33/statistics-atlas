---
id: learning-em-kmeans-small-variance-limit
title: EM to K-means - the small-variance limit
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/K-means]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Unsupervised learning → Clustering & mixtures → K-means
study_band: U–M
note_types: [topic-note, derivation, insight]
question_roles: [cross-topic-connection, assumption-boundary]
source_format: course-slides-and-conversation
created: 2026-11-15
updated: 2026-11-16
status: active
verification: checked
aliases: [K-means as a small-variance limit of GMM EM]
tags: [atlas/learning, subject/computing, topic/em, topic/k-means]
connections:
  - '[[Learning/Statistical computing & learning/Simulation & approximate inference/General EM and Gaussian mixture EM - a side-by-side dictionary]]'
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/Gaussian mixture models]]'
---

# EM to K-means - the small-variance limit

Statistical computing & learning → Statistical learning & prediction → Unsupervised learning → Clustering & mixtures → K-means

**K-means is the hard-assignment limit of a specially constrained GMM EM—not of every GMM.** Make all component covariances equal and spherical, then let their common variance shrink. Away from distance ties, each point's nearest center receives responsibility 1 and the others receive 0 in the limit.

Thibault Randrianarisoa, EM algorithm, University of Toronto, 2026-02-25 (original course PDF retained privately), slide 16

## 1. What does “all clusters have epsilon times I” mean?

For $K\geq2$ components, use the same **fixed covariance** for every component:

$$
\Sigma_k=\epsilon I_D,\qquad \epsilon>0,\qquad k=1,\ldots,K.
$$

Here $I_D$ is the identity matrix: equal variance in every direction and zero cross-coordinate covariance. **$\epsilon$ is the variance; the standard deviation along each coordinate is $\sqrt\epsilon$.** If the standard deviation were called $\epsilon$, the covariance would instead be $\epsilon^2I_D$.

K-means itself does not estimate Gaussian spreads. This is a probabilistic route to its algorithm. For the clean comparison below, also fix equal mixing proportions $\pi_k=1/K$; only the centers are fitted. [Slide 16.]

![[assets/figures/2026-11-15-em-kmeans/responsibility-limit.svg]]

*Original 1-D example: fixed centers $-1,+1$, equal weights. The vertical axis is responsibility for center 1, not a Gaussian density; $r_2=1-r_1$. Only $\epsilon$ changes. The nearest-center boundary stays at 0 while soft probabilities approach the dashed hard assignments. The purple midpoint is a tie, not a hard-limit point.*

## 2. Why do responsibilities become 1 and 0?

The shared Gaussian normalization cancels from the E-step. With $d_{nk}^2=\|x_n-\mu_k\|^2$ and equal weights,

$$
r_{nk}(\epsilon)
=\frac{\pi_k e^{-d_{nk}^2/(2\epsilon)}}{\sum_j\pi_j e^{-d_{nj}^2/(2\epsilon)}}
=\frac{e^{-d_{nk}^2/(2\epsilon)}}{\sum_j e^{-d_{nj}^2/(2\epsilon)}}.
$$

Let $k^*$ be the **unique nearest center**. Divide numerator and denominator by its exponential. Every other squared-distance gap $\Delta_j=d_{nj}^2-d_{nk^*}^2$ is positive, so

$$
r_{nk^*}(\epsilon)
=\frac{1}{1+\sum_{j\ne k^*}e^{-\Delta_j/(2\epsilon)}}
\xrightarrow[\epsilon\downarrow0]{}1,
\qquad
r_{nj}(\epsilon)=r_{nk^*}(\epsilon)e^{-\Delta_j/(2\epsilon)}\longrightarrow0.
$$

**The relative weights matter:** the farther centers' terms vanish relative to the nearest one's. Do not substitute $\epsilon=0$ directly into a Gaussian density. At finite positive $\epsilon$, responsibilities remain strictly between 0 and 1; a displayed 0 or 1 can be rounding.

> [!warning] Exact ties are the exception
> At $x=0$ between centers $-1,+1$, both distances are equal, so responsibilities stay $(0.5,0.5)$ for every positive $\epsilon$. K-means needs a tie-breaking rule. With fixed unequal positive weights, a unique nearest center still wins as $\epsilon\to0$, but tied nearest centers split responsibility in proportion to their weights. The same boundary at finite $\epsilon$ in this figure relies on equal weights.

> [!example]- Numerical example — watch the same point become almost hard-assigned
> Take $\mu_1=-1$, $\mu_2=1$, equal weights and the fixed point $x=-0.2$. Its squared distances are $0.8^2=0.64$ and $1.2^2=1.44$, giving gap $0.8$.
>
> $$
> r_1(\epsilon)=\frac{1}{1+e^{-0.8/(2\epsilon)}}
> =\frac{1}{1+e^{-0.4/\epsilon}},\qquad
> r_2(\epsilon)=\frac{e^{-0.4/\epsilon}}{1+e^{-0.4/\epsilon}}.
> $$
>
> | Variance $\epsilon$ | $r_1$ (nearer center) | $r_2$ (farther center) |
> | --- | --- | --- |
> | $1$ | $0.598688$ | $0.401312$ |
> | $0.25$ | $0.832018$ | $0.167982$ |
> | $0.1$ | $0.982014$ | $0.017986$ |
> | $0.05$ | $0.999665$ | $0.000335$ |
> | $0.01$ | $\approx1-4.25\times10^{-18}$ | $\approx4.25\times10^{-18}$ |
> | Limit $\epsilon\downarrow0$ | $1$ | $0$ |
>
> The point and centers never move in this comparison. At $x=+0.2$, the two columns swap; at the exact midpoint $x=0$, they both remain $0.5$. The last finite row deliberately retains the tiny losing probability instead of rounding it to zero.

## 3. The M-step becomes the K-means center update

For fixed shared covariance and equal fixed weights, the GMM objective is

$$
Q(\mu,\mu^{\mathrm{old}};\epsilon)
=C(\epsilon)-\frac{1}{2\epsilon}\sum_{n,k}r_{nk}^{\mathrm{old}}\|x_n-\mu_k\|^2,
$$

where $C(\epsilon)$ is independent of the candidate centers. Thus maximizing $Q$ minimizes a weighted sum of squared distances. As responsibilities become hard indicators, its update becomes

$$
\mu_k^{\mathrm{new}}
=\frac{\sum_n r_{nk}^{\mathrm{old}}x_n}{\sum_n r_{nk}^{\mathrm{old}}}
\longrightarrow
\frac{1}{|C_k|}\sum_{n\in C_k}x_n,
\qquad C_k=\{n:k\text{ is the nearest old center to }x_n\}.
$$

This assumes unique nearest centers and a nonempty $C_k$; empty clusters need a separate rule. Together, **nearest-center assignment + arithmetic-mean update** are Lloyd's K-means iteration. [Slide 17.]

| Constrained GMM EM, finite $\epsilon$ | K-means |
| --- | --- |
| Soft responsibility for every component | One assigned cluster per point |
| Responsibility-weighted center update | Mean of assigned points |
| Probabilistic model with a fixed shared spread here | Squared-distance clustering; no fitted covariance |

Unrestricted GMM EM can learn unequal/elliptical covariances, so it need not give K-means assignments. Neither method is guaranteed to find a global optimum.

## Connections

- [[Learning/Statistical computing & learning/Simulation & approximate inference/General EM and Gaussian mixture EM - a side-by-side dictionary|General EM and Gaussian mixture EM]] — Starts from its responsibility and weighted-mean formulas, then specializes the covariance and takes the small-variance limit.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Clustering & mixtures/Gaussian mixture models|Gaussian mixture models]] — The equal spherical-covariance model supplies the probabilistic route to hard nearest-center clustering.

## Origin

> [!info]- Source details
> **Source:** Thibault Randrianarisoa, University of Toronto, *EM algorithm*, February 25, 2026, slides 16–17 of the preserved `PML_Lec07.pdf`; both pages read as text and visually inspected. New coverage is limited to these two slides. The user requested a separate small note, the $\epsilon\to0$ explanation, a foldable numerical example and a graph. The derivation details, numeric example, original figure, covariance/standard-deviation distinction and tie qualifications are assistant-added synthesis, not user-authored work or recovered lecture data.
>
> **Slide notation correction:** slide 16 uses $\Sigma_k=\epsilon I$, so its Gaussian quadratic coefficient is $1/(2\epsilon)$. Slide 17 prints $1/(2\epsilon^2)$; this is inconsistent with slide 16 and would instead match $\Sigma_k=\epsilon^2I$. This note uses $1/(2\epsilon)$ consistently. The hard-assignment conclusion is unchanged. The lecture's broad accuracy comparison is not treated as a universal guarantee.
>
> **Checks and reproducibility:** [[assets/figures/2026-11-15-em-kmeans/draw_limit.py|figure generator]], [[assets/figures/2026-11-15-em-kmeans/example-values.json|constructed inputs and table]], [[assets/figures/2026-11-15-em-kmeans/checks.json|numerical checks and hashes]]. Checked normalization, independent Gaussian-density ratios, the 1-D logistic form, unique-nearest limits and equal/unequal-weight ties; numerical agreement supports the analytic proof. Original SVG and rendered PNG inspected; no live Obsidian rendering claim.
>
> **Privacy:** the original PDF remains Git-ignored and unchanged. The note and original generated figure may be tracked; public exports must omit the private PDF and replace its local link/source entry with plain lecture attribution. No publication or commit occurred.
