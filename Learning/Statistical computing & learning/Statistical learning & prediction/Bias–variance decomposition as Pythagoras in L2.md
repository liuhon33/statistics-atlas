---
id: learning-bias-variance-pythagoras-l2
title: Bias–variance decomposition as Pythagoras in L2
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Bias–variance tradeoff]]"
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Risk, fit & generalization → Bias–variance tradeoff
study_band: U–M
note_types:
  - derivation
  - insight
source_format: handwriting
created: 2026-11-08
updated: '2026-11-12'
status: active
verification: checked
learning_state: unknown
aliases:
  - Bias–variance decomposition in L2
  - Pythagorean bias–variance decomposition
  - MSE as squared distance in L2
tags:
  - atlas/learning
  - subject/computing
  - topic/bias-variance
connections:
  - "[[Backbone/Statistical inference & modeling/Inference foundations/Statistical reasoning/Sampling distributions/Mean squared error]]"
  - "[[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2]]"
  - "[[Learning/Statistical computing & learning/Statistical learning & prediction/KNN versus K-means - neighbors predict, centroids cluster]]"
sources:
  - "[[raw/assets/2026-11-08-bias-variance-I01-hilbert-geometry-and-MSE-proof.png]]"
  - "[[assets/figures/2026-11-12-bias-variance-projection/01-l2-projections.svg]]"
  - "[[assets/figures/2026-11-12-bias-variance-projection/02-electricity-knn-tradeoff.svg]]"
  - "[[assets/figures/2026-11-12-bias-variance-projection/build.py]]"
  - "[[assets/figures/2026-11-12-bias-variance-projection/checks.json]]"
  - "https://web.stanford.edu/class/stats202/notes/Linear-regression/K-nearest-neighbors.html"
---

# Bias–variance decomposition as Pythagoras in L2

Statistical computing & learning → Statistical learning & prediction → Learning objectives & evaluation → Risk, fit & generalization → Bias–variance tradeoff

**The bias–variance decomposition is Pythagoras' theorem in the space of square-integrable random variables.** At a fixed input $x$, the prediction error $Y-\hat f(x;D)$ splits into three mutually orthogonal vectors: noise, bias and the estimator's fluctuation. The MSE is the squared length of the error, so

$$
\underbrace{\mathbb E\big[(Y-\hat f)^2\big]}_{\|Y-\hat f\|^2}
=\underbrace{\sigma^2}_{\|\varepsilon\|^2}
+\underbrace{\mathrm{Bias}^2(\hat f)}_{\|f(x)-\mathbb E_D\hat f\|^2}
+\underbrace{\mathrm{Var}(\hat f)}_{\|\hat f-\mathbb E_D\hat f\|^2}.
$$

The cross terms that the algebraic proof has to show are zero are exactly the inner products of these orthogonal pieces.

![[raw/assets/2026-11-08-bias-variance-I01-hilbert-geometry-and-MSE-proof.png]]

*My page, 2026-11-08: the model, definitions and $L^2$ diagram (left), random variables as vectors in $L^2$ (middle), the formal MSE proof and the Pythagoras lemma (right). The original is unchanged; corrections are in the text below.*

## Setup

Take the regression model $Y=f(x)+\varepsilon$ with $\mathbb E[\varepsilon]=0$ and $\mathrm{Var}(\varepsilon)=\sigma^2$, the irreducible error. The goal is to estimate $f$ from training data $D=\{(x_i,Y_i)\}_{i=1}^n$ with an estimator $\hat f(x;D)$. Treat $(x,Y)$ as a new data point: $x$ is fixed, and the new noise $\varepsilon$ is independent of $D$. My page writes this as $\varepsilon\perp D$; there $\perp$ means independence, while everywhere else in the note it means orthogonality.

My definitions:

$$
\mathrm{MSE}(\hat f):=\mathbb E_{Y,D}\big[(Y-\hat f(x;D))^2\big],\qquad
\mathrm{Var}(\hat f):=\mathrm{Var}_D\big[\hat f(x;D)\big],
$$

$$
\mathrm{Bias}(\hat f):=\mathbb E_{Y,D}\big[Y-\hat f(x;D)\big]
=\mathbb E[f(x)]+\mathbb E[\varepsilon]-\mathbb E_D\big[\hat f(x;D)\big]
=f(x)-\mathbb E_D\big[\hat f(x;D)\big].
$$

The MSE is an expectation, so it is the *expected* prediction error at $x$ (my page says "estimated"); ISL §2.2.2 calls it the expected test MSE at $x_0$. Bias is usually defined with the opposite sign, $\mathbb E_D\hat f-f(x)$; the square is the same. Assume $\mathbb E[Y^2]<\infty$ and $\mathbb E_D[\hat f(x;D)^2]<\infty$, so every term below is finite.

## 1. Random variables are vectors

A random variable is a deterministic function $X:\Omega\to\mathbb R$, a measurement device that reads off a number $X(\omega)$ for each outcome $\omega$. For any set $\Omega$, the real-valued functions on $\Omega$ form a real vector space, and the measurable ones form a subspace. Keeping those with a finite second moment gives

$$
\mathcal H=L^2(\Omega,\mathcal F,P)=\{X:\Omega\to\mathbb R\ \text{a random variable}:\ \mathbb E[X^2]<\infty\},
$$

$$
\langle X,Y\rangle=\mathbb E[XY],\qquad \|X\|=\sqrt{\mathbb E[X^2]},\qquad d(X,Y)=\|X-Y\|=\sqrt{\mathbb E[(X-Y)^2]}.
$$

$\mathcal H$ is closed under addition because $(X+Y)^2\le 2X^2+2Y^2$, and $\mathbb E[XY]$ is finite because $|XY|\le\tfrac12(X^2+Y^2)$. Two further facts make it a Hilbert space rather than only a vector space: variables that are equal almost surely are identified, so $\|X\|=0$ forces $X=0$; and $L^2$ is complete.

In any inner-product space, orthogonal vectors obey Pythagoras. If $\langle u,v\rangle=0$, then

$$
\|u+v\|^2=\langle u,u\rangle+\langle u,v\rangle+\langle v,u\rangle+\langle v,v\rangle=\|u\|^2+\|v\|^2 .
$$

My proof writes $\langle u,v\rangle$ twice; the second is $\langle v,u\rangle$, equal by symmetry. Applying the lemma twice gives the same result for three mutually orthogonal vectors.

Two consequences turn expectation and variance into geometry. Let $\mathbf 1$ be the random variable that always equals 1.

- $\mathbb E[X]=\langle X,\mathbf 1\rangle$ and $X-\mathbb E[X]\perp\mathbf 1$, so $\mathbb E[X]\,\mathbf 1$ is the orthogonal projection of $X$ onto the constants, $\operatorname{span}\{\mathbf 1\}$.
- $\mathrm{Var}(X)=\|X-\mathbb E X\|^2$ and $\mathrm{Cov}(X,Z)=\langle X-\mathbb E X,\ Z-\mathbb E Z\rangle$. Variance and covariance are length and inner product after the constant component is removed.

### Orthogonal is not the same as uncorrelated

My note on the page: $\mathrm{Cov}(X,Z)=\mathbb E[XZ]-\mathbb E[X]\,\mathbb E[Z]$, so if $X\perp Z$, meaning $\mathbb E[XZ]=0$, then $\mathrm{Cov}(X,Z)=-\mathbb E[X]\,\mathbb E[Z]$. My last line, "if they're centered, their Cov is zero", holds for orthogonal variables when at least one of them is centred. For centred variables, orthogonal and uncorrelated mean the same thing. Without centring they differ. With $B=\pm1$ equally likely, $X=1+B$ and $Z=1-B$ satisfy $XZ=0$, so they are orthogonal, yet $\mathrm{Cov}(X,Z)=-1$.

## 2. Three orthogonal pieces of the prediction error

Let $\mathcal H_D=\{g(D):\mathbb E[g(D)^2]<\infty\}$ be the square-integrable functions of the training data, the plane on my diagram. It contains the constants, so the axis $\mathbf 1$ lies inside it. Adding and subtracting $f(x)$ and $\mathbb E_D\hat f$:

$$
Y-\hat f(x;D)=\underbrace{Y-f(x)}_{\varepsilon\ \perp\ \mathcal H_D}
+\underbrace{f(x)-\mathbb E_D\hat f}_{\in\ \operatorname{span}\{\mathbf 1\}}
+\underbrace{\mathbb E_D\hat f-\hat f(x;D)}_{\in\ \mathbf 1^{\perp}\cap\,\mathcal H_D}.
$$

The three labels are mine. Each takes one line to check:

- **Bias ⊥ fluctuation.** The bias term is a constant $c$ and the fluctuation has mean zero, so $\langle c\,\mathbf 1,\ \mathbb E_D\hat f-\hat f\rangle=c\,\mathbb E\big[\mathbb E_D\hat f-\hat f\big]=0$.
- **Noise ⊥ everything built from $D$.** For any $g(D)\in\mathcal H_D$, independence and $\mathbb E[\varepsilon]=0$ give $\langle\varepsilon,g(D)\rangle=\mathbb E[\varepsilon]\,\mathbb E[g(D)]=0$. The bias constant and the fluctuation both lie in $\mathcal H_D$, so the noise is orthogonal to both. Mean independence, $\mathbb E[\varepsilon\mid D]=0$, would be enough.

Since $\varepsilon$ is centred, $\|\varepsilon\|^2=\mathbb E[\varepsilon^2]=\sigma^2$. Pythagoras for the three orthogonal pieces then gives

$$
\mathrm{MSE}(\hat f)=\|Y-\hat f\|^2
=\sigma^2+\big(f(x)-\mathbb E_D\hat f\big)^2+\mathbb E_D\big[(\hat f-\mathbb E_D\hat f)^2\big]
=\sigma^2+\mathrm{Bias}^2(\hat f)+\mathrm{Var}(\hat f),
$$

which is the standard decomposition (ISL §2.2.2; ESL §7.3).

### A clean projection diagram

![[assets/figures/2026-11-12-bias-variance-projection/01-l2-projections.svg]]

*Original reconstruction inspired by my handwritten diagram, with $\mu=\mathbb E_D\hat f$. Orange: estimator fluctuation; purple: bias; blue: fresh-response noise; green dashed segment: total prediction error. The original handwriting above is unchanged.*

There are **two different projections**:

$$
P_{\operatorname{span}\{\mathbf 1\}}\hat f=\mu\,\mathbf 1,
\qquad
P_{\mathcal H_D}Y=f(x)\,\mathbf 1.
$$

The first drops $\hat f$ onto the constant axis; the second drops $Y$ onto the training-data space. Follow the colored path $\hat f\to\mu\to f(x)\to Y$: its displacements are $\mu-\hat f$, $f(x)-\mu$, and $Y-f(x)$. They add to the same vector as the green shortcut, and their squared lengths add because they are mutually orthogonal.

**What the picture represents.** Each endpoint is an entire random variable in $L^2$, not a realized scalar prediction from one dataset. The drawing shows a three-dimensional slice containing these vectors; $\mathcal H_D$ need not actually be two-dimensional. Perspective does not preserve the displayed angles or lengths: the right-angle markers refer to $\langle U,V\rangle=\mathbb E[UV]=0$ in $L^2$.

**Reading the diagram.** $f(x)$ and $\mathbb E_D\hat f$ are points on the axis $\mathbf 1$, a distance $|\mathrm{Bias}|$ apart. $\hat f(x;D)$ lies in the plane $\mathcal H_D$; its foot on the axis is $\mathbb E_D\hat f$, at distance $\sqrt{\mathrm{Var}}$. That is the first right angle. $Y$ sits above the plane over $f(x)$, at height $\|\varepsilon\|=\sigma$. That is the second right angle. The dashed line from $\hat f$ to $Y$ has length $\sqrt{\mathrm{MSE}}$.

**Why σ² is irreducible** (added). Because $Y-f(x)=\varepsilon\perp\mathcal H_D$, the constant $f(x)$ is the [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2#Orthogonality characterizes the conditional expectation|orthogonal projection]] of $Y$ onto $\mathcal H_D$, that is, $\mathbb E[Y\mid D]=f(x)$. Every predictor $g(D)$ built from the training data therefore satisfies $\|Y-g(D)\|^2=\sigma^2+\|f(x)-g(D)\|^2\ge\sigma^2$. Bias and variance are the two legs inside the plane, which a better estimator can shorten. The noise leg is perpendicular to the plane, so no estimator can shorten it. The tradeoff is between the two in-plane legs: a more flexible estimator typically moves $\mathbb E_D\hat f$ closer to $f(x)$ but spreads $\hat f$ further from it.

## 3. The algebraic proof is the same argument with the cross term written out

My formal proof, for an estimator $\hat\theta$ of a parameter $\theta$:

$$
\begin{aligned}
\mathrm{MSE}(\hat\theta)&=\mathbb E_\theta(\hat\theta-\theta)^2
=\mathbb E_\theta\big(\hat\theta-\mathbb E_\theta\hat\theta+\mathbb E_\theta\hat\theta-\theta\big)^2\\
&=\mathbb E_\theta\big[(\hat\theta-\mathbb E_\theta\hat\theta)^2\big]
+2\,\mathbb E_\theta\big[(\hat\theta-\mathbb E_\theta\hat\theta)(\mathbb E_\theta\hat\theta-\theta)\big]
+\mathbb E_\theta\big[(\mathbb E_\theta\hat\theta-\theta)^2\big].
\end{aligned}
$$

**Correction.** In the last line of my page I pulled $(\hat\theta-\mathbb E_\theta\hat\theta)$ out of the cross-term expectation. That factor is random and cannot leave the expectation. The constant factor is $(\mathbb E_\theta\hat\theta-\theta)$:

$$
2\,\mathbb E_\theta\big[(\hat\theta-\mathbb E_\theta\hat\theta)(\mathbb E_\theta\hat\theta-\theta)\big]
=2(\mathbb E_\theta\hat\theta-\theta)\,\mathbb E_\theta\big[\hat\theta-\mathbb E_\theta\hat\theta\big]=0 .
$$

The page stops before this step. Finishing it gives $\mathrm{MSE}(\hat\theta)=\mathrm{Var}_\theta(\hat\theta)+\mathrm{Bias}_\theta^2(\hat\theta)$.

Geometrically, the cross term is $2\langle\hat\theta-\mathbb E_\theta\hat\theta,\ (\mathbb E_\theta\hat\theta-\theta)\mathbf 1\rangle$, a fluctuation against a constant, which is zero by the first right angle. My red annotation on the diagram says the same for $\mathbb E[(\hat f-f)^2]$: the $\sqrt{\mathrm{Var}}$ piece is $\perp\operatorname{span}\{\mathbf 1\}$, the bias piece lies in $\operatorname{span}\{\mathbf 1\}$, so the two are orthogonal.

The two decompositions therefore differ by one dimension. The estimation MSE, $\mathbb E(\hat\theta-\theta)^2=\mathrm{Var}+\mathrm{Bias}^2$, lives inside $\mathcal H_D$ and has two legs. The prediction MSE adds the noise leg $\varepsilon$, perpendicular to $\mathcal H_D$, and so adds exactly $\sigma^2$.

## 4. Application: predicting electricity demand with nearest neighbors

Suppose a building manager wants to predict daily electricity use $Y$ (kWh) from outdoor temperature $t$. A simple model is **[[Learning/Statistical computing & learning/Statistical learning & prediction/KNN versus K-means - neighbors predict, centroids cluster#KNN: aggregate targets locally|k-nearest-neighbor regression]]**: find the $k$ past days with temperatures closest to the target temperature, then average their electricity readings:

$$
\hat f_k(t;D)=\frac1k\sum_{i\in N_k(t)}Y_i.
$$

Here $N_k(t)$ is the set of selected day indices. This is the standard KNN regression rule, not a fitted straight line. See [Stanford STATS 202, “KNN estimator”](https://web.stanford.edu/class/stats202/notes/Linear-regression/K-nearest-neighbors.html#knn-estimator).

- **Small $k$:** use very similar-temperature days, but an unusually busy or quiet day can strongly change the prediction. The estimate is local but unstable across training datasets.
- **Large $k$:** average away more day-to-day noise, but include temperatures with genuinely different expected demand. The estimate is stable but can systematically miss the demand at the target temperature.

### A worked example with exact bias and variance

The application is realistic; **the following data-generating model is invented for illustration, not measured building data**. Let

$$
f(t)=50+\tfrac12(t-20)^2,
\qquad Y_i=f(t_i)+\varepsilon_i,
\qquad \mathbb E[\varepsilon_i]=0,\quad \mathrm{Var}(\varepsilon_i)=16.
$$

Temperature is measured in °C. This toy mean curve has a low-demand temperature at $20^\circ\mathrm C$, with greater demand on colder or warmer days. Fix nine training temperatures $t_i=16,17,\ldots,24$, and predict a **new** day at $t=20$. Assume independent training errors and independent new-day noise, all with variance $16\ \mathrm{kWh}^2$. Repeated training datasets here mean new noisy readings at those **same** nine temperatures.

Since the neighbor set is fixed when the temperatures are fixed,

$$
\mu_k:=\mathbb E_D\hat f_k(20;D)
=\frac1k\sum_{i\in N_k(20)}f(t_i),
\qquad
\mathrm{Var}_D(\hat f_k)
=\frac1{k^2}\sum_{i\in N_k(20)}\mathrm{Var}(\varepsilon_i)
=\frac{16}{k}.
$$

The last equality uses independence to remove all covariance terms. Thus, using this note's bias sign convention,

$$
\mathrm{Bias}_k=50-\mu_k,
\qquad
\boxed{\mathrm{MSE}_k(20)=16+(50-\mu_k)^2+\frac{16}{k}.}
$$

For example, $k=5$ uses temperatures $18,19,20,21,22$, so

$$
\mu_5=\frac{52+50.5+50+50.5+52}{5}=51,
\qquad
\mathrm{MSE}_5=16+(-1)^2+\frac{16}{5}=20.2.
$$

| Neighbors $k$ | Mean prediction $\mu_k$ (kWh) | Bias² | Variance | Noise | Expected test MSE |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 50.00 | 0.00 | 16.00 | 16.00 | 32.00 |
| 5 | 51.00 | 1.00 | 3.20 | 16.00 | **20.20** |
| 9 | 53.33 | 11.11 | 1.78 | 16.00 | 28.89 |

*All squared quantities are in $\mathrm{kWh}^2$; displayed decimals are rounded. These are expectations over repeated training readings and an independent new response, not errors from one train/test split.*

![[assets/figures/2026-11-12-bias-variance-projection/02-electricity-knn-tradeoff.svg]]

*Left: the true mean curve and the average of its five nearest values. Right: the exact decomposition for three choices of $k$, using the same component colors as the projection diagram.*

**Back to the geometry.** Changing $k$ chooses a different estimator vector $\hat f_k$ in the same $\mathcal H_D$. Its orange fluctuation leg has length $4/\sqrt{k}$, while its purple bias leg has length $|50-\mu_k|$. Moving from $k=1$ to $k=5$ accepts some bias in exchange for a much larger variance reduction. Moving to $k=9$ reduces variance further, but its added bias costs more than it saves. The blue noise leg stays at length $4$. The goal is the shortest **total squared error**, not the shortest variance leg alone.

This is a concrete trade-off, not a theorem that bias must increase with $k$ for every mean function or input. In practice $f$ is unknown, so validation is used to compare choices of $k$. The exact $16/k$ calculation is conditional on fixed neighbor temperatures and independent, equal-variance errors; random temperatures or correlated daily errors require additional terms. Likewise, “irreducible” is relative to the information used: adding useful predictors can change the noise floor, while changing $k$ alone does not change this model's $16$.

## Connections

- [[Backbone/Statistical inference & modeling/Inference foundations/Statistical reasoning/Sampling distributions/Mean squared error|Mean squared error]] — My formal proof is the estimator version, MSE = Var + Bias²; the prediction MSE here adds one orthogonal noise leg, σ².
- [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2|Conditional expectation as orthogonal projection in L2]] — The same Hilbert space $L^2$ and the same projection onto $\mathbf 1$; here $f(x)=\mathbb E[Y\mid D]$ is the projection of $Y$ onto $\mathcal H_D$, which is why the noise leg cannot be reduced.

- [[Learning/Statistical computing & learning/Statistical learning & prediction/KNN versus K-means - neighbors predict, centroids cluster|KNN versus K-means - neighbors predict, centroids cluster]] — The electricity-demand example shows how KNN’s neighbor count changes bias and variance; K-means’ cluster count has a different role.

## Origin

> [!info]- Source details
> My handwritten page, 2026-11-08: the model and my definitions with the bias calculation, the three-piece split with its orthogonality labels, the $L^2$ diagram, random variables as vectors, the $L^2$ inner product, norm and distance, the Pythagoras lemma, the covariance note, and the formal estimator MSE proof up to the cross term.
>
> Corrections by Claude: the cross-term factor and the missing last step, the two meanings of ⊥, the precise orthogonal-versus-uncorrelated statement, "expected" for "estimated", and the bias sign convention. Added by Claude: the closure and Hilbert-space remarks, the explicit orthogonality checks, the projection argument for the irreducible error, and the one-extra-dimension link between the two proofs.
>
> Added by Codex, 2026-11-12, at the user's request for another projection SVG similar to the handwriting and one real-life application: the clean projection diagram, its reading guide, and the electricity-demand KNN example with a second explanatory SVG. The building scenario and numerical model are agent-created teaching examples, not user handwriting, a measured dataset, or a reported deployment. The KNN definition was checked against the Stanford course source linked above.
>
> Reproduction: [[assets/figures/2026-11-12-bias-variance-projection/build.py|figure generator and exact checks]]; [[assets/figures/2026-11-12-bias-variance-projection/checks.json|constructed coordinates, data and results]]. For the geometry, independent fair signs $U,V$ give $\hat f=2+4U$, $Y=5+3V$, and $D=U$: both projections, all cross inner products and $34=9+9+16$ check exactly. For the application, independent errors taking values $\pm4$ realize the stated moments; enumeration of all $2^{10}=1024$ training/new-response noise outcomes checks the table exactly (also $k=3,7$). These finite-model checks supplement the algebra, not a proof about empirical electricity data. SVGs were parsed and their rendered previews inspected; live Obsidian rendering was not checked. Earlier provenance, original image bytes, home and conceptual connections are unchanged.
