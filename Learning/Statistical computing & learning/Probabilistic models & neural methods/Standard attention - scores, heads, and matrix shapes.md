---
id: learning-standard-attention-shapes
title: Standard attention - scores, heads, and matrix shapes
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Neural networks/Attention mechanisms]]'
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms
study_band: M elective
note_types: [topic-note, derivation, insight]
source_format: handwriting
created: '2026-11-09'
updated: 2026-11-12
status: active
verification: checked
learning_state: practicing
aliases: []
tags: [atlas/learning, subject/computing, topic/attention]
connections:
  - '[[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache]]'
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms]]'
  - "[[Learning/Probability & mathematical foundations/Stochastic processes/Kernels - feature inner products and Gaussian covariances]]"
sources:
  - '[[raw/notes/2026-11-09-attention.pdf]]'
---

# Standard attention - scores, heads, and matrix shapes

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms

**Each head computes its own token-to-token weights, uses them to average value vectors, and contributes to a common output.** My drawing's important observation is “we need to separate here”: packing projections into one matrix multiplication does not merge the heads' attention matrices.

![[assets/figures/2026-11-09-attention/detail-01-token-projections.svg]]

*Original Codex reconstruction of my p. 1 projection branches. Long lines represent token rows; braces give the row and column counts. This fixes one of the $96$ heads in my illustrative $10$-token example. Open the SVG to zoom into the algebra.*

## One head, with every dimension visible

Let $E\in\mathbb R^{T\times D}$ contain the layer's input token representations as rows: $T$ tokens, hidden width $D$. These are word/token embeddings only at the input stage; later layers use contextual hidden states. Use $H$ heads with query, key, and value width $d_h$ for this example. Omit biases, dropout, and positional transformations while tracking the matrix products.

For head $i\in\{1,\ldots,H\}$, the learned projection matrices have shape $D\times d_h$:

$$
Q_i=EW_i^Q,\qquad K_i=EW_i^K,\qquad V_i=EW_i^V
\quad\in\mathbb R^{T\times d_h}.
$$

The query at position $t$ scores the key at position $s$ by a dot product:

$$
S_i=\frac{Q_iK_i^\top}{\sqrt{d_h}}+M,
\qquad
A_{i,ts}=\frac{\exp(S_{i,ts})}{\sum_{u=1}^{T}\exp(S_{i,tu})},
\qquad Z_i=A_iV_i.
$$

$S_i,A_i\in\mathbb R^{T\times T}$ and $Z_i\in\mathbb R^{T\times d_h}$. For causal self-attention, $M_{ts}=0$ when $s\leq t$ and $-\infty$ otherwise. Thus query 1 cannot attend to key 2; each row of $A_i$ sums to one over its allowed keys.

Even before masking, these scores need not form a [[Learning/Probability & mathematical foundations/Stochastic processes/Kernels - feature inner products and Gaussian covariances#1. Why positive semidefiniteness is the right requirement|covariance kernel]].

![[assets/figures/2026-11-09-attention/detail-02-causal-scores.svg]]

*Original Codex expansion of my score calculation: horizontal query rows multiply vertical columns of $K_i^\top$. All $100$ positions are shown, with $q_1k_1^\top$ in the first position and $-\infty$ above the diagonal. This is the masked score calculation; softmax produces the weights below.*

In coordinates, the output row is

$$
z_{t,i}=\sum_{s\leq t}A_{i,ts}v_{s,i}.
$$

![[assets/figures/2026-11-09-attention/detail-03-weights-and-values.svg]]

*Original Codex expansion of my weighted-value step. Softmax changes the masked entries to zero; the first row selects $v_1$, while the last row mixes all ten value rows. Both the full weight matrix and the first, second, and last output-row calculations are shown.*

The weights select and mix **values**; keys determine the weights. The standard operator and per-head construction are given in Vaswani et al., [§§3.2.1–3.2.2, Eq. (1)](https://arxiv.org/pdf/1706.03762).

The $\sqrt{d_h}$ divisor controls score scale. Under the illustrative assumption that all query/key coordinates are independent, centered, and have variance one, the dot product has variance $d_h$, so dividing by $\sqrt{d_h}$ gives variance one. Learned activations need not satisfy those assumptions exactly.

This is the same variance-addition principle as [[Learning/Probability & mathematical foundations/Random variables & distributions/Why divide weights by the square root of fan-in#Why divide weights by the square root of fan-in|fan-in scaling]].

## Packed projections still require separate heads

![[assets/figures/2026-11-09-attention/detail-04-heads-and-output.svg]]

*Original Codex reconstruction of my p. 1 head splitting, block multiplication, output projection, and regrouping. The packed-score identity is displayed separately from the per-head softmax operation.*

Packing $W^Q=[W_1^Q\;\cdots\;W_H^Q]$ computes all queries at once:

$$
EW^Q\in\mathbb R^{T\times Hd_h}
\ \longrightarrow\ (Q_1,\ldots,Q_H).
$$

For the drawing's $T=10$, $H=96$, $d_h=128$, $D=12288$, a common implementation reshapes and permutes this to $H\times T\times d_h$. The attention array then has shape $96\times10\times10$. Batch dimensions are omitted here; implementations can store the axes in another order.

If the packed matrices are instead multiplied without separating heads,

$$
[Q_1\;\cdots\;Q_H]
\begin{bmatrix}K_1^\top\\ \vdots\\ K_H^\top\end{bmatrix}
=\sum_{i=1}^{H}Q_iK_i^\top.
$$

This block identity in the drawing is valid, but applying one softmax to this sum produces a different operation. Standard MHA applies softmax to **each head's** scores. The $D=Hd_h$ equality is part of this example, not a requirement of all attention architectures.

## Concatenation becomes a sum after the output projection

Stack the output-projection blocks $W_i^O\in\mathbb R^{d_h\times D}$ vertically into $W^O\in\mathbb R^{Hd_h\times D}$. Block multiplication gives

$$
O=[Z_1\;\cdots\;Z_H]W^O
=\sum_{i=1}^{H}Z_iW_i^O
=\sum_{i=1}^{H}A_iE\,W_i^VW_i^O.
$$

![[assets/figures/2026-11-09-attention/p01-head-separation-and-output.png|430]]

*Unretouched PDF excerpt, p. 1, lower-right: my separate-head annotation and output-block sum. The surrounding handwriting mixes row and column conventions; the equations above use rows consistently.*

For one head, the two feature maps may be grouped as $W_i^VW_i^O$, or the weighted sum can be evaluated first. This is associativity. It preserves that head's $A_i$; distinct heads generally cannot share one common $A$. The attention module produces $O$ with the same width as $E$, permitting a residual addition $E+O$; that addition is a surrounding block operation.

## Translating the column-token drawing

![[assets/figures/2026-11-09-attention/detail-05-column-convention.svg]]

*Original Codex translation of my column-token drawing. Transposing the representation also transposes the causal mask and changes row normalization to column normalization; the value and output products follow in the same order.*

My left-hand drawing places tokens in columns: $X=E^\top$, $Q_c=Q_i^\top$, $K_c=K_i^\top$, and $V_c=V_i^\top$. Then

$$
K_c^\top Q_c=(Q_iK_i^\top)^\top.
$$

Queries now index **columns**, so normalize over key rows:

$$
A_c=\operatorname{softmax}_{\rm col}
\left(\frac{K_c^\top Q_c}{\sqrt{d_h}}+M^\top\right)=A_i^\top,
\qquad Z_c=V_cA_c=Z_i^\top.
$$

Switching conventions therefore transposes both the mask and the normalization axis. A bare “softmax” label hides this important detail.

In ordinary causal decoding, old keys and values are reused for the new query. Historical queries need not be cached: earlier output states are already computed. This is the setting behind my “no need to cache the Query” annotation.

MLA replaces these separate histories with a [[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache#1. One compressed history supplies all heads|shared latent KV cache]].

## Connections

- [[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache|DeepSeek MLA]] — Starts with these headwise equations, then factorizes keys and values and regroups the same products around a smaller cache.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|Inner products and norms]] — Query-key scores are dot products; their magnitudes and coordinate variances explain the dimension-dependent scaling.

- [[Learning/Probability & mathematical foundations/Stochastic processes/Kernels - feature inner products and Gaussian covariances|Kernels - feature inner products and Gaussian covariances]] — Query–key scores use different feature maps and need not be symmetric or positive semidefinite, unlike a covariance kernel.

## Origin

> [!info]- Source details
> My [[raw/notes/2026-11-09-attention.pdf|attention PDF]], p. 1, upper/central attention calculations and right-hand implementation/output diagrams. Codex standardized orientations and dimensions, clarified the packed-head sum, and supplied the variance argument and checked SVG. Matrix identities were checked algebraically; independent small-matrix calculations also check separate heads, causal normalization, both token conventions, and the output-block sum. Reproducible checks: [[assets/figures/2026-11-09-attention/generate_figures.py|figure and verification script]].
>
> The expanded SVG sequence follows the same source calculations with explicit rows, dimension braces, and causal matrices. [[assets/figures/2026-11-09-attention/generate_details.py|Detailed-figure generator]]; [[assets/figures/2026-11-09-attention/detail-checks.json|ten-token checks]]; [[assets/figures/2026-11-09-attention/detail-coverage.json|source-to-figure coverage]].
