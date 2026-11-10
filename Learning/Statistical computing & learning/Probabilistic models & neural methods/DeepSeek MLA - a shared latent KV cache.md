---
id: learning-deepseek-mla-latent-cache
title: DeepSeek MLA - a shared latent KV cache
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Neural networks/Attention mechanisms]]'
subject: computing
backbone_path: Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms
study_band: M elective
note_types: [topic-note, derivation, question, insight]
question_roles: [mechanism, concept-distinction]
source_format: handwriting
created: '2026-11-09'
updated: '2026-11-09'
status: active
verification: checked
learning_state: practicing
aliases: []
tags: [atlas/learning, subject/computing, topic/attention, topic/mla]
connections:
  - '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Rank and null spaces]]'
sources:
  - '[[raw/notes/2026-11-09-attention.pdf]]'
  - '[[raw/assets/2026-11-09-MLA-I01-key-absorption-identity-cache.png]]'
  - '[[raw/articles/2026-11-09-welch-labs-mla-youtube-auto-captions.txt]]'
---

# DeepSeek MLA - a shared latent KV cache

Statistical computing & learning → Probabilistic models & neural methods → Neural statistical learning → Neural networks → Attention mechanisms

**Cache a shared latent representation of each token, then rearrange the query and output calculations so the full keys and values need not be reconstructed.** My notes identify both halves: absorb the key weights into the query, and apply the value weights after averaging the latent vectors.

MLA learns a shared low-rank key/value representation. First isolate the content calculation in my notes, then restore position. Reference: DeepSeek-AI, [*DeepSeek-V2*, §§2.1.2–2.1.3, Eqs. (9)–(19)](https://arxiv.org/html/2405.04434v5#S2.SS1.SSS2).

![[assets/figures/2026-11-09-attention/mla-01-projections.svg]]

*Original Codex reconstruction of my shared-cache drawing. Each product is shown separately: $E\to C$, $E\to Q_i$, $C\to K_i$, and $C\to V_i$. The ten input rows have width $12288$; the shared latent rows have width $512$; this head's query, key, and value rows have width $128$.*

## 1. One compressed history supplies all heads

Use rows for tokens, omit biases, and first omit positional transformations. For $T$ tokens with width $D$, choose latent width $r$ and head width $d_h$:

$$
\begin{aligned}
E&\in\mathbb R^{T\times D},& W^{DKV}&\in\mathbb R^{D\times r},& C&=EW^{DKV}\in\mathbb R^{T\times r},\\
U_{K,i},U_{V,i}&\in\mathbb R^{r\times d_h},&&& K_i&=CU_{K,i},\quad V_i=CU_{V,i}.
\end{aligned}
$$

Head $i$ has its own feature maps, but every head uses the same $C$. Here the superscript $DKV$ means “down-project for keys and values.” The source example uses $D=12288$, $r=512$, and $d_h=128$; these are illustrative dimensions. A $512\to128$ map for one head can still be a block of an “up-projection”: the full map expands $512$ coordinates into all heads together.

This parameterization is learned. It does not assert that arbitrary pre-existing full-rank [[Learning/Statistical computing & learning/Probabilistic models & neural methods/Standard attention - scores, heads, and matrix shapes#One head, with every dimension visible|MHA weights]] can be losslessly compressed to $r$ dimensions.

## 2. Absorb the key map into the query

The three views of matrix multiplication explain the operations below: row × column gives each score $\widehat q_t c_s^\top$; weighted row combinations give each row of $A_iC$; column × row expands $\widehat Q_iC^\top$ as a sum of outer products over latent coordinates. Associativity then moves the feature maps to the query or output side while preserving the scores and weighted sums.

Let $Q_i\in\mathbb R^{T\times d_h}$ be the content queries. The simplified drawing uses $Q_i=EW_i^Q$. Transposition and associativity give

$$
Q_iK_i^\top
=Q_i(CU_{K,i})^\top
=Q_iU_{K,i}^\top C^\top
=\widehat Q_i C^\top,
\qquad \widehat Q_i:=Q_iU_{K,i}^\top\in\mathbb R^{T\times r}.
$$

If $Q_i=EW_i^Q$, the fixed composite matrix $B_i=W_i^QU_{K,i}^\top\in\mathbb R^{D\times r}$ gives $\widehat Q_i=EB_i$. This matches the orange $B_i$ grouping in my drawing.

![[assets/figures/2026-11-09-attention/mla-02-key-absorption.svg]]

*Original Codex reconstruction of every key-side regrouping in my p. 2 drawing: transpose $CU_{K,i}$, move $U_{K,i}^\top$ beside the query, write the resulting $\widehat q_t$ rows, form $B_i$, and apply it directly to $E$. The horizontal query rows multiply the vertical cached columns.*

For the current query row $q_{t,i}$ and $n$ available cached tokens,

$$
\widehat q_{t,i}=q_{t,i}U_{K,i}^\top\in\mathbb R^{1\times r},
\qquad q_{t,i}K_i^\top=\widehat q_{t,i}C^\top\in\mathbb R^{1\times n}.
$$

The cache is read in latent coordinates. No $n\times d_h$ content-key matrix must be materialized. Regrouping leaves scores unchanged, so the content-only scale stays $\sqrt{d_h}$; changing it to $\sqrt r$ would change the attention weights.

![[assets/figures/2026-11-09-attention/detail-07b-mla-score-staircase.svg]]

*Original Codex expansion using the exact score-matrix format of standard attention. Each allowed entry is now written $\widehat q_t c_s^\top=q_tk_s^\top$; the future triangle remains $-\infty$. The first and last softmax rows show that absorption preserves the causal weights.*

![[assets/figures/2026-11-09-attention/p02-mla-absorption.png|480]]

*Unretouched PDF excerpt, p. 2 left: my shared $C$, transformed query, and “average the latent vector first” derivation. The checked notation makes the transpose and matrix dimensions explicit.*

## 3. Average in latent space, then apply the output map

For content-only attention, let

$$
A_i=\operatorname{softmax}_{\rm row}
\left(\frac{\widehat Q_iC^\top}{\sqrt{d_h}}+M\right),
$$

where the causal mask $M_{ts}$ is zero for $s\leq t$ and $-\infty$ otherwise. Write $H_i=A_iC\in\mathbb R^{T\times r}$. Its row $h_{t,i}=\sum_{s\leq t}\alpha_{ts}c_s$ averages the cached latent rows, where $\alpha_{ts}=(A_i)_{ts}$ for the fixed head $i$.

![[assets/figures/2026-11-09-attention/mla-03-weights-and-latents.svg]]

*Original Codex expansion of the full $10\times10$ causal weight matrix. Every future entry is zero after softmax; the first, second, and last rows of $H_i=A_iC$ show exactly which latent vectors are averaged. Within a fixed-head diagram, $h_t$ abbreviates $h_{t,i}$.*

With output block $W_i^O\in\mathbb R^{d_h\times D}$,

$$
\begin{aligned}
O_i&=A_iV_iW_i^O\\
&=A_i(CU_{V,i})W_i^O\\
&=(A_iC)(U_{V,i}W_i^O)\\
&=(A_iC)T_i,\qquad T_i:=U_{V,i}W_i^O\in\mathbb R^{r\times D},\\
O&=\sum_{i=1}^{H}O_i.
\end{aligned}
$$

For one query, $a_{t,i}C=\sum_{s\leq t}a_{t,i,s}c_s$ is one weighted latent vector. Mapping that vector to the output gives exactly the same result as expanding every historical value first. Heads still have distinct $A_i$ and $T_i$.

$T_i$ is a mathematical grouping, not a requirement to allocate a dense $r\times D$ matrix for every head. An implementation can apply $U_{V,i}$ and $W_i^O$ sequentially after the latent weighted sum if that is cheaper.

![[assets/figures/2026-11-09-attention/mla-04-value-and-output.svg]]

For the feature-by-feature expansion, see the [[Learning/Probability & mathematical foundations/Mathematical tools/Three views of matrix multiplication#3. Column times row: sum whole outer products|outer-product view]].

*Original Codex reconstruction of my “average the latent vector first” calculation. Follow $H_iU_{V,i}=Z_i$, $Z_iW_i^O=O_i$, and the regrouped $H_iT_i=O_i$, with the distributive identity below. The final block multiplication shows why concatenating the heads and applying $W^O$ equals summing their $O_i$ contributions.*

### One decoding step: append token 11

After processing ten tokens, the cache contains $c_1,\ldots,c_{10}$. Processing the next input row $e_{11}$ appends $c_{11}$ and forms the current query $\widehat q_{11,i}$. That query scores all eleven available cache rows, including itself; its output contributes to the prediction of the following token. Historical queries do not need to be recomputed or cached.

![[assets/figures/2026-11-09-attention/mla-05-single-query-decode.svg]]

*Original Codex walkthrough of the entire new row: append $c_{11}$; compute $\widehat q_{11,i}C_{1:11}^\top$; normalize eleven scores; average the same eleven latent rows; apply $T_i$; sum heads. This expands the newest-query explanation in Welch Labs' video ([7:35–9:57](https://www.youtube.com/watch?v=0VLAoVGf_74&t=455s)) using the notebook's dimensions.*

With widths and head count fixed, one such attention step scores $n$ cached tokens and has work proportional to $n$. Generating a whole growing sequence still sums those history lengths: $\sum_{t=1}^n t=n(n+1)/2$.

## “Why is it still called KV matrix?”

This is my exact blue question on p. 2. The shared cache retains both computational roles:

| Role | Expanded form | Computation using the cache |
| --- | --- | --- |
| Key: score history against the query | $q_{t,i}(CU_{K,i})^\top$ | $(q_{t,i}U_{K,i}^\top)C^\top$ |
| Value: supply content to the output | $(a_{t,i}CU_{V,i})W_i^O$ | $(a_{t,i}C)T_i$ |

The physical cache contains $C$, rather than separate full $K_i,V_i$. “KV cache” describes the information and role it supplies. In the drawing's terms: $C$ represents past tokens; $\widehat q_{t,i}$ scores those representations; $T_i$ maps their weighted combination into the output.

![[assets/figures/2026-11-09-attention/p02-why-kv-and-latent-roles.png|680]]

*Unretouched p. 2 question and role summary. In the value identity, the same attention row must occur on both sides, as in the checked table above.*

## My identity-map proposal separates regrouping from compression

My p. 2 proposal sets $W^{DKV}=I_D$, so $C=E$, $U_{K,i}=W_i^K$, and $U_{V,i}=W_i^V$. In the bias-free, position-free setting,

$$
Q_iK_i^\top=(Q_i(W_i^K)^\top)E^\top,
\qquad O_i=(A_iE)(W_i^VW_i^O).
$$

The rearrangement is valid for ordinary MHA too. It caches $D$ scalars per token per layer rather than $2Hd_h$ when key and value widths are both $d_h$. If $D=Hd_h$, that halves the stored scalar count. But the transformed query has width $D$; MLA replaces that wide shared representation with a learned $r$-dimensional bottleneck.

This explains my “compute harder?” comparison. A cached-MHA score uses width $d_h$, while the absorbed MLA content score uses width $r$; with $r=512$ and $d_h=128$, that dot product is wider. Cache reduction alone is not a proof of fewer FLOPs or lower latency. The relevant saving is avoiding full historical key/value storage and repeated expansion; actual speed depends on kernels, memory traffic, sequence length, and projection costs.

### My handwritten comparison and its reproduction

![[raw/assets/2026-11-09-MLA-I01-key-absorption-identity-cache.png]]

*My supplied screenshot, preserved unchanged. The upper comparison retains the small latent cache; the lower comparison proposes caching $X$ itself. Both move the key map to the current query.*

![[assets/figures/2026-11-09-attention/mla-06-handwritten-comparison.svg]]

*Original Codex reproduction of those two comparisons, with dimensions and parentheses checked. Here $X=E$; the lower drawing's full-width key map is named $W_i^K$ to distinguish it from MLA's $U_{K,i}$. Both sides produce a $1\times n$ score row. The transformed query has width $512$ in the upper case and $12288$ in the lower case.*

The upper comparison starts with cached $C$ and one query $q_{11,i}$. Reconstructing all keys and then scoring takes $nrd_h+nd_h$ scalar multiply-adds; transforming the query first and scoring $C$ takes $d_hr+nr$. These counts omit cache creation, softmax, and the value/output calculation. They compare the two parenthesizations of the latent-cache computation; ordinary MHA with its expanded keys already cached uses width $d_h$ for each score.

My “halves the cache size” observation applies to the lower proposal when $D=Hd_h$, both key and value widths are $d_h$, and positions are omitted: $D$ cached scalars replace $2Hd_h$. The earlier [[assets/figures/2026-11-09-attention/detail-09-identity-and-cache.svg|identity-map and cache comparison]] collects these storage formulas.

## The extra component in full DeepSeek MLA

Full MLA adds position-encoded queries $q^R_{t,i}\in\mathbb R^{1\times d_R}$ and keys $k_s^R\in\mathbb R^{1\times d_R}$ shared across heads. Its allowed-token score is

$$
s_{t,i,s}=\frac{
\widehat q_{t,i}c_s^\top+q^R_{t,i}(k_s^R)^\top
}{\sqrt{d_h+d_R}},\qquad s\leq t.
$$

Normalize over $s$ and use the same value calculation. Separate positional features preserve fixed content-key absorption; cache both $c_s$ and $k_s^R$.

The paper also compresses queries and normalizes latent vectors. Absorption holds for the resulting $C,Q_i$; nonlinear normalization cannot be folded into a fixed matrix. These additions come from [§2.1.3, Eqs. (14)–(19); §3.1.2; Appendix C](https://arxiv.org/html/2405.04434v5#A3).

![[assets/figures/2026-11-09-attention/mla-07-position-and-query.svg]]

*Original Codex extension from the paper. Compute the content and positional score matrices separately, add them, divide by $\sqrt{d_h+d_R}$, and apply the causal mask and softmax. With the illustrated widths, $512+64=576$ coordinates are cached per token per layer. The final lines show the compressed query branch and which adjacent linear maps can be absorbed.*

The earlier [[assets/figures/2026-11-09-attention/mha-to-mla.svg|standard-attention/MLA overview]] shows the content and positional branches together.

## Cache sizes with explicit units

For batch size one, $L$ attention layers, $n$ cached tokens, and $b$ bytes per scalar, use key/value width $d_h$, $H$ query heads, and $G$ KV groups:

| Mechanism | Cached scalars per token per layer | Bytes per token across $L$ layers |
| --- | --- | --- |
| MHA: separate KV per head | $2Hd_h$ | $2Hd_hLb$ |
| GQA: one KV pair per group | $2Gd_h$ | $2Gd_hLb$ |
| MQA: one KV pair for all heads | $2d_h$ | $2d_hLb$ |
| MLA content only | $r$ | $rLb$ |
| Full MLA with decoupled position | $r+d_R$ | $(r+d_R)Lb$ |

Total cache is $n$ times the last column (and scales with batch size). This is tensor storage, excluding weights, workspace, allocator overhead, and precision-specific metadata. The structural formulas agree with DeepSeek-V2 [§2.1.4, Table 1](https://arxiv.org/html/2405.04434v5#S2.T1); the numbers below are independently computed examples.

Using the **separate cache example** on p. 2, $H=128$, $d_h=128$, $L=61$, and choosing $b=2$ to reproduce its memory estimates, MHA takes $3{,}997{,}696$ bytes per token: about **4.00 MB**. At $n=100{,}000$, that is about **399.77 GB total**, and one more token adds about 4 MB. It is not 400 GB newly allocated for every token. Here MB and GB are decimal units.

The video's [10:26–10:44 discussion](https://www.youtube.com/watch?v=0VLAoVGf_74&t=626s) concerns **reading** that history for each new query: a straightforward full-attention decode must access historical keys and values. About 400 GB can therefore describe both the stored history and the approximate cache data read to process a new token in this example. Allocation growth and memory traffic are different quantities; actual traffic depends on the implementation and memory reuse.

For the same $L,b,d_h$, GQA with the illustrative choice $G=16$ takes $499{,}712$ bytes/token; MQA takes $31{,}232$. Content-only MLA with $r=512$ takes $62{,}464$; adding $d_R=64$ gives $70{,}272$. These examples explain the source's roughly 500 KB and 31 KB figures without mixing them with the p. 1 $96$-head example. They are not a claimed specification of a particular deployed model; the DeepSeek-V2 report uses $L=60$ and hidden width $5120$ ([§3.1.2](https://arxiv.org/html/2405.04434v5#S3.SS1.SSS2)).

![[assets/figures/2026-11-09-attention/detail-09b-cache-layout.svg]]

*Original Codex reconstruction of my cache rows and layer stacks, with the arithmetic made explicit. The two MLA rectangles are stored together; their different feature widths are not added as matrices. Historical queries need not be cached.*

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Rank and null spaces|Rank and null spaces]] — The concatenated content-key/value map factors through $r$ latent coordinates, so its rank is at most $r$. The identity-map proposal removes this bottleneck; associativity itself does not reduce rank.

## Origin

> [!info]- Source details
> My [[raw/notes/2026-11-09-attention.pdf|attention PDF]], p. 1 bottom cache-comparison transition and p. 2 cache sketches, compression/absorption derivation, identity-map proposal, and blue KV question. The numbered multiplication sketches are covered in the separate linear algebra note. Codex checked the algebra and dimensions, supplied the positional/normalization qualifications from the original paper, and recalculated byte counts. The preserved PDF retains every original marking. Small random rectangular examples independently reproduce expanded and absorbed outputs within $8\times10^{-15}$; the algebra above is the general justification. Code and results: [[assets/figures/2026-11-09-attention/generate_figures.py|verification script]] and [[assets/figures/2026-11-09-attention/checks.json|numeric checks]].
>
> The expanded figures preserve the source's content-only derivation and label the paper's positional addition separately. [[assets/figures/2026-11-09-attention/generate_details.py|Detailed-figure generator]]; [[assets/figures/2026-11-09-attention/detail-checks.json|ten-token checks]]; [[assets/figures/2026-11-09-attention/detail-coverage.json|source-to-figure coverage]].
>
> The later [[raw/assets/2026-11-09-MLA-I01-key-absorption-identity-cache.png|handwritten comparison screenshot]] is embedded beside its reproduction above. Welch Labs, [*How DeepSeek Rewrote the Transformer [MLA]*](https://www.youtube.com/watch?v=0VLAoVGf_74), published 2025-03-05, supplies the newest-query/cache explanation (7:35–10:44) and the latent absorption narrative (13:36–16:14). The [[raw/articles/2026-11-09-welch-labs-mla-youtube-auto-captions.txt|complete exported automatic English captions]] and video description were read; the captions may contain transcription errors. The matrix identities and full positional branch were checked against the DeepSeek-V2 paper and direct algebra.
>
> The seven added SVGs and PNG previews are reproduced by [[assets/figures/2026-11-09-attention/generate_mla_walkthrough.py|the MLA walkthrough generator]]. [[assets/figures/2026-11-09-attention/mla-walkthrough-checks.json|Twenty-eight rectangular numerical identity checks]] agree within $4\times10^{-15}$, including the single new query versus the last row of full causal attention. [[assets/figures/2026-11-09-attention/mla-walkthrough-manifest.json|Source coverage, notation decisions, and visual checks]] record how the handwriting, video, and paper informed each figure.
