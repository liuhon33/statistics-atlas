---
id: reinforcement-learning
title: Reinforcement learning
layer: backbone
level: 3
subject: computing
study_band: M
backbone_path: Statistical computing & learning → Statistical learning & prediction → Reinforcement learning
created: '2026-11-11'
updated: '2026-11-11'
aliases: [RL]
tags: [atlas/backbone, subject/computing, level/3, study/masters]
node_kind: group
parent: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Statistical learning & prediction]]'
sources:
  - '[[raw/articles/2026-11-11-RL-part2-youtube-captions.txt]]'
---

# Reinforcement learning

Statistical computing & learning → Statistical learning & prediction → Reinforcement learning

## Learn actions through their consequences

Reinforcement learning studies how an agent learns a policy for choosing actions from interaction with an environment, using numerical rewards to improve expected cumulative reward. An action can change both the immediate reward and which situations the agent encounters later. This delayed effect makes the quality of an action depend on what the agent will do afterwards. [Sutton & Barto, 2nd ed., §1.1 and §3.1, pp. 1–2 and 47–49](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf#page=23).

![[assets/figures/2026-11-11-reinforcement-learning/03-agent-loop.svg]]

*Original illustration: the policy chooses an action; the environment returns a new state and reward. Evaluation and improvement refine future choices.*

In a Markov decision process, the current state contains the information needed to predict the next state and reward given an action. A policy assigns probabilities to the available actions. Its value function measures expected future return.

For example, a gambler chooses a stake at each capital level. Rewarding only successful arrival at a target makes expected return equal the probability of reaching that target before ruin. When the transition probabilities are known, dynamic programming supplies a planning solution; sampled-experience methods address the setting where they are unknown.

```atlas
```
