---
id: anova-one-and-two-factor-anova
title: One- and two-factor ANOVA
layer: backbone
level: 5
subject: statistics
study_band: U–M
backbone_path: Statistical inference & modeling → Design, sampling & causality → Design of experiments → ANOVA & factorial design → One- and two-factor ANOVA
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

# One- and two-factor ANOVA

Statistical inference & modeling → Design, sampling & causality → Design of experiments → ANOVA & factorial design → One- and two-factor ANOVA

Parent: [[Backbone/Statistical inference & modeling/Design, sampling & causality/Design of experiments/ANOVA & factorial design/ANOVA & factorial design|ANOVA & factorial design]]

## 1. See it and use it

**Do three fertilizers produce the same average plant height?** Measure separate plants: A gives 8, 10, 12 cm; B gives 12, 14, 16; C gives 16, 18, 20. Their means are **10, 14 and 18 cm**.

![[assets/figures/2026-11-10-anova-ancova/anova-initial.svg]]

*Mean separation matters relative to the scatter within each group. Constructed example, not experimental evidence.*

**Analysis of variance (ANOVA)** tests mean differences by comparing between-group and within-group variation. Input: numerical outcomes and group labels. Output: an **F statistic** and a **p-value** testing whether all population means are equal. Here, software gives $F=12$, $p=0.008$: at a prespecified 5% threshold, reject equal means. This says **at least one mean differs**, not which pairs differ or that every pair does. [NIST §3.2.3.1](https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc231.htm).

**One-factor** means one grouping variable: fertilizer. **Two-factor** could add sunlight level; with replication at each combination, test both factors and their **interaction**—whether fertilizer differences depend on sunlight. [NIST §3.2.3.2](https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc232.htm).

The classical F test assumes independent observations and normally distributed errors with equal variance across groups. A large p-value does not establish equal means.

## Origin

> [!info]- Source details
> Introductory level added by Codex, 2026-11-10. NIST/SEMATECH e-Handbook §§3.2.3.1–3.2.3.2, especially Description, Testing and Assumptions, were read for the method and its scope. The plant data and diagram are original constructed illustrations, not NIST's machining data.
>
> Reproduce both introductory diagrams with [[assets/figures/2026-11-10-anova-ancova/make_figures.py|the Python source]]. [[assets/figures/2026-11-10-anova-ancova/checks.json|Numerical checks]] verify means, sums of squares, $F(2,6)=12$ and $p=0.008$; [[assets/figures/2026-11-10-anova-ancova/anova-initial.png|PNG view]]. Model assumptions require study-design and data checks; the arithmetic does not verify them.

```atlas
```
