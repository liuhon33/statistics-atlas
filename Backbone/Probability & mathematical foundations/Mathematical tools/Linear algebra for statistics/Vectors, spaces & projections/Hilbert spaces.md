---
id: spaces-hilbert-spaces
title: Hilbert spaces
layer: backbone
level: 5
subject: probability
study_band: U–M
backbone_path: Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Vectors, spaces & projections → Hilbert spaces
created: '2026-11-09'
updated: '2026-11-09'
status: active
tags: [atlas/backbone, subject/probability, level/5, study/undergraduate-masters]
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Vectors, spaces & projections]]'
related:
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms]]'
applied_in:
  - '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection]]'
---

# Hilbert spaces

Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Vectors, spaces & projections → Hilbert spaces

Parent: [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Vectors, spaces & projections|Vectors, spaces & projections]]

## Definition and scope

A **Hilbert space** is a real or complex inner-product space $H$ complete under $\|x\|=\sqrt{\langle x,x\rangle}$: every sequence whose pairwise distances tend to zero converges in this norm to an element of $H$.

Examples include Euclidean $\mathbb R^n$ and $L^2(\Omega,\mathcal F,P)$, the space of square-integrable random variables, identifying variables equal almost surely. In the real-valued case,

$$
\langle X,Y\rangle=\mathbb E[XY],\qquad \|X\|^2=\mathbb E[X^2].
$$

For a **closed linear subspace** $M\subseteq H$, every $x\in H$ has a unique nearest point $P_Mx\in M$, characterized by $x-P_Mx\perp M$. Consequently,

$$
x=P_Mx+(x-P_Mx),\qquad
\|x\|^2=\|P_Mx\|^2+\|x-P_Mx\|^2.
$$

Closedness matters in infinite dimensions: a best approximant need not exist in a nonclosed subspace. Projection geometry alone says nothing about statistical independence. Euclidean observation vectors and random variables in $L^2$ use different inner products, despite sharing this geometry.

Source: Jean-Marie Dufour, [*Hilbert spaces*](https://jeanmariedufour.github.io/ResE/Dufour_1999_C_TS_HilbertSpaces.pdf), version 2003-02-18, Definition 2.2, Theorem 2.4, Theorem 3.4 and Theorem 3.6 (printed pp. 3–5). Almost-sure identification makes the $L^2$ inner product positive definite.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Inner products and norms|Inner products and norms]] — Completeness in the induced norm is the additional requirement that makes an inner-product space a Hilbert space.
- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Conditional expectation/L2 conditional projection|L2 conditional projection]] — Conditional expectation of a square-integrable variable is its projection onto the closed subspace measurable with respect to the conditioning sigma-algebra.

```atlas
```
