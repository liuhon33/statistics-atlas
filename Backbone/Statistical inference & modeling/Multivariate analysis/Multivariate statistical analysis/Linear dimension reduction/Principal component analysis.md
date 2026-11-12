---
id: pca
title: Principal component analysis
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Multivariate analysis → Multivariate statistical analysis → Linear dimension reduction → Principal component analysis
created: '2026-11-08'
updated: '2026-11-11'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Linear dimension reduction]]'
related:
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/mining]]'
- '[[assets/figures/2026-11-11-pca/draw_pca.py]]'
- '[[assets/figures/2026-11-11-pca/checks.json]]'
---

# Principal component analysis

Statistical inference & modeling → Multivariate analysis → Multivariate statistical analysis → Linear dimension reduction → Principal component analysis

Parent: [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Linear dimension reduction|Linear dimension reduction]]

## 1. See it and use it

Suppose two instruments measure related properties of twelve samples. Plotting both readings gives the blue points below. Most variation follows one diagonal: one coordinate along that line can summarize both readings.

![[assets/figures/2026-11-11-pca/01-projection.svg]]

*Original illustration. Each point is one sample; both measurements use the same units. Means have been subtracted. Orange points are perpendicular projections, and gray segments show what reconstruction loses.*

**Principal component analysis (PCA)** constructs orthogonal linear combinations of centered features, ordered by the variation they capture. Keeping the first few combinations gives fewer numbers per sample. [Stanford STATS 305C, “Maximal variance” and “PCA = SVD”](https://web.stanford.edu/class/stats305c/slides/PCA_I.html).

Here the first combination is `PC1 = (centered A + centered B) / √2`. A sample with centered readings $(2,2)$ gets score $2\sqrt2\approx2.83$. The twelve samples retain **93.8% of total variance** using one score each.

Use PCA to compress correlated measurements, make a first plot, or supply fewer inputs to another method. High variance need not mean biological importance or predictive usefulness. Feature units matter: rescaling a measurement can change the chosen direction.

> [!example]- How to read PCA results — the common plots
> **Read in this order: how much is kept → where the samples sit → which features explain those positions.** A *score* is a sample's new coordinate; a *loading* describes a feature's role in that coordinate. The next fold explains those words with a tiny calculation.
>
> **1. Scree, explained-variance, and cumulative-variance plots: how much is kept?**
>
> ![[assets/figures/2026-11-11-pca/06-variance-reading.svg]]
>
> *A separate, constructed four-feature example, not the two-instrument data above. Each feature has sample variance 1. Its PC variances are 2.4, 1, 0.4, and 0.2; total variance is 4.*
>
> | Plot | What the axes mean | How to read this example |
> | --- | --- | --- |
> | **Scree plot** | PC number versus that PC's variance (its eigenvalue). | Look for a bend followed by small gains. Here the first two PCs carry most of the spread; an elbow is a visual guide, not a definitive dimension test. |
> | **Explained-variance plot** | PC number versus its percentage of **total** variance. | PC1 keeps 60%; PC2 adds 25%. PC2 does **not** keep 25% of the remaining 40%. |
> | **Cumulative-variance plot** | Number of PCs kept versus their combined percentage. | Two keep 85%; three keep 95%. A chosen 90% target needs three, not two. |
>
> Scree and individual explained-variance plots show the same spectrum on different vertical scales; some software calls either a scree plot. Check the axis label. “Variance explained” means **spread represented**, not prediction accuracy, percentage of samples classified correctly, or a causal explanation. No universal 90% cutoff suits every task. [Minitab, Eigenvalue, Proportion, Cumulative, and Scree plot](https://support.minitab.com/en-us/minitab/help-and-how-to/statistical-modeling/multivariate/how-to/principal-components/interpret-the-results/all-statistics-and-graphs/).
>
> **2. Score scatter plot: which samples look similar?**
>
> ![[assets/figures/2026-11-11-pca/07-scores-biplot-reading.svg]]
>
> *Back to the original twelve samples. Left: sample scores. Right: the same scores with feature arrows. Both axes use equal physical spacing per score unit. The biplot arrows are coefficient loadings enlarged threefold for visibility; this is not a correlation biplot.*
>
> Each dot is one sample; its horizontal and vertical coordinates are its PC1 and PC2 scores. Here **right** means larger combined centered A and B; **up** means more centered A relative to centered B. The green sample has coordinates $(6,1)$, not original measurements $(6,1)$.
>
> - **Nearby dots:** similar on the *displayed* components. With omitted PCs, two overlapping dots can still differ elsewhere. Ordinary unwhitened score distances are distances after projection; a 2D view can shrink full-data distances.
> - **Far from the origin:** unusual on these displayed directions, not automatically a bad observation. Near the origin does not rule out unusual omitted coordinates.
> - **Groups or gradients:** possible structure to investigate. Color by known labels or batch to see what aligns with it; PCA did not use those labels merely because you colored the plot. Separation is not a significance test; overlap is not proof of no group difference.
> - **Read the axis percentages.** “PC1 60%, PC2 25%” means this view keeps 85% of total variance. It does not guarantee that every sample, feature, or group difference is well represented.
>
> Here there are only two features and both PCs are shown: together they keep 100%. The projection/rotation algebra in §§2–3 explains the distance statements. Whitening or separate axis rescaling changes the geometry; do not compare screen distances as if nothing changed. [scikit-learn PCA, `whiten`](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
>
> **3. Biplot: what features go with a sample's position?**
>
> Read the right-hand panel in three passes:
> 1. **Dots = samples; arrows = features.** A right-pointing A arrow says the positive PC1 direction reconstructs higher centered A. The upward part says positive PC2 also adds to A.
> 2. **Read a sample along an arrow's direction**, using its perpendicular projection onto the arrow's line. Farther in the arrow's positive direction means a larger reconstructed value for that feature; the opposite direction means smaller. The dashed segment shows this for A. It is **not** “which arrow tip is the sample closest to?”
> 3. **Check the scaling before reading lengths, angles, or numbers.** Here arrows are $3V$ while dots are ordinary scores. Other biplots redistribute the PC scales between dots and arrows. Neither their distance rules nor their arrow-angle rules are interchangeable. Exact values require the declared scaling and, when PCs are omitted, are only reconstructions. [R `biplot`, Arguments and Details](https://stat.ethz.ch/R-manual/R-patched/library/stats/html/biplot.princomp.html).
>
> **4. Loading bars/heatmaps versus a correlation circle: what does each PC mean?**
>
> A **loading bar plot** compares feature weights within one PC. A **loading heatmap** puts features in rows and PCs in columns: color gives the sign and strength of the weight. Look for a common pattern (same signs) or a contrast (opposite signs), then give the PC a cautious descriptive name. PC1 here is a “shared A-and-B” direction; PC2 is an “A-versus-B” direction. A large negative weight matters just as much as an equally large positive one.
>
> ![[assets/figures/2026-11-11-pca/08-loading-correlation-reading.svg]]
>
> *Same data, two meanings of a loading plot. Left: coefficients in the PC recipes. Right: correlations between each feature and each PC. The arrows change because these are different quantities, not different PCA fits.*
>
> In a **correlation circle**, coordinates are feature–PC correlations, between −1 and 1:
> - An arrow near the circle's edge means the displayed PCs represent that feature well; a short arrow means much of its variation lies in other PCs. Short does not mean useless.
> - With equal axis scales and **both features well represented**, a small angle suggests positive correlation, opposite arrows negative correlation, and about $90^\circ$ little linear correlation. With short arrows, these 2D angle readings can be misleading.
> - Do **not** apply that rule to raw coefficient arrows. In the left panel A and B are perpendicular, although their actual correlation is $85/97\approx0.876$! The correlation-circle arrows correctly show their strong positive association. The algebra in §3 explains why.
>
> **5. Contribution and quality-of-representation plots: two different questions**
>
> | Plot or coloring | Plain-language question | Interpretation |
> | --- | --- | --- |
> | **Variable contribution** to a PC | Which features build this axis? | For ordinary PCA with unit loading columns, the contribution is $100v_{jk}^2$ percent. Contributions over features sum to 100% for that PC; squaring hides the sign. A and B each contribute 50% to PC1 here. |
> | **Variable cos² / quality** on a PC plane | How much of *this feature* is visible here? | Add its squared feature–PC correlations on the displayed axes. Near 1 is well represented; near 0 is mostly hidden. A and B each have quality 1 on this full two-PC plane. |
> | **Sample cos² / quality** on a PC plane | How much of *this sample's departure from the mean* is visible here? | Compare its squared displayed score length with its full centered squared length. A low-quality sample needs other PCs before interpreting its apparent neighbors. The ratio is undefined for a sample exactly at the overall mean. |
>
> **Contribution asks who builds a PC; quality asks who is well pictured by it.** Check whether a plot describes variables or samples. These are separately reported quantities, not alternative names for loadings. [FactoMineR manual, PCA, pp. 43–44](https://cran.r-project.org/web/packages/FactoMineR/FactoMineR.pdf#page=43).
>
> **6. Other common views and diagnostics**
>
> - **PC scatterplot matrix / 3D scores:** inspect PC1–PC3 or PC2–PC3 when PC1–PC2 may hide structure. Keep the same fitted PCA when comparing samples or groups.
> - **Score histograms, boxplots, or score-versus-time plots:** show one PC's distribution, group shifts, or drift. They do not say which original features changed; consult loadings too.
> - **Ellipses around score groups:** read the caption. A data-spread ellipse and a confidence region for a mean answer different questions; overlap alone is not a formal test.
> - **Distance / Hotelling $T^2$ plots:** flag unusual score positions relative to the components' spreads. **Residual / Q / squared prediction error plots:** flag samples whose original measurements are poorly reconstructed by the retained PCs. A sample can be ordinary in the displayed score plot but have a large residual. Cutoffs need stated assumptions; flags call for investigation, not automatic deletion. [MathWorks, PCA: Hotelling's T-squared](https://www.mathworks.com/help/stats/pca.html); [PCA residuals and reconstruction](https://www.mathworks.com/help/stats/pcares.html).
>
> **A useful result sentence:** “After [centering/scaling], PC1 and PC2 retain [x%] of variance. PC1 mainly contrasts [features]. [Samples/groups] differ along that pattern. This 2D view leaves [100−x%] outside the plot and does not by itself establish a biological mechanism or a significant difference.”

> [!example]- Loadings and scores — the recipe and each sample's result
> **A loading is part of the recipe. A score is the answer after you put one sample into that recipe.** One fitted recipe is shared by every sample; the answers differ because their measurements differ.
>
> ![[assets/figures/2026-11-11-pca/04-scores-loadings.svg]]
>
> *The existing example: two feature weights on the left, twelve samples' PC1 scores on the right. A feature is not a sample; these two plots index different things.*
>
> Let $A_c=A-\bar A$ and $B_c=B-\bar B$: each reading minus that instrument's mean. Our two recipes are
>
> $$
> \text{PC1 score}=\underbrace{0.707}_{\text{A loading}}A_c+
> \underbrace{0.707}_{\text{B loading}}B_c,\qquad
> \text{PC2 score}=0.707A_c-0.707B_c.
> $$
>
> Here $0.707$ is rounded from $1/\sqrt2$. The exact weights make each direction have length 1.
>
> | Sample's centered readings | PC1 score | PC2 score | Plain-language reading |
> | --- | --- | --- | --- |
> | $(2,2)$ | $2.83$ | $0$ | Both readings are above their means; no A-versus-B contrast. |
> | $(-2,-2)$ | $-2.83$ | $0$ | Both readings are below their means; the opposite end of PC1. |
> | $(2,-2)$ | $0$ | $2.83$ | The sum cancels, but A is above its mean and B below: a strong PC2 contrast. |
>
> These are illustrative inputs to the fitted recipes, not three extra observations used to refit PCA.
>
> **Reading loadings:** a positive weight of a PC adds to that PC's score when that centered feature rises; a negative weight subtracts. A larger absolute weight changes the score more for a one-unit change in that feature, holding the others fixed. It is not a causal effect or universal feature-importance score. Comparing weights is easiest when features have comparable scales; if PCA used standardized measurements, apply the recipe to those standardized values.
>
> **Reading scores:** positive and negative mean opposite ends of a PC, and not necessarily positive and negative raw measurements. A score of zero means “at the center along this direction": the third row makes that distinction visible. A high PC1 score here summarizes the combined pattern; it does not force every original feature to be high. [R `prcomp`, Value: `rotation` and `x`](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prcomp.html).
>
> **Count the entries:** with 100 samples, 5 features, and 2 retained PCs, the loading table is $5\times2$ (two recipes), while the score table is $100\times2$ (two answers per sample). Python's `components_` stores the recipes transposed; `components_.T` matches the loading table here. A score of 2 on PC1 need not be as unusual as 2 on PC2, because the PCs have different spreads.
>
> **Signs can flip harmlessly.** Negate one entire recipe and every corresponding score: the axis reverses, but similarities and reconstructed data do not change. Never compare signs between fits before aligning this convention. Also check whether a source uses “loadings” for recipe coefficients or feature–PC correlations; the plot comparison above shows why the distinction matters.
>
> **Later, SVD gives these same objects mathematical names:** $V$ holds the recipes, $T=X_cV=UD$ holds the sample scores, and $D$ sets each PC's spread. **$U$ alone is not the ordinary score table.** See [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Principal component analysis#SVD — the same directions, with a different scale|the SVD explanation in §3]] for the derivation, and [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/PCA scores and loadings|PCA scores and loadings]] for the short companion reference.

> [!example]- Try the rotating 2D graph
> ```atlas-interactive
> path: assets/figures/2026-11-11-pca/explorer.html
> title: PCA - find the most useful line
> height: 800
> ```
>
> Start with **Horizontal**, then choose **Best line: PC1**. Watch the retained spread increase as the reconstruction error decreases. [[assets/figures/2026-11-11-pca/explorer.html|Open the standalone explorer]].

> [!example]- Python — scikit-learn, using the plotted example
> Rows are samples; columns are features. `PCA` centers columns but does not standardize them. This example intentionally keeps the original common measurement scale.
>
> ```python
> import numpy as np
> from sklearn.decomposition import PCA
>
> a = np.r_[np.arange(-6, 0), np.arange(1, 7)]
> b = np.array([1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1])
> X = np.column_stack((a + b, a - b)) / np.sqrt(2) + [10, 20]
>
> pca = PCA(n_components=1, svd_solver="full")
> scores = pca.fit_transform(X)           # (12, 1): one score per sample
> loadings = pca.components_.T           # (2, 1): feature weights
> X_hat = pca.inverse_transform(scores)  # (12, 2): approximate readings
>
> print(pca.explained_variance_ratio_)   # [0.93814433]
> print(pca.explained_variance_)         # [16.54545455]
> print(np.sum((X - X_hat) ** 2))        # approximately 12
> ```
>
> If equal weighting across different units is intended, fit a `StandardScaler` before PCA. That changes the question to variance on the standardized scale. For prediction, fit **both** preprocessing and PCA on training data only, then transform held-out data using the fitted objects. [PCA API, parameters and attributes](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).

> [!example]- R — prcomp, using the same example
> `rotation` contains feature weights; `x` contains sample scores; `sdev^2` contains covariance eigenvalues.
>
> ```r
> a <- c(-6:-1, 1:6)
> b <- c(1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1)
> X <- sweep(cbind(a + b, a - b) / sqrt(2), 2, c(10, 20), "+")
>
> fit <- prcomp(X, center = TRUE, scale. = FALSE)
> scores <- fit$x[, 1, drop = FALSE]
> loadings <- fit$rotation[, 1, drop = FALSE]
> X_hat <- sweep(scores %*% t(loadings), 2, fit$center, "+")
>
> fit$sdev[1]^2 / sum(fit$sdev^2)        # 0.9381443
> fit$sdev[1]^2                         # 16.54545
> sum((X - X_hat)^2)                    # approximately 12
> ```
>
> Use `scale. = TRUE` when unit-variance feature scaling is appropriate; remove or otherwise handle constant columns first. Signs may differ between R and Python: flipping a score column **and** its loading column leaves reconstruction unchanged. [R stats, `prcomp`: Details and Value](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prcomp.html).

## 2. How it works

### A little deeper — keep variation, lose as little as possible

The orange dot represents a sample using one number. To get back to the original coordinates, place that number along the chosen line. The gray segment is the reconstruction error. The insight in [amoeba's visual explanation on Cross Validated](https://stats.stackexchange.com/a/140579) is that **maximizing projected variation and minimizing squared reconstruction error are the same choice**. The reason is perpendicularity.

Let $X\in\mathbb R^{n\times p}$ contain $n>1$ observations in rows and $p$ numeric features in columns. Write $\bar x\in\mathbb R^p$ for the column means, $\mathbf1$ for the length-$n$ all-ones vector, and

$$
X_c=X-\mathbf1\bar x^\top,\qquad C=\frac{X_c^\top X_c}{n-1}.
$$

$C$ is the sample covariance matrix. These finite-data calculations require no Gaussian model. Missing values need a separate treatment; assume finite complete entries and positive total variance here.

For a **unit** direction $v\in\mathbb R^p$, the score vector is $t=X_cv\in\mathbb R^n$, and reconstruction is $\widehat X_c=tv^\top=X_cvv^\top$. The unit-length constraint prevents artificially increasing variance by multiplying the weights by a large constant. [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|Orthogonal projection]] supplies the right-angle identity, row by row:

$$
\underbrace{\|X_c\|_F^2}_{\text{fixed total squared length}}
=\underbrace{\|X_cv\|_2^2}_{\text{retained squared length}}
+\underbrace{\|X_c-X_cvv^\top\|_F^2}_{\text{squared reconstruction error}}.
$$

$\|A\|_F^2$ means the sum of squares of all matrix entries. Because $t$ has mean zero, its sample variance is $\|t\|_2^2/(n-1)$. Divide the whole identity by $n-1$: more retained variance means exactly less normalized error. The criterion uses **squared** perpendicular distances.

![[assets/figures/2026-11-11-pca/02-variance-error.svg]]

*Original analytic plot for the same twelve samples. The sum is $194/11$. At $45^\circ$, PC1 retains $182/11$ and discards $12/11$; at $135^\circ$, these exchange roles.*

### Matrix algebra — why the optimal direction is an eigenvector

First turn “spread of the projected points” into a matrix expression:

$$
\operatorname{var}_{\rm sample}(t)
=\frac{t^\top t}{n-1}
=\frac{(X_cv)^\top(X_cv)}{n-1}
=v^\top Cv.
$$

So PC1 solves $\max_{v^\top v=1}v^\top Cv$. Introduce a multiplier $\lambda$ for the unit-length constraint:

$$
\mathcal L(v,\lambda)=v^\top Cv-\lambda(v^\top v-1),\qquad
\nabla_v\mathcal L=2Cv-2\lambda v=0.
$$

Thus a stationary direction satisfies $Cv=\lambda v$: precisely the [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors|eigenvector equation]]. Multiplying on the left by $v^\top$ shows that $\lambda=v^\top Cv$, the score variance in that direction.

**Why take the largest eigenvalue?** A covariance matrix is symmetric and positive semidefinite: $w^\top Cw=\|X_cw\|^2/(n-1)\ge0$. It has an orthonormal eigenbasis $v_1,\ldots,v_p$ with $\lambda_1\ge\cdots\ge\lambda_p\ge0$. Expand any unit direction as $v=\sum_j c_jv_j$, where $\sum_jc_j^2=1$. Then

$$
v^\top Cv=\sum_j\lambda_jc_j^2\le\lambda_1\sum_jc_j^2=\lambda_1.
$$

Choosing $v_1$ attains the bound. Requiring the next direction to be perpendicular to $v_1$ removes $c_1$ and gives $v_2$, and so on. This proves the maximum, beyond merely finding stationary points. [Stanford, “Maximal variance”; Illinois CS 357, “Diagonalization of the Covariance Matrix”](https://cs357.cs.illinois.edu/textbook/notes/pca.html).

For our example:

$$
C=\frac1{11}\begin{pmatrix}97&85\\85&97\end{pmatrix},\quad
v_1=\frac1{\sqrt2}\binom11,\quad
v_2=\frac1{\sqrt2}\binom1{-1},\quad
\lambda_1=\frac{182}{11},\quad\lambda_2=\frac{12}{11}.
$$

The off-diagonal $85/11$ records shared variation. In PC coordinates,

$$
\operatorname{Cov}_{\rm sample}(X_cV)=V^\top CV
=\operatorname{diag}(\lambda_1,\ldots,\lambda_p),
$$

where $V=[v_1,\ldots,v_p]$. Scores are **uncorrelated**. Independence requires additional distributional conditions, such as joint Gaussianity. The Illinois page's informal “independent” wording should be read with this correction.

## 3. Deeper understanding and connections

### SVD — the same directions, with a different scale

[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|SVD]] already gives a way to split a matrix into orthogonal patterns. Apply its compact form to **centered data**, with $r=\operatorname{rank}(X_c)$:

$$
\underbrace{X_c}_{n\times p}
=\underbrace{U_r}_{n\times r}
\underbrace{D_r}_{r\times r}
\underbrace{V_r^\top}_{r\times p},
\qquad U_r^\top U_r=V_r^\top V_r=I_r.
$$

$D_r=\operatorname{diag}(d_1,\ldots,d_r)$ contains positive singular values in decreasing order. Substitute, keeping the cancellation visible:

$$
\begin{aligned}
C
&=\frac{(U_rD_rV_r^\top)^\top(U_rD_rV_r^\top)}{n-1}\\
&=\frac{V_rD_r\underbrace{U_r^\top U_r}_{I_r}D_rV_r^\top}{n-1}\\
&=V_r\operatorname{diag}\!\left(\frac{d_1^2}{n-1},\ldots,
\frac{d_r^2}{n-1}\right)V_r^\top.
\end{aligned}
$$

Therefore

$$
\boxed{\lambda_j(C)=\frac{d_j(X_c)^2}{n-1}},\qquad
\boxed{T=X_cV_r=U_rD_r}.
$$

Right singular vectors are feature directions; $U_rD_r$ contains actual scores; columns of $U_r$ alone have unit length. This is the distinction developed in [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/PCA scores and loadings|PCA scores and loadings]]. If $r<p$, the remaining covariance eigenvalues are zero. Centering implies $r\le\min(n-1,p)$.

**Return to the recipe and result in §1.** For sample $i$ and PC $k$,

$$
\underbrace{t_{ik}}_{\text{one sample's score}}
=\sum_{j=1}^{p}\underbrace{(x_{ij}-\bar x_j)}_{\text{centered feature}}
\underbrace{v_{jk}}_{\text{recipe weight}}
=\underbrace{u_{ik}d_k}_{\text{SVD's same answer}}.
$$

Thus a **column of $V_r$** is one feature recipe; a **row of $T$** is one sample's new coordinates. Multiplying $u_k$ by $d_k$ restores the score column's actual scale. Its squared length is $d_k^2$, so its sample variance is $d_k^2/(n-1)$. These are the same quantities shown in the score, scree, and variance plots—not separate PCA results. This discussion uses ordinary, unwhitened scores. [Stanford STATS 305C, “Back to reduced rank” and “PCA = SVD”](https://web.stanford.edu/class/stats305c/slides/PCA_I.html).

![[assets/figures/2026-11-11-pca/03-svd-pieces.svg]]

*Original decomposition of the same $12\times2$ data matrix. Every panel uses the same color scale, from −5 (blue) to +5 (red). The two component matrices add entry by entry to the original; keeping the middle panel gives the rank-one reconstruction.*

Here $d_1=\sqrt{182}$ and $d_2=\sqrt{12}$: singular values are **not** covariance eigenvalues. Squaring converts a length into a sum of squares; dividing by $11$ converts that sum into sample variance. The ratios agree because the common divisor cancels:

$$
\frac{\lambda_1}{\sum_j\lambda_j}
=\frac{d_1^2}{\sum_jd_j^2}
=\frac{182}{194}\approx0.9381.
$$

Using divisor $n$ instead changes eigenvalues to $d_j^2/n$, but leaves directions and variance ratios unchanged. Direct SVD also avoids explicitly forming the Gram matrix $X_c^\top X_c$. [Stanford, “Relation to SVD” and “PCA = SVD”](https://web.stanford.edu/class/stats305c/slides/PCA_I.html); [R `prcomp`, Details](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prcomp.html).

#### Why a biplot and a correlation circle use different arrows

For $k$ retained PCs, the reconstruction identity reads entry by entry:

$$
\widehat x_{c,ij}=\sum_{\ell=1}^k t_{i\ell}v_{j\ell}
=(\text{sample }i\text{'s score point})^\top
(\text{feature }j\text{'s coefficient arrow}).
$$

This **dot product**, not distance to an arrow tip, explains the biplot reading. It equals the original centered value when all nonzero PCs are kept. If arrows are drawn as $3v_j$, as in §1, divide the displayed dot product by 3. With fewer PCs, the result is a reconstructed value. If PCA used standardized features, undo that scaling before adding the original mean.

For a nonconstant feature $j$ with sample standard deviation $s_j$, and a positive-variance PC $k$, the eigenvector equation gives

$$
\begin{aligned}
\operatorname{Cov}(X_{c,\cdot j},t_k)
&=(Cv_k)_j=\lambda_kv_{jk},\\
L_{jk}:=\operatorname{Corr}(X_{c,\cdot j},t_k)
&=\frac{\lambda_kv_{jk}}{s_j\sqrt{\lambda_k}}
=\frac{v_{jk}\sqrt{\lambda_k}}{s_j}
=\frac{v_{jk}d_k}{s_j\sqrt{n-1}}.
\end{aligned}
$$

So **coefficient loadings are $V$; correlation loadings are $L$**, with an extra PC-scale and feature-scale adjustment. For sample-standardized input, $s_j=1$. Here A and B have coefficient arrows $(1/\sqrt2,\pm1/\sqrt2)$ but correlation arrows $(\sqrt{91/97},\pm\sqrt{6/97})$.

Writing $S=\operatorname{diag}(s_1,\ldots,s_p)$, the full feature correlation matrix is

$$
R=S^{-1}CS^{-1}=LL^\top.
$$

With all nonzero PCs, every row of $L$ has length 1, so its dot product with another row is exactly their cosine and feature correlation. With only two PCs, arrow length squared is the feature's displayed **cos² quality**, and the dot product omits other PCs' contributions. Only when both arrows retain nearly all their length does the 2D cosine reliably approximate the full correlation. This derives the circle/angle cautions above; angles between rows of $V$ do not obey the same rule.

### Dimension reduction — rotation first, truncation second

Keeping all $p$ coordinates of a full orthogonal $V$ only changes basis: $X_cV$ preserves Euclidean distances and reconstructs $X_c$ exactly. **Dimension reduction happens when we keep only $k<p$ coordinates.**

$$
\underbrace{T_k=X_cV_k}_{n\times k\ \text{reduced data}},\qquad
\underbrace{\widehat X=\mathbf1\bar x^\top+T_kV_k^\top}_{n\times p\ \text{reconstruction}}.
$$

For $k<r$, the discarded squared error is $\sum_{j=k+1}^r d_j^2$. The [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition#Rank-one pieces and the best low-rank approximation|Eckart–Young–Mirsky result]] makes this the best rank-$k$ approximation in Frobenius norm. A tied eigenvalue can make the chosen directions nonunique; signs are arbitrary even without ties.

This connects several ideas:

- **Projection and regression.** PCA fits a subspace in *feature space*, treating every coordinate symmetrically and measuring perpendicular error. [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Least squares geometry|Ordinary least squares]] fixes predictors and minimizes response residuals. Both use projections, with different spaces and objectives.
- **Preprocessing and generalization.** Centering changes the origin; feature standardization changes the distance metric. Retaining high-variance components is a restriction on the representation, related to [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|regularization]], but low-variance directions can carry predictive signal. Choose predictive preprocessing within [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Validation & model selection/Cross-validation|cross-validation]].
- **Nonlinear alternatives.** A curved set may require more linear coordinates than its intrinsic dimension. [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/Nonlinear manifold overview|Manifold learning]] motivates other objectives. [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/PCA versus visualization embeddings|PCA versus visualization embeddings]] compares PCA's linear reconstruction with t-SNE's pair similarities and UMAP's neighbor graph. An [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Autoencoders|autoencoder]] instead learns an encoder and decoder from a reconstruction objective.

In RNA-seq, PCA may reduce 3,000 gene features to 50 scores before a nonlinear method makes a 2D display. These are two reductions with different purposes; choosing a plotting method does not replace deciding which biological structure matters.

## Origin

> [!info]- Source details
> Enriched at the user's 2026-11-11 request: visual introduction, collapsible Python/R examples, variance/reconstruction equivalence, eigenvector proof, SVD connection, and dimension-reduction context. The staged motivation takes inspiration from [amoeba's answer](https://stats.stackexchange.com/a/140579); all toy data, wording, diagrams, interactive code and displayed derivation steps here are original Codex additions, checked against the cited primary teaching/API sources and the existing SVD page.
>
> [[assets/figures/2026-11-11-pca/draw_pca.py|Figure generator]] and [[assets/figures/2026-11-11-pca/checks.json|numerical checks]] verify covariance, eigenpairs, squared singular values, score covariance, reconstruction error and the projection identity. [[assets/figures/2026-11-11-pca/verify_examples.py|The example checks]] execute both language snippets and independently verify the interactive formulas. Static figures and browser controls were inspected. The explorer also executed in the running Obsidian renderer at widths 760 and 420; this offscreen check does not constitute visual inspection of the entire note in the active pane.
>
> The requested interpretation follow-up adds two initially collapsed regions in §1: common PCA plots, and the loading-recipe/score-result distinction, with an explicit return to these meanings in §3's SVD algebra. Three additional original figures and a reused loading/score figure were inspected as PNG previews. [[assets/figures/2026-11-11-pca/draw_interpretation.py|Interpretation figure generator]], [[assets/figures/2026-11-11-pca/interpretation-data.json|constructed data]], and [[assets/figures/2026-11-11-pca/interpretation-checks.json|numerical checks]] reproduce the plot scales, sample calculations, correlation circle, contribution/quality distinctions, and SVD/reconstruction identities. The four-feature variance spectrum is explicitly separate from the original two-feature example. The added algebra is checked synthesis; plot terminology was checked against the cited primary course and software documentation. This follow-up does not claim a new live-Obsidian visual inspection.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|Singular value decomposition]] — PCA can be computed using an SVD of an appropriately centered data matrix.

```atlas
```
