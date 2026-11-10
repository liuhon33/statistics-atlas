---
id: anova-ancova
title: ANCOVA
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Design, sampling & causality → Design of experiments → ANOVA & factorial design → ANCOVA
created: '2026-11-08'
updated: '2026-11-10'
aliases: []
tags:
- atlas/backbone
- subject/statistics
- level/5
- study/undergraduate-masters
node_kind: knowledge point
parent: '[[Backbone/Statistical inference & modeling/Design, sampling & causality/Design of experiments/ANOVA & factorial design/ANOVA & factorial design]]'
sources:
- '[[_system/Sources/psu]]'
- '[[_system/Sources/psumas]]'
- '[[assets/figures/2026-11-10-anova-ancova/make_figures.py]]'
- '[[assets/figures/2026-11-10-anova-ancova/checks.json]]'
---

# ANCOVA

Statistical inference & modeling → Design, sampling & causality → Design of experiments → ANOVA & factorial design → ANCOVA

Parent: [[Backbone/Statistical inference & modeling/Design, sampling & causality/Design of experiments/ANOVA & factorial design/ANOVA & factorial design|ANOVA & factorial design]]

## 1. See it and use it

**Two teaching methods finish with average scores of 70 and 80 points—but their students started at 50 and 60.** Compare them at the same starting score, rather than attributing the whole ten-point gap to teaching.

![[assets/figures/2026-11-10-anova-ancova/ancova-initial.svg]]

*The vertical gap compares fitted means at the same pre-course score. Constructed data; diamonds are predictions, not new observations.*

**Analysis of covariance (ANCOVA)** combines group comparisons with regression adjustment for a numerical **covariate**, here the pre-course score. Input: each student's group, starting score and final score. Output: adjusted group means, uncertainty intervals and a test of their equality. [Schwarz (2025), §§2–3](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1600764/full).

Suppose the fitted common slope is **0.5 final-score points per starting-score point**. At a common starting score of 55:

$$
\begin{aligned}
\text{A: }&70+0.5(55-50)=72.5,\\
\text{B: }&80+0.5(55-60)=77.5.
\end{aligned}
$$

The adjusted gap is **5 points**, not 10. These are model-based comparisons, not proof of causation. [Cambridge MRC CBU, adjusted-mean formula](https://imaging.mrc-cbu.cam.ac.uk/statswiki/FAQ/ancreg).

The classical common-slope model assumes linear, parallel group relationships and independent normal errors with equal variance. Compare within overlapping covariate ranges; if slopes differ, the group gap depends on starting score.

## Origin

> [!info]- Source details
> Introductory level added by Codex, 2026-11-10. Read Wolf Schwarz, *The Ancova model for comparing two groups: a tutorial emphasizing statistical distribution theory* (2025), §§2–3, for conditional versus unadjusted means, parallel regressions and inference; read Cambridge MRC CBU's “Can I do an analysis of covariance using regression?” through its adjusted-mean formula for the numerical adjustment. Only that formula and regression interpretation are used from the latter, not its later standard-error shortcuts.
>
> The teaching example and figures are original constructed illustrations. [[assets/figures/2026-11-10-anova-ancova/make_figures.py|Reproducible Python source]] and [[assets/figures/2026-11-10-anova-ancova/checks.json|checks]] contain all ten observations, verify the fitted common slope, raw and adjusted means, normal equations and overlap at 55. [[assets/figures/2026-11-10-anova-ancova/ancova-initial.png|PNG view]]. Arithmetic verifies the illustration, not assumptions or causal validity for a real study.

```atlas
```
