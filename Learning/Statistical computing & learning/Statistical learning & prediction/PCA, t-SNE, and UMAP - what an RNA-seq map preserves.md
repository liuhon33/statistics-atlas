---
id: learning-pca-tsne-umap-rnaseq
title: PCA, t-SNE, and UMAP - what an RNA-seq map preserves
layer: learning
primary_home: '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/PCA versus visualization embeddings]]'
subject: computing
backbone_path: Statistical computing & learning → Statistical learning & prediction → Unsupervised learning → Dimension reduction & embeddings → PCA versus visualization embeddings
study_band: U–M
note_types: [topic-note, insight]
source_format: notebook-slides-video
created: '2026-11-11'
updated: '2026-11-12'
status: active
verification: checked
learning_state: unknown
aliases: [RNA-seq dimensionality reduction, PCA tSNE UMAP comparison]
tags: [atlas/learning, subject/computing, topic/dimension-reduction]
connections:
- '[[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Principal component analysis]]'
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition]]'
- '[[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/Nonlinear manifold overview]]'
- '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence]]'
- '[[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Autoencoders]]'
- '[[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation]]'
sources:
- '[[raw/articles/2026-11-11-dimensionality-reduction-slides.pdf]]'
- '[[raw/articles/2026-11-11-Deepia-PCA-tSNE-UMAP-transcript.txt]]'
- '[[raw/notebooks/2026-11-11-rna-seq-tsne/PCA_tSNE_UMAP.ipynb]]'
- '[[raw/notebooks/2026-11-11-rna-seq-tsne/demo.ipynb]]'
- '[[raw/notebooks/2026-11-11-rna-seq-tsne/umap-comparison.ipynb]]'
- '[[raw/notebooks/2026-11-11-rna-seq-tsne/2026-11-11-rna-seq-tsne-readme.md]]'
- '[[raw/notebooks/2026-11-11-rna-seq-tsne/capture-manifest.json]]'
- '[[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-09-output-1.png]]'
- '[[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-12-output-2.png]]'
- '[[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-13-output-1.png]]'
- '[[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-16-output-1.png]]'
---

# PCA, t-SNE, and UMAP - what an RNA-seq map preserves

Statistical computing & learning → Statistical learning & prediction → Unsupervised learning → Dimension reduction & embeddings → PCA versus visualization embeddings

**Reducing dimension requires choosing what to preserve.** PCA keeps a linear summary with large variance and small reconstruction error. t-SNE and UMAP arrange samples using neighborhood relationships. A useful RNA-seq workflow can combine these aims.

## One dataset, two reductions

My local [[raw/notebooks/2026-11-11-rna-seq-tsne/PCA_tSNE_UMAP.ipynb|PCA/t-SNE/UMAP notebook]] uses the Tasic mouse-cortex data. Its saved outputs report **23,822 cells**, with **3,000 selected genes** entering PCA; the original loaded matrix has 45,768 genes. Each point in the following plots is a cell. Colors come from supplied cluster annotations; the embeddings did not predict those labels.

$$
\underbrace{\text{normalized, log-transformed expression}}_{23{,}822\times3{,}000}
\xrightarrow{\text{PCA}}
\underbrace{\text{50 PC scores per cell}}_{23{,}822\times50}
\xrightarrow{\text{t-SNE or UMAP}}
\underbrace{\text{2 plotting coordinates per cell}}_{23{,}822\times2}.
$$

Selecting 3,000 genes keeps a subset of original features. PCA constructs **new combinations** of those features. t-SNE/UMAP then constructs coordinates with a different objective. The two plotted PCs are only two columns of the 50-column input used by the nonlinear methods. Thus their ability to separate groups can partly use information absent from the PC1–PC2 picture.

| First two PCs | t-SNE of 50 PCs | UMAP of 50 PCs |
| --- | --- | --- |
| ![[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-09-output-1.png]] | ![[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-12-output-2.png]] | ![[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-16-output-1.png]] |

*Original saved notebook outputs, recovered without modifying the PNG bytes: cells 9, 12, and 16 (one-based notebook cell numbers). They also appear in the supplied slides, pp. 25, 26, and 28. These are existing results, not a new execution or a controlled performance benchmark.*

## What each method tries to keep

| Question | PCA | t-SNE | UMAP |
| --- | --- | --- | --- |
| What is optimized? | Retained variance; equivalently squared linear reconstruction error | KL divergence between pair-similarity probabilities | Agreement of fuzzy graph memberships through a cross-entropy objective |
| What are the axes? | Ordered linear combinations of features | Coordinates optimized jointly for the sample set | Coordinates optimized to represent a neighborhood graph |
| Main choices | Preprocessing, scaling, number of PCs | Perplexity, initialization, learning rate, optimization settings | Neighborhood size, distance metric, `min_dist`, initialization, optimization settings |
| Explained-variance percentage? | Yes | No PCA-style percentage | No PCA-style percentage |
| A new observation? | Apply the fitted centering/scaling and loading matrix | scikit-learn `TSNE` has no `transform`; extensions such as openTSNE offer placement methods | `umap-learn` offers `transform` into a fitted embedding |
| Typical use here | Compression and an initial global linear view | Explore local similarity at chosen scales | Explore graph-connected structure at chosen scales |

The definitions come from [Stanford's PCA account](https://web.stanford.edu/class/stats305c/slides/PCA_I.html), [the original t-SNE paper, §3](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf), and [the UMAP algorithm explanation](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html#the-umap-algorithm). Software behavior: [scikit-learn TSNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html), [openTSNE API](https://opentsne.readthedocs.io/en/stable/api/index.html), [UMAP transforming new data](https://umap-learn.readthedocs.io/en/latest/transform.html).

### PCA — a shared linear coordinate system

For centered $X_c\in\mathbb R^{n\times p}$, take its compact SVD $X_c=UDV^\top$. Keeping the first $k$ loading columns gives $T_k=X_cV_k=U_kD_k$. The corresponding reconstruction is $T_kV_k^\top$. [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Principal component analysis|The PCA backbone]] derives why the same $V_k$ consists of leading covariance eigenvectors, with $\lambda_j=d_j^2/(n-1)$.

The 50-PC step is a compression choice, not a claim that “50” is universally sufficient. Discarded variation could be noise, batch effects, or meaningful rare-cell biology. Inspect the variance spectrum and sensitivity to the number of PCs. Also remember that PCA itself does not decide whether a large-variance direction is a batch effect or the signal of interest.

### t-SNE — match probabilities of pairs being neighbors

Imagine asking each cell which other cells resemble it. Nearby cells receive high affinity, with a locally adjusted distance scale. t-SNE arranges points so important pairs remain close in the map. It compares **normalized affinities**, rather than trying to keep every Euclidean distance numerically unchanged.

> [!note]- The probability model and its loss
> Let $x_i\in\mathbb R^p$ be input coordinates and $y_i\in\mathbb R^2$ the plotted coordinates, for $i=1,\ldots,n$. Here the input may already be the 50-PC representation. For $j\ne i$:
>
> $$
> p_{j\mid i}=
> \frac{\exp(-\|x_i-x_j\|^2/(2\sigma_i^2))}
> {\sum_{\ell\ne i}\exp(-\|x_i-x_\ell\|^2/(2\sigma_i^2))},
> \qquad p_{ij}=\frac{p_{j\mid i}+p_{i\mid j}}{2n}.
> $$
>
> The bandwidth $\sigma_i>0$ is chosen so the conditional distribution has the requested perplexity:
>
> $$
> \operatorname{Perp}(P_i)=2^{-\sum_{j\ne i}p_{j\mid i}\log_2p_{j\mid i}}.
> $$
>
> This is an effective neighborhood size, not a hard cutoff or a request for that many clusters. In the 2D map, use a heavy-tailed Student-$t$ kernel:
>
> $$
> q_{ij}=
> \frac{(1+\|y_i-y_j\|^2)^{-1}}
> {\sum_{a\ne b}(1+\|y_a-y_b\|^2)^{-1}},
> \qquad L=\sum_{i\ne j}p_{ij}\log\frac{p_{ij}}{q_{ij}}.
> $$
>
> Both $P$ and $Q$ sum to one over ordered off-diagonal pairs; diagonal entries are zero. Large $p_{ij}$ with tiny $q_{ij}$ incurs a strong penalty. The heavy tail helps accommodate moderately separated neighbors in fewer dimensions, addressing crowding. See [van der Maaten & Hinton, §2 and §3.1–3.3, pp. 2581–2585](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf).

In my notebook, cell 12 uses scikit-learn t-SNE with perplexity 30, random initialization, Euclidean distance, automatic learning rate, and seed 42. Cell 13 uses openTSNE with **two perplexities, 30 and 238**, and a small PCA initialization.

> [!example]- The saved multiscale t-SNE result
> ![[raw/assets/2026-11-11-rna-seq-PCA-tSNE-UMAP-cell-13-output-1.png]]
>
> *Original cell-13 output. Here $238=\lfloor23822/100\rfloor$. This uses local and broader affinity scales together; it is not just one unusually large perplexity.*
>
> The comparison changes implementation, initialization, learning-rate settings, and affinity scales together. It cannot isolate the effect of perplexity alone. For a controlled comparison, hold the other choices fixed. Account for the packages' learning-rate conventions: scikit-learn's 200 corresponds to 800 in openTSNE/FIt-SNE, as documented in [scikit-learn's parameter reference](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html).

The repository's [Kobak & Berens paper, “Preserving global geometry with t-SNE”](https://pmc.ncbi.nlm.nih.gov/articles/PMC6882829/) motivates PCA initialization and multiscale similarities. These can improve large-scale organization in the studied settings; they do not turn every distance between islands into a calibrated biological distance.

### UMAP — build a weighted graph, then lay it out

UMAP first connects nearby input points with locally scaled edge weights. It then places low-dimensional points so strong graph connections tend to remain close, with a repulsive contribution discouraging inappropriate closeness. The video's [15:51 segment](https://www.youtube.com/watch?v=o_cAOa5fMhE&t=951s) sits in the explanation of combining directed neighbor relationships into a symmetric graph.

> [!note]- What is being compared mathematically
> In a simplified account of standard UMAP, a directed neighbor weight is
>
> $$
> w_{i\to j}=
> \exp\!\left(-\frac{\max(0,d(x_i,x_j)-\rho_i)}{\sigma_i}\right).
> $$
>
> Here $d$ is the chosen input distance; $\rho_i$ sets a local connectivity offset and $\sigma_i>0$ a local scale. The weight is zero outside the chosen directed neighbor set. The usual fuzzy union combines directions:
>
> $$
> w_{ij}=w_{i\to j}+w_{j\to i}-w_{i\to j}w_{j\to i}\in[0,1].
> $$
>
> These are edge memberships; unlike t-SNE's $p_{ij}$, they do **not** form one normalized distribution over all pairs. Low-dimensional memberships use
>
> $$
> q_{ij}=\frac1{1+a\|y_i-y_j\|^{2b}},
> $$
>
> with positive shape parameters $a,b$ set from the embedding-distance settings. The ideal graph cross-entropy, up to terms constant in $y$, is
>
> $$
> -\sum_{i<j}\left[w_{ij}\log q_{ij}+(1-w_{ij})\log(1-q_{ij})\right].
> $$
>
> This explains attraction and repulsion. Implementations use sampled optimization, including negative sampling; the displayed all-pairs expression is not a claim that each update evaluates that full sum. [UMAP paper, §3](https://arxiv.org/abs/1802.03426); [official explanation, cross entropy and algorithm](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html).

My cell 15 uses `n_neighbors=15`, `min_dist=0.3`, Euclidean distance, and seed 42. `n_neighbors` chooses a neighborhood scale: larger values generally emphasize broader relationships. `min_dist` controls how tightly embedded points may pack in the model; it is not a hard minimum separation enforced between every pair. See [UMAP's parameter guide, the sections for these two parameters](https://umap-learn.readthedocs.io/en/latest/parameters.html).

A point can gain edges through other points choosing it, so the final symmetric graph need not give every vertex exactly 15 neighbors. Pairs without attractive edges still matter through the repulsive part of the optimization.

## How to compare the maps

**Check preservation in the input space as well as appearance in 2D.** The upstream [[raw/notebooks/2026-11-11-rna-seq-tsne/umap-comparison.ipynb|UMAP comparison notebook]], cell 3, implements three useful diagnostics:

- **KNN preservation:** average overlap between each point's $k$ nearest neighbors in input and embedding space.
- **KNC preservation:** the analogous overlap for class centroids. This uses supplied labels and measures a different relationship from point-level neighborhoods.
- **CPD:** Spearman correlation between pairwise distances on a sampled subset, testing broader distance ordering.

These measures can disagree because they ask different questions. In this workflow, evaluate against the **same 50-PC input** when comparing the final 2D step; separately assess information lost between genes and 50 PCs. High agreement with PC space alone says nothing about signal already discarded by PCA.

Compare several seeds and neighborhood scales using the same input, metric, preprocessing, and evaluation sample. Identify which observations actually change neighbors. Check known annotations, marker genes, batch variables, and rare populations in the original representation. A compact island can be useful evidence to investigate; its area, gaps, and orientation are not direct measurements of cell abundance, evolutionary distance, or causal separation.

For predictive use, train preprocessing and the representation inside each training split; evaluate the downstream model on held-out samples. An unsupervised embedding can be useful input to a classifier, but the plot alone is neither a classifier nor a clustering decision.

## Corrections that change the interpretation

The supplied sources provide useful intuition. Keep these refinements beside it:

- **A large $p$ does not make every regression impossible.** With more columns than rows, $X^\top X$ is singular, so the ordinary inverse formula cannot give a unique coefficient vector. Least-squares solutions still exist; regularization or a lower-dimensional model can resolve ambiguity. This refines slides 3 and 32.
- **PCA does not require data to be “linear.”** It always computes a linear summary. It can miss useful curved structure; a nonlinear embedding can emphasize that structure without guaranteeing correct clusters. This refines slides 8–10.
- **KL is an expectation of a log ratio.** It is not the shaded area between two density curves and is not a symmetric metric. Here it compares distributions over **pairs of sample indices**, not two fitted bell-shaped densities in gene space. This corrects the illustration on slide 14 and the video's 8:32–9:06 explanation.
- **Runtime and global preservation depend on the setup.** Fast t-SNE implementations exist; UMAP has no universal guarantee of preserving global distances or outperforming every other method. The slides' speed comparison and the video's final preference describe particular examples, not a method-selection theorem.

> [!note]- Details to check before reusing my notebook as an analysis pipeline
> These are observations about the saved code, not edits to it.
>
> 1. **Normalization denominator:** main cell 8 sums counts over the selected 3,000 genes. Upstream `demo.ipynb` cell 9 uses all loaded genes for each cell's library size. These define different relative-expression scales. Decide deliberately which normalization is intended; they are not equivalent reproductions of the same preprocessing. This Smart-seq2 example uses exon/read counts; the local comment calling them UMI counts should not be taken literally.
> 2. **Paired PC signs:** cell 8 flips columns of the score matrix but leaves `pca.components_` unchanged. This is harmless for Euclidean neighbor distances and plotting. To reconstruct with those flipped scores, flip the corresponding loading vectors too, or undo the score flips before `inverse_transform`.
> 3. **Cell metadata alignment:** cell 3 subsets `counts` to `goodCells` but does not subset `areas` by the same indices. Its input file order assigns 0 to VISp and 1 to ALM, whereas cell 5 prints those labels in reverse. The two printed area counts sum to 25,481, rather than 23,822. Reindex and relabel before using those metadata in a scientific comparison.
> 4. **Sparse zero fraction:** the printed `counts.size / prod(counts.shape)` is a stored-entry fraction for this sparse matrix, not a zero fraction. Stored entries can themselves include explicit zeros. Compute the desired quantity explicitly.
> 5. **Saved UMAP warning:** cell 15 reports a disconnected graph during spectral initialization. Cross-component positioning deserves particular caution. The saved plot does not remove that limitation.
> 6. **Upstream parameter labels:** `umap-comparison.ipynb` cells 4–5 set the second run to `min_dist=.5`, while cell 6 labels that setting `0.3`. Trust the executed parameter only after confirming which run produced a figure; this discrepancy does not apply to the local main notebook's explicit `min_dist=0.3`.

## Further connections

The broader family is **dimensionality reduction**: replace many coordinates with fewer while preserving a specified kind of information. [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/Multidimensional scaling|MDS]] emphasizes a distance or dissimilarity objective; the local notebook already compares PCA and MDS on cluster means in cell 11. Autoencoders learn an encoder–decoder representation by reconstruction; using a two-unit bottleneck is another modeling choice, not a guarantee of a faithful 2D map.

The distinction from [[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation|the earlier standardization note]] is also geometric: there, a whole feature is a vector across observations. Here, the scatterplot puts **one observation at each point** in feature space. The same matrix supports both views, but their axes and projections have different meanings.

## Connections

- [[Backbone/Statistical inference & modeling/Multivariate analysis/Multivariate statistical analysis/Linear dimension reduction/Principal component analysis|Principal component analysis]] — Supplies the linear compression step and the variance/reconstruction criterion used before the 2D embedding.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Singular value decomposition|Singular value decomposition]] — Explains why the PCA input consists of $UD$ scores, with feature directions in $V$ and covariance eigenvalues $d_j^2/(n-1)$.
- [[Backbone/Statistical computing & learning/Statistical learning & prediction/Unsupervised learning/Dimension reduction & embeddings/Nonlinear manifold overview|Nonlinear manifold overview]] — Motivates preserving neighborhoods when curved structure is poorly represented by a small linear subspace.
- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Information for statistical learning/Information measures/KL divergence|KL divergence]] — Defines the asymmetric probability comparison optimized by t-SNE and resolves the density-area misconception.
- [[Backbone/Statistical computing & learning/Probabilistic models & neural methods/Neural statistical learning/Selected architectures & latent models/Autoencoders|Autoencoders]] — Provides a learned reconstruction-based alternative and clarifies why latent-space visualization is a separate reduction.
- [[Learning/Probability & mathematical foundations/Random variables & distributions/Standardization geometry - means, lengths, and correlation|Standardization geometry]] — Distinguishes changing feature scales from changing basis, and observation-space vectors from feature-space points.

## Origin

> [!info]- Source details
> Requested as one learning digest alongside PCA enrichment on 2026-11-11. The comparison, mathematical explanations, code observations, and corrections are Codex synthesis; no new question wording is attributed to the user.
>
> Sources: [supplied Google Slides](https://docs.google.com/presentation/d/1DLhkGDhKqwqpm--8rLNCNh243BtSmmCrJLuGnqupzQg/edit), preserved as a 36-page PDF; [Deepia's video](https://www.youtube.com/watch?v=o_cAOa5fMhE), with the exported English transcript read from 0:02 through its last returned line at 18:29; and the local Ubuntu project at `/home/hongrui_liu/learning/tsne/rna-seq-tsne`. Its remote is [berenslab/rna-seq-tsne](https://github.com/berenslab/rna-seq-tsne), the companion repository to Kobak & Berens (2019). `PCA_tSNE_UMAP.ipynb` is a local untracked adaptation; it is not represented as an unchanged upstream notebook.
>
> All 16 cells and seven saved PNG outputs in the main notebook were inspected. Relevant upstream comparisons are `demo.ipynb` cells 9 and 14–17, and `umap-comparison.ipynb` cells 3–6. Four main-notebook PNGs are embedded; feature-selection, subset-PCA, and centroid-PCA/MDS outputs are preserved separately. No new handwriting or exercise screenshot was supplied.
>
> The slides' static pages were inspected; exported video placeholders (including an unavailable object on p. 18) are not recovered animations. The separate video transcript supplies the narrated account; it is not evidence of having viewed every animation frame. Autoencoder experiments and million-cell notebooks remain outside this three-method digest.
>
> Verification covers source/code reading, the displayed objective definitions and assumptions, PCA algebra, and independently executed small examples. The RNA-seq analysis was **not rerun**; saved outputs are historical evidence, and the data/metadata issues above remain unresolved in the original project. File hashes and exact coverage are recorded in [[_system/Digest Checkpoints]].
