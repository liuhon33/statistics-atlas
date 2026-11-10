---
id: neural-basics-attention-mechanisms
title: Attention mechanisms
layer: backbone
level: 5
subject: computing
study_band: M elective
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms
created: '2026-11-09'
updated: '2026-11-09'
status: active
verification: checked
aliases: []
tags: [atlas/backbone, subject/computing, level/5, study/masters-elective]
node_kind: knowledge point
parent: '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Neural networks/Neural networks]]'
sources: []
---

# Attention mechanisms

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms

Parent: [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Neural networks/Neural networks|Neural networks]]

**Attention forms a query-dependent weighted combination of value vectors.** Scaled dot-product attention uses queries $Q\in\mathbb R^{n_q\times d_k}$, keys $K\in\mathbb R^{n_k\times d_k}$, and values $V\in\mathbb R^{n_k\times d_v}$:

$$
A=\operatorname{softmax}_{\rm row}\!\left(\frac{QK^\top}{\sqrt{d_k}}+M\right),
\qquad O=AV\in\mathbb R^{n_q\times d_v}.
$$

Here $n_q,n_k$ count queries and key/value pairs; $d_k,d_v$ are positive feature dimensions. The mask $M$ is zero on allowed pairs and $-\infty$ elsewhere. Each query must have at least one allowed key. Softmax normalizes over keys, so each output row is a convex combination of value rows, before dropout or an output projection.

![[assets/figures/2026-11-09-attention/attention-reference.svg]]

*Original Codex illustration: similarities become weights, which combine values. The mask specifies which values are available.*

In **self-attention**, queries, keys, and values are projected from the same sequence; cross-attention obtains queries from another representation. **Multi-head attention** computes separate attention weights per head, concatenates the outputs, and projects them. **Multi-head latent attention (MLA)** shares a compressed representation for keys and values; DeepSeek-V2 also retains a separate positional key component.

References: Vaswani et al., [*Attention Is All You Need*, §§3.2.1–3.2.3, Eq. (1)](https://arxiv.org/pdf/1706.03762); DeepSeek-AI, [*DeepSeek-V2*, §§2.1.2–2.1.3](https://arxiv.org/html/2405.04434v5#S2.SS1). Shapes, normalization, and the stated masking condition were checked directly.

```atlas
```
