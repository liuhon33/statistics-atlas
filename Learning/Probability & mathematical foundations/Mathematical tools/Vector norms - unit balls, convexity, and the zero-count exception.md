---
id: learning-vector-norms-unit-balls
title: Vector norms - unit balls, convexity, and the zero-count exception
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms]]'
subject: probability
backbone_path: Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Vectors, spaces & projections → Inner products and norms
study_band: Foundation
note_types: [topic-note, derivation, insight]
source_format: lecture-video-and-official-captions
created: 2026-11-12
updated: 2026-11-12
status: active
verification: checked
learning_state: unknown
aliases: [L1 L2 and infinity norms, Geometry of p norms, L0 is not a norm]
tags: [atlas/learning, subject/probability, topic/norms]
connections:
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Convexity & inequalities/Convex functions & bounds/Convex sets and functions]]'
  - '[[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation]]'
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression]]'
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso]]'
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net]]'
  - '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization]]'
  - '[[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit]]'
sources:
  - 'https://www.youtube.com/watch?v=NcPUI7aPFhA&t=560s'
  - 'https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/resources/lecture-8-norms-of-vectors-and-matrices/'
  - '[[raw/articles/2026-11-12-MIT18065-L08-norms-official-captions.vtt]]'
  - '[[raw/assets/2026-11-12-Norms-I01-unit-balls-at-17m50.png]]'
  - '[[raw/assets/2026-11-12-Norms-I02-board-at-18m26.png]]'
  - '[[assets/figures/2026-11-12-vector-norms/source-manifest.json]]'
  - '[[assets/figures/2026-11-12-vector-norms/draw_and_check.py]]'
  - '[[assets/figures/2026-11-12-vector-norms/checks.json]]'
---

# Vector norms - unit balls, convexity, and the zero-count exception

Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Vectors, spaces & projections → Inner products and norms

**A norm is a rule for measuring a vector's size. Changing that rule changes which vectors count as equally large.** The familiar Euclidean ruler gives a circular boundary in two dimensions; summing absolute coordinates gives a diamond; taking the largest absolute coordinate gives a square. Their filled unit balls are convex. The zero-count and the $0<p<1$ expressions expose different ways a proposed size measure can fail to be a norm.

This note follows Gilbert Strang's **[Lecture 8, 9:20–18:30](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=560s)**. The formulas below make the geometry self-contained.

## 1. The rules and every size measure in this segment

Let $x=(x_1,\ldots,x_n)^\top\in\mathbb R^n$, with finite $n\geq1$. A **norm** is a function $N:\mathbb R^n\to[0,\infty)$ satisfying, for every vector $x,y$ and scalar $a\in\mathbb R$:

1. **Positive definiteness:** $N(x)=0$ if and only if $x=0$.
2. **Absolute homogeneity:** $N(ax)=|a|N(x)$.
3. **Triangle inequality:** $N(x+y)\leq N(x)+N(y)$.

The first rule distinguishes zero from a nonzero vector; the second makes doubling a vector double its length; the third says that adding two vectors cannot cost more length than the sum of their separate lengths. These are the standard norm axioms in [University of Houston M6366, Lecture 1, p. 2](https://www.math.uh.edu/~giles/PDFpapers/Lects.pdf#page=2).

For finite coordinate vectors, $\ell_p$ is the usual notation. Machine-learning discussions often write “L1” and “L2” for these same vector norms.

| Measure | Definition | What it measures | Example $x=(3,-4,0)$ |
| --- | --- | --- | --- |
| $\ell_1$ | $\lVert x\rVert_1=\sum_{i=1}^n \lvert x_i\rvert$ | Total coordinate magnitude | $7$ |
| $\ell_2$ | $\lVert x\rVert_2=\sqrt{\sum_{i=1}^n x_i^2}$ | Euclidean length | $5$ |
| $\ell_\infty$, or max norm | $\lVert x\rVert_\infty=\max_i \lvert x_i\rvert$ | Largest coordinate magnitude | $4$ |
| General $\ell_p$, $1\leq p<\infty$ | $\lVert x\rVert_p=(\sum_{i=1}^n \lvert x_i\rvert^p)^{1/p}$ | A family joining $\ell_1$, $\ell_2$, and the max-norm limit | $(3^p+4^p)^{1/p}$ |
| $0<p<1$; specifically $p=\tfrac12$ | Same expression, but a **quasi-norm**, not a norm when $n\geq2$ | An inward-bending unit sublevel set | $(\sqrt3+2)^2=7+4\sqrt3\approx13.9282$ at $p=\tfrac12$ |
| “$\ell_0$ norm” | $\lVert x\rVert_0=\#\{i:x_i\ne0\}$ | Number of nonzero coordinates; **not a norm** | $2$ |

The absolute values are essential: opposite signs do not cancel a vector's size. The square root in $\ell_2$ is essential too: $\lVert 2x\rVert_2^2=4\lVert x\rVert_2^2$, so the **squared** Euclidean norm is not itself a norm.

## 2. Read a norm through its unit ball

The **unit sphere** is $\{x:N(x)=1\}$; the **closed unit ball** is $B=\{x:N(x)\leq1\}$. In two dimensions, the former is the boundary curve and the latter includes the inside. Strang makes the inclusion of the interior explicit at [17:21–17:33](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=1041s).

For $x\in\mathbb R^2$:

- **$\ell_2$:** $x_1^2+x_2^2\leq1$ gives a disk. Its boundary is a circle.
- **$\ell_1$:** $|x_1|+|x_2|\leq1$ gives a filled diamond, with vertices $(\pm1,0)$ and $(0,\pm1)$. In the first quadrant, the boundary is the line $x_1+x_2=1$; the other quadrants require the absolute values.
- **$\ell_\infty$:** $\max(|x_1|,|x_2|)\leq1$ means **both** $|x_1|\leq1$ and $|x_2|\leq1$. This is the square $[-1,1]^2$. On the boundary, at least one absolute coordinate equals $1$.

![[assets/figures/2026-11-12-vector-norms/01-three-unit-balls.svg]]

*Original analytic illustration of the three lecture shapes. The shaded regions are closed unit balls; all panels use the same coordinate scales. Notice the diamond inside the disk inside the square.*

For a fixed vector, increasing $p$ decreases or preserves its $\ell_p$ size. Consequently the **unit balls grow** as $p$ increases. In particular,

$$
\lVert x\rVert_\infty\leq\lVert x\rVert_2\leq\lVert x\rVert_1,
\qquad B_1\subseteq B_2\subseteq B_\infty.
$$

The max norm really is the $p\to\infty$ limit. With $M=\max_i|x_i|$,

$$
M\leq\left(\sum_i|x_i|^p\right)^{1/p}\leq n^{1/p}M
\longrightarrow M.
$$

This is the precise version of the diamond → circle → square progression at [13:40–14:03](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=820s). Monotonicity for finite vectors is also stated in [M6366, Theorem 1.1, p. 3](https://www.math.uh.edu/~giles/PDFpapers/Lects.pdf#page=3).

```atlas-interactive
path: assets/figures/2026-11-12-vector-norms/explorer.html
title: Vector norm unit balls and the midpoint test
height: 930
```

[[assets/figures/2026-11-12-vector-norms/explorer.html|Open the standalone norm explorer]]

*Original interactive illustration. Try $p=\tfrac12,1,2,\infty$, then the zero-count. Keep an eye on the same midpoint $(\tfrac12,\tfrac12)$ while the ruler changes.*

## 3. Why convexity is the geometric test

A set is **convex** when the entire segment between any two of its points stays in the set. If $x,y\in B$ and $0\leq t\leq1$, the norm axioms give

$$
N(tx+(1-t)y)
\leq N(tx)+N((1-t)y)
=tN(x)+(1-t)N(y)
\leq1.
$$

So every norm's unit ball is convex. This explains the lecture's comparison at [16:36–18:06](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=996s).

The converse needs assumptions: **if positive definiteness and absolute homogeneity already hold**, a convex unit ball implies the triangle inequality. For nonzero $x,y$, write

$$
\frac{x+y}{N(x)+N(y)}
=\frac{N(x)}{N(x)+N(y)}\frac{x}{N(x)}
+\frac{N(y)}{N(x)+N(y)}\frac{y}{N(y)}.
$$

This is a convex combination of two unit vectors, so its size is at most $1$. Homogeneity then gives $N(x+y)\leq N(x)+N(y)$. If either vector is zero, the inequality holds directly. See [*Convexity, Inequalities, and Norms*, Theorem 9, p. 11](https://e.math.cornell.edu/people/belk/measuretheory/Inequalities.pdf#page=11).

For $p\geq1$, the scalar function $u\mapsto|u|^p$ is convex. Hence, for $x,y\in B_p$,

$$
\sum_i|tx_i+(1-t)y_i|^p
\leq t\sum_i|x_i|^p+(1-t)\sum_i|y_i|^p
\leq1.
$$

This proves $B_p$ is convex; positive definiteness and homogeneity follow directly from the formula, so the converse establishes that these are norms. This is the convexity route to Minkowski's inequality. For $p=\infty$, the coordinate bounds make the ball a convex box.

## 4. What fails for $0<p<1$

For $p=\tfrac12$ in two dimensions,

$$
\lVert x\rVert_{1/2}
=(\sqrt{|x_1|}+\sqrt{|x_2|})^2,
\qquad
B_{1/2}=\{x:\sqrt{|x_1|}+\sqrt{|x_2|}\leq1\}.
$$

The sides bend inward. Let $e_1=(1,0)$ and $e_2=(0,1)$. Each has size $1$, but

$$
\lVert e_1+e_2\rVert_{1/2}=4>1+1.
$$

Thus the **triangle inequality fails**. Equivalently, the midpoint $m=(\tfrac12,\tfrac12)$ has size $2>1$, even though both endpoints lie in the set. The ball is not convex. For every $0<p<1$ the same example gives $\lVert e_1+e_2\rVert_p=2^{1/p}>2$; it requires dimension at least two. Homogeneity still holds. This supplies an explicit check of the sketch at [16:12–16:36](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=972s).

![[assets/figures/2026-11-12-vector-norms/02-non-norm-cases.svg]]

*Original analytic illustration. Orange endpoints belong to each set, but their midpoint does not. Left: the $p=\tfrac12$ sublevel set is bounded. Right: the zero-count sublevel set contains both entire coordinate axes, including the origin.*

## 5. What fails for the zero-count

The notation $\lVert x\rVert_0$ counts nonzero coordinates. It ignores their magnitudes: $(100,0)$ and $(0.001,0)$ both have count $1$.

For any $a\ne0$, scaling does not change which coordinates are nonzero:

$$
\lVert ax\rVert_0=\lVert x\rVert_0.
$$

For example, $\lVert2(1,0)\rVert_0=1$, whereas homogeneity would require $2\lVert(1,0)\rVert_0=2$. **Absolute homogeneity fails.** The support-count inequality $\lVert x+y\rVert_0\leq\lVert x\rVert_0+\lVert y\rVert_0$ actually holds: a nonzero coordinate of $x+y$ must come from a nonzero coordinate of $x$ or $y$.

In two dimensions:

- $\lVert x\rVert_0=1$: both coordinate axes with the origin removed, extending without bound.
- $\lVert x\rVert_0\leq1$: both entire axes, including the origin.

This distinguishes the equality set drawn at [14:09–15:17](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=849s) from the later “ball includes the inside” convention. The sublevel set is nonconvex: $(1,0)$ and $(0,1)$ belong to it, but their midpoint has two nonzero entries.

There is no valid substitution of $p=0$ into the $\ell_p$ formula. The useful finite-dimensional limit is

$$
\lim_{p\downarrow0}\lVert x\rVert_p^p
=\lim_{p\downarrow0}\sum_i|x_i|^p
=\#\{i:x_i\ne0\}.
$$

Each nonzero coordinate contributes a term tending to $1$; a zero coordinate contributes $0$ for every $p>0$. It is the **sum of powers**, not generally $\lVert x\rVert_p$ itself, that tends to the count. For example, $\lVert(1,1)\rVert_p=2^{1/p}\to\infty$.

The pictures also need this distinction: as $p\downarrow0$, the finite-$p$ unit balls remain inside $[-1,1]^2$ and approach the coordinate-axis **segments** there. They do not become the unbounded zero-count set. For instance, $(2,0)$ is in the zero-count set but in no finite-$p$ unit ball.

> [!note] Follow the shapes into regularization
> Apply these size measures to a **coefficient vector**, not the observed inputs: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso#2. How it works — a corner, a threshold, and a Laplace prior|lasso uses the L1 norm]], [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression#2. How it works — squared norm and Gaussian prior|ridge uses squared L2]], and [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net#2. How it works — both penalties, one objective|elastic net uses both]]. The diamond's corners explain possible zeros; the disk explains smooth shrinkage. These are forms of [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|regularization]], not guarantees against overfitting: use validation to choose the strength. The [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit#2. How the prior becomes an L2 penalty|Bayesian-regression derivation]] shows exactly how a Gaussian log prior produces the squared norm. These follow-up links were requested after the original lecture digest; its source interval is unchanged.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Convexity & inequalities/Convex functions & bounds/Convex sets and functions|Convex sets and functions]] — Convex combinations explain why norm unit balls are convex and expose the $p<1$ and zero-count counterexamples.
- [[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation|Standardization geometry]] — That note's unit-length normalization uses the Euclidean norm; this comparison shows what changes when a different ruler defines unit size.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Ridge regression|Ridge regression]] — the coefficient penalty uses squared Euclidean length, retaining circular budgets but not norm homogeneity.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Lasso|Lasso]] — the L1 diamond becomes a coefficient budget whose axis corners can yield exactly zero coefficients.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Supervised learning methods/Penalized linear models/Elastic net|Elastic net]] — adding L1 and squared-L2 costs combines axis corners and curvature; the mixed cost is convex but not a norm when the quadratic term is present.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Learning objectives & evaluation/Risk, fit & generalization/Regularization|Regularization]] — a size measure becomes a modeling preference when its value is penalized alongside training error.
- [[Learning/Statistical inference & modeling/Bayesian inference/Bayesian linear regression - ridge, uncertainty, and the flat-prior limit|Bayesian linear regression]] — the squared Euclidean coefficient norm becomes a Gaussian negative log prior, turning norm geometry into the ridge MAP calculation.

## Origin

> [!info]- Source details
> Requested source: Gilbert Strang, MIT 18.065, Spring 2018, *Lecture 8: Norms of Vectors and Matrices*, [9:20–18:30](https://www.youtube.com/watch?v=NcPUI7aPFhA&t=560s). Read every official caption cue intersecting this interval; selected board views were inspected at 17:50 and 18:26. This is caption-based coverage with selected visual inspection, not continuous audiovisual viewing. The [[raw/articles/2026-11-12-MIT18065-L08-norms-official-captions.vtt|full official caption file]] is preserved; material outside the interval is not marked digested.
>
> The lecture begins its transition to a weighted $S$-norm at 18:06; at 18:26 only the $S$ label is on the board. Its definition follows the requested cutoff, so the weighted-norm and later matrix-norm sections are outside this digest.
>
> The user selected the topic and deferred the regularization connections; no personal derivation or substantive question was supplied. The axiom recap, common numerical example, expanded proofs and counterexamples, zero-limit clarification, diagrams and explorer are agent-added explanations. Supporting references were read at the cited sections, not ingested in full. The source sketches and formulas were inspected; clearer generated illustrations are embedded and the two source screenshots remain linked in `sources`.
>
> Verification: analytic norm/convexity arguments, support-count and $p<1$ counterexamples, limit bounds, numerical values and plotted boundaries checked. Reproduction and results: [[assets/figures/2026-11-12-vector-norms/draw_and_check.py|figure generator]], [[assets/figures/2026-11-12-vector-norms/checks.json|mathematical checks]], [[assets/figures/2026-11-12-vector-norms/source-manifest.json|source coverage and hashes]].
>
> Both static previews and the explorer's presets, keyboard slider and wide/narrow layouts were inspected; [[assets/figures/2026-11-12-vector-norms/browser-checks.json|browser checks]] record the results. Live Obsidian rendering could not be checked because the CLI could not reach the app.
