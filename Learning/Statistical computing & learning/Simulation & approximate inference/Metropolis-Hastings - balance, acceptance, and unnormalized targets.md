---
id: learning-metropolis-hastings-balance-acceptance
title: Metropolis-Hastings - balance, acceptance, and unnormalized targets
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Simulation & approximate inference/Markov chain Monte Carlo/Posterior simulation/Metropolis–Hastings]]"
subject: computing
backbone_path: "Statistical computing & learning → Simulation & approximate inference → Markov chain Monte Carlo → Posterior simulation → Metropolis–Hastings"
study_band: M
note_types: [conversation-digest, derivation, question, insight]
question_roles: [concept-distinction, mechanism, assumption-boundary]
source_format: handwriting
created: 2026-11-08
updated: 2026-11-08
status: active
verification: checked
learning_state: practicing
aliases: [MCMC acceptance ratio, My Metropolis-Hastings notes]
tags: [atlas/learning, subject/computing, topic/mcmc, study/masters]
connections:
  - "[[Backbone/Probability & mathematical foundations/Stochastic processes/Discrete-time stochastic models/Markov chains/Detailed balance]]"
  - "[[Backbone/Probability & mathematical foundations/Stochastic processes/Discrete-time stochastic models/Markov chains/Stationary distributions]]"
sources:
  - "[[raw/assets/2026-11-06-Metropolis-Hastings-I01-acceptance-derivation.png]]"
---

# Metropolis-Hastings - balance, acceptance, and unnormalized targets

Statistical computing & learning → Simulation & approximate inference → Markov chain Monte Carlo → Posterior simulation → Metropolis–Hastings

**Metropolis–Hastings corrects a proposal mechanism so that the target distribution is stationary.** It balances probability flow in each direction, and its acceptance rule needs only ratios of target values. A shared, unknown normalization constant cancels.

## 1. Does detailed balance mean making the two transitions equal?

*My first question, paraphrased:* To obtain the target as a stationary distribution, do we make the forward and reverse transition probabilities equal, then always accept when the acceptance ratio exceeds one?

Let $p(x)$ be the target probability mass or density, $x$ the current state, and $x'$ a candidate next state.

| Symbol | Role |
| --- | --- |
| $q(x'\mid x)$ | Proposal mass or density: how we generate a candidate from the current state. |
| $A(x,x')\in[0,1]$ | Acceptance probability, conditional on having proposed $x'$. |
| $T(x\to x')$ | Actual transition probability, or off-diagonal transition density in the continuous case. |

For distinct states,

$$
T(x\to x')=q(x'\mid x)A(x,x').
$$

Generate $x'\sim q(\cdot\mid x)$, then accept it with probability $A(x,x')$. If rejected, the next state is still $x$; **the repeated state counts as a sample**. Thus the full transition rule also includes staying at $x$. For discrete states,

$$
T(x\to x)=1-\sum_{y\ne x}q(y\mid x)A(x,y).
$$

Detailed balance requires

$$
\boxed{p(x)T(x\to x')=p(x')T(x'\to x).}
$$

Each side is the probability at the starting state multiplied by the chance of moving to the other state: **the probability flow**. The transition probabilities themselves generally differ.

For example, if $p(x)=0.2$ and $p(x')=0.8$, the transitions $T(x\to x')=0.5$ and $T(x'\to x)=0.125$ balance:

$$
0.2(0.5)=0.8(0.125)=0.1.
$$

There is four times as much probability at $x'$, so a four-times-smaller chance of leaving toward $x$ gives equal flow.

**Stationary** means that starting with distribution $p$ leaves the distribution equal to $p$ after one step. For a discrete chain, summing detailed balance over starting states proves this:

$$
\sum_x p(x)T(x\to x')
=p(x')\sum_x T(x'\to x)
=p(x').
$$

Detailed balance is sufficient for stationarity, but stationarity alone does not require pairwise balance. Nor does stationarity alone guarantee convergence from any initial state. For example, in a finite chain, irreducibility and aperiodicity ensure convergence to its unique stationary distribution.

## 2. Why always accept when the ratio exceeds one?

![[raw/assets/2026-11-06-Metropolis-Hastings-I01-acceptance-derivation.png]]

*My original handwritten derivation, supplied in the first exchange (displayed page 21/38). The clean equations below distinguish the required acceptance-probability ratio from the particular Metropolis–Hastings choice.*

Substitute $T=qA$ into detailed balance:

$$
p(x)q(x'\mid x)A(x,x')
=p(x')q(x\mid x')A(x',x).
$$

For positive target and proposal factors in both directions,

$$
\frac{A(x,x')}{A(x',x)}
=\frac{p(x')q(x\mid x')}{p(x)q(x'\mid x)}
\equiv r.
$$

$A$ is an **acceptance probability**; $r$ is the **Metropolis–Hastings ratio**. It specifies the ratio of forward and reverse acceptance probabilities, not a “ratio of acceptance ratios.”

My handwritten reasoning correctly identifies $r>1$ with a larger forward acceptance probability. But this does not alone force it to equal one: for $r=2$, both $(A_{\rm forward},A_{\rm reverse})=(1,0.5)$ and $(0.8,0.4)$ satisfy the ratio. Metropolis–Hastings chooses the largest compatible probabilities:

$$
\boxed{A(x,x')=\min(1,r),\qquad A(x',x)=\min(1,1/r).}
$$

The reason is direct: writing $a=rb$ with $a,b\leq1$ gives $a\leq\min(1,r)$, and the displayed choice attains that limit. Substitution makes the flow in either direction equal to

$$
\min\{p(x)q(x'\mid x),\ p(x')q(x\mid x')\}.
$$

So the rule balances the pair exactly. A larger $A$ alone need not mean a larger actual transition $T$, because proposals can have different probabilities.

## 3. What cancels, and does a larger ratio mean a more likely state?

*My follow-up question, paraphrased:* Once normalization cancels, can we calculate the ratio, always accept a more probable candidate, and sometimes accept a less probable one?

Suppose the target is known up to a constant:

$$
p(x)=\frac{\widetilde p(x)}{Z},\qquad
Z=\int\widetilde p(u)\,du,\qquad 0<Z<\infty.
$$

Use a sum for a discrete target. We assume the nonnegative unnormalized value $\widetilde p(x)$ is evaluable; the normalized $p(x)$ may remain unavailable. The ratio is nevertheless exact:

$$
r=\frac{[\widetilde p(x')/Z]q(x\mid x')}
{[\widetilde p(x)/Z]q(x'\mid x)}
=\boxed{\frac{\widetilde p(x')q(x\mid x')}
{\widetilde p(x)q(x'\mid x)}}.
$$

**Only the shared constant cancels.** We still need the unnormalized target values and the proposal ratio.

If the proposal is symmetric, $q(x'\mid x)=q(x\mid x')$, then

$$
r=\frac{\widetilde p(x')}{\widetilde p(x)}
=\frac{p(x')}{p(x)}.
$$

In that case my interpretation holds: always accept a move to equal or greater target mass/density; accept a lower one with probability equal to its relative mass/density. For continuous states, this compares densities, not probabilities of exact points.

With an asymmetric proposal, $r>1$ still means always accept, but it need not mean $p(x')>p(x)$: the reverse-to-forward proposal factor also matters.

| Computed ratio | Acceptance probability | Decision |
| --- | --- | --- |
| $r\geq1$ | $1$ | Always accept the proposed candidate. |
| $0<r<1$ | $r$ | Accept with probability $r$. |
| $r=0$ | $0$ | Reject. |

For $r=0.3$, draw an independent $U\sim\operatorname{Uniform}(0,1)$ and accept if $U<0.3$; otherwise stay at $x$. Start in positive target support and apply the formula to a candidate with positive forward proposal probability, so its denominator is positive. A zero numerator gives rejection; the reciprocal-ratio derivation above concerns positive factors.

Accepting some moves toward lower density lets the chain represent less likely regions as well as peaks. The aim is to sample the distribution, rather than only locate its maximum.

## Connections

- [[Backbone/Probability & mathematical foundations/Stochastic processes/Discrete-time stochastic models/Markov chains/Detailed balance|Detailed balance]] — The pairwise flow condition determines the ratio that the acceptance probabilities must satisfy.
- [[Backbone/Probability & mathematical foundations/Stochastic processes/Discrete-time stochastic models/Markov chains/Stationary distributions|Stationary distributions]] — Summing balanced pairwise flows explains why the target is preserved, while separating invariance from convergence.

## Origin

> [!info]- Source details
> The first two MCMC exchanges in chat `01a1af44-f303-7950-bae5-59d4a7728853`, beginning “here were some of the original notes I took from Markov Chain Monte Carlo Sampling” and “I see so in this case p(x) will be actually calculatable”, plus the original handwritten image above. The handwriting and normalization-cancellation intuition are mine. The distinctions between flows and transitions, probability and ratio, symmetry and general proposals, and normalized and unnormalized targets are assistant clarifications. The stationarity proof and explicit bound on the acceptance pair are added synthesis.
>
> Verification: checked the balance algebra, rejection/stay probability, positive-factor ratio conditions, shared-constant cancellation, symmetric-proposal specialization, and the two-state example. Exact scope and image hash are recorded in [[_system/Digest Checkpoints]].
