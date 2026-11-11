---
id: learning-gamblers-problem-analytic-probability
title: Gamblers problem - probability, martingales, and bold play
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Stochastic processes/Discrete-time stochastic models/Random walks & martingales/Random walks & martingales]]'
subject: probability
backbone_path: Probability & mathematical foundations → Stochastic processes → Discrete-time stochastic models → Random walks & martingales
study_band: U–M
note_types: [derivation, practice, insight]
question_roles: [reconcile-approaches, assumption-boundary]
source_format: conversation
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
aliases: [Analytical gambler problem, Gambler ruin and optimal stakes, Bold play and optional stopping]
tags: [atlas/learning, subject/probability, topic/martingales]
connections:
  - '[[Learning/Statistical computing & learning/Statistical learning & prediction/Gamblers problem - learning an optimal betting policy]]'
sources:
  - '[[raw/assets/2026-11-11-RL-video-gambler-18m36.jpg]]'
  - 'https://arxiv.org/pdf/math/0412362'
  - 'https://ocw.mit.edu/courses/18-440-probability-and-random-variables-spring-2014/95835880b8b2c186229980f4622897df_MIT18_440S14_Lecture35.pdf'
  - 'https://www.randomservices.org/random/games/Bold.html'
  - 'https://www.stat.uchicago.edu/~yibi/teaching/stat317/2021/Lectures/Lecture24.pdf'
---

# Gambler’s problem - probability, martingales, and bold play

Probability & mathematical foundations → Stochastic processes → Discrete-time stochastic models → Random walks & martingales

**Can we solve the same betting problem analytically, rather than by value iteration?** Yes. First-step conditioning gives equations; martingales turn suitable solutions into proofs. The important distinction is that **the familiar gambler’s-ruin formula evaluates “always bet 1”—it does not automatically solve the problem of choosing the stake.**

This is the probability-theory companion to [[Learning/Statistical computing & learning/Statistical learning & prediction/Gamblers problem - learning an optimal betting policy|the reinforcement-learning note]]. The main calculation below solves the original discrete betting model exactly. The final stochastic-calculus section is a related continuous model, not a replacement for it.

## 1. State the problem precisely

Start with integer capital $S_0=s$, where $1\le s<N$. The original example has **target $N=100$** and **win probability $p=0.4$**; write $q=1-p=0.6$.

Before each independent coin flip, choose an integer stake

$$
1\le A_n\le \min(S_n,N-S_n).
$$

Then

$$
S_{n+1}=
\begin{cases}
S_n+A_n,&\text{with probability }p,\\
S_n-A_n,&\text{with probability }q.
\end{cases}
$$

The stake may depend on everything already observed, but not on the next flip. Write $\mathcal F_n$ for that information, including any independent randomization used to select the current stake. Thus $A_n$ is known given $\mathcal F_n$, and the next flip is independent of $\mathcal F_n$.

Stop at

$$
\tau=\inf\{n\ge0:S_n\in\{0,N\}\}.
$$

After stopping, hold the capital fixed. Our objective is

$$
V^*(s)=\sup_\pi\Pr_s^\pi(S_\tau=N),
$$

where $\pi$ ranges over these admissible betting strategies. There is no time discount, and success means reaching $N$ **before ruin**. We use boundary values $V(0)=0$, $V(N)=1$; there is no extra terminal reward to add.

> [!example]- The same original problem statement
> ![[raw/assets/2026-11-11-RL-video-gambler-18m36.jpg]]
> *Reused unchanged from the RL note. The visible lecture frame states target 100, $p(H)=0.4$, and positive integer stakes.*

**Why does play end?** From any interior state, $N-1$ consecutive losses force ruin because each loss removes at least one unit. Consequently, for every admissible policy,

$$
\Pr_s^\pi\{\tau>k(N-1)\}
\le (1-q^{N-1})^k\longrightarrow0.
$$

So $\tau<\infty$ almost surely. Also $0\le S_{n\wedge\tau}\le N$. These are the facts that will justify our stopping arguments—not merely the phrase “apply optional stopping.”

## 2. First solve the simpler problem: always bet one unit

Let

$$
u_s=\Pr_s(\text{reach }N\text{ before }0\mid A_n=1\text{ until stopping}).
$$

### Step 1 — condition on the first flip

From $s$, a win leaves $s+1$ and a loss leaves $s-1$. Therefore

$$
u_s=p\,u_{s+1}+q\,u_{s-1},
\qquad 1\le s<N,
$$

with $u_0=0$ and $u_N=1$. The probabilities describe **eventual success**, not just the next win.

### Step 2 — turn a second-order recurrence into a first-order one

Since $p+q=1$,

$$
\begin{aligned}
p\,u_{s+1}-(p+q)u_s+q\,u_{s-1}&=0,\\
p(u_{s+1}-u_s)&=q(u_s-u_{s-1}).
\end{aligned}
$$

Define the successive differences $d_s=u_s-u_{s-1}$ and $r=q/p$. Then

$$
d_{s+1}=r\,d_s,
\qquad
d_s=r^{s-1}d_1.
$$

### Step 3 — sum the differences and use the boundary

Because $u_0=0$,

$$
u_s=\sum_{j=1}^s d_j
=d_1\sum_{j=0}^{s-1}r^j.
$$

For $p\ne q$, the geometric sum gives

$$
u_s=d_1\frac{1-r^s}{1-r},
\qquad
1=u_N=d_1\frac{1-r^N}{1-r}.
$$

Dividing the first expression by the second eliminates $d_1$:

$$
\boxed{
u_s=\frac{1-(q/p)^s}{1-(q/p)^N}
\quad(p\ne\tfrac12).
}
$$

For $p=q=\tfrac12$, all differences are equal. Since they sum to 1 over $N$ steps, $d_1=1/N$, so

$$
\boxed{u_s=s/N\quad(p=\tfrac12).}
$$

**Examples at $p=0.4$.**

- Target 10, start 3: $u_3=2432/58025\approx0.041913$.
- Target 100, start 30:

$$
u_{30}=\frac{1-1.5^{30}}{1-1.5^{100}}
\approx4.7164\times10^{-13}.
$$

Keeping the same starting fraction $s/N=0.3$ does **not** preserve the unit-stake success probability. The unit stake is much smaller relative to the larger goal.

![[assets/figures/2026-11-11-gambler-analytic/01-fixed-versus-optimal.svg]]

*Original exact-model comparison, with lines joining integer capital states. Orange evaluates always betting 1; blue evaluates the optimal bold policy derived below. The dashed line is the supermartingale upper bound $s/N$, not the subfair optimal value.*

## 3. A second derivation: find a martingale and stop it

A **martingale** is an integrable process whose conditional expected next value equals its current value. A **supermartingale** has conditional expected next value no larger than its current value. These are statements about conditional expectations, not claims that every path stays flat or decreases.

The bounded-martingale stopping principle is reviewed in [Sheffield, MIT 18.440 Lecture 35, slides 4–5 and 11](https://ocw.mit.edu/courses/18-440-probability-and-random-variables-spring-2014/95835880b8b2c186229980f4622897df_MIT18_440S14_Lecture35.pdf#page=11). Here we can see the needed boundedness directly.

### Step 1 — transform biased capital into a martingale

For **unit stakes**, take $r=q/p$ and $M_n=r^{S_{n\wedge\tau}}$. Before absorption,

$$
\begin{aligned}
\mathbb E[M_{n+1}\mid\mathcal F_n]
&=p\,r^{S_n+1}+q\,r^{S_n-1}\\
&=r^{S_n}\left(pr+\frac qr\right)\\
&=r^{S_n}(q+p)\\
&=M_n.
\end{aligned}
$$

After absorption it is constant. Thus the stopped process is a martingale.

### Step 2 — justify the limit, rather than assume it

For every $n$,

$$
\min(1,r^N)\le M_n\le\max(1,r^N).
$$

Hence $\mathbb E[M_n]=r^s$, and almost-sure absorption plus bounded convergence gives

$$
\mathbb E[r^{S_\tau}]
=\lim_{n\to\infty}\mathbb E[M_n]
=r^s.
$$

### Step 3 — only two terminal values remain

On success, $r^{S_\tau}=r^N$; on ruin, it is 1. Therefore

$$
r^s=u_s r^N+(1-u_s),
$$

$$
u_s(r^N-1)=r^s-1,
\qquad
u_s=\frac{r^s-1}{r^N-1}.
$$

This is exactly the formula in §2. For the fair coin, use $S_{n\wedge\tau}$ itself instead: $\mathbb E[S_\tau]=s=N u_s$.

### What survives when the stake is allowed to change?

For an arbitrary legal stake,

$$
\mathbb E[S_{n+1}-S_n\mid\mathcal F_n]=(p-q)A_n.
$$

Thus:

- **Fair coin:** stopped capital is a bounded martingale under every admissible policy. Every policy has success probability $s/N$.
- **Unfavorable coin:** stopped capital is a bounded supermartingale, so

$$
N\Pr_s^\pi(S_\tau=N)=\mathbb E_s^\pi[S_\tau]\le s.
$$

But **this is only an upper bound**. It does not identify the best policy when $p<1/2$.

Also, the unit-stake exponential calculation does not carry over unchanged:

$$
\mathbb E[r^{S_{n+1}}\mid\mathcal F_n]
=r^{S_n}\bigl(pr^{A_n}+qr^{-A_n}\bigr).
$$

The bracket equals 1 for $A_n=1$, but generally not for larger stakes. This is why inserting the unit-stake ruin formula into the controlled problem is not a solution.

## 4. Solve the original unfavorable game using bold play

For the even-payout model with fixed $0<p<1/2$, **bold play is an optimal policy**:

$$
\boxed{a_{\rm bold}(s)=\min(s,N-s).}
$$

Below halfway, stake the entire current capital. Above halfway, stake just enough to reach the goal on a win. At halfway, stake everything. This is the Dubins–Savage result; it also applies to integer fortunes and stakes. See [Schweinsberg, introduction, pp. 1–2](https://arxiv.org/pdf/math/0412362#page=1).

Do not mistake the intuition—avoiding repeated exposure to an unfavorable coin—for a proof. We will both calculate this policy’s value and verify its optimality for the models used here.

### Step 1 — write the success equations for this policy

Let $W(s)$ be the probability of success under bold play. Then

$$
W(0)=0,\qquad W(N)=1,
$$

$$
\boxed{
W(s)=
\begin{cases}
p\,W(2s),&0<s<N/2,\\
p,&s=N/2,\\
p+q\,W(2s-N),&N/2<s<N.
\end{cases}
}
$$

The middle case exists only when $N/2$ is an integer. Why these equations?

- Below halfway, a loss is immediate ruin; only a win continues.
- Above halfway, a win is immediate success; only a loss continues.

There is only **one nonterminal continuation branch** at each state. That makes exact algebra much easier than solving for all possible stakes simultaneously.

### Step 2 — work through start 30, target 100

The states that matter are $30,60,20,40,80$. The policy gives

$$
\begin{aligned}
W(30)&=pW(60),\\
W(60)&=p+qW(20),\\
W(20)&=pW(40),\\
W(40)&=pW(80),\\
W(80)&=p+qW(60).
\end{aligned}
$$

![[assets/figures/2026-11-11-gambler-analytic/02-bold-cycle.svg]]

*The continuing branches form a loop; the other branch at each state ends at 0 or 100. Returning to a state means the same remaining success probability applies again.*

Substitute one line at a time:

$$
\begin{aligned}
W(60)
&=p+qW(20)\\
&=p+qpW(40)\\
&=p+qp^2W(80)\\
&=p+qp^2\bigl[p+qW(60)\bigr]\\
&=p+qp^3+p^2q^2W(60).
\end{aligned}
$$

Move the repeated unknown to the left:

$$
(1-p^2q^2)W(60)=p+qp^3,
$$

$$
W(60)=\frac{p+qp^3}{1-p^2q^2}.
$$

Finally,

$$
\boxed{
W(30)=pW(60)
=\frac{p^2+qp^4}{1-p^2q^2}
=\frac{548}{2945}
\approx0.1860781.
}
$$

This is about an **18.61% success probability**, compared with $4.72\times10^{-13}$ for always betting one unit.

The denominator has a direct probability interpretation. Starting at 60, success before completing one loop has probability $p+qp^3$, and completing the loop has probability $p^2q^2$. Therefore

$$
W(60)
=(p+qp^3)\bigl[1+p^2q^2+(p^2q^2)^2+\cdots\bigr].
$$

We have summed all possible numbers of loops, not truncated the game after a few flips.

### Step 3 — compute any starting capital the same way

For integer $N$, follow the single continuing branch. It either reaches a boundary or revisits one of the finitely many states. Each equation has the form

$$
W(s_j)=c_j+d_jW(s_{j+1}),
$$

where $(c_j,d_j)$ is $(0,p)$ below halfway and $(p,q)$ above halfway. Around a cycle of length $m$, substitution gives

$$
W(s_0)=C+D W(s_0),
$$

$$
C=c_0+d_0c_1+d_0d_1c_2+\cdots+
\left(\prod_{j=0}^{m-2}d_j\right)c_{m-1},
\qquad
D=\prod_{j=0}^{m-1}d_j<1.
$$

So $W(s_0)=C/(1-D)$, followed by back-substitution. For rational $p$, every value obtained this way is rational. This is a finite exact calculation, not a convergence-tolerance rule.

> [!info]- An explicit series for every starting fraction
> Normalize capital by the target: $x=s/N$ and $B(x)=W(s)$. Bold trajectories scale with the target, giving
> $B(x)=pB(2x)$ below halfway and $B(x)=p+qB(2x-1)$ above halfway. This self-similarity and its binary interpretation are developed in [Siegrist, Bold Play, “The Probability of Winning” and “Binary Expansions”](https://www.randomservices.org/random/games/Bold.html).
>
> Write $x=0.b_1b_2\ldots$ in binary, using the terminating expansion when available, and set $c_0=p$, $c_1=q$. Removing the first bit gives
> $B(x)=p b_1+c_{b_1}B(0.b_2b_3\ldots)$.
>
> Repeated substitution yields the explicit expression
>
> $$
> B(x)=\sum_{k=1}^{\infty}p\,b_k\prod_{j=1}^{k-1}c_{b_j},
> \qquad B(0)=0,\quad B(1)=1.
> $$
>
> The empty product is 1. The remainder after $m$ substitutions is at most $\max(p,q)^m$, which tends to zero. Eventually repeating bits can be summed by geometric series—the cycle calculation above in another notation. Under bold play, $W_{100}(30)=W_{10}(3)$ because both start at fraction $0.3$.

## 5. Why this candidate really is optimal

### 5.1 The verification argument

Suppose a function $w$ has $w(0)=0$, $w(N)=1$, $0\le w\le1$, and satisfies

$$
\boxed{p\,w(s+a)+q\,w(s-a)\le w(s)}
$$

for **every legal state and stake**. This means that no first bet, followed by continuation valued at $w$, improves on $w(s)$.

Under any admissible strategy,

$$
\begin{aligned}
\mathbb E[w(S_{(n+1)\wedge\tau})\mid\mathcal F_n]
&\le w(S_{n\wedge\tau}),\\
\mathbb E_s^\pi[w(S_{n\wedge\tau})]
&\le w(s).
\end{aligned}
$$

The first inequality also holds after termination, with equality. It follows for randomized stakes too, since an average of valid inequalities is valid.

Now take $n\to\infty$. Boundedness and almost-sure absorption give

$$
\Pr_s^\pi(S_\tau=N)
=\mathbb E_s^\pi[w(S_\tau)]
\le w(s).
$$

Thus $w$ is an upper bound for **every strategy**, including history-dependent ones.

If a particular policy makes the one-step inequality an equality at every interior state, its transformed capital $w(S_{n\wedge\tau})$ is a martingale. The same limit argument then gives

$$
\Pr_s^{\pi_0}(S_\tau=N)=w(s).
$$

An upper bound that a legal policy achieves is the optimum. This is the probability-theoretic meaning of a Bellman verification argument.

### 5.2 An entirely explicit certificate for target 10

For $p=2/5$, calculate $W$ by the bold equations. Define the loss from choosing stake $a$ once and then continuing boldly:

$$
g(s,a)=W(s)-\left[\tfrac25W(s+a)+\tfrac35W(s-a)\right].
$$

Here is the complete exact check. Each vector lists the gaps for stakes $a=1,2,\ldots,\min(s,10-s)$, in that order.

| Capital $s$ | $2945\,W(s)$ | $2945\,g(s,a)$ for all legal stakes | All optimal stakes |
| ---: | ---: | --- | --- |
| 1 | 128 | $(0)$ | 1 |
| 2 | 320 | $(24,0)$ | 2 |
| 3 | 548 | $(36,0,0)$ | 2, 3 |
| 4 | 800 | $(0,60,60,0)$ | 1, 4 |
| 5 | 1178 | $(150,186,186,150,0)$ | 5 |
| 6 | 1370 | $(0,90,90,0)$ | 1, 4 |
| 7 | 1658 | $(36,0,0)$ | 2, 3 |
| 8 | 2000 | $(54,0)$ | 2 |
| 9 | 2378 | $(0)$ | 1 |

For instance,

$$
\begin{aligned}
g(3,1)
&=\frac{548-\frac25(800)-\frac35(320)}{2945}\\
&=\frac{548-320-192}{2945}
=\frac{36}{2945}>0,\\
g(3,2)
&=\frac{548-\frac25(1178)-\frac35(128)}{2945}
=0.
\end{aligned}
$$

Every gap is nonnegative, and the bold stake has zero gap in every row. Together with §5.1, this proves optimality for **all starting capitals in this target-10 model**, not just for capital 3.

For the original target 100, there are exactly 2,500 legal state–stake pairs. The accompanying [[assets/figures/2026-11-11-gambler-analytic/exact-certificates.json|exact rational certificate]] checks all of them at $p=2/5$, with no floating-point tolerance. The [[assets/figures/2026-11-11-gambler-analytic/check_and_draw.py|reproducible script]] solves the cycles and checks the inequalities. This is a finite exact-arithmetic verification of the specified model; the general all-$N$, all-$p<1/2$ theorem is cited in §4 rather than proved here.

### 5.3 Why the RL policy need not look like bold play

An optimal value function need not have a unique maximizing action. At target 10, capital 3, both stakes 2 and 3 achieve $548/2945$. The earlier explorer selects the smaller tied stake; bold play selects the larger one.

The original target-100 example has the same phenomenon:

$$
\begin{aligned}
Q_{W}(30,20)
&=pW(50)+qW(10)\\
&=\frac25\frac25+\frac35\frac{128}{2945}\\
&=\frac{548}{2945},\\
Q_W(30,30)
&=pW(60)
=\frac{548}{2945}.
\end{aligned}
$$

These are **two** optimal stakes, not necessarily the complete list. With integer stakes, 5 also ties at capital 30. A policy that always chooses a zero-gap action attains $W$ by the same martingale proof.

The [[Learning/Statistical computing & learning/Statistical learning & prediction/Gamblers problem - learning an optimal betting policy#6. What strategy is learned?|RL policy table]] and the analytical bold policy can therefore differ without disagreeing about the best success probability.

### 5.4 What if the coin is favorable?

For completeness, the unit-stake function from §2 is optimal when $p>1/2$. We can prove it with the same verification test.

Now $r=q/p<1$. Define $H(a)=pr^a+qr^{-a}$. Since $H(1)=1$ and

$$
\begin{aligned}
H(a+1)-H(a)
&=pr^a(r-1)+qr^{-a}(r^{-1}-1)\\
&=(p-q)(r^{-a}-r^a)>0\qquad(a\ge1),
\end{aligned}
$$

we have $H(a)\ge1$. Therefore

$$
p\,u_{s+a}+q\,u_{s-a}
=\frac{1-r^s H(a)}{1-r^N}
\le\frac{1-r^s}{1-r^N}
=u_s.
$$

Equality is attained by stake 1, proving its optimality. This relies on the **minimum stake of one unit**.

| Coin | One optimal policy | Optimal success probability |
| --- | --- | --- |
| $0<p<1/2$ | Bold: $\min(s,N-s)$ | $W(s)$ from the exact recurrence/cycles |
| $p=1/2$ | Every admissible policy | $s/N$ |
| $1/2<p<1$ | Timid: always 1 | $\bigl[1-(q/p)^s\bigr]/\bigl[1-(q/p)^N\bigr]$ |

This concerns the stated mathematical objective, not a recommendation to gamble. At $p=0.4$, even an optimal strategy has negative expected net gain: terminal wealth has expectation $NW(s)\le s$.

## 6. Stochastic calculus: the continuous analogue

The discrete model is already solved. To see the related calculus, **change the model explicitly** to

$$
dX_t=\mu\,dt+\sigma\,dB_t,
\qquad X_0=x\in(0,N),\quad \sigma>0,
$$

with constant drift $\mu$, constant diffusion coefficient $\sigma$, and a standard Brownian motion $B_t$. Stop on first reaching 0 or $N$:

$$
T=\inf\{t\ge0:X_t\in\{0,N\}\},
\qquad h(x)=\Pr_x(X_T=N).
$$

Here there is no stake choice: $\mu$ and $\sigma$ are fixed. The corresponding hitting formula is given in [Huang, STAT253/317 Lecture 24, slides 8–10](https://www.stat.uchicago.edu/~yibi/teaching/stat317/2021/Lectures/Lecture24.pdf#page=8); the derivation below uses Itô’s formula.

### Step 1 — make the success function driftless

For a twice continuously differentiable candidate $h$, Itô’s formula gives

$$
dh(X_t)
=\underbrace{\left[\mu h'(X_t)+\frac{\sigma^2}{2}h''(X_t)\right]}_{\text{drift of the transformed process}}dt
+\sigma h'(X_t)\,dB_t.
$$

Set the drift to zero and impose the boundary outcomes:

$$
\frac{\sigma^2}{2}h''(x)+\mu h'(x)=0,
\qquad h(0)=0,\quad h(N)=1.
$$

This differential equation plays the role of the discrete equation
$u_s=pu_{s+1}+qu_{s-1}$.

### Step 2 — solve the differential equation

For $\mu\ne0$, let $k=2\mu/\sigma^2$ and $g=h'$. Then

$$
g'(x)+kg(x)=0
\quad\Longrightarrow\quad
g(x)=C e^{-kx}.
$$

Integrating from 0 to $x$ and using $h(0)=0$,

$$
h(x)=\frac Ck(1-e^{-kx}).
$$

The condition $h(N)=1$ gives $C/k=1/(1-e^{-kN})$. Hence

$$
\boxed{
h(x)=\frac{1-e^{-2\mu x/\sigma^2}}
{1-e^{-2\mu N/\sigma^2}}
\quad(\mu\ne0).
}
$$

For $\mu=0$, $h''=0$, so $h(x)=x/N$.

### Step 3 — verify that the candidate is the hitting probability

On the bounded interval, this candidate and its derivative are bounded. Itô’s formula stopped at $t\wedge T$ therefore gives a true martingale and

$$
\mathbb E_x[h(X_{t\wedge T})]=h(x).
$$

Nondegenerate Brownian motion with constant drift exits a finite interval almost surely. One way to see this is that, over each unit-time block, an increment exceeding $N$ has a fixed positive probability and forces an exit from any surviving interior position. Independent increments give a geometric survival bound. By continuity there is no boundary overshoot, and bounded convergence gives

$$
h(x)=\mathbb E_x[h(X_T)]=\Pr_x(X_T=N).
$$

**The same structure appears again:** construct a harmonic function, stop its martingale, and read off the boundary probabilities.

### Why this is not an exact solution by replacing coin flips with Brownian motion

A Brownian approximation requires a small-step scaling. For jumps of size $\varepsilon=\sigma\sqrt{\Delta t}$, a finite drift $\mu$ requires

$$
p_{\Delta t}
=\frac12+\frac{\mu\sqrt{\Delta t}}{2\sigma}.
$$

Then the expected increment is $\mu\Delta t$, its variance is $\sigma^2\Delta t+o(\Delta t)$, and $p_{\Delta t}\to1/2$. This is not the original model with fixed $p=0.4$ and potentially very large bold stakes. Optimizing a controlled diffusion would also require specifying how the control changes drift and volatility; the fixed-$\mu,\sigma$ ODE alone does not do that.

## 7. What the two notes now say together

| View | Unknown or object | How the solution is obtained |
| --- | --- | --- |
| Fixed-stake probability | $u_s$ | First-step recurrence and a geometric sum |
| Martingale probability | $r^{S_{n\wedge\tau}}$ or $w(S_{n\wedge\tau})$ | Conditional expectation, bounded stopping, terminal values |
| Optimal betting | $W(s)$ and a maximizing stake | Bold-policy cycle equations plus all-action verification |
| RL/model-based planning | Value and policy tables | Repeated Bellman backups or policy evaluation/improvement |
| Continuous analogue | $h(x)$ | Itô’s formula and a boundary-value ODE for a different model |

Probability theory and Bellman planning are not competing theories. The Bellman equation is itself a conditional-probability statement. The difference here is **using structure to calculate and verify the solution directly**, rather than discovering its values by repeated numerical backups.

## Checks and scope

Exact rational checks cover every legal state–stake pair for $N=10,100$ and $p=2/5,1/2,3/5$: 7,575 inequalities in total, with equality for the claimed policies. The unit-stake recurrence, target scaling for bold play, loop formula, optimal-action ties, and the complete table above are checked exactly. The Brownian ODE, boundary conditions and zero-drift limit were checked symbolically. Independent floating-point policy evaluation agrees within $4.45\times10^{-15}$.

See [[assets/figures/2026-11-11-gambler-analytic/check_and_draw.py|reproducible derivation checks and figure generator]], [[assets/figures/2026-11-11-gambler-analytic/checks.json|check summary]], and [[assets/figures/2026-11-11-gambler-analytic/exact-certificates.json|full finite certificates]]. Exact finite verification is distinguished from the cited general bold-play theorem, and both are distinguished from a numerical approximation.

## Connections

- [[Learning/Statistical computing & learning/Statistical learning & prediction/Gamblers problem - learning an optimal betting policy|Gambler’s problem through reinforcement learning]] — solves the same success-probability objective by value/policy iteration; the present martingale verification explains why bold play and different tied greedy policies attain the same value.

## Origin

> [!info]- Source details
> Created separately at the user's explicit request for an analytical probability/stochastic-calculus companion. The question in the opening is an agent paraphrase of that request, not a verbatim quotation. The problem setup and target-10 comparison are inherited from the linked RL note; its original lecture screenshot is reused without modifying or duplicating the file.
>
> All expanded derivations, exact certificates and new figures are agent-added explanations, not transcriptions of the user's handwriting or claims about the lecture's coverage. Read references: Schweinsberg introduction pp. 1–2 for the bold-play theorem and integer-model scope; Sheffield's martingale/stopping definitions and bounded stopping statement; Siegrist's bold recurrence, scaling and binary representation; Huang's Brownian hitting-probability derivation, slides 8–10. The general Dubins–Savage proof is not reproduced. The finite models actually used in these notes have separate exact verification.
>
> Both original SVGs and their generated PNG previews were inspected. No new user attachment or inaccessible prior conversation was ingested. Live Obsidian rendering is not claimed; the draft is left uncommitted for review.
