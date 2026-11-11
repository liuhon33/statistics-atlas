---
id: learning-clt-delta-scaling-transformation
title: CLT and delta method - scaling and transforming estimation error
layer: learning
primary_home: "[[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Transforming limits/Delta method]]"
subject: probability
backbone_path: Probability & mathematical foundations → Limits & concentration → Probability limit theory → Transforming limits → Delta method
study_band: U–M
note_types: [topic-note, derivation]
source_format: conversation-pdf
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: introduced
aliases: [CLT to delta method, Squared sample mean and the zero derivative case]
tags: [atlas/learning, subject/probability, topic/asymptotics]
connections:
  - "[[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT]]"
  - "[[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Transforming limits/Second-order delta examples]]"
sources:
  - "[[raw/conversations/2026-10-18-MLE-conversation.pdf]]"
  - "[[raw/conversations/2026-10-18-MLE-source-manifest.json]]"
---

# CLT and delta method - scaling and transforming estimation error

Probability & mathematical foundations → Limits & concentration → Probability limit theory → Transforming limits → Delta method

**The CLT describes an average's estimation error. The delta method transfers that error through a smooth function using its local slope.** Throughout, the second argument of $N(a,b)$ is the variance.

## CLT: keep a shrinking error visible

Let $X_1,\ldots,X_n$ be iid with mean $\mu$ and variance $0<\sigma^2<\infty$, and let $\bar X_n=n^{-1}\sum_iX_i$. Independence gives

$$
\operatorname{Var}(\bar X_n)=\frac{1}{n^2}\sum_{i=1}^n\sigma^2=\frac{\sigma^2}{n}.
$$

The standard deviation of the error is $\sigma/\sqrt n$. Multiplying by $\sqrt n$ keeps its variance at $\sigma^2$; the **CLT** supplies the limiting shape:

$$
\sqrt n(\bar X_n-\mu)\xrightarrow{d}N(0,\sigma^2),
\qquad
\bar X_n\approx N\!\left(\mu,\frac{\sigma^2}{n}\right)\quad\text{for large }n.
$$

Reference: [Pishro-Nik, §7.1.2, classical iid CLT](https://www.probabilitycourse.com/chapter7/7_1_2_central_limit_theorem.php).

The arrow compares **distributions**: $W_n\xrightarrow{d}W$ means $P(W_n\le t)\to P(W\le t)$ at every continuity point of the limiting CDF. It does not require individual realizations to approach one another. [Definition: §7.2.4](https://www.probabilitycourse.com/chapter7/7_2_4_convergence_in_distribution.php).

If the observations are themselves normal, the displayed normal law for $\bar X_n$ is exact for every $n$. For general iid observations, normality is an approximation. The $\sqrt n$ rate comes from the averaging assumptions; it is not a universal rate for every estimator.

## Delta method: multiply the error by the derivative

Suppose an estimator $T_n$ of a fixed scalar $\theta$ satisfies

$$
\sqrt n(T_n-\theta)\xrightarrow{d}N(0,v),\qquad 0<v<\infty,
$$

and $g$ is differentiable at $\theta$. Differentiability writes the transformed error as

$$
g(T_n)-g(\theta)
=\bigl[g'(\theta)+r(T_n)\bigr](T_n-\theta),
\qquad r(t)\longrightarrow0\text{ as }t\longrightarrow\theta.
$$

The assumed limit implies $T_n\xrightarrow{p}\theta$, so $r(T_n)\xrightarrow{p}0$. After multiplication by $\sqrt n$, Slutsky's theorem gives

$$
\boxed{\sqrt n\bigl[g(T_n)-g(\theta)\bigr]
\xrightarrow{d}N\!\left(0,[g'(\theta)]^2v\right).}
$$

For $g'(\theta)\ne0$, this yields the first-order approximation

$$
g(T_n)\approx N\!\left(g(\theta),\frac{[g'(\theta)]^2v}{n}\right).
$$

The local slope multiplies the error; its **absolute value multiplies standard deviation**, and its **square multiplies variance**. Here $v$ belongs to the scaled limit, not the unscaled estimator. Reference: [Berkeley STAT 135, Theorem 3](https://stat135.berkeley.edu/fall-2026/Modules/11-DeltaMethod.html#delta-method-theorem-for-asymptotic-normality).

## Worked derivation: square the sample mean

For iid $X_i\sim N(\mu,1)$, estimate $\mu^2$ by $\bar X_n^2$. This squares the mean, rather than averaging the squared observations. Write

$$
Z_n=\sqrt n(\bar X_n-\mu)\sim N(0,1).
$$

Expanding the square gives an exact linear term and remainder:

$$
\bar X_n^2-\mu^2
=2\mu(\bar X_n-\mu)+(\bar X_n-\mu)^2,
$$

$$
\sqrt n(\bar X_n^2-\mu^2)
=2\mu Z_n+\frac{Z_n^2}{\sqrt n}.
$$

Because $E[Z_n^2]=1$, Markov's inequality gives, for every $\varepsilon>0$,

$$
P\!\left(\frac{Z_n^2}{\sqrt n}>\varepsilon\right)
\le\frac{1}{\varepsilon\sqrt n}\longrightarrow0.
$$

For fixed $\mu\ne0$, only the linear term survives on this scale:

$$
\sqrt n(\bar X_n^2-\mu^2)\xrightarrow{d}N(0,4\mu^2),
\qquad
\bar X_n^2\approx N\!\left(\mu^2,\frac{4\mu^2}{n}\right).
$$

This is the delta formula with $g(x)=x^2$, $g'(\mu)=2\mu$ and $v=1$.

### When the derivative is zero

At $\mu=0$, the linear term vanishes. The first-order limit collapses to zero, but the estimator still varies:

$$
\sqrt n\,\bar X_n^2\xrightarrow{p}0,
\qquad
\boxed{n\bar X_n^2=Z_n^2\sim\chi_1^2.}
$$

The useful scale is now $n$, and the chi-square law is exact. Near zero, the discarded quadratic term can also matter at a finite sample size.

For a direct check, $\bar X_n^2=\mu^2+2\mu Z_n/\sqrt n+Z_n^2/n$. Using $E[Z_n]=E[Z_n^3]=0$, $E[Z_n^2]=1$ and $E[Z_n^4]=3$ gives

$$
E[\bar X_n^2]=\mu^2+\frac1n,
\qquad
\operatorname{Var}(\bar X_n^2)=\frac{4\mu^2}{n}+\frac2{n^2}.
$$

Thus a zero first-order variance means that a smaller-order term determines the variation.

## Watch the approximation change

Start **Away from zero** and compare the green exact error with the blue linear term. Then choose **At $\mu=0$**: the blue term disappears, but the quadratic term still varies. Pin the current CDF and increase $n$ on the $\sqrt n$ scale to see its distribution concentrate near zero. Finally choose **At zero: use $n$ scale**; changing $n$ now leaves the exact $\chi_1^2$ distribution unchanged.

```atlas-interactive
path: assets/figures/2026-11-11-ci-delta/delta-explorer.html
title: Squared mean — exact error versus delta approximation
height: 1250
```

*Original Codex illustration for iid $N(\mu,1)$ observations. The left graph always uses $\sqrt n$ scaling; the right graph uses the selected scale. Its CDF compares whole sampling distributions, while the $z$ slider selects just one realization. The right graph's horizontal range adapts; pinning retains a reference curve for comparison.*

[[assets/figures/2026-11-11-ci-delta/delta-explorer.html|Open the standalone explorer]]

The CDF is calculated directly from the normal model. For $V=a(\bar X_n^2-\mu^2)$ with $a\in\{1,\sqrt n,n\}$, put $r=\mu^2+t/a$. If $r<0$, then $P(V\le t)=0$. Otherwise the event is $-\sqrt r\le\bar X_n\le\sqrt r$, so

$$
P(V\le t)=\Phi\!\left((\sqrt r-\mu)\sqrt n\right)
-\Phi\!\left((-\sqrt r-\mu)\sqrt n\right).
$$

Here $\Phi$ is the standard normal CDF. This exact curve lets us inspect what the linear approximation discards. The variance bar uses the two terms already derived above; their ratio, for $\mu\ne0$, is

$$
\frac{\text{quadratic variance}}{\text{linear variance}}
=\frac{2/n^2}{4\mu^2/n}=\frac{1}{2n\mu^2}.
$$

Thus the relevant distance from zero is $\sqrt n\,|\mu|$, measured in standard errors of the sample mean. A large value makes the quadratic variance small relative to the linear variance; at zero the linear contribution vanishes completely.

> [!example]- Static comparison of the three regimes
> ![[assets/figures/2026-11-11-ci-delta/delta-overview.svg]]
> Left: at $\mu=1,n=25$, the linear term supplies about 98% of the exact variance. Middle: at $\mu=0$, the $\sqrt n$ error shrinks toward zero. Right: on the $n$ scale, its exact law stays $\chi_1^2$ for every $n$. Horizontal units differ between panels; CDF height always runs from 0 to 1.

## Connections

- [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Laws of large numbers & CLT/Classical iid CLT|Classical iid CLT]] — Supplies the normal limiting error that the delta method transforms.
- [[Backbone/Probability & mathematical foundations/Limits & concentration/Probability limit theory/Transforming limits/Second-order delta examples|Second-order delta examples]] — The squared-mean example at zero shows why a vanishing first derivative changes both the scale and the limiting law.

## Origin

> [!info]- Source details
> Migrated from the [[raw/conversations/2026-10-18-MLE-conversation.pdf|MLE export]], pp. 7–11, and the old vault's checked squared-mean derivation, including its 2026-11-08 expansion. My requests for the delta method and unfamiliar limit notation motivated these explanations; the example and derivations are assistant explanations, not handwritten work attributed to me.
>
> The zero-mean case, remainder bound and exact moments are checked additions from the earlier curation. Routine definition questions are integrated into the text. The migration retains the essential theory and example; unrelated applications and the old diagram package are outside this note.
>
> Added on 2026-11-11: an original Codex interactive comparison, its static fallback, the exact normal-model CDF calculation and variance-ratio interpretation. [[assets/figures/2026-11-11-ci-delta/build.py|Reproducible builder]], [[assets/figures/2026-11-11-ci-delta/ci-delta-reproduction|usage and checks]], and [[assets/figures/2026-11-11-ci-delta/math-checks.json|independent numerical comparisons]]. The illustration checks this normal example; it does not establish the general asymptotic theorems by simulation.
