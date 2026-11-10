---
id: learning-three-matrix-product-views
title: Three views of matrix multiplication
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Matrices & decompositions]]'
subject: probability
backbone_path: Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Matrices & decompositions
study_band: Foundation
note_types: [topic-note, derivation, insight]
source_format: handwriting
created: '2026-11-09'
updated: '2026-11-09'
status: active
verification: checked
learning_state: practicing
aliases: []
tags: [atlas/learning, subject/probability, topic/linear-algebra]
connections:
  - '[[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes]]'
  - '[[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache]]'
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition]]'
sources:
  - '[[raw/notes/2026-11-09-attention.pdf]]'
---

# Three views of matrix multiplication

Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Matrices & decompositions

**The three methods in my attention notes group the same sums differently: one scalar, one output column, or one outer-product matrix at a time.** Choosing the grouping can make an attention calculation much easier to understand.

For $A\in\mathbb R^{m\times r}$ and $B\in\mathbb R^{r\times n}$, the product $P=AB\in\mathbb R^{m\times n}$ is defined by

$$
P_{ij}=\sum_{k=1}^{r}A_{ik}B_{kj}.
$$

The matching inner dimension $r$ is the index being summed out. The views below require no invertibility, symmetry, or square matrices. Reference: Gilbert Strang, [*ZoomNotes for Linear Algebra*, §1.6, printed p. 10 / PDF p. 13](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/4d876a9159e32543eb0d73b4d4382f4c_MIT18_06S10ZoomNotes.pdf#page=13), which also presents the row analogue of the column view.

![[assets/figures/2026-11-09-attention/detail-10-matrix-products.svg]]

*Original Codex expansion of all three constructions in my notes. Long row and column vectors, dimension braces, and the common summation index show exactly what each multiplication produces. The numerical SVGs below instantiate these general identities.*

## 1. Row times column: compute an entry

$$
P_{ij}=A_{i:}B_{:j}.
$$

$A_{i:}$ is row $i$, a $1\times r$ vector; $B_{:j}$ is column $j$, an $r\times1$ vector. Their product is a scalar. In attention, $(QK^\top)_{ts}=q_tk_s^\top$ [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes#One head, with every dimension visible|scores one query-key pair]].

## 2. Matrix times each column: compute an output vector

Write $B=[b_1\;\cdots\;b_n]$, where $b_j=B_{:j}$. Then

$$
AB=[Ab_1\;\cdots\;Ab_n],
\qquad Ab_j=\sum_{k=1}^{r}B_{kj}A_{:k}.
$$

Each column of $B$ supplies coefficients for a linear combination of the columns of $A$. This explains why the columns of $AB$ lie in the column space of $A$.

![[assets/figures/2026-11-09-attention/p01-column-multiplication.png|430]]

*Unretouched PDF excerpt, p. 1, bottom-left: my second multiplication view.*

![[assets/figures/2026-11-09-attention/matrix-detail-2-columns.svg]]

*Codex expansion of my column sketch: dashed outlines keep each vector together. Each $Ab_j$ is a weighted sum of the columns of $A$; the completed output columns are placed side by side, not added to each other.*

The row analogue is just as useful:

$$
(AB)_{i:}=\sum_{k=1}^{r}A_{ik}B_{k:}.
$$

Thus a row of attention weights combines rows of the value matrix. With tokens stored in columns, the same idea becomes a combination of value columns; transposing changes the display, not the underlying weighted sum.

## 3. Column times row: sum whole outer products

$$
AB=\sum_{k=1}^{r}A_{:k}B_{k:}.
$$

Each $m\times1$ column times a $1\times n$ row produces an $m\times n$ matrix. Its rank is at most one (zero if either vector is zero). Looking at entry $(i,j)$ of this sum recovers $\sum_k A_{ik}B_{kj}$, proving equivalence with the first view.

![[assets/figures/2026-11-09-attention/p02-dot-and-outer-products.png|430]]

*Unretouched PDF excerpt, p. 2, upper-left: my first and third views. The source spans a page break; the two excerpts remain separate.*

![[assets/figures/2026-11-09-attention/matrix-detail-1-dot.svg]]

*Detailed version of my first sketch: row 1 of $A$ and column 1 of $B$ give only the top-left entry, $1\cdot2+2\cdot1+0\cdot0=4$. The other row–column pairs fill the remaining entries.*

![[assets/figures/2026-11-09-attention/matrix-detail-3-outer.svg]]

*Detailed version of my third sketch: pair column $k$ of $A$ with row $k$ of $B$. Each pair creates a complete $2\times2$ matrix; add the three matrices entry by entry. Unlike the dot product, an outer product multiplies every column entry by every row entry.*

The three views differ in **what one step produces**:

| View | One multiplication step | Build the final product by |
| --- | --- | --- |
| Row × column | $(1\times r)(r\times1)$: one scalar | Filling each entry $(i,j)$ |
| Matrix × column | $(m\times r)(r\times1)$: one $m$-vector | Placing the $n$ output columns side by side |
| Column × row | $(m\times1)(1\times n)$: one $m\times n$ matrix | Summing the $r$ full matrices |

An attention score matrix can therefore be decomposed feature by feature:

$$
QK^\top=\sum_{k=1}^{d_h}Q_{:k}K_{:k}^\top.
$$

Each term is the contribution of one query/key feature coordinate to every token pair. The summation is over **features within a head**. It does not authorize summing different heads' scores before softmax.

## Why regrouping matters for MLA

Associativity gives $(AB)C=A(BC)$ when dimensions match; matrix order is preserved. For a latent matrix $C\in\mathbb R^{T\times r}$ and feature map $U\in\mathbb R^{r\times d_h}$,

$$
A_{\mathrm{attn}}(CU)=(A_{\mathrm{attn}}C)U.
$$

So averaging expanded values and expanding the averaged latent vector give the same result. With one decoding query, computing $(aC)U$ avoids expanding all historical rows of $C$ first. This is an exact regrouping for a chosen factorization; choosing a small latent rank is a separate modeling decision.

This is the value-side regrouping used in [[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache#3. Average in latent space, then apply the output map|MLA's latent averaging]].

The outer-product view also shows $\operatorname{rank}(CU)\leq r$. In an SVD, $M=\sum_{k=1}^{r_M}\sigma_k u_kv_k^\top$, the same construction uses orthonormal singular vectors and nonnegative singular values, with $r_M=\operatorname{rank}(M)$. A general factorization $CU$ need not be an SVD.

## Connections

- [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes|Standard attention]] — Dot products form scores, row combinations mix values, and block multiplication explains concatenating heads and applying the output projection.
- [[Learning/Statistical computing & learning/Probabilistic models & neural methods/DeepSeek MLA - a shared latent KV cache|DeepSeek MLA]] — Row–column products give latent attention scores, weighted row combinations give $A_iC$, and outer-product sums expose the latent bottleneck; associativity moves feature maps outside the historical-token operations.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|Singular value decomposition]] — An SVD is a structured sum of outer products; it gives a familiar comparison for the general low-rank products used in MLA.

## Origin

> [!info]- Source details
> My [[raw/notes/2026-11-09-attention.pdf|attention PDF]], the numbered multiplication sketches across p. 1 bottom-left and p. 2 top-left, plus the p. 1 weighted-value examples. Codex supplied the index proofs, numerical example, row analogue, and explicit attention/MLA connections. The numerical product and both alternative constructions agree exactly in [[assets/figures/2026-11-09-attention/generate_figures.py|the reproducible script]]; the proofs above establish the general identities.
>
> At my request, Codex added the three detailed row/column-vector SVGs beneath the corresponding handwritten excerpts. These are new explanatory illustrations, not altered handwriting. [[assets/figures/2026-11-09-attention/draw_matrix_vector_details.py|Their dependency-free generator]] checks the shared numerical example and writes [[assets/figures/2026-11-09-attention/matrix-vector-detail-checks.json|the numerical results]]. The original PDF and excerpts remain unchanged.
>
> The general symbolic overview uses the same vector-and-brace format as the attention/MLA walkthrough. [[assets/figures/2026-11-09-attention/generate_details.py|Detailed-figure generator]]; [[assets/figures/2026-11-09-attention/detail-coverage.json|source-to-figure coverage]].
