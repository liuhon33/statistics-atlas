---
id: learning-standardization-geometry
title: Standardization geometry - means, lengths, and correlation
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/Variance and standard deviation]]'
subject: probability
backbone_path: Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → Variance and standard deviation
study_band: U
note_types: [topic-note, derivation, insight, question]
question_roles: [concept-distinction, cross-topic-connection]
source_format: conversation-and-image
created: '2026-11-09'
updated: '2026-11-09'
status: active
verification: checked
learning_state: unknown
aliases: [Centering and standardization as geometry, Pearson correlation as a cosine]
tags: [atlas/learning, subject/probability, topic/standardization]
connections:
  - '[[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic]]'
  - '[[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation]]'
  - '[[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2]]'
  - '[[Learning/Probability & mathematical foundations/Mathematical tools/Three views of matrix multiplication]]'
  - '[[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests]]'
sources:
  - '[[raw/assets/2026-11-09-standardization-I01-visual-reference.png]]'
  - '[[assets/figures/2026-11-09-standardization/draw_standardization.py]]'
  - '[[assets/figures/2026-11-09-standardization/checks.json]]'
  - '[[assets/figures/2026-11-09-standardization/01-coordinate-switch.svg]]'
  - '[[assets/figures/2026-11-09-standardization/02-project-and-center.svg]]'
  - '[[assets/figures/2026-11-09-standardization/03-sd-and-normalization.svg]]'
  - '[[assets/figures/2026-11-09-standardization/04-sphere-and-correlation.svg]]'
  - '[[assets/figures/2026-11-09-standardization/05-center-then-normalize.gif]]'
---

# Standardization geometry - means, lengths, and correlation

Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → Variance and standard deviation

> [!important] These axes are individuals, not features
> In a usual scatterplot, **each point is an individual** and the axes are features. Here, **each axis is an individual** and **one entire feature is a vector**. Its coordinates are that feature's values across all individuals. A colored endpoint is not one person and not a standard deviation.

**Centering removes the mean-direction component. Standard deviation measures the remaining length, up to a known factor. Normalization discards that length, leaving a direction; Pearson correlation is the cosine between two such directions.**

**My question, paraphrased from this request:** Can we follow many colored feature vectors from their original positions, through mean projection and centering, onto a common sphere—and see mean, variance, and correlation in the same geometry?

## 1. The coordinate switch comes first

For a data matrix $D\in\mathbb R^{n\times p}$, rows are individuals and columns are features:

$$
D=\begin{bmatrix}
d_{11}&\cdots&d_{1p}\\
\vdots&&\vdots\\
d_{n1}&\cdots&d_{np}
\end{bmatrix},\qquad
x_j=D_{:j}=(d_{1j},\ldots,d_{nj})^\top\in\mathbb R^n.
$$

The usual row-space picture contains $n$ points in $\mathbb R^p$. Our **observation-space picture** contains $p$ feature vectors in $\mathbb R^n$. This is a different representation of the same table, not merely a rotation of a scatterplot. All features must use the **same individuals in the same order**.

![[assets/figures/2026-11-09-standardization/01-coordinate-switch.svg]]

*Same small table, two views. Individual 1 has values $(1,-0.3)$; individual 2 has $(2,1.7)$; individual 3 has $(3,0.7)$. On the right, cyan A is the whole vector $(1,2,3)$ and orange B is $(-0.3,1.7,0.7)$.*

We use **three individuals** so the observation space really is 3D. There can still be many features: the following diagrams use eight constructed vectors A–H with fixed colors. They are illustrative data, not recovered coordinates from the supplied screenshot. Different raw features can have different physical units; raw lengths are interpreted feature by feature. Normalization removes those units.

## 2. Project onto the all-ones line: the mean component

For one feature $x\in\mathbb R^n$, define

$$
\mathbf1=(1,\ldots,1)^\top,\qquad
\bar x=\frac{\mathbf1^\top x}{n},\qquad
u=\frac{\mathbf1}{\sqrt n}.
$$

The line $\operatorname{span}(\mathbf1)$ contains exactly the **constant features**: everyone has the same value. Its orthogonal projection is

$$
p=\operatorname{proj}_{\mathbf1}(x)
=\frac{x^\top\mathbf1}{\mathbf1^\top\mathbf1}\mathbf1
=\bar x\mathbf1.
$$

Three related objects must stay distinct:

| Object | What it means |
| --- | --- |
| $\bar x$ | Scalar mean; the coefficient of the nonunit vector $\mathbf1$. |
| $p=\bar x\mathbf1$ | Projection **vector**, with every coordinate equal to the mean. |
| $u^\top x=\sqrt n\bar x$ | Signed coordinate along the **unit** mean direction $u$. The projection length is $\sqrt n|\bar x|$. |

Thus “the projection is the mean” is useful shorthand, but the actual arrow is $\bar x\mathbf1$, not the scalar $\bar x$.

## 3. Move the residual arrow to the zero-mean plane

![[assets/figures/2026-11-09-standardization/02-project-and-center.svg]]

*Left: colored arrows are original features; each dashed colored segment goes from its mean projection to its original endpoint. Middle: translate A's residual arrow from its projection foot to the origin, without rotating it. Right: all centered features lie in the plane perpendicular to the gold all-ones direction. The translucent disk is just a finite patch of an infinite plane.*

The residual is the centered feature:

$$
c=x-p=x-\bar x\mathbf1,
\qquad \mathbf1^\top c=\sum_i(x_i-\bar x)=0.
$$

Therefore $c$ belongs to

$$
H=\mathbf1^\perp=\{v\in\mathbb R^n:\mathbf1^\top v=0\}.
$$

For $n=3$, this is the plane $v_1+v_2+v_3=0$ through the origin. For general $n$, it is an $(n-1)$-dimensional hyperplane.

**What exactly moves?** The arrow from $p$ to $x$ has displacement $x-p=c$. Translate both ends by $-p$:

$$
(p\longrightarrow x)\quad\mapsto\quad(0\longrightarrow x-p).
$$

It is the **same vector**, now drawn with its tail at the origin. Its length and direction do not change. Originally it is parallel to $H$, but its tail need not be in $H$. After translation, the entire arrow is in $H$. Equivalently, the original endpoint moves from $x$ to $c$ along a line parallel to $\mathbf1$; $c$ is the orthogonal projection of $x$ onto $H$.

For cyan A:

$$
x_A=(1,2,3)^\top,\quad \bar x_A=2,\quad
p_A=(2,2,2)^\top,\quad c_A=(-1,0,1)^\top.
$$

The translation is not a second statistical operation after centering; it is how we draw the subtraction $x-p$ as an origin-based arrow.

## 4. Where is the standard deviation?

Use the **sample** convention, with $n\ge2$:

$$
s_x^2=\frac1{n-1}\sum_i(x_i-\bar x)^2
=\frac{\|c\|^2}{n-1},\qquad
\boxed{s_x=\frac{\|c\|}{\sqrt{n-1}}.}
$$

The squared residual length is the centered sum of squares; variance divides it by $n-1$; SD takes the square root. These are the [NIST sample variance and SD definitions](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm), interpreted here geometrically.

For A, $\|c_A\|=\sqrt2$ and $s_A=1$. **The residual length is not literally the sample SD**, except when $n=2$. The bracket in the next figure marks a segment of length $s_A$; it does not represent another feature.

![[assets/figures/2026-11-09-standardization/03-sd-and-normalization.svg]]

*Face-on views of the same plane. The orthonormal plotting directions are $v_1=(-1,0,1)/\sqrt2$ and $v_2=(-1,2,-1)/\sqrt6$; these are linear combinations of the individual axes, not new individuals. Left: centered lengths. Middle: sample z-scores. Right: unit-length vectors. The same A–H labels and colors persist.*

The geometric link between mean and variance is **Pythagoras**:

$$
\underbrace{\|x\|^2}_{\text{total squared length}}
=\underbrace{n\bar x^2}_{\text{mean-component squared length}}
+\underbrace{(n-1)s_x^2}_{\text{centered squared length}}.
$$

Equivalently,

$$
\frac1n\sum_i x_i^2=\bar x^2+\frac{n-1}{n}s_x^2.
$$

The mean tells us **where the feature sits along the constant direction**; SD tells us **how far it is from that line**, divided by $\sqrt{n-1}$. Mean alone does not determine variance. Adding $b\mathbf1$ changes the mean by $b$ without changing $c$ or its variance. At a *fixed* total length, however, the two squared components must sum to that fixed value.

## 5. Standardizing is not quite the same as unit normalization

For a nonconstant feature ($s_x>0$), sample z-scores are

$$
z=\frac{x-\bar x\mathbf1}{s_x}=\frac{c}{s_x},\qquad
\mathbf1^\top z=0,\quad s_z=1,\quad\|z\|=\sqrt{n-1}.
$$

With three individuals, they land on a circle of radius $\sqrt2$, not 1. To obtain a **Euclidean unit circle**, use

$$
\boxed{q=\frac{c}{\|c\|}=\frac{z}{\sqrt{n-1}}.}
$$

Now $\|q\|=1$ and $\mathbf1^\top q=0$, but its sample SD is $1/\sqrt{n-1}$, not 1. If instead one defines the descriptive SD using divisor $n$, the corresponding standardized vector has Euclidean radius $\sqrt n$. These are different normalizations of the same direction.

**The circle point is the endpoint of a normalized feature vector, not “the standard deviation.”** A single point retains the pattern of relative deviations across individuals, but discards the original mean and scale. To reconstruct the original feature, retain all three:

$$
\boxed{x=\bar x\mathbf1+\sqrt{n-1}\,s_xq.}
$$

Normalization can **shrink or expand**: feature C has centered length $0.65$, so reaching the unit circle stretches it. A constant feature has $c=0$; it lies on the mean line and has no defined $q$, z-scores, or Pearson correlation with another feature.

### Watch the two operations separately

![[assets/figures/2026-11-09-standardization/05-center-then-normalize.gif]]

*Original animation: first subtract each feature's mean component, moving its endpoint parallel to $\mathbf1$; then change only its radial length within $H$. This animation goes directly from $c$ to $q$, while the static figure above shows the intermediate z-score radius. The view zooms during normalization. Positions are deterministic illustrations, not random samples from a distribution.*

## 6. The sphere–plane intersection and Pearson correlation

![[assets/figures/2026-11-09-standardization/04-sphere-and-correlation.svg]]

*Left: the wireframe unit sphere, the zero-mean plane, and their white intersection circle. Gold is the normal direction $\mathbf1$, not a feature. Every normalized centered feature ends on the circle. Right: the same plane face-on, so A and B's angle can be read without perspective distortion.*

For three individuals:

$$
S^2=\{v\in\mathbb R^3:\|v\|=1\},\qquad
S^2\cap H=\{v:\|v\|=1,\ v_1+v_2+v_3=0\}.
$$

The intersection is a **great circle**, mathematically $S^1$: a one-dimensional curve in a two-dimensional plane. It is not a two-dimensional sphere. Intersecting the **solid ball** $\|v\|\le1$ with the plane would give a **filled disk**; normalized endpoints belong only to its rim. In general, the centered unit vectors form $S^{n-2}$ inside the $(n-1)$-dimensional subspace $H$.

For two nonconstant features measured on the same $n$ individuals,

$$
\begin{aligned}
r_{xy}
&=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}
{\sqrt{\sum_i(x_i-\bar x)^2}\sqrt{\sum_i(y_i-\bar y)^2}}\\
&=\frac{c_x^\top c_y}{\|c_x\|\|c_y\|}
=q_x^\top q_y
=\boxed{\cos\theta}.
\end{aligned}
$$

The first line is the [NIST Pearson correlation formula](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/correlat.htm); the rest follows from the Euclidean inner product. **Correlation is the cosine of the angle**, not the angle itself. The angle is between the two radius vectors from the origin, not between their endpoints without an origin and not the slope angle in the usual scatterplot. With sample z-scores, equivalently $r_{xy}=z_x^\top z_y/(n-1)$.

| Angle | Correlation | Reading the two feature patterns |
| --- | --- | --- |
| $0^\circ$ | $1$ | Identical centered, normalized directions. |
| $60^\circ$ | $0.5$ | Partial alignment, as for A and B. |
| $90^\circ$ | $0$ | Orthogonal centered patterns; not necessarily independence. |
| $180^\circ$ | $-1$ | Opposite directions. |

For the plotted A and B, $c_A=(-1,0,1)$, $c_B=(-1,1,0)$, both lengths are $\sqrt2$, and $c_A^\top c_B=1$. Thus $r_{AB}=1/2$ and $\theta=60^\circ$. No Gaussian assumption is needed.

Two useful consequences:

- **Distance on the sphere:** $\|q_x-q_y\|^2=2(1-r_{xy})$. Highly positively correlated features are nearby; perfectly anticorrelated ones are antipodal.
- **Shift and scale:** replacing $x$ by $ax+b\mathbf1$ preserves $q_x$ when $a>0$ and reverses it when $a<0$. This is why Pearson correlation ignores offsets and positive rescalings, but changes sign under a single negative rescaling.

## 7. Connections to the geometry I have already studied

### Mean–variance separation is not automatically independence

The deterministic decomposition $x=p+c$ holds for every data vector. It does **not** prove that random sample mean and sample variance are independent, one example it work is for the normal distribution, where sample mean and sample variance are independent and orthogonal.  [Lockhart's normal-sample theorem](https://www.sfu.ca/~lockhart/richard/801/01_1/lectures/normal_samples/web.html) states it explicitly. This is the extra probabilistic step in my [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic#2. Orthogonality is geometry; independence uses the Gaussian law|t-statistic note's general proof]]. See also [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Proof of Gaussian's sample mean and variance are independent + rotational invariance#My Question: why rotating the axes leaves the joint law unchanged for Gaussian?|two-observation independence argument]].

There, the vector is standardized by **population** parameters, $(X-\mu\mathbf1)/\sigma$; it is not forced onto a fixed sphere. Here we subtract the **sample** mean and divide by the observed residual norm, forcing $q$ onto the centered unit sphere. The two operations should not share an unexplained “standardized” label.

Estimating the noise scale is what turns the z-test slab into [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests#Why the planes become cones|t-test cones]].

### OLS: restore scale after measuring alignment

For simple regression with an intercept,

$$
\widehat\beta_1=\frac{c_x^\top c_y}{\|c_x\|^2}
=r_{xy}\frac{s_y}{s_x}.
$$

Correlation retains direction; the SD ratio restores the scale and units needed for a slope. With standardized predictor and response, the slope equals $r_{xy}$. This explains my [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation#2. The cosine route finds the nearest point geometrically|three-route OLS result]] using the circle.

### Population L²: when SD really is the residual length

In the [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2#Geometry in $L^2$|population Hilbert space]], vectors are **random variables**, with $\langle U,V\rangle=\mathbb E[UV]$. The constant random variable $1$ has norm 1, unlike the Euclidean vector $\mathbf1$, whose norm is $\sqrt n$. Consequently,

$$
X=\mathbb E[X]\,1+(X-\mathbb E[X]),\qquad
\|X-\mathbb E[X]\|_{L^2}=\operatorname{SD}(X).
$$

For finite, positive variances, population-standardized random variables have unit $L^2$ norm and their inner product is population correlation. This is the setting where “divide by SD and land on a unit sphere” is literally correct without an extra Euclidean factor. It is not the finite-sample coordinate system in the 3D figures.

### Matrices: center all columns, then read correlation as a Gram matrix

Define the centering projector $M=I_n-\mathbf1\mathbf1^\top/n$. It is symmetric, idempotent, and has rank $n-1$. For the data table, $C=MD$ centers every column at once. Normalize each nonzero column of $C$ to form $Q\in\mathbb R^{n\times p}$; then

$$
R=Q^\top Q\in\mathbb R^{p\times p}
$$

is the feature correlation matrix. Its $(j,k)$ entry is the dot product of two normalized feature columns. Thus $R$ is positive semidefinite and has rank at most $n-1$. With only three individuals, all eight directions in the illustration fit in a two-dimensional plane: the $8\times8$ correlation matrix has rank at most 2. This joins the [[Learning/Probability & mathematical foundations/Mathematical tools/Three views of matrix multiplication#1. Row times column: compute an entry|column and dot-product views]] from my matrix-multiplication note. It assumes a common complete set of rows, not different pairwise missing-data subsets.

## Connections

- [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic|Geometric interpretation of the t-statistic]] — Uses the same mean-line and residual-subspace split, while Gaussian independence and population standardization are additional ingredients rather than consequences of centering.
- [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|Three routes from least squares to slope and correlation]] — The cosine between normalized centered features gives Pearson correlation; restoring the SD ratio gives the OLS slope.
- [[Learning/Probability & mathematical foundations/Joint variation & conditioning/Conditional expectation as orthogonal projection in L2|Conditional expectation as orthogonal projection in L2]] — Mean projection has a population analogue, where the expectation inner product makes SD itself the residual norm and population standardization gives unit norm.
- [[Learning/Probability & mathematical foundations/Mathematical tools/Three views of matrix multiplication|Three views of matrix multiplication]] — Applying the centering matrix column by column and taking normalized column dot products produces the correlation Gram matrix.

- [[Learning/Statistical inference & modeling/Frequentist & likelihood inference/Geometric interpretation of z, t, and F tests|Geometric interpretation of z, t, and F tests]] — Uses the mean projection and residual length to explain why known and estimated noise scales produce different decision boundaries.

## Origin

> [!info]- Source details
> Based on my request for a geometric standardization note, with an explicit change of coordinate meaning, colored feature vectors, mean projections, centered arrows, SD, a sphere–plane intersection, and Pearson correlation. The question above is a labeled paraphrase. Codex added the worked data, derivations, diagrams, animation, and links to earlier notes, and corrected the distinctions between mean and projection vector, SD and vector length, standardization and unit normalization, circle and sphere, and correlation and angle.
>
> ![[raw/assets/2026-11-09-standardization-I01-visual-reference.png|450]]
>
> *My supplied visual reference, preserved whole and unchanged. It motivates the colored-vector presentation; its unlabeled points are not treated as a verified dataset or a source of statistical claims. Source creator and original context were not supplied.*
>
> The figures are reproducible from [[assets/figures/2026-11-09-standardization/draw_standardization.py|the generator]], with constructed coordinates and numerical checks in [[assets/figures/2026-11-09-standardization/checks.json|the check record]]. Algebra, normalization factors, dimensions and boundary cases were checked; numerical comparisons support, rather than replace, the derivations. The linked MLA note was consulted for context, not modified or treated as a source for Pearson correlation.
