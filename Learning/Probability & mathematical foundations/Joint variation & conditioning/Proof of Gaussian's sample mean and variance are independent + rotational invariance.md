---
id: learning-density-slices-rotational-invariance
title: Density slices, independence, and rotational invariance
layer: learning
primary_home: "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Conditional density]]"
subject: probability
backbone_path: "Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Marginal & conditional laws → Conditional density"
study_band: U
note_types: [question, insight, derivation]
question_roles: [concept-distinction, assumption-boundary, cross-topic-connection]
source_format: conversation
created: 2026-11-08
updated: 2026-11-12
status: active
verification: checked
learning_state: practicing
aliases: [Density hill and moving board, Rotational invariance versus independence]
tags: [atlas/learning, subject/probability, topic/conditioning, study/undergraduate]
connections:
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Independence versus zero covariance]]"
  - "[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian linear transformations]]"
  - "[[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Sample statistics & order/Sample mean and variance]]"
  - "[[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic]]"
sources:
  - "[[raw/notes/2026-11-09-Statistics-is-just-Geometry-auto-captions.txt]]"
  - "[[raw/conversations/2026-11-04-density-slices-rotation-side-chat-excerpts]]"
  - "[[raw/conversations/2026-11-04-density-slices-rotation-side-chat-manifest.json]]"
  - "[[raw/assets/2026-11-04-conditional-density-denominator.png]]"
  - "[[raw/assets/2026-11-08-normal-sample-I01-projection-video.png]]"
  - "https://www.youtube.com/watch?v=KgqwRQowFLo&t=7s"
  - "https://online.stat.psu.edu/stat414/Lesson26"
---

This note grew out of my questions about the proof of the following theorem:

**If $X_1,\ldots,X_n$ are independent observations from the same Gaussian distribution, with $n\geq2$, then the sample mean $\bar X$ and sample variance $S^2$ are independent.**

A key step in the geometric proof uses the **rotational invariance of the joint standardized sample vector**. Briefly, the [video's proof (key step at 7:38)](https://www.youtube.com/watch?v=KgqwRQowFLo&t=458s) goes as follows:

1. **Standardize:** write $X_i=\mu+\sigma Z_i$, where the $Z_i$ are independent $N(0,1)$ variables and $\sigma>0$.
2. **Rotate:** for two observations, use $U=(Z_1+Z_2)/\sqrt2$ and $V=(Z_2-Z_1)/\sqrt2$. The joint density depends only on $Z_1^2+Z_2^2$, so rotating the axes leaves the joint law unchanged. Thus $U,V$ are still **independent standard normals**, not merely perpendicular coordinates.
3. **Separate the statistics:** since $\bar X=\mu+\sigma U/\sqrt2$ and $S^2=\sigma^2V^2$, the mean depends only on $U$, and the variance only on $V$. Functions of independent coordinates are independent.

For general $n$, the same argument uses one coordinate along $(1,\ldots,1)/\sqrt n$ for the mean and $n-1$ perpendicular coordinates for the residuals; the variance is proportional to the sum of their squares. Rotational invariance again makes these coordinates independent. Understanding this step—and how rotational invariance relates to independence and density slices—is what motivated this note.

# Density slices, independence, and rotational invariance

Probability & mathematical foundations → Joint variation & conditioning → Joint distributions → Marginal & conditional laws → Conditional density

**Independence means that moving a slice leaves its entire normalized density unchanged.** Rotational invariance means that rotating the whole distribution leaves its joint law unchanged. A circularly symmetric density can satisfy the second property while failing the first.

**My question:** Why do the sum-and-difference coordinates of independent standard normals stay independent when chords through a circle change length, and how does sliding a slice differ from rotating the distribution?

## My Question: why rotating the axes leaves the joint law unchanged for Gaussian?

 The screenshot below is the picture I wanted to understand: a sample vector is resolved along two perpendicular diagonal directions, and the text then invokes the rotational invariance of the joint standard-normal density.

![[raw/assets/2026-11-08-normal-sample-I01-projection-video.png]]

*The blue arrow is one realization of the two-observation vector $Z=(Z_1,Z_2)^\top$, not a density height; the dashed lines locate its projections onto the diagonal axes.*

With the displayed directions $e_1=(1,1)^\top/\sqrt2$ and $e_2=(-1,1)^\top/\sqrt2$, the signed coordinates are

$$
U=e_1^\top Z=\frac{Z_1+Z_2}{\sqrt2},\qquad
V=e_2^\top Z=\frac{Z_2-Z_1}{\sqrt2},\qquad
Z=Ue_1+Ve_2.
$$

**Sign convention:** the screenshot labels the second coordinate with $Z_1-Z_2$, the opposite sign to the displayed $e_2$. This note uses $Z_2-Z_1$ consistently. Reversing both that axis and its coordinate changes neither the projection vector nor the conclusions about independence and $V^2$.

For two observations, the projection $Ue_1=(\bar Z,\bar Z)^\top$ is the **mean vector**, while $Ve_2=(Z_1-\bar Z,Z_2-\bar Z)^\top$ is the **residual vector**. They are perpendicular for every sample, regardless of its distribution. The sample mean is $\bar Z=U/\sqrt2$; the sample variance is the squared residual length, $S_Z^2=V^2$. Variance is not itself the signed coordinate $V$.

The extra probabilistic step is that an iid standard-normal pair has the same joint law in these rotated coordinates, so $U,V$ are still independent standard normals. Functions of independent coordinates remain independent, giving $\bar Z\perp\!\!\!\perp S_Z^2$. More generally, iid sampling from $N(\mu,\sigma^2)$ gives independent sample mean and sample variance; see [Penn State STAT 414, §26.3](https://online.stat.psu.edu/stat414/Lesson26). Rotational invariance here belongs to the **joint standardized sample vector**, not to an arbitrary pair of normal variables.

This separates the two claims I need to keep apart: **perpendicular mean/residual vectors are geometry; independent mean/variance statistics require a distributional argument.** To see exactly where that argument succeeds or fails, I can lift many sample points into a density hill and examine its slices. That is the bridge from the video's diagram to my moving-board picture below.

## My hill and moving-board insight


Think about a probability density distribution on a 2D plane.

> even though each area is different, but if you compare the shape (normalized one) it does not depend on where you move the board right?

The board fixes one coordinate, say $U=u$, while the other coordinate $v$ varies. It traces the curve $v\mapsto f_{U,V}(u,v)$. The area under that curve can vary with $u$; independence asks whether dividing out that area leaves the **same curve** each time. This is my geometric insight; the equations below make its conditions explicit.

## Normalize a slice to get a conditional density

Let $U,V$ be real random variables with a joint density $f_{U,V}\geq0$ that integrates to one over $\mathbb R^2$. Holding $u$ fixed and integrating out the second coordinate gives the marginal density

$$
f_U(u)=\int_{-\infty}^{\infty}f_{U,V}(u,t)\,dt.
$$

Here $t$ is a dummy variable for the second coordinate. At $u$ with $0<f_U(u)<\infty$, a conditional density is

$$
\boxed{f_{V\mid U}(v\mid u)=\frac{f_{U,V}(u,v)}{f_U(u)}.}
$$

![[assets/figures/density-slices-gaussian-unit-square/gaussian-vs-unit-square.png]]

*Original illustration by Codex: sampled 2D points are lifted to their exact joint-density heights, with colored vertical cross-sections and their normalized densities below. Height is density. Gaussian slices normalize to the same curve; diagonal slices of a uniform square change width, so normalization cannot make them identical.*

The right panel uses the **unit square $[0,1]^2$**, viewed in centered diagonal coordinates $u=(x+y-1)/\sqrt2$, $v=(y-x)/\sqrt2$. Its density is one on the diamond $|u|+|v|\leq1/\sqrt2$. The square derivation below uses $[-1,1]^2$ instead: this is the same example translated and scaled by two, with density $1/4$ and diamond radius $\sqrt2$. In either case, the original axis-aligned coordinates are independent, but the diagonal coordinates are not. [[Conditional probability (L5)|See this about conditional probability intuition.]]


The slice area $f_U(u)$ is a **density**. Density values and slice areas can exceed one. If $U,V$ carry units, joint density has inverse-product units, the marginal has inverse-$U$ units, and the conditional density has inverse-$V$ units.

Dividing by the slice area makes the conditional density integrate to one. It also gives the defining averaging identity: for measurable sets $A,B\subseteq\mathbb R$,

$$
\begin{aligned}
P(U\in A,V\in B)
&=\int_A\int_B f_{U,V}(u,v)\,dv\,du\\
&=\int_A\left[\int_B f_{V\mid U}(v\mid u)\,dv\right]f_U(u)\,du.
\end{aligned}
$$

Conditional laws at individual null-probability values are version-dependent; the ratio and independence criterion are understood for marginal-almost-every $u$. The examples below use the usual explicit versions on the interiors of their supports.

For variables with a joint density, independence is equivalent to

$$
f_{U,V}(u,v)=f_U(u)f_V(v)\quad\text{almost everywhere},
$$

or, equivalently, $f_{V\mid U}(v\mid u)=f_V(v)$ for marginal-almost-every $u$ and almost every $v$. The **whole normalized distribution** must agree. Merely being normal is insufficient if the conditional means change; matching just two moments is insufficient for general distributions.

## One change of coordinates, three different answers

Now keep the diagonal directions from the screenshot fixed and change only the distribution of the original points. The geometry stays the same; the conditional slices need not.

For $Z=(Z_1,Z_2)^\top$, define the diagonal coordinates

$$
U=\frac{Z_1+Z_2}{\sqrt2},\qquad V=\frac{Z_2-Z_1}{\sqrt2}.
$$

Their directions $e_U=(1,1)^\top/\sqrt2$ and $e_V=(-1,1)^\top/\sqrt2$ are orthonormal. The inverse is

$$
Z_1=\frac{U-V}{\sqrt2},\qquad Z_2=\frac{U+V}{\sqrt2}.
$$

The transformation has determinant one, preserves area, and satisfies $z_1^2+z_2^2=u^2+v^2$. None of these geometric facts by itself says that the random coordinates are independent.

| Original law of $(Z_1,Z_2)$ | Invariant under every rotation? | Original coordinates independent? | Diagonal coordinates independent? |
| --- | --- | --- | --- |
| Independent $N(0,1)$ variables | Yes | Yes | Yes |
| Uniform on $[-1,1]^2$ | No | Yes | No |
| Uniform on the unit disk | Yes | No | No |

### Gaussian hill: the circles are contours

For independent standard normal $Z_1,Z_2$, the inverse transformation and unit absolute Jacobian give

$$
\begin{aligned}
f_{U,V}(u,v)
&=\frac1{2\pi}\exp\left[-\frac{(u-v)^2+(u+v)^2}{4}\right]\\
&=\frac1{2\pi}e^{-(u^2+v^2)/2}
=\phi(u)\phi(v),
\end{aligned}
$$

where $\phi(t)=(2\pi)^{-1/2}e^{-t^2/2}$ is the standard normal density. The marginal integral is explicit:

$$
f_U(u)=\phi(u)\int_{\mathbb R}\phi(t)\,dt=\phi(u),
\qquad f_{V\mid U}(v\mid u)=\phi(v).
$$

The slice at $u=2$ is $e^{-2}$ times the slice at $u=0$, at every $v$. Its height and area shrink together, so normalization restores exactly the same curve.

**A circle drawn on this hill is an equal-density contour, not its outer boundary.** Density stays positive outside that circle. A chord through one contour may shorten while the complete slice, extending over every $v\in\mathbb R$, keeps the same normalized shape.

### Uniform square: rotation changes the support to a diamond

For independent uniform $Z_1,Z_2$ on $[-1,1]$, the joint density is $1/4$ on the centered square. In the diagonal coordinates its support becomes

$$
|u-v|\leq\sqrt2,\quad |u+v|\leq\sqrt2
\quad\Longleftrightarrow\quad |u|+|v|\leq\sqrt2.
$$

For $|u|<\sqrt2$, write $a(u)=\sqrt2-|u|$. The slice has height $1/4$ and width $2a(u)$, so

$$
f_U(u)=\int_{-a(u)}^{a(u)}\frac14\,dt=\frac{a(u)}2,
$$

$$
f_{V\mid U}(v\mid u)=\frac1{2a(u)}\mathbf1_{\{|v|\leq a(u)\}},
\qquad \operatorname{Var}(V\mid U=u)=\frac{a(u)^2}{3}.
$$

Here $\mathbf1$ equals one when its stated condition holds and zero otherwise. The allowed differences become smaller near the diamond's tips. Normalizing changes the slice height but cannot restore its width: the conditional distribution varies with $u$, proving dependence.

A centered square has $90^\circ$ symmetry, but a $45^\circ$ rotation changes its support. Full rotational invariance requires invariance under **every** rotation.

### Uniform disk: rotation preserves the law, but the slices still change

My U06 counterexample combined the words “unit square” with the height $1/\pi$. The normalized density $1/\pi$ belongs to a unit **disk**, whose area is $\pi$. For that model,

$$
f_{Z_1,Z_2}(x,y)=\frac1\pi\mathbf1_{\{x^2+y^2\leq1\}}.
$$

It is invariant under every rotation about the origin, so it is the same uniform disk in $(U,V)$ coordinates. Let $b(u)=\sqrt{1-u^2}$ for $|u|<1$. Then

$$
f_U(u)=\frac{2b(u)}\pi,
\qquad
f_{V\mid U}(v\mid u)=\frac1{2b(u)}\mathbf1_{\{|v|\leq b(u)\}},
$$

$$
\operatorname{Var}(V\mid U=u)=\frac{1-u^2}{3}.
$$

This hill is a flat cylinder. Moving the board changes the rectangular slice's width, and normalizing its area does not remove that change. Both the original coordinates and the diagonal coordinates are dependent.

Rotational invariance means $RZ$ has the same joint law as $Z$ for every planar rotation matrix $R$. It preserves the independence or dependence the law already has. The Gaussian conclusion uses **independent original coordinates plus rotational invariance**. The disk shows why rotational invariance alone is insufficient; the unrotated square shows that independence alone does not imply rotational invariance.

## Perpendicular directions, zero covariance, and sample statistics

The projected vectors $Ue_U$ and $Ve_V$ are perpendicular for every point, for any of these distributions. With finite second moments,

$$
\operatorname{Cov}(U,V)
=\frac12\left(\operatorname{Var}(Z_2)-\operatorname{Var}(Z_1)\right),
$$

because the two cross-covariance terms cancel. Each example has equal coordinate variances and zero means, so $E[UV]=0$: the scalar random variables are also orthogonal in $L^2$, whose inner product is $E[UV]$. The square and disk still give dependent $U,V$. Perpendicular coordinate directions, $L^2$ orthogonality, and independence are distinct statements.

The sample-statistic consequence is particularly clear for two observations. Define

$$
\bar Z=\frac{Z_1+Z_2}{2},\qquad
S_Z^2=\frac{(Z_1-\bar Z)^2+(Z_2-\bar Z)^2}{2-1}.
$$

Direct substitution gives

$$
\bar Z=\frac U{\sqrt2},\qquad S_Z^2=V^2.
$$

For the disk, conditional symmetry gives $E[V\mid U=u]=0$. Consequently,

$$
E[S_Z^2\mid\bar Z=m]=\frac{1-2m^2}{3},
\qquad |m|<\frac1{\sqrt2}.
$$

Its dependence on $m$ proves that these two statistics are dependent. This calculation concerns a dependent pair of observations. For iid normal $X_i=\mu+\sigma Z_i$, with $\sigma>0$,

$$
\bar X=\mu+\frac{\sigma U}{\sqrt2},\qquad S_X^2=\sigma^2V^2,
$$

and independence of $U,V$ gives independence of the sample mean and variance. This is the $n=2$ case motivating the discussion. The statistic here is the sample mean; estimator bias, $E[\widehat\theta]-\theta$, is a different object from the source's informal use of “bias.”

### Is the square a counterexample to the theorem?

**My follow-up question:** “in the svg you graphed about, is the squared one independent? and can be used as a great counter example for the theorem?”

Yes in the original coordinates, no in the diagonal coordinates, and **not a counterexample to the theorem with its normal-sampling assumption intact**:

| Claim                                                                 | What the uniform square shows                                                            |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Independent original coordinates remain independent after rotation    | False in general: independent uniform coordinates become dependent diagonal coordinates. |
| Perpendicular directions or zero covariance imply independence        | False in general: the diagonal coordinates have both properties but are dependent.       |
| Iid observations always give independent sample mean and variance     | False: the square gives iid uniform observations whose mean and variance are dependent.  |
| Iid **normal** observations give independent sample mean and variance | Not refuted: uniform observations do not satisfy the normality assumption.               |

For the unit-square panel, let $X_1,X_2\stackrel{\mathrm{iid}}\sim\operatorname{Unif}(0,1)$ and write $M=(X_1+X_2)/2$, $S^2=(X_1-X_2)^2/2$. The plotted coordinates give $M=1/2+U/\sqrt2$ and $S^2=V^2$. Fixing $M=m$ restricts $X_1$ to a uniform interval centered on $m$, of half-width $a=\min(m,1-m)$. Hence

$$
E[S^2\mid M=m]
=2E[(X_1-m)^2\mid M=m]
=\frac{2}{3}\min(m,1-m)^2,\qquad 0<m<1.
$$

This conditional expectation changes with $m$, proving that $M$ and $S^2$ are dependent—not merely that $U$ and $V$ are dependent. For example, its value is $1/6$ at $m=0.5$, but only $1/150$ at $m=0.9$. Near the upper edge, both observations must be close to one, leaving little room for their difference. These are values of the explicit conditional-density version, not conditioning by dividing point probabilities.

Thus the square is an especially useful **counterexample to dropping the normality assumption**. The disk answers a different question: rotational invariance alone does not imply independence, and its original two coordinates are not iid observations.

### The same bridge for more than two normal observations

For any sample vector $X\in\mathbb R^n$, $n\geq2$, the mean vector $\bar X\mathbf1$ is perpendicular to the residual vector $r=X-\bar X\mathbf1$, because $\mathbf1^\top r=0$. Also $(n-1)S^2=\lVert r\rVert^2$. This is deterministic geometry.

Under iid $N(\mu,\sigma^2)$ sampling with $\sigma>0$, standardize to $Z=(X-\mu\mathbf1)/\sigma$ and choose an orthonormal basis whose first direction is $\mathbf1/\sqrt n$. The rotated coordinates $W_1,\ldots,W_n$ are independent standard normals, with

$$
\bar X=\mu+\frac{\sigma}{\sqrt n}W_1,\qquad
S^2=\frac{\sigma^2}{n-1}\sum_{j=2}^n W_j^2.
$$

The two statistics depend on disjoint independent coordinates. That is the probabilistic reason the theorem works; perpendicular arrows alone are not enough.

The resulting [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic#2. Orthogonality is geometry; independence uses the Gaussian law|t ratio]] has Student’s t distribution.

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Independence versus zero covariance|Independence versus zero covariance]] — The rotated square and disk have zero covariance while their conditional distributions change, giving explicit counterexamples to the converse of independence implying zero covariance.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Multivariate probability/Multivariate normal laws/Gaussian linear transformations|Gaussian linear transformations]] — The orthogonal sum-and-difference transformation preserves the standard Gaussian joint law, and its density factorization proves independence of the transformed coordinates.
- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Useful distribution families/Sample statistics & order/Sample mean and variance|Sample mean and variance]] — For two observations, the sum coordinate determines the sample mean and the squared difference coordinate determines sample variance, transferring the dependence comparison to familiar statistics.

- [[Learning/Probability & mathematical foundations/Random variables & distributions/Geometric interpretation of the t-statistic|Geometric interpretation of the t-statistic]] — The Gaussian rotation proof supplies the independent normal numerator and chi-square denominator needed for the t distribution.

## Origin

> [!info]- Source details
> The [[raw/conversations/2026-11-04-density-slices-rotation-side-chat-excerpts|2026-11-04 side-chat excerpts]] preserve U01–U07 and selected passages of A01–A06, with omissions explicitly marked. U05 supplies my hill/board analogy; U02/U04 motivate the central comparison; U06 supplies the flat-support counterexample idea. The original [[raw/conversations/2026-11-04-density-slices-rotation-side-chat-manifest.json|manifest]] records the historical coverage and the screenshot identity. The only supplied image, I01 at U03, remains archived unchanged; at my request, its display was replaced with the generated Gaussian/unit-square comparison above.
>
> This migration consolidates the earlier checked question and conditional-density equation. The derivations, square/disk correction, precise independence criterion, and covariance bridge include the earlier assistant's explanations and digest checks. The difference coordinate is consistently $V=(Z_2-Z_1)/\sqrt2$ here; reversing its sign changes neither independence nor $V^2$. Inherited parent-chat content is outside this note.
>
> Extension on 2026-11-08: I supplied the projection screenshot and video URL as the motivation, asked for smoother transitions, and asked whether the plotted square refutes the theorem. The screenshot explanation, sign-convention check, explicit uniform-sample counterexample, and general-$n$ bridge are added mathematical synthesis. The linked video's full audio/transcript was not retrieved; the attribution rests on my supplied image and description, not a claimed viewing of the whole video. The normal-sample theorem was independently checked against Penn State STAT 414 §26.3. The new screenshot is now included; other previously excluded parent-chat material remains excluded.
>
> Extension on 2026-11-09: the opening proof summary follows Math with Ming's *Statistics is just ... Geometry?*, using the newly retrieved [[raw/notes/2026-11-09-Statistics-is-just-Geometry-auto-captions.txt|English automatic captions]]: 3:36–7:58 for two observations and 8:00–13:41 for general $n$. This is a caption-grounded summary with independently checked notation and algebra, not a claim of watching every frame. It retains this note's consistent sign for $V$.
>
> Verification: checked the conditional averaging identity, inverse/Jacobian and support transformations, Gaussian factorization, marginal normalizations, conditional second moments, covariance cancellation, and the two-observation identities. The preserved excerpt is selective; the full omitted assistant prose is not claimed as newly recovered.
