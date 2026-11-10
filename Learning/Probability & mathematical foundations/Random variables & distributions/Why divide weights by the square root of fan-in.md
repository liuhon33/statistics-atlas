---
id: learning-fan-in-variance-scaling
title: Why divide weights by the square root of fan-in
layer: learning
primary_home: '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Expectation & moments/Variance and standard deviation]]'
subject: probability
backbone_path: Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → Variance and standard deviation
study_band: U
note_types: [insight, derivation]
source_format: conversation
created: 2026-11-08
updated: 2026-11-09
status: active
tags: [atlas/learning, subject/probability]
connections:
- '[[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Independence versus zero covariance]]'
- '[[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Convolution of independent sums]]'
- '[[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes]]'
sources:
- '[[_system/Digests/Fan-in scaling]]'
---

# Why divide weights by the square root of fan-in

Probability & mathematical foundations → Random variables & distributions → Univariate distribution theory → Expectation & moments → Variance and standard deviation

**Independent contributions add in variance, not standard deviation.** This explains the square-root scaling in weight initialization.

For independent standard normals $X,W$,

$$
\mathbb E[XW]=0,\qquad
\operatorname{Var}(XW)=\mathbb E[X^2]\mathbb E[W^2]-0^2=1.
$$

With **three input features** (fan-in $=3$), a neuron computes

$$
Z=X_1W_1+X_2W_2+X_3W_3.
$$

Assuming all six variables are independent standard normals,

$$
\operatorname{Var}(Z)=1+1+1=3,
\qquad \operatorname{SD}(Z)=\sqrt3.
$$

Thus replacing each weight by $W_i/\sqrt3$ restores output SD to $1$. Generally, $n$ inputs give SD $\sqrt n$, motivating division by $\sqrt{\text{fan-in}}$.

The same variance-addition argument explains [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes#One head, with every dimension visible|attention's square-root score scaling]].

The underlying rule, for independent variables with finite variances, is

$$
\operatorname{Var}\!\left(\sum_i a_iU_i\right)=\sum_i a_i^2\operatorname{Var}(U_i).
$$

**Normality is unnecessary**—indeed, the products $X_iW_i$ are not normal. These calculations average over both random inputs and random weights.

In the supplied screenshot, `x.shape = (1000, 10)` and `w.shape = (10, 200)`: fan-in is **10**, not the batch size or output width. The predicted SD is $\sqrt{10}\approx3.16$, close to the displayed $3.0996$.

**Kaiming distinction:** the above is linear-layer scaling. For ReLU, Kaiming initialization adds gain $\sqrt2$, giving weight SD $\sqrt{2/n}$. [PyTorch initialization reference](https://docs.pytorch.org/docs/2.15/nn.init.html#torch.nn.init.kaiming_normal_).

![[kaiming_scaling.png]]

## Connections

- [[Backbone/Probability & mathematical foundations/Joint variation & conditioning/Joint distributions/Marginal & conditional laws/Independence versus zero covariance|Independence versus zero covariance]] — Independence removes covariance terms; pairwise zero covariance already suffices for variance addition.
- [[Backbone/Probability & mathematical foundations/Random variables & distributions/Univariate distribution theory/Transforming random variables/Convolution of independent sums|Convolution of independent sums]] — Convolution determines the full distribution of an independent sum, whereas this observation needs only its variance.
- [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes|Standard attention]] — Both use variance addition: for independent, centered, unit-variance query/key coordinates, $\operatorname{Var}(\sum_{j=1}^{d_k}q_jk_j)=d_k$, so dividing by $\sqrt{d_k}$ restores unit variance. Here $d_k$ is the head's query/key width ($d_h$ in that note); fan-in scaling acts on initial weights, while attention scales scores before softmax.

## Origin

> [!info]- Source details
> User-selected observation from [Andrej Karpathy's demonstration, linked at 40:38](https://www.youtube.com/watch?v=P6sfmUTpUmc&t=2438s) and the supplied screenshot; derivation and Kaiming qualification supplied by the assistant. Source-access details: [[_system/Digests/Fan-in scaling]].
