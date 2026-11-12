---
id: moments-mgfs-and-characteristic-functions
title: MGFs and characteristic functions
layer: backbone
level: 5
subject: probability
study_band: U
backbone_path: Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → MGFs and characteristic functions
created: '2026-11-08'
updated: '2026-11-12'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/undergraduate
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/Expectation & moments]]'
sources:
- '[[_system/Sources/prob]]'
- '[[_system/Sources/process]]'
---

# MGFs and characteristic functions

Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → MGFs and characteristic functions

Parent: [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/Expectation & moments|Expectation & moments]]

## 1. Use an MGF — recover the mean and variance

Suppose a score $X$ is **0 or 2, each with probability $1/2$**. A **moment-generating function (MGF)** packages averages of powers of $X$ into one function:

$$
M_X(t)=\mathbb E[e^{tX}]
=\tfrac12e^{0t}+\tfrac12e^{2t}
=\tfrac12+\tfrac12e^{2t}.
$$

Here $t$ is an ordinary input, not a random observation. For each chosen $t$, transform the possible scores and take their probability-weighted average. The result is a number; $M_X$ is a curve, **not a probability density**.

![[assets/figures/2026-11-12-mgf/mgf-use.svg]]
*The score distribution stays fixed. The MGF passes through $(0,1)$; its tangent slope there is the mean.*

**Recipe:** differentiate with respect to $t$, then substitute $t=0$:

$$
\begin{aligned}
M_X'(t)&=e^{2t}
&\Longrightarrow\quad \mathbb E[X]&=M_X'(0)=1,\\
M_X''(t)&=2e^{2t}
&\Longrightarrow\quad \mathbb E[X^2]&=M_X''(0)=2.
\end{aligned}
$$

The second result is the **second raw moment**: the average squared score, not the variance. Convert it using

$$
\operatorname{Var}(X)=M_X''(0)-[M_X'(0)]^2=2-1^2=1.
$$

Use this when one manageable MGF makes several moment calculations easier than separate sums or integrals. The derivative rule below requires the MGF to be finite throughout some open interval around zero; our two-score example satisfies this for every real $t$. [MIT 18.600, Lecture 26, PDF pp. 8–9 and 13–19](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/d68c0ee3be77495da2aeaf921f7fc081_MIT18_600F19_lec26.pdf).

## 2. How it works — expansion, expectation, then derivatives

### 2.1 Keep the roles of $X$ and $t$ separate

Hold the distribution of $X$ fixed. Define its $n$th **raw moment** by

$$
m_n=\mathbb E[X^n],\qquad n=1,2,\ldots,\qquad m_0=1.
$$

“Raw” means powers about zero; central moments instead use $X-\mathbb E[X]$. The quantities $m_n$ are constants with respect to $t$. They are not additional random variables.

The [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/LOTUS expectation rule|expectation rule]] makes the MGF concrete:

$$
M_X(t)=
\begin{cases}
\displaystyle\sum_x e^{tx}\,p_X(x), & X\text{ discrete},\\[6pt]
\displaystyle\int_{-\infty}^{\infty} e^{tx}\,f_X(x)\,dx,
& X\text{ has density }f_X.
\end{cases}
$$

We average over **$x$**, but differentiate with respect to **$t$**. The weights $p_X(x)$ or $f_X(x)$ do not change with $t$.

**Standing assumption for this section:** $M_X(t)<\infty$ for all $|t|<h$, for some $h>0$. This permits the local series and derivative operations below, not just evaluation at the single point $t=0$. The justification is given in §2.6. [Siegrist, *Probability, Mathematical Statistics, and Stochastic Processes*, “Generating Functions,” MGF subsection](https://www.randomservices.org/random/expect/Generating.html).

### 2.2 Maclaurin expansion: expectation turns powers into moments

A **Maclaurin series** is a Taylor series centred at zero. Start with the exponential series, where $n!=n(n-1)\cdots1$ and $0!=1$:

$$
e^u=1+u+\frac{u^2}{2!}+\frac{u^3}{3!}+\frac{u^4}{4!}+\cdots.
$$

Substitute $u=tX$. For each possible outcome of $X$,

$$
\begin{aligned}
e^{tX}
&=1+tX+\frac{(tX)^2}{2!}+\frac{(tX)^3}{3!}+\frac{(tX)^4}{4!}+\cdots\\
&=1+tX+\frac{t^2X^2}{2!}+\frac{t^3X^3}{3!}+\frac{t^4X^4}{4!}+\cdots.
\end{aligned}
$$

Now take expectation. Under the standing assumption we may average term by term, and pull out each nonrandom power of $t$:

$$
\begin{aligned}
M_X(t)
&=\mathbb E\!\left[1+tX+\frac{t^2X^2}{2!}+\frac{t^3X^3}{3!}+\cdots\right]\\
&=\mathbb E[1]+\mathbb E[tX]
  +\mathbb E\!\left[\frac{t^2X^2}{2!}\right]
  +\mathbb E\!\left[\frac{t^3X^3}{3!}\right]+\cdots\\
&=1+t\mathbb E[X]+\frac{t^2}{2!}\mathbb E[X^2]
  +\frac{t^3}{3!}\mathbb E[X^3]+\cdots\\
&=1+m_1t+\frac{m_2t^2}{2!}+\frac{m_3t^3}{3!}
  +\frac{m_4t^4}{4!}+\cdots.
\end{aligned}
$$

**This is where expectation enters:** it replaces each random coefficient $X^n$ with the number $\mathbb E[X^n]$. The coefficient of $t^n$ is **$m_n/n!$**, not $m_n$ alone. Linearity does **not** mean $\mathbb E[e^{tX}]=e^{t\mathbb E[X]}$; averaging a nonlinear transformation is a different operation.

### 2.3 Differentiate one step at a time

![[assets/figures/2026-11-12-mgf/mgf-derivative-ladder.gif]]
*Read downward: expand, average, then differentiate the full function repeatedly. A color follows the same original power of $X$. The right column evaluates each completed row at $t=0$; it is not differentiated to obtain the next row. The dots mean the series continues.*

> [!example]- Static view — all steps together
> ![[assets/figures/2026-11-12-mgf/mgf-derivative-ladder.svg]]

**First derivative.** Begin with the final line of §2.2 and use $\frac{d}{dt}t^k=kt^{k-1}$:

$$
\begin{aligned}
M_X'(t)
&=0+m_1+\frac{m_2}{2!}(2t)
  +\frac{m_3}{3!}(3t^2)+\frac{m_4}{4!}(4t^3)+\cdots\\
&=m_1+m_2t+\frac{m_3t^2}{2!}+\frac{m_4t^3}{3!}+\cdots.
\end{aligned}
$$

The cancellations are $2/2!=1$, $3/3!=1/2!$, and $4/4!=1/3!$. **Only now** set $t=0$:

$$
M_X'(0)=m_1+m_2(0)+\frac{m_3(0)^2}{2!}+\cdots
=m_1=\mathbb E[X].
$$

**Second derivative.** Return to $M_X'(t)$, not the number $M_X'(0)$:

$$
\begin{aligned}
M_X''(t)
&=0+m_2+\frac{m_3}{2!}(2t)
  +\frac{m_4}{3!}(3t^2)+\cdots\\
&=m_2+m_3t+\frac{m_4t^2}{2!}+\cdots,\\[3pt]
M_X''(0)
&=m_2+m_3(0)+\frac{m_4(0)^2}{2!}+\cdots
=m_2=\mathbb E[X^2].
\end{aligned}
$$

**Third derivative.** Differentiate $M_X''(t)$ once more:

$$
\begin{aligned}
M_X'''(t)&=0+m_3+\frac{m_4}{2!}(2t)+\cdots
=m_3+m_4t+\cdots,\\
M_X'''(0)&=m_3=\mathbb E[X^3].
\end{aligned}
$$

Each derivative lowers every remaining power of $t$ by one. At zero, only the new constant term survives.

**Why this works for every order.** Track one term $m_kt^k/k!$ through $n$ derivatives:

$$
\frac{d^n}{dt^n}\left(\frac{m_kt^k}{k!}\right)
=\begin{cases}
0,&k<n,\\[3pt]
\displaystyle\frac{m_k}{k!}\frac{k!}{(k-n)!}t^{k-n}
=\frac{m_k}{(k-n)!}t^{k-n},&k\ge n.
\end{cases}
$$

- If $k<n$, differentiation has already removed that term.
- If $k=n$, the expression is the constant $m_n$: the $n!$ from differentiation cancels the original $n!$.
- If $k>n$, a positive power of $t$ remains, so evaluation at zero removes it.

Therefore

$$
\boxed{M_X^{(n)}(0)=m_n=\mathbb E[X^n].}
$$

Setting $t=0$ **before** differentiation would instead give $M_X(0)=1$ and lose the entire curve. Differentiating that constant cannot recover its slope or higher derivatives. [MIT 18.600, Lecture 26, PDF pp. 13–19](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/d68c0ee3be77495da2aeaf921f7fc081_MIT18_600F19_lec26.pdf).

### 2.4 The same relationship directly inside expectation

The series shows **where the moments are stored**. The chain rule shows **why each derivative produces another factor of $X$**. For a fixed outcome $X=x$,

$$
\frac{d}{dt}e^{tx}=xe^{tx},\qquad
\frac{d}{dt}(xe^{tx})=x\,(xe^{tx})=x^2e^{tx}.
$$

Here $x$ is held fixed while $t$ changes. Under our assumption we can interchange differentiation and expectation:

$$
\begin{aligned}
M_X'(t)
&=\frac{d}{dt}\mathbb E[e^{tX}]\\
&=\mathbb E\!\left[\frac{d}{dt}e^{tX}\right]\\
&=\mathbb E[Xe^{tX}],\\[5pt]
M_X''(t)
&=\frac{d}{dt}\mathbb E[Xe^{tX}]\\
&=\mathbb E\!\left[X\frac{d}{dt}e^{tX}\right]\\
&=\mathbb E[X^2e^{tX}].
\end{aligned}
$$

Repeat this step $n$ times, **then** put $t=0$:

$$
M_X^{(n)}(t)=\mathbb E[X^ne^{tX}]
\quad\Longrightarrow\quad
M_X^{(n)}(0)=\mathbb E[X^ne^0]
=\mathbb E[X^n].
$$

Differentiation acts on $t$; expectation averages over $X$; setting $t=0$ removes the remaining exponential. These are three distinct operations. [Fithian, Berkeley Stat 210A, “Moment-generating function and cumulant-generating function,” Eq. (4)](https://stat210a.berkeley.edu/fall-2024/reader/exponential-families.html#moment-generating-function-and-cumulant-generating-function).

### 2.5 Check every operation on the two-score example

For $P(X=0)=P(X=2)=1/2$, expand the actual MGF:

$$
\begin{aligned}
M_X(t)
&=\tfrac12+\tfrac12\left(1+2t+\frac{(2t)^2}{2!}
  +\frac{(2t)^3}{3!}+\frac{(2t)^4}{4!}+\cdots\right)\\
&=1+t+\frac{2t^2}{2!}+\frac{4t^3}{3!}+\frac{8t^4}{4!}+\cdots.
\end{aligned}
$$

| Order | Differentiate the full MGF | Evaluate at zero | Direct expectation check |
| --- | --- | --- | --- |
| 1 | $M_X'(t)=e^{2t}$ | $1$ | $\tfrac12(0)+\tfrac12(2)=1$ |
| 2 | $M_X''(t)=2e^{2t}$ | $2$ | $\tfrac12(0^2)+\tfrac12(2^2)=2$ |
| 3 | $M_X'''(t)=4e^{2t}$ | $4$ | $\tfrac12(0^3)+\tfrac12(2^3)=4$ |

For example, the coefficient of $t^3$ is $4/3!$. Three derivatives multiply it by $3\cdot2\cdot1$, leaving the third raw moment $4$. This is the same answer whether we use the series, the exponential's derivatives, or the original probability-weighted sum.

### 2.6 Why the exchanges are legitimate

The finite-near-zero condition is substantive: $M_X(0)=1$ holds for **every** real-valued random variable, even if the MGF is infinite everywhere else. Existence of a few moments—or even all raw moments—does not by itself guarantee a finite MGF around zero. See [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/Moment existence|Moment existence]].

> [!note]- Justification — an integrable bound for both operations
> Choose $0<a<h$ from the standing assumption. Since
> $$e^{a|X|}\le e^{aX}+e^{-aX},$$
> we have $\mathbb E[e^{a|X|}]\le M_X(a)+M_X(-a)<\infty$.
>
> **Series and expectation.** For $|t|<a$,
> $$\mathbb E\!\left[\sum_{k=0}^{\infty}\left|\frac{t^kX^k}{k!}\right|\right]
> =\mathbb E[e^{|t||X|}]\le\mathbb E[e^{a|X|}]<\infty.$$
> Absolute integrability allows the expectation and series to be interchanged. The resulting power series can be differentiated term by term within $|t|<a$. This establishes a convergent Maclaurin expansion, not merely a formal series.
>
> **Derivative and expectation.** For $|t|\le b<a$ and integer $r\ge0$, the exponential series gives $y^r\le r!e^{(a-b)y}/(a-b)^r$ for $y\ge0$. Hence
> $$|X|^r e^{tX}\le |X|^r e^{b|X|}
> \le\frac{r!}{(a-b)^r}e^{a|X|}.$$
> The final bound is integrable and independent of $t$. Applied to successive derivatives (and their difference quotients via the mean value theorem), it justifies differentiation under expectation by dominated convergence. In particular, every $\mathbb E[|X|^r]$ is finite.
>
> The two-score example needs no infinite-integral argument: its expectation is a finite sum. The bound explains why the general case needs an assumption. The MGF power-series theorem is stated in [Siegrist, “Generating Functions,” MGF subsection](https://www.randomservices.org/random/expect/Generating.html); the explicit bound here is added explanatory detail.

## Origin

> [!info]- Source details
> Reference enrichment requested on 2026-11-12: a practical first reading level, then the Maclaurin expansion and the derivative–expectation relationship one step at a time. This visit develops the MGF part of the existing shared node; characteristic functions and deeper connections are deferred. The worked score example, expanded algebra, domination argument and figures are added synthesis, not attributed user work.
>
> Read sources: Scott Sheffield, MIT 18.600 (Fall 2019), Lecture 26, PDF pp. 8–9 and 13–19; Kyle Siegrist, “Generating Functions,” MGF subsection; Will Fithian, Berkeley Stat 210A, MGF/CGF subsection, especially Eq. (4). Citations are inline. The series is used locally under the stated exponential-integrability condition.
>
> Original figures and checks: [[assets/figures/2026-11-12-mgf/build.py|reproducible generator]] and [[assets/figures/2026-11-12-mgf/checks.json|check record]]. Symbolic/example checks support the displayed algebra; the general justification is the argument above. Both static previews and all five decoded animation stages were inspected; live Obsidian rendering was not verified.

```atlas
```
