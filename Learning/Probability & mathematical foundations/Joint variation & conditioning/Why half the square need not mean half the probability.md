---
id: learning-event-regions-density-volumes
title: Why half the square need not mean half the probability
layer: learning
primary_home: "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Joint CDF and density]]"
subject: probability
backbone_path: "Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Marginal & conditional laws → Joint CDF and density"
study_band: U
note_types: [question, derivation, insight]
question_roles: [concept-distinction, reconcile-approaches, cross-topic-connection]
source_format: conversation-pdf
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
learning_state: practicing
aliases: [Event regions and density volumes, Uniform product probability, Two thirds by density volume]
tags: [atlas/learning, subject/probability, topic/joint-density, study/undergraduate]
connections:
  - "[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Random variables & distribution functions/Support and event regions]]"
  - "[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/CDF transformation method]]"
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property]]"
sources:
  - "[[raw/conversations/2026-10-18-Clarify-Probability-Error.pdf]]"
  - "[[raw/conversations/2026-10-18-Clarify-Probability-Error-manifest.json]]"
  - "[[raw/conversations/2026-10-18-Clarify-Probability-Error-reference.json]]"
  - "[[assets/figures/2026-11-08-probability-regions/pdf-p05-corrected-event-region.png]]"
---

# Why half the square need not mean half the probability

**Original problem:** For independent $X,Y,Z\sim U(0,1)$, find $P(X\leq YZ)$. Let $W=YZ$.

**Follow-up exercise:** If $X\sim U(0,1)$ is independent of a new $W$ with density $f_W(w)=2w$ on $[0,1]$ (zero elsewhere), find $P(X\leq W)$.

Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Marginal & conditional laws → Joint CDF and density

**The event chooses the region; the density supplies its weight.** The triangle $0\leq x\leq w\leq1$ occupies half a unit square. Its probability is $1/4$ when $W$ is the product of two independent uniforms, but $2/3$ when $W$ has density $2w$. In both examples, $X$ is uniform on $[0,1]$ and independent of $W$.

My square construction, correction of the diagonal, and later volume argument connect three ways to calculate the same probability: integrate over a region, measure the solid under a density, or condition on a random threshold.

## 1. My square was useful; the boundary compares values

**My question**, from the archived conversation, p. 1:

> and I draw out the boundary where pdf(x) = pdf (yz) and I calculate the area where pdf(x) is smaller than pdf(yz)?

The distinction is between the random variable $W$, a possible value $w$, and the density height $f_W(w)$. The event $X\leq W$ compares the values $x$ and $w$, so its boundary is $x=w$. Equating density heights would define a different region.

With horizontal coordinate $w$ and vertical coordinate $x$, the line rises from $(0,0)$ to $(1,1)$, and the desired region is below it. I caught the assistant's descending diagonal in the original diagram:

> I think your previous boundary might be wrong? I think the boundary should be from lower left to top right?

Source: PDF p. 5. The corrected diagram is:

![[assets/figures/2026-11-08-probability-regions/pdf-p05-corrected-event-region.png]]

*Diagram extracted from the assistant's corrected figure on PDF p. 5; the archived PDF is unchanged. The green triangle is the event $X\leq W$. Its area is $1/2$; the density determines its probability.*

For a joint density $f_{X,W}$ and a measurable region $A$, probability is

$$
P((X,W)\in A)=\iint_A f_{X,W}(x,w)\,dx\,dw.
$$

Here $A=\{(x,w):0\leq x\leq w\leq1\}$. Ordinary area works directly when the joint density is $1$ on the unit square. A varying density requires weighting each part of the triangle.

## 2. Product threshold: derive the density, then integrate

The original conversation states $f_W(w)=-\ln w$. The following CDF calculation, added during the earlier digest, explains where it comes from.

For $0<w<1$, condition on $Z=z$. If $z\leq w$, every value of $Y$ satisfies $Yz\leq w$. If $z>w$, we need $Y\leq w/z$, which has probability $w/z$. Therefore

$$
F_W(w)=P(YZ\leq w)
=\int_0^w1\,dz+\int_w^1\frac{w}{z}\,dz
=w-w\ln w.
$$

Extend this CDF by $0$ for $w\leq0$ and $1$ for $w\geq1$. Differentiating on $(0,1)$ gives

$$
f_W(w)=-\ln w.
$$

The logarithm is natural. This density diverges as $w\downarrow0$, but its integral is $1$; endpoint density values do not affect probabilities. The variable $YZ$ has this density: it has not been replaced by $-\ln(YZ)$.

Because $X$ is independent of $(Y,Z)$, it is independent of their product. Thus the joint density is $-\ln w$ on the unit square, and

$$
\begin{aligned}
P(X\leq YZ)
&=\int_0^1\int_0^w-\ln w\,dx\,dw\\
&=\int_0^1-w\ln w\,dw\\
&=\left[-\frac{w^2}{2}\ln w+\frac{w^2}{4}\right]_0^1
=\boxed{\frac14}.
\end{aligned}
$$

The lower endpoint is a limit, with $w^2\ln w\to0$. The probability differs from the triangle's area because the product is concentrated toward small $w$, where the allowed vertical interval $0\leq x\leq w$ is short.

## 3. My volume argument for the increasing-density example

The second exercise changes the threshold distribution: $X\sim U(0,1)$ is independent of a new $W$ with density $f_W(w)=2w$ for $0\leq w\leq1$, and zero elsewhere. Find $P(X\leq W)$. The assistant proposed this exercise on PDF p. 4.

**My insight, paraphrased from p. 6:** I pictured the solid under the joint density as half a rectangular box and compared volumes instead of integrating, obtaining $2/3$.

Introduce a height coordinate $h$ for density. It is a geometric coordinate, not another random variable. Independence gives the full solid

$$
S=\{(x,w,h):0\leq x\leq1,\ 0\leq w\leq1,\ 0\leq h\leq2w\}.
$$

For each $x$, its $(w,h)$ cross-section is a triangle of base $1$ and height $2$. Extending that triangle over a unit length in $x$ makes a triangular prism, with volume

$$
V_{\mathrm{total}}=\frac12(1)(2)(1)=1.
$$

This agrees with my half-box picture: the enclosing $1\times1\times2$ box has volume $2$.

To find the desired part, remove the part above $X>W$. Its closure is a tetrahedron with vertices, in $(x,w,h)$ order,

$$
A=(0,0,0),\quad B=(1,0,0),\quad
C=(1,1,0),\quad D=(1,1,2).
$$

The base triangle $ABC$ has area $1/2$ and the perpendicular height from $D$ is $2$. Its volume is

$$
V_{\mathrm{excluded}}=\frac13\left(\frac12\right)(2)=\frac13,
\qquad
P(X\leq W)=1-\frac13=\boxed{\frac23}.
$$

The correction to my original shape description is that the **excluded** part is the tetrahedron. The desired part is the remainder of the prism. The tetrahedron occupies one sixth of the box; the desired remainder occupies one third of the box, or two thirds of the full density solid. The boundary has probability zero.

### The same solid, sliced in either order

Fix $w$. The desired slice has width $w$ in the $x$ direction and density height $2w$, so its cross-sectional area is $2w^2$:

$$
P(X\leq W)
=\int_0^1\int_0^w2w\,dx\,dw
=\int_0^12w^2\,dw=\frac23.
$$

Fixing $x$ instead, the allowed threshold values run from $x$ to $1$:

$$
P(X\leq W)
=\int_0^1\int_x^12w\,dw\,dx
=\int_0^1(1-x^2)\,dx=\frac23.
$$

Both integrals accumulate the same nonnegative density over the same triangle. The two orders correspond to different slices of the volume, connecting the integral calculation to my geometric argument.

## 4. Conditioning explains both answers at once

If $X\sim U(0,1)$ is independent of a threshold $W$ taking values in $[0,1]$, then at a fixed threshold $w$,

$$
P(X\leq W\mid W=w)=P(X\leq w)=w.
$$

Using the tower property on the bounded event indicator gives

$$
P(X\leq W)
=E[\mathbf1_{\{X\leq W\}}]
=E\!\left[E[\mathbf1_{\{X\leq W\}}\mid W]\right]
=\boxed{E[W]}.
$$

Here $E$ denotes expectation under the joint model. The threshold need not have a density.

| Threshold model | Conditional probability at $W=w$ | Result |
| --- | --- | --- |
| $W=YZ$, with $Y,Z$ independent uniforms | $w$ | $E[YZ]=E[Y]E[Z]=1/4$ |
| $f_W(w)=2w$ on $[0,1]$ | $w$ | $E[W]=\int_0^1w(2w)\,dw=2/3$ |
| $W\sim U(0,1)$ | $w$ | $E[W]=1/2$ |

Independence of $X$ from the threshold makes the conditional probability equal $w$. In the product example, independence of $Y$ and $Z$ separately justifies factoring $E[YZ]$.

This is the shortest alternative to the geometric calculation: at each fixed threshold $w$, a uniform $X$ falls below it with probability $w$, so average those thresholds. In particular, the product problem needs neither the CDF nor the density of $YZ$: $P(X\leq YZ)=E[Y]E[Z]=(1/2)(1/2)=1/4$.

The earlier digest added two useful limits of this shortcut. For arbitrary independent real $X,W$,

$$
P(X\leq W)=E[F_X(W)],
$$

where $F_X(t)=P(X\leq t)$ is the CDF of $X$. For uniform $X$ and an unrestricted real threshold, this is $E[\min(1,\max(0,W))]$. Independence matters: if $W=X\sim U(0,1)$, then $P(X\leq W)=1$ while $E[W]=1/2$.

## 5. An integration-free alternative: represent the threshold as a maximum

For the increasing-density exercise, $f_W(w)=2w$ suggests a different construction. Take $X,U,V$ to be three independent $U(0,1)$ variables and define $M=\max(U,V)$. For $0\leq w\leq1$,

$$
P(M\leq w)=P(U\leq w,\ V\leq w)=w^2.
$$

Differentiating gives $f_M(w)=2w$ on $(0,1)$, the same density as $W$. Also, $M$ is independent of $X$. Thus $(X,M)$ has the same joint distribution as the original independent pair $(X,W)$, so we can calculate the desired probability using $M$. This is a distributional representation, not a claim that the original $W$ literally came from two uniforms.

Now $X>M$ means that $X$ is the largest of the three uniforms. Because their joint law is unchanged by permuting their labels, each variable has the same probability of being largest. Ties have probability zero, and exactly one variable is largest, so each probability is $1/3$. Therefore

$$
P(X\leq W)=P(X\leq M)
=1-P(X>\max(U,V))
=1-\frac13=\boxed{\frac23}.
$$

My volume approach identifies an excluded tetrahedron of volume $1/3$. This alternative identifies an excluded ranking event of probability $1/3$. They reach the same answer through different structures: **geometric volume versus permutation symmetry**. Unlike conditioning in section 4, this particular symmetry argument solves the $2w$ example, not the product-threshold problem.

## Connections

- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Random variables & distribution functions/Support and event regions|Support and event regions]] — The inequality between values determines the triangle and its integration limits before any density is used.
- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/CDF transformation method|CDF transformation method]] — Conditioning on one factor derives the product's CDF and then its density, explaining the weight in the first integral.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property|Tower property]] — Averaging the conditional event indicator turns both region calculations into the mean of the threshold.

## Origin

The 2026-11-09 follow-up added the assistant's maximum-and-ranking solution in section 5 and clarified the existing conditioning shortcut in section 4, at my request. These are assistant explanations, not additional original work attributed to me. Verification checked the maximum's CDF and density, independence from $X$, equality of the joint laws, and the equal-probability, zero-tie ranking argument.

Migrated from the already-digested [[raw/conversations/2026-10-18-Clarify-Probability-Error.pdf|Clarify Probability Error export]], pp. 1–11. My contributions are the unit-square proposal, the corrected diagonal on p. 5, and the box/volume argument on p. 6. The CDF derivation, exact tetrahedron coordinates, general CDF identity, and independence counterexample are checked additions from the earlier digest. Routine requests remain in the PDF without becoming questions here.

Verification checked the CDF and normalization, endpoint limits, both integration orders, the tetrahedron volume, and the conditional-expectation proof. The PDF preserves the original erroneous p. 3 diagram; the displayed extraction uses its corrected p. 5 version. The [[raw/conversations/2026-10-18-Clarify-Probability-Error-manifest.json|source manifest]] records the export's identity and coverage; [[assets/figures/2026-11-08-probability-regions/extract_diagram.py|the extraction script]] reproduces the displayed figure.
