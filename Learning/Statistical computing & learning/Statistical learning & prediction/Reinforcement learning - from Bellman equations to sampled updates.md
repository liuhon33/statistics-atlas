---
id: learning-rl-bellman-to-sampled-updates
title: Reinforcement learning - from Bellman equations to sampled updates
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Reinforcement learning]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Reinforcement learning
study_band: M
note_types: [topic-note, derivation, question, insight]
question_roles: [mechanism, concept-distinction, assumption-boundary]
source_format: handwriting
created: 2026-11-11
updated: 2026-11-11
status: active
verification: checked
learning_state: introduced
aliases: [Bellman equations and generalized policy iteration, MC TD and semi-gradient learning]
tags: [atlas/learning, subject/computing, topic/reinforcement-learning]
connections:
  - '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation]]'
  - '[[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Efficient integration/Importance sampling]]'
  - '[[Backbone/Statistical computing & learning/Numerical methods & optimization/Optimization for statistics/Optimization algorithms/Stochastic gradient descent]]'
sources:
  - '[[raw/notes/2026-11-11-Reinforcement-learning-handwritten-notes.pdf]]'
  - '[[raw/articles/2026-11-11-RL-part2-youtube-captions.txt]]'
  - '[[raw/notes/2026-11-11-RL-source-manifest.json]]'
---

# Reinforcement learning - from Bellman equations to sampled updates

Statistical computing & learning → Statistical learning & prediction → Reinforcement learning

**The common task is to value future consequences, then use those values to choose better actions.** Bellman equations express the future recursively. Dynamic programming evaluates the recursion using a known model; Monte Carlo and temporal-difference methods use experience; function approximation shares what is learned across states.

My three handwritten pages trace this progression. The separate [[Learning/Statistical computing & learning/Statistical learning & prediction/Gamblers problem - learning an optimal betting policy|gambler’s-problem note]] turns the Bellman equations into action tables, policy tables and an interactive learning process.

## 1. The objects we are learning about

At time $t$, the agent observes $S_t=s$, chooses $A_t=a$, and receives $R_{t+1}$ and $S_{t+1}$. The trajectory is

$$
S_0,A_0,R_1,S_1,A_1,R_2,S_2,\ldots.
$$

A stationary Markov policy $\pi(a\mid s)$ specifies the probability of choosing action $a\in\mathcal A(s)$ in state $s$. The environment’s transition law is

$$
p(s',r\mid s,a)=\Pr(S_{t+1}=s',R_{t+1}=r\mid S_t=s,A_t=a).
$$

The Markov assumption says that conditioning additionally on earlier history does not change this law. **It does not say that the agent knows $p$.** Knowledge of $p$ is the additional assumption used by dynamic programming. [Sutton & Barto, §3.1 and §4.1](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=70); [lecture, 2:46](https://www.youtube.com/watch?v=_j6pvGEchWU&t=166s).

![[assets/figures/2026-11-11-reinforcement-learning/03-agent-loop.svg]]

*Original reconstruction of the interaction diagram in my p. 1 notes. An action affects later states as well as the next reward.*

For an episode ending at time $T$, the return is

$$
G_t=\sum_{k=t+1}^{T}\gamma^{k-t-1}R_k
=R_{t+1}+\gamma G_{t+1},\qquad G_T=0.
$$

Here $0\leq\gamma\leq1$ discounts later rewards. For continuing problems with bounded rewards, $\gamma<1$ guarantees a finite discounted return. Undiscounted episodic arguments require suitable termination and integrability conditions; finite state space alone does not supply them.

| Object | Definition | What it answers |
| --- | --- | --- |
| Policy $\pi(a\mid s)$ | Distribution over legal actions | What do I do in this state? |
| State value $v_\pi(s)$ | $\mathbb E_\pi[G_t\mid S_t=s]$ | How good is starting here and following $\pi$? |
| Action value $q_\pi(s,a)$ | $\mathbb E_\pi[G_t\mid S_t=s,A_t=a]$ | How good is taking this action once, then following $\pi$? |
| Estimates $V(s),Q(s,a)$ | Tables updated by an algorithm | What do I currently estimate those values to be? |

The expectation in $q_\pi$ fixes the first action. Subsequent actions follow $\pi$. With rewards recorded on transitions and the episode already finished, terminal states have zero remaining return. [Sutton & Barto, §3.5, Eqs. 3.12–3.13](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=80).

## 2. Why can a future return be replaced by a next-state value?

**My question, paraphrased from the red box on p. 1:** Why does

$$
\mathbb E_\pi[G_{t+1}\mid S_t=s,A_t=a]
=\mathbb E_\pi[v_\pi(S_{t+1})\mid S_t=s,A_t=a]
$$

hold, even though $G_{t+1}$ and $v_\pi(S_{t+1})$ are different random quantities?

![[assets/figures/2026-11-11-reinforcement-learning/handwriting-bellman.png]]

*Rendered excerpt of my PDF p. 1, containing the conditional-expectation question and Bellman derivation. The complete original PDF is preserved unchanged.*

There are two averages. First average future returns **within each possible next state**; then average those state-specific means over the next state. The law of total expectation gives

$$
\begin{aligned}
&\mathbb E_\pi[G_{t+1}\mid S_t=s,A_t=a]\\
&=\sum_{s'}\Pr(S_{t+1}=s'\mid S_t=s,A_t=a)
\mathbb E_\pi[G_{t+1}\mid S_{t+1}=s',S_t=s,A_t=a]\\
&=\sum_{s'}\Pr(S_{t+1}=s'\mid S_t=s,A_t=a)v_\pi(s').
\end{aligned}
$$

The second equality uses the Markov property and the fixed stationary policy: once $S_{t+1}$ is known, future evolution under that policy does not depend on the preceding state/action. It also follows if we condition on the intervening reward. This is an equality **of conditional expectations**, not a pathwise replacement of the realized return. [Lecture, 5:27–6:12](https://www.youtube.com/watch?v=_j6pvGEchWU&t=327s).

Now assemble the two building blocks:

$$
\boxed{v_\pi(s)=\sum_a\pi(a\mid s)q_\pi(s,a)}
$$

$$
\boxed{q_\pi(s,a)=\sum_{s',r}p(s',r\mid s,a)[r+\gamma v_\pi(s')]}
$$

Substituting the second into the first gives the **Bellman expectation equation** for $v_\pi$:

$$
v_\pi(s)=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)[r+\gamma v_\pi(s')].
$$

Substituting the first into the second instead gives the action-value version:

$$
q_\pi(s,a)=\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma\sum_{a'}\pi(a'\mid s')q_\pi(s',a')\right].
$$

This explains my four-cell “$v$ or $q$ on each side” diagram: the two mixed equations generate the two recursive equations. The expectation over **actions** comes from $\pi$; the expectation over **next states and rewards** comes from $p$. [Sutton & Barto, §4.1, Eqs. 4.3–4.5](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=96).

## 3. Evaluation keeps the policy fixed; improvement changes it

**Policy evaluation** computes $v_\pi$ for a specified policy. One synchronous sweep is

$$
V_{k+1}(s)=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)
[r+\gamma V_k(s')].
$$

All right-hand sides use the old table $V_k$. An in-place implementation can use values already updated during the current sweep; intermediate numbers will then depend on the sweep order. A sweep visits the table’s states; it is not an episode played by the agent.

**Classic gridworld.** On a $4\times4$ board, the upper-left and lower-right corners terminate the episode. Up/down/left/right each have probability $1/4$, each move earns $-1$, attempting to leave the board leaves the agent in the same state, and $\gamma=1$. Consequently $v_\pi(s)$ is minus the expected number of moves until termination. [Sutton & Barto, Example 4.1, p. 76](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=98); [lecture, 11:57–13:41](https://www.youtube.com/watch?v=_j6pvGEchWU&t=717s).

![[assets/figures/2026-11-11-reinforcement-learning/05-gridworld-evaluation.svg]]

*Original computed reconstruction. Every panel uses the same random policy. Negative values describe time to termination; they do not yet describe optimal play.*

Starting with all zeros, the first sweep sets every nonterminal value to $-1$. For the top-row cell immediately right of the terminal, the second sweep is

$$
V_2=-1+\tfrac14(0-1-1-1)=-1.75.
$$

The $0$ comes from moving into the terminal. One of the $-1$s comes from trying to move off the upper edge and staying put. The converged value there is $-14$, so the random policy takes 14 moves on average from that cell.

**Policy improvement** uses the evaluated future to compare actions:

$$
\pi_{\mathrm{new}}(s)\in\arg\max_{a\in\mathcal A(s)}q_\pi(s,a).
$$

The word “greedy” refers to this **long-term action value**, not just the next reward. In the finite discounted setting, the policy-improvement theorem gives $v_{\pi_{\mathrm{new}}}(s)\geq v_\pi(s)$ for all states. Proper episodic settings admit the corresponding result. Equality is possible; a different action need not be strictly better. [Sutton & Barto, §4.2](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=98).

**Policy iteration** alternates full evaluation and improvement:

$$
\pi_0\ \xrightarrow{\text{evaluate}}\ v_{\pi_0}
\ \xrightarrow{\text{improve}}\ \pi_1
\ \xrightarrow{\text{evaluate}}\ v_{\pi_1}\ \longrightarrow\cdots.
$$

After improvement, the old value table still evaluates the old policy. This is why another evaluation is needed. Retaining the current action when it ties for best prevents pointless switching between equally good policies.

**Value iteration** combines one-step lookahead and maximization in every sweep:

$$
V_{k+1}(s)=\max_a\sum_{s',r}p(s',r\mid s,a)[r+\gamma V_k(s')].
$$

Its fixed point satisfies the Bellman optimality equation. Extract a policy by taking a maximizing action. Generalized policy iteration names the broader interaction between evaluation and improvement, including partial and interleaved versions. Convergence still needs the relevant algorithmic assumptions; arbitrary approximate updates do not automatically converge. [Sutton & Barto, §§4.3–4.6](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=102).

## 4. Monte Carlo replaces model averages with observed returns

For a fixed policy, collect completed episodes and average the returns following visits to a state. If $g_1,\ldots,g_n$ are the included returns from $s$, the running mean obeys

$$
V_n(s)=\frac1n\sum_{i=1}^ng_i
=V_{n-1}(s)+\frac1n[g_n-V_{n-1}(s)].
$$

The update moves **toward** the new return: the sign is plus. For example, $V=0.5$, $g=1$, and $n=3$ gives $V_{\mathrm{new}}=2/3$, not $1/3$. This repairs the minus sign in the last averaging line on my p. 1.

For action values, count visits to $(s,a)$ and use

$$
Q(s,a)\leftarrow Q(s,a)+\alpha[G_t-Q(s,a)].
$$

With $\alpha=1/N(s,a)$ after incrementing the count, this is a sample mean. Constant $\alpha$ gives a recency-weighted estimate, not the ordinary mean, and does not by itself guarantee exact convergence. First-visit MC uses the first occurrence of a state or pair per episode; every-visit MC uses all occurrences. The double sum in my notes is the every-visit form. [Sutton & Barto, §§5.1–5.2](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=114).

My state–action transformation explains why state-value averaging can also estimate action values. Let $\widetilde S_t=(S_t,A_t)$. Under a fixed stationary policy its transition law is

$$
\widetilde p_\pi((s',a'),r\mid(s,a))
=p(s',r\mid s,a)\pi(a'\mid s').
$$

The value of this augmented state is $q_\pi(s,a)$. MC can estimate it without knowing the displayed transition law; it observes trajectories instead.

For control, interleave estimation with policy improvement while retaining exploration. With one selected greedy action $a^*$, an $\varepsilon$-greedy policy assigns

$$
\pi(a\mid s)=
\begin{cases}
1-\varepsilon+\varepsilon/|\mathcal A(s)|,&a=a^*,\\
\varepsilon/|\mathcal A(s)|,&a\ne a^*.
\end{cases}
$$

The probabilities sum to one. Fixed positive $\varepsilon$ retains exploratory actions; convergence claims for a fully greedy optimum require additional exploration and step-size conditions.

## 5. Off-policy learning changes which policy the data evaluates

The **behavior policy** $b$ generates the actions; the **target policy** $\pi$ is the one whose value is sought. On-policy learning uses the same policy for both roles.

For a fixed starting state, the probability of a trajectory includes products of policy probabilities and environment probabilities. If the environment is the same under both policies, its factors cancel in the likelihood ratio:

$$
\rho_{t:T-1}=\prod_{k=t}^{T-1}\frac{\pi(A_k\mid S_k)}{b(A_k\mid S_k)},
\qquad
v_\pi(s)=\mathbb E_b[\rho_{t:T-1}G_t\mid S_t=s].
$$

This requires **coverage**: wherever the target can select an action, the behavior must assign it positive probability. For an action value conditioned on the already chosen $A_t=a$, the correction starts at the **next** action:

$$
q_\pi(s,a)=\mathbb E_b[\rho_{t+1:T-1}G_t\mid S_t=s,A_t=a].
$$

An empty product is one. Long products can create high variance; this is a property of the weighting scheme and data mismatch, not a universal statement that every off-policy algorithm has higher variance. [Sutton & Barto, §5.5, Eqs. 5.3–5.5](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=125).

## 6. TD bootstraps; Monte Carlo waits for the complete return

TD(0) replaces the full observed return with one reward plus an estimate of the remainder:

$$
V(S_t)\leftarrow V(S_t)+\alpha\underbrace{[R_{t+1}+\gamma V(S_{t+1})-V(S_t)]}_{\delta_t\text{, the TD error}}.
$$

**Bootstrapping** means using an existing value estimate inside the update target. This permits an update after one transition. A terminal successor contributes zero remaining value under the transition-reward convention.

An $n$-step target lies between TD(0) and MC:

$$
G_{t:t+n}=
\sum_{k=t+1}^{\min(t+n,T)}\gamma^{k-t-1}R_k
 +\mathbf1\{t+n<T\}\gamma^nV(S_{t+n}).
$$

When the horizon reaches termination, the bootstrap term disappears and the target is the observed return $G_t$. “$n\to\infty$ becomes MC” in my notes means this episodic limit. [Sutton & Barto, §6.1 and §7.1](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=164).

![[assets/figures/2026-11-11-reinforcement-learning/04-update-targets.svg]]

*Original comparison: which information produces the target? A model expectation and a sampled transition are different ways of forming an update.*

### Does TD necessarily perform better than MC?

My p. 2 asks “Why does TD perform better than MC”. The useful distinction is between their **batch solutions**, not a universal ranking.

For a fixed dataset, tabular batch MC fits the observed returns. Under the standard terminating Markov-reward-process setup and convergent batch updates, TD(0) instead solves the Bellman equations of the empirical transition/reward model. TD need not explicitly construct that model. [Sutton & Barto, §6.3, pp. 126–128](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=148).

In the book’s two-state example, the only observed visit to $A$ goes to $B$, then ends with return zero. Across all eight visits to $B$, six return one and two return zero. MC estimates $V(A)=0$, $V(B)=3/4$. The empirical Markov model says $A$ always moves to $B$ with zero immediate reward, so batch TD estimates both as $3/4$.

TD can share evidence through the transition structure; MC directly fits complete returns. Which predicts better depends on the data, step size, approximation and validity of the state representation. The batch comparison does not prove that online TD always wins.

## 7. SARSA, Q-learning and Expected SARSA differ in the continuation target

Each updates $Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha[\text{target}-Q(S_t,A_t)]$.

| Method | Target after observing $S_{t+1}$ | Continuation being evaluated |
| --- | --- | --- |
| SARSA | $R_{t+1}+\gamma Q(S_{t+1},A_{t+1})$ | The next action actually selected by the behavior/target policy |
| Q-learning | $R_{t+1}+\gamma\max_a Q(S_{t+1},a)$ | A greedy continuation, even if behavior explores |
| Expected SARSA | $R_{t+1}+\gamma\sum_a\pi(a\mid S_{t+1})Q(S_{t+1},a)$ | The target policy’s average over next actions |

The first target on my p. 2 is specifically SARSA when it updates an action value. Q-learning changes the sampled next action to a maximum; that explains its off-policy character. Expected SARSA is on-policy when its target policy equals the behavior, and can be off-policy otherwise. All three use zero continuation at termination. [Sutton & Barto, §§6.4–6.6, Eqs. 6.7–6.9](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=151).

The familiar convergence statement for tabular Q-learning requires continued visitation of every relevant state–action pair, suitable diminishing step sizes and the MDP’s convergence conditions. It does not automatically extend to arbitrary neural-network approximators.

## 8. Function approximation shares parameters across states

When a table is too large, approximate $v_\pi(s)$ by $\widehat v(s,w)$, with $w\in\mathbb R^d$. My p. 3 uses two image features—mean pixel intensity and pixel standard deviation—as an illustrative feature vector $x(s)\in\mathbb R^2$:

$$
\widehat v(s,w)=x(s)^\top w.
$$

Updating $w$ changes predictions for every state sharing those features. These two features are an illustration, not a guarantee of a sufficient Markov state representation.

For a fixed policy and weighting distribution $\mu(s)$ over states, the prediction objective is

$$
\overline{\mathrm{VE}}(w)=\sum_s\mu(s)[v_\pi(s)-\widehat v(s,w)]^2.
$$

If states are sampled according to $\mu$ and a target $U_t$ is conditionally unbiased for $v_\pi(S_t)$, the usual sample update is

$$
w\leftarrow w+\alpha[U_t-\widehat v(S_t,w)]\nabla_w\widehat v(S_t,w).
$$

For a fixed policy, $U_t=G_t$ yields gradient Monte Carlo. Appropriate stochastic-approximation regularity, sampling and step-size assumptions are still required for convergence; an unbiased target alone is insufficient. In the linear case the objective is convex, with uniqueness depending on feature coverage/rank. [Sutton & Barto, §§9.2–9.4, pp. 199–205](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=221).

### What changes when the target itself depends on the weights?

**My question, paraphrased from the final lines of p. 3:** If $U_t=R_{t+1}+\gamma\widehat v(S_{t+1},w)$, does its dependence on $w$ change the gradient argument?

![[assets/figures/2026-11-11-reinforcement-learning/handwriting-approximation.png]]

*Rendered excerpt of my PDF p. 3. The final question identifies the difference between a Monte Carlo target and a bootstrapped target.*

Yes. This target is generally biased relative to $v_\pi(S_t)$ because its next-state estimate can be wrong. More specifically,

$$
\mathbb E[U_t\mid S_t=s]-v_\pi(s)
=\gamma\,\mathbb E_\pi[\widehat v(S_{t+1},w)-v_\pi(S_{t+1})\mid S_t=s].
$$

Thus the bias can vanish—for example, with exact next-state values. Dependence on $w$ does not force a nonzero bias in every case.

For the per-transition squared TD error, with $\delta=R_{t+1}+\gamma\widehat v(S_{t+1},w)-\widehat v(S_t,w)$,

$$
\nabla_w\tfrac12\delta^2
=\delta\left[\gamma\nabla_w\widehat v(S_{t+1},w)-\nabla_w\widehat v(S_t,w)\right].
$$

The standard TD parameter update uses only $+\alpha\delta\nabla_w\widehat v(S_t,w)$, treating the target as fixed during that update. It omits differentiation through the next-state estimate, which is why it is called a **semi-gradient**. This per-transition squared error is also a different objective from the unknown true-value error $\overline{\mathrm{VE}}$. Neither should be silently substituted for the other. [Sutton & Barto, §9.3, p. 202](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=224).

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/Law of total expectation|Law of total expectation]] — justifies averaging future returns within each next state before averaging over the transition; this is the key step in my Bellman derivation.
- [[Backbone/Statistical computing & learning/Simulation & approximate inference/Monte Carlo methods/Efficient integration/Importance sampling|Importance sampling]] — changes trajectory expectations from the behavior policy to the target policy while the shared environment factors cancel.
- [[Backbone/Statistical computing & learning/Numerical methods & optimization/Optimization for statistics/Optimization algorithms/Stochastic gradient descent|Stochastic gradient descent]] — explains the function-approximation update and why a weight-dependent bootstrap target requires a semi-gradient qualification.

## Origin

> [!info]- Source details
> My [[raw/notes/2026-11-11-Reinforcement-learning-handwritten-notes.pdf|three-page PDF]] is the primary source: p. 1 covers MDPs, Bellman equations, policy iteration, MC, exploration and importance sampling; p. 2 covers TD, batch comparison and action-value targets; p. 3 covers function approximation and the target’s dependence on weights. The two embedded excerpts are derived renders; all original handwriting remains in the PDF.
>
> Supplement: Mutual Information, [Part 2](https://www.youtube.com/watch?v=_j6pvGEchWU), published 2022-10-25. All available English automatic captions from 0:00–21:05 were read; [[raw/articles/2026-11-11-RL-part2-youtube-captions.txt|archived captions]]. This is caption coverage plus selected gambler-frame inspection, not continuous audiovisual viewing. MC/TD/approximation material comes from the supplied handwriting and the cited textbook, not an assertion that Part 2 teaches those later topics.
>
> Added synthesis: clean derivations, gridworld computation, comparison tables, convergence qualifications and the explicit semi-gradient calculation. Corrections include model knowledge versus the Markov assumption, the running-average sign, conditional importance-ratio indexing and the scope of TD/SGD convergence claims. Checks combine direct algebra, independent gridworld linear equations, numerical examples and the linked [[assets/figures/2026-11-11-reinforcement-learning/checks.json|verification results]]. Full source locators and hashes are in [[raw/notes/2026-11-11-RL-source-manifest.json|the manifest]] and the digest checkpoint.
