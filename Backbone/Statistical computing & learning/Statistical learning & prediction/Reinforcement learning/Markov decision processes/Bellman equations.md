---
id: markov-decision-processes-bellman-equations
title: Bellman equations
layer: backbone
level: 5
subject: computing
study_band: M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Reinforcement learning → Markov decision processes → Bellman equations
created: '2026-11-11'
updated: '2026-11-11'
aliases: [Bellman equation, Bellman optimality equation]
tags:
- atlas/backbone
- subject/computing
- level/5
- study/masters
node_kind: knowledge point
parent: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Markov decision processes/Markov decision processes]]'
---

# Bellman equations

Statistical computing & learning → Statistical learning & prediction → Reinforcement learning → Markov decision processes → Bellman equations

Parent: [[Backbone/Statistical computing & learning/Statistical learning & prediction/Reinforcement learning/Markov decision processes/Markov decision processes|Markov decision processes]]

## Definition and scope

The **state value** of a policy $\pi$ is the expected return from state $s$ when actions follow $\pi$: $v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]$. Conditioning on the first action, reward and next state gives the **Bellman equation**, a consistency condition between the value of a state and the values of its successors:

$$
v_\pi(s)=\sum_{a}\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)\,\bigl[r+\gamma\,v_\pi(s')\bigr].
$$

For a finite MDP this is a system of linear equations. Its unique solution is $v_\pi$, provided $\gamma<1$ or every episode eventually terminates under $\pi$. The **Bellman optimality equation** replaces the average over actions with a maximum:

$$
v_*(s)=\max_{a}\sum_{s',r}p(s',r\mid s,a)\,\bigl[r+\gamma\,v_*(s')\bigr].
$$

Any policy that is greedy with respect to $v_*$ is optimal. Dynamic programming turns these equations into update rules (policy evaluation, value iteration). Sampled methods such as temporal-difference learning estimate the same expectations from experience instead of from $p$.

Source: Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., §3.5 (Bellman equation for $v_\pi$), §3.6 (optimality equations and greedy optimal policies) and §4.1 (existence and uniqueness of $v_\pi$; Bellman equations as update rules). Section-level citation: page and equation numbers were not re-checked.

```atlas
```
