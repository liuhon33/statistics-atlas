---
id: learning-gamblers-problem-dynamic-programming
title: Gamblers problem - learning an optimal betting policy
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Reinforcement learning]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Reinforcement learning
study_band: M
note_types: [practice, derivation, insight]
source_format: video
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: introduced
aliases: [Gambler's problem, Gambler value iteration, Optimal gambling strategy with dynamic programming]
tags: [atlas/learning, subject/computing, topic/reinforcement-learning]
connections:
  - '[[Learning/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning - from Bellman equations to sampled updates]]'
sources:
  - '[[raw/notes/2026-11-11-Reinforcement-learning-handwritten-notes.pdf]]'
  - '[[raw/articles/2026-11-11-RL-part2-youtube-captions.txt]]'
  - '[[raw/assets/2026-11-11-RL-video-gambler-18m36.jpg]]'
  - '[[raw/assets/2026-11-11-RL-video-gambler-bars.jpg]]'
  - '[[raw/notes/2026-11-11-RL-source-manifest.json]]'
---

# Gambler’s problem - learning an optimal betting policy

Statistical computing & learning → Statistical learning & prediction → Reinforcement learning

## Problem setting

A gambler starts with some whole-number capital between 1 and 99 and wants to reach **100 before going broke**. Each round, the gambler chooses a positive integer stake, then flips an independent biased coin: a win (probability $0.4$) adds the stake, and a loss (probability $0.6$) subtracts it. The stake cannot exceed either the current capital or the amount still needed to reach 100. Play stops at 0 or 100.

For example, with 30 units of capital, betting 20 leaves 50 after a win or 10 after a loss. The next stake can depend on this new capital; the gambler does not commit to a fixed sequence of bets.

The task is to find a **policy**—a rule for how much to bet at each capital level—that maximizes the probability of reaching 100, not the expected profit on the next bet. Here the coin's probability is known, so we can compute the policy from the model rather than learn it by playing games.

> [!info]- RL quick reference
>
> The **agent** is the gambler; the **environment** is the biased coin and the capital-update rule. Keep $N=100$ and $p=0.4$ throughout these examples.
>
> | RL term | Meaning here | Concrete example |
> | --- | --- | --- |
> | **State** $S_t=s$ | Current capital, before the next bet. | $S_t=30$; $0$ and $100$ are terminal states. |
> | **Action** $A_t=a$ | The stake chosen now. | $A_t=20$; at capital 30, legal stakes are $1,\ldots,30$. |
> | **Policy** $\pi$ | The rule for choosing an action in each state. | $\pi(30)=20$ means “bet 20 at capital 30.” A deterministic policy has $\pi(a=20\mid s=30)=1$; this is not the coin's win probability. |
> | **Transition model** | Probabilities of the next state, given state and action. | From $s=30$, $a=20$: next capital is 50 with probability $0.4$, or 10 with probability $0.6$. |
> | **Reward** $R_{t+1}$ | Immediate task feedback: 1 only when a bet reaches 100; otherwise 0. | A win $30\to50$ gives **reward 0**, not 20. A win $50\to100$ gives reward 1; ruin gives reward 0. |
> | **Return** $G_t$ | Total future discounted reward: $R_{t+1}+\gamma R_{t+2}+\cdots$. | Here $G_t=1$ if this episode eventually succeeds, and $0$ if it ends in ruin. |
> | **Discount factor** $\gamma$ | How much later rewards are downweighted. | $\gamma=1$: success later counts just as much as success on the next bet. |
> | **State value** $v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]$ | Expected return when starting at $s$ and following $\pi$: the success probability, not the capital. | Under an optimal policy, $v^*(50)=0.4$: a 40% chance of eventual success. |
> | **Action-value estimate** $Q_V(s,a)$ | Score for taking stake $a$ now, using the table $V$ for what follows. | With optimal continuation, $Q_{V^*}(30,20)\approx0.186078$: about an 18.6% success chance. |
>
> **One possible episode:** bet 20 and win from 30 to 50, then bet 50 and win to reach 100. The rewards are $(0,1)$, so $G_0=0+1=1$. That realized return is either 0 or 1; its expectation across possible episodes is a value such as $0.186078$.
>
> **Read the equation in RL terms.** The note's $V$ table stores success probabilities or current estimates of them; a star marks optimal values. The action score is a weighted average over possible next states:
>
> $$
> Q_V(30,20)
> =\underbrace{0.4\,V(50)}_{\text{win probability × next-state value}}
> +\underbrace{0.6\,V(10)}_{\text{loss probability × next-state value}}.
> $$
>
> At convergence, $V^*(50)=0.4$ and $V^*(10)\approx0.043463$, giving $Q_{V^*}(30,20)\approx0.4(0.4)+0.6(0.043463)\approx0.186078$. These are computed values, not initial guesses. **The value update keeps the best score; the policy keeps an action achieving it:**
>
> $$
> V_{\mathrm{new}}(s)=\max_a Q_V(s,a),
> \qquad
> \pi_{\mathrm{new}}(s)\in\arg\max_a Q_V(s,a).
> $$
>
> **Reward bookkeeping:** ordinary RL uses “immediate reward + discounted future value.” Here the success reward is absorbed into the boundary $V(100)=1$, with $V(0)=0$, so the displayed backup has no separate reward term. Do not add another 1 for reaching 100. The ordinary future-return value *after* termination is zero; the boundary convention is explained below.
>
> **Choose the stake that gives the best chance of reaching the target before ruin.** The useful score for a bet includes what can happen after winning or losing it. Dynamic programming discovers the policy by repeatedly passing those future success probabilities back to the current state.

This note develops the reinforcement-learning approach requested in this chat. The separate [[Learning/Probability & mathematical foundations/Stochastic processes/Gamblers problem - probability, martingales, and bold play|analytical companion]] solves the same problem using probability and martingales, then distinguishes its stochastic-calculus analogue.

## 1. Encode the betting problem as an MDP

The lecture’s example uses a goal $N=100$ and independent coin flips with win probability $p=0.4$. Current capital is $s$. Winning adds the stake; losing subtracts it. The episode stops at $0$ or $N$. [Lecture, 18:14–19:01](https://www.youtube.com/watch?v=_j6pvGEchWU&t=1094s); [Sutton & Barto, Example 4.3 and Exercise 4.9, p. 84](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=106).

> [!example]- Original lecture problem statement
> ![[raw/assets/2026-11-11-RL-video-gambler-18m36.jpg]]
> *Mutual Information, Part 2, captured at the visible player time 18:47. The filename records the requested seek position, 18:36. The board explicitly uses positive integer stakes.*

| MDP component | Definition |
| --- | --- |
| Nonterminal states | $s\in\{1,\ldots,N-1\}$, measured in units of capital |
| Terminal outcomes | $0$: ruin; $N$: success |
| Legal action set | $\mathcal A(s)=\{1,\ldots,\min(s,N-s)\}$ |
| Transition after stake $a$ | $s+a$ with probability $p$; $s-a$ with probability $1-p$ |
| Reward | $1$ on entering $N$; $0$ on every other transition |
| Discount | $\gamma=1$ |
| Objective | Maximize the probability of hitting $N$ before $0$ |

The return is the indicator of eventual success, so for a nonterminal state

$$
v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]
=\Pr_\pi(\text{reach }N\text{ before }0\mid S_t=s).
$$

The objective concerns reaching a threshold, not maximizing the expected change in capital on the next bet. Indeed, that next change has expectation $(2p-1)a=-0.2a$ here, yet choosing only the smallest stake need not maximize the chance of reaching the target.

We exclude a zero stake, following the video. The textbook’s displayed action set includes zero, which permits indefinite waiting and creates an unhelpful self-loop tie. Positive stakes keep the episode terminating under every policy in this finite model. For $0<p<1$, any run of $N-1$ losses must cause ruin; its conditional probability is $(1-p)^{N-1}>0$, giving a geometric bound on survival across blocks.

### Two consistent ways to represent success

With the transition reward above, the ordinary future-return values satisfy $v(0)=v(N)=0$ once the episode is over. Reaching $N$ pays the reward on entry.

For simpler tables, introduce the **success-probability boundary values**

$$
V(0)=0,\qquad V(N)=1.
$$

For nonterminal states, $V$ represents the same success probability as $v$. The entry reward is now absorbed into the boundary, so a backup is simply

$$
\boxed{Q_V(s,a)=pV(s+a)+(1-p)V(s-a).}
$$

This is the convention used throughout the explorer. **Do not add another reward of 1 when using $V(N)=1$; that would count success twice.** The boundary shorthand is specifically the undiscounted probability problem here.

## 2. Keep three different tables straight

| Table | Entry | Role |
| --- | --- | --- |
| Legal-action table | $\mathcal A(s)$ | Which stakes are allowed? This never changes. |
| Action-value table | $Q_V(s,a)$ | What does each stake predict, using the current next-state values? |
| State-value table | $V(s)$ | Current estimate of success probability from capital $s$ |
| Policy table | $\pi(s)$, or probabilities $\pi(a\mid s)$ | Which action will be selected? |

A deterministic policy’s row is one chosen stake. As a probability table, that row has probability 1 at the chosen stake and 0 at the other legal stakes. The action-value row can contain many plausible actions even though the policy chooses only one.

For example, at $s=30$, $N=100$, the legal stakes are $1,\ldots,30$. Stake $20$ leads to $50$ or $10$, so its action value is $0.4V(50)+0.6V(10)$. The algorithm compares this with the value of every other legal stake.

## 3. Watch the tables change

> [!info]- GPI refresher — what the explorer updates and how to read its tables
> **Generalized policy iteration (GPI)** is the interaction of **policy evaluation** (estimate how good the current policy is) and **policy improvement** (use those estimates to choose better actions). “Generalized” means these processes can be interleaved before evaluation is complete. Full policy iteration is the clean evaluate-then-improve version:
>
> $$
> \pi_k
> \xrightarrow{\text{evaluate}} V^{\pi_k}
> \xrightarrow{\text{score bets}} Q_{V^{\pi_k}}
> \xrightarrow{\text{improve}} \pi_{k+1}
> \longrightarrow\cdots
> $$
>
> In this problem, evaluation asks **“What is the success probability if I keep following this betting rule?”** Improvement asks **“Given those future values, which stake looks best at each capital?”** The [[Learning/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning - from Bellman equations to sampled updates#3. Evaluation keeps the policy fixed; improvement changes it|foundations note]] develops the same distinction.
>
> **Read the tables as possible decisions, not a history of played bets.**
> - **Action table:** fix one capital $s$. Each row is a legal stake $a$, its win/loss successor states, and the contributions $0.4V(s+a)$ and $0.6V(s-a)$. Their sum is $Q_V(s,a)$; compare these scores to choose a stake.
> - **Full state and policy table:** each row is a capital $s$. **Current V(s)** is its current success-probability estimate; **Policy/Greedy stake** is a bet in capital units, not a probability; **Best one-step Q** is $\max_a Q_V(s,a)$. In value iteration, that best score becomes the next $V(s)$, so it need not equal the current entry yet.
> - The **legal stakes never change**. Their scores and the chosen stake can change. Blue bars are values, green bars are stakes; a sweep updates all nonterminal states, not one sampled game.
>
> **Numerical GPI chain: choose goal 10, win probability 0.4, and Policy iteration.** Inspect capital $s=3$.
>
> **1. Evaluate the initial rule.** Start with $\pi_0(s)=1$ everywhere. Solve the fixed-policy equations
> $$
> V^{\pi_0}(s)=0.4V^{\pi_0}(s+1)+0.6V^{\pi_0}(s-1),
> \qquad V^{\pi_0}(0)=0,\quad V^{\pi_0}(10)=1.
> $$
> This gives $V^{\pi_0}(3)\approx0.041913$: always betting 1 succeeds from capital 3 about 4.19% of the time. Evaluation changes the value table but leaves the policy unchanged.
>
> **2. Score all three legal bets using that same evaluated table.** Rounded values:
>
> | Stake $a$ | Win contribution + loss contribution | $Q_{V^{\pi_0}}(3,a)$ |
> | ---: | --- | ---: |
> | 1 | $0.4(0.071693)+0.6(0.022059)$ | $0.041913$ |
> | 2 | $0.4(0.116364)+0.6(0.008824)$ | $0.051840$ |
> | 3 | $0.4(0.183369)+0.6(0)$ | $0.073348$ |
>
> **3. Improve the policy, then evaluate again.** The largest score is for stake 3, so this row changes from $\pi_0(3)=1$ to $\pi_1(3)=3$. Improve **every** state's row in the same way. Immediately after improvement, the explorer still displays the old value $0.041913$ at capital 3; the next evaluation gives $V^{\pi_1}(3)\approx0.186078$. Why not $0.073348$? That earlier action score means “bet 3 once, then follow the **old** policy”; the new value follows the **improved policy at every future decision**. Do not overwrite a fully evaluated policy value with just the best one-step score and call it full evaluation.
>
> **The default Value iteration mode interleaves the work more tightly.** It uses $V_k\to Q_k$, then writes $V_{k+1}(s)=\max_a Q_k(s,a)$ and obtains the greedy preview $\pi_{k+1}(s)\in\arg\max_a Q_k(s,a)$, without fully evaluating that policy first. For goal 10 after one sweep, $V_1(1)=\cdots=V_1(4)=0$ and $V_1(5)=V_1(6)=0.4$. At capital 3 the action scores are $(0,0.16,0.16)$ for stakes $(1,2,3)$, so the next sweep changes $V_2(3)$ from 0 to $0.16$, while smallest-stake tie-breaking chooses stake 2. Recomputing from $V_2$ changes the action scores to $(0.064,0.16,0.16)$; the greedy stake remains 2. Values and action scores can change even when the chosen action does not. Here $k$ counts computational sweeps, not bets or episodes.

```atlas-interactive
path: assets/figures/2026-11-11-reinforcement-learning/gambler-explorer.html
title: Gambler learning explorer — values, actions and policy
height: 1800
```

[[assets/figures/2026-11-11-reinforcement-learning/gambler-explorer.html|Open the self-contained explorer]]

Try **goal 10**, keep **win probability 0.4**, and inspect **capital 3**. Advance two sweeps. Before opening the action table, predict which stakes can reach a state whose value is already positive. Then use **Go to converged** to see why stakes 2 and 3 tie at about $0.186078$.

The blue bars show current state values. The green bars show stakes, on a separate vertical scale. The orange highlight identifies the selected state/action. All legal actions and their two weighted contributions appear in the action table; the full state/policy table is expandable. Controls start paused, and the file runs without an internet connection.

![[assets/figures/2026-11-11-reinforcement-learning/01-gambler-values-policy.svg]]

*Original analytic illustration for $N=100$, $p=0.4$. Upper panel: successive synchronous value sweeps. Lower panel: one final greedy policy, using the smallest stake among ties within numerical tolerance. The goal value 1 is a boundary condition.*

## 4. Value iteration: compare actions, then replace each state value

Initialize $V_0(s)=0$ for $1\leq s<N$, and hold the two boundaries fixed. At sweep $k$:

$$
Q_k(s,a)=pV_k(s+a)+(1-p)V_k(s-a),
$$

$$
\boxed{V_{k+1}(s)=\max_{a\in\mathcal A(s)}Q_k(s,a).}
$$

The greedy policy obtained from the displayed table is

$$
\pi_{k+1}(s)\in\arg\max_aQ_k(s,a).
$$

**The explorer displays $V_k$ and its greedy preview $\pi_{k+1}$.** Its action table is computed from $V_k$; the next sweep writes each row’s maximum into $V_{k+1}$. Thus early $V_k$ is not asserted to be the fully evaluated value of the displayed greedy policy.

```text
V[0] = 0; V[N] = 1; V[1:N] = 0
repeat:
    old = copy(V)
    for s = 1, ..., N-1:
        for a = 1, ..., min(s, N-s):
            Q[s,a] = p*old[s+a] + (1-p)*old[s-a]
        V[s] = max over legal a of Q[s,a]
    delta = max_s |V[s] - old[s]|
until delta < tolerance
recompute Q from the final V
choose a maximizing stake in each state
```

This is a **synchronous** implementation: the right side always uses `old`. It starts from a lower bound, so values increase toward the optimal hitting probabilities. More precisely, $V_k(s)$ is the largest probability of reaching the goal within at most $k$ bets. This finite-horizon interpretation explains how information moves backward. The limiting greedy policy solves the unlimited-horizon problem. [Sutton & Barto, §4.4 and Example 4.3](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=104).

### First three sweeps, small enough to audit

For $N=10$ and $p=0.4$:

| Capital $s$ | $V_0$ | $V_1$ | $V_2$ | $V_3$ |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0.064 |
| 3 | 0 | 0 | 0.16 | 0.16 |
| 4 | 0 | 0 | 0.16 | 0.256 |
| 5 | 0 | 0.4 | 0.4 | 0.4 |
| 6 | 0 | 0.4 | 0.4 | 0.4 |
| 7 | 0 | 0.4 | 0.4 | 0.496 |
| 8 | 0 | 0.4 | 0.64 | 0.64 |
| 9 | 0 | 0.4 | 0.64 | 0.784 |
| 10 | 1 | 1 | 1 | 1 |

In the first sweep, only capitals $5$ through $9$ can reach the goal in one win, so only those states receive positive nonterminal values. In the second sweep, capitals 3 and 4 can reach states with value $0.4$, giving $0.4\times0.4=0.16$.

At capital $3$, using $V_1$:

| Stake $a$ | Win state | Loss state | $0.4V_1(s+a)$ | $0.6V_1(s-a)$ | $Q_1(3,a)$ |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 4 | 2 | 0 | 0 | 0 |
| 2 | 5 | 1 | 0.16 | 0 | 0.16 |
| 3 | 6 | 0 | 0.16 | 0 | 0.16 |

Hence $V_2(3)=0.16$. With smallest-stake tie-breaking, the greedy policy row is

| State | $\pi_2(a=1\mid s)$ | $\pi_2(a=2\mid s)$ | $\pi_2(a=3\mid s)$ | Chosen stake |
| --- | ---: | ---: | ---: | ---: |
| $s=3$ | 0 | 1 | 0 | 2 |

The tie is initially a tie under a short-horizon estimate. It is not yet proof of equal unlimited-horizon values.

## 5. Policy iteration: evaluate one whole strategy before improving it

Select **Policy iteration** to make the alternating steps explicit. It starts from $\pi_0(s)=1$.

**Evaluation:** hold the stake table fixed and solve

$$
V^{\pi}(s)=pV^{\pi}(s+\pi(s))+(1-p)V^{\pi}(s-\pi(s)),
\qquad V^{\pi}(0)=0,\quad V^{\pi}(N)=1.
$$

This is a linear system in the $N-1$ unknown interior values. The explorer solves that system directly for each evaluation phase. Repeated fixed-policy sweeps are another way to evaluate it; exact numerical linear-system evaluation makes the distinction from value iteration easier to inspect here.

**Improvement:** compute $Q_{V^\pi}(s,a)$ for every legal action and choose a maximizing stake. If the current stake ties for best, retain it; otherwise choose the smallest maximizer. A changed policy requires a new evaluation. The explorer explicitly labels the intermediate phase where the policy has changed but the displayed value table still belongs to the previous policy. [Sutton & Barto, §§4.1–4.3 and Exercise 4.4](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=96).

| Method | What happens before the next greedy comparison? |
| --- | --- |
| Policy iteration | Fully evaluate the current policy |
| Value iteration | Perform one Bellman optimality sweep |

They target the same optimal value function. They can return different but equally good stake tables because ties need not be broken identically.

## 6. What strategy is learned?

For the target-10 example, value iteration produces:

| Capital | Legal stakes | Optimal success probability $V^*(s)$ | One optimal stake |
| ---: | --- | ---: | ---: |
| 1 | 1 | 0.043463 | 1 |
| 2 | 1–2 | 0.108659 | 2 |
| 3 | 1–3 | 0.186078 | 2 |
| 4 | 1–4 | 0.271647 | 1 |
| 5 | 1–5 | 0.400000 | 5 |
| 6 | 1–4 | 0.465195 | 1 |
| 7 | 1–3 | 0.562988 | 2 |
| 8 | 1–2 | 0.679117 | 2 |
| 9 | 1 | 0.807470 | 1 |

Read the last column as a function of **current** capital. Starting at 3, this policy stakes 2. After a win, capital is 5 and the next stake is 5; after a loss, capital is 1 and the next stake is 1. The policy is a contingent strategy, not a preselected sequence of bets.

![[assets/figures/2026-11-11-reinforcement-learning/02-gambler-one-backup.svg]]

*Original calculation at the converged values, with $N=10$, $p=0.4$. The two branches are weighted before they are added.*

The final action-value row at capital 3 is

| Stake | Calculation | Success probability |
| ---: | --- | ---: |
| 1 | $0.4V^*(4)+0.6V^*(2)$ | 0.173854 |
| 2 | $0.4V^*(5)+0.6V^*(1)$ | 0.186078 |
| 3 | $0.4V^*(6)+0.6V^*(0)$ | 0.186078 |

So stake 1 is worse, while stakes 2 and 3 are tied. Betting 2 is **one** optimal decision; betting 3 is also optimal. In the goal-100 example, capital 50 stakes 50 under the selected policy, while other capitals show the repeating pattern in the green bars. Large and small bets can coexist in an optimal policy.

The lecture explicitly selects the smallest tied stake at [19:22–19:27](https://www.youtube.com/watch?v=_j6pvGEchWU&t=1162s). Our value-iteration display uses the same rule, with a $10^{-10}$ numerical tie tolerance. Small changes to tie rules or floating-point rounding can change the visible policy while leaving its achieved value effectively unchanged. Do not interpret every different bar as a different-quality strategy.

Changing the coin in the explorer makes the role of the objective visible: for the fair-coin preset, the optimal values are $s/N$ and all legal first stakes tie; for the favorable preset, betting 1 is optimal. These finite model results are checked independently below. They do not assert that this strategy transfers to games with different payouts, stake constraints or objectives.

## 7. What does “learning” mean in this demonstration?

The explorer knows $p$ and all legal transitions. It performs **model-based planning**: every backup averages all possible next outcomes. A sweep is not 99 games, and the progress slider counts updates, not sampled episodes. The display reconstructs the lecture’s value/policy process; it does not simulate empirical Q-learning.

If $p$ were unknown, an action-value learner could instead observe individual bets and update

$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha
\left[R_{t+1}+\mathbf1\{\text{nonterminal successor}\}\max_aQ(S_{t+1},a)-Q(S_t,A_t)\right].
$$

Here use the original entry-reward convention: a winning terminal transition gives $R_{t+1}=1$ and no continuation term. The displayed maximum is defined as zero at a terminal state, where no action is taken. This sampled Q-learning update needs exploration and appropriate learning-rate conditions. Its target is noisy, unlike the full expectation used above. The [[Learning/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning - from Bellman equations to sampled updates#7. SARSA, Q-learning and Expected SARSA differ in the continuation target|foundations note]] explains the distinction.

## Checks and numerical meaning

The implementation stops synchronous value iteration when the largest change in a sweep is below $10^{-12}$. It reports the Bellman residual of the displayed table. Since $\gamma=1$, the discounted error formula involving $1/(1-\gamma)$ is unavailable; the residual alone is not presented as a certified value-error bound.

Independent checks compare the selected policy’s value from linear equations, the Bellman-inequality linear program, and policy iteration. For $N=10$, all 2,880 deterministic positive-stake policies were enumerated and evaluated. Across the six presets, the largest discrepancy with independent policy evaluation is about $5.1\times10^{-11}$; the LP comparison differs by at most $1.5\times10^{-9}$. Probability bounds and monotonic value sweeps also pass. These numerical checks support the Bellman argument; they are not a substitute for its assumptions.

Reproducible files: [[assets/figures/2026-11-11-reinforcement-learning/math.js|model and algorithms]], [[assets/figures/2026-11-11-reinforcement-learning/check_and_draw.py|independent checks and static figures]], and [[assets/figures/2026-11-11-reinforcement-learning/checks.json|check results]].

## Connections

- [[Learning/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning - from Bellman equations to sampled updates|Reinforcement learning foundations]] — supplies the conditional-expectation derivation and the evaluation/improvement distinction that this betting example makes concrete.

## Origin

> [!info]- Source details
> This separate note was explicitly requested in the current chat. It applies the Bellman/GPI ideas in my [[raw/notes/2026-11-11-Reinforcement-learning-handwritten-notes.pdf|handwritten PDF]], principally p. 1, to the example in Mutual Information’s [Part 2, 18:14–20:42](https://www.youtube.com/watch?v=_j6pvGEchWU&t=1094s). All available automatic captions, 0:00–21:05, were read. Two source screenshots were separately inspected at visible player times 18:47 and 20:08; the [[raw/assets/2026-11-11-RL-video-gambler-bars.jpg|20:08 frame]] documents intermediate value/policy bars.
>
> The target-10 example, action/policy tables, figures, numerical checks and offline explorer are original agent additions. They reconstruct the mathematical mechanism; they are not recovered lecture code or a frame-for-frame reproduction. The original notes do not contain these completed gambler tables. The textbook comparison uses Sutton & Barto, 2nd ed., Chapter 4, especially Example 4.3 and Exercise 4.9, with positive stakes chosen to match the video.
>
> The brief problem-setting introduction was added by the agent on 2026-11-11 at the user's request, restating the model and example already developed below.
>
> The RL quick reference was added at the user's follow-up request on 2026-11-11. Its definitions restate this note's conventions; the target-100 numerical examples were checked with the existing value-iteration implementation and policy linear-system evaluation. They are agent-added illustrations, not quotations from the lecture.
>
> The foldable GPI recap above the explorer was also requested on 2026-11-11. Its target-10 policy/value-iteration steps and table descriptions were checked against the existing implementation; the bet-1 policy values were additionally checked against the finite gambler's-ruin formula. No explorer code or original source was changed.
>
> [[raw/notes/2026-11-11-RL-source-manifest.json|Source manifest]] records exact preserved-file hashes and source coverage. Probability/stochastic-calculus comparisons were initially deferred as requested; they are now developed in the separate analytical companion linked above, not attributed to this lecture or the original handwriting.
