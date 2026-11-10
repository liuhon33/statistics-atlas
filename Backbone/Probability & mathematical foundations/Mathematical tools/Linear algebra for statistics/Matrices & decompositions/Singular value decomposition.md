---
id: svd
title: Singular value decomposition
layer: backbone
level: 5
subject: probability
study_band: Foundation
backbone_path: Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Matrices & decompositions → Singular value decomposition
created: '2026-11-08'
updated: '2026-11-09'
aliases: []
tags:
- atlas/backbone
- subject/probability
- level/5
- study/foundation
node_kind: knowledge point
parent: '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Matrices & decompositions]]'
related:
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors]]'
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Rank and null spaces]]'
- '[[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection]]'
applied_in:
- '[[Backbone/Statistical computing & learning/Numerical methods & optimization/Numerical analysis for statistics/Numerical linear algebra/SVD for rank deficiency]]'
sources:
- '[[_system/Sources/linear]]'
- '[[raw/notes/2025-06-05-linear-algebra-29-svd.pdf]]'
---

# Singular value decomposition

Probability & mathematical foundations → Mathematical tools → Linear algebra for statistics → Matrices & decompositions → Singular value decomposition

Parent: [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Matrices & decompositions|Matrices & decompositions]]

## Definition and geometry

**SVD chooses orthonormal input and output bases in which a fixed linear map acts by nonnegative scaling.** Every real matrix $A\in\mathbb R^{m\times n}$ has a singular value decomposition

$$
A=U\Sigma V^\top,
\qquad U^\top U=UU^\top=I_m,
\qquad V^\top V=VV^\top=I_n.
$$

Here $U\in\mathbb R^{m\times m}$ and $V\in\mathbb R^{n\times n}$ are orthogonal; $I_m,I_n$ are identity matrices. The rectangular diagonal matrix $\Sigma\in\mathbb R^{m\times n}$ contains singular values $\sigma_1\ge\cdots\ge\sigma_q\ge0$, where $q=\min(m,n)$. Exactly $r=\operatorname{rank}(A)$ are positive. No symmetry, invertibility, or full-rank assumption is needed. Reference: MIT 18.06SC, [Lecture 29 summary, pp. 1–2 and 4](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/d273f75ee2552a5c3c35ccab37e5edce_MIT18_06SCF11_Ses3.5sum.pdf).

The **compact SVD** keeps only the positive singular values:

$$
\underbrace{A}_{m\times n}
=\underbrace{U_r}_{m\times r}
\underbrace{\Sigma_r}_{r\times r}
\underbrace{V_r^\top}_{r\times n},
\qquad \Sigma_r=\operatorname{diag}(\sigma_1,\ldots,\sigma_r).
$$

$U_r$ and $V_r$ contain the first $r$ columns of $U$ and $V$. Their columns are orthonormal, but the matrices are generally rectangular.

### Goal: match the row-space and column-space bases

Given $A$, find orthonormal row-space directions $v_1,\ldots,v_r$ whose images are perpendicular column-space directions. Their lengths are $\sigma_i$, and their normalized images are $u_i$:

![[assets/figures/2026-11-09-svd/handwritten-p06-basis-goal.png|720]]

*My original handwritten sketch and block equation, rendered without retouching from PDF p. 6. The clean equation below makes the compact dimensions explicit; the four-subspace diagram further below labels both zero spaces.*

$$
A\underbrace{\begin{bmatrix}v_1&v_2&\cdots&v_r\end{bmatrix}}_{V_r\;:\;n\times r}
=\underbrace{\begin{bmatrix}u_1&u_2&\cdots&u_r\end{bmatrix}}_{U_r\;:\;m\times r}
\underbrace{\begin{pmatrix}
\sigma_1&0&\cdots&0\\
0&\sigma_2&\cdots&0\\
\vdots&\vdots&\ddots&\vdots\\
0&0&\cdots&\sigma_r
\end{pmatrix}}_{\Sigma_r\;:\;r\times r}.
$$

This is $AV_r=U_r\Sigma_r$, or $Av_i=\sigma_i u_i$ one column at a time. The remaining input basis vectors lie in $\ker A$ and go to zero. Together, these actions determine $A=U_r\Sigma_rV_r^\top$.

### Reading the transformation

For an input $x\in\mathbb R^n$, $V^\top x$ gives coordinates along the input directions, $\Sigma$ scales them, and $U$ expresses the result in the output directions. In particular, $Av_i=\sigma_i u_i$ for $1\le i\le r$, with $v_i,u_i$ the corresponding columns. Orthogonal stages may rotate **or reflect**; they preserve Euclidean lengths.

![[assets/figures/2026-11-09-svd/svd_geometry.svg]]

*Original Codex illustration of the circle-to-ellipse idea in the supplied notes, p. 8. This invertible $2\times2$ example has singular values $2$ and $0.75$; every panel uses the same scale. Colors track paired directions, $e_1,e_2$ denote coordinate-axis unit vectors, and the dot tracks one input. A zero singular value would collapse a direction.*

## Constructing the paired bases

The two symmetric Gram matrices expose the singular vectors:

$$
A^\top A=V(\Sigma^\top\Sigma)V^\top,
\qquad AA^\top=U(\Sigma\Sigma^\top)U^\top.
$$

Both are **positive semidefinite**: $z^\top A^\top Az=\|Az\|_2^2\ge0$. The first is positive definite exactly when $A$ has independent columns; the second requires independent rows. Their positive eigenvalues are $\sigma_i^2$. The rectangular products above replace the ambiguous full-SVD shorthand $\Sigma^2$ in the handwriting.

Choose orthonormal eigenvectors $v_i$ of $A^\top A$. For each $\sigma_i>0$, set $u_i=Av_i/\sigma_i$. This also fixes the paired signs. The orthogonality calculation in the notes becomes, for $1\le i,j\le r$,

$$
u_i^\top u_j
=\frac{v_i^\top A^\top Av_j}{\sigma_i\sigma_j}
=\frac{\sigma_j^2}{\sigma_i\sigma_j}v_i^\top v_j
=\delta_{ij},
$$

where $\delta_{ij}$ is $1$ when $i=j$ and $0$ otherwise. Complete the bases using the null spaces; never divide by a zero singular value. Repeated eigenvalues permit an orthonormal choice within their eigenspaces, so singular vectors need not be unique. See MIT, [“Calculation” and “SVD example,” pp. 2–3](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/d273f75ee2552a5c3c35ccab37e5edce_MIT18_06SCF11_Ses3.5sum.pdf).

For the example introduced on p. 2 of the notes, one correctly paired choice is

$$
\begin{pmatrix}4&4\\-3&3\end{pmatrix}
=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\begin{pmatrix}4\sqrt2&0\\0&3\sqrt2\end{pmatrix}
\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
$$

## The four subspaces and projection

![[assets/figures/2026-11-09-svd/svd_four_subspaces.svg]]

*Original Codex reconstruction of my p. 6 sketch. The row-space patch contains $v_1,v_2$ and the column-space patch contains $u_1,u_2$; additional basis directions are suppressed. The dashed arrow ends at the output origin: $A(\ker A)=\{0\}$. The left null space is perpendicular to every possible output of $A$, and is sent to zero by $A^\top$.*

The full bases split the input and output spaces into orthogonal parts:

| Subspace | Ambient space | Orthonormal basis | Dimension |
| --- | --- | --- | --- |
| Row space $\operatorname{col}(A^\top)$ | $\mathbb R^n$ | $v_1,\ldots,v_r$ | $r$ |
| Null space $\ker A$ | $\mathbb R^n$ | $v_{r+1},\ldots,v_n$ | $n-r$ |
| Column space $\operatorname{col}(A)$ | $\mathbb R^m$ | $u_1,\ldots,u_r$ | $r$ |
| Left null space $\ker A^\top$ | $\mathbb R^m$ | $u_{r+1},\ldots,u_m$ | $m-r$ |

$A$ maps its row space bijectively onto its column space and sends its null space to zero. The compact factors give the orthogonal projectors

$$
P_{\rm col}=U_rU_r^\top,\qquad P_{\rm row}=V_rV_r^\top.
$$

Thus $U_r^\top U_r=I_r$, while $U_rU_r^\top=I_m$ only when $r=m$. The analogous condition for $V_rV_r^\top=I_n$ is $r=n$. This resolves the full-versus-compact distinction in pp. 13–14. References: MIT summary, p. 4; UBC CPSC 532D, [SVD appendix, §A.1](https://www.cs.ubc.ca/~dsuth/532D/26w1/notes/html/app_svd.html).

As an added connection to least squares, the Moore–Penrose pseudoinverse is $A^+=V_r\Sigma_r^{-1}U_r^\top$. For $b\in\mathbb R^m$, $A^+b$ is the minimum-Euclidean-norm least-squares solution and $AA^+b=P_{\rm col}b$ is its fitted projection, including when $A$ is rank deficient. See the same appendix, §A.2.

## Rank-one pieces and the best low-rank approximation

Multiplying a column by a row gives an entire matrix:

$$
A=\sum_{i=1}^r\sigma_i u_iv_i^\top,
\qquad Ax=\sum_{i=1}^r\sigma_i u_i(v_i^\top x).
$$

Each term has rank one: measure the input along $v_i$, scale by $\sigma_i$, and output along $u_i$. Keeping only the first $k$ terms defines $A_k=\sum_{i=1}^k\sigma_i u_iv_i^\top$; the upper limit is **$k$**, correcting p. 11.

For $0\le k<r$, the **Eckart–Young–Mirsky theorem** says $A_k$ minimizes the approximation error over matrices $B\in\mathbb R^{m\times n}$ with $\operatorname{rank}(B)\le k$ in each norm below:

| Matrix norm | Definition or singular-value formula | Minimum error $\lVert A-A_k\rVert$ |
| --- | --- | --- |
| Spectral | $\lVert A\rVert_2=\max_{\lVert x\rVert_2=1}\lVert Ax\rVert_2=\sigma_1$ | $\sigma_{k+1}$ |
| Frobenius | $\lVert A\rVert_F=\sqrt{\sum_{ij}A_{ij}^2}=\sqrt{\sum_i\sigma_i^2}$ | $\sqrt{\sum_{i=k+1}^r\sigma_i^2}$ |
| Nuclear | $\lVert A\rVert_*=\sum_i\sigma_i$ | $\sum_{i=k+1}^r\sigma_i$ |

These norms, and singular values themselves, are unchanged by compatible orthogonal multiplication on either side. The theorem concerns orthogonally invariant matrix norms; it does not extend automatically to the vector $1$- and $\infty$-norm formulas listed nearby in the notes. Reference: Ankur Moitra, *Algorithmic Aspects of Machine Learning*, [§2.1, p. 6, Theorems 2.1.2 and 2.1.4 and the intervening invariant-norm statement](https://assets.cambridge.org/97811071/84589/excerpt/9781107184589_excerpt.pdf#page=6).

For the diagonal example on p. 12, $A=\operatorname{diag}(4,3,2,1)$ and $A_2=\operatorname{diag}(4,3,0,0)$; the three errors are $2$, $\sqrt5$, and $3$. With $k=r$, reconstruction is exact.

## Why this gives PCA

**$V_r$ supplies feature weights; $U_r\Sigma_r$ contains the observations' actual PC values.** $U_r$ keeps the same score patterns at unit length, while $\Sigma_r$ supplies their scales.

Here the matrix is **data**: $X\in\mathbb R^{N\times d}$ has $N>1$ observations in rows and $d$ features in columns. Each column is centered; feature standardization is an additional choice. In this section, $r=\operatorname{rank}(X)$, and $u_i,v_i,\sigma_i$ refer to the SVD of $X$.

### Read the data as a sum of outer products

$$
\boxed{X=\sigma_1u_1v_1^\top+\sigma_2u_2v_2^\top+\cdots+\sigma_ru_rv_r^\top.}
$$

Each term is an $N\times d$ matrix: it describes **one component's contribution to every observation and feature**. Its two factors have different roles:

$$
\underbrace{\sigma_i u_i}_{N\times1\;\text{scores across observations}}
\underbrace{v_i^\top}_{1\times d\;\text{feature weights}}.
$$

| Quantity | What its entries refer to | Interpretation |
| --- | --- | --- |
| $v_i\in\mathbb R^d$ | One coefficient per **feature** | The unit principal direction/loading vector: $v_{ji}$ weights feature $j$ when computing PC $i$. |
| $t_i=Xv_i=\sigma_i u_i\in\mathbb R^N$ | One value per **observation** | The actual PC $i$ scores: $t_{\ell i}$ is observation $\ell$'s coordinate along that direction. |
| $u_i=t_i/\sigma_i\in\mathbb R^N$ | One normalized score per **observation** | The pattern of scores across observations, rescaled to have Euclidean length one. |
| $\sigma_i>0$ | One scale per **component** | The length $\lVert t_i\rVert_2$ of the score vector; its sample variance is $\sigma_i^2/(N-1)$. |
| $\sigma_i u_iv_i^\top=t_iv_i^\top$ | An entry for each observation–feature pair | Observation $\ell$ contributes the reconstructed row $t_{\ell i}v_i^\top$ through this component. |

“Loadings” here means the unit direction coefficients in $v_i$. Reference: Stanford STATS 305C, [*PCA (classical)*, “Relation to SVD,” “Back to reduced rank,” and “PCA = SVD”](https://web.stanford.edu/class/stats305c/slides/PCA_I.html).

### Why $Xv_1$ is the PC1 score vector

Let $x_\ell\in\mathbb R^d$ be observation $\ell$'s feature vector, so row $\ell$ of $X$ is $x_\ell^\top$. Multiplying by $v_1$ applies the **same feature weights to every row**:

$$
t_{\ell1}=x_\ell^\top v_1
=X_{\ell1}v_{11}+X_{\ell2}v_{21}+\cdots+X_{\ell d}v_{d1}.
$$

Because $v_1$ is a unit vector, this dot product is the observation's signed coordinate along the first principal direction. Stacking those coordinates gives $t_1=Xv_1$.

The outer-product expression gives the same answer directly. Orthonormality means $v_i^\top v_1=0$ for $i\ne1$ and $v_1^\top v_1=1$, so

$$
Xv_1
=\sigma_1u_1\underbrace{(v_1^\top v_1)}_{1}
+\sigma_2u_2\underbrace{(v_2^\top v_1)}_{0}
+\cdots
=\boxed{\sigma_1u_1}.
$$

Thus the compact score matrix is

$$
T=XV_r=U_r\Sigma_r
=\begin{bmatrix}\sigma_1u_1&\sigma_2u_2&\cdots&\sigma_ru_r\end{bmatrix}
\in\mathbb R^{N\times r}.
$$

Here $V_r$ is $d\times r$ and $U_r$ is $N\times r$. Each column of $U_r\Sigma_r$ contains one PC's actual values for all observations. See also CMU's [*Dimension Reduction*, June 29, 2021, first-PC weighted-sum and SVD slides](https://www.stat.cmu.edu/cmsac/sure/2021/materials/lectures/slides/16-PCA.html).

There is a useful **dual interpretation of $u_i$ as weights over observations**:

$$
X^\top u_i=\sum_{\ell=1}^N u_{\ell i}x_\ell=\sigma_i v_i.
$$

In this direction of multiplication, the coefficients in $u_i$ combine the observations' feature vectors to recover the scaled feature direction. In the usual PCA score calculation, the feature weights are in $v_i$, while $u_i$ records the normalized scores across observations. This matches the subspace sketch: $v_i$ lives in feature/input space $\mathbb R^d$; $u_i$ lives in observation/output space $\mathbb R^N$.

### A numerical example with feature-weight ratio $1:2$

Consider three already-centered observations with two features:

$$
X=\begin{pmatrix}1&7\\-5&-5\\4&-2\end{pmatrix},
\qquad C=\frac{X^\top X}{3-1}
=\begin{pmatrix}21&12\\12&39\end{pmatrix}.
$$

The unit principal directions are

$$
v_1=\frac1{\sqrt5}\begin{pmatrix}1\\2\end{pmatrix},
\qquad v_2=\frac1{\sqrt5}\begin{pmatrix}-2\\1\end{pmatrix}.
$$

Their covariance eigenvalues are $45$ and $15$, so the $1:2$ direction really is PC1 for these data. The vector $(1,2)^\top$ specifies the ratio; dividing by $\sqrt5$ makes its length one. Its coefficients multiply the **original feature columns**:

$$
Xv_1
=\frac1{\sqrt5}X_{:1}+\frac2{\sqrt5}X_{:2}
=\frac1{\sqrt5}\begin{pmatrix}1+2(7)\\-5+2(-5)\\4+2(-2)\end{pmatrix}
=\begin{pmatrix}3\sqrt5\\-3\sqrt5\\0\end{pmatrix}.
$$

$X_{:j}$ denotes feature column $j$. Observation 1 has PC1 value $3\sqrt5\approx6.708$; observation 2 has the opposite score; observation 3 has zero projection on PC1. The weights are shared, but the observations' feature values produce different scores.

Now separate score pattern from scale:

$$
\sigma_1=\lVert Xv_1\rVert_2=3\sqrt{10},
\qquad u_1=\frac{Xv_1}{\sigma_1}
=\frac1{\sqrt2}\begin{pmatrix}1\\-1\\0\end{pmatrix}.
$$

The first entry of $u_1$ is $1/\sqrt2$; multiplying by $\sigma_1$ restores the first observation's actual PC1 value $3\sqrt5$. Read as observation weights, this same $u_1$ takes observation 1 minus observation 2, divided by $\sqrt2$: $X^\top u_1=(x_1-x_2)/\sqrt2=\sigma_1v_1$.

For PC2, $u_2=(1,1,-2)^\top/\sqrt6$ and $\sigma_2=\sqrt{30}$. The two outer products are particularly simple:

$$
X=
\underbrace{\begin{pmatrix}3&6\\-3&-6\\0&0\end{pmatrix}}_{\sigma_1u_1v_1^\top}
+\underbrace{\begin{pmatrix}-2&1\\-2&1\\4&-2\end{pmatrix}}_{\sigma_2u_2v_2^\top}.
$$

*Original Codex example chosen to realize the requested $1:2$ loading ratio; it is not transcribed from the handwritten PDF.*

### How many singular values give how many PCs?

There are $r$ **positive** singular values and therefore $r$ nonzero-variance PCs. Keeping the largest $k$ positive singular values, with $1\le k\le r$, keeps $k$ PC score columns:

$$
T_k=\begin{bmatrix}\sigma_1u_1&\cdots&\sigma_ku_k\end{bmatrix}\in\mathbb R^{N\times k},
\qquad
X_k=T_kV_k^\top=\sum_{i=1}^k\sigma_i u_iv_i^\top\in\mathbb R^{N\times d},
$$

where $V_k=[v_1,\ldots,v_k]$. $T_k$ is the reduced dataset; $X_k$ reconstructs it in the original feature coordinates. Additional directions associated with zero singular values have zero scores and add no variation. Centering bounds the number of informative PCs by $r\le\min(d,N-1)$.

In the example, keeping $\sigma_1$ gives **one** PC score column and the first rank-one matrix above; keeping $\sigma_1,\sigma_2$ gives **two** score columns and reconstructs $X$ exactly. PC1 captures $\sigma_1^2/(\sigma_1^2+\sigma_2^2)=90/120=75\%$ of the total sample variance; PC2 captures the remaining $25\%$.

### Why these particular feature weights?

For a general centered matrix, sample covariance satisfies

$$
C=\frac{X^\top X}{N-1}
=V_r\frac{\Sigma_r^2}{N-1}V_r^\top.
$$

For any unit feature direction $w\in\mathbb R^d$, the score variance is

$$
\operatorname{var}_{\rm sample}(Xw)=w^\top Cw
\le\frac{\sigma_1^2}{N-1},
$$

with equality along a leading principal direction. Subsequent directions maximize remaining score variance subject to orthogonality. This joins the two interpretations in my notes: a maximum-variance coordinate system and the best low-rank reconstruction. PCA minimizes squared perpendicular reconstruction distances in feature space; ordinary regression minimizes squared response-direction residuals. References: Penn State, [STAT 897D §6.1](https://online.stat.psu.edu/stat857/node/36/); Moitra, §2.1, pp. 6–7, Theorems 2.1.2 and 2.1.5.

The notes also store observations in **columns**. For $Y=X^\top$, write the compact SVD as $Y=U_Y\Sigma_YV_Y^\top$. Covariance is $YY^\top/(N-1)$: its **left** singular vectors now carry feature weights, and the scores are $U_Y^\top Y=\Sigma_YV_Y^\top$, with PCs in rows and observations in columns. Always identify which matrix axis represents features before interpreting $u_i$ and $v_i$.

## Symmetric matrices and polar decomposition

For symmetric positive semidefinite $A$, an eigendecomposition $A=Q\Lambda Q^\top$ is an SVD with $U=V=Q$ and $\Sigma=\Lambda\ge0$. Merely being square, symmetric, or satisfying $A^\top A=AA^\top$ is insufficient for $U=V$: $\operatorname{diag}(2,-1)$ satisfies all three but cannot equal $U\Sigma U^\top$, which is always positive semidefinite. This corrects the implication on p. 8.

For **square** $A$, the p. 10 regrouping gives the left polar decomposition:

$$
A=\underbrace{(U\Sigma U^\top)}_{H}\,
\underbrace{(UV^\top)}_{Q},
\qquad H=(AA^\top)^{1/2}\succeq0,\quad Q^\top Q=I.
$$

$H$ is a symmetric stretch and $Q$ is orthogonal. Orthogonal determinants are $\pm1$, so the general square-matrix identity is $|\det A|=\prod_i\sigma_i$, correcting the determinant shorthand on p. 9. The polar factorization follows by applying Nick Higham's [“What Is the Polar Decomposition?”, opening definition and SVD construction](https://nhigham.com/2020/07/28/what-is-the-polar-decomposition/) to $A^\top$ and transposing.

## Source notes and checks

> [!info]- Source details
> Condensed from [[raw/notes/2025-06-05-linear-algebra-29-svd.pdf|the supplied handwritten PDF]], all 16 pages inspected: paired bases and four subspaces (pp. 1–7), orthogonality and geometry (pp. 7–9), compact/polar forms (pp. 9–10), rank approximation and norms (pp. 11–12), and PCA (pp. 13–16). The general row-reduction and matrix-subspace drills on pp. 3–5 remain in the original. The date comes from the supplied filename. Codex reorganized the explanation, corrected the conditions and notation beside the affected results, and added the worked factorization, explicit error formulas, pseudoinverse bridge, and counterexample. The original PDF is unchanged.
>
> The algebra and dimensions were checked against the cited statements; [[assets/figures/2026-11-09-svd/svd_geometry.py|reproducible numerical checks and figure code]] cover rectangular rank deficiency, paired signs, projectors, truncation errors, both PCA orientations, and the square polar identity. At the user's request, one original p. 6 excerpt is now embedded beside the basis-matching goal. [[assets/figures/2026-11-09-svd/svd_subspaces_pca.py|The subspace/PCA revision code]] reproduces that unretouched PDF excerpt, the separately labelled clean schematic, and checks the constructed PCA example. The toy data, expanded score interpretation, and clean diagram are Codex additions. Numerical examples support these checks; the general claims use the displayed arguments and cited theorems.

## Connections

- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Matrices & decompositions/Eigenvalues and eigenvectors|Eigenvalues and eigenvectors]] — The eigensystems of $A^\top A$ and $AA^\top$ supply right and left singular vectors, with eigenvalues equal to squared singular values.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Rank and null spaces|Rank and null spaces]] — Positive and zero singular values separate the four fundamental subspaces and expose their dimensions.
- [[Backbone/Probability & mathematical foundations/Mathematical tools/Linear algebra for statistics/Vectors, spaces & projections/Orthogonal projection|Orthogonal projection]] — Compact singular-vector factors form row/column projectors, connecting least-squares fits and PCA reconstruction.
- [[Backbone/Statistical computing & learning/Numerical methods & optimization/Numerical analysis for statistics/Numerical linear algebra/SVD for rank deficiency|SVD for rank deficiency]] — Singular values reveal rank and the compact factors construct a pseudoinverse without requiring an invertible Gram matrix.

```atlas
```
