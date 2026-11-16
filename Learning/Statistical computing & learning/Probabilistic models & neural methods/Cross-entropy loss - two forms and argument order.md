---
id: learning-cross-entropy-forms-order
title: Cross-entropy loss - two forms and argument order
layer: learning
primary_home: "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/Cross-entropy]]"
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Information for statistical learning → Information measures → Cross-entropy
study_band: U–M elective
note_types: [topic-note, insight]
source_format: pasted-conversation
created: 2026-11-13
updated: 2026-11-16
status: active
verification: checked
learning_state: unknown
aliases: [Cross-entropy argument order, One-hot cross-entropy loss]
tags: [atlas/learning, subject/computing]
connections:
  - "[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/Log loss]]"
sources:
  - "[[raw/conversations/2026-11-13-cross-entropy-pasted-excerpt]]"
---

# Cross-entropy loss - two forms and argument order

Statistical computing & learning → Probabilistic models & neural methods → Information for statistical learning → Information measures → Cross-entropy

**With a one-hot target, cross-entropy is the negative log probability assigned to the correct class.**

## Two equivalent forms

For $C$ classes, let $q_k$ be the target probability and $p_k>0$ the predicted probability; both distributions sum to one. Using natural logarithms,

$$
H(q,p)=-\sum_{k=0}^{C-1}q_k\log p_k.
$$

If the label is $y$, its one-hot target has $q_y=1$ and $q_k=0$ for $k\ne y$. Only the correct-class term survives:

$$
H(q,p)=-\log p_y=\log\left(\frac{1}{p_y}\right).
$$

For $n$ examples, $p_{ik}$ and $q_{ik}$ are example $i$'s prediction and target probabilities, and $y_i$ is its label:

$$
\mathcal L=-\frac1n\sum_{i=0}^{n-1}\sum_{k=0}^{C-1}q_{ik}\log p_{ik}
=-\frac1n\sum_{i=0}^{n-1}\log p_{i,y_i}.
$$

The single-class shortcut requires one-hot targets; soft targets need the weighted sum. [PyTorch loss formulas](https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html).

## Argument order

| Expression | First argument | Second argument |
| --- | --- | --- |
| $H(q,p)$ | Target distribution | Predicted distribution |
| `F.cross_entropy(logits, ys)` | Predicted logits | Target labels |

**The target supplies the weights; the prediction goes inside the logarithm in both cases.** API argument order does not reverse the mathematical distributions. Cross-entropy is generally asymmetric: $H(q,p)\ne H(p,q)$.

```python
import torch
import torch.nn.functional as F

# logits: (n, C); ys: (n,) integer class labels, on the same device
probs = logits.softmax(dim=1)
rows = torch.arange(len(ys), device=logits.device)
loss = -probs[rows, ys].log().mean()

loss = F.cross_entropy(logits, ys)  # same loss, using stable log-softmax
```

Pass **raw logits** to `F.cross_entropy`. This equivalence assumes default mean reduction, no class weights or label smoothing, and valid labels. [PyTorch signature and parameters](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.cross_entropy.html).

## Connections

- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/Log loss|Log loss]] — The one-hot reduction identifies cross-entropy with the observed class's log loss.

## Origin

> [!info]- Source details
> From the user's equivalence observation and argument-order question in the [[raw/conversations/2026-11-13-cross-entropy-pasted-excerpt|pasted exchange]]. The assistant supplied the concise formulation and checked one-hot substitution, signs, averaging, tensor shapes and the official API formulas. Photos and numerical examples are omitted as requested.
