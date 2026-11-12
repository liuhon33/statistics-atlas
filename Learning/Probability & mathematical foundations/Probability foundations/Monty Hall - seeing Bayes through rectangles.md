---
id: learning-monty-hall-bayes-rectangles
title: Monty Hall - seeing Bayes through rectangles
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule]]'
subject: probability
backbone_path: Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule
study_band: U–M
note_types: [question, derivation, insight]
question_roles: [mechanism, assumption-boundary, cross-topic-connection]
source_format: conversation
created: 2026-11-11
updated: 2026-11-12
status: active
verification: checked
learning_state: unknown
aliases: [Monty Hall problem, Monte Hall]
tags: [atlas/learning, subject/probability, topic/bayes]
connections:
  - '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO]]'
sources:
  - '[[_system/Sources/prob]]'
---

# Monty Hall - seeing Bayes through rectangles

Probability & mathematical foundations → Probability foundations → Probability models → Conditional probability → Bayes rule

## 1. The problem and the tempting 50–50 answer

There are **three doors**, one hiding a car and two hiding goats. The car is equally likely behind each door. You choose door 1. Monty knows where the car is, always opens an unchosen goat door, and always offers you the chance to switch. If he can choose between two goat doors, he uses a fair coin.

He opens door 3 and shows a goat. **Should you keep door 1 or switch to door 2?**

A common response is: two doors remain, so each must now have probability $1/2$. Another response says your initial choice had probability $1/3$, so switching must have probability $2/3$. The second answer is correct under the stated rules, but “the original probability stays the same” needs an explanation.

The confusion is that **two possible outcomes need not be equally likely**. Door 1 survived because you selected it; door 2 survived the host's informed selection. The host's behavior depends on where the car is. Treating his reveal as merely deleting an arbitrary door loses that information. The standard setup and competing intuitions are discussed in [Stark's SticiGui, “The Monty Hall Problem”](https://www.stat.berkeley.edu/~stark/SticiGui/Text/montyHall.htm).

*My requested comparison, paraphrased:* start with the puzzle and its confusing intuition, make the 100-door version clear, then use 3Blue1Brown-style rectangles to see precisely why the answer follows.

## 2. First stretch the intuition to 100 doors

There is still one car, now behind one of 100 equally likely doors. Pick door 1. Your initial chance is $1/100$; the chance that the car is somewhere among the other 99 doors is $99/100$.

Monty knows the car's location and opens **98 unchosen goat doors**, leaving your door and one other closed door. He always offers the switch.

![[assets/figures/2026-11-11-bayes-rectangles/06-hundred-doors.svg]]

*Original probability bar. Blue represents your initial choice; amber represents all 99 other initial car locations. The bar describes the initial groups and the success of the always-switch strategy, before conditioning on which particular other door remains.*

Consider the two exhaustive cases:

| Your first choice | Probability | What Monty must leave | Result of switching |
| --- | --- | --- | --- |
| The car | $1/100$ | One of the 99 goats | Lose |
| A goat | $99/100$ | The car, because he only opens goats | Win |

**Switching wins exactly when the first choice was wrong.** Its success probability is $99/100$. With three doors, the same argument gives $2/3$.

Monty has effectively searched the other group while being forbidden to remove its car. This is why the last remaining alternative is compelling. No physical transfer of probability between doors is needed.

This strategy calculation does not require uniform tie-breaking: any informed rule that always leaves one unchosen door and offers the switch gives the same overall win rate. To calculate a posterior after observing a *particular named survivor*, we also need the tie-breaking rule. The rectangle argument makes that distinction visible.

## 3. Now draw the three-door rectangle

Use the [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule#2. How it works — width, height, retained area|width × likelihood-height construction]]. A column represents a possible car location; positions within it encode the host's possible choices. The whole rectangle represents complete game outcomes, **including the host's behavior**.

Let $C_i$ mean the car is at door $i$, and let

$$
E=\{\text{Monty opens door 3 and shows a goat}\}.
$$

Our initial selection of door 1 is fixed throughout. Before the reveal, each column has width $P(C_i)=1/3$. To set each retained height, ask: **if the car were here, how often would this exact observation occur?**

| Hypothesis | Host's available action | Height $P(E\mid C_i)$ | Retained area $P(C_i\cap E)$ |
| --- | --- | --- | --- |
| $C_1$: your door has the car | May open 2 or 3; fair coin | $1/2$ | $1/6$ |
| $C_2$: the other closed door has the car | Must open 3 | $1$ | $1/3$ |
| $C_3$: the opened door has the car | Cannot open 3 and show a goat | $0$ | $0$ |

![[assets/figures/2026-11-11-bayes-rectangles/04-monty-rectangles.svg]]

*Original analytic illustration applying the rectangle idea to Monty Hall. All three prior columns have equal width. Evidence retains half the blue column, all the amber column, and none of the third column. The lower bar renormalizes only the retained areas.*

The total retained area is

$$
P(E)=\frac16+\frac13+0=\frac12.
$$

So

$$
P(C_1\mid E)=\frac{1/6}{1/2}=\frac13,
\qquad
P(C_2\mid E)=\frac{1/3}{1/2}=\frac23.
$$

**You can read the answer before doing the division:** the surviving amber area is twice the surviving blue area. Equal initial widths did not survive equal filtering.

There is also a six-case counting view. Pair each of the three car locations with two equally likely fair-coin outcomes. If the host has only one legal door, both coin outcomes give that same action. Among the three cases consistent with opening door 3, one has the car at 1 and two have it at 2. These cases are the rectangle divided into six equal cells.

### The same rectangle works with 100 doors

Suppose the observed survivor is specifically door 2, and when your initial choice has the car, Monty chooses the surviving goat uniformly among the other 99 doors. Let $E_{100}$ mean he leaves 2 closed and reveals goats behind 3 through 100, ignoring reveal order.

- If the car is at 1, this happens with probability $1/99$.
- If the car is at 2, this happens with probability 1.
- If it is at any door 3 through 100, this event is impossible.

The two retained areas are $1/(100\cdot99)$ and $1/100$: a ratio of **1 to 99**. Normalizing gives $1/100$ for staying and $99/100$ for switching. The large-door intuition and the Bayes calculation agree under the stated symmetric rule.

## 4. Where the 50–50 calculation actually belongs

Change one rule: the host **does not know where the car is**. He randomly opens door 2 or 3, each with probability $1/2$, even if that reveals the car. We happen to observe the same event $E$: door 3 opens and contains a goat.

Now the likelihood heights are $(1/2,1/2,0)$. The first two surviving areas are both $1/6$, so their posterior shares are both $1/2$.

![[assets/figures/2026-11-11-bayes-rectangles/05-host-comparison.svg]]

*Original comparison with identical priors and the identical observed event. Only the observation mechanism changes. A blind host sometimes exposes the car; those games are excluded when conditioning on a goat reveal.*

The physical scene after the reveal looks the same. Its evidential meaning differs because it was generated differently. A correct Bayes calculation therefore needs a model of **how the observation was selected**.

### An informed but biased host

Let $t=P(E\mid C_1)$: when both unchosen doors are goats, Monty opens 3 with probability $t\in[0,1]$. He still always opens an unchosen goat and always offers the switch. The heights are $(t,1,0)$, giving

$$
P(C_1\mid E)=\frac{t}{1+t},\qquad
P(C_2\mid E)=\frac{1}{1+t}.
$$

The familiar answer uses $t=1/2$. If $t=1$, this particular reveal produces $1/2$ versus $1/2$, even though the host is informed. If $t=0$, opening 3 proves that the car is at 2. Across *all* reveals, always switching still wins $2/3$, because it still wins exactly when the first choice was wrong.

```atlas-interactive
path: assets/figures/2026-11-11-bayes-rectangles/monty-explorer.html
title: Monty Hall — change the host, watch the retained rectangles
height: 1100
```

*Start with the standard host, switch to the blind host, then return and change the informed host's choice probability. The evidence stays “opens door 3 and shows a goat.” Predict the heights before comparing the posterior readouts.*

[[assets/figures/2026-11-11-bayes-rectangles/monty-explorer.html|Open the offline Monty Hall explorer]].

## 5. The connection to ELBO — normalize, or fit the normalized shares

Monty's car location is a hidden variable $z$ and the reveal is observed data $x$. Under the standard rules, the joint weights are

$$
(a_1,a_2,a_3)=\bigl(p(C_1,E),p(C_2,E),p(C_3,E)\bigr)
=\left(\frac16,\frac13,0\right).
$$

Their sum is $p(E)=1/2$, and their normalized shares are the posterior $(1/3,2/3,0)$. For three doors we can compute this exactly; **variational inference is unnecessary here**, but this is a small transparent example of its target.

Suppose we nevertheless describe a trial posterior by $q=(r,1-r,0)$. Then

$$
\begin{aligned}
\mathcal L(r)
&=r\log\frac{1/6}{r}+(1-r)\log\frac{1/3}{1-r}\\
&=\log\frac12
-D_{\mathrm{KL}}\!\left((r,1-r)\,\middle\|\,(1/3,2/3)\right).
\end{aligned}
$$

The maximum is at $r=1/3$. At the intuitive but incorrect $r=1/2$, the posterior KL is $\tfrac12\log(9/8)\approx0.0589$ nats, and the ELBO is approximately $-0.7520$, below $\log(1/2)\approx-0.6931$.

The zero in the third rectangle matters: assigning $q_3>0$ to a state with $a_3=0$ makes posterior KL infinite and the ELBO $-\infty$. A zero-probability explanation cannot receive positive variational mass in a finite-ELBO approximation.

This is the [[Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO#2. Posterior KL: identify exactly what the bound leaves out|posterior-KL identity]] from my earlier ELBO note, now with visible areas for every term. The [[Backbone/Probability & mathematical foundations/Probability foundations/Probability models/Conditional probability/Bayes rule#3. Deeper understanding — Bayes becomes variational inference|Bayes reference's Steve example]] works through the derivative, both KL targets, Jensen, and adjustable $q$ in more detail.

## 6. The Bayes update in my diffusion guidance notes

### 6.1 Infer the previous noisy state

The lecture's [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#5.1 Condition on the known clean training image|Gaussian training posterior]] is another direct instance of the same update. Keep the clean training image $x_0$ fixed, observe $x_t$, and infer the preceding state $u=x_{t-1}$:

$$
q(u\mid x_t,x_0)
=\frac{\underbrace{q(u\mid x_0)}_{\text{distribution before seeing }x_t}
\underbrace{q(x_t\mid u)}_{\text{likelihood of the new noisy state}}}
{\underbrace{q(x_t\mid x_0)}_{\text{normalizer}}}.
$$

The forward Markov property removes $x_0$ from the likelihood once $u$ is given. Each candidate previous state is reweighted by how well it could produce the observed next state. For $t\geq2$, the two factors in the numerator are known Gaussian functions of $u$; their product can be normalized by completing the square. This is the continuous-density counterpart of retaining and renormalizing the rectangles.

During generation, the clean $x_0$ is unknown. The desired reverse law instead uses the noisy-data marginal $q(u)$ in place of $q(u\mid x_0)$, as explained in [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#3. The reverse model|the reverse-model section]]. That marginal can be complicated. Having an analytic training posterior does not supply an analytic unconditional reverse law.

### 6.2 Reweight noisy images by a desired label

My lecture note uses Bayes' rule in the [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Diffusion models - Lecture 12 derivations and guided generation#9.3 Derive the classifier-free gradient identity|classifier-free guidance derivation]]. The same weighting has different objects:

| Role | Monty Hall | Diffusion conditioning at time $t$ |
| --- | --- | --- |
| Unknown being reweighted | Car location $C_i$ | Noisy image $x_t$ |
| Evidence held fixed | Particular goat reveal $E$ | Desired label or condition $y$ |
| Distribution before this evidence | $P(C_i)$ | Unconditional noisy-image density $p_t(x_t)$ |
| Likelihood | $P(E\mid C_i)$ | $p_t(y\mid x_t)$ |
| Updated distribution | $P(C_i\mid E)$ | $p_t(x_t\mid y)$ |

For a discrete label $y$ with $p(y)>0$,

$$
p_t(x_t\mid y)=\frac{p_t(x_t)p_t(y\mid x_t)}{p(y)}.
$$

Here “prior” means before conditioning on $y$ at this noise level; it is **not necessarily the terminal Gaussian** used to start generation. Also, $x_t$ is continuous: infinitesimal prior masses $p_t(x_t)\,dx_t$ replace finite-width columns.

The likelihood raises the relative weight of noisy images compatible with $y$. Taking logs turns multiplication into addition. Where the consistent densities are positive and differentiable, differentiate with respect to $x_t$:

$$
\underbrace{\nabla_{x_t}\log p_t(x_t\mid y)}_{g_c}
=\underbrace{\nabla_{x_t}\log p_t(x_t)}_{g_u}
+\nabla_{x_t}\log p_t(y\mid x_t).
$$

The normalizer $p(y)$ disappears from this derivative because it does not vary with $x_t$. Rearranging gives the lecture's $\nabla\log p_t(y\mid x_t)=g_c-g_u$.

So **the rectangle picture explains the reweighting; the score equation describes its local direction in image space**. With the lecture's convention, guidance uses $g_s=g_u+s(g_c-g_u)$. At $s=1$ this is the exact conditional score for consistent distributions; at $s>1$ it amplifies the likelihood direction. Formally, at a fixed time it is the score of a density proportional to $p_t(x_t)p_t(y\mid x_t)^s$, when normalizable. Neural score estimates and a finite-step sampler add approximation; this fixed-time statement alone does not establish an exact final-image sampling law.

## Connections

- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Approximate & latent-variable inference/Variational inference/ELBO|ELBO]] — Monty's retained areas make the joint weights, evidence normalizer, posterior target and variational support restriction explicit in a three-state model.

## Origin

> [!info]- Source details
> User-requested digest on 2026-11-11: explain Monty Hall in the order problem → common confusion → 100 doors → rectangles, then relate it to ELBO and the Bayes step in the diffusion notes. “My requested comparison” is a labeled paraphrase of that request. The worked calculations, host-policy variants, diagrams and explanations are agent-added synthesis; no handwriting or problem screenshot was supplied in this chat.
>
> Visual inspiration: Grant Sanderson's [Bayes video at 8:44](https://www.youtube.com/watch?v=HZGCoVF3YvM&t=524s) and the [official lesson's area section](https://www.3blue1brown.com/lessons/bayes-theorem/#thinking-with-area), read through its written adaptation. The new Monty Hall figures are original illustrations, not frames recovered from the video. The game setup was checked against the cited university material; the variants are explicitly derived here.
>
> The two existing learning notes linked in §§5–6 provide the earlier ELBO and diffusion context. This digest does not ingest their earlier conversations again. Exact enumeration, the $n$-door and biased-host identities, ELBO arithmetic, and figure geometry are checked in [[assets/figures/2026-11-11-bayes-rectangles/build_figures.py|the reproducible generator]] and its companion checks. The diffusion formula follows directly by logarithmic differentiation of Bayes' rule under the stated conditions.
