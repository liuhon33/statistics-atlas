---
id: learning-conditional-expectation-l2-projection
title: Conditional expectation as orthogonal projection in L2
layer: learning
primary_home: "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection]]"
subject: probability
backbone_path: Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → L2 conditional projection
study_band: U
note_types:
  - derivation
  - insight
  - question
question_roles:
  - cross-topic-connection
source_format: handwriting
created: 2026-11-08
updated: 2026-11-09
status: active
verification: checked
learning_state: unknown
aliases:
  - Geometry in L2
  - Geometry of conditional expectations
  - Hilbert-space view of conditional expectation
tags:
  - atlas/learning
  - subject/probability
  - topic/conditional-expectation
connections:
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation]]"
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property]]"
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Total variance]]"
  - "[[Backbone/Statistical inference & modeling/Inference foundations/Statistical reasoning/Sampling distributions/Mean squared error]]"
  - "[[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation]]"
sources:
  - "[[raw/conversations/2026-10-27-total-expectation-and-variance-group-intuition-excerpt]]"
  - "[[raw/assets/2026-11-08-L2-geometry-I01-conditional-expectation-projection-notes.png]]"
  - "[[assets/figures/2026-11-08-L2-geometry/I01-excerpt-geometry-in-L2.png]]"
  - "[[assets/figures/2026-11-08-L2-geometry/I01-excerpt-geometry-of-conditional-expectation.png]]"
  - "[[assets/figures/2026-11-08-L2-geometry/crop_diagrams.ps1]]"
---

# Conditional expectation as orthogonal projection in L2

Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Conditional expectation → L2 conditional projection

**Random variables with finite second moment form a Hilbert space, and in it averaging is projecting.** $\mathbb E[X]$ is the projection of $X$ onto the constants $\mathbf 1$, and $\mathbb E[X\mid Y]$ is the projection of $X$ onto all square-integrable functions of $Y$. The residual is perpendicular to that subspace. The law of total expectation and the "takes out what's given" rule both follow from this orthogonality, with no densities.

The sections below translate my handwritten page. Passages marked **Added** or **Completed by the assistant** are corrections or synthesis, not part of the page.

## Geometry in $L^2$

$$
H\equiv H(L^2,\Omega,P)=\{X:\Omega\to\mathbb R\text{ is a RV}\mid \mathbb E X^2<\infty\}
$$

$$
\langle X,Y\rangle=\mathbb E[XY]
$$

$$
\|X\|=\sqrt{\langle X,X\rangle}=\sqrt{\mathbb E[X^2]}
$$

$$
d(X,Y)=\|X-Y\|=\sqrt{\mathbb E[(X-Y)^2]}
$$

![[assets/figures/2026-11-08-L2-geometry/I01-excerpt-geometry-in-L2.png]]

*My drawing, cropped from the full page: $X$ projected onto the constant direction $\mathbf 1$, with the estimator MSE triangle overlaid in orange.*

In black, the horizontal axis is the constant random variable $\mathbf 1$. The foot of the dashed perpendicular from $X$ is $\mathbb E[X]$, and the dashed side is labelled

$$
\|X-\mathbb E[X]\|=\sqrt{\operatorname{Var}(X)}.
$$

In orange, the same right triangle is drawn for an estimator $\hat\theta$: hypotenuse $\sqrt{\operatorname{MSE}(\hat\theta)}$, side along $\mathbf 1$ labelled $\operatorname{Bias}(\hat\theta)$, and vertical side $\sqrt{\operatorname{Var}[\hat\theta]}$.

**Prop.** $X$ is r.v. $\mu:=\mathbb E[X]$ is the unique number s.t. minimize the function

$$
g(c):=\mathbb E[(X-c)^2].
$$

**Pf.**

$$
\begin{aligned}
g(c)&=\mathbb E[X^2]-2c\,\mathbb EX+c^2\\
g'(c)&=-2\,\mathbb EX+2c=0\\
c&=\mathbb E[X]
\end{aligned}
$$

$\mu:=\mathbb EX$ is the unique minimizer of $g$.

**Added: why the drawing is a projection.** Since $\|\mathbf 1\|^2=\mathbb E[1]=1$, the projection of $X$ onto the line through $\mathbf 1$ is $\langle X,\mathbf 1\rangle\mathbf 1=\mathbb E[X]\,\mathbf 1$. The residual is perpendicular: $\langle X-\mathbb E X,\mathbf 1\rangle=0$. The Prop says the same thing as a nearest point, because $g(c)=\|X-c\mathbf 1\|^2$. The minimum is unique because $g''(c)=2>0$. For the orange triangle, put the true value $\theta$ at the origin:

$$
\hat\theta-\theta=\underbrace{(\mathbb E\hat\theta-\theta)\,\mathbf 1}_{\text{along }\mathbf 1}+\underbrace{(\hat\theta-\mathbb E\hat\theta)}_{\perp\,\mathbf 1}
\quad\Longrightarrow\quad
\operatorname{MSE}(\hat\theta)=\operatorname{Bias}(\hat\theta)^2+\operatorname{Var}(\hat\theta).
$$

Adding the orthogonal noise leg gives the [[Learning/Statistical computing & learning/Statistical learning & prediction/Bias–variance decomposition as Pythagoras in L2#2. Three orthogonal pieces of the prediction error|prediction bias–variance decomposition]].

Strictly, elements of $L^2$ are classes of random variables that agree almost surely; otherwise $\|X\|=0$ would not force $X=0$.

## Defining the conditional expectation by minimum MSE

Motivate → $X,Y\in H(L^2,\Omega,P)\equiv H$.

Denote $\mathcal H_Y:=\{g(Y),\ g\in L^2\}$.

Define conditional expectation of $X$ given $Y$ as $g(Y)\in\mathcal H_Y$, s.t. MSE

$$
\mathbb E[(X-g(Y))^2]\ \text{ is minimized.}
$$

Subtle: minimize a thing over $\infty$-dim subspace requires functional analysis. $\mathcal H_Y$ is a closed subspace.

**Added.** "$g\in L^2$" means $\mathbb E[g(Y)^2]<\infty$ for a measurable $g$. Closedness is what the projection theorem needs: every closed subspace of a Hilbert space has a unique nearest point to each $X$ (unique up to almost-sure equality). So this definition always produces exactly one $\mathbb E[X\mid Y]$.

## Orthogonality characterizes the conditional expectation

**Prop.** The conditional expectation of $X$ given $Y$ is $g(Y)$ $\iff$ for any $h(Y)$,

$$
X-g(Y)\perp h(Y).
$$

**Pf.** $\phi(t):=\mathbb E\big[X-g(Y)-t\cdot h(Y)\big]^2$, $t$ minimizes.

($\Rightarrow$) By definition of $g$, $t=0$ minimizes. $g(Y)$ is conditional exp of $X$

$\Rightarrow$ $\mathbb E[X-g(Y)]^2$ is minimized

$\Rightarrow$ therefore $t=0$ minimizes $g$ *[read $\phi$]*

$$
\begin{aligned}
\Rightarrow\ \phi(t)&:=\mathbb E\big[(X-g(Y))-t\cdot h(Y)\big]^2\\
&=\mathbb E[X-g(Y)]^2-2t\,\mathbb E[(X-g(Y))h(Y)]+t^2\,\mathbb E[h^2(Y)]\\
\phi'(t)&=-2\,\mathbb E[(X-g(Y))h(Y)]+2t\,\mathbb E[h^2(Y)]
\end{aligned}
$$

$\Rightarrow$ $\phi'(0)=0$, since $\phi(t)$, $t=0$ minimize

$\Rightarrow$ $\mathbb E[(X-g(Y))h(Y)]=0$

$\Rightarrow$ $X-g(Y)\perp h(Y)$

($\Leftarrow$) *Completed by the assistant; the page proves only ($\Rightarrow$). Same $\phi$, read the other way.*

Assume $g(Y)\in\mathcal H_Y$ and $X-g(Y)\perp h(Y)$ for every $h(Y)\in\mathcal H_Y$. Take any competitor $k(Y)\in\mathcal H_Y$, and set

$$
h(Y):=k(Y)-g(Y)\in\mathcal H_Y
\qquad(\mathcal H_Y\text{ is a subspace}).
$$

Then $X-k(Y)=\big(X-g(Y)\big)-1\cdot h(Y)$, so $\mathbb E[X-k(Y)]^2=\phi(1)$ and $\mathbb E[X-g(Y)]^2=\phi(0)$.

$$
\begin{aligned}
\phi(t)&=\mathbb E[X-g(Y)]^2-2t\,\underbrace{\mathbb E[(X-g(Y))h(Y)]}_{=\,0\ \text{by}\ \perp}+t^2\,\mathbb E[h^2(Y)]\\
&=\mathbb E[X-g(Y)]^2+t^2\,\mathbb E[h^2(Y)]\\
&\ge\mathbb E[X-g(Y)]^2=\phi(0)
\end{aligned}
$$

$\Rightarrow$ $\phi(1)\ge\phi(0)$, i.e. $\mathbb E[X-k(Y)]^2\ge\mathbb E[X-g(Y)]^2$ for every $k(Y)\in\mathcal H_Y$

$\Rightarrow$ $g(Y)$ minimizes the MSE over $\mathcal H_Y$

$\Rightarrow$ $g(Y)$ is the conditional expectation of $X$ given $Y$. $\blacksquare$

Equality $\phi(1)=\phi(0)$ forces $\mathbb E[h^2(Y)]=0$, i.e. $k(Y)=g(Y)$ almost surely, so the minimizer is also unique. Geometrically, $\phi(1)=\phi(0)+\mathbb E[h^2(Y)]$ is Pythagoras: $\|X-k(Y)\|^2=\|X-g(Y)\|^2+\|g(Y)-k(Y)\|^2$.

The finite-sample counterpart is the [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation#2. The cosine route finds the nearest point geometrically|OLS nearest-point argument]].

**Added: notation.** On the page, $\mathbb E[\cdot]^2$ means $\mathbb E[(\cdot)^2]$, and "for any $h(Y)$" means any $h(Y)\in\mathcal H_Y$. Corollary 1 uses ($\Rightarrow$); Corollary 2 and the tower argument use ($\Leftarrow$).

## Geometry of conditional expectations

![[assets/figures/2026-11-08-L2-geometry/I01-excerpt-geometry-of-conditional-expectation.png]]

*My drawing, cropped from the full page: $X$, its projection $\mathbb E[X\mid Y]$ onto the plane $\mathcal H_Y$, and $\mathbb E(X)$ on the line $\mathbf 1$ inside the plane.*

The blue plane is $\mathcal H_Y$ and the blue line $\mathbf 1$ lies in it. $\mathbb E[X\mid Y]$ is the foot of the perpendicular from $X$ to the plane. The red shaded triangle $X$, $\mathbb E(X)$, $\mathbb E[X\mid Y]$ is labelled "is right angle", with the right angle at $\mathbb E[X\mid Y]$. Its sides are $\sqrt{\operatorname{Var}(X)}$ (purple, from $\mathbb E(X)$ to $X$), $\sqrt{\operatorname{Var}(\mathbb E[X\mid Y])}$ (orange, from $\mathbb E[X\mid Y]$ to $\mathbb E(X)$), and the side from $\mathbb E[X\mid Y]$ to $X$, which I marked $?$. Pythagoras then reads

$$
\boxed{\big[\sqrt{\operatorname{Var}(X)}\big]^2=\sqrt{\operatorname{Var}(\mathbb E[X\mid Y])}^{\,2}+\sqrt{\mathbb E[\operatorname{Var}(X\mid Y)]}^{\,2}}
$$

that is, the law of total variance:

$$
\operatorname{Var}(X)=\operatorname{Var}(\mathbb E[X\mid Y])+\mathbb E[\operatorname{Var}(X\mid Y)].
$$

On the page the last term was $?^2$. **My question, paraphrased from the drawing:** what length is the side marked $?$?

**Completed by the assistant: $?=\sqrt{\mathbb E[\operatorname{Var}(X\mid Y)]}$.** Write $g(Y)=\mathbb E[X\mid Y]$ and use the conditional variance $\operatorname{Var}(X\mid Y):=\mathbb E\big[(X-\mathbb E[X\mid Y])^2\mid Y\big]$.

The $?$ side is the residual:

$$
\begin{aligned}
?^2&=\|X-\mathbb E[X\mid Y]\|^2=\mathbb E\big[(X-\mathbb E[X\mid Y])^2\big]\\
&=\mathbb E\Big[\mathbb E\big[(X-\mathbb E[X\mid Y])^2\mid Y\big]\Big]
&&\text{(law of total expectation)}\\
&=\mathbb E[\operatorname{Var}(X\mid Y)]
&&\text{(definition of conditional variance)}
\end{aligned}
$$

The middle step is the law of total expectation for $Z=(X-\mathbb E[X\mid Y])^2$. $Z$ is integrable but need not be square-integrable, so this step uses the general version of the law (for integrable variables), not the $L^2$ proof in Corollary 1.

The orange side uses Corollary 1 once more, $\mathbb E[\mathbb E[X\mid Y]]=\mathbb E[X]$:

$$
\|\mathbb E[X\mid Y]-\mathbb E[X]\|^2=\mathbb E\Big[\big(\mathbb E[X\mid Y]-\mathbb E\big[\mathbb E[X\mid Y]\big]\big)^2\Big]=\operatorname{Var}(\mathbb E[X\mid Y]).
$$

The right angle comes from the orthogonality Prop ($\Rightarrow$): $\mathbb E[X\mid Y]-\mathbb E[X]=h(Y)$ with $h(y)=g(y)-\mathbb E[X]$, which lies in $\mathcal H_Y$. So the cross term vanishes when the purple side is split at $\mathbb E[X\mid Y]$:

$$
\begin{aligned}
\operatorname{Var}(X)=\|X-\mathbb E[X]\|^2
&=\big\|\big(X-\mathbb E[X\mid Y]\big)+\big(\mathbb E[X\mid Y]-\mathbb E[X]\big)\big\|^2\\
&=\underbrace{\|X-\mathbb E[X\mid Y]\|^2}_{?^2=\mathbb E[\operatorname{Var}(X\mid Y)]}
+2\underbrace{\mathbb E\big[(X-\mathbb E[X\mid Y])\,h(Y)\big]}_{=\,0}
+\underbrace{\|\mathbb E[X\mid Y]-\mathbb E[X]\|^2}_{\operatorname{Var}(\mathbb E[X\mid Y])}.
\end{aligned}
$$

In words, the $?$ side is the spread of $X$ left over after conditioning on $Y$, averaged over $Y$. The orange side is how much the group means themselves vary.

### Group intuition and a small example

Let $Y$ label nonoverlapping groups and $X$ be a uniformly chosen person's score. **Total expectation** averages the group means, weighted by each group's population share. **Total variance** adds the weighted average of within-group variances to the weighted variance of the group means.

| Group | Population share | Mean score | Within-group variance |
| --- | ---: | ---: | ---: |
| A | 20% | 60 | 25 |
| B | 80% | 80 | 25 |

Using population variances,
$$
\begin{aligned}
\mu=\mathbb E[X]&=0.2(60)+0.8(80)=76,\\
\text{within}&=0.2(25)+0.8(25)=25,\\
\text{between}&=0.2(60-76)^2+0.8(80-76)^2=64.
\end{aligned}
$$
Thus $\operatorname{Var}(X)=25+64=89$. To picture the between-group term, replace every score with its group's mean: 20% of people now score 60 and 80% score 80. Their variance is 64. In the triangle above, 64 is the orange side squared and 25 is the residual side squared.

## Corollary 1: $\mathbb E[\mathbb E[X\mid Y]]=\mathbb E[X]$

**Pf.** Pick $h\equiv 1$. $g(Y)$ is $\mathbb E[X\mid Y]$.

$$
\begin{aligned}
&\mathbb E[(X-g(Y))\,h(Y)]=0\\
\Rightarrow\ &\mathbb E[(X-\mathbb E[X\mid Y])\,1]=0\\
\Rightarrow\ &\mathbb E[X]-\mathbb E[\mathbb E[X\mid Y]\,1]=0
\end{aligned}
$$

**Added: the general tower property is nested projection.** Information $Y$ is contained in information $(Y,Z)$, so $\mathcal H_Y\subseteq\mathcal H_{Y,Z}$. For any $h(Y)\in\mathcal H_Y$,

$$
\mathbb E\big[(\mathbb E[X\mid Y,Z]-\mathbb E[X\mid Y])\,h(Y)\big]
=\mathbb E\big[(\mathbb E[X\mid Y,Z]-X)\,h(Y)\big]+\mathbb E\big[(X-\mathbb E[X\mid Y])\,h(Y)\big]=0+0.
$$

The first term vanishes because $h(Y)$ also lies in the larger space $\mathcal H_{Y,Z}$. By ($\Leftarrow$), $\mathbb E[\mathbb E[X\mid Y,Z]\mid Y]=\mathbb E[X\mid Y]$: projecting onto the big subspace and then onto the small one is the same as projecting onto the small one directly. Corollary 1 is the case where the small subspace is the line $\mathbf 1$.

## Corollary 2: takes out what's given rule

$$
\mathbb E[h(Y)X\mid Y]=h(Y)\,\mathbb E[X\mid Y]
$$

Suffices to check $\forall g\in\mathcal H_Y$:

$$
\underbrace{h(Y)\mathbb E[X\mid Y]-h(Y)X}_{①}\ \perp\ \underbrace{g(Y)}_{②}
$$

$h(Y)\mathbb E[X\mid Y]$ is marked "projection". This means that $h(Y)X$ is the conditional expectation given $Y$. Arrows on the page send $h(Y)X$ to the left side and $h(Y)\mathbb E[X\mid Y]$ to the right side of

$$
\mathbb E[h(Y)X\mid Y]=h(Y)\,\mathbb E[X\mid Y].
$$

**Pf.**

$$
\mathbb E\Big[\underbrace{(\mathbb E[X\mid Y]-X)}_{\text{perpendicular}}\ \underbrace{h(Y)\,g(Y)}_{\in\mathcal H_Y}\Big]=0
$$

This expectation is the inner product of ① and ②.

**Added: reading and assumption.** The blue sentence means that $h(Y)\mathbb E[X\mid Y]$ is the conditional expectation of $h(Y)X$ given $Y$, as the arrows show. The check uses ($\Leftarrow$) from the orthogonality Prop. It needs $h(Y)X$ in $L^2$ and $h(Y)g(Y)$ in $\mathcal H_Y$. Both hold when $h$ is bounded. For unbounded $h$, the rule still holds when $X$ and $h(Y)X$ are integrable, but the proof then needs the general (non-$L^2$) definition of conditional expectation.

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation|Law of total expectation]] — Corollary 1 proves this identity by orthogonality with $h\equiv1$, a third route besides the density integrals and group means on that page.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property|Tower property]] — Nested information gives nested closed subspaces, and the tower property becomes "project onto the larger subspace, then the smaller, equals projecting onto the smaller".
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Total variance|Total variance]] — The right triangle in my conditional-expectation drawing is the total-variance decomposition, and the side I marked $?$ is $\sqrt{\mathbb E[\operatorname{Var}(X\mid Y)]}$.
- [[Backbone/Statistical inference & modeling/Inference foundations/Statistical reasoning/Sampling distributions/Mean squared error|Mean squared error]] — My orange overlay reads $\operatorname{MSE}=\operatorname{Bias}^2+\operatorname{Var}$ as Pythagoras: the bias lies along $\mathbf 1$ and the fluctuation is perpendicular to it.
- [[Learning/Statistical inference & modeling/Regression & linear models/Three routes from least squares to slope and correlation|Three routes from least squares to slope and correlation]] — The same geometry in sample space: centering removes the projection onto $\mathbf 1$, and the OLS residual is perpendicular to the fitted subspace, just as $X-\mathbb E[X\mid Y]$ is perpendicular to $\mathcal H_Y$.

## Origin

> [!info]- Source details
> All definitions, propositions, proofs, both drawings, the colour-coded Pythagoras equation and its $?$ are from my handwritten page, supplied 2026-11-08. Only the two drawings are shown as images. They are cropped from the [[raw/assets/2026-11-08-L2-geometry-I01-conditional-expectation-projection-notes.png|full original page]], which stays unchanged in `raw/` and can be reproduced with [[assets/figures/2026-11-08-L2-geometry/crop_diagrams.ps1|the crop script]]. Everything else is transcribed. The bracketed *[read $\phi$]* marks a slip on the page ("minimizes $g$" where $\phi$ is meant). Two parts were completed by the assistant at my request: the ($\Leftarrow$) direction of the orthogonality proof, and the value of the $?$ in the boxed Pythagoras equation, with its derivation. The "Added" passages are also assistant contributions: the projection reading of the first drawing, the closed-subspace remark, the notation note, the nested-projection tower argument, and the boundedness condition for Corollary 2. There is no separate backbone page for the takes-out-what's-given rule, so it has no connection.
>
> Group intuition and numerical example added 2026-11-09 from [[raw/conversations/2026-10-27-total-expectation-and-variance-group-intuition-excerpt]]: the subgroup-averaging intuition is the user's (U01); the weighting clarification and 20%/80% example are the assistant's (A01).
