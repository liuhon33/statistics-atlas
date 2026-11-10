---
id: estimators-raoblackwell-theorem
title: Rao–Blackwell theorem
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Constructing & improving estimators → Rao–Blackwell theorem
created: '2026-11-08'
updated: '2026-11-10'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Constructing & improving estimators]]'
sources:
- '[[_system/Sources/estimate]]'
- '[[_system/Sources/theory]]'
- '[[_system/Sources/asym]]'
---

# Rao–Blackwell theorem

Statistical inference & modeling → Frequentist & likelihood inference → Point estimation → Constructing & improving estimators → Rao–Blackwell theorem

Parent: [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Constructing & improving estimators|Constructing & improving estimators]]

## 1. See it and use it

Want to estimate a coin's heads probability $p$ from three independent tosses with the same $p$? A crude rule uses only the first toss: $U=1$ for heads, $0$ for tails. Rao–Blackwell turns this noisy rule into a steadier one using the **same data**.

![[assets/figures/2026-11-10-rao-blackwell/conditional-average.png]]

*With two heads, these three orders are equally likely. Average the first-toss estimates: $(1+1+0)/3=2/3$.*

**Definition.** Given an estimator $U$ with finite second moment and a **sufficient statistic** $T$—a summary retaining all the sample's information about the unknown parameter—replace $U$ by its conditional average:

$$
U^*=\mathbb E[U\mid T].
$$

The new estimator has the **same mean, no larger variance, and no larger mean squared error**. Thus an unbiased starting rule stays unbiased. See [Cambridge Statistics IB, §3.3, Theorem 3.5, slide 11](https://www.statslab.cam.ac.uk/~sb2116/Statistics_IB/slides/S1B-17-03-sufficiency.pdf#page=11).

**Use it:** choose a starting rule, find a sufficient summary, then average the rule over possible samples sharing that summary. Here $T$ is the total heads count, and $U^*=T/3$. Two heads give $2/3\approx67\%$, rather than $0\%$ or $100\%$.

**Interpretation:** remove irrelevant ordering noise. “Better” means lower or equal average squared error across repeated samples—not necessarily closer on every sample.

## 2. Usage Examples

### Two Bernoulli observations: improve a deliberately crude estimator

Now use **two tosses**, so we can list every possibility. Let

$$
X_1,X_2\overset{\mathrm{iid}}{\sim}\operatorname{Bernoulli}(p),
\qquad 0<p<1,
$$

where $1$ means heads and $0$ means tails. The goal is to estimate the common heads probability $p$.

**Step 1 — start with an estimator.** Take $U=X_1$: ignore the second observation and report either $0$ or $1$. It is crude, but unbiased:

$$
\mathbb E_p[U]=p,
\qquad \operatorname{Var}_p(U)=p(1-p).
$$

**Step 2 — choose a sufficient statistic.** Use $T=X_1+X_2$, the total number of heads. The joint probability is

$$
\Pr_p(X_1=x_1,X_2=x_2)
=p^{x_1+x_2}(1-p)^{2-x_1-x_2}.
$$

It depends on the observations only through their sum. More concretely, conditional on $T=1$, the two possible orders $(1,0)$ and $(0,1)$ each have probability $1/2$, regardless of $p$; for $T=0$ or $2$, the order is determined. This parameter-free conditional distribution makes $T$ a [[Backbone/Statistical inference & modeling/Frequentist & likelihood inference/Point estimation/Constructing & improving estimators/Sufficient statistics|sufficient statistic]].

**Step 3 — average the old estimator within each group.**

![[assets/figures/2026-11-10-rao-blackwell/two-bernoulli.png]]

*Only the mixed-outcome group changes: the old outputs $0$ and $1$ are replaced by their conditional average $1/2$. The three groups themselves are not equally likely.*

In particular,

$$
\Pr_p(X_1=1\mid T=1)
=\frac{p(1-p)}{2p(1-p)}=\frac12.
$$

Therefore

$$
U^*=\mathbb E_p[X_1\mid T]
=\begin{cases}
0,&T=0,\\
1/2,&T=1,\\
1,&T=2
\end{cases}
=\boxed{\frac{T}{2}=\frac{X_1+X_2}{2}}.
$$

Rao–Blackwell has recovered the sample mean from the first-toss-only rule. Although the conditional expectation is computed under $P_p$, the resulting formula **does not require knowing $p$**.

**Step 4 — quantify the improvement.** Independence gives

$$
\mathbb E_p[U^*]=p,
\qquad
\operatorname{Var}_p(U^*)
=\frac{\operatorname{Var}_p(X_1)+\operatorname{Var}_p(X_2)}{4}
=\frac{p(1-p)}{2}.
$$

Both estimators are unbiased, so their mean squared errors equal their variances: **the MSE is halved**. At $p=1/2$, it falls from $1/4$ to $1/8$ (squared-probability units). This is a repeated-sampling comparison, not a guarantee for each observed pair. For example, if $p=0.1$ and the pair is $(0,1)$, the old estimate $0$ happens to be closer to $p$ than the new estimate $0.5$.

The two-observation calculation above is an explicit specialization of Bernoulli-count sufficiency in [Cambridge Statistics IB, Example 3.1, slides 2 and 5](https://www.statslab.cam.ac.uk/~sb2116/Statistics_IB/slides/S1B-17-03-sufficiency.pdf#page=2).

### Why Rao–Blackwell is at least as good: a general proof

Let $U=U(X)$ estimate a fixed real parameter $\theta$, with $\mathbb E_\theta[U^2]<\infty$ for every $\theta$. Let $T=T(X)$ be sufficient and define $U^*=\mathbb E_\theta[U\mid T]$. Here “at least as good” means **no larger mean squared error at every parameter value**.

**1. The bias does not change.** By the [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Tower property|tower property]],

$$
\mathbb E_\theta[U^*]
=\mathbb E_\theta\!\left[\mathbb E_\theta[U\mid T]\right]
=\mathbb E_\theta[U].
$$

Subtracting $\theta$ shows that the two biases are equal. The starting estimator need not be unbiased.

**2. The variance cannot increase.** The law of total variance gives

$$
\operatorname{Var}_\theta(U)
=\underbrace{\mathbb E_\theta[\operatorname{Var}_\theta(U\mid T)]}_{\text{nonnegative variation removed}}
+\operatorname{Var}_\theta(U^*).
$$

**3. Combine them.** Since $\operatorname{MSE}_\theta(U)=\operatorname{Var}_\theta(U)+(\mathbb E_\theta[U]-\theta)^2$,

$$
\boxed{
\operatorname{MSE}_\theta(U)-\operatorname{MSE}_\theta(U^*)
=\mathbb E_\theta[\operatorname{Var}_\theta(U\mid T)]\geq0.
}
$$

For a fixed $\theta$, equality holds exactly when $U=U^*$ almost surely under $P_\theta$—there is no remaining within-group variation to remove. In our toy example, only $T=1$ has conditional variance, namely $1/4$, so the removed MSE is $2p(1-p)\times1/4=p(1-p)/2$.

**Where sufficiency matters:** these expectation/variance identities hold for any conditioning statistic. Sufficiency ensures that the conditional averaging can be carried out without the unknown parameter, yielding a usable estimator. Conditioning on an arbitrary summary does not ensure this. Source: [Cambridge, Theorem 3.5 and following notes, slides 11–12](https://www.statslab.cam.ac.uk/~sb2116/Statistics_IB/slides/S1B-17-03-sufficiency.pdf#page=11).

## 3. Deeper understanding: can I keep Rao–Blackwellizing?

### The ordinary explanation: the same averaging does nothing twice

**Question: can I keep doing Rao–Blackwell to make the estimate more accurate?**

**Not by conditioning on the same $T$ again.** After one pass, $U^*=g(T)$: its value is already determined by $T$. Within a fixed-$T$ group, every sample now receives the same output, so averaging those outputs changes nothing:

$$
\mathbb E_\theta[U^*\mid T]
=\mathbb E_\theta[g(T)\mid T]
=g(T)=U^*.
$$

For the two-toss example, $U^*=T/2$. In the $T=1$ group both $(0,1)$ and $(1,0)$ now give $1/2$. Their average is still $1/2$. There is no new information or additional within-group variation to exploit.

### The geometric explanation: a projection is idempotent

This is precisely the [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection|conditional-expectation projection]] viewpoint. For a fixed parameter value $p$, regard square-integrable random variables as vectors with inner product and squared norm

$$
\langle A,B\rangle_p=\mathbb E_p[AB],
\qquad \|A\|_p^2=\mathbb E_p[A^2].
$$

The closed subspace

$$
\mathcal H_T=L^2(\sigma(T),P_p)
$$

consists of all square-integrable functions of $T$. It is **not merely the line spanned by $T$**: nonlinear functions of $T$ belong too. Conditional expectation is the orthogonal projection $P_T$ onto this subspace:

$$
U^*=P_TU=\mathbb E_p[U\mid T],
\qquad U-U^*\perp\mathcal H_T.
$$

![[assets/figures/2026-11-10-rao-blackwell/projection-idempotence.png]]

*Random variables are points/vectors in this schematic $L^2$ slice, not individual data points. The constant random variable $p$ and the improved estimator $U^*$ both lie in $\mathcal H_T$. The removed component is perpendicular to the subspace.*

Because $p\in\mathcal H_T$, the estimation error splits into perpendicular components:

$$
U-p=(U-U^*)+(U^*-p),
\qquad
\boxed{\|U-p\|_p^2=\|U-U^*\|_p^2+\|U^*-p\|_p^2}.
$$

That is the MSE improvement from §2, now seen as Pythagoras. Once $U^*$ is in the subspace, its projection stays there:

$$
\boxed{P_T^2U=P_TU.}
$$

This property is called **idempotence**. See [Steven Lalley, *Conditional Expectation*, §1, pp. 1–3](https://galton.uchicago.edu/~lalley/Courses/383/ConditionalExpectation.pdf#page=1) for the $L^2$ projection, orthogonality and tower properties.

> [!important] Projecting the estimator is not projecting directly onto the truth
> The closest-point property minimizes $\mathbb E_p[(U-h(T))^2]$ over $h(T)$: it approximates **$U$** using $T$. It does not by itself say that $U^*$ is the best possible estimator of $p$ among all estimators. The MSE comparison with $U$ follows because the constant $p$ also belongs to the projection subspace.

### The qualification: a different subspace can still help

“Projecting again does nothing” is true for the **same projection**, not all successive projections. For example, conditioning $X_1$ on the entire pair $S=(X_1,X_2)$ leaves it unchanged, even though $S$ is sufficient. Subsequently conditioning on the smaller sufficient summary $T=X_1+X_2$ produces $T/2$ and improves it.

More generally, if $T=h(S)$ is also sufficient, the nested-information tower property gives

$$
\mathbb E_\theta[\mathbb E_\theta[U\mid S]\mid T]
=\mathbb E_\theta[U\mid T].
$$

The second step can remove variation left by the first. Conversely, replacing $T$ by an equivalent summary, or conditioning its already-computed function on more information, changes nothing. Do not extend the nested formula to arbitrary non-nested statistics.

Nor can we discard all information and claim a perfect estimator: in the toy example, $\mathbb E_p[U^*]=p$ is an unknown number, not a computable rule. The zero-information summary is not sufficient for this Bernoulli family.

**Takeaway:** one exact Rao–Blackwell step removes everything removable by that particular conditional expectation. Repeating the same step cannot help; changing the summary is a different operation and must still yield a valid estimator.

### Origin

> [!info]- Source details
> Definition and squared-error guarantee checked against Cambridge Statistics IB, Lecture 3, §3.3, Theorem 3.5 (slide 11); Bernoulli-count sufficiency is Example 3.1 (slides 2 and 5). The three-toss example and diagram are original explanatory additions, not copied figures. Reproducible figure generation and exact conditional-average checks: [[assets/figures/2026-11-10-rao-blackwell/build_figure.py|figure source]].
>
> Sections 2–3 added at the user's request: the two-Bernoulli example, proof and repeated-conditioning question. The source theorem is stated in Cambridge slides 11–12; the projection characterization and nested conditioning were checked against Lalley §1. The finite example, geometric specialization and drawings are original synthesis. An existing handwritten conditional-projection figure was inspected; a new figure uses this page's $U,U^*,T,p$ notation and makes idempotence explicit. Reproduce and check the new figures with [[assets/figures/2026-11-10-rao-blackwell/build_deeper.py|the two-observation and projection script]]. All almost-sure and orthogonality statements are under the fixed sampling law; finite checks illustrate rather than prove the general theorem.

```atlas
```
