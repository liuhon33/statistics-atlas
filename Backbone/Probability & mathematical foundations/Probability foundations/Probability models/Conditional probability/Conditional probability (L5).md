---
id: cond-events-conditional-probability
title: Conditional probability
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Conditional probability
created: '2026-11-08'
updated: '2026-11-09'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional probability (L4)]]'
sources:
- '[[_system/Sources/prob]]'
- '[[raw/assets/2026-11-08-total-expectation-I01-joint-density-slices.png]]'
---

# Conditional probability

Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Conditional probability

Parent: [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Conditional probability (L4)|Conditional probability]]

## Definition: restrict, then normalize

For events $A,B$ with $P(B)>0$,

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}.
$$

Knowing $B$ occurred restricts attention to $B$; division by $P(B)$ makes that restricted world have total probability one.

## Reading the density slices

![[raw/assets/2026-11-08-total-expectation-I01-joint-density-slices.png]]


For jointly continuous $X,Y$, write $p(x,y)$ for their joint density and $p_Y(y)=\int p(x,y)\,dx$ for the marginal density. Where $0<p_Y(y_0)<\infty$,

$$
p_{X\mid Y}(x\mid y_0)=\frac{p(x,y_0)}{p_Y(y_0)},
\qquad
P(a\le X\le b\mid Y=y_0)=\int_a^b p_{X\mid Y}(x\mid y_0)\,dx.
$$

- **Gray surface:** joint density; probabilities are volumes over regions of the $x,y$ plane.
- **Teal slice:** fixing $y_0$ leaves a curve in $x$. Its raw area is $p_Y(y_0)$, the corresponding **purple marginal height**, not one. Dividing by this area gives the unit-area conditional density in the upper-right panel.
- **Coral slice:** reverse the roles: fix $x_0$, then divide by $p_X(x_0)$ to obtain a density in $y$. The two conditionals answer different questions.

**Continuous-variable caution:** $p_Y(y_0)$ is a density, not $P(Y=y_0)$, which is zero. The density ratio is not division by that zero probability; for smooth densities it is understood through conditioning on shrinking intervals around $y_0$. Normalization rescales vertically—it need not always stretch.

## What it is used for

**Prediction after observing a variable.** In the displayed standardized jointly Gaussian model, $\rho=0.8$ and

$$
X\mid Y=-1.3\sim N(-1.04,0.36),
\qquad
Y\mid X=1\sim N(0.80,0.36),
$$

where the second parameter is variance. Observing $Y=-1.3$ shifts the predicted mean of $X$ from $0$ to $-1.04$ and reduces its standard deviation from $1$ to $0.6$. Integrating the teal conditional curve over a range gives the probability that $X$ falls in that range **given the observation**. Its balance point is the regression prediction $\mathbb E[X\mid Y=y]$; the linear mean and constant conditional variance here rely on joint Gaussianity, not on conditioning alone.

**Sources:** Hossein Pishro-Nik, *Introduction to Probability, Statistics, and Random Processes*, [§5.2.3, Conditioning by Another Random Variable](https://www.probabilitycourse.com/chapter5/5_2_3_conditioning_independence.php), for the event and density formulas; Lancaster University, *MATH230*, [§10.1.1, Conditional Distributions](https://www.lancaster.ac.uk/~prendivs/accessible/math230/math230_notes.tex/Ch10.S1.SS1.html), for the Gaussian formulas and regression interpretation. Screenshot-specific color interpretation and numerical substitution are explanatory additions.

```atlas
```
