---
id: markov-decision-processes
title: Markov decision processes
layer: backbone
level: 4
subject: computing
study_band: M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Reinforcement learning → Markov decision processes
created: '2026-11-11'
updated: '2026-11-11'
aliases: [MDP, MDPs, finite Markov decision process]
tags:
- atlas/backbone
- subject/computing
- level/4
- study/masters
node_kind: group
parent: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Reinforcement learning]]'
---

# Markov decision processes

Statistical computing & learning → Statistical learning & prediction → Reinforcement learning → Markov decision processes

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Reinforcement learning|Reinforcement learning]]

## Definition and scope

A **finite Markov decision process** (MDP) models an agent that, at each step $t$, observes a state $S_t$, chooses an action $A_t$, and then receives a reward $R_{t+1}$ and a next state $S_{t+1}$. With finitely many states, actions and rewards, one function gives the whole dynamics:

$$
p(s',r\mid s,a)=\Pr\{S_{t+1}=s',\ R_{t+1}=r \mid S_t=s,\ A_t=a\}.
$$

The **Markov property** is the assumption that this distribution depends only on the current state and action, not on the earlier history. A **policy** $\pi(a\mid s)$ gives the probability of each action in each state. The agent seeks a policy that maximizes the expected **discounted return**

$$
G_t=\sum_{k\ge 0}\gamma^{k}R_{t+k+1},\qquad 0\le\gamma\le 1,
$$

with $\gamma<1$ needed for continuing tasks that never terminate.

Source: Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., [§3.1, pp. 47–49](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=69) (dynamics and the Markov property) and §3.3 (returns and discounting). The §3.3 citation is section-level: its page was not re-checked.

```atlas
```
