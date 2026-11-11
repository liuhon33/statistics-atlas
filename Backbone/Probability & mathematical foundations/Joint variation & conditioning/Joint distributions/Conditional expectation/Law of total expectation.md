---
id: conditional-mean-law-of-total-expectation
title: Law of total expectation
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → Law of total expectation
created: '2026-11-08'
updated: '2026-11-11'
status: active
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Conditional expectation (L4)]]'
sources:
- '[[_system/Sources/prob]]'
- '[[raw/assets/2026-11-08-total-expectation-I01-joint-density-slices.png]]'
---

# Law of total expectation

Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → Law of total expectation

Parent: [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Conditional expectation (L4)|Conditional expectation]]

## Statement

For a real random variable $X$ with $\mathbb E|X|<\infty$ and any random variable $Y$ on the same probability space,

$$
\boxed{\mathbb E[\mathbb E[X\mid Y]]=\mathbb E[X].}
$$


The inner expectation is the mean associated with the observed value of $Y$; the outer expectation averages these means over the distribution of $Y$. No independence is required. If $Y$ is discrete, this becomes

$$
\mathbb E[X]=\sum_{y:\,P(Y=y)>0}\mathbb E[X\mid Y=y]P(Y=y).
$$

Thus an overall mean is the **probability-weighted average of subgroup means**, not generally their unweighted average. The integrability assumption ensures finite, well-defined expectations; expressions involving undefined $\infty-\infty$ are outside this statement.

## Visual example

![[assets/figures/tower-property/tower-property.png]]

*Original illustration (Codex), shared with Tower property; reproducible with [[assets/figures/tower-property/draw.ps1|the drawing script]]. Choose a pupil uniformly. Averaging the grade means gives the whole-school mean: $(6/10)7+(4/10)17=11$, matching the direct average of all ten scores.*

## Reading the joint-density graph

Move y₀ to change one conditional mean, then move μₓ to shift their overall weighted average. The lower panel shows the full identity $\mathbb E[\mathbb E[X\mid Y]]=\mu_X$ alongside the selected slice. **Screenshot values** restores the original example used below.

```atlas-interactive
path: assets/figures/2026-11-11-joint-density/joint-density.html
title: Joint density — slices, conditional distributions, and total expectation
height: 1400
```

*Original interactive reconstruction, Codex. The source screenshot is preserved below. Both variables have variance 1; μᵧ = 0, while μₓ, ρ, x₀ and y₀ are adjustable. A camera drag changes only the view. Conditional areas and means use the full Gaussian support.*

[[assets/figures/2026-11-11-joint-density/joint-density.html|Open the standalone explorer]] · [[assets/figures/2026-11-11-joint-density/build.py|Reproduce the figure]] · [[assets/figures/2026-11-11-joint-density/checks.json|Numerical checks]]

> [!example]- Static view
> ![[assets/figures/2026-11-11-joint-density/overview.svg]]
> *Original analytic reconstruction at the screenshot's parameter values. Dashed curves are raw slices; solid curves are normalized conditionals. Dot areas represent relative weights for equal-width y bins.*

> [!info]- Original supplied screenshot
> ![[raw/assets/2026-11-08-total-expectation-I01-joint-density-slices.png]]
> *Preserved unchanged; this original is a static capture. The working controls above are a new reconstruction, not recovered source code.*

$p(x)$ is a distribution of the height for all age groups
$p(x|y)$ distribution of the height, for age y
把X想成身高，$\mathbb E[X]$就是所有年龄段身高的平均值
$\mathbb X|Y$想成对于每个年龄段得身高
$\mathbb E[X|Y]$想成每个年龄段的身高平均值
$\mathbb E[E[X|Y]]$想成每个年龄段甚高的平均值，然后在根据年龄加权取平均值

Write $p(x,y)$ for the joint density, $p_X(x)$ and $p_Y(y)$ for the marginals, and $p_{X\mid Y}(x\mid y)$ for a conditional density. The figure abbreviates these as $p(x)$, $p(y)$ and $p(x\mid y)$.

### 1. Gray surface: the joint density

The whole gray surface represents $p(x,y)$. Its total volume over the entire plane is one:

$$
\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}p(x,y)\,dx\,dy=1.
$$

For a Gaussian, the visible plot shows only part of its infinite support; the normalization concerns the full surface.

### 2. Teal and coral slices: normalize to get conditional densities

Fixing $y=y_0$ cuts out the teal **raw slice** $x\mapsto p(x,y_0)$. Its area is $p_Y(y_0)$, not generally one. Where $p_Y(y_0)>0$,

$$
p_{X\mid Y}(x\mid y_0)=\frac{p(x,y_0)}{p_Y(y_0)},
\qquad
\int p_{X\mid Y}(x\mid y_0)\,dx=1.
$$

The upper-right panel compares the dashed raw slice with the filled normalized curve. Here $p_Y(-1.3)\approx0.17$, so division stretches the slice vertically. In general normalization is a rescaling: if the marginal density exceeds one, it compresses instead. The coral slice at $x=x_0$ works analogously, dividing $p(x_0,y)$ by $p_X(x_0)$ to obtain $p_{Y\mid X}(y\mid x_0)$.

### 3. Purple walls: marginals are slice areas

Each marginal height equals the area of the corresponding raw slice:

$$
p_X(x_0)=\int p(x_0,y)\,dy,
\qquad
p_Y(y_0)=\int p(x,y_0)\,dx.
$$

Thus the coral slice's area equals the purple height at $x_0$ on the $p(x)$ wall; the teal slice's area equals the height at $y_0$ on the $p(y)$ wall. **These are density values, not probabilities of individual points.** For continuous variables, $P(Y=y_0)=0$ even when $p_Y(y_0)>0$.

### 4. Conditional mean: the balance point of a slice

At a fixed $y_0$, the dashed vertical line in the teal panel marks the single number

$$
m(y_0):=\mathbb E[X\mid Y=y_0]
=\int x\,p_{X\mid Y}(x\mid y_0)\,dx.
$$

This is the slice's balance point along the $x$-axis. Multiplying the raw slice by a constant changes its area but not this balance point. As $y_0$ varies, the floor trace consists of points $(m(y),y)$; the random variable $\mathbb E[X\mid Y]$ is $m(Y)$.

For the **standardized jointly Gaussian model shown**, $\mu_X=\mu_Y=0$, $\sigma_X=\sigma_Y=1$ and $|\rho|<1$:

$$
X\mid Y=y\sim N(\rho y,1-\rho^2),
\qquad m(y)=\rho y.
$$

Here $N(\mu,v)$ uses variance $v$. With $\rho=0.8$, $y_0=-1.3$ and $x_0=1$, the two conditional means are $-1.04$ and $0.80$, and both conditional variances are $0.36$. More generally, a jointly Gaussian pair has

$$
m(y)=\mu_X+\rho\frac{\sigma_X}{\sigma_Y}(y-\mu_Y).
$$

This is the regression of $X$ on $Y$; for a non-Gaussian joint distribution the conditional-mean trace need not be straight. The Gaussian mean coincides with the peak, but a general distribution's mean need not.

### 5. Total expectation: average the balance points with their marginal weights

The final averaging is over $Y$:

$$
\boxed{
\mathbb E[\mathbb E[X\mid Y]]
=\int m(y)p_Y(y)\,dy
=\mathbb E[X].
}
$$

The dot sizes along the teal trace illustrate relative density weights. For equal-width $y$ bins, their probability masses are approximately $p_Y(y)\Delta y$; density at a point alone is not a probability. It is the **$x$-coordinates of the conditional balance points** that are averaged. Here $m(y)=\rho y$ and $\mathbb E[Y]=0$, so the average is $\rho\mathbb E[Y]=0$, matching the purple $\mathbb E[X]$ reference line.

The normalization and weighting cancel algebraically:

$$
\int\left[\int x\frac{p(x,y)}{p_Y(y)}\,dx\right]p_Y(y)\,dy
=\iint x\,p(x,y)\,dx\,dy
=\mathbb E[X].
$$

The ratio is used where $p_Y(y)>0$; zero-density values contribute no weight. The earlier assumption $\mathbb E|X|<\infty$ justifies the integration step. Thus the picture illustrates the same law as the class/grade example, now with a continuum of slices.

**Gaussian reference:** Lancaster University, *MATH230*, [§10.1.1, Conditional Distributions](https://www.lancaster.ac.uk/~prendivs/accessible/math230/math230_notes.tex/Ch10.S1.SS1.html), for the conditional normal mean and variance. Diagram-specific interpretation and numerical checks are explanatory additions; the screenshot's originating interactive implementation was not supplied.

## Relation to the tower property

This is the no-information-retained special case of the nested-information tower property: take the outer sigma-algebra to be $\{\varnothing,\Omega\}$, where $\Omega$ is the sample space. Terminology overlaps: some sources also call this identity the tower property or law of iterated expectation. This page isolates the unconditional identity; the sibling Tower property page treats the general nested form.

**Source.** Jonathan Rougier, *APTS Notes on Statistical Inference* (2015), [§1.3.3, p. 15, equation (1.19), and §1.4, p. 17, (LIE)](https://warwick.ac.uk/fac/sci/statistics/apts/students/resources-1516/apts_si_prelim.pdf#page=15). Cross-check: Nicholas Georgiou and Hugo Lo, *APTS Applied Stochastic Processes* (2024; notes originally by Wilfrid Kendall), [§§2.7–2.8](https://maths.dur.ac.uk/users/nicholas.georgiou/ASP24/prelim/_book/expectation-and-probability.html#conditional-expectation-i-property-based-definition). Numerical illustration is an explanatory addition.

```atlas
```
